"""Add/edit modals for tasks and projects.

Notes on the pitfalls these avoid:
- Select option labels are markup sinks too -> user text is a Text piece (A1, S1).
- ``Select.BLANK`` is a plain bool in textual 8.2.8, not a unique sentinel
  (A7). We never rely on it: ``allow_blank=False`` + an explicit "(none)"
  option whose value we map to ``None`` ourselves.
- Options are fixed at compose time, so ``set_options`` (which fires
  ``Changed``) is never called and needs no guard here.
"""

from __future__ import annotations

import calendar
import os
import re
from datetime import date, timedelta
from pathlib import Path

from unicodedata import east_asian_width

from rich._emoji_codes import EMOJI as _RICH_EMOJI
from rich.cells import cell_len, set_cell_size
from rich.text import Text

from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.keys import format_key
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.widgets import (Button, Checkbox, Input, Label, OptionList, Select, Static,
                             TextArea)
from textual.widgets.option_list import Option

from .models import (IMAGE_EXTS, PROJECT_COLORS, PROJECT_STATUSES, TASK_PRIORITIES,
                     Board, Project, Task, _new_id, city_names, dependents_chain,
                     is_open, link_candidates, link_conflicts, loopers_of,
                     open_dependents, project_archive_refusal,
                     grab_clipboard_image, grab_clipboard_text, parse_iso,
                     resolve_city, save_pil_image, templates)
from .boards import clean_name, move_plan, move_project, peek_board, slug
from .people import Directory, mention_ids
from .marks import COLOURS, SHAPES
from .keymap import KEY_STYLE, PRESENT_KEYS, key_line, palette_commands
from .views import (HEX, HOLLOW, board_chip_text, clip, fit, gantt_group_key, gantt_link_frame,
                    gantt_link_order, notes_text, valid_url)

# Imported at MODULE load (before the app starts) on purpose: textual-image
# detects the terminal's graphics support by QUERYING the terminal, which only
# works before Textual seizes it. A lazy import inside the viewer would run
# after app start -> detection fails -> silent low-res half-cell fallback.
try:
    from textual_image.widget import Image as AutoImage
except Exception:          # pragma: no cover - dependency present in prod
    AutoImage = None

NONE_VALUE = "__none__"

# The project's linked-dates rule (batch 2026-10-06-batch-01, LLR-604.5): the
# on-screen labels map to the engine's stored strings. The select always reads a
# stored value back leniently — absent or junk shows the default `push`.
DATE_LINKS_LABELS = ("stay", "push", "together")
DATE_LINKS_VALUES = ("flag", "push_delta", "together")
DATE_LINKS_DEFAULT = "push_delta"   # the engine's CASCADE_DEFAULT_MODE,
# re-spelled here so modals need not import the engine for one constant —
# keep the two in agreement (a comment is the leash; P4 ARCH4-2)

# The emoji table ships with rich (no new dependency). It is a PRIVATE module, so
# tests/test_emoji_picker.py asserts it is still there and still shaped like this
# — if a rich upgrade moves it, that goes red on purpose rather than this file
# quietly falling back to a shorter list nobody notices.
#
# ONLY SINGLE-CODEPOINT, EAST-ASIAN-WIDE ENTRIES ARE OFFERED, and that is the
# whole safety of this feature. The views size every row with `cell_len`, but
# the TERMINAL is what actually draws it, and for every other class the two
# disagree — measured over the 3,608 entries rich ships:
#
#   1 codepoint, EAW=W     1,483   cell_len 2, Unicode 2   <- offered
#   skin tones / flags     1,038   base + modifier: a terminal without the
#                                  modifier draws two glyphs, so 4 cells
#   ZWJ sequences            718   cell_len says 2, the parts sum to 4 (669 of
#                                  them), and an unsupported sequence draws 4
#   1 codepoint, EAW=N/A     337   cell_len says 1, terminals draw emoji at 2
#   variation selector        22   cell_len says 2, the base character is 1
#
# A width the ruler and the glass disagree about is a row that leans, which is
# exactly what a column layout cannot absorb — and it was seen on a real board
# before this filter existed. 1,483 is not a compromise: it is every emoji whose
# width is a fact rather than a negotiation.
def _unambiguously_wide(glyph: str) -> bool:
    """One codepoint, and BOTH rulers agree it is two cells.

    Requiring the agreement rather than either ruler alone is what makes this
    safe, and it is not belt-and-braces: the ten Fitzpatrick skin-tone
    modifiers (U+1F3FB..U+1F3FF, category Sk) are EAW=W yet measure 0 — they
    are not emoji at all, they modify the one before them. Unicode alone would
    have offered ten invisible choices."""
    return (len(glyph) == 1
            and east_asian_width(glyph) == "W"
            and cell_len(glyph) == 2)


_EMOJI_CHOICES = sorted(
    ((name, glyph) for name, glyph in _RICH_EMOJI.items()
     if _unambiguously_wide(glyph)),
    key=lambda pair: pair[0])

_EMOJI_BY_NAME = dict(_EMOJI_CHOICES)

EMOJI_RESULTS = 200        # how many hits the picker draws; it says when it cuts


def search_emoji(needle: str) -> list[tuple[str, str]]:
    """(name, glyph) pairs whose NAME contains `needle`. Space and underscore are
    the same key stroke here — the table spells them `flexed_biceps`, a human
    types 'flexed biceps' — and an empty needle is 'show me everything'.

    Exposed for the tests, which is why the picker holds no search logic of its
    own: the behaviour that decides what you can find is checkable without a UI."""
    q = needle.strip().lower().replace(" ", "_")
    if not q:
        return _EMOJI_CHOICES
    return [pair for pair in _EMOJI_CHOICES if q in pair[0]]

_WEEK_HEADER = "Mo Tu We Th Fr Sa Su"


class CalendarModal(ModalScreen[str | None]):
    """Arrow-key month calendar. Dismisses with 'YYYY-MM-DD' on Enter, None on
    Esc. Navigation: left/right ±1 day, up/down ±1 week, [ / ] (or PageUp/Down)
    ±1 month, t = today. Monday-first; stdlib calendar + datetime only.

    Nav bindings are priority so the focusable scroll container can't eat the
    arrows (pitfall A6)."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        Binding("left", "move(-1)", "-1d", show=False, priority=True),
        Binding("right", "move(1)", "+1d", show=False, priority=True),
        Binding("up", "move(-7)", "-1w", show=False, priority=True),
        Binding("down", "move(7)", "+1w", show=False, priority=True),
        Binding("left_square_bracket,pageup", "month(-1)", "-1m", show=False, priority=True),
        Binding("right_square_bracket,pagedown", "month(1)", "+1m", show=False, priority=True),
        Binding("t", "today", "Today", show=False, priority=True),
        Binding("enter", "pick", "Pick", show=False, priority=True),
    ]

    def __init__(self, initial: str | None = None):
        super().__init__()
        self._sel = parse_iso(initial) or date.today()

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="cal-box", classes="modal"):
            yield Label(self._title_text(), id="cal-title", classes="modal-title")
            yield Static(self._grid_text(), id="cal-grid")

    def _title_text(self) -> Text:
        return Text.assemble((f"{self._sel:%B %Y}", "bold"),
                             "  —  ←→ day · ↑↓ week · [ ] month · t today · enter pick")

    def _grid_text(self) -> Text:
        d = self._sel
        grid = Text()
        grid.append(_WEEK_HEADER, "dim")       # a piece: Text(style=) would dim every day
        for week in calendar.Calendar(firstweekday=0).monthdatescalendar(d.year, d.month):
            grid.append("\n")
            for i, day in enumerate(week):
                if i:
                    grid.append(" ")
                style = ("bold reverse" if day == d
                         else "dim" if day.month != d.month else "")
                grid.append(f"{day.day:2d}", style)
        return grid

    def _redraw(self) -> None:
        # NOT _render: that name is Textual's internal Widget._render(), which
        # must return a Visual. Overriding it to return None makes the screen's
        # own visual None and crashes Visual.to_strips (render_strips).
        self.query_one("#cal-title", Label).update(self._title_text())
        self.query_one("#cal-grid", Static).update(self._grid_text())

    def action_move(self, days: int) -> None:
        self._sel += timedelta(days=days)
        self._redraw()

    def action_month(self, delta: int) -> None:
        month_index = self._sel.month - 1 + delta
        year = self._sel.year + month_index // 12
        month = month_index % 12 + 1
        last = calendar.monthrange(year, month)[1]
        self._sel = self._sel.replace(year=year, month=month, day=min(self._sel.day, last))
        self._redraw()

    def action_today(self) -> None:
        self._sel = date.today()
        self._redraw()

    def action_pick(self) -> None:
        self.dismiss(self._sel.isoformat())

    def action_cancel(self) -> None:
        self.dismiss(None)


class EmojiPicker(ModalScreen[str | None]):
    """Find an emoji by NAME and return the glyph. Dismisses with the character
    on Enter, None on Esc.

    It returns the GLYPH, never the `:shortcode:`. A shortcode is 5+ characters
    that draw as 2, and the views measure what they are given — a title holding
    one would size its row wrong (see tests/test_cells.py). The glyph is a real
    character `views.vis()` can measure, so it costs the layout nothing.

    Zero-width entries are filtered out: they are combining parts, and an emoji
    you cannot see is one you cannot choose."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        Binding("down", "to_list", show=False, priority=True),
    ]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="emoji-box", classes="modal"):
            yield Label("[b]Insert emoji[/b]  —  type to search · ↓ then enter · esc close",
                        classes="modal-title")
            yield Input(placeholder="bug · rocket · fuego…", id="emoji-search")
            yield Label("", id="emoji-count")
            yield OptionList(id="emoji-list")

    def on_mount(self) -> None:
        self._show("")
        self.query_one("#emoji-search", Input).focus()

    def _show(self, needle: str) -> None:
        hits = search_emoji(needle)
        shown = hits[:EMOJI_RESULTS]
        lst = self.query_one("#emoji-list", OptionList)
        lst.clear_options()
        # keyed by NAME, not by glyph: names are unique, glyphs are NOT
        # (`-1` and `__1` are both the same thumbs-down), and duplicate option
        # ids raise DuplicateID.
        lst.add_options([Option(Text(f"{g}  {n.replace('_', ' ')}"), id=n)
                         for n, g in shown])
        # SAY when the list is cut. A picker that silently shows 200 of 900
        # teaches you the other 700 do not exist.
        note = (f"{len(hits)} matches · showing the first {len(shown)}"
                if len(hits) > len(shown) else f"{len(hits)} matches")
        self.query_one("#emoji-count", Label).update(
            Text(note) if hits else "[dim]no emoji by that name[/dim]")

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "emoji-search":
            self._show(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter in the search box takes the first hit — the common case is
        'type three letters, take the obvious one' without reaching for arrows."""
        hits = search_emoji(event.value)
        if hits:
            self.dismiss(hits[0][1])

    def action_to_list(self) -> None:
        self.query_one("#emoji-list", OptionList).focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(_EMOJI_BY_NAME.get(event.option.id))

    def action_cancel(self) -> None:
        self.dismiss(None)


class EmojiPickerMixin:
    """Ctrl+E opens the picker for the focused Input/TextArea and inserts the
    chosen glyph at the cursor. Same shape as ClipboardPasteMixin: each modal
    wires the binding itself, this supplies the action.

    The target is captured BEFORE the screen is pushed — pushing moves focus, so
    reading `app.focused` in the callback would find the picker, not the field."""

    def action_pick_emoji(self) -> None:
        target = self.app.focused
        if not isinstance(target, (Input, TextArea)):
            self.notify("Focus a text field to insert an emoji into.",
                        severity="warning")
            return
        self.app.push_screen(EmojiPicker(),
                             lambda glyph, t=target: self._insert_emoji(t, glyph))

    def _insert_emoji(self, target, glyph: str | None) -> None:
        if not glyph:
            return
        if isinstance(target, Input):
            target.insert_text_at_cursor(glyph)
        else:
            target.insert(glyph)
        target.focus()          # the picker took focus; give it back


class ClipboardPasteMixin:
    """Reliable Ctrl+V text paste for a modal: reads OS clipboard TEXT and
    inserts it into the focused Input/TextArea. Textual's native paste is
    unreliable on Windows, so we read the clipboard ourselves. Each modal wires
    the Ctrl+V binding in its own BINDINGS (Textual doesn't collect BINDINGS from
    a plain mixin); this class supplies the action."""

    def action_paste_text(self) -> None:
        target = self.app.focused
        if not isinstance(target, (Input, TextArea)):
            self.notify("Focus a text field to paste into.", severity="warning")
            return
        text = grab_clipboard_text()
        if not text:
            self.notify("Clipboard has no text.", severity="warning")
            return
        if isinstance(target, Input):
            target.insert_text_at_cursor(text)
        else:
            target.insert(text)


class ButtonKeysMixin:
    """A modal's button keys (batch 2026-10-20-batch-03, D-6): a key bound to
    `press_button('<id>')` presses that button, so the key and the button can never
    do different things. Each modal wires its keys in its own BINDINGS."""

    def action_press_button(self, button_id: str) -> None:
        self.query_one(f"#{button_id}", Button).press()


class DatePickerMixin:
    """Calendar-button handler: opens CalendarModal for a date field and writes
    the picked 'YYYY-MM-DD' back into that field's Input. Button ids are
    'cal-<field-id>' (e.g. 'cal-f-start')."""

    def _open_calendar(self, field_id: str) -> None:
        current = self.query_one(f"#{field_id}", Input).value.strip()
        self.app.push_screen(CalendarModal(current or None),
                             lambda res, fid=field_id: self._on_date_picked(fid, res))

    def _on_date_picked(self, field_id: str, result: str | None) -> None:
        if result:
            self.query_one(f"#{field_id}", Input).value = result


# The narrowest screen on which the editor's chip row fits on ONE row; below
# it the row folds in two. Measured, not derived: the sweep in
# tests/test_edit_window.py walks 80..140 columns and both sides of this value.
# Folded, the row needs 80 columns; below 80 the flags clip (80x24 is the
# smallest size this editor supports).
TASK_CHIPS_ONE_ROW = 137        # 122 + the milestone box (batch 2026-10-04-batch-02, p3_chip_threshold.py)


def notes_preview(text: str, people: dict | None = None) -> Text:
    """The notes as the board paints them: each line through the board's one
    highlight tokeniser, `highlight_segments` (a highlight never crosses a line
    there either), each segment a Text PIECE in its tone — `views.notes_text`.

    No parser reads the notes (S1, S-4): escaping and re-parsing them doubled
    backslashes and turned `:smile:` into an emoji, and handed to a Static as a
    str Textual's own parser read `[B]` or `[LINK=…` as tags — a note holding one
    crashed the editor and could arrive by team sync.

    With `people` (the directory's people by handle, batch 2026-10-21-batch-01), a
    mention of a person it holds is drawn `@Name` bold pink, inside any highlight;
    a mention of a handle it does not hold stays as typed, dimmed."""
    return Text.assemble(notes_text(text, people))      # one Text of plain pieces


# a key per button, beside text fields `alt+<letter>` (batch 2026-10-20-batch-03, D-6)
FORM_KEYS = [Binding("alt+s", "press_button('save')", "Save", priority=True)]
DATE_KEYS = [Binding("alt+t", "press_button('cal-f-start')", "Start date", priority=True),
             Binding("alt+d", "press_button('cal-f-due')", "Due date", priority=True)]
# the boxed modals' key line fits their box: `.modal` is 62 wide, its border and
# padding take 6, a scrollbar up to 2
MODAL_KEYS_W = 54
# short words, so `esc cancel` stays whole at 80 columns (DDR ux UX-DDR-2)
TASK_KEYS = [("alt+s", "save"), ("alt+m", "mark"), ("alt+i", "image"), ("alt+t", "start"),
             ("alt+d", "due"), ("esc", "cancel")]
# the class Select's cell cost on the chip row (its width 16 + one of gap):
# the one-row threshold rises by this when the directory holds classes
MARK_SELECT_W = 17


def mark_option_text(mark) -> Text:
    """A class as the Select's option: its shape in its colour and its name in
    the ink tone — Text pieces, never markup (C-17); `none` is the plain `◆`
    in `mut` (batch 2026-10-24-batch-01, HLR-2605)."""
    if mark is None:
        return Text.assemble(("◆ ", HEX["mut"]), ("none", HEX["mut"]))
    return Text.assemble((mark.shape + " ", HEX[mark.colour]), (mark.name, HEX["ink"]))


# the `@` picker in the notes (batch 2026-10-21-batch-01, the round's item 2, variant A):
# an `@` at a word start, then what is typed after it up to the cursor
MENTION_AT = re.compile(r"(?:^|(?<=\s))@([^\s@]*)$")
DROP_W = 44              # the dropdown's rows, inside its border and padding
DROP_ROWS = 5            # people listed at most; `+ add` comes after them
PICK_KEYS = [("↑↓", ""), ("↵", "pick"), ("esc", "plain text")]
# the new person's role is confirmed with ↵, never alt+s: in the editor alt+s saves the
# task (the round's D5 finding)
ADD_KEYS = [("↵", "add + mention"), ("⇥", "name / role"), ("esc", "back")]


def pick_rows(people: Directory, q: str, sel: int, w: int,
              limit: int) -> tuple[list[Text], list[tuple[str, object]]]:
    """The picker's rows and what each picks: the people `q` finds (name starts,
    then inside the name, then the role), at most `limit`, then `+ add 'q'` when `q`
    is not already someone's name. Every name and role is a Text piece."""
    opts: list[tuple[str, object]] = [("p", p) for p in people.find(q)[:limit]]
    if q.strip() and people.named(q) is None:
        opts.append(("add", q.strip()))
    rows = []
    for i, (kind, v) in enumerate(opts):
        on = i == sel
        r = Text(no_wrap=True)
        r.append("▶ " if on else "  ", HEX["accent"])
        if kind == "p":
            r.append(fit(v.name, 14), f"b {HEX['pink']}" if on else f"b {HEX['ink']}")
            r.append(" " + fit(v.role, max(0, w - 17)), HEX["mut"])
        else:
            r.append("+ add ", f"b {HEX['green']}")
            r.append(f"'{v}'", f"b {HEX['ink']}")
            r.append("  new person", HEX["dim"])
        r.truncate(w, pad=True)
        if on:
            r.stylize("on #1c2533")
        rows.append(r)
    if not opts:
        rows.append(Text(fit("  type a name", w), HEX["dim"]))
    return rows, opts


class MentionDrop(Vertical):
    """The dropdown under the notes' cursor: the people an `@` finds, or the new
    person's name and role. Drawn over the editor (`overlay: screen`)."""

    DEFAULT_CSS = f"""
    MentionDrop {{ overlay: screen; position: absolute; width: {DROP_W + 4}; height: auto;
                   background: #111827; border: round {HEX['pink']}; padding: 0 1;
                   display: none; }}
    MentionDrop #md-head {{ height: 1; }}
    MentionDrop #md-list {{ height: auto; }}
    MentionDrop Input {{ display: none; height: 3; border: tall #334154; }}
    MentionDrop #md-keys {{ height: 1; }}
    """

    def compose(self) -> ComposeResult:
        yield Static(id="md-head")
        yield Static(id="md-list")
        yield Input(placeholder="full name", id="md-name")
        yield Input(placeholder="role, e.g. Legal counsel", id="md-role")
        yield Static(id="md-keys")


class TaskModal(ClipboardPasteMixin, EmojiPickerMixin, DatePickerMixin, ButtonKeysMixin,
                ModalScreen[dict | None]):
    """Returns a dict of task fields on save, or None on cancel. With the people
    directory, an `@` at a word start in the notes opens the mention picker.
    With a marks directory that holds classes, the chip row gains the class
    Select after `milestone` (`alt+m`); an empty directory composes none."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True),
                Binding("ctrl+e", "pick_emoji", "Emoji", priority=True),
                *FORM_KEYS, *DATE_KEYS,
                Binding("alt+m", "mark", "Class", priority=True),
                Binding("alt+i", "press_button('paste-img')", "Paste image", priority=True),
                # the picker's own keys: they act only while it is open (check_action)
                Binding("up", "drop_move(-1)", "", priority=True, show=False),
                Binding("down", "drop_move(1)", "", priority=True, show=False),
                Binding("enter", "drop_pick", "", priority=True, show=False),
                Binding("tab", "drop_field", "", priority=True, show=False)]

    def __init__(self, board: Board, task: Task | None = None,
                 people: Directory | None = None, marks=None):
        super().__init__()
        self.board = board
        self._edit_task = task
        self._people = people
        # the class directory (batch 2026-10-24-batch-01): None or an empty one
        # composes NO class Select — the editor draws as before (HLR-2605)
        self._marks = marks
        # the Select's value as composed: the saved task is written only when
        # the operator CHANGED it — an untouched edit keeps the task's mark,
        # an id the directory lost included (the Changed message is no oracle:
        # Textual posts it on mount)
        self._mark_orig = ""
        # the picker: None (closed), "list" or "add"; the query after `@`, its column,
        # the highlighted row and the rows' choices
        self._mention: str | None = None
        self._q, self._at, self._row, self._sel, self._opts = "", 0, 0, 0, []
        # stable folder key for pasted images; a NEW task adopts it as its id on
        # save, so images live at images/<task-id>/.
        self._img_key = task.id if task else _new_id()

    def compose(self) -> ComposeResult:
        # Full screen (owner verdict 2026-09-30, variant C of the edit round):
        # the notes are the work, so they get the screen; every other control
        # sits on one-row strips around them, and nothing scrolls — the old
        # auto-height modal scrolled the title and Save away the moment you
        # typed in the notes. The `#task-*` rules live in taskboard.tcss.
        t = self._edit_task
        proj_options = [(Text("(none · Inbox)"), NONE_VALUE)] + [
            (Text(p.name), p.id) for p in self.board.projects
        ]
        proj_value = t.project_id if (t and t.project_id) else NONE_VALUE
        phases = self.board.phases
        with Vertical(id="task-box"):
            with Horizontal(id="task-head"):
                # the key is SAID: a picker nobody can find is a picker that
                # does not exist, and this app does not ship keys off-screen.
                yield Label(("[b]Edit task[/b]" if t else "[b]New task[/b]")
                            + "  [dim]· ctrl+e emoji[/dim]", classes="modal-title")
                yield Input(value=(t.title if t else ""), placeholder="what needs doing",
                            id="f-title")
                # the presentation flag (LLR-1602.3): in the title row because the
                # chip row's folded form already needs all 80 columns
                yield Checkbox("Show in presentation",
                               value=t.show_in_present if t else True, id="f-present")
            # two halves so the row can fold in two below TASK_CHIPS_ONE_ROW
            # (on_resize) instead of clipping the flags off the right edge
            with Horizontal(id="task-chips"):
                with Horizontal(id="task-chips-what"):
                    yield Select(proj_options, value=proj_value, allow_blank=False,
                                 id="f-project")
                    yield Select([(Text(p), p) for p in phases],
                                 value=(t.phase if (t and t.phase in phases) else phases[0]),
                                 allow_blank=False, id="f-phase")
                    yield Select([(Text(p), p) for p in TASK_PRIORITIES],
                                 value=(t.priority if t else "normal"),
                                 allow_blank=False, id="f-priority")
                    # one date, its due (LLR-601.3): in this half because the
                    # dates-and-flags half has no room left at 80 columns
                    yield Checkbox("milestone", value=bool(t.milestone) if t else False,
                                   id="f-milestone")
                    # the milestone's class (batch 2026-10-24-batch-01, variant A):
                    # beside `milestone`, like project/phase/priority; composed
                    # ONLY when the directory holds classes — an empty one draws
                    # no Select, and `+ new class…` is the manager's job, never
                    # an option here (the Select only picks)
                    if self._marks is not None and self._marks.marks:
                        cur = (t.mark if (t and t.mark in self._marks.marks) else "")
                        self._mark_orig = cur
                        opts = [(mark_option_text(None), "")]
                        opts += [(mark_option_text(m), cid)
                                 for cid, m in self._marks.marks.items()]
                        yield Select(opts, value=cur, allow_blank=False, id="f-mark")
                with Horizontal(id="task-chips-when"):
                    yield Input(value=(t.start_date or "" if t else ""),
                                placeholder="start", id="f-start", classes="date-input")
                    yield Button("📅", id="cal-f-start", classes="cal-btn")
                    yield Label("→", classes="task-arrow")
                    yield Input(value=(t.due_date or "" if t else ""),
                                placeholder="due", id="f-due", classes="date-input")
                    yield Button("📅", id="cal-f-due", classes="cal-btn")
                    yield Checkbox("blocked", value=bool(t.blocked) if t else False,
                                   id="f-blocked")
                    # the same flag `x` toggles — offered here because this is
                    # where a reader looks for it when the task is already open
                    yield Checkbox("archived", value=bool(t.archived) if t else False,
                                   id="f-archived")
                    yield Checkbox("pinned", value=bool(t.pinned) if t else False,
                                   id="f-pinned")
            with Horizontal(id="task-split"):
                with Vertical(id="task-edit"):
                    yield Label("Notes  [dim]==…== yellow · !!…!! red · ++…++ green[/dim]",
                                classes="task-sec")
                    yield TextArea(t.notes if t else "", id="f-notes")
                with Vertical(id="task-prev"):
                    yield Label("Preview  [dim]ctrl+v paste · esc cancel[/dim]",
                                classes="task-sec")
                    preview = VerticalScroll(id="task-preview-scroll")
                    preview.can_focus = False      # read-only: never a tab stop
                    with preview:
                        yield Static(notes_preview(t.notes if t else "", self.board.people),
                                     id="task-preview")
            with Horizontal(id="task-foot"):
                with Vertical(classes="task-foot-col"):
                    yield Label("URLs  [dim]one per line[/dim]", classes="task-sec")
                    yield TextArea("\n".join(t.urls) if t else "", id="f-urls")
                with Vertical(classes="task-foot-col"):
                    yield Label("Images  [dim]path or URL[/dim]", classes="task-sec")
                    yield TextArea("\n".join(t.images) if t else "", id="f-images")
                with Vertical(id="task-actions"):
                    yield Button("Paste image", variant="primary", id="paste-img")
                    yield Button("Save", variant="success", id="save")
                    yield Button("Cancel", variant="default", id="cancel")
            yield Static(id="task-keys")
        yield MentionDrop(id="mdrop")

    def on_mount(self) -> None:
        self._fit_width(self.app.size.width)

    def on_resize(self, event: events.Resize) -> None:
        self._fit_width(event.size.width)

    def _fit_width(self, width: int) -> None:
        """The chip row folds below `TASK_CHIPS_ONE_ROW` (plus the class Select's
        cost when the directory composes one); the key line drops words to fit
        (`#task-box` pads one cell each side)."""
        one_row = TASK_CHIPS_ONE_ROW + (MARK_SELECT_W if self.query("#f-mark") else 0)
        self.query_one("#task-chips").set_class(width < one_row, "-folded")
        keys = TASK_KEYS if self.query("#f-mark") else \
            [k for k in TASK_KEYS if k[0] != "alt+m"]
        self.query_one("#task-keys", Static).update(key_line(keys, width - 2))

    def action_mark(self) -> None:
        """`alt+m`: focus the class Select and open it (the round's variant A)."""
        sel = self.query_one("#f-mark", Select)
        sel.focus()
        sel.action_show_overlay()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "f-notes":
            self.query_one("#task-preview", Static).update(
                notes_preview(event.text_area.text, self.board.people))
            self.call_after_refresh(self._follow_cursor)
            if self._people is not None:
                if self._mention == "add" and event.text_area.has_focus:
                    self._close_drop()          # typing in the notes leaves the form (CR-1)
                if self._mention != "add":
                    self.call_after_refresh(self._scan)

    def on_text_area_selection_changed(self, event: TextArea.SelectionChanged) -> None:
        if event.text_area.id == "f-notes":
            self._follow_cursor()
            if self._mention == "list":
                self._scan()

    # ---- the `@` picker (batch 2026-10-21-batch-01) ---------------------------
    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action == "mark":
            # `alt+m` acts only where the class Select was composed (HLR-2605:
            # an empty directory draws none)
            return bool(self.query("#f-mark"))
        if action in ("drop_move", "drop_pick"):
            # the form acts only while it holds the focus, the list only while the notes
            # do and it lists something — otherwise the key is the field's (architect
            # A-5; code review CR-1, CR-4)
            if self._mention == "add":
                return self.query_one("#mdrop", MentionDrop).has_focus_within
            return self._mention == "list" and bool(self._opts)
        return True

    def on_descendant_focus(self, event: events.DescendantFocus) -> None:
        """The focus leaving the picker — the list's notes, or the new person's form —
        by `shift+tab` or a click closes it; the typed text stays as typed (architect
        A-5, code review CR-1)."""
        here = (self.query_one("#mdrop", MentionDrop).has_focus_within if self._mention == "add"
                else self.query_one("#f-notes", TextArea).has_focus)
        if self._mention is not None and not here:
            self._close_drop()

    def _scan(self) -> None:
        """Open, narrow or close the picker from the text before the notes' cursor:
        an `@` at a word start and what follows it, unless that is already a
        mention of someone the directory holds."""
        if self._mention == "add":
            return
        notes = self.query_one("#f-notes", TextArea)
        row, col = notes.cursor_location
        m = MENTION_AT.search(notes.document.get_line(row)[:col])
        # a mention of someone held — `@ana.ruiz.` too: the dot ends the sentence, not
        # the handle (HLR-2502; code review CR-2) — opens nothing
        if m is None or any(self._people.get(h) for h in mention_ids("@" + m.group(1))):
            self._close_drop()
            return
        if (self._mention, self._q) != ("list", m.group(1)):
            self._sel = 0
        self._mention, self._q, self._at, self._row = "list", m.group(1), m.start(), row
        self._draw_drop()

    def _draw_drop(self) -> None:
        drop = self.query_one("#mdrop", MentionDrop)
        name = drop.query_one("#md-name", Input)
        role = drop.query_one("#md-role", Input)
        listing = drop.query_one("#md-list", Static)
        head = Text(no_wrap=True)
        if self._mention == "list":
            rows, self._opts = pick_rows(self._people, self._q, self._sel, DROP_W, DROP_ROWS)
            if self._opts and self._sel >= len(self._opts):      # code review CR-3
                self._sel = len(self._opts) - 1
                rows, self._opts = pick_rows(self._people, self._q, self._sel, DROP_W, DROP_ROWS)
            head.append("@", f"b {HEX['pink']}")
            head.append(self._q, f"b {HEX['ink']}")
            head.append("▌", HEX["accent"])
            head.append("   mention a person", HEX["dim"])
            listing.update(Text.assemble(Text("\n").join(rows)))
            keys = PICK_KEYS
        else:
            head.append("New person", f"b {HEX['green']}")
            head.append("  · for every board", HEX["dim"])
            keys = ADD_KEYS
        head.truncate(DROP_W)
        drop.query_one("#md-head", Static).update(head)
        listing.display = self._mention == "list"
        name.display = role.display = self._mention == "add"
        drop.query_one("#md-keys", Static).update(key_line(keys, DROP_W))
        drop.display = True
        off = self.query_one("#f-notes", TextArea).cursor_screen_offset
        sw, sh = self.app.size
        x = max(0, min(off.x - len(self._q) - 1, sw - (DROP_W + 4)))
        y = off.y + 1 if off.y + 11 <= sh else max(0, off.y - 10)
        drop.styles.offset = (x, y)

    def _close_drop(self) -> None:
        self._mention = None
        self.query_one("#mdrop", MentionDrop).display = False

    def _insert_mention(self, handle: str) -> None:
        """`@<typed>` → `@<handle> `, only where the typed text still stands; a line
        changed meanwhile is left alone (code review CR-1)."""
        notes = self.query_one("#f-notes", TextArea)
        end = self._at + 1 + len(self._q)
        self._close_drop()
        if notes.document.get_line(self._row)[self._at:end] == "@" + self._q:
            notes.replace(f"@{handle} ", (self._row, self._at), (self._row, end))
        notes.focus()

    def action_drop_move(self, delta: int) -> None:
        if self._mention == "list":
            self._sel = max(0, min(len(self._opts) - 1, self._sel + delta))
            self._draw_drop()

    def action_drop_field(self) -> None:
        """`tab`: between the new person's name and role while they are open; the
        screen's own `tab` (the next field) otherwise — this binding replaces it."""
        if self._mention != "add":
            self.focus_next()               # leaving the notes closes the list (on_descendant_focus)
            return
        name = self.query_one("#md-name", Input)
        (self.query_one("#md-role", Input) if name.has_focus else name).focus()

    def action_drop_pick(self) -> None:
        if self._mention == "add":
            name = self.query_one("#md-name", Input).value
            role = self.query_one("#md-role", Input).value
            try:
                person = self._people.add(name, role)
            except (OSError, ValueError) as err:
                self.notify(f"The person was not added: {err}", title="People",
                            severity="error", markup=False)
                return
            self._insert_mention(person.id)
            return
        if not self._opts:
            return
        kind, v = self._opts[self._sel]
        if kind == "p":
            self._insert_mention(v.id)
            return
        self._mention = "add"
        self.query_one("#md-name", Input).value = v
        self.query_one("#md-role", Input).value = ""
        self._draw_drop()
        self.query_one("#md-role", Input).focus()

    def _follow_cursor(self) -> None:
        """Keep the preview on the part of the note being written. The preview
        wraps at its own width, so the line maps by proportion, not by row:
        the first line shows the top, the last line shows the bottom."""
        notes = self.query_one("#f-notes", TextArea)
        scroll = self.query_one("#task-preview-scroll", VerticalScroll)
        last = max(1, notes.document.line_count - 1)
        scroll.scroll_to(y=scroll.max_scroll_y * notes.cursor_location[0] / last,
                         animate=False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid == "save":
            self._save()
        elif bid == "paste-img":
            self._paste_image()
        elif bid.startswith("cal-"):
            self._open_calendar(bid[4:])
        else:
            self.dismiss(None)

    def _paste_image(self) -> None:
        """Grab an image (or image files) from the clipboard, persist a pasted
        bitmap under the task's image folder, and append the path(s) to the
        images field. Friendly notice when the clipboard has no usable image."""
        grabbed = grab_clipboard_image()
        if grabbed is None:
            self.notify("No image found in the clipboard.", severity="warning")
            return
        added: list[str] = []
        if isinstance(grabbed, list):                    # files copied in Explorer
            for p in grabbed:
                if Path(p).suffix.lower() in IMAGE_EXTS and os.path.isfile(p):
                    added.append(p)
            if not added:
                self.notify("Clipboard holds no image files.", severity="warning")
                return
        else:                                            # a raw bitmap
            dest = save_pil_image(self.board.image_dir(self._img_key), grabbed)
            added.append(str(dest))
        area = self.query_one("#f-images", TextArea)
        existing = area.text.rstrip("\n")
        area.text = (existing + "\n" if existing else "") + "\n".join(added)
        self.notify(f"Added {len(added)} image{'' if len(added) == 1 else 's'}.",
                    markup=False)

    def action_cancel(self) -> None:
        """`esc`: the picker's step back first — from the new person to the list,
        from the list to plain text — then the editor's cancel."""
        if self._mention == "add":
            self._mention = "list"
            self._draw_drop()
            self.query_one("#f-notes", TextArea).focus()
        elif self._mention == "list":
            self._close_drop()
        else:
            self.dismiss(None)

    def _val(self, wid: str) -> str:
        node = self.query_one(f"#{wid}")
        return str(node.value).strip()

    def _lines(self, wid: str) -> list[str]:
        """Non-blank, stripped lines from a multi-line TextArea, in order."""
        text = self.query_one(f"#{wid}", TextArea).text
        return [ln.strip() for ln in text.splitlines() if ln.strip()]

    def _save(self) -> None:
        title = self._val("f-title") or "Untitled"
        proj = self._val("f-project")
        urls = [v for v in (valid_url(ln) for ln in self._lines("f-urls")) if v]
        data = {
            "id": self._img_key,
            "title": title,
            "project_id": None if proj == NONE_VALUE else proj,
            "phase": self._val("f-phase"),
            "blocked": bool(self.query_one("#f-blocked", Checkbox).value),
            "archived": bool(self.query_one("#f-archived", Checkbox).value),
            "pinned": bool(self.query_one("#f-pinned", Checkbox).value),
            "milestone": bool(self.query_one("#f-milestone", Checkbox).value),
            "show_in_present": bool(self.query_one("#f-present", Checkbox).value),
            "priority": self._val("f-priority"),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
            "notes": self.query_one("#f-notes", TextArea).text.strip(),
            "urls": urls,
            "images": self._lines("f-images"),   # local paths valid at entry (no filter)
        }
        # the class (batch 2026-10-24-batch-01): written only when the operator
        # CHANGED the Select — an untouched edit keeps the task's mark (an id
        # the directory lost included), `none` saves with no `mark` (LLR-2602.1)
        mark_sel = next(iter(self.query("#f-mark")), None)
        if mark_sel is not None and str(mark_sel.value) != self._mark_orig:
            data["mark"] = str(mark_sel.value) or None
        self.dismiss(data)


class ProjectModal(ClipboardPasteMixin, EmojiPickerMixin, DatePickerMixin, ButtonKeysMixin,
                   ModalScreen[dict | None]):
    """Returns a dict of project fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True),
                Binding("ctrl+e", "pick_emoji", "Emoji", priority=True),
                *FORM_KEYS, *DATE_KEYS]

    def __init__(self, project: Project | None = None):
        super().__init__()
        self.project = project

    def compose(self) -> ComposeResult:
        p = self.project
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label(("[b]Edit project[/b]" if p else "[b]New project[/b]")
                        + "  [dim]· ctrl+e emoji[/dim]", classes="modal-title")
            yield Label("Name")
            yield Input(value=(p.name if p else ""), placeholder="project name", id="f-name")
            with Grid(classes="modal-grid"):
                yield Label("Color")
                yield Select([(Text(col), col) for col in PROJECT_COLORS],
                             value=(p.color if p else "violet"),
                             allow_blank=False, id="f-color")
                yield Label("Status")
                yield Select([(Text(s), s) for s in PROJECT_STATUSES],
                             value=(p.status if p else "on_track"),
                             allow_blank=False, id="f-status")
                yield Label("Pinned")
                yield Checkbox("pinned", value=bool(p.pinned) if p else False,
                               id="f-pinned")
                yield Label("Start (YYYY-MM-DD)")
                with Horizontal(classes="date-row"):
                    yield Input(value=(p.start_date or "" if p else ""), placeholder="optional",
                                id="f-start", classes="date-input")
                    yield Button("📅", id="cal-f-start", classes="cal-btn")
                yield Label("Due (YYYY-MM-DD)")
                with Horizontal(classes="date-row"):
                    yield Input(value=(p.due_date or "" if p else ""), placeholder="optional",
                                id="f-due", classes="date-input")
                    yield Button("📅", id="cal-f-due", classes="cal-btn")
            # the linked-dates rule lives OUTSIDE the pinned `.modal-grid` so the
            # grid's cell geometry (test_details_grid TC-411) is untouched.
            stored = p.extra.get("date_links") if p else None
            with Horizontal():
                yield Label("Linked dates")
                yield Select([(Text(label), value)
                              for label, value in zip(DATE_LINKS_LABELS, DATE_LINKS_VALUES)],
                             value=(stored if stored in DATE_LINKS_VALUES
                                    else DATE_LINKS_DEFAULT),
                             allow_blank=False, id="f-date-links")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")
            # the box is 62 wide: short words keep `esc cancel` (code review CR-1)
            yield Label(key_line([("alt+s", "save"), ("alt+t", "start"), ("alt+d", "due"),
                                  ("esc", "cancel")], MODAL_KEYS_W),
                        classes="modal-keys")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid == "save":
            self._save()
        elif bid.startswith("cal-"):
            self._open_calendar(bid[4:])
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _val(self, wid: str) -> str:
        return str(self.query_one(f"#{wid}").value).strip()

    def _save(self) -> None:
        data = {
            "name": self._val("f-name") or "Untitled",
            "color": self._val("f-color"),
            "status": self._val("f-status"),
            "pinned": bool(self.query_one("#f-pinned", Checkbox).value),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
            "date_links": self._val("f-date-links"),
        }
        self.dismiss(data)


class ProjectPicker(ModalScreen[None]):
    """Manage existing projects: edit / archive / delete, in place.

    Mutations persist immediately (Board.save) and re-render the board behind
    the modal, so the picker stays open for the next action. Option labels are
    markup sinks -> each line is a Text built from pieces (A1, S1, S-1: a synced
    status reached it as markup and carried a click action). Deleting a project reassigns
    its tasks to no-project (Inbox), the least-destructive choice — no task is
    ever lost to a project delete.
    """

    BINDINGS = [
        ("escape", "close", "Close"),
        ("e", "edit", "Edit"),
        ("x", "archive", "Archive"),
        ("d", "delete", "Delete"),
        ("m", "move_board", "Move to board"),
        Binding("j", "move(1)", show=False),
        Binding("k", "move(-1)", show=False),
    ]

    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="picker-box", classes="modal"):
            yield Label("[b]Projects[/b]  —  e edit · x archive · d delete · m move to board · "
                        "esc close",
                        classes="modal-title")
            yield OptionList(id="proj-list")

    def on_mount(self) -> None:
        self._reload()
        self.query_one("#proj-list", OptionList).focus()

    # ---- list rendering ----------------------------------------------------
    def _project_line(self, p: Project) -> Text:
        n = sum(1 for t in self.board.tasks if t.project_id == p.id)
        line = Text.assemble((p.name, "bold"), "  ·  ", p.status)
        if p.archived:
            line.append("  ·  ")
            line.append("archived", "dim")
        line.append(f"  ·  {n} task{'s' if n != 1 else ''}")
        return line

    def _reload(self, keep: str | None = None) -> None:
        """Rebuild the list from the board (clear-before-add avoids DuplicateIds)."""
        ol = self.query_one("#proj-list", OptionList)
        ol.clear_options()
        projects = self.board.projects
        if not projects:
            ol.add_option(Option("No projects yet — press esc, then p to add one.",
                                 disabled=True))
            return
        for p in projects:
            ol.add_option(Option(self._project_line(p), id=p.id))
        if keep is not None:
            for i, p in enumerate(projects):
                if p.id == keep:
                    ol.highlighted = i
                    break

    def _current(self) -> Project | None:
        ol = self.query_one("#proj-list", OptionList)
        idx = ol.highlighted
        if idx is None:
            return None
        return self.board.project_by_id(ol.get_option_at_index(idx).id)

    # ---- navigation / actions ---------------------------------------------
    def action_move(self, delta: int) -> None:
        projects = self.board.projects
        if not projects:
            return
        ol = self.query_one("#proj-list", OptionList)
        cur = ol.highlighted if ol.highlighted is not None else 0
        ol.highlighted = max(0, min(len(projects) - 1, cur + delta))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.action_edit()   # Enter / click on a row opens the editor

    def action_edit(self) -> None:
        proj = self._current()
        if proj is None:
            return
        self.app.push_screen(ProjectModal(proj),
                             lambda data, p=proj: self._on_edited(p, data))

    def _on_edited(self, proj: Project, data: dict | None) -> None:
        if not data:
            return
        for k, v in data.items():
            if k == "date_links":
                proj.extra["date_links"] = v
                continue
            setattr(proj, k, v)
        self.board.save()
        self.app.refresh_view()
        self._reload(keep=proj.id)

    def action_archive(self) -> None:
        proj = self._current()
        if proj is None:
            return
        if not proj.archived and self._refused(proj):
            return
        if not proj.archived:
            # Archiving a project also archives its open tasks: the project is the
            # container, and a project that is no longer active should not leave
            # its tasks drawing as active work in the lanes.
            open_tasks = [t for t in self.board.tasks
                          if t.project_id == proj.id and not t.archived]
            if open_tasks:
                msg = (f"Archive '{proj.name}'? Its {len(open_tasks)} open "
                       f"task{'s' if len(open_tasks) != 1 else ''} will be archived too.")
                self.app.push_screen(ConfirmModal(msg, confirm="Archive",
                                                  variant="warning"),
                                     lambda ok, p=proj: self._on_archive(p, ok))
                return
        self._do_archive_toggle(proj)

    def _on_archive(self, proj: Project, ok: bool) -> None:
        if not ok:
            return
        self._do_archive_toggle(proj)

    # ---- move to another board (batch 2026-10-20-batch-01, HLR-2206) ------------
    def action_move_board(self) -> None:
        proj = self._current()
        if proj is None:
            return
        app = self.app
        if app.board_id is None:
            # an unlisted board (`--open`, batch 2026-10-20-batch-03): no registry entry
            # to record the move from
            app.notify("This board is not listed (--open): open it with --board to move "
                       "its projects.", title="Boards", severity="warning", markup=False)
            return
        others = [e for e in app.registry.active() if e.id != app.board_id]
        if not others:
            app.notify("There is no other board to move it to — B, then n, creates one.",
                       title="Boards", severity="warning", markup=False)
            return
        boards = {e.id: peek_board(e.path) for e in others}
        n = sum(1 for t in self.board.tasks if t.project_id == proj.id)
        app.push_screen(MoveTarget(proj, n, others, boards),
                        lambda bid, p=proj: self._move_target(p, bid))

    def _move_target(self, proj: Project, bid: str | None) -> None:
        if not bid:
            return
        app = self.app
        # read again now: the picker's copy may be older than the file (security F1)
        dst = peek_board(app.registry.get(bid).path)
        plan = move_plan(self.board, dst, proj.id, app.move_team_ids(self.board),
                         app.move_team_ids(dst))
        if plan.refusal:
            app.notify(f"{proj.name} was not moved to {app.registry.get(bid).name}: "
                       f"{plan.refusal}.", title="Boards",
                       severity="warning", markup=False)
            return
        src_e, dst_e = app.registry.get(app.board_id), app.registry.get(bid)
        app.push_screen(MoveConfirm(plan, proj, self.board, src_e, dst_e,
                                    date.today().isoformat()),
                        lambda ok: self._move_confirmed(proj, dst, plan, src_e, dst_e, ok))

    def _move_confirmed(self, proj, dst, plan, src_e, dst_e, ok) -> None:
        if not ok:
            return
        app = self.app
        try:
            new_src, _steps = move_project(self.board, dst, proj.id, plan,
                                           date.today().isoformat(), (src_e.name, dst_e.name))
        except OSError as exc:
            if getattr(exc, "board", None) is not None:
                # the source file no longer holds the project: neither may the open
                # board, or the next save would write it back (architect A-27)
                app.after_move(exc.board)
                self.board = app.board
                self._reload()
            steps = getattr(exc, "steps", [])
            # the backups sentence only once a backup was made (ux UX-2, architect A-5)
            backups = (f" The backups (*.pre-move-{date.today().isoformat()}) are beside "
                       "each board file." if steps else "")
            app.notify(f"The move stopped: {exc}. Done: {', '.join(steps) or 'nothing'}."
                       + backups, title="Boards", severity="error", timeout=30, markup=False)
            return
        app.after_move(new_src)
        self.board = app.board
        self._reload()
        app.notify(f"Moved {proj.name} to {dst_e.name} · {len(plan.tasks)} tasks · "
                   f"{plan.kept} links kept · {len(plan.crossing)} dropped", title="Boards",
                   timeout=30, markup=False)

    def _refused(self, proj: Project) -> bool:
        """The guard (D-523): archiving a project archives its tasks, so it is
        refused while an open task outside it waits on one of them."""
        why = project_archive_refusal(self.board, proj.id)
        if why is not None:
            self.app.notify(why, title="Links", severity="warning", markup=False)
        return why is not None

    def _do_archive_toggle(self, proj: Project) -> None:
        if not proj.archived and self._refused(proj):     # judged again at yes
            return
        proj.archived = not proj.archived
        if not proj.archived and proj.present_rank is not None:
            # a rank another project took while this one was archived: back after the
            # last shown rank, never tied (architect A-10); no tie, its place kept (ux UX-1)
            ranks = [p.present_rank for p in self.board.visible_projects(False)
                     if p is not proj and p.present_rank is not None]
            if proj.present_rank in ranks:
                proj.present_rank = max(ranks) + 1
        for t in self.board.tasks:
            if t.project_id == proj.id:
                t.archived = proj.archived
        self.board.save()
        self.app.refresh_view()
        self._reload(keep=proj.id)

    def action_delete(self) -> None:
        proj = self._current()
        if proj is None:
            return
        n = sum(1 for t in self.board.tasks if t.project_id == proj.id)
        msg = f"Delete '{proj.name}'? Its {n} task{'s' if n != 1 else ''} move to Inbox."
        self.app.push_screen(ConfirmModal(msg),
                             lambda ok, p=proj: self._on_delete(p, ok))

    def _on_delete(self, proj: Project, ok: bool) -> None:
        if not ok:
            return
        self.board.delete_project(proj.id)   # tasks -> Inbox (project_id=None)
        self.app.refresh_view()
        self._reload()

    def action_close(self) -> None:
        self.dismiss(None)


class LinkPicker(ModalScreen[tuple[str, str] | None]):
    """`L` — "‹waiter› waits on…" (D-B2, LLR-502.2). Lists the open tasks the
    waiter could wait on — its own project first, then by due, undated last —
    filtered as you type; a linked row says ↵ removes it, a row that would close
    a loop is disabled and shows the loop. Returns ("link" | "unlink", task id),
    ("new", title) for the create row, ("ask", "") for the create row with an
    empty filter, or None. Every user text is a Text piece (S1)."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("down", "move(1)", "Down", priority=True, show=False),
                Binding("up", "move(-1)", "Up", priority=True, show=False)]

    DEFAULT_CSS = """
    LinkPicker { align: center middle; }
    #link-box { width: 100; max-width: 95%; height: 90%; padding: 1 2;
                background: #0d1219; border: round #334154; }
    #link-box Label { margin: 0; }
    #link-list { height: 1fr; margin-top: 1; }
    """

    def __init__(self, board: Board, waiter: Task):
        super().__init__()
        self.board = board
        self.waiter = waiter
        self._loopers = loopers_of(board, waiter)      # ONE walk per open (D-522)
        self._total = len(link_candidates(board, waiter, loopers=self._loopers))

    def compose(self) -> ComposeResult:
        w = self.waiter
        linked = [self.board.task_by_id(x) for x in dict.fromkeys(w.depends_on)]
        linked = [t for t in linked if t is not None and t is not w]
        now = Text("linked now: ", style=HEX["dim"])
        if linked:
            for i, t in enumerate(linked):
                now.append(" · " if i else "", style=HEX["dim"])
                now.append(t.title)
        else:
            now.append("nothing", style=HEX["dim"])
        with Vertical(id="link-box"):
            yield Label(Text.assemble((w.title, "bold"), " waits on…"), classes="modal-title")
            yield Input(placeholder="type to filter", id="link-filter")
            yield Label(Text(""), id="link-count")
            yield Label(now, id="link-linked")
            yield OptionList(id="link-list")
            yield Label(Text("↑↓ move  ·  ↵ link / unlink  ·  type filter  ·  esc cancel",
                             style=HEX["dim"]))

    def on_mount(self) -> None:
        self._fill("")
        self.query_one("#link-filter", Input).focus()

    def _meta(self, t: Task, same: bool) -> Text:
        due = parse_iso(t.due_date)
        bits = Text(style=HEX["dim"])
        if not same:
            p = self.board.project_by_id(t.project_id)
            bits.append(p.name if p else "Inbox")
            bits.append(" · ")
        bits.append(t.phase.upper())
        bits.append(" · " + (f"due {due:%b} {due.day}" if due else "no due"))
        return bits

    def _fill(self, query: str) -> None:
        ol = self.query_one("#link-list", OptionList)
        ol.clear_options()
        rows = link_candidates(self.board, self.waiter, query, loopers=self._loopers)
        q = query.strip()
        if q:
            create = Text.assemble("+ create “", q, "” as a new task it waits on")
        else:
            create = Text("+ create a new task it waits on")
        options = [Option(create, id="__new__")]
        first = None
        for same, heading in ((True, "Same project"), (False, "Other projects")):
            part = [c for c in rows if c.same_project == same]
            if not part:
                continue
            options.append(Option(Text(heading, style="bold"), disabled=True))
            for c in part:
                line = Text("  ")
                line.append(c.task.title, style="bold" if c.linked else "")
                line.append("   ")
                line.append_text(self._meta(c.task, same))
                line.append("\n    ")
                if c.loop:
                    names = [t.title for t in c.loop[1:-1]]
                    line.append("⟲ would loop: this → " + " → ".join(names) + " → this",
                                style=HEX["dim"])
                    line.stylize(HEX["dim"])
                else:
                    if c.linked:
                        line.append("✓ linked (↵ removes) · ", style=HEX["mut"])
                    line.append(c.hint, style=HEX["over"] if c.hint.startswith("◂")
                                else HEX["dim"])
                options.append(Option(line, id=f"c:{c.task.id}", disabled=bool(c.loop)))
                if first is None and not c.loop:
                    first = len(options) - 1
        ol.add_options(options)
        ol.highlighted = first if first is not None else 0
        self.query_one("#link-count", Label).update(
            Text(f"{len(rows)} of {self._total} open", style=HEX["dim"]))

    def on_input_changed(self, event: Input.Changed) -> None:
        self._fill(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        ol = self.query_one("#link-list", OptionList)
        if ol.highlighted is not None:
            self._choose(ol.get_option_at_index(ol.highlighted).id)

    def action_move(self, delta: int) -> None:
        ol = self.query_one("#link-list", OptionList)
        if delta > 0:
            ol.action_cursor_down()
        else:
            ol.action_cursor_up()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self._choose(event.option.id)

    def _choose(self, oid: str | None) -> None:
        if oid == "__new__":
            q = self.query_one("#link-filter", Input).value.strip()
            self.dismiss(("new", q) if q else ("ask", ""))
        elif oid and oid.startswith("c:"):
            tid = oid[2:]
            self.dismiss(("unlink" if tid in self.waiter.depends_on else "link", tid))

    def action_cancel(self) -> None:
        self.dismiss(None)


class TemplatePicker(ModalScreen[tuple[str, str] | None]):
    """`I` — "insert a process" (HLR-1301). Lists a leading `New template...`
    row, then the board's user templates, then the factory presets, each row
    `name — N tasks`; selecting a template returns `("insert", name)`, the
    `New template...` row returns `("new", "")`, `esc` returns None. Every user
    string is a Text piece (S1)."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    DEFAULT_CSS = """
    TemplatePicker { align: center middle; }
    #template-box { width: 64; max-width: 95%; height: auto; max-height: 90%;
                    padding: 1 2; background: #0d1219; border: round #334154; }
    #template-box Label { margin: 0; }
    #template-list { height: auto; margin-top: 1; }
    """

    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self._templates: list = []

    def compose(self) -> ComposeResult:
        with Vertical(id="template-box"):
            yield Label(Text.assemble(("◆ Templates", "bold"), " — insert a process"),
                        classes="modal-title")
            yield OptionList(id="template-list")
            yield Label(Text("↵ insert  ·  esc cancel", style=HEX["dim"]))

    def on_mount(self) -> None:
        ol = self.query_one("#template-list", OptionList)
        self._templates = templates(self.board)
        # the authoring row is NOT a template: it carries a reserved id the
        # selection handler recognises instead of indexing into `_templates`.
        options = [Option(Text("New template...", style="bold"), id="__new__")]
        for i, t in enumerate(self._templates):
            line = Text(t.name, style="bold")
            line.append(f" — {len(t.tasks)} tasks", style=HEX["dim"])
            options.append(Option(line, id=str(i)))
        ol.add_options(options)
        ol.highlighted = 0
        ol.focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = event.option.id
        if oid == "__new__":
            self.dismiss(("new", ""))
        else:
            self.dismiss(("insert", self._templates[int(oid)].name))

    def action_cancel(self) -> None:
        self.dismiss(None)


class TemplateEditor(ButtonKeysMixin, ModalScreen[dict | None]):
    """`I` → `New template...` — author a process from scratch (HLR-1501,
    LLR-1501.1). ONE name field and ONE multi-line tasks field (one task per
    line); Save returns ``{"name", "tasks"}`` — the name stripped and the tasks
    as stripped, non-blank lines in order — `esc` returns None. The linear chain
    is built by the caller: this modal only collects text, so it writes nothing
    and toasts nothing (S1: the name is user text and is never painted here as
    markup)."""

    BINDINGS = [("escape", "cancel", "Cancel"), *FORM_KEYS]

    DEFAULT_CSS = """
    TemplateEditor { align: center middle; }
    #modal-box #f-tasks { height: 8; border: tall #1b2431; background: #0b111a; }
    """

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label("[b]New template[/b]  [dim]· one task per line[/dim]",
                        classes="modal-title")
            yield Label("Name")
            yield Input(placeholder="template name", id="f-name")
            yield Label("Tasks")
            yield TextArea("", id="f-tasks")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")
            yield Label(key_line([("alt+s", "save"), ("esc", "cancel")], MODAL_KEYS_W),
                        classes="modal-keys")

    def on_mount(self) -> None:
        self.query_one("#f-name", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        else:
            self.dismiss(None)

    def _save(self) -> None:
        name = str(self.query_one("#f-name", Input).value).strip()
        text = self.query_one("#f-tasks", TextArea).text
        tasks = [ln.strip() for ln in text.splitlines() if ln.strip()]
        self.dismiss({"name": name, "tasks": tasks})

    def action_cancel(self) -> None:
        self.dismiss(None)


class MilestoneOffer(ModalScreen[list | None]):
    """The one-time milestone offer (M-3 as a migration, LLR-605.4): the board's
    one-day tasks pre-checked, its due-only tasks unchecked, each row naming its
    project, its date and how many open tasks wait on it. `space` toggles the
    highlighted row, `↵` answers with the checked tasks' own ids (by option index,
    never a re-parsed string), `esc` answers with none. Every user string is a Text
    piece (S1)."""

    BINDINGS = [("escape", "not_now", "Not now"),
                Binding("space", "toggle", "Toggle", priority=True, show=False)]

    DEFAULT_CSS = """
    MilestoneOffer { align: center middle; }
    #offer-box { width: 96; max-width: 100%; height: auto; max-height: 100%;
                 padding: 0 1; background: #0d1219; border: round #334154; }
    #offer-box Label { margin: 0; }
    #offer-box .modal-title { width: 100%; }
    #offer-list { height: auto; border: none; padding: 0; }
    """

    def __init__(self, board: Board, candidates: list, today: date):
        super().__init__()
        self.board = board
        self.today = today
        self._rows = [t for t, _p in candidates]
        self._on = [preset for _t, preset in candidates]
        self._index: dict[int, int] = {}          # option index -> row index

    def _offer_row(self, i: int) -> Text:
        """`▣ title   Project · Mon D[ · N waits on it]`: the title is cut with `…`
        to the cells the row leaves, so its project and date always show (code review
        O-1); only the box carries the colour (O-2)."""
        t = self._rows[i]
        p = self.board.project_by_id(t.project_id)
        d = parse_iso(t.due_date)
        waits = len(open_dependents(self.board, t))
        meta = Text("   ", style=HEX["dim"])
        meta.append(p.name if p else "Inbox")
        meta.append(f" · {d:%b} {d.day}")
        if waits:
            meta.append(f" · {waits} wait{'s' if waits == 1 else ''} on it")
        line = Text(no_wrap=True, overflow="ellipsis")
        line.append("▣ " if self._on[i] else "□ ",
                    style=HEX["accent"] if self._on[i] else HEX["mut"])
        line.append(clip(t.title, max(4, self._width() - 2 - meta.cell_len)), style="bold")
        line.append_text(meta)
        return line

    def _width(self) -> int:
        """The cells a row has: the list's own width once laid out, else the box's."""
        lists = self.query("#offer-list")
        w = lists.first().scrollable_content_region.width if lists else 0
        return w if w > 0 else min(96, self.app.size.width) - 6

    def _offer_keys(self) -> Text:
        n = sum(self._on)
        return Text(f"space toggle  ·  ↵ convert {n}  ·  esc not now — won't ask again",
                    style=HEX["dim"])

    def compose(self) -> ComposeResult:
        n = len(self._rows)
        with Vertical(id="offer-box"):
            # the board's chip first (batch 2026-10-20-batch-03, the round's item 7 A)
            yield Label(Text.assemble(board_chip_text(self.board.label),
                                      ("◆ Milestones", "bold"), " · convert one-day tasks?",
                                      (f"   {n} candidate{'s' if n != 1 else ''} · shown once",
                                       HEX["mut"])), classes="modal-title")
            yield Label(Text("Converting keeps the task, its links and its history; "
                             "it becomes a ◆ date.", style=HEX["dim"]))
            yield OptionList(id="offer-list")
            yield Label(self._offer_keys(), id="offer-keys")

    def on_mount(self) -> None:
        ol = self.query_one("#offer-list", OptionList)
        options = []
        first = None
        for preset, heading in ((True, "One-day tasks (start = due)"),
                                (False, "Due date, no start")):
            part = [i for i in range(len(self._rows)) if self._on[i] is preset]
            if not part:
                continue
            options.append(Option(Text(heading, style="bold"), disabled=True))
            for i in part:
                self._index[len(options)] = i
                if first is None:
                    first = len(options)
                options.append(Option(self._offer_row(i)))
        ol.add_options(options)
        ol.highlighted = first
        ol.focus()
        self._fit(self.app.size.height)
        self.call_after_refresh(self._repaint_rows)

    def _repaint_rows(self) -> None:
        """Re-cut every row to the width the list now has (after layout, on resize)."""
        ol = self.query_one("#offer-list", OptionList)
        for index, i in self._index.items():
            ol.replace_option_prompt_at_index(index, self._offer_row(i))

    def on_resize(self, event: events.Resize) -> None:
        self._fit(event.size.height)
        if self._index:
            self.call_after_refresh(self._repaint_rows)

    def _fit(self, height: int) -> None:
        """The list scrolls inside the screen so the title and the keys row stay
        painted at any height (ux UX-3): the box's border, title, line and keys
        row take 5 rows; one more is air."""
        self.query_one("#offer-list", OptionList).styles.max_height = max(3, height - 6)

    def action_toggle(self) -> None:
        ol = self.query_one("#offer-list", OptionList)
        i = self._index.get(ol.highlighted) if ol.highlighted is not None else None
        if i is None:
            return                                # a heading: nothing to toggle
        self._on[i] = not self._on[i]
        ol.replace_option_prompt_at_index(ol.highlighted, self._offer_row(i))
        self.query_one("#offer-keys", Label).update(self._offer_keys())

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss([self._rows[i].id for i in range(len(self._rows)) if self._on[i]])

    def action_not_now(self) -> None:
        self.dismiss([])


class PresentHiddenPicker(ModalScreen[None]):
    """`u` in the presentation (batch 2026-10-19-batch-01, HLR-2106): the items
    left out of it, one row each — a project, or a task (indented under its
    project in view 3) — `○` hidden, `●` shown. `↑↓` move, `space`/`↵` toggle
    the row's "show in presentation" flag and save the board at once (the row
    stays, with its new mark, so a second press undoes the first), `esc`/`q`/`u`
    close. Every name and title is a plain Text piece (S1)."""

    BINDINGS = [Binding("escape,q,u", "close", "Close", priority=True),
                Binding("up,k", "move(-1)", "", priority=True, show=False),
                Binding("down,j", "move(1)", "", priority=True, show=False),
                Binding("space,enter", "toggle", "Toggle", priority=True, show=False)]

    DEFAULT_CSS = """
    PresentHiddenPicker { align: center middle; }   /* its dimmed backdrop: taskboard.tcss */
    #picker-box { width: 64; max-width: 100%; height: auto; max-height: 100%;
                  padding: 0 1; background: #0d1219; border: round #334154; }
    #picker-box Static { margin: 0; }
    """

    def __init__(self, board: Board, rows: list[tuple[str, str, int]]):
        super().__init__()
        self.board = board
        self.rows = rows
        # the cursor starts on the first hidden row: a shown project is listed only
        # as the heading of its hidden tasks, and `space` on it would hide it
        self.cursor = next((i for i, (kind, oid, _) in enumerate(rows)
                            if not self._item(kind, oid).show_in_present), 0)

    def compose(self) -> ComposeResult:
        with Vertical(id="picker-box"):
            yield Static(Text("Hidden from the presentation", style=f"bold {HEX['bright']}"),
                         id="picker-title")
            yield Static(self._rows_text(), id="picker-rows")
            yield Static(Text("↑↓ move · ␣ show/hide · ○ hidden · esc close", style=HEX["dim"]),
                         id="picker-keys")

    def _item(self, kind: str, oid: str):
        return self.board.project_by_id(oid) if kind == "proj" else self.board.task_by_id(oid)

    def _rows_text(self) -> Text:
        if not self.rows:
            return Text("nothing hidden", style=HEX["dim"])
        out = Text(no_wrap=True, overflow="ellipsis")
        for i, (kind, oid, depth) in enumerate(self.rows):
            item = self._item(kind, oid)
            on = i == self.cursor
            if i:
                out.append("\n")
            out.append("▶ " if on else "  ", style=HEX["accent"])
            out.append("   " * depth)
            shown = item.show_in_present
            out.append("● " if shown else "○ ", style=HEX["accent"] if shown else HEX["dim"])
            out.append(item.name if kind == "proj" else item.title,
                       style=f"bold {HEX['accent']}" if on else HEX["bright"])
        return out

    def _repaint(self) -> None:
        self.query_one("#picker-rows", Static).update(self._rows_text())

    def action_move(self, delta: int) -> None:
        if self.rows:
            self.cursor = max(0, min(len(self.rows) - 1, self.cursor + delta))
            self._repaint()

    def action_toggle(self) -> None:
        if not self.rows:
            return
        kind, oid, _ = self.rows[self.cursor]
        item = self._item(kind, oid)
        item.show_in_present = not item.show_in_present
        self.board.save()
        self._repaint()

    def action_close(self) -> None:
        self.dismiss(None)


class PresentKeys(ModalScreen[None]):
    """`?` inside the presentation (batch 2026-10-20-batch-03, the round's item 3 A):
    every key of its seat `keymap.PRESENT_KEYS`, by group; a row that acts in the
    current view (or in every view) bright, another view's dimmed with that view in
    brackets. Never exported: `x` writes the frame only."""

    BINDINGS = [Binding("escape,question_mark,q", "dismiss", "", priority=True)]
    DEFAULT_CSS = """
    PresentKeys { align: center middle; }
    #pk-box { width: 60; max-width: 96%; height: auto; max-height: 96%; padding: 0 2;
              background: #0d1219; border: round #334154; }
    """

    def __init__(self, view: str):
        super().__init__()
        self.view = view

    def lines(self) -> Text:
        out = Text(no_wrap=True, overflow="ellipsis")
        out.append("PRESENTATION KEYS", style=f"bold {HEX['bright']}")
        out.append(f" · view {self.view}", style=HEX["mut"])
        group = None
        for row in PRESENT_KEYS:
            if row.group != group:
                group = row.group
                out.append(f"\n{group}", style=f"bold {HEX['mut']}")
            live = row.view is None or row.view == self.view
            out.append(f"\n  {row.show:<10}", style=KEY_STYLE if live else HEX["dim"])
            out.append(row.label, style=HEX["ink"] if live else HEX["dim"])
            if row.view:
                out.append(f"  ({row.view})", style=HEX["reached"] if live else HEX["dim"])
        out.append("\n? / esc close · dim = another view's key", style=HEX["dim"])
        return out

    def compose(self) -> ComposeResult:
        yield VerticalScroll(Static(self.lines(), id="pk-text"), id="pk-box")


class GanttLinkMode(ModalScreen[tuple[str, str] | None]):
    """`L` in the gantt — the link mode (D-A, LLR-502.3). The gantt is painted with
    the candidate as its selection (its group unfolds) and the proposed link drawn
    on the field; ↑/↓ choose among the open tasks in the gantt's order, skipping
    loops (marked `⟲`) and, with a filter, titles that do not hold it; every
    printable key is filter text, backspace edits it; ↵ links (or unlinks a linked
    candidate), esc cancels. The status rows are Text pieces (S1); the frame is the
    views seat's (D-405, the census's one EXEMPT repaint)."""

    BINDINGS = [Binding("escape", "cancel", "Cancel", priority=True),
                Binding("down", "move(1)", "Down", priority=True, show=False),
                Binding("up", "move(-1)", "Up", priority=True, show=False),
                Binding("enter", "choose", "Link", priority=True, show=False),
                Binding("backspace", "erase", "Erase", priority=True, show=False)]

    DEFAULT_CSS = """
    GanttLinkMode { background: #0b0f17; }
    #glink-frame { height: 1fr; }
    #glink-status { height: 3; }
    """

    def __init__(self, board: Board, waiter: Task, show_archived: bool, today: date):
        super().__init__()
        self.board, self.waiter = board, waiter
        self.show_archived, self.today = show_archived, today
        self.filter = ""
        by_id = {c.task.id: c for c in link_candidates(board, waiter)}
        order = gantt_link_order(board, show_archived, today, gantt_group_key(board, waiter))
        self._cands = [by_id[t.id] for t in order if t.id in by_id]
        self._loops = {c.task.id for c in self._cands if c.loop}
        self._cursor = next((i for i, c in enumerate(self._cands) if not c.loop), None)

    def compose(self) -> ComposeResult:
        yield Static(id="glink-frame")
        yield Static(id="glink-status")

    def on_mount(self) -> None:
        self._paint()

    def on_resize(self, event: events.Resize) -> None:
        self._paint()

    def _allowed(self, c) -> bool:
        q = self.filter.strip().lower()
        return not c.loop and (not q or q in c.task.title.lower())

    @property
    def candidate(self):
        if self._cursor is None or not self._allowed(self._cands[self._cursor]):
            return None
        return self._cands[self._cursor]

    def _paint(self) -> None:
        w, h = self.size.width or 118, self.size.height or 30
        cand = self.candidate
        right = f"{len(self._cands)} candidates · ⟲{len(self._loops)} would loop"
        rows = max(3, h - 3)
        frame, facts = gantt_link_frame(self.board, self.show_archived, self.waiter,
                                        cand.task if cand else None, self.today, w,
                                        rows, right, self._loops)
        # a closed waiter is never drawn, at any height: nothing to say (N2)
        folded = (is_open(self.board, self.waiter)
                  and self.waiter.id not in facts["line_map"])   # rows past the frame are not mapped
        self.query_one("#glink-frame", Static).update(frame)
        self.query_one("#glink-status", Static).update(self._status(cand, w, folded))

    def _status(self, cand, w: int, folded: bool = False) -> Text:
        """Three rows: what is being linked (titles clip to fit), the candidate's
        timing, then the keys — never clipped — with the first loop's path after
        them in what room is left."""
        linked = cand is not None and cand.linked
        out = Text(" LINK ", style="bold")
        if self.filter:
            out.append("filter: ", style=HEX["dim"])
            out.append(clip(self.filter, max(4, w // 3)) + "▏  ")
        fixed = out.cell_len + 11 + (10 if linked else 0)
        half = max(4, (w - 1 - fixed) // 2)
        waiter = clip(self.waiter.title, half)
        out.append(waiter)
        out.append(" waits on… ", style=HEX["dim"])
        if cand is not None:
            out.append(clip(cand.task.title, max(4, w - 1 - fixed - cell_len(waiter))), style="bold")
            if linked:
                out.append("  ✓ linked", style=HEX["mut"])
        else:
            out.append("no match" if self.filter else "nothing to link", style=HEX["dim"])
        out.truncate(w - 1, overflow="ellipsis")      # one row, whatever the glyphs
        out.append("\n ")
        if cand is not None:
            out.append(clip(cand.hint, w - 2),
                       style=HEX["over"] if cand.hint.startswith("◂") else HEX["dim"])
            if folded:
                # the frame could not unfold the waiter's group beside the
                # candidate's: say it rather than lose the link in silence (ux F4)
                # the title clips, the reason stays (code review 005 N1)
                room = w - 2 - cell_len(clip(cand.hint, w - 2))
                tail = " is folded — a taller terminal draws the link"
                if room >= len(tail) + 8:
                    out.append("  · " + clip(self.waiter.title, room - 4 - len(tail)) + tail,
                               style=HEX["dim"])
                elif room >= 20:
                    out.append("  · waiter row folded", style=HEX["dim"])
        keys = "↑↓ choose · type to filter · " + ("↵ unlink" if linked else "↵ link") + " · esc cancel"
        out.append("\n ")
        out.append(keys, style=HEX["dim"])
        first_loop = next((c for c in self._cands if c.loop), None)
        room = w - 2 - len(keys) - 11
        if first_loop is not None and room >= 8:
            path = ["this", *(t.title for t in first_loop.loop[1:-1]), "this"]
            out.append("   ⟲ loop: ", style=HEX["mut"])
            out.append(clip(" → ".join(path), room), style=HEX["dim"])
        return out

    def action_move(self, delta: int) -> None:
        n = len(self._cands)
        if not n:
            return
        i = self._cursor if self._cursor is not None else (-1 if delta > 0 else n)
        for _ in range(n):
            i = (i + delta) % n
            if self._allowed(self._cands[i]):
                self._cursor = i
                break
        self._paint()

    def on_key(self, event: events.Key) -> None:
        if event.character and event.character.isprintable() and len(event.character) == 1:
            self.filter += event.character
            event.stop()
            if self.candidate is None:
                self._cursor = None
                self.action_move(1)
            else:
                self._paint()

    def action_erase(self) -> None:
        self.filter = self.filter[:-1]
        if self.candidate is None:
            self._cursor = None
            self.action_move(1)
        else:
            self._paint()

    def action_choose(self) -> None:
        cand = self.candidate
        if cand is None:
            return
        self.dismiss(("unlink" if cand.linked else "link", cand.task.id))

    def action_cancel(self) -> None:
        self.dismiss(None)


class TeamIdentityPicker(ModalScreen[str | None]):
    """First-run team mode: ask the user to pick their identity from the roster.

    Returns the selected member ``id``, or ``None`` if cancelled.  The roster
    is the already-validated list from ``TeamState.roster()``.
    """

    BINDINGS = [("escape", "cancel", "Cancel")]
    DEFAULT_CSS = """
    #identity-box .modal-title { width: 100%; }
    """

    def __init__(self, roster: list[dict], label: tuple[str, str] | None = None):
        super().__init__()
        self._roster = roster
        self._label = label

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="identity-box", classes="modal"):
            # the board's chip first (batch 2026-10-20-batch-03, the round's item 7 A)
            yield Label(Text.assemble(board_chip_text(self._label),
                                      ("Operator identity", "bold"),
                                      "  —  pick from the team roster"), classes="modal-title")
            yield OptionList(id="identity-list")
            yield Label(key_line([("↵", "pick"), ("esc", "cancel")]), id="identity-keys")

    def on_mount(self) -> None:
        ol = self.query_one("#identity-list", OptionList)
        for member in self._roster:
            uid = member.get("id")
            if not isinstance(uid, str):
                continue
            name = member.get("name", uid)
            ol.add_option(Option(Text(str(name)), id=uid))
        if ol.option_count:
            ol.highlighted = 0
            ol.focus()

    def action_move(self, delta: int) -> None:
        ol = self.query_one("#identity-list", OptionList)
        cur = ol.highlighted if ol.highlighted is not None else 0
        ol.highlighted = max(0, min(ol.option_count - 1, cur + delta))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(event.option.id)

    def action_cancel(self) -> None:
        self.dismiss(None)


class ClockModal(ClipboardPasteMixin, ButtonKeysMixin, ModalScreen[dict | None]):
    """Pick the two ribbon clocks by CITY (type to find one). Returns city names."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True), *FORM_KEYS]

    def __init__(self, clock1: str, clock2: str):
        super().__init__()
        self._clock1 = clock1
        self._clock2 = clock2

    def compose(self) -> ComposeResult:
        # inline autocomplete: type "mad" -> suggests "Madrid" (accept with →/Enter)
        suggester = SuggestFromList(city_names(), case_sensitive=False)
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label("[b]Ribbon clocks[/b] — type a city", classes="modal-title")
            with Grid(classes="modal-grid"):
                yield Label("Clock 1")
                yield Input(value=self._clock1, suggester=suggester,
                            placeholder="find a city…", id="f-clock1")
                yield Label("Clock 2")
                yield Input(value=self._clock2, suggester=suggester,
                            placeholder="find a city…", id="f-clock2")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")
            yield Label(key_line([("alt+s", "save"), ("esc", "cancel")], MODAL_KEYS_W),
                        classes="modal-keys")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            # unknown / blank entry -> keep the current value (guarded)
            c1 = resolve_city(str(self.query_one("#f-clock1").value)) or self._clock1
            c2 = resolve_city(str(self.query_one("#f-clock2").value)) or self._clock2
            self.dismiss({"clock1": c1, "clock2": c2})
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class ConfirmModal(ButtonKeysMixin, ModalScreen[bool]):
    """Small yes/no confirm: `y` confirms, `n` or `esc` cancel, and a key line says
    so (batch 2026-10-20-batch-03, the round's item 6 B); the focus stays on the box,
    so a stray `enter` answers nothing. The message wraps in the box."""

    BINDINGS = [("escape", "no", "No"),
                Binding("y", "press_button('yes')", "Confirm", priority=True),
                Binding("n", "press_button('no')", "Cancel", priority=True)]

    def __init__(self, message: str, confirm: str = "Delete",
                 variant: str = "error"):
        super().__init__()
        self.message = message
        self.confirm = confirm
        self.variant = variant

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="confirm-box", classes="modal"):
            yield Label(Text(self.message), classes="modal-title")
            with Horizontal(classes="modal-buttons"):
                yield Button(Text(self.confirm), variant=self.variant, id="yes")
                yield Button("Cancel", variant="default", id="no")
            yield Label(key_line([("y", self.confirm.lower()), ("n / esc", "cancel"),
                                  ("⇥", "the buttons")]), id="confirm-keys")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

    def action_no(self) -> None:
        self.dismiss(False)


class TextPrompt(ButtonKeysMixin, ModalScreen[str | None]):
    """One-line text prompt. Dismisses with the STRIPPED text on Save/Enter and
    None on Cancel/Esc, so the caller can tell "left it blank" from "cancelled"."""

    BINDINGS = [("escape", "cancel", "Cancel"), *FORM_KEYS]

    def __init__(self, title: str, initial: str = "", placeholder: str = ""):
        super().__init__()
        self._title = title
        self._initial = initial
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label(Text(self._title, style="bold"), classes="modal-title")
            yield Input(value=self._initial, placeholder=self._placeholder, id="f-text")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")
            # `enter` in the field saves too (on_input_submitted; ux UX-13)
            yield Label(key_line([("↵ / alt+s", "save"), ("esc", "cancel")], MODAL_KEYS_W),
                        classes="modal-keys")

    def on_mount(self) -> None:
        self.query_one("#f-text", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        else:
            self.dismiss(None)

    def _save(self) -> None:
        self.dismiss(str(self.query_one("#f-text", Input).value).strip())

    def action_cancel(self) -> None:
        self.dismiss(None)


class PersonForm(ButtonKeysMixin, ModalScreen[tuple[str, str, str] | None]):
    """A person of the directory: name, role, an optional one-line note (batch
    2026-10-21-batch-01). Dismisses with the three fields stripped on Save /
    `enter` / `alt+s`, None on Cancel / `esc`; an empty name is refused in place.
    Editing never changes the person's handle, which the title shows."""

    BINDINGS = [("escape", "cancel", "Cancel"), *FORM_KEYS]

    def __init__(self, person=None):
        super().__init__()
        self._person = person

    def compose(self) -> ComposeResult:
        p = self._person
        title = Text("New person", style="bold") if p is None else Text.assemble(
            ("Edit person ", "bold"), (f"@{p.id}", f"b {HEX['pink']}"))
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label(title, classes="modal-title")
            # each field labelled: a value hides its placeholder (ux UX-8)
            yield Label("Name")
            yield Input(value=p.name if p else "", placeholder="name", id="f-name")
            yield Label("Role")
            yield Input(value=p.role if p else "", placeholder="role, e.g. Client A PM",
                        id="f-role")
            yield Label("Note")
            yield Input(value=p.note if p else "", placeholder="a note (optional)",
                        id="f-note")
            with Horizontal(classes="modal-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")
            yield Label(key_line([("↵ / alt+s", "save"), ("⇥", "next field"), ("esc", "cancel")],
                                 MODAL_KEYS_W), classes="modal-keys")

    def on_mount(self) -> None:
        self.query_one("#f-name", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        else:
            self.dismiss(None)

    def _save(self) -> None:
        name, role, note = (str(self.query_one(f"#f-{k}", Input).value).strip()
                            for k in ("name", "role", "note"))
        if not name:
            self.notify("A person needs a name.", severity="warning")
            self.query_one("#f-name", Input).focus()
            return
        self.dismiss((name, role, note))

    def action_cancel(self) -> None:
        self.dismiss(None)


class _ChoiceRow(Static, can_focus=True):
    """A form row of choices, ←→ moves: MarkForm's shape row and colour row
    (the round's ShapeRow, proto.py:731). The chosen cell is bracketed — the
    accent edge while the row holds the focus; the shape row wears the chosen
    colour, the colour row prints a block in each."""

    BINDINGS = [Binding("left", "step(-1)", "", show=False),
                Binding("right", "step(1)", "", show=False)]

    def __init__(self, label: str, items: list[str], index: int, form, **kw):
        super().__init__(**kw)
        self.label, self.items, self.i, self.form = label, items, index, form

    def on_mount(self) -> None:
        self._draw()

    def on_focus(self) -> None:
        self._draw()

    def on_blur(self) -> None:
        self._draw()

    def _draw(self) -> None:
        t = Text(no_wrap=True)
        t.append(f"{self.label:<7}", style=f"b {HEX['hd']}")
        hue = HEX[COLOURS[self.form.ci]]
        for j, it in enumerate(self.items):
            glyph, style = (it, hue) if self.label == "shape" else ("█", HEX[it])
            on = j == self.i
            edge = HEX["accent"] if (on and self.has_focus) else HEX["dim"]
            t.append("[" if on else " ", style=edge)
            t.append(glyph, style=style)
            t.append("]" if on else " ", style=edge)
        if self.label == "colour":
            t.append(f"  {COLOURS[self.i]}", style=HEX["dim"])
        if self.has_focus:
            t.append("   ←→", style=HEX["dim"])
        self.update(t)

    def action_step(self, delta: int) -> None:
        self.i = (self.i + delta) % len(self.items)
        if self.label == "colour":
            self.form.ci = self.i
        else:
            self.form.si = self.i
        self._draw()
        self.form._preview()


class MarkForm(ButtonKeysMixin, ModalScreen[str | None]):
    """The class form (the manager's `n` and `e`, batch 2026-10-24-batch-01,
    LLR-2606.2): the name, the shape row over `SHAPES`, the colour row over
    `COLOURS`, and a live preview of how the gantt draws the class open, late
    and reached. `alt+s` writes the DIRECTORY itself — a refused write says
    `The marks directory was not saved: <reason>` and KEEPS the form; a saved
    one dismisses with the class's id (kept on edit). `esc` cancels; `alt+n`/
    `alt+c`/`alt+h` focus their rows."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("alt+n", "focus_row('mf-name')", "Name", priority=True),
                Binding("alt+h", "focus_row('mf-shape')", "Shape", priority=True),
                Binding("alt+c", "focus_row('mf-colour')", "Colour", priority=True),
                *FORM_KEYS]

    DEFAULT_CSS = f"""
    MarkForm {{ align: center middle; }}
    #mf-box {{ width: 70; height: auto; background: #111827;
               border: round {HEX['accent']}; padding: 0 1; }}
    #mf-name {{ border: tall #334154; height: 3; }}
    #mf-shape, #mf-colour {{ height: 1; margin-top: 1; }}
    #mf-prev {{ margin-top: 1; height: auto; }}
    #mf-buttons {{ height: 3; margin-top: 1; }}
    #mf-buttons Button {{ width: auto; min-width: 8; margin-right: 1; }}
    """

    def __init__(self, cls_id: str | None = None):
        super().__init__()
        self.cls_id = cls_id

    def compose(self) -> ComposeResult:
        m = self.app.marks.marks.get(self.cls_id or "")
        title = Text("New class" if m is None else "Edit class", style="bold")
        title.append("  · every board", style=HEX["dim"])
        self.si = SHAPES.index(m.shape) if m else 4
        self.ci = COLOURS.index(m.colour) if m else 5
        with Vertical(id="mf-box"):
            yield Label(title, classes="modal-title")
            yield Input(value=m.name if m else "", placeholder="class name, e.g. Legal",
                        id="mf-name")
            yield _ChoiceRow("shape", SHAPES, self.si, self, id="mf-shape")
            yield _ChoiceRow("colour", COLOURS, self.ci, self, id="mf-colour")
            yield Static(id="mf-prev")
            with Horizontal(id="mf-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="default", id="cancel")
            # the whole line is 65 cells: it fits this box whole, `esc cancel`
            # and every field key named (the modal-keys law, AT-2604)
            yield Label(key_line([("alt+n", "name"), ("alt+c", "colour"), ("alt+h", "shape"),
                                  ("alt+s", "save"), ("esc", "cancel")], 66),
                        classes="modal-keys")

    def on_mount(self) -> None:
        self.query_one("#mf-name", Input).focus()
        self._preview()

    def on_input_changed(self, _event: Input.Changed) -> None:
        self._preview()

    def _preview(self) -> None:
        """The mark as every frame draws it (D1 B): shape + colour say the class,
        state moves to text — open, late (the date `over`), reached (hollow + ✓)."""
        if not self.query("#mf-prev"):
            return
        for rid in ("mf-shape", "mf-colour"):
            row = next(iter(self.query(f"#{rid}")), None)
            if row is not None:
                row._draw()
        shape, hue = SHAPES[self.si], HEX[COLOURS[self.ci]]
        name = self.query_one("#mf-name", Input).value.strip() or "…"
        t = Text(no_wrap=True)
        t.append("preview  ", style=HEX["dim"])
        t.append(shape, style=hue)
        t.append(f" {name}\n", style=HEX["ink"])
        for lab, glyph, date_s, dk, tail in (
                ("open", shape, "Nov 7", "mut", ""),
                ("late", shape, "Oct 18", "over", ""),
                ("reached", HOLLOW.get(shape, shape), "Oct 5", "reached", "✓")):
            t.append(f"  {lab:<9}", style=HEX["dim"])
            t.append("··┆····", style=HEX["dim"])
            t.append(glyph, style=hue)
            t.append(tail, style=HEX["reached"])
            t.append(f" {date_s}", style=HEX[dk])
            t.append(" ···┆··\n", style=HEX["dim"])
        self.query_one("#mf-prev", Static).update(t)

    def action_focus_row(self, wid: str) -> None:
        self.query_one(f"#{wid}").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()
        else:
            self.dismiss(None)

    def _save(self) -> None:
        name = str(self.query_one("#mf-name", Input).value).strip()
        if not name:
            self.notify("A class needs a name.", severity="warning")
            self.query_one("#mf-name", Input).focus()
            return
        shape, colour = SHAPES[self.si], COLOURS[self.ci]
        try:
            m = (self.app.marks.add(name, shape, colour) if self.cls_id is None
                 else self.app.marks.edit(self.cls_id, name, shape, colour))
        except (OSError, ValueError) as err:
            # the form stays: the operator fixes the name or cancels (LLR-2606.2)
            self.notify(f"The marks directory was not saved: {err}",
                        title="Milestone classes", severity="error", markup=False)
            return
        self.dismiss(m.id)

    def action_cancel(self) -> None:
        self.dismiss(None)


SEARCH_TEXT_KEYS = [("↵ / alt+s", "filter"), ("esc", "cancel")]
# fits the boxed modal's 54 cells whole, `esc cancel` kept (code review CR-1 of 2026-10-20)
SEARCH_PERSON_KEYS = [("↑↓", ""), ("↵ / alt+s", "filter"), ("alt+p", "their page"),
                      ("esc", "cancel")]


class SearchPrompt(TextPrompt):
    """`/` — the filter, with people (batch 2026-10-21-batch-01, the round's item 3,
    variant A): text filters the tasks as before; an `@` starts a person — the
    list shows the directory's names only (`@` alone, all of them), `↑`/`↓`
    choose, `enter` / `alt+s` filter to the tasks that mention them (`@handle`),
    `alt+p` opens their page in the people view (`open_person`)."""

    BINDINGS = [Binding("up", "move(-1)", "", priority=True, show=False),
                Binding("down", "move(1)", "", priority=True, show=False),
                Binding("alt+p", "page", "", priority=True, show=False)]
    DEFAULT_CSS = "#sp-list { height: auto; margin: 0 0 1 0; }"

    def __init__(self, title: str, initial: str = "", placeholder: str = "", *,
                 people: Directory, open_person) -> None:
        super().__init__(title, initial, placeholder)
        self._people = people
        self._open_person = open_person
        self._sel, self._opts = 0, []

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#modal-box").mount(Static(id="sp-list"), after="#f-text")
        self.call_after_refresh(self._draw)

    def _person_mode(self) -> bool:
        return str(self.query_one("#f-text", Input).value).startswith("@")

    def on_input_changed(self, event: Input.Changed) -> None:
        self._sel = 0
        self._draw()

    def _draw(self) -> None:
        listing = self.query_one("#sp-list", Static)
        if self._person_mode():
            q = str(self.query_one("#f-text", Input).value)[1:]
            held = self._people.get(q.lower())
            # `/` reopened on a person's filter (`@ana.ruiz`) lists that person first
            # (code review CR-1 of increment 005)
            rows, opts = pick_rows(self._people, held.name if held else q, self._sel,
                                   MODAL_KEYS_W - 2, 6)
            self._opts = [v for kind, v in opts if kind == "p"]
            rows = rows[:len(self._opts)] or [Text("  no one by that name", HEX["dim"])]
            listing.update(Text.assemble(Text("\n").join(
                [Text("PEOPLE · names only", f"b {HEX['pink']}")] + rows)))
            keys = SEARCH_PERSON_KEYS
        else:
            self._opts = []
            listing.update(Text.assemble(("text filters tasks · ", HEX["dim"]),
                                         ("@", f"b {HEX['pink']}"),
                                         (" starts a person", HEX["dim"])))
            keys = SEARCH_TEXT_KEYS
        self.query_one(".modal-keys", Label).update(key_line(keys, MODAL_KEYS_W))

    def action_move(self, delta: int) -> None:
        self._sel = max(0, min(len(self._opts) - 1, self._sel + delta))
        self._draw()

    def _save(self) -> None:
        if self._person_mode() and self._opts:
            self.dismiss("@" + self._opts[self._sel].id)
        else:
            super()._save()

    def action_page(self) -> None:
        if self._opts:
            handle = self._opts[self._sel].id
            self.dismiss(None)
            self._open_person(handle)


class PhaseEditor(ModalScreen[None]):
    """Manage the board's ORDERED phases: add / rename / reorder / delete.

    Mutations persist immediately (Board.save) and re-render the board behind
    the modal, so the editor stays open for the next action. Phase names are
    user text -> a Text piece everywhere they are rendered (A1, S1). Renaming moves the
    tasks that referenced the old name and deleting reassigns them to a
    neighbour, so no edit here can orphan a task; the last phase can't be
    deleted because every view indexes into the list.
    """

    BINDINGS = [
        ("escape", "close", "Close"),
        ("a", "add", "Add"),
        ("e", "rename", "Rename"),
        ("d", "delete", "Delete"),
        Binding("left_square_bracket", "reorder(-1)", "Earlier"),
        Binding("right_square_bracket", "reorder(1)", "Later"),
        Binding("j", "move(1)", show=False),
        Binding("k", "move(-1)", show=False),
    ]

    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="picker-box", classes="modal"):
            # the literal [ is escaped so Rich prints the key instead of
            # reading it as the start of a markup tag
            yield Label("[b]Phases[/b]  —  a add · e rename · d delete · "
                        "\\[ / ] reorder · esc close", classes="modal-title")
            yield OptionList(id="phase-list")

    def on_mount(self) -> None:
        self._reload()
        self.query_one("#phase-list", OptionList).focus()

    # ---- list rendering ----------------------------------------------------
    def _phase_line(self, index: int, name: str) -> Text:
        n = sum(1 for t in self.board.tasks if t.phase == name)
        return Text.assemble((f"{index + 1}.", "dim"), "  ", (name, "bold"),
                             f"  ·  {n} task{'s' if n != 1 else ''}")

    def _reload(self, keep: int | None = None) -> None:
        """Rebuild the list from the board (clear-before-add avoids DuplicateIds)."""
        ol = self.query_one("#phase-list", OptionList)
        ol.clear_options()
        phases = self.board.phases
        for i, name in enumerate(phases):
            ol.add_option(Option(self._phase_line(i, name)))
        if phases:
            ol.highlighted = max(0, min(len(phases) - 1, keep or 0))

    def _committed(self, keep: int) -> None:
        self.board.save()
        self.app.refresh_view()
        self._reload(keep=keep)

    def _current_index(self) -> int | None:
        """Position of the highlighted phase, or None when nothing is selected.
        Rows carry no id — a phase is identified by its position, which is the
        thing reordering changes."""
        idx = self.query_one("#phase-list", OptionList).highlighted
        if idx is None or not (0 <= idx < len(self.board.phases)):
            return None
        return idx

    # ---- navigation / actions ---------------------------------------------
    def action_move(self, delta: int) -> None:
        phases = self.board.phases
        if not phases:
            return
        ol = self.query_one("#phase-list", OptionList)
        cur = ol.highlighted if ol.highlighted is not None else 0
        ol.highlighted = max(0, min(len(phases) - 1, cur + delta))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.action_rename()   # Enter / click on a row renames it

    def action_add(self) -> None:
        self.app.push_screen(TextPrompt("New phase", placeholder="phase name"),
                             self._on_added)

    def _on_added(self, name: str | None) -> None:
        if name is None:
            return
        if not name:
            self.notify("A phase needs a name.", severity="warning")
            return
        if not self.board.add_phase(name):
            self.notify(f"'{name}' already exists.", severity="warning", markup=False)
            return
        self._committed(len(self.board.phases) - 1)

    def action_rename(self) -> None:
        i = self._current_index()
        if i is None:
            return
        old = self.board.phases[i]
        self.app.push_screen(TextPrompt("Rename phase", initial=old),
                             lambda new, o=old: self._on_renamed(o, new))

    def _on_renamed(self, old: str, new: str | None) -> None:
        if new is None or new == old:
            return
        if not new:
            self.notify("A phase needs a name.", severity="warning")
            return
        if not self.board.rename_phase(old, new):
            self.notify(f"'{new}' already exists.", severity="warning", markup=False)
            return
        self._committed(self.board.phases.index(new))

    def action_delete(self) -> None:
        i = self._current_index()
        if i is None:
            return
        if len(self.board.phases) <= 1:
            self.notify("A board needs at least one phase.", severity="warning")
            return
        name = self.board.phases[i]
        target = self.board.phases[i - 1] if i > 0 else self.board.phases[1]
        n = sum(1 for t in self.board.tasks if t.phase == name)
        self.app.push_screen(
            ConfirmModal(f"Delete '{name}'? Its {n} task{'s' if n != 1 else ''} "
                         f"move to '{target}'."),
            lambda ok, nm=name, k=i: self._on_delete(nm, k, ok))

    def _on_delete(self, name: str, index: int, ok: bool) -> None:
        if not ok or not self.board.delete_phase(name):
            return
        self._committed(max(0, index - 1))

    def action_reorder(self, delta: int) -> None:
        i = self._current_index()
        if i is None:
            return
        if not self.board.move_phase(self.board.phases[i], delta):
            return
        self._committed(i + delta)      # follow the phase to its new position

    def action_close(self) -> None:
        self.dismiss(None)


def image_block(ref: str):
    """Render one image reference inline (crisp via terminal graphics where
    supported, else a fallback line). Remote URLs are listed as links; a
    missing / unrenderable local file yields a dim notice. A generator of
    widgets, shared by ImageViewer and TaskDetails. Never raises."""
    if valid_url(ref):                       # remote: can't inline; link it
        yield Label(Text(f"link · {ref}"))
        return
    path = Path(ref)
    if path.suffix.lower() not in IMAGE_EXTS or not path.is_file():
        yield Label(Text.assemble(("missing:", "dim"), f" {ref}"))
        return
    if AutoImage is None:
        yield Label(Text.assemble(("(install textual-image to preview)", "dim"), f" {ref}"))
        return
    try:
        img = AutoImage(str(path))           # size comes from the Image TCSS rule
    except Exception:                        # never blank the modal on one bad file
        yield Label(Text.assemble(("could not render:", "dim"), f" {ref}"))
        return
    yield img
    yield Label(Text(path.name, style="dim"))


class ImageViewer(ModalScreen[None]):
    """Show a task's images rescaled inline — crisp via the terminal graphics
    protocol where the terminal supports it (e.g. WezTerm), half-block/Unicode
    fallback otherwise. ``o`` opens every image raw in its OS-default app /
    browser; ``esc`` closes. Remote URLs are listed as links (``o`` opens them).
    """

    BINDINGS = [("escape", "close", "Close"), ("o", "open_raw", "Open raw")]

    def __init__(self, task: Task, board: Board):
        super().__init__()
        self._view_task = task
        self._board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="viewer-box", classes="modal"):
            yield Label(
                Text.assemble((self._view_task.title, "bold"), "  —  o open raw · esc close"),
                classes="modal-title")
            if not self._view_task.images:
                yield Label("[dim]No images on this task.[/dim]")
                return
            for ref in self._view_task.images:
                yield from image_block(ref)

    def action_open_raw(self) -> None:
        self.app.open_all_images_raw(self._view_task)

    def action_close(self) -> None:
        self.dismiss(None)


class TaskDetails(ModalScreen[None]):
    """Every field on a task, with images rendered inline — read-only but for
    its links (D-B, LLR-503.1): the dependency section lists what it waits on
    and what it unblocks (direct and down the chain), with each conflict; `x`
    removes the highlighted direct link, `↵` jumps to it, `L` adds one through
    the picker, `tab` moves between the box and the links. ``o`` opens
    images/URLs raw, ``esc`` closes. Every user-controlled string is a Text
    piece, never parsed (markup-injection pitfall A1, S1)."""

    BINDINGS = [("escape", "close", "Close"), ("o", "open_raw", "Open raw"),
                ("L", "link", "Link"), ("x", "remove", "Remove link"),
                ("enter", "jump", "Jump"),
                Binding("tab", "focus_links", "Links", priority=True, show=False)]

    DEFAULT_CSS = """
    #deps-list { height: auto; max-height: 14; border: none; padding: 0; }
    """

    def __init__(self, task: Task, board: Board):
        super().__init__()
        self._detail_task = task     # NOT self._task: collides with Textual's pump task
        self._board = board

    def compose(self) -> ComposeResult:
        t = self._detail_task
        proj = self._board.project_by_id(t.project_id)
        proj_name = proj.name if proj else "Inbox"
        with VerticalScroll(id="details-box", classes="modal"):
            yield Label(Text.assemble((t.title, "bold"), "  —  o open raw · esc close"),
                        classes="modal-title")
            with Grid(classes="modal-grid"):
                yield Label("Project")
                yield Label(Text(proj_name))
                yield Label("Phase")
                yield Label(Text(t.phase + (" · blocked" if t.blocked else "")
                                 + (" · ◆ milestone" if t.milestone else "")))
                yield Label("Priority")
                yield Label(Text(t.priority))
                yield Label("Start")
                yield Label(Text(t.start_date or "—"))
                yield Label("Due")
                yield Label(Text(t.due_date or "—"))
            yield from self._links()
            yield Label("[b]Notes[/b]  [dim]highlight: ==…== yellow, !!…!! red, ++…++ green[/dim]")
            if t.notes:
                yield Static(notes_preview(t.notes, self._board.people))
            else:
                yield Static("[dim]—[/dim]")
            yield Label("[b]URLs[/b]")
            if t.urls:
                for u in t.urls:
                    yield Label(Text(f"link · {u}"))
            else:
                yield Label("[dim]—[/dim]")
            yield Label("[b]Images[/b]")
            if t.images:
                for ref in t.images:
                    yield from image_block(ref)
            else:
                yield Label("[dim]—[/dim]")

    # ---- the dependency section (D-B) -------------------------------------
    def _links(self):
        t, b = self._detail_task, self._board
        by_id: dict[str, Task] = {}
        for x in b.tasks:
            by_id.setdefault(x.id, x)          # the first of a repeated id
        preds = [by_id[x] for x in dict.fromkeys(t.depends_on) if x != t.id and x in by_id]
        # each predecessor's OWN state (code review F1, operator "Corregir en el
        # 003"): a closed task still lists what it waited on, truthfully
        open_preds = [p for p in preds if is_open(b, p)]
        chain = dependents_chain(b, t)
        direct = [w for w, depth in chain if depth == 1]
        if not is_open(b, t):
            state = ""                         # closed: neither waiting nor ready
        elif open_preds:
            state = "  ◂ waiting"
        elif preds and is_open(b, t):
            state = "  ready"
        else:
            state = ""
        keys = ("  L link · tab links · x remove · ↵ jump" if preds or direct
                else "  L link")
        yield Label(Text.assemble(("Dependencies", "bold"), (state, HEX["mut"]),
                                  (keys, HEX["dim"])), id="deps-head")
        if not preds and not chain:
            yield Label(Text("no links — L adds one", style=HEX["dim"]))
            return
        ol = OptionList(id="deps-list")
        options = [Option(Text.assemble(("Waits on", "bold"),
                                        (f"  ◂{len(open_preds)} open of {len(preds)}",
                                         HEX["dim"])), disabled=True)]
        for p in preds:
            state = ("open" if p in open_preds else
                     "archived" if p.archived else "done")
            options.append(Option(self._row(p, state), id=f"p:{p.id}"))
        options.append(Option(Text.assemble(
            ("Unblocks", "bold"),
            (f"  ▸{len(direct)} direct · {len(chain)} in chain", HEX["dim"])), disabled=True))
        for w, depth in chain:
            if depth == 1:
                options.append(Option(self._row(w, None), id=f"d:{w.id}"))
            else:
                options.append(Option(Text.assemble("  " * (depth - 1) + "└ ",
                                                    self._row(w, None)), disabled=True))
        ol.add_options(options)
        yield ol
        for p, n in link_conflicts(b, t):
            yield Label(Text.assemble(("◂ ", HEX["over"]), self._conflict(t, p, n)))

    def _row(self, task: Task, state: str | None) -> Text:
        due = parse_iso(task.due_date)
        meta = f"{task.phase.upper()} · " + (f"due {due:%b} {due.day}" if due else "no due")
        if state:
            meta += f" · {state}"
        return Text.assemble(task.title, "   ", (meta, HEX["dim"]))

    @staticmethod
    def _conflict(t: Task, p: Task, n: int) -> Text:
        def md(iso):
            d = parse_iso(iso)
            return f"{d:%b} {d.day}"
        if parse_iso(t.start_date) is not None:
            head = f"starts {md(t.start_date)}, overlaps "
        else:
            head = f"due {md(t.due_date)}, overlaps "
        return Text.assemble(head, p.title, f" by {n}d (due {md(p.due_date)})")

    def on_mount(self) -> None:
        self.query_one("#details-box").focus()

    def _highlighted(self) -> str | None:
        lists = self.query("#deps-list")
        if not lists:
            return None
        ol = lists.first(OptionList)
        if ol.highlighted is None:
            return None
        return ol.get_option_at_index(ol.highlighted).id

    def _repaint(self) -> None:
        self.refresh(recompose=True)
        self.call_after_refresh(lambda: self.query_one("#details-box").focus())

    def action_focus_links(self) -> None:
        lists = self.query("#deps-list")
        if not lists:
            return
        ol = lists.first(OptionList)
        if ol.has_focus:
            self.query_one("#details-box").focus()
        else:
            ol.focus()
            if ol.highlighted is None or ol.get_option_at_index(ol.highlighted).disabled:
                ol.action_cursor_down()

    def action_remove(self) -> None:
        oid = self._highlighted()
        if not oid:
            return
        t = self._detail_task
        other = self._board.task_by_id(oid[2:])
        if other is None:
            return
        if oid.startswith("p:"):
            self.app.unlink_tasks(t, other)
        else:
            self.app.unlink_tasks(other, t)
        self._repaint()

    def action_jump(self) -> None:
        oid = self._highlighted()
        if oid:
            self.dismiss(None)
            self.app.jump_to(oid[2:])

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id:
            self.dismiss(None)
            self.app.jump_to(event.option.id[2:])

    def action_link(self) -> None:
        self.app.open_link_picker(self._detail_task, after=self._repaint)

    def action_open_raw(self) -> None:
        self.app.open_all_images_raw(self._detail_task)

    def action_close(self) -> None:
        self.dismiss(None)


def keys_grid(cells: list[str], width: int) -> list[str]:
    """`cells` (`<show> <label>`) laid out column-major in as many columns as
    `width` holds — each column the longest cell plus two — so the list reads
    down, then across, and no row is wider than `width` (one column when even
    one cell does not fit)."""
    if not cells:
        return []
    cw = max(cell_len(c) for c in cells) + 2
    ncol = max(1, width // cw)
    rows = -(-len(cells) // ncol)
    out = []
    for r in range(rows):
        row = [cells[c * rows + r] for c in range(ncol) if c * rows + r < len(cells)]
        out.append("".join(x + " " * (cw - cell_len(x)) for x in row).rstrip())
    return out


GLOBAL_LEAD = "Global  "


def global_lines(entries: list[str], width: int) -> list[str]:
    """`Global  <show> <label>  <show> <label> …` packed into `width`, breaking
    only between entries; a continuation row is indented under the first entry."""
    lines, cur = [], GLOBAL_LEAD
    for e in entries:
        joined = e if cur in (GLOBAL_LEAD, " " * len(GLOBAL_LEAD)) else "  " + e
        if cell_len(cur + joined) > width and cur.strip():
            lines.append(cur.rstrip())
            cur, joined = " " * len(GLOBAL_LEAD), e
        cur += joined
    lines.append(cur.rstrip())
    return lines


def _clip_words(s: str, width: int) -> str:
    """Clip `s` to `width` cells at a WORD boundary, appending `…` when cut.

    Textual's default label wrap breaks a long word mid-glyph and drops the
    rest; the `?` help lines must instead end at a word boundary or with `…`.
    An unbreakable token longer than `width` clips at the edge with `…`."""
    if width <= 0:
        return ""
    if cell_len(s) <= width:
        return s
    out = ""
    for word in s.split():
        candidate = f"{out} {word}" if out else word
        if cell_len(candidate) <= width - 1:      # one cell for the `…`
            out = candidate
        else:
            break
    if out:
        return out + "…"
    return set_cell_size(s, width - 1) + "…"


class _HelpLine(Label):
    """A single help line whose `tail` is clipped at a word boundary to the
    cells the column leaves after `prefix` (the swatch, or a bullet marker).

    Subclasses `Label` (not `Static`) so the suite's `query("Label")` reads it,
    and takes the column width (`1fr`) so `render()` sees the true cells."""

    def __init__(self, prefix: Text, tail: str, tail_style: str | None = None):
        super().__init__("")
        self.styles.height = 1
        self.styles.width = "1fr"
        self._prefix = prefix
        self._tail = tail
        self._tail_style = tail_style

    def render(self) -> Text:
        width = self.content_size.width if self.content_size else self.size.width
        room = max(0, width - self._prefix.cell_len)
        clipped = _clip_words(self._tail, room)
        if self._tail_style:
            return Text.assemble(self._prefix, Text(clipped, style=self._tail_style))
        return Text.assemble(self._prefix, clipped)


class HelpModal(ModalScreen[None]):
    """`?` — the per-view help family: what the view is for, how to read it,
    and what keys work inside it.

    The left side carries the USAGE copy (one section per view), the right side
    carries the live legend and an annotated example; under both, a full-width
    band lists the view's keys column-major, sized to the box. Docked at the
    bottom, outside the scroll, the global palette-only keys (`R` Present, `S`
    Standup, … — read from `KEYMAP`, never typed here) and the closing hint: they
    are visible at every size, however long the body (batch
    2026-10-16-batch-01, LLR-1603.1/.2). From here `m` opens the FULL keymap
    and `?` opens the command palette.
    """

    BINDINGS = [
        Binding("escape,q", "close", "Close", key_display="esc/q"),
        Binding("question_mark", "palette", "Palette"),
        Binding("m", "map", "Map"),
    ]

    DEFAULT_CSS = """
    HelpModal { align: center middle; }
    #help-modal-box {
        width: 110; max-width: 95%; height: auto; max-height: 90%;
        padding: 1 2; background: #0d1219; border: round #334154;
        scrollbar-size-vertical: 1;   /* the body scrolls as one: keep the columns' width */
    }
    #help-modal-box .modal-title { margin: 0 0 1 0; }
    #help-left { width: 48; height: auto; }
    #help-right { width: 1fr; height: auto; }
    #help-cols { height: auto; }
    #help-keys-title { margin: 1 0 0 0; }
    #help-foot { dock: bottom; height: auto; }
    #help-global, #help-hint { width: 100%; }
    """

    def __init__(self, mode: str, board: Board, today=None, size=(96, 30),
                 show_archived: bool = False,
                 team_state=None, team_filter: str = "equipo",
                 selected_id: str | None = None, gantt_focus: str | None = None,
                 gantt_previous: str | None = None, kanban_presentation: str = "grouped",
                 kanban_group: str = "project", kanban_focus: str | None = None):
        super().__init__()
        self._mode = mode
        self._kanban = {"kanban_presentation": kanban_presentation,   # the kanban's legend
                        "kanban_group": kanban_group,                 # reads what it draws
                        "kanban_focus": kanban_focus}                 # (code review K-1)
        self._selected_id = selected_id      # the gantt's legend reads the frame
        self._gantt_focus = gantt_focus      # the screen shows (code review F3)
        self._gantt_previous = gantt_previous
        self._board = board
        self._today = today
        self._show_archived = show_archived
        self._dims = size
        self._team_state = team_state
        self._team_filter = team_filter

    def compose(self) -> ComposeResult:
        from .views import help_example, help_usage, legend_entries
        entries = legend_entries(self._mode, self._board, self._today,
                                 *self._dims, show_archived=self._show_archived,
                                 team_state=self._team_state,
                                 team_filter=self._team_filter,
                                 selected_id=self._selected_id,
                                 gantt_focus=self._gantt_focus,
                                 gantt_previous=self._gantt_previous, **self._kanban)
        example, example_meaning = help_example(self._mode)
        with VerticalScroll(id="help-modal-box"):
            yield Label(Text(f"Help · {self._mode}", style="bold"), classes="modal-title")
            with Horizontal(id="help-cols"):
                with VerticalScroll(id="help-left"):
                    yield Label("[b]Usage[/b]", classes="modal-title")
                    for heading, bullets in help_usage(self._mode):
                        yield Label(Text(heading, style="underline"))
                        for bullet in bullets:
                            yield _HelpLine(Text("  • "), bullet)
                with VerticalScroll(id="help-right"):
                    if entries:
                        yield Label("[b]Legend[/b]", classes="modal-title")
                        for swatch, meaning in entries:
                            yield _HelpLine(Text.assemble(Text.from_markup(swatch), "  "),
                                            meaning)
                    if example:
                        yield Label("[b]Example[/b]", classes="modal-title")
                        yield Label(Text.from_markup(example))
                        yield Label(Text(example_meaning, style="dim"))
            yield Label("[b]Keys[/b] [dim]· this view[/dim]", classes="modal-title",
                        id="help-keys-title")
            # composed at the box's ESTIMATED width so the first layout already
            # holds the band's rows (the scroll range is right from the start);
            # `_fit_keys` then re-lays both at the measured width
            band, glob = self._key_texts(min(110, self.app.size.width * 95 // 100) - 8)
            yield Label(Text(band), id="help-keys")
            with Vertical(id="help-foot"):
                yield Label(Text.assemble((glob[:len(GLOBAL_LEAD)], "bold"),
                                          glob[len(GLOBAL_LEAD):]), id="help-global")
                yield Label("[dim]m full map · ? palette · esc/q closes[/dim]",
                            id="help-hint")

    def on_mount(self) -> None:
        self.call_after_refresh(self._fit_keys)

    def on_resize(self, event: events.Resize) -> None:
        self.call_after_refresh(self._fit_keys)

    def _fit_keys(self) -> None:
        """Lay the Keys band and the global line out at the width the box gives
        its content now (the scrollbar, when there is one, already taken)."""
        width = self.query_one("#help-modal-box").scrollable_content_region.width
        if width <= 0:
            return
        band, glob = self._key_texts(width)
        self.query_one("#help-keys", Label).update(Text(band))
        self.query_one("#help-global", Label).update(
            Text.assemble((glob[:len(GLOBAL_LEAD)], "bold"), glob[len(GLOBAL_LEAD):]))

    def _key_texts(self, width: int) -> tuple[str, str]:
        """The band (column-major `bar_keys`) and the pinned global line
        (`global_keys`, entries never split) at `width`, as plain text."""
        from .keymap import bar_keys, global_keys
        band = keys_grid([f"{k.show:<3} {k.label}" for k in bar_keys(self._mode)], width)
        glob = global_lines([f"{k.show} {k.label}" for k in global_keys(self._mode)], width)
        return "\n".join(band), "\n".join(glob)

    def action_palette(self) -> None:
        self.app.push_screen(CommandPalette(palette_commands(self._mode)),
                             self.app._on_palette_run)

    def action_map(self) -> None:
        from .app import HelpScreen
        shown, hidden = [], []
        for b in self.app.BINDINGS:
            keys = b.key_display or "/".join(format_key(k)
                                             for k in b.key.split(","))
            if b.show is False:
                hidden.append((keys, b.description))
            else:
                shown.append((keys, b.description))
        self.app.push_screen(HelpScreen(shown, hidden))

    def action_close(self) -> None:
        self.dismiss(None)


class StandupModal(ModalScreen[None]):
    """`S` — the week in one read: what moved and what closed, per project.

    Every line is composed at open time from `standup_query`, which reads the
    ONE stamp the board already keeps (`phase_changed`) — nothing is stored
    for this modal, so it can never describe a week the board did not live.
    Read-only by construction: the only action here is close."""

    BINDINGS = [("escape", "close", "Close"), ("q", "close", "Close"),
                ("S", "close", "Close")]

    def __init__(self, board: Board, today=None, show_archived: bool = False):
        super().__init__()
        self._board = board
        self._today = today or date.today()
        self._show_archived = show_archived

    def compose(self) -> ComposeResult:
        from .models import standup_query
        groups = standup_query(self._board, self._today, self._show_archived)
        with VerticalScroll(id="modal-box", classes="modal"):
            yield Label(Text(f"Standup · week ending {self._today.isoformat()}", style="bold"),
                        classes="modal-title")
            if not groups:
                # the honest empty week — one line, no invented motion
                yield Label("Nothing moved this week.")
            for name, items in groups:
                yield Label(Text(f"▐ {name}", style="bold"), classes="modal-title")
                for task, done in items:
                    mark = "✓" if done else "→"
                    yield Label(Text.assemble(f"  {mark} {task.title} ",
                                              (task.phase, "dim")))
                closed = sum(1 for _t, d in items if d)
                yield Label(Text.assemble("  ", (f"{closed}/{len(items)} closed this week",
                                                 "dim")))
            yield Label("[dim]S or esc closes[/dim]", classes="modal-title")

    def action_close(self) -> None:
        self.dismiss(None)


class CommandPalette(ModalScreen[None]):
    """`?` — search every command by name or key and run it without memorising.

    The list is derived from `KEYMAP`, so a command that is added to the seat
    appears here automatically and a removed one disappears."""

    BINDINGS = [("escape", "close", "Close"), ("question_mark", "close", "Close"),
                ("q", "close", "Close"), ("down", "cursor_down", ""),
                ("up", "cursor_up", ""), ("enter", "run", "")]

    DEFAULT_CSS = """
    CommandPalette { align: center middle; }
    #palette-box {
        width: 80; max-width: 95%;
        height: auto; max-height: 80%;
        padding: 1 2;
        background: #0d1219;
        border: round #334154;
    }
    #palette-input { border: tall #1b2431; background: #0b111a; }
    #palette-input:focus { border: tall #2dd4bf; }
    #palette-list { height: auto; max-height: 20; border: none; background: #0d1219; }
    #palette-list > .option-list--option-highlighted {
        background: #1b2431; color: #e6edf3;
    }
    """

    def __init__(self, commands: list[tuple[str, str, str]]) -> None:
        super().__init__()
        self._all = commands
        self._filtered = list(commands)

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="palette-box"):
            yield Input(placeholder="type a command...", id="palette-input")
            yield OptionList(*self._option_lines(self._filtered), id="palette-list")
            yield Label("[dim]esc/?/q close · ↓↑ select · ↵ run[/dim]",
                        classes="modal-title")

    def on_mount(self) -> None:
        self.query_one("#palette-input", Input).focus()

    def _option_lines(self, commands: list[tuple[str, str, str]]) -> list[Text]:
        return [Text(f"{show}  {label}") for show, label, _action in commands]

    def _refresh_list(self) -> None:
        lst = self.query_one("#palette-list", OptionList)
        lst.clear_options()
        lines = self._option_lines(self._filtered)
        if lines:
            lst.add_options(lines)
        else:
            lst.add_options(["[dim]no matches[/dim]"])

    def on_input_changed(self, event: Input.Changed) -> None:
        text = event.value.lower()
        self._filtered = [c for c in self._all
                          if text in c[1].lower() or text in c[0].lower()]
        self._refresh_list()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter while typing runs the highlighted command without leaving the
        keyboard."""
        if event.input.id == "palette-input":
            self.action_run()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Enter/click on the list runs the selected command."""
        self.action_run()

    def action_cursor_down(self) -> None:
        self.query_one("#palette-list", OptionList).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#palette-list", OptionList).action_cursor_up()

    def action_run(self) -> None:
        if not self._filtered:
            return
        lst = self.query_one("#palette-list", OptionList)
        idx = lst.highlighted if lst.highlighted is not None else 0
        if 0 <= idx < len(self._filtered):
            _show, _label, action = self._filtered[idx]
            self.dismiss(action)

    def action_close(self) -> None:
        self.dismiss(None)


# ---- several boards (batch 2026-10-20-batch-01) -----------------------------
def _home_path(path: Path) -> str:
    """A path as the operator reads it: the home folder written `~`."""
    try:
        return "~/" + Path(path).relative_to(Path.home()).as_posix()
    except ValueError:
        return str(path)


class BoardForm(ModalScreen[tuple[str, str] | None]):
    """Create (no entry) or edit a board: a name, one of the eight project
    colours, and the file it creates or keeps (HLR-2205). Every line is a `Text`
    built from plain pieces: a typed name is never parsed as markup."""

    BINDINGS = [Binding("escape", "cancel", "", priority=True),
                Binding("tab", "hue(1)", "", priority=True, show=False),
                Binding("shift+tab", "hue(-1)", "", priority=True, show=False)]
    BOX_W = 64

    def __init__(self, entry=None, *, color: str = "violet", root: Path | None = None,
                 next_id=slug):
        super().__init__()
        self.entry = entry
        self.root = root
        self.next_id = next_id      # the registry's: the folder `create` will make (F3)
        start = entry.color if entry is not None else color
        self.hue = PROJECT_COLORS.index(start) if start in PROJECT_COLORS else 0

    def compose(self) -> ComposeResult:
        with Vertical(id="bf-box"):
            yield Static(Text("Edit board" if self.entry else "New board",
                              style=f"bold {HEX['bright']}"), id="bf-title")
            yield Input(value=self.entry.name if self.entry else "", placeholder="board name",
                        id="bf-name")
            yield Static(id="bf-hues")
            yield Static(id="bf-path")
            yield Static(Text("⇥ colour · ↵ " + ("save" if self.entry else "create and open")
                              + " · esc cancel", style=HEX["dim"]), id="bf-keys")

    def on_mount(self) -> None:
        self.query_one("#bf-name", Input).focus()
        self._paint()

    def on_input_changed(self, _event) -> None:
        self._paint()

    def _paint(self) -> None:
        t = Text("colour  ", style=HEX["mut"])
        for i, c in enumerate(PROJECT_COLORS):
            on = i == self.hue
            t.append("[" if on else " ", style=HEX["bright"])
            t.append("██", style=HEX[c])
            t.append("]" if on else " ", style=HEX["bright"])
        t.append(f"  {PROJECT_COLORS[self.hue]}", style=HEX["dim"])
        self.query_one("#bf-hues", Static).update(t)
        room = self.BOX_W - 4 - 8
        p = Text("file    ", style=HEX["mut"])
        if self.entry is not None:
            p.append(clip(_home_path(Path(self.entry.path)) + "  (unchanged)", room),
                     style=HEX["dim"])
        else:
            name = self.query_one("#bf-name", Input).value
            where = ((self.root or Path.home() / ".taskboard") / "boards" / self.next_id(name)
                     / "board.json")
            p.append(clip(_home_path(where), room), style=HEX["hd"])
        self.query_one("#bf-path", Static).update(p)

    def action_hue(self, delta: int) -> None:
        self.hue = (self.hue + delta) % len(PROJECT_COLORS)
        self._paint()

    def on_input_submitted(self, _event) -> None:
        name = clean_name(self.query_one("#bf-name", Input).value)
        if name:
            self.dismiss((name, PROJECT_COLORS[self.hue]))

    def action_cancel(self) -> None:
        self.dismiss(None)


class MoveTarget(ModalScreen[str | None]):
    """The board a project moves to (HLR-2206): the other active boards, each
    with its colour, name and size. Names are plain `Text` pieces."""

    BINDINGS = [Binding("escape", "cancel", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True, show=False),
                Binding("down,j", "move(1)", "", priority=True, show=False),
                Binding("enter", "choose", "", priority=True, show=False)]

    def __init__(self, project: Project, n_tasks: int, entries: list, boards: dict):
        super().__init__()
        self.project, self.n_tasks = project, n_tasks
        self.targets, self.boards = entries, boards
        self.cursor = 0

    def compose(self) -> ComposeResult:
        head = Text("Move ", style=f"bold {HEX['bright']}")
        head.append("██ ", style=HEX.get(self.project.color, HEX["violet"]))
        head.append(self.project.name, style=f"bold {HEX['bright']}")
        head.append(f"  ({self.n_tasks} tasks)  to which board?", style=HEX["mut"])
        with Vertical(id="mt-box"):
            yield Static(head, id="mt-title")
            yield Static(id="mt-rows")
            yield Static(Text("↑↓ move · ↵ choose · esc cancel", style=HEX["dim"]),
                         id="mt-keys")

    def on_mount(self) -> None:
        self._paint()

    def _paint(self) -> None:
        t = Text(no_wrap=True)
        for i, e in enumerate(self.targets):
            b = self.boards[e.id]
            n_open = sum(1 for x in b.tasks if not b.is_done(x) and not x.archived)
            n_proj = sum(1 for p in b.projects if not p.archived)
            on = i == self.cursor
            if i:
                t.append("\n")
            t.append("▶ " if on else "  ", style=HEX["accent"])
            t.append("██ ", style=HEX.get(e.color, HEX["violet"]))
            t.append(fit(e.name, 24), style=f"bold {HEX['bright']}" if on else HEX["ink"])
            t.append(f"{n_proj} projects · {n_open} open", style=HEX["dim"])
        self.query_one("#mt-rows", Static).update(t)

    def action_move(self, delta: int) -> None:
        self.cursor = max(0, min(len(self.targets) - 1, self.cursor + delta))
        self._paint()

    def action_choose(self) -> None:
        self.dismiss(self.targets[self.cursor].id)

    def action_cancel(self) -> None:
        self.dismiss(None)


class MoveConfirm(ModalScreen[bool]):
    """What a move does, said before it is done (HLR-2206): what moves, the
    links that stay, each link that crosses the boards and will be dropped, the
    backups, the log, and that `u` cannot undo it. The links scroll; the head
    and the keys are always on screen."""

    BINDINGS = [Binding("escape", "no", "", priority=True),
                Binding("y", "yes", "", priority=True, show=False),
                Binding("n", "no", "", priority=True, show=False)]

    def __init__(self, plan, project: Project, src_board: Board, src_entry, dst_entry,
                 day: str):
        super().__init__()
        self.plan, self.project, self.board = plan, project, src_board
        self.src, self.dst, self.day = src_entry, dst_entry, day

    def compose(self) -> ComposeResult:
        p, plan = self.project, self.plan
        done = sum(1 for t in plan.tasks if self.board.is_done(t) or t.archived)
        head = Text()
        head.append("Move project to another board\n\n", style=f"bold {HEX['bright']}")
        head.append("  ██ ", style=HEX.get(p.color, HEX["violet"]))
        head.append(p.name, style=f"bold {HEX['bright']}")
        head.append("   from ", style=HEX["mut"])
        head.append(f" {self.src.name} ",
                    style=f"bold #0d1117 on {HEX.get(self.src.color, HEX['violet'])}")
        head.append("  to ", style=HEX["mut"])
        head.append(f" {self.dst.name} ",
                    style=f"bold #0d1117 on {HEX.get(self.dst.color, HEX['violet'])}")
        head.append(f"\n\n  {len(plan.tasks)} tasks move ({len(plan.tasks) - done} open, {done} "
                    f"done) · {plan.kept} links inside the project stay", style=HEX["hd"])
        links = Text()
        n = len(plan.crossing)
        if n:
            pname = {q.id: q.name for q in self.board.projects}
            links.append(f"  {n} link{'s' if n > 1 else ''} cross the boards and will be "
                         "dropped:\n", style=f"bold {HEX['over']}")
            for waiter, pred in plan.crossing:
                for task, role in ((waiter, ""), (pred, "waits on ")):
                    links.append("    " + ("✕ " if not role else "    "), style=HEX["over"])
                    if role:
                        links.append(role, style=HEX["mut"])
                    links.append(task.title, style=HEX["ink"])
                    where = ("moves" if task.project_id == p.id else
                             f"{pname.get(task.project_id, 'Inbox')}, stays on {self.src.name}")
                    links.append(f"  ({where})\n", style=HEX["dim"])
        links.rstrip()
        foot = Text()
        foot.append(f"  Both board files are backed up first ({Path(self.src.path).name}.pre-move-{self.day}),\n"
                    f"  and the dropped links are listed in move-{self.day}.json beside each.\n"
                    "  u cannot undo a move or the edits before it — the backups are the way "
                    "back.\n", style=HEX["dim"])
        # `y` as every confirmation's (batch 2026-10-20-batch-03, ux UX-2): a stray
        # `enter` moves nothing
        foot.append("\n  ")
        foot.append_text(key_line([("y", f"move{f' and drop {n} links' if n else ''}"),
                                   ("n / esc", "cancel")]))
        with Vertical(id="mc-box"):
            yield Static(head, id="mc-head")
            with VerticalScroll(id="mc-links"):
                yield Static(links, id="mc-links-text")
            yield Static(foot, id="mc-foot")

    def on_mount(self) -> None:
        box = self.query_one("#mc-links", VerticalScroll)
        if not self.plan.crossing:
            box.display = False
        # the links scroll; the head and the keys stay on screen (ux-reviewer UX-3)
        box.styles.max_height = max(3, self.app.size.height - 16)

    def action_yes(self) -> None:
        self.dismiss(True)

    def action_no(self) -> None:
        self.dismiss(False)

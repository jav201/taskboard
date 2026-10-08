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
from .keymap import palette_commands
from .views import (HEX, clip, gantt_group_key, gantt_link_frame, gantt_link_order,
                    highlight_segments, valid_url)

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


def notes_preview(text: str) -> Text:
    """The notes as the board paints them: each line through the board's one
    highlight tokeniser, `highlight_segments` (a highlight never crosses a line
    there either), each segment a Text PIECE in its tone.

    No parser reads the notes (S1, S-4): escaping and re-parsing them doubled
    backslashes and turned `:smile:` into an emoji, and handed to a Static as a
    str Textual's own parser read `[B]` or `[LINK=…` as tags — a note holding one
    crashed the editor and could arrive by team sync."""
    out = Text()
    for i, ln in enumerate(text.split("\n")):
        if i:
            out.append("\n")
        if ln.strip():
            for segment, tone in highlight_segments(ln):
                out.append(segment, HEX[tone])
    return out


class TaskModal(ClipboardPasteMixin, EmojiPickerMixin, DatePickerMixin,
                ModalScreen[dict | None]):
    """Returns a dict of task fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True),
                Binding("ctrl+e", "pick_emoji", "Emoji", priority=True)]

    def __init__(self, board: Board, task: Task | None = None):
        super().__init__()
        self.board = board
        self._edit_task = task
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
                        yield Static(notes_preview(t.notes if t else ""),
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

    def on_mount(self) -> None:
        self._fold_chips(self.app.size.width)

    def on_resize(self, event: events.Resize) -> None:
        self._fold_chips(event.size.width)

    def _fold_chips(self, width: int) -> None:
        self.query_one("#task-chips").set_class(width < TASK_CHIPS_ONE_ROW, "-folded")

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "f-notes":
            self.query_one("#task-preview", Static).update(
                notes_preview(event.text_area.text))
            self.call_after_refresh(self._follow_cursor)

    def on_text_area_selection_changed(self, event: TextArea.SelectionChanged) -> None:
        if event.text_area.id == "f-notes":
            self._follow_cursor()

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
            "priority": self._val("f-priority"),
            "start_date": self._val("f-start") or None,
            "due_date": self._val("f-due") or None,
            "notes": self.query_one("#f-notes", TextArea).text.strip(),
            "urls": urls,
            "images": self._lines("f-images"),   # local paths valid at entry (no filter)
        }
        self.dismiss(data)


class ProjectModal(ClipboardPasteMixin, EmojiPickerMixin, DatePickerMixin,
                   ModalScreen[dict | None]):
    """Returns a dict of project fields on save, or None on cancel."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True),
                Binding("ctrl+e", "pick_emoji", "Emoji", priority=True)]

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
        Binding("j", "move(1)", show=False),
        Binding("k", "move(-1)", show=False),
    ]

    def __init__(self, board: Board):
        super().__init__()
        self.board = board

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="picker-box", classes="modal"):
            yield Label("[b]Projects[/b]  —  e edit · x archive · d delete · esc close",
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


class TemplatePicker(ModalScreen[str | None]):
    """`I` — "insert a process" (HLR-1301). Lists the board's user templates
    first, then the factory presets, each row `name — N tasks`; selecting a row
    returns its name, `esc` returns None. Every user string is a Text piece
    (S1)."""

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
        options = []
        for t in self._templates:
            line = Text(t.name, style="bold")
            line.append(f" — {len(t.tasks)} tasks", style=HEX["dim"])
            options.append(Option(line, id=str(len(options))))
        ol.add_options(options)
        ol.highlighted = 0 if options else None
        ol.focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(self._templates[int(event.option.id)].name)

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
            yield Label(Text.assemble(("◆ Milestones", "bold"), " · convert one-day tasks?",
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

    def __init__(self, roster: list[dict]):
        super().__init__()
        self._roster = roster

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="identity-box", classes="modal"):
            yield Label("[b]Operator identity[/b]  —  pick from the team roster",
                        classes="modal-title")
            yield OptionList(id="identity-list")

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


class ClockModal(ClipboardPasteMixin, ModalScreen[dict | None]):
    """Pick the two ribbon clocks by CITY (type to find one). Returns city names."""

    BINDINGS = [("escape", "cancel", "Cancel"),
                Binding("ctrl+v", "paste_text", "Paste", priority=True)]

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


class ConfirmModal(ModalScreen[bool]):
    """Small yes/no confirm."""

    BINDINGS = [("escape", "no", "No")]

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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

    def action_no(self) -> None:
        self.dismiss(False)


class TextPrompt(ModalScreen[str | None]):
    """One-line text prompt. Dismisses with the STRIPPED text on Save/Enter and
    None on Cancel/Esc, so the caller can tell "left it blank" from "cancelled"."""

    BINDINGS = [("escape", "cancel", "Cancel")]

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
                yield Static(notes_preview(t.notes))
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
    carries the live legend, an annotated example, and the view's own keybar.
    From here `m` opens the FULL keymap and `?` opens the command palette.
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
    }
    #help-modal-box .modal-title { margin: 0 0 1 0; }
    #help-left { width: 48; height: auto; }
    #help-right { width: 1fr; height: auto; }
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
        from .keymap import bar_keys
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
            with Horizontal():
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
                    yield Label("[b]Keys[/b]", classes="modal-title")
                    for k in bar_keys(self._mode):
                        yield Label(Text(f"{k.show}  {k.label}"))
            yield Label("[dim]m full map · ? palette · esc/q closes[/dim]",
                        classes="modal-title")

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

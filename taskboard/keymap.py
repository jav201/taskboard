"""THE KEY BAR IS A CONTRACT.

    EVERY KEY SHOWN WORKS. EVERY KEY THAT WORKS IS SHOWN.
    A capability whose key is not on screen does not exist.

This module is the ONE seat. `KEYMAP` below is the only place a key is declared,
and both halves are generated from it: the app's `BINDINGS` and the bar the user
reads. They cannot drift because there are not two lists.

What this replaced: Textual's `Footer`, which in 8.2.8 reported its bindings
ready and then mounted ZERO children — all 24 live keys rendered as a blank row.
The capabilities were live and the display was empty, which is the exact defect
this law exists to make impossible.

When the row runs out of width, LABELS go, KEYS NEVER DO — a key without its
word is still discoverable, a key that is absent is not. Universal keys sort
first so they can never be the ones lost.
"""

from __future__ import annotations

from typing import NamedTuple

from textual.binding import Binding
from textual.widgets import Static

from .views import HEX

VIEWS = ("swimlanes", "agenda", "gantt", "kanban", "focus")

# Category hues for the layered "more" bar. Each group is drawn with its own
# attention colour so the reader can parse the dense row at a glance.
GROUP_HUE = {
    "system": "amber",
    "views": "violet",
    "nav": "mut",
    "task": "accent",
    "phase": "sky",
    "kanban": "cyan",
    "date": "orange",
    "misc": "green",
}


class Key(NamedTuple):
    keys: str                       # what Textual binds — may be an alias list
    show: str                       # what the bar prints
    action: str                     # the action, exactly as Textual runs it
    label: str                      # the word, first thing to go when it is tight
    universal: bool = False         # sorts first, dropped last
    priority: bool = False          # Textual priority binding
    views: tuple[str, ...] | None = None    # None = live in every view
    primary: bool = False           # shown in the compact primary layer
    group: str = "misc"             # category used by the more-layer grouping
    bar: bool = True                # shown in the docked key bar (False = palette-only)


# THE SEAT. Nothing else in the app may declare a key.
# Primary layer: only the essentials a daily user needs. More layer: everything,
# grouped by category and tinted so the eye can travel.
KEYMAP: tuple[Key, ...] = (
    # -- system / layer -------------------------------------------------------
    Key("?", "?", "legend", "Map", universal=True, primary=True, group="system"),
    Key(";", ";", "layer_toggle", "More", universal=True, primary=True, group="system"),
    Key("q", "q", "quit", "Quit", universal=True, primary=True, group="system"),

    # -- views ----------------------------------------------------------------
    Key("1", "1", "view('swimlanes')", "Lanes", primary=True, group="views"),
    Key("2", "2", "view('agenda')", "Agenda", primary=True, group="views"),
    Key("3", "3", "view('gantt')", "Gantt", primary=True, group="views"),
    Key("4", "4", "view('kanban')", "Kanban", primary=True, group="views"),
    Key("5", "5", "view('focus')", "Focus", primary=True, group="views"),
    Key("7", "7", "view('flow')", "Flow", primary=True, group="views"),
    Key("8", "8", "view('standup')", "Standup", primary=True, group="views"),
    Key("9", "9", "view('people')", "People", primary=True, group="views"),
    Key("0", "0", "view('setup')", "Setup", primary=True, group="views"),

    # -- task -----------------------------------------------------------------
    Key("enter", "↵", "details", "Details", primary=True, group="task"),
    Key("a", "a", "add_task", "Add", primary=True, group="task"),
    Key("e", "e", "edit", "Edit", primary=True, group="task"),
    Key("d,delete", "d", "delete", "Del", primary=True, group="task"),
    Key("x", "x", "archive", "Archive", group="task"),
    Key("X", "X", "purge_done", "Purge done", group="task"),
    Key("v", "v", "toggle_archived", "Archived", group="task"),
    Key("u", "u", "undo", "Undo", group="task"),
    Key("t", "t", "pin_toggle", "Pin task", group="task"),
    Key("T", "T", "project_pin_toggle", "Pin proj", group="task"),

    # -- phase / priority -----------------------------------------------------
    Key("[", "[", "phase_move(-1)", "Phase−", group="phase"),
    Key("]", "]", "phase_move(1)", "Phase+", group="phase"),
    Key("!", "!", "prio_cycle", "Prio", group="phase"),
    Key("b", "b", "toggle_blocked", "Blocked", group="phase"),

    # -- date -----------------------------------------------------------------
    Key("+,=", "+", "due_bump(1)", "Due+", group="date"),
    Key("-", "-", "due_bump(-1)", "Due-", group="date"),

    # -- kanban-only ----------------------------------------------------------
    # `s`/`g` reshape kanban columns only, so — like Tab below — they are only
    # claimed there: advertised where they work, guarded no-ops everywhere else.
    Key("s", "s", "kanban_sort", "Sort", views=("kanban",), group="kanban"),
    Key("g", "g", "kanban_group", "Group", views=("kanban",), group="kanban"),
    # `z` collapses THE LAST phase column to one `✓ N` row — same kanban-only
    # scoping as its sort/group siblings, but it needs no selection and fires
    # from anywhere in the view (§6.5 AMD-02).
    Key("z", "z", "collapse_toggle", "Collapse", views=("kanban",), group="kanban"),
    # `F` focuses ONE project (kanban and gantt); the escape companion leaves
    # it — and is a guarded no-op with no focus active, so it never eats
    # another screen's escape (§6.5 AMD-03).
    Key("F", "F", "focus_cycle", "Focus", views=("kanban", "gantt"), group="kanban"),
    Key("escape", "esc", "focus_exit", "Focus off", views=("kanban", "gantt", "setup"), group="kanban"),
    Key("/", "/", "search", "Search", views=("kanban", "gantt"), group="kanban"),
    # Tab does something in kanban, focus and swimlanes, so it is claimed in
    # all three — the action itself (toggle_presentation) decides which view
    # state to cycle.
    Key("tab", "⇥", "toggle_presentation", "Layout", priority=True,
        views=("kanban", "focus", "swimlanes"), primary=True, group="nav"),

    # -- misc -----------------------------------------------------------------
    # Global commands: always bound, reachable from `?`/palette, but not drawn
    # in the per-view key bar — the bar's real estate belongs to the view.
    Key("o", "o", "open_url", "URL", group="misc", bar=False),
    Key("i", "i", "open_images", "Images", group="misc", bar=False),
    Key("p", "p", "add_project", "New proj", group="misc", bar=False),
    Key("P", "P", "manage_projects", "Projects", group="misc", bar=False),
    Key("f", "f", "manage_phases", "Phases", group="misc", bar=False),
    Key("c", "c", "clocks", "Clocks", group="misc", bar=False),
    Key("R", "R", "report", "Report", group="misc", bar=False),
    # `S` reads the week (shifted, like X/P/R — a rarer, bigger gesture); it
    # derives from the board in ANY view, so — like `R` — it is not scoped.
    Key("S", "S", "standup", "Standup", group="misc", bar=False),

    # -- navigation -----------------------------------------------------------
    # Declared LAST on purpose, and drawn FIRST in the more layer: `universal`
    # is what moves them, not their position here.
    Key("down,j", "↓", "cursor(1)", "Down", priority=True, primary=True, group="nav"),
    Key("up,k", "↑", "cursor(-1)", "Up", priority=True, primary=True, group="nav"),
    Key("left,h", "←", "hmove(-1)", "Left", priority=True, group="nav"),
    Key("right,l", "→", "hmove(1)", "Right", priority=True, group="nav"),

    # -- setup-only -----------------------------------------------------------
    # tab/enter/a/x reuse their board bindings and dispatch on view_mode.
    Key("space", "␣", "setup_toggle", "Toggle", views=("setup",), group="setup"),
    Key("ctrl+s", "^s", "setup_save", "Save", views=("setup",), group="setup"),
)


def app_bindings() -> list[Binding]:
    """The app's BINDINGS, generated. Half of the contract."""
    return [Binding(k.keys, k.action, k.label, priority=k.priority) for k in KEYMAP]


def _live_keys(view: str) -> list[Key]:
    """Every key live in `view`, regardless of layer or bar flag."""
    return [k for k in KEYMAP if k.views is None or view in k.views]


def _layer_keys(view: str, layer: str) -> list[Key]:
    """Keys to display in `layer` for `view`, universal ones first."""
    live = _live_keys(view)
    if layer == "primary":
        live = [k for k in live if k.primary]
    return sorted(live, key=lambda k: not k.universal)


def bar_keys(view: str, layer: str = "more") -> list[Key]:
    """The keys drawn in the per-view key bar: view-local + universal, with
    `bar=False` global commands kept for the palette only.

    Sorted stably, so the declaration order is the reading order within each
    group and the bar does not reshuffle itself as the user switches views or
    layers."""
    return [k for k in _layer_keys(view, layer) if k.bar]


def palette_commands(view: str) -> list[tuple[str, str, str]]:
    """All commands reachable from `view` as (show, label, action).

    The palette lists every live key, including palette-only globals, and runs
    the action string when one is selected. Universal commands sort first so
    the most reliable doors out (quit, palette itself) are always at the top."""
    return [(k.show, k.label, k.action) for k in _layer_keys(view, "more")]


SEP = "  "
GROUP_SEP = "  "


def _width(entries: list[tuple[str, str]], dropped: int) -> int:
    body = SEP.join(f"{show} {label}".strip() for show, label in entries)
    return len(body) + (len(f" +{dropped}") if dropped else 0)


def fit_bar(width: int, view: str, layer: str = "more") -> tuple[list[tuple[str, str]], int]:
    """(what the bar shows, how many keys did not fit) at `width` cells.

    Degradation, in order: the WORDS go first, from the right, one at a time.
    Only when every word is gone and the keys THEMSELVES still overflow does a
    key drop — and then it is counted, never silently swallowed."""
    entries = [[k.show, k.label] for k in bar_keys(view, layer)]
    for i in range(len(entries) - 1, -1, -1):
        if _width([tuple(e) for e in entries], 0) <= width:
            break
        entries[i][1] = ""                    # drop this word, keep its key
    dropped = 0
    while entries and _width([tuple(e) for e in entries], dropped) > width:
        entries.pop()
        dropped += 1
    return [tuple(e) for e in entries], dropped


def _note(entries: list[tuple[str, str]], dropped: int, width: int) -> str:
    """The overflow count, only if IT fits too. Below a handful of cells there
    is no honest bar to draw, and a count that overflows is just another lie."""
    if not dropped:
        return ""
    body = len(SEP.join(f"{show} {label}".strip() for show, label in entries))
    note = f" +{dropped}"
    return note if body + len(note) <= width else ""


def key_bar_plain(width: int, view: str, layer: str = "more") -> str:
    """Exactly what a reader sees, as plain text."""
    entries, dropped = fit_bar(width, view, layer)
    body = SEP.join(f"{show} {label}".strip() for show, label in entries)
    return body + _note(entries, dropped, width)


def _mshow(text: str) -> str:
    """Textual-markup escape for the ONE hostile glyph a key show can hold.

    Neither `rich.markup.escape` nor `textual.markup.escape` touches a bare
    `[` (both only neutralize tag-LOOKING sequences), but the Content parser
    reads `[#hex][[/]` as the literal text `[[/]` — three phantom cells the
    fit math never counted, so a bar that "fit" overflowed its row and the
    last key silently clipped (measured 2026-08-15, kanban bar at 118)."""
    return text.replace("[", "\\[")


def render_key_bar(width: int, view: str, layer: str = "more") -> str:
    """The bar as markup: keys tinted by category, words in the quiet one."""
    entries, dropped = fit_bar(width, view, layer)
    if layer == "primary":
        out = [f"[{HEX['accent']}]{_mshow(show)}[/]" + (f" [{HEX['mut']}]{_mshow(label)}[/]" if label else "")
               for show, label in entries]
        markup = SEP.join(out)
        note = _note(entries, dropped, width)
        return markup + (f"[{HEX['dim']}]{note}[/]" if note else "")

    # more layer: colour each key by its group. We recover the Key from the
    # show token (shows are unique) so the colour matches the source row.
    show_to_key = {k.show: k for k in bar_keys(view, "more")}
    out = []
    for show, label in entries:
        k = show_to_key.get(show)
        hue = GROUP_HUE.get(k.group, "accent") if k else "accent"
        part = f"[{HEX[hue]}]{_mshow(show)}[/]"
        if label:
            part += f" [{HEX['mut']}]{_mshow(label)}[/]"
        out.append(part)
    markup = SEP.join(out)
    note = _note(entries, dropped, width)
    return markup + (f"[{HEX['dim']}]{note}[/]" if note else "")


class KeyBar(Static):
    """The docked key row. It re-reads the contract on every resize and on every
    view change, so what it shows is never a snapshot of an older state."""

    view_mode: str = "swimlanes"
    bar_layer: str = "primary"

    def on_mount(self) -> None:
        self.refresh_bar()

    def on_resize(self, event) -> None:
        self.refresh_bar()

    def set_layer(self, layer: str) -> None:
        self.bar_layer = layer
        self.refresh_bar()

    def refresh_bar(self, view: str | None = None) -> str:
        if view is not None:
            self.view_mode = view
        width = self.content_size.width or self.size.width
        markup = render_key_bar(max(0, width), self.view_mode, self.bar_layer)
        self.update(markup)
        return markup

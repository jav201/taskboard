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

VIEWS = ("swimlanes", "agenda", "gantt", "kanban")


class Key(NamedTuple):
    keys: str                       # what Textual binds — may be an alias list
    show: str                       # what the bar prints
    action: str                     # the action, exactly as Textual runs it
    label: str                      # the word, first thing to go when it is tight
    universal: bool = False         # sorts first, dropped last
    priority: bool = False          # Textual priority binding
    views: tuple[str, ...] | None = None    # None = live in every view


# THE SEAT. Nothing else in the app may declare a key.
KEYMAP: tuple[Key, ...] = (
    Key("1", "1", "view('swimlanes')", "Lanes"),
    Key("2", "2", "view('agenda')", "Agenda"),
    Key("3", "3", "view('gantt')", "Gantt"),
    Key("4", "4", "view('kanban')", "Kanban"),
    Key("enter", "↵", "details", "Details"),
    Key("a", "a", "add_task", "Add"),
    Key("e", "e", "edit", "Edit"),
    Key("d,delete", "d", "delete", "Del"),
    Key("x", "x", "archive", "Archive"),
    Key("X", "X", "purge_done", "Purge done"),
    Key("v", "v", "toggle_archived", "Archived"),
    Key("o", "o", "open_url", "URL"),
    Key("i", "i", "open_images", "Images"),
    Key("p", "p", "add_project", "New proj"),
    Key("P", "P", "manage_projects", "Projects"),
    Key("f", "f", "manage_phases", "Phases"),
    Key("c", "c", "clocks", "Clocks"),
    Key("R", "R", "report", "Report"),
    # Tab only does something in kanban, so it is only claimed there — a key
    # advertised everywhere that answers in one place is the same lie in reverse.
    Key("tab", "⇥", "toggle_presentation", "Layout", priority=True, views=("kanban",)),
    Key("down,j", "↓", "cursor(1)", "Down", priority=True),
    Key("up,k", "↑", "cursor(-1)", "Up", priority=True),
    Key("left,h", "←", "hmove(-1)", "Left", priority=True),
    Key("right,l", "→", "hmove(1)", "Right", priority=True),
    # Declared LAST on purpose, and drawn FIRST: `universal` is what moves it,
    # not its position here. A universal key must be declarable anywhere in this
    # table and still be the last one standing when the row runs out of width.
    Key("?", "?", "legend", "Keys", universal=True),
    Key("q", "q", "quit", "Quit", universal=True),
)


def app_bindings() -> list[Binding]:
    """The app's BINDINGS, generated. Half of the contract."""
    return [Binding(k.keys, k.action, k.label, priority=k.priority) for k in KEYMAP]


def bar_keys(view: str) -> list[Key]:
    """The keys live in `view`, universal ones first. The other half.

    Sorted stably, so the declaration order is the reading order within each
    group and the bar does not reshuffle itself as the user switches views."""
    live = [k for k in KEYMAP if k.views is None or view in k.views]
    return sorted(live, key=lambda k: not k.universal)


SEP = "  "


def _width(entries: list[tuple[str, str]], dropped: int) -> int:
    body = SEP.join(f"{show} {label}".strip() for show, label in entries)
    return len(body) + (len(f" +{dropped}") if dropped else 0)


def fit_bar(width: int, view: str) -> tuple[list[tuple[str, str]], int]:
    """(what the bar shows, how many keys did not fit) at `width` cells.

    Degradation, in order: the WORDS go first, from the right, one at a time.
    Only when every word is gone and the keys THEMSELVES still overflow does a
    key drop — and then it is counted, never silently swallowed."""
    entries = [[k.show, k.label] for k in bar_keys(view)]
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


def key_bar_plain(width: int, view: str) -> str:
    """Exactly what a reader sees, as plain text."""
    entries, dropped = fit_bar(width, view)
    body = SEP.join(f"{show} {label}".strip() for show, label in entries)
    return body + _note(entries, dropped, width)


def render_key_bar(width: int, view: str) -> str:
    """The bar as markup: keys in the attention hue, words in the quiet one."""
    entries, dropped = fit_bar(width, view)
    out = [f"[{HEX['accent']}]{show}[/]" + (f" [{HEX['mut']}]{label}[/]" if label else "")
           for show, label in entries]
    markup = SEP.join(out)
    note = _note(entries, dropped, width)
    return markup + (f"[{HEX['dim']}]{note}[/]" if note else "")


class KeyBar(Static):
    """The docked key row. It re-reads the contract on every resize and on every
    view change, so what it shows is never a snapshot of an older state."""

    view_mode: str = "swimlanes"

    def on_mount(self) -> None:
        self.refresh_bar()

    def on_resize(self, event) -> None:
        self.refresh_bar()

    def refresh_bar(self, view: str | None = None) -> str:
        if view is not None:
            self.view_mode = view
        width = self.content_size.width or self.size.width
        markup = render_key_bar(max(0, width), self.view_mode)
        self.update(markup)
        return markup

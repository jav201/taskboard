"""THROWAWAY prototype — the backlog round (nine small items after batch 2026-10-20-batch-01).

    unset NO_COLOR; PYTHONUTF8=1 python prototypes/backlog_round/proto.py list
    unset NO_COLOR; PYTHONUTF8=1 python prototypes/backlog_round/proto.py shot [SCENE ...]
    unset NO_COLOR; PYTHONUTF8=1 python prototypes/backlog_round/proto.py exports
    python prototypes/backlog_round/proto.py live SCENE [SECONDS]      (a real terminal)

Sub-shape A: the REAL `TaskboardApp` (subclassed here), on a real registry in a
temporary folder (fixture.py), driven by real key presses (`App._press_keys`,
the pilot's own path) — headless for the SVGs, in a real Windows Terminal for
the PNGs (shoot.ps1). Each variant is a subclass of the shipped screen it
changes, patched into `taskboard.app` for that scene only. Nothing under
`taskboard/` is edited; nothing writes outside the temporary folder.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import fixture as fx  # noqa: E402
from rich.text import Text  # noqa: E402
from textual.binding import Binding  # noqa: E402
from textual.containers import VerticalScroll  # noqa: E402
from textual.screen import ModalScreen, Screen  # noqa: E402
from textual.widgets import Label, Static  # noqa: E402

from taskboard import app as app_mod, models, views  # noqa: E402
from taskboard.app import BoardsHome, PresentScreen, TaskboardApp  # noqa: E402
from taskboard.boards import Registry, peek_board  # noqa: E402
from taskboard.modals import ConfirmModal, MilestoneOffer, TeamIdentityPicker  # noqa: E402
from taskboard.models import is_open, parse_iso  # noqa: E402
from taskboard.views import HEX, board_hex, fit  # noqa: E402

TODAY = fx.TODAY
OUT = HERE / "out"


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


app_mod.date = _Today
models.date = _Today
views.date = _Today

RED, SOON = HEX["over"], HEX["soon"]
KEY = f"b {HEX['bright']}"
ROSTER = [{"id": "u1", "name": "username_subject"}, {"id": "u2", "name": "Teammate B"},
          {"id": "u3", "name": "Teammate C"}]


def keys_text(pairs, w: int, tail: str = "") -> Text:
    k = Text(no_wrap=True, overflow="ellipsis")
    for key, lab in pairs:
        k.append(key, style=KEY)
        k.append(f" {lab}  ", style=HEX["mut"])
    if tail:
        k.append(tail, style=HEX["dim"])
    k.truncate(max(1, w))
    return k


def chip(name: str, colour: str) -> Text:
    return Text(f" {name} ", style=f"b #0d1117 on {board_hex(colour)}")


# =============================================================================
# ITEM 1 — option D, an "All boards" agenda (three structures)
# =============================================================================
class Item(NamedTuple):
    band: str
    entry: object
    task: object
    due: date
    project: str


WEEK_END = TODAY + timedelta(days=6 - TODAY.weekday())       # Sunday


def gather(app) -> list[Item]:
    out = []
    for e in app.registry.active():
        b = app.board if e.id == app.board_id else peek_board(e.path)
        names = {p.id: p.name for p in b.projects}
        for t in b.tasks:
            d = parse_iso(t.due_date)
            if d is None or not is_open(b, t):
                continue
            band = ("late" if d < TODAY else "today" if d == TODAY
                    else "week" if d <= WEEK_END else None)
            if band:
                out.append(Item(band, e, t, d, names.get(t.project_id, "")))
    order = {"late": 0, "today": 1, "week": 2}
    out.sort(key=lambda x: (order[x.band], x.due, x.entry.name))
    return out


def when(d: date) -> tuple[str, str]:
    if d < TODAY:
        return f"▲{(TODAY - d).days}d", RED
    if d == TODAY:
        return "today", SOON
    return f"{d:%a} {d.day}", HEX["hd"]


class AgendaBase(Screen[None]):
    BINDINGS = [Binding("escape,A", "back", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True),
                Binding("down,j", "move(1)", "", priority=True),
                Binding("left,h", "side(-1)", "", priority=True),
                Binding("right,l", "side(1)", "", priority=True),
                Binding("enter", "jump", "", priority=True)]
    DEFAULT_CSS = """
    AgendaBase { background: #0d1117; overflow-y: hidden; }
    #ag-body { padding: 0 1; height: 1fr; }
    #ag-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    """
    KEYS = (("↑↓", "move"), ("↵", "open on its board"), ("esc", "back"))

    def compose(self):
        yield Static(id="ag-body")
        yield Static(id="ag-keys")

    def on_mount(self) -> None:
        self.items = gather(self.app)
        self.setup()
        self._paint()

    def on_resize(self, _e) -> None:
        self._paint()

    def setup(self) -> None:
        self.cur = 0

    def _paint(self) -> None:
        w, h = self.app.size
        self.query_one("#ag-body", Static).update(self.body(w - 2, h - 1))
        self.query_one("#ag-keys", Static).update(
            keys_text(self.KEYS, w - 2, "· read-only: nothing here edits a task"))

    def head(self, inner: int) -> Text:
        n = {b: sum(1 for x in self.items if x.band == b) for b in ("late", "today", "week")}
        t = Text(no_wrap=True)
        left = "◆ ALL BOARDS"
        t.append(left, style=f"bold {HEX['bright']}")
        boards = len({x.entry.id for x in self.items})
        sub = f"  {boards} boards · read-only"
        t.append(sub, style=HEX["mut"])
        right = f"▲{n['late']} late · {n['today']} today · {n['week']} to Sun {WEEK_END.day}"
        t.append(" " * max(1, inner - len(left) - len(sub) - len(right)))
        t.append(right, style=HEX["dim"])
        t.truncate(inner)
        return t

    def selected(self) -> Item | None:
        return self.items[self.cur] if self.items else None

    def action_move(self, d: int) -> None:
        self.cur = max(0, min(len(self.items) - 1, self.cur + d))
        self._paint()

    def action_side(self, d: int) -> None:
        self.action_move(d)

    def action_jump(self) -> None:
        it = self.selected()
        if it is None:
            return
        app = self.app
        app.pop_screen()
        if isinstance(app.screen, BoardsHome):
            app.pop_screen()
        if it.entry.id != app.board_id:
            app.switch_board(it.entry.id)
        app.selected_task_id = it.task.id
        app.refresh_view()
        # the real terminal kept a blank frame after the two pops until the next
        # paint (seen in the WT capture): ask the main screen for a full repaint
        app.call_after_refresh(lambda: app.screen.refresh(repaint=True, layout=True))

    def action_back(self) -> None:
        self.app.pop_screen()


class AgendaList(AgendaBase):
    """A · one list, three bands (the multi-board round's option D)."""

    def body(self, inner: int, h: int) -> Text:
        bw = 12 if inner >= 100 else 10
        pw = 20 if inner >= 100 else 0
        heads = {"late": ("LATE", RED), "today": (f"TODAY · {TODAY:%a %d %b}", SOON),
                 "week": (f"REST OF THE WEEK · to Sun {WEEK_END.day}", HEX["hd"])}
        rows: list[Text] = [self.head(inner)]
        cur_row = 0
        band = None
        for i, it in enumerate(self.items):
            if it.band != band:
                band = it.band
                rows.append(Text())
                lab, col = heads[band]
                r = Text(no_wrap=True)
                r.append(lab, style=f"bold {col}")
                r.append(" " + "─" * max(0, inner - len(lab) - 1), style=HEX["frame"])
                rows.append(r)
            on = i == self.cur
            hexc = board_hex(it.entry.color)
            r = Text(no_wrap=True)
            r.append("▶ " if on else "  ", style=HEX["accent"])
            r.append("▌", style=hexc)
            r.append(fit(it.entry.name, bw), style=f"bold {hexc}" if on else hexc)
            r.append(" ")
            if pw:
                r.append(fit(it.project, pw), style=HEX["dim"])
                r.append(" ")
            lab, col = when(it.due)
            tw = inner - 3 - bw - 1 - (pw + 1 if pw else 0) - 8
            r.append(fit(it.task.title, tw), style=f"bold {HEX['bright']}" if on else HEX["ink"])
            r.append(f"{lab:>8}", style=col)
            if on:
                r.stylize("on #16202c")
                cur_row = len(rows)
            rows.append(r)
        top = max(0, min(cur_row - h + 3, len(rows) - h))
        return Text("\n").join(rows[:1] + rows[1 + top:top + h])


class AgendaGrid(AgendaBase):
    """B · a week grid: one column per day (late first), each task a two-line card
    in its board's colour; `←→` changes the column."""
    KEYS = (("←→", "day"), ("↑↓", "task"), ("↵", "open on its board"), ("esc", "back"))

    def cols(self, inner: int):
        if inner >= 100:
            days = [TODAY + timedelta(days=k) for k in range((WEEK_END - TODAY).days + 1)]
            cols = [("LATE", RED, [x for x in self.items if x.band == "late"])]
            for d in days:
                lab = f"TODAY {d.day}" if d == TODAY else f"{d:%a} {d.day}".upper()
                cols.append((lab, SOON if d == TODAY else HEX["hd"],
                             [x for x in self.items if x.due == d]))
            return cols
        return [("LATE", RED, [x for x in self.items if x.band == "late"]),
                (f"TODAY {TODAY.day}", SOON, [x for x in self.items if x.band == "today"]),
                (f"TO SUN {WEEK_END.day}", HEX["hd"], [x for x in self.items if x.band == "week"])]

    def setup(self) -> None:
        self.col, self.row = 1, 0

    def selected(self):
        cols = self.cols(self.app.size.width - 2)
        self.col = min(self.col, len(cols) - 1)
        items = cols[self.col][2]
        return items[min(self.row, len(items) - 1)] if items else None

    def action_move(self, d: int) -> None:
        items = self.cols(self.app.size.width - 2)[self.col][2]
        self.row = max(0, min(len(items) - 1, self.row + d))
        self._paint()

    def action_side(self, d: int) -> None:
        cols = self.cols(self.app.size.width - 2)
        self.col = max(0, min(len(cols) - 1, self.col + d))
        self.row = 0
        self._paint()

    def body(self, inner: int, h: int) -> Text:
        cols = self.cols(inner)
        n = len(cols)
        cw = (inner - (n - 1)) // n
        self.col = min(self.col, n - 1)
        grid: list[list[tuple[str, str]]] = []
        for ci, (lab, col, items) in enumerate(cols):
            on_col = ci == self.col
            cells = [(fit(f"{lab} · {len(items)}" if items else lab, cw),
                      f"bold {col}" + (" on #16202c" if on_col else "")),
                     ("━" * cw if on_col else "─" * cw, HEX["accent"] if on_col else HEX["frame"])]
            for ri, it in enumerate(items):
                hexc = board_hex(it.entry.color)
                on = on_col and ri == min(self.row, len(items) - 1)
                bg = " on #1d2a3a" if on else ""
                cells.append(("▌" + fit(it.task.title, cw - 1),
                              (f"bold {HEX['bright']}" if on else HEX["ink"]) + bg))
                cells.append(("▌" + fit(it.entry.name + (" · " + it.project if cw > 18 else ""),
                                        cw - 1), hexc + bg))
                cells.append((" " * cw, ""))
            grid.append(cells)
        height = h - 2
        rows = [self.head(inner), Text()]
        for y in range(height):
            r = Text(no_wrap=True)
            for ci in range(n):
                cells = grid[ci]
                txt, sty = cells[y] if y < len(cells) else (" " * cw, "")
                if txt.startswith("▌"):
                    it_hex = None
                    # the bar takes the board colour on both card rows
                    k = (y - 2) // 3
                    items = cols[ci][2]
                    if 0 <= k < len(items):
                        it_hex = board_hex(items[k].entry.color)
                    r.append("▌", style=it_hex or sty)
                    r.append(txt[1:], style=sty)
                else:
                    r.append(txt, style=sty)
                if ci < n - 1:
                    r.append("│", style=HEX["frame"])
            rows.append(r)
        return Text("\n").join(rows)


class AgendaRuler(AgendaBase):
    """C · a lane per board across the week's days, each due a dot in the board's
    colour; the chosen day's tasks listed below, every board together."""
    KEYS = (("←→", "day"), ("↑↓", "task"), ("↵", "open on its board"), ("esc", "back"))

    def buckets(self):
        days = [TODAY + timedelta(days=k) for k in range((WEEK_END - TODAY).days + 1)]
        out = [("late", "LATE", [x for x in self.items if x.band == "late"])]
        for d in days:
            out.append((d, "TODAY" if d == TODAY else f"{d:%a} {d.day}",
                        [x for x in self.items if x.due == d]))
        return out

    def setup(self) -> None:
        self.day, self.row = 1, 0

    def selected(self):
        items = self.buckets()[self.day][2]
        return items[min(self.row, len(items) - 1)] if items else None

    def action_move(self, d: int) -> None:
        items = self.buckets()[self.day][2]
        self.row = max(0, min(len(items) - 1, self.row + d))
        self._paint()

    def action_side(self, d: int) -> None:
        self.day = max(0, min(len(self.buckets()) - 1, self.day + d))
        self.row = 0
        self._paint()

    def body(self, inner: int, h: int) -> Text:
        bks = self.buckets()
        lw = 12 if inner >= 100 else 10
        cw = min(13, (inner - lw) // len(bks))
        rows = [self.head(inner), Text()]
        r = Text(no_wrap=True)
        r.append(" " * lw)
        for i, (_k, lab, items) in enumerate(bks):
            on = i == self.day
            col = RED if i == 0 else SOON if i == 1 else HEX["hd"]
            r.append(fit(("▼ " if on else "  ") + lab, cw),
                     style=f"bold {col}" + (" on #16202c" if on else ""))
        rows.append(r)
        boards = self.app.registry.active()
        for e in boards:
            hexc = board_hex(e.color)
            r = Text(no_wrap=True)
            r.append("▌", style=hexc)
            r.append(fit(e.name, lw - 1), style=f"bold {hexc}")
            for i, (_k, _lab, items) in enumerate(bks):
                n = sum(1 for x in items if x.entry.id == e.id)
                bg = " on #16202c" if i == self.day else ""
                dots = ("●" * min(n, cw - 4) + ("+" if n > cw - 4 else "")) if n else "·"
                r.append("  ", style=bg.strip() or None)
                r.append(fit(dots, cw - 2), style=(hexc if n else HEX["frame"]) + bg)
            rows.append(r)
        rows.append(Text("─" * inner, style=HEX["frame"]))
        _k, lab, items = bks[self.day]
        head = Text(no_wrap=True)
        head.append(("LATE" if self.day == 0 else lab.upper()) + f" · {len(items)} due",
                    style=f"bold {RED if self.day == 0 else SOON if self.day == 1 else HEX['hd']}")
        head.append(f" across {len({x.entry.id for x in items})} boards", style=HEX["mut"])
        rows.append(head)
        bw = 12 if inner >= 100 else 10
        pw = 22 if inner >= 100 else 0
        room = h - len(rows)
        start = max(0, min(self.row - room + 1, len(items) - room))
        for ri, it in list(enumerate(items))[start:start + room]:
            on = ri == min(self.row, len(items) - 1)
            hexc = board_hex(it.entry.color)
            r = Text(no_wrap=True)
            r.append("▶ " if on else "  ", style=HEX["accent"])
            r.append("▌", style=hexc)
            r.append(fit(it.entry.name, bw), style=hexc)
            r.append(" ")
            if pw:
                r.append(fit(it.project, pw), style=HEX["dim"])
                r.append(" ")
            wl, wc = when(it.due)
            tw = inner - 3 - bw - 1 - (pw + 1 if pw else 0) - 8
            r.append(fit(it.task.title, tw), style=f"bold {HEX['bright']}" if on else HEX["ink"])
            r.append(f"{wl:>8}", style=wc)
            if on:
                r.stylize("on #1d2a3a")
            rows.append(r)
        if not items:
            rows.append(Text("  nothing due", style=HEX["dim"]))
        return Text("\n").join(rows)


# =============================================================================
# ITEMS 2, 3, 5 — the presentation `R`
# =============================================================================
class _ChipHeader:
    """views.header with the open board's chip, for one render."""

    def __init__(self, label):
        self.label = label
        self.orig = views.header

    def __enter__(self):
        orig, label = self.orig, self.label
        views.header = lambda title, right, w, tone="bright", chip=None: orig(
            title, right, w, tone, chip=label)

    def __exit__(self, *a):
        views.header = self.orig


class PresentChipHint(PresentScreen):
    """2 · B — the chip on the hint row only: the presenter sees the board, the
    frame (and so the export) does not."""

    def _hint(self, w: int) -> Text:
        label = self.app.board.label
        if not label:
            return super()._hint(w)
        ch = chip(*label)
        out = Text(no_wrap=True)
        out.append_text(ch)
        out.append(" ")
        out.append_text(super()._hint(w - ch.cell_len - 1))
        return out


class PresentChipFrame(PresentScreen):
    """2 · C — the chip opens the frame's head row: on screen and in the export."""

    def _frame_text(self, scroll=None):
        with _ChipHeader(self.app.board.label):
            return super()._frame_text(scroll)

    def _render_all(self):
        with _ChipHeader(self.app.board.label):
            return super()._render_all()


PRESENT_KEYS = [
    ("VIEWS", [("1 2 3", "gantt · split · all", None), ("⇥ ⇧⇥", "next / previous view", None)]),
    ("MOVE", [("↑↓ ←→", "the cursor", None), ("←→", "rail ↔ timeline", "all"),
              ("pgdn pgup", "scroll the notes", "split")]),
    ("CURATE", [("␣", "hide the cursor's row", None), ("a", "show everything hidden", None),
                ("u", "list what is hidden", None), ("⇧↑↓", "move a project up / down", "all"),
                ("enter", "fold a project", "all")]),
    ("OUT", [("x", "export this view · SVG + PNG", None), ("esc q", "leave", None),
             ("?", "these keys", None)]),
]


def present_keys_lines(view: str) -> list[Text]:
    out = []
    for head, rows in PRESENT_KEYS:
        out.append(Text(head, style=f"bold {HEX['mut']}"))
        for k, d, only in rows:
            live = only is None or only == view
            r = Text(no_wrap=True)
            r.append(f"  {k:<10}", style=KEY if live else HEX["dim"])
            r.append(d, style=HEX["ink"] if live else HEX["dim"])
            if only:
                r.append(f"  ({only})", style=HEX["reached"] if live else HEX["dim"])
            out.append(r)
    return out


class PresentKeys(ModalScreen[None]):
    """3 · A — `?` inside the presentation: its own keys, the view's live ones bright."""
    BINDINGS = [Binding("escape,question_mark,q", "dismiss", "", priority=True)]
    DEFAULT_CSS = """
    PresentKeys { align: center middle; }
    #pk-box { width: 60; max-width: 96%; height: auto; max-height: 96%; padding: 0 2;
              background: #0d1219; border: round #334154; }
    """

    def __init__(self, view: str):
        super().__init__()
        self.view = view

    def compose(self):
        lines = [Text.assemble(("PRESENTATION KEYS", f"bold {HEX['bright']}"),
                               (f" · view {self.view}", HEX["mut"]))] + present_keys_lines(self.view)
        lines.append(Text("? / esc close · dim = another view's key", style=HEX["dim"]))
        yield VerticalScroll(Static(Text("\n").join(lines)), id="pk-box")


class _HelpHint:
    def _hint(self, w: int) -> Text:
        base = PresentScreen._hint(self, w - 8)
        base.append("  ")
        base.append("?", style=KEY)
        base.append(" keys", style=HEX["mut"])
        return base


class PresentHelpModal(_HelpHint, PresentScreen):
    BINDINGS = [Binding("question_mark", "keys", "", priority=True)]

    def action_keys(self) -> None:
        self.app.push_screen(PresentKeys(views.PRESENT_SCREEN_VIEWS[self._view]))


class PresentHelpSheet(PresentScreen):
    """3 · B — `?` opens a key sheet in place of the hint row: one line per group,
    the view's live keys bright; the frame gives up the rows (never exported:
    `x` writes the frame only)."""
    BINDINGS = [Binding("question_mark", "keys", "", priority=True)]
    SHORT = [
        ("VIEWS", [("1 2 3", "gantt·split·all", None), ("⇥ ⇧⇥", "next/prev view", None)]),
        ("MOVE", [("↑↓ ←→", "cursor", None), ("←→", "rail↔timeline", "all"),
                  ("pgdn pgup", "notes", "split")]),
        ("CURATE", [("␣", "hide row", None), ("a", "show all", None), ("u", "hidden list", None),
                    ("⇧↑↓", "reorder", "all"), ("enter", "fold", "all")]),
        ("OUT", [("x", "export the frame", None), ("esc q", "leave", None)]),
    ]

    def on_mount(self) -> None:
        self._sheet = False
        self._rows = 1

    def _frame_height(self) -> int:
        return max(1, (self.size.height or 0) - getattr(self, "_rows", 1))

    def action_keys(self) -> None:
        self._sheet = not self._sheet
        self._rows = len(self._sheet_lines(self.size.width or 0)) if self._sheet else 1
        self.query_one("#present-hint").styles.height = self._rows
        self._paint()

    def _sheet_lines(self, w: int) -> list[Text]:
        view = views.PRESENT_SCREEN_VIEWS[self._view]
        out = []
        for head, rows in self.SHORT:
            r = Text(no_wrap=True)
            r.append(f"{head:<7}", style=f"bold {HEX['mut']}")
            for k, d, only in rows:
                live = only is None or only == view
                piece = Text.assemble((k, KEY if live else HEX["dim"]),
                                      (f" {d}   ", HEX["ink"] if live else HEX["dim"]))
                if r.cell_len + piece.cell_len > w - 2:
                    out.append(r)
                    r = Text(" " * 7, no_wrap=True)
                r.append_text(piece)
            out.append(r)
        foot = Text(no_wrap=True)
        foot.append("? ", style=KEY)
        foot.append("close the keys · dim = another view's key · never exported", style=HEX["dim"])
        return out + [foot]

    def _hint(self, w: int) -> Text:
        if not getattr(self, "_sheet", False):
            return _HelpHint._hint(self, w)
        return Text(chr(10)).join(self._sheet_lines(w))


class PresentReorderKJ(PresentScreen):
    """5 · A — `K` / `J` (shift+k / shift+j: plain letters every terminal passes)
    reorder too, beside `shift+↑/↓`."""
    BINDINGS = [Binding("K", "reorder(-1)", "", priority=True),
                Binding("J", "reorder(1)", "", priority=True)]

    def _hint(self, w: int) -> Text:
        h = super()._hint(w - 4)
        p = h.plain
        i = p.find("⇧↑↓")
        if i < 0:
            return h
        long = p[i:i + 11] == "⇧↑↓ reorder"
        mid = Text("⇧↑↓/K J" if long else "K J", style=HEX["mut"])
        return h[:i] + mid + h[i + 3:]


# =============================================================================
# ITEM 6 — ConfirmModal
# =============================================================================
class ConfirmFocusYes(ConfirmModal):
    """6 · A — the confirm button holds the focus: `enter` confirms at once."""

    def on_mount(self) -> None:
        self.query_one("#yes").focus()


class ConfirmKeys(ConfirmModal):
    """6 · B — `y` confirms, `n`/`esc` cancel, and a line says so; the focus stays
    on the box, so a stray `enter` does nothing."""
    BINDINGS = [Binding("y", "yes", "", priority=True), Binding("n", "no", "", priority=True)]

    def on_mount(self) -> None:
        box = self.query_one("#confirm-box")
        hint = Label(Text.assemble(("y", KEY), (f" {self.confirm.lower()}   ", HEX["mut"]),
                                   ("n", KEY), (" / ", HEX["dim"]), ("esc", KEY),
                                   (" cancel   ", HEX["mut"]), ("⇥", KEY),
                                   (" the buttons", HEX["mut"])))
        box.mount(hint)

    def action_yes(self) -> None:
        self.dismiss(True)


# =============================================================================
# ITEM 7 — start-up modals naming their board
# =============================================================================
def _board_name(app) -> tuple[str, str]:
    e = app.registry.get(app.board_id) if app.board_id else None
    return (e.name, e.color) if e else ("this board", "violet")


class OfferNamedA(MilestoneOffer):
    """7 · A — the title names the board, as a chip."""

    def on_mount(self) -> None:
        name, colour = _board_name(self.app)
        n = len(self._rows)
        title = Text.assemble(chip(name, colour), " ", ("◆ Milestones", "bold"),
                              " · convert one-day tasks?",
                              (f"   {n} candidate{'s' if n != 1 else ''} · shown once",
                               HEX["mut"]))
        self.query(".modal-title").first().update(title)


class OfferNamedB(MilestoneOffer):
    """7 · B — the box itself wears the board: its colour, its name on the border."""

    def on_mount(self) -> None:
        name, colour = _board_name(self.app)
        box = self.query_one("#offer-box")
        box.styles.border = ("heavy", board_hex(colour))
        box.border_title = Text(f" for board {name} ", style=f"bold {board_hex(colour)}")
        box.border_subtitle = Text(" answers for this board only ", style=HEX["mut"])


class IdentityNamedA(TeamIdentityPicker):
    def on_mount(self) -> None:
        name, colour = _board_name(self.app)
        self.query(".modal-title").first().update(Text.assemble(
            chip(name, colour), " ", ("Operator identity", "bold"),
            " — pick from this board's team roster"))


class IdentityNamedB(TeamIdentityPicker):
    def on_mount(self) -> None:
        name, colour = _board_name(self.app)
        box = self.query_one("#identity-box")
        box.styles.border = ("heavy", board_hex(colour))
        box.border_title = Text(f" for board {name} ", style=f"bold {board_hex(colour)}")


def push_identity(app) -> None:
    app.push_screen(app_mod.TeamIdentityPicker(ROSTER))


# =============================================================================
# ITEMS 8, 9 — notices
# =============================================================================
def warn_twice(app) -> None:
    name, _c = _board_name(app)
    app.notify(f"{name} is already open in another taskboard window (since 09:12). Both "
               "save the same file: the last save wins. Close one of them.",
               title="Boards · open twice", severity="warning", timeout=120, markup=False)


def warn_twice_chip(app) -> None:
    name, colour = _board_name(app)
    app.board.label = (f"{name} ⚠ open twice", colour)
    app.refresh_view()
    warn_twice(app)


def opened_unlisted(app) -> None:
    app.board.label = ("board-copy · not listed", "pink")
    app.refresh_view()
    app.notify("Opened elsewhere/board-copy.json without adding it to your boards "
               "(--open). B lists your 3 boards; this file is not one of them.",
               title="Boards", timeout=120, markup=False)


# =============================================================================
# the app and the scenes
# =============================================================================
class Proto(TaskboardApp):
    BINDINGS = [Binding("A", "agenda_all", "", show=False)]     # prototype: not in KEYMAP
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene: str, root: Path, seconds: float | None = None):
        sc = SCENES[scene]
        self.scene, self._steps, self._seconds = scene, sc["steps"], seconds
        self.played = False
        fx.build(root, last=sc.get("last", "client-a"), offer=sc.get("offer", False),
                 with_copy=sc.get("copy", False))
        reg = Registry.load(root / "boards.json", root / "board.json")
        if sc.get("unlisted"):
            path = str(fx.copy_path(root))
        else:
            entry = reg.opening()
            reg.touch(entry.id, datetime.now())
            path = entry.path
        self._agenda = sc.get("agenda")
        self._undo_patch = []
        for name, val in sc.get("patch", {}).items():
            self._undo_patch.append((name, getattr(app_mod, name)))
            setattr(app_mod, name, val)
        super().__init__(board_path=path, registry=reg, team_sync_interval=1e9)

    def unpatch(self) -> None:
        for name, val in self._undo_patch:
            setattr(app_mod, name, val)

    def check_action(self, action, parameters):
        if action == "agenda_all":
            return self._agenda is not None and not isinstance(self.screen, AgendaBase)
        return super().check_action(action, parameters)

    def action_agenda_all(self) -> None:
        self.push_screen(self._agenda())

    def on_mount(self) -> None:          # runs BEFORE TaskboardApp.on_mount (MRO dispatch)
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.0, lambda: self.run_worker(self._play()))

    async def _play(self) -> None:
        for step in self._steps:
            if isinstance(step, str):
                await self._press_keys([step])
            else:
                r = step(self)
                if inspect.isawaitable(r):
                    await r
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.6)
        self.played = True
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            Path(ready).write_text(f"ready {self.screen_stack!r} board={self.board_id} "
                                   f"sel={self.selected_task_id}", encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


P = "PresentScreen"
SCENES: dict[str, dict] = {
    # 1 · the agenda
    "ag-now": dict(steps=[]),
    "ag-A": dict(steps=["A", "down", "down", "down"], agenda=AgendaList),
    "ag-A-open": dict(steps=["A", "down", "down", "down", "down", "enter"], agenda=AgendaList),
    "ag-B": dict(steps=["A", "down"], agenda=AgendaGrid),
    "ag-C": dict(steps=["A", "down"], agenda=AgendaRuler),
    # 2 · the board's name in the presentation
    "pc-now": dict(steps=["escape", "R"]),
    "pc-B": dict(steps=["escape", "R"], patch={P: PresentChipHint}),
    "pc-C": dict(steps=["escape", "R"], patch={P: PresentChipFrame}),
    # 3 · `?` inside the presentation
    "ph-now": dict(steps=["escape", "R", "3", "question_mark"]),
    "ph-A": dict(steps=["escape", "R", "3", "question_mark"], patch={P: PresentHelpModal}),
    "ph-B": dict(steps=["escape", "R", "3", "question_mark"], patch={P: PresentHelpSheet}),
    # 4 · the export (the screen at `x`; the files themselves: `exports`)
    "ex-now": dict(steps=["escape", "R", "3", "x"]),
    # 5 · a second reorder key
    "ro-now": dict(steps=["escape", "R", "3", "down"]),
    "ro-A": dict(steps=["escape", "R", "3", "down"], patch={P: PresentReorderKJ}),
    "ro-A-moved": dict(steps=["escape", "R", "3", "down", "K"], patch={P: PresentReorderKJ}),
    # 6 · ConfirmModal (the home's archive)
    "cf-now": dict(steps=["left", "x"]),
    "cf-A": dict(steps=["left", "x"], patch={"ConfirmModal": ConfirmFocusYes}),
    "cf-B": dict(steps=["left", "x"], patch={"ConfirmModal": ConfirmKeys}),
    # 7 · start-up modals over the home
    "su-now-offer": dict(steps=[], offer=True),
    "su-A-offer": dict(steps=[], offer=True, patch={"MilestoneOffer": OfferNamedA}),
    "su-B-offer": dict(steps=[], offer=True, patch={"MilestoneOffer": OfferNamedB}),
    "su-now-id": dict(steps=[push_identity]),
    "su-A-id": dict(steps=[push_identity], patch={"TeamIdentityPicker": IdentityNamedA}),
    "su-B-id": dict(steps=[push_identity], patch={"TeamIdentityPicker": IdentityNamedB}),
    # 8 · two instances on one board
    "in-now": dict(steps=["enter"]),
    "in-A": dict(steps=["enter", warn_twice]),
    "in-B": dict(steps=["enter", warn_twice_chip]),
    # 9 · `--board PATH`
    "rg-now": dict(steps=[], copy=True, last="board-copy"),
    "rg-A": dict(steps=["escape", opened_unlisted], unlisted=True),
}
SIZES = [(118, 30), (80, 24)]


def _strip_font(svg: str) -> str:
    return re.sub(r"@font-face\s*\{[^}]*\}", "", svg)


async def _shot_one(scene: str, size) -> None:
    root = Path(tempfile.mkdtemp(prefix="tbbr-"))
    app = Proto(scene, root)
    try:
        async with app.run_test(size=size) as pilot:
            for _ in range(200):
                if app.played:
                    break
                await pilot.pause(0.1)
            await pilot.pause(0.3)
            svg = app.export_screenshot(title=f"taskboard · {scene} · {size[0]}x{size[1]}")
            (OUT / "svg" / f"{scene}_{size[0]}x{size[1]}.svg").write_text(
                _strip_font(svg), encoding="utf-8")
    finally:
        app.unpatch()
        shutil.rmtree(root, ignore_errors=True)


def shot(names: list[str]) -> None:
    (OUT / "svg").mkdir(parents=True, exist_ok=True)
    for name in names or list(SCENES):
        for size in SIZES:
            asyncio.run(_shot_one(name, size))
            print("svg", name, size)


# ---- ITEM 4: the export files, from the app's own export path -----------------
async def _export(size) -> dict:
    """`x` in view 3 (the shipped export: SVG + its Edge PNG), then the same
    timeline rendered with no cursor and cut to its content (the variant)."""
    root = Path(tempfile.mkdtemp(prefix="tbbr-ex-"))
    app = Proto("ex-now", root)
    dest = OUT / "export"
    dest.mkdir(parents=True, exist_ok=True)
    tag = f"{size[0]}x{size[1]}"
    facts = {}
    try:
        async with app.run_test(size=size) as pilot:
            for _ in range(300):
                if app.played:
                    break
                await pilot.pause(0.1)
            await pilot.pause(0.5)
            reports = Path(app.board.path).parent / "reports"
            for f in sorted(reports.glob("present-*-all.*")):
                shutil.copyfile(f, dest / f"now_{tag}{f.suffix}")
            scr = app.screen
            r = scr._render_all()
            facts["now_rows"] = scr._frame_height()
            facts["now_width"] = r.timeline_w
            # the variant: no cursor (a rail cursor on no project draws none on the
            # timeline), the empty rows under the last project cut
            lines, _s, _d = views._all_timeline(app.board, r.timeline_w, scr._frame_height(),
                                                TODAY, ("proj", "-none-"), frozenset(), True)
            blank = " " * r.timeline_w
            while lines and lines[-1] == blank:
                lines.pop()
            text = views.to_text(lines, len(lines), r.timeline_w)
            svg = views.save_present_svg(text, dest / f"clean_{tag}.svg", r.timeline_w, len(lines))
            views.save_present_png(svg, dest / f"clean_{tag}.png", r.timeline_w, len(lines))
            facts["clean_rows"] = len(lines)
    finally:
        app.unpatch()
        shutil.rmtree(root, ignore_errors=True)
    return facts


def exports() -> None:
    facts = {}
    for size in SIZES:
        facts[f"{size[0]}x{size[1]}"] = asyncio.run(_export(size))
    (OUT / "export" / "facts.json").write_text(json.dumps(facts, indent=2), encoding="utf-8")
    print(json.dumps(facts, indent=2))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "shot":
        shot(args[1:])
    elif args and args[0] == "exports":
        exports()
    elif args and args[0] == "live":
        root = Path(tempfile.mkdtemp(prefix="tbbr-live-"))
        Proto(args[1], root, float(args[2]) if len(args) > 2 else None).run()
        shutil.rmtree(root, ignore_errors=True)
    else:
        print(__doc__)

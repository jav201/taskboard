"""THROWAWAY prototype — several boards in one taskboard (multi-board round).

Sub-shape A (tui-design PROTOTYPE.md): the real `TaskboardApp` is subclassed
(`MBApp`) in the capture process only; nothing under taskboard/ is edited. The
board views, key bar, help and modals are the shipped ones. What is new here:

  * a registry (`boards.json`) beside the default board: name, path, colour,
    last opened — `Registry`;
  * the switcher, in three variants (VARIANT):
      A  `B` opens a picker modal: one line per board, type-to-filter, ↵ opens
      B  a tab strip docked on top; `<` / `>` cycle boards; `B` opens A's picker
      C  a home launcher of board cards (counts + a due strip + next dues),
         shown at launch when there is more than one board, and on `B`
  * the active board's chip at the head of every view (A, C) — P2;
  * `m` in the projects manager (`P`): move a project with its tasks to
    another board, crossing links listed and dropped only on confirmation — P3;
  * create / edit (name + colour) / archive a board from the switcher — P4;
  * option D: `A` opens a read-only agenda across every board.

Writes go to the capture's temporary folder only.
"""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

from rich.markup import escape
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Input, Label, Static

from taskboard import app as app_mod
from taskboard import keymap as km
from taskboard import views
from taskboard.modals import ProjectPicker
from taskboard.models import PROJECT_COLORS, Board, is_open
from taskboard.views import HEX, fit, vis

VARIANT = "A"
ROOT: Path | None = None             # the fake ~/.taskboard of this capture
TODAY = date(2026, 10, 20)
NOW = datetime(2026, 10, 20, 9, 30)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
RED = HEX.get("over", "#f43f5e")
SOON = HEX.get("soon", "#fbbf24")
BG = "#0d1117"


def chex(colour: str) -> str:
    return HEX.get(colour, HEX["violet"])


def pretty(path: str | Path) -> str:
    p = Path(path)
    try:
        return "~/.taskboard/" + p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def md(d: date) -> str:
    return f"{d:%b} {d.day}"


def ago(iso: str) -> str:
    mins = int((NOW - datetime.fromisoformat(iso)).total_seconds() // 60)
    if mins < 2:
        return "just now"
    if mins < 60:
        return f"{mins}m ago"
    if mins < 60 * 24:
        return f"{mins // 60}h ago"
    return f"{mins // (60 * 24)}d ago"


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "board"


# --------------------------------------------------------------------------
# the registry
# --------------------------------------------------------------------------
class Registry:
    def __init__(self, path: Path):
        self.path = path
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.entries: list[dict] = raw["boards"]
        self.last: str = raw.get("last") or self.entries[0]["id"]

    def save(self) -> None:
        self.path.write_text(json.dumps({"version": 1, "last": self.last,
                                         "boards": self.entries}, indent=2), encoding="utf-8")

    def get(self, bid: str) -> dict:
        return next(e for e in self.entries if e["id"] == bid)

    def active(self) -> list[dict]:
        return [e for e in self.entries if not e.get("archived")]

    def touch(self, bid: str) -> None:
        self.last = bid
        self.get(bid)["last_opened"] = NOW.isoformat(timespec="minutes")
        self.save()


REG: Registry | None = None
_BOARDS: dict[str, Board] = {}


def board_of(bid: str, app=None) -> Board:
    """The live board when it is the open one; otherwise a fresh read."""
    if app is not None and getattr(app, "board_id", None) == bid:
        return app.board
    return Board.load(REG.get(bid)["path"])


def summary(board: Board, today: date = TODAY) -> dict:
    open_ = [t for t in board.tasks if is_open(board, t)]
    dues = [(date.fromisoformat(t.due_date), t) for t in open_ if t.due_date]
    late = [x for x in dues if x[0] < today]
    upcoming = sorted([x for x in dues if x[0] >= today], key=lambda x: x[0])
    week_end = today + timedelta(days=6 - today.weekday())
    return {"open": len(open_), "late": len(late),
            "week": sum(1 for d, _ in upcoming if d <= week_end),
            "next": upcoming[:5], "late_list": sorted(late, key=lambda x: x[0]),
            "by_day": Counter((d - today).days for d, _ in upcoming),
            "projects": len([p for p in board.projects if not p.archived])}


# --------------------------------------------------------------------------
# P2: the board's chip at the head of every view
# --------------------------------------------------------------------------
_header = views.header


def chip_markup(entry: dict) -> str:
    return f"[b {BG} on {chex(entry['color'])}] {escape(entry['name'])} [/] "


def _header_with_chip(title, right, w, tone="bright"):
    app = CURRENT_APP
    if VARIANT != "B" and app is not None and getattr(app, "board_id", None):
        title = chip_markup(REG.get(app.board_id)) + title
    return _header(title, right, w, tone)


CURRENT_APP = None
views.header = _header_with_chip


# --------------------------------------------------------------------------
# the keys (the seat is patched, so the bar, `?` and the palette all show them)
# --------------------------------------------------------------------------
def patch_keymap() -> None:
    base = tuple(k for k in km.KEYMAP if k.action not in ("boards", "board_cycle(-1)",
                                                          "board_cycle(1)", "all_boards"))
    new = [km.Key("B", "B", "boards", "Boards", universal=True, primary=True, group="system")]
    if VARIANT == "B":
        new += [km.Key("less_than_sign", "<", "board_cycle(-1)", "Board", primary=True,
                       group="system"),
                km.Key("greater_than_sign", ">", "board_cycle(1)", "", primary=True,
                       group="system")]
    new.append(km.Key("A", "A", "all_boards", "All boards", group="misc", bar=False))
    km.KEYMAP = base[:3] + tuple(new) + base[3:]


# --------------------------------------------------------------------------
# B: the tab strip
# --------------------------------------------------------------------------
class TabStrip(Static):
    DEFAULT_CSS = "TabStrip { dock: top; height: 1; width: 1fr; background: #0b0f17; }"

    def on_resize(self, _event) -> None:
        self.refresh_strip()

    def refresh_strip(self) -> None:
        self.update(self.render_strip(self.size.width or self.app.size.width))

    def render_strip(self, w: int) -> Text:
        app = self.app
        entries = REG.active()
        lates = {e["id"]: summary(board_of(e["id"], app))["late"] for e in entries}
        idx = next(i for i, e in enumerate(entries) if e["id"] == app.board_id)
        right = f"{idx + 1}/{len(entries)}  < > "

        def build(cut: int | None) -> Text:
            t = Text(no_wrap=True)
            for e in entries:
                hexc, late = chex(e["color"]), lates[e["id"]]
                name = e["name"]
                if e["id"] == app.board_id:
                    t.append(f" {name} ", style=f"bold {BG} on {hexc}")
                    if late:
                        t.append(f"▲{late}", style=f"bold {RED} on {hexc}")
                        t.append(" ", style=f"on {hexc}")
                else:
                    if cut is not None:
                        name = fit(name, cut).rstrip() if cut > 1 else ""
                    t.append("▌", style=hexc)
                    if name:
                        t.append(f"{name}", style=HEX["mut"])
                    if late and (cut is None or cut > 3):
                        t.append(f" ▲{late}", style=RED)
                t.append("  " if cut is None or cut > 3 else " ")
            return t

        for cut in (None, 12, 7, 4, 1):
            t = build(cut)
            if t.cell_len + len(right) <= w - 1:
                break
        gap = max(1, w - t.cell_len - len(right))
        t.append(" " * gap)
        t.append(right, style=HEX["dim"])
        t.truncate(w)
        return t


# --------------------------------------------------------------------------
# A: the picker modal (also B's `B`)
# --------------------------------------------------------------------------
class BoardPicker(ModalScreen[None]):
    BINDINGS = [Binding("escape", "close", "Close", priority=True),
                Binding("up", "move(-1)", "", priority=True, show=False),
                Binding("down", "move(1)", "", priority=True, show=False),
                Binding("enter", "open", "", priority=True, show=False),
                Binding("ctrl+n", "new", "", priority=True, show=False),
                Binding("ctrl+e", "edit", "", priority=True, show=False),
                Binding("ctrl+x", "archive", "", priority=True, show=False)]
    DEFAULT_CSS = """
    BoardPicker { align: center top; background: #0007; }
    #bp-box { height: auto; max-height: 100%; padding: 0 1; margin-top: 2;
              background: #0d1219; border: round #334154; }
    #bp-filter { border: none; height: 1; padding: 0; background: #151c26; margin: 1 0 0 0; }
    #bp-rows { margin: 1 0 0 0; }
    #bp-keys { margin: 1 0 0 0; }
    """

    def __init__(self):
        super().__init__()
        self.query_text = ""
        self.cursor = 0
        self.rows: list[dict] = []

    def compose(self) -> ComposeResult:
        with Vertical(id="bp-box"):
            yield Static(id="bp-title")
            yield Input(placeholder="type to filter boards", id="bp-filter")
            yield Static(id="bp-rows")
            yield Static(id="bp-keys")

    def _box_w(self) -> int:
        return max(30, min(self.app.size.width - 4, 124))

    def on_mount(self) -> None:
        self.query_one("#bp-box").styles.width = self._box_w()
        if self.app.size.height < 30:
            self.query_one("#bp-box").styles.margin = (0, 0, 0, 0)
        self._filter()
        cur = next((i for i, e in enumerate(self.rows) if e["id"] == self.app.board_id), 0)
        self.cursor = cur
        self.query_one("#bp-filter", Input).focus()
        self._paint()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_text = event.value
        self._filter()
        self.cursor = 0
        self._paint()

    def _filter(self) -> None:
        q = self.query_text.lower().strip()
        self.rows = [e for e in REG.active() if q in e["name"].lower()]

    def _paint(self) -> None:
        inner = self._box_w() - 4
        n = len(REG.active())
        title = Text()
        title.append("Boards", style=f"bold {HEX['bright']}")
        title.append(f"  {n} · {len(self.rows)} shown" if self.query_text else f"  {n}",
                     style=HEX["dim"])
        self.query_one("#bp-title", Static).update(title)
        self.query_one("#bp-rows", Static).update(self._rows(inner))
        keys = ("↑↓ move · ↵ open · ^n new · ^e name/colour · ^x archive · esc close"
                if inner >= 70 else "↑↓ · ↵ open · ^n new · ^e edit · ^x archive · esc")
        self.query_one("#bp-keys", Static).update(Text(fit(keys, inner).rstrip(),
                                                       style=HEX["dim"]))

    def _rows(self, inner: int) -> Text:
        out = Text(no_wrap=True, overflow="ellipsis")
        if not self.rows:
            out.append("no board matches — ^n creates one with this name", style=HEX["dim"])
            return out
        wide = inner >= 96
        name_w = 22 if inner >= 70 else 16
        q = self.query_text.lower().strip()
        for i, e in enumerate(self.rows):
            s = summary(board_of(e["id"], self.app))
            on = i == self.cursor
            if i:
                out.append("\n")
            out.append("▶ " if on else "  ", style=HEX["accent"])
            out.append("██ ", style=chex(e["color"]))
            name = fit(e["name"], name_w)
            j = name.lower().find(q) if q else -1
            nstyle = f"bold {HEX['bright']}" if on else HEX["ink"]
            if j >= 0:
                out.append(name[:j], style=nstyle)
                out.append(name[j:j + len(q)], style=f"bold underline {HEX['accent']}")
                out.append(name[j + len(q):], style=nstyle)
            else:
                out.append(name, style=nstyle)
            out.append("●" if e["id"] == self.app.board_id else " ", style=HEX["accent"])
            out.append(f" {s['open']:>3} open", style=HEX["hd"])
            out.append(f"  ▲{s['late']:<2}" if s["late"] else "   · ",
                       style=RED if s["late"] else HEX["dim"])
            rest = inner - (2 + 3 + name_w + 1 + 9 + 5)
            tail = f"{ago(e['last_opened']):>9}" if wide else ""
            rest -= len(tail)
            if s["next"]:
                d, t = s["next"][0]
                col = SOON if d == TODAY else HEX["hd"]
                lab = "today" if d == TODAY else md(d)
                out.append(f"  next {lab:<6} ", style=col)
                out.append(fit(t.title, max(0, rest - 14)), style=HEX["mut"])
            else:
                out.append(fit("  nothing due", rest), style=HEX["dim"])
            if tail:
                out.append(tail, style=HEX["dim"])
        return out

    def action_move(self, d: int) -> None:
        if self.rows:
            self.cursor = max(0, min(len(self.rows) - 1, self.cursor + d))
            self._paint()

    def action_open(self) -> None:
        if not self.rows:
            return
        bid = self.rows[self.cursor]["id"]
        self.dismiss(None)
        self.app.switch_board(bid)

    def action_new(self) -> None:
        self.app.push_screen(BoardForm(None, self.query_text.strip()), self._formed)

    def action_edit(self) -> None:
        if self.rows:
            self.app.push_screen(BoardForm(self.rows[self.cursor]), self._formed)

    def _formed(self, bid: str | None) -> None:
        if bid is None:
            self._filter()
            self._paint()
            return
        self.dismiss(None)
        self.app.switch_board(bid)

    def action_archive(self) -> None:
        if not self.rows or self.rows[self.cursor]["id"] == self.app.board_id:
            self.app.notify("The open board cannot be archived — switch first.",
                            title="Boards", severity="warning", markup=False)
            return
        e = self.rows[self.cursor]
        e["archived"] = True
        REG.save()
        self.app.notify(f"Archived {e['name']} — its folder is untouched.", title="Boards",
                        markup=False)
        self._filter()
        self.cursor = min(self.cursor, max(0, len(self.rows) - 1))
        self._paint()

    def action_close(self) -> None:
        self.dismiss(None)


class BoardForm(ModalScreen[str | None]):
    """Create (entry None) or edit a board: a name and one of the 8 hues."""
    BINDINGS = [Binding("escape", "cancel", "", priority=True),
                Binding("tab", "hue(1)", "", priority=True, show=False),
                Binding("shift+tab", "hue(-1)", "", priority=True, show=False)]
    DEFAULT_CSS = """
    BoardForm { align: center middle; background: #0007; }
    #bf-box { width: 64; max-width: 100%; height: auto; padding: 0 1;
              background: #0d1219; border: round #334154; }
    #bf-name { border: none; height: 1; padding: 0; background: #151c26; margin: 1 0 0 0; }
    #bf-hues, #bf-path { margin: 1 0 0 0; }
    #bf-keys { margin: 1 0 0 0; }
    """

    def __init__(self, entry: dict | None, name: str = ""):
        super().__init__()
        self.entry = entry
        self.hue = PROJECT_COLORS.index(entry["color"]) if entry else 2
        self.initial = entry["name"] if entry else name

    def compose(self) -> ComposeResult:
        with Vertical(id="bf-box"):
            yield Static(Text("Edit board" if self.entry else "New board",
                              style=f"bold {HEX['bright']}"))
            yield Input(value=self.initial, placeholder="board name", id="bf-name")
            yield Static(id="bf-hues")
            yield Static(id="bf-path")
            yield Static(Text("⇥ colour · ↵ " + ("save" if self.entry else "create and open")
                              + " · esc cancel", style=HEX["dim"]), id="bf-keys")

    def on_mount(self) -> None:
        self.query_one("#bf-name", Input).focus()
        self._paint()

    def on_input_changed(self, _e) -> None:
        self._paint()

    def _paint(self) -> None:
        t = Text("colour  ", style=HEX["mut"])
        for i, c in enumerate(PROJECT_COLORS):
            on = i == self.hue
            t.append("[" if on else " ", style=HEX["bright"])
            t.append("██", style=chex(c))
            t.append("]" if on else " ", style=HEX["bright"])
        t.append(f"  {PROJECT_COLORS[self.hue]}", style=HEX["dim"])
        self.query_one("#bf-hues", Static).update(t)
        name = self.query_one("#bf-name", Input).value.strip()
        p = Text("file    ", style=HEX["mut"])
        if self.entry:
            p.append(pretty(self.entry["path"]) + "  (unchanged)", style=HEX["dim"])
        else:
            p.append(f"~/.taskboard/boards/{slug(name)}/board.json", style=HEX["hd"])
        self.query_one("#bf-path", Static).update(p)

    def action_hue(self, d: int) -> None:
        self.hue = (self.hue + d) % len(PROJECT_COLORS)
        self._paint()

    def on_input_submitted(self, _e) -> None:
        name = self.query_one("#bf-name", Input).value.strip()
        if not name:
            return
        colour = PROJECT_COLORS[self.hue]
        if self.entry:
            self.entry["name"], self.entry["color"] = name, colour
            REG.save()
            self.dismiss(self.entry["id"])
            return
        bid = slug(name)
        path = ROOT / "boards" / bid / "board.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        from fixture import SETTINGS
        Board([], [], path, json.loads(json.dumps(SETTINGS)), PHASES).save()
        REG.entries.append({"id": bid, "name": name, "color": colour, "path": str(path),
                            "last_opened": NOW.isoformat(timespec="minutes"),
                            "archived": False})
        REG.save()
        self.dismiss(bid)

    def action_cancel(self) -> None:
        self.dismiss(None)


# --------------------------------------------------------------------------
# C: the home launcher
# --------------------------------------------------------------------------


def due_strip(s: dict, inner: int, colour: str) -> tuple[Text, Text]:
    """Late badge + one cell (or two) per day from today; height = open tasks due."""
    badge = f"▲{s['late']} " if s["late"] else "   "
    room = inner - len(badge) - 1
    for days, cw in ((28, 2), (21, 2), (14, 2), (28, 1), (21, 1), (14, 1), (7, 1)):
        if days * cw <= room:
            break
    bars, axis = Text(no_wrap=True), Text(no_wrap=True)
    bars.append(badge, style=f"bold {RED}" if s["late"] else HEX["dim"])
    axis.append(" " * len(badge))
    glyph = {0: "·", 1: "▃", 2: "▅", 3: "▇"}
    for i in range(days):
        d = TODAY + timedelta(days=i)
        n = s["by_day"].get(i, 0)
        g = glyph.get(n, "█")
        weekend = d.weekday() >= 5
        style = (HEX["dim"] if n == 0 else (SOON if i == 0 else colour))
        if n == 0 and weekend:
            style = "#3a4350"
        bars.append(g.ljust(cw) if n == 0 else g * cw, style=style)
    # the axis: today, then each Monday's date; the rest stays quiet
    marks = [(0, str(TODAY.day))] + [(i, f"{(TODAY + timedelta(days=i)).day}")
                                      for i in range(1, days)
                                      if (TODAY + timedelta(days=i)).weekday() == 0]
    row = [" "] * (days * cw)
    for i, lab in marks:
        for j, ch in enumerate(lab):
            if i * cw + j < len(row):
                row[i * cw + j] = ch
    line = "".join(row)
    first = len(str(TODAY.day))
    axis.append(line[:first], style=f"bold {SOON}")
    axis.append(line[first:], style=HEX["dim"])
    return bars, axis


class BoardCard(Static):
    pass


class HomeScreen(Screen[None]):
    BINDINGS = [Binding("escape", "back", "", priority=True),
                Binding("left,h", "move(-1)", "", priority=True, show=False),
                Binding("right,l", "move(1)", "", priority=True, show=False),
                Binding("up,k", "move(-2)", "", priority=True, show=False),
                Binding("down,j", "move(2)", "", priority=True, show=False),
                Binding("enter", "open", "", priority=True, show=False),
                Binding("n", "new", "", show=False),
                Binding("e", "edit", "", show=False),
                Binding("x", "archive", "", show=False),
                Binding("A", "all", "", show=False),
                Binding("q", "quit_app", "", show=False)]
    DEFAULT_CSS = """
    HomeScreen { background: #0d1117; }
    #home-title { height: 1; padding: 0 1; }
    #home-grid { grid-size: 2; grid-gutter: 1 2; height: auto; padding: 1 1 0 1; }
    BoardCard { height: auto; padding: 0 1; border-title-style: bold; border-subtitle-color: #5b6675; }
    #home-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    """

    def __init__(self, at_launch: bool = False):
        super().__init__()
        self.at_launch = at_launch
        self.entries = REG.active()
        self.cursor = next((i for i, e in enumerate(self.entries) if e["id"] == REG.last), 0)

    def compose(self) -> ComposeResult:
        yield Static(id="home-title")
        with Grid(id="home-grid"):
            for e in self.entries:
                yield BoardCard(id=f"card-{e['id']}")
        yield Static(id="home-keys")

    def on_mount(self) -> None:
        self._paint()

    def on_resize(self, _e) -> None:
        self._paint()

    def _paint(self) -> None:
        w, h = self.app.size
        inner = (w - 2 - 2) // 2 - 4
        n_next = 5 if h >= 40 else 3 if h >= 30 else 1
        late_tot = 0
        for i, e in enumerate(self.entries):
            s = summary(board_of(e["id"], self.app))
            late_tot += s["late"]
            hexc = chex(e["color"])
            card = self.query_one(f"#card-{e['id']}", BoardCard)
            on = i == self.cursor
            card.styles.border = ("heavy" if on else "round", hexc if on else "#334154")
            card.styles.border_title_color = hexc
            card.border_title = (("▶ " if on else "") + e["name"])
            card.border_subtitle = ("open now" if e["id"] == self.app.board_id else
                                    "opened " + ago(e["last_opened"]))
            t = Text()
            parts = [(f"{s['open']} open", f"bold {HEX['bright']}"),
                     (f"▲{s['late']} late" if s["late"] else "0 late",
                      f"bold {RED}" if s["late"] else HEX["dim"]),
                     (f"{s['week']} due this week", HEX["hd"]),
                     (f"{s['projects']} projects", HEX["dim"])]
            if sum(len(a) + 5 for a, _ in parts) > inner:
                parts = parts[:3]
                parts[2] = (f"{s['week']} this week", HEX["hd"])
            for j, (a, st) in enumerate(parts):
                if j:
                    t.append("  ·  " if inner > 50 else " · ", style=HEX["dim"])
                t.append(a, style=st)
            bars, axis = due_strip(s, inner, hexc)
            t.append("\n")
            t.append_text(bars)
            t.append("\n")
            t.append_text(axis)
            for d, task in s["next"][:n_next]:
                t.append("\n")
                lab = "today" if d == TODAY else md(d)
                t.append(f"{lab:>6}  ", style=SOON if d == TODAY else HEX["hd"])
                t.append(fit(task.title, inner - 8).rstrip(), style=HEX["mut"])
            if not s["next"]:
                t.append("\n")
                t.append("nothing due", style=HEX["dim"])
            if h >= 40:                                  # room: the projects, by colour
                line = Text()
                for p in [p for p in board_of(e["id"], self.app).projects if not p.archived]:
                    line.append("■ ", style=chex(p.color))
                    line.append(p.name + "   ", style=HEX["mut"])
                line.truncate(inner, overflow="ellipsis")
                t.append("\n")
                t.append_text(line)
            card.update(t)
        title = Text(no_wrap=True)
        title.append("◆ TASKBOARD", style=f"bold {HEX['bright']}")
        title.append("  boards", style=HEX["mut"])
        right = f"{len(self.entries)} boards · ▲{late_tot} late · {TODAY:%a %d %b}"
        title.append(" " * max(1, w - 2 - title.cell_len - len(right)))
        title.append(right, style=HEX["dim"])
        self.query_one("#home-title", Static).update(title)
        keys = [("←→↑↓", "move"), ("↵", "open"), ("n", "new"), ("e", "name/colour"),
                ("x", "archive"), ("A", "all boards"), ("esc", "back"), ("q", "quit")]
        k = Text(no_wrap=True)
        for key, lab in keys:
            k.append(key, style=f"b {HEX['bright']}")
            k.append(f" {lab}  ", style=HEX["mut"])
        k.truncate(w - 2)
        self.query_one("#home-keys", Static).update(k)

    def action_move(self, d: int) -> None:
        self.cursor = max(0, min(len(self.entries) - 1, self.cursor + d))
        self._paint()

    def action_open(self) -> None:
        bid = self.entries[self.cursor]["id"]
        self.app.pop_screen()
        self.app.switch_board(bid)

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_new(self) -> None:
        self.app.push_screen(BoardForm(None), self._formed)

    def action_edit(self) -> None:
        self.app.push_screen(BoardForm(self.entries[self.cursor]), self._formed)

    def _formed(self, bid):
        if bid:
            self.app.pop_screen()
            self.app.switch_board(bid)

    def action_archive(self) -> None:
        self.app.notify("Archive: same rule as the picker (not the open board).",
                        title="Boards", markup=False)

    def action_all(self) -> None:
        self.app.push_screen(AllBoardsAgenda())

    def action_quit_app(self) -> None:
        self.app.exit()


# --------------------------------------------------------------------------
# D (option): one read-only agenda across every board
# --------------------------------------------------------------------------
class AllBoardsAgenda(Screen[None]):
    BINDINGS = [Binding("escape,A", "back", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True, show=False),
                Binding("down,j", "move(1)", "", priority=True, show=False),
                Binding("enter", "jump", "", priority=True, show=False)]
    DEFAULT_CSS = """
    AllBoardsAgenda { background: #0d1117; overflow-y: hidden; }
    #ag-body { padding: 0 1; }
    #ag-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    """

    def __init__(self):
        super().__init__()
        self.items: list[tuple[str, str, object, date, str]] = []
        self.cursor = 0

    def compose(self) -> ComposeResult:
        yield Static(id="ag-body")
        yield Static(id="ag-keys")

    def on_mount(self) -> None:
        week_end = TODAY + timedelta(days=6 - TODAY.weekday())
        for e in REG.active():
            b = board_of(e["id"], self.app)
            pname = {p.id: p.name for p in b.projects}
            for t in b.tasks:
                if not (is_open(b, t) and t.due_date):
                    continue
                d = date.fromisoformat(t.due_date)
                band = ("late" if d < TODAY else "today" if d == TODAY
                        else "week" if d <= week_end else None)
                if band:
                    self.items.append((band, e["id"], t, d, pname.get(t.project_id, "")))
        order = {"late": 0, "today": 1, "week": 2}
        self.items.sort(key=lambda x: (order[x[0]], x[3]))
        self._paint()

    def _paint(self) -> None:
        w, _h = self.app.size
        inner = w - 2
        heads = {"late": ("LATE", RED), "today": (f"TODAY · {TODAY:%a %d %b}", SOON),
                 "week": ("REST OF THIS WEEK", HEX["hd"])}
        bw = 20 if inner >= 110 else 12
        pw = 20 if inner >= 110 else 0
        t = Text(no_wrap=True, overflow="ellipsis")
        left = "◆ ALL BOARDS  read-only" + (" · one list across every board"
                                           if inner >= 110 else "")
        counts = Counter(x[0] for x in self.items)
        right = (f"▲{counts['late']} late · {counts['today']} today · "
                 f"{counts['week']} this week")
        t.append(left, style=f"bold {HEX['bright']}")
        t.append(" " * max(1, inner - len(left) - len(right)))
        t.append(right, style=HEX["dim"])
        band = None
        for i, (b, bid, task, d, pname) in enumerate(self.items):
            if b != band:
                band = b
                t.append("\n\n")
                lab, col = heads[b]
                t.append(lab, style=f"bold {col}")
                t.append(" " + "─" * max(0, inner - len(lab) - 1), style=HEX["frame"])
            e = REG.get(bid)
            on = i == self.cursor
            t.append("\n")
            t.append("▶ " if on else "  ", style=HEX["accent"])
            t.append("▌", style=chex(e["color"]))
            t.append(fit(e["name"], bw), style=chex(e["color"]))
            t.append(" ")
            if pw:
                t.append(fit(pname, pw), style=HEX["dim"])
                t.append(" ")
            when = (f"▲{(TODAY - d).days}d" if d < TODAY else "today" if d == TODAY
                    else f"{d:%a} {d.day}")
            title_w = inner - 2 - 1 - bw - 1 - (pw + 1 if pw else 0) - 8
            t.append(fit(task.title, title_w),
                     style=f"bold {HEX['bright']}" if on else HEX["ink"])
            t.append(f"{when:>8}", style=RED if d < TODAY else SOON if d == TODAY
                     else HEX["hd"])
        self.query_one("#ag-body", Static).update(t)
        k = Text(no_wrap=True)
        for key, lab in (("↑↓", "move"), ("↵", "open on its board"), ("esc", "back")):
            k.append(key, style=f"b {HEX['bright']}")
            k.append(f" {lab}  ", style=HEX["mut"])
        k.append("· option D: nothing here is editable", style=HEX["dim"])
        k.truncate(inner)
        self.query_one("#ag-keys", Static).update(k)

    def action_move(self, d: int) -> None:
        self.cursor = max(0, min(len(self.items) - 1, self.cursor + d))
        self._paint()

    def action_jump(self) -> None:
        _b, bid, task, _d, _p = self.items[self.cursor]
        self.app.pop_screen()
        if isinstance(self.app.screen, HomeScreen):
            self.app.pop_screen()
        self.app.switch_board(bid)
        self.app.selected_task_id = task.id
        self.app.refresh_view()

    def action_back(self) -> None:
        self.app.pop_screen()


# --------------------------------------------------------------------------
# P3: move a project (with its tasks) to another board
# --------------------------------------------------------------------------
def crossing(board: Board, pid: str) -> tuple[list, list, int]:
    """(outbound, inbound, inside): links that cross the project's edge."""
    mine = {t.id for t in board.tasks if t.project_id == pid}
    by = {t.id: t for t in board.tasks}
    out, inn, inside = [], [], 0
    for t in board.tasks:
        for dep in t.depends_on:
            if t.id in mine and dep in mine:
                inside += 1
            elif t.id in mine and dep in by:
                out.append((t, by[dep]))
            elif dep in mine:
                inn.append((t, by[dep]))
    return out, inn, inside


def do_move(app, pid: str, target: str) -> dict:
    src = app.board
    dst = Board.load(REG.get(target)["path"])
    proj = src.project_by_id(pid)
    mine = [t for t in src.tasks if t.project_id == pid]
    ids = {t.id for t in mine}
    out, inn, inside = crossing(src, pid)
    stamp = TODAY.isoformat()
    for b in (src, dst):                                   # backups first
        shutil.copy2(b.path, b.path.with_name(f"board.json.pre-move-{stamp}"))
    for t in mine:
        t.depends_on = [d for d in t.depends_on if d in ids]
    for t in src.tasks:
        if t.id not in ids:
            t.depends_on = [d for d in t.depends_on if d not in ids]
    src.projects = [p for p in src.projects if p.id != pid]
    src.tasks = [t for t in src.tasks if t.id not in ids]
    dst.projects.append(proj)
    dst.tasks.extend(mine)
    hist = src.path.parent / "history.jsonl"               # the Flow view's lines move too
    if hist.exists():
        keep, moved = [], []
        for line in hist.read_text(encoding="utf-8").splitlines():
            (moved if json.loads(line).get("task") in ids else keep).append(line)
        hist.write_text("".join(x + "\n" for x in keep), encoding="utf-8")
        with (dst.path.parent / "history.jsonl").open("a", encoding="utf-8") as f:
            f.writelines(x + "\n" for x in moved)
    for tid in ids:                                        # and the pasted images
        img = src.image_dir(tid)
        if img.exists():
            dst.image_dir(tid).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(img), str(dst.image_dir(tid)))
    dropped = [{"task": a.title, "waits_on": b.title} for a, b in out + inn]
    for b in (src, dst):
        (b.path.parent / f"move-{stamp}.json").write_text(json.dumps(
            {"project": proj.name, "from": REG.get(app.board_id)["name"],
             "to": REG.get(target)["name"], "tasks": len(mine), "links_kept": inside,
             "links_dropped": dropped}, indent=2), encoding="utf-8")
    dst.save()
    src.save()
    return {"tasks": len(mine), "kept": inside, "dropped": len(dropped)}


class MoveTarget(ModalScreen[str | None]):
    BINDINGS = [Binding("escape", "cancel", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True, show=False),
                Binding("down,j", "move(1)", "", priority=True, show=False),
                Binding("enter", "choose", "", priority=True, show=False)]
    DEFAULT_CSS = """
    MoveTarget { align: center middle; background: #0007; }
    #mt-box { width: 76; max-width: 100%; height: auto; padding: 0 1;
              background: #0d1219; border: round #334154; }
    #mt-rows, #mt-keys { margin: 1 0 0 0; }
    """

    def __init__(self, board: Board, pid: str, here: str):
        super().__init__()
        self.board, self.pid = board, pid
        self.targets = [e for e in REG.active() if e["id"] != here]
        self.cursor = 0

    def compose(self) -> ComposeResult:
        p = self.board.project_by_id(self.pid)
        n = sum(1 for t in self.board.tasks if t.project_id == self.pid)
        with Vertical(id="mt-box"):
            head = Text("Move ", style=f"bold {HEX['bright']}")
            head.append("██ ", style=chex(p.color))
            head.append(p.name, style=f"bold {HEX['bright']}")
            head.append(f"  ({n} tasks)  to which board?", style=HEX["mut"])
            yield Static(head)
            yield Static(id="mt-rows")
            yield Static(Text("↑↓ move · ↵ choose · esc cancel", style=HEX["dim"]),
                         id="mt-keys")

    def on_mount(self) -> None:
        self._paint()

    def _paint(self) -> None:
        t = Text(no_wrap=True)
        for i, e in enumerate(self.targets):
            s = summary(board_of(e["id"], self.app))
            on = i == self.cursor
            if i:
                t.append("\n")
            t.append("▶ " if on else "  ", style=HEX["accent"])
            t.append("██ ", style=chex(e["color"]))
            t.append(fit(e["name"], 24), style=f"bold {HEX['bright']}" if on else HEX["ink"])
            t.append(f"{s['projects']} projects · {s['open']} open", style=HEX["dim"])
        self.query_one("#mt-rows", Static).update(t)

    def action_move(self, d: int) -> None:
        self.cursor = max(0, min(len(self.targets) - 1, self.cursor + d))
        self._paint()

    def action_choose(self) -> None:
        self.dismiss(self.targets[self.cursor]["id"])

    def action_cancel(self) -> None:
        self.dismiss(None)


class MoveConfirm(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "no", "", priority=True),
                Binding("enter", "yes", "", priority=True, show=False)]
    DEFAULT_CSS = """
    MoveConfirm { align: center middle; background: #0007; }
    #mc-box { width: 84; max-width: 100%; height: auto; padding: 0 1;
              background: #0d1219; border: round #f43f5e; }
    """

    def __init__(self, board: Board, pid: str, here: str, target: str):
        super().__init__()
        self.board, self.pid, self.here, self.target = board, pid, here, target

    def compose(self) -> ComposeResult:
        b, p = self.board, self.board.project_by_id(self.pid)
        mine = [t for t in b.tasks if t.project_id == self.pid]
        done = sum(1 for t in mine if not is_open(b, t))
        out, inn, inside = crossing(b, self.pid)
        src, dst = REG.get(self.here), REG.get(self.target)
        pname = {q.id: q.name for q in b.projects}
        t = Text()
        t.append("Move project to another board\n\n", style=f"bold {HEX['bright']}")
        t.append("  ██ ", style=chex(p.color))
        t.append(p.name, style=f"bold {HEX['bright']}")
        t.append("   from ", style=HEX["mut"])
        t.append(f" {src['name']} ", style=f"bold {BG} on {chex(src['color'])}")
        t.append("  to ", style=HEX["mut"])
        t.append(f" {dst['name']} ", style=f"bold {BG} on {chex(dst['color'])}")
        t.append(f"\n\n  {len(mine)} tasks move ({len(mine) - done} open, {done} done) · "
                 f"{inside} links inside the project stay\n", style=HEX["hd"])
        n = len(out) + len(inn)
        if n:
            t.append(f"\n  {n} link{'s' if n > 1 else ''} cross the boards and will be "
                     "dropped:\n", style=f"bold {RED}")
            for waiter, pred in inn + out:
                for task, role in ((waiter, ""), (pred, "waits on ")):
                    t.append("    " + ("✕ " if not role else "    "), style=RED)
                    if role:
                        t.append(role, style=HEX["mut"])
                    t.append(task.title, style=HEX["ink"])
                    where = ("moves" if task.project_id == self.pid
                             else f"{pname.get(task.project_id, 'Inbox')}, stays on {src['name']}")
                    t.append(f"  ({where})\n", style=HEX["dim"])
        t.append(f"\n  Both board files are backed up first (board.json.pre-move-{TODAY}),\n"
                 f"  and the dropped links are listed in move-{TODAY}.json beside each.\n",
                 style=HEX["dim"])
        t.append("\n  ↵ ", style=f"b {HEX['bright']}")
        t.append(f"move{f' and drop {n} links' if n else ''}", style=HEX["mut"])
        t.append("   esc ", style=f"b {HEX['bright']}")
        t.append("cancel", style=HEX["mut"])
        with Vertical(id="mc-box"):
            yield Static(t)

    def action_yes(self) -> None:
        self.dismiss(True)

    def action_no(self) -> None:
        self.dismiss(False)


class MBProjectPicker(ProjectPicker):
    BINDINGS = [Binding("m", "move_board", "Move to board")]

    def compose(self) -> ComposeResult:
        for w in super().compose():
            yield w

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one(".modal-title", Label).update(
            "[b]Projects[/b] — e edit · x archive · d del · "
            "[b #2dd4bf]m move to board[/] · esc")

    def action_move_board(self) -> None:
        p = self._current()
        if p is None:
            return
        here = self.app.board_id
        self.app.push_screen(MoveTarget(self.board, p.id, here),
                             lambda bid, pid=p.id: self._target(pid, here, bid))

    def _target(self, pid, here, bid) -> None:
        if bid:
            self.app.push_screen(MoveConfirm(self.board, pid, here, bid),
                                 lambda ok: self._confirmed(pid, bid, ok))

    def _confirmed(self, pid, bid, ok) -> None:
        if not ok:
            return
        name = self.board.project_by_id(pid).name
        r = do_move(self.app, pid, bid)
        self.app.refresh_view()
        self._reload()
        self.app.notify(f"Moved {name} to {REG.get(bid)['name']} · {r['tasks']} tasks · "
                        f"{r['kept']} links kept · {r['dropped']} dropped",
                        title="Boards", markup=False, timeout=30)


# --------------------------------------------------------------------------
# the app
# --------------------------------------------------------------------------
class MBApp(app_mod.TaskboardApp):
    CSS_PATH = str(Path(app_mod.__file__).parent / "taskboard.tcss")
    # the app sheet's `Screen { background }` outranks a DEFAULT_CSS, so the
    # dimmed backdrop the shipped modals share is restated here at app level
    CSS = "BoardPicker, BoardForm, MoveTarget, MoveConfirm { background: #0007; }"

    def __init__(self, registry: Path, **k):
        global REG, CURRENT_APP
        REG = Registry(registry)
        self.board_id = REG.last
        super().__init__(board_path=REG.get(REG.last)["path"], **k)
        REG.touch(self.board_id)
        CURRENT_APP = self

    def compose(self) -> ComposeResult:
        if VARIANT == "B":
            yield TabStrip(id="tabstrip")
        yield from super().compose()

    def on_mount(self) -> None:
        super().on_mount()
        if VARIANT == "C" and len(REG.active()) > 1:
            self.push_screen(HomeScreen(at_launch=True))

    def check_action(self, action, parameters):
        if isinstance(self.screen, (HomeScreen, AllBoardsAgenda)):
            return action in ("quit",)
        return super().check_action(action, parameters)

    def switch_board(self, bid: str) -> None:
        if bid == self.board_id:
            return
        self.board = Board.load(REG.get(bid)["path"])
        self.board_id = bid
        self.selected_task_id = None
        self.focused_project_id = None
        self.search_query = None
        self._undo_stack = []
        self._gantt_group = self._gantt_previous = None
        self.team_state = None
        REG.touch(bid)
        self._apply_clock_settings()
        self.refresh_view()
        for strip in self.query(TabStrip):
            strip.refresh_strip()

    def action_boards(self) -> None:
        self.push_screen(HomeScreen() if VARIANT == "C" else BoardPicker())

    def action_board_cycle(self, d: int) -> None:
        ids = [e["id"] for e in REG.active()]
        self.switch_board(ids[(ids.index(self.board_id) + d) % len(ids)])

    def action_all_boards(self) -> None:
        self.push_screen(AllBoardsAgenda())

    def action_manage_projects(self) -> None:
        self.push_screen(MBProjectPicker(self.board))


def make_app(variant: str, registry: Path, root: Path) -> MBApp:
    """Bind the variant's keys, then build the app (BINDINGS are read per class)."""
    global VARIANT, ROOT
    VARIANT, ROOT = variant, root
    patch_keymap()
    cls = type(f"MBApp{variant}", (MBApp,), {"BINDINGS": km.app_bindings()})
    return cls(registry)


if __name__ == "__main__":
    import sys
    import tempfile
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fixture
    root = Path(tempfile.mkdtemp())
    make_app(sys.argv[1] if len(sys.argv) > 1 else "A", fixture.build(root), root).run()

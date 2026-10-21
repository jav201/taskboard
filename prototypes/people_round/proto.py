"""THROWAWAY prototype — the people round: a directory of people and roles,
`@` mentions in the notes, a view per person, search by person.

    unset NO_COLOR; PYTHONUTF8=1 python prototypes/people_round/proto.py list
    unset NO_COLOR; PYTHONUTF8=1 python prototypes/people_round/proto.py shot [SCENE ...]
    python prototypes/people_round/proto.py live SCENE [SECONDS]      (a real terminal)

Sub-shape A: the REAL `TaskboardApp` (subclassed here), on a real registry in a
temporary folder (fixture.py), driven by real key presses (`App._press_keys`,
the pilot's own path) — headless for the SVGs, in a real Windows Terminal for
the PNGs (shoot.ps1). Each variant is a new screen or a subclass of the shipped
one it changes, patched into the app's modules for that scene only. Nothing
under `taskboard/` is edited; nothing writes outside the temporary folder (the
"+ add" path adds the person in memory only).
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
import unicodedata
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
from textual.containers import Vertical  # noqa: E402
from textual.screen import ModalScreen, Screen  # noqa: E402
from textual.widgets import Button, Input, Label, Static, TextArea  # noqa: E402

from taskboard import app as app_mod, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry, peek_board  # noqa: E402
from taskboard.keymap import key_line  # noqa: E402
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

RED, SOON, PINK = HEX["over"], HEX["soon"], HEX["pink"]
HEX["mchip"] = f"b #0d1117 on {PINK}"          # variant B's chip, as a palette key for `c()`
NBSP = " "
WEEK_END = TODAY + timedelta(days=6 - TODAY.weekday())       # Sunday

# =============================================================================
# the directory and the mention tokeniser
# =============================================================================
DIR: dict[str, dict] = {}            # handle -> {"id","name","role","note"}; loaded per app
STYLE: list[str | None] = [None]     # how a mention is drawn: None (today), "A", "B", "C"

MENTION_RE = re.compile(r"(?<![\w.@])@(?:\[([^\]]+)\]\(p:([\w.\-]+)\)|([a-z0-9]+(?:[._\-][a-z0-9]+)*))")


def mention_ids(notes: str) -> list[str]:
    out = []
    for m in MENTION_RE.finditer(notes or ""):
        h = m.group(2) or m.group(3)
        if h not in out:
            out.append(h)
    return out


def split_mentions(text: str) -> list[tuple[str, str | None]]:
    out, last = [], 0
    for m in MENTION_RE.finditer(text):
        if m.start() > last:
            out.append((text[last:m.start()], None))
        out.append((m.group(0), m.group(2) or m.group(3)))
        last = m.end()
    if last < len(text):
        out.append((text[last:], None))
    return out


def name_of(handle: str) -> str | None:
    p = DIR.get(handle)
    return p["name"] if p else None


def fold(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", s.lower())
                   if not unicodedata.combining(ch))


def handle_for(name: str) -> str:
    base = ".".join(fold(name).split()) or "person"
    base = re.sub(r"[^a-z0-9.]", "", base)
    h, n = base, 2
    while h in DIR:
        h, n = f"{base}{n}", n + 1
    return h


def find_people(q: str) -> list[dict]:
    """Name matches first (a word starting with q, then anywhere), then role matches."""
    q = fold(q)
    people = sorted(DIR.values(), key=lambda p: fold(p["name"]))
    if not q:
        return people
    start = [p for p in people if any(w.startswith(q) for w in fold(p["name"]).split())]
    inside = [p for p in people if q in fold(p["name"]) and p not in start]
    role = [p for p in people if q in fold(p["role"]) and p not in start and p not in inside]
    return start + inside + role


def mention_text(handle: str, raw: str) -> Text:
    name = name_of(handle)
    if name is None:
        return Text(raw, style=HEX["dim"])
    if STYLE[0] == "A":
        return Text("@" + name, style=f"b {PINK}")
    if STYLE[0] == "B":
        return Text(f" {name} ", style=f"b #0d1117 on {PINK}")
    return Text(name, style=f"underline {HEX['ink']}")


def notes_preview_m(text: str) -> Text:
    """`modals.notes_preview` with mentions drawn (the board's highlight first, then
    each mention inside its segment, so a highlight around a mention survives)."""
    out = Text()
    if STYLE[0] == "C":
        hs = [h for h in mention_ids(text) if h in DIR]
        if hs:
            out.append("with  ", style=HEX["dim"])
            for i, h in enumerate(hs):
                if i:
                    out.append(" · ", style=HEX["dim"])
                out.append(DIR[h]["name"], style=f"b {HEX['ink']}")
                out.append(f" {DIR[h]['role']}", style=HEX["mut"])
            out.append("\n\n")
    for i, ln in enumerate(text.split("\n")):
        if i:
            out.append("\n")
        if not ln.strip():
            continue
        for segment, tone in views.highlight_segments(ln):
            for piece, h in split_mentions(segment):
                if h is None or STYLE[0] is None:
                    out.append(piece, HEX[tone])
                else:
                    out.append_text(mention_text(h, piece))
    return out


_ORIG_CARD_META = views._card_meta


def card_meta_m(task, board, today, marks, tag):
    toks = _ORIG_CARD_META(task, board, today, marks, tag)
    hs = [h for h in mention_ids(task.notes) if h in DIR]
    if not hs or STYLE[0] == "C":
        return toks
    first = DIR[hs[0]]["name"].split()[0]
    more = f"+{len(hs) - 1}" if len(hs) > 1 else ""
    tok = (f"@{first}{more}", "pink") if STYLE[0] == "A" else (f"{first}{more} ", "mchip")
    return toks[:-1] + [tok] + toks[-1:] if toks else [tok]


_ORIG_NOTE_LINES = views.present_note_lines
_ORIG_NOTE_MARKUP = views._present_note_markup


def _plain_mentions(text: str) -> str:
    def rep(m):
        h = m.group(2) or m.group(3)
        name = name_of(h)
        if name is None:
            return m.group(0)
        name = name.replace(" ", NBSP)
        return ("@" + name) if STYLE[0] == "A" else (f"{NBSP}{name}{NBSP}" if STYLE[0] == "B"
                                                     else name)
    return MENTION_RE.sub(rep, text or "")


def present_note_lines_m(notes: str, w: int):
    return _ORIG_NOTE_LINES(_plain_mentions(notes), w)


def present_note_markup_m(row, w):
    lead, txt = row
    if STYLE[0] not in ("A", "B"):
        return _ORIG_NOTE_MARKUP(row, w)
    txt = views.clip(txt, w - views.vis(lead))
    names = [p["name"].replace(" ", NBSP) for p in DIR.values()]
    pat = "|".join(re.escape(("@" if STYLE[0] == "A" else NBSP) + n + ("" if STYLE[0] == "A" else NBSP))
                   for n in names)
    parts, last = [], 0
    for m in re.finditer(pat, txt) if pat else []:
        parts.append(views.c(views.escape(txt[last:m.start()]), "ink"))
        parts.append(views.c(views.escape(m.group(0)), "pink" if STYLE[0] == "A" else "mchip",
                             bold=STYLE[0] == "A"))
        last = m.end()
    parts.append(views.c(views.escape(txt[last:]), "ink"))
    return views._pad(views.c(views.escape(lead), "mut") + "".join(parts), w)


# =============================================================================
# a person's work across every board
# =============================================================================
class PItem(NamedTuple):
    band: str
    entry: object
    task: object
    due: date | None
    project: str
    board: object


BANDS = ("late", "today", "week", "later", "nodate")
BAND_HEAD = {"late": ("LATE", RED), "today": ("TODAY", SOON),
             "week": (f"THIS WEEK · to Sun {WEEK_END.day}", HEX["hd"]),
             "later": ("LATER", HEX["hd"]), "nodate": ("NO DATE", HEX["mut"])}


def read_boards(app) -> list:
    out = []
    for e in app.registry.active():
        b = app.board if e.id == app.board_id else peek_board(e.path)
        out.append((e, b))
    return out


def person_items(boards, handle: str) -> list[PItem]:
    out = []
    for e, b in boards:
        names = {p.id: p.name for p in b.projects}
        for t in b.tasks:
            if t.archived or not is_open(b, t) or handle not in mention_ids(t.notes):
                continue
            d = parse_iso(t.due_date)
            band = ("nodate" if d is None else "late" if d < TODAY else "today" if d == TODAY
                    else "week" if d <= WEEK_END else "later")
            out.append(PItem(band, e, t, d, names.get(t.project_id, ""), b))
    out.sort(key=lambda x: (BANDS.index(x.band), x.due or date.max, x.entry.name))
    return out


def counts(items) -> tuple[int, int, int]:
    return (sum(x.band == "late" for x in items), sum(x.band == "today" for x in items),
            len(items))


def when(d: date | None) -> tuple[str, str]:
    if d is None:
        return "—", HEX["dim"]
    if d < TODAY:
        return f"▲{(TODAY - d).days}d", RED
    if d == TODAY:
        return "today", SOON
    return f"{d:%a} {d.day}", HEX["hd"]


def chip(name: str, colour: str, w: int) -> Text:
    return Text(fit(f" {name}", w), style=f"b #0d1117 on {board_hex(colour)}")


def row(*parts, w: int) -> Text:
    t = Text(no_wrap=True)
    for p in parts:
        if isinstance(p, Text):
            t.append_text(p)
        else:
            t.append(*p) if isinstance(p, tuple) else t.append(p)
    t.truncate(w, pad=True)
    return t


def mention_line(task, handle: str) -> str:
    """The note line that names the person: the meeting's context."""
    for ln in (task.notes or "").splitlines():
        if handle in mention_ids(ln):
            return ln.strip().lstrip("-* ").strip()
    return ""


def jump(app, it: PItem) -> None:
    while len(app.screen_stack) > 1:
        app.pop_screen()
    if it.entry.id != app.board_id:
        app.switch_board(it.entry.id)
    app.jump_to(it.task.id)
    app.call_after_refresh(lambda: app.screen.refresh(repaint=True, layout=True))


class PeopleBase(Screen[None]):
    """The `@` people view. Read-only; every board read once, when it opens."""
    BINDINGS = [Binding("escape,at", "back", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True),
                Binding("down,j", "move(1)", "", priority=True),
                Binding("left,h", "side(-1)", "", priority=True),
                Binding("right,l", "side(1)", "", priority=True),
                Binding("tab", "pane", "", priority=True),
                Binding("enter", "jump", "", priority=True)]
    DEFAULT_CSS = """
    PeopleBase { background: #0d1117; overflow-y: hidden; }
    #pv-body { padding: 0 1; height: 1fr; }
    #pv-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }
    """
    KEYS: list = []

    def __init__(self, start: str | None = None) -> None:
        super().__init__()
        self.start = start

    def compose(self):
        yield Static(id="pv-body")
        yield Static(id="pv-keys")

    def on_mount(self) -> None:
        boards = read_boards(self.app)
        self.items = {h: person_items(boards, h) for h in DIR}
        # who needs me most first: late, then today, then open, then the name
        self.people = sorted(DIR.values(), key=lambda p: (
            -counts(self.items[p["id"]])[0], -counts(self.items[p["id"]])[1],
            -counts(self.items[p["id"]])[2], fold(p["name"])))
        self.p = next((i for i, p in enumerate(self.people) if p["id"] == self.start), 0)
        self.r, self.pane = 0, "people"
        self._paint()

    def on_resize(self, _e) -> None:
        self._paint()

    def cur(self) -> dict:
        return self.people[self.p]

    def tasks(self) -> list[PItem]:
        return self.items[self.cur()["id"]]

    def _paint(self) -> None:
        w, h = self.app.size
        self.query_one("#pv-body", Static).update(self.body(w - 2, h - 1))
        self.query_one("#pv-keys", Static).update(key_line(self.KEYS, w - 2))

    def head(self, inner: int, sub: str) -> Text:
        t = Text(no_wrap=True)
        t.append("◆ PEOPLE", style=f"bold {HEX['bright']}")
        t.append(f"  {sub}", style=HEX["mut"])
        right = f"{len(DIR)} in the directory · every board · read-only"
        if t.cell_len + len(right) + 1 > inner:
            right = f"{len(DIR)} people · read-only"
        t.append(" " * max(1, inner - t.cell_len - len(right)))
        t.append(right, style=HEX["dim"])
        t.truncate(inner)
        return t

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_pane(self) -> None:
        pass

    def action_move(self, d: int) -> None:
        pass

    def action_side(self, d: int) -> None:
        pass

    def action_jump(self) -> None:
        ts = self.tasks()
        if ts:
            jump(self.app, ts[min(self.r, len(ts) - 1)])


def count_text(late: int, today: int, open_: int) -> Text:
    t = Text(no_wrap=True)
    t.append(f"▲{late}" if late else "  ", style=f"b {RED}")
    t.append(" ")
    t.append(f"●{today}" if today else "  ", style=f"b {SOON}")
    t.append(" ")
    t.append(f"{open_:>2}", style=HEX["hd"])
    return t


def task_rows(items: list[PItem], sel: int | None, w: int, chip_w: int, show_proj: bool,
              handle: str | None = None, context: bool = False) -> tuple[list[Text], int]:
    """Banded task rows: a band head, then one row per task (two with `context`)."""
    rows, band, cur_row = [], None, 0
    pw = 18 if show_proj else 0
    for i, it in enumerate(items):
        if it.band != band:
            band = it.band
            lab, col = BAND_HEAD[band]
            if rows:
                rows.append(Text())
            rows.append(row((lab, f"b {col}"), (" " + "─" * w, HEX["frame"]), w=w))
        on = sel == i
        lab, col = when(it.due)
        tw = w - 2 - chip_w - 1 - (pw + 1 if pw else 0) - 8
        if on:
            cur_row = len(rows)
        r = row(("▶ " if on else "  ", HEX["accent"]), chip(it.entry.name, it.entry.color, chip_w), " ",
                (fit(it.task.title, tw), f"b {HEX['bright']}" if on else HEX["ink"]),
                *([(" " + fit(it.project, pw), HEX["dim"])] if pw else []),
                (f"{lab:>8}", col), w=w)
        if on:                      # the cursor's band, around the board chip (it keeps its hue)
            r.stylize("on #16202c", 0, 2)
            r.stylize("on #16202c", 2 + chip_w)
        rows.append(r)
        if context and handle:
            ctx = mention_line(it.task, handle)
            line = Text(" " * (4 + chip_w), no_wrap=True)
            line.append("“", style=HEX["dim"])
            line.append_text(notes_preview_m(ctx))
            line.append("”", style=HEX["dim"])
            line.truncate(w, pad=True)
            line.stylize(HEX["mut"], 0, 4 + chip_w)
            rows.append(line)
    if not items:
        rows.append(Text("  nothing open with this person", style=HEX["mut"]))
    return rows, cur_row


class PeoplePanes(PeopleBase):
    """A · two panes: the directory on the left, the chosen person's work on the right."""
    KEYS = [("↑↓", "move"), ("⇥", "people ↔ tasks"), ("↵", "open on its board"),
            ("/", "find a name"), ("n", "new person"), ("e", "edit"), ("esc", "back")]

    def body(self, inner: int, h: int) -> Text:
        lw = 32 if inner >= 100 else 24
        rw = inner - lw - 3
        left: list[Text] = []
        for i, p in enumerate(self.people):
            on = i == self.p
            late, today, n = counts(self.items[p["id"]])
            ct = count_text(late, today, n)
            nm = row(("▶ " if on else "  ", HEX["accent"]),
                     (fit(p["name"], lw - 2 - ct.cell_len - 1),
                      f"b {HEX['bright']}" if on else HEX["ink"]), " ", ct, w=lw)
            rl = row(("  " + fit(p["role"], lw - 2), HEX["dim"]), w=lw)
            if on:
                bg = "on #16202c" if self.pane == "people" else "on #121a24"
                nm.stylize(bg)
                rl.stylize(bg)
            left += [nm, rl]
        per = self.cur()
        right = [row((per["name"], f"b {PINK}"), ("  " + per["role"], HEX["hd"]), w=rw)]
        right.append(row((per["note"] or "no note", HEX["mut"] if per["note"] else HEX["dim"]), w=rw))
        right.append(Text())
        trs, cur_row = task_rows(self.tasks(), self.r if self.pane == "tasks" else None, rw,
                                 10 if rw >= 70 else 9, rw >= 78)
        right += trs
        body_h = h - 2
        n = max(len(left), len(right), body_h)
        out = [self.head(inner, "who do I owe what · every board"), Text()]
        for y in range(min(n, body_h)):
            lft = left[y] if y < len(left) else Text(" " * lw)
            rgt = right[y] if y < len(right) else Text()
            out.append(Text.assemble(lft, (" │ ", HEX["frame"]), rgt))
        return Text("\n").join(out)

    def action_pane(self) -> None:
        self.pane = "tasks" if self.pane == "people" else "people"
        self.r = 0
        self._paint()

    def action_move(self, d: int) -> None:
        if self.pane == "people":
            self.p = max(0, min(len(self.people) - 1, self.p + d))
            self.r = 0
        else:
            self.r = max(0, min(len(self.tasks()) - 1, self.r + d))
        self._paint()

    def action_side(self, d: int) -> None:
        self.action_pane()


class PeopleCards(PeopleBase):
    """B · a card per person, the counts drawn as bars; `↵` opens the person (C's page)."""
    KEYS = [("←→↑↓", "move"), ("↵", "their tasks"), ("/", "find a name"), ("n", "new person"),
            ("esc", "back")]

    def body(self, inner: int, h: int) -> Text:
        ncol = 3 if inner >= 100 else 2
        cw = (inner - (ncol - 1) * 2) // ncol
        cards = []
        for i, p in enumerate(self.people):
            items = self.items[p["id"]]
            late, today, n = counts(items)
            on = i == self.p
            fr = HEX["accent"] if on else HEX["frame"]
            title = f" {p['name']} "
            top = row(("╭─", fr), (title, f"b {PINK}" if on else f"b {HEX['ink']}"),
                      ("─" * (cw - 3 - len(title)) + "╮", fr), w=cw)
            def side(content: Text) -> Text:
                t = Text("│ ", style=fr)
                content.truncate(cw - 4, pad=True)
                t.append_text(content)
                t.append(" │", style=fr)
                return t
            rl = side(Text(p["role"], style=HEX["mut"]))
            bar = Text(no_wrap=True)
            bar.append("█" * late, style=RED)
            bar.append("█" * today, style=SOON)
            bar.append("█" * (n - late - today), style=HEX["later"])
            bar.append("  ")
            if n:
                bar.append(f"{late} late" if late else "", style=f"b {RED}")
                bar.append(" · " if late and today else "", style=HEX["dim"])
                bar.append(f"{today} today" if today else "", style=f"b {SOON}")
                bar.append(" · " if late or today else "", style=HEX["dim"])
                bar.append(f"{n} open", style=HEX["hd"])
            else:
                bar.append("nothing open", style=HEX["dim"])
            nxt = Text(no_wrap=True)
            if items:
                lab, col = when(items[0].due)
                nxt.append("next ", style=HEX["dim"])
                nxt.append(items[0].task.title, style=HEX["ink"])
                nxt.append(f" · {lab}", style=col)
            bot = Text("╰" + "─" * (cw - 2) + "╯", style=fr)
            cards.append([top, rl, side(bar), side(nxt), bot])
        out = [self.head(inner, "a card per person · most urgent first"), Text()]
        for r0 in range(0, len(cards), ncol):
            group = cards[r0:r0 + ncol]
            for y in range(5):
                parts = []
                for j, cd in enumerate(group):
                    if j:
                        parts.append(Text("  "))
                    parts.append(cd[y])
                out.append(Text.assemble(*parts))
        top = 0
        sel_line = 2 + (self.p // ncol) * 5
        if sel_line + 5 > h:
            top = sel_line + 5 - h
        return Text("\n").join(out[:2] + out[2 + top:2 + top + h - 2])

    def action_move(self, d: int) -> None:
        ncol = 3 if self.app.size.width - 2 >= 100 else 2
        self.p = max(0, min(len(self.people) - 1, self.p + d * ncol))
        self._paint()

    def action_side(self, d: int) -> None:
        self.p = max(0, min(len(self.people) - 1, self.p + d))
        self._paint()

    def action_jump(self) -> None:
        self.app.push_screen(PersonPage(self.cur()["id"]))


class PersonPage(PeopleBase):
    """C · one person per page: their open tasks by urgency, each with the note line
    that names them (what I wrote about them); `←→` the next person."""
    KEYS = [("←→", "person"), ("↑↓", "task"), ("↵", "open on its board"), ("/", "find a name"),
            ("e", "edit person"), ("esc", "back")]

    def on_mount(self) -> None:
        super().on_mount()
        self.pane = "tasks"
        self._paint()

    def body(self, inner: int, h: int) -> Text:
        per = self.cur()
        late, today, n = counts(self.tasks())
        t = Text(no_wrap=True)
        t.append("◀ ", style=HEX["accent"])
        t.append(per["name"].upper(), style=f"b {PINK}")
        t.append(" ▶", style=HEX["accent"])
        t.append(f"   {per['role']}", style=HEX["hd"])
        right = Text()
        right.append(f"▲{late} late  " if late else "", style=f"b {RED}")
        right.append(f"●{today} today  " if today else "", style=f"b {SOON}")
        right.append(f"{n} open · {self.p + 1} of {len(self.people)}", style=HEX["mut"])
        t.append(" " * max(1, inner - t.cell_len - right.cell_len))
        t.append_text(right)
        t.truncate(inner)
        out = [t, row((per["note"] or "no note", HEX["mut"] if per["note"] else HEX["dim"]), w=inner),
               Text("─" * inner, style=HEX["frame"])]
        trs, cur_row = task_rows(self.tasks(), self.r, inner, 11 if inner >= 100 else 9,
                                 inner >= 100, handle=per["id"], context=True)
        room = h - len(out)
        top = max(0, min(cur_row - room + 3, len(trs) - room))
        return Text("\n").join(out + trs[top:top + room])

    def action_side(self, d: int) -> None:
        self.p = (self.p + d) % len(self.people)
        self.r = 0
        self._paint()

    def action_move(self, d: int) -> None:
        self.r = max(0, min(len(self.tasks()) - 1, self.r + d))
        self._paint()


# =============================================================================
# ITEM 2 — the `@` picker in the task editor's notes
# =============================================================================
def pick_rows(q: str, sel: int, w: int, limit: int) -> tuple[list[Text], list]:
    """The picker's rows: people matching `q`, then `+ add 'Q'` when no name equals it."""
    found = find_people(q)[:limit]
    opts: list = [("p", p) for p in found]
    if q and not any(fold(p["name"]) == fold(q) for p in DIR.values()):
        opts.append(("add", q))
    rows = []
    for i, (kind, v) in enumerate(opts):
        on = i == sel
        if kind == "p":
            r = row(("▶ " if on else "  ", HEX["accent"]),
                    (fit(v["name"], 14), f"b {PINK}" if on else f"b {HEX['ink']}"), " ",
                    (fit(v["role"], w - 19), HEX["mut"]), w=w)
        else:
            r = row(("▶ " if on else "  ", HEX["accent"]), ("+ add ", f"b {HEX['green']}"),
                    (f"'{v}'", f"b {HEX['ink']}"), ("  new person", HEX["dim"]), w=w)
        if on:
            r.stylize("on #1c2533")
        rows.append(r)
    if not opts:
        rows.append(row(("  type a name", HEX["dim"]), w=w))
    return rows, opts


class MentionDrop(Vertical):
    DEFAULT_CSS = f"""
    MentionDrop {{ overlay: screen; position: absolute; width: 46; height: auto;
                   background: #111827; border: round {PINK}; padding: 0 1; display: none; }}
    MentionDrop #md-head {{ height: 1; }}
    MentionDrop #md-list {{ height: auto; }}
    MentionDrop Input {{ display: none; height: 3; border: tall #334154; }}
    MentionDrop #md-keys {{ height: 1; }}
    """

    def compose(self):
        yield Static(id="md-head")
        yield Static(id="md-list")
        yield Input(placeholder="full name", id="md-name")
        yield Input(placeholder="role, e.g. Legal counsel", id="md-role")
        yield Static(id="md-keys")


AT_RE = re.compile(r"(?:^|(?<=\s))@([^\s@]*)$")


class EditorBase(modals.TaskModal):
    def notes(self) -> TextArea:
        return self.query_one("#f-notes", TextArea)

    def insert_mention(self, start_col: int, handle: str) -> None:
        ta = self.notes()
        row_, col = ta.cursor_location
        ta.replace(f"@{handle} ", (row_, start_col), (row_, col))
        ta.focus()

    def add_person(self, name: str, role: str) -> str:
        h = handle_for(name)
        DIR[h] = {"id": h, "name": name, "role": role, "note": ""}
        return h


class EditorInline(EditorBase):
    """A · a dropdown under the cursor, filtering as you type."""
    BINDINGS = [Binding("up", "drop_move(-1)", "", priority=True),
                Binding("down", "drop_move(1)", "", priority=True),
                Binding("enter", "drop_pick", "", priority=True),
                Binding("escape", "drop_close", "", priority=True)]

    def compose(self):
        yield from super().compose()
        yield MentionDrop(id="mdrop")

    def on_mount(self) -> None:
        super().on_mount()
        self.mode, self.q, self.sel, self.opts, self.at = None, "", 0, [], 0

    def check_action(self, action, parameters):
        if action in ("drop_move", "drop_pick", "drop_close"):
            return self.mode is not None
        return super().check_action(action, parameters)

    def on_text_area_changed(self, event) -> None:
        super().on_text_area_changed(event)
        if event.text_area.id == "f-notes" and self.mode != "role":
            self.call_after_refresh(self._scan)

    def _scan(self) -> None:
        ta = self.notes()
        r, col = ta.cursor_location
        m = AT_RE.search(ta.document.get_line(r)[:col])
        if not m:
            self._close()
            return
        self.mode, self.q, self.at = "list", m.group(1), m.start()
        self.sel = min(self.sel, 99)
        self._draw()

    def _draw(self) -> None:
        drop = self.query_one("#mdrop", MentionDrop)
        ta = self.notes()
        w = 44
        if self.mode == "list":
            rows, self.opts = pick_rows(self.q, self.sel, w, 5)
            self.sel = min(self.sel, max(0, len(self.opts) - 1))
            rows, self.opts = pick_rows(self.q, self.sel, w, 5)
            drop.query_one("#md-head", Static).update(
                row(("@", f"b {PINK}"), (self.q or "", f"b {HEX['ink']}"), ("▌", HEX["accent"]),
                    ("   mention a person", HEX["dim"]), w=w))
            drop.query_one("#md-list", Static).update(Text("\n").join(rows))
            drop.query_one("#md-list", Static).display = True
            drop.query_one("#md-role", Input).display = False
            drop.query_one("#md-name", Input).display = False
            drop.query_one("#md-keys", Static).update(
                key_line([("↑↓", ""), ("↵", "pick"), ("esc", "plain text")], w))
        else:
            drop.query_one("#md-head", Static).update(
                row(("New person", f"b {HEX['green']}"), ("  · for every board", HEX["dim"]), w=w))
            drop.query_one("#md-list", Static).display = False
            drop.query_one("#md-name", Input).display = True
            drop.query_one("#md-role", Input).display = True
            drop.query_one("#md-keys", Static).update(
                key_line([("↵", "add + mention"), ("⇥", "name / role"), ("esc", "back")], w))
        drop.display = True
        off = ta.cursor_screen_offset
        sw, sh = self.app.size
        x = max(0, min(off.x - len(self.q) - 1, sw - 48))
        y = off.y + 1
        if y + 10 > sh:
            y = max(0, off.y - 10)
        drop.styles.offset = (x, y)

    def _close(self) -> None:
        self.mode = None
        self.query_one("#mdrop", MentionDrop).display = False

    def action_drop_move(self, d: int) -> None:
        self.sel = max(0, min(len(self.opts) - 1, self.sel + d))
        self._draw()

    def action_drop_pick(self) -> None:
        if self.mode == "role":
            role = self.query_one("#md-role", Input).value.strip()
            name = self.query_one("#md-name", Input).value.strip() or self.q
            h = self.add_person(name, role)
            self._close()
            self.insert_mention(self.at, h)
            return
        if not self.opts:
            return
        kind, v = self.opts[self.sel]
        if kind == "p":
            self._close()
            self.insert_mention(self.at, v["id"])
        else:
            self.mode = "role"
            self.query_one("#md-name", Input).value = v
            self._draw()
            self.query_one("#md-role", Input).focus()

    def action_drop_close(self) -> None:
        if self.mode == "role":
            self.mode = "list"
            self._draw()
            self.notes().focus()
        else:
            self._close()


class PersonPicker(modals.ButtonKeysMixin, ModalScreen[str | None]):
    """B · a small centred window: a filter field, the matches, `+ add` with its role."""
    BINDINGS = [Binding("escape", "cancel", "", priority=True),
                Binding("up", "move(-1)", "", priority=True),
                Binding("down", "move(1)", "", priority=True),
                Binding("alt+a", "press_button('add')", "", priority=True),
                Binding("alt+s", "press_button('ok')", "", priority=True)]
    DEFAULT_CSS = f"""
    PersonPicker {{ align: center middle; }}
    #pp-box {{ width: 56; height: auto; max-height: 22; background: #111827;
               border: round {PINK}; padding: 0 1; }}
    #pp-q, #pp-role {{ border: tall #334154; height: 3; }}
    #pp-role {{ display: none; }}
    #pp-list {{ height: auto; }}
    #pp-buttons {{ height: 3; }}
    #pp-buttons Button {{ width: auto; min-width: 10; margin-right: 1; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self.sel, self.opts, self.adding = 0, [], False

    def compose(self):
        from textual.containers import Horizontal
        with Vertical(id="pp-box"):
            yield Label(Text("Mention a person", style=f"b {PINK}"))
            yield Input(placeholder="name or role", id="pp-q")
            yield Static(id="pp-list")
            yield Input(placeholder="role, e.g. Legal counsel", id="pp-role")
            with Horizontal(id="pp-buttons"):
                yield Button("Mention", variant="success", id="ok")
                yield Button("Add person", variant="primary", id="add")
                yield Button("Cancel", variant="default", id="cancel")
            yield Static(id="pp-keys")

    def on_mount(self) -> None:
        self.query_one("#pp-q", Input).focus()
        self._draw()

    def on_input_changed(self, event) -> None:
        if event.input.id == "pp-q":
            self.sel = 0
            self._draw()

    def on_input_submitted(self, event) -> None:
        self.query_one("#ok", Button).press()

    def _draw(self) -> None:
        q = self.query_one("#pp-q", Input).value.strip()
        rows, self.opts = pick_rows(q, self.sel, 52, 6)
        if self.adding:
            rows = [row(("New person  ", f"b {HEX['green']}"), (q, f"b {HEX['ink']}"),
                        ("  · its role below · every board", HEX["dim"]), w=52)]
        self.query_one("#pp-list", Static).update(Text("\n").join(rows))
        self.query_one("#pp-role", Input).display = self.adding
        self.query_one("#ok", Button).label = "Add" if self.adding else "Mention"
        self.query_one("#cancel", Button).label = "Back" if self.adding else "Cancel"
        self.query_one("#add", Button).display = not self.adding and bool(q)
        keys = ([("↵ / alt+s", "add + mention"), ("esc", "back")] if self.adding else
                [("↑↓", ""), ("↵ / alt+s", "mention"), *([("alt+a", f"add '{q}'")] if q else []),
                 ("esc", "cancel")])
        self.query_one("#pp-keys", Static).update(key_line(keys, 52))

    def action_move(self, d: int) -> None:
        self.sel = max(0, min(len(self.opts) - 1, self.sel + d))
        self._draw()

    def on_button_pressed(self, event) -> None:
        bid = event.button.id
        q = self.query_one("#pp-q", Input).value.strip()
        if bid == "cancel":
            self.action_cancel()
        elif bid == "add":
            self.adding = True
            self._draw()
            self.query_one("#pp-role", Input).focus()
        elif self.adding:
            h = handle_for(q)
            DIR[h] = {"id": h, "name": q, "role": self.query_one("#pp-role", Input).value.strip(),
                      "note": ""}
            self.dismiss(h)
        elif self.opts:
            kind, v = self.opts[self.sel]
            if kind == "p":
                self.dismiss(v["id"])
            else:
                self.query_one("#add", Button).press()

    def action_cancel(self) -> None:
        if self.adding:
            self.adding = False
            self._draw()
            self.query_one("#pp-q", Input).focus()
        else:
            self.dismiss(None)


class EditorModal(EditorBase):
    """B · `@` typed at a word start opens the centred picker."""

    def on_text_area_changed(self, event) -> None:
        super().on_text_area_changed(event)
        if event.text_area.id != "f-notes" or getattr(self, "_picking", False):
            return
        ta = self.notes()
        r, col = ta.cursor_location
        before = ta.document.get_line(r)[:col]
        if before.endswith("@") and (len(before) == 1 or before[-2].isspace()):
            self._picking = True
            self.app.push_screen(PersonPicker(), lambda h, c=col - 1: self._picked(c, h))

    def _picked(self, col: int, handle: str | None) -> None:
        self._picking = False
        if handle:
            self.insert_mention(col, handle)
        else:
            self.notes().focus()


# =============================================================================
# ITEM 3 — search by person
# =============================================================================
_ORIG_MATCHES = views.matches
_ORIG_FILTER_BAR = views.filter_bar
SEARCH: list[str | None] = [None]


def matches_m(task, board, q):
    if q.startswith("@"):
        return "person" if q[1:] in mention_ids(task.notes) else None
    hit = _ORIG_MATCHES(task, board, q)
    if hit or SEARCH[0] != "C":
        return hit
    for h in mention_ids(task.notes):
        p = DIR.get(h)
        if p and (q in fold(p["name"]) or q in fold(p["role"])):
            return "person"
    return None


def filter_bar_m(query, hits, total, w):
    if not query.startswith("@") or query[1:] not in DIR:
        return _ORIG_FILTER_BAR(query, hits, total, w)
    p = DIR[query[1:]]
    left = (views.c("/", "accent", bold=True) + " " + views.c(views.escape(f"@{p['name']}"), "pink", bold=True)
            + views.c(views.escape(f"  {p['role']} · tasks that mention them"), "mut"))
    right = views.c(f"{hits}/{total} tasks", "mut") + views.c(" · esc clears", "dim")
    return [views.header(left, right, w), views.head_rule(w)]


class SearchAt(modals.TextPrompt):
    """A · one field: text filters tasks as today; `@` starts a person — the list
    shows names only, `↵` filters to their tasks, `alt+p` opens their page."""
    BINDINGS = [Binding("up", "move(-1)", "", priority=True),
                Binding("down", "move(1)", "", priority=True),
                Binding("alt+p", "page", "", priority=True)]
    DEFAULT_CSS = "#sp-list { height: auto; margin: 0 0 1 0; }"

    def on_mount(self) -> None:
        super().on_mount()
        self.sel, self.opts = 0, []
        self.query_one("#modal-box").mount(Static(id="sp-list"), after="#f-text")
        self.call_after_refresh(self._draw)

    def check_action(self, action, parameters):
        if action in ("move", "page"):
            return self.query_one("#f-text", Input).value.startswith("@")
        return super().check_action(action, parameters)

    def on_input_changed(self, event) -> None:
        self.sel = 0
        self._draw()

    def _draw(self) -> None:
        v = self.query_one("#f-text", Input).value
        lst = self.query_one("#sp-list", Static)
        keys = self.query(".modal-keys")
        if v.startswith("@"):
            rows, self.opts = pick_rows(v[1:], self.sel, 52, 6)
            self.opts = [o for o in self.opts if o[0] == "p"]
            rows = rows[:len(self.opts)] or [row(("  no one by that name", HEX["dim"]), w=52)]
            lst.update(Text("\n").join([row(("PEOPLE · names only", f"b {PINK}"), w=52)] + rows))
            lst.display = True
            if keys:
                keys.first().update(key_line([("↑↓", ""), ("↵", "their tasks"), ("alt+p", "their page"),
                                              ("esc", "cancel")], 54))
        else:
            lst.update(row(("text filters tasks · ", HEX["dim"]), ("@", f"b {PINK}"),
                           (" starts a person", HEX["dim"]), w=52))
            if keys:
                keys.first().update(key_line([("↵ / alt+s", "filter"), ("esc", "cancel")], 54))

    def action_move(self, d: int) -> None:
        self.sel = max(0, min(len(self.opts) - 1, self.sel + d))
        self._draw()

    def _save(self) -> None:
        v = self.query_one("#f-text", Input).value
        if v.startswith("@") and self.opts:
            self.dismiss("@" + self.opts[self.sel][1]["id"])
        else:
            super()._save()

    def action_page(self) -> None:
        if self.opts:
            h = self.opts[self.sel][1]["id"]
            self.dismiss(None)
            self.app.push_screen(PeoplePanes(h))


class SearchScope(modals.TextPrompt):
    """B · a scope switch in the search window: `tasks` (today's filter) or `people`
    (names only; `↵` opens the person)."""
    BINDINGS = [Binding("alt+n", "scope", "", priority=True),
                Binding("up", "move(-1)", "", priority=True),
                Binding("down", "move(1)", "", priority=True)]
    DEFAULT_CSS = "#sp-list { height: auto; margin: 0 0 1 0; } #sp-scope { height: 1; }"

    def on_mount(self) -> None:
        super().on_mount()
        self.scope, self.sel, self.opts = "tasks", 0, []
        box = self.query_one("#modal-box")
        box.mount(Static(id="sp-scope"), after=".modal-title")
        box.mount(Static(id="sp-list"), after="#f-text")
        self.call_after_refresh(self._draw)

    def check_action(self, action, parameters):
        if action == "move":
            return self.scope == "people"
        return super().check_action(action, parameters)

    def on_input_changed(self, event) -> None:
        self.sel = 0
        self._draw()

    def _draw(self) -> None:
        sc = Text(no_wrap=True)
        for s in ("tasks", "people"):
            on = s == self.scope
            sc.append(f" {s} ", style=(f"b #0d1117 on {HEX['accent']}" if on else HEX["mut"]))
            sc.append(" ")
        sc.append("  alt+n", style=f"b {HEX['bright']}")
        sc.append(" switch", style=HEX["mut"])
        self.query_one("#sp-scope", Static).update(sc)
        lst = self.query_one("#sp-list", Static)
        keys = self.query(".modal-keys")
        if self.scope == "people":
            v = self.query_one("#f-text", Input).value
            rows, self.opts = pick_rows(v, self.sel, 52, 6)
            self.opts = [o for o in self.opts if o[0] == "p"]
            rows = rows[:len(self.opts)] or [row(("  no one by that name", HEX["dim"]), w=52)]
            lst.update(Text("\n").join(rows))
            lst.display = True
            if keys:
                keys.first().update(key_line([("↑↓", ""), ("↵", "open the person"), ("alt+n", "tasks"),
                                              ("esc", "cancel")], 54))
        else:
            lst.display = False
            if keys:
                keys.first().update(key_line([("↵ / alt+s", "filter"), ("alt+n", "people"),
                                              ("esc", "cancel")], 54))

    def action_scope(self) -> None:
        self.scope = "people" if self.scope == "tasks" else "tasks"
        self.sel = 0
        self._draw()

    def action_move(self, d: int) -> None:
        self.sel = max(0, min(len(self.opts) - 1, self.sel + d))
        self._draw()

    def _save(self) -> None:
        if self.scope == "people":
            if self.opts:
                h = self.opts[self.sel][1]["id"]
                self.dismiss(None)
                self.app.push_screen(PeoplePanes(h))
            return
        super()._save()


# =============================================================================
# the app and the scenes
# =============================================================================
def sel(tid: str):
    def step(app):
        app.selected_task_id = tid
        app.refresh_view()
    return step


def notes_end(app) -> None:
    ta = app.screen.query_one("#f-notes", TextArea)
    ta.focus()
    ta.move_cursor(ta.document.end)


def typed(s: str) -> list[str]:
    return ["enter" if ch == "\n" else "space" if ch == " " else ch for ch in s]


class Proto(TaskboardApp):
    BINDINGS = [Binding("at", "people", "", show=False)]     # prototype: not in KEYMAP
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene: str, root: Path, seconds: float | None = None):
        sc = SCENES[scene]
        self.scene, self._steps, self._seconds = scene, sc["steps"], seconds
        self.played = False
        self._root = root
        fx.build(root, last=sc.get("last", "client-a"))
        DIR.clear()
        for p in json.loads((root / "people.json").read_text(encoding="utf-8"))["people"]:
            DIR[p["id"]] = p
        STYLE[0] = sc.get("style")
        SEARCH[0] = sc.get("search")
        reg = Registry.load(root / "boards.json", root / "board.json")
        entry = reg.opening()
        reg.touch(entry.id, datetime.now())
        self._people = sc.get("people")
        self._undo_patch = []
        patch = dict(sc.get("patch", {}))
        if STYLE[0]:
            patch.update({(modals, "notes_preview"): notes_preview_m,
                          (views, "_card_meta"): card_meta_m,
                          (views, "present_note_lines"): present_note_lines_m,
                          (views, "_present_note_markup"): present_note_markup_m})
        patch.update({(views, "matches"): matches_m, (views, "filter_bar"): filter_bar_m})
        for (mod, name), val in patch.items():
            self._undo_patch.append((mod, name, getattr(mod, name)))
            setattr(mod, name, val)
        super().__init__(board_path=entry.path, registry=reg, team_sync_interval=1e9)

    def unpatch(self) -> None:
        for mod, name, val in reversed(self._undo_patch):
            setattr(mod, name, val)

    def check_action(self, action, parameters):
        if action == "people":
            return self._people is not None and len(self.screen_stack) == 1
        return super().check_action(action, parameters)

    def action_people(self) -> None:
        self.push_screen(self._people())

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
            await asyncio.sleep(0.25)
        await asyncio.sleep(0.6)
        self.played = True
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            # first line: the temporary home, so the harness can remove it after closing
            ok = self.check_state()
            Path(ready).write_text(f"{self._root}\n{'OK' if ok else 'BAD'} {self.screen_stack!r} "
                                   f"board={self.board_id} sel={self.selected_task_id}",
                                   encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


# what each scene must end on (recorded headless); a live run that ends elsewhere —
# a key lost while the window was starting — is reported BAD and shot again
EXPECT = {'pv-now': 'Screen', 'pv-A': 'PeoplePanes', 'pv-A-open': 'Screen', 'pv-B': 'PeopleCards',
          'pv-C': 'PersonPage', 'mt-now': 'TaskModal', 'mt-A': 'EditorInline',
          'mt-A-add': 'EditorInline', 'mt-A-done': 'EditorInline', 'mt-B': 'PersonPicker',
          'mt-B-add': 'PersonPicker', 'sr-now': 'TextPrompt', 'sr-now-res': 'Screen',
          'sr-A': 'SearchAt', 'sr-A-res': 'Screen', 'sr-B': 'SearchScope',
          'sr-B-res': 'PeoplePanes', 'sr-C-res': 'Screen'}
VIEW = {'pv-now': 'people', 'pv-A-open': 'kanban', 'sr-now-res': 'kanban', 'sr-A-res': 'kanban',
        'sr-C-res': 'kanban'}


def _check_state(self) -> bool:
    sc = self.scene
    want = EXPECT.get(sc) or {"det": "TaskDetails", "kb": "Screen",
                              "pr": "PresentScreen"}[sc.rsplit("-", 1)[1]]
    view = VIEW.get(sc) or ("kanban" if sc.endswith("-kb") else None)
    depth = {"mt-B": 3, "mt-B-add": 3}.get(sc)
    return (type(self.screen).__name__ == want and (view is None or self.view_mode == view)
            and (depth is None or len(self.screen_stack) == depth))


Proto.check_state = _check_state
TM = (app_mod, "TaskModal")
TP = (app_mod, "TextPrompt")
EDIT = ["escape", sel("tc8"), "e", notes_end]
SEARCH_K = ["escape", "4", "slash"]
SCENES: dict[str, dict] = {
    # 1 · the people view
    "pv-now": dict(steps=["escape", "9"]),
    "pv-A": dict(steps=["escape", "at", "tab", "down"], people=PeoplePanes, style="A"),
    "pv-A-open": dict(steps=["escape", "4", "at", "tab", "down", "enter"], people=PeoplePanes, style="A"),
    "pv-B": dict(steps=["escape", "at", "right"], people=PeopleCards, style="A"),
    "pv-C": dict(steps=["escape", "at", "down"], people=PersonPage, style="A"),
    # 2 · `@` in the editor's notes
    "mt-now": dict(steps=EDIT + typed("\nAsk @an")),
    "mt-A": dict(steps=EDIT + typed("\nAsk @an"), patch={TM: EditorInline}, style="A"),
    "mt-A-add": dict(steps=EDIT + typed("\nCall @Sofia") + ["enter"] + typed("Legal counsel"),
                     patch={TM: EditorInline}, style="A"),
    "mt-A-done": dict(steps=EDIT + typed("\nAsk @an") + ["enter"] + typed("about the stores"),
                      patch={TM: EditorInline}, style="A"),
    "mt-B": dict(steps=EDIT + typed("\nAsk @an"), patch={TM: EditorModal}, style="A"),
    "mt-B-add": dict(steps=EDIT + typed("\nCall @Sofia") + ["alt+a"] + typed("Legal counsel"),
                     patch={TM: EditorModal}, style="A"),
    # 3 · search by person
    "sr-now": dict(steps=SEARCH_K + typed("ana")),
    "sr-now-res": dict(steps=SEARCH_K + typed("ana") + ["enter"]),
    "sr-A": dict(steps=SEARCH_K + typed("@an"), patch={TP: SearchAt}, style="A"),
    "sr-A-res": dict(steps=SEARCH_K + typed("@an") + ["enter"], patch={TP: SearchAt}, style="A"),
    "sr-B": dict(steps=SEARCH_K + ["alt+n"] + typed("ma"), patch={TP: SearchScope}, style="A"),
    "sr-B-res": dict(steps=SEARCH_K + ["alt+n"] + typed("ma") + ["enter"],
                     patch={TP: SearchScope}, style="A"),
    "sr-C-res": dict(steps=SEARCH_K + typed("pm") + ["enter"], search="C", style="A"),
    # 4 · how a mention looks
    "m-now-det": dict(steps=["escape", sel("tc5"), "enter"]),
    "m-now-kb": dict(steps=["escape", "4", sel("tc5")]),
    "m-now-pr": dict(steps=["escape", sel("tc5"), "R", "2"]),
    **{f"m-{v}-det": dict(steps=["escape", sel("tc5"), "enter"], style=v) for v in "ABC"},
    **{f"m-{v}-kb": dict(steps=["escape", "4", sel("tc5")], style=v) for v in "ABC"},
    **{f"m-{v}-pr": dict(steps=["escape", sel("tc5"), "R", "2"], style=v) for v in "ABC"},
}
SIZES = [(118, 30), (80, 24)]


def _strip_font(svg: str) -> str:
    return re.sub(r"@font-face\s*\{[^}]*\}", "", svg)


async def _shot_one(scene: str, size) -> None:
    root = Path(tempfile.mkdtemp(prefix="ppl-svg-"))
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


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "shot":
        shot(args[1:])
    elif args and args[0] == "live":
        root = Path(tempfile.mkdtemp(prefix="ppl-cap-"))
        try:
            Proto(args[1], root, float(args[2]) if len(args) > 2 else None).run()
        finally:
            shutil.rmtree(root, ignore_errors=True)
    else:
        print(__doc__)

"""THROWAWAY prototype — the milestone-marks round: a milestone gets a CLASS
(a user-named shape + colour: "Delivery ▲", "Payment ●", …) so it can be told
apart, chosen in the task editor, managed in a small window, read in every
view that draws a milestone, and filtered or grouped by.

    unset NO_COLOR; PYTHONUTF8=1 python prototypes/milestone_marks/proto.py list
    unset NO_COLOR; PYTHONUTF8=1 python prototypes/milestone_marks/proto.py shot [SCENE ...]
    PYTHONUTF8=1 python prototypes/milestone_marks/proto.py text SCENE [WxH]   (plain dump)
    python prototypes/milestone_marks/proto.py live SCENE [SECONDS]            (a real terminal)

Sub-shape A: the REAL `TaskboardApp` (subclassed here), on a real registry in a
temporary folder (fixture.py), driven by real key presses (`App._press_keys`)
— headless for the SVGs, in a real Windows Terminal for the PNGs (shoot.ps1).

How the marks reach every view without editing `taskboard/`: each shipped draw
of a milestone is `c("◆", milestone_tone(task, …))`. The scene patches
`views.milestone_tone` to return a per-(class, state) palette key and
`views.c` to swap the `◆` for that key's shape and paint it with that key's
colours — one interception point, so lanes, focus, gantt (field, label,
ruler), presentation and its export all change together. The kanban's band
rule, the `A` agenda and the gantt's legend compute their own tones and get
small wrappers. Nothing writes outside the temporary folder.
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import fixture as fx  # noqa: E402
from rich.text import Text  # noqa: E402
from textual.binding import Binding  # noqa: E402
from textual.containers import Horizontal, Vertical  # noqa: E402
from textual.screen import ModalScreen, Screen  # noqa: E402
from textual.widgets import Button, Input, Select, Static  # noqa: E402

from taskboard import app as app_mod, models, modals, ribbon, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.keymap import key_line  # noqa: E402
from taskboard.models import parse_iso  # noqa: E402
from taskboard.views import HEX, fit, vis  # noqa: E402

TODAY = fx.TODAY
OUT = HERE / "out"


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):           # the ribbon's clock agrees with the pinned Tuesday
        base = datetime(2026, 10, 20, 10, 30, 0)
        return base if tz is None else datetime(2026, 10, 20, 16, 30, 0, tzinfo=tz)


ribbon.datetime = _Now
app_mod.date = _Today
models.date = _Today
views.date = _Today
modals.date = _Today if hasattr(modals, "date") else None

# =============================================================================
# the class directory (D2: global, `~/.taskboard/marks.json`, like people.json)
# =============================================================================
CLS: dict[str, dict] = {}            # id -> {"id","name","shape","colour"}; loaded per app
HOLLOW = {"◆": "◇", "▲": "△", "●": "○", "■": "□", "★": "☆", "▼": "▽", "⬟": "⬠", "⬢": "⬡",
          "✦": "✧", "⚑": "⚐"}
SHAPES = ["▲", "■", "⬢", "★", "⬟", "▼", "✦", "⚑"]     # the manager's shape row (glyph sheet)
SWATCH = ["cyan", "amber", "violet", "pink", "green", "orange", "sky", "lime"]
ENC: list[str | None] = [None]       # the encoding (D1): None = today, "A", "B", "C"
LEGEND: list[str | None] = [None]    # item 3: None, "A" (? map), "B" (strip), "C" (in the row)
GROUP: list[bool] = [False]          # item 4 C: the gantt's milestones grouped by class
HIDDEN: set[str] = set()             # item 4 B: classes switched off in the `#` window
BG = {"over": "#5c1424", "today": "#4d3608"}     # variant C's state ground (dark tints)


def mark_of(task) -> dict | None:
    return CLS.get((task.extra or {}).get("mark") or "")


def state_of(task, board, today) -> str:
    if board.is_done(task):
        return "reached"
    d = parse_iso(task.due_date)
    if d is not None and d < today:
        return "over"
    if d == today:
        return "today"
    return "open"


MSTYLE: dict[str, tuple[str, str, str | None]] = {}     # key -> (glyph, fg hex, bg hex)


def mark_key(task, board, today, orig_tone: str) -> str:
    """The palette key a milestone is drawn with under the scene's encoding."""
    v, m, st = ENC[0], mark_of(task), state_of(task, board, today)
    shape = m["shape"] if m else "◆"
    hue = HEX[m["colour"]] if m else HEX[views.project_color(board, task)]
    if v == "A":           # shape = class; colour = state, exactly as today
        glyph, fg, bg = shape, HEX[orig_tone], None
    elif v == "B":         # shape + colour = class; state in the text; hollow = reached
        glyph, fg, bg = (HOLLOW.get(shape, shape) if st == "reached" else shape), hue, None
    else:                  # C: shape + colour = class; state as the cell's ground
        glyph = shape
        fg = HEX["reached"] if st == "reached" else hue
        bg = BG.get(st)
    key = f"mk:{glyph}:{fg}:{bg}"
    HEX[key] = fg
    MSTYLE[key] = (glyph, fg, bg)
    return key


_ORIG_C = views.c
_ORIG_TONE = views.milestone_tone


def c_m(text: str, key: str, bold: bool = False) -> str:
    st = MSTYLE.get(key)
    if st is None:
        return _ORIG_C(text, key, bold)
    glyph, fg, bg = st
    text = text.replace("◆", glyph)
    return f"[{'b ' if bold else ''}{fg}{' on ' + bg if bg else ''}]{text}[/]"


def milestone_tone_m(task, board, today) -> str:
    return mark_key(task, board, today, _ORIG_TONE(task, board, today))


def gantt_milestone_cells_m(task, board, ax, today, tone):
    """The shipped `gantt_milestone_cells`, with the class's glyph in the cell and
    the date beside it carrying the STATE (red late, amber today) in every variant."""
    cells = [(" ", "dim")] * ax.w
    d = parse_iso(task.due_date)
    if d is None or ax.w < 3:
        return cells
    glyph = MSTYLE.get(tone, ("◆",))[0]
    marks = [(glyph, tone)] + ([("✓", "reached")] if board.is_done(task) else [])
    x = ax.cell(d)
    if x < 0:
        cells[0] = (views.OFF_LEFT, "mut")
        x = 1
    elif x >= ax.w:
        cells[-1] = (views.OFF_RIGHT, "mut")
        x = ax.w - 1 - len(marks)
    elif x + len(marks) > ax.w:
        marks = marks[:1]
    x = max(0, min(x, ax.w - len(marks)))
    for i, m in enumerate(marks):
        cells[x + i] = m
    st = state_of(task, board, today)
    key = {"reached": "reached", "over": "over", "today": "soon"}.get(st, "mut")
    lab = views._md(d)
    if LEGEND[0] == "C" and (m := mark_of(task)):
        lab = f"{lab} · {m['name'].lower()}"
    after, before = x + len(marks) + 1, x - 1 - len(lab)
    at = after if after + len(lab) <= ax.w else (before if before >= 0 else None)
    if at is not None:
        for i, ch in enumerate(lab):
            cells[at + i] = (ch, key) if ch != " " else (" ", "gap")
        cells[at - 1 if at == after else at + len(lab)] = (" ", "gap")
    return cells


_ORIG_BAND = views.band_milestone_facts


def band_milestone_facts_m(items, room, color, today):
    """The kanban's band rule: the shipped layout, each milestone's `◆ ` piece
    re-keyed to its class (the facts are laid in `items` order)."""
    out = _ORIG_BAND(items, room, color, today)
    i, res = 0, []
    for f in out:
        if f[0] == "◆ " and i < len(items):
            kind, t = items[i]
            board = BOARD[0]
            res.append(("◆ ", mark_key(t, board, today, f[1])) + tuple(f[2:]))
            i += 1
        else:
            res.append(f)
    return res


BOARD: list = [None]                 # the app's board, for the wrappers that are not handed one
_ORIG_AGENDA_ROW = views._agenda_row


def agenda_row_m(it, on, inner, today):
    """The `A` agenda's row: today it draws no `◆` at all; here a milestone wears
    its mark before the title (the title gives up two cells)."""
    if not it.task.milestone:
        return _ORIG_AGENDA_ROW(it, on, inner, today)
    bw = 12 if inner >= 100 else 10
    pw = 22 if inner >= 100 else 0
    hexc = views.board_hex(it.colour)
    r = Text(no_wrap=True)
    r.append("▶ " if on else "  ", style=HEX["accent"])
    r.append("▌", style=hexc)
    r.append(fit(it.board_name, bw), style=hexc)
    r.append(" ")
    if pw:
        r.append(fit(it.project, pw), style=HEX["dim"])
        r.append(" ")
    wl, wc = views._agenda_when(it.due, today)
    tw = max(1, inner - 3 - bw - 1 - (pw + 1 if pw else 0) - 8 - 2)
    m = mark_of(it.task)
    glyph = m["shape"] if m else "◆"
    fg = HEX[m["colour"]] if m else hexc
    if ENC[0] == "A":
        fg = wc if it.due <= today else hexc
    r.append(glyph, style=fg)
    r.append(" ")
    r.append(fit(it.task.title, tw), style=f"bold {HEX['bright']}" if on else HEX["ink"])
    r.append(f"{wl:>8}", style=wc)
    r.truncate(inner)
    r.pad_right(inner - r.cell_len)
    if on:
        r.stylize("on #1d2a3a")
    return r


# ---- the legend (item 3) and the grouped band (item 4 C) --------------------
def classes_on(board) -> list[dict]:
    used = {(t.extra or {}).get("mark") for t in board.tasks if t.milestone and not t.archived}
    return [m for m in CLS.values() if m["id"] in used]


def legend_strip(board, w: int, lead: str = " ") -> str:
    """B · one row naming the classes this board uses: shape, name, how many open."""
    parts = []
    for m in classes_on(board):
        n = sum(1 for t in board.tasks if t.milestone and (t.extra or {}).get("mark") == m["id"]
                and not board.is_done(t) and not t.archived)
        off = m["id"] in HIDDEN
        tone = "dim" if off else m["colour"]
        parts.append(_ORIG_C(m["shape"], tone) + " "
                     + _ORIG_C(m["name"] + (" (hidden)" if off else f" {n}"),
                               "dim" if off else "mut"))
    parts.append(_ORIG_C("◆", "mut") + " " + _ORIG_C("unclassed", "dim"))
    out = lead + _ORIG_C(" · ", "dim").join(parts)
    if HIDDEN:
        out += _ORIG_C("   # to switch", "dim")
    return views._pad(out, w)


_ORIG_FRAME = views._gantt_frame


def gantt_frame_m(board, show_archived, selected_id, today=None, width=68, height=0,
                  line_map=None, tick=0, focus=None, previous=None, pinned_id=None):
    """The gantt frame with the round's extra rows under the ruler: the legend
    strip (B) or the class band (item 4 C), and HIDDEN classes dropped."""
    today = today or views.date.today()
    if HIDDEN:
        board = _hide(board)
    w = views._clamp_width(width)
    args = (board, show_archived, selected_id, today, width)
    rest = (tick, focus, previous, pinned_id)
    want_strip, want_band = LEGEND[0] == "B" or bool(HIDDEN), GROUP[0]
    if not (want_strip or want_band):
        return _ORIG_FRAME(*args, height, line_map, *rest)
    # the axis first (a dry frame), then the frame packed into the rows left, so its
    # own folding and paging decide what gives way — never a cut from the bottom
    _l, _d, _g, ax = _ORIG_FRAME(*args, height, None, *rest)
    extra = class_band(board, ax, today, w) if want_band else [legend_strip(board, w)]
    lines, drawn, groups, ax = _ORIG_FRAME(*args, max(4, height - len(extra)) if height else 0,
                                           line_map, *rest)
    lines = lines[:3] + extra + lines[3:]
    if line_map is not None:
        for k, v in list(line_map.items()):
            if v >= 3:
                line_map[k] = v + len(extra)
    return lines, drawn, groups, ax


def _hide(board):
    import copy
    proxy = copy.copy(board)
    proxy.tasks = [t for t in board.tasks
                   if not (t.milestone and (t.extra or {}).get("mark") in HIDDEN)]
    return proxy


def class_band(board, ax, today, w) -> list[str]:
    """C · MILESTONES BY CLASS: one row per class, every milestone of the board on
    it (any project), over the same axis as the field below."""
    label_w, chip_w, _f = views.gantt_columns(w)
    guides, weekends = ax.guides(), ax.weekends()
    rows = [views._pad(_ORIG_C(views.fit(" MILESTONES BY CLASS", label_w - 1) + " ", "hd", bold=True)
                       + _ORIG_C("─" * (w - label_w), "frame"), w)]
    for m in list(classes_on(board)) + [None]:
        ms = [t for t in board.tasks if t.milestone and not t.archived and t.due_date
              and (mark_of(t) is m or (m and mark_of(t) and mark_of(t)["id"] == m["id"]))]
        if not ms:
            continue
        cells = [(" ", "dim")] * ax.w
        for t in sorted(ms, key=lambda t: t.due_date):
            x = ax.cell(parse_iso(t.due_date))
            if 0 <= x < ax.w:
                k = milestone_tone_m(t, board, today)
                cells[x] = (MSTYLE[k][0], k)
        nxt = next((t for t in sorted(ms, key=lambda t: t.due_date)
                    if not board.is_done(t) and parse_iso(t.due_date) >= today), None)
        name = m["name"] if m else "unclassed"
        lab = (" " + _ORIG_C(m["shape"] if m else "◆", m["colour"] if m else "mut") + " "
               + _ORIG_C(views.escape(views.fit(f"{name} · {len(ms)}", label_w - 4)), "ink"))
        chip = (views.gantt_milestone_chip(nxt, board, today, chip_w) if nxt and chip_w
                else " " * chip_w)
        rows.append(views._pad(views._pad(lab, label_w) + " "
                               + views._gantt_field(cells, ax, guides, weekends)
                               + (" " + chip if chip_w else ""), w))
    rows.append(views._pad(_ORIG_C("─" * w, "frame"), w))
    return rows


_ORIG_MONTH = views.gantt_month_row


def gantt_month_row_m(ax, today, marks):
    """The ruler's marks wear the class glyph too (the shipped row paints them itself)."""
    return _ORIG_MONTH(ax, today, {x: ((MSTYLE[k][0] if k in MSTYLE else g), k)
                                   for x, (g, k) in marks.items()})


_ORIG_PRULER = views._present_ruler


def present_ruler_m(proj, board, p, cursor):
    out = _ORIG_PRULER(proj, board, p, cursor)
    if LEGEND[0] == "B":
        out = out + [legend_strip_project(board, proj, p.width)]
    return out


def legend_strip_project(board, proj, w) -> str:
    """The presentation's legend: only the classes this project shows, for the room."""
    used = {(t.extra or {}).get("mark") for t in board.tasks
            if t.milestone and t.project_id == proj.id and t.show_in_present}
    parts = [_ORIG_C(m["shape"], m["colour"]) + " " + _ORIG_C(m["name"], "mut")
             for m in CLS.values() if m["id"] in used]
    if None in used:
        parts.append(_ORIG_C("◆", "mut") + " " + _ORIG_C("milestone", "mut"))
    return views._pad("  " + _ORIG_C(" · ", "dim").join(parts), w)


_ORIG_PTASKS = views.present_tasks


def present_tasks_m(board, project_id):
    """The presentation drops the classes switched off in the `#` window too."""
    open_t, tasks = _ORIG_PTASKS(board, project_id)
    keep = [t for t in tasks if not (t.milestone and (t.extra or {}).get("mark") in HIDDEN)]
    return [t for t in open_t if t in keep], keep


_ORIG_LEGEND = views._gantt_legend


def gantt_legend_m(width, drawn):
    """The gantt's spare-row legend: under a variant it names the classes instead of
    one `◆ milestone` (the rest kept, shortest first to go)."""
    if ENC[0] is None or BOARD[0] is None or LEGEND[0] in ("B", "C"):
        return _ORIG_LEGEND(width, drawn - ({"milestone", "reached"} if ENC[0] else set()))
    parts = [_ORIG_C(m["shape"], "mut" if ENC[0] == "A" else m["colour"]) + " "
             + _ORIG_C(m["name"], "dim") for m in classes_on(BOARD[0])]
    head = " " + _ORIG_C(" · ", "dim").join(parts)
    rest = _ORIG_LEGEND(max(0, width - vis(views._strip(head)) - 3),
                        drawn - {"milestone", "reached"})
    out = head + (_ORIG_C(" · ", "dim") + rest.strip() if rest.strip() else "")
    return views._pad(out, width)


# =============================================================================
# the glyph sheet (item 1): every candidate shape at one cell, between bars
# =============================================================================
SHEET = [  # glyph, hollow, verdict, why (verdicts from the real Windows Terminal capture)
    ("◆", "◇", "keep", "the default (no class); also the project's due on span rows"),
    ("▲", "△", "accept", "Cascadia Mono · ▲ is also the 'late' mark in chips (▲2d)"),
    ("■", "□", "accept", "Cascadia Mono"),
    ("⬢", "⬡", "accept", "Cascadia Mono"),
    ("⬟", "⬠", "accept", "Cascadia Mono"),
    ("▼", "▽", "accept", "Cascadia Mono"),
    ("★", "☆", "accept*", "not in Cascadia; WT's fallback font draws it in one cell"),
    ("✦", "✧", "accept*", "not in Cascadia; fallback, one cell"),
    ("⚑", "⚐", "accept*", "not in Cascadia; fallback, one cell"),
    ("●", "○", "avoid", "the gantt's progress dot; ○◔◑◕ are its phase tips"),
    ("◉", "◎", "reject", "the gantt's pulse (◉ ◎)"),
    ("♦", "◈", "reject", "reads as ◆"),
    ("⬤", "◯", "reject", "draws exactly like ● in Cascadia"),
    ("⬛", "⬜", "reject", "East-Asian WIDE: 2 cells, the bars shift"),
    ("⭐", "", "reject", "emoji, WIDE: 2 cells"),
]


class GlyphSheet(Screen[None]):
    BINDINGS = [Binding("escape", "back", "", priority=True)]
    DEFAULT_CSS = "GlyphSheet { background: #0d1117; } #gs { padding: 0 1; }"

    def compose(self):
        yield Static(id="gs")

    def on_mount(self) -> None:
        self._paint()

    def on_resize(self, _e) -> None:
        self._paint()

    def _paint(self) -> None:
        w, h = self.app.size
        inner = w - 2
        t = Text(no_wrap=True)
        t.append("◆ GLYPH SHEET", style=f"b {HEX['bright']}")
        t.append("  each shape 6× in its cells, bars every cell · on a ground · hollow twin",
                 style=HEX["mut"])
        t.append("\n")
        cols = ["cyan", "amber", "violet", "pink", "green", "orange"]
        narrow = inner < 100
        for i, (g, hol, verdict, why) in enumerate(SHEET[: h - 3]):
            hue = HEX[cols[i % len(cols)]]
            vt = {"keep": "mut", "accept": "green", "accept*": "lime", "avoid": "amber",
                  "reject": "over"}[verdict]
            t.append(f"U+{ord(g):04X} ", style=HEX["dim"])
            t.append("│", style=HEX["frame"])
            for _ in range(6):
                t.append(g, style=hue)
                t.append("│", style=HEX["frame"])
            t.append(" ")
            t.append(g * 6, style=hue)
            t.append("│", style=HEX["frame"])
            t.append(" ")
            t.append(g, style=f"{hue} on {BG['over']}")
            t.append(g, style=f"{hue} on {BG['today']}")
            t.append(g, style=f"{hue} on #1a1d22")
            t.append("│", style=HEX["frame"])
            t.append(" ")
            t.append(hol or " ", style=hue)
            t.append("│", style=HEX["frame"])
            t.append(f" {verdict:<7} ", style=f"b {HEX[vt]}")
            if not narrow:
                t.append(why, style=HEX["mut"])
            t.append("\n")
        self.query_one("#gs", Static).update(t)

    def action_back(self) -> None:
        self.app.pop_screen()



_ORIG_LEGEND_ENTRIES = views.legend_entries


def legend_entries_m(mode, board, today=None, *a, **k):
    """The `?` map (legend A): under a variant the gantt's one `◆ milestone` entry
    becomes one entry per class used, plus how this encoding draws the states."""
    out = _ORIG_LEGEND_ENTRIES(mode, board, today, *a, **k)
    if ENC[0] is None or mode != "gantt":
        return out
    keep = [e for e in out if not str(e[1]).startswith("a milestone")]
    add = [(_ORIG_C(m["shape"], "mut" if ENC[0] == "A" else m["colour"]),
            f"{m['name']} · a milestone class")
           for m in classes_on(board)]
    add.append((_ORIG_C("◆", "mut"), "a milestone with no class"))
    if ENC[0] == "B":
        add += [(_ORIG_C("⬢", "amber") + " " + _ORIG_C("Oct 18", "over"),
                 "late: the date beside it turns red"),
                (_ORIG_C("⬡", "amber") + _ORIG_C("✓", "reached"), "reached: the hollow twin ✓")]
    elif ENC[0] == "C":
        add += [(f"[{HEX['amber']} on {BG['over']}]⬢[/]", "late: a red ground under it"),
                (f"[{HEX['amber']} on {BG['today']}]⬢[/]", "today: an amber ground"),
                (_ORIG_C("⬢", "reached") + _ORIG_C("✓", "reached"), "reached: grey ✓")]
    else:
        add += [(_ORIG_C("⬢", "over"), "late: red, whatever the class"),
                (_ORIG_C("⬢", "reached") + _ORIG_C("✓", "reached"), "reached: grey ✓")]
    return keep[:3] + add + keep[3:]


# ---- search by class (item 4 A): `/#pay` -------------------------------------
_ORIG_MATCHES = views.matches
_ORIG_FILTER_BAR = views.filter_bar


def find_class(q: str) -> dict | None:
    q = q.lower()
    return next((m for m in CLS.values() if m["name"].lower().startswith(q)), None)


def matches_m(task, board, q):
    if q.startswith("#"):
        m, mine = find_class(q[1:]), mark_of(task)
        return "class" if (task.milestone and m and mine and mine["id"] == m["id"]) else None
    return _ORIG_MATCHES(task, board, q)


def filter_bar_m(query, hits, total, w, people=None):
    m = find_class(query[1:]) if query.startswith("#") else None
    if m is None:
        return _ORIG_FILTER_BAR(query, hits, total, w, people)
    left = (_ORIG_C("/", "accent", bold=True) + " "
            + _ORIG_C(m["shape"] + " " + m["name"], m["colour"], bold=True)
            + _ORIG_C("  milestones of this class only", "mut"))
    right = _ORIG_C(f"{hits}/{total} tasks", "mut") + _ORIG_C(" · esc clears", "dim")
    return [views.header(left, right, w), views.head_rule(w)]


# =============================================================================
# item 2: choosing the class in the editor, and the class manager
# =============================================================================
def opt_text(m: dict | None) -> Text:
    if m is None:
        return Text.assemble(("◆ ", HEX["mut"]), ("none", HEX["mut"]))
    return Text.assemble((m["shape"] + " ", HEX[m["colour"]]), (m["name"], HEX["ink"]))


def counts_all(app) -> dict[str, tuple[int, int]]:
    """Per class: (open, all) milestones over every board of the registry."""
    out: dict[str, list[int]] = {k: [0, 0] for k in CLS}
    for e in app.registry.entries:
        try:
            b = models.Board.load(e.path)
        except Exception:
            continue
        for t in b.tasks:
            k = (t.extra or {}).get("mark")
            if t.milestone and k in out:
                out[k][1] += 1
                out[k][0] += 0 if b.is_done(t) else 1
    return {k: (v[0], v[1]) for k, v in out.items()}


EDIT_KEYS = list(modals.TASK_KEYS)


class EditorBase(modals.TaskModal):
    """The shipped editor (full screen) plus the round's class control."""
    def on_mount(self) -> None:
        super().on_mount()
        self.mark = (self._edit_task.extra or {}).get("mark") if self._edit_task else None
        modals.TASK_KEYS[:] = EDIT_KEYS[:1] + [("alt+m", "mark")] + EDIT_KEYS[1:]
        self._fit_width(self.app.size.width)


class EditorSelect(EditorBase):
    """A · a `Mark` select in the chip row, beside `milestone` (like project/phase/prio)."""
    BINDINGS = [Binding("alt+m", "mark", "", priority=True)]
    DEFAULT_CSS = "#f-mark { width: 16; } #f-mark SelectOverlay { width: 24; }"

    def on_mount(self) -> None:
        super().on_mount()
        opts = [(opt_text(None), "")] + [(opt_text(m), m["id"]) for m in CLS.values()]
        opts.append((Text("+ new class…", HEX["green"]), "__new"))
        s = Select(opts, value=self.mark or "", allow_blank=False, id="f-mark")
        self.query_one("#task-chips-what").mount(s, after="#f-milestone")

    def action_mark(self) -> None:
        s = self.query_one("#f-mark", Select)
        s.focus()
        s.action_show_overlay()


class MarkSegment(Static, can_focus=True):
    BINDINGS = [Binding("left", "step(-1)", "", show=False),
                Binding("right", "step(1)", "", show=False)]

    def __init__(self, value: str | None, **kw):
        super().__init__(**kw)
        self.ids = [""] + list(CLS)
        self.i = self.ids.index(value or "")

    def on_mount(self) -> None:
        self._draw()

    def on_focus(self) -> None:
        self._draw()

    def on_blur(self) -> None:
        self._draw()

    def _draw(self) -> None:
        t = Text(no_wrap=True)
        t.append("Mark ", style=f"b {HEX['hd']}")
        for j, k in enumerate(self.ids):
            piece = Text(" ") + opt_text(CLS.get(k)) + Text(" ")
            if j == self.i:
                piece.stylize(f"b on {'#1d3a4a' if self.has_focus else '#1d2a3a'}")
            t.append_text(piece)
            t.append(" ")
        t.append("  ←→ choose" if self.has_focus else "  alt+m", style=HEX["dim"])
        self.update(t)

    def action_step(self, d: int) -> None:
        self.i = (self.i + d) % len(self.ids)
        self._draw()


class EditorSegment(EditorBase):
    """B · a row of every class under the chips: all visible, one keystroke."""
    BINDINGS = [Binding("alt+m", "mark", "", priority=True)]
    DEFAULT_CSS = "#f-markrow { height: 1; margin-top: 1; }"

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#task-box").mount(MarkSegment(self.mark, id="f-markrow"),
                                          after="#task-chips")

    def action_mark(self) -> None:
        self.query_one("#f-markrow", MarkSegment).focus()


class EditorPicker(EditorBase):
    """C · the class sits in the title row; alt+m opens a small picker window."""
    BINDINGS = [Binding("alt+m", "press_button('f-markbtn')", "", priority=True)]
    DEFAULT_CSS = "#f-markbtn { width: auto; min-width: 14; margin: 0 1; }"

    def on_mount(self) -> None:
        super().on_mount()
        m = CLS.get(self.mark or "")
        b = Button(opt_text(m) + Text(" ▾ alt+m", HEX["dim"]), id="f-markbtn")
        self.query_one("#task-head").mount(b, before="#f-present")

    def on_button_pressed(self, event) -> None:
        if event.button.id == "f-markbtn":
            event.stop()
            event.prevent_default()      # Textual walks the MRO: TaskModal's handler would dismiss
            self.app.push_screen(MarkPicker(self.mark))


class MarkPicker(modals.ButtonKeysMixin, ModalScreen[str | None]):
    """C · filter field, the classes (with how many milestones each), `+ new`."""
    BINDINGS = [Binding("escape", "dismiss(None)", "", priority=True),
                Binding("up", "move(-1)", "", priority=True),
                Binding("down", "move(1)", "", priority=True),
                Binding("alt+n", "press_button('mp-new')", "", priority=True),
                Binding("alt+s", "press_button('mp-ok')", "", priority=True)]
    DEFAULT_CSS = f"""
    MarkPicker {{ align: center middle; }}
    #mp-box {{ width: 52; height: auto; background: #111827; border: round {HEX['accent']};
               padding: 0 1; }}
    #mp-q {{ border: tall #334154; height: 3; }}
    #mp-buttons {{ height: 3; }}
    #mp-buttons Button {{ width: auto; min-width: 8; margin-right: 1; }}
    """

    def __init__(self, cur: str | None) -> None:
        super().__init__()
        self.cur, self.sel = cur, 0

    def compose(self):
        with Vertical(id="mp-box"):
            yield Static(Text("Milestone class", style=f"b {HEX['accent']}"))
            yield Input(placeholder="filter classes", id="mp-q")
            yield Static(id="mp-list")
            with Horizontal(id="mp-buttons"):
                yield Button("Choose", variant="success", id="mp-ok")
                yield Button("New class", variant="primary", id="mp-new")
                yield Button("Cancel", id="mp-cancel")
            yield Static(id="mp-keys")

    def on_mount(self) -> None:
        self.query_one("#mp-q", Input).focus()
        self.counts = counts_all(self.app)
        self.sel = ([""] + list(CLS)).index(self.cur or "")
        self._draw()

    def on_input_changed(self, _e) -> None:
        self.sel = 0
        self._draw()

    def _opts(self):
        q = self.query_one("#mp-q", Input).value.strip().lower()
        return [k for k in [""] + list(CLS) if not q or (k and CLS[k]["name"].lower().startswith(q))]

    def _draw(self) -> None:
        ids = self._opts()
        self.sel = min(self.sel, max(0, len(ids) - 1))
        rows = []
        for j, k in enumerate(ids):
            m = CLS.get(k)
            r = Text(no_wrap=True)
            r.append("▶ " if j == self.sel else "  ", style=HEX["accent"])
            r.append_text(opt_text(m))
            n = self.counts.get(k, (0, 0))
            tail = f"{n[0]} open · {n[1]} in all boards" if m else "the plain ◆"
            r.append(" " * max(1, 18 - r.cell_len))
            r.append(tail, style=HEX["dim"])
            if j == self.sel:
                r.stylize("on #1d2a3a")
            rows.append(r)
        q = self.query_one("#mp-q", Input).value.strip()
        if q and not any(CLS.get(k, {}).get("name", "").lower() == q.lower() for k in ids):
            rows.append(Text(f"  + new class '{q}'   alt+n", HEX["green"]))
        self.query_one("#mp-list", Static).update(Text("\n").join(rows))
        self.query_one("#mp-keys", Static).update(key_line(
            [("↑↓", ""), ("↵ / alt+s", "choose"), ("alt+n", "new"), ("esc", "cancel")], 48))

    def action_move(self, d: int) -> None:
        self.sel = max(0, self.sel + d)
        self._draw()

    def on_input_submitted(self, _e) -> None:
        self.query_one("#mp-ok", Button).press()

    def on_button_pressed(self, event) -> None:
        bid = event.button.id
        if bid == "mp-cancel":
            self.dismiss(None)
        elif bid == "mp-new":
            self.app.push_screen(MarkForm(None, self.query_one("#mp-q", Input).value.strip()))
        else:
            ids = self._opts()
            self.dismiss(ids[self.sel] if ids else None)


class ShapeRow(Static, can_focus=True):
    """A row of choices, ←→ moves; the shape row and the colour row."""
    BINDINGS = [Binding("left", "step(-1)", "", show=False),
                Binding("right", "step(1)", "", show=False)]

    def __init__(self, label: str, items: list, i: int, form, **kw):
        super().__init__(**kw)
        self.label, self.items, self.i, self.form = label, items, i, form

    def on_mount(self) -> None:
        self._draw()

    def on_focus(self) -> None:
        self._draw()

    def on_blur(self) -> None:
        self._draw()

    def _draw(self) -> None:
        t = Text(no_wrap=True)
        t.append(f"{self.label:<7}", style=f"b {HEX['hd']}")
        hue = HEX[SWATCH[self.form.ci]]
        for j, it in enumerate(self.items):
            g, style = (it, hue) if self.label == "shape" else ("█", HEX[it])
            on = j == self.i
            t.append("[" if on else " ", style=HEX["accent"] if on and self.has_focus else HEX["dim"])
            t.append(g, style=style)
            t.append("]" if on else " ", style=HEX["accent"] if on and self.has_focus else HEX["dim"])
        if self.label == "colour":
            t.append(f"  {SWATCH[self.i]}", style=HEX["dim"])
        t.append("   ←→" if self.has_focus else "", style=HEX["dim"])
        self.update(t)

    def action_step(self, d: int) -> None:
        self.i = (self.i + d) % len(self.items)
        if self.label == "colour":
            self.form.ci = self.i
        else:
            self.form.si = self.i
        self._draw()
        self.form.refresh_preview()


class MarkForm(modals.ButtonKeysMixin, ModalScreen[None]):
    """The class form (new or edit): name, colour, shape, and a live preview of how
    the gantt draws it in each state under the recommended encoding (D1 B)."""
    BINDINGS = [Binding("escape", "dismiss(None)", "", priority=True),
                Binding("alt+h", "focus_row('mf-shape')", "", priority=True),
                Binding("alt+c", "focus_row('mf-colour')", "", priority=True),
                Binding("alt+n", "focus_row('mf-name')", "", priority=True),
                Binding("alt+s", "press_button('mf-ok')", "", priority=True)]
    DEFAULT_CSS = f"""
    MarkForm {{ align: center middle; }}
    #mf-box {{ width: 70; height: auto; background: #111827; border: round {HEX['accent']};
               padding: 0 1; }}
    #mf-name {{ border: tall #334154; height: 3; }}
    #mf-shape, #mf-colour {{ height: 1; margin-top: 1; }}
    #mf-prev {{ margin-top: 1; height: auto; }}
    #mf-buttons {{ height: 3; margin-top: 1; }}
    #mf-buttons Button {{ width: auto; min-width: 8; margin-right: 1; }}
    """

    def __init__(self, cls_id: str | None, name: str = "") -> None:
        super().__init__()
        m = CLS.get(cls_id or "")
        self.m = m
        self.name0 = m["name"] if m else name
        self.si = SHAPES.index(m["shape"]) if m else 4
        self.ci = SWATCH.index(m["colour"]) if m else 5

    def compose(self):
        with Vertical(id="mf-box"):
            yield Static(Text("Edit class" if self.m else "New class", style=f"b {HEX['accent']}")
                         + Text("  · every board", HEX["dim"]))
            yield Input(value=self.name0, placeholder="class name, e.g. Legal", id="mf-name")
            yield ShapeRow("colour", SWATCH, self.ci, self, id="mf-colour")
            yield ShapeRow("shape", SHAPES, self.si, self, id="mf-shape")
            yield Static(id="mf-prev")
            with Horizontal(id="mf-buttons"):
                yield Button("Save", variant="success", id="mf-ok")
                yield Button("Cancel", id="mf-cancel")
            yield Static(id="mf-keys")

    def on_mount(self) -> None:
        self.refresh_preview()
        self.query_one("#mf-keys", Static).update(key_line(
            [("alt+n", "name"), ("alt+c", "colour"), ("alt+h", "shape"),
             ("alt+s", "save"), ("esc", "cancel")], 66))

    def on_input_changed(self, _e) -> None:
        self.refresh_preview()

    def refresh_preview(self) -> None:
        if not self.query("#mf-prev"):
            return
        shape, hue = SHAPES[self.si], HEX[SWATCH[self.ci]]
        self.query_one("#mf-shape", ShapeRow)._draw()
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

    def on_button_pressed(self, event) -> None:
        self.dismiss(None)


class MarksWindow(modals.ButtonKeysMixin, ModalScreen[None]):
    """`#` · the classes: manage them (n new · e edit · d delete) and choose what
    the gantt and the presentation show (␣ hide/show · ↵ only this one)."""
    BINDINGS = [Binding("escape,number_sign", "close", "", priority=True),
                Binding("up,k", "move(-1)", "", priority=True),
                Binding("down,j", "move(1)", "", priority=True),
                Binding("space", "toggle", "", priority=True),
                Binding("enter", "only", "", priority=True),
                Binding("n", "new", "", priority=True),
                Binding("e", "edit", "", priority=True),
                Binding("d", "delete", "", priority=True)]
    DEFAULT_CSS = f"""
    MarksWindow {{ align: center middle; }}
    #mw-box {{ width: 76; height: auto; background: #111827; border: round {HEX['accent']};
               padding: 0 1; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self.sel = 0

    def compose(self):
        with Vertical(id="mw-box"):
            yield Static(id="mw-body")
            yield Static(id="mw-keys")

    def on_mount(self) -> None:
        self.counts = counts_all(self.app)
        self._draw()

    def _draw(self) -> None:
        t = Text(no_wrap=True)
        t.append("# Milestone classes", style=f"b {HEX['accent']}")
        t.append("  · every board · marks.json\n\n", style=HEX["dim"])
        for j, (k, m) in enumerate(CLS.items()):
            on, off = j == self.sel, k in HIDDEN
            r = Text(no_wrap=True)
            r.append("▶ " if on else "  ", style=HEX["accent"])
            r.append("[ ] " if off else "[x] ", style=HEX["dim"] if off else HEX["green"])
            r.append(m["shape"], style=HEX["dim"] if off else HEX[m["colour"]])
            r.append(f" {m['name']:<12}", style=HEX["dim"] if off else HEX["ink"])
            o, a = self.counts.get(k, (0, 0))
            r.append(f"{o:>2} open {a:>3} in all", style=HEX["mut"])
            r.append("   hidden: gantt + present" if off else "", style=HEX["amber"])
            if on:
                r.stylize("on #1d2a3a")
            t.append_text(r)
            t.append("\n")
        t.append("        ◆", style=HEX["mut"])
        t.append(" (no class)   the plain milestone\n", style=HEX["dim"])
        self.query_one("#mw-body", Static).update(t)
        self.query_one("#mw-keys", Static).update(key_line(
            [("↑↓", ""), ("␣", "hide/show"), ("↵", "only this"), ("n", "new"), ("e", "edit"),
             ("d", "delete"), ("esc", "close")], 72))

    def action_move(self, d: int) -> None:
        self.sel = max(0, min(len(CLS) - 1, self.sel + d))
        self._draw()

    def _cur(self) -> str:
        return list(CLS)[self.sel]

    def action_toggle(self) -> None:
        HIDDEN.symmetric_difference_update({self._cur()})
        self._draw()
        self.app.refresh_view()

    def action_only(self) -> None:
        HIDDEN.clear()
        HIDDEN.update(k for k in CLS if k != self._cur())
        self.app.refresh_view()
        self.dismiss(None)

    def action_new(self) -> None:
        self.app.push_screen(MarkForm(None))

    def action_edit(self) -> None:
        self.app.push_screen(MarkForm(self._cur()))

    def action_delete(self) -> None:
        pass          # the prototype shows the key; a y/n ConfirmModal would ask

    def action_close(self) -> None:
        self.dismiss(None)


# =============================================================================
# the app and the scenes
# =============================================================================
def sel(tid: str):
    def step(app):
        app.selected_task_id = tid
        app.refresh_view()
    return step


def push(factory):
    def step(app):
        app.push_screen(factory())
    return step


def typed(s: str) -> list[str]:
    return ["space" if ch == " " else "number_sign" if ch == "#" else ch for ch in s]


class Proto(TaskboardApp):
    BINDINGS = [Binding("number_sign", "marks", "", show=False),     # prototype: not in KEYMAP
                Binding("g", "group", "", show=False)]
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene: str, root: Path, seconds: float | None = None):
        sc = SCENES[scene]
        self.scene, self._steps, self._seconds = scene, sc["steps"], seconds
        self.played = False
        self._root = root
        fx.build(root, last=sc.get("last", "client-a"), marks=sc.get("enc") is not None)
        CLS.clear()
        for m in json.loads((root / "marks.json").read_text(encoding="utf-8"))["marks"]:
            CLS[m["id"]] = m
        ENC[0], LEGEND[0], GROUP[0] = sc.get("enc"), sc.get("legend"), False
        HIDDEN.clear()
        modals.TASK_KEYS[:] = EDIT_KEYS
        reg = Registry.load(root / "boards.json", root / "board.json")
        entry = reg.opening()
        reg.touch(entry.id, datetime.now())
        self._undo_patch = []
        patch = dict(sc.get("patch", {}))
        if ENC[0]:
            patch.update({(views, "c"): c_m, (views, "milestone_tone"): milestone_tone_m,
                          (views, "gantt_milestone_cells"): gantt_milestone_cells_m,
                          (views, "band_milestone_facts"): band_milestone_facts_m,
                          (views, "_agenda_row"): agenda_row_m,
                          (views, "_gantt_frame"): gantt_frame_m,
                          (views, "gantt_month_row"): gantt_month_row_m,
                          (views, "_present_ruler"): present_ruler_m,
                          (views, "present_tasks"): present_tasks_m,
                          (app_mod, "present_tasks"): present_tasks_m,
                          (views, "_gantt_legend"): gantt_legend_m,
                          (views, "legend_entries"): legend_entries_m,
                          (views, "matches"): matches_m, (views, "filter_bar"): filter_bar_m})
        for (mod, name), val in patch.items():
            self._undo_patch.append((mod, name, getattr(mod, name)))
            setattr(mod, name, val)
        super().__init__(board_path=entry.path, registry=reg, team_sync_interval=1e9)
        BOARD[0] = self.board

    def unpatch(self) -> None:
        for mod, name, val in reversed(self._undo_patch):
            setattr(mod, name, val)
        modals.TASK_KEYS[:] = EDIT_KEYS

    def check_action(self, action, parameters):
        if action == "marks":
            return ENC[0] is not None and len(self.screen_stack) == 1
        if action == "group":
            return (SCENES[self.scene].get("group_key", False) and self.view_mode == "gantt"
                    and len(self.screen_stack) == 1)
        return super().check_action(action, parameters)

    def action_marks(self) -> None:
        self.push_screen(MarksWindow())

    def action_group(self) -> None:
        GROUP[0] = not GROUP[0]
        self.refresh_view()

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
                                   f"view={self.view_mode} sel={self.selected_task_id}",
                                   encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)

    def check_state(self) -> bool:
        """What the scene must end on — a live run that ends elsewhere (a key lost
        while the window was starting) is reported BAD and shot again."""
        sc = SCENES[self.scene]
        want, view = sc.get("expect", "Screen"), sc.get("view")
        names = {type(s).__name__ for s in self.screen_stack[-1:]}
        if want == "SelectOverlay":
            return bool(self.screen.query("SelectOverlay")) and \
                self.screen.query_one("#f-mark").expanded
        return want in names and (view is None or self.view_mode == view)


TM = (app_mod, "TaskModal")
G = ["escape", "3"]                       # the gantt
K = ["escape", "4"]                       # the kanban
EDIT = ["escape", "1", sel("tc4"), "e"]   # the editor on "Index v1 delivered" (a Delivery)
SCENES: dict[str, dict] = {}


def scene(name, steps, **kw):
    SCENES[name] = dict(steps=steps, **kw)


# 1 · the encoding (D1): gantt + kanban, today and A/B/C
for _v in (None, "A", "B", "C"):
    _tag = _v or "now"
    scene(f"e-{_tag}-g", G + [sel("tc7")], enc=_v, view="gantt")
    scene(f"e-{_tag}-k", K + [sel("tc3")], enc=_v, view="kanban")
scene("glyphs", ["escape", push(GlyphSheet)], enc="B", expect="GlyphSheet")
# 2 · the editor and the manager
scene("ed-now", EDIT, expect="TaskModal")
scene("ed-A", EDIT + ["alt+m"], enc="B", patch={TM: EditorSelect}, expect="SelectOverlay")
scene("ed-B", EDIT + ["alt+m", "right"], enc="B", patch={TM: EditorSegment}, expect="EditorSegment")
scene("ed-C", EDIT + ["alt+m"], enc="B", patch={TM: EditorPicker}, expect="MarkPicker")
scene("ed-C-new", EDIT + ["alt+m"] + typed("Legal") + ["alt+n"], enc="B",
      patch={TM: EditorPicker}, expect="MarkForm")
scene("mg-list", G + [sel("tc7"), "number_sign", "down"], enc="B", expect="MarksWindow")
scene("mg-edit", G + [sel("tc7"), "number_sign", "down", "e", "alt+h", "right"], enc="B",
      expect="MarkForm")
# 3 · how it reads everywhere (B) and the legend
scene("rd-lanes", ["escape", "1", sel("tc7")], enc="B", view="swimlanes")
scene("rd-focus", ["escape", "5", sel("tc7")], enc="B", view="focus")
scene("rd-agenda", ["escape", "A"], enc="B", expect="AllBoardsAgenda")
scene("rd-now-agenda", ["escape", "A"], expect="AllBoardsAgenda")
scene("rd-pr1", G + [sel("tc9"), "R"], enc="B", expect="PresentScreen")
scene("rd-pr2", G + [sel("tc9"), "R", "2"], enc="B", expect="PresentScreen")
scene("rd-now-pr1", G + [sel("tc9"), "R"], expect="PresentScreen")
scene("lg-A", G + [sel("tc7"), "question_mark"], enc="B", legend="A", expect="HelpModal")
scene("lg-B", G + [sel("tc7")], enc="B", legend="B", view="gantt")
scene("lg-B-pr", G + [sel("tc9"), "R"], enc="B", legend="B", expect="PresentScreen")
scene("lg-C", G + [sel("tc7")], enc="B", legend="C", view="gantt")
scene("lg-C-pr", G + [sel("tc9"), "R"], enc="B", legend="C", expect="PresentScreen")
# 4 · filter and group by class
scene("f-A-res", G + ["slash"] + typed("#pay") + ["enter"], enc="B", view="gantt")
scene("f-B-win", G + [sel("tc7"), "number_sign", "down", "down", "space"], enc="B",
      expect="MarksWindow")
scene("f-B-res", G + [sel("tc7"), "number_sign", "down", "down", "space", "escape"], enc="B",
      view="gantt")
scene("f-B-pr", G + [sel("tc9"), "number_sign", "down", "down", "space", "escape", "R"],
      enc="B", expect="PresentScreen")
scene("f-C", G + [sel("tc7"), "g"], enc="B", group_key=True, view="gantt")


SIZES = [(118, 30), (80, 24)]


def _strip_font(svg: str) -> str:
    return re.sub(r"@font-face\s*\{[^}]*\}", "", svg)


async def _run(scene_name: str, size, fn) -> None:
    root = Path(tempfile.mkdtemp(prefix="ms-svg-"))
    app = Proto(scene_name, root)
    try:
        async with app.run_test(size=size) as pilot:
            for _ in range(200):
                if app.played:
                    break
                await pilot.pause(0.1)
            await pilot.pause(0.3)
            fn(app)
    finally:
        app.unpatch()
        shutil.rmtree(root, ignore_errors=True)


def svg_text(svg: str) -> str:
    """The plain characters of an exported SVG, row by row (for checking a frame)."""
    import html
    rows: dict[float, list] = {}
    for m in re.finditer(r'<text class="[^"]*" x="([\d.]+)" y="([\d.]+)"[^>]*>(.*?)</text>', svg):
        rows.setdefault(float(m.group(2)), []).append((float(m.group(1)), html.unescape(m.group(3))))
    out = []
    for y in sorted(rows):
        line = ""
        for x, s in sorted(rows[y]):
            line = line.ljust(int(round(x / 12.2))) + s
        out.append(line.replace("\xa0", " ").rstrip())
    return "\n".join(out)


def shot(names: list[str]) -> None:
    (OUT / "svg").mkdir(parents=True, exist_ok=True)
    for name in names or list(SCENES):
        for size in SIZES:
            def save(app, name=name, size=size):
                svg = app.export_screenshot(title=f"taskboard · {name} · {size[0]}x{size[1]}")
                (OUT / "svg" / f"{name}_{size[0]}x{size[1]}.svg").write_text(
                    _strip_font(svg), encoding="utf-8")
                ok = app.check_state()
                print("svg", name, size, "OK" if ok else
                      f"BAD {app.screen_stack!r} {app.view_mode}")
            asyncio.run(_run(name, size, save))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "shot":
        shot(args[1:])
    elif args and args[0] == "text":
        size = tuple(int(x) for x in (args[2] if len(args) > 2 else "118x30").split("x"))

        def dump(app):
            print(f"{[type(s).__name__ for s in app.screen_stack]} view={app.view_mode} "
                  f"ok={app.check_state()}")
            print(svg_text(app.export_screenshot()))
        asyncio.run(_run(args[1], size, dump))
    elif args and args[0] == "live":
        root = Path(tempfile.mkdtemp(prefix="ms-cap-"))
        try:
            Proto(args[1], root, float(args[2]) if len(args) > 2 else None).run()
        finally:
            shutil.rmtree(root, ignore_errors=True)
    else:
        print(__doc__)

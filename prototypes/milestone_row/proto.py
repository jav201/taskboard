"""THROWAWAY prototype — the milestone-row round: a project's milestones share
ONE gantt row instead of one row each.

    PYTHONUTF8=1 python prototypes/milestone_row/proto.py list
    PYTHONUTF8=1 python prototypes/milestone_row/proto.py text SCENE [WxH]   (plain dump)
    PYTHONUTF8=1 python prototypes/milestone_row/proto.py check              (widths + rows)
    python prototypes/milestone_row/proto.py live SCENE [SECONDS]            (a real terminal)

The REAL `TaskboardApp` (subclassed), on a real registry in a temporary folder,
driven by real key presses — the harness of `prototypes/milestone_marks/`.
Nothing under `taskboard/` changes. Two interception points:

- `views.gantt_plan` (THE seat both the renderer and `nav_model` read): a
  group's milestones leave its rows and ONE of them — the selected one, else the
  next open one — stands for the whole set (the "rep"). `↑↓` therefore reaches
  the shared row exactly once; the fold budget is recomputed with the new rows.
- `views._gantt_frame`: the rep's drawn line is replaced by the shared row
  (A), merged into the project's span row (B), or moved under the ruler as one
  lane for the whole gantt (C).

`←→` (`hmove`) is a no-op in today's gantt (its nav model is ONE column), so
the prototype gives it to the shared row: it walks the row's milestones by
date. Only the board's gantt (`done_rows=True`) changes; the presentation `R`
and the link mode are untouched (D1).
"""
from __future__ import annotations

import asyncio
import inspect
import json
import os
import shutil
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from taskboard import app as app_mod, models, modals, ribbon, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.models import (LINKS_MIGRATION, MILESTONES_MIGRATION, Board,  # noqa: E402
                              Project, Task, parse_iso)
from taskboard.views import HEX, c, fit, vis  # noqa: E402

TODAY = date(2026, 10, 20)     # a Tuesday, pinned


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        base = datetime(2026, 10, 20, 10, 30, 0)
        return base if tz is None else datetime(2026, 10, 20, 16, 30, 0, tzinfo=tz)


ribbon.datetime = _Now
app_mod.date = _Today
models.date = _Today
views.date = _Today

# =============================================================================
# the synthetic board: 3 projects + the Inbox (D2), one project with 5 milestones
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
CLASSES = [("delivery", "Delivery", "▲", "cyan"), ("payment", "Payment", "⬢", "amber"),
           ("review", "Review", "■", "violet"), ("launch", "Launch", "★", "pink")]
PROJECTS = [("pr", "Pilot rollout", "indigo", -14, 20),
            ("pe", "Eval harness", "blue", -7, 18),
            ("pd", "Docs & handover", "green", 0, 15)]
# id, project, title, phase, start, due, milestone, mark
TASKS = [
    ("m1", "pr", "Kickoff invoice paid", "Done", None, -3, True, "payment"),
    ("m2", "pr", "Rubric sign-off", "Review", None, -1, True, "review"),
    ("m3", "pr", "Steering go/no-go", "Next", None, 4, True, "review"),
    ("m4", "pr", "Store list frozen", "Next", None, 4, True, "delivery"),
    ("m5", "pr", "Pilot launch", "Backlog", None, 10, True, "launch"),
    ("store", "pr", "Pilot store list", "Doing", -3, 3, False, None),
    ("tele", "pr", "Pilot telemetry", "Doing", -5, 6, False, None),
    ("train", "pr", "Train store staff", "Next", 2, 8, False, None),
    ("rota", "pr", "Field support rota", "Backlog", 5, 12, False, None),
    ("g1", "pe", "Golden set frozen", "Next", None, 1, True, "delivery"),
    ("g2", "pe", "Eval report v1", "Backlog", None, 8, True, "review"),
    ("gq", "pe", "Golden question set", "Doing", -6, 0, False, None),
    ("gr", "pe", "Rubric tuning", "Next", 0, 5, False, None),
    ("gx", "pe", "Regression runs", "Backlog", 4, 12, False, None),
    ("h1", "pd", "Handover call", "Backlog", None, 15, True, None),
    ("ha", "pd", "API reference", "Next", 1, 9, False, None),
    ("hr", "pd", "Runbook draft", "Backlog", 6, 14, False, None),
    ("i1", None, "Insurance renewal", "Next", None, 6, True, "payment"),
    ("ip", None, "Renew passport", "Next", None, 2, False, None),
]


def _d(off):
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


def build(root: Path) -> Registry:
    projects = [Project(name=n, color=col, start_date=_d(s), due_date=_d(e), id=f"p{k}")
                for k, n, col, s, e in PROJECTS]
    tasks = [Task(title=title, project_id=(f"p{pk}" if pk else None), phase=ph,
                  priority="normal", start_date=_d(s), due_date=_d(d), milestone=ms,
                  mark=mark, phase_changed=(TODAY - timedelta(days=2)).isoformat(),
                  id=f"t{k}")
             for k, pk, title, ph, s, d, ms, mark in TASKS]
    settings = {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
                "seen_view_renumber_2026_07": True}
    Board(projects, tasks, root / "board.json", settings, PHASES).save()
    entry = {"id": "main", "name": "Client A", "color": "sky",
             "path": str((root / "board.json").resolve()),
             "last_opened": datetime.now().isoformat(timespec="minutes"), "archived": False}
    (root / "boards.json").write_text(json.dumps({"version": 1, "last": "main",
                                                  "boards": [entry]}), encoding="utf-8")
    (root / "marks.json").write_text(json.dumps(
        {"version": 1, "marks": [{"id": i, "name": n, "shape": s, "colour": k}
                                 for i, n, s, k in CLASSES]}, ensure_ascii=False),
        encoding="utf-8")
    return Registry.load(root / "boards.json", root / "board.json")


# =============================================================================
# the variant's plan: milestones leave the rows, one rep stands for the row
VAR: list[str | None] = [None]
LANE: dict[str, list[Task]] = {}         # rep id -> the milestones its row draws
_ORIG_PLAN = views.gantt_plan
_ORIG_FRAME = views._gantt_frame


def _key(t):
    return (parse_iso(t.due_date) or date.max, t.title)


def plan_m(board, show_archived, selected_id, today, body_rows, focus=None, previous=None,
           pinned=None, done_rows=False):
    if VAR[0] is None or not done_rows:              # presentation / link mode: as shipped
        return _ORIG_PLAN(board, show_archived, selected_id, today, body_rows, focus,
                          previous, pinned, done_rows)
    gs = _ORIG_PLAN(board, show_archived, selected_id, today, 10 ** 6, focus, previous,
                    pinned, done_rows)
    LANE.clear()

    def anchor(ms):
        hit = [t for t in ms if t.id == selected_id]
        opn = [t for t in ms if not board.is_done(t)]
        fut = [t for t in opn if (d := parse_iso(t.due_date)) and d >= today]
        return (hit or fut or opn or ms)[0]

    rest = [tuple(t for t in g.rows if not t.milestone) for g in gs]
    if VAR[0] in ("A", "B"):
        rows = []
        for g, r in zip(gs, rest):
            ms = sorted((t for t in g.rows if t.milestone), key=_key)
            if ms:
                rep = anchor(ms)
                LANE[rep.id] = ms
                r = (rep,) + r
            rows.append(r)
    else:                                            # C: one lane for the whole gantt
        rows = list(rest)
        ms = sorted((t for g in gs for t in g.rows if t.milestone), key=_key)
        if ms and rows:
            rep = anchor(ms)
            LANE[rep.id] = ms
            rows[0] = (rep,) + rows[0]
    # the fold budget, as `gantt_plan` spends it, on the new rows
    sel = board.task_by_id(selected_id) if selected_id else None
    sel_i = next((i for i, g in enumerate(gs) if sel is not None and sel in g.open + g.rest), None)
    pin_i = next((i for i, g in enumerate(gs)
                  if pinned is not None and views.group_key(g.project) == pinned), None)
    left, unfold = body_rows - len(gs), [False] * len(gs)
    for i in (sel_i, pin_i):
        if i is not None and not unfold[i]:
            unfold[i] = True
            left -= len(rows[i])

    def pressure(i):
        dues = [d for t in gs[i].open if (d := parse_iso(t.due_date))]
        return (previous is None or views.group_key(gs[i].project) != previous,
                -sum(1 for d in dues if d <= today), -sum(1 for d in dues if d == today),
                min(dues or [date.max]))

    for i in sorted((i for i in range(len(gs)) if i not in (sel_i, pin_i)), key=pressure):
        if rows[i] and len(rows[i]) <= left:
            unfold[i] = True
            left -= len(rows[i])
    return [g._replace(unfolded=unfold[i], rows=rows[i]) for i, g in enumerate(gs)]


# =============================================================================
# drawing the shared row
def _skey(style: str) -> str:
    """A reverse-video key for the selected mark (registered in the prototype only)."""
    k = f"sel-{style}"
    if k not in HEX:
        HEX[k] = f"reverse b {HEX[style]}"
    return k


def lane_cells(members, sel_id, board, ax, today, labels=True, base=None):
    """Each milestone's class mark on its date; two or more in one cell draw `◆2`
    (the selected one's glyph when it is among them); a reached one alone gets its
    `✓`. Then the labels: the selected one's title (after its mark, else before),
    the others' date — `▲Nd` when late — only where it fits whole."""
    W = ax.w
    cells = list(base) if base else [(" ", "dim")] * W
    buckets: dict[int, list[Task]] = {}
    for t in members:
        if (d := parse_iso(t.due_date)) is not None:
            buckets.setdefault(min(max(ax.cell(d), 0), W - 1), []).append(t)
    occ: set[int] = set()
    placed = []
    for x in sorted(buckets):
        ts = buckets[x]
        on = next((t for t in ts if t.id == sel_id), None)
        lead = on or ts[0]
        glyph, style, chip = views.milestone_mark(lead, board, today)
        seq = [(glyph, _skey(style) if on else style)]
        if len(ts) > 1:
            seq.append((str(len(ts)) if len(ts) < 10 else "+", "bright" if on else style))
        elif chip == "✓":
            seq.append(("✓", "reached"))
        x0 = min(x, W - len(seq))
        for i, s in enumerate(seq):
            cells[x0 + i] = s
            occ.add(x0 + i)
        placed.append((x0, x0 + len(seq), ts, lead, on))
    if not labels:
        return cells

    def room(a, step):         # free cells from a (exclusive) in direction step, gap kept
        n, i = 0, a + step
        while 0 <= i < W and i not in occ and (i + step < 0 or i + step >= W
                                                or i + step not in occ):
            n, i = n + 1, i + step
        return n

    def put(a, text, key):
        for i, ch in enumerate(text):
            cells[a + i] = (ch, key) if ch != " " else (" ", "gap")
            occ.add(a + i)

    for x0, x1, ts, lead, on in sorted(placed, key=lambda p: p[4] is None):
        if on is not None:
            text, key, need = on.title, "bright", 6
        else:
            _g, _s, chip = views.milestone_mark(lead, board, today)
            d = parse_iso(lead.due_date)
            text = chip if chip.startswith("▲") else models._md(d)
            key = ("over" if chip.startswith("▲") else "reached" if chip == "✓"
                   else "soon" if d == today else "mut")
            need = len(text)
        ra, rb = room(x1 - 1, 1) - 1, room(x0, -1) - 1      # one gap cell beside the mark
        if ra >= len(text):
            put(x1 + 1, text, key)
        elif rb >= len(text):
            put(x0 - 1 - len(text), text, key)
        elif max(ra, rb) >= need:                           # only a title is ever cut
            cut = fit(text, max(ra, rb))
            put(x1 + 1 if ra >= rb else x0 - 1 - len(cut), cut, key)
    return cells


def lane_label(members, sel_id, board, today, label_w, lead=" ", lead_key="mut"):
    on = next((t for t in members if t.id == sel_id), None)
    if on is not None:
        glyph, style, _chip = views.milestone_mark(on, board, today)
        same = [t for t in members if t.due_date == on.due_date]
        tag = f" {same.index(on) + 1}/{len(same)}" if len(same) > 1 else ""
        title = views.title_markup(on, max(1, label_w - 3 - len(lead) - len(tag)), True)
        return c(lead, lead_key) + c(glyph, style) + " " + title + c(tag, "mut") + " "
    late = sum(1 for t in members if views.milestone_mark(t, board, today)[2].startswith("▲"))
    n = len(members)
    text = f"{n} milestone{'s' if n != 1 else ''}" if label_w >= 24 else f"{n} ms"
    return (c(lead, lead_key) + c("◆", "mut") + " " + c(text, "mut")
            + (" " + c(f"▲{late}", "over") if late else ""))


def frame_m(board, show_archived, selected_id, today=None, width=68, height=0, line_map=None,
            tick=0, focus=None, previous=None, pinned_id=None, done_rows=False):
    if VAR[0] is None or not done_rows:
        return _ORIG_FRAME(board, show_archived, selected_id, today, width, height, line_map,
                           tick, focus, previous, pinned_id, done_rows)
    today = today or views.date.today()      # the pinned Tuesday
    w = views._clamp_width(width)
    label_w, chip_w, _fw = views.gantt_columns(w)
    adj = 0
    for _ in range(4):                    # spend the rows the shared row saved
        lm: dict[str, int] = {}
        lines, drawn, groups, ax = _ORIG_FRAME(board, show_archived, selected_id, today, width,
                                               (height + adj) if height else 0, lm, tick,
                                               focus, previous, pinned_id, done_rows)
        n0 = len(lines)
        lines = _post(lines, lm, groups, ax, board, show_archived, selected_id, today, w,
                      label_w, chip_w, tick)
        if not height or -(len(lines) - n0) == adj:
            break
        adj = -(len(lines) - n0)
    if line_map is not None:
        line_map.clear()
        line_map.update(lm)
    return lines, drawn, groups, ax


def _shift(lm, at, by):
    for k in list(lm):
        if lm[k] >= at:
            lm[k] += by


def _post(lines, lm, groups, ax, board, show_archived, sel_id, today, w, label_w, chip_w, tick):
    board = views._hide(board) if views._hidden_class_ids(board) else board
    guides, weekends = ax.guides(), ax.weekends()

    def row(label, cells, chip):
        out = views._pad(label, label_w) + " " + views._gantt_field(cells, ax, guides, weekends)
        return views._pad(out + (" " + chip if chip_w else ""), w)

    def chip_of(ms):
        on = next((t for t in ms if t.id == sel_id), None)
        nxt = on or next((t for t in ms if not board.is_done(t)
                          and (d := parse_iso(t.due_date)) and d >= today), None)
        return (views.gantt_milestone_chip(nxt, board, today, chip_w) if nxt
                else " " * chip_w)

    lines = list(lines)
    for rep_id, ms in list(LANE.items()):
        if VAR[0] == "A" and rep_id in lm:
            lines[lm[rep_id]] = row(lane_label(ms, sel_id, board, today, label_w),
                                    lane_cells(ms, sel_id, board, ax, today), chip_of(ms))
        elif VAR[0] == "B" and rep_id in lm:
            li = lm[rep_id]
            g = next(g for g in groups if g.rows and g.rows[0].id == rep_id)
            if g.project is not None:
                base = views._gantt_span(g.project, ax,
                                         board.project_progress(g.project.id, show_archived),
                                         tick)
                pchip = (views.gantt_due_chip(g.project.due_date, today, chip_w) if g.open
                         else " " * chip_w)
            else:
                base, pchip = None, " " * chip_w
            on = any(t.id == sel_id for t in ms)
            label = (lane_label(ms, sel_id, board, today, label_w, lead="▾ ",
                                lead_key=(g.project.color if g.project else "dim"))
                     if on else views._gantt_group_label(g, label_w))
            lines[li - 1] = row(label, lane_cells(ms, sel_id, board, ax, today, labels=False,
                                                  base=base), chip_of(ms) if on else pchip)
            del lines[li]
            lm.pop(rep_id)
            _shift(lm, li, -1)
            lm[rep_id] = li - 1
        elif VAR[0] == "C":
            if rep_id in lm:
                li = lm.pop(rep_id)
                del lines[li]
                _shift(lm, li, -1)
            at = 1 + views.GANTT_RULER_ROWS
            lines.insert(at, row(lane_label(ms, sel_id, board, today, label_w),
                                 lane_cells(ms, sel_id, board, ax, today), chip_of(ms)))
            _shift(lm, at, 1)
            lm[rep_id] = at
    return lines


# the width check: every line the gantt hands to the screen, measured
WIDEST: list[tuple[int, int]] = []        # (widest line, width)
_ORIG_TO_TEXT = views.to_text


def to_text_m(lines, height, w, *a, **k):
    from rich.text import Text
    WIDEST.append((max((Text.from_markup(x).cell_len for x in lines), default=0), w))
    return _ORIG_TO_TEXT(lines, height, w, *a, **k)


# =============================================================================
# the app and its scenes
def sel(tid: str):
    def step(app):
        app.selected_task_id = tid
        app.refresh_view()
    return step


def typed(s: str) -> list[str]:
    return ["space" if ch == " " else ch for ch in s]


class Proto(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene: str, root: Path, seconds: float | None = None):
        sc = SCENES[scene]
        self.scene, self._steps, self._seconds = scene, sc["steps"], seconds
        self.played, self._root = False, root
        reg = build(root)
        entry = reg.opening()
        reg.touch(entry.id, datetime.now())
        VAR[0] = sc["var"]
        self._undo = []
        for mod, name, val in ((views, "gantt_plan", plan_m), (views, "_gantt_frame", frame_m),
                               (views, "to_text", to_text_m)):
            self._undo.append((mod, name, getattr(mod, name)))
            setattr(mod, name, val)
        super().__init__(board_path=entry.path, registry=reg, team_sync_interval=1e9)

    def unpatch(self) -> None:
        for mod, name, val in reversed(self._undo):
            setattr(mod, name, val)

    def action_hmove(self, delta: int) -> None:
        """`←→` on a shared row walks its milestones by date (a no-op in today's gantt)."""
        t = self.selected_task
        if VAR[0] and self.view_mode == "gantt" and t is not None and t.milestone:
            for ms in LANE.values():
                ids = [m.id for m in ms]
                if t.id in ids:
                    self.selected_task_id = ids[max(0, min(len(ids) - 1,
                                                           ids.index(t.id) + delta))]
                    self.refresh_view()
                    return
        super().action_hmove(delta)

    def on_mount(self) -> None:
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
            Path(ready).write_text(f"{self._root}\n{'OK' if self.check_state() else 'BAD'} "
                                   f"{self.screen_stack!r} view={self.view_mode} "
                                   f"sel={self.selected_task_id}", encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)

    def check_state(self) -> bool:
        sc = SCENES[self.scene]
        names = {type(s).__name__ for s in self.screen_stack[-1:]}
        return (sc.get("expect", "Screen") in names and self.view_mode == "gantt"
                and (sc.get("sel") is None or self.selected_task_id == sc["sel"]))


G = ["escape", "3"]
SCENES: dict[str, dict] = {}


def scene(name, steps, var, **kw):
    SCENES[name] = dict(steps=steps, var=var, **kw)


scene("now", G + [sel("tm3")], None, sel="tm3")
scene("now-lr", G + [sel("tm3"), "right", "right"], None, sel="tm3")   # ←→: nothing moves
# per variant: the cursor on a task (the row at rest), ↑ onto the row, ← to the late
# one, → past the clash then ↵ (the details)
ANCHOR = {"A": "tm3", "B": "tm3", "C": "tg1"}
NEXT = {"A": "tm4", "B": "tm4", "C": "tm3"}
for v in ("A", "B", "C"):
    scene(f"{v}-rest", G + [sel("tstore")], v, sel="tstore")
    scene(f"{v}-sel", G + [sel("tstore"), "up"], v, sel=ANCHOR[v])
    scene(f"{v}-late", G + [sel("tstore"), "up", "left"], v, sel="tm2")
    scene(f"{v}-enter", G + [sel("tstore"), "up", "right", "enter"], v, sel=NEXT[v],
          expect="TaskDetails")
scene("A-find", G + ["slash"] + typed("store") + ["enter"], "A")

SIZES = [(118, 30), (80, 24)]


async def _run(name: str, size, fn) -> None:
    root = Path(tempfile.mkdtemp(prefix="mr-svg-"))
    app = Proto(name, root)
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
        VAR[0] = None
        shutil.rmtree(root, ignore_errors=True)


def svg_text(svg: str) -> str:
    """The plain characters of an exported SVG, row by row (the marks round's reader)."""
    import html
    import re
    rows: dict[float, list] = {}
    for m in re.finditer(r'<text class="[^"]*" x="([\d.]+)" y="([\d.]+)"[^>]*>(.*?)</text>', svg):
        rows.setdefault(float(m.group(2)), []).append((float(m.group(1)),
                                                       html.unescape(m.group(3))))
    out = []
    for y in sorted(rows):
        line = ""
        for x, s in sorted(rows[y]):
            line = line.ljust(int(round(x / 12.2))) + s
        out.append(line.replace(chr(160), " ").rstrip())
    return chr(10).join(out)


def body_rows(app) -> int:
    """The gantt's drawn rows under the ruler (span + task/milestone rows + lane)."""
    lm: dict[str, int] = {}
    lines, _d, groups, _ax = views._gantt_frame(app.board, False, app.selected_task_id,
                                                TODAY, 118, 0, lm, 0, None, None, None, True)
    return len(lines) - 1 - views.GANTT_RULER_ROWS - (1 if views.legend_strip(app.board, 118)
                                                      else 0)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "text":
        size = tuple(int(x) for x in (args[2] if len(args) > 2 else "118x30").split("x"))

        def dump(app):
            print(f"{[type(s).__name__ for s in app.screen_stack]} sel={app.selected_task_id} "
                  f"ok={app.check_state()}")
            print(svg_text(app.export_screenshot()))
        asyncio.run(_run(args[1], size, dump))
    elif args and args[0] == "check":
        for name in (args[1:] or list(SCENES)):
            for size in SIZES:
                def chk(app, name=name, size=size):
                    wide = max((x for x, _w in WIDEST), default=0)
                    print(f"{name:9} {size[0]}x{size[1]} ok={app.check_state()} "
                          f"widest={wide}/{size[0]} {'OVERFLOW' if wide > size[0] else ''}"
                          f" rows={body_rows(app) if size == (118, 30) else ''}")
                WIDEST.clear()
                asyncio.run(_run(name, size, chk))
    elif args and args[0] == "live":
        root = Path(tempfile.mkdtemp(prefix="mr-cap-"))
        try:
            Proto(args[1], root, float(args[2]) if len(args) > 2 else None).run()
        finally:
            shutil.rmtree(root, ignore_errors=True)
    else:
        print(__doc__)

"""Fixture MR-F — the milestone-row round's synthetic board (Inc MR-a).

Copied from `prototypes/milestone_row/proto.py:70-99` so no test imports a
prototype. Three projects and the Inbox; *Pilot rollout* holds five milestones
(m1 reached, m2 late, m3 + m4 the same day, m5). Every name and date is
synthetic; TODAY is pinned (a Tuesday). Ids are `t<key>`.

Two ways in:
- `board()` — a `Board` in memory with the class directory on `board.marks`
  (layer 0: `render_gantt`, `_gantt_frame`, `gantt_plan`, `nav_model`);
- `build(root)` — a REAL registry (`boards.json` + `marks.json`) for the app,
  read by the shipped `open_app` (black box, through keys).
"""
from __future__ import annotations

import json
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from pathlib import Path

from taskboard.marks import Mark
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, Board, Project, Task

TODAY = date(2026, 10, 20)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
# id, name, shape, hollow twin, colour key (views.HEX)
CLASSES = [("delivery", "Delivery", "▲", "△", "cyan"),
           ("payment", "Payment", "⬢", "⬡", "amber"),
           ("review", "Review", "■", "□", "violet"),
           ("launch", "Launch", "★", "☆", "pink")]
PROJECTS = [("pr", "Pilot rollout", "indigo", -14, 20),
            ("pe", "Eval harness", "blue", -7, 18),
            ("pd", "Docs & handover", "green", 0, 15)]
# key, project, title, phase, start, due, milestone, mark
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
PILOT_MS = ["tm1", "tm2", "tm3", "tm4", "tm5"]          # walk order


def d(off):
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


def settings() -> dict:
    return {"migrations": {"links": LINKS_MIGRATION, "milestones": MILESTONES_MIGRATION},
            "seen_view_renumber_2026_07": True}


def tasks(rows=TASKS) -> list[Task]:
    return [Task(title=title, project_id=(f"p{pk}" if pk else None), phase=ph,
                 priority="normal", start_date=d(s), due_date=d(due), milestone=ms,
                 mark=mark, phase_changed=(TODAY - timedelta(days=2)).isoformat(),
                 id=f"t{k}")
            for k, pk, title, ph, s, due, ms, mark in rows]


def projects() -> list[Project]:
    return [Project(name=n, color=col, start_date=d(s), due_date=d(e), id=f"p{k}")
            for k, n, col, s, e in PROJECTS]


def marks(hidden=()) -> dict:
    return {cid: Mark(cid, n, s, k, hidden=(cid in hidden)) for cid, n, s, _h, k in CLASSES}


def task(key, project, title, phase, start, due, ms=False, mark=None, deps=()) -> Task:
    """One synthetic task in MR-F's shape (`project` a key such as "pr", or None)."""
    return Task(title=title, project_id=(f"p{project}" if project else None), phase=phase,
                priority="normal", start_date=d(start), due_date=d(due), milestone=ms,
                mark=mark, depends_on=[f"t{x}" for x in deps],
                phase_changed=(TODAY - timedelta(days=2)).isoformat(), id=f"t{key}")


def project(key, name, colour="sky", start=-5, due=20) -> Project:
    return Project(name=name, color=colour, start_date=d(start), due_date=d(due), id=f"p{key}")


def board(path: Path | None = None, extra=(), hidden=(), rows=TASKS, extra_projects=()) -> Board:
    """MR-F in memory. `extra` appends Task objects, `extra_projects` Project
    objects; `hidden` hides class ids."""
    b = Board(projects() + list(extra_projects), tasks(rows) + list(extra),
              path or Path("mrf.json"), settings(), PHASES)
    b.marks = marks(hidden)
    return b


def build(root: Path, extra=(), rows=TASKS, extra_projects=(), base_projects=True) -> Path:
    """MR-F as a real registry under `root` (the app's `~/.taskboard`)."""
    root.mkdir(parents=True, exist_ok=True)
    b = Board((projects() if base_projects else []) + list(extra_projects), tasks(rows) + list(extra),
              root / "board.json", settings(), PHASES)
    b.save()
    entry = {"id": "main", "name": "Client A", "color": "sky",
             "path": str((root / "board.json").resolve()),
             "last_opened": datetime.now().isoformat(timespec="minutes"), "archived": False}
    reg = root / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": "main", "boards": [entry]}),
                   encoding="utf-8")
    (root / "marks.json").write_text(json.dumps(
        {"version": 1, "marks": [{"id": i, "name": n, "shape": s, "colour": k}
                                 for i, n, s, _h, k in CLASSES]}, ensure_ascii=False),
        encoding="utf-8")
    return reg


# =============================================================================
# reading a frame — observable output only (plain cells, per-cell style)
# =============================================================================
from rich.cells import cell_len  # noqa: E402
from rich.console import Console  # noqa: E402

from taskboard import views  # noqa: E402
from taskboard.models import parse_iso  # noqa: E402

_CON = Console(width=400, color_system="truecolor", force_terminal=True)
#: the field's ground: blank, the dotted ground and the guides (`┆` week, `╎` today, `┃` month)
GROUND = frozenset(" ·┆╎┃│╯╰╭╮")
MARKS = views.MARK_GLYPHS
HEX = {k: v.lower() for k, v in views.HEX.items()}


def cells_of(line: str) -> list[str]:
    """A line as terminal cells: a wide glyph fills two (the second is ""),
    a zero-width mark joins the cell before it."""
    out: list[str] = []
    for ch in line:
        w = cell_len(ch)
        if w == 0 and out:
            out[-1] += ch
        elif w == 2:
            out += [ch, ""]
        else:
            out.append(ch)
    return out


def norm(cells) -> str:
    """Field cells as text with every ground glyph read as one blank."""
    return "".join(" " if ch in GROUND else ch for ch in cells)


def hexof(st) -> str | None:
    return (st.color.triplet.hex.lower()
            if st is not None and st.color is not None and st.color.triplet else None)


class Frame:
    """One board-gantt frame through the shipped seat `render_gantt` (the app's
    painter), plus `_gantt_frame`'s facts for the same arguments."""

    def __init__(self, b, sel, W=118, H=30):
        self.b, self.sel, self.W, self.H = b, sel, W, H
        self.lm: dict = {}
        self.text = views.render_gantt(b, False, sel, TODAY, W, H, self.lm)
        self.lines = self.text.plain.split("\n")
        self._tl = self.text.split("\n", allow_blank=True)
        _l, self.drawn, self.groups, self.ax = views._gantt_frame(
            b, False, sel, TODAY, W, H, {}, done_rows=True)
        self.label_w, self.chip_w, _fw = views.gantt_columns(W)
        self.x0 = self.label_w + 1

    # -- geometry ------------------------------------------------------------
    def cells(self, i):
        return cells_of(self.lines[i])

    def fcells(self, i):
        return self.cells(i)[self.x0:self.x0 + self.ax.w]

    def ftext(self, i):
        return norm(self.fcells(i))

    def label(self, i):
        return "".join(self.cells(i)[:self.label_w])

    def gutter(self, i):
        return self.cells(i)[self.label_w]

    def chip(self, i):
        return "".join(self.cells(i)[len(self.cells(i)) - self.chip_w:]).strip()

    def cell(self, key):
        """The field cell of task `key`'s due (`ax.cell`)."""
        return self.ax.cell(parse_iso(self.b.task_by_id(key).due_date))

    def spans(self):
        return [i for i, ln in enumerate(self.lines) if ln[:2] in ("▾ ", "▸ ")]

    def span_of(self, name):
        return next(i for i, ln in enumerate(self.lines)
                    if ln[:2] in ("▾ ", "▸ ") and ln[2:].startswith(name[:10]))

    def lane_line(self, ids):
        """THE one line every id of a lane maps to in `line_map` (SEAM-9)."""
        got = {i: self.lm.get(i) for i in ids}
        assert len(set(got.values())) == 1 and None not in got.values(), (
            f"the lane is not one row: line_map {got}")
        return next(iter(got.values()))

    # -- style ---------------------------------------------------------------
    def style(self, i, x):
        """The Style painted at cell `x` of line `i`."""
        line, cx = self._tl[i], 0
        for j, ch in enumerate(line.plain):
            w = cell_len(ch)
            if w == 0:
                continue
            if cx == x:
                return line.get_style_at_offset(_CON, j)
            cx += w
        raise IndexError(x)

    def fstyle(self, i, f):
        return self.style(i, self.x0 + f)


def painted(app) -> list[list[tuple[str, str | None, bool]]]:
    """The app's screen as (char, foreground hex, reverse) per cell."""
    rows = []
    for s in app.screen._compositor.render_strips(app.screen.size):
        cells = []
        for seg in s:
            st = seg.style
            cells += [(ch, hexof(st), bool(st is not None and st.reverse)) for ch in seg.text]
        rows.append(cells)
    return rows


def screen(app) -> list[str]:
    return ["".join(ch for ch, _h, _r in r) for r in painted(app)]


# =============================================================================
# driving the real app through keys
# =============================================================================
@asynccontextmanager
async def gantt(home, size=(118, 30), sel="tstore", hidden=(), **kw):
    """The real app on MR-F (plus `kw` for `build`), in the gantt, `sel` selected."""
    build(home, **kw)
    from taskboard.__main__ import open_app
    app = open_app(None)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("escape")                  # the home
        await pilot.press("3")                       # the gantt
        await pilot.pause()
        for cid in hidden:                           # `#`: the class manager
            await hide_class(pilot, cid)
        if sel is not None:
            app.selected_task_id = sel
            app.refresh_view()
            await pilot.pause()
        yield app, pilot


async def hide_class(pilot, cid):
    await pilot.press("number_sign")
    await pilot.pause()
    for _ in range([c[0] for c in CLASSES].index(cid)):
        await pilot.press("down")
    await pilot.press("space")
    await pilot.press("escape")
    await pilot.pause()


async def keys(pilot, *ks):
    for k in ks:
        await pilot.press(k)
    await pilot.pause()



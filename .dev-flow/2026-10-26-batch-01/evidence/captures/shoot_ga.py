"""Real-app captures of batch 2026-10-26-batch-01 — the SHIPPED `TaskboardApp` at
f4b53cc (done work keeps its gantt row; only archiving hides it), unpatched, in
real Windows Terminal windows. Method inherited from batch 2026-10-21-batch-01's
`shoot_real.py`: the window is selected by its unique `ga-*` title, PrintWindow,
full colour, closed right after its shot; nothing is patched except the scene's
calendar date and the suite's milestone-offer seam (the app module's own
`milestones_marked` reference answers True, as tests/conftest.py does).

Scenes / fixtures (all dates relative to the pinned TODAY = 2026-10-26):

- `gantt`  — the ga-mix board: Website (2 open, 2 done, 1 done+ARCHIVED),
  Mobile (1 open, 1 done), Ops & Security (3 done, no open work), one loose
  Inbox task. Proves G1/G2: done rows visible and quiet, archived task no row.
- `busy`   — the ga-busy board: 8 projects x (2 open + 3 done). At 80x24 the
  done rows consume fold room (G3).
- `busyoff`— the same ga-busy board with every done task archived: the fold a
  flag-off seat (pre-change G-A) would give; the capture-adjacent note
  `busy_flagoff_80x24.txt` is the exact same frame rendered by
  `_gantt_frame(..., done_rows=False)`.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
HOME = Path(tempfile.mkdtemp(prefix="ga-cap-"))
Path.home = classmethod(lambda cls: HOME)

from taskboard import app as app_mod, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.models import Board, Project, Task  # noqa: E402

TODAY = date(2026, 10, 26)
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]
SETTINGS = {"wip_limits": {"Doing": 4, "Review": 3}, "migrations": {"links": 1}}


class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


for _m in (app_mod, models, views, modals):
    _m.date = _Today
app_mod.milestones_marked = lambda settings: True      # the conftest seam


def _d(off: int | None) -> str | None:
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


# (key, name, color, status, start_off, due_off)
MIX_PROJECTS = [
    ("web", "Website Redesign", "violet", "on_track", -40, 10),
    ("mob", "Mobile App", "sky", "on_track", -20, 35),
    ("ops", "Ops & Security", "rose", "on_track", -60, 5),
]
# (key, project|None, title, phase, prio, start_off, due_off, done_days_ago, archived)
MIX_TASKS = [
    ("w3", "web", "Fix checkout 500 error", "Doing", "high", -6, -2, None, False),
    ("w4", "web", "Optimize image assets", "Next", "low", None, 6, None, False),
    ("w1", "web", "Design homepage mockups", "Done", "normal", -38, -20, 3, False),
    ("w2", "web", "Build component library", "Done", "normal", -25, -3, 1, False),
    ("w9", "web", "Old promo landing page", "Done", "low", -60, -40, 60, True),
    ("m3", "mob", "Add push notifications", "Next", "normal", 1, 12, None, False),
    ("m1", "mob", "Set up CI pipeline", "Done", "normal", -20, -12, 2, False),
    ("o1", "ops", "Renew TLS certificate", "Done", "high", -4, -1, 1, False),
    ("o2", "ops", "Rotate API keys", "Done", "high", -3, 0, 4, False),
    ("o3", "ops", "Review pull requests", "Done", "normal", -2, 1, 0, False),
    ("x1", None, "Tidy inbox notes", "Doing", "normal", None, 2, None, False),
]

BUSY_PROJECTS = [
    ("web", "Website Redesign", "violet", "on_track", -40, 10),
    ("mob", "Mobile App", "sky", "on_track", -20, 35),
    ("api", "API Platform", "lime", "at_risk", -30, 21),
    ("dwh", "Data Warehouse", "amber", "on_track", -10, 60),
    ("ops", "Ops & Security", "rose", "on_track", -60, 5),
    ("bil", "Billing", "cyan", "on_track", -25, 40),
    ("doc", "Docs Portal", "pink", "on_track", -15, 30),
    ("res", "Research", "green", "paused", -50, 70),
]
# 8 projects x (2 open + 3 done); done phase_changed 1..5 days ago
BUSY_TASKS = []
_OPEN = [("Scope the work", "Next", "high", None, 4),
         ("Draft the first pass", "Doing", "normal", -3, 9),
         ("Ship the change", "Next", "normal", 2, 14)]
_DONE_TITLES = ["Write the plan", "Review with the team", "Close the loop"]
for _pi, (pk, _name, _c, _s, _ps, _pd) in enumerate(BUSY_PROJECTS):
    BUSY_TASKS.append((f"{pk}a", pk, _OPEN[_pi % 3][0], _OPEN[_pi % 3][1],
                       _OPEN[_pi % 3][2], _OPEN[_pi % 3][3], _OPEN[_pi % 3][4],
                       None, False))
    BUSY_TASKS.append((f"{pk}b", pk, _OPEN[(_pi + 1) % 3][0], _OPEN[(_pi + 1) % 3][1],
                       _OPEN[(_pi + 1) % 3][2], _OPEN[(_pi + 1) % 3][3],
                       _OPEN[(_pi + 1) % 3][4], None, False))
    for _di, _t in enumerate(_DONE_TITLES):
        BUSY_TASKS.append((f"{pk}d{_di}", pk, f"{_t} ({_name.split()[0]})", "Done",
                           "normal", -30 + _di * 3, -18 + _di * 3, 1 + _di, False))


def _board(projects, tasks, path: Path) -> Board:
    projs = {k: Project(name=n, color=c, status=s, start_date=_d(a), due_date=_d(d),
                        id=f"p{k}")
             for k, n, c, s, a, d in projects}
    ts = []
    for key, pk, title, phase, prio, s, d, age, arch in tasks:
        ts.append(Task(title=title, project_id=projs[pk].id if pk else None,
                       phase=phase, priority=prio, start_date=_d(s), due_date=_d(d),
                       archived=arch,
                       phase_changed=(TODAY - timedelta(days=age)).isoformat()
                                     if age is not None else None,
                       id=f"t{key}"))
    return Board(list(projs.values()), ts, path, dict(SETTINGS), PHASES)


def build(name: str) -> Shot:      # noqa: F821 (defined below)
    root = HOME / ".taskboard"
    root.mkdir(parents=True, exist_ok=True)
    if name in ("gantt",):
        board = _board(MIX_PROJECTS, MIX_TASKS, root / "ga-mix.json")
    elif name == "busyoff":
        # the same board with its DONE work archived: done rows and the span's
        # ✓n both leave, open work untouched — the fold a flag-off seat gives
        board = _board(BUSY_PROJECTS,
                       [(*t[:8], t[8] or t[3] == "Done") for t in BUSY_TASKS],
                       root / "ga-busy.json")
    else:                                   # "busy"
        board = _board(BUSY_PROJECTS, BUSY_TASKS, root / "ga-busy.json")
    board.save()
    (root / "people.json").write_text(json.dumps({"version": 1, "people": []}),
                                      encoding="utf-8")
    reg = root / "boards.json"
    reg.write_text(json.dumps({"version": 1, "last": "ga",
                               "boards": [{"id": "ga", "name": "ga capture",
                                           "color": "violet",
                                           "path": str(board.path.resolve()),
                                           "last_opened": datetime.now().isoformat(
                                               timespec="minutes"),
                                           "archived": False}]}, indent=2),
                   encoding="utf-8")
    registry = Registry.load(reg, root / "main.json")
    entry = registry.opening()
    registry.touch(entry.id, datetime.now())
    return Shot(name, SCENES[name], board_path=entry.path, registry=registry)


class Shot(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, name: str, scene: dict, **kw):
        self._name, self._want = name, scene["want"]
        self._seconds = None
        super().__init__(team_sync_interval=1e9, **kw)

    def on_mount(self) -> None:
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.2, lambda: self.run_worker(self._play()))

    async def _play(self) -> None:
        for k in ["escape", "3"]:
            await self._press_keys([k])
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.8)
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            ok = type(self.screen).__name__ == self._want \
                and self.view_mode == "gantt"
            Path(ready).write_text(f"{HOME}\n{'OK' if ok else 'BAD'} "
                                   f"{type(self.screen).__name__} "
                                   f"view={self.view_mode} "
                                   f"board={self.board_id}",
                                   encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


SCENES = {
    "gantt": dict(want="Screen"),
    "busy": dict(want="Screen"),
    "busyoff": dict(want="Screen"),
}


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "live":
        app = build(args[1])
        app._seconds = float(args[2]) if len(args) > 2 else None
        try:
            app.run()
        finally:
            shutil.rmtree(HOME, ignore_errors=True)
    else:
        print(__doc__)

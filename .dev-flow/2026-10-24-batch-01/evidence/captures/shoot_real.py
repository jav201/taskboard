"""Real-app captures of batch 2026-10-24-batch-01 — the SHIPPED `TaskboardApp`, unpatched.

    python .dev-flow/2026-10-24-batch-01/evidence/captures/shoot_real.py list
    python .dev-flow/2026-10-24-batch-01/evidence/captures/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot.ps1` (the people round's capture
method: the window selected by its unique title, PrintWindow, full colour, closed
right after its shot). The subclass below only sets the window title, plays the
scene's keys through the app's own key path (`App._press_keys`) and reports the
screen it ended on: no screen, render or behaviour is replaced. The round's
synthetic boards and classes (`tests/milestone_marks_fixture.py`) live in a
temporary folder that stands in for the home; the calendar is the round's
(Tuesday 2026-10-20). Nothing touches the real home.
"""
from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
HOME = Path(tempfile.mkdtemp(prefix="m01-cap-"))
Path.home = classmethod(lambda cls: HOME)

import milestone_marks_fixture as fx  # noqa: E402
from taskboard import app as app_mod, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


for _m in (app_mod, models, views, modals):
    _m.date = _Today


def sel(tid: str):
    def step(app):
        app.selected_task_id = tid
        app.refresh_view()
    return step


class Shot(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, name: str, scene: dict, **kw):
        self._name, self._steps, self._want = name, scene["keys"], scene["want"]
        self._seconds = None
        super().__init__(team_sync_interval=1e9, **kw)

    def on_mount(self) -> None:           # before TaskboardApp.on_mount (MRO dispatch)
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.2, lambda: self.run_worker(self._play()))

    async def _play(self) -> None:
        for k in self._steps:
            if isinstance(k, str):
                await self._press_keys([k])
            else:
                k(self)
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.8)
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            ok = type(self.screen).__name__ == self._want
            Path(ready).write_text(f"{HOME}\n{'OK' if ok else 'BAD'} {type(self.screen).__name__} "
                                   f"board={self.board_id} sel={self.selected_task_id}",
                                   encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


SCENES = {
    # 1 — the gantt of Client A: classed milestones by the seat (late ■ over + ▲2d,
    # reached hollow △ + ✓, unclassified ◆ in mut) + the legend strip under the ruler
    "gantt": dict(keys=["escape", "3"], want="Screen"),
    # 2 — `#`: the manager with the four classes, counts, the `␣ hide/show` key row
    "manager": dict(keys=["escape", "number_sign"], want="MarksManager"),
    # 3 — `n` from the manager: the form (name field, shape row, colour row, key line)
    "form": dict(keys=["escape", "number_sign", "n"], want="MarkForm"),
    # 4 — `e` on a classed milestone (Index v1 delivered · delivery), `alt+m` opens
    # the class Select after #f-milestone
    "editor": dict(keys=["escape", sel("tc4"), "e", "alt+m"], want="TaskModal"),
    # 5 — `␣` on Payment in the manager, `#` closes, the gantt again: Payment gone,
    # the strip names the drawn classes + `1 hidden`
    "hidden": dict(keys=["escape", "number_sign", "down", "space",
                         "number_sign", "3"], want="Screen"),
    # 6 — `/`, `#pay`, enter in the kanban: the class bar + only Payment's milestones
    "search": dict(keys=["escape", "4", "slash", "#", "p", "a", "y", "enter"],
                   want="Screen"),
    # 7 — the presentation (view 1) of Pilot rollout (payment + review + launch
    # milestones): the strip under its ruler
    "present": dict(keys=["escape", sel("tc9"), "R", "1"], want="PresentScreen"),
}


def build(name: str) -> Shot:
    root = HOME / ".taskboard"
    fx.build(root, last="client-a")
    reg = Registry.load(root / "boards.json", root / "board.json")
    entry = reg.opening()
    reg.touch(entry.id, datetime.now())
    return Shot(name, SCENES[name], board_path=entry.path, registry=reg)


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

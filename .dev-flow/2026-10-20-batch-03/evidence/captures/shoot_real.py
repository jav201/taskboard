"""Real-app captures of batch 2026-10-20-batch-03 — the SHIPPED `TaskboardApp`, unpatched.

    python .dev-flow/2026-10-20-batch-03/evidence/captures/shoot_real.py list
    python .dev-flow/2026-10-20-batch-03/evidence/captures/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot_real.ps1` (the round's capture method:
the window selected by title, PrintWindow, full colour). The subclass below only sets
the window title, plays the scene's keys through the app's own key path and exits on a
timer: no screen, render or behaviour is replaced. The round's synthetic boards
(`tests/backlog_round_fixture.py`) live in a temporary folder that stands in for the
home; the calendar is the round's (Tuesday 2026-10-20). Nothing touches the real home.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
HOME = Path(tempfile.mkdtemp(prefix="b03-cap-"))
Path.home = classmethod(lambda cls: HOME)

import backlog_round_fixture as fx  # noqa: E402
import kg_board  # noqa: E402
from taskboard import app as app_mod, boards, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.models import Board  # noqa: E402


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


for _m in (app_mod, models, views, modals):
    _m.date = _Today


def build(scene: dict) -> TaskboardApp:
    root = HOME / ".taskboard"
    fx.build(root, last=scene.get("last", "client-a"), offer=scene.get("offer", False))
    if scene.get("team"):
        team = HOME / "team"
        team.mkdir()
        cfg = dict(kg_board.TEAM, roster=[{"id": "u1", "name": "username_subject", "hue": "sky"},
                                          {"id": "u2", "name": "Teammate B", "hue": "amber"}])
        (team / "team.json").write_text(json.dumps(cfg), encoding="utf-8")
        b = Board.load(fx.board_path(root, "client-a"))
        b.settings["team_shared_dir"] = str(team)
        b.save()
    if scene.get("twice"):          # another window's marker, as that window writes it
        boards.announce(fx.board_path(root, "client-a"), datetime(2026, 10, 20, 9, 12))
    reg = Registry.load(root / "boards.json", root / "board.json")
    if scene.get("unlisted"):
        return Shot(scene, board_path=fx.copy_path(root), registry=reg)
    entry = reg.opening()
    reg.touch(entry.id, datetime.now())
    return Shot(scene, board_path=entry.path, registry=reg)


class Shot(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, scene: dict, **kw):
        self._steps, self._seconds, self.played = scene["keys"], None, False
        super().__init__(team_sync_interval=1e9, **kw)

    def on_mount(self) -> None:           # before TaskboardApp.on_mount (MRO dispatch)
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.set_timer(1.2, lambda: self.run_worker(self._play()))

    async def _play(self) -> None:
        for k in self._steps:
            await self._press_keys([k])
            await asyncio.sleep(0.35)
        await asyncio.sleep(0.8)
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            Path(ready).write_text(f"ready {self.screen_stack!r}", encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


SCENES = {
    # item 1 — the agenda (from the home), and its `enter` onto Client A
    "agenda": dict(keys=["A"]),
    "agenda-open": dict(keys=["A", "down", "enter"]),
    # items 2, 3, 5 — the presentation on Client A
    "present-chip": dict(keys=["escape", "R"]),
    "present-keys": dict(keys=["escape", "R", "3", "question_mark"]),
    "present-kj": dict(keys=["escape", "R", "3", "down", "K"]),
    # item 4 — `x` in view 3 (the export file itself is copied beside the captures)
    "present-export": dict(keys=["escape", "R", "3", "x"]),
    # item 6 and the objection — every kind of modal key line
    "confirm": dict(keys=["left", "x"]),
    "move-confirm": dict(keys=["escape", "P", "down", "m", "enter"]),
    "task-editor": dict(keys=["escape", "a"]),
    "project-form": dict(keys=["escape", "p"]),
    "clocks": dict(keys=["escape", "c"]),
    # item 7 — the start-up modals
    "offer": dict(keys=[], offer=True),
    "identity": dict(keys=[], team=True),
    # item 8 — a board another window holds
    "twice": dict(keys=["escape"], twice=True),
    # item 9 — `--open`
    "open": dict(keys=[], unlisted=True),
}


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "live":
        scene = SCENES[args[1]]
        app = build(scene)
        app._seconds = float(args[2]) if len(args) > 2 else None
        app.run()
        out = os.environ.get("CAPTURE_EXPORT_DIR")
        if out:
            for f in (HOME / ".taskboard" / "boards" / "client-a" / "reports").glob("present-*-all.*"):
                shutil.copyfile(f, Path(out) / f"{args[1]}-file_{os.environ.get('CAPTURE_SIZE', '')}{f.suffix}")
        shutil.rmtree(HOME, ignore_errors=True)
    else:
        print(__doc__)

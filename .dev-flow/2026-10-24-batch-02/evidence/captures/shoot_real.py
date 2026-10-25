"""Real-app captures of batch 2026-10-24-batch-02 — the SHIPPED `TaskboardApp`, unpatched.

    python .dev-flow/2026-10-24-batch-02/evidence/captures/shoot_real.py list
    python .dev-flow/2026-10-24-batch-02/evidence/captures/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot.ps1` (batch 2026-10-24-batch-01's
capture method: the window selected by its unique title, PrintWindow, full
colour, closed right after its shot). The subclass below only sets the window
title, plays the scene's keys through the app's own key path
(`App._press_keys`) and reports the screen it ended on: no screen, render or
behaviour is replaced. The multi-board round's synthetic boards
(`tests/multi_board_fixture.py`) trimmed to two boards live in a temporary
folder that stands in for the home; the calendar and the clock are pinned to
the fixtures' Tuesday 2026-10-20 09:30 (the house pattern of
`tests/test_home_deferred_start.py`). Nothing touches the real home.
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
HOME = Path(tempfile.mkdtemp(prefix="h01-cap-"))
Path.home = classmethod(lambda cls: HOME)

import multi_board_fixture as mb  # noqa: E402
from taskboard import app as app_mod, boards as boards_mod, models, modals, views  # noqa: E402
from taskboard.app import BoardsHome, TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.models import Board, Task  # noqa: E402

NOW = datetime(2026, 10, 20, 9, 30)


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


for _m in (app_mod, models, views, modals):
    _m.date = _Today
app_mod.datetime = _Now

OPEN_TWICE = "Boards · open twice"
ARCHIVED = "Archived old work"


class Shot(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, name: str, scene: dict, **kw):
        self._name, self._steps, self._want = name, scene["keys"], scene["want"]
        self._check = scene["check"]
        self._seconds = None
        self._before: bytes = b""
        self._default: Path | None = None
        self._foreign: Path | None = None
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
        reason = None
        if type(self.screen).__name__ != self._want:
            reason = f"screen {type(self.screen).__name__} != {self._want}"
        elif self._check is not None:
            reason = self._check(self)
        ready = os.environ.get("PROTO_READY_FILE")
        if ready:
            Path(ready).write_text(
                f"{HOME}\n{'OK' if reason is None else 'BAD ' + reason} "
                f"{type(self.screen).__name__} board={self.board_id} "
                f"sel={self.selected_task_id} toasts={len(self._notifications)}",
                encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


# ---- per-scene end-state checks (None = the scene holds) -------------------- #
def _check_home(app: Shot) -> str | None:
    """AT-2701: the quiet home — no modal, no toast, the default board's bytes
    untouched by the start, and this window wrote no presence marker."""
    if app._notifications:
        return f"{len(app._notifications)} toast(s) at the home"
    if app._default.read_bytes() != app._before:
        return "the default board's bytes changed at the home"
    mine = [m for m in _markers_for(app._default) if app._foreign is None or m != app._foreign.name]
    if mine:
        return f"a presence marker of this window exists: {mine}"
    return None


def _check_offer(app: Shot) -> str | None:
    """AT-2705: the offer is the top screen and the home is gone beneath it."""
    if any(isinstance(sc, BoardsHome) for sc in app.screen_stack):
        return "the home is still on the stack under the offer"
    if type(app.screen_stack[0]).__name__ != "Screen":
        return "no board screen under the offer"
    return None


def _check_start(app: Shot) -> str | None:
    """AT-2702's visible half: the open-twice warning and the archived-old-work
    notice are both up, and the sweep really saved the archive."""
    titles = [n.title for n in app._notifications]
    if titles.count(OPEN_TWICE) != 1:
        return f"{titles.count(OPEN_TWICE)} open-twice notice(s)"
    if titles.count(ARCHIVED) != 1:
        return f"{titles.count(ARCHIVED)} archived-old-work notice(s)"
    if Board.load(app._default).task_by_id("t-old").archived is False:
        return "the sweepable task was not archived"
    if app._default.read_bytes() == app._before:
        return "the default board's bytes did not change (the sweep never ran)"
    return None


def _markers_for(path: Path) -> list[str]:
    d = boards_mod.presence_dir()
    stem = boards_mod._presence_stem(path)
    if not d.is_dir():
        return []
    return sorted(p.name for p in d.iterdir() if p.name.startswith(stem + "-"))


SCENES = {
    # 1 — the quiet home at start (DDR ux-2): two boards, a foreign marker and a
    # sweepable old done task planted on the default board BEFORE the app
    # starts — and still no modal, no toast, no marker of this window, no write
    "home": dict(keys=[], want="BoardsHome", check=_check_home),
    # 2 — enter on the default card: the deferred start runs and the one-time
    # milestone offer opens OVER THE CHOSEN BOARD (the home is not beneath it)
    "offer": dict(keys=["enter"], want="MilestoneOffer", check=_check_offer),
    # 3 — the worst-case toast stack right after leaving the home (DDR ux-2):
    # the foreign marker and the sweepable task both planted before the start;
    # enter on the card; the open-twice warning and the archived-old-work
    # notice are both up over the board
    "start": dict(keys=["enter"], want="Screen", check=_check_start),
}


def build(name: str) -> Shot:
    root = HOME / ".taskboard"
    reg_path = mb.build(root, last="personal")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    reg["boards"] = [e for e in reg["boards"]
                     if e["id"] in ("personal", "client-retail-rag")]
    reg_path.write_text(json.dumps(reg), encoding="utf-8")
    default = mb.board_path(root, "personal")
    scene = SCENES[name]
    marker = None
    if name in ("home", "start"):
        b = Board.load(default)
        b.tasks.append(Task("Old done task", project_id=b.projects[0].id, phase="Done",
                            phase_changed=(mb.TODAY - timedelta(days=40)).isoformat(),
                            id="t-old"))
        b.save()
        marker = boards_mod.announce(default, NOW)
    if name == "offer":
        b = Board.load(default)
        d = (mb.TODAY + timedelta(days=1)).isoformat()
        b.tasks.append(Task("One-day launch dry-run", project_id=b.projects[0].id,
                            phase="Next", start_date=d, due_date=d, id="t-oneday"))
        del b.settings["migrations"]["milestones"]      # an unmarked candidate board
        b.save()
    before = default.read_bytes()
    registry = Registry.load(reg_path, root / "board.json")
    entry = registry.opening()
    registry.touch(entry.id, NOW)
    app = Shot(name, scene, board_path=entry.path, registry=registry)
    app._before, app._default, app._foreign = before, default, marker
    return app


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "live":
        app = build(args[1])
        try:
            app.run()
        finally:
            if app._foreign is not None:
                boards_mod.withdraw(app._foreign)
            shutil.rmtree(HOME, ignore_errors=True)
    else:
        print(__doc__)

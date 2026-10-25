"""Real-app captures of batch 2026-10-25-batch-01 — the SHIPPED `TaskboardApp`, unpatched.

    python .dev-flow/2026-10-25-batch-01/evidence/captures/shoot_real.py list
    python .dev-flow/2026-10-25-batch-01/evidence/captures/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot.ps1` (the method of batches
2026-10-21-batch-02 and 2026-10-24-batch-01/02: the window selected by its
unique title, PrintWindow, full colour, closed right after its shot). The
subclass below only sets the window title, plays the scene's keys through the
app's own key path (`App._press_keys`) and reports the screen it ended on: no
screen, render or behaviour is replaced. Each scene's READY check asserts the
end state AND the scripted content check (batch 2026-10-25-batch-01, ux
condition C2): the composited full-screen-stack render of the LIVE app at
capture time holds > 0 board rows outside the modal's box — so a shot that is
merely non-black can never pass; the pixels and the in-app render are the same
frame. Synthetic boards (`tests/multi_board_fixture.py`) live in a temporary
folder standing in for the home; the calendar/clock are pinned to the fixture's
Tuesday 2026-10-20 09:30. Nothing touches the real home.
"""
from __future__ import annotations

import asyncio
import io
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
HOME = Path(tempfile.mkdtemp(prefix="b01-cap-"))
Path.home = classmethod(lambda cls: HOME)

import multi_board_fixture as mb  # noqa: E402
import kg_board  # noqa: E402
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

OFFER_TITLE = "convert one-day tasks"
PICKER_TITLE = "Operator identity"


class Shot(TaskboardApp):
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")

    def __init__(self, name: str, scene: dict, **kw):
        self._name, self._steps, self._want = name, scene["keys"], scene["want"]
        self._check = scene["check"]
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
                f"toasts={len(self._notifications)}",
                encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


# ---- the scripted content check (ux condition C2) --------------------------- #
def _strips(app) -> list[str]:
    """The composited full screen stack of the LIVE app (the export_screenshot
    source) — the same frame the pixels hold."""
    from rich.console import Console
    render = app.screen._compositor.render_update(
        full=True, screen_stack=app._background_screens)
    console = Console(width=app.size.width, height=app.size.height,
                      file=io.StringIO(), force_terminal=True,
                      color_system="truecolor", record=True,
                      legacy_windows=False, safe_box=False)
    console.print(render)
    return console.export_text().splitlines()


def _rows_outside(app, title: str) -> tuple[int, int] | str:
    rows = _strips(app)
    hits = [i for i, r in enumerate(rows) if title in r]
    if not hits:
        return f"box title {title!r} not in the render"
    t = hits[0]
    top = next((i for i in range(t, -1, -1) if "╭" in rows[i]), None)
    bottom = next((i for i in range(t + 1, len(rows)) if "╰" in rows[i]), None)
    if top is None or bottom is None:
        return f"box borders around {title!r} not found"
    above = sum(1 for r in rows[:top] if r.strip())
    below = sum(1 for r in rows[bottom + 1:] if r.strip())
    return above, below


def _check_board_visible(app: Shot, title: str) -> str | None:
    """The content acceptance: the board's rows show outside the modal's box in
    the very frame being captured."""
    counts = _rows_outside(app, title)
    if isinstance(counts, str):
        return counts
    if counts[0] + counts[1] <= 0:
        return f"no board rows outside the box {counts} (the backdrop is not dimming)"
    return None


# ---- per-scene end-state checks --------------------------------------------- #
def _check_single(app: Shot) -> str | None:
    """AT-2801: the offer is the top screen over the board it started from, and
    the board's rows show around the box."""
    if any(isinstance(sc, BoardsHome) for sc in app.screen_stack):
        return "the home is on the stack of a single-board start"
    return _check_board_visible(app, OFFER_TITLE)


def _check_offer(app: Shot) -> str | None:
    """AT-2802: the offer is the top screen over the chosen board (the home is
    gone) and the board's rows show around the box."""
    if any(isinstance(sc, BoardsHome) for sc in app.screen_stack):
        return "the home is still on the stack under the offer"
    if type(app.screen_stack[0]).__name__ != "Screen":
        return "no board screen under the offer"
    return _check_board_visible(app, OFFER_TITLE)


def _check_picker(app: Shot) -> str | None:
    """AT-2803's picker half + PDR #D1: the picker alone over the dimmed board,
    its placement preserved (geometry pinned at 118x30), rows showing around
    the box."""
    reason = _check_board_visible(app, PICKER_TITLE)
    if reason:
        return reason
    if app.size.width == 118:
        rows = _strips(app)
        top = next(i for i, r in enumerate(rows) if "╭" in r)
        bottom = next(i for i in range(top, len(rows)) if "╰" in rows[i])
        left = rows[top].index("╭")
        right = rows[top].index("╮")
        if (top, left, right, bottom) != (0, 0, 61, 11):
            return f"picker box moved: row {top}, cols {left}-{right}, bottom {bottom}"
    return None


SCENES = {
    # 1 — a single-board start with an unmarked candidate (the commission's
    # first capture): the offer opens at mount over its own board, dimmed
    "single": dict(keys=[], want="MilestoneOffer", check=_check_single),
    # 2 — two boards, `enter` on the default card (the commission's second
    # capture): the offer opens over the chosen board, the home gone
    "offer": dict(keys=["enter"], want="MilestoneOffer", check=_check_offer),
    # 3 — a team-shared board with no identity and the offer mark pre-set: the
    # picker alone over the dimmed board, at its blessed top-left placement
    "picker": dict(keys=[], want="TeamIdentityPicker", check=_check_picker),
}


def _unmark_milestones(path: Path) -> None:
    b = Board.load(path)
    del b.settings["migrations"]["milestones"]      # an unmarked board
    b.save()


def _add_candidate(path: Path) -> None:
    b = Board.load(path)
    d = (mb.TODAY + timedelta(days=1)).isoformat()
    b.tasks.append(Task("One-day launch dry-run", project_id=b.projects[0].id,
                        phase="Next", start_date=d, due_date=d, id="t-oneday"))
    b.save()


def _team(root: Path, board_path: Path) -> None:
    team = root / "team"
    team.mkdir()
    (team / "team.json").write_text(json.dumps(kg_board.TEAM), encoding="utf-8")
    b = Board.load(board_path)
    b.settings["team_shared_dir"] = str(team)
    b.save()


def build(name: str) -> Shot:
    root = HOME / ".taskboard"
    reg_path = mb.build(root, last="personal")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    keep = ("personal",) if name in ("single", "picker") else ("personal", "client-retail-rag")
    reg["boards"] = [e for e in reg["boards"] if e["id"] in keep]
    reg_path.write_text(json.dumps(reg), encoding="utf-8")
    default = mb.board_path(root, "personal")
    if name in ("single", "offer"):
        _unmark_milestones(default)
        _add_candidate(default)
    if name == "picker":
        _team(root, default)              # the marks stay set: no offer, picker alone
    registry = Registry.load(reg_path, root / "board.json")
    entry = registry.opening()
    registry.touch(entry.id, NOW)
    return Shot(name, SCENES[name], board_path=entry.path, registry=registry)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
    elif args and args[0] == "live":
        app = build(args[1])
        try:
            app.run()
        finally:
            shutil.rmtree(HOME, ignore_errors=True)
    else:
        print(__doc__)

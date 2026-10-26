"""Real-app captures of batch 2026-10-25-batch-02 — the SHIPPED `TaskboardApp`, unpatched.

    python .dev-flow/2026-10-25-batch-02/evidence/captures/shoot_real.py list
    python .dev-flow/2026-10-25-batch-02/evidence/captures/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot.ps1` (the method of batches
2026-10-21-batch-02, 2026-10-24-batch-01/02 and 2026-10-25-batch-01: the window
selected by its unique title, PrintWindow, full colour, closed right after its
shot). The subclass below only sets the window title, selects the cursor task,
plays the scene's keys through the app's own key path (`App._press_keys`) and
reports the screen it ended on: no screen, render or behaviour is replaced.
Each scene's READY check asserts the end state AND the scripted content check
(batch 2026-10-25-batch-02's C2, the same discipline as batch-01's): the
composited full-screen-stack render of the LIVE app at capture time — the same
source the pixels hold — must carry the three highlight tones #fbbf24 /
#f43f5e / #4ade80 in its styles AND hold no run of `==`, `!!`, `++` anywhere
(the note rows included), so a shot that is merely non-black can never pass.
Synthetic board only: one project, two open tasks, the FIRST task's notes
holding the highlighted note; it lives in a temporary folder standing in for
the home (`TEMP\\n01-cap-*`), the calendar/clock pinned to Tuesday
2026-10-20 09:30. Nothing touches the real home; no real names anywhere.
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
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
HOME = Path(tempfile.mkdtemp(prefix="n01-cap-"))
Path.home = classmethod(lambda cls: HOME)

from taskboard import app as app_mod, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry  # noqa: E402
from taskboard.models import MILESTONES_MIGRATION, LINKS_MIGRATION  # noqa: E402
from taskboard.models import Board, Project, Task  # noqa: E402

NOW = datetime(2026, 10, 20, 9, 30)      # a Tuesday, pinned like batch-01's


class _Today(date):
    @classmethod
    def today(cls):
        return NOW.date()


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


for _m in (app_mod, models, views, modals):
    _m.date = _Today
app_mod.datetime = _Now

# the commission's highlighted note (the FIRST task's notes); its marker-free
# twin reads: "Review the launch plan with care and the sponsor before Friday"
NOTE = ("Review ==the launch plan== with !!care!! and "
        "++the sponsor++ before Friday")
NOTE_WORDS = ("the launch plan", "care", "the sponsor")
TONES = ("#fbbf24", "#f43f5e", "#4ade80")    # HEX["soon"] / ["over"] / ["green"]
FIRST_ID = "t-first"
PHASES = ["Backlog", "Next", "Doing", "Review", "Done"]


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
            if os.environ.get("PROTO_SHOT_TITLE"):      # re-asserted at capture time
                self.title = os.environ["PROTO_SHOT_TITLE"]
            Path(ready).write_text(
                f"{HOME}\n{'OK' if reason is None else 'BAD ' + reason} "
                f"{type(self.screen).__name__} board={self.board_id} "
                f"toasts={len(self._notifications)}",
                encoding="utf-8")
        if self._seconds:
            self.set_timer(self._seconds, self.exit)


# ---- the scripted content check (the batch's C2) ---------------------------- #
def _strips(app) -> list[str]:
    """The composited full screen stack of the LIVE app (the export source) —
    the same frame the pixels hold."""
    from rich.console import Console
    render = app.screen._compositor.render_update(
        full=True, screen_stack=app._background_screens)
    console = Console(width=app.size.width, height=app.size.height,
                      file=io.StringIO(), force_terminal=True,
                      color_system="truecolor", record=True,
                      legacy_windows=False, safe_box=False)
    console.print(render)
    return console.export_text().splitlines()


def _frame_html(app) -> str:
    """The same composited frame rendered with inline styles — where the tone
    hexes live."""
    from rich.console import Console
    render = app.screen._compositor.render_update(
        full=True, screen_stack=app._background_screens)
    console = Console(width=app.size.width, height=app.size.height,
                      file=io.StringIO(), force_terminal=True,
                      color_system="truecolor", record=True,
                      legacy_windows=False, safe_box=False)
    console.print(render)
    return console.export_html(inline_styles=True)


def _check_scene(app: Shot, view: str) -> str | None:
    """AT-2901 (view 1) / AT-2902 (view 2): the end screen is the presentation,
    the current view is the scene's one, and the composited full-screen frame
    at capture time carries the three tone hexes in its styles with no marker
    run — the note rows read marker-free, the highlighted words painted."""
    screen = app.screen
    if type(screen).__name__ != "PresentScreen":
        return f"screen {type(screen).__name__} != PresentScreen"
    got = views.PRESENT_SCREEN_VIEWS[screen._view]
    if got != view:
        return f"view {got!r} != {view!r} (index {screen._view})"
    rows = _strips(app)
    joined = "\n".join(rows)
    for run in ("==", "!!", "++"):
        if run in joined:
            return f"marker run {run!r} in the composited frame"
    for word in NOTE_WORDS:
        if word not in joined:
            return f"note text {word!r} missing from the frame"
    html = _frame_html(app)
    for tone in TONES:
        if tone not in html:
            return f"tone {tone} absent from the composited frame's styles"
    return None


def _select_first(app: Shot) -> None:
    """The cursor seat: the FIRST task (its notes hold the highlighted note) —
    the app's own ATs set the selection the same way before pressing `R`."""
    app.selected_task_id = FIRST_ID
    app.refresh_view()


# ---- the scenes ------------------------------------------------------------- #
SCENES = {
    # 1 — view 1 `gantt`: the cursor sits on the first task (the highlighted
    # note is its notes), so the gantt cursor note expands under the briefs
    "gantt": dict(keys=[_select_first, "R"], want="PresentScreen",
                  check=partial(_check_scene, view="gantt")),
    # 2 — view 2 `split`: same board, then the view key for split
    "split": dict(keys=[_select_first, "R", "2"], want="PresentScreen",
                  check=partial(_check_scene, view="split")),
}


def build(name: str) -> Shot:
    root = HOME / ".taskboard"
    root.mkdir(parents=True)
    d = lambda off: (NOW.date() + timedelta(days=off)).isoformat()   # noqa: E731
    proj = Project(name="Launch readiness", color="sky",
                   start_date=d(-7), due_date=d(14), id="p-launch")
    first = Task(title="Launch plan review", project_id=proj.id, phase="Doing",
                 priority="high", start_date=d(-3), due_date=d(0), notes=NOTE,
                 phase_changed=d(-3), id=FIRST_ID)
    second = Task(title="Dry-run checklist", project_id=proj.id, phase="Next",
                  priority="normal", start_date=d(1), due_date=d(5),
                  notes="Book the room and invite the pilot stores.",
                  phase_changed=d(-2), id="t-second")
    board = Board([proj], [first, second], root / "board.json",
                  {"migrations": {"links": LINKS_MIGRATION,
                                  "milestones": MILESTONES_MIGRATION},
                   "seen_view_renumber_2026_07": True}, PHASES)
    board.save()
    reg_path = root / "boards.json"
    reg_path.write_text(json.dumps({"version": 1, "last": "main", "boards": [{
        "id": "main", "name": "Launch readiness", "color": "sky",
        "path": str((root / "board.json").resolve()),
        "last_opened": NOW.isoformat(timespec="minutes"), "archived": False}]}),
        encoding="utf-8")
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

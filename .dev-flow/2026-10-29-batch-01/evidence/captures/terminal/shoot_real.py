"""Real-app captures of batch 2026-10-29-batch-01 — the SHIPPED `TaskboardApp`, unpatched:
the `H` report modal and its toast.

    python .dev-flow/2026-10-29-batch-01/evidence/captures/terminal/shoot_real.py list
    python .dev-flow/2026-10-29-batch-01/evidence/captures/terminal/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot.ps1` (copied from batch 2026-10-25-batch-02's
harness: the window selected by its unique `hx-` title, PrintWindow, full colour, closed
right after its shot). The subclass below only sets the window title, selects the cursor
task, plays the scene's keys through the app's own key path (`App._press_keys`) and
reports the screen it ended on: no screen, render or behaviour is replaced.
Each scene's READY check asserts the end state AND a scripted content check on the
composited full-screen-stack frame of the LIVE app at capture time (the source the pixels
hold): the modal's scope marks and board names, or the toast's text.

Synthetic home only, built as `tests/test_report_export_app.py` builds it: the report
fixture's three boards Personal / Client A / Course (`tests/report_fixture.py`), each in
its own folder under `<home>/.taskboard/boards/`, registered in `boards.json`, Client A
opened last; the home is a temporary folder (`TEMP\\hx-cap-*`) standing in for
`Path.home()`; the date pinned to the fixture's TODAY (2026-10-29). Nothing touches the
real home; no real names anywhere.
"""
from __future__ import annotations

import asyncio
import io
import json
import os
import shutil
import sys
import tempfile
from datetime import date, datetime
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
HOME = Path(tempfile.mkdtemp(prefix="hx-cap-"))
Path.home = classmethod(lambda cls: HOME)

import report_fixture as F  # noqa: E402
from taskboard import app as app_mod, models, modals, views  # noqa: E402
from taskboard.app import TaskboardApp  # noqa: E402
from taskboard.boards import Registry, registry_path  # noqa: E402
from taskboard.models import LINKS_MIGRATION, MILESTONES_MIGRATION, default_board_path  # noqa: E402


class _Today(date):
    @classmethod
    def today(cls):
        return F.TODAY


for _m in (app_mod, models, views, modals):
    _m.date = _Today

LISTED = {"personal": ("Personal", "violet", F.personal),
          "client-a": ("Client A", "sky", F.client_a),
          "course": ("Course", "fuchsia", F.course)}
SELECTED = "tst2"            # a Client A task of project Storefront relaunch (TC-3118's seat)


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


# ---- the scripted content check --------------------------------------------- #
def _strips(app) -> str:
    """The composited full screen stack of the LIVE app — the frame the pixels hold."""
    from rich.console import Console
    render = app.screen._compositor.render_update(
        full=True, screen_stack=app._background_screens)
    console = Console(width=app.size.width, height=app.size.height,
                      file=io.StringIO(), force_terminal=True,
                      color_system="truecolor", record=True,
                      legacy_windows=False, safe_box=False)
    console.print(render)
    return console.export_text()


def _check_modal(app: Shot, scope: str) -> str | None:
    """TC-3118's painted claims at capture time: the title, the mark on the scene's
    scope, the three board names, the destination folder and the key line."""
    frame = _strips(app)
    on, off = ("all boards (3)", "Storefront relaunch on Client A")
    if scope == "project":
        on, off = off, on
    want = ["Export an HTML report", f"● {on}", f"○ {off}",
            "Personal · Client A · Course", "Writes to", "reports",
            "workspace", "deck", "both", "all boards", "esc"]
    for w in want:
        if w not in frame:
            return f"{w!r} missing from the composited frame"
    return None


def _check_toast(app: Shot) -> str | None:
    """AT-3101's toast at capture time: one `Report` toast naming the written file and
    offering `o` for 10 s, painted in the frame; the file exists in the open board's
    `reports/` folder."""
    toasts = [n for n in app._notifications if n.title == "Report"]
    if len(toasts) != 1:
        return f"{len(toasts)} Report toasts"
    msg = toasts[0].message
    name = f"workspace-{F.TODAY.isoformat()}.html"
    folder = HOME / ".taskboard" / "boards" / "client-a" / "reports"
    if not msg.startswith(f"Report written: {name} to {folder}") or \
            not msg.endswith("o opens it (10 s)"):
        return f"toast text {msg!r}"
    if not (folder / name).is_file():
        return f"{name} not written"
    flat = " ".join(_strips(app).split())
    for w in ("Report written:", "o opens it (10 s)"):
        if w not in flat:
            return f"{w!r} not painted"
    return None


def _select(app: Shot) -> None:
    """The cursor seat — the app's own ATs set the selection the same way before `H`."""
    app.selected_task_id = SELECTED
    app.refresh_view()


# ---- the scenes ------------------------------------------------------------- #
SCENES = {
    # `esc` leaves the home of boards for the open board (Client A), as the ATs' `start`
    "report-modal": dict(keys=["escape", _select, "H"], want="ReportExport",
                         check=partial(_check_modal, scope="all")),
    "report-modal-p": dict(keys=["escape", _select, "H", "p"], want="ReportExport",
                           check=partial(_check_modal, scope="project")),
    "report-toast": dict(keys=["escape", _select, "H", "b"], want="Screen",
                         check=_check_toast),
}


def build(name: str) -> Shot:
    """The home as `test_report_export_app.build_home` / `open_home` build it."""
    root = HOME / ".taskboard"
    entries = []
    for bid, (bname, colour, make) in LISTED.items():
        board = make(root / "boards" / bid / "board.json")
        board.settings = {"migrations": {"links": LINKS_MIGRATION,
                                         "milestones": MILESTONES_MIGRATION},
                          "seen_view_renumber_2026_07": True}
        board.path.parent.mkdir(parents=True, exist_ok=True)
        board.save()
        entries.append({"id": bid, "name": bname, "color": colour, "path": str(board.path),
                        "last_opened": "2026-10-29T09:00", "archived": False})
    (root / "boards.json").write_text(
        json.dumps({"version": 1, "last": "client-a", "boards": entries}, indent=2),
        encoding="utf-8")
    # the registry exactly as `taskboard.__main__.open_app(None)` opens it
    registry = Registry.load(registry_path(), default_board_path())
    entry = registry.opening()
    registry.touch(entry.id, datetime.now())
    app = Shot(name, SCENES[name], board_path=entry.path, registry=registry)
    app.people.people.update(F.PEOPLE)          # the live directories, in memory only
    app.marks.marks.update(F.MARKS)
    return app


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "list":
        print(" ".join(SCENES))
        shutil.rmtree(HOME, ignore_errors=True)
    elif args and args[0] == "live":
        app = build(args[1])
        try:
            app.run()
        finally:
            shutil.rmtree(HOME, ignore_errors=True)
    else:
        print(__doc__)

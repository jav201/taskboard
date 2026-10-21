"""Real-app captures of batch 2026-10-21-batch-01 — the SHIPPED `TaskboardApp`, unpatched.

    python .dev-flow/2026-10-21-batch-01/evidence/captures/shoot_real.py list
    python .dev-flow/2026-10-21-batch-01/evidence/captures/shoot_real.py live SCENE [SECONDS]

Run inside a real Windows Terminal by `shoot_real.ps1` (the people round's capture
method: the window selected by its unique title, PrintWindow, full colour, closed right
after its shot). The subclass below only sets the window title, plays the scene's keys
through the app's own key path (`App._press_keys`) and reports the screen it ended on:
no screen, render or behaviour is replaced. The round's synthetic boards and people
(`tests/people_round_fixture.py`) live in a temporary folder that stands in for the home;
the calendar is the round's (Tuesday 2026-10-20). Nothing touches the real home.
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
HOME = Path(tempfile.mkdtemp(prefix="p01-cap-"))
Path.home = classmethod(lambda cls: HOME)

import people_round_fixture as fx  # noqa: E402
from textual.widgets import TextArea  # noqa: E402
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


def notes_end(app) -> None:
    ta = app.screen.query_one("#f-notes", TextArea)
    ta.focus()
    ta.move_cursor(ta.document.end)


def tab_to_notes(app) -> None:
    """the notes reached the operator's way: `tab` from the title (`focus_next`)."""
    for _ in range(20):
        if app.focused is not None and app.focused.id == "f-notes":
            break
        app.screen.focus_next()
    ta = app.screen.query_one("#f-notes", TextArea)
    ta.move_cursor(ta.document.end)


def typed(s: str) -> list:
    return ["enter" if ch == "\n" else "space" if ch == " " else "at" if ch == "@" else ch
            for ch in s]


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


EDIT = ["escape", sel("tc8"), "e", notes_end]
SCENES = {
    # item 1 — the people view: A's panes, C's quote under each task, B's box (the
    # operator's objection, composed), then the tasks pane, the jump, the form; and
    # view 9 for D4's naming apart
    "pv": dict(keys=["escape", "at"], want="PeopleDirectory"),
    "pv-tasks": dict(keys=["escape", "at", "tab", "down"], want="PeopleDirectory"),
    "pv-marta": dict(keys=["escape", "at", "down", "down", "enter"], want="PeopleDirectory"),
    "pv-open": dict(keys=["escape", "at", "tab", "down", "enter"], want="Screen"),
    "pv-edit": dict(keys=["escape", "at", "e"], want="PersonForm"),
    "d4-view9": dict(keys=["escape", "9"], want="Screen"),
    # item 2 — the `@` picker in the editor's notes
    "mt-list": dict(keys=EDIT + typed("\nAsk @an"), want="TaskModal"),
    "mt-add": dict(keys=EDIT + typed("\nCall @Sofia") + ["enter"] + typed("Legal counsel"),
                   want="TaskModal"),
    # ux UX-3 (UX-DDR-2): reached by tab, the cursor six lines down: the list flips up
    "mt-flip": dict(keys=["escape", sel("tc8"), "e", tab_to_notes] + typed("\n" * 6 + "Ask @an"),
                    want="TaskModal"),
    "mt-done": dict(keys=EDIT + typed("\nAsk @an") + ["enter"] + typed("about the stores"),
                    want="TaskModal"),
    # item 3 — `/` then `@`
    "sr-list": dict(keys=["escape", "4", "slash"] + typed("@an"), want="SearchPrompt"),
    "sr-res": dict(keys=["escape", "4", "slash"] + typed("@an") + ["enter"], want="Screen"),
    # item 4 — how a mention looks: details, kanban card, presentation (split)
    "m-det": dict(keys=["escape", sel("tc5"), "enter"], want="TaskDetails"),
    "m-kb": dict(keys=["escape", "4", sel("tc5")], want="Screen"),
    "m-pr": dict(keys=["escape", sel("tc5"), "R", "2"], want="PresentScreen"),
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

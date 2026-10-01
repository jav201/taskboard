"""Captures of the REAL app after batch 2026-09-30-batch-01 (no prototype
patches, no prototype CSS): the edit window and the kanban, 120x36 and 80x24.

    python prototypes/edit_modal/capture_after.py svg      -> out/after/*.svg
    python prototypes/edit_modal/capture_after.py live edit|kanban SECONDS
        (what shoot_after.ps1 runs inside Windows Terminal)

Throwaway harness: the fixture board is a temp copy, the date is pinned.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prototypes" / "kanban_priority"))

import fixture  # noqa: E402

fixture.pin_today()

from textual.widgets import TextArea  # noqa: E402

from taskboard.app import TaskboardApp  # noqa: E402

OUT = HERE / "out" / "after"


class Shot(TaskboardApp):
    # a subclass resolves CSS_PATH next to ITS module; point it at the real one
    CSS_PATH = str(ROOT / "taskboard" / "taskboard.tcss")
    def __init__(self, what: str, seconds: float | None = None):
        super().__init__(board_path=str(fixture.write_board()), team_sync_interval=1e9)
        self._what = what
        self._seconds = seconds

    def on_mount(self) -> None:
        super().on_mount()
        if os.environ.get("PROTO_SHOT_TITLE"):
            self.title = os.environ["PROTO_SHOT_TITLE"]
        self.view_mode = "kanban"
        self.selected_task_id = fixture.LONG_TASK_ID if self._what == "edit" else "t11"
        self.refresh_view()
        if self._what == "edit":
            self.call_after_refresh(self._open)
        if self._seconds:
            self.set_timer(self._seconds, self.exit)

    def _open(self) -> None:
        self.action_edit()
        self.call_after_refresh(self._write)

    def _write(self) -> None:
        ta = self.screen.query_one("#f-notes", TextArea)
        ta.focus()
        ta.move_cursor(ta.document.end)
        ta.cursor_blink = False          # a blink-off frame would hide the cursor


async def _svg(what: str, size: tuple[int, int]) -> None:
    app = Shot(what)
    async with app.run_test(size=size) as pilot:
        for _ in range(6):
            await pilot.pause()
        await pilot.pause(0.3)
        name = f"{what}_{size[0]}x{size[1]}.svg"
        app.save_screenshot(filename=name, path=str(OUT))
        print(OUT / name)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "svg":
        for what in ("edit", "kanban"):
            for size in ((120, 36), (80, 24)):
                asyncio.run(_svg(what, size))
    else:
        Shot(sys.argv[2], float(sys.argv[3])).run()

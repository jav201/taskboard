"""Captures for batch 2026-10-06-batch-01 (B2b, moving linked dates) — the
operator's visual verdict surfaces: the bump toast at 118 and 80, the m cycle,
the project editor's new row. SVG + painted text, synthetic board only.

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/capture_b2b.py
"""
import asyncio
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
OUT = ROOT / ".dev-flow" / "2026-10-06-batch-01" / "evidence" / "captures"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import kg_board
import taskboard.app as appmod
appmod.milestones_marked = lambda settings: True   # the offer never opens
from taskboard.app import TaskboardApp             # noqa: E402


async def shoot(app, pilot, stem):
    await pilot.pause()
    strips = app.screen._compositor.render_strips(app.screen.size)
    (OUT / f"{stem}.txt").write_text(
        "\n".join(s.text.rstrip() for s in strips) + "\n", encoding="utf-8")
    app.save_screenshot(f"{stem}.svg", str(OUT))


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    path = tmp / "board.json"
    b = kg_board.milestones(kg_board.shifted(path), date.today())
    b.settings["seen_view_renumber_2026_07"] = True
    b.save()

    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await shoot(app, pilot, "close-kanban-before")
        await pilot.press("+")
        await shoot(app, pilot, "close-toast-118")
        await pilot.press("m")           # together
        await shoot(app, pilot, "close-toast-m-together")
        await pilot.press("m")           # flag
        await shoot(app, pilot, "close-toast-m-flag")

    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(80, 24), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm2"
        app.refresh_view()
        await pilot.press("+")
        await shoot(app, pilot, "close-toast-80")

    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30), notifications=True) as pilot:
        await pilot.press("P")
        await pilot.pause()
        idx = app.board.projects.index(app.board.project_by_id("pdwh"))
        app.screen.query_one("#proj-list").highlighted = idx
        await pilot.press("e")
        await pilot.pause()
        await shoot(app, pilot, "close-project-editor")
    print("captures done")


asyncio.run(main())

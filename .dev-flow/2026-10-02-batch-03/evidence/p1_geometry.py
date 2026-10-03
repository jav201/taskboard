"""P1 probe: the board panel's size inside the running app at the two terminal sizes
(the renderer is asked for the PANEL; ATs name TERMINAL sizes).
    python .dev-flow/2026-10-02-batch-03/evidence/p1_geometry.py"""
import asyncio
import sys
import tempfile
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "tests")]
import kg_board  # noqa: E402
from taskboard.app import BoardView, TaskboardApp  # noqa: E402


async def probe(size):
    tmp = Path(tempfile.mkdtemp(prefix="kg-geo-"))
    b = kg_board.build(tmp / "board.json")
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("4")
        await pilot.pause()
        bw = app.query_one("#board", BoardView).size
        vp = app.query_one("#viewport").size
        print(f"terminal {size[0]}x{size[1]}: board width {bw.width}, viewport height {vp.height}, "
              f"presentation {app.kanban_presentation}")


for s in ((120, 32), (118, 30), (82, 26), (80, 24)):
    asyncio.run(probe(s))

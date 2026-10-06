"""Increment 001 (LLR-601.3, C-39): the smallest width at which the editor's chip row fits on
ONE row with the milestone box. For each width W the fold threshold is patched to W (so the row is
one-row at W) and every focusable chip must be fully visible. Synthetic board in a temp dir.
    python -B .dev-flow/2026-10-04-batch-02/evidence/p3_chip_threshold.py"""
import asyncio, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
import test_edit_window as T
from taskboard import modals

async def fits(w):
    modals.TASK_CHIPS_ONE_ROW = w
    with tempfile.TemporaryDirectory() as d:
        app = T._app(Path(d))
        async with app.run_test(size=(w, 36)) as pilot:
            scr = await T._open_editor_writing(app, pilot)
            chips = [x for x in scr.query_one("#task-chips").query("*") if x.can_focus and x.id]
            clipped = [x.id for x in chips if not T._fully_visible(scr, x)]
            return len(chips), clipped

async def main():
    for w in range(120, 160):
        n, clipped = await fits(w)
        print(w, n, "clipped:", clipped)
        if not clipped:
            print("one row fits from", w); break
asyncio.run(main())

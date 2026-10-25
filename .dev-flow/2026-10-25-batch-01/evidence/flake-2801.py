"""QA-P4-B01-flake — the PDR's flake arm (qa condition C1): AT-2801 at 80x24,
50 repetitions. Two measurements:
  1. 50 sequential pytest runs of the node — all must pass (no timing flake).
  2. 50 in-process renders record the outside-box row counts — min >= 3, so a
     short pause can never dip a run below the >0 threshold.
Run from the worktree root with the worktree package:
  PYTHONPATH=<worktree> python .dev-flow/2026-10-25-batch-01/evidence/flake-2801.py
"""
import asyncio
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path("tests").resolve()))

NODE = ("tests/test_startup_backdrop.py::"
        "test_AT_2801_the_offer_opens_over_the_painted_board[size1]")
FAILURES = 0
for i in range(50):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q",
                        "-p", "no:cacheprovider", NODE],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        FAILURES += 1
        print(f"run {i + 1}: FAIL", flush=True)
print(f"pytest runs: 50, failures: {FAILURES}", flush=True)


async def counts_once():
    import kg_board
    from taskboard.app import TaskboardApp
    from taskboard.modals import MilestoneOffer
    from test_startup_backdrop import (_strips, _rows_outside, _offer_board,
                                       _await_offer, OFFER_TITLE)

    with tempfile.TemporaryDirectory() as td:
        path = _offer_board(Path(td) / "board.json")
        app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
        async with app.run_test(size=(80, 24)) as pilot:
            await _await_offer(pilot, app)
            return _rows_outside(_strips(app), OFFER_TITLE)


mins = [50, 50]
for i in range(50):
    above, below = asyncio.run(counts_once())
    mins[0] = min(mins[0], above)
    mins[1] = min(mins[1], below)
print(f"outside-box rows over 50 renders: min above = {mins[0]}, "
      f"min below = {mins[1]} (threshold >= 3)", flush=True)
print("flake verdict:", "PASS" if FAILURES == 0 and min(mins) >= 3 else "FAIL",
      flush=True)

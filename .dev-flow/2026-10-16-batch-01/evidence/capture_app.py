"""Capture the change FROM THE RUNNING APP (batch 2026-10-16-batch-01).

    python .dev-flow/2026-10-16-batch-01/evidence/capture_app.py <increment> [<increment> ...]

The real `TaskboardApp` runs headless on the PRES-C oracle board (synthetic,
`tests/present_board.py`) with the calendar frozen on the board's TODAY; keys are
pressed through the pilot as a user would, and every frame is the app's own
`export_screenshot()` SVG, written under this evidence directory as
`app-<inc>-<w>x<h>-<step>.svg`. Nothing in `taskboard/` is patched.
"""
from __future__ import annotations

import asyncio
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import present_board as pb  # noqa: E402
from taskboard import app as app_mod  # noqa: E402
from taskboard import models  # noqa: E402

OUT = HERE / "captures"
SIZES = [(118, 31), (80, 25)]


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


app_mod.date = _Today
models.date = _Today

# per increment: (step name, keys pressed before the shot), starting from the
# board view with the oracle cursor selected
PLANS = {
    "001": [("present-open", ["R"]), ("cursor-moved", ["right", "right"])],
    "002": [("present-open", ["R"]), ("hidden", ["space"]), ("show-all", ["a"])],
    "003": [("gantt-help", ["3", "question_mark"])],
}


async def run(inc: str, size: tuple[int, int]) -> list[Path]:
    tmp = Path(tempfile.mkdtemp())
    board = pb.build(tmp / "board.json")
    board.save()
    app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
    written = []
    async with app.run_test(size=size) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.pause()
        app.selected_task_id = pb.CURSOR
        for step, keys in PLANS[inc]:
            for k in keys:
                await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            svg = app.export_screenshot(title=f"taskboard · {inc} · {step}")
            path = OUT / f"app-{inc}-{size[0]}x{size[1]}-{step}.svg"
            path.write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")
            written.append(path)
    return written


def main(argv: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for inc in argv or ["001"]:
        for size in SIZES:
            for p in asyncio.run(run(inc, size)):
                print(p.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main(sys.argv[1:])

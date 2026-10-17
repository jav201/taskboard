"""Capture the change FROM THE RUNNING APP (batch 2026-10-17-batch-01).

    python .dev-flow/2026-10-17-batch-01/evidence/capture_app.py

Batch 2026-10-16-batch-01's `capture_app.py`, re-aimed at the gantt view: the
real `TaskboardApp` runs headless on the PRES-C oracle board (synthetic,
`tests/present_board.py`) with the calendar frozen on the board's TODAY; keys
are pressed through the pilot as a user would, and every frame is the app's own
`export_screenshot()` SVG, written as `captures/app-001-<w>x<h>-<step>.svg`.
As in batch-01, the starting selection is set to the oracle cursor (`tw3`).

Steps, per size:
  gantt-selected      `3` — the label names the selected task
  gantt-none          then `/` `zzqx` `enter` — a search that draws no task:
                      nothing selected, the label column blank (the gantt view
                      always re-selects a drawn task, so this is how "none" looks)
  gantt-nodates       a board file whose `tw3` has no dates, `3` — `selected: no dates`
  present-all-hidden  `R`, then `space` until every task is hidden — no cursor,
                      the presentation's tick label blank
One PNG at 118x31 is Edge's raster of `gantt-selected`, made with the app's own
`views.save_present_png`. Nothing in `taskboard/` is patched.
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
from taskboard import models, views  # noqa: E402

OUT = HERE / "captures"
SIZES = [(118, 31), (80, 25)]


class _Today(date):
    @classmethod
    def today(cls):
        return pb.TODAY


app_mod.date = _Today
models.date = _Today
views.date = _Today


async def _session(size, plan, dateless=False) -> list[Path]:
    tmp = Path(tempfile.mkdtemp())
    board = pb.build(tmp / "board.json")
    if dateless:
        t = board.task_by_id(pb.CURSOR)
        t.start_date = t.due_date = None
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
        for step, keys in plan:
            for k in keys:
                await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            svg = app.export_screenshot(title=f"taskboard · 001 · {step}")
            path = OUT / f"app-001-{size[0]}x{size[1]}-{step}.svg"
            path.write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")
            written.append(path)
    return written


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for size in SIZES:
        shots = asyncio.run(_session(size, [
            ("gantt-selected", ["3"]),
            ("gantt-none", ["slash", *"zzqx", "enter"])]))
        shots += asyncio.run(_session(size, [("gantt-nodates", ["3"])], dateless=True))
        shots += asyncio.run(_session(size, [("present-all-hidden", ["R"] + ["space"] * 10)]))
        for p in shots:
            print(p.relative_to(ROOT).as_posix())
    svg = OUT / "app-001-118x31-gantt-selected.svg"
    png = views.save_present_png(svg, svg.with_suffix(".png"), 118, 31)
    print(png.relative_to(ROOT).as_posix() if png else "png: Edge absent or the render failed")


if __name__ == "__main__":
    main()

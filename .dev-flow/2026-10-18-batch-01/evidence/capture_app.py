"""Capture present v3 FROM THE RUNNING APP (batch 2026-10-18-batch-01).

    python .dev-flow/2026-10-18-batch-01/evidence/capture_app.py

Batch 2026-10-17-batch-01's `capture_app.py`, re-aimed at the presentation's two
views: the real `TaskboardApp` runs headless on the notes board (synthetic,
`tests/present_notes_board.py`, the prototype round's notes) with the calendar
frozen on the board's TODAY; keys are pressed through the pilot as a user
would, and every frame is the app's own `export_screenshot()` SVG, written as
`captures/app-002-<w>x<h>-<n>-<step>.svg`. The starting selection is the
oracle cursor (`tw3`, Fix checkout 500 error). Nothing in `taskboard/` is
patched.

Steps, per size (each continues from the one before):
  1 gantt-open    `R` — the gantt view, as `R` always opens
  2 gantt-long    `→ →` — the long numbered note under the cursor, its lines kept
  3 split-open    `← ←`, `2` — the split view, cursor back on tw3
  4 split-moved   `→` — the cursor moved (Optimize image assets)
  5 split-long    `→` — the long note under the cursor
  6 split-pgdn    `pgdn` — its next page
  7 split-hidden  `←`, `space` — Optimize image assets hidden, out of both parts
The 118x31 SVGs are rasterised to PNG with the app's own
`views.save_present_png` (headless Edge).
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

import present_notes_board as nb  # noqa: E402
from taskboard import app as app_mod  # noqa: E402
from taskboard import models, views  # noqa: E402

OUT = HERE / "captures"
SIZES = [(118, 31), (80, 25)]
PLAN = [("gantt-open", ["R"]),
        ("gantt-long", ["right", "right"]),
        ("split-open", ["left", "left", "2"]),
        ("split-moved", ["right"]),
        ("split-long", ["right"]),
        ("split-pgdn", ["pagedown"]),
        ("split-hidden", ["left", "space"])]


class _Today(date):
    @classmethod
    def today(cls):
        return nb.TODAY


app_mod.date = _Today
models.date = _Today
views.date = _Today


async def _session(size) -> list[Path]:
    tmp = Path(tempfile.mkdtemp())
    nb.build(tmp / "board.json").save()
    app = app_mod.TaskboardApp(board_path=str(tmp / "board.json"))
    written = []
    async with app.run_test(size=size) as pilot:
        for _ in range(50):
            if type(app.screen).__name__ == "MilestoneOffer":
                await pilot.press("escape")
                break
            await pilot.pause()
        await pilot.pause()
        app.selected_task_id = nb.CURSOR
        for n, (step, keys) in enumerate(PLAN, 1):
            for k in keys:
                await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            svg = app.export_screenshot(title=f"taskboard · R present · {step}")
            path = OUT / f"app-002-{size[0]}x{size[1]}-{n}-{step}.svg"
            path.write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")
            written.append(path)
    return written


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for size in SIZES:
        for p in asyncio.run(_session(size)):
            print(p.relative_to(ROOT).as_posix())
            if size == (118, 31):
                png = views.save_present_png(p, p.with_suffix(".png"), *size)
                print(png.relative_to(ROOT).as_posix() if png else "png: Edge absent or failed")


if __name__ == "__main__":
    main()

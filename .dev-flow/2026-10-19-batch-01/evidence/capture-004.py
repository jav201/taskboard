"""Real-app captures of batch 2026-10-19-batch-01 (NO_COLOR unset).

    python .dev-flow/2026-10-19-batch-01/evidence/capture.py <out_dir> <scenario>...   (from a checkout's root)

The shipped `TaskboardApp` runs headless (`run_test`) over the present-portfolio
round's synthetic board (`tests/present_portfolio_board.py`) with the calendar
frozen on its TODAY; keys go through the pilot; each frame is the app's own
`export_screenshot()` SVG. Nothing is subclassed or patched but the date.
Scenarios: view1 (R at 118x31), v3-160, v3-118, v3-80 (R, 3), seq (160x45: the
hide -> reorder -> u picker -> show sequence, and the x export)."""
from __future__ import annotations

import asyncio
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import present_portfolio_board as pf  # noqa: E402
from taskboard import app as app_module  # noqa: E402
from taskboard import models  # noqa: E402


class _Today(date):
    @classmethod
    def today(cls):
        return pf.TODAY


app_module.date = _Today
models.date = _Today


def _save(app, out: Path, name: str) -> None:
    svg = app.export_screenshot(title=f"taskboard · R present · {name}")
    (out / f"{name}.svg").write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")


def _at(scr, target: str) -> bool:
    cur = getattr(scr, "_all_cur", None)
    return cur is not None and cur[1] == target


async def _goto(pilot, scr, target: str) -> None:
    """`↓` then `↑` until the view-3 cursor sits on `target` (a project or task id)."""
    for key in ("down", "up"):
        for _ in range(40):
            if _at(scr, target):
                return
            await pilot.press(key)
            await pilot.pause()
    raise AssertionError(f"cursor never reached {target}: {getattr(scr, '_all_cur', None)}")


async def run(out: Path, name: str, size, steps) -> None:
    tmp = Path(tempfile.mkdtemp())
    pf.build(tmp / "board.json").save()
    app = app_module.TaskboardApp(board_path=str(tmp / "board.json"))
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.selected_task_id = pf.CURSOR
        await pilot.press("R")
        await pilot.pause()
        for frame, keys in steps:
            for k in keys:
                if k.startswith("@"):
                    await _goto(pilot, app.screen if type(app.screen).__name__ == "PresentScreen"
                                else app.screen_stack[-2], k[1:])
                else:
                    await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            _save(app, out, f"{name}-{frame}" if frame else name)
    for svg in (tmp / "reports").glob("*.svg"):
        shutil.copy(svg, out / f"{name}-export-{svg.name}")


SCENARIOS = {
    "view1": ("view1-118x31", (118, 31), [("", [])]),
    "v3-160": ("view3-160x45", (160, 45), [("", ["3"])]),
    "v3-118": ("view3-118x30", (118, 30), [("", ["3"])]),
    "v3-80": ("view3-80x24", (80, 24), [("", ["3"])]),
    "seq": ("seq-160x45", (160, 45), [
        ("1-view3", ["3"]),
        ("2-hidden", ["right", "@pbr", "space"]),
        ("3-reordered", ["left", "@pmr", "shift+up", "shift+up"]),
        ("4-picker", ["u"]),
        ("5-shown", ["down", "space", "escape"]),
        ("6-exported", ["x"]),
    ]),
}


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for key in sys.argv[2:]:
        name, size, steps = SCENARIOS[key]
        asyncio.run(run(out, name, size, steps))
        print("captured", key)


if __name__ == "__main__":
    main()

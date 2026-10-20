"""Real-app captures of the SHIPPED multi-board code (batch 2026-10-20-batch-01).

    unset NO_COLOR; PYTHONUTF8=1 python .dev-flow/2026-10-20-batch-01/evidence/capture.py [PNG_DIR]

Every frame is `taskboard.__main__.open_app` — the app `taskboard` starts — over the
round's four synthetic boards (`tests/multi_board_fixture.py`) in a temporary home,
driven by real keys through `run_test`, saved with `export_screenshot()`. The
calendar and the clock are frozen at 2026-10-20 09:30. Writes SVGs beside this
script in `captures/`; with PNG_DIR, rasterises each with headless Edge.
"""
from __future__ import annotations

import asyncio
import os
import re
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import multi_board_fixture as mb  # noqa: E402
from taskboard import app as app_mod, modals, models, views  # noqa: E402
import taskboard.__main__ as entry  # noqa: E402
from taskboard.models import Board, Project, Task  # noqa: E402

OUT = HERE / "captures"


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 10, 20, 9, 30)


for mod in (app_mod, models, views, modals):
    mod.date = _Today
app_mod.datetime = _Now
entry.datetime = _Now


def _save(app, name: str) -> None:
    svg = app.export_screenshot(title=f"taskboard · {name}")
    (OUT / f"{name}.svg").write_text(re.sub(r"@font-face\s*\{[^}]*\}", "", svg), encoding="utf-8")


async def run(size, steps, last="personal", single=False):
    home = Path(tempfile.mkdtemp())
    Path.home = classmethod(lambda cls: home)
    tb = home / ".taskboard"
    if single:
        board = mb.build_board(tb, "main")
        board.settings["seen_view_renumber_2026_07"] = True
        board.save()
    else:
        mb.build(tb, last)
    app = entry.open_app(None)
    async with app.run_test(size=size) as pilot:
        for _ in range(4):
            await pilot.pause()
        for name, keys in steps:
            for k in keys:
                if k.startswith("@type:"):
                    box = app.focused
                    box.value = k[6:]
                    box.cursor_position = len(box.value)
                else:
                    await pilot.press(k)
                await pilot.pause()
            await pilot.pause()
            await pilot.pause()
            _save(app, name)


def to_png(png_dir: Path) -> int:
    exe = None
    for base in (os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                 os.environ.get("ProgramFiles", r"C:\Program Files")):
        cand = Path(base) / "Microsoft" / "Edge" / "Application" / "msedge.exe"
        if cand.is_file():
            exe = str(cand)
    if exe is None:
        print("no Edge: PNGs skipped")
        return 0
    png_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for svg in sorted(OUT.glob("*.svg")):
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8"))
        w, h = (int(float(m.group(1))) + 4, int(float(m.group(2))) + 4) if m else (1700, 1000)
        png = png_dir / f"{svg.stem}.png"
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={png}", f"--window-size={w},{h}", svg.as_uri()],
                       capture_output=True, timeout=60)
        n += png.exists()
    return n


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for w, h in ((160, 45), (118, 30), (80, 24)):
        asyncio.run(run((w, h), [(f"home-{w}x{h}", [])]))
    asyncio.run(run((160, 45), [("switched-160x45", ["right", "enter"]),
                                ("switched-gantt-160x45", ["3"])]))
    asyncio.run(run((160, 45), [("create-160x45-1-form", ["n", "@type:Course · Kubernetes", "tab"]),
                                ("create-160x45-2-created", ["enter"])]))
    asyncio.run(run((80, 24), [("create-80x24-form", ["n", "@type:Course · Kubernetes"])]))
    asyncio.run(run((160, 45), [("move-160x45-0-main-before", ["escape"]),
                                ("move-160x45-1-projects", ["P", "down"]),
                                ("move-160x45-2-target", ["m", "down"]),
                                ("move-160x45-3-confirm", ["enter"]),
                                ("move-160x45-4-moved", ["enter"]),
                                ("move-160x45-5-main-after", ["escape"]),
                                ("move-160x45-6-client-after", ["B", "up", "enter"])],
                    last="main"))
    asyncio.run(run((80, 24), [("move-80x24-confirm", ["escape", "P", "down", "m", "down", "enter"])],
                    last="main"))
    asyncio.run(run((160, 45), [("single-board-160x45", [])], single=True))
    print("wrote", len(list(OUT.glob("*.svg"))), "svg to", OUT)
    if len(sys.argv) > 1:
        print("png:", to_png(Path(sys.argv[1]).resolve()))


if __name__ == "__main__":
    main()

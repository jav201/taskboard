"""Captures for batch 2026-10-04-batch-01 (B1 links) — SVG + painted text.

    python -B capture_b1.py TREE TAG OUTDIR [SURFACE ...]

TREE is the repo tree to import `taskboard` from (the working tree at base before
any product change, then after); TAG prefixes the files (`base`, `close`). The
board is `tests/kg_board.py`'s, saved in a fresh temp directory (synthetic only;
no user data directory is read or written). Each surface is driven through the
app's own keys and saved as `<TAG>-<surface>-<W>x<H>.svg` and `.txt` at 118x30
and 80x24. Prints no absolute path.

Surfaces: kanban, kanban-lanes, gantt, details (base and close); picker,
gantt-link, guard, ready, migration (close only: they do not exist at base)."""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

TREE, TAG, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
SURFACES = sys.argv[4:] or ["kanban", "kanban-lanes", "gantt", "details"]
sys.path.insert(0, str(TREE))
sys.path.insert(0, str(TREE / "tests"))

import kg_board                                              # noqa: E402
from taskboard.app import TaskboardApp                       # noqa: E402

assert Path(sys.modules["taskboard"].__file__).resolve().is_relative_to(TREE.resolve())

SIZES = tuple(tuple(int(n) for n in wh.split("x")) for wh in
              os.environ.get("CAPTURE_SIZES", "118x30,80x24").split(","))


def _legacy(path: Path) -> None:
    """An unmigrated board as the shipped app left it: `kg_board.legacy` (the shapes
    L1..L8, no migration mark), with the renumber notice seen so the migration's
    toast is the one on screen."""
    b = kg_board.legacy(path, old_done=False)
    b.settings["seen_view_renumber_2026_07"] = True
    b.save()


async def shot(surface: str, size) -> None:
    d = Path(tempfile.mkdtemp())
    path = d / "board.json"
    if surface == "migration":
        _legacy(path)
    else:
        kg_board.build(path).save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=size, notifications=True) as pilot:
        await pilot.pause()
        if surface != "migration":          # its toast IS the subject
            app.clear_notifications()       # the startup notices are not the subject
        keys: list[str] = []
        select = "tm3"
        if surface in ("kanban", "details", "picker", "guard", "ready", "migration"):
            keys = ["4"]
        elif surface == "kanban-lanes":
            keys = ["4", "tab", "tab"]     # lanes (one tab is the matrix — ux E-1)
        elif surface in ("gantt", "gantt-link"):
            keys = ["3"]
        for k in keys:
            await pilot.press(k)
            await pilot.pause()
        if surface == "guard":
            select = "ta3"
        elif surface == "ready":
            select = "tm2"
        elif surface == "picker" or surface == "gantt-link":
            select = "tw5"
        app.selected_task_id = select
        app.refresh_view()
        await pilot.pause()
        if surface == "details":
            await pilot.press("enter")
        elif surface in ("picker", "gantt-link"):
            await pilot.press("L")
            if surface == "gantt-link":
                await pilot.pause()
                await pilot.press(*"push")     # tm3: due 9 days into tw5 — the `═` shows
        elif surface == "guard":
            await pilot.press("x")
        elif surface == "ready":
            await pilot.press("]")
            await pilot.pause()
            await pilot.press("]")
        for _ in range(4):
            await pilot.pause()
        stem = f"{TAG}-{surface}-{size[0]}x{size[1]}"
        app.save_screenshot(f"{stem}.svg", str(OUT))
        strips = app.screen._compositor.render_strips(app.screen.size)
        (OUT / f"{stem}.txt").write_text("\n".join(s.text.rstrip() for s in strips) + "\n",
                                         encoding="utf-8")
        print(stem)


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for surface in SURFACES:
        for size in SIZES:
            await shot(surface, size)


asyncio.run(main())

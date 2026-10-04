"""Captures of the task details view (PV-1, increment 003) — SVG + painted text.

    python -B capture_details.py TREE TAG OUTDIR

TREE is the repo tree to import `taskboard` from (a `git archive` export for the
base, the working tree for the change); TAG prefixes the files (`base`, `after`).
For each terminal size and each project name (short, and the 89-character `LONG`
of `p1_grid_threshold.py`), the app opens the details view with `enter` and the
screen is saved as `<TAG>-details-<W>x<H>[-long].svg` and `.txt`. Prints no
absolute path."""
from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

TREE, TAG, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(TREE))

from taskboard.app import TaskboardApp                    # noqa: E402
from taskboard.models import Board, Project, Task           # noqa: E402

assert Path(sys.modules["taskboard"].__file__).resolve().is_relative_to(TREE.resolve())

LONG = ("Website relaunch for the northern region customer portal and partner "
        "onboarding phase two")


async def shot(size, name, suffix):
    d = Path(tempfile.mkdtemp())
    b = Board.load(d / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project(name, "sky")
    b.projects.append(p)
    b.tasks.append(Task("Write the launch checklist", p.id, "Doing", priority="high",
                        start_date="2026-10-01", due_date="2026-10-09",
                        notes="Draft the ==owner list== and the !!rollback plan!!.\n"
                              "Review with ++ops++ on Friday.",
                        urls=["https://example.com/launch"]))
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        app.selected_task_id = app.board.tasks[0].id
        await pilot.press("enter")
        for _ in range(4):
            await pilot.pause()
        stem = f"{TAG}-details-{size[0]}x{size[1]}{suffix}"
        app.save_screenshot(f"{stem}.svg", str(OUT))
        strips = app.screen._compositor.render_strips(app.screen.size)
        (OUT / f"{stem}.txt").write_text("\n".join(s.text.rstrip() for s in strips) + "\n",
                                         encoding="utf-8")
        print(stem)


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for size in ((140, 40), (80, 24)):
        await shot(size, "Website", "")
        await shot(size, LONG, "-long")


asyncio.run(main())

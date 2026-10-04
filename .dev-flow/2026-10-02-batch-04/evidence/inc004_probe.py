"""Measure the details view: rows between the box's top border and the title, rows
between the title and the first field, label column width, field visibility.

    python -B probe.py TREE
"""
import asyncio, sys, tempfile
from pathlib import Path
TREE = Path(sys.argv[1]); sys.path.insert(0, str(TREE))
from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
assert Path(sys.modules["taskboard"].__file__).resolve().is_relative_to(TREE.resolve())
LONG = ("Website relaunch for the northern region customer portal and partner "
        "onboarding phase two")
FIELDS = ["Project", "Phase", "Priority", "Start", "Due"]


async def one(size, name):
    d = Path(tempfile.mkdtemp()); b = Board.load(d / "board.json")
    b.projects.clear(); b.tasks.clear(); p = Project(name, "sky"); b.projects.append(p)
    b.tasks.append(Task("Write the launch checklist", p.id, "Doing", priority="high",
                        start_date="2026-10-01", due_date="2026-10-09")); b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=size) as pilot:
        await pilot.pause(); app.selected_task_id = app.board.tasks[0].id
        await pilot.press("enter")
        for _ in range(4): await pilot.pause()
        box = app.screen.query_one("#details-box")
        title = box.query_one(".modal-title")
        grid = box.query_one(".modal-grid")
        cells = list(grid.children)
        strips = app.screen._compositor.render_strips(app.screen.size)
        r = box.region
        rows = [strips[y].text[r.x + 1:r.x + r.width - 1] for y in range(r.y, r.y + r.height)]
        above = title.region.y - (r.y + 1)
        below = cells[0].region.y - (title.region.y + title.region.height)
        labw = cells[0].region.width
        valx = cells[1].region.x - cells[0].region.x
        firsts = [row.split()[0] for row in rows if row.split() and row.split()[0] in FIELDS]
        print(f"{size[0]}x{size[1]} {'long' if name == LONG else 'short'}: above={above} "
              f"below={below} label_w={labw} value_dx={valx} title_h={title.region.height} "
              f"visible={firsts == FIELDS} proj_rows={cells[1].region.height}")


async def main():
    for size in ((140, 40), (80, 24)):
        for name in ("Website", LONG):
            await one(size, name)

asyncio.run(main())

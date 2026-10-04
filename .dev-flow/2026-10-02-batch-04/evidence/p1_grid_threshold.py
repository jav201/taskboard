"""C-39 pre-execution of HLR-403's thresholds (P2 Q2-11): the REAL TaskboardApp, a
subclass whose CSS appends the planned rule (the repo stylesheet is untouched), the
details view opened with `enter`. Prints geometry only — no absolute path.
    python -B .dev-flow/2026-10-02-batch-04/evidence/p1_grid_threshold.py"""
from __future__ import annotations

import asyncio
import contextlib
import io
import tempfile
from pathlib import Path

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import ClockModal, ProjectModal

RULE = "#details-box .modal-grid Label { margin-top: 0; height: auto; }"
LONG = ("Website relaunch for the northern region customer portal and partner "
        "onboarding phase two")                                   # 89 chars, spaces


def make(name, rule):
    d = Path(tempfile.mkdtemp())
    b = Board.load(d / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project(name, "sky")
    b.projects.append(p)
    b.tasks.append(Task("Write the spec", p.id, "Doing", priority="high",
                        start_date="2026-10-01", due_date="2026-10-09", notes="n"))
    b.save()

    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    app._probe_rule = rule
    return app


def apply_rule(app):
    """The shipped sheet, then the planned rule, added to the live stylesheet."""
    if app._probe_rule:
        app.stylesheet.add_source(app._probe_rule, read_from=("probe", "rule"))
        app.refresh_css()


async def details(size, name, rule):
    app = make(name, rule)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        apply_rule(app)
        app.selected_task_id = app.board.tasks[0].id
        await pilot.press("enter")
        for _ in range(3):
            await pilot.pause()
        box = app.screen.query_one("#details-box")
        grid = app.screen.query_one(".modal-grid")
        cells = [(str(w.render())[:12], w.region.y, w.region.height, w.region.x)
                 for w in grid.children]
        visible = all(box.region.y <= c[1] and c[1] + max(c[2], 1) <= box.region.y + box.region.height
                      for c in cells)
        strips = app.screen._compositor.render_strips(app.screen.size)
        r = box.region
        painted = "\n".join(s.text[r.x:r.x + r.width] for s in strips[r.y:r.y + r.height])
        joined = " ".join(painted.replace("│", " ").split())   # the border is not text
        return cells, visible, " ".join(name.split()) in joined, box.max_scroll_y


async def edit_heights(rule):
    out = {}
    for label, screen in (("ProjectModal", lambda b: ProjectModal(b.projects[0])),
                          ("ClockModal", lambda b: ClockModal("Tokyo", "London"))):
        app = make("Alpha", rule)
        async with app.run_test(size=(140, 40)) as pilot:
            await pilot.pause()
            apply_rule(app)
            app.push_screen(screen(app.board))
            for _ in range(3):
                await pilot.pause()
            grid = app.screen.query_one(".modal-grid")
            out[label] = [w.region.height for w in grid.children]
    return out


async def main():
    for rule_name, rule in (("base", ""), ("planned", RULE)):
        for size in ((140, 40), (80, 24)):
            for name in ("Alpha", LONG):
                cells, vis, whole, scroll = await details(size, name, rule)
                print(f"{rule_name:8} {size[0]}x{size[1]} name={len(name):>2} chars: "
                      f"cell heights {[c[2] for c in cells]}, rows {[c[1] for c in cells]}, "
                      f"value x {sorted({c[3] for c in cells[1::2]})}, "
                      f"five rows visible at scroll 0: {vis}, name painted whole: {whole}, "
                      f"max_scroll_y {scroll}")
        print(f"{rule_name:8} edit-modal grid cell heights:", await edit_heights(rule))


if __name__ == "__main__":
    sink = io.StringIO()
    with contextlib.redirect_stderr(sink):
        asyncio.run(main())

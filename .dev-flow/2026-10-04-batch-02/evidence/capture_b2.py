"""Captures for batch 2026-10-04-batch-02 (B2a milestones) — SVG + painted text.

    python -B capture_b2.py TREE TAG OUTDIR [SURFACE ...]

TREE is the repo tree to import `taskboard` from (the working tree at base before any
product change, then after); TAG prefixes the files (`base`, `close`). The board is
`tests/kg_board.py`'s shifted to today (`kg_board.shifted`), re-derived here into the prototype's two round-5 boards
(`variants_round5.one_day_board` / `milestone_board`): the base tree has no milestone
field, so at base the "milestone" board is the one-day board (the operator's habit
today). Saved in a fresh temp directory (synthetic only; no user data directory is
read or written). Each surface is driven through the app's own keys and saved as
`<TAG>-<surface>-<W>x<H>.svg` and `.txt` at 118x30 and 80x24. Prints no absolute path.

Surfaces: gantt, kanban, kanban-lanes, kanban-matrix, editor, details (base and close);
offer, legend-gantt, gantt-reached (close only)."""
from __future__ import annotations

import asyncio
import os
import sys
import tempfile
from datetime import timedelta
from pathlib import Path

TREE, TAG, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
SURFACES = sys.argv[4:] or ["gantt", "kanban", "kanban-lanes", "kanban-matrix", "editor",
                            "details"]
sys.path.insert(0, str(TREE))
sys.path.insert(0, str(TREE / "tests"))

import kg_board                                              # noqa: E402
from taskboard.app import TaskboardApp                       # noqa: E402
from taskboard.models import Task                            # noqa: E402
from datetime import date                                    # noqa: E402

assert Path(sys.modules["taskboard"].__file__).resolve().is_relative_to(TREE.resolve())

SIZES = tuple(tuple(int(n) for n in wh.split("x")) for wh in
              os.environ.get("CAPTURE_SIZES", "118x30,80x24").split(","))
HAS_FLAG = "milestone" in Task.__dataclass_fields__


def one_day(b):
    """The operator's habit: milestones typed as one-day tasks (start == due)."""
    for tid, off in (("tw5", 10), ("tm5", 35), ("ta3", 3)):
        t = b.task_by_id(tid)
        t.start_date = t.due_date = (date.today() + timedelta(days=off)).isoformat()
    return b


def milestones(b):
    """`one_day` converted, plus one reached, one late and one ahead (round 5)."""
    one_day(b)
    if not HAS_FLAG:
        return b
    for tid in ("tw5", "tm5", "ta3"):
        b.task_by_id(tid).milestone = True

    def add(tid, pid, title, phase, off, deps):
        d = (date.today() + timedelta(days=off)).isoformat()
        b.tasks.append(Task(title, project_id=pid, phase=phase, start_date=d, due_date=d,
                            depends_on=deps, phase_changed=d, milestone=True, id=tid))
    add("tw0", "pweb", "Mockups approved", b.phases[-1], -12, ["tw1"])
    add("to0", "pops", "Security review sign-off", "Next", -2, [])
    add("td0", "pdwh", "Revenue model signed off", "Backlog", 18, ["td4"])
    b.task_by_id("td5").depends_on = ["td0"]
    return b


async def shot(surface: str, size) -> None:
    d = Path(tempfile.mkdtemp())
    path = d / "board.json"
    b = kg_board.shifted(path)        # the AT board: dates moved to today (qa Q-23)
    if surface == "offer":
        one_day(b)                         # unmarked for milestones: the offer opens
    else:
        milestones(b)
        if surface == "gantt-reached" and HAS_FLAG:   # three reached in one group (ux UX-10)
            for tid, title, off in (("tw8", "Brand guide signed", -9), ("tw9", "Copy deck frozen", -5)):
                d = (date.today() + timedelta(days=off)).isoformat()
                b.tasks.append(Task(title, project_id="pweb", phase=b.phases[-1], start_date=d,
                                    due_date=d, phase_changed=d, milestone=True, id=tid))
        b.settings.setdefault("migrations", {})["milestones"] = 1
    b.settings["seen_view_renumber_2026_07"] = True
    b.save()
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=size, notifications=True) as pilot:
        await pilot.pause()
        if surface != "offer":
            app.clear_notifications()
        keys: list[str] = []
        select = "tw3"
        if surface in ("gantt", "legend-gantt", "gantt-reached"):
            keys, select = ["3"], "tw5"
        elif surface == "kanban" or (surface in ("editor", "details") and TAG == "base"):
            keys = ["4"]
        elif surface in ("editor", "details"):     # close: the gantt, real keys (ux UXV-1)
            keys = ["3"]
        elif surface == "kanban-lanes":
            keys = ["4", "tab", "tab"]
        elif surface == "kanban-matrix":
            keys = ["4", "tab"]
        for k in keys:
            await pilot.press(k)
            await pilot.pause()
        if surface in ("editor", "details"):
            select = "tw5"
        if surface in ("editor", "details") and TAG != "base":
            for _ in range(80):                    # walk to the milestone; the kanban
                if app.selected_task_id == select:  # never selects one (D-614)
                    break
                await pilot.press("down")
                await pilot.pause()
            assert app.selected_task_id == select, app.selected_task_id
        elif surface != "offer":
            app.selected_task_id = select
            app.refresh_view()
            await pilot.pause()
        if surface == "details":
            await pilot.press("enter")
        elif surface == "editor":
            await pilot.press("e")
        elif surface == "legend-gantt":
            await pilot.press("question_mark")
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

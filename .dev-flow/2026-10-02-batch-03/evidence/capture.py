"""Cell-exact captures of the KANBAN on the oracle board (tests/kg_board.py — never a
real board) at the operator's panel sizes, as SVG + text, plus the readability table;
and the running app's whole screen at terminal sizes. Recipe of batches 01/02
(`2026-10-02-batch-02/evidence/capture.py`): a recording Console WIDTH + 2 wide.

    python <this file> OUT_DIR LABEL        (cwd = the tree to capture)

Frames: the oracle selection `tw3` at panels 118x30, 80x24, 80x22; the selection in
Ops & Security (`to3`, the fold seen from below); `g` -> priority and horizon (PV-7);
a 14-high board (the cap, PV-2); the app at terminals 118x30, 120x32, 80x24.
"""
import asyncio
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "tests"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True

from rich.console import Console  # noqa: E402

import kg_board  # noqa: E402
from readability import body, readability  # noqa: E402
from taskboard.models import Task  # noqa: E402
from taskboard.views import render_view  # noqa: E402

PANELS = ((118, 30), (80, 24), (80, 22))


def many_highs():
    b = kg_board.build()
    pids = [p.id for p in b.projects]
    for i in range(10):
        b.tasks.append(Task(f"Urgent item {i + 1}", pids[i % len(pids)], "Backlog", "high",
                            due_date=kg_board._d(5 + i), phase_changed=kg_board._d(-3),
                            id=f"tx{i}"))
    return b


def save(text, w, h, path: Path, title: str) -> None:
    con = Console(width=w + 2, height=h + 4, force_terminal=True, color_system="truecolor",
                  record=True, file=open(os.devnull, "w", encoding="utf-8"))
    con.print(text, end="")
    path.with_suffix(".txt").write_text(con.export_text(clear=False), encoding="utf-8")
    con.save_svg(str(path), title=title)


def views(out: Path, label: str) -> list[str]:
    report = []
    frames = [("kanban", kg_board.build, "tw3", {}), ("kanban-ops", kg_board.build, "to3", {}),
              ("kanban-priority", kg_board.build, "tw3", {"kanban_group": "priority"}),
              ("kanban-horizon", kg_board.build, "tw3", {"kanban_group": "horizon"}),
              ("kanban-14high", many_highs, "tw3", {})]
    for w, h in PANELS:
        for name, build, sel, kw in frames:
            b = build()
            text = render_view("kanban", b, False, sel, kg_board.TODAY, w, h, {}, **kw)
            save(text, w, h, out / f"{label}-{name}-{w}x{h}.svg",
                 f"taskboard · {name} · {label} · {w}x{h}")
            if name == "kanban":
                avg, full, drawn = readability(body(text.plain.split("\n"), h),
                                               [t.title for t in b.tasks])
                report.append(f"{label} {w}x{h}: avg/28 {avg:.1f} · full {full} · drawn {drawn}")
    return report


def app_screens(out: Path, label: str) -> None:
    from taskboard import app as app_mod, models, views as views_mod
    from taskboard.app import TaskboardApp

    class _Today(kg_board.date):
        @classmethod
        def today(cls):
            return kg_board.TODAY

    for mod in (views_mod, app_mod, models):
        mod.date = _Today

    async def run(size):
        tmp = Path(tempfile.mkdtemp(prefix="kg-app-"))
        b = kg_board.build(tmp / "board.json")
        b.save()
        app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
        async with app.run_test(size=size) as pilot:
            await pilot.pause()
            await pilot.press("4")
            await pilot.pause()
            app.selected_task_id = "tw3"
            app.refresh_view()
            await pilot.pause()
            w, h = size
            (out / f"{label}-app-kanban-{w}x{h}.svg").write_text(
                app.export_screenshot(title=f"taskboard · app · {label} · {w}x{h}"),
                encoding="utf-8")

    for size in ((118, 30), (120, 32), (80, 24)):
        asyncio.run(run(size))


def main() -> None:
    out, label = Path(sys.argv[1]), sys.argv[2]
    out.mkdir(parents=True, exist_ok=True)
    report = views(out, label)
    app_screens(out, label)
    (out / f"readability-{label}.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()

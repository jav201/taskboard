"""Cell-exact captures of every view on the oracle board (tests/kg_board.py — never a
real board) plus a scratch team directory, history file and Setup state, at the
operator's two panel sizes, as SVG + text; and the running app's whole screen
(key bar, ribbon, the help modal) at the two terminal sizes.

    python <this file> OUT_DIR LABEL [view,view,...|app]     (cwd = the tree to capture)

The rich recipe of batch-01's capture.py: a recording Console WIDTH + 2 wide.
"""
import asyncio
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "tests"))

from rich.console import Console  # noqa: E402

import kg_board  # noqa: E402
from taskboard import history  # noqa: E402
from taskboard.team_sync import TEAM_FILENAME, TeamState  # noqa: E402
from taskboard.views import render_view  # noqa: E402

SIZES = ((118, 30), (80, 24))
SELECTED = "tw3"
VIEWS = ["swimlanes", "agenda", "gantt", "kanban", "focus", "flow", "standup", "people",
         "setup"]


def fixtures(tmp: Path):
    b = kg_board.build(tmp / "board.json")
    b.task_by_id("tw6").urls = ["https://example.org/redirects"]
    for tid in ("tw3", "ta4"):
        b.task_by_id(tid).pinned = True
    for i, (tid, frm, to) in enumerate([("tw3", "Next", "Doing"), ("tw2", "Doing", "Review"),
                                        ("tw1", "Review", "Done")]):
        history.append(b.path, {"task": tid, "from": frm, "to": to},
                       at=datetime(2026, 9, 20 + i, 10))
    cfg = {"version": 3, "phases": kg_board.PHASES,
           "projects": [{"id": "pweb", "name": "Website Redesign", "color": "violet",
                         "status": "on_track"}],
           "roster": [{"id": "jav", "name": "Javier", "hue": "sky"},
                      {"id": "ana", "name": "Ana", "hue": "amber"}]}
    (tmp / TEAM_FILENAME).write_text(json.dumps(cfg), encoding="utf-8")
    st = TeamState(tmp, user_id="jav")
    st.load_config()
    setup = {"enabled": True, "shared_dir": "D:/team", "interval_minutes": 30,
             "user_id": "jav", "projects": [{"id": "pweb", "name": "Website Redesign",
                                             "shared": True, "color": "violet"}],
             "roster": [{"id": "jav", "name": "Javier", "hue": "sky"}],
             "cursor_section": 0, "cursor_row": 1}
    return b, st, setup


def save(con: Console, path: Path, title: str) -> None:
    path.with_suffix(".txt").write_text(con.export_text(clear=False), encoding="utf-8")
    con.save_svg(str(path), title=title)


def views(out: Path, label: str, which: list[str]) -> None:
    tmp = Path(tempfile.mkdtemp(prefix="kg-cap-"))
    b, st, setup = fixtures(tmp)
    for w, h in SIZES:
        for mode in which:
            kw = {"team_state": st} if mode in ("standup", "people") else {}
            if mode == "setup":
                kw = {"setup_state": setup, "team_state": st}
            text = render_view(mode, b, False, SELECTED, kg_board.TODAY, w, h, {}, **kw)
            con = Console(width=w + 2, height=h + 4, force_terminal=True,
                          color_system="truecolor", record=True,
                          file=open(os.devnull, "w", encoding="utf-8"))
            con.print(text, end="")
            save(con, out / f"{label}-{mode}-{w}x{h}.svg",
                 f"taskboard · {mode} · {label} · {w}x{h}")


def app_screens(out: Path, label: str) -> None:
    """The whole terminal: the gantt with its key bar and ribbon, then `?`."""
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
            await pilot.press("3")
            await pilot.pause()
            app.selected_task_id = SELECTED
            app.refresh_view()
            await pilot.pause()
            w, h = size
            (out / f"{label}-app-gantt-{w}x{h}.svg").write_text(
                app.export_screenshot(title=f"taskboard · app · {label} · {w}x{h}"),
                encoding="utf-8")
            await pilot.press("question_mark")
            await pilot.pause()
            (out / f"{label}-app-help-{w}x{h}.svg").write_text(
                app.export_screenshot(title=f"taskboard · help · {label} · {w}x{h}"),
                encoding="utf-8")

    for size in SIZES:
        asyncio.run(run(size))


def main() -> None:
    out, label = Path(sys.argv[1]), sys.argv[2]
    which = sys.argv[3].split(",") if len(sys.argv) > 3 else VIEWS + ["app"]
    out.mkdir(parents=True, exist_ok=True)
    vs = [v for v in which if v != "app"]
    if vs:
        views(out, label, vs)
    if "app" in which:
        app_screens(out, label)
    print("ok", label, which)


if __name__ == "__main__":
    main()

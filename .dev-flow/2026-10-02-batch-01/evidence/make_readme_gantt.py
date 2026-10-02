"""Regenerate docs/taskboard-gantt.svg: the gantt on the SEEDED DEMO board (never a
real board — the board is created fresh in a temporary directory), 96x26, the
first task of the gantt's walk selected. Run from the project root:
    python .dev-flow/2026-10-02-batch-01/evidence/make_readme_gantt.py
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())

from rich.console import Console  # noqa: E402

from taskboard.models import Board  # noqa: E402
from taskboard.views import nav_model, render_view  # noqa: E402

W, H = 96, 26
with tempfile.TemporaryDirectory() as d:
    board = Board.load(str(Path(d) / "board.json"))        # seeds the demo data
    walk = nav_model("gantt", board, False, None, W, H)[0]
    text = render_view("gantt", board, False, walk[0] if walk else None, None, W, H, {})
    con = Console(width=W + 2, height=H + 4, force_terminal=True, color_system="truecolor",
                  record=True, file=open(os.devnull, "w", encoding="utf-8"))
    con.print(text, end="")
    con.save_svg("docs/taskboard-gantt.svg", title="taskboard · gantt")
print("ok docs/taskboard-gantt.svg")

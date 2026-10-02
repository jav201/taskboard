"""Cell-exact captures of the gantt and kanban on the oracle board (tests/kg_board.py,
never a real board), at the operator's two panel sizes, as SVG + text.

    python <this file> OUT_DIR LABEL        (cwd = the tree to capture)

The rich recipe of the prototype round: a recording Console WIDTH + 2 wide (the
SVG frame) and tall enough for every row.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "tests"))

from rich.console import Console  # noqa: E402

import kg_board  # noqa: E402
from taskboard.views import render_view  # noqa: E402

SIZES = ((118, 30), (80, 24))
SELECTED = "tw3"


def svg(text, w, h, path: Path, title: str) -> None:
    con = Console(width=w + 2, height=h + 4, force_terminal=True, color_system="truecolor",
                  record=True, file=open(os.devnull, "w", encoding="utf-8"))
    con.print(text, end="")
    path.with_suffix(".txt").write_text(con.export_text(clear=False), encoding="utf-8")
    con.save_svg(str(path), title=title)


def main() -> None:
    out, label = Path(sys.argv[1]), sys.argv[2]
    views = sys.argv[3].split(",") if len(sys.argv) > 3 else ["gantt", "kanban"]
    out.mkdir(parents=True, exist_ok=True)
    b = kg_board.build()
    for w, h in SIZES:
        for mode in views:
            text = render_view(mode, b, False, SELECTED, kg_board.TODAY, w, h, {})
            svg(text, w, h, out / f"{label}-{mode}-{w}x{h}.svg",
                f"taskboard · {mode} · {label} · {w}x{h}")
    print("ok", label, views)


if __name__ == "__main__":
    main()

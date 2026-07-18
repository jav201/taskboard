"""Console entry point: `python -m taskboard` and the installed `taskboard`."""

from __future__ import annotations

import argparse

from .app import TaskboardApp
from .models import default_board_path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="taskboard",
        description="A frameless kanban desktop-widget task board (Textual).",
    )
    parser.add_argument(
        "--board",
        metavar="PATH",
        default=None,
        help=f"JSON store to use (default: {default_board_path()})",
    )
    args = parser.parse_args()
    TaskboardApp(board_path=args.board).run()


if __name__ == "__main__":
    main()

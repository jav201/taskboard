"""Console entry point: `python -m taskboard` and the installed `taskboard`."""

from __future__ import annotations

import argparse
from datetime import datetime

from .app import TaskboardApp
from .boards import Registry, registry_path
from .models import Board, default_board_path


def open_app(board: str | None) -> TaskboardApp:
    """The app as `taskboard` starts it (batch 2026-10-20-batch-01): the user's
    registry; `--board PATH` registered and opened, else the board opened last."""
    registry = Registry.load(registry_path(), default_board_path())
    now = datetime.now()
    entry = registry.register(board) if board else registry.opening()
    registry.touch(entry.id, now)
    return TaskboardApp(board_path=entry.path, registry=registry)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="taskboard",
        description="A frameless kanban desktop-widget task board (Textual).",
    )
    parser.add_argument(
        "--board",
        metavar="PATH",
        default=None,
        help=f"JSON store to use, added to the boards list (default: {default_board_path()})",
    )
    parser.add_argument(
        "--report",
        metavar="PROJECT",
        nargs="?",
        const="",
        default=None,
        help="write an HTML report of the board (or of one PROJECT) and exit",
    )
    args = parser.parse_args()

    if args.report is not None:
        # Report and exit: no TUI. The board is READ, never written.
        from .report import write_report
        board = Board.load(args.board or default_board_path())
        wanted = args.report or None
        if wanted is not None:
            names = [p.name for p in board.visible_projects(False)]
            if wanted not in names:
                listed = ", ".join(names) or "(none)"
                parser.exit(2, f"no project named {wanted!r}. "
                               f"On this board: {listed}\n")
        out = write_report(board, project=wanted)
        print(f"Report written to {out}")
        return

    open_app(args.board).run()


if __name__ == "__main__":
    main()

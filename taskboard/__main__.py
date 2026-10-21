"""Console entry point: `python -m taskboard` and the installed `taskboard`."""

from __future__ import annotations

import argparse
import json
from datetime import datetime

from .app import TaskboardApp
from .boards import Registry, expand_home, registry_path
from .models import Board, default_board_path, strip_controls


def open_app(board: str | None, unlisted: str | None = None) -> TaskboardApp:
    """The app as `taskboard` starts it (batch 2026-10-20-batch-01): the user's
    registry; `--board PATH` registered and opened, else the board opened last;
    `--open PATH` (batch 2026-10-20-batch-03) opened without being registered and
    without being recorded as the board opened last."""
    registry = Registry.load(registry_path(), default_board_path())
    if unlisted:
        return TaskboardApp(board_path=expand_home(unlisted), registry=registry)
    now = datetime.now()
    entry = registry.register(board) if board else registry.opening()
    registry.touch(entry.id, now)
    return TaskboardApp(board_path=entry.path, registry=registry)


def _a_board_file(path: str) -> bool:
    """`--open`'s file: a regular file that parses to a JSON object — anything else
    is refused before the loader could seed or quarantine it (security S-3, S-8)."""
    p = expand_home(path)
    try:
        return p.is_file() and isinstance(json.loads(p.read_text(encoding="utf-8")), dict)
    except (OSError, ValueError, RecursionError):
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="taskboard",
        description="A frameless kanban desktop-widget task board (Textual).",
    )
    where = parser.add_mutually_exclusive_group()
    where.add_argument(
        "--board",
        metavar="PATH",
        default=None,
        help=f"JSON store to use, added to the boards list (default: {default_board_path()})",
    )
    where.add_argument(
        "--open",
        metavar="PATH",
        default=None,
        help="open an existing board file without adding it to the boards list",
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
    if args.open is not None and not _a_board_file(args.open):
        # before --report and before anything is built: the loader would seed a
        # missing path (security S-3)
        parser.exit(2, f"taskboard: no board file at {strip_controls(args.open)} "
                       "(--open opens an existing one)\n")

    if args.report is not None:
        # Report and exit: no TUI. The board is READ, never written.
        from .report import write_report
        source = args.board or args.open            # the two are exclusive
        board = Board.load(expand_home(source) if source else default_board_path())
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

    try:
        app = open_app(args.board, args.open)
    except OSError as exc:      # the registry busy or unwritable: a message, not a traceback
        parser.exit(1, f"taskboard: {exc}\n")
    app.run()


if __name__ == "__main__":
    main()

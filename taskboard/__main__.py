"""Console entry point: `python -m taskboard` and the installed `taskboard`."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

from . import report_html
from .app import TaskboardApp
from .boards import Registry, expand_home, name_for, peek_board, registry_path
from .marks import MARKS_NAME, Directory as MarksDirectory
from .models import default_board_path, strip_controls
from .people import PEOPLE_NAME, Directory as PeopleDirectory

REPORT_KINDS = {"workspace": ("workspace",), "deck": ("deck",), "both": ("workspace", "deck")}
ANSWER_MAX = 4096


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


# line and paragraph separators and the bidirectional overrides and isolates
_DROPPED = dict.fromkeys([0x2028, 0x2029, 0x200E, 0x200F, *range(0x202A, 0x202F),
                          *range(0x2066, 0x206A)])


def _safe(text) -> str:
    """Any file-derived or typed text the report command prints to the terminal
    (batch 2026-10-29-batch-02, LLR-4104.3): no control byte, a tab and a newline
    written as `\\t` and `\\n`, no separator or bidi override — it can neither add a
    line nor drive the terminal. The paths printed on stdout do not pass here."""
    text = strip_controls(str(text)).replace("\t", "\\t").replace("\n", "\\n")
    return text.translate(_DROPPED)


def _read_registry() -> Registry:
    """The registry as `taskboard` would load it, without `Registry.load`'s copy of an
    unreadable file (LLR-4104.2: a report run writes nothing but the reports)."""
    path, main = registry_path(), default_board_path()
    try:
        reg = Registry._read(path, str(main))
    except OSError:
        reg = None
    return reg or Registry.single(main)


def _read_directory(cls, path: Path):
    """The people or marks directory, read without `Directory.load`'s copy-aside."""
    try:
        items = cls._read(path)
    except OSError:
        items = None
    return cls(path, items or [])


def _is_tty(stream) -> bool:
    try:
        return stream is not None and stream.isatty()
    except (OSError, ValueError):
        return False


def _read_answer(stream) -> str:
    """One answer line: at most ANSWER_MAX characters (a longer line is drained and
    read as an invalid answer); a closed stdin, an `OSError` or a decoding error is end
    of input, "" (LLR-4102.5)."""
    try:
        if stream is None:
            return ""
        line = stream.readline(ANSWER_MAX + 1)
        if len(line) > ANSWER_MAX:
            while line and not line.endswith("\n"):
                line = stream.readline(ANSWER_MAX + 1)
            return "?\n"
        return line
    except (OSError, ValueError, UnicodeDecodeError):
        return ""


def _board_lines(entries, default) -> str:
    out = []
    for n, e in enumerate(entries, 1):
        out.append(f"  {n}. {_safe(e.name)}{'  (default)' if e.id == default.id else ''}")
        out.append(f"     {_safe(e.path)}")
    return "\n".join(out)


def ask_board(entries, default, stdin, err):
    """`--report`'s board prompt (HLR-4102): the entry chosen, or None for every
    board. A number picks, a blank line takes the default, `a` takes all, `q` or
    end of input exits 1; an invalid answer, or a board whose file is gone, asks
    again. Stdin that is no terminal and ends before any line exits 2."""
    print(f"Boards:\n{_board_lines(entries, default)}", file=err)
    answered = False
    while True:
        err.write(f"Board [1-{len(entries)}, enter = default, a = all, q = quit]: ")
        err.flush()
        line = _read_answer(stdin)
        if line == "":
            if not answered and not _is_tty(stdin):
                print("taskboard: stdin is not a terminal and gave no answer; "
                      "pass --board PATH to choose a board", file=err)
                raise SystemExit(2)
            print("taskboard: no board chosen", file=err)
            raise SystemExit(1)
        answered = True
        answer = line.strip().lower()
        if answer == "q":
            print("taskboard: no board chosen", file=err)
            raise SystemExit(1)
        if answer == "a":
            return None
        if answer == "":
            pick = default
        elif answer.isascii() and answer.isdecimal() and 1 <= int(answer) <= len(entries):
            pick = entries[int(answer) - 1]
        else:
            print(f"Not a choice: {_safe(answer)[:40]}", file=err)
            continue
        if not _a_board_file(pick.path):
            print(f"{_safe(pick.name)}: the board file is missing or unreadable", file=err)
            continue
        return pick


def run_report(args, parser) -> None:
    """`taskboard --report [PROJECT]` (batch 2026-10-29-batch-02): the `H` export from
    the shell. The boards are READ (never written, never registered); the reports are
    the ones `H` writes, through the same calls, into `<board dir>/reports/`; each
    path is printed on its own line."""
    registry = _read_registry()
    wanted = args.report or None
    skipped = 0
    source = args.board if args.board is not None else args.open
    if source is not None:                  # an existing file, checked by main()
        path = expand_home(source)
        e = registry.entry_for(path)
        chosen = [(e.id, e.name, e.color, str(path)) if e
                  else (None, name_for(path), "pink", str(path))]
        primary = str(path)
    else:
        active = registry.active()
        default = registry.opening()
        if default not in active:
            default = active[0] if active else default
        pick = default
        if len(active) > 1:
            pick = ask_board(active, default, sys.stdin, sys.stderr)
        if pick is None:                    # every board
            if wanted is not None:
                parser.exit(2, "taskboard: --report PROJECT names one project on one board; "
                               "choose a board (not 'a') or pass --board PATH\n")
            found = [e for e in active if _a_board_file(e.path)]
            skipped = len(active) - len(found)
            if not found:
                parser.exit(2, "taskboard: no board file can be read\n")
            chosen = [(e.id, e.name, e.color, e.path) for e in found]
            primary = (default if default.id in {f.id for f in found} else found[0]).path
            print(f"Writing the reports of {len(found)} boards into "
                  f"{_safe(Path(primary).parent / 'reports')}", file=sys.stderr)
        else:
            if not _a_board_file(pick.path):
                parser.exit(2, f"taskboard: no board file at {_safe(pick.path)} "
                               "(--report reads an existing board)\n")
            chosen = [(pick.id, pick.name, pick.color, pick.path)]
            primary = pick.path
    people = _read_directory(PeopleDirectory, registry.path.parent / PEOPLE_NAME).people
    marks = _read_directory(MarksDirectory, registry.path.parent / MARKS_NAME).marks
    boards = []
    for bid, name, colour, bpath in chosen:
        board = peek_board(bpath)
        board.marks = marks
        boards.append((bid, name, colour, board))
    key = None
    if wanted is not None:
        visible = boards[0][3].visible_projects(False)
        proj = next((p for p in visible if p.name == wanted), None)
        if proj is None:
            listed = ", ".join(_safe(p.name) for p in visible) or "(none)"
            parser.exit(2, f"no project named {_safe(repr(wanted))}. On this board: {listed}\n")
        bid = boards[0][0]
        key = f"{bid if bid is not None else '#0'}:{proj.id}"
    today = date.today()
    data = report_html.extract(boards, people, marks, today, project=key)
    try:
        paths = report_html.write_reports(data, REPORT_KINDS[args.report_kind or "both"],
                                          Path(primary).parent / "reports", today)
    except OSError as exc:
        parser.exit(1, f"taskboard: report not written: {_safe(exc)}\n")
    if skipped:
        print(f"{skipped} board{'s' if skipped > 1 else ''} skipped "
              "(file missing or unreadable)", file=sys.stderr)
    for p in paths:
        print(os.path.abspath(p))


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
        help="write the HTML reports of the boards (or of one PROJECT) and exit; "
             "asks which board when you have several",
    )
    parser.add_argument(
        "--report-kind",
        choices=sorted(REPORT_KINDS),
        default=None,
        help="with --report: which report to write (default: both)",
    )
    args = parser.parse_args()
    if args.report_kind is not None and args.report is None:
        parser.error("--report-kind needs --report")
    if args.open is not None and not _a_board_file(args.open):
        # before --report and before anything is built: the loader would seed a
        # missing path (security S-3)
        parser.exit(2, f"taskboard: no board file at {strip_controls(args.open)} "
                       "(--open opens an existing one)\n")
    if args.report is not None and args.board is not None and not _a_board_file(args.board):
        # the same refusal for `--board` (batch 2026-10-29-batch-02, LLR-4104.1)
        parser.exit(2, f"taskboard: no board file at {_safe(args.board)} "
                       "(--report reads an existing board)\n")

    if args.report is not None:
        run_report(args, parser)            # no TUI; the boards are READ, never written
        return

    try:
        app = open_app(args.board, args.open)
    except OSError as exc:      # the registry busy or unwritable: a message, not a traceback
        parser.exit(1, f"taskboard: {exc}\n")
    app.run()


if __name__ == "__main__":
    main()

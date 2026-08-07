"""Refuse a commit that would put private board data into this repository.

WHY A HOOK AND NOT A TEST: the sweep already exists and the suite already runs
it, but a test only speaks when someone runs the suite. The leak of 2026-08-07
reached a PUBLIC remote through a generated file nobody thought to look at, and
sat there for two weeks. This is the moment the data would cross the line.

IT READS THE INDEX, NOT THE WORKING TREE. `git show :path` is what is about to
be committed; the file on disk may be newer, older, or absent. Checking the
working tree would pass a commit whose STAGED version leaks.

IT FAILS CLOSED. No board file, an unreadable one, an unexpected error -- the
commit is refused with the reason. A privacy gate that waves the commit through
when it cannot do its job is worse than none, because it is believed. The
escape is deliberate and named: TASKBOARD_PRIVACY_SWEEP=off. `--no-verify`
bypasses it too, and saying so here is more honest than implying otherwise.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.privacy_sweep import (MIN_PREFIX, SKIP_SUFFIXES, board_strings,  # noqa: E402
                                 prefixes)

OFF = "TASKBOARD_PRIVACY_SWEEP"
BOARD_ENV = "TASKBOARD_BOARD"


def default_board() -> Path:
    return Path(os.environ.get(BOARD_ENV) or (Path.home() / ".taskboard" / "board.json"))


def staged_paths(repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        cwd=repo, capture_output=True, text=True).stdout
    return [p for p in out.split("\n") if p.strip()]


def staged_blob(repo: Path, path: str) -> str | None:
    r = subprocess.run(["git", "show", f":{path}"], cwd=repo, capture_output=True)
    if r.returncode != 0:
        return None
    try:
        return r.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def check(repo: Path, board: Path) -> tuple[int, str]:
    """(exit_code, message). 0 only when the staged content was READ and clean."""
    if os.environ.get(OFF, "").lower() == "off":
        return 0, f"privacy sweep disabled by {OFF}=off"
    if not board.is_file():
        return 1, (f"privacy sweep CANNOT RUN: no board at {board}\n"
                   f"  set {BOARD_ENV}, or {OFF}=off to commit deliberately")
    try:
        needles = [(p, s) for s in board_strings(board) for p in prefixes(s)]
    except Exception as exc:                      # unreadable / not json / ...
        return 1, f"privacy sweep CANNOT RUN: {board} unreadable ({exc})"
    if not needles:
        return 1, (f"privacy sweep CANNOT RUN: {board} yielded no protected "
                   f"strings (every record shorter than {MIN_PREFIX}?)")

    hits: list[tuple[str, str]] = []
    for path in staged_paths(repo):
        if Path(path).suffix.lower() in SKIP_SUFFIXES:
            continue
        text = staged_blob(repo, path)
        if text is None:
            continue
        for needle, whole in needles:
            if needle in text:
                hits.append((path, whole))
                break
    if hits:
        lines = ["COMMIT REFUSED -- staged content carries private board data:"]
        lines += [f"    {p}   contains {s!r}" for p, s in hits]
        lines.append(f"  Fix the file, or {OFF}=off if this is deliberate.")
        return 1, "\n".join(lines)
    return 0, ""


def main() -> int:
    repo = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True).stdout.strip())
    code, msg = check(repo, default_board())
    if msg:
        print(msg, file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())

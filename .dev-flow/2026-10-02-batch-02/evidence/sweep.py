"""Privacy sweep of this batch's record and changed files, entity-decoded (BACKLOG S-8).

    python <this file>                (cwd = repo root)

Two passes over the batch directory plus every changed or added product/test file:
(1) a home-path / username pattern; (2) the real board's strings via
`tools/privacy_sweep.sweep` against `~/.taskboard/board.json` when it exists. Prints
file names and counts only — never a matched string.
"""
import html
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
from tools.privacy_sweep import sweep  # noqa: E402

HOME = re.compile(r"(?i)(?:[a-z]:|/[a-z])[\\/]+users[\\/]+(?!<)[^\\/<\s\"']+|onedrive|my drive")
USER = os.environ.get("USERNAME") or os.environ.get("USER") or ""
BATCH = Path(".dev-flow/2026-10-02-batch-02")

changed = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                         capture_output=True, text=True).stdout.splitlines()
files = {Path(ln[3:].strip().strip('"')) for ln in changed}
files |= {p for p in BATCH.rglob("*") if p.is_file()}
files = sorted(p for p in files if p.is_file() and p.suffix not in {".pyc", ".png", ".gif"}
               and p.resolve() != Path(__file__).resolve())   # its own patterns

hits = 0
for p in files:
    text = html.unescape(p.read_text(encoding="utf-8", errors="replace")).replace(" ", " ")
    n = len(HOME.findall(text)) + (text.count(USER) if USER else 0)
    if n:
        hits += 1
        print(f"HIT home-path/username x{n}: {p.as_posix()}")
print(f"swept {len(files)} files (entity-decoded); {hits} file(s) with a home-path/username hit")

board = Path.home() / ".taskboard" / "board.json"
if board.exists():
    leaks = sweep(board, files)
    for f in leaks:
        print(f"HIT real-board string: {Path(f).as_posix()}")
    print(f"real-board sweep: {len(leaks)} file(s)")
else:
    print("real-board sweep: no ~/.taskboard/board.json on this machine — not run")

"""Increment 001 (batch 2026-10-02-batch-04): record the painted style flags of
the TC-415 sites on the tree it runs over, BEFORE the conversion. It uses the
test's own reader (`tests/test_markup_sites.py::_style_readings`), so the
literals TC-415 pins are the values this prints. Run from the repo root:
    python -B .dev-flow/2026-10-02-batch-04/evidence/inc001_style_base.py
Prints no absolute path."""
from __future__ import annotations

import asyncio
import contextlib
import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
from test_markup_sites import _style_readings  # noqa: E402

import taskboard  # noqa: E402

# round 2 (review F2): the reader must read the tree it runs in, never the
# editable install — run with PYTHONPATH=. ; an export has no .git, so it is
# named by the caller (`TREE_LABEL`) instead of by `git rev-parse`
here = Path(taskboard.__file__).resolve().parent.parent == Path.cwd().resolve()
print(f"taskboard imported from the tree under cwd: {'yes' if here else 'NO'}")
assert here, "taskboard resolved outside the tree under test (set PYTHONPATH=.)"
if Path(".git").exists():
    rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "taskboard"],
                           capture_output=True, text=True).stdout.strip()
    print(f"tree: HEAD {rev}; taskboard/ modified against HEAD: {'yes' if dirty else 'no'}")
else:
    print(f"tree: {os.environ.get('TREE_LABEL', 'an export (no .git)')}")
start = os.getcwd()
sink = io.StringIO()
with tempfile.TemporaryDirectory() as tmp:
    try:
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            got = asyncio.run(_style_readings(Path(tmp), os.chdir))
    finally:
        os.chdir(start)
for k, v in got.items():
    print(f"    {k!r}: {v!r},")

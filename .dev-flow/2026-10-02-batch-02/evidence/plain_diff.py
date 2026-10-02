"""Plain-text equality of every view, base module vs working tree (a colour-only change
must not move a character).

    python <this file> BASE_VIEWS_PY        (cwd = repo root)
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "tests"))
sys.path.insert(0, os.path.dirname(__file__))

import capture  # noqa: E402  (the census fixtures)
import kg_board  # noqa: E402
from taskboard import views as cur  # noqa: E402

spec = importlib.util.spec_from_file_location("taskboard.views_base", sys.argv[1],
                                              submodule_search_locations=None)
base = importlib.util.module_from_spec(spec)
base.__package__ = "taskboard"
spec.loader.exec_module(base)

tmp = Path(tempfile.mkdtemp(prefix="kg-diff-"))
b, st, setup = capture.fixtures(tmp)
diffs = checked = 0
for w, h in ((118, 30), (80, 24), (40, 14)):
    for mode in capture.VIEWS:
        for kw in ({}, {"presentation": "lanes"}, {"presentation": "matrix"},
                   {"lanes_presentation": "grid"}, {"focus_presentation": "review"},
                   {"focus_presentation": "stale"}, {"focus_presentation": "inspector"}):
            extra = {"team_state": st} if mode in ("standup", "people") else {}
            if mode == "setup":
                extra = {"setup_state": setup, "team_state": st}
            a = base.render_view(mode, b, False, "tw3", kg_board.TODAY, w, h, {}, **kw, **extra).plain
            c = cur.render_view(mode, b, False, "tw3", kg_board.TODAY, w, h, {}, **kw, **extra).plain
            checked += 1
            if a != c:
                diffs += 1
                print("DIFF", mode, w, h, kw)
print(f"checked {checked} renders, {diffs} plain-text difference(s)")

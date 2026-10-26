"""The views' frames with no chip, rendered from a given tree (TC-2203's oracle).

    python .dev-flow/2026-10-20-batch-01/evidence/frames_base.py <tree> > frames-base.json

Run on `base_ref` (a worktree at 783397e): every view of `VIEW_ORDER` over the
round's Main board (synthetic, built in a temporary folder), the calendar frozen
on 2026-10-20, at widths 40, 80, 118, 160 and height 40 — each frame's plain text
and its markup-free style signature (the spans' text and style per row 0).
The board comes from `tests/multi_board_fixture.py`: whenever that fixture
changes, re-run this on a worktree at 783397e and commit the new JSON (qa QA-26).
Regenerated 2026-10-26 on fix/gantt-done-visible: the ONLY frames that moved are
the gantt's — done work keeps its row there (the operator's verdict); every
other view is byte-identical to the base_ref render.
"""
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(TREE))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tests"))

import multi_board_fixture as mb  # noqa: E402
from taskboard import app as app_mod, views  # noqa: E402

root = Path(tempfile.mkdtemp())
board = mb.build_board(root, "main")
out = {}
for mode in app_mod.VIEW_ORDER:
    for w in (40, 80, 118, 160):
        text = views.render_view(mode, board, False, None, today=date(2026, 10, 20),
                                 width=w, height=40)
        first = text.split("\n")[0]
        out[f"{mode}@{w}"] = {"plain": text.plain,
                              "row0_spans": [[first.plain[s.start:s.end], str(s.style)]
                                             for s in first.spans]}
print(json.dumps(out, ensure_ascii=False, indent=1))

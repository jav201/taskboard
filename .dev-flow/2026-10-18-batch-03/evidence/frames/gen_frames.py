"""The PRES-V4 gantt-notes oracle frames (batch 2026-10-18-batch-03, HLR-2003 / LLR-2003.1).

    python gen_frames.py <checkout at base_ref 620f58c>

They are the round's own variant-A renderer — `prototypes/backlog_polish/capture.py`'s
`cap_fork("fill")`, approved by the operator on 2026-10-18 — run on `base_ref`, so the port is
held to the round's output and not to code this batch wrote. The board, cursor and sizes are
TC-1807's (the notes board, the cursor on `tw5`, 118x30 and 80x24); the PRES-V3 files of
2026-10-18-batch-01 stay as they are.
"""
import importlib
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "prototypes" / "backlog_polish"))
cap = importlib.import_module("capture")
assert Path(cap.views.__file__).resolve().is_relative_to(root), cap.views.__file__
nb = cap.nb
fill = cap.cap_fork("fill")
here = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    board = nb.build(Path(tmp) / "board.json")
    for w, h in ((118, 30), (80, 24)):
        rows = fill(board, nb.PROJECT_ID, nb.LONG, nb.TODAY, w, h, "gantt").plain.split("\n")
        out = here / f"PRES-V4-gantt-notes-{w}x{h}.txt"
        out.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
        print(out.name, len(rows), "rows")

"""qa Q2-1: the smallest kanban height (rows) at which every band of the kg board is
drawn with no fold row, grouped and lanes, at widths 118 and 80 — measured on the tree
given (base). Pure renderer, synthetic board, kg TODAY."""
import re, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
import kg_board
from rich.text import Text
from taskboard.views import render_kanban
b = kg_board.build()
for pres in ("grouped", "lanes"):
    for w in (118, 80):
        for h in range(20, 200):
            t = render_kanban(b, False, None, kg_board.TODAY, width=w, height=h, presentation=pres)
            plain = t.plain if isinstance(t, Text) else str(t)
            if not re.search(r"^[▲▼] \d+ (above|below)|more ↓|\+\d+ more", plain, re.M):
                print(f"{pres:8} width {w}: every band drawn from height {h}")
                break
        else:
            print(f"{pres:8} width {w}: not reached by 200")

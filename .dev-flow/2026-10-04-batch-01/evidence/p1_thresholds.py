"""C-39 pre-execution of the P1 thresholds, with the prototype's own rule functions
(deps_logic.py, cascade.py in worktree kg-mejoras) over tests/kg_board.py. Synthetic only.

    PYTHONPATH=<main> python .dev-flow/2026-10-04-batch-01/evidence/p1_thresholds.py
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
PROTO = ROOT / ".claude/worktrees/kg-mejoras/prototypes/kg_mejoras"
sys.path[:0] = [str(ROOT), str(ROOT / "tests"), str(PROTO)]
import kg_board, deps_logic as D, cascade as C  # noqa: E402

b = kg_board.build()
w = b.task_by_id("tw5")
cands = [t for t in b.tasks if t is not w and D.is_open(b, t)]
print("open candidates for tw5:", len(cands))
ma = [t.title for t in cands if "ma" in t.title.lower()]
print("filter 'ma':", len(ma), ma)
print("overlap(tm3 on tm2):", C.overlap(b.task_by_id("tm3"), C._dates(b.task_by_id("tm3")), C._dates(b.task_by_id("tm2"))[1]))
print("loop_path(tm2 waits on tm5):", " → ".join(t.title for t in D.loop_path(b, b.task_by_id("tm2"), b.task_by_id("tm5"))))
print("downstream of tm3:", [t.title for t in D.downstream(b, b.task_by_id("tm3"))])
before = {t.id for t in b.tasks if D.waiting(b, t)}
msgs = D.complete(b, "tw2")
print("complete tw2 ->", msgs)
b2 = kg_board.build()
w5, w4 = b2.task_by_id("tw5"), b2.task_by_id("tw4")
w4.due_date = w5.start_date
print("overlap tw5 on tw4 when tw5 starts on tw4's due day:", C.overlap(w5, C._dates(w5), C._dates(w4)[1]))
from datetime import date, timedelta
w4.due_date = (date.fromisoformat(w5.start_date) - timedelta(days=1)).isoformat()
print("... and when tw4 is due the day before:", C.overlap(w5, C._dates(w5), C._dates(w4)[1]))
b3 = kg_board.build()
print("tw5 overlaps on its preds:", [(p.title, C.overlap(b3.task_by_id('tw5'), C._dates(b3.task_by_id('tw5')), C._dates(p)[1])) for p in D.open_preds(b3, b3.task_by_id('tw5'))])

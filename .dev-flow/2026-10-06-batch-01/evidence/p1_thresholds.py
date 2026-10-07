"""P1 iteration 2 — execute the AT thresholds on the exact AT board (C-39).

The prototype engine (cascade.py) run over kg_board.shifted + milestones at the real
today, with the shipped Task.milestone bridged into the extra key the prototype reads
(A-14: the port re-derives against the field; the probe proves the numbers first).

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/p1_thresholds.py
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
PROTO = ROOT / ".claude" / "worktrees" / "kg-mejoras" / "prototypes" / "kg_mejoras"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(PROTO))

import kg_board
import cascade as C

TODAY = date.today()


def board():
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    b = kg_board.milestones(kg_board.shifted(tmp / "board.json"), TODAY)
    for t in b.tasks:                       # bridge the shipped field for the prototype
        if t.milestone:
            t.extra["milestone"] = True
    return b


def show(title, b, tid, sd, dd, mode, override=None):
    p = C.plan_move(b, tid, sd, dd, override or mode, TODAY)
    moved = {k: v for k, v in p.moved.items()}
    shifts = {k: p.shift[k] for k in p.moved}
    print(f"{title} [{tid} s{sd:+d} d{dd:+d} mode={p.mode}]")
    print(f"  moved: {sorted(moved)}  shifts: { {k: shifts[k] for k in sorted(shifts)} }")
    print(f"  new/worse conflicts: {p.new_conflicts or 'none'}")
    over = {k: v for k, v in p.project_over.items()
            if v > p.project_over_before.get(k, 0)}
    print(f"  projects pushed past due: {over or 'none'}")
    for k in sorted(moved):
        s, d = moved[k]
        print(f"    {k}: start {s} due {d}")
    return p


b = board()
print("pre-existing overlaps:", C._conflicts(b, C._dates))
print("AT board today:", TODAY)
print()

show("AT-607 bump +1 push_delta (default)", b, "tm2", 0, 1, "push_delta")
show("AT-608 m->together", b, "tm2", 0, 1, "together")
show("AT-608 m->flag", b, "tm2", 0, 1, "flag")
show("AT-609 editor tm2 due +3 push_delta", b, "tm2", 0, 3, "push_delta")
b2 = board()
b2.project_by_id("pdwh").extra["date_links"] = "together"
show("AT-610 together: td4 +2 (dwh=together)", b2, "td4", 2, 2, "together")
show("AT-610 flag: td4 +2", b, "td4", 2, 2, "flag")
show("AT-611 CONTROL (all open): tm2 +3", board(), "tm2", 3, 3, "push_delta")
b3 = board()
b3.task_by_id("tm3").phase = b3.phases[-1]
p = show("AT-611 done stop (tm3 Done): tm2 +3", b3, "tm2", 3, 3, "push_delta")
assert set(p.moved) == {"tm2"}, "the chain stops at the done task"
show("AT-611 milestone whole: td0 +5", b, "td0", 0, 5, "push_delta")
show("AT-611 earlier: tm2 -1 pulls nothing", b, "tm2", -1, -1, "push_delta")
b4 = board()
b4.task_by_id("td2").depends_on = ["ta4"]
b4.project_by_id("papi").extra["date_links"] = "together"
b4.project_by_id("pdwh").extra["date_links"] = "flag"
show("AT-611 cross-project: ta4 +5 (api=together decides)", b4, "ta4", 5, 5, "together")
print()
print("probe done")

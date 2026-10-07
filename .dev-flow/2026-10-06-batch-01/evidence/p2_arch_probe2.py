"""P2 iteration-2 architect probe 2 — D-633's "the constant cancels in the delta".

Re-runs every p1_thresholds.py arm with cascade.overlap MONKEYPATCHED to the
shipped link_overlap measure (milestone start == due is already bridged by
_dates; the shipped measure just drops the milestone carve-out condition), and
compares moved sets / shifts / conflicts against the prototype-measure output.
Then the boundary case: a milestone waiter whose due is ONE day after its
predecessor's due, predecessor pushed +1 (the -1 -> 0 crossing).

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/p2_arch_probe2.py
"""
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(r"C:\Users\jjgh8\Github\taskboard")
PROTO = ROOT / ".claude" / "worktrees" / "kg-mejoras" / "prototypes" / "kg_mejoras"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(PROTO))

import kg_board
import cascade as C

TODAY = date.today()

proto_overlap = C.overlap


def shipped_overlap(w, wdates, pdue):
    """models.py:1812-1824 on _dates output: readable start -> +1 both-days
    formula, NO milestone carve-out; else the dues formula."""
    ws, wd = wdates
    if pdue is None:
        return 0
    if ws:
        return max(0, (pdue - ws).days + 1)
    return max(0, (pdue - wd).days) if wd else 0


def board():
    b = kg_board.milestones(kg_board.shifted(Path(tempfile.mkdtemp()) / "board.json"), TODAY)
    for t in b.tasks:
        if t.milestone:
            t.extra["milestone"] = True
    return b


def run(b, tid, sd, dd, mode):
    p = C.plan_move(b, tid, sd, dd, mode, TODAY)
    return (dict(p.moved), dict(p.shift), list(p.new_conflicts),
            dict(p.project_over), dict(p.project_over_before))


ARMS = [
    ("AT-607", "tm2", 0, 1, "push_delta", None),
    ("AT-608 together", "tm2", 0, 1, "together", None),
    ("AT-608 flag", "tm2", 0, 1, "flag", None),
    ("AT-609", "tm2", 0, 3, "push_delta", None),
    ("AT-610 together", "td4", 2, 2, "together", ("pdwh", "together")),
    ("AT-610 flag", "td4", 2, 2, "flag", None),
    ("AT-611 done-stop", "tm2", 3, 3, "push_delta", ("tm3", "DONE")),
    ("AT-611 milestone whole", "td0", 0, 5, "push_delta", None),
    ("AT-611 earlier", "tm2", -1, -1, "push_delta", None),
]

print("=== every AT arm, prototype measure vs shipped measure ===")
for name, tid, sd, dd, mode, tweak in ARMS:
    results = {}
    for label, ov in (("proto", proto_overlap), ("shipped", shipped_overlap)):
        C.overlap = ov
        b = board()
        if tweak:
            if tweak[0] == "tm3":
                b.task_by_id("tm3").phase = b.phases[-1]
            else:
                b.project_by_id(tweak[0]).extra["date_links"] = tweak[1]
        results[label] = run(b, tid, sd, dd, mode)
    C.overlap = proto_overlap
    same_moved = results["proto"][0] == results["shipped"][0]
    same_conf = results["proto"][2] == results["shipped"][2]
    print(f"{name}: moved sets identical: {same_moved} · conflicts identical: {same_conf}")
    if not same_moved:
        print(f"  proto:   {sorted(results['proto'][0])}")
        print(f"  shipped: {sorted(results['shipped'][0])}")
    if not same_conf:
        print(f"  proto conflicts:   {results['proto'][2]}")
        print(f"  shipped conflicts: {results['shipped'][2]}")

print()
print("=== boundary: milestone waiter due = pred due + 1d, pred +1 under push_delta ===")
for label, ov in (("proto", proto_overlap), ("shipped", shipped_overlap)):
    C.overlap = ov
    b = board()
    pred = b.task_by_id("tm4")          # tm4's waiter tm5 is the milestone
    ms = b.task_by_id("tm5")
    # put tm5's due exactly ONE day after tm4's due (the x = -1 boundary)
    d4 = date.fromisoformat(pred.due_date)
    ms.due_date = ms.start_date = (d4 + timedelta(days=1)).isoformat()
    p = C.plan_move(b, "tm4", 0, 1, "push_delta", TODAY)
    print(f"{label}: tm4 +1d -> moved {sorted(p.moved)} shifts {p.shift}")
C.overlap = proto_overlap
print()
print("probe done")

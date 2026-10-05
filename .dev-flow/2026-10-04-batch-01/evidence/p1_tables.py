"""P1 iteration 2: the oracle tables of TC-503, TC-509 and TC-513 (qa Q-6, Q-7, Q-8, Q-13),
generated with the prototype's own rule functions (deps_logic.py, cascade.overlap) over
tests/kg_board.py (TODAY 2026-09-30, unshifted). The wording is the contract's (LLR-502.2,
LLR-503.1). Synthetic only.

    PYTHONPATH=<main> python .dev-flow/2026-10-04-batch-01/evidence/p1_tables.py
"""
import sys
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
PROTO = ROOT / ".claude/worktrees/kg-mejoras/prototypes/kg_mejoras"
sys.path[:0] = [str(ROOT), str(ROOT / "tests"), str(PROTO)]
import kg_board, deps_logic as D, cascade as C  # noqa: E402
from taskboard.models import Task, parse_iso  # noqa: E402


def md(d): return f"{d:%b} {d.day}"
def ov(w, p): return C.overlap(w, C._dates(w), C._dates(p)[1])


def timing(w, p):
    s, d, pd = parse_iso(w.start_date), parse_iso(w.due_date), parse_iso(p.due_date)
    if s is None and d is None:
        return "this has no dates — timing can't be checked"
    if pd is None:
        return "no due date — timing can't be checked"
    n = ov(w, p)
    if s is not None:
        return (f"◂ overlaps {n}d: due {md(pd)}, this starts {md(s)}" if n
                else f"ok — due {(s - pd).days}d before this starts")
    return (f"◂ overlaps {n}d: due {md(pd)}, this is due {md(d)}" if n
            else "ok — due on or before the day this is due")


print("## TC-503 overlap truth table (the one measure)")
P = Task("P", due_date="2026-10-10")
P0 = Task("P0")
rows = [("start before the due day", Task("w", start_date="2026-10-08", due_date="2026-10-20"), P),
        ("start ON the due day", Task("w", start_date="2026-10-10", due_date="2026-10-20"), P),
        ("start the day after", Task("w", start_date="2026-10-11", due_date="2026-10-20"), P),
        ("no start, due before pred due", Task("w", due_date="2026-10-07"), P),
        ("no start, due ON pred due", Task("w", due_date="2026-10-10"), P),
        ("no start, due after", Task("w", due_date="2026-10-12"), P),
        ("pred has no due", Task("w", start_date="2026-10-01"), P0),
        ("waiter has no dates", Task("w"), P)]
for name, w, p in rows:
    print(f"| {name} | {w.start_date} | {w.due_date} | {p.due_date} | {ov(w, p)} |")

print("\n## TC-509 picker rows (waiter · order · hint); precondition: tw6 waits on tw5")
for wid in ("tw5", "ta2", "to4"):
    b = kg_board.build()
    b.task_by_id("tw6").depends_on = ["tw5"]
    w = b.task_by_id(wid)
    cands = [t for t in b.tasks if t is not w and D.is_open(b, t)]
    key = lambda t: (t.project_id != w.project_id, parse_iso(t.due_date) is None,
                     parse_iso(t.due_date) or date.max, t.title.lower())
    cands.sort(key=key)
    print(f"### waiter {wid} ({w.title}) — {len(cands)} candidates")
    for t in cands:
        if D.loop_path(b, w, t):
            hint = "⟲ would loop: this → " + " → ".join(x.title for x in D.loop_path(b, w, t)[1:-1]) + " → this"
        elif t.id in w.depends_on:
            hint = "✓ linked (↵ removes) · " + timing(w, t)
        else:
            hint = timing(w, t)
        sec = "same" if t.project_id == w.project_id else "other"
        print(f"| {sec} | {t.id} | {t.title} | {hint} |")

print("\n## TC-513 details sections (kg board, unshifted)")
b = kg_board.build()
for tid in ("tm3", "tw5", "ta2", "to4"):
    t = b.task_by_id(tid)
    preds = D.preds(b, t)
    opn = [p for p in D.open_preds(b, t)]
    direct = [x for x in b.tasks if t.id in x.depends_on and D.is_open(b, x)]
    chain = D.downstream(b, t)
    print(f"### {tid} {t.title}: waits on {len(opn)} open of {len(preds)}; ▸{len(direct)} direct · {len(chain)} in chain")
    for p in preds:
        st = "open" if D.is_open(b, p) else ("archived" if p.archived else "done")
        print(f"   waits on: {p.title} [{st}]")
    for x in direct:
        print(f"   unblocks: {x.title}")
    for x in chain:
        if x not in direct:
            print(f"   └ {x.title}")
    for p in opn:
        n = ov(t, p)
        if n:
            s, pd = parse_iso(t.start_date), parse_iso(p.due_date)
            if s:
                print(f"   conflict: ◂ starts {md(s)}, overlaps {p.title} by {n}d (due {md(pd)})")
            else:
                print(f"   conflict: ◂ due {md(parse_iso(t.due_date))}, overlaps {p.title} by {n}d (due {md(pd)})")

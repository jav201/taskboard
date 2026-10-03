"""LED .17 evidence (P4 qa G-001): the readability of the oracle board under the two
width rules LLR-302.1 weighed at P3 — the floor-first split (every column MIN_COL,
the rest by the want above it) and the frames' proportional split (the shipped
rule, the floor-first one only as its fallback).

    python .dev-flow/2026-10-02-batch-03/evidence/widths_compare.py      (cwd = repo root)
"""
import sys

sys.path[:0] = [".", "tests"]
sys.dont_write_bytecode = True
import kg_board  # noqa: E402
from kg_board import body, readability  # noqa: E402
from taskboard import views  # noqa: E402


def floor_first(room, desired):
    k = len(desired)
    extra = room - k * views.MIN_COL
    if extra <= 0:
        return views.distribute(room, k)
    want = [d - views.MIN_COL for d in desired]
    if not sum(want):
        return [views.MIN_COL + e for e in views.distribute(extra, k)]
    shares = [extra * x // sum(want) for x in want]
    for i in sorted(range(k), key=lambda i: (-desired[i], i))[:extra - sum(shares)]:
        shares[i] += 1
    return [views.MIN_COL + s for s in shares]


shipped = views._kanban_widths
for name, rule in (("floor-first (P3 draft)", floor_first), ("proportional (shipped)", shipped)):
    views._kanban_widths = rule
    for w, h in ((118, 30), (80, 24)):
        b = kg_board.build()
        rows = views.render_view("kanban", b, False, "tw3", kg_board.TODAY, w, h, {}).plain.split("\n")
        avg, full, drawn = readability(body(rows, h), [t.title for t in b.tasks])
        widths = views.kanban_plan(b, False, "tw3", kg_board.TODAY, w, h).widths
        print(f"{name:24} {w}x{h}: widths {widths} · avg/28 {avg:.2f} · full {full} · drawn {drawn}")
views._kanban_widths = shipped

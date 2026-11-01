"""Stage durations from a steps.log (same script for Inc C and Inc L): first line of a
stage tag to the line that ends it; prints minutes per stage and the total wall."""
import re, sys
from datetime import datetime
def load(p):
    out = []
    for ln in open(p, encoding="utf-8"):
        m = re.match(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) (E\d)", ln)
        if m:
            out.append((datetime.strptime(m[1], "%Y-%m-%dT%H:%M:%SZ"), m[2], ln))
    return out
for p in sys.argv[1:]:
    rows = load(p)
    first = {}; last = {}
    for t, st, _ in rows:
        first.setdefault(st, t); last[st] = t
    stages = sorted(first)
    print(p)
    for i, st in enumerate(stages):
        end = first[stages[i + 1]] if i + 1 < len(stages) else last[st]
        print(f"  {st}: {(end - first[st]).total_seconds() / 60:6.1f} min")
    print(f"  wall: {(rows[-1][0] - rows[0][0]).total_seconds() / 60:6.1f} min")

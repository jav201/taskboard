"""matrix.py -- the 6x5 matrix, DERIVED from the sheets rather than typed.

The packet's table is the round's headline claim, and a hand-typed table is a
claim nothing checks.  This reads the same `Sheet` objects `render.py` writes
frames from, so the matrix and the frames cannot disagree.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1])); sys.path.insert(0, str(HERE))
import screens as S

LANGS = ["corgi", "blueprint", "prism", "naught", "ledger"]

def cell(sh):
    v = [c.verdict for c, _ in sh.cands.values()]
    ref = [c for c, _ in sh.cands.values() if c.verdict == "refused"]
    if ref:
        return "rehusa", f"{len(ref)}R/{v.count('evoked')}E", ref
    if v.count("evoked"):
        return "evoca", f"{v.count('evoked')}E", []
    return "implementa", "-", []

print(f"{'':10}" + "".join(f"{s:>16}" for s in S.SCREENS))
allc = {}
for L in LANGS:
    line = f"{L:10}"
    for sc in S.SCREENS:
        sh = S.build(L, sc)
        verd, tag, ref = cell(sh)
        allc[(L, sc)] = (verd, tag, [r.name for r in ref],
                         sorted({c.name for c, _ in sh.cands.values()}))
        line += f"{verd + ' ' + tag:>16}"
    print(line)

print("\n--- per screen: which primitive is missing in how many languages ---")
from collections import Counter
cnt = Counter()
for (L, sc), (v, t, ref, names) in allc.items():
    for n in names:
        cnt[(sc, n)] += 1
for sc in S.SCREENS:
    items = sorted([(n, c) for (s, n), c in cnt.items() if s == sc],
                   key=lambda x: -x[1])
    print(f"{sc}: " + ", ".join(f"{n}x{c}" for n, c in items))

print("\n--- refusals, by language ---")
for L in LANGS:
    rs = []
    for sc in S.SCREENS:
        for n in allc[(L, sc)][2]:
            rs.append(f"{sc}:{n}")
    print(f"{L:10} {rs}")

"""PROBE 3 (C-40): every invariant must be REDDENED by a named mutation.

Mutations are applied by monkeypatch -- nothing on disk is edited.
"""
import tempfile, os
from datetime import date, timedelta
from taskboard import views as V
import _probe_identity as P

ORIG_ALLOC = V.allocate
ORIG_LEAD = V.lead_band


def run(tag, use_feasible_filter=True):
    allr = P.sweep()
    # STATIC exclusion only: the `huge` board at h=10 is the one fixture/size pair
    # where no allocation fits. Excluding on `feasible` would be CIRCULAR -- it
    # deletes exactly the renders a broken cost model produces.
    rows = [r for r in allr if r["A"]
            and (r["feasible"] if use_feasible_filter else not (r["name"] == "huge" and r["h"] == 10))]
    checks = {
        "I1 BODY==CHARGE+2A": lambda r: r["body"] == r["charge"] + 2 * r["A"],
        "I3 BODY<=h-2":       lambda r: r["body"] <= r["h"] - 2,
        "I4 lines==h":        lambda r: r["lines"] == r["h"],
        "I5 no blank rows":   lambda r: r["blank"] == 0,
        "I6 lead==prof+2":    lambda r: r["lead"] == (r["prof"] + 2 if r["A"] else 0),
        "I7 2+BODY+ABS==h":   lambda r: 2 + r["body"] + r["absence"] == r["h"],
    }
    res = {}
    for label, fn in checks.items():
        bad = sum(1 for r in rows if not fn(r))
        res[label] = bad
    shed = sum(1 for r in allr if r["shed"])
    print(f"{tag:34s} " + "  ".join(f"{k.split()[0]}:{'ok' if v == 0 else 'RED%d' % v}"
                                    for k, v in res.items())
          + f"   [in-regime n={len(rows)}, shed={shed}]")
    return res


print("baseline first, then one mutation at a time\n")
base = run("BASELINE (unmutated)")

# M1 -- the call site FORGETS to pay for the lead band's head+tail.
#       simulates views.py:2127 becoming `h - 2`
V.allocate = lambda geo, opens, n_rest, room: ORIG_ALLOC(geo, opens, n_rest, room + 2)
run("M1 room = h-2 (lead unpaid)")
V.allocate = ORIG_ALLOC

# M2 -- the call site pays TWICE for the lead band.
V.allocate = lambda geo, opens, n_rest, room: ORIG_ALLOC(geo, opens, n_rest, room - 2)
run("M2 room = h-6 (lead paid twice)")
V.allocate = ORIG_ALLOC

# M3 -- lead_band grows a row without the charge changing.
V.lead_band = lambda *a, **k: ORIG_LEAD(*a, **k) + [("", None)]
run("M3 lead_band draws prof+3")
V.lead_band = ORIG_LEAD

# M4 -- rung four stops reserving the absence row (`- 1` removed).
def _m4(geo, opens, n_rest, room):
    t, p, w = ORIG_ALLOC(geo, opens, n_rest, room)
    return t, p + 1, w
V.allocate = _m4
run("M4 rung4 keeps no absence row")
V.allocate = ORIG_ALLOC

# M5 -- lead_band SHRINKS a row (charge unchanged) -> under-fill
V.lead_band = lambda *a, **k: ORIG_LEAD(*a, **k)[:-1]
run("M5 lead_band draws prof+1")
V.lead_band = ORIG_LEAD

print("\nsanity: baseline restored ->", run("BASELINE (restored)") == base)

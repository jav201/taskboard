"""E2 trace: every LLR and AT of 01-requirements.md -> the graph nodes and TC ids that carry an example for it.

An LLR counts as traced when a node whose `req:` names it carries an `examples:` (or `offers:`) line
whose TC id is that LLR's test by the numbering rule of 01-requirements.md's header
(LLR-4401.n -> TC-(4400+n), 4402 -> 4430+n, 4403 -> 4460+n, 4404 -> 4500+n, 4405 -> 4540+n,
4406 -> 4560+n, 4407 -> 4580+n with the overflow n >= 30 -> 4640+n (TC-4670..TC-4699),
4408 -> 4610+n with the overflow n >= 20 -> 4630+n (TC-4650..TC-4669, E3 round 1), 4409 -> 4630+n;
a trailing letter is a second test of the same LLR). A withdrawn LLR (`— Withdrawn (<finding>)` in its bold
heading, E3 round 1: ARCH-4, ARCH-7) is listed but not traced.
An AT counts as traced when any node or entity carries an `examples:` line opened by `(AT-44nn`.
Graphs: interfaces + S + T + V. Usage: python e2-trace.py > e2-trace.txt (cwd = this folder).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAPHS = ["graph-interfaces.cw.md", "graph-proto-S.cw.md", "graph-proto-T.cw.md", "graph-proto-V.cw.md"]
BASE = {"4401": 4400, "4402": 4430, "4403": 4460, "4404": 4500, "4405": 4540,
        "4406": 4560, "4407": 4580, "4408": 4610, "4409": 4630}
OVERFLOW = {"4407": (30, 4640), "4408": (20, 4630)}  # LLR-4407.n, n >= 30 -> TC-(4640+n); LLR-4408.n, n >= 20 -> TC-(4630+n)
RULED = {}  # no round-0 ruling assigns an explicit TC id in Inc K
KEYS = ("req:", "in:", "out:", "func:", "module:", "modify:", "examples:", "offers:", "oracle:",
        "desc:", "when:", "anchor:", "seen:", "cause:", "effect:", "decision:")
TC_RE = re.compile(r"\((TC-\d{4}[a-z]?)")
AT_RE = re.compile(r"\((AT-\d{4})")


def expected(llr):
    grp, n = llr[4:].split(".")
    n = int(n)
    if grp in OVERFLOW and n >= OVERFLOW[grp][0]:
        return f"TC-{OVERFLOW[grp][1] + n}"
    return f"TC-{BASE[grp] + n}"


def llrs():
    """(active, withdrawn, ats): an id whose bold heading reads `— Withdrawn` (optionally `(<finding>)`) is not traced."""
    text = (HERE / "01-requirements.md").read_text(encoding="utf-8")
    key = lambda s: (s[4:8], int(s.split(".")[1]))  # noqa: E731
    ids = set(re.findall(r"\*\*(LLR-\d{4}\.\d+)\b", text))
    gone = set(re.findall(r"\*\*(LLR-\d{4}\.\d+) — Withdrawn(?: \([^)*]*\))?\*\*", text))
    ats = sorted(set(re.findall(r"^- \*\*(AT-\d{4})\*\*", text, re.M)))
    return sorted(ids - gone, key=key), sorted(gone, key=key), ats


def blocks():
    """Yield (file, node, reqs, tcs, ats) for every node/entity block of the Nodes/Entities sections."""
    for g in GRAPHS:
        name, reqs, tcs, ats, section = None, set(), [], [], None
        for line in (HERE / g).read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("## "):
                if name:
                    yield g, name, reqs, tcs, ats
                name, reqs, tcs, ats, section = None, set(), [], [], s[3:]
                continue
            if section not in ("Nodes", "Entities") or not s or s[0] in "#>|":
                continue
            if s.startswith(KEYS):
                if s.startswith("req:"):
                    reqs |= set(re.findall(r"LLR-\d{4}\.\d+", s))
                elif s.startswith(("examples:", "offers:")):
                    tcs += TC_RE.findall(s)
                    ats += AT_RE.findall(s)
                continue
            if name:
                yield g, name, reqs, tcs, ats
            name, reqs, tcs, ats = s, set(), [], []
        if name:
            yield g, name, reqs, tcs, ats


def short(g):
    return g.split(".")[0].replace("graph-", "")


def main():
    all_llr, withdrawn, all_at = llrs()
    bl = list(blocks())
    untraced = []
    for llr in all_llr:
        want = {expected(llr)} | RULED.get(llr, set())
        hits = []
        for g, node, reqs, tcs, _ats in bl:
            if llr not in reqs:
                continue
            got = sorted({t for t in tcs if re.sub(r"[a-z]$", "", t) in want or t in want})
            if got:
                hits.append(f"{short(g)}:{node} {','.join(got)}")
        print(f"{llr} (TC {'/'.join(sorted(want))}): " + ("; ".join(hits) if hits else "UNTRACED"))
        if not hits:
            untraced.append(llr)
    at_missing = []
    for at in all_at:
        hits = [f"{short(g)}:{node}" for g, node, _r, _t, ats in bl if at in ats]
        print(f"{at}: " + ("; ".join(hits) if hits else "UNTRACED"))
        if not hits:
            at_missing.append(at)
    print("withdrawn (not traced): " + (", ".join(withdrawn) if withdrawn else "none"))
    print(f"traced {len(all_llr) - len(untraced)}/{len(all_llr)} active LLRs ({len(all_llr) + len(withdrawn)} ids)")
    print(f"traced {len(all_at) - len(at_missing)}/{len(all_at)} ATs")
    print("untraced: " + (", ".join(untraced + at_missing) if untraced or at_missing else "none"))
    return 1 if untraced or at_missing else 0


if __name__ == "__main__":
    sys.exit(main())

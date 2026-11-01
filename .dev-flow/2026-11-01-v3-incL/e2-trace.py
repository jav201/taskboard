"""E2 trace: every LLR of 01-requirements.md -> the graph nodes and TC ids that carry an example for it.

An LLR counts as traced when a node whose `req:` names it carries an `examples:` (or `offers:`) line
whose TC id is that LLR's test by the numbering rule of 01-requirements.md's header
(LLR-4301.n -> TC-(4300+n), 4302 -> 4311+n, 4303 -> 4320+n, 4304 -> 4360+n, 4305 -> 4380+n,
4306 -> 4390+n; a trailing letter is a second test of the same LLR), or the id a round-0 ruling
assigned explicitly (RULED below). Usage: python e2-trace.py > e2-trace.txt (cwd = this folder).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAPHS = ["graph-interfaces.cw.md", "graph-proto-D.cw.md", "graph-proto-V.cw.md", "graph-proto-S.cw.md"]
BASE = {"4301": 4300, "4302": 4311, "4303": 4320, "4304": 4360, "4305": 4380, "4306": 4390}
RULED = {"LLR-4304.16": {"TC-4373b"}}  # 03-pdr-rulings round 0, P-V-2
KEYS = ("req:", "in:", "out:", "func:", "module:", "modify:", "examples:", "offers:", "oracle:",
        "desc:", "when:", "anchor:", "seen:", "cause:", "effect:", "decision:")
TC_RE = re.compile(r"\((TC-\d{4}[a-z]?)")


def expected(llr):
    grp, n = llr[4:].split(".")
    return f"TC-{BASE[grp] + int(n)}"


def llrs():
    text = (HERE / "01-requirements.md").read_text(encoding="utf-8")
    return sorted(set(re.findall(r"\*\*(LLR-\d{4}\.\d+)\b", text)),
                  key=lambda s: (s[4:8], int(s.split(".")[1])))


def blocks():
    """Yield (file, node, reqs, tcs) for every node/entity block of the Nodes/Entities sections."""
    for g in GRAPHS:
        name, reqs, tcs, section = None, set(), [], None
        for line in (HERE / g).read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("## "):
                if name:
                    yield g, name, reqs, tcs
                name, reqs, tcs, section = None, set(), [], s[3:]
                continue
            if section not in ("Nodes", "Entities") or not s or s[0] in "#>|":
                continue
            if s.startswith(KEYS):
                if s.startswith("req:"):
                    reqs |= set(re.findall(r"LLR-\d{4}\.\d+", s))
                elif s.startswith(("examples:", "offers:")):
                    tcs += TC_RE.findall(s)
                continue
            if name:
                yield g, name, reqs, tcs
            name, reqs, tcs = s, set(), []
        if name:
            yield g, name, reqs, tcs


def main():
    all_llr = llrs()
    bl = list(blocks())
    untraced = []
    for llr in all_llr:
        want = {expected(llr)} | RULED.get(llr, set())
        hits = []
        for g, node, reqs, tcs in bl:
            if llr not in reqs:
                continue
            got = sorted({t for t in tcs if re.sub(r"[a-z]$", "", t) in want or t in want})
            if got:
                hits.append(f"{g.split('.')[0].replace('graph-', '')}:{node} {','.join(got)}")
        print(f"{llr} (TC {'/'.join(sorted(want))}): " + ("; ".join(hits) if hits else "UNTRACED"))
        if not hits:
            untraced.append(llr)
    print(f"traced {len(all_llr) - len(untraced)}/{len(all_llr)}")
    print("untraced: " + (", ".join(untraced) if untraced else "none"))
    return 1 if untraced else 0


if __name__ == "__main__":
    sys.exit(main())

"""RED counterfactuals for increment 004 (the P4 walkthrough fixes): one mutation at a
time on taskboard/views.py or taskboard/app.py, run the named nodes, record one
verdict PER RESOLVED NODE, restore the bytes and prove the restore by SHA-256.

Run from the root of a SCRATCH COPY of the increment tree (C-40: never in a tree
another session reads):
    python <this file>
"""
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.getcwd()
T = "tests/test_gantt_board.py"

# (id, label, file, before, after, -k selector)
MUTATIONS = [
    ("H1", "a help line longer than the column", "views.py",
     '                             "▾ abierto · ▸ plegado si no cabe."]),',
     '                             "▾ abierto · ▸ plegado si no cabe en la pantalla actual."]),',
     "help_fits"),
    ("H2", "the narrow scale label keeps its leading zero", "views.py",
     "    return f\"{name} · {f'{k:g}'.lstrip('0')} d/cell\"",
     "    return f\"{name} · {k:g} d/cell\"",
     "half_a_day"),
    ("H3", "the packet may start on the clip marker", "views.py",
     "    lo, hi = max(0, a) + (1 if a < 0 else 0), min(ax.w - 1, b)",
     "    lo, hi = max(0, a), min(ax.w - 1, b)",
     "TC_107"),
    ("H4", "a legend line longer than the legend column", "views.py",
     '"calendar guide: Mondays, or the 1st"',
     '"the calendar guide: mondays, or the 1st at coarse scales"',
     "help_fits"),
    ("H5", "a focus the filter empties loses its header label", "views.py",
     '    elif focus:                    # the focused project is not on this (filtered) board',
     '    elif False:                    # the focused project is not on this (filtered) board',
     "empties_still"),
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main() -> int:
    out = []
    survived = []
    for mid, label, fname, before, after, sel in MUTATIONS:
        path = os.path.join(ROOT, "taskboard", fname)
        src = open(path, encoding="utf-8").read()
        assert src.count(before) == 1, f"{mid}: target not found exactly once"
        pre = sha(path)
        open(path, "w", encoding="utf-8").write(src.replace(before, after))
        assert sha(path) != pre, f"{mid}: mutation did not apply"
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rA",
                                "-p", "no:cacheprovider", T, "-k", sel],
                               cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
        finally:
            open(path, "w", encoding="utf-8").write(src)
        post = sha(path)
        arms = re.findall(r"^(PASSED|FAILED|ERROR) (\S+)", r.stdout, re.M)
        red = [n for v, n in arms if v != "PASSED"]
        green = [n for v, n in arms if v == "PASSED"]
        verdict = "KILLED" if red else "SURVIVED"
        if not red:
            survived.append(mid)
        out.append(f"{mid} {label}: {verdict} · -k '{sel}' · arms {len(arms)} "
                   f"(red {len(red)}, green {len(green)}) · restore sha256 {post[:16]} "
                   f"ok={post == pre}")
        for n in red:
            out.append(f"    RED   {n.split('::')[-1]}")
        for n in green:
            out.append(f"    green {n.split('::')[-1]}")
        tail = [ln for ln in r.stdout.splitlines() if " passed" in ln or " failed" in ln]
        out.append("    " + (tail[-1] if tail else "(no summary)"))
    print("\n".join(out))
    print(f"\n{len(MUTATIONS) - len(survived)} of {len(MUTATIONS)} mutations KILLED"
          + (f"; SURVIVED: {survived}" if survived else ""))
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())

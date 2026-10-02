"""RED counterfactuals for increment 002 (the kanban colour budget): one mutation at a
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
T = "tests/test_colour_budget.py"

# (id, label, file, before, after, -k selector)
MUTATIONS = [
    ("K1", "the card's link token back in accent", "views.py",
     '        tokens.append(("↗", "mut"))       # a link affordance, not focus (round-7 budget)',
     '        tokens.append(("↗", "accent"))',
     "shared_card_tokens or kanban_paints_no_accent"),
    ("K2", "the within-the-week due token back in accent", "views.py",
     '        return f"+{delta}d", ("dim" if resting else "mut")   # near, not focus (budget)',
     '        return f"+{delta}d", ("dim" if resting else "accent")',
     "shared_card_tokens or kanban_paints_no_accent or AT_106"),
    ("K3", "the horizon group This week back in accent", "views.py",
     '                                            ("week", "This week", "hd"),',
     '                                            ("week", "This week", "accent"),',
     "kanban_paints_no_accent"),
    ("K4", "the matrix percent back in accent", "views.py",
     '                          + c(fit(pct, prog_w, "right"), "hd" if pid else "dim")))',
     '                          + c(fit(pct, prog_w, "right"), "accent" if pid else "dim")))',
     "kanban_paints_no_accent or AT_106"),
    ("K5", "the grouped kanban title back in accent", "views.py",
     'lines = [header(c("KANBAN", "bright", bold=True) + mode, right, w, tone="bright")]\n'
     '    lines.append(line(sep.join(_windowed_header',
     'lines = [header(c("KANBAN", "accent", bold=True) + mode, right, w, tone="bright")]\n'
     '    lines.append(line(sep.join(_windowed_header',
     "title_is_bold_bright or kanban_paints_no_accent"),
    ("K6", "a clipped title falls back to the accent", "views.py",
     "        return c(fit(_strip(title), w), tone, bold=True)",
     '        return c(fit(_strip(title), w), "accent", bold=True)',
     "TC_119"),
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

"""RED counterfactuals for increment 001 (gantt G-A + AX-2): one mutation at a
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
    ("G1", "the axis takes the LARGEST fitting scale", "views.py",
     "    k = next((s for s in GANTT_SCALES if need <= w * s), GANTT_SCALES[-1])",
     "    k = next((s for s in reversed(GANTT_SCALES) if need <= w * s), GANTT_SCALES[-1])",
     "TC_101"),
    ("G2", "the window forgets the projects' committed dues", "views.py",
     "    hi = max(dues + pdues + [today]) + margin",
     "    hi = max(dues + [today]) + margin",
     "TC_102"),
    ("G3", "the fold stops at the first group that does not fit", "views.py",
     "        if n and n <= left:\n            unfold[i] = True\n            left -= n",
     "        if n and n <= left:\n            unfold[i] = True\n            left -= n\n        elif n:\n            break",
     "TC_103"),
    ("G4", "the fold unfolds the LEAST late first", "views.py",
     "        return (-late_n(ts), first)",
     "        return (late_n(ts), first)",
     "TC_103 or TC_111"),
    ("G5", "the chip calls a future date late", "views.py",
     "    elif d < today:\n        lab, tone = f\"▲{(today - d).days}d\", \"over\"",
     "    elif d != today:\n        lab, tone = f\"▲{(today - d).days}d\", \"over\"",
     "TC_104 or AT_103"),
    ("G6", "the gutter counts finished dependencies", "views.py",
     "            if (d := board.task_by_id(x)) is not None and not board.is_done(d)]",
     "            if (d := board.task_by_id(x)) is not None]",
     "TC_105"),
    ("G7", "nav walks rest work too", "views.py",
     "        return [[t.id for g in groups for t in g.open]]",
     "        return [[t.id for g in groups for t in g.open + g.rest]]",
     "TC_106 or AT_102"),
    ("G8", "the selection repair jumps to the group's first task", "app.py",
     "                pick = ranked[i + 1] if i + 1 < len(ranked) else ranked[i - 1]",
     "                pick = ranked[0] if ranked[0] is not sel else ranked[1]",
     "AT_108"),
    ("G9", "the focused header is not escaped", "views.py",
     "        title += c(\" (focused: \" + escape(clip(focus_p.name, 40)) + \")\", \"mut\")",
     "        title += c(\" (focused: \" + clip(focus_p.name, 40) + \")\", \"mut\")",
     "TC_108"),
    ("G10", "tick labels may touch", "views.py",
     "        if free(p, p + len(lab), 1):",
     "        if free(p, p + len(lab), 0):",
     "TC_113"),
    ("G11", "the Mondays cadence needs MORE than one cell per day", "views.py",
     "    elif cpd >= 1:",
     "    elif cpd > 1:",
     "TC_112 or AT_104"),
    ("G12", "the month row drops the project marks", "views.py",
     "    for x, (g, key) in marks.items():\n        if 0 <= x < w:\n            glyph[x] = (g, key, True, False)",
     "    for x, (g, key) in {}.items():\n        if 0 <= x < w:\n            glyph[x] = (g, key, True, False)",
     "TC_114 or AT_105"),
    ("G13", "the echo ignores the selection", "views.py",
     "    echo = gantt_echo(sel, board, ax, today) if sel is not None else None",
     "    echo = (gantt_echo(board.task_by_id(\"tw3\") or sel, board, ax, today)\n            if sel is not None else None)",
     "AT_105"),
    ("G14", "the chip is one cell wider than its column", "views.py",
     "            out += \" \" + chip",
     "            out += \"  \" + chip",
     "TC_110"),
    ("G15", "the app keeps a done selection (base behaviour)", "app.py",
     "        if self.view_mode == \"gantt\":\n            # The gantt draws OPEN work",
     "        if False:\n            # The gantt draws OPEN work",
     "AT_108"),
    ("G16", "a folded group draws its tasks", "views.py",
     "            shown, paged = (g.open if g.unfolded else []), False",
     "            shown, paged = g.open, False",
     "TC_103 or TC_110 or AT_101"),
    ("G17", "groups exactly filling the body are not paged", "views.py",
     "    if len(groups) > body_rows or (len(groups) == body_rows and sel_open):",
     "    if len(groups) > body_rows:",
     "TC_106"),
    ("G18", "the gantt legend is asked of a frame with no selection", "views.py",
     "        g_lines, drawn, groups, gax = _gantt_frame(board, show_archived, selected_id,",
     "        g_lines, drawn, groups, gax = _gantt_frame(board, show_archived, None,",
     "TC_116"),
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

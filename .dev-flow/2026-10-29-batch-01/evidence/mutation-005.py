"""Increment 005 mutation battery (batch 2026-10-29-batch-01): the DDR corrections —
DQ1/DU2 the printed table, DQ2/DU1 the printed header, DU5 the downloaded view's scope line,
DU3/O3 the gantt axis labels, DU4 the toast's lines, DQ5 the dates arm; then the DQ1
follow-up (no word or date split in the printed table, M11-M14) and CR5-1 (M15).

Each mutant is a single fault in one SOURCE file (`taskboard/report_workspace.py` or
`taskboard/app.py`) applied as exact string replacements (each `old` must occur exactly
once), run against the named node, then the file is restored byte-identically: its sha256
is printed before the mutation and after the restore. A mutant is KILLED when pytest exits
non-zero AND the named node is among the FAILED.

Run from the worktree root:
  env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-005.py [M01 M02 ...]
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WS = ROOT / "taskboard" / "report_workspace.py"
APP = ROOT / "taskboard" / "app.py"
T = "tests/test_report_workspace.py"
TA = "tests/test_report_export_app.py"
HEAD = ("TC_3112_the_printed_header", "test_TC_3112_the_printed_header_names_only_the_shown_boards")
RULES = ("TC_3112_the_print_rules", "test_TC_3112_the_print_rules_hold")
AXIS = ("TC_3112_the_gantt_axis", "test_TC_3112_the_gantt_axis_labels_never_collide")
TC11 = ("TC_3111_the_view_file", "test_TC_3111_the_view_file_reopens_on_its_view")
TC06 = ("TC_3106_filters_follow", "test_TC_3106_filters_follow_the_truth_table[dates]")
PROJ = ("TC_3112_a_project_file", "test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name")
TC20 = ("TC_3120","test_TC_3120_o_opens_the_report_while_the_toast_lives", TA)

CELL_RULE = "  th,td{white-space:normal;overflow-wrap:normal;padding:.25rem .3rem}\n"
NOWRAP_RULE = ("  th,td[data-col=phase],td[data-col=priority],td[data-col=start],td[data-col=due],"
               "td[data-col=age]{white-space:nowrap}\n")
LONGWORD_RULE = ("  td[data-col=title],td[data-col=board],td[data-col=project],td[data-col=status]"
                 "{overflow-wrap:anywhere}\n")
TABLE_RULES = "  .tbl-wrap{overflow:visible}\n  table{font-size:.7rem}\n" + CELL_RULE + NOWRAP_RULE + LONGWORD_RULE

# (id, file, [(old, new), ...], (-k expression, node that must go RED[, test file]), what it breaks)
MUTANTS = [
    ("M01", WS, [("""  $('#print-scope').textContent = printScope(kept);""",
                  """  $('#print-scope').textContent = scopeLine();""")], HEAD,
     "DQ2/DU1: the print keeps the old scope line (every loaded board, hidden ones too)"),
    ("M02", WS, [("""  $('#print-summary').textContent = summaryText(view, WL, true);""",
                  """  $('#print-summary').textContent = summaryText(view);""")], HEAD,
     "DQ2/DU1: the printed summary keeps the file total \"Projects n/N\""),
    ("M03", WS, [(TABLE_RULES, "")], RULES,
     "DQ1/DU2: the print table rules dropped (the table clipped at the page edge)"),
    ("M04", WS, [("""  .tbl-wrap{overflow:visible}
""", "")], RULES,
     "DQ1/DU2: the print keeps the table's scroll window"),
    ("M05", WS, [(CELL_RULE, "")], RULES,
     "DQ1/DU2: the cells never wrap in print (the table wider than the page)"),
    ("M06", WS, [("""  if(DATA.meta.view) return boardsLine(sc.boards);""", "")], TC11,
     "DU5: the downloaded view says \"All loaded boards\""),
    ("M07", WS, [("""    if(placed.some(([a, b]) => x < b + 4 && x + w + 4 > a)) e.remove();
"""
                  """    else placed.push([x, x + w]);""",
                  """    placed.push([x, x + w]);""")], AXIS,
     "DU3/O3: no label is skipped (the day numbers run over the month label)"),
    ("M08", WS, [("""  for(const major of [true, false]) for(const tk of tks){""",
                  """  for(const major of [false, true]) for(const tk of tks){""")], AXIS,
     "DU3/O3: the day labels placed first, the month labels skipped"),
    ("M09", APP, [(r'''        text += f"\n{folder}\no opens it (10 s)"''',
                   '''        text += f" to {folder} — o opens it (10 s)"''')], TC20,
     "DU4: the toast back on one line (a long path splits the file name)"),
    ("M10", WS, [("""    if(v.from && sp[1] < v.from) return false;""",
                  """    if(v.from && sp[1] <= v.from) return false;""")], TC06,
     "DQ5: a span whose due is `from` dropped (the literal dates set goes RED)"),
    ("M11", WS, [(NOWRAP_RULE, "")], RULES,
     "DQ1 follow-up: headers, dates, priority, phase and age may wrap (\"2026-10-/17\")"),
    ("M12", WS, [(CELL_RULE, CELL_RULE.replace("overflow-wrap:normal", "word-break:break-all"))], RULES,
     "DQ1 follow-up: break-all back on the print cells (\"norma/l\")"),
    ("M13", WS, [(LONGWORD_RULE, "")], RULES,
     "DQ1 follow-up: an over-long word cannot break (the table wider than the page)"),
    ("M14", WS, [("      td.dataset.col = c;\n", "")], RULES,
     "DQ1 follow-up: the cells lose their column tag (the per-column print rules match nothing)"),
    ("M15", WS, [("  if(DATA.meta.scope.kind === 'project' && kept.length) return scopeLine();",
                  "  if(DATA.meta.scope.kind === 'project') return scopeLine();")], PROJ,
     "CR5-1: a project file with its project hidden prints the project and its board"),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(k: str, tfile: str = T) -> tuple[int, list[str], str]:
    env = {k2: v for k2, v in os.environ.items() if k2 != "NO_COLOR"}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TASKBOARD_REQUIRE_BROWSER="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", tfile, "-k", k, "-q",
                           "-p", "no:cacheprovider", "-rf"],
                          cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
    out = proc.stdout + proc.stderr
    failed = re.findall(r"^FAILED \S+::(\S+)", out, flags=re.M)
    tail = [ln for ln in out.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
    return proc.returncode, failed, tail[-1] if tail else out[-300:]


def main() -> int:
    killed = 0
    only = set(sys.argv[1:])
    chosen = [m for m in MUTANTS if not only or m[0] in only]
    for mid, path, edits, (k, node, *tf), what in chosen:
        tfile = tf[0] if tf else T
        original = path.read_bytes()
        before = sha(path)
        text = original.decode("utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"  # CRLF checkout (core.autocrlf)
        lines = []
        for old, new in edits:
            old, new = old.replace("\n", nl), new.replace("\n", nl)
            n = text.count(old)
            if n != 1:
                print(f"{mid} SETUP-ERROR: {old!r} occurs {n} times in {path.name}")
                return 2
            lines.append(text[:text.index(old)].count("\n") + 1 + (old.startswith(nl)))
            text = text.replace(old, new)
        try:
            path.write_bytes(text.encode("utf-8"))
            code, failed, tail = run(k, tfile)
        finally:
            path.write_bytes(original)
        after = sha(path)
        ok = code != 0 and node in failed
        killed += ok
        print(f"{mid} {path.name}:{','.join(map(str, lines))} [{what}]")
        print(f"    run: {tfile} -k \"{k}\" -> exit {code}; {tail}")
        print(f"    RED nodes: {failed}")
        print(f"    verdict: {'KILLED' if ok else 'SURVIVED'} (named node {node})")
        print(f"    sha256 before {before}")
        print(f"    sha256 after  {after} {'(restored, identical)' if after == before else '(MISMATCH)'}")
        if after != before:
            return 3
    print(f"\n{killed}/{len(chosen)} mutants killed")
    return 0 if killed == len(chosen) else 1


if __name__ == "__main__":
    sys.exit(main())

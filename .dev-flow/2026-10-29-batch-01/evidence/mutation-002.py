"""Increment 002 mutation battery (batch 2026-10-29-batch-01): export this view.

Each mutant is a single fault in the one SOURCE file of the increment
(`taskboard/report_workspace.py`), applied as exact string replacements (each `old`
must occur exactly once), run against the named node, then the file is restored
byte-identically: its sha256 is printed before the mutation and after the restore.
A mutant is KILLED when pytest exits non-zero AND the named node is among the FAILED.

Run from the worktree root:
  env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-002.py [M01 M02 ...]
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
T = "tests/test_report_workspace.py"
AT3 = ("AT_3103", "test_AT_3103_download_this_view_holds_only_the_filtered_tasks")
TC9 = ("TC_3109", "test_TC_3109_the_download_keeps_only_used_entries")
TC10 = ("TC_3110", "test_TC_3110_notes_off_strips_the_notes")
TC11 = ("TC_3111_the_view_file", "test_TC_3111_the_view_file_reopens_on_its_view")
TC11C = ("TC_3111_the_export_captions", "test_TC_3111_the_export_captions_show_without_hover")
AT4 = ("AT_3104", "test_AT_3104_print_hides_the_controls_and_shows_the_filter_header")
TC12 = ("TC_3112", "test_TC_3112_the_print_rules_hold")
TC22 = ("TC_3122", "test_TC_3122_csv_and_json_hold_the_visible_rows_only")

GUARD = r"/^[=+\-@\t\r]/"
DOM_BUILD = ("  const doc = new DOMParser().parseFromString(PRISTINE, 'text/html');\n"
             "  doc.getElementById('board-data').textContent = scriptSafe(JSON.stringify(d2));\n"
             "  download('workspace-view-' + d2.meta.view.exported + '.html',\n"
             r"           '<!doctype html>\n' + doc.documentElement.outerHTML, 'text/html');")
STRING_REPLACE = ("  const html = PRISTINE.replace(document.getElementById('board-data').textContent,"
                  " scriptSafe(JSON.stringify(d2)));\n"
                  "  download('workspace-view-' + d2.meta.view.exported + '.html',"
                  r" '<!doctype html>\n' + html, 'text/html');")

# (id, [(old, new), ...], (-k expression, node that must go RED), what it breaks)
MUTANTS = [
    ("M01", [("scriptSafe(JSON.stringify(d2))",
              "scriptSafe(JSON.stringify(Object.assign({}, DATA, {meta: d2.meta})))")],
     AT3, "the download re-embeds the full data (no reduction)"),
    ("M02", [("deps: t.deps.filter(k => keys.has(k)), chain: t.chain.filter(k => keys.has(k)),",
              "deps: t.deps, chain: t.chain,")],
     AT3, "deps/chain keys of dropped tasks kept"),
    ("M03", [("boards: boards.map(b => b.name)},", "boards: sc.boards},")],
     AT3, "R3: meta.scope.boards (header N/names) not reduced"),
    ("M04", [("people: DATA.people.filter(p => wl.u.has(p.id)),", "people: DATA.people,")],
     TC9, "LLR-3103.1 negative control: the full people list kept"),
    ("M05", [(DOM_BUILD, STRING_REPLACE)],
     TC9, "D3: the file composed by String.replace (pattern semantics: $' re-inserts the shell)"),
    ("M06", [("textContent = scriptSafe(JSON.stringify(d2));", "textContent = JSON.stringify(d2);")],
     TC9, "LLR-3106.1: the JSON enters the file with raw < > &"),
    ("M07", [("notes_html: notes ? t.notes_html : '', notes_text: notes ? t.notes_text : '',",
              "notes_html: t.notes_html, notes_text: t.notes_text,")],
     TC10, "notes kept when the notes section is off"),
    ("M08", [("notes_text: notes ? t.notes_text : '',", "notes_text: t.notes_text,")],
     TC10, "PA2/C2: notes_html stripped but notes_text kept"),
    ("M09", [("const PRISTINE = document.documentElement.outerHTML;", "let PRISTINE = '';"),
             ("\nstart();\n", "\nstart();\nPRISTINE = document.documentElement.outerHTML;\n")],
     TC11, "the shell captured after rendering (controls rebuilt twice, rendered rows travel)"),
    ("M10", [("return parseHash(location.hash || (DATA.meta.view ? DATA.meta.view.state : ''));",
              "return parseHash(location.hash);")],
     TC11, "D5: the downloaded file ignores meta.view (opens on the default view)"),
    ("M11", [('<span class="cap"> — a PDF of what is shown',
              '<span class="cap" hidden> — a PDF of what is shown')],
     TC11C, "C6: the print caption not visible without interaction"),
    ("M12", [("  .controls,nav,.xgroup,#tt,#card,.dl,.zbtn{display:none!important}",
              "  .xgroup,#tt,#card,.dl,.zbtn{display:none!important}")],
     AT4, "the control bar (.controls / nav, the same element) dropped from the print rule"),
    ("M13", [("  window.addEventListener('beforeprint', setPrinted);\n", "")],
     AT4, "the beforeprint handler does not stamp the printed date"),
    ("M14", [("  #gantt{min-width:0!important}\n", "")],
     TC12, "C14: #gantt{min-width:0!important} dropped (gantt wider than 794 px)"),
    ("M15", [("  @page{margin:0}\n", "")],
     TC12, "C7: @page{margin:0} dropped"),
    ("M16", [("viewBox: `0 0 ${W} ${H}`, ", "")],
     TC12, "the svg viewBox dropped: the print clips the timeline instead of scaling it"),
    ("M17", [("  .scr{display:none!important}\n", "")],
     TC12, "C7: the print shows 'of N' (a count over hidden tasks)"),
    ("M18", [("const rows = exportRows(applyFilters(view, DATA.tasks));",
              "const rows = exportRows(DATA.tasks);")],
     TC22, "the CSV exports the full data"),
    ("M19", [("""  if(/^[=+\\-@\\t\\r]/.test(v) && !/^-?\\d+(\\.\\d+)?$/.test(v)) v = "'" + v;\n""", "")],
     TC22, "the ' formula guard dropped"),
    ("M20", [(GUARD, r"/^[+\-@\t\r]/")], TC22, "prefix class '=' unguarded"),
    ("M21", [(GUARD, r"/^[=\-@\t\r]/")], TC22, "prefix class '+' unguarded"),
    ("M22", [(GUARD, r"/^[=+@\t\r]/")], TC22, "prefix class '-' unguarded"),
    ("M23", [(GUARD, r"/^[=+\-\t\r]/")], TC22, "prefix class '@' unguarded"),
    ("M24", [(GUARD, r"/^[=+\-@\r]/")], TC22, "prefix class TAB unguarded"),
    ("M25", [(GUARD, r"/^[=+\-@\t]/")], TC22, "prefix class CR unguarded"),
    ("M26", [(r" && !/^-?\d+(\.\d+)?$/.test(v)", "")], TC22, "C13: plain numbers prefixed too"),
    ("M27", [("depends_on: t.deps.filter(k => keys.has(k)).map(k => TASKS.get(k).title)",
              "depends_on: t.deps.map(k => TASKS.get(k).title)")],
     TC22, "the CSV/JSON name a dropped dependency's title"),
    ("M28", [("notes: notes ? t.notes_text : '',", "notes: t.notes_text,")],
     TC22, "the CSV/JSON carry notes while the notes section is off"),
    ("M29", [("$('#view-origin').hidden = !mv;", "$('#view-origin').hidden = true;")],
     AT3, "the downloaded file's header does not say it is a filtered view"),
    ("M30", [(".map(p => keptCounts(p, tasks)),", ",")],
     TC9, "projects[] facts carried unchanged: they count dropped tasks"),
    ("M31", [("return Object.assign({}, p, {open: open.length,", "return Object.assign({}, p, {open: p.open,")],
     TC9, "CR2-1: open carried from the source project"),
    ("M32", [("late: mine.filter(t => t.status === 'late').length,", "late: p.late,")],
     TC9, "CR2-1: late carried from the source project"),
    ("M33", [("late: mine.filter(t => t.status === 'late').length,", "late: open.length,")],
     TC9, "CR2-1: late counted as open"),
    ("M34", [("done: mine.filter(t => t.status === 'done').length,", "done: p.done,")],
     TC9, "CR2-1: done carried from the source project"),
    ("M35", [("high: open.filter(t => t.priority === 'high').length,", "high: p.high,")],
     TC9, "CR2-1: high carried from the source project"),
    ("M36", [("worst: null, momentum: null});", "worst: p.worst, momentum: p.momentum});")],
     TC9, "CR2-1: worst and momentum (server-derived) kept in the download"),
    ("M37", [("  return t.mentions.filter(h => view.u.has(h));", "  return t.mentions;")],
     TC10, "SD1: mentions travel while the notes section is off"),
    ("M38", [("window.addEventListener('hashchange', () => { view = viewFromLocation(); render(); });",
              "window.addEventListener('hashchange', () => { view = parseHash(location.hash); render(); });")],
     TC11, "CR2-2: clearing the hash of a downloaded view falls to the default view"),
    ("M39", [("  window.addEventListener('afterprint', unsetPrinted);", "")],
     TC12, "CR2-3: the printed line stays after printing"),
    ("M40", [("function printView(){ window.print(); }", "function printView(){ setPrinted(); window.print(); }")],
     TC12, "CR2-3: the print control stamps the date itself (a second stamp path)"),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(k: str) -> tuple[int, list[str], str]:
    env = {k2: v for k2, v in os.environ.items() if k2 != "NO_COLOR"}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TASKBOARD_REQUIRE_BROWSER="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", T, "-k", k, "-q",
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
    for mid, edits, (k, node), what in chosen:
        original = WS.read_bytes()
        before = sha(WS)
        text = original.decode("utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"  # CRLF checkout (core.autocrlf)
        lines = []
        for old, new in edits:
            old, new = old.replace("\n", nl), new.replace("\n", nl)
            n = text.count(old)
            if n != 1:
                print(f"{mid} SETUP-ERROR: {old!r} occurs {n} times in {WS.name}")
                return 2
            lines.append(text[:text.index(old)].count("\n") + 1 + (old.startswith(nl)))
            text = text.replace(old, new)
        try:
            WS.write_bytes(text.encode("utf-8"))
            code, failed, tail = run(k)
        finally:
            WS.write_bytes(original)
        after = sha(WS)
        ok = code != 0 and node in failed
        killed += ok
        print(f"{mid} {WS.name}:{','.join(map(str, lines))} [{what}]")
        print(f"    run: {T} -k \"{k}\" -> exit {code}; {tail}")
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

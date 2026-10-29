"""Increment 001 mutation battery (batch 2026-10-29-batch-01).

Each mutant is a single fault in one SOURCE file (`taskboard/report_html.py` or
`taskboard/report_workspace.py`), applied as exact string replacements (each `old`
must occur exactly once), run against the named node(s), then the file is restored
byte-identically: its sha256 is printed before the mutation and after the restore.
A mutant is KILLED when pytest exits non-zero AND the named node is among the FAILED.

Run from the worktree root:
  env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-001.py [M01 M02 ...]
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HTML = ROOT / "taskboard" / "report_html.py"
WS = ROOT / "taskboard" / "report_workspace.py"
UNIT = "tests/test_report_html.py"
BROWSER = "tests/test_report_workspace.py"

# (id, file, [(old, new), ...], test file, -k expression, node that must go RED, what it breaks)
MUTANTS = [
    ("M01", HTML, [('rows.append((f"{bkey}:{p.id}", p,', 'rows.append((p.id, p,')],
     UNIT, "TC_3101_extract_is_json", "test_TC_3101_extract_is_json_and_holds_every_fact",
     "projects keyed by the bare id: the two `Docs` (id pdocs) collide"),
    ("M02", HTML, [("        in_scope = {t.id for _, _, ts in rows for t in ts}",
                    "        board.save()\n        in_scope = {t.id for _, _, ts in rows for t in ts}")],
     UNIT, "never_writes", "test_TC_3101_extract_never_writes_a_board",
     "extract saves the board"),
    ("M03", HTML, [('"due_word": _due_word(due_in),', '"due_word": f"{due_in}d",')],
     UNIT, "TC_3102", "test_TC_3102_due_words_are_the_cli_reports",
     "the due word formatted locally"),
    ("M04", HTML, [("rows = [r for r in rows if project is None or r[0] == project]",
                    "rows = [r for r in rows]")],
     UNIT, "TC_3103", "test_TC_3103_project_scope_keeps_one_project",
     "the scope ignores `project`"),
    ("M05", HTML, [('        out.append(path)\n    return out\n',
                    '        out.append(path)\n    return out\n\n\nfrom . import report_workspace  # noqa: E402,F401\n')],
     UNIT, "TC_3104", "test_TC_3104_renderers_read_the_dict_only",
     "PA3: a module-level renderer import in report_html"),
    ("M06", WS, [("from .report_html import embed_json",
                  "from .report_html import embed_json\nfrom .views import HEX  # noqa: F401")],
     UNIT, "TC_3104", "test_TC_3104_renderers_read_the_dict_only",
     "the renderer imports views.HEX"),
    ("M07", WS, [("from .report_html import embed_json",
                  "import importlib\n\nfrom .report_html import embed_json\n\n_R = importlib.import_module('taskboard.report_html')")],
     UNIT, "TC_3104", "test_TC_3104_renderers_read_the_dict_only",
     "PQ10: a dynamic import in the renderer"),
    ("M08", HTML, [('return raw.replace("<", "\\\\u003c").replace(">", "\\\\u003e").replace("&", "\\\\u0026")',
                    'return raw.replace("</", "<\\\\/")')],
     UNIT, "TC_3115", "test_TC_3115_embed_json_and_notes_are_inert",
     "the prototype's `</`-only replace in embed_json"),
    ("M09", HTML, [("""parts.append(f'<span class="hl-{tone}">{esc(piece)}</span>')""",
                    """parts.append(f'<span class="hl-{tone}">{piece}</span>')""")],
     UNIT, "TC_3115", "test_TC_3115_embed_json_and_notes_are_inert",
     "a notes piece left unescaped"),
    ("M10", HTML, [('ch.lower() if ch.isalnum() else "-" for ch in name', 'ch.lower() for ch in name')],
     UNIT, "TC_3123_the_slug", "test_TC_3123_the_slug_is_the_cli_reports",
     "the slug lower-cases only"),
    ("M11", HTML, [('return f"{kind}-{board_slug}-{project_slug}-{today.isoformat()}.html"',
                    'return f"{kind}-{project_slug}-{today.isoformat()}.html"')],
     UNIT, "TC_3123", "test_TC_3123_write_reports_lands_in_the_folder_and_overwrites",
     "the project file name drops the board slug"),
    ("M12", HTML, [('"urls": [u for u in map(valid_url, t.urls) if u],', '"urls": list(t.urls),')],
     UNIT, "TC_3124", "test_TC_3124_extract_keeps_only_http_urls",
     "the valid_url filter dropped"),
    ("M13", HTML, [("if due is not None and due < today:", "if due is not None and due <= today:")],
     UNIT, "TC_3125_one_status", "test_TC_3125_one_status_rule",
     "late derived with <= (the due-today task turns late)"),
    ("M14", WS, [("const b = make('button', null, label);", "const b = make('span', null, label);")],
     BROWSER, "TC_3105", "test_TC_3105_the_bar_is_native_and_counted",
     "a chip built as a <span onclick>"),
    ("M15", WS, [("button[aria-pressed=\"true\"]::before{content:\"\\\\2713\\\\00a0\"}\n", "")],
     BROWSER, "TC_3105", "test_TC_3105_the_bar_is_native_and_counted",
     "C12: the pressed chip loses its check mark"),
    ("M16", WS, [("if(!v.s.has(t.status)) return false;",
                  "if(!v.s.has(t.status === 'late' ? 'open' : t.status)) return false;")],
     BROWSER, "TC_3106 and status", "test_TC_3106_filters_follow_the_truth_table[status]",
     "the status chips map late to open"),
    ("M17", WS, [("t.mentions.some(h => v.u.has(h))", "[...v.u].every(h => t.mentions.includes(h))")],
     BROWSER, "TC_3106 and people", "test_TC_3106_filters_follow_the_truth_table[people]",
     "people: ANY becomes ALL"),
    ("M18", WS, [("  if(!v.p.has(t.project)) return false;\n", "")],
     BROWSER, "TC_3106 and projects", "test_TC_3106_filters_follow_the_truth_table[projects]",
     "the project filter ignored"),
    ("M19", WS, [("  if(v.m.size && !(t.mark && v.m.has(t.mark))) return false;\n", "")],
     BROWSER, "TC_3106 and classes", "test_TC_3106_filters_follow_the_truth_table[classes]",
     "the class filter ignored"),
    ("M20", WS, [("if(v.to && sp[0] > v.to) return false;", "if(v.to && sp[0] >= v.to) return false;")],
     BROWSER, "TC_3106 and dates", "test_TC_3106_filters_follow_the_truth_table[dates]",
     "a span starting ON `to` is dropped"),
    ("M21", WS, [("projectName(t.project)).toLowerCase();", "projectName(t.project));"),
                 ("hay.includes(v.q.toLowerCase())", "hay.includes(v.q)")],
     BROWSER, "TC_3106 and search", "test_TC_3106_filters_follow_the_truth_table[search]",
     "search without case folding"),
    ("M22", WS, [("    if(v.from && v.to && v.from > v.to) return false;\n", "")],
     BROWSER, "TC_3106_the_edges", "test_TC_3106_the_edges_of_the_table",
     "`from` after `to` no longer empties the view"),
    ("M23", WS, [("$('#view-summary').textContent = summaryText(view);",
                  "$('#view-summary').innerHTML = decodeURIComponent(location.hash);")],
     BROWSER, "TC_3107", "test_TC_3107_a_hostile_hash_is_dropped",
     "PQ2(a): the hash echoed into the summary via innerHTML"),
    ("M24", WS, [("filter(x => x !== null && WL[k].has(x))", "filter(x => x !== null)")],
     BROWSER, "TC_3107", "test_TC_3107_a_hostile_hash_is_dropped",
     "PQ2(b): the whitelist bypassed; unknown values reach the controls and the summary"),
    ("M25", WS, [("$('#reset').addEventListener('click', () => { view = defaultView(); render(); });",
                  "$('#reset').addEventListener('click', () => { view = defaultView(); syncControls(); });")],
     BROWSER, "TC_3108", "test_TC_3108_reset_restores_the_defaults",
     "Reset leaves the rows and the hash"),
    ("M26", WS, [("  renderMilestones(kept);\n  writeHash();\n}", "  renderMilestones(kept);\n}")],
     BROWSER, "AT_3102", "test_AT_3102_filters_and_the_hash_round_trip",
     "writeHash skipped"),
    ("M27", WS, [("if(!v.s.has(t.status)) return false;",
                  "if(!v.s.has(t.status === 'late' ? 'open' : t.status)) return false;")],
     BROWSER, "AT_3102", "test_AT_3102_filters_and_the_hash_round_trip",
     "the status chips map late to open (AT's late arm)"),
    ("M28", WS, [('<meta name="viewport" content="width=device-width, initial-scale=1">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                  '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">')],
     BROWSER, "TC_3116", "test_TC_3116_offline_themes_and_phone_width",
     "PQ5: a Google Fonts <link> (one external request)"),
    ("M29", WS, [("main{max-width:76rem;margin:0 auto}", "main{max-width:76rem;margin:0 auto;min-width:600px}")],
     BROWSER, "TC_3116", "test_TC_3116_offline_themes_and_phone_width",
     "a fixed 600 px layout overflows 390 px"),
    ("M30", WS, [("@media (prefers-color-scheme:light){", "@media (prefers-color-scheme:none){")],
     BROWSER, "TC_3116", "test_TC_3116_offline_themes_and_phone_width",
     "the light palette never applies"),
    ("M31", WS, [("if(!v.s.has(t.status)) return false;",
                  "if(!v.s.has(t.archived ? 'archived' : t.done ? 'done' : "
                  "(t.due && t.due < DATA.meta.today) ? 'late' : 'open')) return false;")],
     BROWSER, "TC_3125", "test_TC_3125_the_page_follows_the_status_field",
     "PQ8: the page re-derives status from the dates"),
    ("M32", WS, [('.replace("{data}", embed_json(d)))',
                  '.replace("{data}", embed_json(d)).replace("</h1>", "</h1>" + d["boards"][0]["name"], 1))')],
     BROWSER, "shell_holds_no_board_text", "test_the_page_shell_holds_no_board_text",
     "D2: a board name written into the shell"),
    ("M33", WS, [("\nstart();\n", "\nstart(;\n")],
     UNIT, "PQ6", "test_PQ6_spike_an_async_test_checks_the_page_in_a_worker_thread",
     "the page script does not run (a syntax error)"),
    ("M34", HTML, [('"done": sum(1 for t in ts if not t.archived and board.is_done(t)),',
                    '"done": lane.done_n,')],
     UNIT, "TC_3101_extract_is_json", "test_TC_3101_extract_is_json_and_holds_every_fact",
     "CR2: project done counts archived tasks (lane.done_n)"),
    ("M35", HTML, [("""    bad = [k for k in kinds if k not in ("workspace", "deck")]
    if bad:""", """    Path(folder).mkdir(parents=True, exist_ok=True)
    bad = [k for k in kinds if k not in ("workspace", "deck")]
    if bad:""")],
     UNIT, "write_reports_lands", "test_TC_3123_write_reports_lands_in_the_folder_and_overwrites",
     "CR3: the folder is created before the kinds are checked"),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(test_file: str, k: str) -> tuple[int, list[str], str]:
    env = {k2: v for k2, v in os.environ.items() if k2 != "NO_COLOR"}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TASKBOARD_REQUIRE_BROWSER="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", test_file, "-k", k, "-q",
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
    for mid, path, edits, test_file, k, node, what in chosen:
        original = path.read_bytes()
        before = sha(path)
        text = original.decode("utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"  # CRLF checkout (core.autocrlf)
        for old, new in edits:
            old, new = old.replace("\n", nl), new.replace("\n", nl)
            n = text.count(old)
            if n != 1:
                print(f"{mid} SETUP-ERROR: {old!r} occurs {n} times in {path.name}")
                return 2
            line = text[:text.index(old)].count("\n") + 1
            text = text.replace(old, new)
        try:
            path.write_bytes(text.encode("utf-8"))
            code, failed, tail = run(test_file, k)
        finally:
            path.write_bytes(original)
        after = sha(path)
        ok = code != 0 and node in failed
        killed += ok
        print(f"{mid} {path.name}:{line} [{what}]")
        print(f"    run: {test_file} -k \"{k}\" -> exit {code}; {tail}")
        print(f"    RED nodes: {failed}")
        print(f"    verdict: {'KILLED' if ok else 'SURVIVED'} (named node {node})")
        print(f"    sha256 before {before}")
        print(f"    sha256 after  {after} {'(restored, identical)' if after == before else '(MISMATCH)'}")
        if after != before:
            return 3
    print(f"\n{killed}/{len(MUTANTS)} mutants killed")
    return 0 if killed == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())

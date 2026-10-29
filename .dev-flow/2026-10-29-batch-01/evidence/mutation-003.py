"""Increment 003 mutation battery (batch 2026-10-29-batch-01): the deck, and board text
shown never run in both reports.

Each mutant is a single fault in one file — the increment's SOURCE `taskboard/report_deck.py`,
or, for the conditions carried into this increment (PDR PQ9, security SI1, D1's defence in
depth), `taskboard/report_workspace.py` or `taskboard/report_html.py` — applied as exact
string replacements (each `old` must occur exactly once), run against the named node of
`tests/test_report_deck.py` (M30: `tests/test_report_html.py`), then the file is restored byte-identically: its sha256 is
printed before the mutation and after the restore. A mutant is KILLED when pytest exits
non-zero AND the named node is among the FAILED.

Run from the worktree root:
  env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-003.py [M01 M02 ...]
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DECK = ROOT / "taskboard" / "report_deck.py"
WS = ROOT / "taskboard" / "report_workspace.py"
HTML = ROOT / "taskboard" / "report_html.py"
T = "tests/test_report_deck.py"
AT6 = ("AT_3106", "test_AT_3106_board_text_is_escaped_in_both_reports")
TC13 = ("TC_3113", "test_TC_3113_one_slide_per_project")
TC14 = ("TC_3114", "test_TC_3114_keys_page_and_print_splits")
TC16 = ("TC_3116", "test_TC_3116_offline_themes_and_phone_width")
TC04 = ("TC_3104", "test_TC_3104_the_deck_reads_the_dict_only")
TC02 = ("TC_3102", "test_TC_3102_due_words_are_the_cli_reports", "tests/test_report_html.py")
NEVER = ("never_late", "test_finished_work_is_never_late_in_either_report")

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">'

# (id, file, [(old, new), ...], (-k expression, node that must go RED), what it breaks)
MUTANTS = [
    ("M01", DECK, [("""font-size="{L["fs"]}">{esc(title)}</text>')""",
                    """font-size="{L["fs"]}">{title}</text>')""")],
     AT6, "HLR-3106 negative control: esc removed from the gantt's task title"),
    ("M02", DECK, [("""<p class="nt">{esc(t["title"])}</p>""", """<p class="nt">{t["title"]}</p>""")],
     AT6, "esc removed from the note card's task title"),
    ("M03", DECK, [("""<span class="pname">{esc(p["name"])}</span>""",
                    """<span class="pname">{p["name"]}</span>""")],
     AT6, "esc removed from the slide's project name"),
    ("M04", DECK, [("""rows.append(f"<tr><td>{esc(b['name'])}</td>{cells}</tr>")""",
                    """rows.append(f"<tr><td>{b['name']}</td>{cells}</tr>")""")],
     AT6, "esc removed from the cover's board name"),
    ("M05", DECK, [("""<p class="scope">{esc(_scope_line(d, boards))}</p>""",
                    """<p class="scope">{_scope_line(d, boards)}</p>""")],
     AT6, "esc removed from the cover's scope line"),
    ("M06", DECK, [("""f"{esc(_trunc(proj['name'], L['ochars']))}</text>")""",
                    """f"{_trunc(proj['name'], L['ochars'])}</text>")""")],
     AT6, "esc removed from the overview's project name"),
    ("M07", WS, [("td.appendChild(make('span', markOf(t) ? 'tmark' : null, cellText(t, c)));",
                  "{ const sp = make('span', markOf(t) ? 'tmark' : null); sp.innerHTML = cellText(t, c);"
                  " td.appendChild(sp); }")],
     AT6, "PDR PQ9: the workspace sets the task title via innerHTML"),
    ("M08", HTML, [('"urls": [u for u in map(valid_url, t.urls) if u],', '"urls": list(t.urls),')],
     AT6, "D1: the extraction's valid_url filter dropped (javascript:/data: reach the files)"),
    ("M09", DECK, [('return u if re.match(r"https?://", u or "", re.I) else None', "return u")],
     TC16, "SI1/D1: the deck's http(s) re-check made the identity"),
    ("M10", WS, [(r"function safeHref(u){ return /^https?:\/\//i.test(u || '') ? u : null; }",
                  "function safeHref(u){ return u; }")],
     TC16, "SI1: the workspace's safeHref made the identity"),
    ("M11", DECK, [("""f'rel="noopener noreferrer">{esc(label)}</a></p>')""",
                    """f'>{esc(label)}</a></p>')""")],
     TC16, "LLR-3106.2: the deck's task links lose rel=noopener noreferrer"),
    ("M12", DECK, [(r"""initial-scale=1">\n'""", r"""initial-scale=1">\n""" + FONTS + "'")],
     TC16, "LLR-3106.2 negative control: a Google Fonts <link> (one external request)"),
    ("M13", DECK, [("table{border-collapse:collapse;width:100%%;margin",
                    "table{border-collapse:collapse;width:600px;margin")],
     TC16, "a fixed 600 px table (horizontal page scroll at 390 px)"),
    ("M14", DECK, [("@media (prefers-color-scheme:light){ :root{%(light)s} }\n", "")],
     TC16, "the light palette never applies (both schemes paint the same background)"),
    ("M15", DECK, [("  .g-wide{display:none} .g-narrow{display:block}\n", "")],
     TC16, "the 390 px second layout never swaps in"),
    ("M16", DECK, [('if not p["archived"] and ts:', "if ts:")],
     TC13, "LLR-3105.1 negative control: an archived project gets a slide"),
    ("M17", DECK, [('if not p["archived"] and ts:', 'if not p["archived"]:')],
     TC13, "a task-less project gets a slide"),
    ("M18", DECK, [('ts = [t for t in d["tasks"] if t["project"] == p["key"]]',
                    'ts = [t for t in d["tasks"] if t["project"] == p["key"] and t["status"] != "archived"]')],
     TC13, "R1: an all-archived project (or Inbox) gets no slide"),
    ("M19", DECK, [('count = _plural(len(live), "task")', 'count = _plural(len(tasks), "task")')],
     TC13, "D12: the printed count includes archived tasks"),
    ("M20", DECK, [('    live = [t for t in tasks if t["status"] != "archived"]\n    k = ',
                    '    live = [t for t in tasks if not t["archived"]]\n    k = ')],
     TC13, "D19: the slide re-derives archived from the flag instead of reading status"),
    ("M21", DECK, [("    else if (e.key === 'Home') { show(0); e.preventDefault(); }\n", "")],
     TC14, "LLR-3105.2 negative control: the Home handler dropped"),
    ("M22", DECK, [("t.tagName === 'INPUT' || ", "")],
     TC14, "keys page the deck while an input has focus"),
    ("M23", DECK, [("t.tagName === 'TEXTAREA' ||", "")],
     TC14, "keys page the deck while a textarea has focus"),
    ("M24", DECK, [("cur = Math.min(slides.length - 1, Math.max(0, n));",
                    "cur = (n + slides.length) % slides.length;")],
     TC14, "ArrowRight on the last slide wraps to the first"),
    ("M25", DECK, [(".slide{display:block!important;break-after:page;max-width:none}",
                    ".slide{display:block!important;max-width:none}")],
     TC14, "print: no page break after each slide"),
    ("M26", DECK, [(".slide{display:block!important;break-after:page;max-width:none}",
                    ".slide{break-after:page;max-width:none}")],
     TC14, "print: only the current slide prints"),
    ("M27", DECK, [("  :root{color-scheme:light;%(light)s}\n", "")],
     TC14, "print: the dark palette prints (no light palette)"),
    ("M28", DECK, [("  .bar-nav{display:none}\n", "")],
     TC14, "print: the paging bar prints"),
    ("M29", DECK, [("from .report_html import esc\n", "from .report_html import esc\nfrom .views import HEX\n")],
     TC04, "LLR-3101.3 negative control: the deck imports views.HEX"),
    ("M30", HTML, [('closed=status in ("done", "archived")', 'closed=status == "archived"')],
     TC02, "amendment: done tasks pass closed=False (a done task reads '30d overdue')"),
    ("M31", HTML, [('closed=status in ("done", "archived")', 'closed=status == "archived"')],
     NEVER, "the same fault, seen through the workspace card and the deck row"),
    ("M32", DECK, [("    if (e.ctrlKey || e.altKey || e.metaKey) { return; }\n", "")],
     TC14, "CR3-2: Ctrl/Alt/Meta combinations page the deck (taken from the browser)"),
    ("M33", DECK, [("""+ f'<tspan class="{cls}">{esc(text)}</tspan>'""",
                    """+ f'<tspan class="{cls}">{text}</tspan>'""")],
     AT6, "CR3-3: esc removed from the gantt meta tspan (phase / due word / class label)"),
    ("M34", DECK, [("""\"></span>{esc(n)}</span>'""", """\"></span>{n}</span>'""")],
     AT6, "CR3-3: esc removed from the legend's phase name"),
    ("M35", DECK, [("""{esc(m["shape"])} {esc(m["name"])}</span>'""", """{esc(m["shape"])} {m["name"]}</span>'""")],
     AT6, "CR3-3: esc removed from the legend's class name"),
    ("M36", DECK, [("""text-anchor="end">{esc(label)}</text>')""", """text-anchor="end">{label}</text>')"""),
                   ("""f"{esc(label)}</text>")""", """f"{label}</text>")""")],
     AT6, "esc removed from the milestone's class label"),
    ("M37", DECK, [("""href="{esc(h)}" target""", """href="{h}" target""")],
     AT6, "SC1: the deck writes a task URL into href unescaped (a quote breaks out to onmouseover)"),
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

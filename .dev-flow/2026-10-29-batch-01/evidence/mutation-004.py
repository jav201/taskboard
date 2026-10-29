"""Increment 004 mutation battery (batch 2026-10-29-batch-01): the `H` export from the app —
the seat, the `ReportExport` modal, the action, the toast and the `o` offer.

Each mutant is a single fault in one file — the increment's SOURCE `taskboard/keymap.py`,
`taskboard/modals.py` or `taskboard/app.py`, or (M15, the contract's named negative control
for AT-3105) `taskboard/report_deck.py` — applied as exact string replacements (each `old`
must occur exactly once), run against the named node, then the file is restored
byte-identically: its sha256 is printed before the mutation and after the restore. A mutant
is KILLED when pytest exits non-zero AND the named node is among the FAILED.

Run from the worktree root:
  env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-004.py [M01 M02 ...]
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KEYMAP = ROOT / "taskboard" / "keymap.py"
MODALS = ROOT / "taskboard" / "modals.py"
APP = ROOT / "taskboard" / "app.py"
DECK = ROOT / "taskboard" / "report_deck.py"
T = "tests/test_report_export_app.py"
MK = "tests/test_modal_keys.py"
AT1 = ("AT_3101", "test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it")
AT5 = ("AT_3105", "test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project")
AT7 = ("AT_3107", "test_AT_3107_the_report_modal_obeys_the_modal_key_law", MK)
TC17 = ("TC_3117", "test_TC_3117_H_is_seated_once_off_the_bar")
TC18 = ("TC_3118", "test_TC_3118_scope_keys_and_no_project")
TC19 = ("TC_3119", "test_TC_3119_files_land_beside_the_open_board")
TC20 = ("TC_3120", "test_TC_3120_o_opens_the_report_while_the_toast_lives")
TC20F = ("failed_write", "test_TC_3120_a_failed_write_toasts_and_offers_nothing")
INV = ("TC_2407_every_modal_is_in_the_inventory", "test_TC_2407_every_modal_is_in_the_inventory", MK)

H_ROW = """    Key("H", "H", "report_export", "Report", group="misc", bar=False),\n"""

# (id, file, [(old, new), ...], (-k expression, node that must go RED[, test file]), what it breaks)
MUTANTS = [
    ("M01", KEYMAP, [(H_ROW, "")], TC17, "LLR-3107.1 negative control: the `H` row dropped"),
    ("M02", KEYMAP, [(H_ROW, H_ROW.replace("bar=False", "bar=True"))], TC17,
     "the `H` seat drawn on the bar (not off it like R/A/S)"),
    ("M03", MODALS, [(""",\n                ("o", "all boards"), ("esc", "close")]""",
                      """,\n                ("o", "all boards")]""")], AT7,
     "AT-3107 negative control: the key line drops `esc close`"),
    ("M04", MODALS, [("""        body.append("\\n\\nWrites to  ", style=HEX["mut"])\n"""
                      """        body.append(where, style=HEX["ink"])\n""", "")],
     AT7, "LLR-3107.2: the destination folder never printed"),
    ("M05", MODALS, [("""f"all boards ({len(self.boards)})", "   " + " · ".join(self.boards)),""",
                      """f"all boards ({len(self.boards)})", ""),""")], AT7,
     "PDR C9: the board names the file will contain never printed"),
    ("M06", MODALS, [("""        if scope == "project" and self.project is None:  # nothing to scope to: `o` stays\n"""
                      """            return\n""", "")],
     TC18, "LLR-3107.2: `p` with no current project moves the mark anyway"),
    ("M07", MODALS, [("""        self.scope = "all"\n""", """        self.scope = "project"\n""")], TC18,
     "HR-2: the scope starts at `p`, not `o`"),
    ("M08", MODALS, [("""Binding("p", "scope('project')", "", priority=True, show=False)""",
                      """Binding("p", "write('workspace')", "", priority=True, show=False)""")], AT7,
     "`p` writes and closes instead of moving the scope mark"),
    ("M09", APP, [("""        pid = task.project_id if task is not None else self.focused_project_id\n""",
                   """        pid = present_project_id(self.board, self.selected_task_id,"""
                   """ self.focused_project_id)\n""")],
     TC18, "LLR-3107.2 negative control: the current project from present_project_id's "
           "first-project fallback"),
    ("M10", APP, [("""        folder = Path(self.board.path).parent / "reports"\n"""
                   """        self.push_screen(ReportExport(""",
                   """        folder = Path("reports")\n        self.push_screen(ReportExport(""")], TC19,
     "LLR-3107.3 negative control: the files written beside the CWD"),
    ("M11", APP, [("""                                project=key if scope == "project" else None)""",
                   """                                project=None)""")], AT5,
     "HR-5: the app's `p` scope ignored (the deck holds every project)"),
    ("M12", APP, [("""            key = f"{bid if bid is not None else f'#{pos}'}:{proj.id}" """,
                   """            key = proj.id """)], AT5,
     "PDR C5: the bare project id passed to extract instead of the key"),
    ("M13", APP, [("""        text = (f"Report written: {' and '.join(p.name for p in paths)} to {folder}\"""",
                   """        text = (f"Report written: report to {folder}\"""")], AT1,
     "HLR-3107 negative control: the toast drops the file name"),
    ("M14", APP, [("""        if skipped:\n"""
                   """            text += f" · {skipped} board{'s' if skipped > 1 else ''} skipped"\n""", "")],
     TC19, "LLR-3107.4: the skipped board never counted in the toast"),
    ("M15", DECK, [("""        if not p["archived"] and ts:""", """        if ts:""")], AT5,
     "AT-3105's named control: the deck keeps archived projects (a divergent slide set)"),
    ("M16", APP, [("""        if offer is not None:""",
                   """        if False:""")], AT1,
     "HLR-3107 negative control: `o` keeps `open_url` (no offer branch)"),
    ("M17", APP, [("""            if self._report_clock() < offer[1]:""", """            if True:""")], TC20,
     "LLR-3107.4 negative control: the offer never expires"),
    ("M18", APP, [("""            self._report_offer = None\n            if self._report_clock()""",
                   """            if self._report_clock()""")], TC20, "PDR C8: the offer is not single-use"),
    ("M20", APP, [("""        self._report_offer = (paths[0], self._report_clock() + 10)""",
                   """        self._report_offer = (paths[-1], self._report_clock() + 10)""")], TC20,
     "LLR-3107.4: after `a`, `o` opens the deck instead of the workspace"),
    ("M21", APP, [("""opened = webbrowser.open(path.as_uri())""", """opened = webbrowser.open(str(path))""")],
     TC20, "D9: off Windows the opener gets a bare path, not the file URI"),
    ("M22", APP, [("""        self.notify(text, title="Report", severity="information", timeout=10, markup=False)""",
                   """        self.notify(text, title="Report", severity="information", timeout=5, markup=False)""")],
     AT1, "LLR-3107.4: the toast lives 5 s, not the offer's 10"),
    ("M23", MODALS, [("""    def action_write(self, kind: str) -> None:\n""",
                      """    def _probe(self):\n        return Button("x")\n\n"""
                      """    def action_write(self, kind: str) -> None:\n""")],
     INV, "LLR-3107.2 / TC-2407: the modal grows a Button its INVENTORY row `{}` does not name"),
    ("M24", APP, [("""            paths = report_html.write_reports(d, kinds, folder, today)""",
                   """            paths = report_html.write_reports(d, kinds[:1], folder, today)""")], AT7,
     "`a` writes only the workspace"),
    ("M25", MODALS, [(""""both": ("workspace", "deck")}""", """"both": ("workspace",)}""")], AT7,
     "CR4-1: the `both` token maps to the workspace alone"),
    ("M26", APP, [("""        try:\n            paths = report_html.write_reports(d, kinds, folder, today)\n"""
                   """        except OSError as e:""",
                   """        if True:\n            paths = report_html.write_reports(d, kinds, folder, today)\n"""
                   """        if False:\n            e = None""")],
     TC20F, "CR4-2: the write unguarded (an OSError reaches the app)"),
    ("M27", APP, [("""# a part may be written: no offer\n            self._report_offer = None\n""",
                   """# a part may be written: no offer\n""")],
     TC20F, "CR4-2: the earlier offer left set when a write fails"),
    ("M28", APP, [("""        if not opened:\n""", """        if False:\n""")], TC20,
     "CR4-3: a failed opener says nothing"),
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

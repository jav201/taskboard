"""Premise probes of batch 2026-10-24-batch-01, run on the worktree tree
(HEAD 9873674, branch feat/milestone-marks, base_ref 7e66e0e) from the project
root:  python .dev-flow/2026-10-24-batch-01/evidence/premises.py
Static, read-only probes: no module is imported, no file is written, the real
home is never touched. One printed line per premise."""
import ast
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTO = (ROOT / "prototypes" / "milestone_marks" / "proto.py").read_text(encoding="utf-8")
VIEWS = (ROOT / "taskboard" / "views.py").read_text(encoding="utf-8")
APP = (ROOT / "taskboard" / "app.py").read_text(encoding="utf-8")
KEYMAP = (ROOT / "taskboard" / "keymap.py").read_text(encoding="utf-8")
MODALS = (ROOT / "taskboard" / "modals.py").read_text(encoding="utf-8")
PEOPLE = (ROOT / "taskboard" / "people.py").read_text(encoding="utf-8")
MODELS = (ROOT / "taskboard" / "models.py").read_text(encoding="utf-8")
CONFTEST = (ROOT / "tests" / "conftest.py").read_text(encoding="utf-8")
TEAMSYNC = (ROOT / "taskboard" / "team_sync.py").read_text(encoding="utf-8")


def line_of(text, needle, start=0):
    i = text.find(needle, start)
    if i < 0:
        return -1
    return text.count("\n", 0, i) + 1


def probe(n, text):
    print(f"P-{n} {text}")


head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                      text=True, cwd=ROOT).stdout.strip()

# P-1: the round's chosen variants exist in proto.py at the cited lines
p1 = {
    "HOLLOW": line_of(PROTO, 'HOLLOW = {'),
    "SHAPES": line_of(PROTO, 'SHAPES = ['),
    "mark_key": line_of(PROTO, "def mark_key("),
    "variant B branch": line_of(PROTO, 'elif v == "B"'),
    "gantt_milestone_cells_m": line_of(PROTO, "def gantt_milestone_cells_m("),
    "band_milestone_facts_m": line_of(PROTO, "def band_milestone_facts_m("),
    "agenda_row_m": line_of(PROTO, "def agenda_row_m("),
    "legend_strip": line_of(PROTO, "def legend_strip("),
    "_hide": line_of(PROTO, "def _hide("),
    "legend_strip_project": line_of(PROTO, "def legend_strip_project("),
    "present_tasks_m": line_of(PROTO, "def present_tasks_m("),
    "matches_m": line_of(PROTO, "def matches_m("),
    "filter_bar_m": line_of(PROTO, "def filter_bar_m("),
    "EditorSelect (variant A)": line_of(PROTO, "class EditorSelect("),
    "Select after #f-milestone": line_of(PROTO, 'mount(s, after="#f-milestone")'),
    "MarkForm": line_of(PROTO, "class MarkForm("),
    "MarksWindow (the # manager)": line_of(PROTO, "class MarksWindow("),
}
probe(1, f"proto.py's chosen variants at HEAD {head}: "
         + " | ".join(f"{k} @{v}" for k, v in p1.items())
         + f" | all found: {all(v > 0 for v in p1.values())}")

# P-2: the section-3 milestone sites in views.py / app.py still hold
sites = {
    "lanes marker": 'marker = c("\u25c6", milestone_tone(t, board, today))',
    "focus row": 'marker = c("\u25c6", milestone_tone(task, board, today))',
    "bank edge": 'body = _put_cell(row, edge_cell, c("\u25c6", lane.hue))',
    "kanban/focus glyph": 'glyph = "\u25c6" if t.milestone',
    "gantt title": 'return (c("\u25c6", milestone_tone(task, board, today)) + " "',
    "gantt cells": 'marks = [("\u25c6", tone)]',
    "gantt one-date": 'cells[x] = ("\u25c6", tone)',
    "gantt echo": 'return ({x: "\u25c6"}, tone',
    "ruler milestones": 'marks[ax.cell(md_)] = ("\u25c6", milestone_tone(t, board, today))',
    "gantt label": 'label = " " + c("\u25c6", tone) + " "',
    "chainmap label": 'c("\u25c6", milestone_tone(t, board, today)) + " " if t.milestone',
    "band facts": 'out = [("\u25c6 ", tone), (_md(d), dk)]',
    "fold row": 'full += f" \u00b7 \u25b2{late_ms} \u25c6"',
    "present field row": 'cells = [("\u25c6", "accent") if g == "\u25c6" else (g, k)',
    "agenda row (no \u25c6 today)": "def _agenda_row(",
    "people task rows": "def _task_rows(",
    "notice reached": "reached \u00b7 \u25c6\u2713 \u00b7 u undo",
    "notice milestone": "is a milestone \u00b7 \u25c6 ",
}
found = {k: line_of(VIEWS, v) for k, v in sites.items() if not k.startswith("notice")}
found.update({k: line_of(APP, v) for k, v in sites.items() if k.startswith("notice")})
excl = {
    "title glyph": line_of(VIEWS, 'c("\u25c6 TASKBOARD", "bright", bold=True)'),
    "project due 2613-ish": line_of(VIEWS, 'cells[c1] = ("\u25c6", project.color)'),
    "sel_p due": line_of(VIEWS, 'marks[ax.cell(pd)] = ("\u25c6", sel_p.color)'),
    "mlabel due": line_of(VIEWS, 'c("\u25c6", sel_p.color)'),
    "present proj due": line_of(VIEWS, 'marks[ax.cell(pd)] = ("\u25c6", proj.color)'),
    "app slip notice (project-span, excluded)": line_of(APP, "d past \u25c6"),
}
probe(2, "section-3 sites still hold: "
         + " | ".join(f"{k} @{v}" for k, v in found.items())
         + f" | all found: {all(v > 0 for v in found.values())}"
         + " || exclusions stay: "
         + " | ".join(f"{k} @{v}" for k, v in excl.items()))

# P-3: people.py's Directory is the reuse pattern
p3 = {
    "file_lock, keep_aside import": line_of(PEOPLE, "from .boards import file_lock, keep_aside"),
    "write_atomic import": line_of(PEOPLE, "from .models import"),
    "PEOPLE_NAME": line_of(PEOPLE, 'PEOPLE_NAME = "people.json"'),
    "Directory.load": line_of(PEOPLE, "def load(cls, path)"),
    "keep_aside on unreadable": line_of(PEOPLE, "backup = keep_aside(path)"),
    "_commit under file_lock": line_of(PEOPLE, "with file_lock(self.path):"),
    "write_atomic": line_of(PEOPLE, "write_atomic(self.path,"),
    "handle_for": line_of(PEOPLE, "def handle_for(name: str, taken)"),
}
probe(3, "people.py Directory pattern: "
         + " | ".join(f"{k} @{v}" for k, v in p3.items())
         + f" | all found: {all(v > 0 for v in p3.values())}")

# P-4: '#' (number_sign) is free in keymap.py and unbound in app.py's screens
probe(4, f"'#' free as a KEY: number_sign in keymap.py: {'number_sign' in KEYMAP} | "
         f"a quoted '#' key in keymap.py: {bool(re.search(r'[\'\"]#', KEYMAP))} | "
         f"number_sign in app.py: {'number_sign' in APP}")

# P-5: the modal-keys law and the editor's mount points exist
p5 = {
    "ButtonKeysMixin": line_of(MODALS, "class ButtonKeysMixin:"),
    "TASK_KEYS": line_of(MODALS, "TASK_KEYS = ["),
    "#task-chips-what": line_of(MODALS, 'Horizontal(id="task-chips-what")'),
    "#f-milestone": line_of(MODALS, 'id="f-milestone"'),
}
probe(5, "modal law + editor seats: "
         + " | ".join(f"{k} @{v}" for k, v in p5.items())
         + f" | test_modal_keys.py: {(ROOT / 'tests' / 'test_modal_keys.py').exists()}")

# P-6: the conftest seam keeps tests off the real home
probe(6, f"conftest seam: Path.home monkeypatched: "
         f"{'monkeypatch.setattr(Path, \"home\"' in CONFTEST} | "
         f"line @{line_of(CONFTEST, 'monkeypatch.setattr(Path, \"home\"')}")

# P-7: the app loads a directory beside the registry and hands it to boards
p7 = {
    "Directory.load beside registry": line_of(APP, "Directory.load(self.registry.path.parent / PEOPLE_NAME)"),
    "board.people set": line_of(APP, "self.board.people = self.people.people"),
    "unreadable notice": line_of(APP, 'could not be read; {kept}.'),
    "present_tasks consumed": line_of(APP, "present_tasks(self._board, self._project_id)"),
}
probe(7, "app directory pattern: "
         + " | ".join(f"{k} @{v}" for k, v in p7.items())
         + f" | all found: {all(v > 0 for v in p7.values())}")

# P-8: the suite's scale (static count; the 3152 baseline is re-measured at P4)
n = 0
files = 0
for p in sorted((ROOT / "tests").glob("test_*.py")):
    files += 1
    tree = ast.parse(p.read_text(encoding="utf-8"))
    n += sum(1 for node in ast.walk(tree)
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name.startswith("test_"))
probe(8, f"tests/ static count: {files} files, {n} test functions "
         f"(the commission's full-suite baseline is 3152 passed, re-measured at P4)")

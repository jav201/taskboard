"""Mutation battery of the DDR folds (batch 2026-10-20-batch-03), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_all_agenda.py::"
MK = "tests/test_modal_keys.py::test_AT_2407_alt_s_saves_and_letters_type"
PR = "tests/test_present_backlog_round.py::test_AT_2405_K_and_J_reorder"
A, M, C = "taskboard/app.py", "taskboard/modals.py", "taskboard/taskboard.tcss"
DOCK = "    dock: bottom;\n    width: 100%;"
ARMS = [
    ("D1 the form's key line not docked (ux UX-DDR-1), 118x30", C, DOCK, "    width: 100%;",
     MK + "[size0]"),
    ("D1b the form's key line not docked, 80x24", C, DOCK, "    width: 100%;", MK + "[size1]"),
    ("D2 the editor's long words back (ux UX-DDR-2)", M,
     '("alt+i", "image"), ("alt+t", "start"), ("alt+d", "due"),',
     '("alt+i", "paste image"), ("alt+t", "start date"), ("alt+d", "due date"),', MK + "[size1]"),
    ("D3 `J` not saved (qa QA-DDR-2)", A,
     "        set_present_order(self._board, ids)\n        self._board.save()",
     "        set_present_order(self._board, ids)\n        if delta < 0:\n            self._board.save()",
     PR),
    ("D4 the agenda's jump writes the board (qa QA-DDR-1, DDR-C1)", A,
     "            app.jump_to(it.task.id)\n",
     "            app.jump_to(it.task.id)\n            app.selected_task.title += ' (edited)'\n"
     "            app.board.save()\n",
     T + "test_AT_2401_one_screen_for_every_board"),
    ("D5 the --open notice in the second person (P4's escaped regression)", A,
     'f"to the boards (--open). B lists the {n} "', 'f"to your boards (--open). B lists your {n} "',
     "tests/test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person"),
    ("D5b the --open notice in the second person (AT)", A,
     'f"to the boards (--open). B lists the {n} "', 'f"to your boards (--open). B lists your {n} "',
     "tests/test_boards_backlog_round.py::test_AT_2410_open_without_registering"),
]
print("arms:", len(ARMS), flush=True)
bad = 0
env = dict(os.environ, PY_COLORS="0", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
env.pop("NO_COLOR", None)
for label, path, old, new, node in ARMS:
    f = pathlib.Path(path)
    src = f.read_bytes()
    text = src.decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    o, n = old.replace("\n", nl), new.replace("\n", nl)
    h0 = hashlib.sha256(src).hexdigest()
    if text.count(o) != 1:
        print(f"{label}: BAD (anchor found {text.count(o)} times)", flush=True)
        bad += 1
        continue
    try:
        f.write_bytes(text.replace(o, n, 1).encode("utf-8"))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--color=no", node], env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
    finally:
        f.write_bytes(src)
    h1 = hashlib.sha256(f.read_bytes()).hexdigest()
    assert h1 == h0, "the restore is not proven"
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    bad += verdict != "RED (KILLED)"
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"{label} · {path} · {node.split('::')[1]}: {verdict or 'CRASH/BAD (exit %d)' % r.returncode}"
          f" · sha256 {h0[:12]} restored · {tail}", flush=True)
print("not killed:", bad)
sys.exit(1 if bad else 0)

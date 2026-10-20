"""Increment 001's mutation battery (C-40): one edit per arm, its node(s) run,
the file restored and its hash compared. Run from the project root, NO_COLOR unset:

    python .dev-flow/2026-10-20-batch-01/evidence/mutate-001.py > .dev-flow/2026-10-20-batch-01/evidence/mutation-001.txt
"""
import hashlib
import os
import pathlib
import subprocess
import sys

T = "tests/test_boards.py::"
ARMS = [
    ("taskboard/boards.py", "backup = _keep_aside(path)", "backup = None",
     [T + "test_TC_2201_an_unreadable_registry_is_kept_aside"]),
    ("taskboard/boards.py", 'with open(dest, "xb") as fh:', 'with open(dest, "wb") as fh:',
     [T + "test_TC_2201_an_existing_corrupt_copy_is_never_overwritten"]),
    ("taskboard/boards.py", "            if key in seen_paths:\n                continue",
     "            if False:\n                continue", [T + "test_TC_2201_the_entry_rules"]),
    ("taskboard/boards.py", " or not Path(p).expanduser().is_absolute():", ":",
     [T + "test_TC_2201_the_entry_rules"]),
    ("taskboard/boards.py", 'item.get("archived") is True', 'bool(item.get("archived"))',
     [T + "test_TC_2201_the_entry_rules"]),
    ("taskboard/boards.py", "        if len(self.entries) > 1 or self.path.exists():",
     "        if True:", [T + "test_TC_2201_touch_writes_only_with_more_than_one_board_or_a_file"]),
    ("taskboard/boards.py", "            return      # the unreadable file stays",
     "            pass      # the unreadable file stays",
     [T + "test_AT_2201_no_registry_and_an_unreadable_one"]),
    ("taskboard/boards.py", "        write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))",
     '        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")',
     [T + "test_TC_2201_the_round_trip_and_the_atomic_save"]),
    ("taskboard/boards.py", "            except OSError as exc:      # bookkeeping",
     "            except ZeroDivisionError as exc:      # bookkeeping",
     [T + "test_TC_2202_a_registry_that_cannot_be_written_never_stops_a_start"]),
    ("taskboard/boards.py", "    if not readable:", "    if False:",
     [T + "test_TC_2201_peek_board_never_writes"]),
    ("taskboard/boards.py", "            if self._is_main(e) or Path(e.path).exists():",
     "            if True:", [T + "test_TC_2201_opening",
                             T + "test_TC_2202_the_last_board_missing_at_start"]),
    ("taskboard/boards.py",
     "        return self.main_path is not None and _key(e.path) == _key(self.main_path)",
     "        return e.id == MAIN_ID", [T + "test_TC_2201_opening"]),
    ("taskboard/app.py", "        self._undo_stack = []\n        self._gantt_group = self._gantt_previous = None",
     "        self._gantt_group = self._gantt_previous = None",
     [T + "test_TC_2202_switch_board_starts_the_other_board_over"]),
    ("taskboard/app.py", "            self._team_timer.stop()\n", "",
     [T + "test_TC_2202_switch_board_starts_the_other_board_over"]),
    ("taskboard/app.py", "        if not self._open_board():", "        if False:",
     [T + "test_TC_2202_a_switched_board_gets_the_start_a_board_gets",
      T + "test_TC_2202_a_switch_into_a_team_board_starts_its_timer"]),
    ("taskboard/app.py", "        if at_mount:\n", "        if True:\n",
     [T + "test_TC_2202_the_mount_order_is_the_shipped_one"]),
    ("taskboard/app.py", "        if result.error is not None and at_switch:", "        if False:",
     [T + "test_TC_2202_a_failed_migration_at_a_switch_keeps_the_open_board"]),
    ("taskboard/app.py", "            for k, v in before.items():\n                setattr(self, k, v)",
     '            self.board, self.board_id = before["board"], before["board_id"]',
     [T + "test_TC_2202_a_failed_migration_at_a_switch_keeps_the_open_board"]),
    ("taskboard/app.py", "        if not Path(entry.path).exists():", "        if False:",
     [T + "test_TC_2202_a_missing_board_file_opens_nothing"]),
    ("taskboard/__main__.py", "    entry = registry.register(board) if board else registry.opening()",
     "    entry = registry.opening()", [T + "test_TC_2202_open_app_picks_the_board"]),
]

print("arms:", sum(len(n) for *_x, n in ARMS))
bad = 0
for path, old, new, nodes in ARMS:
    f = pathlib.Path(path)
    src = f.read_bytes()
    h0 = hashlib.sha256(src).hexdigest()
    text = src.decode("utf-8")
    assert text.count(old) == 1, ("anchor", path, old)
    for node in nodes:
        try:
            f.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            assert hashlib.sha256(f.read_bytes()).hexdigest() != h0, "the edit did not apply"
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", node], env=dict(os.environ, PY_COLORS="0",
                                                              PYTHONDONTWRITEBYTECODE="1"),
                               capture_output=True, text=True)
        finally:
            f.write_bytes(src)
        h1 = hashlib.sha256(f.read_bytes()).hexdigest()
        assert h1 == h0, "the restore is not proven"
        verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
        bad += verdict != "RED (KILLED)"
        print(f"{path} [{old.strip()[:50]!r} -> {new.strip()[:40]!r}] {node.split('::')[1]}: "
              f"{verdict or 'CRASH/BAD (exit %d)' % r.returncode} · restore {h1[:16]}", flush=True)
print("not killed:", bad)
sys.exit(1 if bad else 0)

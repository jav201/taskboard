"""Mutation battery of increment 001 re-run at the DDR (+ M22, qa QA-13) (batch 2026-10-20-batch-02), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_boards_concurrency.py::"
B, M, E = "taskboard/boards.py", "taskboard/modals.py", "taskboard/__main__.py"
ARMS = [
    ("M1 O_EXCL dropped", B, "os.O_CREAT | os.O_EXCL | os.O_WRONLY", "os.O_CREAT | os.O_WRONLY",
     T + "test_TC_2301_the_lock_is_exclusive_and_released"),
    ("M2 release removed", B, "        if _lock_token(lock) == token:\n            try:\n                os.unlink(lock)",
     "        if _lock_token(lock) == token:\n            try:\n                pass",
     T + "test_TC_2301_the_lock_is_exclusive_and_released"),
    ("M3 stale test inverted", B, "abs(time.time() - st.st_mtime) > LOCK_STALE",
     "abs(time.time() - st.st_mtime) < LOCK_STALE",
     T + "test_TC_2301_a_stale_lock_is_taken_over_and_a_fresh_one_is_not"),
    ("M4 abs dropped (a future time never stale)", B, "abs(time.time() - st.st_mtime)",
     "(time.time() - st.st_mtime)",
     T + "test_TC_2301_a_stale_lock_is_taken_over_and_a_fresh_one_is_not"),
    ("M5 release not owner-checked", B, "        if _lock_token(lock) == token:", "        if True:",
     T + "test_TC_2301_a_taken_over_holder_never_removes_the_new_lock"),
    ("M6 token-less lock left (S-6)", B, "os.unlink(lock)     # never a token-less",
     "pass  # os.unlink(lock)     # never a token-less",
     T + "test_TC_2301_a_lock_whose_token_cannot_be_written_is_removed"),
    ("M7 commit ignores the file", B, "fresh = self._read(self.path, self.main_path)   # a failed read raises",
     "fresh = None   # a failed read raises",
     T + "test_TC_2301_a_stale_registry_keeps_the_other_writers_board"),
    ("M7b commit ignores the file (AT)", B, "fresh = self._read(self.path, self.main_path)   # a failed read raises",
     "fresh = None   # a failed read raises",
     T + "test_AT_2301_a_board_another_taskboard_made_survives"),
    ("M8 commit takes no lock", B, "        with file_lock(self.path):\n            fresh = None",
     "        with ExitStack():\n            fresh = None",
     T + "test_TC_2301_a_failed_write_changes_nothing"),
    ("M8b commit takes no lock (AT)", B, "        with file_lock(self.path):\n            fresh = None",
     "        with ExitStack():\n            fresh = None",
     T + "test_AT_2301_a_board_another_taskboard_made_survives"),
    ("M9 adoption replaces objects", B, "                old.__dict__.update(e.__dict__)\n                e = old",
     "                pass",
     T + "test_TC_2301_a_stale_registry_keeps_the_other_writers_board"),
    ("M10 copy-aside skipped", B, "if fresh is None and not self._set_aside():",
     "if fresh is None and False:",
     T + "test_TC_2301_an_unreadable_registry_is_never_written_over_without_a_copy"),
    ("M11 history copy removed", B, '        if _backup(src.path.parent / "history.jsonl", day):',
     "        if False:",
     T + "test_TC_2303_the_history_is_copied_with_the_board_files"),
    ("M11b history copy removed (AT)", B, '        if _backup(src.path.parent / "history.jsonl", day):',
     "        if False:",
     T + "test_AT_2303_a_move_keeps_the_source_history_bytes"),
    ("M12 partial copy kept", B, "dest.unlink(missing_ok=True)    # never a partial",
     "pass  # dest.unlink(missing_ok=True)    # never a partial",
     T + "test_TC_2303_a_copy_failing_midway_leaves_no_copy"),
    ("M13 move takes no lock", B, "        beat = held.enter_context(file_lock(dst.path, names[1]))",
     "        beat = lambda: None",
     T + "test_TC_2302_a_busy_target_stops_the_move_before_anything"),
    ("M13b move takes no lock (AT)", B, "        beat = held.enter_context(file_lock(dst.path, names[1]))",
     "        beat = lambda: None",
     T + "test_AT_2302_a_move_into_a_busy_board_stops_before_writing"),
    ("M14 stale-plan check before the lock (QA-8)", B,
     "        beat = held.enter_context(file_lock(dst.path, names[1]))\n"
     "        if _stamp(dst.path) != plan.dst_stamp:\n"
     '            raise OSError("the target board changed since the move was planned")',
     "        if _stamp(dst.path) != plan.dst_stamp:\n"
     '            raise OSError("the target board changed since the move was planned")\n'
     "        beat = held.enter_context(file_lock(dst.path, names[1]))",
     T + "test_TC_2302_a_target_rewritten_while_the_move_waited_is_refused"),
    ("M15 lock held past the target save", B, '        steps.append("saved the target")\n        held.close()',
     '        steps.append("saved the target")',
     T + "test_TC_2302_the_lock_is_held_for_the_target_save_only"),
    ("M16 expanduser back at _key", B, "return os.path.normcase(str(_expand_home(path).resolve()))",
     "return os.path.normcase(str(Path(path).expanduser().resolve()))",
     T + "test_TC_2305_tilde_is_the_seam_home"),
    ("M17 the stored path left raw", B, "str(_expand_home(p)),     # no `~` past the door",
     "p,     # no `~` past the door",
     T + "test_AT_2305_a_tilde_board_opens_from_the_seam_home"),
    ("M18 the backups sentence always", M, 'each board file." if steps else "")',
     'each board file." if True else "")',
     T + "test_AT_2302_a_move_into_a_busy_board_stops_before_writing"),
    ("M20 create's id from memory and disk only (F1)", B,
     "            bid = self._unique_id(slug(name), taken)    # unique against the file and the disk",
     "            bid = self.next_id(name)    # unique against the file and the disk",
     T + "test_TC_2301_a_stale_registry_keeps_the_other_writers_board"),
    ("M21 register ignores memory's ids (F5)", B,
     "r._unique_id(slug(name), {x.id for x in self.entries})", "r._unique_id(slug(name))",
     T + "test_TC_2301_an_entry_only_memory_holds_keeps_its_id_and_file"),
    ("M22 touch always commits (qa QA-13)", B,
     "        if len(self.entries) > 1 or self.path.exists():\n\n            def change(r):",
     "        if True:\n\n            def change(r):",
     T + "test_TC_2301_a_one_board_start_takes_no_lock_and_writes_nothing"),
    ("M19 the busy start a traceback", E, "    except OSError as exc:      # the registry busy",
     "    except ZeroDivisionError as exc:      # the registry busy",
     T + "test_TC_2301_a_busy_registry_at_start_is_a_message_not_a_traceback"),
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
                            "--color=no", node], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=300)
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

"""Mutation battery of increment 003 (batch 2026-10-20-batch-03), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_boards_backlog_round.py::"
B, A, E, M = "taskboard/boards.py", "taskboard/app.py", "taskboard/__main__.py", "taskboard/modals.py"
STALE = "        if abs(time.time() - st.st_mtime) > PRESENCE_STALE:"
ARMS = [
    ("M1 the stale test inverted", B, STALE, "        if abs(time.time() - st.st_mtime) < PRESENCE_STALE:",
     T + "test_TC_2409_the_markers"),
    ("M2 abs dropped (a future time never stale)", B, STALE,
     "        if (time.time() - st.st_mtime) > PRESENCE_STALE:", T + "test_TC_2409_the_markers"),
    ("M3 its own marker counted", B, "        if mine is not None and marker == mine:", "        if False:",
     T + "test_TC_2409_the_markers"),
    ("M4 the name pattern ignored", B, "        if not pattern.fullmatch(name):",
     "        if not name.endswith(\".json\"):", T + "test_TC_2409_the_markers"),
    ("M5 a regular-file check dropped", B, "        if not stat.S_ISREG(st.st_mode):\n            continue",
     "        if False:\n            continue", T + "test_TC_2409_the_markers"),
    ("M6 an empty marker left after a failed write", B,
     "            os.unlink(marker)       # never an empty marker that reads as a window (S-7)",
     "            pass", T + "test_TC_2409_the_markers"),
    ("M7 no presence at opening", A, "        self._enter_presence()\n", "",
     T + "test_AT_2409_a_second_window_is_told_once"),
    ("M8 the marker left at exit", A, "        withdraw(self._presence)          # this window leaves the board",
     "        pass", T + "test_AT_2409_a_second_window_is_told_once"),
    ("M9 the marker left at a switch", A,
     "        withdraw(self._presence)\n        self._presence = announce(self.board.path, datetime.now())",
     "        self._presence = announce(self.board.path, datetime.now())",
     T + "test_AT_2409_a_second_window_is_told_once"),
    ("M10 a gone marker never re-announced", A,
     "            self._presence = announce(self.board.path, datetime.now())", "            pass",
     T + "test_TC_2409_the_lifecycle"),
    ("M11 the notice parsed as markup (S-1)", A,
     'title="Boards · open twice", severity="warning", timeout=30, markup=False)',
     'title="Boards · open twice", severity="warning", timeout=30, markup=True)',
     T + "test_TC_2409_the_lifecycle"),
    ("M11b the --open notice parsed as markup (S-14)", A,
     '                            title="Boards", timeout=15, markup=False)',
     '                            title="Boards", timeout=15, markup=True)',
     T + "test_TC_2410_the_unlisted_board_in_the_app"),
    ("M11c an offset `since` kept (S-13)", B,
     "        return since if since is None or since.tzinfo is None else None", "        return since",
     T + "test_TC_2409_the_markers"),
    ("M11d renew without the time (code review CR-2)", B, "        os.utime(marker)\n        return True",
     "        return marker.exists()", T + "test_TC_2409_the_markers"),
    ("M12 --open's check removed (S-3)", E, "    if args.open is not None and not _a_board_file(args.open):",
     "    if False:", T + "test_TC_2410_a_path_that_is_no_board_is_refused[missing-True]"),
    ("M12b --open's check removed", E, "    if args.open is not None and not _a_board_file(args.open):",
     "    if False:", T + "test_TC_2410_a_path_that_is_no_board_is_refused[text-False]"),
    ("M13 --open registers", E,
     "        return TaskboardApp(board_path=expand_home(unlisted), registry=registry)",
     "        entry = registry.register(unlisted)\n        return TaskboardApp(board_path=entry.path, registry=registry)",
     T + "test_TC_2410_open_app_registers_nothing"),
    ("M13b --open registers (AT)", E,
     "        return TaskboardApp(board_path=expand_home(unlisted), registry=registry)",
     "        entry = registry.register(unlisted)\n        return TaskboardApp(board_path=entry.path, registry=registry)",
     T + "test_AT_2410_open_without_registering"),
    ("M14 the home opened over an unlisted board", A,
     "        if len(self.registry.active()) > 1 and self.board_id is not None:",
     "        if len(self.registry.active()) > 1:", T + "test_AT_2410_open_without_registering"),
    ("M15 the move out of an unlisted board offered", M, "        if app.board_id is None:\n",
     "        if False:\n", T + "test_AT_2410_open_without_registering"),
    ("M16 no `not listed` label", A,
     '            self.board.label = (f"{name_for(self.board.path)} · not listed", "pink")',
     "            self.board.label = None", T + "test_TC_2410_the_unlisted_board_in_the_app"),
    ("M17 the offer's chip dropped", M, 'board_chip_text(self.board.label),',
     "Text(),", T + "test_AT_2408_the_start_up_modals_say_their_board"),
    ("M18 the app passes the picker no label", A, "TeamIdentityPicker(roster, self.board.label)",
     "TeamIdentityPicker(roster)", T + "test_AT_2408_the_start_up_modals_say_their_board"),
    ("M19 the picker's key line dropped", M,
     '            yield Label(key_line([("↵", "pick"), ("esc", "cancel")]), id="identity-keys")\n', "",
     T + "test_TC_2408_the_titles_open_with_the_chip"),
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

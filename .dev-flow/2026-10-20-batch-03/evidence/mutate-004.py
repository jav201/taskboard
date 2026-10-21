"""Mutation battery of increment 004 (batch 2026-10-20-batch-03), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_all_agenda.py::"
A, V, K = "taskboard/app.py", "taskboard/views.py", "taskboard/keymap.py"
ARMS = [
    ("M1 the lane order dropped from the sort", V,
     "    return sorted(out, key=lambda x: (x.due, x.lane))     # stable: board order kept",
     "    return sorted(out, key=lambda x: (x.due, x.board_name))",
     T + "test_TC_2401_buckets_and_dues"),
    ("M1b the lane order dropped (AT)", V,
     "    return sorted(out, key=lambda x: (x.due, x.lane))     # stable: board order kept",
     "    return sorted(out, key=lambda x: (x.due, x.board_name))",
     T + "test_AT_2401_one_screen_for_every_board"),
    ("M2 done tasks listed", V, "            if d is None or d > end or not is_open(board, t):",
     "            if d is None or d > end:", T + "test_TC_2401_buckets_and_dues"),
    ("M3 Sunday excluded", V, "            if d is None or d > end or not is_open(board, t):",
     "            if d is None or d >= end or not is_open(board, t):", T + "test_TC_2401_buckets_and_dues"),
    ("M4 the project column at 80", V, "    pw = 22 if inner >= 100 else 0", "    pw = 22",
     T + "test_TC_2401_every_row_is_the_width_and_board_text_is_literal[80]"),
    ("M5 a missing board's lane not marked", V, "        if state and inner >= 100:",
     "        if False:", T + "test_TC_2401_every_row_is_the_width_and_board_text_is_literal[118]"),
    ("M6 `A` refused on the home (the seat rule)", A,
     '        if action == "agenda_all":\n',
     '        if action == "agenda_all" and len(self.screen_stack) == 1:\n',
     T + "test_AT_2401_one_screen_for_every_board"),
    ("M7 the seat keys alive behind the agenda", A,
     "isinstance(sc, (BoardsHome, AllBoardsAgenda))", "isinstance(sc, BoardsHome)",
     T + "test_TC_2401_where_A_acts_and_what_it_holds"),
    ("M8 the jump never switches", A, "            app.switch_board(bid)", "            pass",
     T + "test_AT_2401_one_screen_for_every_board"),
    ("M9 the home's key row without `A`", V, '("x", "archive"), ("A", "all boards"), ("esc", "back")',
     '("x", "archive"), ("esc", "back")', T + "test_AT_2401_one_screen_for_every_board"),
    ("M10 the agenda's key row cut at its tail", A,
     "        if keys.cell_len > w - 2:                     # the tail goes first, never a key",
     "        if False:", T + "test_AT_2401_one_screen_for_every_board"),
    ("M12 the unlisted board's lane dropped (code review CR-1)", A,
     "        if app.board_id is None:                    # an unlisted board (`--open`)",
     "        if False:", T + "test_TC_2401_the_unlisted_board_is_the_last_lane"),
    ("M13 the unlisted lane's jump skipped (CR-1)", A,
     "        if app.board_id == bid or bid is None:", "        if app.board_id == bid and bid is not None:",
     T + "test_TC_2401_the_unlisted_board_is_the_last_lane"),
    ("M14 a failed switch leaves the agenda open (CR-2)", A,
     "        while len(app.screen_stack) > 1:            # the agenda, and the home beneath it\n"
     "            app.pop_screen()\n        if bid is not None and bid != app.board_id:\n"
     "            app.switch_board(bid)\n",
     "        if bid is not None and bid != app.board_id:\n            app.switch_board(bid)\n"
     "            if app.board_id != bid:\n                return\n"
     "        while len(app.screen_stack) > 1:\n            app.pop_screen()\n",
     T + "test_TC_2401_where_A_acts_and_what_it_holds"),
    ("M11 `A` not in the seat", K, '    Key("A", "A", "agenda_all", "All boards", group="misc", bar=False),\n', "",
     T + "test_AT_2401_one_screen_for_every_board"),
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

"""DDR (C-18): increment 002's arms that named AT-2204's two former nodes, rerun
against the one joined node `test_AT_2204_the_home` (every other node dropped),
then (QA-01) the AT-row mutations of design-proposal.md section 5 that no transcript
had armed on their AT node, each against that node,
one edit per arm, the file restored and its hash compared. Run from the project root, NO_COLOR unset:

    python .dev-flow/2026-10-20-batch-01/evidence/mutate-ddr.py > .dev-flow/2026-10-20-batch-01/evidence/mutation-ddr.txt
"""
import hashlib
import os
import pathlib
import subprocess
import sys

H = "tests/test_boards_home.py::"
ARMS = [
    ("taskboard/views.py", '    if not label:\n        return ""', '    if not label:\n        label = ("X", "violet")',
     [H + "test_TC_2203_no_label_is_the_base_frame", H + "test_TC_2203_board_chip"]),
    ("taskboard/views.py", "{escape(fit(name, 24).rstrip())}", "{fit(name, 24).rstrip()}",
     [H + "test_TC_2203_board_chip", H + "test_TC_2203_markup_in_a_board_name_paints_literally"]),
    ("taskboard/views.py", "return c(escape(fit(_strip(title), w)), tone, bold=True)",
     "return c(fit(_strip(title), w), tone, bold=True)",
     [H + "test_TC_2203_markup_in_a_board_name_paints_literally"]),
    ("taskboard/views.py", "fit(name, 24).rstrip()", "fit(name, 99).rstrip()",
     [H + "test_TC_2203_board_chip"]),
    ("taskboard/views.py", "    tvis, rvis = vis(_strip(title)), vis(_strip(right))",
     "    tvis, rvis = vis(_strip(title)) + vis(_strip(board_chip(chip))), vis(_strip(right))",
     [H + "test_TC_2203_every_view_opens_with_the_chip_at_its_width"]),
    ("taskboard/views.py", '    return header(title, right, w, tone, chip=getattr(board, "label", None))',
     "    return header(title, right, w, tone, chip=None)",
     [H + "test_TC_2203_every_view_opens_with_the_chip_at_its_width",
      H + "test_AT_2203_the_chip_in_every_view"]),
    ("taskboard/views.py", '"week": sum(1 for d, _ in upcoming if d <= week_end)',
     '"week": sum(1 for d, _ in upcoming)',
     [H + "test_TC_2204_board_summary_counts_what_the_cards_show"]),
    ("taskboard/views.py", '            "next": upcoming, "by_day": by_day,',
     '            "next": sorted(dues, key=lambda x: x[0]), "by_day": by_day,',
     [H + "test_TC_2204_board_summary_counts_what_the_cards_show"]),
    ("taskboard/views.py", "    if sum(len(a) + 5 for a, _ in parts) > inner:",
     "    if sum(len(a) for a, _ in parts) + 5 * (len(parts) - 1) > inner:",
     [H + "test_TC_2204_the_counts_row_joins_and_shortens",
      H + "test_AT_2204_the_home"]),
    ("taskboard/app.py", '("cursor", "hmove", "toggle_presentation", "boards")',
     '("cursor", "hmove", "toggle_presentation")',
     [H + "test_TC_2204_check_action_and_the_cursor"]),
    ("taskboard/app.py", "        if action in SEAT_ACTIONS and any(", "        if action in SEAT_ACTIONS and False and any(",
     [H + "test_TC_2204_check_action_and_the_cursor", H + "test_AT_2204_the_home"]),
    ("taskboard/app.py", "            elif Path(e.path).exists():\n                self.boards[e.id] = peek_board(e.path)",
     "            elif True:\n                self.boards[e.id] = Board.load(e.path)",
     [H + "test_TC_2204_seven_boards_scroll_and_a_missing_file"]),
    ("taskboard/app.py", "        self.app.pop_screen()\n        self.app.switch_board(entry.id)",
     "        self.app.switch_board(entry.id)\n        self.app.pop_screen()",
     [H + "test_TC_2204_enter_closes_the_home_before_the_board_starts"]),
    ("taskboard/app.py", "        if len(self.registry.active()) > 1:\n            # FIRST",
     "        if True:\n            # FIRST", ["tests/test_boards.py::test_AT_2201_no_registry_and_an_unreadable_one"]),
    ("taskboard/app.py", "                            if entry is not None and len(self.registry.active()) > 1 else None)",
     "                            if entry is not None else None)",
     [H + "test_AT_2203_the_chip_in_every_view"]),
    ("taskboard/keymap.py", '    Key("B", "B", "boards", "Boards", universal=True, primary=True, group="system"),\n', "",
     [H + "test_TC_2204_B_is_in_the_seat_for_every_view", H + "test_AT_2204_the_home"]),
    ("taskboard/app.py", "        if self.boards.get(entry.id) is None:",
     "        if False:", [H + "test_TC_2204_seven_boards_scroll_and_a_missing_file"]),
    # the code review's folds (F1, F2, F3, F6)
    ("taskboard/views.py", "        then = then.replace(tzinfo=None)", "        pass",
     [H + "test_TC_2204_ago_never"]),
    ("taskboard/views.py", '"label", None)), emoji=False)', '"label", None)))',
     [H + "test_TC_2203_markup_in_a_board_name_paints_literally"]),
    ("taskboard/app.py", 'Binding("down,j", "move(2)", "", priority=True, show=False)',
     'Binding("down,j", "move(1)", "", priority=True, show=False)',
     [H + "test_TC_2204_check_action_and_the_cursor"]),
    ("taskboard/app.py", '            if board is None or board.load_report.get("file_unreadable"):',
     "            if board is None:",
     [H + "test_TC_2204_the_home_reads_an_unreadable_board_without_copying_it"]),
]

print("increment 002 arms read:", sum(len(n) for *_x, n in ARMS))
bad = 0
ARMS = [(p, o, n, [x for x in ns if x.endswith("::test_AT_2204_the_home")]) for p, o, n, ns in ARMS]
ARMS = [a for a in ARMS if a[3]]
# QA-01 (the DDR's qa-reviewer): design-proposal.md section 5's AT-row mutations
# armed against their AT node itself, not only a TC node
B = "tests/test_boards.py::test_AT_2201_no_registry_and_an_unreadable_one"
SW = "tests/test_boards_home.py::test_AT_2202_switching_boards_in_place"
HM = "tests/test_boards_home.py::test_AT_2204_the_home"
FM = "tests/test_boards_forms.py::test_AT_2205_manage_boards_from_the_home"
MV = "tests/test_boards_move.py::test_AT_2206_move_a_project_to_another_board"
ARMS += [
    ("taskboard/boards.py", "        if len(self.entries) > 1 or self.path.exists():\n            try:\n                self.save()",
     "        if True:\n            try:\n                self.save()", [B]),                        # touch writing one board
    ("taskboard/boards.py", "            backup = _keep_aside(path)\n", "            backup = None\n", [B]),  # the quarantine skipped
    ("taskboard/app.py", "        board = Board.load(entry.path)\n        if self._team_timer",
     "        board = self.board\n        if self._team_timer", [SW]),                         # the switch not loading the file
    ("taskboard/boards.py", "        self.last = bid\n        entry.last_opened", "        entry.last_opened", [SW]),  # touch not recording last
    ("taskboard/views.py", "    for j, (a, st) in enumerate(parts):", "    for j, (a, st) in enumerate(parts[::-1]):", [HM]),  # the card's text order
    ("taskboard/app.py", "        self.app.pop_screen()\n        self.app.switch_board(entry.id)\n\n    def action_edit",
     "        self.app.pop_screen()\n\n    def action_edit", [FM]),                            # the new board not opened
    ("taskboard/boards.py", "            entry.archived = True\n",
     "            entry.archived = True\n            shutil.rmtree(Path(entry.path).parent, ignore_errors=True)\n", [FM]),  # archive touching the folder
    ("taskboard/boards.py", "        for t in new_src.tasks:\n            t.depends_on = [d for d in t.depends_on if d not in ids]",
     "        for t in new_src.tasks:\n            pass", [MV]),                                  # links not filtered (source side)
    ("taskboard/boards.py", "            t.depends_on = [d for d in t.depends_on if d in ids]",
     "            t.depends_on = list(t.depends_on)", [MV]),                                     # links not filtered (moving side)
]
print("arms (DDR):", len(ARMS))
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
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
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

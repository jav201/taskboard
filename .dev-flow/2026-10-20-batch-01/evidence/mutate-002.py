"""Increment 002's mutation battery (C-40): one edit per arm, its node(s) run,
the file restored and its hash compared. Run from the project root, NO_COLOR unset:

    python .dev-flow/2026-10-20-batch-01/evidence/mutate-002.py > .dev-flow/2026-10-20-batch-01/evidence/mutation-002.txt
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
      H + "test_AT_2204_the_home_is_the_approved_capture"]),
    ("taskboard/app.py", '("cursor", "hmove", "toggle_presentation", "boards")',
     '("cursor", "hmove", "toggle_presentation")',
     [H + "test_TC_2204_check_action_and_the_cursor"]),
    ("taskboard/app.py", "        if action in SEAT_ACTIONS and any(", "        if action in SEAT_ACTIONS and False and any(",
     [H + "test_TC_2204_check_action_and_the_cursor", H + "test_AT_2204_B_and_the_keys_the_home_holds"]),
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
     [H + "test_TC_2204_B_is_in_the_seat_for_every_view", H + "test_AT_2204_B_and_the_keys_the_home_holds"]),
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

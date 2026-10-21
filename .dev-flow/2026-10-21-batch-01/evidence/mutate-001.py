"""Mutation battery of increment 001 (the directory), batch 2026-10-21-batch-01, from the
project root:  python .dev-flow/2026-10-21-batch-01/evidence/mutate-001.py"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from mutlib import run  # noqa: E402

T = "tests/test_people_directory.py::"
P, A, M = "taskboard/people.py", "taskboard/app.py", "taskboard/models.py"
run([
    ("M1 the write skips the re-read (a second window erases the first)", P,
     "                people = self._read(self.path)          # a failed read raises",
     "                people = None", T + "test_TC_2501_two_windows_never_erase_each_others_people"),
    ("M2 the lock dropped", P, "        with file_lock(self.path):", "        if True:",
     T + "test_TC_2501_a_held_lock_makes_the_write_wait_then_fail_and_change_nothing"),
    ("M3 memory updated before the write", P,
     "            result = change(fresh)\n",
     "            result = change(fresh)\n            self._hold(list(fresh.values()))\n",
     T + "test_TC_2501_a_failed_write_changes_nothing_in_memory"),
    ("M4 a repeated handle kept", P, " or pid in seen or not name:", " or not name:",
     T + "test_TC_2501_the_file_is_read_and_bad_entries_are_skipped"),
    ("M5 the role cap dropped", P, '_clean(item.get("role"), ROLE_MAX)', '_clean(item.get("role"), 999)',
     T + "test_TC_2501_the_file_is_read_and_bad_entries_are_skipped"),
    ("M6 an unreadable file not kept aside", P,
     "            backup = keep_aside(path)\n            return cls(path, [],",
     "            backup = None\n            return cls(path, [],",
     T + "test_TC_2501_an_unreadable_file_is_kept_aside_and_the_directory_starts_empty[{not json]"),
    ("M7 the look-behind dropped (an e-mail becomes a mention)", P,
     'MENTION_RE = re.compile(r"(?<![\\w.@])@', 'MENTION_RE = re.compile(r"@',
     T + "test_TC_2502_mentions_are_read_at_word_starts[mail ana@x.com or @@ana-ids3]"),
    ("M8 a handle may end in a dot", P,
     '_H = r"[a-z0-9]+(?:[._-][a-z0-9]+)*"', '_H = r"[a-z0-9]+(?:[._-][a-z0-9]*)*"',
     T + "test_TC_2502_mentions_are_read_at_word_starts[Ask @ana.ruiz.-ids1]"),
    ("M9 the taken handle not numbered", P, "    while h in taken:", "    while False:",
     T + "test_TC_2502_a_taken_handle_gets_the_next_number"),
    ("M10 _label_board does not hand the directory over", A,
     "        self.board.people = self.people.people\n", "",
     T + "test_AT_2501_one_directory_for_every_board"),
    ("M11 the board saves the directory", M,
     "        self.people: dict = {}\n", "        self.people: dict = {}\n        self.settings['people'] = self.people\n",
     T + "test_AT_2501_one_directory_for_every_board"),
    ("M12 the unreadable notice not said", A,
     '        if self.people.load_report.get("unreadable"):', "        if False:",
     T + "test_AT_2501_an_unreadable_directory_is_said_and_kept"),
    ("M13 an empty file reported unreadable", P,
     "            if not path.exists() or not path.read_bytes().strip():",
     "            if not path.exists():",
     T + "test_TC_2501_an_empty_file_is_an_empty_directory_and_nothing_is_said"),
    ("M14 the link's name unbounded (security S-1)", P, r"[^\]\n]{1,60}", r"[^\]\n]+",
     T + "test_TC_2507_a_crafted_note_is_tokenised_in_linear_time[at-bracket-x50000]"),
    ("M16 the dedupe made quadratic again (code review CR-1)", P,
     "    return list(dict.fromkeys(m.group(2) or m.group(3) for m in MENTION_RE.finditer(text)))",
     "    out = []\n    for m in MENTION_RE.finditer(text):\n        h = m.group(2) or m.group(3)\n"
     "        if h not in out:\n            out.append(h)\n    return out",
     T + "test_TC_2507_a_crafted_note_is_tokenised_in_linear_time[distinct-x40000]"),
    ("M17 edit writes a non-handle (code review CR-5)", P,
     "        if not _HANDLE.fullmatch(handle):               # code review CR-5", "        if False:",
     T + "test_TC_2501_edit_writes_back_a_person_the_file_lost_and_refuses_a_non_handle"),
    ("M15 a push carries the directory (the guard on team sync's record)", "taskboard/team_sync.py",
     "            record = board._to_dict(t)\n",
     "            record = dict(board._to_dict(t), people=[p.name for p in board.people.values()])\n",
     T + "test_AT_2507_a_push_carries_mentions_as_handles_and_no_directory"),
])

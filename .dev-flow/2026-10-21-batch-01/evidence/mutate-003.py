"""Mutation battery of increment 003 (the `@` picker), batch 2026-10-21-batch-01, from the
project root:  python .dev-flow/2026-10-21-batch-01/evidence/mutate-003.py"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from mutlib import run  # noqa: E402

T = "tests/test_people_picker.py::"
MO, A = "taskboard/modals.py", "taskboard/app.py"
run([
    ("M1 `+ add` for an exact name and for `@` alone", MO,
     "    if q.strip() and people.named(q) is None:", "    if True:",
     T + "test_TC_2503_rows_list_the_finds_then_add_when_no_name_matches"),
    ("M2 the picker's keys act while it is closed (enter no new line)", MO,
     '            return self._mention == "list" and bool(self._opts)', "            return True",
     T + "test_AT_2503_arrows_choose_and_esc_leaves_plain_text"),
    ("M3 the list kept open when a click leaves the notes (architect A-5)", MO,
     "        if self._mention is not None and not here:", '        if self._mention == "add" and not here:',
     T + "test_AT_2503_a_click_away_closes_the_list"),
    ("M5 a known handle reopens the list", MO,
     '        if m is None or any(self._people.get(h) for h in mention_ids("@" + m.group(1))):',
     "        if m is None:",
     T + "test_TC_2503_no_picker_inside_a_word_or_on_a_known_handle[\\n@ana.ruiz]"),
    ("M6 never flipped above the cursor", MO,
     "        y = off.y + 1 if off.y + 11 <= sh else max(0, off.y - 10)", "        y = off.y + 1",
     T + "test_AT_2503_reached_by_tab_the_list_opens_inside_the_screen_and_flips_up"),
    ("M7 the mention written without its trailing space", MO,
     '            notes.replace(f"@{handle} ", (self._row, self._at), (self._row, end))',
     '            notes.replace(f"@{handle}", (self._row, self._at), (self._row, end))',
     T + "test_AT_2503_at_an_enter_writes_the_handle_and_the_preview_the_name[size0]"),
    ("M8 esc on the list cancels the editor", MO,
     '        elif self._mention == "list":\n            self._close_drop()\n        else:\n            self.dismiss(None)',
     "        else:\n            self.dismiss(None)",
     T + "test_AT_2503_arrows_choose_and_esc_leaves_plain_text"),
    ("M9 a refused add swallowed silently", MO,
     '                self.notify(f"The person was not added: {err}", title="People",\n'
     '                            severity="error", markup=False)\n',
     "                pass\n",
     T + "test_AT_2503_a_failed_add_says_so_and_keeps_the_form"),
    ("M10 the app hands the editor no directory", A,
     "        self.push_screen(TaskModal(self.board, task, people=self.people),",
     "        self.push_screen(TaskModal(self.board, task),",
     T + "test_AT_2503_add_a_person_in_place_for_every_board"),
    ("M11 `tab` in the form loses the role field", MO,
     '        (self.query_one("#md-role", Input) if name.has_focus else name).focus()',
     "        name.focus()",
     T + "test_AT_2503_add_a_person_in_place_for_every_board"),
    ("M12 the form acts with the focus elsewhere and is not closed (code review CR-1)", MO,
     "        if self._mention is not None and not here:", "        if False:",
     T + "test_AT_2503_the_form_left_for_the_notes_closes_and_writes_nothing"),
    ("M13 a sentence-final dot reopens the list (code review CR-2)", MO,
     'any(self._people.get(h) for h in mention_ids("@" + m.group(1)))', "self._people.get(m.group(1))",
     T + "test_TC_2503_no_picker_inside_a_word_or_on_a_known_handle[\\nAsk @ana.ruiz.]"),
    ("M14 an empty list swallows enter (code review CR-4)", MO,
     '            return self._mention == "list" and bool(self._opts)',
     '            return self._mention == "list"',
     T + "test_TC_2503_with_no_one_listed_enter_is_a_new_line"),
])

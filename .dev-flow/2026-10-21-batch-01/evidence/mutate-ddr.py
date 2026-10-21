"""Mutation arms of the DDR's folds (QA-DDR-2: AT-2501's add and AT-2502's rename driven by
keys), batch 2026-10-21-batch-01, from the project root:
    python .dev-flow/2026-10-21-batch-01/evidence/mutate-ddr.py"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from mutlib import run  # noqa: E402

A = "taskboard/app.py"
run([
    ("D1 `n` in the people view adds no one", A,
     '                Binding("n", "new", "", priority=True),',
     '                Binding("n", "noop_new", "", priority=True),',
     "tests/test_people_directory.py::test_AT_2501_one_directory_for_every_board"),
    ("D2 the form's edit keeps the old name", A,
     "                     else self.app.people.edit(handle, *fields))",
     "                     else self.app.people.people[handle])",
     "tests/test_people_look.py::test_AT_2502_a_renamed_person_draws_the_new_name_and_the_note_keeps_the_handle"),
])

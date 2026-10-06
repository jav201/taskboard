"""P4 fold battery (qa F-1, F-2): writes mutants_p4.json for battery.py.

    python -B mk_mutants_p4.py EXPORT_DIR

V1 converts every remaining candidate after the chosen ones, without logging them (F-1:
the saved milestone set beyond the chosen three). V2 marks only reached milestones on the
ruler (F-2: a missing open milestone's mark beside the project due)."""
import json
import sys
from pathlib import Path

AT604 = ["tests/test_milestone_offer.py::test_AT_604_only_what_was_picked_is_converted_backed_up_logged_and_undoable"]
AT602 = ["tests/test_gantt_milestones.py::test_AT_602_milestones_read_as_dates_reached_ones_quiet_the_ruler_marks_them"]
mutants = [
    {"id": "V1", "file": "taskboard/models.py",
     "old": "        for t in convert:\n            set_milestone(t, True)\n",
     "new": "        for t in convert:\n            set_milestone(t, True)\n"
            "        for t, _p in milestone_candidates(board):\n            set_milestone(t, True)\n",
     "what": "unchosen candidates converted silently", "tests": AT604},
    {"id": "V2", "file": "taskboard/views.py",
     "old": "            if (t.project_id == sel_p.id and t.milestone and not t.archived\n",
     "new": "            if (t.project_id == sel_p.id and t.milestone and not t.archived\n"
            "                    and t.phase == board.phases[-1]\n",
     "what": "the ruler marks only reached milestones", "tests": AT602},
]
Path(__file__).with_name("mutants_p4.json").write_text(
    json.dumps({"export": sys.argv[1], "mutants": mutants}, ensure_ascii=False, indent=1),
    encoding="utf-8")
print("mutants_p4.json:", len(mutants))

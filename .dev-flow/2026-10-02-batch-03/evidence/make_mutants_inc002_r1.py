"""Writes mutants_inc002_r1.json: the code-review round-1 findings of increment
002 — F1 (the reset path), F2 (the `z` rule's direction), F3 (the neighbour)."""
import json
from pathlib import Path

T = "tests/test_kanban_readable.py"
A = "taskboard/app.py"


def m(id_, old, new, nodes, why):
    return {"id": id_, "file": A, "old": old, "new": new, "nodes": nodes, "why": why}


MUTANTS = [
    m("Q13", '        if (self.selected_task_id is not None and self.view_mode == "kanban"\n'
             '                and self.kanban_presentation == "grouped"):',
      '        elif (self.selected_task_id is not None and self.view_mode == "kanban"\n'
      '                and self.kanban_presentation == "grouped"):',
      [T + "::test_TC_312_a_reset_selection_never_lands_on_a_counted_card"],
      "F1: the relocation skipped after a reset to the first visible task"),
    m("Q14", "                    (cols[i][0] for i in range(at, -1, -1) if cols[i]), None)",
      "                    (cols[i][0] for i in range(0, at + 1) if cols[i]), None)",
      [T + "::test_TC_312_the_notification_prints_a_bracket_title_literally"],
      "F2 (Z1): the `z` rule takes the leftmost column"),
    m("Q15", "                        self.selected_task_id = col[min(was[1], len(col) - 1)]",
      "                        self.selected_task_id = col[len(col) - 1]",
      [T + "::test_AT_308_finishing_a_card_keeps_the_cursor_on_the_board"],
      "F3 (Z2): the column's last card instead of the one that took its place"),
]

Path(__file__).with_name("mutants_inc002_r1.json").write_text(
    json.dumps(MUTANTS, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(MUTANTS), "mutants")

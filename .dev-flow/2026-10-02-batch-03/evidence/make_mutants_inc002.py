"""Writes mutants_inc002.json: one mutation per law increment 002 claims (C-40)."""
import json
from pathlib import Path

T = "tests/test_kanban_readable.py"
V = "taskboard/views.py"
A = "taskboard/app.py"


def m(id_, f, old, new, nodes, why):
    return {"id": id_, "file": f, "old": old, "new": new, "nodes": nodes, "why": why}


CAP = [T + "::test_TC_309_the_cap_is_two_thirds_of_the_body"]
MUTANTS = [
    m("Q1", V, "    cap = max(5, 2 * (height - KANBAN_HEAD_ROWS) // 3) if height else None  # LLR-306.1",
      "    cap = None", CAP + [T + "::test_AT_304_a_board_full_of_highs_keeps_its_projects"], "no cap"),
    m("Q2", V, "            shown = lifted[:cap // 3]", "            shown = lifted[:cap // 3 + 1]", CAP,
      "one high too many: the band passes R"),
    m("Q3", V, "    cap = max(5, 2 * (height - KANBAN_HEAD_ROWS) // 3) if height else None  # LLR-306.1",
      "    cap = max(5, (height - KANBAN_HEAD_ROWS) // 2) if height else None", CAP,
      "the half-body cap (caps the approved 80x24 frame)"),
    m("Q4", V, "            if plan.overflow[i]:", "            if False:",
      [T + "::test_TC_309_the_overflow_row_sits_right_under_the_band",
       T + "::test_AT_304_a_board_full_of_highs_keeps_its_projects"], "no `+N more` row"),
    m("Q5", A, "            h = max(1, h - 2)", "            h = h",
      [T + "::test_TC_309_a_filtered_board_walks_what_it_draws"], "the nav asks the full height under a filter"),
    m("Q6", A, "                        self.selected_task_id = col[min(was[1], len(col) - 1)]",
      "                        self.selected_task_id = col[0]",
      [T + "::test_AT_308_finishing_a_card_keeps_the_cursor_on_the_board"], "the cursor to the column's top"),
    m("Q7", A, "            elif was is not None and self.selected_task_id != task.id:",
      "            elif False:",
      [T + "::test_AT_308_finishing_a_card_keeps_the_cursor_on_the_board",
       T + "::test_TC_312_the_notification_prints_a_bracket_title_literally"], "no notification"),
    m("Q8", A, '                self.notify(f"{task.title} done · counted in the ✓ rail · u undo",\n'
               "                            markup=False)",
      '                self.notify(f"{task.title} done · counted in the ✓ rail · u undo",\n'
      "                            markup=True)",
      [T + "::test_TC_312_the_notification_prints_a_bracket_title_literally"], "markup on: a bracket title parsed"),
    m("Q9", A, '        if (self.selected_task_id is not None and self.view_mode == "kanban"',
      '        if False and (self.selected_task_id is not None and self.view_mode == "kanban"',
      [T + "::test_TC_312_the_notification_prints_a_bracket_title_literally"],
      "no relocation off a counted done task (resize)"),
    m("Q10", V, '                           "grouped board; +N more ↓ when it is full",',
      '                           "grouped board.",',
      [T + "::test_TC_310_the_help_describes_the_new_board", T + "::test_AT_306_the_help_explains_what_is_drawn"],
      "the help forgets the cap"),
    m("Q11", V, '"project band, by colour"', '"project header, by colour"',
      [T + "::test_TC_310_the_help_describes_the_new_board", T + "::test_AT_306_the_help_explains_what_is_drawn"],
      "the legend keeps the old label"),
    m("Q12", V, '"▊ !! sync daemon ↗ ·3d ⛓2 +4d"', '"▊ !! sync daemon ↗ ·3d +4d ⛓2"',
      [T + "::test_TC_310_the_help_describes_the_new_board"], "the example's meta order"),
]

Path(__file__).with_name("mutants_inc002.json").write_text(
    json.dumps(MUTANTS, ensure_ascii=False, indent=1), encoding="utf-8")
# the tail, re-run after the round-1 folds (F5, F1) moved Q7's and Q9's sites
Path(__file__).with_name("mutants_inc002_tail.json").write_text(
    json.dumps(MUTANTS[8:], ensure_ascii=False, indent=1), encoding="utf-8")
print(len(MUTANTS), "mutants")

"""Writes mutants_inc001_r1.json: the code-review round-1 survivors of increment
001 (M13, and the reviewer's N1-N4, N8, N18, N19, F3), each against the node
that was added or strengthened to kill it."""
import json
from pathlib import Path

T = "tests/test_kanban_readable.py"
V = "taskboard/views.py"


def m(id_, old, new, nodes, why):
    return {"id": id_, "file": V, "old": old, "new": new, "nodes": nodes, "why": why}


MUTANTS = [
    m("M13", "    if vis(full) > w and up and down:", "    if False:",
      [T + "::test_TC_311_every_selection_is_drawn_inside_the_panel"],
      "the fold row clips its down side away (round 1: SURVIVED)"),
    m("R1", "            out.setdefault((name, p.id if p else None), (color, p, []))[2].extend(items)",
      "            out.setdefault((name, None), (color, p, []))[2].extend(items)",
      [T + "::test_TC_307_the_secondary_limbs_hold"], "groups keyed by name only (N1)"),
    m("R2", "                                sum(1 for c_ in band_cols for t in c_ if not t.archived)",
      "                                sum(1 for c_ in band_cols for t in c_)",
      [T + "::test_TC_307_the_secondary_limbs_hold"], "the open count counts archived cards (N2)"),
    m("R3", '    return c(_literal(fit(full, w)), "mut")', '    return c(fit(full, w), "mut")',
      [T + "::test_TC_311_a_hostile_name_folds_literally_and_an_exact_fit_folds_nothing"],
      "the fold row unescaped (N3)"),
    m("R4", "    room = (height - len(head) - len(pinned_rows) - 1) if height else None",
      "    room = (height - len(head) - len(pinned_rows) - 2) if height else None",
      [T + "::test_TC_311_a_hostile_name_folds_literally_and_an_exact_fit_folds_nothing"],
      "the fold one row early (N4)"),
    m("R5", "    if not board.is_done(task) and not task.archived and wc >= 9:",
      "    if not board.is_done(task) and not task.archived and wc >= 8:",
      [T + "::test_TC_307_the_secondary_limbs_hold"], "the badge from 8 cells (N8)"),
    m("R6", '    head.append(rule_row({x: "┼" for x in seps}, w))',
      '    head.append(rule_row({x: "┼" for x in seps[:-1]}, w))',
      [T + "::test_TC_307_the_secondary_limbs_hold"], "the head rule misses the rail's separator (N18)"),
    m("R7", "        age = days_in_phase(band.done[0], today)", "        age = days_in_phase(band.done[-1], today)",
      [T + "::test_TC_307_the_secondary_limbs_hold"], "the narrow rail's age from the oldest (N19)"),
    m("R8", '                         if not any(o.split(" ")[:k] == words[:k] for o in others)),',
      '                         if not any(o.startswith(" ".join(words[:k])) for o in others)),',
      [T + "::test_TC_308_tags_tell_projects_apart_and_print_literally"],
      "tags compared by characters, not words (F3)"),
]

Path(__file__).with_name("mutants_inc001_r1.json").write_text(
    json.dumps(MUTANTS, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(MUTANTS), "mutants")

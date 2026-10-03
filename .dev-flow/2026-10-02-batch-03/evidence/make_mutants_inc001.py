"""Writes mutants_inc001.json: one mutation per law increment 001 claims (C-40).
Each mutant names the nodes that must go RED. Run by `mutate.py`."""
import json
from pathlib import Path

T = "tests/test_kanban_readable.py"
V = "taskboard/views.py"


def m(id_, old, new, nodes, why):
    return {"id": id_, "file": V, "old": old, "new": new, "nodes": nodes, "why": why}


MUTANTS = [
    m("M1", "    body = _literal(text)\n", "    body = text\n",
      [T + "::test_TC_302_a_card_is_two_rows_of_exactly_its_width"],
      "title pieces printed unescaped"),
    m("M2", '    return head, " ".join(words[i:])', "    return fit(title, w), \"\"",
      [T + "::test_TC_302_the_title_wraps_on_a_word_and_the_rest_sits_under_it",
       T + "::test_AT_301_cards_read_across_the_column"],
      "no word wrap: a one-row title cut with an ellipsis"),
    m("M3", '        toks.append((f"⛓{n}", "mut"))\n    if task.archived:\n        toks.append((ARCHIVED_MARK, "ash"))\n'
            '    else:\n        dtok, dcol = reldue_token(task, today, board, include_done=True)\n'
            '        if dtok:\n            toks.append((dtok, dcol))',
      '        pass\n    if task.archived:\n        toks.append((ARCHIVED_MARK, "ash"))\n'
      '    else:\n        dtok, dcol = reldue_token(task, today, board, include_done=True)\n'
      '        if dtok:\n            toks.append((dtok, dcol))\n    if n:\n        toks.append((f"⛓{n}", "mut"))',
      [T + "::test_TC_303_the_due_token_is_the_last_fact_to_go"],
      "the dependants token after the due: the due sheds first"),
    m("M4", '            rows.append((c("┈" * wc, "frame"), None))', "            pass",
      [T + "::test_TC_304_every_row_is_the_width_and_stacked_cards_are_separated",
       T + "::test_AT_301_cards_read_across_the_column"], "no separator between stacked cards"),
    m("M5", "    k = len(desired)\n", "    k = len(desired)\n    return distribute(room, k)\n",
      [T + "::test_TC_305_the_columns_are_sized_by_their_titles",
       T + "::test_AT_301_cards_read_across_the_column"], "equal widths"),
    m("M6", '                tail[x - used - 1] = "┼"', '                tail[x - used - 2] = "┼"',
      [T + "::test_TC_306_each_project_is_named_once_by_a_band_rule"], "the rule's crossings one cell off"),
    m("M7", "    rail_titles = w >= KANBAN_WIDE and not collapsed",
      "    rail_titles = w > KANBAN_WIDE and not collapsed",
      [T + "::test_TC_307_the_rail_is_titles_when_wide_and_a_count_when_narrow"], "the 100-cell boundary off by one"),
    m("M8", "        band_done = _recent_first(done.get(key, (None, None, []))[2])",
      "        band_done = list(reversed(_recent_first(done.get(key, (None, None, []))[2])))",
      [T + "::test_TC_307_a_full_rail_counts_what_it_cannot_draw"], "the rail oldest first"),
    m("M9", "        drawn = {id(t) for t in shown}", "        drawn = set()",
      [T + "::test_TC_308_the_high_band_is_first_and_holds_exactly_the_open_highs", T],
      "highs drawn again in their project bands"),
    m("M10", "    cols = [[t.id for t in plan.high[i]] + [t.id for b in plan.bands for t in b.cols[i]]",
      "    cols = [[t.id for b in plan.bands for t in b.cols[i]] + [t.id for t in plan.high[i]]",
      [T + "::test_TC_301_nav_is_the_draw_order", T + "::test_AT_303_the_high_band_is_first_and_the_cursor_walks_it"],
      "nav walks the band last: not the draw order"),
    m("M11", "        while first > 0 and sum(len(b) for b in bands[first - 1:s + 1]) <= room:",
      "        while False:",
      [T + "::test_TC_311_a_down_into_a_drawn_band_moves_nothing",
       T + "::test_AT_307_the_selected_card_is_always_whole_on_screen"],
      "the prototype's selection-first window (re-flows on a down)"),
    m("M12", "        s = next((i for i, x in enumerate(ids) if selected_id in x), 0)", "        s = 0",
      [T + "::test_TC_311_the_board_folds_whole_bands_and_names_them",
       T + "::test_TC_311_every_selection_is_drawn_inside_the_panel"], "the window ignores the selection"),
    m("M13", "    if vis(full) > w and up and down:", "    if False:",
      [T + "::test_TC_311_every_selection_is_drawn_inside_the_panel"], "the fold row clips its down side away"),
    m("M14", '    return f"due +{n}d", "soon" if n <= 7 else "dim"', '    return f"due +{n}d", "accent" if n <= 7 else "dim"',
      [T + "::test_AT_305_the_kanban_spends_no_accent", T + "::test_TC_306_each_project_is_named_once_by_a_band_rule"],
      "the project's near due in the accent"),
    m("M15", '            rows.append((c("┈" * wc, "frame"), None))', '            rows.append((c("┈" * wc, "mut"), None))',
      [T + "::test_AT_305_the_kanban_spends_no_accent"], "separators off the frame tone"),
    m("M16", '            tag = (tags.get(p.id, p.name), p.color) if p else ("Inbox", "dim")', "            tag = None",
      [T + "::test_TC_308_the_high_band_is_first_and_holds_exactly_the_open_highs",
       T + "::test_TC_308_tags_tell_projects_apart_and_print_literally"], "no project tag on high cards"),
    m("M17", '                         if not any(o.split(" ")[:k] == words[:k] for o in others)),',
      "                         if True),",
      [T + "::test_TC_308_tags_tell_projects_apart_and_print_literally"], "first word always (API / API)"),
    m("M18", "    if rest and keep < 2:", "    if False:",
      [T + "::test_TC_303_the_due_token_is_the_last_fact_to_go"], "the rest kept with no room: the due sheds"),
    m("M19", "                                          n=n_open))", "                                          ))",
      [T + "::test_TC_313_the_chrome_names_the_modes_and_counts_hidden_phases"], "window markers count the rail's phase"),
    m("M20", "                                + n_high, n_high))", "                                + 0, n_high))",
      [T + "::test_TC_306_each_project_is_named_once_by_a_band_rule"], "the open count drops the lifted highs"),
]

Path(__file__).with_name("mutants_inc001.json").write_text(
    json.dumps(MUTANTS, ensure_ascii=False, indent=1), encoding="utf-8")
# the tail of the battery, re-run after the round-1 fold moved M17's site (F3)
Path(__file__).with_name("mutants_inc001_tail.json").write_text(
    json.dumps(MUTANTS[16:], ensure_ascii=False, indent=1), encoding="utf-8")
print(len(MUTANTS), "mutants")

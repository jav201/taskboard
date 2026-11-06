# Test cases — Inc MR-a: the board gantt's shared milestone row

Base `154e260`; tree `5d2c880` (E5 corrective). One case covers each active HLR and LLR (50). Every node below was checked with `env -u NO_COLOR python -m pytest --collect-only -q` (60 test functions in the two files; parametrized arms count as one node). Results are from `evidence/green-3.txt` (341 passed, 0 failed). Generated from `01-requirements.md` (statements, thresholds, AT citations) and the collected node names; the `full`/`partial` marks are the author's and still owe the independent re-check (E5).

Node prefixes: `M` = `tests/test_milestone_row.py`, `A` = `tests/test_milestone_row_at.py`.

Marks: a TC node goes through the shipped seat (`render_gantt`, `nav_model`, or the real app by keys) and asserts the threshold's values, so it is `full`. An AT node is `partial` for each LLR it cites (it checks a subset of the threshold) and for its HLR.

## HLR-4601 — one milestone row per group

### HLR-4601/1
- **Objective:** Verify that the system draws a group's drawn milestones on one milestone row of the board gantt.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4601.n thresholds; fixture MR-F at 118x30 draws 18 body rows (base 23).
- **Tests:** `A::test_AT_4601_the_row_at_rest` (partial); `A::test_AT_4602_folding` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

## HLR-4602 — the marks on the row

### HLR-4602/1
- **Objective:** Verify that the system draws each drawn milestone on its row as its class mark at its date.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4602.n thresholds.
- **Tests:** `A::test_AT_4601_the_row_at_rest` (partial); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

## HLR-4603 — the row's labels, label column and chip

### HLR-4603/1
- **Objective:** Verify that the system labels the milestone row with the selected milestone's title and the other milestones' dates where they fit.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4603.n thresholds.
- **Tests:** `A::test_AT_4601_the_row_at_rest` (partial); `A::test_AT_4603_onto_the_row_and_along_it` (partial); `A::test_AT_4607_edges` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

## HLR-4604 — `↑↓` stop on the row once, `←→` walk it

### HLR-4604/1
- **Objective:** Verify that when the cursor is on a milestone row, the system lets `←` and `→` select its milestones in walk order.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** the cursor is on a milestone row.
- **Expected result:** all LLR-4604.n thresholds.
- **Tests:** `A::test_AT_4603_onto_the_row_and_along_it` (partial); `A::test_AT_4604_acting_on_the_walked_one` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

## HLR-4605 — search and hidden classes reach single milestones (D3)

### HLR-4605/1
- **Objective:** Verify that the system draws on the milestone row only the milestones the `/` query and the class filter leave visible.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4605.n thresholds.
- **Tests:** `A::test_AT_4605_search_and_hidden_classes` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

## HLR-4606.1 — the link mode keeps one row per milestone (MR-2, R-3)

### HLR-4606.1/1
- **Objective:** Verify that while the link mode is open, the system draws each milestone on its own row.
- **Class:** normal.
- **Preconditions:** the link mode is open.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all thresholds of LLR-4606.1, LLR-4606.2, LLR-4606.3.
- **Tests:** `A::test_AT_4606_link_mode_and_pages` (partial); `A::test_AT_4606b_a_paged_group_pages_to_its_row` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

## HLR-4606.2 — the milestone row is one row of the board gantt's pages (MR-2)

### HLR-4606.2/1
- **Objective:** Verify that the system counts the milestone row as one row of the board gantt's pages.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all thresholds of LLR-4606.4, LLR-4606.5.
- **Tests:** `A::test_AT_4606_link_mode_and_pages` (partial); `A::test_AT_4606b_a_paged_group_pages_to_its_row` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

### LLR-4601.1/1
- **Objective:** Verify that the board gantt draws, for every unfolded group with one or more drawn milestones, exactly one milestone row directly under the group's span row.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** fixture MR-F at 118x30 → 4 milestone rows, each the line after its span row; no other line holds a milestone mark in the body; 4/4.
- **Tests:** `M::test_TC_4801_LLR_4601_1_one_milestone_row_right_under_each_span_row` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.2/1
- **Objective:** Verify that the milestone row holds exactly the group's drawn milestones.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** per group of MR-F, the set of ids on the row = the milestone ids base `gantt_plan` puts in that group's rows (Pilot rollout 5, incl. reached m1; Eval harness 2; Docs 1; Inbox 1); a group with only reached milestones and no open work → no row (D-606); 5/5.
- **Tests:** `M::test_TC_4802_LLR_4601_2_the_row_holds_exactly_the_groups_drawn_milestones` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.3/1
- **Objective:** Verify that the board gantt draws a group's non-milestone tasks one per row, in the order base draws them, under its milestone row.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** per group of MR-F plus a done, not-archived task → the task ids in line order equal base's non-milestone ids in line order, the done one last; 4/4.
- **Tests:** `M::test_TC_4803_LLR_4601_3_tasks_one_per_row_in_base_order_under_the_row` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.4/1
- **Objective:** Verify that the board gantt draws the Inbox group's milestones on the Inbox group's own milestone row.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F → i1 on the line after the `Inbox` span row, 0 Inbox milestones on any project's row; 1/1.
- **Tests:** `M::test_TC_4804_LLR_4601_4_the_inbox_has_its_own_row` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.5/1
- **Objective:** Verify that if none of a group's milestones is drawn, then the board gantt draws no milestone row for that group.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** none of a group's milestones is drawn.
- **Expected result:** a group with no milestone; a group whose every milestone is archived; a group whose only milestones are reached and which has no open work → 0 milestone rows, line count = span + tasks; 3/3.
- **Tests:** `M::test_TC_4805_LLR_4601_5_no_drawn_milestone_no_row` (full); `A::test_AT_4602_folding` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.6/1
- **Objective:** Verify that while a group is folded, the board gantt draws no milestone row for it.
- **Class:** normal (State).
- **Preconditions:** a group is folded. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F at 118x12 → each folded group's span row is followed by the next span row; 1/1 per folded group, ≥ 1 folded.
- **Tests:** `M::test_TC_4806_LLR_4601_6_a_folded_group_draws_no_row` (full); `A::test_AT_4602_folding` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.7/1
- **Objective:** Verify that the board gantt counts a group's milestone row as one row when it decides which groups unfold.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F at 80x24 → 0 folded groups (base folds ≥ 1); MR-F at 118x30 → 0 folded and 18 body rows; 2/2.
- **Tests:** `M::test_TC_4807_LLR_4601_7_the_row_costs_one_row_of_the_fold_budget` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4601.8/1
- **Objective:** Verify that the milestone row's dependency gutter is blank.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F with m3 waiting on the open task `store` → the gutter cell of each of the 4 milestone rows is blank; no `waits` or `early` entry of the frame's `drawn` comes from a milestone row (base adds `waits` for m3's row); 4/4.
- **Tests:** `M::test_TC_4808_LLR_4601_8_the_rows_dependency_gutter_is_blank` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.1/1
- **Objective:** Verify that the milestone row draws each drawn milestone whose due lies inside the field's window as its `<glyph>` in its class style, in its cell.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F, nothing selected on the row → g1 `▲` cyan, g2 `■` violet, h1 `◆` in `mut` (the seat, `milestone_mark`), i1 `⬢` amber, each at `ax.cell(due)`; 4/4.
- **Tests:** `M::test_TC_4811_LLR_4602_1_each_mark_is_its_class_glyph_in_its_class_style` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.2/1
- **Objective:** Verify that the milestone row draws two to nine milestones sharing one cell as one `<glyph>` followed by the digit of their count, the glyph being the selected one's among them, else the first's in walk order.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m3 + m4 (Oct 24) → `■2` (m3 first by title `Steering…` vs `Store…`); with m4 selected → `▲2`; 2/2.
- **Tests:** `M::test_TC_4812_LLR_4602_2_a_shared_cell_is_one_glyph_and_its_count` (full); `A::test_AT_4601_the_row_at_rest` (partial); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.3/1
- **Objective:** Verify that if ten or more milestones share one cell, then the milestone row draws them as one `<glyph>` followed by `+`.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** ten or more milestones share one cell.
- **Expected result:** 10 milestones on one day → `<glyph>+`, 0 cells right of it overwritten beyond 2; 1/1.
- **Tests:** `M::test_TC_4813_LLR_4602_3_ten_or_more_in_one_cell_is_glyph_plus` (full); `A::test_AT_4607_edges` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.4/1
- **Objective:** Verify that the milestone row draws a reached milestone alone in its cell as `<hollow>` followed by `✓` in the reached style.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m1 (Payment) → `⬡✓`; 1/1.
- **Tests:** `M::test_TC_4814_LLR_4602_4_a_reached_milestone_alone_is_hollow_and_tick` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.5/1
- **Objective:** Verify that the milestone row draws the selected milestone's mark in reverse video.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m2 selected → its cell's style has `reverse`; every other mark's style lacks it; 2/2.
- **Tests:** `M::test_TC_4815_LLR_4602_5_the_selected_mark_is_reverse_video` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.6/1
- **Objective:** Verify that if a drawn milestone's due lies before or after the field's window, then the milestone row draws `◂` (before) or `▸` (after) in the field's edge cell on that side and its mark in the cells next inward.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a drawn milestone's due lies before or after the field's window.
- **Expected result:** a reached milestone 40 days back (before `ctx`, the earliest open start); a reached milestone due 90 days ahead (done early), in a group with open work → `◂<hollow>✓` at cells 0–2 and `<hollow>✓▸` at the last three; two reached milestones after the window share the drawn cell → `<glyph>2▸`; 3/3.
- **Tests:** `M::test_TC_4816_LLR_4602_6_off_window_dues_draw_the_edge_glyph_and_the_mark_inward` (full); `A::test_AT_4607_edges` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.7/1
- **Objective:** Verify that if a drawn milestone has no due date, then the milestone row draws no mark for it.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a drawn milestone has no due date.
- **Expected result:** a milestone with `due_date None` on a row with one dated one → 1 mark in the field; 1/1; 0 exceptions.
- **Tests:** `M::test_TC_4817_LLR_4602_7_no_due_draws_no_mark` (full); `A::test_AT_4607_edges` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4602.8/1
- **Objective:** Verify that if a two-cell mark (`<glyph>N`, `<glyph>+` or `<hollow>✓`) falls in the field's last cell, then the milestone row starts that mark in the cell before it.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a two-cell mark (`<glyph>N`, `<glyph>+` or `<hollow>✓`) falls in the field's last cell.
- **Expected result:** through `render_gantt`, a reached milestone alone with its due on the window's last day; two reached ones sharing that cell → `<hollow>✓` and `<glyph>2` at cells `w-2`–`w-1`; the row is exactly `w` cells; 0 exceptions; 2/2.
- **Tests:** `M::test_TC_4818_LLR_4602_8_a_two_cell_mark_in_the_last_cell_starts_one_before` (full).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.1/1
- **Objective:** Verify that the milestone row draws the selected milestone's full title after its mark, past one blank cell, when the cells up to the next mark leave room for the whole title, else before its mark when the room there does.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** 118x30, m5 selected → `Pilot launch` follows `★ `; a reached milestone due on the field's last day selected → its title ends one cell before `⬡✓`; 2/2.
- **Tests:** `M::test_TC_4821_LLR_4603_1_the_selected_title_after_its_mark_else_before` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.2/1
- **Objective:** Verify that if neither side of the selected milestone's mark has room for its whole title, then the milestone row draws the title cut with `…` on the side with more room when that side has 6 cells or more, and no title in the field otherwise.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** neither side of the selected milestone's mark has room for its whole title.
- **Expected result:** 118x30, m2 selected → `Rubric…` between m2 and m3; a cramped row (marks 4 cells apart) → no title cells; 2/2.
- **Tests:** `M::test_TC_4822_LLR_4603_2_no_room_cuts_on_the_roomier_side_from_6_cells` (full).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.3/1
- **Objective:** Verify that the milestone row draws, beside each mark that holds no selected milestone and whose lead is not late, the lead's date `Mon D`, past one blank cell, only where the whole date fits without touching another mark or label.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** 118x30, nothing on Pilot rollout's row selected → `Oct 24` (beside `■2`: its lead m3's date), `Oct 30` beside their marks; g1 `Oct 21`, g2 `Oct 28`; 4/4.
- **Tests:** `M::test_TC_4823_LLR_4603_3_other_marks_carry_their_leads_whole_date_where_it_fits` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.4/1
- **Objective:** Verify that the milestone row draws, beside a mark whose lead is late, the lead's `▲Nd` in the over style in place of its date.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m2 not selected → `▲1d` beside its mark, `Oct 19` 0 occurrences on the row; 1/1.
- **Tests:** `M::test_TC_4824_LLR_4603_4_a_late_lead_shows_its_days_late_in_over` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.5/1
- **Objective:** Verify that the milestone row draws no label over a mark, over another label, or past the field's edges.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** every row of AT-4601..AT-4603 scenes at 118 and 80 → every mark cell still holds its mark, labels disjoint; 10/10 frames.
- **Tests:** `M::test_TC_4825_LLR_4603_5_no_label_covers_a_mark_or_the_edge` (full).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.6/1
- **Objective:** Verify that while no milestone of a row is selected, the row's label column reads `◆ <N> milestones` (`milestone` when N = 1) at a label width of 24 cells or more and `◆ <N> ms` below, followed by ` ▲<L>` in the over style when L ≥ 1 of them are late.
- **Class:** normal (State).
- **Preconditions:** no milestone of a row is selected. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** 118 → `◆ 2 milestones`, `◆ 1 milestone`; 80 → `◆ 5 ms ▲1`; 3/3.
- **Tests:** `M::test_TC_4826_LLR_4603_6_the_label_column_at_rest` (full); `A::test_AT_4601_the_row_at_rest` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.7/1
- **Objective:** Verify that while a milestone of a row is selected, the row's label column reads its `<glyph>`, its title cut to the column, and ` <i>/<N>` when it is the i-th of N milestones in its cell.
- **Class:** normal (State).
- **Preconditions:** a milestone of a row is selected. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m2 → `■ Rubric sign-off`; m4 → `▲ Store list frozen 2/2` (cut at 80, the `2/2` kept); 2/2.
- **Tests:** `M::test_TC_4827_LLR_4603_7_the_label_column_names_the_selected_member` (full); `M::test_TC_4827b_R6_i_of_n_counts_the_cell_not_the_day` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.8/1
- **Objective:** Verify that the milestone row's chip is the selected milestone's `gantt_milestone_chip`, else the anchor's when it is open with a due on or after today, else blank.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m2 selected → `▲1d`; nothing selected on Pilot rollout → `in 4d` (m3); a row whose only milestones are late → blank; 3/3.
- **Tests:** `M::test_TC_4828_LLR_4603_8_the_chip_is_the_selected_else_the_upcoming_anchor` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.9/1
- **Objective:** Verify that the board gantt draws no line wider than the terminal.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** every frame of AT-4601..AT-4607 at 118x30 and 80x24 → max `cell_len` per line ≤ width; 14/14.
- **Tests:** `M::test_TC_4829_LLR_4603_9_no_line_wider_than_the_terminal` (full); `A::test_AT_4601_the_row_at_rest` (partial); `A::test_AT_4607_edges` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.10/1
- **Objective:** Verify that the board gantt's legend names the milestone mark and the reached mark whenever a milestone row draws them.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F at 118x30 → the legend holds `◆ milestone`; with m1 drawn it holds the reached entry as base does; 2/2.
- **Tests:** `M::test_TC_4830_LLR_4603_10_the_legend_names_the_rows_marks` (full).
- **Coverage:** covered. **Result:** verified.

### LLR-4603.11/1
- **Objective:** Verify that if a label that the milestone row draws in the field holds markup brackets, a backslash, or characters wider or narrower than one cell, then the milestone row draws the label's literal text, measured and cut in cells, within the field's width.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a label that the milestone row draws in the field holds markup brackets, a backslash, or characters wider or narrower than one cell.
- **Expected result:** the selected milestone's title set in turn to `a]b[/]`, `[@click=app.quit]x`, `x\`, a wide-glyph title `里程碑 frozen` and a combining-mark title (`e` + U+0301 + `tape`), each drawn after its mark, before it, and cut with `…` → 0 exceptions; the row's `plain` holds the exact title or its `fit` cut ending in `…`; no span carries `@click` or any meta; every line's `cell_len` equals the frame width; 15/15.
- **Tests:** `M::test_TC_4820_LLR_4603_11_a_field_label_draws_its_literal_text_in_cells` (full); `M::test_TC_4820b_SEC6_a_zero_cell_title_draws_nothing_and_keeps_the_width` (full); `M::test_TC_4820c_N9_a_label_run_takes_no_weekend_ground` (full).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.1/1
- **Objective:** Verify that the board gantt's `↑↓` order holds, per group, the milestone row as one stop followed by the group's task rows in line order.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F, the cursor on `Pilot store list`, `↑` → a milestone of Pilot rollout; `↑` again → no move (Pilot rollout is the first group); `↓`×2 from the row → `Pilot telemetry`; 3/3.
- **Tests:** `M::test_TC_4831_LLR_4604_1_up_down_stop_on_the_row_once` (full); `M::test_TC_4831b_LLR_4604_1_the_nav_column_holds_one_stop_per_row` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.2/1
- **Objective:** Verify that when `↑` or `↓` moves the cursor onto a milestone row, the system selects the row's anchor.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `↑` or `↓` moves the cursor onto a milestone row.
- **Expected result:** Pilot rollout → m3 (m1 reached, m2 late); a row of only late ones → the first late one; a row of only reached ones → the first; 3/3.
- **Tests:** `M::test_TC_4832_LLR_4604_2_landing_on_a_row_selects_its_anchor` (full); `M::test_TC_4832b_LLR_4604_2_up_lands_on_the_anchor` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.3/1
- **Objective:** Verify that when `→` is pressed while a milestone of a row is selected, the system selects the next milestone of that row in walk order.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `→` is pressed while a milestone of a row is selected.
- **Expected result:** m3 → m4 (same day) → m5; 2/2.
- **Tests:** `M::test_TC_4833_LLR_4604_3_right_walks_to_the_next_in_walk_order` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.4/1
- **Objective:** Verify that when `←` is pressed while a milestone of a row is selected, the system selects the previous milestone of that row in walk order.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `←` is pressed while a milestone of a row is selected.
- **Expected result:** m3 → m2 → m1; 2/2.
- **Tests:** `M::test_TC_4834_LLR_4604_4_left_walks_back` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.5/1
- **Objective:** Verify that if `←` is pressed on a row's first milestone or `→` on its last, then the system keeps the selection unchanged.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `←` is pressed on a row's first milestone or `→` on its last.
- **Expected result:** m1 + `←` → m1; m5 + `→` → m5; 0 exceptions, no other group's milestone selected; 2/2.
- **Tests:** `M::test_TC_4835_LLR_4604_5_the_ends_keep_the_selection` (full); `A::test_AT_4603_onto_the_row_and_along_it` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.6/1
- **Objective:** Verify that while the selection is not a milestone of a board gantt milestone row, `←` and `→` changes the selection exactly as at base.
- **Class:** normal (State).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** gantt with a task selected → unchanged by `←`/`→`; kanban `←`/`→` → base column jumps; no selection in the gantt → base `_select_first`; 3/3.
- **Tests:** `M::test_TC_4836_LLR_4604_6_off_the_row_left_right_are_base` (full); `A::test_AT_4604_acting_on_the_walked_one` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.7/1
- **Objective:** Verify that when `enter` is pressed while a milestone of a row is selected, the system opens the details of that milestone.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `enter` is pressed while a milestone of a row is selected.
- **Expected result:** m3, `→`, `enter` → `TaskDetails` of m4; 1/1.
- **Tests:** `M::test_TC_4837_LLR_4604_7_enter_opens_the_walked_milestone` (full); `A::test_AT_4604_acting_on_the_walked_one` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4604.8/1
- **Objective:** Verify that a task key pressed while a milestone of a row is selected acts on that milestone.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** m3, `→`, `]` → m4's phase moves one forward, m3's unchanged; `e` → the editor holds m4's title; 2/2.
- **Tests:** `M::test_TC_4838_LLR_4604_8_task_keys_act_on_the_walked_milestone` (full); `A::test_AT_4604_acting_on_the_walked_one` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4605.1/1
- **Objective:** Verify that while a `/` query is set, the milestone row draws only the milestones the query matches.
- **Class:** normal (State).
- **Preconditions:** a `/` query is set. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** `/store` `enter` → Pilot rollout's row draws only m4, `◆ 1 milestone` / its title; the other groups draw no row; 2/2.
- **Tests:** `M::test_TC_4841_LLR_4605_1_a_query_keeps_only_the_matching_milestones_on_the_row` (full); `A::test_AT_4605_search_and_hidden_classes` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4605.2/1
- **Objective:** Verify that if a milestone's class is hidden, then the milestone row does not draw it.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a milestone's class is hidden.
- **Expected result:** class Review hidden in `#` → Pilot rollout's row draws m1, m4, m5; m4's cell `▲` with no count; 2/2.
- **Tests:** `M::test_TC_4842_LLR_4605_2_a_hidden_class_leaves_the_row` (full); `A::test_AT_4605_search_and_hidden_classes` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4605.3/1
- **Objective:** Verify that if a milestone is not drawn on its row (a `/` query does not match it, or its class is hidden), then the system leaves it out of the `←→` walk.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a milestone is not drawn on its row (a `/` query does not match it, or its class is hidden).
- **Expected result:** Review hidden, m1 selected, `→`, `→` → m4, m5; `/store` + `←`/`→` → m4 stays; 2/2.
- **Tests:** `M::test_TC_4843_LLR_4605_3_the_walk_skips_what_the_row_does_not_draw` (full); `M::test_TC_4843b_R4_the_cursor_never_stops_on_a_hidden_class_milestone` (full); `M::test_TC_4843b_R4_the_nav_column_holds_no_hidden_class_milestone` (full); `M::test_TC_4843c_R4_the_stop_is_the_one_the_frame_draws` (full); `M::test_TC_4843d_A5_hiding_the_selected_milestones_class` (full); `A::test_AT_4605_search_and_hidden_classes` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4606.1/1
- **Objective:** Verify that while the link mode is open, the system draws each milestone on its own row.
- **Class:** normal (State).
- **Preconditions:** the link mode is open. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** MR-F, a task selected, `L` → the link frame draws m1..m5 on 5 rows (reached m1 kept while the group has open work, as base), each named in `line_map`; byte-equal to base's link frame; 1/1.
- **Tests:** `M::test_TC_4851_LLR_4606_1_the_link_frame_keeps_one_row_per_milestone` (full); `A::test_AT_4606_link_mode_and_pages` (partial); `A::test_AT_4606b_a_paged_group_pages_to_its_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4606.2/1
- **Objective:** Verify that when `L` is pressed while a milestone of a row is selected, the system opens the link mode with that milestone as the waiting task.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `L` is pressed while a milestone of a row is selected.
- **Expected result:** m3, `→` (m4), `L` → the link frame's waiter is m4; 1/1.
- **Tests:** `M::test_TC_4852_LLR_4606_2_L_on_a_walked_milestone_makes_it_the_waiter` (full); `A::test_AT_4606_link_mode_and_pages` (partial); `A::test_AT_4606b_a_paged_group_pages_to_its_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4606.3/1
- **Objective:** Verify that when the link mode closes, the system draws the board gantt's milestone rows again.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the link mode closes.
- **Expected result:** `L`, `esc` → the frame equals the frame before `L`; `L`, a candidate, `enter` → 4 milestone rows again; 2/2.
- **Tests:** `M::test_TC_4853_LLR_4606_3_closing_the_link_mode_brings_the_rows_back` (full); `A::test_AT_4606_link_mode_and_pages` (partial); `A::test_AT_4606b_a_paged_group_pages_to_its_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4606.4/1
- **Objective:** Verify that when a milestone of a paged group is selected, the board gantt draws the page that holds the group's milestone row.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a milestone of a paged group is selected.
- **Expected result:** a group of 1 milestone row + 20 tasks at 118x14, the cursor on the last task, `↑` until the row → the page shows the row and `▼ <n> below`, the count of task rows off the page; 2/2.
- **Tests:** `M::test_TC_4854_LLR_4606_4_a_selected_member_selects_the_page_holding_the_row` (full); `A::test_AT_4606_link_mode_and_pages` (partial); `A::test_AT_4606b_a_paged_group_pages_to_its_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4606.5/1
- **Objective:** Verify that while the body holds only the span rows and the selected row, the board gantt draws the selected milestone's milestone row as the selected row.
- **Class:** normal (State).
- **Preconditions:** the body holds only the span rows and the selected row. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** The board and selection the threshold names.
- **Expected result:** groups = body rows (D8) and body ≤ 2, a milestone selected → the row drawn is the milestone row (its mark reverse, its label `<glyph> <title>`); 2/2.
- **Tests:** `M::test_TC_4855_LLR_4606_5_only_spans_and_the_selection_draws_the_row` (full).
- **Coverage:** covered. **Result:** verified.

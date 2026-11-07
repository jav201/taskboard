# Test cases — Inc MR-b: the presentation's milestones share one row

Base `8ca174c`; tree = the E5 corrective commit. One case covers each active HLR and LLR (4 + 25 = 29). Every node below was checked with `env -u NO_COLOR python -m pytest --collect-only -q` (37 test functions, 115 collected items, in the two files; parametrized arms count as one node). Results are from `evidence/green-3.txt` (435 passed, 0 failed). Generated from `01-requirements.md` (statements, thresholds, AT citations) and the collected node names; the `full`/`partial` marks are the author's and still owe the independent re-check (E5).

Node prefixes: `P` = `tests/test_present_milestone_row.py`, `A` = `tests/test_present_milestone_row_at.py`. TC numbering (head of `01-requirements.md`): LLR-4651.n → TC-49(0n), LLR-4652.n → TC-49(1n), LLR-4652.10 → TC-4920, LLR-4653.n → TC-49(2n), LLR-4654.n → TC-49(3n).

Marks: a TC node goes through the shipped seat (`render_present`, `render_present_all`, `present_deck_boards`, or the real app by keys) and asserts the threshold's values, so it is `full`. An AT node is `partial` for each LLR it cites (it checks a subset of the threshold) and for its HLR.

## HLR-4651 — one milestone row per project in `R`

### HLR-4651/1
- **Objective:** Verify that the system draws a presented project's drawn milestones on one milestone row of the presentation's field.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4651.n thresholds; MR-F's *Pilot rollout* in view 1 at 118x30 draws 5 field body rows (base 8).
- **Tests:** `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4652_view_2_the_same_field_and_blocks_in_stop_order` (partial); `A::test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

### LLR-4651.1/1
- **Objective:** Verify that views 1 and 2 draw, for a presented project with one or more drawn milestones, exactly one milestone row directly under the project's span row.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** MR-F *Pilot rollout*, views 1 and 2 at 118x30 → the field line after the span row holds m2..m5's marks; no other field line holds a milestone mark; 2/2. *NC:* row after the last task: RED. (carries LLR-4601.1)
- **Tests:** `P::test_TC_4901_LLR_4651_1_one_milestone_row_directly_under_the_span` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4652_view_2_the_same_field_and_blocks_in_stop_order` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.2/1
- **Objective:** Verify that view 3 draws, for every unfolded shown project with one or more drawn milestones, exactly one milestone row directly under the project's head row.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** MR-F, `3`, 118x30 → 3 milestone rows (Pilot rollout, Eval harness, Docs & handover), each the line after its head; 3/3. *NC:* no row in view 3 (per-task rows kept): RED.
- **Tests:** `P::test_TC_4902_LLR_4651_2_view_3_one_row_under_each_head` (full); `A::test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.3/1
- **Objective:** Verify that the presentation's milestone row holds exactly the project's drawn milestones.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** Pilot rollout → {m2, m3, m4, m5} (m1 reached: absent as at base); class Review hidden in `#` → {m4, m5}; m3 hidden with `space` → {m2, m4, m5}; views 1 and 3; 6/6. *NC:* include the reached m1: RED. (carries LLR-4601.2, LLR-4605.2)
- **Tests:** `P::test_TC_4903_LLR_4651_3_the_row_holds_exactly_the_drawn_milestones` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4654_hiding_milestones_from_the_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.4/1
- **Objective:** Verify that the presentation draws a project's open shown non-milestone tasks one per field row, in their base order, under its milestone row.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** Pilot rollout's 4 tasks in base field order under the row, views 1, 2, 3; 3/3. *NC:* sort by title: RED. (carries LLR-4601.3)
- **Tests:** `P::test_TC_4904_LLR_4651_4_tasks_one_per_row_in_base_order_under_the_row` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.5/1
- **Objective:** Verify that if a presented project has no drawn milestone, then the presentation draws no milestone row for it.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a presented project has no drawn milestone.
- **Expected result:** *Docs & handover* with h1 hidden by `space` → view 1 field = span + 2 task rows; view 3 likewise; a project with no milestone; 3/3. *NC:* always emit the row: RED. (carries LLR-4601.5)
- **Tests:** `P::test_TC_4905_LLR_4651_5_no_drawn_milestone_no_row` (full); `A::test_AT_4654_hiding_milestones_from_the_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.6/1
- **Objective:** Verify that while a project is folded in view 3, by `enter` or by the overflow rule, view 3 draws no milestone row for it.
- **Class:** normal (State).
- **Preconditions:** a project is folded in view 3, by `enter` or by the overflow rule. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** `enter` on *Eval harness*'s head → its head followed by the next head; 80x14 overflow-folded project likewise; 2/2. *NC:* draw the row under a folded head: RED. (carries LLR-4601.6)
- **Tests:** `P::test_TC_4906_LLR_4651_6_a_folded_project_draws_no_row` (full); `A::test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.7/1
- **Objective:** Verify that view 3 counts a project's milestone row as one row when it decides which projects the overflow rule folds.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** MR-F at 118x18 → base folds ≥ 1 project, new folds fewer; the layout's row count = heads + milestone rows + task rows; 2/2. *NC:* count one row per milestone in `need`: RED. (carries LLR-4601.7)
- **Tests:** `P::test_TC_4907_LLR_4651_7_the_row_counts_as_one_row_for_the_overflow` (full); `A::test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4651.8/1
- **Objective:** Verify that the presentation's milestone row draws a blank in its dependency gutter.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** MR-F, m3 waiting on the open task `store`; views 1 and 3 at 118x30 and 80x24, the cursor on m3 → the milestone row's gutter cell (the cell after the present label column) is a blank, and no line of the frame shows the `↳` base draws in m3's own row's gutter; 4/4. *NC:* draw the cursor milestone's `gantt_dep_mark` in the gutter: RED. (carries LLR-4601.8; RB-5)
- **Tests:** `P::test_TC_4908_LLR_4651_8_the_rows_dependency_gutter_is_blank` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

## HLR-4652 — the row looks as MR-a's row does

### HLR-4652/1
- **Objective:** Verify that the system draws the presentation's milestone row with the board gantt's milestone-row marks and labels.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4652.n thresholds.
- **Tests:** `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4655_hostile_titles_stay_literal_at_80x24` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

### LLR-4652.1/1
- **Objective:** Verify that the presentation's milestone row draws, in its field, the cells the board gantt's milestone row draws for the same milestones, axis, day and selection, the selection being the cursor milestone, else none.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** views 1 and 3 at 118 and 80, cursor on m3, on m4, on a task → field cells equal `gantt_milestone_row(lane, sel, board, ax, today)` painted over the presentation's field ground; `■2`, `▲2`, `▲1d`, `Oct 30` present as LLR-4602.2 and LLR-4603.3/.4 say; 8/8. *NC:* select the anchor instead of the cursor milestone: RED. (carries LLR-4602.1–4602.8, LLR-4603.1–4603.5)
- **Tests:** `P::test_TC_4911_LLR_4652_1_the_field_is_the_board_gantts_row` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.2/1
- **Objective:** Verify that the presentation's field paints a reversed mark and a covered label cell the way the board gantt's field paints them.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** the cursor on m2 → its cell is reverse video in its class style; a title run covers its cells once, no doubled glyph, no stray tone name; 2/2. *NC:* `_present_field` unchanged (reads `rev:…` as a style name): RED.
- **Tests:** `P::test_TC_4912_LLR_4652_2_a_reversed_mark_and_a_covered_label_paint_once` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.3/1
- **Objective:** Verify that while the cursor is not on one of a row's milestones, the row's present label column reads the project's hue bar `▎` followed by the text LLR-4603.6 gives.
- **Class:** normal (State).
- **Preconditions:** the cursor is not on one of the row's milestones. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** view 1 on a task → `▎ ◆ 4 milestones ▲1` at 118 and `▎ ◆ 4 ms ▲1` at 80; 2/2. *NC:* drop the late count: RED. (carries LLR-4603.6)
- **Tests:** `P::test_TC_4913_LLR_4652_3_the_label_at_rest` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.4/1
- **Objective:** Verify that while the cursor is on one of a row's milestones, the row's present label column reads `⟦`, the hue bar `▎` and the text LLR-4603.7 gives for that milestone.
- **Class:** normal (State).
- **Preconditions:** the cursor is on one of the row's milestones. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** cursor m4 → ` ⟦▎ ▲ Store list frozen   2/2` at 118 and ` ⟦▎ ▲ Store li… 2/2` at 80 (cut by cell width with `…`, tag kept); cursor m2 → ` ⟦▎ ■ Rubric sign-off` at 118 and ` ⟦▎ ■ Rubric sign-…` at 80; 4/4. *NC:* the lead `⟦` absent: RED. (carries LLR-4603.7; the R-7 cut at every width, RB-3)
- **Tests:** `P::test_TC_4914_LLR_4652_4_the_label_on_a_milestone` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.5/1
- **Objective:** Verify that the presentation's milestone row's chip is the chip base draws for the cursor milestone's row, else for the first drawn milestone in walk order with a due on or after today, else blank.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** cursor m2 → m2's base chip; cursor on a task → m3's base chip; a row of only late ones, cursor elsewhere → 13 blanks; 3/3. *NC:* the first milestone's chip (m2's) with the cursor elsewhere: RED. (carries LLR-4603.8)
- **Tests:** `P::test_TC_4915_LLR_4652_5_the_rows_chip` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.6/1
- **Objective:** Verify that if a milestone's title on the presentation's milestone row holds markup brackets, a backslash or characters wider or narrower than one cell, then the presentation draws it as literal text within the row's cells and raise no exception.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a milestone's title on the presentation's milestone row holds markup brackets, a backslash or characters wider or narrower than one cell.
- **Expected result:** titles `a]b[/]`, `[@click=app.quit]x`, `\`, `日本語のタイトル` each as the cursor milestone, views 1 and 3 → the plain text holds the title (or its `…` cut) literally, line `cell_len` = width, 0 exceptions, 0 live tags; 8/8. *NC:* build the label column with `c(title)` unescaped: RED. (carries LLR-4603.11, R-7)
- **Tests:** `P::test_TC_4916_LLR_4652_6_hostile_milestone_titles_are_literal` (full); `A::test_AT_4655_hostile_titles_stay_literal_at_80x24` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.7/1
- **Objective:** Verify that the presentation draws no line wider than the terminal.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** views 1, 2, 3 × {118x30, 100x30, 80x24} on MR-F, the cursor on m3 → max `cell_len` per line ≤ width; 9/9. *NC:* pass the board gantt's label width (30 at 80): RED. (carries LLR-4603.9)
- **Tests:** `P::test_TC_4917_LLR_4652_7_no_line_wider_than_the_terminal` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.8/1
- **Objective:** Verify that the presentation draws its header, ruler rows, legend strip and hint row as at base.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** views 1, 2, 3 × {118x30, 80x24} on MR-F → those rows' plain text equal base's; 6/6. *NC:* count the milestone row in the header's open count: RED.
- **Tests:** `P::test_TC_4918_LLR_4652_8_header_ruler_and_strip_as_at_base` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4655_the_hint_row_is_base` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.9/1
- **Objective:** Verify that if a presented task's title holds a backslash, then view 1 draws the title in its brief line as literal text, each backslash once, within the terminal's width.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a presented task's title holds a backslash.
- **Expected result:** titles `\`, `x\`, `\[x` and `a\[b]`, each the cursor task, view 1 at 118x30 and 80x24 → measured on the rendered frame (`cell_len` of each line of `render_present(…).plain`, after `to_text`; never `_strip` of the markup, SEC-B2): the brief holds `⟦\⟧`, `⟦x\⟧`, `⟦\[x⟧`, `⟦a\[b]⟧` (or the `…` cut) literally, and every line is exactly the width; 8/8. RED on base: `\` and `x\` give a 119 / 81-cell line reading `\\`, and `\[x` reads `[x`; `a\[b]` already reads `a\[b]` on base (rich's `escape` escapes the tag-shaped `[b]`), so it is kept as a positive case. *NC 1:* the brief keeps `escape` (base): RED on `\`, `x\` and `\[x` (`⟦\\`, `⟦[x`). *NC 2:* the measure-only fix, `escape` kept and the line padded or cut by its rendered width: RED on the literal check (`x\\`). (RB-2, SEC-B1: the fix is R-7's `_literal`; ledger LED-2026-11-06-incMRb.11)
- **Tests:** `P::test_TC_4919_LLR_4652_9_a_backslash_title_in_the_brief_is_literal` (full); `A::test_AT_4655_hostile_titles_stay_literal_at_80x24` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4652.10/1
- **Objective:** Verify that if a presented task's title holds a backslash before a `[`, then view 2 draws that backslash in the title of the task's block.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** a presented task's title holds a backslash before a `[`.
- **Expected result:** titles `a\[b]`, `\[x` and `ab\[` followed by 60 `x` (cut after the `\[`), each once as the cursor task, view 2 at 118x30 and 80x24 → the block's first row, measured on the rendered frame after `to_text`, holds `a\[b]`, `\[x`, `ab\[x…` literally, and every line is exactly the width; 6/6. RED on base: `\[x` reads `[x` and `ab\[`+60 `x` reads `ab[x…`; `a\[b]` already reads `a\[b]` on base (rich's `escape` escapes the tag-shaped `[b]`), so it is kept as a positive case. *NC:* the block heading keeps `escape` (base): RED on `\[x` (`▌ [x`). (SEC-B3; ledger LED-2026-11-06-incMRb.10)
- **Tests:** `P::test_TC_4920_LLR_4652_10_a_backslash_before_a_bracket_stays_in_the_block` (full); `A::test_AT_4655_hostile_titles_stay_literal_at_80x24` (partial).
- **Coverage:** covered. **Result:** verified.

## HLR-4653 — the cursor stops at each milestone, and no key changes (R-2)

### HLR-4653/1
- **Objective:** Verify that when `↑` or `↓` moves the presentation's cursor, the system stops at each drawn milestone in stop order.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** all LLR-4653.n thresholds.
- **Tests:** `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (partial); `A::test_AT_4654_hiding_milestones_from_the_row` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

### LLR-4653.1/1
- **Objective:** Verify that when `↑`, `↓`, `←` or `→` moves the cursor in views 1 and 2, the system moves it one place along the presented project's stop order.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `↑`, `↓`, `←` or `→` moves the cursor in views 1 and 2.
- **Expected result:** Pilot rollout, the cursor on m2, `↓`×4 → m3, m4, m5, `Pilot store list`; `↑` → m5; `→` → `Pilot store list` (`side` = move, base); 3/3. *NC:* base order (by due, milestones among tasks): RED.
- **Tests:** `P::test_TC_4921_LLR_4653_1_the_arrows_step_along_the_stop_order` (full); `P::test_TC_4921_LLR_4653_1_the_shared_walk_and_stop_order` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4652_view_2_the_same_field_and_blocks_in_stop_order` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4653.2/1
- **Objective:** Verify that when `↑` or `↓` moves the cursor in view 3, the system moves it one place along the drawn stops: per project, its head, then its drawn milestones in walk order, then its task rows.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `↑` or `↓` moves the cursor in view 3.
- **Expected result:** on *Pilot rollout*'s head, `↓`×5 → m2, m3, m4, m5, `Pilot store list`; 1/1 per step (5/5). *NC:* one stop per milestone row: RED.
- **Tests:** `P::test_TC_4922_LLR_4653_2_down_from_the_head_walks_the_row` (full); `P::test_TC_4922_LLR_4653_2_view_3s_stops_walk_the_row` (full); `A::test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4653.3/1
- **Objective:** Verify that if the cursor task of views 1 and 2 is not drawn, then the system puts the cursor on the first place of the stop order.
- **Class:** robustness (Unwanted).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the cursor task of views 1 and 2 is not drawn.
- **Expected result:** open `R` with no cursor → m2; cursor task hidden by `space` → the stop order's first; 2/2. *NC:* the first by due among all open tasks (base `open_t[0]`): RED in a fixture where a task is due before every milestone.
- **Tests:** `P::test_TC_4923_LLR_4653_3_the_cursor_falls_back_to_the_first_stop` (full); `P::test_TC_4923_LLR_4653_3_the_screen_starts_on_the_first_stop` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4653.4/1
- **Objective:** Verify that when `space` is pressed with the cursor on a drawn milestone, the system hides that milestone alone.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `space` is pressed with the cursor on a drawn milestone.
- **Expected result:** cursor m3, `space` → m3's `show_in_present` false; m2, m4, m5 still on the row; m4 alone in its cell `▲`, no count; 3/3. *NC:* hide every milestone of the cell: RED.
- **Tests:** `P::test_TC_4924_LLR_4653_4_space_hides_the_cursor_milestone_alone` (full); `A::test_AT_4654_hiding_milestones_from_the_row` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4653.5/1
- **Objective:** Verify that view 1 draws its briefs, and view 2 its blocks, in the presented project's stop order.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** view 1 briefs read m2, m3, m4, m5, then the 4 tasks; view 2 blocks in the same order (two columns from 100 wide, filled in order); 2/2. *NC:* briefs in base order: RED.
- **Tests:** `P::test_TC_4925_LLR_4653_5_briefs_and_blocks_follow_the_stop_order` (full); `A::test_AT_4651_view_1_one_row_and_the_walk` (partial); `A::test_AT_4652_view_2_the_same_field_and_blocks_in_stop_order` (partial).
- **Coverage:** covered. **Result:** verified.

### LLR-4653.6/1
- **Objective:** Verify that the presentation binds exactly the keys it binds at base, and its `?` window lists exactly the rows it lists at base.
- **Class:** normal (Ubiquitous).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** the board, view, size and cursor the threshold names.
- **Expected result:** `PresentScreen` binding set = base; `PresentKeys` window text = base; 2/2. *NC:* bind `←→` to a row walk: RED.
- **Tests:** `P::test_TC_4926_LLR_4653_6_the_keys_and_the_window_are_base` (full); `A::test_AT_4655_the_hint_row_is_base` (partial).
- **Coverage:** covered. **Result:** verified.

## HLR-4654 — the `x` deck is unaffected

### HLR-4654/1
- **Objective:** Verify that the system writes the same deck from `x` as at base.
- **Class:** normal.
- **Preconditions:** None stated.
- **Inputs:** The MR-F fixture of its acceptance tests.
- **Expected result:** LLR-4654.1.
- **Tests:** `A::test_AT_4656_the_x_deck_is_the_base_deck` (partial).
- **Coverage:** covered (with its LLR cases). **Result:** verified.

### LLR-4654.1/1
- **Objective:** Verify that when `x` is pressed in any view, the system writes a deck byte-identical to the deck base writes for the same board, view, scope and day.
- **Class:** normal (Event).
- **Preconditions:** None stated. Fixture MR-F unless the threshold builds its own board.
- **Inputs:** `x` is pressed in any view.
- **Expected result:** MR-F, views 1, 2 and 3 → sha256 equal to a base oracle captured on `8ca174c` from the same fixture; 3/3. *NC:* `present_deck_boards` holds `present_stop_order(present_tasks_m(board, p.id)[0])` in place of `present_tasks_m(board, p.id)[1]`: `ppr`'s proxy drops the reached `tm1` (and any done task), so the sha256 of MR-F's deck differs from the oracle: RED, 3/3. (RB-6, A-1: the NC changes WHICH tasks the deck holds, not their order, which the deck re-sorts by board position)
- **Tests:** `P::test_TC_4931_LLR_4654_1_NC_a_deck_holding_the_stop_order_set_differs` (full); `P::test_TC_4931_LLR_4654_1_the_deck_bytes_equal_the_base_oracle` (full); `P::test_TC_4931_LLR_4654_1_the_proxy_holds_base_order_with_tm1` (full); `A::test_AT_4656_the_x_deck_is_the_base_deck` (partial).
- **Coverage:** covered. **Result:** verified.

**Count:** 29 cases (4 HLR, 25 LLR), all `covered`, all `verified`. Every collected node is cited at least once.

# Baseline notes — milestone rows in the gantt and the presentation, the gantt nav, `hmove` and the link mode's pin at 59775bb

**Counts:** 24 nodes, 12 entities, 27 edges. `codewire_lint` exit 0 (0 findings, 0 lines not read). `codewire_marks` wrote 24 marks, 0 nodes without code. `codewire_extract --path taskboard/app.py,taskboard/views.py,taskboard/modals.py` exit **1**: 36 findings, all of kind "unannotated in code" (33 parameters, 3 returns: `_gantt_frame`, `_all_layout`, `_all_timeline`). No type mismatch, no missing node, no mark drift. A first extract run found 8 `nav_model` parameters missing from the graph; the graph now lists the whole signature. 47 calls listed; extract-baseline.txt marks each one REAL, LIFTED or COLLISION. Lines below are at 59775bb (unmarked). The lines in extract-baseline.txt are in the marked tree.

**Which tree is imported:** the probes put the cwd (incMR-marks) first on `sys.path` and print `taskboard.__file__` = `…\taskboard-wt\incMR-marks\taskboard\__init__.py`. The test runs used `python -m pytest` with cwd = incMR-marks, and printed the same path first.

## What the code does now (the facts the requirements depend on)

- **One row per milestone, everywhere.**
  - `gantt_plan` (views.py:2432) puts every milestone in `GanttGroup.rows` as its own entry. Open milestones sit among the open work by due. Reached ones merge by due only while the group has open work (views.py:2480-2483).
  - A same-day pair is two rows with the mark in the same field cell (P-9: tw5 and tw7 both "◆ Oct 10", lines 8 and 9).
  - Nothing groups milestones today: no row type other than the span row, a task row, the "+N not shown" row and the page hint.
- **`task_row`** (views.py:3388, nested in `_gantt_frame`) draws a milestone as ` <glyph> <title> `, the gutter, `gantt_milestone_cells` (views.py:2713, ONE task per call) and `gantt_milestone_chip`.
  - `gantt_milestone_cells` places the mark and its `Mon D` for one milestone. It knows no neighbour, so it has no clash rule: `◆N` does not exist.
  - The selected milestone's title is in the label column (`title_markup`), as for any task.
- **The ruler** (`_gantt_frame`, views.py:3344-3355) marks the selected project's milestones on the month row. The first one drawn wins a same-day cell, and the project's due `◆` is never covered.
- **Which views draw milestones (MR-1):**
  - **Board gantt (view `3` of the main screen).** Rows, ruler marks and legend entries. With `done_rows=True`, done NON-milestone tasks sit at the tail. A reached milestone with no open work in its group draws no row.
  - **`R` view 1 (`gantt`).** Field rows via `_present_task_row` (views.py:7172), only OPEN milestones (`present_tasks_m`, views.py:6655), plus one brief line each under the rule. The cursor walks them.
  - **`R` view 2 (`split`).** The same field rows, plus a block per open task (milestones included).
  - **`R` view 3 (`all`).** Per shown project, a header row and one `_present_task_row` per open task. Each milestone is a stop of `_all_layout`.
  - The presentation ruler (`_present_ruler`, views.py:7204) marks only the project's due, not its milestones.
  - Kanban never draws a milestone as a card (`kanban_work`; it has the band).
- **The gantt nav** (`nav_model`, gantt branch views.py:8425-8429) is ONE column: every `g.rows` id in draw order, folded groups included. Each milestone is a separate `↑↓` stop (P-2: 31 ids, 6 milestones).
- **The link mode (`L` in the gantt, MR-2).**
  - `action_link` (app.py:3629) pushes `GanttLinkMode` (modals.py:2191).
  - The candidates are `gantt_link_order` (views.py:8885), every group's OPEN rows. Open milestones are candidates; reached ones are not (P-5).
  - `↑↓` cycle the candidates (`GanttLinkMode.action_move`, modals.py:2304). `←→` are not bound there.
  - `gantt_link_frame` (views.py:8893) passes the waiter as `pinned_id`. In `gantt_plan`, `pinned` (the waiter's group key) unfolds like the selection. In `_gantt_frame`, when the pinned group and the selected group cannot both be drawn whole, the pinned one gets `avail // 2` rows and the selection gets the rest.
  - A group taller than its room is paged around the selection, else the pin. A page holds both when it can (views.py:3460-3477).
  - `gantt_link_overlay` draws the link between the two rows in `line_map`, which maps task id → line. So a milestone endpoint today is located by its own row.
- **Hidden classes and `/` search (D3).**
  - `_gantt_frame` applies `_hide` (views.py:3148) at its entry. The presentation applies `present_tasks_m`.
  - `/` search: `_view_board` (app.py:4132) renders and navigates `filtered_board` in kanban and gantt. A milestone matches like any task.
  - **Finding P-10:** `nav_model`'s gantt branch does NOT apply `_hide`. With class "payment" hidden (the test_legend fixture, 118x30), the nav column holds tc8, tcc and tce, which `render_gantt` does not draw. I saw this through the pure functions only, not through the app. It is a pre-existing F-3 gap (the cursor can rest on an undrawn row).
- **Other readers of `GanttGroup.rows`:**
  - `TaskboardApp._notify_folded` (app.py:3523): the "reached · ◆✓" toast checks `any(t is task for t in g.rows)`.
  - `legend_entries` (views.py:8650) calls `_gantt_frame` for what the frame draws. Neither is a node of the graph.

## `hmove` (`←`/`→`) in each view

`TaskboardApp.action_hmove` (app.py:3439) moves to the first task of the nearest non-empty column of `_nav_columns()` that way. With no such column, nothing happens. With the selection not located, `_select_first` runs. `check_action` (app.py:2417) holds it while any other screen is on the stack. Column counts are from P-2 (the probe board, width 118, height 0):

| View | Columns | `←→` today |
|---|---|---|
| gantt | 1 | nothing (no other column); no test pins this |
| kanban (grouped, matrix, lanes) | one per phase (P-2: 5) | first card of the next non-empty column (test_app.py::test_right_moves_to_next_column_first_task, ::test_kanban_group_parity_arrow_walk) |
| chainmap | one per depth (P-2: 4) | first task of the next depth column |
| swimlanes `grid` | the grid's panel columns (`grid_nav`) | next panel column |
| swimlanes waves, agenda, focus, people | 1 | nothing |
| flow, standup, setup | 0 | `_select_first` (no task to land on in these) |
| `R` presentation | — | not `hmove`: `PresentScreen.action_side` (app.py:442). In view 3 with the rail (width ≥ 100) it moves the focus between the rail and the timeline. Anywhere else it is `action_move(delta)`, the same step as `↑↓` through the rows, milestones included |
| gantt link mode | — | not bound |

I took the gantt, waves, agenda and focus rows from the code and P-2's column count, not from a pilot run.

## Probes (run in incMR-marks on the suite's `kg_board.milestones(kg_board.build())`, today 2026-09-30, unless said)

- **P-1 `gantt_plan`**, body 10^6, `done_rows`:
  - pweb rows tw0* tw2 tw3 tw4 tw5* tw6 tw1. pmob tm6 tm2 tm3 tm4 tm5* tm1. papi ta1 ta6 ta3* ta4 ta2 ta5. pdwh td2 td4 td0* td3 td5 td1. pops to0* to1 to3 to2 to5 to4 (* = milestone).
  - Body 12 with tw5 selected: only pweb is unfolded (7 rows).
- **P-2 `nav_model`** column counts, as in the table above.
- **P-3 `render_gantt`**, selected tw5:
  - 118x30: 30 lines, 19 tasks mapped, milestone lines tw0 4, tw5 8, ta3 15, to0 21.
  - 80x24: 24 lines, 13 mapped, tw0 4, tw5 8, to0 15.
  - Rows drawn: " ◇ Mockups approved … ◇✓ Sep 18 … ✓ done", " ◆ Launch new homepage ↳ … ◆ Oct 10 … in 10d", " ◆ Security review sign-off … ◆ Sep 28 … ▲2d".
- **P-5 `gantt_link_order`:** 27 candidates. Open milestones tw5, tm5, ta3, td0 and to0 are in; reached tw0 is out.
- **P-6 `present_tasks_m`(pweb)** open = tw2 tw3 tw4 tw5 tw6. `render_present` 118x30: the field row "▎ ◆ Launch new homepage … ◆ Oct 10 … due Oct 10" and the brief "Launch new homepage … in 10d".
- **P-7 `render_present_all`** 118x30: stops pweb tw2 tw3 tw4 tw5 tw6 pmob tm6 … pdwh td2 td4 td0 td3 td5 pops. The pops tasks are cut by the overflow row.
- **P-8 `milestone_mark`:**
  - tw5 → ("◆", "mut", ""); tw0 → ("◇", "mut", "✓"); to0 → ("◆", "mut", "▲2d"); td0 → ("◆", "mut", "").
  - `gantt_milestone_cells`(tw5) = "◆ Oct 10" at cell 26 of 79.
- **P-9:** tw7 "Press kit", a pweb milestone on Oct 10, is added. pweb rows become tw0 tw2 tw3 tw4 tw5 tw7 tw6 tw1, and the nav walks tw5 then tw7.
- **P-10:** the test_legend `_fx_board` with "payment" hidden: nav 14 ids, frame 11 mapped, and nav-not-drawn = tc8, tcc, tce.

## Tests that pin milestone rows or gantt row counts

Found by two AST passes over `tests/test_*.py` and by an instrumented run. The run used a pytest plugin that wraps `views.gantt_plan` and `views._present_task_row` and records which tests see a milestone row. It changes no behaviour. It covered the 58 test files that name a gantt or presentation seat, the gantt view or `R` (665 + 1139 = **1804 passed**, 0 failed, in incMR-marks before the marks were written; `env -u NO_COLOR python -m pytest -q -p no:cacheprovider`). Test files outside those 58 were not instrumented.

**No test pins `hmove` in the gantt**: grep finds `right`/`left` presses only in kanban, agenda, modal and presentation tests.

### A. Tests that assert on a milestone row through a slice seat

AST pass over `tests/test_*.py`: a test body that names a milestone (or `◆`) AND a slice seat. `M` = the instrumented run saw a milestone in a `gantt_plan` group's rows or in a `_present_task_row` call during the test.

| Test | Line | Seats named | M |
|---|---|---|---|
| tests/test_app.py::test_the_today_rule_spans_every_row | :1845 | gantt_plan |  |
| tests/test_app.py::test_the_due_diamond_marks_the_projects_own_date | :1866 | render_gantt |  |
| tests/test_cascade_app.py::test_AT_611_chain_honesty_through_the_app | :329 | stops | M |
| tests/test_gantt_board.py::test_TC_114_the_month_row | :726 | render_gantt |  |
| tests/test_gantt_board.py::test_TC_117_done_rows_are_the_board_gantts_flag_only | :794 | .rows,_gantt_frame,gantt_plan,render_gantt |  |
| tests/test_gantt_board.py::test_TC_108_the_focused_header_paints_a_trailing_backslash_as_typed | :929 | render_gantt |  |
| tests/test_gantt_link.py::test_TC_511_loop_rows_wear_the_mark_in_the_gutter | :111 | gantt_link_frame |  |
| tests/test_gantt_milestones.py::test_TC_609_rows_merge_reached_milestones_by_due_while_open_work_remains | :68 | .rows,gantt_plan | M |
| tests/test_gantt_milestones.py::test_TC_609_a_group_with_only_reached_milestones_draws_no_row | :81 | .rows,gantt_plan |  |
| tests/test_gantt_milestones.py::test_TC_609_nav_walks_the_drawn_rows_in_draw_order | :93 | line_map,nav_model,render_gantt | M |
| tests/test_gantt_milestones.py::test_TC_609_a_selected_reached_milestone_is_drawn_when_rows_are_scarce | :106 | line_map,render_gantt | M |
| tests/test_gantt_milestones.py::test_TC_609_a_selected_reached_milestone_unfolds_its_group | :115 | gantt_plan | M |
| tests/test_gantt_milestones.py::test_TC_610_today_no_due_and_the_inbox | :142 | gantt_milestone_cells |  |
| tests/test_gantt_milestones.py::test_TC_610_cells_hold_one_diamond_and_its_date_and_never_a_bar | :157 | gantt_milestone_cells |  |
| tests/test_gantt_milestones.py::test_TC_610_a_reached_milestone_on_the_last_column_keeps_its_day | :174 | gantt_milestone_cells |  |
| tests/test_gantt_milestones.py::test_TC_610_a_milestone_title_paints_literally | :187 | render_gantt | M |
| tests/test_gantt_milestones.py::test_TC_611_the_legend_names_milestones_right_after_the_selection | :249 | render_gantt | M |
| tests/test_gantt_milestones.py::test_AT_602_milestones_read_as_dates_reached_ones_quiet_the_ruler_marks_them | :313 | gantt_plan | M |
| tests/test_kanban_milestones.py::test_TC_612_no_card_count_or_nav_holds_a_milestone | :67 | line_map,nav_model |  |
| tests/test_kanban_milestones.py::test_TC_612_a_milestone_selection_moves_to_a_drawn_card | :111 | _nav_columns | M |
| tests/test_kanban_milestones.py::test_AT_603_the_columns_hold_only_work_and_the_band_says_what_is_coming | :318 | _nav_columns |  |
| tests/test_legend.py::test_TC_2608_hidden_classes_leave_the_presentations_three_views | :664 | render_present,render_present_all | M |
| tests/test_milestone_marks.py::test_TC_2604_the_seats_truth_table | :89 | milestone_mark |  |
| tests/test_milestone_marks.py::test_TC_2604_a_nonempty_chip_implies_over_at_the_gantt_cells | :111 | gantt_milestone_cells |  |
| tests/test_milestone_marks.py::test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat | :264 | milestone_mark |  |
| tests/test_milestone_marks.py::test_TC_2602_a_mark_set_on_a_non_milestone_is_kept_and_drawn_nowhere | :605 | milestone_mark |  |
| tests/test_milestone_offer.py::test_TC_616_a_task_that_stops_being_a_candidate_is_counted_not_converted | :291 | stops |  |
| tests/test_milestones.py::test_TC_605_the_editor_box_applies_after_the_dates | :256 | stops | M |
| tests/test_present_milestone.py::test_TC_2101_a_milestone_row_is_its_date_not_a_bar | :58 | gantt_milestone_cells,render_present | M |
| tests/test_present_milestone.py::test_TC_2101_a_start_date_does_not_make_a_milestone_a_bar | :95 | gantt_milestone_cells,render_present | M |
| tests/test_present_milestone.py::test_TC_2101_a_late_milestone_is_painted_over | :118 | render_present | M |
| tests/test_present_milestone.py::test_TC_2101_other_rows_are_drawn_as_shipped | :142 | render_present | M |
| tests/test_present_narrow.py::test_TC_1903_every_width_renders_a_whole_frame | :50 | render_present |  |
| tests/test_present_narrow.py::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits | :211 | .rows |  |
| tests/test_present_polish.py::test_TC_2003_no_cursor_note_without_a_cursor_or_notes | :318 | render_present |  |
| tests/test_present_room.py::test_TC_1608_the_frame_holds_no_presenter_text | :47 | render_present |  |
| tests/test_present_views_app.py::test_AT_1802_the_gantt_note_keeps_its_line_breaks | :157 | .rows |  |

### B. Tests that pin gantt / presentation row counts, folds, pages or stops

AST pass: a gantt or `R` seat AND a count (`len(rows|lines|nav|stops|cols)`, `.rows`, `unfolded`, `line_map[…]`, "not shown", "above"/"below"), not already in A. Without `M`, the test's board drew no milestone row in the run, so variant A should not move its counts; with `M` it can.

| Test | Line | Count words | M |
|---|---|---|---|
| tests/test_dependencies.py::test_gantt_critical_chain_highlights_exactly_three_linked_tasks | :201 | len(lines) |  |
| tests/test_flow.py::test_backlog_bar_is_static_across_ticks | :82 | len(rows) |  |
| tests/test_flow.py::test_the_narrowed_comparison_can_still_see_a_bar_move | :115 | above,len(rows) |  |
| tests/test_gantt_board.py::test_AT_102_down_walks_the_drawn_open_work | :129 | len(rows) |  |
| tests/test_gantt_board.py::test_TC_102_the_window_is_fitted_to_the_open_work | :494 | stops |  |
| tests/test_gantt_board.py::test_TC_103_a_group_that_does_not_fit_is_skipped_not_the_end | :537 | unfolded |  |
| tests/test_gantt_board.py::test_TC_103_a_late_tie_unfolds_the_earlier_due_first_and_height_0_unfolds_all | :550 | unfolded |  |
| tests/test_gantt_board.py::test_TC_106_nav_is_the_plans_rows_and_every_selection_is_drawn | :606 | .rows,len(nav) |  |
| tests/test_gantt_board.py::test_TC_106_every_selection_is_drawn_at_every_height | :817 | len(lines) |  |
| tests/test_gantt_link.py::test_TC_512_the_cycle_skips_loops_and_follows_the_filter | :155 | unfolded |  |
| tests/test_gantt_link.py::test_TC_512_link_mode_keeps_the_waiters_group_open | :256 | unfolded |  |
| tests/test_gantt_link.py::test_TC_512_one_page_holds_both_when_it_can | :417 | unfolded |  |
| tests/test_gantt_polish.py::test_AT_205_a_long_project_says_how_much_is_off_the_page | :117 | above,below,line_map[ |  |
| tests/test_gantt_polish.py::test_TC_209_due_today_counts_as_urgency | :166 | unfolded |  |
| tests/test_gantt_polish.py::test_TC_209_a_tie_on_weight_goes_to_the_group_due_today | :174 | unfolded |  |
| tests/test_gantt_polish.py::test_AT_209_weekends_are_painted_in_the_app | :297 | len(lines[0]) |  |
| tests/test_gantt_polish.py::test_TC_209_the_previous_group_is_offered_rows_before_urgency | :427 | unfolded |  |
| tests/test_gantt_polish.py::test_TC_209_the_inbox_can_be_the_previous_group | :438 | unfolded |  |
| tests/test_gantt_polish.py::test_AT_207_the_project_just_left_stays_open | :542 | line_map[ |  |
| tests/test_present_all.py::test_TC_2103_the_frame_sweep | :188 | len(r.stops),len(rows),len(set(r.stops),not shown,stops,unfolded | M |
| tests/test_present_all.py::test_TC_2103_the_order_follows_present_rank | :245 | stops | M |
| tests/test_present_all.py::test_TC_2103_empty_states | :287 | below,stops |  |
| tests/test_present_all.py::test_TC_2104_the_cycle_and_the_hand_off | :689 | below | M |
| tests/test_present_all.py::test_TC_2105_the_curation_writes_exactly_what_changed | :723 | stops | M |
| tests/test_present_all.py::test_TC_2103_no_stop_hides_under_the_overflow_row | :796 | not shown,stops | M |
| tests/test_present_all.py::test_TC_2105_a_resize_keeps_the_cursor_and_the_rail_safe | :823 | below | M |
| tests/test_present_polish.py::test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut | :272 | len(rows),len(views.present_no,not shown |  |
| tests/test_tick_label.py::test_TC_1701_no_gantt_frame_paints_the_scale | :204 | len(rows) |  |

### C. Every other test whose board draws a milestone row in the gantt plan or the presentation (105 test items)

Instrumented run. Tags: `g` a milestone in a `gantt_plan` group's rows; `g2` a group holding 2 or more milestones (the case variant A merges into one row); `p` a milestone drawn by `_present_task_row`. These do not assert on the row by name, but their frames, line maps or cursor walks go through it.

- **tests/test_boards.py** (1): test_TC_2202_switch_board_starts_the_other_board_over [g]
- **tests/test_boards_home.py** (12): test_AT_2203_the_chip_in_every_view [g]; test_TC_2203_every_view_opens_with_the_chip_at_its_width[118] [g]; test_TC_2203_every_view_opens_with_the_chip_at_its_width[160] [g]; test_TC_2203_every_view_opens_with_the_chip_at_its_width[30] [g]; test_TC_2203_every_view_opens_with_the_chip_at_its_width[40] [g]; test_TC_2203_every_view_opens_with_the_chip_at_its_width[80] [g]; test_TC_2203_markup_in_a_board_name_paints_literally[160] [g]; test_TC_2203_markup_in_a_board_name_paints_literally[30] [g]; test_TC_2203_markup_in_a_board_name_paints_literally[40] [g]; test_TC_2203_markup_in_a_board_name_paints_literally[80] [g]; test_TC_2203_no_label_is_the_base_frame [g]; test_TC_2203_the_presentation_takes_no_chip [p]
- **tests/test_cascade_app.py** (1): test_TC_635_a_milestone_due_edit_that_moves_nobody_stays_silent [g2,g]
- **tests/test_gantt_milestones.py** (3): test_TC_611_a_project_without_milestones_marks_only_its_due [g2,g]; test_TC_611_the_map_and_the_help_name_milestones [g2,g]; test_TC_611_the_month_row_marks_the_selected_projects_milestones [g2,g]
- **tests/test_hotfix_2026_11_05.py** (1): test_AT_HF1_C_toggles_saves_toasts_and_shows_in_help [g]
- **tests/test_legend.py** (4): test_AT_2605_hide_and_the_legend [g2,g,p]; test_TC_2607_help_names_the_classes_the_manager_and_the_class_filter [g2,g]; test_TC_2607_the_presentation_views_carry_the_strip [p]; test_TC_2608_hide_drops_the_class_from_the_gantt_and_the_board_is_untouched [g2,g]
- **tests/test_marks_manager.py** (2): test_AT_2601_a_class_is_created_and_survives[size0] [g2,g]; test_AT_2601_a_class_is_created_and_survives[size1] [g2,g]
- **tests/test_milestone_marks.py** (3): test_AT_2603_the_state_shows_in_text [g2,g,p]; test_AT_2606_hash_pay_filters_to_that_class [g2,g]; test_AT_2607_an_unknown_id_is_safe [g2,g]
- **tests/test_milestone_offer.py** (1): test_AT_604_only_what_was_picked_is_converted_backed_up_logged_and_undoable [g]
- **tests/test_milestones.py** (4): test_AT_601_a_task_becomes_a_milestone_saved_undoable_said_and_pushed [g2,g]; test_TC_604_M_sets_with_one_undo_step_and_refuses_an_undated_task [g]; test_TC_605_the_box_reflects_the_task_and_unticking_clears [g2,g]; test_TC_606_details_phase_row_names_the_milestone [g2,g]
- **tests/test_people_look.py** (3): test_AT_2506_details_card_and_presentation_name_the_people[size0] [p]; test_AT_2506_details_card_and_presentation_name_the_people[size1] [p]; test_TC_2506_the_split_view_shows_names [p]
- **tests/test_people_search.py** (1): test_TC_2505_the_gantt_filters_by_person_too [g]
- **tests/test_present_all.py** (12): test_AT_2102_the_order_and_hidden_projects_survive_a_restart [g2,g,p]; test_AT_2103_the_portfolio_on_one_ruler [p]; test_AT_2104_three_views_one_cursor [p]; test_AT_2105_the_presenter_curates_view_3 [p]; test_AT_2106_u_lists_the_hidden_and_brings_one_back [p]; test_AT_2304_an_unarchived_project_never_ties_a_rank [p]; test_TC_2103_equals_the_rounds_capture[size0-C-160-initial.svg] [p]; test_TC_2103_equals_the_rounds_capture[size1-C-118-initial.svg] [p]; test_TC_2103_markup_in_a_name_paints_literally [p]; test_TC_2103_the_rail_counts_every_hidden_task [p]; test_TC_2106_the_picker [p]; test_TC_2106_the_presentation_stays_in_view_behind_the_picker [p]
- **tests/test_present_backlog_round.py** (4): test_AT_2403_question_mark_shows_every_key [p]; test_AT_2405_K_and_J_reorder [p]; test_TC_2405_the_hint_names_K_J[None] [p]; test_TC_2405_the_hint_names_K_J[label1] [p]
- **tests/test_present_html_export.py** (48): test_TC_4701_LLR_4501_1_project_views_write_exact_html_name[1] [p]; test_TC_4701_LLR_4501_1_project_views_write_exact_html_name[2] [p]; test_TC_4702_LLR_4501_2_all_view_writes_exact_html_name [p]; test_TC_4703_LLR_4501_3_bytes_equal_independent_url_free_H_fixture[1] [p]; test_TC_4703_LLR_4501_3_bytes_equal_independent_url_free_H_fixture[2] [p]; test_TC_4704_LLR_4501_4_all_bytes_equal_independent_url_free_H_fixture [p]; test_TC_4707_LLR_4501_7_only_presented_board_reaches_deck[1] [p]; test_TC_4707_LLR_4501_7_only_presented_board_reaches_deck[3] [p]; test_TC_4709_LLR_4501_9_done_task_title_and_notes_reach_file[1] [p]; test_TC_4709_LLR_4501_9_done_task_title_and_notes_reach_file[3] [p]; test_TC_4710_LLR_4501_10_export_changes_neither_board_nor_history[1] [p]; test_TC_4710_LLR_4501_10_export_changes_neither_board_nor_history[2] [p]; test_TC_4710_LLR_4501_10_export_changes_neither_board_nor_history[3] [p]; test_TC_4711_LLR_4501_11_unlisted_board_uses_label_or_fallback[None-this board] [p]; test_TC_4711_LLR_4501_11_unlisted_board_uses_label_or_fallback[label0-Client A] [p]; test_TC_4712_LLR_4501_12_empty_all_scope_still_writes_deck [p]; test_TC_4715_LLR_4501_15_missing_project_falls_back_to_first_visible[False] [p]; test_TC_4715_LLR_4501_15_missing_project_falls_back_to_first_visible[True] [p]; test_TC_4721_LLR_4502_1_hidden_task_and_id_have_zero_occurrences[1] [p]; test_TC_4721_LLR_4502_1_hidden_task_and_id_have_zero_occurrences[2] [p]; test_TC_4721_LLR_4502_1_hidden_task_and_id_have_zero_occurrences[3] [p]; test_TC_4722_LLR_4502_2_hidden_project_and_its_tasks_have_zero_occurrences [p]; test_TC_4723_LLR_4502_3_archived_and_projectless_tasks_are_excluded[1] [p]; test_TC_4723_LLR_4502_3_archived_and_projectless_tasks_are_excluded[3] [p]; test_TC_4724_LLR_4502_4_hidden_milestone_class_is_excluded[1] [p]; test_TC_4724_LLR_4502_4_hidden_milestone_class_is_excluded[3] [p]; test_TC_4725_LLR_4502_5_legend_omits_class_used_only_by_hidden_task [p]; test_TC_4726_LLR_4502_6_export_reads_hide_flags_at_each_press [p]; test_TC_4727_LLR_4502_7_urls_strip_without_mutating_source_or_next_save[1] [p]; test_TC_4727_LLR_4502_7_urls_strip_without_mutating_source_or_next_save[2] [p]; test_TC_4727_LLR_4502_7_urls_strip_without_mutating_source_or_next_save[3] [p]; test_TC_4731_LLR_4503_1_success_toast_is_exact [p]; test_TC_4732_LLR_4503_2_o_opens_offered_deck_once [p]; test_TC_4733_LLR_4503_3_absent_expired_and_consumed_offers_open_nothing [p]; test_TC_4733b_LLR_4503_3_shared_offer_survives_esc_for_one_main_o [p]; test_TC_4734_LLR_4503_4_write_oserror_toasts_without_crashing [p]; test_TC_4735_LLR_4503_5_failed_export_withdraws_earlier_offer [p]; test_TC_4736_LLR_4503_6_opener_oserror_has_exact_error_toast [p]; test_TC_4736b_LLR_4503_6_relative_uri_valueerror_is_caught [p]; test_TC_4737_LLR_4503_7_markup_in_folder_is_literal_toast_text [p]; test_TC_4741_LLR_4504_1_one_file_oracle[1] [p]; test_TC_4741_LLR_4504_1_one_file_oracle[2] [p]; test_TC_4741_LLR_4504_1_one_file_oracle[3] [p]; test_TC_4742_LLR_4504_2_export_starts_no_subprocess[1] [p]; test_TC_4742_LLR_4504_2_export_starts_no_subprocess[2] [p]; test_TC_4742_LLR_4504_2_export_starts_no_subprocess[3] [p]; test_TC_4761_LLR_4506_1_present_help_names_only_HTML_deck [p]; test_TC_4762_LLR_4506_2_present_help_names_o_offer [p]
- **tests/test_present_milestone.py** (1): test_AT_2101_the_cut_over_weekend_reads_as_a_milestone [p]
- **tests/test_present_note_highlights.py** (4): test_AT_2901_gantt_cursor_note_colours_highlights [p]; test_AT_2902_split_view_colours_highlights_two_sizes[size0] [p]; test_AT_2902_split_view_colours_highlights_two_sizes[size1] [p]; test_AT_2904_mentions_bullets_unpaired_markers [p]

## Marks

The `# node:` marks were written only in incMR-marks: 24 lines, in app.py, views.py and modals.py. That worktree is removed at the end of this step. Nothing in taskboard/ or tests/ of ms-row-proto was touched.

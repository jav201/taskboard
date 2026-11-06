# E4 tests — Inc MR-a (board gantt milestone row) — tester

> Author: independent tester. Written from the design only (`01-requirements.md`, `graph-*.cw.md`,
> `e2-seams.md`, `00-e1-rulings.md` R-1..R-8, `e3-addenda.md`, `baseline-notes.md`). The implementation
> was never read. Base: `154e260` (branch `incMR-tests`). `taskboard/` untouched.
> Evidence states are the seven of `/dev-flow`. Nothing here is `approved`: the tester has no verdict.

## 1. Result

**RED on base: `executed`.** One run, `evidence/red-base.txt` (command and `taskboard.__file__` in its
header; the import is this worktree's `taskboard`): **74 failed, 155 passed** over the 2 new files and the
5 re-baselined files.

- 62 of 73 in `tests/test_milestone_row.py` and 10 of 11 in `tests/test_milestone_row_at.py` fail.
  Every one is an `AssertionError` on observable output, never an `AttributeError`, because no test
  calls a seat that does not exist yet. The reasons are behavioural: base draws one row per milestone
  (`line_map` gives the lane ids 5, 6, 8, 9, 12), `←→` do nothing in the gantt, the nav column keeps
  hidden classes (R-4), and the field shows `Mon D`, not the title.
- 2 re-baselined tests now pin the new behaviour and fail on base for the same reason (§5).
- **GREEN: `not-run`.** No implementation exists in this tree. The orchestrator collects the gate
  run (C-25).

**Oracle check: `executed`.** This is a defect probe of the tests, NOT evidence of GREEN. File:
`evidence/oracle-variantA.txt`. The same 7 files were run against the round's visual oracle (`proto.py`,
variant A, through a scratch plugin whose source is in the file): **26 failed, 203 passed**. Every
failure matches a behaviour the oracle predates (§6, "oracle"). Two of my own test defects came out of
it and are fixed: the TC-4820 cut neighbours sat too close, and TC-4836 assumed `_select_first`'s pick.

## 2. Files (tests and records only)

| File | What |
|---|---|
| `tests/milestone_row_fixture.py` | NEW. Fixture MR-F, copied from `proto.py:70-99` so that no test imports a prototype. Also `Frame` (reads `render_gantt` cells and styles), `painted`/`screen` (the app's compositor strips) and `gantt`/`keys`/`hide_class` (drive the real app) |
| `tests/test_milestone_row.py` | NEW. 49 functions, 73 items, covering LLR-4601.1..LLR-4606.5 |
| `tests/test_milestone_row_at.py` | NEW. 8 functions, 11 items, covering AT-4601..AT-4607 through keys at 118x30 and 80x24 |
| `tests/milestone_row_link_golden.json` | NEW. The BASE link frame (MR-F, m4 waiter, 118x30 and 80x24). I captured it at `154e260` before any implementation existed; it is the R-3 "byte-equal to base" oracle |
| `tests/test_gantt_milestones.py`, `test_milestone_marks.py`, `test_legend.py`, `test_milestone_offer.py`, `test_boards_home.py` | Re-baselined (§5) |
| `evidence/red-base.txt`, `evidence/oracle-variantA.txt` | The two runs |

## 3. Requirement → test coverage (node ids as on disk; state on base)

`R` = RED on base for the behavioural reason. `P` = passes on base by design (§4). All nodes are in
`tests/test_milestone_row.py` unless the row says otherwise.

| LLR | TC | Node | Base |
|---|---|---|---|
| 4601.1 | TC-4801 | `test_TC_4801_LLR_4601_1_one_milestone_row_right_under_each_span_row` | R |
| 4601.2 | TC-4802 | `test_TC_4802_LLR_4601_2_the_row_holds_exactly_the_groups_drawn_milestones` | R |
| 4601.3 | TC-4803 | `test_TC_4803_LLR_4601_3_tasks_one_per_row_in_base_order_under_the_row` | R |
| 4601.4 | TC-4804 | `test_TC_4804_LLR_4601_4_the_inbox_has_its_own_row` | R |
| 4601.5 | TC-4805 | `test_TC_4805_LLR_4601_5_no_drawn_milestone_no_row` | P |
| 4601.6 | TC-4806 | `test_TC_4806_LLR_4601_6_a_folded_group_draws_no_row` | P |
| 4601.7 | TC-4807 | `test_TC_4807_LLR_4601_7_the_row_costs_one_row_of_the_fold_budget` | R |
| 4601.8 | TC-4808 | `test_TC_4808_LLR_4601_8_the_rows_dependency_gutter_is_blank` (MR-F variant: m3 waits on `store`; base `drawn` gets `waits`, N-10) | R |
| 4602.1 | TC-4811 | `test_TC_4811_LLR_4602_1_each_mark_is_its_class_glyph_in_its_class_style` | R |
| 4602.2 | TC-4812 | `test_TC_4812_LLR_4602_2_a_shared_cell_is_one_glyph_and_its_count` (also A-7 digit tone) | R |
| 4602.3 | TC-4813 | `test_TC_4813_LLR_4602_3_ten_or_more_in_one_cell_is_glyph_plus` | R |
| 4602.4 | TC-4814 | `test_TC_4814_LLR_4602_4_a_reached_milestone_alone_is_hollow_and_tick` | R |
| 4602.5 | TC-4815 | `test_TC_4815_LLR_4602_5_the_selected_mark_is_reverse_video` | R |
| 4602.6 | TC-4816 | `test_TC_4816_LLR_4602_6_off_window_dues_draw_the_edge_glyph_and_the_mark_inward` (through `render_gantt`, A-1; the −40 d due is checked to fall before the axis start; also the N-8 `◂⬡2` case) | R |
| 4602.7 | TC-4817 | `test_TC_4817_LLR_4602_7_no_due_draws_no_mark` | R |
| 4602.8 | TC-4818 | `test_TC_4818_LLR_4602_8_a_two_cell_mark_in_the_last_cell_starts_one_before` (through `render_gantt`, A-2: a day does reach cell w-1 at 118) | R |
| 4603.1 | TC-4821 | `test_TC_4821_LLR_4603_1_the_selected_title_after_its_mark_else_before` | R |
| 4603.2 | TC-4822 | `test_TC_4822_LLR_4603_2_no_room_cuts_on_the_roomier_side_from_6_cells` (also SEC-6) | R |
| 4603.3 | TC-4823 | `test_TC_4823_LLR_4603_3_other_marks_carry_their_leads_whole_date_where_it_fits` | R |
| 4603.4 | TC-4824 | `test_TC_4824_LLR_4603_4_a_late_lead_shows_its_days_late_in_over` | R |
| 4603.5 | TC-4825 | `test_TC_4825_LLR_4603_5_no_label_covers_a_mark_or_the_edge[118-30/80-24]` (5 scenes each = 10 frames) | R |
| 4603.6 | TC-4826 | `test_TC_4826_LLR_4603_6_the_label_column_at_rest` | R |
| 4603.7 | TC-4827 | `test_TC_4827_LLR_4603_7_the_label_column_names_the_selected_member` (also A-7 `title_markup` cue) | R |
| 4603.8 | TC-4828 | `test_TC_4828_LLR_4603_8_the_chip_is_the_selected_else_the_upcoming_anchor` | R |
| 4603.9 | TC-4829 | `test_TC_4829_LLR_4603_9_no_line_wider_than_the_terminal[118-30/80-24/118-12]` (8 scenes, the AT states, 24 frames) | P |
| 4603.10 | TC-4830 | `test_TC_4830_LLR_4603_10_the_legend_names_the_rows_marks` | P |
| 4603.11 | TC-4820 | `test_TC_4820_LLR_4603_11_a_field_label_draws_its_literal_text_in_cells[...]`: 5 titles × after/before/cut at 118 = 15, plus 5 long cuts at 80 (SEC-7) = 20 | R |
| 4604.1 | TC-4831, TC-4831b | `test_TC_4831_LLR_4604_1_up_down_stop_on_the_row_once` (keys), `test_TC_4831b_LLR_4604_1_the_nav_column_holds_one_stop_per_row` | R, R |
| 4604.2 | TC-4832, TC-4832b | `test_TC_4832_LLR_4604_2_landing_on_a_row_selects_its_anchor`, `test_TC_4832b_LLR_4604_2_up_lands_on_the_anchor` | R, R |
| 4604.3 | TC-4833 | `test_TC_4833_LLR_4604_3_right_walks_to_the_next_in_walk_order` | R |
| 4604.4 | TC-4834 | `test_TC_4834_LLR_4604_4_left_walks_back` | R |
| 4604.5 | TC-4835 | `test_TC_4835_LLR_4604_5_the_ends_keep_the_selection` | P |
| 4604.6 | TC-4836 | `test_TC_4836_LLR_4604_6_off_the_row_left_right_are_base` | P |
| 4604.7 | TC-4837 | `test_TC_4837_LLR_4604_7_enter_opens_the_walked_milestone` | R |
| 4604.8 | TC-4838 | `test_TC_4838_LLR_4604_8_task_keys_act_on_the_walked_milestone` | R |
| 4605.1 | TC-4841 | `test_TC_4841_LLR_4605_1_a_query_keeps_only_the_matching_milestones_on_the_row` | R |
| 4605.2 | TC-4842 | `test_TC_4842_LLR_4605_2_a_hidden_class_leaves_the_row` | R |
| 4605.3 | TC-4843 | `test_TC_4843_LLR_4605_3_the_walk_skips_what_the_row_does_not_draw` | R |
| R-4 | TC-4843b, TC-4843c | `test_TC_4843b_R4_the_nav_column_holds_no_hidden_class_milestone` (P-10 fixture + MR-F), `test_TC_4843b_R4_the_cursor_never_stops_on_a_hidden_class_milestone` (**item 4**, keys), `test_TC_4843c_R4_the_stop_is_the_one_the_frame_draws` | R, R, R |
| A-5 | TC-4843d | `test_TC_4843d_A5_hiding_the_selected_milestones_class` | P |
| 4606.1 | TC-4851 | `test_TC_4851_LLR_4606_1_the_link_frame_keeps_one_row_per_milestone[118x30/80x24]` (golden) | P |
| 4606.2 | TC-4852 | `test_TC_4852_LLR_4606_2_L_on_a_walked_milestone_makes_it_the_waiter` | R |
| 4606.3 | TC-4853 | `test_TC_4853_LLR_4606_3_closing_the_link_mode_brings_the_rows_back` | R (the `esc` half passes on base) |
| 4606.4 | TC-4854 | `test_TC_4854_LLR_4606_4_a_selected_member_selects_the_page_holding_the_row` | R |
| 4606.5 | TC-4855 | `test_TC_4855_LLR_4606_5_only_spans_and_the_selection_draws_the_row[tm3/tm4]` | R |

**ATs** (`tests/test_milestone_row_at.py`; keys only, screen read from the compositor):

| AT | Node | Base |
|---|---|---|
| AT-4601 | `test_AT_4601_the_row_at_rest[size0/size1]` | R, R |
| AT-4602 | `test_AT_4602_folding` | P |
| AT-4603 | `test_AT_4603_onto_the_row_and_along_it[size0/size1]` | R, R |
| AT-4604 | `test_AT_4604_acting_on_the_walked_one` | R |
| AT-4605 | `test_AT_4605_search_and_hidden_classes` | R |
| AT-4606 | `test_AT_4606_link_mode_and_pages` and `test_AT_4606b_a_paged_group_pages_to_its_row` | R, R |
| AT-4607 | `test_AT_4607_edges[size0/size1]` | R, R |

**Uncovered: none of the 43 LLRs or the 7 ATs.** Partial coverage and deviations are in §6.

## 4. Passing on base by design (12 items)

Each of these guards behaviour that base already has and the change must keep. They are not
evidence that the feature works.

- TC-4805: base draws no row for these 3 groups.
- TC-4806 and AT-4602: base folded groups draw only their span row.
- TC-4829 ×3: base never draws past the width.
- TC-4830: base's per-milestone rows add `milestone` and `reached`.
- TC-4835: base `hmove` is a no-op in the gantt, so the ends trivially hold.
- TC-4836: base behaviour, by definition.
- TC-4843d: base's app already moves the selection off a milestone whose class is hidden. The test
  guards that the lane walk does not bring the selection back onto it.
- TC-4851 ×2: the golden IS base's link frame.

## 5. Old tests re-baselined (item 5)

Method (A-4): the candidates come from `baseline-notes.md` §A (`M`), §B (`M`) and §C (`g`/`g2`). Those
20 files were run against the oracle. Base passes all of them. The 12 that failed were read one by one,
and each failure was sorted into one of two kinds: (a) MR-a's requirements break the assertion, so the
test is re-baselined, or (b) the oracle predates a requirement, so the test is left unchanged. Every test
tagged `p` only is byte-identical (the A-4 presentation guard).

| Test | What moved | Change | LLR |
|---|---|---|---|
| `test_gantt_milestones.py::test_TC_609_nav_walks_the_drawn_rows_in_draw_order` | `line_map` names every member of a lane, the nav column only its stop. Comparing ids was therefore false | It now compares LINES: each drawn line holds exactly one stop, in draw order, and `tw0` is in both. This is stricter than before (one stop per line). Passes on base | 4604.1, SEAM-9 |
| `test_gantt_milestones.py::test_AT_602_…` | The selected milestone's field shows its title, not `Mon D`. `Mockups approved` has no row of its own. A lone late milestone's chip is blank. `↑` lands on the anchor | Field: `◆` then `Launch new homepage`, no bar. `◇✓` (mut/reached) and its date in reached grey on the SAME row (`line_map` equal). `Security review sign-off`: `▲2d` in over in the field and a blank chip. `↑` → `tw5`, `←` → `tw0`, `↓` → `tw2`. Dropped: `Mockups` title tone and its `✓ done` chip, because their row no longer exists (4603.3, 4603.8). RED on base | 4601.1, 4603.1, .3, .4, .8, 4604.2, .4 |
| `test_milestone_marks.py::test_AT_2603_the_state_shows_in_text` (gantt arm, 118 and 80) | `Oct 18` in over beside the SELECTED late milestone is gone (title instead). `Handover call` and `Pilot launch` have no title rows | The selected one keeps its label glyph in violet and its `▲2d` chip in over. New helper `_gantt_states_at_rest`: with `tc6` unselected, `■` violet, `▲2d` in over beside it, no `Oct 18`; `◆` mut on `tcd`'s row; `★` pink on `tcb`'s row (118 only, as before). RED on base | 4603.1, .4, .7, .8 |
| `test_legend.py::test_TC_2608_hide_drops_the_class_from_the_gantt…` | The positive control `'Milestone 2 invoice' in gantt` relied on an unselected title | The probe is now `line_map`: hidden → no `tc8/tcc/tce`; shown → all three. The title-absence check is kept. Passes on base | 4601.1, 4605.2, SEAM-9 |
| `test_legend.py::test_AT_2605_hide_and_the_legend` (gantt arms) | Title absence became vacuous, and the unhide check needed an unselected title | Adds `_payment_marks` (`⬢`/`⬡` in the body field): present before hiding, 0 when hidden at 118 and at 80, back after unhide. Title checks kept. Presentation arms untouched. Passes on base | 4605.2 |
| `test_milestone_offer.py::test_AT_604_…` (last assertion) | ` ◆ Launch new homepage` holds only while selected | The converted task's line (`_line_map["tw5"]`) starts ` ◆ `. Passes on base | 4601.1, 4603.6 |
| `test_boards_home.py::test_TC_2203_no_label_is_the_base_frame` (gantt only) | The `783397e` capture of the gantt frames goes stale on purpose | For `gantt`, the frame now equals the shipped `render_gantt` (render_view adds nothing without a label). The head row still equals the capture, and the row-0 span check is kept. Other modes are unchanged. Passes on base | 4601.1 |

**Left unchanged, because only the oracle fails them (the spec keeps them):**

- `test_TC_610_a_milestone_title_paints_literally[[/]]`: the selected label is `title_markup`; the
  oracle's per-character put raises `MarkupError` (R-7).
- `test_TC_611_the_legend_names_milestones_right_after_the_selection` ×2, and
  `test_TC_611_the_map_and_the_help_name_milestones`: the oracle lacks `reached` in `drawn`, which
  LLR-4603.10 requires.

**A-3 (`↳` on a board-gantt milestone row): no test found.** `test_gantt_board.py:180-198` and
`test_gantt.py:610-617` draw no milestone: `kg_board.build()` has none, and the oracle, whose gutter is
blank, passes them. The lost gutter is an accepted behaviour change, so it still goes into the batch
packet (integrator).

## 6. Mutant table (each LLR's negative control → the test that kills it)

Kill states:
- `executed (base)`: base IS the mutant, and the test is RED in `red-base.txt`.
- `executed (oracle)`: the oracle IS the mutant, and the test is RED in `oracle-variantA.txt`.
- `planned`: the kill needs the mutant applied to the implementation, which does not exist yet. The
  reason the test kills it is given.

| LLR | Negative control | Killed by | State |
|---|---|---|---|
| 4601.1 | row after the group's last task | TC-4801 (`== span+1`) | planned |
| 4601.2 | drop reached milestones | TC-4802 (Pilot set holds `tm1`) | planned |
| 4601.3 | tasks sorted by title | TC-4803 (`store, tele, train, rota` ≠ title order) | planned |
| 4601.4 | i1 on the first project's row | TC-4804 | planned |
| 4601.5 | always emit the row | TC-4805 (3 groups, no milestone id mapped) | planned |
| 4601.6 | row under a folded span | TC-4806, AT-4602 | planned |
| 4601.7 | each milestone counted in the fold budget | TC-4807 (80x24 folds Docs) | executed (base) |
| 4601.8 | stop's `↳` in the gutter | TC-4808 | executed (base) |
| 4602.1 | `◆` for every class | TC-4811 | planned |
| 4602.2 | first glyph only, no count | TC-4812 | planned |
| 4602.3 | print `10` | TC-4813 (`+` at x+1, ground at x+2) | planned |
| 4602.4 | filled glyph when reached | TC-4814 | planned |
| 4602.5 | no reverse | TC-4815, TC-4855, AT-4603 | planned |
| 4602.6 | clamp without the edge glyph | TC-4816, AT-4607 | executed (oracle) |
| 4602.7 | undated drawn at today | TC-4817 (1 mark) | planned |
| 4602.8 | 2-cell mark started at w-1 | TC-4818 (cells `w-2..w-1`, line = 118) | planned |
| 4603.1 | always after, overflowing | TC-4821 (`before` case) | planned |
| 4603.2 | cut to any width (`R…`) | TC-4822 (cramped: no title cell) | planned |
| 4603.3 | a cut date (`Oct`) | TC-4823 (regex) | planned |
| 4603.4 | `Oct 19` for the late lead | TC-4824 | planned |
| 4603.5 | no one-cell gap check | TC-4825 | planned |
| 4603.6 | late count omitted | TC-4826 (`▲1`) | planned |
| 4603.7 | `i/N` dropped | TC-4827, TC-4855, AT-4603 | planned |
| 4603.8 | first member's chip (`✓ done`) | TC-4828 (`in 4d`) | planned |
| 4603.9 | label padded to label_w+1 | TC-4829 (≤ W), TC-4820 (= W on the row) | planned |
| 4603.10 | row not adding to `drawn` | TC-4830 | executed (oracle) |
| 4603.11 | per-character `c()` | TC-4820 (`x\` and wide cases garbled or too wide; `MarkupError` on the `a]b[/]` before and cut cases) | executed (oracle) |
| 4603.11 NC 2 | room measured with `len` | TC-4820 wide cases (line `cell_len` ≠ W) | executed (oracle) |
| 4604.1 | one stop per milestone | TC-4831, TC-4831b | executed (base) |
| 4604.2 | first in walk order (m1) | TC-4832, TC-4832b | planned |
| 4604.3 | skip same-day | TC-4833 (`m3 → m4`) | planned |
| 4604.4 | `←` moves forward | TC-4834 | planned |
| 4604.5 | wrap around | TC-4835 | planned |
| 4604.6 | `→` on a task row jumps to the row | TC-4836 | planned |
| 4604.7 | details of the anchor | TC-4837 | executed (base: details of `tm3`) |
| 4604.8 | stop stays the anchor | TC-4838 | executed (base: `]` moved `tm3`) |
| 4605.1 | row from the unfiltered board | TC-4841 (one `▲`, `◆ 1 milestone`) | planned |
| 4605.2 | row built before the class filter | TC-4842 (3 marks) | planned |
| 4605.3 | walk the unfiltered milestones | TC-4843, AT-4605 | planned |
| R-4 | nav keeps hidden classes | TC-4843b ×2, TC-4843c | executed (base) and executed (oracle) |
| 4606.1 | shared row in the link frame | TC-4851 (golden, plain and markup) | planned |
| 4606.2 | the anchor as waiter | TC-4852 | executed (base: waiter `tm3`) |
| 4606.3 | a flag left set by the link frame | TC-4853 | planned |
| 4606.4 | paged by the milestone's base row index | TC-4854 (`▼ 13 below`, no `above`) | planned |
| 4606.5 | base `task_row(sel)` | TC-4855 | executed (base) |

## 7. Deviations, findings, handoffs

- **F-T1, a threshold defect (to `qa-reviewer`).** LLR-4603.1's examples cannot hold on MR-F at 118:
  - **m3:** "`Steering go/no-go` follows `■2 `" does not fit. m5 sits 12 cells right of m3, so 8
    cells are free after the gap, and the round's oracle shows `■2·Steerin…` (scene `A-sel`).
  - **m5:** m5 "with no room after" is false, because 46 cells lie to its right.
  - **What I tested:** the statement. TC-4821 places `after` with g2 and `before` with a reached
    milestone due on the field's last day. TC-4822 pins the oracle's `Steerin…` cut.
  - **Request:** amend the threshold.
  - AT-4603 is written to accept the title whole or cut (`■2 Steerin`).
- **F-T2, A-2 found.** At 118 a product route reaches cell w-1: k = 0.5 and `day(78)` = Nov 22 gives
  cell 78. At 80 it does not, since the start day falls on an odd cell. TC-4818 runs at 118 only.
- **F-T3, N-8 partial.** At k = 0.5 a day is 2 cells, so two marks at w-2 and w-1, or a 2-cell mark
  over the next day's cell, cannot happen on any product route at 118 or 80. The reachable collision is
  `◂⬡✓` over an in-window reached milestone at cell 2, and TC-4816 asserts that it joins the bucket
  (`◂⬡2`). The other N-8 cases are `n/a — unreachable through render_gantt`.
- **F-T4, N-9 not covered.** "A label run does not inherit its first cell's weekend shading" does not
  say what ground the covered cells get. It is ambiguous, so it goes to `qa-reviewer` or `ux-reviewer`.
- **F-T5, a tone carried over.** The re-baselined AT-602 still asserts that a reached lead's date is in
  the reached grey. That is the M-1/UXV-5 law, which MR-a's LLRs do not restate. If the implementation
  paints it `mut`, the test turns RED, and the ruling is `qa-reviewer`'s.
- **F-T6, the golden's author.** `milestone_row_link_golden.json` was captured by the test's own author.
  It is captured from BASE code, which predates the implementation. That is exactly R-3's "byte-equal to
  base" claim, not the implementation's own output.
- **A-1:** satisfied. MR-F's earliest open start is −6 d (`gq`); the axis starts Oct 14, and −40 d
  falls before it, which TC-4816 asserts.

## 8. Gaps and limits

- **GREEN `not-run`.** The mutation kills marked `planned` need the implementation.
- **Width clauses of the ATs.** The compositor crops to the terminal, so a screen width check cannot
  fail. TC-4829 and TC-4820 carry the width clause at layer 0. The AT width asserts are guards only.
- **TC-4843d.** It cannot see the ruler echo directly. It asserts that no painted line names
  `Steering go/no-go`.
- **The re-baseline list is a prediction.** It comes from oracle runs on the 20 candidate files plus
  reading of the code. Any other test the implementation turns RED is for the integrator to sort,
  re-baseline or regression, at the gate run (A-4 owner).
- **Not run here:** the full suite. That is the orchestrator's gate run (C-25).
- **No GPU or network.** No new dependency was added. All data is synthetic; no PII and no credentials.

## 9. Evidence checklist

- [✓] Every named test exists at the cited path and name (§3, collected: 73 + 11 items).
- [✓] Results read from one complete run each, command quoted in the header (`evidence/red-base.txt`:
  74 failed, 155 passed; `evidence/oracle-variantA.txt`: 26 failed, 203 passed).
- [✓] RED on base captured against `154e260` (§1). GREEN is `not-run`.
- [✓] Assertions read observable output (cells, styles, `line_map`, the nav column, the selection after
  keys, the painted screen), never a call sequence.
- [✓] Uncovered requirements named: none. Partials named (F-T3, F-T4).
- [✓] Environment limits declared (§8).
- [✓] No real PII, credentials or client data. Titles and names are synthetic; the owner placeholder is
  not used.
- [✓] Evidence states used: `executed`, `planned`, `not-run`, `n/a — <reason>`.

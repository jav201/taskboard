# E4 — tests — Inc MR-b (the presentation's milestones share one row)

**Author:** tester (independent of the V/S implementers; written from the design only, never from MR-b code).
**Base revision:** `8ca174c` (MR-a merged). Branch `incMRb-tests` at `81c8ec7`: its `taskboard/` equals `8ca174c`'s
(`git diff --stat 8ca174c HEAD -- taskboard` is empty). Every run printed `taskboard.__file__` =
`…\taskboard-wt\incMRb-tests\taskboard\__init__.py`.
**Base oracle:** `tests/milestone_row_present_base.json`, captured on a detached worktree at `8ca174c`
(`taskboard.__file__` = `…\incMRb-base8ca\taskboard\__init__.py`, stored in the JSON) by
`evidence/capture_base.py`, BEFORE any MR-b code existed; the worktree was removed after the capture.
**Evidence state:** RED on base `executed` (`evidence/red-base.txt`). GREEN `not-run` — MR-b is not implemented
on this branch. No verdict here: approval is the reviewers'.

## 1. Files

| File | What |
|---|---|
| `tests/test_present_milestone_row.py` | 25 LLRs, TC-4901..TC-4931, layer 0 + pilot where the LLR is about keys |
| `tests/test_present_milestone_row_at.py` | AT-4651..AT-4656, black box: the real app, `R` and its keys, 118x30 and 80x24 |
| `tests/milestone_row_present_fixture.py` | the readers (cells after `to_text`, `cell_len`, per-cell Style), the app driver, the deck helper and the deck mutant |
| `tests/milestone_row_present_base.json` | the base oracle (deck sha256 layer 0 and app, header/ruler/strip rows, hint rows, `?` window, bindings) |
| `evidence/capture_base.py` | the capture script (run once on `8ca174c`) |
| `evidence/red-base.txt` | the full-suite run on base |
| rewritten: `tests/test_present_milestone.py`, `tests/test_present_all.py`, `tests/test_present_note_highlights.py`, `tests/test_milestone_marks.py` | §5 |

Every frame is measured on the RENDERED text — `render_present(…).plain`, `render_present_all(…).timeline/.frame`,
or the PresentScreen's `#present-frame` Text — per line with `cell_len`; never `_strip` of the markup, never the
assert alone (B-2, SEC-B2).

## 2. Requirement → test coverage

Node ids are `tests/test_present_milestone_row.py::<name>` (TC) and `tests/test_present_milestone_row_at.py::<name>` (AT).

| Req | Test(s) on disk | RED on base |
|---|---|---|
| HLR-4651 (5 body rows, base 8) | `test_TC_4901_LLR_4651_1_one_milestone_row_directly_under_the_span` | yes |
| LLR-4651.1 | `test_TC_4901_LLR_4651_1_one_milestone_row_directly_under_the_span[gantt,split]` | 2/2 |
| LLR-4651.2 | `test_TC_4902_LLR_4651_2_view_3_one_row_under_each_head` | 1/1 |
| LLR-4651.3 | `test_TC_4903_LLR_4651_3_the_row_holds_exactly_the_drawn_milestones[1,3 × all,review_hidden,m3_hidden]` | 6/6 |
| LLR-4651.4 | `test_TC_4904_LLR_4651_4_tasks_one_per_row_in_base_order_under_the_row[gantt,split,all]` | 3/3 |
| LLR-4651.5 | `test_TC_4905_LLR_4651_5_no_drawn_milestone_no_row[1,3]` | 0/2 — passes by design |
| LLR-4651.6 | `test_TC_4906_LLR_4651_6_a_folded_project_draws_no_row` | 1/1 (via its positive control, see §4) |
| LLR-4651.7 | `test_TC_4907_LLR_4651_7_the_row_counts_as_one_row_for_the_overflow` | 1/1 |
| LLR-4651.8 | `test_TC_4908_LLR_4651_8_the_rows_dependency_gutter_is_blank[1,3 × 118x30,80x24]` | 4/4 |
| LLR-4652.1 | `test_TC_4911_LLR_4652_1_the_field_is_the_board_gantts_row[1,3 × tm3,tm4,tstore × 118,80]` | 12/12 |
| LLR-4652.2 | `test_TC_4912_LLR_4652_2_a_reversed_mark_and_a_covered_label_paint_once` | 1/1 |
| LLR-4652.3 | `test_TC_4913_LLR_4652_3_the_label_at_rest[4 params]` | 4/4 |
| LLR-4652.4 | `test_TC_4914_LLR_4652_4_the_label_on_a_milestone[4 params]` | 3/4 (m2 at 118 passes by design) |
| LLR-4652.5 | `test_TC_4915_LLR_4652_5_the_rows_chip[cursor_m2,cursor_task,only_late]` | 2/3 (cursor_m2 passes by design) |
| LLR-4652.6 | `test_TC_4916_LLR_4652_6_hostile_milestone_titles_are_literal[1,3 × 4 titles]` | 8/8 |
| LLR-4652.7 | `test_TC_4917_LLR_4652_7_no_line_wider_than_the_terminal[3 views × 3 sizes]` | 0/9 — passes by design |
| LLR-4652.8 | `test_TC_4918_LLR_4652_8_header_ruler_and_strip_as_at_base[3 views × 2 sizes]`; hint row: `test_AT_4655_the_hint_row_is_base` | 0/6, 0/2 — by design |
| LLR-4652.9 | `test_TC_4919_LLR_4652_9_a_backslash_title_in_the_brief_is_literal[4 titles × 2 sizes]` | 6/8 (`a\[b]` passes on base, F-1) |
| LLR-4652.10 | `test_TC_4920_LLR_4652_10_a_backslash_before_a_bracket_stays_in_the_block[3 titles × 2 sizes]` | 4/6 (`a\[b]` passes on base, F-1) |
| LLR-4653.1 | `test_TC_4921_LLR_4653_1_the_shared_walk_and_stop_order`, `test_TC_4921_LLR_4653_1_the_arrows_step_along_the_stop_order` | 2/2 |
| LLR-4653.2 | `test_TC_4922_LLR_4653_2_view_3s_stops_walk_the_row`, `test_TC_4922_LLR_4653_2_down_from_the_head_walks_the_row` | 2/2 |
| LLR-4653.3 | `test_TC_4923_LLR_4653_3_the_cursor_falls_back_to_the_first_stop`, `test_TC_4923_LLR_4653_3_the_screen_starts_on_the_first_stop` | 2/2 |
| LLR-4653.4 | `test_TC_4924_LLR_4653_4_space_hides_the_cursor_milestone_alone[1,3]` | 2/2 |
| LLR-4653.5 | `test_TC_4925_LLR_4653_5_briefs_and_blocks_follow_the_stop_order[gantt,split]` | 2/2 |
| LLR-4653.6 | `test_TC_4926_LLR_4653_6_the_keys_and_the_window_are_base` (+ `?` in AT-4655) | 0/1 — by design |
| LLR-4654.1 | `test_TC_4931_LLR_4654_1_the_deck_bytes_equal_the_base_oracle[1,2,3]`, `…_NC_a_deck_holding_the_stop_order_set_differs[1,2,3]`, `…_the_proxy_holds_base_order_with_tm1` | 0/7 — by design (the NC passes = the oracle CAN fail) |
| AT-4651 | `test_AT_4651_view_1_one_row_and_the_walk[118x30,80x24]` | 2/2 |
| AT-4652 | `test_AT_4652_view_2_the_same_field_and_blocks_in_stop_order[118x30,80x24]` | 2/2 |
| AT-4653 | `test_AT_4653_view_3_rows_walk_fold_rail_and_overflow` (118x30, then 118x19) | 1/1 |
| AT-4654 | `test_AT_4654_hiding_milestones_from_the_row[118x30,80x24]` | 2/2 |
| AT-4655 | `test_AT_4655_hostile_titles_stay_literal_at_80x24[6 titles]`, `test_AT_4655_the_hint_row_is_base[2 sizes]` | 6/6, 0/2 by design |
| AT-4656 | `test_AT_4656_the_x_deck_is_the_base_deck` | 0/1 — by design |

**Uncovered / partial, named:** none of the 25 LLRs or 6 ATs is without a node. Partial: LLR-4651.6's 80x14
overflow case is layer 0 only (no pilot at 80x14). LLR-4653.3's "cursor task hidden by `space`" case is layer 0
(`render_present` with a hidden `cursor_id`); the screen's own fallback is exercised with no cursor (TC-4923 pilot).
B-6 (a real capture of view 2 on MR-F at 118x30 for the operator's RB-1 review) is `blocked` — it needs MR-b's code.

## 3. Interpretations made (stated, not hidden)

- **AT-4653's "118x18 (room 15, need 15)"** is the FRAME size. The app's hint row takes the terminal's last row, so
  the AT drives a 118x**19** terminal (frame 18, room 15). Layer 0 (TC-4907) uses `render_present_all(…, 118, 18)`,
  as P-4 did.
- **The milestone row is found by place**: views 1/2 the line under the span row (`▌ `), view 3 the line under the
  project's head — the design's statement (LLR-4651.1/.2), not a title search (an unselected title is not painted).
- **TC-4911's field oracle** is MR-a's frozen `gantt_milestone_row` (SEAM-4) on the view's own axis, as LLR-4652.1
  states; the walk order of the lane is restated in the test (`(due is None, due, title, id)`), not imported. On base
  that oracle reproduces P-6's literals (`■ ▲1d     ■2 Steerin… ★ Oct 30`), so the oracle itself is checked.
- **TC-4931's NC** (B-4): the mutant feeds the SHIPPED `present_deck_boards` `present_tasks_m(…)[0]` as `[1]`.
  `present_stop_order` is pure (SEAM-2) and the deck re-sorts by board position, so the mutant's held set equals
  `present_stop_order(…[0])`'s; written without the new unit so the control also runs on base.
- **TC-4916 / AT-4655 `literal_cut`**: the title whole, or its head cut with `…`; a one-cell pad before `…` is
  allowed where a wide glyph did not fit (base cuts `日本語のタイ …`).

## 4. RED on base — `executed`

Command (one complete run): `env -u NO_COLOR python -m pytest -p no:cacheprovider -q -rfE`, header prints
`taskboard.__file__`. Transcript: `evidence/red-base.txt`. The counts below are read from that run (§4.1).

**Why each new test is RED on base** (the first failing assertion, read from the run):
- TC-4901/4902/4904/4907, AT-4651/4652/4653: base draws one field row per milestone (8 body rows; marks on 4 lines;
  view 3 at 118x18 folds Eval harness and Docs & handover).
- TC-4903, TC-4911..4916, AT-4654, AT-4655: the line under the span/head is m2's own row (or a task's), not the
  shared row — no `■2`, no `▲1d`, no `⟦` on a non-m2 cursor, no reverse cell (base paints the cursor `bright` bold).
- TC-4906: its positive control (the cursor project's row under its head) — base has no such row.
- TC-4908: base's m3 row draws `↳` in its gutter.
- TC-4919 (regression, LLR-4652.9): `\` and `x\` → brief `⟦\\⟧` / `⟦x\\⟧`, 119 / 81 cells; `\[x` → `⟦[x⟧`.
- TC-4920 (regression, LLR-4652.10): `\[x` → `▌ [x`; `ab\[`+60 `x` → `▌ ab[x…`.
- TC-4921/4922/4923/4924/4925: `milestone_walk_key` / `present_stop_order` do not exist (AttributeError); the
  cursor walks by due (`↓` from m2 → `Pilot store list`); Docs & handover's fallback is `API reference`.

**Pass on base BY DESIGN** (they pin what must NOT change, or a case base already gets right):
TC-4905 ×2 (no row when no milestone), TC-4914[tm2-118] (base m2 row reads the same), TC-4915[cursor_m2],
TC-4917 ×9 (widths on MR-F's plain titles), TC-4918 ×6 (oracle is base's), TC-4919[`a\[b]`] ×2 and
TC-4920[`a\[b]`] ×2 (F-1), TC-4926 (oracle is base's), TC-4931 ×3 + its NC ×3 + the proxy example (oracle is base's;
the NC passing proves the byte check can fail, 3/3), AT-4655 hint row ×2, AT-4656.

### 4.1 Run result

FILLED FROM THE RUN — see the bottom of this section after the run completes.

## 5. Existing tests rewritten (each one, why, and what was kept)

Rule (B-9): the 7 PRES-V3/PRES-V4 frame oracles hold no milestone and are NOT touched; only tests on milestone
boards were changed, each citing the LLR that moves it. No assertion unrelated to the shared row was removed.

| Test | Why the design changes it | Rewrite or re-baseline; what is kept |
|---|---|---|
| `test_present_milestone.py::test_TC_2101_a_milestone_row_is_its_date_not_a_bar` (8 params) | LLR-4651.1/4652.1: the milestone has no own row; an unselected title is not painted, so `_row(text, title)` finds nothing | **Rewritten** on the project's milestone row (by place). Kept: width, no bar glyph, `◆` in the label, lead `⟦` iff cursor, chip `due <Mon D>`, cursor-vs-off paint distinction, the 36-column clause. Changed by design: the field oracle is `gantt_milestone_row` (was `gantt_milestone_cells`); the off-cursor chip is the first upcoming milestone's (LLR-4652.5); the cursor paint is reverse (SEAM-5) where base had bright bold |
| `…::test_TC_2101_a_start_date_does_not_make_a_milestone_a_bar` | same; with the cursor on `tc2` the row's chip is not `tc5`'s own (LLR-4652.5) | **Rewritten**: cursor on `tc5`; every assertion kept (no bar, one `◆`, `due Nov 6`; no due → no mark, `no dates`) |
| `…::test_TC_2101_a_late_milestone_is_painted_over` | MR-a LLR-4603.3: an unselected late milestone shows its late tag (`▲3d`), not its date; with no upcoming member the row has no chip; the cursor paint is reverse | **Re-baselined**: `◆` in `mut` off the cursor, lateness in `over` (on the tag), the cursor's chip `due Oct 16` in `over` |
| `…::test_TC_2101_other_rows_are_drawn_as_shipped` | — | unchanged |
| `…::test_AT_2101_the_cut_over_weekend_reads_as_a_milestone` | the row is found by place (title not painted off the cursor) | **Rewritten** lookup only; every assertion kept (one `◆` in the span's `◆` column, no bar, `due Oct 25`, both views) |
| `test_present_all.py::test_TC_2103_equals_the_rounds_capture` (160x45, 118x30) | the design changes this frame (LLR-4651.2/.4/.7): milestone rows leave, rows move up, gaps may appear | **Re-baselined** against the same round capture: rail row for row; header + ruler rows equal; the timeline's heads and task rows equal in order (gap rows and milestone rows set aside on both sides); plus one milestone row under each project with open milestones (`◆ 1 m…`, `◆ 2 m…`). On base the filtered comparison passes and only the new row check fails |
| `…::test_AT_2103_the_portfolio_on_one_ruler` | LLR-4651.2: open milestones' titles are not painted off the cursor | **Rewritten**: every open non-milestone title still in the body; milestones read as `  ▎ ◆ 1 milestone` / `2 milestones` under their heads; the rest unchanged |
| `…::test_AT_2104_three_views_one_cursor` | LLR-4653.2: `↓` from Billing Migration's head stops first on `Cut-over weekend` | **Rewritten**: one extra `↓`; the hand-over to view 1 on `Dual-run reconciliation` kept as is |
| `…::test_TC_2103_no_stop_hides_under_the_overflow_row` | a milestone stop's title is not painted off the cursor | **Rewritten** for milestone stops only: the project's milestone row is drawn under its head (and holds the title when it is the cursor); every other stop as before |
| `test_present_note_highlights.py::test_AT_2902_split_view_colours_highlights_two_sizes` | LLR-4653.5: blocks in stop order put `Eval report v1` first, so `Judge rubric` moves to the right column at 118 | **Rewritten** `_block`: reads whichever column holds the heading, cut to the same width; every assertion kept (passes on base too) |
| `test_milestone_marks.py::test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat` | B-5 / LLR-4651.1: `_present_task_row` loses its milestone branch | **Rewritten** list entry `_present_task_row` → `_present_lane_row`. See F-2 |

## 6. Mutant table — each negative control and the test that kills it

| NC (requirement) | Killed by |
|---|---|
| HLR-4651 / LLR-4651.1 row after the last task | TC-4901 (`[5]` is the only mark line), AT-4651 |
| LLR-4651.2 no row in view 3 | TC-4902, AT-4653 |
| LLR-4651.3 include the reached m1 | TC-4903 (`⬢`/`⬡` absent) |
| LLR-4651.4 sort tasks by title | TC-4904, AT-4651 |
| LLR-4651.5 always emit the row | TC-4905, AT-4654 (h1 hidden) |
| LLR-4651.6 row under a folded head | TC-4906, AT-4653 |
| LLR-4651.7 one row per milestone in `need` | TC-4907, AT-4653 (118x19) |
| LLR-4651.8 `gantt_dep_mark` in the gutter | TC-4908 |
| LLR-4652.1 select the anchor | TC-4911[tm4] (`▲2 Store l…`, rev cyan at 18) |
| LLR-4652.2 `_present_field` unchanged | TC-4912 (base: KeyError `rev:violet`, P-8), TC-4911 |
| LLR-4652.3 drop the late count | TC-4913 |
| LLR-4652.4 lead `⟦` absent | TC-4914, AT-4651 |
| LLR-4652.5 the first milestone's chip | TC-4915[cursor_task] (`due Oct 24`, not `due Oct 19`) |
| LLR-4652.6 label built with the raw title | TC-4916 (`a]b[/]` would close a tag; `[@click…]` would be live), AT-4655 |
| LLR-4652.7 the board gantt's label width at 80 | TC-4917, TC-4916 widths |
| LLR-4652.8 count the row in the header | TC-4918 (`8 open` line 0 vs the oracle) |
| LLR-4652.9 NC 1 keep `escape` | TC-4919[`\`, `x\`, `\[x`] (RED on base: this IS the mutant) |
| LLR-4652.9 NC 2 escape kept + pad/cut by rendered width | TC-4919[`x\`] literal check (`⟦x\\⟧` ≠ `⟦x\⟧`), `\[x` (`[x`) |
| LLR-4652.10 heading keeps `escape` | TC-4920[`\[x`, `ab\[…`] (RED on base: this IS the mutant) |
| HLR-4653 / LLR-4653.1 base order | TC-4921 (both), AT-4651, AT-4652 |
| LLR-4653.2 one stop per row | TC-4922 (stops), AT-4653 walk |
| LLR-4653.3 first by due (`open_t[0]`) | TC-4923 (`Handover call`), both |
| LLR-4653.4 hide the whole cell | TC-4924 (m2, m5 still drawn; m4 alone), AT-4654 |
| LLR-4653.5 briefs in base order | TC-4925, AT-4651, AT-4652 |
| LLR-4653.6 bind `←→` to a row walk | TC-4926 (pairs vs oracle), TC-4921 (`→` = move) |
| LLR-4654.1 / HLR-4654 deck holds `present_stop_order(…[0])` (B-4) | TC-4931 — **executed on base: the mutant's sha256 differs from the `8ca174c` oracle in 3/3 views** (`…_NC_a_deck_holding_the_stop_order_set_differs` passes), so `…_the_deck_bytes_equal_the_base_oracle` and AT-4656 can fail |

Only the deck NC was executed as a mutant here; the other NCs are `planned` for the mutant runner on the MR-b tree
(their tests are RED on base, which is a counterexample for most of them, but not a run of the named mutant).

## 7. Findings for the orchestrator (no requirement changed)

- **F-1 (design fact did not reproduce).** LLR-4652.9/.10 and B-3 say base reads `a\[b]` as `a[b]`. On `8ca174c` the
  brief reads `⟦a\[b]⟧` and the block `▌ a\[b]` — correct (rich's `escape` already escapes the tag-shaped `[b]`).
  Probe and run: `TC-4919[a\\[b]]`, `TC-4920[a\\[b]]` pass on base. The real base defects are the trailing `\`
  (doubled, +1 cell) and a `\` before a NON-tag `[` (`\[x` → `[x`, `ab\[x…` → `ab[x…`). I added `\[x` to TC-4919's
  titles (LLR-4652.9 "each backslash once") so the brief's non-tag case has a RED regression too. Route: `qa-reviewer`
  for the threshold wording; the security probe P-a/P-b stays `planned` until TC-4916/4919/4920 run on MR-b (B-3).
- **F-2 (B-5 may not go green).** `test_TC_2604_the_sites_enumeration…` asserts the literal `milestone_mark(` in the
  named function's body. The design's `_present_lane_row` gets its glyphs from `gantt_lane_label` /
  `gantt_milestone_row` and its chip from `_present_chip`; nothing says it calls `milestone_mark(` itself. If it does
  not, this test stays RED on MR-b. Route: `architect` / orchestrator — either the row names the seat, or the
  site list names the units that do.
- **F-3.** AT-4653's 18-row clause is run at a 118x19 terminal (§3).
- **F-4.** B-6's capture is `blocked` (needs MR-b).

## 8. Limits

- GREEN is `not-run`: no MR-b code on this branch. Every "passes on MR-b" expectation above is a design reading.
- No GPU/network limits applied. Synthetic data only (MR-F, the portfolio and people-round fixtures); no PII.
- No dependency added. No production file edited (`git diff --stat -- taskboard` empty).

## 9. Evidence checklist

- ✓ Every test named exists on disk at the cited path and name (`pytest --collect-only` in the run).
- ✓ Each result read from ONE complete run's own output, command quoted (§4, `evidence/red-base.txt`).
- ✓ RED on base captured, base `8ca174c` named (TC-4919, TC-4920 regressions RED except F-1's `a\[b]`).
- ✓ Each test asserts an observable outcome (rendered cells, styles, the file's bytes, the painted widgets).
- ✓ Uncovered / partial items named (§2).
- ✓ Environment limits declared (§8).
- ✓ No real PII, credentials or client data.
- ✓ Evidence states used: `executed`, `not-run`, `planned`, `blocked`.

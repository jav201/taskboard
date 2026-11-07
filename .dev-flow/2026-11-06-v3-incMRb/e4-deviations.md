# E4 — implementation deviations & smoke result (Inc MR-b, the presentation's milestone row)

Implementer: E4 (group V + group S). Design: `.dev-flow/2026-11-06-v3-incMRb/` graphs + requirements + rulings + e3 addenda (binding). MR-a's rulings R-1..R-8 apply where the presentation draws the same row.

## Files changed

- `taskboard/views.py` — group V (11 of the 12 slice units: `milestone_walk_key` + `gantt_plan`, `present_stop_order`, `_present_lane_row`, `_present_field`, `render_present`, `_all_plan`, `_all_layout`, `_all_timeline`, `_present_brief`, `_present_heading`, `_present_task_row`).
- `taskboard/app.py` — group S (1 unit: `PresentScreen._shown_ids` + the `present_stop_order` import).

No other file touched. `tests/` untouched. No git operations. No commit (the orchestrator commits).

## Units implemented (12/12)

| # | Unit | File | Change |
|---|---|---|---|
| 1 | `present_stop_order` | views.py | NEW — milestones in `milestone_walk_key` order, then the other open tasks in base order; pure (SEAM-2) |
| 2 | `milestone_walk_key` / `gantt_plan` | views.py | lifted the nested `walk_key` to module scope; `gantt_plan`'s one use calls it (MR-a frames byte-equal, verified: `test_milestone_row.py` + `test_gantt_milestones.py` 113/113) |
| 3 | `_present_lane_row` | views.py | NEW — label column (` ` + lead + `▎` + `gantt_lane_label(…, label_w - 3)`), blank gutter (LLR-4651.8), field from `gantt_milestone_row` painted by `_present_field`, chip (sel member, else first due ≥ today, else blanks) |
| 4 | `_present_field` | views.py | the three MR-a tones (`""`, `run:<tone>`, `rev:<style>`) paint as `_gantt_field` does (SEAM-8); every other cell as at base |
| 5 | `render_present` | views.py | `stops = present_stop_order(open_t)`; one `_present_lane_row` under the span; task rows over `stops[len(lane):]`; cursor fallback `stops[0]`; briefs/blocks over `stops` (A-4, SEAM-2) |
| 6 | `_all_plan` | views.py | each project's open list in stop order |
| 7 | `_all_layout` | views.py | `need` counts 1 milestone row; each milestone stop maps to the one milestone-row line; tasks each own a line |
| 8 | `_all_timeline` | views.py | head row, then one `_present_lane_row` directly under it, then the non-milestone task rows |
| 9 | `PresentScreen._shown_ids` | app.py | `present_stop_order(present_tasks_m(…)[0])` (SEAM-2); nothing else in app.py changed |
| 10 | `_present_brief` | views.py | RB-2/SEC-B1: title `c(_literal(txt), …)` in place of `c(escape(txt), …)`, `clip` first as before |
| 11 | `_present_heading` | views.py | SEC-B3: title `c(_literal(clip(…)), …)` in place of `escape` |
| 12 | `_present_task_row` | views.py | A-2: the `if task.milestone:` branch removed; both callers pass only non-milestones |

`present_deck_boards` / `present_tasks` / `present_tasks_m` / the keymap and hint rows are untouched on purpose (SEAM-6, R-2). MR-a's `gantt_milestone_row` / `gantt_lane_label` / `_lane_marks` are reused unchanged — no parameter, no branch.

## Deviations (nothing silent)

- **D-1 (B-5's test edit is the integrator's, not mine).** B-5 assigns the `tests/test_milestone_marks.py:153` mark-site rename (`_present_task_row` → `_present_lane_row`) to the **integrator**, and this E4 role is forbidden from touching `tests/`. The code side of B-5 is done (the `if task.milestone:` branch is removed; both `_present_task_row` callers pass only non-milestones). Note for the integrator: `_present_lane_row` delegates to the reused MR-a `gantt_lane_label` / `gantt_milestone_row`, so its body does not literally contain `milestone_mark(` — the census site needs to name the unit that routes through the seat, not a plain rename of the list entry.

## Smoke result

Import check: `C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard.app"` → **ok**.

`env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q tests/test_present.py tests/test_present_all.py` → **51 passed, 5 failed**.

## Tests failing by design (pin one row per milestone, not changed)

- `tests/test_present_all.py::test_TC_2103_equals_the_rounds_capture[size0-C-160-initial.svg]`
- `tests/test_present_all.py::test_TC_2103_equals_the_rounds_capture[size1-C-118-initial.svg]`
- `tests/test_present_all.py::test_AT_2103_the_portfolio_on_one_ruler` — a milestone's title is no longer a full field row, so not every open milestone title appears in the frame body (the row draws marks/dates, the title only when selected).
- `tests/test_present_all.py::test_AT_2104_three_views_one_cursor` — `↓` from a project head now lands on the first milestone in walk order (R-2), not the first due task.
- `tests/test_present_all.py::test_TC_2103_no_stop_hides_under_the_overflow_row` — a milestone stop's title is not in the drawn frame text (only its mark/date on the shared row).

These five are the re-baseline set for the two smoke files, per `01-requirements.md` §6 and `e3-addenda.md` B-9 (re-baseline one at a time, each citing the LLR that moves it).

## Additional by-design failures observed (outside the smoke scope, unchanged)

- `tests/test_present_milestone.py` — 11 tests (`test_TC_2101_a_milestone_row_is_its_date_not_a_bar[36/80/118/160-gantt/split]`, `test_TC_2101_a_start_date_does_not_make_a_milestone_a_bar`, `test_TC_2101_a_late_milestone_is_painted_over`, `test_AT_2101_the_cut_over_weekend_reads_as_a_milestone`). They assert base's "a milestone is a `◆` on its own row" (LLR-2101.1), which this increment replaces with the shared milestone row (HLR-4651).
- `tests/test_milestone_marks.py::test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat` — fails only because B-5's mark-site list edit is the integrator's step (D-1); the code routes through the seat via the reused MR-a units.

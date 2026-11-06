# E4 — integration (Inc MR-a, board gantt milestone row)

Integrator: software-dev. Inputs: build `09f8703` (`e4-deviations.md`), tests `74bc18c` (`e4-tests.md`).
Evidence states are the seven of `/dev-flow`.

## 1. Orchestrator rulings

- **I-1 — deviation D-3 NOT accepted.** `i/N` counts the milestones in the SAME CELL (R-6 F-1), not on the
  same due date: at k > 1 days per cell, different days share a cell. Fix the code; give
  `gantt_lane_label` the axis it needs, inside the graph's intent. D-1 and D-2 are accepted.
- **I-2 — F-T1.** If LLR-4603.1's m3/m5 examples cannot hold at 118 because of the fitted axis, amend
  the EXAMPLE (not the intent) to a feasible one with the same behaviour under test, in one ledger
  entry naming LLR-4603.1, and update the test. If they can hold, fix the code. Prove it by measurement.

## 2. How the rulings came out

**I-1 — code fixed (`impl`).** `taskboard/views.py`:
- `gantt_milestone_row`'s pass-1 bucketing (clamp to the edge cell, N-8 merge into the earlier mark)
  moved verbatim into `_lane_marks(lane, selected_id, board, ax, today) -> list[dict]`;
  `gantt_milestone_row` calls it, so its output is unchanged (every TC-48xx field test still GREEN).
- `gantt_lane_label` gains `ax: GanttAxis` (signature now
  `(lane, selected_id, board, ax, today, label_w)`; one caller, `_gantt_frame.task_row`). Its ` i/N`
  is the selected member's index in the `_lane_marks` record that holds it, so the mark's count, its
  lead and the tag count by ONE rule, as `01-requirements.md` "share one cell" requires. An undated
  member (no bucket) gets no tag.
- Graph note: `graph-proto-V.cw.md`'s `gantt_lane_label` `in:` gains `GanttAxis ax`; `func:` is
  unchanged in intent ("members that share its cell"). `_lane_marks` is a V-internal helper under the
  frozen `gantt_milestone_row` contract, which does not change. Not edited here (orchestrator's file).
- New test `test_TC_4827b_R6_i_of_n_counts_the_cell_not_the_day`: k = 2, m3/m4 (day 4) + a day-5
  milestone in one cell → mark `■3`, tags `1/3`, `2/3`, `3/3`. Mutant (the D-3 same-due rule put back):
  **`executed`, RED** (`AssertionError: ('tm3', ' ■ Steering go/no-go      1/2 ')`), then reverted.

**I-2 — example amended (the infeasible case applies).** Measurement `evidence/i2-measure.txt`
(`executed`, worktree package): at 118x30 the fitted axis is k = 0.5 from Oct 14, w = 79; m3 at cell 20,
m5 at cell 32. After `■2 ` there are 8 cells before the gap to m5, and the 17-cell `Steering go/no-go`
fits on neither side, so the field reads `■2 Steerin…` (LLR-4603.2's cut). m5 has 46 cells after it and
draws `★ Pilot launch` after its mark, so "m5 with no room after" is false. The axis is fitted by the
board, not by the selection: no code change makes the old example true without breaking the fit.
- Ledger: `LED-2026-11-06-incMR.7` names LLR-4603.1 only. New example: m5 selected → `Pilot launch`
  follows `★ `; a reached milestone due on the field's last day selected → its title ends one cell
  before `⬡✓`. The threshold line in `01-requirements.md` is updated to cite it.
- TC-4821 now asserts the m5 `after` case on Pilot rollout's row, plus its existing g2 `after` and
  `Final acceptance` `before` cases. NC (always after) stays RED on the `before` case.

## 3. GREEN-1 failures and their classes

GREEN-1 (`evidence/green-1.txt`): **5 failed, 323 passed**.

| # | Test | Class | Cause | Fix |
|---|---|---|---|---|
| 1 | `test_milestone_row.py::test_TC_4836_…_off_the_row_left_right_are_base` | test | `app.refresh_view()` after clearing the selection re-selects the first row's stop (`tm3`, the same pick `_select_first` makes), so `→` then walks the lane to `tm4` — correct LLR-4604.3 behaviour. The "no selection" precondition never reached the key. (Inferred from the trace `tm4 == tm3` and the GREEN after the fix.) | Drop the refresh; `→` now runs from a real no-selection state and must equal base `_select_first`. Assertion unchanged |
| 2–3 | `test_milestone_row_at.py::test_AT_4607_edges[size0/size1]` | test | The mark count included the `▲` of m2's late label `▲1d` (LLR-4603.4 label, not a mark): 7 ≠ 6 | Strip `▲<n>d` labels before counting. Still `== 6` |
| 4 | `test_gantt_milestones.py::test_AT_602_…` (80x24 half, not re-baselined by the tester) | test | `_select` walked only `↑/↓`; `tw5` (reached in the first half) is no longer its row's stop, so it is reachable only along the row | `_select` aims at the stop of `tid`'s lane (read from the shipped `gantt_lane`), then walks the row with `←/→`; non-milestone targets keep the base walk |
| 5 | `test_milestone_marks.py::test_TC_2604_the_sites_enumeration_…` | seam | The census sweep finds a new literal `◆` at `gantt_lane_label`'s at-rest column (`◆ <N> milestones`, LLR-4603.6). It is a count summary of a row, not one task's mark, so `milestone_mark(task, …)` cannot produce it; the design never listed the site for the census | Declared in `ALLOWED_LINES` with its LLR, as the guard's own message prescribes (the same kind as the declared legend entry). The sweep and every other check are untouched |

Plus the I-1 and I-2 changes (§2). No law guard or assertion was weakened: no assertion removed or
relaxed; one count was corrected to what it claims to count; one site was declared.

## 4. GREEN-2

`evidence/green-2.txt`: **329 passed, 0 failed** (328 of GREEN-1 + the new TC-4827b). Same 13 files:
`test_milestone_row.py`, `test_milestone_row_at.py`, the 5 re-baselined files (`test_boards_home.py`,
`test_gantt_milestones.py`, `test_legend.py`, `test_milestone_marks.py`, `test_milestone_offer.py`) and
the law guards (`test_colour_budget.py`, `test_colour_budget_app.py`, `test_english.py`,
`test_prism_laws.py`, `test_markup_census.py`, `test_modal_keys.py`). `evidence/green-1b.txt` is an
intermediate re-run (1 failed: row 4's first fix) kept for the record.

Note: the brief said "the 7 changed old test files"; commit `74bc18c` changes 5 old test files (plus 2 new
test files and 2 new support files). All of them are in the run.

`taskboard.__file__` = the worktree (`…\taskboard-wt\ms-row-proto\taskboard\__init__.py`), printed by
`python -c` from the same cwd as `python -m pytest` (both put cwd first on `sys.path`). The editable
install points at the main checkout: a script run from another directory imports THAT tree (it
happened once in the measurement probe and was re-run from the worktree).

## 5. Limits

- **Full suite: `not-run`** (the orchestrator's gate run, C-25). `gantt_lane_label`'s signature changed;
  `grep` finds no other caller in `taskboard/` or `tests/`.
- Mutant kills marked `planned` in `e4-tests.md` §6 are still `planned`, except the I-1 mutant above.
- Source files touched: 1 (`taskboard/views.py`). Tests: 5 files. Within the cap.

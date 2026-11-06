# E4 — implementation deviations & smoke result (Inc MR-a, board gantt milestone row)

Implementer: E4 (group V + group S). Design: `.dev-flow/2026-11-06-v3-incMR/` graphs + requirements + rulings + e3 addenda (binding).

## Files changed

- `taskboard/views.py` — group V (8 of 9 units + the interface nodes).
- `taskboard/app.py` — group S (1 unit: `action_hmove`).

No other file touched. `tests/` untouched. No git operations. No commit (the orchestrator commits).

## Units implemented (9/9)

| # | Unit | File | Change |
|---|---|---|---|
| 1 | `GanttGroup` | views.py | `lane: tuple = ()` field (SEAM-1) |
| 2 | `gantt_plan` | views.py | `_hide` first under `done_rows` (N-5, R-4); milestones leave `rows` for `lane` (walk order = due, then title, then id); `rows` = (stop,) + non-milestone rows in base order; stop = selected member else anchor (LLR-4604.2); fold budget counts the row as 1 |
| 3 | `gantt_milestone_row` | views.py | NEW — marks, clash count, `<hollow>✓`, `rev:<style>`, `◂`/`▸`, `w-2` shift (SEC-3), N-8 merge, pass 2 title, pass 3 dates, LABEL PATH (R-7) |
| 4 | `gantt_lane_label` | views.py | NEW — label column (LLR-4603.6/.7) |
| 5 | `gantt_lane` | views.py | NEW — the lane holding the selection (SEAM-3) |
| 6 | `_gantt_frame` | views.py | draws the shared row through `task_row` with a blank gutter (LLR-4601.8); `line_map` maps every lane id (SEAM-9); `drawn` gets `milestone`/`reached`; chip |
| 7 | `_gantt_field` | views.py | `rev:<style>` branch; label run painted as given, `""` paints nothing, no weekend shading on a run (N-9); docstring invariant amended (A-9) |
| 8 | `nav_model` (gantt) | views.py | **no code edit** — it already passes `done_rows=True`; its behaviour changes through `gantt_plan`'s new filter + collapse (R-4, N-5) |
| 9 | `TaskboardApp.action_hmove` | app.py | gantt branch walks the lane via `gantt_lane`; ends are no-ops; else base |

Call-site edits: `render_gantt` and `legend_entries` already pass `done_rows=True` — no change needed. `gantt_link_frame`, `gantt_link_order`, `_notify_folded` leave the flag off (verified: link mode still draws one row per milestone, R-3/LLR-4606.1).

## Deviations (nothing silent)

- **D-1 (nav_model is a no-op edit).** The slice counts `nav_model` as a changed unit, but its source already calls `gantt_plan(..., done_rows=True)`. The R-4/N-5 fix lands entirely inside `gantt_plan` (which now applies `_hide` under `done_rows`), so `nav_model` needs no textual change. Verified by test: with class Review hidden, `nav_model` no longer contains the hidden milestones.
- **D-2 (TC-4821's example wording vs the fitted window).** The graph example "118x30, m3 selected → `Steering go/no-go` starts one cell after `■2`" and "m5 … with no room after" is not literal under the real fitted axis: at 118x30 the window is `k=0.5` (m3 at cell 20, m5 at cell 32), so only 8 cells lie after `■2` and the 17-cell title is cut to `Steering…` — exactly what the variant-A oracle `lane_cells` and LLR-4603.2 produce. The full-title-after and rightmost-no-room-after label cases are reachable at layer 0 on an explicit `GanttAxis` with matching room; the implementer followed the func description and the oracle, not the literal example text.
- **D-3 (`gantt_lane_label` i/N).** "i/N of the members that share its cell" is operationalised as same `due_date` (the variant-A oracle `lane_label`), because the function signature has no axis. Same-cell-by-clamp and same-day coincide for every fixture milestone.

## Smoke result

`env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q tests/test_gantt_milestones.py`

→ **26 passed, 3 failed.** Import check `python -c "import taskboard.app"` passes.

## Tests failing by design (one row per milestone, not changed)

- `tests/test_gantt_milestones.py::test_TC_609_nav_walks_the_drawn_rows_in_draw_order[size0]` (118x30)
- `tests/test_gantt_milestones.py::test_TC_609_nav_walks_the_drawn_rows_in_draw_order[size1]` (80x24)
- `tests/test_gantt_milestones.py::test_AT_602_milestones_read_as_dates_reached_ones_quiet_the_ruler_marks_them`

All three pin the base "one milestone per row" board gantt and are the re-baseline set for this smoke file (per `01-requirements.md` §6 and `e3-addenda.md` A-4).

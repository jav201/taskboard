# E2 seams — Inc MR-a (board gantt milestone row)

There are 2 groups. **V** owns `taskboard/views.py` (`graph-proto-V.cw.md`), and **S** owns `taskboard/app.py` (`graph-proto-S.cw.md`). The frozen contracts are in `graph-interfaces.cw.md`. An implementer proposes a seam change to the orchestrator and never changes a seam alone.

| Seam | Contract | Producer → consumer | Pinned by |
|---|---|---|---|
| SEAM-1 `GanttGroup.lane` | new NamedTuple field, default `()`. It holds the group's drawn milestones in walk order, and it is set only when `done_rows` | V `gantt_plan` → V `_gantt_frame`/`task_row`, V `gantt_lane` | TC-4802, TC-4851 |
| SEAM-2 `GanttGroup.rows` | under `done_rows`, `rows` = (stop,) + the non-milestone rows in base order. The stop is the selected lane member, else the anchor. Without `done_rows`, as base | V `gantt_plan` → V `_gantt_frame` (pages, D8), V `nav_model`; unchanged readers `gantt_link_order` (reads `open`) and S `_notify_folded` (flag off) | TC-4803, TC-4832, TC-4854 |
| SEAM-3 `gantt_lane(board, show_archived, selected_id, today, focus=None) -> tuple[Task, ...]` | the lane that holds the selection, over the hidden-class-filtered board, in walk order; `()` otherwise. S passes `_view_board()`, so the `/` query is already applied | V → S `action_hmove` | TC-4833, TC-4836, TC-4843 |
| SEAM-4 the gantt nav column (`nav_model("gantt", …)`) | one column, one id per milestone row (the stop), built over `_hide(board)` (R-4) | V `nav_model` → S `_nav_columns` → `action_cursor` | TC-4831, TC-4843b, TC-4843c |
| SEAM-5 `selected_task_id` | after `←→` it can name a non-anchor lane member. V's plan makes that member the stop, so it stays in the nav column and in `line_map` | S `action_hmove` writes → V `gantt_plan` reads; unchanged readers `action_details`, `]`, `e`, `action_link` | TC-4837, TC-4838, TC-4852 |
| SEAM-6 the board-gantt flag = `done_rows` | set by `render_gantt`, `legend_entries`, `nav_model` (gantt) and `gantt_lane`; off in `gantt_link_frame`, `gantt_link_order` and `_notify_folded`. No new parameter | V internal; S `_notify_folded` relies on it being off | TC-4851, TC-4853 |
| SEAM-7 `gantt_milestone_row(lane, selected_id, board, ax, today) -> cells` and `gantt_lane_label(lane, selected_id, board, today, label_w) -> str` | the row's field cells, with the tone `rev:<style>` for the selected mark, and its label column. Inc MR-b reuses both unchanged (R-1) | V → V `task_row`; later MR-b `_present_task_row` | TC-4811..TC-4827 |
| SEAM-8 cell tone `rev:<style>` | `_gantt_field` paints it as reverse + bold in `HEX[<style>]` | V `gantt_milestone_row` → V `_gantt_field` | TC-4815 |
| SEAM-9 `line_map` | every lane id maps to the milestone row's line | V `_gantt_frame` → S (`_line_map`, read only in the chain map today) | TC-4801 |

**Cross-group ATs** (one tester): AT-4603, AT-4604, AT-4605 and AT-4606 cross SEAM-3, SEAM-4 and SEAM-5. AT-4601, AT-4602 and AT-4607 are V only.

**Open for E3** (findings F-1..F-5 in `graph-proto-V.cw.md`):
- F-1: the LLR-4603.3 statement disagrees with its own threshold on shared-cell dates.
- F-2: the LLR-4602.1 hue disagrees with the `mut` that the seat gives.
- F-3: AT-4607's `▸` cannot be reached for an open milestone.
- F-4: the slice grows from 6 units to 8 (`_gantt_field`, `gantt_lane`).
- F-5: the milestones' dependency gutter is lost on the shared row.

**R-5:** HLR-4606 is split in place into HLR-4606.1 (link mode) and HLR-4606.2 (pages), in LED-2026-11-06-incMR.3. No LLR, TC or AT id changes.

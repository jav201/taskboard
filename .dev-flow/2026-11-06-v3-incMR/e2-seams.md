# E2 seams — Inc MR-a (board gantt milestone row)

There are 2 groups. **V** owns `taskboard/views.py` (`graph-proto-V.cw.md`), and **S** owns `taskboard/app.py` (`graph-proto-S.cw.md`). The frozen contracts are in `graph-interfaces.cw.md`. An implementer proposes a seam change to the orchestrator and never changes a seam alone.

| Seam | Contract | Producer → consumer | Pinned by |
|---|---|---|---|
| SEAM-1 `GanttGroup.lane` | new NamedTuple field, default `()`. It holds the group's drawn milestones in walk order, and it is set only when `done_rows` | V `gantt_plan` → V `_gantt_frame`/`task_row`, V `gantt_lane` | TC-4802, TC-4851 |
| SEAM-2 `GanttGroup.rows` | under `done_rows`, `rows` = (stop,) + the non-milestone rows in base order. The stop is the selected lane member, else the anchor. Without `done_rows`, as base | V `gantt_plan` → V `_gantt_frame` (pages, D8), V `nav_model`; unchanged readers `gantt_link_order` (reads `open`) and S `_notify_folded` (flag off) | TC-4803, TC-4832, TC-4854 |
| SEAM-3 `gantt_lane(board, show_archived, selected_id, today, focus=None) -> tuple[Task, ...]` | the lane that holds the selection, over the hidden-class-filtered board (filtered inside `gantt_plan`, N-5), in walk order; `()` otherwise. S passes `_view_board()`, so the `/` query is already applied | V → S `action_hmove` | TC-4833, TC-4836, TC-4843 |
| SEAM-4 the gantt nav column (`nav_model("gantt", …)`) | one column, one id per milestone row (the stop), built over the class-filtered board that `gantt_plan` gives under `done_rows` (R-4, N-5) | V `nav_model` → S `_nav_columns` → `action_cursor` | TC-4831, TC-4843b, TC-4843c |
| SEAM-5 `selected_task_id` | after `←→` it can name a non-anchor lane member. V's plan makes that member the stop, so it stays in the nav column and in `line_map` | S `action_hmove` writes → V `gantt_plan` reads; unchanged readers `action_details`, `]`, `e`, `action_link` | TC-4837, TC-4838, TC-4852 |
| SEAM-6 the board-gantt flag = `done_rows` | set by `render_gantt`, `legend_entries`, `nav_model` (gantt) and `gantt_lane`; off in `gantt_link_frame`, `gantt_link_order` and `_notify_folded`. No new parameter | V internal; S `_notify_folded` relies on it being off | TC-4851, TC-4853 |
| SEAM-7 `gantt_milestone_row(lane, selected_id, board, ax, today) -> cells` | the row's field cells, with the tone `rev:<style>` for the selected mark and each field label as ONE escaped run (R-7, LABEL PATH). Inc MR-b reuses it unchanged (R-1). `gantt_lane_label` is V-internal, and MR-b may adopt it (N-6). MR-b invariant: the board gantt's frames stay byte-equal | V → V `task_row`; later MR-b `_present_task_row` | TC-4811..TC-4825, TC-4818, TC-4820 |
| SEAM-8 cell tone `rev:<style>` and the field label run | `_gantt_field` paints `rev:` as reverse + bold in `HEX[<style>]`; it paints a label run (cut by `fit`, escaped once, whole, by `_literal`, upstream) as given and never splits it; `""` paints nothing | V `gantt_milestone_row` → V `_gantt_field` | TC-4815, TC-4820 |
| SEAM-9 `line_map` | every lane id maps to the milestone row's line | V `_gantt_frame` → S (`_line_map`, read only in the chain map today) | TC-4801 |

**Cross-group ATs** (one tester): AT-4603, AT-4604, AT-4605 and AT-4606 cross SEAM-3, SEAM-4 and SEAM-5. AT-4601, AT-4602 and AT-4607 are V only.

**Ruled in E3 round 1** (`00-e1-rulings.md` R-6 to R-8; LED-2026-11-06-incMR.4, .5, .6):
- F-1 to F-5: closed by R-6 (see the decisions in `graph-proto-V.cw.md`).
- SEC-1, N-1, SEC-2: closed by R-7. The escape happens before the cells are laid (LABEL PATH and the `fit` → `_literal` → `[Data: field label run]` → `_gantt_field` edges in `graph-interfaces.cw.md`), and LLR-4603.11 is the negative control.
- SEC-3 (LLR-4602.8), N-2 (AT-4606), N-5 (filter in `gantt_plan`), N-6 (SEAM-7) and N-7 (tones): in the requirements or the graph. N-3, SEC-5 (TC-4843d), N-4 and the E4 checks: in `e3-addenda.md`.

**R-5:** HLR-4606 is split in place into HLR-4606.1 (link mode) and HLR-4606.2 (pages), in LED-2026-11-06-incMR.3. No LLR, TC or AT id changes.

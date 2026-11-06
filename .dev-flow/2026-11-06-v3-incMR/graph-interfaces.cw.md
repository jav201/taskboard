# Code-Wire prototype — Inc MR-a — the shared interfaces (frozen)

The contracts that the two file groups share. Only the differences from `graph-baseline.cw.md` (59775bb) appear here. Owners: **V** = `taskboard/views.py` (graph-proto-V.cw.md) and **S** = `taskboard/app.py` (graph-proto-S.cw.md). V implements every node in this file. S calls `gantt_lane` and reads the nav column. `gantt_milestone_row` and `gantt_lane_label` are also the one interface that Inc MR-b (the presentation) reuses (00-e1-rulings.md §2). An agent proposes a change in this file and never changes an interface alone.

Example sources are the TC and AT ids of `01-requirements.md`: LLR-460h.n maps to TC-(4800 + 10·(h−1) + n). No run is recorded yet. The fixture is MR-F (`prototypes/milestone_row/proto.py:70-99`), with today 2026-10-20. Milestones and tasks are named by the fixture's keys (`m3`, `store`), and the board's ids are `t<key>`. Walk order: due (no due last), then title, then id. Anchor: the first milestone in walk order that is open with a due on or after today, else the first open one, else the first.

## Nodes

gantt_lane
req: LLR-4604.3, LLR-4604.4, LLR-4604.5, LLR-4604.6, LLR-4605.3
in: Board board; bool show_archived; str? selected_id; date today; str? focus = None
out: tuple[Task, ...] lane
func: the drawn milestones of the board-gantt milestone row that holds `selected_id`, in walk order, over `board` with the hidden classes left out (`_hide` when `_hidden_class_ids(board)`); `()` when `selected_id` is None or not on a milestone row. Reads the `lane` of `gantt_plan(board, show_archived, selected_id, today, 10 ** 6, focus, done_rows=True)`: the members do not depend on the fold budget. S passes `_view_board()`, so the `/` query is already applied
module: taskboard/views.py
examples: (TC-4833) MR-F, selected "m3" → lane ["m1", "m2", "m3", "m4", "m5"] (m3 before m4 on Oct 24: `Steering…` < `Store…`)
examples: (TC-4843) class Review hidden, selected "m1" → lane ["m1", "m4", "m5"]: m2 and m3 are not drawn, so they are not walked
examples: (TC-4843) the `/store` board (`filtered_board`), selected "m4" → lane ["m4"]
examples: (TC-4836) selected "store" (a task) → `()`; selected None → `()`

gantt_milestone_row
req: LLR-4602.1, LLR-4602.2, LLR-4602.3, LLR-4602.4, LLR-4602.5, LLR-4602.6, LLR-4602.7, LLR-4603.1, LLR-4603.2, LLR-4603.3, LLR-4603.4, LLR-4603.5
in: tuple[Task, ...] lane; str? selected_id; Board board; GanttAxis ax; date today
out: list[tuple[str, str]] cells
func: the milestone row's field: `ax.w` cells of (glyph, tone) for `_gantt_field`. Pass 1 draws the marks, one per occupied cell. A lone milestone is `<glyph>` in its class style (`milestone_mark`). A reached milestone alone is `<hollow>` + `✓` in `reached`. 2–9 milestones in one cell are `<glyph><N>`, and 10 or more are `<glyph>+`; the glyph is the selected one's when it is among them, else the first's in walk order. The selected mark's tone is `rev:<style>`. A due before or after the window puts `◂` or `▸` in the edge cell and the mark in the next cell inward. No due draws no mark. Pass 2 draws the selected one's label: the full title one blank cell after its mark, else before it; when neither side has room, the title cut with `…` on the roomier side if that side has 6 cells or more; else no title. Pass 3 draws the other marks' labels left to right: `Mon D` (or `▲Nd` in `over` when late) one blank cell beside the mark, only where it fits whole. No label covers a mark, another label or the field's edges
module: taskboard/views.py
oracle: prototypes/milestone_row/proto.py `lane_cells` (variant A, the round's visual oracle) and the A captures in prototypes/milestone_row/out/png/
examples: (TC-4811) MR-F, nothing selected → g1 `▲` tone `cyan`, g2 `■` tone `violet`, h1 `◆` tone `mut` (no class: the seat's `mut`, see finding F-2 in graph-proto-V), i1 `⬢` tone `amber`, each at `ax.cell(due)`
examples: (TC-4812) m3 + m4 on Oct 24, nothing selected → `■2` (m3 first in walk order); m4 selected → `▲2`, the `▲` tone `rev:cyan`
examples: (TC-4813) 10 milestones on one day → `<glyph>+` in 2 cells; the cell right after `+` is unchanged
examples: (TC-4814) m1 (Payment, reached, alone) → `⬡✓`, the `✓` tone `reached`
examples: (TC-4815) m2 selected → m2's cell tone `rev:violet`; m1, m3/m4 and m5 tones carry no `rev:`
examples: (TC-4816) a reached milestone 40 days back → `◂` at cell `0`, `<hollow>` at cell `1`, its `✓` at cell `2`; a milestone due after the window → `<glyph>` at cell `w-2`, `▸` at cell `w-1`
examples: (TC-4817) a milestone with no due beside one dated milestone → `1` mark in the field; no exception
examples: (TC-4821) 118x30, m3 selected → `Steering go/no-go` starts one cell after `■2`; m5 (rightmost) selected with no room after → `Pilot launch` ends one cell before `★`
examples: (TC-4822) 118x30, m2 selected → `Rubric…` between m2's `■` and the `■2`; marks 4 cells apart → no title cell (3 cells < 6)
examples: (TC-4823) 118x30, nothing selected on Pilot rollout → `Oct 24` beside `■2`, `Oct 30` beside `★`; Eval harness → `Oct 21`, `Oct 28`
examples: (TC-4824) m2 not selected → `▲1d` in tone `over` beside m2's mark; `Oct 19` absent from the row
examples: (TC-4825) every row of the AT-4601..AT-4603 scenes at 118 and 80 → every mark cell still holds its mark; label spans disjoint and one cell clear of any mark
examples: (AT-4601) Pilot rollout at rest, 118 → `⬡✓`, `■ ▲1d`, `■2 Oct 24`, `★ Oct 30`
examples: (AT-4607) a milestone after the window, one with no due and 10 on one day on one row → `▸`, no mark for the undated one, `<glyph>+`

gantt_lane_label
req: LLR-4603.6, LLR-4603.7
in: tuple[Task, ...] lane; str? selected_id; Board board; date today; int label_w
out: str label
func: the milestone row's label column, padded to `label_w`. While no lane member is selected: ` ◆ <N> milestones` (`milestone` when N = 1) at `label_w` 24 or more, else ` ◆ <N> ms`, then ` ▲<L>` in `over` when L ≥ 1 members are late. While a member is selected: its `<glyph>` in its style, its title (`title_markup`, cut to the column), and ` <i>/<N>` in `mut` when it is the i-th of N members on its day; the tag is kept and the title is cut first
module: taskboard/views.py
examples: (TC-4826) 118, nothing selected → Eval harness `◆ 2 milestones`, Docs & handover `◆ 1 milestone`; 80 → Pilot rollout `◆ 5 ms ▲1`
examples: (TC-4827) m2 selected → `■ Rubric sign-off`; m4 selected at 118 → `▲ Store list frozen 2/2`; at 80 the title is cut with `…` and the label still ends `2/2`
examples: (AT-4603) m3 selected at 118 → `■ Steering go/no-go 1/2`

## Entities

[Data: GanttGroup.lane]
in: tuple[Task, ...]
desc: NEW field of `GanttGroup` (default `()`): the group's drawn milestones in walk order. These are base's milestone rows (the open ones and, while the group has open work, the reached and not-archived ones, D-606). It is set only when `done_rows` (the board gantt); with `done_rows` False it stays `()` and `rows` stays as base. V writes it (`gantt_plan`). V reads it (`_gantt_frame`, `task_row`, `gantt_lane`), and S reads it through `gantt_lane`

[Data: GanttGroup.rows]
in: tuple
desc: CHANGED under `done_rows`. When `lane` is not empty, `rows` = (stop,) + the non-milestone rows in base order (open by due, then the done tail). The stop is the lane member `selected_id` names, else the lane's anchor. So the row is one entry: one `↑↓` stop, one row of the fold budget and of a page. Without `done_rows`, `rows` is as base (the link mode, `gantt_link_order`, `_notify_folded`)

[Data: gantt nav column]
in: list[list[str]]
desc: `nav_model("gantt", …)`: ONE column of every `g.rows` id in draw order, folded groups included as base, so each milestone row is one id (the stop). CHANGED (R-4): it is built over the board without hidden classes, the board that `_gantt_frame` draws. `TaskboardApp._nav_columns` → `action_cursor` reads it

## Edges

gantt_plan ──▶ [Data: GanttGroup.lane]
gantt_plan ──▶ [Data: GanttGroup.rows]
[Data: GanttGroup.lane] ──▶ gantt_lane
[Data: GanttGroup.lane] ──▶ gantt_milestone_row
when: through `_gantt_frame.<locals>.task_row`, the lane of the row's group
[Data: GanttGroup.lane] ──▶ gantt_lane_label
when: through `_gantt_frame.<locals>.task_row`
nav_model ──▶ [Data: gantt nav column]
[Data: gantt nav column] ──▶ TaskboardApp.action_cursor
gantt_lane.lane ──▶ TaskboardApp.action_hmove

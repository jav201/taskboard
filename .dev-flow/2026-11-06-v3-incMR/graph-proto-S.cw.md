# Code-Wire prototype — Inc MR-a — group S, `taskboard/app.py`

Only the differences from `graph-baseline.cw.md` (59775bb) appear here. S changes one unit, `action_hmove`. `action_cursor` keeps its code, but its gantt behaviour changes through the nav column (a frozen interface in `graph-interfaces.cw.md`). It is listed here so that the `↑↓` examples have an owner. Sources, fixture MR-F, walk order and anchor are as in `graph-interfaces.cw.md`. Today is 2026-10-20 (the fixture pins `date`).

Unchanged on purpose: `_nav_columns`, `_view_board` (the `/` query only; `gantt_plan` applies the hidden classes, N-5), `action_details`, the task keys (`]`, `e`, …), `action_link` and `GanttLinkMode`. These all read `selected_task_id`, and after a walk that id is the walked milestone, not the anchor.

## Nodes

TaskboardApp.action_hmove
req: LLR-4604.3, LLR-4604.4, LLR-4604.5, LLR-4604.6, LLR-4604.7, LLR-4604.8, LLR-4605.3, LLR-4606.2
in: int delta
out: None
func: CHANGED. In the gantt view (`view_mode == "gantt"`), it computes `lane = gantt_lane(self._view_board(), self.show_archived, self.selected_task_id, date.today(), self.focused_project_id)`. When the lane holds the selection, it selects `lane[i + delta]` when that index exists and repaints; at either end it does nothing (no wrap, no other group). Otherwise, and in every other view, it does exactly what base does
module: taskboard/app.py
modify: [Data: TaskboardApp.selected_task_id] (replace)
examples: (TC-4833, root action_hmove) m3 selected, `→` → "m4" (same day, after m3 in walk order); `→` → "m5"
examples: (TC-4834, root action_hmove) m3 selected, `←` → "m2"; `←` → "m1"
examples: (TC-4835, root action_hmove) m1 selected, `←` → "m1"; m5 selected, `→` → "m5"; `0` exceptions; no other group's milestone selected
examples: (TC-4836, root action_hmove) the gantt with "store" selected, `←`/`→` → "store"; kanban `→` → the next column's first task (base); the gantt with no selection → base `_select_first`
examples: (TC-4837, root action_hmove) m3, `→`, `enter` → `TaskDetails` of "m4"
examples: (TC-4838, root action_hmove) m3, `→`, `]` → m4's phase "Next" → "Doing", m3's unchanged; m3, `→`, `e` → the editor holds `Store list frozen`
examples: (TC-4843, root action_hmove) class Review hidden, m1 selected, `→` → "m4", `→` → "m5"; `/store` `enter`, m4 selected, `←`/`→` → "m4"
examples: (TC-4852, root action_hmove) m3, `→` (m4), `L` → the link frame's waiter is "m4"
examples: (AT-4603, root action_hmove) from m3: `→` → m4 (`▲2`, `2/2`); `→` → m5; `→` → m5; `←`×4 → m1; `←` → m1
examples: (AT-4604, root action_hmove) m3, `→`, `enter` → details of m4; `esc`, `]` → m4 one phase on; `↓` → `Pilot store list`; `←`/`→` → no change
examples: (AT-4605, root action_hmove) `/store` `enter` → Pilot rollout's row holds m4 only, `→` keeps m4; `esc` the query, hide class Review in `#` → the row holds m1, m4, m5; `→` from m1 → m4
examples: (AT-4606, root action_hmove) m3, `→`, `L` → the link frame draws one row per drawn milestone (m1..m5), byte-equal to base, waiter m4; `esc` → milestone rows back, m4 selected

TaskboardApp.action_cursor
req: LLR-4604.1, LLR-4604.2, LLR-4605.3
in: int delta
out: None
func: UNCHANGED code. The gantt behaviour changes through the nav column: each milestone row is one id (the stop), so `↑`/`↓` stop on the row once. The stop that `↑` or `↓` lands on is the anchor, because the column was built with the selection not on the row; the next plan then picks that milestone as the stop
module: taskboard/app.py
modify: [Data: TaskboardApp.selected_task_id] (replace)
examples: (TC-4831, root action_cursor) MR-F, "store" selected, `↑` → a Pilot rollout milestone ("m3"); `↑` → no move (Pilot rollout is the first group); `↓`, `↓` → "tele"
examples: (TC-4832, root action_cursor) `↑` onto Pilot rollout's row → "m3" (m1 reached, m2 late); onto a row of only late milestones → its first; onto a row of only reached ones → its first
examples: (TC-4843d, root action_cursor) m3 selected, hide class Review in `#` → the selection leaves m3; `↑` → base `_select_first` (`action_hmove` likewise: `gantt_lane` gives `()`), `0` exceptions; `enter` and `]` do not act on m3; neither the label column nor the ruler echo shows m3 (N-3, SEC-5)
examples: (AT-4603, root action_cursor) from `Pilot store list`, `↑` → m3 selected, its title beside `■2`, the label column `■ Steering go/no-go 1/2`, chip `in 4d`

## Entities

[Data: TaskboardApp.selected_task_id]
in: str?
desc: CHANGED in meaning, not in type. In the gantt it can now name a lane member that is not the anchor (after `←→`). `gantt_plan` makes that member the stop, so the nav column and `line_map` both hold it, and `enter`, `]`, `e` and `L` act on it

[Outside: keys ←→]
desc: KEYMAP `hmove(-1)` / `hmove(1)`, unchanged; in the board gantt they now walk the selected milestone's row

## Edges

[Outside: keys ←→] ──▶ TaskboardApp.action_hmove
when: the main screen is on top; walks a lane only in the gantt with a lane member selected
gantt_lane.lane ──▶ TaskboardApp.action_hmove
TaskboardApp.action_hmove ──▶ [Data: TaskboardApp.selected_task_id]
when: the lane holds the selection and `lane[i + delta]` exists
[Data: gantt nav column] ──▶ TaskboardApp.action_cursor
TaskboardApp.action_cursor ──▶ [Data: TaskboardApp.selected_task_id]

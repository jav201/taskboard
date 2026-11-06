# Code-Wire prototype — Inc MR-a — the shared interfaces (frozen)

The contracts that the two file groups share. Only the differences from `graph-baseline.cw.md` (59775bb) appear here. Owners: **V** = `taskboard/views.py` (graph-proto-V.cw.md) and **S** = `taskboard/app.py` (graph-proto-S.cw.md). V implements every node in this file. S calls `gantt_lane` and reads the nav column. `gantt_milestone_row` is also the one interface that Inc MR-b (the presentation) reuses (00-e1-rulings.md §2). `gantt_lane_label` is V-internal (graph-proto-V.cw.md), and MR-b may adopt it (N-6). MR-b's invariant: the board gantt's frames stay byte-equal. An agent proposes a change in this file and never changes an interface alone.

Example sources are the TC and AT ids of `01-requirements.md`: LLR-460h.n maps to TC-(4800 + 10·(h−1) + n), except LLR-4603.11 → TC-4820. No run is recorded yet. The fixture is MR-F (`prototypes/milestone_row/proto.py:70-99`), with today 2026-10-20. Milestones and tasks are named by the fixture's keys (`m3`, `store`), and the board's ids are `t<key>`. Walk order: due (no due last), then title, then id. Anchor: the first milestone in walk order that is open with a due on or after today, else the first open one, else the first. *Share one cell* and *lead*: as in `01-requirements.md` §1 (one rule for the count, the lead and ` i/N`).

## Nodes

gantt_lane
req: LLR-4604.3, LLR-4604.4, LLR-4604.5, LLR-4604.6, LLR-4605.3
in: Board board; bool show_archived; str? selected_id; date today; str? focus = None
out: tuple[Task, ...] lane
func: the drawn milestones of the board-gantt milestone row that holds `selected_id`, in walk order, over `board` with the hidden classes left out by `gantt_plan` itself (N-5: the class filter's one seat; `gantt_lane` applies none of its own); `()` when `selected_id` is None or not on a milestone row. Reads the `lane` of `gantt_plan(board, show_archived, selected_id, today, 10 ** 6, focus, done_rows=True)`: the members do not depend on the fold budget. S passes `_view_board()`, so the `/` query is already applied
module: taskboard/views.py
examples: (TC-4833) MR-F, selected "m3" → lane ["m1", "m2", "m3", "m4", "m5"] (m3 before m4 on Oct 24: `Steering…` < `Store…`)
examples: (TC-4843) class Review hidden, selected "m1" → lane ["m1", "m4", "m5"]: m2 and m3 are not drawn, so they are not walked
examples: (TC-4843) the `/store` board (`filtered_board`), selected "m4" → lane ["m4"]
examples: (TC-4836) selected "store" (a task) → `()`; selected None → `()`

gantt_milestone_row
req: LLR-4602.1, LLR-4602.2, LLR-4602.3, LLR-4602.4, LLR-4602.5, LLR-4602.6, LLR-4602.7, LLR-4602.8, LLR-4603.1, LLR-4603.2, LLR-4603.3, LLR-4603.4, LLR-4603.5, LLR-4603.11
in: tuple[Task, ...] lane; str? selected_id; Board board; GanttAxis ax; date today
out: list[tuple[str, str]] cells
func: the milestone row's field: `ax.w` cells of (glyph, tone) for `_gantt_field`. Pass 1 draws the marks, one per occupied cell. A lone milestone is `<glyph>` in its class style (`milestone_mark`). A reached milestone alone is `<hollow>` + `✓` in `reached`. 2–9 milestones that share one cell are `<glyph><N>`, and 10 or more are `<glyph>+`; members are bucketed by the cell each is DRAWN in (an off-window one in its edge-side cell), and the glyph is the cell's lead's. The count digit and `+` are `bright` beside the selected glyph, else in the class style (N-7). The selected mark's tone is `rev:<style>`. A due before or after the window puts `◂` or `▸` in the edge cell and the mark (1 or 2 cells) in the cells next inward: `◂<hollow>✓`, `<hollow>✓▸`, `<glyph>2▸`. A 2-cell mark whose cell is `w-1` starts at `w-2` (SEC-3). No due draws no mark. Pass 2 draws the selected one's label in `bright` (N-7): the full title one blank cell after its mark, else before it; when neither side has room, the title cut on the roomier side if that side has 6 cells or more; else no title. Pass 3 draws the other marks' labels left to right: the lead's `Mon D` one blank cell beside the mark, only where it fits whole, in `reached` when the lead is reached, in `soon` when its due is today, else in `mut`; a late lead's `▲Nd` in `over` (E5 F6, the variant-A oracle `proto.py:258`). No label covers a mark, another label or the field's edges. LABEL PATH (R-7; SEC-1, SEC-2, N-1), the same for every label (title, date, `▲Nd`), in this order: (1) room is measured in cells (`vis`/`cell_len`), never `len`; (2) the PLAIN label is cut with `fit`, which counts cells and ends a cut in `…`; (3) the cut piece is escaped ONCE, as a whole, with `_literal`; (4) only then is it laid into the field: the label's first cell holds the whole escaped run in the tone `run:<tone>` (E5 C-5), and each of the next `cell_len` of the PLAIN cut label minus 1 cells holds the consumed glyph `""` (E5 F4: not the escaped run's `cell_len`, which counts `\[` as 2); a label of 0 cells is not laid at all (SEC-6), which `_gantt_field` paints as nothing. A label is never split into per-character cells, and no cell ever holds an unescaped label character. Occupancy and the one-cell gap count cells
module: taskboard/views.py
oracle: prototypes/milestone_row/proto.py `lane_cells` (variant A, the round's visual oracle) and the A captures in prototypes/milestone_row/out/png/
examples: (TC-4811) MR-F, nothing selected → g1 `▲` tone `cyan`, g2 `■` tone `violet`, h1 `◆` tone `mut` (no class: the seat's `mut`, R-6 F-2), i1 `⬢` tone `amber`, each at `ax.cell(due)`
examples: (TC-4812) m3 + m4 on Oct 24, nothing selected → `■2` (m3 first in walk order); m4 selected → `▲2`, the `▲` tone `rev:cyan`
examples: (TC-4813) 10 milestones on one day → `<glyph>+` in 2 cells; the cell right after `+` is unchanged
examples: (TC-4814) m1 (Payment, reached, alone) → `⬡✓`, the `✓` tone `reached`
examples: (TC-4815) m2 selected → m2's cell tone `rev:violet`; m1, m3/m4 and m5 tones carry no `rev:`
examples: (TC-4816) a reached milestone 40 days back (before `ctx`) → `◂` at cell `0`, `<hollow>` at cell `1`, its `✓` at cell `2`; a reached milestone due 90 days ahead, in a group with open work → `<hollow>` at cell `w-3`, `✓` at `w-2`, `▸` at `w-1`; two reached ones after the window → `<glyph>2▸` in the last three cells, never two marks on one cell
examples: (TC-4818) a reached milestone alone, due on the window's last day → `<hollow>` at cell `w-2`, `✓` at `w-1`; two reached ones sharing that cell → `<glyph>2` at `w-2`–`w-1`; `len(cells)` = `w`; no exception
examples: (TC-4817) a milestone with no due beside one dated milestone → `1` mark in the field; no exception
examples: (TC-4821) 118x30, m3 selected → `Steering go/no-go` starts one cell after `■2`; m5 (rightmost) selected with no room after → `Pilot launch` ends one cell before `★`
examples: (TC-4822) 118x30, m2 selected → `Rubric…` (the `fit` cut, 7 cells) between m2's `■` and the `■2`; marks 4 cells apart → no title cell (3 cells < 6)
examples: (TC-4823) 118x30, nothing selected on Pilot rollout → `Oct 24` beside `■2` (its lead m3's date), `Oct 30` beside `★`; Eval harness → `Oct 21`, `Oct 28`
examples: (TC-4824) m2 not selected → `▲1d` in tone `over` beside m2's mark; `Oct 19` absent from the row
examples: (TC-4825) every row of the AT-4601..AT-4603 scenes at 118 and 80 → every mark cell still holds its mark; label spans disjoint and one cell clear of any mark
examples: (TC-4820) m3 selected, its title `a]b[/]` → the label's first cell holds `_literal("a]b[/]")` and the next `5` cells hold `""`; the frame parses through `collapse_runs` + `Text.from_markup`, and its plain text holds `a]b[/]`
examples: (TC-4820) titles `[@click=app.quit]x`, `x\`, `里程碑 frozen`, `e\u0301tape`, each after, before and cut → `0` exceptions; plain = the title or its `fit` cut; `0` spans with `@click` or meta; every line's `cell_len` = width; `15`/`15`
examples: (TC-4820) `里程碑 frozen` cut to 8 cells → `fit` gives `里程碑 …` (`cell_len` 8), one run in its first cell and `7` consumed cells; the row is `w` cells
examples: (AT-4601) Pilot rollout at rest, 118 → `⬡✓`, `■ ▲1d`, `■2 Oct 24`, `★ Oct 30`
examples: (AT-4607) in a group with open work, a reached milestone due 90 days ahead, one with no due and 10 on one day on one row → `<hollow>✓▸` in the last three cells, no mark for the undated one, `<glyph>+`


## Entities

[Data: GanttGroup.lane]
in: tuple[Task, ...]
desc: NEW field of `GanttGroup` (default `()`): the group's drawn milestones in walk order. These are base's milestone rows (the open ones and, while the group has open work, the reached and not-archived ones, D-606). It is set only when `done_rows` (the board gantt); with `done_rows` False it stays `()` and `rows` stays as base. V writes it (`gantt_plan`). V reads it (`_gantt_frame`, `task_row`, `gantt_lane`), and S reads it through `gantt_lane`

[Data: GanttGroup.rows]
in: tuple
desc: CHANGED under `done_rows`. When `lane` is not empty, `rows` = (stop,) + the non-milestone rows in base order (open by due, then the done tail). The stop is the lane member `selected_id` names, else the lane's anchor. So the row is one entry: one `↑↓` stop, one row of the fold budget and of a page. Without `done_rows`, `rows` is as base (the link mode, `gantt_link_order`, `_notify_folded`)

[Data: field label run]
in: str
desc: NEW (R-7). One field label (title, date or `▲Nd`) after LABEL PATH steps 1–3: cut in cells by `fit`, then escaped once, whole, by `_literal`. It sits in the label's first cell; the cells it covers hold `""`. The only non-constant glyph `_gantt_field` ever receives

[Data: gantt nav column]
in: list[list[str]]
desc: `nav_model("gantt", …)`: ONE column of every `g.rows` id in draw order, folded groups included as base, so each milestone row is one id (the stop). CHANGED (R-4): it is built over the board without hidden classes, the board that `_gantt_frame` draws. The filter is applied inside `gantt_plan` when `done_rows` (N-5), so `nav_model` applies none of its own. `TaskboardApp._nav_columns` → `action_cursor` reads it

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
gantt_milestone_row ──▶ fit
when: LABEL PATH steps 1–2: room in cells, the PLAIN label cut with `…`
fit ──▶ _literal
when: step 3: the cut piece escaped once, as a whole, BEFORE any cell is written
_literal ──▶ [Data: field label run]
[Data: field label run] ──▶ _gantt_field
when: step 4: one run in the label's first cell, `""` in the cells it covers; never one cell per character

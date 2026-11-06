# Code-Wire prototype — Inc MR-a — group V, `taskboard/views.py`

Only the differences from `graph-baseline.cw.md` (59775bb) appear here. The nodes are the views.py units this increment changes. V also implements the interface nodes `gantt_lane`, `gantt_milestone_row` and `gantt_lane_label`, whose contracts are frozen in `graph-interfaces.cw.md` and are not repeated here. Sources, fixture MR-F, walk order and anchor are as in `graph-interfaces.cw.md`.

The board-gantt flag is `done_rows`, as in the prototype (`proto.py` `plan_m`). No new parameter. `render_gantt`, `legend_entries`, `nav_model` (gantt) and `gantt_lane` set it. `gantt_link_frame`, `gantt_link_order` and `_notify_folded` leave it off, and their output stays as base (R-3).

Unchanged on purpose: `render_gantt`, `legend_entries`, `gantt_window`, the ruler, `gantt_milestone_cells` (still the presentation's and the link frame's), `gantt_link_order`, `gantt_link_frame` and `gantt_link_overlay`.

## Nodes

gantt_plan
req: LLR-4601.2, LLR-4601.3, LLR-4601.4, LLR-4601.5, LLR-4601.7, LLR-4604.1, LLR-4604.2, LLR-4605.1, LLR-4606.1
in: Board board; bool show_archived; str? selected_id; date today; int body_rows; str? focus = None; str? previous = None; str? pinned = None; bool done_rows = False
out: list[GanttGroup] groups
func: CHANGED under `done_rows`. First it builds base's rows. Then, per group, the milestones leave those rows for `lane` (walk order). `rows` = (stop,) + the non-milestone rows in base order, with the stop being the lane member that `selected_id` names, else the lane's anchor; with no member, no stop. The fold budget and the pressure loop then count `len(rows)`, so the row costs 1. Without `done_rows`, everything is as base, and `lane` is `()`
module: taskboard/views.py
examples: (TC-4802) MR-F → lane sizes Pilot rollout `5` (reached m1 kept: the group has open work), Eval harness `2`, Docs & handover `1`, Inbox `1`
examples: (TC-4802) a group with only reached milestones and no open work → lane `()` and no stop (D-606)
examples: (TC-4803) MR-F, selected "store" → Pilot rollout rows ["m3", "store", "tele", "train", "rota"]; add a done, not-archived task "d1" → rows end "d1"
examples: (TC-4804) MR-F → the Inbox group (project None) lane ["i1"], rows ["i1", "ip"]; no project's lane holds "i1"
examples: (TC-4805) a group with no milestone; one whose every milestone is archived; one with only reached milestones and no open work → lane `()`, rows = its tasks only
examples: (TC-4807) MR-F, body of 80x24 → `0` groups folded (base folds 1 or more); body of 118x30 → `0` folded, `14` rows + `4` span rows = `18`
examples: (TC-4832) selected "store" → Pilot rollout stop "m3" (m1 reached, m2 late); a lane of only late milestones → its first; a lane of only reached ones → its first; selected "m4" → stop "m4"
examples: (TC-4841) the `/store` filtered board → Pilot rollout lane ["m4"]; Eval harness, Docs & handover and the Inbox lanes `()`
examples: (TC-4851) `done_rows` `False` (the link frame) → every lane `()`; Pilot rollout rows hold m1..m5 as five entries, as base

_gantt_frame
req: LLR-4601.1, LLR-4601.6, LLR-4603.9, LLR-4603.10, LLR-4605.2, LLR-4606.3, LLR-4606.4
in: Board board; bool show_archived; str? selected_id; date? today = None; int width = 68; int height = 0; dict? line_map = None; int tick = 0; str? focus = None; str? previous = None; str? pinned_id = None; bool done_rows = False
out: tuple(list[str] lines, set[str] drawn, list[GanttGroup] groups, GanttAxis ax)
func: CHANGED. It draws each group's stop through `task_row`, which draws the milestone row there: directly under the span row, because the stop is the first entry of `rows`. In `line_map`, every lane id maps to the row's line. The paged branch is unchanged: it pages by `rows` index, and a selected lane member is the stop, so the page that holds the selection holds the row. The D8 branch is unchanged: `task_row(sel)` draws the milestone row. `_hide` runs first as base, so a hidden class's milestones are not in any lane
module: taskboard/views.py
examples: (TC-4801) MR-F at 118x30 → `4` milestone rows, each the line right after its span row; no other body line holds a milestone mark; `line_map` "m1".."m5" all equal Pilot rollout's row line
examples: (TC-4806) MR-F at 118x12 → each folded group's span row is followed by the next span row; ≥ `1` folded group
examples: (TC-4829) every frame of AT-4601..AT-4607 at 118x30 and 80x24 → max `cell_len` per line ≤ width; `14`/`14` frames
examples: (TC-4830) MR-F at 118x30 → `drawn` holds "milestone"; with m1 on the row it holds "reached"; the legend reads `◆ milestone`
examples: (TC-4842) class Review hidden in `#` → Pilot rollout's row draws m1, m4, m5; the Oct 24 cell is `▲` with no count
examples: (TC-4853) `L` then `esc` → the frame equals the frame before `L`; `L`, a candidate, `enter` → `4` milestone rows again (no state survives the link frame: the plan is a pure function of `done_rows`)
examples: (TC-4854) one group of a milestone row + 20 tasks at 118x14, the cursor on the last task, `↑` until the row → the page starts with the milestone row and the hint reads `▼ 13 below` (body 10 with the strip, page of 8; the hint counts task rows off the page)
examples: (AT-4601) MR-F at 118x30 → body `18` rows (base 23); at 80x24 → `0` folded groups; no line wider than the terminal
examples: (AT-4602) MR-F at 118x12 → folded groups show only their span row; a group with no milestone draws no milestone row
examples: (AT-4606) a paged group, `↑` onto its milestone row → the page holding the row

_gantt_frame.<locals>.task_row
req: LLR-4603.8, LLR-4606.5
in: Task t
out: str row
func: CHANGED. When `t` is the stop of an unfolded group's lane (an id → group map built once per frame), it returns `row(gantt_lane_label(lane, selected_id, board, today, label_w), " ", gantt_milestone_row(lane, selected_id, board, ax, today), chip)`. The chip is `gantt_milestone_chip` of the selected member, else of the anchor when it is open with a due on or after today, else `chip_w` blanks. The gutter is blank (finding F-5). It adds "milestone" to `drawn` when an open member has a mark, and "reached" when a reached one does; `row` adds "beyond" for `◂`/`▸` as base. Any other `t` is drawn as base
module: taskboard/views.py
examples: (TC-4828) m2 selected → chip `▲1d`; nothing on Pilot rollout selected → `in 4d` (m3); a row whose only members are late → blank chip
examples: (TC-4855) MR-F at 118x6 (body 2: D8, groups > body), m3 selected → Pilot rollout's span row, then the milestone row: label `■ Steering go/no-go 1/2`, the `■2` mark in tone `rev:violet`
examples: (AT-4603) m3 selected → chip `in 4d`

_gantt_field
req: LLR-4602.5
in: list[tuple[str, str]] cells; GanttAxis ax; frozenset[int] guides; frozenset[int] weekends = frozenset()
out: str markup
func: CHANGED. A tone `rev:<style>` paints its glyph in reverse video and bold, in `HEX[<style>]`. Every other tone paints as base. This is the one place where the selected mark's reverse is drawn; no HEX key is registered at run time (the prototype's `_skey` did that)
module: taskboard/views.py
examples: (TC-4815) the cell (`■`, `rev:violet`) → markup `[b reverse <HEX violet>]■[/]`; the cell (`■`, `violet`) → base `c("■", "violet")`

nav_model
req: LLR-4604.1, LLR-4605.3
in: str mode; Board board; bool show_archived; date? today = None; int width = 68; int height = 0; str? selected_id = None; str kanban_sort = "project"; str kanban_group = "project"; bool kanban_collapsed = False; str? kanban_focus = None; str? gantt_focus = None; str presentation = "grouped"; str focus_presentation = "cards"; TeamState? team_state = None; str team_filter = "equipo"
out: list[list[str]] cols
func: CHANGED, gantt branch only (R-4). The board passes through `_hide` when `_hidden_class_ids(board)`, the same board `_gantt_frame` draws, before `gantt_plan(..., done_rows=True)`. The column is still every `g.rows` id in draw order, so each milestone row is one id: its stop. Every other mode is as base
module: taskboard/views.py
examples: (TC-4831) MR-F, selected "store" → gantt `[["m3", "store", "tele", "train", "rota", "g1", "gq", "gr", "gx", "h1", "ha", "hr", "i1", "ip"]]`: one stop per milestone row
examples: (TC-4843b) the test_legend fixture with class "payment" hidden, 118x30 → the column holds none of "tc8", "tcc", "tce" (RED on base: P-10, R-4)
examples: (TC-4843c) MR-F with class Review hidden, selected "store" → Pilot rollout's stop is "m4" (m3 is hidden), the one the frame draws

## Findings

finding F-1 LLR-4603.3's statement leaves out shared cells, but its threshold and AT-4601 date one
anchor: gantt_milestone_row
seen: the statement says "each milestone that is not selected, not late and not part of a shared cell". Its threshold lists `Oct 24`, and Oct 24 is the m3 + m4 cell. AT-4601 reads `■2 Oct 24`, and the oracle (`proto.py` `lane_cells`) dates a shared cell by its lead
cause: the statement's exclusion contradicts its own threshold
effect: a test written from the statement and a test written from the threshold disagree on the `■2` cell
decision: the graph follows the threshold, AT-4601 and the oracle: a shared cell gets its lead's date (or `▲Nd`). E3 rules on correcting the statement; the requirement is not changed here

finding F-2 LLR-4602.1 asks for h1's `◆` in its project hue, but the seat gives `mut`
anchor: gantt_milestone_row
seen: `milestone_mark` returns `◆` in `mut` for an unset class (P-8, baseline), and the oracle draws through that seat
cause: the threshold names a colour that no seat produces
effect: TC-4811 would assert a hue that the code and the oracle do not draw, or force a second colour channel outside the seat
decision: the graph keeps the seat (`mut`). E3 rules on whether the threshold is corrected to `mut`

finding F-3 an open milestone 90 days ahead never draws `▸` in the board gantt
anchor: gantt_milestone_row
seen: `gantt_window` puts every OPEN due inside the window (`hi = max(open dues) + margin`). LLR-4602.6's open milestone 90 days ahead and AT-4607's "a milestone 90 days ahead" therefore draw inside the field, through `render_gantt`
cause: the window is fitted to the open work, so only a reached milestone due after the open work (done early) can fall to the right
effect: AT-4607's `▸` is not reachable black-box as written; TC-4816 is reachable only at layer 0 with an explicit `GanttAxis`
decision: the graph keeps the `▸` rule. E3 rules on rewriting AT-4607 with a reached milestone due after the window, or on keeping `▸` as a layer-0-only check

finding F-4 the slice grows from 6 units to 8
anchor: _gantt_field
seen: the selected mark's reverse needs a tone that `_gantt_field` paints, and `action_hmove` needs the filtered lane without re-deriving the plan
cause: the slice named neither the painter nor a lane accessor
effect: two more views.py units: `_gantt_field` (changed, one branch) and `gantt_lane` (new, an interface). The change is still 2 source files
decision: designed as such; E3 confirms. The alternative to `_gantt_field` is a static `sel-<colour>` table in HEX built at import

finding F-5 the dependency gutter of milestones is lost on the shared row
anchor: _gantt_frame.<locals>.task_row
seen: base draws `gantt_dep_mark` (`↳` waits or early) in the gutter of each milestone row. The oracle's shared row has a blank gutter, and one gutter cell cannot name which of N marks waits
cause: no requirement states the gutter of the shared row
effect: a milestone that waits loses its `↳` in the board gantt, and the legend no longer adds "waits" or "early" for it. The link mode still shows it (one row each, R-3)
decision: the graph follows the oracle (blank gutter). E3 rules: keep it blank, or show the stop's mark

## Edges

[Data: GanttGroup.lane] ──▶ _gantt_frame.<locals>.task_row
[Data: GanttGroup.rows] ──▶ _gantt_frame
[Data: GanttGroup.rows] ──▶ nav_model
[Data: Task.mark] ──▶ nav_model
when: a class is hidden (R-4: `_hide` before the plan)
[Data: TaskboardApp.selected_task_id] ──▶ gantt_plan
when: picks the stop: the selected lane member, else the anchor
_gantt_frame.<locals>.task_row ──▶ gantt_lane_label
_gantt_frame.<locals>.task_row ──▶ gantt_milestone_row
_gantt_frame.<locals>.task_row ──▶ _gantt_field

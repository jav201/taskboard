# Code-Wire baseline — milestone rows in the board's gantt, the presentation's gantt-based views, the gantt nav and `hmove`, and the link mode's pin at 59775bb

Baseline of the code that Inc MR (a project's milestones share one gantt row, variant A, D1–D3) touches, as the code is at commit 59775bb (marks tree `taskboard-wt/incMR-marks`). No design and no proposal: only what the code does now. Every node has `req: to trace`: the requirements of this increment are written in parallel. Example sources are test ids (file::test) of the current suite, or a probe `P-n` run on 59775bb (values printed by the probe, listed in baseline-notes.md). The probes import `taskboard` from incMR-marks (`taskboard.__file__` printed). The probe board is the suite's own `kg_board.milestones(kg_board.build())` (today 2026-09-30): projects pweb, pmob, papi, pdwh, pops; milestones tw0 (pweb, reached, Sep 18), tw5 (pweb, Oct 10), tm5 (pmob, Nov 4), ta3 (papi, Oct 3), td0 (pdwh, Oct 18), to0 (pops, late, Sep 28). P-9 adds tw7 "Press kit", a second pweb milestone on tw5's day. Today every milestone is its own row: the shared row of variant A does not exist yet.

## Nodes

gantt_plan
req: to trace
in: Board board; bool show_archived; str? selected_id; date today; int body_rows; str? focus = None; str? previous = None; str? pinned = None; bool done_rows = False
out: list[GanttGroup] groups
func: THE seat of what the gantt draws and in what order (the renderer and `nav_model` read it): one group per visible project (only `focus` when set) plus the Inbox group (None) for loose tasks when not focused; `rows` = open work and, while the group has open work, its reached milestones merged by due (each milestone ONE row), then with `done_rows` the done non-milestone tasks at the tail; unfold order: the selection's group, the `pinned` group (link mode), then by pressure while all of a group's rows fit `body_rows - len(groups)`
module: taskboard/views.py
examples: (P-1) the probe board, body `1000000`, `done_rows` `True` → pweb rows ["tw0", "tw2", "tw3", "tw4", "tw5", "tw6", "tw1"] (tw0 reached and tw5 are milestones, each its own row); pops rows start "to0"
examples: (P-1) body `12`, selected "tw5" → pweb unfolded `True` with `7` rows; pmob, papi, pdwh, pops folded
examples: (P-9) tw7 on tw5's day → pweb rows ["tw0", "tw2", "tw3", "tw4", "tw5", "tw7", "tw6", "tw1"]: two same-day milestones, two rows
examples: (test_gantt_milestones.py::test_TC_609_rows_merge_reached_milestones_by_due_while_open_work_remains) reached milestones merged among the open rows by due
examples: (test_gantt_milestones.py::test_TC_609_a_group_with_only_reached_milestones_draws_no_row) a group with only reached milestones draws no row

_gantt_frame
req: to trace
in: Board board; bool show_archived; str? selected_id; date? today = None; int width = 68; int height = 0; dict? line_map = None; int tick = 0; str? focus = None; str? previous = None; str? pinned_id = None; bool done_rows = False
out: tuple(list[str] lines, set[str] drawn, list[GanttGroup] groups, GanttAxis ax)
func: the gantt frame: `_hide` first (hidden classes), the head, the two-row ruler (the selected project's due `◆` and its milestones' marks on the month row, first drawn wins a same-day cell), the legend strip, then the body: per group its span row and, when unfolded, one `task_row` per entry of `g.rows`; when the span rows alone fill the body, the page of groups holding the selection plus "+N not shown"; a group taller than its room is paged around the selection (else the pin) with the "▲ N above / ▼ N below" hint; with a pin and a selection in two groups that cannot both fit, the pinned group gets half the rows left; `line_map` gets task id → line
module: taskboard/views.py
examples: (P-3) the probe board at 118x30, selected "tw5" → `30` lines, `19` tasks mapped; milestone lines tw0 `4`, tw5 `8`, ta3 `15`, to0 `21`; no "not shown"
examples: (P-3) at 80x24 → `24` lines, `13` mapped; milestone lines tw0 `4`, tw5 `8`, to0 `15`
examples: (test_gantt_board.py::test_TC_106_nav_is_the_plans_rows_and_every_selection_is_drawn) every selection is drawn at every height
examples: (test_gantt_polish.py::test_AT_205_a_long_project_says_how_much_is_off_the_page) the page hint names the rows above and below

_gantt_frame.<locals>.task_row
req: to trace
in: Task t
out: str row
func: one body row: a milestone is ` <glyph> <title> ` (glyph and style from `milestone_mark`; a reached title in `reached`), the dependency gutter, `gantt_milestone_cells` on the field and `gantt_milestone_chip` (`in Nd`, `today`, `▲Nd`, `✓ done`); a done task a quiet `_gantt_done_bar` row with `✓`; open work a `_gantt_bar` with its due chip; adds what it drew to `drawn` ("milestone", "reached", …)
module: taskboard/views.py
examples: (P-3) tw5 at 118 → " ◆ Launch new homepage", "◆ Oct 10", chip "in 10d"; tw0 → " ◇ Mockups approved", "◇✓ Sep 18", "✓ done"; to0 → "◆ Sep 28", "▲2d"
examples: (P-9) tw5 and tw7 → two rows, both "◆ Oct 10" in the same field cell
examples: (test_gantt_milestones.py::test_TC_610_a_milestone_title_paints_literally) a milestone title with markup characters paints literally

render_gantt
req: to trace
in: Board board; bool show_archived; str? selected_id; date? today = None; int width = 68; int height = 0; dict? line_map = None; int tick = 0; str? focus = None; str? previous = None
out: Text text
func: the board's gantt view: `_gantt_frame(..., done_rows=True)` and the one-line legend when a row is spare; never passes `pinned_id`
module: taskboard/views.py
examples: (P-3) the probe board 118x30 selected "tw5" → `30` lines, milestone rows at lines `4`, `8`, `15`, `21`
examples: (test_gantt_milestones.py::test_TC_611_the_legend_names_milestones_right_after_the_selection) the legend names milestones right after the selection, at 118x30 and 80x24

gantt_milestone_cells
req: to trace
in: Task task; Board board; GanttAxis ax; date today
out: list[tuple[str, str]] cells
func: one milestone's field, `ax.w` cells: its mark on its date (`✓` after it when reached), its `Mon D` after it, or before it when it does not fit; off the window the edge glyph and the mark beside it; no due or a field under 3 cells → blank; the date tone `reached`, `over` (the seat's chip `▲Nd`), `soon` on the day, else `mut`; one task per call, never a bar
module: taskboard/views.py
examples: (P-8) tw5 on the probe axis (width `79`) → "◆ Oct 10" starting at cell `26`
examples: (test_gantt_milestones.py::test_TC_610_cells_hold_one_diamond_and_its_date_and_never_a_bar) one diamond and its date, never a bar
examples: (test_gantt_milestones.py::test_TC_610_a_reached_milestone_on_the_last_column_keeps_its_day) on the last column the mark keeps its day and drops the `✓`

milestone_mark
req: to trace
in: Task task; Board board; date today
out: tuple(str glyph, str style, str chip)
func: THE seat every milestone mark renders through: the class shape and colour (an unset or unknown class `◆` in `mut`); reached → the hollow twin and chip "✓"; late → chip "▲Nd"; else chip ""
module: taskboard/views.py
examples: (P-8) tw5 → ("◆", "mut", ""); tw0 (reached) → ("◇", "mut", "✓"); to0 (late) → ("◆", "mut", "▲2d")
examples: (test_milestone_marks.py::test_TC_2604_the_seats_truth_table) the seat's truth table

nav_model
req: to trace
in: str mode; Board board; bool show_archived; date? today = None; int width = 68; int height = 0; str? selected_id = None; str kanban_sort = "project"; str kanban_group = "project"; bool kanban_collapsed = False; str? kanban_focus = None; str? gantt_focus = None; str presentation = "grouped"; str focus_presentation = "cards"; TeamState? team_state = None; str team_filter = "equipo"
out: list[list[str]] cols
func: the cursor's columns per view; the gantt branch: body = `height - 1 - GANTT_RULER_ROWS`, `gantt_plan(..., done_rows=True)` and ONE column of every `g.rows` id in draw order (every milestone its own stop, folded groups included); it does not apply `_hide`; kanban, chainmap and the swimlanes grid give several columns; agenda, focus, people, swimlanes (waves) one; flow, standup, setup none
module: taskboard/views.py
examples: (P-2) the probe board, width `118`, height `0` → gantt `1` column of `31` ids holding the `6` milestones; kanban `5` columns (no milestone); chainmap `4` columns; agenda `1`; swimlanes `1`; flow, standup, setup `0`
examples: (P-10) the legend fixture with class "payment" hidden, 118x30 → the gantt column still holds "tc8", "tcc", "tce", which `render_gantt` does not map
examples: (test_gantt_milestones.py::test_TC_609_nav_walks_the_drawn_rows_in_draw_order) nav walks the drawn rows in draw order

TaskboardApp._nav_columns
req: to trace
in:
out: list[list[str]] cols
func: `nav_model(view_mode, _view_board(), …)` at the viewport's height and the board's width: the one question the renderer answered; `_view_board` is the `/` search's `filtered_board` in kanban and gantt
module: taskboard/app.py
examples: (test_kanban_milestones.py::test_TC_612_a_milestone_selection_moves_to_a_drawn_card) the selection moves to a drawn card when it is not in the columns

TaskboardApp.action_cursor
req: to trace
in: int delta
out: None
func: `↑`/`↓` (KEYMAP cursor, priority): within the selection's column of `_nav_columns`, one step, no move off the ends; in the gantt every row, milestones included, is a stop; not found → `_select_first`
module: taskboard/app.py
modify: [Data: TaskboardApp.selected_task_id] (replace)
examples: (test_gantt_board.py::test_AT_102_down_walks_the_drawn_open_work) down walks the drawn open work

TaskboardApp.action_hmove
req: to trace
in: int delta
out: None
func: `←`/`→` (KEYMAP hmove(-1)/hmove(1), priority, group nav): the first task of the nearest non-empty column that way; no such column → no-op; not located → `_select_first`. In the gantt (one column) it never moves the selection; in kanban, chainmap and the swimlanes grid it changes column; in agenda, focus, people and swimlanes waves it does nothing; check_action holds it while another screen is on the stack
module: taskboard/app.py
modify: [Data: TaskboardApp.selected_task_id] (replace)
examples: (P-2) gantt `1` column → `→` has no column to reach (code read; no pilot run)
examples: (test_app.py::test_right_moves_to_next_column_first_task) kanban: `right` lands on the next column's first task

TaskboardApp.action_link
req: to trace
in:
out: None
func: `L`: nothing without a selected task; in the gantt pushes `GanttLinkMode(board, task, show_archived, today)`, else the `LinkPicker`; the result goes to `_on_link_picked`
module: taskboard/app.py
examples: (test_gantt_link.py::test_TC_512_link_mode_keeps_the_waiters_group_open) in the gantt `L` opens the link mode on the chart

gantt_link_order
req: to trace
in: Board board; bool show_archived; date today; str? previous = None
out: list[Task] cands
func: the link mode's candidate cycle: `gantt_plan` with every group unfolded, each group's OPEN rows in draw order; an open milestone is a candidate, a reached one is not
module: taskboard/views.py
examples: (P-5) the probe board → starts ["tw2", "tw3", "tw4", "tw5", "tw6", "tm6"]; holds "tm5", "ta3", "td0", "to0"; no "tw0"

gantt_link_frame
req: to trace
in: Board board; bool show_archived; Task waiter; Task? cand; date today; int width; int height; str right; set[str] loops
out: tuple(Text text, dict facts)
func: the gantt as the link mode paints it: `_gantt_frame` with the candidate as the selection, the waiter's group as `previous` and the waiter's id as `pinned_id` (the pin), the head "◆ GANTT · LINK", `⟲` on loop rows, `gantt_link_overlay` draws the link between the waiter's row and the candidate's row through `line_map`
module: taskboard/views.py
examples: (test_gantt_link.py::test_TC_512_one_page_holds_both_when_it_can) one page holds the waiter and the candidate when it can
examples: (test_gantt_link.py::test_TC_511_loop_rows_wear_the_mark_in_the_gutter) loop rows wear `⟲` in the gutter

GanttLinkMode.action_move
req: to trace
in: int delta
out: None
func: `↑`/`↓` in the link mode: the next allowed candidate (not a loop, matching the typed filter), cycling; repaints; `←`/`→` are not bound
module: taskboard/modals.py
modify: [Data: GanttLinkMode state] (replace)
examples: (test_gantt_link.py::test_TC_512_the_cycle_skips_loops_and_follows_the_filter) the cycle skips loops and follows the filter

_hide
req: to trace
in: Board board
out: Board proxy
func: a shallow board proxy without the milestones of hidden classes; `_gantt_frame` applies it at its entry; the board itself is never touched
module: taskboard/views.py
examples: (test_legend.py::test_TC_2608_hide_drops_the_class_from_the_gantt_and_the_board_is_untouched) the payment milestones leave the gantt; a save still writes them

present_tasks_m
req: to trace
in: Board board; str? project_id
out: tuple(list[Task] open_tasks, list[Task] tasks)
func: `present_tasks` (the shown tasks, open first) without hidden-class milestones; open milestones are among the open tasks, so views 1/2 and 3 draw them; reached ones are not open and draw no field row
module: taskboard/views.py
examples: (P-6) pweb → open ["tw2", "tw3", "tw4", "tw5", "tw6"] (tw5 the open milestone; tw0 reached left out)
examples: (test_legend.py::test_TC_2608_present_tasks_m_drops_hidden_classes_and_none_hidden_is_identity) hidden-classed milestones leave both lists

_present_task_row
req: to trace
in: Task task; Board board; _PresentGeo p; bool cursor = False
out: str row
func: one presentation field row: a milestone as the gantt draws it, ` ▎ <glyph> <title>`, `gantt_milestone_cells` on the field (the cursor recolours the mark cells `accent` and leads with `⟦`), its due alone in the chip; other tasks a bar, the cursor as `⟦━⟧`
module: taskboard/views.py
examples: (P-6) tw5 in view 1 at 118x30 → "▎ ◆ Launch new homepage", "◆ Oct 10", chip "due Oct 10"
examples: (test_present_milestone.py::test_TC_2101_a_milestone_row_is_its_date_not_a_bar) a milestone row is its date, not a bar

render_present
req: to trace
in: Board board; str? project_id; str? cursor_id; date today; int width; int height; str view = "gantt"; int scroll = 0
out: Text frame
func: views 1 (`gantt`) and 2 (`split`): head, ruler (the project's due only, no milestone marks), span row, one `_present_task_row` per open task (each milestone a row and a cursor stop), a rule; then view 1 lists each open task's brief (milestones included) and the cursor's note, view 2 a block per open task; below 36 columns one narrow line
module: taskboard/views.py
examples: (P-6) pweb 118x30 → the field row of tw5, and its brief "Launch new homepage" with "in 10d"
examples: (test_present_milestone.py::test_TC_2101_a_late_milestone_is_painted_over) a late milestone is painted `over`

_all_plan
req: to trace
in: Board board
out: list[tuple[Project, list[Task]]] plan
func: view 3's projects: each shown project in `present_order` with its shown open tasks (`present_tasks_m`), open milestones included
module: taskboard/views.py
examples: (P-7) the probe board → pweb first, its tasks include "tw5"

_all_layout
req: to trace
in: list plan; str? cur_pid; frozenset folded; int room
out: tuple(dict open_, bool gap, list stops, dict rows)
func: view 3's layout: hand folds stay; while rows overflow the projects furthest from the cursor's fold to their header; stops in screen order: ("proj", id) then ("task", id) per drawn row, one per milestone
module: taskboard/views.py
examples: (test_present_all.py::test_TC_2103_the_frame_sweep) the stops are the drawn rows, no duplicate

_all_timeline
req: to trace
in: Board board; int width; int height; date today; tuple? cur; frozenset folded; bool rail_focus
out: tuple(list[str] lines, list stops, tuple? cur)
func: view 3's timeline: head, ruler, per project a header row and, when open, one `_present_task_row` per task in the project's hue; the overflow row drops what it covers from the stops; a cursor not among the stops falls to its project's header, else the last or first stop
module: taskboard/views.py
examples: (P-7) the probe board at 118x30 → stops start ["pweb", "tw2", "tw3", "tw4", "tw5", "tw6", "pmob"]; "pops" is a stop, its tasks are cut by the overflow row

render_present_all
req: to trace
in: Board board; tuple? cursor; date today; int width; int height; frozenset folded = frozenset(); bool rail_focus = False
out: PresentAll all
func: view 3 (`all`): below 36 the narrow frame; below `PRESENT_RAIL_MIN` (100) the timeline alone; else the 24-cell rail, `│` and the timeline; returns the frame, the timeline, its width, the stops, the rail stops and the drawn cursor
module: taskboard/views.py
examples: (P-7) the probe board at 118x30 → the stops hold "tw5", "tm5", "ta3", "td0" (each milestone its own stop)
examples: (test_present_all.py::test_TC_2103_no_stop_hides_under_the_overflow_row) no stop hides under the overflow row

PresentScreen.action_move
req: to trace
in: int delta
out: None
func: `↑`/`↓` in `R`: in view 3 the next stop of `_stops()` (clamped); in views 1/2 the next shown open task (clamped), the note scroll reset; nothing while narrow
module: taskboard/app.py
modify: [Data: PresentScreen state] (replace)
examples: (test_present_all.py::test_AT_2104_three_views_one_cursor) three views, one cursor

PresentScreen.action_side
req: to trace
in: int delta
out: None
func: `←`/`→` in `R`: in view 3 with the rail drawn (width 100+) moves the focus between the rail and the timeline (a task cursor becomes its project on the rail); anywhere else the same as `action_move(delta)`, so in views 1/2 and in a rail-less view 3 `←→` step through rows, milestones included
module: taskboard/app.py
modify: [Data: PresentScreen state] (replace)
examples: (test_present_all.py::test_TC_2105_a_resize_keeps_the_cursor_and_the_rail_safe) a resize keeps the cursor and the rail safe

## Entities

[Data: GanttGroup.rows]
in: tuple
desc: `GanttGroup(project, open, rest, late, unfolded, rows)`: `rows` is what the group draws, each task (each milestone) one row; read by `_gantt_frame`, `nav_model`, `gantt_link_order` (through `open`)

[Data: Task.milestone]
in: bool
desc: the task is a milestone: one date, no bar; read by `gantt_plan` (reached ones merge by due), `task_row`, `_present_task_row`; kanban never draws one

[Data: Task.mark]
in: str?
desc: the milestone's class id in the board's marks directory (`board.marks`); a class with `hidden` leaves the gantt through `_hide` and the presentation through `present_tasks_m`

[Data: TaskboardApp.selected_task_id]
in: str?
desc: the main screen's selection; the gantt renders it unfolded and drawn; `action_cursor` and `action_hmove` write it

[Data: TaskboardApp.search_query]
in: str?
desc: the `/` search; in kanban and gantt `_view_board` renders and navigates `filtered_board`, the query's hits, milestones matched like any task

[Data: GanttLinkMode state]
in: tuple
desc: `waiter`, `_cands` (from `gantt_link_order`, loops marked), `_cursor`, `filter`; `_paint` calls `gantt_link_frame` with the waiter as the pin

[Data: PresentScreen state]
desc: `_board`, `_project_id`, `_today`, `_view` (gantt, split, all), `_cursor_id` (views 1/2), `_all_cur` (view 3, ("proj"|"task", id)), `_folded`, `_rail`

[Interface: gantt view]
desc: the main screen's view `3`: `render_gantt` at the viewport size; each milestone its own row ` ◆ title` with `◆ Mon D` on the field

[Interface: presentation frame]
desc: `R`'s `#present-frame`: `render_present` (views 1/2) or `render_present_all(...).frame` (view 3); each open milestone its own field row

[Outside: keys ↑↓]
desc: KEYMAP `cursor(-1)` / `cursor(1)`, priority; in `R` PRESENT_KEYS `move`; in the link mode its own `move`

[Outside: keys ←→]
desc: KEYMAP `hmove(-1)` / `hmove(1)` ("left,h" / "right,l"), priority, group nav; in `R` PRESENT_KEYS `side(-1)` / `side(1)`

[Outside: key L]
desc: KEYMAP `link`; in the gantt the link mode on the chart

## Edges

[Data: Task.milestone] ──▶ gantt_plan
gantt_plan ──▶ [Data: GanttGroup.rows]
[Data: GanttGroup.rows] ──▶ _gantt_frame
[Data: GanttGroup.rows] ──▶ nav_model
[Data: GanttGroup.rows] ──▶ gantt_link_order
[Data: Task.mark] ──▶ _hide
[Data: Task.mark] ──▶ present_tasks_m
[Data: Task.mark] ──▶ milestone_mark
[Data: TaskboardApp.search_query] ──▶ TaskboardApp._nav_columns
[Data: TaskboardApp.selected_task_id] ──▶ TaskboardApp._nav_columns
TaskboardApp.action_cursor ──▶ [Data: TaskboardApp.selected_task_id]
TaskboardApp.action_hmove ──▶ [Data: TaskboardApp.selected_task_id]
when: a non-empty column exists that way; never in the gantt (one column)
[Data: GanttLinkMode state] ──▶ gantt_link_frame
GanttLinkMode.action_move ──▶ [Data: GanttLinkMode state]
[Data: PresentScreen state] ──▶ render_present
[Data: PresentScreen state] ──▶ render_present_all
PresentScreen.action_move ──▶ [Data: PresentScreen state]
PresentScreen.action_side ──▶ [Data: PresentScreen state]
render_gantt ──▶ [Interface: gantt view]
render_present ──▶ [Interface: presentation frame]
render_present_all ──▶ [Interface: presentation frame]
[Outside: keys ↑↓] ──▶ TaskboardApp.action_cursor
when: the main screen is on top (check_action holds it over another screen)
[Outside: keys ↑↓] ──▶ PresentScreen.action_move
when: PresentScreen is on top
[Outside: keys ↑↓] ──▶ GanttLinkMode.action_move
when: the link mode is on top
[Outside: keys ←→] ──▶ TaskboardApp.action_hmove
when: the main screen is on top (check_action holds it over another screen)
[Outside: keys ←→] ──▶ PresentScreen.action_side
when: PresentScreen is on top
[Outside: key L] ──▶ TaskboardApp.action_link

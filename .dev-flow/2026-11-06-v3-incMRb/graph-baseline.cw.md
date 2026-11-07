# Code-Wire baseline — Inc MR-b — the presentation's field rows, its cursor stops, view 3's layout and the deck's scope at 2ce3943

The code that Inc MR-b (the presentation's milestones share one row) touches, as it is at commit 2ce3943 (MR-a merged; marks tree `taskboard-wt/incMRb-marks`, removed after the run). No design here: only what the code does now. Every node has `req: to trace`. Example sources are test ids (file::test) of the current suite or a probe `P-n` run on 2ce3943 over fixture MR-F (`tests/milestone_row_fixture.py`, `board()`, today 2026-10-20); the probes print `taskboard.__file__` = the marks tree (baseline-notes.md). Board ids are `t<key>` and `p<key>`: `ppr` is *Pilot rollout*, `ppe` *Eval harness*, `ppd` *Docs & handover*. MR-a's nodes (`gantt_milestone_row`, `gantt_lane_label`, `_lane_marks`, `_gantt_field`) are in `../2026-11-06-v3-incMR/graph-*.cw.md` and are not repeated; the presentation calls none of them at base.

## Nodes

present_tasks_m
req: to trace
in: Board board; str? project_id
out: tuple(list[Task] open_tasks, list[Task] tasks)
func: the project's shown tasks (`show_in_present`), open first by due (gantt order), with the milestones of a hidden class left out; reached milestones are not open, so no view draws them. The one population of views 1, 2 and 3 and of the deck
module: taskboard/views.py
examples: (P-1) `ppr` → open ["tm2", "tstore", "tm3", "tm4", "ttele", "ttrain", "tm5", "trota"]: the milestones sit among the tasks by due; "tm1" (reached) is absent
examples: (P-7) `ppd` → open ["tha", "thr", "th1"]: the milestone `th1` (Nov 4) is last, after two tasks due before it

gantt_plan.<locals>.walk_key
req: to trace
in: Task t
out: tuple key
func: MR-a's walk order, nested in `gantt_plan`: (no due, due, title, id). Only the board gantt's lane uses it; the presentation has no walk order
module: taskboard/views.py
examples: (P-6) `ppr`'s open milestones sorted by it → ["tm2", "tm3", "tm4", "tm5"] (tm3 before tm4 on Oct 24: `Steering…` < `Store…`)

_present_field
req: to trace
in: list[tuple[str, str]] cells; GanttAxis ax
out: str markup
func: the presentation's field cells to markup over the field ground: `gap` a dim blank; a glyph in `crit` or `accent` as `bright` bold; any other glyph `c(glyph, tone)`, so the tone is read as a style name; the today rule `bright` bold; else lattice or week guide. No branch for `rev:<style>`, `run:<tone>` or the consumed glyph `""`
module: taskboard/views.py
examples: (P-2) the span row of `ppr` at 118x30 → `◂───────●─╎───…◆·…` (73 cells)
examples: (P-8) fed `gantt_milestone_row(lane, "tm2", …)` on `ppr` at 118 (cell `8` = ("■", "rev:violet")) → KeyError `rev:violet`: the tone is read as a style name (the defect LLR-4652.2 names)

_present_task_row
req: to trace
in: Task task; Board board; _PresentGeo p; bool cursor = False
out: str row
func: one field row per task. A milestone: label ` <lead>▎ <glyph> <title>` (lead `⟦` on the cursor, else a blank), the dependency gutter, `gantt_milestone_cells` on the field (the cursor recolours the mark `accent`), and its due alone in the chip. Any other task: `  ▎ <title>`, the gutter, its bar (`⟦━⟧` on the cursor) and its start–end chip
module: taskboard/views.py
examples: (P-2) `tm2` with the cursor at 118x30 → ` ⟦▎ ■ Rubric sign-off          ········■ Oct 19…`, chip `due Oct 19`
examples: (P-2) `tm3` at 80x24 → `  ▎ ■ Steering go/n… ····┆╎···■ Oct 24·…`, chip `due Oct 24`
examples: (test_present_milestone.py::test_TC_2101_a_milestone_row_is_its_date_not_a_bar) a milestone row is its date, not a bar

render_present
req: to trace
in: Board board; str? project_id; str? cursor_id; date today; int width; int height; str view = "gantt"; int scroll = 0
out: Text frame
func: views 1 (`gantt`) and 2 (`split`): the header, the ruler (and the legend strip), the span row, ONE `_present_task_row` per open task in `present_tasks_m` order (each milestone its own row), a rule; then view 1 one brief per open task in the same order plus the cursor's note, view 2 one block per open task, split in two columns from 100 wide (`half = (n+1)//2`). The cursor is `cursor_id` when it is open, else `open_t[0]` (first by due). Below 36 columns one narrow line
module: taskboard/views.py
examples: (P-2) `ppr`, no cursor, 118x30 → lines 5–12 are 8 field rows (m2, store, m3, m4, tele, train, m5, rota); the cursor is `tm2`; briefs lines 14–21 in the same order
examples: (P-3) `ppr`, `split`, 118x30 → left blocks Rubric sign-off, Pilot store list, Steering go/no-go, Store list frozen; right Pilot telemetry, Train store staff, Pilot launch, Field support rota
examples: (P-7) `ppd`, no cursor → the cursor brief `⟦API reference⟧` (the first by due, a task)
examples: (test_present.py::test_TC_1001_the_exact_presc_frame_at_118x30) the PRES-V3 board (no milestone) equals `PRES-V3-gantt-118x30.txt` line for line

present_deck_boards
req: to trace
in: tuple[str|None, str, str, Board] lane; str? project_id
out: list[tuple[str|None, str, str, Board]] lanes
func: the `x` deck's scope: a shallow proxy of the board holding the shown tasks (`present_tasks_m`, open and done) in board order; view 3 (`project_id` None) holds every shown project in `present_order`. Reads no cursor and no fold
module: taskboard/views.py
examples: (test_present_html_export.py::test_TC_4741_LLR_4504_1_one_file_oracle) one file per view, its bytes equal to the oracle

_all_plan
req: to trace
in: Board board
out: list[tuple[Project, list[Task]]] plan
func: view 3's projects: each shown project in `present_order` with its shown open tasks (`present_tasks_m`), milestones among them by due
module: taskboard/views.py
examples: (P-5) MR-F → [("ppr", ["tm2", "tstore", "tm3", "tm4", "ttele", "ttrain", "tm5", "trota"]), ("ppe", ["tgq", "tg1", "tgr", "tg2", "tgx"]), ("ppd", ["tha", "thr", "th1"])]

_all_layout
req: to trace
in: list plan; str? cur_pid; frozenset folded; int room
out: tuple(dict open_, bool gap, list stops, dict rows)
func: view 3's layout. `need` counts 1 head + one row per open task of each unfolded project (+ the gaps). Hand folds stay; while `need` exceeds `room`, the projects furthest from the cursor's fold. Stops in screen order: ("proj", id), then ("task", id) per drawn row, one per milestone; `rows` maps each stop to its own line (from 3)
module: taskboard/views.py
examples: (P-4) MR-F, room 15 (118x18) → `ppe` and `ppd` folded; stops [("proj","ppr"), 8 tasks of ppr, ("proj","ppe"), ("proj","ppd")]
examples: (P-4) MR-F, room 21 (118x24 and 80x24) → nothing folded; 19 stops
examples: (test_present_all.py::test_TC_2103_the_frame_sweep) the stops are the drawn rows, no duplicate

_all_timeline
req: to trace
in: Board board; int width; int height; date today; tuple? cur; frozenset folded; bool rail_focus
out: tuple(list[str] lines, list stops, tuple? cur)
func: view 3's timeline: the header, the ruler, per project its head row and, when unfolded, one `_present_task_row` per open task in the project's hue; the overflow row drops what it covers from the stops; a cursor not among the stops falls to its project's head, else the last or first stop
module: taskboard/views.py
examples: (P-4) MR-F at 118x30 → line 3 `⟦ ■ Pilot rollout …`, lines 4–11 its 8 rows (m2, store, m3, m4, tele, train, m5, rota), line 13 `▾ ■ Eval harness  5 …`, line 20 `▾ ■ Docs & handover …`, line 23 `▎ ◆ Handover call`
examples: (P-4) MR-F at 80x14 → `▸ ■ Eval harness` and `▸ ■ Docs & handover` folded by the overflow rule

render_present_all
req: to trace
in: Board board; tuple? cursor; date today; int width; int height; frozenset folded = frozenset(); bool rail_focus = False
out: PresentAll all
func: view 3 (`all`): below 36 the narrow frame; below `PRESENT_RAIL_MIN` (100) the timeline alone; else the 24-cell rail, `│` and the timeline; returns the frame, the timeline, its width, the stops, the rail stops and the drawn cursor
module: taskboard/views.py
examples: (P-4) MR-F at 118x30, no cursor → cursor ("proj", "ppr"); 19 stops, each milestone its own
examples: (test_present_all.py::test_TC_2103_no_stop_hides_under_the_overflow_row) no stop hides under the overflow row

PresentScreen._shown_ids
req: to trace
in:
out: list[str] ids
func: the cursor's stops in views 1 and 2: the ids of `present_tasks_m(board, project_id)[0]`, read live (a flag change moves them), so in base order (by due)
module: taskboard/app.py
examples: (P-1) `ppr` → ["tm2", "tstore", "tm3", "tm4", "ttele", "ttrain", "tm5", "trota"]

PresentScreen._cursor
req: to trace
in: list[str] ids
out: str? cursor_id
func: the task the frame draws the cursor on, the renderer's own rule: `_cursor_id` when it is in `ids`, else `ids[0]`, else None
module: taskboard/app.py
examples: (P-1) `_cursor_id` None on `ppr` → "tm2"; on `ppd` → "tha"

PresentScreen.action_move
req: to trace
in: int delta
out: None
func: `↑`/`↓` (and `←`/`→` through `action_side` where no rail is drawn): in view 3 the next of `_stops()`, clamped; in views 1 and 2 the next of `_shown_ids()` from `_cursor`, clamped, the note scroll reset; nothing while narrow
module: taskboard/app.py
modify: [Data: PresentScreen state] (replace)
examples: (P-1) `ppr`, cursor `tm2`, `↓` → "tstore" (base order: a task between two milestones)
examples: (test_present_all.py::test_AT_2104_three_views_one_cursor) three views, one cursor

PresentScreen.action_hide
req: to trace
in:
out: None
func: `space`: in views 1 and 2 the cursor's task gets `show_in_present` False and the board is saved; the cursor moves to the next of `_shown_ids()` (the previous at the end). View 3 hides the cursor's stop (`_hide_all`)
module: taskboard/app.py
modify: [Data: Task.show_in_present] (replace); [Data: PresentScreen state] (replace)
examples: (test_present_hide.py::test_AT_1602_space_hides_and_it_is_remembered_a_shows_all) one task hidden and saved; `a` shows it again

## Entities

[Data: PresentScreen state]
desc: `_board`, `_project_id`, `_today`, `_view` (gantt, split, all), `_cursor_id` (views 1/2), `_all_cur` (view 3, ("proj"|"task", id)), `_folded`, `_rail`, `_scroll`

[Data: Task.show_in_present]
in: bool
desc: a task left out of `R` when False; `space` writes it, `a` writes it back; `present_tasks` reads it

[Data: Task.milestone]
in: bool
desc: a milestone draws one date, never a bar; in `R` at base it is a field row like any task

[Interface: presentation frame]
desc: `R`'s `#present-frame`: `render_present` (views 1/2) or `render_present_all(...).frame` (view 3); each open milestone its own field row, its own brief (view 1) and its own block (view 2)

[Outside: keys ↑↓]
desc: `PRESENT_KEYS` `move(-1)` / `move(1)`

[Outside: keys ←→]
desc: `PRESENT_KEYS` `side(-1)` / `side(1)`

[Outside: key space]
desc: `PRESENT_KEYS` `hide`

## Edges

[Data: Task.show_in_present] ──▶ present_tasks_m
[Data: Task.milestone] ──▶ _present_task_row
present_tasks_m ──▶ render_present
present_tasks_m ──▶ _all_plan
present_tasks_m ──▶ PresentScreen._shown_ids
present_tasks_m ──▶ present_deck_boards
_present_task_row ──▶ _present_field
render_present ──▶ _present_task_row
_all_plan ──▶ _all_timeline
_all_layout ──▶ _all_timeline
_all_timeline ──▶ _present_task_row
_all_timeline ──▶ render_present_all
PresentScreen._shown_ids ──▶ PresentScreen._cursor
[Data: PresentScreen state] ──▶ render_present
[Data: PresentScreen state] ──▶ render_present_all
PresentScreen.action_move ──▶ [Data: PresentScreen state]
PresentScreen.action_hide ──▶ [Data: Task.show_in_present]
[Outside: keys ↑↓] ──▶ PresentScreen.action_move
[Outside: keys ←→] ──▶ PresentScreen.action_move
when: through `action_side`, in views 1/2 and in view 3 below 100 columns
[Outside: key space] ──▶ PresentScreen.action_hide
render_present ──▶ [Interface: presentation frame]
render_present_all ──▶ [Interface: presentation frame]

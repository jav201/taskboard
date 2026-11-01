# Inc L — shared interfaces (owned by the orchestrator; agents PROPOSE changes in their group file, never edit here)

> The seams between the three prototype groups. Group D owns models.py + keymap.py; group V owns
> views.py (the rows, the order, the render); group S owns app.py (the screen, the action, the template
> insert stamp). Times are local naive `datetime` unless a node says otherwise. Fixture clock: today
> 2026-11-01, now 2026-11-01T08:10:00.

## Nodes

stamp
req: HLR-4301, LLR-4301.2, LLR-4301.3, LLR-4301.4, LLR-4301.5, LLR-4301.6
in: datetime? now = None
out: str created
func: the one stamp format: `(now or datetime.now()).isoformat(timespec="seconds")`, the format of `history.append`'s `at`. Every creation path calls it (directly or through Board.add_task); no other code formats a created value.
module: taskboard/models.py
examples: (TC-4302b) now `datetime(2026, 11, 1, 8, 10, 7, 999)` → created "2026-11-01T08:10:07"

Board.add_task
req: LLR-4301.5, LLR-4301.7, LLR-4301.2, LLR-4301.4
in: Board self; Task task
out: None
func: reads the clock once, `now = datetime.now()`; if task.created is None: task.created = stamp(now); then (as at base) append, history.append(self.path, {"task", "from": None, "to"}, at=now) (P-D-4: the birth record and created agree to the second), save(). The stamp precedes the save so the file holds it. The seam every UI add path reaches (`_on_task_added`, `_create_and_link`, and Inc K's dump later).
module: taskboard/models.py
modify: [Data: Task.created] (replace when None)
examples: (TC-4305) task Task("a", created=None), clock 2026-11-01T08:10:00 → the board file's entry holds "created": "2026-11-01T08:10:00"; history gains {"task": id, "from": null, "to": "Backlog", "at": "2026-11-01T08:10:00"}
examples: (TC-4307) task Task("a", created="2026-10-01T09:00:00") → created stays "2026-10-01T09:00:00"

added_rows
req: LLR-4303.5, LLR-4304.1, LLR-4304.2, LLR-4304.3, LLR-4304.8, LLR-4304.12, LLR-4304.13
in: list[tuple[str, str, Board?, str]] lanes
out: list[AddedRow] rows
func: one AddedRow per task of every lane whose board is not None, archived tasks included, in lane order then file position. Per board: births = first `at` per task id among `history.read(board.path)` records with `from` None (OSError or ValueError, e.g. UnicodeDecodeError → no births; P-V-1). Per task: `added_moment(task.created)` not None → source "c"; elif `added_moment(births.get(task.id))` not None → source "h"; else source "?" with at None. Never writes; never sets task.created.
module: taskboard/views.py
examples: (TC-4361) a task with created "2026-10-31T18:20:00" and a birth at "2026-10-20T10:00:00" → source "c", at 2026-10-31 18:20
examples: (TC-4362) no created; births at "2026-10-28T10:30:00" then "2026-10-29T11:00:00" for its id → source "h", at 2026-10-28 10:30
examples: (TC-4363) no created, no birth → source "?", at `None`
examples: (TC-4372) history.read raising PermissionError → rows built, the board's unstamped tasks source "?", no exception
examples: (TC-4372b) a history.jsonl holding the byte 0xff → rows built, unstamped tasks source "?", no exception

added_moment
req: LLR-4304.8, LLR-4304.13, LLR-4304.16
in: object value
out: datetime? moment
func: a str that `datetime.fromisoformat` parses → that datetime; an aware one is converted with `.astimezone().replace(tzinfo=None)` (local naive), and a conversion that raises OSError/OverflowError/ValueError gives None (P-V-2); anything else (None, non-str, unparseable) → None. Never raises.
module: taskboard/views.py
examples: (TC-4368) value "not a date" → moment `None`
examples: (TC-4368) value `5` → moment `None`
examples: (TC-4373b) value "1900-01-01T00:00:00+00:00" → moment `None` (no exception)
examples: (TC-4373) value "2026-10-31T18:20:00+00:00" → moment = datetime(2026,10,31,18,20,tzinfo=utc).astimezone().replace(tzinfo=None)

added_order
req: LLR-4304.4, LLR-4304.5, LLR-4304.6, LLR-4306.1
in: list[AddedRow] rows; bool newest; bool show_archived
out: list[AddedRow] ordered
func: drop rows whose task.archived is True unless show_archived; oldest = unknown rows sorted by (lane, pos) + dated rows sorted by (at, lane, pos); newest → the exact reverse of oldest.
module: taskboard/views.py
examples: (TC-4364) rows A(lane 0,pos 0,"?"), B(lane 1,pos 0,"?"), C(lane 0,pos 1,at 10:00), D(lane 1,pos 1,at 10:00), E(lane 0,pos 2,at 09:00); newest `False` → A, B, E, C, D
examples: (TC-4366b) same rows, newest `True` → D, C, E, B, A

first_created
req: LLR-4304.10, LLR-4304.11, LLR-4304.15, LLR-4303.9
in: list[AddedRow] rows
out: datetime? first
func: the minimum `at` over rows with source "c" (archived included: pass the unfiltered rows), else None.
module: taskboard/views.py
examples: (TC-4370) sources c@Oct 31 18:20, c@Nov 1 08:10, h@Oct 28 → first 2026-10-31 18:20
examples: (TC-4371) only "?" and "h" rows → first `None`

state_boxes
req: LLR-4305.1, LLR-4305.2
in: list[str] phases; str phase
out: str boxes
func: n = len(phases); i = phases.index(phase) (0 when absent); n ≤ 8 → "■"×(i+1) + "□"×(n−i−1); n > 8 → f = ceil(8×(i+1)/n), "■"×f + "□"×(8−f).
module: taskboard/views.py
examples: (TC-4381) phases ["Backlog","Doing","Review","Done"], phase "Doing" → boxes "■■□□"
examples: (TC-4381) same phases, phase "Done" → boxes "■■■■"
examples: (TC-4382) 10 phases, index 4 → boxes "■■■■□□□□"

render_added_list
req: HLR-4303, LLR-4303.7, LLR-4303.8, LLR-4303.9, LLR-4303.10, LLR-4303.15, LLR-4303.17, LLR-4305.3, LLR-4304.14, LLR-4306.6
in: list[AddedRow] rows; int sel; bool newest; bool show_archived; int hidden; int unread; datetime? first; date today; dict people; int width; int height
out: Text body
func: the whole body above the key row, `height` lines of at most `width` cells, built from plain Text pieces (never markup): line 1 the head row, line 2 blank, then `height − 2` lines of list (left `lw` cells) ` │ ` detail pane. `rows` are already ordered and filtered (added_order); `sel` indexes them; `hidden` = archived rows left out; `unread` = lanes whose board is None. Group V owns the internals (head, day headers, time labels, row, pane, scroll window).
module: taskboard/views.py
examples: (TC-4327) width 116, height 29, any rows → every list|pane line has "│" at cell index 47 (0-based, = lw 46 + 1); width 78 → at index 35
examples: (TC-4337) rows `[]` → the list area's first line reads "no tasks to list"

AddedList
req: HLR-4303, LLR-4303.2, LLR-4303.4, LLR-4303.5, LLR-4303.14, LLR-4303.16, LLR-4303.19, LLR-4304.7, LLR-4306.2, LLR-4306.3, LLR-4306.4, LLR-4302.6
in:
out: Screen screen
func: app.py Screen[None], in the AllBoardsAgenda pattern: compose reads `board_lanes(app)` once (lanes, ids), `today = date.today()`, `rows = added_rows(lanes)`, `first = first_created(rows)`; state `sel = 0`, `newest = True`, `show_archived = False` (never read from app.show_archived); `_paint` → render_added_list(added_order(rows, newest, show_archived), …, w − 2, h − 1) into #al-body and key_line(ADDED_KEYS, w − 2) into #al-keys. Writes nothing. Group S owns the bindings and actions.
module: taskboard/app.py
examples: (TC-4322) app with 2 registry boards, press N → app.screen is an AddedList

TaskboardApp.action_added_list
req: LLR-4303.2, LLR-4303.3
in: TaskboardApp self
out: None
func: `self._bring(AddedList, AddedList)`, as action_agenda_all.
module: taskboard/app.py
examples: (TC-4323) N, A, N → exactly one AddedList in app.screen_stack and it is app.screen

## Entities

[Data: Task.created]
in: str?
desc: models.py Task field, default None, declared after `show_in_present` and before `extra`, so positional constructors (`Task(title, project_id, phase, …)`) are unaffected. Written by stamp callers only; serialised only when not None; a non-str stored value lives in `extra["created"]` and round-trips (LLR-4302.3).

[Data: AddedRow]
in: NamedTuple(Task task, int lane, str bname, str bcolour, Board board, str source, datetime? at, int pos)
desc: views.py; `lane` indexes the lanes / the screen's `ids` (open_on_board needs `ids[lane]`); `source` ∈ {"c", "h", "?"}; `pos` = file position.

[Data: history.jsonl]
in: lines {"task", "from", "to", "at"}
desc: read only here (history.read); a birth record has from null.

[Interface: AddedList keys]
in: escape,N · up,k · down,j · o · v · enter
desc: all priority bindings of the screen; the key row ADDED_KEYS shows `↑↓ move`, `↵ open on board`, `o newest/oldest`, `v archived`, `esc / N back`.
offers: (TC-4322) "N" → TaskboardApp.action_added_list
offers: (TC-4324) "escape" → AddedList.action_back

## Edges

stamp ──▶ Board.add_task
Board.add_task ──▶ [Data: Task.created]
[Data: Task.created] ──▶ added_moment
[Data: history.jsonl] ──▶ added_rows
added_moment ──▶ added_rows
added_rows ──▶ AddedList
added_rows ──▶ first_created
added_order ──▶ AddedList
first_created ──▶ AddedList
state_boxes ──▶ render_added_list
render_added_list ──▶ AddedList
[Data: AddedRow] ──▶ render_added_list
TaskboardApp.action_added_list ──▶ AddedList

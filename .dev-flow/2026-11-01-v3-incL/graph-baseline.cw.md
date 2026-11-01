# Code-Wire baseline — task creation, persistence and the global-view slice at eb411e1

Baseline of the code that Inc L (the added-order list view and `Task.created`) touches, as the code is at commit eb411e1 (marks tree `taskboard-wt/incL-marks`). No design and no proposal: only what the code does now. Every node has `req: to trace`: the requirements of this increment are written in parallel. Example sources are test ids (file::test) of the current suite, or a probe `P-n` run on eb411e1 (values printed by the probe, listed in baseline-notes.md). The probes import `taskboard` from incL-marks (`taskboard.__file__` printed by each one). Persisted-task construction sites that are not nodes (the seed list, the undo re-insert, the transient span in views.py, team_sync's foreign tasks) are classified in baseline-notes.md and named on the `[Data: Board.tasks]` entity.

## Nodes

Task.from_dict
req: to trace
in: dict d
out: Task task
func: the one load door of a task record; total (never raises): a non-dict or a dict that trips the parser goes to `_rescue_task`; every key not in `_TASK_KEYS` is kept verbatim in `extra` (`_extra_keys`); the legacy `status` and `url` keys are consumed (they are in `_TASK_KEYS`) and so are dropped from the next save; a missing `id` gets a fresh `_new_id()`
module: taskboard/models.py
examples: (P-3) d with "id" "t9", "title" "x", "created" "2026-11-01T10:00:00", "zz" `1`, "status" "doing" → task phase "Doing", extra "created": "2026-11-01T10:00:00" and "zz": `1` (no `created` field on Task)
examples: (P-3) d ["not", "a", "dict"] → task title "(recovered task)", extra "_rescued": `True`, "_rescue_reason": "not a JSON object"
examples: (test_app.py::test_migration_preserves_every_task_and_field) a legacy task with "estimate_hours" `7` → after a load, save and load the task's extra "estimate_hours" is `7`

_rescue_task
req: to trace
in: object entry; str reason
out: Task task
func: a placeholder Task that keeps an unreadable entry's raw content in `notes` ("[rescued] …") and flags it in `extra` (`_rescued`, `_rescue_reason`); title from the entry's `title` or "(recovered task)"; built with `Task(...)`, so it gets a fresh id and the default phase "Backlog"
module: taskboard/models.py
examples: (P-3) entry "title" "Bad", "due_date" `5`, reason "TypeError" → task title "Bad", extra "_rescued": `True`, "_rescue_reason": "TypeError", a new 8-character id
examples: (test_rescue.py::test_rescued_task_roundtrips_through_save) a rescued task survives a save and a reload with its notes and flag

Board.load
req: to trace
in: str | Path path
out: Board board
func: reads a board file; a missing file is SEEDED: `Board(*seed_data(), settings={"migrations": …})` then `save()` — the 16 seed tasks are built with `Task(...)` directly, so no history line is written for them; an unreadable file is quarantined (`.corrupt`) and an empty board returned; otherwise per-entry rescue (`Project.from_dict`, `Task.from_dict`) in FILE ORDER, phases snapped by `canonical_phase`, a `_load_report` set; it writes nothing for an existing file
module: taskboard/models.py
modify: [Data: Board.tasks] (replace)
examples: (P-4) path to a missing file → board with `6` projects and `16` tasks, the file written, history.jsonl NOT written, settings "migrations": "links" `1`, "milestones" `1`
examples: (test_rescue.py::test_one_bad_task_never_empties_the_board) a file with one malformed task → the other tasks load and the bad one is rescued
examples: (P-1) an app-written file → the same tasks in the same order (`ta`, `tb`)

Board._to_dict
req: to trace
in: Task | Project item
out: dict record
func: `asdict(item)` in dataclass field order (title … milestone, mark, show_in_present, extra, id), then drops `show_in_present` when True, `mark` when None, `present_rank` when None (written only when set), then `{**extra, **d}`: the unknown keys are written FIRST, the known fields after them and win on a clash; also the record of each team push (team_sync.push)
module: taskboard/models.py
examples: (P-3) task "t9" with extra "created", "zz" → record keys in order `created`, `zz`, `title`, … , `milestone`, `id` (no `mark`, no `show_in_present`)
examples: (P-1) task "tb" with mark "payment" and show_in_present `False` → keys end `milestone`, `mark`, `show_in_present`, `id`
examples: (test_present_hide.py::test_TC_1603_a_board_with_nothing_hidden_keeps_its_bytes) no hidden task → no record carries "show_in_present"

Board.save
req: to trace
in:
out: None
func: writes `_serialized()` — `json.dumps({"phases", "projects", "tasks", "settings"}, indent=2)` with the default `ensure_ascii=True` (non-ASCII written as `\uXXXX`) — to `self.path` with `write_text` (not atomic; `save_atomic` is the atomic twin used by the move and the cascade); the file's task order is `self.tasks` order
module: taskboard/models.py
modify: [I/O: board.json] (replace)
examples: (P-1) an app-written board: load then save → bytes equal (`True`), `1228` bytes; "Ship café" written as "Ship café"
examples: (P-1) a file whose task carries "created" AFTER "id" (as another version could write it) → the first save is not byte-equal (`False`): the key moves to the front of the record; the second save is a fixed point (`True`)
examples: (test_control_bytes.py::test_TC_410_a_saved_board_round_trips) a file the app saved loads and saves byte-identical

Board.add_task
req: to trace
in: Task task
out: None
func: appends the task to the END of `self.tasks`, appends the creation record `{"task": id, "from": None, "to": task.phase}` to history.jsonl (a failed append does not stop it), then `save()`; it does not stamp `phase_changed` and stores no creation time on the task
module: taskboard/models.py
modify: [Data: Board.tasks] (append)
examples: (test_history.py::test_add_task_appends_creation_record) Task "New" phase "Backlog" on an empty board → one history line, "from" `None`, "to" "Backlog", an "at" key
examples: (P-2) board ["to"], task "tn" → order ["to", "tn"], the file holds "tn", history line `{"task": "tn", "from": null, "to": "Backlog", "at": "2026-11-01T02:50:30"}`

Board.set_task_phase
req: to trace
in: Task task; str phase; date? today = None
out: bool moved
func: snaps `phase` with `canonical_phase`; same phase → False and nothing written; otherwise sets `task.phase`, stamps `phase_changed` with `(today or date.today()).isoformat()` (a DATE, no time) and appends `{"task", "from": old, "to": new}` to history.jsonl; the caller saves
module: taskboard/models.py
examples: (P-2) task "tn" in "Backlog", phase "doing" → moved `True`, phase "Doing", phase_changed "2026-11-01", history line "from" "Backlog", "to" "Doing"
examples: (P-2) the same task, phase "Doing" again → moved `False`
examples: (test_history.py::test_phase_move_appends_one_transition, root action_phase_move) `]` on a "Doing" task in kanban → one line "from" "Doing", "to" "Done"

Board.visible_tasks
req: to trace
in: bool show_archived
out: list[Task] tasks
func: `self.tasks` in board (file) order, archived ones dropped unless `show_archived`; no sort
module: taskboard/models.py
examples: (P-2) tasks "to" (archived) and "tn", show_archived `False` → ["tn"]; show_archived `True` → ["to", "tn"]

Board.phase_index
req: to trace
in: Task task
out: int index
func: the position of `task.phase` in `self.phases`; an unknown phase gives `0`
module: taskboard/models.py
examples: (P-2) task in "Doing" on phases Backlog/Doing/Done → index `1`; a task in "Gone" → index `0`

append
req: to trace
in: str | Path board_path; dict record; datetime? at = None
out: dict? line_record
func: history.append: writes one JSON line `{**record, "at": at.isoformat(timespec="seconds")}` (`at` defaults to `datetime.now()`: local, naive, no offset) to `history.jsonl` in the board file's FOLDER; never raises: an OSError sets `HISTORY_ERROR` and returns None
module: taskboard/history.py
modify: [I/O: history.jsonl] (append); [Data: history.HISTORY_ERROR] (replace)
examples: (P-2) record "task" "tn", "from" `None`, "to" "Backlog" → line_record "at" "2026-11-01T02:50:30" (format YYYY-MM-DDTHH:MM:SS)
examples: (test_history.py::test_append_sets_and_clears_history_error) a directory at the history.jsonl path → line_record `None` and HISTORY_ERROR set; after it is removed an append returns the record and HISTORY_ERROR is `None`

read
req: to trace
in: str | Path board_path
out: tuple(list[dict] records, int skipped)
func: history.read: every valid line of `history.jsonl` in file order; a line is skipped (and counted) when it is invalid JSON, not a dict, or `task`/`to`/`at` is not a string, or `from` is neither None nor a string; blank lines are ignored, not counted; a missing file is `([], 0)`
module: taskboard/history.py
examples: (P-2) a file with one valid creation line, one line with no "from"/"at", "not json", a blank line and a "from" `3` → records one ("from" `None`), skipped `3`
examples: (test_history.py::test_read_missing_file_returns_empty_history) no file → records [] and skipped `0`

TaskboardApp._on_task_added
req: to trace
in: dict? data
out: None
func: the `a` editor's save: pops `milestone`, builds `Task(**data)` from the TaskModal payload (keys id, title, project_id, phase, blocked, archived, pinned, show_in_present, priority, start_date, due_date, notes, urls, images, and `mark` only when the Select changed), applies the milestone box, `board.add_task(task)` (the end of the list, a creation history line, a save), selects it
module: taskboard/app.py
modify: [Data: Board.tasks] (append)
examples: (P-5) data id "tadd0001", title "Added", phase "Backlog" → order ["te", "tadd0001"], history ("tadd0001", `None`, "Backlog")
examples: (test_app.py::test_add_task_modal_appears, root action_add_task) `a`, title "ZZZTASK", save → a task "ZZZTASK" in the board

TaskboardApp._on_template_picked
req: to trace
in: tuple[str, str]? res; str project_id
out: None
func: `I`'s picker result: ("new", …) opens the editor; ("insert", name) builds one `Task(title, project_id, phase=phases[0], notes)` per template task and `board.tasks.append(new)` DIRECTLY (not `add_task`: NO history line), wires `depends_on`, pushes ONE undo entry `{"templates": ids}`, selects the first, `board.save()`
module: taskboard/app.py
modify: [Data: Board.tasks] (append); [Data: TaskboardApp._undo_stack] (append)
examples: (P-5) res ("insert", "Simple chain"), project "pp" → 3 tasks "Plan", "Build", "Ship" in "Backlog" at the end of the list; history.jsonl still holds `1` line (none for the three)
examples: (test_templates_app.py::test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo, root action_templates) `I`, down, enter → `3` new tasks after the old ones, forward chain, one `u` removes all three

TaskboardApp._create_and_link
req: to trace
in: Task waiter; str title
out: None
func: the link picker's create row: title stripped of controls (empty → nothing); a one-phase board is refused with a toast; else `Task(title, project_id=waiter.project_id, phase=phases[0])`, `board.add_task(new)` (creation history line, save), then `link_tasks(waiter, new)`
module: taskboard/app.py
modify: [Data: Board.tasks] (append)
examples: (P-5) waiter "te", title "Linked new" → a task "Linked new" in "Backlog", project "pp", waiter depends_on its id; the last history line "from" `None`, "to" "Backlog"
examples: (test_gantt_link.py::test_R2_2_create_on_a_one_phase_board_is_refused) a one-phase board → no task and the toast "a one-phase board has no open phase to create it in"

TaskboardApp._on_task_edited
req: to trace
in: Task task; dict? data
out: None
func: the `e` editor's save: pops archived, milestone, start_date, due_date; every other payload key is `setattr(task, k, v)` (phase through `set_task_phase`); the payload keys are the TaskModal set (incl. `id`, the same id on an edit), so only the fields the editor knows are written; dates through the cascade, then save
module: taskboard/app.py
examples: (P-5) task "tadd0001", data with title "Edited", phase "Doing" → title "Edited", phase "Doing", phase_changed "2026-11-01", history "from" "Backlog", "to" "Doing"
examples: (test_edit_window.py::test_save_payload_round_trips_every_field, root action_edit) every editor field changed and saved → each task field reads back the new value

move_project
req: to trace
in: Board src; Board dst; str project_id; MovePlan plan; str day; tuple[str, str] names
out: tuple(Board new_src, list[str] steps)
func: carries a project to another board on DEEP COPIES (`copy.deepcopy`, so every Task field and `extra` rides along): backups of both files and the source history, the moving tasks (board order) filtered out of the source and `new_dst.tasks.extend(moving)` (they land at the END of the target's list), target then source `save_atomic`, image folders moved, the moving tasks' history.jsonl lines (any record whose `task` is a moving id, creation lines included) appended to the target folder's history and removed from the source's, move logs; refused when the two boards share a folder
module: taskboard/boards.py
modify: [Data: Board.tasks] (append); [I/O: history.jsonl] (append)
examples: (P-6) src tasks m1 (pm), s1 (ps), m2 (pm); dst d1, d2; move "pm" → dst file order ["d1", "d2", "m1", "m2"]; m1's record still starts with "created"; dst history d2, m1, m2 (each "from" `None`); src history s1 only; the live src keeps ["m1", "s1", "m2"]
examples: (test_boards_move.py::test_TC_2206_the_move) the round's move: target, source, images, history and logs as planned
examples: (test_boards_concurrency.py::test_AT_2303_a_move_keeps_the_source_history_bytes) the source history's backup holds its old bytes

peek_board
req: to trace
in: str | Path path
out: Board board
func: a board read without writing: a missing file → an empty unsaved `Board([], [], p)` (never the seed); an unreadable file → an empty board with `file_unreadable` and NO quarantine copy; else `Board.load(p)`
module: taskboard/boards.py
examples: (P-6) a missing path → `0` tasks, its folder not created (`False`)
examples: (P-6) a file "[1,2" → load_report "file_unreadable": `True`, no ".corrupt" file (`False`)

board_lanes
req: to trace
in: TaskboardApp app
out: tuple(list lanes, list ids)
func: every active registry board as a lane `(name, colour, board | None, state)` and its id: the open board as the app holds it, another one read once with `peek_board` (its `marks` set to the app's live dict; never saved), None with "file missing" / "file unreadable"; an unlisted (`--open`) board last with id None; read by the agenda of every board and the people view
module: taskboard/app.py
examples: (P-8) one board "Main" → lanes [("Main", "violet", the open board, "")], ids ["main"]
examples: (test_all_agenda.py::test_TC_2401_the_unlisted_board_is_the_last_lane) `--open` loose.json → the last lane "loose · not listed", its id `None`

TaskboardApp._bring
req: to trace
in: type kind; Callable make
out: None
func: the global screens' opener (`A`, `@`, `#`): when a screen of `kind` is on the stack, pops the screens over it; else pushes `make()`; so a global screen never piles up
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (P-8) stack Screen, AllBoardsAgenda, PeopleDirectory; `A` → stack Screen, AllBoardsAgenda (the directory popped, no second agenda)
examples: (test_all_agenda.py::test_TC_2401_where_A_acts_and_what_it_holds, root action_agenda_all) `A` on the home → the agenda over it, `3` screens

TaskboardApp.action_agenda_all
req: to trace
in:
out: None
func: `A` (KEYMAP, bar=False, group misc): `_bring(AllBoardsAgenda, AllBoardsAgenda)`; allowed by `check_action` only while no ModalScreen is on the stack
module: taskboard/app.py
examples: (P-8) `A` on the main screen → stack Screen, AllBoardsAgenda
examples: (test_all_agenda.py::test_TC_2401_where_A_acts_and_what_it_holds) `A` over a ConfirmModal or the presentation → nothing opens

TaskboardApp.check_action
req: to trace
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: the app's key gate: `agenda_all`, `people_directory`, `marks_manager` (named here by hand) → allowed only when no ModalScreen is on the stack; any other seat action (`SEAT_ACTIONS`, from KEYMAP) while BoardsHome, AllBoardsAgenda, PeopleDirectory or MarksManager (a hand-written tuple) is on the stack → only `quit`; cursor/hmove/toggle_presentation/boards → refused over any pushed screen; else True
module: taskboard/app.py
examples: (P-8) action "agenda_all" on the main screen → allowed `True`; action "add_task" → `True`
examples: (test_all_agenda.py::test_TC_2401_where_A_acts_and_what_it_holds) with the agenda open, `a`, `d`, `1`, `B`, `x` → the task count unchanged

AllBoardsAgenda.compose
req: to trace
in:
out: ComposeResult widgets
func: reads every board ONCE: `board_lanes(self.app)`, `today = date.today()`, `items = all_agenda(lanes, today)`; yields `Static #ag-body` and `Static #ag-keys` (docked bottom)
module: taskboard/app.py
modify: [Data: AllBoardsAgenda.lanes] (replace); [Data: AllBoardsAgenda.items] (replace)
examples: (P-8) one board with one due today and one undated task → items [("t1", lane `0`)]
examples: (test_all_agenda.py::test_AT_2401_one_screen_for_every_board, root action_agenda_all) three boards → lanes "Personal", "Client", "Course" in registry order

AllBoardsAgenda._paint
req: to trace
in:
out: None
func: `#ag-body` ← `Text.assemble(render_all_agenda(lanes, items, day, row, today, w - 2, h - 1))` (plain Text pieces, no markup parser); `#ag-keys` ← `key_line(AGENDA_KEYS + [("·", "read-only: nothing here edits a task")])`, falling back to `key_line(AGENDA_KEYS, w - 2)` when it does not fit
module: taskboard/app.py
modify: [I/O: Static #ag-body] (replace); [I/O: Static #ag-keys] (replace)
examples: (test_all_agenda.py::test_AT_2401_one_screen_for_every_board) at 118x30 → "◆ ALL BOARDS", "3 boards · read-only", row 29 ends "· read-only: nothing here edits a task"; at 80x24 the key row keeps "←→", "↑↓", "↵", "esc" and drops the tail whole

AllBoardsAgenda.action_jump
req: to trace
in:
out: None
func: `enter`: the chosen bucket's row → `open_on_board(app, ids[lane], task.id)`: pops every pushed screen, switches board when it is another (or starts a deferred one), then `jump_to(task_id)`; nothing when the bucket is empty
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (test_all_agenda.py::test_AT_2401_one_screen_for_every_board) `enter` on "Week 3 plan" → the main screen on "Personal" with that task selected
examples: (test_all_agenda.py::test_TC_2401_where_A_acts_and_what_it_holds) `enter` on a task whose board file is gone → the toast "its file is missing", the open board kept, `1` screen

all_agenda
req: to trace
in: list lanes; date today
out: list[AgendaItem] items
func: every open task (`is_open`) with a due date on or before Sunday from every lane's board (None boards skipped), one `AgendaItem(bucket, lane, board_name, colour, task, project, due, board)` each, bucket "late" or the due date; sorted by (due, lane), stable, so board order is kept inside a lane
module: taskboard/views.py
examples: (test_all_agenda.py::test_TC_2401_buckets_and_dues) the 3-board fixture on Tue 20 → `3` late, `2` today ("Week 3 plan", "Golden question set"), `8` to Sunday; no done or later task

key_line
req: to trace
in: list[tuple[str, str]] pairs; int? width = None
out: Text line
func: a screen's key line in the key bar's style (key bold bright, word muted, three spaces between pairs, a dim " / " between alternative keys); fitted to `width` by dropping words from the right first, then keys
module: taskboard/keymap.py
examples: (P-7) AGENDA_KEYS → line "←→ day   ↑↓ task   ↵ open on its board   esc back"
examples: (P-7) AGENDA_KEYS, width `30` → line "←→ day   ↑↓ task   ↵   esc"
examples: (test_modal_keys.py::test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys) pairs ("y", "archive"), ("n / esc", "cancel") → line "y archive   n / esc cancel"; width `12` → line "alt+s" (the keys go last)

## Entities

[Data: Board.tasks]
in: list[Task]
desc: the board's tasks in FILE ORDER, which is the only order the code keeps; written by `Board.load` (file order), `Board.add_task` (append), `_on_template_picked` (append, models-bypass), `move_project` (filter on the source copy, extend at the end of the target copy), the template undo (filter, app.py:2846), the delete undo (`insert(entry["index"], gone)`: the SAME object back at its old index, app.py:2861), `delete_task` (filter); no task holds a creation time, so after a move or an undo re-insert the list order is not the order of creation

[Data: models._TASK_KEYS]
in: set[str]
desc: models.py:706-709: id, title, project_id, phase, blocked, priority, start_date, due_date, notes, urls, images, archived, pinned, extra, phase_changed, depends_on, milestone, mark, show_in_present, status, url; a key outside it goes to `Task.extra`; "created" is not in it (P-3)

[Data: Task.extra]
in: dict
desc: the unknown keys of a task record, kept verbatim by `Task.from_dict` and written FIRST in the record by `Board._to_dict`; carried by `move_project` (deepcopy) and by the team push; `_rescued` / `_rescue_reason` (rescue) and `_owner` (team_sync foreign tasks, never saved to the board) live here too

[Data: Task dataclass fields]
desc: models.py:868-901, in this order: title, project_id, phase, priority, start_date, due_date, notes, urls, images, archived, pinned, blocked, depends_on, phase_changed (ISO DATE of the last phase move, None = unknown), milestone, mark, show_in_present, extra, id (`_new_id()`: 8 hex chars of uuid4); the record's key order on disk follows this order after the extra keys

[I/O: board.json]
desc: `json.dumps({"phases", "projects", "tasks", "settings"}, indent=2)`, ensure_ascii default (non-ASCII escaped); `save` = `write_text`, `save_atomic` = `write_atomic` (temp file + `os.replace`); an app-written file reloads and saves byte-identical (P-1); a hand-placed unknown key moves to the front of its record on the first save, then is stable

[I/O: history.jsonl]
desc: `<board folder>/history.jsonl`, one JSON line per transition `{"task", "from", "to", "at"}`; `from: null` is the creation record, written only by `Board.add_task`; `at` is `datetime.now().isoformat(timespec="seconds")`, local naive time; readers: `read` → `render_flow` (views.py:4599, intervals from the records) and `legend_entries` mode flow (views.py:8798); one folder holds one board (a move between two boards in one folder is refused, boards.py:690-693)

[Data: history.HISTORY_ERROR]
in: str?
desc: the last append failure, read by `TaskboardApp._warn_history_error` (app.py:2297) once per distinct message

[I/O: TaskModal payload]
desc: modals.py:1334-1357 `TaskModal._save` dict: id (`_img_key`: the task's id on edit, `_new_id()` on add), title, project_id, phase, blocked, archived, pinned, milestone, show_in_present, priority, start_date, due_date, notes, urls, images, and `mark` only when the Select changed; read by `_on_task_added` (`Task(**data)`) and `_on_task_edited` (`setattr` per key); pinned by test_edit_window.py::test_save_payload_round_trips_every_field

[Data: TaskboardApp._undo_stack]
in: list[dict]
desc: one entry per undoable mutation; a template insert pushes `{"templates": ids}`; a delete keeps the full task and its index (`_snapshot`, app.py:2771); `_UNDO_FIELDS` (app.py:2767) = phase, phase_changed, priority, blocked, due_date, archived, pinned, depends_on, start_date, milestone

[Data: keymap.KEYMAP]
in: tuple[Key, ...]
desc: keymap.py:55-177, the one key seat; `app_bindings()` (keymap.py:250) makes `TaskboardApp.BINDINGS` from it; the global screens are `Key("A", "A", "agenda_all", "All boards", group="misc", bar=False)`, `Key("at", "@", "people_directory", …, bar=False)`, `Key("number_sign", "#", "marks_manager", …, bar=False)`: bound always, off the bar, listed by the palette and the `?` help (`global_keys`); uppercase letters in use: A B F H I L M P R S T X; `N` (and lowercase `n`) is not in it

[Data: app.SEAT_ACTIONS]
in: frozenset[str]
desc: app.py:67, every KEYMAP action name; read by `check_action` to hold the main screen's keys behind the home, the agenda, the directory and the marks manager

[Data: app.AGENDA_KEYS]
in: list[tuple[str, str]]
desc: app.py:840 `[("←→", "day"), ("↑↓", "task"), ("↵", "open on its board"), ("esc", "back")]`; the agenda's key line

[Data: App.screen_stack]
in: list[Screen]
desc: Textual's stack; `_bring` pops down to an existing global screen; `open_on_board` pops to the main screen

[Data: AllBoardsAgenda.lanes]
in: list
desc: `(name, colour, board | None, state)` per board, from `board_lanes` at compose; with `ids` beside it; never re-read while the screen is open

[Data: AllBoardsAgenda.items]
in: list[AgendaItem]
desc: `all_agenda(lanes, today)` at compose; `_chosen()` filters it by the bucket `day`; `row` is the cursor in that bucket

[I/O: Static #ag-body]
in: Text
desc: the agenda's rows from `render_all_agenda` (views.py:7811): head, buckets, a lane per board, a rule, the chosen bucket's tasks

[I/O: Static #ag-keys]
in: Text
desc: docked bottom, height 1 (AllBoardsAgenda.DEFAULT_CSS)

[Interface: agenda key line]
desc: `#ag-keys`: "←→ day   ↑↓ task   ↵ open on its board   esc back" + "   · read-only: nothing here edits a task" when it fits; AllBoardsAgenda.BINDINGS (app.py:893) = escape/A back, left/h right/l side, up/k down/j move, enter jump, all priority
offers: "←→ day" → AllBoardsAgenda.action_side
offers: "↑↓ task" → AllBoardsAgenda.action_move
offers: "↵ open on its board" → AllBoardsAgenda.action_jump
offers: "esc back" → AllBoardsAgenda.action_back

[Outside: key A]
desc: KEYMAP `agenda_all` (not priority); on the agenda itself the screen's priority `escape,A` → back wins, so `A` closes it

[Outside: key a]
desc: KEYMAP `add_task` (primary, group task) → TaskModal → `_on_task_added`

[Outside: key I]
desc: KEYMAP `templates` (bar=False) → TemplatePicker → `_on_template_picked`

[Outside: key enter]
desc: AllBoardsAgenda priority binding `jump`

[Outside: key N]
desc: FREE: bound in no KEYMAP entry and in no Screen's BINDINGS in app.py or modals.py (P-7); lowercase `n` is bound in BoardsHome, PeopleDirectory, MarksManager, ConfirmModal and MoveConfirm only; pressed on the main screen it does nothing (P-8)

## Edges

[Data: models._TASK_KEYS] ──▶ Task.from_dict
Task.from_dict ──▶ [Data: Task.extra]
[Data: Task.extra] ──▶ Board._to_dict
[I/O: board.json] ──▶ Board.load
Board.save ──▶ [I/O: board.json]
[Data: Board.tasks] ──▶ Board.save
[Data: Board.tasks] ──▶ Board.visible_tasks
Board.add_task ──▶ [Data: Board.tasks]
Board.load ──▶ [Data: Board.tasks]
TaskboardApp._on_template_picked ──▶ [Data: Board.tasks]
TaskboardApp._on_template_picked ──▶ [Data: TaskboardApp._undo_stack]
move_project ──▶ [Data: Board.tasks]
move_project ──▶ [I/O: history.jsonl]
[I/O: history.jsonl] ──▶ move_project
append ──▶ [I/O: history.jsonl]
append ──▶ [Data: history.HISTORY_ERROR]
[I/O: history.jsonl] ──▶ read
[I/O: TaskModal payload] ──▶ TaskboardApp._on_task_added
[I/O: TaskModal payload] ──▶ TaskboardApp._on_task_edited
[Data: keymap.KEYMAP] ──▶ TaskboardApp.check_action
[Data: app.SEAT_ACTIONS] ──▶ TaskboardApp.check_action
[Data: App.screen_stack] ──▶ TaskboardApp.check_action
[Data: App.screen_stack] ──▶ TaskboardApp._bring
TaskboardApp._bring ──▶ [Data: App.screen_stack]
AllBoardsAgenda.compose ──▶ [Data: AllBoardsAgenda.lanes]
AllBoardsAgenda.compose ──▶ [Data: AllBoardsAgenda.items]
[Data: AllBoardsAgenda.lanes] ──▶ AllBoardsAgenda._paint
[Data: AllBoardsAgenda.items] ──▶ AllBoardsAgenda._paint
[Data: app.AGENDA_KEYS] ──▶ AllBoardsAgenda._paint
AllBoardsAgenda._paint ──▶ [I/O: Static #ag-body]
AllBoardsAgenda._paint ──▶ [I/O: Static #ag-keys]
[Data: AllBoardsAgenda.items] ──▶ AllBoardsAgenda.action_jump
AllBoardsAgenda.action_jump ──▶ [Data: App.screen_stack]
[Outside: key A] ──▶ TaskboardApp.check_action
when: the main screen or the home is on top and no ModalScreen is on the stack; then action_agenda_all runs
[Outside: key a] ──▶ TaskboardApp.check_action
when: the main screen is on top; held (False) while the home, the agenda, the directory or the marks manager is on the stack
[Outside: key I] ──▶ TaskboardApp.check_action
when: the main screen is on top (a seat action, held like `a`)
[Outside: key enter] ──▶ AllBoardsAgenda.action_jump
when: AllBoardsAgenda is the screen (priority binding)

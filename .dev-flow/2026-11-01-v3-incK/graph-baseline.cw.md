# Code-Wire baseline — keys, global screens, task/project creation, stores, image paste and live ink at 545c18a

Baseline of the code that Inc K (a full-screen capture view: the pad, its notes, the dump to a board, `inbox.json`) will call or mirror, as the code is at commit 545c18a (marks tree `taskboard-wt/incK-marks`). No design and no proposal: only what the code does now. Every node has `req: to trace`: the requirements of this increment are written in parallel. Example sources are test ids (file::test) of the current suite, or a probe `P-n` run on 545c18a (values printed by the probe, listed in baseline-notes.md). The probes import `taskboard` from incK-marks (`taskboard.__file__` printed by each one). `marks.Directory` has the same `load`/`refresh`/`_read`/`_commit`/`_set_aside` shape as `people.Directory` (marks.py:76-195); only the people one is a node here, and the marks store is the `[I/O: marks.json]` entity.

## Nodes

app_bindings
req: to trace
in:
out: list[Binding] bindings
func: `TaskboardApp.BINDINGS` (app.py:1312), generated: one `Binding(k.keys, k.action, k.label, priority=k.priority)` per `KEYMAP` entry; the key bar, the palette and the `?` help read the same tuple, so a key that is not in `KEYMAP` is not bound on the main app
module: taskboard/keymap.py
examples: (P-1) at 545c18a → no binding whose keys hold `n` (only `N` → "added_list"); no binding holds an `alt+` key
examples: (test_keymap.py::test_every_binding_the_app_has_comes_from_the_seat) every binding of the app is a KEYMAP entry

key_line
req: to trace
in: list[tuple[str, str]] pairs; int? width = None
out: Text line
func: a screen's key line in the key bar's style (key bold bright, word muted, three spaces between pairs, a dim " / " between alternative keys); fitted to `width` by dropping words from the right first, then keys; what AddedList, AllBoardsAgenda and the modals print as their key row
module: taskboard/keymap.py
examples: (test_modal_keys.py::test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys) pairs ("y", "archive"), ("n / esc", "cancel") → line "y archive   n / esc cancel"
examples: (test_added_list.py::test_TC_4323_N_brings_the_open_list_back_without_a_second_one, root action_added_list) ADDED_KEYS → the key row of the list starts "↑↓ move"

TaskboardApp.check_action
req: to trace
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: the app's key gate: `agenda_all`, `people_directory`, `marks_manager`, `added_list` (a hand-written tuple, app.py:1398) → allowed only when no ModalScreen is on the stack; any other seat action (`SEAT_ACTIONS`) while BoardsHome, AllBoardsAgenda, PeopleDirectory, MarksManager or AddedList (a hand-written tuple, app.py:1403-1405) is on the stack → only `quit`; cursor/hmove/toggle_presentation/boards → refused over any pushed screen; else True
module: taskboard/app.py
examples: (P-4) AddedList on the stack, action "add_task" → allowed `False`
examples: (P-4) AddedList on the stack, action "capture" (not in SEAT_ACTIONS at 545c18a) → allowed `True`
examples: (test_all_agenda.py::test_TC_2401_where_A_acts_and_what_it_holds) with the agenda open, `a`, `d`, `1`, `B`, `x` → the task count unchanged

TaskboardApp._bring
req: to trace
in: type kind; Callable make
out: None
func: the global screens' opener (`A`, `N`, `@`, `#`): when a screen of `kind` is on the stack, pops the screens over it; else pushes `make()`; so a global screen never piles up
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (test_added_list.py::test_TC_4323_N_brings_the_open_list_back_without_a_second_one, root action_added_list) `N`, `@`, `N` → one AddedList on the stack, the directory popped
examples: (P-4) `N` on the main screen → stack ["Screen", "AddedList"]

TaskboardApp.action_added_list
req: to trace
in:
out: None
func: `N` (KEYMAP keymap.py:147, bar=False, group misc, right after `A`): `_bring(AddedList, AddedList)`; the model a new global screen copies: a KEYMAP Key, an `action_*` that calls `_bring`, a name in check_action's two hand-written tuples, a README row
module: taskboard/app.py
examples: (P-4) `N` → stack ["Screen", "AddedList"]; `escape` → ["Screen"]
examples: (test_added_list.py::test_TC_4317_the_open_list_writes_no_board_and_no_history, root action_added_list) the open list writes no board file and no history line

AddedList.compose
req: to trace
in:
out: ComposeResult widgets
func: reads every board ONCE: `board_lanes(self.app)`, `today = date.today()`, `rows = added_rows(lanes)`, `first = first_created(rows)`; yields `Static #al-body` and `Static #al-keys` (docked bottom); `on_screen_resume` repaints but does NOT re-read; its BINDINGS (app.py:971) are priority `escape,N` back, `up,k`/`down,j` move, `o`, `v`, `enter`
module: taskboard/app.py
modify: [Data: AddedList.lanes] (replace)
examples: (test_added_list.py::test_TC_4317_the_open_list_writes_no_board_and_no_history) open, move, flip order → every board file keeps its bytes
examples: (P-4) two boards "Main" and "Side" → the lanes of `board_lanes` in registry order

board_lanes
req: to trace
in: TaskboardApp app
out: tuple(list lanes, list ids)
func: every active registry board as a lane `(name, colour, board | None, state)` and its id: the open board is `app.board` itself (the same object), another is a fresh `peek_board` (its `marks` set to the app's live dict; never saved here), None with "file missing" / "file unreadable"; an unlisted (`--open`) board last with id None
module: taskboard/app.py
examples: (P-4) boards "Main" (open) and "Side" → lanes [("Main", "violet", tasks ["ta1"], ""), ("Side", "cyan", tasks ["tb1"], "")], ids ["main", "side"]; lane 0's board is `app.board` (`True`)
examples: (test_all_agenda.py::test_TC_2401_the_unlisted_board_is_the_last_lane) `--open` loose.json → the last lane "loose · not listed", its id `None`

TaskboardApp._on_task_added
req: to trace
in: dict? data
out: None
func: the `a` editor's save: pops `milestone`, `Task(**data)` from the TaskModal payload, applies the milestone box, `self.board.add_task(task)` (the OPEN board only: end of the list, `created` stamped, a creation history line, a save), selects it; pushes NO undo entry ("a modal add records NOTHING", app.py:2875)
module: taskboard/app.py
modify: [Data: Board.tasks] (append)
examples: (P-4) data id "tadd0001", title "Added", project "pa" → order ["ta1", "tadd0001"], undo stack `[]`
examples: (test_app.py::test_add_task_modal_appears, root action_add_task) `a`, title "ZZZTASK", save → a task "ZZZTASK" in the board

TaskboardApp._on_project_added
req: to trace
in: dict? data
out: None
func: `p` (`action_add_project`, app.py:3757) pushes ProjectModal; its result: pops `date_links`, `Project(**data)` (keys name, color, status, start_date, due_date …), `date_links` into `extra`, `self.board.add_project(proj)` (the OPEN board), refresh; no undo entry, no toast
module: taskboard/app.py
modify: [Data: Board.projects] (append)
examples: (P-4) data name "Gamma", color "cyan" → projects ["Alpha", "Gamma"] in memory and in the file
examples: (test_app.py::test_add_project, root action_add_project) `p`, a name, save → the project in the board

TaskboardApp.action_undo
req: to trace
in:
out: None
func: `u`: pops `_undo_stack` (a session list of dicts on the OPEN board, cleared by `switch_board` and `after_move`) until one entry applies; entry shapes by key: "milestones", "migration", "cascade", "templates" (ids removed), else {"task_id", "fields"[, "task", "index"]} (fields restored, or the deleted task re-inserted); each applied entry saves the open board and toasts (title "Undo"); an empty stack toasts "Nothing to undo."
module: taskboard/app.py
modify: [Data: TaskboardApp._undo_stack] (replace); [Data: Board.tasks] (replace)
examples: (P-4) right after `_on_task_added` → toast ("Nothing to undo.", "Undo"), order unchanged ["ta1", "tadd0001"]
examples: (test_templates_app.py::test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo) one `u` removes all three template tasks

TaskboardApp._refresh_directories
req: to trace
in:
out: None
func: the fresh re-read seat (batch 2026-10-24-batch-02, HD-5): `self.people.refresh()` and `self.marks.refresh()`; a `False` (unparseable) toasts "<file> could not be read; the directory as loaded is kept." (title People / Marks, warning, markup=False); called before `@`, `#`, `a` and `e` open (app.py:1531, 1536, 3503, 3532)
module: taskboard/app.py
examples: (test_directory_refresh.py::test_AT_2706_the_directories_stay_fresh) a person a second Directory wrote → shown the next time the view opens
examples: (test_directory_refresh.py::test_AT_2707_a_failed_re_read_keeps_the_directory) unparseable people.json → one "People" warning, every person kept

Board.add_task
req: to trace
in: Task task
out: None
func: ONE clock read `now`; stamps `task.created = stamp(now)` when None; appends to the END of `self.tasks`; `history.append(self.path, {"task", "from": None, "to": phase}, at=now)` (a failed append does not stop it); `save()`; it works on ANY Board object (a peeked one too) and writes that object's whole task list
module: taskboard/models.py
modify: [Data: Board.tasks] (append); [I/O: board.json] (replace)
examples: (P-3) a peeked board "b" holding ["t0"], Task "Dumped" id "tdump001" → file order ["t0", "tdump001"], created "2026-11-01T04:45:38", b's history line "from" `null`, "to" "Backlog", the same "at"
examples: (P-3) two Board objects loaded from one file, each `add_task` → the file holds ["t0", "ttwo0001"]: the first add ("tone0001") is lost

Board.add_project
req: to trace
in: Project project
out: None
func: appends the project to `self.projects` and `save()`; no history line, no stamp
module: taskboard/models.py
modify: [Data: Board.projects] (append); [I/O: board.json] (replace)
examples: (P-3) peeked board "b", Project "New one" id "pn" → the file's projects ["pb", "pn"]

Board.image_dir
req: to trace
in: str task_id
out: Path folder
func: `<board-dir>/images/<task_id>/` (`self.path.parent / "images" / task_id`); creates nothing; the method is `image_dir` (singular)
module: taskboard/models.py
examples: (P-3) board "b", task "tdump001" → "b/images/tdump001", exists `False`

Board.save
req: to trace
in:
out: None
func: `mkdir(parents)` then `self.path.write_text(self._serialized())` — NOT atomic and under NO lock; `_serialized` is `json.dumps({"phases", "projects", "tasks", "settings"}, indent=2)` (ensure_ascii default: non-ASCII escaped), every record through `_to_dict(…, with_created=True)`; `save_atomic` (models.py:1116) is the `write_atomic` twin
module: taskboard/models.py
modify: [I/O: board.json] (replace)
examples: (P-3) two holders of one file → the last save wins (the other's task is gone)
examples: (test_control_bytes.py::test_TC_410_a_saved_board_round_trips) a file the app saved loads and saves byte-identical

Board.load
req: to trace
in: str | Path path
out: Board board
func: a missing file is SEEDED (16 tasks, one shared `created`) and SAVED; an unreadable file is quarantined (`.corrupt`) and an empty board returned; else per-entry rescue in file order, phases snapped; writes nothing for an existing file; `switch_board` (app.py:1605) loads the next board with it
module: taskboard/models.py
modify: [Data: Board.tasks] (replace)
examples: (P-3) a missing path → `16` tasks and the file written
examples: (test_rescue.py::test_one_bad_task_never_empties_the_board) one malformed task → the others load and it is rescued

write_atomic
req: to trace
in: Path path; str text
out: None
func: the one atomic write: a read-only target is refused (PermissionError) before anything; `mkstemp` beside the RESOLVED target (`.<name>.<random>.tmp`), write utf-8, copy the old mode, `os.replace`; the temp file goes on every failure; used by `Board.save_atomic`, `Registry.save`, `people.Directory._commit`, `marks.Directory._commit`
module: taskboard/models.py
modify: [I/O: people.json] (replace)
examples: (P-2) `Directory.add("Ana Ruiz")` → people.json `{"version": 1, "people": [{"id": "ana.ruiz", …}]}`, no `.tmp` and no `.lock` left
examples: (test_people_directory.py::test_TC_2501_a_failed_write_changes_nothing_in_memory) a failing write → the file and the directory unchanged

save_pil_image
req: to trace
in: Path directory; object image
out: Path dest
func: `directory.mkdir(parents=True)`, the first free `paste-NNN.png` (from 001), converts a non RGB/RGBA/L image to RGB, saves PNG, returns the RESOLVED absolute path; writes at once (before the editor saves)
module: taskboard/models.py
examples: (P-5) folder "b/images/tdump001", a 2x2 image → "b/images/tdump001/paste-001.png"; again → "paste-002.png"
examples: (test_app.py::test_save_pil_image_increments) two saves → paste-001.png then paste-002.png

Directory.load
req: to trace
in: object path
out: Directory directory
func: never raises; a missing or blank file → an empty directory (nothing written); unparseable (`_read` None) or an OSError → `keep_aside(path)` and an empty directory with `load_report` {"unreadable": True, "backup": path | None}; stamps (mtime_ns, size)
module: taskboard/people.py
examples: (P-2) a missing people.json → `0` people, the file not created, load_report `{}`
examples: (P-2) "{not json" → load_report "unreadable" `True`, backup "people.json.corrupt"

Directory.refresh
req: to trace
in:
out: bool? changed
func: the mtime/size-gated re-read: stat unchanged → None (no parse); changed → `_read`; parsed → `_hold` in place (the live dict every board holds) and True; unparseable → False, the in-memory people kept, the new stamp kept so it is reported once
module: taskboard/people.py
modify: [Data: Directory.people] (replace)
examples: (P-2) another instance added "ana.ruiz2" → `True`, ids ["ana.ruiz", "ana.ruiz2"]; again → `None`
examples: (P-2) the file then made "{not json" → `False`, ids kept ["ana.ruiz", "ana.ruiz2"]
examples: (test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size) unchanged stat → no re-parse

Directory._read
req: to trace
in: Path path
out: list[Person]? people
func: `read_bytes` (an OSError raises), `clean_strings(json.loads(...))`; not an object with a `people` list → None; an entry without a valid unique handle or a name is skipped; text fields capped (`_clean`)
module: taskboard/people.py
examples: (test_people_directory.py::test_TC_2501_an_unreadable_file_is_kept_aside_and_the_directory_starts_empty) a non-object file → None, so load keeps it aside
examples: (P-2) a file with "ana.ruiz" and "ana.ruiz2" → two Person entries

Directory._commit
req: to trace
in: (Callable) dict->object change
out: object result
func: read-modify-write: `mkdir`, `with file_lock(self.path)`: re-read the file NOW (`_read`; unparseable and not set aside → OSError, nothing written), `fresh` = the file's people (or the in-memory ones when the file is missing or was set aside), `result = change(fresh)`, `write_atomic(path, json.dumps({"version": 1, "people": [...]}, indent=2, ensure_ascii=False))`; then `_hold(fresh)` and stamp; a failed write raises and changes nothing in memory
module: taskboard/people.py
modify: [I/O: people.json] (replace); [Data: Directory.people] (replace)
examples: (P-2) d1 and d2 loaded from one empty file; d1 adds "Ana Ruiz", then d2 (stale) adds "Ana Ruiz" → the file holds ["ana.ruiz", "ana.ruiz2"]: nothing is lost
examples: (test_people_directory.py::test_TC_2501_two_windows_never_erase_each_others_people) two windows' adds → both people in the file

Directory._set_aside
req: to trace
in:
out: bool kept
func: whether the unparseable file's bytes are safe before it is written over: empty → True; the same bytes as `load_report["backup"]` → True (no second copy); else `keep_aside(path) is not None`
module: taskboard/people.py
examples: (P-2) a directory loaded from "{not json" (copy made at load), then `add("Bo Lin")` → kept `True`, still ONE copy "people.json.corrupt"; the file now holds ["bo.lin"] only
examples: (test_people_directory.py::test_TC_2501_an_unparseable_file_is_kept_aside_before_it_is_replaced) the bytes are copied before the write

Directory.add
req: to trace
in: str name; str role = ""; str note = ""
out: Person person
func: `_clean(name)`; empty → ValueError; `_commit(change)` where change makes `Person(handle_for(name, set(fresh) | set(self.people)), …)`: the handle is unique against the file AND memory
module: taskboard/people.py
modify: [I/O: people.json] (replace)
examples: (P-2) "Ana Ruiz", "Legal" on an empty file → person id "ana.ruiz"; the same name from a stale instance → "ana.ruiz2"

file_lock
req: to trace
in: object path; str? label = None
out: Iterator beat
func: context manager: `<resolved name>.lock` created with O_EXCL holding a random 16-byte hex token; a regular lock older than `LOCK_STALE` (10 s) is taken over; past `LOCK_WAIT` (2 s) raises OSError "<label or name> is busy — another taskboard is writing it; try again in a few seconds (<lock>)"; yields `beat` (renews mtime); removed on exit only while it holds this token; used by Registry._commit, people/marks `_commit` and move_project's target — NOT by `Board.save`
module: taskboard/boards.py
modify: [I/O: <file>.lock] (replace)
examples: (P-2) a fresh foreign `x.json.lock`, label "Inbox" → OSError after `2.0` s "Inbox is busy — another taskboard is writing it; try again in a few seconds"
examples: (test_boards_concurrency.py::test_TC_2301_a_stale_lock_is_taken_over_and_a_fresh_one_is_not) a stale lock is taken over, a fresh one is not

keep_aside
req: to trace
in: Path path
out: Path? backup
func: a byte copy of an unreadable file at the first free `<name>.corrupt`, `.corrupt-2`, … (`open(dest, "xb")`: never replaces a copy); an empty or unreadable file → None
module: taskboard/boards.py
examples: (P-2) people.json "{not json" with "people.json.corrupt" already there → "people.json.corrupt-2"
examples: (test_marks_directory.py::test_TC_2603_the_corrupt_copy_is_never_replaced) an earlier copy is never replaced

peek_board
req: to trace
in: object path
out: Board board
func: a board read without writing: a missing file → an empty unsaved `Board([], [], p)` (default phases; saving it would CREATE the file); an unreadable file → an empty board with `file_unreadable` and no quarantine copy; else `Board.load(p)` (a fresh object each call); the "read again now" step before a cross-board write (modals.py:1601)
module: taskboard/boards.py
examples: (P-3) a missing path → `0` tasks, phases ["Backlog", "Doing", "Done"], the file not created (`False`)
examples: (P-3) board "b" → tasks ["t0"], a new object (not the app's)

TaskModal._paste_image
req: to trace
in:
out: None
func: `alt+i` (TaskModal BINDINGS modals.py:767, `press_button('paste-img')`): `grab_clipboard_image()` (PIL ImageGrab; never raises) → None: toast "No image found in the clipboard."; a LIST of paths (files copied in Explorer): kept only when the suffix is in `IMAGE_EXTS` and `os.path.isfile`, and referenced at their ORIGINAL path (no copy); a bitmap: `save_pil_image(board.image_dir(self._img_key))` at once; the paths are appended as lines of the `#f-images` TextArea; toast "Added N image(s)."
module: taskboard/modals.py
modify: [I/O: images/<task_id>/paste-NNN.png] (append)
examples: (test_app.py::test_clipboard_paste_saves_and_appends) a clipboard bitmap → one paste-NNN.png under the task's folder and its path in the images field
examples: (P-5) folder for `_img_key` "tdump001" (the new id an add will use) → "b/images/tdump001/paste-001.png"

TaskModal.action_pen
req: to trace
in: int i
out: None
func: `alt+1`..`alt+6` open pen i (PEN_CODES r o y g b v), `alt+0` (i = -1) lifts; acts only while `#f-notes` has focus; refuses (toast NOTICE_PEN) a selection or a cursor inside a span; inserts the pair `::<code>::  ::` at the cursor and moves inside it; state `self.pen`, `self._pen_at`; `enter` under a pen is `action_pen_enter` (priority binding, modals.py:775); depends on TaskModal state, not on InkArea
module: taskboard/modals.py
modify: [Data: TaskModal.pen] (replace)
examples: (test_colour_pens.py::test_TC_4230_alt_n_opens_a_spaced_pair_with_the_cursor_inside) `alt+1` in the notes → "::r::  ::" with the cursor inside
examples: (test_colour_pens.py::test_TC_4249_esc_digit_parses_as_alt_digit_after_the_import) ESC 5 → key "alt+5" once modals is imported

InkArea._build_highlight_map
req: to trace
in:
out: None
func: `#f-notes` (a TextArea subclass with its own theme "taskboard-ink"): Textual's own map, then `self._highlights.update(ink_highlights(document.lines))` — byte-offset spans named "pen.<tone>" / "pen.mark" from `colour_spans`, a line over `INK_MAX_LINE` (2000) skipped, a lone surrogate → no ink, any exception → no ink; overrides a PRIVATE Textual hook and only recolours ranges (it cannot change the glyphs shown)
module: taskboard/modals.py
examples: (P-5) lines ["a ::r:: red :: b", "____", "plain"] → `{0: [(2, 8, "pen.mark"), (8, 11, "pen.over"), (11, 14, "pen.mark")]}`: nothing for "____"
examples: (test_colour_pens.py::test_TC_4231_typing_under_a_pen_stays_inside_its_span) typing under a pen stays inside its span

highlight_segments
req: to trace
in: str text
out: list[tuple[str, str]] segments
func: the one tokeniser of the notes' highlight syntax, from `colour_spans`: `==x==` soon, `!!x!!` over, `++x++` green, `::<code>:: x ::` the code's tone, the rest "mut"; markers dropped; read by the board markup and `notes_text` / `notes_preview`; mentions are not its concern (`notes_text` splits them after)
module: taskboard/views.py
examples: (P-5) "a ::r:: red :: b ==soon== @ana.ruiz" → [("a ", "mut"), ("red", "over"), (" b ", "mut"), ("soon", "soon"), (" @ana.ruiz", "mut")]
examples: (P-5) "____" → [("____", "mut")]

## Entities

[Data: keymap.KEYMAP]
in: tuple[Key, ...]
desc: keymap.py:55-181, the one key seat; no `alt+` key and no lowercase `n` in it (P-1); uppercase letters in use A B F H I L M N P R S T X; the global screens are `bar=False` group misc: `A` agenda_all (:143), `N` added_list (:147), `H`, `@` (`at`), `#` (`number_sign`); `u` is undo (:88), `p` add_project (:136), `i` open_images (:135), `o` open_url (:134)

[Data: app.SEAT_ACTIONS]
in: frozenset[str]
desc: app.py:68, every KEYMAP action name (text before "("); a new KEYMAP action joins it and is then held by check_action behind the five global/home screens unless named in the first tuple

[Data: App.screen_stack]
in: list[Screen]
desc: Textual's stack; `_bring` pops down to an existing global screen; `open_on_board` (app.py:876) pops to the main screen, switches board, `jump_to`

[Data: AddedList.lanes]
in: list
desc: `(name, colour, board | None, state)` per board from `board_lanes` at compose, with `ids`; never re-read while the screen is open; lane boards other than the open one are throwaway peeks

[Data: Board.tasks]
in: list[Task]
desc: the board's tasks in file order; `add_task` appends; `Task` fields (models.py:878-915): title, project_id, phase, priority, start_date, due_date, notes (str), urls, images (list[str] of paths or URLs), archived, pinned, blocked, depends_on, phase_changed, milestone, mark, show_in_present, created (str?, `stamp()` "YYYY-MM-DDTHH:MM:SS" local, written only when set), extra, id (`_new_id()`, 8 hex)

[Data: Board.projects]
in: list[Project]
desc: `Project` fields (models.py:838-852): name, color "violet", status "on_track", archived, pinned, start_date, due_date, show_in_present, present_rank, extra, id; `add_project` appends

[Data: TaskboardApp._undo_stack]
in: list[dict]
desc: app.py:1347, a session list of the OPEN board's entries; `switch_board` and `after_move` set it to `[]` (P-4); shapes "milestones", "migration", "cascade", "templates", or {"task_id", "fields"[, "task", "index"]} (`_snapshot`, app.py:2881; `_UNDO_FIELDS` app.py:2877); no entry names a board, and an add pushes none

[Data: Directory.people]
in: dict[str, Person]
desc: the ONE live dict (handle → Person) every board holds (`board.people`); `_hold` clears and refills it in place, so a refresh shows everywhere

[I/O: board.json]
desc: `<board-dir>/board.json`; `Board.save` = `write_text` (not atomic, no lock); `save_atomic` = `write_atomic`; two windows on one board: the last save wins (the presence toast says so, app.py:1481-1483)

[I/O: people.json]
desc: `~/.taskboard/people.json` beside the registry (app.py:1326, `self.registry.path.parent / PEOPLE_NAME`); `{"version": 1, "people": [{"id", "name", "role", "note"}]}`, indent 2, ensure_ascii=False (raw UTF-8, unlike board.json); written only by `_commit`

[I/O: marks.json]
desc: `~/.taskboard/marks.json` (app.py:1329); `{"version": 1, "marks": [{"id", "name", "shape", "colour", "hidden"}]}`; `Mark.name` is the class's display name, `id` its slug; the same load/refresh/_read/_commit/_set_aside pattern as people (marks.py:76-195)

[I/O: <file>.lock]
desc: `<resolved file name>.lock` beside the file, a 16-byte hex token; LOCK_WAIT 2.0 s, LOCK_STALE 10.0 s (boards.py:39-40)

[I/O: images/<task_id>/paste-NNN.png]
desc: `Board.image_dir(task_id)` = `<board-dir>/images/<task_id>/`; written by `save_pil_image` at paste time; `move_project` moves a task's folder that sits directly under the source's images/ (boards.py:795-799); a task's `images` list holds absolute paths

[Data: TaskModal.pen]
in: int?
desc: the open pen index (None = off) and `_pen_at`; state of the TaskModal, read by `action_pen`, `action_pen_enter`, `_lift_pen`, `check_action` (modals.py:1131)

[Interface: added list key line]
desc: `#al-keys`: `key_line(ADDED_KEYS)` (app.py:843) "↑↓ move   ↵ open on board   o newest/oldest   v archived   esc / N back" + "   · read-only: nothing here edits a task" when it fits
offers: "↑↓ move" → AddedList.action_move
offers: "↵ open on board" → AddedList.action_jump
offers: "esc / N back" → AddedList.action_back

[Outside: key N]
desc: KEYMAP `added_list`; on AddedList the screen's priority `escape,N` → back wins

[Outside: key n]
desc: FREE on the main app (P-1, P-4: `n` on the main screen pushes nothing and changes no task); bound only as a screen key in BoardsHome (new), PeopleDirectory (new), MarksManager (new), ConfirmModal (no), MoveConfirm (no)

[Outside: key a]
desc: KEYMAP `add_task` → TaskModal → `_on_task_added`

[Outside: key p]
desc: KEYMAP `add_project` (bar=False) → ProjectModal → `_on_project_added`

[Outside: key u]
desc: KEYMAP `undo` on the main app; `u` is also PresentScreen `hidden_picker` and PresentHiddenPicker `close`

[Outside: key alt+i]
desc: TaskModal `press_button('paste-img')` → `_paste_image`; the only `alt+i` binding in taskboard/

[Outside: key alt+1..alt+6, alt+0]
desc: TaskModal PEN_BINDINGS (modals.py:493-495), priority; ESC+digit reaches the app as `alt+<digit>` only because `_unshadow_alt_digits` (modals.py:75) pops Textual 8.2.8's glyph entries at import

[Outside: key alt+enter]
desc: bound nowhere in taskboard/; in Textual 8.2.8 the legacy ESC CR arrives as plain `enter` (P-1), only the kitty form CSI 13;3u arrives as `alt+enter`

## Edges

[Data: keymap.KEYMAP] ──▶ app_bindings
[Data: keymap.KEYMAP] ──▶ TaskboardApp.check_action
[Data: app.SEAT_ACTIONS] ──▶ TaskboardApp.check_action
[Data: App.screen_stack] ──▶ TaskboardApp.check_action
[Data: App.screen_stack] ──▶ TaskboardApp._bring
TaskboardApp._bring ──▶ [Data: App.screen_stack]
AddedList.compose ──▶ [Data: AddedList.lanes]
Board.add_task ──▶ [Data: Board.tasks]
Board.add_task ──▶ [I/O: board.json]
Board.add_project ──▶ [Data: Board.projects]
Board.add_project ──▶ [I/O: board.json]
[Data: Board.tasks] ──▶ Board.save
[Data: Board.projects] ──▶ Board.save
Board.save ──▶ [I/O: board.json]
[I/O: board.json] ──▶ Board.load
Board.load ──▶ [Data: Board.tasks]
TaskboardApp._on_task_added ──▶ [Data: Board.tasks]
TaskboardApp._on_project_added ──▶ [Data: Board.projects]
[Data: TaskboardApp._undo_stack] ──▶ TaskboardApp.action_undo
TaskboardApp.action_undo ──▶ [Data: TaskboardApp._undo_stack]
TaskboardApp.action_undo ──▶ [Data: Board.tasks]
[I/O: people.json] ──▶ Directory._read
Directory.refresh ──▶ [Data: Directory.people]
Directory._commit ──▶ [Data: Directory.people]
Directory._commit ──▶ [I/O: people.json]
write_atomic ──▶ [I/O: people.json]
Directory.add ──▶ [I/O: people.json]
[I/O: marks.json] ──▶ TaskboardApp._refresh_directories
file_lock ──▶ [I/O: <file>.lock]
save_pil_image ──▶ [I/O: images/<task_id>/paste-NNN.png]
TaskModal._paste_image ──▶ [I/O: images/<task_id>/paste-NNN.png]
TaskModal.action_pen ──▶ [Data: TaskModal.pen]
[Data: TaskModal.pen] ──▶ TaskModal.action_pen
[Outside: key N] ──▶ TaskboardApp.check_action
when: no ModalScreen is on the stack; then action_added_list runs
[Outside: key n] ──▶ TaskboardApp.check_action
when: the main screen is on top; no KEYMAP entry, so nothing runs at 545c18a
[Outside: key a] ──▶ TaskboardApp.check_action
when: the main screen is on top; held (False) while the home or a global screen is on the stack
[Outside: key p] ──▶ TaskboardApp.check_action
when: the main screen is on top (a seat action, held like `a`)
[Outside: key u] ──▶ TaskboardApp.action_undo
when: the main screen is on top
[Outside: key alt+i] ──▶ TaskModal._paste_image
when: TaskModal is the screen (priority binding)
[Outside: key alt+1..alt+6, alt+0] ──▶ TaskModal.action_pen
when: TaskModal is the screen and `#f-notes` has focus

# Baseline notes — task creation, persistence and global-view slice at eb411e1

**Counts:** 26 nodes, 23 entities, 37 edges. That is over the aim of 12–16, because the slice brief names each of these functions. `codewire_lint` exit 0 (0 lines not read). `codewire_marks` wrote 26 marks, 0 nodes without code. `codewire_extract --path models.py,history.py,app.py,boards.py,views.py,keymap.py` exit **1**: 8 findings, all of kind `input_untyped_in_code`. These parameters have no annotation in the code: `_rescue_task.entry`, `Board._to_dict.item`, `append.board_path`, `read.board_path`, `peek_board.path`, `board_lanes.app`, `TaskboardApp._bring.make`, `all_agenda.lanes`. The run found no type mismatch and no missing node. It lists 44 "calls", and most are name collisions. `history.append` and `history.read` are nodes named `append` and `read`, so the extractor counts every `list.append`, `Text.append` and file `.read()` as a call to them. extract-baseline.txt marks each row REAL, LIFTED or COLLISION. Lines below are at eb411e1 (unmarked). The lines in extract-baseline.txt are in the marked tree.

**Which tree is imported:** `pip show taskboard` gives an editable install pointing at `C:\Users\jjgh8\Github\taskboard` (the main checkout). Each probe puts the cwd (incL-marks) first on `sys.path` and prints `taskboard.__file__` = `…\taskboard-wt\incL-marks\taskboard\__init__.py`. The guard run used `python -m pytest` with cwd = incL-marks, which also puts the cwd first.

## Where a persisted task is made (every `Task(` / append / insert in taskboard/)

| Site (eb411e1) | Path | Class | History line? |
|---|---|---|---|
| models.py:1039 `Task.from_dict(t)` in `Board.load` | load of the file | **load** (file order) | no |
| models.py:928 `cls(...)` in `Task.from_dict` | load door | **load** | no |
| models.py:775 `Task(title=…, notes=…, extra=…)` in `_rescue_task` | unreadable entry on load | **load** (rescue placeholder, fresh id) | no |
| models.py:1403-1431, 16 `Task(...)` in `seed_data` | `Board.load` of a missing file, then `save()` (models.py:1007-1011) | **persisted creation** (seed) | **no** (bypasses `add_task`; P-4) |
| app.py:3401 `Task(**data)` + 3403 `add_task` in `_on_task_added` | `a` → TaskModal | **persisted creation** | yes, `from: None` |
| app.py:2565 `Task(...)` + 2566 `add_task` in `_create_and_link` | `L` picker create row | **persisted creation** | yes, `from: None` |
| app.py:2018 `Task(...)` + 2020 `self.board.tasks.append(new)` in `_on_template_picked` | `I` template insert | **persisted creation** | **no** (P-5: history stays at 1 line after 3 inserts) |
| app.py:2861 `self.board.tasks.insert(idx, gone)` in `action_undo` | undo of a delete | **re-insert of the same object** (same id, old index) | no |
| boards.py:813 `new_dst.tasks.extend(moving)` in `move_project` | project move | **re-insert of deep copies** (same ids and fields, at the END of the target) | the source's lines move with the tasks |
| team_sync.py:221 `Task.from_dict(tdict)` in `foreign_tasks` | teammates' push files | **transient** (never added to `board.tasks`; `_owner` in extra) | no |
| views.py:7497 `Task(title="", start_date=…, due_date=…)` in `_all_ruler` | presentation ruler echo | **transient** (a span for `gantt_echo`) | no |
| views.py:3159, 4177 `proxy.tasks = [...]` on `copy.copy(board)` | gantt hide / proxies | **transient** (never saved) | no |

Other things checked: boards.py:437 `Registry.create` writes an EMPTY new board (no task). `__main__.py` makes no task. modals.py:1917 (`TemplateEditor`) makes template rows, not tasks. Nothing else in taskboard/ constructs or appends a persisted Task.

**Callers of `Board.add_task` (eb411e1):** app.py:2566 (`_create_and_link`) and app.py:3403 (`_on_task_added`). There are no others in taskboard/. Tests call it directly (for example test_history.py:59).

**What the edit path writes:** `_on_task_edited` (app.py:3426) runs `setattr` over the keys of the TaskModal payload (modals.py:1334-1357). The keys are id, title, project_id, phase (through `set_task_phase`), blocked, pinned, show_in_present, priority, notes, urls, images, and `mark` only when the Select changed. It pops archived, milestone, start_date and due_date and handles them apart. On an edit, `id` is `_img_key = task.id` (modals.py:798), the same id. Only the fields the editor knows are written. A dataclass field outside this key set is never touched by an edit. `_UNDO_FIELDS` (app.py:2767-2769) is a fixed tuple and does not snapshot any other field.

## Order facts

- `board.tasks` is FILE ORDER. `Board.load` keeps the file's order. `add_task`, the template insert and `move_project` append at the end. The undo re-insert puts the task back at its old index. `visible_tasks` does not sort.
- After a move (P-6), the target's file reads `d1, d2, m1, m2`: the moved tasks come last, whatever their age. No task stores a creation time. The only creation timestamps are the `from: None` lines in history.jsonl, and those exist only for `add_task` tasks. Seed tasks, template inserts and tasks older than the history file have none.
- `phase_changed` is an ISO **date** (`date.today().isoformat()`, models.py:1261), written only by `set_task_phase`.

## History record

- Shape: `{"task": <id>, "from": <old phase> | null, "to": <phase>, "at": <ISO>}` (P-2). The creation record is `from: null`, written only by `Board.add_task` (models.py:1267).
- `at` = `datetime.now().isoformat(timespec="seconds")` (history.py:33-34): **local naive time, no UTC offset**, format `YYYY-MM-DDTHH:MM:SS` (P-2: `2026-11-01T02:50:30`). Compare team_sync's `_utc_now_iso` (team_sync.py:25), which is UTC.
- `read` skips and counts a line that is invalid JSON, not a dict, has a non-string `task`/`to`/`at`, or has a `from` that is neither None nor a string. Blank lines are ignored and not counted (P-2: 1 record, skipped 3).
- File: `<board folder>/history.jsonl`, one per folder. `move_project` refuses two boards in one folder (boards.py:690-693). Readers: `render_flow` (views.py:4599) and `legend_entries` mode flow (views.py:8798).

## Byte stability

- **App-written file:** Board.load then save gives the same bytes (P-1a: `True`, 1228 bytes). The second save of any file is a fixed point (P-1b).
- **Unknown key on a task:** it is kept in `extra` and written FIRST in the record (`{**extra, **d}`, models.py:1065). A file the app wrote with an extra key is therefore stable. A file where another version placed the key elsewhere (P-1b: `created` after `id`) is NOT byte-equal on its first save: the key moves to the front of the record. The parsed JSON is equal (P-1c), and the second save is stable.
- **Key order of a task record:** extra keys first, then title, project_id, phase, priority, start_date, due_date, notes, urls, images, archived, pinned, blocked, depends_on, phase_changed, milestone, [mark], [show_in_present], id. `mark` is written only when set, `show_in_present` only when `false`, `present_rank` (projects) only when set (models.py:1059-1064). A new dataclass field with a default would be written into every record unless `_to_dict` drops it the same way. Then every existing board would change bytes on its next save, and every team push record would grow by one key.
- **ASCII:** `json.dumps` uses the default `ensure_ascii=True`, so `é` is written as `\u00e9`. A file holding raw UTF-8 (hand-written) is not byte-equal after one save (P-1d: `False`).
- `Board.save` is `write_text` (not atomic). `save_atomic` (`write_atomic`) is used by the move, the cascade and a few other paths.
- **Guards that pin byte stability:**
  - tests/test_marks_directory.py::test_TC_2602_a_board_without_marks_keeps_its_bytes_through_a_load_and_a_save
  - tests/test_marks_directory.py::test_TC_2602_an_unknown_id_is_kept_byte_for_byte_through_a_save
  - tests/test_present_hide.py::test_TC_1603_a_board_with_nothing_hidden_keeps_its_bytes
  - tests/test_present_hide.py::test_TC_1603_a_hidden_task_writes_false_and_nothing_else
  - tests/test_present_all.py::test_TC_2102_the_oracle_board_keeps_its_bytes
  - tests/test_control_bytes.py::test_TC_410_a_saved_board_round_trips
  - tests/test_palette_ration.py::test_a_board_with_no_retired_hue_is_left_byte_identical
  - tests/test_cascade.py::test_TC_623_apply_then_restore_round_trips_byte_identically_and_touches_only_planned
  - tests/test_all_agenda.py::test_AT_2401_one_screen_for_every_board (the board files keep their bytes)
  - Unknown keys survive (by value, not bytes): tests/test_app.py::test_migration_preserves_every_task_and_field

## Global views and keys

- **The pattern:** a `Key(…, group="misc", bar=False)` in `KEYMAP` (keymap.py:55-177) gives a binding, an entry in the palette and the `?` help (`global_keys`), and no entry in the key bar. The action calls `_bring(Screen, Screen)` (app.py:1407). The screen is a `Screen` (not modal) that closes on a priority `escape,<its key>` → back. Its key row is `key_line(...)` (keymap.py:180).
- `check_action` (app.py:1286) names `agenda_all`, `people_directory` and `marks_manager` by hand (allowed only with no ModalScreen on the stack). It also holds every seat action behind a hand-written tuple `(BoardsHome, AllBoardsAgenda, PeopleDirectory, MarksManager)` (app.py:1301). A new global screen is not in either list until someone adds it.
- `AllBoardsAgenda` reads every board ONCE, at `compose` (`board_lanes` → `peek_board` for the other boards). `today` is frozen at compose. The screen is read-only, and `enter` uses `open_on_board` (app.py:872): it pops every screen, switches the board when needed, then `jump_to`.
- **`N` is FREE.** No KEYMAP entry and no Screen's BINDINGS in app.py or modals.py binds `N` or `shift+n` (P-7). KEYMAP uppercase letters in use: A B F H I L M P R S T X. Lowercase `n` is bound only in BoardsHome, PeopleDirectory, MarksManager, ConfirmModal and MoveConfirm. None of these is on top while the main screen is active. Pressing `N` on the main screen does nothing (P-8). The README key table is pinned to the seat (test_keymap.py::test_the_readme_keybinding_table_matches_the_seat), so a new key also needs a README row.

## Guards (existing tests that exercise the slice) — 52 ids, run on incL-marks: 54 passed in 24 s (parametrised cases included), state `executed`

- Byte stability: the 10 above.
- History and model:
  - tests/test_history.py::test_phase_move_appends_one_transition, ::test_add_task_appends_creation_record, ::test_history_error_is_surfaced_without_aborting_move, ::test_read_skips_malformed_lines_and_counts_them, ::test_read_missing_file_returns_empty_history, ::test_append_sets_and_clears_history_error
  - tests/test_rescue.py::test_one_bad_task_never_empties_the_board, ::test_rescued_task_roundtrips_through_save, ::test_from_dict_is_total_never_raises
  - tests/test_app.py::test_boots_and_seeds, ::test_at_001_seed_generic_and_complete
- Creation sites:
  - tests/test_app.py::test_add_task_modal_appears, ::test_edit_task
  - tests/test_edit_window.py::test_save_payload_round_trips_every_field
  - tests/test_templates_app.py::test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo, ::test_user_template_lists_before_presets_and_inserts_with_links, ::test_no_project_refuses_with_the_toast, ::test_empty_template_toasts_is_empty
  - tests/test_link_picker.py::test_AT_502_L_links_from_the_picker (the create row)
  - tests/test_gantt_link.py::test_R2_2_create_on_a_one_phase_board_is_refused
- Move:
  - tests/test_boards_move.py::test_TC_2206_the_move, ::test_AT_2206_move_a_project_to_another_board, ::test_TC_2206_two_boards_in_one_folder_are_refused, ::test_TC_2206_a_bad_history_line_never_stops_the_handover, ::test_TC_2206_the_target_holds_a_moving_id
  - tests/test_boards_concurrency.py::test_TC_2303_the_history_is_copied_with_the_board_files, ::test_AT_2303_a_move_keeps_the_source_history_bytes
- Agenda of every board: tests/test_all_agenda.py::test_TC_2401_buckets_and_dues, ::test_TC_2401_every_row_is_the_width_and_board_text_is_literal, ::test_TC_2401_where_A_acts_and_what_it_holds, ::test_TC_2401_the_unlisted_board_is_the_last_lane, ::test_AT_2401_one_screen_for_every_board
- Key contract:
  - tests/test_keymap.py::test_every_binding_the_app_has_comes_from_the_seat, ::test_global_commands_are_palette_only_not_in_the_bar, ::test_the_palette_includes_palette_only_globals, ::test_every_shown_key_has_a_real_action_on_the_app, ::test_the_seat_has_no_duplicate_keys_or_labels, ::test_no_two_shown_keys_share_an_action, ::test_the_readme_keybinding_table_matches_the_seat
  - tests/test_help_keys.py::test_TC_1607_global_keys_are_the_live_palette_only_keys, ::test_AT_1603_the_help_shows_the_global_keys_without_scrolling
  - tests/test_modal_keys.py::test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys, ::test_TC_2407_every_modal_is_in_the_inventory

## Probes (run on incL-marks, `taskboard.__file__` = incL-marks; synthetic boards in a temp folder, `Path.home` redirected to a temp folder for app probes)

- **P-1 (bytes)**
  - An app-written board (project `pa`; tasks `ta`, and `tb` with mark "payment", show_in_present False, title "Ship café"): load then save is byte-equal (`True`, 1228 bytes), and `é` is escaped.
  - The same file with `"created"` placed after `id` on one task: the first save is not equal; the second save is a fixed point; the parsed JSON is equal.
  - The same board written with ensure_ascii=False: not equal after a save.
- **P-2 (history)**
  - `add_task(Task("Probe", id="tn"))` on a board holding `to`: order `[to, tn]`, and the line `{"task": "tn", "from": null, "to": "Backlog", "at": "2026-11-01T02:50:30"}`.
  - `set_task_phase(tn, "doing")`: True, phase `Doing`, `phase_changed` `2026-11-01`, and a second line. The same phase again gives False.
  - `phase_index`: 1, and 0 for an unknown phase.
  - `visible_tasks(False)`: `[tn]` when `to` is archived.
  - `read` on a mixed file: 1 record, 3 skipped.
- **P-3 (from_dict and _to_dict)**
  - The unknown keys `created` and `zz` go to `extra`; `status: doing` gives phase `Doing`; the `_to_dict` key order puts the extra keys first.
  - A non-dict gives `(recovered task)` with `_rescued`.
  - `_rescue_task({"title": "Bad", "due_date": 5}, "TypeError")` gives title "Bad" and a new 8-character id.
  - `"created" in _TASK_KEYS` is False.
- **P-4 (seed):** a missing file gives 6 projects and 16 tasks; the file is written, history.jsonl is NOT written, and the settings are `{"migrations": {"links": 1, "milestones": 1}}`.
- **P-5 (app creation sites, headless `run_test`)**
  - `_on_task_added(payload)`: history `(tadd0001, None, Backlog)`.
  - `_on_template_picked(("insert", "Simple chain"), "pp")`: 3 tasks, and the history still holds 1 line.
  - `_create_and_link(te, "Linked new")`: one more creation line, and the waiter is linked.
  - `_on_task_edited` with title and phase changed: the title is set, the phase goes through `set_task_phase` (one transition line), and `phase_changed` is the date.
  - The file's task order follows the creation order here, because nothing was moved.
- **P-6 (move):** src `m1(pm), s1(ps), m2(pm)` and dst `d1, d2`; moving `pm` gives the dst file `d1, d2, m1, m2`.
  - m1's record still starts with `created` (extra survives the deepcopy).
  - The dst history holds d2, m1 and m2 creation lines; the src history keeps s1.
  - The live `src` object is unchanged.
  - `move_plan(..., None, None)` is refused ("team configuration cannot be read"); out of team mode the app passes `set()` (`move_team_ids`, app.py:1383).
  - `peek_board` on a missing path writes nothing; on an unreadable file it reports `file_unreadable` and makes no `.corrupt` copy.
- **P-7 (keys):** no `n`/`N`/`shift+n` in `app_bindings()`. Screens binding `n`: BoardsHome, MarksManager, PeopleDirectory, ConfirmModal, MoveConfirm. `key_line(AGENDA_KEYS)` gives "←→ day   ↑↓ task   ↵ open on its board   esc back", and at width 30 "←→ day   ↑↓ task   ↵   esc".
- **P-8 (`_bring`, `board_lanes`):**
  - On a one-board app, `board_lanes` gives `[("Main", "violet", <open board>, "")]` and `["main"]`.
  - `A` gives `[Screen, AllBoardsAgenda]`; then `@` gives `+PeopleDirectory`; then `A` gives `[Screen, AllBoardsAgenda]` again (popped, not piled); `A` on the agenda gives `[Screen]`.
  - `N` on the main screen: no screen and no task change.

The `# node:` marks remain uncommitted in incL-marks: 26 lines in app.py (11), models.py (9), boards.py (2), history.py (2), keymap.py (1) and views.py (1). Nothing in taskboard/ or tests/ of capture-proto was touched.

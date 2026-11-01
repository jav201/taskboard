# Baseline notes — keys, global screens, creation, stores, image paste and live ink at 545c18a

**Counts:** 31 nodes, 23 entities, 40 edges. That is one over the aim of 20–30, because the slice brief names each of these functions (`action_add_project` is folded into `_on_project_added`, `ink_highlights` into `InkArea._build_highlight_map`; `marks.Directory` is an entity, not six more nodes). `codewire_lint` exit 0 (0 findings, 0 lines not read). `codewire_marks` wrote 31 marks, 0 nodes without code. `codewire_extract --path models.py,app.py,boards.py,people.py,modals.py,views.py,keymap.py` exit **1**: 8 findings, 7 `input_untyped_in_code` and 1 `return_untyped_in_code`. These have no annotation in the code: `_bring.make`, `board_lanes.app`, `save_pil_image.image`, `Directory.load.path`, `Directory._commit.change`, `file_lock.path` (and its return: a `@contextmanager` generator), `peek_board.path`. No type mismatch, no missing node, no mark drift. 35 calls: 22 REAL, 7 LIFTED (through `refresh_view` / `visible_text`), 6 COLLISION (`Directory.add` vs every `set.add`, `Board.save` vs PIL `Image.save`, `Directory.load` vs `Board.load`). extract-baseline.txt classifies each row. Lines below are at 545c18a (unmarked). The lines in extract-baseline.txt are in the marked tree.

**Which tree is imported:** `pip show taskboard` gives an editable install pointing at `C:\Users\jjgh8\Github\taskboard` (the main checkout): a bare `import taskboard` from any other cwd prints `C:\Users\jjgh8\Github\taskboard\taskboard\__init__.py`. Each probe puts incK-marks first on `sys.path` and prints `taskboard.__file__` = `…\taskboard-wt\incK-marks\taskboard\__init__.py`. The guard run used `python -m pytest` with cwd = incK-marks, which also puts the cwd first (probe printed the same path).

**A prototype of this increment already exists in the tree:** `prototypes/capture_round/proto.py` (not product code). The extractor shows it calling `Board.add_task` (:169), `Board.add_project` (:156), `Board.image_dir` (:165), `Directory.refresh` (:1253), `InkArea._build_highlight_map` (:1318) and `check_action` (:1479). Nothing in `taskboard/` imports it.

## Keys

- **`n` is FREE on the main app.** `KEYMAP` (keymap.py:55-181) has no `n` entry; `app_bindings()` (keymap.py:254) gives only `N` → `added_list` (keymap.py:147) (P-1). Pressing `n` on the main screen pushes nothing and changes no task (P-4). Lowercase `n` is a screen-local key only: BoardsHome `new` (app.py:652 class), PeopleDirectory `new` (app.py:1071), MarksManager `new` (app.py:1212), ConfirmModal `no` (modals.py:2411), MoveConfirm `no` (modals.py:3683). Each of these is on top of the stack when its `n` acts, so none of them meets a main-app `n`.
- **No `alt+` key is in KEYMAP**, and no screen in app.py binds one. All `alt+` bindings live in modals.py (P-1):

| Key the pad wants | Bound today (545c18a) | Where | Same meaning? |
|---|---|---|---|
| `alt+d` (dump) | `press_button('cal-f-due')`, the due-date picker | TaskModal (DATE_KEYS modals.py:402, class :755) and ProjectModal (class :1360) | **No** — "due" there, "dump" in the pad |
| `alt+o` (other) | — | nowhere | — |
| `alt+n` (new project) | `focus_row('mf-name')` | MarkForm (modals.py:2602, class :2592) | **No** — "name" there |
| `alt+a` (review) | — | nowhere | — |
| `alt+i` (image) | `press_button('paste-img')` → `_paste_image` | TaskModal (modals.py:767) | Yes — image |
| `alt+u` (undo) | — | nowhere | — |
| `alt+enter` (divider) | — | nowhere; **and it cannot arrive** in legacy mode (below) | — |

  None of them collides at run time: each is a binding of a modal that is on top only while it is open. They collide only if one of those modals is pushed OVER the pad (for example if `alt+n` opens ProjectModal, then `alt+d` there is "due date"). Textual's own TextArea has `alt+backspace` and `alt+delete` (word delete); Input has `alt+backspace`. Other `alt+` keys in use: `alt+s` (seven forms), `alt+t` (start date), `alt+m` (mark), `alt+c` (colour; MarkForm colour), `alt+h` (MarkForm shape), `alt+p` (SearchPrompt page), `alt+0`..`alt+6` (pens, TaskModal only).
- **`alt+enter` in Textual 8.2.8 (P-1):** the legacy sequence ESC CR is parsed as plain `enter` (the tuple branch of `_sequence_to_key_events` drops the alt). Only the kitty-protocol form `CSI 13;3u` gives `alt+enter`. The modals.py:63-66 comment records that Windows Terminal answers no kitty protocol. So in Windows Terminal, `alt+enter` reaches the pad (when WT does not take it for fullscreen) as `enter`: a newline in the TextArea, not a divider. ESC+letter (`alt+d`, `alt+o`, `alt+n`, `alt+a`, `alt+i`, `alt+u`) parses as `alt+<letter>` (P-1).
- **`alt+<digit>` works only after `modals._unshadow_alt_digits()`** (modals.py:75, run at import) pops Textual 8.2.8's WezTerm glyph entries for ESC 0-6. A pad module that does not import modals first would get glyphs.
- **The global-screen pattern (Inc L's `N`):** a `Key(…, group="misc", bar=False)` in KEYMAP → `action_added_list` (app.py:1543) → `_bring(AddedList, AddedList)` (app.py:1510). `check_action` (app.py:1388) names `agenda_all`, `people_directory`, `marks_manager`, `added_list` by hand (app.py:1398: allowed only with no ModalScreen on the stack) and holds every other seat action behind a hand-written tuple `(BoardsHome, AllBoardsAgenda, PeopleDirectory, MarksManager, AddedList)` (app.py:1403-1405). A new KEYMAP action joins `SEAT_ACTIONS` (app.py:68) automatically, so it is held behind those screens unless it is in the first tuple; a new screen is not in the second tuple until someone adds it, and while it is not, any seat key the focused widget does not consume bubbles to the app and acts on the board behind (P-4: `check_action("capture", …)` with AddedList up is `True` today only because `capture` is not a seat action yet). The README key table is pinned to the seat (tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat).

## Creation and saving

- `_on_task_added` (app.py:3507) → `Task(**data)` → `self.board.add_task(task)` (models.py:1301). `add_task` stamps `created` (`stamp(now)`, models.py:648, the same `now` as the history line), appends to the END, writes the `from: None` history line, then `save()`. It acts on whatever Board object it is called on (P-3: a `peek_board` object works).
- `_on_project_added` (app.py:3760; `p` = `action_add_project` app.py:3757 → ProjectModal) → `Project(**data)` → `self.board.add_project(proj)` (models.py:1312): append + `save()`, no history, no undo, no toast.
- **`Board.save` (models.py:1112) is `write_text`: not atomic, no lock.** `save_atomic` (models.py:1116) uses `write_atomic` (models.py:721). Two Board objects on one file both `add_task` → the file keeps only the second (P-3). So a dump into the OPEN board must go through `app.board`. A dump through a separate object would be erased by the app's next save of its in-memory board.
- **Saving a board other than the open one:** the app has one path that does it, `move_project` (boards.py:760). It re-reads the target fresh (`peek_board`, modals.py:1601: "read again now: the picker's copy may be older than the file"), holds `file_lock(dst.path, name)` (boards.py:776), refuses when `_stamp(dst.path)` (boards.py:679: mtime/size) changed since the plan, and writes with `save_atomic`. `board_lanes` (app.py:847) peeks other boards and says "never saved". A peeked missing file is an empty `Board([], [], p)` with the default phases; saving it CREATES the file (P-3). `Board.load` of a missing file SEEDS 16 tasks and saves (P-3). A board open in another window is overwritten by that window's next save ("last save wins", the presence toast app.py:1481-1483).
- **Undo:** `_undo_stack` (app.py:1347) is a session list of the OPEN board's entries. `switch_board` (app.py:1605) and `after_move` reset it to `[]` (P-4). No entry names a board. "A modal add records NOTHING" (app.py:2875): `u` after `_on_task_added` toasts "Nothing to undo." (P-4). Entry shapes: "milestones", "migration", "cascade", "templates", or `{"task_id", "fields"[, "task", "index"]}` (`_snapshot` app.py:2881, `_UNDO_FIELDS` app.py:2877). `action_undo` is app.py:2900.
- **Toasts:** there is no wrapper helper. Every site calls `self.notify(msg, title=…, severity=…, timeout=…, markup=False)` directly; `markup=False` on any user text. The named helpers are `_notify_save_error` (app.py:1660), `_warn_registry` (app.py:1580), `_warn_history_error` (app.py:2407).

## The store pattern a new `inbox.json` mirrors (people.py, marks.py, boards.py)

- `Directory.load` (people.py:128): never raises; missing/blank → empty (nothing written); unparseable → `keep_aside` + empty + `load_report {"unreadable": True, "backup": …}`; stamps (mtime_ns, size).
- `Directory.refresh` (people.py:149): **this is the "fresh re-read" of batch 2026-10-24-batch-02** (HLR-2706/2707, LLR-2706.1). Stat unchanged → None (no parse); changed → `_read` → `_hold` in place → True; unparseable → False, people kept, new stamp kept (reported once). App seat: `_refresh_directories` (app.py:1520), called before `@` (app.py:1531), `#` (:1536), `a` (:3503), `e` (:3532). marks.py:98 is the twin.
- `Directory._read` (people.py:171): `read_bytes` (OSError raises), `clean_strings(json.loads)`, not `{"people": [...]}` → None, bad entries skipped.
- `Directory._commit` (people.py:216): **the read-modify-write:** `mkdir`; `with file_lock(path)`: re-read NOW, unparseable and not set aside → OSError (nothing written); `change(fresh)`; `write_atomic(path, json.dumps({"version": 1, "people": […]}, indent=2, ensure_ascii=False))`; then `_hold` + stamp. A stale instance's add keeps the other's (P-2: `ana.ruiz` + `ana.ruiz2`). marks.py:160 is the twin.
- `Directory._set_aside` (people.py:238): empty → True; same bytes as the load's backup → True (no second copy); else `keep_aside`. After a set-aside, `fresh` is the IN-MEMORY set (P-2: a directory loaded empty from a bad file then `add("Bo Lin")` → the file holds only `bo.lin`; the old bytes stay in `people.json.corrupt`).
- `Directory.add` (people.py:253): handle unique against the file and memory (`handle_for`, people.py:284).
- `file_lock` (boards.py:102): `<resolved name>.lock`, O_EXCL, a random token, stale after `LOCK_STALE` 10 s (boards.py:40), `OSError("<label> is busy — another taskboard is writing it; try again in a few seconds (<lock>)")` after `LOCK_WAIT` 2 s (boards.py:39) (P-2: 2.0 s). Users: `Registry._commit` (boards.py:347), people `_commit` (people.py:222), marks `_commit` (marks.py:166), move target (boards.py:776). `Board.save` does not use it.
- `keep_aside` (boards.py:69): `<name>.corrupt`, `.corrupt-2`, … created with `"xb"`; never replaces a copy (P-2).
- `write_atomic` (models.py:721): a read-only target is refused first; mkstemp beside the resolved target; mode copied; `os.replace`; the temp file is removed on failure.
- **Encoding differs:** people.json / marks.json / boards.json are written `ensure_ascii=False` (raw UTF-8); board.json uses the default `ensure_ascii=True` (`\uXXXX`).
- Placement: `~/.taskboard/` = `self.registry.path.parent` (app.py:1326 people, :1329 marks). An app built without a registry (`Registry.single`, boards.py:284; the suite builds hundreds) has its registry path beside the board, so the stores land beside the board file, not in the home.
- `marks.Mark` (marks.py:40): `id` (slug, stable on rename), `name` (display), `shape`, `colour`, `hidden`; `MARKS_NAME = "marks.json"` (marks.py:28); `find(q)` is a lower-case prefix match on `name` (marks.py:150).

## Image attach (task editor)

- Key `alt+i` → `press_button('paste-img')` (modals.py:767) → `on_button_pressed` (modals.py:1276) → `_paste_image` (modals.py:1283). It is a **clipboard paste**, not a file picker: `grab_clipboard_image()` (models.py:502, PIL `ImageGrab.grabclipboard`; never raises).
- A list of files (copied in Explorer): kept when `Path(p).suffix.lower() in IMAGE_EXTS` (models.py:499: .png .jpg .jpeg .gif .webp .bmp) and `os.path.isfile(p)`, then **referenced at the original path — not copied** into the per-task folder.
- A bitmap: `save_pil_image(self.board.image_dir(self._img_key), img)` (models.py:631) writes `paste-NNN.png` AT ONCE (P-5: `paste-001.png`, then `paste-002.png`), before the editor saves. A cancelled add leaves the file. `_img_key` (modals.py:798) = the task's id on edit, a fresh `_new_id()` on add, and it becomes the new task's id (payload `"id"`).
- The method is **`Board.image_dir`** (singular, models.py:1018) = `<board-dir>/images/<task_id>/`. R0-9 says `images_dir`. The only code that moves an image folder between boards is `move_project` (boards.py:795-825). There is no "copy one file into a task's folder" helper.
- The opener's safety gate is separate: `_open_local_image` (app.py:3737) refuses UNC, `file://`, a non-allowlisted suffix, a non-file.

## Live colour in the notes (Inc C)

- `#f-notes` is `InkArea(TextArea)` (modals.py:561). It registers its own theme "taskboard-ink" and overrides `_build_highlight_map` (modals.py:572), a **private Textual hook**: Textual's map, then `self._highlights.update(ink_highlights(lines))` (modals.py:537). The spans are byte offsets named `pen.<tone>` / `pen.mark`; a line over `INK_MAX_LINE` = 2000 (modals.py:534) is skipped; a lone surrogate or any exception → no ink. **Highlights only recolour ranges.** They cannot replace glyphs, so a `____` line drawn as a full-width rule (R0-4) is not reachable through this hook (P-5: `ink_highlights(["____"])` gives nothing for it).
- The pens are **TaskModal** state and actions, not InkArea's: `PEN_BINDINGS` (modals.py:493), `action_pen` (modals.py:991), `action_pen_enter` (modals.py:1024, a priority `enter` binding at modals.py:775 gated in TaskModal.check_action modals.py:1131), `action_colour` (`alt+c`, modals.py:1076), `_lift_pen`, `pen_label` (modals.py:498). A pad that wants pens must re-host these.
- `views.highlight_segments` (views.py:3596) is the one tokeniser (from `colour_spans`, views.py:3538; `PEN_CODES` views.py:3507): `==x==` soon, `!!x!!` over, `++x++` green, `::<code>:: x ::`; the markers are dropped; mentions stay in the text (`notes_text` splits them, P-5).

## Guards (existing tests that exercise the slice) — 32 ids, run on incK-marks (marks in place): 38 passed in 16.6 s (parametrised cases included), state `executed`

- Keys: tests/test_keymap.py::test_every_binding_the_app_has_comes_from_the_seat, ::test_the_readme_keybinding_table_matches_the_seat, ::test_the_seat_has_no_duplicate_keys_or_labels, ::test_global_commands_are_palette_only_not_in_the_bar; tests/test_modal_keys.py::test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys, ::test_TC_2407_every_modal_is_in_the_inventory
- Global screens: tests/test_added_list.py::test_TC_4323_N_brings_the_open_list_back_without_a_second_one, ::test_TC_4317_the_open_list_writes_no_board_and_no_history; tests/test_all_agenda.py::test_TC_2401_where_A_acts_and_what_it_holds, ::test_TC_2401_the_unlisted_board_is_the_last_lane
- Creation, saving, undo: tests/test_app.py::test_add_task_modal_appears, ::test_add_project; tests/test_templates_app.py::test_pick_simple_chain_inserts_three_linked_tasks_and_one_undo; tests/test_control_bytes.py::test_TC_410_a_saved_board_round_trips; tests/test_rescue.py::test_one_bad_task_never_empties_the_board
- Store: tests/test_people_directory.py::test_TC_2501_two_windows_never_erase_each_others_people, ::test_TC_2501_a_failed_write_changes_nothing_in_memory, ::test_TC_2501_an_unparseable_file_is_kept_aside_before_it_is_replaced, ::test_TC_2501_an_unreadable_file_is_kept_aside_and_the_directory_starts_empty, ::test_TC_2501_a_held_lock_makes_the_write_wait_then_fail_and_change_nothing; tests/test_marks_directory.py::test_TC_2603_the_corrupt_copy_is_never_replaced; tests/test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size, ::test_TC_2702_a_failed_refresh_keeps_and_flags_once, ::test_AT_2706_the_directories_stay_fresh, ::test_AT_2707_a_failed_re_read_keeps_the_directory; tests/test_boards_concurrency.py::test_TC_2301_the_lock_is_exclusive_and_released, ::test_TC_2301_a_stale_lock_is_taken_over_and_a_fresh_one_is_not
- Image and ink: tests/test_app.py::test_save_pil_image_increments, ::test_clipboard_paste_saves_and_appends; tests/test_colour_pens.py::test_TC_4230_alt_n_opens_a_spaced_pair_with_the_cursor_inside, ::test_TC_4231_typing_under_a_pen_stays_inside_its_span, ::test_TC_4249_esc_digit_parses_as_alt_digit_after_the_import

## Probes (run on incK-marks, `taskboard.__file__` = incK-marks; synthetic data in a temp folder; scripts in `%TEMP%\incK-probe\`, not committed)

- **P-1 (keys):**
  - `app_bindings()` holds `N` and no `n`; no KEYMAP key holds `alt`.
  - Every `alt+`/`n`/`u` binding of every DOMNode class in app, modals, views and keymap was enumerated (the table above).
  - Textual's own: TextArea `alt+backspace`, `alt+delete`; Input `alt+backspace`.
  - Parser (after importing modals): ESC CR → `enter`; ESC d/o/n/a/i/u → `alt+d/o/n/a/i/u`; ESC 5 → `alt+5`; `CSI 13;3u` → `alt+enter`; `CSI 100;3u` → `alt+d`.
- **P-2 (store):**
  - Load missing → 0 people, no file. Then d1 `add("Ana Ruiz","Legal")` → `ana.ruiz`, and stale d2 `add("Ana Ruiz")` → `ana.ruiz2`: both are in the file.
  - `d1.refresh()` → True, then None. No `.lock` left.
  - The file made "{not json": `refresh()` → False, people kept. A load → unreadable + `people.json.corrupt`; then `add("Bo Lin")` → the file holds `[bo.lin]`, still one copy. `keep_aside` again → `people.json.corrupt-2`.
  - A fresh foreign lock → OSError after 2.0 s, "Inbox is busy — another taskboard is writing it; try again in a few seconds".
- **P-3 (board):**
  - Boards a (`pa`, `t0`) and b (`pb`, `t0`). `peek_board(b)` → `[t0]`, default phases. On that object `add_task(Task("Dumped", id="tdump001"))` → the file order `[t0, tdump001]`, `created` = the history `at` (`2026-11-01T04:45:38`), the line `"from": null`.
  - `image_dir` → `b/images/tdump001`, not created. `add_project("New one")` → the file's projects `[pb, pn]`.
  - Peek of a missing path → 0 tasks, default phases, no file. `Board.load` of a missing path → 16 tasks.
  - Two `Board.load(a)` objects each `add_task` → the file `[t0, ttwo0001]` (the first add lost).
- **P-4 (app, headless `run_test` 118x30, two-board registry Main/Side):**
  - The home is on top at start. `board_lanes` → `[("Main","violet",[ta1],""), ("Side","cyan",[tb1],"")]`, `["main","side"]`; lane 0's board `is app.board`.
  - `n` → no screen, no task. `_on_task_added` → `[ta1, tadd0001]`, undo stack `[]`; `u` → "Nothing to undo.".
  - `_on_project_added({"name": "Gamma", …})` → in memory and in the file.
  - `N` → `[Screen, AddedList]`. Then `check_action("add_task")` → False and `check_action("capture")` → True.
  - `switch_board("side")` → undo stack `[]`.
- **P-5 (image and ink):**
  - `save_pil_image` → `b/images/tdump001/paste-001.png`, then `paste-002.png`.
  - `highlight_segments("a ::r:: red :: b ==soon== @ana.ruiz")` → `[("a ","mut"),("red","over"),(" b ","mut"),("soon","soon"),(" @ana.ruiz","mut")]`, and `"____"` → `[("____","mut")]`.
  - `ink_highlights(["a ::r:: red :: b","____","plain"])` → `{0: [(2,8,"pen.mark"),(8,11,"pen.over"),(11,14,"pen.mark")]}`.

The `# node:` marks remain uncommitted in incK-marks: 31 lines in app.py (9), models.py (7), people.py (6), boards.py (3), modals.py (3), keymap.py (2) and views.py (1). Nothing in taskboard/ or tests/ of capture-proto was touched.

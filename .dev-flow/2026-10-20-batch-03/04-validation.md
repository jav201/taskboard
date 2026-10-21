# Validation — taskboard — Batch 2026-10-20-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)


- **Result:** `PASS-WITH-NOTES`
- **Gate run:** `python -m pytest -q -p no:cacheprovider --color=no -rs <chunk files>` over `ls tests/test_*.py | sort` (101 files) in three sequential chunks · exit 0, 0, 0 · `8f0fe85` (a clean worktree `<scratchpad>/b03/wt-p4`, 0 changed files, `NO_COLOR` unset) · the orchestrator — 1398 + 857 + 770 = 3025 passed, 0 failed, 0 skipped, equal to the 3025 collected (`evidence/suite-p4-chunk00..02.txt`, `evidence/suite-p4-summary.txt`, `evidence/collect-p4.txt`). **The second pass.** The first pass at `1647442` failed one standing law — `tests/test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person` (1398 + 857 + 769 passed, 1 failed; `evidence/first-suite-p4-chunk02.txt`, chunk02 exit 1). That law caught increment 003's `--open` notice, which said "your". The fix landed in `8f0fe85` (LED .9, `evidence/p4fold.diff`), and this run followed it.
- **Layer 0:** 4 unit(s) met the criterion (`keymap.key_line`'s fit, `views.all_agenda`'s buckets, `views.present_all_export`'s cut, the presence reader `boards.open_elsewhere`) · 4 carry a named reddening mutation (mutation-001 key arms, mutation-002 export arms, mutation-003 marker arms, mutation-004 agenda arms)
- **Requirements:** 25/25 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative. Each packet's B1 census was green in its targeted run, and the whole suite is green at the gate. The note: two targeted runs (001, 003) did not list a project-wide law suite, so two regressions escaped to later gates (G-1, G-2)
- **Test ledger:** ✓ reconciles (`2962 − 0 + 63 = 3025`)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 25 of 25 rows ✓ with evidence` (an evaluation of the orchestrator's gate run; the qa-reviewer did not run the suite)


---

## Detail (reference)

The qa-reviewer evaluated these rows from the orchestrator's transcripts. It was spawned with its role file, independent of the author, and was read-only toward the repo. The orchestrator writes the rows below from its return. Each result's state is `executed`, by the orchestrator: the two gate passes, the REDs on each increment's base, the mutation batteries, and the real Windows Terminal captures. The qa-reviewer reran no suite. What it did itself, all by inspection:
- read the transcripts;
- compared the chunk lists' union with `git ls-tree 8f0fe85 tests/` (101 = 101, identical);
- counted the four new files' nodes in `collect-p4.txt` (28 + 14 + 15 + 6 = 63);
- viewed 8 of the 32 PNGs;
- measured the dark-pixel share of all 32 PNGs.

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `keymap.key_line` (the fit: whole · words dropped before keys · keys only) | decision (three width branches) | `tests/test_modal_keys.py::test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys` | pass |
| `views.all_agenda` / `render_all_agenda` (buckets, order, Sunday, width) | boundary (Sunday, a due on Sunday, no dues) + decision (done/archived excluded, lane order) | `tests/test_all_agenda.py::test_TC_2401_buckets_and_dues`, `…::test_TC_2401_every_row_is_the_width_and_board_text_is_literal[118]`, `[80]` | pass |
| `views.present_all_export` (no cursor, cut to content, anchor) | boundary (a full frame; no shown project) | `tests/test_present_backlog_round.py::test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content` | pass |
| `boards.open_elsewhere` and the marker writer (fresh / stale / future / wrong shape / foreign / directory / unwritable) | boundary (119 s / 121 s, 121 s ahead) + decision (mine, other board, shape) | `tests/test_boards_backlog_round.py::test_TC_2409_the_markers` | pass |

**Measured by mutation, never by line coverage.** For each unit, the mutation and its RED:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `key_line` | a key dropped before the words; the slash styled as a key; `ConfirmModal`'s key line emptied | yes — KILLED ×3 (of 17/17 arms) | `evidence/mutation-001.txt` |
| `all_agenda` | the lane order dropped from the sort (×2); done tasks listed; Sunday excluded; the project column at 80 | yes — KILLED ×5 (of 15/15 arms) | `evidence/mutation-004.txt` |
| `present_all_export` | the cursor kept; the cut dropping a content row; no cut; anchored on no project; back on the screen's timeline | yes — KILLED ×5 (of 16/16 arms) | `evidence/mutation-002.txt` |
| `open_elsewhere` / markers | stale test inverted; `abs` dropped; its own marker counted; name pattern ignored; regular-file check dropped; an empty marker left after a failed write; an offset `since` kept | yes — KILLED ×7 (of 24/24 arms) | `evidence/mutation-003.txt` |

### UX walkthrough — only if trigger family D fired

Family D fired: every item changes what the operator sees or presses.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| when the operator presses `A` on the home, they see every board's week with lanes in registry order, `TODAY` chosen; `enter` lands on the task's board with the task selected | AT-2401 (`run_test`, keys); WT `agenda_118x30.png`, `agenda-open_*` | the head, lanes, key row (tail dropped whole at 80); the selected task; each board file's bytes | pass |
| when the presenter opens a presentation on a labelled board, the hint row starts with the chip and the slide/export never shows it | AT-2402; WT `present-chip_*` | the hint's text; the frame; the SVG's rows | pass |
| when the presenter presses `?`, a window lists every key with this view's keys bright and other views' keys dim | AT-2403; WT `present-keys_118x30.png` (viewed: readable box, 5 colours, CopyFromScreen) | the window's text and styles at `⇧↑↓ K J` and `pgdn pgup` | pass |
| when the presenter exports view 3, the file reads as a slide (no `⟦`, no `project span`, 21 rows) | AT-2404; `present-export-file_80x24.png` (viewed: no cursor, ends at content) | the SVG's rows; the PNG's size `(width, 21)` | pass |
| when the operator sees a confirmation, its whole message wraps and `y archive  n / esc cancel  ⇥ the buttons` is under it; `enter` answers nothing | AT-2406; WT `confirm_80x24.png` (viewed: whole message over 3 rows, key line) | the message, the key line, the registry after `n` and `y` | pass |
| when the operator types in a form, plain letters type and `alt+s` saves; the key line stays on screen when the box scrolls | AT-2407; WT `project-form_80x24.png` (viewed: line docked at the box's foot), `task-editor_*` | the painted key lines at both sizes; the saved task/project/clock/template; cancelled bytes | pass |
| when a start-up modal appears, its title opens with the board's chip | AT-2408; WT `offer_*`, `identity_80x24.png` (viewed: chip `Client A` before `Operator identity`) | the titles; the identity key line | pass |
| when a second window opens the same board, it reads one `open twice` notice | AT-2409; WT `twice_80x24.png` (viewed: `Client A is already open in another taskboard window (since 09:12)…`) | the notices; the marker count 1 → 2 → 1 → 0 | pass |
| when the operator runs `--open PATH`, the board opens with the chip `board-copy · not listed` and a notice in the app's voice | AT-2410; WT `open_118x30.png` (viewed, re-shot after `8f0fe85`: "…without adding it to the boards (--open). B lists the 3 boards…") | the head row, the label, the notice's exact text, `boards.json`'s bytes | pass |

**Mechanism used:** `a UI test driver`: Textual's headless `run_test`, with the real app built by the shipped `open_app` / `__main__.main` / `TaskboardApp`. Alongside it, real Windows Terminal captures at 118×30 and 80×24 from `evidence/captures/shoot_real.ps1`.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — ux-reviewer at P2/PDR (UX-1..UX-24) and at the DDR over all 30 PNGs (UX-DDR-1..8) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the captures go to the operator at the close as not yet verdicted (PC-1) |

- **Method:** the ATs above, run in the gate run; the ux-reviewer's DDR read of every capture; this reviewer's view of 8 PNGs (`open_118x30`, `agenda_118x30`, `present-keys_118x30`, `twice_80x24`, `project-form_80x24`, `identity_80x24`, `confirm_80x24`, `present-export-file_80x24`).
- **Participants or population:** none (no user evaluation).
- **Evidence of the evaluation:** `evidence/suite-p4-chunk00..02.txt`; `evidence/captures/png/*.png` and `capture-log.txt`; `design/DDR-2026-10-20-batch-03.md` §B PC-1, PC-5.
- **PC-5 (no black capture counts):** re-read at P4 — none of the 32 PNGs is black. The 30 terminal shots have a dark-pixel share of 53–92 %, readable text, 5–46 colours sampled, and every one is logged `ok … window closed`. The black shots of earlier loaded runs are superseded in `capture-log.txt`. The two `present-export-file_*` PNGs are rasterised exports, not terminal shots.
- **Limits:**
  - "Another window" is a second `TaskboardApp` in the same process, not a second terminal. The WT `twice_*` shots show the notice, but not two live windows.
  - `open_118x30.png` / `open_80x24.png` (the re-shoot after the fix) are uncommitted at `8f0fe85` (G-6).
  - No real user has used the build.

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2401 | test | AT-2401 `tests/test_all_agenda.py::test_AT_2401_one_screen_for_every_board` | as in §3 | pass · RED on 003's commit · M1–M15, D4 KILLED | `red-004.txt`, `mutation-004.txt`, `mutation-ddr.txt` D4, the gate run |
| LLR-2401.1 | test (unit) | TC-2401 `…::test_TC_2401_buckets_and_dues`, `…every_row_is_the_width_and_board_text_is_literal[118/80]` | as in §4 | pass · sort / done / Sunday / column-at-80 arms KILLED | `mutation-004.txt` |
| LLR-2401.2 | test (unit) | TC-2401 `…::test_TC_2401_where_A_acts_and_what_it_holds`, `…the_unlisted_board_is_the_last_lane` | as in §4 (LED .7) | pass · `A` on home, seat keys behind, jump, unlisted lane/jump, failed switch arms KILLED | `mutation-004.txt` |
| HLR-2402 | test | AT-2402 `tests/test_present_backlog_round.py::test_AT_2402_the_presenter_reads_the_board_the_slide_never_does` | as in §3 | pass · RED on 001's commit · chip arms KILLED | `red-002.txt`, `mutation-002.txt` |
| LLR-2402.1 | test (unit) | TC-2402 `…::test_TC_2402_the_hint_opens_with_the_chip`, `…the_chip_never_costs_the_keys[2]` | as in §4 | pass · chip dropped ×2, chip in frame, M2b (CR-1) KILLED | `mutation-002.txt` |
| HLR-2403 | test | AT-2403 `…::test_AT_2403_question_mark_shows_every_key` | as in §3 (LED .5) | pass · RED · live/dim AT arm KILLED (after a SURVIVED first run, repaired) | `red-002.txt`, `mutation-002.txt` |
| LLR-2403.1 | test (unit) | TC-2403 `…::test_TC_2403_the_bindings_are_the_seat` | as in §4 | pass · a binding outside the seat KILLED | `mutation-002.txt` |
| LLR-2403.2 | test (unit) | TC-2403 `…::test_TC_2403_the_window_is_the_seat_live_by_view[2]` | as in §4 | pass · `?` unbound, live/dim inverted, `? keys` dropped KILLED | `mutation-002.txt` |
| HLR-2404 | test | AT-2404 `…::test_AT_2404_the_export_reads_as_a_slide[size0-93]`, `[size1-80]` | as in §3 | pass · RED (29 rows, `⟦`) | `red-002.txt`, `mutation-002.txt` |
| LLR-2404.1 | test (unit) | TC-2404 `…::test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content` | as in §4 | pass · 5 export arms KILLED | `mutation-002.txt` |
| HLR-2405 | test | AT-2405 `…::test_AT_2405_K_and_J_reorder` | as in §3 | pass · RED · `K`/`J` unbound KILLED; `J` not saved D3 KILLED | `red-002.txt`, `mutation-002.txt`, `mutation-ddr.txt` D3 |
| LLR-2405.1 | test (unit) | TC-2405 `…::test_TC_2405_the_hint_names_K_J[2]` | as in §4 | pass · a wording without `K J` KILLED | `mutation-002.txt` |
| HLR-2406 | test | AT-2406 `tests/test_modal_keys.py::test_AT_2406_a_confirmation_is_one_written_key[size0/size1]` | as in §3 (LED .4) | pass · RED on base (26 failed, 2 boundary arms pass by design) · `y` unbound, `MoveConfirm` on `enter` AT arms KILLED | `red-001.txt`, `mutation-001.txt` |
| LLR-2406.1 | test (unit) | TC-2406 `…::test_TC_2406_a_confirmation_answers_y_and_n_and_not_enter[4]`, `…the_message_wraps_and_is_whole`, `…the_move_confirms_on_y_never_on_enter`, `…key_line_is_the_key_bar_style…` | as in §4 | pass · wrap ×2, key line, slash arms KILLED · the escaped CSS-order regression (TC-204) folded at the DDR (LED .8) | `mutation-001.txt`, `suite-ddr-first.txt` → `suite-ddr.txt` |
| HLR-2407 | test | AT-2407 `…::test_AT_2407_alt_s_saves_and_letters_type[size0/size1]` | as in §3 (LED .4, .8) | pass · RED · `alt+s` pressing Cancel KILLED; D1, D1b, D2 KILLED | `red-001.txt`, `mutation-001.txt`, `mutation-ddr.txt` |
| LLR-2407.1 | test (unit) | TC-2407 `…::test_TC_2407_alt_s_does_what_save_does[5]`, `…alt_t_and_alt_d_open_the_calendars[4]`, `…alt_i_pastes_an_image`, `…every_modal_is_in_the_inventory`, `…every_button_has_its_key[6]` | as in §4 | pass · the law's unbound key, `alt+t` → due, `alt+i`, editor/`TextPrompt` lines KILLED | `mutation-001.txt` |
| HLR-2408 | test | AT-2408 `tests/test_boards_backlog_round.py::test_AT_2408_the_start_up_modals_say_their_board` | as in §3 | pass · RED on 002's commit | `red-003.txt`, `mutation-003.txt` |
| LLR-2408.1 | test (unit) | TC-2408 `…::test_TC_2408_the_titles_open_with_the_chip` | as in §4 | pass · the offer's chip dropped, no label passed KILLED | `mutation-003.txt` |
| HLR-2409 | test | AT-2409 `…::test_AT_2409_a_second_window_is_told_once` | as in §3 | pass · RED · notice-as-markup (S-1) KILLED | `red-003.txt`, `mutation-003.txt` |
| LLR-2409.1 | test (unit) | TC-2409 `…::test_TC_2409_the_markers` | as in §4 (LED .6) | pass · 7 marker arms KILLED (Layer 0) | `mutation-003.txt` |
| LLR-2409.2 | test (unit) | TC-2409 `…::test_TC_2409_the_lifecycle` | as in §4 | pass · no presence at opening, left at exit, left at switch, not re-announced, `renew` time KILLED | `mutation-003.txt` |
| HLR-2410 | test | AT-2410 `…::test_AT_2410_open_without_registering` | as in §3 (LED .9) | pass · RED (`--open` unknown, exit 2) · D5b KILLED (second-person notice) | `red-003.txt`, `mutation-003.txt`, `mutation-ddr.txt` D5b |
| LLR-2410.1 | test (unit) | TC-2410 `…::test_TC_2410_open_app_registers_nothing`, `…open_of_a_registered_path_is_that_board`, `…a_path_that_is_no_board_is_refused[5]`, `…open_and_board_together_are_refused` | as in §4 | pass · `--open` check removed ×2, registering ×2 KILLED | `mutation-003.txt` |
| LLR-2410.2 | test (unit) | TC-2410 `…::test_TC_2410_the_unlisted_board_in_the_app`; the voice law `tests/test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person` | as in §4 (LED .6, .8, .9) | pass at `8f0fe85` · FAILED at `1647442` (first pass) · D5 KILLED | `first-suite-p4-chunk02.txt`, `mutation-ddr.txt` D5, `suite-p4-chunk02.txt` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2401 | AT-2401 | `open_app`, the home's `A`, `enter`, `A` `down` `enter`, at 118×30 and 80×24 | the agenda's rows (head, lanes `Personal/Client/Course`, key row); the selected task on Personal and on Client A; every board file byte-identical | repr (two jumps across boards) · boundary (80×24: the tail `read-only` dropped whole, every key kept) · negative (no file written — D4 KILLED; `Fitness block` absent) | pass |
| US-2402 | AT-2402 | `R` on Client A, `x`, `3`, `x` | the hint `Client A  1 gantt…`; two exported SVGs with no `Client A` in any row; a one-board app's hint starts `1 gantt` | repr · boundary (one board: no chip) · negative (the chip never in the frame or the export) | pass |
| US-2402 | AT-2403 | `R`, `3`, `?`, `?`, `x`, `1`, `?`, `esc`; each view at 118 and 80 | the `PresentKeys` window's text and styles; the frame unchanged after close; the export's bytes unchanged by the window; every hint ends `? keys` | repr · boundary (80 columns) · negative (the window never reaches an export) | pass |
| US-2402 | AT-2405 | `R`, `3`, `down`, `K`, `J` at 118 and 80 | the rail order; the board file's project order after `K` AND after `J` | repr · boundary (back to the start) · negative (`J` unsaved — D3 KILLED) | pass |
| US-2403 | AT-2404 | `R`, `3`, `x` at 118×30 and 80×24 | `reports/present-board-*-all.svg` read row by row (21 rows, no `⟦`, no `project span`, every project named); the PNG asked for `(width, 21)` | repr · boundary (both sizes) · negative (the screen keeps its cursor; the file has none) | pass |
| US-2404 | AT-2406 | the home's `left`, `x`, `enter`, `n`, `x`, `y`; a task's `d`, `y`; `P`, `down`, `m`, `enter`, `y` | the whole message and key line; `boards.json`'s `archived`; the task gone; the project count minus 1; the notices | repr · boundary (80×24 wrap) · negative (`enter` answers nothing, `n` archives nothing) | pass |
| US-2404 | AT-2407 | `a` `Draft s` `alt+s`; `e` `alt+d`; `p` `tab` `Site` `alt+s`; `c` `alt+s`; `I` `enter` … `alt+s` | the saved task `Draft s` selected; the calendar; the project `Site`; `clock1`; the template; the painted key lines at both sizes; `board.json` unchanged after a cancel | repr · boundary (80×24: words dropped, `esc cancel` whole; line docked — D1/D1b/D2 KILLED) · negative (plain `s` types) | pass |
| US-2405 | AT-2408 | a start with Client A's offer pending; `escape`; the home's `left` `down` `enter` to Course | the offer's title ` Client A  ◆ Milestones…`; the identity picker's ` Course … Operator identity`; its key line `↵ pick   esc cancel`; a one-board start's title without a chip | repr · boundary (one board: no chip) · negative (no chip without a label) | pass |
| US-2406 | AT-2409 | two `TaskboardApp`s on Client A; the first switches to Course; both exit; a third starts | exactly one `open twice` notice in the second; marker count 1 → 2 → 1; Course's marker only; `[]` at the end; nothing in the third | repr · boundary (the switch withdraws the marker) · negative (the first window, and the third after both exit, are told nothing) | pass |
| US-2407 | AT-2410 | `__main__.main` with `--open elsewhere/board-copy.json` (argv), then `B`, `escape` `P` `down` `m` | `boards.json` byte-identical; head ` board-copy · not listed `; the notice's exact text; `B` lists the three boards; the move refused with `This board is not listed (--open)` | repr · boundary (a registered path — TC-2410) · negative (nothing registered; the move refused) | pass |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `A`, bucket `←→`, task `↑↓`, `enter`, `esc` | `TaskboardApp.action_agenda_all`, `AllBoardsAgenda` | yes (home and main screen keys) | AT-2401, TC-2401 | ✓ |
| input | `?`, `K`, `J` in the presentation | `PRESENT_KEYS` / `present_bindings`, `PresentScreen.action_keys` | yes (`R` then the keys) | AT-2403, AT-2405 | ✓ |
| input | `x` (view-3 export) | `views.present_all_export` | yes | AT-2404 | ✓ |
| input | `y` / `n` / `esc` / `enter` in a confirmation | `ConfirmModal`, `MoveConfirm` | yes (home `x`, task `d`, `P` `m`) | AT-2406 | ✓ |
| input | `alt+s` / `alt+i` / `alt+t` / `alt+d` | `ButtonKeysMixin.action_press_button` | yes (`a`, `e`, `p`, `c`, `I`) | AT-2407, TC-2407 | ✓ |
| input | a second window on the same board | `boards.mark_open` / `open_elsewhere` | yes (a second `TaskboardApp` built by the shipped path) | AT-2409 | ✓ |
| input | `--open PATH` (and with `--board`, a missing path, a folder) | `__main__.main` / `open_app(unlisted=)` | yes (argv through `main`) | AT-2410, TC-2410 | ✓ |
| output | the agenda screen; the jumped-to board and task | `render_all_agenda`, the switch | yes (screen text, `app.selected_task`) | AT-2401 | ✓ |
| output | the board files left unwritten by the agenda | — (the agenda writes nothing) | yes (bytes compared) | AT-2401 | ✓ |
| output | the hint chip; the `PresentKeys` window | `PresentScreen._hint`, `modals.PresentKeys` | yes | AT-2402, AT-2403 | ✓ |
| output | `reports/present-board-*-all.svg` / `.png` | `present_all_export`, `action_export` | yes (SVG rows; PNG size) | AT-2404, AT-2402 | ✓ |
| output | the board file's project order after `K`/`J` | the reorder's save | yes | AT-2405 | ✓ |
| output | the confirmation's message and key line; `boards.json`; the board file | `ConfirmModal`, `Registry.archive`, `move_project` | yes | AT-2406 | ✓ |
| output | the forms' key lines; saved task/project/clock/template | the form modals | yes | AT-2407 | ✓ |
| output | the start-up titles with the chip | `MilestoneOffer`, `TeamIdentityPicker` | yes | AT-2408 | ✓ |
| output | the presence marker files; the `open twice` notice | `boards.presence_dir()`, the notice | yes (marker count; notice text) | AT-2409, TC-2409 | ✓ |
| output | the `not listed` chip, the `--open` notice, `boards.json` untouched | `TaskboardApp` (unlisted), `__main__` | yes | AT-2410 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2962 | 0 | 63 | 3025 | 3025 | — / 3025 | yes |

The base is batch-02's gate total at `base_ref` (`1fd667b`). +A is the four new files counted in `collect-p4.txt`: `test_modal_keys.py` 28, `test_present_backlog_round.py` 14, `test_boards_backlog_round.py` 15, `test_all_agenda.py` 6. The modified suites keep their def counts, and one declared rename (TC-1904, increment 002) nets 0 (DDR §B row 5). The fold `8f0fe85` changed one assertion and added no node.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | LLR-2406.1 | **Increment 001's targeted run (`suite-001.txt`) missed `tests/test_colour_budget_app.py`.** Its B1 census keyed on modal class names, not on the stylesheet it edited. The `#confirm-box .modal-title` rule placed before `.modal-title` broke TC-204, and the break escaped to the DDR (`suite-ddr-first.txt`: 1 failed). It is fixed in `1647442` (LED .8). No mutation arm re-proves the rule order: the pre-fix RED is the DDR run itself, by an existing node | major (process) | A census for an edit to `taskboard.tcss` greps the selectors and the colour/budget law suites; add a mutation arm "the confirm-title rule before `.modal-title`" to a later battery |
| G-2 | LLR-2410.2 | **Increment 003's targeted run (`suite-003.txt`) missed `tests/test_prism_laws.py`.** The `--open` notice's "your" escaped two gates (003's packet and the DDR) and failed the P4 gate's first pass (`first-suite-p4-chunk02.txt`). The copy was taken from the round's prototype, which the voice law forbids. Fixed in `8f0fe85` (LED .9; D5, D5b KILLED). Increments 002 and 004 did not list that suite either (`grep -c test_prism_laws suite-00{1..4}.txt` = 0) | major (process) | Every targeted run includes the project-wide source laws (`test_prism_laws.py`, `test_colour_budget_app.py`, `test_markup_census.py`, `test_markup_sites.py`) whenever a printed string or a stylesheet changes. Log the round-copy vs voice-law conflict as an OPERATOR item (done: `BACKLOG.md`) |
| G-3 | HLR-2409 | §5.2 says "no presence marker left by any test". Only AT-2409 asserts `_markers() == []` at the end. Elsewhere, containment comes from the per-test fake home (`tests/conftest.py::_never_the_real_home`), not from a suite-wide count of leftover markers | minor | Accepted: the fake home keeps markers out of the real home. A suite-wide finaliser is optional backlog |
| G-4 | HLR-2403 | At 80 columns the gantt hint no longer names `next` / `show all`; only `?` does. This supersedes HLR-2002's wording (LED .5, D-14) | minor | An OPERATOR item at the close (already in `BACKLOG.md`) |
| G-5 | HLR-2401..HLR-2410 | The real WT captures are not verdicted by the operator (PC-1). `present-keys_118x30`, `offer_80x24` and `identity_*` needed the CopyFromScreen fallback (PrintWindow gave 5–7 colours). The ones viewed are readable | minor | Hand the 32 PNGs to the operator at the close as unverdicted |
| G-6 | HLR-2410 | `evidence/captures/png/open_118x30.png`, `open_80x24.png` and `capture-log.txt` were re-shot after `8f0fe85` and are uncommitted. The committed PNGs show the old "your" notice | minor | Commit the re-shot PNGs and log with the P4 record |
| G-7 | HLR-2406 | Increment 001 deferred `test_milestones.py`, `test_present_hide.py` and `test_link_picker.py` (B1 hits) to P4. They were green at the gate, but the packet's census was not closed inside its own run | minor | Same remedy as G-1: a B1 hit runs in the increment's targeted run |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| TC-204 (increment 001's CSS order, found by the DDR) | `evidence/suite-ddr-first.txt` — `FAILED tests/test_colour_budget_app.py::test_TC_204_modal_titles_and_the_key_map_are_bright` (1 failed, 505 passed) | value (the confirm modal's title colour) | yes — the node reads the painted title's style. No mutation arm re-applies the misordered rule (G-1) | pass — `suite-ddr.txt` (506 passed); the gate run | `tests/test_colour_budget_app.py::test_TC_204_modal_titles_and_the_key_map_are_bright` |
| the voice law + AT-2410 (increment 003's `--open` notice, found by P4's first pass) | `evidence/first-suite-p4-chunk02.txt` — `AssertionError: literals in the app's voice: [('app.py', 'to your boards (--open). B lists your {n} ')]` | value (the literal's words) | yes — D5 (law) and D5b (AT-2410's exact notice) KILLED in `mutation-ddr.txt` | pass — `suite-p4-chunk02.txt` (770 passed) | `tests/test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person`, `tests/test_boards_backlog_round.py::test_AT_2410_open_without_registering` |

### Evidence checklist — qa-reviewer (full)

The qa-reviewer's return (P4) checked the following.
- The three chunk lists' 101 unique files equal `git ls-tree 8f0fe85 tests/` `test_*.py`.
- Each chunk of the second pass exited 0.
- 3025 passed equals the 3025 collected.
- The first pass's failure is read and its fix diffed (`p4fold.diff`).
- Each requirement's RED (`red-001..004.txt`) and mutation transcript (`mutation-001..004.txt`, `mutation-ddr.txt`: 17 + 16 + 24 + 15 + 7 arms, 0 not killed) is read.
- PC-5 is re-read: 32 PNGs, none black, 8 viewed.
- The evidence state and the executor (the orchestrator) are named on each row.
- Mode `validation` · Given/When/Then lives in the ATs' docstrings · no real PII (`username_subject` placeholder in `identity_80x24.png`; synthetic boards under temporary homes).

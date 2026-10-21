# Validation — taskboard — Batch 2026-10-21-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Gate run` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** `PASS-WITH-NOTES`
- **Gate run:** `python -m pytest -q -p no:cacheprovider <chunk files>` over `ls tests/test_*.py | sort` (106 files) in three sequential chunks · exit 0, 0, 0 · `27d155f` (the worktree, 0 dirty paths, `NO_COLOR` unset) · the orchestrator — 1398 + 957 + 797 = 3152 passed, 0 failed, 0 skipped, equal to the 3152 collected (`evidence/suite-p4-chunk00..02.txt`, `evidence/suite-p4-chunk00..02-files.txt`, `evidence/suite-p4-summary.txt`, `evidence/collect-p4.txt`)
- **Layer 0:** 6 unit(s) met the criterion (`people.Directory` load/add/edit, the tokeniser `mention_ids`/`split_mentions`/`handle_for`, `modals.pick_rows`, `views.people_by_urgency`/`progress_box`, `views._scroll_tasks`, `views.matches`/`filter_bar`) · 6 carry a named reddening mutation (`mutation-001..005.txt`)
- **Requirements:** 21/21 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative) — one node per AT (C-18, folded at the DDR); AT-2507's push goes through `TeamState`, not a key (logged, G-3)
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — each packet's B1 census ran green in its targeted suite (`suite-001..005.txt`) and the whole suite is green at the gate
- **Test ledger:** ✓ reconciles (`3025 − 0 + 127 = 3152`)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 9 of 11 rows ✓ with evidence` (an evaluation of the orchestrator's gate run; the qa-reviewer did not run the suite; the two ✗ are a notice — acceptance written as numeric thresholds, not Given/When/Then — and this record's own placeholders, filled here)

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

The qa-reviewer evaluated these rows from the orchestrator's transcripts. It was spawned with its role file, independent of the author, read-only toward the repo; the orchestrator writes the rows from its return. Every result's state is `executed`, by the orchestrator: the gate run, the REDs, the mutation batteries, the real Windows Terminal captures. What the qa-reviewer did itself, by inspection: compared the chunk lists' union with `git ls-tree 27d155f tests/` (106 = 106, no duplicates); grepped every chunk for `failed`/`skipped`/`xfail` (0); reconciled the ledger against batch-03's gate (`git diff 8f0fe85 eac7d42 -- tests` empty); re-hashed the 26 packet digests at the DDR; ran the five people suites once in a scratch copy at the DDR (123 passed).

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `people.Directory.load` / `add` / `edit` (read never raising, the lock, the re-read, caps, the corrupt copy) | boundary (61/201 chars, `{oops`, empty file) + decision (repeated handle, lock held) | `tests/test_people_directory.py::test_TC_2501_*` | pass |
| the tokeniser `mention_ids`, `split_mentions`, `mention_line`, `handle_for` | boundary (e-mail, trailing `.`, link form) + decision | `tests/test_people_directory.py::test_TC_2502_*` | pass |
| `modals.pick_rows` | decision (`+ add` for an exact name or `@` alone) | `tests/test_people_picker.py::test_TC_2503_*` | pass |
| `views.people_by_urgency`, `progress_box` | decision (late > today > open) | `tests/test_people_view.py::test_TC_2504_today_outranks_a_longer_list`, the box arms | pass |
| `views._scroll_tasks` (the cursor's task and quote kept, the marker) | boundary (heights 14–24) | `tests/test_people_view.py::test_TC_2504_a_quote_is_never_shown_without_its_task[*]`, `…the_cursor_and_its_quote…` | pass |
| `views.matches` / `filter_bar` | decision (exact handle, case) | `tests/test_people_search.py::test_TC_2505_*` | pass |

**Measured by mutation, never by line coverage.**

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `Directory` | write skips the re-read; lock dropped; repeated handle kept; cap dropped; no corrupt copy | yes — KILLED (of 17/17) | `evidence/mutation-001.txt` |
| tokeniser | look-behind dropped; handle may end in `.`; quadratic dedupe | yes — KILLED (of 17/17) | `evidence/mutation-001.txt` |
| look | mention outside its segment; NBSP a space; the card's token | yes — KILLED (of 14/14) | `evidence/mutation-002.txt` |
| `pick_rows` / picker | `+ add` for an exact name; `enter` acting while closed; `tab` losing `focus_next` | yes — KILLED (of 13/13) | `evidence/mutation-003.txt` |
| view | done task owed; urgency drops `today`; quote not under its task; scroll window (CR-1) | yes — KILLED (of 19/19) | `evidence/mutation-004.txt` |
| search | person rule falls through; partial handle; bar unnamed; list capped at 8; case-sensitive lookup | yes — KILLED (of 13/13) | `evidence/mutation-005.txt` |
| the DDR's keyed ATs | `n` adds no one; the edit keeps the old name | yes — KILLED (2/2) | `evidence/mutation-ddr.txt` |

### UX walkthrough — only if trigger family D fired

Family D fired: every item changes what the operator sees or presses.

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| when the operator presses `@`, they see who needs them most, the chosen person's box `N late · N today · N open` and their open tasks of every board, each with the note line that mentions them | AT-2504 (`run_test`, keys, both sizes); WT `pv_118x30.png`, `pv_80x24.png` | the head, `▶ Ana Ruiz`, the box, `“Waiting on @Ana Ruiz`, the key row per pane | pass |
| when the operator types `@an` in a task's notes, a list under the cursor offers Ana Ruiz, Andrés Lima, `+ add 'an'`; `enter` writes `@ana.ruiz` and the preview reads `@Ana Ruiz` | AT-2503; WT `mt-list_*`, `mt-flip_80x24.png` (flips up), `mt-add_*`, `mt-done_*` | the list's rows and position, the saved notes, the preview | pass |
| when the operator types `/` then `@an`, names only are listed; `enter` filters the kanban/gantt to that person's tasks and the bar names them | AT-2505; WT `sr-list_*`, `sr-res_*` | `PEOPLE · names only`, `/ @Ana Ruiz`, the tasks shown and hidden | pass |
| when a note mentions a person, the details, the kanban card and the presentation draw `@Name` in pink | AT-2506; WT `m-det_*`, `m-kb_*`, `m-pr_*` | the text and its colour in each | pass |
| when the operator adds or renames a person, every board draws the current name and no board file holds the directory | AT-2501, AT-2502 (keyed at the DDR) | `people.json`, the board files, the details' text | pass |

**Mechanism used:** `a UI test driver`: Textual's headless `run_test` over the real app built by `open_app`; alongside it, real Windows Terminal captures at 118×30 and 80×24 (`evidence/captures/shoot_real.ps1`).

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — ux-reviewer at P2/PDR (UX-1..UX-11) and at the DDR over all 30 PNGs (UX-DDR-1..6) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-person team; the captures go to the operator at the close (PC-1) |

- **Method:** the ATs above in the gate run; the ux-reviewer's DDR read of every capture.
- **Participants or population:** none (no user evaluation).
- **Evidence of the evaluation:** `evidence/suite-p4-chunk00..02.txt`; `evidence/captures/png/*.png`, `capture-log.txt`, `evidence/captures/README.md`; `design/DDR-2026-10-21-batch-01.md` §B PC-1.
- **Limits:** `PersonForm` is clipped at 80×24 (UX-DDR-1, logged, not fixed); the composed people view is not yet verdicted by the operator; no real user has used the build.

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-2501 | test | AT-2501 `tests/test_people_directory.py::test_AT_2501_one_directory_for_every_board` | as in §3 (LED .7) | pass · RED on `base_ref` · D1 KILLED | `red-001.txt`, `mutation-001.txt`, `mutation-ddr.txt` |
| LLR-2501.1 | test (unit) | TC-2501 load arms (`test_people_directory.py`) | as in §4 | pass | `mutation-001.txt` |
| LLR-2501.2 | test (unit) | TC-2501 add/edit, lock, re-read arms | as in §4 | pass | `mutation-001.txt` |
| LLR-2501.3 | test (unit) | TC-2501 `Board.people` arms, `test_TC_2501_another_board_draws_the_same_people` | as in §4 | pass | `mutation-001.txt` |
| HLR-2502 | test | AT-2502 `tests/test_people_look.py::test_AT_2502_a_renamed_person_draws_the_new_name_and_the_note_keeps_the_handle` | as in §3 (LED .7) | pass · D2 KILLED | `mutation-ddr.txt` |
| LLR-2502.1 | test (unit) | TC-2502 tokeniser tables | as in §4 | pass | `mutation-001.txt` |
| HLR-2503 | test | AT-2503 `tests/test_people_picker.py::test_AT_2503_at_an_enter_writes_the_handle_and_the_preview_the_name[*]` | as in §3 (LED .4, .7) | pass · RED on 002's commit | `red-003.txt`, `mutation-003.txt` |
| LLR-2503.1 | test (unit) | TC-2503 `pick_rows` arms | as in §4 | pass | `mutation-003.txt` |
| LLR-2503.2 | test | TC-2503 picker arms (flip-up, `tab`, `esc`, the add form, click-away) | as in §4 | pass | `mutation-003.txt` |
| HLR-2504 | test | AT-2504 `tests/test_people_view.py::test_AT_2504_at_shows_who_needs_what_and_enter_opens_the_task[*]` | as in §3 (LED .5, .7) | pass · RED on 003's commit | `red-004.txt`, `mutation-004.txt` |
| LLR-2504.1 | test (unit) | TC-2504 render, urgency, box, scroll arms | as in §4 | pass | `mutation-004.txt` |
| LLR-2504.2 | test | TC-2504 `@` from the main screen, seat keys behind it, no pile-up, errors | as in §4 | pass | `mutation-004.txt` |
| LLR-2504.3 | test | TC-2504 `n` adds, `e` edits, `/` finds; TC-2407 over `PersonForm` | as in §4 | pass | `mutation-004.txt` |
| HLR-2505 | test | AT-2505 `tests/test_people_search.py::test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks[*]` | as in §3 (LED .6, .7) | pass · RED on 004's commit | `red-005.txt`, `mutation-005.txt` |
| LLR-2505.1 | test (unit) | TC-2505 `matches`, the bar | as in §4 | pass | `mutation-005.txt` |
| LLR-2505.2 | test | TC-2505 `@` alone, `alt+p`, no one, the gantt; TC-2407 over `SearchPrompt` | as in §4 (LED .6) | pass | `mutation-005.txt` |
| HLR-2506 | test | AT-2506 `tests/test_people_look.py::test_AT_2506_details_card_and_presentation_name_the_people[*]` | as in §3 | pass · RED on 001's commit | `red-002.txt`, `mutation-002.txt` |
| LLR-2506.1 | test (unit) | TC-2506 preview, details, card | as in §4 | pass | `mutation-002.txt` |
| LLR-2506.2 | test (unit) | TC-2506 the presentation's notes (NBSP) | as in §4 | pass | `mutation-002.txt` |
| HLR-2507 | test | AT-2507 `tests/test_people_directory.py::test_AT_2507_a_push_carries_mentions_as_handles_and_no_directory` | as in §3 | pass (the push through `TeamState`, G-3) | `mutation-001.txt` |
| LLR-2507.1 | test (unit) | TC-2507 crafted notes in CPU time, foreign tasks | as in §4 | pass | `mutation-001.txt` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-2501 | AT-2501 | `open_app`, `switch_board`, `@` `n` … `alt+s` | `people.json` path and 8 people; one dict for every board; the three board files hold no `people` and no added name | repr · boundary (a switched board) · negative (nothing leaks to a board file) | pass |
| US-2505 | AT-2502 | `@` `e` … `enter`, the details | `@Ana Ruiz Prieto` drawn; the notes keep `@ana.ruiz` | repr · negative (the stored text unchanged) | pass |
| US-2502 | AT-2503 | `e`, the notes, `@an`, `enter`, `alt+s`, both sizes | the list's rows; the saved notes `@ana.ruiz`; the preview `@Ana Ruiz` | repr · boundary (80×24) · negative (`mail ana@x` opens nothing, by its TC arms) | pass |
| US-2503 | AT-2504 | the home's `@`, `tab`, `down`, `enter`, both sizes | the view's rows and box; the task opened on its board | repr · boundary (80×24) · negative (seat keys behind it, by TC) | pass |
| US-2504 | AT-2505 | `4`, `/`, `@an`, `enter`, both sizes | `search_query` `@ana.ruiz`; the bar; tasks shown/hidden | repr · boundary (80×24) · negative («Canary», «Invoice» hidden) | pass |
| US-2505 | AT-2506 | `enter`, `4`, `R` `2`, both sizes | `@Ana Ruiz` in details, card, presentation; no `@ana.ruiz` | repr · boundary (80: the card drops the mention) · negative (no handle drawn) | pass |
| US-2501 | AT-2507 | `TeamState.push` with the directory loaded | the team folder holds only `board.u1.json` with handles and no directory text | repr · negative (no name, role or note leaves) | pass |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `@` in the notes, `↑↓`, `↵`, `esc`, `⇥`, the add form | `TaskModal`'s picker, `pick_rows` | yes | AT-2503, TC-2503 | ✓ |
| input | `@` (home and main screen), `⇥`, `↵`, `n`, `e`, `/`, `esc` | `PeopleDirectory`, `PersonForm` | yes | AT-2504, TC-2504, AT-2501, AT-2502 | ✓ |
| input | `/` then `@…`, `↵`, `alt+p` | `SearchPrompt`, `views.matches` | yes | AT-2505, TC-2505 | ✓ |
| input | `~/.taskboard/people.json` at start (good, unreadable, empty) | `Directory.load` | yes | AT-2501, TC-2501 | ✓ |
| output | `people.json` written under its lock | `Directory.add`/`edit` | yes (file read back) | AT-2501, AT-2503, TC-2501 | ✓ |
| output | `@Name` in pink in details, card, presentation | `notes_preview`, `_card_meta`, `present_note_lines` | yes | AT-2506 | ✓ |
| output | the people view, its box and quotes | `render_people_directory` | yes | AT-2504 | ✓ |
| output | the filtered kanban/gantt and its bar | `filter_bar`, `render_view` | yes | AT-2505 | ✓ |
| output | the team folder after a push | `TeamState.push` | yes (files on disk) | AT-2507 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 3025 | 0 | 127 | 3152 | 3152 | — / 3152 | yes |

The base is batch-03's gate total (`8f0fe85`); `git diff 8f0fe85 eac7d42 -- tests` is empty, so it carries to `base_ref`. +A is the five new files counted in `collect-p4.txt` (45 + 19 + 19 + 32 + 8 = 123) and `test_modal_keys.py` 28 → 32 (+4); `test_keymap.py`, `test_readme.py`, `test_boards_concurrency.py` edited at equal counts; the DDR's 22 renames net 0.

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-1 | — | the P4 evidence (`collect-p4.txt`, `suite-p4-*`) was untracked at `27d155f` | minor | committed with this record |
| G-2 | — | this record's placeholders | minor | filled here |
| G-3 | HLR-2501, HLR-2507 | AT-2501 switches board by `switch_board` and AT-2507 pushes by `TeamState.push`; some TC arms use `.focus()` for a click and set `selected_task_id` directly (QA-DDR-2, QA-DDR-4) | minor | logged in `BACKLOG.md` |
| G-4 | HLR-2504 | `PersonForm` clipped at 80×24 (UX-DDR-1): keys work, the buttons scroll out of view | minor | logged in `BACKLOG.md`, its own increment |
| G-5 | HLR-2501..HLR-2507 | the captures are not yet verdicted by the operator (PC-1) | minor | handed to the operator at the close |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| none — no defect escaped a gate in this batch | | | | | |

### Evidence checklist — qa-reviewer (full)

The qa-reviewer's return (P4), 9 of 11 rows ✓:
- ✓ explicit expected results (§3 thresholds); ✓ empty, boundary, invalid and error arms; ✓ regression — the full suite, 106 files; ✓ exit criteria (§5.2); ✓ synthetic data only (`username_subject` nowhere needed; the round's fixture people); ✓ validation mode declared; ✓ every result attributed to the orchestrator; ✓ Layer B through the shipped surface; ✓ surface reachability both ways.
- ✗ Given/When/Then — §3 states acceptance as numeric thresholds (a notice; the flow's earlier batches read the same way).
- ✗ no unfilled template — G-2, filled by this record.

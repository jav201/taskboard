# PLAN — taskboard — Batch 2026-10-21-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-21-batch-01 |
| Objective | The people round, as the operator's verdict on prototypes/people_round chose: one directory of people (name, role, note) for every board at `~/.taskboard/people.json`; `@` mentions in the notes stored as handles (`@ana.ruiz`), picked from a dropdown under the cursor (variant A); a people view on `@` with two panes (variant A) carrying each task's mentioning note line (from C) and the person's progress box (from B); `/` with `@` filters to a person's tasks (variant A); mentions drawn `@Name` in pink in the details, the kanban card and the presentation (variant A) |
| Last updated | P3 · 2026-10-21 |
| Standing authorization | standing authorization — the orchestrator's commission of 2026-10-21 (the runtime cannot prompt), relaying the operator's request as quoted on the round page and the operator's verdict on the people round, verbatim: «D1: de acuerdo · D2: de acuerdo · D3: de acuerdo · D4: de acuerdo · D5: de acuerdo · formato (storage): handle · 1 view: A · OBJECIÓN: «Estoy de acuerdo con A y robar de C el contexto, pero también robar de B el recuadro de progreso que dice X late X open X today.» · 2 picker: A · 3 search: A · 4 look: A · notes: (none)». Quoted from the commission: «Gates close under it. Do NOT push or merge; stop at the batch close and report», «WORKTREE: … -b feat/people proto/people», «THE DESIGN = the round … port the chosen variants into the real app», «compose it faithfully from the A, B, C renders, and include it in the captures so the operator reviews it», «D4 "de acuerdo" includes whatever the page proposed about the existing team view `9` … apply its proposal», «Also log in BACKLOG.md (not in scope): the presentation's split view shows `!!…!!` and `++…++` markers raw», «max 4 SOURCE files per increment (tests uncapped)», «Every modal button has a direct shown key … `tests/test_modal_keys.py` law must cover new modals», «One directory for all boards at `~/.taskboard/people.json`, written with batch-02's lock/atomic-write pattern», «Team sync must not leak or break on mentions. Synthetic people only», «spawn independent agents (architect at PDR, code-reviewer, qa-reviewer, ux-reviewer, security-reviewer for the new file store) … no self-review», «Real-app captures of each shipped item at 118x30 and 80x24», «full suite in 3 SEQUENTIAL chunks». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents carrying their `agents/<role>.md`); commits on the local branch `feat/people` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); the main checkout (its uncommitted `.gitattributes`) and the other worktrees are not touched; tests never touch the real home. |
| First gate | step 1, on `eac7d42` (`proto/people`, the round on top of `main` `03bae95`), before the rollover: exit 1 — 126 block · 87 notice · 61 not applicable, every BLOCK `V59` naming a file of the commits after the closed batch's `base_ref` `1fd667b` (the round's `prototypes/people_round/` and main's backlog commits), which no closed packet carries; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102` (`evidence/gate-step1.txt`). The rollover re-stamps `base_ref` to `eac7d42`; step 3 (after it): exit 0 — 0 block · 107 notice · 47 not applicable (`evidence/gate-step3.txt`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `03bae952cfb319f7509c17968534bf0f75e65da3`, an ancestor of the worktree's `HEAD` `eac7d42` (`proto/people`); the commission names that base, so no rebase; `base_ref` stamped `eac7d4227b919c995fec153f68aac6f0dfad3c96`. RC-1 (b): not already shipped — on `HEAD` `@` is bound nowhere, no `people.json`, `@` in the notes is text (P-1, P-2, P-3, P-7). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest commit on `origin/main` 2026-10-21 08:19 −0600. Premises: `01-requirements.md` §2.7 (P-1..P-8, all TRUE, `evidence/premises.txt`). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | fired | judged — a new file `taskboard/people.py` in the `models` layer and a new file in the home (`people.json`): `docs/ARCHITECTURE.md` §1, §2 and §4 gain rows (the ARQ amendment) |
| A2 | fired | judged — the planned source files span `models` (`people.py`, `models.py`), `app`, `views`, `modals`, `keymap` |
| A3 | fired | judged — new interfaces consumed across modules: `people.*` (by `app`, `views`, `modals`), `Board.people`, `notes_preview(text, people)`, `TaskModal(…, people=)`, `filter_bar(…, people)`, `board_lanes`/`open_on_board` |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `git grep -l` over `tests/` on `eac7d42`: `TaskModal` → `test_app.py`, `test_edit_window.py`, `test_emoji_picker.py`, `test_markup_sites.py`, `test_milestones.py`, `test_modal_keys.py`, `test_present_hide.py`; `notes_preview` → `test_markup_census.py`, `test_markup_sites.py`; `_card_meta\|kanban_card` → `test_kanban_readable.py`, `test_links.py`; `present_note_lines\|_present_note_markup\|_present_cut` → `test_present_polish.py`, `test_present_views.py`; `filter_bar\|matches(\|filtered_board\|action_search\|"slash"` → `test_app.py`, `test_colour_budget_app.py`, `test_gantt_board.py`, `test_gantt_polish.py`, `test_kanban_readable.py`, `test_milestones.py`, `test_tick_label.py`; `AllBoardsAgenda` → `test_all_agenda.py`; `KEYMAP` → `test_app.py`, `test_archive.py`, `test_boards_home.py`, `test_dependencies.py`, `test_help_keys.py`, `test_kanban_priority.py`, `test_keymap.py`, `test_legend.py`, `test_link_picker.py`, `test_links.py`, `test_momentum.py`, `test_readme.py`, `test_report.py`; `after_move\|_label_board` → `test_boards_backlog_round.py`; `TaskDetails` → `test_app.py`, `test_chainmap_app.py`, `test_details_grid.py`, `test_details_links.py`, `test_details_markup.py`, `test_markup_sites.py`, `test_milestones.py`, `test_modal_keys.py` |
| B2 | not fired | judged — no file changes its location |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | judged — `~/.taskboard/people.json` (read by every later start and by another window), `people.json.lock`, `people.json.corrupt` |
| C1, C2, C4, C5, C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1): `flags: token, role, form, escape` (`evidence/scan-p1.txt`); judged with it — no auth, secret, external integration, destructive operation or network surface (the corrupt copy only adds a file; nothing is removed) |
| C3 | fired | judged — the directory stores personal data about third parties (names, roles, a free note) in a new file; answered in `01-requirements.md` §6.3; the security-reviewer reads the store |
| C6 | fired | judged — `people.json` read as input at start; the picker's and the form's fields; pulled notes' mentions |
| C8 | fired | judged — new screens draw directory and board text (names, roles, notes, the quotes, titles); each a plain Text piece (S1) |
| D1 | fired | judged — every item alters what the operator sees or touches; `ux-reviewer` joins P2, the PDR and the DDR |
| D2 | not fired | judged — the round's prototype is the real `TaskboardApp` with subclasses and new screens, the target's own technology |
| E1 | fired | 5 stories (US-2501..US-2505) and 5 planned increments |
| E2 | not fired | judged — no high risk declared at intake; no board file changes its format (a task's people are read from its notes) |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-20-batch-03's close |

## Where we are

P3 — ARQ, P1, P2 and the PDR closed under the standing authorization (`db3d562`): the four spawned reviewers approved with conditions, folded as LED .2 and the PDR's PC-1..PC-4. Increments are ported from the frozen draft block by block, each with its own RED, battery, targeted suites and independent review; increment 001 (the directory) is done, 002 is next.

## Objective

Port the round's chosen variants into the app — the directory (D1–D3, the handle form), the picker (2 A), the people view (1 A with C's quote and B's box), the person filter (3 A), the look (4 A) — with D4's title and D5's keys.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2501 | READY | increment 001 |
| US-2502 | READY | increment 003 |
| US-2503 | READY | increment 004 |
| US-2504 | READY | increment 005 |
| US-2505 | READY | increment 002 |
| P0 | done | triggers evaluated; refinement done |
| ARQ | approved with conditions | A-1, A-2 folded into `docs/ARCHITECTURE.md` |
| P1 | approved | LED .1, .2 |
| P2 | approved | all four lenses approve with conditions, folded (LED .2) |
| PDR | approved with conditions | PC-1..PC-4 |
| P3 | in progress | increment 001 done (code-reviewer OK; security APPROVE S-1) |

## Roadmap + increment plan

- 001 — the directory (HLR-2501, HLR-2502, HLR-2507): `taskboard/people.py` (new), `taskboard/models.py`, `taskboard/app.py`, `taskboard/boards.py` (`keep_aside`, architect A-3); `tests/test_people_directory.py` (new), `tests/people_round_fixture.py` (new), `tests/test_boards_concurrency.py` (the patched name). 4 source files.
- 002 — the look (HLR-2506): `taskboard/views.py`, `taskboard/modals.py`; `tests/test_people_look.py` (new). 2 source files.
- 003 — the picker (HLR-2503): `taskboard/modals.py`, `taskboard/app.py`; `tests/test_people_picker.py` (new). 2 source files.
- 004 — the people view (HLR-2504): `taskboard/views.py`, `taskboard/app.py`, `taskboard/keymap.py`, `taskboard/modals.py`; `tests/test_people_view.py` (new), `tests/test_modal_keys.py`, `tests/test_keymap.py`, `tests/test_readme.py`; `README.md` (docs). 4 source files.
- 005 — search by person (HLR-2505): `taskboard/views.py`, `taskboard/modals.py`, `taskboard/app.py`; `tests/test_people_search.py` (new), `tests/test_modal_keys.py`; `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` (docs). 3 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-21 | D-1 — one directory `people.json` beside the registry (`~/.taskboard/people.json` for `taskboard`), read never raising, written only on an add or an edit, atomically under `people.json.lock` as a read-modify-write (the registry's `_commit` pattern), an unparseable file copied aside before it is replaced; a person = handle, name, role, note | D1, D2; the commission's «written with batch-02's lock/atomic-write pattern» |
| 2026-10-21 | D-2 — a mention is stored `@handle` (the storage verdict `handle`, S3); the handle derived from the name, `2`, `3`, … when taken, never changed; the link form `@[Name](p:handle)` is read too; a task's people are read from its notes, no board field | D3 and «formato (storage): handle» |
| 2026-10-21 | D-3 — item 1 is A's two panes with, under EACH task, the first note line that mentions the person (C's context; the round's recommendation put it under the cursor's task only, the commission says «under each task») and, above the tasks, B's progress box: a block per open task (red late, amber today, grey the rest) and `N late · N today · N open` — B's rendered order, most urgent first; the objection's spoken order «X late X open X today» names the same three counts | the verdict «1 view: A · OBJECIÓN …»; the commission's reading |
| 2026-10-21 | D-4 — D4 applied as the page proposed: the new view is titled `PEOPLE · directory` on screen and `@` is listed as `People directory`; view `9` keeps `People`; the team roster stays apart (merging the two is a later round) | the verdict «D4: de acuerdo»; the page: «Propongo que la nueva se titule PEOPLE · directory en pantalla» |
| 2026-10-21 | D-5 — every new window button has a direct shown key: `PersonForm` `↵ / alt+s save`, `esc cancel`; `SearchPrompt` keeps `TextPrompt`'s `alt+s`/`esc` and adds `alt+p`; the picker's add confirms the role with `↵`, never `alt+s` (the task's Save); the modal law reads a modal's buttons and bindings along its package bases | D5; the commission's «`tests/test_modal_keys.py` law must cover new modals» |
| 2026-10-21 | D-6 — the people view's `n`, `e` and `/` (shown but inert in the round) are implemented: `PersonForm` adds and edits a person (name, role, note; the handle kept), `/` moves to the first name found; deleting a person is not offered | a shipped key that does nothing breaks the key bar's law; D2's note needs a place to be written |
| 2026-10-21 | D-7 — `enter` on the people pane goes to that person's tasks pane; `enter` on a task opens it on its board (the round opened the first task from either pane) | an unseen task never opens; one more `enter` |
| 2026-10-21 | D-8 — the people view reads every board once when it opens and shares the agenda's lane-building and jump (`board_lanes`, `open_on_board`, moved out of `AllBoardsAgenda`) | one way to read every board; the agenda's tests hold the move |
| 2026-10-21 | D-9 — `Board.people` holds the app's one live `Directory.people` dict (handle → Person), set in `_label_board`, never saved: every view draws the current name, a rename shows at once | the round's module-level `DIR` would leak across the suite's many apps; `Board.label` is the precedent |
| 2026-10-21 | D-10 — five increments, one lane: 001 directory → 002 look → 003 picker → 004 people view → 005 search; the code was drafted in this worktree before the review and is ported per increment after the PDR (the 2026-10-20-batch-03 D-13 pattern) | each ≤ 4 source files; the view and the filter's `alt+p` need the directory and the look |
| 2026-10-21 | D-11 — logged, NOT fixed: the presentation's split view draws `!!…!!` and `++…++` raw (pre-existing; the round's finding) → `BACKLOG.md` | the commission |
| 2026-10-21 | the rollover by script with `devflow-init.py`'s own seed helpers (`evidence/rollover.py`, the 2026-10-20-batch-03 pattern), `ROOT` checked to be this worktree before it ran; `owner` this worktree | the commission's worktree; `V40` |

## Risks / watch-items

- two windows add a person at once · low · the lock and the re-read (TC-2501)
- `tab` in the editor rebound by the picker · medium · it calls `focus_next` when closed; `tests/test_edit_window.py`'s walk
- a teammate's handle naming someone else here · low · D4's accepted consequence
- the existing kanban/presentation pins shift with a mention token · low · the fixtures of the existing suites hold no mentions (B1 census in each packet)
- the people view's cost at open (every board read) · low · as `A`

## Conventions honored

- synthetic data only (the round's boards and eight people, copied to `tests/people_round_fixture.py`); English artifacts, code and UI; the operator's name nowhere (`username_subject`)
- no push, no merge, no reset of shared state, no force; commits end with the commission's co-author line; own paths staged by name
- no test touches the real home (the conftest seam)
- the full suite in three sequential chunks, `NO_COLOR` unset

## Out-of-scope carries

- the presentation's split view drawing `!!…!!`/`++…++` raw (D-11; `BACKLOG.md`)
- deleting a person; mentions in the focus snippet, the swimlanes, the HTML report; merging the team roster (D4) (`BACKLOG.md` at the close)

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1:** exit 1 on `eac7d42` before the rollover — 126 `V59` BLOCKs over the commits after the closed batch's `base_ref` (the round and main's backlog commits), cleared by the rollover's re-stamp; the NOTICEs historical over closed batches (`V9`, `V13`, `V22`, `V23`, `V42`), `V30` (the bundle run).

**P0 (step 3, after the rollover):** 0 block · 107 notice — the step-3 placeholder NOTICEs over the unfilled seeds (`V27`, `V31`–`V38`, `V41`, `V43`–`V51`, `V54`), `V53`, `V30`, the historical NOTICEs above (`V9`, `V13`, `V22`, `V23`, `V42`).

**ARQ … PDR gates:** 0 block · 105 notice — the seeds' placeholder NOTICEs (`V31`–`V38`, `V41`, `V43`–`V51`, `V54`) until their artifacts are written; `V53` while the contract names test nodes not yet written (P3 writes them); `V62` between a `--station` move and this plan's rewrite (the four moves were run back to back, the plan rewritten at P3); `V30`; the historical NOTICEs (`V9`, `V13`, `V22`, `V23`, `V42`).

**P3:** declared per increment below as it lands.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `evidence/premises.py` on `base_ref` | 2026-10-21 | P-1..P-8 TRUE — `evidence/premises.txt` |
| the drafted increments (this worktree, before the PDR), targeted | 2026-10-21 | the five new suites and the touched laws green — draft only, not evidence |
| the draft's full suite, three chunks (scratch) | 2026-10-21 | 1398 + 918 + 797 passed — draft only, not evidence |
| `evidence/suite-001.txt` (increment 001, targeted) | 2026-10-21 | 391 passed |
| `evidence/mutation-001.txt` | 2026-10-21 | 17/17 KILLED |

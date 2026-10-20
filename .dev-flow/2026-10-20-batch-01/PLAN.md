# PLAN — taskboard — Batch 2026-10-20-batch-01

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
| Batch | 2026-10-20-batch-01 |
| Objective | Multi-board (variant C, home cards, of the multi-board round): several boards in one taskboard -- a boards registry with one folder per board and today's board as `Main` in place, the active board's chip in the head row, the Home cards behind `B` (shown at launch when more than one board is open), create / rename+recolour / archive boards, `--board PATH` registering its board, and moving a project to another board from the projects modal (backups, a move log, crossing links dropped and logged, team mode refused) |
| Last updated | P3 · 2026-10-20 |
| Standing authorization | standing authorization — the orchestrator's commission of 2026-10-20 (the runtime cannot prompt), relaying the operator's commission «necesito tener configurados varios boards… hago boards para varios proyectos de distintas disciplinas además de mis tareas personales. Entonces todo está mezclado y no necesariamente debería serlo.» and verdict on `prototypes/multi_board/multi-board-prototype.html` «VARIANTE ELEGIDA: C · Sin objeciones: acepto P1–P4 como están.» Quoted from the commission: «Implement a /dev-flow batch … Batch id `2026-10-20-batch-01`, artifact language English», «Cut local branch `feat/multi-board` from `main` (fff21cc)», «cherry-pick it first so the round folder ships», «Do NOT push», «Max 4 SOURCE files per increment (tests uncapped)», «Finish the whole batch in one go including 04-validation and 05-close». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents carrying their `agents/<role>.md`); commits on the local branch `feat/multi-board` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); `.gitattributes`, the two `inc001-brief.md` files and the untracked old `.dev-flow/*` files are not touched or staged; tests never touch the real `~/.taskboard`. |
| First gate | step 1, on `feat/multi-board` at `783397e` before the rollover: exit 1 — 32 block · 45 notice · 62 not applicable; every BLOCK the outgoing closed batch's record against the tree: `V59` ×32 (2026-10-19-batch-01's `base_ref` `bdf6e9d` predates the round's cherry-pick `783397e`, whose 32 files no packet of that batch names) — repaired by the rollover, which re-stamps `base_ref` at `783397e`; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 65 notice · 47 not applicable (`evidence/gate-step1.txt`, `evidence/gate-step3.txt`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `fff21cc6e81fe9ab22e43e0dc02aa054ccf023d8` = local `main`; `git switch -c feat/multi-board main`; HEAD equals the origin tip, so no rebase is owed. The round's commit `74bbe4d` (local branch `proto/multi-board`) cherry-picked as `783397e` (prototype files only — the design oracle, as the commission asks), and `base_ref` stamped `783397ed64cbb4adcf129c60d1f7381a4dbe5325` so the round is not counted as this batch's work. RC-1 (b): not already shipped — on `origin/main` `git grep -n "boards.json\|switch_board\|registry" taskboard/` → nothing; `taskboard --board` opens one file (`taskboard/__main__.py`). RC-2: `git ls-remote --exit-code --heads origin` → exit 0. Premises: `01-requirements.md` §2.7 (P-1..P-10, all TRUE, `evidence/premises.txt`, `evidence/suite-keyb.txt`). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | fired | judged — `docs/ARCHITECTURE.md` §2 · a new file `taskboard/boards.py` joins the `models` layer and a new boundary (the registry, the move between boards) is drawn; the map amended |
| A2 | fired | judged — the planned source files span five layers: `models` (`boards.py`, `models.py`), `views`, `app` (`app.py`, `__main__.py`, `taskboard.tcss`), `modals`, `keymap` |
| A3 | fired | judged — `docs/ARCHITECTURE.md` §4 · new interfaces (`boards.json`, `Registry`, `peek_board`, `move_plan`/`move_project`, `Board.label`, `header(..., chip=)`, the home's renders, `TaskboardApp(registry=)`, `switch_board`, `open_app`); `KEYMAP` gains `B`; `ProjectPicker` gains `m` |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl --include=*.py` over `tests/`: `header(` → `test_app.py`, `test_present_polish.py`; `key_bar_plain\|render_key_bar\|fit_bar\|bar_keys` → `test_archive.py`, `test_colour_budget_app.py`, `test_help_clip.py`, `test_help_keys.py`, `test_keymap.py`, `test_legend.py`, `test_link_picker.py`, `test_markup_census.py`, `test_milestones.py`, `test_report.py`; `KEYMAP` → `test_app.py`, `test_archive.py`, `test_dependencies.py`, `test_help_keys.py`, `test_kanban_priority.py`, `test_keymap.py`, `test_legend.py`, `test_links.py`, `test_link_picker.py`, `test_momentum.py`, `test_readme.py`, `test_report.py`; `check_action` → `test_present_views_app.py`; `ProjectPicker` → `test_markup_sites.py`; `__main__` → `test_readme.py`; `on_mount` → `test_emoji_picker.py`, `test_milestone_offer.py`, `test_setup_help.py`; `palette_commands` → `test_keymap.py`, `test_report.py`; `global_keys` → `test_help_keys.py`; the measured blast radius of `B` in the seat: `evidence/suite-keyb.txt` |
| B2 | fired | judged — the move relocates files at run time: a project's tasks' image folders (`images/<id>/`, read by `Board.image_dir` and by `task.images`' absolute references, P-3) and history lines (`history.jsonl`, read by `history.read` for the Flow view); the readers are named in HLR-2206 (references rewritten, lines moved); no repository file moves |
| B3 | fired | `ls tests/goldens` → no such directory; the byte oracles are the round's captures `prototypes/multi_board/out/C-*-open.svg`, `C-160-switched.svg`, `move-160-3-confirm.svg` (read by the new tests) and the shipped frames that render a head row — every view's first row is unchanged while `Board.label` is None (TC-2203's byte-identity arm), so no shipped capture drifts; the key bar (in the main screen's frame captures) changes with `B` — named in increment 002's census |
| B4 | fired | judged — `boards.json` (read by `open_app`, the home, the move), the created `boards/<slug>/board.json` (read by `Board.load`), the move's `.pre-move-<date>` copies and `move-<date>.json` (read by the operator), the moved history lines (read by the Flow view) |
| C1, C5, C6 | fired | `devflow-scan-spec.py` over `01-requirements.md` (P1): `flags: session, migration, form, escape`, `security_required: true`, exit 1 (`evidence/scan-p1.txt`) — answered in `01-requirements.md` §6.3; the security-reviewer pass of P2 reads them |
| C2, C3, C4, C7 | not fired | the same scan: no flag in those families |
| C8 | fired | judged — new markup and text sites over file-derived names: the chip (`escape` inside markup), the home's cards, the board form, the move's picker and confirmation (plain `Text` pieces) |
| D1 | fired | judged — a new screen (the home), a chip in every head row, a new key (`B`) in every key bar, new modals; `ux-reviewer` joins P2 and the PDR |
| D2 | not fired | judged — the round ran the real Textual app headless (`app_capture.py`, `export_screenshot`), the target technology |
| E1 | fired | 4 stories (US-2201..US-2204) and 4 planned increments |
| E2 | not fired | judged — no high risk declared at intake; the riskiest write (the move) is guarded by byte copies and refusals |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-19-batch-01's close (`fff21cc`) |

## Where we are

P3 — ARQ approved; P1/P2 approved after two iterate-to-refine rounds (LED .2, .3; three review iterations by four spawned reviewers, `02-review.md`); the PDR sealed approved with conditions PC-1..PC-3 (PC-4, PC-5 discharged at the seal). Increment 001 (the registry and switching) is next.

## Objective

Ship variant C of the multi-board round with P1–P4 as accepted: one folder per board and a registry, today's board as `Main` untouched, the chip, the home behind `B`, board create/edit/archive, `--board` registering, and moving a project between boards.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2201 | READY | increment 001 (registry, switching, `--board`) |
| US-2202 | READY | increment 002 (chip, home, `B`) |
| US-2203 | READY | increment 003 (forms) |
| US-2204 | READY | increment 004 (move, README, backlog) |
| P0 | done | triggers evaluated; refinement done |
| ARQ | approved | `docs/ARCHITECTURE.md` amended (iterations 1–3) |
| P1 | approved after two iterate-to-refine | LED .1, .2, .3 |
| P2 | approved | iteration 3: architect, qa, ux, security approve |
| PDR | approved with conditions | `design/PDR-2026-10-20-batch-01.md`: PC-1..PC-3 open, PC-4/PC-5 discharged |
| P3 | in progress | increment 001 next |

## Roadmap + increment plan

- 001 — the registry and switching (HLR-2201, HLR-2202): `taskboard/boards.py` (new), `taskboard/app.py`, `taskboard/__main__.py`; `tests/test_boards.py` (TC-2201, TC-2202, AT-2201), `tests/multi_board_fixture.py` (the round's boards), `tests/conftest.py` (the home seam). 3 source files.
- 002 — the chip, the home and `B` (HLR-2203, HLR-2204; AT-2202): `taskboard/models.py` (`Board.label`), `taskboard/views.py`, `taskboard/app.py`, `taskboard/keymap.py`; `tests/test_boards_home.py`, the law-driven key-bar updates; `README.md` (the Keys table's `B` row, docs). 4 source files ⚠ (the chip's attribute, its renders, the screen and the key cannot ship apart: a key with no screen, or a screen with no key, breaks the seat's law).
- 003 — the board forms (HLR-2205): `taskboard/boards.py`, `taskboard/modals.py`, `taskboard/app.py`, `taskboard/taskboard.tcss`; `tests/test_boards_forms.py`. 4 source files ⚠ (the registry's writers, the form, its keys on the home and the form's backdrop).
- 004 — the move (HLR-2206): `taskboard/boards.py`, `taskboard/modals.py`, `taskboard/app.py`, `taskboard/taskboard.tcss`; `tests/test_boards_move.py`; `README.md`, `.dev-flow/BACKLOG.md` (docs). 4 source files ⚠ (the move function, its two modals and `m`, the app's after-move hook, the backdrop).

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-20 | D1 — variant C (home cards) is the switcher; variants A and B are not shipped | the operator's verdict «VARIANTE ELEGIDA: C» (the commission) |
| 2026-10-20 | D2 — P1: one folder per board (`~/.taskboard/boards/<slug>/board.json`); the existing `~/.taskboard/board.json` is `Main` in place, nothing moved or migrated; a registry `~/.taskboard/boards.json` (id, name, colour, path, last opened, archived; the last board) validated on load like the board loader (never raising, bad entries skipped or defaulted, a missing file = `Main` alone, an unreadable one copied to `.corrupt`); every registry write atomic; **nothing is written for a one-board user without a registry file** | P1 accepted (the commission); P-1: history, images and reports live beside the board file |
| 2026-10-20 | D3 — P2: the chip opens the head row of every MAIN-screen view; **hidden with a single active board** (today's users see no chip); **not in the presentation** (`R`), whose frames and exports are for an audience and whose byte oracles stay untouched; the name cut to 24 cells | P2 accepted; the commission recommends hiding it with one board; the presentation exclusion is the orchestrator's (recorded, reversible) |
| 2026-10-20 | D4 — P3: `m` in `P` → target picker → confirmation listing the crossing links → byte copies `board.json.pre-move-<date>` (`-2`… never clobbering), `move-<date>.json` (a list, appended) beside each, history lines and image folders moved; crossing links dropped and logged; the source's undo stack cleared; a move is not undoable and the confirmation and README say so. Refusals, nothing written: a project shared in team mode (or team mode with an unreadable configuration), an id the target holds, an image folder the target holds, a phase the target lacks, an unreadable target, no other active board | P3 and the open question's recommended answer (the commission); the team guard the commission asks for; the id, phase and unreadable-target refusals and the image-reference rewrite are the orchestrator's (P-3: absolute references would break) |
| 2026-10-20 | D5 — P4: `n`/`e`/`x` on the home; `x` asks first (`ConfirmModal`) and refuses the open board; archiving leaves the folder untouched; `taskboard --board PATH` registers the path (and un-archives an archived entry holding it) | P4 accepted (the commission); the confirmation is the orchestrator's (archive has no un-archive key) |
| 2026-10-20 | D6 — `B` (`boards`) is a universal, primary key of the seat, after `q`: the key bar of every view, the `?` help and the palette list it; this changes the key bar for one-board users too — the one visible change they get | the seat's law (a key that works is shown) and `B` must work with one board (it is how the second board is created); the round's capture `C-160-switched` shows `B Boards` after `q Quit` |
| 2026-10-20 | D7 — the round's option D (an "all boards" agenda) is not in the core: `BACKLOG.md`, OPTIONAL | the open question's recommended answer (the commission) |
| 2026-10-20 | D8 — switching boards is in place: a new `Board` object, the per-board start rerun (link migration, renumbering notice, sweep, recovery notices, team mode, milestone offer), the old board's team timer stopped; the view and its layouts survive; the selection, focus, search, undo stack, gantt group memory, setup staging and team state do not | the round's `switch_board` plus what it missed (P-6); the undo stack is a board's |
| 2026-10-20 | D9 — a new board's colour defaults to the first project colour no active board uses (else `violet`); `tab`/`shift+tab` cycle all eight | the chips stay apart; the round defaulted to `sky` (index 2) |
| 2026-10-20 | D10 — a created board starts empty with the default phases and settings marking the link and milestone migrations done and the renumbering notice seen | a new board should not greet the operator with notices about an app history it never had |
| 2026-10-20 | D11 — the home is pushed at launch BEFORE the opened board's own modals (team identity, milestone offer), so those modals sit above it and answer for the board behind it | a modal left under the home would answer for whichever board is open when it surfaces |
| 2026-10-20 | D12 — `TaskboardApp(registry=None)` builds an in-memory registry of its board alone, its file beside that board; a suite-wide seam in `tests/conftest.py` points `Path.home()` at a temporary folder for every test | tests construct the app with a temporary board and must never reach `~/.taskboard` (the commission) |
| 2026-10-20 | D13 — the home reads each board once when it opens (`peek_board`: `Board.load` for an existing file, an empty unsaved board for a missing one), never per keypress and never writing | the round reloaded every board on every paint; `Board.load` seeds and saves at a missing path (P-2) |
| 2026-10-20 | D14 — the home's `esc` returns to the open board; its `q` quits; while it is shown no other main-screen key acts | the round's `check_action` rule |
| 2026-10-20 | D15 — four increments: 001 registry + switching → 002 chip + home + `B` → 003 forms → 004 move + README + backlog | the commission's suggested cut, kept within 4 source files each |
| 2026-10-20 | the round's commit cherry-picked as `783397e` and `base_ref` stamped there; the prototype folder ships with the feature (the design oracle) | the commission; `V59` |
| 2026-10-20 | the rollover by script with `devflow-init.py`'s own seed helpers (the 2026-10-18/19 pattern, `evidence/rollover.py`); the evidence home's `-text` mark a per-directory `evidence/.gitattributes` | the root `.gitattributes` was dirty before the batch and the commission says not to touch it |
| 2026-10-20 | the home's guard blocks the key seat's actions only (`SEAT_ACTIONS`), not Textual's own (`focus_next`) — found running AT-2205's key path in a draft; recorded in LLR-2204.1 (LED .3) | the broader guard left `tab` dead in a confirmation over the home |
| 2026-10-20 | code drafted in a scratch worktree (`wt-dev`) while the reviewers read the contract; each increment ports its slice into the branch, after the PDR, with its own RED on `base_ref` and its battery | the reviewers read the shipped code, which the draft must not move under them |
| 2026-10-20 | the reviewer lenses of ARQ, P2 and the PDR run as one spawned agent per role over the drafted artifacts together (architect · qa-reviewer · ux-reviewer · security-reviewer), each returning per-station findings; the gates are then recorded in station order | the four roles are independent of each other and of the author; the 2026-10-19-batch-01 pattern — declared here |

## Risks / watch-items

- the law-driven key-bar updates (`B Boards` in every bar) could hide a weakened assertion · medium · each named old → new in packet 002's census, the new values derived from the seat's strings, never from the code under test
- the home's frame equality with the round's captures depends on Textual's grid and border rendering staying as the round ran it · low · the same Textual pin; AT-2204 fails loudly if it drifts
- a move between boards writes two files and folders · medium · byte copies first, refusals on doubt, target saved before source
- `--board` on a copy registers it · certain · README; `x` archives it

## Conventions honored

- synthetic boards only (`tmp_path`; the round's boards); English artifacts, code and UI; the operator's name nowhere
- no push, no merge, no reset, no force; commits end with the commission's co-author line; own paths staged by name
- no test touches the real `~/.taskboard` (the conftest seam)

## Out-of-scope carries

- variants A and B; option D (`BACKLOG.md`, OPTIONAL)
- un-archiving from the home (`--board PATH` does it)
- locking a board another app instance holds

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1 (before the rollover):** exit 1 — the BLOCKs are the outgoing closed batch's (`V59` ×32, see the header's `First gate`), repaired by the rollover; NOTICEs historical, over closed batches, and the bundle run (`V30`).

**P0 (step 3, after the rollover):** 0 block · 65 notice — the step-3 placeholder NOTICEs (`V27`, `V31`–`V34`, `V36`–`V38`, `V41`, `V43`–`V51`, `V54`) over the unfilled seeds; `V30`; the historical NOTICEs (`V9`, `V13`, `V22`, `V23`, `V42`, `V53`).

**ARQ … PDR gates:** 0 block; `V62` between each `--station` move and this plan's rewrite — cleared by the rewrite; `V53` while the contract names test nodes not yet written (P3 writes them); the step-3 placeholder NOTICEs leaving as each artifact filled.

**Found before the batch:** tracked and modified — `.gitattributes`, `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md` (line endings only); untracked — `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py`. Not touched.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider -rs --color=no` on `base_ref` (a worktree at `783397e`, `NO_COLOR` unset) | 2026-10-20 | 2819 passed, exit 0 — `evidence/suite-base.txt` |
| `783397e` + the conftest home seam only (`evidence/seam.diff`) — architect A-26 | 2026-10-20 | 2819 passed, exit 0 — `evidence/suite-seam.txt` |
| the same with `B` added to the seat (a scratch worktree at `783397e` + one line, `evidence/suite-keyb.diff`) — P-10's blast radius | 2026-10-20 | 3 failed, 2816 passed: `test_TC_203_the_key_bar_wears_bright_keys_and_muted_words` (its `KEYBAR_BASE` literals — law-driven), `test_every_shown_key_has_a_real_action_on_the_app` (no `action_boards` yet — increment 002 adds it), `test_the_readme_keybinding_table_matches_the_seat` (README lacks `B` — increment 002 adds it) — `evidence/suite-keyb.txt` |

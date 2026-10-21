# PLAN — taskboard — Batch 2026-10-20-batch-03

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
| Batch | 2026-10-20-batch-03 |
| Objective | The backlog round after the several-boards batches, as the operator's verdict on prototypes/backlog_round chose: an all-boards agenda on `A` (a lane per board and the chosen day's list, variant C); the board's chip on the presentation's hint row; `?` inside `R` opens its keys; the view-3 export without the cursor, cut to its content; `K`/`J` reorder beside shift+arrows; a direct, shown key for every modal button (`y`/`n` in confirmations, `alt+<letter>` beside text inputs); the board's chip in the start-up modals' titles; one notice when the board is open in another window; `--open PATH` opens a board without registering it |
| Last updated | P3 · 2026-10-20 |
| Standing authorization | standing authorization — the orchestrator's commission of 2026-10-20 (the runtime cannot prompt), relaying the operator's words «Haz lo del backlog por favor.» and the operator's verdict on the backlog round, verbatim: «1 agenda: C · 2 chip: B · 3 help: A · 4 export: limpia · 5 reorder: A · 6 confirm: B · OBJECIÓN: «Esa opción debería ser el estandar para todas las aplicaciones TUI que tenemos. Para tener un acceso directo a los botones. (y cuando hay bloques de entrada de texto usar una combinación específica)» · 7 startup: A · 8 twice: A · 9 register: A · notes: (none)». Quoted from the commission: «Gates close under this authorization. Do NOT push or merge; stop at batch close and report», «WORKTREE: … -b feat/backlog-round fix/backlog-boards, then git cherry-pick 36bba10», «the chosen variant of each item is the spec; port the prototype's code into the real app», «EVERY modal in taskboard gets a direct key per button, visible on screen … In modals with text inputs, plain letters type, so buttons use alt+<letter> (keep ctrl+s where a form already saves with it; keep esc cancel)», «Max 4 SOURCE files per increment (tests uncapped)», «spawn independent agents (code-reviewer, qa-reviewer, ux-reviewer, security-reviewer for the presence marker / CLI) … no self-review», «Real-app captures of each shipped item at 118x30 and 80x24», «full suite in 3 SEQUENTIAL chunks». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents carrying their `agents/<role>.md`); commits on the local branch `feat/backlog-round` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); the main checkout's dirty and untracked files and the other worktrees are not touched; tests never touch the real home. |
| First gate | step 1, on `2eade16` (the base before the cherry-pick, a scratch detached worktree): exit 0 — 0 block · 51 notice · 63 not applicable; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102` (`evidence/gate-step1.txt`). The same run on `1fd667b` (after the commission's cherry-pick, before the rollover) printed 136 BLOCK, every one `V59` naming a `prototypes/backlog_round/` file against the closed batch's `base_ref` `b1b71e4` (`evidence/gate-step1-after-cherry-pick.txt`); the rollover re-stamps `base_ref` to `1fd667b`, the cherry-pick then predates the batch. Step 3 (after the rollover): exit 0 — 0 block · 72 notice · 47 not applicable (`evidence/gate-step3.txt`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `b1b71e4310ea7944edbbb6f16f350352e0a9491b`, an ancestor of the worktree's `HEAD` `1fd667b` (`fix/backlog-boards` at `2eade16`, batch 2026-10-20-batch-02's unpushed close, plus the commission's cherry-pick of `36bba10`); the commission names that base, so no rebase onto `origin/main`; `base_ref` stamped `1fd667b27b0980996d7a8d7ce0a8d7f0e8156e3d`. RC-1 (b): not already shipped — on `HEAD` `A` is bound nowhere, `?` does nothing in `R`, `ConfirmModal` answers no `y`, `--open` is not an option (P-1, P-3, P-6, P-9). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest commit on `origin/main` 2026-10-20 17:57 −0600. Premises: `01-requirements.md` §2.7 (P-1..P-11, all TRUE, `evidence/premises.txt`). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` §2 · no new module and no boundary moved: the agenda screen lives in `app.py` beside the home, its render in `views.py`, the presence markers in `boards.py` (the `models` layer), the presentation's key seat in `keymap.py` |
| A2 | fired | judged — the planned source files span `app` (`app.py`, `__main__.py`), `views`, `modals`, `keymap` and `models` (`boards.py`) |
| A3 | fired | judged — `docs/ARCHITECTURE.md` §4 · new interfaces consumed across modules: `keymap.PRESENT_KEYS`/`present_bindings` (by `app` and `modals`), `boards.announce`/`renew`/`withdraw`/`open_elsewhere` (by `app`), `views.board_chip_text`/`present_all_export`/`render_all_agenda` (by `app`, `modals`), `modals.key_line`; `TeamIdentityPicker` and `open_app` gain a parameter |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl --include=*.py` over `tests/`: `ConfirmModal` → `test_app.py`, `test_archive.py`, `test_boards_home.py`, `test_links.py`, `test_markup_census.py`, `test_markup_sites.py`; `PresentScreen\|present-hint\|_hint` → `test_boards_home.py`, `test_gantt_polish.py`, `test_link_picker.py`, `test_markup_census.py`, `test_markup_sites.py`, `test_present.py`, `test_present_all.py`, `test_present_hide.py`, `test_present_narrow.py`, `test_present_polish.py`, `test_present_views_app.py`, `test_report.py`; `action_export\|render_present_all` → `test_markup_census.py`, `test_present_all.py`; `MilestoneOffer` → `test_help_keys.py`, `test_milestones.py`, `test_milestone_offer.py`, `test_milestone_offer_seam.py`, `test_present.py`, `test_present_hide.py`, `test_present_rulers.py`, `test_present_views_app.py`; `TeamIdentityPicker` → `test_boards_home.py`, `test_markup_sites.py`, `test_milestone_offer.py`, `test_team_sync.py`; `open_app` → `test_boards.py`, `test_boards_concurrency.py`, `test_boards_forms.py`, `test_boards_home.py`, `test_boards_move.py`; the five form modals → `test_app.py`, `test_details_grid.py`, `test_edit_window.py`, `test_emoji_picker.py`, `test_link_picker.py`, `test_markup_census.py`, `test_markup_sites.py`, `test_milestones.py`, `test_present_hide.py`, `test_setup_help.py`, `test_template_new.py`, `test_template_save_app.py`; `MoveConfirm` (its `enter` → `y`, architect A-18, qa QA-19) → `test_boards_move.py`, `test_boards_concurrency.py`; `KEYMAP` → `test_app.py`, `test_archive.py`, `test_boards_home.py`, `test_dependencies.py`, `test_help_keys.py`, `test_kanban_priority.py`, `test_keymap.py`, `test_legend.py`, `test_links.py`, `test_link_picker.py`, `test_momentum.py`, `test_readme.py`, `test_report.py` |
| B2 | not fired | judged — no file changes its location |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | judged — `~/.taskboard/open/<hash>-<token>.json` (read by the other window's `open_elsewhere`); `reports/present-*-all.svg|png` (read by the audience, now without the cursor) |
| C1, C2, C3, C4, C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1): `flags: token, hash, migration, form, escape` (`evidence/scan-p1.txt`); judged with it — no auth, secret, external integration, sensitive data or network surface (the token and hash name presence markers, answered in §6.3) |
| C5 | fired | judged — a destructive file operation: another window's stale presence marker is removed (`unlink`); answered in `01-requirements.md` §6.3; the security-reviewer reads it |
| C6 | fired | the P1 scan's `token`/`hash`/`escape` flags (answered in §6.3) and, judged, the marker files and `--open PATH` read as input |
| C8 | fired | judged — new screens draw board-file text (the agenda's titles, projects and board names; the chips in the hint row and the start-up titles); each a plain Text piece (S1) |
| D1 | fired | judged — every item alters what the operator sees or touches; `ux-reviewer` joins P2, the PDR and the DDR |
| D2 | not fired | judged — the round's prototype is the real `TaskboardApp` with subclasses, the target's own technology |
| E1 | fired | 7 stories (US-2401..US-2407) and 4 planned increments |
| E2 | not fired | judged — no high risk declared at intake; nothing changes a board file's format |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-20-batch-02's close (`2eade16`) |

## Where we are

P3 — ARQ, P1 (one iterate-to-refine: LED .2, LED .3), P2 and the PDR (approved with conditions PC-1..PC-5) closed under the standing authorization; increment 001 is next.

## Objective

Port the round's nine chosen variants into the app, with item 6's objection read as a standard for every modal: a direct, visible key per button.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2401 | READY | increment 004 |
| US-2402 | READY | increment 002 |
| US-2403 | READY | increment 002 |
| US-2404 | READY | increment 001 |
| US-2405 | READY | increment 003 |
| US-2406 | READY | increment 003 |
| US-2407 | READY | increment 003 |
| P0 | done | triggers evaluated; refinement done |
| ARQ | approved | `docs/ARCHITECTURE.md` amended |
| P1 | approved after one iterate-to-refine | LED .1, .2, .3 |
| P2 | approved | iteration 2: all four lenses approve |
| PDR | approved with conditions | PC-1..PC-5 |
| P3 | in progress | increment 001 next |

## Roadmap + increment plan

- 001 — item 6, the modal keys (HLR-2406, HLR-2407): `taskboard/modals.py`, `taskboard/taskboard.tcss`; `tests/test_modal_keys.py` (new). 2 source files.
- 002 — items 2, 3, 4, 5, the presentation (HLR-2402..HLR-2405): `taskboard/app.py`, `taskboard/views.py`, `taskboard/modals.py` (`PresentKeys`), `taskboard/keymap.py` (`PRESENT_KEYS`); `tests/test_present_backlog_round.py` (new), `tests/backlog_round_fixture.py` (new). 4 source files.
- 003 — items 7, 8, 9, the boards (HLR-2408..HLR-2410): `taskboard/boards.py`, `taskboard/app.py`, `taskboard/__main__.py`, `taskboard/modals.py`; `tests/test_boards_backlog_round.py` (new). 4 source files.
- 004 — item 1, the agenda (HLR-2401): `taskboard/app.py`, `taskboard/views.py`, `taskboard/keymap.py`; `tests/test_all_agenda.py` (new); `README.md`, `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` (docs). 3 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-20 | D-1 — item 1 is variant C (`AgendaRuler`), not the recommended A: a lane per board, the chosen day's list below; `A` joins `KEYMAP` off the bar (listed by `?` and the palette); opens on `TODAY`; the list ordered by due date then lane | the verdict «1 agenda: C»; the round: «`A` entra en `KEYMAP` (sin barra, como `R`)» |
| 2026-10-20 | D-2 — the chip on the hint row only (B); never the frame or the export | the verdict «2 chip: B» |
| 2026-10-20 | D-3 — `?` opens a keys window (A), and the presentation's bindings move into one seat `keymap.PRESENT_KEYS` the window is generated from | the verdict «3 help: A»; the round: «Necesita un asiento de teclas para la presentación … la ventana se puede generar de ese asiento» |
| 2026-10-20 | D-4 — the view-3 export: no cursor, folds kept, cut after its last row of content (never a content row) | the verdict «4 export: limpia»; the round: «quitar las filas en blanco del final, nunca filas con contenido» |
| 2026-10-20 | D-5 — `K`/`J` beside `shift+↑/↓`, named in the hint | the verdict «5 reorder: A» |
| 2026-10-20 | D-6 — item 6's objection is a standard for EVERY modal in taskboard: a direct key per button, visible on screen. `ConfirmModal`: `y` confirm / `n` (and `esc`) cancel and the key line of variant B. In modals with text fields plain letters type, so their buttons take `alt+<letter>`: `alt+s` save, `alt+i` paste image, `alt+t`/`alt+d` the start/due calendars; `esc` stays cancel; no modal saves with `ctrl+s` today, so none is kept or added. Every modal is inventoried (`02-review.md`'s inventory and the law TC-2407); none keeps `tab`, `enter` as its only keyboard path. Other TUI repositories are outside this batch (the objection's «todas las aplicaciones TUI que tenemos» is recorded for them in `BACKLOG.md`) | the orchestrator's reading of the objection, recorded as the commission asks |
| 2026-10-20 | D-7 — the round's finding "the confirmation's message is cut at «…its folder is not»" is FIXED here: the key line of D-6 sits under that message in the same box, so the confirmation work touches it; the message wraps (`width: 100%`) | the commission: «fix it if the confirm work touches that exact text, otherwise log it» |
| 2026-10-20 | D-8 — the board's chip opens the start-up modals' titles (A), with more than one board only, like every chip | the verdict «7 startup: A» |
| 2026-10-20 | D-9 — item 8 as one notice at opening (A); each window keeps a presence marker per open board under `~/.taskboard/open/` (one file per window, so two windows never erase each other's), created exclusively with a random token, renewed every 30 s, removed when left; a marker not renewed for 120 s is a dead window's (ignored, removed) — batch-02's lock design (stale-tolerant, owner-token, regular files only); no lock and no blocking; the folder is the home's, never a board's folder, so no board folder changes | the verdict «8 twice: A»; the commission: «an "open elsewhere" presence marker, removed on exit, stale-tolerant» |
| 2026-10-20 | D-10 — `--open PATH` beside `--board` (A): no registry write; the chip `<name> · not listed` on `pink` (the round's colour); no home at start; a notice; no move out of it or into it; a missing file refused (exit 2) because the loader would seed and save sample data there; `--open` and `--board` exclusive | the verdict «9 register: A»; the round: «el chip dice «board-copy · not listed», `B` muestra tus 3 tableros … no recibe proyectos movidos» |
| 2026-10-20 | D-11 — four increments, one lane: 001 modal keys → 002 presentation → 003 boards → 004 agenda | each ≤ 4 source files; the agenda last because its `enter` lands through the switch item 8 marks |
| 2026-10-20 | D-13 — the reviewer lenses of ARQ, P2 and the PDR run as one spawned agent per role (architect · qa-reviewer · ux-reviewer · security-reviewer) over the drafted artifacts together, two iterations; the gates recorded in station order after them; code drafted meanwhile in a scratch worktree (`<scratchpad>/b03/wt-dev`) and ported per increment | the 2026-10-20-batch-02 pattern |
| 2026-10-20 | D-12 — logged, NOT fixed: the black window real Windows Terminal draws after opening `Personal`/`Course` (`prototypes/backlog_round/out/png/black/`), and the blank screen behind the start-up modals — both as new `BACKLOG.md` items | the commission: «Also log, NOT fix … the orchestrator investigates that separately»; «the blank screen behind start-up modals» |
| 2026-10-20 | the rollover by script with `devflow-init.py`'s own seed helpers (`evidence/rollover.py`, the 2026-10-20-batch-02 pattern); `owner` the worktree. A first run of the script, before its `ROOT` was edited, wrote the rollover into the OTHER worktree `taskboard-wt/backlog-fix` (its `state.json`, a `decisions-log.json` and the seeded batch folder); the orchestrator restored that tree at once — `git checkout -- .dev-flow/state.json` and the two new paths removed, a copy kept in the scratch folder — and `git status` there is clean again | the commission's worktree; `V40`; the slip declared rather than hidden |

## Risks / watch-items

- a presence marker outlives a crash for up to 120 s · low · a false notice at most; the stale rule removes it
- the generated presentation bindings could drop a key the suite drives · medium · TC-2403's set equality and the existing presentation suites
- the `alt+<letter>` keys in a terminal that eats `alt` · low · Windows Terminal passes them (P-10 reads the parser); `esc` and `tab` stay
- the hint's `? keys` and `K J` change exact-text pins in the presentation suites · medium · law-driven updates named in increment 002's packet
- the presence folder under the home seam shows in tests that list the home · low · the folder is `~/.taskboard/open/`, never a board folder

## Conventions honored

- synthetic data only (the round's boards, copied to `tests/backlog_round_fixture.py`); English artifacts, code and UI; the operator's name nowhere (`username_subject`)
- no push, no merge, no reset of shared state, no force; commits end with the commission's co-author line; own paths staged by name
- no test touches the real home (the conftest seam)
- the full suite in three sequential chunks, `NO_COLOR` unset

## Out-of-scope carries

- the black window on `Personal`/`Course` in real Windows Terminal, and the blank screen behind the start-up modals (D-12; `BACKLOG.md`)
- the objection's standard for the other TUI repositories (D-6; `BACKLOG.md`)
- a lock on plain board saves (batch-02's open item, unchanged)

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1:** exit 0 on `2eade16` — 0 block · 51 notice; the NOTICEs are historical, over closed batches (`V9`, `V13`, `V22`, `V23`, `V26`, `V42`, `V53`), `V57` (2026-10-20-batch-02's record predates the tree by its close commit), `V40` (the outgoing `state.json`'s `owner` named the other worktree) and the bundle run (`V30`). On `1fd667b` before the rollover: 136 `V59` BLOCKs over the cherry-picked round against the closed batch's `base_ref`, cleared by the rollover's re-stamp (step 3: 0 block).

**P0 (step 3, after the rollover):** 0 block · 72 notice — the step-3 placeholder NOTICEs over the unfilled seeds; `V30`; the historical NOTICEs above.

**ARQ … PDR gates:** 0 block — `V26` (the live contract past its 54 000-character budget: ten HLRs with their thresholds, accepted as batch-02's was); `V53` while the contract names test nodes not yet written (P3 writes them); the increment-001 seed's placeholders (`V31`, `V32`, `V36`–`V38`, `V41`, `V43`, `V44`) until its packet is written; the seeded validation and close records (`V47`–`V51`, `V54`); the seeded DDR record; the historical NOTICEs; `V30`.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `evidence/premises.py` on `base_ref` | 2026-10-20 | P-1..P-11 TRUE — `evidence/premises.txt` |
| the drafted increment 001 (scratch worktree), targeted | 2026-10-20 | `tests/test_modal_keys.py` 27 passed; the move suites' 7 `enter`-confirms RED as expected (law-driven, increment 001) — scratch only, not evidence |

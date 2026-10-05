# PLAN — taskboard — Batch 2026-10-04-batch-01

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`, flow **rev99 pinned**
> (read-only snapshot of skills commit `1154c8a`).

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-04-batch-01 |
| Objective | Batch B1 of the `kg_mejoras` plan: waits-on links independent of Blocked (derived waiting, `◂N`/`▸N` card marks, the ready message), `L` links through the picker and the gantt link mode with loops refused, the details dependency section, the archive/delete guard, and the one-time link migration with backup, log, revert and run-once |
| Flow | **rev99, PINNED** — operator ruling at this batch's kickoff, 2026-10-04, verbatim: "Fijar a rev99". Read and validated ONLY from the read-only snapshot (`git archive` of skills commit `1154c8a`, "flow rev99 — the bundle regenerated over the bump") in the session scratchpad. Reason: rev100 is in progress in `~/.claude/skills` and its `SKILL.md` fails `V7`. `~/.claude` is never edited. Also in `state.json` `flow_pin`. |
| Standing authorization | the operator's commission, asked at this batch's kickoff and relayed by the coordinator (this runtime is a delegated sub-agent and cannot prompt), dated 2026-10-04: **Gates — "Autónomo + regla de HIGH de pruebas":** end-to-end autonomous; the agent self-approves each gate and records every un-asked decision (this plan's decision log, `state.json` `decisions_log`, the close record); a HIGH that is ONLY in tests/evidence (the reviewer confirms the product code correct) may be fixed without stopping, recorded with a RED-first proof and re-reviewed; a HIGH in app behaviour, security or data STOPS and returns to the operator. **Git — "Commit + push tras tu veredicto visual":** the COORDINATOR commits and pushes after verification and after the operator's visual verdict on provisional visual decisions; this agent does not commit, push, stash, reset or checkout anything. `merge: false (no PR; coordinator commits+pushes to main after the operator's visual verdict)`. **Migration safeguard — "Respaldo automático + deshacer":** the one-time migration of an existing board makes a backup copy of the board file BEFORE migrating, logs every change it makes, and can be reverted; it never runs twice (versioned in board settings); this agent never opens, reads or writes the operator's real board (tests and synthetic boards only). **Amendment, asked at the P3 gate on 2026-10-04 — "Sí, solo en el incremento en curso":** for the rest of this batch a HIGH in app behaviour found in the increment under construction (not yet approved) may be fixed without stopping, with a RED-first proof, recorded and re-reviewed; still stop and report a HIGH in code already approved or shipped, any security HIGH, or any HIGH touching the operator's data (the migration); the test-only rule stays. |

## Where we are

**P3 resumed (2026-10-04)** after the operator's ruling on F1 ("Corregir en el 003") and the authorization amendment. Earlier: stopped at increment 003 on F1.
Increments 001 and 002 are approved. Increment 003 (`L`, the picker, the details section, the
project-archive guard, README) is implemented; its code review found **F1 (HIGH, product)**: the
details view of a task that is itself done or archived paints its still-open predecessors as
`done` and counts `◂0 open of M` — the per-row state was taken from `open_predecessors()`, which
is empty for a closed waiter (LLR-503.1 wants each predecessor's own state). Proposed fix (one
function, `modals.py` `TaskDetails._links`): each row's state from the predecessor itself
(`is_open(p)` / archived / done), the count over those states, and no `waiting`/`ready` note on a
closed task; RED-first test. Test-only HIGHs T1, T2 and every other finding are folded; suite
2279 passed + the known clipboard environment flake. Nothing committed.

## Objective

A task can wait on other tasks without being Blocked: the board shows who waits (`◂N`) and who is
waited on (`▸N`), says once when work is ready, links with one key in the picker or on the gantt,
refuses loops and refuses to archive or delete work others still wait on; an existing board's old
`b` links are migrated once, with a backup, a log and a way back.

## RC-1 and flow currency

- RC-1 (a): `git fetch origin` → `origin/main` = `0447070ba154` = HEAD = merge-base; nothing to rebase. `base_ref` stamped from it (`state.json`).
- RC-2: `git fetch origin` answered; `origin/main`'s newest commit 2026-10-03 20:47 −0600 (`0447070`).
- RC-1 (b): no story already shipped on `origin/main` (`evidence/p0-probes.txt` §RC-1 (b): `LinkPicker`, `open_waiters`, link mode, link migration — 0 hits; the `↳ waits on` / `◂` hits are the shipped gantt gutter and the off-window glyphs).
- Rollover from `2026-10-02-batch-04` (P5 closed): its `decisions_log` MOVED to `.dev-flow/2026-10-02-batch-04/decisions-log.json` (28 entries); every single-slot field retired per `stations/shared-batch.md` §Batch rollover (triggers re-evaluated below, artifacts cleared, homes re-pointed, owner re-stamped, authorization re-recorded from this batch's commission, `base_ref` = HEAD, `created_at` re-stamped, `guided` false: not the project's first batch); `mode_history` carried and appended. Seeds from the snapshot's `devflow-init.py` run in a scratch tree (it refuses an initialised `.dev-flow/`), date 2026-10-04; `.gitattributes` gains this batch's `evidence/** -text`; the build caches were already in `.git/info/exclude`. The increment skeleton is held back until P3 so no packet precedes its increment.
- Flow: rev99 snapshot `1154c8a`; `V7` clean. Validator at kickoff (coordinator, `0447070`): **0 block · 26 notice**, exit 0 — re-run by this agent before the rollover: same.
- **Inherited NOTICEs declared** (all 26 predate this batch): `V9` ×8 legacy packets in the flat `.dev-flow/03-increments/` declare no SOURCE count, ×1 batch-02's `increment-002.md` 4-source warning; `V13` ×3 batch-01's `nav-order` address, batch-04's `field-rows` address reached by `REQUIREMENTS.md`, and the computed addresses; `V22` ×3 LLRs of batches 01/02 never used as an IFC owner and 5 legacy US ids not in the canon; `V23` an unparseable design-review citation in legacy `increment-006.md`; `V30` the bundle derives its floors from a subset (benign on this runtime, `SKILL.md`); `V42` ×7 deferral markers in batch-03's record; `V53` the closed-record census count; `V57` batch-04's close record predates this tree by 1 commit (the coordinator's commit). None is this batch's to fix; a closed record is not re-anchored.
- Not runnable here (`SKILL.md` step 4): `V15`, `V16`, `V17` — `not-run` (no canon tree, no checkout table, no hook settings on a bundle runtime).
- Mechanisms unavailable on this runtime, named once (`SKILL.md` step 5): no slash commands, no hooks, no prompt guard, no operator prompt (the standing authorization above closes the gates). Reviewer roles are **spawned as named sub-agents** of this runtime (`qa-reviewer`, `architect`, `security-reviewer`, `ux-reviewer`, `code-reviewer`, `tester`), each told to follow the snapshot's `agents/<role>.md` — independent reviewers, never inline self-review.

## Triggers (evaluated 2026-10-04, P0) {#triggers}

| id | Verdict | Probe / evidence |
|---|---|---|
| B1 | fired | `evidence/p0-probes.txt` §B1: `BlockerPicker` → test_dependencies, test_markup_sites; `toggle_blocked` → test_app, test_dependencies; `depends_on` → kg_board, test_app, test_dependencies, test_gantt, test_gantt_board, test_setup_help; `unblocks_count` → test_app, test_dependencies, test_kanban_readable; `⛓` → test_cells, test_dependencies, test_kanban_readable; `gantt_dep_mark` → test_gantt_board; `action_archive` → test_archive; `TaskDetails` → test_app, test_details_grid, test_details_markup, test_markup_sites; `card_cell` → 7 files; `help_usage` / `legend_entries` → 4 / 8 files → reverse census per increment |
| B2 | not fired | no file moves; new files only |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | the migration rewrites the board file that the next `Board.load` / app start consumes, and writes a backup the revert consumes → output-then-consume AT (C-12) |
| A | not fired (judged) | no `docs/ARCHITECTURE.md`; the dependency logic stays in `models.py` beside `unblocks_count` / `critical_chain` (no new module), as batches 01–04 ruled (D-502) |
| C | fired | new user-text surfaces (picker rows, details section, guard and ready toasts, link-mode status line) and a migration that writes user data (backup, log, board) → security-reviewer at P2 and close (also commissioned); the scan runs at P1 |
| D | fired | user-visible (marks, picker, details section, gantt link mode, toasts) → ux-reviewer at P2/P4; captures 118×30 and 80×24, base and close |
| E | fired | 5 stories, 4 planned increments |
| F | F2 fired | `BACKLOG.md` header base ref `56a1b10` ≠ HEAD `0447070` → reconciled at close; F1 not fired: `V7` clean on the pinned snapshot |

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | approved | rollover; US-501..505 READY; B2 → BACKLOG (D-501) |
| P1 requirements | approved | 5 HLR, 12 LLR, 6 AT, 16 TC; P-1..P-15 TRUE; D-501..D-514 |
| P2 review, iteration 1 | iterate-to-refine | qa FAIL (Q-1), architect FAIL (A-1), security + ux PASS-WITH-NOTES; 0 HIGH |
| P1 refine (iteration 2) | approved | every finding folded; D-515..D-525; re-cut |
| P2 review, iteration 2 | approved | four PASS-WITH-NOTES, 0 blocker, 0 HIGH; 16 minors folded (LED .11) |
| P3 increment 001 | done (revision 4) | 2 SOURCE; code review 4 rounds (R2-F1 test-only HIGH fixed under the standing rule); security PASS; 22/22 mutants; gate 2242 passed |
| P3 increment 002 | done (revision 2) | 3 SOURCE; F1 test-only HIGH folded; F2 product HIGH stopped → ruling → fixed; 21/21; gate 2265 |
| P3 increment 003 | done (revision 2) | 4 SOURCE; F1 product HIGH stopped → ruling → fixed; T1/T2 test-only HIGHs folded; 21/21; gate 2281 + clipboard flake |
| P3 increment 004 | done (revision 3) | 3 SOURCE; F1 product HIGH in the increment under construction fixed without stopping (amended authorization), RED-first, re-reviewed; F2 test oracle rebuilt; D-527, A-7; 25/25; gate 2294 + clipboard flake |
| P4 validation | approved | qa PASS-WITH-NOTES, ux PASS-WITH-NOTES, security PASS-WITH-NOTES; F4 + G-002 folded in increment 005; U-2, security F1 → operator / BACKLOG (D-529, D-530) |
| P3/P4 increment 005 (P4 fold) | done (revision 3) | 1 SOURCE; the folded-waiter note (A-8, D-528); 7/7; gate 2295 + clipboard flake |
| P5 close | closed, then re-opened (D-531) | security PASS-WITH-NOTES; BACKLOG reconciled; canon folded; PV-1..PV-7 accepted |
| P3 increment 006 (re-open) | done (revision 2) | 2 SOURCE; D-528 pin + D-534 page, D-529 lanes floor (D-533 consequence), D-530 read-only save (D-532); 12/12; gate 2306 passed |
| P4 light (re-open) | approved | qa PASS-WITH-NOTES, ux PASS-WITH-NOTES (R6-1..R6-5 LOW → BACKLOG), security delta PASS-WITH-NOTES |
| P5 re-close | closed, then re-opened (D-535) | canon re-folded; BACKLOG updated; validator 0 block (`05-close.md`) |
| P3 increment 007 (second re-open) | done (revision 1) | 1 SOURCE; A-12; non-lanes output byte-identical; 6/6; gate 2306 passed |
| P4 light (second re-open) | approved | qa PASS-WITH-NOTES, ux PASS-WITH-NOTES (N-1..N-3, G-009, G-010 → BACKLOG) |
| P5 second re-close | closed | canon re-folded; BACKLOG updated; validator 0 block (`05-close.md`) |
| US-501 waits-on links | READY | contract rules 1–4 |
| US-502 `L` links | READY | rules 5–7; D-B2 picker, D-A link mode |
| US-503 details section | READY | D-B inside `TaskDetails` |
| US-504 archive/delete guard | READY | round-3 ruling |
| US-505 one-time link migration | READY | `deps_logic.migrate`; operator safeguard |
| B2 (milestones, moving linked dates, the M-3 offer) | OUT → BACKLOG | D-501 |

## Roadmap + increment plan

Re-cut after P2 iteration 1 (A-7, C-21: AT-507, AT-508 added) — the migration first, so no increment ever reads a legacy board under the new meaning:

1. Increment 001 — the one-time link migration (US-505): `migrate_links`, `run_link_migration` (backup, log, mark, atomic save, fail closed), `on_mount` first act, the multi-task undo; the fixture seam (`kg_board` marked) and the census of app-started test boards. Also `b` = external block (A2-3). TC-514..516, part of TC-506 and TC-518; AT-506..508. SOURCE: `models.py`, `app.py`.
2. Increment 002 — the waits-on model, marks and guard (US-501, US-504 minus the project archive): derivations, `◂N`/`▸N`, the gutter and `_flowing`, `b` = external block, ready toasts, the `x`/`d`/editor guard. TC-501..506, 517, 518; AT-501, AT-505. SOURCE: `models.py`, `views.py`, `app.py`.
3. Increment 003 — `L`, the picker (D-B2), link/unlink with undo, the details section (D-B), the project-archive guard, README; `BlockerPicker` retired. TC-507..510, 513; AT-502, AT-504 (+ AT-505's project arm). SOURCE: `keymap.py`, `app.py`, `modals.py`, `models.py` (⚠ at the cap).
4. Increment 004 — the gantt link mode (D-A). TC-511, 512; AT-503. SOURCE: `modals.py`, `views.py`, `app.py`.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-04 | Batch id `2026-10-04-batch-01`, ids in a disjoint `5xx` range | operator's local date (commission); `0xx`..`4xx` taken |
| 2026-10-04 | D-501: run B1 only (stories 1–4 + the link half of story 7); B2 — milestones (M-1/M-2), moving linked dates (round 6), the M-3 one-time milestone offer — to `BACKLOG.md` | pre-authorized split; P0 feasibility: B1 alone is 4 increments over 5 SOURCE files; B2 needs a Task flag, a date-cascade engine, a gantt edit bar that does not exist (`grep "edit bar\|milestone\|date_links" taskboard/` → 0, G-C was deferred) and a second migration |
| 2026-10-04 | D-502: trigger family A judged not fired | dependency logic lives in `models.py` with the shipped dependency seat; no module created |
| 2026-10-04 | P0 approved under the standing authorization | `01-requirements.md` §2.6 |
| 2026-10-04 | P2 iteration 1 → iterate-to-refine (Q-1, A-1 blockers; 0 HIGH); P1 iteration 2 approved: folds, re-cut (migration first), D-515..D-525 | `02-review.md`, LED .6–.10 |
| 2026-10-04 | P2 iteration 2 approved: 16 minors folded at the gate (LED .11); D-518 confirmed as exit rather than open unmigrated | `02-review.md` §Iteration 2 |
| 2026-10-04 | Increment 001 approved (revision 4): A-1, A-2, D-526; R2-F1 (HIGH in tests only) fixed without stopping, RED-first, re-reviewed | `03-increments/increment-001.md` |
| 2026-10-04 | Asked at the gate — F2: "Corregir en el 002" (setup branch first in `action_archive`; RED-first; r2, battery, review; close S-7) | operator, 2026-10-04 |
| 2026-10-04 | Asked at the gate — D-515: "Sí, conservarla"; D-517: "Sí, no vuelve a correr"; D-501 split confirmed | operator, 2026-10-04 |
| 2026-10-04 | STOPPED on increment 002 code review F2 (HIGH, product): the operator's ruling is owed | standing authorization: a HIGH in app behaviour stops |
| 2026-10-04 | Asked at the gate — F1: "Corregir en el 003"; authorization amendment "Sí, solo en el incremento en curso" | operator, 2026-10-04 |
| 2026-10-04 | STOPPED on increment 003 code review F1 (HIGH, product): the operator's ruling is owed | standing authorization: a HIGH in app behaviour stops |
| 2026-10-04 | Increment 004 approved (revision 3): F1 (HIGH, product, increment under construction) fixed without stopping under the amendment, RED-first, re-reviewed; A-7 three status rows; D-527 link mode offers the tasks the gantt draws | `03-increments/increment-004.md` |
| 2026-10-04 | P4 approved: qa, ux, security PASS-WITH-NOTES; increment 005 (the folded-waiter note, A-8) approved revision 3; D-528 fold rule, D-529 lanes title, D-530 the Windows temp file → the operator at close and BACKLOG | `04-validation.md`; `03-increments/increment-005.md` |
| 2026-10-04 | Asked at the gate — visual verdict (`evidence/operator-verdict-provisional.json`): PV-1..PV-7 "Aceptar"; D-528, D-529, D-530 "Corregirlo antes del push"; a new feature request (project presentation with SVG/image export) → BACKLOG, prototype round first | operator, 2026-10-04 |
| 2026-10-04 | D-531: re-open by iterate-to-refine to P3 (increment 006, amendments A-9..A-11), light P4, re-close P5 — the D-422 path; no new batch | the verdict changes product code after P5 |
| 2026-10-04 | Increment 006 approved (revision 2): A-9..A-11; D-532 (cross-platform read-only refusal), D-533 (lanes show no marks at 118 — stated for the operator), D-534 (one page holds both); code review M1 fixed RED-first in the increment under construction; security delta PASS-WITH-NOTES with the safeguard re-run | `03-increments/increment-006.md` |
| 2026-10-04 | Light P4 approved; P5 re-closed: the canon re-folded from the amended statements, BACKLOG updated (the three rulings done; the presentation feature and R6-1..R6-5 added) | `05-close.md` |
| 2026-10-04 | Asked at the gate — D-533: "Dejar ◂ solo, quitar la edad antes" (in lanes the age `·Nd` drops first, then `▸`, then other meta; `◂` stays while the title keeps its 6-cell minimum); D-532: "Sí, en todas las plataformas" (the read-only refusal on every platform; no code change) | operator, 2026-10-04 |
| 2026-10-04 | D-535: re-open again by iterate-to-refine to P3 (increment 007, lanes only, amendment A-12), light P4, re-close P5 — the D-422 path | the ruling changes product code after P5 |
| 2026-10-04 | Increment 007 approved (revision 1): A-12 — in lanes the age sheds first, `◂` last; code review OK, no findings; identity proof 4,404 (mine) / 10,124 (reviewer) renders unchanged outside lanes | `03-increments/increment-007.md` |
| 2026-10-04 | Light P4 approved after increment 007; P5 re-closed again | `04-validation.md`; `05-close.md` |
| 2026-10-04 | **Provisional rulings for the operator** (autonomous, reversible): D-515 a legacy blocked task whose last link is already done keeps its flag; D-517 `u` after the migration keeps the mark (no automatic re-run) | architect A-2, A-4 |
| 2026-10-04 | P1 approved under the standing authorization; D-503 one overlap measure (a start on the due day conflicts); D-514 IFC Part B written by the increments | `01-requirements.md` |

## Provisional visual decisions (for the operator, with the captures to compare)

Listed at P1, captured at P3, closed at P5 (`05-close.md`). Each is the most conservative reversible reading where the verdict frames leave a detail open.

| Id | Decision | Captures (before → after, `evidence/captures/`) |
|---|---|---|
| PV-1 | Card marks `▸M ◂N` in the muted tone where `⛓M` stood, `▸` shed first (D-506); `◂` also reads as the conflict prefix, the details heading and the gantt's off-window glyph — on cards it always carries a count (ux UX-22) | `base-kanban-*` → `close-kanban-*`; `base-kanban-lanes-*` → `close-kanban-lanes-*` |
| PV-2 | The gantt keeps its one-cell `↳` gutter, on the open-predecessor rule and the one overlap measure; no `◂N▸N` in the gantt label (D-505) | `base-gantt-*` → `close-gantt-*` |
| PV-3 | The picker is a centred modal like the other pickers: title, filter, count, "linked now", create row, two sections of two-line options, keys line | — → `close-picker-*` |
| PV-4 | The dependency section sits in the details view after the info grid and before Notes; the editor is unchanged (D-507) | `base-details-*` → `close-details-*` |
| PV-5 | Link mode: a full-screen gantt with the candidate as its selection; the connector in the bright tone from the candidate's due cell; the overlap `═` in the over tone on the waiter's row; three status rows at the bottom — what is linked, the timing, the keys with the loop legend after them (A-7) | — → `close-gantt-link-*` |
| PV-6 | The migration, guard and ready toasts' wording (LLR-501.4, LLR-504.1, LLR-505.3) | — → `close-guard-*`, `close-ready-*`, `close-migration-*` |
| PV-7 | Rule 9′'s boundary under the one measure: a start ON the predecessor's due day is a 1-day conflict (the verdict frames said "starts before"); wording "overlaps Nd" (D-503, qa Q-12) | `base-gantt-*` → `close-gantt-*`; `close-picker-*` |

## Risks / watch-items

- The base board's `b` wrote links that the new rules would read as live waits: the migration (US-505) must run before the first paint; its rule is the prototype's asserted one (`evidence/p1-deps-logic-rerun.txt`).
- `◂`/`▸` are also the gantt's off-window glyphs; on cards they always carry a count.
- The key bar's more layer gains one key (`L`): key-bar width tests move (reverse census).

## Conventions honored

- Test docstrings in the house style (field report · law · RED), AT/TC ids in docstrings and names.
- User text as Text pieces only (S1, batch 2026-10-02-batch-04); toasts `markup=False`.
- Colour budget: accent = focus/today only.
- No new dependency; Textual 8.2.8 / Rich 15.0.0.

## Out-of-scope carries

- B2 (D-501) and batch C (`6` reserved for the chain map view); everything else in `BACKLOG.md`.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| increment-007 gate run (frozen r1) — the final product | 2026-10-04 | 2306 passed in 432.92 s, exit 0 (`evidence/inc007-gate-r1.txt`) |
| increment-006 gate run (frozen r2) | 2026-10-04 | 2306 passed in 414.80 s, exit 0 (`evidence/inc006-gate-r2.txt`) |
| increment-005 gate run (frozen r3) | 2026-10-04 | 2295 passed, 1 failed (clipboard environment flake) in 444.93 s (`evidence/inc005-gate-r3.txt`) |
| increment-004 gate run (frozen r3) | 2026-10-04 | 2294 passed, 1 failed (clipboard environment flake) in 576.52 s (`evidence/inc004-gate-r3.txt`) |
| increment-003 gate run (frozen r2) | 2026-10-04 | 2281 passed, 1 failed (clipboard environment flake) in 408.93 s (`evidence/inc003-gate-r2.txt`) |
| increment-002 gate run (frozen r2) | 2026-10-04 | 2265 passed in 355.60 s, exit 0 (`evidence/inc002-gate-r2.txt`) |
| increment-001 gate run (frozen r4) | 2026-10-04 | 2242 passed in 311.84 s, exit 0 (`evidence/inc001-gate-r4.txt`) |
| `python -m pytest -q -p no:cacheprovider` (base `0447070`) | 2026-10-04 | 2218 passed in 339.95 s, exit 0 (`evidence/base-suite.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.

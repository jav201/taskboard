# PLAN — 2026-08-14-batch-04 (living compendium)

**Batch objective.** Kanban operability: implement the 11 operator-approved
improvements K1–K11 (prototypes reviewed and approved 2026-08-14, artifact
`prototypes/kanban_ideas/out/kanban-ideas.html`), plus reconcile this session's
uncommitted work (aperture wiring, prism hero fix, gallery re-captures) into a
reviewed increment.

**Mode:** `core` (proposed at intake; family E fired: ≥3 stories). Language: `en`.
**Where we are:** Phase 0 — intake & refinement, awaiting kickoff gate.

## Verified at intake (executed, not asserted)

- **RC-1 base currency:** `git fetch origin` 2026-08-14 → `HEAD == origin/main ==
  merge-base == 47726e8`. Branch current. Working tree DIRTY (36 files) — see
  risks.
- **Flow currency (C-45 PULL):** `~/.claude/skills/dev-flow` == backup repo
  `~/kimi/agent-skills/dev-flow` at **rev25** (0 real diffs, 0 missing both
  directions; only line-ending style differs). Verified by full-tree walk.
- **Backlog read:** `.dev-flow/BACKLOG.md` (refreshed 2026-08-07). No open item
  blocks this batch; the kanban-variants merge is shipped. Carries noted below.
- **Prototypes approved:** operator verdict "Quiero todas :P" (2026-08-14),
  K5 limits "implementa con tu recomendación" (default `Doing ≤ 3`, per-phase,
  settings-driven).

## Stories (11 + reconciliation) — INVEST

| id | story | status | observable outcome (the AT surface) |
|---|---|---|---|
| R-00 | Reconcile uncommitted session work (aperture `6`, prism hero, captures, README) | READY | `pytest` 778 green; key `6` opens ApertureScreen (verify_aperture ALL PASSED) |
| R-01 | K1: `[`/`]` move selected task one phase back/forward, dated | READY | pilot: phase + `phase_changed` change; ends are no-ops |
| R-02 | K4: `!` cycles priority low→normal→high; `b` toggles blocked | READY | pilot: fields change + render markers (`!`, ▲) |
| R-03 | K2: `s` cycles column sort (project→priority→due→recent) | READY | render order changes per mode; **nav order == render order** (the parallel-model trap) |
| R-04 | K3: `g` cycles column grouping (project→priority→horizon) | READY | group headers change per mode; nav parity |
| R-05 | K5: WIP limits per phase (default `Doing≤3`), header burns over limit | READY | header shows `n/limit`; over-limit → `over` tone |
| R-06 | K6: kanban cards show aging `·Nd` from `phase_changed` | READY | card with dated move shows `·Nd`; undated shows nothing |
| R-07 | K7: collapse a phase to one summary row (toggle) | READY | collapsed column = 1 row `✓ N`; toggle restores |
| R-08 | K8: focus mode cycles project filter (Esc exits) | READY | only focused project's cards render; header names it |
| R-09 | K9: `+`/`-` (and `=`) bump selected task's due date ±1 day | READY | due_date moves ±1d; undated → today+1 |
| R-10 | K10: `u` undoes last board mutation (session-level) | READY | mutate then undo → field/phase/task restored |
| R-11 | K11: weekly standup modal (moved/closed this week per project) | READY | modal lists only `phase_changed` ≤7d tasks, grouped |

## Trigger evaluation (id · verdict · probe)

- **B1** (touched symbol asserted by other requirements' tests) — **FIRED**:
  `grep -rl "card_cell\|_kanban_groups\|_windowed_header\|KEYMAP" tests/` →
  `test_app.py`, `test_keymap.py` (778 tests assert these symbols).
  → reverse census (C-26) + design review at Phase 2.
- **B2** (file location move) — did not fire: no file moves planned (probe: story list).
- **B3** (byte-identical goldens) — did not fire: `ls tests/` → no `goldens/` dir.
- **B4** (artifact consumed downstream) — did not fire: no new on-disk artifacts.
- **C** (security patterns) — did not fire: no auth/secrets/network/destructive
  DB. Markup over user text already escaped at existing seats (`escape` in
  views.py); K6 adds no new interpolation of raw file text (probe: grep
  `markup=` taskboard/ → Static default; titles pass through `escape`).
- **D** (interaction change) — **FIRED**: 13 new keys + one modal →
  `ux-reviewer` joins the PDR.
- **E** (≥3 stories) — **FIRED**: 11 stories → lane raised `fast` → `core`.
- **F** (flow currency) — verified current (rev25, see above); backlog refresh
  due at Phase 6 (last: 2026-08-07).

## Increment plan (≤4 source files each, tests uncapped)

| inc | content | source files (planned) |
|---|---|---|
| 0 | R-00 reconciliation review + landing decision | (already written: app, keymap, aperture, hero, README) |
| 1 | R-01 + R-02 (K1, K4) | keymap.py, app.py |
| 2 | R-03 + R-04 (K2, K3) + nav-parity oracle | views.py, app.py, keymap.py |
| 3 | R-05 (K5) | views.py, models.py (settings) |
| 4 | R-06 + R-07 (K6, K7) | views.py, app.py, keymap.py |
| 5 | R-08 + R-09 + R-10 (K8, K9, K10) | app.py, keymap.py |
| 6 | R-11 (K11) | modals.py, app.py, keymap.py |

## Risks / watch-items

- **Dirty base (36 uncommitted files)** from the pre-batch session: aperture
  wiring, prism hero fix, gallery re-captures, `prototypes/kanban_ideas/`,
  deleted temp files. Inc 0 exists precisely to land them reviewed; C-44 sweep
  at close covers the rest (incl. auxiliary repo `~/kimi/taskboard-overhaul`,
  untracked scratch — NOT this repo).
- **nav/render parallel model** (known most-expensive bug class, BACKGROUND §7):
  R-03/R-04 change render order — the nav model MUST be derived from the same
  ordering function, with a parity AT.
- `verify_language.py` carries **52 latent failures** (merge-era, measured
  pre-batch via stash isolation): NOT this batch's scope; candidate backlog item.
- Board actions on the aperture: every new key MUST join `BOARD_ACTIONS`
  (check_action drop) — else keys act on the hidden board behind the aperture.

## Conventions honored

≤4 source files/increment · tests uncapped · README key table must document
every bound key (test_keymap enforces) · no commits/push without operator
decision at the merge gate · artifacts in English, conversation in Spanish ·
RED counterfactual mandatory per AT · every acceptance falsifiable (C-40).

## Out-of-scope carries

52 verify_language latent failures · `prototypes/` vs `_prototypes/` decision ·
darkside board-size dead zone (operator deferred) · K12+ (subtasks, recurring,
dependencies, bulk select) — parked, operator said "no los descarto".

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-14 | Batch opened under /dev-flow, lane `core` (E fired) | orchestrator, pending operator gate |
| 2026-08-14 | K5 defaults: `Doing ≤ 3`, per-phase, settings-driven | operator ("implementa con tu recomendación") |
| 2026-08-14 | Collapse toggle key `z` (prototype said `u`; `u` reserved for undo K10) | orchestrator default, pending gate |
| 2026-08-14 | Phase 0 approved; autonomy + merge + decision-recording granted, verbatim "dale con merge aprobado" | operator |
| 2026-08-14 | Batch artifacts live in `.dev-flow/2026-08-14-batch-04/`, NOT the `.dev-flow/` root — the root files are batch-03's retained records (qa-reviewer catch, C-50) | orchestrator |
| 2026-08-14 | REVERSED the above: repo convention is root=current batch (batch-03 overwrote batch-02's the same way; validator reads root paths). `01-requirements.md` + `01b-qa-validation-plan.md` at root; batch-03's preserved in git history. PLAN.md stays in the batch dir | orchestrator |

## Test ledger

| node | suite | last run | result |
|---|---|---|---|
| tests/ | pytest | 2026-08-14 | 778 passed (pre-Inc-1 baseline) |
| tests/test_keymap.py | pytest | 2026-08-14 (qa F-1, orchestrator-verified) | **3 FAILED** — pre-batch session seeded `[`/`]`/`!`/`b` into KEYMAP + BOARD_ACTIONS without handlers/README rows. Batch-scope: Inc 1 closes them. Phase-4 "green" = EMPTY failure set, not "no worse than base". |
| prototypes/verify_aperture.py | harness | 2026-08-14 | ALL PASSED |
| prototypes/verify_language.py | harness | 2026-08-14 | 52 pre-existing failures (not batch scope) |

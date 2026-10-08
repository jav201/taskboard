# PLAN — taskboard — Batch 2026-10-07-batch-06

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 in both modes; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/docs/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-07-batch-06 |
| Objective | Operator-feedback batch: make the dependency web actionable where it is seen -- the chain map draws every open task (linked as today, unlinked as selectable open-chain-head tiles) so chains can be CREATED on the map with L (the C-2b oracle frames amend under a formal LED, the operator's visual re-verdict pending at close); and the kanban window shows its hidden sides -- markers on the phase-head row plus help |
| Standing authorization | Operator (Javier), 2026-10-07: two UX reports from real use -- kanban hides the later phase columns with no on-screen sign of the window ("no logro ver el resto... incluso reescalando"), and the chain map shows projects with no tasks and no way to create a chain ("es imposible crear cadenas"). Read with the established chain: Gates -- autonomous with the two exceptions; Git -- the COORDINATOR commits and pushes at each close (no PR); data safeguard -- synthetic boards only; implementing agents (DeepSeek instances under coordinator briefs, the standing 'Sigue usando Deepseek') do NOT commit/push/stash. The C-2b oracle amendment ships under a formal LED with the operator's visual re-verdict requested at close. This batch runs in the MAIN checkout. (Verbatim in `state.json` `standing_authorization.operator_words`.) |
| First gate | the batch opened by rollover from 2026-10-07-batch-05 (`8284d3a`); the seed readback was clean (state.json `batch_id` rolled to 2026-10-07-batch-06, the ledger seeded with LED-2026-10-07-batch-06.1); the validator baseline at the seed read 0 block · 51 notice (re-verified by the close-out before its fills) |
| Premises / RC-1 | RC-1: local HEAD `8284d3a` == `origin/main` as of the batch's open (pushed at batch-05's close); premises P-1..P-3 in `01-requirements.md` §2.7, all TRUE with executed evidence (P-1: the shipped L LinkPicker flow works off-view, reproduced on a read-only copy of the operator's board -- the fix moves creation INTO the map; P-2: the nav/selection machinery and the `○` glyph already exist -- the tiles are an admission change; P-3: the sealed frames pin the inert row the LED amends) |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| — | not evaluated | `state.json`'s trigger block still reads "NOT EVALUATED" at this close — the P0 trigger evaluation was not rewritten this batch; no trigger fired on the evidence available (the batch's carries came from the operator's direct reports, not a trigger probe) |

## Where we are

Batch CLOSED at the record level, 2026-10-07: both increments implemented by one session and
green (two full-suite passes at 2566), the coordinator's mutation battery M9-M12 all KILLED, the
record filled (packets · validation PASS · this close), the validator at 0 block. Owed next: the
orchestrator's ONE C-25 run; the coordinator's commit + push + `--fold-canon`; and the operator's
visual re-verdict on the amended frames + the new chrome (pending — the batch pushes under the
commission; the operator's verdict folds on arrival).

## Objective

Restated: where the operator looks, the work is actionable. The chain map admits every open task
(`○` tiles), chains are created on the map with the shipped `L` picker, `x` leaves a tile, the
`no links` row survives only for a no-open-work project, and the C-2b oracle amends under
LED-2026-10-07-batch-06.1. The kanban phase-head row marks its hidden sides (`◂` / `▸ N` exact)
and the `?` help names the window.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1201 (chains created on the map) | ✅ done — AT-1201 green | the `○` tiles + L/x/nav on the map + the strip truth; the amended TC-801/TC-802/TC-810; M9/M10/M11 KILLED |
| US-1202 (the kanban shows its hidden sides) | ✅ done — AT-1202 green | `◂`/`▸ N` + the `?` bullet; the two pinned arms updated; M12 KILLED |
| P0..P5 stations | closed at the record level | one implementing session, two increments; the coordinator's review gate `approve`; validation PASS |

## Roadmap + increment plan

- Increment 001 — the kanban window markers (LLR-1202.1): small, shipped first.
- Increment 002 — the chain map admits every open task (LLR-1201.1/.2) + the oracle amendment
  (LED-2026-10-07-batch-06.1): the meaty one, serialized after 001 in the same session.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-07 | The C-2b oracle amends under a formal LED: the amended frames are the new renderer's bytes on the SAME frozen fixture at the batch's evidence home; the test's FRAMES path moves citing the LED; the sealed batch-02 frames stay history | the tiles move every band's bytes — an unamended oracle would pin the old renderer forever; a hand-edited oracle would be unverifiable |
| 2026-10-07 | Root fixes over the discovery-only alternative, for BOTH reports | the coordinator weighed a discoverability-only remedy (help text alone) against surface changes; the operator's "es imposible crear cadenas" — a dead-end surface, not merely an undocumented one — decided it |
| 2026-10-07 | The batch refines the window marks rather than invents them | the shipped `◀ N`/`N ▶` chrome (pinned by test_app.py) was found at review; the contract's glyphs were corrected to the refinement law (`◂` / `▸ N` + the left-edge case + the bullet) |

## Risks / watch-items

- Denser real boards will see bands fold that used to fit (the tiles add rows) — the amended frames
  record this for the kg fixture; the operator's visual re-verdict is the check · mitigated by the
  fold law's shipped behavior (the `+N more ↓` cap) and the verdict itself.
- The `V22` canon fold-back fires as the close gate's only block class (5 × V22 over the batch's
  HLR/LLR ids) — discharged at the coordinator's commit (`--fold-canon`; the close-out never edits
  `REQUIREMENTS.md`). `V2` is clean — the AT-1201/AT-1202 dash tokens already sit in the test files'
  docstrings.

## Conventions honored

- One implementing session, both increments serialized; scratch under the batch's `evidence/`; no git mutations by the implementing agent.
- English artifacts; reserved field names literal; synthetic boards only.
- The sealed batch-02 frames read-only as history.

## Out-of-scope carries

- The operator's visual re-verdict on the amended frames + the new chrome (pending; batch C's form).
- Batch-07 (queued, the operator's request — contract at its P1): process/chain templates — user templates in settings + factory presets, a `T` picker, one undo step.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `pytest tests/test_kanban_window.py tests/test_kanban_readable.py tests/test_cells.py -q` | 2026-10-07 (the session, re-verified at the close-out's review) | 399 passed |
| `pytest tests/test_chainmap.py tests/test_chainmap_app.py -q` | 2026-10-07 | 19 passed |
| `pytest tests/test_app.py -q -k "kanban"` | 2026-10-07 | 30 passed, 132 deselected |
| `pytest -q` (full suite, the settled tree) | 2026-10-07 | 2566 passed ×2 (447.08s · 422.53s — `evidence/inc001-run.log`); the orchestrator's C-25 owns the ONE final run |
| `pytest tests --collect-only -q` (the close-out's re-collection) | 2026-10-07 | 2566 tests collected — reconciles with 2556 − 0 + 10 |

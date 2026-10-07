# Increment 001 — LLR-701.1-.3 · The P4 residue closed

| Field | Value |
|---|---|
| Batch | `2026-10-07-batch-01` |
| Increment | `001` (the batch's only increment) |
| Requirement(s) | `LLR-701.1` · `LLR-701.2` · `LLR-701.3` |
| Acceptance | `TC-701` · `TC-702` · the whole-suite oracle |
| Agent | `software-dev` — **DeepSeek V4 Pro (product) + DeepSeek V4.1 Flash (tests) in parallel**, orchestrated by the coordinator; reviewed by the four lenses |

## 1 · What changed

The P4 residue of batch 2026-10-06-batch-01, behavior-preserving throughout. PRODUCT
(V4 Pro): `models.py` gains `date_base(stored, today)` — the ONE "undated means today" rule,
now shared by `bump_due` and `plan_move`'s undated branch; both hand-rolled date-restore loops
in `app.py` (`action_cascade_mode`, `action_undo`'s cascade branch) call the tested
`models.restore`; `Plan.conflicts` documents itself as the tested totals intermediate.
TESTS (Flash): `TC-701` pins the C-5 vanished-task refusal (synthesized entry — the UI cannot
reach it); `TC-702` pins the toast's narrow-width degradation (fits ≤ width at 80/60/40/24,
non-empty at 24, via `pilot.resize_terminal`).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-701.1 | `date_base`; `bump_due`/`plan_move` use it; the `Plan.conflicts` doc |
| `taskboard/app.py` | source | LLR-701.1 | both restore sites call `models.restore` |
| `tests/test_cascade_app.py` | test | TC-701 · TC-702 · LLR-701.2 · LLR-701.3 | +54 lines, append-only |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 1 (uncapped) |

## 4 · Test results

Full suite: **2514 passed, 0 failed** (V4 Pro's run, 385s; the final coordinator run in
`evidence/close-gate.txt`). The refactor's oracle is the whole suite — a behavior change
reddens it; the lenses verified the equivalence branch-by-branch (qa QAR-3/4, architect
ARCH-R-2, security SEC-R-1's traces, ux UXR-1's mutation pass).

### RED counterfactual / mutation verdicts

The behavior-preserving refactor has no observable mutants by design; the PINS' mutants were
executed LIVE by the ux-lens during P2/P4: the C-5 gate removed → TC-701 RED; `_cascade_toast`'s
width hardcoded to 118 → TC-702 RED — both reverted, post-revert diff byte-identical
(`ux-reviewer`, mutation pass, both reverted and confirmed). The harness's RED-proof: the
inc001 seeded-packet V9 notices predate this packet.

## Evidence files

| Artifact | Path | SHA-256 |
|---|---|---|
| the close suite | `evidence/close-gate.txt` | `76846dd73146a53ce687357b708b43b600599ae704fb35cff8bc148dcb611bb5` |
| the product agent's run | `evidence/chunkA-run.log` | (cited by content) |
| the tests agent's run | `evidence/chunkB-run.log` | (cited by content) |

## 4b · Independent review

Four lenses over the 40-line delta (the P2/P4 combined swarm per the batch's size):
qa PASS-WITH-NOTES (QAR-1: TC-702 pins the floor-guard + the non-empty-at-24 arm — real but
narrow) · architect PASS · security PASS (SEC-R-1: none) · ux PASS-WITH-NOTES (UXR-1: the
60/40/24 rungs assert the constructed string, not the painted widget — accepted: the 80 rung
has painted evidence in AT-607, and a plain-text toast's string is the near-complete visual
truth). No HIGH, no MEDIUM, no folds owed.

## 5 · Risks / 6 · Pending

None beyond the notes. BACKLOG takes nothing new — the five residue items close here.

## Increment gate checklist: all ✓ (2 source files; tests in the same pass; REDs executed by
the lenses' mutation pass; reverse census: bump_due/restore asserted by test_momentum/
test_milestone_offer — green; the code-reviewer lens passed; evidence in chunkA/chunkB run
logs + close-gate.txt).

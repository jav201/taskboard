# Increment 005 — HLR-007 · `Focus Board cursor stays on a drawn card (adopted)`

| Field | Value |
|---|---|
| Batch | `2026-09-30-batch-01` |
| Increment | `005` |
| Lane (if the batch forked) | n/a — one lane |
| Requirement(s) | HLR-007, LLR-007.1 |
| Acceptance | AT-009 |
| Agent | `software-dev` (adopting another session's change) |
| Date | `2026-09-30` |

## 1 · What changed

ADOPTED, not authored here: the Focus Board fix from another session, in the working tree
before this batch, brought in by owner verdict 2026-09-30. `TaskboardApp._select_first`
(`taskboard/app.py`) chooses, in the focus view, among `focus_tasks(board, show_archived)`
— the cards the Focus Board draws — so `t` on the selected card moves the cursor to a drawn
card and the next `t` acts on what the user sees. This packet adds only the AT id to the test's
docstring.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | HLR-007, LLR-007.1 | `focus_tasks` import; focus branch in `_select_first` |
| `tests/test_focus.py` | test | AT-009, HLR-007 | `test_unpinning_the_selected_task_moves_the_cursor_within_focus` (other session); AT id added |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 |
| Doc files | batch record only |

## 3 · How to test

`python -m pytest -q tests/test_focus.py -k unpinning`

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none — no unit met the decision or boundary criterion | n/a |
| **A · white-box** | `core` · `full` | — | n/a |
| **B · black-box** | `core` · `full` | AT-009 `test_unpinning_the_selected_task_moves_the_cursor_within_focus` | 1 passed (full suite) |

### RED counterfactual

| Field | Value |
|---|---|
| **RED counterfactual** | executed by me in a scratch copy (`/tmp/rb`) with the HEAD `taskboard/app.py`: `1 failed` — "the cursor stayed on the card the view no longer draws" (`inc005-red-on-base.txt`) |
| **Mutation verdicts** | 1 mutation (the base `app.py`): KILLED |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | 1 artifact: the app's selection and board state after real `t` key presses |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc005-red-on-base.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc005-red-on-base.txt` | `43f6f4f26064f1e6e9be4c5adcd7a614c42367361a05cf3a79da81b08b0fee01` |
| full-suite-after.txt | `.dev-flow/2026-09-30-batch-01/evidence/full-suite-after.txt` | `a64ea72a3221a02a0467518571349064ab54f545db08e5c11c9276924fe5fc15` |

| Field | Value |
|---|---|
| **Evidence files** | 2 artifacts, each cited above with its SHA-256 |

### Load-bearing emptiness

none — no claim rests on an absence.

### Reverse census

| Field | Value |
|---|---|
| **Reverse census** | B1 `grep -rln "_select_first\|focus_tasks" tests/` → `test_focus.py` — full suite green; B2/B3 did not fire; B4 none; A3 `focus_tasks` already exported by `views.py` |
| **Correction population** | none — no correction |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md over the adopted diff · PASS, 0 HIGH, no findings |

## 5 · Risks

- None beyond the existing F-3 law it restores.

## 6 · Pending items / spec deviations

- Authored by another session; adopted with its test; RED re-captured here.

## 7 · Suggested next task

none.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | §2 |
| 2 | Tests written in this same increment | all | ✓ | other session's test, adopted |
| 3 | Layer 0 written where the criterion applies | `core` · `full` ‹one complete run owned by the orchestrator ~ Layer 0› | ✓ | §4 |
| 4 | **RED counterfactual** declared | `core` · `full` ‹RED counterfactual mandatory ~ RED counterfactual› | ✓ | §RED |
| 5 | **Reverse census** declared | `core` · `full` ‹reverse census of the touched symbol ~ Reverse census› | ✓ | §Reverse census |
| 6 | `code-reviewer` passed | `core` · `full` ‹RED counterfactual mandatory ~ code-reviewer› | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | no signature changed |
| 9 | Coverage claims verified on disk | all | ✓ | nodes collected and run |
| 10 | Load-bearing emptiness declared | all | ✓ | §Load-bearing emptiness |
| 11 | **Mutation verdicts** declared | all | ✓ | §RED |
| 12 | **Instrument RED-proof** declared | all | ✓ | §Instrument |
| 13 | **Correction population** declared | all | ✓ | §Correction |
| 14 | **Emitted-form assertion** declared | all | ✓ | §Emitted |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §Evidence |

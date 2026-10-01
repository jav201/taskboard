# Increment 004 — HLR-006 · `A /-filtered gantt or kanban keeps its panel height (adopted)`

| Field | Value |
|---|---|
| Batch | `2026-09-30-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | n/a — one lane |
| Requirement(s) | HLR-006, LLR-006.1 |
| Acceptance | AT-008 |
| Agent | `software-dev` (adopting the operator's own change) |
| Date | `2026-09-30` |

## 1 · What changed

ADOPTED, not authored here: the operator's gantt-filter fix, already written and tested in the
working tree before this batch, brought into the batch by owner verdict 2026-09-30. In
`render_view` (`taskboard/views.py`) a filtered gantt/kanban is rendered at
`bar_h = max(1, height - 2)`, because the `/` bar is inserted under the header — drawn at full
height, the gantt's last two rows (the time scale and the close) fell under the fold. This
packet adds only the AT id to the two tests' docstrings.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-006, LLR-006.1 | the `bar_h` hunk in `render_view` (3 lines + comment) — the rest of this file's diff is increment 002 |
| `tests/test_gantt.py` | test | AT-008, HLR-006 | 2 tests at the end (operator-written); AT id added to their docstrings |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 |
| Doc files | batch record only |

## 3 · How to test

`python -m pytest -q tests/test_gantt.py -k filtered`

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none — no unit met the decision or boundary criterion (one expression) | n/a |
| **A · white-box** | `core` · `full` | — | n/a |
| **B · black-box** | `core` · `full` | AT-008 `test_filtered_gantt_keeps_its_time_scale_inside_the_panel`, `test_filtered_kanban_fits_the_panel_too` | 2 passed (full suite) |

### RED counterfactual

| Field | Value |
|---|---|
| **RED counterfactual** | executed by me in a scratch copy (`/tmp/rb`, product tree untouched): `bar_h` replaced by `height` in both `render_*` calls → `2 failed` — "filtered gantt is 22 rows in a 20-row panel", "filtered kanban is 22 rows in a 20-row panel" (`inc004-red-on-base.txt`) |
| **Mutation verdicts** | 1 mutation (the one above): KILLED, both arms |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | 1 artifact: the rendered view text, row count and scale row |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc004-red-on-base.txt | `.dev-flow/2026-09-30-batch-01/evidence/inc004-red-on-base.txt` | `201ebdc2be16772b7d5dad2110b8c258da6a9d54317123851e74bc937d6b9a88` |
| full-suite-after.txt | `.dev-flow/2026-09-30-batch-01/evidence/full-suite-after.txt` | `a64ea72a3221a02a0467518571349064ab54f545db08e5c11c9276924fe5fc15` |

| Field | Value |
|---|---|
| **Evidence files** | 2 artifacts, each cited above with its SHA-256 |

### Load-bearing emptiness

none — no claim rests on an absence.

### Reverse census

| Field | Value |
|---|---|
| **Reverse census** | B1 `grep -rln "search_query" tests/` → `test_gantt.py`, `test_app.py` filter tests — full suite green; B2/B3 did not fire; B4/A3 none — `render_view` signature unchanged |
| **Correction population** | none — no correction |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md over the adopted hunk · PASS-WITH-NOTES, 0 HIGH / 2 LOW · F1 (panels of 3 rows or fewer still overflow — the renderer's own minimum) recorded, no change; F2 (kanban test only counted rows) folded — it now also asserts the filter bar and the matching card |

## 5 · Risks

- `height - 2` assumes the filter bar is exactly two rows; if the bar grows, this drifts.

## 6 · Pending items / spec deviations

- Authored by the operator outside this batch; adopted with its tests; RED re-captured here.

## 7 · Suggested next task

none.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | §2 |
| 2 | Tests written in this same increment | all | ✓ | operator-written, adopted |
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

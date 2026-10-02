# Batch close — taskboard — Batch 2026-09-30-batch-01

> Template: flow `templates/close-template.md` (core). Reserved field names kept literal.
> **Not committed**: the commission withholds every git write; the owner commits.

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | rev97 canon export: `cd C:\Users\jjgh8\.claude\jobs\381ba33e\tmp\flow-rev97 && PYTHONUTF8=1 python docs/tools/devflow-validate.py --brief C:\Users\jjgh8\Github\taskboard` · exit 1 · 33 block / 14 notice · 2026-09-30 · `evidence/validator-close.txt`. **0 project-side BLOCKs.** The 33 are environment-only flow-identity findings about `~/.claude` (mid-rev98, not this batch's to touch): 1× V7, 30× V15, 2× V16. V57 (dirty tree) clears only after the coordinator's commit; the coordinator re-runs the gate and records the HEAD in `Gated tree`. |
| Gated tree | `af0f005b7f937706780be55123f5770fa2aa0b75` · clean — commit `af0f005` (feature: full-screen task editor …); gate re-run on it 2026-09-30 with the rev97 canon export: 0 project-side BLOCKs, the same 33 environment-only V7/V15/V16 |
| Re-gate rev98 | 2026-10-02 · flow `2026-10-01-rev98` (`c501b7a33cf229aa`, live bundle) over `750b1c8`: exit 0 · **0 block** · 14 notice · 62 n/a · `evidence/validator-regate-rev98.txt`. The 33 environment-only V7/V15/V16 recorded at the close cleared with the rev98 declaration. |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with `devflow-init.py --fold-canon` |

## 1 · What changed

The task editor is a full-screen notes-first editor with a live highlighted preview (23 note
rows at 120×36 and 11 at 80×24, up from 3; title and Save never scroll away), and the kanban
floats open high-priority cards into a `── high ──` band per column (grouped presentation)
while every open card wears a `!!`/`==`/`++` badge in the notes highlight colours.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-005 | v1 | AT-007 | pass |
| HLR-006 | v1 | AT-008 | pass |
| HLR-007 | v1 | AT-009 | pass |
| HLR-001 | v1 | AT-001, AT-005 | pass |
| HLR-002 | v1 | AT-002 | pass |
| HLR-003 | v1 | AT-003, AT-006 | pass |
| HLR-004 | v1 | AT-004 | pass |

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| (candidate, not landed) a painted-cell check must count CELLS, not codepoints | a 2-cell glyph (📅) shifted every x after it; a focus-bar check read the wrong cell | inc 001, `f-due` false failure |
| (candidate, not landed) for Textual widgets, a Rich-escaped markup string is not escaped | `rich.markup.escape` skips `[B]`/`[LINK=`; Textual parses them | security review S1 |

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | command | no | — |
| 2 | artifact | no | — |
| 3 | catalog | no | — |
| 4 | committed and pushed | no | — |

- **New controls:** none — two candidates recorded above for the owner; landing them is a flow change, outside a product batch's commission

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in the staging list of the hand-off report | 📋 ready to commit — the coordinator commits and pushes (owner verdict 2026-09-30); this agent does not | `git status --short` |
| `taskboard/app.py`, `tests/test_focus.py` | adopted into this batch as increment 005 (owner verdict) | increment-005.md |
| `taskboard/views.py` `bar_h` hunk, `tests/test_gantt.py` | adopted into this batch as increment 004 (owner verdict) | increment-004.md |
| `prototypes/city`, `mapper`, `team_sync`, `vista`, `lanes_load` | 📋 FOUND — earlier rounds, kept on disk, excluded LOCALLY in `.git/info/exclude` (not committed, not deleted) | `.git/info/exclude` |
| this round's regenerable captures (`prototypes/edit_modal/out/*.svg|*.png|*.html`, `out/_look/`, `prototypes/kanban_priority/out/*.svg|*.png`) | 📋 excluded LOCALLY in `.git/info/exclude`; regenerable with `proto.py shot` / `look.py` / `build_html.py` | `.git/info/exclude` |
| `.dev-flow/2026-09-01-batch-12/` | V28 NOTICE: superseded holding only `PLAN.md` (+ the archived `decisions-log.json`); its own PLAN and the archived log record it closed at phase 6 "complete" in the pre-station schema, with no 04-validation / 05-close of the rev97 grammar. Not fabricated after the fact — recorded here | `.dev-flow/2026-09-01-batch-12/PLAN.md` |

### Conditional-gate discharge

- **Conditional-gate discharge:** 1 condition(s) · ✅ all discharged (and S1 in TaskDetails, the backlog half, closed by increment 003)

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| security-reviewer BLOCK-UNTIL S1 (editor preview) | ✅ | `taskboard/modals.py` `notes_preview` returns `Text.from_markup(...)`; `tests/test_edit_window.py::test_a_bracket_textual_would_parse_neither_crashes_nor_vanishes` RED before (`evidence/s1-red.txt`), GREEN after; M12 KILLED |

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| edit window crowded (field report) | shipped (uncommitted) | increment-001 |
| kanban priority cue (field report) | shipped (uncommitted) | increment-002 |
| legend ghosts, `++` green, badges outside kanban, ProjectModal, 80-col titles, S1 in TaskDetails, S2 | carried | `.dev-flow/BACKLOG.md` §Open — after `2026-09-30-batch-01` |
| header refresh | not done — base ref moves only when the owner commits | — |

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-09-30-batch-01
mode: core
verdict: pass
increments: 5
source_files_max: 2
notices_raised: 3            # V7 bundle hash, Layer-0 by-AT (inc 001), captures predate S1 fix
rework_returns: 2            # S1 back into increment 001; owner verdict reopened the batch (inc 003-005)
triggers_fired: "B1,B4,C,D,F"
tests_base_to_post: "1336 -> 1535"
new_control: none
open_items_next: 9
```

- Not done, declared: evaluation with real users; the owner's own walkthrough is pending.

## 6 · Human review ledger — what a human audited, at what depth

- **Human review ledger:** none — no human has reviewed this batch yet; it ends at the owner's gate (working tree + captures)
- **Human perimeter:** the owner (Javier) — reviews the after-captures in `prototypes/edit_modal/out/after/`, the diff of `taskboard/modals.py`, `taskboard/taskboard.tcss`, `taskboard/views.py`, and the four changed tests; then commits

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| everything in this batch | sub-agent reviews + suite 1506 passed | ❌ | `none` | — the owner has not reviewed yet; this batch ends at his gate |

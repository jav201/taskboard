# Close — taskboard — Batch 2026-10-07-batch-04 (Batch E: the presentation behind R)

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` · exit 0 · 0 block · 41 notice · 2026-10-07 |
| Gated tree | `34bab3c` + the batch's working copy — dirty: `taskboard/{views,app,keymap}.py`, `README.md`, `REQUIREMENTS.md` (the fold-canon), `tests/{test_present,present_board,test_report,test_keymap,test_markup_sites,test_markup_census}.py`, `.dev-flow/state.json`, `.gitattributes`, `.dev-flow/rollover_batche.py`, `.dev-flow/2026-10-07-batch-04/**`; the prototype round's dirs (`prototypes/kg_mejoras/`, `prototypes/present_e/`) stay on disk uncommitted — `.git/info/exclude`, house rule, with committed copies of the oracle frames and the verdict under `evidence/` |
| Requirements canon | `.dev-flow/BACKLOG.md` + the batch's `01-requirements.md` (the ids: US-1001, HLR-1001, LLR-1001.1, LLR-1001.2) |

## Objective outcome

**`R` presents the project.** The presentation (PRES-C per the operator's verdict) ships behind
`R`: the gantt field on top, the brief blocks below, the `⟦━⟧` cursor expanding each task's notes,
`x` exporting SVG + PNG to the board's `reports/`, `esc` leaving — byte-faithful to the PRES-C
oracle at 118×30 and 80×24, read-only throughout. The report key is replaced; the shell
`--report` CLI is untouched.

## Numbers

- Suite at close: **2534 passed, 0 failed** (`evidence/close-gate.txt`; `2534 = 2529 − 0 + 5`).
- Tests added: 5 (`tests/test_present.py`) + the frozen oracle board fixture. Source: 3 files
  (`views.py`, `app.py`, `keymap.py`) + the README.
- The contract: 1 LED entry (LED-2026-10-07-batch-04.1), 1 HLR, 2 LLRs, 1 AT + 4 TCs.
- Mutation battery: 6 mutations, 6 KILLED (`evidence/inc001c-run.log`).

## What changed

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1001 | v1 | AT-1001 | ✓ |
| LLR-1001.1 | v1 | TC-1001, TC-1002, TC-1003, TC-1004 | ✓ |
| LLR-1001.2 | v1 | AT-1001 + the rewritten census seats | ✓ |

## New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| `_strip` measures through rich's parse (`emoji=False`) | a user-typed bracket or shortcode silently resizing every row the regex miscounted (129 in a 118 frame, with the old assert agreeing) | TC-1003 (the hostile payload) + mutation M6 as its standing RED |
| the frozen-calendar + marked-board fixture seams (migrations marks, the renumber key, `pb.TODAY`) | app-level ATs rotting under startup writes (the link migration rewriting `depends_on`, the done-sweep archiving, the one-time notice saving) | AT-1001's three debugging rounds, folded into `tests/present_board.py` |
| the oracle pin as a shipped test (`tests/test_present.py` + `evidence/frames/`) | a byte contract validated only ad hoc — pinning nothing on the tree | coordinator review N1 |

## Conditional-gate discharge

None — no conditional gate was pending on this batch.

## Human perimeter

The operator's verdict (`taskboard-veredicto-present.json`: PRES-C, SVG+PNG, `R` replaces the
report) was the commissioning input at batch open; everything after ran autonomously under the
standing commission ("Arranca y continua hasta terminar los cambios propuestos para el
proyecto… HAz ambas, paraleliza"). The coordinator committed nothing without the batch close;
no other human touch point exists in this batch.

## Human review ledger

| Artifact | Human review |
|---|---|
| The commission ("Arranca y continua…", "HAz ambas, paraleliza", "Sigue usando Deepseek") | ✅ the operator's own words |
| The prototype verdict (PRES-C over A/B; SVG+PNG; `R` replaces the report) | ✅ 2026-10-07 — accepted as the batch's contract |
| The code | ❌ machine review only (DeepSeek V4 Pro ×2 runs + the coordinator's review: the oracle pin fold, the `_strip` S1 fold, the 6-mutation battery) |

## How the work was done

DeepSeek V4 Pro implemented the renderer and the screen in two runs (`inc001-run.log`,
`inc001b-run.log`) — the second after OpenCode refused a site-packages read and the PNG recipe
moved inline into the brief. The coordinator then: rewrote the 5 census seats to the present
contract, wrote the oracle pin (`tests/present_board.py` + the frames + `tests/test_present.py`),
fixed the S1 width defect at `_strip`, and ran the mutation battery. The parallel cleanup batch
landed on main in the same window; the two merge by union at `views.py`.

## Lessons carried

- A byte contract without a shipped test pins nothing. The prototype round proved identity
  once; only `TC-1001`/`TC-1002` make it a law of the tree.
- Width measurement must parse exactly like the renderer — same parser, same `emoji=False`.
  A regex "tag stripper" cannot tell a style tag from a bracket the user printed, and an emoji
  substitution inside the measure breaks rows the painters priced as literal text.
- App-level acceptance tests on this app need the house seams: the frozen calendar
  (`app.date` AND `models.date` — the done-sweep reads the latter) and a board marked
  migrated/seen, or startup writes corrupt the fixture under the test.

## Standing constraints honored

No commits/pushes by the implementing agents; the coordinator commits and pushes once per
batch under the operator's commission. Synthetic boards only. The worktree (one lane) merged
back to the trunk by union at the one shared file.

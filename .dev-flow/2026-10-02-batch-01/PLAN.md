# PLAN — taskboard — Batch 2026-10-02-batch-01

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`, flow rev98.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-02-batch-01 |
| Objective | Batch A1 of the kg_mejoras plan: whole-board fitted gantt (G-A) with the AX-2 date ruler, the round-7 colour budget on kanban and gantt, and the README/RUN.md rewrite (K-A + R-1b split to Batch A2 at P0) |
| Standing authorization | the operator's commission, asked at kickoff on 2026-10-02 and relayed by the coordinator (this runtime is a delegated sub-agent and cannot prompt): Gates — "Autónomo, agente Opus": the batch runs end-to-end autonomously, the agent self-approves each station gate and records every un-asked decision; a HIGH finding blocks regardless and returns to the operator. Git — "Commit + push a main, sin PR": commit and push to `origin/main` are authorized for the coordinator only; this agent does not commit, push, stash, reset or checkout and leaves every change in the working tree. `merge: false (no PR; coordinator commits+pushes to main)`. Language — "Inglés". Standing request 2026-09-30: "en el siguiente commit, actualiza el README del repo, está muy desactualizado y tiene errores y problemas estéticos." Split A1/A2 pre-authorized by the commission. |

## Where we are

P5 closed. P4 approved (qa PASS-WITH-NOTES iteration 3, 30/30, gate 1611 passed on the frozen
tree). Close: canon folded (30 rows), privacy sweeps recorded (`evidence/privacy-sweep-close.txt`),
`05-close.md` written. Every change stays in the working tree for the coordinator's commit.

## Objective

Gantt → G-A (fitted whole board, folding, compact chip, dependency gutter) + AX-2 (two-row
ruler, selection echo, no-drop law); colour budget on kanban + gantt; README + RUN.md.

## RC-1 and flow currency

- RC-1: `git fetch origin` → `origin/main` = `57a60756fda9` = HEAD = merge-base. `base_ref` stamped from it.
- Flow: rev98 bundle `<home>\.claude\skills\dev-flow`; validator at P0 after the rollover: **0 block · 35 notice · 45 n/a**, `V7` silent (bundle hashes match).
- Inherited NOTICEs declared (kickoff run at `57a6075`: 0 block, 15 notice): `V9` ×8 legacy packets without a SOURCE count; `V22` 5 legacy US ids not in the canon; `V23` an unparseable design-review citation in a legacy packet (batch-12 era); `V27`/`V28` (batch-12 superseded unclosed — its record is the old schema, not back-filled); `V30` bundle subset (benign on this runtime); `V53` closed-record census; `V57` the batch-01 record predates the tree by 2 commits (re-gate commits). The other P0 NOTICEs are this batch's own seeded placeholders, filled as stations run.
- Not runnable here (`SKILL.md` step 4): `V15`, `V16`, `V17` — `not-run` (no canon tree, no checkout table, no hook settings on a bundle runtime).
- Reviewer roles: spawned as named sub-agents of this runtime (`qa-reviewer`, `ux-reviewer`, `code-reviewer`, `security-reviewer`, `tester` where owed), each given its `agents/<role>.md` brief — independent reviewers, never inline self-review.

## Triggers (evaluated 2026-10-02, P0)

| id | Verdict | Probe / evidence |
|---|---|---|
| B1 | fired | `grep -l "render_gantt\|gantt_\|\"gantt\"" tests/*.py` → 15 files; kanban title/`card_cell`/`reldue_token` asserted in 6+ files → reverse census per increment |
| B2 | not fired | no file moves planned (new files only: `tests/kg_board.py`, `tests/test_gantt_board.py`, `tests/test_colour_budget.py`, `tests/test_readme.py`) |
| B3 | not fired | `ls tests/goldens` → no such directory; no byte-identical golden in the repo |
| B4 | fired | `render_gantt`'s `line_map` is consumed by `app._scroll_selected_into_view`; `nav_model("gantt")` by `app._nav_columns` → AT-102 drives the app |
| A | not fired | one source module (`taskboard/views.py`), no new module, no boundary move (judged; `docs/ARCHITECTURE.md` does not exist in this repo — declared) |
| C | fired | `devflow-scan-spec.py` → `security_required: true` (flags `token`, `role`, `form`); C-17 new seats for board text; README privacy → security-reviewer on the doc diff |
| D | fired | user-visible gantt/kanban → ux-reviewer at P2/P4 + captures 118×30 / 80×24 |
| E | fired | 4 in-scope stories, 4 planned increments |
| F | fired (F2) | `BACKLOG.md` header says `Last refresh: 2026-09-01` while `2026-09-30-batch-01` closed after it → reconciled at this close; F1 (flow hash) not fired: `V7` clean |

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | done | rollover; US-101..104 READY, US-105 OUT (A2) |
| P1 requirements | done | 9 HLR, 18 LLR, AT-101..107; scan run |
| P2 two-lens review (+ security) | done | 2 iterations; `02-review.md` |
| P3 increment 001 — gantt G-A + AX-2 (+ gantt-side budget, selection seat) | done | `views.py`, `app.py`, `modals.py`; code-reviewer 3 rounds (2 HIGH folded); 18/18 mutants killed; 1588 passed |
| P3 increment 002 — kanban colour budget | done | `views.py`; code-reviewer 2 rounds (1 HIGH folded); 6/6 mutants killed; 1606 passed |
| P3 increment 003 — README + RUN.md | done | docs only (0 SOURCE); qa 2 rounds, security PASS-WITH-NOTES |
| P4 validation, iteration 1 | iterate-to-fix | ux UXV-1 FAIL; qa G-001 (C-18) |
| P3 increment 004 — P4 walkthrough fixes | done | `views.py`; code-reviewer 3 rounds OK; 5/5 mutants killed; 1611 passed |
| P4 validation, iteration 2 | done | gate 1611 passed; qa PASS-WITH-NOTES |
| P5 close | done | `05-close.md`; canon fold 30; privacy sweep 0 board strings |

## Roadmap + increment plan

Re-cut at the P2 gate (C-21: the AT set changed): one gantt increment avoids building a
bottom axis only to remove it.
1. Increment 001 — the gantt: G-A + AX-2 + its budget marks (title, chain) + `_select_first` (HLR-101..107, LLR-101.1..11, LLR-102.1..5, LLR-103.2; AT-101..105, 108, 109). SOURCE: `views.py`, `app.py`. Tests: `tests/test_gantt_board.py` + the §6.6 census.
2. Increment 002 — the kanban's colour budget + the colour census over both views (HLR-108; LLR-103.1, 103.3; AT-106). SOURCE: `views.py`.
3. Increment 003 — README.md + RUN.md (HLR-109; AT-107), security-reviewer privacy pass. SOURCE: 0.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-02 | Split: this batch = A1 (gantt G-A + AX-2, budget on kanban/gantt, README/RUN.md); K-A + R-1b → Batch A2 (BACKLOG) | pre-authorized; 14–15 test files per renderer, kanban rewritten one batch ago, plan §Risks (US-105) |
| 2026-10-02 | Ids in a disjoint `1xx` range | `HLR-001..012`, `AT-001..028` already used in the record/canon |
| 2026-10-02 | D2 rest work folds to `✓n`, not navigable | G-A verdict "done folds to ✓n"; F-3 |
| 2026-10-02 | D3 keep flow packet + pulse | shipped motion; verdict silent → conservative |
| 2026-10-02 | D4 today keeps the accent | budget names no today role; AX-2 frames light today in accent — for the operator |
| 2026-10-02 | D5 no weekend shading | not in the commission's AX-2 list; off-palette background — BACKLOG |
| 2026-10-02 | D6–D9 Inbox group, focus kept, `+N not shown` only when spans overflow, selected-group window | `01-requirements.md` §6.2 |
| 2026-10-02 | D10 budget scope = kanban + gantt (+ the two shared card helpers) | app-wide is a 9-view + keybar palette pass — BACKLOG |
| 2026-10-02 | D11 "This week" → `soon`; D12 view text follows the frames (English), help prose stays Spanish | §6.2 |
| 2026-10-02 | P2 folds: D7 keeps `(focused: …)`; D11 → `hd`; neighbour-rule selection repair (UX-15); page-aligned paging; operator questions D4, D9, D10, D12, D13, D14 carried with conservative defaults | `02-review.md` |
| 2026-10-02 | Evidence transcripts redact the personal path | the README fix must not re-leak through the record |

## Risks / watch-items

- Gantt laws written for the 2-day axis (span economy, spend census, vertical fill, motion, legend) — triaged per failure: superseded → rewritten and listed; not superseded → must stay green.
- `k = 0.5` cannot reach `daily` cadence (2 cells/day).
- Many-project boards at 80×24 can still overflow with span rows alone (D8).

## Conventions honored

- Test docstrings in the house style (field report · law · RED), AT/TC ids in docstrings.
- No new dependency; all view code in `taskboard/views.py`; Textual 8.2.8 / rich 15.0.0 pins.
- Prototype code re-derived, not pasted.

## Out-of-scope carries

- Batch A2 (K-A + R-1b + cap), app-wide colour budget, weekend shading — `.dev-flow/BACKLOG.md` at close.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider` (base `57a6075`) | 2026-10-02 | 1535 passed in 131.49 s (`evidence/base-suite.txt`) |
| same, `--ignore=tests/test_colour_budget.py` (after increment 001) | 2026-10-02 | 1588 passed in 167.75 s (`evidence/inc001-green.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.

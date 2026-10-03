# PLAN — taskboard — Batch 2026-10-02-batch-03

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`, flow rev98 (pinned).

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-02-batch-03 |
| Objective | Batch A2: the readable kanban — two-row cards, one project band rule across the columns, `┈` separators, a DONE rail, adaptive column widths, one board-wide high band on top (R-1b) capped with "+N more" |
| Flow pin | **rev98, pinned** — operator ruling at this batch's kickoff, 2026-10-02, verbatim: "Sí, fijar a rev98". The declared rev98 bundle (skills commit `48154ab`, "flow rev98 — the bundle regenerated over closefix 6") is extracted read-only to the session scratchpad (`devflow-rev98-48154ab/dev-flow`); the validator runs from that directory as bundle root and the flow's rules are read there. Reason: rev99 is in progress in `~/.claude/skills` and its `SKILL.md` fails `V7` there (rev99-wip, not declared), as it did for `2026-10-02-batch-02`. `~/.claude` is never edited. |
| Standing authorization | the operator's commission, asked at this batch's kickoff on 2026-10-02 and relayed by the coordinator (this runtime is a delegated sub-agent and cannot prompt), dated 2026-10-02: Gates — "Autónomo, agente Opus": end-to-end autonomous; the agent self-approves each station gate and records every un-asked decision (this plan's decision log, `state.json` `decisions_log`, the close record); a HIGH finding blocks regardless — stop and report back. Git — "Commit + push a main tras tu veredicto visual": the COORDINATOR commits and pushes after the operator's visual verdict; this agent does not commit, push, stash, reset or checkout anything and leaves all changes in the working tree. `merge: false (no PR; coordinator commits+pushes to main after the operator's visual verdict)`. Visual details the verdicts do not settle take the most conservative reversible reading and are listed as provisional visual decisions for the operator. |

## Where we are

**P5 closed.** P0–P4 approved under the standing authorization (P2 and P4 at iteration 2); three increments; suite 1677 → 1855; the close record is `05-close.md`. The coordinator commits after the operator's visual verdict.

## Objective

The kanban (key `4`, grouped) reads: titles across the column on two-row cards, each project
named once, finished work on a narrow rail, the urgent cards first in one capped band.

## RC-1 and flow currency

- RC-1: `git fetch origin` → `origin/main` = `13745f6f268f` = HEAD = merge-base. `base_ref` stamped from it.
- Rollover from `2026-10-02-batch-02` (P5 closed): its `decisions_log` MOVED to `.dev-flow/2026-10-02-batch-02/decisions-log.json`; every single-slot field retired per `stations/shared-batch.md` §Batch rollover (triggers re-evaluated below, artifacts cleared, homes re-pointed, owner re-stamped, authorization re-recorded from this batch's commission, `base_ref` = HEAD, `created_at` re-stamped); `mode_history` carried and appended. Seeds from the pinned bundle's `devflow-init.py` run in a scratch tree (it refuses an initialised `.dev-flow/`), batch id substituted. The increment skeleton is held back until P3 so no packet precedes its increment.
- Flow: rev98, the PINNED snapshot of skills commit `48154ab` (header row "Flow pin"). Validator at kickoff (coordinator, `13745f6`): **0 block · 18 notice**, exit 0 — re-run by this agent before the rollover: same (V7 clean).
- **Inherited NOTICEs declared** (all 18 predate this batch): `V9` ×8 legacy packets (`increment-001..003`, `006..010` in the flat `.dev-flow/03-increments/`) declare no SOURCE count, and ×1 batch-02's `increment-002.md` 4-source warning; `V13` ×2 batch-01's IFC address `nav-order` reached by undeclared files, and its computed `task-rows` addresses; `V22` ×3 batch-01 and batch-02 LLRs never used as an IFC owner, and 5 legacy US ids not in the canon; `V23` an unparseable design-review citation in legacy `increment-006.md`; `V30` the bundle derives its floors from a subset (benign on this runtime, `SKILL.md`); `V53` the closed-record census count; `V57` batch-02's close record predates this tree by 1 commit (the coordinator's commit). None is this batch's to fix; a closed record is not re-anchored.
- Not runnable here (`SKILL.md` step 4): `V15`, `V16`, `V17` — `not-run` (no canon tree, no checkout table, no hook settings on a bundle runtime).
- Mechanisms unavailable on this runtime, named once (`SKILL.md` step 5): no slash commands, no hooks, no prompt guard, no operator prompt (the standing authorization above closes the gates). Reviewer roles are **spawned as named sub-agents** of this runtime (`qa-reviewer`, `ux-reviewer`, `code-reviewer`, `security-reviewer`, `tester` where owed), each told to follow the pinned bundle's `agents/<role>.md` — independent reviewers, never inline self-review.

## Triggers (evaluated 2026-10-02, P0)

| id | Verdict | Probe / evidence |
|---|---|---|
| B1 | fired | `grep -l` over `tests/` for the touched symbols: `render_kanban`/`kanban_order`/`nav_model("kanban"` → test_app, test_kanban_priority, test_dependencies; `card_cell` → test_app, test_archive, test_cells, test_colour_budget, test_dependencies, test_kanban_priority, test_palette_ration; `── high` → test_kanban_priority; `"kanban"` → 18 files → reverse census measured per increment |
| B2 | not fired | no file moves; one new file (`tests/test_kanban_readable.py`) |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | `line_map` → `app._scroll_selected_into_view`; `nav_model` → `app._nav_columns` → AT through the app keys |
| A | not fired (judged) | no `docs/ARCHITECTURE.md`; `views.py` only, as batches 01/02 ruled (D-310) |
| C | fired | `devflow-scan-spec.py` → `security_required: true` (flags `token`, `form`, vocabulary); file-derived project names and split titles are printed as markup (C-17) → hostile-input arms; security-reviewer at P2 |
| D | fired | user-visible → ux-reviewer at P2/P4, captures 118×30 / 80×24 |
| E | fired | 3 stories, 2 planned increments, the most-tested renderer replaced |
| F | F2 fired | `BACKLOG.md` header base ref `a0e7d9a` ≠ HEAD `13745f6` → reconciled at close; F1 not fired: `V7` clean on the pinned bundle |

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | done | rollover; US-301..303 READY; commission item 9 is decision D-301 |
| P1 requirements | done | 8 HLR, 8 LLR, AT-301..306; scan run |
| P2 review, iteration 1 | iterate-to-refine | qa FAIL (Q-1, Q-2 blockers), ux and security PASS-WITH-NOTES; all folded (LED .9–.13) |
| P1 refine | done | HLR-309, HLR-310, LLR-301.3, 309.1, 310.1, AT-307, AT-308; metric re-derived |
| P2 review, iteration 2 | approved | qa FAIL (N-1), ux FAIL (UX-15) → folded; discharge re-read DISCHARGED 12/12 |
| P3 increment 001 | done | `views.py`; code-reviewer 2 rounds (F1 HIGH folded); 28/28 mutants killed; 1821 passed |
| P3 increment 002 | done | `app.py`, `views.py`; code-reviewer 2 rounds (F1 HIGH folded); security PASS-WITH-NOTES; 15/15 mutants killed; 1845 passed |
| P4 validation, iteration 1 | iterate-to-refine + iterate-to-fix | gate 1845 passed; qa PASS-WITH-NOTES (G-001, G-003a, G-004); ux FAIL (UXV3-1 blocker) |
| P3 increment 003 | done | `views.py`; code-reviewer 3 rounds (F1, F2 HIGH folded); 12/12 mutants killed; 1854 passed + clipboard flake |
| P4 validation, iteration 2 | approved | gate 1855 passed (`evidence/p4-gate3.txt`); qa PASS-WITH-NOTES (G-009..G-012 folded); ux re-walk PASS-WITH-NOTES (UXV3-1 fixed; UXV3-12..15 notices) |
| P5 close | closed | canon folded (22 rows; HLR-003, LLR-003.2 superseded); BACKLOG reconciled (+20); sweep 0 new hits; validator 0 block · 19 notice (`evidence/validator-close.txt`) |

## Roadmap + increment plan

Re-cut after P2 iteration 1 (C-21: AT-307, AT-308 added; AT-303 re-defined):

1. Increment 001 — the readable board: plan seat, chrome, two-row cards, separators, adaptive widths, band rules, the rail, the high band (uncapped), band windowing and the fold row, nav; colour budget (HLR-301..305, 307, 309; LLR-301.1, 301.2, 301.3, 302.1, 303.1, 304.1, 305.1, 309.1; AT-301, 302, 303, 305, 307). SOURCE: `views.py`.
2. Increment 002 — the cap, the copy, the cursor off undrawn done work (HLR-306, 308, 310; LLR-306.1, 308.1, 310.1; AT-304, 306, 308; D-312). SOURCE: `views.py`, `app.py`.
3. Increment 003 (P4 iterate-to-fix) — a band taller than the room is cut (HLR-309 amended, LLR-309.2; AT-307 re-parametrised, TC-311); the title-seat regression nodes (G-003a); the G-004 rewrites; the widths transcript (G-001). SOURCE: `views.py`.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-02 | Ids in a disjoint `3xx` range | `0xx`/`1xx`/`2xx` taken in the record and canon |
| 2026-10-02 | Flow pinned to rev98 (operator: "Sí, fijar a rev98"; bundle = skills `48154ab`, read-only snapshot) | `~/.claude/skills/dev-flow` is rev99-wip; its `SKILL.md` fails `V7` |
| 2026-10-02 | D-301 replace the grouped body (not coexist); `tab` unchanged | `01-requirements.md` §6.2 |
| 2026-10-02 | D-302..D-310 (scroll kept, cap half the body, rail recent-first, narrow rail not selectable, `▊` spine, first-word tag, age sheds, other group modes as band rules, A not fired) | `01-requirements.md` §6.2 |
| 2026-10-02 | P2 iteration 1 → iterate-to-refine; folds LED .9–.13; D-302 windowing per the frame; D-311..D-313 | `02-review.md` |
| 2026-10-02 | P2 iteration 2: cap two thirds (D-303), stable window + two-sided fold row (D-314), neighbour after `]`; P2 approved | `02-review.md` §Iteration 2 |
| 2026-10-02 | LLR-302.1 amended at P3 (LED .17): the frames' proportional widths | the floor-first split read 5.3 < 5.5 at 80×24 |
| 2026-10-02 | Increment 001 approved (code review round 2 OK; F2/F11/F13 to 002) | `03-increments/increment-001.md` |
| 2026-10-02 | Increment 002 approved (code review round 2 OK; security PASS-WITH-NOTES) | `03-increments/increment-002.md` |
| 2026-10-02 | P4 iteration 1 → iterate-to-refine HLR-309 (LED .18) + iterate-to-fix increment 003; D-314b the cut (PV-9), D-315 `at risk` unreachable + the head row (PV-10) | `04-validation.md`, `evidence/p4-ux-walkthrough.txt` |
| 2026-10-02 | P4 iteration 2 → approved (autonomous): qa + ux PASS-WITH-NOTES, G-006/009/010/011/012 discharged, G-002 deferred; UXV3-12..15 and PV-9 routed to the operator | `04-validation.md` §Orchestrator fold, `evidence/p4-ux-rewalk.txt` |
| 2026-10-02 | P5 closed (autonomous); LLR-306.1's statement given its `shall` for the canon fold (no change of meaning); V26 contract size declared, not trimmed at close | `05-close.md` |
| 2026-10-02 | Evidence transcripts redact the home path (`<home>`, `evidence/redact.py`) | the record must not leak it |

## Provisional visual decisions (for the operator, with the captures to compare)

| Id | Decision | Captures (before → after) |
|---|---|---|
| PV-1 | whole bands windowed with the fold row as in the frame, but no selected-card detail line when nothing is folded (D-302) | `evidence/captures/` base-kanban-118x30 → close-kanban-118x30; base-kanban-80x24 → close-kanban-80x24 (`.svg` + `.txt`) |
| PV-2 | the cap: two thirds of the body, `+N more ↓`, overflow drawn in the project band (D-303) | `evidence/captures/` base-kanban-14high-118x30 → close-kanban-14high-118x30; base-kanban-14high-80x24 → close-kanban-14high-80x24 (`.svg` + `.txt`) |
| PV-3 | below 100 cells the rail is a count, done tasks not selectable there (D-305) | `evidence/captures/` base-kanban-80x24 → close-kanban-80x24 (count rail); close-kanban-118x30 (titled rail at ≥ 100) (`.svg` + `.txt`) |
| PV-4 | the shipped `▊`/`▲` spine, not the age-thickness ramp (D-306) | `evidence/captures/` base-kanban-118x30 → close-kanban-118x30 (`.svg` + `.txt`) |
| PV-5 | the high card's project tag is the name's first word, more words only when two projects share it (D-307) | `evidence/captures/` base-kanban-14high-80x24 → close-kanban-14high-80x24 (`.svg` + `.txt`) |
| PV-6 | the age token kept at every width, shed first (the frame dropped it below 100 cells) (D-308) | `evidence/captures/` base-kanban-80x24 → close-kanban-80x24 (`.svg` + `.txt`) |
| PV-7 | `g` → priority / horizon draw band rules too (no frame seen) (D-309) | `evidence/captures/` base-kanban-priority-118x30 → close-kanban-priority-118x30; base-kanban-horizon-80x24 → close-kanban-horizon-80x24 (`.svg` + `.txt`) |
| PV-8 | `]` into a count rail: the cursor takes the card that took its place and a notification says where the task went (D-305, D-314, HLR-310) | `evidence/captures/` no static capture (a key sequence): AT-308 / TC-312 and `evidence/p4-ux-walkthrough.txt`; board before the move: close-kanban-80x24 (`.svg` + `.txt`) |
| PV-9 | a band taller than the room is cut around the selection; the fold row counts `▲ k more in NAME` / `▼ m more in NAME` (D-314b, P4 UXV3-1) | `evidence/captures/` base-kanban-14high-80x24 → close-kanban-14high-80x24 (`▼ … more in NAME`); walk in `evidence/p4-ux-rewalk.txt` (`.svg` + `.txt`) |
| PV-10 | the head row stays the shipped chrome (`KANBAN · grouped … N tasks`), not the frame's `KANBAN · high on top … over WIP: …` (D-315, P4 UXV3-7) | `evidence/captures/` base-app-kanban-118x30 → close-app-kanban-118x30; base-app-kanban-80x24 → close-app-kanban-80x24 (`.svg` + `.txt`) |

## Risks / watch-items

- The grouped kanban is pinned by many nodes (B1): `test_kanban_priority.py` encodes HLR-003's per-column band — superseded here, rewritten with reasons.
- A band taller than the room is cut around the selection, so the panel no longer scrolls (§6.3, D-314b); below a room of 3 rows the band is drawn alone and scrolls (declared).
- Readability thresholds come from the prototype measured over this tree (P-6); re-measured at P3.

## Conventions honored

- Test docstrings in the house style (field report · law · RED), AT/TC ids in docstrings.
- No new dependency; Textual 8.2.8 / rich 15.0.0 pins; prototype code re-derived, not pasted.

## Out-of-scope carries

- Everything else in `BACKLOG.md` (Batch S, B, C, D; the help right-column layout; `_strip` F5; screenshots; S-8; the legend ghosts under matrix/focus).

## Security scan

`python <flow>/scripts/devflow-scan-spec.py .dev-flow/2026-10-02-batch-03/01-requirements.md` →
`security_required: true`, flags `token`, `form` (controls 5/5 ok); answered in
`01-requirements.md` §6.4 (`evidence/p1-security-scan.txt`).

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider` (base `13745f6`) | 2026-10-02 | 1677 passed in 237.82 s (`evidence/base-suite.txt`) |
| same, after increment 001 | 2026-10-02 | 1821 passed in 306.79 s (`evidence/inc001-green.txt`) |
| same, after increment 002 | 2026-10-02 | 1845 passed in 357.16 s (`evidence/inc002-green.txt`) |
| P4 gate run, iteration 1 | 2026-10-02 | 1845 passed in 306.00 s (`evidence/p4-gate.txt`) |
| P4 gate run, iteration 2 | 2026-10-02 | 1855 passed in 311.59 s (`evidence/p4-gate3.txt`; `p4-gate2.txt` had the clipboard environment failure, G-011) |
| same, after increment 003 | 2026-10-02 | 1854 passed, 1 failed (clipboard environment) in 325.57 s (`evidence/inc003-green.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.

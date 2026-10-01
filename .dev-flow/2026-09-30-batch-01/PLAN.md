# PLAN — taskboard — Batch 2026-09-30-batch-01

> Living plan (flow `templates/plan-template.md`). Mode `core`, language `en`.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-09-30-batch-01 |
| Objective | Edit window variant C (full-screen editor + live preview) and kanban K4 high band + priority badges, per owner verdict 2026-09-30 |
| Standing authorization | the commission (runtime cannot prompt — a delegated sub-agent), extended by the owner's verdict of 2026-09-30 relayed by the coordinator ("include the Focus Board fix and my gantt-filter fix … fix the TaskDetails S1 … APPROVES the priority colors … the batch must close with ZERO project-side blocks and be committed and pushed. Do NOT commit or push yourself"): "Implement two design decisions in the taskboard Textual app … following the `dev-flow` skill … Javier (the owner) gave the design verdict after a prototype round; you implement exactly that, nothing more. … DO NOT commit, push, stash, reset or checkout anything. Leave everything as working-tree changes. … If scope creeps beyond that or a decision above turns out contradictory/impossible, STOP and report rather than improvising." Read as: autonomy over the gates it commissions (P0–P5); merge NOT granted, and not even a commit (stated). |

## Where we are

Owner verdict 2026-09-30 reopened the batch: increments 003 (S1 in TaskDetails), 004 (adopted
gantt-filter fix) and 005 (adopted Focus Board fix) added; green-vs-project colour accepted
(LED .5). Close record ready; the coordinator commits, re-runs the gate, records the HEAD and
pushes. This agent does not commit.

## Objective

Fold Javier's 2026-09-30 verdict into the shipped app: `TaskModal` → variant C; kanban →
K4 band + K3-style badges reusing `!!`/`==`/`++`.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| P0 intake | done | rollover from `2026-09-01-batch-12` (decisions_log archived to its `decisions-log.json`); batch seeded with the flow's init script in a scratch root and copied in (the script refuses an initialised `.dev-flow/`) |
| P1 requirements | done | 3 stories, 4 HLR, 9 LLR, 6 AT |
| P2 two-lens review | done | qa-reviewer + ux-reviewer, 24 findings folded / declared (`02-review.md`) |
| P3 increment 001 (US-001) | done | 2 source files; 33 nodes; code-reviewer PASS-WITH-NOTES |
| P3 increment 002 (US-002, US-003) | done | 1 source file; 133 nodes; code-reviewer PASS-WITH-NOTES |
| P4 validation | done | `04-validation.md` |
| P3 increment 003 (US-004) | done | S1 in TaskDetails/ImageViewer/image_block; code-reviewer PASS-WITH-NOTES |
| P3 increment 004 (US-005) | done (adopted) | operator's gantt-filter fix; RED re-captured |
| P3 increment 005 (US-006) | done (adopted) | Focus Board fix; RED re-captured |
| P5 close | ready for the coordinator's commit | `05-close.md` |

## Roadmap + increment plan

1. Increment 001 — editor (modals.py, taskboard.tcss).
2. Increment 002 — kanban (views.py).

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-09-30 | Proceed despite the validator's `V7` BLOCK on the flow bundle's own `SKILL.md` hash | the installed flow is the operator's in-progress `rev98-wip` branch (SKILL.md committed today, manifest not re-hashed); repairing it means re-pulling over his WIP, which is not this batch's to do. Every other file hashed clean. Declared, not hidden. |
| 2026-09-30 | Band only in the grouped presentation, not with group=priority; badges in grouped + lanes, not matrix | D1/D2 in `01-requirements.md` §6.2 |
| 2026-09-30 | Archived = not open (no badge, no band) | archived is terminal (`status_glyph`) |
| 2026-09-30 | Focus rail / People keep `!` | commission names the kanban only (D4) |
| 2026-09-30 | `TASK_CHIPS_ONE_ROW = 122` (measured); 120×36 folds the chips | 121 clips `f-pinned` (mutation M5) |
| 2026-09-30 | Calendar buttons 5 cells wide | Textual pads a Button label; a 📅 in a 3-wide button painted 2 cells past its region |
| 2026-09-30 | `++` keeps `green` despite being a project hue | owner accepted explicitly (LED .5) |
| 2026-09-30 | Older prototype rounds and this round's regenerable captures excluded in `.git/info/exclude` (local), never deleted | owner verdict: commit only this round's sources + NOTES + after-captures (≈650 KB) |
| 2026-09-30 | batch-12 V28 recorded, not back-filled | its record is a PLAN + archived log in the old schema; fabricating a close is refused |
| 2026-09-30 | Four existing tests changed | listed in `increment-002.md` §6 — each because the owner's decision changes its expectation |

## Risks / watch-items

- 80-column kanban titles: −3 chars per normal/low card, −1 per high.
- Legend presentation/focus-blindness (inherited) → BACKLOG.
- Tests read Textual's private compositor (8.2.8).

## Conventions honored

- Test docstrings in the house style (field report · law · RED).
- No new dependency; CSS in `taskboard.tcss` (app CSS outranks DEFAULT_CSS).
- Foreign uncommitted edits (`app.py`, `tests/test_focus.py`, `views.py` bar_h, `tests/test_gantt.py`) untouched.

## Out-of-scope carries

- ProjectModal layout; matrix/focus legend ghosts; badges outside the kanban — `.dev-flow/BACKLOG.md`.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest -q` (base, operator figure) | before 2026-09-30 | 1336 passed |
| `python -m pytest -q` (after) | 2026-09-30 | 1535 passed in 213.66 s (`evidence/full-suite-after.txt`) |

## Decision log

Mirrors `state.json` `decisions_log`.

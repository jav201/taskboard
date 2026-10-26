# Increment 001 — HLR-3001..3005 · «done work keeps its gantt row» (AUDITED, shipped as f4b53cc)

| Field | Value |
|---|---|
| Batch | `2026-10-26-batch-01` |
| Increment | `001` (retroactive — the increment shipped as commit `f4b53cc` on 2026-10-26 before this audit batch opened, at the operator's order; this packet records it) |
| Lane | none — one lane |
| Requirement(s) | `US-3001` / `HLR-3001..3005` / `LLR-3001.1-.3, 3002.1-.3, 3004.1-.2, 3005.1-.2` |
| Acceptance | AT-3001..AT-3006 (see 01-requirements.md) |
| Agent | `software-dev` (executed 2026-10-26, pre-flow, by order of the operator; audited by the four P2 lenses) |
| Date | `2026-10-26` |

## 1 · What changed

`gantt_plan` gains `done_rows: bool = False`; when set (board gantt only: `render_gantt`,
`nav_model` gantt mode, the gantt legend) a group's drawn rows are its open rows + reached
milestones by due (D-606, unchanged), then its DONE, not-archived, non-milestone tasks sorted
by due at the tail. Done rows paint quiet: `_gantt_done_bar` (reached tone, no flow packet, no
over/crit, edge-clipped), dimmed title, `✓` chip. Folding/pressure/window unchanged (G3);
presentation byte-identical (G4, default-off flag); nothing else changes (G5).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | HLR-3001, HLR-3002, HLR-3003, HLR-3004, HLR-3005 | `done_rows` flag + `done_tail`, `_gantt_done_bar`, painter done branch, three setters |
| `taskboard/app.py` | source | HLR-3005 | F-3 guard + `_notify_folded` docstring/seat comments |
| `tests/test_gantt.py` | test | HLR-3001, HLR-3002 | AT-3001, AT-3002 — G-A restated + new why-tests |
| `tests/test_gantt_board.py` | test | HLR-3001, HLR-3004, HLR-3005 | AT-3003, AT-3004, AT-3006 — nav rows, flag boundary, AT-113 restated |
| `tests/test_archive.py` | test | HLR-3001 | AT-3005 — order/visibility arms restated |
| `tests/test_gantt_polish.py` | test | HLR-3002, HLR-3005 | AT-206/AT-207/TC-208 pins rebaselined with declared rationale |
| `tests/test_colour_budget.py` | test | HLR-3002, HLR-3003 | TC-110/TC-118 rebaselined with declared rationale |
| `tests/test_milestone_marks.py` | test | HLR-3002 | diamond census +1 |
| `.dev-flow/2026-10-20-batch-01/evidence/frames-base.json` | generated | HLR-3004 | 4 gantt frames regenerated (sealed batch's oracle — qa verdict CLEAN) |
| `.dev-flow/2026-10-20-batch-01/evidence/frames_base.py` | generated | HLR-3004 | generator docstring only (+3 lines) |
| `.dev-flow/2026-10-26-batch-01/evidence/scratch-evidence/suite-chunk00.txt` | generated | HLR-3001, HLR-3002, HLR-3003, HLR-3004, HLR-3005 | full-suite chunk 0, 1440 passed (committed with the change as `.scratch-evidence/`, moved here by the audit) |
| `.dev-flow/2026-10-26-batch-01/evidence/scratch-evidence/suite-chunk01.txt` | generated | HLR-3001, HLR-3002, HLR-3003, HLR-3004, HLR-3005 | full-suite chunk 1, 961 passed |
| `.dev-flow/2026-10-26-batch-01/evidence/scratch-evidence/suite-chunk02.txt` | generated | HLR-3001, HLR-3002, HLR-3003, HLR-3004, HLR-3005 | full-suite chunk 2, 879 passed |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 13** |

## 3 · How to test

`env -u NO_COLOR python -m pytest tests/test_gantt.py tests/test_gantt_board.py tests/test_archive.py` (targeted); full suite in 3 sequential chunks (already executed with the change).

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| Targeted (this audit, qa lens) | 123 + 62 | **185 passed, 0 failed** (`evidence/suite-targeted.txt`, `evidence/suite-targeted2.txt`) |
| Full suite (with the change, consumed) | 3280 | **3280 passed, 0 failed** — 1440 + 961 + 879 in 3 sequential chunks (`evidence/scratch-evidence/suite-chunk0{0,1,2}.txt`) = baseline 3278 + 2 new |
| Import probe | — | `taskboard.__file__` = the worktree (`evidence/import-probe.txt`) |

## 4b · Independent review

`code-reviewer — spawned as a generic agent with agents/code-reviewer.md · OK-TO-ADVANCE (0 HIGH; 2 MEDIUM, 3 LOW — in 02-review.md)`; architect lens: seam APPROVE / records iterate (AX-1..AX-5); qa lens: PASS, golden CLEAN (QA-1..QA-4); ux lens: PASS (UX-1, UX-2).

## Evidence files — bytes at a declared home, verbatim, hash-verified

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| full-suite chunk 0 (with the change) | `.dev-flow/2026-10-26-batch-01/evidence/scratch-evidence/suite-chunk00.txt` | `bec1bb8a92efab1e8d68e348324971edfb6b44c1006d966c4e825d7e060f0cdd` |
| full-suite chunk 1 (with the change) | `.dev-flow/2026-10-26-batch-01/evidence/scratch-evidence/suite-chunk01.txt` | `137d238d60fd86516c75197304fcddd8c5fa28a26eb855502ada658520fb8cf9` |
| full-suite chunk 2 (with the change) | `.dev-flow/2026-10-26-batch-01/evidence/scratch-evidence/suite-chunk02.txt` | `9e6acde8433f3a2c7a0c58bb6f67c7264ce7a6fff6a8bee0273a01dac35a3e7c` |
| targeted run (this audit) | `.dev-flow/2026-10-26-batch-01/evidence/suite-targeted.txt` | `dc926ea141ce406004e5ea247c1db56d279dc6679449e6018e67de3589d0306e` |
| supplemental targeted run (this audit) | `.dev-flow/2026-10-26-batch-01/evidence/suite-targeted2.txt` | `2441634600fab67c9bdbceaaa0cd049e9df057f71aa1aea6158e85cce6ecdf36` |
| import probe (this audit) | `.dev-flow/2026-10-26-batch-01/evidence/import-probe.txt` | `8edf7d996931be309318a241215ebede5dab20061eaf83a6664764ccaef38667` |

## 5 · Residual risks

AX-1/AX-2 (HIGH, records layer: stale canon rows; stale toast string) — proposed fixes in 02-review.md, open in `.dev-flow/BACKLOG.md`; AX-4 (nav/frame body-height parity edge); UX-1 (G3 fold trade-off on busy 80x24 boards — by design, awaiting operator confirmation).

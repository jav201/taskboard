# Inc MR-a — validation (E5: the change only)

**Verdict: done for E5, with two items still owed (below).** No MAJOR or HIGH finding is open. The head before the corrective pass was `478b32c`. The corrective commit is `5d2c880`, and the commit that adds this file carries the records.

## Scope proven
- Requirements: US-4601, 50 active requirements: the HLRs 4601..4606.2 and the LLRs 4601.1..4606.5 (`01-requirements.md`, ledger `01-requirements-ledger.md` .1–.8). TC numbering: LLR-46kk.n → TC-48nn (the rule is at the head of `01-requirements.md`). The cases are in `02-test-cases.md`, 50 of them, all `covered`.
- Design: Code-Wire baseline, interfaces, proto-S (`app.py`) and proto-V (`views.py`) (`graph-*.cw.md`, trace `e2-trace.txt`). PDR round 1 FAIL; round 2 PASS-WITH-NOTES for both reviewers (`03-pdr-*.md`, rulings `00-e1-rulings.md`, addenda `e3-addenda.md`).
- The change: a group's milestones share one row of the board gantt, with marks, labels, the label column and the chip. `←`/`→` walk the row. `/` and hidden classes filter it. Link mode keeps one row per milestone.

## Tests (all runs use `env -u NO_COLOR python -m pytest`; each header prints `taskboard.__file__`)
| Run | cwd | Result | Evidence |
|---|---|---|---|
| RED, the new tests on base `154e260` | base tree | 74 failed / 155 passed | `evidence/red-base.txt` |
| GREEN after the E4 build | worktree | 323 passed / 5 failed (handled at integration) | `evidence/green-1.txt`, `evidence/green-1b.txt`, `e4-integration.md` |
| GREEN after integration, 13 files | worktree | 329 passed | `evidence/green-2.txt` |
| RED first for the corrective tests, at the `478b32c` source | worktree | 2 failed (TC-4820c `x`, `中`) / 29 passed | `evidence/e5-red.txt` |
| **GREEN-3**: the same 13 files plus `test_hygiene.py` (the law guards: English, prism laws, markup census, modal keys, colour budget, hygiene) | worktree | **341 passed, 0 failed** | `evidence/green-3.txt` |

There is no full suite in this increment. It runs once, at the batch end.

## Mutants (run in copies of the tree, never in the worktree)
- E5 battery (DeepSeek v4 Pro, copy `incMR-mut`): 43 killed, 2 survived out of 45 (`05-mutants.md`).
- Corrective replay (copy `incMR-mut2`, removed afterwards): **38 (4605.2) killed** now that `gantt_plan` is the row's one seat (C-2). **39 (4605.3) killed** by TC-4843's per-step walk (C-1). The new 46 (N-9, `len > 1`) and 47 (the SEC-6 guard dropped) are both killed. `evidence/e5-mutant-replay.txt`.
- **Score: 47/47 killed.**

## Reviews of the code
- Code review: PASS-WITH-NOTES, 3 MEDIUM and 3 LOW (`05-review-code.md`). Fixed: F1 (`run:` tone), F2 (a zero-width case added; F2's claim that `étape` was precomposed was wrong, see `e5-corrective.md`), F3, F4 and F6 (graph and ledger .8), F5 (`_LaneMark`). Sent to BACKLOG: F5's optional `place` helper (MR-BL-1).
- Security review: PASS-WITH-NOTES, 2 LOW (`05-review-security.md`). Fixed: SEC-8 (TC-4820b pins the 0-cell guard) and SEC-9 (label runs are marked explicitly, with no inference from length).
- Re-review: nothing was blocking, so none is owed. The orchestrator checks C-1 and C-2 through the replay evidence.
- C-1's premise (that `hmove` walked the unfiltered lane) did not hold at `478b32c`. The test was blind, not the code (`e5-corrective.md`).

## Acceptance tests (black-box, through keys and dialogs)
AT-4601..AT-4607 and AT-4606b are in `tests/test_milestone_row_at.py`, all GREEN in `evidence/green-3.txt`.

## Not done / not run
- **The independent re-check of the `full`/`partial` marks** in `02-test-cases.md` (E5): owed, by someone who did not write them.
- **Real captures:** the UI changed. The prototype round's captures exist (`prototypes/milestone_row/out/png/`), but no Windows Terminal captures of the shipped build were taken in E5.
- Full suite and canon fold: at the batch end, by rule.

# Inc MR-b — validation (E5: the change only)

**Verdict: done for E5, with three items still owed (below).** No MAJOR or HIGH finding is open. The head before the corrective pass was `d04cc36`. One commit carries the corrective pass and these records. It changes no source file.

## Scope proven
- Requirements: US-4651 and 29 active requirements: HLR-4651..4654 and LLR-4651.1..4654.1 (`01-requirements.md`; ledger `01-requirements-ledger.md`, entries .1 to .11). TC numbering: LLR-4651.n → TC-49nn (the rule is at the head of `01-requirements.md`). The cases are in `02-test-cases.md`: 29 of them, all `covered`.
- Design: Code-Wire baseline, interfaces, proto-S (`app.py`) and proto-V (`views.py`) (`graph-*.cw.md`, trace `e2-trace.txt`). PDR round 1 PASS-WITH-NOTES for both reviewers (`03-pdr-*.md`). The rulings are in `00-e1-rulings.md` and the addenda in `e3-addenda.md`. The corrections are RB-2..RB-6, SEC-B1..B3 and A-1/A-2, which give a slice of 12 units in 2 files.
- The change: in `R`, a project's drawn milestones share one row in views 1, 2 and 3. The row reuses MR-a's field and label. The cursor, briefs and blocks follow one stop order. The `x` deck is byte-identical to base.

## Tests (all runs use `env -u NO_COLOR python -m pytest`; each header prints `taskboard.__file__`)
| Run | cwd | Result | Evidence |
|---|---|---|---|
| RED, the new and re-baselined tests on base `8ca174c` (full suite) | base worktree `incMRb-tests` | 98 failed / 4317 passed | `evidence/red-base.txt` |
| GREEN-1 after the E4 build, 15 files | worktree | 429 passed / 6 failed (all `test` defects, handled at integration) | `evidence/green-1.txt`, `e4-integration.md` |
| GREEN-2 after integration, the same 15 files | worktree | 435 passed | `evidence/green-2.txt` |
| **GREEN-3** after the E5 corrective pass, the same 15 files: the 2 new files, the 4 changed files, MR-a's 3 files (byte-identical to `8ca174c`), and the law guards `test_colour_budget`, `test_colour_budget_app`, `test_english`, `test_prism_laws`, `test_markup_census`, `test_modal_keys` | worktree | **435 passed, 0 failed** | `evidence/green-3.txt` |

The full suite does not run in this increment. It runs once, at the batch end.

## Mutants (run in a copy of the tree, never in the worktree)
- E5 battery (DeepSeek v4 Pro, a throwaway copy detached at `5a6a906`): one mutant for each E1 negative control, 26 in all, NC-01..NC-26 (`05-mutants.md`).
- **Score: 26/26 killed.** The corrective pass changed no source and weakened no assertion, so no replay is owed.

## Reviews of the code
- Code review (it covers the security lens, `SEC-` tags): PASS-WITH-NOTES, with 0 HIGH, 1 MEDIUM and 2 LOW (`05-review-code.md`).
  - **F1 (MEDIUM, `design-gap`) fixed.** LLR-4652.9 is amended: `\[x` is RED on base, `a\[b]` is a positive case, and the threshold is 8/8 (ledger `.11`). The `\`/`x\` RED claim (119 / 81 cells, `\\`) holds. The test was already right, and no code changed.
  - **F2 (LOW, `impl`) fixed.** The J-1 assertion in `tests/test_milestone_marks.py` is split with parentheses, with the same four conjuncts. MR-b's two `SEAT_SITES` labels now read `":7499 …"`.
  - **SEC-F3 (LOW, pre-existing) sent to the backlog** as MRb-BL-1. The other `SEAT_SITES` labels that were stale before MR-b went to the backlog as MRb-BL-2 (`.dev-flow/BACKLOG.md`).
- No separate security review was run. The code reviewer covered the security lens, and the PDR security review (`03-pdr-security.md`) covered the design. Nothing was blocking, so no re-review is owed.

## Acceptance tests (black-box, through keys and dialogs)
AT-4651..AT-4656 are in `tests/test_present_milestone_row_at.py`: 7 functions, 16 items. All are GREEN in `evidence/green-3.txt`.

## Trace
`trace_check.py --req .dev-flow/2026-11-06-v3-incMRb/01-requirements.md --base 8ca174c --src taskboard` on `7e71bcd`: **1 US, 29 active requirements (0 withdrawn), 0 gaps, exit 0.** The canon (`--canon`) is folded at the batch end.

## Not done / not run
- **The independent re-check of the `full`/`partial` marks** in `02-test-cases.md` (E5): owed, by someone who did not write them.
- **Real captures:** the UI changed, but no Windows Terminal captures of the shipped build were taken in E5.
- Full suite and canon fold: at the batch end, by rule.

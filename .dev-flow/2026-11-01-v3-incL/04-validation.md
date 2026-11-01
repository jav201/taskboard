# Inc L — validation (E5: the change only)

**Verdict: done.** No open MAJOR/HIGH. Head at close: `5151ced` (corrective pass) plus the records commit after it.

## Scope proven
- Requirements: 6 HLR, **69 active LLR** (70 ids; LLR-4304.16 withdrawn by ARCH-3), 5 AT (`01-requirements.md`; ledger LED.1–LED.5). Every active LLR has ≥ 1 test (`evidence/red-summary.md` TC→LLR map; TC-4362b added at E5).
- Design: Code-Wire graph — baseline 26 nodes (lint 0; extract exit 1 = 8 untyped-input findings, no drift); prototype 56 nodes (interfaces 10, D 11, V 16, S 19), lint 0 on all four; 69/69 active LLRs traced to examples (`e2-trace.txt`).
- Seams between groups: D→V (`Task.created`, `stamp`), D→S (`stamp`, `Board.add_task`), V→S (`added_rows`, `added_order`, `first_created`, `render_added_list`, `AddedRow`), keymap→S (`added_list`), S→views (`board_lanes` lanes). One seam defect at integration (day-header base style bled bold over the pane), fixed in `render_added_list`.
- PDR: round 0 (28 prototype findings, 5 MAJOR, all ruled); round 1 architect FAIL (1 HIGH, 2 MEDIUM) + security PASS-WITH-NOTES (3 MEDIUM); round 2 both PASS-WITH-NOTES (`03-pdr-*.md`, `03-pdr-rulings.md`).

## Creation paths that set `created`
`Board.add_task` (stamps when None, one clock read shared with the history birth record) — reached by the editor add (`_on_task_added`, `a`) and the link-picker create row (`_create_and_link`, `L`); the template insert (`_on_template_picked`, `I`, one stamp for all inserted tasks); the seed of a missing board (`Board.load`). Kept unchanged: edit, `move_project` (deepcopy), undo restore, rescue (never stamped). Inc K's dump must go through `Board.add_task`. `created` is never sent in the team push (SEC-1).

## Old boards keep their bytes (proven)
- TC-4315 ×3: plain, legacy and unknown-key old boards — load + save byte-equal to the bytes `eb411e1` writes (frozen oracle; the legacy board is rewritten by the migration at base too).
- TC-4316: adding a task to an old board leaves every old entry byte-identical, with a birth record present to back-fill from.
- TC-4317 / AT-4305: sha256 of both boards and both `history.jsonl` unchanged across `N ↓ ↓ o v v esc`; the security review hashed every file under home: 0 changed.

## Tests (all `env -u NO_COLOR python -m pytest`, `taskboard.__file__` in each header)
| Run | cwd | Result | Evidence |
|---|---|---|---|
| RED, new tests on base `eb411e1` | incL-base | 90 failed / 4 passed (guards by design: TC-4315 ×3, TC-4316), 0 errors, all assertion failures | `evidence/red-base.txt`, `red-summary.md` |
| GREEN after E4 build | worktree | 126 passed / 1 failed (seam: header style) | `evidence/green-1.txt` |
| GREEN after integration | worktree | 162 passed (Inc L tests + keymap, help keys, modal keys) | `evidence/green-2.txt` |
| Guards (modules exercising the changed functions) | worktree | 722 passed, 1 skipped (pre-existing Windows-clipboard skip in test_app) | `evidence/guards-1.txt` |
| RED, E5 regression TC-4362b on `79cf2b2` | worktree before the fix | 1 failed / 94 passed; CR-4/CR-5 arms proven by scratch mutants | `evidence/red-e5.txt` |
| GREEN after the corrective pass | worktree | 226 passed | `evidence/green-3.txt` |

No full suite in this increment (it runs once at batch end).

## Mutants (new arms only, in the copy `incL-mut`)
50/50 killed (`05-mutants.md`, `evidence/mutants-run.txt`; DeepSeek v4 Pro ran them; the orchestrator replayed M30 — tie-break removed — independently: killed by TC-4364 and TC-4366b, `evidence/mutant-spotcheck-M30.txt`). The CR-1 arm is proven by TC-4362b failing on `79cf2b2`.

## Reviews of the code
- Code review: PASS-WITH-NOTES — 6 MINOR (CR-1 design-gap fixed + LED.5; CR-2, CR-3, CR-4, CR-5 impl fixed; CR-6 design-gap deferred → L-BL-5). `05-review-code.md`.
- Security review: PASS-WITH-NOTES — 5 LOW (SR-1, SR-3, SR-4 inherited → L-BL-6..8; SR-2 = L-BL-4; SR-5 backlog written). `05-review-security.md`.
- Re-review of blocking items: none were MAJOR/HIGH; the orchestrator verified CR-1 via TC-4362b RED→GREEN.

## Acceptance tests (black-box, keys and dialogs)
AT-4301 (two boards, `N`, `o`, `↓`, `esc`, bytes unchanged), AT-4302 (`a` add → row 0, old entries unchanged), AT-4303 (`I` template → three rows, one time), AT-4304 (`v` archived toggle), AT-4305 (old board: `≈` and `?`, source lines, bytes unchanged) — all GREEN in `green-3.txt`.

## E13 captures — real Windows Terminal, truecolor
`evidence/captures/`: `ls-newest`, `ls-oldest`, `ls-archived`, `ls-pane`, `ls-inferred`, `ls-unknown` at 118x30 and 80x24 (12 PNG, 274–354 colours each, end state checked, 0 retries). Each `cpi-` window closed by exact title; final assertion "no cpi-* window left open" (`captures.md`, `capture-log.txt`). Orchestrator review: matches the design.

## Timing (same script for both increments, `timing.py` → `evidence/timing.txt`)
Inc L wall 114 min (E0 2.5, E1 3.7 inside E2a, E2 35.0, E3 21.4, E4 31.5, E5 23.7) vs Inc C 134 min (E2 29.6, E3 37.4, E4 27.1, E5 39.0).

## Not done / not run
- Full suite — by rule, at batch end.
- CR-6 (home key row naming `N`) — deferred, L-BL-5.

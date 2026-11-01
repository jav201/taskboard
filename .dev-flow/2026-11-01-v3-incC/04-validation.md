# Inc C — validation (E5: the change only)

**Verdict: done.** No open MAJOR/HIGH. Head at close: see `git log` (corrective pass `9c9521d`, records after it).

## Scope proven
- Requirements: 6 HLR, **68 LLR**, 4 AT (`01-requirements.md`; ledger LED.1–LED.7). Every LLR has ≥ 1 test (`evidence/red-summary.md` TC→LLR map).
- Design: Code-Wire graph — baseline 12 nodes; prototype 37 nodes (interfaces 5, V 9, M1 13, M2 10), lint 0 on all four; 68/68 LLRs traced to examples (`e2-trace.txt` covers 67 + LLR-4204.10 → TC-4296/4297).
- PDR: round 1 architect FAIL (1 MAJOR, 2 HIGH) + security PASS-WITH-NOTES (3 MED); round 2 both PASS-WITH-NOTES (`03-pdr-*.md`, rulings `03-pdr-rulings.md`).

## Tests (all `env -u NO_COLOR python -m pytest`, `taskboard.__file__` in each header)
| Run | cwd | Result | Evidence |
|---|---|---|---|
| RED, new tests on base `0a8dfaa` | incC-base | 212 failed / 6 passed (4 guards by design, 2 oracle self-checks), 0 errors, all assertion failures | `evidence/red-base.txt`, `red-summary.md` |
| GREEN after E4 (no integration fix needed) | worktree | 252 passed (Inc C tests + test_modal_keys) | `evidence/green-1.txt` |
| Guards (modules that exercise the changed functions) | worktree | 230 + 119 passed | `evidence/guards-1.txt`, `guards-2.txt` |
| RED, E5 regression tests on `4fa090a` | worktree before fix | 8 failed / 2 pass (CR-1 pin, 2 000-char boundary) | `evidence/red-e5.txt` |
| GREEN after the corrective pass | worktree | 260 passed + 2 re-ruled → 3 passed; RED control for TC-4290 via scratch plugin | `evidence/green-2.txt`, `green-2b.txt` |
| Final: Inc C tests + all guards | worktree | 610 passed, 1 timing failure (TC-4296 0.85 s > 0.8 s) → LED.7 → 7/7 passed | `evidence/green-3.txt`, `green-3b.txt` |

No full suite in this increment (it runs once at batch end).

## Mutants (new arms only, in the copy `incC-mut`)
40/40 killed (`05-mutants.md`; DeepSeek v4 Pro ran them; the orchestrator replayed M14 independently: killed by TC-4249). The corrective arms (E13-1, CR-2, CR-3/SR-2, CR-4, SR-1) are proven by their regression tests failing on `4fa090a` (`red-e5.txt`).

## Reviews of the code
- Code review: PASS-WITH-NOTES — 1 MEDIUM (CR-1, design-gap: accepted as designed, pinned), 7 MINOR (4 impl, 4 design-gap … CR-2..CR-6 fixed, CR-7/CR-8 accepted). `05-review-code.md`.
- Security review: PASS-WITH-NOTES — SR-1 MEDIUM (design-gap: fixed, LLR-4204.10), SR-2 LOW (fixed), SR-3 LOW (accepted, README). `05-review-security.md`.
- E13-1 (orchestrator, from the captures): opaque palette screen — impl, fixed, TC-4290.
- Re-review of blocking items: none were MAJOR/HIGH; the orchestrator verified the two MEDIUM fixes (SR-1 via TC-4296/4297, E13-1 via TC-4290 + the new capture).

## Acceptance tests (black-box, keys and dialogs)
AT-4201 (pens → save → details), AT-4202 (palette), AT-4203 (HTML export), AT-4204 (legacy unchanged) — all GREEN in `green-3.txt`.

## E13 captures — real Windows Terminal, truecolor
`evidence/captures/`: `ed-pen`, `palette` (re-shot after E13-1), `details`, `present` at 118x30 and 80x24, plus `html-workspace.png` (0 console errors). Every shot ≥ 8 colours, end state checked, each `cpi-` window closed by title, final assertion "no cpi-* window left" (`captures.md`, `capture-log.txt`).

## Not done / not run
- Real-terminal alt+digit key press (ARCH-14) — `not-run` (key injection failed on this desktop); BACKLOG C-BL-2.
- Full suite — by rule, at batch end.

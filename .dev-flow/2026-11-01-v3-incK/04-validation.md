# Inc K — validation (E5: the change only)

**Verdict: done.** No open MAJOR/HIGH. Head at close: `473ac1d` (corrective pass) plus the records commit after it.

## Scope proven
- Requirements: 9 HLR, **206 active LLR** (215 ids, 9 withdrawn), 8 AT (`01-requirements.md`; ledger LED.1–LED.6). LED.6 (E5): LLR-4407.50, LLR-4407.51, LLR-4408.21 added; LLR-4401.8, LLR-4402.14, LLR-4407.19, LLR-4407.35, LLR-4408.3 reworded.
- Design: baseline 31 nodes; prototype interfaces 29 + S 45 + T 9 + V 41 nodes; lint 0; trace 203/203 + 8/8 at E3. E5 amended the touched contracts in `graph-proto-S.cw.md` / `graph-proto-V.cw.md`.
- PDR: round 1 FAIL (arch 1 HIGH 4 MAJOR; sec 3 MAJOR) → round 2 PASS-WITH-NOTES; addenda A-1..A-4 (`03-pdr-*.md`, `03-pdr-rulings.md`).

## E4 integration (`e4-integration.md`)
GREEN-1 27 failed / 438 passed → fixes F1–F9 (seam 21 tests on one root cause: `rich.color.Color` vs `textual.color.Color`; impl 2; test 6) and the orchestrator's **R-E4-1** ruling: `write_atomic` unchanged; `Inbox._commit` counts the bytes on disk (`len(data) + text.count("\n") * (len(os.linesep) - 1)`); TC-4677's count per platform; new TC-4677c (real filesystem, `os.path.getsize` at CAP and CAP + 1), RED before the fix (`DID NOT RAISE`).

## Tests (all `env -u NO_COLOR python -m pytest`, `taskboard.__file__` in each header)
| Run | cwd | Result | Evidence |
|---|---|---|---|
| RED, new tests on base `545c18a` | incK-base | 323 failed / 1 guard (TC-4415) | `evidence/red-base.txt`, `red-summary.md` |
| GREEN-1 after E4 build | worktree | 27 failed / 438 passed | `evidence/green-1.txt` |
| GREEN-2 after integration + R-E4-1 (7 files) | worktree | 466 passed | `evidence/green-2.txt` |
| Guards-1 (10 modules exercising the changed functions) | worktree | 255 passed | `evidence/guards-1.txt` |
| RED, E5 corrective tests on `f931070` | worktree | each new test RED for its behavioural reason (2 via temporary mutants) | `evidence/red-e5.txt` |
| GREEN-3 after the corrective pass (7 files) | worktree | 478 passed | `evidence/green-3.txt` |
| Guards-2 | worktree | 255 passed | `evidence/guards-2.txt` |

No full suite in this increment (it runs once at batch end).

## Mutants (new arms only, copy `incK-mut` at `f931070`)
**59/60 killed** (`05-mutants.md`, `evidence/mutants-run.txt`; DeepSeek v4 Pro ran them, 13:34–13:52). M48 (`Inbox.load` reads the whole file) SURVIVED: TC-4675's store was exactly CAP + 1 bytes, so a whole read was indistinguishable. Fixed in the corrective pass: a TC-4675 arm at CAP + 4096, RED under M48. Orchestrator replay: M40 (SEC-1 multiset) killed, M48 survived (`evidence/mutant-spotcheck.txt`).

## Reviews of the code
- Code review: PASS-WITH-NOTES — 1 MEDIUM (CR-1 design-gap), 7 MINOR (`05-review-code.md`).
- Security review: PASS-WITH-NOTES — 5 LOW, 3 INFO (`05-review-security.md`).
- Rulings (`03-pdr-rulings.md` § E5): FIX CR-1, CR-2, CR-3, CR-5, CR-7, K-SEC-1, K-SEC-2, K-SEC-3, K-SEC-5 + the M48 test gap — all fixed RED-first (`05-corrections.md`). BACKLOG: CR-4, CR-6, CR-8, K-SEC-4, I-1..I-3 → K-BL-1..15.
- Re-review: nothing blocking was open (no MAJOR/HIGH); the orchestrator re-read the CR-1 fix (`mark_notice` holds `dumped` only when the file was unchanged) and closed it.

## Acceptance tests (black-box, keys and dialogs)
AT-4401 (118x30 and 80x24), AT-4402, AT-4403, AT-4404, AT-4405, AT-4406, AT-4407, AT-4408 — **8/8 GREEN** (9 cases) at `473ac1d` (`evidence/at-run.txt`).

## E13 captures — real Windows Terminal, truecolor
`evidence/captures/`: k-empty, k-dividers, k-notice, k-rail, k-review, k-dump, k-newproject, k-colour at 118x30 and 80x24 (16 PNG, 223–487 colours, 0 retries, end state checked) at `f931070`. Each `cpi-` window closed by exact title; final assertion "no cpi-* window left open" (`captures.md`, `capture-log.txt`). The corrective pass changed no drawn state of these scenes (CR-7 only below 80 columns, where `w - 2` = 78 at 80; K-SEC-2's notice and CR-3's home quit are not in a scene), so no reshoot. Orchestrator viewed `k-rail_118x30.png`: matches the design. Notes: k-rail draws no `or` line (note 4 matches one project); the one-time divider notice covers the `alt+n` field for 15 s on first use (K-BL-14).

## Timing (`timing.py` → `evidence/timing.txt`, same script as Inc L)
Inc K wall 217.6 min (E0 1.6, E2 61.4 incl. E1, E3 45.8, E4 64.6, E5 44.2) vs Inc L 114.1 min (E2 35.0, E3 21.4, E4 31.5, E5 23.7). Inc K is ~3× Inc L's LLR count (206 vs 69): 1.06 vs 1.65 min per LLR. E4 includes a conductor hand-off.

## Operator flags
- R1-1: the divider key is `alt+l` (Textual 8.2.8 reads ESC CR as `enter` from Windows Terminal); hint row `____ ↵ new note · alt+l divider`.
- P-V-1: the new-project field cycles boards with `tab` (`alt+b` parses as `ctrl+left`).
- ARCH-11: dumped note text stays in `inbox.json` 7 days after its task is deleted (commission-mandated).

## Not done / not run
- Full suite — by rule, at batch end.
- BACKLOG K-BL-1..15 (`.dev-flow/BACKLOG.md`).

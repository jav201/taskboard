# Increment 001 — HD-1..HD-4 · the home defers the board's start

| Field | Value |
|---|---|
| Batch | `2026-10-24-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2701` / `LLR-2701.1`, `LLR-2701.2` · `HLR-2702` / `LLR-2702.1`, `LLR-2702.2`, `LLR-2702.3`, `LLR-2702.4` · `HLR-2703` / `LLR-2703.1` · `HLR-2704` / `LLR-2704.1` · `HLR-2705` / `LLR-2705.1` · `HLR-2708` / `LLR-2708.1`, `LLR-2708.2` |
| Acceptance | `AT-2701` · `AT-2702` · `AT-2703` · `AT-2704` · `AT-2705` · white-box `TC-2703` |
| Agent | `software-dev` (spawned coder sub-agent) |
| Date | `2026-10-25` |

## 1 · What changed

The board start is split into a read-only mount half and the deferred write half, gated by one started-board record (the PDR's design, decisions `PDR-2026-10-24-batch-02#D1..D3`). With the home shown at start, `on_mount` renders the board but starts nothing; leaving the home (`enter` on a card through `switch_board`'s same-board branch, or `esc`/`back` through `BoardsHome.action_back`) runs the deferred start exactly once; the single-board and `--open` mounts run the full start at mount byte-for-byte as before. `switch_board`'s failure restore carries the record back with the rest of the session state. **PDR condition C1** (this packet names every regression arm and its mutation), **C2** (the `unlisted:<path>` record key + the B→esc-on-`--open` arm), **C3** (the restore invariant + `_mount_board`'s position after the sweep) and **C5** (risks R1/R2, carried in the PDR record) are discharged here.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-2701.1, LLR-2702.1, LLR-2702.2, LLR-2702.3, LLR-2702.4 (LED-2702.1r4), LLR-2704.1, LLR-2705.1, LLR-2708.1, LLR-2708.2 | the `_started_board` record + `_started_key()` (`app.py:1254`, `:1257`); `on_mount`'s home branch (`:1311-1324`); `_mount_board()` (`:1418`); `_open_board`'s guard/record (`:1429-1450`); `switch_board`'s same-board pending branch + the `keep` restore (`:1476+`); `BoardsHome.action_back` (`:759-767`); `open_on_board`'s pending-start branch for the agenda/people jump (`:870-884`, code review F1) |
| `tests/test_home_deferred_start.py` | test | HLR-2701, HLR-2702, HLR-2703, HLR-2704, HLR-2705, LLR-2701.2, LLR-2702.1, LLR-2702.2, LLR-2702.3, LLR-2702.4, LLR-2703.1, LLR-2704.1 | new — AT-2701, AT-2702, AT-2703, AT-2704, AT-2705 + TC-2703 (6 nodes) |
| `tests/test_boards.py` | test | HLR-2708, LLR-2708.1, LLR-2708.2 (the PDR-C1 named arms) | `test_TC_2202_switch_board_starts_the_other_board_over` leaves the home before the same-board no-op; `test_TC_2202_the_mount_order_is_the_shipped_one` expects the read-only half at the with-home mount, then the deferred start after `esc` |
| `tests/test_boards_backlog_round.py` | test | HLR-2705, LLR-2705.1, HLR-2708, LLR-2708.1 (the PDR-C1 named arms) | AT-2408, AT-2409, TC-2409 lifecycle: the marker/notice move off mount — each arm leaves the home first; the `--open` second-window arm has the first window leave its home before the second opens; pinned strings unchanged |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |

The named test updates are the permitted diffs of HLR-2708/LED-2708r1 — the change of timing is the point of each; no assertion was weakened (the arms drive the home with keys; the same-board no-op re-asserted only after the start completes). One implementer deviation, ratified here: the AT-2703 `--open` arm exercises the `unlisted:` sentinel through `open_app(None, unlisted=side)` (a truly unlisted board shows no home — HD-4 — so the C2 arm starts it at mount, then `B` → home → `esc` must re-run nothing).

## 3 · How to test

`env -u NO_COLOR python -m pytest -q tests/test_home_deferred_start.py tests/test_boards.py tests/test_boards_home.py tests/test_boards_backlog_round.py tests/test_milestone_offer.py tests/test_milestone_offer_seam.py tests/test_team_views.py tests/test_team_sync.py`

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| B | `tests/test_home_deferred_start.py::test_AT_2701_the_home_touches_nothing` (incl. the `q` beat, LLR-2701.2) | 1 passed (`suite-001.txt`) |
| B | `::test_AT_2702_enter_runs_the_deferred_start` | 1 passed |
| B | `::test_AT_2703_escape_runs_the_start_once` (incl. the C2 `--open` arm) | 1 passed |
| B | `::test_AT_2704_another_board_never_writes_the_default` | 1 passed |
| B | `::test_AT_2705_the_offer_opens_over_the_board` (`milestone_offer` seam marker) | 1 passed |
| A | `::test_TC_2703_a_failed_deferred_start_keeps_the_board_pending` | 1 passed |
| regression pin | the 8 named suites + the two jump-seat suites (`test_all_agenda.py`, `test_people_view.py`) | 440 passed, 0 failed (`suite-001.txt`, post-F1-fold) |

| Field | Value |
|---|---|
| **RED counterfactual** | mutant E1 of `mutation-001.py` — `on_mount`'s home branch calling `_open_board(at_mount=True)` instead of `_mount_board(at_mount=True)`, i.e. the pre-HD-1 defect shape restored — made `test_AT_2701_the_home_touches_nothing` fail (notice at mount, marker written, sweep ran) · `.dev-flow/2026-10-24-batch-02/evidence/mutation-001.txt` · restore digest `89ff66cf3c6425160dfe83b3d30d478246b4a9fbdd1eb0b5ef248c629d8af89b` (the post-increment app.py, proven after every arm) |
| **Mutation verdicts** | 24 arms, 0 CRASH/BAD, per-arm verdicts in `mutation-001.txt`: E1 KILLED by AT-2701/AT-2704/AT-2705 (survived AT-2702/AT-2703 — "exactly once" holds under it, the correct reading) · E2 (no record write) KILLED by AT-2702, AT-2703, TC-2703 · E3 (`action_back` pops without `_open_board()`) KILLED by AT-2703 · E4 (record written before the migration gate) KILLED by TC-2703 |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | none — this increment emits no artifact |
| **Reverse census** | 5 probes, all B1-driven (the trigger fired at intake): B1 `grep -rln "_open_board\|_mount_board\|_started_board\|switch_board" tests/` → the 3 touched test files only, each named above · B2 no file moved (none) · B3 no golden capture (`ls tests/ | grep -i golden` → fixture names only) · B4 no path another component consumes · A3 no consumed interface re-signed — 0 foreign hits |
| **Correction population** | none — no correction |
| **Where it ran** | the orchestrator's own tree, no other session reading; the battery restored and hash-proved app.py after every arm |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite run | `.dev-flow/2026-10-24-batch-02/evidence/suite-001.txt` | `a8c6b3eb15c3530f0cc0974cf7266c6d80bc62c7b569bac9972426154dd695cb` |
| RED capture + battery | `.dev-flow/2026-10-24-batch-02/evidence/mutation-001.txt` | `4002cd760c40d0192104c38996d7f70eb8151db65ee0ae1274790227c490f5d0` (against the pre-F1-fix app.py; restore digest `89ff66cf…`) |
| code-review F1 discharge | `.dev-flow/2026-10-24-batch-02/evidence/mutation-001b-f1.txt` | `72f62bc7e7482b497dd20beed921df67c608f365b9971adbfeeb34f694c4f928` (the `open_on_board` elif removed → AT-2702 RED; restore digest `dd40a190…`, the post-fix app.py) |
| the battery runner | `.dev-flow/2026-10-24-batch-02/evidence/mutation-001.py` | (the instrument, runnable) |

| Field | Value |
|---|---|
| **Evidence files** | 2 transcripts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with `agents/code-reviewer.md` · round 1: BLOCK-UNTIL F1 (the `open_on_board` pending-start hole — folded, discharged by re-read + `mutation-001b-f1.txt`) · round 2: **PASS, 0 HIGH** (one LOW, N1 — the IFC SOURCE line, folded into the contract) |

## 5 · Risks

R1/R2 (record/restore interplay; sweep-under-view ordering) are carried by TC-2703 and the mount-order arm respectively — both green. The `unlisted:` key compares a path string; two `--open` windows on the same file compute the same key, which is correct (the second window is told by the presence notice, unchanged). LLR-2706's seats and `refresh()` do not exist yet — increment 002; this increment touches none of its files.

## 6 · Pending items / spec deviations

The AT-2703 `--open` arm deviation (section 2) — ratified against PDR-C2's intent.

**Code review round 1 (finding F1, HIGH, BLOCK-UNTIL):** the agenda-of-every-board and
people-view jump onto a task's board (`open_on_board`) popped the home and, when the task
was on the current board, never ran the pending start — the window would never announce
itself (the silent collision HLR-2705 exists to prevent). Folded: `open_on_board` gained
the pending-start branch reusing LLR-2702.3's seam; the contract's LLR-2701... LLR-2702.1
path list was amended to name the jump (LED-2702.1r4); AT-2702's node gained the fifth-path
beat; the focused mutation discharge is `mutation-001b-f1.txt`. The suite transcript was
re-taken post-fold (440 passed).

## 7 · Suggested next task

Increment 002 (HD-5, `people.py` + `marks.py` + `app.py` + the `SearchPrompt` seat), then the DDR.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | §4: 6 new nodes + 3 named updated files |
| 3 | Layer 0 where it applies | ✓ | TC-2703 covers the record's state machine arms (unit-level via the integration seam; the pure-logic halves ride increment 002's TCs) |
| 4 | RED counterfactual | ✓ | §4, E1 transcript |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ⏸ | §4b — at the gate |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen; no consumed interface re-signed |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt`: 402 passed |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence — every quiet assertion pairs with its fired counterpart in AT-2702/2703 |
| 11 | Mutation verdicts | ✓ | §4: 24 arms, targets KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ⏸ | §4b — at the gate |
| 16 | Evidence files | ✓ | §4: 2 digests |

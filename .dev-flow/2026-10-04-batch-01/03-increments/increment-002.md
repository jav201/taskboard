# Increment 002 — HLR-501, HLR-504 (LLR-501.1..501.4, LLR-504.1) · the waits-on model, the marks, the guard

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal). Mode
> `core`, language `en`. Revision 2 (frozen r2): code review round 1 BLOCK-UNTIL F1 (HIGH, tests
> only — folded under the operator's standing rule) and F2 (HIGH, product — the batch STOPPED and
> the operator ruled "Corregir en el 002"); round 2 OK to advance.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-501, LLR-501.1, LLR-501.2, LLR-501.3, LLR-501.4; HLR-504, LLR-504.1 (all paths but the project archive, which is increment 003's); amendments A-3, A-4; D-503, D-506, D-508, D-519 |
| Acceptance | AT-501, AT-505 · white-box TC-501..506, TC-517, TC-518 · unit the derivations in `models.py` (layer 0 inside TC-501..503, 517, 518) |
| Agent | `software-dev` |
| Date | `2026-10-04` |

---

## 1 · What changed

**Links mean "waits on" and the board shows it: cards paint `◂N` (waits on N open tasks) and `▸N`
(N open tasks wait on it) instead of `⛓N`; finishing work says once what became ready; and an open
task others wait on cannot be archived or deleted.** `models.py` derives the state from live links
over board tasks only (dangling, self and repeated ids ignored; closed tasks count nothing; one id
map, iterative walks): `open_predecessors`, `open_dependents`, `link_marks` (one reverse index per
render), `dependents_chain`, `link_overlap` (the one measure — a start on the predecessor's due day
is a 1-day conflict, D-503), `link_conflicts`, `loop_path` (over closed tasks too), `waiting_ids`,
`ready_messages` (at most 3, then "+K more ready"), `archive_refusal`. `views.py`: every card caller
passes one marks map; marks shed before the project tag (A-3); a teammate's task paints none; the
gantt `↳` gutter reads open predecessors and the one measure; the flow packet stops for a waiting
task; the kanban help names `◂N`, `▸N` and `L`. `app.py`: the ready toast after `]` and the editor;
the guard on `x`, `d` (before its confirm and again at `yes`) and the editor's archived box (judged
after its phase, other fields saved); `x` in Setup now only removes a setup row (F2, A-4, S-7 closed).
Also folded: increment 001's N1 — the atomic save keeps the board file's permissions.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-501.1, LLR-501.4, LLR-504.1, LLR-505.2 | the waits-on block; `save_atomic` keeps the target's mode (N1) |
| `taskboard/views.py` | source | LLR-501.2, LLR-501.3 | `_link_tokens`; `marks=` through `card_cell`, `_card_meta`, `kanban_card`, `_kanban_cell` and their callers (focus review, people, kanban grouped and lanes); `gantt_dep_mark`; `_flowing`; kanban help |
| `taskboard/app.py` | source | LLR-501.4, LLR-504.1 | `_say_ready`, `_refuse`; guards in `action_archive` (Setup branch first), `action_delete`, `_on_delete`, `_on_task_edited` |
| `tests/test_links.py` | test | HLR-501, HLR-504, LLR-501.1, LLR-501.2, LLR-501.3, LLR-501.4, LLR-504.1 | +23 nodes: TC-501 ×2, TC-502, TC-503 ×8, TC-504 ×3, TC-505, TC-506 ×2, TC-517 ×3, TC-518, AT-501, AT-505 |
| `tests/test_dependencies.py` | test | LLR-501.2 | the `⛓` token tests rewritten to `▸`/`◂` |
| `tests/test_kanban_readable.py` | test | LLR-501.2, LLR-501.4 | TC-302 (`tm5` paints `◂1`), TC-303 (`marks=`), TC-310 (`▸` in the example), AT-308 (the ready toast follows the rail note) |
| `tests/test_gantt_board.py` | test | LLR-501.3 | TC-105's same-day arm is `over` (D-503) |
| `tests/test_gantt_polish.py` | test | LLR-501.4 | the fold-notice helper leaves out `Ready` toasts (F1) |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 5 (uncapped) |
| Doc files | 0 (records: amendments A-3, A-4, ledger LED .14, .15) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_links.py tests/test_gantt_polish.py tests/test_kanban_readable.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-501 ×2, TC-502, TC-503 ×8, TC-517 ×3 (unit arm), TC-518 | in the 24 below |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-501..506, TC-517, TC-518 (+ TC-506's `b` arm from 001) | 22 passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-501, AT-505 | 2 passed |

Gate run on frozen r2: `python -m pytest -q -p no:cacheprovider` → **2265 passed in 355.60 s, exit 0**
(`evidence/inc002-gate-r2.txt`). Round 1's run held the six stale pins F1 named: 6 failed, 2257 passed
(`evidence/inc002-green.txt`). The highest count in the cited evidence, 7 failed, is the RED counterfactual's
deliberate failures (`evidence/inc002-red-on-inc001.txt`, increment 002's tests on increment 001's product).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | increment 002's tests on increment 001's frozen r4 product (hashes matched): 7 superseded pins FAILED and `test_links.py` could not import the new API (`evidence/inc002-red-on-inc001.txt`); F2's own test FAILED on frozen r1 — `ta3` archived from Setup (`evidence/inc002-f2-red.txt`); F1's RED is the six failures in `inc002-green.txt`; restore digests per mutant in `inc002-mutations-r2.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | r2: **21 of 21 KILLED** (`evidence/inc002-mutations-r2.txt`, spec `mutants_inc002_r2.json`): N1 closed predecessors counted · N2 repeated id · N3 strict measure · N4 open-only loop search · N5 a teammate task paints marks · N6 marks dropped · N7 archived predecessor in the gutter · N8 packet on a waiting task · N9 no cap · N10 ready while still waiting · N11–N13 `x`/`d`/editor unguarded · N14 the archived set's own waiters · N15 the people view on the fallback · N16 closed waiters counted · N18 `◂` shed before `▸` · N19 ready never said · N20 Setup `x` reaches the task · N21 no fold notice · N22 delete not judged again. r1: 16/18 (N5, N16 SURVIVED — input-set gaps, arms added) |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments: `battery.py` reported N5/N16 SURVIVED in r1 before r2's arms; TC-517's Setup arm FAILED on r1 (`inc002-f2-red.txt`) before its pass was believed |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts asserted against the painted/emitted form: the kanban screen (marks and their muted tone read from the compositor's segments, AT-501), the toasts (`str(toast.render())`, AT-501, AT-505, TC-506), the saved board file (TC-506, TC-517) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `inc002-gate-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-gate-r2.txt` | `b4d6c2c720308f57da39ae29e5804c9b0930ee7646b8a6ccb5e8f7983b7ed552` |
| `inc002-green.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-green.txt` | `9d9d4bfb6324bbd5304f11f43ab31cd20aa5f2d1776de8c526e12b05289339de` |
| `inc002-green-r2pre.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-green-r2pre.txt` | `887fe501603864604f707e5d64c0010fb9aa089c84c22fc1d7bb459171884732` |
| `inc002-red-on-inc001.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-red-on-inc001.txt` | `0e92c524341e0bf0b5a1c243773ea47ed6eb2727c91ce2196c9222a316d2512b` |
| `inc002-f2-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-f2-red.txt` | `56b405948617f546d45f186fb0c451d0d33fce3193fb036604af17cfb432133e` |
| `inc002-mutations.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-mutations.txt` | `a38dac19b9aa4f3d1ce3470c36bd6ed312c27458b50c9b6334550b0e9978b93f` |
| `inc002-mutations-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-mutations-r2.txt` | `afe1a7f1e9ca75b0c44cf22a73a3df79327f48755606aecc1cab6a5c205bc3f0` |
| `mutants_inc002_r2.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc002_r2.json` | `70be50b6cc7488215f62f47d0703749320ef6ec265f15839ba422a35cb02eb9c` |
| `inc002-frozen-r2.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc002-frozen-r2.sha256` | `19ca5d14daa79b9caf20b325eaca755466f7d15f29ceddb4c05b92a8329b2720` |

| Field | Value |
|---|---|
| **Evidence files** | 9 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no other card renderer is left on the unblock count" and "no other archive path bypasses the guard" |
| If the result is an ABSENCE, what made the search wide enough | callers derived from the AST (TC-504, ≥ 4); archive paths: `x`, `d`, editor, Setup `x` (F2), project archive (increment 003), sweep and `X` (done only, exempt) |
| Synthetic instance of the absent case | N15 (the people view on the fallback) and N20 (Setup `x`) KILLED |
| **Positive control for every probe that returned an ABSENCE** | N15, N20 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 `grep -rl` over `tests/` for `⛓`, `unblocks=`, `card_cell`, `kanban_card`, `gantt_dep_mark`, `_flowing`, `action_archive`, `toggle_blocked`, notification lists — `test_dependencies.py`, `test_kanban_readable.py`, `test_gantt_board.py` updated; `test_gantt_polish.py` was found by the full run, not by the symbol grep (it keys on notifications) — named as a census miss, fixed (F1); B2 0 moves; B3 no goldens; B4 the saved board (TC-506, TC-517 read the file); A3 `link_marks` etc. read by `views.py` and `app.py` only |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "`⛓N` → `▸N`/`◂N`" — population `grep -rn "⛓\|unblocks=" taskboard tests` before the first edit: 3 product sites (`card_cell`, `_card_meta`, the help text/example) and 4 test files; all edited; `unblocks_count` kept for the `unblock` sort (D-513) |

### Signed-balance test ledger

`post = base − deleted + added` → `2265 = 2242 − 0 + 23` ✓ (the 23 new `test_links.py` nodes; pins rewritten in place).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · round 1 BLOCK-UNTIL F1, F2: F1 HIGH (tests only: six stale fold-notice pins) folded without stopping under the operator's standing rule, RED = `inc002-green.txt`; F2 HIGH (product: Setup `x` archived the hidden board selection past the guard) → batch STOPPED, operator ruled "Corregir en el 002", fixed RED-first (`inc002-f2-red.txt`); F3–F7 test arms, F10, N1, N4 folded; F8 → BACKLOG, F9 declined (D-513) · round 2 (frozen r2) OK to advance; R2-1 MEDIUM (tests only: no markup-title arm for the refusal toast) and R2-2 NIT → increment 003's tests · no HIGH open |

---

## 5 · Risks

- Grouped kanban at 118 shows 7 of 8 `◂` (a high-band card keeps its project tag, A-3): the mark is in its details.
- Render cost grows quadratically on boards of thousands of tasks (F8, BACKLOG); real views page their rows.

## 6 · Pending items / spec deviations

- R2-1, R2-2 → increment 003's tests. F8 → BACKLOG. `L` (named by the help and the refusal text) lands in increment 003.

## 7 · Suggested next task

Increment 003 — `L`, the picker, the details section, the project-archive guard, README.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 23 new nodes |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | TC-501..503, 517, 518 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 (one miss named) |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | round 2 OK to advance |
| 7 | No file from another lane | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen |
| 9 | Coverage on disk | all | ✓ | `pytest --collect-only tests/test_links.py` → 24 |
| 10 | Load-bearing emptiness | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 21/21 |
| 12 | **Instrument RED-proof** | all | ✓ | 2 |
| 13 | **Correction population** | all | ✓ | 1 |
| 14 | **Emitted-form assertion** | all | ✓ | 3 |
| 15 | **Independent review** | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** | all | ✓ | 9 |

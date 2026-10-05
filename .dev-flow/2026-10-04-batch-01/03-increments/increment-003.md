# Increment 003 — HLR-502, HLR-503, HLR-504 (LLR-502.1, LLR-502.2, LLR-502.4, LLR-503.1, LLR-504.1) · `L`, the picker, the details section

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal). Mode
> `core`, language `en`. Revision 2 (frozen r2): code review round 1 BLOCK-UNTIL F1 (HIGH,
> product — the batch STOPPED, the operator ruled "Corregir en el 003" and amended the standing
> authorization) and T1, T2 (HIGH, tests/evidence — folded under the test-only rule); round 2 OK.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-502, LLR-502.1, LLR-502.2, LLR-502.4; HLR-503, LLR-503.1; HLR-504, LLR-504.1 (the project archive); amendments A-5, A-6; D-509, D-522, D-523, D-525 |
| Acceptance | AT-502, AT-504, AT-505 (project arm) · white-box TC-507..510, TC-513, TC-517, TC-502 (off-board arm) · unit `link_refusal`, `link_hint`, `loopers_of`, `link_candidates`, `project_archive_refusal` |
| Agent | `software-dev` |
| Date | `2026-10-04` |

---

## 1 · What changed

**`L` makes the selected task wait on another one, from a picker; the details view lists and
edits a task's links; archiving a project others wait on is refused.** `LinkPicker` (replacing the
retired `BlockerPicker`): "‹title› waits on…", a filter, "N of M open", "linked now", a create row,
then the waiter's project first and the rest by due — each a two-line row with its timing hint (the
one measure), "✓ linked (↵ removes)" on a linked one, and a loop row disabled with its path; the
highlight starts on the first candidate; the loop set is computed once per open. The app adds a
link only when `link_refusal` allows (self, closed, loop — named, long paths shortened), removes
one, each one undo step, and creates a task to wait on (waiter's project, first phase, no dates;
refused on a one-phase board). `TaskDetails` gains the dependency section: `Waits on` (each
predecessor's own state — open, done, archived — and "◂N open of M"), `Unblocks` (direct rows and
disabled `└` chain rows, "▸N direct · K in chain"), the conflict lines, and on its heading the keys
`L link · tab links · x remove · ↵ jump` (A-5: the title row the operator accepted stays); `tab`
moves between the box and the list; `x` removes the highlighted link in its direction; `↵` jumps
(clearing a hiding focus or search; saying so when the view cannot draw the task). The project
manager refuses to archive a project while an open task outside it waits on one of its tasks,
before its confirm and again at `yes`. README: the `L` row, `b` as the outside block, the Links
section and the migration's restore path. `L` is bound in the primary layer and painted at 80
columns with no key dropped.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/keymap.py` | source | LLR-502.1 | `L` → `link` |
| `taskboard/models.py` | source | LLR-502.1, LLR-502.2, LLR-504.1 | `link_refusal`, `link_hint`, `LinkCandidate`, `loopers_of`, `link_candidates`, `project_archive_refusal` |
| `taskboard/app.py` | source | LLR-502.1, LLR-503.1 | `action_link`, `open_link_picker`, `_on_link_picked`, `_ask_done`, `link_tasks`, `unlink_tasks`, `_create_and_link`, `jump_to` |
| `taskboard/modals.py` | source | LLR-502.2, LLR-503.1, LLR-504.1 | `LinkPicker` (replacing `BlockerPicker`); the `TaskDetails` section and keys; the `ProjectPicker` guard |
| `README.md` | doc | | the key table, `b`, Links and blocking, the migration |
| `tests/test_link_picker.py` | test | HLR-502, LLR-502.1, LLR-502.2 | NEW: TC-509 ×3 (oracle pasted from `p1-tables.txt`), TC-507 ×2, TC-508, TC-510 ×2, AT-502 |
| `tests/test_details_links.py` | test | HLR-503, LLR-503.1 | NEW: TC-513 ×4, AT-504 |
| `tests/test_links.py` | test | HLR-504, LLR-504.1, LLR-501.1 | AT-505's project arm; TC-517 ×2 (inside waiters; markup refusal R2-1); TC-502 off-board arm (R2-2) |
| `tests/test_markup_sites.py` | test | LLR-502.2 | the `LinkPicker` S1 arm (in AT-401) |
| `tests/test_colour_budget_app.py` | test | LLR-502.1 | the key-bar pins with `L` (T1) |
| `tests/test_link_migration.py` | test | LLR-501.1 | TC-518 measured in CPU time (T1) |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ |
| Test files | 6 (uncapped) |
| Doc files | 1 (`README.md`; records: A-5, A-6, LED .16, .17) |

- ⚠ **At 4 source files:** `L` is one gesture over four seats — the key (`keymap.py`), its rules (`models.py`), its actions (`app.py`) and its two screens (`modals.py`); cutting the picker from the details section would have shipped a section whose `L` opens nothing.

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_link_picker.py tests/test_details_links.py tests/test_links.py tests/test_markup_sites.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-507 (refusal), TC-509 ×3, TC-517 (project unit arm) | in the 41 below |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-507 ×2, TC-508, TC-509 ×3, TC-510 ×2, TC-513 ×4, TC-517 ×2, TC-502 | 15 passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-502, AT-504, AT-505 (project arm) | 3 passed |

Gate run on frozen r2: `python -m pytest -q -p no:cacheprovider` → **2281 passed, 1 failed in 408.93 s**
(`evidence/inc003-gate-r2.txt`); the one failure is `test_win_clipboard_roundtrip`, whose SETUP message
names the environment (Windows refused `Set-Clipboard`) — the known flake (G-011), not this code.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | increment 003's tests on increment 002's frozen r2 product (hashes matched): `test_link_picker.py` cannot import `LinkPicker`, TC-513 and AT-504 FAILED, AT-505's project arm FAILED, AT-401's picker arm FAILED (`evidence/inc003-red-on-inc002.txt`); F1's test FAILED before its fix — `tw4` painted `done` (`evidence/inc003-f1-red.txt`, on the r1 product plus the r2 test folds, modals.py `9ce401c7…`; the reviewer reproduced F1 on frozen r1 itself) |

| Field | Value |
|---|---|
| **Mutation verdicts** | r2: **21 of 21 KILLED** (`evidence/inc003-mutations-r2.txt` + P8 re-anchored in `inc003-mutations-r2b.txt`; spec `mutants_inc003_r2.json`): P1 closed predecessor · P2 loops · P3 long path · P4 order · P5 done offered · P6 loop unmarked · P7 hint off by a day · P8 inside waiters · P9 project unguarded · P10 highlight on create · P11 loop selectable · P12 chain selectable · P13 wrong direction · P14 app skips refusal · P15 unlink not undoable · P16 created in the Inbox · P17 jump keeps a filter · P18 tab stuck · P19/P20 F1 · P21 F3. r1: 15/18 (P8, P14, P17 SURVIVED — arms added). Not killed by any mutant here: the F4 one-phase guard (R2-2) — its arm lands with increment 004's tests |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments: `battery.py` reported P8/P14/P17 SURVIVED and P1 `MISMATCH` (its own newline-translating restore, fixed to byte-exact I/O with anchors following each file's line endings — `app.py`, `modals.py`, `keymap.py` are CRLF, `models.py` LF); TC-513's closed-waiter arm FAILED before F1's fix |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 4 artifacts asserted in their emitted form: the picker's option prompts (`prompt.plain`), the details' `#deps-list` rows and heading (`render()`), the toasts (`str(toast.render())`), the saved board file (AT-502, AT-504) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `inc003-gate-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-gate-r2.txt` | `610b3445c1a7c95df3f9feca5702642de7042dcfb198d8fdf2af4e7a97840ebb` |
| `inc003-gate-r1.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-gate-r1.txt` | `f9f08fd35511c0b2d6bcb36768791795c693bc726d94aa4533619b449c7adc4f` |
| `inc003-green-r2pre.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-green-r2pre.txt` | `97ec8e8b2ad077a961dd9838fe4adfbf8a3d828d6b995fa07fbb5b7eedc716c0` |
| `inc003-red-on-inc002.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-red-on-inc002.txt` | `63853a54ffb1f21aaebd1830cf7443a0a01ad5fc3a0f78708fc80a0864b24451` |
| `inc003-f1-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-f1-red.txt` | `c282e9b6683ccfb029c39607d6d670f93d9f8697e8e8da35032cc7892cbbd2ad` |
| `inc003-mutations.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-mutations.txt` | `b478fb76747b6e0534d04676c5519114c79eafe53e30f0dcf1cae824add35865` |
| `inc003-mutations-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-mutations-r2.txt` | `95de954e9e8c00e2d6443be565bc64aa3a967c0c86f4b79c6f7c971154484f08` |
| `inc003-mutations-r2b.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-mutations-r2b.txt` | `359122c35a14babb405155f83f41006e086e66d18e16fe1cf7425261a686231d` |
| `mutants_inc003_r2.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc003_r2.json` | `34a57a8c80e7c6c6fb957ef931d403010d0c5ddb3a9a8b26aef8e08df8bd2862` |
| `inc003-frozen-r2.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc003-frozen-r2.sha256` | `2f14f992d27bc3021f5f2b3f56a2f0232969255c40036692d6e88a1b7eeb5f29` |
| `battery.py` | `.dev-flow/2026-10-04-batch-01/evidence/battery.py` | `a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb` |

| Field | Value |
|---|---|
| **Evidence files** | 11 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no picker row offers a loop", "no key is dropped from the bar" |
| If the result is an ABSENCE, what made the search wide enough | loops: `loopers_of` agrees with `loop_path` on 300 random boards (reviewer probe); the bar: `key_bar_plain` at 80 for kanban and gantt checked for a `+N` count (TC-508) |
| Synthetic instance of the absent case | P6, P11 (a loop offered / selectable) KILLED |
| **Positive control for every probe that returned an ABSENCE** | P6, P11 |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 `grep -rl` over `tests/` for `BlockerPicker`, `TaskDetails`, `#details-box`, `ProjectPicker`, `KEYMAP`/key bar strings, `README` — `test_markup_sites.py` (picker arm), `test_readme.py`/`test_keymap.py` (green with the README row), `test_colour_budget_app.py` (TC-203's bar pins — found by the gate run, not the symbol grep: named as a census miss, fixed under T1), `test_details_grid.py`/`test_details_markup.py` (green: the title row unchanged, A-5); B2 0 moves; B3 no goldens; B4 the saved board (AT-502, AT-504 re-read it); A3 `link_candidates`, `loopers_of` read only by `modals.py` |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "`b` no longer links; `L` does" — population `grep -rn "BlockerPicker\|blocker" taskboard tests README.md` before the first edit: `modals.py` (class), `app.py` (already gone in 001), `test_markup_sites.py` (arm), README (row and section); all edited; `grep BlockerPicker taskboard/` → 0 (TC-508) |

### Signed-balance test ledger

`post = base − deleted + added` → `2282 = 2265 − 0 + 17` ✓ (9 in `test_link_picker.py`, 5 in `test_details_links.py`, 3 in `test_links.py`; the S1 picker arm lives inside AT-401; 2282 = 2281 passed + the clipboard flake).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · round 1 BLOCK-UNTIL F1, T1, T2: F1 HIGH (product: a closed task's open predecessors painted `done`) → batch STOPPED, operator ruled "Corregir en el 003" and amended the authorization ("Sí, solo en el incremento en curso"), fixed RED-first; T1 HIGH (tests/evidence: stale key-bar pins, a wall-clock bound under load) and T2 HIGH (tests: the app's refusal untested) folded under the test-only rule; F2–F7, T3–T6, N1 folded · round 2 (frozen r2) OK to advance: F1, T1, T2 verified on the diff with mutants; R2-1 (evidence: a wrong line-ending claim, P8's anchor, the r2 runs) answered here; R2-2 (the one-phase guard untested) → increment 004's tests; R2-3 → amendment A-6; R2-4 NIT · no HIGH open |

---

## 5 · Risks

- In 003, `L` on the gantt opens the picker; the gantt link mode is increment 004 (README already describes it).
- The picker lists every open task; on a board of thousands the list is long (filtering narrows it).

## 6 · Pending items / spec deviations

- R2-2: a one-phase-board arm for the create guard (increment 004's tests).
- Contract size: 55.6k characters vs the 54k budget (`V26` notice, declared at close).

## 7 · Suggested next task

Increment 004 — the gantt link mode (D-A).

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ⚠ | 4 / 4, reason in §2 |
| 2 | Tests written in this same increment | all | ✓ | 17 new nodes |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | TC-507, TC-509, TC-517 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 (one miss named) |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | round 2 OK to advance |
| 7 | No file from another lane | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen |
| 9 | Coverage on disk | all | ✓ | `pytest --collect-only` → 41 in the three files |
| 10 | Load-bearing emptiness | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 21/21 |
| 12 | **Instrument RED-proof** | all | ✓ | 2 |
| 13 | **Correction population** | all | ✓ | 1 |
| 14 | **Emitted-form assertion** | all | ✓ | 4 |
| 15 | **Independent review** | all | ✓ | `code-reviewer` |
| 16 | **Evidence files** | all | ✓ | 11 |

# Increment 004 — HLR-605 (LLR-605.1..605.4) · an existing board is offered milestones once, safely

> **Where this lives:** the repo, next to the diff — `.dev-flow/2026-10-04-batch-02/03-increments/increment-004.md`.
> Template `templates/increment-template.md` (rev100); notice convention `⚠` notice · `✗` block · `✓` with evidence.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-02` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-605; LLR-605.1, LLR-605.2, LLR-605.3, LLR-605.4; D-608..D-612, D-615..D-618, D-620, D-621, D-625; LED .9 |
| Acceptance | AT-604, AT-605, AT-606 · white-box TC-614..TC-617 · the seam controls |
| Agent | `software-dev` (this runtime) |
| Date | `2026-10-05` |

---

## 1 · What changed

**An existing board is offered milestones once (M-3 as a migration).** As the last step of start,
a readable board without the offer's mark is checked for candidates — open tasks with a readable due
whose start equals it (one-day, pre-checked) or is empty (due-only, unchecked). With none, the board
is marked silently. Otherwise a centred offer lists them in two groups, each row with its project, its
date and how many open tasks wait on it; `space` toggles, `↵` converts exactly the checked candidates
(re-read at that moment; any that stopped being one are counted, not converted), `esc` converts none
— "not now — won't ask again". Either answer marks the board. Converting reads the board file's bytes
once, writes them to `<board>.pre-milestones` and a log to `<board>.milestones-log` (both by exclusive
create, never over a file), sets the flags (start = due), the mark and saves atomically, says
"Milestones: N converted · backup ‹name› · u undo"; `u` reverts the conversion in one step and keeps
the mark. Any failure restores the board in memory first, removes this run's files best-effort,
leaves the file untouched and unmarked, says why, and the app keeps running (the offer returns next
start). A board this version seeds carries both marks and is never offered. The suite's seam
(`tests/conftest.py`) starts every unmarked test as if its board had answered the offer.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-605.1, LLR-605.2, LLR-605.3 | `Board.load` seeds both marks; `MILESTONES_MIGRATION`, `MILESTONE_BACKUP`, `MILESTONE_LOG`, `MILESTONE_LOG_NOTE`; `milestones_marked`, `milestone_candidates`, `MilestoneConversion`, `run_milestone_offer` |
| `taskboard/app.py` | source | LLR-605.3 | `_offer_milestones` (on_mount's last step), `_on_offer_answered`, the `milestones` undo branch |
| `taskboard/modals.py` | source | LLR-605.4 | `MilestoneOffer` (`#offer-list`), `open_dependents` import |
| `README.md` | doc | | the one-time offer paragraph |
| `tests/conftest.py` | test | HLR-605 | NEW: the suite seam (D-611): `taskboard.app.milestones_marked` answers True unless `milestone_offer` |
| `tests/test_milestone_offer.py` | test | HLR-605, LLR-605.1, LLR-605.2, LLR-605.3, LLR-605.4 | NEW: TC-614..TC-617, AT-604..AT-606 (37 nodes) |
| `tests/test_milestone_offer_seam.py` | test | HLR-605 | NEW: the two seam controls |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 1 (outside the count) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_milestone_offer.py tests/test_milestone_offer_seam.py
python -m pytest -q -p no:cacheprovider tests/test_markup_census.py tests/test_link_migration.py
python -m pytest -q -p no:cacheprovider          # the gate
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | TC-614 (candidates, exclusions, the mark table ×8) | passed |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-615 (9 + 3 failures), TC-616 (10), TC-617 (5), seam controls (2) | passed |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | AT-604, AT-605, AT-606 | passed |

Gate run on frozen r2: `python -m pytest -q -p no:cacheprovider` → **2485 passed, 1 failed** in 470.77 s — the one failure is `test_win_clipboard_roundtrip`, the known environmental clipboard flake (G-011) (`.dev-flow/2026-10-04-batch-02/evidence/inc004-gate-r2.txt`). r1 (superseded by the review folds): 2480 passed, 1 failed (the same flake) (`inc004-gate-r1.txt`). The larger failure counts in the cited evidence come from the deliberately failing transcripts (the batteries and the RED captures), never from a gate run.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| **RED counterfactual** | the r2 arms on the r1 product: 4 of 5 RED (`inc004-r2-red.txt`; the identity-picker arm is an ordering pin) → `inc004-r2-green.txt`; and the r1 tests on the increment-003 product, reconstructed in an export and proven by hash (`models.py` 221276da = 001 r3, `app.py` da16dda6 and `modals.py` f541ccc0 = 003 r2), the new names stubbed and the export's seam made tolerant: 22 of 33 arms RED (`evidence/inc004-red-on-inc003.txt`); the 11 GREEN are labelled: the 8 mark-table arms ran the oracle's own stub there (the product function is absent — battery O3 covers the product), and 3 absence pins (no offer on an unreadable load; a read-only board says nothing; the unmarked seam control) |

| Field | Value |
|---|---|
| **Mutation verdicts** | **23 of 23 KILLED** at r2 (`evidence/inc004-mutations-r3.txt`, spec `mutants_inc004_r3.json`; the r1 battery built by `mk_mutants_inc004.py`) — OD1 the due not restored on failure · OD2 `u` without the due · OD3 the log's raw start · OR1 the title not cut · OR2 the colour as the row's base style, and the 18 of r1: , per resolved node, every restore hash OK: O1 a start ≠ due task as due-only · O2 board order · O3 the mark read with `bool()` · O4 the backup not the file's bytes · O5 no mark · O6 cleanup not best-effort · O7 a failure leaves the flags on · O8 a chosen non-candidate converted · O9 a seeded board unmarked · O10 a no-candidate board unmarked · O11 no one-step undo · O12 the toast hides the ineligible count · O13 a stale keys row · O14 `↵` returns every row · O15 `esc` converts every row · O16 the list unbounded · O17 a failure keeps the mark · O18 no offer at start. r1: O12 SURVIVED (`inc004-mutations.txt`) → the TC-616 ineligible arm; 18/18 at `inc004-mutations-r2.txt` |

### Instrument RED-proof

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments: the battery (O12 reported `SURVIVED` at r1); the reconstruction of the base product (its hashes compared against the 003 freeze before any arm ran); the census plugin `p4_offer_census.py` (its `offers_in_marked_nodes` counts the marked tests' offers — a non-zero positive control) |

### Emitted-form assertion (C-42)

| Field | Value |
|---|---|
| **Emitted-form assertion** | 5 artifacts in their emitted form: the saved board (re-read JSON), the backup (its bytes), the log (re-read JSON), the painted offer (compositor strips), the toasts (`Toast.render()`) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| inc004-red-on-inc003.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-red-on-inc003.txt | 45b45bc7e01e381e9711adc1aae6352e0a3242da9307fc43f27e292796ff22f6 |
| inc004-r2-red.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-r2-red.txt | bd42f1c76d316c973118d23ec375ae3be24e3bfc74ec85e32a40e7b27cd19853 |
| inc004-r2-green.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-r2-green.txt | d8763c990c1d90492c4293312d37275582bc158df52645f0eee2c6cd4cbe3d67 |
| inc004-mutations.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-mutations.txt | f87eceb886e15e65647eb36bf522cbb644d21665f9502096d907e7b1e3a3efbc |
| inc004-mutations-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-mutations-r2.txt | 64bf43f4db9f512531510b825deede2965783b81ca4f9387e2f3844ed49e091d |
| inc004-mutations-r3.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-mutations-r3.txt | 60b494c7ebafbe74705a355640a3ea372c49170af146db92a75545ce048b603d |
| mutants_inc004.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc004.json | 46de55e498687a7ac098b50f0827e4c2a5c69956e2f1de6d852b8029c293b163 |
| mutants_inc004_r2.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc004_r2.json | a3b3cd79c9c21b269b171d9f58386920b1bc41c9ca9ffd0da61fdc3133f0ec17 |
| mutants_inc004_r3.json | .dev-flow/2026-10-04-batch-02/evidence/mutants_inc004_r3.json | c9bcd6a05933bbd55de4ad29b7292c429fefaf9f875a4beddb133108ecee5266 |
| mk_mutants_inc004.py | .dev-flow/2026-10-04-batch-02/evidence/mk_mutants_inc004.py | 4da60f156335cd8645ad7581c1e78fe0d0a32ac343a17c97327d60dc83b127ca |
| battery.py | .dev-flow/2026-10-04-batch-02/evidence/battery.py | a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb |
| make_export.sh | .dev-flow/2026-10-04-batch-02/evidence/make_export.sh | 2de30a0c31d7a484499ad4226cf49417f619ccf616a3978dcbbcb4c32d1fe57a |
| inc004-frozen-r1.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc004-frozen-r1.sha256 | 4cc02402ce04f0c88eda487ca874637b2bdde441058ba3cfb398f2136bdb8852 |
| inc004-frozen-r2.sha256 | .dev-flow/2026-10-04-batch-02/evidence/inc004-frozen-r2.sha256 | dcf7024e5631d8b03e2b75c2d526b3d30488022b71e31d6fe2981ed0a4c321c1 |
| inc004-gate-r1.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-gate-r1.txt | 210970f97a620bbaffa63717acc7d042d825ef21a92adcef57fa5bb49b759be3 |
| inc004-gate-r2.txt | .dev-flow/2026-10-04-batch-02/evidence/inc004-gate-r2.txt | 6e8d805ca2fdf05c3986398aed99f8630cbf8a654d27a7ce2409725a2bc151c9 |

| Field | Value |
|---|---|
| **Evidence files** | 16 artifacts at `artifact_homes.evidence`, cited with the digests of their stored bytes (home paths redacted before hashing) |

### Load-bearing emptiness (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no unmarked test sees the offer" (the seam) |
| If the result is an ABSENCE, what made the search wide enough | the census re-run over the whole suite (every app start, `p4-offer-census.json`) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `tests/test_milestone_offer_seam.py` (both directions) |
| Synthetic instance of the absent case | the marked seam control on the same board: the offer opens |
| **Positive control for every probe that returned an ABSENCE** | `offers_in_marked_nodes` > 0 in the census |

### Reverse census — trigger family B

| Field | Value |
|---|---|
| **Reverse census** | 5 probes. B1 `grep -rln "on_mount\|Board.load\|action_undo\|_undo_stack\|migrations\|load_report\|TaskboardApp(" tests/` → every app-started test (372 at P1) — the seam keeps their offer step a no-op; the full suite below; `test_markup_census.py` (TC-401) reddened on the first draft (helper names and bindings it cannot prove `Text`) and passes after conforming (renamed `_offer_row`/`_offer_keys`, plain `options = []`, `Text(..., no_wrap=True)`); `test_link_migration.py`, `test_rescue.py` green with the seeded marks. B2 not fired. B3 not fired. B4: the saved board, backup and log are consumed by the next start, the operator's manual restore and a teammate's pull — AT-604 (a fresh app re-reads the file), TC-615 (a pull sees no extra user). A3: `Board.load` seeds a settings dict (no caller passes settings for a seed) |

### Correction population

| Field | Value |
|---|---|
| **Correction population** | none — no claim corrected (the late `#f-milestone` IFC block is an addition, LED .9) |

### Signed-balance test ledger

`post = base − deleted + added` → `2486 = 2447 − 0 + 39` ✓ (37 in `test_milestone_offer.py`, 2 in `test_milestone_offer_seam.py`).

---

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named agent with `agents/code-reviewer.md` · OK-WITH-NOTES at r2, 0 HIGH: r1 O-1 MEDIUM (product: a long title pushed the row's project and date off with no `…`), O-2 LOW (the box colour as the row's base style), O-3 LOW (the identity-picker order unpinned) and a NIT (the undo wording) folded RED-first (LED .10); r2 all DISCHARGED (O-1 re-probed at 80/60/140 and on resize). `security-reviewer` — spawned with `agents/security-reviewer.md` · r1 PASS-WITH-NOTES: S-1..S-9 of P2 verified in code and by probes; S4-1 LOW (a canonicalised due not restored by `u` or a failure) folded RED-first; r2 PASS, 0 open (the operator's safeguard verified in code: nothing unchosen converted, backup first by exclusive create, log, `u`, never twice, fail-closed) |

---

## 5 · Risks

- The seam makes every unmarked test start as if its board had answered the offer: a regression that offers on a MARKED board is caught only by the offer's own tests (TC-616, AT-605) — the census shows 0 offers in unmarked nodes.
- An unreadable board is still saved over by the shipped renumber notice (B1 security S-13, BACKLOG); the offer adds nothing there (no offer, no mark).
- The offer covers the team identity picker until it is answered (D-615).

## 6 · Pending items / spec deviations

- LED .9: the `#f-milestone` IFC block belonged to increment 001.

## 7 · Suggested next task

P4 validation; then the close.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence |
|---|---|---|---|---|
| 1 | ≤4 source files | all | ✓ | 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 39 new nodes |
| 3 | Layer 0 where the criterion applies | `core` · `full` | ✓ | `milestone_candidates`, `milestones_marked`, `run_milestone_offer`: TC-614, TC-615 |
| 4 | **RED counterfactual** | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none declared |
| 9 | Coverage claims verified on disk | all | ✓ | `pytest --collect-only` → 37 + 2 |
| 10 | Load-bearing emptiness declared | all | ✓ | §4 |
| 11 | **Mutation verdicts** | all | ✓ | 18/18 |
| 12 | **Instrument RED-proof** | all | ✓ | §4 |
| 13 | **Correction population** | all | ✓ | none |
| 14 | **Emitted-form assertion** | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** | all | ✓ | §4 |

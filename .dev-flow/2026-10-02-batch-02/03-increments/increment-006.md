# Increment 006 — HLR-207, HLR-203 · P4 iterate-to-fix: AT-207 one node, the record corrected

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Flow pinned to rev98.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-02` |
| Increment | `006` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-207 (AT-207 realisation, C-18); HLR-203 (amended, LED .19) |
| Acceptance | AT-207 (one parametrised node) · TC-205 / AT-203 re-derived unchanged |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**P4's qa pass failed two blockers, both on AT-207, and this increment fixes them without touching
product code.** AT-207 was realised by two test functions (C-18 wants one node): they are now one
node parametrised over the two terminal sizes, and the 118×30 arm gained the fold checks — which
are RED on the base tree too — while its "at most one upward move" bound alone stays a regression
pin. Increment 005's packet claimed mutants had killed the 118×30 walk; none had — the claim is
corrected, as is the list of mutants that did kill the legend pin (S2, S4, S6). HLR-203 is
amended (Before/After, LED .19) to name the seat it governs — `reldue_token` — and to declare the
Focus view's `date_chip` seats outside it (the walkthrough's UXV2-1); increment 001's node
breakdown is corrected.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `tests/test_gantt_polish.py` | test | HLR-207 | the two AT-207 functions → one node over `((80,24),2)`, `((118,30),1)`; `_walk` removed |

Record only (no trace owed, `.dev-flow/**`): `01-requirements.md` (HLR-203, §6.5), `01-requirements-ledger.md` (LED .19), `PLAN.md` (D-209 row), `03-increments/increment-005.md` (§4 two rows), `03-increments/increment-001.md` (§2 breakdown).

| Count | Value |
|---|---|
| **SOURCE files** | **0 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 (record edits only) |

## 3 · How to test

```bash
python -m pytest -q tests/test_gantt_polish.py -k AT_207
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | n/a — no unit changed | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | n/a — no TC changed | — |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-207 (2 arms of one node) | 2 passed |

Suite after the merge: `python -m pytest -q -p no:cacheprovider` → **1677 passed in 187.77s, exit 0**
(`evidence/inc006-suite.txt`); a docstring-only edit followed it, and the P4 gate re-run is the run
of record.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment-004 tree with the merged node; then mutant W1 on the increment tree |
| Where it ran | scratch exports |
| Transcript | `evidence/inc006-red.txt` (both arms FAILED); `evidence/inc006-mutations.txt` (W1: 2 of 2 arms red) |
| Restore proven by | sha256 `views.py` `a4688ae7c1788b66…` (OK) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 2 |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | both arms of the merged AT-207 RED on the increment-004 tree (Website folds at `tm6` at both sizes) · `evidence/inc006-red.txt` · W1 (`previous` ignored) reddens both · restore digest in `evidence/inc006-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 1 of 1 KILLED (`evidence/inc006-mutations.txt`, spec `mutants_inc006.json` — its `why` text was reworded after the run (code review F4/N2); the mutation's old/new/nodes bytes are unchanged, so the transcript's verdict stands): W1, 2 of 2 arms red; the reviewer's own CR-W2 (the previous group offered last) also reddened both |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the merged walk | the increment-004 tree | `▾ Website` absent at `tm6` (both sizes) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 1 instrument, shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted gantt panel | `#board` rows and `line_map` rows through the 24-step walk | 2 passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact, asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-004 tree | `.dev-flow/2026-10-02-batch-02/evidence/inc006-red.txt` | `4465df2997c01ee40bd4e2e0604c699bd96c07102bdb4d02ebc34f74dcd864fe` |
| mutation battery | `.dev-flow/2026-10-02-batch-02/evidence/inc006-mutations.txt` | `6fba7dcf01835cebc9b7eee7f234f818127c7443556f3c66018f018b31ac6ae5` |
| mutant spec | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc006.json` | `da39944316a3ed5a9627acdcb2e45be92be57a76518c7cbc94c2122c708a5483` |
| suite after the merge | `.dev-flow/2026-10-02-batch-02/evidence/inc006-suite.txt` | `4f567b47338f6442ccce91b7b24d4dab240cd599152fcbbe9871f3f4d7c5b331` |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts under the declared home, each cited with its digest |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "AT-207 is realised by exactly one node" |
| If the result is an ABSENCE, what made the search wide enough | `grep -c "def test_AT_207" tests/` = 1; 10 `test_AT_2*` functions for 10 ATs (code review) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `assert "tm6" in ids and "ta1" in ids and len(set(ids)) == 25` |
| Conjunctive criteria: one mutation per conjunct | W1 (fold checks); the up-move bound is a declared pin |
| Synthetic instance of the absent case | the increment-004 tree |
| **Positive control for every probe that returned an ABSENCE** | both arms RED there |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rn "_walk\|test_AT_207" tests/` | none outside the file |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | none | did not fire |
| B4 artifact produced here is consumed elsewhere | none (a test) | did not fire |
| A3 | interface consumed by another module changed | none | did not fire |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes, none fired: a test-only merge |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| AT realised by more than one node | `def test_AT_2NN` functions per AT id | `grep -n "def test_AT_2" tests/*.py` | 11 functions / 10 ids | 1 (AT-207) | none |
| `date_chip` seats named in the HLR-203 exclusion | callers of `date_chip` in `views.py` | `grep -n "date_chip(" taskboard/views.py` (code review F3) | 6 | 6 named | none |

| Field | Value |
|---|---|
| **Correction population** | 2 corrections, each enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1677 = 1677 − 2 + 2` ✓ (two one-node functions → one node of two arms).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` (rev98 snapshot) · round 1: PASS-WITH-NOTES, no HIGH — the merge loses nothing and the 118×30 fold checks are real facts (probed on both trees); F1 MEDIUM (the corrected kill list missed S2), F2 MEDIUM (the §6.5 amendment lacked the full After, Deleted/New and the re-derivation), F3 MEDIUM (the exclusion named one of six `date_chip` seats), F4 LOW ("the 118×30 arm is a pin" overstated), F5 LOW (unreadable param ids) · F1–F4 folded (record-only); F5 deferred (renaming the ids would re-cite every transcript) · round 2: PASS-WITH-NOTES, no HIGH finding — F1–F4 folded and re-read on the unmoved set (After == Statement verified; digests verified); F5 deferred; notes N1–N3 (this cell; the spec's reworded `why`; the BACKLOG entries owed at close) |

## 5 · Risks

- None new: no product file changed.

## 6 · Pending items / spec deviations

- Code review F5 (param ids `[size0-2]`) — cosmetic, BACKLOG at close.
- The six `date_chip` seats outside HLR-203 (ux UXV2-1, LED .19) — BACKLOG at close.

## 7 · Suggested next task

P4 re-validation (gate re-run, qa iteration 2), then P5 close.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 0 / 4 |
| 2 | Tests written in this same increment | all | ✓ | the merged node |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — no unit changed |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | no product file |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | one `def test_AT_207` |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |

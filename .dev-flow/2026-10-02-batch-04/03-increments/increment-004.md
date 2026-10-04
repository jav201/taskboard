# Increment 004 — HLR-403 (LLR-403.1) · the operator's visual verdict: UX-3 and UX-4

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Cut after the batch
> re-opened to P3 (D-422) on the operator's verdict of 2026-10-04. Revision 2: code review F1
> (MEDIUM, a missing pin for the other modals' titles) folded into TC-420, battery r2; round-2 NIT
> (name that pin in TC-420's docstring and LLR-403.1) folded, frozen r4.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-04` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-403 (threshold), LLR-403.1; D-406, PV-1, UX-3, UX-4; §6.5 amendment A-7 |
| Acceptance | AT-406 (unchanged, re-run) · white-box TC-411, TC-420, TC-421 · unit `n/a — a stylesheet rule has no unit` |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-04` |

---

## 1 · What changed

**The details view now has one blank row under its title instead of two above it, and its label
column is 10 cells wide instead of 20.** The operator's verdict on the increment-003 captures
(`evidence/operator-verdict-provisional.json`): PV-1 accepted, UX-3 and UX-4 applied. One scoped
stylesheet block: `#details-box .modal-title { margin: 0 0 1 0; }` and `#details-box .modal-grid {
grid-columns: 10 1fr; }`.

Root cause of the old spacing (`evidence/inc004-probe.txt`, the computed margin read in the probe):
`.modal Label` (class + type) outranks `.modal-title` (class). In Textual its `margin-top: 1`
replaces the title's whole margin, so `.modal-title { margin-bottom: 1 }` never reached the title.
That left two rows above it (box padding plus the margin) and none below. The id-scoped rule
outranks `.modal Label`.

The 89-character project name now wraps over 2 rows at 80×24 instead of 3. Values start at x 34 / 16
instead of 44 / 26. No row is added: the short-name box keeps its height. `TaskDetails.compose`
is untouched because the spacing is pure CSS.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/taskboard.tcss` | source | LLR-403.1 (amendment A-7) | the scoped title margin and label column, with a comment naming the cascade |
| `tests/test_details_grid.py` | test | HLR-403, LLR-403.1 | NEW TC-420 ×2, TC-421 ×2; TC-411's long-value arm at 80×24: 3 → 2 rows |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 (records: `01-requirements.md` amendment A-7, ledger LED .13, `PLAN.md`, `state.json`) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_details_grid.py tests/test_details_markup.py
python -B .dev-flow/2026-10-02-batch-04/evidence/inc004_probe.py "$(pwd)"
python -B .dev-flow/2026-10-02-batch-04/evidence/capture_details.py "$(pwd)" after2 .dev-flow/2026-10-02-batch-04/evidence/captures
```

Manual check: `taskboard`, select a task, `enter`. Expect one blank row above the title and one
below it, then `Project`. The values start 11 cells right of the labels.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `n/a — one stylesheet rule, no unit of code` | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-411 ×6 (the long-value arm amended), TC-420 ×2 (title gap from the painted rows; an edit modal's title keeps its two rows above, F1), TC-421 ×2 (painted value offset 11 for the five labels with the long name, the five painted in order, `ProjectModal` offset 21) | 10 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-406 (unchanged; it finds the value column from the painted row) | 1 passed |

Gate run on frozen r3 (the tree after the F1 fold): `python -m pytest -q -p no:cacheprovider` → **2218 passed
in 398.62 s, exit 0** (`evidence/inc004-gate-r3.txt`). Earlier: r1 2218 passed, exit 0 (`inc004-green.txt`).
Frozen r4 differs from r3 only by TC-420's docstring; on r4 the details-grid, details-markup and edit-window
files → 91 passed (`evidence/inc004-details-r4.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | (a) increment 003's stylesheet with this increment's tests (the live tree before the rule, hashed in `inc004-red-tree.sha256`); (b) the stylesheet battery |
| Where it ran | (a) the live checkout before the edit; (b) a scratch export (`git archive` + the working tree's package and tests) |
| Transcript | `inc004-red-on-inc003.txt`: 5 failed / 6 passed — TC-420 ×2 `(2, 3, …)` (two rows above, none below), TC-421 ×2 `[21, 21, 21, 21, 21]`, TC-411 long arm at 80×24 `(1, 3) == (1, 2)` |
| Restore proven by | the battery's per-mutant sha256 check (all OK) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 11 (the grid file) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | the 6 the rule does not move: TC-411 cells ×2, the long arm at 140×40 (2 rows either way), the edit-modal pins ×2, AT-406 |

| Field | Value |
|---|---|
| **RED counterfactual** | increment 003's stylesheet with this increment's tests: 5 RED on the intended assertions (`evidence/inc004-red-on-inc003.txt` sha256 `56fd740a…`); restore digests in `inc004-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | r2: 6 of 6 non-equivalent KILLED, 1 equivalent (`evidence/inc004-mutations-r2.txt` sha256 `cf9e1256…`, `mutants_inc004_r2.json`; r1 5 of 5 in `inc004-mutations.txt`). U7 (code review F1): the title rule widened to `.modal .modal-title` → TC-420's edit-modal arm RED. r1: U1 no row under the title, U2 a row added rather than moved, U4 the 20-cell column back (TC-421 and TC-411's long arm), U5 a 9-cell column (off by one), U6 the column rule widened to every `.modal-grid` (the `ProjectModal` pin). U3 (the longhand `margin-top: 0; margin-bottom: 1` in the same id rule) SURVIVED and is equivalent: the id-scoped rule outranks `.modal Label` either way. It also proved the first comment wrong (it said the shorthand was required), so the comment was corrected in r2 |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `inc004_probe.py` | increment 003's stylesheet (scratch tree, tcss sha256 = `inc003-frozen-r2`) | `above=2 below=0 value_dx=21`, the long name `proj_rows=3` at 80×24 (`inc004-probe.txt`) |
| TC-420 / TC-421 | increment 003's stylesheet | RED (`inc004-red-on-inc003.txt`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown reporting a failure before its pass was believed (table above) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted details view | TC-420 reads the compositor's painted rows inside `#details-box` (blank, title, blank, `Project`); TC-421 measures each label-to-value offset on the painted row | pass at 140×40 and 80×24 |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact asserted against the painted form (table above) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| the operator's verdict | `.dev-flow/2026-10-02-batch-04/evidence/operator-verdict-provisional.json` | `0b3bfdf6f1f29e7522a36188872215255d65ccd3a383884fcd0369fafe4cd3c2` |
| RED on increment 003 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-red-on-inc003.txt` | `56fd740a221f605b4ea322696d20b3e42eb87178f5bcaed951775878c701225c` |
| tree the RED ran on | `.dev-flow/2026-10-02-batch-04/evidence/inc004-red-tree.sha256` | `89c339b3a70af2942c93c810f5bab5b4fedff8122f560a03ede2494b144457c2` |
| geometry before/after | `.dev-flow/2026-10-02-batch-04/evidence/inc004-probe.txt` | `81f20874dd7675138afe6f2ace1496ad25a9c74a3f5440315944627d8eb7034b` |
| the probe | `.dev-flow/2026-10-02-batch-04/evidence/inc004_probe.py` | `5c0325328232ec6b7eb74e21d519a375c73e79e7a45eebd0af769822a6dcdefc` |
| full suite, frozen r1 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-green.txt` | `d68c73b9359fc1648899a90881665b7d4524ca5f9c3248fff7d581b1f83ace25` |
| battery | `.dev-flow/2026-10-02-batch-04/evidence/inc004-mutations.txt` | `bd343e8a4ec8dd442fead8a3dbc22d33ee97d779de8f36a52d4243121d14715f` |
| battery spec | `.dev-flow/2026-10-02-batch-04/evidence/mutants_inc004.json` | `ea4e19f34a797be7a3765456a74df0c7c8ed4e50365633fdb8f5ca2bf863d2ea` |
| battery r2 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-mutations-r2.txt` | `cf9e12566a037954e28c2bce7b8ebdd14d0c74f4668ff97f6e5f788147624359` |
| battery spec r2 | `.dev-flow/2026-10-02-batch-04/evidence/mutants_inc004_r2.json` | `18b1687db7abc3177a18b42d76c9409818b7fadedc9c869161a721722832290e` |
| frozen set r3 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-frozen-r3.sha256` | `6342c83478e93e29e6c707e87a0c49ffcab6a47de121485e3329ccf124c5df8d` |
| gate run, frozen r3 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-gate-r3.txt` | `e32272ff3d4ae4c6ebda73987c65caabf1b6ba91b080b92ab4b0cb300a7968fd` |
| frozen set r4 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-frozen-r4.sha256` | `9e165fd7f64553950b556f862797fac4198437ccbd21079ca78bd84126296d73` |
| details files, frozen r4 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-details-r4.txt` | `00eee10cf248e05665191620bee298123c5fe8040feff223f164b13756a97dc5` |
| frozen set r1 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-frozen-r1.sha256` | `2e01f0f9414e325b274cc764535cba47edc28196a5bf815b1296406411fa416e` |
| frozen set r2 | `.dev-flow/2026-10-02-batch-04/evidence/inc004-frozen-r2.sha256` | `62b8097c63e40fe355e6275354b755523ca078345a4c765492a2b504c9a6e08f` |
| capture after2, 140×40 | `.dev-flow/2026-10-02-batch-04/evidence/captures/after2-details-140x40.svg` | `5039d9765d781bcda842b823a6c8b5d65c2bd0402ea0eb361bd29f5bb25bebda` |
| capture after2, 80×24 long | `.dev-flow/2026-10-02-batch-04/evidence/captures/after2-details-80x24-long.svg` | `fbd4182de8d4d6343a3923cfa9d1e684ed968fa8396479aa1ee57a652b4e2cbc` |

| Field | Value |
|---|---|
| **Evidence files** | 18 artifacts at `artifact_homes.evidence`, each cited with the digest of its stored bytes (table above; the other `after2-details-*` captures and the `.txt` twins sit beside them) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no other modal's title or grid changed" |
| If the result is an ABSENCE, what made the search wide enough | every `modal-title` / `modal-grid` in the package (`grep -rn "modal-title\|modal-grid" taskboard/*.py`): only `TaskDetails` mounts `#details-box` (`modals.py:1168`) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-411's edit-modal pins; TC-421's `ProjectModal` offset 21; TC-420's `ProjectModal` title arm |
| Conjunctive criteria: one mutation per conjunct | title gap (U1, U2), column (U4, U5), scope of each rule (U6, U7) |
| Synthetic instance of the absent case | U6 (the column rule widened) and U7 (the title rule widened) turn the `ProjectModal` pins RED |
| **Positive control for every probe that returned an ABSENCE** | U6, U7 KILLED |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln -e "#details-box" -e "modal-grid" -e "modal-title" tests/` | `test_details_markup.py`, `test_markup_sites.py`, `test_control_bytes.py` (read `#details-box` text), `test_colour_budget_app.py`, `test_edit_window.py`, `test_emoji_picker.py` (other modals' titles): all green in the full suite |
| B2 file moved on disk | `git diff --name-status HEAD -- taskboard tests \| grep ^R` | 0 |
| B3 byte-identical golden captures this source | `ls tests/goldens` | no such directory |
| B4 artifact produced here is consumed elsewhere | the stylesheet is read by the app only | none |
| A3 | interface consumed by another module changed | `grep -rn "details-box" taskboard` | no new address; `#details-box .modal-grid` keeps its declared consumers (A-6) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 with their commands and verdicts: B1 six test files, all green; B2, B3, B4 0; A3 no new address |

### Correction population — enumerated BEFORE the first site was edited

| Field | Value |
|---|---|
| **Correction population** | n/a — no correction across a population; one scoped block added |

### Signed-balance test ledger

`post = base − deleted + added` → by node id `2218 = 2214 − 1 + 5` ✓ reconciles: TC-411's long arm renamed `a_long_value_wraps_under_itself[size1-3]` → `[size1-2]` (one id out, one in), plus TC-420 ×2 and TC-421 ×2. By count that is 2214 − 0 + 4 (qa N1). TC-420's edit-modal title arm (F1) lives inside the existing TC-420 nodes.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · round 1 OK-WITH-NOTES, no HIGH: F1 MEDIUM, tests only (nothing pinned the other modals' titles: `.modal .modal-title` survived) → folded into TC-420 with U7; F2 LOW (validation and close records carry pre-A-7 thresholds) → fixed at the re-close; F3 NIT (x 34 / 16 asserted only as the 11-cell offset) accepted. Round 2 (frozen r3) OK to advance: the F1 fold was verified (the widened mutant KILLED by TC-420 at both sizes), plus one NIT (name the `ProjectModal` pin in TC-420's docstring and LLR-403.1), folded at r4 · no HIGH |

---

## 5 · Risks

- The 10-cell column assumes the five labels: `Priority` (8) is the widest. A longer label would wrap under itself.
- The values keep the dim label tone `#8b98a5` (UX-8, pre-existing, BACKLOG).

## 6 · Pending items / spec deviations

- Amendment A-7 (LED .13). A light P4 over the `after2-details-*` captures, then the re-close of P5.

## 7 · Suggested next task

P4 (light): `qa-reviewer` evaluation and `ux-reviewer` walkthrough over `after2-details-*`.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | §2 |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — a stylesheet rule (§4) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 field |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 field |
| 6 | `code-reviewer` passed — a HIGH blocks | `core` · `full` | ✓ | §4b: round 2 OK, no HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | the edit modals pinned (TC-411, TC-421) |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `inc004-gate-r3.txt` |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 C-55 table |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 field: r2 6/6 + 1 equivalent |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 table |
| 13 | **Correction population** declared | all | ✓ | §4 field (n/a with its reason) |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 table |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 table |

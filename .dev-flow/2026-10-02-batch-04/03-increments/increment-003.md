# Increment 003 — HLR-403 (LLR-403.1) · the details info grid paints its fields

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Revision 2 (code
> review F1 folded under the operator's ruling "Sí, corregir y seguir", 2026-10-03).

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-04` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-403 (LLR-403.1); D-406, PV-1; §6.5 A-6 |
| Acceptance | AT-406 · white-box TC-411 · unit `n/a — a stylesheet rule has no unit` |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-03` |

---

## 1 · What changed

**`enter` on a task now shows its Project, Phase, Priority, Start and Due — one row per field, a long
value wrapping under its own column.** The info grid painted blank on base (P-5): Textual 8.2.8 sizes
an auto-height grid row to the label's one line and the shared `.modal-grid Label { margin-top: 1 }`
ate it (P-9). One scoped stylesheet rule, `#details-box .modal-grid Label { margin-top: 0; height:
auto; }`, fixes it; the edit modals' grids (rows of 3-row inputs) keep their geometry. The details
markup test now reads the project and phase fields off the painted screen, as the other fields.
The look is a provisional visual decision (PV-1), with UX-3 (a gap under the title) and UX-4 (a
narrower label column) open to the operator on the captures.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/taskboard.tcss` | source | LLR-403.1 | `#details-box .modal-grid Label { margin-top: 0; height: auto; }` |
| `tests/test_details_grid.py` | test | HLR-403, LLR-403.1 | NEW: TC-411 ×6, AT-406 |
| `tests/test_details_markup.py` | test | HLR-403 | the project/phase arms read the painted screen |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_details_grid.py tests/test_details_markup.py
python -B .dev-flow/2026-10-02-batch-04/evidence/capture_details.py "$(pwd)" after .dev-flow/2026-10-02-batch-04/evidence/captures
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | `n/a — one stylesheet rule, no unit of code` | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-411 ×6 (cells ≥1 row on the label's row ×2; a long value wraps ×2; edit-modal grid pins ×2) | 6 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-406 (four cases: 140×40; the long name at 80×24 with all five fields painted in order; no dates + blocked; Inbox) | 1 passed |

Gate run (the P4 gate run over the final tree, frozen r2): `python -m pytest -q -p no:cacheprovider` →
**2214 passed in 306.98 s, exit 0** (`evidence/p4-gate.txt`; the clipboard environment test passed this run).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | (a) the base tree `56a1b10` (`git archive`) with this increment's test files; (b) the stylesheet battery; (c) AT-406's visibility clause at 80×12 |
| Where it ran | scratch exports; (c) on the current tree with the test's own helpers (read-only) |
| Transcript | `inc003-red-on-base.txt`: 23 failed / 27 passed — 17 from THIS rule (5 grid nodes, 12 project/phase arms), 6 from the earlier increments' parse fixes (the new payloads on notes, title, image and viewer-title arms; code review F3); `inc003-f1-red.txt`: at 80×12 the old clause True, the new False |
| Restore proven by | the battery's per-mutant sha256 check (all OK) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 50 (7 grid + 43 details) |
| Verdict granularity | per node (`-rA`); AT-406 per case |
| Arms that stayed GREEN | the two edit-modal pins (TC-411, by design: they pin base geometry) and 25 details arms that the earlier increments' fixes or the base already paint |

| Field | Value |
|---|---|
| **RED counterfactual** | the base tree with this increment's tests: 17 RED owed to this rule (`evidence/inc003-red-on-base.txt` sha256 `a2546285…`); AT-406's visibility clause RED at 80×12 (`evidence/inc003-f1-red.txt` sha256 `ee95507c…`); exports discarded (restore n/a), the battery's restore digests in `inc003-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 3/3 KILLED (`evidence/inc003-mutations.txt` sha256 `58807156…`): G1 the top margin back (17 arms RED), G2 `height: 1` (a long value cut: 3 arms RED), G3 the rule widened to every `.modal-grid` (the edit-modal pins RED); AT-406's visibility clause: the old form survived a cut-off field (code review F1), the new form RED at 80×12 |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| AT-406's visibility clause | the details view at 80×12 (two of five fields painted) | old form: no failure (vacuous — code review F1); new form: `False` (`inc003-f1-red.txt`) |
| `capture_details.py` | the base tree | the blank grid captured (`captures/base-details-80x24.txt`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown reporting a failure before its pass was believed (table above) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the painted details view | AT-406 reads the compositor's painted rows inside `#details-box` (label and value on one row, the long name rebuilt from its wrapped rows, every continuation row's first character at the value column) | all four cases pass on the final tree |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact asserted against the painted form (table above) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| gate run, frozen r2 (P4 gate) | `.dev-flow/2026-10-02-batch-04/evidence/p4-gate.txt` | `cb68cdefc96f718ac5588542ba208bee7860132068163d667025f48a20ee0680` |
| RED on base | `.dev-flow/2026-10-02-batch-04/evidence/inc003-red-on-base.txt` | `a2546285f31fb45fea23d4594c22f01c42e18790a3962cf330a8877ea36edb9d` |
| visibility clause RED | `.dev-flow/2026-10-02-batch-04/evidence/inc003-f1-red.txt` | `ee95507c92ae8b98aed0b71f6d481be01826d91cd1a5f0d15dc84b729dfba1c3` |
| battery | `.dev-flow/2026-10-02-batch-04/evidence/inc003-mutations.txt` | `588071565f6ec9883f3c04f16147ea60fcce68f17bf776d7d9cae73a20a9febf` |
| suite on r1 (kept) | `.dev-flow/2026-10-02-batch-04/evidence/inc003-green.txt` | `4093be7c513041c98c6bdc7d88fff12ce4a135227715a80a42d39bf8de92b661` |
| capture before, 140×40 | `.dev-flow/2026-10-02-batch-04/evidence/captures/base-details-140x40.svg` | `8f98cde6f3c17b5ef83799ed008b65452a0e06a54cf53683a6207f3c1fddd013` |
| capture after, 140×40 | `.dev-flow/2026-10-02-batch-04/evidence/captures/after-details-140x40.svg` | `d647c13cb19b17fdbf7418f1998950f6f0914962c1a0a2ff12e8137901848d6c` |
| capture before, 80×24 long | `.dev-flow/2026-10-02-batch-04/evidence/captures/base-details-80x24-long.svg` | `5fff3619b6335d9733d65c731decbb7ed666851d5ea1bc708924b59c3ed146f9` |
| capture after, 80×24 long | `.dev-flow/2026-10-02-batch-04/evidence/captures/after-details-80x24-long.svg` | `a0d172d37a1f70e388a16453f50aa172ab4eac6a6c2a25edd460966efee96770` |
| frozen set r2 | `.dev-flow/2026-10-02-batch-04/evidence/inc003-frozen-r2.sha256` | `4e242ee667437aba62c2a965b84aad286be0d939e1ee0c7fbd78047495f99b72` |

| Field | Value |
|---|---|
| **Evidence files** | 10 artifacts at `artifact_homes.evidence`, each cited with the digest of its stored bytes (table above; the other four captures and the `.txt` twins sit beside them) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no other modal grid changed" |
| If the result is an ABSENCE, what made the search wide enough | every `.modal-grid` in the package (`grep -n "modal-grid" taskboard/*.py` → TaskModal? no: ProjectModal, ClockModal, TaskDetails) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-411's edit-modal pins, docstring "a regression PIN" |
| Conjunctive criteria: one mutation per conjunct | margin (G1), height (G2), scope (G3) |
| Synthetic instance of the absent case | G3 (the rule widened) turns the pins RED |
| **Positive control for every probe that returned an ABSENCE** | G3 KILLED |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln -e "#details-box" -e "modal-grid" tests/` | `test_details_markup.py` (rewritten in place), `test_markup_sites.py`, `test_control_bytes.py` (read `#details-box` text only, green) |
| B2 file moved on disk | `git diff --name-status HEAD -- taskboard tests \| grep ^R` | 0 |
| B3 byte-identical golden captures this source | `ls tests/goldens` | no such directory |
| B4 artifact produced here is consumed elsewhere | the stylesheet is read by the app only | none |
| A3 | interface consumed by another module changed | `grep -rn "details-box" taskboard` | the address `#details-box .modal-grid` gains one consumer, `tests/test_details_grid.py` (A-6) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 with their commands and verdicts: B1 three test files, one rewritten in place, two re-validated green; B2, B3, B4 0; A3 one consumer declared (A-6) |

### Correction population — enumerated BEFORE the first site was edited

| Field | Value |
|---|---|
| **Correction population** | n/a — no correction across a population; one rule added |

### Signed-balance test ledger

`post = base − deleted + added` → `2214 = 2207 − 0 + 7` ✓ reconciles

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · round 1 `BLOCK-UNTIL: F1` (F1 HIGH, test-only: AT-406's visibility clause could not fail; the rule itself confirmed correct — STOPPED and reported; the operator ruled "Sí, corregir y seguir" and amended the standing authorization for test-only HIGHs), F2 MEDIUM (the green file read mid-run — the run completed: 2213 passed + the clipboard environment failure), F3 LOW (declared in §4); round 2 (frozen r2) OK to advance — F1 discharged by re-reading the clause and re-running `inc003_f1_probe.py` (80×12: new clause False), no new finding |

---

## 5 · Risks

- PV-1 is provisional: the compact one-row-per-field look, UX-3 and UX-4 wait for the operator's verdict on the captures.
- The values keep the dim label tone `#8b98a5` (UX-8, pre-existing, BACKLOG).

## 6 · Pending items / spec deviations

- Amendment A-6 (LED .12). PV-1, UX-3, UX-4 to the operator (close record).

## 7 · Suggested next task

P4 — the gate run, `qa-reviewer` evaluation and `ux-reviewer` walkthrough over the captures.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | §2 |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — a stylesheet rule (§4) |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 field |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 field |
| 6 | `code-reviewer` passed — a HIGH blocks | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | the edit modals' grids pinned (TC-411) |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `p4-gate.txt` |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 C-55 table |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 field: 3/3 + the clause RED |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 table |
| 13 | **Correction population** declared | all | ✓ | §4 field (n/a with its reason) |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 table |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 table |

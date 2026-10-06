# Validation — taskboard — Batch 2026-10-04-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.

- **Result:** PASS-WITH-NOTES — 0 blocker gaps. qa-reviewer APPROVE-WITH-NOTES and ux-reviewer APPROVE-WITH-NOTES, 0 HIGH each. Their three MEDIUM findings were test or evidence defects (qa F-1, F-2; ux UXV-1), and all three are folded (§Orchestrator fold). The LOWs went to BACKLOG or to the operator's visual verdict. One environment failure is declared (G-011).
- **Layer 0:** 20 units met the criterion (cyclomatic ≥ 3 or crossing the board-file boundary) · 20 carry a named reddening mutation (KILLED in the battery transcripts cited in §Layer 0; 79 of 79 final-battery mutants KILLED, plus the P4 pair V1, V2)
- **Requirements:** 16/16 pass (4 HLR + 12 LLR) · 0 blocker fails. The one failed node in the close gate is outside every requirement (G-011, environment).
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface, with boundary and negative arms. The surface is `TaskboardApp` driven with real keys via `run_test`; the painted strips, the toasts, and the saved board file, its backup, its log and the pushed team file are re-read from disk. US-604 is OUT (B2b, D-601), so it owes no AT. Note G-002 (qa F-3).
- **Surface-reachability (bidirectional):** ✓ every named input and every named output/deliverable is reached or observed at the surface (matrix below).
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative. The batch superseded no shipped capability. The changed literals (the `KEYBAR_BASE` gantt bar, the editor's widget ids 17 → 18, the kanban header counts) are each in an increment's reverse census and amended in the canon (LLR-001.3).
- **Test ledger:** ✓ reconciles: 2486 = 2306 − 0 + 180, matching the 2486 nodes the orchestrator's close gate collected (2485 passed, 1 failed, `evidence/close-gate.txt`).
- **Evidence checklist (qa-reviewer):** qa-reviewer · 6 of 6 rows ✓ with evidence (the one ✗ at its evaluation, the seam census, is discharged in §Orchestrator fold)

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

---

## Detail (reference)

### What was executed, by whom, on which tree

| Run | Executor | Tree | Command | Output | State |
|---|---|---|---|---|---|
| Base suite | orchestrator (P1) | `4b2c13a` | `python -m pytest -q` | `evidence/base-suite.txt`: 2306 passed in 450.07 s, exit 0 | `executed` |
| **The ONE complete gate run** (C-25) | **orchestrator** | the product at close: increment 004 frozen r2 plus the P4 test folds (`evidence/close-frozen.sha256`) | `python -B -m pytest -q -p no:cacheprovider` | `evidence/close-gate.txt`: **1 failed, 2485 passed in 476.36 s**. The failure is `tests/test_app.py::test_win_clipboard_roundtrip`, a clipboard SETUP failure in the environment (G-011) | `executed` |
| Increment 004 gate (frozen r2, before the P4 folds) | orchestrator | 004 r2 | same | `evidence/inc004-gate-r2.txt`: 1 failed (the same flake), 2485 passed in 470.77 s | `executed` |
| Freeze check | qa-reviewer | working tree | `sha256sum -c inc004-frozen-r2.sha256` and `find -newer` | all 7 hashes match; no product, test or README file newer than the gate's start | `executed` |
| Targeted batch nodes | **qa-reviewer** | same | AT-601..606, TC-615/616, both seam controls | 30 passed, 0 failed | `executed` |
| Probes on synthetic boards | qa-reviewer, ux-reviewer, security-reviewer | same | scratch scripts (`scratchpad/qa/*`, `walk*.py`, `secprobe/`) | the offer converts exactly the ticked set; the ruler carries two Data Warehouse marks; a live walk of `M`, the gantt and kanban, and the offer | `executed` |
| Offer seam census (§5, Q-9) | orchestrator | close tree | `pytest -p p4_offer_census` (full suite) | `evidence/p4-offer-census.json` (r2): 585 app starts; 297 unmarked starts with a candidate; 140 suppressed by the seam alone; **0 offers in unmarked nodes**; 13 offers in the 21 marked starts | `executed` |
| RED counterfactuals, mutation batteries | software-dev (packets 001–004; P4 pair here) | each increment's frozen revision, in a scratch export | `evidence/battery.py` + `mutants_*.json` | see §Layer 0 | `executed` |
| Close captures | orchestrator | close tree | `evidence/capture_b2.py . close …` | 36 files in `evidence/captures/close-*` (editor/details re-shot after UXV-1) | `executed` |

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `Task.from_dict` (milestone) | invalid input: only `True` is a flag | TC-601 | pass |
| `set_milestone` | cc ≥ 3 (due / start only / none) | TC-602, TC-603 | pass |
| `bump_due` (milestone arm) | cc ≥ 3 | TC-603 | pass |
| `action_milestone_toggle` + undo | boundary: saves and pushes the board | TC-604, AT-601 | pass |
| `_apply_editor_milestone` | cc ≥ 3 | TC-605 | pass |
| `gantt_plan` rows | cc ≥ 3 | TC-609 | pass |
| `milestone_tone` / `gantt_milestone_chip` | cc ≥ 3 | TC-610 | pass |
| `gantt_milestone_cells` | cc ≥ 3 (edges, last column) | TC-610 | pass |
| the ruler's milestone marks | cc ≥ 3 | TC-611, AT-602 | pass |
| `nav_model` (gantt rows, kanban work) | cc ≥ 3 | TC-609, TC-612 | pass |
| `kanban_work` and its callers | cc ≥ 3 | TC-612 | pass |
| `band_milestone_facts` / `band_rule_facts` | cc ≥ 3 | TC-613 | pass |
| `_select_first` (kanban) | cc ≥ 3 | TC-612, AT-603 | pass |
| `milestone_candidates` | cc ≥ 3 | TC-614 | pass |
| `milestones_marked` | invalid input (int / bool / str / absent) | TC-615 | pass |
| `run_milestone_offer` | boundary: writes the board, backup and log | TC-615 | pass |
| `_create_beside` (shared with B1) | boundary: exclusive create | TC-615 (names taken) | pass |
| `_offer_milestones` / `_on_offer_answered` | cc ≥ 3; boundary (on-mount order) | TC-616, AT-604..606 | pass |
| `action_undo` (milestones arm) | boundary: restores and saves | TC-616, AT-604 | pass |
| `MilestoneOffer` (`_offer_row`, `_fit`, toggle) | cc ≥ 3 | TC-617 | pass |

**Measured by mutation, never by line coverage.**

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `from_dict` | M1 `bool()` for `is True`; M5 the field dropped | ✓ KILLED | `evidence/inc001-mutations-r3.txt` |
| `set_milestone` / `bump_due` | M2 the start wins; M3 bump moves only the due; M4 undated flagged | ✓ KILLED | same |
| toggle + undo | M6 snapshot after the change; M7 start not restored; M8 a refusal still saves; M9, MB the band wording | ✓ KILLED | same |
| editor | M10, M12 the box ignored or dropped; M11, MD, ME the start toast; MC refusal keeps the flag; M13 no details mark | ✓ KILLED | `inc001-mutations-r3.txt`, `inc001-mutations-r3b.txt` |
| gantt rows / nav | G1..G4, GR | ✓ KILLED | `evidence/inc002-mutations-r2.txt` |
| tone / chip / cells | G5..G7, G13, G14, GE | ✓ KILLED | same |
| ruler / legend | G8, G9; P4 V2 (only reached marks) | ✓ KILLED (V2 SURVIVED before the fold) | `inc002-mutations-r2.txt`; `evidence/p4-mutations-before.txt` → `p4-mutations-after.txt` |
| kanban work / selection | K1..K6, K12, K13 | ✓ KILLED | `evidence/inc003-mutations-r3.txt` |
| band rule / legend | K7..K11, K14..K16, KL1..KL3 | ✓ KILLED | same |
| candidates / mark | O1..O3, O9, O10 | ✓ KILLED | `evidence/inc004-mutations-r3.txt` |
| `run_milestone_offer` | O4..O8, O17, OD1, OD3; P4 V1 | ✓ KILLED | `inc004-mutations-r3.txt`; `p4-mutations-after.txt` |
| on-mount / undo / toast | O11, O12, O18, OD2 | ✓ KILLED | `inc004-mutations-r3.txt` |
| offer screen | O13..O16, OR1, OR2 | ✓ KILLED | same |

### UX walkthrough — trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `M` on a dated task → a ` ◆` row with its date and chip, and a toast naming where it shows | `3`, `↓`, `M` (AT-601; ux live walk) | row and toast text | pass |
| `M` again / `u` → a task again | `M`, `u` | flag and dates on disk | pass (UXV-3: `u` is silent, LOW → BACKLOG) |
| no date → refused, nothing written | `M` on an undated task | toast; file bytes identical | pass |
| gantt: `◆` + date, no bar; reached `◆✓` in ash; ruler marks the selected project's milestones | `3` `↑` `↓` `]` (AT-602) | strips + colours | pass |
| kanban: milestones off the columns and the counts, on the band rule | `4` `tab` `g` `M` `]` (AT-603) | strips; `25 tasks` header | pass |
| first start: the offer, choose, convert, `u` | `space` `↓` `↵` `u` (AT-604) | box, toasts, backup, log | pass |
| `esc` → never asked again | `esc` (AT-605) | toast; no file; fresh app no offer | pass |
| a failing backup → nothing changed, said, offered next start | AT-606 | file bytes identical; error toast | pass |

**Mechanism used:** a UI test driver (Textual `App.run_test` with pilot key presses)

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — the only user is the operator, whose visual verdict on the captures is the coordinator's next step |

- **Method:** ux-reviewer read base vs close captures (text plus SVG colours) and drove the real app with real keys on the synthetic shifted board in a scratch folder.
- **Participants or population:** none. The expert inspection was done by one reviewer agent; no user took part.
- **Evidence of the evaluation:** the ux-reviewer report summarised in §Orchestrator fold; captures in `evidence/captures/`.
- **Limits:** colours were read from SVGs, not a real terminal. Not walked: `]` until reached, AT-606's failure path, team sync, quitting with the offer open, the 34-candidate offer (TC-617 covers it).

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-601 | test | `pytest tests/test_milestones.py` | the contract's | pass | close gate |
| HLR-602 | test | `pytest tests/test_gantt_milestones.py` | the contract's | pass | close gate |
| HLR-603 | test | `pytest tests/test_kanban_milestones.py` | the contract's | pass | close gate |
| HLR-605 | test | `pytest tests/test_milestone_offer.py` | the contract's; the saved milestone set exactly `tw5`, `tm5`, `to3` (asserted since the F-1 fold) | pass | close gate; qa targeted run |
| LLR-601.1 | test (unit) | `-k "TC_601 or TC_602 or TC_603 or TC_607 or TC_608"` | the contract's | pass | close gate |
| LLR-601.2 | test | `-k TC_604` | the contract's | pass | close gate |
| LLR-601.3 | test | `-k "TC_605 or TC_606"` and `tests/test_edit_window.py` | 18 widget ids | pass | close gate |
| LLR-602.1 | test | `-k TC_609` | the contract's | pass | close gate |
| LLR-602.2 | test | `-k TC_610` | the contract's | pass | close gate |
| LLR-602.3 | test | `-k TC_611` | the contract's | pass | close gate |
| LLR-603.1 | test | `-k TC_612` | the contract's | pass | close gate |
| LLR-603.2 | test | `-k TC_613` | the contract's | pass | close gate |
| LLR-605.1 | test | `-k TC_614` | the contract's | pass | close gate |
| LLR-605.2 | test | `-k TC_615` | the contract's | pass | close gate; qa targeted run |
| LLR-605.3 | test | `-k TC_616` | the contract's | pass | close gate; qa targeted run |
| LLR-605.4 | test | `-k TC_617` | the contract's | pass | close gate |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-601 | AT-601 | `3` `↓` `M` `+` `u` `e` | painted row, toasts, board file, pushed `board.<user>.json` | ✓ · undated refusal · byte-identical file | pass |
| US-602 | AT-602 | `3` `↑` `↓` `]` at 118×30 and 80×24 | strips and colours; the month row's two Data Warehouse marks | ✓ · last column / 80 cells · no bar | pass |
| US-603 | AT-603 | `4` `tab` `g` `M` `]`; Ops at 118×40 | strips; the `25 tasks` header; band rules | ✓ · lanes and matrix · no card | pass |
| US-605 | AT-604 | the offer, `space` `↓` `↵`; fresh apps; `u` | board file, `.pre-milestones.1`, log, toasts | ✓ · backup name taken · unchosen untouched | pass |
| US-605 | AT-605 | `esc`; no candidate; a seeded board | no file; mark; no offer | ✓ · empty · seeded | pass |
| US-605 | AT-606 | a refusing backup `open`; the next start | file bytes identical; error toast; offer again | ✓ · failure · retry | pass |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | the `M` key | `action_milestone_toggle` | yes | AT-601 | ✓ |
| input | the editor's milestone box | `#f-milestone` → `_apply_editor_milestone` | yes | AT-601 (`e`), TC-605 | ✓ |
| input | a pulled teammate's flag | `Task.from_dict` | yes | TC-607 | ✓ |
| input | gantt `↑` `↓` `]` | `nav_model` rows, `_notify_folded` | yes | AT-602 | ✓ |
| input | kanban `tab` `g` `M` | `kanban_work`, `_select_first` | yes | AT-603 | ✓ |
| input | the offer's `space` `↓` `↵` `esc` | `MilestoneOffer` → `run_milestone_offer` | yes | AT-604, AT-605 | ✓ |
| input | `u` after a conversion | `action_undo` (milestones) | yes | AT-604, TC-616 | ✓ |
| output | the milestone row, chip, reached `◆✓` | `gantt_milestone_cells`, `gantt_milestone_chip` | yes | AT-602 | ✓ |
| output | the ruler marks and the legend | `render_gantt`, `legend_entries` | yes | AT-602, TC-611 | ✓ |
| output | the band rule's milestones; the header counts | `band_rule_facts`, `render_view` | yes | AT-603 | ✓ |
| output | the details mark | `TaskDetails` | yes | TC-606; close-details capture | ✓ |
| output | the saved board / pushed team file | `Board.save`, team push | yes | AT-601 | ✓ |
| output | backup, log, mark | `run_milestone_offer` | yes | AT-604, TC-615 | ✓ |
| output | the toasts (convert / not now / failure / undo) | `_on_offer_answered`, `action_undo` | yes | AT-604..606 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2306 | 0 | 180 | 2486 | 2486 | — / 2485 (+1 environment failure, G-011) | yes |

The 180 new nodes are 41 in `test_milestones.py`, 29 in `test_gantt_milestones.py`, 71 in `test_kanban_milestones.py`, 37 in `test_milestone_offer.py` and 2 in `test_milestone_offer_seam.py`. The P4 folds added assertions only, no nodes.

### Gaps detected

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | HLR-605, HLR-602 | qa F-1, F-2: AT-604 did not assert the saved milestone set exactly; AT-602's ruler arm passed on the project due alone | minor | **folded** (§Orchestrator fold), V2 RED → KILLED |
| G-002 | HLR-601..603 | qa F-3..F-5: some AT arms set the selection directly; no push of offer-converted flags; the ash month mark is checked as "any" | minor | BACKLOG |
| G-011 | — | `test_win_clipboard_roundtrip` fails on its clipboard SETUP in this environment | minor (environment) | BACKLOG (carried) |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| n/a — no defect escaped the suite; the in-batch HIGH (001 F2-1) was caught at its gate and is recorded in packet 001 | | | | | |

### Evidence checklist — qa-reviewer (full)

- ✓ **Mode declared.** `validation`, at the top of the qa report and of this record.
- ✓ **Each result names who executed it.** See §What was executed.
- ✓ **Black-box via `run_test` keys and on-disk files.** All six ATs (Layer B).
- ✓ **Bidirectional surface-reachability.** 7 input and 7 output rows, no gap.
- ✓ **No PII.** Synthetic boards only (`tests/kg_board.py` in `tmp_path`; the reviewers' scratch boards). Evidence is redacted to `<home>`/`<session>`; security S5-1 is folded.
- ✓ **Seam census.** It was `not-run` when qa evaluated. The orchestrator then ran it on the close tree (`evidence/p4-offer-census.json` (r2): 585 app starts; 297 unmarked starts with a candidate; 140 suppressed by the seam alone; **0 offers in unmarked nodes**; 13 offers in the 21 marked starts), and the reconciliation with P1's 274 is below.

---

### Orchestrator fold after the P4 evaluations (2026-10-05)

| Finding | Source | Handling | Evidence |
|---|---|---|---|
| F-1 (MED, tests): the saved milestone set not asserted exactly | qa | AT-604 asserts `{milestones} == {tw5, tm5, to3}` and the second copy's exact set. V1 (unchosen converted silently) was already KILLED by the undo arm and stays KILLED | `evidence/p4-mutations-before.txt`, `p4-mutations-after.txt` |
| F-2 (MED, tests): the ruler arm passes on the project due | qa | AT-602 counts two Data Warehouse marks. V2 (only reached marks) SURVIVED before and is KILLED after | same |
| UXV-1 (MED, evidence): the close editor/details captures showed a non-milestone | ux | `capture_b2.py` walks to the milestone in the gantt with real keys; the four close shots were re-taken | `evidence/captures/close-editor-*`, `close-details-*` |
| S5-1 (LOW, evidence): two files carried a home path | security (close) | redacted (the redactor now also catches the `/c/Users/…` form) | `evidence/mutants_p4.json`, `p4-offer-census-run.txt` |
| The seam census (Q-9) | qa ✗ row | run on the close tree; reconciled below | `evidence/p4-offer-census.json` |
| UXV-2, UXV-4, UXV-5, UXV-7, UX-12 | ux | for the operator's visual verdict (PLAN §Provisional visual decisions) | captures |
| UXV-3, UXV-6, F-3..F-5, S5-3 | ux, qa, security | BACKLOG | `.dev-flow/BACKLOG.md` |

**The census reconciliation.** P1 measured 274 app starts whose board held a candidate (`evidence/p1-offer-census.txt`); at P1 no board carried a mark. The P4 r1 run (`p4-offer-census-run-r1.txt`) counted only the starts the seam itself suppresses, 140, which looked short of 274. The two counted different things. Since increment 004, a board file created by `Board.load` is seeded with the mark (D-617), so it never offers, with or without the seam. r2 records every row and P1's own measure: **297** unmarked starts hold a candidate (≥ 274 ✓; +23 from the batch's new tests). They split into 140 suppressed by the seam alone and 157 on seeded or already-marked boards (66 in `test_app.py`, 37 in `test_edit_window.py`, …); 0 are unreadable. The safety condition holds: **0 offer screens in unmarked nodes**. The §5 threshold is met on the measure it was set with.

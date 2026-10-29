# Increment 005 — HLR-3104 · `the DDR corrections: the printed view names only what it shows`

> **Owed in.** `core` ✓ · `full` ✓
> **Reserved field names** (language-independent, parsed literally): `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`

| Field | Value |
|---|---|
| Batch | `2026-10-29-batch-01` |
| Increment | `005` (a correction increment: discharges DDR condition C-DDR-1) |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-3101` / `HLR-3104`, `HLR-3103`, `HLR-3107` / `LLR-3104.1, LLR-3103.2, LLR-3107.4` · `LED-2026-10-29-batch-01.27` amends all three |
| Acceptance | `AT-3103` · `AT-3104` · white-box `TC-3106`, `TC-3111`, `TC-3112`, `TC-3120` |
| Agent | `software-dev` (spawned implementer; the orchestrator ran the suites and the mutation battery, re-shot the captures and made the print-wrap fix; this packet was written by a scribe from the records) |
| Date | `2026-10-29` |

---

## 1 · What changed

The DDR (`design/DDR-2026-10-29-batch-01.md`, `approved with conditions`) found that the printed report named hidden boards, counted hidden projects and clipped its task table. This increment discharges C-DDR-1 (commit `7b47714`).

**The printed header names only what is shown (DQ2 = DU1 = O2).** The print has its own scope line and summary (`#print-scope`, `#print-summary`, visible in print only; the screen keeps its own). The scope line names only the boards that hold a shown task (a project file: its shown project) and the shown projects; the summary counts `Projects n`, with no `/N`; the task line reads `Showing x tasks` without `of N`. A whole hidden board, a hidden project and the file's totals no longer appear in the PDF.

**The task table prints whole (DQ1 = DU2 = O1).** In print the table scroll window is removed and the table ends at 740 px (inside the 794 px page). The headers, the dates, the priority, the phase and the in-phase cell stay on one line; other text wraps between words. A word wider than its column may still break; only the hostile or very long fixture tokens do. After the orchestrator looked at the re-shot print preview, the first rule (`break-all` on the cells) was replaced by this word-wise wrapping: it had split `normal` into `norma/l` and a date into `2026-10-/17`.

**The axis labels never collide (DQ3 = DU3 = O3).** The gantt tick labels skip any label that would overlap its neighbour (month and day labels, at 1366 and 794 px, day and default zoom).

**A downloaded view says what it holds (DU5).** The header of a downloaded view reads `Boards in this view (N): <names>`, not `All loaded boards`.

**The toast on three lines (DU4).** `taskboard/app.py:1960-1963` writes `Report written: <files>[ · n boards skipped]` / `<folder>` / `o opens it (10 s)`, so a long folder path wraps on its own line and never splits a file name.

**Test strengthening (DQ4, DQ5, CR5-1).** AT-3104 now asserts at 794 px (the printed width), not at 1366. The Q9 dates arm of TC-3106 is literal: it asserts the exact 10 ids. CR5-1 (from the code review): a project file whose project is hidden prints no project name and no board name, with its own arm and mutant. The wording changes are `LED-2026-10-29-batch-01.27`.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/report_workspace.py` | source | LLR-3104.1, LLR-3103.2 | print-only `#print-scope` / `#print-summary` (`:417`, `:426`, `:897`); `printScope` and the `Boards in this view (N)` wording (`:386-394`); the print table rules (`:147-151`); the cell column tags (`:660`); the tick-label collision skip (`:522-526`) |
| `taskboard/app.py` | source | LLR-3107.4 | the toast on three lines (`:1960-1963`) |
| `tests/test_report_workspace.py` | test | LLR-3104.1, LLR-3103.2 / AT-3103, AT-3104, TC-3106, TC-3111, TC-3112 | 3 NEW nodes (`test_TC_3112_the_printed_header_names_only_the_shown_boards`, `test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name` (CR5-1), `test_TC_3112_the_gantt_axis_labels_never_collide`); the table arm and the one-line-cells arm in `test_TC_3112_the_print_rules_hold`; AT-3104 at 794 px; TC-3111 and AT-3103 read `Boards in this view`; the Q9 dates arm literal |
| `tests/test_report_export_app.py` | test | LLR-3107.4 / TC-3120 | the expected toast on three lines (the helper and the line-by-line assertion) |
| `tests/test_modal_keys.py` | test | LLR-3107.4 / AT-3107 | the toast prefix check (`:518`) follows the new first line |
| `.dev-flow/2026-10-29-batch-01/01-requirements.md`, `01-requirements-ledger.md` | doc | LLR-3104.1, LLR-3103.2, LLR-3107.4 | the amendment `LED-2026-10-29-batch-01.27` |
| `.dev-flow/2026-10-29-batch-01/design/DDR-2026-10-29-batch-01.md`, `PLAN.md` | doc | — | the DDR's Discharge and re-seal; the plan's state and Test ledger row |
| `.dev-flow/2026-10-29-batch-01/evidence/captures/` | generated | LLR-3104.1, LLR-3103.2 | the captures re-shot after the fixes (`workspace-print-preview.png`, `workspace-configured-view.png`, `workspace-downloaded-view.png`, the PDFs and the two written HTML files) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** (`report_workspace.py`, `app.py`) |
| Test files | 3 (uncapped) |
| Doc files | 4 (outside the count) |

## 3 · How to test

```bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
cd C:/Users/jjgh8/Github/taskboard-wt/report-proto
env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q -p no:cacheprovider   # must print a path inside report-proto
TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_export_app.py tests/test_report.py tests/test_report_html.py tests/test_report_workspace.py tests/test_report_deck.py
env -u NO_COLOR python -m pytest -q tests/test_modal_keys.py -k AT_3107
git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py | wc -l   # 0 (TC-3121)
# the mutation battery
env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-005.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none separate — the print rules and the label skip are asserted through the nodes below | n/a |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | `test_TC_3112_the_printed_header_names_only_the_shown_boards` (LLR-3104.1: a fixture that hides a whole board; its name and `/6` are absent from the printed scope line and summary, the shown boards and `Projects n` present) · `test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name` (CR5-1: project scope, 0 kept tasks) · `test_TC_3112_the_print_rules_hold` (the table arm: right edge ≤ 794, last column visible; the one-line-cells arm: headers, dates, priority, phase and in-phase on one line) · `test_TC_3112_the_gantt_axis_labels_never_collide` (bounding boxes of the labels at 1366 and 794 px, day and default zoom) · `test_TC_3111_the_view_file_reopens_on_its_view` (LLR-3103.2: `Boards in this view`) · `test_TC_3106_filters_follow_the_truth_table[dates]` (Q9 literal: the exact 10 ids) · `test_TC_3120_o_opens_the_report_while_the_toast_lives` (LLR-3107.4: the three toast lines) | in the 68 below |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | `test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` (now at 794 px) · `test_AT_3103_download_this_view_holds_only_the_filtered_tasks` (`Boards in this view`) · `test_AT_3107_the_report_modal_obeys_the_modal_key_law` (the toast prefix) | in the 68 below, plus the AT-3107 run |
| regression | `core` | the nodes of increments 001–004 in the five report files | green in the run below |
| increment total | — | `TASKBOARD_REQUIRE_BROWSER=1` over the five report files, 0 skipped | **68 passed** in 30.78 s (`suite-005.txt`), plus `test_AT_3107_…` 1 passed |

The package-scanning law suites and `test_app`, `test_keymap`, `test_help_keys`, `test_readme` were not re-run in this increment; none of them reads the changed bytes (the census below); they run at P4 (the chunked full suite).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | 15 single-fault mutants M01–M15, each a one-line change aimed at one of this increment's OWN assertions |
| Instrument | project code, mutated by the script `evidence/mutation-005.py` (anchor-checked string replacement, `finally`-restore, per-node verdicts) |
| Where it ran | this worktree, the increment tree; the harness restores the file before the next mutant |
| Transcript | `evidence/mutation-005.txt` (15/15 on the final bytes, after the print-wrap fix and the CR5-1 arm) |
| Restore proven by | sha256 recorded before and after every mutant (`restored, identical`); final `report_workspace.py` `66195b9e94fe2b0187227af9bc028cc82c3ccd056ef1f30f237232185daaa1c1`, `app.py` `701b551de8fefcaa37b029a92ae08033d64aeebe2f7455dfe89d904711703984` |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every run |
| Arms resolved at baseline | 15 mutants, each with its `-k` selection resolved to the named node |
| Verdict granularity | per resolved node id (the transcript prints `RED nodes: [...]` for each mutant) |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | the DDR findings' own mutations: M01 (the print keeps the old scope line with every loaded board) and M02 (the printed summary keeps `Projects n/N`) turn `test_TC_3112_the_printed_header_names_only_the_shown_boards` RED; M03 and M04 (the print table rules dropped, the scroll window kept) turn `test_TC_3112_the_print_rules_hold` RED — the clipped table of O1 · transcript `evidence/mutation-005.txt` · restore digests as in the table above |

### Mutation verdicts

| Field | Value |
|---|---|
| **Mutation verdicts** | 15/15 KILLED, none survived, none BAD, per resolved node: M01 the old scope line, M02 the `n/N` summary → `test_TC_3112_the_printed_header_names_only_the_shown_boards` · M03 the table rules dropped, M04 the scroll window kept, M05 cells never wrap, M11 headers, dates, priority, phase or age may wrap, M12 `break-all` back on the cells, M13 an over-long word cannot break, M14 the cells lose their column tag → `test_TC_3112_the_print_rules_hold` · M06 the download says `All loaded boards` → `test_TC_3111_the_view_file_reopens_on_its_view` · M07 no label skipped, M08 the day labels placed first → `test_TC_3112_the_gantt_axis_labels_never_collide` · M09 the toast back on one line → `test_TC_3120_o_opens_the_report_while_the_toast_lives` · M10 a span whose due is `from` dropped → the literal dates arm of `test_TC_3106_filters_follow_the_truth_table` · M15 a project file with its project hidden prints the project and its board → `test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name` · arms that stayed GREEN: none · transcript `evidence/mutation-005.txt` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the printed-text read under `emulate_media(media="print")` (scope line, summary) | M01, M02 (the old scope line, `Projects n/N`) | `test_TC_3112_the_printed_header_names_only_the_shown_boards` RED |
| the table's bounding box and per-cell line count in print at 794 px | M03, M04, M05, M11, M12, M13, M14 | `test_TC_3112_the_print_rules_hold` RED per mutant |
| the axis labels' bounding boxes | M07, M08 | `test_TC_3112_the_gantt_axis_labels_never_collide` RED per mutant |
| the notification record's message split on newlines | M09 (one line) | TC-3120 RED |
| the literal id set of the dates arm | M10 | TC-3106 RED |
| the project-file printed text | M15 | CR5-1 node RED |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 6 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the printed page (the view as printed, under print emulation at 794 px) | the scope line and summary text, the table's box and each cell's line count, the labels' boxes are read from the rendered page, not from the source string | passed; M01..M05, M07, M08, M11..M15 turn it RED |
| the downloaded file's header (saved bytes, re-opened) | TC-3111 saves the download, re-opens it headless, reads `Boards in this view` | passed; M06 turns it RED |
| the toast the user reads | the notification record's message split into its three lines | passed; M09 turns it RED |
| the re-shot print preview and PDF | `evidence/captures/workspace-print-preview.png` shows `Boards in this view (1): Client A` and every table column | read by the orchestrator and by the DDR re-seal |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 4 artifact classes (the printed page, the downloaded file, the toast, the re-shot captures), each asserted in the form the recipient receives |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-005.txt | .dev-flow/2026-10-29-batch-01/evidence/suite-005.txt | 232678b95bc5c73db80ac608770e9fe1cf0a2e3a062dbac2da2a3e0a8add08d1 |
| mutation-005.txt | .dev-flow/2026-10-29-batch-01/evidence/mutation-005.txt | 1d51394c2c3d9192063a5fc40088376387b95b8a32183a3b70cb320e151461ee |
| mutation-005.py | .dev-flow/2026-10-29-batch-01/evidence/mutation-005.py | 5938f4ef6df0f716930a76a21325ea84cd86ade173e36ad278d11f9372e8f1e2 |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — "the printed text names and counts no hidden board or project" |
| If the result is an ABSENCE, what made the search wide enough | the TC-3112 fixture hides a WHOLE board and a project of a shown board; the assertion lists the hidden names and `/6` against the printed scope line and summary, and the project-file arm (CR5-1) covers the 0-kept path; a literal list, not a pattern |
| Guard labelled as protecting a CONCLUSION, not a behaviour | the absence arms protect the conclusion "the PDF a recipient receives carries no hidden name or total"; the downloaded file's own byte check (LLR-3103.1) is unchanged |
| Conjunctive criteria: one mutation per conjunct | the header: board names (M01), total (M02); the table: rules (M03), window (M04), wrapping (M05), one-line cells (M11), `break-all` (M12), long words (M13), column tags (M14); the axis: neighbour skip (M07), order (M08); the project file (M15) |
| Synthetic instance of the absent case | the workspace test fixture with three boards, one of them fully hidden by the filter, and a project file with its only project hidden |
| **Positive control for every probe that returned an ABSENCE** | M01 and M02 put the hidden board name and `/N` back, so the absence arms fire on the present case |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rln "All loaded boards\|Report written\|Projects \|of N" tests/` · `grep -rln "report_workspace" tests/` | the toast text was asserted in `tests/test_report_export_app.py` (helper and line check) and `tests/test_modal_keys.py:518` (the prefix check): both EDITED here, named. `All loaded boards` was asserted in TC-3111 and AT-3103 of `tests/test_report_workspace.py`: EDITED to `Boards in this view`. AT-3104 and the Q9 dates arm: tightened. `tests/test_report_html.py`, `test_report_deck.py` and `test_report.py` do not read the workspace page: green and unedited |
| B2 file moved on disk | n/a — no file moved (probe not fired, declared) | — |
| B3 byte-identical golden captures this source | `tests/goldens/` does not exist (P0 probe) | not fired; the `evidence/captures/` files are not goldens, they are re-shot |
| B4 artifact produced here is consumed elsewhere | `grep -rln "workspace-.*html\|print-scope\|print-summary" tests/ taskboard/` | the written pages are consumed by the OS opener and the tests above; `#print-scope` and `#print-summary` have no other reader |
| A3 interface consumed by another module changed | `git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py \| wc -l` | 0 lines (TC-3121); `report_workspace.render`'s signature and the dict shape are unchanged |

| Field | Value |
|---|---|
| **Reverse census** | 4 probes run (B1 with the existing-test edits named: `test_report_export_app.py` toast helper, `test_modal_keys.py:518`, TC-3111, AT-3103, AT-3104, the Q9 arm; B3; B4; A3); B2 declared not fired; every movement is a planned wording change of `LED .27` |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| DQ1 = DU2: the printed table clipped | every `.tbl-wrap` / table print rule and every column of the task table | `grep -n "tbl-wrap\|@media print" taskboard/report_workspace.py` and the table's header cells | 1 print block, 1 wrapper, 8 columns | the print block (scroll window off, table 740 px, per-column rules, word-wise wrapping); the table arm and the one-line-cells arm | 0 |
| DQ2 = DU1: the printed header names hidden boards and totals | every printed text that names a board or a project or counts them | `grep -n "scopeLine\|summaryText\|Showing\|Projects" taskboard/report_workspace.py` | 4 (scope line, summary, task line, the downloaded header) | all 4: `printScope`, the `Projects n` summary, `Showing x tasks`, the download header | 0 |
| DU3 = DQ3: axis labels collide | every gantt tick label (month and day) | `grep -n "tick\|axis" taskboard/report_workspace.py` | the month and day label emitters | the skip of a label that overlaps its neighbour | 0 |
| DU4: the toast splits a file name | every place the toast text is built or asserted | `grep -rn "Report written" taskboard/ tests/` | 1 producer + 3 test sites (`test_report_export_app.py` helper and line check, `test_modal_keys.py:518`) | the producer and the 3 test sites | 0 |
| DU5: the downloaded header reads `All loaded boards` | every place that string occurs | `grep -rn "All loaded boards" taskboard/ tests/` | the producer + TC-3111 + AT-3103 | the downloaded-view path (`report_workspace.py:386-394`) and TC-3111, AT-3103 | 0; the string survives only in the unfiltered scope line (`report_workspace.py:387`, `report_deck.py:293`) where every loaded board is shown, which is true there |
| DQ4: AT-3104's width bound is 1366 | every width bound in AT-3104 | `grep -n "set_viewport_size\|794\|1366" tests/test_report_workspace.py` (AT-3104 body) | 1 node | tightened to 794 | 0 |
| DQ5: Q9 only partly literal | the dates arm's expected set | `grep -n "TRUTH_ARMS" tests/test_report_workspace.py` | 1 arm (dates) | the arm asserts the exact 10 ids; M10 pins it | 0 |
| CR5-1: the project file with its project hidden | every path through `printScope` | `sed -n 380,400p taskboard/report_workspace.py` | 3 (all boards, a board file, a project file) | the project-file path covered by a node and M15 | 0 |

| Field | Value |
|---|---|
| **Correction population** | 8 corrections (DQ1, DQ2, DU3, DU4, DU5, DQ4, DQ5, CR5-1), each enumerated with its method and its count; all edited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| `All loaded boards` as the downloaded view's header | `grep -rn "All loaded boards" taskboard/ tests/` | yes — the surviving refs are the unfiltered scope line (`report_workspace.py:387`, `report_deck.py:293`, `tests/report_fixture.py:232`, `test_report_export_app.py:187`), where all boards are shown and the wording is true; the filtered download says `Boards in this view`; the ledger keeps the before text | `01-requirements-ledger.md` LED .27 |
| `Report written: <name> to <dir> — o opens it (10 s)` (the one-line toast) | `grep -rn "to {folder} —" taskboard/ tests/` | yes — 0 hits; the live statement gives the three lines | `01-requirements.md` LLR-3107.4 |

### Signed-balance test ledger

`post = base − deleted + added` → `68 = 65 − 0 + 3`  ✓ reconciles: the base is the 65 nodes of the five report files before this increment (html 12, workspace 22, deck 6, report 18, export_app 7); this increment adds 3 nodes (`test_TC_3112_the_printed_header_names_only_the_shown_boards`, `test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name`, `test_TC_3112_the_gantt_axis_labels_never_collide`); no node deleted; the table, one-line-cells and Q9 arms are inside existing nodes. `test_AT_3107_…` (`tests/test_modal_keys.py`) is counted once, in increment 004's total.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | code-reviewer — spawned as a generic agent with agents/code-reviewer.md · OK to advance (with notes) · 0 HIGH; CR5-1 and CR5-2 LOW, CR5-3 intended; the post-review print-wrap fix was NOT re-read by the code-reviewer (declared) |

Reading: 0 HIGH; the reviewer ran 31 tests (workspace and export_app). The print-only / screen-only split is correct (`.scr` against `.prtb`); the print span reads `Showing x tasks` without `of N`; the tiles, notes, milestones and gantt labels come from the kept tasks; no printed or downloaded text names or counts a hidden item. The collision skip holds at 1366 and 794 px (both widths, day and default zoom). M01–M07 map to distinct nodes. The `(0)` edge case is acceptable (safe output). Findings: CR5-1 (LOW, `report_workspace.py:388-391`, the project-scope with 0 kept path untested) — fixed with an arm and mutant M15; CR5-2 (LOW, the TC-3112 summary literal depends on the fixture order) — accepted, the fixture order is fixed and the literal is by design (Q9); CR5-3 (LOW, the working tree also touches `evidence/captures`) — intended: the orchestrator re-shot the captures after 005 and committed them with it.

Post-review change, not re-read: the print table never breaks words mid-word (the orchestrator's look at the re-shot print preview). Its pin is M11..M14 and the one-line-cells arm.

---

## 5 · Risks

- **The post-review print-wrap fix was not re-read by a reviewer** (declared in §4b); the pin is M11..M14 and the one-line-cells arm; the DDR re-seal reads the re-shot print preview.
- **A word wider than its column may still break** in print (only the hostile or very long fixture tokens do); by design, since a table wider than the page would clip.
- **The real print dialog was not exercised** (carried from the DDR's "not covered"): print is asserted through `emulate_media(media="print")` at 794 px and the re-shot PDF.
- **Browser tests do not run in CI:** Playwright is not a declared dependency; this machine's transcripts (`suite-005.txt`, `mutation-005.txt`) are the evidence of record.
- **The mutation harness anchors on source text:** a later edit to those lines makes a mutant `SETUP-ERROR`; the harness reports it rather than passing.
- **The TC-3112 summary literal depends on the fixture order** (CR5-2, accepted).

## 6 · Pending items / spec deviations

- **Requirement amendment:** `LED-2026-10-29-batch-01.27` (LLR-3104.1, LLR-3103.2, LLR-3107.4). The frozen dict shape is untouched, so the PDR is not re-opened.
- **DDR condition C-DDR-1:** discharged by this increment (DQ1, DQ2 with arms and mutants; DQ3, DQ4, DQ5, DU3, DU4, DU5); the DDR is re-sealed in the same commit batch. DQ6 (TC-3121 is an inspection pin) is named in `04-validation.md` at P4.
- **Carried:** CR3-4, CR3-5 and CR4-4 in `BACKLOG.md`; CR5 (the Inbox key collision) from increment 001; the DDR's notices N1 (opaque modal backdrop) and N2 (faint dashed export buttons) to `BACKLOG.md`; the package-scanning law suites and the chunked full suite at P4.
- **Other agent:** `evidence/captures/terminal/` is being re-shot by another agent and is not part of this increment's commit.

## 7 · Suggested next task

DDR re-seal (C-DDR-1 discharged), then P4: the full suite in 3 sequential chunks, the package-scanning laws, the validation record (`04-validation.md`, with the TC-3121 inspection pin named).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 3 new nodes, arms in 5 existing nodes, 3 test files |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | §4: no unit is separate from its TC node |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4: M01..M04 · `evidence/mutation-005.txt` · restore digests |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4: 4 probes; the existing-test edits named |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b: OK to advance with notes, 0 HIGH; the print-wrap fix not re-read (declared) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | TC-3121: `report.py`, `__main__.py`, `views.py` diff 0 lines vs `9da7438`; the dict shape unchanged |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `suite-005.txt` (68 passed), `mutation-005.txt` (15 KILLED); digests in the evidence rows |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 table with positive controls |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | §4: 15 mutants, per-node verdicts, none green |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4: 6 instruments |
| 13 | **Correction population** declared | all | ✓ | §4: 8 corrections with methods |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4: the printed page, the downloaded file, the toast, the re-shot captures |
| 15 | **Independent review** names somebody | all | ✓ | §4b: code-reviewer |
| 16 | **Evidence files** declared | all | ✓ | §4: rows written by `devflow-evidence.py` |

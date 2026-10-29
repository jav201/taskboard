# Validation — taskboard — Batch 2026-10-29-batch-02

> **Artifact language:** English. Phase 4 artifact. Content owner: `qa-reviewer` (spawned as a generic agent with `agents/qa-reviewer.md`, model sonnet), who evaluated the results and named who executed each; the orchestrator wrote this record. The one complete gate-suite run is the orchestrator's.

**`Mode`:** `validation`

## ✅ Verdict (read first)

- **Result:** `PASS-WITH-NOTES`
- **Gate run:** `env -u NO_COLOR TASKBOARD_REQUIRE_BROWSER=1 python -m pytest -q -p no:cacheprovider -rs <chunk files>` in 3 sequential chunks (41 + 39 + 38 test files, `ls tests/test_*.py | sort | split`) · exit 0, 0, 0 · 1461 + 1032 + 872 = 3365 passed, 0 failed, 0 skipped · on commit `9a0d1b1` (one doc-only README line changed after it; `tests/test_readme.py` and `tests/test_report_cli.py` re-run: 44 passed) · run by the orchestrator (`evidence/suite-p4-chunk00.txt`, `chunk01`, `chunk02`). The first run of chunk 02 FAILED 1 (`tests/test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person`: the new `--report` help text said «when you have several»); it is kept as `suite-p4-chunk02-run1-FAILED.txt`, fixed in `9a0d1b1`, and all three chunks were re-run on the fixed commit (the first-run transcripts of chunks 00 and 01 are kept as `*-run1.txt`: 1461 and 1032 passed). The baseline's TC-1902 skip did not occur: 0 skipped.
- **Layer 0:** `0 unit(s) met the criterion · 0 carry a named reddening mutation` (none due; the prompt and the reader are crossed in-process by TC-4103 / TC-4110 and mutated by M02, M13, M15, M16, M25..M28)
- **Requirements:** 5/5 HLR and 16/17 LLR pass (LLR-4105.4 is due at the close) · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ US-4101's `AT-4101..AT-4107` observe the outcome through the shipped surface (the `python -m taskboard --report` subprocess; headless Chromium for the files), with boundary and negative evidence
- **Surface-reachability (bidirectional):** ✓ all named inputs AND outputs/deliverables reached/observed at the surface; not exercised by the reviewer: exit 1 from an unwritable folder (TC-4111 covers it), a real TTY and Ctrl-C (inspection only)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative (`evidence/supersession-001.txt`)
- **Test ledger:** ✓ reconciles (`3332 − 0 + 33 = 3365`)
- **Evidence checklist (qa-reviewer):** `qa-reviewer · 11 of 12 rows ✓ with evidence; the 12th (LLR-4105.4) is not-run until the close`

> Notes (all LOW): G-001 the LLR-4105.1 command as written matches `write_reports` (TC-4109 uses a word boundary and is right); G-002 the `a` notice announces the folder but does not say «combined» (the README warns); G-003 `red-base-001.txt` ran 31 of the 33 nodes (the two added in the review fold, TC-4113 and TC-4114, are killed by M09 and M29 instead); G-004 message polish; G-005 the README structure line (fixed). See Gaps.

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| none | no unit meets cyclomatic ≥ 3 with a boundary crossed beyond the CLI itself | n/a | n/a |

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| none — no Layer 0 unit is due | n/a | n/a | n/a |

### UX walkthrough — trigger family D (D1) fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| with two boards and `taskboard --report`, they see a numbered list with the default marked and the question naming every answer | CLI subprocess | list, `(default)`, `Board [1-2, enter = default, a = all, q = quit]:` | ✓ |
| an invalid answer is said and asked again | CLI subprocess | `Not a choice: x` and the prompt again | ✓ |
| `a` names where the combined data goes | CLI subprocess | `Writing the reports of 2 boards into <folder>` on stderr | ⚠ announces, does not warn (G-002); the README warns |
| a script with no stdin is told what to do | CLI subprocess | `pass --board PATH to choose a board` | ✓ |
| a missing `--board` path is refused plainly | CLI subprocess | `taskboard: no board file at <path> (--report reads an existing board)` | ✓ |
| an unknown project lists the real ones | CLI subprocess | `no project named 'Nope'. On this board: …` | ✓ (no `taskboard:` prefix, G-004) |

**Mechanism used:** CLI subprocess (a temp HOME and USERPROFILE, synthetic boards); artifact on disk; headless Chromium for the two files.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed (qa-reviewer, about 20 probes in `.scratch/qa/`, deleted at the close; and the suite's AT nodes) |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed (qa-reviewer read the wording of every message) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — a one-owner developer tool; the operator judges it on use |

- **Method:** the reviewer ran each situation as a subprocess and read stderr, stdout and the exit code.
- **Participants or population:** none (no user evaluation).
- **Evidence of the evaluation:** the reviewer's P4 report; the AT nodes in `evidence/suite-p4-chunk0*.txt`.
- **Limits:** no real terminal (a TTY) and no Ctrl-C were driven; the wording was judged by a reviewer, not by a user.

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-4101, LLR-4101.1, LLR-4101.2 | test | `tests/test_report_cli.py::test_TC_4101_report_kind_selects_the_files`, `::test_TC_4102_report_kind_is_validated`, `::test_TC_4107_the_cli_bytes_equal_the_h_path_bytes`, `::test_TC_4111_a_reports_path_that_cannot_be_a_folder_exits_1` | 2/1/1 paths; bytes equal the in-process write; exit 1 on an OSError | pass | chunk transcripts; mutants M06, M10, M12, M21 killed |
| HLR-4102, LLR-4102.1..4102.5 | test | `::test_TC_4103_the_prompt_answers`, `::test_TC_4103_a_picked_board_whose_file_is_gone_asks_again`, `::test_TC_4104_a_skips_and_counts_a_missing_board`, `::test_TC_4108_one_board_does_not_prompt_and_a_missing_default_is_refused`, `::test_TC_4110_stdin_that_misbehaves_never_tracebacks`, `::test_TC_4112_a_falls_back_when_the_default_board_is_unreadable` | the arms of HLR-4102's threshold | pass | M02..M04, M13, M15..M18, M25..M28 killed |
| HLR-4103, LLR-4103.1 | test | `::test_TC_4105_project_with_a_is_refused` (+ AT-4104) | scoped files; exit 2 | pass | M05, M22 killed |
| HLR-4104, LLR-4104.1..4104.3 | test | `::test_TC_4106_names_and_paths_are_printed_without_control_bytes`, `::test_TC_4106_a_path_with_two_spaces_is_printed_unchanged`, `::test_TC_4110_a_corrupt_registry_people_and_marks_are_not_copied_aside`, `::test_TC_4113_a_board_flag_registers_nothing`, `::test_TC_4114_a_stdout_that_cannot_spell_the_path_still_prints_it` | no control byte, no `.corrupt`, registry bytes unchanged | pass | M01, M07, M08, M09, M14, M20, M29 killed |
| HLR-4105, LLR-4105.1 | inspection + test | `::test_TC_4109_the_source_and_the_readme_pin_the_new_behaviour`; `git diff 4ca4a7d -- taskboard/report.py` → 0 lines | 0 and 0 | pass | M24 killed |
| LLR-4105.2 | test | `tests/test_readme.py::test_TC_120_the_facts_the_readme_states_match_the_code` | every flag documented | pass | chunk transcripts |
| LLR-4105.3 | test | `tests/test_report.py` (the two rewritten nodes) | 0 failed | pass | chunk transcripts; RED against the base |
| LLR-4105.4 | inspection | `grep -n "S-3" .dev-flow/BACKLOG.md` | 1 closed, 1 open | pending — due at the close (P5) | `05-close.md` |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-4101 | AT-4101 `test_AT_4101_two_boards_pick_two_writes_b_and_c_for_board_two` | `taskboard --report`, stdin `2` | the two files under board 2's `reports/`; board 1 and the registry unchanged | invalid answers re-asked (AT-4103) · RED at the base | pass |
| US-4101 | AT-4102 `test_AT_4102_a_writes_reports_covering_all_boards` | stdin `a` | the embedded data names both boards; stderr names the folder | a missing board skipped and counted (TC-4104) | pass |
| US-4101 | AT-4103 `test_AT_4103_empty_piped_stdin_exits_2_with_the_list`, `test_AT_4103_q_and_an_end_of_input_after_a_bad_answer_exit_1` | empty pipe, `q`, bad answers | exit 2 with the list; exit 1; nothing written | the Windows NUL case exits 1 (D-2) | pass |
| US-4101 | AT-4104 `test_AT_4104_board_flag_does_not_prompt_and_project_scopes` | `--board`, `PROJECT` | two files; the project-scoped file; the unknown-project error | unknown project → exit 2 and the list | pass |
| US-4101 | AT-4105 `test_AT_4105_missing_board_path_is_refused_and_creates_nothing` | `--board <missing, folder, text, ESC, empty>` | exit 2, nothing created | RED at the base (it seeds the file) | pass |
| US-4101 | AT-4106 `test_AT_4106_the_written_files_load_headless_with_no_console_errors` | headless Chromium | 0 console errors, 0 page errors, 0 foreign requests | fails if the browser is absent (`TASKBOARD_REQUIRE_BROWSER=1`) | pass |
| US-4101 | AT-4107 `test_AT_4107_the_old_report_is_not_reachable_and_the_readme_says_so` | `--board … --report` | 2 new paths, no `Report written to` | RED at the base | pass |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `--report`, `PROJECT`, `--report-kind`, `--board`, `--open` | argparse in `main` | yes | AT-4104, TC-4101, TC-4102, AT-4105 (+ TC-2410) | ✓ |
| input | stdin answers: number, blank, `a`, `q`, invalid, EOF, long line, bad bytes, closed stdin | `ask_board`, `_read_answer` | yes | AT-4101..AT-4103, TC-4103, TC-4110 | ✓ |
| output | the two HTML files | `report_html.write_reports` | yes | AT-4101, AT-4106, TC-4107 | ✓ |
| output | stdout paths, stderr list and messages, exit codes 0/1/2 | `run_report`, `ask_board` | yes | AT-4101..AT-4105, TC-4106, TC-4114 | ✓ |
| output | the README text | `README.md` | yes | AT-4107, TC-4109, TC-120 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 3332 | 0 | 33 | 3365 | 3365 (1461 + 1032 + 872) | 3365 / 3365 | yes |

### Gaps detected
| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | LLR-4105.1 | the threshold command as written in the contract matches `write_reports` (returns 1) | minor | TC-4109 uses a word boundary and is the gate; the wording is recorded in the backlog |
| G-002 | LLR-4102.4 | the `a` notice announces the folder; it does not say «combined» or warn about sharing | minor | the README carries the warning; the wording polish goes to the backlog |
| G-003 | evidence | `red-base-001.txt` ran 31 of 33 nodes | minor | TC-4113 and TC-4114 are killed by M09 and M29 instead |
| G-004 | UX | the unknown-project error has no `taskboard:` prefix; no newline after the prompt before an end-of-input error; `a` with `PROJECT` is refused after the prompt | minor | backlog |
| G-005 | docs | the README structure line for `report.py` was stale | minor | fixed in this batch (doc only; `tests/test_readme.py` re-run) |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| `tests/test_prism_laws.py::test_no_literal_in_the_source_can_emit_the_second_person` (the suite's own law caught the new help text before merge) | `evidence/suite-p4-chunk02-run1-FAILED.txt` | value (the offending literal named) | yes | pass | the same node |

### Evidence checklist — qa-reviewer (full)
- [x] Mode declared: validation.
- [x] Every case has a result or a state, with the executors named (orchestrator: the 3 chunks; author: mutation and red-base; qa-reviewer: 57 single nodes and about 20 CLI probes).
- [x] Layer B observed through the shipped CLI, with boundary and negative probes.
- [x] Bidirectional reachability.
- [x] Balance 3365 equals the chunk totals (read from the three transcripts' tails).
- [x] The first run of chunk 02 kept as FAILED, fixed, re-run.
- [x] Mutation 27 of 27 killed; red-base 29 failed, 2 passed.
- [x] Supersession inspected.
- [x] UX acts declared.
- [x] No real data: temp HOME, synthetic boards, the real `~/.taskboard` untouched.
- [x] No unfilled template placeholders in the reviewer's rows.
- [ ] LLR-4105.4: `not-run`, owed at P5.

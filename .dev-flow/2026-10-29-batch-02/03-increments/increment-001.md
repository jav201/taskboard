# Increment 001 — HLR-4101..HLR-4105 · `taskboard --report` exports the new HTML and asks for the board

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-29-batch-02/03-increments/increment-001.md`. It is not synced to the vault.

| Field | Value |
|---|---|
| Batch | `2026-10-29-batch-02` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-4101` · `HLR-4101..HLR-4105` · `LLR-4101.1`, `LLR-4101.2`, `LLR-4102.1..LLR-4102.5`, `LLR-4103.1`, `LLR-4104.1..LLR-4104.3`, `LLR-4105.1..LLR-4105.4` · ledger `LED-2026-10-29-batch-02.1..6` |
| Acceptance | `AT-4101..AT-4107` · white-box `TC-4101..TC-4114` · unit none — the prompt and the reader are exercised in-process by TC-4103 and TC-4110 |
| Agent | `software-dev` |
| Date | `2026-10-29` |

---

## 1 · What changed

`taskboard --report` now writes the interactive workspace and the deck, the two reports the `H` modal writes, through the same two calls (`report_html.extract`, `report_html.write_reports`), into `<board dir>/reports/`, and prints each path on its own line. With several boards in the registry it prints a numbered list on stderr and reads an answer on stdin (a number, an empty line for the default, `a` for every board, `q` to quit). `--report PROJECT` scopes to that project of the chosen board, `--report-kind {workspace,deck,both}` picks the files, and a `--board PATH` that is no board file is refused with exit 2 before a loader can seed it. The command only reads: no board file, registry entry, `.corrupt` copy or `last` mark is written. The mechanism is `run_report` and `ask_board` in `taskboard/__main__.py`; the old static report is no longer reachable from the CLI. One example session:

```
$ echo 2 | taskboard --report
Boards:
  1. Alpha  (default)
     C:\Users\x\.taskboard\boards\alpha\board.json
  2. Beta
     C:\Users\x\.taskboard\boards\beta\board.json
Board [1-2, enter = default, a = all, q = quit]:        <- stderr
C:\Users\x\.taskboard\boards\beta\reports\workspace-2026-10-29.html   <- stdout
C:\Users\x\.taskboard\boards\beta\reports\deck-2026-10-29.html
```

---

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/__main__.py` | source | LLR-4101.1, 4101.2, 4102.1..4102.5, 4103.1, 4104.1..4104.3, 4105.1 | `--report-kind`; `run_report`, `ask_board`, `_safe`, `_read_registry`, `_read_directory`, `_read_answer`; the `--board` refusal; no import of the old report |
| `taskboard/app.py` | source | LLR-4105.1 | one docstring sentence (`action_present`) that said `--report` still writes the old report |
| `README.md` | doc | | the Reports section and two command-table rows |
| `tests/test_report_cli.py` | test | HLR-4101, HLR-4102, HLR-4103, HLR-4104, HLR-4105 | NEW: 33 nodes, AT-4101..AT-4107 and TC-4101..TC-4114 |
| `tests/test_report.py` | test | LLR-4105.3 | the two CLI tests rewritten (below), plus the `Path` import moved to module level |
| `.dev-flow/BACKLOG.md` | doc | LLR-4105.4 | at the close (P5) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 2 (uncapped) |
| Doc files | 2 (outside the count) |

- `taskboard/report.py` is byte-unchanged (`git diff 4ca4a7d -- taskboard/report.py` printed 0 lines): `write_report`, `build_report` and `report_path` stay because `tests/test_report.py` (the old report's own law suite) uses them and `report_path` is TC-3123's oracle (decision D-4); the retirement goes to the backlog.
- **The two changed tests (CR-4), each justified.** `test_the_cli_writes_a_report_and_says_where` asserted `Report written to` and one old-report file; it now asserts two paths (`workspace-…`, `deck-…`) under `<board dir>/reports/`, no `Report written to`, `~/.taskboard` not created and the board's bytes unchanged. `test_the_cli_scopes_to_a_project_and_refuses_an_unknown_one` asserted `platform-` in stdout; it now asserts `workspace-cli2-platform-` (the `H` scope-`p` name) and the same unknown-project error and list. Both keep their original two facts; both are RED against the base `__main__.py`.

---

## 3 · How to test

```bash
export PYTHONDONTWRITEBYTECODE=1
python -c "import taskboard; print(taskboard.__file__)"        # the import probe, from the repo root
env -u NO_COLOR TASKBOARD_REQUIRE_BROWSER=1 python -m pytest -q -p no:cacheprovider tests/test_report_cli.py tests/test_report.py tests/test_readme.py tests/test_boards_backlog_round.py tests/test_report_html.py
env -u NO_COLOR python .dev-flow/2026-10-29-batch-02/evidence/mutation-001.py
```

---

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none — cyclomatic ≤ 10 per function and the one boundary (stdin) is crossed by TC-4103 / TC-4110 | n/a |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | `tests/test_report_cli.py::test_TC_4101_report_kind_selects_the_files` … `::test_TC_4114_a_stdout_that_cannot_spell_the_path_still_prints_it` (TC-4101..TC-4114) | 89 passed in the affected files (`suite-001.txt`) |
| **B · black-box** `AT-NNN` ↔ story | `core` · `full` | `tests/test_report_cli.py::test_AT_4101_two_boards_pick_two_writes_b_and_c_for_board_two` … `::test_AT_4107_the_old_report_is_not_reachable_and_the_readme_says_so` (AT-4101..AT-4107, subprocesses, headless Chromium for AT-4106) | included in the 89 passed |

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | 27 single-fault mutants of `taskboard/__main__.py`, and the whole new file run against the base `__main__.py` |
| Instrument | `.dev-flow/2026-10-29-batch-02/evidence/mutation-001.py`, exact string replacements with `old` occurring once, restore checked by sha256 |
| Where it ran | the worktree root, by the author (the orchestrator of this batch); no concurrent reader of `__main__.py` while it ran |
| Transcript | `mutation-001.txt` (27 killed, 0 survived, restore IDENTICAL); `red-base-001.txt` (the new file against the base: 29 failed, 2 passed) |
| Restore proven by | sha256 `f52b2ff66c254f5142363c0730b4cc5f5afec5093bf1b6aa38c258aa3312311e` before and after |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` |
| Arms resolved at baseline | 33 (`-k report`: `33 passed`) |
| Verdict granularity | per named test: KILLED needs a non-zero exit AND the named node among the FAILED |
| Arms that stayed GREEN | none |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/__main__.py` `run_report`, the `Path(primary).parent / "reports"` argument → `Path("reports")` (M06) made `test_AT_4101_two_boards_pick_two_writes_b_and_c_for_board_two` fail; all 27 transcripts in `.dev-flow/2026-10-29-batch-02/evidence/mutation-001.txt` · restore digest `f52b2ff66c254f5142363c0730b4cc5f5afec5093bf1b6aa38c258aa3312311e`; against the base file the new tests are RED 29 of 31 (`.dev-flow/2026-10-29-batch-02/evidence/red-base-001.txt`) |

| Field | Value |
|---|---|
| **Mutation verdicts** | 27 of 27 KILLED, arms that stayed GREEN: none — M01 registry read with `load` · M02 invalid answer = default · M03 empty pipe exits 1 · M04 `a` reads only the default · M05 PROJECT ignored · M06 files beside the CWD · M07 raw board name printed · M08 `--board` refusal removed · M09 `--board` registered · M10 `--report-kind` ignored · M12 write unguarded · M13 closed stdin raises · M14 stdout path collapsed · M15 wrong default marked · M16 `q` exits 0 · M17 fallback = last board · M18 skips not counted · M20 bidi kept · M21 kind without report accepted · M22 PROJECT with `a` accepted · M23 missing registry raises · M24 CLI calls the old report · M25 no cap on the answer · M26 non-ASCII digit picks · M27 every stream a TTY · M28 missing picked board accepted · M29 unspellable stdout raises · `.dev-flow/2026-10-29-batch-02/evidence/mutation-001.txt` · restore digest `f52b2ff66c254f5142363c0730b4cc5f5afec5093bf1b6aa38c258aa3312311e`. Declared NOT mutated: the `default not in active` fallback line (it fires only when every board is archived, a registry state the app does not produce), and the `KeyboardInterrupt` arm (no portable way to raise it in a subprocess test); both are reviewed by reading. M11 and M19 are unused ids. |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the new test file | the base `__main__.py` (no report branch) | `29 failed, 2 passed` (`red-base-001.txt`) |
| the mutation harness | each of 27 faults in the mechanism under test | `KILLED` with the named node in `FAILED` (`mutation-001.txt`); an unmatched anchor raised `AssertionError: ('M14', …, 0)` rather than passing silently (seen once while authoring) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 2 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| `<board dir>/reports/workspace-<date>.html`, `deck-<date>.html` | AT-4106 loads both in headless Chromium: 0 console errors, 0 page errors, 0 foreign requests, ≥ 3 slides; TC-4107: the CLI's bytes equal `extract` + `write_reports` bytes for the same boards, people and day | passed (`suite-001.txt`) |
| stdout paths and stderr text of the command | AT-4101 compares stdout to the exact expected paths; TC-4106 / TC-4114 check the printed bytes | passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 2 artifacts, each asserted against the form its producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| EVIDENCE_ROWS | | |
| suite-001.txt | .dev-flow/2026-10-29-batch-02/evidence/suite-001.txt | 15c3b72d432b1b0a1f8b8bd6dba0cbc0dba5d8f7211259a5d6f39731eb0d47cf |
| mutation-001.txt | .dev-flow/2026-10-29-batch-02/evidence/mutation-001.txt | f91c1e08553966304bcd0043f1c76dbd2f694f493cc8c4a0aa43113acd5ced68 |
| red-base-001.txt | .dev-flow/2026-10-29-batch-02/evidence/red-base-001.txt | b34a335fa42fe488a5f0889188a39a38ee443ccfb3ab14b6a20fcd5b9a9b14a7 |
| supersession-001.txt | .dev-flow/2026-10-29-batch-02/evidence/supersession-001.txt | de4f339be3e6f0f890d91311e4436b948cd29acc7c9044dee3cd096758e17219 |
| reverse-census.txt | .dev-flow/2026-10-29-batch-02/evidence/reverse-census.txt | 869fbb032c153fbfde9844a984686d2bf239ecd5684da2d2abe7bdc23bc0650f |

| Field | Value |
|---|---|
| **Evidence files** | `6 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | no — the «nothing written» claims (AT-4101, AT-4105, TC-4110, TC-4113) compare the full file list and digests before and after, with positive controls in the mutants M01, M08 and M09 |
| If the result is an ABSENCE, what made the search wide enough | the tree listing is recursive over the whole temp HOME |
| Guard labelled as protecting a CONCLUSION, not a behaviour | none |
| Conjunctive criteria: one mutation per conjunct | no conjunctive criterion |
| Synthetic instance of the absent case | corrupt `boards.json`, `people.json`, `marks.json` (TC-4110); a missing path, a folder, a text file, an ESC-byte path and an empty value (AT-4105) |
| **Positive control for every probe that returned an ABSENCE** | the same listing helper returned the `reports/` entries on the success runs (AT-4101) |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl "taskboard.__main__\|entry.main\|--report\|open_app" tests/` (`evidence/reverse-census.txt`) | 24 files import `__main__`, almost all only `open_app` (unchanged); `--report` is asserted by `tests/test_report.py` (2 tests, changed) and `tests/test_boards_backlog_round.py::test_TC_2410_a_path_that_is_no_board_is_refused` (`--open` + `--report`, re-run: passes); `tests/test_readme.py::test_TC_120_the_facts_the_readme_states_match_the_code` (flags vs README, re-run: passes after the `--report-kind` row) |
| B2 file moved on disk | none — no file moved | 0 |
| B3 golden captures this source | `ls tests/goldens` | no such directory |
| B4 artifact produced here is consumed elsewhere | the reports are read by a browser | AT-4106 loads both written files headless |
| A3 interface consumed by another module changed | `grep -rn "from .__main__\|import __main__" taskboard/` | 0 hits in `taskboard/`; `open_app` is unchanged |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run: B1 3 test files re-validated, B2 none, B3 no directory, B4 AT-4106, A3 0 hits — 0 foreign breakage |

### Correction population — enumerated BEFORE the first site was edited

| Field | Value |
|---|---|
| **Correction population** | none — no correction; the two rewritten CLI tests are a supersession, enumerated above in §2 and by B1 |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| `Report written to` | `grep -rn "Report written to" taskboard tests README.md` | yes — only the negative assertions in `tests/test_report.py`, `tests/test_report_cli.py` and the toast of `H` (a different string, `Report written:`) | `evidence/supersession-001.txt` |

### Signed-balance test ledger

`post = base − deleted + added` → the full suite runs at P4; for this increment: 0 deleted, 33 added in `tests/test_report_cli.py`, 2 rewritten in place (net 0).

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md (model sonnet) · PASS with notes, 0 HIGH / 0 MEDIUM / 6 LOW · F1 answer cap, F2 stdout encoding, F3 Ctrl-C, F4 the `app.py` docstring, F5 import order and F6 the people oracle all folded into commit d30acf0 with 5 new mutants and TC-4114; the re-read of that delta: PASS, 0 HIGH · `security-reviewer` — spawned as a generic agent with agents/security-reviewer.md (default model) · PASS, 0 HIGH / 0 MEDIUM / 3 LOW · its F1 (`--open` message through `_safe`) folded into commit d30acf0, F2 (a symlinked `reports/` is followed, as `H` does) and F3 (check-then-read window) accepted |

---

## 5 · Risks

- A pipe held open with no data waits, as any pipe does (D-2); the tests never do that.
- `Registry._read` and `Directory._read` are private; the coupling is pinned by M01 / M23 and TC-4110, which fail loudly on a rename.
- The `default not in active` fallback and the `KeyboardInterrupt` arm are not mutation-checked (§4).
- A `reports/` symlink is followed, as in `H` (security F2); `a` combines every board into one folder, which the stderr notice and the README name.
- The review folds (commit d30acf0) were re-read by the code-reviewer (§4b).

## 6 · Pending items / spec deviations

- D-4: the old static report (`taskboard/report.py`'s `build_report`, `write_report`, `report_path`) and `tests/test_report.py`'s law suite stay; retiring them is a backlog item written at the close.
- D-2: the Windows NUL device reads as a terminal (`isatty() == True`) and exits 1 where the commission's «non-TTY exits 2» would say 2; the README states it.
- BACKLOG: the `--report --board <missing path>` S-3 line is marked closed, and the retirement item is added, at the close (LLR-4105.4).

## 7 · Suggested next task

Phase 4, `stations/p4-validation.md`: the full suite in three sequential chunks, then `qa-reviewer`.

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | `tests/test_report_cli.py` (33 nodes), `tests/test_report.py` (2 rewritten) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | not due: §4 Layer 0 |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4, `mutation-001.txt`, `red-base-001.txt` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4: 5 probes, 0 foreign breakage |
| 6 | `code-reviewer` passed — a HIGH blocks | `core` · `full` | ✓ | §4b |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | `report_html.extract` / `write_reports` consumed unchanged; `taskboard/report.py` byte-unchanged |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `suite-001.txt`: 89 passed |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | §4: 27 of 27 KILLED |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4: 2 instruments |
| 13 | **Correction population** declared | all | ✓ | §4: none, declared |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4: 2 artifacts |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared, with digests | all | ✓ | §4: 5 artifacts, each at the declared home with the digest of its stored bytes |

# Requirements Document — taskboard — Batch 2026-10-29-batch-02

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/req-template.md` and its part 2, `templates/guides/req-template.part2.md`, explain each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose
`taskboard --report` stops writing the old static report. It exports the new HTML reports (the interactive workspace B and the vector deck C, built by `2026-10-29-batch-01`) through the code path the app's `H` modal uses, and it asks which board when the registry holds more than one. The words are the operator's, from the review of `2026-10-29-batch-01`: «Que el comando --report exporte el html, que pregunte por el board.»

### 1.2 Scope
In: the `--report` and `--report-kind` flags of `taskboard/__main__.py`; the board prompt; the project scope; the refusal of a missing `--board` path; the README's `--report` text and command table; the tests that asserted the old report through the CLI.
Not in: the reports' content or the `H` modal (unchanged); `taskboard/report.py` (byte-unchanged, §6.2 D-4); the TUI; any push or merge.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| B / C | the workspace report (`workspace-<date>.html`) and the deck (`deck-<date>.html`) |
| `H` path | `report_html.extract(...)` then `report_html.write_reports(...)`, as `TaskboardApp._on_report_chosen` calls them |
| active board | a registry entry that is not archived |
| default board | `Registry.opening()`: the last board opened when active, else the first active one |
| non-TTY | `sys.stdin.isatty()` is false (a pipe or a file) |

### 1.4 References
`.dev-flow/COMMISSION-cli-report-html.md` (CR-1..CR-5, AT-a..AT-f); `.dev-flow/2026-10-29-batch-01/` (the reports, HR-1); `taskboard/app.py` `action_report_export`, `_on_report_chosen`, `board_lanes`; `taskboard/report_html.py`; `.dev-flow/BACKLOG.md` (security S-3 for `--report`).

### 1.5 Document overview
§2 the story and its premises, §3 five HLR, §4 the LLRs and the information flow, §5 validation, §6 decisions and risks, §7 the (empty) ledger.

---

## 2. Overall description

### 2.1 Product perspective
`taskboard` is a Textual app with a shell entry point. `--report` is its no-TUI branch. Today it reads one board and writes the old static report; after this batch it reads one or all boards and writes B and C into `<board dir>/reports/`, exactly as `H` does.

### 2.2 Product functions
Pick the board (flag, default, or a prompt); extract once; write B, C or both; print the paths; never write a board or the registry.

### 2.3 User characteristics
The owner, at a shell or in a script. The prompt serves a person at a terminal; `--board PATH` and a piped answer serve scripts.

### 2.4 Constraints
Python 3.11+, the existing dependencies, no new one. At most 4 source files per increment. Synthetic data and a temp HOME in tests; the real `~/.taskboard` is never touched.

### 2.5 Assumptions and dependencies
`report_html.extract` and `write_reports` stay as batch-01 left them (A3 not fired). The registry file format is unchanged.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-4101 | As the owner running taskboard from a shell, I want `taskboard --report` to export the new HTML reports and ask me which board, so that the command gives the same reports as `H` and never silently picks the wrong board. | the operator's review of `2026-10-29-batch-01`, `.dev-flow/COMMISSION-cli-report-html.md` | READY |

#### Refinement log (one block per story)

**US-4101 — `--report` exports the new HTML and asks for the board**
- **INVEST:** I ✓ (no other story) · N ✓ (CR-1..CR-5 fix the behaviour, the flag names stay open to review) · V ✓ · E ✓ (one module and a README) · S ✓ (one increment) · T ✓ (six ATs)
- **Functionality (V, N):** user = the owner at a shell · outcome = two HTML files for the chosen board(s) and their paths on stdout · why = the CLI and the app must not drift, and a default board must not be exported by accident · out of scope = report content, the `H` modal, the old report's code.
- **Feasibility (E, S):** implementation path = a report branch in `__main__.main` that selects boards, reads them with `peek_board`, calls `report_html.extract` and `write_reports` · dependencies/unknowns = a pipe is not a TTY on any platform, and the Windows NUL device reports `isatty() == True` (§2.7 row 7) · fits one batch? = yes.
- **Evaluability (T) — behavioral, black-box:** When `taskboard --report` runs with two registered boards and `2` on stdin, the user observes two file paths under board 2's `reports/` folder and board 1's bytes unchanged (AT-4101); with `a`, reports that cover both boards (AT-4102); with an empty piped stdin, exit 2 and the board list (AT-4103); with `--board PATH`, no prompt (AT-4104); with a missing `--board` path, a refusal and nothing created (AT-4105); the files load headless with 0 console errors (AT-4106).
- **Open questions:** none; the choices the commission left open are D-1..D-6 in §6.2.
- **Classification:** `READY` — all five decisions are recorded in the commission.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | At the base, `--report` calls the old `report.write_report` and never asks for a board. | premise | ✅ TRUE | `git show origin/main:taskboard/__main__.py \| grep -n write_report` → lines 73 and 83 (`evidence/rc-p0.txt`) | the batch changes it |
| 2 | `report_html.extract` and `write_reports` run with no app and no TTY. | premise | ✅ TRUE | `evidence/premise-probes.txt` P6: `['workspace-2026-10-29.html', 'deck-2026-10-29.html']` | the CLI calls them directly |
| 3 | Reading an existing board with `peek_board` writes nothing (bytes and mtime unchanged). | premise | ✅ TRUE | `evidence/premise-probes.txt` P2: `bytes_unchanged=True mtime_unchanged=True` | the CLI reads with `peek_board` |
| 4 | `Board.load` on a missing path creates a seeded board there (security S-3). | premise | ✅ TRUE | `evidence/premise-probes.txt` P3: `creates the file: True` | LLR-4104.1 refuses the path first |
| 5 | `Registry.load` with no registry file writes nothing. | premise | ✅ TRUE | `evidence/premise-probes.txt` P4: `~/.taskboard created=False` | the CLI loads the registry read-only |
| 6 | A subprocess given `HOME` and `USERPROFILE` resolves the registry under them, and `taskboard` imports from the worktree when the cwd is the repo root. | premise | ✅ TRUE | `evidence/premise-probes.txt` P1 and `evidence/import-probe.txt` (from `tests/` it imports the MAIN checkout, so the tests set `cwd=` the repo root) | CLI tests pass `cwd` and env |
| 7 | A piped stdin is not a TTY; the Windows NUL device (`subprocess.DEVNULL`) reports `isatty() == True` and reads `''`. | premise | ✅ TRUE | `evidence/premise-probes.txt` P5: pipe `False '2\n'`; DEVNULL `True ''` | D-2: the exit-2 rule keys on «not a TTY and EOF at the first read», and tests use a pipe or a fake stream |

- **Premise evaluation:** 7 premise(s) · ✅ 7 TRUE / ❌ 0 FALSE / ❓ 0 UNDECIDABLE

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane (one increment).

---

## 3. High-level requirements (HLR)

### HLR-4101 — `--report` writes the new HTML reports through the `H` path
- **Traceability:** US-4101
- **Ledger:** none
- **Statement:** When `taskboard --report` runs on a readable board, the system shall write the reports chosen by `--report-kind` (`workspace`, `deck` or `both`; default `both`) into `<board dir>/reports/` by calling `report_html.extract` and `report_html.write_reports` as the `H` export does, print each written path on its own line on stdout, start no TUI, and exit 0.
- **Rationale (informative):** CR-1. One code path, so the CLI and the app cannot drift.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_cli.py -k "AT_4104 or AT_4106 or TC_4101 or TC_4107"`
- **Numeric pass threshold:** `--board PATH --report` exits 0 and prints exactly 2 paths, `workspace-<today>.html` and `deck-<today>.html`, both existing, non-empty, under `<board dir>/reports/`; `--report-kind workspace` prints exactly 1 and `deck` exactly 1; the CLI's bytes equal the bytes `write_reports` writes in-process for the same boards and day (TC-4107); each file loaded headless logs 0 console errors, 0 page errors and makes 0 requests but itself.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** two paths on stdout, two files that open.
  - **Shipped surface:** the `taskboard --report` command line.
  - **Acceptance test(s):** AT-4104, AT-4106
  - **Boundary catalog (QC-3):** ☑ empty (a board with no tasks still writes both files) ☑ boundary (`--report-kind` each of its three values; a second same-day run overwrites) ☑ invalid (`--report-kind other`, and `--report-kind` without `--report`, exit 2) ☑ error (the `reports/` folder cannot be created: exit 1 with a message)
  - **Negative control:** executed at P1 against `base_ref`: `taskboard --board <b> --report` prints `Report written to …` and writes a single old-report file (`evidence/base-behaviour.txt`), so AT-4104's two-path assertion is RED there.

### HLR-4102 — `--report` asks which board when there is more than one
- **Traceability:** US-4101
- **Ledger:** none
- **Statement:** When `taskboard --report` runs with neither `--board` nor `--open` and the registry holds more than one active board, the system shall print a numbered list of the boards (name and file path, the default board marked) and read an answer from stdin: a number picks that board, an empty line picks the default board, `a` picks every board, an invalid answer asks again, and `q` or end of input exits with code 1 writing nothing; and when stdin is not a TTY and ends before any line, the system shall exit with code 2, print the list and say to pass `--board PATH`, writing nothing.
- **Rationale (informative):** CR-2. A multi-board user must choose; a script must never hang on a hidden prompt.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_cli.py -k "AT_4101 or AT_4102 or AT_4103 or TC_4103 or TC_4104"`
- **Numeric pass threshold:** stdin `2\n` with boards Alpha, Beta: 2 paths under Beta's `reports/`, 0 under Alpha's, Alpha's bytes (SHA-256) unchanged, the list on stderr names both boards; stdin `a\n`: reports covering both boards (the workspace's embedded data names both); stdin `` (empty pipe): exit 2, 0 files, stderr names both boards and `--board PATH`; stdin `q\n`: exit 1, 0 files; stdin `x\n` then end: exit 1, 0 files; stdin `9\n2\n`: asks again, then writes Beta's (1 re-ask message); a fake TTY stream at end of input: exit 1 (TC-4103).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the right board's files, or a clear refusal with the list.
  - **Shipped surface:** the `taskboard --report` command line with stdin.
  - **Acceptance test(s):** AT-4101, AT-4102, AT-4103
  - **Boundary catalog (QC-3):** ☑ empty (empty piped stdin: exit 2; blank line: the default) ☑ boundary (`1`, the last number, `0` and one past the last) ☑ invalid (`x`, `9`, a negative number) ☑ error (a picked board whose file is missing is refused and asked again; EOF)
  - **Negative control:** at the base `--report` never reads stdin, so stdin `2\n` still writes the default board's old report: AT-4101's «Beta» assertion is RED there (`evidence/base-behaviour.txt`).

### HLR-4103 — `PROJECT` scopes the report to one project
- **Traceability:** US-4101
- **Ledger:** none
- **Statement:** When `taskboard --report PROJECT` runs, the system shall scope the reports to the project of that name on the chosen board, as `H` scope `p` does; an unknown name shall exit with code 2, list the board's projects and write nothing; and when the answer to the board prompt is `a`, the system shall refuse `PROJECT` with a message, exit 2 and write nothing.
- **Rationale (informative):** CR-3. The old meaning of the argument survives as a scope.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_cli.py -k "AT_4104 or TC_4105"`
- **Numeric pass threshold:** `--board <b> --report Alpha-project`: 2 files named `workspace-<board slug>-<project slug>-<today>.html` and the deck's, whose embedded data holds that project and no other; `--report Nope`: exit 2, stderr contains `no project named 'Nope'` and every visible project name, 0 files; stdin `a\n` with a `PROJECT`: exit 2, 0 files.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** only that project in the files, or an error that lists the choices.
  - **Shipped surface:** the `taskboard --report PROJECT` command line.
  - **Acceptance test(s):** AT-4104
  - **Boundary catalog (QC-3):** ☐ empty (N/A — the empty argument means «no project») ☑ boundary (a name with a space; a name present on only one of the two boards) ☑ invalid (an unknown name; `PROJECT` with `a`) ☑ error (n/a beyond the unknown name)
  - **Negative control:** at the base `--report PROJECT` writes the old report, whose file name starts with the project slug and whose body is not the workspace page: AT-4104's embedded-data assertion is RED there.

### HLR-4104 — reading is safe: nothing is written but the reports, and a missing path is refused
- **Traceability:** US-4101
- **Ledger:** none
- **Statement:** When `taskboard --report` runs, the system shall write no board file and no registry file, shall not register a `--board` path, shall refuse a `--board` path (or a default or picked board) that is not an existing board file with exit code 2 before anything is built and without creating anything at that path, and shall print every board name and file path it shows with control characters removed.
- **Rationale (informative):** CR-5, security S-3. `Board.load` seeds a missing path (§2.7 row 4); `--open` already refuses one.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_cli.py -k "AT_4101 or AT_4105 or TC_4106 or TC_4108"`
- **Numeric pass threshold:** `--board <missing> --report`: exit 2, stderr starts `taskboard: no board file at `, nothing at that path and no new file anywhere under the temp HOME; after a successful run every board file and `boards.json` has the same SHA-256 as before and `~/.taskboard` was not created when it did not exist; a board named with an ESC byte and a path with an ESC byte print with 0 bytes `\x1b`, 0 bytes in `\x00-\x08\x0b-\x1f\x7f` and no embedded newline.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a refusal and an untouched disk, or reports and an otherwise untouched disk.
  - **Shipped surface:** the `taskboard --report --board PATH` command line and the prompt text.
  - **Acceptance test(s):** AT-4105
  - **Boundary catalog (QC-3):** ☑ empty (an empty `--board ''` value) ☑ boundary (a folder; a text file that is not a board) ☑ invalid (a path holding an ESC byte) ☑ error (the default board file missing: refused, not seeded)
  - **Negative control:** at the base `--board <missing> --report` creates a seeded board at the path (`evidence/base-behaviour.txt`): AT-4105's «nothing created» assertion is RED there.

### HLR-4105 — the CLI no longer reaches the old report, and the README says what it does now
- **Traceability:** US-4101
- **Ledger:** none
- **Statement:** The system shall not call `report.write_report` from the command line, and the README's `--report` section and command table shall describe the new behaviour (both reports, the board prompt, `PROJECT`, `--report-kind`, the output folder, the exit codes, and that the old static report is no longer written).
- **Rationale (informative):** CR-4. `taskboard/report.py` stays byte-unchanged (D-4).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_cli.py -k AT_4107` and `env -u NO_COLOR python -m pytest -q tests/test_readme.py -k TC_120`
- **Numeric pass threshold:** `grep -c write_report taskboard/__main__.py` → 0; `git diff 4ca4a7d -- taskboard/report.py` → 0 lines; the README holds the strings `--report-kind`, `reports`, `exit code 2`, `exit code 1` and not `Report written to`; the CLI's stdout holds no `Report written to`; TC-120 (every flag documented) passes.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `--report` output is the new files; the README tells the same story.
  - **Shipped surface:** the command line and the README.
  - **Acceptance test(s):** AT-4107
  - **Boundary catalog (QC-3):** none — documentation and a deletion of one call; no input class applies.
  - **Negative control:** the base README says "Each writes one self-contained HTML file" and `__main__.py` calls `write_report`: both assertions of AT-4107 are RED at the base.

---

## 4. Low-level requirements (LLR)

### LLR-4101.1 — the flags
- **Traceability:** HLR-4101
- **Ledger:** none
- **Statement:** The parser shall define `--report-kind` with the choices `workspace`, `deck` and `both` (default `both`), and shall exit with code 2 when `--report-kind` is given without `--report`.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_TC_4102_report_kind_is_validated` (subprocess)
- **Numeric pass threshold:** `--report-kind other` → exit 2; `--report-kind deck` alone → exit 2; the three valid values → exit 0 with 1, 1 and 2 paths.
- **Negative control:** a mutant that accepts `--report-kind` without `--report` turns the second arm red.
- **Boundary catalog:** ☑ invalid ☑ boundary ☐ empty (N/A) ☐ error (N/A)

### LLR-4101.2 — extract once, write through the `H` path
- **Traceability:** HLR-4101, HLR-4103
- **Ledger:** none
- **Statement:** The report branch shall build `(registry id | None, name, colour, Board)` for each chosen board, read the people and marks directories beside the registry, call `report_html.extract` with the project key `<board key>:<project id>` when `PROJECT` is given, and call `report_html.write_reports` with the kinds of `--report-kind`, `today` and the folder `<primary board dir>/reports`, where the primary board is the single chosen board or, for `a`, the default board.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_TC_4101_report_kind_selects_the_files` and `tests/test_report_cli.py::test_TC_4107_the_cli_bytes_equal_the_h_path_bytes`
- **Numeric pass threshold:** TC-4101: files `{workspace}`, `{deck}`, `{workspace, deck}` for the three kinds; TC-4107: 2 of 2 files byte-equal to an in-process `extract` + `write_reports` on the same boards, people and marks.
- **Negative control:** a mutant that writes to the current directory instead of the board's folder turns TC-4101 red.
- **Boundary catalog:** ☑ empty (a board with no tasks) ☑ boundary (same-day rerun overwrites) ☐ invalid (N/A) ☑ error (an unwritable folder: exit 1)

### LLR-4102.1 — which boards are in play
- **Traceability:** HLR-4102, HLR-4104
- **Ledger:** none
- **Statement:** With `--board PATH` or `--open PATH`, the report branch shall use that one file, with its registry id, name and colour when the registry lists it and `None`, the file's name and `pink` otherwise, and shall not prompt; with neither, it shall use the registry's active boards and prompt only when there are more than one; with one, it shall use the registry's opening board.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4104_board_flag_does_not_prompt_and_project_scopes` and `tests/test_report_cli.py::test_TC_4108_one_board_does_not_prompt_and_a_missing_default_is_refused`
- **Numeric pass threshold:** `--board` with 2 registered boards and an empty piped stdin: exit 0 (no prompt, no exit 2); a registry of 1 board and an empty piped stdin: exit 0; the default board file missing: exit 2, nothing created.
- **Negative control:** a mutant that prompts even with `--board` turns AT-4104 red (exit 2).
- **Boundary catalog:** ☑ empty (no registry file: the default board alone) ☑ boundary (exactly one active board among archived ones) ☑ invalid (n/a) ☑ error (a missing file)

### LLR-4102.2 — the prompt
- **Traceability:** HLR-4102
- **Ledger:** none
- **Statement:** The prompt shall print to stderr one numbered line per active board (`N. name`, then the file path on the next line, `(default)` after the default board's name), then read lines from stdin: `a` (any case) → all boards, a number within the list → that board, a blank line → the default board, `q` (any case) → exit 1, anything else → a message and another prompt; end of input after at least one line, or on a TTY, → exit 1; a picked board whose file is missing or unreadable shall be refused with a message and asked again.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_TC_4103_the_prompt_answers` (subprocess pipe, plus an in-process fake TTY stream)
- **Numeric pass threshold:** the arms in HLR-4102's threshold, each with its exit code and file count.
- **Negative control:** a mutant that treats an invalid answer as the default turns the `9\n2\n` arm red.
- **Boundary catalog:** ☑ empty ☑ boundary ☑ invalid ☑ error

### LLR-4102.3 — non-interactive refusal
- **Traceability:** HLR-4102
- **Ledger:** none
- **Statement:** When stdin is not a TTY and the first read returns end of input, the report branch shall print the board list and the sentence `pass --board PATH to choose a board` to stderr, exit with code 2 and write nothing.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4103_empty_piped_stdin_exits_2_with_the_list`
- **Numeric pass threshold:** exit 2; stderr holds both board names and `--board PATH`; 0 files under any `reports/`.
- **Negative control:** a mutant that exits 1 there turns it red.
- **Boundary catalog:** ☑ empty ☐ boundary (N/A) ☐ invalid (N/A) ☐ error (N/A)

### LLR-4102.4 — all boards
- **Traceability:** HLR-4102
- **Ledger:** none
- **Statement:** For `a`, the report branch shall read every active board whose file exists and parses as a board (`peek_board`, `load_report["file_unreadable"]` false), skip the others, say on stderr how many were skipped, and write the reports of the rest into the default board's folder; with none readable it shall exit 2 and write nothing.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4102_a_writes_reports_covering_all_boards` and `tests/test_report_cli.py::test_TC_4104_a_skips_and_counts_a_missing_board`
- **Numeric pass threshold:** AT-4102: the workspace's embedded `boards` names Alpha and Beta; TC-4104: a third board with a missing file → 1 skipped on stderr, still exit 0 and 2 files.
- **Negative control:** a mutant that reads only the default board turns AT-4102 red.
- **Boundary catalog:** ☑ empty (all missing → exit 2) ☑ boundary (one skipped) ☐ invalid (N/A) ☑ error

### LLR-4103.1 — the project lookup
- **Traceability:** HLR-4103
- **Ledger:** none
- **Statement:** With `PROJECT` on a single chosen board, the report branch shall find the first visible project (`board.visible_projects(False)`) with that exact name and pass its key to the extract; if there is none it shall exit with code 2 and the message `no project named 'X'. On this board: a, b`; with `a` it shall exit with code 2 and a message saying `PROJECT` needs one board.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4104_board_flag_does_not_prompt_and_project_scopes` and `tests/test_report_cli.py::test_TC_4105_project_with_a_is_refused`
- **Numeric pass threshold:** as HLR-4103.
- **Negative control:** a mutant that ignores `PROJECT` turns the embedded-data arm red.
- **Boundary catalog:** ☑ boundary ☑ invalid ☐ empty (N/A) ☐ error (N/A)

### LLR-4104.1 — refuse a path that is no board
- **Traceability:** HLR-4104
- **Ledger:** none
- **Statement:** Before any board is read, the report branch shall refuse, with exit code 2 and `taskboard: no board file at <path>`, a `--board` path and a default or picked board whose file is not a regular file parsing to a JSON object (the `--open` test, `_a_board_file`), and shall create nothing at that path.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4105_missing_board_path_is_refused_and_creates_nothing`
- **Numeric pass threshold:** missing path, folder, text file, ESC-byte path: 4 of 4 exit 2; the tree under the temp HOME and the target's parent has the same file list before and after.
- **Negative control:** a mutant that calls `Board.load` first turns the missing-path arm red (it seeds the file).
- **Boundary catalog:** ☑ empty ☑ boundary ☑ invalid ☑ error

### LLR-4104.2 — nothing else is written
- **Traceability:** HLR-4104
- **Ledger:** none
- **Statement:** The report branch shall not call `Registry.register`, `Registry.touch`, `Registry.save`, `Board.save` or any other writer, and shall create no file but the reports and the `reports/` folder.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4101_two_boards_pick_two_writes_b_and_c_for_board_two` (hash arms) and `tests/test_report_cli.py::test_TC_4106_names_and_paths_are_printed_without_control_bytes`
- **Numeric pass threshold:** every board file and `boards.json` keeps its SHA-256 and mtime; `--board` of an unlisted file leaves `boards.json` absent or unchanged.
- **Negative control:** a mutant that registers the `--board` path turns the registry-bytes arm red.
- **Boundary catalog:** ☑ empty (no registry file) ☐ boundary (N/A) ☐ invalid (N/A) ☐ error (N/A)

### LLR-4104.3 — printed text
- **Traceability:** HLR-4104
- **Ledger:** none
- **Statement:** Every board name and file path the prompt, the messages or the skip count print shall go through `strip_controls` and have its whitespace runs collapsed to one space, so a name or a path cannot add a line or send a control sequence to the terminal.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_cli.py::test_TC_4106_names_and_paths_are_printed_without_control_bytes`
- **Numeric pass threshold:** a board named `Evil\x1b[2J\nFAKE 3. injected` prints on exactly one list line with 0 ESC bytes.
- **Negative control:** a mutant that prints the raw name turns it red.
- **Boundary catalog:** ☐ empty (N/A) ☐ boundary (N/A) ☑ invalid ☐ error (N/A)

### LLR-4105.1 — the old report is out of the CLI
- **Traceability:** HLR-4105
- **Ledger:** none
- **Statement:** `taskboard/__main__.py` shall not import or call `report.write_report` or `report.build_report`, and `taskboard/report.py` shall be byte-unchanged.
- **Validation:** `inspection`
- **Executed verification:** `grep -c "write_report\|build_report" taskboard/__main__.py` and `git diff 4ca4a7d -- taskboard/report.py` (packet §2)
- **Numeric pass threshold:** 0 and 0 lines.
- **Negative control:** none — an inspection pin, not a gate (C-40's corollary).
- **Boundary catalog:** none — no input surface.

### LLR-4105.2 — the README
- **Traceability:** HLR-4105
- **Ledger:** none
- **Statement:** The README's Reports section and its command-line table shall describe `--report`, `--report PROJECT` and `--report-kind`, the board prompt and its answers, the output folder, the exit codes 1 and 2, and shall say the old static report is no longer written.
- **Validation:** `test (unit)`
- **Executed verification:** `tests/test_report_cli.py::test_AT_4107_the_old_report_is_not_reachable_and_the_readme_says_so` and `tests/test_readme.py::test_TC_120_the_facts_the_readme_states_match_the_code`
- **Numeric pass threshold:** the strings of HLR-4105's threshold present (5 of 5), `Report written to` absent, TC-120 passing.
- **Negative control:** at the base README the new strings are absent: the test is RED there.
- **Boundary catalog:** none — documentation.

### Information Flow Contract (IFC) — C-54

- **Part A — flows:**

```
FLOW: report-cli
  SOURCE : argv, stdin, ~/.taskboard/boards.json, the board files, people.json and marks.json — file-derived and user-typed, untrusted text
  NODES  :
    - fn    : __main__.main — the flags
      owner : LLR-4101.1
      in    : argv
      out   : report mode, PROJECT, the kinds
    - fn    : __main__ — the board source (flag, default, or the prompt's list)
      owner : LLR-4102.1
      in    : --board / --open, the registry
      out   : the boards in play, the default board
    - fn    : __main__ — the refusal of a path that is no board
      owner : LLR-4104.1
      in    : a path
      out   : the path accepted, or exit 2 with nothing created
    - fn    : __main__ — the prompt
      owner : LLR-4102.2
      in    : the list, a line of stdin
      out   : one board, all boards, the default, or exit 1
    - fn    : __main__ — the non-interactive refusal
      owner : LLR-4102.3
      in    : stdin that is not a TTY and ends at once
      out   : exit 2 and the list on stderr
    - fn    : __main__ — all boards
      owner : LLR-4102.4
      in    : every active board
      out   : the readable boards and the skipped count
    - fn    : __main__ — the project lookup
      owner : LLR-4103.1
      in    : PROJECT, the chosen board
      out   : a project key, or exit 2 with the list
    - fn    : __main__ — printed text
      owner : LLR-4104.3
      in    : board names and paths
      out   : one clean line each (strip_controls)
    - fn    : report_html.extract (unchanged) via __main__
      owner : LLR-4101.2
      in    : the boards, people, marks, today, the project key
      out   : the dict
    - fn    : report_html.write_reports (unchanged) via __main__
      owner : LLR-4101.2
      in    : the dict, the kinds, the folder, today
      out   : the files and their paths
    - fn    : __main__ — nothing else is written
      owner : LLR-4104.2
      in    : the whole run
      out   : no board file and no registry file changed
    - fn    : __main__ — the old report unreachable
      owner : LLR-4105.1
      in    : the module's imports
      out   : no call to write_report
    - fn    : README.md — the Reports section and the command table
      owner : LLR-4105.2
      in    : the behaviour above
      out   : the documented behaviour
  SINK   : <board dir>/reports/workspace-<date>.html and deck-<date>.html; stdout (the paths); stderr (the list, messages); the exit code
```

- **Part B — boundary decomposition:** no — a command line with one entry point and no component a consumer addresses on its own (the template's «CLI emitting one report» row).

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the story's outcome through the shipped surface (the WHAT). Method: `acceptance`, as subprocesses of `python -m taskboard` on a temp HOME and USERPROFILE with the repo root as the working directory.

The browser check (AT-4106) runs under `TASKBOARD_REQUIRE_BROWSER=1`, so a missing Playwright fails instead of skipping.

| AT | Commission | Asserts |
|---|---|---|
| AT-4101 | AT-a | stdin `2\n`, two boards: B and C for board 2, both paths printed, board 1 and the registry unchanged |
| AT-4102 | AT-b | stdin `a\n`: reports covering all boards |
| AT-4103 | AT-c | empty piped stdin: exit 2 with the list, nothing written; `q` and end of input: exit 1 |
| AT-4104 | AT-d | `--board` does not prompt; `PROJECT` scopes; an unknown project errors with the list |
| AT-4105 | AT-e | a missing `--board` path is refused and nothing is created |
| AT-4106 | AT-f | the written files load headless with 0 console errors |
| AT-4107 | CR-4 | no `Report written to`, the README tells the new story |

### 5.2 Batch acceptance criteria
- Every LLR is covered by at least one TC or AT with a passing result, or an inspection row.
- 0 blocker failures in validation; the full suite passes in 3 sequential chunks (baseline 3332 passed; only the TC-1902 skip accepted).
- Every AT and TC node mutation-checked: every mutant killed or declared.
- The validator reports 0 BLOCK at start and at close.
- `code-reviewer` (increment), `security-reviewer` (CR-5) and `qa-reviewer` (P4) are spawned, not self-executed.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
See §1.3.

### 6.2 Relevant design decisions
- **D-1** The prompt and messages go to stderr; the paths go to stdout, one per line.
- **D-2** Non-TTY stdin is read; only «not a TTY and end of input at the first read» exits 2. A TTY at end of input, or a later end of input, exits 1. The Windows NUL device reports a TTY (§2.7 row 7), so it exits 1, still without waiting.
- **D-3** `--report` never registers a `--board` path and never records «last opened».
- **D-4** `taskboard/report.py` stays byte-unchanged: `write_report`, `build_report` and `report_path` are used by `tests/test_report.py` and `report_path` is TC-3123's oracle; the commission removes entry points only when nothing else uses them. The backlog gets the retirement of the static report and its law suite.
- **D-5** With `a`, the files land in the default board's `reports/`, as `H` writes beside the open board.
- **D-6** `PROJECT` is looked up by exact name among the visible projects; the first match wins.

### 6.3 Open risks
Security questions routed by the Phase-1 scan (`security_required: true`, flag `hash`, `evidence/scan-spec.txt`), answered:
- **The flag.** `hash` matched the SHA-256 digests the tests compare to prove a file is unchanged. No credential or secret is hashed or stored; the batch has no auth surface.
- **Input surface.** One line of stdin and the argv. Both are parsed as a number, `a`, `q` or empty; nothing is executed or interpolated into a path: a board is picked only by its index in the registry's own list (LLR-4102.2). `PROJECT` is looked up by equality, never used as a path (the file name uses `report_html.slug`).
- **Printed text.** Board names and paths are file-derived; they pass `strip_controls` and have whitespace collapsed (LLR-4104.3), so they cannot inject lines or terminal sequences.
- **Reading never writes.** Missing `--board` paths are refused before `Board.load` can seed them (LLR-4104.1, closes BACKLOG's S-3 item for `--report`); the registry is not written (D-3).
- **Data exposure.** `a` puts every board's data in one folder, the same exposure as `H` scope `o` (README warns). A wrong default pick exports one board the owner did not mean: the prompt marks the default and a script must name `--board`.
- **Residual.** A pipe held open without data waits. `Registry.load` may copy an unreadable `boards.json` aside, as every start does (security S-2).

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-29-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```

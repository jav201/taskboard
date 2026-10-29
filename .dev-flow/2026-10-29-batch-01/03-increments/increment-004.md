# Increment 004 — HLR-3107 · `the H key, the export modal, the toast and the o offer`

> **Owed in.** `core` ✓ · `full` ✓
> **Reserved field names** (language-independent, parsed literally): `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`

| Field | Value |
|---|---|
| Batch | `2026-10-29-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-3101` / `HLR-3107` / `LLR-3107.1, LLR-3107.2, LLR-3107.3, LLR-3107.4, LLR-3107.5` · `LED-2026-10-29-batch-01.26` amends LLR-3107.4 |
| Acceptance | `AT-3101` · `AT-3105` · `AT-3107` · white-box `TC-3117`, `TC-3118`, `TC-3119`, `TC-3120`, `TC-3121` |
| Agent | `software-dev` (spawned implementer; the orchestrator ran the suites, the code-review and the security gate; this packet was written by a scribe from the records) |
| Date | `2026-10-29` |

---

## 1 · What changed

The reports are reachable from the app. `H` (a global key, off the bar, in the `misc` group beside `R` and `A`) opens `ReportExport`, a keys-only modal: `b` workspace, `c` deck, `a` both, `p <current project>` or `no project selected`, `o all boards (N)`, `esc close`. It marks the scope (it starts at `o`), prints the destination folder (`<board dir>\reports\`, long paths keeping their end) and the names of the boards the file will contain (PDR C9). `p` and `o` move the mark and keep the modal open; `b`/`c`/`a` dismiss with the kinds and the scope; `esc` dismisses with nothing and writes nothing. The current project is the selected task's project, else the focused project, never `present_project_id`'s first-project fallback (PDR C5: the project KEY goes to `extract`).

`action_report_export` collects every loaded board through `board_lanes(self)` (a lane whose board is `None` is skipped and counted), calls `report_html.write_reports` into `Path(self.board.path).parent / "reports"` and toasts `Report written: <names> to <dir> — o opens it (10 s)` (`title="Report"`, `severity="information"`, `timeout=10`, `markup=False`; ` · 1 board skipped` / ` · n boards skipped` when lanes were skipped). It sets a single-use offer, `self._report_offer = (path, self._report_clock() + 10)`; `action_open_url` checks it first, so the first `o` within 10 s opens the just-written file (the workspace after `a`) with `os.startfile` on Windows, else `webbrowser.open(path.as_uri())`; only a path under `<board dir>/reports/` that this export wrote (D9). `_report_clock = time.monotonic` is the one seam for the expiry (D16). The `x` export of `R` and the CLI `--report` are untouched (`git diff 9da7438` of `report.py`, `__main__.py`, `views.py`: 0 lines, TC-3121).

The review rounds added failure handling the contract had not named: a write that raises `OSError` (a partial write included) toasts `Report not (fully) written: <error>` with severity error, clears any earlier offer and offers nothing (CR4-2); an open that fails toasts `Could not open the report` (CR4-3); the `a` key binds the token `both`, mapped to the kinds tuple (CR4-1); the README `H` row carries the shared-folder warning (SA1). The wording changes are `LED-2026-10-29-batch-01.26`.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/keymap.py` | source | LLR-3107.1 | one row `Key("H", "H", "report_export", "Report", group="misc", bar=False)` with a comment in the file's style (`:146`) |
| `taskboard/modals.py` | source | LLR-3107.2 | `ReportExport` ModalScreen (`:3257`), no Button; marked scope rows, destination and board names, key line via `key_line`; built with `Text.append` (no markup) |
| `taskboard/app.py` | source | LLR-3107.3, LLR-3107.4 | `_report_clock` (`:1213`), `_report_offer` (`:1252`), `action_report_export`, `_on_report_chosen`, `_open_report` (`:1922–1978`), the offer branch in `action_open_url` (`:3598`) |
| `README.md` | doc | LLR-3107.1 | the `H` row in the global keys table (`:139`) with the shared-folder warning (SA1) |
| `tests/test_report_export_app.py` | test | HLR-3107 / AT-3101, AT-3105, TC-3117..TC-3120 | NEW, 7 nodes |
| `tests/test_modal_keys.py` | test | LLR-3107.2 / AT-3107, TC-2407 | the `"ReportExport": {}` row in `INVENTORY` and `test_AT_3107_the_report_modal_obeys_the_modal_key_law` |
| `.dev-flow/2026-10-29-batch-01/01-requirements.md`, `01-requirements-ledger.md` | doc | LLR-3107.4 | the amendment `LED-2026-10-29-batch-01.26` |
| `.dev-flow/2026-10-29-batch-01/PLAN.md`, `.dev-flow/BACKLOG.md` | doc | — | the plan's state and Test ledger row; CR4-4 as a watch item |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** (`keymap.py`, `modals.py`, `app.py`; README.md is docs) |
| Test files | 2 (uncapped) |
| Doc files | 5 (outside the count) |

## 3 · How to test

```bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
cd C:/Users/jjgh8/Github/taskboard-wt/report-proto
env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q -p no:cacheprovider   # must print a path inside report-proto
TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_export_app.py tests/test_modal_keys.py tests/test_keymap.py tests/test_help_keys.py tests/test_readme.py tests/test_app.py tests/test_report.py tests/test_report_html.py tests/test_report_workspace.py tests/test_report_deck.py
git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py | wc -l   # 0 (TC-3121)
# the mutation battery
env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-004.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none separate — the modal's pure parts (scope mark, key line, destination clipping) are asserted through the nodes below | n/a |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | `test_TC_3117_H_is_seated_once_off_the_bar` (LLR-3107.1: one `KEYMAP` row, `bar is False`, `H` in `?` and the palette, `h` keeps its meaning) · `test_TC_3118_scope_keys_and_no_project` (LLR-3107.2: scope default `o`, `p` then `o`, "no project selected", the destination line and board names) · `test_TC_3119_files_land_beside_the_open_board` (LLR-3107.3: the registry of three boards with one missing, the file names, the skipped count, 0 board files changed) · `test_TC_3120_o_opens_the_report_while_the_toast_lives` (LLR-3107.4: the toast text from the notification record, `_report_clock` replaced, `os.startfile` patched `raising=False` and `webbrowser.open` recorded, single use, expiry, main screen only with `?` open, both opener branches) · `test_TC_3120_a_failed_write_toasts_and_offers_nothing` (CR4-2) · TC-3121, the inspection pin: `git diff 9da7438` of `report.py`, `__main__.py`, `views.py` = 0 lines (`suite-004.txt`) | 5 passed (+ the TC-3121 inspection, 0 lines) |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | `test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it` (a synthetic multi-board home; `H`, `b`; the file under `<board dir>/reports/`, the toast names it, the page loaded headless in a worker thread: 0 console errors, 0 external requests) · `test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project` (slides == the chosen projects, literal counts, `p` scope → that project's slide and the board+project slugs in the name) · `test_AT_3107_the_report_modal_obeys_the_modal_key_law` (`tests/test_modal_keys.py`: the painted key line matches the six patterns, each key pressed and its effect asserted, nothing written on `esc`) | 3 passed |
| regression | `core` | the B1 census suites and the 58 nodes of increments 001–003 | green in the run below |
| increment total | — | `TASKBOARD_REQUIRE_BROWSER=1` over the ten files, 0 skipped | **314 passed** in 124.71 s (`suite-004.txt`): report_html 12, workspace 22, deck 6, keymap 24, help_keys 9, readme 11, app 170, report 18, modal_keys 35, export_app 7 |

All seven acceptance tests now have a node on disk (AT-3101, AT-3105, AT-3107 here; AT-3102..AT-3104 and AT-3106 in 001–003); the gate's `V2` rows clear with this increment. The package-scanning law suites were not re-run in this increment; they run at P4 (the plan's chunked full suite).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | 27 single-fault mutants M01–M28 (M19 dropped, see Pending items), each a one-line change aimed at one of this increment's OWN assertions; M25–M28 were written for the review fixes and M21/M23 rebased onto the fixed bytes |
| Instrument | project code, mutated by the script `evidence/mutation-004.py` (anchor-checked string replacement, `finally`-restore, per-node verdicts) |
| Where it ran | this worktree, the increment tree; the harness restores the file before the next mutant |
| Transcript | `evidence/mutation-004.txt` (the last run, 27 mutants on the final bytes, is the verdict of record) |
| Restore proven by | sha256 recorded before and after every mutant (`restored, identical`); final `keymap.py` `c4598df3ffaef0a9f55d76af55bfb10801d1f45b0a1b0ed914b7dd87d121aada`, `modals.py` `828c234b87346f3b49a69c11e254e451b92e025abe3dce6d3ef38c3a02f2f28c`, `app.py` `95cf151f1fb536563fe61217398a71c5d4e160895e9a90e7d66a1b1bf04cdbc5`, README.md `f6e47057539e005394fec6e5d0d80757ed70f6d35a122bdce160370f56cf3c43`; `report_deck.py` (M15) `5f8d062cd25c1c1be01a744e53a9e603311740cb6996eb6b2155cd5de7ccd34d` |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every run |
| Arms resolved at baseline | 27 mutants, each with its `-k` selection resolved to the named node(s) |
| Verdict granularity | per resolved node id (the transcript prints `RED nodes: [...]` for each mutant) |
| Arms that stayed GREEN | none in the final run (M19 survived in the first run and was dropped, see Pending items) |

| Field | Value |
|---|---|
| **RED counterfactual** | the ATs' own mutations: M13 (the toast drops the file name), M11 (the app's `p` scope ignored) and M15 (`report_deck` keeps archived projects, AT-3105's named control) turn AT-3101 and AT-3105 RED; M03 (the key line drops `esc close`), M24 (`a` writes only the workspace) and M25 (the `both` token maps to the workspace alone) turn `test_AT_3107_the_report_modal_obeys_the_modal_key_law` RED; M01 and M02 (the `H` row dropped, or drawn on the bar) turn TC-3117 RED · transcript `evidence/mutation-004.txt` · restore digests as in the table above |

### Mutation verdicts

| Field | Value |
|---|---|
| **Mutation verdicts** | 27/27 KILLED, none survived, none BAD in the final run, per resolved node: M01 the `H` row dropped, M02 the seat on the bar → TC-3117 · M03 the key line drops `esc close`, M23 the modal grows a Button its INVENTORY row `{}` does not name, M24 `a` writes only the workspace, M25 CR4-1 the `both` token to the workspace alone → AT-3107 (M23 also TC-2407) · M04 the destination folder never printed, M05 the board names never printed (C9), M06 `p` with no project moves the mark, M07 the scope starts at `p`, M08 `p` writes and closes → TC-3118 · M09 the current project from `present_project_id`'s fallback (C5), M12 the bare project id to `extract` instead of the key → TC-3118 / AT-3105 · M10 the files written beside the CWD, M14 the skipped board never counted → TC-3119 · M11 the app's `p` scope ignored, M15 `report_deck` keeps archived projects → AT-3105 · M13 the toast drops the file name → AT-3101 · M16 `o` keeps `open_url`, M17 the offer never expires, M18 the offer is not single-use, M20 after `a` `o` opens the deck, M21 off Windows a bare path, M22 the toast lives 5 s → TC-3120 · M26 the write unguarded, M27 the earlier offer left set after a failed write → `test_TC_3120_a_failed_write_toasts_and_offers_nothing` · M28 a failed opener says nothing → TC-3120 (CR4-3) · arms that stayed GREEN: none · transcript `evidence/mutation-004.txt` |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the painted-modal key-line read (patterns `b workspace` … `esc close`) | M03 (the key line drops `esc close`) | AT-3107 RED (`mutation-004.txt`) |
| the notification-record read (message text, severity, title) | M13, M14, M22 (the toast drops the name or the count, or lives 5 s) | AT-3101 / TC-3119 / TC-3120 RED per mutant |
| the file-system read of `<board dir>/reports/` (names, count, bytes of the boards) | M10 (written beside the CWD) | TC-3119 RED |
| the opener call record (`os.startfile` patched `raising=False`, `webbrowser.open` recorded) | M16, M17, M18, M20, M21 | TC-3120 RED per mutant |
| the loaded deck's slide count and titles | M11, M15 | AT-3105 RED |
| the `INVENTORY` law (TC-2407) | M23 (a Button added) | `test_TC_2407_every_modal_is_in_the_inventory` RED |
| the failed-write read (error toast, no offer, `o` falls through to `open_url`) | M26, M27 | `test_TC_3120_a_failed_write_toasts_and_offers_nothing` RED |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 7 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the report files written by the `H` action (the saved bytes under `<board dir>/reports/`) | AT-3101 loads the written workspace headless as `file://` (in a worker thread, per the PQ6 decision): 0 console errors, 0 external requests; AT-3105 reads the written deck's slide titles and counts | passed (`suite-004.txt`); M13, M11, M15 turn them RED |
| the toast the user reads | the notification record's message, severity and title compared to the template; the toast is not read from the painted screen | passed; M13, M14, M22 turn it RED |
| the painted modal | AT-3107 reads the modal as painted (key-line tokens by pattern) at 118x30 | passed; M03 turns it RED |
| the opener's argument | TC-3120 asserts the path handed to `os.startfile` / the URI handed to `webbrowser.open` equals the written file inside `reports/` | passed; M16, M18, M20, M21 turn it RED |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 4 artifact classes (the written report files, the toast, the painted modal, the opener's argument), each asserted in the form the user or the OS receives |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-29-batch-01/evidence/suite-004.txt | 5a4e41af6592c3321f1443e5da6882f25a11b214288de9ddb6b51a9d0cf582e4 |
| mutation-004.txt | .dev-flow/2026-10-29-batch-01/evidence/mutation-004.txt | 5a66c553e31fd526fe7ee01268fa803880810e0132a3c6afd4eac9ed56b97d97 |
| mutation-004.py | .dev-flow/2026-10-29-batch-01/evidence/mutation-004.py | 5b2c82eb81ce0c85bc43b94e3a7006f928c5e9722251f67e93571313d25ba808 |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — "no change reaches `report.py`, `__main__.py` or `views.py`" (TC-3121) and "the offer opens only a path this export wrote under `reports/`" |
| If the result is an ABSENCE, what made the search wide enough | TC-3121 is a diff against the batch's base `9da7438` over the three files (0 lines), not a grep; the opener takes `paths[0]` of this export's `write_reports` result and nothing else, which the security-reviewer traced, and M20/M21 change which path or URI it receives |
| Guard labelled as protecting a CONCLUSION, not a behaviour | TC-3121 protects the conclusion "the `x` export and the CLI report are unchanged"; it is an inspection pin, not a gate (C-40's corollary) |
| Conjunctive criteria: one mutation per conjunct | the offer: single-use (M18), expiry (M17), path (M20), URI (M21), main screen (TC-3120's `?` arm, see Pending items); the toast: name (M13), count (M14), timeout (M22); the modal: seat (M01, M02), esc (M03), destination (M04), board names (M05), `p` with no project (M06), default scope (M07), `p` keeps the modal (M08) |
| Synthetic instance of the absent case | `tests/test_report_export_app.py` builds a registry of three fixture boards, one missing, and a home with no selected task; TC-3120's failing write makes `reports` a file |
| **Positive control for every probe that returned an ABSENCE** | the TC-3121 diff is a count and fires on any edit to the three files; M20 and M21 make the opener receive another path or URI, so the opener-argument probe fires on the present case |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl KEYMAP tests/` · `grep -rl INVENTORY tests/` · `grep -rl open_url tests/` · `grep -rl build_report tests/` | the same hits as the P3 entry census. The KEYMAP readers `tests/test_keymap.py` (24), `tests/test_help_keys.py` (9), `tests/test_readme.py` (11) and `tests/test_app.py` (170) are green in the 314-pass run with the `H` row in place; `INVENTORY` is read by `tests/test_modal_keys.py`: the one planned row `"ReportExport": {}` was ADDED (the TC-2407 law passes with it; M23 proves the row is read); the `open_url` readers (`test_app`, `test_keymap`) are green with the offer branch in `action_open_url`; `tests/test_report.py` (18) is green. No existing assertion moved |
| B2 file moved on disk | n/a — no file moved (probe not fired, declared) | — |
| B3 byte-identical golden captures this source | `tests/goldens/` does not exist (P0 probe) | not fired |
| B4 artifact produced here is consumed elsewhere | `grep -rln "report_html\|report_workspace\|report_deck\|ReportExport" taskboard/ tests/` | the written files are consumed by the OS opener (`o`) and by the new tests; the modal is consumed by `action_report_export` only |
| A3 interface consumed by another module changed | `git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py \| wc -l` | 0 lines (TC-3121); `app.py` gained members, none removed or retyped; `action_open_url` gained a first branch that falls through to its old body |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run (B1 with its readers re-validated and the INVENTORY row named, B3, B4, A3 with the TC-3121 diff; B2 declared not fired); the only legitimate movement is the planned INVENTORY row |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| CR4-1: the `a` key bound `write('workspace,deck')`, a comma-split of two arguments that Textual passes as one | every modal binding that carries a multi-valued action argument | `grep -n "write(" taskboard/modals.py` | 3 (`b`, `c`, `a`) | 1 — `a` binds `write('both')`, mapped to the kinds tuple; M25 pins it | 0 |
| CR4-2: the `OSError` branch of the write was untested, and a partial write said nothing was written | every place the export writes files or sets the offer | `grep -n "write_reports\|_report_offer" taskboard/app.py` | 3 (the write, the offer set, the offer consumed) | the write branch (error toast, offer cleared), the node `test_TC_3120_a_failed_write_toasts_and_offers_nothing`, M26, M27; `LED .26` | 0 |
| CR4-3: `_open_report` was silent on failure | every opener call | `grep -n "startfile\|webbrowser.open" taskboard/app.py` | 2 (`os.startfile`, `webbrowser.open`) | both fail visibly (toast `Could not open the report`); M28 pins it | 0 |
| SA1 (security, info): `reports/` lands beside the open board, a synced or versioned folder would carry an `o`-scope file with every loaded board | every place the README or the modal names the destination | `grep -n "reports" README.md taskboard/modals.py` | 2 (the README `H` row, the modal's destination line) | the README row gained the shared-folder warning; the modal already prints the folder and the board names | 0; D8 accepted, the PU3 question to the operator goes on the review page |
| Deviation 1: the main-screen guard in the offer branch | the offer's consumers | `grep -n "_report_offer" taskboard/app.py` | 2 | the guard removed (unreachable, see Pending items); M19 dropped | 0 |

| Field | Value |
|---|---|
| **Correction population** | 5 corrections (CR4-1, CR4-2, CR4-3, SA1, deviation 1), each enumerated with its method and its count; all edited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| `<n> board(s) skipped` in LLR-3107.4 | `grep -n "board(s)" .dev-flow/2026-10-29-batch-01/01-requirements.md` | yes — the live statement now gives `1 board skipped` / `n boards skipped`; the ledger keeps the before text | `01-requirements.md` LLR-3107.4; `01-requirements-ledger.md` LED .26 |

### Signed-balance test ledger

`post = base − deleted + added` → `314 = 306 − 0 + 8`  ✓ reconciles: the base is the 306 nodes of the ten files before this increment (58 of 001–003, app 170, keymap 24, help_keys 9, readme 11, modal_keys 34); this increment adds 8 nodes (7 in `tests/test_report_export_app.py`, `test_AT_3107_…` in `tests/test_modal_keys.py`); no node deleted. The first run, before the review fixes, was 313 (the CR4-2 node is the 314th).

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | code-reviewer — spawned as a generic agent with agents/code-reviewer.md · OK to advance (with notes) · 0 HIGH; CR4-2 MEDIUM (the `OSError` path untested) resolved with a test and a mutant; CR4-1 and CR4-3 LOW fixed; CR4-4 noted; the fixes were NOT re-read by the code-reviewer (declared) |

Reading: 0 HIGH; the reviewer re-ran 65 tests (export_app, modal_keys, keymap). Deviation 1 (the main-screen guard dropped) verified safe: `o` has no priority, the modal binding chain stops before the app's bindings, `check_action` returns only `quit` under home/agenda/people/marks, and TC-3120 pins the behaviour with `?` open. Findings: CR4-1 (LOW, `modals.py:3269,:3314`, the comma split) fixed; CR4-2 (MEDIUM, `app.py:1945-1949`, the `OSError` branch untested, a partial write says nothing was written) fixed with a test, the wording `Report not (fully) written` and mutants M26/M27; CR4-3 (LOW, `app.py:1963-1975`, `_open_report` silent on failure) fixed; CR4-4 (LOW, tests read `app._notifications` and `_report_clock`) accepted as the D16 seam and entered in `.dev-flow/BACKLOG.md` as a watch item for Textual upgrades.

Security: security-reviewer at the gate — PASS (6 passed in its run). Verified: the opener gets `paths[0]` of this export's `write_reports`; the folder is the board's parent plus `reports`; file names are fixed kind words, the date and alphanumeric-or-`-` slugs (no separator, no `..`, a kind prefix, so no reserved device name), so hostile names cannot redirect the write; the offer is single-use, cleared on the first `o` and checked against its 10 s deadline; the opener is `os.startfile` else `webbrowser.open(as_uri())` with `OSError` swallowed; no board text is executed; the modal is built with `Text.append` (no markup); the toasts use `markup=False`; a write `OSError` toasts an error with no traceback. SA1 (minor, info): a synced or versioned folder carries an `o`-scope file with every loaded board; D8 accepted; disposition: the README sentence and the PU3 question to the operator on the review page. The fixes (CR4-1..3, the README line) were applied after the security-reviewer read; M25–M28 and the TC-3120 failed-write node are their pin.

---

## 5 · Risks

- **CR4-4 (watch item):** the tests read Textual's private `app._notifications` and the app's `_report_clock`; a Textual upgrade can rename the first. The nodes fail loudly, not silently. In `BACKLOG.md`.
- **SA1 / D8 (accepted):** the `o` scope writes every loaded board's data into `reports/` beside the open board; in a shared or synced folder others can read it. The modal prints the folder and the board names; the README warns; PU3 asks the operator.
- **The review fixes were not re-read by a reviewer** (declared in §4b); their pin is M25–M28 and the TC-3120 failed-write node.
- **Partial writes are possible:** workspace written, deck failed; the toast says `not (fully) written`, no offer is made, the written file stays on disk.
- **Browser tests do not run in CI:** Playwright is not a declared dependency; this machine's transcripts (`suite-004.txt`, `mutation-004.txt`) are the evidence of record.
- **Flaky baseline test:** `test_win_clipboard_roundtrip` (TC-1902, the clipboard) failed once in a baseline run and passed on re-run; the accepted skip family, outside this change.
- **The mutation harness anchors on source text:** a later edit to those lines makes a mutant `SETUP-ERROR`; the harness reports it rather than passing.

## 6 · Pending items / spec deviations

- **Deviation 1, the main-screen guard removed:** the implementer's explicit "main screen only" check in the offer branch was unreachable (an `o` over another screen never reaches `action_open_url`), so its mutant M19 survived on the first run; the guard was removed, M19 dropped, the survivor recorded in `mutation-004.txt`, and TC-3120 checks the behaviour from outside with `?` open. The code-reviewer verified it safe. The requirement's behaviour is unchanged (recorded in `LED .26`).
- **Deviation 2, the archive sweep:** opening Client A auto-archives `st1` (done 20 days ago, the app's sweep), so the tests expect `10 tasks · 2 archived`.
- **Deviation 3, new failure toasts:** `Report not (fully) written: <error>` and `Could not open the report` are not in the original LLR; recorded as `LED-2026-10-29-batch-01.26` (LLR-3107.4).
- **Deviation 4, the plural:** the skipped count reads `1 board` / `n boards` (the contract said `board(s)`); `LED .26`.
- **Deviation 5, the opener branch:** it checks `hasattr(os, "startfile")` so TC-3120 tests both branches on one machine.
- **Deviation 6, `a` binds `both`:** Textual passed only the first of two action arguments, so the comma form failed; fixed as CR4-1.
- **Requirement amendment:** `LED-2026-10-29-batch-01.26` (LLR-3107.4). The frozen dict shape is untouched, so the PDR is not re-opened.
- **Increment-004-owned conditions, all discharged:** C5 (the key to `extract`), C8 (single-use offer, main screen), C9 (board names in the modal), D9 (only a path written by this export), D10, D16 (the clock seam), PU3 (the operator question goes on the review page), the toast, offer and destination rules.
- **Carried:** CR3-4, CR3-5 and CR4-4 in `BACKLOG.md`; CR5 (the Inbox key collision) from increment 001; the package-scanning law suites and the chunked full suite at P4.

## 7 · Suggested next task

P3 closes. DDR (design-detail review): the ux-reviewer's seven observable criteria walk the real `H` modal, the toast and the written reports; then P4 (the full suite in 3 sequential chunks, the package-scanning laws, the validation record).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 3 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 7 nodes in `tests/test_report_export_app.py`, AT-3107 in `tests/test_modal_keys.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | §4: no unit is separate from its TC node |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4: the ATs' own mutants · `evidence/mutation-004.txt` · restore digests |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4: 5 probes; KEYMAP, INVENTORY and `open_url` readers green; the INVENTORY row named |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b: OK to advance with notes, 0 HIGH; the fixes not re-read (declared) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | TC-3121: `report.py`, `__main__.py`, `views.py` diff 0 lines vs `9da7438`; the dict shape unchanged |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `suite-004.txt` (314 passed), `mutation-004.txt` (27 KILLED); digests in the evidence rows |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 table with positive controls |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | §4: 27 mutants, per-node verdicts, none green |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4: 7 instruments |
| 13 | **Correction population** declared | all | ✓ | §4: 5 corrections with methods |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4: the written files, the toast, the painted modal, the opener's argument |
| 15 | **Independent review** names somebody | all | ✓ | §4b: code-reviewer and security-reviewer |
| 16 | **Evidence files** declared | all | ✓ | §4: rows written by `devflow-evidence.py` |

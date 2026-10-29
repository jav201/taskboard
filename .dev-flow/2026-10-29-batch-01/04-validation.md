# Validation — taskboard — Batch 2026-10-29-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)

> **Reserved field names.** `Result` · `Gate run` · `Layer 0` · `Evidence checklist` · `⏸ DEFER` — parsed literally, never translated.
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.

- **Result:** PASS-WITH-NOTES
- **Gate run:** `env -u NO_COLOR TASKBOARD_REQUIRE_BROWSER=1 python -m pytest -q -rs -p no:cacheprovider tests/<117 files in 3 disjoint chunks>` (driven by the orchestrator's `run_p4.sh`; each chunk's exact command line is the `cmd:` header of its transcript) ·
  exit 0 on all three chunks · HEAD `18e6057` (`18e605706b7810f890d9aa129ae345b9c1e51b98`, the toast re-shot commit; `git diff 7b47714 18e6057` touches capture evidence and records only — no source change after increment 005's code) · executed by the orchestrator (C-25), three SEQUENTIAL chunks, nothing in parallel:
  chunk00 **1443 passed** (`evidence/suite-p4-chunk00.txt`, 296.75 s), chunk01 **1025 passed** (`evidence/suite-p4-chunk01.txt`, 460.06 s), chunk02 **864 passed** (`evidence/suite-p4-chunk02.txt`, 177.66 s) · total **3332 passed, 0 failed, 0 skipped**. The file list is `evidence/suite-p4-files.txt` (117 files = `ls tests/test_*.py`; the helpers `tests/report_browser.py` and `tests/report_fixture.py` hold no tests).
- **Baseline reconciliation:** commission baseline 3281 (Windows) + 51 new nodes since `d117ea0` (`tests/test_report_html.py` 12, `tests/test_report_workspace.py` 25, `tests/test_report_deck.py` 6, `tests/test_report_export_app.py` 7, `tests/test_modal_keys.py` +1 — AT-3107) = 3332 expected = 3332 passed. `tests/test_report.py` (pre-existing, 18) is inside chunk02 and unchanged.
- **Clipboard delta (named, not smoothed):** the commission allows one skip, TC-1902 (`tests/test_app.py`, chunk00). This run TC-1902 RAN and PASSED — 0 skips in all three chunks. `TASKBOARD_REQUIRE_BROWSER=1` was set, so no browser node could skip either (§5.1, `LED-2026-10-29-batch-01.15`).
- **Layer 0:** none — no unit met the decision or boundary criterion apart from its TC node (each packet's checklist row 3); the decision-bearing units (`extract`'s keys, scope and status rule, `embed_json`, `notes_html`, `slug`, the deck's slide rule) are verified by their unit TCs, each with a named reddening mutant in `evidence/mutation-001.txt` / `mutation-003.txt` (table below).
- **Requirements:** 26/26 pass (7 HLR + 19 LLR) · 0 blocker fails.
- **Black-box acceptance (Layer B):** ✓ every story's AT observes its outcome through the shipped surface (boundary + negative): AT-3101..AT-3107 each realise in exactly one on-disk node (C-18), re-executed inside the green chunks (AT-3107 in chunk01, the other six in chunk02); plus the family-D painted evidence — 11 headless-browser captures and 3 real Windows Terminal PNGs at 118x30.
- **Surface-reachability (bidirectional):** ✓ all named inputs (the `H` key and the modal keys, the five filter kinds, the URL hash, hostile board text and URLs) AND outputs (the two report files, the downloaded view, the CSV/JSON, the print view, the deck's slides, the toast and the `o` open) reached/observed at the surface.
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative — `increment-001.md` (the one-form filter label), `increment-002.md` (TC-3105's Tab list 43→45, named), `increment-003.md`, `increment-004.md` (`board(s) skipped`), `increment-005.md` (`All loaded boards` in the downloaded header; the one-line toast: 0 hits).
- **Test ledger:** ✓ reconciles (`base − D + A = post`) — base 3281 − D 0 + A 51 = post 3332; actual 3332 (1443 + 1025 + 864); passed/full 3332/3332.
- **Evidence checklist (qa-reviewer):** qa-reviewer — spawned as a generic agent with agents/qa-reviewer.md · accept with notes (V1–V4, below) · 10 of 10 rows ✓ with evidence.

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part. — every line is ✓; the PASS-WITH-NOTES carries the qa notes V1–V4 and the TC-3121 inspection pin (G-001).

---

## Detail (reference)

### Layer 0 — unit

`none — no unit met the decision or boundary criterion` apart from its TC node: the packets (`increment-001.md` … `increment-005.md`, checklist row 3) declare that every decision-bearing unit is exercised by its own unit TC, so the units are listed here with those TC nodes and their reddening mutants.

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `report_html.extract` (keys, scope, Inbox, deps cut) | boundary (board files → the dict) + branches | `tests/test_report_html.py::test_TC_3101_extract_is_json_and_holds_every_fact`, `::test_TC_3103_project_scope_keeps_one_project` | pass — chunk02; executed by the software-dev implementer at P3 (`suite-001.txt`), re-executed by the orchestrator's gate |
| the one status rule / due word | decision (archived > done > late > open; finished work never late) | `::test_TC_3125_one_status_rule`, `::test_TC_3102_due_words_are_the_cli_reports` | pass — same |
| `embed_json`, `notes_html` | boundary (board text → HTML) | `::test_TC_3115_embed_json_and_notes_are_inert` | pass — same |
| the http(s) URL filter in `extract` | decision (scheme whitelist) | `::test_TC_3124_extract_keeps_only_http_urls` | pass — same |
| `slug` / file names | decision | `::test_TC_3123_the_slug_is_the_cli_reports` | pass — same |
| the renderers read the dict only | boundary (import direction) | `::test_TC_3104_renderers_read_the_dict_only` | pass — same |
| the deck's slide rule | decision (archived / task-less / all-archived) | `tests/test_report_deck.py::test_TC_3113_one_slide_per_project` | pass — same (`suite-003.txt`) |

**Measured by mutation, never by line coverage.** Executed by the spawned implementers; transcripts kept beside their harnesses:

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| `extract` keys | M01 projects keyed by the bare id | ✓ KILLED | `evidence/mutation-001.txt` |
| `extract` scope | M04 the scope ignores `project` | ✓ KILLED | `mutation-001.txt` |
| status rule | M13 late derived with `<=`; M30/M31 done tasks pass `closed=False` | ✓ KILLED | `mutation-001.txt`, `mutation-003.txt` |
| due word | M03 the due word formatted locally | ✓ KILLED | `mutation-001.txt` |
| `embed_json` / `notes_html` | M08 the prototype's `</`-only replace; M09 a notes piece unescaped | ✓ KILLED | `mutation-001.txt` |
| URL filter | M12 the filter dropped; M08 (003) the same through both files | ✓ KILLED | `mutation-001.txt`, `mutation-003.txt` |
| `slug` | M10 lower-cases only; M11 the board slug dropped | ✓ KILLED | `mutation-001.txt` |
| import direction | M05 module-level renderer import; M06/M29 a renderer imports `views.HEX`; M07 dynamic import | ✓ KILLED | `mutation-001.txt`, `mutation-003.txt` |
| deck slide rule | M16 archived project gets a slide; M17 task-less project; M18 all-archived gets none; M19 count includes archived | ✓ KILLED | `mutation-003.txt` |

Batch totals: 35/35 (`mutation-001.txt`), 40/40 (`mutation-002.txt`), 37/37 (`mutation-003.txt`), 27/27 (`mutation-004.txt`), 15/15 (`mutation-005.txt`) — 154/154 KILLED, 0 survivors. (`mutation-001.txt` also holds an earlier run whose M35 was a SETUP-ERROR; the final run in the same file kills all 35.)

### UX walkthrough — trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| Press `H`: the modal names the folder, the boards and every key (`b c a`, `p`/`o`, `esc`), scope `o` marked | real `TaskboardApp` in Windows Terminal (`wt.exe`), 118x30, synthetic home | READY check on the live composited frame: `ReportExport` on top, `● all boards (3)`, the board names, `Writes to … reports`, the key words | pass — `evidence/captures/terminal/png/report-modal_118x30.png`; executor: orchestrator |
| Press `p`: the scope mark moves to the current project, the modal stays | same | `● Storefront relaunch on Client A`, same folder and keys | pass — `report-modal-p_118x30.png` |
| Press `b`: one toast names the file and the folder and offers `o` | same | exactly one `Report` toast, the three lines of LED .27, the file exists | pass — `report-toast_118x30.png` (re-shot at `7b47714`); the long temp folder path wraps mid-word (residual, low — BACKLOG) |
| The workspace at 1366/390 px, light/dark; the configured view, the print preview, the downloaded view; the deck at 1366/390 px, light/dark | headless Chromium over the files `write_reports` wrote | 11 shots, 0 console errors, 0 external requests, 0 hidden task titles in the downloaded view (`evidence/captures/capture-log.json`: `errors: []`, `external: []`) | pass — `evidence/captures/*.png`; the re-shot print preview reads `Boards in this view (1): Client A` with every table column (`DDR-2026-10-29-batch-01#D1`) |
| Leave no trace | n/a | `no hx-* window left open`; no `hx-cap-*` home, `hx-*.ready`/`.cmd` left in TEMP | pass — `evidence/captures/terminal/README.md` §Results |

**Mechanism used:** a UI test driver — real terminal windows of the shipped app with scripted keys and a content check on the live frame; a headless-browser driver (Playwright Chromium) for the written HTML files.

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed — the terminal harness (`shoot.ps1`/`shoot_real.py`, 3/3 on try 1) and the orchestrator's browser shooter (11 shots), by the orchestrator |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | performed — the DDR ux-reviewer's seven observable criteria (DDR §B) and the orchestrator's reading O1–O3; the qa-reviewer at P4 did not open the PNGs (note V3) |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — one-person team; no user population exists to recruit. The operator's review page `review.html` asks for a judgement of the HR-3 controls; it is not a user evaluation. |

- **Method:** scripted walkthrough over the synthetic fixture (`tests/report_fixture.py`: Personal / Client A / Course, TODAY 2026-10-29), nothing in the real home.
- **Participants or population:** n/a — no user evaluation performed (one-person team).
- **Evidence of the evaluation:** `evidence/captures/` (11 PNGs, `capture-log.json`, `reports/` HTML + PDF) and `evidence/captures/terminal/` (README, 3 PNGs, `png/capture-log.txt`).
- **Limits:** the real browser print dialog was not exercised (print emulation only); the expert inspection is reviewer agents against their own criteria; nothing here establishes usability with a real audience.

### Layer A — functional (white-box): per-requirement results

All rows executed by the orchestrator's P4 gate (C-25) unless named; the run is `-q`, so a node's pass is inferred from its file inside a chunk with 0 failed and 0 skipped (note V1).

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|---|---|---|---|---|---|
| HLR-3101 | test | AT-3105's `a` arm + LLR-3101.1..3's TCs; `tests/test_report.py` | deck titles == workspace projects with a slide; per-project `<n> tasks` == the fixture literals; `test_report.py` 18 passed | pass | chunk02 (864 passed) |
| HLR-3102 | test | `tests/test_report_workspace.py::test_AT_3102_filters_and_the_hash_round_trip` + TC-3105..3108 | shown ids == the truth table (0 extra, 0 missing) per filter kind; count == non-default filters; the hash round trip identical | pass | chunk02 |
| HLR-3103 | test | `tests/test_report_workspace.py::test_AT_3103_download_this_view_holds_only_the_filtered_tasks` + TC-3109..3111, TC-3122 | downloaded ids == shown ids; every dropped unique token 0 times, raw and JSON-escaped | pass | chunk02 |
| HLR-3104 | test | `tests/test_report_workspace.py::test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` + TC-3112 | under print media 0 visible controls, card, tooltip; the header visible with the filter summary; width at 794 px (DQ4) | pass | chunk02 |
| HLR-3105 | test | `tests/test_report_export_app.py::test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project` + TC-3113, TC-3114 | slides == 2 + the literal project count; `End`/`Home` counters | pass | chunk02 |
| HLR-3106 | test | `tests/test_report_deck.py::test_AT_3106_board_text_is_escaped_in_both_reports` + TC-3115, TC-3116, TC-3124 | 0 dialogs; the literal `<script>alert(1)</script>` visible; 0 `<script>alert(1)` in the bytes; 0 non-http(s) anchors | pass | chunk02 |
| HLR-3107 | test | `tests/test_report_export_app.py::test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it`, `tests/test_modal_keys.py::test_AT_3107_the_report_modal_obeys_the_modal_key_law` + TC-3117..3120 | 1 file under `reports/`; 1 toast with the LED .27 text; 0 console errors, 0 external requests; `o` within 10 s → 1 open | pass | chunk02 (AT-3101), **chunk01** (AT-3107, 1025 passed) |
| LLR-3101.1 | test (unit) | TC-3101, TC-3124, TC-3125 | JSON round trip; task count; unique keys; http(s) only | pass | chunk02; M01, M12 KILLED |
| LLR-3101.2 | test (unit) + inspection | TC-3102; `git diff 9da7438 -- taskboard/report.py tests/test_report.py` | 0 due-word mismatches; diff 0 lines; 18 passed | pass | chunk02; each packet §2; `suite-005.txt` |
| LLR-3101.3 | test (unit) + inspection | TC-3103, TC-3104 (the AST walk over the three renderers) | scope `p` 1 project; 0 banned imports; `render(d) == render(d)` | pass | chunk02; M04–M07, M29 KILLED |
| LLR-3102.1 | test (e2e) | TC-3105, TC-3108 | native controls only; the hand-enumerated Tab list (45 after 002); Reset restores the defaults | pass | chunk02; M14, M15, M25 KILLED |
| LLR-3102.2 | test (e2e) | TC-3106 (6 arms; the dates arm literal — DQ5) | per arm shown == expected | pass | chunk02; M16–M22 (001), M10 (005) KILLED |
| LLR-3102.3 | test (e2e) | TC-3107 | 0 dialogs, 0 `img`, `value` == `<b>x</b>` | pass | chunk02; M23, M24 KILLED |
| LLR-3103.1 | test (e2e) | TC-3109, TC-3110 | ids == shown; 0 unused directory entries; notes off → 0 notes and mentions | pass | chunk02; `mutation-002.txt` |
| LLR-3103.2 | test (e2e) | TC-3111 | the file-name pattern; multisets equal; `Boards in this view (N)` (DU5) | pass | chunk02; M06 (005) KILLED |
| LLR-3103.3 | test (e2e) | TC-3122 | CSV/JSON rows == shown; the formula guard on `= + - @` | pass | chunk02; `mutation-002.txt` |
| LLR-3104.1 | test (e2e) | TC-3112 (+ the three increment-005 arms) | 0 visible controls under print; the table ends inside the page; only the shown boards named; no `/N` | pass | chunk02; M01–M05, M07, M08, M11–M15 (005) KILLED |
| LLR-3105.1 | test (unit) | TC-3113 | slides == 2 + the literal count; `1 task` / `N tasks` | pass | chunk02; M16–M20 (003) KILLED |
| LLR-3105.2 | test (e2e) | TC-3114 | `N / N` after `End`; `1 / N` after `Home`; break-after on N/N | pass | chunk02; M21–M28 (003) KILLED |
| LLR-3106.1 | test (unit) | TC-3115 + AT-3106 | 0 `<`/`>`/`&` in the embed; `&lt;b&gt;` in the notes | pass | chunk02; M08, M09 (001), M01–M07, M33–M37 (003) KILLED |
| LLR-3106.2 | test (e2e) | TC-3116 over both files | 0 requests; 0 non-http(s) anchors; no horizontal scroll at 390 px, light and dark | pass | chunk02; M11–M15 (003) KILLED |
| LLR-3107.1 | test (unit) | TC-3117 + the census suites `test_keymap`, `test_help_keys`, `test_readme` | 1 `H` row, `bar False`; in the palette and `?` | pass | chunk02 (TC-3117, `test_readme`), chunk01 (`test_keymap`, `test_help_keys`) |
| LLR-3107.2 | test (integration) | AT-3107 + TC-3118 | the key line 6/6 patterns; `p` marks; `esc` 0 files; `INVENTORY["ReportExport"] == {}` | pass | chunk01 (AT-3107), chunk02 (TC-3118) |
| LLR-3107.3 | test (integration) | TC-3119, TC-3123 | `a` 2 files; slugged names; the missing board counted; 0 board bytes changed | pass | chunk02; `mutation-004.txt` |
| LLR-3107.4 | test (integration) | TC-3120 | 1 notification == the template; `o` < 10 s → 1 open inside `reports/`; after 10 s → `open_url` | pass | chunk02; M20 (004), M09 (005) KILLED |
| LLR-3107.5 | inspection | TC-3121 — **an inspection pin, not a node** (DQ6, `DDR-2026-10-29-batch-01#D3`): `git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py` at each packet §2; the present and report suites re-run here | diff 0 lines; the suites 0 failed | pass | `suite-005.txt` (diff 0 lines); the `test_present*` files (chunk01/chunk02) and `tests/test_report.py` (chunk02) all inside green chunks |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-3101 / HLR-3107 | AT-3101 → `tests/test_report_export_app.py::test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it` | the app by keys (`H`, `b`) | `reports/workspace-<today>.html` loaded headless (0 console errors, 0 external requests) + the toast | ✓·✓·✓ | pass — chunk02; executor: orchestrator |
| US-3101 / HLR-3102 | AT-3102 → `tests/test_report_workspace.py::test_AT_3102_filters_and_the_hash_round_trip` | the written workspace in headless Chromium, real clicks and keys | the shown rows, the count, `location.hash` re-opened | ✓·✓·✓ | pass — chunk02; executor: orchestrator |
| US-3101 / HLR-3103 | AT-3103 → `tests/test_report_workspace.py::test_AT_3103_download_this_view_holds_only_the_filtered_tasks` | the "Download this view" control | the downloaded file's bytes (raw + JSON-escaped token search), re-opened headless (B4) | ✓·✓·✓ | pass — chunk02; executor: orchestrator |
| US-3101 / HLR-3104 | AT-3104 → `tests/test_report_workspace.py::test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` | print emulation after `beforeprint` | the computed styles of the controls, card, tooltip and header at 794 px | ✓·✓·✓ | pass — chunk02; executor: orchestrator |
| US-3101 / HLR-3105 | AT-3105 → `tests/test_report_export_app.py::test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project` | the app by keys (`H o c`, `H p c`), then the deck's keys | `reports/deck-<today>.html`: slide count, titles, counters | ✓·✓·✓ | pass — chunk02; executor: orchestrator |
| US-3101 / HLR-3106 | AT-3106 → `tests/test_report_deck.py::test_AT_3106_board_text_is_escaped_in_both_reports` | both written files, loaded and paged | 0 dialogs; the literal hostile text; the bytes | ✓·✓·✓ | pass — chunk02; executor: orchestrator |
| US-3101 / HLR-3107 | AT-3107 → `tests/test_modal_keys.py::test_AT_3107_the_report_modal_obeys_the_modal_key_law` | `H`, then each modal key | the painted key line and each key's effect | ✓·✓·✓ | pass — **chunk01**; executor: orchestrator |

All Layer B rows: executed at P3 by the software-dev implementers (`suite-001.txt` … `suite-005.txt`) and re-executed in the orchestrator's P4 gate. The P4 run is the execution of record; the qa-reviewer consumed it and did not run it. The run is `-q`: a node's pass is inferred from its file in a chunk with 0 failed and 0 skipped (note V1).

### Bidirectional surface-reachability matrix

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | the `H` key and the modal keys `b c a p o esc` | `keymap` → `ReportExport` | yes — pilot by keys, and the WT captures | AT-3101, AT-3107, TC-3118 | ✓ |
| input | the five filter kinds (project, status, person, class, date) + search | the page's filter state | yes — real clicks and keys in Chromium | AT-3102, TC-3106 | ✓ |
| input | the URL hash (incl. a hostile one) | the hash parser | yes — the page opened at the hash | AT-3102, TC-3107 | ✓ |
| input | hostile board text and task URLs | `extract` → `_e` / `textContent` / `embed_json` | yes — the hostile fixture through both files | AT-3106, TC-3115, TC-3124 | ✓ |
| output | `reports/workspace-<date>.html` / `deck-<date>.html` | `report_html.write_reports` | yes — the files on disk, loaded headless | AT-3101, AT-3105 | ✓ |
| output | the downloaded view, the CSV and the JSON | the page's download code | yes — `expect_download` bytes, re-opened | AT-3103, TC-3111, TC-3122 | ✓ |
| output | the print view | `@media print` | yes — print emulation, computed styles; the print-preview capture | AT-3104, TC-3112 | ✓ |
| output | the toast and the `o` open | the app's notification + the opener | yes — the notification record, the patched opener, the WT toast capture | AT-3101, TC-3120 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 3281 (commission baseline, Windows) | 0 | 51 | 3332 | 3332 (1443 + 1025 + 864, 3 chunks) | 3332 / 3332 | yes |

### Gaps detected

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | LLR-3107.5 | TC-3121 has no test node; it is an inspection pin (DQ6, `DDR-2026-10-29-batch-01#D3`) | minor | none — recorded as inspection, discharged by the 0-line diff and the green suites |
| G-002 | HLR-3104 | the real browser print dialog (its header and footer under `@page { margin: 0 }`) is inspected, not driven | minor | none in this batch — a declared limit |
| G-003 | the browser ATs | CI installs no browser, so CI skips the browser nodes; their evidence is this machine's transcripts | minor | declared in `01-requirements.md` §6.3; CI work is the cross-platform BACKLOG item |

### Escaped-bug regression (if a defect escaped the suite)

| Regression id (`AT-NNN` / `TC-NNN`) | Pre-fix run (evidence it FAILED) | Pre-fix RED kind (value / shape) | Post-fix value-discriminating? (QC-2) | Post-fix result | Reconciled node |
|-------------------------------------|----------------------------------|----------------------------------|----------------------------------------|-----------------|-----------------|
| TC-3112's table and scope arms (DDR DQ1/DQ2, missed by the 001–004 suite) | the DDR's captures before 005 and increment 005's RED counterfactual (`03-increments/increment-005.md` §4) | value | yes — mutants M01–M05, M11–M15 restore the clipped table or the hidden names and redden (`evidence/mutation-005.txt`) | pass | `tests/test_report_workspace.py::test_TC_3112_the_print_rules_hold`, `::test_TC_3112_the_printed_header_names_only_the_shown_boards`, `::test_TC_3112_a_project_file_with_its_project_hidden_prints_no_name` |

### QA-P4 notes (folded — none forces iterate)

| # | Severity | Note | Fold |
|---|---|---|---|
| V1 | info | the run was `-q`: a node's pass is inferred from its file inside a chunk with 0 failed, not read per node | named in the Layer A and Layer B preambles |
| V2 | minor | confirm `BACKLOG.md` holds CR3-4, CR3-5, CR4-4, CR5 (the Inbox key) and the DDR notices (the opaque modal backdrop, the faint dashed export buttons) | discharged at the close — `05-close.md` §4 |
| V3 | info | the qa-reviewer did not open the PNGs; the orchestrator and the DDR ux lens viewed them | named in the UX walkthrough's expert-inspection row |
| V4 | info | 3 chunks are acceptable: disjoint, together the 117 files, and they reconcile | the Gate run line and the ledger |

### Evidence checklist — qa-reviewer (full)

qa-reviewer (evaluation; execution attributed per row) — 10 of 10 ✓:

- [✓] Import probe from the worktree root — `evidence/import-probe.txt`: `taskboard.__file__ = C:\Users\jjgh8\Github\taskboard-wt\report-proto\taskboard\__init__.py` (orchestrator)
- [✓] Every pytest under `env -u NO_COLOR` — the `cmd:` header of each P4 chunk; the P3 transcripts `evidence/suite-001.txt` … `suite-005.txt`
- [✓] The full suite in 3 SEQUENTIAL chunks with transcripts — `evidence/suite-p4-chunk00.txt`, `suite-p4-chunk01.txt`, `suite-p4-chunk02.txt`, the file list `evidence/suite-p4-files.txt`; 3332 passed, 0 skipped (orchestrator)
- [✓] Baseline reconciliation — 3281 + 51 = 3332; TC-1902 passed (no skip)
- [✓] Mutation of the new tests — `evidence/mutation-001.txt` … `mutation-005.txt` (35/35, 40/40, 37/37, 27/27, 15/15), the harnesses `mutation-00N.py` beside them (software-dev implementers)
- [✓] Browser screenshots — `evidence/captures/` 11 PNGs (both reports at desktop and phone width, light and dark; the configured view; the print preview; the downloaded view), `capture-log.json` 0 errors / 0 external; `evidence/captures/reports/` the generated HTML + PDF (orchestrator)
- [✓] Terminal capture at 118x30 — `evidence/captures/terminal/png/report-modal_118x30.png`, `report-modal-p_118x30.png`, `report-toast_118x30.png`; `hx-` titles, closed by title, `no hx-* window left open` (orchestrator)
- [✓] The review page — `.dev-flow/2026-10-29-batch-01/review.html` (Spanish prose, the screenshots, links to the generated files; orchestrator)
- [✓] Layer B: every AT observes the deliverable through the shipped surface with boundary + negative evidence; one node each (C-18)
- [✓] No real PII or secrets — the synthetic fixture only (`tests/report_fixture.py`; the capture homes are fresh TEMP folders); mode declared `validation`; no unfilled template placeholders in the returned rows

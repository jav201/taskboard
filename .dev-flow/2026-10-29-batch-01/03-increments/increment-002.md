# Increment 002 — HLR-3103 · HLR-3104 · `export the configured view: print and the filtered download`

> **Owed in.** `core` ✓ · `full` ✓
> **Reserved field names** (language-independent, parsed literally): `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`

| Field | Value |
|---|---|
| Batch | `2026-10-29-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-3101` / `HLR-3103` · `HLR-3104` / `LLR-3103.1, LLR-3103.2, LLR-3103.3` · `LLR-3104.1` (LLR-3103.1 as LED .24 amended it) |
| Acceptance | `AT-3103` · `AT-3104` · white-box `TC-3109..TC-3112`, `TC-3122` |
| Agent | `software-dev` (spawned implementer; the orchestrator ran the suites, the code-review and the security gate; this packet was written by a scribe from the records) |
| Date | `2026-10-29` |

---

## 1 · What changed

The workspace page can now leave the app's data behind in two controlled ways. "Print / Save as PDF" prints what is shown, and "Download this view" writes a new self-contained HTML file that holds only the tasks the current view keeps. Both sit in an "Export this view" group with their captions visible next to them, without hover, at 1366 and 390 px; the CSV and JSON buttons are labelled "visible rows only". Nothing in the app reaches the page yet (the `H` key and the modal are increment 004); the surface is still the file `write_reports(...)` writes and a browser opens.

Mechanism. Print: the print control and the browser's `beforeprint` event call the same function, which stamps the printed date in the view header; `@media print` hides every control, the task card and the tooltip, shows the view header (filters applied, generated date, printed date, scope line), keeps the full-gantt fix (`#gantt{min-width:0!important}`, plus an SVG `viewBox` so the timeline scales rather than clips), sets `@page { margin: 0 }` with the body padding applied in print (so the browser prints no path or URL), sets `break-inside: avoid` on rows and cards, and counts kept tasks only. Download: the pristine shell is captured at load, before the first render; the new file is that shell with `#board-data` replaced through a `DOMParser` and `textContent` (no `String.replace` pattern semantics, D3, so a task titled `$&` or `$'` cannot re-insert the shell); the data is reduced by an allowlist build (`reduce`) to the kept tasks and what they use, dependency and chain keys of dropped tasks are cut, `notes_html` and `notes_text` are stripped when the notes section is off, `meta.scope` board names and the header's board count follow the kept boards (R3), `meta.view` carries the summary, the export date and the hash state and is restored through `parseHash` on open (D5), and the JSON is escaped for `<`, `>`, `&` client-side. The file is named `workspace-view-<date>.html`, opens with 0 console errors on the same view, and its header says it is a filtered view. CSV and JSON export the visible rows only, reduced the same way, with the formula guard (a `'` prefix on cells beginning `=`, `+`, `-`, `@`, TAB or CR, except plain numbers, C13).

Review fixes landed in this increment: CR2-1 (MEDIUM, the download's re-derived project facts), CR2-2 and CR2-3 (LOW), and the security finding SD1 (mentions of withheld notes). SD1 and CR2-1 amend the contract as `LED-2026-10-29-batch-01.24`.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/report_workspace.py` | source | HLR-3103, HLR-3104 / LLR-3103.1, LLR-3103.2, LLR-3103.3, LLR-3104.1 | the "Export this view" group and captions, `@media print` and `@page`, `PRISTINE`, `reduce`, `keptCounts`, `scriptSafe`, `downloadView`, `printView`/`setPrinted`/`beforeprint`/`afterprint`, the `csvCell` guard, `exportRows`, `viewFromLocation`, the view-origin line |
| `tests/test_report_workspace.py` | test | HLR-3103, HLR-3104 / AT-3103, AT-3104, TC-3109..TC-3112, TC-3122 | +8 nodes; one 001 node edited (TC-3105's Tab list, see Reverse census) |
| `tests/report_fixture.py` | fixture | HLR-3103 / LLR-3103.1 | task st9 note "@carmen.vega checks the quote", so the `$&`/`$'` task falls in AT-3103's one-person view |
| `.dev-flow/2026-10-29-batch-01/01-requirements.md`, `01-requirements-ledger.md` | doc | LLR-3103.1 | the amendment `LED-2026-10-29-batch-01.24` |
| `.dev-flow/2026-10-29-batch-01/PLAN.md` | doc | — | the plan's state, the Test ledger rows, SD2 as an accepted risk |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped; `report_fixture.py` is a support module) |
| Doc files | 4 (outside the count) |

## 3 · How to test

```bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
cd C:/Users/jjgh8/Github/taskboard-wt/report-proto
env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q -p no:cacheprovider   # must print a path inside report-proto
TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_html.py tests/test_report_workspace.py tests/test_report.py
# the mutation battery
env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-002.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none separate — the export JS functions (`reduce`, `csvCell`, `downloadView`, `printView`) are asserted by the white-box nodes below | n/a |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | `test_TC_3109_the_download_keeps_only_used_entries` · `test_TC_3110_notes_off_strips_the_notes` · `test_TC_3111_the_view_file_reopens_on_its_view` · `test_TC_3111_the_export_captions_show_without_hover` · `test_TC_3112_the_print_rules_hold` · `test_TC_3122_csv_and_json_hold_the_visible_rows_only` (6, `tests/test_report_workspace.py`) | 6 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | `test_AT_3103_download_this_view_holds_only_the_filtered_tasks` — presses "Download this view" on the written `file://` page with `expect_download`, searches the saved bytes raw and JSON-escaped for every dropped item's unique token (qzN1/qzK1 included), keeps a `$&`/`$'` task in the view, compares row multisets, re-opens the downloaded file headless (0 console errors, 0 external requests, same view) · `test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` — `emulate_media(media="print")`, dispatches `beforeprint`, opens the card and the tooltip first, reads computed styles | 2 passed |
| regression | `core` | `tests/test_report.py` (18) and the 44 nodes of increment 001 (`tests/test_report_html.py` 12, `tests/test_report_workspace.py` 14 incl. the edited TC-3105) | green in the run below |
| increment total | — | `TASKBOARD_REQUIRE_BROWSER=1` over the three files, 0 skipped | **52 passed** in 12.93 s (`suite-002.txt`) |

The AT-3101 and AT-3105..AT-3107 nodes are not written yet (increments 003–004): the `V2` rows for them in the gate are station-expected, as the plan declares. The package-scanning law suites were not re-run in this increment; they re-run in increment 004 and at P4.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | 40 single-fault mutants M01–M40, each a one-line change to `report_workspace.py` aimed at one of this increment's OWN new assertions (the list under *Mutation verdicts*) |
| Instrument | project code, mutated by the script `evidence/mutation-002.py` (anchor-checked string replacement, `finally`-restore, per-node verdicts) |
| Where it ran | this worktree, the increment tree; the harness restores the file before the next mutant |
| Transcript | `evidence/mutation-002.txt` (holds several runs as the battery grew from M29 to M40; the last, M01–M40 on the final bytes, is the verdict of record; one earlier start aborted on a harness `SyntaxError` and was logged) |
| Restore proven by | sha256 recorded before and after every mutant (`restored, identical`); final `report_workspace.py` `99a97735c581126ce1cc481fc2adc1c4e81129f0672cf5baa58df27f58870f83`, the tree's bytes at commit `613702e` |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every run |
| Arms resolved at baseline | 40 mutants, each with its `-k` selection resolved to the named node(s) |
| Verdict granularity | per resolved node id (the transcript prints `RED nodes: [...]` for each mutant) |
| Arms that stayed GREEN | none. M38 is KILLED by the node's ~11 s timeout, not by an assertion (clearing the hash of a downloaded view hangs the wait for the restored view) |

| Field | Value |
|---|---|
| **RED counterfactual** | the AT's own mutations: `report_workspace.py:748` the file composed by `String.replace` (M05, D3) and `:749` the JSON entering the file with raw `<>&` (M06) turn `test_AT_3103_download_this_view_holds_only_the_filtered_tasks` RED, and `:126` the control bar dropped from the print rule (M12) turns the print node RED · transcript `evidence/mutation-002.txt` · restore digests as in the table above |

| Field | Value |
|---|---|
| **Mutation verdicts** | 40/40 KILLED, none survived, none BAD in the final run, per resolved node (line numbers are those the transcript's last run lists): M01 `:749` the download re-embeds the full data · M02 `:716` deps/chain keys of dropped tasks kept · M03 `:733` R3, `meta.scope.boards` not reduced · M04 `:738` the full people list kept (LLR-3103.1 negative control) · M05 `:748` D3, `String.replace` composition · M06 `:749` raw `<>&` in the embedded JSON · M07 `:717` notes kept with the section off · M08 `:717` `notes_html` stripped but `notes_text` kept (PA2/C2) · M09 `:149,849` the shell captured after rendering · M10 `:811` D5, the downloaded file ignores `meta.view` · M11 `:886` C6, the print caption not visible without interaction · M12 `:126` the control bar dropped from the print rule · M13 `:823` the `beforeprint` handler does not stamp the date · M14 `:141` C14, `#gantt{min-width:0!important}` dropped · M15 `:124` C7, `@page{margin:0}` dropped · M16 `:487` the SVG `viewBox` dropped · M17 `:128` C7, the print shows "of N" · M18 `:784` the CSV exports the full data · M19 `:758` the `'` guard dropped · M20–M25 `:758` one prefix class unguarded each (`=`, `+`, `-`, `@`, TAB, CR) · M26 `:758` C13, plain numbers prefixed too · M27 `:778` CSV/JSON name a dropped dependency's title · M28 `:780` CSV/JSON carry notes with the section off · M29 `:399` the downloaded file's header does not say it is a filtered view · M30 `:736` project facts carried unchanged · M31–M36 CR2-1, one per remaining count and the null facts (`:702` open carried, `:703` late carried, `:703` late counted as open, `:704` done carried, `:705` high carried, `:705` worst and momentum kept) · M37 `:710` SD1, mentions travel with notes off → `test_TC_3110_notes_off_strips_the_notes` · M38 `:822` CR2-2, clearing the hash of a downloaded view → `test_TC_3111_the_view_file_reopens_on_its_view` · M39 `:824` CR2-3, the printed line stays after printing · M40 `:693` CR2-3, a second stamp path in the print control → both `test_TC_3112_the_print_rules_hold` · arms that stayed GREEN: none · transcript `evidence/mutation-002.txt` (the per-mutant node ids sit under each `M..` header) |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the byte search of the downloaded file (raw and JSON-escaped, every dropped item's token) | M01 (no reduction) and M04 (the full people list) | the AT-3103 and TC-3109 nodes RED — the search found the dropped names in the saved bytes (`mutation-002.txt`, M01, M04) |
| the `$&`/`$'` task in the kept view | M05: the file composed by `String.replace` | the AT-3103 node RED — the pattern re-inserted the shell (`mutation-002.txt`, M05) |
| the print-media computed-style reads (`emulate_media`) | M12 (control bar not hidden), M15 (`@page` margin), M14 (gantt width at 794 px) | the AT-3104 / TC-3112 nodes RED (`mutation-002.txt`, M12, M14, M15) |
| the CSV cell reader, one arm per prefix class | M19–M26, each a single class unguarded or the number exemption removed | `test_TC_3122_csv_and_json_hold_the_visible_rows_only` RED for each (`mutation-002.txt`) |
| the mutation harness | the earlier start with a `SyntaxError` in the harness itself | the run aborted loudly and was re-run; the transcript keeps the aborted start (`mutation-002.txt`) |
| the 8 new nodes | the 40 mutants above (mechanism faults, not verdict edits) | per-node RED as listed under *Mutation verdicts* |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 6 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the downloaded view file (`workspace-view-<date>.html`) — the saved bytes | `test_AT_3103_download_this_view_holds_only_the_filtered_tasks`: through `expect_download`, searches the file's bytes raw AND JSON-escaped for every dropped item's unique token (qzN1/qzK1 included) and asserts the kept row multiset | passed (`suite-002.txt`); M01, M04, M05, M06 turn it RED |
| the same file — the data element | `test_TC_3109_the_download_keeps_only_used_entries` and `test_TC_3110_notes_off_strips_the_notes`: parse `#board-data` of the saved file; every project/board/person/class is used by a kept task, 0 dangling dependency keys, notes off → 0 non-empty `notes_html`/`notes_text`, no mentions without a person filter | passed; M02, M03, M04, M07, M08, M37 turn them RED |
| the same file — re-opened | `test_TC_3111_the_view_file_reopens_on_its_view`: opens the saved file headless, 0 console errors, 0 external requests, the same visible set, the header says it is a filtered view | passed; M10, M29, M38 turn it RED |
| the print media | `test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` and `test_TC_3112_the_print_rules_hold`: under `emulate_media(media="print")` after `beforeprint`, computed styles of every control, the card and the tooltip are hidden, the view header shows the filters and both dates, `@page` margin 0, gantt `scrollWidth <= 794` at a 794 px viewport, counts over kept tasks | passed; M12–M17, M39, M40 turn them RED |
| the CSV and JSON files | `test_TC_3122_csv_and_json_hold_the_visible_rows_only`: the saved CSV/JSON hold the visible rows only, guard prefixes per class, plain numbers unprefixed | passed; M18–M28 turn it RED |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifact classes (the downloaded view file, the print media, the CSV/JSON files) asserted in 5 forms against the bytes or computed styles the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-29-batch-01/evidence/suite-002.txt | f3515dc66f2d627fcc482a8611ce05451c234265739ffe92e54d232f94945814 |
| mutation-002.txt | .dev-flow/2026-10-29-batch-01/evidence/mutation-002.txt | 86f8c6f3b0d5713bc0a0c2be82750538e474abd9dd2581311da2a4a3fcef4664 |
| mutation-002.py | .dev-flow/2026-10-29-batch-01/evidence/mutation-002.py | cdd4739b8c6118a4372d5fb0bd7793c4b60cf0e9edfa2ed730dcd3d10f7da0bb |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — "no hidden item's text reaches the downloaded bytes" and "no other module is touched" |
| If the result is an ABSENCE, what made the search wide enough | AT-3103 searches the saved bytes for every dropped item's unique token in two encodings (raw and JSON-escaped); the module probe is `git diff --stat 31eddb2 613702e -- taskboard/keymap.py taskboard/app.py taskboard/modals.py taskboard/report.py` over the whole of the four files |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_AT_3103_...` protects the conclusion "the file leaves the hidden data out", not one function's behaviour; M01, M04, M05, M06 each break one conjunct |
| Conjunctive criteria: one mutation per conjunct | AT-3103: no reduction (M01), full people (M04), `String.replace` (M05), raw `<>&` (M06); TC-3110: notes kept (M07), `notes_text` kept (M08), mentions kept (M37); TC-3112: control bar (M12), `@page` (M15), gantt width (M14), "of N" (M17) |
| Synthetic instance of the absent case | `tests/report_fixture.py` holds hidden tasks with the qzN1/qzK1 tokens, a hidden person, a hidden board, a dropped dependency and the `$&`/`$'` task |
| **Positive control for every probe that returned an ABSENCE** | M01 (no reduction) makes the byte search find the tokens in the saved file, so the search fires on the present case; the `git diff --stat` probe over the four files returned no line while the same command over `taskboard/report_workspace.py` returns 167 changed lines |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl KEYMAP tests/` · `grep -rl INVENTORY tests/` · `grep -rl open_url tests/` · `grep -rl build_report tests/` | the same hits as increment 001 (KEYMAP: 15 files; INVENTORY: test_modal_keys; open_url: test_app, test_keymap; build_report: test_report). Re-validated as untouched: this increment edits no `keymap.py`, `app.py`, `modals.py` and no `report.py` — `git diff --stat 31eddb2 613702e -- taskboard/keymap.py taskboard/app.py taskboard/modals.py taskboard/report.py` is empty — so no KEYMAP/INVENTORY/`open_url` assertion can move. `git diff 31eddb2 613702e --stat -- taskboard tests` lists three files only: `taskboard/report_workspace.py`, `tests/report_fixture.py`, `tests/test_report_workspace.py`. `tests/test_report.py` (18) is green in the 52-pass run |
| B2 file moved on disk | n/a — no file moved (probe not fired, declared) | — |
| B3 byte-identical golden captures this source | `tests/goldens/` does not exist (P0 probe) | not fired |
| B4 artifact produced here is consumed elsewhere | `grep -rln "report_html\|report_workspace" taskboard/ tests/` | unchanged from increment 001: the two sources and the two test files; the downloaded file is consumed by the same page code (it is the shell plus reduced data) and is re-opened by AT-3103 and TC-3111 |
| A3 interface consumed by another module changed | the 001 tests of `report_workspace` | one 001 test was edited, by supersession: `test_TC_3105_the_bar_is_native_and_counted` asserted the Tab-order list `len(want) == 43`; the two new controls (print, dl-view) make it 45. The edit is this increment's own change to the control bar's tab stops, not a regression; the node stays green and still fails if a control loses its native element. No other 001 node was edited. (Within this increment's own TC-3111 node the expected chip count was set to 13, not 15, when SD1 stopped mentions travelling with notes off.) |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run (B1 with its hits re-validated, B3, B4, A3; B2 declared not fired); `git diff --stat` over `keymap.py`, `app.py`, `modals.py`, `report.py` is empty |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| CR2-1: the download's re-derived project facts (a second client-side engine) | every place the download computes a project's open/late/done/high/worst/momentum | `grep -n "keptFacts\|keptCounts\|momentum\|worst" taskboard/report_workspace.py` | 1 production site (`keptFacts`, `:695-712` before the fix) | 1 — momentum and worst null; four plain counts over kept statuses (`keptCounts`); branches and pins removed; M30–M36 pin each count | 0 |
| CR2-2: `hashchange` did not restore `meta.view.state` | every reader of the location hash at start or on change | `grep -n "parseHash\|hashchange\|viewFromLocation" taskboard/report_workspace.py` | 2 (start, `hashchange`) | both call the one `viewFromLocation()`; M38 pins it | 0 |
| CR2-3: a double stamp of the printed date and a line that stays visible on screen | every definition and call of the stamp | `grep -n "setPrinted\|printView\|afterprint\|beforeprint" taskboard/report_workspace.py` | 1 stamp function, 2 callers (`printView`, `beforeprint`) | the stamp dropped from `printView` (it only calls `window.print`); `afterprint` hides the line; M39, M40 pin it | 0 |
| SD1: mentions of withheld notes travel with notes off | every place the download or the exports emit a mention or a person | `grep -n "mentions\|people" taskboard/report_workspace.py` over `reduce` and `exportRows` | 3 seats (`reduce`'s tasks, `reduce`'s people, `exportRows`' mentions column) | all 3 follow the one rule (no person filter → none; with one → the pressed people's); TC-3110's arm and M37 pin it | 0 |

| Field | Value |
|---|---|
| **Correction population** | 4 corrections (CR2-1, CR2-2, CR2-3, SD1), each enumerated with its method and its count; none left unedited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| LLR-3103.1 saying nothing of mentions and project facts | `grep -n "LED-2026-10-29-batch-01.24" .dev-flow/2026-10-29-batch-01/01-requirements.md` → the `Ledger:` field of LLR-3103.1 | yes — the live contract states both rules; the ledger keeps the before text | `01-requirements.md:372`, `:373`, `:376`; `01-requirements-ledger.md` LED .24 |
| `len(want) == 43` in the 001 node TC-3105 | `grep -n "len(want) ==" tests/test_report_workspace.py` → `== 45` | yes — one site, edited | `tests/test_report_workspace.py` (TC-3105) |

### Signed-balance test ledger

`post = base − deleted + added` → `52 = 44 − 0 + 8`  ✓ reconciles: the base is increment 001's 44 (`suite-001.txt`: 12 + 14 + 18); this increment adds 8 nodes to `tests/test_report_workspace.py` (AT-3103, AT-3104, TC-3109, TC-3110, TC-3111 ×2, TC-3112, TC-3122); no node deleted; one existing node (TC-3105) was edited, not counted as added.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | code-reviewer — spawned as a generic agent with agents/code-reviewer.md · PASS (0 HIGH; CR2-1 MEDIUM and CR2-2/CR2-3 LOW applied and re-read on 613702e) · no HIGH finding |

The first reading was "OK to advance with notes" (34/34 re-run on workspace + html; mutation 29/29 + M30): CR2-1 (MEDIUM, `keptFacts`: open/late/done/high/worst/momentum unread by the UI and a second JS engine of `views.sitting`/`lane_facts`) was resolved by nulling momentum and worst and keeping four plain counts; CR2-2 (LOW, `hashchange` did not restore `meta.view.state`) and CR2-3 (LOW, a double stamp and a Printed line that stays on screen) were fixed; the re-read on `613702e` found no new finding. Deviations the reviewer accepted: the fixture st9 note, TC-3105 43→45, the `viewBox`, the `due_in` CSV column, the direct `csvCell` arms, the no-filter summary text, the kept-only summary, and the table sort buttons excluded from "every control".

Security: security-reviewer at the gate — PASS (22 passed in its run; mutation-002 no survivors; `.scratch/p3/sec-002.md`). No dropped board fact reaches the downloaded bytes on any traced path (`reduce` is an allowlist build; deps/chain cut to kept keys; project status and due word from the project's own state; people/classes/boards and `meta.scope.boards` reduced; DOMParser + `textContent` so `$&` is inert, M05; `scriptSafe`, M06; CSV/JSON on reduced data, M18 M27 M28; guard classes M19–M26; `@page` margin 0, M15; no `attr(href)` in print). SD1 (minor: with notes off, mentions still named who is in the withheld notes) was fixed in this increment and recorded as `LED-2026-10-29-batch-01.24`. SD2 (minor: the owner's search text travels verbatim in `meta.view` and is printed in the file's header) is an accepted risk, declared in PLAN Risks. SI1 (the `safeHref` test and mutant) remains carried to increment 003.

---

## 5 · Risks

- **Accepted risk SD2:** the owner's search text is in the downloaded file's `meta.view` and printed in its header ("Search: ..."); it is the owner's own input and visible before the file is sent.
- **Browser tests do not run in CI:** Playwright is not a declared dependency; this machine's transcripts (`suite-002.txt`, `mutation-002.txt`) are the evidence of record.
- **`safeHref` is still not exercised (SI1):** carried to increment 003.
- **The download is the batch's data-exposure control (C4):** a later change to `reduce` that adds a directory without reducing it would leak a hidden name; AT-3103 and TC-3109 search the bytes in raw and escaped forms and M01–M04 pin the known seats.
- **M38 is killed by a timeout, not an assertion:** the node waits for the restored view and fails after about 11 s; the failure is real but slow.
- **The mutation harness anchors on source text:** a later edit to those lines makes a mutant `SETUP-ERROR`; the harness reports it rather than passing.
- **Print output is verified by computed styles and a 794 px viewport, not by a rendered PDF.**

## 6 · Pending items / spec deviations

- **Deviation, fixture st9 note:** a note "@carmen.vega checks the quote" so the `$&` task falls in AT-3103's one-person view.
- **Deviation, TC-3105 43→45:** the Tab list gains print and dl-view (the edited 001 node, named in the Reverse census).
- **Deviation, `viewBox` added to the gantt SVG:** without it the printed gantt clipped instead of scaling (M16).
- **Deviation, `due_in` CSV column** added to the export rows.
- **Deviation, the `-3d`, TAB and CR guard arms** call `csvCell` directly: no natural cell in the fixture carries them.
- **Deviation, summary text:** with no filter the summary reads "No filters: all tasks (open · late · done) of every project"; the downloaded file's summary names kept items only.
- **Deviation, table sort buttons** are excluded from "every control" hidden in print (they sit in the table header, not in the control bar).
- **Deviation, TC-3111's expected chip count 13, not 15:** a side effect of SD1 (mentions no longer travel with notes off).
- **Increment-002-owned conditions, all discharged:** C6 (captions visible without hover), C7 (`@page` margin 0, kept-task counts), C13/PQ1 (CSV guard, one mutant per class), C14/PQ3 (gantt at 794 px, M14), PQ4 arms (`$&`/`$'`, qzN1/qzK1), PA2 (notes_text stripped, M08), CR6 (the formula guard), D2, D3, D5, D7, D13, D14, R2, R3.
- **Carried:** SI1 to 003; CR5 in `BACKLOG.md`.
- **Requirement amendments recorded:** SD1 and CR2-1 → LLR-3103.1, `LED-2026-10-29-batch-01.24`.

## 7 · Suggested next task

Increment 003: `taskboard/report_deck.py` (and `taskboard/report_html.py` only if the frozen dict lacks a fact), AT-3106, the deck renderer behind the `deck` kind of `write_reports`; carry SI1 (a `safeHref` test with the edited-data-element arm and an identity mutant).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 1 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 8 new nodes in `tests/test_report_workspace.py` |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | §4: no unit is separate from its TC node |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4: M05/M06 for AT-3103, M12 for AT-3104 · `evidence/mutation-002.txt` · restore digests |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4: 5 probes; `git diff --stat` over `keymap.py app.py modals.py report.py` empty; TC-3105 supersession named |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b: PASS, 0 HIGH, re-read on 613702e |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | `report.py`, `views.py`, `people.py`, `models.py`, `report_html.py` unchanged by this increment |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `suite-002.txt` (52 passed), `mutation-002.txt` (40 KILLED); digests in the evidence rows |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 table with positive controls |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | §4: 40 mutants, per-node verdicts, none green |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4: 6 instruments |
| 13 | **Correction population** declared | all | ✓ | §4: 4 corrections with methods |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4: the downloaded file, the print media, the CSV/JSON in 5 forms |
| 15 | **Independent review** names somebody | all | ✓ | §4b: code-reviewer and security-reviewer |
| 16 | **Evidence files** declared | all | ✓ | §4: rows written by `devflow-evidence.py` |

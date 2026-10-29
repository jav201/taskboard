# Increment 001 — HLR-3101 · HLR-3102 · HLR-3106 · `the one extraction and the interactive workspace with its controls`

> **Owed in.** `core` ✓ · `full` ✓
> **Reserved field names** (language-independent, parsed literally): `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`

| Field | Value |
|---|---|
| Batch | `2026-10-29-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `US-3101` / `HLR-3101` · `HLR-3102` · `HLR-3106` / `LLR-3101.1, LLR-3101.2, LLR-3101.3` · `LLR-3102.1, LLR-3102.2, LLR-3102.3` · `LLR-3106.1, LLR-3106.2` (LLR-3101.* and LLR-3102.* as LED .22 and LED .23 amended them) |
| Acceptance | `AT-3102` · white-box `TC-3101..TC-3108`, `TC-3115`, `TC-3116` (workspace arm), `TC-3123..TC-3125` · unit: none separate — the `extract` / `embed_json` / `notes_html` / `slug` / `write_reports` units are the TC nodes in `tests/test_report_html.py` |
| Agent | `software-dev` (spawned implementer; the orchestrator ran the law suites, the code-review and the security gate; this packet was written by a scribe from the records) |
| Date | `2026-10-29` |

---

## 1 · What changed

The batch now has its data layer and its interactive page. `taskboard/report_html.py` holds the ONE extraction of every loaded board (`extract`) that both reports will read; `taskboard/report_workspace.py` renders variant B from that dict as a single self-contained HTML file with the HR-3 control bar. Nothing in the app reaches them yet (the `H` key, the modal and the toast are increment 004), so this increment's user-reachable surface is the file `write_reports(...)` writes and a browser opens: filters by project, status, person, class, dates and search, section toggles, zoom, one Reset, an active-filter count, and the whole view in the URL hash.

Mechanism. `extract(boards, people, marks, today, project=None)` returns a JSON-able dict with one status rule (archived > done > late = not done and due before today > open) and one `due_word` per task, computed server-side so the page never re-derives them (D19); task URLs pass `views.valid_url` (http/https only, D1); project and task keys are unique across boards (`<board index>:<project id>`) and dependencies and chains carry keys, not titles (D6); `project=` is the project KEY (PA4). `embed_json` writes `<`, `>`, `&` as `\u003c`, `\u003e`, `\u0026` so no board string can close the data element; `notes_html` builds the notes from escaped `highlight_segments` pieces. `slug` and `report_name` name the files and are pinned against `report.report_path` (D20); `write_reports` validates its kinds first, then imports each renderer by a plain function-local `from . import` (PA3). The page is built client-side from `#board-data` (the shell holds no board text, D2), puts board strings in the DOM only through `textContent`, parses the hash against whitelists built from the data (unknown values dropped), and keeps the round's full-gantt print fix (`6c1225f`). The count reads `0 filters active`, `1 filter active`, `N filters active`: the singular is CR1's outcome, ratified by `LED-2026-10-29-batch-01.23`.

Code-review fixes landed in this increment: CR2 (project `done` counted archived tasks), CR3 (a partly written set when a kind fails), CR4 (a bare `StopIteration` on an unknown project key), CR7 (an unused `renderHeader` parameter).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/report_html.py` | source | HLR-3101, HLR-3106 / LLR-3101.1, LLR-3101.2, LLR-3101.3, LLR-3106.1 | new — `extract`, `embed_json`, `notes_html`, `slug`, `report_name`, `write_reports` |
| `taskboard/report_workspace.py` | source | HLR-3102, HLR-3106 / LLR-3102.1, LLR-3102.2, LLR-3102.3, LLR-3106.1, LLR-3106.2 | new — `build_workspace(data)`: variant B ported, the HR-3 control bar, the URL hash, light/dark, 390 px, the print fix |
| `tests/report_fixture.py` | fixture | HLR-3101, HLR-3106 | new — synthetic in-memory boards, never saved: hostile title/note/person name, a cross-project dependency, an archived task, an unlisted board (PA5), a due-today task, the qzN1/qzK1 tokens and the `$&`/`$'` task (PQ4) |
| `tests/report_browser.py` | test | LLR-3102.1, LLR-3102.2, LLR-3102.3, LLR-3106.2 | new — the headless-chromium helper: `require_browser` guard (D15), `new_context`, `open_page` with the request collector (PQ5), control readers |
| `tests/test_report_html.py` | test | HLR-3101, HLR-3106 / TC-3101..3104, 3115, 3123..3125 | new — 12 nodes incl. the PQ6 spike |
| `tests/test_report_workspace.py` | test | HLR-3102 / AT-3102, TC-3105..3108, 3116, 3125 | new — 14 nodes (9 functions, `test_TC_3106_filters_follow_the_truth_table` over 6 arms) |
| `.dev-flow/2026-10-29-batch-01/01-requirements.md`, `01-requirements-ledger.md` | doc | LLR-3102.1 | the CR1 amendment: `LED-2026-10-29-batch-01.23` |
| `.dev-flow/BACKLOG.md`, `.dev-flow/2026-10-29-batch-01/PLAN.md` | doc | — | CR5 as an open item; the plan's state |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 4 (uncapped; `report_fixture.py` and `report_browser.py` are support modules) |
| Doc files | 4 (outside the count) |

## 3 · How to test

```bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
cd C:/Users/jjgh8/Github/taskboard-wt/report-proto
env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q -p no:cacheprovider   # must print a path inside report-proto
TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_html.py tests/test_report_workspace.py tests/test_report.py
# the package-scanning law suites (run by the orchestrator, 298 passed)
env -u NO_COLOR python -m pytest -q tests/test_english.py tests/test_hygiene.py tests/test_markup_census.py tests/test_markup_sites.py tests/test_privacy_sweep.py tests/test_control_bytes.py
# the mutation battery
env -u NO_COLOR python .dev-flow/2026-10-29-batch-01/evidence/mutation-001.py
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | none separate — each unit (`extract`, `embed_json`, `notes_html`, `slug`, `write_reports`) is asserted by the white-box nodes below | n/a |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | `test_TC_3101_extract_is_json_and_holds_every_fact` · `test_TC_3101_extract_never_writes_a_board` · `test_TC_3102_due_words_are_the_cli_reports` · `test_TC_3103_project_scope_keeps_one_project` · `test_TC_3103_an_unknown_project_key_is_refused` · `test_TC_3104_renderers_read_the_dict_only` · `test_TC_3115_embed_json_and_notes_are_inert` · `test_TC_3123_the_slug_is_the_cli_reports` · `test_TC_3123_write_reports_lands_in_the_folder_and_overwrites` · `test_TC_3124_extract_keeps_only_http_urls` · `test_TC_3125_one_status_rule` · `test_PQ6_spike_an_async_test_checks_the_page_in_a_worker_thread` (12, `tests/test_report_html.py`) · `test_TC_3105_the_bar_is_native_and_counted` · `test_TC_3106_filters_follow_the_truth_table[6 arms]` · `test_TC_3106_the_edges_of_the_table` · `test_TC_3107_a_hostile_hash_is_dropped` · `test_TC_3108_reset_restores_the_defaults` · `test_TC_3116_offline_themes_and_phone_width` · `test_TC_3125_the_page_follows_the_status_field` · `test_the_page_shell_holds_no_board_text` (13 of the 14, `tests/test_report_workspace.py`) | 25 passed; the browser module alone: 14 passed in 5.24 s (module wall 6.19 s, PQ7) |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | `test_AT_3102_filters_and_the_hash_round_trip` — presses the controls on the written `file://` page, reads the visible rows and bars; filters by project, status, person, class and date; copies `location.hash`, opens a fresh page with it, asserts the same visible set and control states; Reset clears | 1 passed (the 14th browser node) |
| regression | `core` | `tests/test_report.py` (the CLI report's pin; untouched) | 18 passed |
| increment total | — | `TASKBOARD_REQUIRE_BROWSER=1` over the three files | **44 passed** (`suite-001.txt`) |
| package-scanning law suites | `core` | `test_english`, `test_hygiene`, `test_markup_census`, `test_markup_sites`, `test_privacy_sweep`, `test_control_bytes` | **298 passed** in 107.77 s (`laws-001.txt`), run by the orchestrator |

The AT-3101 and AT-3103..AT-3107 nodes are not written yet (increments 002–004): the `V2` rows for them in the gate are station-expected, as the plan declares.

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | 35 single-fault mutants M01–M35, each a one-line change to `report_html.py` or `report_workspace.py` aimed at one of this increment's OWN new assertions (the list under *Mutation verdicts*) |
| Instrument | project code, mutated by the script `evidence/mutation-001.py` (anchor-checked string replacement, `finally`-restore, per-node verdicts) |
| Where it ran | this worktree, the increment tree; the harness restores each file before the next mutant |
| Transcript | `evidence/mutation-001.txt` |
| Restore proven by | sha256 recorded before and after every mutant (`restored, identical`); final `report_html.py` `53942a406a5c5207ee4841a56ee9628a45932966a26e9a72e39a116097167fc4`, `report_workspace.py` `3f69ea1cc0e9de5923f5e11a7ebd98ced878a61bf694c914cfa2a2a47906b658` — equal to the tree's bytes at commit `31eddb2` |
| Bytecode cache | `PYTHONDONTWRITEBYTECODE=1` on every run |
| Arms resolved at baseline | 35 mutants, each with its `-k` selection resolved to the named node(s); the six parametrized arms `[projects]`, `[people]`, `[classes]`, `[status]`, `[dates]`, `[search]` selected by id |
| Verdict granularity | per resolved node id (the transcript prints `RED nodes: [...]` for each mutant) |
| Arms that stayed GREEN | none of the targeted nodes. The transcript holds two runs: in the first, M35 returned `SETUP-ERROR` (its anchor text was absent after the CR3 fix had changed the line); the anchor was corrected and M35 re-ran KILLED in the second run, the verdict of record |

| Field | Value |
|---|---|
| **RED counterfactual** | the AT's own mutations: `report_workspace.py:245` status chips map `late` to `open` (M27) and `report_workspace.py:705` `writeHash` skipped (M26) both turn `test_AT_3102_filters_and_the_hash_round_trip` RED; the extraction's own: `report_html.py:127` project `done` counting archived tasks (M34) turns `test_TC_3101_extract_is_json_and_holds_every_fact` RED · transcript `evidence/mutation-001.txt` · restore digests as in the table above, returned to the pre-mutation bytes after every mutant |

| Field | Value |
|---|---|
| **Mutation verdicts** | 35/35 KILLED, none survived, none BAD in the final run, per resolved node: M01 `report_html.py:106` projects keyed by the bare id → `test_TC_3101_extract_is_json_and_holds_every_fact` · M02 `:114` extract saves the board → `test_TC_3101_extract_never_writes_a_board` · M03 `:148` due word formatted locally → `test_TC_3102_due_words_are_the_cli_reports` · M04 `:110` scope ignores `project` → `test_TC_3103_project_scope_keeps_one_project` · M05 `:219` module-level renderer import (PA3) · M06 `report_workspace.py:12` renderer imports `views.HEX` · M07 `:12` dynamic import in the renderer (PQ10) → all three `test_TC_3104_renderers_read_the_dict_only` · M08 `report_html.py:67` the `</`-only replace → `test_TC_3115_embed_json_and_notes_are_inert` · M09 `:54` a notes piece left unescaped → the same node · M10 `:177` slug lower-cases only → `test_TC_3123_the_slug_is_the_cli_reports` · M11 `:186` project file name drops the board slug → `test_TC_3123_write_reports_lands_in_the_folder_and_overwrites` · M12 `:151` `valid_url` filter dropped → `test_TC_3124_extract_keeps_only_http_urls` · M13 `:76` late derived with `<=` → `test_TC_3125_one_status_rule` · M14 `report_workspace.py:275` chip as `<span onclick>` · M15 `:50` pressed chip loses its check mark (C12) → `test_TC_3105_the_bar_is_native_and_counted` · M16 `:245` status chips map late to open · M17 `:246` people ANY→ALL · M18 `:244` project filter ignored · M19 `:247` class filter ignored · M20 `:252` span starting ON `to` dropped · M21 `:257` search without case folding → one arm each of `test_TC_3106_filters_follow_the_truth_table[status, people, projects, classes, dates, search]` (PQ11) · M22 `:249` `from` after `to` no longer empties → `test_TC_3106_the_edges_of_the_table` · M23 `:383` the hash echoed into the summary via `innerHTML` · M24 `:200` whitelist bypassed (PQ2 a, b) → `test_TC_3107_a_hostile_hash_is_dropped` · M25 `:340` Reset leaves rows and hash → `test_TC_3108_reset_restores_the_defaults` · M26 `:705` `writeHash` skipped · M27 `:245` late→open → `test_AT_3102_filters_and_the_hash_round_trip` · M28 `:747` a Google Fonts `<link>` (PQ5) · M29 `:26` fixed 600 px layout · M30 `:18` light palette never applies → `test_TC_3116_offline_themes_and_phone_width` · M31 `:245` the page re-derives status from dates (PQ8) → `test_TC_3125_the_page_follows_the_status_field` · M32 `:832` a board name written into the shell → `test_the_page_shell_holds_no_board_text` · M33 `:741` the page script does not run → `test_PQ6_spike_an_async_test_checks_the_page_in_a_worker_thread` · M34 `report_html.py:127` CR2 → `test_TC_3101_extract_is_json_and_holds_every_fact` · M35 `:205` CR3 the folder created before the kinds are checked → `test_TC_3123_write_reports_lands_in_the_folder_and_overwrites` · arms that stayed GREEN: none among the named nodes · transcript `evidence/mutation-001.txt` · restore digests as above. The code-reviewer's mapping note (CR8): M05–M07 all sit on TC-3104, M16 and M27 cover one defect through two nodes, M33 is killed by the spike. |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| the request collector (PQ5: counts http(s), ws(s) and any `file:` URL other than the page's own, ignoring `about:`/`blob:`/`data:`) | M28: a Google Fonts `<link>` planted in the page's mechanism | `test_TC_3116_offline_themes_and_phone_width` RED — the collector counted the external request (`mutation-001.txt`, M28) |
| the hash whitelist assertions (PQ2) | M23 (hash echoed via `innerHTML`) and M24 (whitelist bypassed), each a single fault in the mechanism | `test_TC_3107_a_hostile_hash_is_dropped` RED for both (`mutation-001.txt`, M23, M24) |
| the browser harness itself (PQ6) | M33: a syntax error in the page script | the spike node RED — the worker-thread browser launch sees a page that does not run, not a green one (`mutation-001.txt`, M33) |
| the mutation harness | M35's first anchor, text no longer in the file after the CR3 fix | `SETUP-ERROR: ... occurs 0 times in report_html.py` — the harness refuses a mutant whose anchor did not apply instead of calling it killed or survived; the anchor was corrected and the re-run is the verdict of record (`mutation-001.txt`, first run) |
| the 25 increment nodes | the 35 mutants above (mechanism faults, not verdict edits) | per-node RED as listed under *Mutation verdicts* |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 5 instruments, each shown RED before its first PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the workspace HTML file `write_reports` writes (`<board dir>/reports/workspace-<date>.html`) — shell bytes | `test_the_page_shell_holds_no_board_text`: reads the page the renderer emitted with the data element removed and asserts no board title, note, person or board name appears outside `#board-data` (D2) | passed (`suite-001.txt`); M32 (a board name written into the shell) turns it RED |
| the same file — the data element | `test_TC_3115_embed_json_and_notes_are_inert`: asserts the bytes of the data element hold no raw `<`, `>`, `&`, and that a hostile title `<script>alert(1)</script>` and a note with `</script>` and `&` appear only escaped | passed; M08 and M09 turn it RED |
| the same file — requests when opened | `test_TC_3116_offline_themes_and_phone_width` opens the written `file://` URL and asserts 0 requests beyond the page's own (PQ5), 0 console and page errors, `scrollWidth <= innerWidth` at 390 x 844, the dark scheme loads | passed; M28, M29, M30 turn it RED |
| the dict that is embedded in the file — URLs | `test_TC_3124_extract_keeps_only_http_urls` asserts the embedded dict keeps `http`/`https` URLs and drops `javascript:` and `data:` | passed; M12 turns it RED |
| the file on disk | `test_TC_3123_write_reports_lands_in_the_folder_and_overwrites`: the file exists in `reports/`, a second write overwrites it, a failing kind writes none | passed; M11 and M35 turn it RED |
| the board files | `test_TC_3101_extract_never_writes_a_board`: every board file's bytes are identical before and after an export | passed; M02 turns it RED |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 1 artifact class (the workspace HTML file) plus the board files it must not alter, asserted in 6 forms against the bytes the producer wrote |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-29-batch-01/evidence/suite-001.txt | e6d0594bc34b9af9fa88e3b21cbed3b9cbf1a790ae1ddb3d713d9a721b6aa40b |
| mutation-001.txt | .dev-flow/2026-10-29-batch-01/evidence/mutation-001.txt | e562590efb672e88add580e25e06924178e134cf695ed52f83aa7add8a53e525 |
| mutation-001.py | .dev-flow/2026-10-29-batch-01/evidence/mutation-001.py | a08711f9ce691acb475d430af64d39e74554531c9681538db9835a61d6e4864b |
| laws-001.txt | .dev-flow/2026-10-29-batch-01/evidence/laws-001.txt | 3ae790c385af0af213ec918f00486fbc213c3f6d4c9a3644d2e7a1f40b2ca585 |

| Field | Value |
|---|---|
| **Evidence files** | `4 artifact(s), each at the declared home, with the digest of its bytes on disk` |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes — "no module outside the new ones imports `report_html` / `report_workspace`" and "the CLI report is unaffected" |
| If the result is an ABSENCE, what made the search wide enough | `grep -rln "report_html\|report_workspace" taskboard/ tests/` over the whole package and the whole test tree, and `git diff 9da7438 -- taskboard/report.py tests/test_report.py` (0 lines) |
| Guard labelled as protecting a CONCLUSION, not a behaviour | `test_TC_3104_renderers_read_the_dict_only` — it protects the conclusion "one extraction feeds both renderers", not a behaviour of one function; M05, M06, M07 each break one conjunct |
| Conjunctive criteria: one mutation per conjunct | TC-3104: module-level import (M05), `views.HEX` import (M06), dynamic import (M07); TC-3107: innerHTML echo (M23), whitelist bypass (M24); TC-3116: external request (M28), fixed width (M29), palette (M30) |
| Synthetic instance of the absent case | `tests/report_fixture.py` holds the cases the real boards lack: hostile strings, an archived task, a cross-project dependency, an unlisted board, a due-today task |
| **Positive control for every probe that returned an ABSENCE** | the same `grep -rln "report_html\|report_workspace"` returns the two source files and `tests/test_report_html.py`, `tests/test_report_workspace.py` (the known-present users) — the probe fires on the present case; the `git diff 9da7438` probe over `taskboard/report.py tests/test_report.py` returned 0 lines while the same command over `taskboard/report_html.py` (new since that ref) returns its full text |

### Reverse census — trigger family B, and A3

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -rl KEYMAP tests/` · `grep -rl INVENTORY tests/` · `grep -rl open_url tests/` · `grep -rl build_report tests/` | KEYMAP: 15 files (test_app, test_archive, test_boards_home, test_dependencies, test_help_keys, test_kanban_priority, test_keymap, test_legend, test_links, test_link_picker, test_marks_manager, test_momentum, test_people_view, test_readme, test_report); INVENTORY: test_modal_keys; open_url: test_app, test_keymap; build_report: test_report. Re-validated as untouched: this increment edits no `keymap.py`, `app.py`, `modals.py` (`git diff --stat 9da7438` over the three is empty), so no KEYMAP/INVENTORY/`open_url` assertion can move; the key-table census suites re-run in increment 004. `tests/test_report.py` (18) is green in the 44-pass run |
| B2 file moved on disk | n/a — no file moved (probe not fired, declared) | — |
| B3 byte-identical golden captures this source | `tests/goldens/` does not exist (P0 probe) | not fired |
| B4 artifact produced here is consumed elsewhere | `grep -rln "report_html\|report_workspace" taskboard/ tests/` | `taskboard/report_html.py`, `taskboard/report_workspace.py`, `tests/test_report_html.py`, `tests/test_report_workspace.py` only — the HTML file is consumed by the same page code (and, from increment 002, by the downloaded copy); the app does not import it until increment 004 |
| A3 interface consumed by another module changed | `git diff 9da7438 -- taskboard/report.py tests/test_report.py`; `grep -n "^from\|^import" taskboard/report_html.py` | the diff is empty (0 lines): `report._e` and `report._due_word` are consumed unchanged, as are `views.HEX/highlight_segments/lane_facts/sitting/valid_url`, `people.split_mentions/mention_ids`, `models.parse_iso/days_in_phase`; no existing interface changed |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run (B1 with its hits re-validated, B3, B4, A3; B2 declared not fired); `git diff 9da7438 -- taskboard/report.py tests/test_report.py` is empty |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| CR2: project `done` counted archived tasks | every place a project's done count is produced | `grep -n "done_n" taskboard/report_html.py` (0 hits after the fix; 1 before, at `:127`) | 1 production site | 1 (`report_html.py:127`, done from `status == "done"`); M34 pins it | 0 |
| CR3: a partly written set when a kind fails | every path of `write_reports` that creates the folder or writes before the kinds are validated | `grep -n "mkdir\|write_text\|unknown report kind" taskboard/report_html.py` | 1 path | 1 (`write_reports`, `:200-207`, kinds validated first); M35 pins it | 0 |
| CR4: a bare `StopIteration` on an unknown project key | every lookup of a project key in `report_html.py` | `grep -n "no project with the key" taskboard/report_html.py` | 2 (`:154` in `extract`, `:195` in `_scope_slugs`) | both raise `ValueError`; `test_TC_3103_an_unknown_project_key_is_refused` | 0 |
| CR7: an unused `renderHeader` parameter | every definition and call of `renderHeader` | `grep -n "renderHeader" taskboard/report_workspace.py` | 1 definition + 1 call (`:378`, `:699`) | the definition takes no parameter | 0 — the `#view-summary` element it fills is increment 002's header seat |
| CR1: "1 filter active" against the pinned "N filters active" | the count's wording in the live contract and in the assertions | `grep -n "filters active" .dev-flow/2026-10-29-batch-01/01-requirements.md; grep -n "filter.* active" tests/test_report_workspace.py` | 2 contract lines (`:332`, `:335`) + the 6 test sites cr-001 lists | the contract lines by `LED-2026-10-29-batch-01.23`; the test sites already asserted the singular | 0 |

| Field | Value |
|---|---|
| **Correction population** | 5 corrections (CR1, CR2, CR3, CR4, CR7), each enumerated with its method and its count; none left unedited |

#### Supersession-completeness inspection (V-3)

| Superseded marker | grep result | All surviving refs negative? | Evidence (file:line) |
|-------------------|-------------|------------------------------|----------------------|
| the one-form label `labelled "N filters active"` | `grep -c 'labelled "N filters active"' .dev-flow/2026-10-29-batch-01/01-requirements.md` → 0 after the amendment; the remaining mentions are the ledger entries' before/after text (LED .22, LED .23) and the sealed PDR record's C10 | yes — the live contract reads the three-form label | `01-requirements.md:332`, `:335`; `01-requirements-ledger.md` LED .23 |

### Signed-balance test ledger

`post = base − deleted + added` → `44 = 18 − 0 + 26`  ✓ reconciles: `tests/test_report.py` held 18 at the base (P1 probe 6, `evidence/p1-probes.txt`) and is untouched; the increment adds 26 nodes (12 in `test_report_html.py`, 14 in `test_report_workspace.py`); no node deleted, none rewritten. The 298 of `laws-001.txt` is a separate run over the package-scanning suites, not part of this ledger.

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | code-reviewer — spawned as a generic agent with agents/code-reviewer.md · OK to advance (with notes) · no HIGH found, so nothing to resolve; 2 MEDIUM (CR1 singular "1 filter active" against the pinned "N filters active" — resolved by an LLR wording amendment; CR2 project `done` counted archived tasks — fixed) and 6 LOW (CR3, CR4, CR7 fixed; CR5 declared risk; CR6 to increment 002; CR8 noted); 25/25 increment tests re-run green (executed), mutation battery read (33/33 killed, mapping to the named nodes holds). Security: security-reviewer at the gate — PASS (`.scratch/p3/sec-001.md`; 25 passed in its run); S1 (task URL schemes) executed-verified: `report_html.py:150` keeps only `valid_url` results, TC-3124 passes, M12 killed; the client re-check `safeHref` (`/^https?:\/\//i`, `target=_blank rel="noopener noreferrer"`) stands as defence in depth; carry SI1 to increment 003 (no test or mutant exercises `safeHref` yet: add TC-3116's edited-data-element arm and a `safeHref`→identity mutant). |

---

## 5 · Risks

- **Inbox key collision (CR5, declared, in `BACKLOG.md`):** the Inbox lane's key `<board index>:inbox` equals the key of a project whose id was hand-edited to `inbox`; in the report only, the two would merge into one row. The board and the app are unaffected.
- **Browser tests do not run in CI:** Playwright is not a declared dependency, so the browser nodes skip there (`TASKBOARD_REQUIRE_BROWSER=1` makes a missing Playwright fail locally, D15). This machine's transcripts are the evidence of record.
- **`safeHref` is not yet exercised (SI1):** the server filter is the proven control; the client re-check has no test or mutant until increment 003.
- **`csvCell` has no formula guard yet (CR6):** the CSV/JSON downloads are the round's, left as they were; the guard (C13) is increment 002's.
- **Two derivations of "late" would diverge** if a later change re-derived it in the page: M31 and M13 pin the single server-side rule today.
- **The mutation harness anchors on source text:** a later edit to those lines makes a mutant `SETUP-ERROR` (it happened once, M35); the harness reports it rather than passing.

## 6 · Pending items / spec deviations

- **Deviation, `views.lane_facts` instead of `lanes_of`:** `lanes_of` ranks and names lanes by project name only, which would merge two projects of one name across boards; the extraction needs per-project lane facts, so it reads `views.lane_facts`. Flagged for the DDR.
- **Deviation, count wording (CR1):** "1 filter active" in the singular; the contract is amended (`LED-2026-10-29-batch-01.23`), not the code.
- **Deviation, `worst` is `None` when a project has 0 open tasks** (there is no task to carry).
- **`write_reports` fails the `deck` kind until increment 003:** the kind is validated first (CR3) and refused; the deck renderer does not exist yet.
- **Per-test timeout is Playwright's 10 s per action:** `pytest-timeout` is not installed, and no dependency was added.
- **PQ6 decided:** an app-level (Textual `run_test`, asyncio) test launches Playwright inside a worker thread through `asyncio.to_thread` (proven by the spike `test_PQ6_spike_an_async_test_checks_the_page_in_a_worker_thread`); no shared browser fixture lives in the export-app module (increment 004). The browser module's wall time is 6.19 s (PQ7).
- **Increment-001-owned PDR conditions, all discharged except Q9 in part** (PA3, PA4, PA5, PA7, PQ2, PQ4, PQ5, PQ6, PQ7, PQ8, PQ10, PQ11, Q9, Q10, Q12, Q13, Q16, C10–C12): PA3 `write_reports` function-local imports + TC-3104 arm (M05); PA4 `extract(project=<key>)` (TC-3103); PA5 the unlisted board in the fixture and AT-3102's hash round trip; PA7 TC-3116's workspace arm at 390 px, both themes, offline; PQ2 two single-fault mutations for TC-3107 (M23, M24); PQ4 the qzN1/qzK1 tokens and the `$&`/`$'` task in the kept view; PQ5 the request collector, proven by the Google Fonts mutation (M28); PQ6 the spike; PQ7 module-scoped browser, a fresh context per test, per-test timeout, module time 6.19 s; PQ8 `test_TC_3125_the_page_follows_the_status_field` over a due-today task (M31); PQ10 TC-3104 also fails on `import_module`/`__import__` (M07); PQ11 one mutation per filter arm (M16–M21); C10–C12 the count unit, the 390 px first-viewport rule and the non-colour chip cue (TC-3105, M15). **Q9 is discharged in part:** the dates arm asserts a literal id subset plus the computed rule, not a fully literal set; carried to increments 002 and 003 as a strengthening. (Q10, Q12, Q13, Q16 are discharged as the implementer reported them; this packet's author did not re-derive each from its text.)
- **Carried:** SI1 to 003; CR6 / C13 to 002; CR5 in `BACKLOG.md`.

## 7 · Suggested next task

Increment 002: `taskboard/report_workspace.py` only, HR-4 — the print view (header, `@page`, captions, kept-task counts) and "Download this view" (the filtered self-contained file, directories reduced, `csvCell` formula guard), AT-3103 and AT-3104, TC-3109..TC-3112 and TC-3122; strengthen Q9's dates arm in passing.

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | §2: 2 / 4 |
| 2 | Tests written in this same increment | all | ✓ | 26 new nodes across `tests/test_report_html.py` (12) and `tests/test_report_workspace.py` (14) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | §4: no unit is separate from its TC node |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4: M26/M27 for AT-3102, M34 for TC-3101 · `evidence/mutation-001.txt` · restore digests |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4: 5 probes; `git diff 9da7438 -- taskboard/report.py tests/test_report.py` empty |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b: OK to advance (with notes), 0 HIGH |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | `report.py`, `views.py`, `people.py`, `models.py` consumed unchanged; `git diff 9da7438 -- taskboard/report.py` empty |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | `suite-001.txt` (44 passed), `laws-001.txt` (298 passed), `mutation-001.txt` (35 KILLED); digests in the evidence rows |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 table with positive controls |
| 11 | **Mutation verdicts** declared — per arm | all | ✓ | §4: 35 mutants, per-node verdicts, none green |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4: 5 instruments |
| 13 | **Correction population** declared | all | ✓ | §4: 5 corrections with methods |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4: the workspace HTML file in 6 forms |
| 15 | **Independent review** names somebody | all | ✓ | §4b: code-reviewer and security-reviewer |
| 16 | **Evidence files** declared | all | ✓ | §4: rows written by `devflow-evidence.py` |

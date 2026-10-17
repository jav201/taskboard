# Validation — taskboard — Batch 2026-10-16-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`); for Spanish batches **translate the prose, never a label** — the reserved field names are declared in §✅ Verdict and are read literally.
> Phase 4 artifact. Content owner: `qa-reviewer`, who **EVALUATES** the results of the validation strategy fixed in Phase 1, **names who executed each one** and returns the rows; the orchestrator writes `04-validation.md` (`stations/shared-homes-roles.md` §Delegation). The ONE complete gate-suite run is the orchestrator's (`C-25`); a sub-agent consumes the result and never owns the run.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/validation-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

**`Mode`:** `validation`

## ✅ Verdict (read first)

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Result` · `Gate run` · `Layer 0` · `Evidence checklist` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.
>
> **And so are the three verdict tokens** `PASS` · `PASS-WITH-NOTES` · `FAIL`, which are VALUES and not prose.
> A Spanish batch writes `- **Result:** PASS`, not `- **Resultado:** aprobado`: the label, the tokens and the
> reviewer-identity tokens below are the machine's vocabulary.

- **Result:** PASS-WITH-NOTES
- **Gate run:** `python -m pytest -q -p no:cacheprovider` (the CI command, `.github/workflows/ci.yml:61`, plus no cache) · exit 1 · `8cd8dbde21b4b88ff56472ddf677c8a475b1c941` · executed by the orchestrator (software-dev), 2026-10-17T14:53:40Z, `evidence/suite-p4.txt` — 3 failed, 2631 passed; 2 failures pre-existing at base `64443be` (`evidence/preexisting-base-failures.txt`), 1 environment (`tests/test_app.py::test_win_clipboard_roundtrip`: its setup guard reports the machine-global clipboard refused `Set-Clipboard`; the batch diff touches no clipboard code; re-run twice, same setup failure — `evidence/p4-clipboard-env.txt`) → G-001, G-002
- **Layer 0:** 11 unit(s) met the criterion · 11 carry a named reddening mutation (32 mutants: 31 KILLED, 1 declared equivalent N7)
- **Requirements:** 11/11 pass · 0 blocker fails
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the shipped surface (boundary + negative)
- **Surface-reachability (bidirectional):** ⚠ 1 gaps (the PNG export is observed conditionally — G-004)
- **Supersession inspection (read off the P3 packets):** ✓ all surviving refs negative (increments 001 and 004 reverse census; every live oracle ref is `PRES-R2-*`; `PRES-R`/`PRES-C`/"hybrid" survive in comments and docstrings only — G-005)
- **Test ledger:** ✓ reconciles (`2592 − 0 + 42 = 2634`)
- **Evidence checklist (qa-reviewer):** qa-reviewer · 11 of 11 rows ✓ with evidence

> If every line is ✓, the Detail below is reference only. Any ⚠/✗ → read the matching part.

Who executed what: the gate suite, the P3 mutation batteries and the app captures — the orchestrator (software-dev); the `qa-reviewer` (spawned — generic agent with agents/qa-reviewer.md) evaluated those results, and itself ran a targeted re-run of the batch's TC/AT nodes at `8cd8dbd` (`tests/test_present.py tests/test_present_rulers.py tests/test_present_room.py tests/test_present_hide.py tests/test_help_keys.py -k "AT_ or TC_"` → 47 passed), `--collect-only` (2634) and the clipboard diff check (empty).

---

## Detail (reference)

### Layer 0 — unit

| Unit | Which criterion | Node id | Result |
|---|---|---|---|
| `views.gantt_day_row(shade_weekends=)` | LLR-1601.1 no weekend shading in present; gantt default unchanged | `tests/test_present_rulers.py::test_TC_1601_the_ruler_rows_their_colours_and_no_weekend` | executed · pass |
| `views._present_ruler` (month/tick rows, labels, tones) | LLR-1601.1 | `test_TC_1601_*` (3), `tests/test_present_room.py::test_TC_1608_*` (4) | executed · pass |
| `views.present_span_label` + chip / `_present_cols` | LLR-1601.2 | `test_TC_1602_*` (3), `tests/test_present.py` TC-1001/TC-1002 | executed · pass |
| `Task.from_dict` / `Board._to_dict` omission / `_TASK_KEYS` | LLR-1602.1 | `tests/test_present_hide.py::test_TC_1603_*` (3) | executed · pass |
| `views.present_tasks` / `present_hidden` | LLR-1602.2 | `test_TC_1604_the_filter_and_the_axis_fit_the_shown_tasks` | executed · pass |
| `PresentScreen` hide / show_all / hint count | LLR-1602.2 | `test_TC_1604_space_moves_*`, `test_TC_1604_the_hint_row_*` | executed · pass |
| `TaskModal` `f-present` + result key | LLR-1602.3 | `test_TC_1605_*` (2) + `tests/test_edit_window.py` | executed · pass |
| `HelpModal` column-major grid | LLR-1603.1 | `tests/test_help_keys.py::test_TC_1606_*` (4) | executed · pass |
| `keymap.global_keys` | LLR-1603.2 | `test_TC_1607_global_keys_are_the_live_palette_only_keys` | executed · pass |
| global-line packing / wrap | LLR-1603.2 | `test_TC_1607_the_line_packs_and_wraps_only_between_entries` | executed · pass |
| `#help-foot` dock | LLR-1603.2 | `test_AT_1603_*` (both sizes) | executed · pass |

**Measured by mutation, never by line coverage.**

| Unit | Mutation applied | RED observed? | Transcript |
|---|---|---|---|
| present ruler / chips | M1–M8 | 8/8 KILLED — executed by the orchestrator, increment 001 | `evidence/mutation-001.txt` |
| hide flag / filter / keys / editor | N1–N11 | 10/11 KILLED; N7 (`a` `priority=False`) SURVIVED — declared equivalent, code-reviewer verified; behaviour asserted by TC-1604 arm (i) — executed by the orchestrator, increment 002 | `evidence/mutation-002.txt` |
| help band / global line | P1–P6 | 6/6 KILLED — executed by the orchestrator, increment 003 | `evidence/mutation-003.txt` |
| tick-row label / room frame | Q1–Q7 | 7/7 KILLED — executed by the orchestrator, increment 004 | `evidence/mutation-004.txt` |

### UX walkthrough — only if trigger family D fired

| Criterion (when the user does X, they observe Y) | Driven with the REAL mechanism | Painted result asserted | Verdict |
|---|---|---|---|
| `R` → ruler rows (today + month, the selected task's dates) and a chip on each field row; `→` moves the dates | Textual `run_test` 118×31, keys `R`, `right` | `#present-frame` rows 1–5 | executed · pass (orchestrator suite; qa re-run) |
| `space` → the task leaves the frame, the hint ends `· 1 hidden`; `x` export holds no `hidden`/title; restart keeps it; `a` restores and the file returns to its bytes | `run_test` 118×31, keys `R`, `space`, `x`, restart, `a` | `#present-frame`, `#present-hint`, `board.json` bytes, `reports/present-*.svg` | executed · pass |
| editor: "Show in presentation" fully painted at 80×24, `space` toggles, Save writes the flag | `run_test` 80×24, task editor | `#f-present` region + `board.json` | executed · pass |
| `?` in gantt → `R Present` / `S Standup` with no scroll; `end` → the gantt keys whole, the global line still pinned | `run_test` 118×30 and 80×24, keys `3`, `?`, `end` | compositor rows | executed · pass |
| the frame and export carry no presenter text; the tick label reads `selected task ▸` | renderer + SVG at both sizes (TC-1608) | frame text + SVG | executed · pass |

**Mechanism used:** a UI test driver (Textual `App.run_test` / Pilot, headless), plus artifacts on disk (`board.json`, the exported SVG); app captures `evidence/captures/app-00{1..4}-*` at 118×31 and 80×25 by the orchestrator

| Act | What it is | Performed? |
|---|---|---|
| Automated walkthrough | the criteria above, driven through the REAL mechanism | performed |
| Expert inspection | a cognitive walkthrough against declared criteria, by a reviewer and not a user | not performed — the ux-reviewer inspected the design at P2/PDR (02-review UX-1..8, PDR PC-10/PC-11), not the built screens at P4 |
| Evaluation with users | real users of the system, doing the tasks named in the context of use | not performed — no user evaluation was done in this batch |

- **Method:** headless driver scripts written by the author (software-dev), run in the gate suite by the orchestrator. The operator's design verdicts on the prototype captures (2026-10-16) and on the P3 handoff (2026-10-17) are design input, not a usability evaluation.
- **Participants or population:** none — no user took part.
- **Evidence of the evaluation:** `evidence/suite-p4.txt`, `evidence/captures/`, `evidence/frames/PRES-R2-*.txt`
- **Limits:** shows the keys reach the painted surface and the deliverables are right; does not show a presenter or a room reads the ruler and chips correctly. The tasks were chosen by the author. The operator has not looked at the 80-column oracle frame (G-003); `selected: no dates` was never shown to the operator (G-006).

### Layer A — functional (white-box): per-requirement results

| Req | Method | Executed verification | Numeric threshold | Result | Evidence |
|-----|--------|-----------------------|-------------------|--------|----------|
| HLR-1601 | test | `pytest tests/test_present.py tests/test_present_rulers.py tests/test_present_room.py` | every arm passes; frames = `PRES-R2-118x30/80x24.txt` line for line | executed · pass | suite-p4 (orchestrator); `tests/test_present.py:81,87,171`; qa re-run 47 passed |
| LLR-1601.1 | test (unit) | `-k "TC_1601 or TC_1608"` | accent today, bright/over echo, no weekend bg; TC-1608 arms | executed · pass | M1, M4, M5, M8, Q1–Q7 KILLED |
| LLR-1601.2 | test (unit) | `-k TC_1602` + TC-1001/1002 | 6 label cases + cross-year + unparseable + 3 tones; frames exact | executed · pass | M2, M3, M7 KILLED |
| HLR-1602 | test | `pytest tests/test_present_hide.py tests/test_present.py tests/test_report.py` | every arm passes | executed · pass | suite-p4; the zero-save arms green |
| LLR-1602.1 | test (unit) | `-k TC_1603` | byte-identical round-trip; `false` only; `"no"` → shown | executed · pass | N1, N2, N3 KILLED |
| LLR-1602.2 | test (integration) | `-k "TC_1604 or AT_1602"` | filter, axis, cursor ends, all-hidden, no-op writes, hint texts | executed · pass | N4–N6, N8, N9, N11 KILLED; N7 declared equivalent |
| LLR-1602.3 | test (integration) | `-k TC_1605` + `tests/test_edit_window.py` | `f-present` painted at 80×24, toggles, Save writes; `TASK_CHIPS_ONE_ROW` unchanged | executed · pass | N10 KILLED |
| HLR-1603 | test | `pytest tests/test_help_keys.py tests/test_help_clip.py tests/test_legend.py tests/test_setup_help.py` | every arm passes | executed · pass | suite-p4 |
| LLR-1603.1 | test (unit) | `-k TC_1606` | each key once, column-major, ≤ inner width; the 7-in-3 order arm | executed · pass | P1, P5, P6 KILLED |
| LLR-1603.2 | test (unit + integration) | `tests/test_help_keys.py` | the line = every `bar=False` key; row count computed; no split | executed · pass | P2, P3, P4 KILLED |
| HLR-1001 (repointed: TC-1001/TC-1002/AT-1001) | test | `tests/test_present.py -k "TC_1001 or TC_1002 or AT_1001"` | frames equal `PRES-R2-*`; `R`/move/`x`/`esc` write nothing | executed · pass | the old PRES-C oracle RED against the new renderer (`inc001-red-old-oracle.txt`) |

### Layer B — behavioral (black-box) acceptance

| US | Acceptance test (`AT-NNN`) | Surface driven | Deliverable observed (path / element) | repr · boundary · negative | Result |
|----|----------------------------|----------------|---------------------------------------|----------------------------|--------|
| US-1601 | AT-1601 → `tests/test_present_rulers.py::test_AT_1601_R_paints_the_ruler_and_the_dates_follow_the_cursor` | `R`, `→` via `run_test` 118×31 | `#present-frame` rows 1–5 | repr: oracle board · boundary: the cursor on a no-start task (`due Oct 6`), 80×24 by TC-1002 · negative: RED on base (`red-001.txt`) | executed · pass (orchestrator) |
| US-1602 | AT-1602 → `tests/test_present_hide.py::test_AT_1602_space_hides_and_it_is_remembered_a_shows_all` | `R`, `space`, `x`, restart, `a` | `#present-frame`, `#present-hint`, `board.json` bytes, `reports/present-*.svg` | repr: hide the cursor task · boundary: restart persistence, byte restore · negative: the SVG holds no `hidden`/title; `red-002.txt` | executed · pass (orchestrator) |
| US-1603 | AT-1603 → `tests/test_help_keys.py::test_AT_1603_the_help_shows_the_global_keys_without_scrolling` (parametrised 118×30 / 80×24) | `3`, `?`, `end` | compositor rows (global line + Keys band) | repr: 118×30 · boundary: 80×24 · negative: RED on base (`red-003.txt`) | executed · pass (orchestrator) |
| HLR-1001's story (batch-04, repointed) | AT-1001 → `tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle` | `R`, move, `x`, `esc` | `#present-frame` = `PRES-R2-118x30.txt`; SVG (+PNG where Edge renders) | repr · zero-save negative · old-oracle RED | executed · pass (orchestrator) |

### Bidirectional surface-reachability matrix (extends A-5)

| Direction | US dimension / deliverable | Service param / producer | Reached/observed at surface? | TC / AT | Status |
|-----------|---------------------------|--------------------------|------------------------------|---------|--------|
| input | `R` | `PresentScreen` open | yes | AT-1601, AT-1602, AT-1001 | ✓ |
| input | `←/→` (and `↑↓`) | cursor move | yes | AT-1601, TC-1604 | ✓ |
| input | `space` | hide the cursor task | yes | AT-1602, TC-1604 | ✓ |
| input | `a` | show all | yes | AT-1602, TC-1604 | ✓ |
| input | `x` | `save_present_svg` / `save_present_png` | yes | AT-1602, AT-1001 | ✓ |
| input | `?` | `HelpModal` | yes (both sizes) | AT-1603 | ✓ |
| input | editor checkbox `f-present` | `TaskModal` result `show_in_present` | yes (80×24) | TC-1605 | ✓ |
| output | frame (ruler, chips, field) | `views.render_present` | yes, `#present-frame` | AT-1601, AT-1001 | ✓ |
| output | SVG export | `save_present_svg` | yes, `reports/present-*.svg` | AT-1602, AT-1001, TC-1608 | ✓ |
| output | PNG export | `save_present_png` (needs Edge) | conditional: the file OR the "PNG needs Microsoft Edge" toast; content never asserted | AT-1001 | gap (G-004) |
| output | board.json | `Board._to_dict` | yes, bytes on disk | AT-1602, TC-1605 | ✓ |
| output | hint row | `#present-hint` | yes | AT-1602, TC-1604 | ✓ |
| output | help modal | `HelpModal` | yes, compositor rows | AT-1603 | ✓ |

### Signed-balance test ledger

| base | − D | + A | = post | actual collected | passed-lean / full | reconciles? |
|------|-----|-----|--------|------------------|--------------------|-------------|
| 2592 (`64443be`: 2590 passed + 2 pre-existing fail) | 0 | 42 (13 + 13 + 9 + 7) | 2634 | 2634 (suite-p4 3 + 2631, orchestrator; `--collect-only`, qa-reviewer) | n/a (no `slow` marker) / 2631 passed + 2 pre-existing + 1 environment | yes |

### Gaps detected

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | — (no batch change) | `tests/test_app.py::test_win_clipboard_roundtrip` failed in the gate run and in two re-runs: the machine-global clipboard refused `Set-Clipboard` in the test's setup guard. Attribution to the environment accepted by qa-reviewer (the failure precedes the code under test; the batch diff touches no clipboard code; green in suite-001..004), but no green run exists on `8cd8dbd` — `not-run` there | minor | carried to `BACKLOG.md`: re-run the node when the clipboard is free |
| G-002 | — (out of scope) | 2 standup tests fail at base `64443be` (the name scrub), unchanged by the batch | minor | already in `BACKLOG.md` |
| G-003 | HLR-1601 / §6.3 | ⏸ DEFER the operator's visual verdict on the 80-column oracle frame (`PRES-R2-80x24.txt`) — owed | minor | already in `BACKLOG.md` |
| G-004 | HLR-1001 (export) | the PNG export is observed only conditionally (file OR toast); its content never asserted | minor | accepted as a declared limit: the PNG is Edge's raster of the asserted SVG |
| G-005 | HLR-1601 (supersession) | comment/docstring refs to the superseded oracle and "hybrid" (`views.py:6023,6028,6273`; `tests/test_present.py:75`; test names `*_presc_frame_*`) — no live dependency | minor | carried to `BACKLOG.md` as a doc-only cleanup |
| G-006 | LLR-1601.1 | `selected: no dates` (dim) for a dateless selection is the orchestrator's decision (LED .8, increment 004 review F2), not in the operator's verdict | minor | owed to the operator: approve or reject; carried to `BACKLOG.md` |
| G-007 | — (evidence quality) | `mutation-001.txt` M1/M4 lines are truncated before the changed token; the mutations are described in the increment 001 packet and the RED is recorded | minor | noted; widen `mutate.py`'s printed window next time |

### Escaped-bug regression (if a defect escaped the suite)

none — no defect escaped the suite in this batch.

### Evidence checklist — qa-reviewer (full)

- [x] Acceptance criteria are observable — ✓ each HLR acceptance block states outcome, surface and AT (`01-requirements.md` §3).
- [x] Test cases have an explicit Expected — ✓ every Layer A row carries a numeric threshold; the ATs assert literals (`tests/test_present_rulers.py:199-210`, `tests/test_present_hide.py:349-375`).
- [x] Edge cases include empty, boundary, invalid, error — ✓ the boundary catalog per HLR/LLR; error "none new", with its reason.
- [x] Regression checklist exists — ✓ reverse census in increments 001-004 + the repointed TC-1001/1002/AT-1001 + the full gate suite.
- [x] Exit criteria stated — ✓ `01-requirements.md` §5.2.
- [x] No real PII / secrets — ✓ fixture `tests/present_board.py`; the `username_subject` placeholder.
- [x] Mode declared — ✓ `validation`.
- [x] Every case carries a result or a state, executor named — ✓ all `executed` by the orchestrator; qa-reviewer's targeted re-run named separately; G-001 `not-run` on HEAD.
- [x] Layer B — ✓ AT-1601/1602/1603 + AT-1001 drive `run_test` and observe the frame, the hint, `board.json`, the SVG.
- [x] Bidirectional surface-reachability — ✓ 7 inputs, 6 outputs; 1 minor gap (G-004).
- [x] No unfilled template — ✓ every TC/AT bound to a node.

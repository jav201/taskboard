# Increment 001 — LLR-1701.1 · `the tick row's label names the selection, never the scale, in both views`

| Field | Value |
|---|---|
| Batch | `2026-10-17-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1701` / `LLR-1701.1` (LED-2026-10-17-batch-01.1, .2, .3) |
| Acceptance | `AT-1701` · white-box `TC-1701` · unit: `_gantt_tick_label` (layer 0: three branches, cyclomatic 4) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-17` |

## 1 · What changed

The operator's commission of 2026-10-17 («Es la etiqueta de Mondays y cells? … hay que quitarla. No agrega valor»). `taskboard/views.py` gains `_gantt_tick_label(selected, echo, meta, label_w)`, the one rule both views now call for the tick row's label: `selected task ▸` in the echo's tone, bold, when the selected task's echo fits the field; the echo's own text plus ` ▸` when it does not; `selected: no dates` in `dim` for a dateless selection; blank with nothing selected. `_gantt_frame` (the gantt view, and link mode, which paints the same frame) and `_present_ruler` (the presentation and its `x` export) both call it; `_gantt_scale_label` — the scale text `Mondays · 1 day = 2 cells` / `Mondays · .5 d/cell` — is deleted (P-1: it had no other caller). Five pinned tests of earlier batches change law-driven (§4), and `tests/test_tick_label.py` encodes why: no frame of either view or of the export ever paints the scale text, and the label names the selected task.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-1701.1 | `_gantt_tick_label` added; `_gantt_scale_label` deleted; `_gantt_frame` and `_present_ruler` label their tick row with it; `_present_ruler` docstring |
| `tests/test_tick_label.py` | test | HLR-1701, LLR-1701.1 | new: TC-1701 (26 nodes, the pattern's positive control and the layer-0 branch test among them) and AT-1701 (4 nodes) |
| `tests/test_gantt_board.py` | test | HLR-1701, LLR-1701.1 | AT-104: the day-row label assertion `Mondays · 1 cell = 1 day` → `selected task ▸`, docstring (its "nothing selected" premise was false: `_select_first` re-selects); TC-110 deleted with the function it pinned |
| `tests/test_present_rulers.py` | test | HLR-1701, LLR-1701.1 | TC-1601: the no-cursor tick label `Mondays · 1 day = 2 cells` → blank, plus the ticks still paint; docstring |
| `tests/test_present_room.py` | test | HLR-1701, LLR-1701.1 | TC-1608: the `_scale_text` helper (it called the deleted function) → `_is_scale_text`, written from the rule (the `SCALE_TEXT` pattern, after code-review F-3) with its own positive control and false-match guard; (c)'s last arm: no selection → blank; module docstring |
| `tests/test_gantt.py` | test | HLR-1701 | the dead-cell law `dead <= 25` → `<= 25.5` = 25 + 100·15/2880, the 15 cells the removed `Mondays · 1 d/cell` inked at 96×30 (QA2-1); docstring states the derivation |
| `.dev-flow/2026-10-17-batch-01/evidence/mutate.py` | doc | LLR-1701.1 | the mutation battery (7 mutants, 19 arms) |
| `.dev-flow/2026-10-17-batch-01/evidence/capture_app.py` | doc | HLR-1701 | batch-01's capture tool re-aimed at the gantt view |
| `.dev-flow/2026-10-17-batch-01/evidence/captures/app-001-*.svg`, `app-001-118x31-gantt-selected.png` | generated | HLR-1701 | the real app at 118×31 and 80×25: gantt selected, none, dateless; presentation all hidden |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_tick_label.py tests/test_present_room.py tests/test_present_rulers.py tests/test_gantt_board.py tests/test_gantt.py tests/test_present.py`; full suite `python -m pytest -q -p no:cacheprovider`; mutants `python .dev-flow/2026-10-17-batch-01/evidence/mutate.py <a tree no one else reads>`; captures `python .dev-flow/2026-10-17-batch-01/evidence/capture_app.py`. By hand: `3` with a task selected → the third row's label reads `selected task ▸`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 | `tests/test_tick_label.py::test_TC_1701_the_label_function_branches` | in the full suite (`suite-001.txt`) |
| A | `tests/test_tick_label.py` TC-1701 (the other 25 nodes); TC-1608, TC-1601, AT-104, the dead-cell law, TC-1001/TC-1002 (PRES-R2 frames, unchanged) | in the full suite (`suite-001.txt`) |
| B | `tests/test_tick_label.py::test_AT_1701_the_tick_row_names_the_selection` ×2, `::test_AT_1701_a_board_with_no_task_has_a_blank_label` ×2 | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` | 2 failed, 2661 passed — 2663 collected = 2634 at base − 1 (TC-110) + 30 (`test_tick_label.py`); the 2 failures are the known standup pair in `tests/test_team_views.py` (pre-existing since the 2026-10-11 rewrite, backlog) (`suite-001.txt`); `test_present_room.py` re-run alone after code-review F-3: 7 passed (`suite-001-f3.txt`) |

Assertions that changed, and why each legitimately did (B1, the census of LED .1/.2 and QA2-1): AT-104 (2026-10-02-batch-01) — the day row's label is no longer the scale; the test cleared `selected_task_id`, but the gantt view re-selects a drawn task (F-3), so the label names it; TC-110 — deleted with `_gantt_scale_label`, whose fit at 20 cells it pinned (coordinator's decision); TC-1601 (2026-10-16-batch-01) — with no cursor the label is blank where it was the scale, and the ticks are now asserted to paint; TC-1608 (c) — its scale helper called the deleted function, and its no-selection arm expected the scale; the dead-cell law — the scale's 15 cells are blank by the operator's decision, the bound moves by exactly their share. No other assertion changed; the PRES-R2 and C-2b oracle frames are unchanged (B3: no cursor-less frame among them).

| Field | Value |
|---|---|
| **RED counterfactual** | `tests/test_tick_label.py` run on the base source (`HEAD` `de9c4a2`, `taskboard/` unmodified, `views.py` sha256 `42181496e6d0148959a4faa9b7ebda940ff0a005d6c7a58c5b8bb1cb24127294`, the transcript's header): 27 failed, 3 passed — every TC-1701/AT-1701 arm RED on the scale text (`assert 'Mondays · 1 cell = 1 day' == 'selected task ▸'`), GREEN only the pattern's positive control and the gantt too-long-echo arm ×2 (unchanged behaviour: the base already labelled an overflowing echo with its own text) · `.dev-flow/2026-10-17-batch-01/evidence/red-001.txt` · the restore is the increment's own bytes, `views.py` sha256 `28c5ad717e2309d40a6d114c7e12825f26800c7954b0b8a06fbdfb27a0587876` |
| **Mutation verdicts** | 7 mutants × 19 arms, one node per run, all KILLED: M1 the no-selection branch returns the scale text (5 arms) · M2 the echo branch paints `dim` (2) · M3 the dateless branch paints `over` (2) · M4 a too-long echo labelled `selected task` (2) · M5 a dateless selection treated as none (2) · M6 the gantt view passes no selection (3, incl. link mode and AT-1701) · M7 the presentation passes no cursor (3, incl. TC-1608 and AT-1701) · arms that stayed GREEN: none · run in a scratch `git worktree` holding the increment's exact bytes while the full suite ran in the checkout · `.dev-flow/2026-10-17-batch-01/evidence/mutation-001.txt` · restore digest `28c5ad717e2309d40a6d114c7e12825f26800c7954b0b8a06fbdfb27a0587876` (before = after, every arm) |
| **Instrument RED-proof** | 1 instrument: the scale-text pattern `SCALE_TEXT` — shown able to report a match first: its positive control matches the five old labels, plain and inside a `save_present_svg` SVG (`test_TC_1701_the_scale_pattern_sees_every_old_label`), and on the base tree the sweep arms went RED on it (`red-001.txt`); the harness `mutate.py` asserts its arm count (19) and that each edit applied |
| **Emitted-form assertion** | 1 artifact: the presentation's `x` SVG — TC-1701 (b) reads the bytes `save_present_svg` writes, with `&#160;` read as a space (measured on the base export: 54 × `&#160;`, 0 × `&amp;#160;`), positive controls `PRESENT` and `Redesign` readable in it |
| **Reverse census** | 5 probes: B1 `grep -rln "_gantt_scale_label\|d/cell\|1 cell = 1 day\|1 day = 2 cells\|cadence" tests/` → `test_gantt_board.py` (AT-104 changed, TC-110 deleted; `:223-227, 238, 318, 336-343, 750` read and survive), `test_present_rulers.py` (TC-1601 changed; `:105-108, 200-208` survive), `test_present_room.py` (TC-1608 changed; `:70, 100` survive), `test_gantt_polish.py:336-338`, `test_present_hide.py:203-211`, `test_gantt.py:589-606` (survive), `test_gantt_link.py:53` (a comment about the axis, unaffected); plus the C-39 full-suite pre-execution, which found the one hit grep cannot see — `test_gantt.py:287`, the dead-cell law (changed, QA2-1) · B2 no file moved · B3 the PRES-R2 and C-2b frames: 0 hits of the pattern (`grep -c cell` → 0), unchanged; only increment 001's `PRES-R-*.txt` of 2026-10-16-batch-01 match, read by no test · B4 the `x` export: TC-1701 (b) reads it · A3 `git grep -n _gantt_scale_label -- taskboard tests` after the change → no hit; `gantt_day_row`'s signature and `meta` unchanged — 0 foreign hits left |
| **Correction population** | the operator's correction of shipped label text: the population is every site that painted `_gantt_scale_label` — `_gantt_frame` (gantt view, link mode, the gantt legend's frame call reads only the month row and body) and `_present_ruler` (presentation, `x` SVG, PNG raster of that SVG) — enumerated by `git grep` before the first edit (P-1); both sites now call `_gantt_tick_label`, all covered by TC-1701 |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-17-batch-01/evidence/suite-001.txt | 7fd65d3115e5a816b9653977267d1d3c91da057639adca382faa56bc9b8440df |
| suite-001-f3.txt | .dev-flow/2026-10-17-batch-01/evidence/suite-001-f3.txt | 94f0aa50d63df60964e0bb5613ca42b2cb4e4a6913c719409aa55ab3b3616ed5 |
| red-001.txt | .dev-flow/2026-10-17-batch-01/evidence/red-001.txt | c2fd3dae79744abd4176e2ff926075970621af1ee38509aa09886093341a4194 |
| mutation-001.txt | .dev-flow/2026-10-17-batch-01/evidence/mutation-001.txt | e2f8ecbf103ed75a2ba4508464703cf1fc54cdf7f9f51468aa56d98417e0cf7a |
| app-001-118x31-gantt-nodates.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-118x31-gantt-nodates.svg | b89c53b4e46fe8c8a6f133db599f1d7f7fed58fc1fe817c16f6a70a834398701 |
| app-001-118x31-gantt-none.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-118x31-gantt-none.svg | f839722a4dc868487a7beaec95b7fe58ff6999f95e0dda527cd514a6d889f2f2 |
| app-001-118x31-gantt-selected.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-118x31-gantt-selected.svg | afd60f196d4be44aab2e73671472bc11eaa277c178564c7f140d5667e5ec794f |
| app-001-118x31-present-all-hidden.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-118x31-present-all-hidden.svg | 438663cffab18dab24cb7611abbba288e6a3257b669641305d57f578a2cb7a4a |
| app-001-80x25-gantt-nodates.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-80x25-gantt-nodates.svg | 4905984e9283b33ef6b8ac84b1a51e1b9caef9ad8f72267507bffdafd3d39045 |
| app-001-80x25-gantt-none.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-80x25-gantt-none.svg | a57e267f32b8b900325dd335b392a68e0592daa318896f768b3cdaa9efd01946 |
| app-001-80x25-gantt-selected.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-80x25-gantt-selected.svg | 322bfd18a11ae587bd24ed913f5cf8052edfa5ab29d1b77d2e44cd5dc4963c96 |
| app-001-80x25-present-all-hidden.svg | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-80x25-present-all-hidden.svg | b79754272eb4af7aad77355dc303d65dda1ad2d4fda878c506ab8e00b92e2d08 |
| app-001-118x31-gantt-selected.png | .dev-flow/2026-10-17-batch-01/evidence/captures/app-001-118x31-gantt-selected.png | 09c7a75538d8c7faa81b2c72a6081c3cda53706cbfd7a7502fc27190715ca436 |

| Field | Value |
|---|---|
| **Evidence files** | 13 artifacts, each at the declared home, with the digest of its bytes on disk (rows printed by `devflow-evidence.py`; its `--write` refused because the root `.gitattributes` carries no mark for this home — the mark is the nested `evidence/.gitattributes` (`** -text`), since the root file is a pre-existing dirty file the commission leaves alone; `git check-attr text` → `unset`) |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-with-notes (OK to advance), 0 HIGH · F-1 MEDIUM: four canon rows (HLR-105, LLR-101.10, LLR-1601.1, LLR-1602.2) still `active` while requiring the scale label → planned at close step 1 (the canon's status cells, with LLR-102.2; LED .1/.2 §6.3) · F-2 LOW: the README hero image → Out of scope (LED .2), to `BACKLOG.md` at the close · F-3 LOW: `test_present_room.py`'s `"cell" in label` would also match `cancelled` → fixed: the same pattern as `SCALE_TEXT`, plus a false-match guard; the file re-run, 7 passed (`suite-001-f3.txt`) · F-4 NIT: `meta["cadence"]` written and no longer read → kept: `gantt_day_row`'s `meta` is left unchanged on purpose (A3 not fired; LLR-102.1's cadence still drives the ticks) |

## 5 · Risks

The label column narrows below 60 columns (`max(6, width // 3)`): at 48 columns `selected: no dates` reads `selected: no d…` (accepted, LLR-1701.1); below 48 `selected task ▸` is cut too. The gantt view always holds a selection while it draws a task (`_select_first`), so "blank" appears only when it draws none (a search that matches nothing, a board without open tasks) — stated in HLR-1701. The capture's `gantt-none` step reaches that state through a search (`zzqx`), not a cleared selection.

## 6 · Pending items / spec deviations

None against the contract. Carried: the README hero image `docs/taskboard-gantt.svg` still shows `Mondays · 1 d/cell` (Out of scope, LED .2; to `BACKLOG.md` at the close); the operator's approval of `selected: no dates` stays an open backlog item. Finding for the record: AT-104's "nothing selected" premise had been false since batch 2026-10-02-batch-01 (the base label was the scale shown *with* a selection) — corrected in its docstring.

## 7 · Suggested next task

Phase 4, `stations/p4-validation.md`: the gate run of the full suite.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_tick_label.py` (30 nodes) + 5 law-driven updates |
| 3 | Layer 0 where it applies | ✓ | `_gantt_tick_label`: cyclomatic 4 → `test_TC_1701_the_label_function_branches`, every branch, killed M1–M5 |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt`: 27 failed on base |
| 5 | Reverse census | ✓ | §4: 5 probes + the C-39 pre-execution; every hit re-validated |
| 6 | `code-reviewer` passed | ✓ | §4b: PASS-with-notes, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen in this repo |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | the absence claims (no scale text; no caller of the deleted function) each carry a positive control: the pattern matches the old labels; `git grep` found the 3 sites before the change |
| 11 | Mutation verdicts | ✓ | §4: 19/19 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: the pattern's positive control; the harness's arm count |
| 13 | Correction population | ✓ | §4: 2 sites, enumerated first |
| 14 | Emitted-form assertion | ✓ | §4: the `x` SVG bytes |
| 15 | Independent review | ✓ | §4b: spawned `code-reviewer`; F-3 fixed, F-1/F-2/F-4 routed |
| 16 | Evidence files | ✓ | §4: 13 digests printed by `devflow-evidence.py` (`--write` refused on the root mark; declared) |

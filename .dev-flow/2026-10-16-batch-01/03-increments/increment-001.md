# Increment 001 — LLR-1601.1, LLR-1601.2 · `the presentation's date ruler and start–end chips`

| Field | Value |
|---|---|
| Batch | `2026-10-16-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1601` / `LLR-1601.1`, `LLR-1601.2` (and the repointed `LLR-1001.1` oracle, LED-2026-10-16-batch-01.1) |
| Acceptance | `AT-1601` (+ the repointed frame arm of `AT-1001`) · white-box `TC-1601`, `TC-1602`, `TC-1001`, `TC-1002` · unit: `TC-1601`/`TC-1602` are unit-level (layer 0: `present_span_label` has 6 branches) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-16` |

## 1 · What changed

`R`'s frame gains the gantt view's two ruler rows above the span row — the month row (today's number and the `today Wed Sep 30` label in accent, the project's due `◆`) and the tick row (the cursor task's exact dates via `gantt_echo`, in its own tone; the echo's full text plus ` ▸` in the label column when it has no room in the field, else the scale label) — with no weekend shading (`gantt_day_row` gains `*, shade_weekends=True`; the gantt view keeps the default). Every field row now ends with a 13-cell start–end chip (`present_span_label`: `Sep 24–28`, `Aug 21–Oct 10`, `due Oct 14`, `Oct 6`, `from Sep 3`, `no dates`), `over` once the due has passed; columns label 30/20, chip 13. The brief rows keep the relative days. The PRES-R oracle frames are written into this batch's evidence and cross-checked against the approved prototype; TC-1001/TC-1002/AT-1001 are repointed to them.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-1601.1, LLR-1601.2 | `gantt_day_row(..., shade_weekends=True)`; `_present_cols` 30/20 · 13; `present_span_label` + `_present_chip(start, due, today, width)` replace the due-and-distance chip; `_present_ruler`; `render_present` appends the ruler; section comment and two docstrings updated |
| `tests/test_present_rulers.py` | test | HLR-1601, LLR-1601.1, LLR-1601.2 | new: TC-1601 ×3, TC-1602 ×3 (+7 parametrised label cases), AT-1601 |
| `tests/test_present.py` | test | LLR-1001.1 (repointed by HLR-1601) | `FRAMES` → this batch's `PRES-R-*`; docstrings; assertions unchanged |
| `.dev-flow/2026-10-16-batch-01/evidence/gen_frames.py` | doc | HLR-1601 | the oracle writer + `render_b2` cross-check (D1/D2/D3 declared); batch record, not shipped |
| `.dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R-118x30.txt` | generated | LLR-1601.2 / TC-1001, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R-80x24.txt` | generated | LLR-1601.2 / TC-1002 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-16-batch-01/evidence/mutate.py` | doc | this batch's increments | the mutation harness; batch record |
| `.dev-flow/2026-10-16-batch-01/evidence/capture_app.py` | doc | this batch's increments | the running-app capture; batch record |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-001-118x31-present-open.svg` | generated | HLR-1601 (AT-1601) | the app's own `export_screenshot()` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-001-118x31-cursor-moved.svg` | generated | HLR-1601 (AT-1601) | the app's own `export_screenshot()` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-001-80x25-present-open.svg` | generated | HLR-1601 (AT-1601) | the app's own `export_screenshot()` |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-001-80x25-cursor-moved.svg` | generated | HLR-1601 (AT-1601) | the app's own `export_screenshot()` |
| `prototypes/present_rulers/app_capture.py` | doc | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/build_html.py` | doc | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/legend_proto.py` | doc | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/app-118-1-open.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/app-118-2-cursor-moved.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/app-118-3-hidden.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/app-118-4-show-all.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/app-80-1-open.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/app-80-3-hidden.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/legend-grid.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/legend-proposed.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/legend-shipped.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-A-118x30.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-A-118x30.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-A-80x24.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-A-80x24.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-B-118x30.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-B-118x30.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-B-80x24.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-B-80x24.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-B2-118x30.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-B2-118x30.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-C-118x30.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-C-118x30.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-C-80x24.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-C-80x24.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-S-118x30.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-S-118x30.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-S-80x24.svg` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/out/present-S-80x24.txt` | generated | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/present-rulers-prototype.html` | doc | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |
| `prototypes/present_rulers/proto.py` | doc | HLR-1601, HLR-1602, HLR-1603 | the prototype round (not modified) behind the operator's verdict of 2026-10-16; committed unmodified |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_rulers.py tests/test_present.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the cross-check: `python .dev-flow/2026-10-16-batch-01/evidence/gen_frames.py`; the captures: `python .dev-flow/2026-10-16-batch-01/evidence/capture_app.py 001`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 and A | `tests/test_present_rulers.py` TC-1601 ×3, TC-1602 ×3 (9 nodes with the parametrised cases); `tests/test_present.py` TC-1001, TC-1002 | in the full suite (`suite-001.txt`) |
| B | `tests/test_present_rulers.py::test_AT_1601_R_paints_the_ruler_and_the_dates_follow_the_cursor`; `tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle` | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` | 2 failed, 2603 passed (`suite-001.txt`); the 2 failures are pre-existing on `base_ref` (`preexisting-base-failures.txt`: `tests/test_team_views.py` standup ×2, the 2026-10-11 rewrite), not this increment's |

| Field | Value |
|---|---|
| **RED counterfactual** | every new and repointed node run against `taskboard/views.py` at `base_ref` `64443be`: 16 failed, 2 passed (the 2 = TC-1003/TC-1004, untouched) · `.dev-flow/2026-10-16-batch-01/evidence/red-001.txt` · restore digest `fdfc82532dfabc6728aa363814c90014befab53c2780cc663ec0a51ac141b5bc`; and the old PRES-C oracle against the new renderer: TC-1001, TC-1002, AT-1001 failed (`inc001-red-old-oracle.txt`) |
| **Mutation verdicts** | 8 mutants on `taskboard/views.py`, all KILLED: M1 `shade_weekends=False`→`True` (TC-1601) · M2 `chip_w = 13`→`12` (TC-1602, TC-1001) · M3 same-month label → `<Mon D>–<Mon D>` (TC-1602) · M4 echo tone forced `bright` (TC-1601) · M5 today label `accent`→`bright` (TC-1601) · M6 ruler rows not appended (AT-1601, AT-1001) · M7 past-due chip `over`→`mut` (TC-1602) · M8 echo label tone → `dim` (TC-1601) · arms that stayed GREEN: none · `.dev-flow/2026-10-16-batch-01/evidence/mutation-001.txt` · restore digest `fdfc82532dfabc6728aa363814c90014befab53c2780cc663ec0a51ac141b5bc` |
| **Instrument RED-proof** | 2 instruments: `mutate.py` (its first run reported `NOT APPLIED` on CRLF anchors — a failure it can report — then KILLED on each), `gen_frames.py` (its first run FAILED on row 2 before D3 was declared, LED .7) |
| **Emitted-form assertion** | 2 artifacts: the oracle frames are asserted as the renderer EMITS them (`Text.plain` rows, `test_present.py::_frame`); the captures are the app's own `export_screenshot()` SVG |
| **Reverse census** | 5 probes: B1 `grep -rl` for `render_present`, `_present_chip`, `_present_cols`, `gantt_day_row`, `present_span_label`, `_present_ruler`, `PRES-C` over `tests/ prototypes/ taskboard/` → `test_present.py` (repointed), `test_markup_census.py` (the presentation seat row: still true — `PresentScreen._paint` unchanged), `test_present_rulers.py` (new), `prototypes/present_rulers/*` (throwaway; `gantt_day_row`'s new keyword defaults, `_present_cols` callers there still run — `gen_frames.py` imports them); `_present_chip` reaches only `views.py` and the new test · B2 no file moved · B3 `ls tests/goldens` → none; the byte oracle is the batch evidence frame, re-captured and named · B4 the SVG export carries the new frame (AT-1001 `x` arm green) · A3 `gantt_day_row`'s keyword defaults to the shipped behaviour (TC-1601 gantt arm) — 0 foreign hits left un-revalidated |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-16-batch-01/evidence/suite-001.txt | e6e34aa4e50d8fed2f16390b72efc5c45e34b284c95f450228787159dcda6e24 |
| red-001.txt | .dev-flow/2026-10-16-batch-01/evidence/red-001.txt | b7166525330095762ca1c93699f80869c4ed2d9ac693798f5a01588210e6a494 |
| inc001-red-old-oracle.txt | .dev-flow/2026-10-16-batch-01/evidence/inc001-red-old-oracle.txt | 468190b14a4cf0d7d267bd16bf2f2b6544091be7ff4529ee862c3d8a5955a56e |
| mutation-001.txt | .dev-flow/2026-10-16-batch-01/evidence/mutation-001.txt | f98e911b0e029200b411b14431a1bd0a828f9f0c931d9e630369f83ba6c9676d |
| preexisting-base-failures.txt | .dev-flow/2026-10-16-batch-01/evidence/preexisting-base-failures.txt | 9467ed9e1141d1fe6b9dfc705e3e86ec73c97cfe66d92ff690a126c95b7f31f2 |
| PRES-R-118x30.txt | .dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R-118x30.txt | d74f7082552028cefb2bc2e45ad826e3d9063c231833a50862ec654b1db0f328 |
| PRES-R-80x24.txt | .dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R-80x24.txt | da72253d5a2889dfdeaf811b47a3dafa6917371135ef71674d5dcebc4c0762e7 |
| app-001-118x31-present-open.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-001-118x31-present-open.svg | b7bc76ce4c9e6c479b39c7b757e6bccf4daadb37191bfc7c0ddba5da83ba8767 |
| app-001-118x31-cursor-moved.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-001-118x31-cursor-moved.svg | a38ead76bef77438a0961b2b2b63da8f9adb6659fafdd9dd4afabca8b2a2196a |
| app-001-80x25-present-open.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-001-80x25-present-open.svg | 1c1b80e555349ac2ed0cde94ef6645e99e31ea1685041b3eb49dff0f426bbf0e |
| app-001-80x25-cursor-moved.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-001-80x25-cursor-moved.svg | 906f2f0d183c31d07f1e5c1c7d3bb42b1117de0fc9e0391a32f13a60086bbd3c |

| Field | Value |
|---|---|
| **Evidence files** | `11 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 MEDIUM (the echo-in-label branch untested) → fixed: `test_TC_1601_an_echo_too_long_for_the_field_moves_to_the_label` + mutant M8 KILLED · F2 LOW (two stale PRES-C/C-2b docstrings) → fixed · F3 LOW (~10 lines repeat the gantt ruler layout) → deferred to `BACKLOG.md` (sharing it would touch the gantt view) |

## 5 · Risks

The oracle comes from the shipped renderer; its independence rests on the `render_b2` cross-check (layout and chips, D1/D2/D3 declared) and the hand-written literals (ruler cells). The 80-column frame has no operator visual verdict yet (deferred in the contract §6.3 and carried in `BACKLOG.md`).

## 6 · Pending items / spec deviations

- LED-2026-10-16-batch-01.7: the cross-check's third delta D3 (the tick-row label follows the commission, not the prototype).
- Kept as shipped and declared for the operator: the header's ` — hybrid` suffix and the in-frame keys row (the prototype capture dropped both).
- 2 pre-existing failures on `base_ref` (team standup), carried to `BACKLOG.md`.

## 7 · Suggested next task

Increment 002 — the persisted "show in presentation" flag (`models.py`, `app.py`, `modals.py`, `views.py`).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_rulers.py` (new), `tests/test_present.py` (repointed) |
| 3 | Layer 0 where it applies | ✓ | `present_span_label` (6 branches): TC-1602 unit cases |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: 0 HIGH, F1/F2 fixed, F3 deferred |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | B3's absence (no goldens dir) is the only empty probe; positive control: the batch evidence frames ARE found and repointed |
| 11 | Mutation verdicts | ✓ | §4: 8/8 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: both instruments shown failing first |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |

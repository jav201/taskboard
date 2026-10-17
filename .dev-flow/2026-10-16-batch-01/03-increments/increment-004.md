# Increment 004 — LLR-1601.1, LLR-1602.2 · `the frame speaks to the room: the tick label names the selected task; no " — hybrid", no in-frame keys`

| Field | Value |
|---|---|
| Batch | `2026-10-16-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1601` / `LLR-1601.1`; `HLR-1602` / `LLR-1602.2` (the all-hidden frame); amended by `LED-2026-10-16-batch-01.8` |
| Acceptance | `AT-1601` (unchanged) · white-box `TC-1608` (new), `TC-1001`/`TC-1002`/`AT-1001` (repointed frames), `TC-1604` (all-hidden arm) · unit: `_present_ruler`'s label branch (layer 0: three branches) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-17` |

## 1 · What changed

The operator's verdict on the P3 handoff (2026-10-17), items 2 and 3. In `views._present_ruler` the tick row's label no longer shows the axis scale (`Mondays · 1 day = 2 cells`) while a task is selected: when the selected task's echo fits in the field the label reads `selected task ▸`, right-aligned, bold, in the echo's tone — it names what the bright dates on that row are; when the echo does not fit, the echo's full text plus ` ▸` stays (the existing fallback); when the selected task has no date the label reads `selected: no dates` in `dim` (the orchestrator's decision: the verdict did not name this case, and the label must still never be the scale while a task is selected); with no selected task (no open task) the scale label stays. In `views.render_present` the header loses ` — hybrid` and the in-frame keys row (`←→  move the cursor · the cursor'd task's notes expand`) is gone; the freed row is padding (or content when the brief needs it). The hint row below the frame already carries the keys. The PRES-R oracle frames are regenerated; `gen_frames.py`'s cross-check against the approved prototype now holds with ONE delta (D3, the tick label) instead of three — rows 0 and the former keys row now match `render_b2` byte for byte.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-1601.1, LLR-1602.2 | `_present_ruler`: label branch + docstring; `render_present`: header suffix and keys row dropped |
| `tests/test_present_room.py` | test | HLR-1601, LLR-1601.1 | new: TC-1608 ×4 (7 nodes) — no presenter text in frame or SVG; `selected task ▸` in the echo's tone; never the scale with a selection; the long-echo fallback |
| `tests/test_present_hide.py` | test | LLR-1602.2 | TC-1604 all-hidden arm: `"move the cursor" in frame[5]` → `frame[5].strip() == ""`; docstring |
| `tests/test_present.py` | test | HLR-1001 | TC-1004 docstring only (`keys row` → `ruler`) |
| `.dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R2-118x30.txt` | generated | HLR-1601 | new file: PRES-R-118x30 with rows 1, 3, 18 (1-based) changed — header, tick label, former keys row; PRES-R-* stay untouched as increment 001's hashed evidence |
| `.dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R2-80x24.txt` | generated | HLR-1601 | new file: PRES-R-80x24 with the same three rows changed |
| `.dev-flow/2026-10-16-batch-01/evidence/gen_frames.py` | doc | HLR-1601 (§6.3) | cross-check: D1/D2 retired, D3 asserts `selected task ▸` |
| `.dev-flow/2026-10-16-batch-01/evidence/mutate.py` | doc | LLR-1601.1 | battery 004 (Q1–Q7) |
| `.dev-flow/2026-10-16-batch-01/evidence/capture_app.py` | doc | HLR-1601 | the 004 plan |
| `.dev-flow/2026-10-16-batch-01/evidence/captures/app-004-*.svg`, `app-004-118x31-present-open.png` | generated | HLR-1601 | the real app, `R` open and after `→→`, at 118×31 and 80×25 |
| `.dev-flow/2026-10-16-batch-01/01-requirements.md`, `01-requirements-ledger.md` | doc | LED-.8 | the amendment (§1.2, HLR-1601, LLR-1601.1, LLR-1602.2, §5.1, §6.3) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_room.py tests/test_present.py tests/test_present_rulers.py tests/test_present_hide.py`; oracle: `python .dev-flow/2026-10-16-batch-01/evidence/gen_frames.py` (expects `HOLDS (delta D3 only)` at both sizes); captures: `python .dev-flow/2026-10-16-batch-01/evidence/capture_app.py 004`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 and A | `tests/test_present_room.py` TC-1608 (7 nodes); TC-1001/TC-1002 (repointed frames); TC-1604 all-hidden arm | in the full suite (`suite-004.txt`) |
| B | `tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle`, `tests/test_present_rulers.py::test_AT_1601_R_paints_the_ruler_and_the_dates_follow_the_cursor` | in the full suite (`suite-004.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` | 2 failed, 2632 passed (2625 at increment 003 + the 7 TC-1608 nodes) (`suite-004.txt`); the 2 failures are the pre-existing `base_ref` pair (`preexisting-base-failures.txt`) |

Assertions that changed, and why each legitimately did: TC-1001, TC-1002 and AT-1001 repointed from `PRES-R-*` to the new `PRES-R2-*` frames (regenerating in place broke increment 001's hashed evidence rows — `V41` — so the re-capture is a new file); the frames (3 rows each: header without ` — hybrid`; tick label `selected task ▸` instead of the scale; the former keys row now blank) — consumed unchanged by TC-1001, TC-1002 and AT-1001; TC-1604's all-hidden arm (the row under the separator was the keys row, now blank). No other assertion changed. `test_TC_1601_a_project_with_no_open_task_still_paints_its_ruler` still pins `Mondays · 1 day = 2 cells` with no selection — green, unchanged, and it is the no-cursor arm of the new rule.

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/views.py` at `8303045` (the batch tip before this increment) swapped in: 10 failed, 15 passed — TC-1608 ×6 (the frame/SVG arm, the label arm and the never-the-scale arm, both sizes), TC-1001, TC-1002, AT-1001, TC-1604; the long-echo fallback arm stays GREEN on base, as it should (unchanged behaviour) · `.dev-flow/2026-10-16-batch-01/evidence/red-004.txt` · restore digest `42181496e6d0148959a4faa9b7ebda940ff0a005d6c7a58c5b8bb1cb24127294` |
| **Mutation verdicts** | 7 mutants, all KILLED: Q1 the label keyed on `echo_label` again (the selected task gets `selected: no dates`) · Q2 `cursor's dates` (jargon; the label and presenter-text arms) · Q3 the label in `dim`, not the echo's tone · Q4 a dateless selection falls back to the scale · Q5 ` — hybrid` back in the header · Q6 the in-frame keys row back · Q7 the long-echo fallback lost · arms that stayed GREEN: none · `.dev-flow/2026-10-16-batch-01/evidence/mutation-004.txt` · restore digest `42181496e6d0148959a4faa9b7ebda940ff0a005d6c7a58c5b8bb1cb24127294` |
| **Instrument RED-proof** | none — no new instrument; `gen_frames.py`'s cross-check was edited and holds (`HOLDS (delta D3 only)`); its D3 arm asserts the shipped label literally |
| **Emitted-form assertion** | 1 artifact: TC-1608 (a) reads the SVG `save_present_svg` writes — the `x` export path — with positive controls (`PRESENT`, `Redesign`, `selected` readable in it) |
| **Reverse census** | 5 probes: B1 `grep -rl "render_present\|_present_ruler\|PRES-R" tests/ taskboard/ prototypes/` → `test_markup_census.py` (green), `test_present.py` (frames repointed, green), `test_present_rulers.py` (green, no assertion changed), `test_present_room.py` (new), `app.py` (caller, unchanged), `prototypes/present_rulers/*` (the approved prototype — frozen evidence, still carries ` — hybrid`/the keys row, not edited); `grep -rn "move the cursor\|hybrid" tests/` → `test_present_hide.py:209` (changed, above) · B2 no file moved · B3 the PRES-R frames are the only golden; the re-capture is written as `PRES-R2-*` by `gen_frames.py --write` after the cross-check held, the PRES-R files untouched · B4 the `x` export carries the new frame — asserted by TC-1608 (a) · A3 no signature changed |
| **Correction population** | the operator's verdict is a correction of shipped frame text: the population is every place the frame's text reaches — the frame (TC-1001/1002/AT-1001), the `x` SVG (TC-1608 a), the PNG (rasterised from that SVG, `save_present_png`), the all-hidden frame (TC-1604) — all covered |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-16-batch-01/evidence/suite-004.txt | e45126294b2370e36bb82a6995f8316f577ff95eb910cc73d4f693eb5683bc6b |
| red-004.txt | .dev-flow/2026-10-16-batch-01/evidence/red-004.txt | 8da2f7edb6614cddcf650a783634b235a5ce7fbabab9407e5a89dcb76a6469de |
| mutation-004.txt | .dev-flow/2026-10-16-batch-01/evidence/mutation-004.txt | 31ffebafa6a62fb86bb43029660257b3bbcba7e1609eea070b3ff77c5270e227 |
| app-004-118x31-present-open.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-004-118x31-present-open.svg | 0e0324121ed47aa012010eb8058036a64837775f321988f4bd07ca0fdbfa11bc |
| app-004-118x31-cursor-moved.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-004-118x31-cursor-moved.svg | b6d541a1e6b19a544a0f084d2e525d2da71d8ce8e1830ddc4fe4bb49e9b0a95d |
| app-004-80x25-present-open.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-004-80x25-present-open.svg | 8264ff82a18a9bad9ebff5e42c5d2ba112f6ef906dfd6a794395b944544be3ef |
| app-004-80x25-cursor-moved.svg | .dev-flow/2026-10-16-batch-01/evidence/captures/app-004-80x25-cursor-moved.svg | 566bd0bb46760d90ce54468fe409ca4d5f9490b737051072a25da0520276452c |
| app-004-118x31-present-open.png | .dev-flow/2026-10-16-batch-01/evidence/captures/app-004-118x31-present-open.png | b8cae5fe30ffb3109a59ec261dd9708d4c7371e9fe56133d96f80b5d32ad066e |

| Field | Value |
|---|---|
| **Evidence files** | `8 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · PASS with notes, 0 HIGH · 0 MEDIUM · F1 LOW (the gantt view's own tick label still shows the scale with a selection — outside the verdict) → `BACKLOG.md` at the close as an operator option · F2 LOW (`selected: no dates` is the orchestrator's decision) → owed to the operator, §6 · F3 LOW (a docstring line overran) → fixed · F4 LOW (the no-selection arm's reachability unstated) → fixed in the docstring · re-dispatched after the fold (docstrings only; `views.py` diff unchanged): OK to advance, 20 passed on the two touched test files · re-dispatched again after the `V41` fold (PRES-R restored, re-capture as PRES-R2, three `_frame` calls repointed): OK to advance, PRES-R→PRES-R2 differ in exactly the three rows, no assertion weakened, 5 passed |

## 5 · Risks

`selected task ▸` is fixed English text in a 20-cell label at 80 columns (15 cells used); a future rename must still fit. The PNG of the export is Edge's render of the same SVG, so it inherits the SVG's text; it is not asserted separately.

## 6 · Pending items / spec deviations

- **Owed to the operator (approve or reject):** the selected-task-with-no-date label `selected: no dates` (dim) was not in the verdict; decided here and recorded in LED-.8 (review F2).
- After the review, the increment gate's `V41` blocked twice on increment 001's evidence rows (the PRES-R frames had been regenerated in place, so their bytes no longer matched 001's digests). The fix: PRES-R restored byte-for-byte from `8303045`, the re-capture written as `PRES-R2-*` (same bytes as the in-place one), TC-1001/TC-1002/AT-1001 repointed by file name only; `tests/test_present.py` re-run 5 passed and `gen_frames.py` HOLDS (delta D3 only). The reviewer re-read this fold (§4b).
- The full suite (`suite-004.txt`) ran before the review fold; the fold touched two test docstrings only, and the two files were re-run green (20 passed) by the reviewer.
- `prototypes/present_rulers/` still shows ` — hybrid` and the keys row: it is the frozen, approved prototype, not shipped code.
- The operator's visual verdict on the 80-column oracle frame stays ⏸ DEFER (`BACKLOG.md`).

## 7 · Suggested next task

The DDR (`stations/p4-validation.md` §DDR), then P4 and the P5 close.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_room.py`, `tests/test_present_hide.py` |
| 3 | Layer 0 where it applies | ✓ | TC-1608 covers the label's three branches |
| 4 | RED counterfactual | ✓ | §4, `red-004.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen; no signature changed |
| 9 | Coverage verified on disk | ✓ | `suite-004.txt` |
| 10 | Load-bearing emptiness | ✓ | TC-1608 (a)'s absence claims carry positive controls on the same SVG |
| 11 | Mutation verdicts | ✓ | §4: 7/7 KILLED |
| 12 | Instrument RED-proof | ✓ | none new, declared |
| 13 | Correction population | ✓ | §4 |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4 |

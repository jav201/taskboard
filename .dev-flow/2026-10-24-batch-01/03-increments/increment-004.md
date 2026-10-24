# Increment 004 — HLR-2607, HLR-2608 · `the legend strip, hide, /#cls`

| Field | Value |
|---|---|
| Batch | `2026-10-24-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2607` / `LLR-2607.1`, `LLR-2607.2` · `HLR-2608` / `LLR-2608.1`, `LLR-2608.2` |
| Acceptance | `AT-2605` minted here · `AT-2606` minted here — white-box `TC-2607` (×8), `TC-2608` (×6) |
| Agent | `software-dev` (spawned coder) |
| Date | `2026-10-24` |

## 1 · What changed

The gantt gained the legend strip under its ruler and the presentation gained it under both per-project views' rulers, with the exports carrying it: only the classes drawn in the frame (shape in colour + name, then `N hidden`), nothing when no classed milestone is in view, cut from the right at 80 cells. `_hide` (the shallow `copy.copy` proxy, the PDR's Q3) is applied at `_gantt_frame`'s entry — hidden classes leave the cells, the title markers and the fold counts while the board object stays untouched (a save writes what it held). `present_tasks_m` wraps `present_tasks` and is consumed by `render_present`, view 3's `_all_plan`, the presentation screen's `_shown_ids` (app.py:392) and therefore both export writers. The gantt's spare-row details line (`_gantt_legend`) gained the class entries beside the kept `◆ milestone` entry — the round's `◆` part has exactly one home (delta A8, no double-drawn `◆`); the painted-frame assertion at 118×30 AND 80×24 (the PDR's ux PC-1) confirms `_gantt_legend` as the operator-visible details-line seat — QA-3's hedge resolved by assertion, no ledger entry. `matches_m`/`filter_bar_m` are wired into the `matches`/`filter_bar` seats (prefix, lower-case class resolution mirroring `Directory.find` — ARCH-2; a `#cls` naming nothing keeps nothing; the bar reads `/ <shape> <Name> milestones of this class only`; the overlay lights no text for a class query). `?` (the gantt and kanban help + the gantt legend entries) names the classes, the `#` manager and the `/#cls` filter (UX-4); the README documents the directory, the encoding, the keys, the filter and the accepted costs. AT-2605 drives the whole chain by real keys at both sizes; AT-2606 drives the search.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2607.1/.2, LLR-2608.1/.2 | the strips, `_hide`/`_hidden_class_ids`/`present_tasks_m`, the search seats + overlay, `_gantt_legend`'s class entries, the help, the census `ALLOWED_LINES` extension (one new `◆` help line, per the census's own mechanism) |
| `taskboard/app.py` | source | LLR-2608.1 | the presentation's `_shown_ids` nav seat consumes `present_tasks_m` (+import) |
| `README.md` | doc | HLR-2607 | the "Milestone classes" prose + `marks.json`/`marks.json.corrupt` data-file rows |
| `tests/test_legend.py` | test | HLR-2607, HLR-2608 (TC-2607, TC-2608, AT-2605) | 12 nodes |
| `tests/test_milestone_marks.py` | test | HLR-2608 (TC-2608, AT-2606) | 4 nodes + the census extension |
| `tests/test_readme.py` | test | HLR-2607 | 2 nodes |
| `tests/test_markup_census.py` | test | the 003 amendment (LLR-2605.1/LLR-2606.3) | two EXEMPT rows: `MarksManager._paint`'s frame and the Select's options are Text-piece safe |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |

## 3 · How to test

`env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_legend.py tests/test_readme.py -k "AT_2605 or TC_2607 or readme"` (20 passed); `… tests/test_legend.py tests/test_milestone_marks.py -k "AT_2605 or AT_2606"` (2 passed); the close suites (`evidence/suite-004.txt`, 60 passed incl. the markup census); the touched batch (`evidence/suite-004b.txt`).

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | TC-2607 (×8), TC-2608 (×6) | 14 passed (`suite-004.txt`) |
| B | `test_AT_2605_hide_and_the_legend` (the whole chain by keys at 118×30 and 80×24: gantt, all three presentation views, both export paths, the painted details line, the unhide cycle) · `test_AT_2606_hash_pay_filters_to_that_class` | 2 passed (`suite-004.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/views.py` `_gantt_frame` — the hide application dropped (`if _hidden_class_ids(board): board = _hide(board)` → `if False:`) — made `test_AT_2605_hide_and_the_legend` fail (hidden classes still draw) · `evidence/mutation-004.txt` (arm 12) · restore digest `bf28e2a742b4b7505f6189e92472ee4e7d2002b3df6067561c4f05ed009b175b` |
| **Mutation verdicts** | 19 arms, one per new node: **19/19 KILLED · 0 SURVIVED · 0 CRASH/BAD** · every restore proven by hash · `evidence/mutation-004.txt` · arms that stayed GREEN: none (three first-round arms re-aimed before the final run — the presentation-carriage arm now drops the ruler's strip append, the overlay arm lights the class name, the readme arm drops the asserted hide sentence) |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | the presentation export's emitted form: AT-2605 asserts the SVG bytes carry the strip (the export path is exercised end-to-end, not only the painted frame) |
| **Reverse census** | 5 probes: B1 `grep -rl "legend_strip\|present_tasks\|filter_bar\|matches(" tests/` — the touched suites re-run (both transcripts: `suite-004.txt` 60 passed, `suite-004b.txt` 988 passed · 1 skipped — the environmental clipboard arm, pre-existing); B2 no file moved; B3 no golden capture; B4 the strips/exports consumed by the presentation export — AT-2605's SVG arms; A3 no other module — 0 foreign hits (`grep -rl "legend_strip_project\|present_tasks_m" tests/` → the new/touched suites only) |
| **Correction population** | one — the 003 amendment: `tests/test_markup_census.py`'s two EXEMPT rows (its gate missed the census suite; both seats are Text-piece safe). Folded in this increment (tests uncapped); recorded in §6. |
| **Frozen interfaces** | people.py, boards.file_lock/keep_aside, models.write_atomic/clean_strings untouched; the section-3 exclusion sites byte-identical (the census enforces it); `Board._to_dict` byte-preservation intact — verified in the diff the code-reviewer reads |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-004.txt | 4dc23405e79b9c89b5c0d5ddebce7089af8c911abc21b70d2e63cdb655f71f34 |
| suite-004b.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-004b.txt | 3f7bf808971b6b35a7fa154e80156a94032ff2fd56605bc09d6fdbbc4004fef6 |
| mutation-004.txt | .dev-flow/2026-10-24-batch-01/evidence/mutation-004.txt | 5379f63a10e03ed9935fcd59424e866d26fc599ac2f8537e5cdbcd9937ed557d |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · BLOCK-UNTIL: F1 → fixed and re-verified (F1: `_legend_row`'s lone over-long name branch crashed with IndexError — reachable at the gantt's MIN_WIDTH with manager-legal 60-char names; fixed exactly per the reviewer's prescription, the cut budget verified against the row-width invariant; one new test node `test_TC_2607_a_lone_over_long_name_is_cut_not_crashed` minted; the battery re-ran whole, 19/19 KILLED) · DISCHARGED by the same reviewer — OK to advance, 0 HIGH (F1 fixed and re-verified on the diff; the suites re-ran after the fix) |

## 5 · Risks

(1) The strips name classes of the board's non-archived milestones (the round's `classes_on`); under `focus` a class whose milestones are off-focus is still named — the round's own behaviour, not exercised by the suites. (2) A lone `#` filters to the first class in sorted order (round-faithful, asserted). (3) View 3 draws no strip (deviation 3 in §6). (4) The strip costs one body row whenever classes are drawn; the frame's own folding decides what gives way. (5) The strips and details line draw class shapes directly (not through `milestone_mark`) — they draw class identity, not milestone state, matching the round and `render_marks`. (6) The 003-owned markup-census RED was folded here (§6); nothing remains for P4.

## 6 · Pending items / spec deviations

AT-2605 and AT-2606 are minted here — all seven ATs now realise exactly one node each (C-18; the ATLAS is complete). The declared items: (1) the 003 amendment (two EXEMPT rows — folded, census green); (2) `filter_bar_m`'s `marks` parameter (sanctioned by the PDR §6 ruling — the seat has no board argument); (3) view 3 draws no strip (the LLR's prose says "per project in the all-boards presentation" but its thresholds and the round name only the gantt and split views + exports — reading kept, flagged); (4) the "band facts" wording (the kanban band rule keeps drawing hidden classes' milestones: HLR-2608's statement, MM-D6 and the manager frame scope the hide to gantt + presentation — round-faithful, flagged); (5) the lone-`#` ruling (asserted); (6) the QA-3 TC-2607 name sharing (each LLR's `-k` selector is file-scoped — no rename needed); (7) the details-line hedge resolved by painted-frame assertion at both sizes (no ledger). No silent spec edit.

## 7 · Suggested next task

The batch close: the DDR (design/validation review with the captures), the P4 full suite in three sequential chunks, the close record. The commissioned `m01-` captures of the gantt strip, the hide and the `/#pay` bar at 118×30 and 80×24 remain the visual confirmation.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | 19 new nodes (18 + the F1 arm) + the census amendment |
| 3 | Layer 0 where it applies | ✓ | §4 (the strip/fit unit arms) |
| 4 | RED counterfactual | ✓ | §4, `mutation-004.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ⏳ | §4b: PASS after FIX FIRST |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | §4 + the census |
| 9 | Coverage verified on disk | ✓ | `suite-004.txt`: 60 passed |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 18/18 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: the census amendment, named |
| 14 | Emitted-form assertion | ✓ | §4: the SVG export bytes |
| 15 | Independent review | ⏳ | §4b: PASS, F1 discharged |
| 16 | Evidence files | ✓ | §4: 3 digests |

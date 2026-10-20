# Increment 004 — LLR-2104.1, LLR-2105.1, LLR-2106.1 · `the screen and the picker`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-19-batch-01/03-increments/increment-004.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-19-batch-01` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2104`, `HLR-2105`, `HLR-2106` / `LLR-2104.1`, `LLR-2105.1`, `LLR-2106.1`; `LLR-2103.1` (the drawn stops, LED .4); `AT-2102`, `AT-2103` owed by 002/003 |
| Acceptance | `AT-2102`..`AT-2106` · white-box `TC-2103` (the overflow row, the rail's count), `TC-2104` ×3, `TC-2105` ×2, `TC-2106` (the picker) · unit: the hint's wording choice (Layer 0, TC-2104 over 165 widths × 3 counts) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-19` |

---

## 1 · What changed

`PresentScreen` gains its third view: `3`, and `tab`/`shift+tab` cycle 1 → 2 → 3 → 1. View 3 is painted and exported through `render_present_all`, routed inside `_frame_text` so the markup census's exempt key (`PresentScreen._paint` / `self._frame_text()`) stands (PC-3); it holds its own cursor (`("proj" | "task", id)`), the folded projects and the rail's focus, none persisted. Entering view 3 puts the cursor on the current project (on the rail from 100 columns, else on the views-1/2 task's row or its project's header, else the first drawn row); leaving it shows its cursor's project and task in views 1/2. `←/→` move the focus between rail and timeline (from 100 columns; else they move); `space` hides the cursor's task or project on the timeline (the cursor to the next row) and toggles a project in place on the rail; `a` shows every hidden project and task and notifies `Shown again: P project(s) + T task(s)` (`markup=False`); `shift+↑/↓` move the cursor's project in `present_order` (every project on the rail, the shown ones on the timeline) and renumber every visible project densely; `enter` folds or unfolds a project; `pgdn`/`pgup` do nothing in view 3, `enter`/`shift+↑/↓` nothing in views 1/2. `u` opens `modals.PresentHiddenPicker` (title, `○`/`●` rows as plain `Text` pieces, `space`/`enter` toggles and saves, `esc`/`q`/`u` close) in every view. `x` in view 3 writes the timeline without the rail to `present-board-<date>-all.svg/.png`. The hint names three views; view 3 has its own wordings (with and without the rail); the count reads ` · u N hidden` (` · N hidden` below 36 columns). In `views`: the stops no longer include a row the overflow row covers, and the rail counts every visible project's hidden tasks (code review F1, F3 of increment 003). README §Presentation rewritten for three views; `BACKLOG.md` gains this batch's lane.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-2104.1, LLR-2105.1, LLR-2106.1 | `PresentScreen`: bindings `3`, `←/→` → `side`, `shift+↑/↓`, `enter`, `u`; view 3's state, paint, keys, hint, export; imports |
| `taskboard/modals.py` | source | LLR-2106.1 | `PresentHiddenPicker` |
| `taskboard/views.py` | source | LLR-2103.1 (LED .4), HLR-2103 | `_all_timeline` trims the stops to drawn rows; `_all_rail` counts every visible project's hidden tasks |
| `tests/test_present_all.py` | test | HLR-2102, HLR-2103, HLR-2104, HLR-2105, HLR-2106, LLR-2103.1, LLR-2104.1, LLR-2105.1, LLR-2106.1 | AT-2102..AT-2106, TC-2104 ×3, TC-2105 ×2 (the curation; the resize, code review F1/F2), TC-2106 (the picker), TC-2103 ×2 (the overflow row, the rail's count) |
| `tests/test_present_narrow.py` | test | LLR-2104.1, LLR-1904.1 | law-driven: TC-1904's names and literal first widths, its overflow arm, AT-1904 |
| `tests/test_present_polish.py` | test | LLR-2104.1, HLR-2002 | law-driven: TC-2002's first widths and names; AT-2002 (the split view at 80, LED .2) |
| `tests/test_present_views_app.py` | test | LLR-2104.1, HLR-1803 | law-driven: TC-1808's five cells, AT-1803's three-view wrap |
| `tests/test_present_hide.py` | test | LLR-2104.1, HLR-1602 | law-driven: TC-1604's two cells and its count, AT-1602's `· u 1 hidden` |
| `tests/test_markup_census.py` | test | LLR-2104.1, LLR-2106.1 (PDR PC-3) | the `PresentScreen._paint` exempt key's reason text only (names `render_present_all`); the key unchanged |
| `README.md` | doc | HLR-2103..HLR-2106 | §Presentation: three views, the keys, what is saved |
| `.dev-flow/BACKLOG.md` | doc | — | this batch's lane |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 6 (uncapped) |
| Doc files | 2 (outside the count) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_all.py tests/test_present_narrow.py tests/test_present_polish.py tests/test_present_views_app.py tests/test_present_hide.py tests/test_markup_census.py`; the battery: `python .dev-flow/2026-10-19-batch-01/evidence/mutate.py 004` and `... 004-views`; the captures: `python .dev-flow/2026-10-19-batch-01/evidence/capture.py <out> v3-160 v3-118 v3-80 seq`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A | `tests/test_present_all.py::test_TC_2104_*` ×4, `::test_TC_2105_the_curation_writes_exactly_what_changed`, `::test_TC_2106_the_picker`, `::test_TC_2103_no_stop_hides_under_the_overflow_row`, `::test_TC_2103_the_rail_counts_every_hidden_task` | in the full suite (`suite-004.txt`) |
| B | `tests/test_present_all.py::test_AT_2102_*`, `::test_AT_2103_*`, `::test_AT_2104_*`, `::test_AT_2105_*`, `::test_AT_2106_*` | in the full suite (`suite-004.txt`) |
| law-driven | TC-1904 (+ overflow arm), AT-1904, TC-2002 ×8, AT-2002, TC-1808 ×5, AT-1803, TC-1604 ×2, AT-1602 | in the full suite (`suite-004.txt`); 21 failed on the new screen before the update (`lawdriven-before.txt`) — exactly the P-5 / LED .2 set |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean worktree at `fc55d3a` (004 with its review fixes) | 0 failed, 2818 passed, 0 skipped (`suite-004.txt`; 2805 nodes at increment 003 + the 13 this increment wrote; the clipboard roundtrip passed this run) |

| Field | Value |
|---|---|
| **RED counterfactual** | the test file and the fixture copied into a scratch worktree at `base_ref` `bdf6e9d`, source untouched: the screen's nodes RED — 10 failed (`evidence/red-004.txt`); the overflow-row node RED on increment 003's `views.py` and GREEN with this increment's (checked by stash, and as mutant R1) |
| **Mutation verdicts** | 20 mutants (17 + the 3 of the review fixes, S1–S3 KILLED, `mutation-004-review.txt`), the selection pre-checked GREEN: Q1 `tab` modulo 2 · Q2 the tail without `u` · Q3 leaving view 3 keeps the old project · Q4 the export with the rail · Q5 `a` with nothing hidden saves · Q6 the reorder ranks the shown only · Q7 `enter` saves · Q8 the rail's `space` moves the cursor · Q9 the picker's toggle does not save · Q10 the picker's titles through a markup parser · Q11 `a`'s notice says nothing · Q12 `u` unbound · Q13 view 3's middle wording dropped · Q14 no rail focus on entry · Q15 `space` on a header hides nothing — 15 KILLED (`mutation-004.txt`); R1 the stops keep cut rows · R2 the rail's count over shown projects only — 2 KILLED (`mutation-004-views.txt`; R2 SURVIVED its first run, the rail-count node was added and it was re-run) · arms that stayed GREEN: none · harness `evidence/mutate-004.py` |
| **Instrument RED-proof** | 3 instruments: `evidence/mutate.py` (packet 001); `evidence/hint_widths.py` — the first widths it prints are not the code's output (it measures the literal strings with `rich.cells.cell_len`; the tables fail against the shipped two-view screen, `red-004.txt`'s TC-2104 rows); `evidence/capture.py` — on `base_ref` its `view1` scenario painted the milestone bar (`captures/view1-118x31-before.svg`) |
| **Emitted-form assertion** | 3 artifacts: the frame and hint as Textual holds them; the picker's `#picker-rows` `Text`; the exported `-all` SVG read from disk (AT-2104) |
| **Reverse census** | 5 probes: B1 `grep -rl "_hint\|present-hint\|1 gantt\|PRESENT_VIEWS\|tab" tests/test_present*.py` → the six files above, each updated or green; `grep -rn "PRESENT_VIEWS\[" taskboard/` → none left (every screen site indexes `PRESENT_SCREEN_VIEWS`, A-11) · B2 no file moved · B3 the PRES-V3/V4 frame tests read `render_present`, untouched here — green · B4 the `-all` export, read by AT-2104 · A3 `app` → `modals`, `views`, `models`; `modals` → `views`, `models` — allowed — 0 foreign hits |
| **Correction population** | 1 correction: the shipped assertions of the two-view hint and wrap — re-enumerated by running them on the new screen before editing (21 failed, `lawdriven-before.txt`), each updated old → new with its new value from `hint-widths.txt`: TC-1904 THRESHOLDS (gantt 0: 36/58/73/84 → 36/64/80/91, …), TC-2002 MIDDLE_FIRST ((73, 84) → (80, 91), …), TC-1808's cells (100 split: long → middle; 99/96 split hidden: middle → short; 80 split: middle → short, hidden: short → compact), TC-1604 (`· 2 hidden` → `· u 2 hidden`), AT-1602 (`· 1 hidden` → `· u 1 hidden`), AT-1904 (50: `⇥ ←→ ␣ x esc · 3 hidden` → with `3 all` and `u`; the split view at 50: compact → `esc`), AT-2002 (the split view at 80: middle → short, with a count → compact — HLR-2002 superseded in part, LED .2), AT-1803 (`tab` from view 2 reaches view 3) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-19-batch-01/evidence/suite-004.txt | 249944771ae02fbfdcf76a3c827a4377427f193a6756141f0090454078b6b3ff |
| red-004.txt | .dev-flow/2026-10-19-batch-01/evidence/red-004.txt | b1219f1baf8151bcbec8853170714c2f911b456d6ead1e511af0413cb26a782e |
| red-004-review.txt | .dev-flow/2026-10-19-batch-01/evidence/red-004-review.txt | c3e2b792df04303d7e235cb4372de1a1ec2fd7bff82937915e212e611db9bb92 |
| mutation-004.txt | .dev-flow/2026-10-19-batch-01/evidence/mutation-004.txt | 70226c540a05674c0d9301c7a0901e5afbb1c6a78b727921e835d8cd678ba879 |
| mutation-004-views.txt | .dev-flow/2026-10-19-batch-01/evidence/mutation-004-views.txt | 2c457821f55baf0abb3e2986b810701d21fd4e11dfd4112d703498909e42dfc0 |
| mutation-004-review.txt | .dev-flow/2026-10-19-batch-01/evidence/mutation-004-review.txt | 55615dc90ecfcdbc9029bbe1f933a7413dbffe14e09fea7d03d56d7d7b31c81f |
| mutate-004.py | .dev-flow/2026-10-19-batch-01/evidence/mutate-004.py | 15953563c530cc0db0d36c05fc7637ab1a58908e9213b86abbff81da89295e38 |
| hint-widths.txt | .dev-flow/2026-10-19-batch-01/evidence/hint-widths.txt | 316c0542d2140e8824e2636b0d0df90f41deaa039dae88e93b1f48a3b497c75c |
| hint_widths.py | .dev-flow/2026-10-19-batch-01/evidence/hint_widths.py | 82d7c25cfea14b2b5528e8a7339ee29656f535623dad74c0ea2d58d9403d1089 |
| lawdriven-before.txt | .dev-flow/2026-10-19-batch-01/evidence/lawdriven-before.txt | 53b6e12479e1f39f186bf08cddaac954b74f3dcd71a89f76b91d283b45d4f28e |
| capture.py (the version that ran at increment 004; increment 006 changed one step) | .dev-flow/2026-10-19-batch-01/evidence/capture-004.py | 7619e3fcc6988265d404c2e3893adb8585cd54e10801b545e7330d4113e78187 |
| view3-160x45.svg | .dev-flow/2026-10-19-batch-01/evidence/captures/view3-160x45.svg | da80142a95b987d5b2c5d8964a7817337df862c22539c913e2cc8968d168ea7e |
| seq-160x45-export-present-board-2026-10-19-all.svg | .dev-flow/2026-10-19-batch-01/evidence/captures/seq-160x45-export-present-board-2026-10-19-all.svg | 00f40aa5dd3fe554b58765ba72edec629f968b1fa4c18258348e932fb102dfc9 |

| Field | Value |
|---|---|
| **Evidence files** | 13 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK after one fix round: at `6d9f344` BLOCK-UNTIL F1 HIGH (`space` on the rail crashed after a resize across 100 columns: a task cursor looked up as a project) + F2 LOW (a trip below 36 columns dropped view 3's cursor) + F3 MEDIUM (the overflow trim repeated the layout's row arithmetic) + F4 LOW (a double lookup, a comment); all four fixed in `fc55d3a`, the resize node RED on `6d9f344` (`red-004-review.txt`), S1–S3 KILLED (`mutation-004-review.txt`); re-verdict OK, one LOW note open (the painter still places rows itself) |

## 5 · Risks

The picker covers the presentation (a modal over a modal: the frame is not seen behind it, `captures/seq-160x45-4-picker.svg`); below ~14 rows view 3's projects past the overflow row are reachable only from the rail; `shift+arrow` may not pass some terminals (UX-8).

## 6 · Pending items / spec deviations

The `?` help is unchanged (D8 deviation, `BACKLOG.md`); the split view's 80-column hint is the short one (LED .2, `BACKLOG.md`).

## 7 · Suggested next task

The DDR, then Phase 4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | `tests/test_present_all.py` and the law-driven files |
| 3 | Layer 0 where it applies | ✓ | TC-2104's wording sweep |
| 4 | RED counterfactual | ✓ | §4, `red-004.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen; the census key unchanged (PC-3) |
| 9 | Coverage verified on disk | ✓ | `suite-004.txt` |
| 10 | Load-bearing emptiness | ✓ | `grep "PRESENT_VIEWS\["` → none, quoted |
| 11 | Mutation verdicts | ✓ | §4: 20/20 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 1 correction, re-enumerated by command |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

# Increment 001 — LLR-1801.1, LLR-1801.2, LLR-1801.3, LLR-1802.1 · `the split view and the note wrapper (renderer)`

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
> `.dev-flow/2026-10-18-batch-01/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1801` / `LLR-1801.1`, `LLR-1801.2` · `HLR-1802` / `LLR-1802.1` · `HLR-1803` / `LLR-1801.3`, `LLR-1803.3` (the `present_paths` half; its screen half is increment 002's) · the repointed `LLR-1001.1` oracle (LED-2026-10-18-batch-01.1) |
| Acceptance | `AT-1001` (repointed) · white-box `TC-1801`..`TC-1807`, `TC-1001`, `TC-1002` · unit `TC-1801` (`present_note_lines`, 5 branches), `TC-1802` (`present_alloc`, cyclomatic 9) — AT-1801..AT-1803 drive the screen and land with increment 002 |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

`render_present` gains `view` (`PRESENT_VIEWS = ("gantt", "split")`) and `scroll`, and the header names the view in one dim word. The split view is the prototype's D2 · stacked, ported faithfully into `taskboard/views.py`: the gantt rows on top, then a block per shown open task (heading + note) in two columns from 100 wide, the fair share (`present_alloc`) with every cut declared, `no notes` for an empty note, nothing under the rule with every task hidden. One note wrapper (`present_note_lines`) keeps line breaks, bullets and numbered items for both views, so the gantt view's cursor note no longer flattens a plan into one line (`_present_note_lines` / `_present_note_row` deleted). `scroll` is a page: the cut cursor note pages (`_present_scrolled`, tiling with no gap), and when no cursor note can scroll each cut column pages its whole text; at page 0 an overflowing column keeps the cursor's block in view (`_present_window`), and the whole-text paging starts where page 0 was, so a page never moves the text back. `present_paths` gains `view` (`-split` file names). The eight PRES-V3 oracle frames are written in this batch's evidence and cross-checked row for row against the prototype's own renderer; TC-1001 / TC-1002 / AT-1001 are repointed to them. The prototype round behind the operator's verdict is committed (sources, SVGs, page; the PNGs, regenerable and embedded in the page, are locally excluded).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-1801.1, LLR-1801.2, LLR-1801.3, LLR-1802.1, LLR-1803.3 | `PRESENT_VIEWS`; `present_note_lines`, `_present_note_markup`, `_present_cut`, `_present_scrolled`, `_present_window`, `present_alloc`, `_present_heading`, `_PresentColumn`, `_present_column`, `_present_stack`; `render_present(..., view, scroll)` (the view word, the split branch, the gantt note rows); `present_paths(..., view)`; `_present_note_lines` and `_present_note_row` deleted |
| `tests/test_present_views.py` | test | HLR-1801, HLR-1802, HLR-1803, LLR-1801.1, LLR-1801.2, LLR-1801.3, LLR-1802.1 | new: TC-1801..TC-1807 (48 nodes with the parametrised cases) |
| `tests/present_notes_board.py` | fixture | HLR-1801, HLR-1802, HLR-1803 | new: the PRES-C board with the prototype round's notes, links and images (synthetic; `username_subject` the placeholder) |
| `tests/test_present.py` | test | LLR-1001.1 (repointed by HLR-1802) | `FRAMES` → this batch's `PRES-V3-gantt-*`; docstrings; assertions unchanged |
| `.dev-flow/2026-10-18-batch-01/evidence/gen_frames.py` | doc | HLR-1801, HLR-1802 | the oracle writer + the row-for-row cross-check against `views_d.py` (D1, D2 declared); batch record, not shipped |
| `.dev-flow/2026-10-18-batch-01/evidence/mutate.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the mutation harness (001: M1..M19; 002: N1..N11); batch record |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-118x30.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-80x24.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-notes-118x30.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-notes-80x24.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-118x30.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-80x24.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-long-118x30.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-long-80x24.txt` | generated | HLR-1801, HLR-1802 / TC-1803, TC-1807, TC-1001, TC-1002, AT-1001 | the oracle frame, written by `gen_frames.py --write` |
| `prototypes/present_views/app_capture.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/app_capture2.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/build_html.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/fixture.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-A-gantt.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-B-cards-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-B-cards-moved.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-B-cards.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-C-slide-empty.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-C-slide-moved.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-C-slide.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-D-split-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-D-split.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/118-tab-cycle.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-A-gantt.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-B-cards-moved.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-B-cards.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-C-slide-long-pgdn.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-C-slide-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-C-slide.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-D-split-long-pgdn.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-D-split-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/80-D-split.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-A-gantt.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D2-stacked-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D2-stacked-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D2-stacked-pgdn.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D2-stacked.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D3-columns-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D3-columns-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D3-columns.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D4-inline-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D4-inline-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-118-D4-inline.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-A-gantt.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D2-stacked-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D2-stacked.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D3-columns-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D3-columns.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D4-inline-hidden.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D4-inline-long.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/out/r2-80-D4-inline.svg` | generated | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/present-views-prototype.html` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/views_d.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |
| `prototypes/present_views/views_proto.py` | doc | HLR-1801, HLR-1802, HLR-1803 | the prototype round (not modified) behind the operator's verdicts of 2026-10-17/18; committed unmodified |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_views.py tests/test_present.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the oracle and its cross-check: `python .dev-flow/2026-10-18-batch-01/evidence/gen_frames.py`; the battery: `python .dev-flow/2026-10-18-batch-01/evidence/mutate.py <a scratch copy of the tree> 001`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 and A | `tests/test_present_views.py` TC-1801..TC-1807 (48 nodes); `tests/test_present.py` TC-1001, TC-1002 | in the full suite (`suite-001.txt`) |
| B | `tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle` (repointed) | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider` in a git worktree at `9810be6` holding this increment's files | 2 failed, 2709 passed (`suite-001.txt`); the 2 failures are the pre-existing standup tests of `tests/test_team_views.py` (`suite-base.txt`), not this increment's |

| Field | Value |
|---|---|
| **RED counterfactual** | every new and repointed renderer node run against `taskboard/views.py` at `base_ref` `6ddea9f` (a `git archive` export with this increment's test files and frames copied in): 51 failed, 0 passed — `present_note_lines` / `present_alloc` absent, `render_present` takes no `view`, the gantt note flattened, no view word · `.dev-flow/2026-10-18-batch-01/evidence/red-001.txt` · restore digest `460cf8128c618972607fc12778412143d606b7ed9edbd95b104ba2b6bcf0d178` (the batch tree's `views.py`, untouched: the RED ran on the base export, which was never mutated) |
| **Mutation verdicts** | 20 mutants on `taskboard/views.py`, 30 arms, all KILLED: M1 line breaks dropped (TC-1801, TC-1807, TC-1803) · M2 dash kept (TC-1801, TC-1803) · M3 one digit (TC-1801) · M4 `>= 100` → `> 100` (TC-1804[100-30]) · M5 the cursor's half dropped (TC-1802 room-6 row, TC-1803 long 80) · M6 cut mark removed (TC-1803, TC-1807, TC-1804) · M7 `no notes` removed (TC-1804, TC-1803) · M8 note escape dropped (TC-1805) · M9 note paging ignored (TC-1806) · M10 area branch removed (TC-1806) · M11 page 1 skips the top (TC-1806) · M12 4 gantt rows (TC-1807) · M13 view word dropped (TC-1807, TC-1001) · M14 a page jumps rows (TC-1806 ×2) · M15 the cursor loses its below-floor row (TC-1802) · M16 one-row cut unit dropped (TC-1803) · M17 all-hidden columns painted (TC-1804) · M18 page 0 hides the cursor's block (TC-1804 ×2) · M19 the first page down jumps back (TC-1806) · M20 wide glyphs wrapped by code points (TC-1801) · arms that stayed GREEN: none · `.dev-flow/2026-10-18-batch-01/evidence/mutation-001.txt` · restore digest `460cf8128c618972607fc12778412143d606b7ed9edbd95b104ba2b6bcf0d178` |
| **Instrument RED-proof** | 2 instruments: `gen_frames.py` (its first run, before `--write`, FAILED on all 8 frames — `gen-frames-001.txt`); `mutate.py` (asserts its arm count and that each edit applied; the qa-reviewer's own PDR run of it reported 2 SURVIVED arms for M5, which led to the room-6 row — a failure it can report) |
| **Emitted-form assertion** | 2 artifacts: the oracle frames are asserted as the renderer EMITS them (`Text.plain` rows, `_frame` reads the file); the export's SVG is asserted in increment 002 (AT-1803, `&#160;` unescaped) |
| **Reverse census** | 5 probes: B1 `grep -rl` for `render_present`, `present_paths`, `_present_note_lines`, `_present_note_row`, `PRES-R2` over `tests/ taskboard/ prototypes/` → `test_present.py` (repointed), `test_present_room.py`, `test_present_rulers.py`, `test_tick_label.py` (call `render_present` with six arguments: the defaults keep the gantt view; their frames read the ruler and field rows, not the header word — green in `suite-001.txt`), `test_markup_census.py` (the `_paint` seat, unchanged in this increment), `prototypes/present_rulers/*`, `prototypes/present_views/views_proto.py` (import the deleted helpers: frozen evidence, ARCHITECTURE §3; `gen_frames.py` binds them) · B2 no file moved · B3 `ls tests/goldens` → none; the PRES-V3 frames are new files, PRES-R / PRES-R2 untouched · B4 the export's default name unchanged for `gantt` (AT-1001's `x` arm green) · A3 `render_present`'s new arguments default to the shipped view — 0 foreign hits left un-revalidated |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-18-batch-01/evidence/suite-001.txt | ab2300906c550a877be2d6c4e1a528e0642899ba45819f7676b99f2aa0b334f7 |
| suite-base.txt | .dev-flow/2026-10-18-batch-01/evidence/suite-base.txt | b059e46948fcebb26e7a9f2bab93cf54ce38cedaaa530293861df0098914ddd0 |
| red-001.txt | .dev-flow/2026-10-18-batch-01/evidence/red-001.txt | 74deca7a29aa35bd6b44c1963601e6029ff6885beeda5dcc9570cd2e7e00e714 |
| mutation-001.txt | .dev-flow/2026-10-18-batch-01/evidence/mutation-001.txt | df555a4854ee47d4ef4cc091561fd3f4bc94e30565df650e0e2f0c9bcd4841c9 |
| gen-frames-001.txt | .dev-flow/2026-10-18-batch-01/evidence/gen-frames-001.txt | bc2f0bf9c2ef23af67c13cccd30ea455053beaae5e5e378cd981bc977b8b5efe |
| PRES-V3-gantt-118x30.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-118x30.txt | c7a9a076728acb8eb63f0585a34c4deef15bca659b47a1878e781dab38933cdc |
| PRES-V3-gantt-80x24.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-80x24.txt | 8ab8268f6a4ca5247bce3467a1e5d3c42df140f7d10771e2f6b524b0828095f6 |
| PRES-V3-gantt-notes-118x30.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-notes-118x30.txt | 6c337f9ca4a66783ad1e2c0b839173d342c6e97a51b8ac21524972412aee5b65 |
| PRES-V3-gantt-notes-80x24.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-gantt-notes-80x24.txt | 232edc9af0c7d85a6b98d42d1bb4e021f9e878e3f38d931d072f11f78057925a |
| PRES-V3-split-118x30.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-118x30.txt | b13bb7a2ba5486b111b681a79fccd50a06d2c2fa4becdf84327d6f89d2c91471 |
| PRES-V3-split-80x24.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-80x24.txt | d7441450afbefc7fd5d36c79b02e8e8e82a589cdcafea7d373fc671af5c1369f |
| PRES-V3-split-long-118x30.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-long-118x30.txt | e0e8f5c98a234e2454f2c3f1522581a478b7b42bf87cbd462283aeca18553326 |
| PRES-V3-split-long-80x24.txt | .dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-split-long-80x24.txt | f1aa7997c1316fc3352d20ae7a1d41716f4645814f55d27c20a04e832dbd8803 |

| Field | Value |
|---|---|
| **Evidence files** | `13 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 MEDIUM (`textwrap` counts code points: a CJK row 40 cells wide at w = 20, half of it hidden behind one `…`) → fixed: `_wrap_cells`, LED .6, TC-1801 wide arm, M20 KILLED · F2 LOW (two `mark` helpers) → fixed: `_present_mark` · F4 LOW (`view` unescaped in the header) → fixed: `escape(view)` · F3 LOW (the bar choice computed twice), F5 LOW (the one-row cut paints its lead `ink`, as the prototype does), F6 LOW (TC-1804's cut check calls the wrapper; the exact frames anchor it) → accepted · re-read on the re-frozen set (views.py 460cf812…): OK to advance |

## 5 · Risks

The oracle frames come from the shipped renderer; their independence rests on the row-for-row cross-check against the approved prototype's own renderer (`views_d.py`), equal at every row but the two declared D2 rows. The paging and the area scroll are the brief's and the reviewers' additions to the prototype; their frames at `scroll > 0` have no prototype to compare with — TC-1806's coverage arm and the captures of increment 002 stand in.

## 6 · Pending items / spec deviations

- Declared deltas from the prototype (`gen_frames.py`): D1 `N. ` items up to three digits; D2 a one-row cut reads ` … +N lines`, with no second `…`. Beyond the frames: paging by tiled pages (UX-1), the area scroll (the brief), the cursor's block kept in view at page 0 (QA2-1), no backward jump (PDR PC-U1), nothing under the rule with every task hidden (UX-5).
- `present_paths`' view suffix ships in this increment (one file); its test (TC-1809) and the screen's use land with increment 002.
- 2 pre-existing failures on `base_ref` (team standup), carried in `BACKLOG.md` since 2026-10-16-batch-01.
- Below ~36 columns `render_present` asserts on the gantt ruler's row width (`today Wed Sep 30` in a 20-cell label) — on `base_ref` too (probed at 20 and 30 columns on the base export); not this increment's code, carried to `BACKLOG.md` (code-review note).

## 7 · Suggested next task

Increment 002 — the screen (`taskboard/app.py`: the view keys, the page, the hint, the export of the current view), its tests, the README.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_views.py` (new), `tests/test_present.py` (repointed) |
| 3 | Layer 0 where it applies | ✓ | `present_note_lines`, `present_alloc`: TC-1801, TC-1802 |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: 0 HIGH; F1, F2, F4 fixed and re-read; F3, F5, F6 accepted |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | B3's absence (no goldens dir) is the only empty probe; positive control: the batch evidence frames ARE found and repointed |
| 11 | Mutation verdicts | ✓ | §4: 30/30 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: both instruments shown failing first |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |

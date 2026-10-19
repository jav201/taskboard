# Increment 003 — LLR-2003.1 · `the gantt note fills the free rows`

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
> `.dev-flow/2026-10-18-batch-03/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-03` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2003` / `LLR-2003.1` |
| Acceptance | `AT-2003` · white-box `TC-2003`, `TC-1807` (updated) · unit none — one expression, no boundary crossed |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

The gantt view's cursor note now uses the rows that were left empty under the brief list: `render_present` computes, before the brief loop, `room = max(3, height - len(lines) - len(open_t))` — the frame's height less the header, ruler, span, task and rule rows and one row per brief, never below the shipped 3 — and cuts the cursor's note to it (`_present_cut`, unchanged, still declaring `… +N lines`). At 80×25 the long note of the notes board shows 9 rows ending `… +5 lines` where it showed 3; at 118×31 its 11 rows show whole; where the frame has no free row the floor of 3 overflows exactly as shipped. Variant A of the round's item 3, the same arithmetic as its `cap_fork("fill")` on every frame (P-4). Surface: `R` → `#present-frame`, and the `x` export. The docstring of `render_present` and the module map's `tests` row say so.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2003.1 | `render_present`: `room` before the brief loop, the cursor's note cut to it; the docstring (the note, the PRES-V4 frames, the `reached` marks) |
| `tests/test_present_polish.py` | test | HLR-2003, LLR-2003.1 | new: TC-2003 ×4 (the long note equals PRES-V4 at both sizes; the sweep with the room-equals-note, one-short, one-free-row and overflow boundaries; no note without notes), AT-2003 |
| `tests/test_present_views.py` | test | LLR-2003.1, LLR-1802.1 | law-driven: TC-1807 reads the PRES-V4 gantt-notes frames; 11 / 9 note rows; the cut check at 80 only, none at 118; the line-break checks kept (qa-reviewer QA-7) |
| `tests/test_present_views_app.py` | test | LLR-2003.1, HLR-1802 | law-driven: AT-1802 reads the PRES-V4 gantt-notes frames (found by `suite-003-run1.txt`, below); its line-break checks kept |
| `docs/ARCHITECTURE.md` | doc | LLR-2003.1 | the `tests` row: the PRES-V4 frames read by the two test files (no longer "planned") |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 3 (uncapped) |
| Doc files | 1 (outside the count) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k 2003`; `python -m pytest -q -p no:cacheprovider tests/test_present_views.py tests/test_present.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the battery: `python .dev-flow/2026-10-18-batch-03/evidence/mutate.py 003` from the root of a scratch copy of the tree; the round comparison and the captures: `evidence/port_captures.py`, `evidence/explain_diff.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | `tests/test_present_polish.py::test_TC_2003_the_long_note_equals_the_rounds_frame[118-30]`, `[80-24]`, `::test_TC_2003_the_note_takes_every_free_row_and_declares_its_cut`, `::test_TC_2003_no_cursor_note_without_a_cursor_or_notes` (TC-2003); `tests/test_present_views.py::test_TC_1807_the_cursor_note_keeps_its_line_breaks` ×2 (updated) | in the full suite (`suite-003.txt`) |
| B | `tests/test_present_polish.py::test_AT_2003_the_gantt_note_runs_to_the_bottom_of_the_frame` (AT-2003) | in the full suite (`suite-003.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree with increments 001–003 | 0 failed, 2759 passed, 0 skipped (`suite-003.txt`, run 2; 2754 + the 5 new nodes). Run 1 (`suite-003-run1.txt`): 2 failed, 2757 passed — AT-1802 ×2 still read the PRES-V3 gantt-notes frames (the census had missed the site; §4 Correction population), re-pointed at PRES-V4 before run 2, with code-review F1/F2 folded |

| Field | Value |
|---|---|
| **RED counterfactual** | the test files copied into a scratch worktree at `base_ref` `620f58c` with the PRES-V4 frames beside them: TC-2003 ×3 and AT-2003 RED (4 failed, 1 passed — the no-notes arm, a regression pin: no note row without notes is true of the 3-row cap too), TC-1807 ×2 RED (2 failed, 46 passed in `tests/test_present_views.py`) · `.dev-flow/2026-10-18-batch-03/evidence/red-003.txt` · the battery's restore digests below |
| **Mutation verdicts** | 4 mutants, 11 arms, every node pre-checked GREEN on the unmutated copy: 11 KILLED — K1 the room stays 3 → TC-2003 [80-24], the sweep, AT-2003, TC-1807 [80], AT-1802 [80] · K2 the floor dropped (`max(0, …)`) → the sweep (its one-free-row heights, PDR) · K3 the briefs not subtracted → TC-2003 [80-24], the sweep, AT-2003 · K4 one row too many → TC-2003 [80-24] (PDR PC-3), the sweep; arms that stayed GREEN: none · `.dev-flow/2026-10-18-batch-03/evidence/mutation-003.txt` · `views.py` restored to `08e2d72d67db…` by digest after every arm |
| **Instrument RED-proof** | 3 instruments: `mutate.py` (10 arms RED; its pre-check, increment 001); `evidence/frames/gen_frames.py` — its frames differ from the shipped 3-row render at 80×24 and 118×30 (TC-1807 and TC-2003 RED on base, above), so they are not the base renderer's own output; `port_captures.py --compare` (increment 001) |
| **Emitted-form assertion** | 2 artifacts: the frame as `#present-frame` holds it (`content.plain`, AT-2003, against the round's PRES-V4 file) and the frame as the app exports it (`export_screenshot` SVG against the round's composed forks, `compare-003.txt`) |
| **Reverse census** | 5 probes: B1 `grep -rl "render_present" tests/` → `test_markup_census.py`, `test_present.py`, `test_present_narrow.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py` (TC-1807 updated), `test_present_views_app.py` (AT-1802 updated, after run 1 — see Correction population), `test_tick_label.py`, `test_present_polish.py` — the others render the gantt view with a note that fits 3 rows or at sizes without a cut note (TC-1001/1002: a 2-row note), green in `suite-003.txt` · B2 no file moved · B3 the PRES-V3 gantt-notes frames drift as planned and are no longer read (TC-1807 reads PRES-V4); the files stay byte-identical (`git diff --stat 620f58c -- .dev-flow/2026-10-18-batch-01` empty) · B4 the `x` export writes the filled frame (`compare-003.txt`) · A3 `render_present`'s signature and frame shape unchanged; `_present_cut` unchanged |
| **Correction population** | 1 correction: the shipped assertions that the gantt note is 3 rows (the PRES-V3 gantt-notes frames) · ⚠ the population was first taken from the P2 census (TC-1807 alone) and NOT re-enumerated by command before the first edit: `suite-003-run1.txt` failed AT-1802 ×2 on the old frames. Then enumerated: `grep -rn "len(notes) == 3\|PRES-V3-gantt-notes" tests/` → `tests/test_present_views.py` (TC-1807) and `tests/test_present_views_app.py:154-155` (AT-1802) · both sites edited, none left; AT-1802 RED on base against PRES-V4 (`red-003.txt`, addendum), K1 kills it (`mutation-003.txt`) |

**The round comparison** (`compare-003.txt`, the final one): the real app's captures of five scenes at 118×31 and 80×25 against the round's three A forks composed, re-run on `base_ref` (`expected/upto-3/`): 9 EQUAL, 1 DIFFER — the gantt cut row's `· ` lead at 80×25, the deviation declared in increment 001 (`explain_diff.py` at the end of the transcript). **The captures** (`evidence/captures/`): the gantt and the split view, five scenes, as SVG at 118×31 and 80×25 and PNG at 118 (the app's own `export_screenshot` and `save_present_png`); read by eye against the round's A PNGs (`notecap-A-gantt-long-118x31`, `contrast-A-split-long-118x31`): the same frames.

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-18-batch-03/evidence/suite-003.txt | 826e29d2a890cffe202997936a1686de7c7f913255b2b004b01d95c842ed65a3 |
| suite-003-run1.txt | .dev-flow/2026-10-18-batch-03/evidence/suite-003-run1.txt | ec82697ec6fa4910d3d4f8e2b7499040783ecc9ef567ef14ca33c9e1812a53a9 |
| red-003.txt | .dev-flow/2026-10-18-batch-03/evidence/red-003.txt | fd67671d5485c28d8426cf57db03aaa7fa2f648aae0335cbc645f2700b8bb6cd |
| mutation-003.txt | .dev-flow/2026-10-18-batch-03/evidence/mutation-003.txt | b722270ad9aba91a399d4aa30e7724b5b762a97ff597bb709c5301950f7bf5a2 |
| compare-003.txt | .dev-flow/2026-10-18-batch-03/evidence/compare-003.txt | fe074a0ac4b034269be31366c93ccf9f204a7afe3cb4a606bfdbbba8aa47a2cf |
| gen_frames.py | .dev-flow/2026-10-18-batch-03/evidence/frames/gen_frames.py | 6a6e17c9ce2a23ab6ed393480e1f4cf312f3c147b364b9dc22ee801f3b05f9ef |
| PRES-V4-gantt-notes-118x30.txt | .dev-flow/2026-10-18-batch-03/evidence/frames/PRES-V4-gantt-notes-118x30.txt | 6753d6cf2db0d012ff251a8355c3815a5e7867c4da918e196eaa6060f6f42c70 |
| PRES-V4-gantt-notes-80x24.txt | .dev-flow/2026-10-18-batch-03/evidence/frames/PRES-V4-gantt-notes-80x24.txt | efe6741817e6ee1e98d989110f8b004ab696400ceacc45346bd9a954f333acee |
| mutate.py | .dev-flow/2026-10-18-batch-03/evidence/mutate.py | af990ec3a8739cc8af07bcc9c908a9519cd7b5fe094a8d2dbcacbb73c4a794d2 |
| explain_diff.py | .dev-flow/2026-10-18-batch-03/evidence/explain_diff.py | 11e9ea4679816e7428515e50cb5d3eef94b89a02eeb1e38062764c16d29535b4 |
| gantt-118x31.png | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-118x31.png | c9a67b470495a614d118126bed42e99faa485cf2a3ffb4e6d597505ee70de2be |
| gantt-118x31.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-118x31.svg | 0ec68409587f14c6afcb8b7c0115a07bfc1314bf4c88213fdb1b971104ec55ff |
| gantt-80x25.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-80x25.svg | fb7a18b9eb78634b92781fbbb4a7fea7da5b4d271f520e48d700dcf0e4cb6130 |
| gantt-hidden-118x31.png | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-hidden-118x31.png | e6f342f5c1dbc45b5a32705deb36e3d64ec2049c7c073f2dd379ff7b1a5f20c3 |
| gantt-hidden-118x31.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-hidden-118x31.svg | d9d741eef1d762846f983fee075dc84c4eb7f6483a2d618c3b418e6c3a9725dd |
| gantt-hidden-80x25.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-hidden-80x25.svg | dbe3fc0a519a21738b3eb5fd0705a3e551d8c2ae726235e62de4fe580106ad98 |
| gantt-long-118x31.png | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-long-118x31.png | 78cf7a72b5a658904e8177ca26a88970452bfe98c7ffee0a5584180eebe8c311 |
| gantt-long-118x31.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-long-118x31.svg | 8a269aea9e52155a1e85d982b6bf911e2ef12d2823b7191c0b29198e19a2d736 |
| gantt-long-80x25.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/gantt-long-80x25.svg | 01d5eb0afced33abe3f996a8ab957a577f0eefe13bcf4fe8621579becd0b6593 |
| split-118x31.png | .dev-flow/2026-10-18-batch-03/evidence/captures/split-118x31.png | cf55f4ae2e255623733c218ea6cd89f10dd21983beb1cb1e67780d01b711202b |
| split-118x31.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/split-118x31.svg | cba8ecd6c87195553a14a839bff9e6c9413d95bdc8e5954572a1246265154086 |
| split-80x25.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/split-80x25.svg | 4a2d94544fe0464ef1af0ebb6c1b1eef7b30abbb006567575050515f1be7feb2 |
| split-long-118x31.png | .dev-flow/2026-10-18-batch-03/evidence/captures/split-long-118x31.png | e5c800d4246661c73959a4dee31ce5fb7fd7581826f66c5ad0fbc4b5448bc135 |
| split-long-118x31.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/split-long-118x31.svg | d29c3c8978d620266dfcb707ba3bcca4c8da6a93fa3546f15a112fdadb1c4048 |
| split-long-80x25.svg | .dev-flow/2026-10-18-batch-03/evidence/captures/split-long-80x25.svg | 7087301780ccac2b0a4e10b67efd1d8d0ae85d9e81a769d16f1919ee953780fc |

| Field | Value |
|---|---|
| **Evidence files** | `25 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 LOW (the no-cursor case claimed by the test's name, not exercised) → fixed: the arm with every task hidden (no cursor) added · F2 LOW (the sweep's docstring omitted the `L + 1` heights) → fixed · `room` named instead of inline judged immaterial (the same expression and place) |

## 5 · Risks

With the fill, the gantt view can show more of the cursor's note than the split view, which shares the room among every note (ux-reviewer UX-1) — variant A as approved; recorded for the operator in `BACKLOG.md`.

## 6 · Pending items / spec deviations

- LLR-2003.1 writes the expression inside the `_present_cut` call; the code names it `room` before the loop, the same value (the LLR's "`lines` the rows painted before the brief list").

## 7 · Suggested next task

The DDR, then Phase 4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | §2: 5 new nodes, TC-1807 and AT-1802 updated |
| 3 | Layer 0 where it applies | ✓ | not due: one expression, cyclomatic 1, no boundary crossed |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-003.txt` |
| 10 | Load-bearing emptiness | ✓ | the no-notes arm asserts an absence: its positive control is TC-2003's sweep, where the same probe (`startswith("  · ")`) finds the note rows of every task with notes |
| 11 | Mutation verdicts | ✓ | §4: 11/11 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ⚠ | §4: enumerated late — after run 1 failed on the site the census missed; declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |

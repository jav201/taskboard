# Increment 001 — LLR-2001.1 · `the quiet marks in reached`

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
> `.dev-flow/2026-10-18-batch-03/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-03` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2001` / `LLR-2001.1` |
| Acceptance | `AT-2001` · white-box `TC-2001` · unit none — four literals, cyclomatic 1, no boundary crossed |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

On a projector the presentation's quiet marks now read: the header's view word (`gantt` / `split`), a note's cut mark `… +N lines` (and ` … +N lines` beside a one-row note) and a paged window's edge marks `↑ N lines above` / `↓ N more lines` are painted `reached` (`#7a828c`, 4.87:1 on `#0d1117`) instead of `dim` (`#5b6675`, 3.25:1) — variant A of the round's item 1. Four tone literals in `taskboard/views.py`: `render_present`'s view word, `_present_cut`'s two cut marks, `_present_mark`. Every other `dim` mark (the `· ` lead, `no notes`, the separators, `+N more rows not shown`, `no project to present`) is unchanged. Surface: `R` → `#present-frame`, and the `x` export of the same frame.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2001.1 | `"dim"` → `"reached"` at `_present_cut` (the one-row tag, the `… +N lines` row), `_present_mark` (and its docstring), `render_present`'s view word |
| `tests/test_present_polish.py` | test | HLR-2001, LLR-2001.1 | new: TC-2001 ×4 (the sweep, the one-row cut, `no project to present`, the contrast ordering), AT-2001 |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 0 |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_polish.py` and `python -m pytest -q -p no:cacheprovider tests/test_present.py tests/test_present_views.py tests/test_present_views_app.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the battery: `python .dev-flow/2026-10-18-batch-03/evidence/mutate.py 001` from the root of a scratch copy of the tree; the round comparison: `.dev-flow/2026-10-18-batch-03/evidence/port_captures.py` (its docstring).

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | `tests/test_present_polish.py::test_TC_2001_the_quiet_marks_are_reached_and_the_rest_stays_dim`, `::test_TC_2001_a_one_row_cut_is_reached`, `::test_TC_2001_no_project_to_present_stays_dim`, `::test_TC_2001_reached_reads_on_a_projector_and_stays_below_the_text` (TC-2001) | in the full suite (`suite-001.txt`) |
| B | `tests/test_present_polish.py::test_AT_2001_the_quiet_marks_read_in_the_running_app` (AT-2001) | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree with increment 001 | 1 failed, 2744 passed (`suite-001.txt`; 2740 + the 5 new nodes): the 1 is `tests/test_help_keys.py::test_AT_1603_the_help_shows_the_global_keys_without_scrolling[80x24]`, a HelpModal paint read after 3 pauses — the timing flake 2026-10-18-batch-02 carried; it fails 2 of 8 runs alone on `base_ref` and 1 of 5 on this tree (`flake-001.txt`); no file of this increment reaches the help modal; hardened in increment 002 (the commission's 0-failure target). After the suite, comment-only folds of code-review F1 (`views.py:64`) and F2 (a test comment): `tests/test_present_polish.py` re-run, 5 passed |

| Field | Value |
|---|---|
| **RED counterfactual** | `tests/test_present_polish.py` copied into a scratch worktree at `base_ref` `620f58c`: 3 failed, 2 passed — the sweep (`↓ 9 more lines` `#5b6675` at 36×12 split), the one-row cut (`. … +4 lines` `#5b6675`) and AT-2001 (the view word `#5b6675`) RED; `test_TC_2001_no_project_to_present_stays_dim` and `test_TC_2001_reached_reads_on_a_projector_and_stays_below_the_text` pass on base — a regression pin (out-of-scope line stays `dim`) and the why (the colour arithmetic, true of the palette on both sides) · `.dev-flow/2026-10-18-batch-03/evidence/red-001.txt` · the RED ran on the scratch worktree; the battery's restore digests below |
| **Mutation verdicts** | 6 mutants, 10 arms, every node pre-checked GREEN on the unmutated copy (PDR PC-2): 10 KILLED — M1 the view word `dim` → the sweep, AT-2001 · M2 the one-row tag `dim` → the one-row cut node · M3 the cut row `dim` → the sweep, AT-2001 · M4 `_present_mark` `dim` → the sweep, AT-2001 (after `pgdn`, PDR PC-1) · M5 the note lead `reached` → the sweep, AT-2001 · M6 `no notes` `reached` → the sweep; arms that stayed GREEN: none · `.dev-flow/2026-10-18-batch-03/evidence/mutation-001.txt` · each file restored to `c31cd96d022a…` (views.py) by digest after every arm |
| **Instrument RED-proof** | 2 instruments: `evidence/mutate.py` — 10 arms RED on planted mutants (above), its pre-check refuses a node already red (PDR PC-2); `evidence/port_captures.py --compare` — reported `DIFFER` ×4 on the port's captures (`compare-001.txt`) before any `EQUAL` was believed, and `EQUAL` ×14 on the round's own re-run (`expected/compare-round.txt`) |
| **Emitted-form assertion** | 2 artifacts: the frame as `#present-frame` holds it (its `Text` spans, AT-2001) and the frame as the app exports it (`export_screenshot` SVG, `compare-001.txt`: the port's SVGs against the round's) |
| **Reverse census** | 5 probes: B1 `grep -rl "render_present\|lines above\|more lines" tests/` → `test_markup_census.py`, `test_present.py`, `test_present_narrow.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py`, `test_present_views_app.py`, `test_tick_label.py`, `test_row_cost.py` — none asserts the marks' tone (plain text or other tones); 101 passed across the presentation files before the full suite · B2 no file moved · B3 no goldens; the PRES-V3 frames are plain text, unchanged (TC-1001/1002 green) · B4 the `x` export writes the same frame: its SVG carries `#7a828c` for the marks (`compare-001.txt`) · A3 `_present_cut`, `_present_mark` have no caller outside `views` but the frozen round (`grep -rn "_present_cut\|_present_mark" --include=*.py . ` → `taskboard/views.py`, `prototypes/backlog_polish/capture.py`) — 0 foreign hits re-validated |
| **Correction population** | none — no correction |

**The round comparison** (`compare-001.txt`): the real app's captures of five scenes at 118×31 and 80×25 against the round's own contrast-A fork re-run on `base_ref` (`expected/upto-1.txt`): 6 EQUAL, 4 DIFFER. Each DIFFER is one run on the gantt view's cut row: the round paints `· … +N lines` as one `#7a828c` run, the port paints the `· ` lead `#5b6675` and the mark `#7a828c`. Cause: on base the lead and the cut row are adjacent `dim` runs that `collapse_runs` merges into one span, and the fork repaints every `dim` span its pattern finds in — so it repainted the lead with the mark. The round's page says the rest of `dim` stays; HLR-2001 (P2-approved) keeps the lead `dim` on every row. **Declared deviation** (§6).

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-18-batch-03/evidence/suite-001.txt | c76c97ff9a87306da3b19ccae44306a4f6b8495aa7e7de011673c87280922828 |
| flake-001.txt | .dev-flow/2026-10-18-batch-03/evidence/flake-001.txt | 4a6864dc230bae20812ef8fcab65908a7bad1469b020985b6537e175e490d5ac |
| red-001.txt | .dev-flow/2026-10-18-batch-03/evidence/red-001.txt | a71274e7d08b1501d7819079a6b5b4dd69b54eb09b44007a4e4a21a7a2617bef |
| mutation-001.txt | .dev-flow/2026-10-18-batch-03/evidence/mutation-001.txt | 6c56e27df79a20499b739db141c870eeffddac2a037585538833b65950693df0 |
| compare-001.txt | .dev-flow/2026-10-18-batch-03/evidence/compare-001.txt | c4e00cc7896ce3a11b2b7747ddf608d791ab2585121a0548a7076586658dbcf2 |
| mutate.py | .dev-flow/2026-10-18-batch-03/evidence/mutate.py | 22499429ec513dcc326b0d1bf5c9ca836076d6d110181cde1470ffa5ffe95908 |
| port_captures.py | .dev-flow/2026-10-18-batch-03/evidence/port_captures.py | 73f49fbfe1c68d58be0d0a54131861d05fd0dd1678e158f25a569fa7179bf463 |

| Field | Value |
|---|---|
| **Evidence files** | `7 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 LOW (the `reached` token's comment names only milestones) → fixed (`views.py:64`) · F2 LOW (the view-word guard stands in for `header()`'s rule) → fixed: a comment stating it is that rule read off the row · the compare-001 deviation judged right (HLR-2001 keeps the lead `dim`; the round's repaint came from `collapse_runs`) |

## 5 · Risks

The tone is the operator's approved A; on a real projector it was not measured (contrast computed only). The view word in a header too wide for its row is painted whole in bold `bright` as shipped (HLR-2001's clause).

## 6 · Pending items / spec deviations

- Deviation (declared): the gantt cut row's `· ` lead stays `dim`, where the round's capture painted it `reached` by a span-merge artefact of its fork (`compare-001.txt`). One glyph per frame; the operator may ask for it.

## 7 · Suggested next task

Increment 002 — the middle hint wording (HLR-2002).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_polish.py` (new, 5 nodes) |
| 3 | Layer 0 where it applies | ✓ | not due: four literals, cyclomatic 1, no boundary crossed |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence: the sweep asserts the marks it meets and a seen-set requires every kind (view word, cut, `↑`, `↓`, lead, `no notes`, overflow) |
| 11 | Mutation verdicts | ✓ | §4: 10/10 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |

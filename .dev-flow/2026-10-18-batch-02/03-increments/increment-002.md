# Increment 002 — LLR-1903.1, LLR-1904.1 · `the presentation at any width`

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
> `.dev-flow/2026-10-18-batch-02/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-02` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-1903` / `LLR-1903.1` · `HLR-1904` / `LLR-1904.1` |
| Acceptance | `AT-1903`, `AT-1904` · white-box `TC-1903` · unit `TC-1904` |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

The presentation no longer kills the app below 36 columns. `views.render_present`, when `width < PRESENT_MIN_WIDTH` (36 — the narrowest frame whose gantt field keeps a cell), returns one `mut` line, the longest rung of `PRESENT_NARROW` that fits (`widen to 36+ columns · esc leave`, `widen to 36+ columns`, `needs 36+ cols`, `36+ cols`, `36+`; cut with `…` below 3 columns; every row empty at width 0), then blank rows — before reading the project, the view, the cursor or the scroll. `PresentScreen` takes no key but `esc`/`q` there (`_narrow()` guards `move`, `view` — and so `cycle` —, `scroll`, `hide`, `show_all`), and `x` notifies `Widen the terminal to 36+ columns to export` instead of writing a file; widened again, the frame is the one before the narrowing (only the page resets, as every resize already did). The hint row tries four wordings longest first — long, short, a new compact `⇥ ←→ ␣ x esc` (`pgdn ⇥ ←→ ␣ x esc` in split), then the view switch with `esc` — and below 36 shows `esc leave` and the hidden count; whatever still does not fit is cut with `…` (`Text.truncate`), and it is empty when the row has no cell. The stale presentation section comment in `views.py` (PRES-C, "hybrid", PRES-R) and the TC-1001 banner in `tests/test_present.py` now name PRES-V3.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-1903.1 | `PRESENT_MIN_WIDTH`, `PRESENT_NARROW`; the narrow branch at the top of `render_present` and its docstring; the presentation section comment |
| `taskboard/app.py` | source | LLR-1903.1, LLR-1904.1 | imports `PRESENT_MIN_WIDTH`; `PresentScreen._narrow`; the guard in `action_move`, `action_view`, `action_scroll`, `action_hide`, `action_show_all`; the notice in `action_export`; `_hint`'s four wordings, narrow branch, zero-budget guard and truncation |
| `tests/test_present_narrow.py` | test | HLR-1903, HLR-1904, LLR-1903.1, LLR-1904.1 | new: TC-1903 (the sweep), TC-1904 ×3 (the threshold table, the bold span, the overflowing count), AT-1903, AT-1904 |
| `tests/test_present.py` | test | LLR-1903.1 | the TC-1001 banner comment (PRES-R → PRES-V3); no assertion changed |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py tests/test_present.py tests/test_present_views.py tests/test_present_views_app.py tests/test_present_hide.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the battery: `python .dev-flow/2026-10-18-batch-02/evidence/mutate.py 002` from the root of a scratch copy of the tree.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 | `tests/test_present_narrow.py::test_TC_1904_the_hint_takes_the_first_wording_that_fits`, `::test_TC_1904_the_current_view_is_bold_and_bright`, `::test_TC_1904_an_overflowing_count_is_cut_visibly` (TC-1904) | in the full suite (`suite-002.txt`) |
| A | `tests/test_present_narrow.py::test_TC_1903_every_width_renders_a_whole_frame` (TC-1903); the PRES-V3 frame nodes TC-1001/1002 unchanged | in the full suite (`suite-002.txt`) |
| B | `tests/test_present_narrow.py::test_AT_1903_narrowed_the_presentation_says_how_wide_and_waits` (AT-1903), `::test_AT_1904_the_hint_shortens_and_cuts_visibly` (AT-1904) | in the full suite (`suite-002.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --ignore=tests/test_backlog_polish_round.py` on the working tree with increments 001 and 002 | 0 failed, 2739 passed (`suite-002.txt`, run 2; 2733 + the 6 new nodes). Run 1 (`suite-002-run1.txt`): 1 failed, 2738 passed — `tests/test_help_keys.py::test_AT_1603_the_help_shows_the_global_keys_without_scrolling[118x30]`, a HelpModal paint read after 3 pauses; 5/5 green in isolation (`flake-002.txt`); no file of this increment reaches `modals.py` or `keymap.py`; carried to `BACKLOG.md` as a timing flake |

| Field | Value |
|---|---|
| **RED counterfactual** | `tests/test_present_narrow.py` on `base_ref` `9e82b10` (a `git archive` export, the file copied in): 5 failed, 1 passed — TC-1903 (`AssertionError: (36, 35, …)` from `_present_finish`), TC-1904 ×2, AT-1903, AT-1904 RED; `test_TC_1904_the_current_view_is_bold_and_bright` passes on base — a regression pin (the shipped hint already bolds the current view) · `.dev-flow/2026-10-18-batch-02/evidence/red-002.txt` · the RED ran on the export; the battery's restore digests below |
| **Mutation verdicts** | 15 mutants, 20 arms: 19 KILLED — N1 the floor at 35 → TC-1903, AT-1903 · N2 the floor at 37 → TC-1903 · N3 a rung dropped → TC-1903, AT-1903 · N4 the rung in `dim` → TC-1903 · N5 no compact wording → TC-1904, AT-1904 · N6 the narrow hint uncut → TC-1904, AT-1904 · N7 the wide hint uncut (PC-2) → TC-1904 (overflow) · N8 no zero-budget guard → TC-1904 · N9 the narrow hint keeps the names → TC-1904, AT-1904 · N10 `space`, N11 `a`, N12 the view keys, N13 the moves, N14 `x` acting when narrow → AT-1903 each; arms that stayed GREEN: N15 (`pgdn` acting when narrow) → AT-1903 SURVIVED, the declared regression pin: a narrow frame is the same at every page, so `action_scroll`'s same-frame check refuses the page anyway, and a resize resets it — no test can see this guard · `.dev-flow/2026-10-18-batch-02/evidence/mutation-002.txt` · restore digests printed per arm for `views.py` and `app.py` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate.py` — its first 002 run crashed on the runner's cp1252 decoding (`UnicodeDecodeError`, no verdict believed) and was fixed (`encoding="utf-8"`); its second run showed N12/N13 SURVIVED, which rewrote AT-1903's keys (LED .6) — the kept run is after both |
| **Emitted-form assertion** | 3 artifacts: the frame as `#present-frame` holds it (`content.plain`, AT-1903), the hint as `#present-hint` holds it, with its `Text` spans (AT-1904), and the notice as `app.notify` receives it (the house seam, `tests/test_app.py`); `render_present`'s `Text` spans read for the `mut` tone (TC-1903) |
| **Reverse census** | 5 probes: B1 `grep -rl "render_present\|present-hint\|PresentScreen\|_hint" tests/` → `test_markup_census.py`, `test_markup_sites.py`, `test_present.py`, `test_present_hide.py`, `test_present_room.py`, `test_present_rulers.py`, `test_present_views.py`, `test_present_views_app.py`, `test_report.py`, `test_tick_label.py` (all render at 36+ columns: unchanged; green in `suite-002.txt`), `test_gantt_polish.py`, `test_link_picker.py` (other screens' own `_hint`) · B2 no file moved · B3 no goldens; the PRES-V3 frames read at 118×30 / 80×24 unchanged (TC-1001/1002 green) · B4 `x` below 36 writes nothing (AT-1903: no `reports/`); at 36+ the export is unchanged (AT-1803 green) · A3 `render_present`'s domain and `PRESENT_MIN_WIDTH` in `docs/ARCHITECTURE.md` §4 — 0 foreign hits left un-revalidated |
| **Correction population** | none — no correction |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-18-batch-02/evidence/suite-002.txt | 4c3d60a4ee694e54b5d8ce07afe08811df239217e8a7bf8a601b14738e2692bd |
| suite-002-run1.txt | .dev-flow/2026-10-18-batch-02/evidence/suite-002-run1.txt | b5463fc3ed1d53f51104e93c73a2b6e29351127c32c9324529c37c00b73e7e6b |
| flake-002.txt | .dev-flow/2026-10-18-batch-02/evidence/flake-002.txt | 2b3348ab292567377bb333a415d6034ff8dc77ba0cf776d350edc9b309b1dc46 |
| red-002.txt | .dev-flow/2026-10-18-batch-02/evidence/red-002.txt | 29a2b6aa1dd82b7bc948aeaac5625b6bba1c9d3d4bfef301dcf4b988760e71ea |
| mutation-002.txt | .dev-flow/2026-10-18-batch-02/evidence/mutation-002.txt | 4a6753f8526bc7deed209262fffbbc2703c4bb6bf06fd8c17c0118dbb2a090df |
| mutate.py | .dev-flow/2026-10-18-batch-02/evidence/mutate.py | 4618053867a27d4654b7ede8198fa7b3cedcac74f7fb1f6a799a0dedc1b9e8d0 |

| Field | Value |
|---|---|
| **Evidence files** | `6 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 MEDIUM (TC-1903's sweep 20.6 s) → fixed: sampled above 36 (LED .7), 1.8 s · F2 LOW (the rungs repeat 36 by hand) → fixed: built from `PRESENT_MIN_WIDTH` · F3 LOW (`_narrow`'s docstring omitted `q`; `split` renamed `pg`) → fixed · re-read on the folded set: OK to advance (F1–F3 verified on the diff); the battery re-run on the folded set (`mutation-002.txt`) |

## 5 · Risks

The narrow rungs, the key guard, the export notice and the compact wording are UI the operator has not seen; they ship under the commission's FIX class and are shown in the round (increment 003) for review. Below 36 the presenter cannot hide or move — deliberate (ux-reviewer UX-7), and the hint says only `esc leave`.

## 6 · Pending items / spec deviations

- LED .6 (AT-1903's narrow keys), LED .7 (TC-1903 sampled above the floor; the rungs built from the constant).
- N15 declared a regression pin (§4).

## 7 · Suggested next task

Increment 003 — the polish prototype round.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | `tests/test_present_narrow.py` (new, 6 nodes) |
| 3 | Layer 0 where it applies | ✓ | `_hint` (cyclomatic 7): TC-1904; the narrow branch: TC-1903 |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt` |
| 10 | Load-bearing emptiness | ✓ | AT-1903's "no `reports/`" is an absence: its positive control is AT-1803, where `x` at 80 columns writes `reports/present-…svg` through the same `action_export` |
| 11 | Mutation verdicts | ✓ | §4: 19/20 KILLED, N15 declared |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |

# Increment 001 — LLR-2101.1 · `a milestone is a ◆ on its date`

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
> `.dev-flow/2026-10-19-batch-01/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-19-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2101` / `LLR-2101.1` |
| Acceptance | `AT-2101` · white-box `TC-2101` · unit none — one branch, no boundary crossed |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-19` |

---

## 1 · What changed

A milestone in the presentation (views 1 and 2) is now drawn the way the board's gantt draws it: `_present_task_row` gains a milestone branch that builds the field from the gantt's own `gantt_milestone_cells` (`◆` on the due and the date beside it, never a bar), puts `◆` in the milestone's tone before the title (the title keeps `label_w - 6` cells), accents the `◆` under the cursor (the field's echo) and gives the chip the due alone (`due <Mon D>`, `no dates` without one). Every other task row is drawn as shipped. On `base_ref` "Cut-over weekend" (no start, due in 6 days) was a 7-day bar from today (P-1); the round's board is copied into `tests/present_portfolio_board.py` (with the milestone offer's mark, so the startup offer never covers the app under test). The code reviewer's F1 (the cursor's `⟦` lead unasserted) and F2 (no late milestone in the sweep) are folded into TC-2101 before the commit.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2101.1 | `_present_task_row`: the milestone branch and a docstring |
| `tests/test_present_milestone.py` | test | HLR-2101, LLR-2101.1 | new: TC-2101 ×10 (the sweep of every open milestone, views 1/2 × 36/80/118/160; a start date and no due; a late milestone; the non-milestone row), AT-2101 |
| `tests/present_portfolio_board.py` | test | HLR-2101, HLR-2103 | new: the round's synthetic board as a fixture (Security Audit hidden through `Project.extra`, as the round did, until increment 002) |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_milestone.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`, `NO_COLOR` unset); the battery: `python .dev-flow/2026-10-19-batch-01/evidence/mutate.py 001`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | `tests/test_present_milestone.py::test_TC_2101_a_milestone_row_is_its_date_not_a_bar[*]` ×8, `::test_TC_2101_a_start_date_does_not_make_a_milestone_a_bar`, `::test_TC_2101_other_rows_are_drawn_as_shipped`, `::test_TC_2101_a_late_milestone_is_painted_over` (TC-2101) | in the full suite (`suite-001.txt`) |
| B | `tests/test_present_milestone.py::test_AT_2101_the_cut_over_weekend_reads_as_a_milestone` (AT-2101) | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree with increment 001 | 0 failed, 2768 passed, 1 skipped (the clipboard roundtrip, its refusal quoted) — `suite-001.txt` (2757 on `base_ref` + the 11 nodes this increment first wrote); after the code review's F1/F2 were folded (the `⟦` lead asserted, one late-milestone node added), `tests/test_present_milestone.py` alone: 12 passed (`fold-001.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | the two test files copied into a scratch worktree at `base_ref` `bdf6e9d`, source untouched: TC-2101 ×10 and AT-2101 RED — 11 failed, 1 passed (the non-milestone control, a regression pin) · `.dev-flow/2026-10-19-batch-01/evidence/red-001.txt` |
| **Mutation verdicts** | 5 mutants over `taskboard/views.py`, the selection pre-checked GREEN: M1 the branch removed (the bar returns) · KILLED; M2 the chip keeps the start date · KILLED; M3 the cursor's `◆` not accented · KILLED; M4 the label's `◆` dropped · KILLED; M5 the cursor's `⟦` lead never drawn (code review F1) · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-19-batch-01/evidence/mutation-001.txt` (harness `evidence/mutate-001.py`, the version that ran it) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate.py` — its pre-check refuses a red selection (exit 2 before any mutant), and every mutant's restore is checked by digest; its five arms RED above |
| **Emitted-form assertion** | 1 artifact: the frame as `#present-frame` holds it (`content.plain`, AT-2101), which is the frame `x` exports (`_frame_text`, unchanged) |
| **Reverse census** | 5 probes: B1 `grep -rl "_present_task_row" tests/` → none; `grep -l milestone tests/present_board.py tests/present_notes_board.py` → none, so the PRES-V3/V4 frame tests (`test_present.py`, `test_present_views.py`, `test_present_views_app.py`, `test_present_polish.py`) cannot drift — green in `suite-001.txt` · B2 no file moved · B3 no golden captures a milestone row · B4 the export writes the same frame · A3 no other module — 0 foreign hits |
| **Correction population** | none — no shipped assertion pinned the bar |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-19-batch-01/evidence/suite-001.txt | 720d5b5b46cfb1d8523611c678b62ba38c5113bce3969d8f1bb1088347759a33 |
| red-001.txt | .dev-flow/2026-10-19-batch-01/evidence/red-001.txt | 9f6d2cee6af88758ebde0a13ca917009d11826caf2526326a15df787e4335466 |
| mutation-001.txt | .dev-flow/2026-10-19-batch-01/evidence/mutation-001.txt | 776e29f69bc138aab713dc29a49bf5125d787f2de0dd5f41ba3c98b9d4047fb7 |
| mutate-001.py | .dev-flow/2026-10-19-batch-01/evidence/mutate-001.py | 998fc0e2ce577d7db227da29ca2853dff1e8d3b8e638aed551524c742d7ae036 |
| fold-001.txt | .dev-flow/2026-10-19-batch-01/evidence/fold-001.txt | c68f8db7199ffe95df93501a1864856cc5a8f03a4867ef74775a854d18150708 |
| view1-118x31-after.svg | .dev-flow/2026-10-19-batch-01/evidence/captures/view1-118x31-after.svg | c14b637bb772ed253a5cc8f4d174d3d795062c8c79bf34ff45021e3da44a3171 |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK with findings, 0 HIGH: F1 LOW (the `⟦` lead unasserted) and F2 LOW (no late milestone) folded into TC-2101; F3 LOW (a redundant `_pad`) kept by the reviewer's own note; F4 accepted (the fixture copy) |

## 5 · Risks

The ruler's echo for a milestone cursor still reads `no start · due <Mon D>`, as the board gantt's does (out of scope, §1.2 of the contract).

## 6 · Pending items / spec deviations

none.

## 7 · Suggested next task

Increment 002 — the model (HLR-2102).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_milestone.py` |
| 3 | Layer 0 where it applies | ✓ | not due: one branch, no boundary crossed |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b: OK with findings, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | the census's "none" rests on two greps, quoted |
| 11 | Mutation verdicts | ✓ | §4: 5/5 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

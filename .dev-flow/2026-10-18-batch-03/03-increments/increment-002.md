# Increment 002 — LLR-2002.1 · `the middle hint wording`

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
> `.dev-flow/2026-10-18-batch-03/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-18-batch-03` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2002` / `LLR-2002.1` |
| Acceptance | `AT-2002` · white-box none — the method is the unit · unit `TC-2002`, `TC-1904` (updated) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-18` |

---

## 1 · What changed

At 80 columns the hint row now names `next` and `show all`: `PresentScreen._hint` tries a middle wording — `⇥ next · ←→ ↑↓ · ␣ hide · a show all · x export · esc`, with `pgdn · ` before it in the split view and two-space gaps after the view names — right after the long one and before the short one (the round's `HINT_A`, verbatim; variant A of item 2). At 80×25 with nothing hidden both views take it (the split view's is exactly the 78 cells the row holds); with a task hidden the count leaves room only for the short wording, as shipped. Surface: `R` → `#present-hint`. Also, test-only: `tests/test_help_keys.py::test_AT_1603…` waits, bounded, for the help's scroll to paint instead of reading it after 3 pauses — the pre-existing timing flake that failed `suite-001.txt` (2 of 8 runs on `base_ref`), hardened for the commission's 0-failure target.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-2002.1 | `_hint`: the middle wording between the long and the short one; its docstring |
| `tests/test_present_polish.py` | test | HLR-2002, LLR-2002.1 | new: TC-2002 ×8 (both views × 0/1/3/10 hidden: the middle wording's first width, one below the long one's, the short a column narrower, the long at its first width), AT-2002 |
| `tests/test_present_narrow.py` | test | LLR-2002.1, LLR-1904.1 | law-driven: TC-1904's table gains the `middle` tier (gantt 73 / 84 / 85, split 80 / 91 / 92 for 0 / 3 / 10 hidden — P-3); every other tier and the monotonicity check unchanged |
| `tests/test_present_views_app.py` | test | LLR-2002.1, LLR-1803.2 | law-driven: TC-1808's cells at 100 / 99 split + 1 hidden, 96 split and split + 1 hidden, 80 gantt and split → the middle wording (`MIDDLE`); 80 split + 1 hidden stays short; the docstring says why |
| `tests/test_present_hide.py` | test | LLR-2002.1, LLR-1602.2 | law-driven: TC-1604 at 80×25 — the middle wording with nothing hidden, the short one with two hidden (two expected strings; qa-reviewer QA-5) |
| `tests/test_help_keys.py` | test | HLR-1603 | AT-1603: a bounded wait (≤ 50 pauses) for the gantt pairs after `end`, then the same assertions |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 5 (uncapped) |
| Doc files | 0 |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_polish.py -k 2002`; `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py tests/test_present_views_app.py tests/test_present_hide.py tests/test_help_keys.py` (with `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8`); the battery: `python .dev-flow/2026-10-18-batch-03/evidence/mutate.py 002` from the root of a scratch copy of the tree.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 | `tests/test_present_polish.py::test_TC_2002_the_middle_wording_sits_between_the_long_and_the_short[gantt-0 … split-10]` ×8 (TC-2002); `tests/test_present_narrow.py::test_TC_1904_the_hint_takes_the_first_wording_that_fits` (TC-1904, updated) | in the full suite (`suite-002.txt`) |
| B | `tests/test_present_polish.py::test_AT_2002_the_80_column_hint_names_next_and_show_all` (AT-2002) | in the full suite (`suite-002.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree with increments 001 and 002 | 0 failed, 2754 passed, 0 skipped (`suite-002.txt`; 2745 + the 9 new nodes; the hardened AT-1603 green). After the suite, code-review F1 folded test-only (TC-1904 sweeps 1 hidden too, LED .5): `tests/test_present_narrow.py` re-run, 6 passed (no transcript kept; green in the later full run `suite-003.txt`, 0 failed — DDR C2) |

| Field | Value |
|---|---|
| **RED counterfactual** | the five test files copied into a scratch worktree at `base_ref` `620f58c`: 18 failed, 27 passed — TC-2002 ×8, AT-2002, TC-1904, TC-1808 ×4 (100, 99, 96, 80), TC-1604 [80] RED on the missing wording (and 001's three nodes, RED there by design) · `.dev-flow/2026-10-18-batch-03/evidence/red-002.txt` · the battery's restore digests below |
| **Mutation verdicts** | 4 mutants, 8 arms, every node pre-checked GREEN on the unmutated copy: 8 KILLED — N1 no middle wording → TC-2002 [gantt-0], TC-1904, AT-2002 · N2 the middle wording tried before the long one → TC-2002 [split-3], TC-1904 · N3 its gap one space → TC-2002 [gantt-10], AT-2002 · N4 its keys drop `show all` → AT-2002; arms that stayed GREEN: none · `.dev-flow/2026-10-18-batch-03/evidence/mutation-002.txt` · `app.py` restored to `603cff7e17cd…` by digest after every arm |
| **Instrument RED-proof** | 2 instruments: `mutate.py` (8 arms RED; its pre-check, increment 001); `tests/test_help_keys.py`'s hardened AT-1603 — its assertions are the shipped ones, read after the wait: the flake's RED is `flake-001.txt` (2/8 failed on base), 20/20 passed after (`flake-002.txt`) |
| **Emitted-form assertion** | 1 artifact: the hint as `#present-hint` holds it (`content.plain` and its `Text` spans, AT-2002, TC-1808, TC-1604) |
| **Reverse census** | 5 probes: B1 `grep -rl "_hint\|present-hint" tests/` → `test_present_hide.py`, `test_present_narrow.py`, `test_present_views_app.py` (each updated, named in §2), `test_gantt_polish.py`, `test_link_picker.py` (other screens' own `_hint`: untouched, green) · B2 no file moved · B3 no goldens; the hint is outside the frame, so no frame oracle reads it · B4 the hint is never exported (`x` writes the frame only: AT-1802 and the PRES-V3 nodes unchanged) · A3 `_hint` has no caller outside `app` but the frozen round (`grep -rn "_hint(" --include=*.py taskboard prototypes/backlog_polish` → `taskboard/app.py`, `prototypes/backlog_polish/capture.py`) |
| **Correction population** | 1 correction: the shipped hint tests that pin the short wording where the middle one now fits · enumerated before the first edit with `grep -rn "a all · x export" tests/` → `test_present_hide.py:231`, `test_present_narrow.py:90/94`, `test_present_views_app.py:260` (and the qa-reviewer's cell list QA-5/QA-6) · every cell the middle tier reaches edited (§2), every cell it does not (118 / 100 / 99 gantt and split, 80 split + 1 hidden, TC-1604's two-hidden arm) left with its literal |

**The round comparison** (`compare-002.txt`): the real app's captures against the round's contrast and hint A forks composed, re-run on `base_ref` (`expected/upto-2.txt`): 6 EQUAL — the hint row at 80×25 in both views equals the round's `HINT_A` capture — and 4 DIFFER, each exactly the gantt cut row's `· ` lead declared in increment 001 (`explain_diff.py`'s run-by-run listing at the end of the transcript); nothing else differs.

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-18-batch-03/evidence/suite-002.txt | b39fcd5c7c2d7c6ea3cb401a6c01ece76674b53ad1c90856c5b109a6a6bc7ab2 |
| red-002.txt | .dev-flow/2026-10-18-batch-03/evidence/red-002.txt | e29f430bc83addcc30d82a9b56246bbc17c262b62d5437a2bbf71427f8ea99f1 |
| mutation-002.txt | .dev-flow/2026-10-18-batch-03/evidence/mutation-002.txt | e3704896faee3f39c93bd80785493078115ca7ab80943fb30c95a9737174484d |
| flake-002.txt | .dev-flow/2026-10-18-batch-03/evidence/flake-002.txt | 63c6d1b36199e7f7b3cc0fdf55cada0e92fccab4acd38473774343d7c14e8230 |
| compare-002.txt | .dev-flow/2026-10-18-batch-03/evidence/compare-002.txt | 133d6f420b0a88ed6c4e58cdf8cd640ff3cf4145d76b570fdaeb94ddedc54e56 |
| explain_diff.py | .dev-flow/2026-10-18-batch-03/evidence/explain_diff.py | 11e9ea4679816e7428515e50cb5d3eef94b89a02eeb1e38062764c16d29535b4 |
| mutate-001-002.py | .dev-flow/2026-10-18-batch-03/evidence/mutate-001-002.py | 22499429ec513dcc326b0d1bf5c9ca836076d6d110181cde1470ffa5ffe95908 |

| Field | Value |
|---|---|
| **Evidence files** | `7 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned with agents/code-reviewer.md · OK to advance, 0 HIGH · F1 MEDIUM (LLR-2002.1 claimed a 1–140 sweep at 1 hidden no node ran) → fixed: TC-1904 sweeps 0 / 1 / 3 / 10 hidden, the threshold restated (LED .5) · F2 LOW (the wordings repeated as literals in three test files) → kept: each is a literal oracle, deliberately not shared with the code or each other · the AT-1603 hardening judged not weakening (the same assertions after a bounded wait) · the law-driven updates judged equally exact or stronger |

## 5 · Risks

The middle wording drops `move` and `leave` from the long one; the round showed it so and the operator approved it. At widths where a hidden count pushes the hint below the middle wording, the short one returns as shipped.

## 6 · Pending items / spec deviations

- The AT-1603 hardening is outside the three commissioned items — a test-only change for the commission's 0-failure target, declared here; `BACKLOG.md`'s flake line closes at the batch close.

- The battery ran with the harness as it stood at increments 001–002, kept as `evidence/mutate-001-002.py` (digest above); `evidence/mutate.py` later gained increment 003's anchors.

## 7 · Suggested next task

Increment 003 — the gantt note fills the free rows (HLR-2003).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | §2: 9 new nodes, 4 updated files |
| 3 | Layer 0 where it applies | ✓ | `_hint` (a loop over five wordings): TC-2002, TC-1904 |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt` |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 8/8 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 1, enumerated |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: digests |

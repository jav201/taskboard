# Increment 005 — LLR-2106.1 · `the presentation stays in view behind the picker`

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
> `.dev-flow/2026-10-19-batch-01/03-increments/increment-005.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-19-batch-01` |
| Increment | `005` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2106` / `LLR-2106.1` |
| Acceptance | `AT-2106` (unchanged, green) · white-box `TC-2106` (the backdrop) · unit none — one style line |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-20` |

---

## 1 · What changed

The coordinator's follow-up of 2026-10-20 on the capture `seq-160x45-4-picker`: the `u` picker opened over a blank screen. Cause: the app's `Screen { background: #0d1117 }` rule (`taskboard/taskboard.tcss:3-6`) paints every screen opaque unless a later rule says otherwise — the edit modals and pickers share one (`taskboard.tcss:290-293`, `#0007`), which this change missed (the code review's F1, folded in 006) — so Textual's own `ModalScreen` backdrop (the background at 60%) never applied. `PresentHiddenPicker` now sets, inline (an inline style outranks the app's type rule, which outranks `DEFAULT_CSS`), the presentation's colour at 60% (`Color(13, 17, 23, 0.6)`): the presentation stays in view behind the list, dimmed. Every capture of the batch was re-taken on this tree.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | LLR-2106.1 | `PresentHiddenPicker.__init__`: the translucent backdrop; `Color` imported |
| `tests/test_present_all.py` | test | HLR-2106 | new: TC-2106 — the screenshot with the picker open holds the frame's text |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "picker or stays_in_view"`; the capture: `python .dev-flow/2026-10-19-batch-01/evidence/capture.py <out> seq`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | `tests/test_present_all.py::test_TC_2106_the_presentation_stays_in_view_behind_the_picker` | 2 passed with the picker nodes (`-k "stays_in_view or picker"`, run by the orchestrator); in the P4 gate run at `91d1f8c` (`suite-p4.txt`) |
| full suite | none at `7c4140a`: the run started there was stopped when the code review moved the backdrop into the app's shared modal rule (increment 006); the full suite ran at `91d1f8c`, which holds this change's node | `suite-p4.txt` |

| Field | Value |
|---|---|
| **RED counterfactual** | the node on `fc55d3a`'s `modals.py` (the opaque picker), the rest of the tree as now: 1 failed — the screenshot holds the picker and no frame text · `.dev-flow/2026-10-19-batch-01/evidence/red-005.txt` |
| **Mutation verdicts** | 1 mutant: the backdrop line removed — the same state as the RED capture (the line is the whole change) · KILLED · `.dev-flow/2026-10-19-batch-01/evidence/red-005.txt` |
| **Instrument RED-proof** | none — no instrument beyond the suite and `capture.py` (packet 004) |
| **Emitted-form assertion** | 1 artifact: the app's own `export_screenshot()` SVG with the picker open (the node, and `captures/seq-160x45-4-picker.svg`) |
| **Reverse census** | 5 probes: B1 `grep -rln "PresentHiddenPicker" tests/` → `tests/test_present_all.py` only · B2 no file moved · B3 no golden reads the picker · B4 the captures re-taken · A3 `modals` imports `textual.color`, an allowed direction — 0 foreign hits |
| **Correction population** | none — no shipped assertion touched |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| red-005.txt | .dev-flow/2026-10-19-batch-01/evidence/red-005.txt | adfb9832f19ed3d544a44faf7372f4b7ac0167c1673ddcc1d0da72336c17208c |
| suite-p4.txt | .dev-flow/2026-10-19-batch-01/evidence/suite-p4.txt | 9717f81a2c47e381a44c3862f5f1257e06fabba1b7475cba5a010b7f17829257 |
| seq-160x45-4-picker.svg | .dev-flow/2026-10-19-batch-01/evidence/captures/seq-160x45-4-picker.svg | 3ad11440d82b38f11e614119f71e5e614d2c6b5472999ee5512846e778103432 |

| Field | Value |
|---|---|
| **Evidence files** | 3 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK to advance: F1 MEDIUM (the inline colour departs from the app's shared modal rule `taskboard.tcss:290-293`, `background: #0007`) and F2 LOW (the node does not check the dimming) — both folded in increment 006 |

## 5 · Risks

The other modals of the app stay opaque (unchanged; the presentation's picker is the one that should show what it filters).

## 6 · Pending items / spec deviations

none.

## 7 · Suggested next task

Phase 4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | the backdrop node |
| 3 | Layer 0 where it applies | ✓ | not due: one style line |
| 4 | RED counterfactual | ✓ | §4, `red-005.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b: OK, F1/F2 folded in 006 |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-p4.txt` (at `91d1f8c`) |
| 10 | Load-bearing emptiness | ✓ | the census's grep quoted |
| 11 | Mutation verdicts | ✓ | §4: KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

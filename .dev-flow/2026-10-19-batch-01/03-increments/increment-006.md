# Increment 006 — LLR-2106.1 · `the shared backdrop and the first hidden row`

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
> `.dev-flow/2026-10-19-batch-01/03-increments/increment-006.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-19-batch-01` |
| Increment | `006` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2105`, `HLR-2106` / `LLR-2106.1` |
| Acceptance | `AT-2105` (the folded caret), `AT-2106` · white-box `TC-2106` (the backdrop, the picker's first row) · unit none — two lines and a CSS selector |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-20` |

---

## 1 · What changed

Three findings of the code review of 005 and of Phase 4, folded before the gate. The picker's backdrop moves from 005's inline colour into the rule the app's other modals share (`taskboard.tcss`, `TaskModal, …, CalendarModal, PresentHiddenPicker { align: center middle; background: #0007; }`), and the node now checks the backdrop is translucent (`0 < alpha < 1`). The picker's cursor opens on its first hidden row: in view 3 a shown project is listed (`●`) only as the heading of its hidden tasks, and `u` then `space` on row 0 hid a project the presenter was showing (ux-reviewer UX4-1, major, driven headless); its key line now reads `↑↓ move · ␣ show/hide · ○ hidden · esc close` (UX4-2). AT-2105 reads the folded project's `▸` caret after moving the cursor off its header (the cursor's `⟦` lead had hidden the caret — qa-reviewer G-1). `docs/ARCHITECTURE.md`: `PresentAll` names its six fields (the DDR's drift), the picker row its first row and its backdrop. The capture script's step after `u` toggles the first row, and every capture was re-taken.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | LLR-2106.1 | `PresentHiddenPicker`: the cursor on the first hidden row, the key line; the inline backdrop and the `Color` import removed |
| `taskboard/taskboard.tcss` | source | LLR-2106.1 | `PresentHiddenPicker` joins the shared modal backdrop rule |
| `tests/test_present_all.py` | test | HLR-2105, HLR-2106 | TC-2106: the first row, the translucent backdrop; AT-2105: the caret off the cursor; the resize node pauses after each resize |
| `docs/ARCHITECTURE.md` | doc | LLR-2103.1, LLR-2106.1 | the `PresentAll` and `PresentHiddenPicker` rows |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 1 (uncapped) |
| Doc files | 1 (outside the count) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_all.py` (49 nodes); the captures: `python .dev-flow/2026-10-19-batch-01/evidence/capture.py <out> seq`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A, B | `tests/test_present_all.py` (49) | 49 passed (run by the orchestrator before the commit); in the P4 gate run |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean worktree at `91d1f8c` | 0 failed, 2819 passed, 0 skipped (`suite-p4.txt`, exit 0; the P4 gate run) |

| Field | Value |
|---|---|
| **RED counterfactual** | the nodes on `7c4140a`'s `modals.py` and `taskboard.tcss`: TC-2106 (the picker) RED — the cursor `▶` on `● Customer Portal`, row 0 · `.dev-flow/2026-10-19-batch-01/evidence/red-006.txt`; the backdrop node RED on the opaque picker (`red-005.txt`) |
| **Mutation verdicts** | 2 mutants, each the state of a RED capture: the cursor at row 0 (`red-006.txt`) · KILLED; the picker out of the shared rule — the opaque backdrop of `fc55d3a` (`red-005.txt`) · KILLED · arms that stayed GREEN: none |
| **Instrument RED-proof** | none — no new instrument (`capture.py`'s step changed to match the first row) |
| **Emitted-form assertion** | 2 artifacts: `#picker-rows`'s `Text` (the cursor's row) and the app's `export_screenshot()` SVG with the picker open |
| **Reverse census** | 5 probes: B1 `grep -rln "PresentHiddenPicker\|picker-rows" tests/` → `tests/test_present_all.py` only · B2 no file moved · B3 no golden reads `taskboard.tcss`'s modal rule (`grep -rln "#0007" tests/` → none) · B4 the captures re-taken · A3 `modals` drops `textual.color` — 0 foreign hits |
| **Correction population** | 1 correction: AT-2105's fold check (`▸` or `⟦` → `▸` after `↑`) — the one assertion that accepted the cursor's lead in place of the caret (qa-reviewer G-1) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| red-006.txt | .dev-flow/2026-10-19-batch-01/evidence/red-006.txt | 89f29f21ecdf2643fde8591462b7092db79338e77d8416811601107b9d5e0c65 |
| red-005.txt | .dev-flow/2026-10-19-batch-01/evidence/red-005.txt | adfb9832f19ed3d544a44faf7372f4b7ac0167c1673ddcc1d0da72336c17208c |
| suite-p4.txt | .dev-flow/2026-10-19-batch-01/evidence/suite-p4.txt | 9717f81a2c47e381a44c3862f5f1257e06fabba1b7475cba5a010b7f17829257 |
| seq-160x45-4-picker.svg | .dev-flow/2026-10-19-batch-01/evidence/captures/seq-160x45-4-picker.svg | 3ad11440d82b38f11e614119f71e5e614d2c6b5472999ee5512846e778103432 |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · APPROVE, 0 major: three minor notes kept open — the alpha check passes on 005's inline colour too (it proves the dimming, not the rule), the resize node's pauses not named in the commit message (named here), the key line explains `○` and not `●` |

## 5 · Risks

none new — the picker now dims the presentation as the edit modals dim the board.

## 6 · Pending items / spec deviations

UX4-4..UX4-7 of the P4 walkthrough are recorded in `04-validation.md` and `BACKLOG.md`.

## 7 · Suggested next task

Phase 4's gate run, then the close.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | `tests/test_present_all.py` |
| 3 | Layer 0 where it applies | ✓ | not due |
| 4 | RED counterfactual | ✓ | §4, `red-006.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-p4.txt` |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 2/2 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: 1, named |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

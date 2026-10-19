# Increment 003 — LLR-2103.1 · `the renderer of Present view 3`

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
> `.dev-flow/2026-10-19-batch-01/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-19-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2103` / `LLR-2103.1`; the rows of `LLR-2106.1` |
| Acceptance | `AT-2103` (lands with increment 004, which binds `3`) · white-box `TC-2103`, `TC-2106` (the rows) · unit: the auto-fold loop through TC-2103's sweep |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-19` |

---

## 1 · What changed

`views.render_present_all(board, cursor, today, width, height, folded, rail_focus)` draws Present view 3: the round's variant C (`prototypes/present_portfolio/portfolio_proto.py`, its A/C path) moved into `views` — the header (`◆ PRESENT · N projects  all`, open and past-due counts), the ruler fitted to the shown projects' open work with the cursor's dates echoed (`project span ▸` on a header), per shown project in `present_order` a header row and its shown open tasks (each through `_present_task_row`, so milestones are increment 001's diamonds), a blank row between projects while everything fits, the projects furthest from the cursor's folded when the rows do not fit, and from 100 columns a 24-cell rail and a `│` listing every visible project numbered with `●`/`○`. It returns `PresentAll(frame, timeline, timeline_w, stops, rail_stops, cursor)`; below 36 columns it is `render_present`'s narrow frame. `PRESENT_SCREEN_VIEWS = PRESENT_VIEWS + ("all",)` and `present_hidden_rows` (what `u` will list) are added. Nothing in the app reaches it yet (increment 004). Differences from the round, each deliberate: milestones through the fixed row; a `Task` (not a `SimpleNamespace`) carries the project span to `gantt_echo`; the returned cursor is the drawn one; B's code left out. Its frame text equals the round's approved C captures at 160×45 and 118×30, row for row.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/views.py` | source | LLR-2103.1, LLR-2104.1, LLR-2106.1 | `PRESENT_SCREEN_VIEWS`, `PRESENT_RAIL_MIN`, `PRESENT_RAIL_W`, `PresentAll`, `render_present_all` and its helpers, `present_hidden_rows`; `present_order` imported from `models` |
| `tests/test_present_all.py` | test | HLR-2103, LLR-2103.1, LLR-2106.1 | TC-2103 ×12 (the sweep over three boards × seven widths, the ranked order, the round's captures read as files, the markup payloads, the empty states), TC-2106's rows |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2103 or TC_2106"`; the battery: `python .dev-flow/2026-10-19-batch-01/evidence/mutate.py 003`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A | `tests/test_present_all.py::test_TC_2103_*` ×12, `::test_TC_2106_the_hidden_rows` | in the full suite (`suite-003.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean worktree at `231e56b` | 0 failed, 2804 passed, 1 skipped (`suite-003.txt`; 2791 + the 13 nodes this increment wrote) |

| Field | Value |
|---|---|
| **RED counterfactual** | the test file and the fixture copied into a scratch worktree at `base_ref` `bdf6e9d`, source untouched: TC-2103 ×12 and TC-2106's rows RED — 13 failed (`render_present_all` and `present_hidden_rows` do not exist) · `.dev-flow/2026-10-19-batch-01/evidence/red-003.txt` |
| **Mutation verdicts** | 8 mutants, the selection pre-checked GREEN: P1 the rail below 100 columns · KILLED; P2 hidden projects on the timeline · KILLED; P3 the auto-fold may fold the cursor's project · KILLED; P4 the order ignores `present_rank` (QA-13's witness) · KILLED; P5 the rail's name without `escape` (PC-2) · KILLED; P6 the header's name without `escape` (PC-2) · KILLED; P7 a hidden project's own hidden tasks dropped from `u` · KILLED; P8 `u` lists shown tasks · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-19-batch-01/evidence/mutation-003.txt` (harness `evidence/mutate-003.py`) |
| **Instrument RED-proof** | 2 instruments: `evidence/mutate.py` (packet 001); the test's SVG reader `_svg_rows` — it reads the round's capture as a file, and a reader that matched nothing would leave blank rows the frame never equals (the code reviewer's check) |
| **Emitted-form assertion** | 1 artifact: the frame's `Text` (its plain text and spans) as the screen will paint it; the export's file is increment 004's AT-2104 |
| **Reverse census** | 5 probes: B1 `grep -rl "PRESENT_VIEWS\|render_present\b" tests/` → the PRES-V3/V4 frame and hint tests — `PRESENT_VIEWS` unchanged, green in `suite-003.txt` · B2 no file moved · B3 no golden captures view 3; the round's C captures are read, not written · B4 nothing consumes the new frame yet · A3 `views` imports `models.present_order`, an allowed direction — 0 foreign hits |
| **Correction population** | none — no shipped assertion touched |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-19-batch-01/evidence/suite-003.txt | bc0b1a183301ac106ea5d66e361558e7a042b13950706cf93e9f114456e35d32 |
| red-003.txt | .dev-flow/2026-10-19-batch-01/evidence/red-003.txt | dacd87cc27835753b18088ea87cc12e4d7deed76fcbf81f8652d1a711c852668 |
| mutation-003.txt | .dev-flow/2026-10-19-batch-01/evidence/mutation-003.txt | d0b1dc3db5bc92715303c06570345321e038ccfba2fa237163ba0d65c00c4449 |
| mutate-003.py | .dev-flow/2026-10-19-batch-01/evidence/mutate-003.py | f79aa3b7dbbbbc129c2b81f8e736b570c816c65ab38b54980a4aa96fa074a2d0 |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK with findings, 0 HIGH: F1 MEDIUM (stops included rows the overflow row covers) — fixed in increment 004 (`views.py`, the drawn-row trim) with a regression node RED without it; F2 MEDIUM (the sweep's heights bounded to 10 and 45, against the LLR's four) — the bound is QA-12's, the threshold amended (LED-2026-10-19-batch-01.4); F3 LOW (the rail's hidden-task count over shown projects only) — aligned with HLR-2103 in increment 004; F4 LOW (`_all_fit` repeats `_present_finish`'s overflow rule) — kept, a frame and a row list; F5 LOW (labels short at 100–124 columns, as the round) — kept |

## 5 · Risks

At heights where even the folded headers overflow, the projects past the overflow row are not reachable with `↑↓` on the timeline (the rail, from 100 columns, lists them all; selecting one there folds the others first) — inherited from the round; recorded.

## 6 · Pending items / spec deviations

The sweep runs heights 10 and 45 (LED .4); the review's F1 and F3 land in increment 004's `views.py` change.

## 7 · Suggested next task

Increment 004 — the screen and the picker.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_all.py` |
| 3 | Layer 0 where it applies | ✓ | the auto-fold loop through the sweep |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b: OK with findings, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-003.txt` |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 8/8 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

# Increment 002 — LLR-2304.1, LLR-2306.1 · `an unarchived project never ties a rank; _move_target(proj, bid)`

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
> `.dev-flow/2026-10-20-batch-02/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-02` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2304`, `HLR-2306` / `LLR-2304.1`, `LLR-2306.1` |
| Acceptance | `AT-2304` · white-box `TC-2304`, `TC-2306` · unit: the unarchive rank rule (Layer 0 by the decision criterion: tie / no tie / no rank, `TC-2304`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in the scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

Unarchiving a project in the projects modal (`P`, `x`) no longer lets it tie a presentation rank. `ProjectPicker._do_archive_toggle` keeps the project's `present_rank` when no other project the presentation lists holds the same rank (an archive undone at once keeps its place, ux UX-1), and otherwise gives it one more than the largest rank among the other listed projects — archived projects' ranks and its own never counted — before the board is saved. `ProjectPicker._move_target` takes `(proj, bid)`: the picker's copy of the boards it never read is no longer passed (code review N2 of 2026-10-20-batch-01). HLR-2304's title and outcome now say "never ties" (LED .3, PDR condition PC-4).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/modals.py` | source | LLR-2304.1, LLR-2306.1 | `_do_archive_toggle`'s rank rule; `_move_target(proj, bid)` and its callback |
| `tests/test_present_all.py` | test | HLR-2304, LLR-2304.1 | appended: TC-2304, AT-2304 |
| `tests/test_hygiene.py` | test | HLR-2306, LLR-2306.1 | new: TC-2306 (AT-2306 joins at increment 003) |
| `.dev-flow/2026-10-20-batch-02/evidence/mutate-002.py` | doc | HLR-2304, HLR-2306 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **1 / 4** |
| Test files | 2 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_all.py tests/test_hygiene.py -k "2304 or 2306"` (with `NO_COLOR` unset); the targeted set of `suite-002.txt`; `python .dev-flow/2026-10-20-batch-02/evidence/mutate-002.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_present_all.py::test_TC_2304_the_unarchive_rank_rule`, `::test_AT_2304_an_unarchived_project_never_ties_a_rank`, `tests/test_hygiene.py::test_TC_2306_move_target_takes_the_project_and_the_board` — 3 nodes | executed: 310 passed in the targeted run of the presentation, hygiene, archive, move, markup-site and app files (`suite-002.txt`) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 001's commit `d7c3dea` (a clean worktree, `taskboard/` untouched, the two test files copied in): 3 failed — TC-2304 `(0, 1, 0) == (2, 1, 0)` (the tie kept), AT-2304 the ranks `{'pcp': 0, …}` not distinct (Customer Portal tied, listed first), TC-2306 `['self', 'proj', 'bid', '_boards']` · `.dev-flow/2026-10-20-batch-02/evidence/red-002.txt` |
| **Mutation verdicts** | 6 arms over 5 mutants, one run, each restore proven by digest: the rank kept on a tie · KILLED ×2 (TC, AT-2304); always re-ranked (UX-1) · KILLED; archived projects' ranks counted · KILLED; its own rank counted · KILLED; the unused parameter back · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-02/evidence/mutation-002.txt` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-002.py` — increment 001's harness (`mutate-001.py`, its RED seen at increment 001: a `BAD` anchor and a `SURVIVED` arm) with this increment's arms; `arms: 6` |
| **Emitted-form assertion** | 1 artifact: the board file (`json.loads` of its bytes: `present_rank`, `archived`) read after each step of AT-2304 and at the end of TC-2304 |
| **Reverse census** | 4 probes: B1 `grep -rln "_do_archive_toggle\|action_archive\|present_rank\|_move_target" tests/` → `test_archive.py` (the toggle's archive half — green), `test_boards_move.py` (a move clears `present_rank`; AT-2206 drives the callback — green), `test_present_all.py` — all in `suite-002.txt`, 310 passed · B2 no file moves · B3 no golden capture renders an unarchived project's order · B4 the board file's `present_rank` — read by `present_order` (AT-2304) — 0 foreign hits |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-20-batch-02/evidence/suite-002.txt | 71cbad8f343a0682044798c3e2792b073d7ed0a5464cd89479c1db575d8a3133 |
| red-002.txt | .dev-flow/2026-10-20-batch-02/evidence/red-002.txt | 8fe09a210fe08e9efa45d8902579a966143ec39b8d90dd670d14101db35e59f5 |
| mutation-002.txt | .dev-flow/2026-10-20-batch-02/evidence/mutation-002.txt | fb4acf0483573aabc152867d7c72296ad1ad81bcbf5d9bfbf3e79fce0d46ac8f |
| mutate-002.py | .dev-flow/2026-10-20-batch-02/evidence/mutate-002.py | b090cba619b8563141773f819a7da05ec733fea597a9c0bf066c9930ebf5454c |
| inc002.diff | .dev-flow/2026-10-20-batch-02/evidence/inc002.diff | 77a2ff9feb8ce2b70339fca6b35ba06f1058be1f214b05bbddf20016b5119a8f |

| Field | Value |
|---|---|
| **Evidence files** | 5 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` · **OK to advance** (PASS) · no findings; LLR-2304.1 and LLR-2306.1 verified by re-read against `present_order`, `set_present_order` and the move callback; N1–N5 KILLED |

## 5 · Risks

A team pull unarchives a shared project outside the picker (`taskboard/team_sync.py:289-290` sets `archived` from the teammate's `team.json`, and never writes `present_rank`, `:296-297`), so that path can still leave a tied rank; board order then breaks the tie as before. Out of the commission's item (the picker's unarchive) — carried to `BACKLOG.md` at the close.

## 6 · Pending items / spec deviations

The full suite is owed at P4. AT-2304 sets the selection on the round's cursor task as set-up, through `_Show.open` (qa QA-10), as every presentation node does. PC-4 (UX-9) discharged by LED .3.

## 7 · Suggested next task

Increment 003 — the hardened tests (tests only, LLR-2306.2).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 1 source file |
| 2 | Tests in this increment | ✓ | `tests/test_present_all.py`, `tests/test_hygiene.py` |
| 3 | Layer 0 where it applies | ✓ | the rank rule's three branches |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 4 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-002.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 6/6 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

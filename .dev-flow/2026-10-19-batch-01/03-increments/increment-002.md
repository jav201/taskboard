# Increment 002 — LLR-2102.1 · `a project's presentation state on the board`

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
> `.dev-flow/2026-10-19-batch-01/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-19-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2102` / `LLR-2102.1` |
| Acceptance | `AT-2102` (lands with increment 004, which ships the keys it drives) · white-box `TC-2102` · unit: the load rule's type table (Layer 0, `TC-2102` ×18 parametrized) |
| Agent | `software-dev` (the orchestrator, self-implemented) |
| Date | `2026-10-19` |

---

## 1 · What changed

`Project` carries two presentation fields: `show_in_present` (True by default; the JSON `false` alone hides — the save rule `Board._to_dict` already applies to tasks covers projects with no new branch, P-2) and `present_rank` (None by default; only a non-boolean integer is kept, any other value read as None, never raising; `_to_dict` drops a None rank so a board without ranks keeps its bytes). Both are in `_PROJECT_KEYS`, so neither lands in `extra`. `models.present_order(board)` returns the visible projects ranked first by rank, then the unranked, board order breaking ties; `models.set_present_order(board, ids)` writes rank `i` on `ids[i]`. `team_sync`'s pull builds a new team project without the two keys (security S-4): a teammate's `team.json` never curates this board's presentation. The test fixture now hides Security Audit through the field.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-2102.1 | `Project.show_in_present`, `Project.present_rank`, their load rule, `_PROJECT_KEYS`; `_to_dict` drops a None rank; `present_order`, `set_present_order` |
| `taskboard/team_sync.py` | source | LLR-2102.1 | the pull strips `show_in_present` / `present_rank` from a new project's entry |
| `tests/test_present_all.py` | test | HLR-2102, LLR-2102.1 | new: TC-2102 ×22 (the load table ×18, the save rule, byte-identity, the order, the team pull) |
| `tests/present_portfolio_board.py` | test | LLR-2102.1 | Security Audit hidden through the field |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 2 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2102`; the battery: `python .dev-flow/2026-10-19-batch-01/evidence/mutate.py 002`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 and A | `tests/test_present_all.py::test_TC_2102_*` ×22 (TC-2102) | in the full suite (`suite-002.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` in a clean worktree at `1c601bc` | 0 failed, 2791 passed, 1 skipped (`suite-002.txt`; 2769 at increment 001 with its folded node + the 22 nodes this increment wrote) |

| Field | Value |
|---|---|
| **RED counterfactual** | the test file and the fixture copied into a scratch worktree at `base_ref` `bdf6e9d`, source untouched: TC-2102 RED — 21 failed, 1 passed (the PRES-V3 board's byte-identity, a regression pin true before the change) · `.dev-flow/2026-10-19-batch-01/evidence/red-002.txt` |
| **Mutation verdicts** | 6 mutants, the selection pre-checked GREEN: N1 a boolean accepted as a rank · KILLED; N2 a None rank written · KILLED; N3 the shown flag read truthy · KILLED; N4 the unranked first · KILLED; N5 the team pull keeps the keys · KILLED; N6 the ranks not from 0 · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-19-batch-01/evidence/mutation-002.txt` (harness `evidence/mutate-002.py`) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate.py` (its pre-check and restore digests, packet 001); its six arms RED above |
| **Emitted-form assertion** | 1 artifact: the board file as written (`json.loads` of the saved bytes, and the bytes themselves for identity) |
| **Reverse census** | 5 probes: B1 `grep -rl "Project.from_dict\|_to_dict\|_PROJECT_KEYS" tests/` → `test_app.py`, `test_palette_ration.py`, `test_sync_fields.py`, `test_cascade.py` — green in `suite-002.txt`; `grep -rn "Project(" taskboard/` → `app.py:2519` (`Project(**data)` from the project editor, whose keys are the editor's own fields — unaffected) and the seed · B2 no file moved · B3 no golden reads a project record · B4 the board file gains two optional keys: readers `Board.load` (this change), `team_sync`'s pull (this change), older app versions (`extra`) · A3 the interface rows amended at ARQ — 0 foreign hits |
| **Correction population** | none — no shipped assertion pinned a project's keys |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-19-batch-01/evidence/suite-002.txt | 76c1a685577f77ba724077634eea99da08cc6b517a631d42fbe72699130e8cca |
| red-002.txt | .dev-flow/2026-10-19-batch-01/evidence/red-002.txt | 8b81d8aa8f723b45039403cbdbed2ea96ef88e30eeec9abf6db1fe5e6fcd3f8d |
| mutation-002.txt | .dev-flow/2026-10-19-batch-01/evidence/mutation-002.txt | f622966339327426ed62a67f6946b7a0aa4936e0a118998927c233f33620be29 |
| mutate-002.py | .dev-flow/2026-10-19-batch-01/evidence/mutate-002.py | abbdacdab99123179b46e997d8a6b39bb92a8f5b28f2e2f1658e82959bd86f9c |

| Field | Value |
|---|---|
| **Evidence files** | 4 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · OK, 0 HIGH, 0 MEDIUM: F1 LOW (`set_present_order` raises on an unknown id — the one caller, increment 004's reorder, passes `present_order`'s ids only; kept), F2 LOW (the existing-project half of the team-pull test is a regression guard only; N5 carries the intent), F3 LOW (a redundant sort term, kept as the LLR spells it), F4 LOW (an archived project keeps a stale rank — recorded in the contract's §6.3) |

## 5 · Risks

An archived project keeps its rank and may tie with another on unarchive (board order breaks the tie; §6.3).

## 6 · Pending items / spec deviations

AT-2102 is owed by increment 004 (it drives the keys 004 binds), as the plan states.

## 7 · Suggested next task

Increment 003 — the view-3 renderer.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 2 source files |
| 2 | Tests in this increment | ✓ | `tests/test_present_all.py` |
| 3 | Layer 0 where it applies | ✓ | the load rule's type table, 18 cases |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b: OK, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt` |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 6/6 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

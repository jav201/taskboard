# Increment 003 — LLR-2205.1 · `creating, editing and archiving boards`

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
> `.dev-flow/2026-10-20-batch-01/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-01` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2205` / `LLR-2205.1` |
| Acceptance | `AT-2205` · white-box `TC-2205` · unit: the name rule and the slug's collisions (Layer 0, `TC-2205`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in a scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

Boards are managed from the home. `n` opens `BoardForm` (`New board`): a name, the eight project colours (`tab`/`shift+tab`, the first colour no active board wears chosen at first) and the file it will create (`~/.taskboard/boards/<slug>/board.json`, cut with `…`); `enter` creates the folder — never one that exists, the slug made unique against the registry and the disk — and an empty board in it (the default phases; the link and milestone migrations marked done and the renumbering notice seen), registers it, closes the home and opens the new board. `e` renames and recolours the cursor's board (the chip follows); `x` asks `Archive <name>? …` with the buttons `Archive` / `Cancel`, archives another board in the registry (its folder untouched) and says so; the open board cannot be archived. A registry that cannot be written is said in a notice at a switch (code review N1/N2 of increment 001), and a rename or an archive that cannot be written says it was not made. The registry reads a `last_opened` with an offset as none (code review F1 of increment 002). `BoardForm` joins the shared modal backdrop.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/boards.py` | source | LLR-2205.1 | `Registry.create`, `edit`, `archive` (each rolled back on a failed save), `next_id`; `_iso_or_none` refuses an offset |
| `taskboard/modals.py` | source | LLR-2205.1 | `BoardForm`, `_home_path` |
| `taskboard/app.py` | source | LLR-2205.1 | `BoardsHome` `n`/`e`/`x` and their callbacks; the `save_error` notice at a switch |
| `taskboard/taskboard.tcss` | source | LLR-2205.1 | `BoardForm` in the shared backdrop rule; the form's box |
| `tests/test_boards_forms.py` | test | HLR-2205, LLR-2205.1 | new: TC-2205, AT-2205 |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ — the registry's writers, the form, its keys on the home and the form's backdrop: the form cannot be reached or seen without the other three (planned so at the PDR) |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_boards_forms.py`; the battery: `python .dev-flow/2026-10-20-batch-01/evidence/mutate-003.py 003`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_boards_forms.py` — TC-2205 (15 nodes), AT-2205 (1) — 16 nodes | in the full suite (`suite-003.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree (`dc643e4` + this increment) | **blocked** — the host stopped the run at ~73% because the machine ran critically low on memory (3.6 GB free of 63.2 GB, other sessions' processes), with 0 failures up to that point (`suite-003-stopped.txt`); not restarted, per the host's instruction. In its place a targeted foreground run: the batch's 4 test files and every shipped file that drives the app, the modals, the key seat, the markup census, the README and the report — 0 failed, 391 passed (`suite-003.txt`). The whole suite is owed at the P4 gate run |

| Field | Value |
|---|---|
| **RED counterfactual** | on `base_ref` `783397e` (the main checkout's `boards.py` moved aside, restored by digest) RED at collection — a RED of absence; on increment 002's commit `dc643e4` (a clean worktree, every node reached): 14 failed, 0 passed (the 14 nodes before the review's two were added) — each node RED for its own reason (no `create`, no `BoardForm`, no `n`/`e`/`x`, the offset accepted) · `.dev-flow/2026-10-20-batch-01/evidence/red-003.txt` |
| **Mutation verdicts** | 20 mutants over 23 arms, one node per arm, each restore proven by digest: `exist_ok=True` · KILLED (the racing-folder arm); the slug ignoring the disk · KILLED; an empty name accepted · KILLED; the 60 cut dropped · KILLED; a reserved name unsuffixed · KILLED; `free_color` always violet · KILLED ×2; `edit` not saving · KILLED (after TC-2205 read the file before the archive — its first run SURVIVED: the archive's save wrote the edit too); the open board archivable · KILLED; the renumbering flag missing · KILLED (AT-2205's settings arm); the button `Delete` · KILLED ×2; the chip not following a rename · KILLED; the colour cycle clamped · KILLED; an offset kept · KILLED; the switch's `save_error` silent · KILLED; a rename's write failure unhandled · KILLED; the code review's F1 and F3: `create` keeping its entry after a failed save · KILLED, `create` leaving its folder · KILLED, `edit` not rolled back · KILLED ×2, `archive` not rolled back · KILLED, the preview's folder not the one created · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-01/evidence/mutation-003.txt` (harness `evidence/mutate-003.py`) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-003.py` (anchors once, edits applied; its draft run saw the `edit` survivor above) |
| **Emitted-form assertion** | 3 artifacts: the created board file (`json.loads` of its bytes: no project, no task, its settings), `boards.json` (its bytes unchanged where nothing may change; `json.loads` of an entry otherwise), the form's lines as Textual holds them (`#bf-path`, `#bf-hues` content) |
| **Reverse census** | 5 probes: B1 `grep -rln "ConfirmModal\|BoardsHome\|taskboard.tcss\|_iso_or_none" tests/` → `test_app.py`, `test_archive.py` (`ConfirmModal`, unchanged — this increment calls it with its existing `confirm=`/`variant=` arguments), `test_boards_home.py` (green), `test_markup_census.py` (the new `notify` calls carry `markup=False`; the form's lines are `Text`) · B2 no file moved · B3 no golden reads the form · B4 a created `boards/<slug>/board.json` (read by `Board.load` — a board with no project opens as today's empty grid) · A3 the interface rows amended at ARQ — 0 foreign hits |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-003.txt | 4379ddfd6b5fa93ce6340bf89fe98dd775eef3b537b5a3237da49a37d8df3b33 |
| suite-003-stopped.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-003-stopped.txt | dae8eafd278c7a2f39026a923c264a9d31e34a567b89a224ebbccdc4c97bdb84 |
| red-003.txt | .dev-flow/2026-10-20-batch-01/evidence/red-003.txt | 8601cb5b0ea3ae8bf1e56d4dc60b6dc06aa4a422ce71ca8e9691d4d6f63992ee |
| mutation-003.txt | .dev-flow/2026-10-20-batch-01/evidence/mutation-003.txt | 09579d4b07257246a6a71224b8027497357f916555b03007481ca0ce4fad5cc0 |
| mutate-003.py | .dev-flow/2026-10-20-batch-01/evidence/mutate-003.py | 74068348fac4f56f0f758fe19676241d67c843bb30e19a2e8a2449eea51014d4 |
| inc003.diff | .dev-flow/2026-10-20-batch-01/evidence/inc003.diff | 12101b9373822b090d075e7936da4314e54ef1b0ab7ff5fe9f556f291bd713cc |

| Field | Value |
|---|---|
| **Evidence files** | 6 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-WITH-NOTES, 0 HIGH open: round 1 (`inc003.diff`) BLOCK-UNTIL F1 — HIGH, `create`/`edit`/`archive` changed the registry in memory before a failing save and never rolled back (the "not created" notice was false); F2 MEDIUM (the payload test could not fail), F3, F4 LOW — all folded; round 2 (`inc003b.diff`): F1 fixed and verified, 4 targeted nodes pass, 23/23 arms killed; LOW notes open: N1 the unused `PAYLOADS`/`Text` in the test file, N2 the test reads Textual's private `_border_title` (the public markup check beside it) |

## 5 · Risks

A name longer than the form's box is cut on the `file` line only; the slug of a name with no ASCII letter is `board` (`board-2`, …).

## 6 · Pending items / spec deviations

The code review's LOW N1 (an unused list and import in `tests/test_boards_forms.py`) is left for a later edit of that file — editing the reviewed set after the verdict would re-open the review for no behaviour.

## 7 · Suggested next task

Increment 004 — moving a project to another board.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ⚠ | §2: 4 source files, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_boards_forms.py` |
| 3 | Layer 0 where it applies | ✓ | the name rule, the slug collisions |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-003.txt` (targeted, 391 passed); the full run blocked by the host's memory reaper — owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 23/23 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

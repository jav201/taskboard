# Increment 001 — LLR-2201.1, LLR-2202.1 · `the boards registry and switching boards in place`

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
> `.dev-flow/2026-10-20-batch-01/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2201`, `HLR-2202` / `LLR-2201.1`, `LLR-2202.1` |
| Acceptance | `AT-2201` · `AT-2202` lands with increment 002 (it drives `B` and the home) · white-box `TC-2201`, `TC-2202` · unit: the registry's load table and the slug (Layer 0, `TC-2201`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in a scratch worktree, ported here after the PDR) |
| Date | `2026-10-20` |

---

## 1 · What changed

The app knows several boards. `taskboard/boards.py` (new, `models` layer) holds the registry `boards.json` beside the default board: `Registry.load` never raises — a missing file is the default board alone (`main`, `Main`), an unreadable one is copied byte for byte to the first free `boards.json.corrupt[-N]` and never rewritten at an opening, and every entry is cleaned and validated (absolute path, no repeated path, a safe id, a name cut to 60, a project colour, an ISO time, `archived` only for `true`); `opening()` passes over a board whose file is missing; `register`, `touch` (written only with more than one board or an existing file) and an atomic `save`; `peek_board` reads a board without ever writing. `__main__.open_app` loads the registry, registers `--board PATH`, picks the board and records it; `main()` runs it (`--report` untouched). `TaskboardApp` takes `registry=` (None → an in-memory registry of its own board, its file beside that board, so the suite never reaches the home folder), its mount runs the per-board start `_open_board()` (the shipped ten steps, the clock interval at mount only) and warns about an unreadable registry or a skipped missing board; `switch_board` loads another board in place, clears the per-board state, stops the old team timer (now kept), reruns the start, and — when the new board's link migration fails — restores the open board as it was. The suite runs under a per-test fake home (`tests/conftest.py`) and the CLI's subprocess tests get one too. Nothing is visible yet: no chip, no home, no key (increment 002).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/boards.py` | source | LLR-2201.1 | new: `Registry`, `BoardEntry`, `slug`, `clean_name`, `registry_path`, `peek_board` |
| `taskboard/app.py` | source | LLR-2202.1 | `registry=`, `board_id`, `_team_timer`; `on_mount` → `_open_board`, `_warn_registry`; `switch_board`; `_migrate_links(at_switch)` |
| `taskboard/__main__.py` | source | LLR-2202.1 | `open_app`; `main()` runs it; `--board`'s help names the registration |
| `taskboard/models.py` | source | LLR-2201.1 | `write_atomic(path, text)` factored out of `Board.save_atomic` (behaviour-identical), shared with the registry's save (code review F2) |
| `tests/test_boards.py` | test | HLR-2201, HLR-2202, LLR-2201.1, LLR-2202.1 | new: TC-2201, TC-2202, AT-2201 |
| `tests/multi_board_fixture.py` | fixture | HLR-2201, HLR-2202 | the round's four synthetic boards and registry, copied from `prototypes/multi_board/fixture.py` |
| `tests/conftest.py` | test | HLR-2201 | the per-test fake home (`Path.home()`), D12 / architect A-32 |
| `tests/test_report.py` | test | HLR-2202 | the CLI's subprocess runs get a temporary `HOME`/`USERPROFILE`; `--report` registers nothing (security S-13) |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ — `models.py` joined at the code review's F2: the registry's atomic save reuses the board's writer instead of a second copy without its guards; the increment cannot shed it without duplicating that code |
| Test files | 4 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_boards.py tests/test_report.py`; the battery: `python .dev-flow/2026-10-20-batch-01/evidence/mutate-001.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_boards.py::test_TC_2201_*` (23 nodes), `test_TC_2202_*` (12), `test_AT_2201_no_registry_and_an_unreadable_one` — 36 nodes | in the full suite (`suite-001.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree (base `ff1f023` + this increment) | 0 failed, 2855 passed (`suite-001.txt`; the ledger 2819 + 36 = 2855) |

| Field | Value |
|---|---|
| **RED counterfactual** | the test files copied into a clean worktree at `base_ref` `783397e` with the main checkout's `taskboard/boards.py` moved aside for the run (the editable install's finder serves a missing module from the main checkout — found while capturing this RED; the first capture, which it fooled, was discarded) and restored by digest `8065378e…09f` = `8065378e…09f`: `tests/test_boards.py` RED at collection (`ImportError: cannot import name 'boards'`) — a RED of absence; the per-arm proof is the battery below · `.dev-flow/2026-10-20-batch-01/evidence/red-001.txt` |
| **Mutation verdicts** | 20 mutants over 22 arms, run one node per arm on this tree, each restore proven by digest: the quarantine skipped · KILLED; `.corrupt` reused · KILLED; a repeated path kept · KILLED; a relative path kept · KILLED; `archived` truthy · KILLED; `touch` writing one board · KILLED; the unreadable file rewritten at the opening · KILLED (after AT-2201 gained its "kept as found" arm — its first run SURVIVED, the predicate was missing); `peek_board` quarantining · KILLED; a missing board not skipped · KILLED ×2; the undo stack kept · KILLED; the team timer not stopped · KILLED; the start not run · KILLED ×2; the interval at every switch · KILLED; a failed migration stopping the app · KILLED; the snapshot not restored · KILLED; a missing file switched to · KILLED; `--board` ignored · KILLED; the registry's save written in place · KILLED; a write failure stopping the start · KILLED; the default board known by its id · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-01/evidence/mutation-001.txt` (harness `evidence/mutate-001.py`) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-001.py` — it asserts each anchor occurs once and each edit changed the file, and its first run reported one SURVIVED arm, so it can see a survivor |
| **Emitted-form assertion** | 2 artifacts: `boards.json` as written (`json.loads` of its bytes; the bytes themselves for the unreadable file kept and the failed swap) and the `.corrupt` copies (their bytes) |
| **Reverse census** | 5 probes: B1 `grep -rln "TaskboardApp(\|on_mount\|set_interval\|_start_team_daemon\|__main__" tests/` → `test_app.py` and 60 app-driving files (unchanged calls: `registry=` is keyword-only with a default), `test_emoji_picker.py` (`TaskboardApp()` with no path — now under the fake home), `test_milestone_offer.py`, `test_setup_help.py` (`on_mount` order — green in the suite), `test_readme.py` (`main()` with `--help` — green) · B2 no file moved · B3 no golden reads the start · B4 `boards.json` is new: readers `open_app` (this change), the home and the move (increments 002, 004) · A3 the interface rows amended at ARQ — 0 foreign hits |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-001.txt | 5cc2cba53fbdb793f06002b4f950b5e94c22aae1efb17e93c62ef9c983cf7e18 |
| red-001.txt | .dev-flow/2026-10-20-batch-01/evidence/red-001.txt | 9f78963a55ba5447b35043d4b537c5510d809c6a379e8e1575c9b6933c746794 |
| mutation-001.txt | .dev-flow/2026-10-20-batch-01/evidence/mutation-001.txt | e0d700ec5e7681e7d52cd7e4a0e14bb27f30d3de8a8541e3e0a8be925748393a |
| mutate-001.py | .dev-flow/2026-10-20-batch-01/evidence/mutate-001.py | 34a3b2d4f04bcf2ef1aafaef2620615564e6125b5541df89993890417b2144d6 |
| premises.txt | .dev-flow/2026-10-20-batch-01/evidence/premises.txt | 49ead02c269a2aa453f75c830072e811d1f1a1af521a65d2b9077ffcaba12c9b |
| suite-base.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-base.txt | 2c968843603d53cafbb6c971342da7030812c13626666259f07e3c7d97332bda |
| suite-seam.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-seam.txt | 35c7949d892eb237a5f5aa2d68f750774956de72097e718296a94dace287fae6 |
| inc001.diff | .dev-flow/2026-10-20-batch-01/evidence/inc001.diff | 4ddf93450482f89b4ac5fa90f432881f0c8b8b00fcc3a671f7b6080bf9acc941 |

| Field | Value |
|---|---|
| **Evidence files** | 8 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-WITH-NOTES, 0 HIGH: round 1 (on `inc001.diff`/`inc001b.diff`) F1 MEDIUM (a registry write failure stopped a start or a switch), F2 MEDIUM (the registry's save duplicated `Board.save_atomic` without its guards), F5 MEDIUM (threshold arms not asserted), F3, F4, F6, F7 LOW — all folded and re-read on `inc001c.diff` (round 2: PASS-WITH-NOTES); round-2 notes N1 (a `save_error` at a switch not shown) and N2 (its notice not asserted mounted), LOW — carried to increment 003, which next changes the registry's writers |

## 5 · Risks

`--board PATH` registers the path, so a copy opened with it joins the boards (README, increment 004); two app instances may both write `boards.json` (last write wins, as with the board file).

## 6 · Pending items / spec deviations

AT-2202 is owed by increment 002 (it drives `B` and the home). `free_color` (LLR-2205.1) lands here, because `register` needs it.

## 7 · Suggested next task

Increment 002 — the chip, the home and `B`.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ⚠ | §2: 4 source files, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_boards.py` |
| 3 | Layer 0 where it applies | ✓ | the load table, the slug, `opening` |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` (absence) + the battery |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt` |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 22/22 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

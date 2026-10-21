# Increment 003 — LLR-2408.1, LLR-2409.1, LLR-2409.2, LLR-2410.1, LLR-2410.2 · `the start-up modals' chip, open twice, --open`

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
> `.dev-flow/2026-10-20-batch-03/03-increments/increment-003.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.


| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-03` |
| Increment | `003` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2408`, `HLR-2409`, `HLR-2410` / `LLR-2408.1`, `LLR-2409.1`, `LLR-2409.2`, `LLR-2410.1`, `LLR-2410.2` |
| Acceptance | `AT-2408`, `AT-2409`, `AT-2410` · white-box `TC-2408`, `TC-2409`, `TC-2410` · unit: the marker reader (`open_elsewhere`: fresh / stale / future / wrong shape / foreign; Layer 0) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in the scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

The boards take the round's items 7, 8 and 9. The milestone offer and the team identity picker open their titles with the board's chip (when the board has one), both titles wrap, and the picker shows `↵ pick   esc cancel`. Each window now keeps a presence marker per open board in `~/.taskboard/open/` (`boards.announce`; renewed every 30 ticks, withdrawn when the board is left or the app exits); opening a board another live window holds shows one warning (`… is already open in another taskboard window (since 09:30). Both save the same file: the last save wins. Close one of them.`, `markup=False`, 30 s); a marker not renewed for 120 s is a dead window's and is removed by the reader after a second `lstat`; the reader is total (any shape, a 4096-byte read) and never follows a link. `taskboard --open PATH` opens an existing board file without registering it: checked before `--report` and before anything is built (a missing path, a folder or a file that is not a board → exit 2, its control characters stripped), the chip `<name> · not listed`, no home at start, a notice, no move out of it; `--open` and `--board` are exclusive.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/boards.py` | source | LLR-2409.1, LLR-2410.1 | `PRESENCE_STALE`, `presence_dir`, `announce`, `renew`, `withdraw`, `open_elsewhere`, `_since`, `_presence_stem`; public `expand_home`, `name_for` |
| `taskboard/app.py` | source | LLR-2408.1, LLR-2409.2, LLR-2410.2 | `_presence`, `_enter_presence` (in `_open_board`), the 30-tick renewal, `on_unmount`; `_label_board`'s unlisted label; `on_mount` without the home for an unlisted board and its notice; `TeamIdentityPicker(roster, self.board.label)` |
| `taskboard/__main__.py` | source | LLR-2410.1 | `--open` (exclusive with `--board`), `_a_board_file` checked before `--report`, `open_app(board, unlisted=None)` |
| `taskboard/modals.py` | source | LLR-2408.1, LLR-2410.2 | the offer's and the picker's chip and wrapping titles, the picker's key line; `ProjectPicker.action_move_board` refuses an unlisted board |
| `tests/test_boards_backlog_round.py` | test | HLR-2408, HLR-2409, HLR-2410, LLR-2408.1, LLR-2409.1, LLR-2409.2, LLR-2410.1, LLR-2410.2 | new: TC-2408, AT-2408, TC-2409 ×2, AT-2409, TC-2410 ×4 (+ parameters), AT-2410 |
| `.dev-flow/2026-10-20-batch-03/evidence/mutate-003.py` | doc | HLR-2408, HLR-2409, HLR-2410 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** — at the cap: the markers live in `models` (`boards.py`), their lifecycle in `app`, the CLI in `__main__`, the titles and the move refusal in `modals`; three items, one per layer, none splittable across fewer files without a layer ban |
| Test files | 1 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_boards_backlog_round.py` (with `NO_COLOR` unset); the targeted set of `suite-003.txt`; `python .dev-flow/2026-10-20-batch-03/evidence/mutate-003.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_boards_backlog_round.py` — 15 nodes: `test_TC_2408_the_titles_open_with_the_chip`, `test_AT_2408_the_start_up_modals_say_their_board`, `test_TC_2409_the_markers`, `test_TC_2409_the_lifecycle`, `test_AT_2409_a_second_window_is_told_once`, `test_TC_2410_open_app_registers_nothing`, `test_TC_2410_open_of_a_registered_path_is_that_board`, `test_TC_2410_a_path_that_is_no_board_is_refused[5]`, `test_TC_2410_open_and_board_together_are_refused`, `test_TC_2410_the_unlisted_board_in_the_app`, `test_AT_2410_open_without_registering` | executed: 916 passed in the targeted run, after the reviews' fixes (`suite-003.txt`) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 002's commit `5d50baa` (a clean detached worktree, the new test file as first written copied in): 14 failed, 0 passed (the arms added after the reviews — the offset `since`, `renew`'s time, the registered path, the notice's markup flag — are proven by their mutation arms M11b–M11d) · `.dev-flow/2026-10-20-batch-03/evidence/red-003.txt` |
| **Mutation verdicts** | 24 arms over 22 mutants, one run, each restore proven by digest: the stale test inverted · KILLED; `abs` dropped (a future time never stale) · KILLED; its own marker counted · KILLED; the name pattern ignored · KILLED; the regular-file check dropped · KILLED; an empty marker left after a failed write (S-7) · KILLED; no presence at opening · KILLED; the marker left at exit · KILLED; the marker left at a switch · KILLED; a gone marker never re-announced · KILLED; the notice parsed as markup (S-1) · KILLED; the `--open` notice parsed as markup (S-14) · KILLED; an offset `since` kept (S-13, code review CR-1) · KILLED; `renew` without the time (CR-2) · KILLED; `--open`'s check removed (S-3) · KILLED ×2; `--open` registering · KILLED ×2; the home over an unlisted board · KILLED; the move out of an unlisted board offered · KILLED; no `not listed` label · KILLED; the offer's chip dropped · KILLED; the app passing the picker no label · KILLED; the picker's key line dropped · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-03/evidence/mutation-003.txt` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-003.py` — increment 001's harness (its RED seen at increment 002: a `CRASH/BAD` node id and a `SURVIVED` arm) with this increment's arms; its first run here printed `GREEN (SURVIVED)` for M11b (the notice's text, not its flag, was read) and `BAD` for M17 (an anchor the review's cleanup moved), both repaired before the recorded run; `arms: 24` |
| **Emitted-form assertion** | 1 artifact: the presence marker — its JSON read back (`since` `2026-10-20T09:30`) and its name matched against the pattern another window reads (TC-2409) |
| **Reverse census** | 4 probes: B1 `grep -rln "open_app\|Registry\|MilestoneOffer\|TeamIdentityPicker\|action_move_board" tests/` → the boards suites, `test_milestone_offer.py`, `test_milestone_offer_seam.py`, `test_team_sync.py`, `test_markup_sites.py`, `test_markup_census.py` — green in `suite-003.txt`; architect A-12's notice census `grep -ln "_notifications\|notify" tests/*.py \| xargs grep -ln "open_app\|TaskboardApp("` → 26 files, all run in `suite-003.txt` · B2 no file moves · B3 no golden capture renders a start-up title or a notice · B4 the marker (above); `boards.json`, untouched by `--open` (AT-2410 compares its bytes) · 0 foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | none — no shipped assertion changed |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-003.txt | .dev-flow/2026-10-20-batch-03/evidence/suite-003.txt | 2ab20b8d0c02ade4c1389233c8f5a9f5bbd90303a035301e111382e17b271eaa |
| red-003.txt | .dev-flow/2026-10-20-batch-03/evidence/red-003.txt | d6c28800ebefe2d690bf690f65a3cc3eed3b2282a3e374cf45cebf22761d0a77 |
| mutation-003.txt | .dev-flow/2026-10-20-batch-03/evidence/mutation-003.txt | 83aebae9dc034a260fe44ba40524996505bdd5c0913227fd9b6d121215f8a85a |
| mutate-003.py | .dev-flow/2026-10-20-batch-03/evidence/mutate-003.py | b22119b8994aedc94b6908d3fc26dcc95d18d416fbbc309a97ac39dd4a2ccd84 |
| inc003.diff | .dev-flow/2026-10-20-batch-03/evidence/inc003.diff | 1b8a80d4e4ec12af94e434df640b7c8959f1b39dabec6d5fe8540815d89e9d77 |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance** after one FIX FIRST: HIGH CR-1 (an offset-aware marker `since` crashed the start's sort) resolved in `_since`, verified on the re-read diff; MEDIUM CR-2 (`renew`'s time untested) asserted, M11d KILLED; LOW CR-3 (the registered path) tested, CR-4 applied, CR-5 noted (§6) · `security-reviewer` — spawned as a generic agent with agents/security-reviewer.md · **APPROVE** · PDR PC-4: S-1, S-2, S-3 discharged in code and TCs (M11, M12, M12b KILLED); S-4..S-8, S-11 verified; LOW S-13 (= CR-1) and S-14 (the `--open` notice's markup test vacuous on Windows paths: now asserts its flag, M11b KILLED) fixed |

## 5 · Risks

A marker outlives a crash for up to 120 s (a false notice); a suspended window stops renewing (no notice); `--open` opens read-write and its start may write the file (§6.3; a read-only `--open` is an OPERATOR item). The black window real Windows Terminal draws on `Personal`/`Course` (D-12) is not this increment's.

## 6 · Pending items / spec deviations

The full suite is owed at P4. TC-2410's bracketed file name is `[x]copy.json`, not the LLR's `[b]x[/b].json` (a `/` cannot be in a Windows file name; code review CR-5). PDR PC-4 (security S-1..S-3 re-read in this code) — see §4b.

## 7 · Suggested next task

Increment 004 — the agenda of every board (HLR-2401), and the docs.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 4 source files, at the cap, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_boards_backlog_round.py` |
| 3 | Layer 0 where it applies | ✓ | the marker reader's branches |
| 4 | RED counterfactual | ✓ | §4, `red-003.txt` |
| 5 | Reverse census | ✓ | §4: 4 probes + the notice census |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-003.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 24/24 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

# Increment 004 — LLR-2401.1, LLR-2401.2 · `the agenda of every board, and the docs`

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
> `.dev-flow/2026-10-20-batch-03/03-increments/increment-004.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-03` |
| Increment | `004` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2401` / `LLR-2401.1`, `LLR-2401.2` |
| Acceptance | `AT-2401` · white-box `TC-2401` (the pure render and the screen) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in the scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

The round's item 1, variant C: `A` opens one read-only screen with every board's week. A lane per active board (registry order) plus a last lane for a board opened with `--open` (its chip's name), a dot per due in each bucket (`LATE`, `TODAY`, each day to Sunday), the chosen bucket's tasks below; `←→` day, `↑↓` task, `enter` opens the task on its board (the agenda and the home popped, `switch_board`, `jump_to`), `esc`/`A` back. Every board is read once, at open (`peek_board`), and nothing is written; the date is read once too (code review CR-3). A missing or unreadable board file is a dim lane with its state. The home's key row names `A all boards`. While the agenda is on the stack, no seat action but `quit` acts. The README, `docs/ARCHITECTURE.md` and `.dev-flow/BACKLOG.md` take the batch's four increments.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/app.py` | source | LLR-2401.2 | `AGENDA_KEYS`, `AllBoardsAgenda`, `action_agenda_all`; `check_action` allows `agenda_all` and holds the seat behind the agenda |
| `taskboard/views.py` | source | LLR-2401.1 | `AgendaItem`, `agenda_buckets`, `all_agenda`, `render_all_agenda` and its helpers; `HOME_KEYS` gains `A all boards` |
| `taskboard/keymap.py` | source | LLR-2401.2 | `Key("A", …, "agenda_all", bar=False)` |
| `tests/test_all_agenda.py` | test | HLR-2401, LLR-2401.1, LLR-2401.2 | new: TC-2401 ×5 nodes, AT-2401 |
| `tests/test_boards_home.py` | test | HLR-2401 | the home's key row compared whole with the round's capture (`A all boards`) |
| `README.md`, `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` | doc | HLR-2401, HLR-2402, HLR-2403, HLR-2404, HLR-2405, HLR-2406, HLR-2407, HLR-2408, HLR-2409, HLR-2410 | the batch's keys, CLI, `open/` folder, module and decision rows, the round's findings logged |
| `.dev-flow/2026-10-20-batch-03/evidence/mutate-004.py` | doc | HLR-2401 | the increment's mutation battery |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** |
| Test files | 2 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_all_agenda.py` (with `NO_COLOR` unset); the targeted set on line 2 of `suite-004.txt`; `python .dev-flow/2026-10-20-batch-03/evidence/mutate-004.py`. By hand: `python -m taskboard`, `A` on the home or the main screen.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| A and B | `tests/test_all_agenda.py` — 6 nodes: `test_TC_2401_buckets_and_dues`, `test_TC_2401_every_row_is_the_width_and_board_text_is_literal[118]`, `[80]`, `test_TC_2401_where_A_acts_and_what_it_holds`, `test_TC_2401_the_unlisted_board_is_the_last_lane`, `test_AT_2401_one_screen_for_every_board` | executed: 654 passed in the targeted run, after the review's fixes (`suite-004.txt`) |
| full suite | owed at the P4 gate run | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on increment 003's commit `b05799c` (a clean detached worktree, the new test file as first written copied in): 5 failed, 0 passed · `.dev-flow/2026-10-20-batch-03/evidence/red-004.txt`; the unlisted-lane node added after the review is proven by arms M12/M13 |
| **Mutation verdicts** | 15 arms, one run, each restore proven by digest: the lane order dropped from the sort · KILLED ×2; done tasks listed · KILLED; Sunday excluded · KILLED; the project column at 80 · KILLED; a missing board's lane not marked · KILLED; `A` refused on the home · KILLED; the seat keys alive behind the agenda · KILLED; the jump never switches · KILLED; the home's key row without `A` · KILLED; the agenda's key row cut at its tail · KILLED; `A` not in the seat · KILLED; the unlisted lane dropped (CR-1) · KILLED; the unlisted lane's jump skipped (CR-1) · KILLED; a failed switch leaves the agenda open (CR-2) · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-03/evidence/mutation-004.txt` |
| **Instrument RED-proof** | 1 instrument: `evidence/mutate-004.py` — increment 001's harness; after the review's CR-5 rewrite its run printed `BAD (anchor found 0 times)` for M10 (the stale anchor), then `GREEN (SURVIVED)` for M10 against the old test (the clipped tail was not read); the test now asserts `read-only` absent at 80 and the recorded run kills it; `arms: 15` |
| **Emitted-form assertion** | 1 artifact: the board files — AT-2401 compares every board file's bytes before and after (the agenda writes nothing) |
| **Reverse census** | 3 probes: B1 `grep -rln "HOME_KEYS\|home_keys\|KEYMAP\|check_action\|SEAT_ACTIONS" tests/` → the home, keymap, help, README and seat suites — all in `suite-004.txt` · B2 no file moves · B3 the home's key-row capture (`test_boards_home.py`) updated to the round's capture, declared in §4 *Correction population* · 0 foreign hits |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | 1 assertion: `test_boards_home.py`'s key row — the constant `KEY_ROW` replaced by the round's approved capture with `A all boards` (LED .7) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-004.txt | .dev-flow/2026-10-20-batch-03/evidence/suite-004.txt | c690205f723a383bb1766d5be291523576a40c32e24b664bdd72704bd86ecef8 |
| red-004.txt | .dev-flow/2026-10-20-batch-03/evidence/red-004.txt | 794b7ace20dc1b3e4939be8590f18a52c20b02aa4f2b883b24e945f958583761 |
| mutation-004.txt | .dev-flow/2026-10-20-batch-03/evidence/mutation-004.txt | 7b14fb718268dac2e95b976a2d5be73f5ebc944eaaa5df67cadb832b6602dba6 |
| mutate-004.py | .dev-flow/2026-10-20-batch-03/evidence/mutate-004.py | a95266cfc8a8f3408a6c31d0e1e18320bc7cd033f54c35163f9b093a3613f756 |
| inc004.diff | .dev-flow/2026-10-20-batch-03/evidence/inc004.diff | 231bd4e748ae78677bf65d5ffb084ff4b2b1768c41aaa48ab2f5537e96a21d9d |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance** (no HIGH) · MEDIUM CR-1 (the unlisted lane and its jump untested) → `test_TC_2401_the_unlisted_board_is_the_last_lane`, M12/M13 KILLED; MEDIUM CR-2 (the missing-file jump did not assert the agenda closed) → asserted, M14 KILLED; LOW CR-3 (the date read in four places) → `self.today` read once; CR-4 (a jump landing silently on an id-less file) → logged in `BACKLOG.md`; CR-5 (the tail found by the string's shape) → a width check; CR-6/CR-7 (the docstring, two ARCHITECTURE rows) → aligned · no `security-reviewer` owed: the agenda only reads (the reviewer's hand-off) |

## 5 · Risks

The lanes are not capped: many boards on few rows hide the selected task (declared limit, in `BACKLOG.md`). The list is ordered by lane, where the round's capture ordered by board name (identical on the fixture). Real Windows Terminal captures of the agenda came out black in this session — see the DDR (PC-5).

## 6 · Pending items / spec deviations

The full suite is owed at P4. LED .7: `agenda_all` is always allowed by `check_action` (a depth guard was unobservable), and the home's row at 80 ends `… A all boards  esc back  q` as the round's capture does.

## 7 · Suggested next task

The DDR, then the P4 gate run.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | `tests/test_all_agenda.py` |
| 3 | Layer 0 where it applies | ✓ | n/a — no pure helper outside the render, which TC-2401 covers |
| 4 | RED counterfactual | ✓ | §4, `red-004.txt` |
| 5 | Reverse census | ✓ | §4: 3 probes |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-004.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 15/15 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 1, declared |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

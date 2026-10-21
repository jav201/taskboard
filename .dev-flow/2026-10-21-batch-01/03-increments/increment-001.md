# Increment 001 — LLR-2501.1, LLR-2501.2, LLR-2501.3, LLR-2502.1, LLR-2507.1 · `the people directory`

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
> `.dev-flow/2026-10-21-batch-01/03-increments/increment-001.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-21-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2501`, `HLR-2502`, `HLR-2507` / `LLR-2501.1`, `LLR-2501.2`, `LLR-2501.3`, `LLR-2502.1`, `LLR-2507.1` |
| Acceptance | `AT-2501`, `AT-2507` · white-box `TC-2501`, `TC-2502`, `TC-2507` · unit: the tokeniser, the handle, the directory's load and writes (Layer 0) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted before the PDR in this worktree, ported here block by block from the frozen draft) |
| Date | `2026-10-21` |

---

## 1 · What changed

The people directory. A new module `taskboard/people.py` in the `models` layer holds `Person` (handle, name, role, note) and `Directory`. The directory is read from `people.json` beside the registry and never raises: a missing, empty or blank file gives an empty directory; an unreadable one is copied aside first. It is written only by `add` and `edit`, as the registry is: under its lock, re-reading the file, atomically. The module also holds the mention tokeniser (`MENTION_RE`, `mention_ids`, `split_mentions`, `mention_line`) and `handle_for`. The link form's name is bounded and the handles are deduplicated in linear time (security S-1, code review CR-1). `Board.people` is a memory-only attribute. The app loads the directory at start, hands its one live dict to every board it opens, and warns once when the file is unreadable. `boards._keep_aside` becomes the public `keep_aside` (architect A-3).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/people.py` | source | LLR-2501.1, LLR-2501.2, LLR-2502.1, LLR-2507.1 | new: `Person`, `Directory` (`load`, `_read`, `get`, `find`, `named`, `_commit`, `_set_aside`, `add`, `edit`), `PEOPLE_NAME`, the caps, `MENTION_RE`, `mention_ids`, `split_mentions`, `mention_line`, `fold`, `handle_for` |
| `taskboard/models.py` | source | LLR-2501.3, LLR-2507.1 | `Board.people = {}` (set by the app, never saved) |
| `taskboard/app.py` | source | LLR-2501.3 | `self.people = Directory.load(...)` in `__init__`; `_label_board` sets `board.people`; `after_move` carries it; `_warn_registry` says an unreadable directory |
| `taskboard/boards.py` | source | LLR-2501.1 | `_keep_aside` → `keep_aside` (public, its docstring generalised; architect A-3) |
| `tests/test_people_directory.py` | test | HLR-2501, HLR-2502, HLR-2507, LLR-2501.1, LLR-2501.2, LLR-2501.3, LLR-2502.1, LLR-2507.1 | new: 45 nodes (TC-2501, TC-2502, AT-2501, AT-2507, TC-2507) |
| `tests/people_round_fixture.py` | test | HLR-2501 | new: the round's synthetic boards and eight people, copied from `prototypes/people_round/fixture.py` so no test imports a prototype |
| `tests/test_boards_concurrency.py` | test | LLR-2501.1 | the monkeypatched name `_keep_aside` → `keep_aside` (the rename, law-driven) |
| `.dev-flow/2026-10-21-batch-01/evidence/mutate-001.py`, `mutlib.py` | doc | HLR-2501, HLR-2502, HLR-2507 | the increment's mutation battery and the batch's runner |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** — at the cap: the new module, the board's attribute, the app's hand-off, and `boards.py` for the public `keep_aside` (A-3); the last could not move to a later increment because `people.py` imports it |
| Test files | 3 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_people_directory.py` (with `NO_COLOR` unset); the targeted set of `suite-001.txt`; `python .dev-flow/2026-10-21-batch-01/evidence/mutate-001.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_people_directory.py` — 45 nodes, among them `test_TC_2501_the_file_is_read_and_bad_entries_are_skipped`, `test_TC_2501_two_windows_never_erase_each_others_people`, `test_TC_2501_a_held_lock_makes_the_write_wait_then_fail_and_change_nothing`, `test_TC_2502_mentions_are_read_at_word_starts`, `test_AT_2501_one_directory_for_every_board`, `test_AT_2507_a_push_carries_mentions_as_handles_and_no_directory`, `test_TC_2507_a_crafted_note_is_tokenised_in_linear_time` | 391 passed with the touched files' suites (`suite-001.txt`: the boards suites, `test_team_sync.py`, `test_markup_census.py`, `test_app.py`) |
| full suite | owed at the P4 gate run (the draft's full run, three chunks, was green: 1398 + 918 + 797 — scratch, not evidence) | not-run |

| Field | Value |
|---|---|
| **RED counterfactual** | on `base_ref` (`taskboard/` at `eac7d42`, this increment's tests copied in): collection error, `ImportError: cannot import name 'people'` — the whole file RED (`red-001.txt`); each assertion's own RED is the battery below |
| **Mutation verdicts** | 17 arms, one run, each restore proven by digest: the re-read under the lock skipped · KILLED; the lock dropped · KILLED; memory held before the write · KILLED; a repeated handle kept · KILLED; the role cap dropped · KILLED; an unreadable file not kept aside · KILLED; the look-behind dropped · KILLED; a handle ending in `.` · KILLED; the taken handle not numbered · KILLED; `_label_board` not handing the directory over · KILLED; the board saving the directory · KILLED; the unreadable notice dropped · KILLED; an empty file reported unreadable · KILLED; the link's name unbounded (S-1) · KILLED; the quadratic dedupe (CR-1) · KILLED; `edit` writing a non-handle (CR-5) · KILLED; a push carrying the directory (team sync's record) · KILLED — arms that stayed GREEN: none (`mutation-001.txt`; its first runs printed SURVIVED for M8 and M11 and BAD for M7: the tests were strengthened — `Ask @ana.ruiz.` and the quoted `"people"` key — and the node id corrected) |
| **Instrument RED-proof** | 1 instrument: `evidence/mutlib.py` (the 2026-10-20-batch-03 runner, unchanged in logic); its RED seen here: a `BAD (anchor found 0 times)` and two `GREEN (SURVIVED)` arms before the fixes |
| **Emitted-form assertion** | 1 artifact: `people.json` — read back as JSON (`version` 1, the ids in order) and by a second `Directory.load` (TC-2501) |
| **Reverse census** | 4 probes: B1 `grep -rln "keep_aside\|_label_board\|after_move\|_to_dict" tests/` → the boards suites (`test_boards*.py`), `test_app.py`, `test_team_sync.py`-adjacent fixtures — rerun in `suite-001.txt`; the private name `_keep_aside` patched in `test_boards_concurrency.py:276` → renamed (law-driven, the only foreign hit); B4 `people.json`, `people.json.lock`, `people.json.corrupt` → read by `Directory` only (`grep -rn "people.json" taskboard/` → `people.py`, `app.py` via `PEOPLE_NAME`); A3 `Board.people` consumed by no module yet (increment 002 draws it) — 1 foreign hit, re-validated |
| **Evidence files** | the table under §4 *Evidence files*: each artifact's path and SHA-256 |
| **Correction population** | none — no shipped assertion changed (the patched name is a rename) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-21-batch-01/evidence/suite-001.txt | 1656e14f731ff122917ada8e9b90c1b776d3086471f5fd984498aff7daaf4dde |
| red-001.txt | .dev-flow/2026-10-21-batch-01/evidence/red-001.txt | 433ad5b0dd0905edfe4b2027faeeccb7342c804a7c0588d216e219fd6a6b16bb |
| mutation-001.txt | .dev-flow/2026-10-21-batch-01/evidence/mutation-001.txt | c903c36c142bfab22b31377add0c936e7d3f9df1d2883bdc86c65654e9025414 |
| mutate-001.py | .dev-flow/2026-10-21-batch-01/evidence/mutate-001.py | 3513464b6fe9f2900f523f6514a5e058c4c8b0aa2dcddc017eba0448001932ff |
| mutlib.py | .dev-flow/2026-10-21-batch-01/evidence/mutlib.py | fe8c686fee4d010d551fa90d95879768dc0b6893637b8a5e25e2c829030a784b |
| inc001.diff | .dev-flow/2026-10-21-batch-01/evidence/inc001.diff | e91cba468748d998cb7f5ab8f040b2848809012d122cfd34501ce8447bbdbbcc |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · **OK to advance**, 0 HIGH; CR-1 (quadratic dedupe) and CR-2 (a wall-clock bound flaky under load) MEDIUM, both fixed (`dict.fromkeys`; CPU time, 2 s, a 40 000-handle craft); CR-3 (the `\xff\xfe` case now bytes), CR-4 (one handle pattern `_H`), CR-5 (`edit` refuses a non-handle; the write-back tested), CR-7 (cleanups) fixed; CR-6 (`Søren` → `s.ren`) recorded as a known limit (§6). `security-reviewer` (PDR PC-2) — spawned with agents/security-reviewer.md · **APPROVE** S-1: re-timed 100 000-character crafts at 0.001–0.033 s per call, `split_mentions` joining back exactly |

## 5 · Risks

A person another window adds shows here after a restart or this window's next write (A-7, accepted). The `.corrupt` copy follows the umask on POSIX, and a file that stays unreadable gets one more copy per start (S-2, S-3, accepted and logged).

## 6 · Pending items / spec deviations

The full suite is owed at P4. `handle_for` splits a word at a letter NFKD cannot fold (`Søren` → `s.ren`, `Łukasz` → `ukasz`; code review CR-6): a known limit, recorded for `BACKLOG.md`. The render-side timing check (`notes_text`, `_card_meta`) lands with them in increment 002.

## 7 · Suggested next task

Increment 002 — how a mention looks (HLR-2506).

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 4 source files, at the cap, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_people_directory.py` |
| 3 | Layer 0 where it applies | ✓ | the tokeniser, the handle, the load's table |
| 4 | RED counterfactual | ✓ | §4, `red-001.txt` and the battery |
| 5 | Reverse census | ✓ | §4: 4 probes, 1 foreign hit renamed |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ⚠ | `suite-001.txt` (targeted); the full run owed at P4 |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 17/17 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4: `people.json` read back |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

# Increment 001 — HLR-2601, HLR-2602, HLR-2603 · `the store and the field`

| Field | Value |
|---|---|
| Batch | `2026-10-24-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2601` / `LLR-2601.1`, `LLR-2601.2`, `LLR-2601.3` · `HLR-2602` / `LLR-2602.1`, `LLR-2602.2` · `HLR-2603` / `LLR-2603.1`, `LLR-2603.2` |
| Acceptance | `AT-2601` (001 arms; the node mints in 003) · `AT-2602` · `AT-2607` (TC arms here; the node mints in 002) — white-box `TC-2601`, `TC-2602`, `TC-2603` |
| Agent | `software-dev` (spawned coder) |
| Date | `2026-10-24` |

## 1 · What changed

Increment 001 ships the milestone-class store and the task field. `taskboard/marks.py` (new): `Mark`, `MARKS_NAME`, `SHAPES` (the eight glyphs of proto.py:85; `◆` stands apart, not a member), `COLOURS` (the round's `SWATCH`, all named tones of `views.HEX`), and `Directory` — `load` never raising (missing/blank → empty silently; unreadable → empty after a `keep_aside` byte copy and a `load_report`), the entry validation (slug id via `people._HANDLE`, unique, named, shape ∈ SHAPES, colour ∈ COLOURS — LED .29/.40, typed fields, `hidden` coerced to bool, one-line whitespace flattening and the 60-char cap via `people._clean`), `find` prefix-only lower case (the round's `find_class`), and `add`/`edit`/`set_hidden` writing as a read-modify-write under `boards.file_lock` through `models.write_atomic`, refilling the one live dict only after a successful write. `taskboard/models.py`: `Task.mark` (read as held, written only when set — the `show_in_present` pattern), `Board.marks` (memory only, never saved). `taskboard/app.py`: the directory loaded beside `people.json`, handed to every board at mount and every switch (`Board.marks` beside `Board.people`), carried through `after_move`, and the once-at-mount unreadable-file notice. Tests: `tests/milestone_marks_fixture.py` (the round's boards + four synthetic classes on the shipped field) and `tests/test_marks_directory.py` (31 nodes / 34 collected arms: TC-2601 load/write arms, TC-2602 round-trip arms, TC-2603 + `test_AT_2602_the_store_is_safe`, the TC-2607 push arm, the LLR-2601.3 hand-off arms incl. the restart).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/marks.py` | source | LLR-2601.1, LLR-2601.2, LLR-2601.3, LLR-2603.1, LLR-2603.2 | the directory |
| `taskboard/models.py` | source | LLR-2602.1, LLR-2602.2 | `Task.mark`, `Board.marks` |
| `taskboard/app.py` | source | LLR-2601.3, LLR-2603.2 | the load, the hand-off, the notice |
| `tests/milestone_marks_fixture.py` | fixture | HLR-2601…2603 | the fixture |
| `tests/test_marks_directory.py` | test | HLR-2601, HLR-2602, HLR-2603 (TC-2601, TC-2602, TC-2603, AT-2602, AT-2607 TC arms, TC-2601-handoff) | 31 nodes |

| Count | Value |
|---|---|
| **SOURCE files** | **3 / 4** (`__main__.py` not needed) |

## 3 · How to test

`env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_marks_directory.py` (34 arms); with the touched existing suites: `tests/test_people_directory.py tests/test_team_sync.py tests/test_sync_fields.py` (`evidence/suite-001.txt`, 145 passed) and `tests/test_boards_move.py tests/test_boards.py tests/test_app.py` (`evidence/suite-001b.txt`, 235 passed · 1 skip — pre-existing and environmental: a clipboard-dependent arm, `Set-Clipboard` ExternalException; skipped identically with the increment stashed).

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0 | `tests/test_marks_directory.py::test_TC_2601_the_file_is_read_and_bad_entries_are_skipped` (the ≥3-branch + boundary unit) | 1 passed (`suite-001.txt`) |
| A and B | the 30 other nodes (TC-2601/2602/2603, `test_AT_2602_the_store_is_safe`, TC-2607) | 33 passed (`suite-001.txt`) |

| Field | Value |
|---|---|
| **RED counterfactual** | `taskboard/marks.py` `_commit`: the on-disk re-read dropped (`fresh = {m.id: m for m in (marks if …)}` → memory only) — the contract's named two-window mutation — made `test_TC_2601_two_directories_on_one_file_both_survive_an_add` fail (the second window erases the first's class) · `evidence/mutation-001.txt` (arm 9) · restore digest `56c8145e0e8ca2c8647d0810ee7b78dea951570e00335124f81413b2ef954b8b` |
| **Mutation verdicts** | 31 arms, one per new node (the unreadable-load node has 4 params): 31/31 KILLED · 0 SURVIVED · 0 CRASH/BAD · every restore proven by hash · `evidence/mutation-001.txt` · arms that stayed GREEN: none |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | none — this increment emits no artifact |
| **Reverse census** | 5 probes: B1 `grep -rl "milestone_tone\|milestone" tests/` — the touched suites re-run (people/team/sync/boards/app, 380 passed); B2 no file moved; B3 no golden capture (`tests/goldens` absent); B4 `marks.json` is consumed by every later start — TC-2603's fresh-home arm; A3 no other module — 0 foreign hits (`grep -rl "MarksDirectory\|board.marks" tests/` → `test_marks_directory.py` only) |
| **Correction population** | none — no correction |
| **Frozen interfaces** | `people.py` untouched; `boards.file_lock`/`keep_aside`, `models.write_atomic`/`clean_strings` called, not edited; the section-3 exclusion sites byte-identical; `Board._to_dict` byte-preservation for all other fields — verified in the diff the code-reviewer reads |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-001.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-001.txt | 382f38d15f25f67d1a55aef5b0dc0eb4ec189e226b16cb8d8f99a167ace58823 |
| suite-001b.txt | .dev-flow/2026-10-24-batch-01/evidence/suite-001b.txt | e5d68ecf3576ebcd52350db97bfb7a09cf5415ff4299e75ce3ac847ca3ef042f |
| mutation-001.txt | .dev-flow/2026-10-24-batch-01/evidence/mutation-001.txt | 83bda4386866b9b64273bf44bd39730065efdee885d1f237ca76d078e18b2d03 |

| Field | Value |
|---|---|
| **Evidence files** | `3 artifact(s), each at the declared home, with the digest of its bytes on disk` |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS, 0 HIGH (F1/F2 LOW notes, no fix owed; the frozen-interface instrument run: people.py, boards.file_lock/keep_aside, models.write_atomic/clean_strings, the exclusion sites incl. app.py:2433, `_to_dict` byte-preservation — all named untouched) · `security-reviewer` for `marks.py` — spawned as a generic agent with agents/security-reviewer.md · PASS (load validation, the keep_aside/atomic/lock windows, the hostile arms, the notice path, no secrets; two LOW hygiene notes, no fix owed) |

## 5 · Risks

`Directory.find` returns `Mark | None` (mirroring the round's `find_class`); increment 004's `matches_m` wiring confirms the shape. The `add`/`edit` shape/colour `ValueError` guards are additive to the spec's letter (a write-boundary guard consistent with the load validation). The two-app restart node runs two sequential `run_test` apps in one test; it passed but is the least conventional pattern in the file. No test leaves a `marks.json.lock`.

## 6 · Pending items / spec deviations

AT-2601's realising node (`tests/test_marks_manager.py::test_AT_2601_a_class_is_created_and_survives`, increment 003) and AT-2607's (`tests/test_milestone_marks.py::test_AT_2607_an_unknown_id_is_safe`, increment 002) mint in their increments (C-18: one node per AT); their store-side arms run here as TC nodes. P4 node-name reconciliation (V-5) for the TC↔AT split. No silent spec edit: all four declared deviations are recorded above and in §5.

## 7 · Suggested next task

Increment 002: `views.milestone_mark` + the 20-site routing with the site-enumeration guard, `views.render_marks`, and `tests/test_milestone_marks.py` minting `test_AT_2607_an_unknown_id_is_safe`; it consumes `board.marks` and `Directory.find` shipped here.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ✓ | §2: 3 source files |
| 2 | Tests in this increment | ✓ | 31 nodes / 34 arms |
| 3 | Layer 0 where it applies | ✓ | §4: the load/skip unit |
| 4 | RED counterfactual | ✓ | §4, `mutation-001.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes |
| 6 | `code-reviewer` passed | ✓ | §4b: PASS, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | §4, the diff |
| 9 | Coverage verified on disk | ✓ | `suite-001.txt`: 34 passed |
| 10 | Load-bearing emptiness | ✓ | no claim rests on an absence |
| 11 | Mutation verdicts | ✓ | §4: 31/31 KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b: code-reviewer + security-reviewer PASS |
| 16 | Evidence files | ✓ | §4: 3 digests |

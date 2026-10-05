# Increment 001 — HLR-505 (LLR-505.1..505.3) + LLR-501.4's `b` · the one-time link migration

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Revision 4
> (frozen r4): code review rounds 1–4 and the security check folded; R2-F1 (a HIGH in tests
> only) fixed under the operator's standing rule with a RED-first proof and re-reviewed.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**.

| Field | Value |
|---|---|
| Batch | `2026-10-04-batch-01` |
| Increment | `001` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-505, LLR-505.1, LLR-505.2, LLR-505.3; LLR-501.4 (the `b` clause, moved here by architect A2-3); LLR-501.1 (`is_open`); amendments A-1, A-2 |
| Acceptance | AT-506, AT-507, AT-508 · white-box TC-514, TC-515, TC-516, TC-518 (migration arm), TC-506 (`b` arm) · unit `migrate_links`, `run_link_migration`, `links_marked`, `_create_beside`, `Board.save_atomic` (layer 0 inside TC-514/515/518) |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-04` |

---

## 1 · What changed

**An existing board now opens with its old `b` links migrated once — a byte-identical backup
first, every change logged, `u` to revert — and `b` marks an outside block only.** The first act
of `TaskboardApp.on_mount` is `run_link_migration`: before the renumber notice or the old-done
sweep can save, it copies the board file's own bytes to `<board file name>.pre-links-migration`
(numbered when taken, exclusive create, never through a symlink), writes
`<board file name>.links-migration-log` (JSON: date, backup name, each change before/after, a
note), applies the legacy rule, sets `settings["migrations"]["links"] = 1` and saves through a
random exclusive temporary file swapped in with `os.replace`. Any failure undoes the in-memory
change, removes the files the run made, leaves the board file untouched and unmarked, and the app
exits printing the reason (a file name, no folder) and the way out. One toast: "Links migrated: N
tasks · backup ‹name› · u undo" (30 s). `u` restores every changed task as one step and keeps the
mark (D-517). A marked or unreadable board is never touched.

The rule (`migrate_links`, pure): dangling, self and repeated ids go; a blocked task whose last
stored id is live and open waits on it and loses the flag (log note: "press b if this was an
outside block", A2-1); last id live but closed → flag kept (D-515); no live last id → flag kept;
other ids to open tasks were released and go; ids to closed tasks stay; any link that would close
a loop over the links already kept goes, a blocker dropped so keeps its flag (D-516). Cost:
one id map, set-based dedupe, a walk back only when a link points at an already-processed task.

`b` (`action_toggle_blocked`) now flips `blocked` and nothing else — no picker, `depends_on`
untouched, one undo step (D-504). `BlockerPicker` is unreachable until increment 003 replaces it.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-505.1, LLR-505.2, LLR-501.1 | `is_open`; `LinkChange`, `LinkMigration`, `links_marked`, `migrate_links`, `_create_beside`, `_set_links`, `run_link_migration`; `Board._serialized` / `save_atomic` (`save` reuses `_serialized`, unchanged behaviour); imports `errno`, `os`, `tempfile` |
| `taskboard/app.py` | source | LLR-505.3, LLR-501.4 | `_migrate_links` as `on_mount`'s first act; the `"migration"` undo entry; `action_toggle_blocked` = flag only; `_on_blocker_picked`, `_on_new_blocker` and the `BlockerPicker` import removed; `Text` imported for the exit message |
| `tests/test_link_migration.py` | test | HLR-505, LLR-505.1, LLR-505.2, LLR-505.3, LLR-501.1 | NEW: TC-514 ×4, TC-515 ×16 (5 parametrized marks, 3 failure arms), TC-516, TC-518, AT-506, AT-507, AT-508 (25 nodes) |
| `tests/test_links.py` | test | HLR-501, LLR-501.4 | NEW: TC-506's `b` arm (1 node; increment 002 extends the file) |
| `tests/kg_board.py` | fixture | HLR-505, HLR-501 | the migration mark on `build()` (the §5 fixture seam, Q-1); `shifted()` (the AT board, Q-3); `LEGACY`, `LEGACY_AFTER`, `LEGACY_CHANGED`, `legacy()` (§5's eight shapes) |
| `tests/test_app.py` | test | HLR-505 | `_mode_board` carries the mark (new-model data; its link fed the `unblock` sort) |
| `tests/test_dependencies.py` | test | LLR-501.4 | AT-D1's two block-flow tests removed (superseded, D-504); the unblock test asserts no screen; `_board` carries the mark |
| `tests/test_markup_sites.py` | test | LLR-501.4 | the `BlockerPicker` arm of AT-401 removed (the picker is unreachable; increment 003 adds the `LinkPicker` arm) |

| Count | Value |
|---|---|
| **SOURCE files** | **2 / 4** |
| Test files | 6 (uncapped; one of them the fixture module) |
| Doc files | 0 (records: `01-requirements.md` amendments A-1, A-2, ledger LED .12, .13, `PLAN.md`, `state.json`) |

## 3 · How to test

```bash
python -m pytest -q -p no:cacheprovider tests/test_link_migration.py tests/test_links.py
python -m pytest -q -p no:cacheprovider          # the gate
python -B .dev-flow/2026-10-04-batch-01/evidence/battery.py .dev-flow/2026-10-04-batch-01/evidence/mutants_inc001_r4.json out.txt   # in an export
```

Manual (synthetic only): build `tests/kg_board.legacy(<tmp>/board.json)`, run
`taskboard --board <tmp>/board.json`: one toast names the backup; `board.json.pre-links-migration`
and `board.json.links-migration-log` sit beside the board; `u` reverts; restarting shows nothing.

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | the migration units inside TC-514 (rule, loop, repeated id, empty), TC-515 (names, marks, failures, symlinks, temp) and TC-518 (cost) | 21 passed (in the 25 below) |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-514 ×4, TC-515 ×16, TC-516, TC-518, TC-506 (`b`) | 23 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-506, AT-507, AT-508 | 3 passed |

Gate run on frozen r4: `python -m pytest -q -p no:cacheprovider` → **2242 passed in 311.84 s, exit 0**
(`evidence/inc001-gate-r4.txt`). Earlier, frozen r2: 2241 passed, exit 0 (`evidence/inc001-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | (a) the base tree (`git archive HEAD`) with this increment's tests; (b) the product battery, 22 mutants (`mutants_inc001_r4.json`) |
| Instrument | `evidence/battery.py` (per-node verdicts, anchor-count check, restore by hash) |
| Where it ran | a scratch export (`git archive HEAD` + the working tree's `taskboard/` and `tests/`), never the working tree |
| Transcript | `inc001-red-on-base.txt`: TC-506 FAILED on base (`b` pushes `BlockerPicker`: `len(screen_stack) == 2`); the base app leaves L2 `(True, ['to1','to2'])`, L3 `(False, ['ta1'])`, no file beside the board; `test_link_migration.py` cannot import `MIGRATION_BACKUP` |
| Restore proven by | each mutant's restore digest in `inc001-mutations-r4.txt` (all `OK`) |
| Bytecode cache | `-B`, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider` |
| Arms resolved at baseline | 26 (25 + TC-506) |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | per mutant, named in the battery file (e.g. M4 reddens only the `True` and `"1"` mark arms) |

| Field | Value |
|---|---|
| **RED counterfactual** | base tree + this increment's tests: TC-506 RED (BlockerPicker pushed), the legacy board untouched by the base app (`evidence/inc001-red-on-base.txt` sha256 `be4114a0c34f2267a79e904f03f62f7b73a883378f49d13fdf3468eed8789a87`); R2-F1's own RED-first proof (`evidence/inc001-r2f1-red.txt`): r1's per-link forward search FAILS the fixed hub-first arm in 18.99 s; restore digests in that file |

| Field | Value |
|---|---|
| **Mutation verdicts** | r4: **22 of 22 KILLED** (`evidence/inc001-mutations-r4.txt`, spec `mutants_inc001_r4.json`): M1 released links kept · M2 D-515 broken · M3 no loop check · M4 loose mark · M5 overwrite a taken name · M6 no rollback · M7 save in place · M8 malformed mark not logged · M9 a team-pull-readable backup name · M10 quadratic dedupe · M11 migration after the renumber save and the sweep · M12 undo one task · M13 no stop on failure · M14 `b` touches `depends_on` · M15 symlink written through · M16 fixed temp name · M17 a failed run leaves files · M18 a repeated id migrated · M19 walk back stops early · M20 dict mark replaced · M21 walk on every link · M22 temp left on failure. History: r1 14/15 (M15 SURVIVED → F3 arm); r2 19/19 (+M6 re-anchored); r3 M9 SURVIVED — it exposed my r3 edit deleting the team-pull arm; restored in r4, KILLED |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| `battery.py` | M15 (r1), M9 (r3) | `SURVIVED` with every node GREEN — the instrument reports a surviving mutant rather than a blanket pass (`inc001-mutations.txt`, `inc001-mutations-r3.txt`) |
| `battery.py` anchor check | M6 / M7 after their code moved | `BAD (anchor found 0 times)` — never counted as a verdict |
| TC-518 | r1's per-link forward search, hub-first | FAILED in 18.99 s (`inc001-r2f1-red.txt`) |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown reporting a failure before its pass was believed (table above) |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the backup file | `backup.read_bytes() == raw` (the board file's bytes read before the start) | equal (AT-506, TC-515) |
| the log file | `json.loads(log)["changes"][*]["task_id"]` == the changed set | `{L1, L2, L3, L5, L7a, L7b}` |
| the saved board | `json.loads(board)` tasks' `(blocked, depends_on)` per shape | §5's table |
| the toast | `str(toast.render())` of each painted `Toast` holds `Links migrated` once | 1 |
| the exit message | the process's stderr, whitespace-normalised | holds "Link migration stopped", "Permission denied", `--board`, no `tmp_path` |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 5 artifacts asserted against their emitted bytes (table above) |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| `inc001-gate-r4.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-gate-r4.txt` | `86427c75f329225221cba18924f61242bfc64f7d4cf8bcfd6dc47d910179a1cf` |
| `inc001-green.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-green.txt` | `8ea58e4bdb560af774fe6ad5aa5932ebc37b3168d85620fa87f7bf3012211b3b` |
| `inc001-red-on-base.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-red-on-base.txt` | `be4114a0c34f2267a79e904f03f62f7b73a883378f49d13fdf3468eed8789a87` |
| `inc001-r2f1-red.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-r2f1-red.txt` | `9c6e84b93531f1d9df5f14afa4fb88f49c5436b37c59b99706bc9b0029cfb233` |
| `inc001-mutations-r4.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-mutations-r4.txt` | `34f9173534d71916e4454e2541da5d1e7bf26ecda83f0d43c4027bf6dfcb17ed` |
| `mutants_inc001_r4.json` | `.dev-flow/2026-10-04-batch-01/evidence/mutants_inc001_r4.json` | `a15312aebce93784cc2ca92f9c4f6ba7fd4587a9a61172ab431497be6224f9d9` |
| `inc001-mutations.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-mutations.txt` | `e9cde1c08a9c20b2dff19df91464134232ecf3e99e5f223ec5f4ace74417358b` |
| `inc001-mutations-r2.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-mutations-r2.txt` | `a61d2eb263ac1a130bb3d146c5d12894d426a6b85d1742d47bdb21f08902153e` |
| `inc001-mutations-r3.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-mutations-r3.txt` | `4afec55c44596b82a031a07f4756d691ff49569635796719a91233b27aa4ff65` |
| `inc001-reverse-census.txt` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-reverse-census.txt` | `918d853cd5866f43877249533160a29949749e0c6d6e6a1a0e712eab09dc148f` |
| `inc001-frozen-r4.sha256` | `.dev-flow/2026-10-04-batch-01/evidence/inc001-frozen-r4.sha256` | `af03fd346233325c5fee30c7b9833492675c638b2984a7ee72381ccbc2d968de` |
| `battery.py` (revised in increment 003 to byte-exact restores; this increment's runs used its first revision, whose bytes were not kept) | `.dev-flow/2026-10-04-batch-01/evidence/battery.py` | `a84222ed67665884e0a77f30fd6d4e91e9785cf4d57030fb006fc8ccc42491cb` |
| `base-suite.txt` | `.dev-flow/2026-10-04-batch-01/evidence/base-suite.txt` | `e81dd09a783c07db8a8aa76e222a936b566c4ccb3e9abcf81884ae5fcc4599ff` |

| Field | Value |
|---|---|
| **Evidence files** | 13 artifacts at `artifact_homes.evidence`, each cited with the digest of its stored bytes (table above); home paths redacted to `<home>` before hashing |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no other app-started test board is changed by the migration" |
| If the result is an ABSENCE, what made the search wide enough | every test file starting `TaskboardApp` crossed with `depends_on` / `blocked=True` / `kg_board` (`inc001-reverse-census.txt`); the only boards with links were `kg_board` (marked), `_mode_board` and `test_dependencies._board` (marked); the rest hold blocked tasks with no link, which the rule leaves |
| Guard labelled as protecting a CONCLUSION, not a behaviour | the full gate run (2242 passed) |
| Conjunctive criteria: one mutation per conjunct | backup (M5, M15), log (M8, M17), apply (M1–M3), mark (M4, M20), atomic save (M7, M16, M22), order (M11), undo (M12), stop (M13) |
| Synthetic instance of the absent case | `kg_board.legacy()` — a board the migration DOES change, AT-506 |
| **Positive control for every probe that returned an ABSENCE** | the first full run with the seam missing on `_mode_board` turned `test_kanban_sort_cycles_and_names_the_mode` RED (P3 run 1, 6 failures, all dispositioned) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | `grep -l` over `tests/` for `toggle_blocked`, `BlockerPicker`, `_undo_stack`, `migrations`, and app-started boards with links (`inc001-reverse-census.txt`) | `test_app.py` (sort fixture marked; undo tests green), `test_dependencies.py` (AT-D1 superseded: 2 nodes removed; unblock test adjusted), `test_markup_sites.py` (BlockerPicker arm removed), `kg_board.py` (marked); all green in the gate |
| B2 file moved on disk | `git diff --name-status HEAD -- taskboard tests \| grep ^R` | 0 |
| B3 byte-identical golden captures this source | `ls tests/goldens` | no such directory |
| B4 artifact produced here is consumed elsewhere | the migrated board file → the next `Board.load`; the backup → the restore path; the log → the reader | AT-506's C-12 chain (a fresh app over the file the first wrote); TC-515's team-pull arm (the shared folder's reader sees no extra member) |
| A3 | interface consumed by another module changed | `grep -rn "save_atomic\|_serialized\|run_link_migration" taskboard` | only `models.py` and `app.py`; `Board.save` unchanged in behaviour |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes run of B1 · B2 · B3 · B4 · A3 with their commands and verdicts: B1 four files touched and green; B2, B3 0; B4 two consumers, each with a node; A3 no new cross-module consumer |

### Correction population — enumerated BEFORE the first site was edited

| Field | Value |
|---|---|
| **Correction population** | 1 correction: "an app-started test board holding a link must be new-model data" — population enumerated by `inc001-reverse-census.txt` (14 files) before any fixture was marked; 3 sites marked (`kg_board.build`, `_mode_board`, `test_dependencies._board`), 11 left (no link, or the migration's own legacy boards) |

### Signed-balance test ledger

`post = base − deleted + added` → `2242 = 2218 − 2 + 26` ✓ reconciles (deleted: AT-D1's two block-flow nodes; added: 25 in `test_link_migration.py`, 1 in `test_links.py`; the `BlockerPicker` arm lived inside the AT-401 node).

---

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · round 1 OK-WITH-NOTES, no HIGH (F1, F2 MEDIUM product; F3–F5 LOW; F6 LOW pending; F7, F8 NIT) → all folded; round 2 BLOCK-UNTIL R2-F1 (HIGH, tests only: TC-518's hub board listed last could not fail; product F1–F5/F8 verified) → fixed under the operator's standing rule for test-only HIGHs with the RED-first proof `inc001-r2f1-red.txt`; round 4 (frozen r4) OK to advance — R2-F1 discharged by re-reading the test, N1 (0600 temp mode on POSIX) and N2 (D-526 margin) LOW, N3 NIT · `security-reviewer` — spawned as a generic agent with agents/security-reviewer.md · PASS-WITH-NOTES then PASS on r3: S-1..S-4, S-11, S-13, S2-1..S2-3, F1, F2 verified by probes; S3-1 MEDIUM (a crash-left temp locked every start) and S3-2, S3-3 LOW folded and verified · no HIGH open |

---

## 5 · Risks

- The migration runs on the operator's real board at the first start after this lands — synthetic boards only were used here (A2); its safeguard (backup by exclusive create, log, atomic save, fail closed, `u`) is what protects it.
- D-515 and D-517 are provisional rulings for the operator; A2-1's case (a flag set after a release to a still-open task) cannot be told apart from data and is flagged in the log.
- A dense rotating board of 800 closed tasks × 400 links migrates in ~1.2 s (bounded 2 s, D-526; margin thin on a slow host, N2).
- POSIX only: the swapped-in board file takes the temporary file's 0600 mode (N1) — folded in increment 002.

## 6 · Pending items / spec deviations

- N1 (0600 mode on POSIX): copy the old file's mode before the swap — increment 002 (`models.py`).
- F6: `BlockerPicker` (`modals.py`) is dead until increment 003 removes it.
- Amendments A-1, A-2 (LED .12, .13): the exit wording, the random temp name, the kept mark keys, D-526.

## 7 · Suggested next task

Increment 002 — the waits-on model, marks and guard (LLR-501.1..501.4, LLR-504.1 minus the project archive).

---

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ✓ | 2 / 4 (§2) |
| 2 | Tests written in this same increment | all | ✓ | 26 new nodes (§2, §4) |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | `migrate_links` (cc > 3), `run_link_migration`, `_create_beside`, `save_atomic`: TC-514/515/518 |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 field; `inc001-red-on-base.txt`, `inc001-r2f1-red.txt` |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 field; `inc001-reverse-census.txt` |
| 6 | `code-reviewer` passed — a HIGH blocks | `core` · `full` | ✓ | §4b: round 4 OK to advance; R2-F1 resolved |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched | all | ✓ | none frozen; `Board.save` behaviour unchanged |
| 9 | Coverage claims verified **on disk** | all | ✓ | `pytest --collect-only tests/test_link_migration.py tests/test_links.py` → 26 nodes named in §2 |
| 10 | Load-bearing emptiness declared | all | ✓ | §4 table |
| 11 | **Mutation verdicts** declared | all | ✓ | 22/22 KILLED (r4) |
| 12 | **Instrument RED-proof** declared | all | ✓ | 3 instruments |
| 13 | **Correction population** declared | all | ✓ | 1 correction, 14 files enumerated |
| 14 | **Emitted-form assertion** declared | all | ✓ | 5 artifacts |
| 15 | **Independent review** names somebody | all | ✓ | `code-reviewer`, `security-reviewer` |
| 16 | **Evidence files** declared | all | ✓ | 13 artifacts with digests |

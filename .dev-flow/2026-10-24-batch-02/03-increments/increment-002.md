# Increment 002 — HD-5 · the directories stay fresh

| Field | Value |
|---|---|
| Batch | `2026-10-24-batch-02` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2706` / `LLR-2706.1`, `LLR-2706.2`, `LLR-2706.3` · `HLR-2707` / `LLR-2707.1` |
| Acceptance | `AT-2706` · `AT-2707` · white-box `TC-2701`, `TC-2702` · `PDR-2026-10-24-batch-02#D3`'s node |
| Agent | `software-dev` (spawned coder sub-agent) |
| Date | `2026-10-25` |

## 1 · What changed

Both directories gain an mtime/size-gated re-read (`Directory.refresh()` → None unchanged / True reloaded / False failed), swapping parsed entries into the live dict in place via the existing `_hold` — the boards hold the same dict object, so every view sees fresh data. The stamp is set at load, after own writes, and advanced even on a failed re-read (a bad file is reported once, not on every open). The app refreshes both directories before the four surfaces build — the task editor (add and edit), `@` (people directory), `#` (marks manager) — and the `/` search through the PDR's one-shot callback, fired the first time the query names `@`/`#`, including an initial query, before the naming keystroke's own frame (`PDR #D3`, condition C4). A failed re-read keeps the in-memory directory and notifies once, `markup=False`, titled `People`/`Marks` (LLR-2707.1).

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/people.py` | source | LLR-2706.1, LLR-2707.1 | `_stamp` + `_stamped()` (`:111`, `:118-123`); `load` converges on one stamped return (`:133-146`); `refresh()` (`:149-167`); `_commit` stamps after the write (`:235`) |
| `taskboard/marks.py` | source | LLR-2706.2, LLR-2707.1 | the byte-level sibling (`:59`, `:66-71`, `:82-95`, `refresh` `:98-116`, `_commit` `:179`) |
| `taskboard/app.py` | source | LLR-2706.3, LLR-2707.1 | `_refresh_directories()` (`:1410-1417`) with the four seats (`:1421`, `:1426`, `:3323`, `:3352`) and the search's `on_directory_query=self._refresh_directories` (`:3308`) |
| `taskboard/modals.py` | source | LLR-2706.3 (PDR #D3) | `SearchPrompt` gains the keyword-only `on_directory_query` (`:2224`), the one-shot `_directory_queried` flag, and `_directories_named()` checked in `on_mount` and `on_input_changed` before each `_draw` (`:2235-2257`) |
| `tests/test_directory_refresh.py` | test | HLR-2706, HLR-2707, LLR-2706.1, LLR-2706.2, LLR-2706.3, LLR-2707.1 | new — TC-2701, TC-2702 (both parametrized over people/marks), AT-2706, AT-2707, and `test_D3_the_search_query_refreshes_the_directories_once` |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** — ⚠ the commission named three (`people.py`, `marks.py`, `app.py`); the fourth is `modals.py`, the PDR-#D3 search seat's home: the callback must live where the query is read, and no smaller cut exists. The reason is declared here per the cap's warning rule. |

No pre-existing test was touched; the one RED seen during the work (`test_TC_2505`'s lone-`@` empty frame when the callback skipped a draw) was a defect in the first cut of the new code, fixed in it — not a weakened assertion.

## 3 · How to test

`env -u NO_COLOR python -m pytest -q tests/test_directory_refresh.py tests/test_people_search.py tests/test_home_deferred_start.py tests/test_people_directory.py tests/test_people_view.py tests/test_marks_manager.py tests/test_marks_directory.py tests/test_modal_keys.py tests/test_boards_home.py tests/test_boards.py tests/test_boards_backlog_round.py tests/test_all_agenda.py`

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0/unit | `tests/test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size[people|marks]` — unchanged → None / same dict / 0 parses · same-size edit + moved mtime → True / 1 parse · size-only change with frozen mtime → True | 2 passed (`suite-002.txt`) |
| 0/unit | `::test_TC_2702_a_failed_refresh_keeps_and_flags_once[people|marks]` — corrupt → False + kept · again → None (stamp advanced) · fixed → True | 2 passed |
| B | `::test_AT_2706_the_directories_stay_fresh` — the other window's `Directory` adds a person and a class; `@`, `#`, the editor's `alt+m` Select, and the `/` `@` completion all name them | 1 passed |
| B | `::test_AT_2707_a_failed_re_read_keeps_the_directory` — exactly one `People` warning (`warning`, `markup=False`), the directory kept, no re-notify while the file stays bad | 1 passed |
| B | `::test_D3_the_search_query_refreshes_the_directories_once` — the callback fires once, incl. an initial `@`/`#` query, before that frame draws | 1 passed |
| regression pin | the 12 named suites (incl. all of increment 001's) | 276 passed, 0 failed (`suite-002.txt`) |

P4's expected-new-node count is **11** (6 of increment 001 + 5 here, counting the parametrized TCs as one node id each); the suite baseline 3235 + 11 = 3246 collected.

| Field | Value |
|---|---|
| **RED counterfactual** | mutant E5 of `mutation-002.py` — the app's `if directory.refresh() is False:` → `if False:`, the pre-HD-5 shape in which the seats never re-read — made `test_AT_2706_the_directories_stay_fresh` fail (the fresh person never appears; the P1 probe's exact RED, `evidence/red-p1.txt`) · `evidence/mutation-002.txt` |
| **Mutation verdicts** | 30 arms, 0 CRASH/BAD, per-arm verdicts in `mutation-002.txt`: E1 (no mtime gate) KILLED by TC-2701, TC-2702, AT-2707 · E2 (the size arm dropped) KILLED by TC-2701 · E3 (failure empties the dict) KILLED by TC-2702, AT-2707 · E4 (no stamp advance on failure) KILLED by TC-2702, AT-2707 · E5 (seats never refresh) KILLED by AT-2706, AT-2707 · E6 (the callback on every keystroke) KILLED by the D3 node — every PDR §5/C4 named mutation KILLED on its target; survivals are the correct cross-products |
| **Instrument RED-proof** | none — no instrument beyond the suite |
| **Emitted-form assertion** | none — this increment emits no artifact |
| **Reverse census** | 5 probes, B1-driven: B1 `grep -rln "refresh\|_stamp\|on_directory_query" tests/` → `tests/test_directory_refresh.py` only · B2 no file moved · B3 no golden capture · B4 no artifact another component consumes · A3 no consumed interface re-signed (`SearchPrompt`'s new parameter is keyword-only with a None default — additive) — 0 foreign hits |
| **Correction population** | none — no correction |
| **Where it ran** | the orchestrator's own tree, no other session reading; every arm restored its file and proved the restore by hash (`before:`/`after:` pairs in the transcript) |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite run | `.dev-flow/2026-10-24-batch-02/evidence/suite-002.txt` | `666ddfd77fd314eb72b3c1d6cd6a8c86a85fe842d555ff585c271df702321c02` |
| RED capture + battery | `.dev-flow/2026-10-24-batch-02/evidence/mutation-002.txt` | `3ce1d17b5ed4d159b27d9534b40b6a5762c1ebc84e68962d146273f6b6119b0b` |
| the battery runner | `.dev-flow/2026-10-24-batch-02/evidence/mutation-002.py` | (the instrument, runnable) |

| Field | Value |
|---|---|
| **Evidence files** | 2 transcripts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with `agents/code-reviewer.md` · **PASS, 0 HIGH** (two LOW notes: F1 the marks-side notice arm — shared-line covered, disclosed in §5; F2 the `#` arm of the search predicate precedes `#` filter support — harmless, named) |

## 5 · Risks

The `#` half of the search seat has no named assertion (P2 round-2 minor m9, named open): the re-read call is shared per seat, the `@` arm covers the wiring, and the `#` manager/editor arms cover the marks directory. The stamp's ns-resolution mtime pair makes same-instant same-size writes from another process vanishingly unlikely; a miss costs one stale open, not data. `Directory.refresh()` during `_commit`'s locked write is never concurrent (same thread).

## 6 · Pending items / spec deviations

One node beyond the contract's named set: `test_D3_...` implements PDR condition C4's predicate pin (initial-query firing, once-only, draw ordering) — named with the PDR id in the house style; no new TC id minted. Nothing else pending.

## 7 · Suggested next task

The DDR, then P4.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ⚠ | §2: 4/4 with the declared reason (the PDR-#D3 seat) |
| 2 | Tests in this increment | ✓ | §4: 5 new node ids (7 with parametrization) |
| 3 | Layer 0 where it applies | ✓ | TC-2701/TC-2702 — the gate's three arms per directory |
| 4 | RED counterfactual | ✓ | §4, E5 transcript (mirrors `red-p1.txt`) |
| 5 | Reverse census | ✓ | §4: 5 probes, 0 foreign hits |
| 6 | `code-reviewer` passed | ✓ | §4b: PASS, 0 HIGH |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen; the SearchPrompt change is additive |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt`: 276 passed |
| 10 | Load-bearing emptiness | ✓ | TC-2702's second beat pairs the silence with the notice's presence |
| 11 | Mutation verdicts | ✓ | §4: 30 arms, targets KILLED |
| 12 | Instrument RED-proof | ✓ | §4: none, declared |
| 13 | Correction population | ✓ | §4: none, declared |
| 14 | Emitted-form assertion | ✓ | §4: none, declared |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: 2 digests |

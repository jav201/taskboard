# Design proposal — taskboard — Batch 2026-10-24-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Design proposal` · `7 · Forward-applicability table` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.

> **Owed in.** `core` by trigger · `full` ✓

> **Where this lives: the VAULT + Drive**, not the repo — it is deliberation, and its traceability to
> code is weak. It is **cited by id** from the repo (`PDR-<batch_id>#D<n>`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.**

| Field | Value |
|---|---|
| Id | `PDR-2026-10-24-batch-02` |
| Requirements covered | `HLR-2701 v2 · HLR-2702 v2 · HLR-2703 v1 · HLR-2704 v1 · HLR-2705 v1 · HLR-2706 v2 · HLR-2707 v1 · HLR-2708 v2` (v = the post-P2-refinement revisions; LLR-2701.1..LLR-2708.2, LLR-2702.4 included) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `app` (app.py) · `models` (people.py, marks.py) · `modals` (modals.py — the SearchPrompt seat only) |
| Triggers that fired | `A2` (takes ARQ, PDR, DDR up) · `B1` (reverse census) · `D1` (interaction) |
| Author / reviewers | author: the orchestrator · reviewers: `architect` (this PDR) · `qa-reviewer` + `ux-reviewer` at the DDR (the operator's roster) |

---

## 1 · Objective and scope

Two defects of the start-with-home, per the approved contract:

1. **The deferred start (HD-1..HD-4).** With the home shown at start, the default board's start — link migration, renumbering notice (a writer), old-done sweep, presence marker + the open-twice notice, team-mode start, the milestone offer — must not run and no board file may be written until the user leaves the home onto a board. Leaving runs it exactly once (a started-board record); the single-board and `--open` mounts keep today's full start at mount; `B`'s home pops back to an already-started board.
2. **The fresh directories (HD-5).** `people.Directory` and `marks.Directory` gain an mtime/size-gated re-read swapped into the live dict in place; the app runs it at the four open seats (the task editor, `@`, `#`, and the `/` search when its query names `@`/`#`); a failed re-read keeps the in-memory directory and notifies once, `markup=False`.

What this design will NOT do: change any modal body, the notice's wording, the migration/sweep/presence/offer logic, the home's cards or keys, the team sync, or any behaviour on the single-board / `--open` / later-`B` paths. No UI change beyond the two defect fixes.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `app` (`app.py`) | the started-board record; the split of the mount/start into a read-only mount half and the deferred writers; the four re-read seats and the refresh-failure notices | `TaskboardApp._started_board` (internal), `_mount_board(at_mount)`, `_refresh_directories()` (internal) | the directories' parsing (that is `models`); the search prompt's widgets |
| `models` (`people.py`, `marks.py`) | `Directory.refresh()` on both directories: stat mtime_ns+size against the last-read stamp; re-parse via the existing `_read` only on change; swap via the existing `_hold` (in place, so the boards' live dicts update); stamp updates on load, on own writes, on a failed re-read (so a bad file is not re-parsed and re-notified on every open) | `Directory.refresh() -> None \| True \| False` (unchanged / reloaded / failed — additive, consumed only by `app`) | notifying (the app owns the user-facing notice) |
| `modals` (`modals.py`) | `SearchPrompt` gains one optional keyword callback, invoked the first time the query names `@` or `#` | `SearchPrompt(..., on_directory_query=None)` — additive, keyword-only, default None | the directories (it receives the live Directory object as today) |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ — all three modules are declared owners of exactly these surfaces; the amendment batch-02 already made (people/marks re-read exposed, app owns the seats) is the map this design implements.

## 3 · Diagrams

Interaction (the only viewpoint that applies):

```
start, ≥2 boards                start, 1 board / --open
─────────────                   ─────────────────────────
on_mount                        on_mount
 ├─ push BoardsHome             └─ _open_board(at_mount=True)   ← unchanged (HD-4)
 ├─ _mount_board()  (read-only)      ├─ migrate → renumber → sweep
 └─ _warn_registry()                 ├─ _mount_board()
                                     ├─ presence → team → offer
BoardsHome                          └─ record := board_id
 ├─ enter on a card → pop → switch_board(bid)
 │    └─ bid == current and start pending → _open_board()   (LLR-2702.3)
 ├─ esc/back → pop → _open_board()  (no-op when started)
 └─ q → quit, nothing written
```

State (the record): `_started_board: str | None` holds a BOARD KEY, written ONLY on a completed start (the migration gates the rest, so a failed start has no partial writers to double-run). The key is `board_id` for a listed board and `unlisted:<resolved path>` for an `--open` board — so the guard answers both, and `B` → `esc` over an already-started `--open` board (reached because `action_boards` pushes the home unconditionally) is a no-op, as HLR-2708 pins. On `switch_board`'s failure restore, the record names the board that came back (its key): the restore writes it back to the previously started board's key — under write-at-completion it already holds it, so the invariant is "after the restore the record names the board that came back".

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `people.Directory` / `marks.Directory` | `load`, `find`, `add`, `edit`, (`set_hidden`) | + `refresh()` | `app._refresh_directories()` only | n/a — one lane, no fork |
| `TaskboardApp._open_board` | the full start, unguarded | the same body with the record guard at entry and the record write at completion | `on_mount`, `switch_board`, `BoardsHome` | n/a |
| `TaskboardApp._mount_board` | — (new, extracted from `_open_board`'s read-only middle) | select first, refresh, clock settings, the one shared interval (at mount), rescue notice — called by `_open_board` in TODAY's position (after the sweep), and by `on_mount`'s home branch alone | `on_mount` (home branch), `_open_board` | n/a |
| `SearchPrompt.__init__` | `(title, initial, placeholder, *, people, open_person)` | + `on_directory_query=None`, invoked ONCE the first time the query names `@` or `#` — including an `initial` query that already names one (a reopened filter), and before the `_draw` that shows the naming keystroke's own frame | `app.action_search` | n/a |

No consumed interface is re-signed (trigger A3 stays not fired); every change is additive or internal to `app`.

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| AT-2701 | B | at the start home: 0 open-twice notices, 0 own markers, default board bytes unchanged (foreign marker + sweepable task planted) | restore the mount-time `_open_board(at_mount=True)` call — the notice/marker/sweep all fire at mount (the P1 probe's RED, `evidence/red-p1.txt`) |
| AT-2702 | B | `enter` on the default card: notice once, marker written, sweepable task archived | drop the record write at `_open_board`'s completion → the start re-runs on the later `B`/`esc` (double notice) |
| AT-2703 | B | `esc` runs the start once; `B` then `esc` re-runs nothing | make `action_back` pop without `_open_board()` → the start never runs (board unstarted, no marker) |
| AT-2704 | B | picking the second board starts it and the default file is byte-identical | run the deferred start for the default at mount (the pre-HD-1 shape) → the default is swept/renumbered and its bytes move |
| AT-2705 | B (`milestone_offer` seam marker) | the offer is not on the stack while the home is up; after `enter` it is the top screen with the board beneath | push the offer at mount (the pre-HD-1 shape) → the offer sits over the home |
| AT-2706 | B | a person/class another `Directory` wrote appears in the people view, the `#` manager, the editor's `alt+m` Select, and the `/` `@` completion | make `refresh()` a no-op (return None always) → every surface stays stale |
| AT-2707 | B | an unreadable re-read keeps the directory, exactly one `markup=False` warning, no re-notify while the file stays bad | let a failed re-read clear the dict → the directory empties; or notify per open → two notices |
| TC-2701 | 0/unit | the gate: unchanged file → same dict, 0 parses; mtime move (same size) → 1 parse, new entry; size move → 1 parse | drop the size arm (mtime only) → the size-only mutant survives; cache forever → the mtime mutant survives |
| TC-2702 | 0/unit | a failed parse keeps the entries and reports False once | (a) report True on failure → the once arm inverts · (b) clear the dict on failure → the keep arm inverts |
| TC-2703 | A | a forced migration failure on the deferred start: record pending, board view beneath, one notice, `B`/`esc` retries exactly once | write the record before the migration → the retry is swallowed (spy count 1) |

**Declared here, at authoring time.** The mutation of TC-2701's third arm is the notable one: a size-only change with a preserved mtime is the gate's blind side and gets its own arm (LLR-2706.1's boundary class).

## 6 · Risks and rejected alternatives

Risks carried into the increments: (R1) the record's restore interplay — `switch_board`'s failure restore must leave the record naming the board that came back (increment 001, TC-2703's arms); (R2) the sweep lands under a view refreshed only when `_mount_board` keeps its today-position inside `_open_board` (increment 001 states the call order in its packet).

| Alternative considered | Why it was rejected |
|---|---|
| Defer the start by not LOADING the default board at mount (build it lazily on pick) | `self.board` backs the home's own card, the chip, `B`'s home and the `--open` notice; lazy loading re-touches every reader. The defect is the start's writers, not the load. |
| A per-board started SET instead of the single record | Only the current board can ever be pending (a cross-board `switch_board` always runs the full start); a set adds bookkeeping with no case to answer. |
| Re-read the directories on a timer / file-watch instead of at the open seats | The commission names the four open seats; a timer adds a live notice source and surprise refreshes mid-edit. Open-time re-reads are the cheapest correct freshness. |
| Re-read on EVERY `/` open (unqualified) | The contract binds the search seat to queries that name `@`/`#` (P2 round-1 fold); an unqualified refresh contradicts LLR-2706.3 as amended. |
| Notify on every open while a re-read keeps failing | HD-5 says "notifies once"; the stamp advances on a failed re-read so a bad file is reported once and then left alone until it changes again. |

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics (the record, the split, `_mount_board`, `refresh()`, the search callback, the stamp semantics) | the Phase-3 increments | increment 001's and 002's packets §1; the implementer sub-agent's brief |
| enablers (the sweepable-default and planted-foreign-marker helpers, the second-`Directory` "other window" pattern, the `milestone_offer` seam marker on AT-2705) | Phase 3 and validation | the AT/TC nodes of `tests/test_home_deferred_start.py` and `tests/test_directory_refresh.py` |
| proposed test cases (the table above, each with its reddening mutation) | layers 0/A/B, and the DDR | §5 of this proposal → the packets' §4 → the DDR's review of observability |
| design → requirement traceability | the matrix and the DDR | §1/§2 here name the LLRs each characteristic implements; the DDR re-reads it |

## 8 · Parallelisation plan *(only if the batch forks)*

Not parallelised — one lane (the declared empty stands in the contract's §2.8; the two increments run sequentially and both touch `app.py` in sequence).

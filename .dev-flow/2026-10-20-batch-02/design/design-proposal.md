# Design proposal — taskboard — Batch 2026-10-20-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Design proposal` · `7 · Forward-applicability table` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **Why a HEADING is reserved here and a FIELD NAME everywhere else:** `C-49`'s artifact is the §7 TABLE, and a rule that read a summary bullet instead of the rows would be reading a claim about the table rather than the table. `V52` therefore keys on this document's own H1 and on the §7 heading, which is why both are on the machine plane. **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`.

> **Owed in.** `core` by trigger · `full` ✓
> **Source:** `/dev-flow-init` step 4's seed-by-level table, which is this fact's one home. A level marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Where this lives: the VAULT + Drive**, not the repo — it is deliberation, and its traceability to
> code is weak. It is **cited by id** from the repo (`PDR-<batch_id>#D<n>`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-20-batch-02` |
| Requirements covered | `HLR-2301 v1 · HLR-2302 v1 · HLR-2303 v1 · HLR-2304 v1 · HLR-2305 v1 · HLR-2306 v1 · LLR-2301.1 · LLR-2301.2 · LLR-2302.1 · LLR-2303.1 · LLR-2304.1 · LLR-2305.1 · LLR-2306.1 · LLR-2306.2` |
| Modules touched (from `docs/ARCHITECTURE.md`) | `models` (`taskboard/boards.py`) · `modals` (`taskboard/modals.py`) |
| Triggers that fired | `A2 · A3 · B1 · B4 · C5 · C6 · D1 · E1` |
| Author / reviewers | `architect` · `qa-reviewer` · `ux-reviewer` (D1) · `security-reviewer` (C5, C6) |

---

## 1 · Objective and scope

The non-visual backlog items of `01-requirements.md` §1.1, in three increments on one branch (`fix/backlog-boards`, one lane):

- **001 — `boards.py` (HLR-2301, HLR-2302, HLR-2303, HLR-2305).** `LOCK_WAIT`, `LOCK_STALE`, `file_lock` (LLR-2301.1); `Registry._read` split out of `load`, `Registry._commit` / `_adopt` / `_carry`, and `register` / `create` / `edit` / `archive` / `touch` rewritten as changes applied inside `_commit` (LLR-2301.2); `move_project` takes `file_lock(dst.path)` around the stale-plan check … target save (LLR-2302.1) and backs up `history.jsonl` with the board files (LLR-2303.1); `_expand_home` at `_key`, `_read` (the stored path normalised) and `register` (LLR-2305.1); the stopped-move notice keeps its backups sentence only after a backup (`modals.ProjectPicker._move_confirmed`, ux UX-2) and `__main__.main` exits with the busy message (ux UX-4). 3 source files (`boards.py`, `modals.py`, `__main__.py`); tests in a new `tests/test_boards_concurrency.py`.
- **002 — `modals.py` (HLR-2304, HLR-2306 code half).** `_do_archive_toggle` ranks an unarchived project after the last shown rank (LLR-2304.1); `_move_target(proj, bid)` (LLR-2306.1). 1 source file; tests in `tests/test_present_all.py` (TC/AT-2304) and the signature arm in the new `tests/test_hygiene.py`.
- **003 — tests only (HLR-2306 test half, LLR-2306.2).** `tests/test_boards_forms.py`, `tests/test_boards_home.py` (AT-2204), `tests/test_present_all.py` (AT-2104, AT-2106, AT-2102), `tests/test_hygiene.py` (AT-2306 complete). 0 source files.

Out: any new notice, screen or key; a lock on plain board saves or on the move's source; `~user`.

## 2 · Modules and boundaries

| Module | Change | Boundary moved? |
|---|---|---|
| `models` (`boards.py`) | `file_lock` joins the module's exposed interface (consumed inside the module and by tests); the `Registry` writers keep their signatures and change their contract (read-modify-write, adoption in place); `move_project` keeps its signature | no — `docs/ARCHITECTURE.md` §4 rows amended (the ARQ amendment) |
| `modals` | `ProjectPicker` internals only (`_do_archive_toggle`, `_move_target`) | no |

No new import edge: `boards.py` adds `contextlib`, `time` (stdlib).

## 3 · Diagrams

```
registry write (any instance)              move (target side)
  change requested                            refusal check (no lock)
    └─ mkdir registry folder                  └─ file_lock(target)  ── busy > LOCK_WAIT → OSError, nothing written
       └─ file_lock(boards.json)                 ├─ stale-plan check (mtime, size)
          ├─ fresh = _read(file) | copy(self)    ├─ backups: board.json ×2, history.jsonl
          ├─ change(fresh)                       ├─ build copies, save target
          ├─ fresh.save()  (atomic)              └─ release
          └─ release                           save source, images, history lines, logs (unlocked, as before)
       └─ adopt fresh into self (entries updated in place)
```

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| `boards.file_lock`, `LOCK_WAIT`, `LOCK_STALE` (new) | — | as LLR-2301.1 | `Registry`, `move_project`, tests | no — one lane |
| `Registry.register/create/edit/archive/touch` | write `self` whole | read-modify-write under the lock, adopt in place (LLR-2301.2) | `app.BoardsHome` (create, edit, archive), `app.TaskboardApp.switch_board` (touch), `__main__.open_app` (register, touch), tests | no |
| `Registry.save` | the atomic write | unchanged (the commit's last step) | tests that patch it (`tests/test_boards_forms.py::test_TC_2205_a_failed_registry_save_changes_nothing`) | no |
| `move_project` | backups, then saves | + the target lock and the history copy (LLR-2302.1, LLR-2303.1) | `modals.ProjectPicker`, tests | no |
| `ProjectPicker._move_target` | `(proj, bid, _boards)` | `(proj, bid)` | its own callback | no |

## 5 · Proposed test cases

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-2301 | 0/A | `file_lock` (exclusive, released on exit and on an exception, busy past `LOCK_WAIT`, stale taken over, fresh not); two stale registries interleaving every writer → nothing lost, entries adopted in place, ids picked fresh, a failed save changes nothing and removes `create`'s folder, an unreadable file at commit copied aside, a one-board `touch` with no file takes no lock | `O_EXCL` dropped; the `finally` unlink removed; the stale test inverted; `_commit` writing `self` instead of `fresh`; adoption replacing objects; the copy-aside skipped |
| AT-2301 | B | the app's `B`, `n` after another registry created a board → both on disk and both cards; a held lock → the create notice names `boards.json` as busy, nothing written | `_commit` writing `self`; the lock skipped |
| TC-2302 | 0/A | the target lock held → `OSError`, `.steps == []`, both folders' hashes unchanged; the lock present during the target's save and gone during the source's; a stale lock taken over | the lock removed from `move_project`; the release moved after the source save |
| AT-2302 | B | the move's `enter` with the target locked → the move's notice says busy, both files and folders unchanged, the test's lock left in place; unlocked → the move done, no lock left | the lock removed |
| TC-2303 | 0/A | the copy's bytes, its step, `-2` on a second move, no history → no copy, a failing target save → the copy exists | the `_backup(history)` call removed; moved after the rewrite |
| AT-2303 | B | the move by keys keeps `history.jsonl.pre-move-2026-10-20` with the undecodable byte | the copy removed |
| TC-2304 | A | the unarchive rank rule's four cases through `ProjectPicker` | the rank kept; archived ranks counted; its own rank counted |
| AT-2304 | B | `P` `x`, `R` `3` reorder, `P` `x` again, `R` `3` → the unarchived project listed last, ranks distinct | the rank kept |
| TC-2305 | 0 | `_expand_home`'s forms with the environment's home elsewhere; `entry_for` and `register` under `Path.home()` | `expanduser` back at `_key`, `load` or `register` |
| AT-2305 | B | a `~` board opened from the home is the seam home's file, not the environment's | `expanduser` back at `_key` |
| AT-2306 | law | `_move_target`'s signature; no `._border_title` in `tests/`; every module-level name of `tests/test_boards_forms.py` read | the parameter back; `PAYLOADS` back |
| LLR-2306.2 nodes | B | AT-2204 (`B` in the help's keys, `R` by keys), AT-2104 (the cursor's `⟦` row), AT-2106 (`u` in view 2), AT-2102 (the rail's `▶` row) | `B` dropped from the help; the cursor drawn elsewhere; `u` unbound in view 2; the rail cursor moved |

**5b · The gauntlet controls that apply, and who pays:** C-40 (each new assertion RED on `base_ref` — a clean worktree at `b1b71e4` — or by a recorded mutation; the orchestrator, `mutate-00N.py` beside its transcript); C-19 (one complete run per gate; the whole suite in three sequential chunks at P4 — the host's memory, the commission); C-42 (the ATs read the notices, the frames and the files); B1's reverse census in each packet (`tests/test_boards.py`, `tests/test_boards_forms.py`, `tests/test_boards_move.py`, `tests/test_present_all.py`, `tests/test_archive.py`).

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| `msvcrt.locking` / `fcntl.flock` | two platform paths; a byte-range lock cannot be inspected for staleness; the commission asks stdlib, Windows-safe and a stale lock that never blocks |
| merging whole registries (union of both sides' entries) | an id collision would rename an entry the app already holds by id (`board_id`); the one-change replay keeps every other writer's change and touches only its own |
| replacing `self.entries` with the fresh objects | `BoardsHome` holds entry objects across an edit (`_paint` after `_edited`); in-place adoption keeps them live |
| a lock on every `Board.save` | every save of every board would take a file lock (the suite saves thousands of times); out of the commission's scope |
| a pid in the lock file and a liveness check | `os.kill(pid, 0)` is not a liveness probe on Windows; the age rule is enough for a lock held milliseconds |
| always re-ranking an unarchived project last | an archive undone at once would move the presenter's first project to last (ux UX-1); the rank is changed only on a tie |
| ranking an unarchived project 0 when no other is ranked | it would jump ahead of every unranked project |
| a pid in the lock and a liveness probe instead of the token | not portable to Windows; the token makes the release owner-safe, the age rule covers the dead owner |

Risks: a stale lock taken over while its owner lives (a write > 10 s; the move renews its lock after the copies); a plain board save still last-write-wins; the source history is rewritten outside any lock (security S-5); a lock wait blocks the event loop up to `LOCK_WAIT` (ux UX-6, architect A-4); `taskboard --board` with the registry busy exits with the message (ux UX-4); the hardened ATs could pass vacuously — each gets a recorded mutation (increment 003).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics | the Phase-3 increments | §1–§4 here → increments 001–003's packets §1 and §2; §2 → the ARQ amendment of `docs/ARCHITECTURE.md` |
| rejected alternatives and risks | the DDR | §6 → the DDR's "what changed against the PDR and why" |
| enablers (fixtures, data, scaffolding, env) | Phase 3 and validation | `tests/multi_board_fixture.py` (the round's boards), `tests/present_portfolio_board.py`, the conftest home seam; a clean `base_ref` worktree for the REDs; `LOCK_WAIT` patched to 0.2 s in the lock tests |
| proposed test cases | layers 0/A/B and the DDR | §5 → the packets' §4 `Mutation verdicts`; the DDR's checklist |
| design → requirement traceability | the matrix and the DDR | §5's Id column ↔ `01-requirements.md` §3/§4; the packets' §2 `Traces to` |

- ⚠ Any row whose consumer column is empty: **remove the output, or explain why it is being produced.**

## 8 · Parallelisation plan *(only if the batch forks)*

none — one lane, three increments in order.

**After the P2/PDR review, iteration 1 (LED-2026-10-20-batch-02.2):** the conditions are carried by the requirements — the `~` normalised at load (architect A-1, security S-4); an unreadable registry never written over without a copy (security S-1); the lock owner-safe, regular-file-only, time-symmetric and renewed (S-2, S-3, A-3); the history copy streamed (S-5); the notice without a false backups sentence and naming the target board (UX-2, UX-3, A-5); a busy start a message (UX-4, A-4); the unarchive rank kept without a tie (UX-1); AT-2304 ranks first, then archives (QA-1); the hygiene law scoped (QA-2, QA-3); AT-2104's cursor row (QA-4); the missing arms (QA-5, QA-7); `touch`'s in-memory exception (QA-6); §4's consumers (A-6).

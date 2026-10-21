# PLAN — taskboard — Batch 2026-10-20-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-20-batch-02 |
| Objective | Backlog fixes after the multi-board batch (non-visual): `~` in the boards registry resolved through `Path.home()`; a byte copy of the source `history.jsonl` before a move; registry writes as a read-modify-write under a short advisory lock and the move's target board locked while it is rewritten; an unarchived project placed after the last shown presentation rank; `ProjectPicker._move_target`'s unused parameter removed; test hardening (test_boards_forms, AT-2204, AT-2104, `u` in view 2, fewer private reads) |
| Last updated | P5 · 2026-10-20 |
| Standing authorization | standing authorization — the orchestrator's commission of 2026-10-20 (the runtime cannot prompt), relaying the operator's words «Haz lo del backlog por favor.»; the orchestrator scoped this batch to the NON-VISUAL items of `.dev-flow/BACKLOG.md` lines 138–167 (visual items go to a separate prototype round). Quoted from the commission: «Gates close under this authorization; do NOT push, do NOT merge — stop at the batch close and report», «WORK IN A NEW WORKTREE … `-b fix/backlog-boards main`», «Max 4 SOURCE files per increment (tests uncapped)», «Do not add any warning/notification UI», «Keep it simple, stdlib only, Windows-safe; a stale lock must not block forever», «spawn independent reviewers as the flow requires … do not self-review», «run the full suite in 3 SEQUENTIAL chunks … never in parallel». Read as: every gate of this batch is autonomous (reviewer roles are spawned sub-agents carrying their `agents/<role>.md`); commits on the local branch `fix/backlog-boards` are authorized, each ending with the commission's co-author line; **push and merge are NOT authorized**; synthetic data only; the operator's name nowhere (`username_subject`); the main checkout's dirty and untracked files and the other worktrees are not touched; tests never touch the real home. |
| First gate | step 1, on `fix/backlog-boards` at `b1b71e4` before the rollover: exit 0 — 0 block · 49 notice · 63 not applicable; `V7`: bundle identical to its manifest both directions, 57 declared files, `2026-10-12-rev102`. Step 3 (after the rollover): exit 0 — 0 block · 70 notice · 47 not applicable (`evidence/gate-step1.txt`, `evidence/gate-step3.txt`). |
| Premises / RC-1 | RC-1 (a): `git fetch origin` → `origin/main` = `b1b71e4310ea7944edbbb6f16f350352e0a9491b` = local `main` = the worktree's `HEAD`; no rebase owed; `base_ref` stamped `b1b71e4310ea7944edbbb6f16f350352e0a9491b`. RC-1 (b): not already shipped — on `origin/main` `grep -n "lock" taskboard/boards.py` → nothing; `history.jsonl` is never passed to `_backup` (`taskboard/boards.py:485-486`); `_move_target` still takes `_boards` (`taskboard/modals.py:786`). RC-2: `git ls-remote --exit-code --heads origin` → exit 0; newest commit on `origin/main` 2026-10-20 17:57 −0600. Premises: `01-requirements.md` §2.7 (P-1..P-7, all TRUE, `evidence/premises.txt`). |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — `docs/ARCHITECTURE.md` §2 · no new module and no boundary moved: `file_lock` lives in `boards.py` (the `models` layer) |
| A2 | fired | judged — the planned source files span two layers: `models` (`taskboard/boards.py`) and `modals` (`taskboard/modals.py`) |
| A3 | fired | judged — `docs/ARCHITECTURE.md` §4 · the contracts of `Registry`'s writers and of `move_project` change (read-modify-write under a lock; the history copy and the target lock); `file_lock` is a new interface of `models`; the rows amended (ARQ) |
| A4 | not fired | judged — one lane, increments in order |
| B1 | fired | `grep -rl --include=*.py` over `tests/`: `Registry` → `test_boards.py`, `test_boards_forms.py`; `move_project` → `test_boards_move.py`; `_move_target` → none; `_do_archive_toggle\|action_archive` → `test_archive.py`; `present_rank` → `test_boards_move.py`, `test_present_all.py`; `expanduser\|Path.home` → `conftest.py`, `test_boards.py`, `test_boards_home.py` |
| B2 | not fired | judged — no file changes its location; the move still moves the same images and history lines |
| B3 | not fired | `ls tests/goldens` → no such directory; no shipped frame renders the lock, the copy or the rank of an unarchived project in a capture a test compares bytes with |
| B4 | fired | judged — `history.jsonl.pre-move-<date>` (read by the operator, a way back), `boards.json.lock` / `board.json.lock` (read by the other instance's `file_lock`) |
| C1, C2, C3, C4, C7 | not fired | `devflow-scan-spec.py` over `01-requirements.md` (P1): `flags: escape` only (`evidence/scan-p1.txt`); judged with it — no auth, secret, external integration, sensitive data or network surface |
| C5 | fired | judged — a destructive file operation: a stale lock file is removed (`unlink`) by another instance; answered in `01-requirements.md` §6.3; the security-reviewer reads it |
| C6 | fired | the P1 scan's `escape` flag (answered in §6.3) and, judged, the registry's hand-editable `~` paths read as input |
| C8 | not fired | judged — no new markup site; the one markup-adjacent change is a test reading the public `border_title` |
| D1 | fired | judged — the presentation's order after an unarchive (HLR-2304) and the text of existing error notices when a lock is busy (HLR-2301, HLR-2302); `ux-reviewer` joins P2 and the PDR |
| D2 | not fired | judged — no prototype in this batch |
| E1 | fired | 4 stories (US-2301..US-2304) and 3 planned increments |
| E2 | not fired | judged — no high risk declared at intake; the registry and the move keep their byte copies and atomic writes |
| E3 | not fired | judged — internal tool, no client deliverable |
| F1 | not fired | `V7`: bundle identical to its manifest at `2026-10-12-rev102` |
| F2 | not fired | judged — `BACKLOG.md` was refreshed at 2026-10-20-batch-01's close (`b1b71e4`) |

## Where we are

P5 — closed. Increments 001–003, the DDR (approved) and P4 (PASS-WITH-NOTES: 2962 passed in three chunks) are done on the local branch `fix/backlog-boards`; the canon folded; push and merge are not authorized — the orchestrator's, on the operator's word.

## Objective

Close the non-visual backlog items left by 2026-10-20-batch-01 and 2026-10-19-batch-01: two instances never lose each other's registry changes, a move holds its target and keeps the source history's bytes, an unarchived project keeps the presenter's order, `~` goes through the suite's seam, and the suite reads the screen.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2301 | DONE | increment 001 |
| US-2302 | DONE | increment 001 |
| US-2303 | DONE | increment 002 |
| US-2304 | DONE | increments 001 (`~`), 002 (the parameter), 003 (tests) |
| P0 | done | triggers evaluated; refinement done |
| ARQ | approved | `docs/ARCHITECTURE.md` amended (A-1's row fixed) |
| P1 | approved after one iterate-to-refine | LED .1, .2 |
| P2 | approved | iteration 2: architect, qa approve; security, ux approve with conditions |
| PDR | approved with conditions | `design/PDR-2026-10-20-batch-02.md`: PC-1..PC-4 open |
| P3 | done | 001 `d7c3dea`, 002 `9cec898`, 003 `e1c936d`; code review OK to advance each; security APPROVE at 001 |
| DDR | approved | `design/DDR-2026-10-20-batch-02.md`: A-9, A-10, QA-11..QA-14 folded before the seal |
| P4 | PASS-WITH-NOTES | the gate run by the orchestrator at `0206fcd`: 1377 + 827 + 758 = 2962 passed |
| P5 | closed | `05-close.md`; the canon folded (14 ids); push and merge not authorized |

## Roadmap + increment plan

- 001 — `boards.py`: the lock, the registry's read-modify-write, the move's target lock and history copy, `~` (HLR-2301, HLR-2302, HLR-2303, HLR-2305): `taskboard/boards.py`, `taskboard/modals.py` (the stopped-move notice, UX-2), `taskboard/__main__.py` (the busy start, UX-4); `tests/test_boards_concurrency.py` (new). 3 source files.
- 002 — `modals.py`: the unarchive rank and `_move_target(proj, bid)` (HLR-2304, HLR-2306): `taskboard/modals.py`; `tests/test_present_all.py`, `tests/test_hygiene.py` (new, its signature arm). 1 source file.
- 003 — test hardening (HLR-2306, LLR-2306.2): `tests/test_boards_forms.py`, `tests/test_boards_home.py`, `tests/test_present_all.py`, `tests/test_hygiene.py`; `.dev-flow/BACKLOG.md` (docs). 0 source files.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-20 | D1 — the lock is a lock FILE `<name>.lock` created with `os.open(O_CREAT \| O_EXCL)`, removed on release; busy past `LOCK_WAIT` (2 s) → `OSError`; older than `LOCK_STALE` (10 s) → taken over | stdlib, Windows-safe, a stale lock never blocks (the commission); P-6 |
| 2026-10-20 | D2 — a registry write replays its ONE change on the file as read under the lock, and the result is adopted in place (the same entry objects) | another instance's change survives; `BoardsHome` holds entry objects across an edit |
| 2026-10-20 | D3 — the move locks its target from the stale-plan check to the target's save; the source and plain board saves take no lock | the commission names the target; a lock on every save is out of scope |
| 2026-10-20 | D4 — no new notice: a busy lock is an `OSError` whose text the existing notices already show | the commission: no warning/notification UI in this batch |
| 2026-10-20 | D5 — an unarchived ranked project takes `max(other shown ranks) + 1`, or no rank when none is ranked | "after the last shown rank" (the commission); rank 0 would put it ahead of unranked projects |
| 2026-10-20 | D6 — `~` and `~/…` (`~\…` on Windows) through `Path.home()`; `~user` read as written | the suite's seam patches `Path.home` (G-9); the app never writes `~user` |
| 2026-10-20 | D7 — three increments: 001 `boards.py` → 002 `modals.py` → 003 tests | one source file each; the tests-only increment last so its mutations run over the finished code |
| 2026-10-20 | the rollover by script with `devflow-init.py`'s own seed helpers (`evidence/rollover.py`, the 2026-10-20-batch-01 pattern); `owner` the worktree | the commission's worktree; `V40` |
| 2026-10-20 | D8 — LED .2: the `~` normalised at load (A-1); an unreadable registry never written over without a copy (S-1); the lock token-owned, regular-file-only, time-symmetric, renewed (S-2, S-3); the notice and the busy start (UX-2..UX-4); the rank kept unless tied (UX-1); AT-2304 re-cut (QA-1) | the P2/PDR review, iteration 1 |
| 2026-10-20 | D9 — A-7 (in-place adoption by id) accepted LOW and carried to `BACKLOG.md`: the guard the architect proposed keeps two entries of one id in memory; A-8/S-9 (an unwritable folder reported as busy) recorded in §6.3 | the case needs a synthesized `main-2` id reused for another file; the message names the lock's path and the wait is bounded |
| 2026-10-20 | code drafted in a scratch worktree outside the branch (`<scratchpad>/wt-dev`, detached at `b1b71e4`) while the reviewers read the contract; each increment ports its slice into the branch after the PDR, with its own RED on `base_ref` and its battery | the reviewers read the shipped code, which the draft must not move under them (the 2026-10-20-batch-01 pattern) |
| 2026-10-20 | the reviewer lenses of ARQ, P2 and the PDR run as one spawned agent per role over the drafted artifacts together (architect · qa-reviewer · ux-reviewer · security-reviewer); the gates are then recorded in station order | the 2026-10-20-batch-01 pattern; the roles are independent of each other and of the author |

## Risks / watch-items

- a stale lock taken over while its owner still writes · low · the registry's writes take milliseconds; `LOCK_STALE` is 10 s; the re-read keeps earlier entries anyway
- the registry's in-place adoption could leave the home's `entries` stale for an entry another instance added · low · the home re-reads the registry each time it opens
- the hardened ATs could pass vacuously · medium · each gets a recorded mutation in increment 003's battery

## Conventions honored

- synthetic data only (`tmp_path`; the round's fixtures); English artifacts, code and UI; the operator's name nowhere
- no push, no merge, no reset, no force; commits end with the commission's co-author line; own paths staged by name
- no test touches the real home (the conftest seam; the `~` tests point the environment's home at a temporary folder too)
- the full suite in three sequential chunks, `NO_COLOR` unset

## Out-of-scope carries

- any notice or screen that tells the operator another instance is running (the separate prototype round)
- a lock on plain board saves and on the move's source; `~user`
- every other open item of `BACKLOG.md` lines 138–167 (left as they are)

## Gate notices and runtime absences

**Runtime absences (`SKILL.md` gate step 5), named once:** no slash commands, no hooks of the flow's own, no operator prompt (the standing authorization stands in at every gate); reviewer roles run as spawned agents carrying their `agents/<role>.md` role. `V15`, `V16`, `V17`: `not-run` — no canon tree, checkout table or flow hook from a bundle. `/dev-flow-sync`: `not-run` — no deployment record in a bundle install.

**Step 1 (before the rollover):** exit 0 — 0 block · 49 notice; the NOTICEs are historical, over closed batches (`V9`, `V13`, `V22`, `V23`, `V26`, `V42`, `V53`), `V57` (2026-10-20-batch-01's record predates the tree by its close commit), `V40` (the outgoing `state.json`'s `owner` named the main checkout) and the bundle run (`V30`).

**P0 (step 3, after the rollover):** 0 block · 70 notice — the step-3 placeholder NOTICEs over the unfilled seeds; `V30`; the historical NOTICEs above.

**P3 … DDR gates:** 0 block, but for `V2`'s station-expected BLOCKs at increment 001's gate (AT-2304 and AT-2306 have no node until increments 002 and 003 — the runbook's P3 entry red), cleared by increment 003; `V53` while the contract named nodes not yet written; `V22` LLR-2306.2 owns no IFC node (it constrains the tests).

**P4 and the close:** 0 block; `V50`, `V51`, `V54` on the seeded close record until it was written; `V57` (the unfilled `Gated tree` row, filled by close step 7; then `record predates this tree by 1 commit(s)` at the final gate) expected; the historical NOTICEs (`V9`, `V13`, `V22`, `V23`, `V42`, `V53`) over closed batches; `V30` the bundle run.

**ARQ … PDR gates:** 0 block · 68 notice — `V62` between each `--station` move and this plan's rewrite (cleared by the rewrite); `V53` while the contract names test nodes not yet written (P3 writes them); `V22` LLR-2306.2 owns no IFC node (it constrains the tests, transforms no data — a question, not a gate); `V23` the seeded DDR record's placeholders (filled at the DDR); the increment-001 seed's placeholders (`V31`, `V32`, `V36`–`V38`, `V41`) until its packet is written; the historical NOTICEs.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `evidence/premises.py` on `base_ref` | 2026-10-20 | P-1..P-7 TRUE — `evidence/premises.txt` |
| `tests/test_boards_concurrency.py` on `base_ref` (increment 001's RED) | 2026-10-20 | 20 failed, 1 passed — `evidence/red-001.txt` |
| increment 001, targeted (9 files) | 2026-10-20 | 199 passed — `evidence/suite-001.txt` |
| increment 002's RED on `d7c3dea`; targeted (7 files) | 2026-10-20 | 3 failed — `evidence/red-002.txt`; 310 passed — `evidence/suite-002.txt` |
| increment 003's RED on `9cec898`; targeted (4 files) | 2026-10-20 | 1 failed — `evidence/red-003.txt`; 104 passed — `evidence/suite-003.txt` |
| the batteries | 2026-10-20 | 25/25, 6/6, 7/7 KILLED; at the DDR 26/26, 7/7 — `evidence/mutation-00{1,2,3}.txt`, `evidence/mutation-ddr-00{1,3}.txt` |
| the whole suite at P4 (three sequential chunks over `ls tests/test_*.py | sort`, a clean worktree at `0206fcd`, the orchestrator) | 2026-10-20 | 1377 + 827 + 758 = 2962 passed, 0 failed, 0 skipped — `evidence/suite-p4-chunk00..02.txt` |

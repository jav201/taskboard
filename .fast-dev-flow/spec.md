# Quick Spec — the deliberate one-time archive, and archive from the editor

**Status:** CLOSED 2026-07-30 · **Base ref:** `ff5a10b` (main) · **Flow:** fast-dev-flow · **Language:** English

## 1. Objective
Javier's board hit the case increment 10's packet predicted: every finished task
on it predates `phase_changed`, so the standing 20-day sweep moves **0 of 30**
(measured, premise table below) and the feature reads as absent — while the UI
carries the weight of all that old work. Give him a **deliberate one-time purge**
for work the timer can never reach, and put an archive control **inside the
editor**, where he went looking for it.

## 2. User stories
- As a user with a board older than the feature, I want to clear out finished
  work in one deliberate action — told how much, asked first, never surprised.
- As a user, I want to archive a task while I have it open for editing, not only
  from the board.
- As a user, I want the archive to keep behaving like the archive: `v` shows it,
  `x` brings it back, nothing is deleted.

## 3. Acceptance criteria (observable)
- **AC1.** `X` on a board with N finished-but-undated tasks opens a confirm that
  states N and does **not** move anything until it is confirmed; cancelling
  moves nothing.
- **AC2.** Confirming archives exactly those N, saves, and says so.
- **AC3.** The purge **never touches dated done work**, however old — that
  belongs to the 20-day timer.
- **AC4.** The purge **stamps nothing**: an archived task's `phase_changed`
  stays `None`.
- **AC5.** Conservation: every task id survives and only `archived` differs.
- **AC6.** Reversible: the task is hidden by default, listed under `v`, and
  `archived = False` restores it.
- **AC7.** After the purge the standing sweep owns the future: a task stamped
  today and aged 20 days is archived by the timer.
- **AC8.** `X` on a board with nothing to purge says so and opens no confirm.
- **AC9.** The task editor has an `archived` control; toggling it and saving
  archives the task, and the change persists.
- **AC10.** `X` appears in the key bar and in the README (the KEYMAP contract).
- **AC11.** All 333 existing tests stay green.

## 4. Premise table (C-43) — all probes executed against disk

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| The standing sweep is inert on a pre-stamp board | premise | TRUE | probe: `auto_archive_done()` -> **0 of 30** tasks |
| Those tasks are findable as a set | premise | TRUE | probe: `unstamped_done()` -> **30** |
| `Board.unstamped_done` / `archive_unstamped_done` exist | premise | TRUE | probe P1/P2 -> True |
| `X` is in the KEYMAP seat | premise | TRUE | probe P3 -> `['X']` |
| `action_purge_done` exists on the app | premise | TRUE | probe P4 -> True |
| `ConfirmModal` can carry a non-"Delete" label | premise | TRUE | probe P5 -> True (added this batch) |
| The editor exposes `f-archived` and returns it | premise | TRUE | probe P6/P7 -> True |
| The startup notify for the standing sweep exists | premise | TRUE | probe P8 -> "Archived old work" in `app.py` |
| Archiving is a flag, so nothing is deleted | axiom | TRUE | `models.py` `visible_tasks(show_archived)`; conservation law already in `tests/test_archive.py` |
| **Tests for any of this exist** | premise | FALSE -> **RESOLVED** | was `grep -c` -> **0**; now 12 laws in `tests/test_archive.py`, 28 passing in that file, 6 mutants killed |

## 5. Security flags
Scan of objective + criteria: **none fired.** No auth, secrets, network, or
external integration. The one sensitive axis is **data loss**, which is not on
the flag list but is this batch's main risk — answered by AC3/AC4/AC5/AC6 and by
the fact that archiving is a flag, never a delete. `security_required: false`.

## 6. Non-goals
- Changing the 20-day rule or `AUTO_ARCHIVE_DAYS`.
- Back-filling `phase_changed` for old work (the whole point is that it stays
  unknown).
- Any automatic purge — this action only ever runs when a human presses `X`.
- Archiving projects (this is tasks only; `P` already archives projects).

## 7. Files (6 — one over the cap, stated)
`taskboard/models.py` · `taskboard/keymap.py` · `taskboard/app.py` ·
`taskboard/modals.py` · `tests/test_archive.py` · `README.md`

## 8. Flow deviation, recorded
The instruction to run this increment under `/fast-dev-flow` arrived **after the
implementation was written**, so this spec was produced mid-batch rather than
before code. Its premise table is therefore a **verification** of what exists
(every row is an executed probe against disk, and one came back FALSE) rather
than a plan. The remaining work — the tests — is being done spec-first.

## 9. Close

All 11 acceptance criteria are covered by named tests, each confirmed present on
disk (`tests/test_archive.py`, 28 passing). 343 green overall; one pre-existing
environmental failure (`test_win_clipboard_roundtrip`) proved not ours — the OS
clipboard itself is refusing operations right now (`Set-Clipboard` errors), and
this batch changes no clipboard code.

Six mutants verified red: the sweep taking stamped work, the sweep inventing a
date, a wrong count in the confirm, the purge running without asking, the purge
deleting instead of archiving, and the editor's control not being applied.

**The README law built last increment caught this batch's own omission**: `X`
was in the seat and missing from the README, and the keybinding test went red
until it was documented. That is the control paying for itself.

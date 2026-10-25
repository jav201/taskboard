# Commission — the home defers the board's start; the directories stay fresh

Written by the orchestrator on 2026-10-24 for batch `2026-10-24-batch-02`. Branch `fix/home-deferred-start`, from `main` `ffedf02`.

## The operator's words

The question, 2026-10-23:

> «Me es útil incluso tener dos terminales abiertas, cada una con un board distinto… vi el mensaje de que ya tenía el board abierto y tenía que cerrarlo, a pesar de que estaba en la ventana de selección de Boards.»

The orchestrator then proposed the fix described here. The approval, 2026-10-24: «Ok, arréglalo.»

## The defect, read in the code

`TaskboardApp.on_mount` (`taskboard/app.py`, around line 1301) pushes `BoardsHome` when more than one board is active, then calls `_open_board(at_mount=True)` for the default board under the home. That start does three things before the user has picked any board:

- **It writes the default board.** `_migrate_links` and `_sweep_old_done` save it.
- **It announces presence.** `_enter_presence` writes a marker, and notifies when another window holds the same board. That notice is the false alarm the operator saw.
- **It opens the board's modals.** `_init_team_mode` (the identity picker) and `_offer_milestones` open over the home. This is also the BACKLOG item about the blank screen behind the start-up modals (D-12 of 2026-10-20-batch-03).

A second defect: `self.people` and `self.marks` are loaded once at mount. A person or class added in another window does not appear until restart, although the writes themselves are safe (read-modify-write under a lock).

## Decisions (record each in the plan)

- **HD-1, the start is deferred.** With the home shown at start, the default board's start is deferred. No migration, sweep, presence marker, team start or milestone offer runs, and the board file is not written, until the user leaves the home onto a board.
  - **What still happens at mount.** Things that only read: building the board for rendering, the clock interval (once), the registry/people/marks load notices (`_warn_registry`), the key bar.
  - **The paths onto the default board.** `enter` on its card, or `esc` / `back` from the home. Each runs the deferred start exactly once.
  - **Picking another board.** `switch_board` handles it as today, and the default board, never started, is never written.
  - **Quitting from the home.** Nothing is written to any board.
  - `switch_board` currently returns early when `bid == self.board_id`. The deferred case must still run the start.
- **HD-2, the start-up modals open over the board.** The team identity picker and the milestone offer then open over the chosen board, not over the home. This closes the blank-screen item.
- **HD-3, the open-twice notice stays real.** Opening a board that another window really holds still notifies once (batch-03 item 8 A). It now fires only when that board is actually opened.
- **HD-4, unchanged paths.** These keep today's behaviour:
  - a single active board (no home);
  - `--open PATH`, which shows no home;
  - `B` pressed later inside the app, because the board is then already started.
- **HD-5, the directories stay fresh.**
  - **When they re-read.** `self.people` and `self.marks` re-read their file, cheaply, only when its mtime or size changed. They do so when any of these opens: the task editor (`TaskModal`, which owns the `@` picker and the `alt+m` Select), the people directory (`@`, `PeopleDirectory`), the marks manager (`#`, `MarksManager`), and the `/` search with `@…` or `#…`.
  - **Load failures.** A re-read that fails keeps the in-memory copy and notifies once, like the mount's load notice. It never empties the directory.
- **No UI change** beyond the false notice disappearing and the start-up modals appearing over the board instead of the blank home. No prototype is needed: the operator approved the fix as described.

## Increments

At most 4 SOURCE files each; tests are uncapped.

| # | Content | Source files (expected) |
|---|---|---|
| 001 | HD-1 to HD-4 | `taskboard/app.py`, plus `boards.py` only if the presence helper needs it |
| 002 | HD-5 | `taskboard/people.py`, `taskboard/marks.py`, `taskboard/app.py` |

## Acceptance

One node per AT, driven by keys.

- **AT-a, the home touches nothing.**
  1. Set up two boards. The default board holds a sweepable old done task, and another window's fresh presence marker exists for it.
  2. Start the app.

  On the home, there is no open-twice notice, no marker is written for this window, and the default board's bytes are unchanged.

  3. Press `enter` on the default board's card.

  The notice appears once, the marker is written, and the sweep runs.
- **AT-b, `esc` runs the start once.** At start, `esc` from the home runs the deferred start exactly once. Pressing `B` and then `esc` later does not run it again.
- **AT-c, another board.** At start, picking the second board never writes the default board's file.
- **AT-d, the modals open over the board.** At start with the home, the milestone offer appears only after a board is chosen, and over that board.
- **AT-e, the directories are fresh.** A person added to `people.json` by a second `Directory` instance (the other window) appears in the `@` picker the next time the editor opens. The same holds for a class in the `alt+m` Select and in `#`.
- **AT-f, an unreadable re-read.** An unreadable `people.json` at re-read time keeps the in-memory directory and notifies once.
- **Regressions.** Every existing test of the home, multi-board, presence, team mode and the milestone offer stays green. Update a test only when the change of timing is the point (HD-2), and say so in the packet.

## Evidence

- **Tests.** `env -u NO_COLOR` for pytest.
- **Full suite.** At P4: 3 SEQUENTIAL chunks, baseline 3235 passed + 1 environmental skip (the clipboard arm TC-1902), with transcripts. Any other skip or fail blocks the close.
- **Validator.** `--brief` at start and at close: 0 BLOCK.
- **Mutation.** Every new test is mutation-checked.
- **Captures.** One real Windows Terminal capture pair, at 118x30 and 80x24: the milestone offer over the chosen board after the home.
  - Each window has a unique `h01-` title, is closed by title right after its shot, and is verified gone.
  - Never close another window.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
  - Reject black or fewer-than-8-colour shots.

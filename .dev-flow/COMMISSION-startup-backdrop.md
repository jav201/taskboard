# Commission — the board shows behind the start-up modals (D-12)

Written by the orchestrator on 2026-10-25 for batch `2026-10-25-batch-01`. Branch `fix/startup-backdrop`, from `main` `3053c1e`.

## The operator's words

The original finding is D-12 in `.dev-flow/BACKLOG.md`, from the 2026-10-20 backlog round: "the blank screen behind the start-up modals". The commission for this batch, 2026-10-25: «Sigue, tú planeas, la implementación dásela a kimi 2.8». The orchestrator chose D-12 as the next backlog item.

## The defect

The BACKLOG entry, as `2026-10-24-batch-02` left it, says this:

- **What the user sees.** When the one-time milestone offer (`MilestoneOffer`) or the team identity picker (`TeamIdentityPicker`) opens at start, the screen behind it is empty.
- **Where it was measured.** The independent qa probe (QA-P4-04) counted 0 text rows above the offer box. That holds on the deferred `enter` path from the home and on a plain single-board start. The captures are `.dev-flow/2026-10-24-batch-02/evidence/captures/png/offer_*.png`.
- **Contrast.** Every other modal, such as the task editor, opens over a visible board under the shared `#0007` backdrop.

**The code path.**

- `TaskboardApp._open_board` (`taskboard/app.py`) calls `refresh_view()` and then `_init_team_mode()` and `_offer_milestones()`.
- Those two push their `ModalScreen` in the same tick, around lines 1552 and 1674.
- **Hypothesis, NOT verified:** the board view renders width-dependent content, and at that moment it has not been laid out or painted at its real size. The modal goes up over a screen whose `BoardView` holds nothing yet.

The implementer verifies this before fixing.

## Decisions (record each in the plan)

- **SB-1, diagnose first.** Reproduce the empty backdrop in a headless `run_test` at 118x30 and 80x24, and turn that reproduction into the failing test. Find the real cause with file:line. If the hypothesis is wrong, say so in the packet. The fix follows the cause, not the hypothesis.
- **SB-2, the fix.**
  - The start-up modals open only after the board has painted at its real size, so the user sees the board, dimmed by the shared backdrop, behind them.
  - The likely mechanism is deferring the pushes with `call_after_refresh`, or with whatever the cause dictates.
  - The order stays as it is today: identity picker first, offer last (D-615). The rule that the offer covers whatever the start opened stays too.
- **SB-3, nothing else changes.**
  - No modal's content, keys or answers change.
  - The deferred start from the home (`2026-10-24-batch-02`, HD-1..HD-4) behaves exactly as now.
  - Quitting while a start-up modal is open writes the same things as today.
- **No prototype is needed.** This brings the start-up modals in line with how every other modal already looks, so it is not a new design.

## Increments

One increment, 001: at most 4 SOURCE files, expected `taskboard/app.py` only. Tests are uncapped.

## Acceptance

One node per AT, driven by keys.

- **AT-a, the offer.** On a single-board start whose board has milestone candidates, the offer opens with the board's rows visible behind it: more than 0 text rows outside the offer box, at 118x30 and at 80x24.
- **AT-b, the home path.** Start with two boards, then `enter` on the default card. The offer opens over the chosen board with its rows visible.
- **AT-c, team mode.** In team mode, the identity picker opens over the visible board, then the offer over that. The order is unchanged.
- **AT-d, regressions.** Every existing test of the offer, the picker, the home, multi-board, presence and team mode stays green. Change a test only where a timing assumption must move, and justify it in the packet.

## Evidence

- **Import probe.** Before any test, check that pytest in the worktree imports the worktree's `taskboard/`: run a probe test that prints `taskboard.__file__` (the package is installed editable from the main checkout). Use `python -m pytest` from the worktree root.
- **Tests.** Every pytest runs with `env -u NO_COLOR` (bash); `NO_COLOR=` does NOT unset it.
- **Full suite.** At P4: 3 SEQUENTIAL chunks. The baseline is 3248 passed + 1 environmental skip (TC-1902, the clipboard arm). Any other skip or fail blocks the close. Keep the transcripts.
- **Validator.** `--brief` at start and at close: 0 BLOCK.
- **Mutation.** Every new test is mutation-checked. Reverting the deferral must turn AT-a red.
- **Captures.** Real Windows Terminal captures at 118x30 and 80x24 of the offer over the visible board (the single-board start and the home path).
  - Reuse `.dev-flow/2026-10-24-batch-02/evidence/captures/` with `b01-` titles.
  - Close each window by title right after its shot, and verify it is gone. Never close any other window.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
  - Reject black shots and shots with fewer than 8 colours.

# Mutant battery — Inc MR-a (board gantt milestone row), stage E5

Tree: `C:\Users\jjgh8\Github\taskboard-wt\incMR-mut`, detached at `8e3272e` (throwaway).
Change under test: `git diff 154e260 8e3272e -- taskboard/`.
Interpreter: `C:/Users/jjgh8/anaconda3/python.exe`.
Command per mutant: `env -u NO_COLOR python -m pytest -q -p no:cacheprovider <node>`, cwd = this copy,
mutant applied to `taskboard/`, reverted with `git checkout -- <file>`. Baseline: **85 passed**.

## Result table

| # | LLR | Mutation (negative control) | Test node(s) | Result |
|---|---|---|---|---|
| 1 | 4601.1 | row after the group's last task | test_TC_4801… | KILLED |
| 2 | 4601.2 | drop reached milestones | test_TC_4802… | KILLED |
| 3 | 4601.3 | tasks sorted by title | test_TC_4803… | KILLED |
| 4 | 4601.4 | i1 on the first project's row | test_TC_4804… | KILLED |
| 5 | 4601.5 | always emit the row | test_TC_4805… | KILLED |
| 6 | 4601.6 | row under a folded span | test_TC_4806…, test_AT_4602… | KILLED |
| 7 | 4601.7 | each milestone counted in the fold budget | test_TC_4807… | KILLED |
| 8 | 4601.8 | stop's `↳` in the gutter | test_TC_4808… | KILLED |
| 9 | 4602.1 | `◆` for every class | test_TC_4811… | KILLED |
| 10 | 4602.2 | first glyph only, no count | test_TC_4812… | KILLED |
| 11 | 4602.3 | print `10` | test_TC_4813… | KILLED |
| 12 | 4602.4 | filled glyph when reached | test_TC_4814… | KILLED |
| 13 | 4602.5 | no reverse | test_TC_4815…, test_TC_4855…, test_AT_4603… | KILLED |
| 14 | 4602.6 | clamp without the edge glyph | test_TC_4816…, test_AT_4607… | KILLED |
| 15 | 4602.7 | undated drawn at today | test_TC_4817… | KILLED |
| 16 | 4602.8 | 2-cell mark started at w-1 | test_TC_4818… | KILLED |
| 17 | 4603.1 | always after, overflowing | test_TC_4821… | KILLED |
| 18 | 4603.2 | cut to any width (`R…`) | test_TC_4822… | KILLED |
| 19 | 4603.3 | a cut date (`Oct`) | test_TC_4823… | KILLED |
| 20 | 4603.4 | `Oct 19` for the late lead | test_TC_4824… | KILLED |
| 21 | 4603.5 | no one-cell gap check | test_TC_4825… | KILLED |
| 22 | 4603.6 | late count omitted | test_TC_4826… | KILLED |
| 23 | 4603.7 | `i/N` dropped | test_TC_4827…, test_TC_4855…, test_AT_4603… | KILLED |
| 24 | 4603.8 | first member's chip (`✓ done`) | test_TC_4828… | KILLED |
| 25 | 4603.9 | label padded to label_w+1 | test_TC_4829… | KILLED |
| 26 | 4603.10 | row not adding to `drawn` | test_TC_4830… | KILLED |
| 27 | 4603.11 | per-character `c()` | test_TC_4820… | KILLED |
| 28 | 4603.11 NC2 | room measured with `len` | test_TC_4820… | KILLED |
| 29 | 4604.1 | one stop per milestone | test_TC_4831…, test_TC_4831b… | KILLED |
| 30 | 4604.2 | first in walk order (m1) | test_TC_4832…, test_TC_4832b… | KILLED |
| 31 | 4604.3 | skip same-day | test_TC_4833… | KILLED |
| 32 | 4604.4 | `←` moves forward | test_TC_4834… | KILLED |
| 33 | 4604.5 | wrap around | test_TC_4835… | KILLED |
| 34 | 4604.6 | `→` on a task row jumps to the row | test_TC_4836… | KILLED |
| 35 | 4604.7 | details of the anchor | test_TC_4837… | KILLED |
| 36 | 4604.8 | stop stays the anchor | test_TC_4838… | KILLED |
| 37 | 4605.1 | row from the unfiltered board | test_TC_4841… | KILLED |
| 38 | 4605.2 | row built before the class filter | test_TC_4842… | **SURVIVED** |
| 39 | 4605.3 | walk the unfiltered milestones | test_TC_4843…, test_AT_4605… | **SURVIVED** |
| 40 | R-4 | nav keeps hidden classes | test_TC_4843b… ×2, test_TC_4843c… | KILLED |
| 41 | 4606.1 | shared row in the link frame | test_TC_4851… | KILLED |
| 42 | 4606.2 | the anchor as waiter | test_TC_4852… | KILLED |
| 43 | 4606.3 | a flag left set by the link frame | test_TC_4853… | KILLED |
| 44 | 4606.4 | paged by the milestone's base row index | test_TC_4854… | KILLED |
| 45 | 4606.5 | base `task_row(sel)` | test_TC_4855… | KILLED |

**Killed: 43 · Survived: 2.**

## Survivors

### LLR-4605.2 — "row built before the class filter" (TC-4842)

The class filter is applied at **two** seats before `gantt_plan` builds the lane:

1. `_gantt_frame` entry — `if _hidden_class_ids(board): board = _hide(board)` (pre-existing, LLR-2608.1);
2. `gantt_plan` entry — the new `if done_rows and _hidden_class_ids(board): board = _hide(board)` (the "N-5: THE ONE SEAT").

Removing only the `gantt_plan` seat (the one the requirements name as the single seat) leaves the row still
filtered, because `_gantt_frame` already filtered the board before `gantt_plan` ran — the test read 3 marks
and passed. Removing only the `_gantt_frame` seat likewise survives, because `gantt_plan` re-filters. TC-4842
turns RED only when **both** seats are removed. So the negative control cannot be expressed as a single-seat
mutation: the "one seat" claim is false, and TC-4842's assertion (`tm2`/`tm3` absent) cannot observe which seat
did the filtering.

### LLR-4605.3 — "walk the unfiltered milestones" (TC-4843, AT-4605)

`action_hmove` walks `gantt_lane(self.board, …)` (unfiltered), selects a filtered-out milestone (e.g. `tm3`
under `/store`), then calls `refresh_view()` → `_select_first()`. `_select_first` re-validates the selection
against the filtered nav order (F-3); `tm3` is not in `_view_board()`, so `board.task_by_id("tm3")` is `None`
and the selection snaps back to `order[0]` = `tm4`. The test asserts only the final selection, so the transient
walk is invisible. Missing assertion: none at the final-selection level can catch it — the walk's effect is
neutralised by the selection-validity law before it is observable.

## Notes

- 4602.7 killed via `TypeError` (undated milestone's `today` reaches `ax.cell`); 4603.1 killed via `IndexError`
  ("always after" runs off the field on the before-case). Both are test failures (KILLED), not assertion errors.
- 4603.11 killed 8 of 20 parametrized cases; 4603.11 NC2 killed the 4 wide-glyph cases — both FAIL the node.
- 4605.1: applied as `filtered_board` keeping all milestones (the row reads the unfiltered milestone set); killed.
- 4606.3: applied as `render_gantt` dropping `done_rows=True` (the shared-row flag is not restored); killed.
- No background processes left; the tree was reverted to `8e3272e` after every mutant (`git status` clean).

## E5 corrective replay (2026-11-06, Opus 5.5)

Tree: `C:\Users\jjgh8\Github\taskboard-wt\incMR-mut2`, detached at `5d2c880` (the corrective commit), removed
afterwards with `git worktree remove --force`. Same command and interpreter as above; `taskboard.__file__` =
the copy's. Baseline of the replayed nodes: 37 passed. Evidence: `evidence/e5-mutant-replay.txt`.

| # | LLR | Mutation (negative control) | Test node(s) | Result |
|---|---|---|---|---|
| 38 | 4605.2 | drop the class filter in `gantt_plan` (`if False:`), now the row's only seat (C-2) | test_TC_4842… | KILLED (1 failed) |
| 39 | 4605.3 | `action_hmove` walks the unfiltered lane: `gantt_lane` over a copy of `self.board` with `marks = {}` | test_TC_4843…, test_AT_4605… | KILLED (2 failed) |
| 46 | 4603.11 N-9 | tell a label run by `len(glyph) > 1` again (F1) | test_TC_4820c… ×3 | KILLED (2 failed, the 2-codepoint arm passes by design) |
| 47 | SEC-6 | drop the `n <= 0` guard in `put_label` (SEC-8) | test_TC_4820b… ×3 | KILLED (3 failed) |

**After the replay: Killed 47 · Survived 0.** Rows 38 and 39 replace the SURVIVED rows above; 46 and 47 are new.

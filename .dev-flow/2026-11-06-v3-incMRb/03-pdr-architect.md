# E3 PDR round 1 — architect — Inc MR-b

> Reviewer: architect (Opus), read-only. Tree: `ms-row-proto` at `fe8ecb8` (product code equal to `8ca174c`).
> Read: `01-requirements.md`, the ledger, `00-e1-rulings.md` (RB-1..RB-6, taken as the intended design),
> the four `graph-*.cw.md`, `e2-seams.md`, `baseline-notes.md`; `views.py` 285-312, 2480-2520, 3140-3170,
> 6945-6970, 7015-7035, 7475-7720, 7806-7920; `app.py` 395-470, 520-540, 637-660; `report_html.py` 17-26;
> `tests/test_present.py` 58-89; `tests/test_milestone_marks.py` 145-160. No test was run: every check below is
> `executed` as a code read, none as a test run.

**Verdict: PASS-WITH-NOTES.** 0 MAJOR, 2 MINOR (A-1, A-2), 5 NOTE. None blocks E4. The two MINORs fit the
one correction pass that RB-2..RB-6 already schedule.

## Focus answers

1. **Stop order (RB-1): consistent in all three views.** Views 1 and 2 get the field, the briefs, the blocks and
   the cursor fallback from one list. `render_present` takes `stops[0]` and `PresentScreen._cursor` takes `ids[0]`
   from the same `present_stop_order` (SEAM-2). Only one app-side reader of the order exists, `_shown_ids`
   (`app.py:403`), and `PresentScreen` has no click handler that maps a line to a task. View 3 gets its order from
   `_all_plan`, and `_all_timeline` (`views.py:7859`) is its only caller. `_all_axis`, `_all_late` and
   `_all_label` do not depend on order (7721-7766). `_hide_all`'s next-stop rule (`app.py:530-539`) works with
   several stops on one line. The overflow cut (7865-7866) keeps or cuts a whole shared line. The blocks are
   covered in A-3.
2. **`milestone_walk_key`: the lift is byte-identical.** `walk_key` (2490-2492) uses no local of `gantt_plan`:
   `parse_iso` and `date` are module names. `lane_anchor` stays nested. The order and every board-gantt frame are
   unchanged. See A-5 for an error in the graph's text.
3. **Byte oracles on boards with no milestone stay equal.** On such boards `present_stop_order` returns its input
   unchanged, `stops[0] == open_t[0]`, `_all_layout`'s `need` and lines match base, and the note room formula
   (7625) gets the same inputs. `_present_field`'s new branches are reached only through
   `gantt_milestone_row`'s cells (`rev:` 2861, `run:` 2956, consumed `""`). The PRES-V3 and PRES-V4 tests compare
   plain text (`test_present.py:58-67, 83`), and their boards hold no title containing `[` or `\`. E2-F6 and
   TC-4905/TC-4918 are correct.
4. **The `x` deck is unaffected.** `present_deck_boards` (7647-7680) stays untouched. `report_html` imports none
   of the slice (`report_html.py:26`). `action_export` (`app.py:637-660`) reads no cursor and no order. The one
   gap is in the negative control: A-1.
5. **`_present_brief` (RB-2): the minimal fix is one token.** See A-6.

## Findings

**A-1 — MINOR — the deck's negative control cannot fail on order.** `present_deck_boards` re-sorts what it holds
by board position (`proxy.tasks = sorted(held, key=lambda t: pos[t.id])`, `views.py:7679`), so a mutant that only
changes the order is undone before the deck sees it. LLR-4654.1's NC, "the proxy holding tasks in stop order",
therefore cannot turn RED by order on any fixture. E2-F7's remedy, a fixture with a task ahead of a milestone, does
not help. RB-6's wording, "draws the shared row into the deck", names no place in the code.
*Fix:* make the NC a mutant that changes which tasks the deck holds. At 7675, replace
`present_tasks_m(board, p.id)[1]` with `present_stop_order(present_tasks_m(board, p.id)[0])`. That drops the
reached `tm1` and every done task, so the sha256 of the deck from MR-F no longer matches the `8ca174c` oracle.
Reword HLR-4654's NC, LLR-4654.1's NC and TC-4931 to match. Drop the extra-fixture remedy.

**A-2 — MINOR — the milestone branch of `_present_task_row` becomes dead code; remove it.** After MR-b, both
callers (7617 and 7894) pass only non-milestones, so 7480-7490 has no product route. Tests that call it directly
would then test an entry point no route calls (E4's *partial* rule), and the presentation would hold two ways to
draw a milestone that can drift apart.
*Fix:* delete the `if task.milestone:` branch. This is a change to an existing unit: 11 units, still 2 files.
Update the mark-site list in `tests/test_milestone_marks.py:153` from `_present_task_row` to `_present_lane_row`.
`gantt_milestone_cells` keeps its caller in the board gantt (3698), so it stays.

**A-3 — NOTE — what RB-1 does to the split view's blocks.** View 2 splits by count, `half = (n + 1) // 2` (7622).
With the stops led by milestones, on MR-F's `ppr` the left column holds all four milestones and the right column
all four tasks (TC-4925). Both columns get the same `room`. If milestone notes are short and task notes are long,
the left column sits half empty while `present_alloc` cuts the task notes harder than at base. The order is still
right: the field reads top to bottom and the blocks column by column. This is a visible change, not a defect.
*Fix:* no design change. Put a view-2 capture of MR-F at 118x30 in the operator's RB-1 review.

**A-4 — NOTE — draw the field from one list.** `render_present`'s graph draws the task rows from "each
non-milestone of `open_t`", and the briefs from `stops`. The output is the same either way.
*Fix:* draw both from `stops[len(lane):]`, so the order has one source, as SEAM-2 states.

**A-5 — NOTE — the graph miscounts `walk_key`'s uses.** `graph-proto-V.cw.md` (`gantt_plan`) says "its two
uses". There is one, at 2511 (`baseline-notes.md` says the same).
*Fix:* change it to "its one use".

**A-6 — NOTE — keep RB-2 to the swap.** At 7544, change `c(escape(txt), …)` to `c(_literal(txt), …)`. `gap` is
already measured on the raw `txt`. Leave `_present_finish`'s width assert (7561-7562) as it is. Moving that
product `assert` to measure the rendered text would widen the change, and any latent mismatch elsewhere would
then crash the app. The swap keeps the plain oracles byte-equal: for a title with no `[` and no trailing `\`,
`_literal` and `escape` return the same string (290-312). View 2's block title (7402) also calls
`escape(clip(…))`, but P-9 measured it width-true. Leave it alone. If the RB-2 test finds it wrong, that is a
ruling for the orchestrator, not a silent fix.

**A-7 — NOTE — RB-3..RB-5 need no further design change.** RB-3 matches P-6's strings at 80 columns. For RB-4,
118x18 is what the arithmetic supports (`_all_layout` example: need 15, room 15). RB-5's blank gutter is already
in `_present_lane_row`. Citing LLR-4601.8 is enough, and adding an LLR costs more than it gains.

## Evidence checklist

- ✓ Constraints stated (`executed`): R-1, R-2 and R-7, the 4-file budget, and byte equality for boards with no
  milestone and for the deck (`01-requirements.md` §1, §6).
- ✓ Alternatives: `n/a — RB-1 decided the stop order; R-1 and SEAM-4 fix the reuse of MR-a's row`. A-2 removes code
  rather than adding a second design.
- ✓ Constraints that do not apply: cost and latency are `n/a — local TUI render, no service`; privacy is
  `n/a — no data leaves the board; the deck path is unchanged (A-1)`.
- ✓ Each recommendation has a rationale tied to a constraint (A-1 → HLR-4654; A-2 → E4's partial rule; A-6 → byte
  oracles).
- ✓ Risks listed: A-3 is visible to the operator; A-6 explains why the product assert stays.
- ✓ Diagram: `n/a — the four graphs carry the flow; this review adds no edge`.
- ✓ What would change the verdict: A-1 left as it is, so that E4 reports a deck NC that cannot fail as RED, would
  make it MAJOR; so would a probe showing 7402 doubles the `\`.
- ✓ Two-layer requirements: US-4651 → AT-4651..4656, and US → HLR-4651..4654 → LLR → TC-49nn (§3-§5, the
  numbering rule in the header).

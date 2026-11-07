# E3 addenda — Inc MR-b — instructions to E4

E3 round 1 closed PASS-WITH-NOTES from both reviewers (`03-pdr-architect.md`, `03-pdr-security.md`). The design
corrections are in the requirements (LED-2026-11-06-incMRb.3 to .9), the graphs and `e2-seams.md`. This file holds
every MINOR and NOTE that remains as an E4 instruction, plus the two E2 notes that are still open. Binding on E4.

| # | From | Owner | Instruction |
|---|---|---|---|
| B-1 | SEC-B1, A-6 | V implementer | In `_present_brief` and `_present_heading`, make only the `escape(…)` → `_literal(…)` swap, with the title cut first by `clip`, as now. Leave `_present_finish`'s width assert (`views.py:7561-7562`) as it is. Do not add a measure-and-pad fix. If a test shows another `escape(clip(…))` site wrong, report it to the orchestrator; do not fix it silently. |
| B-2 | SEC-B2 | V tester | Measure TC-4916, TC-4917, TC-4919, TC-4920 and AT-4655 with `cell_len` on each line of the rendered frame (`render_present(…).plain` or the pilot's screen, after `to_text`). Never measure with `_strip` of the markup or with the assert alone. Prove TC-4919 RED on base: the line is 119 cells at 118 and 81 at 80, and it reads `\\`. |
| B-3 | SEC-B3 | V tester and AT tester | TC-4920 and AT-4655 include `a\[b]`, `\[x` and a title cut after `\[`. Prove TC-4920 RED on base (`a[b]`). The security probe's evidence (P-a, P-b) stays `planned` until these cases and TC-4916 run through `to_text`. |
| B-4 | A-1, RB-6 | mutant runner | TC-4931's NC is the mutant in LLR-4654.1. At `views.py:7671`, replace `present_tasks_m(board, p.id)[1]` with `present_stop_order(present_tasks_m(board, p.id)[0])`. Each of the 3 decks' sha256 must differ from the `8ca174c` oracle (3/3 RED). Do not use an order-only mutant: the deck re-sorts by board position (`views.py:7675`), so it cannot fail. Capture the base oracle on `8ca174c` before E4 edits anything. |
| B-5 | A-2 | integrator | Remove the `if task.milestone:` branch of `_present_task_row`. Change the mark-site list in `tests/test_milestone_marks.py:153` from `_present_task_row` to `_present_lane_row`, citing LLR-4651.1. Keep `gantt_milestone_cells`: the board gantt still calls it (`views.py:3698`). No test may call `_present_task_row` with a milestone. Such a test is *partial*, because no product route calls it that way. |
| B-6 | A-3 | AT tester | Take a real capture of view 2 on MR-F at 118x30 for the operator's RB-1 review. The left column holds the four milestones and the right column the four tasks. Label it as a visible change, not a defect. |
| B-7 | A-4 | V implementer | `render_present` draws the task rows and the briefs from one list, `stops[len(lane):]` and `stops`, as the graph now states (SEAM-2). Do not iterate over `open_t` a second time. |
| B-8 | E2-F5 | V tester | Run TC-4918 with the same cursor on base and new. The tick row echoes the cursor, and LLR-4653.3 moves `ppd`'s default cursor. |
| B-9 | E2-F6 | integrator | PRES-V3, PRES-V4 and the 7 frame-oracle tests in `baseline-notes.md` B-1 hold no milestone. They stay byte-equal, and a change in them is a regression. Re-baseline only the tests on milestone boards, one at a time, each citing the LLR that moves it. |
| B-10 | A-5, A-7 | — | No E4 action. A-5 is fixed in the graph (`gantt_plan`: one use of `walk_key`). A-7 needs no change; RB-5 is LLR-4651.8. |

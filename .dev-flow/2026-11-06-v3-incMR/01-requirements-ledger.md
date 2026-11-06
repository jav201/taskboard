# Requirements ledger — taskboard — Inc MR-a, a project's milestones share one row in the board's gantt

> Append-only. Every entry names the requirements it amends one by one (V26: no ranges).

### LED-2026-11-06-incMR.1 — verdict A, D2 and D3 made strict, with the failure paths the round left open
- **Requirement:** HLR-4601
- **Requirement:** HLR-4602
- **Requirement:** HLR-4603
- **Requirement:** HLR-4604
- **Requirement:** HLR-4605
- **Date:** 2026-11-06
- **What changed:** the round's variant A and the verdict (D2 `fila`, D3 `si`) were split into 35 single-`shall` LLRs (LLR-4601.1..4605.3). Added beyond the round's words, each as its own requirement: the row's members pinned to base's drawn milestones, reached ones kept while the group has open work (LLR-4601.2, D-606); task rows and the done tail pinned to base (LLR-4601.3); no row for a group with nothing drawn (LLR-4601.5) or folded (LLR-4601.6); the fold budget counting the row as 1 (LLR-4601.7); 10+ on a day as `+` (LLR-4602.3); off-window and no-due milestones (LLR-4602.6, LLR-4602.7); the title cut floor of 6 cells (LLR-4603.2); no label over a mark (LLR-4603.5); the label column's two states and the `i/N` tag (LLR-4603.6, LLR-4603.7); the chip rule (LLR-4603.8); the legend still naming the marks (LLR-4603.10); the landing rule (LLR-4604.2); the walk's ends (LLR-4604.5); `←→` elsewhere unchanged (LLR-4604.6); task keys acting on the walked milestone (LLR-4604.8); hidden and unmatched milestones out of the walk (LLR-4605.3).
- **Why:** the row replaces N rows by one stop, so every place that keyed a milestone by its own row — the fold budget, `line_map`, the legend's `drawn` set, the nav column, the keys acting on the selected task — can silently act on the anchor instead of the walked milestone, or leak a hidden one. `nav_model` reads the board without the class filter today, so the walk must be pinned separately (LLR-4605.3).
- **Evidence:** `taskboard/views.py:2432-2525` (`gantt_plan`, D-606 rows, fold budget), `views.py:3381-3394` (`task_row` for a milestone), `views.py:2713-2735` (`gantt_milestone_cells`: edge glyphs, no due draws nothing), `views.py:2751-2768` (`gantt_milestone_chip`), `views.py:8425-8430` (`nav_model` gantt branch), `taskboard/app.py:3439-3453` (`action_hmove`), `app.py:4132-4137` (`_view_board`: search only); `prototypes/milestone_row/proto.py:141-369` (variant A plan, cells, labels) and the A captures in `prototypes/milestone_row/out/png/`.

### LED-2026-11-06-incMR.2 — MR-2: the link mode and the paged fold (rulings 2, 3, R-3)
- **Requirement:** HLR-4606
- **Requirement:** LLR-4606.1
- **Requirement:** LLR-4606.2
- **Requirement:** LLR-4606.3
- **Requirement:** LLR-4606.4
- **Requirement:** LLR-4606.5
- **Date:** 2026-11-06
- **What changed:** the link mode keeps one row per milestone (LLR-4606.1) and opens with the walked milestone as waiter (LLR-4606.2); the board gantt's rows return when it closes (LLR-4606.3). The paged fold treats the row as one row: a selected milestone pages to the row (LLR-4606.4), and the D8 and ≤ 2-row frames draw the row as the selected row (LLR-4606.5).
- **Why:** R-3 (`00-e1-rulings.md`): each `═`, connector and `⟲` names one task by its row. The pages and the D8 frame index rows and draw `task_row(sel)`, which would draw a lone milestone row the board no longer has.
- **Evidence:** `views.py:8885-8960` (`gantt_link_order`, `gantt_link_frame`, `gantt_link_overlay`), `views.py:3421-3476` (D8 and paged branches); `00-e1-rulings.md` §3 facts 3–4, §4, R-3.

### LED-2026-11-06-incMR.3 — HLR-4606 split into HLR-4606.1 (link mode) and HLR-4606.2 (pages), ruling R-5
- **Requirement:** HLR-4606
- **Requirement:** HLR-4606.1
- **Requirement:** HLR-4606.2
- **Date:** 2026-11-06
- **What changed:** HLR-4606 had two responses (one row per milestone in the link mode; the milestone row as one row of the pages) under one `shall`. It is split in place and keeps the parent id with `.1` and `.2`, as the skill's E1 rule says. HLR-4606.1 holds LLR-4606.1, LLR-4606.2 and LLR-4606.3. HLR-4606.2 holds LLR-4606.4 and LLR-4606.5. No LLR id, TC number or AT changes. The E1 note proposed HLR-4607 for the second half; the skill's split rule takes precedence, so HLR-4607 is not used.
- **Why:** one `shall` per requirement. In the E2 graph the two responses fall on different units: the link mode on `gantt_plan` with `done_rows` off, and the pages on `_gantt_frame`'s paged and D8 branches.
- **Evidence:** `00-e1-rulings.md` R-5 (approved in advance); `graph-proto-V.cw.md` nodes `gantt_plan` (TC-4851), `_gantt_frame` (TC-4854) and `_gantt_frame.<locals>.task_row` (TC-4855).

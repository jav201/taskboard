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

### LED-2026-11-06-incMR.4 — E3 round 1, ruling R-6: the architect's F-1 to F-5 adopted as written
- **Requirement:** LLR-4601.8
- **Requirement:** LLR-4602.1
- **Requirement:** LLR-4602.6
- **Requirement:** LLR-4603.3
- **Requirement:** LLR-4603.4
- **Requirement:** LLR-4603.7
- **Requirement:** AT-4601
- **Requirement:** AT-4607
- **Date:** 2026-11-06
- **What changed:** §1 defines *share one cell* and *lead*. LLR-4603.3 dates each mark by its lead, a shared cell included (F-1). LLR-4603.4 shows `▲Nd` when the mark's lead is late (F-1). LLR-4603.7 counts ` i/N` in the mark's cell, not on its day (F-1). LLR-4602.1's threshold gives h1 `◆` in `mut`, the seat (F-2). LLR-4602.6's threshold uses a reached milestone due 90 days ahead, `<hollow>✓▸` in the last three cells, and two off-window members bucketed in the cell they are drawn in (F-3). AT-4607 is rewritten with the same reached milestone (F-3). New LLR-4601.8: the milestone row's dependency gutter is blank, TC-4808 (F-5). AT-4601 now cites LLR-4601.8 and checks the blank gutter. §6: the slice is 9 units in 2 files, 3 new and 6 changed, with `gantt_lane`, `_gantt_field` and `nav_model` numbered (F-4).
- **Why:** F-1: the statement of LLR-4603.3 contradicted its threshold and AT-4601. At `k > 1` days per cell, "on its day" and "in its cell" disagree. F-2: no seat draws a project hue, and `milestone_tone` has no caller. F-3: `gantt_window` keeps every open due inside the window, so the open `▸` case cannot be reached through a product route. F-4: the count left out the painter, the lane accessor and `nav_model`'s change of behaviour. F-5: one gutter cell cannot name which of N marks waits. Removing it is preferred over guarding it.
- **Evidence:** `03-pdr-architect.md` §1 (F-1 to F-5); `00-e1-rulings.md` R-6; `views.py:2310-2321` (`GanttAxis` k), `views.py:2518-2533` (`gantt_window`), `views.py:2600-2602` (`milestone_mark`), `views.py:2731-2733` (reached mark geometry), `views.py:3384-3386` (`gantt_dep_mark` in the gutter).

### LED-2026-11-06-incMR.5 — E3 round 1, ruling R-7: field labels are escaped as one string before they are laid into cells (SEC-1, N-1, SEC-2)
- **Requirement:** LLR-4603.11
- **Date:** 2026-11-06
- **What changed:** new Unwanted LLR-4603.11. A field label that holds markup brackets, a backslash, or wide or combining characters is drawn as its literal text, measured and cut in cells, within the field's width. The threshold covers 5 titles (`a]b[/]`, `[@click=app.quit]x`, `x\`, a wide-glyph title and a combining-mark title) in 3 placements (after, before, cut). It has two negative controls (per-character cells; room measured with `len`). Its TC is TC-4820, an exception to the numbering rule, because TC-4831 is LLR-4604.1's. The design is in `graph-interfaces.cw.md` `gantt_milestone_row`, LABEL PATH, in this order: measure in cells, cut the plain text with `fit`, escape once with `_literal`, then lay the run into one cell and mark the cells it covers as consumed. Of the two fixes the ruling allows, this is the smaller one: the seat stays Rich markup, and the change adds no `Text` pipeline.
- **Why:** the probes in `03-pdr-security.md` SEC-1: `a]b[/]` raises `MarkupError`, `[@click…]` becomes a live tag, and `x\` leaves a style open. SEC-2 measured a `wide中文` title at 6 by `len` and 8 cells wide. Escaping each character does not help, because `collapse_runs` joins same-style neighbours again.
- **Evidence:** `03-pdr-security.md` SEC-1, SEC-2; `03-pdr-architect.md` N-1; `views.py:75-78` (`c`), `views.py:95-108` (`fit`), `views.py:290` (`_literal`), `views.py:2877-2895` (`_gantt_field`); `prototypes/milestone_row/proto.py:242-266` (`put`).

### LED-2026-11-06-incMR.6 — E3 round 1, ruling R-8: the remaining MEDIUM, LOW and MINOR findings
- **Requirement:** LLR-4602.8
- **Requirement:** AT-4606
- **Date:** 2026-11-06
- **What changed:** new Unwanted LLR-4602.8. A two-cell mark that falls in the field's last cell starts one cell inward, TC-4818 (SEC-3). AT-4606 now reads "one row per drawn milestone (m1..m5), byte-equal to base" (N-2). The rest is design or an E4 instruction and changes no requirement text. The *share one cell* definition answers SEC-4. In the graph, the class filter moves into `gantt_plan` (N-5). Only `gantt_milestone_row` stays frozen for MR-b, and `gantt_lane_label` moves to V (N-6). The tones go into the funcs (N-7). TC-4843d covers N-3 and SEC-5. N-4 and the E4 checks go in `e3-addenda.md`. LLR count: 43.
- **Why:** SEC-3: the second cell of the mark would land at index `w`. N-2: AT-4606 disagreed with LLR-4606.1 and TC-4851.
- **Evidence:** `03-pdr-security.md` SEC-3, SEC-4, SEC-5; `03-pdr-architect.md` N-2 to N-7; `00-e1-rulings.md` R-8.

### LED-2026-11-06-incMR.7 — E4 integration, ruling I-2: LLR-4603.1's threshold example made feasible (F-T1)
- **Requirement:** LLR-4603.1
- **Date:** 2026-11-06
- **What changed:** the threshold EXAMPLE only; the `shall` is unchanged. Was: "118x30, m3 selected → `Steering go/no-go` follows `■2 `; m5 (rightmost) selected with no room after → its title ends one cell before its mark". Now: "118x30, m5 selected → `Pilot launch` follows `★ `; a reached milestone due on the field's last day selected → its title ends one cell before `⬡✓`; 2/2". The behaviour under test is the same: whole title after the mark when the room to the next mark (or edge) holds it, else whole before it; the NC (always after, overflowing) is still RED on the `before` case. TC-4821 asserts the new example (plus the g2 case it already had).
- **Why:** measured, `evidence/i2-measure.txt`: the fitted axis at 118x30 is k = 0.5 from Oct 14; m3 sits at cell 20 and m5 at cell 32, so 8 cells lie between `■2 ` and the gap before m5, and the 17-cell title cannot be whole on either side (TC-4822's `Steerin…` cut is the requirement-true output). m5 has 46 cells after it, so "no room after" is false. The axis is fitted by the board, not by the selection, so no code change can make the old example hold.
- **Evidence:** `evidence/i2-measure.txt`; `e4-tests.md` §7 F-T1; `e4-deviations.md` D-2; `e4-integration.md` I-2.

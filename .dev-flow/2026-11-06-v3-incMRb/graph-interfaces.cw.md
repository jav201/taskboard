# Code-Wire prototype — Inc MR-b — the shared interfaces (frozen)

The contracts that the two file groups share. Only the differences from `graph-baseline.cw.md` (2ce3943) appear here. Owners: **V** = `taskboard/views.py` (graph-proto-V.cw.md) and **S** = `taskboard/app.py` (graph-proto-S.cw.md). V implements every node in this file. S calls `present_stop_order` and reads the view-3 stops. An agent proposes a change in this file and never changes an interface alone.

MR-a's frozen `gantt_milestone_row` and its V-internal `gantt_lane_label` and `_lane_marks` (`../2026-11-06-v3-incMR/graph-interfaces.cw.md`, `graph-proto-V.cw.md`, as amended by LED-2026-11-06-incMR.8) are reused UNCHANGED (R-1, SEAM-7): MR-b adds no parameter and no branch to them, and the board gantt's frames stay byte-equal. R-7's LABEL PATH holds for every label the presentation's milestone row draws: the field labels come only from `gantt_milestone_row`, and the label column only from `gantt_lane_label` (`title_markup`, escaped and cut in cells).

Example sources are the TC and AT ids of `01-requirements.md`: LLR-4651.n → TC-(4900+n), LLR-4652.n → TC-(4910+n), LLR-4653.n → TC-(4920+n), LLR-4654.n → TC-(4930+n). No run is recorded yet; the plain values come from the probes on 2ce3943 (`baseline-notes.md`, P-1..P-8), which call MR-a's shipped units on the presentation's own axis. Fixture MR-F (`tests/milestone_row_fixture.py`), today 2026-10-20; ids `t<key>`, projects `ppr` *Pilot rollout*, `ppe` *Eval harness*, `ppd` *Docs & handover*. *Walk order*, *drawn milestones*, *stop order* and *cursor milestone*: as in `01-requirements.md` §1.

## Nodes

milestone_walk_key
req: LLR-4653.1, LLR-4653.2
in: Task t
out: tuple key
func: NEW at module scope, LIFTED from `gantt_plan.<locals>.walk_key` with its body unchanged: `(due is None, due or date.max, title, id)`. `gantt_plan` calls it in place of the nested def (MR-a's lane order and every board-gantt frame byte-unchanged), and `present_stop_order` calls it, so the board and `R` share one walk order
module: taskboard/views.py
examples: (TC-4921) `ppr`'s open milestones sorted by it → ["tm2", "tm3", "tm4", "tm5"] (tm3 before tm4 on Oct 24: `Steering…` < `Store…`)
examples: (TC-4922) a milestone with no due sorts after every dated one: key `(True, date.max, …)`
examples: (TC-4921) MR-a's `gantt_lane(MR-F, …, "tm3", …)` → still ["tm1", "tm2", "tm3", "tm4", "tm5"] (MR-a TC-4833 unchanged)

present_stop_order
req: LLR-4653.1, LLR-4653.2, LLR-4653.3, LLR-4653.5
in: list[Task] open_t
out: list[Task] stops
func: NEW. One project's stop order: the milestones of `open_t` sorted by `milestone_walk_key`, then the other tasks of `open_t` in their given (base) order. Pure; adds and drops nothing (`open_t` is already `present_tasks_m(…)[0]`: shown, open, hidden classes out). The ONE source of the order for the field, the briefs, the blocks, the view-3 stops (V) and the views-1/2 cursor (S)
module: taskboard/views.py
examples: (TC-4921) `ppr` open ["tm2", "tstore", "tm3", "tm4", "ttele", "ttrain", "tm5", "trota"] → stops ["tm2", "tm3", "tm4", "tm5", "tstore", "ttele", "ttrain", "trota"]
examples: (TC-4923) `ppd` open ["tha", "thr", "th1"] → stops ["th1", "tha", "thr"]: the milestone first though both tasks are due before it
examples: (TC-4923) class Review hidden: `ppr` open has no tm2/tm3 → stops ["tm4", "tm5", "tstore", "ttele", "ttrain", "trota"]
examples: (TC-4922) `ppe` open ["tgq", "tg1", "tgr", "tg2", "tgx"] → stops ["tg1", "tg2", "tgq", "tgr", "tgx"] (view 3's per-project order)
examples: (TC-4925) a project with no milestone (the PRES-V3 board) → stops = `open_t`, same order

present_deck_boards
req: LLR-4654.1
in: tuple[str|None, str, str, Board] lane; str? project_id
out: list[tuple[str|None, str, str, Board]] lanes
func: UNCHANGED on purpose (slice row "—"). The `x` deck's scope keeps reading `present_tasks_m(…)[1]` in board order; it never calls `present_stop_order`, never reads a cursor, a fold or a view-3 stop. S keeps calling it as at base (app.py:648)
module: taskboard/views.py
examples: (TC-4931) MR-F, `x` in views 1, 2 and 3 → each deck file's sha256 equals the base oracle captured on `8ca174c` from the same fixture; `3`/`3`
examples: (AT-4656) the proxy for `ppr` holds the 9 shown tasks, `tm1` (reached) included, in the order base holds them; `present_stop_order` is not called (its 8 open stops would drop `tm1`)

## Entities

[Data: present stop order]
in: list[Task]
desc: NEW. `present_stop_order(present_tasks_m(board, pid)[0])`. V reads it in `render_present` (cursor fallback, field, briefs, blocks) and `_all_plan` (view 3); S reads it in `PresentScreen._shown_ids`. Its first element is the cursor fallback on both sides, so the renderer's cursor and S's `_cursor` always agree (SEAM-2)

[Data: PresentAll.stops]
in: list[tuple[str, str]]
desc: CHANGED content, same type. View 3's stops in screen order: per drawn project ("proj", id), then one ("task", id) per drawn milestone in walk order, ALL mapped by `_all_layout`'s `rows` to the one milestone-row line, then one ("task", id) per drawn task. S's `_stops`, `action_move` and `_hide_all` read it as at base

[Data: present label column]
in: str
desc: the field row's first `label_w` cells (`_present_cols`: 30 from 100 columns, else 20). On the milestone row: ` `, the lead (`⟦` in `accent` bold when the cursor is a member, else a blank), `▎` in the project's hue, then `gantt_lane_label(lane, sel, board, ax, today, label_w - 3)`, padded to `label_w`. `label_w - 3` is 27 at 30 and 17 at 20, so the `milestones`/`ms` switch (24) falls between the two

## Edges

milestone_walk_key ──▶ present_stop_order
milestone_walk_key ──▶ gantt_plan
present_stop_order ──▶ [Data: present stop order]
[Data: present stop order] ──▶ render_present
[Data: present stop order] ──▶ _all_plan
[Data: present stop order] ──▶ PresentScreen._shown_ids
_all_layout ──▶ [Data: PresentAll.stops]
[Data: PresentAll.stops] ──▶ PresentScreen.action_move
when: view 3, through `_stops()`
[Data: PresentAll.stops] ──▶ PresentScreen.action_hide
when: view 3, through `_hide_all`
gantt_lane_label ──▶ [Data: present label column]
when: through `_present_lane_row`, width `label_w - 3`

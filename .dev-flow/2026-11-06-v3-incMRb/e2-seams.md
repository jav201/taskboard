# E2 seams — Inc MR-b (the presentation's milestone row)

There are 2 groups. **V** owns `taskboard/views.py` (`graph-proto-V.cw.md`, 7 nodes), and **S** owns `taskboard/app.py` (`graph-proto-S.cw.md`, 5 nodes: one changed, four with unchanged code). The frozen contracts are in `graph-interfaces.cw.md` (3 nodes). An implementer proposes a seam change to the orchestrator and never changes a seam alone.

| Seam | Contract | Producer → consumer | Pinned by |
|---|---|---|---|
| SEAM-1 `milestone_walk_key(t) -> tuple` | lifted from `gantt_plan.<locals>.walk_key`, with its body unchanged: `(due is None, due or date.max, title, id)`. The board gantt and `R` share one walk order | V → V `gantt_plan` (board frames byte-equal), V `present_stop_order` | TC-4921, TC-4922; MR-a TC-4833 unchanged |
| SEAM-2 `present_stop_order(open_t) -> list[Task]` | the milestones in walk order, then the other tasks in base order. Pure: it adds and drops nothing. Its `[0]` is the cursor fallback on both sides | V → V `render_present` (field, briefs, blocks, cursor), V `_all_plan`; V → S `PresentScreen._shown_ids` → `_cursor`, `action_move`, `action_hide`, `action_show_all` | TC-4921, TC-4923, TC-4925 |
| SEAM-3 `PresentAll.stops` (view 3) | the same type as at base. Per drawn project: the head; then one ("task", id) per drawn milestone in walk order, all mapped by `rows` to the one milestone-row line; then one stop per task. The overflow cut and the cursor fallback are as at base | V `_all_layout` / `_all_timeline` → S `_stops`, `action_move`, `_hide_all`, `action_view` | TC-4922, TC-4906, TC-4924 |
| SEAM-4 `gantt_milestone_row`, `gantt_lane_label` (MR-a SEAM-7) | reused UNCHANGED: no parameter and no branch. The label column passes `label_w - 3`. Each field label stays ONE escaped run (R-7 LABEL PATH) | MR-a V → MR-b V `_present_lane_row` | TC-4911, TC-4913, TC-4914, TC-4916; MR-a TC-4811..TC-4825, TC-4820 unchanged |
| SEAM-5 cell tones `rev:<style>`, `run:<tone>` and the glyph `""` (MR-a SEAM-8) | `_present_field` paints them as `_gantt_field` does. A run is painted as given and is never split or re-escaped; `""` paints nothing. Every other cell is painted as at base (today rule `bright` bold) | MR-a `gantt_milestone_row` → V `_present_field` | TC-4912, TC-4916, TC-4918 |
| SEAM-6 `present_deck_boards` | UNCHANGED on purpose. The deck reads `present_tasks_m(…)[1]` in base order, never the stop order, a cursor or a fold | V → S (`x`, app.py:648) | TC-4931, AT-4656 |
| SEAM-7 keys and the `?` window | `PRESENT_KEYS`, `present_bindings()`, `PresentKeys(view).lines()` and the hint row are unchanged (R-2) | keymap → S | TC-4926 |

**Cross-group ATs** (one tester): AT-4651, AT-4652, AT-4653 and AT-4654 cross SEAM-2 and SEAM-3 (V draws, S steps or hides). AT-4655 crosses SEAM-4, SEAM-5 and SEAM-7. AT-4656 is SEAM-6 only.

**Order of work:** V lands SEAM-1 and SEAM-2 first. S's one change (`_shown_ids`) imports `present_stop_order` and nothing else.

## Findings for the orchestrator (detail in `graph-proto-V.cw.md` § Findings; no requirement was changed)

| Id | Severity (proposed) | What | Proposed ruling |
|---|---|---|---|
| E2-F1 | MAJOR | AT-4655 ("widths kept" in view 1) cannot pass. On a `\` title, `_present_brief` doubles the backslash and the line is width + 1 (P-9). The unit is outside the slice | add `_present_brief` (`escape` → `_literal`), giving 10 units, or narrow AT-4655 to the row |
| E2-F2 | MINOR | LLR-4652.4 and AT-4651 quote the uncut label at 80 columns. The row gives ` ⟦▎ ■ Rubric sign-…` and ` ⟦▎ ▲ Store li… 2/2` | tests assert the graph's per-width strings |
| E2-F3 | MINOR | AT-4653: "at 80x24 the overflow folds fewer projects than at base" cannot be met, because base folds 0 there | move the clause to 118x18 or 80x18 (base folds 2, new 0) |
| E2-F4 | MINOR | the milestone row's gutter is unspecified. The design draws a blank (MR-a LLR-4601.8) | a ledger note, or a new LLR |
| E2-F5 | NOTE | LLR-4652.8 holds for the same cursor only. LLR-4653.3 moves `ppd`'s default cursor, so its tick row follows | E4 compares base and new with the same cursor |
| E2-F6 | NOTE | PRES-V3 and PRES-V4 are milestone-free: they are byte guards, not the re-baselines that §6 says | E4 keeps them byte-equal |
| E2-F7 | MINOR | LLR-4654.1's negative control may be vacuous on MR-F. Its board order already equals the stop order, so only `tm1` would drop | E4 proves the NC RED by order, or adds a fixture |

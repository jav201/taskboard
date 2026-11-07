# Code-Wire prototype — Inc MR-b — group V (`taskboard/views.py`)

Only the differences from `graph-baseline.cw.md` (2ce3943). The shared contracts (`milestone_walk_key`, `present_stop_order`, `present_deck_boards`, the stop and label-column entities) are in `graph-interfaces.cw.md`; MR-a's `gantt_milestone_row`, `gantt_lane_label` and `_lane_marks` are reused unchanged. Sources, fixture and ids: as in `graph-interfaces.cw.md`. Line numbers in the examples are frame lines (0 = the header). Field widths (`_present_cols`): views 1/2 at 118 → label 30, field 73; at 100 → 30, 55; at 80 → 20, 45. View 3 with the rail at 118 → the timeline is 93 wide, label 20, field 58; at 80 (no rail) → label 20, field 45.

## Nodes

gantt_plan
req: LLR-4653.1, LLR-4653.2
in: Board board; bool show_archived; str? selected_id; date today; int body_rows; str? focus = None; str? previous = None; str? pinned = None; bool done_rows = False
out: list[GanttGroup] groups
func: CHANGED in one place only: the nested `walk_key` def is removed and its one use (A-5) calls the module's `milestone_walk_key`. Every other line, and every output, is as at 2ce3943 (MR-a's invariant: the board gantt's frames stay byte-equal)
module: taskboard/views.py
examples: (TC-4921) MR-F, `done_rows`, selected "tm3" → `ppr`'s lane ["tm1", "tm2", "tm3", "tm4", "tm5"], as MR-a's TC-4833
examples: (TC-4922) every MR-a board-gantt oracle (`tests/test_milestone_row*.py`) unchanged: `0` assertions edited

_present_lane_row
req: LLR-4651.3, LLR-4651.8, LLR-4652.1, LLR-4652.3, LLR-4652.4, LLR-4652.5, LLR-4652.6, LLR-4652.7
in: tuple[Task, ...] lane; str? cursor_id; Board board; _PresentGeo p
out: str row
func: NEW. The presentation's milestone row, `p.width` cells: `sel` = `cursor_id` when it names a member of `lane`, else None. Label column (`[Data: present label column]`): ` ` + lead (`⟦` accent bold when `sel`, else ` `) + `▎` in `p.hue` + `gantt_lane_label(lane, sel, board, p.ax, p.today, p.label_w - 3)`, padded to `p.label_w`. Gutter: one blank (no `gantt_dep_mark`; LLR-4651.8, carrying MR-a's LLR-4601.8; RB-5). Field: `_present_field(gantt_milestone_row(lane, sel, board, p.ax, p.today), p.ax)`. Chip: ` ` + `_present_chip(None, m.due_date, p.today, p.chip_w)` for `m` = the `sel` member, else the first member in walk order with a due on or after `p.today`, else `p.chip_w + 1` blanks. Every label is MR-a's (R-7): no title is cut, escaped or laid here
module: taskboard/views.py
examples: (TC-4911) view 1, 118x30, cursor "tm3" → the field's plain holds `■2 Steerin…`; the `rev:violet` cell is field cell `18`; cursor "tm4" → `▲2 Store l…`, `rev:cyan` at cell `18`
examples: (TC-4911) view 1, 118x30, cursor "tstore" (a task) → field plain holds `■ ▲1d`, `■2 Oct 24`, `★ Oct 30`; no cell has a `rev:` tone; at 80x24 → `▲1d ■`, `■2`, `★ Oct 30`
examples: (TC-4911) view 3, cursor ("task", "tm3") → the field equals `gantt_milestone_row(lane, "tm3", board, ax, today)` on view 3's own axis (`_all_axis`), painted by `_present_field`
examples: (TC-4913) cursor "tstore" → label column `  ▎ ◆ 4 milestones ▲1` at 118 (`label_w - 3` = 27 ≥ 24) and `  ▎ ◆ 4 ms ▲1` at 80 (17)
examples: (TC-4914) cursor "tm2" → ` ⟦▎ ■ Rubric sign-off` at 118, ` ⟦▎ ■ Rubric sign-…` at 80
examples: (TC-4914) cursor "tm4" → ` ⟦▎ ▲ Store list frozen   2/2` at 118, ` ⟦▎ ▲ Store li… 2/2` at 80 (cut by cell width with `…`, tag kept; RB-3)
examples: (TC-4915) cursor "tm2" → chip `    due Oct 19` in `over`; cursor "tstore" → `    due Oct 24` (tm3, the first due on or after Oct 20); lane ("tm2",) alone (tm3, tm4, tm5 hidden), cursor "tstore" → `14` blanks
examples: (TC-4903) lane = the milestones of `present_stop_order(open_t)`: `ppr` → ("tm2", "tm3", "tm4", "tm5"), `tm1` (reached) absent; class Review hidden → ("tm4", "tm5"); tm3 hidden by `space` → ("tm2", "tm4", "tm5")
examples: (TC-4916) cursor on a milestone titled `a]b[/]`, at 80 → the label column's plain holds `a]b[/]` (or its `…` cut) and the field run is `_literal` of the `fit` cut; line `cell_len` `80`; `0` exceptions
examples: (TC-4916) titles `[@click=app.quit]x`, `\` and `日本語のタイトル`, each the cursor, views 1 and 3 at 80x24 → plain literal, `0` spans with `@click` or meta, line `cell_len` = width; `8`/`8`
examples: (TC-4908) MR-F, m3 waiting on `store`, cursor "tm3", views 1 and 3 at 118x30 and 80x24 → the cell at `p.label_w` (the gutter) is a blank; no `↳` on the line; `4`/`4`
examples: (TC-4917) every width → `cell_len(row)` = `p.width`: label `p.label_w` + gutter `1` + field `p.field_w` + chip `p.chip_w + 1`
examples: (AT-4651) view 1, 118x30, cursor "tm2" → line `5` reads ` ⟦▎ ■ Rubric sign-off`, then `■` reversed in violet with `Rubric…` after it, then `■2 Oct 24`, `★ Oct 30`, chip `due Oct 19`
examples: (AT-4655) a hostile title walked onto in views 1 and 3 at 80x24 → this row stays literal and `80` cells (the brief line: `_present_brief`, LLR-4652.9)

_present_field
req: LLR-4652.2, LLR-4652.6, LLR-4652.8
in: list[tuple[str, str]] cells; GanttAxis ax
out: str markup
func: CHANGED: three branches before base's, taken from `_gantt_field` (SEAM-8): a `""` glyph (a consumed label cell) paints nothing; a `run:<tone>` cell paints its glyph (one field label run, already cut by `fit` and escaped once by `_literal` upstream) as `c(glyph, <tone>)`, never split, re-measured or re-escaped; a `rev:<style>` cell paints `[b reverse HEX[<style>]]<glyph>[/]`. Every other cell is painted as at base (the today rule `bright` bold; `crit`/`accent` glyphs `bright` bold). No caller sends a weekend set: the present field has no shading. E4 checks that no base caller sends a `""` glyph (the PRES-V3/V4 frames stay byte-equal)
module: taskboard/views.py
examples: (TC-4912) `ppr` at 118, cursor "tm2": cell `8` ("■", "rev:violet") → `[b reverse <HEX violet>]■[/]`; base raises KeyError `rev:violet` (P-8)
examples: (TC-4912) the `Rubric…` run in its first cell + `6` consumed cells → `Rubric…` painted once; the field's plain is `73` cells; no doubled glyph, no stray `violet`/`bright` word in the plain
examples: (TC-4916) a run cell holding `_literal("a]b[/]")` → `Text.from_markup` of the row parses; plain holds `a]b[/]`
examples: (TC-4918) the span row and every task bar → markup byte-equal to base (no `""`, `run:` or `rev:` cell reaches them)

render_present
req: LLR-4651.1, LLR-4651.3, LLR-4651.4, LLR-4651.5, LLR-4652.7, LLR-4652.8, LLR-4653.3, LLR-4653.5
in: Board board; str? project_id; str? cursor_id; date today; int width; int height; str view = "gantt"; int scroll = 0
out: Text frame
func: CHANGED. `stops = present_stop_order(open_t)`; `lane` = its milestones (they lead it, in walk order). The cursor is `cursor_id`'s task when it is in `open_t`, else `stops[0]`, else None. The field: the span row; then, when `lane` is not empty, ONE `_present_lane_row(lane, cursor.id, board, p)`; then one `_present_task_row` per task of `stops[len(lane):]` (the non-milestones in `open_t` order), so the field and the briefs read one list (A-4, SEAM-2). View 1: one brief per task of `stops`, the cursor's note under its brief; the note room is still `max(3, height - len(lines) - len(open_t))`. View 2: the blocks over `stops`, split at `half = (len(stops) + 1) // 2` from 100 wide. The header, the ruler (its echo is the cursor task's, as at base), the legend strip and the axis are computed as at base from the same `open_t`
module: taskboard/views.py
examples: (TC-4901) `ppr`, view 1, 118x30, no cursor → line `4` the span, line `5` the milestone row (m2..m5 marks), lines `6`–`9` the 4 tasks, line `10` the rule; no other field line holds `■`, `▲` or `★`; view 2 the same lines; `2`/`2`
examples: (TC-4901) HLR-4651: the same frame has `5` field body rows (base `8`)
examples: (TC-4903) view 1 `ppr` → line `5` holds the marks of tm2..tm5 only (`⬢`/`⬡` of tm1 absent); class Review hidden → line `5` holds `▲` and `★` only
examples: (TC-4904) lines `6`–`9` = `Pilot store list`, `Pilot telemetry`, `Train store staff`, `Field support rota` (base order); views 1 and 2
examples: (TC-4905) `ppd` with th1 hidden → field = span + 2 task rows (`API reference`, `Runbook draft`), no milestone row; the PRES-V3 board (no milestone) → frames byte-equal to `PRES-V3-gantt-118x30.txt` and `-80x24.txt`
examples: (TC-4923) `ppr`, no cursor → cursor "tm2"; `ppd`, no cursor → cursor "th1" (`⟦Handover call⟧`; base `⟦API reference⟧`, P-7); cursor_id "tm3" after tm3 is hidden → "tm2", the first stop
examples: (TC-4925) view 1 `ppr` → briefs lines `11`–`18`: Rubric sign-off, Steering go/no-go, Store list frozen, Pilot launch, Pilot store list, Pilot telemetry, Train store staff, Field support rota
examples: (TC-4925) view 2 `ppr` 118x30 → left column Rubric sign-off, Steering go/no-go, Store list frozen, Pilot launch; right column Pilot store list, Pilot telemetry, Train store staff, Field support rota
examples: (TC-4917) views 1, 2 × {118x30, 100x30, 80x24}, cursor "tm3" → max `cell_len` per line ≤ width; `6`/`6` (view 3: `_all_timeline`)
examples: (TC-4918) views 1, 2 × {118x30, 80x24}, cursor "tm2" → the header `8 open · ▲1 past due`, ruler lines `1`–`2`, the legend strip line `3`: plain equal to base
examples: (AT-4651) view 1 at 118x30 and 80x24: span, one milestone row, 4 task rows; the briefs follow m2, m3, m4, m5, then the tasks
examples: (AT-4652) view 2 (`2`): the same field; the blocks in stop order

_all_plan
req: LLR-4652.8, LLR-4653.2
in: Board board
out: list[tuple[Project, list[Task]]] plan
func: CHANGED: each shown project's open list is `present_stop_order(present_tasks_m(board, p.id)[0])`. The set is unchanged, so `_all_label`'s counts, `_all_axis` and the header's open count are as at base
module: taskboard/views.py
examples: (TC-4922) MR-F → [("ppr", ["tm2", "tm3", "tm4", "tm5", "tstore", "ttele", "ttrain", "trota"]), ("ppe", ["tg1", "tg2", "tgq", "tgr", "tgx"]), ("ppd", ["th1", "tha", "thr"])]
examples: (TC-4918) the view-3 header still reads `16 open · ▲1 past due`; the `ppe` head still `5`

_all_layout
req: LLR-4651.6, LLR-4651.7, LLR-4653.2
in: list plan; str? cur_pid; frozenset folded; int room
out: tuple(dict open_, bool gap, list stops, dict rows)
func: CHANGED. An unfolded project costs 1 head + 1 milestone row when it has a milestone + 1 row per non-milestone, in `need` and in the lines. Stops in screen order: ("proj", id); then, when unfolded, one ("task", m.id) per milestone in plan (walk) order, ALL mapped in `rows` to the one milestone-row line; then one ("task", t.id) per non-milestone, each its own line. A folded project (by hand or by the overflow rule) adds only its head. The fold rule itself (furthest from the cursor's project first, never the cursor's) is as at base
module: taskboard/views.py
examples: (TC-4907) MR-F, room `15` (118x18): need = 6 + 5 + 4 = `15` → nothing folded (base folds ppe and ppd, P-4); rows = 3 heads + 3 milestone rows + 9 task rows; no gap (17 > 15)
examples: (TC-4906) room `11` (80x14): need `15` → ppd then ppe folded → need `8`, gap fits (`10`): `▸` heads, no milestone row under them
examples: (TC-4906) `ppe` in `folded` (enter), room `27` → stops hold ("proj", "ppe") and no ("task", "tg1"), ("task", "tg2")
examples: (TC-4922) room `27`, cursor "ppr" → stops begin [("proj","ppr"), ("task","tm2"), ("task","tm3"), ("task","tm4"), ("task","tm5"), ("task","tstore")]; rows of tm2..tm5 all `4`; tstore `5`
examples: (AT-4653) at 118x18 the overflow folds `0` projects where base folds `2` (RB-4)

_all_timeline
req: LLR-4651.2, LLR-4651.3, LLR-4651.6, LLR-4652.7
in: Board board; int width; int height; date today; tuple? cur; frozenset folded; bool rail_focus
out: tuple(list[str] lines, list stops, tuple? cur)
func: CHANGED: per project its head row; when unfolded, its milestones (the leading milestones of its plan list) as ONE `_present_lane_row(lane, cur[1] if cur is a task else None, board, pg)` directly under the head, then one `_present_task_row` per non-milestone. The overflow cut, the cursor fallback and the ruler are as at base; a cursor on a milestone stop is the row's `sel`
module: taskboard/views.py
examples: (TC-4902) MR-F at 118x30 → heads at lines `3`, `10`, `16`; milestone rows at `4` (m2..m5), `11` (`▲` g1, `■` g2), `17` (`◆` h1); `3`/`3`
examples: (TC-4903) the row under `ppr`'s head holds tm2..tm5 and no tm1; with class Review hidden, tm4 and tm5 only
examples: (TC-4906) `enter` on Eval harness → line `10` `▸ ■ Eval harness`, the next drawn head `▸`/`▾ ■ Docs & handover` with no milestone row between
examples: (TC-4917) view 3 × {118x30, 100x30, 80x24}, cursor ("task", "tm3") → max `cell_len` ≤ width; `3`/`3`
examples: (AT-4653) `3` at 118x30: under each head one milestone row, then the tasks

_present_task_row
req: LLR-4651.1, LLR-4651.4
in: Task task; Board board; _PresentGeo p; bool cursor = False
out: str row
func: CHANGED (A-2): the `if task.milestone:` branch (its mark, `gantt_milestone_cells`, the dependency gutter and the due chip) is removed. Both callers, `render_present` (`stops[len(lane):]`) and `_all_timeline` (the non-milestones of the plan list), pass only non-milestones; a milestone is drawn only by `_present_lane_row`. The task row is as at base: `  ▎ <title>`, the gutter, its bar (`⟦━⟧` on the cursor) and its start–end chip. `gantt_milestone_cells` keeps its caller in the board gantt
module: taskboard/views.py
examples: (TC-4904) `tstore` at 118x30, cursor on it and off it → markup byte-equal to base's row for `tstore`
examples: (TC-4901) MR-F, views 1, 2 and 3 → `0` field lines outside the milestone row hold `■`, `▲`, `★` or `◆`; the mark-site list in `tests/test_milestone_marks.py` names `_present_lane_row`, not `_present_task_row`

_present_brief
req: LLR-4652.9
in: Task task; _PresentGeo p; bool cursor; int width
out: str line
func: CHANGED (RB-2, SEC-B1): the title is `c(_literal(txt), tone, bold=True)`, with `txt = clip(task.title, max_title)` as now, in place of `c(escape(txt), …)`. `_literal` closes a trailing backslash run with its own tag, which survives `collapse_runs` merging the title with the same-style `⟧`, and it keeps a `\` before a non-tag `[`. `gap` is still measured on the raw `txt`. `_present_finish`'s width assert is left as it is (A-6)
module: taskboard/views.py
examples: (TC-4919) view 1 at 80x24, cursor on a task titled `x\` → the brief's plain reads `⟦x\⟧`, one backslash; `cell_len` of the line in `render_present(…).plain` = `80` (base `81`, `⟦x\\⟧`); at 118x30 → `118` (base `119`)
examples: (TC-4919) titles `\` and `a\[b]` as the cursor → `⟦\⟧` and `⟦a\[b]⟧` (base `a[b]`); every line `cell_len` = width; `6`/`6`
examples: (TC-4919) a title with no `[` and no trailing `\` → markup byte-equal to base (`_literal` and `escape` return the same string)
examples: (AT-4655) `x\` and `a\[b]` walked onto in view 1 at 80x24 → the brief literal, `80` cells

_present_heading
req: LLR-4652.10
in: Task task; int w; bool on; str hue; date today; bool empty
out: str row
func: CHANGED (SEC-B3): the title is `c(_literal(clip(task.title, tw)), …)` in place of `c(escape(clip(task.title, tw)), …)`; `tw`, the bar, the dates and the padding are as at base
module: taskboard/views.py
examples: (TC-4920) view 2 at 118x30, a task titled `a\[b]` → the block's first row holds `a\[b]` (base `a[b]`); `\[x` → `\[x` (base `[x`); `ab\[` + 60 `x`, cut → `ab\[x…` (base `ab[x…`); each line of the rendered frame = width; at 80x24 the same; `6`/`6`
examples: (TC-4920) a title with no `[` and no trailing `\` → markup byte-equal to base
examples: (AT-4655) `a\[b]` walked onto in view 2 at 80x24 → the block heading literal, `80` cells

## Findings

finding E2-F1 AT-4655 "widths kept" cannot hold in view 1 without a unit outside the slice
anchor: render_present
seen: (P-9, baseline-notes.md) a milestone titled `\` or `x\` as the cursor in view 1 at 80x24 → the brief line reads `⟦\\⟧` and is `81` cells; views 2 and 3 are `80`
cause: `_present_brief` builds its title with `escape(clip(…))`, the escape R-7 rejected for cut pieces; `_present_finish` measures markup, not the rendered line, so it does not catch it
effect: AT-4655 (each hostile title walked onto in views 1 and 3 at 80x24, widths kept) fails on the `\` title whatever the milestone row does; LLR-4652.6 (the row only) holds
decision: RULED RB-2 with SEC-B1 and SEC-B2 (LED .3): option (a), `_literal` only; `_present_brief` is node and slice unit 10; LLR-4652.9 measures the rendered frame

finding E2-F2 the 80-column label literals in LLR-4652.4 and AT-4651 are uncut
anchor: _present_lane_row
seen: (P-6) `gantt_lane_label` at `label_w - 3` = 17 cuts the cursor title at 80: ` ⟦▎ ■ Rubric sign-…`, ` ⟦▎ ▲ Store li… 2/2`
cause: LLR-4652.4's threshold writes `⟦▎ ▲ Store list frozen 2/2` "(cut, tag kept, at 80)", and AT-4651 writes `⟦▎ ■ Rubric sign-off` for both 118x30 and 80x24
effect: a test that asserts the literal as written fails at 80 for a correct row
decision: RULED RB-3 (LED .5): LLR-4652.4 and AT-4651 now quote the cut form at 80

finding E2-F3 AT-4653's 80x24 overflow clause cannot be met
anchor: _all_layout
seen: (P-4) at 80x24 base folds no project of MR-F (room 21, need 19); the design needs 15
cause: AT-4653 says "At 80x24 the overflow folds fewer projects than at base"; fewer than 0 is not possible
effect: the clause has no passing outcome; LLR-4651.7's own example (118x18: base folds 2, the design 0) shows the intent
decision: RULED RB-4 (LED .6): AT-4653's clause is at 118x18

finding E2-F6 the PRES-V3 and PRES-V4 frames are guards, not re-baselines
anchor: render_present
seen: `tests/present_board.py` and `tests/present_notes_board.py` hold no milestone (baseline-notes.md B-1)
cause: 01-requirements.md §6 lists PRES-V3, PRES-V4 and the `test_present*` family among the frames that pin one row per milestone
effect: under this design the 7 frame-oracle test functions named in baseline-notes.md stay byte-equal; a change in them is a regression
decision: E4 keeps them byte-equal and re-baselines only the tests on milestone boards, one at a time, each citing its LLR

finding E2-F4 the milestone row's dependency gutter is not specified
anchor: _present_lane_row
seen: base draws `gantt_dep_mark` on each milestone's own row; MR-a's row draws a blank gutter (LLR-4601.8); no MR-b LLR names the gutter
cause: MR-b carries LLR-4602/4603 but not LLR-4601.8
effect: the design draws one blank (MR-a's rule), and no requirement or test pins it
decision: RULED RB-5 (LED .7): LLR-4651.8 (TC-4908)

finding E2-F5 LLR-4652.8 holds only for the same cursor
anchor: render_present
seen: the tick row echoes the cursor task; LLR-4653.3 moves the default cursor of `ppd` from `tha` to `th1`
cause: the ruler is unchanged; its input, the cursor, changes by design
effect: on `ppd` with no cursor the tick row differs from base; on MR-F's `ppr` (the LLR-4652.8 threshold) the cursor is `tm2` in both, so the threshold holds
decision: E4 runs TC-4918 with the same cursor on base and new, as written

finding E2-F7 LLR-4654.1's negative control may be vacuous on MR-F
anchor: present_deck_boards
seen: in MR-F every project lists its milestones first (`TASKS`), so the board order of the open tasks already equals the stop order (`ppr` m2..m5, then the 4 tasks)
cause: the NC "the deck's proxy holding tasks in stop order" changes only `tm1`'s presence on MR-F
effect: the NC may turn RED for dropping `tm1`, not for the order it is meant to catch
decision: RULED RB-6 with A-1 (LED .8): the NC mutates which tasks the deck holds (drops `tm1`); an order-only mutant cannot fail, since the deck re-sorts by board position; no extra fixture

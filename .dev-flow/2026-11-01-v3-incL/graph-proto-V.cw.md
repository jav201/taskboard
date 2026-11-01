# Code-Wire prototype — group V (taskboard/views.py) — Inc L, the added-order list view

Differences from `graph-baseline.cw.md` (eb411e1) only: every node below is NEW in views.py; no baseline node changes. Group V owns the rows, the inference, the order and the whole body of the list view. The seven interface nodes and `[Data: AddedRow]` of `graph-interfaces.cw.md` are cited, never redefined: the five data nodes appear here with their `in:`/`out:` copied exactly, a `func:` that only adds implementation notes, and extra examples for this group's LLRs; `render_added_list` appears with its internals. New internal nodes: `_added_head`, `_added_plan`, `_added_day_label`, `added_time_label`, `_added_row`, `_added_top`, `_added_pane`, `_added_meta`, `added_source_line`, `_one_line` (10), plus the constant `ADDED_LEGEND`. Every example was run against a scratch reference of this design outside the repo (`%TEMP%/incL-V/ref.py`, importing the capture-proto worktree's `taskboard`, `taskboard.__file__` = `…\capture-proto\taskboard\__init__.py`; `created` set through `extra` since base `Task` has no field yet); no product code or test was edited. E3 round-1 corrections (ARCH-1, ARCH-3, ARCH-8, SEC-2, SEC-3, SEC-4/A-3; findings at the end) were NOT run on that reference: their new examples say `planned`, except the shuffled-input orders of TC-4364/TC-4365, run on a pure reference sort (`executed`, see added_order). Reused helpers of views.py, named: `fit` (views.py:98), `clip` (:906), `vis` (:87), `project_color` (:255, the board's project-hue rule: a PROJECT_COLORS key, `dim` for the Inbox), `board_hex` (:696), `milestone_mark` (:2593, THE milestone seat), `mention_names` (:3619), `notes_text` (:3646), `_SEARCH_CONSOLE` (:4135, a module Console that does no I/O), `HEX` (:45); `parse_iso` from models.

### Fixture F-V (synthetic; clock today 2026-11-01, now 2026-11-01T08:10:00 as in graph-interfaces)

> Lane 0 `("Work", "sky", work, "")`, phases Backlog · Doing · Review · Done, project p1 "Eval harness" (colour blue). File order:
> w1 "Volume oracle script" p1 Backlog, no created, no birth · w2 "Sync notes" p1 Doing, created "2026-10-31T18:20:00", priority high, start 2026-10-30, due 2026-11-03, milestone True (mark None), notes "::b:: ask the vendor ::\nping @ana before Friday", urls ["https://example.com/spec"], images ["img/w2/board.png"], depends_on ["w3"] · w3 "Pilot store list" p1 Review, no created; history.jsonl births for w3 at "2026-10-28T10:30:00" then "2026-10-29T11:00:00" · w4 "Pay the rent" p1 Backlog, created "2026-11-01T08:10:00" · w5 "Old archived" p1 Done, archived True, no created, no birth.
> Lane 1 `("Home", "lime", home, "")`, phases Todo · Doing · Done, project p2 "House" (green). h1 "Hybrid search index" no project (Inbox) Todo, no created, no birth · h2 "Compose file anatomy" p2 Done, created "2026-10-31T21:47:00".
> people = {"ana": Person("ana", "Ana Ruiz")}. first = first_created(all 7 rows) = 2026-10-31 18:20. hidden = 1 (w5).
> Newest first, archived hidden: w4, h2, w2, w3, h1, w1. Oldest first: w1, h1, w3, w2, h2, w4.

### Body at 118x30 (render width 116, height 29), newest first, sel = 2 (w2); every line exactly 116 cells, trailing spaces not shown; lines 12–28 are 46 spaces + " │ " + 67 spaces

> ```
>  0 ADDED  6 tasks · every board · newest first  ·  time = created  ≈ = history  ? = unknown · 1 archived hidden
>  1
>  2 TODAY                                          │ Sync notes
>  3  08:10  ■□□□ ▍Pay the rent                     │ Eval harness · Work
>  4 YESTERDAY                                      │ Doing  ▲ high  Oct 30→Nov 3  ◆ milestone  @Ana Ruiz  ↗ 1  ▤ 1
>  5  21:47  ■■■  ▍Compose file anatomy             │ added Sat Oct 31 · 18:20 · the created field
>  6 ▶18:20  ■■□□ ▍Sync notes                       │ ───────────────────────────────────────────────────────────────────
>  7 WED OCT 28 ≈                                   │ ask the vendor
>  8  ≈10:30 ■■■□ ▍Pilot store list                 │ ping @Ana Ruiz before Friday
>  9 BEFORE OCT 31 · ?                              │ ↗ https://example.com/spec
> 10  ?      ■□□  ▍Hybrid search index              │ ▤ board.png
> 11  ?      ■□□□ ▍Volume oracle script             │ after: Pilot store list
> ```

### Body at 80x24 (render width 78, height 23), same state; every line exactly 78 cells; lines 14–22 are 34 spaces + " │ " + 41 spaces

> ```
>  0 ADDED  6 tasks · newest first  ·  time = created  ≈ = his… · 1 archived hidden
>  1
>  2 TODAY                              │ Sync notes
>  3  08:10  ■□□□ ▍Pay the rent         │ Eval harness · Work
>  4 YESTERDAY                          │ Doing  ▲ high  Oct 30→Nov 3  ◆ milestone
>  5  21:47  ■■■  ▍Compose file anatomy │ @Ana Ruiz  ↗ 1  ▤ 1
>  6 ▶18:20  ■■□□ ▍Sync notes           │ added Sat Oct 31 · 18:20 · the created
>  7 WED OCT 28 ≈                       │ field
>  8  ≈10:30 ■■■□ ▍Pilot store list     │ ─────────────────────────────────────────
>  9 BEFORE OCT 31 · ?                  │ ask the vendor
> 10  ?      ■□□  ▍Hybrid search index  │ ping @Ana Ruiz before Friday
> 11  ?      ■□□□ ▍Volume oracle script │ ↗ https://example.com/spec
> 12                                    │ ▤ board.png
> 13                                    │ after: Pilot store list
> ```

### Performance of one paint (the screen repaints on every key)

> For N listed rows, T tasks on the cursor's board and a cursor note of L characters: `added_order` (called by S each paint) O(N log N); `render_added_list` O(N) for the plan (one tuple and one `date` per row, no Text built) and the state-column width (one `min(8, len(phases))` per row), O(room) for the visible Text rows (room = height − 2), O(min(L, room × (rw + 1))) to wrap the cursor's note (the A-3 cut; SEC-4 measured 0.92 s for an uncut 5 MB wrap), O(T) to resolve `after:` titles. Nothing is computed per task for the pane: `notes_text`, the wrap, `mention_names` and the `after:` dict are built for the cursor's task only (a hard rule of `_added_pane`: it takes ONE row). `history.read` runs once per board at compose (S), never in a paint. Measured on the scratch reference (one board, a third of the tasks unknown, 118x30): N = 500 → order 0.1 ms + render 1.0 ms; N = 2 000 → 0.3 + 1.7 ms; N = 20 000 → 3.4 + 8.7 ms (state `executed`). No limit is needed; S may cache the two orders per archived state, but at these numbers it need not.

## Nodes

render_added_list
req: HLR-4303, LLR-4303.7, LLR-4303.8, LLR-4303.9, LLR-4303.10, LLR-4303.15, LLR-4303.17, LLR-4304.14, LLR-4306.6, LLR-4305.3
in: list[AddedRow] rows; int sel; bool newest; bool show_archived; int hidden; int unread; datetime? first; date today; dict people; int width; int height
out: Text body
func: interface node (graph-interfaces.cw.md), internals: width = max(1, width); lw = 46 if width >= 100 else 34; rw = max(0, width − lw − 3); room = max(0, height − 2). Line 0 = `_added_head(len(rows), newest, show_archived, hidden, unread, width)`; line 1 = `width` spaces. Left column: when rows is empty, one line `fit("no tasks to list", lw)` in HEX["dim"] and no pane; else sel = max(0, min(sel, len(rows) − 1)), sw = max(min(8, len(r.board.phases)) for r in rows) (= the widest `state_boxes` length among the listed rows), plan = `_added_plan(rows, today, first)`, top = `_added_top(plan, sel, room)`, and each of plan[top:top + room] becomes a day header `Text(fit(label, lw))` (style `b` + HEX["dim"] when the label starts with "BEFORE ", else `b` + HEX["hd"]) or `_added_row(rows[i], i == sel, sw, lw)`. Pane, cut = `_added_pane(rows[sel], first, people, today, rw, room)`; when cut (the note was longer than the pane can show, A-3 / SEC-4) it keeps min(len(pane), room − 1) lines and ends with `clip("… more lines", rw)` in HEX["dim"] (no count: the cut note's real length is never wrapped); else, when it has more than room lines, it keeps room − 1 and ends with `clip(f"… {k} more lines", rw)` in HEX["dim"], k = the lines left out + 1 (P-V-7). Body line 2 + k (k in 0..room−1) = left line k (or lw spaces) + " │ " in HEX["frame"] + pane line k copied, `no_wrap`, `truncate(rw, overflow="ellipsis")`; each line then `truncate(width)` and `pad_right` to exactly `width` cells; lines joined with "\n", at most max(1, height) lines. Built only from `Text.append(str, style)` pieces: no markup parser anywhere. Pure: reads its inputs, writes nothing.
module: taskboard/views.py
examples: (TC-4327) F-V newest, sel `2`, width `116`, height `29` → `29` lines, each `116` cells; lines 2–28 hold "│" at index `47` and nowhere else; width `78`, height `23` → `23` lines of `78` cells, "│" at index `35`
examples: (TC-4327) rows `[]`, width `116`, height `29` → lines 2–28 all hold "│" at index `47`
examples: (TC-4328) F-V newest, sel `2`, width `116` → line 6 is "▶18:20  ■■□□ ▍Sync notes" padded to `46` cells, then " │ " and the rule
examples: (TC-4329) F-V newest, width `116` → the day header lines, top to bottom, "TODAY", "YESTERDAY", "WED OCT 28 ≈", "BEFORE OCT 31 · ?" (lines 2, 4, 7, 9)
examples: (TC-4330) F-V newest, sel `2`, width `116` → pane lines 1–5 (body lines 2–6 after index 49) "Sync notes", "Eval harness · Work", "Doing  ▲ high  Oct 30→Nov 3  ◆ milestone  @Ana Ruiz  ↗ 1  ▤ 1", "added Sat Oct 31 · 18:20 · the created field", "─" × `67`
examples: (TC-4337) rows `[]`, hidden `1`, width `116` → body line 2 starts "no tasks to list" (style `#5b6675`) and every pane cell is a space
examples: (TC-4335) one board "Big" of 40 tasks, task k created "2026-10-(1 + k mod 28)T09:kk:00", newest, sel `39` (the oldest, "Task 00"), width `78`, height `23` → body line 22 reads "▶09:00  ■□□ ▍Task 00", line 20 "THU OCT 01"
examples: (TC-4383) a 3-phase board row "Three" (phase A) and a 5-phase board row "Five" (phase C), newest, sel `0`, width `116` → lines "▶07:00  ■□□   ▍Three" and " 06:00  ■■■□□ ▍Five": both titles start at cell `15`
examples: (TC-4383) a 3-phase row and a 10-phase row (phase index 4), width `78` → "▶07:00  ■□□      ▍Three" and " 05:00  ■■■■□□□□ ▍Ten": titles at cell `18`
examples: (TC-4340) title "[red]x[/red]", project "[b]P[/b]", board "[i]B[/i]", notes "[red]x[/red] ::b:: ask the vendor ::", width `116` → row "▶08:00  ■□□ ▍[red]x[/red]", pane lines "[red]x[/red]", "[b]P[/b] · [i]B[/i]", and the note line "[red]x[/red] ask the vendor" with "ask the vendor" in `#60a5fa`
examples: (TC-4335) a task whose notes are 40 lines "line 0".."line 39", width `78`, height `23` → body lines 2..21 hold pane lines 1..20 and body line 22 reads "… 26 more lines" (the 309-character note is under the A-3 cap of at most 15 × 42 = 630 here, so it is not cut and the count stands)
examples: (TC-4335b) a task whose note is `100 000` characters, width `78`, height `23` → body line 22 reads "… more lines" (no count) in `#5b6675` (`planned`; A-3)

_added_head
req: LLR-4304.14, LLR-4303.6, LLR-4306.6
in: int n; bool newest; bool show_archived; int hidden; int unread; int width
out: Text head
func: pieces in order: "ADDED" (`b` HEX["accent"]); B = f"  {n} task{'s' if n != 1 else ''} · every board · " (HEX["mut"]); C = "newest first" or "oldest first" (`b` HEX["ink"]); the legend `ADDED_LEGEND` = "  ·  time = created  ≈ = history  ? = unknown" (45 cells, HEX["dim"]); the tail: f" · {unread} board{'s' if unread != 1 else ''} not read" (HEX["soon"]) when unread > 0, then " · archived shown" (HEX["mut"]) when show_archived, else f" · {hidden} archived hidden" (HEX["mut"]) when hidden > 0. Fitting (tail always kept, so the row ENDS with it): if A+B+C+legend+tail > width (cells, `vis`), B drops "every board · " (f"  {n} tasks · "); then room = width − A − B − C − tail; legend whole when room ≥ 45, `clip(legend, room)` when room ≥ 20, else omitted. Then `truncate(width, overflow="ellipsis")` (only below ~70 cells with both tail pieces) and `pad_right` to width. `n` is the count of listed rows (after the archived filter)
module: taskboard/views.py
examples: (TC-4374) n `6`, newest `True`, hidden `1`, unread `0`, width `116` → "ADDED  6 tasks · every board · newest first  ·  time = created  ≈ = history  ? = unknown · 1 archived hidden"
examples: (TC-4374) same, newest `False` → "ADDED  6 tasks · every board · oldest first  ·  time = created  ≈ = history  ? = unknown · 1 archived hidden"
examples: (TC-4326) n `6`, hidden `1`, unread `1`, width `116` → "ADDED  6 tasks · newest first  ·  time = created  ≈ = history  ? = unknown · 1 board not read · 1 archived hidden"; pieces styled "ADDED" `b #2dd4bf`, "  6 tasks · " `#8b98a5`, "newest first" `b #e6edf3`, legend `#5b6675`, " · 1 board not read" `#fbbf24`, " · 1 archived hidden" `#8b98a5`
examples: (TC-4326) unread `2`, width `116` → ends "· 2 boards not read · 1 archived hidden"; width `78` → "ADDED  6 tasks · newest first · 2 boards not read · 1 archived hidden"
examples: (TC-4396) n `7`, show_archived `True`, width `116` → ends "? = unknown · archived shown"; n `6`, hidden `1`, width `78` → "ADDED  6 tasks · newest first  ·  time = created  ≈ = his… · 1 archived hidden"
examples: (TC-4396) hidden `0`, show_archived `False`, width `78` → "ADDED  6 tasks · newest first  ·  time = created  ≈ = history  ? = unknown" (no archived piece)

_added_plan
req: LLR-4303.9, LLR-4304.11
in: list[AddedRow] rows; date today; datetime? first
out: list[tuple[int, str]] plan
func: the list area's line plan, O(len(rows)), no Text built: one pass marks, per calendar date of a dated row, whether EVERY row of that date is source "h" (hist_only); a second pass walks rows in the given order and emits (−1, label) whenever the row's day key (r.at.date(), or None for an unknown row) differs from the previous row's, then (i, ""). label = `_added_day_label(key, today)` + (" ≈" if hist_only[key]) for a date; for None, "BEFORE " + f"{first:%b} {first.day}".upper() + " · ?" when first is set, else "BEFORE ANY RECORD · ?". Never `%-d` (not portable, P-V-4)
module: taskboard/views.py
examples: (TC-4329) F-V newest → plan [(−1, "TODAY"), (0, ""), (−1, "YESTERDAY"), (1, ""), (2, ""), (−1, "WED OCT 28 ≈"), (3, ""), (−1, "BEFORE OCT 31 · ?"), (4, ""), (5, "")]
examples: (TC-4329) rows c@2026-10-31 18:20 then h@2026-10-31 09:00, today 2026-11-01 → [(−1, "YESTERDAY"), (0, ""), (1, "")] (a day with a created row has no ≈); the h row alone → [(−1, "YESTERDAY ≈"), (0, "")]; an h row at 2026-11-01 07:05 → [(−1, "TODAY ≈"), (0, "")]
examples: (TC-4371) a board "Solo" of 2 tasks, none stamped, no history, first `None` → plan [(−1, "BEFORE ANY RECORD · ?"), (0, ""), (1, "")]

_added_day_label
req: LLR-4303.9
in: date day; date today
out: str label
func: "TODAY" when day == today; "YESTERDAY" when day == today − 1 day; else f"{day:%a %b %d}".upper() (zero-padded day, as LLR-4303.9 writes); a day after today (a created stamped ahead of the clock) gets its date
module: taskboard/views.py
examples: (TC-4329) day 2026-10-28, today 2026-11-01 → label "WED OCT 28"; day 2026-10-05 → "MON OCT 05"; day 2026-11-02 → "MON NOV 02"

added_time_label
req: LLR-4304.9
in: AddedRow row
out: tuple(str label, str style)
func: source "c" → (f"{row.at:%H:%M}", HEX["ink"]); "h" → (f"≈{row.at:%H:%M}", HEX["mut"]); "?" → ("?", HEX["dim"]); the row pads it to 7 cells with `fit`
module: taskboard/views.py
examples: (TC-4369) F-V newest rows → labels "08:10", "21:47", "18:20", "≈10:30", "?", "?" (styles `#e6edf3` ×3, `#8b98a5`, `#5b6675` ×2)

_added_row
req: LLR-4303.8, LLR-4305.3, LLR-4305.4, LLR-4306.5, LLR-4303.20
in: AddedRow row; bool on; int sw; int lw
out: Text line
func: one list row, exactly lw cells, left to right: "▶" if on else " " (HEX["accent"]); `fit(label, 7)` in the label's style (added_time_label); b = `state_boxes(row.board.phases, row.task.phase)`, its "■" run in HEX["ink"] and its "□" run in HEX["dim"] (no other style on those cells); (sw − len(b)) spaces + " " (no style); "▍" in HEX[`project_color(row.board, row.task)`]; `clip(_one_line(title), lw − 10 − sw)` styled `b` HEX["ink"] when on, HEX["hd"] otherwise, and for an archived task HEX["dim"] (`b` HEX["dim"] when on); then `truncate(lw)`, `pad_right` to lw
module: taskboard/views.py
examples: (TC-4328) F-V w2, on `True`, sw `4`, lw `46` → "▶18:20  ■■□□ ▍Sync notes" + 22 spaces; spans "▶" `#2dd4bf`, "18:20  " `#e6edf3`, "■■" `#e6edf3`, "□□" `#5b6675`, "▍" `#60a5fa`, "Sync notes" `b #e6edf3`
examples: (TC-4384) F-V h2 (Done on a 3-phase board), on `False`, sw `4` → " 21:47  ■■■  ▍Compose file anatomy"; "■■■" `#e6edf3`, "▍" `#4ade80`, title `#c9d4e0`; h1 (Inbox) → "▍" `#5b6675`, "■" `#e6edf3`, "□□" `#5b6675`; over the 6 F-V rows the state cells carry only `#e6edf3` and `#5b6675`
examples: (TC-4395) F-V w5 (archived), archived shown, on `False` → " ?      ■■■■ ▍Old archived" with "Old archived" `#5b6675`; on `True` → "Old archived" `b #5b6675`
examples: (TC-4340) title "[red]x[/red]", on `True`, sw `3`, lw `46` → "▶08:00  ■□□ ▍[red]x[/red]" (the brackets are cells, no style from them)

_added_top
req: LLR-4303.15
in: list[tuple[int, str]] plan; int sel; int room
out: int top
func: the scroll window, a pure function of the cursor (the render keeps no state): si = the plan index of the entry (sel, ""); top = max(0, min(si − room + 1, len(plan) − room)) — the formula of `render_all_agenda`: the cursor's line is the last visible one once it passes the first page, and the window never runs past the plan's end
module: taskboard/views.py
examples: (TC-4335) the 40-task board, newest → plan of `68` entries; sel `39`, room `21` → top `47` (the cursor's line is visible, last); sel `0` → top `0`

_added_pane
req: LLR-4303.10, LLR-4303.12, LLR-4303.13, LLR-4304.10, LLR-4303.20, LLR-4304.17
in: AddedRow row; datetime? first; dict people; date today; int rw; int room
out: tuple(list[Text] lines, bool cut)
func: ([], False) when rw ≤ 0; else, for this ONE row: 1 `clip(_one_line(title), rw)` in `b` HEX["ink"]; 2 the chip: board part bp = `clip(_one_line(row.bname), max(1, rw // 2))`, project part = `clip(_one_line(p.name if p else "Inbox"), max(1, rw − 3 − vis(bp)))` in HEX[`project_color`], " · " in HEX["dim"], bp in `board_hex(row.bcolour)`; 3 the meta line(s) `_added_meta(row, people, today, rw)`; 4 `added_source_line(row, first)` in HEX["mut"] (HEX["dim"] for source "?"), WRAPPED, never clipped; 5 "─" × rw in HEX["frame"]; then the notes: n = (notes or "").strip("\n"); cut BEFORE any markup or wrap (A-3 / SEC-4): nroom = max(0, room − the lines built so far); cap = nroom × (rw + 1) — the most characters the pane can ever show of a note, counting one break per line; cut = len(n) > cap; n = n[:cap] (so a 5 MB note costs a slice, not a wrap); `notes_text(n, people)` when n.strip(), else Text("no notes", HEX["dim"]); wrapped with `Text.wrap(_SEARCH_CONSOLE, rw, overflow="fold")` — rich passes the console only to `Lines.justify`, which does nothing for the default justify, so no live console and no I/O are needed (a word wider than rw folds at the cell boundary; spans survive the wrap); then each url `clip("↗ " + _one_line(u), rw)` in HEX["cyan"], each image `clip("▤ " + _one_line(Path(im).name), rw)` in HEX["mut"], then, when depends_on, `clip("after: " + ", ".join(titles.get(d, d)), rw)` in HEX["mut"] with titles = {t.id: t.title for t in row.board.tasks if isinstance(t.id, str)} (SEC-3, LLR-4304.17: a list or dict id is never hashed and resolves no link; `depends_on` is already coerced to str; an unknown id shows itself); returns (lines, cut)
module: taskboard/views.py
examples: (TC-4330) F-V w2, first 2026-10-31 18:20, rw `67` → lines "Sync notes" (`b #e6edf3`), "Eval harness · Work" ("Eval harness" `#60a5fa`, " · " `#5b6675`, "Work" `#38bdf8`), the meta line, "added Sat Oct 31 · 18:20 · the created field" (`#8b98a5`), "─" × `67`, "ask the vendor", "ping @Ana Ruiz before Friday", "↗ https://example.com/spec", "▤ board.png", "after: Pilot store list"
examples: (TC-4332) the same, the note line "ask the vendor" → one span `#60a5fa`, no "::" drawn; "ping @Ana Ruiz before Friday" → "ping " `#8b98a5`, "@Ana Ruiz" `b #f472b6`, " before Friday" `#8b98a5`
examples: (TC-4333) the same → `3` lines after the notes: "↗ https://example.com/spec" (`#22d3ee`), "▤ board.png" (`#8b98a5`), "after: Pilot store list" (`#8b98a5`)
examples: (TC-4332) notes "::g:: done: the rubric draft is ready for the pilot review on friday :: then ship", rw `41` → 2 note lines "done: the rubric draft is ready for the " (all `#4ade80`) and "pilot review on friday then ship" ("pilot review on friday" `#4ade80`, " then ship" `#8b98a5`)
examples: (TC-4370) F-V w2, rw `41` → the source line wraps to "added Sat Oct 31 · 18:20 · the created" and "field"
examples: (TC-4332b) a task whose note is `5 000 000` characters ("lorem " repeated), rw `67`, room `27` → cut `True`; at most 22 × 68 note characters reach `notes_text`; one `render_added_list` paint at 118x30 under `50` ms (`planned`; security probe p2 measured 0.92 s for the uncut 5 MB wrap, SEC-4; NC no cut: RED on the time bound)
examples: (TC-4377) F-V-like board holding a task of id ["x"] titled "Odd" and the cursor's task with depends_on ["x"] → the pane's last line "after: x" (the list id resolves no title), `0` exceptions; the cursor on the ["x"] task itself → the pane paints, `0` exceptions (`planned`; NC `{t.id: t.title}` over every task: TypeError unhashable type, RED)

_added_meta
req: LLR-4303.11, LLR-4306.7
in: AddedRow row; dict people; date today; int rw
out: list[Text] lines
func: pieces in order, each one Text piece: the phase (HEX["done"] when `board.is_done`, HEX["mut"] when `board.phase_index` is 0, else HEX["sky"]); "archived" (HEX["dim"]) when the task is archived; the priority "▲ high" (HEX["rose"]) / "▽ low" (HEX["dim"]) / "· normal" (HEX["dim"]); the dates when `parse_iso(start)` or `parse_iso(due)` gives a date: f"{s:%b} {s.day}→{d:%b} {d.day}", f"due {d:%b} {d.day}" or f"from {s:%b} {s.day}", in HEX["over"] when due < today and not done, HEX["soon"] when due == today and not done, else HEX["mut"]; the milestone when `task.milestone`: glyph, style, _ = `milestone_mark(task, board, today)`, f"{glyph} {class name or 'milestone'}" in HEX[style] (class = board.marks.get(task.mark)); the people `" ".join("@" + n for n in mention_names(task, people))` in `b` HEX["pink"]; f"↗ {len(urls)}" and f"▤ {len(images)}" in HEX["mut"]. Pieces are packed greedily into lines of ≤ rw cells, two spaces between pieces on a line, a piece never split (one wider than rw is clipped): one line at 118x30 for the fixture, two at 80x24 (P-V-3)
module: taskboard/views.py
examples: (TC-4331) F-V w2, rw `67` → one line "Doing  ▲ high  Oct 30→Nov 3  ◆ milestone  @Ana Ruiz  ↗ 1  ▤ 1": `7` pieces styled `#38bdf8`, `#fb7185`, `#8b98a5`, `#8b98a5`, `b #f472b6`, `#8b98a5`, `#8b98a5`; rw `41` → "Doing  ▲ high  Oct 30→Nov 3  ◆ milestone" and "@Ana Ruiz  ↗ 1  ▤ 1" (7/7 pieces)
examples: (TC-4331) F-V w1 (bare) → one line "Backlog  · normal" (2 pieces)
examples: (TC-4397) F-V w5, archived shown → "Done  archived  · normal"

added_source_line
req: LLR-4304.10, LLR-4304.15
in: AddedRow row; datetime? first
out: str line
func: "c" → f"added {at:%a %b %d · %H:%M} · the created field"; "h" → f"added ≈ {at:%a %b %d · %H:%M} · from history.jsonl"; "?" → f"added: unknown, before {first:%b} {first.day} · #{pos + 1} in {_one_line(bname)}'s board file" when first is set, else f"added: unknown · #{pos + 1} in {_one_line(bname)}'s board file"
module: taskboard/views.py
examples: (TC-4370) F-V w2 → line "added Sat Oct 31 · 18:20 · the created field"; w3 → "added ≈ Wed Oct 28 · 10:30 · from history.jsonl"; h1, first 2026-10-31 18:20 → "added: unknown, before Oct 31 · #1 in Home's board file"
examples: (TC-4375) F-V h1, first `None` → "added: unknown · #1 in Home's board file"; board "Solo" second task, first `None` → "added: unknown · #2 in Solo's board file"

_one_line
req: LLR-4303.8, LLR-4303.20
in: object s
out: str line
func: str(s) with every "\r", "\n" and "\t" replaced by one space: a title or name read from a hand-edited file keeps tab and newline through `strip_controls`, and one of them inside a body line would split it and shift the whole layout (P-V-9); used on every single-line piece (titles, project, board, mark and person names, urls, image names)
module: taskboard/views.py
examples: (TC-4328) s "a\nb\tc" → line "a b c"

added_rows
req: LLR-4304.1, LLR-4304.2, LLR-4304.3, LLR-4304.8, LLR-4304.12, LLR-4304.13, LLR-4304.17
in: list[tuple[str, str, Board?, str]] lanes
out: list[AddedRow] rows
func: fixed by graph-interfaces.cw.md (not restated). Implementation notes: births = {} then `births.setdefault(rec["task"], rec["at"])` for each record with `rec.get("from") is None` and `isinstance(rec.get("task"), str)` (history.read already guarantees `task`/`at` are str; the check keeps the key a str by this function's own contract, SEC-3); the read is wrapped `except (OSError, ValueError, RecursionError)` → no births (ValueError covers UnicodeDecodeError from a non-UTF-8 byte, P-V-1; RecursionError a deeply nested line, which `history.read` does not catch, SEC-2; both in the interface func); per task, the birth lookup runs only when `isinstance(task.id, str)` — a list or dict id is unhashable and could never match a str key, so it gets source "?" (or "c") with no dict lookup at all (SEC-3, LLR-4304.17); a birth `at` goes through `added_moment` like `created`, so an offset-aware `at` is not a birth (LLR-4304.13, ARCH-3); `task.created` read as the attribute group D adds
module: taskboard/views.py
examples: (TC-4361) F-V → w2 source "c" at 2026-10-31 18:20, h2 "c" at 2026-10-31 21:47, w4 "c" at 2026-11-01 08:10
examples: (TC-4362) F-V w3 (births 10-28 10:30 then 10-29 11:00) → source "h", at 2026-10-28 10:30
examples: (TC-4363) F-V w1, w5, h1 → source "?", at `None`
examples: (TC-4368) created "not a date" and a birth at "2026-10-28T10:30:00" → source "h"; created "not a date", no birth → source "?"; `0` exceptions
examples: (TC-4372) F-V with history.read monkeypatched to raise PermissionError → `7` rows, w3 source "?" (its births unread), w2/h2/w4 still "c", no exception
examples: (TC-4372b) a board folder whose history.jsonl holds the byte 0xff (here `\xff\xfe`) → rows built, the unstamped task source "?", a stamped one still "c", no exception (probe: base history.read raises UnicodeDecodeError, not OSError)
examples: (TC-4372c) a board folder whose history.jsonl holds one line of `10 000` nested `[` → rows built, the unstamped task source "?", a stamped one still "c", `0` exceptions (`planned`; security probe p3: base history.read raises RecursionError on such a line, 03-pdr-security.md SEC-2; NC guard without RecursionError: RED)
examples: (TC-4373) created "2026-10-31T18:20:00+00:00", no birth → source "?"; the same created with a birth at "2026-10-28T10:30:00" → source "h", at 2026-10-28 10:30; no created and the only birth `at` "2026-10-28T10:30:00+00:00" → source "?" (an aware `at` is not a birth); `0` exceptions (`planned`; NC convert or strip the offset: arm 1 gives source "c", RED)
examples: (TC-4377) a peeked board holding tasks of id ["x"] and {"a": 1} (no created) and a birth record for "x" → `2` rows, both source "?", at `None`, `0` exceptions (`planned`; security probe p2: an unguarded `births.get(task.id)` raises TypeError unhashable type, NC RED)

added_moment
req: LLR-4304.8, LLR-4304.13
in: object value
out: datetime? moment
func: fixed by graph-interfaces.cw.md (not restated). Implementation note: `if not isinstance(value, str): return None`; the parse alone sits in one `try: m = datetime.fromisoformat(value) except ValueError: return None`; then `return m if m.tzinfo is None else None` — an offset-aware value is not valid (ARCH-3 ruling: no conversion, no `astimezone()`; the app writes only naive local stamps, `stamp` and history.py:33). No time-zone arithmetic means no machine-dependent result and nothing that can raise after the parse
module: taskboard/views.py
examples: (TC-4373) value "2026-10-31T18:20:00+00:00" → moment `None` (the same on every machine's zone; `planned`; NC convert with `astimezone()`: a datetime, RED)
examples: (TC-4373b) value "2026-10-31T18:20:00Z" → moment `None`; value "1960-01-01T00:00:00+00:00" → moment `None` with `0` exceptions (`planned`)
examples: (TC-4368) value "2026-10-31" → moment 2026-10-31 00:00 (a date-only string is a valid created)

added_order
req: LLR-4304.4, LLR-4304.5, LLR-4306.1
in: list[AddedRow] rows; bool newest; bool show_archived
out: list[AddedRow] ordered
func: fixed by graph-interfaces.cw.md (not restated). Implementation note: two `sorted` calls with the interface keys, unknown + dated, `[::-1]` for newest; stable and total because (lane, pos) is unique per row. The explicit (lane, pos) keys stay even though `added_rows` emits lane-major order: they make the order independent of that contract, and the tests below feed a hand-shuffled input so that dropping them is caught (ARCH-1). The shuffled-input arms of TC-4364/TC-4365 below were run on a pure reference sort with the interface keys (scratch `%TEMP%/incL-e3/probe.py`, state `executed`, not on views.py): the correct orders are as listed; the moment-only mutant (unknowns in input order) and the unknowns-last mutant give the RED orders named in each example
module: taskboard/views.py
examples: (TC-4391) F-V, newest `True`, show_archived `False` → ids "w4", "h2", "w2", "w3", "h1", "w1" (`6` rows, w5 absent); show_archived `True` → "w4", "h2", "w2", "w3", "h1", "w5", "w1" (`7` rows)
examples: (TC-4365) F-V rows given in REVERSE (lane, pos) order (h2, h1, w5, w4, w3, w2, w1; ARCH-1 hand-shuffled input), newest `False`, show_archived `False` → "w1", "h1", "w3", "w2", "h2", "w4": the 2 unknown rows are rows 0–1 in (lane, pos) order (NC unknowns kept in input order: "h1", "w1", … RED; NC unknowns last: "w3", "w2", "h2", "w4", "w1", "h1", RED)
examples: (TC-4364) a Work row (lane 0, pos 3) and a Home row (lane 1, pos 0), both at 2026-10-31 10:00, given Home first, newest `False` → the Work row first; with the registry order swapped (Home lane 0, Work lane 1), given Work first → the Home row first (NC sort by moment alone: input order kept in both arms, RED)
examples: (TC-4364) the same reversed F-V input (h2 … w1), newest `False`, show_archived `True` → "w1", "w5", "h1", "w3", "w2", "h2", "w4" (unknown by lane then file position: w1 pos 0, w5 pos 4, then lane 1; NC moment-only with unknowns unsorted: "h1", "w5", "w1", … RED)

first_created
req: LLR-4304.11, LLR-4304.15
in: list[AddedRow] rows
out: datetime? first
func: fixed by graph-interfaces.cw.md (not restated). Its input is every task the list read, archived included (S passes the unfiltered rows), which is exactly the subject of LLR-4304.11 / LLR-4304.15 as reworded by ARCH-8 ("no task the list read (archived included) has a valid created"), not "no listed task"
module: taskboard/views.py
examples: (TC-4371) F-V all 7 rows → first 2026-10-31 18:20; the "Solo" board's 2 rows → first `None`
examples: (TC-4371) a board whose only stamped task is archived (created "2026-10-30T09:00:00") and 2 unknown live tasks, archived hidden → first 2026-10-30 09:00, so the unknown rows' header reads "BEFORE OCT 30 · ?", not "BEFORE ANY RECORD · ?" (`planned`; ARCH-8)

state_boxes
req: LLR-4305.1, LLR-4305.2
in: list[str] phases; str phase
out: str boxes
func: fixed by graph-interfaces.cw.md (not restated); phases is never empty (Board.__init__ falls back to DEFAULT_PHASES), so n ≥ 1
module: taskboard/views.py
examples: (TC-4381) phases ["Backlog","Doing","Review","Done"]: phase "Backlog" → boxes "■□□□"; "Doing" → "■■□□"; "Review" → "■■■□"; "Done" → "■■■■"
examples: (TC-4382) phases "P0".."P9": index 0 → boxes "■□□□□□□□"; index 4 → "■■■■□□□□"; index 9 → "■■■■■■■■"

## Entities

[Data: AddedRow]
in: NamedTuple(Task task, int lane, str bname, str bcolour, Board board, str source, datetime? at, int pos)
desc: cited from graph-interfaces.cw.md, unchanged; the render reads task, bname, bcolour, board (phases, projects, tasks, marks), source, at, pos

[Data: views.HEX]
in: dict[str, str]
desc: UNCHANGED palette; keys used by the list view: accent, mut, dim, ink, hd, frame, sky, done, rose, over, soon, pink, cyan, and every PROJECT_COLORS key through project_color / board_hex; no new key

[Data: views.ADDED_LEGEND]
in: str
desc: NEW constant "  ·  time = created  ≈ = history  ? = unknown" (45 cells)

[Data: views._SEARCH_CONSOLE]
in: rich.console.Console
desc: UNCHANGED (views.py:4135, force_terminal, width 9999); reused as the console argument of Text.wrap, which only hands it to Lines.justify (a no-op for the default justify): no output is written

[Data: Board.marks]
in: dict
desc: the marks directory by id, set by the app on every lane board (board_lanes); read through milestone_mark and for the class name

[I/O: history.jsonl]
desc: read only, once per board, by added_rows (history.read); never written by this group

[Data: Task.created]
in: str?
desc: group D's field (graph-interfaces.cw.md); read by added_rows through added_moment; never written here

## Edges

[Data: Task.created] ──▶ added_rows
[I/O: history.jsonl] ──▶ added_rows
[Data: AddedRow] ──▶ added_order
[Data: AddedRow] ──▶ first_created
[Data: AddedRow] ──▶ render_added_list
[Data: AddedRow].at ──▶ _added_plan
[Data: AddedRow].source ──▶ added_time_label
[Data: AddedRow].source ──▶ added_source_line
[Data: AddedRow].board ──▶ _added_row
[Data: AddedRow].board ──▶ _added_meta
[Data: Board.marks] ──▶ _added_meta
[Data: views.HEX] ──▶ _added_head
[Data: views.HEX] ──▶ _added_row
[Data: views.HEX] ──▶ _added_pane
[Data: views.HEX] ──▶ _added_meta
[Data: views.ADDED_LEGEND] ──▶ _added_head
[Data: views._SEARCH_CONSOLE] ──▶ _added_pane
added_moment.moment ──▶ added_rows
_added_plan.plan ──▶ _added_top.plan
_added_day_label.label ──▶ _added_plan
added_time_label.label ──▶ _added_row
state_boxes.boxes ──▶ _added_row
_added_meta.lines ──▶ _added_pane
added_source_line.line ──▶ _added_pane
_added_head.head ──▶ render_added_list
_added_row.line ──▶ render_added_list
_added_top.top ──▶ render_added_list
_added_pane.lines ──▶ render_added_list

## Findings

finding P-V-1 MAJOR: history.read raises UnicodeDecodeError, which LLR-4304.12's OSError guard misses
anchor: added_rows
seen: (TC-4372b) probe on the worktree: a history.jsonl holding `\xff\xfe` → `history.read` raises UnicodeDecodeError (isinstance OSError `False`, ValueError `True`); with only `except OSError`, one stray byte in any registry board's history makes `N` crash at compose
cause: history.read opens the file in text mode (utf-8) and iterates it unguarded; LLR-4304.12 and the interface name only OSError
effect: the list view cannot open while any board's history is not valid UTF-8 (hand edit, partial copy, another tool)
decision: ruling (03-pdr-rulings round 0): "Accept. added_rows guards history.read with except (OSError, ValueError) (a non-UTF-8 byte raises UnicodeDecodeError). LLR-4304.12 widened; TC-4372b." Applied: added_rows func and TC-4372b; graph-interfaces added_rows (orchestrator)

finding P-V-2 MAJOR: added_moment's astimezone() raises on Windows for aware moments before 1970 and at the year bounds
anchor: added_moment
seen: (TC-4373b) probe (Python 3.12.7, Windows): "1960-01-01T00:00:00+00:00" → `astimezone()` OSError [Errno 22]; "0001-01-01T00:00:00+05:00" and "9999-12-31T23:59:59-05:00" → OverflowError; the interface func says "Never raises" but its formula has no guard
cause: Windows localtime rejects negative timestamps; the conversion leaves the datetime range at the bounds
effect: one hand-edited `created` (or a history `at` with an offset) crashes the view on open
decision: ruling (03-pdr-rulings round 0): "Accept. added_moment returns None when astimezone() raises (OSError before 1970 on Windows, OverflowError/ValueError at the bounds). New LLR-4304.16; TC-4373b." Applied at round 0 to added_moment and the interface. SUPERSEDED by ARCH-3 (round 1, below): the conversion is removed, so nothing is left to guard — LLR-4304.16 is withdrawn, its 1900/0001 examples and the `except (OverflowError, OSError)` are gone from added_moment, and TC-4373b now pins "…Z" → None

finding P-V-3 minor: seven meta pieces and the source line do not fit one line of the 41-cell pane at 80x24
anchor: _added_meta
seen: (TC-4331, TC-4370) at rw `41` the fixture's 7 pieces need 61 cells and "added Sat Oct 31 · 18:20 · the created field" 44; HLR-4303 asks every LLR-4303.n threshold at 80x24 too, while LLR-4303.10/.11 say "the meta line"
cause: the LLRs were sized on the 118x30 capture
effect: a single clipped line would fail 7/7 pieces (LLR-4303.11) and the exact source string (LLR-4304.10) at 80x24
decision: ruling (03-pdr-rulings round 0): "Accept V's proposal (meta pieces and source line wrap inside the pane at 80x24 instead of clipping)." Applied: _added_meta func and TC-4331, _added_pane func (source line wrapped) and TC-4370, the 80x24 body above

finding P-V-4 minor: the "first created date" definition uses `%b %-d`, which Windows strftime rejects
anchor: _added_plan
seen: 01-requirements.md §1 Definitions: "as `%b %-d` (e.g. `Oct 31`)"; views.agenda_buckets' docstring already says "never `%-d`"
cause: a POSIX-only strftime flag in the definition
effect: a literal implementation raises ValueError on this machine
decision: ruling (03-pdr-rulings round 0): "Accept: no %-d; the day number is formatted as str(d.day)." Applied: _added_plan (BEFORE <first created date> as f"{first:%b} {first.day}"), added_source_line (before <first created date>); the day headers and the source line's date keep `%a %b %d` (zero-padded `%d`, portable), as LLR-4303.9 and LLR-4304.10 write them

finding P-V-5 minor: reading of "a day known only from history"; the round's ListB split mixed days
anchor: _added_plan
seen: (TC-4329) the proto's ListB keys each h row's header as "<DATE> ≈" and never uses TODAY/YESTERDAY for h rows, so a day holding c and h rows alternates headers in time order (c 10:00, h 11:00, c 12:00 → 3 headers)
cause: the proto computed the header per row, not per day
effect: duplicate day headers; LLR-4303.9's literal text asks one header per added day
decision: ruling (03-pdr-rulings round 0): "Accept: one header per day; ≈ only when every row of that day has source h." Applied: _added_plan func and TC-4329

finding P-V-6 minor: LLR-4306.6 "end with" and LLR-4304.14 "clipped to the width" collide at 80 cells
anchor: _added_head
seen: (TC-4396) the proto head alone is 88 cells; clipping the row at 78 would cut the archived piece LLR-4306.6 requires at its end
cause: the two LLRs were written separately
effect: at 80x24 the archived or not-read count would vanish
decision: ruling (03-pdr-rulings round 0): "Accept V's degrade order for the head row (drop every board, then the legend; the order word and counts stay)." Applied: _added_head func, TC-4326 and TC-4396

finding P-V-7 minor: a note longer than the pane is cut; the pane does not scroll
anchor: render_added_list
seen: (TC-4335) a 40-line note at 80x24 → 21 pane lines; no LLR says what happens past the pane
cause: the pane has no key of its own (keys move the list cursor)
effect: silent truncation would hide note lines, urls and `after:`
decision: ruling (03-pdr-rulings round 0): "Accept: a full pane ends with … k more lines in HEX[dim]." Applied: render_added_list func and TC-4335 (40-line note)

finding P-V-8 minor: the scroll window is stateless, as the agenda's
anchor: _added_top
seen: render_added_list has no `top` input (interface), so the window is derived from sel each paint: past the first page the cursor's line is the last visible one, also while moving up
cause: the render is pure by the interface; render_all_agenda uses the same formula (`start = row − room + 1`)
effect: moving up from the bottom scrolls the list every step instead of moving the cursor inside a fixed page
decision: ruling (03-pdr-rulings round 0): "Accept: the scroll window is stateless (computed from sel each paint), as the agenda's." Applied: _added_top func and TC-4335

finding P-V-9 minor: titles and names may hold tab or newline, which would split a body line
anchor: _one_line
seen: models.strip_controls keeps tab and newline; Task.from_dict keeps any str title; `fit`/`clip` do not flatten; render_all_agenda has the same exposure (pre-existing)
cause: single-line pieces built from free text
effect: one hand-edited title with "\n" shifts every following body line and the `│` column
decision: ruling (03-pdr-rulings round 0): "Accept: tab and newline in a title/project/board name are drawn as one space." Applied: _one_line and its callers (_added_row, _added_pane, added_source_line), TC-4328

finding P-V-10 minor: render_added_list's req list in graph-interfaces omits LLR-4303.15, LLR-4303.17 and LLR-4305.3, which its internals serve
anchor: render_added_list
seen: graph-interfaces.cw.md render_added_list `req:` lists HLR-4303, LLR-4303.7, .8, .9, .10, LLR-4304.14, LLR-4306.6, while its own TC-4337 example is LLR-4303.17
cause: the interface was cut before the internals were designed
effect: a trace from LLR-4303.15/.17 or LLR-4305.3 to the code would miss its node
decision: ruling (03-pdr-rulings round 0): "Accept: render_added_list req list gains the 3 LLRs V named." Applied: graph-interfaces render_added_list req (orchestrator; checked: LLR-4303.15, LLR-4303.17, LLR-4305.3 present); this file's node unchanged

finding ARCH-1 HIGH: the tie-break negative controls of LLR-4304.4 / LLR-4304.5 could not fire
anchor: added_order
seen: (03-pdr-architect.md ARCH-1) `added_rows` emits lane-major order and `sorted` is stable, so a mutant that sorts dated rows by moment alone and leaves unknowns unsorted gives the correct order for every input built through the F-V lanes; only a permuted input turns it RED
decision: ruling (03-pdr-rulings round 1): "Accept. TC-4364/TC-4365 feed added_order a hand-shuffled input (not lane/pos order), so a mutant that drops the tie-break or puts unknowns last turns RED. LLR-4304.4/.5 NC text rewritten." Applied: added_order func (keys kept, why) and its TC-4364 (both tie arms given in reverse lane order; the F-V archived arm on the reversed input) and TC-4365 (reversed F-V input) examples, each with its RED mutant order; run on a reference sort (`executed`); TC-4391 stays on the lane-major input (it pins the archived filter, not the order)

finding ARCH-3 MEDIUM: remove the offset-aware conversion instead of guarding it
anchor: added_moment
seen: (03-pdr-architect.md ARCH-3) the app never writes an aware value; `astimezone()` brought a Windows-only failure (P-V-2, LLR-4304.16) and TC-4373's oracle depended on the runner's zone (identity on a UTC runner, so "drop tzinfo" passed there)
decision: ruling (03-pdr-rulings round 1): "Accept — remove, not guard. An offset-aware created or at is not valid (added_moment → None); no conversion. LLR-4304.13 rewritten; LLR-4304.16 withdrawn (P-V-2's guard has nothing left to guard)." Applied: added_moment req (LLR-4304.16 removed), func (one `except ValueError`, aware → None) and TC-4373 / TC-4373b (as in the interfaces: "+00:00" and "Z" → None); added_rows req (+LLR-4304.13) and TC-4373 arms (no birth → "?", birth → "h", an aware birth `at` is no birth); P-V-2's decision marked superseded

finding ARCH-8 MINOR: LLR-4304.11/.15 said "no listed task" while first_created reads all rows
anchor: first_created
seen: (03-pdr-architect.md ARCH-8) the only stamped task archived and hidden: the literal LLR text asked for "BEFORE ANY RECORD", the design shows "BEFORE OCT 30"
decision: ruling (03-pdr-rulings round 1): "Accept: LLR-4304.11/.15 say 'no task the list read (archived included)'." Applied: first_created func (its input named as the LLRs' subject) and a TC-4371 arm (archived-only stamp → "BEFORE OCT 30 · ?"); the design is unchanged

finding SEC-2 MEDIUM: one deeply nested line in any board's history.jsonl crashed `N`
anchor: added_rows
seen: (03-pdr-security.md SEC-2, probe p3) a 200 000-`[` line makes `history.read` raise RecursionError, neither OSError nor ValueError; the list reads every registry board's history
decision: ruling (03-pdr-rulings round 1): "Accept. added_rows guards history.read with (OSError, ValueError, RecursionError); TC-4372c (one deeply nested line). Backlog L-BL-2: fix history.read at the source (Flow view crashes today)." Applied: added_rows func (the widened guard) and TC-4372c (10 000 nested `[`, as LLR-4304.12's threshold); L-BL-2 is the orchestrator's BACKLOG entry

finding SEC-3 MEDIUM: a non-string task id on another board crashed `N` and the pane
anchor: added_rows
seen: (03-pdr-security.md SEC-3, probe p2) `Task.from_dict` keeps any JSON id; `births.get(task.id)` and `{t.id: t.title}` raise TypeError unhashable type for a list or dict id
decision: ruling (03-pdr-rulings round 1): "Accept. Birth lookups and the after: title lookup use only str ids; a non-str id gets no birth record and resolves no link. New LLR-4304.17, TC-4377." Applied: added_rows req (+LLR-4304.17), func (lookup only for a str id; births keyed by str `task` only) and TC-4377; _added_pane req (+LLR-4304.17), func (`titles` from str ids only) and TC-4377 (pane arms)

finding SEC-4 LOW: a huge note re-wrapped on every paint
anchor: _added_pane
seen: (03-pdr-security.md SEC-4, probe p2) `notes_text` + wrap cost 0.17 s for a 1 MB note and 0.92 s for 5 MB, on every key while the cursor is on it
decision: ruling (03-pdr-rulings round 1): "Accept: the pane wraps at most room × (rw + 1) characters of the cursor's note; when cut, the tail reads … more lines (no count)." (addendum A-3) Applied: _added_pane in (`room`), out (`cut`), func (the cut before notes_text); render_added_list func (the `… more lines` tail when cut; P-V-7's count otherwise), TC-4335 (count kept: under the cap), TC-4335b and TC-4332b; the performance note

### Seams (the linter reads only Nodes/Entities/Edges/Findings, so this list is a note, as in incC's graph-proto-V)

> Calls V makes into another group:
> - group D: reads `Task.created` (the field, LLR-4301.1) in added_rows; `Board.phases`, `Board.project_by_id`, `Board.is_done`, `Board.phase_index` (unchanged models API); `parse_iso` (models).
> - history.read (unchanged module; not a group's node).
> Calls other groups make into V (all from group S's `AddedList`, app.py):
> - compose: `rows = added_rows(lanes)` once; `first = first_created(rows)` over the UNFILTERED rows (archived included); `hidden` = count of rows with `task.archived` left out (graph-proto-S passes 0 while archived are shown; the head ignores `hidden` then); `unread` = count of lanes whose board is None.
> - each paint: `listed = added_order(rows, newest, show_archived)`; `render_added_list(listed, sel, newest, show_archived, hidden, unread, first, today, app.people.people, w − 2, h − 1)`; `sel` indexes `listed` (S clamps it and keeps the cursor's task across `v`, LLR-4306.4); the key row is S's (`key_line(ADDED_KEYS + [read-only tail])`, else `key_line(ADDED_KEYS, w − 2)`: addendum A-2).
> - `enter`: S reads `listed[sel].lane` and `.task.id` for `open_on_board(app, ids[lane], task.id)`.
> - layer-0 tests may call `added_time_label`, `added_source_line`, `state_boxes`, `added_moment` directly.

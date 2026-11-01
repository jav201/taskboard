# Code-Wire prototype — group V (taskboard/app.py, taskboard/keymap.py, README `n` row) — Inc K

Differences from `graph-baseline.cw.md` (545c18a) only. Group V owns the capture view on `n`: `PadArea` (an `InkArea` subclass: Inc C's live colour, the divider rule, the ghost), `CaptureView` (head, pad, hint row, rail, name field, key row; debounce, toasts, the pad keys `alt+d/o/n/a/i/u/l`, `esc`), `ReviewList` (variant C's batch review on `alt+a`), the pure painters (`hit_text`, `capture_head`, `capture_hint`, `rail_rows`, `review_rows`), `TaskboardApp.action_capture`, the changed `TaskboardApp.__init__` and `TaskboardApp.check_action`, and the `n` entry of `keymap.KEYMAP` (+ README row). New: 37 nodes. Changed: 3 nodes (`TaskboardApp.__init__`, `TaskboardApp.check_action`, `app_bindings`). G-V calls G-S (`taskboard/inbox.py`) and G-T (`taskboard/suggest.py`) only through the public names of `graph-interfaces.cw.md`; every notice text below is G-V's unless it says "G-S's text, shown verbatim".

E2 correction pass (round 0b, `03-pdr-rulings.md`): every finding below carries its ruling; P-V-1 (`tab` board cycle), P-V-2, P-V-6, P-V-7, P-V-8, P-V-10, P-V-12, P-V-13, P-S-4, P-S-8, P-S-15 and P-T-4 are applied in the nodes. E2c cross-check: the fixture is now G-T's executed fixture F and every hit score and why list below equals an executed example of graph-proto-T (G-T wins; the earlier scratch values of `ref_rail.py` over G-V's own boards are withdrawn).

### Fixture F (synthetic; G-T's executed fixture F; every example below uses it unless it says otherwise)

> Clock now 2026-11-01T10:02:00 (graph-interfaces). Store folder `S` = the registry's folder; store `S/inbox.json`; pad images `S/inbox-images/`.
> Registry lanes (board order) = graph-proto-T §Fixture F: lane 0 `Client A`, colour `sky`, file `S/boards/client-a/board.json`, THE OPEN BOARD, phases ["Backlog", "Doing", "Done"], projects `Eval harness` (id `pe`, colour `blue`) and `Pilot rollout` (id `pr`, colour `indigo`) with F's eight tasks; lane 1 `Course`, colour `violet`, file `S/boards/course/board.json`, phases ["Todo", "Doing", "Done"], project `Module 4 · Volumes` (id `pv`, colour `violet`) with F's three tasks; marks M (`payment`, `release`). The phases are the ones G-S's fixture S uses (graph-interfaces E2c note).
> Notes: N1 = "Golden set: 12 questions still have no answer key\nask @username_subject which stores count"; N2 = "Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png"; N3 = "Quote for the new client: contracts Q&A\ntwo weeks, fixed price"; N4 = "Steering deck: demo the hybrid search on pilot stores"; N5 = "Answer the region chair".
> Hits — G-T's executed values (graph-proto-T suggest examples TC-4475, TC-4479, AT-4402, AT-4407; scored text = `note_task` title + "\n" + notes, P-T-4): N1 → [Eval harness 0.341 ▰▰▰ why questions, @username_subject, key; Pilot rollout 0.2869 ▰▰▱ why stores, @username_subject] → options [Eval harness, Pilot rollout]; N2 → [Module 4 · Volumes 0.668 ▰▰▰ why volume, oracle, script] → options [Module 4 · Volumes]; N3 → [] → options [None]; N4 → [Pilot rollout 0.6444 ▰▰▰ why pilot, stores, steering, demo, hybrid, search] → options [Pilot rollout]; N5 → [Pilot rollout 0.1488 ▰▱▱ why chair, region] → options [None, Pilot rollout]. E2c checked: equal to G-T's executed examples.
> Hues: project `HEX["blue"]` #60a5fa, `HEX["indigo"]` #818cf8, `HEX["violet"]` #a78bfa; board `board_hex("sky")` #38bdf8, `board_hex("violet")` #a78bfa; `HEX["accent"]` #2dd4bf, `HEX["amber"]` #fbbf24, `HEX["dim"]` #5b6675, `HEX["mut"]` #8b98a5, `HEX["ink"]` #e6edf3, `HEX["hd"]` #c9d4e0, `HEX["done"]` #3f9c6d; `keymap.KEY_STYLE` = "b #e6edf7".

### Probes (read-only, scripts under `%TEMP%\incK-probe-V\`, never in the repo; each prints `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`)

> - **P-V-1 (probe_v.py p1_divider):** a `PadArea(InkArea)` whose `get_line(i)` returns `"─" * max(w, len(raw))` (w = `scrollable_content_region.width`) for a divider line not under the cursor, mounted in a Textual pilot with the layout CSS below. 118x30: pad region (0, 1, 68, 27), content (2, 2, 64, 25), w 64; text "a\n____\nb", cursor (2, 1) → screen row 3 cells x 2..65 = 64 × `─`, no `_`; `_highlights` holds no row; cursor (1, 0) → the row reads `____`, no `─`; cursor back (2, 1) → 64 × `─` again (the line cache keys on the selection under `soft_wrap=True`). 80x24: pad (0, 1, 80, 14), w 76 → 76 × `─`. A rule of w − 1 leaves the last content cell blank (`w-1 mode`), so the rule is w long. Textual's own render adds one cursor cell (`set_length(len + 1)`) that the compositor crops (screen row exact).
> - **P-V-1b (probe_v2.py):** the rule's colour must be a SPAN (`t.stylize(HEX["dim"])`): a `Text(..., style=HEX["dim"])` base style is lost (render_line segment colour `#e0e0e0`); with the span → `#5b6675`. A 150-`_` divider wraps to 3 visual rows drawn 63 + 63 + 24 × `─` (Textual divides the returned Text at the raw line's wrap offsets).
> - **P-V-2 (p2_ghost):** `placeholder` = the 4 ghost lines joined by "\n"; empty pad → pad rows 1..4 read `first line → the task's title`, `next lines → its notes`, 24 × `─`, `____ ↵ starts the next note`, colour {#5b6675} from `PadArea > .text-area--placeholder { color: #5b6675; }`; after `x` → none (rows "x", "", "", "") at 118x30 and 80x24.
> - **P-V-3 (p3_alt + probe_v2 parser):** the XTermParser turns ESC d → Key("alt+d", "d"), ESC l → Key("alt+l", "l") — a PRINTABLE character — and ESC b → Key("ctrl+left", None), ESC CR → Key("enter", "\r"). With NON-priority screen bindings, the terminal-form alt+d / alt+l / alt+b reach the focused TextArea and type "dlb" (pad "abc" → "abcdlb"), and type "d" into a focused Input; the pilot form Key("alt+d", None) does reach the binding (so pilot tests alone cannot see this). With `priority=True` the terminal form fires the binding and inserts nothing, in the pad and in the Input. TextArea's own bindings hold no `alt+` letter (only alt+backspace, alt+delete).
> - **P-V-4 (p4_unmount):** `Screen.on_unmount` runs on `app.exit()` with the screen on the stack and on `pop_screen()`, but its children are already gone: `query_one(PadArea)` raises NoMatches. So the unmount write reads `CaptureView._text`, never the widget.
> - **P-V-5 (p5_layout):** the CSS below → 118x30: head (0, 0, 118, 1), pad (0, 1, 68, 27), hint (0, 28, 68, 1), rail-box (68, 1, 50, 28), keys (0, 29, 118, 1); rail content width 48; name field open → rail (68, 1, 50, 25), field (68, 26, 50, 3). 80x24 (`-narrow`): pad (0, 1, 80, 14), hint (0, 15, 80, 1), rail-box (0, 16, 80, 7), keys (0, 23, 80, 1); rail content width 78; field open → rail (0, 16, 80, 4), field (0, 20, 80, 3).
> - **P-V-6 (p6_keys):** `key_line(CAPTURE_KEYS, 116)` = `alt+d dump   alt+o other   alt+n new project   alt+a review   alt+i image   alt+u undo   esc close` (98 cells); `key_line(CAPTURE_KEYS, 78)` = `alt+d dump   alt+o other   alt+n new project   alt+a   alt+i   alt+u   esc` (74); review keys at 108 and 72 = `↑↓ move   ␣ include   o other   d dump 3 checked   u undo   esc back` (68).
> - **P-V-7 (p7_changed):** `pad.text = …` and `pad.insert(…)` each post one `TextArea.Changed`; `insert("\n____\n", (0, 3))` on "abc" leaves the cursor (2, 0).
> - **P-V-8 (p8_real_app):** real `TaskboardApp`, 2 boards: `app.BINDINGS` holds no `n`; with AddedList pushed, `app.query("#board")` still finds the board view (1), so `refresh_view` reaches it from a pushed screen.
> - **P-V-9 (probe_v3.py):** the ReviewList box CSS below → 118x30 box (3, 9, 112, 12), body content width 108; 80x24 box (2, 6, 76, 12), content width 72; `self.styles.background = Color(13, 17, 23, 0.6)` in on_mount is kept (the app's `Screen { background }` rule outranks DEFAULT_CSS, as the prototype's `see_through`).

### Layout CSS (CaptureView.DEFAULT_CSS, probed in P-V-5)

> `CaptureView { background: #0d1117; }` · `#cap-head { height: 1; padding: 0 1; }` · `#cap-main { height: 1fr; }` · `#cap-left { width: 1fr; }` · `#cap-hint { height: 1; padding: 0 1; }` · `#cap-rail-box { width: 50; }` · `#cap-rail { height: 1fr; padding: 0 1; }` · `#cap-new { display: none; }` · `#cap-new.on { display: block; }` · `#cap-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }` · `CaptureView.-narrow #cap-main { layout: vertical; }` · `CaptureView.-narrow #cap-rail-box { width: 1fr; height: 7; }`. PadArea.DEFAULT_CSS: `PadArea { height: 1fr; border: tall #2dd4bf 40%; background: #0b0f17; }` · `PadArea > .text-area--placeholder { color: #5b6675; }`. ReviewList.DEFAULT_CSS: `ReviewList { align: center middle; }` · `#rv-box { width: 96%; max-width: 112; height: auto; max-height: 90%; background: #0b0f17; border: round #2dd4bf; border-title-color: #2dd4bf; padding: 0 1; }` · `#rv-body { height: auto; }`.

### Markup rule (tests/test_markup_census.py, LLR-4409.4)

> Every `Static.update` / `Static(…)` takes a rich `Text` returned by a censused `-> Text` function whose every `return` is a plain-`=` name bound to `Text(...)` (never `Text("\n").join(...)`: the census does not trust `.join`), or `key_line(...)`; `border_title` is a `Text(...)` or a literal; every `notify` passes `markup=False`; no `Text.from_markup`. Rows are joined by appending `"\n"` and `append_text` onto one `out = Text()`.

## Nodes

app_bindings
req: LLR-4401.1, LLR-4401.13, LLR-4401.15
in:
out: list[Binding] bindings
func: changed from baseline: generated as before; `keymap.KEYMAP` gains ONE entry `Key("n", "n", "capture", "Capture", group="misc", bar=False)` placed directly after the `N` entry (comment: "`n` — the capture view (Inc K, LLR-4401.1): global, off the bar, like `N`"), not priority, no `views`; so `TaskboardApp.BINDINGS` holds `Binding("n", "capture", "Capture", priority=False)`. README.md main key table gains, right after the `N` row, the row `| \`n\` | Capture | A full-screen notes pad: type, and separate notes with a \`____\` line (\`alt+l\` inserts one); beside each note, the project of any board that matches it best, with the words that matched. \`alt+d\` turns the cursor's note into a task there, \`alt+o\` picks the next suggestion, \`alt+n\` a new project, \`alt+a\` reviews every note, \`alt+i\` attaches the clipboard image, \`alt+u\` undoes the last dump (kept 7 days), \`esc\` closes. The pad lives in \`~/.taskboard/inbox.json\` |`
module: taskboard/keymap.py
oracle: README.md, main key table, row `n` (after `N`)
examples: (TC-4401) KEYMAP → exactly `1` entry with keys "n", action "capture", label "Capture", bar `False`, views `None`, priority `False`; its index = index of "N" + `1`; tests/test_keymap.py key-law tests GREEN (5/5)
examples: (TC-4413) README.md → test_the_readme_keybinding_table_matches_the_seat GREEN, and a line starting "| `n` | Capture |" exists in the main table (the second assertion is needed: see finding P-V-4)
examples: (TC-4415) BoardsHome on top, `n` → BoardForm (new board) pushed, no CaptureView; PeopleDirectory on top, `n` → PersonForm; MarksManager on top, `n` → MarkForm (3/3: their screen bindings run before the app's non-priority `n`)

TaskboardApp.__init__
req: LLR-4407.1
in: Path? board_path = None; float team_sync_interval = 1800.0; Registry? registry = None
out: None
func: changed from baseline: after the marks directory, `self.inbox = Inbox.load(self.registry.path.parent / INBOX_NAME)` (one store for every board, beside the registry, as people.json); and two session flags `self._inbox_said = False` (the load notice of LLR-4407.8 shown once per app) and `self._divider_said = False` (the divider notice shown once per session even when the flag write fails). Imports added to app.py: `from .inbox import (INBOX_NAME, DumpTarget, Inbox, attach_images, dump_note, entry_for, is_divider, note_at, note_count, note_parts, note_task, prune_dumped, undo_dump, with_note, without_note)`, `from .suggest import bars, corpus, options, suggest`, and `grab_clipboard_image`, `strip_controls` added to the `from .models import (...)` list (tests patch `taskboard.app.grab_clipboard_image` and spy `taskboard.app.suggest`)
module: taskboard/app.py
modify: [Data: TaskboardApp.inbox] (replace)
examples: (TC-4581) a registry in a temporary folder T → app.inbox.path == T / "inbox.json"; after the first pad write the file exists there and not beside the board file
examples: (TC-4586) no inbox.json in T → app.inbox.pad "", no file created by the constructor

TaskboardApp.check_action
req: LLR-4401.3, LLR-4401.11, LLR-4401.12, LLR-4401.14, LLR-4401.15
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: changed from baseline: the always-allowed tuple becomes ("agenda_all", "people_directory", "marks_manager", "added_list", "capture") — each allowed only while no ModalScreen is on the stack; the holding tuple becomes (BoardsHome, AllBoardsAgenda, PeopleDirectory, MarksManager, AddedList, CaptureView) — while one is on the stack every other SEAT action but `quit` is refused; so the priority app bindings j/k/h/l/up/down/left/right/tab are refused in the pad and in the review list and fall through to the TextArea / the list's own bindings; the docstring names `capture` and `n` beside `A`, `@`, `#`, `N`
module: taskboard/app.py
examples: (TC-4411) a ModalScreen (TaskModal) on the stack, action "capture" → allowed `False`; no ModalScreen → `True`; `a`, then `n` typed in the task editor's title → title holds "n", no CaptureView on the stack (3/3)
examples: (TC-4412) CaptureView open, actions "add_task", "delete", "cursor" → allowed `False` each (3/3); "quit" → `True`
examples: (TC-4403, root action_capture) empty pad, keys n N A q j k h l B u v @ # ? ; typed → pad text "nNAqjkhlBuv@#?;", app.screen still the CaptureView, `0` board writes (3/3: the NC drops CaptureView from the holding tuple, so `j`/`k` reach `cursor` and arm 1 fails)
examples: (TC-4414) AddedList on top (`N`), action "capture" → `True` (no modal); AllBoardsAgenda on top (`A`) → `True`

TaskboardApp.action_capture
req: LLR-4401.2, LLR-4401.14, HLR-4401
in:
out: None
func: new: `n` → `self._bring(CaptureView, CaptureView)` (as action_added_list): a CaptureView already on the stack is brought to the top, else a new one is pushed; docstring "`n`: the capture view (Inc K, LLR-4401.2)"
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (TC-4402, root action_capture) fixture F, `escape` (leaves the home), `n` → app.screen is a CaptureView
examples: (TC-4414, root action_capture) `N`, `n` → stack ["Screen", "AddedList", "CaptureView"]; `escape`, `n` → still exactly `1` CaptureView and it is app.screen; `A`, `n` from the main screen → stack ["Screen", "AllBoardsAgenda", "CaptureView"]; app.run_action("capture") with the CaptureView on top → stack unchanged (3/3)
examples: (AT-4401, root action_capture) 118x30, fixture F, no inbox.json. Keys: `escape` (the home closes), `n` → CaptureView; pad rows 2..5 read `first line → the task's title`, `next lines → its notes`, 24 × `─`, `____ ↵ starts the next note`; screen row 28 (x 0..67) plain `____ ↵ new note · alt+l divider`; row 0 `CAPTURE  0 notes · suggestions read every board`; rail `no notes yet`
examples: (AT-4401, root action_capture) then type `Golden set answer key`, `enter`, `_` `_` `_` `_`, `enter` → screen row 3, cells x 2..65 = 64 × `─`; exactly `1` notification "That ____ line divides notes: the text above and below it dump as two tasks. alt+l inserts one." title "Capture"; S/inbox.json holds "divider_notice": `True`; row 0 `CAPTURE  2 notes · suggestions read every board`
examples: (AT-4401, root action_capture) then type `Pilot stores`, `alt+l` → pad text "Golden set answer key\n____\nPilot stores\n____\n", cursor (4, 0); `escape` → app.screen is the main Screen; S/inbox.json "pad" equals "Golden set answer key\n____\nPilot stores\n____\n"; sha256 of both board.json, both history.jsonl, people.json and marks.json equal their values before `n` (6/6)
examples: (AT-4401, root action_capture) the same keys at 80x24 → the rail-box region (0, 16, 80, 7) starts below the pad region (0, 1, 80, 14); the hint row is (0, 15, 80, 1)

PadArea.__init__
req: LLR-4402.12, LLR-4409.1
in: str text = ""; str? id = None
out: None
func: new class `PadArea(InkArea)` (Inc C's live colour unchanged: its theme "taskboard-ink" and `_build_highlight_map`); `__init__` calls `super().__init__(text, id=id)` then sets `self.placeholder = GHOST` (the module constant: "first line → the task's title\nnext lines → its notes\n" + "─" * 24 + "\n____ ↵ starts the next note"); Textual draws the placeholder only while `self.text == ""`, in the `text-area--placeholder` component style (`#5b6675` via DEFAULT_CSS); `soft_wrap` stays True (the TextArea default), which P-V-1 needs; no pens (R0-11)
module: taskboard/app.py
examples: (TC-4442) empty pad at 118x30 → pad rows 2..5 plain (stripped) "first line → the task's title", "next lines → its notes", 24 × `─`, "____ ↵ starts the next note", colour `#5b6675` (P-V-2); type `x` → none of the 4 lines on screen, pad row 2 "x" (2/2)
examples: (TC-4631) pad text "::b:: x ::" → the cell of "x" carries `#60a5fa` (HEX["blue"]) and the marker cells `#5b6675` (HEX["dim"]) (2/2, the InkArea highlight map)

PadArea.get_line
req: LLR-4402.6, LLR-4402.7, LLR-4402.18, HLR-4402
in: int line_index
out: Text line
func: new override of TextArea's public `get_line` (P-V-1): `line = super().get_line(line_index)`; when `line_index != self.selection.end[0]` and `is_divider(line.plain)` → returns `t = Text("─" * max(w, len(line.plain)), end="", no_wrap=True)` with `t.stylize(HEX["dim"])` (a span, P-V-1b), w = `self.scrollable_content_region.width`; else `line` unchanged. Never touches the highlight map (R1-5) and never changes the document: the stored text keeps its underscores
module: taskboard/app.py
examples: (TC-4436) 118x30, text "a\n____\nb", cursor (2, 1) → screen row 3 holds `─` in all 64 content cells (x 2..65) and no `_`; 80x24 → 76 cells (2/2)
examples: (TC-4437) cursor (1, 0) → that row holds "____" and no `─` (1/1)
examples: (TC-4448) text "a\n____\nb" → `pad._highlights` holds no entry for row `1`; render_line(1) segments read `─` with colour `#5b6675` (2/2: the NC styles the underscores and the row still reads "____")

hit_text
req: LLR-4403.16, LLR-4409.4
in: Hit? hit; int? width = None
out: Text text
func: new pure painter: `t = Text(no_wrap=True)`; hit None → `t.append("+ new project", f"b {HEX['amber']}")`; else `t.append(hit.doc.project_name, f"b {HEX.get(hit.doc.project_colour, HEX['sky'])}")`, `t.append(" · ", HEX["dim"])`, `t.append(hit.doc.board_name, board_hex(hit.doc.board_colour))`, `t.append(" " + bars(hit.score), HEX["accent"] if hit.score >= 0.16 else HEX["amber"])`; `width` → `t.truncate(width, overflow="ellipsis")`; returns t (never parses markup)
module: taskboard/app.py
examples: (TC-4476) hits of scores 0.41, 0.20, 0.09 on Eval harness · Client A → plains "Eval harness · Client A ▰▰▰", "… ▰▰▱", "… ▰▱▱" (3/3); the cells of "Eval harness" carry `b #60a5fa`, "Client A" `#38bdf8` (4/4)
examples: (TC-4634) a project named "[b]P[/b]" on Client A, score 0.2 → plain "[b]P[/b] · Client A ▰▰▱" (literal brackets)
examples: (TC-4476) hit None → plain "+ new project", style `b #fbbf24`

capture_head
req: LLR-4401.9, LLR-4403.20, LLR-4409.4
in: int count; int unread; int width
out: Text head
func: new pure painter: `t = Text(no_wrap=True)`; `t.append("CAPTURE", f"b {HEX['accent']}")`; `t.append(f"  {count} note{'' if count == 1 else 's'} · suggestions read every board", HEX["mut"])`; unread > 0 → `t.append(f" · {unread} board{'' if unread == 1 else 's'} not read", HEX["amber"])`; `t.truncate(width, overflow="ellipsis")`; width = the screen width − 2 (the head's padding)
module: taskboard/app.py
examples: (TC-4409) count `3`, unread `0`, width `116` → plain "CAPTURE  3 notes · suggestions read every board"; count `1` → "CAPTURE  1 note · suggestions read every board" (2/2)
examples: (TC-4480) count `3`, unread `1` → plain ends " · 1 board not read"; unread `2` → ends " · 2 boards not read"
examples: (TC-4401, harness) count `0`, unread `0` → plain "CAPTURE  0 notes · suggestions read every board"

capture_hint
req: LLR-4402.11
in:
out: Text hint
func: new pure painter of CAPTURE_HINT: `t = Text(no_wrap=True)`; `t.append("____ ↵", KEY_STYLE)`, `t.append(" new note", HEX["mut"])`, `t.append(" · ", HEX["dim"])`, `t.append("alt+l", KEY_STYLE)`, `t.append(" divider", HEX["mut"])` → plain "____ ↵ new note · alt+l divider" (31 cells, fits 66 and 78); the `#cap-hint` Static under the pad holds it in every state (it is never hidden or updated)
module: taskboard/app.py
examples: (TC-4441) the hint row's plain text equals "____ ↵ new note · alt+l divider" at 118x30 (row 28) and 80x24 (row 15), with an empty pad, with 3 notes (N1, N2, N3) and with the name field open (4/4)

rail_rows
req: LLR-4401.8, LLR-4401.16, LLR-4401.17, LLR-4403.15, LLR-4403.17, LLR-4403.18, LLR-4403.19, LLR-4403.25, LLR-4405.13, LLR-4407.31, LLR-4408.9, LLR-4409.4
in: list[RailNote] notes; int? cur; int width; bool wide; int dumped
out: Text rail
func: new pure painter; rows built as Text (no_wrap, each truncated to `width` with "…"), joined by "\n" onto one `out = Text()`. No notes → the one row "no notes yet" (dim), then, wide and dumped > 0, a blank row and the dumped row. Wide: every note in pad order; narrow (`wide` False): only notes[cur]; cur None and notes exist → the one row "no note under the cursor" (dim, P-V-7 ruled ACCEPT, LLR-4401.17). Per note k (1-based), p = "▌" (accent) when k−1 == cur else " ": (1) p + f"{k} " (`b accent` on the cursor's note, else dim) + title (`b ink` / hd) + (f"  ▣ {n}" in amber when n = note.images > 0); a flagged note (note.flag set) → (2) p + "  ⚑ " + note.flag (amber; note.flag = f"on {board} — delete it here", P-V-8 ruled) and nothing else; else (2) p + "  → " (accent) + hit_text(chosen); (3) chosen not None → p + "    why " (dim) + " · ".join(chosen.why[:3]) (mut); chosen None and hits → p + "    weak: " (dim) + " · ".join(hits[0].why[:2]) + f" ({hits[0].doc.project_name})" (mut); chosen None, no hits → p + "    no project shares a word" (mut); (4) only on the cursor's note and only when the note has other options → p + "    or " (dim) + the options other than the chosen one, in options order, each hit_text, joined by "  ·  " (dim); then, wide only, one blank row. Wide and dumped > 0 → last row "✓ dumped {dumped}" (`b #3f9c6d`) + "  ·  alt+u undo  ·  kept 7 days" (dim)
module: taskboard/app.py
examples: (TC-4475) N1, N2, N3, cur `2`, width `48`, wide, dumped `0` → plain rows " 1 Golden set: 12 questions still have no answe…", "   → Eval harness · Client A ▰▰▰", "     why questions · @username_subject · key", "", " 2 Volume lab fails on WSL  ▣ 1", "   → Module 4 · Volumes · Course ▰▰▰", "     why volume · oracle · script", "", "▌3 Quote for the new client: contracts Q&A", "▌  → + new project", "▌    no project shares a word", "" (9 lines + 3 spacers; hits = G-T's executed TC-4475 example)
examples: (TC-4477) N1, N2, N3, cur `0` → rows 1..4 "▌1 Golden set: 12 questions still have no answe…", "▌  → Eval harness · Client A ▰▰▰", "▌    why questions · @username_subject · key", "▌    or Pilot rollout · Client A ▰▰▱"; notes 2 and 3 have no "or" row (2/2)
examples: (TC-4478) N3 chosen None, hits [] → its reason row "     no project shares a word" (exact, cursor elsewhere)
examples: (TC-4479) N5 chosen None, hits [Pilot rollout 0.1488 why chair, region] (G-T's executed TC-4479), cur `0` → rows "▌1 Answer the region chair", "▌  → + new project", "▌    weak: chair · region (Pilot rollout)", "▌    or Pilot rollout · Client A ▰▱▱"
examples: (TC-4408) N1, N2, N3, cur `1`, width `78`, narrow → plain rows "▌2 Volume lab fails on WSL  ▣ 1", "▌  → Module 4 · Volumes · Course ▰▰▰", "▌    why volume · oracle · script": exactly `1` title row of the 3 notes (3/3 with the region arms of CaptureView._paint)
examples: (TC-4416) notes [], wide, dumped `0` → plain "no notes yet"
examples: (TC-4485) one board with 0 projects, note "rotation plan" → rows "▌1 rotation plan", "▌  → + new project", "▌    no project shares a word"; `0` exceptions (2/2)
examples: (TC-4553) N3 only, dumped `2`, wide → last row "✓ dumped 2  ·  alt+u undo  ·  kept 7 days"; dumped `0` → no row starting "✓ dumped" (2/2)
examples: (TC-4619) N2 → its title row ends "  ▣ 1"; N3 → no "▣" (2/2)
examples: (TC-4671) N1, N2 flagged with flag "on Course — delete it here", N3, cur `0`, width `48` → rows 5..6 " 2 Volume lab fails on WSL  ▣ 1", "   ⚑ on Course — delete it here" (31 cells, uncut); no "→ Module" option row for it (2/2; P-V-8 ruled)
examples: (TC-4417) notes [N1, N2], cur `None`, width `78`, narrow → the one row "no note under the cursor" (1/1)
examples: (TC-4634) note title "[red]x[/red] [@click=app.quit]q", cur `0` → row 1 plain "▌1 [red]x[/red] [@click=app.quit]q" (literal; the app keeps running)

review_rows
req: LLR-4406.2, LLR-4406.13, LLR-4409.4
in: list[ReviewRow] rows; int sel; int width
out: Text body
func: new pure painter; tw = width − 42 when width ≥ 90 (wide) else width − 6. Per row i: r1 = ("▶ " if i == sel else "  ", accent) + ("[x] ", `b accent`) or ("[ ] ", dim) + the title (row.title, or "(no title line)" in dim when ""), `b ink` on sel else hd, truncated to tw with "…" and padded to tw (`truncate(tw, overflow="ellipsis", pad=True)`); wide and not flagged → "  " + hit_text(row.option, 34). r2 = "      " + (narrow and not flagged → hit_text(row.option, 34) + "  ") + (flagged → "⚑ " + row.flag in amber, row.flag = "on <board> — delete it here" (P-V-8); option None → "needs a name: alt+n in the pad" in amber; else "why " dim + " · ".join(row.option.why[:3]) mut), truncated to width. After the rows: a blank row and `key_line([("↑↓", "move"), ("␣", "include"), ("o", "other"), ("d", f"dump {k} checked"), ("u", "undo"), ("esc", "back")], width)`, k = the checked count. Joined onto one Text
module: taskboard/app.py
examples: (TC-4562) rows N1 [x] Eval harness, N2 [x] Module 4 · Volumes, N3 [ ] None, N4 [x] Pilot rollout, sel `0`, width `108` → plain lines "▶ [x] Golden set: 12 questions still have no answer key                   Eval harness · Client A ▰▰▰", "      why questions · @username_subject · key", "  [x] Volume lab fails on WSL                                             Module 4 · Volumes · Course ▰▰▰", "      why volume · oracle · script", "  [ ] Quote for the new client: contracts Q&A                             + new project", "      needs a name: alt+n in the pad", "  [x] Steering deck: demo the hybrid search on pilot stores               Pilot rollout · Client A ▰▰▰", "      why pilot · stores · steering", "", "↑↓ move   ␣ include   o other   d dump 3 checked   u undo   esc back" (trailing spaces stripped)
examples: (TC-4573) the same rows with N4 unchecked → last line holds "d dump 2 checked"; width `72` → all 6 key glyphs "↑↓", "␣", "o", "d", "u", "esc" present (2/2)
examples: (TC-4634) a row titled "[red]x[/red]" → r1 holds the literal "[red]x[/red]"

CaptureView.compose
req: LLR-4401.6, LLR-4401.7, LLR-4401.8, LLR-4401.18, LLR-4403.23, LLR-4407.13, LLR-4407.27, HLR-4401
in:
out: ComposeResult widgets
func: new `CaptureView(Screen[None])`, BINDINGS all priority (P-V-3; P-V-2 ruled, LLR-4401.18): escape→close, alt+d→dump, alt+o→other, alt+n→new, tab→board (P-V-1 ruled: acts only while the name field is open, else does nothing), alt+a→review, alt+i→image, alt+u→undo, alt+l→divider; NO alt+enter, no alt+b. compose: `self._refreshed = self.app.inbox.refresh()` (re-read only when the store stamp changed; never writes), `self._rebuild_docs()`, then yields `Static(id="cap-head")`, `Horizontal(#cap-main)` holding `Vertical(#cap-left)` [PadArea(self.app.inbox.pad, id="cap-pad"), Static(capture_hint(), id="cap-hint")] and `Vertical(#cap-rail-box)` [Static(id="cap-rail"), Input(placeholder="project name", id="cap-new")], then `Static(id="cap-keys")`. State set here: `self._saved = self.app.inbox.pad`, `self._text = self._saved`, `self.choice = {}`, `self._field = None`, `self._field_lane = 0`, `self._timer = None`, `self._esc_armed = False`, `self._flag_pending = False`, `self._pending_drop = None`. Writes no board, no history, no store
module: taskboard/app.py
modify: [Data: CaptureView.docs] (replace); [Data: CaptureView._saved] (replace)
examples: (TC-4406, root action_capture) store "pad" "a\n____\nb" → pad text "a\n____\nb" (1/1)
examples: (TC-4407, root action_capture) 118x30 → rail-box region x `68`, width `50`; pad region x `0` (2/2, P-V-5)
examples: (TC-4593, root action_capture) a second Inbox wrote pad "x" after this app loaded → the next `n` shows pad "x"; a reopen with the file unchanged → `0` parses (spy on Inbox._read) (2/2)
examples: (TC-4483, root action_capture) fixture F → CaptureView.docs holds `3` docs: 2 from Client A and 1 from Course (corpus over both lanes, not app.board only)
examples: (TC-4607, root action_capture) `n`, type "abc", wait 1.3 s, `escape` → sha256 of both board.json, both history.jsonl, people.json and marks.json unchanged (6/6)
examples: (TC-4447, harness) CaptureView.BINDINGS, PadArea.BINDINGS (inherited) and ReviewList.BINDINGS → no key list names "alt+enter"
examples: (TC-4418, root action_capture) pad "abc", cursor (0, 1), `events.Key("alt+o", "o")` posted through the driver (the terminal form, P-V-3) → pad text "abc"; `events.Key("alt+u", "u")` with empty "dumped" → pad "abc", notification "Nothing to undo."; every CaptureView binding `priority` `True` (3/3)

CaptureView.on_mount
req: LLR-4401.5, LLR-4401.8, LLR-4407.8, LLR-4407.14, LLR-4407.38
in:
out: None
func: new: `pad.focus()`, `pad.move_cursor(pad.document.end)`; `self.set_class(self.app.size.width < 100, "-narrow")`; the load notice once per app: when `app.inbox.load_report.get("unreadable")` and not `app._inbox_said` → `app._inbox_said = True` and notify, backup = load_report["backup"]: with a backup → f"inbox.json could not be read; it was copied to {Path(backup).name} and the pad starts empty." else "inbox.json could not be read and no copy could be kept; the pad starts empty." (P-V-6 ruled ACCEPT, LLR-4407.38), title "Capture", severity "warning", timeout 15, markup False; `self._refreshed is False` → notify "inbox.json could not be read; the pad as loaded is kept." (title "Capture", warning, 15, markup False; Inbox.refresh reports a bad stamp once); then `self._paint()`. `on_resize` re-sets the class and repaints; `on_screen_resume` repaints (after the review list)
module: taskboard/app.py
examples: (TC-4405, root action_capture) store pad "a\nb" → app.focused is the pad; cursor_location == document.end (`(1, 1)`) (2/2)
examples: (TC-4588, root action_capture) inbox.json holding `{"pad": 5}` → notification "inbox.json could not be read; it was copied to inbox.json.corrupt and the pad starts empty." severity "warning", markup `False`; pad "" (3/3); a second `n` → no second such notification
examples: (TC-4594, root action_capture) the file made "{not json" after load → `1` notification "inbox.json could not be read; the pad as loaded is kept."; pad as loaded; `escape`, `n` with the file unchanged → no second one (3/3)
examples: (AT-4406, root action_capture) inbox.json = `{"pad": 5}`; `escape`, `n` → pad "", the set-aside notice, S/inbox.json.corrupt bytes == `{"pad": 5}`
examples: (TC-4678, root action_capture) inbox.json of 8 388 609 bytes (load_report backup `None`) → notification "inbox.json could not be read and no copy could be kept; the pad starts empty." severity "warning", markup `False`; pad "" (2/2 with the keep_aside-None arm)

CaptureView._rebuild_docs
req: LLR-4403.20, LLR-4403.23, LLR-4403.24, LLR-4403.21
in:
out: None
func: new: `self.lanes, self.ids = board_lanes(self.app)`; `self.docs = corpus(self.lanes, self.app.marks.marks)`; `self.unread = sum(1 for lane in self.lanes if lane[2] is None)`; `self._hits = {}` (the cache is valid only for these docs). Called by compose, after every dump that saved a board and after every undo in state "undone"
module: taskboard/app.py
modify: [Data: CaptureView.docs] (replace); [Data: CaptureView._hits] (clear)
examples: (TC-4484, root action_dump) before: note "rotation" → hits [] ; dump note "Rotation plan" into Eval harness (alt+d with that choice), then type note "rotation" → hits hold Eval harness `0.1179` why "rotation" (G-T's executed TC-4484)
examples: (TC-4480, root action_capture) Course's board.json deleted before `n` → unread `1`, head ends " · 1 board not read", no doc from Course

CaptureView.options_for
req: LLR-4403.21, LLR-4404.17, LLR-4403.28
in: str text
out: list[Hit?] opts
func: new: hits = `self._hits.get(text)`, else nt = `note_task(text)` and `self._hits[text] = suggest(nt.title + "\n" + nt.notes, self.docs)` (the module attribute `suggest`, so a spy sees each call; the cache keyed by the Part text, the scored text without image lines: P-T-4 ruled, LLR-4403.28); returns `options(hits)`. `chosen(text)` = opts[self.choice.get(text, 0) % len(opts)]; the choice dict is keyed by the note's exact text and shared with the review list (S-c)
module: taskboard/app.py
modify: [Data: CaptureView._hits] (append)
examples: (TC-4481, root action_capture) pad N1, N2, N3 painted (3 suggest calls), then 5 characters typed at the end of N2's first line → `0` further calls for N1's and N3's texts (spy on taskboard.app.suggest; calls only for N2's 5 new texts)
examples: (TC-4517, root action_other) cursor in N1, `alt+o`, then `alt+a` → review row 1 shows "Pilot rollout · Client A ▰▰▱", the same option as the rail's `→` line
examples: (TC-4488, root action_capture) pad N2 → the spy sees suggest called with "Volume lab fails on WSL\nthe oracle script expects /mnt/c" (no image line)

CaptureView._paint
req: LLR-4401.8, LLR-4401.9, LLR-4401.10, LLR-4401.16, LLR-4403.15, LLR-4404.22, LLR-4402.11, HLR-4401
in:
out: None
func: new: parts = `note_parts(pad.text)`, notes = [p for p in parts if p.is_note]; cur = index in notes of `note_at(pad.text, pad.cursor_location[0])` (None when that is None); `#cap-head` ← capture_head(note_count(pad.text), self.unread, w − 2); `#cap-rail` ← rail_rows([RailNote(note_task(p.text).title, image-line count, self.options_for(p.text), chosen, hits, flag line from `app.inbox.flag_for(p.text)` via `_where`)], cur, rail content width (48 wide / 78 narrow), wide = w ≥ 100, dumped = len(prune_dumped(app.inbox.dumped, datetime.now()))); `#cap-keys` ← field closed: key_line(CAPTURE_KEYS, w − 2) with CAPTURE_KEYS = [("alt+d", "dump"), ("alt+o", "other"), ("alt+n", "new project"), ("alt+a", "review"), ("alt+i", "image"), ("alt+u", "undo"), ("esc", "close")]; field open: key_line([("↵", f"create on {lane name} + dump"), ("⇥", "board"), ("esc", "back")], w − 2) (P-V-1 ruled); then `self._notice_divider()`. Called on mount, resize, screen resume, every TextArea.Changed and SelectionChanged, and after every action
module: taskboard/app.py
examples: (TC-4410, root action_capture) 80x24 → key row plain "alt+d dump   alt+o other   alt+n new project   alt+a   alt+i   alt+u   esc" (7/7 glyphs); 118x30 → "alt+d dump   alt+o other   alt+n new project   alt+a review   alt+i image   alt+u undo   esc close" (7/7 words) (2/2, P-V-6)
examples: (TC-4408, root action_capture) 80x24, pad N1\n____\nN2\n____\nN3, cursor in N2 → rail region (0, 16, 80, 7), y `16` > the pad's last row `14`, height `7`; its rows hold exactly 1 title row, "▌2 Volume lab fails on WSL  ▣ 1"
examples: (TC-4522, root action_new) 118x30, field open, open board Client A → key row plain "↵ create on Client A + dump   ⇥ board   esc back"
examples: (TC-4409, root action_capture) pad N1\n____\nN2\n____\nN3 → head plain "CAPTURE  3 notes · suggestions read every board"
examples: (TC-4416, root action_capture) empty pad, no dumped entries → rail plain "no notes yet"

CaptureView._notice_divider
req: LLR-4402.13, LLR-4402.14, LLR-4402.15
in:
out: None
func: new: returns at once when `app.inbox.divider_notice` is True or `app._divider_said`; else when any line i of pad.text has `is_divider(line)` and i != the cursor row (a line drawn as a rule, P-V-1) → `app._divider_said = True`; notify("That ____ line divides notes: the text above and below it dump as two tasks. alt+l inserts one.", title="Capture", severity="information", timeout=15, markup=False); then `app.inbox.mark_notice()` (OSError → notify f"inbox.json could not be saved: {error}", warning; the session flag still holds it to once); after a successful mark, `self._saved` is unchanged (mark_notice keeps the pad the file holds)
module: taskboard/app.py
modify: [Data: inbox.json] (replace)
examples: (TC-4443, root action_capture) empty pad, type "a", `enter`, "____", `enter` → exactly `1` notification with that text, title "Capture", markup `False`; then "b", `enter`, "____", `enter` → still `1` (2/2)
examples: (TC-4444, root action_capture) after the notice → S/inbox.json read back holds "divider_notice": `True` (1/1)
examples: (TC-4445, root action_capture) a new TaskboardApp on a store with "divider_notice": true, a divider made → `0` such notifications (1/1)
examples: (TC-4592, root action_capture) "divider_notice": "yes" and 1 → the notice shows on the first divider (2/2; Inbox.load reads only the boolean true)

CaptureView.on_text_area_changed
req: LLR-4407.15, LLR-4407.18, LLR-4407.25
in: TextArea.Changed event
out: None
func: new: `self._text = pad.text`; `self._esc_armed = False`; when `self._unsaved()` (= strip_controls(self._text) != self._saved or self._flag_pending or self._pending_drop is not None) → stop `self._timer` and `self._timer = self.set_timer(1.0, self._flush)` (debounce: one write 1.0 s after the last change); `self._paint()`. `on_text_area_selection_changed` sets `self._esc_armed = False` and repaints (no timer)
module: taskboard/app.py
modify: [Data: CaptureView._text] (replace)
examples: (TC-4595, root action_capture) type "abc", wait 1.3 s → stored "pad" "abc"; 10 keys 0.05 s apart then 1.3 s → exactly `1` call of Inbox.write_pad (spy) (2/2)
examples: (TC-4598, root action_capture) open, move the cursor, wait 1.3 s, `escape` → inbox.json bytes and mtime unchanged; with no inbox.json, no file created (2/2)

CaptureView._flush
req: LLR-4407.15, LLR-4407.18, LLR-4407.21, LLR-4407.22, LLR-4407.23, LLR-4407.37, LLR-4402.16, LLR-4409.5
in:
out: bool saved
func: new: the one pad write. Not `_unsaved()` → True (no write). text = strip_controls(pad.text); `res = app.inbox.write_pad(text, drop=self._pending_drop)`; OSError e → notify(f"inbox.json could not be saved: {e}", title="Capture", severity="warning", timeout=15, markup=False), return False (pad and memory kept). Success → `self._saved = res.pad`, `self._flag_pending = False`, `self._pending_drop = None`; `res.written and res.pad != pad.text` (a union or stripped controls, P-S-8 ruled) → pad.text = res.pad, cursor (min(row, last line), min(col, that line's length)), `self._text = res.pad`; only `res.union` → notify("inbox.json changed in another window: its notes were merged into the pad.", title="Capture", severity="warning", timeout=15, markup=False); return True. The divider lines go verbatim (no normalising)
module: taskboard/app.py
modify: [Data: inbox.json] (replace); [Data: CaptureView._saved] (replace)
examples: (TC-4446, root action_capture) type "______" → pad text and stored "pad" both "______" (1/1)
examples: (TC-4600, root action_capture) pad "a\n________\n\nb  " on an unchanged file → stored "pad" byte-identical "a\n________\n\nb  "
examples: (TC-4601, root action_capture) the file changed by a second Inbox (fresh pad "a\n____\nc", fresh dumped text "b"), this pad "a\n____\nb\n____\nd", cursor (4, 1) → pad text "a\n____\nc\n____\nd", cursor (4, 1) (2/2)
examples: (TC-4602, root action_capture) the same → notification "inbox.json changed in another window: its notes were merged into the pad." (1/1)
examples: (TC-4603, root action_capture) a fresh foreign S/inbox.json.lock, type "x", wait 3.3 s (LOCK_WAIT 2 s + debounce) → notification starting "inbox.json could not be saved: " and holding "is busy"; pad "x"; app.inbox.dumped unchanged (2/2)
examples: (TC-4635, root action_capture) a pasted "\x1b" and "\x9b" in the pad → stored "pad" holds neither, and the pad text holds neither after the write (P-S-8), no merge notification (2/2)
examples: (TC-4677, root action_capture) a pad of "a" × 8 400 000 pasted, wait 1.3 s → notification "inbox.json could not be saved: inbox.json would hold 8400047 bytes, over the 8388608-byte limit, so it was not written" (G-S's OSError text after LLR-4407.23's prefix); inbox.json bytes and app.inbox.pad unchanged (3/3)
examples: (TC-4589, root action_capture) unreadable store with keep_aside patched to return None, type "x", wait 1.3 s → file bytes unchanged; the save notification holds "was not written" (G-S's OSError text, shown verbatim)
examples: (AT-4408, root action_capture) this pad "a\n____\nb"; a second Inbox instance records a dump entry of text "b" and writes pad "a\n____\nc"; here type `enter`, "____", `enter`, "d" (pad "a\n____\nb\n____\nd"), wait 1.3 s → S/inbox.json "pad" == "a\n____\nc\n____\nd", the pad shows it, the merge notification once, and the boards hold the one task the second window made (no task created twice)

CaptureView.action_close
req: LLR-4401.4, LLR-4404.27, LLR-4407.16, LLR-4407.24, LLR-4407.25
in:
out: None
func: new, `escape` (priority): name field open → hide it (`remove_class("on")`, value ""), `self._field = None`, focus the pad, repaint, return. Else when `self._unsaved()`: `self._esc_armed` → stop the timer, `self.app.pop_screen()` (closes without saving; on_unmount tries once more); else `self._flush()` True → pop; False → `self._esc_armed = True`, notify("inbox.json could not be saved — esc again closes without saving.", title="Capture", severity="warning", timeout=15, markup=False) and stay. Nothing unsaved → pop. Any text change or cursor move disarms (on_text_area_changed / selection_changed)
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace); [Data: CaptureView._esc_armed] (replace)
examples: (TC-4404, root action_close) field closed, nothing unsaved, `escape` → app.screen is the main Screen (1/1)
examples: (TC-4527, root action_close) field open, `escape` → field hidden; app.focused is the pad; boards and inbox.json unchanged (3/3)
examples: (TC-4596, root action_close) type "abc" then `escape` at once → stored "pad" "abc" (1/1)
examples: (TC-4604, root action_close) a fresh foreign inbox.json.lock, type "x", `escape` → the view stays on top; notification "inbox.json could not be saved — esc again closes without saving." (2/2)
examples: (TC-4605, root action_close) then `escape` → closed (1/1); instead "y" typed then `escape` → the warning again (2/2)
examples: (AT-4406, root action_close) a held S/inbox.json.lock: type "x", wait 3.3 s → the save notification, pad "x"; `escape` → the esc warning once; `escape` → the main Screen

CaptureView.on_unmount
req: LLR-4407.17
in:
out: None
func: new: stops `self._timer`; when `self._unsaved()` → `app.inbox.write_pad(strip_controls(self._text), drop=self._pending_drop)` inside try/except OSError (swallowed: the screen is gone). Reads `self._text`, never the PadArea (P-V-4: children are already removed at unmount)
module: taskboard/app.py
modify: [Data: inbox.json] (replace)
examples: (TC-4597, root action_capture) type "abc", `app.exit()` at once → stored "pad" "abc" (1/1)

CaptureView.action_divider
req: LLR-4402.9, LLR-4402.10, LLR-4402.17
in:
out: None
func: new, `alt+l` (priority, P-V-3); field open → nothing. row = cursor row, line = pad.document.get_line(row): line.strip() == "" → `pad.replace("____\n", (row, 0), (row, len(line)))`; else `pad.insert("\n____\n", (row, len(line)))`; then `pad.move_cursor((row + 1, 0))` when blank else `(row + 2, 0)` (the TextArea edit keeps undo; Changed drives the debounce)
module: taskboard/app.py
examples: (TC-4439, root action_divider) "abc", cursor (0, 1), `alt+l` → text "abc\n____\n", cursor (2, 0); "abc\nd", cursor (0, 1) → "abc\n____\n\nd", cursor (2, 0) (2/2)
examples: (TC-4440, root action_divider) "a\n", cursor (1, 0) → "a\n____\n", cursor (2, 0) (1/1)
examples: (TC-4447, root action_capture) "abc", cursor (0, 3), the key event Key("enter", "\r") of ESC CR (what alt+enter sends) → text "abc\n", no "____" line (2/2 with the bindings arm of CaptureView.compose)

CaptureView.action_dump
req: LLR-4404.18, LLR-4404.28, LLR-4404.30, HLR-4404
in:
out: None
func: new, `alt+d` (priority); field open → nothing. part = `note_at(pad.text, cursor row)` (on a divider line the note above); None → notify("No note under the cursor.", title="Capture", severity="warning", timeout=10, markup=False); else `self.dump_part(part, quiet=False)`
module: taskboard/app.py
examples: (TC-4528, root action_dump) empty pad: `alt+d`, `alt+o`, `alt+n` → each "No note under the cursor."; `0` changes (3/3)
examples: (TC-4530, root action_dump) "a\n____\nb", cursor row 1 → the note dumped is "a"; row 2 → "b" (2/2, note_at's rule)
examples: (TC-4518, root action_dump) cursor in N3 (chosen + new project), `alt+d` → the name field shown and focused, border title "New project for note 1"; no board changed (2/2)
examples: (AT-4402, root action_dump) fixture F, store pad = N2 with S/inbox-images/board-0938.png present. Keys: `escape`, `n` → rail rows "▌1 Volume lab fails on WSL  ▣ 1", "▌  → Module 4 · Volumes · Course ▰▰▰", "▌    why volume · oracle · script"; `alt+d` → Course's board.json holds a task titled "Volume lab fails on WSL", notes "the oracle script expects /mnt/c", phase "Todo", created matching `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$`, images [S/boards/course/images/<id>/board-0938.png]; S/inbox-images/board-0938.png gone; pad ""; notification "Dumped → Module 4 · Volumes · Course   ·   alt+u undo"; inbox.json "dumped" holds `1` entry with images ["board-0938.png"]

CaptureView.dump_part
req: LLR-4407.32, LLR-4404.29, LLR-4404.18, HLR-4404
in: Part part; bool quiet
out: bool ok
func: new, the one dump path of `alt+d` and the review list's `d`: flag = `app.inbox.flag_for(part.text)` → notify(f"This note is already on {board}; delete it from the pad.", warning) and False (board = `_where(flag["board"], flag["project"])[1]`); `note_task(part.text).title == ""` → notify("This note has no text line for a title.", warning), False; ch = chosen(part.text); ch None → quiet: False; else open the name field for this note (as action_new) and False; else `self._dump(part, ch.doc.board_path, ch.doc.board_name, ch.doc.project_id, None, quiet, ch.doc.project_name)`
module: taskboard/app.py
examples: (TC-4672, root action_dump) a flagged note (text N2, flag board S/boards/course/board.json), `alt+d` → `0` tasks added; notification "This note is already on Course; delete it from the pad." (3/3 with the review arms of ReviewList.action_toggle)
examples: (TC-4529, root action_dump) note "img: a.png" and note "::b:: ::" → "This note has no text line for a title."; `0` tasks (2/2)

CaptureView._dump
req: LLR-4404.1, LLR-4404.6, LLR-4404.7, LLR-4404.8, LLR-4404.10, LLR-4404.11, LLR-4404.12, LLR-4404.13, LLR-4404.14, LLR-4405.14, LLR-4407.26, LLR-4407.29, LLR-4407.30, LLR-4403.24, LLR-4408.12, LLR-4409.4
in: Part part; Path path; str board; str? project_id; str? new_name; bool quiet; str project_name = ""
out: bool ok
func: new: target = DumpTarget(path, board, live=app.board when `Path(path).resolve() == Path(app.board.path).resolve()` else None); stop the timer; out = `dump_note(target, project_id, new_name, part.text, app.inbox.images_dir, project_name)` (P-S-1: `project_name` = the chosen hit's `doc.project_name`, "" for a new project); not out.ok → notify(out.notice, title="Capture", severity="warning", timeout=15, markup=False) (G-S's text, shown verbatim), return False, pad untouched. ok → new, row = `without_note(pad.text, part)`; entry = `entry_for(out, part.text, path, datetime.now())` (P-S-15 ruled: G-V builds no entry itself; `images` = out.images, the moved file names, P-V-13); try `res = app.inbox.write_pad(strip_controls(new), record=entry)` (LLR-4407.29: at once): success → pad.text = res.pad (P-S-8: whatever the file now holds), cursor (row, 0), `self._text`/`self._saved` = res.pad, union → the merge notice; OSError e → the pad keeps the note, `app.inbox.flag(entry)`, `self._flag_pending = True`, the timer restarted (1.0 s), notify(f"{out.project_name} · {board} got the task, but inbox.json could not be saved: {e} — the note stays in the pad, flagged ⚑.", severity="warning", timeout=30, markup=False). Then (both branches) not quiet and the store write succeeded → notify(f"Dumped → {out.project_name} · {board}   ·   alt+u undo", title="Capture", severity="information", timeout=10, markup=False); out.missing → notify(f"{len(out.missing)} image(s) not found: {', '.join(out.missing)}", warning); target.live → `app.refresh_view()` (P-V-8: reaches the board view from a pushed screen); `self._rebuild_docs()`; repaint; return True. Never touches `app._undo_stack`
module: taskboard/app.py
modify: [Data: inbox.json] (replace); [Data: CaptureView._saved] (replace); [Data: Inbox state] (append)
examples: (TC-4501, root action_dump) cursor in N2 → Course's task count +1, the new task's project_id = Module 4 · Volumes' id (2/2: not the open board)
examples: (TC-4506, root action_dump) pad "a\n____\nb\n____\nc" with b and c dumpable: dump b → pad "a\n____\nc"; dump c → "a\n____\nb"; every other line byte-identical (3/3, without_note applied)
examples: (TC-4507, root action_dump) → notification "Dumped → Module 4 · Volumes · Course   ·   alt+u undo", markup `False`, title "Capture" (1/1)
examples: (TC-4508, root action_dump) N1 into Eval harness (Client A, the open board) → app.board holds the task; Client A's board.json holds it; after `escape` the board view's render holds "Golden set: 12 questions still have no answer key" (3/3)
examples: (TC-4510, root action_dump) Course's file deleted after `n` → notification "Course's file is missing — nothing dumped."; pad unchanged; no file at that path (3/3)
examples: (TC-4511, root action_dump) Course's file made "{bad" → "Course's file cannot be read — nothing dumped."; file bytes unchanged (2/2)
examples: (TC-4512, root action_dump) Module 4 · Volumes removed from Course's file after `n` → "Module 4 · Volumes is no longer on Course — nothing dumped." (2/2)
examples: (TC-4513, root action_dump) a fresh foreign Course board.json.lock → notification holds "is busy"; pad and board bytes unchanged (3/3)
examples: (TC-4514, root action_dump) Course's board.json read-only → notification starts "Course could not be saved: " and ends " — nothing dumped."; pad unchanged (2/2)
examples: (TC-4554, root action_dump) dump N1 (open board) → len(app._undo_stack) unchanged (`0`); `escape`, `u` on the board → "Nothing to undo." and the task stays (3/3 with action_undo's arm)
examples: (TC-4606, root action_dump) taskboard.inbox.write_atomic patched to raise OSError once, dump N2 → Course holds the task; the pad still holds N2; app.inbox.flagged holds `1` entry with text N2; after 1.3 s (the retry write succeeds) inbox.json "flagged" holds it and "dumped" does not (4/4)
examples: (TC-4670, root action_dump) the same → notification starting "Module 4 · Volumes · Course got the task, but inbox.json could not be saved: " and ending " — the note stays in the pad, flagged ⚑.", markup `False`, severity "warning" (1/1)
examples: (TC-4609, root action_dump) after `alt+d` → stored "pad" equals the pad text with no wait (0 s) (1/3; the undo and image arms on their nodes)
examples: (TC-4622, root action_dump) a note "T\nimg: gone.png" (no such file) dumped → the task notes hold "img: gone.png"; notification "1 image(s) not found: gone.png" (2/2)
examples: (TC-4634, root on_input_submitted) a new project "[b]P[/b]" on Client A → notification "Dumped → [b]P[/b] · Client A   ·   alt+u undo" literal (markup False; the notice holds no note title, finding P-V-9)

CaptureView._where
req: LLR-4407.31, LLR-4407.32, LLR-4405.9
in: str board_path; str project_id
out: tuple(str project, str board)
func: new: board = the name of the registry entry whose resolved path equals `Path(board_path).resolve()` (`app.registry.active()`), else `name_for(board_path)`; project = the name of the project with that id on that lane's board when the lane is readable, else the id itself (finding P-V-8: flagged/dumped entries carry ids only)
module: taskboard/app.py
examples: (TC-4671, harness) board_path "S/boards/course/board.json", project_id "pv" → project "Module 4 · Volumes", board "Course" (the rail's flag line "on Course — delete it here")
examples: (TC-4549, harness) a path in no registry entry ".../loose/board.json" → board "loose" (name_for)

CaptureView.action_other
req: LLR-4404.16, LLR-4404.17
in:
out: None
func: new, `alt+o` (priority); field open → nothing; part None → "No note under the cursor." (warning); else `self.choice[part.text] = self.choice.get(part.text, 0) + 1` (wraps through `% len(opts)` when read), repaint
module: taskboard/app.py
modify: [Data: CaptureView.choice] (replace)
examples: (TC-4516, root action_other) cursor in a note with 3 options [A, B, C] → `alt+o` ×3 → the rail's `→` line shows A again; after one `alt+o` it shows B (2/2)
examples: (AT-4403, root action_other) pad N5, cursor in it → rail "▌  → + new project", "▌    weak: chair · region (Pilot rollout)"; `alt+o` → "▌  → Pilot rollout · Client A ▰▱▱"; `alt+o` → "▌  → + new project" again

CaptureView.action_new
req: LLR-4404.19, LLR-4404.20, LLR-4404.28, LLR-4407.32
in:
out: None
func: new, `alt+n` (priority); field open → nothing; part None → "No note under the cursor."; flagged → the flagged refusal of dump_part (P-V-10 ruled ACCEPT, LLR-4407.32); title "" → "This note has no text line for a title."; else `self._field = part.text`, `self._field_lane` = the index of the lane whose board is `app.board`, the Input: `border_title = Text(f"New project for note {k}")` (k = 1-based position of the part among the notes), value "", `add_class("on")`, `focus()`; repaint (key row of the field)
module: taskboard/app.py
modify: [Data: CaptureView._field] (replace)
examples: (TC-4519, root action_new) pad N1\n____\nN2\n____\nN3, cursor in N3, `alt+n` → field border title plain "New project for note 3" (1/1)
examples: (TC-4520, root action_new) open board Course (lane 1) → key row "↵ create on Course + dump   ⇥ board   esc back" (1/1; the NC starts at lane 0 Client A)
examples: (TC-4672, root action_new) a flagged note (text N2), `alt+n` → no name field; notification "This note is already on Course; delete it from the pad." (the alt+n arm)

CaptureView.action_board
req: LLR-4404.21
in:
out: None
func: new, `tab` (priority, P-V-1 ruled: the orchestrator's probe confirms ESC b → `ctrl+left`, so `alt+b` never reaches the app from a terminal) while the field is open (closed → nothing; the app's priority `tab` is held by check_action while the CaptureView is on the stack, and the Input keeps its value and focus): `self._field_lane` = the next lane index i in board order with `self.lanes[i][2] is not None`, wrapping after the last; repaint the key row
module: taskboard/app.py
modify: [Data: CaptureView._field] (replace)
examples: (TC-4521, root action_new) 3 readable boards, open board lane 0 → `tab` ×3 posted as `events.Key("tab", "\t")` → key row names lane 0 again, the field's value and focus kept; a fourth board with a missing file at lane 2 is skipped: lanes 0 → 1 → 3 → 0 (3/3)

CaptureView.on_input_submitted
req: LLR-4404.23, LLR-4404.25, LLR-4404.26, HLR-4404
in: Input.Submitted event
out: None
func: new: part = the first note Part of pad.text whose text == self._field; None → close the field, "No note under the cursor."; else lane = self.lanes[self._field_lane]; ok = `self._dump(part, lane[2].path, lane[0], None, event.value, quiet=False, project_name="")` (dump_note checks the name: blank and taken are G-S's refusals, shown verbatim, the field stays open); ok → hide the field, `self._field = None`, focus the pad
module: taskboard/app.py
examples: (TC-4523, root on_input_submitted) cursor in N3, `alt+n`, type "Contracts pilot", `enter` → Client A's board.json holds project "Contracts pilot" and a task whose project_id is its id; Board.save called `1` time (spy) (3/3)
examples: (TC-4525, root on_input_submitted) type "   ", `enter` → notification "A project needs a name."; `0` projects added; the field still open (3/3)
examples: (TC-4526, root on_input_submitted) type "eval HARNESS ", `enter` → notification holds "Client A already has a project named"; `0` projects added (2/2)
examples: (AT-4403, root on_input_submitted) pad N5: `alt+n` → field "New project for note 1", key row "↵ create on Client A + dump   ⇥ board   esc back"; `tab` → "↵ create on Course + dump   ⇥ board   esc back"; type "Contracts pilot", `enter` → Course's board.json holds project "Contracts pilot" (colour "lime", the first PROJECT_COLORS hue Course does not use) and the task "Answer the region chair" with that project_id, save_atomic called `1` time; the pad no longer holds N5; then a new note "Client call", `alt+n`, `tab`, type "contracts PILOT", `enter` → notification holds "Course already has a project named"; no second project

CaptureView.action_review
req: LLR-4406.1, LLR-4406.14
in:
out: None
func: new, `alt+a` (priority); field open → nothing; notes = [p.text for p in note_parts(pad.text) if p.is_note] (the pad as it is now, not the store); [] → notify("No notes to review.", title="Capture", severity="warning", timeout=10, markup=False); else `self.app.push_screen(ReviewList(self, notes))`
module: taskboard/app.py
examples: (TC-4561, root action_review) pad N1\n____\nN2\n____\nN3\n____\nN4 (N4 typed 0.2 s before) → `4` rows in pad order; app.screen is a ModalScreen (2/2)
examples: (TC-4574, root action_review) empty pad, `alt+a` → notification "No notes to review."; app.screen is the CaptureView (2/2)

CaptureView.action_image
req: LLR-4408.4, LLR-4408.5, LLR-4408.6, LLR-4408.7, LLR-4408.8, LLR-4407.29
in:
out: None
func: new, `alt+i` (priority); field open → nothing; part None → "No note under the cursor." and no file written; else res = `attach_images(app.inbox.images_dir, grab_clipboard_image())`; res.notice → notify(res.notice, warning) (G-S's texts); res.names → the note's last non-blank line index j in [part.start, part.end]; `pad.insert("".join("\nimg: " + n for n in res.names), (j, len(line j)))`; then `self._flush()` at once (LLR-4407.29)
module: taskboard/app.py
examples: (TC-4614, root action_image) note "T\nx", cursor on "T", 2 names ["paste-001.png", "shot.png"] → note "T\nx\nimg: paste-001.png\nimg: shot.png" (1/1); before a divider "T\nx\n____\nb" → "T\nx\nimg: paste-001.png\nimg: shot.png\n____\nb"
examples: (TC-4615, root action_image) grab → None → notification "No image found in the clipboard."; pad unchanged (1/1)
examples: (TC-4616, root action_image) grab → [a.txt, b.svg] → "Clipboard holds no image files."; `0` copies (2/2)
examples: (TC-4617, root action_image) a read-only S/inbox-images, grab → a 2x2 PIL image → notification starts "The image could not be saved: "; pad unchanged (2/2)
examples: (TC-4618, root action_image) empty pad, `alt+i` → "No note under the cursor."; `0` files in S/inbox-images (2/2)
examples: (TC-4609, root action_image) after `alt+i` → stored "pad" equals the pad text at once (2/3)
examples: (AT-4407, root action_image) pad "Vendor call\n::b:: ask the vendor :: @username_subject", taskboard.app.grab_clipboard_image patched to a 2x2 PIL image: `escape`, `n`, `alt+i` → pad "Vendor call\n::b:: ask the vendor :: @username_subject\nimg: paste-001.png", S/inbox-images/paste-001.png exists, the cells of "ask the vendor" carry `#60a5fa`; `alt+n`, type "Vendor desk", `enter` → the task "Vendor call" on Client A with notes "::b:: ask the vendor :: @username_subject" byte for byte and images [S/boards/client-a/images/<id>/paste-001.png]; then pad "[red]x[/red]" → rail row "▌1 [red]x[/red]" literal; `alt+n`, type "[b]P[/b]", `enter` → "Dumped → [b]P[/b] · Client A   ·   alt+u undo" literal (finding P-V-11 on the AT text)

CaptureView.action_undo
req: LLR-4405.1, LLR-4405.3, LLR-4405.7, LLR-4405.9, LLR-4405.10, LLR-4405.11, LLR-4405.14, LLR-4405.15, LLR-4405.16, LLR-4405.17, LLR-4407.29, LLR-4403.24, HLR-4405
in:
out: None
func: new, `alt+u` (priority; the review list's `u` calls it too); field open → nothing. `self._pending_drop` set → `self._flush()` first and stop when it fails. entry = `app.inbox.last_dump(datetime.now())` (G-S reads the file's `dumped` fresh, P-S-6 ruled); None → notify("Nothing to undo.", title="Capture", severity="warning", timeout=10, markup=False). `entry["board"]` not samefile with the file of a lane of `self.lanes` (`board_lanes`) → notify(f"{entry['board']} is not a known board — nothing undone.", warning), the entry kept, nothing else (P-S-4 ruled, LLR-4405.16). live = app.board when Path(entry["board"]).resolve() == Path(app.board.path).resolve() else None; out = `undo_dump(entry, live, app.inbox.images_dir)`; board = _where(entry["board"], entry["project"])[1]; state "changed" → notify(f"{entry['title']} changed since the dump — undo left it.", warning), nothing else; "failed" → notify(f"{board} could not be changed: {out.notice} — nothing undone.", warning), nothing else; "undone" / "gone" → new = with_note(pad.text, out.note_text); try `res = app.inbox.write_pad(strip_controls(new), drop=entry)` → pad.text = res.pad whenever it differs (P-S-8; cursor kept, clamped), `self._saved`/`self._text` = res.pad; OSError e → pad.text = new, `self._pending_drop = entry`, the save notice; "gone" → notify(f"{entry['title']} is no longer on {board}: the note is back in the pad.", warning); "undone" → notify(f"Undone: {entry['title']} left {board}; the note is back in the pad.", title="Capture", severity="information", timeout=10, markup=False) (P-V-12 ruled AMEND, LLR-4405.15); live: `app.refresh_view()`; `self._rebuild_docs()`. Never reads or writes `app._undo_stack` (R1-4)
module: taskboard/app.py
modify: [Data: inbox.json] (replace); [Data: CaptureView._saved] (replace)
examples: (TC-4541, root action_undo) dumps of N1 then N2; `alt+u` → N2's task gone from Course, N1's kept on Client A; `alt+u` → N1's gone (2/2)
examples: (TC-4543, root action_undo) pad "a" at the undo → pad "a\n____\n" + N2; empty pad → pad N2 (2/2, with_note applied)
examples: (TC-4547, root action_undo) empty "dumped", and one entry at "2026-10-24T10:01:00" (8 days old) → notification "Nothing to undo."; `0` changes (2/2)
examples: (TC-4549, root action_undo) N2's task deleted from Course after the dump → notification "Volume lab fails on WSL is no longer on Course: the note is back in the pad."; the pad ends with N2 (1/1)
examples: (TC-4550, root action_undo) N2's task retitled after the dump → "Volume lab fails on WSL changed since the dump — undo left it."; board, pad and inbox.json bytes unchanged (2/2)
examples: (TC-4551, root action_undo) a fresh foreign Course board.json.lock → notification starts "Course could not be changed: " and ends " — nothing undone."; pad and inbox.json unchanged (2/2)
examples: (TC-4554, root action_undo) len(app._undo_stack) equal before the dump, after it and after `alt+u` (3/3 with _dump's arms)
examples: (TC-4609, root action_undo) after `alt+u` → stored "pad" equals the pad text at once (3/3)
examples: (TC-4555, root action_undo) the AT-4402 dump, then `alt+u` → exactly `1` notification "Undone: Volume lab fails on WSL left Course; the note is back in the pad.", title "Capture", markup `False` (1/1)
examples: (TC-4556, root action_undo) the newest entry's "board" edited in inbox.json to "S/loose/board.json" (a board-shaped file in no lane) → notification "S/loose/board.json is not a known board — nothing undone."; the entry still in "dumped"; S/loose/board.json and both lane board files byte-unchanged (3/3)
examples: (TC-4557, root action_undo) dumps of N1 then N2; a second Inbox drops N2's entry from inbox.json (undone in another window); `alt+u` here → N1's task leaves Client A; N2's note not restored here (2/2 with G-S's memory arm)
examples: (AT-4404, root action_undo) fixture F, pad N1\n____\nN2: cursor in N2 `alt+d`, cursor in N1 `alt+d` (pad ""); `alt+u` → N1's task leaves Client A and the pad is N1 (empty pad: no divider); `alt+a`, `u` → N2's task leaves Course, the review shows 2 rows, pad "N1\n____\nN2"; `escape`, `alt+u` → "Nothing to undo."; an entry at "2026-10-24T10:01:00" added to inbox.json "dumped" by hand, then any pad write → it is gone from "dumped"

ReviewList.on_mount
req: LLR-4406.1, LLR-4406.3, LLR-4406.15, LLR-4407.32, HLR-4406
in:
out: None
func: new `ReviewList(ModalScreen[None])` built with (CaptureView view, list[str] texts); compose: `Vertical(#rv-box)` (border_title "Review · dump checked") holding `Static(id="rv-body")`; BINDINGS priority: escape→back, up→move(-1), down→move(1), space→toggle, o→other, d→dump, u→undo. on_mount: `self.styles.background = Color(13, 17, 23, 0.6)` (P-V-9), `self.sel = 0`, `self.on = [view.chosen(t) is not None and app.inbox.flag_for(t) is None for t in texts]`, paint = review_rows([ReviewRow(note_task(t).title, view.chosen(t), on[i], flag line)], sel, #rv-body content width (108 at 118x30, 72 at 80x24)). A ModalScreen, so typed letters never reach the pad; `x`, `a` bubble to the app and are held by check_action (CaptureView on the stack). Needs `"ReviewList": {}` in tests/test_modal_keys.py INVENTORY (finding P-V-5)
module: taskboard/app.py
examples: (TC-4563, root action_review) N1, N2, N3, N4 → rows 1, 2, 4 "[x]", row 3 "[ ]" (2/2)
examples: (TC-4575, root action_review) typing `x` and `a` in the review list → the pad text unchanged; Client A's task count unchanged (1/1)

ReviewList.action_move
req: LLR-4406.4
in: int delta
out: None
func: new: `self.sel = max(0, min(len(self.texts) - 1, self.sel + delta))`; repaint
module: taskboard/app.py
examples: (TC-4564, root action_review) `up` at row 0 → sel `0`; `down` ×9 on 4 rows → sel `3` (2/2)

ReviewList.action_toggle
req: LLR-4406.5, LLR-4406.6, LLR-4407.32
in:
out: None
func: new, `space`: t = texts[sel]; flagged → notify(f"This note is already on {board}; delete it from the pad.", warning), stays unchecked; view.chosen(t) None → stays unchecked, notify("Needs a name: alt+n in the pad.", title="Capture", severity="warning", timeout=10, markup=False); else `self.on[sel] = not self.on[sel]`; repaint (the key row's k follows)
module: taskboard/app.py
examples: (TC-4565, root action_review) row 1 "[x]" → `space` "[ ]" → `space` "[x]" (2/2)
examples: (TC-4566, root action_review) `space` on N3's row → stays "[ ]"; notification "Needs a name: alt+n in the pad." (2/2)
examples: (TC-4672, root action_review) a flagged note's row opens "[ ]"; `space` → stays "[ ]" with "This note is already on Course; delete it from the pad."

ReviewList.action_other
req: LLR-4406.7
in:
out: None
func: new, `o`: `view.choice[t] = view.choice.get(t, 0) + 1` for t = texts[sel] (the shared dict); the chosen option now None → `self.on[sel] = False`; repaint
module: taskboard/app.py
modify: [Data: CaptureView.choice] (replace)
examples: (TC-4567, root action_review) row 1 (N1) `o` → row 1 shows "Pilot rollout · Client A ▰▰▱"; `escape` → the rail's N1 `→` row shows "Pilot rollout · Client A ▰▰▱" (2/2)

ReviewList.action_dump
req: LLR-4406.8, LLR-4406.9, LLR-4406.10, LLR-4406.16, HLR-4406
in:
out: None
func: new, `d`: checked = [t for t, on in zip(texts, self.on) if on] (pad order); k = 0; for each t: part = the first note Part of view's current pad whose text == t (None → not dumped); `view.dump_part(part, quiet=True)` True → k += 1 (each failure shows its own notice and leaves its note in the pad); then notify(f"Dumped {k} of {len(checked)} checked", title="Capture", severity="information", timeout=10, markup=False) and `self.dismiss(None)`
module: taskboard/app.py
examples: (TC-4568, root action_review) 3 of 4 checked (N1, N2, N4) → 3 tasks on their boards; the pad holds N3 only (2/2)
examples: (TC-4569, root action_review) after `d` → app.screen is the CaptureView (1/1)
examples: (TC-4570, root action_review) Course's file deleted before `d` → N1 and N4 dumped, N2 in the pad, notifications "Course's file is missing — nothing dumped." and "Dumped 2 of 3 checked" (3/3)
examples: (TC-4576, root action_review) all 3 succeed → notification "Dumped 3 of 3 checked", markup `False` (1/1)
examples: (AT-4405, root action_review) fixture F, pad N1\n____\nN2\n____\nN3\n____\nN4: `escape`, `n`, `alt+a` → 4 rows, rows 1, 2, 4 "[x]"; `down` `down` `space` → row 3 stays "[ ]", "Needs a name: alt+n in the pad."; `up` `up` `o` → row 1 "Pilot rollout · Client A ▰▰▱"; `d` → Client A holds N1's task (project Pilot rollout) and N4's (Pilot rollout), Course holds N2's; "Dumped 3 of 3 checked"; app.screen is the CaptureView; pad == N3

ReviewList.action_undo
req: LLR-4406.11
in:
out: None
func: new, `u`: `view.action_undo()`; then texts = the notes of view's pad now; `self.on` = the old check for a text still present (first occurrence), else the opening rule; `self.sel` clamped; repaint
module: taskboard/app.py
examples: (TC-4571, root action_review) one dump of N2 earlier, review open on N1, `u` → a row for N2 appears as row 2 "[x]" (2/2)

ReviewList.action_back
req: LLR-4406.12
in:
out: None
func: new, `escape`: `self.dismiss(None)`; changes nothing
module: taskboard/app.py
examples: (TC-4572, root action_review) `escape` → app.screen is the CaptureView; boards and inbox.json unchanged (2/2)

## Entities

[Data: keymap.KEYMAP]
in: tuple[Key, ...]
desc: CHANGED: one entry `Key("n", "n", "capture", "Capture", group="misc", bar=False)` right after `N`; `capture` joins app.SEAT_ACTIONS automatically

[I/O: README key table]
desc: CHANGED: README.md main key table, one row `| \`n\` | Capture | …` after the `N` row (text in app_bindings); the home table's `n` row (New board) unchanged

[Data: TaskboardApp.inbox]
in: Inbox
desc: NEW: the one store of the app (graph-interfaces [Data: Inbox state]), loaded in TaskboardApp.__init__; plus `_inbox_said`, `_divider_said` session flags

[Data: App.screen_stack]
in: list[Screen]
desc: Textual's stack; CaptureView is a Screen (not modal); ReviewList a ModalScreen over it

[Data: CaptureView.docs]
in: list[Doc]
desc: NEW: corpus(lanes) at open and after every board-changing dump/undo, with `lanes`, `ids`, `unread`

[Data: CaptureView._hits]
in: dict[str, list[Hit]]
desc: NEW: the hit cache keyed by the note's exact text; cleared with every new docs (LLR-4403.21)

[Data: CaptureView.choice]
in: dict[str, int]
desc: NEW: the chosen option index per note text, read modulo len(options); shared with ReviewList (S-c)

[Data: CaptureView._saved]
in: str
desc: NEW: the pad text (control characters removed) as last read from or written to the store; `_unsaved()` compares it with the pad

[Data: CaptureView._text]
in: str
desc: NEW: the pad text as of the last TextArea.Changed; what on_unmount writes (P-V-4)

[Data: CaptureView._field]
in: str?
desc: NEW: the note text the name field targets (None = closed), with `_field_lane` (index into lanes)

[Data: CaptureView._esc_armed]
in: bool
desc: NEW: True after the "esc again closes without saving" warning until the text or the cursor changes

[Data: RailNote]
in: NamedTuple(str title, int images, list[Hit?] options, Hit? chosen, list[Hit] hits, str? flag)
desc: NEW, app.py: one note as the rail paints it; `flag` is "on <board> — delete it here" for a flagged note (P-V-8 ruled AMEND; the rail draws "⚑ " before it)

[Data: ReviewRow]
in: NamedTuple(str title, Hit? option, bool checked, str? flag)
desc: NEW, app.py: one review row

[Data: app.GHOST]
in: str
desc: NEW: "first line → the task's title\nnext lines → its notes\n" + "─" * 24 + "\n____ ↵ starts the next note"

[Data: app.CAPTURE_KEYS]
in: list[tuple[str, str]]
desc: NEW: [("alt+d", "dump"), ("alt+o", "other"), ("alt+n", "new project"), ("alt+a", "review"), ("alt+i", "image"), ("alt+u", "undo"), ("esc", "close")]

[Data: Inbox state]
desc: G-S (graph-interfaces): read through `pad`, `dumped`, `flagged`, `divider_notice`, `load_report`, `images_dir`; changed only through write_pad, flag, mark_notice

[Data: inbox.json]
desc: G-S (graph-interfaces): written by Inbox.write_pad / Inbox.mark_notice only

[Data: DumpOutcome]
desc: G-S (graph-interfaces): ok, task, project_id, project_name, new_project, images, missing, notice

[Data: UndoOutcome]
desc: G-S (graph-interfaces): state, note_text, notice

[Data: Hit]
desc: G-T (graph-interfaces): doc, score, why

[Interface: capture view]
desc: the `n` screen: head row, pad, hint row, rail, key row; bindings all priority (P-V-3)
offers: (TC-4402) "n" → TaskboardApp.action_capture
offers: (TC-4501) "alt+d dump" → CaptureView.action_dump
offers: (TC-4516) "alt+o other" → CaptureView.action_other
offers: (TC-4519) "alt+n new project" → CaptureView.action_new
offers: (TC-4561) "alt+a review" → CaptureView.action_review
offers: (TC-4614) "alt+i image" → CaptureView.action_image
offers: (TC-4541) "alt+u undo" → CaptureView.action_undo
offers: (TC-4439) "alt+l divider" → CaptureView.action_divider
offers: (TC-4404) "esc close" → CaptureView.action_close

[Interface: name field]
desc: the Input under the rail while open; key row "↵ create on <board> + dump   ⇥ board   esc back" (P-V-1 ruled)
offers: (TC-4523) "↵ create on Client A + dump" → CaptureView.on_input_submitted
offers: (TC-4521) "⇥ board" → CaptureView.action_board
offers: (TC-4527) "esc back" → CaptureView.action_close

[Interface: review list]
desc: the modal of variant C; key row "↑↓ move   ␣ include   o other   d dump <k> checked   u undo   esc back"
offers: (TC-4564) "↑↓ move" → ReviewList.action_move
offers: (TC-4565) "␣ include" → ReviewList.action_toggle
offers: (TC-4567) "o other" → ReviewList.action_other
offers: (TC-4568) "d dump 3 checked" → ReviewList.action_dump
offers: (TC-4571) "u undo" → ReviewList.action_undo
offers: (TC-4572) "esc back" → ReviewList.action_back

[Outside: key n]
desc: CHANGED: bound on the app (non-priority) to `capture`; the home, the people directory and the marks manager keep their own `n`; typed into the pad and the name field

[Outside: key tab]
desc: the name field's board cycle (P-V-1 ruled: `alt+b` replaced, since ESC b arrives as `ctrl+left` in Textual 8.2.8, P-V-3); a CaptureView priority binding, acting only while the field is open

## Edges

[Data: keymap.KEYMAP] ──▶ app_bindings
app_bindings ──▶ [I/O: README key table]
[Outside: key n] ──▶ TaskboardApp.check_action
when: no ModalScreen on the stack; then TaskboardApp.action_capture runs
[Outside: key n] ──▶ PadArea.get_line
when: the pad has focus (typed, no binding: the TextArea consumes it)
[Outside: key tab] ──▶ CaptureView.action_board
when: the name field is open
TaskboardApp.__init__ ──▶ [Data: TaskboardApp.inbox]
TaskboardApp.action_capture ──▶ [Data: App.screen_stack]
[Data: App.screen_stack] ──▶ TaskboardApp.check_action
[Data: TaskboardApp.inbox] ──▶ CaptureView.compose
[Data: Inbox state] ──▶ CaptureView._paint
[Data: Inbox state] ──▶ CaptureView.dump_part
[Data: Inbox state] ──▶ CaptureView.action_undo
CaptureView.compose ──▶ [Data: CaptureView.docs]
CaptureView._rebuild_docs ──▶ [Data: CaptureView.docs]
CaptureView._rebuild_docs ──▶ [Data: CaptureView._hits]
[Data: CaptureView.docs] ──▶ CaptureView.options_for
CaptureView.options_for ──▶ [Data: CaptureView._hits]
[Data: CaptureView._hits] ──▶ CaptureView.options_for
[Data: CaptureView.choice] ──▶ CaptureView.options_for
CaptureView.action_other ──▶ [Data: CaptureView.choice]
ReviewList.action_other ──▶ [Data: CaptureView.choice]
[Data: Hit] ──▶ hit_text
hit_text ──▶ rail_rows
hit_text ──▶ review_rows
[Data: RailNote] ──▶ rail_rows
[Data: ReviewRow] ──▶ review_rows
[Data: app.CAPTURE_KEYS] ──▶ CaptureView._paint
[Data: app.GHOST] ──▶ PadArea.__init__
capture_head ──▶ CaptureView._paint
rail_rows ──▶ CaptureView._paint
capture_hint ──▶ CaptureView.compose
CaptureView.on_text_area_changed ──▶ [Data: CaptureView._text]
[Data: CaptureView._text] ──▶ CaptureView.on_unmount
[Data: CaptureView._saved] ──▶ CaptureView._flush
CaptureView._flush ──▶ [Data: CaptureView._saved]
CaptureView._flush ──▶ [Data: inbox.json]
CaptureView._dump ──▶ [Data: inbox.json]
CaptureView._dump ──▶ [Data: Inbox state]
CaptureView.action_undo ──▶ [Data: inbox.json]
CaptureView.on_unmount ──▶ [Data: inbox.json]
CaptureView._notice_divider ──▶ [Data: inbox.json]
[Data: DumpOutcome] ──▶ CaptureView._dump
[Data: UndoOutcome] ──▶ CaptureView.action_undo
CaptureView.action_new ──▶ [Data: CaptureView._field]
CaptureView.action_board ──▶ [Data: CaptureView._field]
[Data: CaptureView._field] ──▶ CaptureView.on_input_submitted
CaptureView.action_close ──▶ [Data: CaptureView._esc_armed]
[Data: CaptureView._esc_armed] ──▶ CaptureView.action_close
CaptureView.action_close ──▶ [Data: App.screen_stack]
CaptureView.action_review ──▶ [Data: App.screen_stack]
review_rows ──▶ ReviewList.on_mount

## Findings

finding P-V-1 MAJOR: `alt+b` (the name field's board cycle) cannot reach the app in a real terminal
anchor: CaptureView.action_board
seen: (P-V-3) Textual 8.2.8's ANSI table maps ESC b to `ctrl+left` (and ESC f to `ctrl+right`); the parser gives Key("ctrl+left", None) for ESC b, so a binding on `alt+b` fires only in a pilot (Key("alt+b")) or a kitty-protocol terminal, which Windows Terminal is not (modals.py:63-66). TC-4521 would pass in the pilot and the key would never work for the operator
cause: LLR-4404.21 / LLR-4404.22 copy the prototype's `alt+b`; R1-1 fixed the same class of defect for `alt+enter` only
effect: a shown key that never works (keymap law, R1-1's own reason); the dump target stays the open board, so dumping into a new project on another board is impossible from a real terminal
decision: ruled — ACCEPT (MAJOR, round 0b; the orchestrator's probe confirms `ESC b` → `ctrl+left`, `ESC a/d/i/l/n/o/u` → `alt+<letter>`): the name field's board cycle is `tab`, shown `⇥ board`; LLR-4404.21 / LLR-4404.22 and AT-4403 reworded. Applied: CaptureView.compose, CaptureView._paint, CaptureView.action_board, CaptureView.on_input_submitted, [Interface: name field], [Outside: key tab]

finding P-V-2 every pad key must be a PRIORITY binding, or the terminal types its letter
anchor: CaptureView.compose
seen: (P-V-3) ESC d arrives as Key("alt+d", "d"), printable; with a non-priority binding the focused TextArea inserts "d" (pad "abc" → "abcdlb" for alt+d/alt+l/alt+b) and the focused Input inserts "d"; the pilot's Key("alt+d", None) reaches the binding either way, so pilot tests cannot see the defect
cause: TextArea._on_key inserts any printable key before the screen's non-priority bindings
effect: none if the bindings are priority (as graph-interfaces says); a later "cleanup" to non-priority would pass every pilot test and break the real terminal
decision: ruled — ACCEPT (round 0b): every CaptureView pad key is a priority binding; a test posts the terminal form and asserts the pad text unchanged — new LLR-4401.18 (TC-4418, posted with `alt+o` / `alt+u` so the action itself leaves the pad as it was). Applied: CaptureView.compose

finding P-V-3 the rule's colour must be a span, not the Text's base style
anchor: PadArea.get_line
seen: (P-V-1b) `Text("─" * w, style=HEX["dim"])` renders `#e0e0e0`; `t.stylize(HEX["dim"])` renders `#5b6675`
cause: TextArea._render_line rebuilds the line's segments from spans; the Text-level style is not carried
effect: a rule in the default ink, as bright as text
decision: ruled — ACCEPT (round 0b). As designed in PadArea.get_line; no change

finding P-V-4 TC-4413's negative control cannot fail: `n` is already documented in the README
anchor: app_bindings
seen: README.md home table line 326 "| `n` | New board …"; test_the_readme_keybinding_table_matches_the_seat collects every backticked key of the first cell of every "| `" line, so `n` is "documented" without the new row
cause: the existing law checks key spelling only, not the row's meaning or table
effect: LLR-4401.13's NC ("no README row: that test RED") stays GREEN — a vacuous check
decision: ruled — ACCEPT (round 0b): TC-4413 asserts the README row `| \`n\` | Capture |`; LLR-4401.13's threshold reworded. Applied: app_bindings TC-4413 example (unchanged)

finding P-V-5 a new ModalScreen in app.py breaks TC-2407 unless the inventory grows
anchor: ReviewList.on_mount
seen: tests/test_modal_keys.py::test_TC_2407_every_modal_is_in_the_inventory walks every ModalScreen class of modals and app and requires it in INVENTORY
cause: ReviewList is a ModalScreen defined in app.py
effect: a guard test RED at E4 if forgotten
decision: ruled — ACCEPT (round 0b): the tester adds `"ReviewList": {}` to `tests/test_modal_keys.py` INVENTORY (E4 test edit); no node change

finding P-V-6 no notice text for an unreadable store that could not be copied aside
anchor: CaptureView.on_mount
seen: LLR-4407.8 words "it was copied to <backup name>"; Inbox.load reports backup None when keep_aside fails (LLR-4407.9)
cause: the requirement covers the copy that succeeded only
effect: the implementer would print "copied to None"
decision: ruled — ACCEPT the wording (round 0b): new LLR-4407.38 (TC-4678); LLR-4407.8 covers the copied case. Applied: CaptureView.on_mount

finding P-V-7 the narrow rail has no rule when the cursor is in no note
anchor: rail_rows
seen: LLR-4401.8 "showing the cursor's note only"; the cursor can sit in the empty part after a divider or on a blank pad line while other notes exist
cause: gap in LLR-4401.8
effect: a blank or arbitrary narrow rail
decision: ruled — ACCEPT (round 0b): new LLR-4401.17 (TC-4417). Applied: rail_rows

finding P-V-8 flagged and dumped entries carry ids only, and the flag line overflows the wide rail
anchor: CaptureView._where
seen: FlaggedEntry / DumpedEntry hold `board` (path) and `project` (id) but no names; LLR-4407.31's line "⚑ already dumped → Module 4 · Volumes · Course — delete it here" is 60 cells with its 3-cell indent, the wide rail is 48 (P-V-5)
cause: the entry schema (LLR-4407.33) and the rail width were set apart
effect: names must be resolved by G-V; the line is cut ("…") in the wide rail, so "delete it here" is lost for long names
decision: ruled — AMEND (round 0b): names resolved as proposed (_where); the wide-rail flag line is shortened to `⚑ on <board> — delete it here` (the same text in the narrow rail and the review row, one string); the LLR-4407.30 notice keeps the full sentence; LLR-4407.31 reworded. Applied: rail_rows, review_rows, [Data: RailNote], CaptureView._where

finding P-V-9 TC-4634's notice arm cannot see a note title: the dump notice holds none
anchor: CaptureView._dump
seen: LLR-4409.4 threshold "note title [red]x[/red] … literal in the rail row, the review row and the dump notice"; the notice of LLR-4404.7 is "Dumped → <project> · <board> …"
cause: the threshold assumed the title is in the notice
effect: the arm is vacuous for a title
decision: ruled — ACCEPT (round 0b): LLR-4409.4's threshold and AT-4407 reworded to the markup project name. Applied: CaptureView._dump TC-4634 example (unchanged)

finding P-V-10 `alt+n` on a flagged note would dump it a second time
anchor: CaptureView.action_new
seen: LLR-4407.32 refuses `alt+d` and the review `d` on a flagged note; `alt+n` + enter creates a project and dumps the same note again (a duplicate task)
cause: gap in LLR-4407.32
effect: the duplicate R2 F-12 wanted to prevent
decision: ruled — ACCEPT (round 0b): LLR-4407.32 names `alt+n`; TC-4672 gains the arm. Applied: CaptureView.action_new

finding P-V-11 AT-4407's note has no notes line
anchor: CaptureView.action_image
seen: AT-4407 note `::b:: ask the vendor :: @username_subject` is one line, so it is the title line (LLR-4404.2: visible text "ask the vendor @username_subject") and the task notes are "" — "the task notes keep the span and mention verbatim" cannot hold
cause: AT text
effect: the AT fails as written
decision: ruled — ACCEPT (round 0b): AT-4407's note is `Vendor call\n::b:: ask the vendor :: @username_subject` (requirements amended). Applied: CaptureView.action_image AT-4407 example (unchanged)

finding P-V-12 a successful undo shows no notice
anchor: CaptureView.action_undo
seen: LLR-4405.1..4405.11 word notices for nothing-to-undo, gone, changed and failed only; a cross-board undo removes a task the user cannot see from the pad
cause: gap (F-13: strings are E1 proposals)
effect: the only feedback is the note coming back at the pad's end
decision: ruled — AMEND (round 0b): a successful undo shows `Undone: <title> left <board>; the note is back in the pad.` — new LLR-4405.15 (TC-4555). Applied: CaptureView.action_undo

finding P-V-13 who words the dump refusals
anchor: CaptureView._dump
seen: graph-interfaces preamble "G-V owns … every notice text"; DumpOutcome.notice "holds the refusal text" and dump_note's examples carry the texts ("Course's file is missing — nothing dumped.")
cause: two statements of ownership
effect: the same string could be written twice or differ
decision: ruled — ACCEPT (round 0b): G-S words the dump_note / attach refusals; G-V shows `notice` verbatim and owns every other text; DumpOutcome.images = the moved file names (graph-interfaces amended), recorded through `entry_for` (P-S-15). Applied: CaptureView._dump

finding P-V-14 a failed store write after a successful undo needs a pending drop
anchor: CaptureView.action_undo
seen: undo_dump removes the task from its board, then write_pad(drop=entry) may fail; the entry stays in the file's `dumped`, so a later `alt+u` would find the task gone and restore the note a second time
cause: the board-then-store pair is not atomic (R2 F-12) and Inbox.write_pad takes one `drop`
effect: a duplicated note in the pad
decision: ruled — ACCEPT (round 0b), as designed; no change

### Seams

> Calls G-V makes into G-S (`taskboard/inbox.py`): `INBOX_NAME`; `Inbox.load(path)` (TaskboardApp.__init__); `inbox.refresh()` (CaptureView.compose); `inbox.pad`, `.dumped`, `.flagged`, `.divider_notice`, `.load_report`, `.images_dir` (read only); `inbox.write_pad(pad, record=, drop=)` → WriteResult (or OSError) (_flush, _dump, action_undo, on_unmount); `inbox.flag(entry)` (_dump on OSError); `inbox.flag_for(text)` (_paint, dump_part, action_new, ReviewList); `inbox.last_dump(now)` (action_undo); `inbox.mark_notice()` (_notice_divider); `is_divider`, `note_parts`, `note_count`, `note_at`, `note_task`, `without_note`, `with_note`, `prune_dumped` (the dumped count of the rail); `DumpTarget(path, name, live)`; `dump_note(target, project_id, new_name, note, folder, project_name)` → DumpOutcome (P-S-1); `entry_for(outcome, note, board_path, now)` → DumpedEntry (P-S-15); `undo_dump(entry, live, folder)` → UndoOutcome; `attach_images(folder, grabbed)` → AttachResult.
> Calls G-V makes into G-T (`taskboard/suggest.py`): `corpus(lanes, app.marks.marks)` (lanes = board_lanes(app)[0]); `suggest(nt.title + "\n" + nt.notes, docs)` → [Hit] with nt = `note_task(part.text)` (P-T-4; through the module attribute `taskboard.app.suggest`); `options(hits)` → [Hit?]; `bars(score)`. Reads `Hit.doc.project_name`, `.project_colour`, `.board_name`, `.board_colour`, `.board_path`, `.project_id`, `Hit.score`, `Hit.why`.
> Calls into G-V from other groups: none (G-S and G-T import nothing from app.py). The orchestrator's checks: TaskboardApp.check_action's two tuples (R1-6) and the README row (LLR-4401.13).
> Seam changes ruled in round 0b and applied in graph-interfaces: P-V-1 (`alt+b` → `tab`), P-V-13 (DumpOutcome.images = names; refusal-text ownership), P-S-1, P-S-8, P-S-15, P-T-4.

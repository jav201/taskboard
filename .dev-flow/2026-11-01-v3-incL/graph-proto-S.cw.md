# Code-Wire prototype — group S: the list screen, its key gate and the template stamp (Inc L, E2b)

Differences from `graph-baseline.cw.md` only, for `taskboard/app.py`. New nodes are the methods of the `AddedList` screen; changed nodes say `changed from baseline:`; four creation-adjacent nodes are written as `unchanged from baseline:` because Inc L relies on them staying as they are (each with the example that pins it). The shared seams `AddedList` (the class), `TaskboardApp.action_added_list`, `[Interface: AddedList keys]`, `stamp`, `Board.add_task`, `added_rows`, `added_order`, `first_created` and `render_added_list` are defined in `graph-interfaces.cw.md` and are NOT repeated here; proposed changes to them are findings below.

Textual 8.2.8 facts this design relies on (read in `textual/app.py:3966-3988`, `textual/app.py:4223-4248`, `textual/screen.py:408-455`, executed in probe S-1): a key is first offered to PRIORITY bindings walking `reversed(screen._binding_chain)`, i.e. the App first, then the screen, then the focused widget; then to non-priority bindings walking `screen._modal_binding_chain` from the focused widget up, a chain that STOPS at the first modal node, so under any `ModalScreen` the App's non-priority bindings (all of KEYMAP but `tab` and the four arrows/`hjkl`) are never offered. `run_action` returns False when the target's `check_action` returns False, and the walk then goes on to the next binding. Consequences on the list screen (a plain `Screen`, no focusable widget, so its chain is `[AddedList, App]`): the App's priority `cursor`/`hmove`/`toggle_presentation` bindings are offered first and refused by `check_action`, so the screen's own priority `up,k`/`down,j` act; every other screen key (`escape,N`, `o`, `v`, `enter`) has no App priority twin, so the screen's priority binding takes it before the App's non-priority `N` (`added_list`), `o` (`open_url`), `v` (`toggle_archived`), `enter` (`details`) or `escape` (`focus_exit`) are ever asked.

Probe S-1 (executed, `taskboard.__file__` = `…\taskboard-wt\capture-proto\taskboard\__init__.py`, synthetic one-board app, `Path.home` redirected to a temp folder; scratch script outside the repo): with a `ConfirmModal` pushed, `A` leaves the stack `['Screen', 'ConfirmModal']` both with the real `check_action` and with `check_action` forced to allow `agenda_all`; with the task editor open, `A` types into the title (`'A'`) and the stack stays `['Screen', 'TaskModal']` in both runs. So the modal gate of `agenda_all` (and of `added_list`) is never reached by a key press (finding P-S-1). Probe S-2 (executed): `key_line(ADDED_KEYS)` gives "↑↓ move   ↵ open on board   o newest/oldest   v archived   esc / N back", cell_len `71`; at width 60 "↑↓ move   ↵ open on board   o newest/oldest   v   esc / N"; at width 30 "↑↓ move   ↵   o   v   esc / N". Probe S-3 (E3 round 1, executed on the real `keymap.key_line`, scratch `%TEMP%/incL-e3/probe.py`): `key_line(ADDED_KEYS + [("·", "read-only: nothing here edits a task")])` is `112` cells ("… esc / N back   · read-only: nothing here edits a task"), so the tail fits a 116-cell key row (118x30) and is dropped at 78 (80x24), leaving the 71-cell line of the 5 keys (A-2).

**Evidence state of this file's node examples (ARCH-4): `planned`.** Only probes S-1, S-2 and S-3 above were executed; none of the pilot examples on the nodes below (TC-43nn, AT-430n) was run before E4. The E4 tester's RED-on-base run is their first execution, and the tester runs every one of them.

### Test fixture of this group (synthetic; `tests/added_list_fixture.py`, built like `backlog_round_fixture.build`)
> Home: `Path.home` redirected to `tmp_path` (the `home` fixture of `tests/test_all_agenda.py`); registry `<tmp>/.taskboard/boards.json`, `"last": "alpha"`, two active entries in this order: `alpha` "Alpha" (colour sky, `boards/alpha/board.json`) and `beta` "Beta" (colour lime, `boards/beta/board.json`), each board in its own folder (one history.jsonl per folder). App: `open_app(None)`; with two active boards it starts on BoardsHome, so every sequence below starts with `escape` (the main screen on Alpha, the board started) and every byte hash is taken AFTER that `escape` (finding P-S-4).
> Clock: `date` → 2026-11-01 in app, models, views, modals (`_Today`); `models.datetime.now()` → 2026-11-01T08:10:00 (the clock `stamp()` reads; TC-4303 uses the advancing clock of finding P-S-2).
> Alpha, phases Backlog Doing Review Done, project `pa` "Ops": `ta1` "Sync notes" Doing, created "2026-10-31T18:20:00"; `ta2` "Pilot store list" Backlog, no created key; `ta3` "Old invoice" Review, no created key. Alpha history.jsonl: one line `{"task": "ta2", "from": null, "to": "Backlog", "at": "2026-10-28T10:30:00"}`.
> Beta, phases Todo Doing Done, project `pb` "Home": `tb1` "Pay the rent" Todo, created "2026-11-01T07:55:00"; `tb2` "Archive scans" Done, no created key. Beta history.jsonl: one line `{"task": "tb2", "from": "Doing", "to": "Done", "at": "2026-10-29T12:00:00"}` (a move, not a birth). Option `with_archived`: Beta also holds `tb3` "Old receipts" Done, archived `true`, created "2026-10-30T09:00:00". Option `archived_on_alpha` (TC-4344 only, the open board): Alpha also holds `ta4` "Old memo" Review, archived `true`, created "2026-10-30T09:00:00".
> Derived (group V's nodes): sources tb1 c, ta1 c, ta2 h, tb2 ?, ta3 ?; first created date "Oct 31" (with `with_archived`: "Oct 30", archived included). Newest first: tb1, ta1, ta2, tb2, ta3 under TODAY · YESTERDAY · WED OCT 28 ≈ · BEFORE OCT 31 · ?; labels "07:55", "18:20", "≈10:30", "?", "?". Oldest first: ta3, tb2, ta2, ta1, tb1. Detail-pane source lines: tb1 "added Sun Nov 01 · 07:55 · the created field"; ta1 "added Sat Oct 31 · 18:20 · the created field"; ta2 "added ≈ Wed Oct 28 · 10:30 · from history.jsonl"; tb2 "added: unknown, before Oct 31 · #2 in Beta's board file"; ta3 "added: unknown, before Oct 31 · #3 in Alpha's board file".

### Acceptance sequences (black box; the example lines below carry each one on its node)
> AT-4301: `escape`; sha256 of the 4 files; `N` → stack [Screen, AddedList]; 5 rows with titles in order "Pay the rent", "Sync notes", "Pilot store list", "Archive scans", "Old invoice"; day headers in order "TODAY", "YESTERDAY", "WED OCT 28 ≈", "BEFORE OCT 31 · ?"; the head holds "newest first"; state boxes "■□□", "■■□□", "■□□□", "■■■", "■■■□"; cursor row 0, pane line 1 "Pay the rent". `o` → head "oldest first", row 0 "Old invoice", cursor 0, pane line 1 "Old invoice". `down` → cursor 1, pane line 1 "Archive scans". `escape` → stack [Screen], board_id "alpha", selected_task_id as before `N`; the 4 hashes equal.
> AT-4302: `escape`; `a`, type "Call the bank", `alt+s` → Alpha's file holds the new task with "created": "2026-11-01T08:10:00"; the `json.dumps(entry, indent=2)` slices of ta1, ta2, ta3 equal those before `a`. `N` → row 0 "Call the bank", label "08:10", under "TODAY", cursor 0, pane source "added Sun Nov 01 · 08:10 · the created field"; row 1 "Pay the rent".
> AT-4303: `escape` (ta1 selected, project pa); `I`, `down`, `enter` (preset "Simple chain") → Alpha gains "Plan", "Build", "Ship", each created "2026-11-01T08:10:00"; Alpha history.jsonl still `1` line. `N` → rows 0–2 "Ship", "Build", "Plan" (one moment, tie broken by file position, newest first is the exact reverse), labels "08:10" ×3 under "TODAY"; row 3 "Pay the rent".
> AT-4304 (`with_archived`): `escape`; `N` → 5 rows, no "Old receipts", the head ends "· 1 archived hidden". `v` → 6 rows, row 2 "Old receipts" under "FRI OCT 30" with its title in HEX["dim"], the head ends "· archived shown", cursor still row 0 "Pay the rent". `v` → 5 rows, the head ends "· 1 archived hidden", cursor row 0.
> AT-4305: `escape`; sha256 of the 4 files; `N`; `down` → label "18:20", pane source "added Sat Oct 31 · 18:20 · the created field"; `down` → label "≈10:30", source "added ≈ Wed Oct 28 · 10:30 · from history.jsonl"; `down`, `down` → label "?", source "added: unknown, before Oct 31 · #3 in Alpha's board file"; `escape` → the 4 hashes equal; Alpha's entries for ta2 and ta3 hold no "created" key.

## Nodes

AddedList.__init__
req: LLR-4304.6, LLR-4306.2, HLR-4303
in:
out: None
func: NEW. `super().__init__()` (no constructor argument: `_bring(AddedList, AddedList)` calls `AddedList()`; the screen reads `self.app`, see finding P-S-7). View state: `self.sel = 0`, `self.newest = True` (opens newest first, LLR-4304.6), `self.show_archived = False` (a constant start value, never read from `app.show_archived`, LLR-4306.2). Snapshot slots, filled by compose: `self.lanes = []`, `self.ids = []`, `self.rows = []`, `self.first = None`, `self.today = None`
module: taskboard/app.py
modify: [Data: AddedList.view] (replace); [Data: AddedList.snapshot] (replace)
examples: (TC-4392, root action_added_list) `app.show_archived = True` on the main screen (fixture `with_archived`), `escape` already pressed, `N` → screen show_archived `False`; `5` rows; no row titled "Old receipts"; the head ends "· 1 archived hidden"
examples: (TC-4366, root action_added_list) `escape`, `N` → newest `True`, sel `0`, row 0 is "Pay the rent" (tb1, the newest stamped task; created "2026-11-01T07:55:00")

AddedList.compose
req: LLR-4303.2, LLR-4303.3, LLR-4303.5, LLR-4302.6, HLR-4303
in:
out: ComposeResult widgets
func: NEW, the AllBoardsAgenda pattern (app.py:887). Runs ONCE per instance: Textual composes a screen at its first push, and `_bring` returning to an instance on the stack does not compose it again, so the boards are read once when the view opens (LLR-4303.5). Steps: `self.lanes, self.ids = board_lanes(self.app)`; `self.today = date.today()`; `self.rows = added_rows(self.lanes)`; `self.first = first_created(self.rows)` (the unfiltered rows, archived included); yield `Static(id="al-body")` then `Static(id="al-keys")`. Class attribute `DEFAULT_CSS = "AddedList { background: #0d1117; overflow-y: hidden; }  #al-body { padding: 0 1; height: 1fr; }  #al-keys { dock: bottom; height: 1; padding: 0 1; background: #0b0f17; }"` (the agenda's values). Reads only: `board_lanes` gives the open board as held and `peek_board` for the others (never the seed, never a `.corrupt` copy), `added_rows` reads history.jsonl; nothing here calls `save`, `save_atomic`, `history.append` or sets `task.created` (LLR-4302.6). LLR-4302.6's subject is the list view, i.e. these code paths (ARCH-6): the App's timers keep running under any screen (`_team_sync_tick` in team mode, app.py:1729, :1738; the presence renewal in `_tick`, app.py:1813–1815) and are not the list's writes; TC-4317's fixture has no team mode. No try/except: `board_lanes` maps a missing/unreadable file to a None lane and `added_rows` is total (OSError, ValueError or RecursionError from a history read → no births, SEC-2; a non-str task id → no birth lookup, SEC-3)
module: taskboard/app.py
modify: [Data: AddedList.snapshot] (replace)
examples: (TC-4322, root action_added_list) fixture, `escape`, `N` → app.screen is an AddedList; app.screen_stack types ["Screen", "AddedList"]
examples: (TC-4325, root action_added_list) fixture (3 + 2 tasks), `escape`, `N` → rows `5`; lanes names ["Alpha", "Beta"]; ids ["alpha", "beta"] (NC only `app.board`: `3` rows, RED)
examples: (TC-4323, root action_added_list) `escape`, `N`, `A`, `N` → compose ran `1` time; exactly `1` AddedList in app.screen_stack and it is app.screen; stack types ["Screen", "AddedList"]
examples: (TC-4317, root action_added_list) `escape`; sha256 of boards/alpha/board.json, boards/beta/board.json, boards/alpha/history.jsonl, boards/beta/history.jsonl; `N`, `down`, `down`, `o`, `v`, `v`, `escape` → the 4 hashes equal (4/4) (NC a `save()` in compose: Alpha's hash differs, RED)
examples: (AT-4301, root action_added_list) the AT-4301 sequence above: `N` → 5 rows "Pay the rent", "Sync notes", "Pilot store list", "Archive scans", "Old invoice"; headers "TODAY", "YESTERDAY", "WED OCT 28 ≈", "BEFORE OCT 31 · ?"

AddedList.on_mount
req: HLR-4303
in:
out: None
func: NEW. `self._paint()` (the first paint, after compose has filled the snapshot)
module: taskboard/app.py
examples: (TC-4322, root action_added_list) `escape`, `N` → `#al-body` line 1 holds "newest first" and `#al-keys` starts "↑↓ move   ↵ open on board   o newest/oldest   v archived   esc / N back" (the read-only tail follows only at a width where it fits whole, A-2)

AddedList.on_screen_resume
req: LLR-4303.11, HLR-4303
in:
out: None
func: NEW (addendum A-1, ARCH-5). `self._paint()`: when the list is back on top (`escape` from the agenda, the people directory or the marks manager, or `N` through `_bring`), it repaints at once, so a person or mark class renamed under `@` / `#` (`_refresh_directories`, app.py:1418) shows without waiting for the next key. The snapshot is NOT re-read (LLR-4303.5): only `_paint`, which reads the live `app.people.people` and the lane boards' `marks`
module: taskboard/app.py
examples: (TC-4331b, root action_added_list) fixture plus a people file with `ana` "Ana Ruiz" and ta1's notes "ping @ana"; `escape`, `N`, `down` (sel `1`, "Sync notes": pane meta holds "@Ana Ruiz"); `@`; the directory renames `ana` to "Ana Ortiz" (`app.people` re-read as `_refresh_directories` does); `escape` → stack ["Screen", "AddedList"] and, with no further key, the pane meta holds "@Ana Ortiz" (NC no `on_screen_resume`: still "@Ana Ruiz", RED)

AddedList.on_resize
req: HLR-4303
in: events.Resize _event
out: None
func: NEW. `self._paint()` (the widths of render_added_list follow the terminal: lw 46 from a 100-cell body, else 34)
module: taskboard/app.py
examples: (TC-4327, root harness) `N` at 118x30, then `pilot.resize_terminal(80, 24)` → every list|pane line of `#al-body` has "│" at cell index `35` (before the resize: `47`)

AddedList._ordered
req: LLR-4304.6, LLR-4304.7, LLR-4306.3
in:
out: list[AddedRow] rows
func: NEW. `added_order(self.rows, self.newest, self.show_archived)`: the rows as shown, in display order, archived ones dropped unless shown. The one place the screen derives display order; `_paint`, `action_move`, `action_archived` and `action_jump` all index THIS list with `self.sel`, so the cursor and the drawn row can never disagree
module: taskboard/app.py
examples: (TC-4367, root action_order) fixture rows, newest `False`, show_archived `False` → titles ["Old invoice", "Archive scans", "Pilot store list", "Sync notes", "Pay the rent"]
examples: (TC-4393, root action_archived) fixture `with_archived`, newest `True`, show_archived `True` → titles ["Pay the rent", "Sync notes", "Old receipts", "Pilot store list", "Archive scans", "Old invoice"]

AddedList._paint
req: LLR-4303.19, LLR-4303.6, LLR-4304.6, LLR-4302.6, HLR-4303
in:
out: None
func: NEW. `w, h = self.app.size`; `rows = self._ordered()`; `hidden = 0 if self.show_archived else sum(1 for r in self.rows if r.task.archived)`; `unread = sum(1 for lane in self.lanes if lane[2] is None)`; `#al-body` ← `render_added_list(rows, self.sel, self.newest, self.show_archived, hidden, unread, self.first, self.today, self.app.people.people, w - 2, h - 1)` (a Text of plain pieces; `Static.update` of a Text parses no markup); `#al-keys` ← `keys = key_line(ADDED_KEYS + [("·", "read-only: nothing here edits a task")])`; `if keys.cell_len > w - 2: keys = key_line(ADDED_KEYS, w - 2)` — AllBoardsAgenda._paint's rule (app.py:936–938): the read-only tail goes first, never a key (addendum A-2, ARCH-9). Reads the live people dict at each paint (names for `@people`); writes only the two Statics, never a board or history (LLR-4302.6)
module: taskboard/app.py
modify: [I/O: Static #al-body] (replace); [I/O: Static #al-keys] (replace)
examples: (TC-4339, root action_added_list) 80x24, `escape`, `N` → `#al-keys` plain "↑↓ move   ↵ open on board   o newest/oldest   v archived   esc / N back" (the tail line is `112` > `78` cells, so it is dropped; the 5-key line is `71` ≤ `78`): the 5 glyphs "↑↓", "↵", "o", "v", "esc / N" present and no "read-only" (NC omit `v`: RED)
examples: (TC-4339, root action_added_list) 118x30 → `#al-keys` plain "↑↓ move   ↵ open on board   o newest/oldest   v archived   esc / N back   · read-only: nothing here edits a task" (`112` ≤ `116` cells); the 5 words "move", "open on board", "newest/oldest", "archived", "back" present (A-2)
examples: (TC-4326, root action_added_list) fixture with boards/beta/board.json deleted after build → unread `1`; rows `3`; the head holds "1 board not read"
examples: (TC-4366, root action_added_list) `N` → newest `True`; the head holds "newest first"
examples: (AT-4305, root action_added_list) `N`, `down` → pane source "added Sat Oct 31 · 18:20 · the created field"; `down` → "added ≈ Wed Oct 28 · 10:30 · from history.jsonl"; `down`, `down` → "added: unknown, before Oct 31 · #3 in Alpha's board file"

AddedList.action_move
req: LLR-4303.14, LLR-4303.18
in: int delta
out: None
func: NEW. Bound `up,k` → `move(-1)` and `down,j` → `move(1)`, priority. `n = len(self._ordered())`; if `n == 0`: return (no paint, sel stays 0, nothing on screen changes: LLR-4303.18); else `self.sel = max(0, min(n - 1, self.sel + delta))` and `self._paint()`. The scroll window that keeps the cursor's row on screen is render_added_list's (group V)
module: taskboard/app.py
modify: [Data: AddedList.view] (replace)
examples: (TC-4334, root action_move) one-board registry holding only Alpha (no home at start), `N` → rows "Sync notes", "Pilot store list", "Old invoice"; `up` → sel `0`; `down` ×5 → sel `2` (NC no clamp: IndexError, RED)
examples: (TC-4334, root action_move) same, sel `2`; `k` → sel `1`; `j` → sel `2`
examples: (TC-4338, root action_move) one-board registry, Alpha's three tasks archived, `N` → rows [] and the list area reads "no tasks to list"; `up`, `down` → sel `0`, `0` exceptions, app.screen is the AddedList
examples: (AT-4301, root action_move) after `o`, `down` → sel `1`; pane line 1 "Archive scans"

AddedList.action_order
req: LLR-4304.7, LLR-4304.6
in:
out: None
func: NEW. Bound `o` → `order`, priority (the App's non-priority `o` = `open_url` is never asked). `self.newest = not self.newest`; `self.sel = 0`; `self._paint()`. On an empty list it still flips the order named in the head (LLR-4303.18 names only enter, ↑, ↓)
module: taskboard/app.py
modify: [Data: AddedList.view] (replace)
examples: (TC-4367, root action_order) fixture, `escape`, `N`, `down` ×3 (sel `3`, "Archive scans"), `o` → newest `False`, sel `0`, row 0 "Old invoice", head "oldest first" (NC keep the cursor index: sel `3`, RED)
examples: (TC-4367, root action_order) then `o` → newest `True`, sel `0`, row 0 "Pay the rent", head "newest first"

AddedList.action_archived
req: LLR-4306.3, LLR-4306.4, HLR-4306
in:
out: None
func: NEW. Bound `v` → `archived`, priority (the App's `v` = `toggle_archived` is never asked; `app.show_archived` is never read or written). Steps: `rows = self._ordered()`; `key = (rows[self.sel].lane, rows[self.sel].pos) if rows else None`; `self.show_archived = not self.show_archived`; `new = self._ordered()`; `self.sel = next((i for i, r in enumerate(new) if (r.lane, r.pos) == key), 0)`; `self._paint()`. The key is (lane, file position), not `task.id`: two boards may hold one id (a copied board file, as `backlog_round_fixture`'s `with_copy` registers), and the pair names exactly one row of the snapshot (finding P-S-8). A list that turns empty gets sel `0`
module: taskboard/app.py
modify: [Data: AddedList.view] (replace)
examples: (TC-4393, root action_archived) fixture `with_archived`, `escape`, `N` → `5` rows; `v` → `6` rows; `v` → `5` rows (NC one-way: RED)
examples: (TC-4394, root action_archived) `N`, `down`, `down` (sel `2`, "Pilot store list"); `v` → sel `3`, row 3 "Pilot store list"; `v` → sel `2`, row 2 "Pilot store list" (same task, NC reset to 0: RED)
examples: (TC-4394, root action_archived) `N`, `v`, `down`, `down` (sel `2`, "Old receipts", archived); `v` → sel `0`, row 0 "Pay the rent"
examples: (AT-4304, root action_archived) `N` → head ends "· 1 archived hidden"; `v` → row 2 "Old receipts" under "FRI OCT 30", head ends "· archived shown", sel `0`; `v` → head ends "· 1 archived hidden"

AddedList.action_jump
req: LLR-4303.16, LLR-4303.18, LLR-4303.24
in:
out: None
func: NEW. Bound `enter` → `jump`, priority (the App's `enter` = `details` is never asked). `rows = self._ordered()`; if empty: return (LLR-4303.18); else `r = rows[self.sel]` and `open_on_board(self.app, self.ids[r.lane], r.task.id)`, exactly as `AllBoardsAgenda.action_jump`. What follows is the existing behaviour (node `open_on_board`): every pushed screen is popped first (the list and a home beneath it), so a board switch's own writes happen after the list is gone (LLR-4302.6 holds); then the task is selected by `jump_to`, which may refuse with a toast (archived while the main screen hides archived: LLR-4303.24, the existing notice and no selection, P-S-3 ruling; or not drawn in the view). The list never sets `app.show_archived`
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (TC-4336, root action_jump) fixture, `escape`, `N`, `down` (sel `1`, "Sync notes" of Alpha, the open board), `enter` → stack types ["Screen"]; app.board_id "alpha"; app.selected_task_id "ta1" (NC `enter` unbound: the App's `details` opens TaskDetails over the list, RED)
examples: (TC-4336b, root action_jump) `escape`, `N` (sel `0`, "Pay the rent" of Beta), `enter` → stack types ["Screen"]; app.board_id "beta" (a switch); app.selected_task_id "tb1"
examples: (TC-4344, root action_jump) fixture `archived_on_alpha`, app.show_archived `False`, `escape` (selected "ta1"), `N`, `v`, `down`, `down` (sel `2`, "Old memo", archived, Alpha = the open board), `enter` → stack types ["Screen"]; app.board_id "alpha"; app.selected_task_id "ta1" (unchanged); app.show_archived `False`; one notification "Old memo is archived — v shows it" (NC select the archived task: selected_task_id "ta4", RED)
examples: (TC-4344b, root action_jump) fixture `with_archived`, app.show_archived `False`, `escape`, `N`, `v`, `down`, `down` (sel `2`, "Old receipts", archived, Beta), `enter` → stack types ["Screen"]; app.board_id "beta" (the switch happens first); app.selected_task_id is not "tb3"; one notification "Old receipts is archived — v shows it"
examples: (TC-4338, root action_jump) one-board registry, all three archived, `N`, `enter` → app.screen is the AddedList; `0` exceptions; app.selected_task_id unchanged

AddedList.action_back
req: LLR-4303.4
in:
out: None
func: NEW. Bound `escape,N` → `back`, priority: `self.app.pop_screen()`. `N` on the list is taken by this priority binding before the App's non-priority `N` (`added_list`) is offered, so `N` closes the list it opened: stack after `N`, `N` = the stack before them. Without the screen's `N`, the App's `added_list` would run `_bring(AddedList, …)`, which finds the list already on top and does nothing (the NC arm of TC-4324)
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (TC-4324, root action_back) fixture, `escape`, `N`, `escape` → stack types ["Screen"]
examples: (TC-4324, root action_back) `escape`, `N`, `N` → stack types ["Screen"]; `0` AddedList on the stack (NC no screen `N`: the list stays, RED)
examples: (TC-4324, root action_back) at start (BoardsHome on top, no `escape`), `N` → stack types ["Screen", "BoardsHome", "AddedList"]; `N` → ["Screen", "BoardsHome"]
examples: (TC-4323, root action_back) `escape`, `N`, `A` → ["Screen", "AddedList", "AllBoardsAgenda"]; `A` (the agenda's own priority `escape,A`) → ["Screen", "AddedList"]; `escape` → ["Screen"]

open_on_board
req: LLR-4303.16
in: TaskboardApp app; str? bid; str task_id
out: None
func: unchanged from baseline (app.py:872): pops every screen above the bottom one; when `bid` is another board, `app.switch_board(bid)` (a missing file: the notice "<name>: its file is missing (<path>). Nothing was opened." and no switch); when `bid` is the open board and the home deferred its start, `app._open_board()`; then `app.jump_to(task_id)` only if `app.board_id == bid` or `bid is None` (the unlisted `--open` board, the last lane). Called by the list's `enter` with `ids[row.lane]`
module: taskboard/app.py
modify: [Data: App.screen_stack] (replace)
examples: (TC-4336b, root action_jump) bid "beta", task_id "tb1", open board "alpha" → app.board_id "beta"; selected_task_id "tb1"; stack types ["Screen"]
examples: (TC-4336d, root action_jump) fixture, boards/beta/board.json deleted after `N`, row "Pay the rent", `enter` → stack types ["Screen"]; app.board_id "alpha"; a notification holding "its file is missing"

TaskboardApp.jump_to
req: LLR-4303.16, LLR-4303.24
in: str task_id
out: None
func: unchanged from baseline (app.py:2569): no task of that id on the open board → nothing; an archived task while `app.show_archived` is False → the notice "<clip(title, 40)> is archived — v shows it", no selection; else focus and search left, `selected_task_id = task.id`, a refresh, and the notice "<title> is not drawn in this view" when the view does not draw it. The list's own `v` (AddedList.view.show_archived) is NOT the main screen's `v`, so an archived row the list shows still meets this refusal (LLR-4303.24, P-S-3 ruling: kept as is)
module: taskboard/app.py
examples: (TC-4344, root action_jump) open board Alpha, selected "ta1", task "ta4" "Old memo" archived, show_archived `False` → selected_task_id "ta1" (unchanged); notice "Old memo is archived — v shows it"
examples: (TC-4344b, root action_jump) task "tb3" archived, show_archived `False` → selected_task_id is not "tb3"; notice "Old receipts is archived — v shows it"
examples: (TC-4336, root action_jump) task "ta1", show_archived `False` → selected_task_id "ta1"

TaskboardApp.check_action
req: LLR-4303.21, LLR-4303.22, LLR-4303.3, HLR-4303
in: str action; tuple[object, ...] parameters
out: bool? allowed
func: changed from baseline: two edits, the rest as at base. (1) The modal gate's tuple gains `"added_list"`: `if action in ("agenda_all", "people_directory", "marks_manager", "added_list"): return not any(isinstance(sc, ModalScreen) for sc in self.screen_stack)` (LLR-4303.21). It comes first, so `added_list` (a SEAT_ACTIONS member once KEYMAP holds `N`) passes the holding screens like `A`, `@`, `#`. (2) The holding tuple gains `AddedList`: `(BoardsHome, AllBoardsAgenda, PeopleDirectory, MarksManager, AddedList)` → any other seat action while one of them is on the stack returns `action == "quit"` (LLR-4303.22). Docstring: name the list and `N` beside the agenda and `A`. Consequences on the list: `a`, `e`, `d`, `x`, `I`, `B`, `?`, `1`..`0`, `u` … do nothing; `q` quits; `A` pushes the agenda over the list, `@` the directory, `#` the marks manager; `N` from any of those three (list beneath) pops back to the list (`_bring`); the arrows' App priority `cursor`/`hmove` are refused (also by the base `len(screen_stack) > 1` rule), so the screen's own `up,k`/`down,j` act
module: taskboard/app.py
examples: (TC-4341, root harness) main screen, no modal → `app.check_action("added_list", ())` `True`
examples: (TC-4341, root harness) `a` (TaskModal pushed) → `app.check_action("added_list", ())` `False` (NC `added_list` not gated: `True`, RED); `ConfirmModal` pushed instead → `False`
examples: (TC-4341, root action_add_task) `a`, `N` → stack types ["Screen", "TaskModal"]; title Input value "N" (black-box arm; Textual never offers the App's `N` under a modal, so this arm alone cannot fail the NC: finding P-S-1)
examples: (TC-4342, root action_added_list) fixture, `escape`, `N`, `a` → stack types ["Screen", "AddedList"] (no TaskModal) (NC AddedList missing from the holding tuple: TaskModal opens, RED)
examples: (TC-4342, root action_added_list) `N`, `d` → no ConfirmModal; len(app.board.tasks) `3`
examples: (TC-4342, root action_added_list) `N`, `A` → stack types ["Screen", "AddedList", "AllBoardsAgenda"]
examples: (TC-4342, root action_added_list) `N`, `@` → ["Screen", "AddedList", "PeopleDirectory"]; `N` → ["Screen", "AddedList"]
examples: (TC-4342, root harness) AddedList on the stack → `app.check_action("quit", ())` `True`; `app.check_action("templates", ())` `False`; `app.check_action("agenda_all", ())` `True`

TaskboardApp._on_template_picked
req: LLR-4301.3, HLR-4301
in: tuple[str, str]? res; str project_id
out: None
func: changed from baseline: one stamp for the whole insert. After the empty-template refusal and before the loop: `when = stamp()` (the `stamp` of models.py, imported into app.py); each inserted task is `Task(title=one.title, project_id=project_id, phase=self.board.phases[0], notes=one.notes, created=when)`. Everything else as at base: `board.tasks.append(new)` directly (still NO history line: Inc L does not change which paths write history), `depends_on` wiring, ONE undo entry `{"templates": ids}`, the first selected, `board.save()`, the toast. `res` None, `("new", …)`, an unknown name or an empty template: no stamp call, no task
module: taskboard/app.py
modify: [Data: Board.tasks] (append); [Data: TaskboardApp._undo_stack] (append); [Data: Task.created] (replace)
examples: (TC-4303, root harness) res ("insert", "Simple chain"), project "pa", `models.datetime.now()` advancing `1` s per call from 2026-11-01T08:10:00 → 3 tasks "Plan", "Build", "Ship"; created ["2026-11-01T08:10:00", "2026-11-01T08:10:00", "2026-11-01T08:10:00"]; `1` distinct value (NC no stamp: created `None`, RED; NC a `stamp()` per task: `3` distinct values, RED)
examples: (TC-4303, root harness) same insert → Alpha history.jsonl still `1` line; the saved file holds "created": "2026-11-01T08:10:00" in the 3 new entries
examples: (TC-4303, root harness) res ("insert", "<an empty template>") → no task, toast "Template '<name>' is empty."
examples: (AT-4303, root action_templates) fixture, `escape`, `I`, `down`, `enter` → Alpha gains "Plan", "Build", "Ship" each created "2026-11-01T08:10:00"; `N` → rows 0–2 "Ship", "Build", "Plan", labels "08:10"; row 3 "Pay the rent"

TaskboardApp._on_task_added
req: LLR-4301.2
in: dict? data
out: None
func: unchanged from baseline: `Task(**data)` from the TaskModal payload, whose keys never include `created`, so the task reaches `Board.add_task` with `created` None and `add_task` stamps it before its save (LLR-4301.5, group D). No stamp call in app.py for this path
module: taskboard/app.py
modify: [Data: Board.tasks] (append)
examples: (TC-4302, root action_add_task) real clock; t0 = `datetime.now().replace(microsecond=0)`; `a`, type "Call the bank", `alt+s`; t1 = `datetime.now()` → the new task's created matches `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$` and t0 ≤ fromisoformat(created) ≤ t1; the board file's entry holds the same value (NC remove the stamp from the add path: created `None`, RED)
examples: (AT-4302, root action_add_task) fixture, `escape`, `a`, "Call the bank", `alt+s` → Alpha's entry "created": "2026-11-01T08:10:00"; ta1, ta2, ta3 entries byte-equal to before; `N` → row 0 "Call the bank", label "08:10", pane source "added Sun Nov 01 · 08:10 · the created field"

TaskboardApp._create_and_link
req: LLR-4301.4
in: Task waiter; str title
out: None
func: unchanged from baseline: `Task(title, project_id=waiter.project_id, phase=phases[0])` (created None) → `board.add_task(new)` stamps it (group D) → `link_tasks(waiter, new)`. An empty title or a one-phase board: no task, so no stamp
module: taskboard/app.py
modify: [Data: Board.tasks] (append)
examples: (TC-4304, root harness) Alpha, waiter "ta1", title "new", frozen clock 2026-11-01T08:10:00 → a task "new" with created "2026-11-01T08:10:00"; "ta1" depends_on holds its id; Alpha history gains a line with "from" `None` (NC bypass the stamp: created `None`, RED)
examples: (test_gantt_link.py::test_R2_2_create_on_a_one_phase_board_is_refused) a one-phase board → no task; the toast "a one-phase board has no open phase to create it in"

TaskboardApp._on_task_edited
req: LLR-4301.8
in: Task task; dict? data
out: None
func: unchanged from baseline: `setattr` over the TaskModal payload's keys only (id, title, project_id, phase via set_task_phase, blocked, pinned, show_in_present, priority, notes, urls, images, mark when changed; archived, milestone and dates apart). `created` is not a payload key, so an edit never reads or writes it
module: taskboard/app.py
examples: (TC-4308, root action_edit) Alpha task "ta1" created "2026-10-01T09:00:00"; `e`, change the title to "Sync notes v2", `alt+s` → created "2026-10-01T09:00:00"
examples: (TC-4308, root action_edit) task "ta2" (no created); `e`, change the title, `alt+s` → created `None`; Alpha's file entry for "ta2" holds no "created" key (NC stamp on edit: RED)

TaskboardApp.action_undo
req: LLR-4301.10
in:
out: None
func: unchanged from baseline: the delete entry re-inserts the SAME Task object (`board.tasks.insert(idx, gone)`, app.py:2861), so every field, `created` included, comes back as it was; no stamp. A template insert's undo removes the tasks (their stamps go with them)
module: taskboard/app.py
modify: [Data: Board.tasks] (append)
examples: (TC-4310, root action_undo) Alpha, "ta1" created "2026-10-01T09:00:00" selected; `d`, `y`, `u` → "ta1" back at index `0`; created "2026-10-01T09:00:00"; the saved file holds "created": "2026-10-01T09:00:00" (NC re-stamp on restore: RED)
examples: (TC-4310, root action_undo) "ta2" (no created) selected; `d`, `y`, `u` → created `None`; its file entry holds no "created" key

## Entities

[Data: AddedList.snapshot]
in: tuple(list lanes, list ids, list[AddedRow] rows, datetime? first, date today)
desc: NEW. Written once by `AddedList.compose` (and emptied by `__init__`); never re-read while the screen lives, even when `_bring` returns to it from the agenda, the directory or the marks manager (LLR-4303.5). `ids[lane]` is the registry id `open_on_board` needs (None: the unlisted board). `rows` holds archived tasks too; `first` comes from all of them

[Data: AddedList.view]
in: tuple(int sel, bool newest, bool show_archived)
desc: NEW. The screen's own state: `sel` indexes `AddedList._ordered()`; `newest` starts True; `show_archived` starts False and is independent of `TaskboardApp.show_archived` both ways (neither reads the other)

[Data: app.ADDED_KEYS]
in: list[tuple[str, str]]
desc: NEW, app.py beside AGENDA_KEYS: `[("↑↓", "move"), ("↵", "open on board"), ("o", "newest/oldest"), ("v", "archived"), ("esc / N", "back")]`. One pair per screen binding (j/k ride `↑↓`; `N` rides `esc`); read by `AddedList._paint` through `key_line`

[I/O: Static #al-body]
in: Text
desc: NEW. The list and the pane from render_added_list: `h − 1` lines, `w − 2` cells (padding 0 1)

[I/O: Static #al-keys]
in: Text
desc: NEW. Docked bottom, height 1, background #0b0f17; `key_line(ADDED_KEYS + [read-only tail])` when it fits `w − 2`, else `key_line(ADDED_KEYS, w − 2)` (A-2)

[Interface: AddedList key row]
desc: NEW. The controls `#al-keys` shows, each with the node a press must run (the screen's priority BINDINGS: `escape,N` back · `up,k` move(-1) · `down,j` move(1) · `o` order · `v` archived · `enter` jump). The seam entity `[Interface: AddedList keys]` (graph-interfaces) names the same keys; this one points each control at its action node (finding P-S-6)
offers: (TC-4334) "↑↓ move" → AddedList.action_move
offers: (TC-4336) "↵ open on board" → AddedList.action_jump
offers: (TC-4367) "o newest/oldest" → AddedList.action_order
offers: (TC-4393) "v archived" → AddedList.action_archived
offers: (TC-4324) "esc / N back" → AddedList.action_back

[Data: App.screen_stack]
in: list[Screen]
desc: as in the baseline; the list adds the states [Screen, AddedList], [Screen, BoardsHome, AddedList] (`N` on the home) and [Screen, AddedList, <AllBoardsAgenda | PeopleDirectory | MarksManager>]; never two AddedList (`_bring`)

[Data: app.SEAT_ACTIONS]
in: frozenset[str]
desc: as in the baseline; gains "added_list" when group D adds the KEYMAP entry `N`; `check_action` tests the modal gate before SEAT_ACTIONS, so the new member is not held by the holding screens

[Data: Board.tasks]
in: list[Task]
desc: as in the baseline; `_on_template_picked` now appends tasks that carry one shared `created`

[Data: Task.created]
in: str?
desc: seam entity of graph-interfaces; in app.py it is written only by `_on_template_picked` (through `stamp()`); every other app path leaves it to `Board.add_task` or keeps it

[Data: TaskboardApp._undo_stack]
in: list[dict]
desc: as in the baseline

[Outside: key N]
desc: CHANGED. KEYMAP `added_list` (group D: global, `bar=False`, not priority) → `check_action` → `action_added_list`; on the list itself the screen's priority `escape,N` → back wins; under any ModalScreen Textual never offers it (chain cut at the modal)

[Outside: key escape]
desc: AddedList priority `back` (the App's non-priority `focus_exit` is never asked on the list)

[Outside: key up,k / down,j]
desc: the App's priority `cursor(±1)` is offered first and refused by check_action; then AddedList's priority `move(±1)`

[Outside: key o]
desc: AddedList priority `order` (the App's `open_url` is never asked on the list)

[Outside: key v]
desc: AddedList priority `archived` (the App's `toggle_archived` is never asked on the list; `app.show_archived` unchanged)

[Outside: key enter]
desc: AddedList priority `jump` (the App's `details` is never asked on the list)

[Outside: key A, @, #]
desc: no AddedList binding; the App's `agenda_all` / `people_directory` / `marks_manager`, allowed by check_action (no modal), push their screen over the list

[Outside: key seat]
desc: every other KEYMAP key pressed on the list (`a`, `e`, `d`, `x`, `I`, `B`, `?`, `u`, the view digits …): refused by check_action; `q` quits

## Edges

[Outside: key N] ──▶ TaskboardApp.check_action
when: AddedList is not the screen; added_list allowed iff no ModalScreen is on the stack; then action_added_list (`_bring`)
[Outside: key N] ──▶ AddedList.action_back
when: AddedList is the screen (its priority binding wins over the App's non-priority N)
[Outside: key escape] ──▶ AddedList.action_back
when: AddedList is the screen
[Outside: key up,k / down,j] ──▶ TaskboardApp.check_action
when: AddedList is the screen; the App's priority cursor binding is asked first and refused
[Outside: key up,k / down,j] ──▶ AddedList.action_move
when: AddedList is the screen
[Outside: key o] ──▶ AddedList.action_order
when: AddedList is the screen
[Outside: key v] ──▶ AddedList.action_archived
when: AddedList is the screen
[Outside: key enter] ──▶ AddedList.action_jump
when: AddedList is the screen
[Outside: key A, @, #] ──▶ TaskboardApp.check_action
when: AddedList is the screen; allowed (no modal); the screen is pushed over the list
[Outside: key seat] ──▶ TaskboardApp.check_action
when: AddedList is on the stack; refused except quit
AddedList.__init__ ──▶ [Data: AddedList.view]
AddedList.__init__ ──▶ [Data: AddedList.snapshot]
AddedList.compose ──▶ [Data: AddedList.snapshot]
[Data: AddedList.snapshot].rows ──▶ AddedList._ordered
[Data: AddedList.view].newest ──▶ AddedList._ordered
[Data: AddedList.view].show_archived ──▶ AddedList._ordered
[Data: AddedList.snapshot] ──▶ AddedList._paint
[Data: AddedList.view] ──▶ AddedList._paint
[Data: app.ADDED_KEYS] ──▶ AddedList._paint
AddedList._paint ──▶ [I/O: Static #al-body]
AddedList._paint ──▶ [I/O: Static #al-keys]
AddedList.action_move ──▶ [Data: AddedList.view]
AddedList.action_order ──▶ [Data: AddedList.view]
AddedList.action_archived ──▶ [Data: AddedList.view]
[Data: AddedList.view].sel ──▶ AddedList.action_jump
[Data: AddedList.snapshot].ids ──▶ AddedList.action_jump
AddedList.action_jump ──▶ open_on_board
open_on_board ──▶ [Data: App.screen_stack]
open_on_board ──▶ TaskboardApp.jump_to
AddedList.action_back ──▶ [Data: App.screen_stack]
[Data: App.screen_stack] ──▶ TaskboardApp.check_action
[Data: app.SEAT_ACTIONS] ──▶ TaskboardApp.check_action
AddedList.compose ──▶ added_rows
AddedList.compose ──▶ first_created
AddedList._ordered ──▶ added_order
AddedList._paint ──▶ render_added_list
TaskboardApp._on_template_picked ──▶ [Data: Task.created]
TaskboardApp._on_template_picked ──▶ [Data: Board.tasks]
TaskboardApp._on_template_picked ──▶ [Data: TaskboardApp._undo_stack]
TaskboardApp._on_task_added ──▶ [Data: Board.tasks]
TaskboardApp._create_and_link ──▶ [Data: Board.tasks]
TaskboardApp.action_undo ──▶ [Data: Board.tasks]

## Findings

finding P-S-1 MAJOR: the key arm of LLR-4303.21 cannot fail its negative control
anchor: TaskboardApp.check_action
seen: (probe S-1) Textual 8.2.8 offers non-priority bindings along `_modal_binding_chain`, which stops at the first modal node (`screen.py:449-455`); `N` (like `A`) is a non-priority App binding, so under the task editor it is never offered: the title Input takes "N" and the stack stays [Screen, TaskModal], WITH or WITHOUT the gate. The same holds for `A` over a ConfirmModal (both runs of probe S-1). LLR-4303.21's threshold ("with the task editor open, `N` … → no list view") passes under its own NC ("`added_list` not gated")
cause: the gate in check_action is defence in depth for a path no key reaches (the palette dismisses itself before `run_action`, so it is not under a modal either)
effect: TC-4341 written from the threshold text is vacuous; the gate could be removed or broken with every test green
decision: ruling (03-pdr-rulings round 0): "Accept. TC-4341 asserts app.check_action("added_list", ()) is False with a ModalScreen on the stack (and True without); a pilot arm checks that N in the task editor opens no list view. LLR-4303.21 threshold rewritten." Applied: TaskboardApp.check_action TC-4341 (2 direct `check_action` arms: True with no modal; False under TaskModal and ConfirmModal — the NC arm; plus the pilot key arm, not the NC's). The same weakness of test_TC_2401 stays a backlog note

finding P-S-2 the "one same stamp" arm of LLR-4301.3 is vacuous under a frozen clock
anchor: TaskboardApp._on_template_picked
seen: with `models.datetime.now()` fixed at 08:10:00, a mutant that calls `stamp()` once per task also yields 1 distinct value; with the real clock it yields 1 value unless the loop crosses a second boundary (flaky detection)
decision: ruling (03-pdr-rulings round 0): "Accept (same clock as P-D-10): TC-4303/TC-4306 use a clock that advances 1 s per call (monkeypatched models.datetime), so a stamp-per-task mutant fails." Applied: TaskboardApp._on_template_picked TC-4303 (advancing clock: 1 distinct value; per-task NC 3, RED); fixture note's clock line

finding P-S-3 `enter` on an archived row the list shows lands on a refusal, and LLR-4303.16 does not say so
anchor: AddedList.action_jump
seen: the list's `v` is independent of the main screen's `v` (LLR-4306.2). With the list showing archived tasks and `app.show_archived` False, `enter` on "Old receipts" pops the list, switches to Beta, and `jump_to` refuses: notice "Old receipts is archived — v shows it", no selection (existing behaviour, app.py:2575). Likewise "<title> is not drawn in this view" for a task the current view folds away. LLR-4303.16 says "select the cursor's task on its board" with no exception
cause: the requirement was written for the open-board, live-task case only (its threshold covers just that)
effect: an implementer may set `app.show_archived = True` to honour the literal text, which silently changes the main screen's `v`
decision: ruling (03-pdr-rulings round 0): "Accept. New LLR-4303.24: enter on an archived task while the main screen hides archived shows the existing jump_to notice (<title> is archived — v shows it) and selects nothing." Applied: req LLR-4303.24 on AddedList.action_jump and TaskboardApp.jump_to; TC-4344 (open board, fixture `archived_on_alpha`: notice + selected_task_id unchanged + show_archived unchanged), TC-4344b (the cross-board case, formerly TC-4336c)

finding P-S-4 a two-board registry starts on BoardsHome; the byte hashes must follow the board start
anchor: AddedList.compose
seen: `TaskboardApp.on_mount` pushes BoardsHome when more than one board is active and defers the board start (app.py:1324-1331); `escape` on the home starts the board (`_open_board`: migrations, sweeps, presence). `N` on the home is allowed (no modal) and opens the list over it: [Screen, BoardsHome, AddedList]
effect: LLR-4302.6's "sha256 before `N`" taken before leaving the home may measure the board start's writes, not the list's; the ATs say "press `N`" from an unspecified screen
decision: ruling (03-pdr-rulings round 0): "Accept: LLR-4302.6's hashes are taken after leaving the home (escape), before N." Applied: fixture note, AddedList.compose TC-4317, AT-4301 and AT-4305 sequences

finding P-S-5 TC ids already used by the interface examples collide with this group's tests
anchor: TaskboardApp._on_task_added
seen: graph-interfaces gives `stamp` the example id TC-4302 (the format) and `added_order` TC-4366 (newest = reverse). By the numbering rule TC-4302 is LLR-4301.2's test (the editor path) and TC-4366 LLR-4304.6's (the list opens newest first)
decision: ruling (03-pdr-rulings round 0): "Accept: interface examples renamed TC-4302 → TC-4302b (stamp format), TC-4366 → TC-4366b (pure reverse)." Applied: here TC-4302 stays the editor-path pilot test (_on_task_added); this file's LLR-4304.6 pilot arms are renamed TC-4366b → TC-4366 (AddedList.__init__, AddedList._paint), since TC-4366b is now the interface's pure reverse

finding P-S-6 the interface offers point at the class, not at an action node
anchor: AddedList.action_back
seen: graph-interfaces `[Interface: AddedList keys]`: `offers: (TC-4324) "escape" → AddedList`. An offer names the node a press must run; `AddedList` is the screen class, so C16 cannot check that `back` ran
decision: ruling (03-pdr-rulings round 0): "Accept: the offer for escape names AddedList.action_back." Applied: graph-interfaces `[Interface: AddedList keys]` (orchestrator; checked); here `[Interface: AddedList key row]` keeps one offer per control, all naming action nodes

finding P-S-7 the `AddedList` seam declares an input the screen never receives
anchor: AddedList.__init__
seen: graph-interfaces `AddedList`: `in: TaskboardApp app`. `TaskboardApp.action_added_list` is `self._bring(AddedList, AddedList)` and `_bring` calls `make()` with no argument (app.py:1415); the screen reads `self.app`, as AllBoardsAgenda does
decision: ruling (03-pdr-rulings round 0): "Accept: AddedList has no in: app (it reads self.app)." Applied: graph-interfaces `AddedList` (orchestrator; checked: `in:` empty); here AddedList.__init__ takes no argument

finding P-S-8 the archived toggle keeps "the same task" by row, not by task id
anchor: AddedList.action_archived
seen: LLR-4306.4's threshold says "same task id"; task ids are unique per board only: a copied board file (backlog_round_fixture `with_copy`, `board-copy` registered) holds the ids of its source, so `task.id` can match two rows
decision: ruling (03-pdr-rulings round 0): "Accept: the cursor keeps its task by (lane, pos) (ids can repeat across boards). LLR-4306.4 'same task' means the same (lane, pos)." Applied: AddedList.action_archived func and TC-4394 (same (lane, pos) after `v`, `v`)

finding ARCH-4 MINOR: this file's node examples carried no evidence state
anchor: AddedList.compose
seen: (03-pdr-architect.md ARCH-4) groups D and V state that every example ran on a scratch reference; S stated only probes S-1 and S-2, so its ~45 pilot examples read as checked while they were `planned`
decision: ruling (03-pdr-rulings round 1): "Accept: the tester runs every S example; none is claimed executed before E4." Applied: header paragraph "Evidence state of this file's node examples: planned" (probes S-1..S-3 the only executed items)

finding ARCH-5 MINOR: the list did not repaint when resumed
anchor: AddedList.on_screen_resume
seen: (03-pdr-architect.md ARCH-5) `@` / `#` over the list can rename a person or mark class; back on the list, `#al-body` kept the last paint's names until the next key (AllBoardsAgenda has the same exposure, pre-existing)
decision: ruling (03-pdr-rulings round 1): "Accept: AddedList.on_screen_resume repaints (people/marks renamed under @/# show at once). Example under LLR-4303.11 (TC-4331b)." (addendum A-1) Applied: new node AddedList.on_screen_resume (`self._paint()`) with TC-4331b; the agenda's twin is the orchestrator's backlog note, not in this file

finding ARCH-6 MINOR: LLR-4302.6's subject was the whole system, but app timers write while the list is open
anchor: AddedList.compose
seen: (03-pdr-architect.md ARCH-6) `_team_sync_tick` (team mode) and the presence renewal in `_tick` run under any screen; TC-4317's fixture has no team mode, so the test passes while the system-wide statement is false in team mode
decision: ruling (03-pdr-rulings round 1): "Accept: LLR-4302.6's subject becomes 'the list view'." Applied: AddedList.compose func (the subject is the list's own code paths; the timers named as not the list's writes); TC-4317 unchanged

finding ARCH-9 MINOR: the key row dropped the agenda's read-only tail
anchor: AddedList._paint
seen: (03-pdr-architect.md ARCH-9) AllBoardsAgenda._paint appends `("·", "read-only: nothing here edits a task")` and drops it first when narrow (app.py:936–938); S wrote "no read-only tail" for an equally read-only screen
decision: ruling (03-pdr-rulings round 1): "Accept (conformance): the key row adds the agenda's tail · read-only: nothing here edits a task when it fits whole, else drops it first (AllBoardsAgenda._paint)." (addendum A-2) Applied: AddedList._paint func (the agenda's two-step rule), TC-4339 (118x30: tail shown, 112 ≤ 116 cells; 80x24: tail dropped, all 5 keys stay), on_mount TC-4322 ("starts"), [I/O: Static #al-keys], probe S-3

finding SEC-2 MEDIUM: a deeply nested history line crashed `N` at compose
anchor: AddedList.compose
seen: (03-pdr-security.md SEC-2) compose's "no try/except" rested on `added_rows` being total for OSError only; a RecursionError from `history.read` escaped compose
decision: ruling (03-pdr-rulings round 1): "Accept. added_rows guards history.read with (OSError, ValueError, RecursionError); TC-4372c." Applied here: AddedList.compose func text (what makes `added_rows` total); the guard and TC-4372c are group V's (graph-proto-V added_rows)

finding SEC-3 MEDIUM: a non-str task id on a peeked board crashed `N`
anchor: AddedList.compose
seen: (03-pdr-security.md SEC-3) `births.get(task.id)` ran in compose for every row; a list or dict id raised TypeError
decision: ruling (03-pdr-rulings round 1): "Accept. Birth lookups and the after: title lookup use only str ids … New LLR-4304.17, TC-4377." Applied here: AddedList.compose func text only; the lookups and TC-4377 are group V's. The screen keeps the cursor by (lane, pos) (P-S-8), so no S code hashes a task id; `enter` on such a row passes the id to `open_on_board` → `jump_to`, which compares ids with `==` (base behaviour, not hashed)

### Seams
> Calls INTO other groups (consumed by app.py): group D — `stamp()` (models.py) in `_on_template_picked`, ONE call per insert; `Task(..., created=when)` (the field and its keyword, LLR-4301.1); `Board.add_task` stamps for `_on_task_added` and `_create_and_link` (no app.py change); the KEYMAP entry `Key("N", "N", "added_list", …, bar=False)` (keymap.py), which makes the App binding and the SEAT_ACTIONS member this file's check_action names; README row for `N`. Group V — `added_rows(lanes)` and `first_created(rows)` in `AddedList.compose`; `added_order(rows, newest, show_archived)` in `AddedList._ordered`; `render_added_list(rows, sel, newest, show_archived, hidden, unread, first, today, people, width, height)` in `AddedList._paint`, with `width = w − 2`, `height = h − 1`, `hidden` = archived rows left out (0 while shown), `unread` = lanes whose board is None, `people` = `app.people.people`; `[Data: AddedRow]` fields `task`, `lane`, `pos` read by the screen.
> Calls OUT of this group that others rely on: none into app.py — groups D and V call nothing in app.py. The interface node `TaskboardApp.action_added_list` (`_bring(AddedList, AddedList)`) is implemented in app.py by this group as defined in graph-interfaces; `AddedList` and `ADDED_KEYS` are defined after `AllBoardsAgenda` / beside `AGENDA_KEYS`.
> Shared test fixture: `tests/added_list_fixture.py` (the fixture note above) is offered to group V's pilot tests (TC-4327, TC-4328, TC-4329, TC-4330) so that the headers, labels and source lines above are the same strings in both groups' tests.

# Requirements — taskboard — Inc L, the added-order list view (dev-flow-v3-beta)

> Strict EARS (five forms only), ISO/IEC/IEEE 29148. One `shall` per requirement. Each carries a
> numeric pass threshold and a negative control (*NC*: a mutant that turns its test RED). Ids continue
> the repo's sequence in a fresh block: US-4301, HLR-4301..4306, LLR-4301.n..4306.n, TC-43nn, AT-43nn.
> Base: `eb411e1` (branch `feat/capture-list-colour`, Inc C done). Commission:
> `.dev-flow/COMMISSION-capture-list-colour.md` §Inc L (L-1..L-5). Design source: the round's
> `ListB` (`prototypes/capture_round/proto.py`, `out/png/ls-B_*.png`) plus the operator's deltas
> (the state column, the archived toggle).
> **TC numbering:** LLR-4301.n → TC-(4300+n); LLR-4302.n → TC-(4311+n); LLR-4303.n → TC-(4320+n);
> LLR-4304.n → TC-(4360+n); LLR-4305.n → TC-(4380+n); LLR-4306.n → TC-(4390+n). A second test of one LLR adds a letter (TC-4364b).

## 1. Scope

**In:** the new `Task.created` field and its stamping at every path that creates a persisted task; its
serialisation (written only when set); the inference of an added moment for old tasks (history, then
unknown) with no rewrite; the global list view on `N` (variant B: narrow list + detail pane), its order
toggle, the phase-box state column, the archived toggle, its keys.
**Not in:** Inc K (the capture view, `inbox.json`, its dump — it must reach `Board.add_task`, which
stamps; LLR-4301.5 is the seam). No change to `history.jsonl`'s format or to which paths write it
(template insert keeps writing no history record). No new dependency.

**Definitions.**

| Term | Meaning |
|---|---|
| stamp | `datetime.now().isoformat(timespec="seconds")`: local time, `YYYY-MM-DDTHH:MM:SS`, the format of `history.append`'s `at` |
| valid created | a `created` value that is a `str` and that `datetime.fromisoformat` parses |
| birth record | a `history.read` record whose `task` is the task's id and whose `from` is `None` (written by `Board.add_task`) |
| added moment | a row's place in time: its valid created (source `c`), else the `at` of its first birth record in file order (source `h`, shown `≈`), else unknown (source `?`) |
| first created date | the earliest valid created among all tasks the list read (archived included), as `%b %-d` (e.g. `Oct 31`) |
| old board | a board file whose tasks hold no `created` key |
| list view | the screen `N` opens (working name `AddedList`) |
| row | one task line in the list (a day header is not a row) |
| state column | the run of phase boxes in a row |
| board order | the order `app.board_lanes` returns the boards in (registry order, the unlisted `--open` board last) |
| file position | a task's index in its board's `tasks` list |

## 2. Source user story

**US-4301.** As the board's owner (`username_subject`), I want one list of every task of every board in
the order I added them, with where each one stands and everything about the one under the cursor, so that
what I captured in a hurry is findable by when I added it, not by its planned dates. (Operator verdict 2:
B, plus a state column of phase boxes and an archived toggle; D3: `Task.created`, old tasks inferred,
never rewritten.)

## 3. High-level requirements

### HLR-4301 — every persisted task records when it was added
- **Traceability:** US-4301 · L-5 · D3
- **Ledger:** LED-2026-11-01-incL.1
- **Statement:** The system shall set `Task.created` to a stamp on every path that creates a persisted task.
- **Validation:** `test` — `tests/test_task_created.py`
- **Numeric pass threshold:** 5/5 creation paths stamp (LLR-4301.2..4301.6); 3/3 non-creation paths keep the value (LLR-4301.8..4301.10).
- **Acceptance test(s):** AT-4302, AT-4303
- **Negative control:** base `Task` has no `created`: TC-4301, TC-4302 and every stamping TC RED at base.

### HLR-4302 — old boards keep their bytes and old tasks are never rewritten
- **Traceability:** US-4301 · L-5 · D3
- **Ledger:** LED-2026-11-01-incL.1
- **Statement:** The system shall leave the stored bytes of every task that holds no `created` unchanged by this increment's code.
- **Validation:** `test` — `tests/test_task_created.py -k bytes`
- **Numeric pass threshold:** 0 byte differences over LLR-4302.4..4302.6.
- **Acceptance test(s):** AT-4305
- **Negative control:** a mutant that back-fills an inferred `created` on save: AT-4305 RED.

### HLR-4303 — a global list view on `N`, variant B
- **Traceability:** US-4301 · L-1 · verdict 2
- **Ledger:** LED-2026-11-01-incL.1
- **Statement:** The system shall show every listed task in a narrow list beside a detail pane for the cursor's task when `N` is pressed.
- **Validation:** `test` — `tests/test_added_list.py` (pilot)
- **Numeric pass threshold:** all LLR-4303.n thresholds at 118x30 and 80x24.
- **Acceptance test(s):** AT-4301
- **Negative control:** base has no `N` binding: AT-4301 RED.

### HLR-4304 — rows in added order, inferred honestly for old tasks
- **Traceability:** US-4301 · L-2 · L-5 · D3
- **Ledger:** LED-2026-11-01-incL.1
- **Statement:** The system shall order the list by each task's added moment and label how that moment is known.
- **Validation:** `test` — `tests/test_added_list.py -k order` (layer 0 + pilot)
- **Numeric pass threshold:** all LLR-4304.n thresholds.
- **Acceptance test(s):** AT-4301, AT-4305
- **Negative control:** order by file position only: TC-4364 RED.

### HLR-4305 — the state column
- **Traceability:** US-4301 · L-3 · verdict 2 objection
- **Ledger:** LED-2026-11-01-incL.1
- **Statement:** The system shall show in each row one box per phase of the task's board, filled up to the task's phase.
- **Validation:** `test`
- **Numeric pass threshold:** all LLR-4305.n thresholds.
- **Acceptance test(s):** AT-4301
- **Negative control:** fill exclusive of the current phase: TC-4381 RED.

### HLR-4306 — the archived toggle
- **Traceability:** US-4301 · L-4 · verdict 2 objection
- **Ledger:** LED-2026-11-01-incL.1
- **Statement:** The system shall hide archived tasks from the list until the archived toggle shows them dimmed.
- **Validation:** `test`
- **Numeric pass threshold:** all LLR-4306.n thresholds.
- **Acceptance test(s):** AT-4304
- **Negative control:** archived listed by default: TC-4391 RED.

## 4. Low-level requirements

### 4.1 `Task.created` and the creation paths (HLR-4301)

- **LLR-4301.1 — Ubiquitous.** The system shall hold a task's added moment in an optional field `Task.created` whose default is `None`.
  Threshold: `Task("x").created is None`; `Task("x", created="2026-10-31T18:20:00").created == "2026-10-31T18:20:00"`; 2/2. *NC:* a `default_factory` stamp: arm 1 RED.
- **LLR-4301.2 — Event.** When a task is added through the task editor (`a`, a title, `alt+s`), the system shall set its `created` to a stamp.
  Threshold: the saved task's `created` matches `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$` and lies within [t0, t1] of the test's clock reads; 1/1. *NC:* remove the stamp from the add path: RED.
- **LLR-4301.3 — Event.** When a template is inserted (`I`), the system shall set `created` on every inserted task to one same stamp.
  Threshold: for a 3-task template, 3/3 stamped, 1 distinct value. *NC:* no stamp on template insert: RED.
- **LLR-4301.4 — Event.** When the link picker's create row creates a task, the system shall set its `created` to a stamp.
  Threshold: `_create_and_link(waiter, "new")` → the new task stamped; 1/1. *NC:* bypass the stamp: RED.
- **LLR-4301.5 — Event.** When `Board.add_task` receives a task whose `created` is `None`, the system shall set its `created` to a stamp before the board is saved.
  Threshold: the board file read back holds the task's `created` = the stamp; 1/1. *NC:* stamp after `save()`: the file lacks the key: RED.
- **LLR-4301.6 — Event.** When a missing board file is seeded with sample data (`Board.load` on a path that does not exist), the system shall set `created` on every seeded task to one same stamp.
  Threshold: n/n seeded tasks stamped, 1 distinct value. *NC:* seed without stamps: RED.
- **LLR-4301.7 — Unwanted.** If `Board.add_task` receives a task whose `created` is already set, then the system shall keep that value.
  Threshold: `created="2026-10-01T09:00:00"` survives `add_task`; 1/1. *NC:* always overwrite: RED.
- **LLR-4301.8 — Event.** When a task is edited (`e`, any change, `alt+s`), the system shall keep its `created` unchanged.
  Threshold: a stamped task and an unstamped task edited: values `"2026-10-01T09:00:00"` and `None` unchanged; 2/2. *NC:* stamp on edit: arm 2 RED.
- **LLR-4301.9 — Event.** When a project is moved to another board (`boards.move_project`), the system shall keep each moved task's `created` unchanged in the target board file.
  Threshold: a stamped task keeps its value, an unstamped one keeps no key; 2/2. *NC:* re-stamp moved tasks: RED.
- **LLR-4301.10 — Event.** When a deleted task is restored by `u`, the system shall keep its `created` unchanged.
  Threshold: 1/1. *NC:* re-stamp on restore: RED.
- **LLR-4301.11 — Unwanted.** If a board entry is rescued as unreadable (`_rescue_task`), then the system shall leave the rescued task's `created` as `None`.
  Threshold: `Task.from_dict(["x"]).created is None`; 1/1. *NC:* stamp in `_rescue_task`: RED.

### 4.2 The board file (HLR-4302)

- **LLR-4302.1 — Ubiquitous.** The system shall write a task's `created` key only when the task's `created` is not `None`.
  Threshold: `Board._to_dict(Task("x"))` has no `created` key; with a value, the key holds it; 2/2. *NC:* always write: arm 1 RED (`"created": null`).
- **LLR-4302.2 — Ubiquitous.** The system shall read a task's `created` from a board entry whose `created` value is a `str`.
  Threshold: `Task.from_dict({"title":"a","created":"2026-10-30T08:10:00"}).created == "2026-10-30T08:10:00"`; and `"not a date"` is read as the same string (validity is the list's concern, LLR-4304.8); 2/2. *NC:* parse-or-drop on read: arm 2 RED.
- **LLR-4302.3 — Unwanted.** If a board entry's `created` value is not a `str`, then the system shall write that value back unchanged when the board is saved.
  Threshold: entries with `"created": 5` and `"created": null` round-trip load→save to the same values; 2/2. *NC:* drop non-string values: RED.
- **LLR-4302.4 — Event.** When an old board is loaded and saved with no change, the system shall write the exact bytes it read.
  Threshold: 3 synthetic old boards (plain; legacy `status`/`url` keys; an unknown task key) — byte-equal after `Board.load` + `save()`; 3/3. *NC:* `_to_dict` writes `"created": null`: RED.
- **LLR-4302.5 — Event.** When a task is added to an old board, the system shall write every other task's entry exactly as it was.
  Threshold: each old task's JSON entry (the `json.dumps(entry, indent=2)` slice) equal before and after the add; n/n. *NC:* back-fill inferred `created` on save: RED.
- **LLR-4302.6 — State.** While the list view is open, the system shall write no board file and no `history.jsonl`.
  Threshold: sha256 of 2 board files and their 2 `history.jsonl` equal before `N` and after `↓ ↓ o v v esc`; 4/4. *NC:* a `save()` in the screen's compose: RED.

### 4.3 The list view (HLR-4303)

- **LLR-4303.1 — Ubiquitous.** The keymap shall declare `N` as one global key (action `added_list`, `bar=False`, no `views` scope), as `A` is declared.
  Threshold: exactly 1 `KEYMAP` entry whose `keys` is `"N"`; `bar is False`; `views is None`; the existing key-law tests stay GREEN; 3/3. *NC:* entry missing: RED.
- **LLR-4303.2 — Event.** When `N` is pressed on the main screen, the system shall open the list view.
  Threshold: `app.screen` is the list view after `N`; 1/1. *NC:* unbound: RED.
- **LLR-4303.3 — Event.** When `N` is pressed while a list view is already on the screen stack, the system shall bring that list view to the top without opening a second one.
  Threshold: `N`, `A`, `N` → exactly 1 list view on the stack and it is `app.screen`; 1/1. *NC:* always push: 2 instances: RED.
- **LLR-4303.4 — Event.** When `esc` or `N` is pressed in the list view, the system shall close the list view.
  Threshold: both keys → the main screen is `app.screen`; 2/2. *NC:* `N` not bound in the screen: arm 2 RED (a second view or none closed).
- **LLR-4303.5 — Ubiquitous.** The list view shall read the tasks of every board `app.board_lanes` returns, read once when the view opens.
  Threshold: registry of 2 boards (3 + 2 tasks) → 5 rows; 1/1. *NC:* only `app.board`: 3 rows: RED.
- **LLR-4303.6 — Unwanted.** If a board's file is missing or unreadable, then the list view shall show `· <n> board(s) not read` in its head row.
  Threshold: 1 missing board → the head row holds `1 board not read`; 2 → `2 boards not read`; 2/2. *NC:* silent skip: RED.
- **LLR-4303.7 — Ubiquitous.** The list view shall draw the list in the left `lw` cells and the detail pane after a ` │ ` separator, with `lw = 46` when the body is ≥ 100 cells wide and `lw = 34` otherwise.
  Threshold: the `│` at cell 47 (118x30, after the 1-cell gutter) and cell 35 (80x24) on every body line; 2/2. *NC:* one width for both: one arm RED.
- **LLR-4303.8 — Ubiquitous.** Each row shall read, left to right: the cursor mark (`▶` or a space), the time label (LLR-4304.9) in 7 cells, the state column (HLR-4305), a space, `▍` in the task's project hue, and the title clipped to the cells left.
  Threshold: the fixture row for a stamped `Doing` task on a 4-phase board reads `▶18:20  ■■□□ ▍Sync notes` at 118x30 (pads per the graph example); no row exceeds `lw` cells; 2/2. *NC:* state column after the title: RED.
- **LLR-4303.9 — Ubiquitous.** The list shall put a day header line before the first row of each added day: `TODAY`, `YESTERDAY`, else the date as `%a %b %d` in upper case; a day known only from history ends with ` ≈`; unknown rows sit under `BEFORE <first created date> · ?`.
  Threshold: the fixture yields headers `TODAY`, `YESTERDAY`, `WED OCT 28 ≈`, `BEFORE OCT 31 · ?` in that order (newest first, today 2026-11-01); 4/4. *NC:* no ≈ suffix: RED.
- **LLR-4303.10 — Ubiquitous.** The detail pane shall show, from its top line: the cursor task's title in bold; the project name and board name; the meta line; the source line (LLR-4304.10); a rule of `─`.
  Threshold: pane lines 1–5 match the graph example at 118x30; 1/1. *NC:* source line missing: RED.
- **LLR-4303.11 — Ubiquitous.** The detail pane's meta line shall hold the task's phase, its priority, its start→due dates when set, its milestone mark when set, its `@people` when any, its link count when any and its image count when any.
  Threshold: a task with all seven facts shows 7/7 pieces; a bare task shows phase and priority only; 2/2. *NC:* drop the dates: RED.
- **LLR-4303.12 — Ubiquitous.** The detail pane shall render the task's notes below the rule through `views.notes_text`, wrapped to the pane width.
  Threshold: notes `::b:: ask the vendor ::` → pane cells for `ask the vendor` carry `HEX["blue"]` and no `::` is drawn; 1/1. *NC:* plain `Text(notes)`: markers drawn: RED.
- **LLR-4303.13 — Ubiquitous.** The detail pane shall list after the notes each URL, each image file name and `after:` with the titles of the tasks the task waits on.
  Threshold: 1 URL, 1 image, 1 predecessor → 3/3 lines present. *NC:* drop `after:`: RED.
- **LLR-4303.14 — Event.** When `↓`/`j` or `↑`/`k` is pressed in the list view, the system shall move the cursor one row down or up, clamped to the first and last rows.
  Threshold: 3 rows: `↑` at row 0 stays 0; `↓`×5 ends at 2; 2/2. *NC:* no clamp: IndexError/RED.
- **LLR-4303.15 — Ubiquitous.** The list shall scroll so that the cursor's row is on screen.
  Threshold: 40 tasks at 80x24, cursor moved to the last row → its title is drawn; 1/1. *NC:* no scroll window: RED.
- **LLR-4303.16 — Event.** When `enter` is pressed in the list view, the system shall close the list view and select the cursor's task on its board (`open_on_board`).
  Threshold: cursor on a task of the open board → `app.selected_task_id` is its id and the list view is gone; 1/1. *NC:* `enter` unbound: RED.
- **LLR-4303.17 — Unwanted.** If the list holds no row, then the list view shall show `no tasks to list` in the list area.
  Threshold: 1/1 (all tasks archived, archived hidden). *NC:* blank: RED.
- **LLR-4303.18 — Unwanted.** If `enter`, `↑` or `↓` is pressed while the list holds no row, then the system shall leave the screen unchanged.
  Threshold: 0 exceptions, screen still the list view; 3/3. *NC:* index the empty list: IndexError: RED.
- **LLR-4303.19 — Ubiquitous.** The list view's key row shall show every key the view binds — `↑↓ move`, `↵ open on board`, `o newest/oldest`, `v archived`, `esc / N back` — fitted by `keymap.key_line` (words go first, keys never).
  Threshold: at 80x24 all 5 key glyphs present; at 118x30 all 5 words present; 2/2. *NC:* omit `v`: RED.
- **LLR-4303.20 — Unwanted.** If a title, project name, board name or note holds Rich markup (e.g. `[red]x[/red]`), then the list view shall draw it as literal text.
  Threshold: the literal `[red]x[/red]` appears in the list row and in the pane; 2/2. *NC:* `Text.from_markup(title)`: RED.

### 4.4 Order and inference (HLR-4304)

- **LLR-4304.1 — Ubiquitous.** The system shall take a task's added moment from its valid created when it has one.
  Threshold: a task with `created` and a birth record of another time → moment = `created`, source `c`; 1/1. *NC:* prefer history: RED.
- **LLR-4304.2 — Unwanted.** If a task has no valid created, then the system shall take its added moment from the `at` of its first birth record in its board's `history.jsonl`, with source `h`.
  Threshold: 2 birth records for one id → the first one's `at`; 1/1. *NC:* last record: RED.
- **LLR-4304.3 — Unwanted.** If a task has neither a valid created nor a birth record, then the system shall mark its added moment unknown, with source `?`.
  Threshold: 1/1. *NC:* use file mtime: RED.
- **LLR-4304.4 — Ubiquitous.** The system shall order dated rows by added moment, ties broken by board order and then file position.
  Threshold: 3 tasks on 2 boards with one equal moment → order matches the graph example (oldest first); 1/1. *NC:* ignore the tie-break: RED in 1 of 2 runs with boards swapped.
- **LLR-4304.5 — Ubiquitous.** The system shall place every unknown row before every dated row in oldest-first order, unknown rows ordered by board order and then file position.
  Threshold: oldest first → the 2 unknown rows are rows 0–1, in file order; 1/1. *NC:* unknown last: RED.
- **LLR-4304.6 — Ubiquitous.** The list view shall open newest first (the exact reverse of oldest first).
  Threshold: on open, row 0 is the newest stamped task; 1/1. *NC:* oldest first default: RED.
- **LLR-4304.7 — Event.** When `o` is pressed in the list view, the system shall reverse the order and put the cursor on the first row.
  Threshold: `o` → row 0 is the oldest unknown row and the cursor is 0; `o` again → newest first; 2/2. *NC:* keep the cursor index: RED.
- **LLR-4304.8 — Unwanted.** If a task's `created` is a `str` that `datetime.fromisoformat` rejects, then the system shall treat the task as having no valid created.
  Threshold: `created="not a date"` with a birth record → source `h`; without → `?`; 0 exceptions; 2/2. *NC:* crash on parse: RED.
- **LLR-4304.9 — Ubiquitous.** Each row's time label shall be the moment's `HH:MM` for source `c`, `≈HH:MM` for source `h` and `?` for source `?`.
  Threshold: 3/3 labels. *NC:* no ≈: RED.
- **LLR-4304.10 — Ubiquitous.** The detail pane's source line shall read `added <%a %b %d · %H:%M> · the created field` for source `c`, `added ≈ <%a %b %d · %H:%M> · from history.jsonl` for source `h`, and `added: unknown, before <first created date> · #<file position + 1> in <board name>'s board file` for source `?`.
  Threshold: 3/3 exact strings in the fixture. *NC:* omit `#n`: RED.
- **LLR-4304.11 — Unwanted.** If no listed task has a valid created, then the list shall head the unknown rows with `BEFORE ANY RECORD · ?`.
  Threshold: a board of 2 unknown tasks → the header string exact; 1/1. *NC:* `BEFORE NONE · ?`: RED.
- **LLR-4304.12 — Unwanted.** If reading a board's `history.jsonl` raises `OSError`, then the system shall infer that board's tasks with no birth records.
  Threshold: `history.read` monkeypatched to raise `PermissionError` → the view opens, those tasks are source `?` or `c`; 0 exceptions; 1/1. *NC:* unguarded read: RED.
- **LLR-4304.13 — Unwanted.** If an added moment carries a UTC offset, then the system shall compare it as the local naive time it denotes.
  Threshold: `created="2026-10-31T18:20:00+00:00"` sorted with naive moments: 0 exceptions, position equals that of its local-time equivalent; 1/1. *NC:* compare aware with naive: TypeError: RED.
- **LLR-4304.15 — Unwanted.** If no listed task has a valid created, then the detail pane's source line for source `?` shall read `added: unknown · #<file position + 1> in <board name>'s board file`.
  Threshold: 1/1 exact string. *NC:* `before None`: RED.
- **LLR-4304.14 — Ubiquitous.** The list view's head row shall name the order (`newest first` or `oldest first`), the row count and the legend `time = created  ≈ = history  ? = unknown`, clipped to the width.
  Threshold: at 118x30 the head holds `newest first` and the legend; after `o`, `oldest first`; 2/2. *NC:* fixed text: RED.

### 4.5 The state column (HLR-4305)

- **LLR-4305.1 — Ubiquitous.** The state column shall hold one box per phase of the task's board: `■` for every phase up to and including the task's phase, `□` for each later phase.
  Threshold: phases `Backlog Doing Review Done` → `■□□□`, `■■□□`, `■■■□`, `■■■■` (a done task all filled); 4/4. *NC:* exclusive fill: `□□□□` for Backlog: RED.
- **LLR-4305.2 — Unwanted.** If a board has more than 8 phases, then the state column shall hold 8 boxes with `ceil(8 × (index + 1) / phases)` of them filled.
  Threshold: 10 phases: index 0 → 1 filled, index 4 → 4, index 9 → 8; 3/3. *NC:* draw 10 boxes: RED.
- **LLR-4305.3 — Ubiquitous.** The state column shall be as wide as the widest board's box count among the listed rows, a shorter run padded with spaces on its right.
  Threshold: rows from a 3-phase and a 5-phase board: titles start in the same cell; 1/1. *NC:* no padding: RED.
- **LLR-4305.4 — Ubiquitous.** The state column shall draw filled boxes in `HEX["ink"]` and empty boxes in `HEX["dim"]`, and no other style.
  Threshold: the set of styles on state-column cells over the fixture ⊆ {ink, dim}; 1/1. *NC:* a phase hue: RED.

### 4.6 The archived toggle (HLR-4306)

- **LLR-4306.1 — State.** While archived tasks are hidden, the list shall omit every task whose `archived` is true.
  Threshold: 4 tasks, 1 archived → 3 rows; 1/1. *NC:* no filter: RED.
- **LLR-4306.2 — Ubiquitous.** The list view shall open with archived tasks hidden, whatever the main screen's `v` state is.
  Threshold: `app.show_archived = True`, then `N` → archived hidden; 1/1. *NC:* inherit `show_archived`: RED.
- **LLR-4306.3 — Event.** When `v` is pressed in the list view, the system shall toggle between hiding and showing archived tasks.
  Threshold: `v` → 4 rows, `v` → 3 rows; 2/2. *NC:* one-way: RED.
- **LLR-4306.4 — Event.** When the archived toggle changes, the system shall keep the cursor on the same task if it is still listed, else put it on the first row.
  Threshold: cursor on a live task, `v`, `v` → same task id; cursor on an archived task, `v` → row 0; 2/2. *NC:* reset to 0 always: arm 1 RED.
- **LLR-4306.5 — State.** While archived tasks are shown, the list shall draw each archived row's title in `HEX["dim"]`.
  Threshold: 1/1. *NC:* no dimming: RED.
- **LLR-4306.7 — State.** While archived tasks are shown and the cursor is on an archived task, the detail pane's meta line shall hold `archived`.
  Threshold: 1/1. *NC:* no word: RED.
- **LLR-4306.6 — Ubiquitous.** The head row shall end with `· <n> archived hidden` while archived tasks are hidden and `n > 0`, and with `· archived shown` while they are shown.
  Threshold: 2/2 strings. *NC:* no count: RED.

## 5. Acceptance tests (black-box, keys and dialogs)

- **AT-4301** — two boards in the registry (synthetic, 3 + 2 tasks, one with 4 phases): press `N`; the list shows 5 rows newest first with headers and state boxes; `o` → oldest first; `↓`; the pane follows the cursor; `esc` returns to the board. Board and history bytes unchanged (LLR-4302.6).
- **AT-4302** — on an old board: `a`, type a title, `alt+s`; `N` → the new task is row 0 with today's `HH:MM` and source `the created field`; the board file holds its `created`; every old task's entry is byte-identical to before (LLR-4302.5).
- **AT-4303** — `I`, pick a 3-task template; `N` → the three tasks are rows 0–2 with one same time label.
- **AT-4304** — one archived task: `N` → not listed, head `1 archived hidden`; `v` → listed, dimmed, head `archived shown`; `v` → hidden again.
- **AT-4305** — an old board with a `history.jsonl` birth record for one task and none for another, plus one stamped task: `N` shows `≈HH:MM` and `?`; the detail pane source lines read as LLR-4304.10; after `esc` the board file and history are byte-identical.

## 6. Slice of functions to change (named and counted)

| # | File | Unit | Change |
|---|---|---|---|
| 1 | models.py | `Task` dataclass: field `created` | changed |
| 2 | models.py | `_TASK_KEYS` + `Task.from_dict` (read `created`; non-`str` kept in `extra`) | changed |
| 3 | models.py | `Board._to_dict` (`created` written only when set) | changed |
| 4 | models.py | `Board.add_task` (stamp when `None`) + a `stamp()` helper | changed/new |
| 5 | models.py | `seed_data` / `Board.load` seed path (stamp seeded tasks) | changed |
| 6 | app.py | `_on_template_picked` (stamp inserted tasks) | changed |
| 7 | app.py | `action_added_list` + list screen (`AddedList`: compose, paint, move, order, archived, jump, back) | new |
| 8 | views.py | `added_rows(lanes, …)` (rows + inference), `added_order`, `state_boxes`, `render_added_list` | new |
| 9 | keymap.py | `KEYMAP` entry `N` | changed |

Unchanged on purpose (verified at E2): `_on_task_added` and `_create_and_link` (both reach
`Board.add_task`), `_on_task_edited`, `boards.move_project` (deepcopy keeps the field; history lines
already move), the undo re-insert, `_rescue_task`, `history.*`.
**Count: 9 units in 4 source files** (models.py, app.py, views.py, keymap.py) — within the 4-source-file budget.

## 7. Counts

US 1 · HLR 6 · LLR 63 (4301: 11, 4302: 6, 4303: 20, 4304: 15, 4305: 4, 4306: 7) · AT 5.

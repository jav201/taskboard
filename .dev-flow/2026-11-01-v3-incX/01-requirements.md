# Requirements — taskboard — Inc X, `x` in the presentation exports the HTML deck (dev-flow-v3-beta)

> Strict EARS (five forms only), ISO/IEC/IEEE 29148. One `shall` per requirement. Each carries a
> numeric pass threshold and a negative control (*NC*: a mutant that turns its test RED). Ids continue
> the repo's sequence in a fresh block: US-4501, HLR-4501..4506, LLR-4501.n..4506.n, AT-4501..4506.
> Range check (2026-11-01, `grep -rhoE "(HLR|LLR|AT|US)-45[0-9]{2}" REQUIREMENTS.md .dev-flow/ tests/`):
> no hit. `TC-45nn`/`TC-46nn` are taken by Inc K, so the TCs of this increment use `TC-47nn`.
> Base: `509d444` (branch `feat/present-x-html`, from `main` `2fbd5d2`). Commission:
> `.dev-flow/COMMISSION-present-x-html.md`, decisions X-1..X-4.
> **TC numbering:** LLR-4501.n → TC-(4700+n); LLR-4502.n → TC-(4720+n); LLR-4503.n → TC-(4730+n);
> LLR-4504.n → TC-(4740+n); LLR-4505.n → TC-(4750+n); LLR-4506.n → TC-(4760+n). A second test of one
> LLR adds a letter (TC-4703b).

## 1. Scope

**In:** `x` in `R` writes the HTML deck (report C) through the writer `H` → `c` uses, scoped to what
the presentation shows (X-1); the toast and its `o` offer inside `R`; the SVG/PNG export, its file
naming and its Edge rasteriser removed (X-2); `H` drawn in the main key bar and listed once in the `?`
help (X-3); the export wording in the presentation's `?` window and the README (X-2, X-4).
**Not in:** the presentation's frames, views, hint rows and every key but the new `o` (X-4); the deck
and workspace renderers and the extraction (`report_deck.py`, `report_workspace.py`, `report_html.py`)
— reused unchanged; `H`'s own modal and its outputs; the static CLI report (`report.py`, X-2).
No new dependency.

**Definitions.**

| Term | Meaning |
|---|---|
| deck | the HTML file `report_deck.render` produces (report C): cover, overview, one slide per project holding a task |
| presented board | the board `R` was opened on (the open board) |
| presented project | in views 1 and 2 (`gantt`, `split`), the project the screen shows |
| shown project | in view 3 (`all`), a visible (not archived) project whose `show_in_present` is true |
| shown task | a task of a presented or shown project that is not archived, whose `show_in_present` is true, and that is not a milestone of a hidden milestone class — the tasks the presentation's views draw, open and done |
| presentation order | `present_order` of the presented board: ranked projects first by rank, then the rest in board order |
| board slug | `report_html.slug` of the presented board's registry name (its label for an unlisted board) |
| offer | the single-use permission, live for 10 s after a written toast, for `o` to open that file |
| primary bar | the main screen's key bar in its default (`primary`) layer, as `keymap.key_bar_plain(w, view, "primary")` reads it |
| main views | `swimlanes agenda gantt kanban focus chainmap flow standup people setup` |
| `<date>` | today's date as `YYYY-MM-DD` |

## 2. Source user story

**US-4501.** As the board's owner (`username_subject`), I want `x` in the presentation to write the
HTML deck of exactly what I am presenting — nothing I hid — and offer to open it, and I want the
HTML report key `H` to be visible in the key bar, so that the export I reach for is the one I use and
the report I could not find is on screen. (Operator: «Vamos a eliminar el reporte svg, ya no le veo
sentido ahora, y quedémonos con el html.»)

## 3. High-level requirements

### HLR-4501 — `x` in `R` writes the deck of what the presentation shows
- **Traceability:** US-4501 · X-1
- **Ledger:** LED-2026-11-01-incX.1
- **Statement:** When `x` is pressed in the presentation, the system shall write the deck of the presentation's scope into the presented board's `reports/` folder.
- **Validation:** `test` — `tests/test_present_x_html.py` (pilot + layer 0)
- **Numeric pass threshold:** all LLR-4501.n thresholds.
- **Acceptance test(s):** AT-4501, AT-4502, AT-4505
- **Negative control:** base `x` writes an `.svg`: TC-4701 RED at base (no `deck-*.html`).

### HLR-4502 — what the presentation hides is not in the file's bytes
- **Traceability:** US-4501 · X-1
- **Ledger:** LED-2026-11-01-incX.1
- **Statement:** The system shall leave out of the deck's bytes every project and task the presentation does not draw.
- **Validation:** `test` — byte search over the written file
- **Numeric pass threshold:** 0 occurrences of every sentinel over LLR-4502.1..4502.6.
- **Acceptance test(s):** AT-4501, AT-4502
- **Negative control:** export the unfiltered board: TC-4721 RED.

### HLR-4503 — the toast names the file and offers `o`
- **Traceability:** US-4501 · X-1
- **Ledger:** LED-2026-11-01-incX.1
- **Statement:** When the deck is written from the presentation, the system shall name the file in a toast and let `o` open it for 10 s.
- **Validation:** `test` — pilot, `_report_clock` seam, `os.startfile`/`webbrowser.open` monkeypatched
- **Numeric pass threshold:** all LLR-4503.n thresholds.
- **Acceptance test(s):** AT-4503, AT-4504
- **Negative control:** `o` unbound in `R`: TC-4732 RED.

### HLR-4504 — the SVG/PNG export is removed
- **Traceability:** US-4501 · X-2
- **Ledger:** LED-2026-11-01-incX.1
- **Statement:** The system shall export the presentation in no format but the HTML deck.
- **Validation:** `test` + `inspection`
- **Numeric pass threshold:** all LLR-4504.n thresholds.
- **Acceptance test(s):** AT-4501, AT-4502
- **Negative control:** keep the `save_present_svg` call beside the deck: TC-4741 RED.

### HLR-4505 — `H` is discoverable
- **Traceability:** US-4501 · X-3
- **Ledger:** LED-2026-11-01-incX.1
- **Statement:** The system shall show the `H` key in the main screen's primary key bar and list it in the `?` help.
- **Validation:** `test` — layer 0 over `keymap.fit_bar` / `key_bar_plain`, pilot for `?`
- **Numeric pass threshold:** all LLR-4505.n thresholds at 80 and 118 columns.
- **Acceptance test(s):** AT-4506
- **Negative control:** base `H` has `bar=False`: TC-4751 0/20 RED at base.

### HLR-4506 — the wording says HTML, and nothing else of `R` changes
- **Traceability:** US-4501 · X-2 · X-4
- **Ledger:** LED-2026-11-01-incX.1
- **Statement:** The system shall describe the presentation's export as the HTML deck wherever it names the export.
- **Validation:** `test` + `inspection` (README)
- **Numeric pass threshold:** all LLR-4506.n thresholds.
- **Acceptance test(s):** AT-4506
- **Negative control:** base label `export this view · SVG + PNG`: TC-4761 RED at base.

## 4. Low-level requirements

### 4.1 Writing the deck (HLR-4501)

- **LLR-4501.1 — Event.** When `x` is pressed in view 1 or view 2 at a width of 36 columns or more, the system shall write the deck to `<board dir>/reports/deck-<board slug>-<project slug>-<date>.html`, where the project slug is `report_html.slug` of the presented project's name.
  Threshold: views 1 and 2 each → that file exists, its name exact; 2/2. *NC:* keep the `present-<slug>-<date>` stem: RED.
- **LLR-4501.2 — Event.** When `x` is pressed in view 3 at a width of 36 columns or more, the system shall write the deck to `<board dir>/reports/deck-<date>.html`.
  Threshold: 1/1 exact name. *NC:* a `-all` suffix: RED.
- **LLR-4501.3 — State.** While no task of the presented project is hidden, archived or a milestone of a hidden class, the deck `x` writes in view 1 or view 2 shall be byte-identical to the deck `H` writes with `c` and scope `p` for that project on the same day.
  Threshold: fixture board (2 projects, a done task, a milestone with a class, a dependency, notes with a mention), views 1 and 2 vs `H c p` → `bytes ==`; 2/2. *NC:* render with a board key other than the registry id (`#0`): RED.
- **LLR-4501.4 — State.** While the registry lists only the presented board and none of its projects or tasks is hidden, archived, ranked out of board order or without a project, the deck `x` writes in view 3 shall be byte-identical to the deck `H` writes with `c` and scope `o` on the same day.
  Threshold: 1/1 `bytes ==`. *NC:* pass `people={}` to the extraction: the mention renders as plain `@handle`: RED.
- **LLR-4501.5 — Ubiquitous.** The deck `x` writes in view 1 or view 2 shall hold the presented project as its only project, whatever that project's own `show_in_present` value.
  Threshold: board of 3 projects → 1 project slide, named the presented project, the other 2 names 0 occurrences; the same with the presented project's flag set false (hidden on view 3's rail); 2/2. *NC:* scope = every shown project: RED.
- **LLR-4501.6 — Ubiquitous.** The deck `x` writes in view 3 shall hold the shown projects in presentation order.
  Threshold: projects A, B, C with ranks C=0, A=1, B=2 → overview rows and project slides read C, A, B; 2/2 (overview, slides). *NC:* board order: A, B, C: RED.
- **LLR-4501.7 — Ubiquitous.** The deck `x` writes shall hold the presented board as its only board.
  Threshold: registry of 2 boards → the cover's board table has 1 row; the other board's name and its projects' names 0 occurrences; views 1 and 3; 2/2. *NC:* extract over every `board_lanes` board: RED.
- **LLR-4501.8 — Ubiquitous.** The deck `x` writes in view 3 shall hold a project folded with `enter` with all its shown tasks.
  Threshold: fold project B (`enter`), `x` → B's slide lists its 2 shown tasks; 1/1. *NC:* skip folded projects: RED.
- **LLR-4501.9 — Ubiquitous.** The deck `x` writes shall hold every shown task of each project it holds, open and done.
  Threshold: a project with 2 open and 1 done shown task → its slide reads `3 tasks` and the done title is present; views 1 and 3; 2/2. *NC:* open tasks only (view 3's frame population): RED.
- **LLR-4501.10 — Event.** When `x` writes the deck, the system shall leave the board file and its `history.jsonl` unchanged.
  Threshold: sha256 of both equal before and after `x` in views 1, 2, 3; 6/6. *NC:* a `board.save()` in the export: RED.
- **LLR-4501.11 — Unwanted.** If the presented board is not in the registry (opened with `--open`), then the system shall name the board in the deck and in the file name by the board's label name, or `this board` when the board has no label.
  Threshold: label `("Client A", "pink")` → the cover's board cell is `Client A` and the views-1 file is `deck-client-a-<project slug>-<date>.html`; no label → `this board` and `deck-this-board-…`; 2/2. *NC:* a registry lookup that raises on `bid None`: RED.
- **LLR-4501.12 — Unwanted.** If no project is shown in view 3, then the system shall write a deck whose overview slide reads `No project in this scope holds a task.`
  Threshold: every project hidden on the rail, `x` → the file exists and holds the sentence; 0 exceptions; 2/2. *NC:* return before writing on an empty scope: RED.
- **LLR-4501.13 — Unwanted.** If `x` is pressed while the presentation is narrower than 36 columns, then the system shall show the warning toast `Widen the terminal to 36+ columns to export`, titled `Present`.
  Threshold: 30 columns → the toast text exact; 1/1 (unchanged from base). *NC:* drop the narrow branch: RED.
- **LLR-4501.14 — Unwanted.** If `x` is pressed while the presentation is narrower than 36 columns, then the system shall write no file.
  Threshold: `reports/` absent after `x` at 30 columns; 1/1. *NC:* write before the width check: RED.

### 4.2 What stays out of the bytes (HLR-4502)

- **LLR-4502.1 — Ubiquitous.** The deck shall hold no task whose `show_in_present` is false.
  Threshold: a hidden task titled `HIDDEN-T-7Q` with id `hidt7q` → 0 occurrences of either string in the file's bytes, views 1, 2 and 3; 3/3. *NC:* extract from the unfiltered board: RED.
- **LLR-4502.2 — Ubiquitous.** The deck `x` writes in view 3 shall hold no project whose `show_in_present` is false, and none of its tasks.
  Threshold: a hidden project `HIDDEN-P-4K` with a shown task `UNDER-HIDDEN-P` → 0 occurrences of both; 2/2. *NC:* filter tasks only: RED.
- **LLR-4502.3 — Ubiquitous.** The deck shall hold no archived task, no task of an archived project and no task without a project.
  Threshold: sentinels `ARCH-T`, `ARCH-P-TASK`, `NO-PROJ-T` → 0 occurrences each, and no `Inbox` slide; views 1 and 3; 2/2 (each arm all 3 sentinels). *NC:* keep the extraction's Inbox row: RED.
- **LLR-4502.4 — Ubiquitous.** The deck shall hold no milestone whose class is hidden.
  Threshold: a milestone `HID-CLASS-MS` of a class hidden in `#` → 0 occurrences, views 1 and 3; 2/2. *NC:* filter by `present_tasks` instead of `present_tasks_m`: RED.
- **LLR-4502.5 — Ubiquitous.** The deck's legend shall list only the milestone classes of the tasks the deck holds.
  Threshold: a class `CLASS-ONLY-HIDDEN` used only by a hidden task → its name 0 occurrences; 1/1. *NC:* pass every class to the deck: RED.
- **LLR-4502.6 — Event.** When `x` is pressed, the system shall read the presentation's hide flags as they stand at that press.
  Threshold: `space` on a task in view 1, then `x` → that title 0 occurrences; `a`, then `x` → present; 2/2. *NC:* a scope captured when `R` opened: RED.

### 4.3 The toast and the offer (HLR-4503)

- **LLR-4503.1 — Event.** When `x` has written the deck, the system shall show the information toast `Report written: <file name>\n<folder>\no opens it (10 s)`, titled `Report`, for 10 s.
  Threshold: exact text, title and timeout; 1/1. *NC:* the old `Exported …` text: RED.
- **LLR-4503.2 — Event.** When `o` is pressed in the presentation while an offer is live, the system shall open the offered file with the operating system's default handler.
  Threshold: `os.startfile` (or `webbrowser.open` off Windows) monkeypatched → called once with the deck's path; 1/1. *NC:* `o` unbound in `R`: 0 calls: RED.
- **LLR-4503.3 — Unwanted.** If `o` is pressed in the presentation while no offer is live (none made, 10 s or more elapsed, or already used), then the system shall open nothing.
  Threshold: no `x` → 0 calls; `x`, clock + 10 s, `o` → 0 calls; `x`, `o`, `o` → 1 call in total; 0 exceptions; 3/3. *NC:* an offer with no expiry: arm 2 RED.
- **LLR-4503.4 — Unwanted.** If writing the deck raises `OSError`, then the system shall show the error toast `Report not (fully) written: <error>`, titled `Report`.
  Threshold: `reports` is an existing plain file (mkdir fails) → exact text; 0 exceptions; 1/1. *NC:* unguarded write: the screen crashes: RED.
- **LLR-4503.5 — Unwanted.** If writing the deck raises `OSError`, then the system shall withdraw any live offer.
  Threshold: a live offer from an earlier `x`, then a failing `x`, then `o` → 0 calls; 1/1. *NC:* keep the earlier offer: RED.
- **LLR-4503.6 — Unwanted.** If the operating system's handler fails to open the offered file, then the system shall show the error toast `Could not open the report <file name>.`
  Threshold: `os.startfile` raises `OSError` → exact text; 1/1. *NC:* swallow silently: RED.
- **LLR-4503.7 — Unwanted.** If the file name or the folder holds Rich markup, then the system shall show it in the toast as literal text.
  Threshold: board folder named `[red]rx[/red]` → the toast's plain text holds `[red]rx[/red]`; 1/1. *NC:* `markup=True`: RED.

### 4.4 The SVG/PNG export removed (HLR-4504)

- **LLR-4504.1 — Ubiquitous.** The presentation's export shall write exactly one file, an `.html`.
  Threshold: `reports/` after `x` in views 1, 2 and 3 holds 0 `.svg`, 0 `.png` and 0 `present-*` files; 3/3. *NC:* keep the `save_present_svg` call: RED.
- **LLR-4504.2 — Ubiquitous.** The presentation's export shall start no external process.
  Threshold: `subprocess.run` and `subprocess.Popen` monkeypatched to raise → `x` in views 1, 2 and 3 writes the deck; 0 calls; 3/3. *NC:* keep the Edge rasteriser: RED.
- **LLR-4504.3 — Ubiquitous.** The package shall hold no code that writes the presentation frame as an SVG or rasterises it.
  Threshold: inspection `grep -rnE "save_svg|msedge|--screenshot|present_paths|present_all_export" taskboard/*.py` → 0 hits; 1/1. *NC:* leave `views.save_present_svg` defined: 1 hit: RED.

### 4.5 `H` in the key bar and the help (HLR-4505)

- **LLR-4505.1 — Ubiquitous.** The primary bar shall show the key `H` in every main view at 80 and at 118 columns.
  Threshold: 10 views × {80, 118} → `H` among the drawn keys; 20/20. *NC:* `bar=False` (base): 0/20 RED.
- **LLR-4505.2 — Ubiquitous.** The primary bar shall draw every key, and the same overflow count, it draws at base in each main view at 80 and at 118 columns.
  Threshold: base key set ⊆ new key set and `dropped` equal; 20/20. *NC:* promote every global key (`R A N n @ # I S`) to the bar too: 10/20 RED.
- **LLR-4505.3 — Ubiquitous.** The primary bar shall lose at most one word, of those it draws at base, in each main view at 80 and at 118 columns.
  Threshold: 20/20 cases with ≤ 1 word lost. *NC:* declare `H` universal (sorted first, keeping its word): 7/20 cases lose 2+ words: RED.
- **LLR-4505.4 — Ubiquitous.** The primary bar shall draw `H Report` when the bar has room for every entry with its word.
  Threshold: width 250, view `swimlanes` → `H Report` in the plain bar; 1/1. *NC:* an empty label: RED.
- **LLR-4505.5 — Ubiquitous.** The `?` help shall list `H` with the word `Report` exactly once.
  Threshold: over the Keys band and the global line, 1 entry `H Report` in each of the 10 main views; 10/10. *NC:* `H` in both the band and the global line: 2: RED.

### 4.6 Wording, and the rest of `R` unchanged (HLR-4506)

- **LLR-4506.1 — Ubiquitous.** The presentation's `?` window shall name `x` with the words `export this view · HTML deck`.
  Threshold: the window's text holds that row; `SVG` and `PNG` 0 occurrences in the window; 2/2. *NC:* base label: RED.
- **LLR-4506.2 — Ubiquitous.** The presentation's `?` window shall name `o` with the words `open the last export (10 s)`.
  Threshold: 1/1 row. *NC:* a bound `o` missing from `PRESENT_KEYS`' window rows: RED.
- **LLR-4506.3 — Ubiquitous.** The presentation shall bind exactly the keys it binds at base plus `o`.
  Threshold: the set of `PresentScreen` binding keys = base set (`1 2 3 tab shift+tab up,k down,j left,h right,l pageup pagedown space a u shift+up,K shift+down,J enter x escape,q question_mark`) ∪ {`o`}; 1/1. *NC:* `o` bound but `K`/`J` lost in the edit: RED.
- **LLR-4506.4 — Ubiquitous.** The presentation's hint row shall read exactly what it reads at base, in every view.
  Threshold: views 1, 2, 3 × widths {130, 118, 100, 80, 60, 36}, hidden count 0 and 2 → plain text equal to base; 36/36. *NC:* add `o open` to the hint: RED.
- **LLR-4506.5 — Ubiquitous.** The README shall describe the presentation's export as the HTML deck and name neither SVG nor PNG as its format.
  Threshold: inspection over `README.md` minus its `<img` lines → 0 matches of `SVG|PNG`; the `R` key-table row holds `HTML deck`; `tests/test_keymap.py::test_the_readme_keybinding_table_matches_the_seat` GREEN; 3/3. *NC:* base README (lines 140, 189, 291, 410): RED.

## 5. Acceptance tests (black-box, keys and dialogs)

- **AT-4501** — views 1 and 2. A registry of 2 boards; the open board has 2 projects; a task of the presented project titled `HIDDEN-T-7Q`. `R`, `space` on that task, `x` → the toast reads `Report written: deck-<board slug>-<project slug>-<date>.html` …; the file exists; `HIDDEN-T-7Q`, the other project's name and the other board's name 0 occurrences; `reports/` holds no `.svg`/`.png`; the board file's sha256 equal before and after `x`. `2`, `x` → the same file, rewritten. (LLR-4501.1, .5, .7, .10; LLR-4502.1, .6; LLR-4504.1)
- **AT-4502** — view 3. Projects A, B, C. `R`, `3`; on the rail `K` until C is first; `space` on B (hidden); `enter` folds A on the timeline; `x` → `deck-<date>.html`; overview and slides read C, A; B's name 0 occurrences; A's slide lists all its shown tasks. (LLR-4501.2, .6, .8; LLR-4502.2)
- **AT-4503** — the offer. `R`, `x`, `o` → the OS handler (monkeypatched) gets the deck's path once; `o` again → no second call; `x`, the clock moved 10 s, `o` → no call. (LLR-4503.1..4503.3)
- **AT-4504** — the failure. `reports` exists as a plain file. `R`, `x` → `Report not (fully) written: …`; `o` → no call; the presentation still answers `esc`. (LLR-4503.4, .5)
- **AT-4505** — narrow. The terminal at 30 columns: `R`, `x` → `Widen the terminal to 36+ columns to export`; no `reports/` folder. (LLR-4501.13, .14)
- **AT-4506** — discoverability and wording. At 118x30 and 80x24 the main key bar shows `H`; `?` → the help lists `H Report` once; `esc`, `H` → the report modal opens (unchanged). `R`, `?` → the window lists `x export this view · HTML deck` and `o open the last export (10 s)`. (LLR-4505.1, .5; LLR-4506.1, .2)

## 6. Slice of functions to change or remove (named and counted)

| # | File | Unit | Change | Requirements |
|---|---|---|---|---|
| 1 | app.py | `PresentScreen.action_export` | rewritten: the deck of the scope through `report_html.extract` + `write_reports(…, ("deck",), …)`; the narrow branch kept | LLR-4501.1–.14, LLR-4502.6, LLR-4503.1, .4, .5, LLR-4504.1, .2 |
| 2 | app.py | `PresentScreen.action_open_export` (`o`) | new: takes the app's offer, else nothing | LLR-4503.2, .3, .6 |
| 3 | app.py | `TaskboardApp._on_report_chosen` | changed: its write → toast → offer tail becomes one shared method both `H` and `x` call | LLR-4501.3, .4, LLR-4503.1, .4, .5, .7 |
| 4 | app.py | module imports from `views` (drop `present_paths`, `save_present_svg`, `save_present_png`, `present_all_export`); `PresentScreen` docstring | changed | LLR-4504.3 |
| 5 | views.py | `present_deck_boards(board, project_id \| None)` — the presented board filtered to the shown projects (presentation order) and shown tasks, never saved | new | LLR-4501.5–.9, LLR-4502.1–.5 |
| 6 | views.py | `present_paths` | removed | LLR-4504.3 |
| 7 | views.py | `save_present_svg` | removed | LLR-4504.1, .3 |
| 8 | views.py | `_find_msedge` | removed | LLR-4504.2, .3 |
| 9 | views.py | `save_present_png` | removed | LLR-4504.2, .3 |
| 10 | views.py | `present_all_export` | removed | LLR-4504.3 |
| 11 | views.py | `_all_timeline` parameter `anchor` (its only caller is `present_all_export`) and the now-unused imports `os`, `shutil`, `subprocess` | changed (E2 confirms no other user) | LLR-4504.3 |
| 12 | keymap.py | `KEYMAP` entry `H`: `bar=True`, `primary=True`, declared after `↑` so it is the primary layer's last entry | changed | LLR-4505.1–.5 |
| 13 | keymap.py | `PRESENT_KEYS`: the `x` row's words; a new `o` row (`open_export`, group `OUT`) | changed | LLR-4506.1–.3 |
| — | README.md | lines 140, 189, 291, 410 (docs, not a source file) | changed | LLR-4506.5 |
| — | .dev-flow/BACKLOG.md | items on the SVG/PNG export (lines 284, 298, 326 at base) closed as obsolete, citing the commission (process record) | changed | X-2 |

**Count: 13 units in 3 source files** (app.py, views.py, keymap.py) — 5 removed, 2 new, 6 changed;
within the 4-source-file budget. `report_html.py`, `report_deck.py`, `modals.py` unchanged on purpose.

**Tests the removal touches (for E4, justified one by one in the packet):** `tests/test_present.py`
(~185), `test_present_all.py` (~488, ~697), `test_present_backlog_round.py` (~64, 144–145, 233–308),
`test_present_room.py` (~56), `test_present_views_app.py` (~240, 320–323), `test_tick_label.py`
(~51, ~251), `test_legend.py` (587–762), `test_present_hide.py` (~370), `test_present_narrow.py` (~242),
`test_present_note_highlights.py` (~211), `test_present_polish.py`, `test_markup_census.py` (a census
row naming the `x` export); any key-bar test that pins `H` as `bar=False`.

## 7. Counts

US 1 · HLR 6 · LLR 40 (4501: 14, 4502: 6, 4503: 7, 4504: 3, 4505: 5, 4506: 5) · AT 6.

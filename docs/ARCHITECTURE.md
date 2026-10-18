# Architecture — module map — taskboard

> **Artifact language.** Canonical **English scaffold**; generate in the project's language.

> **Owed in.** `core` by trigger · `full` ✓
> **No reserved-field block.** What a rule reads out of this artifact is `V8`'s `` `path/**` `` **globs** — paths, not words — so there is no label here for a translation to lose (the population and its reasons live in `LANG RESERVED-population-closed`).
> **Source:** `/dev-flow-init` step 4's seed-by-level table, which is this fact's one home. A level marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Home: the REPO** (`docs/ARCHITECTURE.md`), versioned beside the code — **not** the vault. It is the
> **oracle** the A-family triggers read: from a document store no mechanical check could open it.
> It is a **standing project artifact**, not a per-batch one: batches amend it, they do not recreate it.

> **Distilled from IEEE 1016 by one selection rule: a viewpoint enters this map only if it FEEDS A
> TRIGGER.** In: **Composition** (A1/A2 + the source-file budget) · **Dependency** (A3 + parallelisation)
> · **Interface** (A3 + output-then-consume) · **Context** (the security family). Out — they belong in
> the design proposal, and only when they apply: Logical · Information · Patterns · Structure ·
> Interaction · State Dynamics · Algorithm · Resource. Keeping the other eight out is deliberate: a map
> that tries to describe everything stops being checkable, and a map that is not checkable is prose.

| Field | Value |
|---|---|
| Last amended by | `2026-10-18-batch-02` |
| Date | `2026-10-18` |

---

## 1 · Context — the system boundary

taskboard is a local, single-user terminal app. Everything it touches crosses one of these lines.

| External actor / service | Direction | What crosses | Notes |
|---|---|---|---|
| the operator's terminal | in / out | key presses, the painted screen | Textual; the only interactive surface |
| the board file `board.json` (default `~/.taskboard/board.json`) | in / out | projects, tasks, settings | read at mount, written on every mutation (`Board.save`); a corrupt file is quarantined |
| the board's `reports/` folder | out | presentation SVG/PNG, the HTML report | `views.present_paths`, `report.py` |
| `history.jsonl` beside the board | out | the transition log | `history.py` |
| a shared team folder (`team.json`, `user-*.json`) | in / out | team projects' tasks | `team_sync.py`; personal tasks never leave |
| Microsoft Edge (headless) | out | the SVG to rasterise | `views.save_present_png`; absent → SVG only |
| the clipboard | in | text, images | the editors' paste |

---

## 2 · Composition — the modules

| Module | Paths it owns | What it encapsulates | What it EXPOSES | What does NOT belong to it |
|---|---|---|---|---|
| `taskboard` (the shipped package) | `taskboard/**` | the whole application; its layers are the next table | `main`, `TaskboardApp` | tests, tooling, prototypes |
| `tests` | `tests/**` | the suite | — | shipped code |
| `tools` | `tools/**` | repo tooling (the privacy hook, sweeps) | — | shipped code |
| `docs` | `docs/**` and the `*.md` files at the root | project documentation | — | code |
| `dev-flow record` | `.dev-flow/**`, `.fast-dev-flow/**` | the batch records and their evidence | — | shipped code |
| `prototypes` | `prototypes/**`, `_prototypes/**`, `_tui_prism_proposal/**` | throwaway prototype rounds and their captures | — | shipped code (nothing in `taskboard/` imports them) |
| `packaging` | `.githooks/**`, `.github/**`, `.claude/**`, `.s19tool/**`, `build/**`, `taskboard.egg-info/**` and the root files `pyproject.toml`, `requirements.txt`, `.gitattributes`, `.gitignore`, `wezterm.lua`, `debug-*.log` | install, repo settings, local build output | — | code |

**The layers of `taskboard/**`** — one file belongs to exactly one layer. These are the units the A-family triggers count ("touches ≥2 modules" counts layers), and the dependency and interface tables below are written over them. They are listed by file because the package is flat; the glob above is the mechanical claim (`V8`).

| Layer | Files | What it encapsulates | What it EXPOSES | What does NOT belong to it |
|---|---|---|---|---|
| `models` | `models.py`, `history.py` | the board's data, its JSON (de)serialisation, its pure queries, the transition log | `Board`, `Project`, `Task`, `Board.load/save`, the query functions | any markup, any widget, any key |
| `views` | `views.py`, `wave.py`, `ribbon.py` | every board render: pure functions from a `Board` (+ size, today, view state) to Rich markup / `Text` | `render_view`, `render_present`, the gantt/kanban/chainmap renderers, `legend_entries`, `help_usage`, the export writers | reading keys, mutating the board, Textual widgets |
| `keymap` | `keymap.py` | the one key seat: every binding of the main screen and the modals (`PresentScreen.BINDINGS` excepted, §5), the key bar, the palette list | `KEYMAP`, `Key`, `app_bindings`, `bar_keys`, `palette_commands`, `fit_bar`, `KeyBar` | actions themselves, help copy |
| `modals` | `modals.py` | the modal screens (editors, pickers, help, standup) | `TaskModal`, `ProjectModal`, `HelpModal`, `CommandPalette`, … | the main screen, board persistence policy |
| `app` | `app.py`, `__main__.py`, `__init__.py`, `taskboard.tcss` | the Textual application: actions, the undo stack, the screens it pushes (`PresentScreen`), saving after mutations | `TaskboardApp`, `PresentScreen`, `main` | rendering a board (that is `views`), declaring a key (that is `keymap`) |
| `team_sync` | `team_sync.py` | the shared-folder push/pull | `TeamSync` (`foreign_tasks`, `probe_setup_health`, `sync_tone`) | the board's own file |
| `report` | `report.py` | the HTML report | `build_report` | the presentation |

**Staleness rule — the map checks itself.** A touched file that falls under **no** declared module means this map is out of date: **ARQ fires on its own** and the map is amended before requirements are derived.

- **Every path in the tree is claimed by exactly one module.** Overlapping prefixes are a defect of this document, not an ambiguity to be resolved case by case.

---

## 3 · Dependency — who may reach whom

| Module | Depends on | Forbidden direction | Why the ban exists |
|---|---|---|---|
| `models` | — | `models` → anything in the package | the data layer is loadable and testable alone; `team_sync` and the report read it |
| `views` | `models`, `team_sync` (`sync_tone` at module level, `probe_setup_health` function-local — the two import each other, one direction at function scope only) | `views` → `app`, `modals`, `keymap` | renders are pure functions; the oracle frames are byte-tested without an app |
| `keymap` | `views` (colours) | `keymap` → `app`, `modals` | the seat is read by the app and the modals, never the reverse |
| `modals` | `models`, `views`, `keymap` | `modals` → `app` at import time (a local import inside an action is tolerated: `HelpModal.action_map`) | the app pushes modals; a modal importing the app would cycle |
| `app` | every module above | — | the top of the graph |
| `team_sync` | `models`; `views.HEX` function-local only (`team_sync.py:48`, local to dodge the import cycle — tolerated like `modals` → `app`) | `team_sync` → `app`; `team_sync` → `views` at import time | it runs headless on a timer |
| `report` | `models`, `views` | — | — |
| `prototypes` | `taskboard` — public AND private names (`_present_ruler`, …) | `taskboard` → `prototypes` | a prototype round is frozen evidence tied to the commit it ran on; a later batch may delete a private name it imports (2026-10-17-batch-01 broke `present_rulers/proto.py`, 2026-10-18-batch-01 `present_rulers/app_capture.py` and `present_views/views_proto.py`, and with them the files that import them: `present_views/views_d.py`, `app_capture.py`, `app_capture2.py`), and a batch that re-runs one as a cross-check binds the missing names itself (`.dev-flow/2026-10-18-batch-01/evidence/gen_frames.py`); a round file that no longer runs says so in a `HISTORICAL` header naming the last commit it ran on, and is not repaired (2026-10-18-batch-02). A round that shows variants of literals (a tone, a wording, a cap) replaces, in its own process only, whole functions and methods with forked copies it holds (`prototypes/backlog_polish/` rebinds `taskboard.app.render_present` — `app` binds the name at import — `PresentScreen._hint`, and the private `views._present_cut` that `render_present` calls); the forks are frozen to the commit the round ran on, like its imports, and never reach `taskboard/`. Rejected: lifting the literals into module constants of `views`/`app` so a round can patch them — a production change made for a prototype |
| `tests` | `taskboard`; `prototypes` and `.dev-flow/**` evidence as FILES only (the oracle frames, a round's captures and page — `tests/test_present_views.py`, the round acceptance test of 2026-10-18-batch-02) | `taskboard` → `tests` | the suite reads artifacts; nothing shipped reads the suite |

---

## 4 · Interfaces — the contracts between modules

| Interface | Owner module | Consumers | Shape | Frozen? |
|---|---|---|---|---|
| `board.json` task record | `models` | `team_sync` (pushes `Board._to_dict`, `team_sync.py:157`; pulls through `Task.from_dict`, `:221`, into `foreign_tasks` for the team views only — a pulled task never joins the board, so a teammate's `show_in_present` never hides anything in this board's presentation), every older/newer app version (unknown keys round-trip through `extra`) | one JSON object per task; optional keys omitted when at their default only where the model says so (`show_in_present`, batch 2026-10-16-batch-01) | no |
| `Task` fields | `models` | `app` (`_on_task_edited` sets editor keys by name, `_UNDO_FIELDS`), `views`, `modals` | dataclass attributes | no |
| `render_present(board, project_id, cursor_id, today, width, height, view="gantt", scroll=0) -> Text` | `views` | `app.PresentScreen` (paint, export, the scroll clamp), tests, prototypes | a `height`×`width` `Text` for every `width` ≥ 0 (the screen passes `self.size.width or 0`): from `PRESENT_MIN_WIDTH` (36, the narrowest frame whose gantt field keeps one cell) the views' frame, below it one `mut` line — the longest rung of `PRESENT_NARROW` (`widen to 36+ columns · esc leave` … `36+`) that fits, cut with `…` when none does; every row empty at width 0 — and blank rows, ignoring `view`, `scroll` and the cursor (batch 2026-10-18-batch-02); `view` one of `PRESENT_VIEWS` (`gantt`, `split`), `scroll` a page number, read by `split` only (batch 2026-10-18-batch-01) | no |
| `PRESENT_MIN_WIDTH` | `views` | `app.PresentScreen` (below it no key but `esc`/`q` acts, `x` notifies instead of exporting, the hint shows `esc leave`), tests | `36`, an `int` (batch 2026-10-18-batch-02) | no |
| `PRESENT_VIEWS` | `views` | `app.PresentScreen` (the view keys, the hint row), tests | `("gantt", "split")`, the view names in key order | no |
| `present_paths(board, project_name, today=None, view="gantt")` | `views` | `app.PresentScreen` (export), tests | `(svg, png)` paths in `reports/`; a view other than `gantt` adds `-<view>` to the name | no |
| `present_tasks(board, project_id)` / `present_hidden(board, project_id)` | `views` | `app.PresentScreen` (reads `[0]`) | `present_tasks` → `tuple[list[Task], list[Task]]` (shown open by due, shown all), `present_hidden` → `list[Task]`, gantt order | no |
| `present_span_label(start, due) -> str` | `views` | `views.render_present`, tests | the field-row chip text | no |
| `present_note_lines(notes, w) -> list[tuple[str, str]]`, `present_alloc(ns, cur, room, floor_n=2) -> list[int]` | `views` | `views.render_present`, tests | `(lead, text)` note rows that fit `w`; note rows per task (batch 2026-10-18-batch-01) | no |
| `gantt_day_row(ax, today, echo, *, shade_weekends=True)` | `views` | `views` (the gantt view, the presentation) | list of cell markup + meta | no |
| `KEYMAP`, `bar_keys`, `global_keys`, `palette_commands` | `keymap` | `app` (bindings), `modals.HelpModal`, `modals.CommandPalette` | tuples of `Key` | no |
| `TaskModal` result dict | `modals` | `app._on_task_added` / `_on_task_edited` | `{field: value}` keyed by `Task` field names; `_on_task_added` pops `milestone`, `_on_task_edited` pops `archived`/`milestone`/`start_date`/`due_date` and routes `phase` through the board; every other key (the new `show_in_present` among them) is applied by `setattr` | no |

- **Changing one of these is trigger A3** — it fires ARQ, PDR *and* DDR, and it is never done inside a lane.

---

## 5 · Rationale — the decisions, and why

| Decision | Alternative rejected | Re-open when |
|---|---|---|
| renders live in `views` as pure functions over a `Board` | rendering inside widgets | a render needs live widget state it cannot take as an argument |
| the key seat is one tuple (`KEYMAP`) and the help/bar/palette derive from it | per-screen binding lists | a screen needs a key the seat cannot express |
| optional board keys are omitted at their default when byte-identity of existing boards matters | always writing every field (`asdict`) | a consumer needs the key present to tell "default" from "unknown" |
| the presentation lives in `app` (`PresentScreen`) beside the main screen, not in `modals` | moving it to `modals` | `app.py` is split |
| the presentation's views are one renderer with a `view` argument in `views`; the screen holds only the view index and the scroll offset, never persisted (batch 2026-10-18-batch-01) | a renderer function per view; remembering the last view in `settings` | a third view needs state the renderer cannot take as an argument, or the operator asks for the view to be remembered |
| the presentation's own keys (`1`/`2`, `tab`, `pgdn`, …) are `PresentScreen.BINDINGS`, outside `KEYMAP`, like its shipped `←→`/`space`/`a`/`x` | adding them to the `KEYMAP` seat | the `?` help or the palette must list the presentation's keys |

# Requirements Document — taskboard — Batch 2026-10-02-batch-04

> Live contract (current state only). Mode `core`. Language `en`. The append-only ledger is
> `01-requirements-ledger.md`. Template: flow `templates/req-template.md` (reserved field
> names kept literal). Ids use a batch-disjoint `4xx` range (`US-401`, `HLR-401`,
> `LLR-401.1`, `AT-401`, `TC-401`): `0xx`..`3xx` are taken in the record and the canon.
> Iteration 3; P2 iterations 1–3 folded (iteration 1 under the operator's rulings of 2026-10-03, `PLAN.md`).

## 1. Introduction

### 1.1 Purpose
Batch S (hardening), inserted between Batch A and Batch B of the `kg_mejoras` plan. Pre-existing
defects carried in `BACKLOG.md` and found at this batch's P2: user or synced text handed to a markup
parser kills the screen, vanishes, or (security S-1, HIGH) carries a clickable app action from a
teammate's `team.json` (S1, S-5, S-1, S-3, S-4); control bytes in a board or a teammate's file reach
the terminal (S2, L1); the task details' info grid paints blank.

### 1.2 Scope
In: every site in `taskboard/modals.py` and `taskboard/app.py` that hands a value to a Textual
markup sink or to a markup parser, user text there built as Rich `Text` pieces (operator ruling 2,
"Piezas de texto, sin formato"), with a census test that derives the site population from the
code; synced project fields validated as loading validates them (ruling 1, "Sí, dentro de S");
control-byte stripping of every string read from the board file at load, from `team.json` /
`board.<user>.json` at sync and from the clipboard, with one rule; the details view's info grid.
Out: the board renderers in `views.py` (but for the one highlight tokeniser both seats read, D-411) — their own seat (Rich markup built with `escape`, where
`collapse_runs` S-2 lives) is not this batch's (D-405); text typed in a session (an `Input` cannot
type a control byte; pasted text passes the clipboard rule) and OS paths and exception text, which
are not stripped but reach the screen only as `Text` pieces or `markup=False` toasts; legacy
`history.jsonl` records (D-409); Unicode format characters (bidi overrides, zero-width — S-9); every
other `BACKLOG.md` item.

### 1.3 Definitions
| Term | Definition |
|------|------------|
| markup sink | a Textual API that parses a `str` as Textual markup: the first markup parameter of a widget constructor (`content`, `label`, `prompt`, Select `options` prompts), a `tooltip=` keyword, `notify` with markup on, `Static.update`, `OptionList.add_option(s)` / `replace_option_prompt*`, `Select.set_options`, `border_title` / `border_subtitle` / `tooltip` |
| markup parser | `Text.from_markup`, `Content.from_markup`, `rich.markup.render`, `Text.from_ansi`, the helper `modals._rich`, and any name bound to one of them |
| markup-inert value | an app literal `str` (a literal, or literals joined by `+` / chosen by `if`), a Rich `Text` built without a parser (`Text(...)`, `Text.assemble(...)`, a name bound to one), a parser call over an app literal, a call by its bare name (or as `self.<method>` of its own class) of a function annotated `-> Text`, defined in a censused module, whose every `return` is itself markup-inert (P3 code review F1), or — for `notify` — any `str` with `markup=False` |
| user or synced text | text the app did not write: a task title, notes, URL or image reference, a project or phase name or status, a roster name or id, a typed id or name, a file path, an exception message |
| payload set | `[LINK=http://e]x` (a Textual tag Rich's `escape` leaves alone, P-1), `x\\\` (a run of three trailing backslashes, which turns the app's closing tag into text under `_rich`, S-4), `:smile: [b]y[/b]` (a Rich emoji code and a Rich tag, S-4); for a file path, a directory named `a[B]x` and one named `[B]x` |
| control byte | C0 (U+0000–U+001F) except tab and newline, DEL (U+007F), C1 (U+0080–U+009F) |

### 1.4 References
`BACKLOG.md` "Security S1, the remaining sites (MEDIUM)", "Security S2 (LOW)", "`TaskDetails`
info grid paints blank (pre-existing)", "Titles carry terminal escape sequences" (L1), "`app.py`
notifies prompt-typed ids and exceptions with markup on" (S-5), "`collapse_runs` can join two
adjacent same-style escaped pieces" (S-2); the plan `prototypes/kg_mejoras/IMPLEMENTATION-PLAN.md`
§Batch S (worktree `kg-mejoras`); `02-review.md` iteration 1 (findings Q-, A-, S-, UX-); the shipped
seat `modals._rich`; `tests/test_details_markup.py` (HLR-005 of `2026-09-30-batch-01`).

## 2. Overall description

### 2.1 Product perspective
Text reaches the screen two ways: the board renderers build Rich `Text` from escaped markup in
`views.py` (out of scope), and the modals, pickers and notifications in `modals.py` / `app.py` hand
values to Textual — the seat of S1. Text enters the app through four doors: `Board.load`, team
sync's `_read_json`, the Setup view's own read of `team.json` (`app.py`, A-3) and the clipboard —
the seats of S2. Synced project fields reach the board through `apply_config_to_board` — the seat
of S-1/S-3.

### 2.3 User characteristics
One operator at a terminal (80×24 up to full screen, keyboard first); in team mode, teammates
whose files arrive through a shared folder.

### 2.4 Constraints
Textual 8.2.8, Rich 15.0.0, Python 3.12; no new dependency; the board file format unchanged.

### 2.5 Assumptions
- A1: a teammate's file is untrusted input (team mode, `team_sync.py` docstring).
- A2: the census's sink set is Textual's as of 8.2.8 (§1.3); a Textual upgrade re-runs P-6.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-401 | As a taskboard user, alone or in a team, I want every title, name, id, path or message a dialog, picker or notification shows to appear exactly as written, so that text with square brackets, backslashes or colons — mine or a teammate's — never kills the screen, vanishes or changes. | BACKLOG S1 + S-5; plan §Batch S; P2 S-4 | READY |
| US-402 | As a taskboard user, I want control bytes in my board file, a teammate's synced file or the clipboard removed when they come in, so that no task text can drive my terminal, while tabs and newlines survive and a board file holding no control byte round-trips unchanged. | BACKLOG S2 + L1 | READY |
| US-403 | As a taskboard user opening a task's details (`enter`), I want its Project, Phase, Priority, Start and Due fields painted, so that I can read them. | BACKLOG (pre-existing) | READY |
| US-404 | As a team member, I want a teammate's `team.json` to be unable to put an action, an unknown colour or a non-text name into my board, so that a shared folder cannot run anything in my app or crash its views. | P2 security S-1 (HIGH), S-3; operator ruling 1 | READY |

#### Refinement log

**US-401 — user text never meets a markup parser**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality:** dialogs, pickers and toasts paint user and synced text exactly; out of scope = the Rich-built board views.
- **Feasibility:** `Text` pieces (`Text.assemble`, `Text.append`) and `notify(markup=False)`; the census measured 45 unsafe sites in `modals.py` (34) and `app.py` (11) under the first rule (P-8) plus the `_rich` sites over user text (P-11). Fits one increment of 2 SOURCE files.
- **Evaluability:** for each reachable site (§5.1) and each payload of the set, the screen stays up and paints the payload exactly.
- **Classification:** READY.

**US-402 — control bytes stripped at the doors**
- **INVEST:** all ✓.
- **Evaluability:** a board file whose title, notes, project and phase hold ESC and C1 opens with those bytes gone from the screen and from the parsed next save; a teammate's dirty board reaches a second user clean through the app's own save and push; a clean file round-trips through the app byte-identical.
- **Classification:** READY.

**US-403 — the info grid paints**
- **INVEST:** all ✓.
- **Evaluability:** `enter` on a task paints `Project`, `Phase`, `Priority`, `Start`, `Due` and their values inside the details box; a long value wraps rather than being cut (base: 0-row cells, P-5).
- **Classification:** READY.

**US-404 — a shared config cannot act**
- **INVEST:** all ✓.
- **Evaluability:** a `team.json` whose project status is `[@click=app.pwn]X`, colour `evil` and name `123` is applied: the project picker shows a valid status and clicking its line fires no action; every view renders (base: the click ran the action; gantt raised `KeyError`, P-12).
- **Classification:** READY.

RC-1 (b), already shipped? — none: on `origin/main` = `56a1b10` the census flags 45 sites (P-8), `Board.load` keeps ESC (P-3), sync keeps it (P-4), the grid paints 0-row cells (P-5), a synced status fires an action (P-12).

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | `Label(escape("[LINK=http://e]x"))` raises `MarkupError` in textual 8.2.8, and `escape` leaves the payload unchanged | premise | ✅ TRUE | `evidence/p0-probes.txt` §P-1 | HLR-401 |
| P-2 | `modals._rich` over the escaped payload builds a `Text` whose plain is the payload | premise | ✅ TRUE | `p0-probes.txt` §P-2 | superseded as fix form by ruling 2 (P-11) |
| P-3 | `Board.load` keeps ESC, BEL and C1 bytes in task text | premise | ✅ TRUE | `p0-probes.txt` §P-3 | HLR-402 |
| P-4 | `TeamState.foreign_tasks` keeps ESC in a teammate's title | premise | ✅ TRUE | `p0-probes.txt` §P-4 | HLR-402 |
| P-5 | The shipped `.modal-grid Label` rule paints a Label-only grid with 0-row cells | premise | ✅ TRUE | `p0-probes.txt` §P-5; `evidence/p1-grid-minimise.txt` | HLR-403 |
| P-6 | A Rich `Text` in `Label`, `Option`, a `Select` prompt and a `Button` paints the payload literally (4 of 4) | premise | ✅ TRUE | `p0-probes.txt` §P-6 | LLR-401.1 fix forms (C-15 identity: these sinks accept `Text`) |
| P-7 | In the app, `notify(payload, markup=False)` paints a toast holding the payload; `notify(escape(payload))` raises `MarkupError`; `run_test` paints toasts only with `notifications=True` | premise | ✅ TRUE | `p0-probes.txt` §P-7 | LLR-401.2; the ATs run with `notifications=True` |
| P-8 | The first census over `taskboard/` found 150 sink sites: 102 markup-inert, 45 not (34 `modals.py`, 11 `app.py`), 3 built from app constants only | premise | ✅ TRUE | `evidence/p1-census-base.txt` (C-39 pre-execution) | TC-404 floor |
| P-9 | Root cause: an auto-height grid row is sized to the Label's 1-line content and `margin-top: 1` consumes it; zero margin paints the cells | premise | ✅ TRUE | `evidence/p1-grid-minimise.txt` (variants `no-margin`, `fix-scoped`) | LLR-403.1 |
| P-10 | Base suite: 1854 passed, 1 failed — `test_win_clipboard_roundtrip`, whose own SETUP message names the environment (`Set-Clipboard` failed), the known flake (G-011) | premise | ✅ TRUE | `evidence/base-suite.txt` at `56a1b10` | test ledger base |
| P-11 | Under the iteration-2 rule (no non-literal value reaches a parser) the census over `modals.py` / `app.py` finds 150 sink sites — 89 markup-inert, 58 not (11 `app.py`, 47 `modals.py`), 3 exempt — and 15 parser calls, all over a non-literal (`modals.py`: the `_rich` sites and `notes_preview`); `x\\\` (and `a\\`) and `:smile:` through `_rich(escape(...))` paint altered (`evidence/p1-pieces-probe.txt`) | premise | ✅ TRUE | `evidence/p1-census-iter2.txt`; `evidence/p1-pieces-probe.txt` | LLR-401.1, LLR-401.3 |
| P-12 | On base, a `team.json` project status `[@click=app.pwn]X` applied by `apply_config_to_board` makes a click on the project picker line fire `app.pwn`; colour `evil` makes the gantt raise `KeyError`; name `123` raises in render | premise | ✅ TRUE | `evidence/p1-sync-fields-probe.txt` (re-run of the reviewer's `p_status.py`) | HLR-404 |
| P-13 | `Text.assemble` and `Text.append` paint `x\\\`, `a\\`, `:smile:` and `[b]y[/b]` exactly, and a style given as a piece applies only to that piece | premise | ✅ TRUE | `evidence/p1-pieces-probe.txt` | LLR-401.3 |

| P-14 | With the planned rule in the real app's stylesheet: 1-row cells at 140×40 and 80×24; an 89-character name wraps over 2 / 3 rows at the value column (x 44 / 26), next label after it, painted whole; five fields visible at 80×24 (max scroll 3, as base); edit-modal grid cells keep 2/3 | premise | ✅ TRUE | `evidence/p1-grid-threshold.txt` (`p1_grid_threshold.py`) | HLR-403, LLR-403.1 thresholds (C-39) |
| P-15 | On base: roster hue `[]` raises `TypeError` in setup, roster name `123` in people and standup; duplicate `team.json` project / roster ids are both kept; `project_color_on_load([])`, `({})` raise; hue `evil` rendered fine here (the reviewer's crash needed tasks) | premise | ✅ TRUE | `evidence/p1-roster-probe.txt` | HLR-404, LLR-404.1, LLR-404.2 |
| P-16 | When `history.jsonl` beside a board in `a[B]x` is a directory, the transition-log message is `PermissionError: …` holding `repr(str(path))`, not `str(path)`, on this Windows host | premise | ✅ TRUE | `evidence/p1-history-probe.txt` | HLR-401 (AT-403's expected text) |

- **Premise evaluation:** 16 premise(s) · ✅ TRUE 16 / ❌ FALSE 0 / ❓ UNDECIDABLE 0

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-401 — Dialogs, pickers and toasts paint user and synced text exactly
- **Traceability:** US-401
- **Ledger:** LED-2026-10-02-batch-04.1, LED-2026-10-02-batch-04.4, LED-2026-10-02-batch-04.8
- **Statement:** When a modal, a picker option, a select prompt, a button or a notification shows user or synced text, the system shall paint that text exactly as written — square brackets, backslashes and colons included — and shall keep the screen running.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_markup_sites.py tests/test_markup_census.py tests/test_details_markup.py`
- **Numeric pass threshold:** every reachable site of §5.1 with every payload of the set, each in its own run: 0 exceptions and the text painted exactly — a toast read from its painted `Toast`; a report or recovery path compared whole with `str(path)`; the transition-log toast compared with the OS error message the same failing write produces (`PermissionError: [Errno 13] Permission denied: <repr of the path>` on Windows, P-16); a Setup id compared lowercased; the census: 0 non-exempt sites not markup-inert, 0 parser calls over a non-literal; the app-styled sites keep their painted style (TC-415); 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the dialog or toast opens and shows the text as typed, styled as before.
  - **Shipped surface:** `TaskboardApp` keys via `App.run_test(notifications=True)`.
  - **Acceptance test(s):** AT-401, AT-402, AT-403
  - **Boundary catalog (QC-3):** ☑ invalid (the payload set) ☑ boundary (a path whose bracket follows a separator `[B]x`, and one inside a name `a[B]x`; a lowercased Setup id) ☐ empty — N/A ☑ error (the sync-failure toast, TC-412; the transition-log toast)
  - **Negative control:** on base, per site: `MarkupError` at the Textual-parsed sites, an altered or vanished payload at the `_rich` sites (P-1, P-7, P-11) → RED.

### HLR-402 — Control bytes are stripped where text enters
- **Traceability:** US-402
- **Ledger:** LED-2026-10-02-batch-04.2, LED-2026-10-02-batch-04.5, LED-2026-10-02-batch-04.8
- **Statement:** When the board file is loaded, a teammate's file or the team config is read, or clipboard text is pasted, the system shall remove every control byte from every string it reads, turn each CR-LF pair into one newline, and leave every other character unchanged, so that a board file the app saved, holding no control byte, loads and saves byte-identical.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_control_bytes.py`
- **Numeric pass threshold:** a board whose title, notes, project name, phase, URLs and dates hold ESC, C1, BEL and DEL: 0 control bytes in the loaded model, in the strings of the next saved file (parsed JSON), and — for ESC and C1, which reach the paint (Rich drops BEL, Q-5) — in the painted details view; tabs, newlines and characters ≥ U+00A0 kept; a dirty board opened by the app in team mode pushes a file whose parsed strings hold 0 control bytes, and that file reaches a second `TeamState` and a second app clean; a file the app saved, holding no control byte: `Board.load` + `save` byte-identical (TC-410); 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a dirty board opens with the bytes gone from the screen and from the next save; what the app pushes reaches a teammate clean.
  - **Shipped surface:** `TaskboardApp` over a board file on disk and a shared directory.
  - **Acceptance test(s):** AT-404, AT-405
  - **Boundary catalog (QC-3):** ☑ boundary (tab, newline, CR-LF, a lone CR, U+00A0, U+009F, U+007F, emoji) ☑ empty (empty strings, a board with no tasks) ☑ invalid (non-string JSON values left alone; a phase made only of control bytes, D-408) ☐ error — N/A
  - **Negative control:** the base tree keeps ESC in the loaded title (P-3) and the synced title (P-4) → RED.

### HLR-403 — The details info grid paints its fields
- **Traceability:** US-403
- **Ledger:** LED-2026-10-02-batch-04.3, LED-2026-10-02-batch-04.6, LED-2026-10-02-batch-04.8, LED-2026-10-02-batch-04.9, LED-2026-10-02-batch-04.13
- **Statement:** When the details view of a task is opened, the system shall paint the labels `Project`, `Phase`, `Priority`, `Start` and `Due` in order, each with its value beginning on the label's row beside it, and a value wider than its column shall wrap under itself rather than be cut.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_details_grid.py tests/test_details_markup.py`
- **Numeric pass threshold:** (measured: `evidence/p1-grid-threshold.txt`, `evidence/inc004-probe.txt`) at terminals 140×40 and 80×24, priority `high`: each of the five labels painted inside `#details-box` with its value starting on the same row at the value column (x 34 at 140, x 16 at 80); the 89-character name `LONG` painted whole (whitespace normalised) over 2 rows at 140 and at 80×24, each continuation row's first painted character at the value column, the `Phase` label on the row after the value's last row; at 80×24 with the long name the five fields are inside the visible box at scroll 0; every grid cell ≥ 1 row; the edit modals' grid cells keep their base heights (`ProjectModal` 2/3 per label/input, `ClockModal` 2/3); 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `enter` shows the five fields and their values; a long value wraps.
  - **Shipped surface:** `TaskboardApp` key `enter` (painted screen via `App.run_test`).
  - **Acceptance test(s):** AT-406
  - **Boundary catalog (QC-3):** ☑ boundary (an Inbox task; no dates `—`; a blocked task `· blocked`; a long value; 80×24) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base tree paints none of the five labels (P-5, `p1-grid-threshold.txt` base rows: 0-row cells) → RED.

### HLR-404 — A shared config cannot act or crash
- **Traceability:** US-404
- **Ledger:** LED-2026-10-02-batch-04.7, LED-2026-10-02-batch-04.8, LED-2026-10-02-batch-04.9
- **Statement:** When the team config is applied, the system shall take from a synced project entry only the fields the entry holds, and of those only values that loading a board file accepts — an unknown status or colour of any type becoming the loading default, a name that is not a non-empty text and a date that is neither text nor empty being ignored; a roster entry's name that is not a non-empty text shall read as its id and a hue the palette does not hold as `mut`; and of two synced projects or roster entries with one id the first shall be kept.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_markup_sites.py -k AT_407 tests/test_sync_fields.py`
- **Numeric pass threshold:** a `team.json` whose existing project carries status `[@click=app.view('gantt')]X`, colour `[]`, name `123`, due `7`, a new project with the same hostile fields and a duplicate id, a roster entry with name `123` and hue `[]`, and a duplicate roster id: the app started once with no team identity (the identity picker opens: it renders and lists each roster id once) and once as `a` (startup sync): clicking each cell of the existing project's painted status, one run per cell, leaves the view unchanged, the line paints `on_track` and neither `[@click` nor `gantt`, its name and due keep their previous values; the new project paints `Untitled` / `on_track`; the picker shows one line per project id, holding the first synced entry; views 1–8, the Setup view, the project picker and the team identity picker render with 0 exceptions; the base RED of the `app.view('gantt')` click is recorded at P3 (UX3-2); 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the shared folder's hostile project and roster fields neither run an action nor crash a view or a picker.
  - **Shipped surface:** `TaskboardApp` in team mode (a shared directory on disk) via `App.run_test`, the mouse click on the picker line.
  - **Acceptance test(s):** AT-407
  - **Boundary catalog (QC-3):** ☑ invalid (action tag, unhashable colour, int name, int date, roster int name and unhashable hue, duplicate ids) ☑ boundary (a valid synced status `paused` and colour `sky` still applied; a synced `null` due clears the date) ☐ empty — N/A ☐ error — N/A
  - **Negative control:** on base the click fires the action, an unknown colour raises in four views, duplicate ids are both kept, a roster name `123` raises in people and standup (P-12, P-15) → RED.

## 4. Low-level requirements (LLR)

### LLR-401.1 — Every markup sink is fed a markup-inert value
- **Traceability:** HLR-401
- **Ledger:** LED-2026-10-02-batch-04.4, LED-2026-10-02-batch-04.8, LED-2026-10-02-batch-04.10
- **Statement:** Every call in `taskboard/` that hands a value to a markup sink shall hand it a markup-inert value, except the seven sites the census declares — five built from app constants: `KeyBar.refresh_bar` (key bar), `Ribbon.update_clock` (clocks), `HelpScreen.compose` (keymap screen), and in `HelpModal.compose` the parser over `help_example`'s example and the parser over `legend_entries`' swatch; and the two board repaints `TaskboardApp._repaint_flow` / `refresh_view` (`views.render_view`, the board seat, D-405) — each keyed by module, function, sink and the value's source text with its binding.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_markup_census.py -k "TC_401 or TC_402 or TC_403 or TC_404"`
- **Numeric pass threshold:** census over `taskboard/`: 0 non-exempt sites not markup-inert; each of the seven exemptions matches exactly one live site by its source text and binding; the planted module: each unsafe form flagged and each safe form passed (the lists in TC-403, including `.tooltip =`, `border_subtitle`, `set_options`, `replace_option_prompt`, `rich.markup.render`, an aliased parser, a keyword method sink, a tuple rebinding, `Select.from_values`, `Select(prompt=)`, `setattr(w, "border_title", …)`, and a method call named like a `-> Text` function); population ≥ 140 sites covering the 11 sink kinds the app uses; every widget class the package imports from Textual is a censused sink or a declared plain-text widget (`Input`, `TextArea`); 0 failures.
- **Negative control:** the base tree → TC-401 RED listing the sites (`evidence/p1-census-iter2.txt`); a sink kind dropped, a name trusted without its binding, a parser over user text trusted → TC-403 RED; an exemption whose site or binding is removed or replaced → TC-402 RED (a value ADDED to an exempt function is a new key, flagged by TC-401 / TC-406).
- **Boundary catalog:** ☑ boundary (a name bound to `Text` vs to a str; an `IfExp` of literals; a Select pair) ☑ invalid (an attribute, an f-string, a free name, a parser over a non-literal) ☐ empty — N/A ☐ error — N/A

### LLR-401.2 — A notification carrying user text has markup off and the raw text
- **Traceability:** HLR-401
- **Ledger:** none
- **Statement:** Every `notify` call whose message is not an app literal shall pass `markup=False` and shall build its message without `escape`, so that the toast shows the text as written and no escaping backslash.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_markup_census.py -k TC_405` (TC-405); `pytest tests/test_markup_sites.py -k TC_412` (TC-412)
- **Numeric pass threshold:** 0 `notify(..., markup=False)` messages in `taskboard/` holding an `escape(...)` call (AST); the team-sync failure toast, driven by declared fault injection (a `TeamState.sync` patched to raise an exception carrying each payload — the sync path never raises on its own, Q-3), paints `Team sync failed: <payload>` exactly; 0 failures.
- **Negative control:** a planted `notify(f"'{escape(name)}'", markup=False)` → TC-405 flags it; on base TC-412 raises `MarkupError`.
- **Boundary catalog:** ☑ invalid (escape inside an f-string, inside a bound name; the payload set) ☐ empty — N/A ☐ boundary — N/A ☑ error (the sync-failure path)

### LLR-401.3 — User text is built as Text pieces, never parsed
- **Traceability:** HLR-401
- **Ledger:** LED-2026-10-02-batch-04.4, LED-2026-10-02-batch-04.8, LED-2026-10-02-batch-04.9, LED-2026-10-02-batch-04.10
- **Statement:** In `modals.py` and `app.py`, every markup parser call shall take an app literal or be one of the census's declared app-constant sites; user or synced text shall be added to a `Text` as a piece (`Text(...)`, `Text.assemble`, `Text.append`) whose style is an app constant or a lookup in a constant table keyed by a validated field; the notes' `==` / `!!` / `++` highlights shall be built as styled pieces from one tokeniser (`views.highlight_segments`, NEW) that the board's `_highlight_markup` also reads; the app-styled sites shall keep their painted style, and app text holding a bracket (`[ ] month`, `[ / ] reorder`) shall paint without a backslash.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_markup_census.py -k TC_406` (TC-406); `pytest tests/test_markup_sites.py -k TC_415` (TC-415); `pytest tests/test_highlight_segments.py` (TC-417); `pytest tests/test_details_markup.py`
- **Numeric pass threshold:** 0 parser calls in `modals.py` / `app.py` over a non-literal outside the exemptions (AST, every call); TC-415 reads the painted segments of: the details and image-viewer title (bold, as base paints it: the `.modal-title` rule bolds the whole row), a project-picker line off the cursor (name bold, `archived` dim), a phase-editor line (`N.` dim, name bold), the standup (`▐ project` bold, phase dim, `k/n closed` dim), the calendar (month bold; selected day bold + reverse; days outside the month dim; week header as on base), the help modal (headings bold, usage heading underlined, example meaning dim), the `—` placeholders and `missing:` / `could not render:` prefixes (dim), the text-prompt title (bold) — each equal to the base tree's painted flags (an arm whose bold the `.modal-title` rule also carries is a preservation pin no code-side mutation reddens, named in the evidence), recorded at P3 before the conversion as literals in the test with their base transcript (`evidence/inc001-style-base.txt`); the calendar and phase-editor titles paint `[ ] month` and `[ / ] reorder`; the details view and the editor preview (keys typed into the notes) paint `==…==` soon, `!!…!!` over, `++…++` green with markers hidden; `_highlight_markup`'s output unchanged — equal to the base function's over a derived input set of every input the base rendered (TC-417, layer 0), and every existing board node green; an empty highlight (`====`) no longer raises (D-415); 0 failures.
- **Negative control:** base: `_rich(f"[b]{escape(t.title)}[/b]")` and `notes_preview`'s `Text.from_markup` → TC-406 RED; the title `x\\\` and `:smile:` painted altered (P-11); a converted site dropping its style piece → TC-415 RED (the mutation is named per arm at P3).
- **Boundary catalog:** ☑ invalid (the payload set in notes, title, URL, image) ☑ boundary (a highlight around a payload: `!!x\\\!!`; a cursor row vs an off-cursor row) ☐ empty — N/A ☐ error — N/A

### LLR-402.1 — One control-byte rule
- **Traceability:** HLR-402
- **Ledger:** LED-2026-10-02-batch-04.5, LED-2026-10-02-batch-04.11
- **Statement:** A function `strip_controls` (NEW, `taskboard/models.py`) shall return its `str` argument with each CR-LF pair turned into one newline and every control byte removed (tab and newline kept), and every other value unchanged; `clean_strings` (NEW) shall apply it to every string inside nested dicts and lists, keys included; `_clean_clipboard_text` shall apply `strip_controls` before its length cap.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_control_bytes.py -k "TC_407 or TC_414"` (TC-407, TC-414)
- **Numeric pass threshold:** over every code point U+0000..U+00FF: kept exactly when tab, newline, 0x20..0x7E or ≥ 0xA0 (256 arms, derived); CR-LF → LF, a lone CR removed; emoji and U+00A0 kept; ints, bools and `None` unchanged; nested strings and keys cleaned (two keys equal after cleaning: the later wins, D-408); `_clean_clipboard_text("a\r\nb\rc")` is `"a\nbc"` and its shipped arms hold; 0 failures.
- **Negative control:** a rule keeping CR or DEL, or dropping U+00A0 → RED on that arm; the base `_clean_clipboard_text` keeps `\r` → TC-414 RED.
- **Boundary catalog:** ☑ boundary (U+001F/U+0020, U+007E/U+007F, U+009F/U+00A0) ☑ empty (`""`) ☑ invalid (non-str values) ☐ error — N/A

### LLR-402.2 — The load door
- **Traceability:** HLR-402
- **Ledger:** none
- **Statement:** `Board.load` shall pass the parsed JSON through `clean_strings` before building any project, task, phase or setting.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_control_bytes.py -k "TC_408 or TC_410"` (TC-408, TC-410)
- **Numeric pass threshold:** a board file with a control byte planted in every string value of every project, task, phase and setting (the set derived by walking the file's JSON, its size asserted): 0 control bytes in any string attribute of the loaded board; a file the app saved holding no control byte: load + save byte-identical; a dirty file: the second save equals the first; a phase made only of control bytes loads the default phases (D-408); a hand-edited project name `""` or an int date loads as `Untitled` / `None` (D-410); 0 failures.
- **Negative control:** `Board.load` without the call → TC-408 RED (P-3).
- **Boundary catalog:** ☑ boundary (a legacy `url` string; a rescued task) ☑ empty (no tasks; a `""` name) ☑ invalid (a control-only phase; an int date) ☐ error — N/A

### LLR-402.3 — The sync doors
- **Traceability:** HLR-402
- **Ledger:** LED-2026-10-02-batch-04.5, LED-2026-10-02-batch-04.11
- **Statement:** `team_sync._read_json` shall pass every dict it returns through `clean_strings`, and the Setup view shall read `team.json` through `_read_json`, so that the team config and every teammate's file are clean before any task, project, phase, roster entry or republished config is built from them.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_control_bytes.py -k "TC_409 or TC_419"` (TC-409, TC-419)
- **Numeric pass threshold:** a teammate file and a `team.json` with control bytes in titles, notes, project names, phases and roster names: 0 control bytes in `foreign_tasks()`, `member_names()`, the board after `apply_config_to_board`, and the `team.json` the Setup view writes back; 0 failures.
- **Negative control:** `_read_json` without the call → TC-409 RED (P-4).
- **Boundary catalog:** ☑ invalid (a non-dict file stays `None`) ☐ empty — N/A ☐ boundary — N/A ☐ error — N/A

### LLR-403.1 — The details grid rule
- **Traceability:** HLR-403
- **Ledger:** LED-2026-10-02-batch-04.6, LED-2026-10-02-batch-04.12, LED-2026-10-02-batch-04.13
- **Statement:** The stylesheet shall give the labels of the details view's info grid (`#details-box .modal-grid Label`) no top margin and an automatic height, that grid a 10-cell label column, and the details title no top margin and one row below it, leaving the other modals as they are.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_details_grid.py -k "TC_411 or TC_420 or TC_421"` (TC-411, TC-420, TC-421)
- **Numeric pass threshold:** in the details view every `.modal-grid` child ≥ 1 row, each value cell on its label's row; the 89-character name's cell 2 rows at 140×40 and at 80×24 with its label 1 row; 1 blank row above the title, 1 under, the `ProjectModal` title 2 under its border (TC-420); values 11 cells right of labels, five visible (long name), `ProjectModal` 21 (TC-421); the `ProjectModal` grid cells 2/3 per label/input and the `ClockModal` 2/3 (the base heights, a pin; `evidence/p1-grid-threshold.txt`); 0 failures.
- **Negative control:** the base stylesheet → 0-row cells → RED (P-5); increment 003's tree → TC-420, TC-421 RED.
- **Boundary catalog:** ☑ boundary (80×24; a long value) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-404.1 — Synced project fields pass the loading rule
- **Traceability:** HLR-404
- **Ledger:** LED-2026-10-02-batch-04.7, LED-2026-10-02-batch-04.8, LED-2026-10-02-batch-04.9, LED-2026-10-02-batch-04.11
- **Statement:** `project_color_on_load` shall return the default colour for any value it does not know, of any type; `Project.from_dict` shall give a name that is not a non-empty `str` the value `Untitled`, a start or due date that is neither a `str` nor `None` the value `None`, and `archived` / `pinned` the value `True` only for the boolean `True`; `apply_config_to_board` shall, for an existing project, set each of `name`, `color`, `status`, `start_date`, `due_date` present in the synced entry from `Project.from_dict`'s value for it, except a name that is not a non-empty `str` and a date that is neither a `str` nor `None`, which it shall leave unchanged, shall apply `archived` to an existing project only when the synced value is a boolean, shall apply only the first synced entry of each id (to an existing project as to a new one), and shall append a new project from `Project.from_dict` only for an id no earlier project holds.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_sync_fields.py -k "TC_413 or TC_418"` (TC-413, TC-418)
- **Numeric pass threshold:** over status {`[@click=app.pwn]X`, `at_risk`, each of `PROJECT_STATUSES`}, colour {`evil`, `[]`, `{}`, `#123456`, each of `PROJECT_COLORS`}, name {`123`, `None`, `""`, `Untitled`, `Ops`}, start {`7`, `None`, `2026-10-01`}, due {`7`, `None`, `2026-10-09`}, `archived` / `pinned` {`1`, `"true"`, `"false"`, `None`, `True`, `False`}, each key present and absent (arms derived from the model's constant tuples plus the hostile values): the applied value equals `Project.from_dict`'s for a board file, the previous value where the input is refused, the previous value where the key is absent; a synced `Untitled` name is applied; a synced `null` due clears it; a new project equals `Project.from_dict(entry)`; of two entries with one id — existing or new — only the first is applied or appended; 0 failures.
- **Negative control:** base `apply_config_to_board` (`setattr` of raw values) and base `project_color_on_load([])` → the hostile arms RED (P-12, P-15).
- **Boundary catalog:** ☑ invalid (the hostile values) ☑ boundary (every valid constant; `Untitled`; `null` due) ☑ empty (`""` name; an entry holding only `id`) ☐ error — N/A

### LLR-404.2 — The roster passes a loading rule too
- **Traceability:** HLR-404
- **Ledger:** LED-2026-10-02-batch-04.8, LED-2026-10-02-batch-04.9
- **Statement:** A function `clean_roster` (NEW, `taskboard/team_sync.py`) shall return a synced roster with the first entry of each id, each entry's name a non-empty `str` or else its id, and each entry's hue a key of the palette `views.HEX` (tested without hashing an unhashable value) or else `mut`; `TeamState.roster` (and through it `member_names` / `member_hues`) and the Setup view's roster read and republish (`app.py`) shall read the roster only through it.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_sync_fields.py -k TC_416` (TC-416)
- **Numeric pass threshold:** a roster with ids `a`, `a`, `b`, names `123`, `""`, `Bo`, hues `[]`, `evil`, every key of `HEX`: `clean_roster` and `roster()` give ids `a`, `b` (the first `a`); names `a`, `Bo`; hues `mut` for `[]` and `evil`, each `HEX` key kept; the Setup view's staged roster equals `clean_roster`'s; the people, standup and setup views and the team identity picker render with 0 exceptions, the picker painting `a` for the name `123`; 0 failures.
- **Negative control:** base: duplicate ids kept, roster name `123` raises in people and standup, hue `[]` in setup (P-15) → RED.
- **Boundary catalog:** ☑ invalid (int name, unhashable hue, unknown hue, duplicate id) ☑ boundary (every `HEX` key) ☑ empty (`""` name) ☐ error — N/A

## 4b. Information Flow Contract (IFC)

Part A always. Part B: the details view's info grid is addressed by a stylesheet selector, and
this batch adds a rule keyed on it.

```
FLOW: text to the screen
  SOURCE : the board file on disk; team.json and board.<user>.json in the shared directory; the clipboard; typed input; OS errors and paths
  NODES  :
    - fn    : strip_controls / clean_strings / _clean_clipboard_text
      owner : LLR-402.1
      in    : any JSON value; clipboard text
      out   : the value with control bytes removed from every string
    - fn    : Board.load
      owner : LLR-402.2
      in    : the board file
      out   : a Board built from cleaned strings
    - fn    : team_sync._read_json and the Setup view's team.json read
      owner : LLR-402.3
      in    : a shared-directory JSON file
      out   : a cleaned dict
    - fn    : project_color_on_load / Project.from_dict / apply_config_to_board
      owner : LLR-404.1
      in    : a synced project entry
      out   : project fields loading would accept
    - fn    : clean_roster, read by TeamState.roster (member_names, member_hues) and the Setup view's roster read and republish
      owner : LLR-404.2
      in    : the synced roster
      out   : one entry per id, text names, palette hues
    - fn    : the modal, picker and notification sinks (modals.py, app.py)
      owner : LLR-401.1
      in    : user or synced text, app literals
      out   : a markup-inert value at each sink
    - fn    : the Text-piece builders and views.highlight_segments
      owner : LLR-401.3
      in    : user or synced text, constant styles
      out   : a Rich Text no parser has read
    - fn    : TaskboardApp notify sites
      owner : LLR-401.2
      in    : user or synced text
      out   : a toast with markup off and the raw text
    - fn    : the details grid rule
      owner : LLR-403.1
      in    : the details view's grid labels
      out   : one painted row per field, long values wrapped
  SINK   : the painted screen, the saved board file and the pushed teammate file
```

```
COMPONENT: details-info-grid
  PARENT : SYSTEM
  SURFACE: the task details view (key enter)
  INPUTS : task: Task ; board: Board
  OUTPUTS:
    - id          : field-rows
      value       : the five label/value pairs of the info grid
      address     : "#details-box .modal-grid"
      cardinality : 5 rows, INDEXED POSITIONALLY
      consumers   : taskboard/taskboard.tcss ; taskboard/modals.py::TaskDetails ; tests/test_details_markup.py ; tests/test_details_grid.py
      owner       : LLR-403.1
```

## 5. Validation strategy

Layer A (`TC-401`..`TC-421`) and Layer B (`AT-401`..`AT-407`, one node each — C-18) are pytest
nodes carrying their id in their docstring and name; The ATs
drive `TaskboardApp` through `App.run_test(notifications=True)`; inside each AT node every site and
payload runs in its own `run_test`, failures are collected and reported together, and the base run
records every site RED (Q-4). A toast is read as `str(toast.render())` of each painted `Toast` in
`app.screen.query("Toast")` — its title, a newline, its message (UX-6, P-7). Keys: the shipped
keymap's (`taskboard/keymap.py`), per site in §5.1; the team identity picker opens at mount in team
mode without an identity (`app.py` `_init_team_mode`). TC-401..TC-406
walk the package's AST; TC-407..TC-410, TC-413, TC-414, TC-416 drive the model and team sync on
disk; TC-412 is the declared fault injection for the sync-failure toast (Q-3); TC-415 reads painted
segments against the base's. Details captures go to `evidence/captures/`.

| AT | Story | Drives (each site with each payload of the set; screen alive and text painted exactly) |
|---|---|---|
| AT-401 | US-401 | board-file text: the sites of §5.1 marked *board*, the details/image branches and the editor preview included |
| AT-402 | US-401 | synced text: the sites marked *synced* |
| AT-403 | US-401 | typed and OS text: the sites marked *typed* / *path*; path sites over a board directory `a[B]x` and one `[B]x` (the report and recovery toasts compared whole with `str(path)`; the transition-log toast compared with the error text of the same failing write — a directory named `history.jsonl` beside the board, then `]`); Setup ids expected lowercased |
| AT-404 | US-402 | a dirty board file opened by the app: details painted without ESC and C1; `]` saves; the saved file's parsed strings hold 0 control bytes |
| AT-405 | US-402 | the C-12 chain: app A opens a dirty board in team mode (its startup sync pushes `board.<A>.json`); the file A wrote is re-read — its parsed strings hold 0 control bytes — and fed unchanged to a second `TeamState` and to a second app, whose painted board holds no control byte |
| AT-406 | US-403 | `enter` at 140×40 and 80×24, priority `high`: the five labels and values painted, the 89-character name wrapped under the value column, the next label after it, the five visible at 80×24 |
| AT-407 | US-404 | team mode with a hostile `team.json` (§HLR-404), the startup sync, `P`: a click on the existing project's line leaves the view unchanged and paints `on_track`; the new project; views 1–8, Setup and both pickers render |

### 5.1 The reachable sites (from the census, P-8 / P-11)

| Site | Where | Text | Keys | AT |
|---|---|---|---|---|
| delete-task confirm | `app.py` `action_delete` → `ConfirmModal` | task title (board) | `d` | AT-401 |
| archive / restore toast | `app.py` `action_archive` | task title (board) | `x` | AT-401 |
| pin toast | `app.py` `action_project_pin_toggle` | project name (board) | `T` | AT-401 |
| project picker line | `modals.py` `ProjectPicker._project_line` | project name (board) | `P` | AT-401 |
| project archive / delete confirm | `modals.py` `ProjectPicker.action_archive`, `action_delete` → `ConfirmModal` | project name (board) | `P` then `x` / `d` | AT-401 |
| blocker picker | `modals.py` `BlockerPicker.on_mount` | task title (board) | `b` on an unblocked task | AT-401 |
| task editor project and phase selects | `modals.py` `TaskModal.compose` | project, phase names (board) | `e` | AT-401 |
| phase editor list, delete-phase confirm, rename prompt | `modals.py` `PhaseEditor._reload`, `action_delete`, `action_rename` | phase name (board) | `f`, then `d` / `e` | AT-401 |
| standup | `modals.py` `StandupModal.compose` | project name, title, phase (board) | `S` | AT-401 |
| details view, image viewer | `modals.py` `TaskDetails`, `ImageViewer` | title, notes, URL (board) | `enter`, `i` | AT-401 (and AT-007) |
| image block branches | `modals.py` `image_block` | a URL ref (`link ·`) and a missing file (`missing:`) with every payload; an existing image `a[B]x.png` (`path.name`) and a corrupt `bad[B].png` (`could not render:`) with the bracket payload only — the other payloads are not legal Windows file names; the `install textual-image` branch is n/a (textual-image installed) | `enter` | AT-401 |
| editor preview | `modals.py` `notes_preview` via `TaskModal` | notes typed as keys | `e`, type | AT-401 |
| team identity picker | `modals.py` `TeamIdentityPicker.on_mount` | roster name (synced) | opens at mount in team mode with no identity | AT-402 |
| teammate project / phase in the editor selects and the picker | via `apply_config_to_board` | project name, phase (synced) | `e`, `P` | AT-402 |
| team-sync failure toast | `app.py` `_team_sync_tick` | exception text | fault injection | TC-412 |
| Setup duplicate member / project id toasts | `app.py` `_on_setup_member_added`, `_on_setup_project_added` | typed id, lowercased | `0`, `tab` to the roster / projects section, `a`, the id typed twice | AT-403 |
| phase editor duplicate-name toasts (add, rename) | `modals.py` `PhaseEditor._on_added`, `_on_renamed` | typed name | `f`, `a` / `e`, an existing name | AT-403 |
| report-written toast | `app.py` `action_report` | file path | `R` | AT-403 |
| board-recovered toast | `app.py` `_warn_if_rescued` | file path | an unreadable board file at mount | AT-403 |
| transition-log toast | `app.py` `_warn_history_error` | OS error text with a path | `]` with `history.jsonl` a directory | AT-403 |

The other census sites are built from app constants and are converted for the census rule;
TC-415 pins the style of the sites LLR-401.3 lists; emoji and palette lines keep their text pins.

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion shown RED on the base tree or by a recorded mutation.
- the census lists 0 non-exempt unsafe sites and 0 parser calls over a non-literal; each existing node the batch changes is listed in its increment's reverse census.
- full suite: 0 failures other than the declared clipboard environment flake.

## 6. Appendices

### 6.2 Relevant design decisions
- D-401: Trigger family A judged not fired: the `taskboard` package is one module (no module map), as batches 01–03 ruled (D-215, D-310).
- D-402: The census exempts seven sites: five built from app constants only — the key bar, the clocks, the keymap screen, and the help modal's example and legend swatches (parsed once each from views-built constant markup) — and the two board repaints, whose seat is `views.py` (D-405); each keyed by module, function, sink and source text with its binding, guarded both ways (TC-402).
- D-403: User or synced text is a `Text` piece; app literals may stay markup; a notification carrying user text uses `markup=False` and no styling (operator ruling 2; ux found no toast losing styling, `02-review.md`).
- D-404: CR-LF becomes LF, a lone CR is removed (the commission keeps only `\n` and `\t`; a CR-only old-Mac note joins its lines — UX-7, accepted), DEL is removed with C0/C1; the clipboard cleaner shares the rule (A-2, ruling 3).
- D-405: `collapse_runs` S-2 and the S-4 class in the board renderers stay in `BACKLOG.md`: their seat is `views.py`'s Rich markup, not the Textual sinks; this batch's seat holds no `collapse_runs` call (ruling 2: "decide per seat").
- D-406: The details grid takes one row per field (no blank row between), values wrap (UX-1); the edit modals' grids untouched — PV-1 accepted 2026-10-04; UX-3, UX-4 applied (A-7).
- D-407: The sync-failure toast is verified white-box by declared fault injection (TC-412): the sync path swallows its own errors, so no black-box input reaches it (Q-3).
- D-408: `clean_strings` cleans keys: two keys equal after cleaning keep the later value; a phase made only of control bytes becomes empty, so the phase list is refused and the default phases load, as for any empty phase (A-4); path-valued settings that held DEL or C1 lose them (accepted: such a path is hostile input).
- D-409: Legacy `history.jsonl` records are not cleaned (S-8): the app writes them from loaded, now clean, text; the old records' phase names are matched against the board's phases before painting. Routed to `BACKLOG.md`.
- D-410: Synced project fields are validated by `Project.from_dict` — the loading rule, one seat (operator ruling 1); the loading rule gains the name, date, `archived` / `pinned` and any-type colour checks so a board file and a team config are judged alike; a hand-edited board file holding a `""` or non-text name, a non-text date or a non-boolean flag is normalised on load and rewritten on the next save (A2-2). For a synced entry, refusal is judged on the INPUT (A2-1): only keys present are applied; a name that is not a non-empty text and a date that is neither text nor `null` leave the field unchanged; a synced `Untitled` name is applied; a synced `null` date clears the date, as on base.
- D-411: The notes highlight has one tokeniser, `views.highlight_segments` (NEW), read by the board's `_highlight_markup` (output unchanged) and by the details/preview piece builder (A2-3, C-50); `views.py` joins increment 001 as its third SOURCE file.
- D-412: The roster passes a loading rule in `team_sync` (S2-1): first entry per id, a text name or the id, a palette hue or `mut`; duplicate synced project ids keep the first (S2-1). The palette is `views.HEX`, imported inside `clean_roster` (function-local: `views` imports `team_sync` at module level, a module-level import would be a cycle — A3 note); the Setup view reads the roster through it (A3-1).
- D-414: Synced phases and a new project's extra keys are accepted as cleaned (control bytes) and otherwise unvalidated (S3-2): phases reach the screen only as Text pieces; extras are never rendered. A bound on duplicate phase names and the phase list's length is routed to `BACKLOG.md`.
- D-415: `highlight_segments` takes the group that MATCHED; the base `_highlight_markup` read `m.group(1) or m.group(2) or m.group(3)`, which is `None` for an empty highlight (`====`, `!!!!`) and raised `TypeError` — a note holding one crashed every board renderer that paints notes. Fixed by the tokeniser split (found at P3), pinned by TC-417.
- D-416: An empty synced project id (literal or once cleaned) is refused (P3 F1: the board grew per tick).
- D-417: A file nested deeper than the cleaning follows is unreadable: `team.json` → a `could not be read` toast; a teammate file → skipped; `board.json` → quarantined (P3 S4-1).
- D-418: Setup stages an id's first entry with the board's validated values (P3 F3).
- D-419: A board-file project id of control bytes only gets a fresh id; its tasks fall to the Inbox (accepted, F6). The toast fires for an unreadable `team.json` only, not an incomplete one (G1).
- D-413: A Text piece's style is an app constant or a lookup in a constant table keyed by a validated field (S2-4: a style from data could carry an OSC-8 link); checked by the code review, not by the census.

### 6.3 Open risks
- A Textual upgrade can add sinks or change which parameters parse markup (A2); the census derives the constructor sinks from Textual's signatures and checks that every imported widget is censused or declared plain; the method and attribute sink names are a declared list (TC-404 checks they exist).
- The census is syntactic: method sinks match by name, so a `dict.update` in a module that imports Textual is counted (it fails loud); a parser call is judged over its argument only (A-6).
- Unicode format characters (U+202E and kin) are not control bytes and pass; they cannot move the cursor or emit sequences (S-9, BACKLOG).
- Security questions (scan `devflow-scan-spec.py`: `security_required: true`, flags `session`, `form`, `escape` — `evidence/p1-security-scan.txt`): inputs: the board file, the shared directory (untrusted, A1), the clipboard, typed prompts, OS paths/errors; no render mode is turned on — markup parsing is removed from user text (C-17 in reverse: AT-401..403, AT-407, LLR-401.1, LLR-401.3); the synced config is validated (HLR-404); no secret, auth, network or destructive surface; `security-reviewer` at P2 and close.

### 6.4 Phase-1 reconciliation log
- Iteration 2 (2026-10-03): P2 iteration 1 folded under the operator's rulings 1–3 (`PLAN.md`); every finding's disposition in `02-review.md` §Iteration-1 fold.

### 6.5 Requirement amendments (Before / After · Deleted / New)

**A-1 (P3, increment 001, 2026-10-03)** — LLR-401.1, §1.3, D-402. *Before:* five declared sites; a `-> Text` function trusted by its annotation. *After:* seven (the two board repaints, D-405); trusted only when every `return` is inert. *New:* two EXEMPT keys, planted `_lie`/`_parsed`. HLR-401 re-read: unchanged (LED .10).

**A-2 (P3, increment 001)** — LLR-401.3. *Before:* the title tail "not bold". *After:* bold as base paints it (`.modal-title` CSS); CSS-carried arms are named pins (LED .10).

**A-3 (P3, increment 001)** — LLR-401.3, D-415. *Before:* unchanged "over a payload-free set". *After:* over a derived set of every input the base rendered; an empty highlight no longer raises. *New:* TC-417 (LED .10).

**A-4 (P3, increment 001)** — §5. *Before:* `_maybe_pick_identity`. *After:* `_init_team_mode` (LED .10).

**A-5 (P3, second increment revision 2, 2026-10-03)** — LLR-404.1, LLR-402.3, LLR-402.1. *New:* TC-418 (D-418), TC-419 (D-417), D-416 with TC-413 arms, TC-410's keep-everything-else arm. *Deleted:* the dead CR-LF replace in `strip_controls`. HLR-402, HLR-404 re-read: unchanged (LED .11).

**A-6 (P3, increment 003)** — IFC Part B. *New:* consumer `tests/test_details_grid.py` (V13). HLR-403 unchanged (LED .12).

**A-7 (P3 re-opened, increment 004, 2026-10-04)** — HLR-403, LLR-403.1, D-406. *Before:* gap above the title; 20-cell labels (x 44/26); long name 3 rows at 80×24. *After:* gap below; 10 cells (x 34/16); 2 rows. *New:* TC-420, TC-421 (LED .13).

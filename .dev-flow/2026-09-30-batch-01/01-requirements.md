# Requirements Document — taskboard — Batch 2026-09-30-batch-01

> Live contract (current state only). Mode `core`. Language `en`. The append-only ledger is
> `01-requirements-ledger.md`. Template: flow `templates/req-template.md` (reserved field
> names kept literal).

## 1. Introduction

### 1.1 Purpose
Implement the owner's (Javier) design verdict of 2026-09-30 after the prototype round
"edición + prioridad" (`prototypes/edit_modal/NOTES.md`, `prototypes/kanban_priority/NOTES.md`):
the task edit window becomes variant **C** (full screen + live preview), and the kanban gets
**K4** (a high-priority band per column) plus **priority badges** borrowed from K3 that reuse
the notes highlight syntax `!!` / `==` / `++` and its three tones.

### 1.2 Scope
In: `TaskModal` (layout, styling, live preview, focus mark), `taskboard.tcss` rules scoped to
the task editor, the kanban ordering seat (`kanban_order`) and its two callers in the grouped
presentation (renderer + `nav_model`), `card_cell` (badge), kanban legend entry and kanban help
example.
Out: `ProjectModal` (unchanged), the Focus view rail and People view (they keep the `!` ink
token — see §6.2 D4), the matrix legend's pre-existing presentation-blindness, any new keys.

### 1.3 Definitions
| Term | Definition |
|------|------------|
| open card | a task that is not done (`Board.is_done` false) and not archived |
| band | the per-column block of open high-priority cards at the top of a grouped kanban column, under a `── high ──` divider and closed by a rule |
| badge | a 2-cell reverse-video token before the card title: `!!` (high, `over`), `==` (normal, `soon`), `++` (low, `green`) |
| chip row | the property strip of the editor: project · phase · priority · start→due + calendar buttons · blocked/archived/pinned |

### 1.4 References
`prototypes/edit_modal/proto.py` (VariantC), `prototypes/kanban_priority/proto.py` (K3, K4),
`taskboard/modals.py:325` (`TaskModal`), `taskboard/views.py:309` (`card_cell`),
`views.py:2613` (`_highlight_markup`), `views.py:3961` (`kanban_order`),
`views.py:4036` (`_kanban_column_rows`), `views.py:4690` (`nav_model` kanban branch),
`views.py:5090` (kanban legend `!` entry), `views.py:4919` (kanban `help_example`).

## 2. Overall description

### 2.1 Product perspective
Textual TUI (`textual 8.2.8`). The editor is a `ModalScreen`; the kanban is rendered as rich
markup by `render_kanban` with a `line_map` the app uses to place the cursor, and `nav_model`
gives the arrow-key order. F-3 law: the cursor never rests on a card the view does not draw,
and nav order = draw order.

### 2.3 User characteristics
One owner-operator (Javier), keyboard-first, Windows Terminal, sizes from 80×24 to full screen.

### 2.4 Constraints
≤ 4 source files per increment; no new dependency; ids `f-title f-project f-phase f-priority
f-start f-due f-blocked f-archived f-pinned f-notes f-urls f-images paste-img save cancel
cal-f-start cal-f-due` and the `_save` payload are a contract with `app._on_task_added` /
`_on_task_edited` and existing tests.

### 2.5 Assumptions
- A1: Textual app CSS (`taskboard.tcss`) outranks widget `DEFAULT_CSS` regardless of
  specificity (measured in the round, `NOTES.md` "El CSS va en App.CSS").
- A2: the owner accepts the colour conflicts the badges introduce — stated in the commission, and the green-vs-project-hue conflict accepted explicitly on 2026-09-30 (LED .5).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-001 | As the board owner editing a task, I want the notes to take most of the screen with a live highlighted preview, so that I can see everything already written plus what I am typing. | Javier, "toda la interfaz de edición está muy amontonada… la parte de texto es muy pequeña"; verdict C 2026-09-30 | READY |
| US-002 | As the board owner scanning the kanban, I want open high-priority cards to float to a labelled band at the top of each column, so that the urgent work is the first thing I see and walk to. | Javier, "KANBAN necesita algunos cues…"; verdict K4 2026-09-30 | READY |
| US-003 | As the board owner, I want every open card to wear a priority badge in the notes highlight vocabulary (`!!` red, `==` yellow, `++` green), so that priority reads at a glance in one colour language. | Javier, "el uso de insignias, reusando !!, == y ++ para 3 colores"; 2026-09-30 | READY |
| US-004 | As the board owner, I want to open any task's details even when its text (mine or synced from a teammate) contains square brackets, so that a note can never crash the app or lose words. | security review S1 of this batch; owner verdict 2026-09-30 "fix the TaskDetails S1 the same way" | READY |
| US-005 | As the board owner filtering the gantt with `/`, I want the time scale to stay on screen, so that the filtered bars can still be dated. | field report 2026-09-30 (operator's own fix, adopted into this batch by owner verdict 2026-09-30) | READY |
| US-006 | As the board owner unpinning cards in the Focus Board, I want the cursor to move to a card the board still draws, so that the next `t` acts on what I see. | field report 2026-09 (Focus Board fix, adopted into this batch by owner verdict 2026-09-30) | READY |

#### Refinement log

**US-001 — full-screen editor**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality:** user = owner · task = writing notes in an existing task · environment = Windows Terminal 120×36 down to 80×24 · observable outcome = ≥20 (120×36) / ≥10 (80×24) note rows visible, title and Save on screen while typing, preview reflects the text.
- **Feasibility:** rewrite `TaskModal.compose` + scoped tcss; prototype measured C at 23/11 rows.
- **Evaluability:** `run_test` at both sizes, compositor regions.
- **Classification:** READY.

**US-002 — high band**
- **INVEST:** all ✓. user/task = owner scanning and arrowing through kanban; environment = grouped presentation, any group/sort; outcome = band under `── high ──` divider, cursor walks band first.
- **Classification:** READY.

**US-003 — badges**
- **INVEST:** all ✓. outcome = reverse badge per open card in kanban (grouped + lanes), none on done/archived.
- **Classification:** READY.

### 2.7 Premise evaluation (C-43)

| # | Premise | Tier | Verdict | Executed evidence | Disposition |
|---|---|---|---|---|---|
| P-1 | The shipped editor shows 3 note rows and scrolls title and Save off-screen at both sizes | premise | ✅ TRUE | `measure_real.py` on base `a9bbd1c` → `evidence/measure-baseline.json`: notes_rows_visible 3/3, title_fully_visible false, save_fully_visible false | — |
| P-2 | `kanban_order` is the single ordering seat consumed by both `_kanban_column_rows` and `nav_model` | premise | ✅ TRUE | `grep -n kanban_order taskboard/views.py` → 4050 (renderer), 4247 (lanes), 4713/4734 (nav) | — |
| P-3 | App CSS outranks `DEFAULT_CSS` (so one-row overrides can live in `taskboard.tcss`) | hypothesis | ✅ TRUE | round NOTES.md; re-verified in P3 by the focus-mark TC (style read back from the widget) | — |
| P-4 | `_highlight_markup` is the one renderer of `==`/`!!`/`++` and maps them to `soon`/`over`/`green` | premise | ✅ TRUE | `views.py:2613-2631` read | — |
| P-5 | Baseline kanban title budget per open card (fixture, selected t11): 11–18 chars at 120, 2–13 at 80 | premise | ✅ TRUE | `evidence/measure-baseline.json` `kanban.*.open_cards` | — |

- **Premise evaluation:** 5 premise(s) · 5 ✅ TRUE / 0 ❌ FALSE / 0 ❓ UNDECIDABLE

### 2.8 Fork preconditions (C-52)
- **Fork preconditions:** none — this batch runs one lane

## 3. High-level requirements (HLR)

### HLR-001 — Full-screen task editor with live preview
- **Traceability:** US-001
- **Ledger:** LED-2026-09-30-batch-01.2
- **Statement:** When a task is opened for editing, the editor shall fill the screen with a one-line title row, a property chip row, a notes editor beside a live preview, and a footer strip holding URLs, images, paste-image, Save and Cancel, such that with focus in the notes every control stays fully on screen at 120×36 and 80×24; tab shall walk title → chips (left to right, row by row) → notes → URLs → images → paste-image → Save → Cancel and never stop on the preview; Save shall be operable from the keyboard (tab to it, enter); escape shall close without saving; and the hints for ctrl+e, ctrl+v and esc shall be painted in full at both sizes.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_edit_window.py`
- **Numeric pass threshold:** notes rows visible ≥ 20 at 120×36 and ≥ 10 at 80×24 with the 23-line fixture; preview ≥ 20 columns and ≥ the notes' visible rows minus 2; `#f-title` and `#save` fully visible at both sizes; all 17 contract ids fully visible at both sizes; tab order exactly as stated (17 stops); 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the notes occupy most of the screen; the title and Save stay visible while typing.
  - **Shipped surface:** `TaskboardApp` → `e` opens `TaskModal` on the selected task.
  - **Acceptance test(s):** AT-001, AT-005
  - **Boundary catalog (QC-3):** ☑ boundary (80×24 smallest supported, 120×36 reference) ☑ empty (new task, no notes) ☐ invalid — N/A: no input value is judged by layout ☐ error — N/A: layout raises nothing
  - **Negative control:** the base editor (`a9bbd1c`) yields 3 rows and title/Save off-screen — the AT is RED on base (captured at P3).

### HLR-002 — Live highlighted preview
- **Traceability:** US-001
- **Ledger:** LED-2026-09-30-batch-01.3
- **Statement:** While the editor is open, the preview shall show the notes rendered with the app's highlight syntax (`==…==` soon, `!!…!!` over, `++…++` green) from the moment the editor opens, shall update after each edit, and shall keep the line holding the editor's cursor in view.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_edit_window.py -k preview`
- **Numeric pass threshold:** on open, the fixture's first `==…==` span is painted in `HEX["soon"]`; after typing a new `!!…!!` span on the last line the preview paints that text in `HEX["over"]` inside its visible rows; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** typed highlight appears coloured in the preview.
  - **Shipped surface:** `TaskModal` via the app.
  - **Acceptance test(s):** AT-002
  - **Boundary catalog (QC-3):** ☑ empty (no notes → empty preview) ☑ boundary (highlight marker unclosed renders raw) ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** removing the change handler leaves the preview stale, and removing the initial render leaves it empty on open → RED (P3).

### HLR-003 — Kanban high-priority band
- **Traceability:** US-002
- **Ledger:** LED-2026-09-30-batch-01.4
- **Statement:** While the kanban is in the grouped presentation and its group mode is not `priority`, each column shall draw its open high-priority cards first, under a `── high ──` divider and closed by a rule, followed by the column's normal grouping without those cards, and the arrow-key order shall equal that draw order. The band holds the column's open high cards after the project-focus filter, blocked ones included (they keep their `▲` prefix), ordered by the active sort exactly as any group is; a card whose priority changes moves into or out of the band and keeps the cursor.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_priority.py -k band`
- **Numeric pass threshold:** over every group mode × sort mode the seat declares (read from `_KANBAN_GROUP_MODES` × `_KANBAN_SORT_MODES`) × focus on/off × show_archived on/off, for every column: nav order == ids in ascending `line_map` row, band ids == open high ids of that column in the sort's order, 0 done/archived high ids in a band; the fixture holds a column with ≥ 2 open high, 1 blocked high, 1 done high and 1 archived high; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the band and its divider render; `j`/`k` walk the band first.
  - **Shipped surface:** `render_kanban` + `nav_model` as the app calls them, and the app's key walk.
  - **Acceptance test(s):** AT-003, AT-006
  - **Boundary catalog (QC-3):** ☑ empty (column with no open high → no divider) ☑ boundary (done high stays out; group=priority, lanes, matrix → no band; collapsed/focused column) ☐ invalid — N/A: no input ☐ error — N/A
  - **Negative control:** base tree draws no divider → RED (P3).

### HLR-004 — Priority badges on open kanban cards
- **Traceability:** US-003
- **Ledger:** LED-2026-09-30-batch-01.1, LED-2026-09-30-batch-01.5
- **Statement:** When the kanban draws a card (grouped or lanes presentation), an open card shall carry a reverse-video badge before its title — `!!` in `over` for high, `==` in `soon` for normal, `++` in `green` for low — and a done or archived card shall carry none; the neutral `!` token shall not be drawn on kanban cards.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_kanban_priority.py -k badge`
- **Numeric pass threshold:** per priority the badge text and style match; done/archived cards 0 badges; every kanban row exactly `w` cells; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** coloured badges per priority, none on done.
  - **Shipped surface:** `render_kanban` (grouped, lanes).
  - **Acceptance test(s):** AT-004
  - **Boundary catalog (QC-3):** ☑ boundary (done high, archived, very narrow column) ☑ empty (no open cards) ☐ invalid — N/A: unknown priority falls back to normal like `_PRIO_RANK` ☐ error — N/A
  - **Negative control:** base tree draws `!` ink and no `==`/`++` → RED (P3).
- **Supersedes:** the AC5 / Prism law "a judging hue is never worn by a priority mark" for kanban cards only — ledger `LED-2026-09-30-batch-01.1`.

### HLR-005 — Task text is never parsed as Textual markup in the details view
- **Traceability:** US-004
- **Ledger:** none
- **Statement:** When the details view of a task is opened, the system shall paint the task's title, project name, phase, priority, dates, notes, URLs and image references exactly as stored, including any square-bracket text, and shall keep the notes' `==`/`!!`/`++` highlights.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_details_markup.py`
- **Numeric pass threshold:** 4 hostile strings × 5 fields: the view opens and each string is painted literally (20/20); the `!!…!!` highlight is painted in `over`; 0 failures.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the details view opens and shows bracketed text as typed.
  - **Shipped surface:** `TaskboardApp` → `enter` → `TaskDetails`.
  - **Acceptance test(s):** AT-007
  - **Boundary catalog (QC-3):** ☑ invalid (Textual-tag-shaped text: `[LINK=`, `[B]`, `[ red]`, unclosed `a[b`) ☑ boundary (each user-controlled field) ☐ empty — N/A: unchanged path ☐ error — N/A
  - **Negative control:** the base tree raises MarkupError on `[LINK=…` and drops `[B]…` text → RED (`evidence/inc003-red-on-base.txt`, 11 failed).

### HLR-006 — A `/`-filtered gantt or kanban keeps its panel height
- **Traceability:** US-005
- **Ledger:** none
- **Statement:** While a `/` filter is active, the gantt and kanban views shall be exactly the panel's height, with the filter bar inserted under the header, so that the gantt's time scale stays on screen.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_gantt.py -k filtered`
- **Numeric pass threshold:** filtered view rows == panel height (20); the unfiltered scale row is among them; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the time scale stays visible under a filter.
  - **Shipped surface:** `render_view` as the app calls it with `search_query`.
  - **Acceptance test(s):** AT-008
  - **Boundary catalog (QC-3):** ☑ boundary (gantt and kanban, 20-row panel) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** drawing the filtered view at full height → 22 rows → RED (`evidence/inc004-red-on-base.txt`).

### HLR-007 — The Focus Board cursor stays on a drawn card
- **Traceability:** US-006
- **Ledger:** none
- **Statement:** While the Focus Board is shown, the selection shall rest only on a task the Focus Board draws (pinned tasks and tasks of pinned projects).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q tests/test_focus.py -k unpinning`
- **Numeric pass threshold:** after unpinning the selected card the selection is the remaining drawn card; a second `t` empties the board; 0 failures.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `t` twice empties a two-card Focus Board.
  - **Shipped surface:** `TaskboardApp` keys `5`, `t`.
  - **Acceptance test(s):** AT-009
  - **Boundary catalog (QC-3):** ☑ boundary (last card unpinned) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A
  - **Negative control:** the base `app.py` keeps the cursor on the removed card → RED (`evidence/inc005-red-on-base.txt`).

## 4. Low-level requirements (LLR)

### LLR-001.1 — Chip row keeps every control reachable
- **Traceability:** HLR-001
- **Ledger:** none
- **Statement:** The `TaskModal` chip row shall lay out on one row when the screen is at least `TASK_CHIPS_ONE_ROW` columns wide and on two rows below it (NEW — created in Phase 3; value fixed at P3 by measurement), keeping every chip fully visible from 80 to 140 columns.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_edit_window.py -k chip`
- **Numeric pass threshold:** for widths 80..140 step 4 plus `TASK_CHIPS_ONE_ROW` − 1 and `TASK_CHIPS_ONE_ROW`, at height 36 (and 80×24), every chip fully visible, the chip set read from the chip container (≥ 10); 0 failures.
- **Negative control:** forcing the one-row layout at 80 columns clips `f-pinned` → RED (P3).
- **Boundary catalog:** ☑ boundary (the threshold column and one below) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-001.2 — Visible focus mark on one-row fields
- **Traceability:** HLR-001
- **Ledger:** none
- **Statement:** Every one-row focusable control of the editor (title, selects, dates, flags, calendar and footer buttons) shall show an accent left bar while focused and no accent bar while unfocused.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_edit_window.py -k focus_mark`
- **Numeric pass threshold:** for each control, focused left-border colour == `HEX["accent"]` and every other control's != it; the painted screen carries the accent bar on the focused control; 0 failures. The notes/URLs/images TextAreas are multi-row and keep their tall focus border (not in this set).
- **Negative control:** deleting the `:focus` rule → RED (P3).
- **Boundary catalog:** none — no input class applies: a style read-back per control

### LLR-001.3 — Contract preserved
- **Traceability:** HLR-001
- **Ledger:** none
- **Statement:** The `TaskModal` shall keep all 17 widget ids, the `_save` payload keys and values, the escape / ctrl+v / ctrl+e bindings, the calendar buttons and paste-image, and the `.modal-title` label naming ctrl+e.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_edit_window.py -k save_payload` plus existing `tests/test_app.py` (ctrl+v, calendar) and `tests/test_emoji_picker.py` nodes
- **Numeric pass threshold:** payload equals the expected dict built from edited values; existing nodes green; 0 failures.
- **Negative control:** dropping `pinned` from the payload → RED (P3).
- **Boundary catalog:** ☑ empty (new task: id is the image key, title "Untitled") ☐ boundary — N/A ☐ invalid — N/A: url validation is unchanged and covered by existing tests ☐ error — N/A

### LLR-001.4 — ProjectModal untouched
- **Traceability:** HLR-001
- **Ledger:** none
- **Statement:** The editor's full-screen rules shall be scoped to the task editor so that `ProjectModal` keeps its 62-column `.modal` box.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_edit_window.py -k project_modal`
- **Numeric pass threshold:** ProjectModal box outer width == 62 at 120×36; 0 failures.
- **Negative control:** styling `#modal-box` instead of the task box widens ProjectModal → RED (P3).
- **Boundary catalog:** none — one fixed size checks the scoping

### LLR-002.1 — Preview rendering
- **Traceability:** HLR-002
- **Ledger:** none
- **Statement:** The preview shall render each notes line through `_highlight_markup` (`views.py:2613`) and shall be refreshed on every `TextArea.Changed` from `#f-notes`.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_edit_window.py -k preview`
- **Numeric pass threshold:** preview spans contain the new text in `over`; 0 failures.
- **Negative control:** handler removed → stale preview → RED (P3).
- **Boundary catalog:** ☑ empty ☑ boundary (unclosed marker) ☐ invalid — N/A ☐ error — N/A

### LLR-003.1 — The band lives in the ordering seat
- **Traceability:** HLR-003
- **Ledger:** none
- **Statement:** `kanban_order` (`views.py:3961`) shall accept a keyword `band` (NEW) and, when true and the group mode is not `priority`, shall return the column's open high-priority cards as a first group named by the constant `KANBAN_BAND` (NEW), followed by the remaining groups without those cards, empty groups omitted; with `band` false it shall return exactly what it returns today.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_priority.py -k seat`
- **Numeric pass threshold:** band ids == open high ids in seat order; band absent for group=priority, collapsed, no high; band=False identical to base output; 0 failures.
- **Negative control:** band built from all high (done included) → RED on the done-high arm (P3).
- **Boundary catalog:** ☑ empty ☑ boundary (done high, archived high, blocked high, focus filter, collapsed) ☐ invalid — N/A ☐ error — N/A

### LLR-003.2 — Grouped renderer and navigator both ask for the band; lanes and matrix do not
- **Traceability:** HLR-003
- **Ledger:** none
- **Statement:** `_kanban_column_rows` and the grouped branch of `nav_model` shall call `kanban_order(..., band=True)`; the lanes and matrix paths shall not; the renderer shall draw the band as a non-selectable `── high ──` divider row, the cards, and a non-selectable closing rule.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_kanban_priority.py -k band`
- **Numeric pass threshold:** per column nav ids == line_map-row-ordered ids; lanes/matrix output contains no band divider and no NUL; 0 failures.
- **Negative control:** nav without band while render has it → order mismatch → RED (P3).
- **Boundary catalog:** ☑ boundary (lanes, matrix, group=priority) ☐ empty — covered by LLR-003.1 ☐ invalid — N/A ☐ error — N/A

### LLR-004.1 — Badge in `card_cell`
- **Traceability:** HLR-004
- **Ledger:** none
- **Statement:** `card_cell` (`views.py:309`) shall accept a keyword `badge` (NEW); when true and the card is open it shall draw the priority badge plus one space between the prefix and the title and shall not add the `!` token; the cell shall stay exactly `wc` cells; the kanban grouped and lanes callers shall pass `badge=True`.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_priority.py -k badge`
- **Numeric pass threshold:** markup carries `reverse` + the tone hex + the token; cell_len == wc for wc in 0..40; 0 failures.
- **Negative control:** badge on a done card → RED (P3).
- **Boundary catalog:** ☑ boundary (wc smaller than prefix+badge) ☑ empty (wc 0) ☐ invalid — N/A: unknown priority → normal ☐ error — N/A

### LLR-004.2 — Legend and help say what is drawn
- **Traceability:** HLR-004
- **Ledger:** none
- **Statement:** The kanban legend shall list the `!!`, `==`, `++` badges each only when a visible open card of that priority exists and shall not list the `!` token; the kanban help example shall show a badge instead of `!`, and the kanban help usage shall say the band appears in the grouped presentation only.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_kanban_priority.py -k legend`
- **Numeric pass threshold:** entries present/absent per board; existing ghost-mark law green; 0 failures.
- **Negative control:** legend keeps `!` → RED (P3).
- **Boundary catalog:** ☑ empty (no open normal → no `==` entry) ☐ boundary — N/A ☐ invalid — N/A ☐ error — N/A

### LLR-005.1 — Task text reaches Textual widgets only as a Rich `Text`
- **Traceability:** HLR-005
- **Ledger:** none
- **Statement:** `TaskDetails` and `image_block` (`taskboard/modals.py`) shall pass every label holding escaped task text through `_rich` (NEW — created in Phase 3), and `TaskDetails` shall render the notes with `notes_preview`.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_details_markup.py`
- **Numeric pass threshold:** 21 nodes pass; mutations N1–N6 KILLED.
- **Negative control:** any one label handed back as a str → its field's arms RED (N1–N5).
- **Boundary catalog:** ☑ invalid (four Textual-tag shapes) ☑ boundary (five fields) ☐ empty — N/A ☐ error — N/A

### LLR-006.1 — Filtered views are drawn two rows shorter
- **Traceability:** HLR-006
- **Ledger:** none
- **Statement:** `render_view` (`taskboard/views.py`) shall render a filtered gantt or kanban at `bar_h = max(1, height - 2)` when a height is given.
- **Validation:** `test (unit)`
- **Executed verification:** `pytest tests/test_gantt.py -k filtered`
- **Numeric pass threshold:** 2 nodes pass.
- **Negative control:** `bar_h` replaced by `height` → both RED.
- **Boundary catalog:** ☑ boundary (height 20) ☐ empty — N/A: `height=0` keeps 0 by construction ☐ invalid — N/A ☐ error — N/A

### LLR-007.1 — `_select_first` reads the Focus Board's own task set
- **Traceability:** HLR-007
- **Ledger:** none
- **Statement:** `TaskboardApp._select_first` (`taskboard/app.py`) shall, in the focus view, choose among `focus_tasks(board, show_archived)`.
- **Validation:** `test (integration)`
- **Executed verification:** `pytest tests/test_focus.py -k unpinning`
- **Numeric pass threshold:** 1 node passes.
- **Negative control:** base `app.py` → RED.
- **Boundary catalog:** ☑ boundary (last card) ☐ empty — N/A ☐ invalid — N/A ☐ error — N/A

## 5. Validation strategy
Layer A (TC) and Layer B (AT) are pytest nodes in `tests/test_edit_window.py` and
`tests/test_kanban_priority.py` (NEW — created in Phase 3); file names, `-k` selectors and
node ids are provisional until P3 (V-5). Full suite `python -m pytest -q` at close; baseline
1336 passed (operator figure, re-measured at P3).

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new test that asserts NEW behaviour shown RED on the base tree; preservation tests (LLR-001.3 payload, LLR-001.4 ProjectModal, `band=False` identity) are GREEN on base by design and are shown RED under their named mutation instead.
- full suite: 0 failures beyond any pre-existing flake, named.

## 6. Appendices

### 6.2 Relevant design decisions
- D1: the band applies only in the grouped presentation, and not with group=priority (the High group already is the band). Lanes: lanes are themselves a grouping axis with height-capped cells; a band there would have to be a pseudo-lane named by a sentinel, and with group=priority would duplicate the HIGH lane. Matrix draws no cards, only per-project counts, so there is nothing to float.
- D2: badges in grouped and lanes (both draw `card_cell`), not matrix (no cards drawn).
- D3: archived counts as not open (no badge, no band) — archived is terminal (`status_glyph`).
- D4: the Focus review rail and People view keep the `!` ink token; the commission names the kanban only.

### 6.1 Verification beyond automation (UX-11)
- automated walkthrough (AT-005, tab order) — planned; owner's own walkthrough at 80×24 — planned (PNG review); evaluation with other users — n/a — one-person product.

### 6.3 Open risks
- The badge costs 3 cells on every open card: net −3 title cells on normal/low cards, net −1 on high (the 2-cell ` !` token is freed); at 80 columns titles were already 2–13 chars (measured, P-5).
- `++` wears `green`, which is also an offered project hue (`models.py` PROJECT_COLORS): on a green project the `▊` stripe and the low badge share a hue — found at P2 (Q-2); accepted by the owner 2026-09-30 (LED .5).
- A blocked high card shows `▲` in `over` beside `!!` in `over` (Q-13).
- Legend ghosts the legend cannot see (it is presentation-, focus- and collapse-blind today): under a project focus or in matrix the legend can list a badge no card draws. Pre-existing class (the `!` entry had it); fixing it needs `app.py`/`HelpModal` plumbing — out of scope, BACKLOG. Collapse cannot ghost: only the last (done) phase collapses and done cards wear no badge.
- A column taller than the viewport: the band does not change the existing scroll-to-cursor mechanism; not separately tested (declared, UX-9).
- Colour conflicts accepted by owner 2026-09-30: `==` yellow = due-today amber family; `!!` red sits beside the overdue `-Nd` chip in `over`.

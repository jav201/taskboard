# Requirements Document — taskboard — Batch 2026-10-19-batch-01

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/req-template.md` and its part 2, `templates/guides/req-template.part2.md`, explain each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose
The live contract for batch 2026-10-19-batch-01: Present view 3 `all` — every shown project on one date ruler beside a project rail (variant C, "curate rail", of the prototype round `prototypes/present_portfolio/`), with hiding and re-showing projects and tasks, a persisted presentation order, folding and a `u` picker of hidden items in all three Present views; and the shipped bug the round found in views 1/2 (a start-less milestone drawn as a bar from today).

### 1.2 Scope
In: `models` — `Project.show_in_present`, `Project.present_rank`, their load/save rule, the presentation order; `views` — the milestone row of the presentation, the view-3 renderer (timeline, rail, fold, narrow fallback), the hidden-items rows; `app.PresentScreen` — view 3 (`3`, `tab` cycling 1 → 2 → 3), its cursor, its keys (`space`, `a`, `shift+↑/↓`, `enter`, `←/→`), the hint row's three view names and `u` count, `x` in view 3, `u`; `modals` — the hidden-items picker; the tests these change (law-driven updates named in each packet's census); `README.md`, `docs/ARCHITECTURE.md`, `.dev-flow/BACKLOG.md` (docs). Out: the board gantt, lanes, kanban and every other view's project order (they keep board order); variants A and B of the round; B's ticks on folded headers; remembering folds or the last view across `R` presses; the `?` help modal (it lists the main screen's keys only; the presentation's keys live in its hint row — see §6.3); pushing to any remote.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| view 3 / `all` | the third view of the presentation (`R`): every shown project of the board on one date ruler |
| shown project | a visible (not archived) project whose `show_in_present` is true |
| presentation order | the order of the visible projects in view 3: projects with a `present_rank` first, by rank, then those without one, board order breaking ties |
| rail | the left column of view 3 (24 cells and a `│` divider) listing every visible project in presentation order, numbered, `●` shown / `○` hidden; drawn only at 100 columns or more |
| timeline | view 3 without its rail: the header, the ruler, and per shown project a header row and its shown open tasks |
| fold | a project drawn as its header row only; by hand (`enter`), or automatically when the rows do not fit (the projects furthest from the cursor's first) |
| picker | the modal `u` opens, listing the hidden items with a toggle |
| round | `prototypes/present_portfolio/` — `portfolio_proto.py` (the renderer), `app_capture.py` (the screen), `fixture.py`, `out/`, the verdict page |

### 1.4 References
- The operator's verdict on the round, 2026-10-19 (the commission): «C: Me parece la mejor opción para mis objetivos.» · «Sí, que persista el orden.» · «Siempre la traigo con (a), pero sería útil tener el seleccionador propuesto con (u)». The earlier commission: «necesito que en el modo presentación pueda tener la vista del gantt con todos los proyectos… esconder tareas o proyectos… reordenar los proyectos en el orden que mejor me convenga.»
- The orchestrator's decisions D1–D8 (the commission; `PLAN.md` §Key decisions).
- The round: `prototypes/present_portfolio/portfolio_proto.py` (`ordered`, `layout`, `timeline_lines`, `rail_lines`, `render`), `app_capture.py` (`PortfolioScreen`), `out/C-*.svg`.
- The presentation in the canon: HLR-1602, HLR-1803, LLR-1803.1..1803.3, HLR-1904, LLR-1904.1, HLR-2002, LLR-2002.1; `taskboard/app.py:181-418`, `taskboard/views.py:6038-6600`; the board gantt's milestone row `views.py:3032-3040`.

### 1.5 Document overview
§2 the stories, premises and fork preconditions; §3 six HLRs; §4 six LLRs and the information-flow contract; §5 the validation strategy.

---

## 2. Overall description

### 2.1 Product perspective
The presentation (`R`) gains a third view next to `1 gantt` and `2 split`, and a picker. The data model gains two optional project keys. The board's other views are untouched.

### 2.2 Product functions
1. A milestone reads as a `◆` on its date in every presentation view, never as a bar.
2. View 3 shows the portfolio: every shown project and its open work on one ruler, a rail to curate it.
3. The presenter hides and re-shows projects and tasks, folds projects and reorders them; hiding and the order are saved on the board.
4. `u` lists what is hidden, in every view, and brings items back one by one.

### 2.3 User characteristics
A presenter in the real app, keyboard only, on a shared screen or projector; usually at 118 columns or more; at times at 80×24. The operator brings hidden items back with `a` («Siempre la traigo con (a)»).

### 2.4 Constraints
Textual + Rich as shipped; no new dependency; every frame row exactly `width` cells and exactly `height` rows; every board-file string escaped before it enters markup, or appended to a `Text` as plain text (S1/C8); a board with nothing hidden and no rank keeps its bytes on load + save; the round's committed files are not rewritten; synthetic data only; the operator's name nowhere.

### 2.5 Assumptions and dependencies
The round's fixture (`prototypes/present_portfolio/fixture.py`) is copied into `tests/present_portfolio_board.py` (its board unchanged; Security Audit hidden through `Project.extra` at increment 001, as the round did, and through the new field from increment 002) so the suite does not import a prototype. Microsoft Edge is present for the PNG renders of the captures (`views._find_msedge()`).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-2101 | As a presenter, I want a milestone with no start date to read as a `◆` on its date in the presentation, as on the board's gantt, so that the room does not read a milestone as weeks of work. | the round's finding ("Cut-over weekend" drawn from today to Oct 25 in view 1); D7 | READY |
| US-2102 | As a presenter, I want a presentation view with the gantt of all my projects at once, so that I can walk the room through the whole portfolio. | the commission «la vista del gantt con todos los proyectos»; the verdict «C»; D1, D5, D6 | READY |
| US-2103 | As a presenter, I want to hide projects or tasks and to put the projects in the order that suits me, kept for the next time, so that I present only what matters in my order. | the commission «esconder tareas o proyectos… reordenar»; the verdict «Sí, que persista el orden»; D2, D3 | READY |
| US-2104 | As a presenter, I want a list of what is hidden on `u`, in every view, so that I can bring back one item without showing everything. | the verdict «sería útil tener el seleccionador propuesto con (u)»; D4 | READY |

#### Refinement log (one block per story)

**US-2101 — the milestone reads as a milestone**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter (and the room) · outcome = a milestone's field row in views 1/2 (and 3) shows `◆` on its due and the date beside it, the chip `due <Mon D>`, the label marked `◆`; never a bar · why = on `base_ref` "Cut-over weekend" (no start, due in 6 days) is drawn as a 7-day bar from today (P-1) · out of scope = the ruler's echo for a milestone cursor (as the board gantt), the brief rows
- **Feasibility (E, S):** implementation path = a milestone branch in `views._present_task_row` built on the board gantt's `gantt_milestone_cells` (the round's `task_row`) · dependencies/unknowns = none · fits one batch? = yes, one increment, 1 source file
- **Evaluability (T) — behavioral, black-box:** When the presenter opens `R` on the round's board with the cursor in Billing Migration, the "Cut-over weekend" row shows one `◆` at its due's column and no bar glyph (AT-2101).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2102 — the portfolio view**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter · outcome = `3` (and `tab` from view 2) shows view 3: a header (`◆ PRESENT · N projects  all`, open and late counts), the ruler fitted to the open work of the shown projects, per shown project in presentation order a header row (caret, colour, name, counts, its span, its chip) and its shown open tasks; a rail at 100 columns or more; folds when the rows do not fit; `x` exports the timeline without the rail to `present-board-<date>-all.svg/.png` · why = the commission and the verdict (C) · out of scope = variants A/B, B's ticks
- **Feasibility (E, S):** implementation path = the round's renderer (`portfolio_proto.py`, the A/C path) moved into `views` as one function; the round's screen (`app_capture.py`) folded into `PresentScreen` · dependencies/unknowns = US-2103's model fields (increment 002 before 003) · fits one batch? = yes, two increments: the renderer (003, 1 source file), the screen (004)
- **Evaluability (T) — behavioral, black-box:** When the presenter presses `R` then `3` at 160×45, the frame lists every shown project's name in presentation order with its open tasks, the rail lists every project numbered with `○` on the hidden one; at 80×24 there is no rail; `x` writes a `-all` SVG holding the projects and not the rail's `PROJECTS` (AT-2103, AT-2104).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2103 — curate the portfolio, kept for next time**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter · outcome = in view 3 `space` hides the cursor's row (a task, or a project on its header; on the rail `space` toggles `●`/`○`), `a` shows every hidden project and task, `shift+↑/↓` moves the cursor's project in the presentation order, `enter` folds or unfolds a project, `←/→` move the focus between rail and timeline; hiding and the order are saved at once and survive a restart; the board's own views keep board order · why = the commission, «que persista el orden» · out of scope = remembering folds; reordering the board itself
- **Feasibility (E, S):** implementation path = two optional `Project` fields with the `Task.show_in_present` save rule (increment 002); the keys in `PresentScreen` (increment 004) · dependencies/unknowns = none (P-2, P-3) · fits one batch? = yes, two increments
- **Evaluability (T) — behavioral, black-box:** When the presenter hides a project and moves another to the top, then restarts the app, view 3 shows the same order without the hidden project, and the board's gantt still lists the projects in board order (AT-2102, AT-2105).
- **Open questions:** none.
- **Classification:** `READY`.

**US-2104 — the hidden-items picker**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = a presenter · outcome = `u` in any view opens a picker listing the hidden items (view 1/2: the current project's hidden tasks; view 3: every hidden project and every hidden task, grouped under its project), `space`/`enter` toggles the row (saved at once), `esc` closes and the presentation repaints; the hint row says `u N hidden` when something is hidden · why = the verdict's note · out of scope = editing anything but the show flags
- **Feasibility (E, S):** implementation path = its rows in `views` (increment 003), one `ModalScreen` in `modals` and the key in `app` (increment 004) · dependencies/unknowns = none · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter hides two tasks in view 1, presses `u`, toggles one and closes, the frame shows that task again and the other stays hidden (AT-2106).
- **Open questions:** none.
- **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | On `base_ref`, `render_present` draws a milestone with no start date as a bar from today to its due | premise | TRUE | probe `evidence/premises.py` on `base_ref`: `render_present(round board, "pbm", "tb3", 2026-10-19, 118, 30)` → the row `▎ Cut-over weekend ↳······┆·············━━━━━━━━━━━━━○┆…  due Oct 25` (bar glyphs from the today column to the due) — `evidence/premises.txt` | HLR-2101 |
| P-2 | `Board._to_dict` drops `show_in_present` when it is `True` for any record that has the field, so a `Project` field of that name gets the task's save rule without a new branch | premise | TRUE | `taskboard/models.py:1000-1001` `if d.get("show_in_present") is True: del d["show_in_present"]`, applied to every project and task (`:1007-1008`) | LLR-2102.1 adds only `present_rank`'s omission |
| P-3 | No shipped view other than the presentation reads a project order other than `board.projects` | premise | TRUE | `grep -rn "present_rank" taskboard/` → no hit (`evidence/premises.txt`); `visible_projects` returns `board.projects` in order (`models.py:1122-1123`) | the board's views keep board order (HLR-2102) |
| P-4 | The round's variant C at 80 columns leaves the rail's project names 10 cells and the field 26 | premise | TRUE | `prototypes/present_portfolio/portfolio_proto.py`: `rail_w(80)` → 18, the name `fit(p.name, rw - 8)` → 10 cells; `_present_cols(80 - 19, False)` → field `61 - 20 - 2 - 13 = 26` (`evidence/premises.txt`) | below 100 columns no rail (D5) |
| P-5 | Tests pin the hint row's two view names and its ` · N hidden` tail literally | premise | TRUE | `tests/test_present_narrow.py:87` (`NAMES2, NAMES1 = "1 gantt  2 split  ", "1 gantt 2 split "`), `tests/test_present_polish.py:201-236`, `tests/test_present_views_app.py:268-277`, `tests/test_present_hide.py:230-233` and AT-1602's `endswith("· 1 hidden")` | law-driven updates in increment 004's census (TC-1904 and its overflow arm, AT-1904, TC-1808, TC-2002, AT-2002, TC-1604, AT-1602, AT-1803), each new value derived from the wording strings, never from the code under test |
| P-6 | `R` always opens the presentation on view 1, on the selected task's project | premise | TRUE | `taskboard/app.py:245` `self._view = 0`; `app.py:853-867` `present_project_id(...)` | view 3 is entered with `3` or `tab` (HLR-2104) |
| P-7 | `present_paths(board, None, today, "all")` names `present-board-<YYYY-MM-DD>-all.svg/.png` | premise | TRUE | `taskboard/views.py:6550-6561`: the slug of `None` is `board`, `tail = "-all"` for a view other than `gantt` (`evidence/premises.txt`) | the view-3 export name (HLR-2104) |

- **Premise evaluation:** 7 premise(s) · ✅ TRUE ×7

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: four increments in order on one branch, one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-2101 — A milestone in the presentation is a `◆` on its date
- **Traceability:** US-2101
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** When the presentation paints a field row for a milestone task, the system shall draw it as the board's gantt draws a milestone — `◆` on its due and the due's date beside it, nothing when it has no due or when the field is under 3 cells — and never as a bar, whatever its start date; the row's chip shall read its due alone (`due <Mon D>`, `no dates` without one), and its label shall carry `◆` before the title.
- **Rationale (informative):** a milestone has one date and no duration (D-603); a bar from today reads as work in progress.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_milestone.py`
- **Numeric pass threshold:** AT-2101: the round's board saved to disk, the app at 118×31 with the calendar frozen on 2026-10-19 (`app.date`, `models.date`), the selected task `Tax rules for new regions`, `R`: in `#present-frame` the row holding `Cut-over weekend` holds exactly one `◆` in its field (cells 31–103), in the same column as the `◆` of the project row `▌ BILLING MIGRATION` (the project's due, Oct 25, is the milestone's day), and no bar glyph in its field — none of `╌` (a task's reach), `━` (the critical chain), `▬` (the flow packet) or a phase tip `○ ◔ ◑ ◕`; its chip reads `due Oct 25` (true on `base_ref` too — the glyph and column checks are the discriminating ones); `2` (the split view) → the same row, the same checks.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the milestone row shows a diamond on its date, not a bar.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame` (and the `x` export, which writes the same frame).
  - **Acceptance test(s):** AT-2101
  - **Boundary catalog (QC-3):** ☑ boundary (a milestone given a start date; a 36-column frame, whose 1-cell field holds no `◆`, as the gantt's) ☑ empty (a milestone with no due: an empty field and `no dates`) ☐ invalid — none: dates are parsed by the shipped `parse_iso` ☐ error — none
  - **Negative control:** on `base_ref` AT-2101 is RED: the row is a bar from today (`evidence/red-001.txt` — planned).

### HLR-2102 — A project's presentation state is saved on the board
- **Traceability:** US-2103
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** The system shall keep, per project, whether it is shown in view 3 of the presentation (shown by default; views 1/2 present any project) and its place in the presentation order (none by default), save both in the board file — the shown flag only as the JSON `false`, the place only as an integer — and read them back on load, a record's shown flag being false only for the JSON `false` and its place being kept only for an integer that is not a boolean, never raising on any other value; the presentation order shall be the projects with a place first, by place, then the others, board order breaking ties; the place shall never be painted; a project a team pull adds to the board shall arrive shown and unplaced, whatever `team.json` holds; every other view shall keep the board's project order.
- **Rationale (informative):** «Sí, que persista el orden»; a presentation-only order keeps the board gantt untouched (the round's before/after, D2); a teammate's `team.json` never curates this board's presentation (security review S-4).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2102 or AT_2102"`
- **Numeric pass threshold:** AT-2102: the round's board saved to disk, the app at 160×45, calendar frozen, the selected task `Tax rules for new regions`, `R`, `3` (the rail's cursor on Billing Migration), `↓` (Mobile Release 3.2), `shift+↑` ×2, `↓` until the rail's cursor is on Brand Refresh, `space` → the file's projects carry `present_rank` Mobile Release 3.2 0, Customer Portal 1, Billing Migration 2, Data Platform 3, Security Audit 4, Brand Refresh 5, and `"show_in_present": false` on Security Audit and Brand Refresh only; the app restarted, `R`, `3` → the timeline's project headers read Mobile Release 3.2, Customer Portal, Billing Migration, Data Platform in that order and the rail marks Brand Refresh `○`; `esc`, `3` (the main screen's gantt) → the project groups that it lists appear in board order (Customer Portal before Billing Migration before Mobile Release 3.2 before Data Platform).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the presentation order and the hidden projects survive a restart; the board gantt's order does not change.
  - **Shipped surface:** `board.json` written by the app; `PresentScreen` view 3 after a restart; the main screen's gantt.
  - **Acceptance test(s):** AT-2102
  - **Boundary catalog (QC-3):** ☑ boundary (rank 0; a negative rank; duplicate ranks; projects without a rank after ranked ones) ☑ empty (no key at all: shown, unranked, bytes kept) ☑ invalid (`present_rank` `true`, `false`, `"2"`, `2.5`, `1.0`, `null`, `[]`; `show_in_present` `0`, `"false"`, `null`) ☐ error — none: the load rule never raises
  - **Negative control:** on `base_ref` AT-2102 is RED: there is no view 3 and `Project` has no such field (`evidence/red-004.txt` — planned; AT-2102 lands with increment 004, which ships the keys it drives).

### HLR-2103 — View 3 draws every shown project on one ruler
- **Traceability:** US-2102
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2, LED-2026-10-19-batch-01.3
- **Statement:** When the presentation shows view 3, the system shall paint a header naming the shown projects' count and the view word `all`, with the open and past-due counts of their shown open tasks; the two-row ruler on one axis fitted to the open work of the shown projects (the gantt window rule), its tick row echoing the cursor's exact dates — a task's, or on a project header its project's span labelled `project span ▸`; then, in presentation order, per shown project a header row (`▾` open / `▸` folded, `■` in its colour, its name, its open count, late count and countdown as room allows, its span with `◆` due and `●` progress, its start–end chip) followed, unless folded, by its shown open tasks as the presentation's task rows; a blank row between projects when every row fits; when the rows do not fit, the projects furthest from the cursor's (never the cursor's own) folded to their header, then `+N more rows not shown`; at 100 columns or more a 24-cell rail and a `│` divider at the left, listing every visible project in presentation order — numbered by position, `●` shown / `○` hidden, the name cut to 16 cells, the cursor's project marked (`▶` with the rail's focus, `›` without) — and under it `<S> shown · <H> hidden` and, when any, `<T> task(s) hidden` (the hidden tasks of every visible project); below 100 columns no rail, the timeline taking the full width; below 36 columns the narrow frame of HLR-1903. Every project name and task title shall paint literally, whatever markup characters it holds.
- **Rationale (informative):** variant C of the round (the operator's verdict «C»); the rail dropped below 100 columns (P-4, D5).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2103 or AT_2103"`
- **Numeric pass threshold:** AT-2103: the round's board saved to disk, calendar frozen, the selected task `Tax rules for new regions`, `R`, `3`: at 160×45 the frame's first row starts (after the rail) `◆ PRESENT · 5 projects  all` and ends (right-stripped) `23 open · ▲2 past due`; the timeline's project headers read Customer Portal, Billing Migration, Mobile Release 3.2, Data Platform, Brand Refresh in that order, every shown open task title is in the frame, and no row holds `Threat model review`, `Help-center links` or `Cost dashboards`; the rail's rows read `  1 ● Customer Portal`, `▶ 2 ● Billing Migrati…`, `  3 ● Mobile Release …`, `  4 ● Data Platform`, `  5 ○ Security Audit`, `  6 ● Brand Refresh` (as their first cells: the lead cell, then the number right-aligned in two), then ` 5 shown · 1 hidden` and ` 2 tasks hidden`; at 118×30 the rail is drawn and every row is exactly 118 cells; at 80×24 no row holds `PROJECTS` or `│` and every row is exactly 80 cells.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the portfolio on one ruler, the rail beside it on wide screens.
  - **Shipped surface:** `R` → `3` → `PresentScreen` `#present-frame`.
  - **Acceptance test(s):** AT-2103
  - **Boundary catalog (QC-3):** ☑ boundary (99/100 columns: the rail appears; 36 columns; rows that just fit vs one row too many: an auto-fold) ☑ empty (every project hidden: the header and ruler only; a project with no dates; a project with no open task) ☑ invalid (`[@click=app.quit]x[/]`, a trailing `\`, `[bold` and `x[/]` in a project name and a task title paint literally, no `@click` meta in any span, no `MarkupError` — security review S-2) ☐ error — none
  - **Negative control:** on `base_ref` AT-2103 is RED: `3` does nothing in the presentation (`evidence/red-004.txt` — planned).

### HLR-2104 — View 3 is reached, left and exported like the others
- **Traceability:** US-2102
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** While the presentation is open, the system shall show view 3 on `3`, and `tab` / `shift+tab` shall cycle 1 → 2 → 3 → 1 (and back); entering view 3 shall put the cursor on the current project — on the rail where the rail is drawn; else on the views-1/2 cursor task's row when it is drawn, else on its project's header when drawn, else on the first drawn row; leaving view 3 shall show, in views 1/2, the cursor's project (hidden from view 3 or not) with the cursor's task; `↑/↓` shall move the cursor over the focus's rows (the rail's projects, or the timeline's drawn header and task rows), `←/→` shall move the focus between rail and timeline where the rail is drawn and otherwise move the cursor as `↑/↓`; `pgdn`/`pgup` shall do nothing in view 3, and `enter`, `shift+↑/↓` nothing in views 1/2; `x` in view 3 shall export the timeline without the rail to `present-board-<YYYY-MM-DD>-all.svg` and `.png`; the hint row shall name the three views (`1 gantt`, `2 split`, `3 all`), view 3's own keys in view 3, and, when something is hidden, ` · u N hidden` (views 1/2: the project's hidden tasks; view 3: the hidden projects plus the hidden tasks of every visible project), ` · N hidden` below 36 columns; `R` shall still open on view 1. The hint's other rules stand (HLR-1904, HLR-2002) — at 80 columns the split view's hint now takes the short wording with nothing hidden and the compact one with something hidden.
- **Rationale (informative):** the round's screen (`app_capture.py`) and D6; `u` named where it acts (D4); one count, so the view-3 wordings keep their labels at 118 columns (ux-reviewer UX-1).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2104 or AT_2104"`; `python -m pytest -q -p no:cacheprovider tests/test_present_narrow.py tests/test_present_polish.py tests/test_present_views_app.py tests/test_present_hide.py`
- **Numeric pass threshold:** AT-2104: the round's board saved to disk at 160×45, calendar frozen, the selected task `Tax rules for new regions`, `R` → the hint starts `1 gantt  2 split  3 all`, the `1 gantt` span bold; `tab` `tab` → view 3 (` all` in the header), the rail's `▶` on Billing Migration; `tab` → view 1, its header naming Billing Migration; `3`, `→` (the timeline: the cursor on Billing Migration's header, the tick row `project span ▸`), `↓` → the cursor on `Dual-run reconciliation`, the tick row's label `selected task ▸`; `1` → view 1 with `⟦Dual-run reconciliation⟧` as its brief cursor; `3`, `x` → exactly one `reports/present-board-2026-10-19-all.svg`, whose text holds every shown project's name and holds neither `PROJECTS` nor `shown ·` nor the hint; the hint in view 3 ends `· u 3 hidden` and holds `␣ hide`, `⇧↑↓` and `enter fold` (the middle wording at 160 columns at least).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the presenter moves between the three views with one cursor, exports view 3 without its rail, reads the keys in the hint.
  - **Shipped surface:** `PresentScreen` keys, `#present-frame`, `#present-hint`, `reports/`.
  - **Acceptance test(s):** AT-2104
  - **Boundary catalog (QC-3):** ☑ boundary (`shift+tab` from view 1 to view 3; 99 vs 100 columns for `←/→`; below 36 columns `3` does nothing and `x` notifies, as in views 1/2; entering view 3 below 100 columns on a hidden project: the first drawn row) ☑ empty (nothing hidden: no `u` in the hint) ☐ invalid — none ☐ error — none: the export's PNG step returns None without Edge, as shipped
  - **Negative control:** on `base_ref` AT-2104 is RED: `tab` from view 2 returns to view 1 and the hint names two views (`evidence/red-004.txt` — planned).

### HLR-2105 — The presenter curates view 3
- **Traceability:** US-2103
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** While view 3 is shown, `space` on the timeline shall hide the cursor's row from the presentation — a task (its `show_in_present`), or a project on its header (its `show_in_present`) — and move the cursor to the next drawn row (the previous at the end); on the rail `space` shall toggle the cursor project between shown and hidden, the cursor staying on it; `a` shall show every hidden project and every hidden task of the visible projects and say so in a notice (`Shown again: <P> project(s) + <T> task(s)`); `shift+↑` / `shift+↓` shall move the cursor's project one place up / down in the presentation order — among every project on the rail, among the shown projects on the timeline — and number every visible project's place densely from 0; `enter` on a project's header (or its rail row) shall fold or unfold it for the rest of the presentation, and do nothing on a task; each change of a flag or a place shall save the board at once, and a key that changes nothing shall write nothing.
- **Rationale (informative):** the round's keys (D3), the board's flags as in views 1/2 (HLR-1602); the toggle in place lets a second `space` undo the first (UX-2); `a` reaches every project's tasks, so it says what it brought back (UX-3).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2105 or AT_2105"`
- **Numeric pass threshold:** AT-2105: the round's board saved to disk at 160×45, calendar frozen, the selected task `Tax rules for new regions`, `R`, `3`, the file's bytes taken; `→` (the timeline), `↓` until the cursor is on Data Platform's header, `enter` → no row holds `Ingest pipeline v2`, the header's caret is `▸`, the file's bytes unchanged; `enter` → the task is back; `↑` until the cursor is on `Offline mode`, `space` → no row holds `Offline mode`, the file holds that task `"show_in_present": false`; `↓` until the cursor is on Brand Refresh's header, `space` → no timeline row holds `Brand Refresh`, the rail's row reads `○ Brand Refresh`, the file holds it `false`; `←` (the rail), `↓`/`↑` to Brand Refresh, `space` → `● Brand Refresh`, the rail's `▶` still on it, the file without its flag; `a` → a notice `Shown again: 1 project + 3 tasks`, the file holds no `show_in_present` key; `a` again → the file's bytes unchanged; `↑` until the rail's cursor is on the first project, `shift+↑` → the file's bytes unchanged.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** projects and tasks leave and come back, the order follows the presenter, folds open and close.
  - **Shipped surface:** `PresentScreen` view 3 keys; `board.json`; the notice.
  - **Acceptance test(s):** AT-2105
  - **Boundary catalog (QC-3):** ☑ boundary (`shift+↑` on the first / `shift+↓` on the last: nothing; hiding the last drawn row: the cursor moves up; hiding the last shown project: header and ruler only; `space` twice on the rail: back as it was) ☑ empty (`a` with nothing hidden; `space` with no cursor) ☐ invalid — none ☐ error — none
  - **Negative control:** on `base_ref` AT-2105 is RED: no view 3 (`evidence/red-004.txt` — planned).

### HLR-2106 — `u` lists what is hidden and brings items back one by one
- **Traceability:** US-2104
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** While the presentation is open at 36 columns or more, `u` shall open a picker titled `Hidden from the presentation` listing the hidden items — in views 1/2 the current project's hidden tasks; in view 3, in presentation order, each visible project that is hidden or holds hidden tasks, followed by its hidden tasks, indented — each row marked `○` hidden or `●` shown, every name and title painted literally; `↑/↓` shall move the picker's cursor, `space` / `enter` shall toggle the cursor row's show flag and save the board at once, the row staying listed with its new mark; `esc`, `q` or `u` shall close the picker and the presentation shall repaint; with nothing hidden the picker shall say `nothing hidden`.
- **Rationale (informative):** the operator's note «sería útil tener el seleccionador propuesto con (u)» (D4); `u` closes what it opened (UX-7).
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k "TC_2106 or AT_2106"`
- **Numeric pass threshold:** AT-2106: the round's board saved to disk at 118×31, calendar frozen, the selected task `Tax rules for new regions`, `R` (Billing Migration), `space` ×2 (`Tax rules for new regions` and the next task by due, `Refund edge cases`, hidden), `u` → the picker's rows (`#picker-rows`, its `Text`) read `○ Tax rules for new regions` and `○ Refund edge cases`; `space` on the first → `● Tax rules for new regions`, the file holds that task without the flag; `esc` → the frame shows `Tax rules for new regions` and not `Refund edge cases`; `3`, `u` → the rows Customer Portal, `Help-center links`, Billing Migration, `Refund edge cases`, Data Platform, `Cost dashboards`, Security Audit in that order, the three tasks and Security Audit `○`, the other projects `●`; `esc`, `a`, `u` → `nothing hidden`.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a list of the hidden items; one comes back without the others.
  - **Shipped surface:** `u` in `PresentScreen` → the picker; `board.json`; `#present-frame`.
  - **Acceptance test(s):** AT-2106
  - **Boundary catalog (QC-3):** ☑ boundary (toggle twice: hidden again; the first and last row; `u` closes) ☑ empty (nothing hidden) ☑ invalid (the S-2 payloads in a title are listed literally — C8) ☐ error — none
  - **Negative control:** on `base_ref` AT-2106 is RED: `u` does nothing in the presentation (`evidence/red-004.txt` — planned).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-2101.1 — The milestone branch of `_present_task_row`
- **Traceability:** HLR-2101
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** `views._present_task_row(task, board, p, cursor)` shall, for `task.milestone`, build the field from `gantt_milestone_cells(task, board, p.ax, p.today, milestone_tone(task, board, p.today))` — under the cursor its `◆` in `accent` — the label `" "` + (`⟦` in accent bold under the cursor, else `" "`) + `▎` in the hue + `" "` + `◆` in the milestone tone + `" "` + `_present_title(task, label_w - 6)`, and the chip `_present_chip(None, task.due_date, …)`; a task that is not a milestone shall be drawn as shipped.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_milestone.py -k TC_2101`
- **Numeric pass threshold:** TC-2101 passes: over the round's board, views 1 and 2, widths 36, 80, 118, 160, every open milestone of every project as the cursor and as a non-cursor row: the row's field holds every non-blank glyph of `gantt_milestone_cells` on the frame's axis in its cell and no bar glyph, as many `◆` as those cells (none at 36), the chip reads `due <Mon D>`, the label holds `◆`; the `◆` is bold `HEX["bright"]` (the accent echo) exactly under the cursor; a milestone given a start date is drawn the same, one with no due draws an empty field and `no dates`; a non-milestone row keeps its bar; the PRES-V3 frame tests (`tests/test_present_views.py`, `tests/test_present.py`, whose boards hold no milestone) stay green.
- **Negative control:** TC-2101 goes RED when the branch is removed (the bar returns), when the chip keeps the start date, and when the cursor's `◆` is not accented (mutations at increment 001 — planned).
- **Boundary catalog:** ☑ boundary (a start date; a 1-cell field at 36 columns) ☑ empty (no due) ☐ invalid — none ☐ error — none

### LLR-2102.1 — The project fields and the presentation order
- **Traceability:** HLR-2102
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** `models.Project` shall carry `show_in_present: bool = True` and `present_rank: int | None = None`, both in `_PROJECT_KEYS`; `Project.from_dict` shall read `show_in_present` as `d.get("show_in_present") is not False` and `present_rank` as the value when `isinstance(v, int) and not isinstance(v, bool)`, else `None`; `Board._to_dict` shall drop `present_rank` when it is `None` (the shipped `show_in_present is True` drop applies unchanged); `models` shall provide `present_order(board) -> list[Project]` (the visible projects sorted by `(rank is None, rank if rank is not None else 0, board index)`) and `set_present_order(board, ids)` (rank `i` on the project `ids[i]`); `team_sync`'s pull shall build a new project from the team entry without its `show_in_present` and `present_rank` keys.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2102`
- **Numeric pass threshold:** TC-2102 passes: the load table — `show_in_present` `false` → False; absent, `true`, `0`, `"false"`, `null` → True; `present_rank` `0`, `3`, `-3`, `10**300` → kept; absent, `null`, `true`, `false`, `"2"`, `2.5`, `1.0`, `[]` → None — no exception, neither key landing in `extra`; save: a default project writes neither key, a hidden one `"show_in_present": false`, a ranked one `"present_rank": n`; load + save of the PRES-V3 board and of the round's board with every flag shown keeps their bytes; `present_order` with ranks on two projects and four unranked → the two by rank, then the rest in board order; duplicate ranks → board order between them, stable over two calls; archived projects are not listed; `set_present_order` then `present_order` returns the ids given; a team pull of a new project whose entry holds `"show_in_present": false, "present_rank": 0` adds it shown and unranked.
- **Negative control:** TC-2102 goes RED when `present_rank` accepts a boolean, when `None` is written, when `show_in_present` is read truthy (`0` hides), when the unranked sort before the ranked, and when the pull keeps the keys (mutations at increment 002 — planned).
- **Boundary catalog:** ☑ boundary (rank 0; a negative rank; duplicates; a 300-digit rank) ☑ empty (no keys) ☑ invalid (the types above) ☐ error — none: `from_dict` never raises on these

### LLR-2103.1 — `render_present_all`
- **Traceability:** HLR-2103
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2, LED-2026-10-19-batch-01.4
- **Statement:** `views` shall provide `render_present_all(board, cursor, today, width, height, folded=frozenset(), rail_focus=False) -> PresentAll`, `cursor` a `("proj" | "task", id)` pair or None, returning `PresentAll(frame, timeline, timeline_w, stops, rail_stops, cursor)` — the painted frame (`height` × `width`), the timeline alone (`height` × `timeline_w`, what `x` exports), the timeline's drawn rows as cursor stops in screen order, the rail's stops (every visible project in `present_order`; empty below `PRESENT_RAIL_MIN` = 100 columns), and the cursor as drawn (None on the timeline while the rail's cursor is a hidden project; a task folded away → its project's header; else the first stop); built from the round's `geo`, `layout`, `timeline_lines`, `head_row`, `ruler`, `head` and `rail_lines` (the A/C path only, `PRESENT_RAIL_W` = 24), each task row through `_present_task_row`, every board-file string through `escape(fit(...))` (never `fit(escape(...))`); below `PRESENT_MIN_WIDTH` the narrow frame of `render_present`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2103`
- **Numeric pass threshold:** TC-2103 passes: over the round's board, the same board ranked in reverse with Data Platform hidden, and the PRES-V3 board × widths 36, 60, 80, 99, 100, 118, 160 × heights 10 and 45 × the cursor None, on each project header and on each project's first task × rail focus on/off × folded ∅ / {the first shown project}: exactly `height` rows of exactly `width` cells; every stop a row the frame draws (none under the overflow row) and the drawn cursor one of them; the rail present iff width ≥ 100; the timeline's project headers in `present_order` restricted to shown projects; hidden tasks and hidden projects' tasks absent; the cursor's project never auto-folded; a frame that holds every row has no `+N more rows not shown` and no auto-folded project; the frame's plain text at 160×45 and 118×30 with the round's starting state (the rail's cursor on Billing Migration) equals the round's C captures' text (`prototypes/present_portfolio/out/C-160-initial.svg`, `C-118-initial.svg`) row for row; the S-2 payloads in a project name and a task title paint literally with no `@click` in any span.
- **Negative control:** TC-2103 goes RED when the rail is drawn below 100 columns, when hidden projects reach the timeline, when the auto-fold may fold the cursor's project, when the order ignores `present_rank`, and when a name loses its `escape` (mutations at increment 003 — planned).
- **Boundary catalog:** ☑ boundary (99/100; rows exactly fitting) ☑ empty (all hidden; no dates; no open task) ☑ invalid (markup in a name) ☐ error — none

### LLR-2104.1 — `PresentScreen`'s third view
- **Traceability:** HLR-2104
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** `views` shall provide `PRESENT_SCREEN_VIEWS = PRESENT_VIEWS + ("all",)` (`PRESENT_VIEWS`, `render_present`'s views, unchanged); `app.PresentScreen` shall bind `3` → `view(2)` and `←/→` → `side(∓1)` with priority, index `_view` into `PRESENT_SCREEN_VIEWS` at every site (cycle modulo 3), hold the view-3 cursor, the folded project ids (session only) and the rail's focus (True on entering view 3 where the rail is drawn), keep `_paint`'s `update(self._frame_text())` with view 3 routed inside `_frame_text` through `render_present_all` (so the markup census's exempt key stands), export view 3 with `present_paths(board, None, today, "all")` writing `PresentAll.timeline` at `timeline_w`; `_hint` shall build the view names from `PRESENT_SCREEN_VIEWS` and the tail ` · u N hidden` (` · N hidden` below `PRESENT_MIN_WIDTH`), and in view 3 try the wordings `⇥ next · ↑↓ move · ←→ rail/timeline · ␣ hide · ⇧↑↓ reorder · enter fold · a show all · x export · esc leave`, `⇥ · ↑↓ · ←→ rail · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc`, `⇥ ↑↓ ←→ ␣ ⇧↑↓ enter a x esc`, `esc` where the rail is drawn, and `⇥ next · ←→ ↑↓ move · ␣ hide · ⇧↑↓ reorder · enter fold · a show all · x export · esc leave`, `⇥ · ←→ ↑↓ · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc`, `⇥ ←→ ↑↓ ␣ ⇧↑↓ enter a x esc`, `esc` where it is not — two-space gaps after the view names for the first two, one space for the others.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2104`
- **Numeric pass threshold:** TC-2104 passes: the cycle table (1 → 2 → 3 → 1, `shift+tab` reversed, `3` from 1 and 2); the cursor hand-off both ways (the task kept, the project picked, a hidden project's first drawn row); the hint for every view × widths 36–200 × hidden 0 / 1 / 3 equals the wording of a LITERAL first-width table (the census of packet 004 states how each first width was measured: `rich.cells.cell_len` over the literal strings, outside the code) plus the tail; `present_paths(..., "all")` ends `-all.svg`; TC-1904's table, TC-1904's overflow arm, AT-1904, TC-1808, TC-2002, AT-2002, TC-1604, AT-1602 and AT-1803 updated law-driven (census in packet 004, old → new).
- **Negative control:** TC-2104 goes RED when `tab` wraps after view 2, when the tail drops `u`, when leaving view 3 keeps the old project (mutations at increment 004 — planned); the export written with the rail is AT-2104's mutation.
- **Boundary catalog:** ☑ boundary (each wording's first width and one below; 99/100 for the rail wordings) ☑ empty (nothing hidden) ☐ invalid — none ☐ error — none

### LLR-2105.1 — View 3's curation actions
- **Traceability:** HLR-2105
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** `app.PresentScreen` shall bind `shift+up` → `reorder(-1)`, `shift+down` → `reorder(1)`, `enter` → `fold` with priority (each doing nothing outside view 3); in view 3 `action_hide` shall set the cursor task's or project's `show_in_present = False` on the timeline, save, and move the cursor to the next drawn stop after it, else the previous; on the rail it shall toggle the project's flag, save, and keep the cursor; `action_show_all` shall set every hidden visible project and every hidden task of the visible projects shown, save once and notify `Shown again: <P> project(s) + <T> task(s)` with `markup=False`, nothing when nothing was hidden; `action_reorder(d)` shall move the cursor's project `d` places in `present_order` (among every project on the rail, among the shown on the timeline), write the order with `set_present_order` and save, nothing at either end; `action_fold` shall toggle the cursor project's id among the folded, nothing on a task; `action_side` shall set the rail's focus where the rail is drawn (a task cursor becoming its project on the rail), else move; `pgdn`/`pgup` shall do nothing in view 3.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2105`
- **Numeric pass threshold:** TC-2105 passes: on a mounted screen over a saved board with `Board.save` counted: `space` on a task, on a header → one save each, the flags as stated, the cursor on the next stop (the previous at the end); `space` twice on the rail → two saves, hidden then shown, the cursor unmoved; `a` → one save, every flag true, one notice; `a` again → zero saves; `shift+↑` ×2 from the rail's 3rd project → it is first, the ranks 0..n-1 dense over the visible projects (hidden ones included); at the top → zero saves; on the timeline `shift+↓` passes over a hidden project; `enter` ×2 → folded then unfolded, zero saves; `enter` on a task, `enter` / `shift+↑` in views 1/2, `pgdn` in view 3 → zero saves and the frame unchanged.
- **Negative control:** TC-2105 goes RED when a key that changes nothing still saves, when the reorder ignores hidden projects on the rail, when the ranks are not dense, when `enter` saves, when the rail's `space` moves the cursor (mutations at increment 004 — planned).
- **Boundary catalog:** ☑ boundary (the ends of the order; the last stop) ☑ empty (no cursor; nothing hidden) ☐ invalid — none ☐ error — none

### LLR-2106.1 — The picker
- **Traceability:** HLR-2106
- **Ledger:** LED-2026-10-19-batch-01.1, LED-2026-10-19-batch-01.2
- **Statement:** `views` shall provide `present_hidden_rows(board, project_id, all_view) -> list[tuple[str, str, int]]` (`(kind, id, depth)`; views 1/2: the project's hidden tasks at depth 0; view 3: per project of `present_order` that is hidden or holds hidden tasks, the project at depth 0, then its hidden tasks at depth 1); `modals` shall provide `PresentHiddenPicker(board, rows)`, a `ModalScreen[None]` painting its title, one line per row — `○`/`●` and the name or title appended to a `Text` as plain text — in `#picker-rows`, a cursor row, and the keys line `↑↓ move · ␣ toggle · esc close`, every widget fed by a `Text` built without a parser or by a `-> Text` method of its own (no new exempt key in `tests/test_markup_census.py`); `space`/`enter` toggle the row object's `show_in_present` and `board.save()`; `esc`/`q`/`u` dismiss; `app.PresentScreen` shall bind `u` → `hidden_picker` with priority, push the picker with those rows (at 36 columns or more) and repaint on its dismissal.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_all.py -k TC_2106`
- **Numeric pass threshold:** TC-2106 passes: `present_hidden_rows` on the round's board → views 1/2 on Customer Portal `[("task", "tc6", 0)]`; view 3 `[("proj", "pcp", 0), ("task", "tc6", 1), ("proj", "pdp", 0), ("task", "td4", 1), ("proj", "psa", 0)]`; with every flag shown, `[]` (increment 003); the picker toggles one flag per keypress with one save each, the mark follows the flag, the rows stay; the S-2 payloads in a title paint literally; `nothing hidden` with no row; `tests/test_markup_census.py` green with its exempt keys unchanged (increment 004).
- **Negative control:** TC-2106 goes RED when the rows include a shown task, when a hidden project's own hidden tasks are dropped, when a toggle does not save, when the title is parsed as markup (mutations at increments 003 and 004 — planned).
- **Boundary catalog:** ☑ boundary (toggle twice) ☑ empty (no row) ☑ invalid (markup in a title) ☐ error — none

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the presentation frame, from the board to the screen and the export
  SOURCE : the board file on disk (projects, tasks, their presentation flags and ranks); the terminal size; the keys
  NODES  :
    - fn    : models.Project.from_dict, Board._to_dict, present_order, set_present_order
      owner : LLR-2102.1
    - fn    : views._present_task_row, its milestone branch
      owner : LLR-2101.1
    - fn    : views.render_present_all
      owner : LLR-2103.1
    - fn    : app.PresentScreen, view 3, the hint and the export
      owner : LLR-2104.1
  SINK   : the terminal surface (#present-frame, #present-hint) and the x export (reports/present-board-*-all.svg, .png)
```

```
FLOW: the presenter's curation, from a key to the board file
  SOURCE : the keys space, a, shift+up/down, enter, u (PresentScreen, PresentHiddenPicker)
  NODES  :
    - fn    : app.PresentScreen.action_hide, action_show_all, action_reorder, action_fold, action_side
      owner : LLR-2105.1
    - fn    : modals.PresentHiddenPicker, views.present_hidden_rows
      owner : LLR-2106.1
  SINK   : board.json (Board.save) and the repainted frame
```

- **Part B — boundary decomposition:** `no — the frame, the hint and the picker are widgets of one screen addressed only through it; the board file's new keys are fields of the existing project record, read by the same loader`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer 0: the load rule's type table (TC-2102), the hint's wording choice (TC-2104), the auto-fold loop (TC-2103). Layer A: TC-2101..TC-2106 at the renderer, model and screen-method level. Layer B: AT-2101..AT-2106 drive the real app headless (`run_test`, keys) on the round's board saved to disk, reading `#present-frame`, `#present-hint`, the picker, `board.json` and `reports/`. Beside the suite, the real app is captured (SVG, `NO_COLOR` unset) at 160×45, 118×30, 80×24 and through the hide → reorder → `u` → show sequence, and compared by eye with the round's C captures.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT through its surface;
- every new assertion RED on `base_ref` or by a recorded mutation; mutants KILLED on the new logic;
- the full suite: 0 failures; transcript under the batch's evidence;
- a board with no presentation key keeps its bytes on load + save; the board's gantt keeps board order;
- real-app captures of view 3 at 160×45, 118×30, 80×24, the sequence hide → reorder → `u` → show, the `-all` export, view 1 before/after the milestone fix, under `evidence/captures/`;
- the round's committed files unchanged (`git diff --stat bdf6e9d -- prototypes/present_portfolio` empty);
- the RED and mutation transcripts the HLR/LLR negative controls mark `planned` exist before their increment's gate.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions (D1–D8 and the orchestrator's own) and `docs/ARCHITECTURE.md` (amended by this batch).
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-19: 65 patterns, 5 control rows ok, `flags: session, billing, migration`, `security_required: true`, exit 1 (`evidence/scan-p1.txt`). The answers: `session` (C1) — the word names the presentation's in-memory fold state ("session only"), not an authenticated session: no login, token, credential or permission is read or written; `billing` (C4) — the round's synthetic project "Billing Migration": no payment, personal or billing data enters the board, the fixture is synthetic; `migration` (C5) — the same synthetic project's name: no schema change, no data migration, no destructive write (the board gains two optional keys read by the shipped total loader, and a board without them keeps its bytes). C1, C4 and C5 are recorded fired (the scan's words; triggers only raise) and answered here; the security-reviewer pass of P2 reads these answers. C2, C3, C6, C7: not flagged — no secret, no external integration, no new input surface beyond keys inside the app, no network. C8 is judged fired: view 3 paints project names on the rail and in headers, and the picker paints names and titles — every such site escapes (`escape(fit(...))`) or appends plain `Text`; TC-2103 and TC-2106 carry a markup-in-a-name arm.
- **The presentation order is presentation-only (D2).** The orchestrator read «que persista el orden» as an order kept for the presentation, leaving the board's gantt in board order (the round's before/after); the operator may prefer the board's own order. Switching is a small change (`present_order` returning `board.projects`); flagged in the close for the operator.
- **The `?` help.** D8 asks to add view 3 and `u` to the `?` help's Keys grid. The `?` help lists the main screen's keys only (`bar_keys(mode)`, LLR-1603.1); the presentation's keys have never been there — they live in the hint row by design (`docs/ARCHITECTURE.md` §5: `PresentScreen.BINDINGS` outside `KEYMAP`, "re-open when the `?` help … must list the presentation's keys"). This batch keeps that design: view 3 and `u` are named in the hint row and the README; the help is not changed — a declared deviation from D8.
- **The 80-column hint (HLR-2002's outcome superseded in part).** Three view names take 7 more cells (`3 all  `): at 80 columns the gantt view keeps the middle wording with nothing hidden (its first width becomes exactly 80), while the split view falls to the short wording with nothing hidden and to the compact one with something hidden (` · u 1 hidden`); HLR-2002's "the 80-column hint names next and show all" no longer holds for the split view. A consequence of naming the third view (LED .2); flagged for the operator in the close.
- **`shift+↑/↓` in some terminals.** Some terminals and multiplexers do not pass `shift+arrow`; reordering has no other key (ux-reviewer UX-8). Recorded; the presenter's terminal (the operator's) passes it — the round's captures pressed it through the real app.
- **`space` on the timeline only hides (UX-9).** A hidden project comes back on the rail (`space`), with `u` or `a`; below 100 columns (no rail) only `u` or `a` — a consequence of D5.
- **Archived projects keep their rank (architect A-10).** The dense renumbering covers the visible projects; an archived project keeps an old rank and may tie on unarchive — board order breaks the tie. Recorded.
- **A team pull (security review S-4).** A NEW project added by a team pull arrives shown and unranked (LLR-2102.1 strips the keys); an existing project's flags are never touched by a pull.
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-19-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```

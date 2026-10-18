# Requirements Document — taskboard — Batch 2026-10-18-batch-01

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
The live contract for batch 2026-10-18-batch-01 (present v3): the presentation (`R`) gains a second view, `split`, that shows every shown open task's notes at once under the gantt rows; the gantt view's cursor note keeps its line breaks; one key switches the views.

### 1.2 Scope
In: `R`'s two views (`gantt`, `split`), their keys (`1`, `2`, `tab`, `shift+tab`, `pgdn`, `pgup`) and hint row, the header's view word, the shared cursor and hidden tasks, the `x` export of the current view, the README's Presentation section, the `BACKLOG.md` items the brief names (the README section and the backlog edits are documentation deliverables of increment 002 and of the close, not requirements: no requirement owns them, `tests/test_readme.py` keeps the README honest). Out: round 1's "Slide" view C (kept as an optional backlog item) and "Cards" view B (dropped); images in either view (the split view shows none — the brief allows "a count and file names, if shown at all"); remembering the last view; done tasks; every other view of the app; pushing to any remote.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| gantt view | the presentation as shipped on `base_ref`: header, the two ruler rows, the span row, one field row per shown open task, a rule, the brief one-liners with the `⟦…⟧` cursor and the cursor's note expanded |
| split view | the prototype's D2 · stacked: the gantt view's rows down to the rule, then one block per shown open task |
| block | a task's heading row (`▌`/`▎` bar, title, start–end, days late or left, `no notes` when empty) and its note rows |
| shown open task | a task of the presented project that is visible, not done and has `show_in_present` (`present_tasks(...)[0]`) |
| note rows | a note wrapped to the block's width by `present_note_lines`: line breaks kept, `- `/`* `/`• ` → `• `, `N. ` kept, hanging indent |
| cut mark | `… +N lines` on the last kept row of a cut note, or ` … +N` beside a note kept to one row |
| room | the rows below the rule in the split view (`height - 10` with five open tasks) |
| area scroll | `pgdn` when no cursor note in the frame can scroll: each cut column shows its whole text, every note whole, windowed |

### 1.4 References
- The commission (PLAN header) and its approved design: `prototypes/present_views/` — `views_d.py` (D2: `alloc`, `_clipped`, `_heading`, `_stack_column`, `render_stacked`, `render_gantt`), `views_proto.py` (`wrap_notes`, `_note_markup`, `_scrolled`), `app_capture.py` / `app_capture2.py` (the key set), the page `present-views-prototype.html` §"Ronda 2", the captures `out/r2-118-D2-stacked*.png`, `out/r2-80-D2-stacked*.png`, `out/r2-118-A-gantt.png`.
- The shipped presentation: batch 2026-10-07-batch-04 (HLR-1001), batch 2026-10-16-batch-01 (HLR-1601..HLR-1603), batch 2026-10-17-batch-01 (HLR-1701); `taskboard/views.py:6025-6308`, `taskboard/app.py:181-318` on `base_ref`.

### 1.5 Document overview
§2 stories and premises, §3 three HLRs, §4 seven LLRs and the information-flow contract, §5 the validation strategy, §6 risks.

---

## 2. Overall description

### 2.1 Product perspective
`render_present` gains a `view` (and `scroll`) argument; both views share the top of the frame, the cursor rule and `present_tasks`. `PresentScreen` holds the view index and the scroll offset and never persists them.

### 2.2 Product functions
1. `2` (and `tab`) shows the split view: every shown open task's notes at once, cut fairly and declared.
2. The gantt view's cursor note keeps its line breaks, bullets and numbers.
3. `1`, `2`, `tab`, `shift+tab` switch views; `pgdn`/`pgup` scroll the split view's notes; the cursor, the hidden tasks, `a` and `x` work across both; `R` opens on the gantt view.

### 2.3 User characteristics
One presenter at a terminal 80–118+ columns wide, showing one project to a room (often over a screen share), keyboard only. The task: walk the room through the timeline, then through what each task says, switching between the two without losing the place.

### 2.4 Constraints
Textual + Rich as shipped; no new dependency; every row exactly `width` cells and the frame exactly `height` rows (`_present_finish` asserts it); S1 — every board-file string escaped before it enters markup; the PRES-R / PRES-R2 / PRES-C oracle frames on disk are never rewritten — new frames go in new files.

### 2.5 Assumptions and dependencies
The fixtures `tests/present_board.py` (the PRES-C oracle board) stays as it is; `tests/present_notes_board.py` (new) copies the prototype round's notes overlay so no test imports a prototype.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-1801 | As a presenter, I want a second view in the presentation that shows, under the gantt rows, the notes of every shown open task at the same time, so that the room reads what each task says while the timeline stays in sight. | operator, 2026-10-17: «si las demás tareas tienen texto, me gustaría que todas se vieran al mismo tiempo»; the prototype round `prototypes/present_views/` (round 2, D2 · stacked, chosen 2026-10-17/18); `BACKLOG.md` "Present v3" | READY |
| US-1802 | As a presenter, I want the gantt view's expanded cursor note to keep its line breaks, bullets and numbered steps, so that a plan reads as the steps it is and not as one run-on line. | the coordinator's brief (the prototype's accepted fix: «la nota de la vista gantt conserva sus saltos de línea»), `prototypes/present_views/out/r2-118-A-gantt.png` | READY |
| US-1803 | As a presenter, I want one key to switch between the two views (`1`, `2`, `tab`, `shift+tab`), `pgdn`/`pgup` to scroll the notes, and the cursor, the hidden tasks and the `x` export to follow the view I am on, with `R` always opening on the gantt view, so that switching in front of the room never loses my place or writes anything. | the coordinator's brief (keys, shared state, R opens on gantt, the view not remembered) and the prototype's key set | READY |

#### Refinement log (one block per story)

**US-1801 — the split view: every task's notes at once**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter and the room · outcome = `2` in `R` shows the shipped gantt rows on top and, below them, one block per shown open task (heading: title, dates, days late or left; then its wrapped note with line breaks, bullets and numbered lists kept), the cursor's block in accent, two columns at ≥ 100 columns and one below; everything when it fits, else the cursor's note up to half the area and every other note at least 1–2 rows, each cut declared; a task with no notes is one row with `no notes` · why = the operator wants every task's text visible at once · out of scope = done tasks, images (not shown in this view), the round-1 "Slide" (C, kept as a backlog option) and "Cards" (B, dropped) views
- **Feasibility (E, S):** implementation path = port `prototypes/present_views/views_d.py` (`alloc`, `_clipped`, `_heading`, `_stack_column`, `render_stacked`) and the helpers of `views_proto.py` it calls (`wrap_notes`, `_note_markup`, `_scrolled`) into `taskboard/views.py` beside `render_present`, which gains a `view` argument · dependencies/unknowns = none · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter presses `R` then `2`, the painted frame shows text from every shown open task that has notes, the gantt rows above, and `no notes` for a task without one (AT-1801).
- **Open questions:** none — the brief and the verdicts settle the layout, the share and the cut marks.
- **Classification:** `READY` — prototyped with real-app captures and chosen by the operator.

**US-1802 — the gantt view's note keeps its structure**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = the cursor note (at most 3 rows) keeps its line breaks, bullets and numbered items, a cut said `… +N lines` · why = on `base_ref` `_present_note_lines` runs `textwrap.wrap` over the whole note, which flattens it («Sep 22. 1. Feature-flag…») · out of scope = the brief rows, the ruler, the field
- **Feasibility (E, S):** implementation path = the gantt branch of `render_present` uses the split view's note wrapper (`render_gantt` in `views_d.py`) · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter moves the cursor onto a task whose note is a numbered plan, the painted frame shows `1. Feature-flag …` starting its own row (AT-1802).
- **Open questions:** none.
- **Classification:** `READY`.

**US-1803 — switching, scrolling, and what the views share**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = `1` gantt, `2` split, `tab`/`shift+tab` cycle; `pgdn`/`pgup` scroll the split view's notes; the keys appear in the hint row only, never in the frame or the `x` export; the header carries a quiet grey view word; the cursor and the space-hidden tasks are shared; `a` and `x` work in both views, `x` exporting the current view's frame; `R` always opens on the gantt view and the view is not remembered, so the presentation still writes only `show_in_present` · why = the presenter switches in front of the room · out of scope = remembering the last view (refused by the brief)
- **Feasibility (E, S):** implementation path = `taskboard/app.py` `PresentScreen` gains six priority bindings, a view index and a scroll offset · dependencies/unknowns = the app's own `1`/`2` and `tab` must not fire behind the modal (checked at P1) · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the presenter presses `2`, `tab`, `shift+tab`, `1`, the header's view word follows and the board behind does not change view; `pgdn` scrolls the cut note; `space` in the split view hides the task from both views; `x` writes the current view's frame (AT-1803).
- **Open questions:** none.
- **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | `render_present` has exactly one production caller, `app.PresentScreen` (paint and export) | premise | TRUE | `git grep -n "render_present(" 6ddea9f -- taskboard` → `app.py:250` (`_paint`), `app.py:305` (`action_export`), `views.py:6263` (def) | the new `view`/`scroll` arguments default to the shipped behaviour's `gantt`; the screen passes both |
| P-2 | On `base_ref` the gantt view's cursor note flattens line breaks | premise | TRUE | `render_present` on `base_ref` over the notes board, cursor `tw5`, 118×30 → note rows `· Go-live plan, agreed with marketing and support on Sep 22. 1. Feature-flag the new homepage …` (the base export in the scratchpad) | US-1802's defect, AT-1802's RED |
| P-3 | While `PresentScreen` is open the app's own `1`/`2` (views) and `tab` (`toggle_presentation`) do not fire | premise | TRUE | `keymap.py:61-62` (`1`, `2` non-priority) — Textual's `_modal_binding_chain` stops at the modal screen; `keymap.py:124` (`tab` priority) is released by `TaskboardApp.check_action` while `len(self.screen_stack) > 1` (`app.py:389-391` on `base_ref`); probe on the draft: AT-1803 presses `2`, `tab`, `shift+tab`, `1` and `app.view_mode` is unchanged | the screen's six bindings are `priority=True`, like its shipped ones |
| P-4 | `pagedown`, `pageup` and `shift+tab` are bound nowhere a `PresentScreen` key press can reach | premise | TRUE | `git grep -n "pagedown\|pageup\|shift+tab" 6ddea9f -- taskboard` → `modals.py:140-141` only (the date picker's month keys, another screen); Textual's `Screen` binds `tab`/`shift+tab` to focus moves without priority | the screen's priority bindings win |
| P-5 | The prototype's renderers draw from the shipped helpers this batch keeps (`_present_ruler`, `_present_span_row`, `_present_task_row`, `_present_brief`, `_present_finish`, `present_tasks`, `present_span_label`, `_present_due`) | premise | TRUE | `prototypes/present_views/views_d.py:13-16`, `views_proto.py:17-21` import them; each is defined on `base_ref` (`views.py:6064`, `:6125`, `:6153`, `:6184`, `:6192`, `:6208`, `:6231`, `:6250`) | the port is a faithful one and the prototype stays the cross-check oracle (`evidence/gen_frames.py`) |
| P-6 | `present_tasks` already leaves out hidden and done tasks for every part of the frame | premise | TRUE | `views.py:6064-6070` on `base_ref`: `[t for t in _present_pool(...) if t.show_in_present]`, open = `not board.is_done(t)` | the split view's blocks take `open_t` from the same call: hidden and done tasks are out of both parts |
| P-7 | At the operator sizes the screen's frame is 118×30 and 80×24 and the hint row 116 / 78 cells | premise | TRUE | `app.py:243-244` (`_frame_height` = height − 1), `app.py:216-220` (`#present-hint` `padding: 0 1`) on `base_ref` | the oracle frames are 118×30 / 80×24; the hint's 80-column form must fit 78 cells |
| P-8 | `_present_note_lines` and `_present_note_row` have no caller left once the gantt branch uses the new wrapper, and no test names them | premise | TRUE | `git grep -n "_present_note_lines\|_present_note_row" 6ddea9f` → `views.py` (defs, one call site each in `render_present`), `prototypes/present_rulers/{app_capture,proto}.py`, `prototypes/present_views/views_proto.py`; `grep -rl` in `tests/` → none | both are deleted; the two prototypes that import them are throwaway rounds (`present_rulers/proto.py` already fails to import since 2026-10-17-batch-01 deleted `_gantt_scale_label`); `gen_frames.py` binds inert names before importing `views_d` |

- **Premise evaluation:** 8 premise(s) · ✅ TRUE ×8

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: two increments in order on one branch, one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-1801 — The split view shows every shown open task's notes at once
- **Traceability:** US-1801
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2, LED-2026-10-18-batch-01.3
- **Statement:** When the presentation shows its `split` view, the system shall paint the gantt view's rows down to its rule and, below them, one block per shown open task in gantt order — a heading (title, start–end, days late or left) and then the task's note rows — the cursor's block in accent, in two columns (the first half of the tasks on the left) when the frame is at least 100 columns wide and one column below that; every note whole when they all fit; otherwise the cursor's note promised up to half the room and every other note at least two rows (one when even that does not fit), each cut declared (`… +N lines`); a task with no notes in one row reading `no notes`; so that text from every shown open task with notes is on screen at the same time whenever the room holds a heading per task and a row per note. Below that, the cursor's note still keeps one row and a column whose blocks overflow the room ends on `↓ N more lines`; with no shown open task, nothing is painted under the rule.
- **Rationale (informative):** the operator, 2026-10-17: «si las demás tareas tienen texto, me gustaría que todas se vieran al mismo tiempo»; the prototype round's D2 was chosen for it.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views.py tests/test_present_views_app.py -k "1801 or 1802 or 1803 or 1804 or 1805 or 1806"`
- **Numeric pass threshold:** every arm passes; AT-1801 at 118×31 and 80×25: `R` then `2` paints rows equal to `PRES-V3-split-118x30.txt` / `PRES-V3-split-80x24.txt`, and after each of four `→` the frame holds the first words of each of the four shown open tasks' notes and `no notes`; nothing is saved.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `R`, `2` → under the gantt rows, every task's heading and text at once; the cursor's block accented; the task without notes reads `no notes`; a cut note says `… +N lines`.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame`; key `2`.
  - **Acceptance test(s):** AT-1801
  - **Boundary catalog (QC-3):** ☑ empty (a task with no notes; every task hidden → nothing under the rule, TC-1804) ☑ boundary (99 / 100 columns — one column vs two; 80×24, where every non-cursor note is one or two rows; 80×19, exactly a heading per task and a row per note; 80×18, 118×15 and 80×11, below it; a note longer than the room) ☑ invalid (markup in a note or a title — painted literally, TC-1805) ☐ error — none: the renderer has no failure path
  - **Negative control:** on `base_ref` AT-1801 is RED: `PresentScreen` binds no `2` and `render_present` takes no `view` — captured at increment 002 (`evidence/red-002.txt`).

### HLR-1802 — The gantt view keeps a note's structure and names its view
- **Traceability:** US-1802
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2
- **Statement:** When the presentation shows its `gantt` view, the system shall expand the cursor task's note in at most three rows that keep the note's line breaks, bullets and numbered items, the last row reading `… +N lines` when the note is longer; and in both views the header shall carry the current view's name as one dim word after the project name.
- **Rationale (informative):** a numbered go-live plan read as «Sep 22. 1. Feature-flag …» is the defect the brief names; the view word is the prototype's.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present.py tests/test_present_views.py tests/test_present_views_app.py -k "1001 or 1002 or 1807 or AT_1802"`
- **Numeric pass threshold:** every arm passes; AT-1802 at 118×31 and 80×25: `R` (the header reads `◆ PRESENT · Website Redesign  gantt`), `→ →` onto `Launch new homepage` → the painted rows equal `PRES-V3-gantt-notes-118x30.txt` / `-80x24.txt`, a row starts `  · 1. Feature-flag`, and no row holds `Sep 22. 1.`; TC-1001 / TC-1002 / AT-1001 equal `PRES-V3-gantt-118x30.txt` / `-80x24.txt`.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the cursor's note in the gantt view reads as its lines: `Go-live plan … Sep 22.` / `1. Feature-flag …` / `… +11 lines`.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame`; keys `←`/`→`.
  - **Acceptance test(s):** AT-1802
  - **Boundary catalog (QC-3):** ☑ empty (a cursor task with no notes → no note row) ☑ boundary (a note of exactly three rows, uncut; a longer one, cut at three; 80 columns) ☑ invalid (markup in the note, TC-1805) ☐ error — none
  - **Negative control:** on `base_ref` AT-1802 is RED: the note rows read `… Sep 22. 1. Feature-flag …` (P-2) — captured at increment 002 (`evidence/red-002.txt`); TC-1807 is RED at increment 001 (`evidence/red-001.txt`).

### HLR-1803 — One key switches the views; the views share the presenter's place
- **Traceability:** US-1803
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2
- **Statement:** While the presentation is open, the system shall show the `gantt` view on `1`, the `split` view on `2`, the next view on `tab` and the previous one on `shift+tab` (wrapping), without the board behind it reacting to those keys; shall page the split view's notes on `pgdn` / `pgup` — the cursor's note when it is cut and keeps at least 3 rows, otherwise (no cursor note in the frame can scroll) each cut column's whole text, every note whole — with no row a page skips; shall keep one cursor and one set of hidden tasks for both views, with `space`, `a`, `←`/`→`/`↑`/`↓` and `x` acting in either; shall export with `x` the frame of the view on screen, each view to its own file; shall name the keys in the hint row under the frame and never in the frame or the export; and shall open on the `gantt` view each time `R` is pressed, writing nothing but the `show_in_present` flag.
- **Rationale (informative):** the brief's key set and shared state; the view is not remembered so the presentation's only write stays the flag.
- **Validation:** `test`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views_app.py tests/test_present_hide.py tests/test_present.py`
- **Numeric pass threshold:** every arm passes; AT-1803 at 80×25 on the notes board: `R` → header `gantt`; `2` → `split`; `tab` → `gantt`; `shift+tab` → `split`; `tab tab` → `split`; `1` → `gantt`; the app's `view_mode` unchanged (a declared seam: the board behind is not on screen) and the screen still `PresentScreen`; `2 → →` → the split heading ` ▌ Launch new homepage`, then `1` → `⟦Launch new homepage⟧`; `2`, `pgdn` → `lines above` on screen, `pgup` → the frame before; twelve `pgdn` → the note's last line (`username_subject`) on screen, then `pgup` → a frame different from that last page (no dead pages); `space` → `Launch new homepage` in neither view, 1 save; `x` (gantt) then `2`, `x` → both `reports/present-website-redesign-2026-09-30.svg` and `reports/present-website-redesign-2026-09-30-split.svg` exist (literal paths), the split one holds `split` and `Design tokens are frozen`, the gantt one does not hold that note text, and neither SVG nor the frame holds any of `pgdn`, `⇥`, `1 gantt`, `2 split`, `esc`, `x export`, `hide`; `a` → 2 saves; `esc`, `R` → `gantt`; 2 saves in all.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the header's view word follows the keys; the cursor and the hidden tasks are the same in both views; `pgdn` reveals more of a cut note; the export file of the split view sits beside the gantt one; reopening starts on `gantt`.
  - **Shipped surface:** keys `R`, `1`, `2`, `tab`, `shift+tab`, `pgdn`, `pgup`, `→`, `space`, `a`, `x`, `esc` → `PresentScreen` (`#present-frame`, `#present-hint`), the board file, `reports/`.
  - **Acceptance test(s):** AT-1803
  - **Boundary catalog (QC-3):** ☑ empty (`pgdn` in the gantt view and with nothing cut — nothing moves) ☑ boundary (`tab` wrapping both ways; `pgdn` past the end; 80 columns, where the hint is shortest) ☐ invalid — none: no typed input ☐ error — none: the export's PNG absence is the shipped toast (AT-1001)
  - **Negative control:** on `base_ref` AT-1803 is RED: `2` is unbound on `PresentScreen` and the header has no view word — captured at increment 002 (`evidence/red-002.txt`).

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.
> Same regime: EARS syntax owed in `full`, recommended in `core`. ID format: `LLR-<HLR>.<M>`.

### LLR-1801.1 — One note wrapper keeps a note's structure
- **Traceability:** HLR-1801, HLR-1802
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2
- **Statement:** `taskboard/views.py` shall provide `present_note_lines(notes, w) -> list[tuple[str, str]]` returning `(lead, text)` rows that fit `w` cells: the note stripped, split on line breaks, each line stripped; a blank line one `("", "")` row, a run of blank lines one row; a line starting `- `, `* ` or `• ` led `• `; a line starting one to three digits, `.` and a space led by that marker; each line wrapped by `textwrap.wrap` at `max(4, w - vis(lead))`, its continuation rows led by as many spaces as the lead; an empty or `None` note no rows. `_present_note_markup` paints a row `lead` in `mut` and `text` in `ink`, each escaped, padded to `w`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views.py -k TC_1801`
- **Numeric pass threshold:** TC-1801 passes: the ten exact rows of its mixed note at `w = 24` (a plain line, three bullet forms → `• `, a collapsed blank run, `1. ` and `12. ` with a two-row hanging wrap, a last line); a blank-only note, `""` and `None` → `[]`; every row of the long fixture note at 30 cells fits 30.
- **Negative control:** TC-1801 goes RED when the line split is removed (the base wrapper: the whole note one paragraph), when the bullet branch keeps `- `, or when the number branch takes one digit only (mutants recorded in packet 001).
- **Boundary catalog:** ☑ empty (`""`, `None`, blank lines only) ☑ boundary (a two-digit item; a wrap at the hanging indent; a run of blank lines) ☐ invalid — markup is S1's, LLR-1801.2 ☐ error — none

### LLR-1801.2 — The split layout: blocks, columns, the fair share, the cut marks
- **Traceability:** HLR-1801
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2, LED-2026-10-18-batch-01.3
- **Statement:** `views.PRESENT_VIEWS` shall be `("gantt", "split")`, in key order. `render_present(..., view="split")` shall paint the gantt view's header (its view word `split`), ruler, span row, field rows and rule, then, when there is a shown open task, `room = height - <those rows>` rows: at `width >= 100` two columns of `(width - 5) // 2` cells (the first `ceil(n / 2)` shown open tasks on the left) joined by ` │ ` after a one-cell margin, else one column of `width - 2` cells after the margin; with no shown open task nothing under the rule. Each column (`_present_column`, `_present_stack`) paints per task `_present_heading` — `▌ ` accent bar and accent bold title for the cursor, `▎ ` in the project's hue and bright bold title otherwise, the title clipped, then right-aligned `present_span_label` in `mut`, a space and `_present_due` in its tone, preceded by `no notes  ·  ` in `dim` for a task with no notes (the dates dropped when fewer than 4 title cells would remain) — then `present_alloc(ns, cur, room - <tasks in the column>, floor_n=2)` rows of its note (`_present_cut`), each prefixed by the block's bar: every note whole when `sum(ns) <= room`; else `want = min(ns[cur], max(floor_n, room // 2))` for the cursor, `min(n, floor_n)` for every other note, the largest other reduced by one while `sum + want > room` and some other exceeds 1, the cursor then given `max(min(1, ns[cur]), min(want, room - sum))` (a row for its note even over the room), the rest to the cursor first, then round-robin. A note kept to `k >= 2` of `n` rows shows `k - 1` rows and `… +<n - k + 1> lines` in `dim`; kept to one row, its first line (cut to fit with no `…` of its own) and ` … +<n - 1> lines` in `dim`; at page 0 a column whose blocks exceed the room shows its first `room - 1` rows and `↓ N more lines`, or — when that would leave the cursor's block below the window and the room holds 3 rows — the window ending on the cursor's block, under `↑ N lines above` (and over `↓ N more lines` when rows remain). Every string from the board file is escaped (S1).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views.py -k "TC_1802 or TC_1803 or TC_1804 or TC_1805"`
- **Numeric pass threshold:** TC-1802's eight `present_alloc` truth-table rows exact (among them the cursor on the no-notes task and a room of 3 for four notes → `[1, 1, 1, 1, 0]`), each within the room with ≥ 1 row per note whenever the room holds one, and ≥ 1 row for a cursor with notes always; TC-1803: the four PRES-V3 split frames equal at 118×30 and 80×24 (cursor `tw3`, cursor `tw5`), and the split view's rows 1–9 equal the gantt view's; TC-1804 at 118×30, 80×24, 100×30, 99×30, 140×40, 118×24, 80×30, 120×36 and 80×19 with every open task as the cursor: the first words of each of the 4 noted tasks' notes (a set drawn from the board, not from the renderer), `no notes`, `… +` in the block of every note one of whose wrapped rows is absent, `│` on every notes row at ≥ 100 and none below, every row exactly `w` cells; at 80×18, 118×15 and 80×11, for every cursor, `more lines` or `lines above` under the rule, and (where the room is 3 rows or more) the cursor's block on screen with the first words of its note, every row exact; every task hidden → rows 5.. blank at 118×30 and 80×24; a hidden and a done task in neither part; at 80×24 the long note keeps more rows as the cursor's than as another's; TC-1805: `[/] boom`, `[bold]x[/bold] item`, `[link=https://e.x]y[/link]` and `[red]Optimize` painted literally in both views at both sizes, and — at the one-row cut (60×20), a paged cursor note, a markup cursor title, a note ending in `\` and one holding `\[` — every one literal and every row exact.
- **Negative control:** TC-1803/TC-1804 go RED when the two-column threshold moves (`>= 100` → `> 100`), when the cursor's half is dropped (`room // 2` → `0`), when the cut mark is removed, or when the no-notes word is removed; TC-1805 goes RED when a note row's `escape` is dropped (mutants recorded in packet 001).
- **Boundary catalog:** ☑ empty (no notes; every task hidden) ☑ boundary (99/100 columns; a room that holds one row per note and no more; a note longer than the room; headings alone over the room) ☑ invalid (markup in notes and titles) ☐ error — none

### LLR-1801.3 — Scrolling the split view's notes
- **Traceability:** HLR-1803
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2, LED-2026-10-18-batch-01.3
- **Statement:** `render_present(..., view="split", scroll=p)` shall read `p` as a page: when the cursor's note is cut and keeps at least 3 rows, the cursor's block shows page `p` of its note (`_present_scrolled`) and every other block stays as at page 0; when no cursor note in the frame can scroll, each column shows page `p - 1` of its whole text — every heading and every note whole — for `p >= 1`, and its page-0 blocks at `p = 0`. `_present_scrolled(rows, room, p, w)` tiles the rows with no gap: page 0 the first `room - 1` rows, page `p >= 1` the next `room - 2` rows from row `room - 1 + (p - 1)(room - 2)` under `↑ <start> lines above`, the last page (its start clamped to `len - room + 1`) ending on the last row; `↓ <N> more lines` last whenever rows remain below; a room under 3 rows its first rows and `↓ N more lines`. The gantt view shall ignore `scroll`. Every frame stays exactly `height` × `width`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views.py -k TC_1806`
- **Numeric pass threshold:** TC-1806: at 80×24 with cursor `tw5` (its note kept to 4 rows), page 1 shows `↑ 3 lines above` and `↓`, page 999 shows the note's last line (`username_subject`), rows 0–17 unchanged; at 60×20 with cursor `tw3` (no cursor note can scroll) page 1 shows `• Buttons, inputs and cards: done` (absent at page 0) and `more lines`, page 999 shows `username_subject` and `↑`; paging from 0 until the frame stops changing shows every wrapped row of the cursor's note at 80×24, 118×30 and 80×30 (cursor `tw5`) and of every note at 60×20 (cursor `tw3`), and stops within 60 pages; the gantt view equal at `scroll` 0 and 10; at 118×30, 80×24, 60×20, 118×12 and 80×11, four cursors × five pages: every frame `h` rows of `w` cells.
- **Negative control:** TC-1806 goes RED when the note branch ignores `scroll`, when the area branch is removed (pgdn moves nothing at 60×20), when page 1 of the area no longer opens the column at its top, or when a page skips rows (the fixed 5-row step of the first draft, ux-reviewer UX-1) — mutants recorded in packet 001.
- **Boundary catalog:** ☑ empty (nothing cut → nothing moves) ☑ boundary (the last page; `s` past the end; a room of 1–2 rows) ☐ invalid — none ☐ error — none

### LLR-1802.1 — The gantt view's note rows and the header's view word
- **Traceability:** HLR-1802
- **Ledger:** LED-2026-10-18-batch-01.1
- **Statement:** `render_present(..., view="gantt")` shall paint, under the cursor's brief row, `_present_cut(present_note_lines(notes, width - 6), 3, width - 6)`, each row `  · ` (the dot `dim`) + the row, padded to `width`; `_present_note_lines` and `_present_note_row` shall not exist. In both views the header's title shall be `◆ PRESENT · <project>` followed by `  <view>` in `dim`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present.py tests/test_present_views.py -k "TC_1001 or TC_1002 or TC_1807"`
- **Numeric pass threshold:** TC-1807: the gantt frames on the notes board (cursor `tw5`) equal `PRES-V3-gantt-notes-118x30.txt` / `-80x24.txt`, with exactly 3 note rows — the first ending `Sep 22.`, the second starting `  · 1. Feature-flag`, the third matching `  · … +<N> lines` — and no `Sep 22. 1.`; the header starts `◆ PRESENT · Website Redesign  <view> ` in both views at both sizes, and no frame holds a key word (`pgdn`, `⇥`, `1 gantt`, `2 split`, `esc`); TC-1001 / TC-1002 equal `PRES-V3-gantt-118x30.txt` / `-80x24.txt`.
- **Negative control:** TC-1807 is RED on `base_ref` (the note flattened, no view word) — `evidence/red-001.txt`; it goes RED when the 3-row cap moves or the view word is dropped (mutants recorded in packet 001).
- **Boundary catalog:** ☑ empty (a cursor task with no notes) ☑ boundary (3 rows exactly; 80 columns) ☐ invalid — S1, LLR-1801.2 ☐ error — none

### LLR-1803.1 — The screen's view keys and state
- **Traceability:** HLR-1803
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2
- **Statement:** `app.PresentScreen` shall bind, with `priority=True`, `1` → `view(0)`, `2` → `view(1)`, `tab` → `cycle(1)`, `shift+tab` → `cycle(-1)`, `pagedown` → `scroll(1)`, `pageup` → `scroll(-1)`; hold `_view` (an index into `PRESENT_VIEWS`, 0 at construction, set by `view(i)` and `cycle(d)` modulo the tuple's length) and `_scroll` (a page, 0 at construction and reset to 0 on a view change, a cursor move, `space` and `a`); paint and export `render_present(..., PRESENT_VIEWS[self._view], self._scroll)` through one method, `_frame_text`; and on `scroll(d)` in the split view move `_scroll` by `d` (never below 0), not taking a page down that paints the same frame as the current one; `scroll` does nothing in the gantt view.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views_app.py -k TC_1810`
- **Numeric pass threshold:** TC-1810: the six bindings present on `PresentScreen.BINDINGS` with `priority=True` and their actions; the app's `1`/`2` bindings non-priority and `check_action("toggle_presentation", ())` `False` while the screen is open; a new screen's `_view == 0` and `_scroll == 0`; in the split view at 80×25 with cursor `tw5` `pgdn` sets `_scroll` to 1, twenty more `pgdn` stop below 21 and one more leaves `_scroll` unchanged, `pgup` from 0 leaves it 0; `pgdn` in the gantt view leaves it 0; a cursor move resets it to 0.
- **Negative control:** TC-1810 goes RED when a binding loses `priority`, when the same-frame guard is removed (`_scroll` grows past the end), or when the move no longer resets `_scroll` (mutants recorded in packet 002).
- **Boundary catalog:** ☑ empty (`pgup` at 0; `pgdn` with nothing cut) ☑ boundary (the last page; `tab` wrapping) ☐ invalid — none ☐ error — none

### LLR-1803.2 — The hint row names the keys of the view on screen
- **Traceability:** HLR-1803
- **Ledger:** LED-2026-10-18-batch-01.1, LED-2026-10-18-batch-01.2
- **Statement:** `PresentScreen._hint(w)`, `w` the screen's width (the hint gets `w - 2` cells, P-7), shall return a `Text`: for each view `<i + 1> <name>` — `bold #e6edf7` for the current view, `#5b6675` for the other — then, in the split view only, `pgdn notes · ` / `pgdn · `; then `⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave` / `⇥ · ←→ · ␣ hide · a all · x export · esc`; then ` · <n> hidden` when `n > 0` tasks are hidden — the keys and the count in `#8b98a5`. The long wording (the view names followed by two spaces each, `pgdn notes · `, the long keys) is used when the whole hint fits `w - 2` cells, else the short one (one space each, `pgdn · `, the short keys).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views_app.py tests/test_present_hide.py -k "TC_1808 or TC_1604"`
- **Numeric pass threshold:** TC-1808 at 118×31, 100×31, 99×31, 96×31 and 80×25: the exact gantt, split, and split-with-one-hidden hints of the test's table (the long wording at 118; long until a count is added at 100 and 99; short in the split view at 96; short at 80), the current view's span `bold`, the other's not, and each hint within `w - 2` cells; TC-1604's hint arm (law-driven, `tests/test_present_hide.py`) reads the gantt hint plus ` · 2 hidden` at 118 and 80.
- **Negative control:** TC-1808 goes RED when `pgdn` is shown in the gantt view or the bold moves to the other view (mutants recorded in packet 002); on `base_ref` the hint has no view names (`evidence/red-002.txt`).
- **Boundary catalog:** ☑ empty (no hidden task → no tail) ☑ boundary (99 vs 100 columns; a two-digit count at 80) ☐ invalid — none ☐ error — none

### LLR-1803.3 — `x` exports the current view to its own file
- **Traceability:** HLR-1803
- **Ledger:** LED-2026-10-18-batch-01.1
- **Statement:** `views.present_paths(board, project_name, today=None, view="gantt")` shall name the export `present-<slug>-<YYYY-MM-DD>` for `gantt` (as shipped) and `present-<slug>-<YYYY-MM-DD>-<view>` for any other view, `.svg` and `.png`; `PresentScreen.action_export` shall write `_frame_text()` to `present_paths(..., PRESENT_VIEWS[self._view])`.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest -q -p no:cacheprovider tests/test_present_views_app.py -k "TC_1809 or AT_1803"`
- **Numeric pass threshold:** TC-1809: `present_paths(b, "Website Redesign", 2026-09-30)` == the `gantt` call, named `present-website-redesign-2026-09-30.svg`; the `split` call `…-2026-09-30-split.svg` / `.png`; AT-1803's `x` arm writes the split file with the split frame.
- **Negative control:** TC-1809 goes RED when the suffix is dropped (both views one file) or added to `gantt` (the shipped name changes, AT-1001's `x` arm too) — mutants recorded in packet 002.
- **Boundary catalog:** ☐ empty — none: a project name is always resolved ☑ boundary (the default argument = `gantt`) ☐ invalid — none ☐ error — none: the PNG absence is AT-1001's toast

### Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: a task's notes, from the board file to the presentation's frame and its export
  SOURCE : the board file on disk (tasks: title, notes, start/due dates, show_in_present); the presenter's keys (cursor, view, scroll); the terminal size
  NODES  :
    - fn    : views.present_note_lines, views._present_note_markup
      owner : LLR-1801.1
    - fn    : views.present_alloc, views._present_column, views._present_heading, views._present_cut and render_present's split branch
      owner : LLR-1801.2
    - fn    : views._present_scrolled and _present_stack's scroll branches
      owner : LLR-1801.3
    - fn    : render_present's gantt branch and the header's view word
      owner : LLR-1802.1
    - fn    : app.PresentScreen view, cycle and scroll actions, _frame_text
      owner : LLR-1803.1
    - fn    : app.PresentScreen._hint
      owner : LLR-1803.2
    - fn    : app.PresentScreen.action_export over views.present_paths
      owner : LLR-1803.3
  SINK   : the terminal surface (#present-frame, #present-hint) and reports/present-<slug>-<date>[-split].svg / .png
```

- **Part B — boundary decomposition:** `no — no component of the boundary is addressable on its own: the frame and the hint are the two Statics PresentScreen already paints, addressed by no consumer but the screen and the tests that read them; the export file is the shipped writer's.`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer A: TC-1801..TC-1807 at renderer level (`render_present`, `present_note_lines`, `present_alloc`; increment 001), TC-1808..TC-1810 at screen level (increment 002), and the repointed TC-1001 / TC-1002. Layer B: AT-1801..AT-1803, the real app headless (`run_test`, keys through the pilot) on the notes board saved to `tmp_path`; AT-1001 repointed.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC and every story a passing AT driving the shipped surface, each AT one node;
- every new assertion RED on `base_ref` or by a recorded mutation; mutation batteries on the new logic, every mutant KILLED or declared;
- the pinned tests of earlier batches the change reaches are updated law-driven and named (B1): TC-1001 / TC-1002 / AT-1001 (the frames), TC-1604's hint arm, TC-402's `PresentScreen._paint` exemption key;
- the full suite green but for the known base failures (the two standup tests in `tests/test_team_views.py`, and `test_win_clipboard_roundtrip` when the environment's clipboard fails), its transcript under the batch's evidence;
- real-app captures (SVG) at 118×31 and 80×25: the split view opened, the cursor moved, the long note under the cursor, a hidden task, `pgdn`; the fixed gantt view; PNGs of the 118 ones through headless Edge; looked at and compared with the prototype's `r2-118-D2-stacked*.png` / `r2-80-D2-stacked*.png` / `r2-118-A-gantt.png`.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions and `design/design-proposal.md`.
### 6.3 Open risks
- **Security questions (the P1 scan):** `devflow-scan-spec.py` over this document, 2026-10-18: 5 control rows ok, `flags: `form`, `escape``, `security_required: true`. `form` hits prose ("the 80-column form" of the hint, "its shortest form") — no input form is added: the batch adds no text input, only six keys on an existing screen. `escape` hits the S1 law this contract states (LLR-1801.2): the one security-relevant surface is C8 — the split view and the gantt note rows compose Rich markup over board-file text (note bodies, titles); every such string goes through `rich.markup.escape` before it enters markup, and TC-1805 paints `[/]`, `[bold]…[/bold]`, `[link=…]` and a markup title literally in both views. No auth, secret, network, external integration, sensitive data or new write: the export writes the shipped `reports/` folder (a new `-split` file name only). C8 fired, so `security-reviewer` joins P2.
- The supersession reaches canon rows owned by earlier batches: LLR-1001.1's oracle (PRES-R2 → PRES-V3; 2026-10-07-batch-04, repointed by 2026-10-16-batch-01), LLR-1601.1's frame clauses (the header), LLR-1602.2 (j)'s hint texts (2026-10-16-batch-01). Their canon status cells are updated at the close.
- The area scroll (LLR-1801.3) is the brief's addition; the prototype only scrolled the cursor's note. P2 iteration 1 made both scrolls page by page (no skipped row, UX-1).
- **Declared and accepted at P2 (not changed):** a paged window can start on an item's continuation row (UX-2 — the tiling shows every row; snapping to item starts is a backlog option); in the area scroll the headings scroll with the text (UX-3 — the text is whole, the cursor accent marks the cursor's block); `pgdn` stays in the split hint even when nothing is cut (UX-6 — one hint per view, the README names `shift+tab` as `⇧⇥`); the dim view word and cut marks on a screen share are judged on the 118 PNG captures at P4 (UX-7); `present_paths` does not validate `view` (S-1 — every caller passes a `PRESENT_VIEWS` constant, internal callers are trusted); `textwrap` counts code points, so a note with wide glyphs can wrap into a row `clip` cuts with a visible `…` (S-3 — the frame stays exact, the cut is visible; a cell-width wrap is a backlog option).
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-18-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```

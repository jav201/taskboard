# Requirements Document — taskboard — Batch 2026-10-16-batch-01

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
The live contract for batch 2026-10-16-batch-01: the presentation (`R`) gains a date ruler and start–end chips, a per-task persisted "show in presentation" flag, and the `?` help modal stops losing keys (a full-width Keys band and a pinned line of the palette-only global keys).

### 1.2 Scope
In: the four decisions of the prototype round `prototypes/present_rulers/` (operator verdict 2026-10-16 — variant B ruler, start–end chips, the persisted hide flag, the `?` legend fix) and the re-captured PRES oracle frames. Out: any other change to the presentation beyond the operator's verdict of 2026-10-17 (increment 004: the header's ` — hybrid` suffix and the in-frame keys row leave the frame, the tick row's label names the selected task), weekend shading on the present field, undo for the hide flag, any change to the gantt view's own output, pushing to any remote.

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| field row | a row of the presentation's gantt field: the project's span row or an open task's bar row |
| brief row | a one-line task block below the separator, carrying the relative due (`▲2d`, `in 10d`) |
| ruler | the two rows above the span row: the month row (month bands, today's number, the project's due `◆`) and the tick row (day ticks or the cursor task's echo) |
| echo | the cursor task's exact start–end drawn on the tick row (`gantt_echo`, the gantt view's own) |
| hidden task | a task whose "show in presentation" flag is off; it is still on the board and in every other view |
| global key | a `KEYMAP` entry with `bar=False`: live in every view, reachable from the palette, never on the key bar |

### 1.4 References
- The prototype round and its verdict page: `prototypes/present_rulers/present-rulers-prototype.html`; the reference renderers `prototypes/present_rulers/proto.py` (`_ruler_rows`, variant B) and `app_capture.py` (`span_label`, `chip`, `cols`, `render_b2`, `PresentB2`); the legend round `legend_proto.py` (`_grid_keys`) and `out/legend-grid.svg`.
- The shipped presentation contract: batch 2026-10-07-batch-04, HLR-1001 / LLR-1001.1 / LLR-1001.2, oracle frames `.dev-flow/2026-10-07-batch-04/evidence/frames/PRES-C-*.txt`.
- The module map `docs/ARCHITECTURE.md` (ARQ of this batch).

### 1.5 Document overview
§2 the stories and premises, §3 three HLRs (one per story), §4 their LLRs and the information-flow contract, §5 the validation strategy.

---

## 2. Overall description

### 2.1 Product perspective
The presentation (`R`, `PresentScreen` over `views.render_present`) is a modal surface of the TUI; the help modal (`?`, `HelpModal`) is another. The hide flag is the only new board data and rides the existing `board.json` task record.

### 2.2 Product functions
1. A date ruler above the presentation's field and both dates on every field row.
2. Hide a task from the presentation (persisted), bring every hidden task back.
3. A `?` help modal whose key lists are complete at every supported size.

### 2.3 User characteristics
One operator presenting a project to a room (a meeting, a screen share) from a terminal 80–118+ columns wide; keyboard-only.

### 2.4 Constraints
Textual + Rich as shipped; no new dependency; Windows terminal; every row exactly `width` cells (S1); the C-2b colour budget as amended by the operator (today on the ruler stays accent).

### 2.5 Assumptions and dependencies
The PRES-C oracle board (`tests/present_board.py`) stays the fixture for the frames; the ruler reuses the gantt view's builders unchanged in output.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-1601 | As the presenter, I want the presentation's field to carry dates — a month/day ruler with the cursor task's exact dates, and each bar's start–end beside it — so that the room can read WHEN each bar is without me reading it out. | operator verdict 2026-10-16 on `prototypes/present_rulers/` («Se ve mejor en acento», variant B + chips) | READY |
| US-1602 | As the presenter, I want to leave a task out of the presentation and have that choice remembered, so that a meeting sees only what belongs in it without my editing the board for it. | operator 2026-10-16: «Que se guarde en la tarea, una bandera basta.» | READY |
| US-1603 | As a user reading `?`, I want the global keys (`R` Present, `S` Standup, …) visible without scrolling and every key of the view listed whole, so that the help is the place I find a key. | operator 2026-10-16: «Ok, implementa la recomendación con los keys.» (the legend capture showed `R`/`S` absent and the Keys list clipped) | READY |

#### Refinement log (one block per story)

**US-1601 — the presentation ruler and chips**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter and the room · outcome = dates readable on the field · why = the shipped field shows bars with no calendar · out of scope = weekend shading, brief-row changes
- **Feasibility (E, S):** implementation path = re-seat `gantt_month_row`/`gantt_day_row`/`gantt_echo` in the present columns, a chip label function · dependencies/unknowns = none (the prototype composes the shipped helpers) · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the user presses `R` on the oracle board, the painted frame shows the month row, the tick row with the cursor task's dates, and a `Mon D–D` chip on each field row (AT-1601).
- **Open questions:** none — the operator's verdict settled the colours (today accent, echo bright).
- **Classification:** `READY` — prototype-proven.

**US-1602 — hide a task from the presentation**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the presenter · outcome = a hidden task leaves the field and the brief, the choice survives a restart · why = a meeting deck should not carry every task · out of scope = undo, per-meeting sets
- **Feasibility (E, S):** implementation path = one boolean on `Task`, omitted from `board.json` when on; `space`/`a` in `PresentScreen`; a checkbox in the task editor · dependencies/unknowns = the byte-identity of a board with no hidden task · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the user presses `R`, then `space`, the cursor task leaves the frame, the hint row reads `· 1 hidden`, and `board.json` on disk carries the flag on that task only; `a` brings it back and the file returns to its original bytes (AT-1602).
- **Open questions:** none.
- **Classification:** `READY`.

**US-1603 — the `?` help shows every key**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = anyone pressing `?` · outcome = the view's keys and the global keys visible · why = `R`/`S` are palette-only and absent from the help; the Keys list overflows the right pane · out of scope = the full map (`m`) and the palette
- **Feasibility (E, S):** implementation path = a grid band under the two columns, a pinned footer line derived from `KEYMAP` · fits one batch? = yes
- **Evaluability (T) — behavioral, black-box:** When the user presses `?` in the gantt view at 118×30 and 80×24, the painted screen shows `R Present` and `S Standup` without scrolling; the view's keys are in the scrolled body, none cut (AT-1603).
- **Open questions:** none.
- **Classification:** `READY`.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| P-1 | The gantt view's ruler builders can be reused for the present field without changing the gantt view's output: `gantt_day_row` shades weekends inside the builder and nothing else in it is gantt-specific | premise | TRUE | `taskboard/views.py:2727-2789` (`gantt_day_row`; the shading is the single line `out.append(_on_weekend(m) if x in weekends else m)`); `gantt_month_row` `:2792-2844` paints no weekend | a keyword parameter defaulting to the shipped behaviour (LLR-1601.1) |
| P-2 | A new dataclass field on `Task` is written to every task record by `Board._to_dict` (`asdict`), so a field that must be absent when on needs an explicit omission | premise | TRUE | `taskboard/models.py:991-995` (`d = asdict(item)`; `{**d.pop("extra", {}), **d}`) | LLR-1602.1 omits the key when the task is shown |
| P-3 | `PresentScreen` binds `h` to cursor-left, so the hide key cannot be `h` | premise | TRUE | `taskboard/app.py:189` `Binding("left,h", "move(-1)", ...)` | `space` hides, `a` shows all (LLR-1602.2) |
| P-4 | The `?` modal draws its Keys list from `bar_keys(mode)`, which drops every `bar=False` key, so `R` and `S` never reach the help | premise | TRUE | `taskboard/keymap.py:182-189` (`[k for k in _layer_keys(view, layer) if k.bar]`); `taskboard/modals.py:1974-1976` (`HelpModal.compose` loops `bar_keys(self._mode)`) | LLR-1603.2 derives the global line from `KEYMAP` |
| P-5 | Local `main` and `origin/main` share no merge-base (origin was rewritten 2026-10-11); the source tree `taskboard/` is byte-identical between them | premise | TRUE | `git merge-base HEAD origin/main` → empty; `git rev-list --left-right --count HEAD...origin/main` → `198 199`; `git diff --stat HEAD origin/main -- taskboard` → empty | the batch branches from `origin/main` (`present-v2`), local `main` untouched (PLAN Key decisions) |
| P-6 | A teammate's `show_in_present` cannot hide a task in this board's presentation: pulled team tasks are parsed for the team views only and never join `board.tasks`, which is all `present_tasks` reads | premise | TRUE | `taskboard/team_sync.py:208-229` (`foreign_tasks` builds a separate list); `views.py:6057-6061` (`present_tasks` reads `board.visible_tasks`) | the flag rides the push record as task data; no `team_sync` change (ARQ finding 4) |

- **Premise evaluation:** 6 premise(s) · ✅ TRUE ×6

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

- **Fork preconditions:** none — this batch runs one lane: increments 001 → 002 → 003 land in order on one branch, one owner (the orchestrator) holds the trunk.

---

## 3. High-level requirements (HLR)

### HLR-1601 — The presentation carries its dates
- **Traceability:** US-1601
- **Ledger:** LED-2026-10-16-batch-01.1, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5, LED-2026-10-16-batch-01.7, LED-2026-10-16-batch-01.8
- **Statement:** When the presentation is painted, the system shall draw a two-row date ruler above the field (month bands with today and the project's due, then day ticks or the cursor task's exact dates) and shall end every field row with that row's start–end chip, the brief rows keeping the relative days.
- **Rationale (informative):** the shipped field showed bars with no calendar; the operator chose variant B with chips.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_present.py tests/test_present_rulers.py tests/test_present_room.py -q`
- **Numeric pass threshold:** every arm passes; the painted frames equal the re-captured oracle `.dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R2-118x30.txt` / `PRES-R2-80x24.txt` line for line (PRES-R2: increment 004's re-capture after the operator's verdict of 2026-10-17; increment 001's `PRES-R-*.txt` stay on disk as its evidence) (TC-1001, TC-1002 and AT-1001's frame arm, all three repointed there); the oracle's independence from the renderer rests on `evidence/gen_frames.py` (§6.3) and on the literals TC-1601/TC-1602/AT-1601 write by hand from the fixture's dates.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** after `R`, the frame's second row names the month(s) and today's date in the label column, the third row carries the cursor task's dates (or the day ticks), and each field row ends in `Sep 24–28`-style chip; moving the cursor moves the dates on the tick row.
  - **Shipped surface:** key `R` → `PresentScreen` `#present-frame`.
  - **Acceptance test(s):** AT-1601
  - **Boundary catalog (QC-3):** ☑ empty (a project with no open task: the ruler still paints — TC-1601) ☑ boundary (80×24; a cross-month span; start == due; no start; no due; no dates) ☑ invalid (an unparseable date reads as absent — TC-1602) ☐ error — none new
  - **Negative control:** the shipped renderer at the batch's base paints no month row (AT-1601 is RED on base).

### HLR-1602 — A task can be left out of the presentation, persistently
- **Traceability:** US-1602
- **Ledger:** LED-2026-10-16-batch-01.2, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.6
- **Statement:** While the presentation is open:
  1. `space` shall hide the cursor task and save the board at once (TC-1604, AT-1602);
  2. `a` shall show every hidden task again and save the board when it changed a flag (TC-1604, AT-1602);
  3. a hidden task shall leave the field and the brief, and the field's time axis shall fit the shown tasks (TC-1604);
  4. the cursor shall skip hidden tasks (TC-1604);
  5. the hidden count shall appear in the hint row only, never in the frame or the export (TC-1604, AT-1602);
  6. the flag shall persist on the task in the board file (TC-1603) and be editable in the task editor as "Show in presentation" (TC-1605).
- **Rationale (informative):** «Que se guarde en la tarea, una bandera basta.»
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_present_hide.py tests/test_present.py tests/test_report.py -q`
- **Numeric pass threshold:** every arm passes.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `R`, `space` → the cursor task's title is gone from the painted frame, the hint row ends `· 1 hidden`, the `board.json` on disk differs from before by that task's flag only; `x` → the exported SVG holds no `hidden`, not the hidden task's title, and the header's open count one lower; restart and `R` → still hidden; `a` → it is back and the file equals its original bytes.
  - **Shipped surface:** key `R` → `PresentScreen` (`#present-frame`, `#present-hint`), the board file on disk, the task editor (`e`).
  - **Acceptance test(s):** AT-1602
  - **Boundary catalog (QC-3):** ☑ empty (every task hidden — TC-1604) ☑ boundary (hiding the last task in the list moves the cursor up; `a` with nothing hidden writes nothing — TC-1604) ☑ invalid (a hand-edited non-boolean is read as shown — TC-1603) ☐ error — none new
  - **Negative control:** on the base tree `space` hides nothing — the cursor task's title stays painted (AT-1602 RED on base).

### HLR-1603 — The `?` help shows the global keys without scrolling and every view key whole
- **Traceability:** US-1603
- **Ledger:** LED-2026-10-16-batch-01.3, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5
- **Statement:** When `?` is opened, the help modal shall show the global palette-only keys pinned at the bottom of the modal outside its scroll area, visible without scrolling at every supported size (80×24 and up), and shall list the view's keys whole in a full-width band under the usage and legend columns, inside the scrolled body, in as many columns as the box's inner width holds.
- **Rationale (informative):** the capture `out/legend-shipped.svg` shows the Keys list cut at the box edge and `R`/`S` absent.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_help_keys.py tests/test_help_clip.py tests/test_legend.py tests/test_setup_help.py -q`
- **Numeric pass threshold:** every arm passes.
- **Priority:** medium
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** in the gantt view, `?` at 118×30 and at 80×24 → the painted screen (the compositor's rows) shows `R Present` and `S Standup` with no scroll; the Keys band, scrolled into view, paints the gantt keys whole (the AT hard-codes the `<key> <label>` pairs it checks).
  - **Shipped surface:** key `?` → `HelpModal`.
  - **Acceptance test(s):** AT-1603
  - **Boundary catalog (QC-3):** ☑ boundary (80×24, the smallest supported size; 118×30) ☐ empty — none: every view has keys ☐ invalid — none ☐ error — none
  - **Negative control:** on the base tree the painted screen holds neither `R Present` nor `S Standup` (AT-1603 RED on base).

---

## 4. Low-level requirements (LLR)

### LLR-1601.1 — The ruler rows, re-seated in the present columns
- **Traceability:** HLR-1601
- **Ledger:** LED-2026-10-16-batch-01.1, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5, LED-2026-10-16-batch-01.8
- **Statement:** `views.render_present` shall paint, between the header and the span row, the month row from `gantt_month_row` (the project's due as `◆` in the project's colour) labelled `today <Wkd> <Mon D>` in `accent`, and the tick row from `gantt_day_row` with the cursor task's `gantt_echo`, labelled `selected task ▸` in the echo's tone, bold, when the echo's label fits in the field, with the echo's full text plus ` ▸` in the echo's tone when it did not, with `selected: no dates` in `dim` when the cursor task has no date, and with the scale label in `dim` only when there is no cursor task (never while one exists); both rows in the present columns (label | gutter | field | space + chip-width blank); today's number and rule on the ruler in `accent`, the echo in its own tone (`bright`, `over` when past due); no weekend background on either row; `gantt_day_row` shall take a keyword `shade_weekends` defaulting to `True`, so the gantt view's output is unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_present_rulers.py tests/test_present_room.py -q -k "TC_1601 or TC_1608"`
- **Numeric pass threshold:** TC-1601 passes: the ruler markup carries `accent` on today's cells, the echo cells in `bright` (in `over` when the cursor task is past due), no weekend background anywhere in the frame — the fixture's window spans several weekends (Sep–Oct 2026), so the arm can go RED; the gantt day row with the default still carries the weekend background. TC-1608 passes: at 118×30 and 80×24 the frame and its `x` SVG hold none of `hybrid`, `cursor`, `move the`, `←→`, `notes expand`; the oracle cursor's tick label is `selected task ▸` in `over`, bold; every open task in turn, and one with no dates, never gets the scale label; with no open task the scale returns; the too-long echo keeps `Sep 1 → Oct 14 ▸`.
- **Negative control:** TC-1601's weekend arm goes RED when the present ruler shades weekends (mutation `shade_weekends=False` → `True`).
- **Boundary catalog:** ☑ boundary (the echo label too long for the field → the label column carries it) ☑ empty (no cursor task → the scale label; no open task → the ruler still paints — TC-1601; a cursor task with no date → `selected: no dates` — TC-1608) ☐ invalid — none ☐ error — none

### LLR-1601.2 — Start–end chips on every field row
- **Traceability:** HLR-1601
- **Ledger:** LED-2026-10-16-batch-01.1, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5
- **Statement:** `views` shall provide `present_span_label(start, due)` returning `<Mon D>–<D>` when both dates fall in one month of one year, `<Mon D>–<Mon D>` across months (across years too, with no year: `Dec 28–Jan 3`), `due <Mon D>` with no start, `<Mon D>` when start equals due, `from <Mon D>` with no due, and `no dates` with neither; the span row (the project's start and due) and every task row shall end with that label right-aligned in a 13-cell chip, toned `over` when the due is before today, `dim` with no dates, `mut` otherwise; the present columns shall be label 30 / chip 13 when the width is at least 100, label 20 / chip 13 below; the brief rows keep the relative due unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_present_rulers.py -q -k TC_1602` and the oracle arms `tests/test_present.py -k "TC_1001 or TC_1002"`
- **Numeric pass threshold:** TC-1602's six label cases, the cross-year case, an unparseable date read as absent, and three tones pass; TC-1001/TC-1002 equal `.dev-flow/2026-10-16-batch-01/evidence/frames/PRES-R-118x30.txt` / `PRES-R-80x24.txt` line for line; TC-1602 also checks the oracle board's chips as literals written by hand from `tests/present_board.py`'s dates.
- **Negative control:** chip width 12 clips `Aug 21–Oct 10` (TC-1602 width arm RED at 12).
- **Boundary catalog:** ☑ boundary (cross-month, cross-year, start == due) ☑ empty (no dates) ☑ invalid (an unparseable date reads as absent, `parse_iso` — TC-1602) ☐ error — none

### LLR-1602.1 — The flag on the task, absent from the file when on
- **Traceability:** HLR-1602
- **Ledger:** LED-2026-10-16-batch-01.2, LED-2026-10-16-batch-01.6
- **Statement:** `Task` shall carry `show_in_present: bool = True`, and `show_in_present` shall be in `_TASK_KEYS` (so the raw value never also lands in `extra`, where `_to_dict`'s merge would resurrect a `false` after the flag is turned back on); `Task.from_dict` shall read it as `False` only when the record holds the JSON `false` under `show_in_present`; `Board._to_dict` shall omit the key when it is `True`, so a board with no hidden task serialises byte-identical to the base; the key travels in the team push record like any task field (P-6).
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_present_hide.py -q -k TC_1603`
- **Numeric pass threshold:** TC-1603 passes: a round-trip of the oracle board is byte-identical; a hidden task writes `"show_in_present": false` and nothing else changes; a non-boolean value (`"no"`) loads as shown and is dropped on the next save (a declared byte change for that hand-edited file only); after hide-then-show the record holds no `show_in_present` and nothing in `extra`.
- **Negative control:** dropping the omission writes the key on every task (TC-1603 byte arm RED).
- **Boundary catalog:** ☑ boundary (the key absent; `true`; `false`) ☑ invalid (a string `"no"` loads as shown) ☐ empty — none ☐ error — none

### LLR-1602.2 — `space` / `a` in the presentation, the filter, the hint count
- **Traceability:** HLR-1602
- **Ledger:** LED-2026-10-16-batch-01.2, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5, LED-2026-10-16-batch-01.8
- **Statement:** `views.present_tasks` shall return only the shown tasks (the open ones by due, and all), and `views.present_hidden` the hidden ones among the tasks `present_tasks` would otherwise return (visible, open or done, of that project); the field's axis is built over the shown open tasks only, so hiding the task with the latest due narrows it; `PresentScreen` shall bind `space` to hide the cursor task (the cursor moves to the next shown task by due, or the previous one at the end, or none) and `a` to show every hidden task, both with `priority=True` like the screen's other keys (the app's own `a` add-task never fires under the presentation), each saving the board when it changed a flag and writing nothing otherwise; with every task hidden the frame paints the header, the ruler (scale label), the span row and the separator, and no brief row; the hint row shall read `←→ ↑↓ move · ␣ hide · a show all · x export · esc leave` at width ≥ 100, `←→ move · ␣ hide · a all · x export · esc` below (the commission's exact texts), followed by ` · <n> hidden` when n > 0, where n = `len(present_hidden(board, project_id))`; the frame (and therefore the `x` export) shall never carry the hidden count; opening, moving, exporting and leaving shall write nothing.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_present_hide.py -q -k "TC_1604 or AT_1602"` and `tests/test_present.py tests/test_report.py`
- **Numeric pass threshold:** TC-1604 (filter; axis narrows; next-task cursor; last-task cursor; all hidden; `space` with every task hidden writes nothing; `a` with nothing hidden writes nothing; `a` opens no editor; hint texts; the frame never holds `hidden`) and AT-1602 pass; AT-1001 and `test_pressing_R_opens_the_presentation_read_only` still record zero saves for `R`/move/`x`/`esc`. Undo: `show_in_present` is not in `_UNDO_FIELDS` (`app.py:1502-1504`), so undoing an earlier board action neither restores nor overwrites a flag.
- **Negative control:** a `space` that does not save leaves the file unchanged (AT-1602 file arm RED).
- **Boundary catalog:** ☑ empty (all hidden) ☑ boundary (the last task hidden; `a` with nothing hidden) ☐ invalid — none ☐ error — none

### LLR-1602.3 — "Show in presentation" in the task editor
- **Traceability:** HLR-1602
- **Ledger:** LED-2026-10-16-batch-01.2, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5
- **Statement:** `TaskModal` shall carry a `Checkbox` labelled `Show in presentation` (id `f-present`) in the title row (`#task-head`, after the title input; the chip row's measured `TASK_CHIPS_ONE_ROW` = 137 and its 80-column folded form stay unchanged), checked from the task's flag (checked for a new task); it is the tab stop after the title (a consequence of the placement, accepted), and its result shall carry `show_in_present`; the edit and add paths shall apply it like the other flags; the editor's measured one-row and folded layouts shall hold at 80 columns and above.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_present_hide.py -q -k TC_1605` and `tests/test_edit_window.py`
- **Numeric pass threshold:** TC-1605 passes (at 80×24 `f-present` is fully painted on screen and `space` on it toggles it; unchecking + Save writes the flag); the editor window sweep stays green with `TASK_CHIPS_ONE_ROW` unchanged.
- **Negative control:** unchecking the box and saving writes the flag (TC-1605 RED if the result drops the key).
- **Boundary catalog:** ☑ boundary (new task: checked) ☐ empty ☐ invalid ☐ error — none

### LLR-1603.1 — The Keys band
- **Traceability:** HLR-1603
- **Ledger:** LED-2026-10-16-batch-01.3, LED-2026-10-16-batch-01.4
- **Statement:** `HelpModal` shall move the view's keys (`bar_keys(mode)`) out of the right column into a band under the two columns: the heading `Keys · this view` and a column-major grid whose cell width is the longest `<show> <label>` plus two, whose column count is the box's inner width divided by that, and whose row count is the key count divided by the column count, rounded up.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_help_keys.py -q -k TC_1606`
- **Numeric pass threshold:** TC-1606 passes: every key appears exactly once, column-major, no line wider than the inner width; the order arm uses 7 keys at a width holding 3 columns (3 rows, the last column short), where row-major and column-major differ.
- **Negative control:** a row-major grid fails the order arm.
- **Boundary catalog:** ☑ boundary (inner width smaller than one cell → one column; 7 keys in 3 columns) ☐ empty — every view has keys ☐ invalid ☐ error — none

### LLR-1603.2 — The pinned global line
- **Traceability:** HLR-1603
- **Ledger:** LED-2026-10-16-batch-01.3, LED-2026-10-16-batch-01.4, LED-2026-10-16-batch-01.5
- **Statement:** `keymap` shall provide `global_keys(view)` — the live `KEYMAP` entries with `bar=False`, in declaration order; `HelpModal` shall paint them as `Global  <show> <label>  <show> <label> …` (entries joined by two spaces) docked at the bottom of the box, outside the scrolled content, wrapped only at an entry boundary when the inner width cannot hold one line, with the `m full map · ? palette · esc/q closes` hint on its own pinned row below it: 2 pinned rows at 118×30 (inner width 104, the global line ~101 cells), 3 at 80×24 (inner width 70, the global line in 2 rows).
- **Validation:** `test (unit)` + `test (integration)`
- **Executed verification:** `python -m pytest tests/test_help_keys.py -q`
- **Numeric pass threshold:** TC-1607 (the line is derived from `KEYMAP`: every `bar=False` key, no other; the expected row count at 104 and at 70 is computed from the `KEYMAP`-derived entries, not hard-coded — today 1 and 2; no entry split) and AT-1603 pass.
- **Negative control:** a hand-typed list missing a newly added global key fails TC-1607.
- **Boundary catalog:** ☑ boundary (80 columns: the line wraps at an entry boundary) ☐ empty ☐ invalid ☐ error — none

### Information Flow Contract (IFC) — C-54

- **Part A — flows:**

```
FLOW: the presentation, from the board file to the screen, the board file and the reports/ folder
  SOURCE : the board file on disk (projects, tasks, start/due dates, show_in_present); the keys R, ←→↑↓, space, a, x, esc; the selection
  NODES  :
    - fn    : views.render_present ruler rows (gantt_month_row, gantt_day_row shade_weekends=False, gantt_echo) in the present columns
      owner : LLR-1601.1
    - fn    : views.present_span_label + the field-row chip + _present_cols
      owner : LLR-1601.2
    - fn    : models.Task.show_in_present + Task.from_dict + Board._to_dict omission
      owner : LLR-1602.1
    - fn    : views.present_tasks / present_hidden filter + PresentScreen space / a / hint count
      owner : LLR-1602.2
    - fn    : modals.TaskModal f-present checkbox + its result key
      owner : LLR-1602.3
  SINK   : the terminal surface (#present-frame, #present-hint), the board file on disk, the reports/ exports
```

```
FLOW: the help modal, from the key seat to the screen
  SOURCE : KEYMAP (taskboard/keymap.py), the current view, the terminal size
  NODES  :
    - fn    : HelpModal Keys band (column-major grid over bar_keys)
      owner : LLR-1603.1
    - fn    : keymap.global_keys + HelpModal pinned global line
      owner : LLR-1603.2
  SINK   : the terminal surface (the ? modal)
```

- **Part B — boundary decomposition:** `no — no component of the boundary is addressable on its own: both surfaces are modal screens of the one TUI; the board file is the existing record, gaining one optional key.`

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer A: TC-1601 … TC-1608, plus the repointed TC-1001/TC-1002. Layer B: AT-1601, AT-1602, AT-1603, each driving the real app headless (`run_test`) and reading the painted screen or the file on disk.

### 5.2 Batch acceptance criteria
- every LLR has a passing TC; every story a passing AT driving the shipped surface;
- every new assertion RED on the base tree or by a recorded mutation;
- the full suite green at each increment, transcript under the batch's evidence;
- app captures at 118×31 and 80×25 per increment under the batch's evidence.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
See `PLAN.md` §Key decisions and the PDR record.
### 6.3 Open risks
- The oracle frames are re-captured from the shipped renderer. `evidence/gen_frames.py` writes them and cross-checks every row against the approved prototype's `render_b2` (`prototypes/present_rulers/app_capture.py`), called at both sizes: every row must be equal except one listed delta — D3 row 2's label column only (the shipped tick row reads `selected task ▸`, the operator's verdict of 2026-10-17; `render_b2` wrote `cursor's dates ▸` there — the field and chip cells must still match). Increment 004 retired the former deltas D1 (the header's ` — hybrid` suffix) and D2 (the in-frame keys row): the shipped frame carries neither, so row 0 and the last content row now match `render_b2` byte for byte. The prototype composes the same ruler builders, so the cross-check proves the layout and the chips, not the ruler cells; the ruler cells are pinned by hand-written literals (TC-1601/TC-1602/AT-1601). At 80 columns the operator saw only the app frames at 80×25, never an 80×24 `render_b2` frame — ⏸ DEFER the operator's visual verdict on the 80-column oracle frame — owed, carried to `BACKLOG.md` at the close.
- **Security questions (the P1 scan, iteration 1: `security_required: true` on the pattern `form`):** the hit is the phrase "its 80-column folded form" — the editor's chip-row LAYOUT, not an input form. The batch adds no new text input: one checkbox in the existing task editor and the keys `space`/`a`; no auth, secret, network or external integration. The one security-relevant surface is C8 (markup over board-file text): every new row (ruler, chips, hint count, global line) is built from parsed dates, integers or `KEYMAP` literals, and the S1 escape/width law (TC-1003) keeps covering the titles. No open security risk.
- A stray `space` mid-meeting can only be recovered with `a`, which also reveals tasks hidden on purpose (no undo — out of scope by decision). A stated limit.
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-16-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```

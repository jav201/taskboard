# Requirements Document — taskboard — Batch 2026-10-29-batch-01

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

The live contract of batch `2026-10-29-batch-01`: the app exports two HTML reports of every
loaded board from ONE data extraction — **B, the workspace** (gantt, table, notes, milestones;
filter and display controls whose state lives in the URL hash; an "Export this view" action that
prints the configured view or downloads a self-contained file holding only the filtered data)
and **C, the deck** (cover, overview, one slide per chosen project, paged by keys). A global
`H` modal writes them to `<board dir>/reports/` and a toast offers `o` to open the file. The
design is the prototype round `prototypes/html_report/` (variants B and C, chosen by the
operator on 2026-10-29); the decisions are HR-1..HR-6 of the commission.

### 1.2 Scope

Covers: three NEW modules — `taskboard/report_html.py` (the extraction and the shared HTML
helpers), `taskboard/report_workspace.py` (B), `taskboard/report_deck.py` (C) — and the `H`
export in `taskboard/app.py` (the action, the board collection, the toast, the `o` offer),
`taskboard/modals.py` (`ReportExport`) and `taskboard/keymap.py` (the `H` seat); README's key
documentation (docs, not source).

Does NOT cover: the old CLI report `taskboard --report` (`taskboard/report.py`, `build_report`)
— it stays byte-unchanged (HR-1); the presentation's `x` SVG/PNG export (it stays, HR-2); any
write back to a board from a report (the reports are read-only); team folders; CI installing a
browser (declared, §6.3).

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| workspace (B) | `reports/workspace-<date>.html`: the interactive report — control bar, gantt, table, notes, milestones, embedded JSON |
| deck (C) | `reports/deck-<date>.html`: cover + overview + one slide per project in scope, paged by keys, one slide per printed page |
| the dict | the JSON-able facts `report_html.extract(...)` returns; the ONLY input of both renderers (HR-1) |
| scope | `o` all loaded boards (default) or `p` the current project, chosen in the `H` modal |
| loaded boards | `app.board_lanes(app)` (`taskboard/app.py:841`): every active registry board, the open one as the app holds it, the others via `peek_board`; missing/unreadable skipped |
| current project | the selected task's project, else the focused project (`F`, `focused_project_id`, `taskboard/app.py:1238`), else none |
| view | the state of B's controls: projects, status, people, classes, dates, search, sections, zoom |
| the hash | B's URL fragment `#v=1&p=..&s=..&u=..&m=..&from=..&to=..&q=..&sec=..&z=..` |
| filtered download | B's "Download this view": a new self-contained HTML whose embedded JSON holds only the kept tasks |
| late / open | a task is `late` when open and due before today; `open` when open and not late |
| hostile text | board text carrying HTML (`<script>alert(1)</script>`), quotes and `&` — board files are untrusted input |

### 1.4 References

- `.dev-flow/COMMISSION-html-report.md` — the commission (HR-1..HR-6, increments, AT-a..AT-g, evidence).
- `prototypes/html_report/variant_b/` and `variant_c/` (`build.py`, `NOTES.md`), `fixture.py`, `shot.py` — the design (commit `65deb62`, print fix `6c1225f`).
- `taskboard/report.py` — the old CLI report and its honesty helpers `_e` (`:78`), `_due_word` (`:85`), `report_path` (`:265`); its laws in `tests/test_report.py`.
- `tests/test_modal_keys.py:267` — the modal-key law's `INVENTORY` (batch 2026-10-20-batch-03).
- `evidence/p1-probes.txt` (draft-time probes) and `evidence/rc-p0.txt` (RC-1/RC-2).

### 1.5 Document overview

§2 the story, its premises and the fork declaration. §3 seven HLRs (one per decision limb).
§4 the LLRs, each naming its source module, its touched symbols (the C-26 reverse census) and
its verification nodes. The IFC follows §4. §5 validation. §6.3 the security answers (family C).

---

## 2. Overall description

### 2.1 Product perspective

Today the app exports a board as the CLI's static single-board HTML (`report.py`) and the
presentation as SVG/PNG pictures (`x` in `R`). The operator found the SVG hard to use and asked
for an interactive HTML report exported from the app. The new modules sit beside `report.py`:
`report_html` reads boards (models, views helpers, people) and produces the dict; the two
renderers turn the dict into one self-contained file each; the app collects the loaded boards,
asks the modal what to write and where, writes, and offers to open. Nothing in a report writes
back to a board.

### 2.2 Product functions

- Extract every fact both reports show, once, into a JSON-able dict (HR-1).
- Render B with the HR-3 control bar and URL-hash state, and the HR-4 view export (print, download).
- Render C from the same dict: cover, overview, one slide per project in scope (HR-5).
- Escape every board string; work offline as one file; light/dark; phone width (HR-6).
- `H` → modal (`b`/`c`/`a`, `p`/`o`, `esc`) → files in `reports/` → toast → `o` opens (HR-2).

### 2.3 User characteristics

The board's owner (`username_subject` in tests and captures), who exports and configures a
view, and a recipient who opens a file in a browser with no app installed. No other role.

### 2.4 Constraints

- Four increments, at most 4 SOURCE files each (001: 2, 002: 1, 003: ≤2, 004: 3); tests uncapped.
- Standard library only in the shipped code (no new runtime dependency); the browser tests use Playwright, installed on this Windows machine and not declared in `requirements.txt` (`evidence/p1-probes.txt` probe 7) — guarded by `pytest.importorskip`.
- English UI strings; synthetic data only; the operator's real name never appears.
- `report.py`, `build_report` and `tests/test_report.py` unchanged; the `x` export unchanged.

### 2.5 Assumptions and dependencies

- The helpers the extraction consumes exist unchanged (§2.7 row 2).
- The sync Playwright API cannot run inside the asyncio loop a Textual pilot test runs in (§2.7 row 7): the app-level ATs load the written file headless outside that loop (a worker thread or a subprocess) — `assumed — verify in Phase 3` which one.
- Chromium (Playwright's) renders `prefers-color-scheme`, `@media print` emulation and downloads headless (prototype `shot.py`; `evidence/p1-probes.txt` probe 7).

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-3101 | As the board's owner, I export my boards from the app as an HTML workspace I can filter and as a concise deck, and I can send a recipient exactly the view I configured, so I share only what each person should see. | the operator's request and verdict, quoted in `.dev-flow/COMMISSION-html-report.md` | READY |

#### Refinement log (one block per story)

**US-3101 — the HTML reports exported from the app (B + C)**
- **Context of use:** user = the board's owner, an expert keyboard user of the app · task = sharing board status with different people (a client, a teammate) · environment = Windows terminal app, reports opened in a desktop or phone browser, offline, sent as a file · observable outcome = the files exist in `reports/`, open in a browser, filter, and a downloaded view holds only what was shown.
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the board's owner · outcome = two HTML reports from one extraction; B's controls (projects, status, people, classes, dates, sections, reset, count, keyboard, hash); B's view export (print, filtered download); C's slides per chosen project; `H` modal, files, toast, `o` · why = the SVG export was hard to use, and "no siempre queremos mandar toda la información a distintas personas" · out of scope = editing from a report, re-pointing the CLI report, replacing the `x` export, team folders.
- **Feasibility (E, S):** implementation path = port the round's `variant_b/build.py` and `variant_c/build.py` into three modules over one dict; the app reuses `board_lanes`, `notify`, the `KEYMAP` seat and the modal-key law · dependencies/unknowns = none blocking; the asyncio/Playwright interaction is a test-harness detail (§2.5) · fits one batch? = yes, in the commission's four increments.
- **Evaluability (T) — behavioral, black-box:** "When the owner presses `H` then `b`, the toast names `workspace-<date>.html` and the file loads in a browser with 0 console errors and 0 external requests; when the owner's view hides project X and the owner presses Download this view, X's task titles are absent from the downloaded file's bytes." → AT-3101..AT-3107.
- **Open questions:** none — the commission and the orchestrator's brief pin HR-1..HR-6; where they are silent this contract decides and `PLAN.md` §Key decisions records it.
- **Classification:** `READY` — INVEST closed on all six axes; the outcome is observable through the app's keys and the written files; seven black-box ATs stated.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | `H` has no seat in `KEYMAP` on HEAD nor on `origin/main` | premise | ✅ TRUE | `grep -n 'Key("H"' taskboard/keymap.py` exit 1; uppercase seats `['A','B','F','I','L','M','P','R','S','T','X']` (`evidence/p1-probes.txt` probe 1); `git show origin/main:taskboard/keymap.py \| grep -n 'Key("H"'` exit 1 (`evidence/rc-p0.txt`) | HR-2 seats `H` (LLR-3107.1) |
| 2 | The consumed helpers exist: `report._e` `:78`, `_due_word` `:85`, `report_path` `:265`; `views.HEX` `:45`, `lanes_of` `:978`, `sitting` `:1744`, `highlight_segments` `:3505`; `people.mention_ids` `:67`, `split_mentions` `:75`; `models.parse_iso` `:648`, `days_in_phase` `:790`; `app.board_lanes` `:841`; `boards.peek_board` `:614` | premise | ✅ TRUE | `grep -n` of each (`evidence/p1-probes.txt` probe 2) | consumed unchanged (A3 not fired) |
| 3 | `report_path`'s slug rule maps `Client A` → `client-a` and `None` → `board`; `_due_word` gives `3d overdue`, `due today`, `in 4d`, `no date`, closed `-3d`; `_e` escapes `<`, `>`, `&`, `"` | premise | ✅ TRUE | executed: `C:\x\reports\client-a-2026-10-29.html`, `…\board-2026-10-29.html`, `['3d overdue', 'due today', 'in 4d', 'no date'] -3d`, `&lt;script&gt;alert(1)&lt;/script&gt; &amp; &quot;q&quot;` (probe 3) | LLR-3107.3's slug; LLR-3101.2's due words; LLR-3106.1's escape |
| 4 | `highlight_segments` drops the markers and keeps raw `<b>` in a segment; `split_mentions` keeps raw `<i>` in a piece — so the notes HTML must escape each segment | premise | ✅ TRUE | `[('a','soon'),(' ','mut'),('b','over'),(' ','mut'),('c','green'),(' <b>x</b>','mut')]`, `[('ask ',None),('@ana','ana'),(' about <i>it</i>',None)]` (probe 4) | LLR-3106.1 escapes per segment |
| 5 | None of the three modules, the fixture or the five test files exists yet | premise | ✅ TRUE | `ls` → `No such file or directory` × 8 (probe 5); `git ls-tree origin/main taskboard/report_html.py … \| wc -l` → `0` (`evidence/rc-p0.txt`) | every one `NEW — created in Phase 3` |
| 6 | The old CLI report's suite is green at `base_ref` and is this batch's regression pin | premise | ✅ TRUE | `env -u NO_COLOR python -m pytest -q tests/test_report.py` → `18 passed` (probe 6) | LLR-3101.2 keeps it at 18 passed |
| 7 | Playwright 1.62.0 + Chromium 151 run headless here; the sync API refuses to run inside a running asyncio loop | premise | ✅ TRUE | `playwright 1.62.0`, `chromium 151.0.7922.34`, `sync inside loop: Error It looks like you are using Playwright Sync API inside the asyncio loop.` (probe 7) | AT-3101/AT-3105 load the file outside the pilot's loop (§2.5) |
| 8 | `present_project_id` falls back to the first visible project, which HR-2's "no project selected" forbids | premise | ✅ TRUE | `taskboard/views.py:6540-6551` (the fallback at `:6550-6551`) | LLR-3107.2 does not reuse its fallback |
| 9 | The B1 census of tests naming the touched seats is the brief's list | premise | ✅ TRUE | `grep -rl KEYMAP tests/` → 15 files; `INVENTORY` → `tests/test_modal_keys.py`; `open_url` → `tests/test_app.py`, `tests/test_keymap.py`; `build_report` → `tests/test_report.py` (probe 8) | the P3 reverse census re-runs it per increment |

- **Premise evaluation:** 9 premise(s) · ✅ 9 TRUE / ❌ 0 FALSE / ❓ 0 UNDECIDABLE.

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ | one lane; A3 not fired — the consumed interfaces of §2.7 row 2 stay unchanged |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ | one lane; increments run in order 001→004 (A4 not fired) |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ | one lane; the B1 census (§2.7 row 9) is run at P2/P3 over the whole set |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ | the orchestrator owns the trunk |

- **Fork preconditions:** none — this batch runs one lane.

---

## 3. High-level requirements (HLR)

**The chains:** US-3101 → HLR-3101 (one extraction, HR-1), HLR-3102 (B and its controls, HR-3,
AT-b), HLR-3103 (filtered download, HR-4b, AT-c), HLR-3104 (print, HR-4a, AT-d), HLR-3105 (the
deck, HR-5, AT-e), HLR-3106 (escaping and offline, HR-6, AT-f), HLR-3107 (the `H` export, HR-2,
AT-a, AT-g). **Every AT node's docstring carries its bare id (`AT-3101`)**, which is the token
`V2` resolves — the function name `test_AT_3101_…` is not.

**The AT surface, declared once.** B's and C's behaviours (AT-3102..AT-3104, AT-3106) are
observed by driving the written HTML in headless Chromium — real clicks, real key presses, real
print emulation, a real download — and asserting the DOM, the network log and the downloaded
bytes. Increments 001–003 produce those files through `report_html.write_reports`, the very call
the `H` action makes; AT-3101, AT-3105 and AT-3107 drive the app by keys.

### HLR-3101 — both reports come from one extraction
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** When the reports are written, the system shall build both from one extraction of the loaded boards, people and milestone classes, so the workspace and the deck shall agree on every project, task, date and due word they show; the CLI report (`taskboard --report`) shall stay as it is.
- **Rationale (informative):** HR-1. The CLI report is a single-board, script-free document with its own laws (`tests/test_report.py`: read-only board, unaged, no forecast) serving scripts; re-pointing it to B would change a shipped CLI output outside the commission's increments. The extraction reuses its honesty helpers so the two cannot disagree on a due word.
- **Validation:** `test`
- **Executed verification:** AT-3105's `a` arm (P3, increment 004) plus LLR-3101.1..3's TCs; `env -u NO_COLOR python -m pytest -q tests/test_report.py` (18 passed at `base_ref`).
- **Numeric pass threshold:** for one `H a` export: the deck's project slide titles == the workspace's embedded non-archived project names in scope (set equality, same count) AND per project the deck's task count == the workspace's embedded task count for that project; `tests/test_report.py` 18 passed, 0 failed.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the two files written by one `H a` show the same projects with the same task counts; `taskboard --report` writes what it wrote before.
  - **Shipped surface:** the `H` modal's `a` key; the two files in `reports/`.
  - **Acceptance test(s):** AT-3105
  - **Boundary catalog (QC-3):** ☑ empty (a loaded board with no tasks: present in both with 0 tasks) ☑ boundary (scope `p`: one project in both) ☐ invalid (N/A — the dict is produced, not parsed from user input) ☑ error (an unreadable registry board: skipped in both, counted in the toast — LLR-3107.3)
  - **Negative control:** executed at P1 against `base_ref` — no extraction exists (`taskboard/report_html.py` absent, probe 5) and `H` has no seat (probe 1), so the `a` arm finds no file; the node-level RED is increment 004's mutation (the deck rendered from a second, divergent extraction that keeps archived projects) turning AT-3105's agreement arm red.

### HLR-3102 — the workspace filters by project, status, person, class and date, and the hash keeps the view
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** When the workspace is open, the system shall offer one control bar — a Projects selector (All, None, one checkbox per project grouped by board in its colour), Status chips (open, late, done, archived), People chips, Class chips, a from/to date range, Search, Section toggles (gantt, table, notes, milestones), Zoom and one Reset — where every control is a native focusable element showing its state and the bar shows the number of active filters; the gantt, table, notes and milestones shall show exactly the tasks every active filter keeps; the view shall be written to the URL hash on every change and restored from it on load and on `hashchange`.
- **Rationale (informative):** HR-3, the operator's note («mejoraras los controles para el display y filtro de información y de proyectos»). The hash makes a configured view bookmarkable and re-openable.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_workspace.py -k AT_3102` (node `tests/test_report_workspace.py::test_AT_3102_filters_and_the_hash_round_trip`, minted at increment 001) plus TC-3105..TC-3108.
- **Numeric pass threshold:** over the fixture, for each of the five filter kinds driven by clicks/keys: the set of task ids shown in the table == the set the truth table of LLR-3102.2 computes (0 extra, 0 missing); the active-filter count == the number of non-default filters; after the round trip (read `location.hash`, open a fresh page at that URL) the shown set and every control's state are identical (0 differences); Reset → the default shown set and `location.hash` == `""`.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** unchecking a project, pressing `late`, a person, a class or a date range narrows every section at once; the count reads the number of active filters; reopening the bookmarked URL shows the same view.
  - **Shipped surface:** `reports/workspace-<date>.html` in a browser.
  - **Acceptance test(s):** AT-3102
  - **Boundary catalog (QC-3):** ☑ empty (None projects → 0 tasks and a "no tasks match" line) ☑ boundary (a range whose `to` equals a task's start: the task shows; an undated task with a range set: hidden) ☑ invalid (a hash with unknown keys/values: dropped — LLR-3102.3) ☐ error (N/A — the page has no failing I/O)
  - **Negative control:** executed at P1 against `base_ref` — no workspace exists (probe 5); the node-level RED is increment 001's mutation: the status filter treats `late` as `open` (or `writeHash` skipped), and AT-3102's late arm (or round-trip arm) goes red.

### HLR-3103 — "Download this view" sends only the configured view
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** When the owner chooses "Download this view", the system shall write a new self-contained HTML file whose embedded data holds only the tasks the current view keeps, with projects, boards, people and classes reduced to those kept tasks use, and which opens on the same view with a header stating the filters applied and the export date; the control's label shall state that only this file leaves the hidden data out.
- **Rationale (informative):** HR-4(b): «no siempre queremos mandar toda la información a distintas personas». Trigger C4: the download is the batch's data-exposure control. Trigger B4: the file B produces is consumed by B's own code when the recipient opens it.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_workspace.py -k AT_3103` (node `tests/test_report_workspace.py::test_AT_3103_download_this_view_holds_only_the_filtered_tasks`, increment 002) plus TC-3109..TC-3111.
- **Numeric pass threshold:** with project X unchecked and one person filter on: the downloaded file's embedded task ids == the source page's shown ids; X's every task title and X's name occur 0 times in the downloaded bytes (raw and JSON-escaped forms both searched); 0 `deps`/`chain` entries name a dropped task; the downloaded file, re-opened headless, shows the same task set, its header contains the filter summary and the export date, and logs 0 console errors.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the recipient's file shows exactly the owner's view, and opening its source finds no trace of the hidden project.
  - **Shipped surface:** the workspace's "Download this view" control; the file `workspace-view-<date>.html` the browser saves.
  - **Acceptance test(s):** AT-3103
  - **Boundary catalog (QC-3):** ☑ empty (a view keeping 0 tasks: the file opens and says "no tasks match") ☑ boundary (a kept task depending on a dropped one: the dependency entry removed, the kept task stays) ☑ invalid (notes section off: every `notes_html` stripped from the file) ☐ error (N/A — the download is client-side, no I/O the page can fail)
  - **Negative control:** executed at P1 against `base_ref` — no download exists (probe 5); the node-level RED is increment 002's mutation: the download re-embeds the full data (no reduction), and AT-3103's absent-title arm goes red.

### HLR-3104 — printing prints the configured view and no controls
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** When the workspace is printed ("Print / Save as PDF" or the browser's print), the system shall hide every control and print the view header (filters applied, generated date, printed date) and the shown sections, with the whole gantt timeline and rows and cards never split across pages; the control's label shall state that the file still holds all data.
- **Rationale (informative):** HR-4(a). The print hides data visually only; HLR-3103 is the one output that leaves it out, and the UI says which.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_workspace.py -k AT_3104` (node `tests/test_report_workspace.py::test_AT_3104_print_hides_the_controls_and_shows_the_filter_header`, increment 002) plus TC-3112.
- **Numeric pass threshold:** under `emulate_media(media="print")` with one filter active: every control element's computed `display` == `none` (0 visible controls); the view header is visible and contains the filter summary and both dates; the gantt figure's rendered width ≤ the page width (no clipped timeline); the "Print / Save as PDF" control calls `window.print` exactly once per press.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the PDF shows the header and the chosen sections, the whole gantt, no buttons.
  - **Shipped surface:** the workspace in print media.
  - **Acceptance test(s):** AT-3104
  - **Boundary catalog (QC-3):** ☑ empty (no filter active: the header says "all tasks") ☑ boundary (sections all off but one) ☐ invalid (N/A — print takes no input) ☐ error (N/A)
  - **Negative control:** executed at P1 against `base_ref` — no workspace exists (probe 5); the node-level RED is increment 002's mutation: `.controls` dropped from the print rule, and AT-3104's 0-visible-controls arm goes red.

### HLR-3105 — the deck is concise and pages by keys
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** When the deck is written, the system shall render a cover, an overview and one slide per non-archived project in the chosen scope, in board then project order; the arrow keys, PageUp/PageDown and Home/End shall page through it while focus is not in a text field; printing shall put one slide on each page.
- **Rationale (informative):** HR-5 — «quisiera tener disponible la variante C que es más concisa». The scope chosen in the `H` modal is the deck's project filter.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_export_app.py -k AT_3105` (node `tests/test_report_export_app.py::test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project`, increment 004) plus TC-3113, TC-3114.
- **Numeric pass threshold:** `H o c`: slide count == 2 + the number of non-archived projects across the loaded boards, project slide titles == those names; `H p c` with a task of project Y selected: slide count == 3, the project slide titled Y; pressing `End` then `Home` shows the last then the first slide (`n / N` counter reads `N / N` then `1 / N`).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the deck's slides are the projects the owner chose, and the keys page through them.
  - **Shipped surface:** the `H` modal's `c` key; `reports/deck-<date>.html` in a browser.
  - **Acceptance test(s):** AT-3105
  - **Boundary catalog (QC-3):** ☑ empty (scope `o` with a board holding no project: it adds no slide) ☑ boundary (scope `p`: exactly one project slide; `ArrowRight` on the last slide stays there) ☐ invalid (N/A — no input parsed) ☐ error (N/A)
  - **Negative control:** executed at P1 against `base_ref` — no deck exists (probe 5); the node-level RED is increment 003/004's mutation: archived projects get slides, and AT-3105's count arm goes red.

### HLR-3106 — board text is shown, never run, and the files stand alone
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** If board text holds HTML, script, quotes or `&`, then both reports shall show it as literal text and shall run nothing from it; each report shall be one file that works offline with 0 external requests, in light and dark themes, with no horizontal page scroll at 390 px width.
- **Rationale (informative):** HR-6; triggers C8 (HTML rendering of file-derived text) and C6. Board files are untrusted — a teammate's pull or a hand-edited file can carry markup.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_deck.py -k AT_3106` (node `tests/test_report_deck.py::test_AT_3106_board_text_is_escaped_in_both_reports`, increment 003) plus TC-3115, TC-3116; AT-3101's 0-request arm.
- **Numeric pass threshold:** over the hostile fixture, in both files: 0 `dialog` events while loaded and paged; the hostile title is visible as the literal text `<script>alert(1)</script>`; the page holds exactly the `<script>` elements its template emits (count unchanged by the hostile fixture); the bytes contain 0 occurrences of `<script>alert(1)`; 0 requests other than the file itself; `scrollWidth ≤ clientWidth` at 390 px in light and dark.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** a task titled `<script>alert(1)</script>` reads as that text in both reports; nothing pops up; the files open with no network.
  - **Shipped surface:** both written files in a browser.
  - **Acceptance test(s):** AT-3106
  - **Boundary catalog (QC-3):** ☑ empty (empty title/notes: rendered empty, no error) ☑ boundary (`</script>` inside a note: cannot close the data element) ☑ invalid (hostile title, note, person name) ☐ error (N/A)
  - **Negative control:** executed at P1 against `base_ref` — the reports do not exist (probe 5); probe 4 shows the raw segments carry live markup (`' <b>x</b>'`) until escaped; the node-level RED is increment 003's mutation: one `_e` call removed from the deck's title cell, and AT-3106's literal-text arm goes red.

### HLR-3107 — `H` exports from the app, says where, and offers `o`
- **Traceability:** US-3101
- **Ledger:** none
- **Statement:** When the owner presses `H` on the main screen, the system shall open a modal whose every key is printed on it — `b` workspace, `c` deck, `a` both, scope `p` current project or `o` all loaded boards (default `o`, the chosen scope marked), `esc` close; `b`/`c`/`a` shall write the files to `<board dir>/reports/` and show a toast naming them and the folder and offering `o`; while that toast is on screen, `o` shall open the just-written file with the OS default handler; the presentation's `x` export shall stay as it is.
- **Rationale (informative):** HR-2. `H` is free (§2.7 row 1); global and off the bar like `R`/`A`/`S`; every modal key direct and shown (the modal-key law).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_report_export_app.py -k AT_3101` and `env -u NO_COLOR python -m pytest -q tests/test_modal_keys.py -k AT_3107` (nodes `tests/test_report_export_app.py::test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it`, `tests/test_modal_keys.py::test_AT_3107_the_report_modal_obeys_the_modal_key_law`, increment 004) plus TC-3117..TC-3121.
- **Numeric pass threshold:** `H b`: exactly 1 file `reports/workspace-<today>.html` under the open board's folder, non-empty, holding the embedded data; 1 toast whose text == `Report written: workspace-<today>.html to <dir> — o opens it`; the file loaded headless logs 0 console errors and 0 page errors and makes 0 requests other than itself; `o` within the toast's 10 s → 1 open call with that path; the modal shows the six keys `b c a p o esc` (6/6 printed); `ReportExport` is in `INVENTORY` as `{}` and the law's arms pass.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** `H b` writes the file and the toast says where; `o` opens it.
  - **Shipped surface:** the app's main screen (`H`, the modal, the toast, `o`).
  - **Acceptance test(s):** AT-3101, AT-3107
  - **Boundary catalog (QC-3):** ☑ empty (`p` with no current project: the modal reads "no project selected" and the scope stays `o`) ☑ boundary (`o` after the toast expired: `open_url` again; same-day re-export: overwritten) ☐ invalid (N/A — the modal takes keys only) ☑ error (a missing registry board: skipped and counted in the toast)
  - **Negative control:** executed at P1 against `base_ref` — `H` has no seat (probe 1), so pressing it writes nothing; the node-level RED is increment 004's mutation: the toast drops the file name (or `o` keeps `open_url`), and AT-3101's toast (or open) arm goes red.

---

## 4. Low-level requirements (LLR)

> Each LLR names its source module, the symbols it touches (the C-26 reverse census) and its
> verification. `NEW` = created in Phase 3; names are provisional until the increment mints
> them (V-5) and are reconciled at P4. TC ids are minted here; their nodes land in the named
> increment.

### LLR-3101.1 — `extract` returns the JSON-able facts of the loaded boards
- **Traceability:** HLR-3101
- **Ledger:** none
- **Statement:** `report_html.extract(boards, people, marks, today, project=None) -> dict` shall return only JSON-able values (`json.dumps` succeeds with no custom encoder): `meta` (generated date, today, scope), `boards`, `projects` (each with a key unique across boards — the board id joined to the project id — its board, name, colour, archived), `tasks` (each with a unique key, project key, title, phase, start, due, done, archived, milestone, mark, blocked, mentioned person ids, `deps` keys, `due_word`, `notes_html`, urls), `people` (directory people mentioned in a task) and `marks` (classes used). It shall read the boards and never write them. Source: `taskboard/report_html.py` (NEW). Touched symbols (C-26): `report_html.extract` NEW; consumes `views.lanes_of`, `views.sitting`, `models.parse_iso`, `models.days_in_phase`, `people.mention_ids` unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `tests/test_report_html.py::test_TC_3101_extract_is_json_and_holds_every_fact` (TC-3101, increment 001).
- **Numeric pass threshold:** over `tests/report_fixture.py` (NEW): `json.loads(json.dumps(d)) == d`; task count == the fixture's task count (archived included); project keys unique (`len(set) == len`); each board file's bytes identical before and after (0 changed).
- **Negative control:** a mutation keying projects by the bare project id makes two fixture projects collide and the uniqueness arm goes red (increment 001's battery).
- **Boundary catalog:** ☑ empty (a board with no tasks) ☑ boundary (two boards with the same project id) ☐ invalid (N/A — boards arrive parsed) ☐ error (N/A — unreadable boards never reach it, LLR-3107.3)

### LLR-3101.2 — the extraction reuses the CLI report's honesty helpers; the CLI report is unchanged
- **Traceability:** HLR-3101
- **Ledger:** none
- **Statement:** Every `due_word` in the dict shall be `report._due_word(days, closed)` (`taskboard/report.py:85`) for the task's due distance, and every server-side escape in the reports shall go through `report._e` (`:78`); `taskboard/report.py` and `tests/test_report.py` shall stay byte-unchanged. Source: `taskboard/report_html.py`. Touched symbols: none in `report.py` (consumed only).
- **Validation:** `test (unit)` + `inspection`
- **Executed verification:** `tests/test_report_html.py::test_TC_3102_due_words_are_the_cli_reports` (TC-3102, increment 001); `git diff 9da7438 -- taskboard/report.py tests/test_report.py` empty at every increment; `tests/test_report.py` re-run.
- **Numeric pass threshold:** for every fixture task, `due_word == _due_word(...)` (0 mismatches); the diff is 0 lines; `tests/test_report.py` 18 passed.
- **Negative control:** a mutation formatting the due word locally (`f"{d}d"`) reddens TC-3102's late-task arm (`3d overdue` ≠ `-3d`).
- **Boundary catalog:** ☑ boundary (due today; closed project → plain distance) ☑ empty (no due → `no date`) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3101.3 — the scope filters the extraction, and the renderers read the dict alone
- **Traceability:** HLR-3101, HLR-3105
- **Ledger:** none
- **Statement:** With `project=None` the dict shall hold every project and task of the given boards; with `project=<key>` only that project and its tasks (dependencies naming a task outside it removed). `report_workspace` and `report_deck` shall take only the dict: they shall import nothing from `taskboard.models`, `taskboard.boards`, `taskboard.views`, `taskboard.people`, `taskboard.marks`, `taskboard.app`, `taskboard.modals` or `taskboard.keymap`, and rendering the same dict twice shall give identical bytes. Source: `taskboard/report_html.py`, `taskboard/report_workspace.py`, `taskboard/report_deck.py` (all NEW). Touched symbols: `report_html.extract` (its `project` argument).
- **Validation:** `test (unit)` + `inspection`
- **Executed verification:** `tests/test_report_html.py::test_TC_3103_project_scope_keeps_one_project` (TC-3103, increment 001); `tests/test_report_deck.py::test_TC_3104_renderers_read_the_dict_only` (TC-3104, increment 003: the import probe `rg -n "^\s*(from|import) .*taskboard\.(models|boards|views|people|marks|app|modals|keymap)|^\s*from \.(models|boards|views|people|marks|app|modals|keymap)" taskboard/report_workspace.py taskboard/report_deck.py` → 0 hits, and the determinism arm).
- **Numeric pass threshold:** scope `p`: 1 project, its task count, 0 foreign keys in any `deps`; import probe 0 hits; `render(d) == render(d)` (byte equality).
- **Negative control:** a renderer importing `views.HEX` makes the import probe report 1 hit (red); scope ignoring `project` keeps all projects and the 1-project arm goes red.
- **Boundary catalog:** ☑ boundary (a cross-project dependency cut by the scope) ☑ empty (a project with no tasks in scope) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3102.1 — the control bar: every control native, visible, counted, keyboard-reachable; Reset
- **Traceability:** HLR-3102
- **Ledger:** none
- **Statement:** The workspace page shall carry one control bar: a `<details>` "Projects n/N" with All, None and one checkbox per project grouped by board with its colour chip; Status chips `open` `late` `done` `archived` (default all pressed but `archived`); one People chip per directory person mentioned in a task; one Class chip per class used; `from`/`to` `<input type=date>`; a Search input; Section toggles `gantt` `table` `notes` `milestones`; Zoom; Reset; the active-filter count. Every chip shall be a `<button aria-pressed>`, every control reachable by `Tab`, its state visible without hovering. Reset shall restore every default and clear the hash. Source: `taskboard/report_workspace.py` (NEW). Touched symbols: `report_workspace.render` NEW (the page template, its JS).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_workspace.py::test_TC_3105_the_bar_is_native_and_counted` (TC-3105) and `::test_TC_3108_reset_restores_the_defaults` (TC-3108), increment 001, headless.
- **Numeric pass threshold:** every control is a `button`/`input`/`summary` element (0 `div`/`span` click targets); `Tab` from the page top reaches each control (reached set == control set); chip `aria-pressed` == its filter state for all chips; the count text == the number of non-default filters after each of 5 actions; Reset → count 0, `location.hash == ""`.
- **Negative control:** a chip built as a `<span onclick>` is unreachable by `Tab` and TC-3105's reach arm goes red.
- **Boundary catalog:** ☑ empty (a board with no people → no People chips, the group hidden) ☑ boundary (one project: the selector reads `1/1`) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3102.2 — the filters' truth table
- **Traceability:** HLR-3102
- **Ledger:** none
- **Statement:** A task shall be shown when it passes every active filter, per this table (today = `meta.today`):

  | Filter | Off / default | Keeps a task when |
  |---|---|---|
  | Projects | all checked | its project is checked |
  | Status | open, late, done pressed | its status chip is pressed, status = `archived` if archived, else `done` if done, else `late` if due < today, else `open` |
  | People | none pressed (no filter) | it mentions ANY pressed person |
  | Classes | none pressed (no filter) | its milestone class is ANY pressed class |
  | Dates | no `from`, no `to` | its [start..due] span meets [from..to] (a missing bound is open; a one-date task is a point); undated tasks show only when no bound is set |
  | Search | empty | its title, notes text or project name contains the text, case-folded |

  Source: `taskboard/report_workspace.py` (JS). Touched symbols: `report_workspace.render` (its `applyFilters` JS function, NEW).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_workspace.py::test_TC_3106_filters_follow_the_truth_table` (TC-3106, increment 001): a parametrized arm per table row; each arm's expected set is computed in Python from the fixture by the table's rule, never read from the page.
- **Numeric pass threshold:** per arm, shown ids == expected ids (0 extra, 0 missing); 6 arms resolved (the arm count asserted before any verdict).
- **Negative control:** the mutation `late → open` (status ignores the due date) reddens the Status arm; `ANY → ALL` for people reddens the People arm.
- **Boundary catalog:** ☑ boundary (span touching `to`; due == today is `open`) ☑ empty (undated task with a range set) ☑ invalid (`from` > `to`: 0 tasks, the count shows the filter) ☐ error (N/A)

### LLR-3102.3 — the hash grammar is parsed against whitelists; nothing from it is injected
- **Traceability:** HLR-3102, HLR-3106
- **Ledger:** none
- **Statement:** The page shall write `#v=1&p=..&s=..&u=..&m=..&from=..&to=..&q=..&sec=..&z=..` (comma-separated values, URI-encoded) on every control change, and read it on load and on `hashchange`. Each value shall be accepted only when in its whitelist — `p` ⊆ project keys, `s` ⊆ {open, late, done, archived}, `u` ⊆ people ids, `m` ⊆ class ids, `sec` ⊆ {gantt, table, notes, milestones}, `z` ⊆ the zoom names, `from`/`to` matching `YYYY-MM-DD` and a real date; `q` shall only ever be assigned to the search input's `value`; an unknown key, value or `v` shall be dropped. No hash value shall reach `innerHTML`, a selector string or an attribute other than `value`. Source: `taskboard/report_workspace.py` (JS). Touched symbols: `report_workspace.render` (`parseHash`, `writeHash` JS functions, NEW).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_workspace.py::test_TC_3107_a_hostile_hash_is_dropped` (TC-3107, increment 001) — opens the page at `#v=1&p=<img src=x onerror=alert(1)>&s=bogus&q=%3Cb%3Ex%3C%2Fb%3E`; AT-3102's round-trip arm.
- **Numeric pass threshold:** 0 `dialog` events; 0 `img` elements created; the search input's `value` == `<b>x</b>` as text; the view == the default view but for `q`; 0 console errors.
- **Negative control:** a mutation that sets project labels from the hash via `innerHTML` creates the `img` and fires the dialog — TC-3107 red.
- **Boundary catalog:** ☑ invalid (hostile and unknown values) ☑ empty (no hash → defaults) ☑ boundary (`v=2` → hash ignored) ☐ error (N/A)

### LLR-3103.1 — the download reduces the data to the kept tasks
- **Traceability:** HLR-3103
- **Ledger:** none
- **Statement:** "Download this view" shall build its embedded JSON from the kept tasks only (the LLR-3102.2 result set): `projects`, `boards`, `people` and `marks` reduced to those the kept tasks use; every `deps`/`chain` entry naming a dropped task removed; every `notes_html` stripped when the notes section is off; the JSON escaped as LLR-3106.1 requires before it enters the file. Source: `taskboard/report_workspace.py` (JS). Touched symbols: `report_workspace.render` (`downloadView` JS function, NEW).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_workspace.py::test_TC_3109_the_download_keeps_only_used_entries` (TC-3109) and `::test_TC_3110_notes_off_strips_the_notes` (TC-3110), increment 002, headless with `expect_download`.
- **Numeric pass threshold:** in the downloaded JSON: task ids == shown ids; every project/board/person/class present is used by a kept task (0 unused); 0 dangling dependency keys; notes off → 0 non-empty `notes_html`; 0 raw `<` in the embedded JSON text.
- **Negative control:** a mutation keeping the full `people` list leaves a hidden person's name in the file — TC-3109 red.
- **Boundary catalog:** ☑ empty (0 kept tasks) ☑ boundary (a kept task whose dependency is dropped) ☑ invalid (notes off) ☐ error (N/A)

### LLR-3103.2 — the downloaded file opens on the same view and says so
- **Traceability:** HLR-3103, HLR-3104
- **Ledger:** none
- **Statement:** The page shall capture its own pristine shell at load, before any rendering, and the download shall reuse that shell with the reduced JSON and a `meta.view` holding the filter summary, the export date and the hash state, named `workspace-view-<date>.html`; opened, that file shall restore `meta.view`'s state and show a header stating the filters and the export date. The download control's label shall read that only this file leaves the hidden data out; the print control's label, that the file still holds all data. Source: `taskboard/report_workspace.py`. Touched symbols: `report_workspace.render` (the shell capture, the view header, NEW).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_workspace.py::test_TC_3111_the_view_file_reopens_on_its_view` (TC-3111, increment 002) — saves the download, re-opens it headless (B4's output-then-consume arm).
- **Numeric pass threshold:** the suggested file name matches `workspace-view-\d{4}-\d{2}-\d{2}\.html`; the re-opened page's shown ids == the source's; its header contains the summary and the date; 0 console errors; the two labels' texts present verbatim.
- **Negative control:** a mutation capturing the shell after rendering duplicates the rendered rows in the re-opened file — the id-set arm goes red (duplicates).
- **Boundary catalog:** ☑ boundary (re-downloading from a downloaded file: same set) ☑ empty (no filter: the header says all tasks) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3104.1 — the print stylesheet
- **Traceability:** HLR-3104
- **Ledger:** none
- **Statement:** The page's `@media print` shall hide the control bar, the task modal, the tooltip and every download/print control; show the view header (filters applied, generated date, and the printed date set on `beforeprint`); keep the round's full-gantt rules (`.gantt-wrap{overflow:visible}`, `#gantt{min-width:0!important}`, `#gantt svg{width:100%;height:auto}`, prototype commit `6c1225f`); and set `break-inside: avoid` on table rows and note/milestone cards. "Print / Save as PDF" shall call `window.print()`. Source: `taskboard/report_workspace.py`. Touched symbols: `report_workspace.render` (the stylesheet, NEW).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_workspace.py::test_TC_3112_the_print_rules_hold` (TC-3112, increment 002), headless print emulation.
- **Numeric pass threshold:** the three gantt rules and `break-inside: avoid` present in the page's stylesheet (4/4); under print media every control `display: none`, the header `display` ≠ `none`; `window.print` stubbed and pressed: 1 call.
- **Negative control:** dropping `#gantt{min-width:0!important}` leaves the gantt wider than the print page — the width arm goes red.
- **Boundary catalog:** ☑ boundary (a long project: rows not split) ☐ empty (N/A — the header always prints) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3105.1 — the deck's slides come from the dict in scope
- **Traceability:** HLR-3105, HLR-3101
- **Ledger:** none
- **Statement:** `report_deck.render(d) -> str` shall emit a cover (totals per board, the class legend), an overview (every project in scope on one timeline) and one slide per non-archived project of the dict, in the dict's board-then-project order, each a vector gantt with real `<text>` labels, today's rule, dependency arrows and the project's notes, from the dict alone. Source: `taskboard/report_deck.py` (NEW). Touched symbols: `report_deck.render` NEW.
- **Validation:** `test (unit)`
- **Executed verification:** `tests/test_report_deck.py::test_TC_3113_one_slide_per_project` (TC-3113, increment 003).
- **Numeric pass threshold:** slide count == 2 + non-archived projects of the fixture dict; slide titles in order == those names in order; scope-`p` dict → 3 slides.
- **Negative control:** a mutation iterating every project (archived included) adds one slide — the count arm goes red.
- **Boundary catalog:** ☑ empty (no project → cover and overview only) ☑ boundary (one project) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3105.2 — paging keys and one slide per printed page
- **Traceability:** HLR-3105
- **Ledger:** none
- **Statement:** The deck page shall page forward on `ArrowRight`/`PageDown`, back on `ArrowLeft`/`PageUp`, to the first slide on `Home` and the last on `End`, ignoring those keys while focus is in an `input`/`textarea`; it shall show an `n / N` counter and on-screen previous/next buttons; `@media print` shall print every slide, one per page, in the light palette. Source: `taskboard/report_deck.py`. Touched symbols: `report_deck.render` (the page JS and CSS).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_deck.py::test_TC_3114_keys_page_and_print_splits` (TC-3114, increment 003) — real `keyboard.press` calls, print emulation.
- **Numeric pass threshold:** after `End`: counter `N / N`; `ArrowRight` there: still `N / N`; `Home`: `1 / N`; `PageDown`: `2 / N`; under print media all N slides displayed with `break-after: page` (N/N).
- **Negative control:** a mutation dropping the `Home` handler leaves the counter at `N / N` — red.
- **Boundary catalog:** ☑ boundary (first and last slide) ☐ empty (N/A — cover and overview always exist) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3106.1 — escaping: server-side `_e`, client-side `textContent`, script-safe JSON, notes from escaped segments
- **Traceability:** HLR-3106, HLR-3103
- **Ledger:** none
- **Statement:** Every board string a renderer writes into HTML shall pass through `report._e`; every board string the page's JS sets shall be set with `textContent` (or an attribute value), never `innerHTML`; the embedded JSON — written by `report_html.embed_json(d)` and, client-side, by the download — shall carry `<`, `>`, `&` as `\u003c`, `\u003e`, `\u0026`, so no board text can close the data element; `notes_html` shall be built server-side by `report_html.notes_html(text, people)` from `highlight_segments` and `split_mentions` pieces, each piece escaped, wrapped only in constant tags. Source: `taskboard/report_html.py`, `report_workspace.py`, `report_deck.py`. Touched symbols: `report_html.embed_json` NEW, `report_html.notes_html` NEW; consumes `views.highlight_segments`, `people.split_mentions` unchanged.
- **Validation:** `test (unit)`
- **Executed verification:** `tests/test_report_html.py::test_TC_3115_embed_json_and_notes_are_inert` (TC-3115, increment 001) and AT-3106.
- **Numeric pass threshold:** `embed_json` of a dict holding `</script><b>&` contains 0 `<`, 0 `>`, 0 `&` and `json.loads` of it returns the original string; `notes_html('==a== <b>x</b> @ana')` contains `&lt;b&gt;` and 0 `<b>` outside the constant tags.
- **Negative control:** the prototype's `.replace("</", "<\\/")` form (`variant_b/build.py:708`) leaves `<b>` and `&` raw — the 0-`<` arm goes red against it.
- **Boundary catalog:** ☑ invalid (hostile title, note, person name) ☑ boundary (`</script>` in a note) ☑ empty (empty notes → empty `notes_html`) ☐ error (N/A)

### LLR-3106.2 — one offline file, light and dark, phone width
- **Traceability:** HLR-3106
- **Ledger:** none
- **Statement:** Each report shall inline all its CSS and JS and reference no external resource (no `src`/`href` to `http(s)`, no font, no CDN); task URLs shall appear only as `<a rel="noopener noreferrer">` links, never loaded; both pages shall define light and dark palettes via `prefers-color-scheme`, and lay out at 390 px with no horizontal page scroll. Source: `report_workspace.py`, `report_deck.py`. Touched symbols: both `render` functions (CSS, markup).
- **Validation:** `test (e2e)`
- **Executed verification:** `tests/test_report_deck.py::test_TC_3116_offline_themes_and_phone_width` (TC-3116, increment 003) over both files.
- **Numeric pass threshold:** per file: requests other than the file URL == 0; `scrollWidth ≤ clientWidth` at 390×844 in `light` and `dark` (2/2 per file); the body's computed background differs between the two schemes.
- **Negative control:** a mutation adding a Google Fonts `<link>` produces 1 external request — red.
- **Boundary catalog:** ☑ boundary (390 px) ☐ empty (N/A) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3107.1 — the `H` seat
- **Traceability:** HLR-3107
- **Ledger:** none
- **Statement:** `KEYMAP` shall gain one row `Key("H", "H", "report_export", "Report", group="misc", bar=False)`; `H` shall be named in `?` and in the palette like `R`, `A`, `S`; README's key documentation shall name it. Source: `taskboard/keymap.py` (`KEYMAP`, `:55`); README.md (docs). Touched symbols: `keymap.KEYMAP` (one NEW row); the action name `report_export` NEW.
- **Validation:** `test (unit)`
- **Executed verification:** `tests/test_report_export_app.py::test_TC_3117_H_is_seated_once_off_the_bar` (TC-3117, increment 004); the B1 census suites (`tests/test_keymap.py`, `tests/test_help_keys.py`, `tests/test_readme.py`) re-run.
- **Numeric pass threshold:** exactly 1 `KEYMAP` row with `show == "H"`, `bar is False`; `H` in `palette_commands()` and in the `?` text; the census suites 0 failed.
- **Negative control:** without the row, pressing `H` does nothing — TC-3117 red (probe 1 is the executed pre-state).
- **Boundary catalog:** ☑ boundary (`h` lowercase keeps its meaning) ☐ empty (N/A) ☐ invalid (N/A) ☐ error (N/A)

### LLR-3107.2 — the `ReportExport` modal: keys only, every key shown, scope marked
- **Traceability:** HLR-3107
- **Ledger:** none
- **Statement:** `modals.ReportExport` (NEW) shall be a `ModalScreen` with no `Button` and its own `BINDINGS` `b`, `c`, `a`, `p`, `o`, `escape`, each printed on the modal; the scope shall start at `o` and the chosen scope be marked; `p`/`o` shall change the scope and keep the modal open; `b`/`c`/`a` shall dismiss with `(kinds, scope)`; `escape` shall dismiss with `None`. The current project shall be the selected task's project, else `focused_project_id`, else none — not `present_project_id`'s first-project fallback (`views.py:6550`); with none, the `p` line shall read "no project selected" and pressing `p` shall leave the scope at `o`. `tests/test_modal_keys.py`'s `INVENTORY` shall gain `"ReportExport": {}`. Source: `taskboard/modals.py`. Touched symbols: `modals.ReportExport` NEW; `INVENTORY` (`tests/test_modal_keys.py:267`, one row).
- **Validation:** `test (integration)`
- **Executed verification:** AT-3107 and `tests/test_report_export_app.py::test_TC_3118_scope_keys_and_no_project` (TC-3118, increment 004), app pilot at 118x30.
- **Numeric pass threshold:** the modal's rendered text contains `b`, `c`, `a`, `p`, `o`, `esc` (6/6); after `p` (with a selected task): the `p` line marked, modal still open; after `p` with no current project: "no project selected" shown, scope `o`; `esc`: modal gone, 0 files written.
- **Negative control:** reusing `present_project_id` makes the no-project arm pick the first project — red.
- **Boundary catalog:** ☑ empty (no current project) ☑ boundary (`p` then `o`) ☐ invalid (N/A — unbound keys do nothing) ☐ error (N/A)

### LLR-3107.3 — collecting the loaded boards and writing the files
- **Traceability:** HLR-3107, HLR-3101
- **Ledger:** none
- **Statement:** The action shall collect the boards from `app.board_lanes(app)` (`taskboard/app.py:841`), skipping a lane whose board is `None` and counting it; it shall call `report_html.write_reports(d, kinds, folder, today)` (NEW), which writes `workspace-<date>.html` and/or `deck-<date>.html` in `Path(app.board.path).parent / "reports"` (created when missing), with scope `p` inserting the project slug by `report_path`'s rule (`workspace-<slug>-<date>.html`); a same-day export overwrites; nothing else is written. Source: `taskboard/app.py`, `taskboard/report_html.py`. Touched symbols: `app.TaskboardApp.action_report_export` NEW, `report_html.write_reports` NEW, `report_html.report_name` NEW; consumes `app.board_lanes` unchanged.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_export_app.py::test_TC_3119_files_land_beside_the_open_board` (TC-3119, increment 004) with a registry of the three fixture boards, one of them missing.
- **Numeric pass threshold:** `a` writes exactly 2 files (names as above); `p` on project `Client A`'s task → `workspace-client-a-<date>.html`; a second export the same day → still 2 files; the missing board counted 1 in the toast; 0 board files changed (bytes).
- **Negative control:** a mutation writing beside the CWD instead of the open board's folder makes the path arm red.
- **Boundary catalog:** ☑ error (a missing board file) ☑ boundary (same-day re-export) ☑ empty (registry of one board) ☐ invalid (N/A)

### LLR-3107.4 — the toast and the `o` offer
- **Traceability:** HLR-3107
- **Ledger:** none
- **Statement:** After writing, the app shall `notify` with `title="Report"`, `severity="information"`, `timeout=10`, `markup=False` the text `Report written: <name> to <dir> — o opens it` (both names joined by ` and ` for `a`; ` · <n> board(s) skipped` appended when lanes were skipped); while that offer is live (10 s from the notify), `o` shall open the just-written file (the workspace for `a`) with `os.startfile(path)` on Windows, else `webbrowser.open(path.as_uri())`, and only a path the app itself wrote in this export; after the offer expires, `o` shall act as `open_url` (`taskboard/app.py:3526`). Source: `taskboard/app.py`. Touched symbols: `app.TaskboardApp.action_open_url` (the offer branch), the export's offer state NEW.
- **Validation:** `test (integration)`
- **Executed verification:** `tests/test_report_export_app.py::test_TC_3120_o_opens_the_report_while_the_toast_lives` (TC-3120, increment 004): `os.startfile`/`webbrowser.open` replaced by recorders, the clock advanced past 10 s.
- **Numeric pass threshold:** toast text equal to the template (1 notification); `o` at t < 10 s → 1 open call with the written path, 0 `webbrowser.open` of task URLs; `o` at t > 10 s → 0 open calls of the report, `open_url`'s behaviour.
- **Negative control:** a mutation never expiring the offer keeps opening the report at t > 10 s — red.
- **Boundary catalog:** ☑ boundary (t just past 10 s) ☑ empty (no selected task after expiry: `o` does nothing) ☐ invalid (N/A) ☐ error (N/A — `OSError` from the opener is swallowed like `_open_local_image`)

### LLR-3107.5 — the `x` export and the CLI report stay as they are (regression pin)
- **Traceability:** HLR-3107, HLR-3101
- **Ledger:** none
- **Statement:** No change shall reach `views.present_paths`, `views.save_present_svg`, `views.save_present_png`, `views.present_all_export`, `report.py` or `__main__`'s `--report` path. Source: none (a pin). Touched symbols: none.
- **Validation:** `inspection`
- **Executed verification:** `git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py` at each increment's packet §2; the present and report suites re-run at P4 (TC-3121, an inspection row of increment 004's packet).
- **Numeric pass threshold:** the diff is 0 lines; the suites 0 failed.
- **Negative control:** none — an inspection pin, not a gate (C-40's corollary).
- **Boundary catalog:** none — no input surface.

### Information Flow Contract (IFC) — C-54

- **Part A — flows:**

```
FLOW: report-export
  SOURCE : the loaded boards (the open board as the app holds it; the other active registry boards via peek_board), people.json and marks.json — file-derived, untrusted text
  NODES  :
    - fn    : keymap.KEYMAP row H -> app.TaskboardApp.action_report_export (NEW)
      owner : LLR-3107.1
      in    : the H key press on the main screen
      out   : the ReportExport modal pushed
    - fn    : modals.ReportExport (NEW)
      owner : LLR-3107.2
      in    : the keys b c a p o esc, the current project
      out   : (kinds, scope) or None
    - fn    : app.board_lanes (taskboard/app.py:841) via action_report_export
      owner : LLR-3107.3
      in    : the registry, the open board
      out   : the readable boards, the skipped count
    - fn    : report_html.extract (NEW)
      owner : LLR-3101.1
      in    : boards, people, marks, today
      out   : the dict (JSON-able facts)
    - fn    : report_html.extract (NEW) — the scope filter
      owner : LLR-3101.3
      in    : the dict's facts + project key or None
      out   : the dict in scope
    - fn    : report_html.extract (NEW) — due words via report._due_word
      owner : LLR-3101.2
      in    : each task's due distance, the project's closed flag
      out   : due_word strings
    - fn    : report_html.notes_html (NEW)
      owner : LLR-3106.1
      in    : raw notes text, the people directory
      out   : notes HTML from escaped segments only
    - fn    : report_workspace.render (NEW)
      owner : LLR-3102.1
      in    : the dict
      out   : the workspace page (control bar, sections, embedded JSON)
    - fn    : report_html.embed_json (NEW)
      owner : LLR-3106.1
      in    : the dict
      out   : script-safe JSON text (< > & as \u003c \u003e \u0026)
    - fn    : report_deck.render (NEW)
      owner : LLR-3105.1
      in    : the dict
      out   : the deck page (cover, overview, one slide per project)
    - fn    : report_html.write_reports (NEW)
      owner : LLR-3107.3
      in    : the rendered pages, kinds, the folder, today, the scope slug
      out   : reports/workspace-<date>.html and/or reports/deck-<date>.html
    - fn    : app.TaskboardApp.notify (the export toast)
      owner : LLR-3107.4
      in    : the written names, the folder, the skipped count
      out   : the toast and a live 10 s open offer
    - fn    : app.TaskboardApp.action_open_url (the offer branch)
      owner : LLR-3107.4
      in    : o while the offer is live
      out   : os.startfile(path) / webbrowser.open(path.as_uri())
  SINK   : the files <board dir>/reports/workspace-<date>.html and deck-<date>.html; the toast; the OS default handler
```

```
FLOW: workspace-view
  SOURCE : the workspace file's embedded JSON (#board-data) and location.hash — the hash is untrusted input
  NODES  :
    - fn    : parseHash (report_workspace page JS, NEW)
      owner : LLR-3102.3
      in    : location.hash
      out   : a view state with whitelisted values only
    - fn    : applyFilters (report_workspace page JS, NEW)
      owner : LLR-3102.2
      in    : the view state, the embedded tasks, meta.today
      out   : the kept task set
    - fn    : the control bar and sections renderers (report_workspace page JS, NEW)
      owner : LLR-3102.1
      in    : the view state, the kept set
      out   : the controls' states, the count, the gantt/table/notes/milestones via textContent
    - fn    : writeHash (report_workspace page JS, NEW)
      owner : LLR-3102.3
      in    : the view state
      out   : location.hash
    - fn    : the print stylesheet and window.print (report_workspace page, NEW)
      owner : LLR-3104.1
      in    : the rendered view, print media
      out   : the printed page with the view header and no controls
    - fn    : downloadView (report_workspace page JS, NEW) — reduce
      owner : LLR-3103.1
      in    : the kept set, the embedded data, the sections state
      out   : the reduced, script-safe JSON
    - fn    : downloadView (report_workspace page JS, NEW) — shell and meta.view
      owner : LLR-3103.2
      in    : the pristine shell captured at load, the reduced JSON, the view state
      out   : the file workspace-view-<date>.html
  SINK   : the browser's view; the printed page or PDF; the downloaded file workspace-view-<date>.html
```

```
FLOW: deck-paging
  SOURCE : the deck file's slides and the recipient's key presses
  NODES  :
    - fn    : the paging handler (report_deck page JS, NEW)
      owner : LLR-3105.2
      in    : ArrowLeft/Right, PageUp/Down, Home/End outside text fields
      out   : the shown slide and the n / N counter
  SINK   : the browser's view; one slide per printed page
```

- **Part B — boundary decomposition:** no — each report is one self-contained file a consumer opens whole in a browser; nothing outside the file addresses a component of it. The two addresses inside it — the hash grammar (`v=1`) and the embedded data element — are read only by the same file's own code (and by a re-opened downloaded view, which is the same code), and are contracted by LLR-3102.3 and LLR-3106.1 with a version key, not by consumer lists.

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer A: TC-3101..TC-3121 (unit arms over `extract`, `embed_json`, `notes_html`, the renderers'
output; headless e2e arms over the pages' controls; app-pilot arms over the modal, files, toast
and `o`; inspection pins). Layer B: AT-3101..AT-3107, one on-disk node each:

| AT | Commission | Node (planned) | Increment |
|---|---|---|---|
| AT-3101 | AT-a | `tests/test_report_export_app.py::test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it` (also loads the file headless: 0 console errors, 0 external requests) | 004 |
| AT-3102 | AT-b | `tests/test_report_workspace.py::test_AT_3102_filters_and_the_hash_round_trip` | 001 |
| AT-3103 | AT-c | `tests/test_report_workspace.py::test_AT_3103_download_this_view_holds_only_the_filtered_tasks` | 002 |
| AT-3104 | AT-d | `tests/test_report_workspace.py::test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` | 002 |
| AT-3105 | AT-e | `tests/test_report_export_app.py::test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project` | 004 |
| AT-3106 | AT-f | `tests/test_report_deck.py::test_AT_3106_board_text_is_escaped_in_both_reports` | 003 |
| AT-3107 | AT-g | `tests/test_modal_keys.py::test_AT_3107_the_report_modal_obeys_the_modal_key_law` | 004 |

Browser nodes open with `pytest.importorskip("playwright.sync_api")`: they run on this Windows
machine and skip where Playwright is absent (CI — declared, §6.3). The fixture
`tests/report_fixture.py` (NEW, increment 001) is synthetic: three boards Personal / Client A /
Course, people Ana Ruiz / Luis Prado / Carmen Vega, classes Delivery / Billing / Launch, TODAY
2026-10-29, a hostile title `<script>alert(1)</script>`, a hostile note and person name, a
cross-project dependency, an archived task and an archived project.

### 5.2 Batch acceptance criteria
- 100% of LLRs covered by at least one executed verification with a pass result.
- Every AT-3101..AT-3107 node passes on this machine, observing the outcome through the app's keys or the written files, with its boundary arms and a recorded mutation kill (C-40).
- The P4 full suite, 3 sequential chunks: 3281 + the new-node count passed, the only skip TC-1902 (and, where Playwright is absent, the declared browser skips), 0 failed.
- `tests/test_report.py` 18 passed; `git diff 9da7438 -- taskboard/report.py` empty.
- No requirement without an assigned validation method.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
- See §1.3.

### 6.2 Relevant design decisions
- HR-1 (LLR-3101.1..3, LLR-3107.5); HR-2 (LLR-3107.1..4); HR-3 (LLR-3102.1..3); HR-4 (LLR-3103.1..2, LLR-3104.1); HR-5 (LLR-3105.1..2); HR-6 (LLR-3106.1..2). The PDR (`PDR-2026-10-29-batch-01`) carries the design decisions the code takes.

### 6.3 Open risks

**Security — family C (C4, C6, C8 fired; C1–C3, C5, C7 not).** The scan
(`evidence/scan-p1.txt`) is answered flag by flag in the last bullet; each control is a
requirement, not an open risk.

- **C8 — HTML rendering of file-derived board text.** Control: LLR-3106.1 — server-side `report._e` on every board string, client-side `textContent` only, notes HTML from escaped `highlight_segments`/`split_mentions` pieces in constant tags (probe 4 shows the raw pieces carry live markup), and the embedded JSON with `<`, `>`, `&` as `\u003c`, `\u003e`, `\u0026` so `</script>` in board text cannot close the data element (the prototype's `</`-only replace is the negative control). Hostile ATs: AT-3106 (title, note, person name; 0 dialogs; literal text), TC-3115.
- **C6 — the URL hash is an input surface.** Control: LLR-3102.3 — every hash value parsed against a whitelist drawn from the embedded data or a constant set; `q` only ever a `value`; unknown dropped; no hash value reaches `innerHTML`, a selector or a non-`value` attribute. Hostile arm: TC-3107.
- **C4 — the filtered download exists to keep hidden data from a recipient.** Control: LLR-3103.1 — the downloaded JSON rebuilt from the kept tasks only, every directory reduced, dangling dependencies removed, notes stripped when the notes section is off; the UI states that only the download leaves hidden data out and that the print does not (LLR-3103.2, HLR-3104). Assertion on the bytes, both raw and JSON-escaped forms: AT-3103, TC-3109. Residual: the print path deliberately keeps all data in the file — stated on the control, not a defect.
- **Opening a file from the app.** `o` opens only the path the export just wrote (LLR-3107.4), the same OS call the app's image opener already gates (`taskboard/app.py:3565`); no user-supplied path reaches it.
- **Not fired, with reason:** no authentication, secret, external integration, database or network service is touched; the reports make 0 requests (LLR-3106.2); task URLs are inert links.
- **Test-harness risk:** Playwright is not a declared dependency; CI skips the browser nodes, so CI cannot see AT-3102..AT-3104, AT-3106 and the browser arms of AT-3101/AT-3105. Their evidence is this machine's transcripts (P3, P4).
- **Scan flags** (`evidence/scan-p1.txt`: `security_required: true`, flags `token`, `role`, `hash`, `user input`, `form`, `escape`), each traced to its match: `hash` → the URL hash, the genuine C6 input surface, answered by LLR-3102.3 (bullet C6 above); `escape` → the genuine C8 control, LLR-3106.1 (bullet C8); `user input` → HLR-3101's boundary catalog ("not parsed from user input") — the dict has no parsed input; the untrusted inputs are board text (C8) and the hash (C6), both answered; `token` → the template preamble's "reserved token" and §3's "the token `V2` resolves" (an id-matching word, no credential exists); `role` → §2.3 "No other role" (no authorization surface exists or changes); `form` → prose ("the prototype's … form", "Information Flow"), no HTML form posts anything — the reports submit nothing anywhere.

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-29-batch-01

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.part2.md` in the guide directory init prints), and nothing
above this line is ever edited._
```

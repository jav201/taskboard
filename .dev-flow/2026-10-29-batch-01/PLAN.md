# PLAN — taskboard — Batch 2026-10-29-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-29-batch-01 |
| Objective | the app exports two HTML reports from ONE data extraction of every loaded board: variant B, the interactive workspace (gantt, table, notes, HR-3 controls with URL-hash state, HR-4 export of the configured view as print-to-PDF and as a filtered self-contained download), and variant C, the concise vector deck (one slide per chosen project); a global H modal (b/c/a, p/o scope, esc) writes them to <board dir>/reports/ and a toast offers o to open (HR-1..HR-6) |
| Last updated | P4 · 2026-10-29 |
| Standing authorization | The operator, 2026-10-29, on `prototypes/html_report/html-report-round.html`: the verdict block quoted verbatim in `.dev-flow/COMMISSION-html-report.md` («Variante B: ELEGIDA · Variante C: ELEGIDA · Recomendación general (B, H global, todos los boards, convive con SVG): no confirmada (no objection)» and the note «…mejoraras los controles para el display y filtro de información y de proyectos… una opción dentro del mismo reporte para exportar la vista… a PDF…»), then «decide cómo continuar, con opus o sonnet»; the orchestrator's task: gates close under it, «Do NOT push or merge». Read from the commission and the task: autonomy over the gates the commission names (P0..P5, ARQ, PDR, DDR); merge/push NOT granted; a HIGH finding blocks regardless and returns to the operator. |
| First gate | start run (`evidence/gate-start.txt`, over the closed 2026-10-26-batch-01 record): exit 1 · 38 block, ALL `V59` — the closed batch's stale `base_ref` `f4b53cc` charged against the prototype commits; cleared by the rollover's re-stamp (`base_ref` = HEAD `9da7438`), the same remedy as 2026-10-26-batch-01's P0. After rollover (`evidence/gate-p0-rollover.txt`): exit 0 · 0 block / 182 notice / 47 n/a · `V7`: bundle identical to the manifest it ships, both directions (57 declared files unmoved, 0 undeclared) at `2026-10-12-rev102` · `V25`: origin answered (5 refs, newest 2.83 days old) · `V30` half (3.12.7 witnessed; 3 derived floors not derivable from a bundle) |
| Premises / RC-1 | `origin/main` verified at `9cc7d4e` (`9cc7d4e20db24dbe928a2b95045a8ef120ccedd1`, 2026-10-26 11:59 -0600) = the merge-base of HEAD; RC-1(a): HEAD `9da7438` is strictly ahead (7 commits ahead, 0 behind) — no rebase; RC-1(b): the story is NOT already shipped — `git show origin/main:taskboard/keymap.py \| grep -n 'Key("H"'` exits 1 (no `H` seat) and `git ls-tree origin/main taskboard/` lists no `report_html.py`, `report_workspace.py` or `report_deck.py` (only `report.py`); RC-2: `git ls-remote --exit-code --heads origin` exit 0, 5 heads, newest `origin/main` 2026-10-26 (`evidence/rc-p0.txt`). Premises: the design is the prototype round (B, C); the CLI report stays (HR-1); synthetic data only; tests drive the app by keys and the pages in headless Chromium. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | fired | judged — new modules `taskboard/report_html.py`, `taskboard/report_workspace.py`, `taskboard/report_deck.py` |
| A2 | fired | judged — the touch set spans `report_html`, `report_workspace`, `report_deck`, `app`, `modals`, `keymap` (6 layers ≥ 2) |
| A3 | not fired | judged — no existing interface changes; the new modules consume `views.HEX`/`highlight_segments`/`lanes_of`/`sitting`, `people.split_mentions`/`mention_ids`, `models.parse_iso`/`days_in_phase`, `report._due_word` unchanged |
| A4 | not fired | judged — increments run in order 001→004 |
| B1 | fired | `grep -rl KEYMAP tests/` → test_app, test_archive, test_boards_home, test_dependencies, test_help_keys, test_kanban_priority, test_keymap, test_legend, test_links, test_link_picker, test_marks_manager, test_momentum, test_people_view, test_readme, test_report; `INVENTORY` → test_modal_keys; `open_url` → test_app, test_keymap; `build_report` → test_report — reverse census at P2/P3 |
| B2 | not fired | judged — no file moves |
| B3 | not fired | probe — `tests/goldens/` does not exist |
| B4 | fired | judged — the "Download this view" file is produced by the workspace page and consumed by the same page code when the recipient opens it → output-then-consume AT (AT-3103 re-opens the downloaded file headless) |
| C1, C2, C3, C5, C7 | not fired | judged — no auth, secrets, external integration, DB or network service; the reports make 0 external requests |
| C4 | fired | judged — the filtered download exists to keep hidden board data from recipients (a data-exposure control) |
| C6 | fired | judged — the page parses the URL hash (an input surface) |
| C8 | fired | judged — HTML rendering of file-derived board text (titles, notes, names) |
| D1 | fired | judged — a new key, a modal, a toast and two user-facing documents |
| D2 | not fired | judged — the prototype is Python generating HTML, the same tech as the target |
| E1 | fired | judged — 4 increments |
| E2, E3 | not fired | judged — no high-risk or client/regulated context |
| F1 | not fired | bundle runtime — the `V7` line stands as the probe (bundle identical to its manifest at `2026-10-12-rev102`) |
| F2 | not fired | `.dev-flow/BACKLOG.md` carries «Last refresh: 2026-10-26 (2026-10-26-batch-01 close)» = the last close |
| ARQ · PDR · DDR | taken up | A1/A2 fired → `devflow-init.py` took ARQ, PDR and DDR into `stations_active` |

## Where we are

DDR approved, 2026-10-29 (`design/DDR-2026-10-29-batch-01.md`, re-sealed after increment 005): qa-reviewer and ux-reviewer had found that the print view clipped the task table (DQ1/DU2/O1) and named hidden boards and counted hidden projects (DQ2/DU1/O2), both high, plus low findings DQ3-DQ5, DU3-DU5. Correction increment 005 (commit `7b47714`, packet `03-increments/increment-005.md`, `LED-2026-10-29-batch-01.27` on LLR-3104.1, LLR-3103.2, LLR-3107.4) discharges condition C-DDR-1: 68 passed (`evidence/suite-005.txt`), 15/15 mutants killed (`evidence/mutation-005.txt`), code-reviewer OK to advance (LOW only; the post-review print-wrap fix was not re-read, declared); the re-shot `workspace-print-preview.png` shows `Boards in this view (1): Client A` and every table column. Station moved to P4 (in-progress). Owed next: the full suite in 3 sequential chunks, the package-scanning law suites, and the validation record `04-validation.md` (naming the TC-3121 inspection pin, DQ6).

PDR approved with conditions, 2026-10-29 (`design/PDR-2026-10-29-batch-01.md`): the architect, qa-reviewer and ux-reviewer lenses each returned `approved with conditions` (PA1–PA7, PQ1–PQ12, PU1–PU7). The orchestrator's dispositions C1–C14 are folded as ONE ledger entry, `LED-2026-10-29-batch-01.22` (PDR conditions), into the contract (nine LLRs), `docs/ARCHITECTURE.md` (§3, §4) and the design proposal (§3.1, §3.2, §4); the open item P-1 is closed. The increment-owned conditions pass to the increments: 001 (PA3 code, PA4, PA5, PA7, PQ2, PQ4–PQ8, PQ10, PQ11, C10–C12), 002 (PQ1/C13, PQ3/C14, C6, C7, PA2 verification), 003 (PQ9, Q11), 004 (C8, C9, the PU3 operator question). The ux-reviewer's seven observable criteria are the DDR's checklist. Station moved to P3 (in-progress). Owed next: P3 increment 001 (`taskboard/report_html.py`, `taskboard/report_workspace.py`, the fixture and the first tests). **Update, P3 increment 001 done (code `31eddb2`, packet `03-increments/increment-001.md`):** `report_html.py` (the one extraction) and `report_workspace.py` (variant B with the HR-3 controls and the hash) are written; 44 passed (`evidence/suite-001.txt`), 35/35 mutants killed (`evidence/mutation-001.txt`), the package-scanning law suites 298 passed (`evidence/laws-001.txt`); code-reviewer OK to advance (2 MEDIUM: CR1 resolved by `LED-2026-10-29-batch-01.23`, CR2 fixed), security-reviewer PASS (S1 executed-verified; SI1 carried to 003). CR5 (the Inbox key collision) is declared and in `BACKLOG.md`. Owed next: increment 002 (`taskboard/report_workspace.py`: the print view and the filtered download). **Update, P3 increment 002 done (code `613702e`, packet `03-increments/increment-002.md`):** `report_workspace.py` now exports the configured view — the print view (`@page { margin: 0 }`, controls hidden, kept-task counts, the printed date by one function) and "Download this view" (the pristine shell with `#board-data` replaced by the reduced, escaped data; CSV/JSON on visible rows with the formula guard); 52 passed (`evidence/suite-002.txt`), 40/40 mutants killed (`evidence/mutation-002.txt`); code-reviewer PASS after a re-read on `613702e` (CR2-1 MEDIUM, CR2-2 and CR2-3 LOW applied), security-reviewer PASS (SD1 fixed and recorded as `LED-2026-10-29-batch-01.24`; SD2 accepted as a risk). Owed next: increment 003 (`taskboard/report_deck.py`). **Update, P3 increment 003 done (code `f7eb6d7`, packet `03-increments/increment-003.md`):** `report_deck.py` (variant C, the deck from the one dict: cover, overview, a slide per project, paging keys, one slide per printed page, 390 px layout) and a value change in `report_html.py` (finished work is never late; the frozen dict shape is unchanged, so the PDR stays closed); 58 passed (`evidence/suite-003.txt`), 37/37 mutants killed (`evidence/mutation-003.txt`); code-reviewer OK to advance (CR3-2, CR3-3 fixed; CR3-4, CR3-5 in `BACKLOG.md`), security-reviewer PASS (S1 verified both sides, SI1 and SC1 discharged); requirement amendment `LED-2026-10-29-batch-01.25`. Owed next: the next P3 increment (increment 004, the app wiring). **Update, P3 increment 004 done (code `e8ec477`, packet `03-increments/increment-004.md`):** the `H` key, the `ReportExport` modal, the toast and the `o` offer reach `write_reports` from the app (`keymap.py`, `modals.py`, `app.py`; README `H` row); 314 passed (`evidence/suite-004.txt`), 27/27 mutants killed (`evidence/mutation-004.txt`); code-reviewer OK to advance (CR4-2 MEDIUM resolved with a test and a mutant, CR4-1 and CR4-3 LOW fixed, CR4-4 watch item in `BACKLOG.md`), security-reviewer PASS (SA1 README warning); the failure toasts and the singular skipped count are `LED-2026-10-29-batch-01.26`. All AT-3101..AT-3107 nodes exist; **P3 closes and the DDR is next.**

## Objective

Export, from the app, two HTML reports of every loaded board built from one extraction — B, the workspace with clear filter/display controls whose view lives in the URL hash and can be printed or downloaded as a file holding only the configured view; C, the concise deck with one slide per chosen project — through a global `H` modal, with a toast that offers `o` to open the file (HR-1..HR-6).

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-3101 | READY | INVEST ✓ on six axes; DoR passed; the sole story |
| P0 | approved | gate 0 block (`evidence/gate-p0.txt`); batch opened `cb76bee` |
| ARQ | approved | module map amended (3 new layers, 6 interfaces, 4 rationale rows, §6 worksheet); tree check: map current (`evidence/arq-map-check.txt`); gate 0 block (`evidence/gate-arq.txt`) |
| P1 | approved (iteration 1) | the amendment D1–D20 folded (LED-2026-10-29-batch-01.1 … .20); 19 LLRs (new LLR-3103.3); TC-3101..3125; was: contract US-3101, HLR-3101..3107, 18 LLRs, AT-3101..3107, TC-3101..3121, 3 FLOW blocks; scan answered (§6.3); gate 0 block (`evidence/gate-p1.txt`) |
| P2 | approved (round 2) | `evidence/gate-p2.txt`; round 1 iterate-to-refine (D1–D20), round 2 approve (R1–R7 → LED .21) |
| PDR | approved with conditions | `design/PDR-2026-10-29-batch-01.md` sealed 2026-10-29; architect, qa-reviewer, ux-reviewer; C1–C14 discharged at the contract by `LED-2026-10-29-batch-01.22`; the increment-owned conditions pass to 001–004 |
| P3 | approved | increments 001–004 done and gated (`31eddb2`, `613702e`, `f7eb6d7`, `e8ec477`); 314 passed, every AT node on disk; correction increment 005 (`7b47714`, LED .27) discharges the DDR condition: 68 passed, 15/15 mutants |
| DDR | approved | `design/DDR-2026-10-29-batch-01.md` re-sealed: C-DDR-1 discharged by increment 005 (DQ1, DQ2 with arms and mutants; DQ3-DQ5, DU3-DU5) |
| P4 | in-progress | the full suite in 3 chunks, the law suites, `04-validation.md` |
| P5 | pending | — |

## Roadmap + increment plan

| # | Content | SOURCE files | ATs / TCs |
|---|---|---|---|
| 001 | `taskboard/report_html.py` (extract, notes HTML, embed_json, names, `write_reports`) + `taskboard/report_workspace.py` (B with the HR-3 controls, the hash, the print fix); tests `tests/report_fixture.py`, `tests/test_report_html.py`, `tests/test_report_workspace.py` | 2 | AT-3102; TC-3101..3108, 3115, 3123..3125 (TC-3104 moved to 001 by LED .21) |
| 002 | `taskboard/report_workspace.py` (HR-4: print view + filtered download) | 1 | AT-3103, AT-3104; TC-3109..3112, 3122 (the CSV/JSON downloads, LLR-3103.3) |
| 003 | `taskboard/report_deck.py` (+ `taskboard/report_html.py` ONLY if the frozen dict lacks a fact — a dict-shape amendment that re-opens the PDR; `write_reports` maps the `deck` kind from 001, `PDR-2026-10-29-batch-01` §3.2) | 1–2 | AT-3106; TC-3113, 3114, 3116; TC-3104 re-run |
| 004 | `taskboard/app.py` (action, collection, toast, `o` offer), `taskboard/modals.py` (`ReportExport`), `taskboard/keymap.py` (`H`); README.md (docs) | 3 | AT-3101, AT-3105, AT-3107; TC-3117..3121; `INVENTORY` row; keymap/help/readme laws re-validated |

PDR precedes P3 (architect lens + ux), DDR follows it; the full suite runs at P4 in 3 sequential chunks.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-29 | HR-1 — ONE extraction `report_html.extract(boards, people, marks, today, project=None) -> dict`; B embeds it, C renders from the SAME dict (never from Board objects). **The old CLI `taskboard --report` (`report.py`) stays as it is.** | it is a single-board, script-free, server-rendered document with its own laws in `tests/test_report.py` (read-only board, unaged, no forecast) serving the CLI and scripts, where an interactive page adds nothing; re-pointing it to B would change a shipped CLI output and its tests outside the commission's increments. The new module reuses `report._e` and `report._due_word` so the two cannot disagree on a due word. Retiring/re-pointing it is a BACKLOG item for the operator |
| 2026-10-29 | HR-2 — `H` global (free, probe 1), `bar=False`, group misc, in `?` and the palette; `ReportExport` keys only (`b` `c` `a`, scope `p`/`o` default `o`, `esc`), INVENTORY `{}`; files `<board dir>/reports/workspace-<date>.html` / `deck-<date>.html` (`p` inserts the slug); toast `Report written: … to <dir> — o opens it` (title Report, information, 10 s, markup off); `o` opens the just-written file while the toast lives (`os.startfile` / `webbrowser.open(path.as_uri())`); the `x` export untouched | the commission's HR-2 with the round's recommendation (no objection); the modal-key law |
| 2026-10-29 | HR-3 — one control bar: Projects disclosure (All/None, checkbox per project by board, colour chip), Status chips (late = open and due before today), People and Class chips (any-semantics), from/to dates (span meets range; undated only with no range), Search, Section toggles, Zoom, Reset; native focusable controls; the active-filter count; the view in a whitelisted, versioned URL hash | the operator's note on the controls; C6 |
| 2026-10-29 | HR-4 — (a) Print / Save as PDF: `@media print` hides every control, prints the view header, keeps the round's full-gantt fix (`6c1225f`), `break-inside: avoid`; label "the file still holds all data". (b) Download this view: a new self-contained HTML (the pristine shell) whose JSON holds only the kept tasks, directories reduced, dangling deps removed, notes stripped when notes are off, `meta.view` reopening the same view; label "only this file leaves the hidden data out" | the operator's note on exporting the view; C4 |
| 2026-10-29 | HR-5 — C from the same dict: cover + overview + one slide per project in scope; arrows/PageUp/PageDown/Home/End; one slide per printed page; the app's scope is its project filter | the operator's «variante C que es más concisa» |
| 2026-10-29 | HR-6 — single file, offline, 0 external requests; light + dark; no horizontal scroll at 390 px; every board string `html.escape`d (via `report._e`) or `textContent`; the embedded JSON with `<` `>` `&` as `\u003c` `\u003e` `\u0026`; notes HTML from escaped segments; English UI; synthetic data | the commission's constraints; C8 |
| 2026-10-29 | D8 (P2 round 1, S8/A5) — the export's scope default STAYS `o` (all loaded boards) and the files land where HR-2 says, `<board dir>/reports/`; declared an accepted risk with two controls: the modal prints the destination folder and the scope's board count before any key writes, and both reports' header states the scope (`All loaded boards (N): <names>` / `Project <name> on <board>`) | the round's default and the commission's HR-2 stand; the risk (every board's data beside the open board, maybe a client's folder) is made visible at the moment of writing and in the file itself; the operator may revisit it on the review page |
| 2026-10-29 | D19 (P2 round 1, A3) — ONE status rule, server-side: `extract` emits each task's `status` (archived > done > late = not done and due before today > open) and its `due_word` via `report._due_word(days)` (tasks never pass `closed`); the workspace JS and the deck read these fields and never re-derive them | two derivations (JS and the deck's Python) had already disagreed on `late` across `report.py`, `views.py` and the page; one emitter makes the two reports agree by construction (HR-1) |
| 2026-10-29 | D20 (P2 round 1, A9/Q13) — project-scope file names are `workspace-<board slug>-<project slug>-<date>.html` (same for the deck); the slug rule is the CLI report's, copied into one function `report_html.slug` and pinned against `report.report_path` (TC-3123); `docs/ARCHITECTURE.md` §4 gains the `board_lanes` consumer, the consumed `report._e`/`_due_word` and the `slug` rows; the fixture's Client A project is renamed `Storefront relaunch` | same-named projects on two boards collided in one file name; an unpinned copy of a rule drifts |
| 2026-10-29 | PDR (`design/PDR-2026-10-29-batch-01.md`) — approved with conditions: the dict admits nine facts and drops `closed`/`inbox`; `notes_text` leaves the download with `notes_html`; `write_reports` imports each renderer by a plain function-local `from . import` (no `importlib`); `project` is the key `<board key>:<project id>`; `views.HEX` is frozen; the exports carry visible captions, print loses the browser header and footer (`@page` margin 0); the `o` offer is single-use and main-screen-only; the filter count counts filter kinds; the CSV guard excepts plain numbers; print width is measured at 794 px | the PDR lenses' findings PA1–PA7, PQ1–PQ12, PU1–PU7 as ruled by the orchestrator's C1–C14; one ledger entry, `LED-2026-10-29-batch-01.22` |
| 2026-10-29 | Scribe decisions where the brief is silent (each carried into the contract, open to the P2 lenses): (1) project and task keys unique across boards = board id + id; (2) the deck's slides are the NON-archived projects in scope (the C prototype's `visible_projects(False)`); (3) action name `report_export`, key label `Report` — provisional until 004; (4) the `a` toast joins both names with ` and ` and appends ` · <n> board(s) skipped`; (5) a hash whose `v` ≠ 1 is ignored whole; `from` > `to` keeps 0 tasks; (6) "current project" never takes `present_project_id`'s first-project fallback; (7) the renderers import `report_html` at module level and `write_reports` reaches them function-locally, so 003 also touches `report_html.py` (within ≤2) — superseded at PDR: `write_reports` maps the `deck` kind from 001 by a function-local import, so 003 touches `report_html.py` only for a dict-shape amendment; (8) the download's client-side JSON is escaped like the server's; (9) increments 001–003's browser ATs produce the files through `write_reports` (the call `H` makes) and assert only through the browser; (10) the app ATs load the file headless outside the pilot's asyncio loop (thread or subprocess, decided at P3 — probe 7); (11) IFC Part B: no (one whole-file consumer); (12) the fixture adds an archived project (the deck count arm); (13) the ledger starts empty (a v1 contract) | the brief binds what it says; these are the minimal choices where it says nothing |
| 2026-10-29 | PQ6 (increment 001) — app-level (Textual `run_test`, asyncio) tests that load a written file launch Playwright inside a worker thread via `asyncio.to_thread`; no subprocess, no shared browser fixture in the export-app module | proven by `test_PQ6_spike_an_async_test_checks_the_page_in_a_worker_thread` (killed by M33); the sync API refuses to start inside a running loop (probe 7), a worker thread has none; the browser module wall time is 6.19 s (PQ7) |
| 2026-10-29 | CR1 (increment 001) — the active count reads `0 filters active`, `1 filter active`, `N filters active` | correct English; the code kept the singular and the contract was amended (`LED-2026-10-29-batch-01.23`) rather than ship "1 filters active" |
| 2026-10-29 | SD1 and CR2-1 (increment 002) — with the notes section off the download drops the mentions (unless a person filter is active, then only the pressed people's), people reduce to those referenced, and a kept project's momentum and worst are null with plain counts over the kept tasks | a withheld note's mentions named who is in it; the first re-derivation of project facts was a second client-side engine nobody reads (`LED-2026-10-29-batch-01.24`; `.scratch/p3/sec-002.md`, `.scratch/p3/cr-002.md`) |

## Risks / watch-items

- **DDR C-DDR-1 (open):** the print view clips the task table and leaks hidden board names and the hidden-project denominator ("Projects 2/6") into the PDF recipients receive · high · increment 005 discharges DQ1, DQ2 with test arms and mutants; the DDR is re-sealed afterwards. Cosmetic notices (opaque modal backdrop, faint dashed export buttons) are in BACKLOG.
- The app-level ATs need Playwright outside Textual's asyncio loop (probe 7: the sync API refuses inside a running loop) · high likelihood of a harness snag · decided at P3 (worker thread or subprocess), named in the packet.
- Playwright is not a declared dependency; CI skips every browser node · certain · declared in `01-requirements.md` §6.3; this machine's transcripts are the evidence.
- The filtered download is the batch's data-exposure control (C4): a reduction that misses one directory leaks a hidden name · medium · AT-3103 searches the bytes in raw and JSON-escaped forms; TC-3109 checks every directory.
- Board text reaches HTML in three seats (server templates, client JS, the download's JSON) (C8) · medium · LLR-3106.1 + AT-3106 + TC-3115 with a hostile fixture.
- **Accepted risk (D8):** scope `o`, the default, writes every loaded board's facts into `<board dir>/reports/` of the OPEN board, which may be a client's folder · certain when the owner exports from such a board · controls: the modal shows the destination folder and board count before writing (LLR-3107.2), both reports' header states the scope (LLR-3102.1, LLR-3105.1); the operator may revisit the default on the review page.
- Task URLs are the fourth board-text sink (S1, HIGH) · fixed in the contract by D1 (server `valid_url` filter + client `^https?://` re-check) · open until the security lens re-reads the fold at P2 round 2; AT-3106's `javascript:`/`data:` arms and TC-3124 prove it at increments 001/003.
- The live contract is past the lean budget (`V26` NOTICE, 86k chars after the D1–D20 fold) · certain · declared; narration can move to the ledger at a later fold.
- **CR5 (increment 001, declared; BACKLOG):** the Inbox key `<board index>:inbox` collides with a hand-edited project id `inbox`; the report merges the two (the board and the app are unaffected) · low · open; fix is a reserved Inbox key pinned by a fixture project with id `inbox`.
- **Accepted risk (SD2, increment 002):** the owner's search text travels verbatim in the downloaded file's `meta.view` (summary and `q`) and is printed in the file's header ("Search: ...") · low · accepted — it is the owner's own input and is visible in the header before the file is sent; the file never carries a hidden item's text except what the owner typed.
- B1: 15 test files read `KEYMAP`; a new `H` row may move a key-table law · medium · the census suites re-run in 004.

## Conventions honored

- English artefacts and commits; chat with the operator in Spanish; the review page in Spanish prose (P4).
- Synthetic data only; the `username_subject` placeholder, never the operator's real name.
- Every pytest run as `env -u NO_COLOR python -m pytest`; the import probe before any test (`evidence/import-probe.txt`).
- No push, no merge; commits by name (never `git add -A`, never `.scratch/`); each commit ends with `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.
- The flow bundle is never edited; artefacts are fixed instead.

## Out-of-scope carries

- Retiring or re-pointing the CLI report (`taskboard --report`) to the workspace — a BACKLOG item for the operator (HR-1).
- Replacing the presentation's `x` SVG/PNG export — stays (HR-2).
- Writing back to a board from a report; per-recipient files written by the app; CI installing a browser.
- The 3 known Linux CI failures — BACKLOG, not this batch (commission §Evidence).

## Gate notices and runtime absences

- **Runtime absences (named once, per `SKILL.md` §*What refuses an invocation here* step 5):** no named reviewer roles, no hooks, no prompt guard, no slash commands. Reviewer roles run as spawned generic sub-agents carrying the bundle's `agents/<role>.md`; implementation increments are authored by spawned `software-dev` sub-agents under orchestrator briefs and reviewed by different spawned agents; the batch's artefacts are written by a spawned scribe sub-agent from the orchestrator's brief. Every gate that would ask closes under the standing authorization above. Rules `not-run` from a bundle: `V15` (no canon tree), `V16` (no checkout table), `V17` (no `settings.json` hooks). `V30` runs half (witnesses 3.12.7; the three derived floors are not derivable from a bundle). dev-flow-sync: `not-run` — no export destination declared, and push/merge not granted.
- **Start gate** (`evidence/gate-start.txt`): exit 1, 38 block, all `V59` (stale `base_ref` `f4b53cc`); cleared by the rollover's re-stamp.
- **Rollover gate** (`evidence/gate-p0-rollover.txt`): exit 0 · 0 block / 182 notice / 47 n/a.
- **P4 entry gate** (`evidence/gate-p4-entry.txt`, after the `--station P4` move and this rewrite): see the exit line in that file; the DDR is re-sealed `approved` and increment 005's packet is on disk (`V9` for 005 gone with its SOURCE count).
- **DDR entry gate** (`evidence/gate-ddr-entry.txt`, after the `--station DDR` move and this rewrite): exit 0 · 0 block — the families declared below; `V2` is gone (AT-3101..AT-3107 all have a node on disk).
- **P3 increment 004 gate** (`evidence/gate-p3-004.txt`, before the `--station DDR` move): exit 0 · 0 block — the `V2` rows of AT-3101, AT-3105 and AT-3107, station-expected since the P3 entry, are cleared by increment 004's nodes.
- **PDR gate** (`evidence/gate-pdr.txt`, after the C1–C14 fold and the sealed PDR record, before the `--station P3` move): exit 0 · 0 block / 218 notice / 50 n/a — `V52` stays gone; the PDR record's section B/DDR rows are the seed's until the DDR; `V26` grew with the fold (the contract stays past the lean budget, declared below).
- **P3 entry gate** (`evidence/gate-p3-entry.txt`, after the `--station P3` move and this rewrite): exit 1 · 7 block (all `V2`: AT-3101..AT-3107 have no node on disk) / 219 notice / 49 n/a — STATION-EXPECTED at P3 entry, before any test exists; recorded, not fixed: increments 001–004 write the nodes and each increment's gate must show the corresponding `V2` rows gone, all seven at the DDR
- **PDR pre-review gate** (`evidence/gate-pdr-pre.txt`): exit 0 · 0 block / 217 notice / 50 n/a — `V52` left (the design proposal's §7 names every consumer and where it reads); `V23` down to the seeds' remaining placeholder lines (the DDR seed, the PDR §D example row, the proposal preamble's `PDR-<batch_id>#D<n>`); the rest unchanged.
- **P2 gate** (`evidence/gate-p2.txt`, round 2 approve, before the `--station PDR` move): exit 0 · 0 block / 220 notice / 49 n/a — the families below; `V26` 87,095 characters after LED .21.
- **P2 round 2 entry gate** (`evidence/gate-p1-iter2b.txt`, after the `--station P2` move and this rewrite): exit 0 · 0 block / 220 notice / 49 n/a — the same families as the iteration-1 gate; no `V62` (the plan names P2).
- **P2 round 1 gate** (`evidence/gate-p2-r1.txt`, before the send-back): exit 0 · 0 block / 216 notice / 49 n/a — the families below, unchanged.
- **P1 iteration-1 scan** (`evidence/scan-p1-iter2.txt`): exit 1, `security_required: true`, the same 6 flags (`token`, `role`, `hash`, `user input`, `form`, `escape`) and 5/5 control rows `ok`; the §6.3 answers stand, and §6.3 now also names the URL sink (D1), the accepted `o` risk (D8) and the opener's ground (D9).
- **P1 iteration-1 gate** (`evidence/gate-p1-iter2.txt`): exit 0 · 0 block / 220 notice / 49 n/a — `V53` grew to 37 lines (the new nodes TC-3122..TC-3125); `V26` 85,988 characters; the other families unchanged.
- **P1 gate** (`evidence/gate-p1.txt`): exit 0 · 0 block / 216 notice / 49 n/a — the same families as the ARQ gate, each declared below; `V53` carries the 32 planned-node mention lines of the contract (expected at steps 7–9); 0 `V33`/`V34`/`V35`/`V45`/`V46` findings on this contract (every `Negative control`, `Boundary catalog`, `Acceptance test(s)`, `Premise evaluation`, `Fork preconditions` filled); `V26` the declared budget NOTICE.
- **P1 scan** (`evidence/scan-p1.txt`): exit 1, `security_required: true`, flags `token`, `role`, `hash`, `user input`, `form`, `escape` — every flag traced to its match and answered in `01-requirements.md` §6.3 (`hash` → LLR-3102.3, C6; `escape` → LLR-3106.1, C8; the C4 control is LLR-3103.1; `token`, `role`, `form`, `user input` are prose matches); the scanner's 5 control rows all `ok`.
- **ARQ gate** (`evidence/gate-arq.txt`): exit 0 · 0 block / 216 notice / 49 n/a — `V27` left with the P0 decision; the rest are the families declared below, unchanged.
- **P0 gate** (`evidence/gate-p0.txt`): exit 0 · 0 block / 217 notice / 48 n/a — every NOTICE family declared in the table below; `V25` not raised (origin answered); the closed batch's `decisions-log.json` and the rollover land in the batch-open commit.

**NOTICE families, declared** (each printed by the gate; why it stands; when it leaves):

| Family | Why it stands | Leaves |
|---|---|---|
| `V9` | `increment-001.md` is the seed (no SOURCE count yet); the rest are closed batches' packets | 001's packet |
| `V13` | IFC `COMPONENT` addresses of closed batches reached by undeclared files (sealed records); this contract has no Part B | never in this batch (sealed) |
| `V22` | closed batches' LLRs never used as owners; here LLR-3106.2 (a constraint: offline, themes, width) and LLR-3107.5 (a regression pin) own no transform by design | stays (a question, never a gate) |
| `V23` | design-review citations in closed records that do not parse, and the seeded `design/` templates' placeholder ids (6 lines in `design/*.md`) | the seeds' lines at PDR/DDR; the closed ones stay |
| `V26` | the live contract is past the lean budget (`_LEAN_MAX_CHARS`) — 7 HLRs and 19 LLRs over three new modules and three touched ones, each LLR carrying its census symbols and nodes, grown by the D1–D20 fold | a later fold may move narration into the ledger |
| `V27` | no dated `decisions_log` entry yet (P0 gate only) | left with the P0 `--decision` (2026-10-29) |
| `V30` | the gate runs from a bundle | never (every gate) |
| `V31`, `V32`, `V36`, `V37`, `V38`, `V41`, `V43`, `V44` | `increment-001.md` seed fields hold their placeholders | 001's packet |
| `V42` | deferral markers in closed records too short to key or outside a lane (sealed); the batch record untracked until the P0 commit | the step-3 one with the P0 commit; the closed ones stay |
| `V47`, `V48`, `V49` | `04-validation.md` seed placeholders | P4 |
| `V50`, `V51`, `V54` | `05-close.md` seed placeholders | P5 |
| `V52` | `design/design-proposal.md` §7 still the template | left at PDR (`evidence/gate-pdr-pre.txt`) |
| `V53` | this contract names 29 planned test nodes (7 AT, 22 TC) — one line per mention — in `tests/test_report_html.py`, `tests/test_report_workspace.py`, `tests/test_report_deck.py`, `tests/test_report_export_app.py` and `tests/test_modal_keys.py` that Phase 3 has not written; plus the closed-record census line | each node's increment |

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q` (from the worktree root) | 2026-10-29 | 1 passed — `taskboard.__file__ = C:\Users\jjgh8\Github\taskboard-wt\report-proto\taskboard\__init__.py`, inside the worktree (`evidence/import-probe.txt`) |
| `env -u NO_COLOR python -m pytest -q tests/test_report.py` (P1 probe 6, the CLI report's pin) | 2026-10-29 | 18 passed (`evidence/p1-probes.txt`) |
| `TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_html.py tests/test_report_workspace.py tests/test_report.py` (increment 001) | 2026-10-29 | 44 passed — 12 + 14 new nodes + the 18 of `test_report.py` (`evidence/suite-001.txt`); browser module wall 6.19 s |
| `python .dev-flow/2026-10-29-batch-01/evidence/mutation-001.py` (increment 001) | 2026-10-29 | 35/35 mutants KILLED (`evidence/mutation-001.txt`) |
| the package-scanning law suites: `test_english`, `test_hygiene`, `test_markup_census`, `test_markup_sites`, `test_privacy_sweep`, `test_control_bytes` (increment 001) | 2026-10-29 | 298 passed in 107.77 s (`evidence/laws-001.txt`) |
| `TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_html.py tests/test_report_workspace.py tests/test_report.py` (increment 002) | 2026-10-29 | 52 passed — 44 + 8 new nodes (AT-3103, AT-3104, TC-3109, TC-3110, TC-3111 x2, TC-3112, TC-3122) (`evidence/suite-002.txt`) |
| `python .dev-flow/2026-10-29-batch-01/evidence/mutation-002.py` (increment 002) | 2026-10-29 | 40/40 mutants KILLED (`evidence/mutation-002.txt`) |
| `TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q tests/test_report_deck.py tests/test_report_workspace.py tests/test_report_html.py tests/test_report.py` (increment 003) | 2026-10-29 | 58 passed — 52 + 6 new nodes (`evidence/suite-003.txt`) |
| `python .dev-flow/2026-10-29-batch-01/evidence/mutation-003.py` (increment 003) | 2026-10-29 | 37/37 mutants KILLED (`evidence/mutation-003.txt`) |
| `TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q` over `tests/test_report_export_app.py`, `test_modal_keys`, `test_keymap`, `test_help_keys`, `test_readme`, `test_app`, `test_report`, `test_report_html`, `test_report_workspace`, `test_report_deck` (increment 004) | 2026-10-29 | 314 passed — 306 + 8 new nodes (`evidence/suite-004.txt`); TC-3121 diff 0 lines |
| `python .dev-flow/2026-10-29-batch-01/evidence/mutation-004.py` (increment 004) | 2026-10-29 | 27/27 mutants KILLED (`evidence/mutation-004.txt`) |
| `TASKBOARD_REQUIRE_BROWSER=1 env -u NO_COLOR python -m pytest -q` over `tests/test_report_export_app.py`, `test_report`, `test_report_html`, `test_report_workspace`, `test_report_deck` (increment 005, the DDR corrections) | 2026-10-29 | 68 passed — 65 + 3 new nodes; plus `test_modal_keys.py::test_AT_3107_…` 1 passed (`evidence/suite-005.txt`) |
| `python .dev-flow/2026-10-29-batch-01/evidence/mutation-005.py` (increment 005) | 2026-10-29 | 15/15 mutants KILLED (`evidence/mutation-005.txt`) |

## Decision log (human-readable mirror of `state.json`)

| Station | Date | Decision |
|---|---|---|
| P0 | 2026-10-29 | P0 intake approved under the batch's standing authorization — the operator's verdict (B and C chosen, the round's recommendation not objected) and «decide cómo continuar, con opus o sonnet», quoted in the commission; rollover re-stamped `base_ref` 9da7438 (the start gate's 38 `V59` blocks cleared); RC-1(a) no rebase, RC-1(b) not shipped, RC-2 origin answered; triggers A1 A2 B1 B4 C4 C6 C8 D1 E1 fired (ARQ, PDR, DDR taken up); US-3101 READY; gate 0 block; batch opened in `cb76bee`. ARQ next. |
| ARQ | 2026-10-29 | ARQ module map approved under the batch's standing authorization — three new layers (`report_html`, `report_workspace`, `report_deck`), their dependency bans and import direction, six interface rows, four rationale rows, a one-lane serial worksheet; the tree check: map current (`evidence/arq-map-check.txt`); gate 0 block; the architect lens reads the map again at P2. P1 next. |
| P1 | 2026-10-29 | P1 requirements approved under the batch's standing authorization — US-3101; HLR-3101..3107; 18 LLRs with source module, C-26 symbols and TC node; AT-3101..3107 (one planned black-box node each); 9 premises TRUE; one lane; three FLOW blocks; the scan's 6 flags answered with the C4/C6/C8 controls; gate 0 block (`V26`, `V53` declared). P2 review is next. |
| P2 | 2026-10-29 | P2 round 1: iterate-to-refine — architect, qa-reviewer and security-reviewer lenses (S1 HIGH: task URL schemes); dispositions D1–D20 fold into the contract by amendment; P1 is next (`--iterate-to P1`, iteration 1). |
| PDR | 2026-10-29 | PDR approved with conditions under the batch's standing authorization — architect, qa-reviewer, ux-reviewer; LED .22 discharges the PDR-close conditions C1–C14 at the contract; the increment-owned conditions pass to increments 001–004; P3 is next. |
| P1 | 2026-10-29 | P1 amendment approved under the batch's standing authorization — D1–D20 folded as `LED-2026-10-29-batch-01.1` … `.20`; new LLR-3103.3; new TC-3122..TC-3125; scan re-run, gate 0 block. P2 round 2 is next. |
| P2 | 2026-10-29 | P2 approved under the batch's standing authorization — round 2: architect, qa-reviewer, security-reviewer approve; S1 HIGH discharged at contract level; LED .21 folds the round-2 minors (R1–R7); PDR is next. |
| P3 | 2026-10-29 | P3 increment 001 approved under the batch's standing authorization — code-reviewer OK to advance (2 MEDIUM resolved: CR1 by LED .23, CR2 fixed), security-reviewer PASS (S1 executed-verified); 44 passed, 35/35 mutants killed; P3 continues with the next increment. |
| P3 | 2026-10-29 | P3 increment 005 approved under the batch's standing authorization — the DDR correction: code-reviewer OK to advance (LOW only; post-review print-wrap fix not re-read, declared); 68 passed, 15/15 mutants killed; LED .27; DDR is next. |
| DDR | 2026-10-29 | DDR approved under the batch's standing authorization — C-DDR-1 discharged by increment 005; P4 is next. |

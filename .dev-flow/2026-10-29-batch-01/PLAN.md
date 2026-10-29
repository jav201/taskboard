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
| Last updated | P2 · 2026-10-29 |
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

P2. P1 closed under the standing authorization (gate 0 block, `evidence/gate-p1.txt`): the live contract holds US-3101, HLR-3101..HLR-3107, 18 LLRs, AT-3101..AT-3107 and TC-3101..TC-3121, three IFC `FLOW` blocks and the family-C answers; the module map was approved at ARQ. Owed next: the P2 review (`02-review.md`) — the review lenses spawned with their `agents/` role files, the architect lens re-reading the module map and the contract's census symbols, the security pass over §6.3 (C4, C6, C8) — then PDR before P3.

## Objective

Export, from the app, two HTML reports of every loaded board built from one extraction — B, the workspace with clear filter/display controls whose view lives in the URL hash and can be printed or downloaded as a file holding only the configured view; C, the concise deck with one slide per chosen project — through a global `H` modal, with a toast that offers `o` to open the file (HR-1..HR-6).

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-3101 | READY | INVEST ✓ on six axes; DoR passed; the sole story |
| P0 | approved | gate 0 block (`evidence/gate-p0.txt`); batch opened `cb76bee` |
| ARQ | approved | module map amended (3 new layers, 6 interfaces, 4 rationale rows, §6 worksheet); tree check: map current (`evidence/arq-map-check.txt`); gate 0 block (`evidence/gate-arq.txt`) |
| P1 | approved | contract: US-3101, HLR-3101..3107, 18 LLRs, AT-3101..3107, TC-3101..3121, 3 FLOW blocks; scan answered (§6.3); gate 0 block (`evidence/gate-p1.txt`) |
| P2 | in-progress | the review lenses owed (`02-review.md`) |
| PDR, P3, DDR, P4, P5 | pending | — |

## Roadmap + increment plan

| # | Content | SOURCE files | ATs / TCs |
|---|---|---|---|
| 001 | `taskboard/report_html.py` (extract, notes HTML, embed_json, names, `write_reports`) + `taskboard/report_workspace.py` (B with the HR-3 controls, the hash, the print fix); tests `tests/report_fixture.py`, `tests/test_report_html.py`, `tests/test_report_workspace.py` | 2 | AT-3102; TC-3101..3103, 3105..3108, 3115 |
| 002 | `taskboard/report_workspace.py` (HR-4: print view + filtered download) | 1 | AT-3103, AT-3104; TC-3109..3112 |
| 003 | `taskboard/report_deck.py` + `taskboard/report_html.py` (the `deck` kind of `write_reports`; any fact the deck lacks) | ≤2 | AT-3106; TC-3104, 3113, 3114, 3116 |
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
| 2026-10-29 | Scribe decisions where the brief is silent (each carried into the contract, open to the P2 lenses): (1) project and task keys unique across boards = board id + id; (2) the deck's slides are the NON-archived projects in scope (the C prototype's `visible_projects(False)`); (3) action name `report_export`, key label `Report` — provisional until 004; (4) the `a` toast joins both names with ` and ` and appends ` · <n> board(s) skipped`; (5) a hash whose `v` ≠ 1 is ignored whole; `from` > `to` keeps 0 tasks; (6) "current project" never takes `present_project_id`'s first-project fallback; (7) the renderers import `report_html` at module level and `write_reports` reaches them function-locally, so 003 also touches `report_html.py` (within ≤2); (8) the download's client-side JSON is escaped like the server's; (9) increments 001–003's browser ATs produce the files through `write_reports` (the call `H` makes) and assert only through the browser; (10) the app ATs load the file headless outside the pilot's asyncio loop (thread or subprocess, decided at P3 — probe 7); (11) IFC Part B: no (one whole-file consumer); (12) the fixture adds an archived project (the deck count arm); (13) the ledger starts empty (a v1 contract) | the brief binds what it says; these are the minimal choices where it says nothing |

## Risks / watch-items

- The app-level ATs need Playwright outside Textual's asyncio loop (probe 7: the sync API refuses inside a running loop) · high likelihood of a harness snag · decided at P3 (worker thread or subprocess), named in the packet.
- Playwright is not a declared dependency; CI skips every browser node · certain · declared in `01-requirements.md` §6.3; this machine's transcripts are the evidence.
- The filtered download is the batch's data-exposure control (C4): a reduction that misses one directory leaks a hidden name · medium · AT-3103 searches the bytes in raw and JSON-escaped forms; TC-3109 checks every directory.
- Board text reaches HTML in three seats (server templates, client JS, the download's JSON) (C8) · medium · LLR-3106.1 + AT-3106 + TC-3115 with a hostile fixture.
- The live contract is past the lean budget (`V26` NOTICE, 72k chars) · certain · declared; the P2 lenses may fold narration out.
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
| `V26` | the live contract is past the lean budget (`_LEAN_MAX_CHARS`) — 7 HLRs and 18 LLRs over three new modules and three touched ones, each LLR carrying its census symbols and nodes | P2 may fold narration into the ledger |
| `V27` | no dated `decisions_log` entry yet (P0 gate only) | left with the P0 `--decision` (2026-10-29) |
| `V30` | the gate runs from a bundle | never (every gate) |
| `V31`, `V32`, `V36`, `V37`, `V38`, `V41`, `V43`, `V44` | `increment-001.md` seed fields hold their placeholders | 001's packet |
| `V42` | deferral markers in closed records too short to key or outside a lane (sealed); the batch record untracked until the P0 commit | the step-3 one with the P0 commit; the closed ones stay |
| `V47`, `V48`, `V49` | `04-validation.md` seed placeholders | P4 |
| `V50`, `V51`, `V54` | `05-close.md` seed placeholders | P5 |
| `V52` | `design/design-proposal.md` §7 still the template | PDR |
| `V53` | this contract names 25 planned test nodes (7 AT, 18 TC; 32 mention lines) in `tests/test_report_html.py`, `tests/test_report_workspace.py`, `tests/test_report_deck.py`, `tests/test_report_export_app.py` and `tests/test_modal_keys.py` that Phase 3 has not written; plus the closed-record census line | each node's increment |

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `env -u NO_COLOR python -m pytest .scratch/test_import_probe.py -s -q` (from the worktree root) | 2026-10-29 | 1 passed — `taskboard.__file__ = C:\Users\jjgh8\Github\taskboard-wt\report-proto\taskboard\__init__.py`, inside the worktree (`evidence/import-probe.txt`) |
| `env -u NO_COLOR python -m pytest -q tests/test_report.py` (P1 probe 6, the CLI report's pin) | 2026-10-29 | 18 passed (`evidence/p1-probes.txt`) |

## Decision log (human-readable mirror of `state.json`)

| Station | Date | Decision |
|---|---|---|
| P0 | 2026-10-29 | P0 intake approved under the batch's standing authorization — the operator's verdict (B and C chosen, the round's recommendation not objected) and «decide cómo continuar, con opus o sonnet», quoted in the commission; rollover re-stamped `base_ref` 9da7438 (the start gate's 38 `V59` blocks cleared); RC-1(a) no rebase, RC-1(b) not shipped, RC-2 origin answered; triggers A1 A2 B1 B4 C4 C6 C8 D1 E1 fired (ARQ, PDR, DDR taken up); US-3101 READY; gate 0 block; batch opened in `cb76bee`. ARQ next. |
| ARQ | 2026-10-29 | ARQ module map approved under the batch's standing authorization — three new layers (`report_html`, `report_workspace`, `report_deck`), their dependency bans and import direction, six interface rows, four rationale rows, a one-lane serial worksheet; the tree check: map current (`evidence/arq-map-check.txt`); gate 0 block; the architect lens reads the map again at P2. P1 next. |
| P1 | 2026-10-29 | P1 requirements approved under the batch's standing authorization — US-3101; HLR-3101..3107; 18 LLRs with source module, C-26 symbols and TC node; AT-3101..3107 (one planned black-box node each); 9 premises TRUE; one lane; three FLOW blocks; the scan's 6 flags answered with the C4/C6/C8 controls; gate 0 block (`V26`, `V53` declared). P2 review is next. |

# Design proposal — taskboard — Batch 2026-10-29-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language
> The normative rules below are language-independent. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Design proposal` · `7 · Forward-applicability table` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **Why a HEADING is reserved here and a FIELD NAME everywhere else:** `C-49`'s artifact is the §7 TABLE, and a rule that read a summary bullet instead of the rows would be reading a claim about the table rather than the table. `V52` therefore keys on this document's own H1 and on the §7 heading, which is why both are on the machine plane. **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`.

> **Owed in.** `core` by trigger · `full` ✓
> **Source:** `/dev-flow-init` step 4's seed-by-level table, which is this fact's one home. A level marked `—` **does not owe this artifact, and its absence is not an omission**; `by trigger` means the station exists only when the `triggers` block fired, and `stations_active` in `state.json` is the authority for *this* batch. Where a SECTION or a gate row is owed more narrowly than the artifact, it says so on the row.

> **Where this lives: the VAULT + Drive**, not the repo — it is deliberation, and its traceability to
> code is weak. It is **cited by id** from the repo (`PDR-<batch_id>#D<n>`), never copied.
> What binds code — a frozen interface, a design characteristic — also lands in the **repo**, in the
> requirement or in `docs/ARCHITECTURE.md`. *The vault keeps the deliberation; the repo keeps the commitment.*

> **The forward-applicability rule (ISO/IEC/IEEE 15288).** Everything below must be NAMED as the input
> of a later activity. **If a section of this proposal is nobody's input, delete it — it does not belong
> in the PDR.** That rule is what allows this document to cost half the batch without being waste.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-29-batch-01` |
| Requirements covered | `US-3101 · HLR-3101..HLR-3107 v1 · LLR-3101.1..LLR-3101.3 · LLR-3102.1..LLR-3102.3 · LLR-3103.1..LLR-3103.3 · LLR-3104.1 · LLR-3105.1..LLR-3105.2 · LLR-3106.1..LLR-3106.2 · LLR-3107.1..LLR-3107.5` (the contract as approved at P2 round 2, ledger through `LED-2026-10-29-batch-01.21`) |
| Modules touched (from `docs/ARCHITECTURE.md`) | NEW `report_html` (`taskboard/report_html.py`), `report_workspace` (`taskboard/report_workspace.py`), `report_deck` (`taskboard/report_deck.py`); touched `app` (`taskboard/app.py`), `modals` (`taskboard/modals.py`), `keymap` (`taskboard/keymap.py`); README.md (docs); `tests/` |
| Triggers that fired | `A1 · A2 · B1 · B4 · C4 · C6 · C8 · D1 · E1` (PLAN.md#triggers) |
| Author / reviewers | `architect` (author: the orchestrator, written by the scribe from the orchestrator's brief) · reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (family D fired), each spawned independently |

---

## 1 · Objective and scope

Port the prototype round's variants B and C into the app as two renderers over ONE frozen
extraction dict, behind a global `H` modal, so the owner exports a filterable workspace and a
concise deck of every loaded board (or one project), prints or downloads exactly the configured
view, and opens the written file from the toast (`01-requirements.md`, HLR-3101..HLR-3107).

This design will NOT: change `report.py` or `taskboard --report`; change the presentation's `x`
export; write any board; make any network request; let the page write any file other than the
browser download the owner clicks; add a runtime dependency.

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `report_html` (`taskboard/report_html.py`, NEW, increment 001) | the extraction (boards → the dict of §3.1); notes HTML from escaped segments; script-safe JSON; the slug and file names; writing the files | `extract`, `notes_html`, `embed_json`, `slug`, `report_name`, `write_reports`, `esc` (= `report._e`) — signatures in §3.2 | `app`, `modals`, `keymap`, `boards`, `team_sync`; from `report` anything but `_e`/`_due_word` (LLR-3101.3) |
| `report_workspace` (`taskboard/report_workspace.py`, NEW, 001 + 002) | variant B: the page template, its CSS (screen + print) and its JS (§3.3) | `render(d) -> str` | any package module but `report_html` (LLR-3101.3) |
| `report_deck` (`taskboard/report_deck.py`, NEW, 003) | variant C: cover, overview, project slides as server-rendered SVG + paging JS (§3.4) | `render(d) -> str` | the same as `report_workspace` |
| `app` (`taskboard/app.py`, touched, 004) | `action_report_export` (collect, extract, write, toast), the 10 s `o` offer, `_report_clock` | the action (bound by `KEYMAP`) | rendering HTML (that is the renderers) |
| `modals` (`taskboard/modals.py`, touched, 004) | `ReportExport` (§3.5) | the modal class | writing files, reading the registry |
| `keymap` (`taskboard/keymap.py`, touched, 004) | the `H` row | `KEYMAP` | — |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ — the three new layers, their bans and the import direction (renderers → `report_html` at module level; `write_reports` → renderers function-local) are the ARQ map as amended through `LED-2026-10-29-batch-01.21`.

## 3 · Diagrams

### 3.0 Information viewpoint — one extraction, two renderers, one in-page filter

```
board files ──► app.board_lanes ──► [(id, name, colour, Board)]  (None boards skipped, counted)
people.json, marks.json ─────────────────────┐
                                              ▼
                  report_html.extract(boards, people, marks, today, project)
                     │  status rule · due_word=_due_word(days) · valid_url · notes_html · keys
                     ▼
                the dict d  (§3.1 — FROZEN for increment 003)
          ┌──────────┴───────────┐
report_workspace.render(d)   report_deck.render(d)
  shell + embed_json(d)        cover · overview · slides (server SVG, _e escaped)
          └──────────┬───────────┘
        report_html.write_reports ──► <board dir>/reports/{workspace,deck}[-<b>-<p>]-<date>.html
                                                       │ toast · o (≤10 s) ─► os.startfile / webbrowser
   in the browser (workspace only):
   #board-data ─► DATA ─► parseHash(location.hash | meta.view) ─► view ─► applyFilters ─► kept
        kept ─► render sections (textContent; notes_html the one innerHTML) ─► writeHash(view)
        kept ─► downloadView (reduce + shell + meta.view) ─► workspace-view-<date>.html
        kept ─► CSV / JSON (visible rows, formula guard) · beforeprint ─► print header
```

### 3.1 The extraction dict — FROZEN shape (Information viewpoint)

Derived from LLR-3101.1 and the prototype's `collect()` (`prototypes/html_report/variant_b/build.py:62-130`).
Dates are ISO `YYYY-MM-DD` strings; colours are `#rrggbb` from `views.HEX`; every list is in board
order, then the board's project order (Inbox last), then the board's task order.

| Path | Type | Meaning / source |
|---|---|---|
| `v` | `int` = `1` | the shape's version; the page refuses (shows an error line) any other |
| `meta.generated` | `str` date | the export date (`today`) |
| `meta.today` | `str` date | the day statuses and due words are computed against |
| `meta.scope` | `{kind: "all" \| "project", project: str \| None, boards: [str]}` | `project` = the project key in scope `p`; `boards` = board NAMES in scope (the header's `All loaded boards (N): <names>` / `Project <name> on <board>`) |
| `meta.view` | `dict \| None` | `None` in an exported report; in a downloaded view: `{state: <the hash state object>, summary: str, exported: str date}` |
| `boards[]` | `{key: str, name: str, colour: str}` | `key` = registry id, or `#<position>` for an unlisted board (id None) |
| `projects[]` | `{key, board, id, name, colour, archived, status, momentum, open, done, late, worst, high, due, due_word, phases}` | `key` = `<board key>:<project id>` or `<board key>:inbox`; `board` = board key; `id` str or None (`None` marks the Inbox — no separate flag); `status` = the lane status (`on_track`, `at_risk`, …); `momentum` = `views.sitting(...)` or `"nothing open"`; `open`/`done`/`late`/`high` ints; `worst` int or None; `due` date or None; `due_word` = `report._due_word(due_in, closed)` computed inside `extract` (the project's own word; `closed` is read there, never emitted); `phases` = the board's phase list |
| `tasks[]` | `{key, project, board, title, phase, priority, start, due, due_in, age, done, archived, status, blocked, milestone, mark, mentions, deps, chain, due_word, notes_html, notes_text, urls}` | `key` = `<board key>:<task id>`; `project`/`board` = keys; `priority` str; `start`/`due` date or None; `due_in` int or None; `age` = `models.days_in_phase` int or None; `status` ∈ `archived` > `done` > `late` > `open` (§1.3); `mark` = class key or None; `mentions` = person ids; `deps` = task keys this task waits on; `chain` = task keys downstream of it (transitive); `due_word` = `report._due_word(due_in)`; `notes_html` = `notes_html(notes, people)`; `notes_text` = the notes with markers dropped (search only); `urls` = `views.valid_url` results only |
| `people[]` | `{id: str, name: str, role: str}` | directory people mentioned in at least one task in scope |
| `marks[]` | `{key: str, name: str, shape: str, colour: str}` | classes used by at least one milestone in scope |

**Closed by the PDR (P-1, C1, `LED-2026-10-29-batch-01.22`):** `priority`, `age`, `due_in`, `notes_text`, `high`, `worst`, `v`, `tasks[].board`, `projects[].id` and `people[].role` are admitted in LLR-3101.1 (the table above is the shape); `closed` and `inbox` are dropped (`closed` only fed the project's due word, the Inbox is the project whose `id` is `None`). Discharged.

### 3.2 `report_html` — public functions

| Signature | Behaviour |
|---|---|
| `extract(boards: list[tuple[str \| None, str, str, Board]], people: dict[str, Person], marks: dict[str, Mark], today: date, project: str \| None = None) -> dict` | the §3.1 dict; `boards` = `(registry id, name, colour, board)` from `board_lanes`, `None` boards already skipped by the caller; `project` = the project KEY `<board key>:<project id>` that `app` builds, never the bare id (C5); reads, never writes |
| `notes_html(text: str, people: dict[str, Person]) -> str` | per line: `highlight_segments` → per segment `split_mentions`; each piece `esc`-aped inside `<span class="hl-<tone>">` (a known mention `<span class="hl-<tone> mention">@<name></span>`); lines joined by `<br>` — only constant tags |
| `embed_json(d: dict) -> str` | `json.dumps(d, ensure_ascii=False, separators=(",", ":"))` then `<` → `\u003c`, `>` → `\u003e`, `&` → `\u0026` |
| `slug(name: str) -> str` | `"".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")[:40]` (the CLI's rule, pinned by TC-3123) |
| `report_name(kind: str, today: date, board_slug: str \| None = None, project_slug: str \| None = None) -> str` | `workspace-<date>.html`, or `workspace-<board slug>-<project slug>-<date>.html`; `kind` ∈ {`workspace`, `deck`} |
| `write_reports(d: dict, kinds: tuple[str, ...], folder: Path, today: date) -> list[Path]` | `folder.mkdir(parents=True, exist_ok=True)`; for each kind, renders each kind through a plain function-local `from . import report_workspace` / `from . import report_deck` (C4: no `importlib`, which the AST walk cannot see; the deck branch is written in 001 and its import resolves once 003 adds the module, so 003 adds no line here) and writes UTF-8; overwrites a same-day file; returns the paths in `kinds` order |

### 3.3 `report_workspace` — page structure and JS inventory

Page structure (one file, `<!doctype html>`, inline CSS and JS, no external reference):

```
<header id="view-header">  scope line · generated date · [printed date] · filter summary   (all filled by JS)
<nav class="controls" aria-label="Filters">                                    (every control built by JS from DATA)
   <details id="f-projects"><summary>Projects n/N</summary> All · None · per board: ☐ project (colour chip) …
   status chips  open late done archived · people chips · class chips · from/to <input type=date>
   search <input type=search> · sections  gantt table notes milestones · zoom  fit day week month
   Reset · active-filter count
   Export this view:  [Print / Save as PDF] "the file still holds all data"
                      [Download this view]  "only this file leaves the hidden data out"
                      [Download CSV] [Download JSON]  "visible rows only"
<main>  section#s-gantt (svg)  ·  section#s-table  ·  section#s-notes  ·  section#s-milestones
<div id="card" role="dialog"> the task card   ·   <div id="tt"> the tooltip
<script id="board-data" type="application/json">  embed_json(d)  </script>
<script>  the page JS  </script>
```

**The shell carries NO board-derived text outside `#board-data`** (LLR-3103.2): titles, headings
and every label above are constants; everything board-derived is set by JS with `textContent`.

| JS function | Owner LLR | What it does |
|---|---|---|
| `const DATA` / `SHELL` | 3103.2 | `DATA = JSON.parse(#board-data.textContent)`; `SHELL` = `document.documentElement.outerHTML` captured FIRST, before any render, with `#board-data` emptied |
| `whitelists(DATA)` | 3102.3 | the allowed values: project keys, `STATUS`, people ids, class keys, `SECTIONS`, `ZOOMS` |
| `parseHash(str, wl) -> view` | 3102.3 | splits `#v=1&…`; drops a `v` ≠ 1 whole; keeps only whitelisted values; dates by `/^\d{4}-\d{2}-\d{2}$/` + a real-date check; `q` kept as a string; also used on `meta.view.state` (LLR-3103.2) |
| `writeHash(view)` | 3102.3 | `history.replaceState` with the encoded view (`p` = CHECKED keys) — default view → empty hash |
| `buildControls(DATA, view)` | 3102.1 | creates every control as `button[aria-pressed]` / `input` / `details>summary`, labels by `textContent`, the active-filter count |
| `applyFilters(view, tasks) -> kept` | 3102.2 | the truth table: projects ∩ status (reads `t.status`) ∩ people-any ∩ classes-any ∩ date span ∩ search (`toLowerCase` over title, `notes_text`, project name) |
| `render()` | 3102.1 | `kept = applyFilters(...)`; `renderHeader`, `renderGantt`, `renderTable`, `renderNotes`, `renderMilestones` by the section toggles; `writeHash` |
| `renderHeader(view, kept)` | 3102.1, 3104.1 | the scope line, the filter summary (kept items only), the dates |
| `safeHref(u)` | 3106.2 | returns `u` only if `/^https?:\/\//i.test(u)`, else `null` (no anchor) |
| `openCard(key)` / `closeCard()` | 3106.1 | the card by `textContent`; `notes_html` → the card's notes by `innerHTML` (the ONE exception); dep/chain titles resolved from `DATA.tasks` by key (missing → nothing) |
| `setPrinted()` + `beforeprint` listener | 3104.1 | writes the printed date into the header; the Print control calls `setPrinted()` then `window.print()` |
| `reduce(DATA, kept, view) -> d2` | 3103.1 | kept tasks; projects/boards/people/marks used by them; deps/chain filtered to kept keys; notes stripped when notes are off; `meta.scope.boards` and `meta.view` over kept items |
| `downloadView()` | 3103.2 | `d2 = reduce(...)`; `json = JSON.stringify(d2).replace(/[<>&]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4,'0'))`; the file = `SHELL` with the data element's text set through a DOM build (a `DOMParser` document, `textContent`), serialised — no `String.replace` with a string replacement; Blob → `workspace-view-<date>.html` |
| `csvCell(v)`, `downloadCsv()`, `downloadJson()` | 3103.3 | visible rows only, reduced as `reduce`; `csvCell` prefixes `'` to a cell starting with `= + - @ \t \r` (a `-3d` due word included) |
| `reset()` | 3102.1 | the default view, the hash cleared |

CSS: `:root` palette with a `prefers-color-scheme: light` override (both themes); no fixed widths
over 390 px (the gantt scrolls inside `.gantt-wrap`, never the page; long titles wrap with
`overflow-wrap: anywhere`); `@media print` = the round's rules (`variant_b/build.py:229-246`) plus:
`.controls, #card, #tt, .dl, .zbtn, nav { display: none !important }`, `#view-header { display: block }`,
`tr, .card, .note, .ms { break-inside: avoid }`, and the full-gantt fix of commit `6c1225f` —
`.gantt-wrap{overflow:visible}`, `#gantt{min-width:0!important}`, `#gantt svg{width:100%;height:auto;max-width:none}`.

### 3.4 `report_deck` — slide inventory (from `prototypes/html_report/variant_c/build.py`)

| Slide | Content, read from the dict | Prototype seat |
|---|---|---|
| cover | the scope line (`meta.scope`), per-board table (projects, open, done, overdue, archived from `projects[]`/`tasks[]`), totals tiles, the class legend (`marks[]`) | `title_slide` `:564`, `legend` `:503` |
| overview | every project in scope on one timeline (`projects[].due`, the tasks' spans) | `overview_slide` `:607`, `gantt_overview` `:398` |
| one per project | for every non-archived project (Inbox included) holding ≥1 task of any status: header (name, colour chip, lane status, open/done/high/late/worst, `due_word`, momentum), `<n> tasks` (non-archived), the vector gantt (real `<text>`, today's rule, dependency arrows by `deps` keys, mark shapes), notes (`notes_html`) and `safeHref` links, footer `<k> archived` when k > 0 (`0 tasks · k archived` when all are) | `project_slide` `:512`, `gantt_project` `:272`, `_meta` `:183`, `archived_tasks` `:496` |

Paging JS (`variant_c/build.py:756`): `keydown` on `ArrowRight`/`PageDown` +1, `ArrowLeft`/`PageUp`
−1, `Home` first, `End` last, ignored when `document.activeElement` is `input`/`textarea`; the
counter `n / N`; previous/next buttons. `@media print`: every `.slide` displayed, `break-after: page`,
the light palette. Every board string on a slide is `esc`-aped server-side; URLs only through the
dict's filtered `urls` and the page's `safeHref` re-check.

### 3.5 `app` / `modals` / `keymap` — the `H` export (Interaction viewpoint)

`ReportExport` at 118x30 (a centred `ModalScreen`, the app's modal backdrop; keys only, no `Button`):

```
┌ Export an HTML report ─────────────────────────────────────────────┐
│                                                                    │
│   Scope   ● all boards (3)       Personal · Client A · Course       │
│           ○ Storefront relaunch on Client A                         │
│                                                                    │
│   Writes to  C:\…\boards\client-a\reports\                          │
│                                                                    │
│   b workspace   c deck   a both   p Storefront relaunch   o all boards   esc close │
└────────────────────────────────────────────────────────────────────┘
```

- The key line is `keymap.key_line([("b", "workspace"), ("c", "deck"), ("a", "both"), ("p", <project name or "no project selected">), ("o", "all boards"), ("esc", "close")], width)` — the shared painter (`taskboard/keymap.py:177`), so the words fold before the keys at narrow widths.
- The scope mark is `●`/`○`; `p`/`o` move it (re-render, modal stays); with no current project the `p` row reads `no project selected` and `p` leaves `o` marked.
- The destination line is the open board's `reports/` folder; the board count is the readable lanes of `board_lanes` (skipped ones are counted in the toast, not here).
- `b`/`c`/`a` dismiss `(kinds, scope)`; `escape` dismisses `None` and writes nothing.
- `app.TaskboardApp.action_report_export`: lanes → `extract` → `write_reports` → `notify("Report written: <name> to <dir> — o opens it (10 s)", title="Report", severity="information", timeout=10, markup=False)` (both names joined by ` and `; ` · <n> board(s) skipped`); the offer = `(path, deadline = self._report_clock() + 10)`; `_report_clock = time.monotonic` (the test seam).
- `action_open_url`: if an offer is live (`_report_clock() < deadline`), open the offer's path (`os.startfile` on Windows, else `webbrowser.open(path.as_uri())`, `OSError` swallowed) and return; else today's behaviour.
- `KEYMAP` row: `Key("H", "H", "report_export", "Report", group="misc", bar=False)`; README's key table gains `H`.

### 3.6 Enablers (fixtures, helpers, environment)

- **`tests/report_fixture.py` (NEW, increment 001)** — synthetic only, TODAY = 2026-10-29, built on the round's `fixture.py` shapes: boards Personal / Client A / Course; people Ana Ruiz / Luis Prado / Carmen Vega plus the hostile person; classes Delivery / Billing / Launch. Each hidden-able item carries a unique token no UI string contains (`qzP1`, `qzB1`, `qzU1`, `qzM1`, `qzT1`, `qzL1` for project, board, person, class, title, URL). It holds: the hostile title `<script>alert(1)</script>`; a note `</script><b>x</b> & "q" ==hi==`; a person named `<img src=x onerror=window.__x=1>`; a project and a board named with `<img src=x onerror=window.__x=2>`; URLs `javascript:alert(1)` and `data:text/html,<b>x</b>` beside a valid `https://example.test/…`; a title with `$&` and `$'`; a title `=1+1`; a task 1 day late (`-1d` → CSV `'`); a 120-character title and a Unicode title (`Año nuevo — ñandú 日本語`); a project-less (Inbox) task; a cross-project dependency and a chain of three; an archived task; an archived project; a project whose tasks are all archived; a task-less project; two boards each with a project named `Docs`; the Client A board's project `Storefront relaunch` (no project shares a board's name); undated tasks; a task with `start == due`. Literal expected sets (ids, counts, statuses, due words) are module constants beside the data (Q9, Q16).
- **`tests/report_browser.py` (NEW, increment 001)** — the shared headless helper: `require_browser()` (imports `playwright.sync_api`; when missing, `pytest.fail` if `TASKBOARD_REQUIRE_BROWSER=1`, else `pytest.skip`); `open_page(path, *, scheme="dark", viewport=(1366, 900), hash="")` returning a page with collectors `console_errors`, `page_errors`, `requests` (every URL but the file's), `dialogs`; `shown_ids(page)` (the table's `data-key`s as a multiset); `download(page, control)` (`expect_download`, saved under `tmp_path`).
- **`TASKBOARD_REQUIRE_BROWSER`** — set by every run on this machine and by the P4 chunks (`env -u NO_COLOR TASKBOARD_REQUIRE_BROWSER=1 python -m pytest …`).
- **App-level browser checks (AT-3101, AT-3105)** — the pilot runs in the test's event loop; after the `async with app.run_test(...)` block the written file is checked with `await asyncio.to_thread(check, path)`, where `check` uses the sync API (a worker thread has no running loop — §2.7 row 7). Fallback, if the thread form misbehaves on Windows: `subprocess.run([sys.executable, "-m", "tests.report_browser", path])` with a JSON verdict on stdout. Decided by the first run in increment 004 and named in its packet.

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| the extraction dict (§3.1) | — (NEW) | the §3.1 shape, `v = 1` | `report_workspace.render`, `report_deck.render`, the page JS, a downloaded view, tests | **FROZEN for increment 003** — the deck is written against it; a fact the deck finds missing re-opens this PDR (a dict-shape amendment, `report_html.py` touched in 003, the workspace re-checked) |
| `report_html` functions (§3.2) | — (NEW) | as §3.2 | `app`, the renderers, tests | frozen from increment 001's gate (signatures) |
| the hash grammar `#v=1&p=..&s=..&u=..&m=..&from=..&to=..&q=..&sec=..&z=..` | — (NEW) | LLR-3102.3 | the page, `meta.view`, bookmarks | versioned by `v` |
| `KEYMAP` | no `H` | one `H` row | `app` bindings, help, palette, README law | n/a (one lane) |
| `action_open_url` | opens task URLs | the offer branch first | the `o` key | n/a |
| `report._e`, `report._due_word`, `views.valid_url`, `views.HEX`, `views.highlight_segments`, `views.lanes_of`, `views.sitting`, `people.split_mentions`, `people.mention_ids`, `models.parse_iso`, `models.days_in_phase`, `app.board_lanes`, `keymap.key_line` | — | **byte-unchanged**, consumed | everyone | **frozen** — a change returns to the trunk (A3) |

**PDR conditions discharged in this file (`LED-2026-10-29-batch-01.22`):** C1 (§3.1 — the dict shape), C3 (this §4 — `views.HEX` frozen and consumed), C4 and C5 (§3.2 — `write_reports` imports, `project` is the key). C2 and C6–C14 land in the contract; the increment-owned conditions are listed in `PDR-2026-10-29-batch-01.md`.

## 5 · Proposed test cases

Files: `tests/test_report_html.py` (unit), `tests/test_report_workspace.py` (headless), `tests/test_report_deck.py`
(unit + headless), `tests/test_report_export_app.py` (pilot + headless), `tests/test_modal_keys.py` (AT-3107 +
the `INVENTORY` row). Every AT node's docstring carries its bare id; every browser node goes through `require_browser()`.

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| TC-3101 `test_TC_3101_extract_is_json_and_holds_every_fact` (001) | 0 | the §3.1 shape (keys and types per record), JSON round trip, counts == literals, unique keys, Inbox key, no task text inside another task, board bytes unchanged | key projects by bare id (two `Docs` collide) |
| TC-3102 `test_TC_3102_due_words_are_the_cli_reports` (001) | 0 | every `due_word` == `report._due_word(due_in)` and == the literal (`1d overdue`, `due today`, `in 4d`, `no date`) | format the due word locally (`f"{d}d"`) |
| TC-3103 `test_TC_3103_project_scope_keeps_one_project` (001) | 0 | scope `p`: 1 project, its literal count, 0 foreign keys in `deps`/`chain` | ignore `project` |
| TC-3104 `test_TC_3104_renderers_read_the_dict_only` (001, re-run 003) | A (inspection) | AST walk: renderers import only `report_html`; `report_html` none of `app modals keymap boards team_sync`, from `report` only `_e`/`_due_word`; `render(d) == render(d)` | `from .views import HEX` in a renderer; a function-local `from .report import _e` |
| TC-3105 `test_TC_3105_the_bar_is_native_and_counted` (001) | A (e2e) | every control native; `Tab` reaches exactly the hand-enumerated list (fixture literals); `aria-pressed` == state; the count after 5 actions; the scope header literal | a chip as `<span onclick>` |
| TC-3106 `test_TC_3106_filters_follow_the_truth_table` (001) | A (e2e) | 6 arms (one per table row) + edge arms (status all off, `from == due`, `to == start`, `from > to`), each shown-id set == a literal set | `late` chip mapped to `open`; people `ANY` → `ALL` |
| TC-3107 `test_TC_3107_a_hostile_hash_is_dropped` (001) | A (e2e) | the hostile hash: 0 dialogs, 0 `img`, `q` as text, the default view otherwise | drop the whitelist AND echo the hash into the summary via `innerHTML` (Q10) |
| TC-3108 `test_TC_3108_reset_restores_the_defaults` (001) | A (e2e) | Reset → count 0, empty hash, default shown set | Reset leaves the hash |
| TC-3109 `test_TC_3109_the_download_keeps_only_used_entries` (002) | A (e2e) | the downloaded JSON's sets; 0 unused entries; 0 dangling keys; every `qz*` token of the hidden items 0 times (raw + escaped); the `$&`/`$'` title case | keep the full `people` list; `String.replace(SHELL, marker, json)` |
| TC-3110 `test_TC_3110_notes_off_strips_the_notes` (002) | A (e2e) | notes off → 0 `notes_html`/`notes_text` | keep notes when the section is off |
| TC-3111 `test_TC_3111_the_view_file_reopens_on_its_view` (002) | A (e2e) | file name pattern; reopened rows == source as a MULTISET; an edited `meta.view` unknown key dropped; header; labels | capture `SHELL` after rendering (rows duplicate) |
| TC-3112 `test_TC_3112_the_print_rules_hold` (002) | A (e2e) | `beforeprint` dispatched, card + tooltip opened, computed styles under print: controls none, header visible with both dates, `break-inside: avoid`; the gantt width ≤ the viewport width; `window.print` 1 call | drop `#gantt{min-width:0!important}` (width arm); drop `.controls` from the print rule |
| TC-3113 `test_TC_3113_one_slide_per_project` (003) | 0 | slide count/titles/`<n> tasks`/`<k> archived` == literals; the all-archived project and Inbox have `0 tasks · k archived`; the task-less project has none; scope `p` → 3 | iterate archived projects too; skip all-archived projects |
| TC-3114 `test_TC_3114_keys_page_and_print_splits` (003) | A (e2e) | `End`/`ArrowRight`/`Home`/`PageDown` counters; keys ignored in an input; print: N/N slides, `break-after: page` | drop the `Home` handler |
| TC-3115 `test_TC_3115_embed_json_and_notes_are_inert` (001) | 0 | `embed_json` 0 `<`/`>`/`&`, round trip; `notes_html` escapes `<b>`, keeps the constant tags only | the prototype's `.replace("</", "<\\/")` |
| TC-3116 `test_TC_3116_offline_themes_and_phone_width` (003) | A (e2e) | both files: 0 requests; 390 px light and dark with the long and Unicode titles: no page overflow; the two schemes' backgrounds differ | add a Google Fonts `<link>`; a fixed 600 px table |
| TC-3117 `test_TC_3117_H_is_seated_once_off_the_bar` (004) | 0 | 1 `H` row, `bar=False`, in the palette and `?` | drop the row |
| TC-3118 `test_TC_3118_scope_keys_and_no_project` (004) | A (pilot) | `p`/`o` marks, "no project selected", `esc` writes nothing; `INVENTORY["ReportExport"] == {}` and TC-2407's arms | reuse `present_project_id` (first-project fallback) |
| TC-3119 `test_TC_3119_files_land_beside_the_open_board` (004) | A (pilot) | file names (board + project slugs), the two `Docs` projects → 2 names, same-day overwrite, the missing board counted, board bytes unchanged | write beside the CWD |
| TC-3120 `test_TC_3120_o_opens_the_report_while_the_toast_lives` (004) | A (pilot) | the notification record's text; `o` < 10 s → 1 open inside `reports/`; > 10 s → `open_url` (via `_report_clock`; `os.startfile` patched `raising=False`) | never expire the offer |
| TC-3121 (004) | A (inspection) | `git diff 9da7438 -- taskboard/report.py taskboard/__main__.py taskboard/views.py` empty | — (a pin) |
| TC-3122 `test_TC_3122_csv_and_json_hold_the_visible_rows_only` (002) | A (e2e) | visible rows only; tokens absent; `'=1+1` and `'-1d` | export the full data; drop the `'` prefix |
| TC-3123 `test_TC_3123_the_slug_is_the_cli_reports` (001) | 0 | `slug(n)` == `report_path`'s slug for 3 names | lower-case only (no `-` mapping) |
| TC-3124 `test_TC_3124_extract_keeps_only_http_urls` (001) | 0 | the hostile task's `urls` == `[]`, the valid one kept | drop the `valid_url` filter |
| TC-3125 `test_TC_3125_one_status_rule` (001) | 0 | every task's `status` == its literal; the deck and the page read it (grep of the JS: no `due_in < 0` status derivation) | derive `late` with `<=` |
| AT-3101 `test_AT_3101_H_b_writes_the_workspace_and_the_toast_names_it` (004) | B | `H b`: the file, the toast, headless load 0 errors / 0 requests, `o` opens it | the toast drops the file name |
| AT-3102 `test_AT_3102_filters_and_the_hash_round_trip` (001) | B | five filter kinds by clicks; count; the hash round trip; Reset | skip `writeHash` |
| AT-3103 `test_AT_3103_download_this_view_holds_only_the_filtered_tasks` (002) | B | the download's ids == shown; every hidden token 0 times; reopened (B4) same view | re-embed the full data |
| AT-3104 `test_AT_3104_print_hides_the_controls_and_shows_the_filter_header` (002) | B | print: 0 visible controls, header with the filters and dates | drop `.controls` from the print rule |
| AT-3105 `test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project` (004) | B | `H o c` / `H p c` slide literals; `H a` agreement per project | a second extraction keeping archived projects |
| AT-3106 `test_AT_3106_board_text_is_escaped_in_both_reports` (003) | B | both files: 0 dialogs, `window.__x` undefined, literal hostile text, 0 non-http(s) anchors, 0 `<script>alert(1)` bytes | remove one `esc` from the deck's title; drop `safeHref` |
| AT-3107 `test_AT_3107_the_report_modal_obeys_the_modal_key_law` (004) | B | `H`: the key line's six patterns, the destination and count; each key's effect | the key line drops `esc close` |

Layer 0 applies to `extract`, `notes_html`, `embed_json`, `slug` (cyclomatic ≥ 3 or crossing the
`report_html` boundary). The P3 battery runs each named mutation per arm with restore digests (C-40).

### 5.1 Design → requirement traceability

| Design element | Requirement(s) |
|---|---|
| §3.1 dict, `extract` | LLR-3101.1, LLR-3101.2, LLR-3101.3 |
| `notes_html`, `embed_json`, `esc` | LLR-3106.1 |
| `slug`, `report_name`, `write_reports` | LLR-3107.3 |
| `parseHash`, `writeHash`, `whitelists` | LLR-3102.3 |
| `buildControls`, `render`, `renderHeader`, `reset` | LLR-3102.1 |
| `applyFilters` | LLR-3102.2 |
| `reduce`, `downloadView`, `SHELL` | LLR-3103.1, LLR-3103.2 |
| `csvCell`, `downloadCsv`, `downloadJson` | LLR-3103.3 |
| `setPrinted`, print CSS | LLR-3104.1 |
| `safeHref`, palettes, layout | LLR-3106.2 |
| deck slides, paging | LLR-3105.1, LLR-3105.2 |
| `ReportExport` | LLR-3107.2 |
| `action_report_export`, offer, `_report_clock` | LLR-3107.3, LLR-3107.4 |
| `KEYMAP` `H` | LLR-3107.1 |
| frozen consumed interfaces (§4) | LLR-3107.5 |

## 6 · Risks and rejected alternatives

> Rejected alternatives are owed WHERE A REAL DECISION EXISTS.

| Alternative considered | Why it was rejected |
|---|---|
| Each renderer reads the boards itself (the round's two `collect`s) | two extractions disagree (the round's `late` rules already did); HR-1 and D19 pin one dict |
| The app writes the filtered view file (Python reduces) | a second filter engine that can disagree with the page's `applyFilters`; the owner configures the view in the browser, not in the app |
| `String.replace(SHELL, marker, json)` to build the download | `$&`/`$'` in board text re-insert the block (S3); a DOM build is pattern-free |
| A subprocess per app-level browser check as the default | slower and harder to debug than `asyncio.to_thread`; kept as the declared fallback (§3.6) |
| Default scope `p` | D8 keeps `o` (the round's default, HR-2) with two visible controls |

Risks: the dict's open facts (P-1) were closed at the PDR by `LED-2026-10-29-batch-01.22`; a fact the deck lacks at
003 re-opens this PDR; the gantt SVG's width at 390 px needs `.gantt-wrap` scrolling, not page
scrolling (TC-3116); the browser tests are invisible to CI (declared in `01-requirements.md` §6.3).

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics — the frozen §3.1 dict, the §3.2 signatures, the §3.3 page structure and JS inventory, the §3.4 slide inventory, the §3.5 modal layout and offer | the Phase-3 increments 001–004 (the `software-dev` authors) and their `code-reviewer` passes | this file §3, cited as `PDR-2026-10-29-batch-01#D1` (the dict), `#D2` (the page), `#D3` (the deck), `#D4` (the `H` export) in each increment brief and packet §1 |
| enablers — `tests/report_fixture.py`, `tests/report_browser.py`, `TASKBOARD_REQUIRE_BROWSER`, the `asyncio.to_thread` check | Phase 3 (increment 001 creates the first two; 004 the thread check) and the P4 suite | this file §3.6; increment 001's brief; the P4 chunk commands in `04-validation.md` |
| proposed test cases — TC-3101..TC-3125, AT-3101..AT-3107, each with its reddening mutation | layers 0/A/B at P3 (each increment's mutation battery) and the DDR | this file §5; the increment packets' `Mutation verdicts`; the DDR record `design/DDR-2026-10-29-batch-01.md` |
| design → requirement traceability (§5.1) | the DDR and the P4 matrix row | this file §5.1; `04-validation.md` |

- ⚠ Any row whose consumer column is empty: none — all four rows name a consumer and a place.

## 8 · Parallelisation plan *(only if the batch forks)*

One lane — §8 not owed (`01-requirements.md` §2.8 declares the empty). The increment cut, serial:

| Increment | SOURCE files | Count |
|---|---|---|
| 001 | `taskboard/report_html.py`, `taskboard/report_workspace.py` (B, HR-3 controls, the hash) | 2 / 4 |
| 002 | `taskboard/report_workspace.py` (HR-4: print, download, CSV/JSON) | 1 / 4 |
| 003 | `taskboard/report_deck.py` (+ `taskboard/report_html.py` ONLY if the dict lacks a fact — that is a dict-shape amendment and re-opens this PDR) | 1–2 / 4 |
| 004 | `taskboard/app.py`, `taskboard/modals.py`, `taskboard/keymap.py`; README.md (docs, not source) | 3 / 4 |

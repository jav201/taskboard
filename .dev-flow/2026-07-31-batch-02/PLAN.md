# PLAN — taskboard · batch 2026-07-31-batch-02 (living compendium)

## BLUF

**The feature is real and new (RC-1 clean: no report exists), but it does NOT need
the full V-model — it compresses to `/fast-dev-flow` weight, and I recommend
routing it there.** Phase 0 also produced one finding that changes the design
before a line is written: **the app's 8 project hues FAIL as a chart palette**,
measured, so the report cannot lean on hue.

## Where we are
Phase 0 (story intake), at its gate. Nothing implemented.

## Objective
A self-contained local document (HTML) reporting the board — whole board or one
project — generated on demand, read-only over `board.json`.

## Routing recommendation — `/fast-dev-flow`, argued

The command's own matrix routes by *kind*, not by enthusiasm:

| Test | This feature |
|---|---|
| Client deliverable / regulated context? | **No** — an internal tool for one user |
| Small feature with a known implementation path? | **Yes** — one new module, one output format, two thin entry points |
| Files | ~6: `report.py` (new), `__main__.py`, `keymap.py`, `app.py`, `tests/test_report.py` (new), `README.md` |
| Unknowns | none structural; the data layer already exposes everything needed |

Cost of the full V-model here: 6 phases, 4 artifacts, 3 parallel review agents, a
traceability matrix and an executive summary — for a feature whose acceptance is
"a file appears at a path, it opens, and it says true things". **The ceremony
would exceed the work.** The coordinator asked me to say so if it compressed;
it compresses.

**What I am NOT dropping by routing down:** the premise table, observable
acceptance criteria, the read-only law, the mutation battery, and the
per-increment review packet. Those are fast-flow obligations too.

## Blocker to resolve before any batch opens (state, not code)

`.dev-flow/state.json` says **batch `2026-07-18-batch-01`, phase 6,
`awaiting-sync`** — and the flow's own routing rule for `awaiting-sync` is *"do
not advance"*. That batch closed in practice on 2026-07-18; every batch since has
run through `/fast-dev-flow` and never touched `state.json`, so the file now
asserts something false about the project's state. This is exactly the C-44
hazard: *the canonical state file is what the next session reads to orient
itself.* It must be dispositioned (synced, or explicitly closed) rather than
stepped over.

## RC-1 — base currency

- local HEAD `eec625b` == `origin/main` `eec625b` — **current, nothing to rebase**.
  (The last commit was pushed by the operator between batches.)
- Already-shipped check for "report": `grep` finds only `load_report` (load
  health) and `archivable_report` (archive counts) — **unrelated. The story is new.**
- Backlog routing: no `docs/engineering-rules.md`, so the canonical file is
  `.dev-flow/BACKLOG.md`. Its **header is stale** (`Base ref b3cc60d`, "226 tests
  green", "none pushed") while its body is current — fix at close.

## Story intake (INVEST + Definition of Ready)

**US-01 — "As the board's owner, I want to generate a report of the whole board
or of one project, so I can read and share its state outside the TUI."**

| Axis | Assessment |
|---|---|
| **Valuable** | Yes — the data exists but is only readable inside a terminal widget |
| **Negotiable** | Yes — content set is specced below, not dictated by the user |
| **Estimable / Small** | Yes — one module + two entry points |
| **Independent** | Yes — no dependency on open backlog items |
| **Testable (black-box)** | Yes — *"When `taskboard --report` runs over a fixture board, a self-contained HTML file exists at the reported path, opens standalone, and states the board's real counts."* |

**Status: READY** — one open decision, resolved below (format).

## The format decision — HTML, with the alternative struck

Javier said *"probablemente un svg o un html"*, which delegates the choice.

**HTML, because a report is a document, not a picture.** It carries prose, tables
and several figures at once; it reflows on a phone; text in it is selectable and
searchable; it prints to PDF from any browser. **A single `.html` file with the
CSS and the SVG figures inlined is exactly as self-contained as a `.svg`** — one
file, no CDN, opens anywhere.

**~~SVG as the container~~** — struck, and the reason is concrete: an SVG is a
fixed canvas. Text does not reflow, long project names overflow or need manual
truncation, and a board with 3 projects and one with 40 need different canvas
heights computed by hand. SVG is the right tool for the *figures*, so it is used
**inside** the HTML — which is the arrangement that gets both properties.

*Strikeable:* if he ever wants one image to paste into a chat, `--format svg`
emitting a single figure is a small follow-on, not a redesign.

## Phase-0 finding that constrains the design (measured, not asserted)

Ran the `dataviz` validator over the app's own 8 project hues as a categorical
palette (`scripts/validate_palette.js`, dark surface `#0d1117` **and** light):

```
[FAIL] CVD separation      worst adjacent #e879f9 fuchsia <-> #a78bfa violet   dE 0.4 (protan)
[FAIL] Normal-vision floor worst adjacent #a78bfa violet  <-> #818cf8 indigo   dE 5.4  (below the 15 floor)
[PASS] Chroma floor, contrast vs surface
```

Two consequences, and the second is a real app finding:

1. **The report may not encode a project by hue alone.** Every figure carries
   direct labels and a table view; ordering and position do the work hue cannot.
   (The skill mandates the table view anyway; this makes it load-bearing.)
2. **The app has the same collision** — `violet` and `indigo` are two of the eight
   colours a project can be assigned, and at ΔE 5.4 they are hard to tell apart
   *with full colour vision*; `fuchsia`/`violet` are identical to a protan reader.
   **The colour ration measured identity-vs-severity distance and never measured
   identity-vs-identity.** New backlog item; out of scope for this batch.

## Content set — only what the data honestly supports

Per project, and for the board: open / done counts · overdue count and worst
lateness · the due horizon · the load curve (drawn by `wave.py`, the real engine)
· momentum **where stamps exist, `unaged` where they do not** · archived counts ·
project status. **No forecasts, no velocity, no invented dates** — the momentum
increment's ruling travels to the document.

## Register (Prism doctrine travels)
Identity names, severity judges, ash means spent; the document states facts about
dates and counts and never addresses or grades the reader. It is the turn's log,
in document form.

## Out of scope (named, so it is not invented later)
No scheduling, no emailing, no cloud, no auto-open without saying so, no history
the board does not store.

## Risks / watch-items
- **Read-only law** — generating a report must leave `board.json` byte-identical;
  law it with a fixture, mutation-check it.
- Report opened in a browser is outside the app's control; the file is local only.
- `~/.taskboard` untouchable — fixtures only, as ever.

## Decision log
- 2026-07-31 · Routing: recommend `/fast-dev-flow` over `/dev-flow`, argued above.
- 2026-07-31 · Format: HTML container, SVG figures inlined; SVG-as-container struck.
- 2026-07-31 · Palette: report will not encode identity by hue alone (measured).

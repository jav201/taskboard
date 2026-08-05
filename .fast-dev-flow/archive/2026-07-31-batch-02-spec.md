# Quick Spec — the board report (self-contained HTML)

**Status:** CLOSED 2026-07-31 · **Base ref:** `eec625b` (origin/main) · **Batch:** `2026-07-31-batch-02`
**Flow:** `/fast-dev-flow` — routed here from `/dev-flow` Phase 0, operator-approved
2026-07-31. Rationale in `.dev-flow/2026-07-31-batch-02/PLAN.md`.
**Authorization:** end-to-end autonomous · **commit on `main`, never push** · every
un-asked decision recorded in the plan's decision log.

## 1. Objective
Generate a **self-contained local HTML document** reporting the board — the whole
board or one project — on demand. It states what the data actually holds and
nothing more, and it never modifies the board.

## 2. User story
**US-01** — *As the board's owner, I want to generate a report of the whole board
or of one project, so I can read and share its state outside the TUI.*

## 3. Acceptance criteria (observable)
- **AC1.** `taskboard --report --board <fixture>` writes a `.html` file, prints its
  path, and exits without starting the TUI.
- **AC2.** `--report "<project name>"` scopes the document to that project;
  an unknown name exits non-zero and names the mistake, writing nothing.
- **AC3.** The file is **self-contained**: no `http://`/`https://` sub-resource, no
  `<script src>`, no `<link rel=stylesheet href>`. Opening it needs only a browser.
- **AC4.** **READ-ONLY LAW** — generating a report **never writes the board**:
  `Board.save` is not called and the file's mtime does not move, for both scopes.
  *(Amended at close. It was first written as "byte-identical (md5 before ==
  after)" — which its own mutant proved vacuous: saving an unmodified board
  rewrites the SAME bytes, so a checksum cannot see a write, only a change.)*
- **AC5.** The counts in the document equal the board's real counts (open, done,
  overdue, archived) for board scope and for project scope.
- **AC6.** Momentum is honest: a project whose tasks carry no `phase_changed`
  reads **`unaged`**, never `0d`.
- **AC7.** No figure encodes a project by hue alone: every figure ships direct
  labels **and** a table view of the same numbers.
- **AC8.** Register: the document contains no second person and no grading of the
  reader (the same law `test_prism_laws.py` applies to the views).
- **AC9.** `R` in the app generates the report and reports the path in a notice;
  it never opens anything without saying so. `R` obeys the KEYMAP contract (on the
  bar, in the README).
- **AC10.** All 345 existing tests stay green.

## 4. Premise table (C-43) — executed probes

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| No report feature exists (RC-1 already-shipped) | premise | TRUE | grep: only `load_report` (load health) + `archivable_report` (archive counts) |
| Per-project facts are already computed | premise | TRUE | probe P2: `LaneFacts` = name, hue, status, tasks, open, late, done_n, total, today_n, high, due_in, worst |
| Momentum + the `unaged` honesty already exist | premise | TRUE | probe P3: `views.sitting()` callable |
| The load curve engine is available to draw with | premise | TRUE | probe P4: `wave.load_curve` callable |
| The CLI is argparse and extensible | premise | TRUE | probe P6: `argparse` in `__main__` |
| `R` is free in the KEYMAP seat | premise | TRUE | probe P7: `R` not among the seat's shown keys |
| The 8 project hues are safe as a chart palette | hypothesis | **FALSE** | `validate_palette.js`: fuchsia-violet dE **0.4** protan; violet-indigo dE **5.4** normal (floor 15). Dark **and** light. -> AC7 exists because of this. |
| The board is only ever read | axiom (re-proved here) | asserted | AC4 makes it a law with a fixture + a mutant |

## 5. Security flags
Scan: **none fired.** No auth, secrets, network, credentials, or external
integration. The report is a local file, generated on demand, from data already on
disk. `security_required: false`.

Two adjacent risks are handled as design, not flags:
- **Untrusted text into markup** — task titles, notes and project names are
  user-authored and go into HTML. **Every interpolated value is escaped**
  (`html.escape`), with a hostile-title law. This is the C-17 lesson in a new
  surface: the app already learned it for rich markup.
- **Data at rest** — the report contains the board's contents in cleartext; it is
  written beside the board it came from, never uploaded.

## 6. Non-goals (named so they are not invented)
No scheduling, no email, no cloud, no auto-open, no history the board does not
store, **no forecasts or velocity** (the momentum ruling travels), no PDF
generation (a browser prints one).

## 7. Design decisions

**HTML container, SVG figures inlined.** A report is a document: prose + tables +
several figures, reflowing, searchable, printable. A single `.html` with CSS and
SVG inlined is as self-contained as a `.svg`, without the fixed canvas. *Struck:*
SVG-as-container — text does not reflow and long names overflow. *Strikeable
later:* `--format svg` for one pasteable figure.

**Output path** = `<the board file's own directory>/reports/<scope>-<date>.html`.
So the real app writes to `~/.taskboard/reports/`, and every test writes beside its
fixture — the live directory is unreachable from a test by construction.

**Figures, per the `dataviz` procedure:** form first (magnitude -> bar; the load
curve -> the real `wave` engine's own shape), colour last and computed, direct
labels, a table view beside every figure, no dual axis, status hues reserved.

## 8. Files (5)
`taskboard/report.py` (new) · `taskboard/__main__.py` · `taskboard/keymap.py` ·
`taskboard/app.py` · `tests/test_report.py` (new). README updated at close (+1).

## 9. Close

All 10 acceptance criteria are covered by named tests (18 in `tests/test_report.py`,
each confirmed on disk). **363 green.** Eight mutants verified red.

**The premise table's one FALSE premise did its job**: the palette measurement is
why AC7 exists, and AC7's law is what kills the "named only by its colour chip"
mutant.

**A vacuous law, found by its own mutant and rewritten.** The read-only law first
compared the board file's CHECKSUM before and after — and a report that called
`board.save()` PASSED it, because saving an unmodified board writes the same bytes
back. Content-equality cannot see a write, only a change; and the risk is exactly
the case where they differ (a load-time remap or the archive sweep in memory would
be flushed over the user's file, silently, with a green test). The law now asserts
what it means: `Board.save` is never called, and the file's mtime does not move.

**Two of my own laws caught this batch's omissions** — the README keybinding law
(`R` bound, undocumented) and the prism-laws manifest (the prototype gained
`law_spend` upstream while this batch was in flight; recorded as QUEUED for the
approved increment 22b rather than skipped).

**Defect found and fixed in the document itself:** a completed project was being
reported "9d overdue". Nothing is expected of a closed project, so nothing about
it can be late — the same ruling the due meter obeys, now carried into the report.

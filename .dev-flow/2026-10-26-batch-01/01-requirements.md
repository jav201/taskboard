# Requirements Document — taskboard — Batch 2026-10-26-batch-01 (retroactive audit)

> **Artifact language.** Canonical English scaffold; this batch's language is English.
> **Retroactive authoring, declared:** every requirement below was written AFTER the
> implementation it audits (commit `f4b53cc`, shipped 2026-10-26 10:27 -0600), at the
> operator's order («esta vez sólo implementa… después auditas»). The source of truth for
> intent is the operator's request and the orchestrator's decisions G1–G5 (`.kimi-prompt.md`).
> Traceability here binds the shipped bytes to that intent; it does not pretend the flow ran first.

## 1. Introduction

### 1.1 Purpose

The audited change reverses the old gantt rule G-A («done folds to ✓n»): a task that reaches
DONE on the board's gantt now **keeps its row** — quiet, in the done tone, with a `✓` chip,
never rendered late — and **only archiving hides work**. The seam is a `done_rows` flag on
`gantt_plan` (`taskboard/views.py:2438`), set only by the board's gantt view (`render_gantt`,
`nav_model`, the gantt legend); every other consumer (the presentation, link mode) leaves the
flag off and is byte-identical.

### 1.2 Scope

Covers: `gantt_plan`'s row computation (`taskboard/views.py:2438-2490`), the done-row painting
(`_gantt_done_bar`, `taskboard/views.py:2842-2867`; the done branch of the task-row painter,
`:3399-3406`), the flag's three setters (`render_gantt` `:3262`, `nav_model` `:8366-8370`,
`legend_entries` `:8658-8662`), and the F-3 selection guard's comment/seat
(`taskboard/app.py:2113-2123`, `_notify_folded` `:2296-2308`).

Does NOT cover: lanes, kanban, agenda, focus, people, keys, hints (G5); the presentation
(`render_present*`, views 1/2/3, `x` exports) — byte-identical by G4; archiving itself
(unchanged: archived work never draws a row).

### 1.3 Definitions

- **G-A** — the retired rule «done folds to ✓n» (design records: `REQUIREMENTS.md`, `.dev-flow/BACKLOG.md`).
- **Quiet row** — a drawn row whose bar is entirely in the `reached` tone, whose title is dimmed
  `c(title, "reached")`, and whose right-hand chip is `✓` in that tone (no due chip, no `▲Nd`).
- **Done tail** — after a group's open rows (with its reached milestones merged by due, D-606),
  its DONE, NOT-archived, non-milestone tasks, sorted by due (G1).

## 2. Information Flow Contract (IFC)

One flow: which rows the board's gantt draws. Written retroactively; the nodes are the shipped
seats (line numbers at `f4b53cc`).

```
FLOW: the board gantt's drawn rows (done work kept, archived hidden)
  SOURCE : board.visible_tasks(show_archived) — the board file's task records (taskboard/views.py:2458)
  NODES  :
    - fn    : gantt_plan (taskboard/views.py:2438) — group open work; fold/pressure/window from open work only
      owner : HLR-3003
      in    : board + show_archived + selected_id + today + body_rows + focus/previous/pinned + done_rows
      out   : list[GanttGroup] — rows, open/rest counts, unfolded flags (G3 unchanged)
    - fn    : gantt_plan done_tail (taskboard/views.py:2473-2482) — the DONE, not-archived, non-milestone filter, computed only when done_rows is set
      owner : LLR-3001.1
      in    : the group's rest set + the done_rows flag (default False)
      out   : [] when the flag is off
    - fn    : gantt_plan done_tail append (taskboard/views.py:2485-2490) — the tail merged after the open+milestone rows, in due order, milestones excluded
      owner : LLR-3001.2
      in    : the open+milestone merge + the tail
      out   : the group's full rows tuple
    - fn    : _gantt_done_bar (taskboard/views.py:2842-2867) — the quiet bar, all reached tone, no flow packet, edge-clipped
      owner : LLR-3002.1
      in    : a done task + the axis
      out   : w cells, reached tone, no over/crit
    - fn    : _gantt_done_bar same-day branch (taskboard/views.py:2852-2857) — a one-date done task renders as a ◆ in reached
      owner : LLR-3002.2
      in    : a done task with start == due
      out   : the diamond cell in reached
    - fn    : _gantt_frame task-row painter done branch (taskboard/views.py:3399-3406) — dimmed title + ✓ chip
      owner : LLR-3002.3
      in    : a done task row + label width + chip width
      out   : the row's label, mark, cells, ✓ chip (never a due chip)
    - fn    : render_gantt / legend_entries gantt seat (taskboard/views.py:3263, :8659) — the flag's view setters
      owner : LLR-3001.3
      in    : the frame/legend call
      out   : done_rows=True — every other consumer leaves the default (G4)
    - fn    : nav_model gantt mode (taskboard/views.py:8369) — the cursor model reads the same rows
      owner : LLR-3005.1
      in    : the nav call
      out   : the flattened walk of g.rows, done rows included
  SINK   : the terminal cells of the board's gantt view and the cursor model (both read g.rows, F-3 parity)
```

Part B (crossed flows): none — no flow reads another batch's retained state; the presentation
and link mode never read this flow (byte-identical, HLR-3004).

## 3. Requirements

### US-3001 — Done work stays visible on the gantt; only archiving hides it

The operator, verbatim: «Cuando una tarea pasa a DONE (último estado) en el GANTT desaparece.
En el GANTT no quiero que desaparezca, creo que sólo deberían dejar de ser visibles sólo si
están archivadas.» As a board user I finish a task and it remains on the gantt, unmistakably
finished, until I archive it.

**Ledger:** none — written retroactively at v1; the flow follows the implementation by order of
the operator, not by defect of the record (declared in §1).

### HLR-3001 — Which rows (G1)

- **Statement:** On the board's gantt view, a group's drawn rows shall be its open rows with its reached milestones placed by date exactly as before (D-606), followed at the tail by its DONE, NOT-archived, non-milestone tasks sorted by due; a group with no open work but done work shall show its done rows, and archived tasks shall never draw a row.

**Acceptance test(s):** AT-113, AT-108 — the shipped suite's black-box ids the change restated
(`AT-3001` `tests/test_gantt.py::test_finished_work_keeps_a_quiet_row_and_the_count`
(done row kept at tail, `✓` chip, still counted in `✓n`); `AT-3002`
`tests/test_gantt.py::test_a_project_of_only_done_work_still_shows_it` (all-done project shows
its rows in due order); `AT-3005` `tests/test_archive.py::test_the_gantt_never_lists_an_archived_task`
(archived stays hidden).

**Boundary catalog:** done+archived → no row (archived wins); done milestone → D-606 seat, not
the tail; group with open work and done work → both, open first; group with only done work →
tail only.

**Negative control:** with `done_rows=False` (the default), a board with done work draws no done
row — encoded by `AT-3004`'s flag-boundary arm and the presentation byte-identity arm.

**Validation:** the change's own chunk transcripts (`evidence/scratch-evidence/suite-chunk0{0,1,2}.txt`,
3280 passed) + the audit's targeted re-runs (04-validation.md).

**Ledger:** none — v1 retroactive.

#### LLR-3001.1

`gantt_plan` computes the done tail only when `done_rows` is set; default is off.
*Trace:* `taskboard/views.py:2473-2482` (`done_tail`), `:2438` (the flag), `:2485-2490`
(rows computation).

- **Statement:** The done tail shall be computed only when `done_rows` is set, and `done_rows`
  shall default to False so every consumer that does not ask for done rows draws none.
- **Executed verification:** the flag-boundary node `tests/test_gantt_board.py::test_TC_117_done_rows_are_the_board_gantts_flag_only` (123-passed targeted run, `evidence/suite-targeted.txt`).
- **Ledger:** none — v1 retroactive.

#### LLR-3001.2

The tail is appended after the open+milestone merge, keeping due order; milestone tasks that
are done remain governed by D-606 (they are not duplicated into the tail — the tail filters
`not t.milestone`). *Trace:* `taskboard/views.py:2475-2478`, `:2485-2490`.

- **Statement:** The tail shall be appended after the open+milestone merge in due order, and
  done milestone tasks shall be excluded from it (D-606 governs them).
- **Executed verification:** the due-order arm of `tests/test_gantt.py::test_a_project_of_only_done_work_still_shows_it` (123-passed targeted run, `evidence/suite-targeted.txt`).
- **Ledger:** none — v1 retroactive.

#### LLR-3001.3

Only the board's gantt view sets the flag: `render_gantt`, `nav_model` (gantt mode), and the
gantt legend seat of `legend_entries`. No other call site passes it.
*Trace:* `taskboard/views.py:3265`, `:8370`, `:8662`; reverse census in 02-review.md (architect lens).

- **Statement:** Exactly three call sites — `render_gantt`, `nav_model`'s gantt mode, and the
  gantt legend seat — shall pass `done_rows=True`; no other `gantt_plan`/`_gantt_frame` call
  site shall pass it.
- **Executed verification:** the call-site census of 02-review.md (architect lens, executed
  read-only analysis) + the flag-boundary node (123-passed targeted run).
- **Ledger:** none — v1 retroactive.

### HLR-3002 — How a done row looks (G2)

- **Statement:** A done row shall be quiet: its bar shall use the existing `reached` tone with no flow packet, no `over`/late colouring and no critical-chain weight; its title shall be dimmed like a reached milestone's; its right-hand chip shall be `✓` in the reached tone instead of the due chip, so finished work never reads as `▲Nd` late; its dependency mark and off-window clipping shall follow the existing rules.

**Acceptance test(s):** AT-113 — the shipped black-box id (its `✓`-chip arm); `AT-3001` asserts
the `✓` chip, no `▲`, no `d ago`, dimmed title spans, and no `HEX["over"]` tone on the done row
(`tests/test_gantt.py:93-113`); `AT-3006`
`tests/test_gantt_board.py::test_AT_113_finishing_a_task_keeps_it_drawn_and_an_extra_key_is_local`
(finishing by keys keeps the task drawn and the cursor local).

**Boundary catalog:** done row inside the window; done row outside the window (clipped);
same-day start/due (diamond); done row with dependency mark.

**Negative control:** a done row carries no `crit` tone and adds nothing to the `drawn` set —
encoded in the legend census assertions (`tests/test_gantt_board.py`, `not any("critical chain"…)`
for the done-row board).

**Validation:** as HLR-3001.

**Ledger:** none — v1 retroactive.

#### LLR-3002.1

`_gantt_done_bar` paints the same geometry as an open bar but entirely in `reached`, with
`OFF_LEFT`/`OFF_RIGHT` edge markers off the window (G3 clipping).
*Trace:* `taskboard/views.py:2842-2867`.

- **Statement:** `_gantt_done_bar` shall paint the open-bar geometry entirely in the `reached`
  tone — no flow packet, no priority hue, no critical-chain weight — and shall clip off-window
  bars to the edge like any bar.
- **Executed verification:** the quiet-bar arms of `tests/test_gantt.py::test_finished_work_keeps_a_quiet_row_and_the_count` (123-passed targeted run, `evidence/suite-targeted.txt`).
- **Ledger:** none — v1 retroactive.

#### LLR-3002.2

A one-date done task renders as a `◆` diamond in `reached` at its date.
*Trace:* `taskboard/views.py:2852-2857`; census `tests/test_milestone_marks.py` (+1 line in the diff).

- **Statement:** A done task whose start equals its due shall render as a `◆` diamond in the
  `reached` tone at that date.
- **Executed verification:** `tests/test_milestone_marks.py` diamond census (62-passed
  supplemental run, `evidence/suite-targeted2.txt`).
- **Ledger:** none — v1 retroactive.

#### LLR-3002.3

The painter's done branch dims the title `c(title_markup(...), "reached")` and emits the `✓`
chip instead of `gantt_due_chip`. *Trace:* `taskboard/views.py:3399-3406`.

- **Statement:** The task-row painter's done branch shall dim the title in the `reached` tone
  and emit a `✓` chip in that tone instead of the due chip.
- **Executed verification:** the chip/dim arms of `tests/test_gantt.py::test_finished_work_keeps_a_quiet_row_and_the_count` (123-passed targeted run).
- **Ledger:** none — v1 retroactive.

### HLR-3003 — The unchanged parts (G3)

- **Statement:** The span row's `✓n` count shall stay as a summary; folding and pressure shall be computed from open work, with a group unfolding as a whole and done rows included in its height; `gantt_window` shall be computed from open work, and a done bar outside the window shall clip to the edge like any bar.

**Acceptance test(s):** `AT-3001` asserts the span keeps `✓n` alongside the done row;
`tests/test_gantt.py` colour-budget arms assert the done rows of the typical board are drawn and
the dead-cell budget still holds (`_census(out)["dead"] <= 29.5`); the fold behaviour is
asserted in `tests/test_gantt_board.py` (group height and unfold arms updated to the new law).

**Boundary catalog:** window edge — a done bar beginning/ending off-window shows the `◂`/`▸`
edge marker in `mut`, same as any bar.

**Negative control:** a done task outside the window never extends the window (window is
open-work-derived) — encoded by the frame arms at 96x30 in `tests/test_gantt.py`.

**Validation:** as HLR-3001.

**Ledger:** none — v1 retroactive.

### HLR-3004 — The presentation is NOT changed (G4)

- **Statement:** Presentation mode (`R`, views 1/2/3, `render_present*`, `x` exports) shall keep its behaviour, and where it shares `gantt_plan`/the frame seat its output shall be byte-identical — realised by the `done_rows` default (`False`) that only the board's gantt view overrides; link mode included.

**Acceptance test(s):** `AT-3004` `tests/test_gantt_board.py::test_TC_117_done_rows_are_the_board_gantts_flag_only`
(the flag boundary: board gantt draws done rows; presentation + link mode frames are
byte-identical); `AT-3003`'s presentation arm
(`tests/test_gantt_board.py::test_TC_106_nav_is_the_plans_rows_and_every_selection_is_drawn`).

**Boundary catalog:** the flag's default vs the three setters — the full call-site census is the
architect lens's deliverable.

**Negative control:** `gantt_plan(...)` with no `done_rows` argument returns rows with no done
task id — asserted inside `AT-3004`.

**Validation:** as HLR-3001; byte-identity arms inside `AT-3004`.

**Ledger:** none — v1 retroactive.

#### LLR-3004.1

Every `gantt_plan`/`_gantt_frame` call site without the flag draws no done row.
*Trace:* `taskboard/views.py:2438` (default), `:3278` (`_gantt_frame` default); reverse census
of call sites in 02-review.md (architect lens).

- **Statement:** Every `gantt_plan`/`_gantt_frame` call site that does not pass the flag shall
  draw no done row — the presentation and link mode included.
- **Executed verification:** the byte-identity arms of `tests/test_gantt_board.py::test_TC_117_done_rows_are_the_board_gantts_flag_only` (123-passed targeted run).
- **Ledger:** none — v1 retroactive.

#### LLR-3004.2

The TC-2203 golden regeneration moved ONLY the gantt frames; every other view's bytes are
identical to base_ref. *Evidence:* the regenerated
`.dev-flow/2026-10-20-batch-01/evidence/frames-base.json` diff is 8 lines (4 frames × 2 lines);
the qa lens's golden-file verdict in 02-review.md.

- **Statement:** The regenerated sealed oracle shall differ from base_ref only in the gantt
  frames — exactly 4 of 40 frames, `.plain` field only — and a HEAD regeneration shall
  reproduce the committed golden byte-exactly.
- **Executed verification:** the qa lens's golden regen at base_ref vs HEAD
  (`evidence/qa-regen-baseref.json`, `evidence/qa-regen-head.json` — verdict CLEAN).
- **Ledger:** none — v1 retroactive.

### HLR-3005 — Nothing else changes (G5) — and the cursor reaches done rows

- **Statement:** Lanes, kanban, agenda, focus, people, keys and hints shall not change; the cursor shall reach a done row by keys because `nav_model` reads the same `g.rows` the screen draws (F-3), and an archived selection shall still be moved to a drawn row by the F-3 guard.

**Acceptance test(s):** AT-108 — the shipped black-box id (entering a done task lands on drawn
work); `AT-3003` (nav is the plan's rows — done ids included in the flattened g.rows walk);
`AT-3006` (finishing keeps the task drawn, the extra key is local);
`tests/test_archive.py::test_open_work_comes_first_and_finished_work_sinks_to_the_tail`
(order).

**Boundary catalog:** selection on a done row; selection on an archived task (F-3 neighbour move);
all-done board cursor walk.

**Negative control:** no key binding, hint text, or other view's output changed — the diff census
(code-reviewer lens) confirms the touched set is exactly the 13 files.

**Validation:** as HLR-3001.

**Ledger:** none — v1 retroactive.

#### LLR-3005.1

`nav_model`'s gantt mode passes `done_rows=True` and flattens `g.rows`.
*Trace:* `taskboard/views.py:8366-8371`.

- **Statement:** `nav_model`'s gantt mode shall pass `done_rows=True` and flatten `g.rows`, so
  the cursor walk reaches the done rows the screen draws.
- **Executed verification:** `tests/test_gantt_board.py::test_TC_106_nav_is_the_plans_rows_and_every_selection_is_drawn` (123-passed targeted run).
- **Ledger:** none — v1 retroactive.

#### LLR-3005.2

The F-3 selection guard treats archived selections only; its docstring/seat updated.
*Trace:* `taskboard/app.py:2113-2123`; `_notify_folded` `:2296-2308`.

- **Statement:** The F-3 selection guard shall concern archived selections only; a selected done
  task is drawn, so the guard leaves it. (The guard's notification wording is finding AUD-02,
  open — it is records-layer, not behaviour.)
- **Executed verification:** `tests/test_gantt_board.py::test_AT_108_entering_on_a_done_task_lands_on_drawn_work` (123-passed targeted run).
- **Ledger:** none — v1 retroactive.

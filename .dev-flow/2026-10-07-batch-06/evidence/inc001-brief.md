# CHUNK — DeepSeek V4 Pro — batch 2026-10-07-batch-06 (operator-feedback), increments 001+002

You implement BOTH increments of batch-06 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`, IN THIS ORDER: (1) the kanban window markers
(small), then (2) the chain map's `○` tiles (the meaty one, including the oracle
amendment). Read the contract first: `.dev-flow/2026-10-07-batch-06/01-requirements.md`
(HLR-1201/1202, LLR-1201.1/.2, LLR-1202.1, LED-2026-10-07-batch-06.1).

## SANDBOX
- NEVER write or run anything outside the project tree: no /tmp. Scratch goes under
  `.dev-flow/2026-10-07-batch-06/evidence/`; run it with
  `env -u NO_COLOR PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-07-batch-06/evidence/<name>.py`
  from the repo root. No git. No site-packages reads.

## TASK 1 — LLR-1202.1: the kanban window markers (views.py, kanban region)

The kanban plan (`views.py`, `KanbanPlan` / the planner near line ~4720) computes
`fits` (columns that fit), `start` (window offset), `n_open`. The phase-head row is
rendered from the plan. Change:
1. When `start > 0`: render `◂` immediately before the first visible phase title
   (dim/mut tone). When `start + fits < n_open`: render `▸ N` (N exact =
   `n_open - start - fits`) immediately after the last visible title. When the
   window shows everything: NO markers (byte-identical head row to today).
2. `help_usage("kanban")` gains one bullet in "first thing to do" (or a fitting
   group), verbatim tail: `more phases than fit — the window follows the selection
   (j/k into a later column) · ◂ ▸ mark the hidden sides`.
3. New test file `tests/test_kanban_window.py`: a 4-phase fixture at a width fitting
   2 columns — assert `◂` and `▸ 2` in the head row; the selection moved to the
   last phase — assert the left marker appears and the right count drops; at a
   width fitting all 4 — assert NO markers; the help bullet string present.
   Follow the house conventions (frozen calendar seam where needed, `views.render_kanban`
   directly like `tests/test_chainmap.py` renders). RED on base: no markers exist.

Verify: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_kanban_window.py tests/test_kanban_readable.py tests/test_cells.py -q` all green.

## TASK 2 — LLR-1201.1/.2: the chain map admits every open task (the `○` tiles)

Today the chain map draws only LINKED tasks; a zero-link project draws one inert
`─▌‹project›  ‹n› open · no links ───…` row and nothing is selectable — the
operator's "es imposible crear cadenas". Change:

1. **Renderer** (`views.py`, `_chainmap_plan` / `render_chainmap`): admit every
   OPEN unlinked task of a band's project as a one-row tile at depth 0, marked
   `○` (the legend's existing "open chain head" glyph — reuse the shipped chrome of
   a chain-head row: title, due chip, late mark; NO connectors, NO meta row — one
   row per task). The tiles join the band's draw order (after the chains? place
   them AFTER the chained tasks, `○` first-in-first-out by due — state your choice
   and why in the report). The band HEAD counts stay exactly as shipped
   (`‹n› linked · ‹m› open not linked` — the tiles ARE the m). The inert
   `no links` row now renders ONLY for a project with no open work at all.
   Fold-aware: the `○` rows take part in the fold and the `+N more ↓` cap like any
   row (a band whose first row doesn't fit still drops whole; only painted rows
   reach `line_map`).
2. **Nav + seats** (`_chainmap_nav`, app): the `○` tiles enter nav at the depth-0
   column in band order — so the arrows/`j`/`k` reach them and the selection rests
   on them. `L` on any tile opens the shipped LinkPicker and applies the pick (the
   tile joins the picked chain on re-render — the shipped apply path, verify it
   handles a task whose incoming link is its FIRST). `x` unlinks as shipped and the
   task REMAINS an `○` tile (visible, re-linkable). The selection strip for an `○`
   selection names its truth: `◂ waits on  nothing yet` / `▸ unblocks  nothing waits
   on it` (use the strip's existing forms; if a form needs a small extension, make
   it and show it).
3. **`?` help** (`help_usage("chainmap")`): add a bullet: `○ an open task with no
   links yet — L starts its chain here`.
4. **THE ORACLE AMENDMENT (LED-2026-10-07-batch-06.1)** — the C-2b frames pinned
   the inert row and your tiles change them, at BOTH sizes:
   a. Render the amended frames: the TC-801 fixture (see `tests/test_chainmap.py`'s
      `_base(together=True)` — `kg_board.shifted` + Data Warehouse `together`,
      `frozen` calendar) at 118×30 and 80×24, exactly as the test renders
      (`views.render_chainmap(b, False, "tm3", TODAY, width=w, height=h).plain.split("\n")`).
   b. Write the rows to `.dev-flow/2026-10-07-batch-06/evidence/frames/C-2b-118x30.txt`
      and `C-2b-80x24.txt` (UTF-8; CRLF line endings to match the sealed frames).
   c. Point `tests/test_chainmap.py`'s `FRAMES` at the new home and note the
      amendment (one line in the file's docstring: amended under
      LED-2026-10-07-batch-06.1; the sealed batch-02 frames stay history).
   d. New arms: an unlinked task paints as `○` and is selectable; `L` on it links
      it ON the map (the picker opens, pick a predecessor, `depends_on` lands, the
      re-render shows the tile inside the chain); `x` leaves an `○` tile; the
      `no links` row only for a no-open-work project; the nav arm reaches an `○`.
      Extend `tests/test_chainmap.py` / `tests/test_chainmap_app.py` — house style.
5. **Untouched laws**: TC-803 (greyscale), TC-804 (header counts — the counts
   themselves don't change), TC-807 (hostile title), TC-808 (cycle), TC-810 (the
   cap/fold), the m/x view-dispatch, the `m` rule cycle, the C-2b 80-shed law. If
   any of them reddens, your change over-reached — stop and report.

Verify: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q` green, then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it.

## DISCIPLINE
- Minimal diffs, shipped voice, English comments, S1 (escape + clip) everywhere a
  user string paints.
- Report per task: what changed (file:line), the amended-frame story (the row
  diffs at both sizes, summarized), the new arms' results, the full-suite count,
  anything you punted.

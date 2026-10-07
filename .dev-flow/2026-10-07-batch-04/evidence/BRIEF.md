# CHUNK B — DeepSeek V4 Pro — BATCH E PROTOTYPE ROUND (the present-e worktree)

You are the prototype builder for BATCH E of the kg_mejoras plan — **project presentation
mode** — in the worktree at `C:/Users/jjgh8/Github/taskboard/.claude/worktrees/present-e`
(its own checkout; NEVER touch the main checkout at C:/Users/jjgh8/Github/taskboard).
NO git mutations of any kind.

## THE OPERATOR'S REQUEST (verbatim, batch 2026-10-04-batch-01, D-530)
"presentación de un proyecto completo: el gantt, las tareas y el texto de las tareas en
un formato apropiado para presentar; exportar SVG o una imagen de lo proyectado."

## THE PLAN'S RULING (IMPLEMENTATION-PLAN.md, batch E)
This is DESIGN WORK: a prototype round with real renders and a verdict comes first. Seeds:
the existing `R` report (self-contained HTML), G-A + AX-2 (the gantt), the details section,
the WT/SVG capture pipeline (export = the same rich save_svg). The batch's INCREMENT is
prototypes/kg_mejoras/ style: compose shipped helpers, exact height rows of width cells,
UI strings in English, a fixture board.

## READ FIRST
- `prototypes/kg_mejoras/variants_polish.py` / `variants_gantt.py` — the house prototype
  style (how the rounds built variants + frames). COPIED INTO THIS WORKTREE for you
  (read it here, not in the kg-mejoras worktree — external directories are refused).
- `prototypes/kg_mejoras/out/` — the round frames (the verdicted visual language; also here).
- `taskboard/report.py` (in THIS worktree) — the shipped `R` report's shape.
- `taskboard/views.py` — the gantt renderer + `_md`/`fit`/`c` helpers you compose.

## BUILD (in the worktree, under `prototypes/present_e/`)
Three presentation variants of ONE project (use the kg fixture — 5 projects, pick
"Website Redesign"), each rendered at 118×30 and 80×24 as `<variant>-<W>x<H>.txt` +
`.svg` (the house frame format: exact rows of width cells, `save_screenshot`-style SVGs
are NOT needed — write text frames + export SVGs via rich's export where the variant is
markup, like the kg frames):
- **PRES-A "the gantt, large"**: the project's gantt rows (the chains/spans/due chips)
  re-laid for reading across a room: bigger due chips, the task titles with their NOTES
  text under each row (the "texto de las tareas"), one section per phase.
- **PRES-B "the brief"**: a document form: the project header (name, due, counts), then
  each open task as a block — title, dates, phase, the notes paragraph wrapped to the
  width, the links line.
- **PRES-C "the hybrid"**: top half the gantt field (the visual), bottom half the brief
  blocks for the tasks ON SCREEN, a `⟦━⟧` cursor moving through them (keys ←→ move, the
  notes of the cursor'd task expand).
Rules: every untrusted string escaped+clipped (S1); the C-2b budget (accent = focus only);
width-1 glyph discipline. Export: each variant ALSO renders to a standalone `.svg` via
rich (Console(record=True) … export_svg) so the export path is proven.

## VERIFY
Each variant runs clean: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor
PYTHONIOENCODING=utf-8 python prototypes/present_e/build.py` (you write build.py) prints
the frame paths. Eyeball your own frames (print them) for width discipline.

## REPORT BACK
The variant list, the frame paths, the design decisions each variant made (what a
presentation needs that the dashboard does not), the export path proof, and your
recommendation with ONE question for the operator's verdict sheet.

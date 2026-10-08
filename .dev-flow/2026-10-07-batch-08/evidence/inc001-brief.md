# CHUNK — DeepSeek V4 Pro — batch 2026-10-07-batch-08 (templates v2), increment 001

You implement batch-08's increment 001 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`: save a chain as a template from the app.

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-08/01-requirements.md` — HLR-1401,
  LLR-1401.1.
- The seats you compose (read them): the batch-07 template store
  (`models.templates`, `models._read_template`); the `I` picker + insert
  (`app.action_templates`, `_on_template_picked`); the one-line text prompt the
  app already uses (the TextPrompt pattern — find how an existing action opens it);
  `chainmap` view-dispatch (`x`/`m` are view-dispatched there — your key follows the
  same wiring).

## SANDBOX
- NEVER write or run anything outside the project tree: no /tmp, no site-packages.
  Scratch under `.dev-flow/2026-10-07-batch-08/evidence/`; run with
  `env -u NO_COLOR PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-07-batch-08/evidence/<name>.py`
  from the repo root. No git.

## THE WORK — `taskboard/models.py`, `taskboard/app.py`, `taskboard/keymap.py`,
## `taskboard/views.py` (the chainmap keybar/help only). Plus TWO NEW test files.
## Nothing else.

1. **LLR-1401.1 — `models.chain_template(board, task_id) -> Template | None`**:
   the task's connected component through `depends_on` WITHIN ITS PROJECT — BFS both
   directions, OPEN tasks only (skip done/archived), each task once; None when the
   task is missing, done or archived. Emit a template whose order is topological
   (every `wait` points backward): walk the component sorting so predecessors come
   first (the house has `sort_by_due` and the chain map's own ordering — pick a
   deterministic order and state it; a task with MULTIPLE predecessors keeps the
   FIRST encountered as its `wait`, the rest are dropped — the template shape cannot
   hold a fan-in). Titles/notes verbatim.
2. **The key** — `,` (comma), VIEW-DISPATCHED on the chain map only
   (`Key(",", ",", "chain_template_save", "Save chain tpl", views=("chainmap",),
   group="chains")` — find the right group; the keybar re-derives). In
   `app.action_chain_template_save`: require the chain map with a selected tile
   (nothing selected -> the shipped refusal style, one line, `markup=False`);
   `chain_template(board, sel)`; None -> a toast saying the selection carries no
   open chain; else open the one-line TextPrompt for the NAME (prefill the chain's
   first task title, selected); on submit: append `{"name", "tasks"}` to
   `settings["templates"]` (create the list), save the board, toast EXACTLY
   `Template '<name>' saved — <N> tasks` (`markup=False`); esc/empty cancels, NOTHING
   written. NOT an undo step (settings, not tasks — declare in the docstring). The
   saved template lists in the `I` picker immediately (it already reads
   `settings.templates` — verify, no change expected).
3. **Tests** (new files):
   - `tests/test_template_save.py` — the unit arms: both-direction BFS (a mid-chain
     task saves the whole component); the fan-in drop (a task with two predecessors
     saves ONE wait — and a ROUND-TRIP arm: `templates()` reads it back, and feeding
     it through the insert logic's link builder reproduces a CHAIN not a diamond);
     the single-task degenerate case; None for done/archived/missing.
   - `tests/test_template_save_app.py` — the app arms (house pilot pattern; the
     batch-06 seams: frozen calendar not needed here, but the conftest milestone
     seam applies): on the chain map with a selected tile, `,` opens the name
     prompt; typing a name + enter saves (settings.templates holds the entry; the
     toast equals the pinned literal); `I` then lists it; esc leaves
     `settings.templates` byte-identical; an unlinked `○` tile saves a one-task
     template. File docstring carries `AT-1401` (dash form).

## DISCIPLINE
- First: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_template_save.py tests/test_template_save_app.py -q` green, then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it (check the key you chose is FREE first — `grep 'Key(","' taskboard/keymap.py` must be 0 before you write it).
- S1 everywhere; minimal diffs; shipped voice; English comments.

## REPORT BACK
Per item: what changed (file:line), the ordering/drop decisions, the test results,
the full-suite count, anything you punted.

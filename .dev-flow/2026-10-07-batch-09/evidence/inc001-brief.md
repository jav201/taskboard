# CHUNK — DeepSeek V4 Pro — batch 2026-10-07-batch-09 (templates v3: scratch authoring)

You implement batch-09's increment 001 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`: author a template from scratch in the app.

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-09/01-requirements.md` — HLR-1501,
  LLR-1501.1.
- The seats you compose (read them): the batch-07 `I` picker
  (`app.action_templates`, the picker modal in modals.py, `_on_template_picked`);
  the batch-08 save (`app._on_chain_template_named` — the settings append + the
  pinned toast `Template '<name>' saved — <N> tasks`); the store validation
  (`models._read_template` / `templates`); the app's text-editing patterns
  (how the setup/project editors collect text — pick the LIGHTEST house-consistent
  composition; a Textual TextArea is fine if the app already ships one — check).

## SANDBOX
- NEVER write or run anything outside the project tree: no /tmp, no site-packages.
  Scratch under `.dev-flow/2026-10-07-batch-09/evidence/`; run with
  `env -u NO_COLOR PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-07-batch-09/evidence/<name>.py`
  from the repo root. No git.

## THE WORK — `taskboard/modals.py` (the editor), `taskboard/app.py` (the wiring),
## `taskboard/views.py` (the `?` bullet only). Plus ONE NEW test file. Nothing else.

1. **The picker row**: the `I` picker's list gains `New template...` as the FIRST
   option (before user templates and presets; it is not a template — the app
   recognizes it and routes to the editor instead of inserting).
2. **The editor modal**: a small modal with ONE name field and ONE multi-line tasks
   field (one task per line); Save/esc semantics per the contract: lines are trimmed,
   empty lines skipped, the emitted template is the LINEAR chain (task i waits on
   i-1; task 0 waits on nothing); an all-empty edit (blank name or zero task lines)
   saves NOTHING and toasts one line saying why; esc cancels, nothing written.
   On save: append through the same settings seam the batch-08 save uses, `save()`,
   toast the EXACT batch-08 literal `Template '<name>' saved — <N> tasks`
   (title="Templates", `markup=False`). NOT an undo step (docstring, the batch-08
   rule).
3. **The `?` bullet**: the templates help/help_usage line notes that `I` inserts and
   `New template...` authors; notes stay JSON-only at this version (one clause).
4. **Tests** — `tests/test_template_new.py` (new; docstring carries `AT-1501` in
   dash form): the picker lists `New template...` first; the editor saves a linear
   chain from multi-line input with blank lines skipped (assert the exact
   `depends_on` wait indices after an `I` insert round-trip); the toast equals the
   pinned literal; all-empty saves nothing (settings byte-identical); esc writes
   nothing; a single-task line works.

## DISCIPLINE
- First: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_template_new.py -q` green, then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it (G-011, the clipboard flake, is a KNOWN declared environmental failure — name it and move on).
- S1 everywhere (titles are user text); minimal diffs; shipped voice; English comments.

## REPORT BACK
What changed (file:line), the editor composition you chose and why, the test
results, the full-suite count, anything you punted.

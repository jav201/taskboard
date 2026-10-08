# CHUNK — DeepSeek V4 Pro — batch 2026-10-07-batch-07 (templates), increment 001

You implement batch-07's increment 001 in the MAIN checkout at
`C:/Users/jjgh8/Github/taskboard`. Process/chain templates insertable into a project.

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-07/01-requirements.md` — HLR-1301,
  LLR-1301.1 (the store), LLR-1301.2 (the insert).
- The patterns you compose (read them): the LinkPicker family (`taskboard/modals.py`,
  how `L` opens it and applies a pick in `app.py`); the milestones ONE-step undo
  (`app.action_undo`'s `"milestones"` branch — your insert pushes ONE entry with all
  created ids, and undo removes them all); `action_present`'s project resolution
  (`present_project_id`); the `?` help shape (`views.help_usage`).

## SANDBOX
- NEVER write or run anything outside the project tree: no /tmp, no site-packages.
  Scratch under `.dev-flow/2026-10-07-batch-07/evidence/`; run with
  `env -u NO_COLOR PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-07-batch-07/evidence/<name>.py`
  from the repo root. No git.

## THE WORK — `taskboard/models.py`, `taskboard/app.py`, `taskboard/keymap.py`,
## `taskboard/views.py` (help_usage only), `taskboard/modals.py` (the picker modal,
## modeled on the LinkPicker). Plus TWO NEW test files. Nothing else.

1. **LLR-1301.1 — the store** (`models.py`): `settings["templates"]` = a list of
   `{"name": str, "tasks": [{"title": str, "notes"?: str, "wait": int|null}]}`. Provide
   the read as a small public helper (e.g. `templates(board) -> list[Template]` named
   your way, document it): lenient — skip malformed entries (non-text name, empty
   title, non-list tasks, bad task fields); a `wait` that is not a valid earlier index
   reads as `None` (the task is kept, the link dropped). Ship TWO factory presets in
   code (always available, listed AFTER user templates):
   - `Simple chain`: Plan -> Build -> Ship (a 3-chain, each waits on the previous).
   - `Bugfix`: Triage -> Fix -> Verify (same shape).
   Each picker row shows the name + task count.
2. **LLR-1301.2 — the insert**:
   - `keymap.py`: `Key("I", "I", "templates", "Templates", group="misc", bar=False)`
     (global, palette-only — add `"templates"` to the app's action list in app.py the
     way `"present"` is listed).
   - `app.py` `action_templates`: resolve the target project EXACTLY like
     `action_present` does (selected task's project; the focused project when set; none
     -> the toast `No project to insert into.`, title="Templates", `markup=False`).
     Push a picker modal (model it on the LinkPicker: same chrome, an OptionList of
     `name — N tasks`, esc closes).
   - On a pick: create the tasks in the board's FIRST phase, NO dates, ids generated
     (the house id seam), titles/notes from the template; link them per `wait`
     (forward-only; a dropped `wait` = unlinked); select the FIRST created task; push
     ONE undo entry holding every created id (the milestones pattern — undo restores by
     removing them all); save; refresh; toast EXACTLY
     `Inserted '<name>' — <N> tasks into <project>` (the project's NAME, title="Templates",
     `markup=False`). An EMPTY template (0 tasks) inserts nothing and toasts
     `Template '<name>' is empty.` instead.
   - `views.help_usage`: the kanban (or a general) bullet naming `T` and documenting
     that v1 edits templates in the board's JSON (`settings.templates`) — one line.
3. **THE TESTS** (new files):
   - `tests/test_templates.py` — store arms: round-trip (write settings.templates, read
     back equal); lenient read (a junk list -> only valid entries, malformed `wait`
     dropped); presets present with the exact names and counts; boundary: no user
     templates -> presets only.
   - `tests/test_templates_app.py` — app arms (the house pilot pattern): `T` opens the
     picker listing presets with counts; pick `Simple chain` on a board with a selected
     task -> 3 tasks created in that task's project, first phase, no dates,
     `depends_on` exactly the forward chain; the toast equals the pinned literal; `u`
     removes ALL 3 in one step; a second `u` -> "Nothing to undo."; the no-project arm
     (a board with no selection resolvable -> the refusal toast); a user template in
     `settings.templates` lists BEFORE presets and inserts with its links; an empty
     template -> the `is empty` toast. File docstring carries `AT-1301` (dash form).

## DISCIPLINE
- The suite stays green: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests/test_templates.py tests/test_templates_app.py -q` first, then the FULL suite once — report the count; if anything outside your files reddens, STOP and name it.
- S1 everywhere (titles are user text into markup — escape+clip via the shipped seams).
- Minimal diffs, shipped voice, English comments.

## REPORT BACK
Per LLR: what changed (file:line), the picker/insert flow, the test results, the
full-suite count, anything you punted.

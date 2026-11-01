# E4 build task — group V

You implement an APPROVED design. The design is a Code-Wire graph; follow it exactly. You do NOT write or
edit tests. You touch ONLY `taskboard/views.py`. Other implementers edit models.py, keymap.py and app.py at the same time: never touch them. Names
they provide (see `graph-interfaces.cw.md`) you import with the exact contracts written there.

Working directory: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (git worktree; do not commit, run no
git command that changes state). Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (your shell `python` is
3.14 — never use it). Textual is 8.2.8: its source is under `C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/`.

## Read first (folder `.dev-flow/2026-11-01-v3-incL/`)
- `graph-interfaces.cw.md` — the shared contracts.
- `graph-proto-V.cw.md` — your group's nodes: every `func:` and `examples:` line is binding (exact strings, widths, styles).
- `01-requirements.md` — the LLRs your nodes cite in `req:`.
- `03-pdr-rulings.md` (rounds 0 and 1) — rulings override anything older; `e4-addenda.md` — apply the items that touch your file.
- `graph-baseline.cw.md` / `baseline-notes.md` — the code as it was.

## Rules
- Text shown to the user is built from Rich `Text` pieces, never from markup with board text in it.
- Keep all existing behaviour. Match the file's style: docstrings explain WHY and cite requirement ids (e.g. `(Inc L, LLR-4304.2)`).
- No new dependency. Synthetic data only; never a real person's name.
- When you cannot follow the graph, do not improvise silently: append a line to
  `.dev-flow/2026-11-01-v3-incL/e4-deviations.md` (`DEV-V-n: node · what the graph says · what you did · why`).

## Self-check before you finish (no test writing)
- C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard, taskboard.views as v; print(taskboard.__file__); print(v.state_boxes([\"Backlog\",\"Doing\",\"Review\",\"Done\"], \"Doing\"), v.added_moment(\"2026-10-31T18:20:00+00:00\"))"` → `■■□□ None`.
- `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_all_agenda.py tests/test_highlight_segments.py tests/test_colour_notes.py` — report the result.

Finish with a short summary: functions/classes added or changed with line numbers, deviations (or "none").

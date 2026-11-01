# E4 build task — group S

You implement an APPROVED design. The design is a Code-Wire graph; follow it exactly. You do NOT write or
edit tests. You touch ONLY `taskboard/inbox.py` (new file). Other implementers edit the other Inc K files at the same time: never
touch them. Names they provide (see `graph-interfaces.cw.md`) you import with the exact contracts written there.

Working directory: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (git worktree; do not commit, run no
git command that changes state). Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (your shell `python` is
3.14 — never use it). Textual is 8.2.8: its source is under `C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/`.

## Read first (folder `.dev-flow/2026-11-01-v3-incK/`)
- `graph-interfaces.cw.md` — the shared contracts.
- `graph-proto-S.cw.md` — your group's nodes: every `func:` and `examples:` line is binding (exact strings, widths, styles, caps).
- `01-requirements.md` — the LLRs your nodes cite in `req:`.
- `00-orchestrator-rulings.md` and `03-pdr-rulings.md` (all rounds) — rulings override anything older; `e4-addenda.md` — apply the items that touch your files.
- `graph-baseline.cw.md` / `baseline-notes.md` — the code as it was at `545c18a`.

## Rules
- Text shown to the user is built from Rich `Text` pieces, never from markup with note or board text in it.
- Keep all existing behaviour. Match the repo's style: docstrings explain WHY and cite requirement ids (e.g. `(Inc K, LLR-4407.3)`).
- No new dependency. Synthetic data only; never a real person's name.
- When you cannot follow the graph, do not improvise silently: append a line to
  `.dev-flow/2026-11-01-v3-incK/e4-deviations.md` (`DEV-S-n: node · what the graph says · what you did · why`).

- inbox.py imports from `taskboard.models`, `taskboard.boards`, `taskboard.history` only (never `app`, never `suggest`).

## Self-check before you finish (no test writing)
- `C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard, taskboard.inbox as i; print(taskboard.__file__); print(i.note_count('a\n____\n'), i.is_divider('____  '), i.is_divider(' ____'))"` → the worktree path, `2 True False`.
- Run 3 of your graph's examples by hand in a scratch script under `%TEMP%` (Path.home redirected to a temp folder) and report them.

Finish with a short summary: functions/classes added or changed with line numbers, deviations (or "none").

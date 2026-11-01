# E4 build task — group T

You implement an APPROVED design. The design is a Code-Wire graph; follow it exactly. You do NOT write or
edit tests. You touch ONLY `taskboard/suggest.py` (new file). Other implementers edit the other Inc K files at the same time: never
touch them. Names they provide (see `graph-interfaces.cw.md`) you import with the exact contracts written there.

Working directory: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (git worktree; do not commit, run no
git command that changes state). Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (your shell `python` is
3.14 — never use it). Textual is 8.2.8: its source is under `C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/`.

## Read first (folder `.dev-flow/2026-11-01-v3-incK/`)
- `graph-interfaces.cw.md` — the shared contracts.
- `graph-proto-T.cw.md` — your group's nodes: every `func:` and `examples:` line is binding (exact strings, widths, styles, caps).
- `01-requirements.md` — the LLRs your nodes cite in `req:`.
- `00-orchestrator-rulings.md` and `03-pdr-rulings.md` (all rounds) — rulings override anything older; `e4-addenda.md` — apply the items that touch your files.
- `graph-baseline.cw.md` / `baseline-notes.md` — the code as it was at `545c18a`.

## Rules
- Text shown to the user is built from Rich `Text` pieces, never from markup with note or board text in it.
- Keep all existing behaviour. Match the repo's style: docstrings explain WHY and cite requirement ids (e.g. `(Inc K, LLR-4407.3)`).
- No new dependency. Synthetic data only; never a real person's name.
- When you cannot follow the graph, do not improvise silently: append a line to
  `.dev-flow/2026-11-01-v3-incK/e4-deviations.md` (`DEV-T-n: node · what the graph says · what you did · why`).

- suggest.py imports no taskboard module except what the graph names (it is pure).

## Self-check before you finish (no test writing)
- `C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard, taskboard.suggest as s; print(taskboard.__file__)"`.
- Reproduce the graph's executed examples (fixture F) in a scratch script under `%TEMP%` and report each value against the graph: N1 → Eval harness, the AT-4402 note → `Module 4 · Volumes` 0.668 with why `volume · oracle · script`.

Finish with a short summary: functions/classes added or changed with line numbers, deviations (or "none").

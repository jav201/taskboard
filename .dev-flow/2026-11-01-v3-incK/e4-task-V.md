# E4 build task — group V

You implement an APPROVED design. The design is a Code-Wire graph; follow it exactly. You do NOT write or
edit tests. You touch ONLY `taskboard/app.py`, `taskboard/keymap.py` and `README.md` (the `n` row only). Other implementers edit the other Inc K files at the same time: never
touch them. Names they provide (see `graph-interfaces.cw.md`) you import with the exact contracts written there.

Working directory: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (git worktree; do not commit, run no
git command that changes state). Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (your shell `python` is
3.14 — never use it). Textual is 8.2.8: its source is under `C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/`.

## Read first (folder `.dev-flow/2026-11-01-v3-incK/`)
- `graph-interfaces.cw.md` — the shared contracts.
- `graph-proto-V.cw.md` — your group's nodes: every `func:` and `examples:` line is binding (exact strings, widths, styles, caps).
- `01-requirements.md` — the LLRs your nodes cite in `req:`.
- `00-orchestrator-rulings.md` and `03-pdr-rulings.md` (all rounds) — rulings override anything older; `e4-addenda.md` — apply the items that touch your files.
- `graph-baseline.cw.md` / `baseline-notes.md` — the code as it was at `545c18a`.

## Rules
- Text shown to the user is built from Rich `Text` pieces, never from markup with note or board text in it.
- Keep all existing behaviour. Match the repo's style: docstrings explain WHY and cite requirement ids (e.g. `(Inc K, LLR-4407.3)`).
- No new dependency. Synthetic data only; never a real person's name.
- When you cannot follow the graph, do not improvise silently: append a line to
  `.dev-flow/2026-11-01-v3-incK/e4-deviations.md` (`DEV-V-n: node · what the graph says · what you did · why`).

- app.py imports `taskboard.inbox` and `taskboard.suggest` by the interface names; those files are being written in parallel — code against the contracts.
- Every pad key is a priority binding (ruling P-V-2); the divider key is `alt+l`, `alt+enter` is not bound (R1-1); the name field's board cycle is `tab` (P-V-1).

## Self-check before you finish (no test writing)
- `C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard, taskboard.app as a, taskboard.keymap as k; print(taskboard.__file__); print([x.keys for x in k.KEYMAP if x.action=='capture'])"`.
- `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_keymap.py tests/test_help_keys.py tests/test_modal_keys.py tests/test_added_list.py` — report the result (a failure ONLY because inbox.py/suggest.py are not finished yet, or TC-2407's INVENTORY lacking `ReviewList` (the tester adds it), is expected: say so).

Finish with a short summary: functions/classes added or changed with line numbers, deviations (or "none").

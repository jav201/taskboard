# E2b prototype task — one group of Inc K (shared brief)

You write the functional design of ONE file-ownership group as a Code-Wire graph — contracts and
concrete examples taken from the requirements — BEFORE any code exists. You write NO code: never edit
`taskboard/` or `tests/`, never put stubs or marks in the source. You may run read-only probes (python
-c against the worktree, cwd = worktree, print `taskboard.__file__`). English only. Synthetic data only;
never a real person's name (owner placeholder `username_subject`).

Worktree: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (do not commit, no state-changing git).
Interpreter: `C:/Users/jjgh8/anaconda3/python.exe`. Textual 8.2.8 source:
`C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/`.
Folder: `.dev-flow/2026-11-01-v3-incK/`.

## Read first
- `01-requirements.md` (TC numbering rule in its header) and `01-requirements-ledger.md`.
- `graph-interfaces.cw.md` — the seams. You do NOT edit it. If a seam is wrong or missing, write a
  `## Findings` entry `finding P-<G>-n …` in YOUR file with `seen:` and a proposed change; the orchestrator rules.
- `graph-baseline.cw.md` + `baseline-notes.md` — the code as it is at `545c18a`. Write only the
  DIFFERENCES: new nodes, and changed nodes (say `changed from baseline:` in `func`).
- Grammar: `C:/Users/jjgh8/Github/code-wire/docs/Notation-Grammar.md`. Model of depth and style:
  `.dev-flow/2026-11-01-v3-incC/graph-proto-V.cw.md` (and M1/M2).
- `00-orchestrator-rulings.md` (R0, R1, R2) — the orchestrator's rulings; they override older text.
- Design source for the screen: `prototypes/capture_round/proto.py` variant A (`PadScreen`, `Inbox`,
  `dump`, `undo_dump`, `hit_text`, `options`, lines ~100-470) and variant C's review (`ReviewScreen`,
  ~743-830); `prototypes/capture_round/suggest.py` (TF-IDF); captures (Read as images)
  `prototypes/capture_round/out/png/cap-A_118x30.png`, `cap-A-dump_*`, `cap-A-new_*`, `cap-C-rev_*`
  (both sizes). The operator's deltas: the `____` divider drawn as a full-width rule, the hint row, the
  empty-pad ghost and the one-time notice; the divider key is `alt+l` (R1-1), not `alt+enter`.

## What to write — `graph-proto-<G>.cw.md`
- Every node: `req:` (the LLR ids it serves), `in:`/`out:`, `func:` precise enough that an implementer
  needs no guess (exact strings, widths, styles by `HEX[...]` key, ordering, failure handling), `module:`,
  `modify:` for data it writes, and `examples:` lines with the TC id of the test that will check it — exact
  input → exact expected output. Every LLR of your group gets ≥ 1 concrete example.
- `## Entities` / `## Edges` for what your nodes read and write.
- `## Findings` for every gap, contradiction or risk you find in the requirements or interfaces
  (`finding P-<G>-n <title>` / `anchor:` / `seen:` / `decision: proposed — …`).
- Run `C:/Users/jjgh8/anaconda3/python.exe C:/Users/jjgh8/Github/code-wire/tools/codewire_lint.py <file>`
  until exit 0 with `not read=0`.
- List at the end of your file, under `## Seams`, each call you make into another group's node and each
  call another group must make into yours.

Return ≤ 10 lines: node count, LLRs covered (and any of your group's LLRs left without an example),
findings count with one line each for MAJOR ones, lint result.

## Group notes
- **G-S** owns `taskboard/inbox.py` (new). **G-T** owns `taskboard/suggest.py` (new). **G-V** owns
  `taskboard/app.py`, `taskboard/keymap.py` and the README `n` row.
- **G-V:** Textual's TextArea line render is private API. Before you fix the divider-rule mechanism
  and the empty-pad ghost, prove them with a read-only probe script placed under `%TEMP%` (never in the
  repo) that mounts the subclass in a Textual pilot at 118x30 and asserts the rendered line; cite the
  probe and its output in the node's `func:`. Same for any `alt+…` key you rely on inside a TextArea
  (does the TextArea consume it before the screen binding?).
- **G-S:** untrusted inputs are the file `inbox.json` (any JSON, any size), note text, image names.
  State the caps and the rejection rule for each in `func:`.

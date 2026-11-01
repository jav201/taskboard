# E2b prototype task — one group of Inc L (shared brief)

You write the functional design of ONE file-ownership group as a Code-Wire graph — contracts and
concrete examples taken from the requirements — BEFORE any code exists. You write NO code: never edit
`taskboard/` or `tests/`, never put stubs or marks in the source. You may run read-only probes (python
-c against the worktree, cwd = worktree, print `taskboard.__file__`). English only. Synthetic data only;
never a real person's name (owner placeholder `username_subject`).

Worktree: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (do not commit, no state-changing git).
Interpreter: `C:/Users/jjgh8/anaconda3/python.exe`. Textual 8.2.8 source:
`C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/`.
Folder: `.dev-flow/2026-11-01-v3-incL/`.

## Read first
- `01-requirements.md` (63 LLRs, 5 ATs; TC numbering rule in its header) and `01-requirements-ledger.md`.
- `graph-interfaces.cw.md` — the seams. You do NOT edit it. If a seam is wrong or missing, write a
  `## Findings` entry `finding P-<G>-n …` in YOUR file with `seen:` and a proposed change; the orchestrator rules.
- `graph-baseline.cw.md` + `baseline-notes.md` — the code as it is at `eb411e1`. Write only the
  DIFFERENCES: new nodes, and changed nodes (say `changed from baseline:` in `func`).
- Grammar: `C:/Users/jjgh8/Github/code-wire/docs/Notation-Grammar.md`. Model of depth and style:
  `.dev-flow/2026-11-01-v3-incC/graph-proto-V.cw.md` (and M1/M2).
- Design source for the screen: `prototypes/capture_round/proto.py` `all_rows`, `ordered`, `when`,
  `day_head`, `meta`, `proj_chip`, `source_line`, `ListBase`, `ListB` (lines ~825–1145) and the capture
  `prototypes/capture_round/out/png/ls-B_118x30.png` / `_80x24.png` (Read them as images). The
  operator's deltas: the state column between the time label and the project bar; the archived toggle.

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

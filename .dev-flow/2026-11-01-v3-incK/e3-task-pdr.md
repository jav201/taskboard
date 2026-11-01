# E3 PDR task — code-free design review of Inc K (shared brief)

You review a DESIGN, not code: there is no implementation yet. The design is a Code-Wire graph plus strict
EARS requirements. English only. Synthetic data only (owner placeholder `username_subject`). You never edit
`taskboard/`, `tests/` or the design files; you write ONE review file. Read-only probes are welcome:
scratch scripts under `%TEMP%/incK-pdr-<role>/`, interpreter `C:/Users/jjgh8/anaconda3/python.exe -I`,
cwd = the worktree, print `taskboard.__file__` (the editable install points at the main checkout, so put the
worktree first on `sys.path`). Mark each claim `executed` (probe ran) or `read` (from text).

Worktree: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (head has the design commits; base code `545c18a`).
Folder: `.dev-flow/2026-11-01-v3-incK/`.

## Read
- Your role file (path in your prompt).
- `.dev-flow/COMMISSION-capture-list-colour.md` §Inc K (K-1..K-6) — the operator's scope.
- `00-orchestrator-rulings.md` and `03-pdr-rulings.md` — rulings override older text.
- `01-requirements.md` + `01-requirements-ledger.md`.
- `graph-interfaces.cw.md`, `graph-proto-S.cw.md` (inbox.py), `graph-proto-T.cw.md` (suggest.py),
  `graph-proto-V.cw.md` (app.py, keymap.py, README), `e2-trace.txt`.
- `graph-baseline.cw.md`, `baseline-notes.md` and the real callers in `taskboard/` at base.

## Write `03-pdr-<role>.md` (model: `.dev-flow/2026-11-01-v3-incL/03-pdr-architect.md` / `03-pdr-security.md`)
- First line: `**Verdict: PASS | PASS-WITH-NOTES | FAIL**` with counts by severity (HIGH, MAJOR, MEDIUM, MINOR/LOW, INFO).
- Each finding: id (`ARCH-n` / `SEC-n`), severity, anchor (file + node or LLR id), what is wrong, evidence
  (`executed`/`read`), and a proposed change. Prefer removing a feature over guarding it.
- FAIL only for an open HIGH or MAJOR.
- A "checked and sound" list so the orchestrator can see coverage.

Return ≤ 10 lines: verdict, counts, one line per HIGH/MAJOR.

# E4 build task — group V (views.py, report_deck.py, report_workspace.py, README.md)

You implement an APPROVED design. The design is a Code-Wire graph; follow it exactly. You do NOT write
or edit tests. You touch ONLY these files: `taskboard/views.py`, `taskboard/report_deck.py`,
`taskboard/report_workspace.py`, `README.md`. Another implementer edits `taskboard/modals.py` at the same
time: never touch it.

Working directory: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (git worktree; do not commit, do
not run git commands that change state). Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (your shell
`python` is 3.14 — never use it).

## Read first
- `.dev-flow/2026-11-01-v3-incC/graph-interfaces.cw.md` — the shared contracts (`PEN_CODES`, `Span`,
  `colour_spans`, `highlight_segments`). Names, field order and signatures are binding: modals.py imports them.
- `.dev-flow/2026-11-01-v3-incC/graph-proto-V.cw.md` — your nodes: `colour_spans` (the algorithm in
  `func:` and the notes, LINEAR time: cache the next match of each kind, re-search only when the scan
  passes it), `highlight_segments` (derived from `colour_spans`, signature unchanged), `legend_entries`
  focus rows, deck CSS (`.hl-orange/.hl-blue/.hl-violet` + variables in LIGHT and dark blocks with the
  hexes the graph gives), workspace CSS (3 classes + 3 `:root` variables like `.hl-soon`), README lines.
  Every `examples:` line is an exact expected value.
- `.dev-flow/2026-11-01-v3-incC/01-requirements.md` §4.1, §4.2, §4.6 (LLR-4201.n, 4202.1–.8, 4206.n).
- `.dev-flow/2026-11-01-v3-incC/03-pdr-rulings.md` — rulings override anything older.

## Rules
- Keep `_HIGHLIGHT_RE` exported and unchanged (a frozen-oracle test imports it).
- No new dependency. Match the file's style (docstrings explain why, cite the requirement ids).
- `PEN_CODES` and `Span` (a `NamedTuple`) live in views.py next to `highlight_segments`.
- Do not change `notes_text`, `_highlight_markup`, `present_note_lines` (the graph says they need no change).
- When you cannot follow the graph, do not improvise silently: append a line to
  `.dev-flow/2026-11-01-v3-incC/e4-deviations.md` (`DEV-V-n: node · what the graph says · what you did · why`).

## Self-check before you finish (no test writing; run these one-liners)
`C:/Users/jjgh8/anaconda3/python.exe -c "from taskboard.views import highlight_segments as h, colour_spans as c; print(h('a ::b:: x :: c')); print(h('::b:: x ::r:: y ::')); print(h('std::vector')); print(c('a ::b:: x :: c'))"`
must print exactly the graph's values. Then `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q tests/test_highlight_segments.py tests/test_report_html.py -p no:cacheprovider` must pass.

Finish with a short summary: functions added/changed with line numbers, deviations (or "none").

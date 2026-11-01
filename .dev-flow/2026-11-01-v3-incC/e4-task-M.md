# E4 build task — group M (taskboard/modals.py: pens, live ink, colour palette, details label)

You implement an APPROVED design. The design is a Code-Wire graph; follow it exactly. You do NOT write
or edit tests. You touch ONLY `taskboard/modals.py`. Another implementer edits `taskboard/views.py`
at the same time: never touch it. It will provide `PEN_CODES`, `Span`, `colour_spans` and the new
`highlight_segments` with the exact contracts of `graph-interfaces.cw.md` — import them from `.views`.

Working directory: `C:/Users/jjgh8/Github/taskboard-wt/capture-proto` (git worktree; do not commit, do
not run git commands that change state). Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` (your shell
`python` is 3.14 — never use it). Textual is 8.2.8: read its source under
`C:/Users/jjgh8/anaconda3/Lib/site-packages/textual/` when the graph names an internal.

## Read first
- `.dev-flow/2026-11-01-v3-incC/graph-interfaces.cw.md` — shared contracts, incl. `TaskModal.check_action`,
  `TaskModal._pen_span`, `TaskModal._lift_pen`, `[Data: TaskModal.pen]`.
- `.dev-flow/2026-11-01-v3-incC/graph-proto-M1.cw.md` — pens and live ink: the ESC-digit parser fix at
  import, BINDINGS (alt+1..alt+6 → pen(i), alt+0 → pen off, enter → pen_enter AFTER drop_pick), the one
  Notes label form (`pen_label`/`_pen_label`, ≤ 38 cells), `action_pen` (with its refusals and the
  visible-text check), `action_pen_enter`, `_pen_follow` + `_pen_at`, `_save` (lift before reading),
  `ink_highlights` (one-pass byte offsets, surrogatepass), `InkArea` (TextArea subclass with a private
  theme copy, `_build_highlight_map` override that falls back to the base map on ANY exception).
- `.dev-flow/2026-11-01-v3-incC/graph-proto-M2.cw.md` — `action_colour`, `colour_target`, `recolour`,
  `palette_offset`, `ColourPalette` (ModalScreen; DEFAULT_CSS; no Button; keys 1–6/0/esc as priority
  bindings; rows as the graph shows), `_apply_colour` (re-validate the target; visible-text check),
  `TaskDetails.compose` label, the notices N1–N4 (exact texts in the graph).
- `.dev-flow/2026-11-01-v3-incC/01-requirements.md` §4.3–§4.5 and LLR-4202.9/.10.
- `.dev-flow/2026-11-01-v3-incC/03-pdr-rulings.md` — rulings override anything older.

## Rules
- Every label/notice/palette row is built from Text pieces or constant markup only; user text never goes into markup.
- Keep all existing behaviour: the `@` mention picker, `alt+s/m/i/t/d`, `ctrl+v`, `ctrl+e`, the preview.
- `#f-notes` keeps its id (tests query it); it becomes an `InkArea`.
- No new dependency. Match the file's style (docstrings explain why and cite requirement ids).
- When you cannot follow the graph, do not improvise silently: append a line to
  `.dev-flow/2026-11-01-v3-incC/e4-deviations.md` (`DEV-M-n: node · what the graph says · what you did · why`).

## Self-check before you finish (no test writing)
- `C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard.modals as m; print(m.recolour('the plan works', 4, 8, 'b'))"` matches the graph.
- `env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_edit_window.py tests/test_people_picker.py tests/test_modal_keys.py tests/test_people_look.py` — report the result; if `test_modal_keys` fails only because `ColourPalette` is not in its inventory, say so (the tester owns that file).

Finish with a short summary: functions/classes added/changed with line numbers, deviations (or "none").

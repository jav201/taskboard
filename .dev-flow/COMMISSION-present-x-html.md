# Commission — the presentation exports HTML; the SVG export is removed

Written by the orchestrator on 2026-11-01. Branch `feat/present-x-html` starts from `main` `2fbd5d2`. The process is **dev-flow-v3-beta**, ONE small increment: increment folder `.dev-flow/2026-11-01-v3-incX/`. The orchestrator runs every stage from the main session; there is no per-increment conductor.

## The operator's words (verbatim)

> «estoy usando export y sigue haciendo export de svg... no está el html implementado?» — then — «Vamos a eliminar el reporte svg, ya no le veo sentido ahora, y quedémonos con el html.»

## Today

- `x` in the presentation (`R`, `PresentScreen.action_export`, `taskboard/app.py` ~623) writes an SVG of the terminal frame (`views.save_present_svg` ~7354), plus a PNG through Microsoft Edge (`save_present_png`, `_find_msedge` ~7367–7385). File names come from `present_paths` (~7340), with `-split`/`-all` suffixes. View 3 uses `present_all_export` (~7656), which draws the timeline without the cursor.
- The HTML reports ship on `H`, a global key outside `R` (batch `2026-10-29-batch-01`):
  - `taskboard/report_html.py` holds the shared extraction;
  - `report_workspace.py` builds report B and `report_deck.py` builds report C;
  - the `ReportExport` modal lives in `modals.py` ~3761; `action_report_export` lives in `app.py` ~2993.
- `H` has `bar=False` in `keymap.py` ~152, so the key bar never shows it. That is why the operator never found it.

## Decisions (record each in `03-pdr-rulings.md`)

- **X-1, `x` in `R` exports HTML.** `x` writes the HTML **deck** (report C) through the same writer `H` → `c` uses. Its scope is exactly what the presentation is showing:
  - views 1 and 2: the presented project;
  - view 3 (`all`): every project shown in the curate rail, in the presentation order.

  Hidden projects and tasks (the presentation's hide flags) are excluded from the file's bytes, never merely hidden visually.

  Afterwards a toast names the path and offers `o` to open it in the browser, as `H` does. Below `PRESENT_MIN_WIDTH`, the narrow-frame rule for `x` stays as it is today.
- **X-2, the SVG/PNG export is removed.** Remove `save_present_svg`, `save_present_png`, `_find_msedge`, the PNG path, `present_paths`, and `present_all_export`, if nothing else uses them. Check every caller and test. The `-split`/`-all` SVG naming goes too.
  - Tests that pin the SVG export are deleted or rewritten to the HTML export. Justify each one in the packet.
  - README, help and hint wording: "x export" now means HTML.
  - BACKLOG items about the SVG/PNG export (the cursor in the export, Edge, PNG content) are closed as obsolete, citing this commission.
  - Keep the old static CLI report (`report.py`) as it is. It is a separate item.
- **X-3, `H` becomes discoverable.** `H report` shows in the key bar (`bar=True`, or the bar's equivalent), and the `?` help lists it. Keep the key-bar fit rules at 80 columns: if `H report` does not fit, the bar drops it the same way it drops other keys.
- **X-4, nothing else changes** in the presentation's views, keys, or hints, apart from the export wording.

## Scope and size

The expected size is under 40 LLRs and under 20 prototype nodes. The likely source files are `app.py`, `views.py`, `keymap.py`, and README. At most 4 source files.

## Evidence

- **Tests.** Run `env -u NO_COLOR python -m pytest`, with `taskboard.__file__` printed in every transcript header. Run RED with cwd set to a clean base worktree, and GREEN with cwd set to this worktree.
- **E5 scope.** Run the change-only tests PLUS the repository's law guards: `tests/test_colour_budget*.py`, `test_english.py`, `test_prism_laws.py`, `test_markup_census.py`, `test_modal_keys.py`, and the key-bar and help tests.
- **Captures.** Take real Windows Terminal captures at 118x30 and 80x24 of the key bar showing `H report`, and of the toast after `x` in `R`. Add a browser screenshot of the deck produced by `x` from view 3, with one project hidden.
  - Give each window a unique `xh-` title and close it by that title.
  - Never close any other window.
  - Launch with `cmd /c 'set NO_COLOR=& set COLORTERM=truecolor& wt.exe -w new --title <t> ...'`.
- **Batch end.** Run the full suite once, in 3 sequential chunks; the baseline is 4023 passed. Then push only on the operator's approval, and check the CI after the push.

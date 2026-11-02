# Baseline notes — the presentation's export, the `H` report flow and the key bar at 509d444

**Counts:** 22 nodes, 17 entities, 23 edges. `codewire_lint` exit 0 (0 lines not read). `codewire_marks` wrote 22 marks, 0 nodes without code. `codewire_extract --path app.py,views.py,models.py,modals.py,report_html.py,report_deck.py,keymap.py` exit **1**: 2 findings, both of kind `input_untyped_in_code` (`present_all_export.folded`, `TaskboardApp._on_report_chosen.res`). No type mismatch and no missing node. 18 calls listed; extract-baseline.txt marks each one REAL, LIFTED or COLLISION. Lines below are at 509d444 (unmarked); the lines in extract-baseline.txt are in the marked tree.

**Which tree is imported:** `pip show taskboard` gives an editable install pointing at `C:\Users\jjgh8\Github\taskboard` (the main checkout). The probe puts the cwd (incX-marks) first on `sys.path` and prints `taskboard.__file__` = `…\taskboard-wt\incX-marks\taskboard\__init__.py`. The guard run used `python -m pytest` with cwd = incX-marks and printed the same path first.

## The removal targets (X-2): every caller and every test

Found by `grep -rn` over the whole tree (`.dev-flow/` excluded) and by an AST pass over `tests/*.py` that names the enclosing top-level function of each hit.

### Product callers (taskboard/)

| Target (509d444 line) | Callers in taskboard/ | Imported by |
|---|---|---|
| `views.present_paths` (views.py:7340) | `PresentScreen.action_export` app.py:636 (view 3), app.py:639 (views 1/2) | app.py:57 |
| `views.save_present_svg` (views.py:7354) | `PresentScreen.action_export` app.py:641 | app.py:61 |
| `views._find_msedge` (views.py:7367) | `views.save_present_png` views.py:7385 only | — |
| `views.save_present_png` (views.py:7379) | `PresentScreen.action_export` app.py:642 | app.py:59 |
| `views.present_all_export` (views.py:7656) | `PresentScreen.action_export` app.py:634 | app.py:55 |

No other product module calls them: not `__main__.py` (its `--report` path calls `report_html.extract` and `write_reports` at __main__.py:213-215), not `report.py`, not `modals.py`. In views.py the only uses of `import os` (:19), `import shutil` (:21) and `import subprocess` (:22) are in these functions (os at :7360, :7370-7371; shutil at :7376; subprocess at :7394-7395), so those three imports become unused with them. `Console` stays: `_SEARCH_CONSOLE` (:4135) uses it.

Related, not named by the commission: `PresentAll.timeline` and `PresentAll.timeline_w` (views.py:7413-7417, "what `x` exports") are read by NO product code at 509d444 (`present_all_export` calls `_all_timeline` itself); only tests read them (test_present_all.py::test_TC_2103_the_frame_sweep, ::test_TC_2103_no_stop_hides_under_the_overflow_row; test_legend.py::test_TC_2608_…). They are not removal targets unless the requirements say so.

### Prototype callers (prototypes/, not product code; they break if the functions go)

- prototypes/backlog_round/proto.py:870 `views.save_present_svg`, :871 `views.save_present_png`
- prototypes/present_portfolio/app_capture.py:47 (import), :288 `save_present_svg`
- prototypes/present_views/app_capture.py:42 (import `_find_msedge`), :120 `_find_msedge()`
- text only (no call): prototypes/html_report/verdict/build.py:178, prototypes/present_portfolio/build_html.py:161, prototypes/present_views/app_capture.py:15 (docstring)

### Tests that call a target by name (10 test functions and 1 fixture in 7 files)

| Test | Targets it uses | What it pins |
|---|---|---|
| tests/test_legend.py::test_TC_2607_the_presentation_views_and_export_carry_the_strip (:583) | `save_present_svg`, `present_all_export` | the legend strip is in the exported SVG |
| tests/test_legend.py::test_TC_2608_hidden_classes_leave_the_presentations_three_views_and_exports (:671) | `save_present_svg`, `present_all_export`, `PresentAll.timeline` | hidden milestone classes leave the exports |
| tests/test_present_all.py::test_TC_2104_the_view_names_and_the_u_tail_in_views_1_2 (:686) | `present_paths` | "present-board-2026-10-19-all.svg" and a ".png" twin |
| tests/test_present_backlog_round.py `png` fixture (:56) | monkeypatches `app.save_present_png` | the seam; used by ::test_AT_2402 (:134), ::test_AT_2403 (:224), ::test_AT_2404 (:301) |
| tests/test_present_backlog_round.py::test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content (:269) | `present_all_export` | no cursor, cut at the last row, folds follow the anchor |
| tests/test_present_room.py::test_TC_1608_the_frame_and_its_export_hold_no_presenter_text (:48) | `save_present_svg` | the SVG holds no key text |
| tests/test_present_views_app.py::test_TC_1809_each_view_exports_to_its_own_file (:316) | `present_paths` | gantt has no suffix, split ends "-split" (.svg, .png) |
| tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle (:137) | `present_paths`, toast "PNG needs Microsoft Edge" | `x` writes the SVG; Edge toast; runs the REAL `save_present_png` (no stub): on this machine Edge is installed, so the test launches headless Edge |
| tests/test_tick_label.py::test_TC_1701_the_scale_pattern_sees_every_old_label (:45) | `save_present_svg` | the scale regex sees labels inside an SVG |
| tests/test_tick_label.py::test_TC_1701_no_present_frame_or_export_paints_the_scale (:235) | `save_present_svg` | no frame or export paints the old scale |

### Tests that press `x` in `R` and read the SVG files (no target named, but they pin the SVG export)

- tests/test_legend.py::test_AT_2605_hide_and_the_legend (:702; `x` at :760, :762, `reports.glob("*.svg")` :765)
- tests/test_present_all.py::test_AT_2104_three_views_one_cursor_and_the_export (:458; `x` :488, the name "present-board-2026-10-19-all.svg" :490)
- tests/test_present_backlog_round.py::test_AT_2402_the_presenter_reads_the_board_the_slide_never_does (:134; `x` :144-145, `_exports` :146)
- tests/test_present_backlog_round.py::test_AT_2403_question_mark_shows_every_key (:224; the binding pair ("x", "export") :173, `x` :233/:246, `_exports` byte compare)
- tests/test_present_backlog_round.py::test_AT_2404_the_export_reads_as_a_slide (:301; "present-board-2026-10-20-all.svg" :310)
- tests/test_present_hide.py::test_AT_1602_space_hides_and_it_is_remembered_a_shows_all (:336; `x` :370, glob "present-*.svg" :372)
- tests/test_present_note_highlights.py::test_AT_2903_split_export_svg_carries_tones (:200; `x` :211, glob "*.svg" :213)
- tests/test_present_views_app.py::test_AT_1803_the_view_keys_and_what_the_views_share (:178; `x` :240-241, the two SVG names :242-243)
- helper tests/test_present_backlog_round.py::_exports (:107) globs `present-*.svg`

### Tests that pin the `x export` wording (X-4 keeps the wording unless the requirements change it)

tests/test_present_all.py (:623, :627, :693), tests/test_present_hide.py (:230-234), tests/test_present_narrow.py (:90-97), tests/test_present_polish.py (:177-179), tests/test_present_views_app.py (:32, :266-268). They pin "x export" in the hint row, not "SVG". The `?` window row "export this view · SVG + PNG" (keymap.py:244) is pinned by no test found by grep for "SVG + PNG".

### Tests that pin `H` off the bar (X-3 changes this)

- tests/test_report_export_app.py::test_TC_3117_H_is_seated_once_off_the_bar (:238): asserts `h.bar is False` and `h in keymap.global_keys(view)` for every view.
- tests/test_help_keys.py::test_TC_1607_global_keys_are_the_live_palette_only_keys (:96): `global_keys` = the live bar=False keys (generic; moves `H` out of the global line if bar=True).
- tests/test_help_keys.py::test_AT_1603_the_help_shows_the_global_keys_without_scrolling: the `?` global line.
- tests/test_keymap.py::test_global_commands_are_palette_only_not_in_the_bar (:70): `GLOBAL_ACTIONS` (:66) does NOT hold `report_export`, so it does not block `H` going on the bar.
- tests/test_added_list.py:881 lists the global keys in seat order with "H".

### Non-code references to the targets

- REQUIREMENTS.md active LLRs that name them: LLR-1803.3 (:219), LLR-1905.1 (:229, `save_present_png` in a prototype capture), LLR-2104.1 (:245), LLR-2404.1 (:289), LLR-2903.1 (:384, "save_present_svg, present_paths and present_all_export shall stay byte-unchanged"), LLR-3107.5 (:412, "No change shall reach views.present_paths, views.save_present_svg, views.save_present_png, views.present_all_export").
- docs/ARCHITECTURE.md:42, :48 (Edge as an outside system), :70, :117, :122, :131.
- README.md:140 ("export SVG+PNG"), :189, :291-294 (`x` exports to an SVG and a PNG, `-split`, `-all`), :410 (`reports/` holds "the presentation's SVG + PNG exports").
- The PresentScreen docstring (app.py:206-226) says `x` exports SVG + PNG.
- BACKLOG.md entries found by grep for svg/png/edge that are about the export: :284 (no node asserts the marks inside the exported SVG/PNG), :326 (the PNG export asserted only as "file or the Edge toast"). The grep is not exhaustive for the commission's closure list (the cursor in the export, Edge, PNG content).

## Probes (run on incX-marks; synthetic boards in a temp folder; `USERPROFILE`/`HOME` redirected to a temp folder for the app probe; the PNG writer stubbed on `taskboard.app` in the app probe, so no Edge process ran)

Probe board: projects Alpha `pA` (present_rank 1), Beta `pB` (present_rank 0), Gamma `pC` (show_in_present False), Delta `pD` (archived); tasks a1, a2 (hidden) in Alpha, b1 in Beta, c1 in Gamma, d1 in Delta. Today 2026-11-01.

- **P-1 (`present_paths`):** "Website Redesign" → `reports/present-website-redesign-2026-11-01.svg` + `.png`; view "split" adds `-split`; project None, view "all" → `present-board-2026-11-01-all.svg`; 60 × "x" → a 40-character slug; "!!!" → slug "board".
- **P-2 (`save_present_svg`, `_find_msedge`, `save_present_png`):** the SVG is written, starts `<svg`, its title text is `taskboard&#160;·&#160;presentation`, the `reports` folder is created. `_find_msedge()` on this machine = `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`. With `_find_msedge` → None the PNG is None; with a binary that rejects Edge's flags (python) it is None and no PNG appears.
- **P-3 (`present_order`, `present_all_export`):** `present_order` = [pB, pA, pC] (board.projects [pA, pB, pC, pD]): hidden Gamma kept, archived Delta dropped. The export at 118×29 is width 93, 8 rows; Beta before Alpha; no Gamma, no "Alpha hidden", no Delta. At 90×29 (no rail) width 90.
- **P-4 (`extract`, `write_reports`, the deck):**
  - `extract` (scope all) keeps the BOARD order [#0:pA, #0:pB, #0:pC, #0:pD] and every task, the hidden a2 and the hidden project Gamma included; it reads neither `show_in_present` nor `present_rank` (grep: no `show_in_present` or `present_order` in report_html.py, report_deck.py or report_workspace.py).
  - Project scope "#0:pA" → tasks a1, a2 (the hidden one included). An unknown key → ValueError.
  - `write_reports(("deck",))` → `deck-2026-11-01.html`; project scope → `deck-main-alpha-2026-11-01.html`; kind "svg" → ValueError "unknown report kind: svg", no folder made.
  - `slide_projects` → Alpha, Beta, Gamma (archived Delta has no slide). The page holds "Gamma" and "Alpha hidden"; "Alpha" comes before "Beta"; the scope line is "All loaded boards (1): Main".
- **P-5 (keys):**
  - The `H` row: `('H', 'H', 'report_export', 'Report', universal False, priority False, views None, primary False, 'misc', bar False)`.
  - `bar_keys(view, "more")` has no H; `global_keys` = o i p P f c R A N n H @ # I S (every view).
  - `key_bar_plain(118, "swimlanes", "primary")` = "? Map  ; More  q Quit  B Boards  1 Lanes  2 Agenda  3 Gantt  4 Kanban  5 Focus  6  7  8  9  0  ↵  a  e  d  L  ⇥  ↓  ↑" (0 dropped).
  - At 118 "more": every word but "Map" gone, 0 dropped ("…  [  ]  !  b  +  -  m  ⇥  ↓  ↑  ←  →").
  - At 80 "primary": 0 dropped ("? Map  ; More  q Quit  B  1 …"). At 80 "more": 12 keys dropped, the bar ends "M +12".
  - So a bar=True `H` in group misc and not `primary` would be drawn only in the "more" layer (`;`); where it lands in the row depends on its seat position, and at 80 it is dropped with the other right-hand keys. The bar is not group-sorted: only `universal` sorts first.
  - The `?` window's x row: "export this view · SVG + PNG" (OUT).
- **P-6 (app, headless, `--open` board "Main"):**
  - `R` on a1 at 118×31, `x` → the warning toast "Exported present-alpha-2026-11-01.svg to <folder> — PNG needs Microsoft Edge". In split the name ends `-split.svg`; in view 3 it is `present-board-2026-11-01-all.svg`. No board write, no `o` offer.
  - **`H` while `R` is open does nothing** (the stack stays [Screen, PresentScreen]). **`o` while `R` is open does nothing**: a live `_report_offer` is not used and stays set. The cause is Textual 8.2.8: `App.check_bindings` uses `screen._modal_binding_chain` for non-priority keys, and that chain stops at the top ModalScreen. PresentScreen is a ModalScreen, and the app's `H` and `o` are not priority. test_TC_3120 already pins "an `o` over another screen leaves the offer for the main screen".
  - `H` on the main screen → ReportExport, scope "all", project ("Alpha", "Main"), boards ["Main"]. `p` → scope "project". `c` → the toast "Report written: deck-main-alpha-2026-11-01.html\n<folder>\no opens it (10 s)" (title Report, information). Then `o` → `_open_report(deck-main-alpha-2026-11-01.html)`.
  - At 30×20 `R`, `x` → the toast "Widen the terminal to 36+ columns to export", no file.

## Facts the requirements depend on

- **Scope today vs X-1:** the deck writer's scope input is `extract(boards, …, project=key)`. It has "all" (every project of every given board, in board order) or one project key. It has no hide filter and no presentation order. So a deck from `x` with X-1's scope (hidden excluded from the bytes, view 3 in presentation order) cannot be built by passing today's arguments: `extract` (or what feeds it) must change. That is a requirement and graph decision, not a baseline one.
- **The hide flags:** for views 1/2, `present_tasks` drops tasks with show_in_present False. For view 3, `_all_plan` drops hidden projects, and their tasks are filtered the same way. Hidden milestone classes are a third hide (`present_tasks_m`, `_hidden_class_ids`), which the export also honours today (test_TC_2608).
- **`o` inside `R`:** today the `o` offer works only on the main screen (P-6). X-1 asks for `o` after `x` in `R`. PRESENT_KEYS has no `o` row, and the app's `o` does not reach past the modal.
- **The `H` flow's key:** the extract key is `<registry id or #pos>:<project id>` (app.py:3006-3009). The board list comes from `board_lanes` (every loaded board), not just the presented board.
- **The shared writer:** the CLI `--report` (__main__.py:213-215) uses the same `extract` + `write_reports`. LLR-3107.5 also pins `report.py` and that path unchanged.

## Guards (existing tests that exercise the slice): 49 passed in 48.8 s on incX-marks

The 17 export tests listed above by id, plus tests/test_report_export_app.py, tests/test_report_html.py and tests/test_report_deck.py (whole files), test_keymap.py::test_global_commands_are_palette_only_not_in_the_bar, test_help_keys.py::test_TC_1607_global_keys_are_the_live_palette_only_keys and ::test_AT_1603_the_help_shows_the_global_keys_without_scrolling. Command: `env -u NO_COLOR python -m pytest -q -p no:cacheprovider <ids>`, cwd incX-marks. After the run no headless msedge process was left (checked with `Win32_Process`, command line matching "headless").

The `# node:` marks were written only in incX-marks: 22 lines in app.py, views.py, models.py, modals.py, report_html.py, report_deck.py and keymap.py. That worktree is removed at the end of this step. Nothing in taskboard/ or tests/ of x-html was touched.

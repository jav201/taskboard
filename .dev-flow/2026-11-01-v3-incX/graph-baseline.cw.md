# Code-Wire baseline — the presentation's `x` export, the `H` report flow and the key bar's `bar` flag at 509d444

Baseline of the code that Inc X (the presentation's `x` exports the HTML deck; the SVG/PNG export is removed; `H` joins the key bar) touches, as the code is at commit 509d444 (marks tree `taskboard-wt/incX-marks`). No design and no proposal: only what the code does now. Every node has `req: to trace`: the requirements of this increment are written in parallel. Example sources are test ids (file::test) of the current suite, or a probe `P-n` run on 509d444 (values printed by the probe, listed in baseline-notes.md). The probes import `taskboard` from incX-marks (`taskboard.__file__` printed). The probe board is synthetic: projects Alpha (`pA`, present_rank `1`), Beta (`pB`, present_rank `0`), Gamma (`pC`, show_in_present `False`), Delta (`pD`, archived); tasks a1 (Alpha), a2 (Alpha, show_in_present `False`), b1 (Beta), c1 (Gamma), d1 (Delta). The nodes slated for removal by the commission (X-2) are `present_paths`, `save_present_svg`, `_find_msedge`, `save_present_png` and `present_all_export`; their callers and tests are listed in baseline-notes.md.

## Nodes

PresentScreen.action_export
req: to trace
in:
out: None
func: `x` in `R` (PRESENT_KEYS row "export this view · SVG + PNG", priority binding); below `PRESENT_MIN_WIDTH` (36) a warning toast and nothing written; view 3 (`all`) writes `present_all_export` (the timeline without the rail and without the cursor, cut to its content) to `present_paths(board, None, today, "all")`; views 1/2 write `_frame_text()` to `present_paths(board, project_name, today, view)`; then `save_present_svg` and `save_present_png`; the toast names the files and the folder; it writes no board, offers no `o`, and reads no hide flag itself (the renders already drop hidden rows)
module: taskboard/app.py
modify: [I/O: reports/present-*.svg] (replace); [I/O: reports/present-*.png] (replace)
examples: (P-6, root action_export) `R` on a1 at 118x31, `x` → toast "Exported present-alpha-2026-11-01.svg to", "PNG needs Microsoft Edge", severity "warning" (the PNG writer stubbed to None)
examples: (P-6, root action_export) `2` then `x` → "present-alpha-2026-11-01-split.svg"; `3` then `x` → "present-board-2026-11-01-all.svg"
examples: (P-6) at 30x20 `R`, `x` → toast "Widen the terminal to 36+ columns to export", no file
examples: (test_present_views_app.py::test_AT_1803_the_view_keys_and_what_the_views_share) `x` in gantt then in split → two files, "present-website-redesign-2026-09-30.svg" and "present-website-redesign-2026-09-30-split.svg"

PresentScreen._frame_text
req: to trace
in: int? scroll = None
out: Text frame
func: the current view's frame at the panel's size, what is painted and what `x` exports in views 1/2: `render_present(board, project_id, cursor_id, today, w, h, view, scroll)`; in view 3 `render_present_all(...).frame` (the rail included; `x` does not use it there)
module: taskboard/app.py
examples: (test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle) `R` at 118x31 on the oracle board → the frame equals PRES-V3-gantt-118x30

present_paths
req: to trace
in: Board board; str? project_name; date? today = None; str view = "gantt"
out: tuple(Path svg, Path png)
func: `<board folder>/reports/present-<slug>-<YYYY-MM-DD>[-<view>]` with `.svg` and `.png`; slug = lowercase alphanumerics, every other character "-", stripped, cut to 40, "board" when empty or when project_name is None; `gantt` adds no suffix; creates nothing
module: taskboard/views.py
examples: (P-1) project_name "Website Redesign", today 2026-11-01 → svg "present-website-redesign-2026-11-01.svg", png "present-website-redesign-2026-11-01.png" in "reports"
examples: (P-1) project_name `None`, view "all" → svg "present-board-2026-11-01-all.svg"; project_name "!!!" → "present-board-2026-11-01.svg"
examples: (test_present_views_app.py::test_TC_1809_each_view_exports_to_its_own_file) view "split" → "present-website-redesign-2026-09-30-split.png"

save_present_svg
req: to trace
in: Text text; Path path; int width; int height
out: Path path
func: prints `text` on a recording rich Console (width + 2, height + 4, truecolor, output to devnull) and `save_svg(path, title="taskboard · presentation")`; makes the parent folder
module: taskboard/views.py
modify: [I/O: reports/present-*.svg] (replace)
examples: (P-2) Text "hello ◆", path s/reports/p.svg, `20` x `2` → path; the file starts "<svg", holds "taskboard&#160;·&#160;presentation"; the folder "reports" made
examples: (test_present_room.py::test_TC_1608_the_frame_and_its_export_hold_no_presenter_text) the exported SVG holds no presenter key text

_find_msedge
req: to trace
in:
out: str? exe
func: the headless Edge binary: `msedge.exe` under ProgramFiles(x86) then ProgramFiles (`Microsoft/Edge/Application`), else `shutil.which("msedge")` or `which("microsoft-edge")`; None when absent
module: taskboard/views.py
examples: (P-2) this machine → exe "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

save_present_png
req: to trace
in: Path svg_path; Path png_path; int width; int height
out: Path? png
func: rasterises the SVG with headless Edge (`--headless=new --disable-gpu --screenshot=<png> --window-size=<w*10>,<h*20> <svg uri>`, `subprocess.run`, timeout 30 s); None when `_find_msedge` is None, on timeout or OSError, on a non-zero exit, or when no PNG appears; never raises
module: taskboard/views.py
modify: [I/O: reports/present-*.png] (replace)
examples: (P-2) `_find_msedge` → None → png `None`
examples: (P-2) `_find_msedge` → a binary that rejects the flags (python) → png `None`, no file written
examples: (test_present_backlog_round.py::test_AT_2404_the_export_reads_as_a_slide) the `png` fixture stubs it on `taskboard.app` and records the cells asked: the export's timeline width and row count

present_all_export
req: to trace
in: Board board; date today; int width; int height; frozenset folded = frozenset(); str? anchor = None
out: tuple(Text text, int width, int rows)
func: view 3's export: the timeline at the width the screen draws it (`width - PRESENT_RAIL_W - 1` from `PRESENT_RAIL_MIN` 100, else `width`), `_all_timeline` laid out around `anchor` with NO cursor, trailing blank rows cut; the projects are `_all_plan`: shown projects (show_in_present) in `present_order`, each with its shown open tasks
module: taskboard/views.py
examples: (P-3) the probe board at 118 x 29 → width `93`, rows `8`; "Beta" before "Alpha" (present order); no "Gamma" (hidden project), no "Alpha hidden" (hidden task), no "Delta" (archived)
examples: (P-3) the same board at 90 x 29 (no rail) → width `90`, rows `8`
examples: (test_present_backlog_round.py::test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content) no cursor glyph in the text and no blank last row

present_order
req: to trace
in: Board board
out: list[Project] projects
func: the visible (not archived) projects in the presentation's order: `present_rank` set first by rank, then the others; board order breaks ties; hidden projects (show_in_present False) are included (the rail lists them with "○")
module: taskboard/models.py
examples: (P-3) the probe board → projects ["pB", "pA", "pC"] (board.projects ["pA", "pB", "pC", "pD"])

present_tasks
req: to trace
in: Board board; str? project_id
out: tuple(list[Task] open_tasks, list[Task] tasks)
func: one project's visible tasks in gantt order with the hidden ones (show_in_present False) left out: (open ones, all shown); the hide filter of views 1/2 and their export
module: taskboard/views.py
examples: (test_present_hide.py::test_AT_1602_space_hides_and_it_is_remembered_a_shows_all) a task hidden with `space` leaves the field, the brief and the export

TaskboardApp.action_report_export
req: to trace
in:
out: None
func: `H` (KEYMAP, bar=False, group misc, not priority): `board_lanes` → the loaded boards `(id, name, colour, board)` (a None board skipped and counted); the current project = the selected task's, else the focused one (never `present_project_id`'s fallback); its extract key `<board id or #pos>:<project id>`; folder `<open board folder>/reports`; pushes `ReportExport(folder, board names, (project, board) | None)` with `_on_report_chosen` as callback
module: taskboard/app.py
examples: (P-6, root action_report_export) one `--open` board "Main", a1 selected, `H` → stack ["Screen", "ReportExport"], scope "all", project ("Alpha", "Main"), boards ["Main"]
examples: (P-6) `H` while `R` is open → stack ["Screen", "PresentScreen"] unchanged (a non-priority app key does not pass a ModalScreen)
examples: (test_report_export_app.py::test_TC_3119_files_land_beside_the_open_board) the files land in the open board's `reports/` folder

TaskboardApp._on_report_chosen
req: to trace
in: tuple[tuple[str, ...], str]? res; list boards; int skipped; str? key; Path folder
out: None
func: None → nothing; else `extract(boards, people, marks, today, project=key if scope == "project")`, `write_reports(d, kinds, folder, today)`; an OSError → error toast "Report not (fully) written: <error>" and the offer cleared; else the info toast "Report written: <names joined by ' and '>[ · N board(s) skipped]\n<folder>\no opens it (10 s)" and `_report_offer = (paths[0], clock + 10)`
module: taskboard/app.py
modify: [Data: TaskboardApp._report_offer] (replace); [I/O: reports/<kind>-*.html] (replace)
examples: (P-6, root action_report_export) `H`, `p`, `c` → toast "Report written: deck-main-alpha-2026-11-01.html", "o opens it (10 s)", title "Report", severity "information"
examples: (test_report_export_app.py::test_TC_3120_a_failed_write_toasts_and_offers_nothing) a write that raises OSError → one toast "Report not (fully) written:" and no offer

TaskboardApp.action_open_url
req: to trace
in:
out: None
func: `o` (KEYMAP, bar=False): first the `H` offer — single use; within its 10 s `_open_report(path)` and return; after that every valid http(s) URL of the selected task; non-priority, so it does not act while a ModalScreen (the presentation among them) is on top
module: taskboard/app.py
modify: [Data: TaskboardApp._report_offer] (clear)
examples: (P-6, root action_open_url) after `H`, `p`, `c` on the main screen, `o` → opened ["deck-main-alpha-2026-11-01.html"]
examples: (P-6) a live offer set while `R` is open, `o` → opened [] and the offer still set
examples: (test_report_export_app.py::test_TC_3120_o_opens_the_report_while_the_toast_lives) `o` at 9.9 s opens the file; a second `o` is open_url again; `o` over another screen leaves the offer

TaskboardApp._open_report
req: to trace
in: Path path
out: None
func: `os.startfile(path)` where it exists (Windows), else `webbrowser.open(path.as_uri())`; an OSError or a False open → error toast "Could not open the report <name>."
module: taskboard/app.py
examples: (test_report_export_app.py::test_TC_3120_o_opens_the_report_while_the_toast_lives) without `os.startfile` the opener is `webbrowser.open` of the file URI; a failing opener toasts

ReportExport.action_scope
req: to trace
in: str scope
out: None
func: `p` / `o` in the modal: moves the scope mark ("project" | "all") and repaints; "project" with no current project → nothing (the mark stays on "all"); the modal stays open
module: taskboard/modals.py
examples: (P-6) `H`, `p` → scope "project"
examples: (test_report_export_app.py::test_TC_3118_scope_keys_and_no_project) no selected task and no focus → `p` leaves "all" marked; the key line reads "no project selected"

ReportExport.action_write
req: to trace
in: str kind
out: None
func: `b` / `c` / `a`: dismisses `(kinds, scope)` with kinds ("workspace",), ("deck",) or ("workspace", "deck"); `esc` (action_cancel) dismisses None
module: taskboard/modals.py
examples: (P-6) `H`, `p`, `c` → the callback gets kinds ("deck",) and scope "project"; one file "deck-main-alpha-2026-11-01.html"
examples: (test_report_export_app.py::test_AT_3105_H_c_writes_the_deck_with_one_slide_per_chosen_project) `H c` → the deck with one slide per project in scope

extract
req: to trace
in: list boards; dict people; dict marks; date today; str? project = None
out: dict d
func: report_html.extract: per board `(id | None, name, colour, Board)` (key = id or "#<pos>"), per project in BOARD ORDER (`board.projects`, then an Inbox row) every task of it; `project` keeps one key, an unknown key raises ValueError; it reads NO hide flag (show_in_present) and NO present_rank; archived projects and tasks are kept (flagged); returns the JSON-able dict v1 (meta.scope kind "all" | "project")
module: taskboard/report_html.py
examples: (P-4) the probe board as "Main" (#0) → projects ["#0:pA", "#0:pB", "#0:pC", "#0:pD"], tasks ["#0:a1", "#0:a2", "#0:b1", "#0:c1", "#0:d1"] (the hidden a2 and pC kept), scope kind "all"
examples: (P-4) project "#0:pA" → tasks ["#0:a1", "#0:a2"], scope kind "project"
examples: (P-4) project "#0:nope" → ValueError "no project with the key '#0:nope' on the given boards"
examples: (test_report_html.py::test_TC_3101_extract_never_writes_a_board) extract saves no board

write_reports
req: to trace
in: dict d; tuple[str, ...] kinds; Path folder; date today
out: list[Path] paths
func: every kind checked first (an unknown kind → ValueError, nothing created); makes `folder`; per kind renders (`report_workspace.render` | `report_deck.render`) and writes `report_name(kind, today, board slug, project slug)`: "<kind>-<YYYY-MM-DD>.html" for scope all, "<kind>-<board slug>-<project slug>-<YYYY-MM-DD>.html" for a project; a same-day file is overwritten
module: taskboard/report_html.py
modify: [I/O: reports/<kind>-*.html] (replace)
examples: (P-4) kinds ("deck",), scope all → paths ["deck-2026-11-01.html"]; scope "#0:pA" → ["deck-main-alpha-2026-11-01.html"]
examples: (P-4) kinds ("svg",) → ValueError "unknown report kind: svg", folder made `False`
examples: (test_report_html.py::test_TC_3123_write_reports_lands_in_the_folder_and_overwrites) a second same-day write overwrites; the folder holds `2` files

render
req: to trace
in: dict d
out: str page
func: report_deck.render: one self-contained HTML page: a cover (`_scope_line`, counts per board), an overview (every project in scope on one timeline) and one slide per `slide_projects` entry, in the dict's order (board then project order); reads the dict alone
module: taskboard/report_deck.py
examples: (P-4) the probe dict (scope all) → the page holds "Gamma" (hidden project) and "Alpha hidden" (hidden task), no "Delta one" (archived project); "Alpha" before "Beta" (board order, not present order); scope line "All loaded boards (1): Main"
examples: (test_report_deck.py::test_TC_3113_one_slide_per_project) the fixture → `13` sections; the archived and the task-less project get no slide

slide_projects
req: to trace
in: dict d
out: list[tuple[dict, list]] entries
func: (project, its tasks) for every non-archived project in the dict that holds a task, in the dict's order
module: taskboard/report_deck.py
examples: (P-4) the probe dict → slides ["Alpha", "Beta", "Gamma"]

bar_keys
req: to trace
in: str view; str layer = "more"
out: list[Key] keys
func: the keys the docked key bar draws in `view`: live keys (views None or containing view), the primary layer only `primary`, universal ones first, and only `bar=True`; `fit_bar`, `render_key_bar` and the `?` help's Keys band read it
module: taskboard/keymap.py
examples: (P-5) view "swimlanes", layer "more" → no "H" (bar `False`)
examples: (test_keymap.py::test_global_commands_are_palette_only_not_in_the_bar) no global action (`open_url`, `present`, `standup`, …) is bar=True in any view

global_keys
req: to trace
in: str view
out: list[Key] keys
func: the live keys with `bar=False`, in seat order; the `?` help pins them on its global line (`HelpModal._key_texts`)
module: taskboard/keymap.py
examples: (P-5) view "swimlanes" → shows ["o", "i", "p", "P", "f", "c", "R", "A", "N", "n", "H", "@", "#", "I", "S"]
examples: (test_help_keys.py::test_TC_1607_global_keys_are_the_live_palette_only_keys) exactly the live bar=False entries in seat order; a seat key added later is last

fit_bar
req: to trace
in: int width; str view; str layer = "more"
out: tuple(list[tuple[str, str]] entries, int dropped)
func: what the bar shows at `width`: `bar_keys` as (show, label); words dropped from the right first, then whole keys from the right, counted in `dropped` (drawn as " +N" when it fits); the KeyBar starts on the primary layer, `;` toggles "more"
module: taskboard/keymap.py
examples: (P-5) width `118`, "swimlanes", "primary" → dropped `0`, bar "? Map  ; More  q Quit  B Boards  1 Lanes"
examples: (P-5) width `80`, "swimlanes", "more" → dropped `12`, the bar ends "M +12"
examples: (P-5) width `118`, "swimlanes", "more" → dropped `0`, every word but "Map" gone

## Entities

[Data: PresentScreen state]
desc: `_board`, `_project_id`, `_project_name`, `_today` (frozen at open), `_view` (index into PRESENT_SCREEN_VIEWS = gantt, split, all), `_cursor_id`, `_all_cur`, `_folded` (view 3, this presentation only), `_rail`; read by `action_export` for the file names and the view-3 layout

[Data: Task.show_in_present]
in: bool
desc: the task's presentation flag (True unless the file says false); `space` / `a` / `u` in `R` write it; `present_tasks` and `_all_plan` drop False; `extract` does not read it

[Data: Project.show_in_present]
in: bool
desc: view 3's project flag; `present_order` keeps hidden projects (the rail shows them "○"), `_all_plan` drops them from the timeline and so from `present_all_export`; `extract` does not read it

[Data: Project.present_rank]
in: int?
desc: the presentation's own order (view 3, `shift+↑/↓`, `K`/`J`); read by `present_order`; `extract` and the deck keep `board.projects` order

[I/O: reports/present-*.svg]
desc: `<board folder>/reports/present-<slug>-<date>[-split|-all].svg`, written by `save_present_svg` from `action_export`; a same-day export overwrites

[I/O: reports/present-*.png]
desc: the PNG twin, written by headless Edge in `save_present_png` when Edge is found and exits 0

[I/O: reports/<kind>-*.html]
desc: `<open board folder>/reports/workspace-*.html` and `deck-*.html` (report B and C), written by `write_reports`; names from `report_name`

[Data: TaskboardApp._report_offer]
in: tuple[Path, float]?
desc: the `H` export's `o` offer: (first written path, `_report_clock()` + 10); set by `_on_report_chosen`, cleared on a failed write and on the first `o`; read only by `action_open_url` (main screen)

[Data: keymap.KEYMAP]
in: tuple[Key, ...]
desc: the one key seat; `Key("H", "H", "report_export", "Report", group="misc", bar=False)` (keymap.py:152), `Key("o", "o", "open_url", "URL", group="misc", bar=False)`; `bar` is read by `bar_keys` (bar=True) and `global_keys` (bar=False) only; `palette_commands` lists every live key whatever `bar`

[Data: keymap.PRESENT_KEYS]
in: tuple[PresentKey, ...]
desc: the presentation's seat: `present_bindings()` makes PresentScreen.BINDINGS (all priority) and `PresentKeys` (`?` in `R`) lists the rows; the OUT row `PresentKey((("x", "export"),), "x", "export this view · SVG + PNG", "OUT")`; no row binds `o` or `H`

[Data: App.screen_stack]
in: list[Screen]
desc: Textual's stack; PresentScreen and ReportExport are ModalScreens; Textual 8.2.8 `Screen._modal_binding_chain` stops the non-priority binding chain at the top modal, so the app's `H` and `o` do not act while `R` is open (P-6)

[Interface: presentation hint row]
desc: `#present-hint`, `PresentScreen._keys_hint`: the first wording that fits, longest first; each names "x export" (or "x" in the shortest); e.g. views 1/2 at 118 "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"
offers: "x export" → PresentScreen.action_export

[Interface: key bar]
desc: `KeyBar` (keymap.py), docked; `refresh_bar` → `render_key_bar(width, view, layer)` → `fit_bar`; primary layer at start, `;` toggles "more"; `H` is not on it in any view or layer (bar=False)

[Interface: ReportExport key line]
desc: `#rx-keys`: `key_line([("b", "workspace"), ("c", "deck"), ("a", "both"), ("p", <project name, 30 cells> | "no project selected"), ("o", "all boards"), ("esc", "close")], inner)`
offers: "b workspace" → ReportExport.action_write
offers: "c deck" → ReportExport.action_write
offers: "a both" → ReportExport.action_write
offers: "p" → ReportExport.action_scope
offers: "o all boards" → ReportExport.action_scope

[Outside: key x]
desc: PRESENT_KEYS priority binding `export` on PresentScreen; on the main screen `x` is KEYMAP `archive` (a different action)

[Outside: key H]
desc: KEYMAP `report_export`, not priority, bar=False

[Outside: key o]
desc: KEYMAP `open_url`, not priority, bar=False; in ReportExport a priority `o` → scope('all')

## Edges

[Data: PresentScreen state] ──▶ PresentScreen.action_export
[Data: PresentScreen state] ──▶ PresentScreen._frame_text
PresentScreen.action_export ──▶ [I/O: reports/present-*.svg]
PresentScreen.action_export ──▶ [I/O: reports/present-*.png]
save_present_svg ──▶ [I/O: reports/present-*.svg]
save_present_png ──▶ [I/O: reports/present-*.png]
[Data: Task.show_in_present] ──▶ present_tasks
[Data: Task.show_in_present] ──▶ present_all_export
[Data: Project.show_in_present] ──▶ present_all_export
[Data: Project.present_rank] ──▶ present_order
TaskboardApp._on_report_chosen ──▶ [Data: TaskboardApp._report_offer]
TaskboardApp._on_report_chosen ──▶ [I/O: reports/<kind>-*.html]
write_reports ──▶ [I/O: reports/<kind>-*.html]
[Data: TaskboardApp._report_offer] ──▶ TaskboardApp.action_open_url
TaskboardApp.action_open_url ──▶ [Data: TaskboardApp._report_offer]
[Data: keymap.KEYMAP].bar ──▶ bar_keys
[Data: keymap.KEYMAP].bar ──▶ global_keys
[Data: keymap.PRESENT_KEYS] ──▶ PresentScreen.action_export
[Data: App.screen_stack] ──▶ TaskboardApp.action_report_export
[Data: App.screen_stack] ──▶ TaskboardApp.action_open_url
[Outside: key x] ──▶ PresentScreen.action_export
when: PresentScreen is the top screen (priority binding); below 36 columns it only toasts
[Outside: key H] ──▶ TaskboardApp.action_report_export
when: the main screen is on top (a non-priority app binding does not pass a ModalScreen; held behind the home and the global screens by check_action)
[Outside: key o] ──▶ TaskboardApp.action_open_url
when: the main screen is on top; not while PresentScreen or another modal is on top

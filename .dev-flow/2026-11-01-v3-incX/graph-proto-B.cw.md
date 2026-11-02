# Inc X — prototype graph, group B: `taskboard/views.py`

> Only the differences from `graph-baseline.cw.md` (509d444). The seams are frozen in `graph-interfaces.cw.md`:
> `present_deck_boards` and `present_name` are implemented exactly as frozen there (`render` is unchanged, ruling 8); this
> file adds their internal parts, the extra examples, and the removals (X-2). `report_html.py` and
> `report_deck.py` stay byte-unchanged (rulings 8 and 12). Fixture X and probe P-X1: see the head of
> `graph-interfaces.cw.md`. Removed nodes keep their baseline contract so the extractor and the review can
> name what goes; each says REMOVED in `func:`.

## Nodes

present_deck_boards
req: LLR-4501.3, LLR-4501.10, LLR-4501.15, LLR-4502.7
in: tuple[str?, str, str, Board] lane; str? project_id
out: list[tuple[str?, str, str, Board]] boards
func: as frozen in graph-interfaces.cw.md. Internal rules: `copy.copy(board)` (the `_hide` proxy pattern, views.py:3151), then `proxy.projects` and `proxy.tasks` are assigned NEW lists; each held task is shallow-copied and its copy's `urls` is cleared before `extract`; the source board's lists, its projects and its tasks, including their URLs, are never changed. `present_order`, `visible_projects`, `present_tasks_m` and `_hidden_class_ids` are the only scope readers, so a missing presented id falls back exactly as the frame does and the deck hides what the frames hide. No call of `save`, no cache, no write of any file.
module: taskboard/views.py
examples: (TC-4703) fixture X, project_id "pA", nothing hidden → proxy tasks "a1", "a2", "a3" in board order (not gantt order), all with urls []; the deck's bytes equal `H`'s over the same proxy
examples: (TC-4710) the hidden-sentinel board, project_id `None` → the source board keeps its projects ["pA", "pB", "pH", "pR"] and every task's flag (P-X1: board untouched True)
examples: (TC-4715) project_id "missing" and visible projects [pA, pB] → proxy projects [pA]; no None enters `extract`
examples: (TC-4727) a1 has URL "https://example.test/capability-a1" → proxy a1 urls [], source a1 urls ["https://example.test/capability-a1"]

present_name
req: LLR-4501.1
in: str? project_name; date today
out: str name
func: as frozen in graph-interfaces.cw.md; `from .report_html import slug` is inside the function, avoiding the module-level circular import; no local slug rule. `None` returns view 3's collision-free `present-<today>.html`.
module: taskboard/views.py
examples: (TC-4701c) project_name "!!!", today 2026-11-01 → name "present-project-2026-11-01.html"
examples: (TC-4702) project_name `None`, today 2026-11-01 → name "present-2026-11-01.html"

present_paths
req: LLR-4504.3
in: Board board; str? project_name; date? today = None; str view = "gantt"
out: tuple(Path svg, Path png)
func: REMOVED (X-2). Its only callers were `PresentScreen.action_export` (app.py:636, :639); its name rule moves to `present_name`. The module imports `os`, `shutil` and `subprocess` go with this node and the next three (their only users; `Console` stays for `_SEARCH_CONSOLE`).
module: taskboard/views.py
examples: (TC-4743) inspection `grep -rnE "save_svg|msedge|--screenshot|present_paths|present_all_export" taskboard/views.py` → `0` hits (base: 9)

save_present_svg
req: LLR-4504.1, LLR-4504.3
in: Text text; Path path; int width; int height
out: Path path
func: REMOVED (X-2): no `.svg` of the frame is written by anything.
module: taskboard/views.py
examples: (TC-4741) `x` in views 1, 2, 3 → `0` ".svg" in `reports/`
examples: (TC-4743) "save_svg" `0` hits in taskboard/*.py

_find_msedge
req: LLR-4504.2, LLR-4504.3
in:
out: str? exe
func: REMOVED (X-2); its only caller was `save_present_png`.
module: taskboard/views.py
examples: (TC-4742) `x` with subprocess.run and subprocess.Popen patched to raise → `0` calls
examples: (TC-4743) "msedge" `0` hits in taskboard/*.py

save_present_png
req: LLR-4504.1, LLR-4504.2, LLR-4504.3
in: Path svg_path; Path png_path; int width; int height
out: Path? png
func: REMOVED (X-2): no headless Edge, no `subprocess` in views.py.
module: taskboard/views.py
examples: (TC-4741) `x` in views 1, 2, 3 → `0` ".png" in `reports/`
examples: (TC-4742) `x` in views 1, 2, 3 → the deck written, `0` process starts
examples: (TC-4743) "--screenshot" `0` hits in taskboard/*.py

present_all_export
req: LLR-4504.3
in: Board board; date today; int width; int height; frozenset folded = frozenset(); str? anchor = None
out: tuple(Text text, int width, int rows)
func: REMOVED (X-2): view 3's export is the deck of `present_deck_boards(lane, None)`, not the timeline text.
module: taskboard/views.py
examples: (TC-4743) "present_all_export" `0` hits in taskboard/*.py

_all_timeline
req: LLR-4504.3
in: Board board; int width; int height; date today; tuple? cur; frozenset folded; bool rail_focus
out: tuple(list[str] lines, list stops, tuple? cur)
func: CHANGED from base: the parameter `anchor` and its docstring go (its only caller was `present_all_export`, grep views.py:7665); `around` is the cursor's project as at base when `anchor` was None. `render_present_all` calls it as before, so every frame of view 3 is unchanged. `PresentAll.timeline`'s comment "what `x` exports" becomes "the frame without the rail" (the field stays: tests read it).
module: taskboard/views.py
examples: (test_present_all.py::test_AT_2104_three_views_one_cursor_and_the_export) view 3 frames at 118x30 → equal to base (the frame part of the test)
examples: (TC-4743) "anchor" is not a parameter of `_all_timeline`; `render_present_all` frames equal to base

## Entities

[Data: Task.show_in_present]
in: bool
desc: CHANGED reader set: also read by `present_deck_boards` (through `present_tasks_m`) at each `x`

[Data: Task.urls]
in: list[str]
desc: CHANGED reader set: `present_deck_boards` clears each shallow-copied held task's URLs before `extract`; source tasks and `H`'s reports keep theirs

[Data: Project.show_in_present]
in: bool
desc: CHANGED reader set: view 3's `present_deck_boards` drops a project whose flag is False; views 1/2 ignore the presented project's own flag (LLR-4501.5)

[Data: Project.present_rank]
in: int?
desc: CHANGED reader set: `present_deck_boards` orders view 3's projects by `present_order`, so the deck follows the presentation's order

## Edges

[Data: Task.show_in_present] ──▶ present_deck_boards
[Data: Task.urls] ──▶ present_deck_boards
[Data: Project.show_in_present] ──▶ present_deck_boards
[Data: Project.present_rank] ──▶ present_deck_boards

## Findings

finding P-B-1 the proxy board keeps the real board's path
anchor: present_deck_boards
seen: `copy.copy(board)` shares `path`, `settings`, `phases`; a `save()` on the proxy would write the filtered lists over the board file
cause: the `_hide` precedent (views.py:3151) uses the same shallow proxy
effect: none while the proxy reaches only `extract`, which never writes a board (test_report_html.py::test_TC_3101_extract_never_writes_a_board); LLR-4501.10's sha256 test (TC-4710) covers the `x` path
decision: resolved — rulings 21/F-9 and 22/S-2 accept no extra guard; the proxy is never cached or stored, and TC-4710 plus its `board.save()` mutant are mandatory E4 controls

finding P-B-2 two names could meet: a project slug "all", and view 3's former name
anchor: present_name
seen: `report_html.slug("All")` = "all", so view 3's former "present-all-<date>.html" could collide with that project's view-1 file; `slug("!!!")` = "" (P-X1)
cause: ruling 9's original pattern `present-<project-slug|all>-<date>.html`
effect: a same-day `x` of view 3 could overwrite that project's deck
decision: resolved — ruling 21/F-11 names view 3's file `present-<date>.html`, which cannot equal any non-empty-slug project name; the empty project slug still becomes "project"

finding P-B-3 the frozen signature of present_deck_boards differs from the slice's
anchor: present_deck_boards
seen: 01-requirements.md §6 row 5 names `present_deck_boards(board, project_id | None)`; the interface takes the lane `(id, name, colour, board)` and returns extract's `boards` list
cause: the registry identity (id, name, colour) is needed for the byte identity of LLR-4501.3 (its negative control is a wrong board key) and lives in app.py
effect: views.py reads no registry; app.py builds the lane (`PresentScreen._deck_lane`)
decision: resolved — ruling 21/F-9 accepts the lane signature; §6 row 7 now matches it

finding P-B-4 the removals leave stale text outside the source
anchor: present_paths
seen: (baseline-notes.md) REQUIREMENTS.md active LLR-1803.3, LLR-1905.1, LLR-2104.1, LLR-2404.1, LLR-2903.1, LLR-3107.5 name the removed functions; docs/ARCHITECTURE.md:42, :48, :70, :117, :122, :131 name Edge and the SVG export; three prototype scripts call them (ruling 5)
cause: X-2 removes the functions
effect: those rows and docs describe code that no longer exists
decision: resolved — rulings 20 and 21/F-9: the canon ids superseded by HLR-4504 are named individually in the ledger; ARCHITECTURE.md is edited with the README in E4 group A; ruling 5's one line per prototype folder (or BACKLOG) is written in E4

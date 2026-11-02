# Inc X — prototype graph, group A: `taskboard/app.py` + `taskboard/keymap.py`

> Only the differences from `graph-baseline.cw.md` (509d444). The seams are frozen in
> `graph-interfaces.cw.md`: this file calls `present_deck_boards`, `extract` (unchanged), `render(d)` (unchanged,
> ruling 8) and `present_name` there, and implements `PresentScreen.action_open_export` exactly as frozen there (not repeated
> here). Fixture X, probes P-X1 and P-X2: see the head of `graph-interfaces.cw.md`. `F` = `S/boards/main/reports`.
> Rulings applied: 1–22. In particular, `H` keeps its current seat (16), view 3's name is
> `present-<date>.html` (21/F-11), and `x` shares `TaskboardApp._report_offer` with `H` (21/F-12).
> Docs in this group, no node:
> the README rows at lines 140, 189, 291, 410 (LLR-4506.5, carried by `action_export`'s `oracle:` below) and the
> PresentScreen docstring (`x` writes the HTML deck of what is shown to `reports/`; `o` opens it for 10 s).

## Nodes

PresentScreen.action_export
req: LLR-4501.1, LLR-4501.2, LLR-4501.3, LLR-4501.4, LLR-4501.10, LLR-4501.13, LLR-4501.14, LLR-4501.15, LLR-4502.6, LLR-4502.7, LLR-4503.1, LLR-4503.4, LLR-4503.5, LLR-4503.7, LLR-4504.1, LLR-4504.2, LLR-4504.3, LLR-4506.5
in:
out: None
func: CHANGED from baseline (rewritten). (1) `_narrow()` → the warning toast "Widen the terminal to 36+ columns to export", title "Present", timeout 6, markup False, and return: no file, the offer untouched (base). (2) `lane = self._deck_lane()`; `pid = None` in view 3, else `self._project_id`. (3) `boards = present_deck_boards(lane, pid)`, read at this press (the hide flags as they stand now). (4) In views 1/2, `project = boards[0][3].projects[0] if boards[0][3].projects else None`, `key = None if project is None else f"{lane[0] if lane[0] is not None else '#0'}:{project.id}"`, and `project_name = None if project is None else (self._project_name if self._board.project_by_id(pid) is not None else project.name)`; in view 3, `key = None` and `project_name = None`. `today = date.today()` (as `H`); `d = report_html.extract(boards, self.app.people.people, self.app.marks.marks, today, project=key)`. (5) `folder = Path(self._board.path).parent / "reports"`, `path = folder / present_name(project_name, today)`. (6) `written = self.app._write_report(write, folder)` where `write()` does `folder.mkdir(parents=True, exist_ok=True)`, `path.write_text(report_deck.render(d), encoding="utf-8")` and returns `[path]`. (7) `self.app._report_offer = (written, self.app._report_clock() + 10)` when written is not None, else None. No `board.save()`, no subprocess, no SVG/PNG; the module drops its imports of `present_all_export`, `present_paths`, `save_present_png`, `save_present_svg` (slice 4) and imports `present_name` from views.
module: taskboard/app.py
modify: [Data: TaskboardApp._report_offer] (replace); [I/O: reports/present-*.html] (replace)
oracle: README.md rows at lines 140, 189, 291, 410: the `R` key-table row and the presentation section describe `x` as the HTML deck
examples: (TC-4701, root action_export) fixture X, `R` on a1 at 118x31, `x` → the file "present-alpha-2026-11-01.html" in `F`; `2`, `x` → the same name, rewritten (ruling 9, LLR-4501.1 as amended)
examples: (TC-4702, root action_export) `3`, `x` → the file "present-2026-11-01.html" in `F`
examples: (TC-4703, root action_export) fixture X, view 1 and view 2 `x` vs `H` `p` `c` over the same URL-cleared proxy the same day → `bytes ==` (rulings 8 and 14; both scope elements read "Project Alpha on Main")
examples: (TC-4704, root action_export) a registry of one board, nothing hidden, ranks in board order, `3`, `x` vs `H` `c` `o` over the same URL-cleared proxy → `bytes ==` (rulings 8 and 14; both scope elements read "All loaded boards (1): Main")
examples: (TC-4710, root action_export) sha256 of "board.json" and "history.jsonl" before and after `x` in views 1, 2, 3 → equal, `6`/`6`
examples: (TC-4713, root action_export) 30 columns, `x` → toast "Widen the terminal to 36+ columns to export", title "Present"
examples: (TC-4714, root action_export) 30 columns, `x` → `reports/` exists `False`
examples: (TC-4715, root action_export) project_id "missing", first visible project Alpha → key "main:pA", file "present-alpha-2026-11-01.html", deck holds "Alpha"
examples: (TC-4726, root action_export) `space` on a1 in view 1, `x` → "a-open-1" `0` occurrences in the file; `a`, `x` → "a-open-1" present
examples: (TC-4727, root action_export) a1 has URL "https://example.test/capability-a1" → `0` occurrences in the file; `H`'s deck of the original board keeps it
examples: (TC-4731, root action_export) `x` → toast "Report written: present-alpha-2026-11-01.html\n<F>\no opens it (10 s)", title "Report", severity "information", timeout `10`
examples: (TC-4734, root action_export) `reports` is a plain file → toast starting "Report not (fully) written: ", title "Report", severity "error"; `0` exceptions
examples: (TC-4735, root action_export) `x` (offer live), then `reports` replaced by a plain file, `x` → `TaskboardApp._report_offer` `None`; `o` → opener `0` calls
examples: (TC-4737, root action_export) the board folder named "[red]rx[/red]" → the toast's plain text holds "[red]rx[/red]" (markup `False`)
examples: (TC-4741, root action_export) `x` in views 1, 2, 3 → after each press `reports/` holds that scope's "present-*.html", `0` ".svg", `0` ".png", and no other file is new or changed
examples: (TC-4742, root action_export) subprocess.run and subprocess.Popen patched to raise → `x` in views 1, 2, 3 writes the deck; `0` calls
examples: (TC-4743) inspection `grep -rnE "save_svg|msedge|--screenshot|present_paths|present_all_export" taskboard/app.py` → `0` hits (base: 9, app.py:55-642)
examples: (TC-4765) inspection README.md minus its `<img` lines → `0` matches of "SVG|PNG"; the `R` row holds "HTML deck"; test_keymap.py::test_the_readme_keybinding_table_matches_the_seat GREEN
examples: (AT-4501, root action_export) registry of 2 boards, `R`, `space` on "HIDDEN-T-7Q", `x` → toast "Report written: present-alpha-2026-11-01.html"; "HIDDEN-T-7Q" `0`; no ".svg"/".png"; board sha256 equal; `2`, `x` → the same file
examples: (AT-4502, root action_export) `R`, `3`, `K` until C is first, `space` on B, `enter` on A, `x` → "present-2026-11-01.html"; slides read C, A; B `0` occurrences
examples: (AT-4504, root action_export) `reports` a plain file, `R`, `x` → "Report not (fully) written: "; `o` → `0` calls; `esc` closes the presentation
examples: (AT-4505, root action_export) 30 columns, `R`, `x` → "Widen the terminal to 36+ columns to export"; no `reports/`

PresentScreen._deck_lane
req: LLR-4501.7, LLR-4501.11
in:
out: tuple[str?, str, str, Board] lane
func: NEW. The presented board as `extract` names it, the tuple `board_lanes` gives the open board, without reading any other board's file: when `self.app.board_id` is not None and `self.app.registry.get(board_id)` is an entry → `(entry.id, entry.name, entry.color, self._board)`; else (an unlisted board, `--open`) → `(None, label[0], label[1], self._board)` with `label = self._board.label or ("this board", "pink")`.
module: taskboard/app.py
examples: (TC-4707, root action_export) a registry of 2 boards, "main" open → lane ("main", "Main", "sky", board); the other board's file is not read; the cover's board table has `1` row
examples: (TC-4711, root action_export) `--open`, label ("Client A", "pink") → lane (`None`, "Client A", "pink", board); the cover's board cell "Client A"; the file "present-alpha-2026-11-01.html"
examples: (TC-4711, root action_export) `--open`, no label → lane name "this board"; the cover's board cell "this board"

TaskboardApp._write_report
req: LLR-4503.1, LLR-4503.4, LLR-4503.7
in: (Callable) None->list[Path] write; Path folder; int skipped = 0
out: Path? first
func: NEW: the write → toast tail `_on_report_chosen` had, shared by `H` and `x` (slice 3). `paths = write()`; an OSError `e` → toast "Report not (fully) written: <e>", title "Report", severity "error", timeout 10, markup False, return None. Else the toast "Report written: <names joined by ' and '>" + (" · <n> board(s) skipped" when skipped) + "\n<folder>\no opens it (10 s)", title "Report", severity "information", timeout 10, markup False; return `paths[0]`. It stores no offer: both callers store `TaskboardApp._report_offer` (ruling 21/F-12).
module: taskboard/app.py
examples: (TC-4731, root action_export) write → [`F`/"present-alpha-2026-11-01.html"] → first that path; toast "Report written: present-alpha-2026-11-01.html\n<F>\no opens it (10 s)"
examples: (TC-4734, root action_export) write raises FileExistsError → first `None`; toast "Report not (fully) written: "
examples: (TC-4737, root action_export) folder "S/[red]rx[/red]/reports" → the toast's plain text holds "[red]rx[/red]"
examples: (test_report_export_app.py::test_TC_3120_a_failed_write_toasts_and_offers_nothing, root action_report_export) `H`, a write that raises OSError → one toast "Report not (fully) written:" (unchanged for `H`)

TaskboardApp._on_report_chosen
req: LLR-4501.3, LLR-4501.4
in: tuple[tuple[str, ...], str]? res; list boards; int skipped; str? key; Path folder
out: None
func: CHANGED from baseline: its tail is now `first = self._write_report(lambda: report_html.write_reports(d, kinds, folder, today), folder, skipped)` and `self._report_offer = (first, self._report_clock() + 10)` when first is not None, else None. Same toasts, files and offer as base; the deck it writes over the same URL-cleared proxy is the reference of TC-4703/TC-4704.
module: taskboard/app.py
modify: [Data: TaskboardApp._report_offer] (replace)
examples: (TC-4703, root action_report_export) fixture X's URL-cleared proxy, `H`, `p`, `c` → "deck-main-alpha-2026-11-01.html", its scope element "Project Alpha on Main"
examples: (TC-4704, root action_report_export) view 3's URL-cleared proxy, `H`, `c` (scope all) → "deck-2026-11-01.html", its scope element "All loaded boards (1): Main"
examples: (test_report_export_app.py::test_TC_3120_o_opens_the_report_while_the_toast_lives, root action_open_url) `o` at 9.9 s opens the file (unchanged)

TaskboardApp._open_report
req: LLR-4503.6
in: Path path
out: None
func: CHANGED from baseline (ruling 22/S-6): unchanged opener and toast, but catches `(OSError, ValueError)` so a relative path's `as_uri()` failure off Windows cannot escape into `R`; this also fixes the pre-existing `H` path.
module: taskboard/app.py
examples: (TC-4736, root action_open_export) relative board path off Windows, path.as_uri() raises ValueError → error toast "Could not open the report present-alpha-2026-11-01.html.", `0` exceptions

PresentScreen._keys_hint
req: LLR-4506.4
in: int w; int hidden; int room
out: Text hint
func: UNCHANGED (X-4, LLR-4506.4): the wordings still say "x export", which now means the HTML deck; no `o` in the hint (finding P-A-1, ruling 10).
module: taskboard/app.py
examples: (TC-4764) views 1, 2, 3 × widths 130, 118, 100, 80, 60, 36 × hidden `0` and `2` → plain text equal to base, `36`/`36`; view 1 at 118, hidden 0 holds "⇥ next · ←→ ↑↓ move · ␣ hide · a show all · x export · esc leave"

present_bindings
req: LLR-4506.3, LLR-4503.2
in:
out: list[Binding] bindings
func: UNCHANGED code; its seat changes (PRESENT_KEYS): a new row `PresentKey((("o", "open_export"),), "o", "open the last export (10 s)", "OUT")` right after the `x` row, so PresentScreen binds `o` → `action_open_export` (priority).
module: taskboard/keymap.py
examples: (TC-4763) the binding keys = "1", "2", "3", "tab", "shift+tab", "up,k", "down,j", "left,h", "right,l", "pageup", "pagedown", "space", "a", "u", "shift+up,K", "shift+down,J", "enter", "x", "escape,q", "question_mark" and "o"; `21` bindings
examples: (TC-4732) the binding "o" has action "open_export" and priority `True`

PresentKeys.lines
req: LLR-4506.1, LLR-4506.2
in:
out: Text lines
func: UNCHANGED code (modals.py, not in the slice); it lists PRESENT_KEYS by group, so it shows the changed `x` row "export this view · HTML deck" and the new `o` row under OUT.
module: taskboard/modals.py
examples: (TC-4761) `R`, `?` → the window holds "export this view · HTML deck"; "SVG" `0` and "PNG" `0` occurrences
examples: (TC-4762) the window holds "open the last export (10 s)" on the row of "o"
examples: (AT-4506) `R`, `?` → "x" "export this view · HTML deck" and "o" "open the last export (10 s)" listed

fit_bar
req: LLR-4505.1, LLR-4505.2, LLR-4505.3, LLR-4505.4
in: int width; str view; str layer = "more"
out: tuple(list[tuple[str, str]] entries, int dropped)
func: UNCHANGED code (ruling 1: the fit rules stand). The KEYMAP `H` row keeps its current seat between `n` and `@` and becomes `Key("H", "H", "report_export", "Report", primary=True, group="misc")` (bar True); no seat or palette-order change. E3-P1's 10 views × {80, 118} × {primary, more} table is recorded in e3-addenda.md.
module: taskboard/keymap.py
examples: (TC-4751) 10 main views × widths `80` and `118`, layer "primary" → "H" among the drawn keys, `20`/`20` (E3-P1)
examples: (TC-4752) the same 20 cases → the base keys ⊆ the new keys and dropped equal (`0` everywhere), `20`/`20` (E3-P1)
examples: (TC-4753) the same 20 cases → at most `1` word lost, `20`/`20`: swimlanes at 118 loses "Focus", at 80 loses "Quit"; agenda, gantt, chainmap lose none (E3-P1)
examples: (TC-4754) width `250`, "swimlanes", "primary" → the plain bar holds "H Report"; it first fits at `193` columns (E3-P1; ruling 16)
examples: (AT-4506) 118x30 and 80x24 → the main key bar shows "H"; `H` → the ReportExport modal opens (unchanged)

HelpModal._key_texts
req: LLR-4505.5
in: int width
out: tuple(str band, str glob)
func: UNCHANGED code (modals.py): the band lists `bar_keys(mode)` ("more" layer, now holding `H` before `↓`) and the global line lists `global_keys(mode)` (now without `H`), so `H Report` appears once.
module: taskboard/modals.py
examples: (TC-4755) each of the 10 main views → the band holds "H   Report" `1` time and the global line holds no "H Report"; `10`/`10`
examples: (AT-4506) `?` on the main screen → the help lists "H   Report" once

global_keys
req: LLR-4505.5
in: str view
out: list[Key] keys
func: UNCHANGED code; with `H` bar=True it leaves this list.
module: taskboard/keymap.py
examples: (TC-4755) view "swimlanes" → shows ["o", "i", "p", "P", "f", "c", "R", "A", "N", "n", "@", "#", "I", "S"] (E3-P1; base had "H" between "n" and "@")

bar_keys
req: LLR-4505.5
in: str view; str layer = "more"
out: list[Key] keys
func: UNCHANGED code; `H` is now in both layers at its existing declaration seat: before `↓` in "primary" and "more".
module: taskboard/keymap.py
examples: (TC-4755) view "swimlanes", layer "more" → the last keys "⇥", "H", "↓", "↑", "←", "→" (E3-P1)

## Entities

[Data: keymap.KEYMAP]
in: tuple[Key, ...]
desc: CHANGED: the `H` row stays between `n` and `@`, with `primary=True` and `bar` True; its comment and the nearby `N` comment no longer say `H` is off the bar (ruling 16). The palette order is unchanged. The "more" layer drops one key more in every measured view at 80 and at gantt/kanban at 118 (E3-P1 table in e3-addenda.md); test_TC_3117 is rewritten to pin X-3 (ruling 7), and TC-4321 drops `H` from `global_keys` (ruling 15).

[Data: keymap.PRESENT_KEYS]
in: tuple[PresentKey, ...]
desc: CHANGED: the `x` row reads `PresentKey((("x", "export"),), "x", "export this view · HTML deck", "OUT")`; a new row `PresentKey((("o", "open_export"),), "o", "open the last export (10 s)", "OUT")` follows it. Nothing else.

[I/O: reports/present-*.svg]
desc: REMOVED (X-2): no node writes it any more.

[I/O: reports/present-*.png]
desc: REMOVED (X-2): no node writes it any more.

[Interface: presentation keys window]
desc: `PresentKeys` (`?` in `R`): the rows of PRESENT_KEYS
offers: "x export this view · HTML deck" → PresentScreen.action_export
offers: "o open the last export (10 s)" → PresentScreen.action_open_export

[Interface: key bar]
desc: CHANGED: the primary layer shows `H` before `↓ ↑` in every main view; `H Report` with its word from 193 columns (ruling 16)
offers: "H Report" → TaskboardApp.action_report_export

## Edges

PresentScreen._deck_lane.lane ──▶ present_deck_boards.lane
PresentScreen.action_export ──▶ [I/O: reports/present-*.html]
PresentScreen.action_export ──▶ [Data: TaskboardApp._report_offer]
TaskboardApp._on_report_chosen ──▶ [Data: TaskboardApp._report_offer]
[Data: keymap.KEYMAP].bar ──▶ bar_keys
[Data: keymap.KEYMAP].bar ──▶ global_keys
[Data: keymap.PRESENT_KEYS] ──▶ present_bindings
[Outside: key x] ──▶ PresentScreen.action_export
when: PresentScreen is the top screen (priority binding); below 36 columns it only toasts

## Findings

finding P-A-1 the rulings and LLR-4506.4 disagree on the presentation's hint row
anchor: PresentScreen._keys_hint
seen: ruling 1 says "the presentation's hint and `?` window name the export as HTML"; ruling 6 says "The R hint names x (HTML), not H"; LLR-4506.4 and X-4 say the hint reads exactly as at base ("x export"), and 6 test files pin "x export"
cause: the rulings can be read as "the hint names `x`, whose export is now HTML" or as "the hint's words change"
effect: a changed wording shifts which wording fits at the boundary widths, so more of the hint than the export word changes (against X-4)
decision: resolved — ruling 10: the hint row keeps its base wording and LLR-4506.4 stands; the hint parts of rulings 1 and 6 are withdrawn; HTML is named in the `?` window (ruling 4) and the README only

finding P-A-2 ruling 4 names the `o` row "o open export"; LLR-4506.2 fixes the words "open the last export (10 s)"
anchor: present_bindings
seen: 00-e1-rulings.md ruling 4 vs 01-requirements.md LLR-4506.2
cause: the ruling is a summary, the requirement fixes the text
effect: none if the ruling's words are the action's name
decision: resolved — ruling 21/F-9 accepts action "open_export", words per LLR-4506.2

finding P-A-3 `o` in `R` acts at every width
anchor: PresentScreen.action_open_export
seen: every other key of `R` but `esc`/`q` does nothing below 36 columns (`_narrow`); LLR-4503.2 has no width condition
cause: an offer from a wide `x` can still be live after the terminal is narrowed
effect: `o` opens the browser on a narrow screen; nothing on the screen changes, so the "nothing would show what it did" reason does not apply
decision: resolved — ruling 21/F-9 accepts no width check on `o` (as LLR-4503.2 says)

finding P-A-4 the "more" layer drops keys and the named law guard needs a recorded re-baseline
anchor: fit_bar
seen: E3-P1 re-measured 10 views × {80, 118} × {primary, more}: the more layer drops one additional key in all 10 views at 80 and in gantt/kanban at 118; gantt 80 primary gains `H`, and gantt 118 more becomes `… / H ↓ +3`; the full table is in e3-addenda.md
cause: `H` joins both bar layers at its existing seat (bar True, primary True)
effect: LLR-4505.2/.3 hold on the primary layer; `test_colour_budget_app.py`'s two KEYBAR_BASE strings and TC-4321's global-key expectation go RED until their justified updates
decision: resolved — rulings 15 and 16 accept the current seat; E4 re-baselines KEYBAR_BASE with comment and evidence, and TC-4321 drops `H`

finding P-A-5 the deck's date is the press's, the frames' is the presentation's open
anchor: PresentScreen.action_export
seen: `PresentScreen._today` is frozen at open; `H` uses `date.today()`
cause: LLR-4501.3 compares with `H` "on the same day"; the name's `<date>` is today's date (Definitions)
effect: across midnight the deck is dated the new day while the frame keeps the old one
decision: resolved — ruling 21/F-9 accepts `date.today()` at the press, as `H`

finding P-A-6 an unlisted board's key is "#0" for `x` and "#<n>" for `H`
anchor: PresentScreen._deck_lane
seen: `H` keys an unlisted board by its position among every loaded board (`#<n>`), `x` passes one board (`#0`); the key reaches the bytes (`data-project="#0:pA"`)
cause: LLR-4501.3's While clause did not exclude an unlisted board
effect: on `--open` with a non-empty registry the views-1/2 bytes differ from `H`'s in the keys
decision: resolved — ruling 17 adds "the presented board is in the registry" to LLR-4501.3; TC-4703 uses a registry board (as AT-4501)

finding P-A-7 LLR-4506.5 is an inspection of README.md, which no function holds
anchor: PresentScreen.action_export
seen: the requirement checks docs text
cause: README is docs, outside both groups' source files
effect: it is carried here as an `oracle:` and an inspection example (TC-4765)
decision: resolved — ruling 21/F-9 accepts keeping it on this node; E4 group A edits the four README lines

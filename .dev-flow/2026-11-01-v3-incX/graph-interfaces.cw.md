# Inc X — shared interfaces (frozen at E2; owned by the orchestrator: a group PROPOSES a change as a finding in its own file, never edits here)

> The seams between the two prototype groups. **Group A** owns `taskboard/app.py` + `taskboard/keymap.py`
> (+ the README rows, docs only): `PresentScreen` (the `x` export, the new `o`, the presented
> board's lane), the shared write → toast tail `TaskboardApp._write_report`, the shared
> `TaskboardApp._report_offer`, the `KEYMAP` `H` row and the `PRESENT_KEYS` rows. **Group B** owns
> `taskboard/views.py`: the deck scope (`present_deck_boards`), the removals (X-2) and the file name.
> `report_html.py` and `report_deck.py` stay unchanged; the source budget is app, views, keymap = 3.
> No cover change (ruling 8). Only the DIFFERENCES from `graph-baseline.cw.md` (509d444) are written;
> a node marked "unchanged" is listed only because a seam or an example needs it.
> Rulings applied: 00-e1-rulings.md 1–22.
> Fixture X (synthetic, used by every example unless a line says otherwise): today 2026-11-01; registry
> `S/boards.json` lists one board `main` named "Main", colour "sky", file `S/boards/main/board.json`
> (folder `F` = `S/boards/main/reports`); phases ["Backlog", "Doing", "Done"]; projects Alpha `pA`
> (present_rank 1), Beta `pB` (present_rank 0); tasks a1 "a-open-1" (pA, Doing, 2026-10-28 → 2026-11-05,
> notes "ask @ana.ruiz", urls ["https://example.test/capability-a1"]), a2 "a-done" (pA, Done),
> a3 "a-gate" (pA, milestone, class `gate`, depends on a1), b1 "b-open" (pB). People
> {ana.ruiz: "Ana Ruiz"}; classes {gate: "Gate" ▲}. `_report_clock` replaced by a fake clock that starts
> at `100.0`. Probe P-X1 (read-only, `%TEMP%\incX-e2\probe_deck.py`, cwd and PYTHONPATH = this worktree,
> `taskboard.__file__` = `…\taskboard-wt\x-html\taskboard\__init__.py`) simulated
> `present_deck_boards` with `copy.copy` on fixture X and printed the values cited "(P-X1)".
> Probe P-X2 (`%TEMP%\incX-e2\probe_bar.py`, same tree) swapped `keymap.KEYMAP` in memory for `H` at its
> current seat with bar=True, primary=True and printed the bars cited "(P-X2)"; E3-P1 re-measured that seat.

## Nodes

present_deck_boards
req: LLR-4501.5, LLR-4501.6, LLR-4501.7, LLR-4501.8, LLR-4501.9, LLR-4501.12, LLR-4501.15, LLR-4502.1, LLR-4502.2, LLR-4502.3, LLR-4502.4, LLR-4502.5, LLR-4502.7
in: tuple[str?, str, str, Board] lane; str? project_id
out: list[tuple[str?, str, str, Board]] boards
func: NEW (group B, views.py). `lane` = the presented board as `report_html.extract` takes it, `(registry id | None, name, colour, Board)` (group A builds it, `PresentScreen._deck_lane`). Returns `[(id, name, colour, proxy)]`, exactly one entry, where `proxy = copy.copy(board)` with two NEW lists and nothing else changed. For views 1/2, resolve `project_id` exactly as `render_present`: `board.project_by_id(project_id)`, else the first of `board.visible_projects(False)`, else none; `proxy.projects` holds that project whatever its own `show_in_present`. For view 3, `proxy.projects` = `[p for p in present_order(board) if p.show_in_present]`. `proxy.tasks` = shallow copies, IN BOARD ORDER, of the tasks in `present_tasks_m(board, p.id)[1]` for a held project p (shown, not archived, not a milestone of a hidden class, open and done), each with `urls = []`; every other per-task value stays unchanged. Folds (`_folded`) are not read. Source Project and Task objects are never changed; the proxy is handed only to `extract` (read-only, TC-3101), never cached or saved. Board order of the tasks keeps the deck's bytes equal to `H`'s over the same URL-cleared proxy when nothing is hidden.
module: taskboard/views.py
examples: (TC-4705) a board of 3 projects, project_id "pA" whose show_in_present is `False` → boards[0] proxy projects ["pA"]; the deck holds "Alpha" and neither other name
examples: (TC-4706) ranks C=`0`, A=`1`, B=`2`, project_id `None` → proxy projects "Gamma", "Alpha", "Beta" (P-X1 prints view3 project order ['Gamma', 'Alpha', 'Beta'])
examples: (TC-4707) lane ("main", "Main", "sky", board), a registry of 2 boards → boards has `1` entry, its name "Main"
examples: (TC-4708) project B folded with `enter` in view 3 → B's proxy tasks are both its shown tasks (folds are not an input)
examples: (TC-4709) Alpha with 2 open and 1 done shown task → `3` proxy tasks of pA; the deck slide reads "3 tasks" and holds "a-done" (P-X1)
examples: (TC-4712) every project hidden on the rail, project_id `None` → proxy projects [] and the deck reads "No project in this scope holds a task." (P-X1: empty True, scope boards ['Main'])
examples: (TC-4715) project_id "missing", visible projects [pA, pB] → proxy projects [pA], the deck holds "Alpha", `0` exceptions
examples: (TC-4721) task "HIDDEN-T-7Q" id "hidt7q" with show_in_present `False` → in no proxy list; `0` occurrences in the deck (P-X1, views 1 and 3)
examples: (TC-4722) project "HIDDEN-P-4K" hidden, its task "UNDER-HIDDEN-P" shown, project_id `None` → neither in the proxy (P-X1)
examples: (TC-4723) "ARCH-T" (archived task), "ARCH-P-TASK" (task of an archived project), "NO-PROJ-T" (no project) → none in the proxy; no "Inbox" in the deck (P-X1)
examples: (TC-4724) milestone "HID-CLASS-MS" of a class hidden in `#` → not in the proxy (present_tasks_m) (P-X1)
examples: (TC-4725) class "CLASS-ONLY-HIDDEN" used only by a hidden task → extract's marks over the proxy hold no such class; the deck's legend `0` occurrences (P-X1)
examples: (TC-4727) a1 urls ["https://example.test/capability-a1"] → that URL `0` occurrences in the deck; source a1.urls unchanged
examples: (AT-4501) registry of 2 boards, `space` on "HIDDEN-T-7Q" in view 1 → the proxy holds pA only, without that task
examples: (AT-4502) projects A, B, C; C ranked first; B hidden on the rail; A folded → proxy projects "C", "A"; A with all its shown tasks

extract
req: LLR-4501.3, LLR-4501.4, LLR-4501.7
in: list boards; dict people; dict marks; date today; str? project = None
out: dict d
func: UNCHANGED (report_html.py stays byte-unchanged). The scope input of the deck writer, frozen: group A calls it with `boards = present_deck_boards(lane, pid)`, `app.people.people`, `app.marks.marks`, `date.today()` at the press, and `project = None` in view 3, else the key `<lane id, or "#0" when the id is None>:<resolved project id>` — the key `H` builds for a registry board (app.py:3006-3009), so the dict of views 1/2 equals `H` → `p`'s over the same URL-cleared proxy.
module: taskboard/report_html.py
examples: (TC-4703) the URL-cleared proxy of pA, project "main:pA" → scope kind "project", the same dict as `H`'s extract over that proxy
examples: (TC-4704) the URL-cleared proxy of view 3, project `None`, a registry of one board → scope kind "all", boards ["Main"]

render
req: LLR-4501.3, LLR-4501.4, LLR-4501.12
in: dict d
out: str page
func: UNCHANGED (ruling 8: no cover change; report_deck.py's rendering is the base code). The deck writer `H` → `c` uses; group A calls it as `render(d)`, so the `x` deck is byte-identical to `H`'s for the same d.
module: taskboard/report_deck.py
examples: (TC-4703) d of fixture X's URL-cleared proxy, scope "main:pA" → the page's scope element reads "Project Alpha on Main", and the bytes equal `H` `p` `c`'s deck over that proxy
examples: (TC-4704) d of view 3's URL-cleared proxy (Alpha, Beta), a registry of one board → the scope element reads "All loaded boards (1): Main", and the bytes equal `H` `c` `o`'s deck over that proxy
examples: (TC-4712) d with no project → the overview reads "No project in this scope holds a task."

present_name
req: LLR-4501.1, LLR-4501.2
in: str? project_name; date today
out: str name
func: NEW (group B, views.py; rulings 12 and 21/F-11): returns `present-<slug>-<today>.html` for a project name and `present-<today>.html` for None. It takes the slug through a function-local `from .report_html import slug`, with "project" when the slug is empty; no local slug rule. Pure; never the `deck-…`/`workspace-…` names, so `x` never overwrites `H`'s files.
module: taskboard/views.py
examples: (TC-4701) project_name "Alpha", today 2026-11-01 → name "present-alpha-2026-11-01.html" (views 1 and 2 write the same file)
examples: (TC-4701b) project_name "Website Redesign", today 2026-11-01 → name "present-website-redesign-2026-11-01.html"
examples: (TC-4702) project_name `None`, today 2026-11-01 → name "present-2026-11-01.html"

PresentScreen.action_open_export
req: LLR-4503.2, LLR-4503.3, LLR-4503.6
in:
out: None
func: NEW (group A, app.py; rulings 6 and 21/F-12: `o` binds on PresentScreen and consumes the app's shared offer). Bound by the new PRESENT_KEYS row `(("o", "open_export"),)`, priority like every row. Takes `offer = self.app._report_offer` and sets that slot to None; when offer is not None and `self.app._report_clock() < offer[1]`, calls `self.app._open_report(offer[0])` (os.startfile, else webbrowser.open of the URI; its failure toast unchanged). Otherwise nothing: no URL fallback, no toast. Never raises.
module: taskboard/app.py
modify: [Data: TaskboardApp._report_offer] (clear)
examples: (TC-4732, root action_open_export) `x` in view 1 at clock `100.0`, `o` → opener called once with "present-alpha-2026-11-01.html"
examples: (TC-4733, root action_open_export) no `x`, `o` → opener called `0` times; `x`, clock `110.0`, `o` → `0` calls; `x`, `o`, `o` → `1` call in total; `x`, `esc`, `o` → `1` call with the deck's path
examples: (TC-4736, root action_open_export) os.startfile raises OSError → error toast "Could not open the report present-alpha-2026-11-01.html."
examples: (AT-4503) `R`, `x`, `o` → the handler gets the deck's path once; `o` again → no second call

## Entities

[Data: TaskboardApp._report_offer]
in: tuple[Path, float]?
desc: CHANGED: the existing single-use `o` offer, (the written report, `_report_clock()` + 10), now shared by `H` and `x`; set by their successful writes, cleared by a failed write and by every `o`; survives leaving `R`, so the toast stays true; one slot and one expiry rule.

[I/O: reports/present-*.html]
desc: NEW: `<board folder>/reports/present-<project slug>-<date>.html` (views 1/2) or `present-<date>.html` (view 3), written by `PresentScreen.action_export` from `render(d)` (bytes = `H` → `c`'s over the same URL-cleared proxy, rulings 8 and 14); a same-day export overwrites; never a `deck-*`/`workspace-*` name.

[Outside: key o in R]
desc: PRESENT_KEYS row `o` → `open_export`, a priority binding on PresentScreen; the app's `o` (`open_url`) stays as it is and does not pass the modal.

## Edges

present_deck_boards.boards ──▶ extract.boards
extract.d ──▶ render.d
PresentScreen.action_export.project_name ──▶ present_name.project_name
PresentScreen.action_export.today ──▶ present_name.today
[Data: TaskboardApp._report_offer] ──▶ PresentScreen.action_open_export
PresentScreen.action_open_export ──▶ [Data: TaskboardApp._report_offer]
[Outside: key o in R] ──▶ PresentScreen.action_open_export
when: PresentScreen is the top screen

## Findings

finding I-1 the cover of ruling 3 breaks the byte identity of LLR-4501.3 and LLR-4501.4
anchor: render
seen: (P-X1) with `presented` False the `x` deck of fixture X equals `H`'s byte for byte, views 1/2 and 3; ruling 3 puts "Presented · Alpha" / "Presented · 2 projects" on the cover where `H` writes "Project Alpha on Main" / "All loaded boards (1): Main"
cause: ruling 3 (cover) and LLR-4501.3/.4 (bytes ==) were written apart; rulings override
effect: a literal `bytes ==` test is RED by design
decision: resolved — ruling 8: the cover change is dropped; `render(d)` is unchanged, LLR-4501.3/.4 stand as written (`bytes ==`), and the examples test plain byte equality

finding I-2 ruling 3's file name differs from LLR-4501.1, .2, .11, LLR-4504.1, AT-4501 and AT-4502
anchor: present_name
seen: LLR-4501.1 `deck-<board slug>-<project slug>-<date>.html`, LLR-4501.2 `deck-<date>.html`, LLR-4501.11 a board slug in the name, LLR-4504.1 "0 `present-*` files", AT-4501 toast `Report written: deck-…`, AT-4502 `deck-<date>.html`; LLR-4501.1's negative control ("keep the `present-<slug>-<date>` stem: RED") is now the design
cause: ruling 3 gives `x` its own name `present-<project-slug|all>-<YYYY-MM-DD>.html`
effect: the graph uses ruling 3 under the same TC ids; the requirement texts still say `deck-…`
decision: resolved — ruling 9: the six texts are amended to `present-<project slug|all>-<date>.html` (LED-2026-11-01-incX.3); LLR-4504.1 checks 0 `.svg`, 0 `.png` and 1 `present-*.html` per press; LLR-4501.1's and LLR-4501.2's NCs write `H`'s `deck-…` name; LLR-4501.11 keeps only its cover arm

finding I-3 ruling 3's cover line has no requirement
anchor: render
seen: no LLR states the text "Presented · <project name>" / "Presented · <n> project(s)"
cause: ruling 3 came after E1
effect: the cover line is designed (`_presented_line`, group B) but traced only through TC-4703/4704
decision: resolved — ruling 8: no cover line, so no new LLR; `_presented_line` and the `_cover` change are removed from group B

finding I-4 the slice and two texts outside ruling 9's list still describe report_deck.py as unchanged
anchor: present_name
seen: 01-requirements.md §1 "Not in" lists `report_deck.py` as reused unchanged; §6 says "13 units in 3 source files" and "`report_deck.py` … unchanged on purpose"; HLR-4501's NC reads "(no `deck-*.html`)"; `present_name` (ruling 9) is a new unit in report_deck.py
cause: ruling 9 lists six ids to amend; the scope, the slice and HLR-4501 were not among them
effect: the slice under-counts by one unit and one source file (14 units in 4 files, still within ruling 3's budget); HLR-4501's NC names the wrong file, though TC-4701 is still RED at base (base `x` writes `.svg`)
decision: resolved — rulings 12 and 19: `present_name` is a new unit in views.py with a function-local slug import; report_deck.py stays unchanged; §1, §6 and HLR-4501's NC are amended

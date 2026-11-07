# Code-Wire prototype — Inc MR-b — group S (`taskboard/app.py`, `PresentScreen`)

Only the differences from `graph-baseline.cw.md` (2ce3943). S changes ONE unit (`_shown_ids`); the other nodes keep their code and change behaviour through it or through V's view-3 stops (`[Data: PresentAll.stops]`, `graph-interfaces.cw.md`). No key, binding, hint row or `?` line changes (R-2). Sources, fixture and ids: as in `graph-interfaces.cw.md`.

## Nodes

PresentScreen._shown_ids
req: LLR-4653.1, LLR-4653.3
in:
out: list[str] ids
func: CHANGED: the ids of `present_stop_order(present_tasks_m(self._board, self._project_id)[0])`, read live as at base. The same order V's `render_present` draws its milestone row, briefs and blocks in, so a step of the cursor is a step along what the frame shows
module: taskboard/app.py
examples: (TC-4921) `ppr` → ["tm2", "tm3", "tm4", "tm5", "tstore", "ttele", "ttrain", "trota"] (base ["tm2", "tstore", "tm3", …], P-1)
examples: (TC-4923) `ppd` → ["th1", "tha", "thr"]

PresentScreen._cursor
req: LLR-4653.3
in: list[str] ids
out: str? cursor_id
func: code UNCHANGED: `_cursor_id` when in `ids`, else `ids[0]`, else None. With the new `_shown_ids`, `ids[0]` is the first stop, the renderer's own fallback (`[Data: present stop order]`, SEAM-2)
module: taskboard/app.py
examples: (TC-4923) `R` opened on `ppr` with no cursor → "tm2"; on `ppd` → "th1" (base "tha")
examples: (TC-4923) `_cursor_id` "tm3", then tm3 hidden → "tm2", the stop order's first

PresentScreen.action_move
req: LLR-4653.1, LLR-4653.2
in: int delta
out: None
func: code UNCHANGED. Views 1/2: one place along `_shown_ids()` (the stop order), clamped, note scroll reset. View 3: one place along `_stops()` (`PresentAll.stops`, now with one stop per drawn milestone on the shared row), clamped
module: taskboard/app.py
modify: [Data: PresentScreen state] (replace)
examples: (TC-4921) view 1 `ppr`, cursor "tm2", `↓`×4 → "tm3", "tm4", "tm5", "tstore"; then `↑` → "tm5"
examples: (TC-4922) view 3 at 118x30, cursor ("proj", "ppr"), `↓`×5 → ("task","tm2"), ("task","tm3"), ("task","tm4"), ("task","tm5"), ("task","tstore"); `5`/`5`
examples: (AT-4651) view 1 at 118x30 and 80x24 from "tm2": `↓` → tm3 (its title beside `■2`), `↓` → tm4 (`▲2`, label tag `2/2`), `↓` → tm5, `↓` → `Pilot store list`
examples: (AT-4652) view 2 (`2`): the same walk, tm2 → tm3 → tm4 → tm5 → tstore
examples: (AT-4653) view 3: `↓` from *Pilot rollout*'s head walks tm2..tm5, then tstore, ttele, ttrain, trota

PresentScreen.action_side
req: LLR-4653.1, LLR-4653.6
in: int delta
out: None
func: code UNCHANGED: where view 3 draws the rail (≥ 100 columns) `←`/`→` move the focus between rail and timeline; anywhere else `action_move(delta)`, so in views 1/2 `→` is one step along the stop order. The bindings and the `?` window are not touched
module: taskboard/app.py
modify: [Data: PresentScreen state] (replace)
examples: (TC-4921) view 1 `ppr`, cursor "tm5", `→` → "tstore" (`side` = move, base)
examples: (TC-4926) `PresentScreen.BINDINGS` key set = base; `PresentKeys(view).lines()` text = base for views 1, 2, 3; `2`/`2`
examples: (AT-4653) view 3 at 118x30, cursor on a ppr stop, `←` → the rail on *Pilot rollout* (base)
examples: (AT-4655) `?` after the hostile-title walk → the window is as at base

PresentScreen.action_hide
req: LLR-4653.4
in:
out: None
func: code UNCHANGED: `space` hides the cursor's task alone (`show_in_present` False, saved) and moves the cursor to the next of `_shown_ids()` (the previous at the end); in view 3 `_hide_all` does the same over `PresentAll.stops`. On the shared row the cursor milestone is one stop, so it alone is hidden
module: taskboard/app.py
modify: [Data: Task.show_in_present] (replace); [Data: PresentScreen state] (replace)
examples: (TC-4924) view 1 `ppr`, cursor "tm3", `space` → tm3 `show_in_present` False; tm2, tm4, tm5 still on the row; cursor "tm4"; tm4 alone in its cell: `▲` with no `2`; `3`/`3`
examples: (TC-4924) view 3, cursor ("task", "tm3"), `space` → the same, cursor ("task", "tm4")
examples: (AT-4654) view 1, cursor tm3, `space` → row holds tm2, tm4, tm5; `u` lists tm3; `a` → tm3 back on the row; class Review hidden in `#`, then `R` → the row holds tm4, tm5; h1 hidden → *Docs & handover* draws no row

## Entities

[Data: PresentScreen state]
desc: unchanged fields. `_cursor_id` can now name any drawn milestone of the shared row (one stop each); `_all_cur` can be ("task", <milestone id>) on view 3's shared row. Leaving and entering view 3 (`action_view`) carry them as at base

## Edges

[Outside: keys ↑↓] ──▶ PresentScreen.action_move
[Outside: keys ←→] ──▶ PresentScreen.action_side
[Outside: key space] ──▶ PresentScreen.action_hide
PresentScreen._shown_ids ──▶ PresentScreen._cursor

# Inc X — E3 addenda for E4

Rulings 12–22 are applied in the requirements, ledger, graphs and seams. This file records the accepted measurement and the remaining E4 work; it does not expand scope.

## F-3 / F-4 key-bar measurement (rulings 15–16)

Read-only in-memory probe of `keymap.KEYMAP`, with only `H` changed to `bar=True, primary=True` at its current seat between `n` and `@`. Each cell is `d base→new; w base→new`: `d` = dropped keys, `w` = entries still drawing their word. Primary dropped is 0→0 in all 20 cases; primary loses at most one word in all 20. `H Report` first fits at 193 columns.

| View | 80 primary | 118 primary | 80 more | 118 more |
|---|---|---|---|---|
| swimlanes | d 0→0; w 3→2 | d 0→0; w 9→8 | d 12→13; w 0→0 | d 0→0; w 1→0 |
| agenda | d 0→0; w 3→3 | d 0→0; w 9→9 | d 11→12; w 0→0 | d 0→0; w 2→1 |
| gantt | d 0→0; w 3→3 | d 0→0; w 9→9 | d 14→15; w 0→0 | d 2→3; w 0→0 |
| kanban | d 0→0; w 3→2 | d 0→0; w 9→8 | d 18→19; w 0→0 | d 6→7; w 0→0 |
| focus | d 0→0; w 3→2 | d 0→0; w 9→8 | d 12→13; w 0→0 | d 0→0; w 1→0 |
| chainmap | d 0→0; w 3→3 | d 0→0; w 9→9 | d 11→12; w 0→0 | d 0→0; w 2→1 |
| flow | d 0→0; w 4→3 | d 0→0; w 10→9 | d 9→10; w 0→0 | d 0→0; w 3→2 |
| standup | d 0→0; w 4→3 | d 0→0; w 10→9 | d 9→10; w 0→0 | d 0→0; w 3→2 |
| people | d 0→0; w 4→3 | d 0→0; w 10→9 | d 9→10; w 0→0 | d 0→0; w 3→2 |
| setup | d 0→0; w 4→3 | d 0→0; w 10→9 | d 12→13; w 0→0 | d 0→0; w 0→0 |

## E4 implementation and test addenda

1. **F-3 law guards.** Re-baseline `KEYBAR_BASE` in `tests/test_colour_budget_app.py` following its own comment-plus-evidence convention: gantt 80 primary becomes `? Map  ; More  q Quit  B  1  2  3  4  5  6  7  8  9  0  ↵  a  e  d  L  H  ↓  ↑`; gantt 118 more becomes `?  ;  q  B  1  2  3  4  5  6  7  8  9  0  ↵  a  e  d  L  x  X  v  u  t  T  M  [  ]  !  b  +  -  m  F  esc  /  H  ↓ +3`. This is a recorded, law-driven re-baseline, not a weakened guard. TC-4321 drops `H` from `global_keys("gantt")`; the packet records both justifications.
2. **F-10 file-set oracle.** After each press, `reports/` holds that scope's `present-*.html`, 0 `.svg`, 0 `.png`, and no other file is new or changed. The second press of views 1/2 may rewrite the same path and therefore need not create a new directory entry.
3. **S-2 proxy lifetime.** Never store or cache the proxy or its `boards` list on `PresentScreen` or the app. Run TC-4710's 6/6 sha256 control and its `board.save()`-in-export mutant in the mutant table.
4. **S-4 path safety.** Add the traversal test: project `..\..\evil` writes `present-evil-<date>.html`; project `CON` writes `present-con-<date>.html`; each resolved path's parent equals the resolved reports folder `F`.
5. **S-6 URI failure.** `_open_report` catches `(OSError, ValueError)`; test a relative path whose `as_uri()` raises ValueError off Windows and assert the exact existing error toast with 0 escaped exceptions.
6. **F-12 shared offer.** Test `x`, `esc`, `o`: the app's shared single-use offer opens the just-written deck once, so the toast remains true after leaving `R`. A failed `x` clears that same slot.
7. **F-13 stale text and dead state.** Update `tests/test_markup_census.py`'s "shared with the x export" reason. Put the stale `PresentKeys` docstring "Never exported: `x` writes the frame only." in BACKLOG because `modals.py` is outside the slice. `_project_name` is now consumed by `present_name` on the normal views-1/2 path; do not remove it or change constructor tests. HLR-4501's NC is already corrected in the design.
8. **P-B-4 documentation.** Update the named Edge/SVG lines in `docs/ARCHITECTURE.md`; mark the three frozen prototype scripts historical in their folder READMEs or BACKLOG (ruling 5). Fold the individually named canon ids at batch end.
9. **S-7 renderer boundary.** The implementation must render only through `report_deck.render`; do not add another HTML sink or change the renderer.

## Known limits to record in BACKLOG

- **S-1:** per-task metadata other than URLs that the presentation does not draw (priority and `<n>d in phase`) remains unchanged in the deck.
- **F-6:** an archived presented project remains a known limit; no guard is added.
- **S-4:** same-day overwrite and same-slug project-name collisions remain accepted; F-11 removes only the view-3/`All` collision.
- **S-5:** a planted `reports/` symlink or junction is followed, matching `H`; no guard is added.
- **F-13:** the stale `PresentKeys` docstring remains until a separate `modals.py` change.
- **S-6(2):** no residual remains after F-12; the shared app offer supersedes the reviewer's stale-toast limitation.

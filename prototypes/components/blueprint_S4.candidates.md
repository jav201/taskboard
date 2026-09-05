# blueprint · S4 — modal dialog — candidates

Frame: `blueprint_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("blueprint")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `pane_split` — **refused**

- **element drawn:** the divider between the two panes -- NOT DRAWN
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** 'not one element is boxed, at any width' -- the ten marks this language draws contain no vertical stroke, so a pane rule is unconstructable.  The division is AIR at a second datum, which is what a drawing office does with two views on one sheet

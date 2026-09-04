# blueprint · S4 — modal dialog — candidates

Frame: `blueprint_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("blueprint")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.overlay` — **refused**

- **element drawn:** the modal's box -- NOT DRAWN; registration marks instead
- **frame rows:** 17
- **proposed signature:** `Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]`
- **the commitment it must honour:** 'not one element on this sheet is boxed' and the ten marks contain no vertical stroke and no rectangle junction, so a dialog box is unconstructable.  What marks the selection is the REGISTRATION PAIR (`┌ ┐` above, `└ ┘` below -- four corners that never join), which is this language's selection mechanism already

## `pane_split` — **refused**

- **element drawn:** the divider between the two panes -- NOT DRAWN
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** 'not one element is boxed, at any width' -- the ten marks this language draws contain no vertical stroke, so a pane rule is unconstructable.  The division is AIR at a second datum, which is what a drawing office does with two views on one sheet

## `Kit.field_row` — **evoked**

- **element drawn:** the detail pane's caption -> value rows
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.field_row(self, caption: str, value: str, w: int, state: str = DEFAULT) -> str`
- **the commitment it must honour:** the definition-list row a detail pane, a KPI tile and a settings summary all are -- COMPONENTS.md's census lists the stat tile and has no row for this.  It is the single most reused shape in the six screens and the ONE the contract has no seat for, so all five languages are currently drawing LEDGER's mechanism (dot leaders): ledger's own answer generalised into four languages that never chose it, which is the palette-swap failure with a leader instead of a hue

## `Kit.knockout_cell` — **evoked**

- **element drawn:** the knockout on the default answer
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.knockout_cell(self, text: str) -> str`
- **the commitment it must honour:** 'exactly ONE element per view reverses to a pale ground with dark ink, and it is the hero.'  On a board that cell is the title block's STATE; on a confirm the hero is the answer, so the knockout MOVES -- and the sheet must still carry exactly one

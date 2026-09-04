# prism · S4 — modal dialog — candidates

Frame: `prism_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("prism")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.field_row` — **evoked**

- **element drawn:** the detail pane's caption -> value rows
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.field_row(self, caption: str, value: str, w: int, state: str = DEFAULT) -> str`
- **the commitment it must honour:** the definition-list row a detail pane, a KPI tile and a settings summary all are -- COMPONENTS.md's census lists the stat tile and has no row for this.  It is the single most reused shape in the six screens and the ONE the contract has no seat for, so all five languages are currently drawing LEDGER's mechanism (dot leaders): ledger's own answer generalised into four languages that never chose it, which is the palette-swap failure with a leader instead of a hue

## `Kit.overlay` — **evoked**

- **element drawn:** the modal's border and the board's ±1 grey step behind it
- **frame rows:** 11, 12, 13, 14, 15, 16, 17, 18
- **proposed signature:** `Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]`
- **the commitment it must honour:** 'depth by ±1 grey step, never borders -- borders are RESERVED for modals'.  This language is the only one of the five whose commitment licenses the box, and the recede is `depth_ground()`, which the kit already computes.  The primitive is missing; the MECHANISM is not

## `pane_split` — **evoked**

- **element drawn:** the vertical divider between the list and the detail pane
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** the language's own answer to 'two regions side by side' -- a rule, a grey step, air, or a refusal; COMPOSITION is a per-kit commitment (COMPONENTS.md: 'composition is the last palette-swap')

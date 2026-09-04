# naught · S4 — modal dialog — candidates

Frame: `naught_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("naught")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.overlay` — **refused**

- **element drawn:** the modal's frame -- NOT DRAWN
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]`
- **the commitment it must honour:** 'no frames at all' is one of this language's four commitments, so an overlay BOX is unconstructable.  The separation is the lattice going unlit behind a lit question, and the count is a DRAWN sprite because a count is exactly what this language draws

## `Kit.field_row` — **evoked**

- **element drawn:** the detail pane's caption -> value rows
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.field_row(self, caption: str, value: str, w: int, state: str = DEFAULT) -> str`
- **the commitment it must honour:** the definition-list row a detail pane, a KPI tile and a settings summary all are -- COMPONENTS.md's census lists the stat tile and has no row for this.  It is the single most reused shape in the six screens and the ONE the contract has no seat for, so all five languages are currently drawing LEDGER's mechanism (dot leaders): ledger's own answer generalised into four languages that never chose it, which is the palette-swap failure with a leader instead of a hue

## `Kit.recede` — **evoked**

- **element drawn:** the inactive board, drawn as an unlit lattice
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.recede(self, rows: list[str]) -> list[str]`
- **the commitment it must honour:** 'the unlit grid is visible -- dark dots render in the dim tier rather than as spaces.  That faint lattice IS the signature.'  So this language's scrim is the one it was already drawing

## `pane_split` — **evoked**

- **element drawn:** the vertical divider between the list and the detail pane
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** the language's own answer to 'two regions side by side' -- a rule, a grey step, air, or a refusal; COMPOSITION is a per-kit commitment (COMPONENTS.md: 'composition is the last palette-swap')

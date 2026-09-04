# ledger · S1 — list + detail — candidates

Frame: `ledger_S1.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("ledger")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.field_row` — **evoked**

- **element drawn:** the detail pane's caption -> value rows
- **frame rows:** 6, 7, 8, 9, 10, 11
- **proposed signature:** `Kit.field_row(self, caption: str, value: str, w: int, state: str = DEFAULT) -> str`
- **the commitment it must honour:** the definition-list row a detail pane, a KPI tile and a settings summary all are -- COMPONENTS.md's census lists the stat tile and has no row for this.  It is the single most reused shape in the six screens and the ONE the contract has no seat for, so all five languages are currently drawing LEDGER's mechanism (dot leaders): ledger's own answer generalised into four languages that never chose it, which is the palette-swap failure with a leader instead of a hue

## `pane_split` — **evoked**

- **element drawn:** the vertical divider between the list and the detail pane
- **frame rows:** 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** the language's own answer to 'two regions side by side' -- a rule, a grey step, air, or a refusal; COMPOSITION is a per-kit commitment (COMPONENTS.md: 'composition is the last palette-swap')

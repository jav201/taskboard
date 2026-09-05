# ledger · S4 — modal dialog — candidates

Frame: `ledger_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("ledger")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `pane_split` — **evoked**

- **element drawn:** the vertical divider between the list and the detail pane
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** the language's own answer to 'two regions side by side' -- a rule, a grey step, air, or a refusal; COMPOSITION is a per-kit commitment (COMPONENTS.md: 'composition is the last palette-swap')

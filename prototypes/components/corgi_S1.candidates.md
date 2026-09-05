# corgi · S1 — list + detail — candidates

Frame: `corgi_S1.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("corgi")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `pane_split` — **evoked**

- **element drawn:** the vertical divider between the list and the detail pane
- **frame rows:** 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
- **proposed signature:** `Kit.pane_split(h: int) -> list[str]`
- **the commitment it must honour:** the language's own answer to 'two regions side by side' -- a rule, a grey step, air, or a refusal; COMPOSITION is a per-kit commitment (COMPONENTS.md: 'composition is the last palette-swap')

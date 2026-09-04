# naught · S3 — settings — candidates

Frame: `naught_S3.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("naught")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.button(..., danger=True)` — **evoked**

- **element drawn:** the destructive action and the zone that holds it
- **frame rows:** 19, 20
- **proposed signature:** `Kit.button(self, label, w=0, state=DEFAULT, danger: bool = False)`
- **the commitment it must honour:** severity on a CONTROL, which the contract has never had: it must read in greyscale (COMPONENTS.md 'severity by the language's reserved hues AND a glyph, never hue alone') -- and in ledger and corgi the reserved hue is already spent, so the mechanism cannot be the hue

## `Kit.menu` — **evoked**

- **element drawn:** the open select's list of options
- **frame rows:** 12, 13, 14
- **proposed signature:** `Kit.menu(self, options, selected: int, w: int, state: str = DEFAULT) -> list[str]`
- **the commitment it must honour:** COMPONENTS.md names the context menu 'the biggest historical gap'.  The frame is the language's overlay answer, and a language that refuses overlays must say what it does instead

## `Kit.select` — **evoked**

- **element drawn:** the closed select (its value and its disclosure mark)
- **frame rows:** 10, 11, 12, 13, 14
- **proposed signature:** `Kit.select(self, options, selected: int, w: int = 0, state: str = DEFAULT, open_: bool = False) -> str`
- **the commitment it must honour:** COMPONENTS.md census: 'the closed-state anatomy and the open overlay's frame'.  Distinct from `stepper`, which shows the two ways OFF a value; a select shows the one way INTO a list

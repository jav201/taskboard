# naught · S2 — form with validation — candidates

Frame: `naught_S2.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("naught")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.textarea` — **evoked**

- **element drawn:** the multi-line notes field
- **frame rows:** 13, 14, 15
- **proposed signature:** `Kit.textarea(self, lines: list[str], caret: tuple[int,int] | None, w: int, h: int, state: str = DEFAULT) -> list[str]`
- **the commitment it must honour:** the text field's contract over a RECTANGLE: the value comes back byte for byte, the caret takes a column of its own, and the window moves in two axes instead of one

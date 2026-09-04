# blueprint · S2 — form with validation — candidates

Frame: `blueprint_S2.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("blueprint")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.required()` — **evoked**

- **element drawn:** the required-field marker beside a caption
- **frame rows:** 3, 5
- **proposed signature:** `Kit.required(self) -> str`
- **the commitment it must honour:** one mark, in the language's own notation -- corgi numbers, ledger leaders, blueprint dimensions; it may NOT be a bare '*' in five languages, which is the palette-swap failure at one glyph

## `Kit.textarea` — **evoked**

- **element drawn:** the multi-line notes field
- **frame rows:** 12, 13, 14
- **proposed signature:** `Kit.textarea(self, lines: list[str], caret: tuple[int,int] | None, w: int, h: int, state: str = DEFAULT) -> list[str]`
- **the commitment it must honour:** the text field's contract over a RECTANGLE: the value comes back byte for byte, the caret takes a column of its own, and the window moves in two axes instead of one

## `STATES += INVALID  /  Kit.error(msg, w)` — **evoked**

- **element drawn:** the invalid field's mark and its inline message
- **frame rows:** 5, 6
- **proposed signature:** `LG.INVALID = 'invalid'; Kit.error(self, msg: str, w: int) -> str`
- **the commitment it must honour:** a sixth control state, derived in `component_states` like the other five, reading on GLYPH + STRUCTURE and never on the alert hue alone (COMPONENTS.md state matrix; NAVIGATION.md 'never colour alone')

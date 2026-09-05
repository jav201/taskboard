# corgi · S2 — form with validation — candidates

Frame: `corgi_S2.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("corgi")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.error` — **evoked**

- **element drawn:** the inline error message under the invalid field
- **frame rows:** 7
- **proposed signature:** `Kit.error(self, msg: str, w: int) -> str`
- **the commitment it must honour:** the message is CONTENT and comes back byte for byte; what is missing is the language's NOTATION for a row that explains a rejection -- ledger's leaders, corgi's segment legend, blueprint's revision note.  The STATE itself is no longer a candidate: `STATES += INVALID` shipped in inc14 and the field above is drawn in it

## `Kit.required()` — **evoked**

- **element drawn:** the required-field marker beside a caption
- **frame rows:** 4, 6
- **proposed signature:** `Kit.required(self) -> str`
- **the commitment it must honour:** one mark, in the language's own notation -- corgi numbers, ledger leaders, blueprint dimensions; it may NOT be a bare '*' in five languages, which is the palette-swap failure at one glyph

## `Kit.textarea` — **evoked**

- **element drawn:** the multi-line notes field
- **frame rows:** 13, 14, 15
- **proposed signature:** `Kit.textarea(self, lines: list[str], caret: tuple[int,int] | None, w: int, h: int, state: str = DEFAULT) -> list[str]`
- **the commitment it must honour:** the text field's contract over a RECTANGLE: the value comes back byte for byte, the caret takes a column of its own, and the window moves in two axes instead of one

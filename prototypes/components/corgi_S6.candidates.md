# corgi · S6 — command palette — candidates

Frame: `corgi_S6.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("corgi")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.keyhint` — **evoked**

- **element drawn:** the key hint row
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.keyhint(self, pairs: list[tuple[str, str]], w: int) -> str`
- **the commitment it must honour:** §3b: 'in a TUI the numbers ARE the keybindings, which makes the numbering functional rather than decorative.'  This language already HAS the notation -- what is missing is the seat, and the caller must still supply every key (inc12 §8.3)

## `Kit.match` — **evoked**

- **element drawn:** the highlighted span of the query inside a result
- **frame rows:** 6, 7, 8, 9, 10, 11
- **proposed signature:** `Kit.match(self, text: str, span: tuple[int, int], state: str = DEFAULT) -> str`
- **the commitment it must honour:** the CONTENT law (L-33 / inc12): the result's text comes back byte for byte and only its NOTATION is the language's -- so a language that upper-cases titles may not upper-case a match, and the emphasis may not be the accent alone

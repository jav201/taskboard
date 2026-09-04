# corgi · S4 — modal dialog — candidates

Frame: `corgi_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("corgi")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.overlay` — **refused**

- **element drawn:** the overlay and the dimmed board -- NOT DRAWN
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]`
- **the commitment it must honour:** 'the mode takes over the screen -- no persistent navigation chrome; its answer to smallness is fewer things at once'.  A dialog over a board is two modes at once.  The confirm is a MODE, and because the numbers ARE the keybindings (§3b) its two answers are numbered rather than trapped in a focus ring

## `Kit.keyhint` — **evoked**

- **element drawn:** the key hints along the bottom
- **frame rows:** 16
- **proposed signature:** `Kit.keyhint(self, pairs: list[tuple[str, str]], w: int) -> str`
- **the commitment it must honour:** inc12 §8.3: 'a mark that encodes a binding belongs to whoever owns the keymap.  Never the library.'  So the kit owns the NOTATION (corgi's brackets, ledger's leaders) and the caller supplies every key

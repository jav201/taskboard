# ledger · S4 — modal dialog — candidates

Frame: `ledger_S4.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("ledger")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.overlay` — **refused**

- **element drawn:** the delete dialog -- REFUSED AT THE CONTENT, not the frame
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.overlay(self, rows, w, h, under: list[str]) -> list[str]`
- **the commitment it must honour:** 'nothing is deleted, everything is balanced' -- the genre rules out silent deletion as a design (LANGUAGES.md #9, 'what the genre obligates').  A confirm-to-destroy is therefore not a dialog this language may style; the honest screen is the reversing entry, and it is a PAGE rather than an overlay because a ledger has no surface in front of the page

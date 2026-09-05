# ledger · S5 — live monitor / log — candidates

Frame: `ledger_S5.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("ledger")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.readout_label` — **refused**

- **element drawn:** the readout's label -- LABELLED, never numbered
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.readout_label(self, label: str) -> str`
- **the commitment it must honour:** L-33: 'because the numbering IS the keymap, this language has no notation for a passive readout.  A [5] over a chart nobody can act on is the decorative numbering §3b defines itself against.  Readouts are LABELLED; controls are NUMBERED.'  The right response to wanting a numbered readout is to notice

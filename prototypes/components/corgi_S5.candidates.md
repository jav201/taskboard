# corgi · S5 — live monitor / log — candidates

Frame: `corgi_S5.txt` / `.svg` — 100×32, rendered through `taskboard.language.kit("corgi")`.

Every element below was drawn **by hand in `prototypes/components/screens.py`**, not by a kit method. Everything else in the frame came out of a kit call and is therefore *implemented*. Verdicts are the spec's closed set: **implemented / evoked / refused**.

## `Kit.readout_label` — **refused**

- **element drawn:** the readout's label -- LABELLED, never numbered
- **frame rows:** — nothing is drawn; that is the answer
- **proposed signature:** `Kit.readout_label(self, label: str) -> str`
- **the commitment it must honour:** L-33: 'because the numbering IS the keymap, this language has no notation for a passive readout.  A [5] over a chart nobody can act on is the decorative numbering §3b defines itself against.  Readouts are LABELLED; controls are NUMBERED.'  The right response to wanting a numbered readout is to notice

## `Kit.log_row` — **evoked**

- **element drawn:** the log row's level mark and its severity channel
- **frame rows:** 9, 10, 11, 12, 13, 14, 15, 16
- **proposed signature:** `Kit.log_row(self, ts: str, level: str, msg: str, w: int) -> str`
- **the commitment it must honour:** `ICONS` has six domain kinds and no log level.  The level must read in greyscale on a glyph, and the alert hue is rationed -- ledger spends it only on debt, blueprint only on overdue, naught has one red total

## `Kit.tail` — **evoked**

- **element drawn:** the tail marker (the streaming/held state of the log)
- **frame rows:** 17
- **proposed signature:** `Kit.tail(self, held: bool) -> str`
- **the commitment it must honour:** an INDETERMINATE indicator, which COMPONENTS.md's state matrix says must be MOTION and never a frozen half-fill; `spinner(tick)` is the moving half and this is the held one

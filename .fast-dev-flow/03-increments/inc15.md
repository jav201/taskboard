# Increment 15 — `Kit.field_row`: the most reused shape in six screens gets a seat, and five mechanisms

**Batch:** `kits-learn-3` · **AC-2** · operator ruling 2 of 2026-09-04
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/components/screens.py` —
**3 source files**.

---

## 1. The defect

The PROTOTYPE round's own words: the caption → value row *"is the single most reused shape in the six
screens and the ONE the contract has no seat for, so all five languages are currently drawing LEDGER's
mechanism (dot leaders): ledger's own answer generalised into four languages that never chose it, which is
the palette-swap failure with a leader instead of a hue."*

The line that did it, in `screens.py`, is worth quoting because the defect is visible in the code:

```python
lead = k.LEAD if hasattr(k, "LEAD") else " "
```

An `hasattr` against one language's typographic argument, with a space as the fallback. Two of eleven kits
declare `LEAD`; the other nine got air, and the two that had it got ledger's row whether or not it was
theirs.

---

## 2. The mechanism

`Kit.field_row(caption, value, w) -> str`, exactly the three arguments the ruling names. No `state`
parameter: a definition row has no control affordance, and a parameter that only tints would be
speculative surface.

**What is the contract's and what is the language's**, stated once at the base seat so no language decides
it twice:

- the **VALUE is CONTENT** — byte for byte, never recased, never cut (L-33 / inc12);
- the **CAPTION is a LABEL, and a label is NOTATION** — a language that letters its legends in capitals
  letters this one too, exactly as `tile_row` already does. That asymmetry is the ruling;
- the **GAP is the MECHANISM**, and it is nobody's default.

`w` is a **minimum for the figure** — the stepper's rule for the stepper's reason: a row that truncated a
value to fit would be lying about the number.

**Six seats, six answers**, and the same input in each (`("due date", "12/09/26", 40)`):

```
nord        due date                        12/09/26      air to a right column
corgi       DUE DATE 12/09/26                             the silkscreen beside the readout
blueprint   DUE DATE ·───────────────────── 12/09/26      a dimension
prism       due date                    ⡀⡤⣶ 12/09/26      the ember frontier
naught      due date 12/09/26 ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦      the lattice, unlit
ledger      DUE DATE ······················ 12/09/26      dot leaders
```

- **nord/base** — the terminal's own two-column list. No leader: the terminal's convention is a COLUMN,
  and a column is found by *alignment* rather than followed by a line.
- **corgi** — a panel does not rule a line from a legend to its display; it **prints the legend where the
  display is**. The label is engraved in the aluminium register, the figure stands in the glass beside it,
  the rest is bare panel. Left-packed, and **not numbered** — the numbers are the parameter keymap (L-33,
  ruling 3), and a caption is a name, not a key.
- **blueprint** — a **dimension**: the name at its datum, the extension line out of it, the figure
  terminating the run. The one mechanism here that is a *measurement* rather than a fill. Both marks it
  spends (`LEAD`, `EXT`) are already in the ten; no vertical stroke, nothing boxed.
- **prism** — the **ember frontier**, its second commitment applied to a row instead of a quantity:
  *"quantity is a solid field being CONSUMED, not a track being filled"*. The value is where the field ran
  out. No leader and no stroke — this language separates by tone and by consumption.
- **naught** — **the lattice is the ground**, so the row's remainder is drawn. Dense: the figure sits
  beside the name; what follows is unlit grid. **The fill is after the value and never between**, which is
  the exact structural difference from a leader — a leader *connects* two marks, a lattice is a *ground*
  that was already there.
- **ledger** — dot leaders, and here they are the language's **own**. `_leadered()` is the one function
  that argument lives in, and this is the plainest thing it has ever been asked for.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | the base seat + 5 overrides (`Naught`, `Corgi`, `Prism`, `Ledger`, `Blueprint`) |
| `tests/test_components.py` | 7 new laws, 47 new tests |
| `prototypes/components/screens.py` | S1's detail pane calls `k.field_row`; `C_FIELDROW` and the `hasattr(k, "LEAD")` line deleted |

**A near-miss worth recording.** The first insertion put the ember frontier in **darkside**, because the
anchor was "the `tile_row` that lowercases its label" and darkside's does — prism *is* darkside's
descendant and they sit next to each other in the file. It was caught by rendering (prism came back
byte-identical to nord) and moved with an assertion that the anchor's enclosing class is `Prism`
(`.fast-dev-flow/probes/_inc15_fix_prism.py`). **Anchoring an edit on a code shape rather than on a name
is how a mechanism lands in the wrong language**, and the thing that caught it was the property test's own
premise: five languages must not agree.

---

## 4. The property test

`test_five_languages_return_five_different_rows` — same caption, same value, same width, five rows that
differ **as cells**. Compared on the **plain** text, not the markup: two rows differing only in a colour
token are two recolours, and comparing markup would let this test pass on exactly the defect it names.

Beside it, `test_no_language_borrows_ledgers_leaders` makes the anti-palette-swap law falsifiable rather
than promised: ledger's row **must** contain a run of `LEAD`, and **no other language's may**. Put the
`hasattr(k, "LEAD")` line back and blueprint goes red.

And the laws that guard the contract's two halves in all eleven languages: exactly `w` cells (asserted
with a caller string containing `[`, because `mark()` escapes into two characters that occupy one cell —
pitfall A1); the figure back **byte for byte** including `"Q3 -1,204.55"` and `"AbCd"`; **never truncated**
even when the row is asked for 12 cells and handed a 25-character value; the caption's letters always
present. Plus one structural law for the mechanism most easily mistaken for a leader:
`test_naughts_row_fills_after_the_figure_and_never_between`.

---

## 5. Test results

```
python -X utf8 -m pytest -q
424 passed, 2 skipped, 4 warnings in 31.86s        (inc14 left it at 377 — +47)
```

```
python prototypes/capture_languages.py --surface    # plain and alone (F-8)
11 surfaces -> prototypes/gallery ; no two identical (55 pairs)
moved vs baseline-kits2: the same four surface_{corgi,industrial}.{txt,svg} as at inc14
```

`prototypes/verify_language.py` was **not** re-run for this increment and that is a decision, not an
omission: spec §4 runs it when an increment changes the **state axis or a glyph table**, and this one adds
a method and touches neither. It is run again at the batch's close.

---

## 6. The capture (AC-7)

```
python -X utf8 prototypes/components/render.py
68 hand-drawn elements declared (9 refused, 59 evoked)      (inc14 left it at 76)
```

**Eight elements gone**: `field_row` in the five S1 frames, plus the three S4 backdrops (prism, naught,
blueprint) that carry S1's candidates forward — a hand-drawn element does not stop being hand-drawn
because it was drawn behind something else, and it does not stop being *implemented* either.

---

## 7. Risks

- **Six languages share the base row** (instrument, swiss, industrial, nord, darkside, solari). nord *is*
  the base, so five of them are inheriting rather than choosing. That is the seat existing without a
  mechanism, which is a weaker version of the defect this increment fixed — recorded in §8 and bounded by
  the batch's scope (five prototyped languages get mechanisms; the rest get the seat).
- **The caption/value asymmetry is a ruling, not a law of nature.** Three languages letter the caption in
  capitals. A caller who needs the caption verbatim has no way to ask for it, and the test asserts only
  that its *letters* survive.
- **`clip()` still guards the frame.** `field_row` returns exactly `w` cells for fitting input and wider
  for a long value; `screens.py` clips at the pane width, so an overlong value is cut **in the frame**
  while the primitive keeps its promise. The frame is where that trade is visible.

## 8. Pending

- Five languages' own definition rows (instrument, swiss, industrial, darkside, solari). Next round.
- `Kit.error`, `required`, `textarea`, `pane_split`, `readout_label` — still hand-drawn, still declared,
  still out of scope (spec §5, §6.3).

## 9. For the skill

- **`COMPONENTS.md`'s census has a stat tile and no definition row.** It is the most reused shape in the
  six canonical screens; it belongs in the census with its six mechanisms, because the mechanisms are the
  content — a "caption → value row" with no per-language answer is how four languages ended up drawing a
  fifth's leaders.
- **The rule worth exporting is the asymmetry**: the value is content, the caption is notation, the gap is
  the mechanism. It settles a whole family of rows (KPI tile, settings summary, detail pane) in one
  sentence.
- **`hasattr(kit, "TOKEN")` in a caller is a smell with a name now.** It is a caller reaching for one
  language's signature and handing everyone else a default — the palette-swap failure inverted.

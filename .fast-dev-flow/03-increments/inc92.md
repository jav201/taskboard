# inc92 — L12 corrected: four kits were filed as hue-only and all four are painted with a channel

Batch `rework-10`, increment 2 of 3.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation):

- **A frame has no focus; the round presses keys.** The instrument is `App.run_test()` + `Pilot` on
  the widget slice, per language, driving a fixed script and capturing the screen after each key
  through the same `cell_grid` the raster uses.
- **L12 corrected:** the match channel in grey is weight or decoration where the kit declares it, and
  the grey test reads the sidecar's `bold`/`underline` flags, not colour tokens; a kit is hue-only in
  grey only if its match run carries neither.

And the increment's own brief: *the grey law becomes legible (≥ 3:1 effective **or** weight ≥ 1.3× the
neighbour's ink **or** decoration present) on the grey PNG; swiss's 0.83× is judged — if weight is
present it passes on weight, else it is a Limit.*

## §1 — cause

`SESION-PERSONA.md` §3 carries a notice measured while the human-session sheet was being prepared,
and it is the reason this increment exists:

> El *match* de estos cuatro kits **no viaja solo en el matiz**. En el sidecar del raster, el run del
> match lleva `bold=True` en nord, swiss y prism, y `underline=True` en instrument. … `match_branch()`
> clasifica por la relacion entre tokens de color y **no lee `bold` ni `underline`**.

That is the whole defect in one sentence, and it had been shipping since inc84 measured L12 and inc86
wrote it into four kit docstrings as a LIMIT.

## §2 — mechanism

### The classification, and why it could not have failed

`match_branch()` read `MATCH_STYLE`'s **token** and returned `hue` for every kit spending `accent` or
`alert` — and in that branch it **never looked at the style word at all**:

```python
    if token in ("accent", "alert") and value != t["ink"]:
        return "hue", value, t["ground"]
    return word, value, t["ground"]        # <- the only place `word` is used
```

So instrument, whose `MATCH_STYLE` is `underline {accent}` and whose six match runs on `S6` are every
one of them drawn with a rule under them, was filed as carrying the match on hue alone. Nord, prism
and swiss, all three drawn in the bold instance, were filed the same way. **The raster's sidecar has
carried the flag since inc43** — `cell_grid` returns five fields and two of them are `bold` and
`underline` — and the classification never read them.

It is now read off the paint: `match_seat()` finds the run `Kit.match` paints and `match_branch()`
takes its flags. Both `legibility.py` and the suite carry the derivation, as they always have, so the
two can only agree by being right.

### Finding the seat is a contract question and not a colour question

The seat is *the first run whose text is the query and whose right-hand neighbour is painted in
`mut`* — which is a description of what `match(label, query)` emits (prefix in `mut`, the query in
`MATCH_STYLE`, suffix in `mut`), and the sheet's first result `redirect to task` has an empty prefix.
**Asked by colour instead, solari's reverse branch matches its own tab bar and its own header two
rows higher up**, and the measurement would have been taken on a chrome run.

### The grey law, on the grey PNG for the first time

Section H of `legibility.txt` measured **tokens**: it took `accent`, took `mut`, greyed both through
`raster.grey_of`'s transform and divided. That answers a question about two colours. The ruling asks
for *legible on the grey PNG*, so every number is now taken off `<kit>_S6.grey.png`, cell by cell,
over the match seat and the body run beside it:

```
effective   the mean grey of the pixels the run PAINTS against the same for
            the body -- section C's definition of `effective`, along the one
            dimension grey has
ink         mean |grey - ground| over the run's whole box: area AND depth
coverage    the fraction of pixels that differ from the ground at all: area
            alone
```

The weight clause has **two arms** and swiss is why: `ink >= 1.30` (the ruling's number), or failing
that `coverage > 1.00`, which is the ruling's *"if weight is present it passes on weight"* turned
into a measurement rather than a flag.

## §3 — the four kits, before and after

```
kit         declared            painted     eff    ink    cov   carried by
instrument  underline {accent}  underline  2.31   2.42   1.30   weight + decoration
prism       bold {accent}       bold       1.76   1.82   1.22   weight
nord        bold {accent}       bold       1.44   1.74   1.22   weight
swiss       bold {alert}        bold       1.17   1.07   1.21   weight (coverage arm)
```

| kit | inc86 said | inc92 measures |
| --- | --- | --- |
| instrument | hue-only, 2.42:1 in grey, LIMIT | **underlined**; carried by decoration AND weight; effective 2.31:1 |
| prism | hue-only, 1.59:1 in grey, LIMIT | **bold**; carried by weight (1.82× ink); effective 1.76:1 |
| nord | hue-only, 1.34:1 in grey, LIMIT | **bold**; carried by weight (1.74× ink); effective 1.44:1 |
| swiss | hue-only, 1.52:1 in grey, LIMIT | **bold**; carried by weight on the COVERAGE arm alone; effective 1.17:1 |

**`0 kits carry the match on HUE ALONE.` Eleven of eleven have weight, decoration or both, so the
hue-only Limit has no members and the table that held four rows is replaced by one that holds all
eleven.**

### swiss, and the one seat where area and depth disagree

swiss's match covers **1.21×** the lit area of the body beside it and carries only **1.07×** its ink,
because its red falls **darker** than the grey of that body: depth cancels most of what area gained.
A single number would have had to choose between *"swiss's match is heavier"* and *"swiss's match is
fainter"*, and both are true of different halves of the same measurement. The ruling's own
disposition is what admits it, and **swiss is the only kit of eleven that needs that arm**.

### The notice does not reproduce, and the way it fails is informative

`SESION-PERSONA.md` §3 measured nord 1.36×, prism 1.42×, instrument 1.86× and swiss 0.83×. This
increment's ink column is **1.28–1.30× higher on all four** — one constant factor, identical in every
row — so the two measurements differ by a **definition** and not by a reading, and the ORDER is the
same in both. The one place it matters is swiss, where the notice says the match is FAINTER than its
body and this table says it is barely HEAVIER. **That disagreement is exactly why the ruling did not
rest swiss on the number**, and it is reported in the report itself rather than reconciled away.

### What survives of L12, and it is a thinner thing

**None of the four clears the EFFECTIVE clause in grey.** instrument 2.31, prism 1.76, nord 1.44,
swiss 1.17, against a floor of 3. So the surviving Limit is not *"the match rides hue alone"* — that
sentence is false and was always false — but *"the match is found in grey by 21–30 % of AREA and not
by tone"*. Each of the four docstrings is REWRITTEN to say that, with its own number, rather than
deleted: deleting them would have thrown away the true half with the false one.

## §4 — law and teeth

| law | what it binds |
| --- | --- |
| `test_the_match_channel_in_grey_is_weight_or_decoration_and_not_hue` | five clauses: the painted channel is what `MATCH_STYLE` declares in all eleven; NO kit is hue-only; each keeps its three numbers to two decimals re-measured off the grey PNG; every kit's channel is carried by at least one clause; and **exactly one kit needs the coverage arm, and it is swiss** |
| `test_the_four_kits_the_old_table_named_carry_the_corrected_limit` | the four and no others carry an L12 paragraph; each cites *L12 corrected*, says LIMIT and RECORDED AND NOT FIXED, carries its own effective number to two decimals, and **no longer says the sentence inc92 disproved** (`RIDES HUE ALONE`) |

**Teeth** — `test_the_grey_match_measurement_can_tell_a_channel_from_no_channel`. A law that finds a
channel everywhere is worth nothing, so the same measurement is run over two mutants built from the
shipped pictures: the match run measured against ITSELF must come back at exactly 1.00×, and the
comparison turned round (body against match) must come back UNDER one on every kit. The number has to
have a direction and not just a magnitude.

## §5 — what was found by looking

1. **The defect is one line long and it shipped through two increments that were about it.** inc84
   measured L12 and inc86 recorded it, and both used the classification rather than checking it. A
   derivation that returns before it uses its own second variable is the kind of thing a test cannot
   catch, because every law about it was written from the same reading.
2. **The corpus already had the evidence and had had it for forty-nine increments.** `cell_grid`
   started returning `bold` and `underline` at inc43 — *"66 declared runs across the eleven S6 sheets,
   none painted"* is that increment's own line — and the L12 measurement, three batches later, went
   round it to the tokens.
3. **prism's docstring said the opposite of what is true, in a paragraph about honesty.** It read:
   *"this kit already moved PRIORITY off hue and onto a glyph (`!2`) … so the match is the one place
   left where prism still asks colour to carry a distinction by itself."* It never was. The weight was
   always there.
4. **nord's Limit was doctrine and the doctrine survives, inverted.** The old note said base16 has no
   identity to spend on a second channel. It has one and it is the only one it owns: the TONE is the
   user's palette, and the WEIGHT is nord's.
5. **Three of the eleven are carried by a clause nobody would have thought to write.** industrial,
   darkside and solari are `reverse`, and a reversed run is 3.60× the body's coverage — the whole cell
   instead of a glyph's worth of it. It is the loudest channel in the corpus and the only one that
   does not need the eye to compare two things.

## §6 — files and frames

| file | change |
| --- | --- |
| `prototypes/components/legibility.py` | `GREY_WEIGHT_FLOOR`, `match_seat()`, `match_in_grey()`, `match_branch()` corrected, section H rewritten. 1065 → 1202 lines |
| `tests/test_components.py` | `_MATCH_QUERY`, `_match_seat`, `match_branch` corrected, `MATCH_IN_GREY` (4 rows → 11), `MATCH_WAS_CALLED_HUE_ONLY`, `GREY_WEIGHT_FLOOR`, `_match_in_grey`; two laws replaced by three |
| `taskboard/language.py` | the four L12 docstrings rewritten — instrument, swiss, nord, prism |
| `prototypes/out/legibility.txt` | section H |

**Frames changed: ZERO.** No token, no glyph and no tier moved; what moved is a classification and
four paragraphs. `render.py`, `raster.py`, `second_width.py`, `matrix.py` and `collision_census.py`
were all re-run and `git status --porcelain` shows no artefact under `prototypes/components/`.

**Gallery 30–51: none changed byte-wise**, read off `prototypes/components/` (the `.txt`).
`capture_languages.py` was not run: no board changed.

## §7 — deviations, named

- **The hue-only set is now EMPTY, and the ruling's phrasing anticipated a smaller correction.** The
  ruling says *"a kit is hue-only in grey only if its match run carries neither"*; measured, none of
  the eleven carries neither. `MATCH_IN_GREY` is therefore not four rows shortened but eleven rows
  widened, so the table still has teeth instead of being a vacuous empty dict.
- **swiss passes on the coverage arm and the brief's number says it should fail.** The brief's weight
  clause is `ink ≥ 1.3×` and swiss measures 1.07×. The brief's next sentence — *"if weight is present
  it passes on weight"* — is what admits it, and the arm is written as a MEASUREMENT (coverage > 1.00)
  rather than as a flag read, so the pass is still something the pixels say.
- **`GREY_DISTINCT` (1.10) is now unused by section H** and is left in place: it is a reporting
  threshold with its own docstring and no law was built on it.
- **The four kits keep their L12 paragraphs though none of them is hue-only any more.**
  `MATCH_WAS_CALLED_HUE_ONLY` is a named set, so a kit leaves it by somebody deciding it should — and
  the human session's `F15`–`F22` were chosen off the old reading, which is a reason to keep the four
  identifiable.

## §8 — gates

```
pytest -q                1536 passed, 1 failed, 2 skipped in 48.16s
                         (inc91 1536 total -> 1537, +1 net: 2 laws removed,
                          3 added.  The one failure is
                          test_win_clipboard_roundtrip, environment-coupled,
                          reported and not counted, not touched)
verify_language.py       ALL PASSED                                      exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn     exit 0
                         -- and nothing changed on disk
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                           exit 0
legibility.py            1202 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct     exit 0
matrix.py                refusals [] for all eleven                      exit 0
collision_census.py      TOTAL 23 · homoglyph rows 22 · both self-checks
                         green · zero collisions: darkside               exit 0
keys.py                  not re-run: no frame the key round photographs
                         changed
capture_languages.py     not run: no board changed
```

`BELOW_THE_FLOOR`, old → new: **4 → 4, unchanged.** This increment moves no seat.

## §9 — pending / next

- **inc93** takes K5 and K6, the two defects inc91 recorded, and writes the round.
- **Handed back:** whether 21 % more lit area is FOUND by an eye. This increment can say the channel
  is in the pixels; it cannot say anyone sees it. `SESION-PERSONA.md`'s `F15`–`F22` were built to ask
  exactly that and were built off the reading this increment corrects — **the eight frames are still
  the right eight, and the question they ask has changed**: not *"is hue enough?"* but *"is 21 % of
  area enough?"*. The sheet's own §7.9 said the session could not settle it, and it still cannot; what
  has changed is that the corpus now knows what it is asking.

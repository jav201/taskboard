# Increment 35 — `required` for the six that inherited it

**Batch:** `inheritors-2` · the first half of `kits-learn-4` §5's declared debt (`spec.md` §8, "What was
NOT done, and why")
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**.

**Six languages were marking an obligation with `*`, which is the base kit's mark and the palette-swap
failure at one glyph — the narrowest seat in the file and therefore the easiest place in the repo for
eleven languages to agree by accident. Five now answer for themselves and the sixth DECLARES the base.
11 marks, 11 distinct cells, exactly one `*` and the test names whose.**

---

## 1. The state this increment found

```
naught ∙   corgi ▀   prism ⡀   ledger †   blueprint ├          <- inc29, five languages
instrument *   swiss *   industrial *   nord *   darkside *   solari *
```

`kits-learn-4` seated `Kit.required` for the five the PROTOTYPE round rendered and its §5 put the other
six out of scope by the operator's own enumeration of seven mechanisms. The base comment has said what is
wrong with the leftover the whole time:

> "It may NOT be a bare `*` in eleven languages, which is the palette-swap failure at a single glyph …
> `*` is the terminal's own convention and the base kit is the terminal; **every language with an
> alphabet of its own answers below**."

Six had not answered.

---

## 2. The five mechanisms, each with the commitment it was derived from

### instrument — §1 · *"numerals and icons drawn on a COARSE DOT GRID … borders almost absent"*

```
REQUIRED = "⠁"      one dot, at the top of the cell
```

Severity in this language is **dot count** (`⠂⠂ / ⠆⠆ / ⠇⠇`), so an obligation — a property, not a
severity — is the count's floor: the least this matrix can light. Not `⡀`: that is prism's dot and it sits
at the **bottom**, which is a different reading of the same grid, and the two languages own opposite ends
of it.

### swiss — §2 · *"near-mono + one accent (classically red) … no boxes — alignment does the dividing"*

```
REQUIRED = "•"      the ladder's own mark, set solid
```

**This language has no glyph alphabet to reach into** — it is the cheapest of the eleven precisely because
it draws none — so the only honest mark is one it already uses, at the other end of the one channel it
commits to. Its severity ladder is a WEIGHT ladder (`· / ─ / ━`); the obligation is `·` at full weight.
Not the accent: the accent is rationed and an obligation is not an alarm.

### industrial — §3 · *"boxed groups … EVERYTHING IS NUMBERED AND LABELLED"*

```
REQUIRED = "▐"      the plate, opened
```

The plate (`DISPLAY_BOX`'s `▐`/`▌`) is this language's whole notation: it plates its keys, its figures and
its display. A field that may not be left empty is a plate that has been **opened and is not closed until
it is filled** — the leading half cell, alone. It could not be a number, and that is not an aesthetic
choice: L-33 rules that this language's digits are the MODES, and an obligation is not a mode.

### darkside — §8 · *"achromatic + ONE RESERVED ACCENT … hierarchy by WEIGHT AND DIMMING, not size"*

```
REQUIRED = "▪"      one solid achromatic cell
```

**Two channels are closed by commitment before the design starts.** The accent "marks interactivity,
nothing else" and a required field is not interactive; the `· / o / O` ladder is spoken for by severity.
What is left is the channel the language itself names — weight — and `▪` is the heaviest a single
achromatic cell gets **without becoming a border**, which is the one thing this language has forbidden
itself.

### solari — §10 · *"THE SEAM IS THE WHOLE DIVIDER VOCABULARY … the structure device is the cell FACE"*

```
REQUIRED = "▁"      a seam with nothing flipped onto it
```

On a departure board a field that must be filled is a face that **has not turned yet**, and what shows is
the seam under it. It is the same mark `field_row` closes its gap with, and that is the commitment rather
than a collision: this language has ONE divider and spends it everywhere. Not a digit — the digits are the
quantity (DATAVIZ law 1) and an obligation states no quantity.

### nord — §6 · *"the only language that INHERITS THE USER'S ENVIRONMENT instead of overriding it"*

**Nord keeps `*`, and that is an answer.** `*` is the terminal's own convention for a required field and
this language's whole commitment is to be the terminal. Giving it a mark of its own would not fill a hole,
it would leave base16 doctrine — the same ruling inc32 made for its other seven mechanisms, and it is
asserted the same way: `REQUIRED` joins
`test_nord_declares_the_environment_and_the_declaration_is_checked`, which walks the MRO and requires the
owner to be `Kit`.

### 2a. A conflict this increment did NOT average

**The batch's own brief asked for "never `*`" and nord's declaration says otherwise.** Both cannot be
literally true, and blending them (a mark for nord, cited to a doctrine that forbids one) would have been
the worse answer. What is implemented is the stronger claim the two agree on:

- **eleven distinct marks**, which is the property the debt was actually about, and
- **`*` survives in exactly one language, named** — `test_only_the_language_that_declares_the_
  environment_marks_with_a_star` asserts `starred == ["nord"]`, so a *sixth* language drifting back to the
  base star is red, and nord's declaration is legal because it is written down.

A test reading "no star anywhere" would have made nord's own commitment illegal and it is recorded here
rather than quietly resolved.

---

## 3. The property tests

| test | what it holds |
| --- | --- |
| `test_eleven_languages_mark_an_obligation_eleven_ways` | **11 / 11 distinct cells.** The seat is one cell wide, which makes it the easiest place in the repo to agree by accident |
| `test_only_the_language_that_declares_the_environment_marks_with_a_star` | `*` appears exactly once and the list is `["nord"]` |
| `test_a_required_mark_survives_greyscale` (×11) | one cell, non-blank in `plain`, **and still distinct from all ten others with colour stripped at the source** — two marks differing only in a hue token are two recolours of one mark |
| `test_an_inheritors_required_mark_costs_no_rationed_hue` (×6) | the ink tier, never `alert`. Industrial is the row that matters: its own entry says it "FAILS when colour must carry severity" |
| `test_no_language_numbers_a_required_field` (existing, ×11) | now covers the six as well — L-33 |
| `test_nord_declares_the_environment…` (existing, +`REQUIRED`) | nord's `REQUIRED` is owned by `Kit` and a mechanism landing on nord by accident is red |

The eleven marks, measured rather than typed:

```
naught ∙   corgi ▀   instrument ⠁   swiss •   industrial ▐   nord *
darkside ▪   prism ⡀   ledger †   solari ▁   blueprint ├
distinct: 11 of 11        stars: ['nord']
```

**`INHERITORS` moved to the module header** beside `PROTOTYPED`. It was declared 200 lines below the first
law that needs it; both halves of the eleven are now read from the same place. No test changed meaning.

---

## 4. Test results

```
python -X utf8 -m pytest -q tests/test_components.py    546 passed in 0.52s      (was 526)
python -X utf8 -m pytest -q                             900 passed, 2 skipped   (was 880)
python -X utf8 prototypes/verify_language.py            10857 PASS · ALL PASSED (baseline 10857)
python -X utf8 prototypes/components/render.py          30 frames · 0 hand-drawn · 60 pairs, none identical
git status --short                                      M language.py · M test_components.py
```

**`git status` after the re-render is the load-bearing line.** `render.py` rewrote all 30 frames and all
30 sidecars and **not one of them changed on disk**, which is the evidence that this increment moved no
committed frame: the five prototyped languages' `required` is untouched, and the six that changed render
in no frame yet (inc37).

---

## 5. Risks

- **Five of these marks have never been photographed.** They are held by property tests and by nothing
  anyone can look at until inc37 renders the six. A mark that is legal, distinct and *ugly at 100×32* is
  a state these tests cannot detect.
- **`▐` is chrome used as a mark.** Industrial marks with its plate on purpose — its plate is its
  alphabet — but a reader who has not read the commitment will read it as a stray box edge. It is the
  choice most likely to come back at the frame round.
- **`▁` and `•` sit low and small in a cell.** Both survive greyscale as shapes, but neither was measured
  for legibility against a caption at the terminal's own contrast; `verify_ink.py` is not run per-mark.
- **`⠁` and `⡀` are one dot each at opposite corners.** Distinct as cells, and distinguishable to a
  reader only if the two languages are seen side by side — which is exactly what the matrix does, so the
  claim is testable at inc37 rather than assumed here.
- **The star test is now the only thing standing between the base and a sixth `*`.** It is one assertion
  on a list, and it is worth saying that this is a weaker guard than a registry with a citation per entry
  — but a registry of one entry, for a language whose doctrine is already asserted by MRO, would be
  ceremony.

## 6. Pending

- **`pane_split` for the six** — inc36, the other half of the debt.
- **The six render in no frame** — inc37.
- **F-8** (`--surface` plain and alone) and the export — at the batch close.

## 7. Suggested next task

inc36 — `pane_split` for the six, with swiss's and darkside's `PANE_SPLIT_REFUSED` citations already
written in the registry's own comment.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `900 passed, 2 skipped` (§4). `verify_language.py` **ALL PASSED**
      at 10857, the baseline count. `render.py` green at 30 frames, 0 hand-drawn, and no frame moved.
- [x] **No secrets in code or output** — five class constants and five tests. No network, no dependency,
      no path outside the worktree.
- [x] **No destructive commands run without approval** — none run. Nothing removed; `render.py` rewrote
      its own 60 artefacts byte-identically.
- [x] **File count within cap** — 2 source files, plus this packet: 3.
- [x] **Review packet attached** — this document.

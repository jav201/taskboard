# Increment 37 — frames for the inheritors: the matrix goes to 11 × 6

**Batch:** `inheritors-2` · `kits-learn-4` §8's second "what was NOT done": *"The six inheritors render in
no frame … their thirty new mechanisms are held by 40 property tests and by nothing anyone can look at."*
**Files:** `prototypes/components/render.py`, `prototypes/components/matrix.py`,
`tests/test_components.py` — **3 source files**; plus 108 regenerated artefacts (36 new frames × `.txt` /
`.svg` / `.candidates.md`).

**The sweep's language list was a typed list of five, and that list is how six languages went
unphotographed through three batches while collecting thirty-eight mechanisms of their own. It is now read
off `LG.KITS`. 66 frames, 330 pairs and no two alike, zero hand-drawn elements, zero clipped, and the six
that had never been looked at came out right on the first sweep.**

---

## 1. The matrix, 11 × 6

```
                        S1              S2              S3              S4              S5              S6
naught        implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
corgi         implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
instrument    implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
swiss         implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
industrial    implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
nord          implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
darkside      implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
prism         implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
ledger        implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
solari        implementa -    implementa -    implementa -    implementa -    implementa -    implementa -
blueprint     implementa -    implementa -    implementa -    implementa -    implementa -    implementa -

--- refusals, by language ---
naught [] corgi [] instrument [] swiss [] industrial [] nord [] darkside []
prism [] ledger [] solari [] blueprint []
```

**66 of 66 `implementa`, and the empty refusal list is the point, not an omission.** A refusal in this
column would mean a frame *declared a hand-drawn element it could not get from a kit*. There are none —
every language that says no to something says it in a **registry the mechanism reads**
(`MODAL_BORDER_REFUSED` 7, `PANE_SPLIT_REFUSED` 5, `READOUT_NUMBER_REFUSED` 3, `LABEL_REFUSED`), so the
refusal is *rendered* rather than *noted*, which is what puts the cell at `implementa`.

`matrix.py` derives every cell from the same `Sheet` objects `render.py` writes the frames from, so the
table and the frames cannot disagree — and both now read `list(S.LG.KITS)` rather than a list of five.

---

## 2. The sweep

```
11 languages x 6 screens | viewport 100x32 | animations off
  ...
  66 .txt + 66 .svg -> prototypes/components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
```

**Zero `CLIPPED` warnings across all 66.** The six inheritors were composed against the same
`fixture.py` at the same 100×32, through the same `capture_languages.settle` / `cell_grid` /
`svg_from_grid` the gallery's own board frames were taken with — the sweep's whole reason for importing
rather than reimplementing the render path.

Ink, the six that are new (the five prototyped are unmoved, byte for byte):

```
instrument  S1 36.0  S2 13.2  S3 13.6  S4 34.1  S5 14.6  S6 14.9
swiss       S1 16.4  S2 11.5  S3 14.7  S4 18.7  S5 17.1  S6 14.0
industrial  S1 24.0  S2 13.9  S3 15.4  S4 23.0  S5 17.8  S6 15.1
nord        S1 19.3  S2  8.5  S3 11.7  S4 19.9  S5 14.2  S6 12.7
darkside    S1 13.1  S2  8.7  S3  8.9  S4 14.4  S5 11.3  S6  8.3
solari      S1 33.5  S2 13.7  S3 13.8  S4 23.6  S5 14.5  S6 11.2
```

The spread reads as the languages do: instrument and solari are dense by commitment (a graticule and a
seam under everything), darkside is the airiest of the eleven, and its S6 at 8.3 % is the lowest frame in
the sweep — flagged in §5 rather than passed over.

### 2a. What the two new mechanisms look like at 100×32

The S1 gutter, which is the seat inc36 seated, at rows 3–5 of each frame:

```
industrial   ...  [ 5]▌ ▐[DETAIL]  Fix login redirect          two plates, facing
instrument   ...     5 ⠸ ⣿ DETAIL  Fix login redirect          a graticule column
swiss        ...     5             D E T A I L  Fix login…     air: the next column IS the division
solari       ... PRI     DETAIL  FIX LOGIN REDIRECT            air: padding holds the columns apart
```

**Industrial's `▌ ▐` reads as one convention with its own keyhint** (`▐up▌`) in the same frame, which was
the argument inc36 made from the source and could not show. **Instrument's `⠸` sits in a frame whose field
rows are ruled with `⠒` and whose bars are `⣿`** — the graticule column is legible *as a graticule* beside
them, and it does not read as the `⠇⠇` error rung, which is the risk inc36 named and could only assert.

---

## 3. Three tests, because a list is what failed here

`render.py`'s sweep laws lived inside a prototype script that **pytest does not run**. The defect this
increment fixed was exactly that: a list nothing checked, stale for three batches. So the laws move to
where the gate runs them, asserted on the artefacts rather than on the source.

| test | what it holds | teeth |
| --- | --- | --- |
| `test_every_language_has_a_frame_for_every_screen` | every `LG.KITS` × screen has a `.txt`, and there are exactly 66 | one frame moved aside → `AssertionError: ['swiss_S3.txt']` |
| `test_no_two_languages_render_a_screen_identically` | 55 pairs per screen, 330 in all, on the shipped `.txt` | same plant → red |
| `test_no_frame_declares_a_hand_drawn_element` | all 66 sidecars say "Nothing was drawn by hand" | it is the round's headline claim, read off the file that would record a breach |

**They read the shipped artefacts and do not re-render.** A re-render in the suite would need Textual and
a settle per frame; the `.txt` is what every law in this repo measures and what a reader judges, so it is
what is asked. The cost is that a stale artefact passes — which is why `render.py` is run after every
increment that touches a mechanism a frame consumes, and why `git status` after a re-render is quoted in
each packet.

The plant was `mv prototypes/components/swiss_S3.txt prototypes/out/_b37_hold.txt`, and it was moved back
and the three re-run green.

---

## 4. Test results

```
python -X utf8 prototypes/components/render.py   66 .txt + 66 .svg · 330 pairs, none identical
                                                 0 hand-drawn · 0 CLIPPED
python -X utf8 prototypes/components/matrix.py   66 of 66 implementa · every refusal list empty
python -X utf8 -m pytest -q                      933 passed, 2 skipped   (was 930)
python -X utf8 prototypes/verify_language.py     10857 PASS · ALL PASSED (baseline 10857)
git status --short (tracked)                     M render.py · M matrix.py · M test_components.py
```

**No previously committed frame changed.** The 30 frames from `kits-learn-4` were rewritten by the same
sweep and none of them appears as modified — only the 108 new files appear as untracked. The six
inheritors' new `required` and `pane_split` could not have moved them, and now that is measured rather
than argued.

---

## 5. Risks

- **These 36 frames have not been judged.** They are *correct* by every law this repo can run — distinct,
  unclipped, kit-composed, zero hand-drawn — and correct is not the same as good. The five prototyped
  languages went through an operator PROTOTYPE round; these six have not, and nothing here substitutes
  for that.
- **darkside S6 is 8.3 % ink, the sweep's floor.** `verify_ink.py` is not one of this batch's gates, so
  no ink-floor law was applied to any of the 66. DENSITY.md has one; it was not run. Named rather than
  claimed clean.
- **The three new tests pass on stale artefacts.** They assert what is on disk. A `screens.py` edit that
  is never re-swept leaves them green and the frames wrong — the mitigation is procedural (run
  `render.py`, quote `git status`), which is weaker than a test.
- **The suite now depends on files under `prototypes/`.** `tests/` reaching into a prototype directory is
  a coupling this file did not have. It is one path constant and the alternative — re-rendering 66 frames
  inside pytest — costs Textual and a settle per frame.
- **330 pairwise comparisons pass today at ELEVEN languages.** The law gets quadratically harder with
  each kit added, and the first collision will not be a bug in the law.
- **`solari_S1` at 33.5 % and `instrument_S1` at 36.0 %** are the two densest frames in the sweep, both
  on the screen with a split. Neither was checked against a small terminal; the frames are 100×32 and the
  languages' own entries warn about exactly this (swiss "fails: small terminals", instrument "fails:
  dense tabular data").

## 6. Pending

- **A PROTOTYPE round on the six.** Not this batch's, and it is the honest next thing.
- **`verify_ink.py` over the 66** — not run, named.
- **F-8** (`--surface` plain and alone) and the export — the batch close, next.

## 7. Suggested next task

The batch close: `--surface` plain and alone, `export_to_skill.py`, and the gallery candidates.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `933 passed, 2 skipped`. `verify_language.py` **ALL PASSED** at
      10857. `render.py` 66 frames, 330 pairs none identical, 0 hand-drawn, 0 clipped. `matrix.py` 66 of
      66. The three new tests are red-then-green against a moved frame (§3).
- [x] **No secrets in code or output** — two prototype scripts' language lists, one test block, and
      rendered frames of a fixture board. No network, no dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — one `mv` of a frame into the gitignored scratch
      yard and back, for the teeth check, verified by re-running the tests green. Nothing deleted.
- [x] **File count within cap** — 3 source files, plus this packet: 4. The 108 artefacts are the sweep's
      output, not hand-edited files.
- [x] **Review packet attached** — this document.

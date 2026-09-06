# Increment 43 — the exporter paints the style tier, and `reverse` goes back to being a ground

**Batch:** `rework-2` · `PROTOTYPE-inheritors.md` §7 q9 · answers inc41 §4
**Files:** `prototypes/capture_languages.py`, `tests/test_components.py` — **2 source files**, plus the
**33 `.svg` those two re-rendered** (11 component frames + 22 gallery captures). **No `.txt` moved, in
either corpus.**

**inc41 measured 66 declared match runs across the eleven S6 sheets and 0 painted, asserted that as a fact,
and named the sharp case: `reverse` is a GROUND channel that this exporter paints 16 times in
`industrial_S1` and dropped in `industrial_S6`, because Rich hands it over as a style FLAG with colour and
bgcolor still in their declared order. inc43 runs inc41's own comparison again and it comes out EQUAL:
66 declared, 66 painted, 11 of 11. `bold` and `underline` became text attributes; `reverse` became what it
always was — `cell_grid` swaps the pair and the exporter's existing background-run code paints it, with no
new branch and no second idea of what a ground is. The blast radius was larger than the 66: the same
exporter takes the gallery, and eleven boards were carrying 15–48 bold runs each that had never reached a
picture.**

---

## 1. What was actually broken, in one measurement

```
                              MATCH_STYLE        declared   painted@HEAD   painted@inc43
naught       bold #f5f5f5     bold                      6              0               6
corgi        bold #f2f2f2     bold                      6              0               6
instrument   underline …      underline                 6              0               6
swiss        bold #e2231a     bold                      6              0               6
industrial   reverse #ff4b1f  reverse                   6              0               6
nord         bold #88c0d0     bold                      6              0               6
darkside     bold #f5f5f5     bold                      6              0               6
prism        bold #2dd4bf     bold                      6              0               6
ledger       underline …      underline                 6              0               6
solari       reverse #f0ede4  reverse                   6              0               6
blueprint    bold #eef4f8     bold                      6              0               6
TOTAL                                                  66              0              66
```

`painted@HEAD` is measured against the pre-increment `.svg` restored from `HEAD` into a scratch directory,
with the same function that measures the new ones. **This is inc41's comparison, on inc41's numbers, with
the answer it deliberately did not have.**

**And the declaration census answers "which other frames" before the re-render did.** Across all 66 sheets,
`bold` / `underline` / `reverse` / `italic` appear in **exactly eleven — the eleven S6, six runs each, one
word each**. No S1–S5 frame declares a style run at all. So eleven `.svg` were predicted to move and eleven
moved; there was no "any frame with a `match`, `bold` or `reverse` run" beyond them.

## 2. The mechanism, and why the swap is in `cell_grid` and not in the exporter

`Kit.match` is the one contract seat whose emphasis may not add a cell — operator ruling 9, the result text
comes back byte for byte — so all eleven kits spell `MATCH_STYLE` as a style over a hue. Two shapes reach
Rich, and they are not the same kind of thing:

```
bold / underline     a property of the TEXT
reverse              a GROUND channel wearing a style word's costume
```

Measured off the compositor, before anything was changed:

```
naught     S6   'bold=True  ul=None  rev=None'   #f5f5f5 on #121212
instrument S6   'bold=None  ul=True  rev=None'   #2dd4bf on #121212
industrial S6   'bold=None  ul=None  rev=True'   #ff4b1f on #121212      <- NOT swapped
solari     S6   'bold=None  ul=None  rev=True'   #f0ede4 on #121212      <- NOT swapped
```

**That last column is the whole defect.** Rich leaves `color` and `bgcolor` in their declared order and
sets a flag; an exporter reading only `bgcolor` sees the page's own ground and correctly paints nothing.
So the fix is not "teach the exporter a third channel" — it is to resolve the flag where the cell is read:

```python
if st and st.reverse:
    fg, bg = bg, fg
```

After that line the run IS ink on a ground, and `svg_from_grid`'s background-run loop paints it with no
edit at all. **`svg_from_grid` keeps exactly one idea of what a ground is**, which is the property that
would have been given up by branching on `reverse` inside the exporter, and the one that would have let the
two notions drift apart later.

The two changes, in full:

- `cell_grid` — the cell is now `(char, fg, bg, bold, underline)`; `reverse` is resolved into `fg`/`bg` at
  read time. Two call sites in the repo, both updated by the tuple being read positionally.
- `svg_from_grid` — a text run breaks on `(colour, weight, decoration)` instead of on colour alone, and
  emits `font-weight="bold"` / `text-decoration="underline"`.

**What is still dropped, said out loud in the docstring:** `italic`, `strike`, `dim`, `blink`. No kit
declares one. The law below is a comparison of declared runs against painted ones, so the day a kit reaches
for `italic` the law goes red rather than the docstring going quietly out of date.

## 3. The law, and why it is not an arithmetic trick

`test_the_svg_paints_exactly_the_style_runs_the_kit_declared` (11 cases) asserts four things per language:

1. the sheet declares **6** runs;
2. every declared run's word is the kit's own `MATCH_STYLE` word;
3. the `.svg` paints **the same number**;
4. and paints **the same word** — a `bold` language's S6 carries no `text-decoration` anywhere in the file,
   and vice versa. *Six of something* is not allowed to pass for *six of the right thing*.

`test_the_style_law_is_not_vacuous_and_the_two_reverse_kits_are_the_proof` carries the teeth:

- **the swap is asserted, not its arithmetic.** For industrial and solari, all six runs paint the query in
  the CELL'S OWN GROUND on a rect of the kit's hue. Painting the hue as ink on the ground keeps the count
  at six and means nothing was fixed.
- **the seventh `re` is the trap, and it is a real one.** The query also sits in the search FIELD one row
  above the results, in ordinary ink, in all eleven frames. A measurement that counted `<text>` by content
  scores 7. The test asserts 7 total and exactly 6 on the ground — so the discriminator is checked rather
  than trusted.

**Counting reversed runs needed both a hue and a width, and solari is why.** solari's `MATCH_STYLE` is
`reverse {ink}` = `#f0ede4`, which is **the same colour its S6 bands already paint**. Counting rects by
fill scores its two bands as match runs. A reversed run is the query's own cells turned into a ground, so
its rect is exactly `len("re") × 8.4 = 16.8` wide:

```
solari_S6 rect fills, after       industrial_S6 rect fills, after
  1 × #121212  (canvas)             1 × #121212  (canvas)
  2 × #f0ede4  58.8 / 840.0 wide    6 × #ff4b1f  16.8 wide   <- the six runs
  6 × #f0ede4  16.8 wide  <- runs
solari_S6 before: 2 × #f0ede4     industrial_S6 before: none
```

## 4. What this did to the two laws inc41 wrote, and neither had to be deleted

- **`test_the_svg_paints_exactly_the_grounds_the_kit_declared` went red on `industrial_S6`** —
  `declared set()` vs `painted {'#ff4b1f'}` — and it was right to. `declared_grounds` only knew the
  `[#123 on #456]` spelling. **`[reverse #456]` is the same channel said backwards**, and the helper now
  counts it. **The exporter and the census had matching blind spots, which read as agreement on zero.**
- **the vacuity roster is 13 → 14.** `industrial_S6` joins **without one glyph changing**: it declared six
  grounds the whole time and neither side could see them. `solari_S6` was already on the roster for its
  bands, and its reverse hue is the same colour, so the SET did not move even though six rects appeared —
  which is exactly the case the roster exists to make somebody look at.
- **`test_no_style_tier_survives_the_exporter_and_that_is_why_S6_is_unjudged` is deleted**, as its own
  docstring instructed: *"the day the exporter learns a style, this goes red and points at the round that
  has to be redone."* It went red on `naught` first. It is replaced by the two laws above, not dropped.

## 5. Files and frames changed

**The eleven component `.svg`, and nothing else in that corpus:**

```
blueprint_S6  corgi_S6  darkside_S6  industrial_S6  instrument_S6  ledger_S6
naught_S6     nord_S6   prism_S6     solari_S6      swiss_S6
```

**All 66 `.txt` are byte-identical** — md5 of every one taken before and after; not one differed. That is
the expected result and the one that matters: the `.txt` is the artefact every law measures, a style is not
a cell, and this increment did not put one there.

**THE BLAST RADIUS WAS LARGER THAN THE 66, AND THIS IS THE JUDGMENT CALL IN THIS INCREMENT.**
`prototypes/gallery/` is taken with **the same `svg_from_grid`** — `render.py`'s own docstring says why
(*"if these frames were produced by a second renderer they would not be comparable"*), and inc42 committed
a gallery re-bake one commit ago. So **all 22 gallery `.svg` moved and all 22 gallery `.txt` did not**:

```
board_*.svg      11 files   bold runs: naught 48, corgi 44, blueprint 30, ledger 27, solari 27,
                            instrument 26, industrial 24, nord 23, prism 23, swiss 21, darkside 15
gallery_*.svg    11 files   bold runs: 2 each
```

The live board has been declaring bold — the meter's `◦◦◦◦` runs among them — for as long as these
captures have existed, and no picture of it ever showed one. **Leaving the gallery unbaked was the one
alternative and it is the worse one:** it would put the two corpora on two different exporters, which is
the exact property `render.py` exists to protect. **33 generated `.svg` in one increment is over the
nominal five-file cap; they are the output of one two-file change and not five decisions, the batch
instruction authorised re-rendering all 66, and the gallery follows from the same edit — but it was not
asked for by name, so it is flagged here rather than buried in a file list.**

## 6. The skill: re-exported, and its own gallery is untouched

```
$ python -X utf8 prototypes/export_to_skill.py                                   exit 0
  wrote C:\Users\jjgh8\.claude\skills\tui-design\assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 22 written, 44 already identical -> ...\tui-design\assets\languages
  wrote SURFACES.md (11 postures)
```

**22 written** are the 22 gallery `.svg`; **44 already identical** are the 22 `.txt` and the 22
`surface_*` files. The export agrees with `git status` from the other side.

```
$ python -X utf8 assets/gallery/verify_gallery.py                                exit 0
  [ok  ] 44_instrument-list-graticule   100×32  BOX-FREE (0 corners, 56 box-draw cells)
  [ok  ] 45_industrial-list-plate       100×32  BOX-FREE (0 corners, 135 box-draw cells)
  [ok  ] 46_swiss-list-next-column      100×32  BOX-FREE (0 corners, 229 box-draw cells)
  [ok  ] 47_solari-list-gate-seam       100×32  BOX-FREE (0 corners, 0 box-draw cells)
  [ok  ] 48_industrial-modal-plate-lid  100×32  BOX-FREE (0 corners, 139 box-draw cells)
  [ok  ] 49_darkside-modal-rounded-lid  100×32  BOXED (1 box walked)
  [ok  ] 50_solari-form-printed-severity 100×32  BOX-FREE (0 corners, 6 box-draw cells)
  [ok  ] 51_instrument-monitor-dot-ladder 100×32  BOX-FREE (0 corners, 0 box-draw cells)
  [ok  ] INDEX.md                        51 entries, 2 commitment lines each

  52 passed, 0 failed  (51 frames)
```

**The skill's gallery is untouched, which is the case the round asked to have stated.** Its 51 `.svg` live
in `assets/gallery/svg/` and are generated by the skill's OWN `render_svg.py` from the `.txt`; the export
writes to `assets/languages/` and never reaches them. Checked three ways: mtimes still 00:02 (this work ran
at 10:22), **zero of the 51 contain `font-weight`**, and `verify_gallery.py` passes all 52 checks including
frames 44–51.

## 7. Gates, verbatim

```
$ python -X utf8 -m pytest -q                                                    exit 0
1004 passed, 2 skipped, 4 warnings in 38.12s
```
inc42's 993 **− 1** (the deleted style-tier limit) **+ 12** (eleven parametrised style-law cases and the
vacuity/teeth test) = **1004**.

```
$ python -X utf8 prototypes/verify_language.py                                   exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                 exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                 exit 0
11 rows x 6 screens, every cell `implementa -`
per screen: no primitive missing in any language; refusals, by language: all []

$ python -X utf8 prototypes/capture_languages.py                                 exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
```

**`render.py` was run a second time and all 132 artefacts came back byte-identical** — the new exporter is
idempotent, so a frame moving in a later increment will mean a frame moved, not that the renderer is noisy.

## 8. Risks

- **A bold face may not have the same advance as its regular.** `svg_from_grid`'s whole grid strategy is
  one `x` per run, and its docstring is explicit that error cannot accumulate ACROSS a row because the next
  run re-anchors at its own absolute coordinate. A bold run is still a run with its own `x`, so the
  guarantee is unchanged — but **inside** a bold run, a viewer whose fallback bold face has a different
  advance will drift, and bold runs on the boards are up to 23 cells long. Not observed; not measured in a
  browser either. Named because it is the property this file spent two rejected designs to protect.
- **`text-decoration="underline"` is a presentation attribute SVG inherits from CSS.** It renders in every
  engine tried by `render_svg.py`'s lineage, and it is not otherwise exercised here.
- **The reversed-run count uses a width.** `16.8` is `len(QUERY) × CW` and would need revisiting if the
  fixture's query changed length. The alternative — counting by fill — is the one solari breaks (§3), so
  the coupling is deliberate and the constant is derived rather than typed.
- **33 generated `.svg` in one increment** (§5). Flagged, not hidden.
- **The gallery boards now carry 15–48 bold runs each and nobody has judged those pictures.** They are
  more faithful than what they replace, which is not the same as saying anyone has looked.

## 9. Pending — found by looking, not fixed

- **The live board's bold has never been judged in a picture.** Eleven boards, 15–48 runs each, invisible
  until this increment. Whether every one of those is a deliberate weight channel or an inherited default
  is a question for the language round, not for the exporter.
- **solari's match is the same colour as solari's bands.** `reverse {ink}` = `#f0ede4` = the S6 band
  ground. A match run that lands ON a band is a band-coloured rect on a band — invisible. The six in this
  frame do not, so it does not show; it is a collision in the declaration and belongs to inc44's census.
- **`gallery_darkside` is calendar-dependent** (inc42 §3). Still live.
- **`blueprint_S4`'s destructive control has no danger mark and no focus mark** (inc41 §8). Still live.

## 10. Suggested next task

inc44 — `verify_ink.py` naming its subject, and the collision census the language rework needs.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1004 passed, 2 skipped`, exit 0 (§7), with the arithmetic
      993 − 1 + 12 shown. `verify_language.py` **ALL PASSED** exit 0. `render.py` 66 frames, exit 0, run
      twice and byte-identical the second time. `matrix.py` 66 of 66, exit 0. `capture_languages.py` 22
      grids identical across two processes, exit 0. The skill's `verify_gallery.py` **52 passed, 0 failed**.
- [x] **No secrets in code or output** — a renderer change and a test change; every artefact is a picture
      of the synthetic `_fixture_late.json` or of a composed kit sheet. No network, no dependency.
- [x] **No destructive commands run without approval** — none. `git show HEAD:...` copied eleven `.svg`
      into `prototypes/out/` (ignored) to measure the before-count; nothing was checked out over the tree.
- [x] **File count within cap for hand edits, OVER it for artefacts** — 2 source files, 33 regenerated
      `.svg`, this packet. §5 states the call and the alternative that was rejected.
- [x] **Review packet attached** — this document.

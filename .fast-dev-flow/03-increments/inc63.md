# Increment 63 — the exporter's ground is DECLARED, never inferred

**Batch:** `rework-6a`, increment 1 of 4 · ruling **E4**, the one objection of
`PROTOTYPE-inheritors-3.md` that is not a kit, a sheet or a law but a line of the exporter.
**Files:** `prototypes/capture_languages.py`, `prototypes/components/render.py`,
`prototypes/race_probe.py`, `tests/test_components.py` — **4 source files**, plus **66 regenerated
component `.svg`** (0 `.txt`, 0 gallery artefacts) and this packet.

**All 66 component sheets shipped their canvas as `#121212` — Textual's own default screen ground, a
colour no kit in this corpus declares.** Ten dark languages survived that by luck. ledger, the corpus's
only light-paper kit (`ground #e9e1cf`, `ink #1c1a15`), shipped six sheets of **1.08:1** — black ink on
a black canvas, with the dot leaders (`#c4b99f`, 9.62:1) the only legible thing on the page and the
hierarchy therefore exactly inverted. The defect had two halves that agreed with each other:
`cell_grid()` took *"the most common background in the frame"* for its ground, and `render.py` assigned
the screen's background **after the first paint**, too late for strips the compositor had already
cached. So every cell arrived on `#121212`, the frequency count agreed, and no rect was ever written
over it. After this increment every one of the 66 canvases carries `THEMES[lang]["ground"]`, the worst
ink-on-ground contrast in the corpus is **10.60:1** (blueprint), and **the 22 gallery artefacts are
byte-identical** — which is the strongest evidence available that the new ground is the right one,
because those 22 were already correct and the declared ground reproduces them exactly.

Suite 1111 → 1123. `.txt` byte-identical, all 66.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **E4:** the exporter reads the kit's declared `ground` and `ink`; it never infers them from frequency.

> **F, amended:** the band never covers a gate HEADER row, of any gate; it covers task rows of the first
> gate the confirm does not name, below that gate's header, and goes to the foot of the schedule when no
> such rows exist. A frame must never show a task under a gate it does not belong to.

> **G vs ruling 10:** on S4 the fixture mood is calm; G applies to S2 only. Recorded, no code.

> **inc60 info to air:** doctrine for blueprint and ledger (a line-type ladder where absence is the calm
> state, LANGUAGES.md §11 and #9). Recorded, no code.

> **C, follow-through:** the channel C freed on swiss gets filled: the invalid text field has a wall,
> paper and a closer from swiss's own alphabet.

This increment carries out **E4**. The other four are `inc64`–`inc66` and the batch's §16.

## 1. The measurement, before anything was written

`prototypes/components/*.svg` at `abd5193`, the canvas rect of every one of the 66, against
`THEMES[lang]["ground"]`:

| language | declared `ground` | canvas the `.svg` painted | `ink` | contrast against the canvas | against the declared ground |
|---|---|---|---|---|---|
| naught | `#000000` | `#121212` | `#f5f5f5` | 17.18 | 19.26 |
| corgi | `#0d0d0d` | `#121212` | `#f2f2f2` | 16.73 | 17.36 |
| instrument | `#0a0d12` | `#121212` | `#e8edf2` | 15.90 | 16.52 |
| swiss | `#101010` | `#121212` | `#f4f4f4` | 17.03 | 17.30 |
| industrial | `#1a1a1a` | `#121212` | `#f2f2f2` | 16.73 | 15.55 |
| nord | `#2e3440` | `#121212` | `#eceff4` | 16.25 | 10.84 |
| darkside | `#000000` | `#121212` | `#f5f5f5` | 17.18 | 19.26 |
| prism | `#0d1117` | `#121212` | `#e6edf3` | 15.85 | 16.02 |
| **ledger** | **`#e9e1cf`** | **`#121212`** | **`#1c1a15`** | **1.08** | **13.36** |
| solari | `#0b0b0c` | `#121212` | `#f0ede4` | 16.00 | 16.81 |
| blueprint | `#123a5c` | `#121212` | `#eef4f8` | 16.89 | 10.60 |

**Eleven of eleven were wrong, not one.** `PROTOTYPE-inheritors-3.md` §0a reported ledger because ledger
is the only kit whose ground is far enough from `#121212` for the eye to catch it; the round's
`cell_grid()` diagnosis (*"measures the background as the most common background"*) is right and the
blast radius is the whole corpus.

**And the same measurement over `prototypes/gallery/*.svg` came back CLEAN — 22 of 22 carrying the
declared ground.** That is what told this increment there were two halves. A frequency count that
returns the right answer on the board sweep and the wrong one on the component sweep is not measuring a
ground; it is measuring which pipeline set its background before the first paint.

```
board_ledger      painted #e9e1cf  declared #e9e1cf      ledger_S1..S6   painted #121212
gallery_ledger    painted #e9e1cf  declared #e9e1cf      declared #e9e1cf
```

## 2. Cause and mechanism

**Cause, half one — the exporter.** `capture_languages.cell_grid()` ended with a frequency count over
every cell's background and returned the winner as the frame's ground, *"measured, not assumed, because
several languages paint a full-bleed panel over it"*. A count cannot distinguish a ground from a
full-bleed mistake; when the mistake covers 3200 of 3200 cells it wins by definition.

**Cause, half two — the render path.** `prototypes/components/render.py` mounted the sheet, awaited
`pilot.pause()`, and only then assigned `app.screen.styles.background`. Measured directly:

```
screen bg style:     Color(233, 225, 207)          # e9e1cf -- the assignment DID take
static rich_style:   #e0e0e0 on #e9e1cf            # and the widget knows it
compositor strip:    '> ' #2b3a67 on #121212       # and the cached strips do not
bg counts:           [('#121212', 3200)]
```

The assignment lands on the styles object but never reaches strips the compositor has already cached,
so the capture reads a frame the screen no longer describes. `capture_languages.sweep_surfaces()` had
the identical shape and is fixed the same way.

**Mechanism.**

- `cell_grid(app)` becomes **`cell_grid(app, ground)`** — the declared ground is a required argument,
  the frequency block is deleted, and the same value is both the canvas and the "this cell needs no
  rect" test. `svg_from_grid` is untouched: it already had exactly one idea of what a ground is.
- `write(...)` gains `ground: str = ""` and **raises** when an SVG is asked for without one. The three
  call sites (`sweep`, `sweep_surfaces`, `race_probe.sweep_into`) pass `THEMES[lang]["ground"]`.
- `render.py` and `sweep_surfaces()` declare the ground **in the Screen CSS, before compose**, instead
  of assigning it after the first pause. Verified before the change was kept:

  ```
  ledger S6     declared #e9e1cf  [('#e9e1cf', 3200)]
  blueprint S4  declared #123a5c  [('#123a5c', 3188), ('#eef4f8', 12)]   # the knockout survives
  nord S1       declared #2e3440  [('#2e3440', 3200)]
  ```

**Both halves were necessary and neither is sufficient.** Fixing only the exporter would have written
the right string into the canvas rect and then covered it with a full-bleed `#121212` run — the picture
unchanged, the law green. That failure mode is the second tooth below.

## 3. The law

`test_the_svg_canvas_is_the_kits_declared_ground`, parametrised over the eleven, over all six screens —
**66 frames, three clauses**:

1. the canvas rect's fill **equals** `LG.kit(lang).t["ground"]`;
2. `contrast(ink, ground) >= 4.5` (WCAG 1.4.3 body text), computed in the test from the two hexes with
   `L = 0.2126R + 0.7152G + 0.0722B` over linearised channels and `(L1+0.05)/(L2+0.05)`;
3. **once every background run is subtracted, no colour has more area left than the declared ground.**

Clause 3 is why clause 1 is not vacuous. `ground_report()` returns the canvas colour and the area each
ground colour actually *shows*, in the picture's own coordinate units — the canvas's share being what is
left after every `<rect>` is taken off it. It has no opinion about cell width, which is the exporter's
business.

The floor is nowhere near any kit, so the ratios are also **written down** rather than only bounded
(`GROUND_INK_CONTRAST`): a kit that walked its ink halfway to its paper would still clear 4.5:1, and a
number moving in that table is a design change somebody has to look at.

```
naught 19.26 · corgi 17.36 · instrument 16.52 · swiss 17.30 · industrial 15.55 · nord 10.84
darkside 19.26 · prism 16.02 · ledger 13.36 · solari 16.81 · blueprint 10.60
```

## 4. Teeth

`test_the_declared_ground_law_bites_on_the_defect_it_was_written_for` — **not a monkeypatch and not a
hand-built picture.** `ledger_S6.svg` as it ships, edited the two ways the defect actually presents:

- **(a) the canvas takes Textual's ground.** One substitution on the canvas rect. `ground_report` reads
  `#121212`, the contrast clause reads **1.08:1**, `< 4.5` asserted.
- **(b) the canvas is right and something full-bleed sits on it** — the shape a naive fix takes.
  Clause 1 passes (asserted, and the assertion says so: *"that is the point"*); clause 3 catches it.

**And the law was watched failing on the real pre-inc63 bytes**, restored from `abd5193`:

```
ledger_S1      canvas #121212  declared #e9e1cf  canvas==declared False  widest #121212  contrast 1.08
ledger_S6      canvas #121212  declared #e9e1cf  canvas==declared False  widest #121212  contrast 1.08
industrial_S1  canvas #121212  declared #1a1a1a  canvas==declared False  widest #121212  contrast 16.73
prism_S4       canvas #121212  declared #0d1117  canvas==declared False  widest #121212  contrast 15.85
```

industrial and prism are in that list on purpose: they show the law biting where **no contrast problem
exists**. The defect was never only ledger's.

## 5. One existing law had to be repaired, and it was resting on the defect

`test_the_style_law_is_not_vacuous_and_the_reverse_kits_are_the_proof` went **RED** on solari the moment
the ground became correct:

```
AssertionError: ('solari', ['\xa0BOARD\xa0', '\xa0COMMAND\xa0\xa0QUERY\xa0'RE'\xa0\xa0·\xa06 RESULTS…',
                            're', 're', 're', 're', ...])
```

It read *"no text run anywhere in this sheet is painted in the ground colour except the six match
runs"* — and that held **only because the canvas was wrong**. `#121212` is a colour no kit declares, so
every legitimate knockout in the frame fell outside the query by accident. With `#0b0b0c` in place,
solari's masthead plates paint ink in the ground too, and they are not match runs.

Repaired by **pairing on coordinate, which is stronger than what it replaced**: `svg_from_grid` puts a
text run's baseline `0.78` of a line below its row's top, which is where that row's background rect
starts, so each of the six ground-inked `re` runs must sit on a `<rect>` of the kit's own match hue at
the same `x` and `y - 13.26`. Measured: industrial 6 hue rects / 6 match runs, darkside 6 / 6, **solari
8 / 6** — the two extra being exactly the masthead plates that broke the old blanket assertion.

Watched failing by hand with the plates stripped out of a copy of `solari_S6.svg`:

```
plates removed -> [False, False, False, True, False, True]     # law RED
```

The old assertion's other half — *the seventh `re`, in the search field, is not a match run* — is
untouched and still asserted (`len(every) == 7`, `every.count(ground) == 6`).

## 6. Frames changed

**66 of 66 component `.svg`.** Every language, every screen: the canvas moves from `#121212` to the
declared ground, and any run that was suppressed for matching `#121212` is now written or dropped
against the right ground. The brief expected "ledger's twelve and possibly others"; the answer is **all
of them**, which §1 measures and §0a of the round did not predict because it read the one language where
the mistake is visible.

**0 of 66 `.txt`.** `git diff --stat -- 'prototypes/components/*.txt'` is empty. The ground is a colour;
the text artefact cannot carry it.

**0 of 22 gallery artefacts.** `capture_languages.py` plain re-run: `22 captures`, `22 grids identical
across two PROCESSES`, and `git status --porcelain prototypes/gallery/` **empty**. Those 22 were already
right, and the declared ground reproduces them byte for byte — the closest thing to a control arm this
increment has.

**Gallery 30–51 in the skill:** untouched by this increment, and `export_to_skill.py` is run at the
close of the batch, not here.

Background-run coverage after the change, per frame, as a share of the picture (the input to clause 3):

```
industrial_S1 28.25%   prism_S4 48.84%   solari_S1 12.41%   ledger_S1 3.50%   ledger_S4 3.50%
darkside_S1 2.53%   prism_S1 2.53%   solari_S2..S6 3.1-3.8%   blueprint_S2/S4 0.34/0.38%
everything else 0.00%
```

`prism_S4` at 48.8% is the corpus's widest legitimate panel and is comfortably under its own ground.

## 7. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1123 passed, 2 skipped, 4 warnings in 34.31s

$ python -X utf8 prototypes/verify_language.py
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)  worst 4 of 40 over 155 captures

ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ python -X utf8 prototypes/components/matrix.py
--- refusals, by language ---
naught     []   corgi      []   instrument []   swiss      []   industrial []   nord       []
darkside   []   prism      []   ledger     []   solari     []   blueprint  []
                                                        (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       25
TOTAL homoglyph rows             1
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  re-sweeping in a fresh process to check reproducibility...
  22 grids identical across two PROCESSES

  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)

$ git status --porcelain prototypes/gallery/
                                                        (empty)
```

Suite: **1111 → 1123** (+11 parametrised arms of the new law, +1 teeth). Census **25**, homoglyph rows
**1** — both unchanged; this increment moved no declaration.

## 8. Risks

1. **`cell_grid`'s signature changed and it is imported by four modules.** `render.py`, `write()` and
   `race_probe.py` are updated; `write()` raises rather than guesses when an SVG is asked for with no
   ground, so a fifth caller added later fails loud instead of shipping `#000000`.
2. **The surface sweep (`--surface`) is fixed but NOT re-run** — it is not in this batch's gates and its
   artefacts are not in `prototypes/gallery/`. Its next run will move its `.svg` files the same way the
   66 moved. Said out loud rather than left to be discovered.
3. **Clause 3 is an area comparison, not a legibility measurement.** A kit could paint 49% of a sheet in
   a colour that ruins it and pass. What the clause exists to forbid is the *canvas being covered by the
   thing it replaced*, and that is what it does.
4. **Ruling E (the `.svg` is darkside's artefact of record) is now audited and holds** — §7.3 of the
   round objected that the promotion presupposed a faithful exporter and that darkside's survival was
   luck. It was luck: darkside declared `#000000` and shipped `#121212`. It is now measured.

## 9. Found by looking, not fixed

- **The law measures `ink`, and most body text in these sheets is `mut`.** The ruling names `ground` and
  `ink`, so the law asks about `ground` and `ink` — but `mut` against the declared ground, measured with
  the same formula while writing the law, is the sharpest thing this increment turned up and did not
  touch. **Five of the eleven are below the 4.5 floor:**

  ```
  nord 3.50 · solari 3.65 · instrument 4.26 · darkside 4.43 · ledger 4.45
  blueprint 4.65 · industrial 5.38 · swiss 5.51 · naught 6.08 · prism 6.43 · corgi 6.91
  ```

  Not fixed and not asserted here: moving a `mut` is a design change in five kits at once and it is
  nobody's ruling. It belongs on the objection list, not inside an exporter increment.
- **`#2dd4bf` is still the match accent of two languages at once** (instrument and prism) and still the
  ink of prism's `▸` cursor on the same row — §0c of the round, third time named, untouched here.
- **`_TEXTUAL_DEFAULT_GROUND = "#121212"` is now a constant in the test file.** It is there because it is
  the colour 66 frames shipped, and the teeth reproduce that on real bytes. If Textual's default ever
  moves, the teeth still test the historical defect, which is the right behaviour.
- **The frequency count was not merely wrong, it was self-confirming.** `svg_from_grid` suppresses a rect
  whenever `bg == ground`, so the more completely a mistake covers the frame the more certainly the
  exporter agrees with it and the fewer rects it writes to leave a trace. The old `ledger_S6.svg`
  contains **zero** background rects.

## 10. Pending — not this increment

- **inc64** — prism's inverted checkbox (L8) and its two-directional fill (L9).
- **inc65** — `solari_S4` under F amended, and `corgi_S4` under inc40's head law (C8).
- **inc66** — the S4 walls (C2) and swiss's freed channel.
- `mut` against ground, unmeasured in all eleven (§9).
- E2 (no font metric in the `.svg`), K2, K5, L6, L7, C5–C7, C9, C10, G1, G2 — all still open.

## 11. Suggested next task

`inc64`, as briefed: prism's checked knob must be the fuller cell, and the language's fill direction
must be one declaration used at S1, S3 and S5.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1123 passed, 2 skipped, 1 failed`
      (baseline for this batch, measured before any edit: `1111 passed, 2 skipped, 1 failed`). The
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      **reported, not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py` 66
      frames / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `capture_languages.py`
      plain: 22 captures, 22 grids identical across two processes, **0 moved**. `collision_census.py`
      both self-checks green, TOTAL 25, homoglyph rows 1.
- [x] **No secrets in code or output** — one exporter argument, two CSS declarations, two call sites, one
      contrast helper, one area reader, two tests. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none. Pre-change bytes were read with
      `git show abd5193:…` into `prototypes/out/inc63_before/`.
- [x] **File count within cap** — **4 source files**: `prototypes/capture_languages.py`,
      `prototypes/components/render.py`, `prototypes/race_probe.py`, `tests/test_components.py`.
      `race_probe.py` is in because it is the fourth caller of `write()` and the new signature would
      have failed it at run time; `test_components.py` carries both the new law and the repair of §5.
- [x] **Review packet attached** — this document.

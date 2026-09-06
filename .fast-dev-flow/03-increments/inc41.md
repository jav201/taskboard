# Increment 41 — the SVG paints the tier the kit declared; the tier it drops is a different one

**Batch:** `rework-1` · `PROTOTYPE-inheritors.md` §0b, §2.7 `blueprint_S4`, §4, §7 q2/q3/q9
**Files:** `tests/test_components.py` — **1 source file. No kit and no sheet was changed, and §1 is why.**

**The premise inverts on inspection. `blueprint_S4.svg` paints `DELETE` as the sheet's knockout because
the OPERATOR ruled on 2026-09-04 that it may — ruling 10, recorded verbatim, implemented by inc17, cited
at two seats — and because the `.txt` cannot carry a background, which three separate places in this repo
had already published. The exporter decided nothing: measured over all 66 frames, it paints exactly the
grounds the kits declare, no more and no fewer. What the exporter DOES drop is the STYLE tier — 66
declared match runs across the eleven S6 frames, none painted — and that is the round's §4, an operator
question, and now an asserted limit instead of a silence.**

---

## 1. Question 10 was answered by the operator, not by the render

`PROTOTYPE-inheritors.md` §0b:

> *"`PROTOTYPE.md` §4, pregunta 10 … **Ya se movió.** … La respuesta a la pregunta 10 fue «sí» y la dio el
> render, no el operador."*

**`PROTOTYPE.md` §4 is titled "Preguntas para el veredicto" — it is the list of questions PUT to the
operator, not a list of open ones.** All ten were answered on 2026-09-04 and the answers are recorded:

> `.fast-dev-flow/archive/spec-20260905-kits-learn-3-closed.md` §6.1 — *"the operator's ten rulings
> (2026-09-04) — the law of this batch"*:
>
> **10. Blueprint's knockout may *move* from the title block to the default answer in a confirm —
> exactly one per view.**

inc17 implemented it (`.fast-dev-flow/03-increments/inc17.md`: *"Batch: kits-learn-3 · AC-4 · operator
rulings 4, 5 and 10"*, and §"`knockout_cell`, and ruling 10"). It is cited at both seats that spend it:

- `Kit.knockout_cell` — *"operator ruling 10 lets that single knockout MOVE to a confirm's default answer.
  A mechanism that can move needs a seat to move to."*
- `screens.s4_blueprint` — *"the ONE thing this language changes: operator ruling 10 lets its single
  knockout MOVE from the title block to the default answer."*

**And the `.txt` limitation was published before the round, three times.** `knockout_cell`'s docstring:
*"AND IT IS THE ONE MARK IN THIS FILE THAT DOES NOT SURVIVE THE `.txt`: an inversion is a background, so a
cell grid shows the word and not the emphasis. Recorded rather than worked around — the honest place to
read a knockout is the SVG."* `s4_blueprint` says it again. `PROTOTYPE.md` §3 said it first, as a
collateral finding: *"el knockout de blueprint es invertir el fondo, y el `.txt` no lo lleva … la
convención de la casa es que el `.txt` es la obra — aquí no basta."*

**So the `.txt` and the `.svg` do not disagree about which control is the knockout. They agree; one of
them cannot show it.** That is `PROTOTYPE-inheritors.md` §7 **q10** — whether the `.txt` stays "the work"
— and it is the operator's, not this increment's. **No fix. Doctrine, cited.**

---

## 2. The exporter has no opinion — measured, over 66 frames

The round's inference was that `svg_from_grid` had made a choice. It has not made one anywhere:

```
declared grounds (from the composed markup)  ==  painted <rect> fills (svg, minus the sheet canvas)
                                            66 of 66 frames
```

The 13 frames that declare a ground at all, which is the law's whole evidence:

```
industrial_S1 [#2e2e2e]        darkside_S1 [#1f1f1f]      prism_S1 [#1f2630]
ledger_S1     [#e0d7c2]        solari_S1   [#17171a #e03a2f #f0ede4 #f5a300]
solari_S2     [#f0ede4]        solari_S3   [#17171a #f0ede4]
prism_S4      [#1f2630]        ledger_S4   [#e0d7c2]      solari_S4 [#f5a300]
blueprint_S4  [#eef4f8]        solari_S5   [#17171a #f0ede4]   solari_S6 [#f0ede4]
```

The other 53 declare none and paint none — a true pass and an empty one, which is why the roster above is
asserted (`test_the_ground_law_is_not_vacuous`) rather than left implied.

**Compared as SETS, not counts, on purpose.** A ground run crossing a row boundary becomes several
`<rect>`s: prism declares one and gets 22, industrial declares one and gets 16. Counting would assert a
fact about Textual's segmentation instead of about the kit. What the law is for is a colour appearing
that nobody asked for, or one that was asked for and did not arrive.

`blueprint_S4`'s single declared ground is `#eef4f8`, which is `knockout_cell`'s own composition
(`[{t['ground']} on {c['ink']}]` = `[#123a5c on #eef4f8]`), and the `.svg` paints that rect with that fill
and the text on it in that foreground. **Faithful to the cell.**

---

## 3. `├ CLEAR ┤` is an UNSPENT law, not a missing one

The round's corollary: *"en los seis frames el title block se dibuja `<text ... fill="#7fa8c4">├ CLEAR ┤`,
tinta normal: **el knockout del title block no se renderiza en ninguno de los seis.**"*

True, and it is the mechanism working. `Blueprint._state_cell`:

> *"The reverse fires on `alert` alone, so a sheet with nothing overdue carries no reversed cell at all —
> and still states its condition."*

and the class docstring's next bullet: *"**alert is spent on OVERDUE and nothing else.** A calm sheet
carries zero `alert`."* The seeded board is calm, so the state cell says `CLEAR` in normal ink. Exercised
in both moods so the claim is not a story about a dead branch:

```
mood 'clear'  ->  ('├ CLEAR ┤',   False)
mood 'alert'  ->  ('├ OVERDUE ┤', True)
```

**And this is exactly what makes ruling 10's move legal rather than merely permitted** — the argument
`s4_blueprint` already wrote down and the round did not pick up: *"the sheet's one knockout is UNSPENT and
the confirm may take it without the title block losing anything. 'Exactly one element per view' holds by
arithmetic, not by promise."*

**Phrasing risk worth naming.** `Blueprint.__doc__` opens the bullet with *"exactly ONE element per view
reverses … and it is the title block's STATE cell"*, which reads as a floor; the bullet two lines down
turns it into a ceiling. The round read the first without the second. Nothing is wrong in the code and
nothing is edited here, but the sentence has now misled one careful reader.

---

## 4. What the exporter DOES drop, and it is not a background

`Kit.match` marks the query inside a result row with `MATCH_STYLE`, which every one of the eleven spells
as a **style** over a hue:

```
naught bold {ink}          corgi bold {ink}         instrument underline {accent}
swiss  bold {alert}        industrial reverse {accent}   nord bold {accent}
darkside bold {ink}        prism bold {accent}      ledger underline {ink}
solari reverse {ink}       blueprint bold {ink}
```

Every S6 sheet declares **6** such runs. `svg_from_grid` emits background runs and fill colours and
nothing else, so:

```
66 declared style runs across the eleven S6 frames    ->    0 painted
0 `font-weight` and 0 `text-decoration` in any of the eleven S6 `.svg`
```

**The sharp case is the one the round called diagnosable, and it holds up.** industrial's
`reverse {accent}` and solari's `reverse {ink}` ARE a ground channel — the same channel this exporter
paints 16 times in `industrial_S1` — and they are still not painted, because `reverse` reaches Rich as a
style word rather than as `on <colour>`. `painted_grounds("industrial", "S6")` is empty;
`painted_grounds("industrial", "S1")` is not.

**Not fixed here, and the reason is scope rather than difficulty.** Teaching the exporter
`bold` / `underline` / `reverse` re-renders all 66 `.svg` and **re-opens the round that judged them** —
`PROTOTYPE-inheritors.md` §7 q9 puts that to the operator in exactly those terms. What this increment
does instead is make the limit **falsifiable**: `test_no_style_tier_survives_the_exporter_and_that_is_why_S6_is_unjudged`
goes red the day a style is painted, and points at the round that has to be redone.

---

## 5. What changed

`tests/test_components.py`, four tests and five helpers. **No kit, no sheet, no frame.**

| test | what it holds |
| --- | --- |
| `test_the_svg_paints_exactly_the_grounds_the_kit_declared` | 11 languages × 6 screens: declared grounds == painted rect fills |
| `test_the_ground_law_is_not_vacuous` | the 13-frame roster, derived and compared with a written one |
| `test_blueprints_knockout_is_where_operator_ruling_10_put_it` | the ruling quoted in the docstring; the rect/text pair matched to `knockout_cell`'s own colours; the title block's cell exercised in both moods |
| `test_no_style_tier_survives_the_exporter_and_that_is_why_S6_is_unjudged` | 66 declared style runs, 0 painted, and the two `reverse` languages named |

**The pair is its own teeth.** The same comparison — *what the kit declared against what the exporter
painted* — comes out EQUAL on the ground tier in 66 of 66 and UNEQUAL on the style tier in 11 of 11. A
law that only ever passed would prove nothing about the comparison; this one is watched failing on a real
tier in the same file.

**One coupling introduced, said out loud:** `sheet_rows()` imports `prototypes/components/screens.py` into
the suite, because the declarations exist nowhere else — the `.txt` has them stripped and the `.svg` has
them rendered. `screens.py` imports without Textual (unlike `render.py`, which is why `FRAMES` is a path
and not an import), and the helper adds the three paths its own `fixture` import needs. It is the first
time this file reaches into `prototypes/` for anything but bytes on disk.

---

## 6. Gates, verbatim

```
$ python -X utf8 -m pytest -q
993 passed, 2 skipped, 4 warnings in 32.82s
```
(inc40's 979 + 14: eleven ground-law cases, the vacuity roster, the ruling-10 seat, the style-tier limit.)

```
$ python -X utf8 prototypes/verify_language.py                                   exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                 exit 0
  66 .txt + 66 .svg   ·   66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                 exit 0
11 rows x 6 screens, every cell `implementa -`; no missing primitives, no refusals

$ python -X utf8 prototypes/capture_languages.py                                 exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
```

**Frames changed by this increment: none.** `render.py` re-swept all 66 and every one came back
byte-identical, which is the expected result of an increment that changed only tests.

---

## 7. Risks

- **`sheet_rows()` couples the suite to a prototype module.** If `screens.py` ever grows a Textual import,
  or `fixture.py` grows a side effect, four tests break for a reason that has nothing to do with what they
  assert. The alternative was to assert nothing about declarations, which is what let §0b happen.
- **The ground law is a SET comparison.** A frame that declared a colour twice and painted it once would
  pass. Counts were rejected for a stated reason (§2), but the gap is real.
- **The style-tier test asserts a defect as a fact.** That is deliberate and it is also the sort of test
  that gets read as an endorsement. Its docstring says three times that it is a limit awaiting §7 q9; if
  the operator answers q9 by teaching the exporter, this test is the first thing to delete.
- **Nothing here judges whether ruling 10 was a good ruling.** It was made, it is recorded, and this
  increment holds the code to it. `PROTOTYPE-inheritors.md` §7 q2 asks the operator to reconsider it; that
  is still open and this increment does not prejudge it.

## 8. Pending — found by looking, not fixed

- **`blueprint_S4`'s destructive control has no danger mark and no focus mark, in EITHER tier.** The
  `.txt` reads `DELETE    ├  CANCEL  ┤`. `screens.s4_blueprint` builds the confirm's default answer with
  `k.knockout_cell(" DELETE ")` instead of `k.button(..., FOCUSED, danger=True)`, so DELETE loses its
  walls, its `DANGER_FORM` (`━`) and its focus state, and gains the reverse. **Ruling 10 moved the
  KNOCKOUT; it did not say the default answer stops being a button.** It is the only one of the eleven S4
  frames where the destructive control carries no danger mark — the same shape of defect inc38 fixed for
  swiss, on a worse control. Fixing it needs `knockout_cell` and `button` to compose (a knockout wrapping
  already-tagged markup double-escapes), which is a new kit seat or a `knockout=` parameter on
  `Kit.button` — **a design change, so it is named and left for the operator** rather than invented here.
- **`prototypes/gallery/gallery_darkside.{txt,svg}` are stale on disk and it is not this batch's doing.**
  `capture_languages.py` renders a radio as `( )` where the committed frame has `(.)`. **Proved not mine:**
  `taskboard/language.py` was checked out at the pre-batch commit `8604607`, `capture_languages.py` re-run,
  and the identical diff appeared; source and gallery were then restored. The gallery was last baked at
  **inc21**, and `language.py` has been edited in at least a dozen increments since. Somebody changed a
  glyph and never re-baked. Re-baking is 22 artefacts and belongs to whoever owns that sweep.
- **`prototypes/out/_b37_test.py` still makes `pytest -q` mutate the suite** (inc39 §9). The filename
  matches pytest's default `*_test.py`, so bare `pytest` from the repo root runs its module body and
  appends a duplicate block to `tests/test_components.py`; HEAD carries three such copies. Neutralised by
  hand for all three commits in this batch. **One line fixes it** — `testpaths = ["tests"]` in
  `pyproject.toml`, or rename the probe.

## 9. Suggested next task

The three items in §8, in that order: the `pyproject.toml` line first (it is one line and it stops the
repo corrupting itself on every gate run), then blueprint's confirm button, then the gallery re-bake.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `993 passed, 2 skipped` (§6). `verify_language.py` **ALL PASSED**,
      exit 0. `render.py` 66 frames / 330 pairs / 0 hand-drawn, exit 0, **0 frames moved**. `matrix.py`
      66 of 66, exit 0. `capture_languages.py` 22 grids identical across two processes, exit 0.
- [x] **No secrets in code or output** — four tests and five helpers, all reading files already in the
      repo. No network, no dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. The drift probe checked out `language.py`
      at `8604607` and restored it from `HEAD` in the same command; `git status` after it showed only the
      intended test-file edit. `tests/test_components.py` restored from a snapshot after `pytest` to undo
      the self-append of §8.
- [x] **File count within cap** — 1 source file (`tests/test_components.py`) plus this packet and the
      `spec.md` `rework-1` section: 3.
- [x] **Review packet attached** — this document.

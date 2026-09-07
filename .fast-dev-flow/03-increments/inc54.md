# Increment 54 — the destructive default answer is a button that carries the knockout

**Batch:** `rework-5a`, closing increment · carries out **Ruling C1** on `PROTOTYPE-inheritors-2.md` §5
**C1**, named in inc41 §8 and carried untouched through inc49 §12, inc50 §10 and inc51 §11
**Files:** `taskboard/language.py`, `prototypes/components/screens.py`, `tests/test_components.py`
— **3 source files**, plus 2 regenerated frame artefacts and this packet.

**Operator ruling 10 of 2026-09-04 let blueprint's single knockout MOVE from the title block to a
confirm's default answer. inc17 implemented the move with `knockout_cell(" DELETE ")` — and a cell is not
a control, so the one irreversible answer on that sheet had NO danger form and NO focused walls in either
tier, while ten other languages' S4 carried both. The ruling did not say the default answer stops being a
button. `Kit.button` gains a `knockout` keyword — not a composition, because `mark()` would escape the
button's own tags — which puts the tier over the WHOLE seat in ONE span, so "exactly one knockout per
view" is still one ` on ` tag. Blueprint's S4 answer is now `╞ ━DELETE━ ╡` reversed, and the law that
says so is asked of all eleven off the shipped frames. Frames: `blueprint_S4` (txt + svg), and nothing
else.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **inc54 · Ruling C1: the destructive default answer is a button that carries the knockout**
> `screens.s4_blueprint` builds DELETE with `knockout_cell(" DELETE ")`, so it has no danger mark and no
> focus mark in either tier. Ruling 10 of 2026-09-04 moved the knockout to the default answer; it did not
> say the default answer stops being a button. Add the kit seat: `Kit.button(..., knockout=True)` (or a
> `knockout` state the button composes; pick the one that does not double-escape and say why), so
> blueprint's S4 default answer renders as `button(FOCUSED, danger=True)` with the knockout tier on the
> whole seat; "exactly one knockout per view" must still hold (test). The other ten languages: a
> `knockout` request on a language whose registry refuses knockouts (`KNOCKOUT_REFUSED`? read what
> exists) falls back to the plain focused danger button. Law: in every language's S4, the destructive
> default answer carries the language's danger form, its focused form, and, where the language spends a
> knockout, the knockout tier, in both txt and svg (extend inc41's tier comparison). Frames changed:
> blueprint_S4 (txt+svg); explain any other.

---

## 1. What was there, measured against the other ten

`screens.py` composes the confirm's answers in two places, and they were two different shapes:

```python
answers(sh)          # ten languages
    k.button("Delete", 10, FOCUSED, danger=True) + "   " + k.button("Cancel", 10, DEFAULT)

s4_blueprint(sh)     # the eleventh
    k.knockout_cell(" DELETE ") + "   " + k.button("CANCEL", 8, DEFAULT)
```

**`knockout_cell` is one tag around one string.** It has no walls, no state, no danger form — its whole
docstring is *"a cell that trades ink for ground"*. So blueprint's `.txt` read

```
                            DELETE    ├  CANCEL  ┤
```

**the SAFE answer is the only one on the row that looks like a control**, and the irreversible one is a
bare word. In the `.svg` the word gained a reversed ground and still no walls and no `━ ━`. Read against
the other ten at the same seat, the gap is not subtle:

```
naught      '○  ∙Delete∙  ○'      instrument  '⠼  ⠛Delete⠛  ⢧'      swiss      '▪  ╲Delete╱   '
corgi       '▔▔ █Delete█ ▔▔'      industrial  '▐_╱╱Delete╱╱_▌'      nord       '▐  #Delete#  ▌'
darkside    '▮  ▚Delete▞  ▮'      prism       '⣿⢤ ⣿Delete⣿ ⢤⣿'      ledger     '▶  (Delete)  │'
solari      '▔  ▀Delete▄  ▔'      blueprint   'DELETE'
```

(the focused walls of each language's `button.main`, with its `DANGER_FORM` around the word — the
pattern the law in §4 builds and searches for.)

## 2. The seat: a keyword, and why not a composition

```python
def button(self, label, w=0, state=DEFAULT, danger=False, knockout=False):
    ...
    if knockout and self.knockout:
        return (f"[{self.t['ground']} on {self.c['ink']}]"
                f"{mark(walls[:half] + text + walls[half:])}[/]")
```

**A KEYWORD AND NOT `knockout_cell(self.button(...))`, and the reason is `mark()`.** The ruling asked for
the shape that does not double-escape and this is the measurement: `mark` escapes a literal `[` as `\[`,
and a composed call would hand it a string that is ALREADY markup — so every tag the button wrote would
come back as literal text in the frame. The tier has to be chosen INSIDE, where the pieces are still
plain.

**ONE SPAN AND NOT THREE, which is what keeps the ruling's own test countable.** The walls and the word
go inside a single `ground on ink` run, so a view's knockouts are its ` on ` tags and
`test_exactly_one_knockout_per_view_still_holds_on_blueprints_confirm` can count them. Three tags would
be one element to a reader and three to the counter — and the counter is the only thing that can tell.

**The per-part tones are deliberately dropped.** A knockout that let the walls keep their own hue would
be two channels fighting over one seat; a knockout IS the tier of the whole element.

## 3. What "the registry refuses knockouts" turned out to be

The ruling asked whether a `KNOCKOUT_REFUSED` roster exists. **It does not, and one was not invented.**
What exists is the theme token:

```
naught corgi instrument swiss industrial nord darkside prism ledger solari   knockout=None
blueprint                                                                    knockout=True
```

and `Blueprint.knockout`, a property reading it. `verify_language` already flips that token to prove the
reverse video is live rather than hardcoded (*"blueprint.knockout=False removes the reverse video AND
the …"*). **A second roster would have been a second place to say the same thing**, and the two would
have drifted — so the property MOVED UP to `Kit`, unchanged, because `button` has to ask it of all eleven
and a property on one subclass can only answer for one. `Blueprint`'s copy is deleted; it now inherits
the identical implementation.

**A refused request is IGNORED, not raised on.** Ten of the eleven have no token, and a caller composing
one S4 for all of them should not have to know which; for them `knockout=True` returns the plain button
of the state and danger they asked for, byte for byte.

## 4. The law, over all eleven, read off the shipped frames

`test_the_destructive_default_answer_is_a_focused_danger_button[lang]`, eleven parametrisations:

> In every language's S4 the irreversible default answer carries **this language's DANGER FORM**, **this
> language's FOCUSED WALLS**, and — where the registry spends a knockout — **the KNOCKOUT TIER over the
> whole seat**, in the `.txt` and in the `.svg`.

**It is read off the shipped frame and not off the composition**, which is what keeps it from asserting
that `screens.py` equals itself: the pattern is built from the KIT's declarations —
`button.main[FOCUSED]` split in half, `DANGER_FORM` around the word, centred to the width `screens.py`
passes — and searched for in `<lang>_S4.txt`. A language that stopped drawing its focused walls there, or
drew a bare word, goes red. Then, for a language that spends a knockout, the `.svg`'s reversed run is
matched against the SAME seat string — which is the extension of inc41's tier comparison the ruling
asked for: inc41 asserts *declared == painted* over all 66 frames as SETS; this asserts **which run**
carries the ground and **what is inside it**.

Two more tests:

- **`test_a_knockout_a_language_refuses_falls_back_to_the_plain_button`** — asserted as an EQUALITY
  against the un-knocked call rather than as "no ` on ` appears", because the second would also pass if
  the knocked call returned something else entirely. And the one language that DOES spend it must
  DIFFER, which is the half that keeps the test from being vacuous: an implementation that ignored the
  keyword everywhere would satisfy the ten and fail there. It also asserts the roster —
  `[lang for lang in LANGS if kit(lang).knockout] == ["blueprint"]`.
- **`test_exactly_one_knockout_per_view_still_holds_on_blueprints_confirm`** — the ruling's own
  condition, counted on the composed rows of the frame the knockout moved to.

**`test_blueprints_knockout_is_where_operator_ruling_10_put_it` was UPDATED, not replaced.** Ruling 10
stands and the cell still reverses; what moved is that the reversed thing is a button. The test now
asserts the BUTTON seat as well as `knockout_cell`'s own contract (which is still a seat, still used by
the title block), and the `.svg` assertion reads `╞ ━DELETE━ ╡` where it read ` DELETE `.

**Watched fail by hand, on the real composition.** `s4_blueprint` reverted to `knockout_cell(" DELETE ")`
and the frames re-rendered:

```
$ python -X utf8 -m pytest tests/test_components.py -q -k "destructive_default or exactly_one_knockout"
E  AssertionError: ('blueprint', '╞ ━DELETE━ ╡',
                    ['                           DELETE 3 TASKS?  …',
                     '                            DELETE    ├  CANCEL  ┤  …'])
E  AssertionError: the seat is gone
FAILED ...test_the_destructive_default_answer_is_a_focused_danger_button[blueprint]
FAILED ...test_exactly_one_knockout_per_view_still_holds_on_blueprints_confirm
2 failed, 10 passed in 0.42s
```

**The law names the language, the seat it expected and the rows it actually found**, and the other ten
parametrisations stay green under the same revert — which is what says this was one language's
composition and not a base defect. `screens.py` was restored from a byte copy and `render.py` re-run;
the thirteen re-run green.

## 5. Frames changed — `blueprint_S4` only

```
 M prototypes/components/blueprint_S4.svg
 M prototypes/components/blueprint_S4.txt
```

```
before                             DELETE    ├  CANCEL  ┤
after                             ╞ ━DELETE━ ╡   ├  CANCEL  ┤
```

and the `.svg`, where the knockout is the honest place to read it:

```
-<rect x="236.8" y="282.0" width="67.2"  height="17.0" fill="#eef4f8"/>
-<text x="236.8" y="295.3" fill="#123a5c"> DELETE </text>
-<text x="329.2" y="295.3" fill="#eef4f8">├  CANCEL  ┤</text>
+<rect x="236.8" y="282.0" width="100.8" height="17.0" fill="#eef4f8"/>
+<text x="236.8" y="295.3" fill="#123a5c">╞ ━DELETE━ ╡</text>
+<text x="362.8" y="295.3" fill="#eef4f8">├  CANCEL  ┤</text>
```

**One rect, wider by four cells, and the reversed run now contains the walls and the danger marks.**

**Nothing else moved, and the reason is arithmetic rather than luck.** `knockout=` defaults to `False`,
so the other ten `k.button(...)` call sites in `screens.py` return the same bytes; `Kit.knockout` reads a
token ten themes do not carry; and `knockout_cell` is untouched, so blueprint's title block, its tabs and
`_state_cell` are byte for byte what they were. **Gallery: 0 of the 22** — the board draws no confirm.
**Census: 33 → 33 and homoglyph rows 4 → 4** — no glyph table and no meaning mark changed.

**Of the eight frames whose gallery copies live in the skill, none moved this increment.** (`darkside_S4`
moved in inc52 and inc53; `blueprint_S4` is not one of the eight.)

## 6. Gates, verbatim

```
$ python -X utf8 -m pytest -q
1083 passed, 2 skipped, 4 warnings in 38.99s

$ python -X utf8 prototypes/verify_language.py                                        exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
  -> 1 of the 66 moved

$ python -X utf8 prototypes/components/matrix.py                                      exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                                      exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 0 of the 22 moved

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  1 of the 5 collisions the round found by hand still come back out of
              the census; 4 are asserted CLOSED and cannot grow back
  self-check  the homoglyph roster is exact for all eleven (4 rows, 3 languages)
  TOTAL  33 -> 33     ·     TOTAL homoglyph rows  4
```

**`1070 → 1083`: +13** — eleven parametrisations of the law, the fallback test, the one-per-view count.

**A NOTE ON THE CLIPBOARD RED, because it moved twice in this batch.**
`tests/test_app.py::test_win_clipboard_roundtrip` was RED at `6970cac` (the batch's base) and has been
GREEN on every run of this batch, including one FAILING run inside this increment before the last one. It
drives the real Windows clipboard through PowerShell and fails when anything else on the desktop holds
it (spec §10.6). **It is environment-coupled in both directions: reported, not counted, not touched.** Do
not read `1083 passed` as evidence that it was fixed.

## 7. Risks

- **The destructive answer got FOUR CELLS WIDER** (8 → 12) and the row grew from 23 cells to 27. At
  W=100 inside a 60-cell overlay that is air; at a narrower measure the two answers would be the first
  thing to collide. Nothing in this repo renders S4 below 100 cells, so it is untested rather than safe.
- **The knockout now paints the WALLS as well as the word.** A reversed run of 12 cells is a bigger block
  of ground than a reversed run of 8, and blueprint's first-fixation law is *"exactly ONE element per
  view reverses"* — one element, but a louder one. `PROTOTYPE-inheritors-2.md` has not judged the new
  frame and neither has the operator.
- **`━DELETE━` spends `━` a sixth time in blueprint** (`LEVELS["error"]`, `DANGER_FORM`, the sparkline
  peak, the scrollbar's view, the ladder S5 reads — and now visibly on S4, where before the danger form
  was simply absent). inc51 §9 already flagged the accumulation; this increment makes it visible in a
  frame for the first time rather than adding a role.
- **`Kit.knockout` is now on the base class, so any future theme that sets the token gets the behaviour
  without anybody looking at its S4.** That is the point of a registry, and it is also how a language
  acquires a knockout by accident. The law in §4 would catch it — it asserts the tier for every language
  whose registry spends one — which is why the law is parametrised over all eleven and not written for
  blueprint.
- **`knockout_cell` still exists and is still the title block's seat.** There are now TWO ways to reverse
  a cell, and the difference between them (a cell versus a control) is exactly the distinction this
  increment exists to draw. A caller who reaches for the wrong one gets the old defect back and only the
  §4 law is watching.

## 8. Found by looking, not fixed

- **`answers()` composes the destructive answer for ten languages and `s4_blueprint` for the eleventh**,
  and the two are now the same SHAPE but still two call sites with two labels (`Delete`/`DELETE`) and two
  widths (10/8). The law's `S4_ANSWER` table has to carry that split. Folding the two into one call is a
  `screens.py` refactor and is not this increment's.
- **Blueprint is the only language in the corpus with a `knockout` token**, so the fallback branch of
  `Kit.button` is exercised by ten languages and the knockout branch by one. `verify_language`'s existing
  token-flip is the only place the reverse direction is proven.
- **The `.txt` still cannot show the knockout** — `knockout_cell`'s docstring records it and it is now
  equally true of `button(knockout=True)`. What the `.txt` gained is the DANGER FORM and the FOCUSED
  WALLS, which is the half of C1 that the cell grid can carry.

## 9. Pending — the operator's, untouched by this batch

- **A** — corgi, prism and blueprint have never had an increment. `rework-5a` moved corgi's invalid
  channel and blueprint's twice and judged neither frame.
- **E** — `darkside_S1`: the rail or the `.txt`. inc53 came near it and stayed off the vertical stroke
  for that reason.
- **F** — may a solari confirm eat the gate it names? **G** — blueprint's first-fixation law is in a test
  and in no image; this increment made the knockout bigger and did not answer it.
- **K2** (the laws compare code points — inc53's homoglyph table is the first crack in it), **K4**,
  **L1–L6**, **C2**, **C4–C7**, **E2**, **E3**.

## 10. Suggested next task

**Close the batch (phase C): `spec.md` §13 `rework-5a`, then `export_to_skill.py`.** After that, **corgi**
— decision A's sharpest entry, three increments of this programme have edited its declarations and no
frame of it has ever been judged.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1083 passed, 2 skipped, 0 failed` (§6), with the
      environment-coupled `test_win_clipboard_roundtrip` explicitly reported and not counted (§6's note:
      it was red at the batch base, red once mid-increment and green at the end). `verify_language.py`
      ALL PASSED exit 0. `render.py` 66/330/0, 1 of 66 moved. `matrix.py` 66 of 66.
      `capture_languages.py` 22 captures, 0 moved. `collision_census.py` both self-checks green,
      33 → 33. The law was watched fail by hand on the real composition; the output is verbatim in §4.
- [x] **No secrets in code or output** — one keyword argument, one property moved up a class, one
      composition line, three test functions. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The watch-it-fail experiment used byte copies of `language.py` and
      `screens.py` and restored from them.
- [x] **File count within cap** — 3 hand-written source files (`taskboard/language.py`,
      `prototypes/components/screens.py`, `tests/test_components.py`); the 2 frame artefacts are written
      by `render.py`.
- [x] **Review packet attached** — this document.

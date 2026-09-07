# Increment 67 — the quantity widgets join set B, and a fill cell stops being a meaning mark

**Batch:** `rework-6b`, increment 1 of 4 · **K5**, under **ruling A amended**.
**Files:** `taskboard/language.py`, `taskboard/naught.py`, `prototypes/collision_census.py`,
`prototypes/verify_language.py`, `tests/test_components.py` — **5 source files**, plus 12 regenerated
component artefacts (6 frames), 4 regenerated gallery artefacts (2 frames) and the regenerated census
table.

**Every law in this repo read `PART_GLYPHS`, `FIELD_LEAD` or `IDENT_GLYPHS`, and a progress bar is
none of those.** So `MEANING_AT_AN_OPENER` and `MEANING_AT_A_NAMED_SEAT` could both read **0 for all
eleven languages** while `naught_S1` drew thirteen `∙` — that kit's `LEVELS["error"]` and its
`DANGER_FORM` byte for byte — ten rows above a task whose overdue leader is the same cell, and while
`corgi_S1` spent **forty-seven** `█` on a partition, a creature and a pager without one of them meaning
a danger. Three of `PROTOTYPE-inheritors-3.md`'s eight new `rework` verdicts lived in exactly the widget
the instruments could not see. Suite **1165 → 1188**. **Census 26 → 35**, and every one of the nine is
the new surface becoming visible rather than a kit getting worse; **homoglyph rows 1 → 2**, the extra
one likewise. `█` in `corgi_S1`: **47 → 2**. `⣿` in `prism_S3`: **11 → 2**.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **A, amended (K5):** the census's B set reaches every quantity widget: slider, bar, scrollbar, meter,
> sparkline, pager, mascot. Their fill and track cells are chrome; a fill cell may not be a meaning mark
> of its language.

> **D, amended (K2):** the homoglyph list is derived, not enumerated: two cells are homoglyphs when they
> are the same base shape at a different size or fill (ring/disc, dot sizes, dash counts within a
> family), and the named four join it now: naught `⊙`/`◉` and `○`/`◦`, ledger `†`/`‡`, blueprint
> `╌ ┄ ┈`.

> **L2:** a disabled control always carries a mark; air is not a state.

> **`mut` contrast:** `mut` is body text and must reach 4.5:1 against the declared ground in every kit,
> with the ladder `ink > mut > dim` kept ordered.

This increment carries out **A amended**. D amended is inc68, L2 is inc69, `mut` is inc70.

---

## 1. The four frames, read before anything was written

```
naught_S1  f13   ◦ ∙∙∙∙∙∙∙∙∙∙∙∙∙ ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦  44%
                 ^^^^^^^^^^^^^ thirteen ∙ = LEVELS["error"] = DANGER_FORM, and
                 f23 is `∙ Rate-limit the API … 2d!`, where ∙ means overdue.
                 ∙ stands 70 times in this frame and two of them are the answer.

corgi_S1   f04-f30  █ [D] D E T A I L …        the partition, 25 rows tall
           f18-f23  ██ ██ / █  █ / ██████      the creature, 18 cells
           f31      view ██ ░░ ░░ ░░           the pager's current page
                 47 candidates for "point at the cells that mean irreversible",
                 zero of them correct, and the tallest is a wall.

prism_S1   f31   view ⠒⣿⣿⣿⣿⠒⠒⠒⠒⠒⠒⠒ 3-10 of 23
                 the window drawn in LEVELS["error"] / DANGER_FORM, to say
                 "you are here". ⣿ stands 28 times in this frame; none is a danger.

prism_S3   f16   row density   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70
           f20   ⠿⠉⣿Delete all⣿⠉⠿
                 nine cells of the danger form as a VALUE, four rows above two
                 cells of it as an IRREVERSIBLE ACT.
```

**The criterion, in the round's own words:** *«en `prism_S3`, tapar las palabras y decir cuál de las dos
tiradas de `⣿` es un valor y cuál es un botón irreversible.»* Before this increment the frame had eleven
candidates and no answer. After it, it has two.

---

## 2. The declaration: four of the seven widgets needed none, and three did

The ruling names seven widgets. **Four were already declared and only the READER excluded them:**

| widget | where it lives | what was wrong |
| --- | --- | --- |
| slider | `COMPONENT_PARTS["slider"]` → `PART_GLYPHS` | in the tables since the registry was written |
| bar | `COMPONENT_PARTS["bar"]` | same |
| scrollbar | `COMPONENT_PARTS["scrollbar"]` | same |
| **pager** | **IS the scroll bar** | `screens.s1` calls `k.scrollbar(st, sz, tot, 12)`; `corgi_S1`'s `view ██ ░░ ░░ ░░` and `scrollbar.indicator` are ONE declaration seen twice |

Their absence was `collision_census.py`'s `OTHERS` tuple — *"SLIDER, BAR AND SCROLLBAR ARE OUT OF THE B
SET by the same request, which named six controls"* — a **reader's boundary, not a missing
declaration**. inc67 deletes the boundary; the tuple stays, empty, so the diff shows what it was.

**Three are drawn outside `PART_GLYPHS` in all eleven and needed a declaration:** the **meter**, the
**sparkline** and the **mascot**.

### 2.1 Which shape, and why

The brief left the choice open (*"a `QUANTITY_GLYPHS` table or entries in `PART_GLYPHS` the census
reads; pick what the registry pattern supports and say why"*). **It is a method on the `Kit`,
`quantity_glyphs()`, and not entries in `PART_GLYPHS`.**

`PART_GLYPHS` is keyed by part and read by `part_glyph` **through the state chain**: every row in it
answers *"what does this slot look like in state X"*. A meter has no states — it has a **value** — and a
mascot is a drawing. Putting them there would hand `component_states`, the disabled-seat law and the
checked-pair law three components with no states to walk, which is precisely the dead metadata
`COMPONENT_PARTS` refuses by name at `GRIPS` and `VIEWED` (*"a `knob` added here to make it feel
operable would be the dead metadata this file has refused twice"*).

**The precedent for a declaration outside the tables is inc57's**, and this is its third and fourth
member: `FIELD_LEAD` and `IDENT_GLYPHS` were literals inside methods until a census could not see them,
and the census's own docstring states the rule — *"a mark a language DRAWS and this file cannot SEE is
this census's own blind spot, and the fix is a declaration rather than a bigger reader."*

### 2.2 Derived, never typed

A hand table of 11 kits × 4 seats that nothing reads is the thing this codebase rules against. Every
value comes from a seat that already exists:

* **`meter.fill` / `meter.track` / `meter.open` / `meter.close`** — a new registry row `METER_CELLS`,
  keyed on the **same `meter` token** that dispatches `METERS` and `METER_RAMP`. An `int` is an index
  into `cover_ramp()` (the ONE SEAT, #45 — six of the thirteen mechanisms ask it for their cells and
  spelling those as literals here would be the second answer that seat exists to prevent); a `str` is a
  literal that mechanism owns; `None` is a mechanism with no such cell, which is how `odometer` and
  `dimension` — the two `RAMPLESS_METERS` — say they have no fill at all.
* **`spark.peak` / `spark.floor`** — `cover_ramp()[-1]` and `[0]`, because `Kit.spark` routes through
  that same seat in every branch but `odometer`.
* **`mascot.pixel`** — `base_pixel(base)`, a new function that renders an all-on bitmap at the base's own
  declared sub-cell resolution (`bases.BASES[base]["sub"]`). **A mascot's partial cells are its pixel at
  partial coverage** — a braille cat is a full cell in the middle and part-cells along its edges, exactly
  as a ramp's middle steps are its terminal partly covered — so the declaration is the PIXEL. A law that
  read every cell of the artwork would be measuring the drawing, not the alphabet. Two kits override it:
  corgi (§3.2) and naught, whose `mascot()` is `face()` and never reaches `bases.py` at all.

### 2.3 And a law binds the declaration to the drawing

`test_a_quantity_widget_draws_what_it_declares`, over all eleven. Two of the three seats are read by the
drawing directly — `_meter_dotgrid` passes `meter.fill`/`meter.track` into `NA.dot_meter`, and
`Kit.mascot` substitutes `MASCOT_PIXEL` — but the other eleven mechanisms spell their cells in eleven
different structures (a braille bitmap, groups of five, a printed figure), so one `(fill, track)` pair
read at the call site would have to be re-expanded inside each of them anyway. **The table is the
declaration and the law is what makes it true:** every widget is rendered at its floor and at its
ceiling and the declared cells have to be the cells that came out.

Its last clause is the one worth naming: **`solari` declares NOTHING**, and that is asserted rather than
allowed. An odometer's quantity is a row of FIGURES, its spark is the one branch of `Kit.spark` that
never reaches a ramp, and it keeps no pet — the one kit of the eleven whose whole quantity vocabulary is
outside this law, asserted so a ramp arriving there cannot arrive in silence.

---

## 3. The law, and the four fixes it forced

> **A fill cell is never a `LEVELS` / `DANGER_FORM` / `REQUIRED` mark of its language.**

`test_a_fill_cell_is_never_a_meaning_mark`, all eleven, over six seats:
`slider.indicator`, `bar.indicator`, `scrollbar.indicator` (from the tables, every state) and
`meter.fill`, `spark.peak`, `mascot.pixel` (from the declaration).

**The FILL and not the track**, which is the ruling's own word and the same narrowing the opener law
makes. A track is the ground a reading is laid on and three languages spend their calm rung on it
deliberately — corgi's `▁▁`, naught's `◦`, prism's `⣀`. The FILL is the datum. *A language may lay a
quantity on its own ground; it may not say "this much" with the cell it says "this is an error" with.*

**It is a ROSTER, not a zero**, on inc48's own precedent (*"IT IS A MEASUREMENT, NOT A PASS. Four
languages still fail it, counted per language so the roster can only move when somebody edits it"*).
**22 rows before this increment, 16 after.**

### 3.1 naught — the ladder counts, the meter charges

`_meter_dotgrid` called `NA.dot_meter`, which filled with `NA.ON` — a literal inside a drawing function,
and that literal is `∙`, this kit's error rung and its danger byte. `dot_meter` takes `on`/`off`
arguments now and `_meter_dotgrid` passes the declaration in.

The cell is `NA.CHARGE = "◉"`, the rung **above** the lit dot on this kit's own charge ramp
(`⋅ ◦ ∙ ◉ ●`). The argument is the language's own sentence, kept instead of two readings sharing a cell:
**the lattice COUNTS (`◦◦ / ∙◦ / ∙∙` is a count of lit dots) and the pixel CHARGES.**

```
naught_S1 f13   before  ◦ ∙∙∙∙∙∙∙∙∙∙∙∙∙ ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦  44%
                after   ◦ ◉◉◉◉◉◉◉◉◉◉◉◉◉ ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦  44%
```

`∙` in that frame: **70 → 57**. The thirteen that were a percentage are gone; the two that mean overdue
stand.

### 3.2 corgi — the bar is milled, not driven

Two declarations, one ruling: inc58's **THE BANK IS THE READING, THE PANEL IS THE MILLED METAL**.

* `PANE_RULE` `█` → `▓`. A pane edge is panel, so it takes the top step of the shade ramp — the same
  ramp the switch's live track and the field's paper are cut from, and no rung of anything.
* `MASCOT_PIXEL` `""` → `▓`. This kit's base is `segment`, which cannot draw a creature, so `Kit.mascot`
  falls back to `block` — and the fallback's pixel is `█`. The drawing is kept and its pixel moves.

`█` in `corgi_S1`: **47 → 2** (the pager's `██`, which is a roster row). In `corgi_S6`: **18 → 0**.

### 3.3 prism — a slider is a control, and a thumb follows its own shaft

inc59 scoped the toggle away from the ember because **a toggle is a control and is read from the TOP**,
and left the slider behind. **A slider is a control by the same registry fact the toggle is one**:
`GRIPS` says it has a knob, and `COMPONENT_PARTS` says in as many words that *"a switch is a slider whose
range is boolean"*. So the slider takes the toggle's tables byte for byte:

```
slider.main       ⣀ / ⠄   ->   ⠉ / ⠄     (= switch.main)
slider.indicator  ⣿ / ⣤   ->   ⠿ / ⠛     (= switch.indicator)
```

And the pager: prism's own comment already said *"a shaft is not a scale … the shaft is drawn as an
unlit lattice and the thumb is the only fire on it"* — **the shaft had left the ember and the thumb had
not**. `scrollbar.indicator` `⣿`/`⣤` → `⠿`/`⠛`.

```
prism_S3 f16   before  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70      after  ⠿⠿⠿⠿⠿⠿⠿⠿⠿⢸⠉⠉⠉⠉ 70
prism_S1 f31   before  view ⠒⣿⣿⣿⣿⠒⠒⠒⠒⠒⠒⠒        after  view ⠒⠿⠿⠿⠿⠒⠒⠒⠒⠒⠒⠒
```

`⣿` in `prism_S3`: **11 → 2**, and the two are `⣿Delete all⣿`.

### 3.4 The exemption, by name, and why it is not a blanket

The ruling permits *"exemptions by name only where the doctrine says the meter IS the severity device"*.
`THE_METER_IS_THE_SEVERITY_DEVICE`, three seats in two languages, each with its citation:

| seat | citation |
| --- | --- |
| prism `meter.fill` | inc59: *"the ember is read from the BOTTOM"*. `LEVELS ⣀⣤⣿` IS the ember's own ramp read as three rungs, and `DANGER_IS_THE_TOP_RUNG` already names `⣿⣿` here |
| prism `bar.indicator` | the readbar is that same ember through `component_cells`; **no grip** (`actuator("bar")` is `None`), and `PROTOTYPE-inheritors-3.md` §2.10 judges `prism_S5`'s `⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀` correct BY NAME |
| corgi `meter.fill` | inc58: *"THE BANK IS THE READING…"*. `LEVELS ▁▁/▄▄/██` IS the segment bank at three heights |

**The slider and the pager do not get it, and the frame is why.** Ruling A's own condition is that an
exemption *"leave the opener of a control distinct from an error rung IN THE FRAME"* — `prism_S3` puts
nine cells of the slider's fill four rows above `⣿Delete all⣿`, and `prism_S1`'s pager drew the same cell
to say "you are here". The frame refused the exemption exactly as it refused corgi's and naught's blanket
ones in `rework-5c`.

### 3.5 The sixteen rows that stand, by owner

| language | n | what they are |
| --- | --- | --- |
| naught | 3 | `slider.indicator`, `bar.indicator` and the creature's pixel, all the lit dot. The lattice IS this language, and the round §2.8 calls that face the best thing on `naught_S6`. Named, not moved |
| corgi | 6 | the slider's and the bar's two heights (`▁▁ ▄▄`), the pager's `██`, and the spark's peak (`█` — **L6**) |
| swiss | 3 | the hairline meter's `━`, the spark's `━`, the dead scroll thumb's `─`. **L6**, and in this language it is the whole quantity family: the severity ladder IS the weight ladder |
| prism | 1 | the mascot's `⣿` — the braille base's own terminal. Moving it means a second base for one drawing, or no creature. `prism_S4` puts eight of them three rows under `⣿Delete⣿` |
| solari | 1 | the pager's `▄`, `DANGER_FORM`'s lower half. One cell of a two-cell hatch whose other half is nowhere near it — the weakest row here, and still a row |
| blueprint | 2 | the pager's `━` and the spark's `━`. Same shape as swiss |

**Five of the sixteen are L6** (*the sparkline is drawn with the top rungs of `LEVELS`*), which
`spec.md` §16.6 lists as untouched. They are now **counted** for the first time.

---

## 4. The two seat laws were extended where the ruling said, and only there

**The knob law reaches `slider.knob`** — `KNOB_SEATS` gains `("slider", "knob")` and
`meaning_marks_at_named_seats` loops `RULED_CONTROLS + ("slider",)`. It costs nothing: all eleven grips
are clean (`◉ ▙▟ ⡇ │ | ▌ ◎ ⢸ ▪ ▼ ┤`, not one of them a rung), so **both rosters stay at 0 for all
eleven**. It is here so that the day one is not, somebody has to edit a number.

**The DEAD-mark clause does not follow it**, and the narrowing is measured rather than assumed: looping
the slider through that clause too costs exactly **one** row — corgi's `slider.indicator[disabled]`
(`▁▁`, `LEVELS["info"]`, a dead fill drawn with the calm rung) — and nothing anywhere else. Ruling A
amended asks for the laws *"where a quantity widget has an opener or a knob"*; a disabled track is
neither.

**The opener law reaches the meter's bracket.** Two of the thirteen mechanisms bracket their run —
industrial's `[ … ]` and blueprint's `├ … ┤` — and a bracket is an announcement in exactly the sense
this law means. Both are clean today.

**The slider, the bar and the scroll bar are NOT asked for an opener**, and the reason is structural
rather than a scope choice: their `main` and `indicator` are a cell the composer **repeats**, so `▁▁`'s
"opener" is `▁` and its "closer" is `▁` — the same cell twice, with nothing announced. Measured before it
was left out: it fires on **corgi fifteen times and nowhere else**, and every one of the fifteen is
already a row on `FILL_IS_NOT_A_MEANING`.

---

## 5. Teeth

`test_the_fill_law_goes_red_on_the_declarations_inc67_moved` — **three arms on the REAL declarations
this increment changed**, each naming the seat the row comes back at:

1. `METER_CELLS["dotgrid"]` restored to `(NA.ON, NA.OFF)` — the row returns at `meter.fill` and nowhere
   else, and naught goes 3 → 4.
2. `Prism.PART_GLYPHS["scrollbar.indicator"][DEFAULT]` restored to `⣿` — `prism_S1` row 31 verbatim.
3. `Corgi.MASCOT_PIXEL` emptied — the row returns at `mascot.pixel` with `█`.

Plus a **vacuity check on the exemption**: emptied, it grows exactly `{"prism": 3, "corgi": 1}` and
moves no other language.

`test_a_quantity_widget_draws_what_it_declares` carries its own teeth in its shape — the meter clause
asserts the fill is drawn at the ceiling **and not at the floor**, so a mechanism that swapped its two
cells goes red here as well as at inc64's direction law.

---

## 6. Three existing laws had to move, and every move is written into the test

* **`CORGI_BANK_BEFORE`'s `knob` row: named seats 4 → 6.** `knob` is the SHARED table — the switch's
  grip and the slider's — so one restored declaration now shows at both. The two extra rows are
  `slider.knob` at `default` and `focused`, which is `corgi_S3`'s own finding: this kit drew `██` as the
  slider's KNOB twelve rows above `▁▁█Delete all█▁▁`, **and only the switch's half of it was ever
  counted.**
* **`BLUEPRINT_SHEET_BEFORE`: openers 7 → 8, then 12 → 13.** Restoring `REQUIRED = "├"` now also lights
  `meter.open`, because blueprint's `dimension` opens its span with the very terminator inc60 took
  obligation off — a seat no law in this file could reach until the quantity widgets were declared. The
  arms are cumulative, so the second number carries the first.
* **`NAUGHT_LATTICE_BEFORE`: named seats 10 → 11.** `◉` is `PART_GLYPHS["knob"][DEFAULT]`, so restoring
  obligation onto it lights the slider's grip as well as the switch's.
* **`test_prism_draws_no_control_on_the_embers_own_rungs`** asserted `part_key("slider","indicator") ==
  "indicator"`. It now asserts the opposite, plus that the slider's two tables are the toggle's **byte
  for byte** and that no cell of `slider.*` or `scrollbar.indicator` is on the ember ramp.
* **`CELL_INK` gains `◉` (0.22)** — the direction law needs a weight for naught's new fill. **Only that
  one cell:** `●` was added in the first draft and made the ticked-box law read a filled disc as
  *lighter* than its outline, because `mark_ink` already scores hollow/solid on its own. A weight is
  added when a law needs it, never as a set. That first draft is recorded in the comment.

---

## 7. `verify_language.py` caught one, for the fourth time in the programme

```
[FAIL] naught.layout=flow keeps the METER's dots (they answer to `meter`)
```

The check asserted `ON in fl_meter` — **the right answer for the wrong reason.** Its claim is *"the meter
keeps its dots"*, not *"the meter keeps `NA.ON`"*, and it was spelling the cell instead of asking the
seat. It reads `Kit.quantity_glyphs()` now and is true of whatever this language fills with. **This is the
first edit `verify_language.py` has taken in the programme**, and it is a strengthening: the file that
caught the defect is the file whose claim was under-specified.

It also caught a second one that was purely mine: `#46`'s source census reads `language.py` for
half-cell fills, and my new docstring **spelled one as a prose example**, which is indistinguishable
from a sixth seat. The example is gone and the reason is in the docstring.

---

## 8. The census went 26 → 35, and the nine are the surface, not a regression

```
language      before(inc66)   after(inc67)   what the delta is
naught             4              4          (∙, ◦, ⋅, ● already collided)
corgi              2              5          ▄ warn×meter+slider+bar · ▁ info×slider+bar · ░ invalid×meter.track+spark.floor+scrollbar
instrument         4              4
swiss              3              5          ─ warn×meter.track+slider+scrollbar · ━ error×meter.fill+spark.peak
industrial         2              2
nord               1              1
darkside           1              1
prism              2              4          ⣀ info×readbar+meter.track · ⣤ warn×readbar[disabled]
ledger             2              2
solari             3              4          ▄ DANGER_FORM×scrollbar.indicator
blueprint          2              3          ╌ warn×scrollbar.main[disabled]  (and ━ gained spark+scrollbar on a row it already had)
--------------------------------------------------------------------------
TOTAL             26             35
homoglyph rows     1              2
```

**Not one of the nine is a kit that got worse.** Every one is a cell that was already spent where it is
spent, in a widget the census had been told not to read. The four fixes SUBTRACTED from the count they
would otherwise have added to — `prism_S3`'s slider and `prism_S1`'s pager would have put `⣿` on the
same row as `LEVELS["error"]` and `DANGER_FORM`, and corgi's `█` would have carried `pane.rule` and
`mascot.pixel` as well as the pager.

**`PANE_RULE` joined `DECLARED_MARKS`, and it is not a quantity widget.** It is there because the round
named corgi's partition in the same breath as its creature, and **a fix nothing measures is a fix that
can silently come back**. It is the same argument inc57 made for `FIELD_LEAD`: a constant the kit
declares and only the drawing reads. It creates no new collision in any of the eleven.

**The homoglyph row is naught's, and it is the same row inc61 closed.** `∙` (danger + error rung) stands
against `·` at `scrollbar.main` — the pager's SHAFT. inc61 retired `·` from naught's controls and *could
not* have moved this one, because the scroll bar was outside set B. **The alphabet is one round pixel at
six charges and the shaft is still spending the retired one.** Left standing as a question for inc68,
which is the K2 increment and is where a homoglyph row belongs.

---

## 9. Frames changed

**Six component frames moved in the `.txt`** (12 artefacts with their `.svg`):

```
naught_S1   the meter's thirteen cells       ∙ 70 -> 57
corgi_S1    the partition, the creature      █ 47 -> 2
corgi_S6    the creature                     █ 18 -> 0
prism_S1    the pager                        ⣿ 28 -> 24
prism_S3    the slider                       ⣿ 11 -> 2
prism_S4    the pager (behind the modal)     ⣿ 18 -> 14
```

**Gallery: 2 of the 22 artefacts** — `board_naught` (the dot meter) and `gallery_corgi` (the component
sheet's slider row and mascot). `board_corgi` did not move and that is checkable: corgi's board layout is
`strip`, one full-width mode surface, so it draws no pane split at all — the partition only exists in the
two-pane composition `screens.s1` builds.

**Skill gallery 30–51:** four of the twenty-two have a source among the six — **32 `prism_S3`,
35 `corgi_S6`, 37 `corgi_S1`, 43 `prism_S4`**. They are not re-installed by this increment;
`export_to_skill.py` runs at the close of the batch, per the batch's own gate list.

---

## 10. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1188 passed, 2 skipped, 4 warnings in 35.77s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**Baseline at `a113385` was `1 failed, 1165 passed`, the same one test.** +23. `test_win_clipboard_roundtrip`
drives the real Windows clipboard through PowerShell (§10.6); it is **environment-coupled, reported, not
counted and not touched**, and `1188 passed` is not a claim about it either way.

```
$ python -X utf8 prototypes/verify_language.py
ALL PASSED                                          (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> …/prototypes/components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py
  --- refusals, by language ---
  naught [] · corgi [] · instrument [] · swiss [] · industrial [] · nord []
  darkside [] · prism [] · ledger [] · solari [] · blueprint []

$ python -X utf8 prototypes/collision_census.py
self-check  1 of the 5 collisions the round found by hand still come back out of the census; 4 are asserted CLOSED and cannot grow back
self-check  the homoglyph roster is exact for all eleven (2 rows, 2 languages)
TOTAL                       35
TOTAL homoglyph rows             2

$ python -X utf8 prototypes/capture_languages.py plain
  22 grids identical across two PROCESSES
  22 captures -> …/prototypes/gallery
  no two boards identical
```

---

## 11. Risks

1. **The roster is sixteen rows long and five of them are L6.** A roster is a record, not a fix, and this
   one is the largest introduced in the programme. The risk is that it reads as "K5 is closed"; it is
   not. K5's *instrument* is closed — the widget is visible to the census and to a law for the first time
   — and its *findings* are sixteen and named.
2. **naught's meter now fills with `◉`, which is also `PART_GLYPHS["knob"][DEFAULT]`** — the slider's
   grip. That is B×B (alphabet, not counted), and the two are different widgets, but a reader who has
   learned `◉` as "the grip" meets a row of them as a percentage. Not measurable from a frame at one
   width; recorded.
3. **`base_pixel` is well defined for a base whose lit cell is one glyph** (block, block2, quadrant,
   braille, shade, half) and less so for the three FONT bases (slab, flap, stencil), where it returns the
   base's terminal RUN — blueprint's is `▀▀`. It is asserted to be DRAWN by `mascot()`, so it is true;
   it is not obviously the only true answer for those three.
4. **`CELL_INK` gained a declared weight**, which is taste under E2 (no font metric in the artefacts).
   `0.22` is ordinal and placed by the kit's own ramp; nothing photometric was measured and the docstring
   already says the eight declared weights are ordinal.

---

## 12. Found by looking, not fixed

* **The pager was never a separate widget.** Three rounds of documents call `corgi_S1` f31 and
  `prism_S1` f31 "the pager", and `screens.s1` draws it with `k.scrollbar(...)` — a component that has
  been in `PART_GLYPHS` since the registry was written. **The declaration existed and the reader was
  told to skip it**; the whole of K5 for that widget was one tuple in one file.
* **inc59 scoped the toggle off the ember and left the slider on it**, in an increment whose ruling is
  *"a control is read from the TOP"* — and `COMPONENT_PARTS` says in as many words that a switch IS a
  slider whose range is boolean. The registry had already stated the fact that made the omission an
  inconsistency; nothing read the registry against the declaration.
* **corgi's partition was `█` because its BASE cannot draw.** `Corgi.MASCOT_PIXEL` and `PANE_RULE` are
  two different seats with the same cause: the kit's `segment` base is a digit base, so anything
  pictorial falls back to `block`, whose pixel is the error rung. **The fallback was chosen for
  legibility and nobody asked what cell it landed on.**
* **A law's blast radius is three times its brief.** The fill law fires on 22 rows in six languages; the
  round named four frames in three. The difference is L6 (five rows), solari's pager and blueprint's,
  and it is on a roster rather than fixed because those are named objections with their own owners.
* **The suite's teeth constants are a coupling nobody had exercised.** Widening `KNOB_SEATS` by one entry
  moved three cumulative teeth tests in three different increments' sections, and each was a SHARED
  `knob` table showing at two components. That is the widening working, and it is also the sharpest
  argument for why those constants are constants.
* **`test_win_clipboard_roundtrip` was RED in the baseline at `a113385` and in this increment's run.**
  Reported, not counted, not touched.

---

## 13. Pending — not this increment

* **K2** — the derived homoglyph table, and naught's `scrollbar.main` row this increment revealed
  (**inc68**).
* **K4** — a per-part state law (**inc68**).
* **L2** — swiss's disabled `Save` (**inc69**).
* **`mut` contrast** in five kits (**inc70**).
* **L6, L7, L10, C5–C10, E2, E3, G2** — untouched.

## 14. Suggested next task

**inc68**, as briefed: replace the fixed five-pair `HOMOGLYPHS` with a derived table plus the named four,
re-run `homoglyph_rows()`, fix the rows inside languages already reworked (naught's pager shaft is one of
them, and it is the row this increment put on the board), and add K4's per-part state law with teeth on
one real table.

---

## Evidence checklist

- [x] **Tests / type checks / lint pass** — `pytest -q` **1188 passed**, 1 failed
  (`test_win_clipboard_roundtrip`, environment-coupled, red in the baseline too, named in §10).
  `verify_language.py` **ALL PASSED, exit 0**. `render.py` 66/330/0. `matrix.py` refusals `[]` × 11.
  `collision_census.py` both self-checks green.
- [x] **No secrets in code or output** — no credential, token or path outside the worktree is written or
  printed; the only new I/O is `prototypes/out/collision_census.txt`, which the census already wrote.
- [x] **No destructive commands run without approval** — no `rm`, no force push, no rename; every write
  is a tracked file in this worktree.
- [x] **File count within cap** — **5 source files**, the cap exactly:
  `taskboard/language.py`, `taskboard/naught.py`, `prototypes/collision_census.py`,
  `prototypes/verify_language.py`, `tests/test_components.py`. Regenerated artefacts (12 component,
  4 gallery, 1 census table) are outputs of the gates, not hand edits.
- [x] **Review packet attached** — this file.

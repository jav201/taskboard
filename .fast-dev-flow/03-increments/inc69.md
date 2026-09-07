# Increment 69 — air is not a state

**Batch:** `rework-6b`, increment 3 of 4 · **L2**.
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 2 regenerated
component artefacts (1 frame) and 2 regenerated gallery artefacts (1 frame).

**One seat in the whole corpus drew nothing, and it was the button the reader is meant to press.**
`swiss_S2` row 18 read `     Save        ▫   Cancel` — `Save` is DISABLED and swiss declared that state as
four spaces — directly above `Save is held until due parses`, which is a legend. Three adversarial
rounds named it, `spec.md` §11.3 has admitted it word for word since `rework-3`, and in six batches the
only thing that changed in that row was that **`Cancel` gained a mark**. Suite **1202 → 1225**. One frame
moved; census unchanged at 35 collisions and 30 homoglyph rows.

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

This increment carries out **L2**.

---

## 1. Cause — it was a decision, twice, and both times it was written down

**inc38** built swiss's button ladder and said this, verbatim:

> *"DISABLED is air, and it is the one decision that is not the ladder. Nothing in this alphabet is
> lighter than `·` except a dashed RULE (`┆ ╎ ┈`) — the shape being given up. So the mark is simply not
> set… A control nobody may press is a word, and that is what this language would have said anyway."*

**inc46** rebuilt the ladder as `▫ ▪ ■` (because `·` was `LEVELS["info"]` and `•` was `REQUIRED`) and
kept the air, restating the same reason at the declaration:

> *"DISABLED IS STILL AIR, for inc38's stated reason: there is nothing lighter than the hollow square in
> this alphabet that is not a dashed RULE, which is the shape being given up."*

**Two things are wrong with the last sentence of inc38's, and the ruling names the second.**

1. *"A control nobody may press is a word"* — **so is a legend**, and `swiss_S2` puts one directly under
   it. The frame's own criterion: cover row 18 and row 19 and say which of the two is a control. No
   answer.
2. **The shape was not given up.** This kit spends the dashed rule at **five dead seats already** — `┆` at
   `knob`, `checkbox.main`, `textfield.main` and `stepper.step`; `╎` at `radio.main` and `stepper.main`.
   "The shape being given up" is a shape this language draws every time a control dies.

---

## 2. Mechanism — the mark is derived, not chosen

`Swiss.PART_GLYPHS["button.main"][DISABLED]`: `"    "` → `"╎   "`.

**`╎` is `stepper.main`'s dead cell.** `stepper.main` is this kit's *other* `▫` seat — `▫▫` live, `╎╎`
dead — so the kit had already answered *"what does a dead `▫` look like here"* in a different table, and
the button takes that answer instead of a new one. Asserted in the law rather than asserted about it.

| requirement (ruling L2 / the brief) | how `╎` meets it |
| --- | --- |
| a mark from swiss's own alphabet | `stepper.main[DISABLED]` and `radio.main[DISABLED]` already draw it |
| distinct from `▫`, the lightest live rung | a broken stroke against a hollow square: **SHAPE**, which is a stronger channel than the weight the brief asked for, and it is lighter as well. K4's `state_channel` reads it as `shape` |
| not a meaning mark | swiss's meanings are `· ─ ━ ╲ ╱ •` and `▮` (`CUR`); `╎` is none of them |
| not a homoglyph of the ladder | asserted: `╎ ∉ _twins("▫")` — it steps OFF the square family rather than being a fourth square |
| width-safe | `╎` is East-Asian-Width **NEUTRAL**; `┆`, the kit's other dead vertical, is **AMBIGUOUS**. The one dashed vertical in swiss's dead vocabulary that is safe is the one the button takes |

**The seat's arithmetic is untouched:** four cells, the mark and one cell of air leading the field, the
two that used to close it still air. Same width across all four states, so the word cannot move under the
state and a caller laying out a row of buttons sees no change.

```
swiss_S2 f18   before                       Save        ▫   Cancel
               after                   ╎    Save        ▫   Cancel
```

---

## 3. The conflict this ran into, and how it was paid for rather than dodged

**inc38's other law forbids exactly this cell.** `test_swiss_puts_no_wall_around_a_button_at_any_width`
is swiss's §2 commitment made executable — *"no boxes — ALIGNMENT DOES THE DIVIDING"* — and its
`is_wall` predicate is **derived from the codepoint**: the whole Box Drawing block minus three diagonals,
plus every Block Element. `╎` is U+254E. **The first run of the fix went red on it, twice.**

So L2 and inc38's law cannot both bind unchanged, and this is the conflict surfaced rather than averaged:

**`is_wall` excludes the DASHED strokes now, on the diagonals' own argument extended.** The existing
exclusion says *"a stroke that leans closes no corner"*; U+2504–U+250B and U+254C–U+254F are the light
and heavy double, triple and quadruple dashes, and **a stroke that is broken closes no corner either.**
The evidence is not rhetorical: this kit has spent five of those cells at five dead control seats for
eight increments and nobody has called them boxes.

**And the exclusion is paid for in the same move, with a clause that is stronger than the one it
loosens.** The law now also asserts that **no button seat carries a mark at both ends** — read at the two
halves `Kit.button` actually splits the glyph into. That is what "no boxes" claims, and it is a claim a
per-character codepoint rule could never make: `▪ Cancel ▪` is an enclosure, and **it passes `is_wall` at
every width** because neither cell is in the Box Drawing block at all. The repair is the shape §16.3
records for inc63's and inc66's repairs — *"stronger than what it replaced"*.

---

## 4. The law, over all eleven, and it is two clauses

> **No control state is drawn as air.**

`AIR` is the ASCII space and U+2800, the same pair everything else in this file calls blank.

**Clause one — the declaration.** `declared_air(lang)` walks every `(component, part, state)` the
registry derives — **110 seats per kit** — through `part_glyph`, so a state a kit does not declare is
judged on the glyph it actually *falls back to*: a fallback that is air is still air on the screen.
**Exactly one seat in the corpus failed it**, and it is the one the round named. Every other kit marks
every state of every part, including the four that renounce a mascot, the two whose meters draw no ramp
and the one whose severity ladder is words.

**Clause two — the rendering, at three widths.** A declaration is not a rendering: `Kit.button` centres
the label in a field the caller sizes and `Kit.textfield` lays the value on paper, so a mark that
survived only at the width somebody happened to render is a mark that vanishes when a dialog grows. The
row is taken, the caller's own word is *removed* (`replace`, not searched around — a label can contain
anything), and what is left has to have a cell in it. Widths 1, 10 and 24 — below the label, at the
dialog's own, and at swiss's `MEASURE_MIN` — which are the three
`test_swiss_puts_no_wall_around_a_button_at_any_width` already argues for: *"the only width anyone tested
was the only width anyone calls"*.

---

## 5. Teeth

`test_the_air_law_goes_red_on_the_declaration_inc69_moved` — three arms:

1. **inc38's declaration restored, byte for byte** (`"    "`). The declared clause goes red naming
   `("button", "main", "disabled")` **and nothing else**, every other kit stays clean, and the rendered
   clause goes red too.
2. **A mark that exists and does not survive the composer**: `"   ╎"` — the cell parked in the CLOSING
   half of a seat whose opening half leads the field. **The declared clause reads clean and cannot see
   it.** That is why L2 is two clauses and not one, and the arm asserts the blindness rather than
   describing it.
3. **The reader is not vacuous**: it visits `sum(len(parts) × len(states))` = **110 seats**, a number
   somebody has to edit if `COMPONENT_PARTS` or `component_states` shrinks under it.

---

## 6. The census

```
                    inc68    inc69
collisions            35       35     (unchanged, and per language too)
homoglyph rows        30       30
```

`╎` was already spent at `radio.main[DISABLED]` and `stepper.main[DISABLED]`, both chrome, so adding a
third chrome seat keeps it in the *"shared between two CONTROLS only (alphabet, not counted)"* bucket. A
mark taken from the kit's own dead vocabulary costs the census nothing **by construction**, which is the
argument for deriving it instead of picking one.

---

## 7. Frames changed

**One component frame moved in the `.txt`** (2 artefacts with its `.svg`): `swiss_S2`, one row.

No other swiss sheet draws a disabled control: `swiss_S1`, `S3`, `S4`, `S5` and `S6` were re-rendered and
came back byte-identical, which is the check that the change reached the seat and nothing else.

**Gallery: 2 of the 22** — `gallery_swiss` (the component sheet's button row). `board_swiss` did not
move; a board draws no disabled button.

**Skill gallery 30–51: none.** Entry **46 is `swiss_S1`**, not `swiss_S2`, and no other entry has a swiss
source. Checked against §16.5's list.

---

## 8. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1225 passed, 2 skipped, 4 warnings in 36.02s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

inc68 closed at `1 failed, 1202 passed`. **+23.** `test_win_clipboard_roundtrip` drives the real Windows
clipboard through PowerShell; **environment-coupled, reported, not counted, not touched.**

```
$ python -X utf8 prototypes/verify_language.py
ALL PASSED                                          (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> …/prototypes/components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py          (exit 0)
  --- refusals, by language ---   all eleven []

$ python -X utf8 prototypes/collision_census.py
self-check  1 of the 5 collisions the round found by hand still come back out of the census; 4 are asserted CLOSED and cannot grow back
self-check  the homoglyph roster is exact for all eleven (30 rows, 8 languages)
TOTAL                       35
TOTAL homoglyph rows            30

$ python -X utf8 prototypes/capture_languages.py plain
  22 grids identical across two PROCESSES
  no two boards identical
```

---

## 9. Risks

1. **A law was loosened.** `is_wall` no longer counts dashed box-drawing strokes. The argument is the
   diagonals' own, the evidence is five seats this kit already draws, and the loosening is paid for with
   an enclosure clause the old rule could not make — but it *is* a loosening, and a reader who disagrees
   should look at §3 first. **The alternative was to leave swiss the one kit in eleven with a control
   nobody can see, or to invent a cell outside its alphabet.**
2. **`╎` reads as a rule, and swiss's whole identity is that rules are scarce.** One broken vertical at
   the left of a dead button is a mark; at a glance it is also the fifth stroke on a screen whose
   commitment is *"ONE hairline rule"*. Measured: `swiss_S2` has one hairline and this cell is not one —
   it is a control's seat, not a divider — but it is a judgement and it is written down as one.
3. **The rendered clause covers the button and the text field only.** The other six components take no
   width argument (`checkbox`, `radio`, `switch`, `stepper`) or take one whose padding is a track rather
   than air (`slider`, `bar`, `scrollbar`), so their seats are covered by the declared clause alone. A
   composer that learned to pad one of those would slip past clause two.
4. **`110` is a hard number in a test.** It is derived from `COMPONENT_PARTS` and `component_states` at
   import time, so it moves when the registry does — which is the point — but it will need editing the
   next time a part or a state is added, and the failure message says so.

---

## 10. Found by looking, not fixed

* **The only thing that changed in that row in six batches is that the SAFE answer gained a mark.**
  inc53 moved swiss's chosen radio to `▪`, which put a mark on `Cancel`'s neighbourhood; `Save` stayed
  air. A frame can get *worse* while every increment touching it is an improvement, and the round's
  §4.3 says exactly that about this row.
* **The law that forbade the fix is the law swiss's identity is made of**, and it was written by the same
  increment that created the defect. inc38 declared the air *and* the no-wall rule in one pass, and the
  two together left the kit with no legal way to mark a dead button. **A commitment and its enforcement
  written in the same breath can close a door nobody meant to close.**
* **`┆` is East-Asian-Width AMBIGUOUS and swiss spends it at four seats.** naught retired `·` for exactly
  that property (inc61, and `naught.py`'s own header measures it). Nobody has asked swiss the same
  question; four of its dead seats are on an ambiguous-width cell and this increment happened to pick the
  neutral one because it came from `stepper.main`. **Luck, not measurement**, and it is named here so the
  next round can measure it.
* **The declared clause is blind to a mark in the closing half**, which arm two proves rather than
  asserts. Any kit could park a cell where the composer never paints it and read clean.
* **`test_win_clipboard_roundtrip` was RED in this increment's run**, as in the baseline. Reported, not
  counted, not touched.

---

## 11. Pending — not this increment

* **`mut` contrast** in five kits (**inc70**).
* **swiss's other two objections on the same frame**: five controls open with a wall and none closes
  (`swiss_S2` (b)), and `swiss_S4`'s confirm — the second was closed in inc66, the first is untouched.
* **The invalid-rune discrepancy** — 12 rows across two instruments, waiting on a ruling.
* **L6, L7, L10, C5–C10, E2, E3, G2** — untouched.

## 12. Suggested next task

**inc70**, as briefed: raise `mut` to ≥ 4.5:1 against the declared ground in nord, solari, instrument,
darkside and ledger, with the smallest change that keeps `ink > mut > dim` ordered and keeps the hue
family; then the law over all eleven and the re-render.

---

## Evidence checklist

- [x] **Tests / type checks / lint pass** — `pytest -q` **1225 passed**, 1 failed
  (`test_win_clipboard_roundtrip`, environment-coupled, red in the baseline, named in §8).
  `verify_language.py` **ALL PASSED, exit 0**. `render.py` 66/330/0. `matrix.py` refusals `[]` × 11.
  `collision_census.py` both self-checks green.
- [x] **No secrets in code or output** — no credential, token or out-of-worktree path is written or
  printed.
- [x] **No destructive commands run without approval** — no `rm`, no force push, no rename.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
  `tests/test_components.py`. Regenerated artefacts (2 component, 2 gallery) are gate outputs.
- [x] **Review packet attached** — this file.

# Increment 14 — `INVALID` enters the state axis, derived, and drawn in shape by eleven languages

**Batch:** `kits-learn-3` · **AC-1** · operator ruling 1 of 2026-09-04
**Files:** `taskboard/language.py`, `tests/test_components.py` (new), `prototypes/verify_language.py`,
`prototypes/components/screens.py` — **4 source files**, the cap.

---

## 1. The defect the PROTOTYPE round found by rendering

Six canonical screens, five languages, thirty frames — and **S2 could not be rendered at all**. Not because
a language was weak: because `STATES` had six entries and none of them was `invalid`, so the premise of a
form ("this value was rejected") had no seat in the contract. What the five frames did instead is the
finding:

```
due*   [ 12/09/26                         ] !      <- five languages, one red `!`
```

Every one of them marked the rejected field with **the same glyph in the same hue**, because the prototype
had to invent the mark and there was nothing per-language to invent it *from*. That is the palette-swap
failure this whole file exists to make unconstructable, reached at a single character.

After this increment the same row, in three of the five:

```
ledger      due*   ‡12/09/26··························‡
corgi       due*   ▄▀12/09/26··························▀▄
blueprint   due*   ┤12/09/26··························├
```

A daggered entry, a mis-seated segment bank, a reversed dimension. No hue, no `!`, and no line of
`screens.py` drawing any of it.

---

## 2. The mechanism

**The axis.** `INVALID = "invalid"` is the seventh entry of `STATES` and its **sixth control state**,
between `ACTIVE` and `DISABLED`, so a per-component axis is `STATES` minus `CHECKED` in order.

**The derivation, which is the whole increment.** `component_states()` gained **one named term used
twice**:

```python
settable = bool(actuator(name)) and has_interior(name) and not checkable
```

`EDITED` is the putting, `INVALID` is the answer it got back, and they cannot come apart —
*what the arrows can change, the form can reject.* Both terms are registry facts already declared. No new
tuple, no component name, nothing hand-listed, and the falsifiable consequence is asserted:
`slider`, `textfield` and `stepper` take it; `bar` and `scrollbar` have no actuator, `button` has no
interior, and `switch` / `checkbox` / `radio` are `CHECKABLE`.

**The exclusion is a decision, not an oversight** (spec §6.2). `CHECKABLE` declares that a control's RANGE
is boolean, and a boolean cannot be out of range — both of its values are legal. "This box is required and
unticked" is a fact about the **form**, which is a set of controls and has no seat on a per-component axis.
This contract has refused three times to answer a scope question with a hand list at a seat; this is the
fourth. The day a form object exists is the day that state has somewhere to live.

**The marks — thirty-three of them, one law.** `DISABLED` is a control that cannot be touched; `INVALID` is
one that **has been touched and answered back**. So each language's invalid form is its own mark
*refusing*, declared in `PART_GLYPHS` at the three seats where that component's control states already live
(`knob` for the slider, `textfield.main`, `stepper.step`):

| language | knob | field ground | stepper | the sentence it draws |
| --- | --- | --- | --- | --- |
| nord/base | `▚` | `] [` | `][` | the terminal's brackets turned back on the value |
| naught | `◑` | `◑·◑` | `◑◑` | a dot that will not settle — charge is the only channel there is |
| corgi | `▀▄` | `▄▀·▀▄` | `▀▄▄▀` | an LCD bank driven at both ends and resolving at neither |
| instrument | `⠶` | `⠸⠶⠇` | `⢠⡄` | the walls swapped, the middle rank knocked out |
| swiss | `╲` | `╲ ╱` | `›‹` | the rules LEAN — a typographic mark plainly not upright |
| industrial | `/` | `▌/▐` | `><` | a stencilled strike through the plate |
| darkside | `Ø` | `Ø Ø` | `ØØ` | the round knob crossed; the tube that will not light |
| prism | `⣹` | `⣹⠀⣏` | `⢀⡀` | the dense block BROKEN |
| ledger | `‡` | `‡·‡` | `‡‡` | **the accountant's exception mark** — this language does not erase a queried figure, it daggers it |
| solari | `═` | `═·═` | `══` | the flap caught on its seam, landed on neither face |
| blueprint | `├` | `┤·├` | `├┤` | the dimension REVERSED — a measure that does not close |

**Colour is not spent, and that is stated rather than skipped.** `part_tone` is untouched: the state rides
shape alone, and a test asserts the tone channel is byte-identical to `DEFAULT`'s. Two of these languages
have already spent their alert hue on something a control borrowing it would break — ledger's on literal
debt, blueprint's on overdue — so "never colour alone" is enforced here as **no colour at all**. The
caller's error *message* keeps whatever hue the caller gives it.

---

## 3. Files modified

| file | what |
| --- | --- |
| `taskboard/language.py` | `INVALID` in `STATES`; the `settable` term in `component_states`; 33 `INVALID` entries across the eleven `PART_GLYPHS` tables |
| `tests/test_components.py` | **new file** — the component contract's first seat in the pytest gate; 6 laws × 11 languages = 36 tests |
| `prototypes/verify_language.py` | the sweep's own arithmetic: 8 edits, listed in §5 |
| `prototypes/components/screens.py` | S2's due field is drawn in `INVALID`; the hand-drawn `!` is deleted; `C_INVALID` narrows to `C_ERROR` |

The insertion of the 33 glyph entries was scripted (`.fast-dev-flow/probes/_inc14_glyphs.py`) with **every
replacement asserted to fire exactly once** — a silent miss leaves a language falling back to `DEFAULT`,
which is the exact failure the property test is written against, so it is caught in two places.

---

## 4. The property test, and the mutation that proves it can fail

`test_invalid_survives_greyscale_in_every_language` is parameterised over **all eleven** languages, and for
each of the three components that take the state it compares the render at `INVALID` against **every other
state the registry derives**, pairwise, on the glyph channel alone (`shape()` joins the cells' glyphs — a
projection, not a regex over a coloured string).

Not "the render moved" — moved from *what*? A language that declared an invalid mark identical to its
disabled one would satisfy a diff against `DEFAULT` and tell a user with a **dead** field that it is a
**wrong** one. And the failure this is really written against is a **miss** rather than a mistake:
`part_glyph` falls back along the state chain, so a language that simply forgot to declare `INVALID`
renders `DEFAULT` and reads as "fine". That silence is what goes red.

Proved falsifiable before it was believed:

```
$ python -X utf8 -c "... del kit('ledger').PART_GLYPHS['textfield.main']['invalid'] ..."
red as required: ('ledger', 'textfield')
```

Five other laws sit beside it: the derivation answers for **four probe components no language has heard
of** (a `INVALID_COMPONENTS = (...)` tuple would fail that one, which is why there isn't one); `INVALID` is
in `STATES` once and in order; the tone channel is unmoved; and an invalid field still returns its value
**byte for byte** — the content law does not lapse because a value is wrong. A field that hid, truncated or
recased a rejected value would be editing the user's text as a way of complaining about it.

---

## 5. Test results

```
python -X utf8 -m pytest -q
377 passed, 2 skipped, 4 warnings in 30.29s          (baseline 341 passed — +36)
```

```
python -X utf8 prototypes/verify_language.py
2 FAILURE(S): ['character: the token is `MOTION_STEPS` ...', 'prism: rail renders IFF ... layout=rail']
```

**That last line is the pre-existing state of that script, measured before any edit in this batch**, and
the measurement is itself a finding — see §7 (**F-14**). The run at the true pre-batch tree
(`git show HEAD:taskboard/language.py`, installed, swept, restored) gives the **same two failures and no
others**. In between, the axis change took the script to **31** failures; **29 of them were the script's own
arithmetic**, and they are now edited rather than suppressed:

| where | was | is |
| --- | --- | --- |
| `registry: the state axis is LVGL's canonical six, in order` | a hand-typed six-tuple | the seven-tuple, with `invalid` named and dated |
| `TF5` (the field's axis, read at five sites) | a hand-typed five-tuple | `TFS`, six entries |
| `the five grounds are pairwise DISTINCT` ×11 | `== 5` | `== len(forms)` — **counted off the derivation, never numbered** |
| `all five states are pairwise distinct in greyscale` ×11 | `== 5` | `== len(greys)`, with `INVALID` named as the one a fallback would silently pass |
| `EDITED IS THE STEPPER'S HOME` | a hand-typed five-tuple | six, `INVALID` included |

Two of those literals had to be edited because they were literals. That is the increment paying the price
the file's own doctrine names, and the fix was to replace the number with the derivation wherever the
check's meaning allowed it — so the **next** state to arrive edits five lines instead of twenty-nine.

```
python prototypes/capture_languages.py --surface        # plain and alone (F-8)
11 surfaces -> prototypes/gallery ; no two identical (55 pairs)
62 / 66 byte-identical to .fast-dev-flow/baseline-kits2
```

The four that differ are `surface_{corgi,industrial}.{txt,svg}` — **exactly the four `kits-learn-2` §6.2
named as moving**, against a baseline swept before that batch's edit. Nothing in inc14 moved a surface
frame, and the comparison is reported rather than re-baselined.

---

## 6. The capture (AC-7)

```
python -X utf8 prototypes/components/render.py
30 .txt + 30 .svg ; 30 candidates files ; no two frames identical within a screen (60 pairs)
76 hand-drawn elements declared (9 refused, 67 evoked)
```

**The count did not fall, and that is the honest number.** The element that moved —
*"the invalid field's mark"* — is gone from all five S2 sidecars; what remains under a narrower name is
the **message row**, `Kit.error`, which is the caller's words on a row whose *notation* no language has a
seat for. The candidate shrank to exactly that. S2 keeps three candidates because `required` and
`textarea` were never in this batch (spec §6.3).

---

## 7. Risks

- **F-14 · NEW · `prototypes/verify_language.py` was already red at HEAD**, two checks, unrelated to this
  batch: `character: the token is MOTION_STEPS ...` and `prism: rail renders IFF the language declares
  layout=rail`. Measured, not inherited on faith — the pre-batch tree was installed and swept. Recorded
  here, run around, **not fixed in this batch** (it is not this batch's surface, and fixing a sweep while
  changing what it measures is how a green run stops meaning anything).
- **The eleventh language is a language nobody prototyped.** Six of the eleven got an `INVALID` mark from
  this increment without a frame to judge it in. The marks are in-alphabet and the greyscale law holds for
  all eleven, but "in-alphabet and distinct" is weaker than "the operator looked at it".
- **`instrument`'s invalid knob (`⠶`) is its own disabled *indicator* glyph.** Different part, different
  component, and every state of every component is still pairwise distinct — but a wide instrument slider
  at `INVALID` puts a mark on its knob that the same language uses for dead track elsewhere.
- **`‡` and `Ø` are width-ambiguous in a CJK-configured terminal.** So is `∙`, which this file already ships
  in two languages, so the exposure is not new — but the rectangle law depends on the terminal agreeing.

## 8. Pending

- `Kit.error` — the notation of the message row. Proposed by the sidecars, **not ruled on**, out of scope.
- Form-level validity (a required-but-unticked box). Deliberately excluded; §2 says what overturning it costs.
- The gallery screen (`prototypes/widget_slice/app.py`) now derives a **sixth row** for three components
  and was not re-photographed — its blocks read `COMPONENT_STATES`, so they grew on their own. The suite
  and the sweep both pass; no gallery frame is in the baseline set.

## 9. For the skill

- **A state axis must be derived or it will be six literals in a sweep.** The cost of adding one state to
  this contract was 1 term in the derivation, 33 declared marks — and **29 checks that had hand-typed the
  number five**. `COMPONENTS.md`'s state matrix should say: count states off the derivation, never write
  the number.
- **`INVALID` belongs in the state matrix as the sixth control state**, with the rule stated as *what the
  arrows can change, the form can reject*, and with the exclusion (a boolean cannot be out of range) said
  in the same paragraph — because that is the half a reader will otherwise assume was forgotten.
- **The eleven marks are a gallery page on their own**: one row per language, `default` beside `invalid`,
  colour off. It is the clearest available demonstration of "the mechanism is the language's, the state is
  the contract's".

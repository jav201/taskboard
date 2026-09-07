# Increment 57 — the marks a language draws where no instrument can see them

**Batch:** `rework-5b`, closing increment · carries out the four hygiene items the rounds named:
`spec.md` §12.7 (darkside's `(O)` and the `LEVELS` comment), §12.5 / §12.7 (`capture_languages.py`'s
stepper claim) and §13.8 (the eleven `field_row` leaders)
**Files:** `taskboard/language.py`, `prototypes/collision_census.py`,
`prototypes/capture_languages.py`, `prototypes/verify_language.py`, `tests/test_components.py` —
**5 source files**, plus 14 regenerated artefacts, the regenerated census table and this packet.

**Four items, and three of them are the same defect: a language DRAWS a mark that no instrument in this
repo can SEE. `collision_census.py` reads `PART_GLYPHS` and five meaning families; darkside's active
tab and moon doodle and all eleven `field_row` leaders were literals inside methods, so they were
outside it — the limit §10.4 published for `▬`, §12.7 for `(O)` and §13.8 for the leaders. Two declared
constants close it (`Kit.FIELD_LEAD`, `Kit.IDENT_GLYPHS`), the census reads them, and a law asserts the
row draws exactly what the kit declares so the declaration cannot drift away from the drawing. THE
DECLARATION IMMEDIATELY EARNED ITSELF: with the old identity alphabet declared, darkside goes from 1
colliding cell to 3 and the census TOTAL from 33 to 35 — `o` is `LEVELS["warn"]` and `O` is
`LEVELS["error"]`, and both were the moon and the active tab. The moon now waxes through this kit's own
grip (`◎ ◉ ●`). Frames: the six darkside components and `board_darkside`. Suite 1088 → 1100.**

---

## 0. The brief, and what each item became

> **inc57 · hygiene the rounds named.** (a) `Darkside.tabs()` and `wordmark()` print `(O)` (`O` was the
> error rung; `wordmark` is the moon doodle) outside `PART_GLYPHS`: move both to declared cells the
> census reaches (a `PART_GLYPHS["tab"]`/`["wordmark"]` or a declared constant the census reads), keep
> the date-driven doodle but from the new alphabet; (b) `Darkside.LEVELS` comment cites `CUR` as `O`
> (it is `▊` since inc45): fix the comment; (c) `capture_languages.py`'s docstring says the sheet
> renders the stepper and it never has: either add a stepper row to the component sheet at 118×34 (if
> it fits; then 22 gallery frames change and must be re-baked, list them) or fix the docstring, and say
> which and why; (d) `field_row` leaders are drawn outside `PART_GLYPHS` in all eleven so the census
> cannot reach them: declare them (`PART_GLYPHS["field.leader"]` or a constant the census reads) and
> add them to set B; report the census delta and fix any new collision this reveals in a language
> already touched by rework (leave corgi/prism/blueprint/naught findings named for 5c). Frames changed:
> list.

| | what it became | frames |
| --- | --- | --- |
| **(a)** | `Darkside.PHASES` / `TAB_ON` / `TAB_OFF` moved onto this kit's own grip ramp, and `IDENT_GLYPHS` declares them where the census reads them | darkside ×6, `board_darkside` |
| **(b)** | the comment corrected, and it says WHEN it went wrong (inc45) rather than only what is true now | none |
| **(c)** | **the docstring, not the sheet** — with the arithmetic that decided it (§3) | none |
| **(d)** | `Kit.FIELD_LEAD` on all eleven, read by the census as a B-family, held to the drawing by a law over all eleven | none |

**A constant and not a `PART_GLYPHS` slot**, and the choice is worth one line: `PART_GLYPHS` is
addressed through `part_key` / `part_glyph` / `COMPONENT_PARTS` and every state `component_states`
derives, and four laws walk it. A field leader has no states and an identity mark has no control, so
putting them there would have invented a component to hold a mark — and would have handed the opener
law, the named-seat law and the stepper law three seats that are not controls. A declared constant is
the smaller claim, and the census reads it in six lines.

---

## 1. (a) Darkside's identity was spelling its own severity ladder

```python
LEVELS = {"info": "· ", "warn": "o ", "error": "O "}
PHASES = ("( )", "(.)", "(o)", "(O)", "(o)", "(.)")           # the moon
tabs()   -> f"[{accent}](O)[/]..."  if active  else "( )"     # the active tab
```

**The active tab was marked with the ERROR RUNG**, and the moon waxed `. → o → O` through warn and
error. `spec.md` §12.7 found it two batches ago **by reading the source**, which is the method a census
exists to replace: neither `collision_census.py` nor any of the four laws could see either seat,
because both were literals inside methods.

**The new ramp is this kit's own GRIP**, already declared at `PART_GLYPHS["knob"]`:

```python
PHASES = ("( )", "(◎)", "(◉)", "(●)", "(◉)", "(◎)")
TAB_ON, TAB_OFF = "(●)", "( )"
IDENT_GLYPHS = PHASES + (TAB_ON, TAB_OFF)
```

`◎` a ring, `◉` a ring with a filled centre, `●` a disc — **one drawing gaining a stroke and then
filling, which is COUNT and then WEIGHT and never diameter** (ruling D), and a LADDER at monotone
intensities, which **ruling D's addendum** (recorded in `inc55.md` §0) says is ONE declaration rather
than two meanings sharing a shape. The date-driven doodle is kept exactly as it was — `PHASES[day % 6]`
— from the new alphabet.

**AND THE TAB WEARING THE GRIP IS THIS CLASS'S OWN SENTENCE**, not a new idea. Its docstring: *"the ONE
accent (KMBlue) is spent EXCLUSIVELY on interactive affordances — the knob, the switch state, THE
ACTIVE TAB"*. Three things; now one alphabet.

**What `verify_language` had to be told.** One check asserted *"`. o O` stays where it belongs —
darkside's SPINNER and its doodle are motion and identity, never data"*, with `"(o)" in PHASES` as half
its body. **It went red, correctly**, and the fix is not to delete it: the SPINNER keeps `. o O`
(motion is a mark nobody is asked to name), the doodle left it, and the check now asserts both — plus
that every identity cell is one the `knob` table declares. That is the same law with a truer clause.

## 2. (b) A comment two batches out of date

```
- # A DIMMING LADDER MADE OF ITS OWN CURSOR. `CUR` is `O`; …
+ # A DIMMING LADDER, AND IT NO LONGER SHARES A CELL WITH THE CURSOR. This
+ # comment read "a dimming ladder made of its own cursor. `CUR` is `O`",
+ # and that has been FALSE SINCE inc45, which moved `CUR` to `▊` precisely
+ # because the error rung and the cursor were one mark. …
```

**It says when it went wrong, not only what is true now**, because the next reader's question is
whether the ladder was ever meant to be the cursor — and the answer is yes, until a law said otherwise.

## 3. (c) The docstring, and the arithmetic that decided it

`capture_languages.py` claimed the component sheet carries *"slider, bar, switch, checkbox, radio,
button, text field, scroll bar and stepper, each in the states the registry derives"*. Measured, the
`g` screen composes:

```
wordmark    8 rows   cumulative  8       text field   9   cumulative 43
label       1                    9       scroll bar   6              49
rule        1                   10       STEPPER     12              61
mascot      9                   19
checkable   5                   24       #gallery-box shows about 25
radio       5                   29
button      5                   34
```

and `gallery_nord.txt` at 118×34 ends at the checkable block, exactly as `spec.md` §12.5 reported.

**THE DOCSTRING WAS FIXED, NOT THE SHEET, and the reason is that "a stepper row" is not what it would
cost.** The stepper's block begins at row 50 of a body the box shows 25 of. Making it visible means
dropping the identity block and four components — a redesign of the app's `g` screen, in
`prototypes/widget_slice/app.py`, which is not a file this batch touches — and it would re-bake all 22
gallery artefacts for a frame nobody asked to move. **The claim was the defect.** The corrected
paragraph names what the sheet DOES show, names everything below the fold including the stepper, gives
the arithmetic, and records that inc51's stepper law consequently still stands on its property test
alone.

## 4. (d) Eleven field leaders, declared

```
naught      ◦     the unlit pixel, run out right of the figure   (= NA.OFF)
corgi       ""    air -- "no leader, no right column", its own first line
instrument  ⠒     the lattice tick                               (= LATT)
swiss       ""    air -- the figure sits on the second column of the measure
industrial  ""    air -- inc48 took the plate off this row on purpose
darkside    ▔     the rail laid flat (inc53 chose it; inc57 declares it)
prism       ⡀⡤⣶   the ember frontier, ordered
ledger      ·     the dot leader                                 (= LEAD)
solari      ▁     the seam                                       (= SEAM)
blueprint   ·─    the origin dot and the extension               (= LEAD + EXT)
nord        ""    air -- the base's, "a column is found by ALIGNMENT"
```

**EMPTY IS A REAL ANSWER and four languages give it.** It is a commitment with a citation in each kit,
not a hole in the table, and the law asserts it.

**THE LAW KEEPS THE DECLARATION LOAD-BEARING.**
`test_a_field_row_draws_exactly_the_leader_it_declares[lang]`, eleven parametrisations: the cells the
row DRAWS, with the caller's words taken out in all three registers (four kits upper-case the caption,
two lower-case it), are exactly `set(FIELD_LEAD)`. **A constant nothing checks is a comment.**

## 5. The census delta

```
language      inc56   inc57         what moved
naught           5       5          ◦  6 -> 7 families   (+ field.leader)
corgi            5       5          -
instrument       4       4          B x B alphabet 12 -> 14  (⠒ against the controls)
swiss            2       2          -
industrial       2       2          -
nord             1       1          -
darkside         1       1          -   (and see below)
prism            4       4          ⡀  2 -> 3 families   (+ field.leader open)
ledger           2       2          ·  5 -> 6 families   (+ field.leader)
solari           3       3          -
blueprint        4       4          ·  5 -> 6 families   (+ field.leader open)
                                    B x B alphabet 8 -> 9   (─, the extension)
-------------------------------------------------
TOTAL           33      33          homoglyph rows 4 -> 4
```

**TOTAL unchanged, and four rows got wider.** Every cell a leader landed on was already colliding for
another reason, so the leaders revealed no NEW collision — they made four existing rows say one more
true thing. The four are `naught ◦`, `prism ⡀`, `ledger ·`, `blueprint ·`.

**Three of the four are the languages the brief reserves for `5c` and are left named.** The fourth,
`ledger ·`, is a language already touched by rework and **is examined rather than waved past**: `·` is
ledger's `LEAD` — *"the one function this language's whole typographic argument lives in"* — and the
family it joins is `INVALID textfield.main mid`, which is the field's **RUNE**. inc52 §0 excluded the
rune from the invalid law by name and in writing (*"the rune is the PAPER the value lies on in every
state; counting it would have turned 'what a field is made of here' into 'your value is wrong'"*). A
leader and a paper being one cell is that same alphabet, so **no new collision was revealed in a
language already touched by rework, and nothing was moved on this ground.**

### 5a. What the declaration bought, measured on the real declaration

The old identity alphabet put back by hand and the census re-run:

```
$ python -X utf8 prototypes/collision_census.py -o out/_b57_census_old.txt
DARKSIDE   3 colliding cells   (LEVELS · /o /O   DANGER ▚▞  REQUIRED ▪  CUR ▊)
  O   [2 families]  LEVELS[error]  ·  identity.mark mid (declared)
  o   [2 families]  LEVELS[warn]  ·  identity.mark mid (declared)
  ·   [2 families]  LEVELS[info]  ·  textfield.main mid (edited)
TOTAL                       35
```

**33 → 35, and darkside 1 → 3.** The declaration is what makes the defect visible; the move is what
closes it. `(.)` is a FULL STOP and `LEVELS["info"]` is a MIDDLE DOT, so the third rung never collided
— **two of three, said exactly** rather than rounded up.

## 6. Teeth

- **`test_the_census_reaches_every_mark_declared_outside_the_glyph_tables`** carries §5a as its own
  arm: every language's `FIELD_LEAD` cells are asserted present in the census's role map, darkside is
  asserted at exactly one colliding cell, and the old alphabet restored inside the test takes it to
  three with `severity` **and** `identity` named on both.
- **The field law was watched fail by hand on a real drift** — darkside's `field_row` set back to a
  literal while its declaration stayed `▔`:

```
$ python -X utf8 -m pytest tests/test_components.py -q -k "field_row_draws"
FAILED tests/test_components.py::test_a_field_row_draws_exactly_the_leader_it_declares[darkside]
       - AssertionError: ('darkside', {'▁'}, '▔')
```

  **It names the language, what was drawn and what was declared.** The other ten stayed green under the
  same edit, which is what says the law is per-language and not a global assertion in disguise.
- **`verify_language`'s own check went red on the real change** before it was updated, and that is
  reported as a gate event and not hidden:
  `1 FAILURE(S): ["flow: ... and `. o O` stays where it belongs — darkside's SPINNER and its doodle are
  motion and identity, never data"]`. It is the fourth time a `verify_language` law has caught
  something the pytest suite could not (§11.5 records the first two).
- `language.py` was restored from a byte copy (`prototypes/out/_b57_lang.bak`) after both experiments
  and `render.py` re-run.

## 7. Frames changed

```
 M prototypes/components/darkside_S1.{txt,svg}      (O)board -> (●)board
 M prototypes/components/darkside_S2.{txt,svg}
 M prototypes/components/darkside_S3.{txt,svg}      ( )board … (O)cfg -> (●)cfg
 M prototypes/components/darkside_S4.{txt,svg}
 M prototypes/components/darkside_S5.{txt,svg}
 M prototypes/components/darkside_S6.{txt,svg}
 M prototypes/gallery/board_darkside.{txt,svg}      (O)board -> (●)board
```

**Six component frames and one gallery board — and every one of them is ONE ROW, the mode strip's
active tab.** The `field_row` declarations moved no frame at all, which is the honest outcome of a
change that renames where a mark is written and not which mark it is: `test_a_field_row_draws_exactly_
the_leader_it_declares` is the only reason anyone can be sure of that, and it is why it exists.

**Gallery: 1 of the 22** (`board_darkside`). **`gallery_darkside` did NOT move, and the reason is the
calendar trap of §10.3**: today is day 6, `6 % 6 = 0`, and `PHASES[0]` is `"( )"` in the old alphabet
and in the new one alike. **On any other day of the month it would have moved**, and this is E3 being
live rather than closed.

**Of the eight gallery frames installed in the skill, ONE changed byte-wise:
`49_darkside-modal-rounded-lid`, whose source is `darkside_S4`** — the tab row. It was already stale
from `rework-5a` (`inc54.md`/§13.6: the danger form and the six field leaders) and is now stale in a
third place. `export_to_skill.py` does not touch `assets/gallery/`, so it stays stale until somebody
re-installs it by hand or teaches the exporter that directory. The other seven are byte-identical to
their sources.

## 8. Risks

- **`(●)` is one cell away from `{●}`**, this kit's `checkbox.knob[active]`, and `( )` IS
  `checkbox.main[default]`. That is B×B — an alphabet, which the census counts and does not list, and
  which this file's own boundary decision calls *"how a language reads as one language"*. It is a real
  reading risk on a row where a tab strip sits above a form, and it is the price of taking the identity
  marks out of the severity ladder. The alternative was a mark this kit does not declare, which is the
  move inc49 refused on ruling D's ground.
- **`Darkside.SPIN` is still `(".", "o", "O", "o")`** — the same two severity rungs, in the motion
  family, drawn outside `PART_GLYPHS` and now outside `IDENT_GLYPHS` too. **Not fixed and not
  declared**: no kit's `SPIN` is censused, censusing one language's would be arbitrary, and
  `verify_language` holds a law that says the spinner is where that family belongs. **Named in §9.**
- **`FIELD_LEAD` is a set of cells, not a composition.** Two languages build their row from other
  declarations (`ledger` from `LEAD` through `_leadered`, `blueprint` from `LEAD + EXT`), so their
  `FIELD_LEAD` is an alias with the source named in a comment. If one of those constants moves and
  `FIELD_LEAD` does not, the LAW catches it — that is exactly the drift arm — but the comment is what
  tells the next editor where to look.
- **`capture_languages.py`'s corrected docstring describes a viewport at ONE size.** It is true at
  118×34 and would be wrong at a taller one; it says 118×34 in the first line for that reason.

## 9. Found by looking, not fixed

- **`Darkside.SPIN = (".", "o", "O", "o")` is the same collision one family over.** The spinner's `o`
  and `O` are `LEVELS["warn"]` and `LEVELS["error"]`. It is defensible — a spinner is motion and nobody
  reads a rung off a turning cell — and it is a decision nobody has made in writing. **The instrument
  cannot see it: no language's `SPIN` is in the census.**
- **`gallery_darkside` did not move because of the date** (§7), which is E3 alive. A change that moves
  a cell of `PHASES` is invisible on 6 days in 30 and visible on the rest.
- **The census's B×B counts are where the field leaders actually showed up**: instrument 12 → 14,
  blueprint 8 → 9. Those two numbers are printed per language precisely so the B×B boundary stays
  reversible, and this is the first increment where they moved for a reason other than a control.
- **`prototypes/widget_slice/app.py` is where the component sheet's contents are decided**, and no
  batch in this worktree has ever edited it. The stepper is composed there and photographed nowhere,
  which is (c)'s real shape: the sweep is honest and the sheet is a screen designed for a scroll.
- **`test_win_clipboard_roundtrip` was RED in both full-suite runs of this increment** and green in
  inc55's. Environment-coupled (spec §10.6, §13.8). **Reported, not counted, not touched.**

## 10. Gates, verbatim

```
$ python -X utf8 -m pytest -q                                              exit 1
1 failed, 1099 passed, 2 skipped, 4 warnings in 42.10s     (inc56 left 1088)
FAILED tests/test_app.py::test_win_clipboard_roundtrip
       - AssertionError: assert None == 'roundtrip 123 ABC taskboard'

$ python -X utf8 prototypes/verify_language.py                             exit 0
ALL PASSED                                                 (10859 checks)
  ... and it was RED first, on the `. o O` check, until that law was told
      where the doodle went (§6)

$ python -X utf8 prototypes/components/render.py                           exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                           exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                           exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 1 of the 22 moved  (board_darkside)

$ python -X utf8 prototypes/collision_census.py                            exit 0
  TOTAL  33 -> 33      zero collisions: NONE
  TOTAL homoglyph rows  4 -> 4
  (with the old identity alphabet declared: TOTAL 35, darkside 3 -- §5a)
```

**`1088 → 1100`:** eleven field-leader parametrisations and the census-reader law. The one red is the
clipboard test.

## 11. Pending — not this increment

- **The three languages that have never had an increment** (decision A) — corgi, prism, blueprint —
  and the four census rows §5 leaves named for `5c`.
- **`Darkside.SPIN`** (§9), and every other language's `SPIN`, `mascot()` and `wordmark()` marks: the
  same blind spot one family over.
- **A component sheet tall enough to photograph the stepper** (§3).
- **K2**, **K4**, **L1–L6**, **C2**, **C4**–**C7**, **E2**, **E3** untouched.

## 12. Suggested next task

**Close the batch: `spec.md` §14 `rework-5b`, then `export_to_skill.py` and push.**

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1099 passed, 2 skipped, 1 failed`; the
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      reported, not counted, not touched. `verify_language.py` ALL PASSED exit 0 **after** its `. o O`
      law was updated, and its red is reported in §6 and §10 rather than skipped. `render.py` 66/330/0.
      `matrix.py` 66 of 66, refusals `[]`. `capture_languages.py` 22 captures, 1 moved.
      `collision_census.py` both self-checks green, 33 → 33, homoglyphs 4 → 4.
- [x] **No secrets in code or output** — two kit constants, eleven declarations, three method bodies
      reading them, one census pass, two docstrings, one `verify_language` check and two tests. No
      network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. Both watch-it-fail experiments used a
      byte copy of `language.py` (`prototypes/out/_b57_lang.bak`) and restored from it; `git status`
      confirms the tree.
- [x] **File count within cap** — **5**: `taskboard/language.py`, `prototypes/collision_census.py`,
      `prototypes/capture_languages.py`, `prototypes/verify_language.py`, `tests/test_components.py`.
      `verify_language.py` was NOT planned and is in because its own law went red on the real change —
      named here rather than folded in quietly. The 14 frame artefacts and the census table are written
      by `render.py`, `capture_languages.py` and `collision_census.py`.
- [x] **Review packet attached** — this document.

# Increment 60 — blueprint's terminators are chrome and nothing else

**Batch:** `rework-5c`, increment 3 of 5 · decision **A** for the last of the three languages that had
never had an increment
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 8 regenerated
component artefacts, 2 regenerated gallery artefacts, the regenerated census table and this packet.

**`blueprint_S2` is the oldest finding still open in this worktree — `PROTOTYPE-inheritors.md` §9.4's
"`├` is `REQUIRED` and the dimension's opening terminator", carried unresolved through four batches. The
frame says it twice: `title├` and `due├` stand eleven rows above `├ ┤ api`, `├╪┤ ui` and
`├   Cancel   ┤`. blueprint's defect is not one language reaching for chrome — it is obligation standing
ON the chrome and severity standing UNDER it, so the fix moves in both directions. Two MEANINGS moved
and six glyph tables with them: `REQUIRED` left the terminator for a doubled RUN, `LEVELS["info"]`
DROPPED ITS MARK ENTIRELY (the brief asked which meaning is dropped and why — this is the answer, by
name), every dead run left the warn rung, and the refusal stopped borrowing the HELD hatch. opener
12 → 0, named 12 → 0, census 4 → 2, TOTAL 28 → 26. Suite 1103 → 1106. `verify_language` went RED again
and its law wrote half the answer.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **A — the five languages that never had an increment get one each, guided by the laws.** Each
> increment ends with that language's rosters at zero or with every remaining row exempted by name and
> citation.

The brief for this increment, quoted because its last sentence decided the shape of §4:

> `├ ┤` are REQUIRED and every control's terminators; `━` is error and danger (top-rung exemption) and
> the HELD/INVALID hatch `╱` doubles. Blueprint has TEN marks by docstring; find the assignment where
> REQUIRED is not a terminator (or the terminators are not REQUIRED), and where INVALID does not share
> the HELD texture, citing §11. **If ten marks cannot cover it, say which meaning is dropped and why, by
> name.**

## 1. The ruling this increment writes

> **(i) THE TERMINATORS ARE CHROME AND NOTHING ELSE.** `├ ┤` and their weight ramp (`╞ ╡ ┣ ┫ ╎ ╏`) fix
> where a run BEGINS and ENDS, and every control on this sheet is built out of them, so no MEANING may
> be one. `REQUIRED` leaves `├` for a doubled RUN, `═`.
>
> **(ii) A MEANING IS A LINE TYPE, AND A DEAD THING IS NOT A MEANING.** The severity ladder is a
> line-type ramp: **nothing** for info, `╌╌` dashed for warn, `━━` heavy for error. A dead run is the
> same dash at a FINER COUNT — `┈` a dead LEADER, `┄` a dead EXTENT — which is ruling D's first channel
> and already this kit's own answer at `indicator[DISABLED]`.
>
> **(iii) THE HATCH IS ONE MARK AT TWO DIRECTIONS.** `╱` is HELD (LANGUAGES.md §11: *"held work is
> HATCHED, never coloured (`hatch='╱'`)"*, and `Blueprint.icon` says it again: *"HELD is the HATCH
> itself"*). `╲` is REFUSED. A drawing office hatches ADJACENT PARTS IN OPPOSITE DIRECTIONS, so the
> hatch stays ONE mark of the alphabet and spends a channel it has always spent — and DIRECTION is one
> of ruling D's four.

**The kit's own argument for `├` is what (i) overturns, and it is quoted rather than paraphrased:**
*"On a drawing an unfigured dimension is a REFERENCE and a figured one is required; the mark that says
an extent must be given is the terminator that opens it."* The argument does not survive the sheet.
`├` opens **every** dimension here, required or not — the button, the checkbox, the field, the danger
button on `blueprint_S3`. **A mark on every span says nothing about which span must be figured.**

## 2. The dropped meaning, by name — `LEVELS["info"]`

The brief asked for this decision explicitly and here it is with its reasons.

`··` was `LEVELS["info"]` **and** `LEAD`, the leader-origin dot. `LEAD` is this sheet's most-spent
chrome cell: the stepper's ground at five states, the field's paper at three, the switch's track at six,
the scroll bar's shaft, `FIELD_LEAD`, and the rule `·──` under every heading. One of the two had to give
way and there was no third cell — `─` is the extension line, `├ ┤` are the terminators, `━` is spent
twice already, `┌ ┐ └ ┘` are the registration marks.

**The sheet's own commitment decides it:** *"alert is spent on OVERDUE and nothing else. **A calm sheet
carries zero alert.**"* A drawing office does not rule a line to say there is nothing to note. So
blueprint's info rung is AIR, and the ladder starts at nothing: `""` / `╌╌` / `━━`.

**It is a precedent in this corpus and not an invention.** `Ledger.LEVELS` has carried a blank info rung
since inc45 (`{"info": "  ", "warn": "* ", "error": "**"}`), and
`test_blueprint_says_nothing_when_there_is_nothing_to_note` asserts ledger's blank rather than citing it,
so a change to ledger takes this argument's ground away loudly.

## 3. Ten marks could not cover it — the count is TWELVE now, corrected in the docstring

The class docstring said: *"The only box-drawing glyphs this language draws are `─ ━ ├ ┤ ╌` (the
dimension vocabulary), `┌ ┐ └ ┘` (registration marks) and the hatch — **TEN**, and not one of them is a
vertical stroke or a rectangle junction, so a containing box here is not merely absent: it is
**unconstructable**."*

**Two of the twelve are this increment's, and one of them was already being drawn.**

| mark | what it is | why it is affordable |
| --- | --- | --- |
| `═` | `REQUIRED` — a DOUBLED run | a run, not a terminator, so it can never be the mark that opens a control; **no vertical, no junction**, so the unconstructability sentence survives it |
| `┄` | the dead EXTENT | **`indicator[DISABLED]` had drawn it all along** and the count had never noticed. Not a new mark; a mark the docstring had missed |

`┈` (the dead LEADER) is the third dash count and is §4's. The hatch is still **one** mark: `╱` held,
`╲` refused.

**The docstring now reads TWELVE with both additions named and the unconstructability argument
restated.** Correcting a language's own count is cheaper than quietly shipping eleven marks under a
docstring that says ten.

## 4. `verify_language` went RED, for the fifth time in this worktree, and its law wrote half the answer

The first answer sent **every** dead run to `┄`. Four failures:

```
4 FAILURE(S): ['blueprint: the disabled indicator differs in SHAPE from the track. An extent
separated from its range by hue alone is the colour-only defect one cell in — and it is what three
of these languages were shipping',
 'blueprint: the disabled indicator differs in SHAPE from the track — the two-channel law one cell in',
 'blueprint: the checked+disabled indicator differs in SHAPE from the track — the two-channel law one
cell in',
 "... and nord's BOARD is identical either way ..."]
```

The switch's dead TRACK and its dead INDICATOR had collapsed onto one mark. **So there are TWO dead
runs, and the split follows the two LIVE marks they replace:** a dead LEADER (`·`, the mark this drawing
rules every gap with) is `┈`, a dead EXTENT (`─`, the span itself) is `┄` — the ground fades one dash
count further than the thing lying on it. `┈` went to `main[DISABLED]` (the switch's track),
`stepper.main[DISABLED]` (the schedule's ground) and `textfield.main[DISABLED]` (the field's paper);
`┄` to `indicator[DISABLED]` (unchanged), the checkbox's dead datum and the radio's.

**The fourth failure was a cascade** — the nord check went green again with no nord edit — and
`verify_language.py` was **not touched**. The tree was confirmed clean at `c44472a` first (`ALL PASSED`)
so the reds were attributed to this change and not assumed.

## 5. The seven declarations, before and after

| # | what | before | after |
| --- | --- | --- | --- |
| 1 | `REQUIRED` | `├` — the terminator that opens every dimension | `═` — a doubled RUN |
| 2 | `LEVELS` | `·· ╌╌ ━━` | `"" ╌╌ ━━` — **info drops its mark** (§2) |
| 3 | `main` (the switch's track) | `·` / `╌` | `·` / `┈` |
| 4 | `checkbox.knob` DISABLED | `╎╌╎` | `╎┄╎` |
| 5 | `radio.knob` DISABLED | `╏╌╏` | `╏┄╏` |
| 6 | `textfield.main` | INVALID `╱·╱`, DISABLED `╎╌╎`, **EDITED `╞╌╡`** | `╲·╲`, `╎┈╎`, **`╞─╡`** |
| 7 | `stepper.main` DISABLED · `knob`/`stepper.step` INVALID | `╌╌` · `╱`, `╱╱` | `┈┈` · `╲`, `╲╲` |

**The EDITED paper is the one cell no roster asked for and the census did.** It read `╌`,
`LEVELS["warn"]`, so a field somebody was typing into carried a warning under the caret — a live census
row (`╌ [2 families] LEVELS[warn] · textfield.main mid (edited)`) after the dead runs moved. It banks up
to the EXTENSION LINE instead, which is the same move it always made (a leader becoming a continuous
run) said with a mark that means nothing. That took blueprint from 3 rows to 2.

## 6. The rosters and the census

```
                      inc59   inc60          collision census   inc59  inc60
MEANING_AT_AN_OPENER                         naught                 5      5
  blueprint             12       0           corgi                  2      2
  naught                 3       3           instrument             4      4
  the other nine         0       0           swiss                  2      2
                                             industrial             2      2
MEANING_AT_A_NAMED_SEAT                      nord                   1      1
  blueprint             12       0           darkside               1      1
  naught                12      12           prism                  2      2
  the other nine         0       0           ledger                 2      2
                                             solari                 3      3
**TEN of the eleven are clean on both.**     blueprint              4      2
naught is the last, and inc61 is its         ---------------------------------
increment.                                   TOTAL                 28     26
                                             homoglyph rows         4      4
```

**blueprint's two remaining rows, both exempted by name with a citation:**

- **`━` [2 families]** — `LEVELS[error]` × `DANGER_FORM`. `DANGER_IS_THE_TOP_RUNG["blueprint"]`:
  *"`━━` — LEVELS[error]; the HEAVY weight, this alphabet's loudest mark"*. Intact.
- **`·` [5 families]** — `INVALID textfield.main mid` (the **RUNE**) × the field leader and four chrome
  seats. This is the exclusion `inc52.md` §0 wrote by name: *"a field's glyph is wall, RUNE, wall and
  the rune is the PAPER the value lies on in every state"*. It was **6** families before and lost
  `LEVELS[info]`. The identical row exists for corgi (inc58) and ledger (spec §14.4): **the census and
  the test law disagree about the rune and have since inc52**, and this is the third language where
  that disagreement is the only thing left.

`... 1 further cells would collide if slider/bar/scrollbar were in the B set` — was 0. That is
`scrollbar.main[DISABLED]`, still `BREAK` = `╌` = `LEVELS["warn"]`, and it is the declared cost of
leaving the scroll bar out of the B set. Named, not hidden.

## 7. Teeth

**Watched failing BY HAND** (`prototypes/out/_watch60.py`, output at `prototypes/out/watch60.txt`):

```
AS SHIPPED                     opener  0  named  0
+ the five dead-run tables     opener  1  named  8
+ REQUIRED back on the opener  opener  7  named 12
+ LEVELS[info] back on LEAD    opener 12  named 12
  opener law RED on blueprint, 12 seats; first three:
      ('button.main', 'default', '├  ┤', '├')
      ('checkbox.main', 'default', '├ ┤', '├')
      ('checkbox.main', 'checked', '├ ┤', '├')
  named seat law RED on blueprint, 12 seats; first three:
      ('checkbox.knob', 'default', '├╪┤', '├')
      ('checkbox.knob', 'disabled', '╎╌╎', '╌')
      ('checkbox.knob', 'checked', '├╪┤', '├')
  hatch restored: icon(blocked)='[#7fa8c4]╱╱[/]'  invalid channel='╱╱╱╲╲'
      -> HELD and REFUSED share {'╱'}
```

**MY FIRST DRAFT OF THE FIRST NUMBER WAS `(0, 0)` AND IT WAS WRONG**, which is why it is a constant in
the suite (`BLUEPRINT_TABLES_WORTH`) rather than a claim in this packet. I predicted that restoring the
chrome alone would light nothing, because `├` is no longer the obligation mark — true — and because `╌`
is no longer a severity rung — **false**. inc60 left `LEVELS["warn"]` exactly where it was and moved the
DEAD RUNS off it, so putting the dead datums back scores (1, 8) with no meaning restored at all. The
test now asserts the measurement and its docstring says the prediction was wrong.

**Three new tests:**

- `test_both_seat_laws_go_red_on_the_two_meanings_inc60_moved` — the three halves in order (tables,
  `REQUIRED`, `LEVELS`), each with its cumulative count asserted, both laws required to raise at the
  end, and the other ten languages held still on both rosters at every step.
- `test_blueprints_refusal_is_the_held_hatch_turned_the_other_way` — ruling (iii) at both ends, with the
  HELD mark **read off `Blueprint.icon`** rather than off a literal, so a kit that moved its hatch and
  left the invalid channel behind goes red.
- `test_blueprint_says_nothing_when_there_is_nothing_to_note` — ruling (ii)'s dropped mark as a LAW: the
  info rung is blank, the other two are not, **ledger's blank is asserted as the precedent**, `LEAD` is
  still `·` and still the stepper's ground, and `REQUIRED` is neither `OPEN` nor `CLOSE`.

**And one existing test had to be rebuilt, which is the finding worth more than the test.**
`test_the_rune_is_excluded_from_the_invalid_channel_by_name` rode on a LIVE DEFECT: blueprint's rune was
`·` and `LEVELS["info"]` was `··`, so the exclusion could be watched without patching anything. inc60
sent info to air, and **the corpus now has no language left whose rune is a meaning** — measured, all
eleven, and asserted in the rebuilt test. *An exclusion whose teeth depend on a defect being present
dies the day the defect is cured, and it dies GREEN.* The meaning is patched in now.

`INVALID_CHANNEL_BEFORE` (inc52's teeth) gained a fifth field for the same class of reason: its
blueprint-knob arm restores `├` and asks for `("required", "invalid")`, and with obligation moved that
arm **passed for the wrong reason**. It now restores the pre-inc52 `REQUIRED` alongside — the whole
state, rather than a weakened assertion.

## 8. Frames changed

```
blueprint_S2   the form      title├ / due├ -> title═ / due═; the invalid field's hatch turns;
                             the EDITED field's paper banks up to the extension line
blueprint_S3   the settings  the dead switch  ├╎╌  ->  ├╎┈
blueprint_S5   the log       the severity column: the info rung is air
blueprint_S6   the monitor   the controls in the strip
gallery_blueprint.{txt,svg}  the component sheet
```

`blueprint_S1` and `blueprint_S4` did not move. `render.py` 66 frames / 330 pairs / 0 hand-drawn;
`capture_languages.py plain` 22 captures, 22 grids identical across two processes, 1 moved.

## 9. Risks

- **`╌`, `┄` and `┈` are three dashed horizontals told apart by DASH COUNT** (2, 3, 4). Count is ruling
  D's first channel and the census's `HOMOGLYPHS` table lists no box-drawing pair, so no instrument
  objects — but at a 12px cell a reader is being asked to count dashes. Two of the three only ever
  appear on DEAD seats, which is the mitigation: the live sheet carries `╌` and nothing near it.
- **`═` is an eleventh box-drawing mark in a language whose identity is a short alphabet.** The
  unconstructability argument survives it (§3) and the docstring is corrected, but the alphabet grew and
  that is a real cost of this ruling. **The operator may prefer the other branch — drop `REQUIRED`
  entirely and say obligation in TYPE — and the seven declarations are in one table (§5).**
- **A calm blueprint row now carries no severity mark at all** (§2). That is the sheet's stated
  commitment, and it means an `info` row and a row with no severity are indistinguishable — which is
  what "info" means on a drawing and is nonetheless a loss of a distinction the other ten languages keep.
- **`blueprint_S3`'s danger button still opens with `├`** (`├ ━Delete all━ ┤`), and that is now correct
  rather than tolerated: `├` carries no meaning after this increment.

## 10. Found by looking, not fixed

- **`Blueprint.ERROR_FILL = "╌"` is `LEVELS["warn"]` ruling the ERROR row out to the margin.**
  `blueprint_S2` row 6 reads `━━ expected YYYY-MM-DD ╌╌╌╌…` — the error rung leads and the WARN rung
  letters the rest, **two severities on one row**. The kit argues it in writing (*"a REVISION NOTE:
  lettered on a DASHED extension out of the feature that changed, which is what `╌` is for on this sheet
  and what its WARN rung already spells"*) and **no law and no census reaches it** — `ERROR_FILL` is a
  constant outside `PART_GLYPHS`, the same blind spot inc57 closed for `FIELD_LEAD` and `IDENT_GLYPHS`.
  It is under this increment's own ruling and was left alone deliberately: the boundary this increment
  took was "everything the census can see", and taking one more constant would have been taking all of
  them. **This is the sharpest thing inc60 leaves open.**
- **The `·` rune row is the third language with the identical shape** (corgi inc58, ledger §14.4,
  blueprint here). The census counts the rune and `_invalid_marks` excludes it by name. **Three
  languages' last remaining row is one disagreement between two instruments**, and nobody has decided
  which is right.
- **`Blueprint.REG`, the four registration marks, are outside every instrument** — same class as
  `Corgi.PANE_RULE` (inc58 §10). `┌` is `CUR` and the other three are drawn at the sheet's corners; none
  is censused.
- **inc51's `stepper.step[INVALID]` teeth for blueprint (`├┤` restored) still passes for a NEW reason.**
  Its arm is "the terminators exchanged", which is an ORIENTATION defect and independent of what `├`
  means — so it survived obligation moving, unlike the inc52 arm one screen up which did not. Two teeth
  tests over the same declaration, one blind to a meaning move and one not, and only one of them
  noticed.
- **The checkbox's and the radio's terminators still point out and in respectively** (`├ ┤` against
  `┤ ├`), which is the declared orientation channel `HANDED_FIELDS`'s law exempts by name — and with
  `├` no longer a meaning it is now a pure B×B distinction, which is what it always claimed to be.

## 11. Pending — not this increment

- naught (opener 3, named 12, two homoglyph rows, "no unspent cell") and ledger (one homoglyph row) are
  inc61; inc62 closes the batch.
- `Blueprint.ERROR_FILL` and `Blueprint.REG` (§10) — a census widening, not a language rework.
- `49_darkside-modal-rounded-lid` in the skill's `assets/gallery/` is stale for the fourth batch running.

## 12. Suggested next task

**inc61 — naught and ledger.** naught: `◉` is `REQUIRED` at both knobs and `∙`/`·` is a homoglyph row
twice over; naught's doctrine (§0) is CHARGE — how many are lit — so COUNT (one dot against two) is the
channel where it has no cell left, or an exemption by name with the citation. ledger: `·` is the field
leader against its own `·` homoglyph row, and `†` is `REQUIRED` against `‡` invalid.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1106 passed, 2 skipped, 1 failed`
      (inc59 closed at `1103 passed`; +3 is this increment's three new tests). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) — **reported,
      not counted, not touched.** `verify_language.py` **ALL PASSED exit 0 — and it was RED FIRST, four
      checks at once** (§4), reported rather than skipped, with the pre-change tree confirmed green at
      `c44472a` before the reds were attributed. `render.py` 66 frames / 330 pairs / 0 hand-drawn.
      `matrix.py` 66 of 66, refusals `[]` for all eleven. `capture_languages.py plain` 22 captures, 22
      grids identical across two processes, 1 moved. `collision_census.py` both self-checks green,
      TOTAL 28 → 26, homoglyph rows 4.
- [x] **No secrets in code or output** — two kit meanings, six glyph tables, one class docstring, two
      roster entries, one teeth-table field, three new tests and one rebuilt one. No network, no new
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. `git stash` / `git stash pop` was used
      once to confirm the pre-change tree was green under `verify_language`; the tree was verified
      restored afterwards.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`. **`prototypes/verify_language.py` was NOT edited** — its law found a
      real defect and the fix went into the kit.
- [x] **Review packet attached** — this document.

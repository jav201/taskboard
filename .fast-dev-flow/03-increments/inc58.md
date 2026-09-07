# Increment 58 — corgi crosses its own frontier

**Batch:** `rework-5c`, increment 1 of 5 · carries out decision **A** of `PROTOTYPE-inheritors-2.md` §6
for the language that has carried the corpus's widest roster since inc48
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 8 regenerated
component artefacts, 4 regenerated gallery artefacts, the regenerated census table and this packet.

**corgi's segment bank is four cells and all four of them mean something — `▁` info, `▄` warn, `▀`
obligation, `█` error and the danger form — and until this increment the same four cells were also
every control's chrome. 38 opener seats and 16 named seats, the two widest entries either roster has
ever carried. THE EXEMPTION WAS THE FIRST THING TESTED AND IT FAILED ITS OWN CONDITION: an exemption
must leave a control's opener distinct from an error rung IN THE FRAME, and `corgi_S2` drew `██` as
the error message's leader three rows under `██ ON ui`, a CHECKED checkbox, while `corgi_S3` drew `██`
as the slider's KNOB twelve rows above `▁▁█Delete all█▁▁`. So the controls moved instead, under one
sentence this kit had already written and never enforced: THE BANK IS THE READING AND THE PANEL IS THE
METAL. Eleven declarations, opener 38 → 0, named 16 → 0, census 5 → 2, TOTAL 33 → 30. Suite 1099 →
1101.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **A — the five languages that never had an increment get one each, guided by the laws.** Each
> increment ends with that language's rosters at zero or with every remaining row exempted by name and
> citation.

And the brief's own instruction for this increment, quoted because it decided the shape of the work:

> Corgi's commitment (LANGUAGES.md §4) is "the numbers are the keymap" and a segment display; decide
> from the doctrine which meanings keep the ramp and which controls move to the dead/undriven cells
> (`░`, `·`) or to count (two segments), or whether corgi's answer is a by-name exemption for the whole
> ramp as `DANGER_IS_THE_TOP_RUNG` already is: **but an exemption must leave the opener of a control
> distinct from an error rung in the frame, so measure `corgi_S3` and `corgi_S4` before deciding.**

## 1. The exemption, measured first and refused

The brief's condition is a fact about the shipped frames, so it was read off them before anything was
written. Three cells were checked in the frames as they stood at `067400c`:

| cell | what it means | where else it stands, in the SAME frame |
| --- | --- | --- |
| `██` | `LEVELS["error"]` **and** `DANGER_FORM` | `corgi_S2` row 7 `██ expected YYYY-MM-DD` (the error message's own leader) against row 11 `▒▒ -- api  ██ ON ui  ██ ON urgent` — **the CHECKED checkbox, three rows apart** |
| `██` | as above | `corgi_S3` row 16 `row density  ▄▄ ▄▄ ▄▄ ██ ▁▁[70]` — **the slider's KNOB** — against row 20 `▁▁█Delete all█▁▁`, twelve rows down |
| `▁▁` | `LEVELS["info"]` | `corgi_S4` `▔▔ █Delete█ ▔▔   ▁▁  Cancel  ▁▁` — the lowest severity rung **opening the safe answer**, which is `swiss_S3`'s finding verbatim in another alphabet |

**One cell, four readings, one screen.** A blanket exemption for the ramp would have had to say that a
reader meeting `██` on `corgi_S3` can tell the switch's grip from the danger form; the frame says they
are the same two cells. The exemption was refused and the controls moved.

`DANGER_IS_THE_TOP_RUNG["corgi"]` survives untouched — it covers `danger` against `ladder` and nothing
else, and `██` is still `LEVELS["error"]` set as a form around a label.

## 2. The ruling this increment writes

> **THE BANK IS THE READING, THE PANEL IS THE METAL.** corgi owns two ramps and had never said which
> was which. The SEGMENT BANK is glass driven to a HEIGHT — `▁` an eighth, `▄` a half, `▀` the upper
> half, `█` the whole cell — and every one of those four carries a meaning here. The SHADE RAMP
> (`· ░ ▒ ▓`) and the QUADRANTS (`▛▜ ▙▟ ▘▝ ▖▗`) are not bars at all; they are a texture and a corner,
> milled aluminium rather than lit glass. **A control is never drawn as a driven bar, and a meaning is
> never drawn as a texture.**

**It is this kit's own sentence, not a new one.** `Corgi.field_row`'s docstring already names the
frontier — *"the frontier is the two REGISTERS -- engraved aluminium against driven glass"* — and
`Corgi.scrollbar.main` already names the ghost — *"a segment present but NOT DRIVEN"*. What inc58 does
is enforce the frontier on the controls, which had been standing on both sides of it since the kit was
written.

**The knob takes the QUADRANT family and it is the only part that does.** `▛▜` shoulders PROUD (the
reader's key), `▙▟` shoulders SEATED (the grip at rest, the key latched), `▘▝` the upper corners alone
(the key turning), `▖▗` the lower corners alone (the key pressed flush). Four marks on POSITION, which
is one of ruling D's four channels — and it makes inc46's lesson structural: *"a knob drawn like the
fill is not a knob"* is now a fact about the shape family rather than a thing somebody has to remember.

## 3. The eleven declarations, before and after

| # | key | before | after | why |
| --- | --- | --- | --- | --- |
| 1 | `switch.main` | **did not exist** — fell to `main`, `▁▁` / `··` | `▒▒` / `··` | the switch was drawn from the SLIDER's tables, so its off-track was `LEVELS["info"]` |
| 2 | `switch.indicator` | **did not exist** — fell to `indicator`, `▄▄` / `▁▁` | `▓▓` / `··` | its ON-track was `LEVELS["warn"]` and its dead track `LEVELS["info"]` |
| 3 | `knob` | `██ ▀▀ ▓▓ ▒▒ ░░ ╳╳` | `▙▟ ▛▜ ▘▝ ▖▗ ░░ ╳╳` | the grip of every switch and slider was the error rung, and focused it was `REQUIRED` |
| 4 | `checkbox.main` | `▁▁ ▔▔ ▂▂ ··` | `▒▒ ▛▜ ▖▗ ··` | a height ladder whose bottom rung is `LEVELS["info"]` |
| 5 | `checkbox.knob` | `██ ▛▜ ▓▓ ▒▒` | `▓▓ ▙▟ ▘▝ ╳╳` | the CHECK was `LEVELS["error"]`; it is now metal DRIVEN against metal idle |
| 6 | `radio.main` | `▁◦ ▔◦ ▂◦ ·◦` | `▒◦ ▛◦ ▓◦ ·◦` | **cell one only** — the lamp is the choice and was never a bar |
| 7 | `radio.knob` | `▁● ▔● ▂● ·◌` | `▒● ▛● ▓● ·◌` | as above |
| 8 | `button.main` | `▁▁▁▁ ▔▔▔▔ ▄▄▄▄ ····` | `▒▒▒▒ ▛▛▜▜ ▓▓▓▓ ····` | `▁▁  Cancel  ▁▁` opened the safe answer with the info rung |
| 9 | `textfield.main` | `▁▁·▁▁ ▔▔·▔▔ ▔▔▁▔▔ ▄▄·▄▄` | `▒▒·▒▒ ▛▛·▜▜ ▛▛▒▜▜ ▓▓·▓▓` | INVALID `░░·░░` and DISABLED `·····` **unchanged** (inc52) |
| 10 | `stepper.main` | `▁▁▁▁ / ····` | `▒▒▒▒ / ····` | five opener seats in one line |
| 11 | `stepper.step` | `▄▄▄▄ ▀▀▀▀ ▓▓▓▓ ████ ░░░░ ╳╳╳╳` | `▓▓▓▓ ▛▛▜▜ ▘▘▝▝ ▖▖▗▗ ░░░░ ╳╳╳╳` | warn, `REQUIRED` and error on three states of one control |

**INVALID AND DISABLED WERE NOT TOUCHED ANYWHERE.** `░░` is inc52's ghost and `··` / `╳╳` are this
kit's dead marks; every one of them is byte-identical to `067400c`. The increment moves what was on
the bank and nothing else.

## 4. What did NOT move, and the cost is declared rather than absorbed

**`main`, `indicator` and `scrollbar.*` keep the bank.** For the slider and the bar they are a
QUANTITY, and a quantity here is a reading: *"the reading rides on segment HEIGHT, not on
lit-vs-ghost"* is this kit's own twice-cured defect (its comment on `SLOT_SEP`), and moving the fill
onto a shade would re-open it. The switch is hardware and now takes scoped tables, so the base pair is
reached by the slider and the bar alone.

**The cost is that corgi's census count falls partly because the READER LOST REACH, and the census
prints the number itself:**

```
corgi, before   ... 5 further cells shared between two CONTROLS only (alphabet, not counted)
                ... 1 further cells would collide if slider/bar/scrollbar were in the B set
corgi, after    ... 11 further cells shared between two CONTROLS only (alphabet, not counted)
                ... 3 further cells would collide if slider/bar/scrollbar were in the B set   <-- 1 -> 3
```

`▁` and `▄` are still `LEVELS["info"]` and `LEVELS["warn"]` and are still the slider's shaft and fill.
The census excludes slider, bar and scroll bar from its B set **by the operator's own request**
(`collision_census.py` header), so those two cells produce no row — and that is A × B, which spec §11.2
records the rule as PERMITTING (*"those are A×B rows, which the census calls questions and the rule
permits"*). **Named here so the drop from 5 to 2 is not read as five cells moving.** Three of them did;
two of them went where the instrument does not look, and the instrument says so in its own output.

## 5. The rosters and the census

```
                      067400c   inc58
MEANING_AT_AN_OPENER
  corgi                   38       0     <-- the widest entry either roster ever carried
  naught                   3       3
  prism                   25      25
  blueprint               12      12
  the other seven          0       0

MEANING_AT_A_NAMED_SEAT
  corgi                   16       0
  naught                  12      12
  prism                   16      16
  blueprint               12      12
  the other seven          0       0

HANDED_FIELDS       6 languages -> 7    corgi joins (see §7)
```

```
collision census      067400c   inc58
naught                    5        5
corgi                     5        2      <-- `▁` `▄` `▀` rows gone; `█` 5 families -> 2
instrument                4        4
swiss                     2        2
industrial                2        2
nord                      1        1
darkside                  1        1
prism                     4        4
ledger                    2        2
solari                    3        3
blueprint                 4        4
-------------------------------------
TOTAL                    33       30
homoglyph rows            4        4      (naught 2, darkside 1, ledger 1 — unchanged)
```

corgi's two remaining rows, both pre-existing and both named:

- **`█` [2 families]** — `LEVELS[error]` × `DANGER_FORM`. This is `DANGER_IS_THE_TOP_RUNG["corgi"]`,
  *"`██` — LEVELS[error]; the segment driven to full height"*, and the exemption is intact.
- **`·` [7 families]** — `INVALID textfield.main mid` (the RUNE) × the disabled chrome of seven parts.
  This is the exclusion `inc52.md` §0 wrote by name: *"a field's glyph is wall, RUNE, wall and the rune
  is the PAPER the value lies on in every state"*. `tests/test_components.py::_invalid_marks` excludes
  it; the census does not, and spec §14.4 records the same row for ledger. Unchanged by this increment.

## 6. Teeth

**Watched failing BY HAND on the real declarations, one at a time** (`prototypes/out/_watch58.py`,
output at `prototypes/out/watch58.txt`), which is what turns "the roster is 0" into "the roster is 0
and here is what each of the eleven was worth":

```
AS SHIPPED   opener 0  named 0
  restore switch.main        -> opener   6  named   0
  restore switch.indicator   -> opener  14  named   8
  restore knob               -> opener  18  named  12
  restore checkbox.main      -> opener  20  named  12
  restore checkbox.knob      -> opener  22  named  14
  restore radio.main         -> opener  24  named  14
  restore radio.knob         -> opener  26  named  16
  restore button.main        -> opener  28  named  16
  restore textfield.main     -> opener  30  named  16
  restore stepper.main       -> opener  35  named  16
  restore stepper.step       -> opener  38  named  16
ALL ELEVEN RESTORED  opener 38  named 16
  opener law RED on corgi, 38 seats; first three:
      ('button.main', 'default', '▁▁▁▁', '▁')
      ('button.main', 'active', '▄▄▄▄', '▄')
      ('checkbox.main', 'default', '▁▁', '▁')
  named seat law RED on corgi, 16 seats; first three:
      ('checkbox.knob', 'default', '██', '█')
      ('checkbox.knob', 'checked', '██', '█')
      ('radio.knob', 'default', '▁●', '▁')
```

**In the suite, two new tests:**

- `test_both_seat_laws_go_red_on_each_of_the_eleven_tables_inc58_moved` — eleven arms off
  `CORGI_BANK_BEFORE`, each restoring ONE table and asserting BOTH counts against the number that
  table is worth, each requiring the matching law to raise, and each holding **the other ten languages
  still** on both rosters. The first two arms **delete a key** rather than restore one, because that is
  the defect in its original shape: corgi declared no `switch.main` and no `switch.indicator` at all.
- `test_corgi_draws_no_control_as_a_driven_bar` — **the ruling's whole sentence**, not its two seats.
  Every cell of every ruled control is checked against corgi's bank written as the full Unicode run
  `▁▂▃▄▅▆▇█▀▔`, deliberately wider than the four cells that mean something today: the point of the
  ruling is that the BANK is the readings' register, so a control reaching for `▃` or `▅` would be
  reaching into it whether or not that step is spoken for yet. It also asserts that the quadrant family
  appears at `knob`, `main` (the stepper's ground is `stepper.main`) and `step` only, and that the
  slider still resolves `main` while the switch resolves `switch.main`.

## 7. `HANDED_FIELDS` grew, and nobody decided it — the derivation noticed

corgi's field walls were a bank at a height (`▁▁ … ▁▁`, `▔▔ … ▔▔`) and **a bank has no hand**. They are
now the engraved key's two SHOULDERS, `▛▛ … ▜▜`, which are mirror images by construction. The language
always drew a key that way — `button.main`'s own comment says *"both shoulders are two cells wide and
the label sits in the milled channel between them"* — and only now spells the two shoulders with two
marks.

So `invalid_walls_are_handed_right` can fire on corgi for the first time, and `HANDED_FIELDS` goes
6 → 7. **It passes**: corgi's INVALID walls are `░░ … ░░`, inc52's ghost, unhanded. This is exactly the
event the roster's own comment describes for swiss in inc46 — *"Nobody decided that; the derivation
noticed it and this line is where it had to be written down"* — and it is written down.

## 8. Frames changed

**Four component frames and one gallery board, all corgi:**

```
corgi_S2   the form      the field walls, the checkboxes, the radios, both buttons
corgi_S3   the settings  five switches, the slider's knob, the danger button's walls
corgi_S4   the confirm   `▔▔ █Delete█ ▔▔   ▁▁  Cancel  ▁▁` -> `▛▛ █Delete█ ▜▜   ▒▒  Cancel  ▒▒`
corgi_S6   the monitor   the controls in the strip
gallery_corgi.{txt,svg}  the component sheet
```

`corgi_S1` and `corgi_S5` did **not** move: neither composes a ruled control. `render.py` reports
66 frames / 330 pairs / 0 hand-drawn and no two frames identical within a screen.

**`gallery_darkside.{txt,svg}` ALSO MOVED, AND IT IS NOT THIS INCREMENT'S DOING — IT IS E3 FIRING FOR
THE FIRST TIME.** The moon doodle is `PHASES[date.today().day % 6]`; the calendar day rolled 6 → 7
during this session, `PHASES[0]` is `"( )"` and `PHASES[1]` is `"(◎)"`, and the diff is that one cell
on that one row:

```
-                              │  ( ) gal
+                              │  (◎) gal
```

spec §14.5 predicted it in writing — *"On 29 days in 30 it would have moved. E3 is alive and this batch
is its second measurement"* — and this is its **third measurement and its first actual fire in this
worktree**. The artefact is committed because it is what the generator produces today; nothing in
`taskboard/language.py`'s darkside kit changed.

## 9. Risks

- **The frames got LIGHTER and that is a judgement, not a measurement.** `▒` and `▓` spend less ink
  than `▁▁`/`▄▄` at some seats and more at others; the whole-frame ink figures moved by under a point.
  Whether a TE panel should read as milled metal rather than as lit segments is the ruling, and the
  ruling is the orchestrator's under decision A — **the operator may reverse it and the eleven
  declarations are in one table (§3) so reversing it is one edit.**
- **`▖▗` is a faint ACTIVE mark.** A key pressed flush shows only its lower corners, which is the
  physical reading, but it is the lightest state in the set and a reader skimming for "which key is
  down" has less ink to find than before. Distinct in greyscale (it is its own code point pair) and
  `verify_language`'s pairwise-distinctness checks pass; it is a legibility risk, not a correctness one.
- **The slider still wears two severity rungs** (§4). Permitted by the rule, invisible to the census by
  the operator's own scoping request, and now the largest single thing corgi does that no instrument in
  this repo measures.
- **`Corgi.PANE_RULE = "█"` is the danger form drawn 16 times down `corgi_S1`** — see §10.

## 10. Found by looking, not fixed

- **`Corgi.PANE_RULE = "█"` — the display frame is `LEVELS["error"]` and `DANGER_FORM`, sixteen cells
  down the middle of `corgi_S1`.** It is a constant on the kit and outside `PART_GLYPHS`, so it is
  exactly the blind spot inc57 closed for `FIELD_LEAD` and `IDENT_GLYPHS` and did not close for this.
  The kit argues the cell on its own terms (*"the pane seat is the display frame — a SOLID BAR ...
  framed by SOLID BARS", LANGUAGES.md §3b verbatim*), so it is not obviously wrong; it is
  **unmeasured**, which is a different complaint. No roster reaches it and this increment did not widen
  one to catch it.
- **`Corgi.DISCLOSE = "▄"` and `Corgi.LIT = "▄"` are `LEVELS["warn"]`**, drawn as the select's
  disclosure (`▒▒mon    ▄▒▒` on `corgi_S3`) and the mode strip's lit segment. The kit's own comment
  answers the first — *"Two banks, two meanings, one alphabet"* — and nothing answers the second. Same
  blind spot as `PANE_RULE`, same reason it is named and not moved.
- **`▔` and `▂` left corgi's alphabet entirely and neither law asked them to.** They were chrome, not
  meanings, so the opener and named-seat laws were indifferent — but `▔` against `▀` (`REQUIRED`) and
  `▂` against `▁` (`LEVELS["info"]`) are two DRAWINGS OF ONE BAR AT TWO HEIGHTS, which is ruling D's
  own target in a family the `HOMOGLYPHS` table does not list. **The table is five pairs of round and
  square marks and no block pair is in it.** Widening it was measured as out of scope here (inc53
  refused to chain `· ∙ • ●` on a 19-against-5 count); this increment removed the two instances by
  taking the whole chrome off the bank, which is a cure that happens to cover a disease nobody has
  declared yet. **K2 is still open and this is a second crack in it.**
- **Eleven tables and only ONE of them was reached by BOTH laws at full strength** (`switch.indicator`,
  8 openers and 8 named seats). The named-seat law's whole corgi entry came from three tables; the
  opener law's from all eleven. Two laws over the same kit measure very different surfaces, and the
  §6 restore table is the first place in this worktree that number has been printed.
- **corgi's `·` census row did not move and cannot be moved from the control side.** It is 7 families
  because the RUNE of the invalid field is `·` and seven parts wear `·` when dead — and the rune is
  excluded by name from the test law and not from the census. spec §14.4 records the identical row for
  ledger. **The two instruments disagree about the rune and have since inc52.**

## 11. Pending — not this increment

- prism (opener 25, named 16), blueprint (12/12) and naught (3/12) are inc59–inc61.
- `Corgi.PANE_RULE`, `DISCLOSE` and `LIT` (§10) — a census widening, not a language rework.
- `49_darkside-modal-rounded-lid` in the skill's `assets/gallery/` is stale for the fourth batch
  running (spec §13.6, §14.5).

## 12. Suggested next task

**inc59 — prism.** Same shape, narrower alphabet: the ember ramp `⣀ ⣤ ⣿` is `LEVELS`, `DANGER_FORM`
and every control's chrome at once, `⡀` is `REQUIRED`, and the exclusivity checks in
`verify_language.py` have to be read before any braille cell outside the ramp is spent.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1101 passed, 2 skipped, 1 failed`
      (`067400c` was `1099 passed, 2 skipped, 1 failed`; +2 is this increment's two new tests). The
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      **reported, not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py`
      66 frames / 330 pairs / 0 hand-drawn. `matrix.py` 66 of 66, refusals `[]` for all eleven.
      `capture_languages.py plain` 22 captures, 22 grids identical across two processes, no two boards
      identical. `collision_census.py` both self-checks green, TOTAL 33 → 30, homoglyph rows 4.
      Verbatim tails in `prototypes/out/`.
- [x] **No secrets in code or output** — eleven glyph tables, two roster entries, one roster tuple,
      two tests and one packet. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. The watch-it-fail probe
      (`prototypes/out/_watch58.py`) patches `LG.Corgi.PART_GLYPHS` in its own process and writes
      nothing; `git status` shows only the two source files and the generated artefacts.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`. The 12 frame/gallery artefacts and the census table are written by
      `render.py`, `capture_languages.py` and `collision_census.py`.
- [x] **Review packet attached** — this document.

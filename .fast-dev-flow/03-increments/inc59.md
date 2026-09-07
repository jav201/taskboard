# Increment 59 — prism's ember is read from the bottom

**Batch:** `rework-5c`, increment 2 of 5 · decision **A** of `PROTOTYPE-inheritors-2.md` §6 for the
second of the three languages that had never had an increment
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 8 regenerated
component artefacts, 2 regenerated gallery artefacts, the regenerated census table and this packet.

**Prism's ember ramp is the four dot-rows of a braille cell filling upward, and three of its four steps
plus the leading dot carry a meaning. Every control was drawn out of the same cells. `prism_S4` is the
single sharpest frame in the corpus: `⣿⣤ ⣿Delete⣿ ⣤⣿   ⣿⣀  Cancel  ⣀⣿` — the DANGER FORM around the
irreversible answer and the WALL of the safe button beside it, THE SAME CELL, eight columns apart on one
row. The kit had already written the cure for one part and never applied it to the others: the knob's
own comment says every state is "a BROKEN field ... precisely so the knob can never be mistaken for a
full cell of fire". inc59 widens that sentence to every control and gives it a direction — the ember is
read from the BOTTOM, a control from the TOP. Ten declarations, opener 25 → 0, named 16 → 0, census
4 → 2, TOTAL 30 → 28. Suite 1101 → 1103. `verify_language` went RED first, on a closed seat, and its
own comment supplied the fix.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **A — the five languages that never had an increment get one each, guided by the laws.** Each
> increment ends with that language's rosters at zero or with every remaining row exempted by name and
> citation.

The brief's instruction for this increment:

> Prism's ember ramp `⣀ ⣤ ⣿` is LEVELS and DANGER and every control's chrome. Prism's doctrine (§8):
> borders reserved for modals, the ember ramp as the whole severity device, `⡀` REQUIRED. Same shape of
> decision as corgi: **which braille cells outside the ramp (prism borrows braille from instrument;
> check `verify_language`'s exclusivity checks first) can carry chrome without being a rung.**

## 1. The frames, read before anything was written

| cell | what it means | where else it stands, in the SAME frame |
| --- | --- | --- |
| `⣿` | `LEVELS["error"]` **and** `DANGER_FORM` | `prism_S4` row 19: `⣿⣤ ⣿Delete⣿ ⣤⣿   ⣿⣀  Cancel  ⣀⣿` — **the danger form and the safe button's wall, ONE ROW, eight columns apart** |
| `⣿` | as above | `prism_S2` row 7 `⣿⣿ expected YYYY-MM-DD` (the error message's leader) against row 11 `⣿⣀⣿ api  ⣿⠀⣿ ui` — **the checkboxes, four rows apart** |
| `⣿` | as above | `prism_S3` rows 4–8: `⣿⣿⢸` — **the switch's ON track**, sixteen rows above `⣿⣀⣿Delete all⣿⣀⣿` |
| `⣀` | `LEVELS["info"]` | `prism_S2` row 9 `⣀⣀⣀ low  ⣀⣀⣀ norm  ⣀⣿⣀ high` — the radio group, and the field's paper under focus |

No exemption was drafted for prism. The `prism_S4` row settles it on its own: an exemption has to leave
a control's opener distinct from an error rung, and here the two are not merely alike, they are the
identical cell in the identical row.

## 2. The ruling this increment writes

> **THE EMBER IS READ FROM THE BOTTOM; A CONTROL IS READ FROM THE TOP.** prism's ramp is the four
> dot-ROWS of a braille cell filling upward — `⣀` one row, `⣤` two, `⣶` three, `⣿` the whole cell,
> nothing left to burn — and `⡀` is its leading dot. **No control draws a rung of that ramp.** Where a
> control needs a field it draws the SAME dot-rows READ FROM THE TOP — `⠁` one dot, `⠉` one row, `⠛`
> two, `⠿` three — the identical shape ladder at the opposite POSITION in the cell, which is ruling D's
> third channel, and it stops one row short of `⣿` by construction.

**It is the kit's own sentence, widened.** `Prism.PART_GLYPHS["knob"]` already carries it:

> *"Every state below is a BROKEN field (a dot column missing) precisely so the knob can never be
> mistaken for a full cell of fire or for an empty cell of track."*

That was true of one part and false of every other part in the same table. inc59 makes it true of all of
them and gives it a spelling: a control is the ramp upside down.

**The broken fields the kit already declares are NOT rungs and are untouched** — `⣷` `⣾` at the walls,
`⢿` at the grip, `⣹` `⣏` at the refused value (inc51, inc52), `⢸` the half cell, and the residue
`⠄ ⠁ ⠈`. What moved is exactly the cells that mean something.

## 3. The ten declarations, before and after

| # | key | before | after | why |
| --- | --- | --- | --- | --- |
| 1 | `switch.main` | **did not exist** — fell to `main`, `⣀` / `⠄` | `⠉` / `⠄` | the off-track was `LEVELS["info"]`. **Worth ZERO on both rosters** — see §6 |
| 2 | `switch.indicator` | **did not exist** — fell to `indicator`, `⣿` / `⣤` | `⠿` / `⠛` | the ON-track was the error rung and the danger form at 6 named seats; the dead one was `LEVELS["warn"]` at 2 more |
| 3 | `checkbox.main` | `⣿⣀⣿ ⣷⣀⣷ ⣾⣀⣾ ⠄⠄⠄` | `⠿⠉⠿ ⣷⠉⣷ ⣾⠉⣾ ⠄⠄⠄` | intact wall + intact centre; the two BROKEN walls kept |
| 4 | `checkbox.knob` | `⣿⠀⣿ ⣷⠀⣷ ⣾⠀⣾ ⠄⠀⠄` | `⠿⠀⠿ ⣷⠀⣷ ⣾⠀⣾ ⠄⠀⠄` | the DEFAULT wall only |
| 5 | `radio.main` | `⣀⣀⣀ ⣤⣤⣤ ⣶⣶⣶ ⠄⠄⠄` | `⠉⠉⠉ ⠛⠛⠛ ⠿⠿⠿ ⠄⠄⠄` | the run WAS the ember, info and warn rungs at four openers |
| 6 | `radio.knob` | `⣀⣿⣀ ⣤⣿⣤ ⣶⣿⣶ ⠄⠁⠄` | `⠉⢸⠉ ⠛⢸⠛ ⠿⢸⠿ ⠄⠁⠄` | the CHOSEN cell was `⣿` at six named seats — see below |
| 7 | `button.main` | `⣿⣀⣀⣿ ⣿⣤⣤⣿ ⣿⣿⣿⣿ ⠄⠄⠄⠄` | `⠿⠉⠉⠿ ⠿⠛⠛⠿ ⠿⠿⠿⠿ ⠄⠄⠄⠄` | every live cell of the control was a rung. The press still BREATHES |
| 8 | `textfield.main` | `⣿⠀⣿ ⣿⣀⣿ ⣿⣤⣿ ⣿⣶⣿` | `⠿⠀⠿ ⠿⠁⠿ ⠿⠉⠿ ⠿⠛⠿` | wall + paper. The paper's ladder is 0, 1, 2, 4 dots inside a wall of 6, so the wall always stands above it. `⣹⠀⣏` and `⠄⠄⠄` unchanged |
| 9 | `stepper.main` | `⣀⣀` / `⠄⠄` | `⠉⠉` / `⠄⠄` | five of the twenty-five opener seats in one line |
| 10 | `stepper.step` | `⡀⢀ ⡄⢠ ⡆⢰ ⣇⣸ ⣹⣹ ⠁⠈` | `⠄⠠ ⡄⢠ ⡆⢰ ⣇⣸ ⣹⣹ ⠁⠈` | **DEFAULT only.** `⡀` is `REQUIRED`, so a stepper at rest said the seat was compulsory |

**`radio.knob`'s chosen cell is the increment's one judgement call.** The kit's comment says *"checkbox
carves, radio LIGHTS — so the two families differ in DIRECTION, not in brightness"*, and that sentence
was false as written: the run was `⣀ ⣤ ⣶` and the chosen cell `⣿`, which differs in brightness and in
nothing else. The chosen cell is now the HALF CELL `⢸` — **this kit's own words about the part it
is**: *"the knob is a HALF-CELL mark (`⢸` / `⡇`), the only vocabulary here whose grip can sit inside a
cell — the same half-cell precision the meter's frontier needs, said about POSITION."* A COLUMN standing
in a run of ROWS. The comment is now true.

**`stepper.step`'s ladder is preserved exactly, one dot-row up.** `⠄⠠ → ⡄⢠ → ⡆⢰ → ⣇⣸` is 1, 2, 3, 5
dots a side and **each rung is a superset of the one below it** — `⠄⠠` plus the bottom dot is `⡄⢠`.
Direction is untouched: left column steps back, right column steps forward.

## 4. `verify_language` went RED, and its own comment supplied the fix

The first answer for `stepper.step[DEFAULT]` was `⠂⠐`, row two. `verify_language` refused it:

```
1 FAILURE(S): ["#44: the METER no longer spells the registry's unlit — and the claim goes exactly
that far: TWO other seats still do (`Instrument.BLANK`, its `radio.main`) and they are the KIT's
vocabulary, not this family. `plot`'s `off=` left at #40d"]
  ['language.py:162', 'language.py:4956', 'language.py:5419', 'language.py:7410', 'language.py:7413']
```

`⠐` is a **closed, counted seat**: the check asserts `len(_dots) == 3` over every `⠐` in the package,
naming `COVER_RAMPS["braille"][0]`, `Instrument.BLANK` and `Instrument.radio.main`. **This is the fourth
time in this worktree that `verify_language` has caught something the pytest suite could not** (§11.5
twice, §14.7 once), and it caught it twice in one increment: the second red was the COMMENT explaining
the first, because the law counts occurrences in comments too — which is precisely what its own text
says it does, and why it tells the reader to write the cell in dot NUMBERS.

**The law was not narrowed.** Its comment says *"the fix for a red is never to narrow the law that found
it"*, so the step took row THREE (`⠄⠠`, dots 3 and 6, counted by nothing) and the kit comment names row
two in dot numbers instead of spelling it. `verify_language.py` was **not edited**.

## 5. The rosters and the census

```
                      inc58   inc59
MEANING_AT_AN_OPENER
  prism                 25       0
  naught                 3       3
  blueprint             12      12
  the other eight        0       0

MEANING_AT_A_NAMED_SEAT
  prism                 16       0
  naught                12      12
  blueprint             12      12
  the other eight        0       0
```

```
collision census      inc58   inc59
naught                    5       5
corgi                     2       2
instrument                4       4
swiss                     2       2
industrial                2       2
nord                      1       1
darkside                  1       1
prism                     4       2
ledger                    2       2
solari                    3       3
blueprint                 4       4
-------------------------------------
TOTAL                    30      28
homoglyph rows            4       4     (naught 2, darkside 1, ledger 1 — prism has none)
```

prism's `⣀`, `⣤` and `⡀`-as-a-step rows are gone; `⣿` fell from 7 families to 2. **The two that remain:**

- **`⣿` [2 families]** — `LEVELS[error]` × `DANGER_FORM`, which is `DANGER_IS_THE_TOP_RUNG["prism"]`,
  *"`⣿⣿` — LEVELS[error]; nothing left to burn"*. Exempt by name with its citation, intact.
- **`⡀` [2 families]** — `REQUIRED` × `field.leader open (declared)`, and it was 3 families before this
  increment (the stepper's DEFAULT step left it). **Exempted here by name and with the kit's own
  citation, and the citation is CONTESTABLE, which is said out loud rather than left for the next
  reader.** `Prism.REQUIRED`'s comment argues the identity: *"THE EMBER'S LEADING CELL — the frontier
  `field_row` draws, at one dot. 'Quantity is a solid field being CONSUMED': a required seat is a field
  the value has not reached yet."* **The frame does not bear it out.** `prism_S1` draws the leader
  `⡀⡤⣶` on six detail rows — `Web`, `doing`, `3d`, `high`, `open`, `jav201` — none of which is
  compulsory and all of which have a value. So the leader is not "a field the value has not reached
  yet"; it is every definition row's lead-in. This is an A × B row, which spec §11.2 records the rule
  as PERMITTING, and it is not one of the three rosters ruling A names — so it is exempted and NOT
  fixed, because both available fixes churn a declaration that neither law touched (`FIELD_LEAD` is
  inc57's, one batch old; `REQUIRED`'s comment is the ember doctrine). **Carried to §10.**

`... 2 further cells would collide if slider/bar/scrollbar were in the B set` — was 0, is 2. That is the
declared cost of §7, printed by the instrument itself.

## 6. Teeth

**Watched failing BY HAND, one declaration at a time** (`prototypes/out/_watch59.py`, output at
`prototypes/out/watch59.txt`):

```
AS SHIPPED   opener 0  named 0
  restore switch.main        -> opener   0  named   0
  restore switch.indicator   -> opener   0  named   8
  restore checkbox.main      -> opener   2  named   8
  restore checkbox.knob      -> opener   4  named  10
  restore radio.main         -> opener   8  named  10
  restore radio.knob         -> opener  12  named  16
  restore button.main        -> opener  15  named  16
  restore textfield.main     -> opener  19  named  16
  restore stepper.main       -> opener  24  named  16
  restore stepper.step       -> opener  25  named  16
ALL TEN RESTORED  opener 25  named 16
  opener law RED on prism, 25 seats; first three:
      ('button.main', 'default', '⣿⣀⣀⣿', '⣿')
      ('button.main', 'focused', '⣿⣤⣤⣿', '⣿')
      ('button.main', 'active', '⣿⣿⣿⣿', '⣿')
  named seat law RED on prism, 16 seats; first three:
      ('checkbox.knob', 'default', '⣿⠀⣿', '⣿')
      ('checkbox.knob', 'checked', '⣿⠀⣿', '⣿')
      ('radio.knob', 'default', '⣀⣿⣀', '⣀⣿')
```

**`switch.main` SCORES ZERO ON BOTH ROSTERS AND MOVED ANYWAY.** Its glyph is ONE cell, so the opener law
skips it (`len(glyph) < 2` — a one-cell glyph has no opener), and `main` is a named seat only when the
control is dead. So `⣀`, `LEVELS["info"]`, was the off-track of every prism switch and **no law in this
file reached it.** It moved under the ruling, not under a roster, and it is written into
`PRISM_EMBER_BEFORE`'s own comment so the next reader meets it rather than deducing it.

**In the suite, two new tests:**

- `test_both_seat_laws_go_red_on_each_of_the_ten_tables_inc59_moved` — ten arms off
  `PRISM_EMBER_BEFORE`, restored in declaration order with CUMULATIVE counts asserted after each, both
  laws required to raise once all ten are back, and the other ten languages held still on both rosters
  in every arm.
- `test_prism_draws_no_control_on_the_embers_own_rungs` — the ruling's sentence over every cell of every
  ruled control, against `Prism.RAMP` (all FOUR steps, not the three that mean something today — the
  same widening inc58 made for corgi's bank and for the same reason). It also asserts the scoping that
  lets the slider keep the ember, and — in dot COUNTS, off the shipped declarations — that **the
  checkbox's wall ladder now CLIMBS**: it ran `⣿` (8 dots) at rest, `⣷` (7) focused, `⣾` (7) active, a
  control that DIMMED when the reader arrived at it. At `⠿` (6) it climbs.

## 7. What did NOT move, and the cost

**`main`, `indicator` and `scrollbar.*` keep the ember**, and the kit's reason is explicit: *"A SHAFT IS
NOT A SCALE. The slider's track is every value the knob could take, so it is the ramp's floor."* A
quantity in this language IS the ember. The switch is hardware and takes scoped tables, so the base pair
is now the slider's and the bar's alone — **the same trade inc58 made for corgi, and it costs the same
kind of blindness**: the census's own last line goes `0 further cells` → `2 further cells would collide
if slider/bar/scrollbar were in the B set`. `⣀` and `⣿` are still the info and error rungs and still the
slider's shaft and fill.

## 8. Frames changed

```
prism_S2   the form      the field walls and paper, the checkboxes, the radios, both buttons
prism_S3   the settings  five switches, both selects, the danger button
prism_S4   the confirm   ⣿⣤ ⣿Delete⣿ ⣤⣿   ⣿⣀  Cancel  ⣀⣿  ->  ⠿⠛ ⣿Delete⣿ ⠛⠿   ⠿⠉  Cancel  ⠉⠿
prism_S6   the monitor   the controls in the strip
gallery_prism.{txt,svg}  the component sheet
```

`prism_S4`'s new row is the finding fixed and visible: **`⣿` is now the only intact cell on it**, and it
is the danger form. `prism_S1` and `prism_S5` did not move — neither composes a ruled control.
`render.py` 66 frames / 330 pairs / 0 hand-drawn. `capture_languages.py` moved 1 of the 22.

**`gallery_darkside` did not move this time**, which is E3 behaving as spec §14.5 describes: the day did
not roll during this increment, and `PHASES[7 % 6]` is what inc58 already committed.

## 9. Risks

- **`⠿` is six dots and `⣿` is eight, and a reader at 12px may not count them.** The two are told apart
  by POSITION — `⠿` sits high in the cell, `⣿` fills it — which is ruling D's third channel and a real
  one, but it is a finer distinction than corgi's `▒` against `▄`. The mitigation is that the two never
  appear in the same ROLE any more: after this increment `⣿` appears in a control's seat nowhere at all.
- **The controls got lighter.** prism_S2's ink fell and the form reads calmer, which is arguably right
  for a language whose commitment is "airy" — and arguably a loss of the "walls of fire" the kit's own
  comment describes. **This is the orchestrator's judgement under decision A and the operator may
  reverse it**; the ten declarations are in one table (§3).
- **`⡀` is still two things** (§5), exempted with a citation the increment itself argues against.
- **`⠄` is now a live DEFAULT step and prism's residue everywhere else.** `stepper.step[DEFAULT]` is
  `⠄⠠` while `⠄` is the DISABLED mark of `main`, `checkbox.main`, `radio.main`, `stepper.main` and
  `textfield.main`. B × B, permitted, and the pair `⠄⠠` is unique — but a live step drawn with the dead
  language's cell is a legibility cost and it was taken because row two is closed (§4).

## 10. Found by looking, not fixed

- **`Prism.REQUIRED` and `Prism.FIELD_LEAD` are the same claim said twice, and the frame refutes the
  kit's argument for it** (§5). The leader `⡀⡤⣶` stands on six rows of `prism_S1` that are neither
  required nor empty. Exempted with its citation and named as contestable.
- **`switch.main` proves the opener law has a hole the width of a one-cell glyph.** `if len(glyph) < 2:
  continue` means a language that draws its controls in SINGLE cells is invisible to the opener law
  entirely. prism draws `main` and `indicator` that way and both were severity rungs. No roster would
  ever have found it; the ruling did. **The law's exclusion is defensible — a one-cell glyph has no
  "first cell" distinct from itself — and it is now measured rather than assumed.**
- **`Prism.SPIN = ("⣀", "⣤", "⣶", "⣿", "⣶", "⣤")` is the whole ember ramp, including both meaning
  rungs, breathing once a frame.** No language's `SPIN` is censused — spec §14.7 named the same gap for
  darkside — and this is the second measurement of it. Defensible (a spinner is motion, not a reading)
  and still a decision nobody has made in writing.
- **`Prism.keyhint` draws `⣶` between every key and its word** and `Prism.DISCLOSE = "⣶"`. `⣶` is the
  ramp's third step and carries no meaning, so no law fires — but it is the one ramp step `LEVELS`
  skipped, and if severity ever wanted a fourth rung it would collide with both.
- **The checkbox DIMMED when focused for the life of this kit** (§6) and no instrument here measures
  the direction of a state ladder. inc41 asserts declared == painted; nothing asserts that attention
  adds ink. The new test does it for prism's checkbox only, by name.

## 11. Pending — not this increment

- blueprint (opener 12, named 12, census 4, plus the `╱` shared by HELD and INVALID) is inc60; naught
  and ledger are inc61.
- `Prism.SPIN`, `keyhint`'s `⣶`, and the `⡀` exemption (§10).
- `49_darkside-modal-rounded-lid` in the skill's `assets/gallery/` is stale for the fourth batch running.

## 12. Suggested next task

**inc60 — blueprint.** Ten marks by docstring and twelve seats on each roster: `├ ┤` are `REQUIRED` and
every control's terminators, `━` is the error rung and the danger form (top-rung exemption), and `╱`
doubles as the HELD texture and the INVALID hatch since inc52. Find the assignment where `REQUIRED` is
not a terminator — or the terminators are not `REQUIRED` — and where `INVALID` does not share the HELD
texture, citing LANGUAGES.md §11. If ten marks cannot cover it, say which meaning is dropped and why, by
name.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1103 passed, 2 skipped, 1 failed`
      (inc58 closed at `1101 passed`; +2 is this increment's two new tests). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) — **reported,
      not counted, not touched.** `verify_language.py` **ALL PASSED exit 0 — and it was RED TWICE
      first**, on the real declaration and then on the comment about it (§4), reported rather than
      skipped and fixed without editing the law. `render.py` 66 frames / 330 pairs / 0 hand-drawn.
      `matrix.py` 66 of 66, refusals `[]`. `capture_languages.py plain` 22 captures, 22 grids identical
      across two processes, 1 moved. `collision_census.py` both self-checks green, TOTAL 30 → 28,
      homoglyph rows 4.
- [x] **No secrets in code or output** — ten glyph tables, two roster entries, one roster tuple, one
      `STEP_TURNS` entry, two tests and one packet. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none. The watch-it-fail probe
      (`prototypes/out/_watch59.py`) patches `LG.Prism.PART_GLYPHS` in its own process and writes
      nothing.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`. **`prototypes/verify_language.py` was NOT edited**, deliberately: its
      law found a real defect and the law's own comment forbids narrowing it.
- [x] **Review packet attached** — this document.

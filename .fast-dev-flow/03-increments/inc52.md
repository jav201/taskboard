# Increment 52 — `INVALID` never takes `DANGER_FORM`: the ruling of record, revoked

**Batch:** `rework-5a`, opening increment · carries out **Ruling C** on `PROTOTYPE-inheritors-2.md` §6
decision (C), which inc51 §11 listed as the operator's and applied twice more while it waited
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 6 regenerated
frame artefacts, the regenerated census table and this packet.

**inc39 ruled that where un-flipping a field's walls would collide with DEFAULT byte for byte, the walls
take that language's own `DANGER_FORM`; inc51 applied it a sixth and seventh time and wrote down that it
was doing so under a ruling nobody had confirmed. That ruling is revoked here. Ten declarations move in
four kits and one kit's `DANGER_FORM` moves instead, and the law that closes them is the one-mark-one-
meaning law with `invalid` added as its fifth family and NO by-name exemption against the danger form.
Census 36 → 33; the meaning×meaning count with the four `DANGER_IS_THE_TOP_RUNG` exemptions subtracted
falls 6 → 4, and all four that are left are the exemption itself. Six frames moved.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **inc52 · Ruling C: `INVALID` never takes `DANGER_FORM`**
> "Does not parse" and "destroys data" are two meanings. inc39's rule ("where un-flipping collides, the
> walls take the language's DANGER_FORM") is revoked. Apply inc51's clause 2 to the text field:
> `textfield[INVALID]` walls and `stepper.step[INVALID]` draw from the cells the kit already spends on a
> rejected value at its knob (the declared invalid channel), never from `DANGER_FORM`, `LEVELS` or
> `REQUIRED`. Revert the seven applications by name: nord/Kit `? ?` (check: is `?` also anything else? if
> clean, keep), swiss `╲ ╱` textfield and `╲╲` stepper, blueprint `━·━` and `━━`, darkside `Ø…Ø`
> (darkside's `Ø` is both DANGER and invalid knob: DANGER moves, since the knob's invalid mark was
> declared first; cite), corgi `▄`/`█` if applicable, ledger `‡` if it still doubles. Extend
> `test_a_languages_meaning_marks_do_not_share_a_cell` so `DANGER_FORM` vs the declared INVALID marks has
> NO by-name exemption; the "DANGER_FORM as top rung of LEVELS" exemption for naught/corgi/prism/blueprint
> stays (that is tier, a declared channel). Teeth: restore swiss `╲ ╱`, the test names swiss and the two
> roles. Re-render, list frames changed, census before/after.

### 0a. Which half of the ruling became a law, and why the other half did not

The ruling states a POSITIVE clause ("draw from the cells the kit already spends on a rejected value at
its knob") and a NEGATIVE one ("never from `DANGER_FORM`, `LEVELS` or `REQUIRED`). **Only the negative is
written as a law, and the positive is used as the design rule for the moves.** Measured before deciding —
walls only, as the ruling scopes it:

```
language     knob[INVALID]   textfield walls   walls ⊆ knob's cells?
naught       ◑               ◑   ◑             yes
corgi        ▀▄              ▄▀  ▀▄            yes
instrument   ⠶               ⠸   ⠇             NO
swiss        ╲               ╲   (air)         yes
industrial   /               ▐   ▌             NO
nord (Kit)   ▚               ?   ?             NO
darkside     Ø               Ø   Ø             yes
prism        ⣹               ⣹   ⣏             NO
ledger       ‡               ‡   ‡             yes
solari       ═               ═   ═             yes
blueprint    ├               ━   ━             NO
```

**The positive clause as a law would go red on five, and the FIRST of the five is `nord ? ?` — which the
same ruling orders kept if `?` is clean.** It is clean (`?` appears nowhere else in `Kit` or in nord;
the census has no `?` row), so it is kept. Three of the other four are languages whose invalid walls are
their DEFAULT walls with the PAPER carrying the state — instrument, industrial and prism — which is their
declared idiom and which inc39 §8 already recorded as a standing question, not a defect this ruling
names. So the positive clause is the rule the moves were CHOSEN by (every new cell below comes from the
kit's own knob) and the negative clause is the rule the test ENFORCES. Said out loud rather than quietly
narrowed.

**The rune is excluded from the law by name.** A field's glyph is *"wall, RUNE, wall"* (`Kit.field_form`)
and the rune is the PAPER the value's own cells lie on — blueprint's `·`, naught's `·`, ledger's `·` are
the paper of DEFAULT and ACTIVE and FOCUSED too. Counting it would have turned "what a field is made of
here" into "your value is wrong", and it would have made four more languages red for a reason the ruling
does not name. The exclusion has its own test (§3).

---

## 1. What was actually there, and which direction each collision runs

| kit | the cell | it was | and also | which is older, by the kit's own words |
| --- | --- | --- | --- | --- |
| **swiss** | `╲` | `knob`/`textfield.main`/`stepper.step` `[INVALID]` | `DANGER_FORM[0]` | the kit says the DANGER form came second — *"`field_form(INVALID)` is `╲ ╱` here, SO a destructive control is bracketed by the same pair"* |
| **darkside** | `Ø` | the same three slots | `DANGER_FORM` both halves | the kit says the same — `DANGER_FORM = ("Ø","Ø")  # its own INVALID wall, the struck mark` |
| **blueprint** | `━` | `textfield.main`/`stepper.step` `[INVALID]` | `DANGER_FORM` **and** `LEVELS["error"]` | the invalid walls are inc39's own edit (`c99ddb8`); the rung and the form predate it |
| **blueprint** | `├` | `knob[INVALID]` | `REQUIRED` | `REQUIRED = "├"` carries its own citation; the knob's invalid was never argued |
| **corgi** | `▀` | `knob`/`textfield.main`/`stepper.step` `[INVALID]` | `REQUIRED` | `REQUIRED = "▀"` — *"the upper bank lit"* |
| **corgi** | `▄` | the same three slots | `DISCLOSE` **and** `LEVELS["warn"]` | `DISCLOSE = "▄"` — *"the bank below the segment"* |
| **instrument** | `⠇` | `textfield.main[INVALID]`, closing rail | `LEVELS["error"]` | the rung is the ladder's; the rail is every field state's |

**Two of the seven run the other way, and the ruling says so for darkside.** swiss's and darkside's kits
both derive the danger form FROM the field, in a comment. The ruling names darkside explicitly (*"DANGER
moves, since the knob's invalid mark was declared first"*) and names swiss's textfield and stepper in the
revert list. **So the two are resolved in opposite directions, and it is deliberate on the ruling's word
rather than on a principle this increment invented** — the tension is recorded in §8 as a risk.

**`corgi ▄`/`█` — the ruling's "if applicable" is answered NO for `█` and YES for `▄`.** corgi's invalid
walls were never its `DANGER_FORM` (`█ █`), so corgi is not one of inc39's applications and the E1
exemption (`██` = `LEVELS["error"]` as a form) is untouched. But `▀` and `▄` are `REQUIRED` and the warn
rung, which the ruling's own "never from `LEVELS` or `REQUIRED`" reaches. It moved.

**`ledger ‡` — "if it still doubles" is answered NO.** inc45 moved ledger's ladder to `* / **`, so `‡` is
the invalid wall and `†` is `REQUIRED`, and neither appears in `LEVELS`. Left alone; the test asserts it
(`test_ledgers_two_daggers_are_an_order_and_not_a_pair`, unchanged).

---

## 2. The ten moves, each onto a cell with a citation in its own kit

| kit | slot | was | is | the citation |
| --- | --- | --- | --- | --- |
| **swiss** | `knob[INVALID]` | `╲` | **`║`** | the four weights of this stroke (`│ ┃ █ ┆`) are the CONTROL's own states, so rejection cannot take a fifth weight without being read as one; it takes the other channel this alphabet has — **COUNT**, the first the batch rule lists. One mark on one side, enclosing nothing at any width (inc38's argument, inc46's seat), so *"no boxes, at any width"* survives. A doubled rule in the margin is what a compositor sets beside copy that is queried. |
| swiss | `textfield.main[INVALID]` | `╲  ` | **`║  `** | the knob's own mark |
| swiss | `stepper.step[INVALID]` | `╲╲` | **`║║`** | the knob's own mark; inc51's clause 2 holds through both edits |
| **darkside** | `DANGER_FORM` | `("Ø","Ø")` | **`("▚","▞")`** | §8 leaves hue out (*"the accent marks interactivity, NOTHING ELSE"*) and an enclosure out (*"NEVER borders"*); WEIGHT is what is left. Half coverage is a step between this kit's `▬` and its `█`, the pair is HANDED — the hatch leans out on each side, which is what makes it a form and not one mark used twice — and neither cell is drawn anywhere else in this kit. `Ø` stays where it was declared. |
| **blueprint** | `knob[INVALID]` | `├` | **`╱`** | the class docstring lists the sheet's alphabet as *"`─ ━ ├ ┤ ╌` (the dimension vocabulary), `┌ ┐ └ ┘` (registration marks) **and the hatch** — TEN"*, and `hatch="╱"` is the one of the ten that states neither an extent nor a datum. On a drawing a figure that must not be used is HATCHED. |
| blueprint | `textfield.main[INVALID]` | `━·━` | **`╱·╱`** | the same; the rune stays `·`, the paper of every other state |
| blueprint | `stepper.step[INVALID]` | `━━` | **`╱╱`** | the knob's own mark |
| **corgi** | `knob[INVALID]` | `▀▄` | **`░░`** | `░` is the ONE cell in this kit's block alphabet that no meaning and no other control state spends — the shaft's own ghost, *"a segment present but NOT DRIVEN"* (`scrollbar.main`). The words stay in the milled channel and the bank behind them shows nothing, because the machine would not drive it. |
| corgi | `textfield.main[INVALID]` | `▄▀·▀▄` | **`░░·░░`** | the knob's own mark; rune unchanged |
| corgi | `stepper.step[INVALID]` | `▀▄▄▀` | **`░░░░`** | the knob's own mark |
| **instrument** | `textfield.main[INVALID]` | `⠸⠶⠇` | **`⠶⠶⠶`** | `⠶` is what this kit already spends on a rejected value at its knob AND at its stepper. The rails come OFF when the span is refused: keeping them cost the closing rail `⠇`, which is `LEVELS["error"]`, on a language whose whole method is that the paper carries the state. |

**`╳` was refused three times, and the reason is a measurement.** It is the obvious answer for swiss
(`╲`+`╱` in one cell), for blueprint (cross-hatch) and for corgi. It is the CORPUS'S DEAD MARK: `Kit`
spends it at `knob[disabled]`, `checkbox.knob[disabled]`, `radio.knob[disabled]` and
`stepper.step[disabled]`, and corgi and nord re-declare it at their own disabled seats. inc45 §7 refused
`×` for nord on exactly this ground — *"a cross meaning 'dead' beside a cross meaning 'dangerous' is
exactly the defect this increment exists to remove"*. Dead and refused are two claims.

---

## 3. The law, and the three tests

`tests/test_components.py`.

**The law** — `_meaning_marks` gains a fifth family, `invalid`, built by `_invalid_marks(k)` from
`knob[INVALID]`, the two WALLS of `textfield.main[INVALID]` and `stepper.step[INVALID]`, read as
DECLARATIONS (a table without the key is not read — `collision_census.py`'s own line). The E2 exclusion
that said *"INVALID IS NOT IN THIS SET"* is gone and its docstring now names the ruling it reverses.
`DANGER_IS_THE_TOP_RUNG` stays and its scope is written down: it covers `danger` against `ladder` and
nothing else, **because tier is a channel a language declares and a rejection is not a tier of a
destruction**.

**The teeth** — `test_the_invalid_channel_law_goes_red_on_the_declarations_inc52_moved`, **ten
parametrisations**, one per moved declaration, each restoring the exact byte string HEAD carried and
asserting (a) the law names the LANGUAGE and the TWO ROLES, (b) the parametrised law raises for that
language, (c) the other ten stay clean under the same patch. Swiss's three slots each carry the collision
alone, and so do blueprint's and corgi's — which is what says these are ten declarations in four kits
rather than one shared defect.

**The eleventh arm** — `test_the_invalid_channel_law_goes_red_on_darksides_restored_danger_form` is the
one that patches a MEANING rather than a glyph table, because darkside is the one kit where the danger
form is what moved.

**The exclusion's own teeth** — `test_the_rune_is_excluded_from_the_invalid_channel_by_name` asserts the
boundary in BOTH directions: blueprint's invalid rune IS `·` and `·` IS `LEVELS["info"]` and the law is
still silent; put the same cell on a WALL (`·╱·`) and it fires. An exclusion nobody can watch is a hole.

**Watched fail by hand, on the real declaration.** swiss's three `╲` restored in `language.py`:

```
$ python -X utf8 -m pytest "tests/test_components.py::test_a_languages_meaning_marks_do_not_share_a_cell" -q
E       AssertionError: ('swiss', [('danger', 'invalid', '╲', '╲╱', '╲╲ ╲╲')])
FAILED ...[swiss]
1 failed, 10 passed in 0.64s
```

**The language, the two roles, the shared cell and both marks** — which is the ruling's teeth clause,
verbatim. `language.py` was restored from a byte copy taken before the experiment and the eleven re-run
green (`11 passed in 0.49s`).

## 4. One exemption deleted, and the deletion is measured before it is made

`meaning_marks_at_an_opener` carried *"a field whose INVALID walls are that language's own
`DANGER_FORM`"*, on inc39's ruling. With the ruling revoked the exemption has nothing to stand on, so it
is deleted rather than left as an exemption nothing sits under (`verify_language`'s own bargain: *"an
exemption no hit sits under is an exemption widened past its evidence"*). **Measured before deleting it,
across all eleven, it fired ZERO times** — swiss, darkside, blueprint and corgi had already moved off it
in this same increment — so the rosters are unchanged by the deletion and corgi's −2 below is the
DECLARATIONS moving, not the exemption going.

| roster | before | after | what moved |
| --- | --- | --- | --- |
| `MEANING_AT_AN_OPENER["corgi"]` | 40 | **38** | `▄▀·▀▄` opened on the warn rung and `▀▄▄▀` on `REQUIRED`; both now open on the ghost |
| naught 3 · prism 25 · blueprint 12 · seven zeros | — | **unchanged** | — |
| `MEANING_AT_A_NAMED_SEAT`, all eleven | — | **unchanged** | `knob[INVALID]` is not a state `component_states` derives for a checkbox, a radio or a switch, so no knob seat moved |

## 5. Census delta

```
language      inc51   inc52
naught            5       5
corgi             5       5
instrument        5       4
swiss             3       2
industrial        2       2
nord              1       1
darkside          2       1
prism             4       4
ledger            2       2
solari            3       3
blueprint         4       4
--------------------------
TOTAL            36      33
```

**Three rows leave the census outright** — `swiss ╲` (DANGER_FORM open + the three invalid slots),
`darkside Ø` (DANGER_FORM both halves + the four invalid slots) and `instrument ⠸` (invalid + two chrome
families, now chrome only, i.e. B×B alphabet). **Four more rows LOSE their invalid family and stay**,
because they still carry a meaning and chrome: `corgi ▄` 6 → 5 families, `corgi ▀` 4 → 3,
`instrument ⠇` 4 → 3, `blueprint ━` 3 → 2. And `blueprint ├` is unchanged at 6 — it is `REQUIRED` at
seven chrome seats, which is decision A's territory and not this ruling's.

**The number the ruling is actually about — PAIRS of meanings sharing a cell, measured off the
declarations with the law's own reader and the four `DANGER_IS_THE_TOP_RUNG` exemptions held aside —
falls 8 → 0.** Run with HEAD's ten strings and darkside's `("Ø","Ø")` put back:

```
before   corgi      invalid × ladder  ▄   ·  invalid × required  ▀
         instrument invalid × ladder  ⠇
         swiss      danger  × invalid ╲
         darkside   danger  × invalid Ø
         blueprint  danger  × invalid ━   ·  invalid × ladder  ━  ·  invalid × required  ├
         ------------------------------------------------------------- 8 live, 4 exempt
after    (none)                                                     0 live, 4 exempt
```

The four exempt pairs are `naught ∙`, `corgi █`, `prism ⣿` and `blueprint ━` — the danger form as the
ladder's TOP rung, by name and with the citation each kit carries. **After this increment no language has
two meanings on one cell that the exemption does not cover.** That is the first time it has been true in
the corpus.

**`corgi ░` does not appear in the census, and the boundary says so in a number.** `░` is
`scrollbar.main[DEFAULT]`, and the scroll bar is outside the census's six controls — so the row shows up
in corgi's foot line as `... 1 further cells would collide if slider/bar/scrollbar were in the B set`
(was 0). The choice is the census's own declared boundary and it is now one number louder.

## 6. Frames changed — 6 `.txt` and their 6 `.svg`

`git status --short prototypes/components/` after `render.py`, and no others:

```
blueprint_S2   corgi_S2   darkside_S3   darkside_S4   instrument_S2   swiss_S2
12 files changed, 15 insertions(+), 15 deletions(-)
```

Read at the seat each move was made:

```
blueprint_S2   due├          ╱12/09/26··························╱      (was ━ … ━)
corgi_S2       due▀          ░░12/09/26··························░░    (was ▄▀ … ▀▄)
instrument_S2  due⠁          ⠶12/09/26⠶⠶⠶⠶…⠶⠶⠶                        (was ⠸ … ⠇)
swiss_S2       due•          ║12/09/26                                 (was ╲)
darkside_S3    ▬ ▚Delete all▞ ▬   7 tasks, not recoverable             (was ▬ ØDelete allØ ▬)
darkside_S4    │ ▮  ▚Delete▞  ▮   ▬   Cancel   ▬       │               (was ▮  ØDeleteØ  ▮)
```

**S2 is the only screen that renders an INVALID field** (`screens.py`'s one `INVALID` call site,
inc39 §6) and **no artefact in this repo draws a stepper at all** (inc51 §7) — which is why four kits
moved three declarations each and only one frame apiece moved. darkside is the exception in both
directions: its `DANGER_FORM` is what changed, so its two frames with a destructive control moved and its
S2 did not.

**Gallery: 0 of the 22.** `capture_languages.py` rewrote all 22 and none moved — the board draws no
invalid field and no destructive button.

**Of the eight frames whose gallery copies live in the skill** (spec §11: `instrument_S1`,
`industrial_S1`, `swiss_S1`, `solari_S1`, `industrial_S4`, `darkside_S4`, `solari_S2`, `instrument_S5`),
**one moved byte-wise: `darkside_S4`.** The skill is exported at the batch's close, not here.

## 7. Gates, verbatim

```
$ python -X utf8 -m pytest -q
1067 passed, 2 skipped, 4 warnings in 34.11s
```

**`1054 → 1067`, and the clipboard test is GREEN this run.** +12 is this increment's tests (ten
parametrised teeth arms, darkside's arm, the rune exclusion's arm); the thirteenth is
`tests/test_app.py::test_win_clipboard_roundtrip`, which was RED at `6970cac` and passed here — it drives
the real Windows clipboard through PowerShell and depends on nothing else on the desktop holding it
(spec §10.6). **It is environment-coupled in both directions: reported, not counted, not touched.**

```
$ python -X utf8 prototypes/verify_language.py                                        exit 0
  [PASS] sweep: ... and every `# nth-exempt:` claim is USED — an exemption no hit sits under is an
         exemption widened past its evidence  2 claimed, 0 unused
  [PASS] settle() keeps headroom under its bound  worst 4 of 40 over 155 captures
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
  -> 6 of the 66 moved

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
  TOTAL  36 -> 33
```

## 8. Risks

- **swiss and darkside are resolved in OPPOSITE directions, and both kits carry the same comment.**
  Swiss's `DANGER_FORM` says *"`field_form(INVALID)` is `╲ ╱` here, so a destructive control is bracketed
  by the same pair"*; darkside's says *"its own INVALID wall, the struck mark"*. Both name the field as
  the older declaration. The ruling moves darkside's DANGER and swiss's INVALID, and this increment
  followed the ruling's by-name revert list rather than generalising darkside's criterion. **If the
  operator prefers the criterion over the list, swiss's three lines revert and its `DANGER_FORM` moves
  instead** — one edit either way, and the teeth table would swap one row.
- **`║` against `┃` is COUNT against WEIGHT at 12 px, and the `.svg` carries no font metric.** Two thin
  strokes versus one thick one. It is the same argument inc49 made for `◎`/`◉` against `· o O` and it has
  the same unresolvable half (round-2 finding E2). Named, not settled.
- **`corgi ░` is the scroll shaft's cell.** corgi's own comment reads `░` as *"a segment present but not
  driven, which is what an LCD shows where NOTHING IS ON"* — which is a near neighbour of "refused" and
  not the same claim. The defence is that corgi already draws "dead" with `╳╳` at its disabled seats, so
  the two are distinguished inside this kit; the objection is that a reader who has learned `░` from the
  scroll bar has learned "empty", not "rejected".
- **`blueprint ╱` is also the sheet's HELD texture.** `hatch="╱"` draws blocked work on the board
  (*"held work is HATCHED, never coloured"*). No law reaches it — `hatch` is a token, not a `PART_GLYPHS`
  slot and not a meaning mark — which is the same limit spec §10.4 published for `▬`. So blueprint now
  says "blocked" and "refused" with one texture in two places the census cannot see. **Named, not fixed,
  and it is the weakest of this increment's four choices.**
- **`darkside ▚ ▞` are two cells this kit did not draw before.** Every other cell in its alphabet is at a
  knob, an opener, an indicator or a disabled mark, so a danger form taken from the existing alphabet
  would have failed the seat law it already passes at zero. Two new code points is the cost of that, and
  it is the only place in this increment where a mark is not already in its kit.
- **instrument's refused field has no rails.** `⠶⠶⠶` at 34 cells is one texture end to end, and this
  language's own comment calls a field *"a measured span"*. A span with no terminators is not a span; the
  defence is that a refused value has no extent to state. One line to reverse.
- **Six frames moved and none of them has been judged.** Same standing as every frame this programme has
  moved since inc37.

## 9. Found by looking, not fixed

- **`Kit.PART_GLYPHS["textfield.main"][INVALID] = "? ?"` is the base's line and nord's answer**, and it
  does NOT come from nord's knob (`▚`). It is kept on the ruling's own instruction because `?` is clean —
  but it means the base kit and nord say rejection with one mark at the field and a different one at the
  knob and the stepper. The positive clause would close that; §0a says why it was not made a law.
- **`instrument`, `industrial` and `prism` spell rejection with their DEFAULT walls and a changed
  PAPER**, so their invalid walls are chrome that means nothing — which passes this law and fails the
  ruling's positive clause. instrument's moved for a different reason (its closing rail was the error
  rung); industrial's `▐ ▌` and prism's `⣹ ⣏` did not, and are now the only two languages whose field
  walls do not change at all when the value is refused.
- **`blueprint ├` is still `REQUIRED` at seven chrome seats** and `corgi ▄`/`▀` are still `LEVELS[warn]`
  and `REQUIRED` at nine. Both are A×B rows, both are decision **A** (three languages that have never had
  an increment), both untouched.
- **The class docstring of `Blueprint` says its alphabet is TEN glyphs** and the kit draws
  `┣ ┫ ╞ ╡ ╎ ╏ ╪ ◉ ○ ●` besides. The docstring was already stale before this increment and this increment
  did not touch it; it is now one glyph staler in the sense that the hatch has a second job.

## 10. Pending — not this increment

- **inc53 (Ruling D)** — channels are count, weight, position and direction; diameter alone is not one.
- **inc54 (Ruling C1)** — the destructive default answer is a button that carries the knockout.
- **Decisions A, E, F, G, K2, K4, L1–L6, C2, C4–C7** — the operator's, untouched.

## 11. Suggested next task

**inc53 — Ruling D**, and the two cells it names: swiss's radio knob `●` beside `REQUIRED •` and
darkside's field leader `◦` beside `LEVELS["warn"] = o`.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1067 passed, 2 skipped, 0 failed` (§7). The environment-coupled
      `test_win_clipboard_roundtrip` was RED at `6970cac` and is GREEN here; reported, not counted, not
      touched. `verify_language.py` ALL PASSED exit 0. `render.py` 66/330/0, 6 of 66 moved.
      `matrix.py` 66 of 66. `capture_languages.py` 22 captures, 0 moved. `collision_census.py` self-check
      green, 36 → 33. The teeth were watched fail by hand on the real declaration and the output is
      pasted verbatim in §3.
- [x] **No secrets in code or output** — ten glyph-table entries, one `DANGER_FORM`, three test
      functions and one deleted exemption. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The watch-it-fail experiment used a byte copy of `language.py` and
      restored from it; `git diff --stat` is unchanged by it.
- [x] **File count within cap** — 2 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`); the 12 frame artefacts and the census table are written by gate
      scripts.
- [x] **Review packet attached** — this document.

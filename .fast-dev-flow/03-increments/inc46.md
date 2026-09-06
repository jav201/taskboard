# Increment 46 — instrument and swiss: the meaning leaves the opener, the indicator and the dead mark

**Batch:** `rework-3` · closes `spec.md` §9.4's `instrument_S2`, `instrument_S3`, `instrument_S4`,
`swiss_S3`, `swiss_S4` and half of `swiss_S2`
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`
— **3 source files**, plus 18 regenerated frame artefacts, 4 regenerated gallery artefacts, the census
table and this packet.

**Instrument's error rung `⠇` was opening the SAFE button and its obligation mark `⠁` was the DISABLED
switch, the dead track, the dead checkbox and the dead field's paper. Swiss's `━` was the switch's ON
indicator, its `•` was the focus ring on an irreversible button and the radio's knob, its `·` — the
LOWEST severity rung — opened `╲Delete all╱`, and four of its five controls still enclosed their content
in a language committed to "no boxes, at any width". All of it moved. The batch rule's second and third
named seats — the INDICATOR of a switch and a DISABLED mark — are now a law over all eleven languages,
with the six that still fail it counted by name. Census 53 → 48; instrument 8 → 7, swiss 9 → 5.**

---

## 1. instrument

### 1a. The rails mirror — `⠇` stops opening the safe button

`⠇` is three dots in the LEFT braille column, which is `LEVELS["error"]`'s own cell, and it was the
opening rail of every button and every text field. `instrument_S4` is what that renders as:

```
before   ⠧  ⠛Delete⠛  ⠼   ⠇   Cancel   ⠸
after    ⠼  ⠛Delete⠛  ⠧   ⠸   Cancel   ⠇
```

The rail takes **the column inc36 already chose for the gutter**, and inc36 wrote the reason down when it
chose it: `⠸` *"because `⠇` is the error rung and a neutral divider with the cell of the ladder would say
'rejected' to a greyscale reader"*. The same sentence applies to a button's first cell, more sharply,
because a divider is not a thing you press.

**And the ink now looks at the content.** `⠇ … ⠸` sets each rail's dots on its OUTER edge — `] [` in
braille, the shape inc39 spent a whole increment removing from the INVALID state. `⠸ … ⠇` faces them in.
Every state moved together, so the handedness inc39's law reads is kept and only its direction changed:

| state | before | after |
| --- | --- | --- |
| `button.main` DEFAULT / FOCUSED / ACTIVE | `⠇  ⠸` `⠧  ⠼` `⣇⣀⣀⣸` | `⠸  ⠇` `⠼  ⠧` `⣸⣀⣀⣇` |
| `textfield.main` DEFAULT / FOCUSED / EDITED / ACTIVE / INVALID | `⠇⠒⠸` `⠧⠒⠼` `⠧⠤⠼` `⣇⠒⣸` `⠇⠶⠸` | `⠸⠒⠇` `⠼⠒⠧` `⠼⠤⠧` `⣸⠒⣇` `⠸⠶⠇` |

**What the round meant by `instrument_S4`, verified.** The round called it *"severidad invertida"* because
`⠧ ⠛Delete⠛ ⠼` reads heavier than `⠇ Cancel ⠸`. Counted in dots, that reading is wrong: `⠧` and `⠼` are
FOUR dots and `⠇` and `⠸` are three, so the heavier button is the FOCUSED one — and the focused one **is**
the destructive one, which is correct. The danger form `⠛` is four dots against the ladder's three, so it
is heavier than the error rung too. **The defect in that frame was never the weight; it was that the only
severity cell on a destructive confirm sat on `Cancel`, at its opening rail.** That is what moved.

**`⠇` is still the CLOSER, and it is a declared cost.** The LEFT braille column *is* the severity ladder's
column — `⠂` one dot, `⠆` two, `⠇` three — so the only left-column rail that shares no cell with the
ladder is the four-dot `⡇`, and `⡇` is this language's caret, its own index mark. A field whose closing
rail is its caret is worse than one whose closing rail is a rung. The batch rule names the OPENER, the
switch indicator and the disabled mark; a closer is none of the three. Written at the seat, and listed in
§6 as still open.

### 1b. `⠁` is obligation and nothing else

`instrument_S3`, the round's criterion verbatim: *"mostrar `S2` y `S3` seguidas y preguntar qué significa
`⠁` — hay dos respuestas correctas y ninguna pista en pantalla."*

```
before   sync to remote            ⠄⠁⠁   (no remote configured)
after    sync to remote            ⠄⠈⠈   (no remote configured)
```

Five seats moved, and the replacements are rungs this language already spends on dead things:

| seat | before | after | why that rung |
| --- | --- | --- | --- |
| `checkbox.main` DISABLED | `⠁` | `⠄` | the same column's BOTTOM dot — the dead knob, the dead button's rails and the dead field's rails already wear it |
| `textfield.main` DISABLED | `⠄⠁⠄` | `⠄⠄⠄` | the whole field at the dead rung |
| `main` DISABLED (slider · bar · switch track) | `⠁` | `⠈` | **not** `⠄`: that is the dead KNOB, and `verify_language` holds a knob to differing in SHAPE from both the fill and the track. `⠈` is the rung this language's dead stepper track already wears (`⠈⠈`) |
| `scrollbar.main` DISABLED | `⠁` | `⠈` | `⠄` is this shaft's LIVE datum |
| `stepper.main` DEFAULT (the end stop) | `⠁⠁` | `⠒⠒` | the register's baseline, `main`'s own datum |

`⠁` now carries `REQUIRED` and nothing else. **Its census row is gone.**

---

## 2. swiss

### 2a. The switch's ON indicator stops being the error rung

`━` was `LEVELS["error"]` **and** the passed extent of every slider, bar and switch — the batch rule's
second named seat, exactly. It is now `▀`, the rule RISEN: the half-height weight this language already
spends on a pressed radio, one more step of the only ladder it owns.

**`▬` was the first answer and it was wrong for a measured reason.** `▬` over `─` is byte for byte
darkside's bar, and `verify_language`'s *"no two languages draw the same bar either"* went red on it. A
weight step that lands on another language's is not a weight step this language owns. The failure is
written at the seat so the next reader does not re-make the choice.

**`main` keeps `─`, and the exemption is by EXTENT rather than by silence.** A rung is ONE cell at the
head of a row, in a column that aligns — which is the whole of ruling 8 — and a track is a RUN of `n`
cells under a word. `DISCLOSE` is the same mark for the same reason. It is the weakest exemption in this
batch and it is written down at the declaration.

### 2b. One mark, one side — inc38's answer taken to the other four controls

*"No boxes — ALIGNMENT DOES THE DIVIDING"*, at any width. A wall is a PAIR: it is border-shaped because
it ENCLOSES. inc38 proved the third option on the button; this takes it to the rest. **The ladder is
unchanged** (`│ ┃ █ ┆`, the same four weights); the rule that led is kept and the rule that closed is not
set. Same cell counts, same one width per state, so no caller's row moves.

```
checkbox.main   │ │ ┃ ┃ █ █ ┆ ┆      ->  │    ┃    █    ┆
checkbox.knob   │▪│ ┃▪┃ █▮█ ┆·┆      ->  │▪   ┃▪   █▪   ┆▪
radio.main      ╵ ╵ ╹ ╹ ▀ ▀ ╎ ╎      ->  ╵    ╹    ▀    ╎
radio.knob      ╵•╵ ╹•╹ ▀●▀ ╎·╎      ->  ╵●   ╹●   ▀●   ╎●
textfield.main  │ │ ┃ ┃ ┃·┃ █ █ ╲ ╱ ┆ ┆  ->  │    ┃    ┃·   █    ╲    ┆
```

Three things moved with the walls:

- **`•` is obligation and nothing else.** The radio's knob read `•`, which is `REQUIRED` (inc35, *"the
  ladder's mark set solid"*), so a compulsory field and a chosen option were one cell — and `swiss_S4`
  put that same `•` on the focus ring of an irreversible button. The choice takes `●`, the solid round
  bullet this knob already wore when it was pressed. *Square marks a box, round marks a choice*,
  unchanged.
- **The CHECKED bit stops carrying the state.** `█▮█` and `┆·┆` spent `▮` (now `CUR`) and `·`
  (`LEVELS["info"]`) on the mark, and the second of those put a severity rung at a DISABLED seat. The
  square bullet is the checked bit in every state; the leading rule's weight is the control state.
- **The field's second wall was defended with a false claim, and the claim is now deleted rather than
  worked around.** The kit read: *"a value may fill every cell, so a walled-off field is the only place a
  full one can say DISABLED without colour"*. That is inc38's WALLS-OR-NOTHING dichotomy again. The
  LEADING rule says DISABLED whether the field is full or empty — it is the first cell of the row and no
  value can reach it — and what the closing rule carried was the field's EXTENT, which in a language
  whose divider is alignment is the next column's job.

**Swiss joined `HANDED_FIELDS`, and nothing decided that.** With the enclosure gone the field opens with a
rule and closes with air, so its opening and closing vocabularies differ and inc39's law can now fire on
it. The derivation noticed; the roster is where it had to be written down.

### 2c. The button's ladder leaves the marks that mean something

inc38 built `· • ●` and asserted that every cell appeared elsewhere in swiss's own declaration — right
instinct, wrong set: **two of the three rungs were declarations.** `swiss_S3` is what that renders as.

```
before   · ╲Delete all╱     7 tasks, not recoverable
after    ▫ ╲Delete all╱     7 tasks, not recoverable
```

The ladder is now **ONE shape at three weights**, and the shape is the square bullet this language already
declares for a box: `▫` hollow, `▪` inked, `■` filled, DISABLED still air. Neither `▫` nor `■` is a new
IDEA — they are `▪` at its two other weights — but they **are** new code points, and the rewritten law
records that trade instead of hiding it. inc38's own law (*no wall around a button at any width*, derived
from the codepoint rather than from a hand list) is untouched and still bites: all three rungs are
Geometric Shapes, not box-drawing and not block elements.

---

## 3. The law this increment adds

**`test_a_meaning_never_stands_at_a_disabled_or_indicator_seat[lang]`**, eleven parametrisations. A mark
that means something about the work — a severity rung, the `DANGER_FORM`, the `REQUIRED` mark — may not
stand at a DISABLED seat or at a switch's INDICATOR, over the same six controls the census reads.

**`CUR` is deliberately not in the set**, and the narrowing is named rather than left silent: a cursor
says where the reader is, not what the work is worth, and inc48's opener law names the same three
declarations.

**It is a MEASUREMENT, not a pass.** Six languages still fail it, and the count is asserted **per
language** so the roster can only move when somebody edits it — the same bargain `HANDED_FIELDS` makes one
screen up:

| language | count | what it is |
| --- | --- | --- |
| naught | 9 | `∙` is the switch's ON indicator and `◦` its dead one — both rungs of the count ladder. Naught has ONE round pixel at six charges and no unspent cell. **Open.** |
| corgi | 8 | the segment bank: `▄▄` ON, `▁▁` dead — `LEVELS["warn"]` and `LEVELS["info"]`. No increment in this batch. **Open.** |
| prism | 8 | `⣿` ON, `⣤` dead — the top two rungs. **Open.** |
| solari | 6 | `▁` is `REQUIRED` and the switch's indicator. **inc47.** |
| blueprint | 8 | `╌` is `LEVELS["warn"]` and this language's whole DISABLED vocabulary — five parts wear it. **Open.** |
| instrument · swiss · industrial · nord · darkside · ledger | **0** | and two of those six were not zero before this increment |

Its teeth are a separate test with two arms, because five of the eleven parametrisations assert a
NON-ZERO count and that is the shape of assertion that rots into a snapshot if nobody watches it fire.
Arm one restores instrument's dead checkbox to `⠁`; arm two restores swiss's switch indicator to `━`.
Each must move that language's count off zero **and name the part and the mark**.

Three tests were rewritten rather than deleted: `FLIPPED_INVALID["instrument"]` is now `⠇⠶⠸` (the rails
turned, so the exchanged form is the mirror of what it was — the defect being restored is the same
defect, only its spelling moved), `HANDED_FIELDS` gained swiss, and
`test_the_swiss_buttons_ladder_is_made_of_marks_it_already_spends` became
`test_the_swiss_buttons_ladder_is_one_shape_at_three_weights`.

`prototypes/collision_census.py`'s roster marks `instrument ⠁` **closed by inc46**; three of the round's
five are now asserted closed and two still come back live.

---

## 4. Census delta

```
language      HEAD  inc45  inc46      live A x A (exemptions subtracted)
naught           3      5      5      0
corgi            5      5      5      2   ▄ INVALID+severity · ▀ INVALID+REQUIRED
instrument       8      8      7      1   ⠇ INVALID+severity   (the closer; §1a)
swiss            8      9      5      0
industrial       5      4      4      1   ▐ INVALID+REQUIRED   (inc48)
nord             5      4      4      0
darkside         3      3      3      0
prism            5      5      5      1   ⡀ INVALID+REQUIRED
ledger           4      2      2      0
solari           3      3      3      0
blueprint        5      5      5      3   ├ · ━
TOTAL           54     53     48          15 -> 8 -> 8
```

`instrument` loses `⠁` outright; `swiss` loses `•`, `━`, `▮` and one more — its `▮` row went because the
checkbox's ACTIVE mark stopped being the cursor cell, which nobody set out to fix and the census caught.
**The live meaning×meaning count does not move**, and that is the honest reading: this increment is about
the batch rule's SECOND clause (a meaning at a named seat), not its first.

---

## 5. Artefacts changed

**9 `.txt` and their 9 `.svg`:** `instrument_S2` `instrument_S3` `instrument_S4` `instrument_S6`,
`swiss_S2` `swiss_S3` `swiss_S4` `swiss_S5` `swiss_S6`.

Instrument S2/S3/S4/S6 and swiss S2/S3/S4/S6 were expected. **`swiss_S5` is the one to explain**, and it
is one row:

```
-  EVENTS/S    ━━━━━━━───────  5
+  EVENTS/S    ▀▀▀▀▀▀▀───────  5
```

`readbar` draws the passed extent from `indicator`, so the monitor's load bar moved with the switch. That
is the mechanism working: the switch's ON segment and the bar's passed run are ONE declaration in this
kit, which is why fixing the switch fixed the bar.

**4 gallery artefacts:** `gallery_instrument.{txt,svg}` and `gallery_swiss.{txt,svg}` — the widget sheets,
which is where the control changes actually live. The other 18 gallery files are byte-identical.

**None of the eight frames whose gallery copies live in the skill moved this increment**
(`instrument_S1`, `industrial_S1`, `swiss_S1`, `solari_S1`, `industrial_S4`, `darkside_S4`, `solari_S2`,
`instrument_S5` — all unchanged). The two gallery BOARD sheets that did move are a separate set and are
re-exported by `export_to_skill.py` at the close of inc48.

---

## 6. Gates, verbatim — AND ONE RED THAT IS NOT MINE

```
$ python -X utf8 -m pytest -q
1 failed, 1028 passed, 2 skipped, 4 warnings in 35.07s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**1016 → 1028**: eleven parametrisations of the named-seat law plus its teeth test. The red is the
environment-coupled clipboard test (spec §10.6), red at HEAD before this batch began.

```
$ python -X utf8 prototypes/verify_language.py                                        exit 0
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)  worst 4 of 40 over 155 captures
ALL PASSED
```

**It was red twice on the way, and both reds are in the record above**: instrument's dead track taking
`⠄` collided with its dead KNOB (*"the disabled knob differs in SHAPE from both the fill and the track"*,
three failures), and swiss's `▬` indicator made its bar byte-identical to darkside's (*"no two languages
draw the same bar either"*). Both were fixed at the declaration and both reasons are written at the seat.

```
$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                      exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                                      exit 0
  22 grids identical across two PROCESSES
  22 captures -> prototypes\gallery
  no two boards identical
  -> 4 of the 22 moved: gallery_instrument.{txt,svg}, gallery_swiss.{txt,svg}

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  2 of the 5 collisions the round found by hand still come back out of
              the census; 3 are asserted CLOSED and cannot grow back
  TOTAL  53 -> 48
```

---

## 7. Risks

- **Swiss's text field now closes with AIR at every width.** A full value runs to the edge of its
  budget with nothing marking where the budget ended. The argument is the language's own — alignment is
  the divider — but this is the change in this batch most likely to be judged wrong at a glance, and it
  is one dictionary entry to reverse.
- **`▫` and `■` are two new code points in the language that draws fewest.** They are `▪` hollow and `▪`
  full, so the SHAPE is not new, but swiss's alphabet went from four marks to six and the round's
  arithmetic finding (*"su alfabeto tiene cuatro celdas y sus seis pantallas necesitan distinguir por lo
  menos once cosas"*) is answered partly by widening the alphabet rather than only by spending it better.
  Said plainly because it is the kind of answer that should be visible.
- **`⠇` still closes every instrument button and field** (§1a). The batch rule permits it; a reader who
  scans right-to-left does not care about the rule.
- **Swiss's disabled button is still air**, so `swiss_S2`'s finding — *"`Save` (DISABLED) is
  typographically a caption"* — is only half answered: the four controls beside it no longer have walls,
  so the screen is consistent, but the dead control still has no mark. There is nothing in this alphabet
  lighter than `▫` that is not a dashed rule (the shape being given up) or `·` (a severity rung, which
  the new law forbids at exactly this seat). **Open, and named in §8.**
- **The named-seat law asserts five non-zero counts.** That is a snapshot shape, and it is defended by a
  teeth test rather than by hope. If a later increment fixes solari and does not edit the roster, the
  suite goes red — which is the point, and which will feel like a false positive to whoever hits it.

---

## 8. Pending — not fixed here

- **`solari ▁` and `nord_S1`** — inc47. Solari's 6 in the named-seat roster goes with it.
- **`industrial ▐`, the caption-as-button in `industrial_S3` / `darkside_S3`, `darkside_S1`,
  `darkside_S6`, and the opener law over all eleven** — inc48.
- **`swiss_S2`'s disabled button reads as a caption** (§7). Open.
- **`swiss_S4`'s modal opens with a rule and never closes** — the round's second objection on that frame.
  Untouched; it is a composition finding in `overlay_instead`, not a glyph.
- **`instrument ⠇` closes every button and field** (§1a). Declared cost.
- **`instrument ⠛` is the `DANGER_FORM` and the FOCUSED checkbox** — the census row the round named in
  §10.4 and the one finding on `instrument_S4` this increment did not touch. Not an opener, not an
  indicator, not a disabled mark, so no law in this batch reaches it.
- **naught, corgi, prism and blueprint fail the named-seat law**, 33 seats between them (§3). None has an
  increment in this batch.
- **`Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`** — inc39's unfixed defect (spec §9.5).
- **`test_win_clipboard_roundtrip` is environment-coupled** (spec §10.6).

## 9. Suggested next task

inc47 — solari and nord. Solari's `▁` is `REQUIRED`, the switch indicator and eighteen chrome seats, and
it is the only census row of the sixteen with an exact count attached (`solari_S2`: *"`▁` aparece más de
sesenta veces en esta pantalla y dos de ellas son la respuesta"*), which makes it the one finding in the
batch that can be closed with a before/after MEASUREMENT rather than with a frame.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1028 passed, 2 skipped, 1 failed`; the
      failure is `test_win_clipboard_roundtrip`, red at HEAD before this batch (§6).
      `verify_language.py` **ALL PASSED** exit 0 — after two named reds that were fixed at the
      declaration, both recorded in §6. `render.py` 66 frames / 330 pairs / 0 hand-drawn. `matrix.py`
      66 of 66. `capture_languages.py` 22 captures, 4 moved and named. `collision_census.py` self-check
      green, 53 → 48.
- [x] **No secrets in code or output** — glyph tables and rendered frames only. No network, no new
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force. The commit names its files explicitly.
- [x] **File count within cap** — 3 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`, `prototypes/collision_census.py`); everything else in the commit is
      regenerated by a gate script.
- [x] **Review packet attached** — this document.

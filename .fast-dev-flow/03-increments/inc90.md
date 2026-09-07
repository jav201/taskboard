# inc90 — L10, enumerated: twenty rows on nine drawings, and the batch close

Batch `rework-9`, increment 4 of 4.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation):

- **Declared seat by seat, not by character:** the declared-seat derivation intersects the mark with
  the seat its contract method paints (`log_row`'s rung column, not any cell with the same
  character); prose never counts.
- **Cursors are marks:** the three cursors in `accent` (instrument `⣿` 2.94, swiss `▮` 2.57,
  industrial `▶` 2.97) obey Q1's effective clause; fix by the smallest hue-preserving lightness step
  of `accent`, and re-run the match-tier law (inc73) since `accent` is a match ink in some kits: both
  must hold.
- **Drawing problems are fixed by drawing:** corgi's invalid wall `░` (1.44 in ink, a dither) takes
  the heavy shade `▓` (panel register, inc67), and ledger's warn rung `*` (2.86 on light paper) takes
  a heavier printer's mark by area from ledger's own alphabet (`¶`, `§`, `※` or `**`'s sibling; cite
  #9 and keep error distinct), both judged by Q1 at the seat.
- **Both-clause seats move by area** (inc82's kind): the eight seats failing coverage AND contrast
  take a bigger glyph from their language's alphabet; `naught ◦` (13.5 %) is among them and gets no
  eye exemption.
- **naught_S2 L10:** the 12 homoglyph rows and 8 state rows on naught's form are fixed by SHAPE and
  COUNT (the lattice counts, the pixel charges: inc61), so the form's marks stop resting on one
  drawing.
- **inc84 §6 correction:** the packet's claim "gallery 30–51 none changed" was read off
  `prototypes/gallery/` (boards), not the component grids; entries 35 and 36 did change. Correct the
  packet in place with a dated note, never silently.

This increment is the **fifth**, and the batch close.

## §1 — cause

L10 is the round's oldest open rework. Round five looked at it on the raster and confirmed it *"sin
margen"*: the radio row (`◌ low  ◌ norm  ⊚ high`) and the tag row (`◦ api  ◉ ui  ◉ urgent`) are, in
the PNG, **two rows of little circles, one hollow and one full in both**. The criterion has not
changed in three rounds — *cover the label column and say which row is a single choice and which are
independent boxes* — and it has had **no answer** in any of them. Round five added an axis L10 does
not name: **`⊛` (the obligation) reads as `○` (the unchosen well)**, on the same screen, three rows
apart.

`STATES_TOLD_APART_BY_SIZE`'s own note already said what closing it would take: *"a second channel
for this alphabet, which is a language-level increment."*

## §2 — mechanism

**The ruling names two channels and this language can spend neither. That is the finding, and this
increment's whole job is to say it with numbers instead of with a sentence.**

### Twenty rows rest on nine drawings

```
three solid dots at three sizes          ⋅  ∙  ●
six ringed things at six diameters/fills ◦  ○  ◎  ◉  ⊙  ⊛
```

Fourteen distinct pairs carry all twenty rows — the census's 12 homoglyph rows and the 8 state rows —
and every one is recorded with its XOR distance as a percentage of the cell. **The tightest is `○`
against `◉` at 5.82 %**, which is `stepper.step` FOCUSED against ACTIVE, and it is within a point of
the tightest pair in the whole corpus (`ledger † ‡` at 4.87 %) — a pair three rounds argued about and
inc76 built a raster to settle. **This is not a slip in a table. It is this language's founding rule
("the pixel is ROUND … everything here is round") measured at 9×19 px.**

### The three channels, and why each is closed

| channel | why the form cannot leave on it |
| --- | --- |
| **count** — *the lattice counts* | **RESERVED.** inc61's rule: `NA.ON`, the lit lattice dot, belongs to the count and to nothing else, and **no control seat draws it**. That rule exists because the lit dot IS `DANGER_FORM` and two severity rungs — inc61 found `naught_S3` rendering every live switch as `∙∙◉` twelve rows above `◦ ∙Delete all∙ ◦`. A control that counted would be spelling the error rung. |
| **charge** — *the pixel charges* | **ALREADY SPENT, and it is where these rows come from.** `⋅ ◦ ∙ ◉ ●` and the ring family `◌ ○ ◑ ◍ ◎` are one ramp read at nine settings, so a pair told apart by charge is told apart by DIAMETER AND FILL — the pair of channels ruling D refuses as a sole answer. |
| **interior** — *the circled operator's inner mark* | **THE ONE REAL SECOND CHANNEL, and it is outside the face.** `⊖ ⊙ ⊚ ⊗ ⊛` tell apart by what is inside one outline, not by diameter — but **three of its five members are three of the four cells `raster.py` routes through Segoe UI Symbol by name.** Widening it means adding codepoints to `FALLBACK_CELLS`, which is a new alphabet for a language. |

**So the refusal is not "we could not think of anything".** It is: the ruling's own two channels are
one reserved and one exhausted, the third exists and lies outside the measured face, and the move that
would use it is a language-level change that needs a round.

## §3 — law

| law | what it binds |
| --- | --- |
| `test_l10_is_twenty_rows_on_nine_drawings_and_names_why_each_stands` | (a) **the two counts are read LIVE** — 12 from `collision_census.homoglyph_rows("naught")` and 8 from `states_without_a_channel("naught")`, neither copied; (b) every pair still measures the recorded distance to 2 dp, through the face the corpus is rastered on **including the fallback** — two of the nine drawings are only there; (c) the roster **covers both rosters in both directions**: every pair the census reports and every pair the state rows rest on is here and nothing else is; (d) both channels this alphabet spends are used and the third appears in no row at all; (e) **nine drawings**, asserted |
| `test_the_two_channels_the_l10_ruling_names_are_both_blocked` | **the count is reserved** — every seat of the six components a form actually operates is walked and none draws `NA.ON`, which is inc61's rule executed rather than quoted; **the charge is spent** — the nine drawings are drawn at ≥ 24 declared seats between them, so there is no setting of the ramp left that is not already saying something |

`_cov_any` extends `_cov` to the four cells the primary face does not carry, by reading the fallback
face **and its per-cell size** off the sidecar — the same numbers `raster.py` uses and inc76's
declaration law already pins, so it inherits that check rather than adding a second one. `_cov`'s own
declared limitation ("the primary face only") is left standing; this is the one section that has to
measure `⊛` and `⋅`, because they are two of the nine.

## §4 — teeth

`test_the_l10_roster_bites_in_both_directions` — **three arms, and they are the shape
`BELOW_THE_FLOOR`'s already have**, because this roster makes the same kind of claim: it is a RECORD
of what the corpus does, and a record that cannot go stale is a comment.

1. **drop a pair** (`○ ◉`, the tightest) and the coverage clause fires;
2. **add a pair the corpus does not draw** (`◑ ◍`) and it fires the other way — a roster that could
   only be too small is half a roster;
3. **let one control seat draw the lit lattice dot** — `checkbox.main[DEFAULT] = NA.ON` — and the
   count clause fires. **That is inc61's rule executed rather than quoted**, and it is the arm that
   matters: the refusal's first reason is a rule, and a rule nobody runs is a sentence.

## §5 — what was found by looking

**1. Nine drawings carry twenty rows, and nobody had counted them.** The census reports rows and the
state roster reports rows; neither reports the CELLS underneath, so L10 had been discussed for three
rounds as "twelve rows and eight rows" — a number that sounds like twenty problems. It is nine
drawings, and once that is written down the refusal writes itself: nine cells of one shape family, in
a language whose founding rule is that everything is that shape.

**2. `○` against `◉` at 5.82 % is the second-tightest pair in the corpus and it is a STATE pair, not
a homoglyph row.** The census does not see it — `stepper.step` FOCUSED and ACTIVE are two states of
one part, which `states_without_a_channel` reports and `homoglyph_rows` does not. Two instruments,
two rosters, and the tightest thing either of them holds was in the one nobody was measuring
distances on.

**3. The `count` channel appears in no row of the roster, and that is the finding rather than a gap.**
The first draft of the law asserted all three channels were USED — the standard non-vacuity arm — and
it went red. It should have: `count` is not a channel any of these rows is on **or could move to**,
because inc61 reserved it outright. The law now asserts `used == {"charge", "interior"}` and
`used < set(L10_CHANNELS)`, and the third channel's entry carries the argument for why it is empty.

**4. `indicator` draws the lit dot and it is not a violation.** The first walk of "no control seat
draws `NA.ON`" went red on the slider's and the bar's fill — which is the count, by inc61's own
sentence (*"quantity is a row of discrete LIT DOTS"*). The clause is about the six components a form
OPERATES, and the exception is written into the law rather than filtered out of it.

**5. The batch's four increments moved the census twice in opposite directions and no law pins the
total.** 27 → 26 (inc88, a collision closed by a drawing chosen for legibility) → 23 (inc89, three
more closed the same way). Recorded in `spec.md` §24.7 and handed back: a number that has moved twice
in one batch and is asserted nowhere is a number the next batch will move without noticing.

## §6 — files and frames

| file | change |
| --- | --- |
| `tests/test_components.py` | `_cov_any` / `_xor_any`, `L10_CHANNELS`, `L10_RESTS_ON_ONE_DRAWING` (14 pairs), `L10_ROWS`; two laws and one tooth in three arms |
| `.fast-dev-flow/spec.md` | **§24** — the batch record: the rulings, the four increments, twelve findings, the floor batch to batch, the laws, the refusals, the artefacts and the status |

**Frames changed: ZERO.** `render.py`, `raster.py`, `second_width.py` and `legibility.py` were all
re-run and `git status --porcelain` is empty on `prototypes/`. A roster is not a drawing.

**Gallery 30–51: none changed byte-wise**, read off `prototypes/components/`.
`capture_languages.py` was not run: no board changed.

## §7 — deviations, named

- **L10 is not redrawn, and this packet is the argument for why not.** The ruling asks for SHAPE and
  COUNT; §2 shows the count is reserved by a rule with teeth and the shape channel that would work is
  outside the measured face. What the increment delivers instead is the enumeration — which is what a
  round needs to rule on the question properly, and what three rounds of prose did not produce.
- **`naught_S4` is untouched.** The `DANGER_FORM` frame is round five's other confirmed rework for
  this kit and it is in no brief, this batch's included.
- **`⊛` reading as `○` is in the roster and is not separately fixed.** It is row two by tightness
  (10.85 %) and it wants the same cell every other row wants.
- **The three naught rows still under the floor are not this increment's**, and inc89's packet says
  why. They are one alphabet's ceiling.

## §8 — gates

```
pytest -q                1498 passed, 1 failed, 2 skipped, 26 warnings in 49.16s
                         (inc89 1496 -> 1499, +3: 2 laws + 1 tooth.  The one
                          failure is test_win_clipboard_roundtrip,
                          environment-coupled, reported and not counted)
verify_language.py       ALL PASSED                                     exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn    exit 0
                         -- and nothing changed on disk
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                          exit 0
legibility.py            876 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct     exit 0
matrix.py                refusals [] for all eleven                      exit 0
collision_census.py      TOTAL 23 · homoglyph rows 22 · both self-checks
                         green · zero collisions: darkside               exit 0
capture_languages.py     not run: no board changed
export_to_skill.py       11 languages round-trip · every token, doc and
                         family verified · captures 6 WRITTEN / 60 already
                         identical (the six gallery artefacts inc88 moved) ·
                         SURFACES.md 11 postures.  Re-run: 0 written /
                         66 already identical.                           exit 0
```

The skill repo was **not** committed.

`BELOW_THE_FLOOR`, old → new: **4 → 4, unchanged.** This increment moves no seat, and that is what its
§2 is about.

**BELOW_THE_FLOOR across the batch: 18 → 4**, and every remaining row measures exactly 14.0 %:

```
naught      severity ∙ #f5f5f5  COV   14.0%   9.66   the disc
naught      severity ◦ #f5f5f5  COV   14.0%   5.68   the ring; inc89 §2
naught      danger   ∙ #f5f5f5  COV   14.0%   9.66   DANGER_FORM, in no brief
swiss       required • #f4f4f4  COV   14.0%   9.13   exempt by EYE (inc86)
```

## §9 — pending / next

Batch `rework-9` is closed; `spec.md` §24 is the record. What goes back to the round:

- **naught's three 14.0 % rows and L10** — one alphabet's ceiling, wanting a cell the language does
  not have. The path exists and is named: the circled operator's interior mark, which needs
  `FALLBACK_CELLS` widened and therefore a round.
- **the slider's and the stepper's invalid marks** — no contract call, therefore unmeasured at their
  own seat (inc87 §5.2).
- **the census total** — moved twice in this batch, pinned by no law (§5.5).
- **`naught_S4`** — the `DANGER_FORM` frame, still in no brief.

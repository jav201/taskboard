# Increment 64 — prism ticks its boxes forward and fills its bars one way

**Batch:** `rework-6a`, increment 2 of 4 · **L8** (the inverted checkbox) and **L9** (the bar that
fills two ways), both new in `PROTOTYPE-inheritors-3.md` and both prism's.
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 4 regenerated
component artefacts (`prism_S1`, `prism_S2`, `.txt` and `.svg`), 4 regenerated gallery artefacts
(`board_prism`, `gallery_prism`) and this packet.

**`prism_S2` row 11 rendered the fixture's two TICKED tags as empty boxes and its one clear tag with a
mark inside it, and `prism_S1` row 13 drew a 44 % bar with twelve LIGHT cells of twenty-seven so the
picture reads 56 %.** Both are inversions, both are prism's, and neither had an instrument that could
see it: no law in this repo had ever compared two states of one part (K4), and the meter, the slider and
the bar are all outside `PART_GLYPHS` and outside the census's set B (K5, spec §15.4). Two centres
swapped and one bitmap loop flipped; two laws added, over all eleven, with their teeth on the real
declarations. Suite 1123 → 1147. Census 25, homoglyph rows 1 — unchanged.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **E4:** the exporter reads the kit's declared `ground` and `ink`; it never infers them from frequency.

> **F, amended:** the band never covers a gate HEADER row, of any gate; it covers task rows of the first
> gate the confirm does not name, below that gate's header, and goes to the foot of the schedule when no
> such rows exist. A frame must never show a task under a gate it does not belong to.

> **G vs ruling 10:** on S4 the fixture mood is calm; G applies to S2 only. Recorded, no code.

> **inc60 info to air:** doctrine for blueprint and ledger (a line-type ladder where absence is the calm
> state, LANGUAGES.md §11 and #9). Recorded, no code.

> **C, follow-through:** the channel C freed on swiss gets filled: the invalid text field has a wall,
> paper and a closer from swiss's own alphabet.

The brief for this increment:

> `prism_S2`'s checkbox reads `⠿⠀⠿` checked and `⠿⠉⠿` unchecked; inc59 moved both tables. Fix so
> checked is the fuller cell, per prism's ember doctrine (fuller = more). Property test: for every
> language, the checked knob's ink count … is greater than or equal to the unchecked, or the language
> declares the pair explicitly with a citation. `prism_S1`'s progress bar fills light while S3/S5 fill
> heavy: find the two code paths, unify to one declaration, and add a law that a language's fill
> direction is one declaration used everywhere.

## 1. The frames, read before anything was written

```
prism_S2  f11   tags          ⠿⠉⠿ api  ⠿⠀⠿ ui  ⠿⠀⠿ urgent
prism_S1  f13   ⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  44%
prism_S3  f16   row density   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70
prism_S5  f04   EVENTS/S      ⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀ 5
```

The fixture ticks `ui` and `urgent` and leaves `api` clear. Measured on the other ten, which all draw it
the same way and the opposite way round from prism:

```
darkside   ( ) api  (◎) ui  (◎) urgent          corgi   ▒▒ -- api  ▓▓ ON ui
naught     ◦ api  ◉ ui  ◉ urgent                ledger  │ │ open api  │×│ posted ui
```

**Ten of eleven add ink when a box is ticked; prism took it away.** Measured on the box alone, at all
four control states, before anything moved:

```
prism  default  ⠿⠉⠿ 1.75 / ⠿⠀⠿ 1.50   focused ⣷⠉⣷ 2.00 / ⣷⠀⣷ 1.75
       active   ⣾⠉⣾ 2.00 / ⣾⠀⣾ 1.75   disabled ⠄⠄⠄ 0.38 / ⠄⠀⠄ 0.25
```

And the fill direction, read by rendering each widget at its floor and its ceiling and taking the track's
own cell from each:

```
                meter            slider           readbar
prism      ⣿ -> ⣀   BACKWARDS   ⣀ -> ⣿          ⣀ -> ⣿
the other ten           every one of them light -> heavy
```

## 2. Cause and mechanism — L8

**Cause.** `Prism.PART_GLYPHS` carries the box in two tables: `checkbox.main` is the box body, drawn
when the bit is clear, and `checkbox.knob` is the box with the mark, drawn when it is set. The walls are
identical between them in every state by construction ("so the box survives the mark instead of being
redrawn by it") and **only the centre cell distinguishes the two**. The centres were the wrong way round:

```
before   checkbox.main  ⠿⠉⠿  (a mark in the box)      checkbox.knob  ⠿⠀⠿  (the empty well)
after    checkbox.main  ⠿⠀⠿                            checkbox.knob  ⠿⠉⠿
```

inc59 moved **both** tables in one increment — off `⣿`/`⣀`, which were `DANGER_FORM` and
`LEVELS["info"]`, onto cells read from the top — and did not notice it had preserved an inversion,
because nothing in this repo compares two states of one part. That is K4, named open since round one,
and this is the first law here that closes any of it.

**Mechanism.** The two centres are swapped and nothing else. The walls, the four states and inc59's
climbing ladder are untouched; the kit's comment stops claiming the box is "a field with a hole burned in
it" and says what it now draws, with the frame that asked for the change quoted in it.

## 3. Cause and mechanism — L9

**Cause: two code paths, and they disagreed.**

- `Kit.slider` / `Kit.readbar` go through `component_cells`, which spends `PART_GLYPHS["indicator"]`
  (`⣿`) on the value and `PART_GLYPHS["main"]` (`⣀`) on the rest. **Heavy is more.**
- `Kit.meter` dispatches on `THEMES[lang]["meter"]`; prism is the only kit with `meter="ember"`, and
  `_meter_ember` composes its own braille bitmap: `if x < burnt: ash.fill_to(x, 1) else:
  live.fill_to(x, DOT_ROWS)`. **The DONE side was the ash.**

The ember's docstring called that "a field being CONSUMED" and meant it. It is a coherent idea and it
loses to two facts: the same language fills the other way at two other widgets in the same sweep, and a
bar labelled `44%` whose first twelve cells of twenty-seven are the light one is a bar that reads 56 %.

**Mechanism.** The loop is flipped and `burnt` is renamed `alight`; the emit loop's tie-break at the
frontier cell moves from ash-wins to fire-wins, so the boundary is where the field ends rather than one
cell short of it. **Everything the mechanism exists for is untouched** — the half-cell frontier, the
field-or-figure rule, the shape channel that survives greyscale:

```
  0 ⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀   0%
 44 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀  44%
 47 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀  47%      <- the half cell, still there
 50 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀  50%
100 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ 100%
```

`meter="ember"` is declared by **one** language (`themes.py:322`), so this reaches prism and nothing else.

## 4. The two laws

**`test_a_ticked_box_is_never_lighter_than_an_empty_one`**, over the eleven, at four control states.
It compares **the box, not the control** (`checkbox_knob`), and **only the cells that move**:

- the box without the word — three kits spend a word at `check_label` (`ON`/`--`, `posted`/`open`,
  `ON `/`OFF`), and counting it makes the law measure how long the English is. Measured: a whole-control
  reading calls solari's ACTIVE checkbox **lighter** when ticked, because `OFF` is a letter longer than
  `ON `, while the box itself goes `▁·▁` → `▁█▁`;
- only the moved cells, because the walls are identical between the two tables in every language, so
  comparing whole runs would have meant weighing thirty-seven wall glyphs to learn nothing;
- `>=`, not `>`: naught ticks by changing a mark's SHAPE at the same weight (`◦`→`◉`, `○`→`●`,
  `◌`→`◍`), which is ruling D's first channel spent honestly.

**`test_a_languages_fill_direction_is_one_declaration`**, over the eleven, at three widgets — the meter
(S1), the slider (S3) and the readbar (S5). Each is rendered at floor and ceiling, the track's own cell
is taken from each (`track_cell`: the commonest non-ASCII glyph, because the head of these runs is a
knob or a bracket and appears once while the track appears ten to twenty-five times), and the ceiling's
cell must be **strictly** fuller than the floor's. Strict here and `>=` at the box, for a stated reason:
a checkbox may tick by shape at equal weight, a QUANTITY may not, because the reader is judging an amount
from a length.

**How a cell is weighed.** `cell_ink` computes braille (dots over eight) and the block elements
(U+2580–U+259F, declared coverage) and **declares** eight more — `·` `◦` `∙` `─` `━` `▪` `▬` `▫` —
each a pair the corpus draws side by side. Anything else returns **`None`, a refusal and not a zero**: a
law that scored an unknown glyph as empty would pass every language that moved to one. The box law uses
`mark_ink`, which scores an unknown as a FULL mark — the direction that makes it harder to pass, since
an unchecked unknown then counts as the fullest thing on the page.

**The direction law's two skips are a written roster**, `RAMPLESS_METERS`: solari (`meter="odometer"`,
"QUANTITY IS DIGITS, never a bar") and blueprint (`meter="dimension"`). Their floor and ceiling cells
are a digit and a terminator, which are not fill and never will be. The law **asserts they are still
unweighable** — a third language arriving there, or one of these two growing a ramp, goes red.

## 5. Teeth

**`test_the_ticked_box_law_bites_on_the_frame_it_was_written_for`** puts inc59's two centres back on
`Prism.PART_GLYPHS` and sweeps all eleven: the red list is **exactly `prism` at all four states and
nothing else**, asserted as a list and as a set of states, then the shipped declaration is asserted green
in both directions.

**`test_the_fill_direction_law_bites_and_its_roster_is_not_vacuous`** re-installs the pre-inc64
`_meter_ember` into `LG.METERS["ember"]` — the whole loop, ash-first — and asserts the track cells come
back `(⣿, ⣀)`, floor fuller than ceiling, which is the law red. It then asserts the shipped pair is
`(⣀, ⣿)` and re-derives `RAMPLESS_METERS` from the eleven rather than trusting the constant.

Both are on the real declarations and the real registry, monkeypatched back to the previous increment's
state, not on hand-built strings.

## 6. Frames changed

| frame | what moved |
|---|---|
| `prism_S1` `.txt` `.svg` | row 13: `⣀`×12 `⣿`×15 → `⣿`×12 `⣀`×15, still `44%` |
| `prism_S2` `.txt` `.svg` | row 11: `⠿⠉⠿ api  ⠿⠀⠿ ui  ⠿⠀⠿ urgent` → `⠿⠀⠿ api  ⠿⠉⠿ ui  ⠿⠉⠿ urgent` |
| `board_prism` `.txt` `.svg` | the board meter, 13 %: light-first → heavy-first, 108 cells |
| `gallery_prism` `.txt` `.svg` | the component sheet's four checkbox rows, both columns, all four states |

**Nothing else moved, and the reason is checkable:** `meter="ember"` is one language's declaration and
`Prism.PART_GLYPHS` is one language's table. `prism_S3` and `prism_S5` were already heavy-first and are
byte-identical — they are the two frames the objection compared against, and they did not have to move
for the language to agree with itself.

**Gallery 30–51 in the skill:** untouched here; `export_to_skill.py` runs at the close of the batch.

## 7. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1147 passed, 2 skipped, 4 warnings in 34.39s

$ python -X utf8 prototypes/verify_language.py
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)  worst 4 of 40 over 155 captures

ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ python -X utf8 prototypes/components/matrix.py
  66 of 66 · refusals [] for all eleven                 (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       25
TOTAL homoglyph rows             1
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  re-sweeping in a fresh process to check reproducibility...
  22 grids identical across two PROCESSES

  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)

$ git status --porcelain prototypes/gallery/
 M prototypes/gallery/board_prism.svg
 M prototypes/gallery/board_prism.txt
 M prototypes/gallery/gallery_prism.svg
 M prototypes/gallery/gallery_prism.txt
```

Suite **1123 → 1147** (+11 box arms, +11 direction arms, +2 teeth). Census **25**, homoglyph rows **1**:
the swap is a permutation of two cells prism already spent, so no cell entered or left the language.

## 8. Risks

1. **`_meter_ember`'s doctrine changed, not just its arithmetic.** The kit still says quantity is a field
   at half-cell precision; it no longer says the field is being consumed. That sentence is rewritten in
   the code, in the increment that rewrote the behaviour, and the reason is in the comment. Anyone who
   preferred the consumption reading is disagreeing with L9, not with this implementation.
2. **`CELL_INK`'s eight declared weights are ORDINAL, not photometric.** They are declared, not measured,
   because the artefacts carry no font metric (E2). Every one of them is only ever asked "which of these
   two is fuller", and each is a pair the corpus draws adjacent.
3. **`track_cell` reads the commonest non-ASCII glyph.** A widget whose track were shorter than its
   chrome would confuse it. Measured across the 33 renderings: the track runs 10–25 cells and every
   knob, bracket and terminator appears once or twice.
4. **The box law reaches only what `component_cells` composes.** A language that drew a checkbox by hand
   in `screens.py` would be invisible to it — as `matrix.py` reports, none does (0 hand-drawn elements
   over 66 frames).

## 9. Found by looking, not fixed

- **K5 is still the roof over both of these.** The fix landed, but the reason both defects lived for a
  whole batch is that no census and no roster reaches a slider, a bar, a meter, a sparkline, a pager or a
  mascot. `prism_S3`'s slider still draws **nine `⣿`, `DANGER_FORM` byte for byte, four rows above
  `⣿Delete all⣿`**, and this increment does not touch it: it is inside set B's exclusion, which is the
  operator's, and §7.1 of the round objects to the exclusion rather than to the frame.
- **`prism_S5`'s sparkline is still drawn in block elements** (`▂▅▂▅▂▅█▅`) in a language whose whole
  alphabet is braille, and `naught_S5`'s is drawn in braille in a language of circles. One composer hands
  out alphabets without asking the kit. Neither is in scope here.
- **The box law is the first thing in this repo to compare two states of one part.** K4's other two
  cases — `blueprint_S3`'s `├─┤` / `├┤·` / `├╎┈` — are a THREE-state comparison on a ladder, not a
  two-state one on a bit, and this law's shape does not reach them.
- **`⡇` is now drawn by the meter at the frontier** where the old direction drew `⡀`. It is a cell the
  kit already spends (the stepper's ACTIVE half-column names it), `verify_language` is green, and the
  census is unmoved — but it is a new occurrence of a half-cell fill and it is recorded here rather than
  discovered later.

## 10. Pending — not this increment

- **inc65** — `solari_S4` under F amended, and `corgi_S4` under inc40's head law (C8).
- **inc66** — the S4 walls (C2) and swiss's freed channel.
- K5 (no instrument reaches a quantity widget), L6, L7, L10, C5–C7, C9, C10, E2, E3, G1, G2 — open.

## 11. Suggested next task

`inc65`, as briefed: `Solari.band_head` moves below the header of the first unnamed gate, and `corgi_S4`
gets inc40's head law while keeping the board gone.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1147 passed, 2 skipped, 1 failed`
      (inc63 closed at `1123 passed`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) — **reported,
      not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py` 66 frames / 330
      pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `capture_languages.py` plain: 22
      captures, 22 grids identical across two processes, 4 artefacts moved (2 frames).
      `collision_census.py` both self-checks green, TOTAL 25, homoglyph rows 1.
- [x] **No secrets in code or output** — two kit tables swapped, one bitmap loop flipped, two laws and
      two teeth. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.

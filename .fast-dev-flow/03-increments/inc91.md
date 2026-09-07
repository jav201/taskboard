# inc91 — the key instrument: six frames per language, and the two steps no key can reach

Batch `rework-10`, increment 1 of 3.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation):

- **A frame has no focus; the round presses keys.** The instrument is `App.run_test()` + `Pilot` on
  the widget slice, per language, driving a fixed script and capturing the screen after each key
  through the same `cell_grid` the raster uses.
- **L12 corrected:** the match channel in grey is weight or decoration where the kit declares it, and
  the grey test reads the sidecar's `bold`/`underline` flags, not colour tokens; a kit is hue-only in
  grey only if its match run carries neither.

This increment is the **first** of the batch and implements the first ruling. It **records and does
not fix**, which is its brief's own instruction.

## §1 — cause

`PROTOTYPE-inheritors-5.md` converged on one sentence and it is the whole reason this file exists:
*"a key: `App.run_test()` + `Pilot`, five rounds unused; a frame cannot fail on focus because a frame
has no focus."* `SESION-PERSONA.md` §7.3 says the same thing from the other side, in the list of what
a human session cannot see: *"Ninguna tecla. El foco es decoracion en los 66 frames y lo sigue siendo
aqui … y el mecanismo real que existe y no se ha usado es `App.run_test()` + `Pilot`."*

Every artefact this programme has judged is a photograph of a composed surface. `render.py` mounts a
kit's output in a bare `Static`; `raster.py` paints that grid at 9×19 px; `legibility.py` measures the
paint. **None of the three can press anything**, so five rounds of objections about focus, about a
modal, about an invalid field and about a match run were arguments about pictures of those states.

## §2 — mechanism

`prototypes/components/keys.py` drives the real `TaskboardWidget` — the app `capture_languages.py`
already photographs — through a fixed six-step script in each of the eleven languages, at 100×32, and
reads every frame through `capture_languages.cell_grid`, which is the function the raster reads.

### The script, and where each key came from

| step | keys | what it is |
| --- | --- | --- |
| `K1` | *(none)* | the page as it opens, on the app's own `AUTO_FOCUS` seat |
| `K2` | `tab` ×3 | the focus ring walks three seats: `#hero` → a `Tile` |
| `K3` | `question_mark` | the app's modal. **It binds no delete**, so the brief's *"the key the app binds for delete or the modal"* resolves to the second half |
| `K4` | `escape` | the modal is dismissed |
| `K5` | `c` `1` `2` `/` `9` `9` `/` `2` `6` `tab` | `12/99/26` typed at the screen the app offers for editing, and a `tab` to blur it |
| `K6` | `ctrl+p` `r` `e` `f` `r` `e` | the command palette, and a query with exactly one match (`Refresh now`) |

`12/99/26` is a day-99 month, which `taskboard.models.parse_iso` refuses and which every one of the
eleven kits draws a state for. `refre` matches one command and only one, in all eleven, because the
commands are the app's and do not vary by language — which is what makes K6 a comparison of MATCH
RENDERING rather than of result sets.

### One session per language and not six

Step 4 is only a law about restoration if the modal it dismisses is the one step 3 opened, and step
2's walk is only a walk if it starts where step 1 left the ring. Six sessions would have measured six
first frames.

### The artefacts, and the two passes that make them

66 frames × `.txt` + `.svg` + `.png` + a `.json` sidecar. The sidecar carries what the laws need and
what no picture holds: **the focused widget's id, class and screen rectangle**, the modal box's
rectangle, the screen class, the settle read count, and the grid run-encoded.

The raster is taken in **two passes** — pass one writes the text so `key_cells()` has a corpus to
read, pass two paints with metrics built from that corpus — because the fallback declaration has to be
checkable rather than guessed.

### The corpus's first double-width cell, and nobody chose it

Textual's command palette draws its prompt as `SearchIcon`, whose glyph is `U+1F50E`. It is **two
columns wide**, so the palette row arrives 99 grid entries long for a 100-column frame and everything
right of the prompt would have been painted one cell left of where the terminal puts it. `widen()`
gives a wide glyph a continuation cell so column N of the raster is column N of the terminal; the
glyph is drawn into a box two cells wide. **The SVG takes the raw grid and the PNG takes the wide
one**, because the SVG's own renderer already advances two columns for a two-column glyph.

The uncovered set is declared and asserted, and **it is not the sheets' set**: `raster.FALLBACK_CELLS`
is `⊖⊚⊛⋅`; the live app spends `⊖⊙⊚` plus the prompt, and neither `⊛` nor `⋅`. Two cells the sheets
draw are drawn by no screen the app HAS.

### The K5 law was a character scan first, and it passed twice on a screen with no field

Asked as *"is any cell anywhere drawing the wall glyph in the wall tone"*, the invalid clause came
back **green on instrument (5 cells) and industrial (2)** — instrument because `⠶` is that kit's
chrome as well as its wall, industrial because `▐` and `▌` are half blocks it spends everywhere.

That is `spec.md` §23.3.1 one instrument further out. `role_map` keyed by CHARACTER credited
darkside's prose `o` to its severity family; inc87 fixed it by asking what the CONTRACT PAINTS.
`field_seats()` now asks for the SHAPE `field_form` declares — wall, paper, wall, with the walls in
`field_wall_tone`'s tier and the paper in another, which is that method's own doctrine — and the two
green cells go away. **A law written the old way would have shipped a pass for a state neither kit
draws.**

## §3 — law

Five laws in `tests/test_components.py`, all read off the artefacts, none importing the instrument.

| law | ×11? | what it binds |
| --- | --- | --- |
| `test_the_key_script_the_frames_were_taken_with_is_the_one_declared` | roster | 66 sidecars, each carrying its step, its keys, its viewport and its language; the script is declared a SECOND time in the suite so the two can only agree by somebody editing both |
| `test_the_seat_that_holds_focus_is_drawn_differently_when_it_holds_it` | ×11 | **the first thing in this corpus that could ever fail on focus.** Judged on the focused widget's own region, so a clock redrawn elsewhere cannot pass it |
| `test_a_modal_draws_a_band_and_the_band_is_the_kits_own_panel` | ×11 | the band exists AND its ground is the kit's `panel`, not `widget.tcss`'s hard-coded `#0d1219` |
| `test_escape_gives_back_the_page_the_modal_covered` | ×11 | cell for cell against K2 — and K4 must NOT equal K1, or the app threw the focus walk away |
| `test_the_two_states_no_key_can_reach_are_recorded_with_a_stale_check` | roster | **the round's result, written as a law that will go red** when either is fixed |
| `test_the_live_search_seat_prints_a_cell_the_measured_face_has_not_got` | roster | the prompt is uncovered by the face and two columns wide, both asserted |

## §4 — teeth

- **The focus law's tooth is in the same function**, because the mutant is the FRAME and not the code:
  the same measurement is run over a pair that did not move, and it must find nothing. A measurement
  that always finds a difference cannot pass this.
- **The restoration law's second clause is its own tooth**: K4 ≠ K1. A frozen app whose `escape` did
  nothing at all would satisfy "K4 == K2" and fails here.
- **`test_the_two_recorded_failures_are_failures_of_the_app_not_of_the_law`** is the arm that matters
  most, and it is what stops the record from being vacuous. `not seats` and `not painted` hold most
  easily when the measurement is broken, so both are run against frames that DO carry what they look
  for, built out of each kit's own `field_form` and `MATCH_STYLE`. Neither is a frame the app produces
  — that is the finding — and both are frames every one of the eleven knows how to draw.

## §5 — what was found by looking, BEFORE any fix

```
  language    K1 K2 K3 K4 K5 K6
  naught       ok  ok  ok  ok   X   X
  corgi        ok  ok  ok  ok   X   X
  instrument   ok  ok  ok  ok   X   X
  swiss        ok  ok  ok  ok   X   X
  industrial   ok  ok  ok  ok   X   X
  nord         ok  ok  ok  ok   X   X
  darkside     ok  ok  ok  ok   X   X
  prism        ok  ok  ok  ok   X   X
  ledger       ok  ok  ok  ok   X   X
  solari       ok  ok  ok  ok   X   X
  blueprint    ok  ok  ok  ok   X   X

  LAWS: 44 of 66 hold, 22 FAIL -- recorded, not fixed here
```

**The failures are not language-shaped, and that is the finding.** Every one of the eleven fails
exactly K5 and K6, and passes exactly K1–K4. No kit is worse than another at either. The two failures
are facts about the APP, and both of them are places where the corpus draws a state the app cannot
reach:

1. **K5 — the widget has no live TYPED seat, in any language.** `textfield_block`'s own docstring said
   so three passes ago and refused to invent one: *"Pass 53 read this app for a live text seat and
   found none — nothing in the engine is TYPED — and refused to invent one."* That refusal is now
   measured: the INVALID state **all eleven kits draw at `S2`**, whose walls inc85 moved into `ink`
   across every one of them, is reachable by **no key**. Eleven kits draw a refusal nobody can
   provoke.
2. **K6 — the command palette is byte-identical in all eleven languages.** Measured on the frames:
   the palette's eight rows, run-encoded, collapse to **ONE distinct block across the eleven**. Its
   chrome is `#141f27` and `#0e395a` — Textual's own theme — and its match highlight is
   `bold+underline` on `#0e395a` in every language, which is **no kit's `MATCH_STYLE`**: not
   instrument's `underline {accent}`, not swiss's `bold {alert}`, not darkside's `reverse {mut}`. The
   app's ONE live match run speaks none of the eleven languages.

Three more, found by looking rather than by measuring:

3. **On ledger the palette is not merely un-languaged — it inverts the kit.** ledger is the corpus's
   one light-paper language (`#e9e1cf`), and the palette lays a `#141f27` slab across the middle of
   it. The one kit whose ground is paper gets the framework's night mode.
4. **The palette's prompt is a colour emoji outside the corpus's measured face and outside its grid**
   (§2). It is also the only cell in 66 frames that neither a kit nor a screen chose.
5. **The palette's blank cells carry `#00ff00`** — Textual's `Input` default — on every one of the
   eleven. It paints nothing only because those cells are spaces.

And one about the instrument rather than the corpus:

6. **The frame is deterministic and the number of looks it takes to settle is not.** 264 artefacts are
   byte-identical across two processes; `settle_reads` lands on 8, 9 or 10 depending on where the
   event loop was when the key arrived. It is in the sidecar and it is **masked** from the
   reproducibility bargain by a named constant (`UNPINNED`), not dropped from the record.

## §6 — files and frames

| file | change |
| --- | --- |
| `prototypes/components/keys.py` | **new, 661 lines.** The script, the two-pass raster, `widen`, `field_seats`, `judge`, and the fresh-process reproducibility check |
| `tests/test_components.py` | `KEYS`, `KEY_SCRIPT`, `KEY_RESTORE_AGAINST`, `KEY_UNREACHABLE`; six laws and the vacuity arm |
| `prototypes/components/keys/` | **new, 264 artefacts**: 66 `.txt` + 66 `.svg` + 66 `.png` + 66 `.json` (2 990 KB of PNG) |

**Frames changed: ZERO.** No kit, no screen and no theme was touched. `render.py`, `raster.py`,
`second_width.py`, `matrix.py` and `collision_census.py` were re-run and `git status --porcelain` on
`prototypes/components/*_S?.*` is empty.

**Gallery 30–51: none changed byte-wise**, read off `prototypes/components/` (the `.txt`).
`capture_languages.py` was not run: no board changed.

## §7 — deviations, named

- **K4 is judged against K2 and the brief says K1.** The brief's words are *"escape → the band is gone
  and the page is byte-identical to K1"*. Read literally that asks `escape` to undo the three `tab`s
  the script itself pressed one step earlier, which no app does and none should. The law is judged
  against **the frame the modal covered**, and the distance from K1 — 326 to 811 cells, the focus
  walk — is reported in the same line rather than hidden. `RESTORE_AGAINST` is a named constant so
  the choice is arguable.
- **K5's keys land on a screen with no field, and that IS the step.** The brief asks for a date typed
  into the date field; the app has none, so the keys are sent at the screen the app offers for editing
  (`c`) and the law asks whether the language's declared invalid field is anywhere on the resulting
  frame. It is not, in eleven of eleven.
- **K6 is drawn over the config screen and not over the board.** The script is a SEQUENCE and step 6
  is pressed where step 5 left the user. It is the same in all eleven, which is what the comparison
  needs.
- **The invalid seat and the palette match are NOT fixed here.** The brief: *"do not fix kits in this
  increment, record."* They are inc93's.

## §8 — gates

```
pytest -q                1535 passed, 1 failed, 2 skipped in 48.23s
                         (baseline 1499 -> 1536 total, +37: 1 roster + 11 focus
                          + 11 band + 11 escape + 1 record + 1 vacuity arm +
                          1 face.  The one failure is
                          test_win_clipboard_roundtrip, environment-coupled,
                          reported and not counted, not touched)
keys.py                  264 artefacts identical across two PROCESSES
                         (66 .txt + 66 .svg + 66 .png + 66 .json)        exit 0
                         settle reads [8, 9, 10] -- masked, not dropped
                         LAWS: 44 of 66 hold, 22 FAIL, recorded
verify_language.py       ALL PASSED                                      exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn     exit 0
                         -- and nothing changed on disk
matrix.py                refusals [] for all eleven                       exit 0
collision_census.py      TOTAL 23 · homoglyph rows 22 · both self-checks
                         green · zero collisions: darkside                exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct      exit 0
capture_languages.py     not run: no board changed
```

`BELOW_THE_FLOOR`, old → new: **4 → 4, unchanged.** This increment moves no seat.

## §9 — pending / next

- **inc92**, the batch's second ruling: L12 corrected, `match_branch()` and `MATCH_IN_GREY` read the
  sidecar flags.
- **inc93** takes K5 and K6, which are the two defects this increment recorded, and the round that
  judges the 66 key frames.
- **What this instrument still cannot see**, said before anyone asks it to: one script, one width, one
  focus walk, no human, and no second press of the same key. It can tell you a seat is drawn
  differently when it holds the ring; it cannot tell you that anyone would notice.

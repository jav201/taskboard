# inc87 — a declared seat is a column, not a character; and the correction inc84 needed

Batch `rework-9`, increment 1 of 4.

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

This increment is the **first** and the **sixth**.

## §1 — cause

**`inc85.md` §5.1 found it and refused to fix it in the increment that would have benefited from its
absence.** After inc85 moved twenty-six quiet meaning marks into `ink`, exactly one `mut` seat was
left under Q1's effective clause — `darkside severity o #757575` at 2.51 — and it was the one row
that made the increment's own law need an exception. It is not a rung.

`collision_census.role_map()` is keyed by **CELL**. darkside is the one kit of eleven whose severity
ladder is a lowercase letter (`· ` / `o ` / `O `), so the census credits **every `o` in the corpus**
to the severity family. The derivation then walked every toned run of `log_row`'s output and credited
any character the census named — and `board loaded` has two of them. The row measured the letter `o`
of a log MESSAGE, painted in `mut` because a message is a text run and K6 is the floor written for
it.

**`legibility.py`'s own docstring claimed this could not happen.** *"Only cells `role_map` already
credits to that family survive, so a letter that happens to sit inside a log message is not promoted
to a severity rung by being printed next to one."* The intersection it describes is real and it does
not do that job, because both halves of it are keyed by character.

**And before inc85 the defect was invisible.** The rung and the message produced the same `(o, mut)`
pair, so the row looked exactly like a rung that had not moved yet. It only became a separate,
wrong-looking row once the rung left `mut` and the message did not.

## §2 — mechanism

**A seat is a COLUMN.** Each of the five contract calls now declares the prose it hands the contract
alongside the call itself:

```python
A_SEAT_CALLS = (
    ("severity", ("09:41", "board loaded"), lambda k: [k.log_row(lv, …) …]),
    ("danger",   ("Delete",),   lambda k: [k.button("Delete", danger=True)]),
    ("required", (),            lambda k: [k.required()]),
    ("cursor",   ("a", "b"),    lambda k: [k.menu(["a", "b"], 0)[0]]),
    ("invalid",  ("12/09/26",), lambda k: [k.textfield("12/09/26", …)]),
)
```

The contract methods return the caller's text **byte for byte** — `log_row`'s docstring says exactly
that, in those words, and it is a promise the contract already made for its own reasons — so the
columns that text fills are known exactly. `toned_columns()` flattens the markup to the row as it
reaches the glass and records where each toned run stands in it; `prose_columns()` returns the
columns the caller's own strings occupy; the intersection with `role_map` is then taken **per
column** instead of per character.

`log_row`'s rung column is a severity seat. The same letter inside the message printed beside it is
not. **Prose never counts.**

### The one thing this mechanism can get wrong, said out loud

The strike is by string occurrence, and every occurrence is struck rather than the first — a
derivation that guessed which copy of the caller's text was the real one would be deciding by
position the thing it exists to read off the contract. The cost is that **a caller who handed a
contract the kit's own mark as content would strike the mark**. That is not hidden in a comment: it
is clause (c) of the law, *the strike may never empty a family*, asserted in all eleven kits for all
five families, and it is why the law's second arm swaps the twelve-column MESSAGE and not the
one-character menu option.

## §3 — law

| law | what it binds |
| --- | --- |
| `test_the_declared_seat_is_a_column_the_contract_paints_not_a_character` (×11) | **a declared seat does not move when the caller changes its words.** (a) swap the time, the message, the label, the option and the value for text this kit credits to no family, at their original lengths, and the seats are identical; (b) swap the message for **this kit's own severity ladder** repeated to the same twelve columns, and the seats are identical again; (c) all five families still have a seat, in every kit; (d) everything the character-keyed derivation saw and this one does not is named in `PROSE_NOT_A_SEAT` with ≥ 20 words of reason, and nothing else is lost |
| `test_no_meaning_mark_that_only_misses_the_contrast_clause_is_left_quiet` (×11) | **strengthened, not edited around.** Its clause used to read *"a quiet `EFF`-only row must be the one named `a letter of the message`"*. It now reads *"no `EFF`-only row is painted in `mut` or `dim`"*, with no survivor and no name. A law that carried an exception carries none |
| `test_the_uncured_table_covers_what_it_claims_to` | two kinds, both used — the third kind (`a letter of the message`) is retired because the row it held was never a seat |

**The law never mentions columns.** It changes the words and checks the answer, which is the only
construction under which the mechanism and the law can agree by being right rather than by being the
same code twice. This is the standing bargain `legibility.py` and `tests/test_components.py` already
have (`test_this_files_picture_metrics_are_the_exporters`), applied to a derivation instead of to an
arithmetic.

## §4 — teeth

`test_the_seat_derivation_bites_when_it_reads_by_character` — **the mutant is the strike itself**,
not the roster: `_prose_columns` is made to return nothing, which is precisely the code that shipped
before this increment. Three laws must notice, and they are chosen because they are the three
different things the defect was doing at once:

1. **it invents a seat** — `("severity", "o", mut)` comes back for darkside and `("invalid", "/",
   ink)` for industrial;
2. **it invents a FAILING seat** — the invariance law goes red on those two kits, and the assertion
   is written per-kit so a mutant that broke all eleven would be visible as a different failure;
3. **it miscounts the corpus** — `test_a_meaning_mark_clears_the_two_clause_floor_at_its_declared_
   seat("darkside")` goes red, because `BELOW_THE_FLOOR` grows a row that is a log message.

Both caches (`declared_seat_tones`, `floor_rows`) are cleared on the way in and on the way out, and
the green state is asserted on both sides — a memoised derivation would otherwise let the tooth ask
the cache what the kit says.

## §5 — what was found by looking

**1. The ruling names one kit and the mechanism found a second, in a family nobody was looking at.**
`industrial invalid / #f2f2f2` was **passing** at 26.3 % coverage and 5.02 effective. industrial
declares `/` as the INVALID mark of its **slider knob** and its **stepper step**; the field this
derivation exercises is handed the value `12/09/26`, and the two slashes of the date were being read
as the field's rejection mark. It is the same defect as darkside's with the sign reversed — a seat
invented out of prose that happened to look healthy — and the fix removes it in the same line.

**2. And that exposes a hole the fix does not fill: two invalid marks in this corpus have no contract
call of their own.** `A_SEAT_CALLS` exercises five methods; `slider` and `stepper` are not among
them, so industrial's `/` now has **no** declared seat and is not measured at its own. It was never
measured at its own — the 5.02 was a number about a date separator — so nothing was lost, but the
gap is now visible where it was covered. **Handed back, not taken**: adding calls raises the bound
count and is a different question from the one the ruling asked.

**3. The bound-seat count fell for the second time in three increments and the two falls are
different events.** 89 → 86 was inc85's TIER MOVE seen from the counter's side (a seat drawn in two
tones is two rows, and three of them collapsed to one when the quiet copy moved onto the loud one).
86 → 84 is this increment's DERIVATION FIX (two rows that were never seats). Both are asserted beside
the failing count, so a seat that stops being **drawn** can never be mistaken for a seat that passed.

**4. Nine kits are byte-for-byte unaffected and that is the strongest evidence the fix is narrow.**
The seat count per kit: naught 7→7, corgi 7→7, instrument 8→8, swiss 8→8, industrial **9→8**, nord
6→6, darkside **9→8**, prism 8→8, ledger 6→6, solari 13→13, blueprint 5→5. A derivation change that
touched nine languages it had no business touching would look identical to this one in the report's
total.

**5. Two directories in this repo are called "gallery", and inc84 checked the wrong one.**
`prototypes/gallery/` holds the twenty-two board and component GRIDS `capture_languages.py` writes.
The skill's `assets/gallery/` holds the twenty-two numbered frames **30–51**, each a copy of one
sheet in `prototypes/components/`. inc84 ran `git status --porcelain` on the first and reported the
second. Entries **35 `corgi_S6`** and **36 `ledger_S6`** did change, because inc84 moved all eleven
`S6` sheets at 100×32 and two of the twenty-two sources are `S6` sheets. The mapping was not assumed:
it was checked with `cmp` against eight installed frames and cross-read against the four entries
`inc67.md` names and the one `inc69.md` corrects (46 is `swiss_S1`, not `swiss_S2`).

**6. `MEANING_MARKS` did not move, and the reason is a boundary worth naming.** Section E of the
report reads `role_map` directly and asks a different question — *how many marks does the corpus
draw, and how many are under 3:1 at their worst seat* — which has no declared seat in it at all. A
derivation fix that had moved section E's numbers would have been reaching past the ruling.

## §6 — files and frames

| file | change |
| --- | --- |
| `prototypes/components/legibility.py` | `A_SEAT_CALLS` gains the prose per call; `toned_columns()` and `prose_columns()` added; `declared_tones()` intersects by column; §F of the report gains the paragraph that says so |
| `tests/test_components.py` | `seat_calls()` / `_SEAT_PROSE` (the words made swappable), `_row_columns()`, `_prose_columns()`, `seat_tones()`; `PROSE_NOT_A_SEAT` (2 rows), `_blind_seat_tones()`, one law ×11 and one tooth; `BELOW_THE_FLOOR` 17 → 16 keys, `FLOOR_SEATS_BOUND/FAILING` 86/18 → 84/17, `EFFECTIVE_UNCURED` 6 → 5 rows and 3 → 2 kinds |
| `prototypes/out/legibility.txt` | 867 → 876 lines; §F re-measured and re-worded by the report itself, nothing hand-edited |
| `.fast-dev-flow/03-increments/inc84.md` | **§6 corrected in place**, dated 2026-09-07, with the two-directory confusion named and the verification of both entries |

**Frames changed: ZERO.** `render.py`, `raster.py` and `second_width.py` were re-run and
`git status --porcelain` is empty on `prototypes/components/`. A derivation is not a drawing.

**Gallery 30–51: none changed byte-wise**, and this time read off `prototypes/components/` — the
twenty-two sources are `ledger_S3`, `corgi_S3`, `prism_S3`, `naught_S5`, `blueprint_S5`, `corgi_S6`,
`ledger_S6`, `corgi_S1`, `ledger_S1`, `naught_S2`, `ledger_S2`, `blueprint_S2`, `naught_S4`,
`prism_S4`, `instrument_S1`, `industrial_S1`, `swiss_S1`, `solari_S1`, `industrial_S4`,
`darkside_S4`, `solari_S2`, `instrument_S5`, and not one of the sixty-six `.txt` moved.
`capture_languages.py` was **not** run: no board changed.

## §7 — deviations, named

- **`SEATS_MOVED_TO_INK` keeps its `darkside severity o` row**, at `("mut", 2.51, 8.34)`. Those two
  numbers are measurements of the GLYPH on the kit's ground at two tiers, not of the defective row,
  and the rung really did move. Removing it would have deleted the record of a move that happened.
- **`OBLIGATION_UNDER_THE_FLOOR`, `SEEN_BY_EYE` and `NAMED_RUNS_5_TO_7` are untouched.** None of them
  holds a row the derivation moved.
- **The slider and the stepper get no seat call.** §5.2. Adding two calls would change the bound
  count in the same increment that changes the derivation, and the two effects would be impossible to
  read apart in the report.
- **The 80×24 sheets are not in the gallery correction.** The skill installs the gallery at 100×32
  only, so inc84's 80-column moves cannot reach entries 30–51 whatever they touched.

## §8 — gates

```
pytest -q                1478 passed, 2 skipped, 26 warnings in 52.09s
                         (inc86 1466 -> 1478, +12: 11 parametrized + 1 tooth;
                          ZERO failed -- test_win_clipboard_roundtrip passed
                          in this run.  Baseline run before the increment:
                          1 failed, 1465 passed -- the clipboard test, which
                          is environment-coupled, reported and not counted)
verify_language.py       ALL PASSED                                     exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn    exit 0
                         -- and nothing changed on disk
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                          exit 0
legibility.py            876 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct     exit 0
matrix.py                refusals [] for all eleven                      exit 0
collision_census.py      TOTAL 27 · homoglyph rows 24 (both unchanged)   exit 0
capture_languages.py     not run: no board changed
export_to_skill.py       runs at the batch close (inc90)
```

`BELOW_THE_FLOOR`, old → new: **18 → 17 rows.** The row that left is
`("darkside", "severity", "o", "#757575"): "EFF"`, and it left because it was never a seat.

## §9 — pending / next

- **inc88** — the three cursors in `accent`, corgi `░` → `▓`, ledger `*` → a heavier printer's mark.
- **Handed back by this increment:** `slider` and `stepper` have no seat call, so two of industrial's
  three declared invalid marks are unmeasured at their own seat (§5.2).

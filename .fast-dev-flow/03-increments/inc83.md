# inc83 — solari_S4 at 24 rows (F) and the opener (K8); blueprint_S4 (four corners are not a box)

Batch `rework-8`, increment 3 of 4.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation), all adopted from round five's
recommendations:

- **Q1:** the legibility floor is two clauses, not a product: coverage ≥ 15 % of the cell AND
  effective contrast ≥ 3:1, both at the declared seat.
- **Q2:** runs of 1–4 cells carrying an A-family role are bound by the floor; runs of ≥ 8 cells of one
  glyph are structure, bound only to "not equal to the ground"; 5–7 named per seat like
  `DIM_CLASSIFIES`.
- **Q3:** the floor is judged at the declared seat; the worst seat is reported as a notice, never red.
- **F at 24 rows:** the band takes the nearest full-measure position that cuts no gate block, below
  first then above; if neither fits, the band is the whole page (a full-screen confirm);
  `LANGUAGES.md` gets no minimum height.
- **K8/E6:** a run of blank cells on a non-ground background is ink; the census, `painted_runs()` and
  `legibility.py` count it (18 runs in 3 kits today); it obeys Q2 as structure.
- **Greyscale:** `raster.py` also writes a greyscale PNG per frame (luminance only); L12's three
  hue-only match channels are judged on it, and a match that vanishes in grey is recorded as a Limit
  of the language, not fixed.

## §1 — cause

### solari — a placement rule written on a page that always had somewhere to go

Ruling F: *a confirm never covers the gate it names.* inc55 satisfied it by walking the page's gates
in order and taking the first one the confirm does **not** name that has room, falling through to
`schedule_foot` when none does. inc78 pointed the same law at 80×24 and it went red:

```
100x32   about=DOING   heads BACKLOG@3 DOING@9 BLOCKED@19 DONE@22
                       BACKLOG has no room (3+1+6 > 9), BLOCKED has none (19+1+6 > 22),
                       DONE does -> band 23..28, clear below DOING's block (9..18)   GREEN
 80x24   about=DOING   heads BACKLOG@3 DOING@9 BLOCKED@19
                       BACKLOG has no room, BLOCKED has none, there is no DONE
                       -> schedule_foot -> band 17..22, and rows 17,18 ARE DOING     RED
```

**The rule had no way to notice.** It asked "which gate has room" and never asked "does this position
touch the gate I am about". At 32 rows the two questions have the same answer; at 24 they do not.

### blueprint — a promise the alphabet cannot keep

`blueprint_S4` delimits its modal with four loose corners `┌ ┐ └ ┘` **44 cells (396 px) apart**. Round
five looked at the pixels and turned a limit of method into a defect of design: at 16 px the eye does
not close that gap, so the frame **says "here is a rectangle" and shows four marks**. Its criterion —
*point at the modal's border* — has no answer.

And the proof that the vocabulary is not broken, only mis-scaled, is on the **same sheet**: the mode
strip draws `┌ ┐` / `└ ┘` at **two** cells and reads as a box cleanly. **The missing law is about
distance, not about glyphs** (K10).

## §2 — mechanism

### `Solari.band_head` — a scan of positions, not a walk of gates

The anchor stops being "the first unnamed gate with room" and becomes **the nearest legal position**.
A position is legal when the band lies inside the page, starts at or below the masthead, covers no
gate **header** (F amended, unchanged) and touches **no row of the named gate's block** (F itself).
The scan runs **below** the named block first, nearest outward, then **above** it, nearest outward —
the ruling's own order.

**It reproduces every anchor inc55 and inc65 shipped without being told to.** At 100×32,
`about=BACKLOG` → 10 (unchanged, so `solari_S4.txt` does not move); `about=DOING` → 23 (unchanged).
At 80×24, `about=BACKLOG` → 10 (unchanged, so `w80/solari_S4.txt` does not move either).

**Two fallbacks, and they are not interchangeable:**

| condition | answer | why |
| --- | --- | --- |
| no unnamed gate exists (every gate named, or a one-gate page) | `schedule_foot` — **inc55's, untouched** | on such a page there is nowhere that does not touch the named gate, and the confirm's own words are the only thing left to say which gate it is about |
| an unnamed gate exists and no position is legal | **`None` → the band takes the whole page** | the page ran out; a band that cannot avoid the gate it names must stop pretending to be a band |

Sliding the second into the first would put a band on the gate it names and call it a fallback.
`overlay_instead` draws the full-screen form as opener bar → question → air → seam on the last row,
which is what corgi does by doctrine.

**The opener stays.** The band's first row is `w` blank cells on `accent` — a hundred of them at 100
columns, the brightest run the kit draws, and C3‴/K8's whole subject. Under Q2 it is **structure**
(≥ 8 cells) and owes exactly one thing: not to equal the ground it stands on. `#f5a300` against
`#0b0b0c` is **9.48:1**. It is now counted (inc81 §G) and it stays.

### `Blueprint.overlay_instead` — a crosshair is a point

The four marks become `┼`, declared as `Blueprint.REGISTER`.

A **corner** is a stub of two walls: it points along both of them and promises a rectangle the next
cell over. A **crosshair** is a point — symmetric, no handedness, no stroke running out of it in any
direction. Four of them at the corners of an extent is what a drawing office actually registers a
region with, and **no reader can be owed a rectangle by a cross**, so the distance stops mattering.

This is the language's own doctrine, not a new one: `LANGUAGES.md` §11 and this method's own first
line since it was written — *"not one element on this sheet is boxed, at any width"*, and the ten
marks contain no vertical stroke, so the walls **cannot** exist. The corners were promising something
the alphabet has no way to draw.

`┼` was free: not declared at any seat, drawn at none of the 66 frames, and the one cell of the light
box-drawing family this sheet had not spent. **Side effect:** `┌` goes back to being only `Blueprint.
CUR`, which it also was.

## §3 — law

| law | what it binds |
| --- | --- |
| `test_a_solari_confirm_never_covers_the_gate_it_names` | now two-branched: for every gate, either the named block survives byte-for-byte **or** the band took the page — and the full-screen branch must be in `SOLARI_TAKES_THE_PAGE`, must leave **no gate header on screen at all**, and must close on the seam |
| `test_ruling_F_holds_at_both_heights_and_says_where_the_page_ran_out` | the same question at **both** heights, per gate, with the whole-page branch reached exactly where the roster says |
| `test_a_language_that_refuses_the_box_spends_no_cell_of_one` (×6) | **K10**: a kit in `MODAL_BORDER_REFUSED` spends none of the four **corner** cells of its own `MODAL_BOX` on the thing it draws instead |
| `test_blueprints_registration_marks_are_points_and_not_corners` | the shipped frame: four `┼`, two rows, one squared extent, and no box cell between them — with the mode strip's own corners explicitly still there |
| `SECOND_WIDTH_RED` | **now empty**, and kept rather than deleted because an empty recorded set is the only kind that can go red by growing |

**Why K10 is a law about a PROMISE and not about a DISTANCE.** A threshold was the obvious shape and
it is the wrong one: the number would have to be invented inside this increment, it would differ per
glyph and per face, and round five's own §7 warns against exactly that. What is checkable without
inventing anything is the promise — and removing the promise removes the distance question with it.

**The corners and not the strokes.** `MODAL_BOX` is `"┌┐└┘──││"`; the law reads its first four cells.
swiss and ledger open and close their bands with `─` and neither is claiming a box: a rule is one
stroke and says nothing about a second dimension. Without that distinction the law failed both of them
for doing their job.

## §4 — teeth

- `test_ruling_F_holds_at_both_heights…` clause (c) **re-installs inc55's rule** and watches it
  produce the old arithmetic: nothing eaten at 100×32, **rows 17 and 18 eaten at 80×24**. The fix is
  shown against the defect, not against a description of it.
- `test_the_refused_box_law_bites_on_the_corners_blueprint_shipped` — `REGISTER` put back to `┌`,
  which is the declaration round five photographed; blueprint goes red and the other five refusing
  kits stay green.
- `test_the_bands_old_anchor_ate_the_gate_the_confirm_names` and
  `test_the_wrong_gate_law_bites_on_the_anchor_inc55_shipped` (both pre-existing) still bite,
  unmodified, against the new `band_head`.

## §5 — what was found by looking

**1. The shipped frames did not have to move, and that is the strongest thing about the fix.**
`solari_S4` is byte-identical at **both** widths after the anchor was replaced — because the new scan
reproduces inc55's and inc65's answers wherever they were already right. What changed is the two
mechanism arms nobody could see: `about=BLOCKED` at 100×32 moves 10 → 23 and `about=DONE` moves
10 → 13, both of them now **below/above the named block** instead of at the first gate that happened
to have room. A rule can be wrong in three places and only fail in one.

**2. The full-screen branch is reached exactly once in the whole corpus** — `(24, "DOING")` — and it
is the arm inc78 recorded as red. Every other gate at every other height still gets a band.

**3. blueprint's mode strip was never the problem and the fix does not touch it.** `┌ ┐` at two cells
is still on `blueprint_S1` and on `S4`; the law asks about the **overlay**, which is the element that
claimed to be a dialog.

**4. `test_win_clipboard_roundtrip` passed in this increment's full run** (1401 passed, 0 failed) and
failed in inc81's and inc82's. Three passes, two failures, five runs, no change to anything it
touches. Recorded, not counted, not touched — and now demonstrated rather than asserted.

## §6 — files and frames

| file | change |
| --- | --- |
| `taskboard/language.py` | `Solari.band_head` rewritten as a position scan with two named fallbacks and `None` for "the page ran out"; `Solari.overlay_instead` gains the full-screen branch and the opener's K8 note; `Blueprint.REGISTER = "┼"` declared and `Blueprint.overlay_instead` draws it |
| `tests/test_components.py` | ruling-F law two-branched + `SOLARI_TAKES_THE_PAGE`; the 80×24 arithmetic law rewritten as the fix's law with inc55's rule re-installed as its teeth; `SECOND_WIDTH_RED` emptied; K10's law + blueprint's frame law + teeth |
| `prototypes/out/legibility.txt` | corpus 207 → 208 distinct painted glyphs (`┼` joins at 25.6 % ink), 2799 → 2800 drawings; `┌ ┐ └ ┘` each lose one cell |

**Frames changed — 2, at two widths, and nothing else:**

```
prototypes/components/blueprint_S4.txt  .svg     prototypes/components/png/blueprint_S4.png  .json
prototypes/components/w80/blueprint_S4.txt  .svg  .png  .json
```

**`solari_S4` did not change at either width.** Neither did any other frame.
**Gallery 30–51: none changed byte-wise** (`capture_languages.py` run plain, `git status --porcelain`
empty on `prototypes/gallery/`).

## §7 — deviations, named

- **`LANGUAGES.md` gets no minimum height**, per the ruling, and none was added. solari renders at 24
  rows; what it does there is take the screen for a confirm it cannot place beside the schedule.
- **K10 is enforced as a promise, not as a distance** (§3). The distance number round five measured
  (44 cells vs 2) is in the docstring as the evidence and nowhere as a constant.
- **The one-gate fallback still lets the band sit inside the named gate.** That is inc55's second
  sentence and this increment did not touch it: `test_a_page_whose_every_gate_is_named_puts_the_band_
  at_the_foot` still asserts it, and the branch is unreachable from any shipped frame.

## §8 — gates

```
pytest -q                1401 passed, 2 skipped, 4 warnings in 45.00s
                         (inc82 1391 -> 1401, +10; ZERO failed this run --
                          test_win_clipboard_roundtrip passed, see §5.4)
verify_language.py       ALL PASSED                                    exit 0
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn   exit 0
matrix.py                refusals [] for all eleven                     exit 0
collision_census.py      TOTAL 27 · homoglyph rows 24 (unchanged by inc83) exit 0
raster.py                66 PNGs identical across two PROCESSES         exit 0
legibility.py            byte-identical across two PROCESSES            exit 0
second_width.py          0 rows cut · 330 pairs distinct                exit 0
second_width (laws)      SECOND_WIDTH_RED == set() -- 0 red, both solari arms
capture_languages.py     22 grids identical across two PROCESSES · gallery UNCHANGED
```

## §9 — pending / next

- **inc84** — the key bar at 24 rows (C12), the greyscale capture (L12) and truncation marking (C13).
- Still unruled from inc81/inc82: swiss `•` at 14.0 %, and the K6-vs-Q1 collision on `mut`.

# Increment 53 — a channel is count, weight, position or direction; diameter alone is not one

**Batch:** `rework-5a` · carries out **Ruling D** on `PROTOTYPE-inheritors-2.md` §6 decision (D) and its
§0b/§4 finding — *"cinco de los seis lenguajes que sí tuvieron incremento resolvieron una colisión
mudándose a un homoglifo"*
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`
— **3 source files**, plus 8 regenerated frame artefacts, 2 gallery artefacts, the regenerated census
table and this packet.

**The word "channel" has carried five increments of argument and has never been defined, so a language
could close a collision by moving to the same drawing at another size and the instruments would sign it.
It is defined here, in the census's header and in the rule's docstring: COUNT, WEIGHT, POSITION,
DIRECTION — and DIAMETER ALONE IS NOT ONE. The census gains a homoglyph table with a roster and a
self-check, and it finds five rows on first run. Two are fixed — swiss's chosen option left `●` (which is
`REQUIRED •` at another size) and darkside's field leader left `◦` (which is `LEVELS["warn"] o` at
another size). Three are printed and named. Four earlier moves are ACCEPTED with the channel each
spends, written into the table so the acceptance is a record rather than a silence. Frames: 4 `.txt` and
their `.svg`, plus 2 gallery artefacts.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **inc53 · Ruling D: channels are count, weight, position and direction; diameter alone is not a
> channel**
> Write it into the rule's docstring in `tests/test_components.py` and into `collision_census.py`'s
> header. Consequences to fix now: swiss radio knob `●` beside `REQUIRED •` (same shape, diameter only):
> the knob takes a cell distinct by count or weight from swiss's own ladder (`▫ ▪ ■` is the button's; the
> radio may use the ring/disc pair `○ ●`? no: `○` vs `•` is still diameter; use a mark distinct by shape
> family, e.g. the slab `▮` is the caret, so pick from swiss's alphabet with a citation, or make the knob
> a count: `••` is two marks, count). darkside field leader `◦` beside `LEVELS["warn"] = o` (homoglyph):
> the leader takes a non-letterform cell from darkside's alphabet (its `▏` seam, its `·`? check `·` is
> `LEVELS["info"]`: no). Accepted and left as is, with the reason written: industrial `▪ → ▶` beside `▼`
> (direction), solari `▁ → ▮` (shape family), darkside `O → ▊` (weight), darkside knobs `◎ ◉` (count).
> Add a homoglyph table to the census: pairs the census treats as the same drawing (`• ●`, `○ O`, `o ◦`,
> `· ∙`, `▪ ■`? decide and list) so `collision_census.py` flags a meaning mark whose homoglyph is chrome;
> print the rows it adds and fix the ones this ruling covers. Frames changed: swiss S3/S6 (radios),
> darkside S1/S2 (field rows); explain any other.

---

## 1. The definition, written in both places

`prototypes/collision_census.py`'s module docstring and `tests/test_components.py`'s section head now
carry the same four lines, each with the increment that spent that channel:

```
COUNT      how many marks.        `◎ ◉` against `· o O`  (inc49)
WEIGHT     how much ink.          `O` against `▊`        (inc45)
POSITION   where the mark stands. a caret inside a value against chrome at an opener (inc48/49)
DIRECTION  which way it points.   `▪` against `▶`        (inc45)
```

**This is the word the corpus has been leaning on since inc45 §0** — *"unless the two are distinct on a
channel that language declares (count, weight, tier, position)"* — and `VERIFY.md`'s *"assert
distinctness on the channel that is LEFT"*. Until now the list was a parenthesis in one increment's
prose. `tier` is not in the ruling's four and it survives anyway, in one place and by name: the
`DANGER_IS_THE_TOP_RUNG` exemption, which is a rung said as a form. It is a declared channel of one
kit's own ladder, not a general one, and inc52 wrote its scope down.

## 2. The homoglyph table — decided, listed, and narrower than it could have been

```
• ●   BULLET / BLACK CIRCLE            the solid disc
· ∙   MIDDLE DOT / BULLET OPERATOR     the small solid disc
○ O   WHITE CIRCLE / LATIN O           the ring
o ◦   LATIN o / WHITE BULLET           the small ring
▪ ■   SMALL / FULL BLACK SQUARE        the solid square
```

**They are PAIRS and not FAMILIES, and that is the decision the ruling's question mark left open.**
Chaining `· ∙ • ●` into one transitive family puts a MIDDLE DOT and a BLACK CIRCLE in one drawing — a
tenfold difference a reader separates at any cell height — and it was measured before it was refused:
**19 rows against 5.** Adjacent sizes only.

**`▪ ■` is in the table and costs nothing today (zero rows).** It is listed on the same argument as
`• ●` rather than left out because it happens to be quiet; it is the pair that would catch a language
moving a meaning onto one square while its chrome holds the other. Said out loud so nobody reads its
silence as an oversight.

**The check is asymmetric and the ruling's words are why:** *"flags a meaning mark whose homoglyph is
chrome"*. One side an A-family, the other side a B-family. Two chrome cells that are one drawing are an
ALPHABET — the same call the census already makes for B×B — and two MEANINGS that are one drawing is a
question the census asks of the cell itself and would answer twice here. Both directions of each pair are
read, so it does not matter which of the two a kit declared first.

**Homoglyph rows are NOT added to the per-language counts.** A homoglyph row is a question about two
drawings; the count is a question about one cell. Folding them in would have made `TOTAL 33` mean two
different things.

## 3. What it found on first run — five rows, and which are fixed

| language | the row | verdict |
| --- | --- | --- |
| **swiss** | `•` is `REQUIRED` and its homoglyph `●` is `radio` chrome | **FIXED** (§4) |
| **darkside** | `o` is `LEVELS["warn"]` and its homoglyph `◦` is `radio` chrome | **PRINTED.** The ruling covers the FIELD LEADER, which is fixed in §5 — and the leader is invisible to this census either way, because `field_row` draws it outside `PART_GLYPHS` (inc49 §11's limit). What the census sees is `radio.knob[default]`, which the ruling does not name. |
| **naught** | `∙` is `LEVELS[error]`+`DANGER_FORM` and `·` is checkbox+stepper+switch+textfield chrome | **PRINTED.** naught's whole alphabet is one round pixel at six charges (`⋅ · ◦ ∙ ◉ ●`), so a homoglyph table over round dots is a table over this language's entire vocabulary. spec §11.5 in writing: *"naught and solari have no unspent cell left"*. Decision **A**. |
| **naught** | `·` is the INVALID rune and `∙` is switch+textfield chrome | **PRINTED.** Same. |
| **ledger** | `·` is the INVALID rune and `∙` is `textfield` chrome | **PRINTED.** |

Roster and self-check: `HOMOGLYPH_ROSTER` in `collision_census.py`, all eleven, exact — the same bargain
the suite's rosters make (*a number is a record only while somebody has to edit it*), plus
`assert any(...)`, which is what keeps a broken pair list from printing a clean corpus.

## 4. swiss: the chosen option leaves the round family

```
before   "radio.knob": {DEFAULT: "╵● ", FOCUSED: "╹● ", ACTIVE: "▀● ", DISABLED: "╎● "}
after    "radio.knob": {DEFAULT: "╵▪ ", FOCUSED: "╹▪ ", ACTIVE: "▀▪ ", DISABLED: "╎▪ "}
```

`REQUIRED` is `•` and inc46 moved the chosen option from `•` to `●` — **which is the same solid disc at
the next size up.** swiss's whole round family is `· • ●`, one disc at three diameters, so there is no
round cell to move to.

**COUNT was available and was refused with the bill named.** `╵••` is two marks against `REQUIRED`'s one,
which is the ruling's own suggestion — and it puts `REQUIRED`'S OWN CELL at a `radio.knob` seat, the seat
inc49's law names, taking swiss from a clean `MEANING_AT_A_NAMED_SEAT` of **0** to a counted roster.
inc51 §4 paid a bill like that at the declaration rather than exempting it; here a cheaper answer exists,
so the bill is not incurred at all.

**The cheaper answer is that the distinction the bullet carried is ALREADY DRAWN.** A checkbox here leads
with a FULL-HEIGHT rule (`│ ┃ █ ┆`) and a radio with a HALF-HEIGHT tick (`╵ ╹ ▀ ╎`), in every state —
weight and extent, this language's declared channel (*"hierarchy by weight, generous emptiness"*). The
bullet's SHAPE was a second channel saying the same thing, and it is what cost `REQUIRED` its cell. So
both controls set the square bullet this language already sets inside a box, and the rule that leads them
says which control it is.

**The doctrine this overturns is named rather than dropped.** The kit's comment read *"a square bullet
marks a box, a ROUND bullet marks a choice"*. It is rewritten to say where the distinction went, and the
test asserts it there: `checkbox.knob` and `radio.knob` have the same state set, differ in their FIRST
cell in every state, and are identical in every other cell.

## 5. darkside: the field leader leaves the letterform ring

```
before   f"[{c['dim']}]{mark('◦')}[/] "
after    f"[{c['dim']}]{mark('▔')}[/] "
```

`LEVELS["warn"]` is `o `, and `◦` is that ring one size down — so the seat under every figure in the
detail pane and the middle rung of the severity ladder were one drawing. **A LETTERFORM LADDER can only
be kept clear of by leaving the letterform family.**

**And there is a second reason, which is another law's.** `◦` is `LG.NA.OFF`, naught's own unlit pixel,
and `verify_language` holds *"naught's pixel pair is exclusive to naught ON THE BOARD"*. That law is
scoped to the meter, so this row sat just outside it — drawing another language's signature cell six
times per frame.

**`▔` is the `RAIL` turned ninety degrees**: the same one-eighth stroke, the lightest weight the block
family has, which is what a seat under a figure should be in a language whose second word is AIRY. It is
not a rung, not a control's shoulder, not a switch indicator and not a disabled mark — **which is exactly
what `▁` WOULD have been** (`indicator[DISABLED]`), and that is why the seat is the upper eighth and not
the lower one.

**It is deliberately NOT the rail itself, and the reason is inc48's measurement rather than a taste.**
The ruling suggests `▏`. inc48 tried `▏` here and recorded why it refused: `darkside_S1`'s objection is
that this language *"se prohibió el trazo vertical en el único sitio donde hacía falta y lo imprime
catorce veces donde no"*, and routing the detail pane's six field rows through the rail took that frame
from **16 vertical strokes to 22**. That frame is round-2's decision **E**, still open. `▔` is
horizontal, so it costs that count nothing — the fix does not prejudge the decision.

## 6. The four accepted moves, with the channel each spends

Written into `HOMOGLYPHS`' own comment block, because an acceptance that lives only in a packet is a
silence:

| move | channel | why it is not a homoglyph |
| --- | --- | --- |
| industrial `▪ → ▶` | **DIRECTION** | a square against a pointer — two drawings |
| solari `▁ → ▮` | **SHAPE FAMILY** | a ground against a slab |
| darkside `O → ▊` | **WEIGHT** | a letterform ring against a stroke |
| darkside knobs `◎ ◉` against `· o O` | **COUNT** | two concentric strokes against one (inc49 §5, which refused `○` on this ground and said so at the seat) |

The fifth of `PROTOTYPE-inheritors-2.md` §0b's list — swiss `• → ●` — is the homoglyph, and it is §4.

## 7. Teeth

Three tests, and two of them were watched fail on the real declarations.

- **`test_swisss_chosen_option_is_not_the_obligation_mark_at_another_size`** asserts about the PAIR and
  not about the new cell, so it still bites if somebody picks a different answer later: no cell of any
  `radio.knob` state may be `REQUIRED`, **and none may be `REQUIRED`'s HOMOGLYPH** — the second clause is
  the one inc46 walked past. Then it asserts where the box/choice distinction went.
- **`test_darksides_field_leader_is_not_a_severity_rung_at_another_size`** reads the RENDERED ROW,
  because no census can see this mark. The leader is ISOLATED rather than searched for — everything
  between the end of the caption and the start of the figure, stripped, asserted to be one cell — so the
  assertion cannot be satisfied by a letter of `status` or `open`. (Its first draft skipped those letters
  by name and would have passed a leader of `o`; that is why it is written this way.)
- **`test_the_homoglyph_table_is_one_table_in_two_files`** loads `collision_census.py` and compares the
  tuples. Two copies of a list is two lists.

**Watched fail, by hand, on the real declarations.** swiss's four `▪` reverted to `●` and darkside's
`▔` to `◦`:

```
$ python -X utf8 -m pytest tests/test_components.py -q -k "chosen_option or field_leader"
E       AssertionError: ('default', '╵● ', '●')
E       assert '●' not in '╵● '
>       assert _twin(leader) not in rungs, (leader, _twin(leader), sorted(rungs))

$ python -X utf8 prototypes/collision_census.py
AssertionError: HOMOGLYPH ROSTER: swiss has 1 row(s), the roster says 0:
                [('•', ['required'], '●', ['radio'])]
```

**Three instruments, three reds, one for each thing that moved.** `language.py` was restored from a byte
copy taken before the experiment; the three tests re-run green and the census exits 0.

## 8. Census delta

```
                       inc52   inc53
colliding cells (TOTAL)   33      33
homoglyph rows (TOTAL)     —       4      (5 on the run before the two fixes)
```

**The collision count does not move, and that is the point of keeping the two tables apart.** Nothing
this increment did put a meaning on a chrome cell or took one off: swiss's `●` and `▪` are both chrome,
and darkside's leader was never in `PART_GLYPHS` at all. The homoglyph section is where the work shows.

## 9. Frames changed — 4 `.txt` and their 4 `.svg`, and the ruling's prediction was wrong twice

```
darkside_S1   darkside_S3   darkside_S4   swiss_S2
```

**The ruling expected `swiss S3/S6` and `darkside S1/S2`. Explained from the call sites in
`screens.py`:**

| call | line | screens it reaches | what actually moved |
| --- | --- | --- | --- |
| `k.radio_group(...)` | `screens.py:355`, inside **`s2`** | S2 only | **swiss_S2**, not S3/S6 — no other screen draws a radio group. S3 draws switches, a select and a slider; S6 draws the match strip. |
| `k.field_row(cap, val, right)` | `screens.py:261`, the detail pane of **`s1`** | S1 — **and S4**, which overlays a modal on S1's page and leaves the rows under it legible | **darkside_S1 and darkside_S4** |
| `k.field_row("danger zone", ...)` | `screens.py:422`, inside **`s3`** | S3 | **darkside_S3** — the danger-zone CAPTION is a field row, which is the same fact `PROTOTYPE-inheritors.md` §2 read as "caption and control open alike" |

So the leader moved on three darkside frames rather than two, and the radio on one swiss frame rather
than two. **`darkside_S2` has no field row and no radio group** — its form rows are built from
`k.textfield` and `k.checkbox` directly.

```
darkside_S1/S4   status                         ▔ open        (was ◦ open)
darkside_S3      danger zone     ▔ delete every completed task
swiss_S2         priority      ╵   low  ╵   norm  ╵▪  high     (was ╵●  high)
```

**Gallery: 2 of the 22 — `gallery_swiss.{txt,svg}`**, the component strip's four radio rows
(`╵● mid` → `╵▪ mid` at default/focused/active/disabled). `gallery_darkside` did NOT move: the board
capture draws no field row, which is the same measurement §9's table makes from the other side.

**Of the eight frames whose gallery copies live in the skill, one moved: `darkside_S4`** — the same one
inc52 moved. `gallery_swiss` is a board capture and is not among the eight.

## 10. Gates, verbatim

```
$ python -X utf8 -m pytest -q
1070 passed, 2 skipped, 4 warnings in 33.91s

$ python -X utf8 prototypes/verify_language.py                                        exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
  -> 4 of the 66 moved

$ python -X utf8 prototypes/components/matrix.py                                      exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                                      exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 2 of the 22 moved (gallery_swiss.txt, gallery_swiss.svg)

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  1 of the 5 collisions the round found by hand still come back out of
              the census; 4 are asserted CLOSED and cannot grow back
  self-check  the homoglyph roster is exact for all eleven (4 rows, 3 languages)
  TOTAL  33 -> 33     ·     TOTAL homoglyph rows  4
```

**`1067 → 1070`: +3**, the three tests in §7. The clipboard test is green again this run.

## 11. Risks

- **swiss's checkbox and radio now set the SAME bullet.** They are told apart by the rule that leads
  them — full height against half height — which is drawn in every state and is this language's declared
  channel. It is one channel where there were two, and a reader who has learned the bullet's shape has
  learned nothing. **The kit comment says so; the operator may prefer the count answer and its bill.**
- **`▔` is a one-eighth stroke at the TOP of the cell, and the figure sits beside it, not on it.** The
  docstring's phrase is *"the figure stands on one mark of its own"*; an upper eighth reads more like a
  tick than a plinth. The lower eighth `▁` would have read better and is `indicator[DISABLED]`, which is
  a named seat — so the better drawing was unavailable for a law's reason.
- **darkside's radio still draws `◦`**, whose homoglyph `o` is `LEVELS["warn"]`, and the census prints it
  every run. The ruling covers the leader; this is not fixed and not exempted.
- **Ruling D reaches two LADDERS that this increment did not touch, and they are the largest thing it
  leaves open.** swiss's button ladder is `▫ ▪ ■` (inc46: *"ONE SHAPE AT THREE WEIGHTS"*) and
  industrial's severity ladder is `▫▫ ▪▪ ■■` (*"severity is the square's SIZE"*). Both are one square at
  three DIAMETERS. Neither is reachable by this increment's check — swiss's is chrome on both sides, and
  industrial's three rungs are ONE declaration, which every instrument here counts as one — but **the
  ruling's own words say the channel they claim is not one.** Named in §12; not fixed.
- **The homoglyph table is a judgement about DRAWINGS made from code points.** `o`/`◦` are one ring in
  most terminal fonts and two shapes in some; the `.svg` carries no font metric (round-2 E2). The table
  is the corpus's declared answer, not a measurement.

## 12. Found by looking, not fixed

- **swiss `▫ ▪ ■` and industrial `▫▫ ▪▪ ■■` are diameter ladders** (see §11). industrial's is a SEVERITY
  ladder, which makes it the more serious of the two: LANGUAGES.md §3 says this palette *"FAILS WHEN
  COLOUR MUST CARRY SEVERITY"*, so the square's size is all it has — and ruling D says size alone is not
  a channel. **The two statements cannot both be right, and this increment did not have to choose
  because a ladder is one declaration everywhere in this corpus.** It is the sharpest open consequence of
  the ruling.
- **naught's alphabet is a diameter ramp end to end** — `⋅ · ◦ ∙ ◉ ●`, six charges of one round pixel,
  which LANGUAGES.md §0 calls *"how many are lit is the signal"*. Under this table two of its rows are
  homoglyph rows and there is no unspent cell (spec §11.5). Decision **A**.
- **`Darkside.LEVELS`' comment still cites a `CUR` that moved in inc45** (inc49 §11, inc51 §10, still
  true), and **`Darkside.tabs()` and `wordmark()` still print `(O)`** outside `PART_GLYPHS`.
- **`field_row` is drawn outside `PART_GLYPHS` in every one of the eleven**, so the census can reach none
  of the eleven leaders. Only darkside's was named by the ruling; ten others are unmeasured by any
  instrument in this repo.

## 13. Pending — not this increment

- **inc54 (Ruling C1)** — the destructive default answer is a button that carries the knockout.
- **Decisions A, E, F, G, K2, K4, L1–L6, C2, C4–C7** — the operator's, untouched.

## 14. Suggested next task

**inc54 — Ruling C1**, `blueprint_S4`'s DELETE, which is built with `knockout_cell` and therefore carries
no danger mark and no focus mark in either tier.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `1070 passed, 2 skipped, 0 failed` (§10). The
      environment-coupled `test_win_clipboard_roundtrip` is green this run; reported, not counted, not
      touched. `verify_language.py` ALL PASSED exit 0. `render.py` 66/330/0, 4 of 66 moved.
      `matrix.py` 66 of 66. `capture_languages.py` 22 captures, 2 moved. `collision_census.py` both
      self-checks green, 33 → 33, homoglyph rows 4. Both new laws AND the census roster were watched
      fail by hand on the real declarations; the output is pasted verbatim in §7.
- [x] **No secrets in code or output** — one glyph-table slot, one literal in a kit method, one table and
      one roster in the census, three test functions. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The watch-it-fail experiment used a byte copy of `language.py` and
      restored from it.
- [x] **File count within cap** — 3 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`, `prototypes/collision_census.py`); the 8 frame artefacts, the 2 gallery
      artefacts and the census table are written by gate scripts.
- [x] **Review packet attached** — this document.

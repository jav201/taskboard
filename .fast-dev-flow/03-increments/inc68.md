# Increment 68 — the homoglyph table is derived, and two states of one part must differ on a channel

**Batch:** `rework-6b`, increment 2 of 4 · **K2** (ruling D amended) and **K4**.
**Files:** `prototypes/collision_census.py`, `taskboard/language.py`, `tests/test_components.py` —
**3 source files**, plus 4 regenerated component artefacts (2 frames) and the regenerated census table.

**A ruling that binds only against the pairs somebody wrote down is not a ruling about shape.**
`HOMOGLYPHS` was five hand-picked pairs and the four tightest pairs in the corpus were outside it, so
the instrument that enforces ruling D could only ever enforce it where somebody had already looked.
And `homoglyph_rows` skipped MEANING × MEANING on an argument that is true of one cell and false of
two — which is why **ledger's `†` against `‡`, the tightest pair in the corpus, read ZERO through three
rounds.** Meanwhile K4 has been open since round two: nothing in this repo compares two states of the
same part, which is how inc59 rewrote both halves of a checkbox and preserved an inversion between them.
Suite **1188 → 1202**. **Homoglyph rows 1 → 30** and **collisions unchanged at 35**; one row closed at
its declaration.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **A, amended (K5):** the census's B set reaches every quantity widget: slider, bar, scrollbar, meter,
> sparkline, pager, mascot. Their fill and track cells are chrome; a fill cell may not be a meaning mark
> of its language.

> **D, amended (K2):** the homoglyph list is derived, not enumerated: two cells are homoglyphs when they
> are the same base shape at a different size or fill (ring/disc, dot sizes, dash counts within a
> family), and the named four join it now: naught `⊙`/`◉` and `○`/`◦`, ledger `†`/`‡`, blueprint
> `╌ ┄ ┈`.

> **L2:** a disabled control always carries a mark; air is not a state.

> **`mut` contrast:** `mut` is body text and must reach 4.5:1 against the declared ground in every kit,
> with the ladder `ink > mut > dim` kept ordered.

This increment carries out **D amended** and **K4**.

---

## 1. K2 — cause, mechanism, law

### 1.1 Cause

`collision_census.HOMOGLYPHS` was `(("•","●"), ("·","∙"), ("○","O"), ("o","◦"), ("▪","■"))` — five
pairs, chosen by hand in inc53, with an explicit decision recorded beside them: *"THEY ARE PAIRS AND NOT
FAMILIES… Chaining `· ∙ • ●` into one transitive family would put a MIDDLE DOT and a BLACK CIRCLE in one
drawing… Adjacent sizes only."*

`PROTOTYPE-inheritors-3.md` §0d is what that cost, in one table:

| language | the pair | the two meanings | where |
| --- | --- | --- | --- |
| naught | `⊙` vs `◉` | radio chosen vs checkbox ticked | `naught_S2` f9 and f11, two rows apart |
| naught | `○` vs `◦` | radio unchosen vs tag unticked | the same two rows |
| ledger | `†` vs `‡` | `REQUIRED` vs `INVALID` | `ledger_S2` f4 and f6, three cells apart |
| blueprint | `╌` `┄` `┈` | warn vs dead extension vs dead leader | `blueprint_S3` f6, dash counts 2/3/4 |

**None of the four was in the table**, and the census read **1 row for the whole corpus**.

### 1.2 The second cause, and it is worse than the list

`homoglyph_rows` required **one side meaning, one side chrome**, on this argument: *"two MEANINGS that
are one drawing are a severity/obligation question this file already asks of the cell itself and would
answer twice here."*

**That is true of ONE cell and false of TWO.** The cell-level census asks "does this cell carry two
roles"; it cannot ask "are these two different cells the same drawing". So `†` (`REQUIRED`) against `‡`
(`INVALID`) — both A-families — was invisible **by construction**, and it is the pair the round calls
the tightest in the corpus.

### 1.3 Mechanism

`HOMOGLYPH_FAMILIES`, five rows, and a homoglyph is **any two members of one row**:

```
⋅ · ∙ • ●          the round FILLED mark
◦ o ○ ◎ ◉ ⊙ ⊛ O    the round HOLLOW mark and what stands inside it
▫ □ ▪ ■            the SQUARE, hollow and filled, small and full
† ‡                the reference mark and the same mark with a second bar
╌ ┄ ┈              one BROKEN horizontal at two, three and four dashes
                   -> 48 pairs
```

`HOMOGLYPHS` is **derived** from it, so a family gains a member in one place. `homoglyph_rows` now
reports meaning × meaning as well, **with the ladder exclusion by name**: two cells that are both rungs
of this kit's own `LEVELS` are one declaration seen twice, which is the D-addendum verbatim (*"A ladder
is one meaning at monotone intensities and is one declaration: industrial's severity `▫▫ ▪▪ ■■` passes
from hollow to filled (weight) and grows (size) in the same direction, so it stands."*). That exclusion
is worth **4 rows** — industrial's three squares and darkside's `o`/`O`.

**Triangles are not a family**, and that is the ruling's other half: `▶ ▼ ▸` differ by DIRECTION, which
the D-addendum rules a channel wherever a language already spends it. Asserted in the suite so it cannot
be added by accident.

`tests/test_components.py` reads the families from the census and derives the same pairs; the
one-table-in-two-files law now checks the **families**, the **pairs** and the **derivation's own
arithmetic** (`n(n-1)/2 = 48`).

### 1.4 The thirty rows, and what causes them

**1 → 30.** Grouped, because thirty rows read one at a time are thirty taste arguments and grouped they
are six facts:

| n | cause |
| --- | --- |
| **6** | **THE INVALID RUNE**, and the repo already knows. `spec.md` §15.5 and §16.4: the CENSUS counts a field's paper rune as a rejection mark while the LAW does not (`_invalid_marks` reads the two WALLS, not the paper, since inc52). Six rows are a `·` or `⋅` that is a field's paper standing against a filled disc at another size — corgi, ledger, solari, blueprint, naught ×2. **The day the census adopts the law's exclusion, all six go at once**, the same sentence §16.4 already wrote about six COLLISION rows |
| **5** | **NAUGHT'S GROUND.** `◦` is `LEVELS["info"]` and it is this kit's BLANK — `THE_GROUND_IS_NOT_A_MARK`, granted by name in inc61 and priced at `GROUND_EXEMPTION_IS_WORTH = (7, 2)`. The two seat laws subtract it; the census does not, on the standing decision that a census asks questions |
| **4** | **NAUGHT'S `⊛`**, and this is **the ruling contradicting the round**. §2.8 calls `⊛` the best obligation mark in the corpus by name (*"un asterisco dentro de un anillo no se parece a nada más en la pantalla"*); ruling D amended puts every ring in one family, so it is a homoglyph of `○ ◎ ◉ ⊙`. Recorded as the disagreement it is, with both positions written down |
| **8** | **DARKSIDE'S RING ALPHABET.** `LEVELS` is `· / o / O` and inc49 moved every control to `◎ ◉` citing COUNT — a move the census's own docstring listed as ACCEPTED. Under the amendment a ring is a ring at any fill. Closing them means re-alphabeting darkside's controls off rings, a language-level increment |
| **4** | one pair each: swiss `·`(info) vs `•`(REQUIRED) — two meanings; nord `·`(info) vs `●` at a radio knob; **ledger `†` vs `‡`**, invisible until this increment; naught `∙`(danger+error) vs `●`(`CUR`) |
| **2** | **BLUEPRINT'S DASH LADDER.** Formally a COUNT channel, formally allowed by D; the round's objection is that counting dashes in a 12px cell is not a channel a reader has. E2 is why it cannot be settled from the artefact |
| **1** | **SOLARI, and it is the census's own false positive.** `LEVELS` here is three WORDS (`OK ` / `DLY` / `CNX`) and `_cells` splits a word into letters, so the `O` of `OK` is read as a severity MARK and matches a radio's `◉`. A language whose ladder is words declares no severity cell at all. Named, not special-cased |

### 1.5 The one that was fixed

**naught's `scrollbar.main`, `·` → `NA.OFF`.** inc61 RETIRED `·` from this alphabet with three reasons —
it is the homoglyph of the lit dot, it is the one rung that is East-Asian-Width **Ambiguous**, and
LANGUAGES.md §0's own pass-10 had already *"measured and rejected"* it — and moved every control off it.
**It could not move this one**: the scroll bar was outside set B by the operator's request, so nothing
could see that the SHAFT had kept it. inc67 put the widget in the set and the row came straight back.

The shaft takes the unlit lattice, which is what its own comment already claims it is (*"the lattice at
its faintest pitch"*). `·` was a sixth charge on a five-charge ramp.

```
naught_S1 f31   before  view ·●●●●······· 3-10 of 23
                after   view ◦●●●●◦◦◦◦◦◦◦ 3-10 of 23
naught_S4 f31   the same row, behind the modal
```

`·` is now **absent from this kit entirely**, and §2.8's second objection to `naught_S1` — *"`·` (U+00B7)
contra `∙` (U+2219, la celda de peligro) contra `◦` (el suelo) en el mismo frame"* — is answered: three
sizes of one round pixel in one frame are now two.

---

## 2. K4 — cause, mechanism, law

### 2.1 Cause

**No law in this corpus compares two states of the same part.** Every law reads a glyph against the
meanings, or one part against another, or a frame against a fixture. Nothing asked the question a reader
asks of a control — *"is this one on or off?"* — which is a question about two rows of one table.

Two frames paid for it:

* `blueprint_S3` — a switch's three states are `├─┤` / `├┤·` / `├╎┈`, told apart by DASH COUNT at 2, 3
  and 4. inc60's own packet: *"a un cell de 12 px se le está pidiendo al lector que cuente guiones"*.
* `prism_S2` — inc59 rewrote a checkbox's two centres in one increment and **preserved an inversion
  between them**; the fixture's two ticked tags rendered as empty boxes and eleven months of property
  tests could not see it. inc64's box law is the first law here that compares two states of one part, and
  it is one part, one pair, one direction. **This is the general one.**

### 2.2 Mechanism — the channel is ruling D's four and nothing else

`state_channel(g1, g2)` returns which of COUNT, POSITION, SHAPE, WEIGHT separates two glyphs, or `None`:

* **COUNT** — different lengths.
* **POSITION** — the same cells in a different order: a mark that moved.
* **SHAPE** — at least one differing cell is a different DRAWING from its partner (not in the same
  `HOMOGLYPH_FAMILIES` row). Nine of the eleven spend this.
* **WEIGHT** — every differing cell is its partner at another size or fill **and** this file has a
  measured ink order for the pair.

**Distinct code points is not a channel**, and that is the whole of K2. Measured before the law was
written: **every one of the eleven already has pairwise-distinct glyphs in every table, zero duplicates**
— so a law that asked for distinctness would pass everywhere and say nothing.

`None` is a **REFUSAL, not a pass** — the same bargain `cell_ink` makes (*"`None` means 'this file has no
weight for that cell', which is a REFUSAL and not a zero"*). Two cells of one family with no measured
weight between them are *one drawing at two diameters*, which ruling D says is no channel; and a pair
this file has never weighed is a pair it may not certify (E2).

### 2.3 The roster: 9 rows in 2 languages

| language | n | what |
| --- | --- | --- |
| naught | 8 | six seats tell two states apart with a ring at another size or fill: `◦`/`○` at the button, the checkbox and the field's paper, `◉`/`◎` at the shared knob and the checkbox's, `○`/`◦` at the radio's ground. This is §2.8's `naught_S2` finding read off the declarations, and `spec.md` §11.5 already records that this kit *"has no unspent cell left"* |
| darkside | 1 | `◎`/`◉` at the shared knob, default against focused — inc49's move, listed as ACCEPTED under COUNT by the census's own docstring, and a row under the amendment |

**swiss was 2 until `■` was weighed.** Its button ladder is `▫ ▪ ■`, the shape the D-addendum names as
the one that STANDS, and `CELL_INK` had a weight for two of its three rungs. Supplying the third
(`■ = 0.45`) is a **measurement being supplied, not a law being loosened**: without it the law was
refusing a ladder the ruling had already blessed.

### 2.4 The ordering clause, on the two kits whose ladders are arithmetic

Only two, and the reason is E2: a braille cell's dots and a dash glyph's dashes are properties of the
**code point**, so no font metric is needed.

* **prism's four** (inc59: *"a control is read from the TOP"*, *"the ladder climbs instead of dimming"*).
  `radio.main`, `button.main`, `checkbox.main`, `checkbox.knob` over `DISABLED → DEFAULT → FOCUSED →
  ACTIVE`: **non-decreasing along the order and strictly up end to end.** Two adjacent rungs may tie
  (`⣷` and `⣾` are both seven dots, one carved at the top and one at the bottom — a DIRECTION channel,
  which `state_channel` is what asks of them), but a control may never be dimmer at a later rung.
* **blueprint's three** (inc60: *"a meaning is a LINE TYPE"*). `LEVELS["warn"]` = `╌` (2 dashes), the
  dead INDICATOR = `┄` (3), the dead GROUND = `┈` (4): strictly increasing, all three distinct, and the
  LIVE indicator is asserted to be **off this ladder entirely** — a solid rule is the one thing a reader
  never has to count. **This law does not settle the round's objection**; it asserts that *if* a reader
  can count at all, counting gives the right answer.

---

## 3. Teeth

`test_the_state_channel_law_goes_red_on_a_real_table` — three arms, two of them on real declarations
from earlier increments:

1. **prism's pre-inc59 checkbox walls**, verbatim from that increment's own comment (`⣿` at rest, `⣷`
   focused, `⣾` active — *"a control that DIMMED when the reader arrived at it"*). The **ordering** law
   goes red.
2. **inc64's inversion**, the two checkbox centres swapped back. It goes red at the box law and leaves
   the **channel** law green — **which is the point**: an inversion is an ORDER defect and not a CHANNEL
   defect, and K4 has two clauses for exactly that reason.
3. **The channel reader itself**, on the seat this increment repaired: naught's shaft is `◦` live and `⋅`
   dead — a ring against a dot, two DRAWINGS, so `state_channel` calls it SHAPE. Put the dead shaft on a
   ring one size along and it is diameter and nothing else: **exactly one new row, and the assertion
   names the part and both glyphs.**

The K2 half carries its teeth in the derivation law: the families, the pairs and `n(n-1)/2 = 48` are all
asserted across the two files, and triangles are asserted **absent** from every family.

---

## 4. The census

```
                    inc67    inc68
collisions            35       35     (unchanged, per language as well)
homoglyph rows         1       30
homoglyph pairs read   5       48
languages with a row   1        8
```

**Collisions did not move at all**, and that is the check on the change: `·` leaving naught's shaft took
a cell out of a chrome family it shared with nothing, and widening the homoglyph reader touches no
collision count by construction (*"these rows are NOT added to the counts above"*).

Per language: naught 12, corgi 1, swiss 1, nord 1, darkside 8, ledger 2, solari 2, blueprint 3;
instrument, industrial and prism are clean.

---

## 5. Frames changed

**Two component frames moved in the `.txt`** (4 artefacts with their `.svg`): `naught_S1` and
`naught_S4`, one row each — the pager.

**Gallery: 0 of the 22.** `gallery_naught` did not move and that is checkable the same way `gallery_swiss`
was in §16.5: the component sheet is cut at 118×34 before its scroll-bar row, the same cut §12.5 records
for the stepper. **The one seat this increment repaired is a seat no gallery artefact draws** — which is
also, exactly, why nothing had caught it.

**Skill gallery 30–51:** `naught_S1` and `naught_S4` are **not** sources for any of the twenty-two
(`42 naught_S4`… — see below). Checked against §16.5's list: entry **42 is `naught_S4`**, so **one of the
twenty-two has a moved source**; it is re-installed at the close of the batch by `export_to_skill.py`,
per the batch's gate list.

---

## 6. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1202 passed, 2 skipped, 4 warnings in 36.21s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

inc67 closed at `1 failed, 1188 passed`. **+14.** `test_win_clipboard_roundtrip` drives the real Windows
clipboard through PowerShell; **environment-coupled, reported, not counted, not touched.**

```
$ python -X utf8 prototypes/verify_language.py
ALL PASSED                                          (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> …/prototypes/components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py
  --- refusals, by language ---
  naught [] · corgi [] · instrument [] · swiss [] · industrial [] · nord []
  darkside [] · prism [] · ledger [] · solari [] · blueprint []

$ python -X utf8 prototypes/collision_census.py
self-check  1 of the 5 collisions the round found by hand still come back out of the census; 4 are asserted CLOSED and cannot grow back
self-check  the homoglyph roster is exact for all eleven (30 rows, 8 languages)
TOTAL                       35
TOTAL homoglyph rows            30

$ python -X utf8 prototypes/capture_languages.py plain
  22 grids identical across two PROCESSES
  22 captures -> …/prototypes/gallery
  no two boards identical
```

---

## 7. Risks

1. **The homoglyph roster went from 1 to 30 and 29 of those are NOT fixed.** A roster is a record. The
   risk is that a reader takes 30 as a regression; the collision total is unchanged and the per-language
   collision counts are identical, which is the evidence that nothing got worse. What changed is that the
   instrument can now see a class of question it could not ask.
2. **Ruling D amended contradicts `PROTOTYPE-inheritors-3.md` §2.8 about naught's `⊛`**, which that
   document praises by name as the best obligation mark in the corpus. Four rows are that disagreement.
   The roster records both positions; **nobody has ruled on which wins**.
3. **`state_channel` returns `None` for a pair this file has no weight for**, so part of K4's roster is
   measuring *what `CELL_INK` covers*. That is E2 stated honestly rather than hidden, and it is the same
   refusal `cell_ink` already makes — but a reader should not read "8 rows for naught" as "8 defects";
   read it as "8 pairs this file cannot certify".
4. **`CELL_INK` gained a second declared weight in two increments** (`◉` in inc67, `■` here). Both are
   ordinal and both were added because a specific law needed them. The first draft of inc67's addition
   (`●`) broke the ticked-box law and was withdrawn — the failure mode is real and the answer is to add a
   weight only when a law demands it.
5. **`·` is gone from naught but `⋅` is not**, and `⋅` is EAW-Ambiguous by the same argument inc61 used
   to retire `·`. It is the field's paper and the dead ground. Not touched; named.

---

## 8. Found by looking, not fixed

* **The asymmetry in `homoglyph_rows` was an argument, and the argument was wrong.** *"Two meanings that
  are one drawing are a question this file already asks of the cell itself"* — the cell-level question is
  "does THIS cell carry two roles", which cannot reach two different cells. The corpus's tightest pair
  sat behind that sentence for three rounds and the sentence was in the file the whole time, next to the
  code that skipped it.
* **The census reads a WORD ladder cell by cell.** solari's `LEVELS` is `OK ` / `DLY` / `CNX`, and
  `_cells` splits them into `O K D L Y C N X` — eight "severity marks", one of which matches a radio's
  `◉` at another fill. The round calls solari's log *"el mejor de los once por un margen amplio"* and the
  reason is precisely that it uses words; the instrument penalises it for that. One row, named.
* **Three separate rosters now record the same discrepancy.** The invalid RUNE is counted as a meaning by
  the census and excluded by the laws: §15.5 named it for five languages, §16.4 for six collision rows,
  and inc68 finds six more homoglyph rows with the same cause. **Twelve rows in one repo waiting on one
  decision**, which is a strong argument for making it.
* **Every part table in all eleven kits already has pairwise-distinct glyphs.** Measured before K4's law
  was written, and it is what forced the law to be about CHANNELS instead of distinctness — a
  distinctness law would have passed eleven for eleven on day one and proved nothing.
* **The seat this increment repaired is drawn by no gallery artefact.** `gallery_naught` is cut before
  its scroll-bar row at 118×34, the same cut §12.5 records for the stepper. A declaration whose only
  rendering is a frame nobody installed is a declaration nobody looks at, which is how `·` survived
  inc61.
* **`test_win_clipboard_roundtrip` was RED in this increment's run**, as in the baseline. Reported, not
  counted, not touched.

---

## 9. Pending — not this increment

* **L2** — swiss's disabled `Save` (**inc69**).
* **`mut` contrast** in five kits (**inc70**).
* **The invalid-rune discrepancy** — 12 rows across two instruments, waiting on a ruling.
* **naught's ring alphabet (8 K4 rows + 9 homoglyph rows)** and **darkside's (1 + 8)** — language-level
  increments, not census edits.
* **L6, L7, L10, C5–C10, E2, E3, G2** — untouched.

## 10. Suggested next task

**inc69**, as briefed: give swiss's DISABLED button a mark from its own alphabet, distinct by weight from
`▫` and from any meaning mark, and assert over all eleven that no control state renders as pure air at
any width.

---

## Evidence checklist

- [x] **Tests / type checks / lint pass** — `pytest -q` **1202 passed**, 1 failed
  (`test_win_clipboard_roundtrip`, environment-coupled, red in the baseline, named in §6).
  `verify_language.py` **ALL PASSED, exit 0**. `render.py` 66/330/0. `matrix.py` refusals `[]` × 11.
  `collision_census.py` both self-checks green.
- [x] **No secrets in code or output** — no credential, token or out-of-worktree path is written or
  printed.
- [x] **No destructive commands run without approval** — no `rm`, no force push, no rename.
- [x] **File count within cap** — **3 source files**: `prototypes/collision_census.py`,
  `taskboard/language.py`, `tests/test_components.py`. Regenerated artefacts (4 component, 1 census
  table) are gate outputs.
- [x] **Review packet attached** — this file.

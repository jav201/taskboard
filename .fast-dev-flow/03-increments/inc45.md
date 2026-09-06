# Increment 45 — one mark, one meaning: the seven A×A cells

**Batch:** `rework-3` (the language-level rework) · answers `spec.md` §10.4 / §10.5 and
`PROTOTYPE-inheritors.md` §7 q5 and q6
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`
— **3 source files**, plus 48 regenerated frame artefacts, the regenerated census table and this packet.

**Six cells in six languages carried two MEANINGS with no control involved — `naught ∙` (severity,
danger, obligation, position), `nord !` (severity, danger), `swiss ━` (error, position),
`industrial ▪` (warn, position), `darkside O` (error, position), `ledger † ‡` (obligation and refusal,
warn and error). All six are closed, and the law written to close them found a SEVENTH the round never
named: `corgi ▄` is `DANGER_FORM` and `LEVELS["warn"]` — the same defect as nord's, one rung further down
its own ladder. The four language-level marks that mean something about the work are now pairwise
cell-disjoint in ALL ELEVEN languages. Census 54 → 53 cells; meaning×meaning with the two named
exemptions subtracted, 15 → 8, and every one of the eight left is `INVALID` against something, which is a
per-part slot inc39 already rules.**

---

## 0. The rule this batch enforces, written once

> A cell that carries a **meaning** — a severity rung `LEVELS[*]`, the `DANGER_FORM`, `REQUIRED`, `CUR`,
> or a declared `INVALID` mark — may not carry a second meaning in the same language **unless the two are
> distinct on a channel that language declares** (count, weight, tier, position); and it may not stand at
> a position in control chrome where a reader would take it for that meaning: **the opener of a control,
> the indicator of a switch, a disabled mark**. Chrome-on-chrome (B×B) is an ALPHABET and is not a
> collision. **Every exemption is by name with a citation in the kit; silence is not an exemption.**

The channel clause is `VERIFY.md`'s own, *"assert distinctness on **the channel that is left**"*: where a
prior load-bearing ruling has frozen one channel, the law moves to the next one rather than being
weakened until it means nothing. Increment 45 enforces the first half — meaning against meaning;
inc48 enforces the second — meaning at an opener.

---

## 1. What moved, cell by cell, with the citation

| language | was | is | which meaning kept the cell, and why | census row |
| --- | --- | --- | --- | --- |
| **naught** `REQUIRED` | `∙` (`NA.ON`) | **`◉`** | The **ladder** keeps the lit dot. LANGUAGES.md §0 is the first sentence of this language: *"quantity is a row of discrete lit dots ... **how many are lit** is the signal"* — the severity ladder IS that sentence (`◦◦ / ∙◦ / ∙∙`, a count). Obligation takes the tier above on the charge ramp `⋅ · ◦ ∙ ◉ ●` this kit already spends across `PART_GLYPHS` (`◉` = *"a dot with an EYE"*, its knob; *"the one LIT dot in the lattice"*, its caret). | `∙` 6 families → 5 |
| **naught** `CUR` | `∙` (`NA.ON`) | **`●`** | Same argument, other end of the ramp: `●` is *"the round pixel at full brightness"* — its pressed key — and position is *"where the current is"*, the phrase `Naught.overlay_instead` uses for operator ruling 4. | new row (A×B) |
| **corgi** `DANGER_FORM` | `("▄","▄")` | **`("█","█")`** | **Found by the law, not by the round.** `▄▄` is `LEVELS["warn"]`: a destructive key and a warning row were the same cell at the MIDDLE of the ladder. `██` is `LEVELS["error"]` — the ladder's TOP rung set as a form, which is the named exemption below. | `▄` 7 → 6; `█` 4 → 5 |
| **nord / `Kit`** `DANGER_FORM` | `("!","!")` | **`("#","#")`** | The **ladder** keeps `!` (ruling 8: `· ` / `! ` / `!!` — one width, three shapes). `nord_S3`'s objection verbatim: *"decir si `!Delete all!` es «peligroso» o «hay una advertencia sobre esto»"* — two correct answers. `#` is the **root prompt**, the environment's own mark for the account that can destroy, and nord's whole commitment is to inherit the environment rather than invent. | `!` 3 families → 1 (gone) |
| **nord / `Kit`** `textfield.main[INVALID]` | `"! !"` | **`"? ?"`** | inc39 gave these walls the `DANGER_FORM` because un-flipping alone collided with DEFAULT byte for byte — **not** because destruction and rejection are one claim. Letting them follow `#` would only have moved the overload. `?` is the environment's own mark for a value it cannot read, and is spent nowhere else in this kit. inc39's law still holds by construction: same mark both sides, no handedness to read a state off. | `?` new, one family |
| **swiss** `CUR` | `━` | **`▮`** | The **ladder** keeps the rule: a weight ladder of HORIZONTAL rules (`· ─ ━`) is this language's entire hierarchy device. `swiss_S1`'s criterion was *"with the colour taken away, say whether DOING is SELECTED or in ERROR"*. `▮` is the solid slab swiss already spends on its edited knob and its pressed checkbox mark, on the **other axis** — and deliberately not a block element or a box-drawing cell, because *"no boxes, at any width"*. | `━` 3 families → 2 |
| **industrial** `CUR` | `▪` | **`▶`** | The **ladder** keeps the squares, and it has nowhere else to go: LANGUAGES.md §3 says this palette *"**FAILS WHEN COLOUR MUST CARRY SEVERITY**, because the palette already spent colour on identity"*, so severity is the square's SIZE (`▫▫ / ▪▪ / ■■`). The cursor leaves the family and takes `DISCLOSE`'s own form — *"solid, flat, stamped"* — turned ninety degrees. | `▪` 2 families → 1 (gone) |
| **darkside** `CUR` | `O` | **`▊`** | The **ladder** keeps `O`: the class docstring is where severity is committed (*"passive data is grey STEPS whose levels ride on SHAPE"*) and `· / o / O` is that commitment. §8's other clause is *"hierarchy by **WEIGHT AND DIMMING**, not size"* and *"depth by ±1 grey step, **never borders**"*. `RAIL` is `▏`, the thinnest stroke this alphabet draws; the cursor is that stroke at full weight. One stroke, two weights, and no border — one mark on one side encloses nothing at any width. | `O` 4 families → 3 |
| **ledger** `LEVELS` | `  ` / `† ` / `‡ ` | **`  ` / `* ` / `**`** | **Obligation and refusal keep the daggers**, because footnote ORDER is this language's stated notation: *"`†` marks the entry that must be made, `‡` ... marks the one that was refused"*. Reference marks are ASSIGNED, not ranked: the printer's order is `* † ‡ § ‖ ¶`, the daggers are spoken for, so the ladder takes the FIRST mark and **doubles** it for the graver note — which is what a compositor does when one mark is not enough. Doubling is not a new channel here: *"quantity is TALLY marks in groups of five — the mechanism used when you **COUNT** rather than measure"*. | `†` and `‡` both 2 families → 1 (both gone) |

**Naught, corgi and ledger had no frame among the sixteen.** Three of the seven cells were invisible to
the round and visible to the census — which is what §10.5 said the census was for.

---

## 2. The two exemptions, by name

**E1 — `DANGER_FORM` may be the severity ladder's TOP rung, set as a FORM.** `Kit.DANGER_FORM`'s own
docstring declares what a danger form is: *"a pair of marks that **bracket the label INSIDE the walls**,
and never a hue ... the form is therefore the WHOLE channel"*. A destructive control and an error row are
one claim about one gravity, so the ladder's top rung said as an enclosure is one meaning wearing two
grammatical forms, not two meanings. Four languages spend it that way and each carries the citation in
its own kit:

| language | form | rung |
| --- | --- | --- |
| naught | `∙ … ∙` | `LEVELS["error"] = "∙∙"` — *"two lit dots, and not the one red"* |
| corgi | `█ … █` | `LEVELS["error"] = "██"` — *"the segment driven to full height"* (inc45) |
| prism | `⣿ … ⣿` | `LEVELS["error"] = "⣿⣿"` — *"nothing left to burn"* |
| blueprint | `━ … ━` | `LEVELS["error"] = "━━"` — *"the HEAVY weight, this alphabet's loudest mark"* |

**It is the TOP rung or nothing**, and that is the exemption's teeth: `nord !` and `corgi ▄` were both
this exemption spent one rung too low, and both moved. The test asserts
`"".join(DANGER_FORM) == LEVELS["error"]` for the four before it grants them anything.

**E2 — `INVALID` is not in the law's set, and the exclusion is named rather than silent.** inc39 ruled
(spec §9.2) that where un-flipping a field's walls would collide with DEFAULT byte for byte, the walls
take that language's own `DANGER_FORM`; five languages spell rejection with their danger form **on
purpose**. A law over `INVALID` would therefore be a law over that ruling, so `INVALID` stays governed by
inc39's own law and this one says so out loud — `VERIFY.md` item 6, *"name the excluded mechanism and its
ruling ... rather than special-casing it silently"*.

---

## 3. The law, and its teeth

`tests/test_components.py`, two new tests plus one rewritten:

- **`test_a_languages_meaning_marks_do_not_share_a_cell[lang]`**, eleven parametrisations. The four
  language-level declarations — the severity **ladder** (all three rungs as ONE declaration, because the
  census counts them as one: *"two severity rungs sharing a cell is a severity problem, not a
  collision"*), `DANGER_FORM`, `REQUIRED`, `CUR` — may not **share a cell**. Not "may not be equal":
  SHARE, because `industrial ▪` against `▪▪` proves that doubling a mark for alignment is not a channel —
  the first cell of the rung is the cursor either way.
- **`test_the_one_mark_one_meaning_law_goes_red_on_the_six_it_was_written_for`**, eight arms. Each arm
  restores exactly the byte string HEAD carried, and the assertion is that **the law names the language
  and the two roles** — `frozenset(("cursor", "ladder")) in roles("swiss")` — not that something,
  somewhere, went red. The eighth arm is the exemption's own teeth: corgi's danger form put back one rung
  DOWN the ladder must be red.
- **`test_ledgers_two_daggers_are_an_order_and_not_a_pair`** now asserts what its title always claimed:
  `†` is `REQUIRED`, `‡` is the invalid wall, **and neither appears in `LEVELS` at all**.

The pair-finding is a module-level function, `shared_cell_pairs(lang)`, and not an inline loop — pytest's
assertion rewriting turns an assert's own message into a formatted string long before a caller can
inspect it, so a teeth test that scraped `AssertionError.args` would have been asserting on a repr. (It
was, for one run; the arm passed against `frozenset({"'"})`.)

`prototypes/collision_census.py`'s self-check changed shape rather than losing rows. `FOUND_BY_HAND` grew
a fourth field, `closed_by`: a fixed row **stays** on the roster with the increment that fixed it, and its
assertion **inverts** — the named families must no longer meet on that cell. So the instrument fires in
both directions (red if the census stops seeing a live collision, red if a language grows a closed one
back), and `assert live` keeps the check from going vacuous when the last row is closed.

```
self-check  3 of the 5 collisions the round found by hand still come back out of the census;
            2 are asserted CLOSED and cannot grow back
```

---

## 4. Census delta

```
language      cells  ->      live A x A  ->      what is left, after the two named exemptions
naught            3  ->   5           1  ->   0   —
corgi             5  ->   5           2  ->   2   ▄ INVALID+severity · ▀ INVALID+REQUIRED
instrument        8  ->   8           1  ->   1   ⠇ INVALID+severity            (inc46)
swiss             8  ->   9           1  ->   0   —
industrial        5  ->   4           2  ->   1   ▐ INVALID+REQUIRED            (inc48)
nord              5  ->   4           1  ->   0   —
darkside          3  ->   3           1  ->   0   —
prism             5  ->   5           1  ->   1   ⡀ INVALID+REQUIRED
ledger            4  ->   2           2  ->   0   —
solari            3  ->   3           0  ->   0   —
blueprint         5  ->   5           3  ->   3   ├ INVALID+REQUIRED · · INVALID+severity · ━ three
TOTAL            54  ->  53          15  ->   8
```

**Two numbers, and the second is the one this increment is about.** The left pair counts every cell that
does more than one job, meanings AND chrome together; the right pair counts only cells carrying two or
more MEANINGS, with E1 and E2 subtracted. **Every one of the eight left involves `INVALID`**, which is
E2's territory and inc39's law.

**And the left number is honest about what it costs.** `naught` goes 3 → 5 and `swiss` 8 → 9 because the
marks their obligation and position moved ONTO were already spent on chrome — naught's whole alphabet is
one round pixel at six charges, so there is no unspent cell to move to, and swiss draws four cells on
purpose ("el hallazgo de swiss es aritmético", the round's own words). Those are A×B rows: the census
calls them *questions*, and the batch rule permits them, because `◉` stands at a knob and a caret and `▮`
at a checkbox mark — **not** at an opener, a switch indicator or a disabled mark. The law is what moved;
the census counts what the law does not govern too, and that is the difference the table is drawn to
show.

---

## 5. Frames changed — 24 `.txt` and their 24 `.svg`

```
corgi_S3 corgi_S4
darkside_S1 darkside_S3 darkside_S4 darkside_S6
industrial_S1 industrial_S3 industrial_S4 industrial_S6
ledger_S2 ledger_S5
naught_S1 naught_S2 naught_S3 naught_S4 naught_S6
nord_S2 nord_S3 nord_S4
swiss_S1 swiss_S3 swiss_S4 swiss_S6
```

Read at the seat each objection named:

```
nord_S2       due*          ?12/09/26                          ?     (was `] … [`, then `! … !`)
nord_S3       [ #Delete all# ]   7 tasks, not recoverable            (was `[ !Delete all! ]`)
ledger_S5     09:41:09 *  3 tasks overdue in BACKLOG
              09:41:18 ** rate limit hit  retry in 30 s              (was `† ` / `‡ `)
swiss_S1      ▮ D O I N G                     4                      (was `━ D O I N G`)
industrial_S1 ▶ ▐▌ [2]DOING                              [ 4]▌       (was `▪ ▐▌ [2]DOING`)
darkside_S1   ▊ ▏  doing 4                                           (was `O ▏  doing 4`)
naught_S1     ● DOING                                                (was `∙ DOING`)
naught_S2     title◉        ○Fix login◉ redirect∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙○     (was `title∙ … ∙∙∙∙∙`)
```

**Of the eight frames whose gallery copies live in the skill** (spec §11's list — `instrument_S1`,
`industrial_S1`, `swiss_S1`, `solari_S1`, `industrial_S4`, `darkside_S4`, `solari_S2`, `instrument_S5`),
**four moved byte-wise this increment: `industrial_S1`, `swiss_S1`, `industrial_S4`, `darkside_S4`.**

---

## 6. Gates, verbatim — AND ONE RED THAT IS NOT MINE

```
$ python -X utf8 -m pytest -q
1 failed, 1016 passed, 2 skipped, 4 warnings in 36.32s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**1004 → 1016**: eleven parametrisations of the new law plus its teeth test. The one red is
`test_win_clipboard_roundtrip`, which drives the real Windows clipboard through PowerShell and fails when
anything else on the desktop holds it (spec §10.6). It is red at HEAD as well — the baseline run for this
batch, before a line of this increment existed, returned the identical failure — and it touches nothing
this increment touches.

```
$ python -X utf8 prototypes/verify_language.py                                        exit 0
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)  worst 3 of 40 over 155 captures
ALL PASSED

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
  -> and all 22 committed files are BYTE-IDENTICAL: no board rendering moved.

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  3 of the 5 collisions the round found by hand still come back out of
              the census; 2 are asserted CLOSED and cannot grow back
  TOTAL  54 -> 53
```

---

## 7. Risks

- **`#` as nord's danger form is a claim about the environment, not about the kit.** The argument is that
  `#` is the root prompt and therefore the terminal's own mark for "this account can destroy". A reader
  who reads `#` as a shell COMMENT gets the opposite reading. It was chosen over `×` because the base
  already spends the cross family on DISABLED (`╳`), and a cross meaning "dead" beside a cross meaning
  "dangerous" is exactly the defect this increment exists to remove. **The operator may prefer another
  mark; it is one line.**
- **`▊` and `▏` are one weight step apart** in darkside, which is the channel that language declares and
  also the channel a 12px cell renders worst. The two never share a column (`RAIL_W` is 3), so the
  reading is by weight in the margin rather than by comparison — but this is a font-dependent judgement
  the `.txt` cannot settle, exactly as `industrial_S5`'s `▪`/`■` cannot be settled in the `.txt`.
- **`naught ◉` is `REQUIRED` and the field's caret**, so `naught_S2` row 4 carries `◉` twice with two
  readings. A caret is a POSITION inside a value, not chrome at an opener, an indicator or a disabled
  mark, so the batch rule permits it — and it is strictly better than what it replaced, where `REQUIRED`
  was `∙` and the EDITED field's own paper was a run of `∙`. Named, not hidden.
- **`ledger **` is two cells of ASCII in a language whose other marks are typographic.** It is the
  printer's own doubling and it keeps `LEVELS` at one width, but it is the least ornamental mark ledger
  now draws.
- **Seven languages moved in one increment.** The brief named six; the law found corgi. Each is a single
  declaration and each carries its citation, but this is the widest single edit of the batch and the
  frames are the evidence.

---

## 8. Pending — not fixed here

- **`instrument` and `swiss`** — inc46. Eight and nine census cells, the two widest left.
- **`solari ▁` and `nord_S1`** — inc47.
- **`industrial ▐`, the caption-as-button in `industrial_S3` / `darkside_S3`, `darkside_S1`,
  `darkside_S6`, and the opener law over all eleven** — inc48.
- **`corgi ▀` is `REQUIRED` and the INVALID wall**, and **`corgi ▄` is `LEVELS["warn"]` and the INVALID
  wall** — two live meaning×meaning rows in a language with no frame among the sixteen and no increment
  in this batch. Found by the census; **not fixed, and not exempted**.
- **`prism ⡀` is `REQUIRED` and the INVALID stepper step**; **`blueprint ├ · ━`** carry three more. Both
  languages are outside this batch's four increments.
- **`Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`** — inc39's unfixed defect (spec §9.5): a stepper's
  halves are directions, not walls. It is why `nord [` and `nord ]` are still census rows.
- **`swiss ━` is still the switch INDICATOR** and `swiss ─` still the switch main — the severity ladder
  drawn as chrome at a position the batch rule names. inc46.
- **`test_win_clipboard_roundtrip` is environment-coupled** (spec §10.6).

## 9. Suggested next task

inc46 — `instrument` and `swiss`, the two languages the census still puts at eight and nine cells, and the
two whose remaining findings are all at CONTROL positions rather than between meanings: `⠇` opening a safe
button, `⠁` as both obligation and DISABLED, `instrument_S4`'s inverted severity, and swiss's remaining
walls.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1016 passed, 2 skipped, 1 failed`; the
      failure is `test_win_clipboard_roundtrip`, red at HEAD before this increment (§6).
      `verify_language.py` **ALL PASSED** exit 0. `render.py` 66 frames / 330 pairs / 0 hand-drawn.
      `matrix.py` 66 of 66. `capture_languages.py` 22 captures, all byte-identical.
      `collision_census.py` self-check green, 54 → 53.
- [x] **No secrets in code or output** — glyph tables and rendered frames only. No network, no new
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force. The commit names its files explicitly.
- [x] **File count within cap** — 3 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`, `prototypes/collision_census.py`); everything else in the commit is
      regenerated by a gate script.
- [x] **Review packet attached** — this document.

# Increment 74 — K7's `dim` clause and L7: which `dim` run classifies, and the seat moves rather than the token

**Batch:** `rework-7a`, increment 3 of 4 · **K7's `dim` clause** and **L7**.
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 20
regenerated component `.svg` and 2 regenerated gallery `.svg`. **No `.txt` moved**, in any of the 66
or the 22 — colour only, for the second increment running.

**`dim` is under 3:1 in all eleven and under 1.6:1 in five.** inc70 measured that and left it as a
roster (`DIM_AGAINST_GROUND`) because raising it is a change in the token ten kits spend their
GROUND on. K7 does not ask for that: it asks *where `dim` classifies*. So this increment builds the
seat table, finds **two classifying seats drawn in `dim`**, and moves the seats.

**And the sweep found a second kit the round did not name.** corgi's mode strip drew `FORM` `CFG`
`LOG` in `dim` at 1.71:1 with their key numbers legible beside them — ledger's defect inverted, in
the kit whose S1 the round called clean. A case-sensitive first draft of the reader missed it,
which is recorded in the reader's own comment.

Suite **1289 → 1313**. Census unchanged (**29** / **24**) — no glyph moved.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **K6:** contrast is measured against the background actually under the run (the second grounds:
> selection bands, plates, match rects), not only the canvas. `ink` and `mut` ≥ 4.5:1 against every
> ground they are painted on; `focus` ≥ 3:1.

> **K7:** `dim` ≥ 3:1 wherever it classifies (a severity rung on a log row, a dash count, a state
> mark); a purely decorative leader or seam is exempt by seat, named. `alert` ≥ 4.5:1 against every
> ground it is painted on, all eleven.

> **Match tier:** `accent` (or the match ink) against `mut` and against `ink` ≥ 3:1, all eleven, so
> raising `mut` cannot silently erase the match.

> **L7 measured:** the `info` rung may be air (blueprint, ledger, doctrine) or drawn; if drawn it
> obeys K7 (≥ 3:1). Nine languages draw it under 2:1: fix each.

> **C8, second half:** corgi's confirm gets walls from its display frame (`▓`, inc67's register
> ruling) with the board still gone; thirty blank rows with no opener or closer is not a modal.

> **swiss `╎`:** stands; consistency with the kit's own dead cell beats one fewer vertical.
> Recorded.

> **industrial `/`:** the value's separators and the field paper may not be one glyph: the paper
> becomes a cell that no value can contain (cite industrial's alphabet), the invalid marks at
> slider.knob/stepper.step stay.

And the two rulings correcting the match tier and industrial's `focus`, quoted verbatim in
`inc73.md` §0b — both discharged there.

**K7's `alert` clause was carried out in inc73**, all five kits the brief named plus the fifth it did
not: nord 3.05 → 4.50, corgi 3.99 → 4.50, naught 4.05 → 4.51, swiss 4.07 → 4.52, **industrial 4.06 →
4.52 on its plate**. This increment is K7's `dim` clause and L7.

---

## 1. Why the seat moves and not the token

```
dim against its own ground, all eleven (DIM_AGAINST_GROUND, inc70):
  solari 1.20 · blueprint 1.24 · naught 1.35 · darkside 1.39 · ledger 1.50 ·
  nord 1.69 · corgi 1.71 · instrument 1.74 · swiss 1.75 · industrial 1.96 · prism 3.25
```

**Ten of eleven are under the 3:1 floor and the ruling's first branch is unavailable in ten kits at
once.** inc70 declined it in writing: *"raising `dim` to 3.0 in ten kits is a design change an order
of magnitude larger than this increment's, in the token every language spends its GROUND on."* K7
offers the other branch — *"a purely decorative leader or seam is exempt by seat, named"* — and this
increment takes it, which means the corpus needs a table of seats.

**The table is SEATS, not code lines.** There are 160 `c["dim"]` sites in `language.py`; enumerating
them would be a list of expressions, not of readings. A seat is something a reader points at, so
every row of `DIM_CLASSIFIES` is rendered through the kit's own contract method and read back.

| seat | verdict | reason |
|---|---|---|
| `log.rung` | **classifies** | the mark that says WHICH KIND of event a row is |
| `tabs.inactive` | **classifies** | the words that say which modes exist and which one you are not in |
| `part.disabled` | **carried** | `test_two_states_of_one_part_are_told_apart_on_a_channel` — every kit separates DISABLED from live by GLYPH, over every declared table, and the exception roster is `STATES_TOLD_APART_BY_SIZE` |
| `log.time` | decorates | a timestamp is content the row carries, not a class it belongs to |
| `field.leader` | decorates | it joins two things that are both legible and says nothing about either |
| `tabs.separator` | decorates | the rule between two mode names |
| `pane.seam` | decorates | solari names it `seam` and it is one step off the flap face by construction |
| `pager.unlit` | decorates | the LIT dots carry the position and are not `dim`; an unlit dot is the track |

**`carried` is the only branch that lets a classifying seat keep `dim`, and it may not be claimed
without a green law.** A vacuity arm asserts the cited law exists and runs it over all eleven — a
citation nobody runs is not a citation, which is the lesson inc65 wrote when
`MODAL_KEEPS_NOTHING`'s citation was checked and its SCOPE was not.

---

## 2. Cause and mechanism — the log's severity rung

**Cause.** `log_row` set `tone = {"info": c["dim"], "warn": c["mut"]}.get(level, c["ink"])`. Round
four's §0b measured the bottom rung in the artefact, and it is the mark that says which kind of event
a row is:

```
instrument ⠂⠂ 1.74 · swiss · 1.75 · industrial ▫▫ 1.96 · nord ·  1.69 ·
darkside ·  1.39 · naught ◦◦ 1.35 · corgi ▁▁ 1.71 · solari OK  1.20
```

Its criterion — *"point at the log rows that carry a severity"* — answered **two of eight**.

**Mechanism.** One line:

```python
tone = c["mut"] if level in ("info", "warn") else c["ink"]
```

**The tier ladder has two rungs and the shape ladder has three, and that is stated rather than
hidden.** This corpus owns exactly two legible neutral tiers (`mut` and `ink`); a three-rung ladder
cannot have three of them. The tier splits where the row's BODY already splits — calm against
noteworthy — and info against warn is carried by the glyph ladder, which the method's own docstring
already calls the channel: *"the level READS WITH THE COLOUR REMOVED."*

**After, per kit** (the rung's tier against the kit's ground):

```
kit          rung   was (dim)   now (mut)
naught       ◦◦          1.35        6.08
corgi        ▁▁          1.71        6.91
instrument   ⠂⠂          1.74        4.50
swiss        ·           1.75        6.85
industrial   ▫▫          1.96        5.81
nord         ·           1.69        4.51
darkside     ·           1.39        4.56
prism        ⣀⣀          3.25        6.43
solari       OK          1.20        3.65   (the named band exemption)
blueprint    (air)       1.24           —   doctrine
ledger       (air)       1.50           —   doctrine
```

## 3. Cause and mechanism — the inactive mode labels, in TWO kits

**Cause, ledger.** `Ledger.tabs` drew the whole inactive entry — leader AND word — in `dim`, and
ledger's `dim` is `#c4b99f`, the dot leader, at **1.50:1** on the page. Round four's criterion for
`ledger_S1` was *"name the four modes"*, and it answered **one**.

**Cause, corgi, and the round did not name it.** `Corgi._strip` drew the unlit legend in `dim`
(`#3a3a3a`, **1.71:1**) while the key numbers beside it stood in `alu` and could be read:

```
[#6fe36f]\[1][/][#6fe36f]B O A R D[/] [#9a9a9a]\[2][/][#3a3a3a]FORM[/] ...
```

**A sweep of all eleven found exactly these two.** The other nine already give an inactive label
`mut` — the base `tabs` does it, and every override but these two kept it.

**Mechanism.** The seat splits into its two parts in both kits:

```
ledger  [{dim}]{LEAD} {o}[/]        ->  [{dim}]{LEAD}[/][{mut}] {o}[/]
corgi   [{screen if on else dim}]   ->  [{screen if on else mut}]
```

The leader stays where every other leader on ledger's page is; the WORD takes `mut`. corgi's lit
mode keeps the screen's own green, so what says *which* mode is on is unchanged.

**And the first draft of the reader missed corgi entirely.** `dim_seat_tones` searched for the label
case-sensitively and corgi UPPERCASES its legend, so the law passed on a kit that had the very
defect. The reader is case-insensitive now and its comment says why — a law that finds nothing
because it looked in the wrong case is worse than no law.

## 4. L7, measured — and the count is eight, not nine

The brief said *"nine languages draw it under 2:1"*. Measured through this increment's own teeth,
which restore the old tone for all eleven at once and collect who goes red:

```
red on the restored dim rung (8):
  instrument · swiss · industrial · nord · darkside · naught · corgi · solari
green, and each for its own reason (3):
  blueprint   the rung is AIR by doctrine (L7, spec.md §16.1)
  ledger      the same doctrine, and inc60's cited precedent
  prism       dim is 3.25:1 -- the only kit of the eleven over the floor
```

**Eight, with solari among them and prism not.** solari's rung is three WORDS (`OK ` / `DLY` /
`CNX`) drawn at 1.20:1 — the lowest reading in the corpus — and the round's §0b listed it under
"words" rather than measuring it. prism's 3.25:1 was already over the floor and the round said so.
The number is in the teeth's own comment, not only here.

**Neither air kit was touched.** `INFO_RUNG_IS_AIR` holds their citations and
`test_the_info_rung_is_air_by_doctrine_or_legible_by_tier` asserts a drawn rung is never air's
citation and an air rung always has one — so a kit cannot quietly stop drawing its rung and inherit
the doctrine.

## 5. Every token moved

**None.** This increment moves **two seats and zero tokens**, which is the whole of its argument:
K7's floor is unreachable in ten kits and the ruling's second branch is what the corpus can actually
pay.

## 6. The laws

**`test_a_dim_run_that_classifies_is_legible_or_has_moved`** — over all eleven, seat by seat. The
verdict comes from `DIM_CLASSIFIES` and the tier from the kit, so neither half can be adjusted to fit
the other. A `classifies` seat either clears 3:1 in `dim` or is not drawn in `dim`. The ladder clause
(`ink > mut > dim` against the ground) rides along, because it is the half a floor cannot carry.

**Non-vacuous by construction:** `dim_seat_tones` returns only the seats it could actually render,
and the law requires `tabs.inactive` to be among them for every kit and `log.rung` for every kit that
draws one. A kit that stopped drawing a mode strip would go red rather than pass by absence.

**`test_the_dim_table_covers_what_it_claims_to`** — the table's own arms: every verdict is one of the
three the ruling allows; both branches that let a seat KEEP `dim` are used (so the law is not passing
because everything was called decorative); and `carried` names a law that exists and is run here.

**`test_the_info_rung_is_air_by_doctrine_or_legible_by_tier`** — L7 read from the other end: the seat
that classifies a CALM row either says nothing at all with a citation, or is painted in a tier a
reader has. solari is counted with the drawn, deliberately: its rungs are words, and text is exactly
what `mut` is for.

## 7. Teeth

**`test_the_dim_law_bites_on_the_two_seats_inc74_moved`** has two arms of different shapes, because
the two defects were of different shapes.

The `log_row` arm restores the `dim` rung for **all eleven at once** — the seat is the base's and the
defect was the corpus's — and asserts the exact red list of eight (§4). It is the arm that produced
the count.

The `tabs` arm is **ledger's alone**, which is what the measurement said: ten kits already give an
inactive label `mut`, and corgi is fixed at its own seat rather than at the base's. It asserts
ledger's `dim` at exactly 1.50:1 before the law goes red, and that the other ten stay green.

## 8. Frames changed — **svg only**

**0 `.txt` moved, of the 66 and of the 22.** 22 `.svg`:

| | files |
|---|---|
| components (20) | all six of `corgi` and `ledger` (the mode strip is on every screen); `S5` of `darkside` `industrial` `instrument` `naught` `nord` `prism` `solari` `swiss` |
| gallery (2) | `board_corgi` `board_ledger` |

`blueprint` moved nothing: its rung is air and its mode strip was already `mut`.

**Gallery 30–51 in the skill:** the batch close runs `export_to_skill.py`; see §12.

## 9. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1313 passed, 2 skipped, 4 warnings in 34.37s

$ python -X utf8 prototypes/verify_language.py
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
TOTAL                       29
TOTAL homoglyph rows            24
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)
```

Suite **1289 → 1313** (+11 dim-seat arms, +11 info-rung arms, +1 table arm, +1 teeth). Census
unchanged: no glyph moved.

## 10. Risks

1. **The log's tier ladder lost a rung.** `info` and `warn` are both `mut` now, so with the colour
   stripped the two are told apart by SHAPE alone. That is what the contract already claims the
   channel is, but it is one channel where there used to be two, and a round that judges the `.txt`
   will not see the loss while a round that judges the `.svg` will.
2. **`DIM_CLASSIFIES` covers eight seats and `language.py` has 160 `dim` sites.** The table is
   honest about being a table of readings rather than of expressions, and the law is non-vacuous —
   but a ninth classifying seat that nobody has rendered is not caught by it. The next seat to
   arrive has to be added by hand.
3. **`part.disabled` keeps `dim` on a `carried` verdict**, and that verdict rests on
   `STATES_TOLD_APART_BY_SIZE`, which is **8 for naught and 1 for darkside**. In those nine rows the
   glyph channel is exactly what the cited law says it is not, so the tier is doing more work there
   than the exemption admits.
4. **corgi's inactive legend is now `mut` (`#9a9a9a`) and its key numbers are `alu` (`#9a9a9a`).**
   One hex, two seats, both chrome — an alias rather than a double role, so inc73's role law is
   green; but the strip now draws the key and its label at one weight where it drew two.

## 11. Found by looking, not fixed

- **solari's `info` rung is 3.65:1 after the move and that is its named band exemption, not a pass.**
  It is the only kit whose severity rung still misses `MUT_FLOOR`, and the reason is the
  impossibility proof in `THE_BAND_IS_A_SECOND_GROUND`, four batches old and still a request for a
  ruling.
- **The round's §0b count was seven and the brief's was nine; the measurement is eight.** Neither
  earlier number was wrong about what it looked at — the round counted drawn GLYPHS under 2:1 and
  did not measure solari's words. The discrepancy is recorded because a count nobody reconciles
  becomes a fact.
- **`log.time` is `dim` in all eleven** and is 1.20–3.25:1 accordingly. Called decorative here, and
  a reader who wants to know WHEN something happened would disagree; the ruling's example list does
  not name it and this increment did not widen it on its own authority.
- **The pager's unlit dots are `dim` and naught's are `◦` at 1.35:1.** Called decorative because the
  LIT dots carry the position. `naught_S1` row 31 reads `view ◦●●●●◦◦◦◦◦◦◦` and the claim is that the
  four lit dots and their offset are the whole message.

## 12. Pending — not this increment

- inc75 (C8's second half and industrial's paper).
- The batch close: `export_to_skill.py`, `spec.md` §19.
- solari's per-row band ink; `depth_ground()`'s role (inc73 §12).

## 13. Suggested next task

inc75: corgi's confirm takes walls `▓` from its display frame with the board still gone, and
industrial's invalid field stops papering a value in the glyph that value contains.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1313 passed, 2 skipped, 1 failed`
      (inc73 closed at `1289 passed`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      **reported, not counted, not touched.** `verify_language.py` ALL PASSED exit 0. `render.py`
      66/330/0. `matrix.py` refusals `[]` ×11. `collision_census.py` both self-checks green, 29 and
      24, **both unchanged**. `capture_languages.py` plain: 22 captures, 22 grids identical across
      two processes, 2 artefacts moved.
- [x] **No secrets in code or output** — two seat tones, one seat table, three laws, one teeth. No
      token moved. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **2 source files**: `taskboard/language.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.

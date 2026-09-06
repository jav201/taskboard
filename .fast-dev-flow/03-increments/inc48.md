# Increment 48 — a caption stops reading as a control, and no control opens with a meaning

**Batch:** `rework-3`, closing increment · closes `spec.md` §9.4's `industrial_S2`, `industrial_S3`,
`darkside_S3`, `darkside_S6`; answers `darkside_S1` with a citation
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 14 regenerated
frame artefacts, the census table, this packet and the skill export.

**The danger-zone caption is not a button the sheet drew — it is each language's own `field_row` plating
the VALUE, and industrial's plate was byte for byte its DEFAULT button while darkside's leader was byte
for byte its button's opening shoulder. Both rows now read as captions, with `nord_S3` as the reference.
`industrial ▐` was `REQUIRED` and the opening half of every plate; obligation takes `!`, the register's
own stencil, and the plate keeps the cell. `darkside`'s `MATCH_STYLE` was `bold {ink}` in a language that
renounced hue by commitment — zero channels on a terminal that renders bold as brighter — and is now a ±1
grey STEP of ground, which is the one channel §8 says it owns. And the opener law is written over all
eleven: SEVEN are clean and four are counted by name.**

---

## 1. The caption-as-button: whose code plates it

**The question the brief asked, answered by reading.** `screens.py` line 422 builds the danger zone's
caption with `k.field_row("danger zone", F.DANGER_LABEL, W - 4)` and its control with
`k.button(F.DANGER_ACTION, 12, DEFAULT, danger=True)`. **The sheet never calls `button` for a caption.**
What plates the caption is each language's own `field_row`, and two of the eleven plate it with the cell
their own button opens with:

| language | `field_row` drew | `button.main[DEFAULT]` | verdict |
| --- | --- | --- | --- |
| industrial | `▐ {value} ▌` | `▐  ▌` | **byte for byte the same plate** |
| darkside | `▬ {value}` | `▬  ▬` | **byte for byte the same opening shoulder** |
| nord | `{value}`, bare | `[  ]` | the reference — the one of the seven that already had it right |

```
industrial_S3   before   DANGER ZONE                  ▐ delete every completed task ▌
                         ▐ ╱╱Delete all╱╱ ▌   7 tasks, not recoverable
                after    DANGER ZONE                    delete every completed task
                         ▐ ╱╱Delete all╱╱ ▌   7 tasks, not recoverable

darkside_S3     before   danger zone                  ▬ delete every completed task
                         ▬ ØDelete allØ ▬   7 tasks, not recoverable
                after    danger zone                  ◦ delete every completed task
                         ▬ ØDelete allØ ▬   7 tasks, not recoverable
```

**industrial's plate goes back to meaning what it means everywhere else** — a STAMP on a code, on a
display, or on a CONTROL. A definition row is none of the three. The caption stays UPPERCASE, which is
the *"everything is NUMBERED AND LABELLED"* half and costs no chrome. What is left is the base's
composition with this language's register laid over it, and that is the honest reading: what industrial
had to say about a definition row was the capitals, not the walls.

**darkside's row keeps a seat and changes which one.** `◦` is spent on nothing here but an unchosen radio
— not a rung, not a shoulder, not a switch indicator, not a disabled mark — and it is the lightest cell
this alphabet has, which is what a seat should be in a language whose second word is AIRY.

**It was `▏` first, and the measurement is why it is not.** The docstring had always claimed the mark was
*"RAIL-weight"*, so the rail looked like the answer. `darkside_S1`'s objection is that this language
*"se prohibió el trazo vertical en el único sitio donde hacía falta y lo imprime catorce veces donde no"*,
and routing the detail pane's six field rows through the rail took that frame **from 16 vertical strokes
to 22**. A fix that makes the frame it was measured against worse is not a fix. With `◦`:

```
darkside_S1     ▏  16 -> 16       ▬  6 -> 0       ◦  0 -> 6
```

**And the row may not simply go bare**, which is written at the seat rather than discovered twice:
dropping the mark makes `Darkside.field_row` byte for byte `Kit`'s, and
`test_no_two_languages_answer_a_mechanism_the_same_way[field_row]` went red on `[["nord", "darkside"]]`.
*"The caption is lowercased"* is not a difference when the caller's caption is already lowercase. **A
language that answers a mechanism by deleting its answer has not answered it.**

---

## 2. `industrial ▐` — obligation moves, the plate keeps the cell

```
before   title▐        ▐Fix login| redirect---------------▌
after    title!        ▐Fix login| redirect---------------▌
```

The round's criterion on `industrial_S2` is *"en la fila 4, decir cuál de los dos `▐` es la obligación —
la respuesta depende de saber que el otro pertenece al control"*. Eight spaces apart, one row, one cell,
two jobs.

**The plate keeps the cell**, because the plate is this language's whole notation — §3, *"BOXED GROUPS …
EVERYTHING IS NUMBERED AND LABELLED"* — and a control that stopped wearing it would stop being this
language. **Obligation takes the register's own attention code.** This vocabulary is ASCII stencil
(`| I X # x _ - . = @ O o`), and §3's own failure clause — *"FAILS WHEN COLOUR MUST CARRY SEVERITY,
because the palette already spent colour on identity"* — is what pushed severity onto the square's SIZE
(`▫▫ ▪▪ ■■`). That leaves `!` unspent here, and it is what a panel stencils beside a control that must be
set before the machine will run. It is not a severity rung in this language and it is not a number (L-33:
the digits are the MODES).

---

## 3. `darkside_S6` — the match becomes a grey step

`MATCH_STYLE` was `bold {ink}`, and the round's verdict on that frame is the only `rework` in the sixteen
that is about the DESTINATION rather than the artefact: *"en un lenguaje que ha renunciado al matiz,
`bold {ink}` es peso y nada más. Un terminal que renderiza `bold` como «más brillante» — el comportamiento
por defecto de buena parte de ellos — le deja a este lenguaje **cero canales**."*

§8 names the channel this language actually owns: *"DEPTH BY ±1 GREY STEP of background, NEVER borders"*.
A matched run is a region of the row, so it takes the same step — `reverse {mut}`, the ground up one rung
of the ramp with the text sitting on it. Not a hue (the ramp is achromatic), not the reserved accent, not
weight; so it survives the one terminal configuration `bold` does not.

```
darkside_S6.svg   before   1 <rect> (the canvas), 0 font-weight   -- inc43 painted the tier and there was none to paint
                  after    7 <rect> (canvas + six runs at #737373), 0 font-weight
```

Two rosters moved with it and both are asserted, not adjusted quietly:

- **`GROUNDED_FRAMES` is 14 → 15**, `darkside_S6` joining. The docstring already carried the sentence
  that makes an arrival as interesting as a departure; it now carries the arrival too.
- **the reverse kits are 2 → 3**, and `test_the_style_law_is_not_vacuous_and_the_two_reverse_kits_are_the_proof`
  is renamed and re-parametrised. inc43 called `reverse` the SHARP case, because a `bold` language's law
  is one attribute on one element and a `reverse` language's is a ground the exporter used to drop
  entirely. **darkside is now in the half of the corpus where the law is hard**, which is the right side
  of that line for the language with the least colour.

---

## 4. `darkside_S1` — what is doctrine, and what is the operator's

The round's verdict was `rework`, and its own last sentence says who owns it: *"O el rail cede, o el `.txt`
deja de ser la obra para este lenguaje, y eso es un veredicto del operador."* This increment does not
pre-empt that. What it can do is separate the three claims:

- **The grey step is DOCTRINE, cited, and it is not missing — it is unphotographable.**
  `Darkside.pane_split_instead` writes it down at the seat: *"a background is not a cell, so a cell grid
  shows `w` spaces. It DOES survive greyscale, which is the law that applies — a grey step is a step with
  every hue removed."* The `.svg` carries 28 rects of it. This is the third mark in this contract with
  that limit, after the knockout (`Kit.knockout_cell`) and the match, and all three are recorded.
- **The rail is DOCTRINE under inc38's own principle**, and this increment declined to add to it. `▏` is
  one mark on one side, which encloses nothing at any width — the argument inc38 used to take swiss's
  walls off its button and inc46 used to take them off three more controls. Whether a depth device drawn
  as a STROKE can stand in a language whose §8 says *"depth by ±1 grey step, NEVER borders"* is the
  operator's question; **this increment made sure it did not get worse** (§1), and the count is in this
  packet so the ruling has a number.
- **`▬` with six meanings is a DEFECT and it is fixed here.** The round listed them: *"leader de
  `field_row`, pared de botón, pared de select, segmento de switch encendido, relleno de slider, prefijo
  de caption"*. The first and the last were the same seat, and it was the seat that collided with the
  button. `darkside_S1` now carries none.

---

## 5. The opener law

**`test_no_control_opens_with_a_mark_that_means_something[lang]`**, eleven parametrisations. No control's
opening cell, in any state, may be a `LEVELS` / `DANGER_FORM` / `REQUIRED` mark of its language.

This is the finding the census was built around, in `collision_census.py`'s own words: *"a language has a
small alphabet, spends one glyph on severity or obligation, and then spends the same glyph on a control's
chrome — so a reader who has learned 'this mark means error' meets it **opening a button**."*

**THE OPENER AND NOT EVERY CELL, deliberately.** A mark that means something may stand in a control — a
closer, a paper, a knob, a mark inside a box — because a reader meets those AFTER the control has
announced itself. The first cell is the announcement, which is why the round's phrasing is *"el peldaño de
error ABRE el botón seguro"* and not *"aparece en"*.

**Two exclusions, both by ruling rather than by convenience:**

- **the stepper is out.** `stepper.main` and `stepper.step` are two-cell strings whose halves are
  DIRECTIONS, not walls — spec §9.5, inc39's own words when it declined to extend its INVALID law there:
  *"a stepper's halves are directions, not walls, so it needs its own law"*. A law about what OPENS an
  enclosure cannot be asked of a pair that encloses nothing. **It costs the law swiss's and nord's
  `stepper.main` (`··`, whose first cell is `LEVELS["info"]`), five seats each, and that is named here
  rather than absorbed.**
- **a field whose INVALID walls are its own `DANGER_FORM`** — inc39's ruling, spec §9.2. There the opening
  cell IS the rejection, said in the language's loudest form, which is the opposite of a reader mistaking
  it for one.

**The roster, measured:**

| language | count | what it is |
| --- | --- | --- |
| naught | 2 | `◦` opens the button and the field, and `LEVELS["info"]` is `◦◦`. **The roster's arguable entry:** naught's info rung is ZERO LIT DOTS — the unlit lattice, which LANGUAGES.md §0 calls this language's visible GROUND — so *"nothing is lit"* and *"an empty seat"* may be one meaning rather than two. The argument is written in the test and **NOT granted**: an exemption is the operator's, and silence is not one. |
| corgi | 31 | the segment bank is `LEVELS` and the chrome ladder at once (`▁▁ ▄▄ ██` against `▁▁ ▔▔ ▂▂ ··`). The widest single roster entry in the corpus. |
| prism | 19 | `⣿` is `LEVELS["error"]`, the `DANGER_FORM` **and** the opening cell of the button, the checkbox and the field. |
| blueprint | 6 | `├` is `REQUIRED` and the dimension's opening terminator — §9.4's `blueprint_S2`, still open. |
| **instrument · swiss · industrial · nord · darkside · ledger · solari** | **0** | four of the seven were not zero before this batch |

Its teeth are two arms that must name the control AND the mark: restoring `Industrial.REQUIRED = "▐"`
must fire on `button.main` and `textfield.main` with `▐`; restoring swiss's pre-inc46 ladder `· • ●` must
fire on `button.main` with `·` and `•`. Each arm also asserts **the other ten stay where they were**,
which is what proves the eleven are eleven declarations rather than one shared object.

---

## 6. Census delta

```
language      HEAD  inc45  inc46  inc47  inc48      live A x A
naught           3      5      5      5      5      0
corgi            5      5      5      5      5      2
instrument       8      8      7      7      7      1
swiss            8      9      5      5      5      0
industrial       5      4      4      4      4      1
nord             5      4      4      4      4      0
darkside         3      3      3      3      3      0
prism            5      5      5      5      5      1
ledger           4      2      2      2      2      0
solari           3      3      3      3      3      0
blueprint        5      5      5      5      5      3
TOTAL           54     53     48     48     48          15 -> 8
```

**48 → 48 again, and for the same reason as inc47.** `industrial ▐` lost `REQUIRED` and kept
`INVALID + button + textfield`, so it is a smaller row and still a row; `darkside ▬` was never a census row
at all, because it carried no A-family — **the caption-as-button finding is one the census cannot see, and
§10.4 said so in advance** (*"a composition finding; the caption is not a `PART_GLYPHS` slot"*). The
numbers this increment moved are the roster in §5 and the six counts in §1 and §3.

---

## 7. Artefacts changed

**7 `.txt` and 8 `.svg`:** `darkside_S1` `darkside_S3` `darkside_S4` `industrial_S1` `industrial_S2`
`industrial_S3` `industrial_S4` (both tiers), plus **`darkside_S6.svg`** — the `.txt` cannot carry a
ground, so that frame moves in one tier only, which is the whole point of §3.

**Gallery: 0 of the 22 moved.** No board rendering changed.

**The skill export, run twice.** First run: `6 written, 60 already identical` — `board_nord.{txt,svg}`
(inc47), `gallery_instrument.{txt,svg}` and `gallery_swiss.{txt,svg}` (inc46). Second run after this
increment's frames: `0 written, 66 already identical`, which is the idempotence check.

**Five of the eight installed gallery frames (44–51) are now stale and must be re-installed:**

| # | gallery frame | source | state |
| --- | --- | --- | --- |
| 44 | `44_instrument-list-graticule` | `instrument_S1` | identical |
| **45** | `45_industrial-list-plate` | `industrial_S1` | **CHANGED** (inc45 cursor, inc48 field_row) |
| **46** | `46_swiss-list-next-column` | `swiss_S1` | **CHANGED** (inc45 cursor) |
| 47 | `47_solari-list-gate-seam` | `solari_S1` | identical |
| **48** | `48_industrial-modal-plate-lid` | `industrial_S4` | **CHANGED** (inc45 cursor) |
| **49** | `49_darkside-modal-rounded-lid` | `darkside_S4` | **CHANGED** (inc45 cursor) |
| **50** | `50_solari-form-printed-severity` | `solari_S2` | **CHANGED** (inc47 obligation) |
| 51 | `51_instrument-monitor-dot-ladder` | `instrument_S5` | identical |

`export_to_skill.py` does **not** touch `assets/gallery/` — it writes `assets/languages.py`,
`assets/languages/` and `SURFACES.md` — so these five are a manual install and are listed here and in
`spec.md` §11 rather than done silently. **The skill repo was not committed** (its `assets/languages/`
and `languages.py` are written; committing it is not this batch's to do).

---

## 8. Gates, verbatim — AND ONE RED THAT IS NOT MINE

```
$ python -X utf8 -m pytest -q
1 failed, 1040 passed, 2 skipped, 4 warnings in 34.62s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**1028 → 1040**: eleven parametrisations of the opener law plus its teeth test. The red is the
environment-coupled clipboard test (spec §10.6), red at HEAD before this batch began.

```
$ python -X utf8 prototypes/verify_language.py                                        exit 0
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
  -> 0 of the 22 moved

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  1 of the 5 collisions the round found by hand still comes back out of
              the census; 4 are asserted CLOSED and cannot grow back
  TOTAL  48 -> 48

$ python prototypes/export_to_skill.py "C:/Users/jjgh8/.claude/skills/tui-design"     exit 0
  wrote assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 6 written, 60 already identical      (re-run: 0 written, 66 already identical)
  wrote SURFACES.md (11 postures)
```

**Four tests were rewritten on the way and each red is recorded**: `field_row` distinctness (nord vs
darkside, §1), the ground roster (14 → 15, §3), the reverse-kit count (2 → 3, §3), and the style law's
own name.

---

## 9. Risks

- **`!` as industrial's obligation reads as an alarm**, and `Kit.REQUIRED`'s own docstring says an
  obligation *"is a PROPERTY of the field rather than an alert"*. The defence is that industrial's alerts
  are SQUARES (`▫▫ ▪▪ ■■`) by the §3 failure clause, so `!` says nothing else in this language — but a
  reader arriving from any of the other ten brings the bang's usual meaning with them. **One line to
  reverse.**
- **industrial's definition rows lost their plate everywhere, not only in the danger zone.**
  `industrial_S1`'s detail pane went from `▐PROJECT   ▐ Web ▌` to `PROJECT      Web`, which is a real
  loss of signature on a frame the round scored `keep with a note` — and that frame is installed in the
  skill's gallery as #45. The trade is stated: the plate meant three things in one view and now means
  two.
- **`reverse {mut}` puts near-black text on mid grey** for darkside's match. It is a ±1 step and it is the
  channel §8 declares, but nobody has looked at it in a real terminal; the `.svg` is the only evidence
  and the `.svg` is not a terminal.
- **The opener law's naught entry may be an exemption rather than a defect** (§5). It is on the roster as
  a NUMBER, so if the operator grants the exemption the roster is edited and the suite says so.
- **Three rosters now assert non-zero counts** (`HANDED_FIELDS`, `MEANING_AT_A_NAMED_SEAT`,
  `MEANING_AT_AN_OPENER`). Each has a teeth test, but a batch that fixes corgi or prism without editing
  them will go red on something that looks like a false positive. That is the design; it is worth knowing
  it is the design.

---

## 10. Pending — not fixed in this batch

- **corgi (31), prism (19), blueprint (6) and naught (2)** open controls with a meaning. **corgi, prism
  and blueprint also fail the named-seat law** (8 each). None of the four had an increment in this batch.
- **Six live meaning×meaning census rows** in corgi (`▄`, `▀`), instrument (`⠇`), industrial (`▐`), prism
  (`⡀`) and blueprint (`├`, `·`, `━`) — all of them `INVALID` against something, which is inc39's ruling
  and E2's territory.
- **`Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`** — inc39's unfixed defect (spec §9.5), and now
  also the reason the opener law excludes the stepper. **The stepper's own law is still unwritten.**
- **`darkside_S1`: rail or `.txt`** — the operator's ruling (§4).
- **`swiss_S2`'s disabled button reads as a caption**; **`swiss_S4`'s modal opens and never closes**;
  **`instrument ⠛` is the `DANGER_FORM` and the FOCUSED checkbox**; **`instrument ⠇` closes every button
  and field** (inc46 §1a).
- **The five stale gallery frames** (§7) are a manual install.
- **`blueprint_S4`'s destructive control has no danger mark and no focus mark** (inc41 §8).
- **`gallery_darkside` is calendar-dependent** (spec §10.3).
- **`test_win_clipboard_roundtrip` is environment-coupled** (spec §10.6).

## 11. Suggested next task

**corgi, prism and blueprint** — the three languages this batch never opened, and between them the whole
of what is left: 56 opener seats, 24 named seats, and six of the eight live meaning×meaning census rows.
corgi is the sharpest of the three and has never had a frame judged: its four-step block ramp is
`LEVELS`, the chrome ladder, the danger form and the obligation mark at once, which is the same defect
naught has and one rung wider.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1040 passed, 2 skipped, 1 failed`; the
      failure is `test_win_clipboard_roundtrip`, red at HEAD before this batch (§8).
      `verify_language.py` **ALL PASSED** exit 0. `render.py` 66 frames / 330 pairs / 0 hand-drawn.
      `matrix.py` 66 of 66. `capture_languages.py` 22 captures, 0 moved.
      `collision_census.py` self-check green. `export_to_skill.py` exit 0, idempotent on re-run.
- [x] **No secrets in code or output** — glyph tables, two `field_row` methods and rendered frames. No
      network, no new dependency. The only path outside the worktree is the skill directory the export
      is invoked with, and the skill was **not** committed.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force. The commit names its files explicitly.
- [x] **File count within cap** — 2 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`); everything else in the commit is regenerated by a gate script.
- [x] **Review packet attached** — this document.

# Increment 44 — a measurement that names its subject, and the census the sixteen findings were waiting for

**Batch:** `rework-2` · closes `spec.md` §10.4 / §10.5
**Files:** `prototypes/verify_ink.py`, `prototypes/collision_census.py` (new), `.gitignore`,
`tests/test_scratch_cannot_be_committed.py` — **4 source files**, plus the generated
`prototypes/out/collision_census.txt`, this packet and `spec.md` §10.

**`verify_ink.py` printed a bare table of percentages and those percentages were quoted as if they
described the 66 frames. They describe the LIVE widget at eleven languages by three size classes, and they
drift. Every line now carries its subject — `glance ink, 11x3, live` — and a `--frames` mode measures the
66 `.txt` deterministically with one shared formula, which now discards the braille blank and takes
`instrument_S1` from 36.0% to 34.3%: it was over DENSITY.md's floor on padding. `collision_census.py`
reproduces the five overloaded cells the round found by hand and finds 49 more — 54 across the eleven, and
NOT ONE LANGUAGE IS CLEAN. Three of the languages carrying the widest cells have no frame among the
sixteen at all.**

---

## 1. `verify_ink.py`: the number now says what it is a number about

The script drives `TaskboardWidget` on the late fixture at three widths and prints an 11×3 table. Nothing
in that output said so, and §9-era prose quoted it at `prototypes/components/*.txt`. Different surface,
different content, different geometry.

| | headline | subject | deterministic? |
| --- | --- | --- | --- |
| default | `glance ink, 11x3, live` | the running widget, late fixture, `height=26`, widths 40/60/110 | **no** |
| `--frames` | `frame ink, 66 frames, static` | `prototypes/components/*_S?.txt` | **yes** — it reads files |

```
$ python -X utf8 prototypes/verify_ink.py --frames                               exit 0
frame ink, 66 frames, static (11 languages x 6 screens, read from components/*.txt)

language           S1       S2       S3       S4       S5       S6
------------------------------------------------------------------
blueprint       22.4%    13.1%    11.3%    19.4%    12.3%    10.4%
corgi           27.0%    14.4%    15.7%     2.7%    17.8%    15.4%
darkside        13.1%     8.7%     8.9%    14.4%    11.3%     8.3%
industrial      24.0%    13.9%    15.4%    23.0%    17.8%    15.1%
instrument      34.3%    13.2%    13.6%    32.3%    14.6%    12.9%
ledger          47.5%    18.1%    19.2%    48.8%    19.5%    16.6%
naught          29.2%    15.1%    13.6%    35.0%    14.5%    12.5%
nord            19.3%     8.5%    11.7%    19.9%    14.2%    12.7%
prism           14.8%     8.7%     8.9%    16.2%    11.4%     9.8%
solari          33.5%    13.7%    13.8%    22.8%    14.5%    11.2%
swiss           16.4%    11.4%    14.6%    18.6%    17.1%    14.0%

floor    corgi_S4                        2.7%
ceiling  ledger_S4                      48.8%
```

**Neither mode is a gate**, and the module docstring says why: DENSITY.md's 35% is a design target for a
glance surface, and a script that failed a build on it would be asserting the target had been agreed as a
threshold. It has not.

**The drift is now measured rather than described.** Two runs back to back, nothing changed:

```
industrial board   50.8%  ->  51.5%      (0.7 points)
nord       board   29.2%  ->  29.3%
the other 31 cells                        identical
```

So the drift is real, small, and on this pair it stayed out of the `glance` column the floor is read off.
Cause still not established — the docstring's "animation phase is the suspicion, not a finding" stands.

**ONE FORMULA, AND IT CHANGED.** Both modes now use `ink_fraction` with
`BLANKS = " " + U+2800 BRAILLE PATTERN BLANK`. A braille blank is an EMPTY braille cell — a space that
happens to live in the braille block — and instrument draws in braille while prism borrows the cell, so
it appears 422 times across the 66 frames. It was being counted as ink. Seven frames move:

```
instrument_S1   36.0% -> 34.3%   (-1.8)      <- CROSSES DENSITY.md's 35% FLOOR
instrument_S4   34.1% -> 32.3%   (-1.8)
instrument_S6   14.9% -> 12.9%   (-1.9)
prism_S1        16.7% -> 14.8%   (-1.9)
prism_S2        10.6% ->  8.7%   (-1.9)
prism_S4        18.2% -> 16.2%   (-1.9)
prism_S6        11.8% ->  9.8%   (-1.9)
```

**`instrument_S1` was above the glance floor on padding.** Measured, not fixed, and carried into
`spec.md` §10.6.

The arithmetic self-check gained the two cases that make the change falsifiable — a strip of braille
blanks must read `0.00`, and a drawn braille cell must read as ink — because the first version of this
probe returned 0.0% for everything and that was the probe.

## 2. `collision_census.py`: the two sets, and the line that decides what a collision is

**A — severity and obligation:** `LEVELS[*]`, `DANGER_FORM`, `REQUIRED`, the DECLARED `invalid` mark of
every glyph table, and `CUR`.
**B — control chrome:** every `PART_GLYPHS` slot the registry reaches for `button`, `checkbox`, `radio`,
`switch`, `textfield` and `stepper`, resolved through `Kit.part_glyph` in every state
`component_states` derives.

> **A cell collides when it carries roles from two or more A-families, or from at least one A-family and
> at least one B-family. B × B is counted and not listed.**

- **A × B** is the request verbatim: instrument's `⠇` is the ERROR rung and the opener of a SAFE button.
- **A × A** had to be included or three of the five would have been missed: swiss's `━` is the cursor AND
  `LEVELS["error"]`; nord's `!` is `warn` AND `DANGER_FORM`. Two meanings is two meanings.
- **B × B is not a collision.** A language has an ALPHABET, and a button and a text field sharing a wall
  form is how a language reads as one language. The count is printed at the foot of every language so the
  decision stays visible and can be reversed by whoever disagrees.

**Position is part of the role**, because the round's own phrasing is positional: the finding is not
"instrument spends `⠇` on a button", it is that `⠇` is the button's **opener** — the first thing the eye
reaches.

**A FALLBACK IS NOT A DECLARATION, and that line is the difference between a census and a pile.** The
first run reported 68 collisions. `Kit.part_glyph` walks the state chain, so a part with no `invalid` key
returns its DEFAULT glyph — and crediting that to the INVALID family made **every language's caret collide
with itself** and every stepper track carry a rejection mark. Fourteen spurious rows, all one artefact.
Skipping undeclared `invalid` states takes the census to **54**, and the five hand-found rows all survive.

**What the census cannot see, stated in its own docstring:** `select` and `textarea` declare no
`PART_GLYPHS` family (they compose from the textfield's slots plus their own literals, inc16/inc30), so
their chrome reaches this census through `textfield` and any mark of their own is outside it. `slider`,
`bar` and `scrollbar` are outside set B by the request's own list; each language prints how many further
cells would collide if they were in.

**The five the round found by hand are asserted before any table is printed** — the same bargain
`verify_ink.py` makes with its arithmetic:

```
$ python -X utf8 prototypes/collision_census.py
self-check  the 5 collisions the round found by hand all come back out of the census
```

## 3. The census

```
language       colliding cells
naught                       3      corgi                        5
instrument                   8      swiss                        8
industrial                   5      nord                         5
darkside                     3      prism                        5
ledger                       4      solari                       3
blueprint                    5
------------------------------
TOTAL                       54

zero collisions: NONE -- all eleven overload at least one cell
```

Every row, with its families (the full seat lists are in `prototypes/out/collision_census.txt`):

| lang | cell | fam | the roles |
| --- | --- | --- | --- |
| naught | `∙` | 6 | LEVELS[error] + LEVELS[warn] · DANGER_FORM · REQUIRED · CUR · switch.indicator |
| naught | `◦` | 6 | LEVELS[info] + LEVELS[warn] · button.main open+close · checkbox.main · radio.main · stepper |
| naught | `·` | 5 | INVALID textfield.main mid · checkbox.main (disabled) · stepper.main · switch · textfield |
| corgi | `·` | 7 | INVALID textfield.main mid · button (disabled) · checkbox · radio · stepper · switch · textfield |
| corgi | `▁` | 7 | LEVELS[info] · button.main open+mid+close · checkbox · radio · stepper · switch · textfield |
| corgi | `▄` | 7 | LEVELS[warn] · DANGER_FORM · INVALID stepper.step mid + textfield walls · button · checkbox · radio · switch |
| corgi | `▀` | 4 | REQUIRED · INVALID stepper.step + textfield.main mid · stepper.step (focused) · switch |
| corgi | `█` | 4 | LEVELS[error] · checkbox.knob · stepper.step (active) · switch |
| **instrument** | **`⠇`** | **4** | **LEVELS[error] · INVALID textfield.main open · button.main open · textfield.main open** |
| **instrument** | **`⠁`** | **5** | **REQUIRED · checkbox.main (disabled) · stepper.main · switch.main (disabled) · textfield (disabled)** |
| instrument | `⠶` | 3 | INVALID textfield.main mid · radio.knob · switch.indicator (disabled) |
| instrument | `⠸` | 3 | INVALID textfield.main close · button.main close · textfield.main close |
| instrument | `⣿` | 3 | CUR · checkbox.knob · switch.indicator |
| instrument | `⠛` | 2 | DANGER_FORM · checkbox.main (focused) |
| instrument | `⡄` `⢠` | 2 | INVALID stepper.step · stepper.step (default), each on the opposite side |
| swiss | `·` | 6 | LEVELS[info] · button.main open · checkbox.knob · radio.knob · stepper.main · textfield.main |
| **swiss** | **`•`** | **3** | **REQUIRED · button.main open (focused) · radio.knob** |
| **swiss** | **`━`** | **3** | **LEVELS[error] · CUR · switch.indicator** |
| swiss | `─` | 2 | LEVELS[warn] · switch.main |
| swiss | `╱` `╲` | 2 | DANGER_FORM · INVALID textfield.main wall |
| swiss | `‹` `›` | 2 | INVALID stepper.step · stepper.step (default), sides exchanged |
| industrial | `▐` | 4 | REQUIRED · INVALID textfield.main open · button.main open · textfield.main open |
| industrial | `▌` | 3 | INVALID textfield.main close · button.main close · textfield.main close |
| industrial | `<` `>` | 3 | INVALID stepper.step · radio.knob · radio.main, sides exchanged |
| industrial | `▪` | 2 | LEVELS[warn] · CUR |
| **nord** | **`!`** | **3** | **LEVELS[error] + LEVELS[warn] · DANGER_FORM · INVALID textfield.main walls** |
| nord | `[` `]` | 4 | INVALID stepper.step · button.main wall · checkbox.knob · checkbox.main · textfield |
| nord | `·` | 2 | LEVELS[info] · stepper.main |
| nord | `▸` | 2 | CUR · stepper.step close (focused) |
| darkside | `O` | 4 | LEVELS[error] · CUR · checkbox.knob · switch.knob |
| darkside | `Ø` | 2 | DANGER_FORM · INVALID stepper.step + INVALID textfield.main walls |
| darkside | `·` | 2 | LEVELS[info] · textfield.main mid (edited) |
| prism | `⣀` | 7 | LEVELS[info] · button · checkbox · radio · stepper · switch · textfield |
| prism | `⣿` | 7 | LEVELS[error] · DANGER_FORM · button (all three walls) · checkbox · radio · switch · textfield |
| prism | `⣤` | 5 | LEVELS[warn] · button.main mid (focused) · radio · switch · textfield |
| prism | `⡀` | 3 | REQUIRED · INVALID stepper.step close · stepper.step open |
| prism | `⢀` | 2 | INVALID stepper.step open · stepper.step close |
| ledger | `▶` | 7 | CUR · button.main open · checkbox · radio · stepper · switch · textfield |
| ledger | `·` | 5 | INVALID textfield.main mid · checkbox · radio · switch · textfield |
| ledger | `†` | 2 | LEVELS[warn] · REQUIRED |
| ledger | `‡` | 2 | LEVELS[error] · INVALID stepper.step + INVALID textfield.main walls |
| **solari** | **`▁`** | **7** | **REQUIRED · button · checkbox · radio · stepper · switch · textfield — 18 declared seats** |
| solari | `·` | 4 | INVALID textfield.main mid · checkbox · switch · textfield |
| solari | `▼` | 4 | CUR · checkbox.knob · stepper.step close · switch.knob |
| blueprint | `├` | 7 | REQUIRED · INVALID stepper.step open · button · checkbox · radio · stepper · textfield |
| blueprint | `┤` | 7 | INVALID stepper.step close · button · checkbox · radio · stepper · switch · textfield |
| blueprint | `╌` | 6 | LEVELS[warn] · checkbox · radio · stepper · switch · textfield, all in DISABLED |
| blueprint | `·` | 5 | LEVELS[info] · INVALID textfield.main mid · stepper · switch · textfield |
| blueprint | `━` | 3 | LEVELS[error] · DANGER_FORM · INVALID textfield.main walls |

**The five in bold are the round's own, reproduced.** solari's `▁` is 7 families and 18 declared seats;
the round counted **nine jobs in one SCREEN**, this counts roles in the KIT, and it is the widest single
cell in the corpus either way.

**Which of the eleven have zero collisions: none.** Every language overloads at least one cell, and the
three that overload most widely by family count — naught `∙` and `◦` at six each, corgi's whole four-step
ramp, ledger's `†` that is `warn` and `REQUIRED` at once — **have no frame among the sixteen the round
flagged.** The round judged 42 frames; the census reads 11 kits.

**And the census flags inc39's own fix.** `swiss ╱ ╲`, `nord !`, `blueprint ━`, `corgi ▄`, `darkside Ø`
and `ledger ‡` all put `DANGER_FORM` on the INVALID textfield walls — **which is exactly the rule inc39
applied on purpose** (`spec.md` §9.2). The census cannot tell a deliberate alignment from an accident. It
asks the question; the answer is the operator's, and the docstring says so.

## 4. The census table is committed, which needed two more edits

`prototypes/out/*` is ignored with five named exceptions. `collision_census.txt` is a sixth — a generated
file that is nonetheless reviewed and read by the language rework — so `.gitignore` gains
`!prototypes/out/collision_census.txt`, **and `tests/test_scratch_cannot_be_committed.py`'s
`MUST_STAY_COMMITTABLE` roster gains the same path.** The roster exists precisely so that "ignore the
yard" cannot quietly drop a repository file; adding the exception without the roster entry would have left
that law true and incomplete. It went red until the file was staged, which is the law working.

## 5. Gates, verbatim — AND ONE RED THAT IS NOT MINE

```
$ python -X utf8 -m pytest -q                                                    exit 1
1004 passed, 2 skipped, 4 warnings in 34.74s
FAILED tests/test_app.py::test_win_clipboard_roundtrip
  - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

**This is an environment failure and it is stated as a red, not explained away.** The test drives the real
Windows clipboard through PowerShell. The OS is refusing the operation to anything right now:

```
$ powershell -NoProfile -Command "Set-Clipboard -Value 'probe2'; Get-Clipboard"
Set-Clipboard : Requested Clipboard operation did not succeed.
```

Two independent facts, both checked: the failure reproduces outside Python entirely, and **neither
`taskboard/models.py` (which holds `grab_clipboard_text`) nor `tests/test_app.py` was touched by any of the
three increments in this batch** — the full file list of `1140c96..worktree` is 45 paths and neither is
among them. It passed at inc42 and inc43 in this same session. It is carried into `spec.md` §10.6 as the
one test in the suite whose result depends on the machine's GUI state.

**1004 passed is unchanged from inc43** — this increment adds a script and a mode, and no test.

```
$ python -X utf8 prototypes/verify_language.py                                   exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                 exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                 exit 0
11 rows x 6 screens, every cell `implementa -`
per screen: no primitive missing in any language; refusals, by language: all []
```

**Frames changed: 0 of 66. Gallery files changed: 0.** This increment writes one table and no artefact.

## 6. Risks

- **The census is a census of DECLARATIONS.** A collision exists in the kit whether or not the two roles
  land in the same photograph, and seven of the sixteen findings have no census row because they are
  composition or typography. Reading the census as "the sixteen, solved" would be wrong in both
  directions.
- **B × B is excluded by a judgment.** Two controls sharing a wall is an alphabet; it is also how a real
  overload could hide. The count is printed per language so the boundary is a number.
- **The `invalid` fallback rule is a second judgment** (§2), and it removed 14 rows. If a language ever
  MEANS its invalid state to be identical to its default, this census will say nothing about it —
  which is arguably the wrong silence. Stated in the code comment where the `continue` is.
- **The braille-blank change moves seven published frame numbers** and takes one across DENSITY.md's
  floor. It is a correction, not a regression, and it is the sort of correction that reads as a
  regression if nobody says which it is.
- **`verify_ink.py` still drifts.** The mode split does not fix that; it removes the reason anyone had to
  care, by giving the deterministic question its own answer.

## 7. Pending — not fixed here

- **The sixteen language-level frames** (`spec.md` §10.4). Untouched; annotated.
- **The 49 census rows the round never named** (§10.5), including three languages with no frame at all.
- **`gallery_darkside` is calendar-dependent** (inc42 §3).
- **`instrument_S1` is under the glance floor** (§1).
- **`blueprint_S4`'s destructive control has no danger mark and no focus mark** (inc41 §8).
- **`test_win_clipboard_roundtrip` is environment-coupled** (§5).

## 8. Suggested next task

The language rework itself, and the census says where to start: the cells carrying an A×A collision, since
those are two MEANINGS on one mark with no control involved and no composition argument available —
`naught ∙`, `nord !`, `swiss ━`, `industrial ▪`, `darkside O`, `ledger †`. Six cells, six languages, and
none of them needs a frame re-judged first.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1004 passed, 2 skipped, 1 failed`;
      the failure is `test_win_clipboard_roundtrip`, proved environmental two ways in §5.
      `verify_language.py` **ALL PASSED** exit 0. `render.py` 66 frames, exit 0, 0 moved. `matrix.py`
      66 of 66, exit 0. `collision_census.py` self-check green. `verify_ink.py` both modes exit 0.
- [x] **No secrets in code or output** — the census reads `taskboard/language.py` glyph tables; the ink
      table reads the synthetic `_fixture_late.json` and files already in the repo. No network, no
      dependency, no new path outside the worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete.
- [x] **File count within cap** — 4 source files (`verify_ink.py`, `collision_census.py`, `.gitignore`,
      `tests/test_scratch_cannot_be_committed.py`) plus the generated table, this packet and `spec.md`
      §10: 7 paths, 4 of them hand-written source.
- [x] **Review packet attached** — this document.

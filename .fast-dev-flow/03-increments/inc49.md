# Increment 49 — the named-seat law learns what a knob is

**Batch:** `rework-4`, opening increment · closes `PROTOTYPE-inheritors-2.md` §5 **K1** (and its §0c)
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus 4 regenerated
frame artefacts, 2 gallery artefacts, the census table and this packet.

**inc46 wrote the indicator clause as `comp == "switch" and part == "indicator"`, and in these kits the
indicator is the TRACK. The cell a reader points at and calls "the switch" is the KNOB, and the law never
looked at it — so `darkside` drew the perilla of all five switches on `darkside_S3` with `O`, which is its
own `LEVELS["error"]`, while `MEANING_AT_A_NAMED_SEAT["darkside"]` read **0**. The clause now covers
`switch.knob`, `checkbox.knob` and `radio.knob`. Five languages move: darkside 0 → 4 and is fixed at its
own declaration back to 0; naught 8 → 12, corgi 8 → 16, prism 8 → 16, blueprint 8 → 12, all four already
on the roster before the widening and all four the operator's decision (A).**

---

## 1. The cause: a clause that named the wrong part

`COMPONENT_PARTS["switch"]` is `("main", "indicator", "knob")`, and the registry's own comment says why —
*"a switch is a slider whose range is boolean, so its ANATOMY is a range control's anatomy … indicator
behind the knob when on, track ahead of it when off"*. So in every one of the eleven the **indicator is
the run of track behind the grip** and the **knob is the grip**. inc46's clause asked about the run.

What the gap hid, verbatim from `darkside_S3` at `a8a7a5d`:

```
  notify on overdue         ▬▬O
  daily digest              ▬▬O
  sound                     O──
  sync to remote            x╌╌   (no remote configured)
  compact rows              ▬▬O
```

`Darkside.LEVELS = {"info": "· ", "warn": "o ", "error": "O "}`. The census signed it —
`O [3 families] LEVELS[error] · checkbox.knob mid · switch.knob mark` — and the law did not.
`PROTOTYPE-inheritors-2.md` §0c names the same blind spot in two more languages: `naught ◉`
(`REQUIRED` at the knob) and `corgi ██` / `▀▀` (the error and warn rungs at the knob).

## 2. The mechanism: `KNOB_SEATS`, written as a set so the exclusion is visible

```python
KNOB_SEATS = (("switch", "knob"), ("checkbox", "knob"), ("radio", "knob"))
...
named = (dead
         or (comp == "switch" and part == "indicator")
         or (comp, part) in KNOB_SEATS)
```

Every knob `RULED_CONTROLS` reaches. **The slider's knob is out, and the reason is the census's boundary
and not a claim**: `RULED_CONTROLS` is the six components `collision_census.py` reads, so the two
instruments ask the same question of the same set, and the slider is in neither. Written as a set rather
than as `part == "knob"` so that boundary is legible at the seat.

## 3. The law, stated so it can be argued with

> A mark that carries a MEANING — a `LEVELS` rung, the `DANGER_FORM` or `REQUIRED` — may not stand at a
> seat where a reader would take it for that meaning. The seats are: the OPENER of a control (inc48), the
> INDICATOR of a switch, a DISABLED mark, and **every KNOB the registry declares**.

`CUR` stays out of the meaning set, unchanged and for inc46's stated reason: a cursor says where the
reader is, not what the work is worth.

## 4. The roster, by name, measured

| language | before | after | what the widening found |
| --- | --- | --- | --- |
| **darkside** | 0 | **0** (4 before the fix) | `O` = `LEVELS["error"]` at `switch.knob` and `checkbox.knob`, default and checked. **Fixed in §5.** |
| naught | 8 | **12** | `◉` = `REQUIRED` at `switch.knob` and `checkbox.knob`. spec §11.5 in writing: *"naught and solari have no unspent cell left … that argument is available exactly twice and it has been spent twice"*. Open. |
| corgi | 8 | **16** | `██` (`LEVELS["error"]`) and `▀▀` at `switch.knob`, `██` at `checkbox.knob`, `▁●` at `radio.knob`. Never had an increment. Open. |
| prism | 8 | **16** | `⣿` (`LEVELS["error"]` and `DANGER_FORM`) at `checkbox.knob`; `⣀ ⣤ ⣿` at `radio.knob`. Never had an increment. Open. |
| blueprint | 8 | **12** | `├` = `REQUIRED` at `checkbox.knob` (`├╪┤`) and `radio.knob` (`┤○├`). Never had an increment. Open. |
| instrument · swiss · industrial · nord · ledger · solari | 0 | **0** | the widening reaches them and finds nothing. |

**Four of the five that moved were already failing this law before the clause widened**, and all four are
`PROTOTYPE-inheritors-2.md` §6 decision **A** — the three languages that have never had an increment, plus
naught, which has no unspent cell. They are **counted by name with their reason**, which is the third
state this law has always had (*"it is a measurement, not a pass"*), not fixed and not exempted here.
**Only one language went from clean to failing under the widening, and that is the one the blind spot was
hiding.**

## 5. darkside's fix, at its own declaration, with the citation

```
before   "knob":          {DEFAULT: "O",   FOCUSED: "◎",   EDITED: "◆", ACTIVE: "●", …}
         "checkbox.knob": {DEFAULT: "(O)", FOCUSED: "[◎]", ACTIVE: "{●}", DISABLED: "╌x╌"}
after    "knob":          {DEFAULT: "◎",   FOCUSED: "◉",   EDITED: "◆", ACTIVE: "●", …}
         "checkbox.knob": {DEFAULT: "(◎)", FOCUSED: "[◉]", ACTIVE: "{●}", DISABLED: "╌x╌"}
```

**The ramp starts one rung up, and both new cells were already in this kit's alphabet** — `◎` is the grip
it drew for FOCUSED and `◉` is the mark its radio sets on the chosen item (`«◉»`). Nothing was invented.

**AND IT IS DELIBERATELY NOT `○`.** The obvious edit is to swap the LATIN LETTER O for the geometric
`○` U+25CB, and that is exactly the mistake `PROTOTYPE-inheritors-2.md` §0b/§4 documents five times over:
*"cinco de los seis lenguajes que sí tuvieron incremento resolvieron una colisión mudándose a un
homoglifo"* — `• → ●`, `▬ → ◦`, `▪ → ▶`, `▁ → ▮`, `O → ▊`. `○` against `O` is not even a homoglyph, it is
the same drawing. `◎` and `◉` differ from `· o O` by **COUNT** — two concentric strokes against one —
which is the first channel the batch rule lists (`inc45.md` §0: *count, weight, tier, position*).

**The ramp still climbs and the language's own laws hold.** `◎` (ring + dot) → `◉` (ring + disc) → `●`
(solid disc) is monotone fill, which is *"FILL INVERSION, this language's declared idiom"*; nothing is
boxed; `part_tone` still reaches only the grip with the one accent (§8, *"the accent marks interactivity,
NOTHING ELSE"*). And the knob stays plainly distinct from the track it rides — `▬▬◎` against the fill
`▬` and the empty run `─` — which is what `verify_language`'s *"a knob drawn like the fill is not a
knob"* asks (spec §11.5).

```
darkside_S3   after    notify on overdue         ▬▬◎
                       sound                     ◎──
                       row density               ▬▬▬▬▬▬▬▬▬◎──── 70
darkside_S2   after    tags          ( ) api  (◎) ui  (◎) urgent
```

**One collision closed and one B×B row opened, and it is named:** `◉` is now the FOCUSED grip of the
switch, the checkbox (`[◉]`) and the radio (`«◉»`). That is three controls sharing one chrome mark, which
is the census's B×B boundary — *"two controls sharing a wall form is how a language reads as one
language"* — and it is the same mark for the same state in all three, not two meanings on one cell.

## 6. Teeth

`test_the_named_seat_law_goes_red_on_the_three_declarations_it_moved`, arm three:

```python
tbl = dict(LG.Darkside.PART_GLYPHS["knob"]); tbl[LG.DEFAULT] = "O"
monkeypatch.setitem(LG.Darkside.PART_GLYPHS, "knob", tbl)
hits = meaning_marks_at_named_seats("darkside")
assert hits and all(h[0] == "switch.knob" for h in hits), hits
assert all(h[3] == LG.kit("darkside").LEVELS["error"].strip() for h in hits), hits
assert all(len(meaning_marks_at_named_seats(o)) == MEANING_AT_A_NAMED_SEAT[o]
           for o in LANGS if o != "darkside")
```

**It names the LANGUAGE, the SEAT and the MARK**, and it restores the SHARED `knob` table only — so
`checkbox.knob` stays where inc49 put it and the hits can only be `switch.knob`. That is what proves the
widening is what caught it, rather than the disabled arm catching it sideways. The third assertion holds
the other ten still, which is what proves the eleven are eleven declarations.

**And the law itself was watched fail, by hand, on the real declaration.** Reverting the two
`Darkside.PART_GLYPHS` lines to `O` / `(O)` and leaving the roster at 0:

```
$ python -X utf8 -m pytest "tests/test_components.py::test_a_meaning_never_stands_at_a_disabled_or_indicator_seat[darkside]" -q
E       AssertionError: ('darkside', [('checkbox.knob', 'default', '(O)', 'O'), ('checkbox.knob', 'checked', '(O)', 'O'), ('switch.knob', 'default', 'O', 'O'), ('switch.knob', 'checked', 'O', 'O')])
E       assert 4 == 0
1 failed in 0.60s
```

`language.py` was restored from a byte copy taken before the edit and the eleven parametrisations re-run
green (`11 passed in 0.46s`); `git diff --stat` shows the same 21/2 line change as before the experiment.

## 7. Census delta

```
language      a8a7a5d   inc49
naught             5       5
corgi              5       5
instrument         7       7
swiss              5       5
industrial         4       4
nord               4       4
darkside           3       2
prism              5       5
ledger             2       2
solari             3       3
blueprint          5       5
------------------------------
TOTAL             48      47
```

`darkside O [3 families] LEVELS[error] · checkbox.knob mid · switch.knob mark` is **gone** — the one row
this increment was aimed at, and the first time in `rework-3`/`rework-4` that the total has moved at all
(inc47 and inc48 both closed findings at 48 → 48). `zero collisions: NONE` still holds for all eleven.

## 8. Artefacts changed

**Frames: 2 (`.txt` + `.svg` each).** `darkside_S2` (the three checkbox knobs on the tags row) and
`darkside_S3` (five switch knobs and the slider's grip). No other language's frame moved, which is the
point: the widening is a test-side clause and darkside is the only kit whose declaration changed.

**Gallery: 2 of the 22.** `gallery_darkside.{txt,svg}` — the component strip's `default` and `focused`
knob rows. **Checked against the calendar trap** (spec §10.3): the diff is the two knob rows only, the
moon doodle cell is unchanged, so this is the knob and not `PHASES[date.today().day % 6]`.

## 9. Gates, verbatim

```
$ python -X utf8 -m pytest -q                                                          (before)
1 failed, 1040 passed, 2 skipped, 4 warnings in 34.25s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'

$ python -X utf8 -m pytest -q                                                          (after)
1 failed, 1040 passed, 2 skipped, 4 warnings in 33.60s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'

$ python -X utf8 prototypes/verify_language.py                                        exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                                      exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                                      exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 2 of the 22 moved (gallery_darkside.txt, gallery_darkside.svg)

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  1 of the 5 collisions the round found by hand still come back out of
              the census; 4 are asserted CLOSED and cannot grow back
  TOTAL  48 -> 47
```

**`1040 → 1040`: the test count does not move.** This increment widened an existing parametrised law and
added an arm to an existing teeth test; it wrote no new test function. That is worth saying out loud,
because "no new tests" usually means "no new law" and here it means the opposite — the law that existed
now reaches four seats it could not see.

## 10. Risks

- **`◎` at 12 px.** The new default grip is a ring with a dot in it and the focused one is a ring with a
  disc in it. On the artefact they are two code points; **the `.svg` carries no font metric**, which is
  round-2 finding E2 verbatim, so nobody can say from here whether `◎` and `◉` separate at cell height.
  The count argument (two strokes vs one) is what separates them from `· o O`; what separates them from
  *each other* is fill, and fill is the channel this language declares. **Not resolved, and it cannot be
  from an `.svg`.**
- **The roster now asserts four non-zero counts that got BIGGER.** A batch that opens corgi, prism or
  blueprint will go red on numbers that look like regressions and are the record. That is the design
  (inc48 §9 said the same of three rosters); it is worth knowing it is the design.
- **`Darkside.LEVELS`' own comment is now stale and this increment did not touch it.** It reads *"A
  DIMMING LADDER MADE OF ITS OWN CURSOR. `CUR` is `O`"* — `CUR` has been `▊` since inc45. Left alone
  deliberately (surgical change), reported in §11.
- **The knob moved for the SLIDER too**, because `knob` is the shared table: `darkside_S3`'s row-density
  grip went `▬▬▬▬▬▬▬▬▬O────` → `▬▬▬▬▬▬▬▬▬◎────`. That is one grip vocabulary across the language, which is
  what the shared table is for, but it is a frame change nobody asked for and it is listed in §8.

## 11. Found by looking, not fixed

- **`Darkside.tabs()` still prints `(O)` for the active tab**, and `wordmark()`'s doodle prints `(O)` at
  one of six phases — `darkside_S3` row 1 is `( )board  ( )form  (O)cfg  ( )log`. Both are drawn
  **outside `PART_GLYPHS`**, so neither this law nor the census can reach them, which is the limit
  spec §10.4 already published for `▬` (*"the caption is not a `PART_GLYPHS` slot"*). So the error rung
  is off every knob in this language and still marks the active tab. **Named, not fixed** — it is a
  change to a method rather than to a glyph table, and it is a new finding rather than one on the record.
- **`Darkside.LEVELS`' comment cites a `CUR` that moved three increments ago** (see §10).
- **The blind spot was structural, not a typo.** `COMPONENT_PARTS` gives `switch` the same three parts as
  `slider` on purpose, and the clause that named `indicator` was written from the word rather than from
  the registry. The two other clauses of the same rule (`dead`, and inc48's opener) are derived from the
  registry and were never wrong.

## 12. Pending — not this increment

- **C3 `solari_S4`** and **K3 the stepper's law** — inc50 and inc51 of this batch.
- **Decisions A, C, D, E, F, G and finding C1** are the operator's and are untouched. Listed in the
  batch's close.

## 13. Suggested next task

**inc50 — `solari_S4`'s band shrinks to its content instead of sliding down the page** (C3).

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1040 passed, 2 skipped, 1 failed`; the
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6),
      red at `a8a7a5d` before this increment and reported, not counted. `verify_language.py` ALL PASSED
      exit 0. `render.py` 66/330/0. `matrix.py` 66 of 66. `capture_languages.py` 22 captures, 2 moved.
      `collision_census.py` self-check green, 48 → 47.
- [x] **No secrets in code or output** — two glyph-table lines and one test clause. No network, no new
      dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The commit names its files explicitly.
- [x] **File count within cap** — 2 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`); the other 7 paths in the commit are written by gate scripts.
- [x] **Review packet attached** — this document.

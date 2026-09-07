# Increment 56 — the corpus's one knockout is finally in a picture (ruling G)

**Batch:** `rework-5b`, middle increment · carries out **Ruling G** on
`PROTOTYPE-inheritors-2.md` §6 decision (G), named in `spec.md` §9.3 q3, §9.4, §12.6 and §13.7 and
untouched by four batches
**Files:** `prototypes/components/fixture.py`, `prototypes/components/screens.py`,
`tests/test_components.py` — **3 source files**, plus 2 regenerated frame artefacts and this packet.

**`Kit.mood` is the ONE board-wide fact a kit is ever given, and no screen builder in `screens.py` had
ever set it: all 66 frames were composed by kits carrying the constructor's default `"clear"`. The
fixture has had an overdue task since it was written (`Rate-limit the API`, two days late, still
open). So blueprint's first-fixation law — the single knockout of an eleven-language corpus — was
asserted in a test and appeared in no image, which is round decision G word for word. The fixture now
DERIVES the mood from its own tasks and `screens.s2` hands it over, and `blueprint_S2`'s title block
reads `├ OVERDUE ┤` on a reversed ground in the `.svg`. `GROUNDED_FRAMES` 15 → 16.**

**AND THE RULING'S FRAME PREDICTION WAS WRONG, which is reported rather than worked around: ONE S2
frame changed, not eleven. The reason is measured and is the sharper finding — only TWO of the eleven
kits read `Kit.mood` at all, and the second one reads it through a seat S2 does not compose.**

---

## 0. Ruling (orchestrator, 2026-09-06, on the operator's delegation)

> **inc56 · Ruling G: the S2 fixture carries one alert-mood item for all eleven**
> Blueprint's first-fixation law (`├ OVERDUE ┤` reverse on the `alert` mood) is exercised in a test and
> appears in no picture because the seeded board is calm. Give the S2 sheet fixture one item in `alert`
> mood (an overdue task) so every language's alert state renders on S2. Report for each language what
> changed in S2 (quote the cells), confirm blueprint's fixation now shows in the svg with the
> reverse/knockout tier, and confirm "exactly one knockout per view" still holds for blueprint S2.
> Re-render: expect eleven S2 frames changed; list any other. Extend inc41's tier comparison so the
> alert run is asserted painted in blueprint S2.

### 0a. The one place this increment departs from the ruling, and why

**The ruling says "give the S2 sheet fixture one item in `alert` mood (an overdue task)". The fixture
already has one**, and adding a second would have changed eleven `S1` frames (the list reads `TASKS`)
and no `S2` frame at all (the form does not). What was missing was never the ITEM — it was that
nobody ever handed the FACT to a kit. So the fixture states the mood it already implies, derived from
`TASKS` rather than typed, and `screens.s2` sets `k.mood` from it. Everything the ruling asks to be
confirmed is confirmed below; the count of moved frames is not eleven and §3 says why in numbers.

---

## 1. What was there

```python
# taskboard/language.py, Kit.__init__
# board MOOD, set by the app each redraw ("clear" / "busy" / "alert");
self.mood = "clear"
```

```python
# prototypes/components/screens.py -- six builders, and not one assignment
$ grep -c "mood" prototypes/components/screens.py       # before inc56: 0 assignments
```

`Blueprint._state_cell` has reversed on `alert` alone since inc17, and its own docstring says the
consequence: *"a sheet with nothing overdue carries no reversed cell at all"*. `spec.md` §9.3 q3 ruled
that **unspent, not missing** — correctly, because it is what makes operator ruling 10's move to the
confirm legal by arithmetic. What nobody closed is that a mechanism which is only ever unspent is a
mechanism nobody can look at, and the sweep is the thing people look at.

## 2. The mechanism, in two seats

**(a) The fixture derives the fact from its own content.**

```python
MOOD = ("alert" if any(d is not None and d < 0 and phase != "done"
                       for _t, _p, phase, d, _pr, _s in TASKS)
        else "busy" if TASKS else "clear")
```

**Derived and not typed**, so a fixture whose tasks all come back on time says `busy` here without
anybody remembering to change a second line — and so that the rule is the app's own rule, quoted from
`Blueprint._state_cell`: *"anything overdue and not done"*.

**(b) `screens.s2` hands it over**, `k.mood = F.MOOD`, one line before `chrome()`.

**WHY THIS SHEET AND NOT ALL SIX, and it is arithmetic rather than taste.** `s4_blueprint` spends that
language's single knockout on the destructive default answer under operator ruling 10, and it is
affordable there *because the title block's knockout is unspent* — its own docstring says so and
`test_exactly_one_knockout_per_view_still_holds_on_blueprints_confirm` counts it. **An alert mood on
S4 would light the title block as well: two knockouts on one view, which is ruling 10's own condition
broken.** So the fact goes to the sheet with no knockout of its own. Written into `s2`'s docstring.

## 3. What changed in S2, per language — quoted, and the answer is ten times "nothing"

```
naught      0 rows      corgi       0 rows      instrument  0 rows
swiss       0 rows      industrial  0 rows      nord        0 rows
darkside    0 rows      prism       0 rows      ledger      0 rows
solari      0 rows
blueprint   3 rows
   29 - '       ┌    ┐                    ─────────'
   29 + '       ┌    ┐                  ───────────'
   30 - ' board  FORM  cfg  log           ├ CLEAR ┤'
   30 + ' board  FORM  cfg  log         ├ OVERDUE ┤'
   31 - '       └    ┘                    ─────────'
   31 + '       └    ┘                  ───────────'
```

**The word is longer, so the dimension around it grows and the registration marks move — which is the
two-channel law working in the `.txt`: the state is a SPAN with a word riding on it, and the reverse
is spent on attention alone.** `_state_cell`'s docstring says exactly that, and this is the first frame
in the repo where it can be read.

**WHY TEN LANGUAGES DID NOT MOVE, measured rather than guessed.** `self.mood` is read at exactly three
places in `taskboard/language.py`, and one of them is the assignment:

```
Kit.__init__     line 1421   self.mood = "clear"                      (the write)
Naught.face      line 4264   mask = self.FACES.get(mood or self.mood, ...)
Blueprint._state_cell  9271  word = self.STATE.get(self.mood, "CLEAR")
                       9274  self.mood == "alert"
```

**Two kits of eleven read it.** And naught's reaches a frame only through `face()` → `mascot()` →
`Kit.empty_state()`, which S2 does not compose — measured by setting the mood globally in a probe:
under `alert` on every screen, exactly **seven** of the 66 frames move (`blueprint_S1`…`S6` and
`naught_S6`, naught's empty-state face), and `naught_S2` is not among them.

**So the ruling's "every language's alert state renders on S2" is not something a mood can deliver
today.** The other nine languages have an alert HUE — `cal_cell("over")`, the card's overdue tone, the
`over` rung of each `COVER_RAMPS` — and every one of those seats is handed a CARD or a DAY, never the
board. A screen that showed nine languages' alert state would need a per-item alert on the form, which
is a design increment: `Blueprint`'s own class docstring already names the per-item knockout as the
follow-up ("a per-item knockout is the named follow-up"), and that is the same seat.

## 4. The law

> **Blueprint's first fixation is painted on the form.** `blueprint_S2` carries exactly ONE ` on ` tag,
> it is the title block's state cell, the `.txt` reads `├ OVERDUE ┤` (and no longer `├ CLEAR ┤`), and
> the `.svg` paints a rect of this kit's INK at that cell with the text inside it in this kit's GROUND.

`test_blueprints_first_fixation_is_painted_on_the_form`.

**IT EXTENDS inc41's TIER COMPARISON THE WAY inc54 DID.** inc41 asserts *declared == painted* over 66
frames as SETS; inc54 asserted WHICH run carries the ground on S4 and what is inside it; this asserts
the same of the ALERT run on S2. The rect is found by the kit's own ink and the reversed text is
matched **at the rect's own x**, because the state cell is the fourth thing on that row and a search by
colour alone finds the mode strip's words first:

```
<rect x="270.4" y="520.0" width="92.4" height="17.0" fill="#eef4f8"/>
<text x="270.4" y="533.3" fill="#123a5c">├ OVERDUE ┤</text>
```

**"Exactly one knockout per view" is confirmed for S2** in the same test, counted on the composed rows
the way inc54 counts it for S4 — `sum(r.count(" on ") for r in rows) == 1` — and the one row that
carries it is quoted in the failure message.

**AND THE MECHANISM IS SHOWN SPENT RATHER THAN MERELY PRESENT**: the same kit's seat is read in both
moods (`("├ CLEAR ┤", False)` and `("├ OVERDUE ┤", True)`), so a cell that reversed in every mood
could not pass.

**`GROUNDED_FRAMES` 15 → 16**, `blueprint_S2` added, and the roster's own docstring records that this
one arrived because a FACT was handed over rather than because a declaration changed — nothing in
`Blueprint` moved.

## 5. Teeth

`test_a_form_never_told_the_mood_shows_no_first_fixation` — `F.MOOD` patched back to `clear`, which is
what every sheet in `screens.py` did until this increment, and the real composition re-run:

- blueprint's S2 carries **zero** ` on ` tags and the title block reads `├ CLEAR ┤`;
- **the other ten are asserted byte-identical either way**, which is the arm that says the ten
  unchanged frames in §3 are a fact about the kits and not about this patch.

**IT PATCHES THE FIXTURE AND NOT THE KIT, deliberately.** Patching `Blueprint.mood` would prove the kit
reads an attribute; decision (G) is about the fact that nobody ever WROTE to it, so the teeth run the
real composition with the real default.

**And the law was watched fail by hand on the real composition** — the line `k.mood = F.MOOD` deleted
from `screens.s2` and `render.py` re-run, so the frames on disk were the pre-inc56 ones:

```
$ python -X utf8 -m pytest tests/test_components.py -q -k "fixation or not_vacuous"
>       assert sum(r.count(" on ") for r in rows) == 1, \
E       assert 0 == 1
FAILED tests/test_components.py::test_blueprints_first_fixation_is_painted_on_the_form
        - AssertionError: []

>       assert sorted(got) == sorted(GROUNDED_FRAMES), got
E       assert ['blueprint_S...dger_S1', ...] == ['blueprint_S...rial_S6', ...]
FAILED tests/test_components.py::test_the_ground_law_is_not_vacuous
        - AssertionError: ('industrial_S1', 'darkside_S1', 'prism_S1', 'ledger_S1', '...

2 failed, 2 passed, 729 deselected in 0.41s
```

**The failing message on the first is `[]` — the list of rows carrying a ground, empty** — which is the
finding stated as an artefact: there is no reversed run on that frame at all. `screens.py` was restored
from a byte copy (`prototypes/out/_b56_screens.bak`) and `render.py` re-run.

## 6. Frames changed — `blueprint_S2` only

```
 M prototypes/components/blueprint_S2.svg
 M prototypes/components/blueprint_S2.txt
```

**One, where the ruling expected eleven.** §3 is the measurement and the reason. Ink 13.1% →
**13.3%** — two cells: `CLEAR` (5) becomes `OVERDUE` (7) and the dimension's two terminators stay,
so the span grows by exactly the word.

**Gallery: 0 of the 22.** `capture_languages.py` composes boards and a component sheet, not the six
canonical screens, and neither sets a mood.
**Census: 33 → 33, homoglyph rows 4 → 4** — no declaration changed.
**Of the eight gallery frames installed in the skill, none moved**; `blueprint_S2` is not one of them.

## 7. Risks

- **THE SAME SEEDED BOARD IS NOW `alert` ON S2 AND `clear` ON THE OTHER FIVE.** Two frames of one
  fixture disagree about the same fact, and that is a real cost, not a rounding error. It is taken
  knowingly: the alternative — the mood on every sheet — puts two knockouts on `blueprint_S4` and
  breaks operator ruling 10's condition. **The honest fix is a per-item knockout that does not collide
  with the confirm's, which `Blueprint`'s class docstring has named as the follow-up since inc17.**
  Written into `screens.s2`'s docstring so the next reader meets it there.
- **The `.txt` gains a word and loses two hairlines.** `├ OVERDUE ┤` is wider than `├ CLEAR ┤`, so the
  title block's state span grows into the row. At 100 cells it fits; at the block's narrowest live seat
  (`TB_MIN = 42`) `block_cells`' declared drop order sheds `work` before `state`, which is asserted
  elsewhere and is why nothing here needed changing — but a longer STATE word than `OVERDUE` would be a
  new question.
- **`F.MOOD` is a fixture-level constant read by one builder.** A second builder that wanted it would
  copy one line; the honest move at that point is `build()` setting it once, and that is a change to
  the sheet contract rather than to a screen. Named so the copy does not happen silently — the same
  note `inc50.md` §9 made about `screens.s4`'s air.

## 8. Found by looking, not fixed

- **Only two of eleven kits read `Kit.mood`, and one of them reads it through `empty_state`.** The
  board's mood is described in `Kit.__init__` as the fact *"languages with a functional identity
  element read"* — measured, that is naught's face and blueprint's state cell, and nothing else in the
  corpus. **Nine languages have no board-wide channel at all**, which is a bigger finding than the one
  ruling G names and is the reason its frame count could not be met.
- **A global alert mood moves seven frames, and one of them is a problem.** `blueprint_S4` would carry
  the title block's knockout AND the confirm's. The arithmetic that makes ruling 10 legal is a
  coincidence of the fixture being calm, and it has now been measured rather than assumed.
- **`Kit.empty_state` is the only seat naught's mood reaches**, so naught's status face is on exactly
  one frame of six — `naught_S6`, the no-match state — and only if the sweep ever sets a mood. It does
  not, so today it is on none.
- **`test_win_clipboard_roundtrip` moved from GREEN to RED between two runs of the same tree**, again:
  green in the gate run that produced `1088 passed`, red in the identical re-run after the
  watch-it-fail restore (`1 failed, 1087 passed` — the same 1088 tests). It drives the real Windows
  clipboard through PowerShell (spec §10.6, §13.8). **Reported, not counted, not touched, and `1088
  passed` is not a claim about it either way.**

## 9. Gates, verbatim

```
$ python -X utf8 -m pytest -q                                              exit 0
1088 passed, 2 skipped, 4 warnings in 33.35s               (inc55 left 1086)

$ python -X utf8 -m pytest -q                    # re-run after the restore, exit 1
1 failed, 1087 passed, 2 skipped, 4 warnings in 34.86s
FAILED tests/test_app.py::test_win_clipboard_roundtrip
       - AssertionError: assert None == 'roundtrip 123 ABC taskboard'

$ python -X utf8 prototypes/verify_language.py                             exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                           exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py                           exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                           exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 0 of the 22 moved

$ python -X utf8 prototypes/collision_census.py                            exit 0
  TOTAL  33 -> 33      zero collisions: NONE
  TOTAL homoglyph rows  4 -> 4
```

**`1086 → 1088`:** the law and its teeth.

## 10. Pending — not this increment

- **inc57 — the hygiene the rounds named** (darkside's `(O)`, the `LEVELS` comment, the stepper claim
  in `capture_languages.py`, the eleven `field_row` leaders).
- **The per-item knockout** — the design increment §7 names, still the operator's.
- **Decision A**, **K2**, **K4**, **L1–L6**, **C2**, **C4**–**C7**, **E2**, **E3** untouched.

## 11. Suggested next task

**inc57 — the hygiene the rounds named**, then close the batch in `spec.md` §14.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1088 passed, 2 skipped` on the gate run;
      the re-run of the same tree after the watch-it-fail restore returned `1 failed, 1087 passed`, and
      the failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec
      §10.6) — reported, not counted, not touched (§8). `verify_language.py`
      ALL PASSED exit 0. `render.py` 66/330/0. `matrix.py` 66 of 66, refusals `[]`.
      `capture_languages.py` 22 captures, 0 moved. `collision_census.py` both self-checks green,
      33 → 33, homoglyphs 4 → 4.
- [x] **No secrets in code or output** — one derived fixture constant, one assignment in a screen
      builder, two tests and a roster entry. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none. The watch-it-fail experiment commented
      out one line and restored it; `git status` confirms the tree.
- [x] **File count within cap** — **3** (`prototypes/components/fixture.py`,
      `prototypes/components/screens.py`, `tests/test_components.py`). The 2 frame artefacts are
      written by `render.py`.
- [x] **Review packet attached** — this document. **The ruling's frame prediction (eleven) is reported
      as not met, with the measurement that explains it (§3, §8), rather than reconciled.**

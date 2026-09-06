# Increment 51 — the stepper gets the law inc39 said it needed, and stops being excluded from the one it had

**Batch:** `rework-4`, closing increment · closes `PROTOTYPE-inheritors-2.md` §5 **K3** and `spec.md`
§9.5's last open "found by looking" item
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files**, plus the census table
and this packet. **Frames changed: none.**

**`Kit.PART_GLYPHS["stepper.step"][INVALID]` has read `][` since the seat existed, and spec §9.5 has
carried it as a known defect since inc39 — which declined to fix it in the same sentence that said why:
*"a stepper's halves are DIRECTIONS, not walls, so it needs its own law"*. That law is written here, in
two clauses, over all eleven; six kits that spelled REJECTED by turning their two arrows round are moved
onto their own refusal marks; and the stepper's by-name exclusion from inc48's opener law is removed. The
bill inc48 §5 published in advance — swiss's and nord's `stepper.main`, five seats each — was PAID at the
declaration rather than exempted, so both stay at zero. The census falls 47 → 36, the largest single move
of the whole rework programme, and the live meaning×meaning count falls 8 → 6.**

---

## 1. Cause: a law that was named, deferred, and then used as the reason for a second exclusion

`Kit.PART_GLYPHS`, at the seat, says what the two cells are:

> *"THE TWO STEPS AS ONE EVEN STRING — the button's walls convention, read for direction instead of for
> sides: the first half is the step BACK and the second half is the step FORWARD. One declaration, two
> cells, and the cell's POSITION is what says which way it goes."*

inc39 fixed four FIELDS that spelled `INVALID` by exchanging their two walls and stopped at the stepper
(spec §9.5). inc48 then excluded the stepper from the opener law **citing inc39's deferral** — so one
unwritten law became the reason for a second exclusion, and both were recorded three times
(spec §9.5, §11.5, inc48 §5, and the round's §5 K3) without moving.

Measured, six of the eleven were carrying the turn:

```
                DEFAULT      INVALID      what INVALID is
nord / Kit      -+           ][           two brackets the stepper NEVER declares, facing IN
instrument      ⡄⢠          ⢠⡄          DEFAULT exchanged
swiss           ‹›           ›‹           DEFAULT exchanged
industrial      <>           ><           DEFAULT exchanged
prism           ⡀⢀          ⢀⡀          DEFAULT exchanged
blueprint       ┤├           ├┤           DEFAULT exchanged — and `├` is also REQUIRED
```

**And it is worse on a stepper than it was on a field.** inc39's argument against the flip was that *"the
two marks sit at opposite ends of a 34-cell row"*; on a stepper the two cells **TOUCH**, so the reader is
asked to compare two arrows side by side and remember which way they pointed in the state before.

## 2. The law

> **1. A step pair is two DIRECTIONS, and no state is another state turned round.** For any two states of
> `stepper.step`, one may not be the other with its halves exchanged. A pair whose halves are equal
> (`████`, `◆◆`, `ØØ`) has no handedness and cannot violate it — which is what keeps the law about
> ORIENTATION and not about repetition.
> **2. INVALID is said on the language's own refusal channel.** The cells `stepper.step[INVALID]` is drawn
> from must come from what that kit already spends on a rejected VALUE — its `knob[INVALID]` and its
> `textfield.main[INVALID]`, both read as DECLARATIONS so a kit cannot pass by inheriting one.

`test_a_steppers_halves_are_directions_and_invalid_is_not_a_turn[lang]`, eleven parametrisations.

**Why both clauses.** Clause 1 alone is satisfiable by inventing any unused mark, which is how a kit
acquires a cell nobody can read. Clause 2 says the mark must be one the reader has already met meaning
exactly this, elsewhere in the same language. **And clause 1 alone would have left the BASE's own defect
standing:** `nord ][` is not any nord state exchanged — `[` and `]` are the BUTTON's walls and the
CHECKBOX's well (census row `nord [ ] (4 each)`), a pair the stepper never declares. Only clause 2 reaches
it. That split is asserted in the teeth rather than described.

**Five of the eleven already obeyed both clauses** — `darkside ØØ`, `ledger ‡‡`, `solari ══`, `naught ◑◑`,
`corgi ▀▄▄▀` — which is what says the rule is the corpus's own and not an invention.

## 3. The six moves, each onto its own kit's refusal

| kit | was | is | the citation |
| --- | --- | --- | --- |
| **nord** (`Kit`) | `][` | `▚▚` | `knob[INVALID]` — the grip this kit wears when a value is refused; no direction to read |
| instrument | `⢠⡄` | `⠶⠶` | `knob[INVALID]`, and the fill of its invalid field (`⠸⠶⠇`) |
| swiss | `›‹` | `╲╲` | `knob[INVALID]` and `textfield.main[INVALID]` — inc39's ruling (spec §9.2), not a new claim |
| industrial | `><` | `//` | `knob[INVALID]`, and the hatch that fills a rejected field (`▐/▌`) |
| prism | `⢀⡀` | `⣹⣹` | `knob[INVALID]`, and the cell that opens its refused field (`⣹⠀⣏`) |
| blueprint | `├┤` | `━━` | what this sheet already draws around a refused value (`━·━`, inc39 §9.2). **Not `├├`**: `├` is `REQUIRED`, so doubling the knob's mark would have kept the obligation mark on a rejected stepper |

**`nord`'s is the base's line**, so patching `Kit` moves nord and nothing else — the same measurement
inc39 §9.3 q1 had to make, and the teeth assert it by checking the other ten stay clean under that arm.

## 4. The opener law loses its exclusion, and the bill is paid

`OPENING_CONTROLS` was `("button", "checkbox", "radio", "switch", "textfield")`. It is now those five
**plus `stepper`**.

inc39's ruling was right about ENCLOSURE and wrong about ANNOUNCEMENT: *"a law about what OPENS an
enclosure cannot be asked of a pair that encloses nothing"* is true, and irrelevant — whatever cell stands
first is what a reader meets first, whether it is a wall or an arrow. With the stepper's own law written,
the exclusion has nothing left to stand on.

**What it cost, and who paid.** inc48 §5 published the bill in advance: *"it costs the law swiss's and
nord's `stepper.main` (`··`, whose first cell is `LEVELS["info"]`), five seats each, and that is named
here rather than absorbed."* Both were paid at the declaration:

```
swiss   "stepper.main" DEFAULT  ··  ->  ▫▫    the lightest rung of the one-shape ladder inc46 built it
                                              (`▫ ▪ ■`), whose whole point is that no rung is a
                                              declaration. "Present, not acted on" is what an end-stop says.
nord    "stepper.main" DEFAULT  ··  ->  ░░    the lightest rung of the shade ramp this kit already owns
                                              (`░` shaft, `▒` dead indicator, `▓` press, `█` view) —
                                              what a terminal draws where there is nothing to act on.
```

**The opener roster, before and after:**

| language | before | after | why |
| --- | --- | --- | --- |
| **swiss** | 0 | **0** | the five seats were paid, not exempted |
| **nord** | 0 | **0** | same, at `Kit` |
| naught | 2 | **3** | `◉◉`, the ACTIVE step, opens with `REQUIRED` |
| corgi | 31 | **40** | the whole stepper: `▁▁▁▁` at five states of the ground, four of the step |
| prism | 19 | **25** | `⣀⣀` (the ground, five states) and `⡀⢀` (the DEFAULT step, first cell `REQUIRED`) |
| blueprint | 6 | **12** | `··` (`LEVELS["info"]`) at five states of the ground, `╌╌` (`warn`) at the dead one |
| instrument · industrial · darkside · ledger · solari | 0 | **0** | the widening reaches them and finds nothing |

**The four that grew were already on the roster** and are `PROTOTYPE-inheritors-2.md` §6 decision **A** —
corgi, prism and blueprint have never had an increment, and naught has no unspent cell (spec §11.5).
Counted by name with their reason, not fixed and not exempted.

## 5. Teeth

`test_the_stepper_law_goes_red_on_the_six_turns_inc51_moved`, seven arms:

- **six arms, one per declaration**, each restoring the exact byte string HEAD carried at `251511d`. Each
  must (a) make the parametrised law raise, (b) leave the other ten clean, and (c) for the five whose turn
  is their own DEFAULT exchanged, report hits that name **the INVALID state and the turned string**. The
  `STEP_TURNS` table carries a third column saying which clause is expected to fire, so **nord's arm
  asserts that clause 1 is SILENT** and clause 2 is what catches it — a claim, not an accident.
- **a seventh arm for clause 2 alone**: darkside's INVALID set to `≠≠`, a mark no kit declares. Clause 1
  passes it (both halves equal, no turn) and clause 2 must still be red — which is what says clause 2 is
  doing work rather than restating clause 1.

**Watched fail by hand, on the real declarations.** Reverting `Kit`'s `▚▚` to `][` and blueprint's `━━`
to `├┤`:

```
$ python -X utf8 -m pytest "tests/test_components.py::test_a_steppers_halves_are_directions_and_invalid_is_not_a_turn" -q
E       AssertionError: ('blueprint', [('default', 'invalid', '┤├', '├┤')])
FAILED ...[nord]      - AssertionError: ('nord', '][')
FAILED ...[blueprint] - AssertionError: ('blueprint', [('default', 'invalid', '┤├', '├┤')])
2 failed, 9 passed in 0.67s
```

**The two reds are different clauses on the same law**, which is the whole design: blueprint names the two
STATES and the two strings, nord names the string alone because there is no state to name. `language.py`
was restored from a byte copy taken before the experiment and the eleven re-run green
(`11 passed in 0.47s`).

## 6. Census delta — the largest of the programme

```
language      rework-3   inc49   inc50   inc51
naught             5        5       5       5
corgi              5        5       5       5
instrument         7        7       7       5
swiss              5        5       5       3
industrial         4        4       4       2
nord               4        4       4       1
darkside           3        2       2       2
prism              5        5       5       4
ledger             2        2       2       2
solari             3        3       3       3
blueprint          5        5       5       4
------------------------------------------------
TOTAL             48       47      47      36
```

**−11 in one increment**, against −6 across the whole of `rework-3`. The rows that went away are exactly
the turns: each `⡄`/`⢠`, `‹`/`›`, `<`/`>`, `[`/`]`, `⢀` and `┤` row existed *because* one state was
another turned round, so the cell carried both `INVALID stepper.step open` and `stepper.step close` at
once. `nord` is now **1**, the cleanest language in the corpus.

**And the number that matters more — live meaning × meaning — falls 8 → 6.** Counted the way §11.2 counts
it (rows carrying two or more A-families, with the four `DANGER_IS_THE_TOP_RUNG` exemptions subtracted):

```
before   naught ∙ · corgi ▄ █ ▀ · instrument ⠇ · swiss ╲ · darkside Ø · prism ⣿ ⡀ · blueprint ├ · ━   = 12 - 4 = 8
after    naught ∙ · corgi ▄ █ ▀ · instrument ⠇ · swiss ╲ · darkside Ø · prism ⣿   · blueprint · ━     = 10 - 4 = 6
```

**`prism ⡀` and `blueprint ├` are closed** — both were `REQUIRED` sharing a cell with an `INVALID
stepper.step`, which is to say both of the eight live rows that spec §11.2 says *"every one of the eight
left involves `INVALID`"* and that were the stepper's.

## 7. Frames changed: **none**

`render.py` rewrote all 66 and **not one artefact moved**; `capture_languages.py` rewrote all 22 and
**not one moved**. The brief's condition — *"add one row to the S3 sheet only if the sheet already has a
stepper"* — is not met: the S3 component sheet draws switches, selects and a slider, and no stepper.

**And this increment proves something stronger than "no frame renders an INVALID stepper".** Eight
declarations changed across seven kits, two of them `stepper.main[DEFAULT]` — the string every LIVE state
of the ground falls back to. If any of the 88 `.txt` drew a stepper in any live state, swiss's or nord's
would have moved. **No artefact in the repo draws a stepper at all** (a stepper drawn only in DISABLED
would still escape this argument, and is named here as the one hole in it). `capture_languages.py`'s own
docstring says the component sheet carries *"and stepper, each in the states the registry derives"* — at
118×34 the sheet does not reach it. **So the law stands on the property test alone, which is stated rather
than glossed over.**

## 8. Gates, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1054 passed, 2 skipped, 4 warnings in 34.03s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'

$ python -X utf8 prototypes/verify_language.py                                        exit 0
ALL PASSED

$ python -X utf8 prototypes/components/render.py                                      exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
  -> 0 of the 66 moved

$ python -X utf8 prototypes/components/matrix.py                                      exit 0
  11 x 6 = 66 cells, every one `implementa`; refusals [] for all eleven

$ python -X utf8 prototypes/capture_languages.py                                      exit 0
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
  -> 0 of the 22 moved

$ python -X utf8 prototypes/collision_census.py                                       exit 0
  self-check  1 of the 5 collisions the round found by hand still come back out of
              the census; 4 are asserted CLOSED and cannot grow back
  TOTAL  47 -> 36

$ python -X utf8 prototypes/export_to_skill.py "C:/Users/jjgh8/.claude/skills/tui-design"   exit 0
  wrote assets\languages.py (22 KB, 11 languages)
  verified: 11 languages, every token, doc and family round-trips
  captures: 2 written, 64 already identical            <- gallery_darkside.{txt,svg}, inc49
  wrote SURFACES.md (11 postures)

$ (re-run, the idempotence check)                                                     exit 0
  captures: 0 written, 66 already identical
```

**`1042 → 1054`: +12** — eleven parametrisations of the stepper law plus its teeth. The clipboard red is
`test_win_clipboard_roundtrip`, environment-coupled (spec §10.6), red at `a8a7a5d` before this batch
began — **reported, not counted, not touched**.

**The skill's installed gallery, frames 44–51: all eight are byte-identical to their sources, and none of
them changed in `rework-4`.** The five that spec §11.4 listed as stale (45, 46, 48, 49, 50) carry an
mtime of 2026-09-06 12:54, before this batch's first commit — the manual re-install §11.4 asked for was
done outside it. This batch's three moved frames (`darkside_S2`, `darkside_S3`, `solari_S4`) are not
sources for any of 44–51. **The skill repo was not committed.**

## 9. Risks

- **`swiss ▫▫` puts the button's DEFAULT rung on the stepper's dead end.** It is chrome-on-chrome, which
  the census counts as alphabet, but `swiss_S1`'s standing note is already *"four solid rectangles at four
  sizes (`▫ ▪ ■ ▮`)"* and this adds a fifth SEAT to that vocabulary even though it adds no new cell.
  One line to reverse.
- **`nord ░░` is the base kit's line**, so it is nord's answer and nobody else's — but `░` is also this
  kit's `scrollbar.main[DEFAULT]`. Both say "ground you cannot act on", and they are different components
  at different widths; a reader who reads `░░` as a scroll shaft has read it wrong in a way the shaft's
  own docstring (*"a slider's track is a SCALE and a scroll bar's is a SHAFT"*) did not anticipate.
- **`blueprint ━━` spends `━` a FIFTH time.** `PROTOTYPE-inheritors-2.md` §4 lists `blueprint_S5` as an
  objection that got worse without its label moving, precisely because `━` accumulated roles
  (`LEVELS["error"]`, `DANGER_FORM`, both walls of the invalid field, the sparkline peak). This adds the
  invalid stepper. **The defence is that it is inc39's ruling applied consistently — decision (C) — and
  the alternative was `├├`, which is `REQUIRED`.** Both options are on a cell that already speaks; the
  operator's ruling on C decides which is right, and this increment took the one inc39 already took.
- **None of it is in a picture.** §7: no artefact draws a stepper, so every claim here is a claim about
  declarations, verified by a property test and by nothing a reader can look at.
- **The opener roster now asserts four counts that got bigger** (naught 3, corgi 40, prism 25,
  blueprint 12). A batch that opens any of those three unjudged languages will go red on numbers that look
  like regressions and are the record. Same design note inc48 §9 and inc49 §10 carry.

## 10. Found by looking, not fixed

- **`capture_languages.py`'s docstring overstates what the sheet shows.** It lists *"and stepper, each in
  the states the registry derives"* among what `gallery_<lang>.txt` captures; at 118×34 the component
  sheet is cut off after the switch and checkbox rows. **The one component all eleven declare is the one
  component nobody has ever seen rendered.** Naming it rather than fixing it: making the sheet taller is a
  capture-geometry change that would move all 22 gallery artefacts, which is not this increment's.
- **`Darkside.LEVELS`' comment still cites a `CUR` that moved in inc45** (reported in inc49 §11, still
  true).
- **`Darkside.tabs()` and `wordmark()` still print `(O)`**, outside `PART_GLYPHS` where no law reaches
  (inc49 §11).

## 11. Pending — the operator's, untouched by this batch

Listed rather than acted on, which is what the batch was scoped to:

- **A** — corgi, prism and blueprint have never had an increment; twelve of the 66 frames are unjudged.
  This batch made their rosters BIGGER and more precise and fixed none of them.
- **C** — `INVALID` takes the `DANGER_FORM` (inc39's ruling). **inc51 applied it a sixth and seventh
  time** (swiss `╲╲`, blueprint `━━`) because it is the ruling of record; if C is reverted, those two
  lines revert with it.
- **D** — is diameter/rotation a channel a language declares? inc49 refused a homoglyph move on that
  ground and said so at the seat.
- **E** — `darkside_S1`: the rail or the `.txt`.
- **F** — may a solari confirm eat the gate it names? **inc50 came within one design decision of it and
  stopped** (inc50 §4).
- **G** — blueprint's first-fixation law is in a test and in no image.
- **C1** — `blueprint_S4`'s destructive control is built with `knockout_cell` instead of `button`, so it
  carries no danger mark and no focus mark in either tier. Named in inc41 §8, untouched here.

Also still open and not this batch's: **K2** (the three laws compare code points), **K4** (no law compares
two states of one part), **L1–L6**, **C2**, **C4**–**C7**, **E2** (the `.svg` has no font metric) and
**E3** (`gallery_darkside` is calendar-dependent).

## 12. Suggested next task

**corgi.** It is decision A's sharpest entry and this batch made the case worse on paper: 40 opener seats
(up from 31), 16 named seats (up from 8), 3 live meaning×meaning rows. Its four-step block ramp is
`LEVELS`, the chrome ladder, the danger form and the obligation mark at once, and no frame of it has ever
been judged.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1054 passed, 2 skipped, 1 failed`; the
      failure is `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6), red
      before this batch began — reported, not counted, not touched. `verify_language.py` ALL PASSED
      exit 0. `render.py` 66/330/0, 0 of 66 moved. `matrix.py` 66 of 66. `capture_languages.py` 22
      captures, 0 moved. `collision_census.py` self-check green, 47 → 36. `export_to_skill.py` exit 0,
      idempotent on re-run.
- [x] **No secrets in code or output** — eight glyph-table entries and one test block. No network, no new
      dependency. The only path outside the worktree is the skill directory the export is invoked with,
      and **the skill was not committed**.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The two watch-it-fail experiments used byte copies of `language.py` and
      restored from them; the working tree's line endings were restored to the repo's CRLF convention
      after a scripted edit normalised them, and `git diff --stat` is unchanged by that.
- [x] **File count within cap** — 2 hand-written source files (`taskboard/language.py`,
      `tests/test_components.py`); the census table is written by a gate script.
- [x] **Review packet attached** — this document.

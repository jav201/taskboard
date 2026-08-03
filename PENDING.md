# PENDING — open items

---

# CLOSING STATE — 2026-07-28, sixty-ninth pass. **THE SKILL NOW HAS A RUNNABLE EXEMPLAR AND — FOR THE FIRST TIME IN THIRTEEN DOCUMENTS AND SIXTY-NINE PASSES — A LAW OF ITS OWN. `verify_exemplar.py`: 51 CHECKS, ALL PASSED ×3; SIX MUTANTS AT 1, 3, 1, 5, 2 AND 1 RED, NONE VACUOUS; BASELINE == RESTORED BYTE FOR BYTE.**

> Updated by the sixty-ninth pass (**#3 CLOSED**; nothing added). **THE COMPONENT-CONTRACT TRACK'S
> ITEM LIST IS DONE** — see the TRACK CLOSING NOTE at the end of this block, which also states the
> ledger's remaining OPEN rows honestly, including the three the pass-68 recommendation did not
> predict. The sixty-eighth pass's block follows unchanged below.

**THE BUDGET SPANNED TWO TREES, AND IT WAS DECIDED BEFORE THE INCREMENT RATHER THAN DURING IT** —
which is what item #3's need (3) asked for, and what no pass in this series had done. Three files
in the SKILL repo (`assets/exemplar.py`, `assets/verify_exemplar.py`, `SKILL.md`) and **exactly one
here** (this file). Nothing else in either tree moved; `git status` in this worktree carries the
same pre-existing modifications it carried at pass 68's close. **No commit, no push** — the skill
repo's owner pushes it.

## What shipped, and where

| file | tree | what it is |
|---|---|---|
| `~/.claude/skills/tui-design/assets/exemplar.py` | SKILL | ONE screen, **426 code lines** under **525 lines of citation** (951 total — the prose is the artifact's job, and the number is stated rather than rounded) |
| `~/.claude/skills/tui-design/assets/verify_exemplar.py` | SKILL | **the law** — 51 checks, standalone, crash-safe, its own verdict line, exit code |
| `~/.claude/skills/tui-design/SKILL.md` | SKILL | two index entries, above the reference-file list |
| `PENDING.md` | HERE | this block |

**It is SELF-CONTAINED, and that was a ruling rather than a convenience.** It imports nothing from
this worktree. `taskboard/language.py` is 6812 lines and is a SHOWCASE, not a library; an exemplar
that leaned on it would teach the taskboard. Every seat is re-implemented at exemplar scale — a
three-entry parts registry, one value seat, one coverage seat, one motion engine.

## The doctrine map — which document each piece renders

The language is **PUNCH**, invented for the file: a punched-card instrument committing on three
STRUCTURAL axes (drawn 4x5 numerals at `sx=2` on a visible unpunched field · the **sprocket rail**
as the only divider, no boxes anywhere · the ramp `·░▒█` as the one quantity family every chart and
every control draws from). The screen's subject is **the skill's own BUDGET.md**: `H`, computed
from a region table written before the screen, drawn as the hero.

| piece | the doc it renders |
|---|---|
| brief · posture · task flow, in the module docstring | SKILL.md workflow 0-1, INTAKE.md |
| token dict where **every key is consumed**, mutation-tested | LANGUAGES.md ("code, not a manifest") |
| 4x5 mask, tabular advance, `sx=2`, gap drawn UNLIT | COMPONENTS.md display type + drawn-glyph metrics |
| three brightness tiers + ONE reserved semantic hue | HIERARCHY.md brightness ladder |
| the drawn hero as the signature — it RENDERS, never labels | SKILL.md signature critique |
| registry · `actuator` · derived axis · CHECKED product · one `value_pos` | COMPONENTS.md, the contract |
| coverage as an INDEX, the microbar floor at ONE seat, the no-dither ruling | DATAVIZ.md, the coverage primitive |
| shared declared scale · unlit track · clip-and-FLAG · chrome once | DATAVIZ.md laws 2, 3, 4, 9, 11, 12, 13 |
| legend DERIVED from `active_bindings`, aliases printed, three width tiers | COMPONENTS.md, the legend law |
| `can_focus` decided by the CONTRACT; focus on two channels | NAVIGATION.md |
| two transitions as LISTS OF RENDER STATES, regime off the EVENT, refresh floor | MOTION.md |
| the region/class/cost table and `H >= 5` as a gate | BUDGET.md |

**The four rulings the exemplar made, each named in the file where it happens.**

* **A `bar` is not a slider we chose not to focus.** Its two-entry axis, its absence from
  `motion_events`, and `can_focus = False` on its widget all fall out of `actuator("bar") is None`.
  Mutant M2 (give the bar a knob) reds exactly those three and nothing else.
* **The composed screen is a PURE MODEL first.** Every structural law measures the model with no
  Textual import; a separate drive law then asserts **the composited frame IS the model, row for
  row**. That pair is what caught this file's two worst defects (below).
* **NO AMBIENT, and it is a decision.** The screen is glanced at, so nothing loops in the reading
  path. Two `transition`s ship; the ambient regime exists in the table and is asserted unreached.
* **The bar's readout was changed because it could not vary.** It first showed the tick's share of
  a frame — 0.3 %, drawing zero at every value, DATAVIZ law 13's own defect. It reads the flip's
  per-step duration now, which the slider beside it governs.

## The law — 51 checks, and the oracles do not call the seats they measure

Blocks: registry and derivations (6) · render read off its own part TAGS (4) · greyscale two-channel
(4) · value model (2) · data-viz laws (8) · hierarchy and the first fixation (6) · the legend (3) ·
motion (6) · tokens (3) · budget (1) · the headless drive (8).

**THE MUTATION BATTERY, and its own restore discipline.** A `.ORIG` written before the first edit,
restored in a `finally`, every anchor verified before the run, and the baseline re-run afterwards
requiring the ORIGINAL count.

| mutant | reds | what it proves |
|---|---|---|
| M1 the microbar floor removed | **1** | the floor's single seat is load-bearing |
| M2 the bar is given a knob | **3** | axis, motions and focusability are all DERIVED |
| M3 indicator == main (separated by HUE alone) | **1** | the shape law sees what greyscale pairs do not |
| M4 clamp instead of clip | **5** | and three of the five are the row budget and the frame-is-the-model pair — a lie in a bar's length wrecks the layout |
| M5 the legend hand-written, with a phantom key | **2** | see below |
| M6 the tempo pushed into the illegal 400-2000 ms gap | **1** | the regime is a check, not a comment |

**M5 SURVIVED ITS FIRST RUN AT ZERO RED, AND THAT IS THE PASS'S SHARPEST FINDING ABOUT ITS OWN
INSTRUMENT.** The two legend laws asked `binding_pairs` for the truth and then checked a row built
from `binding_pairs` — **an oracle calling the function under test moves with the mutant**, which is
VERIFY.md's own named hole, reproduced in this suite's first draft. Both laws now re-derive from
`screen.active_bindings` and from the DECLARED `_KEY_NAMES` map, and split the row on the separator
rather than on the renderer's join convention, so the oracle knows nothing the renderer knows.
Same mutant: **2 red**.

## FOUR DEFECTS THE LAWS CAUGHT IN THE EXEMPLAR ITSELF — the artifact was wrong four times first

None of these were visible in the source, and all four are recorded rather than quietly fixed.

1. **A float boundary read as an overflow.** `0.56 / 0.02` is `28.000000000000004`, so the last
   IN-RANGE sample flagged itself as clipped. Caught by the clip law asserting at the exact cell
   where the tier is bought, not at a list of widths.
2. **A dead `tab` binding, shipped and indicated nowhere.** `Binding("tab", "swap", …)` was written
   and Textual resolves `tab` to its own `app.focus_next` — so the action never fired AND the key
   never reached the legend. **Deriving the row from the LIVE bindings is what surfaced it**; a
   hand-written legend would have advertised it happily. The binding is deleted and the render
   follows focus instead.
3. **An 80-cell rail WRAPPING inside a padded widget**, each wrapped line silently doubling.
4. **Every gap row dropped on the floor.** The model carried the empty rows that buy the hero its
   isolation and the GLASS DID NOT — so the first-fixation law was measuring a screen nobody was
   looking at. Defects 3 and 4 were both caught by the row-for-row law, which did not exist until
   the render was LOOKED AT.

## The item's four needs, answered — and where one was RESTATED rather than met literally

1. **Structure, not tone, measurable.** The item asked for "the greyscale diff between TWO
   languages' exemplar renders". **The exemplar ships ONE language, so that measurable is not
   available and a different one is used** — said here rather than glossed: **every structural
   token mutated must MOVE the greyscale render** (6 tokens, all consumed), **with a colour-only
   mutation as the CONTROL that must move NOTHING** (5 colour tokens, zero structural movement).
   The pair is arguably the stronger claim — a two-language diff can be passed by two languages
   that both carry structure in tone — but it is **not the claim the item wrote**, and the
   substitution is the reader's to accept or reject.
2. **Every glyph from a kit seat.** Held as a source law: no frame builder holds a drawn-glyph
   literal (`motion_frames`'s source is pure ASCII), no derivation or composer seat names a
   component, and every mark on the screen comes from `PART_GLYPHS`, the ramp or the pixel base.
3. **A home in a different repo.** Done, and the two-tree budget was decided up front (above).
4. **A law.** `verify_exemplar.py`. The skill has one now.

## Verification

| suite | result |
|---|---|
| `python assets/verify_exemplar.py` (skill repo) | **51 passed, 0 failed — ALL PASSED**, three back-to-back runs |
| the six-mutant battery | 1 · 3 · 1 · 5 · 2 · 1 red; **baseline == restored** |
| headless drive at 80x30 and 100x34 | composes, settles in 1 iteration, no row wraps at either size |
| the composited render | **looked at** — pasted in the increment's report, per VERIFY.md |
| `prototypes/verify_language.py` (HERE) | **9923 / 0, ALL PASSED** — unchanged, proving zero coupling |

**WHAT THIS PASS DID NOT DO, NAMED.** The exemplar was never opened in a real terminal — every
verdict here is from `run_test`'s compositor, exactly as every render claim in this series has been
since pass 61. Its glyph coverage is **attributed, not measured** (`·░▒█ ▚ ▞ ▌ »` and the
box-drawing focus rail), which is the one thing this skill says can never be measured. The other
five worktree suites were not re-run: this increment touches no file in this tree except this one,
and `verify_language` at 9923 is the load-bearing negative control.

## TRACK CLOSING NOTE — the component-contract track's item list is DONE

With #3 closed, **every item the component-contract track filed is closed**: the contract itself
(#1, pass 55), the motion axis (#36, pass 68), the last two items that move shipped cells (#46 and
#36, pass 68), and now the exemplar. **The track is finished; the LEDGER is not**, and the
difference is worth stating plainly.

**THE REMAINING OPEN ROWS ARE SEVEN, NOT THREE — and pass 68's recommendation predicted three.**
Said loudly because a closing note that agrees with its own forecast is not a measurement:

| # | row | shape |
|---|---|---|
| **2** | the gallery should demo `plot` variants | OPEN, partly served; the layout half is closed |
| **22** | `test_win_clipboard_roundtrip` has no skipif/mock | **WATCH** — env-dependent, proved; failed once in pass 68's round 3 |
| **26** | `invalid` is not a control state | OPEN — **named shape, not started** (a `VALIDATABLE` registry tuple) |
| **30** | the component family is closed, the INVENTORY is not | OPEN — select/dropdown (a POPUP question first) and tabs/segmented |
| **31** | a single trailing backslash cannot be rendered beside a close tag | OPEN — measured, asserted, **not curable at that seat** |
| **32** | the escaping defect at 40 sites | **APP half DEFERRED** to real app work; design half closed at pass 57 |
| **34** | a bracketed queue title renders ONE CELL SHORT | OPEN — measured, not introduced by the sweep, not cured |

Plus two standing **watches**: the settle timeout (zero in eleven runs on a quiet machine at pass
68, two in four on a loaded one — consistent with the load hypothesis and **not proof of it**), and
#22's clipboard. Of the seven, **#22, #31, #32-app and #34 are app questions or env questions**;
**#2, #26 and #30 are design work that would open a NEW track** rather than continue this one.

**THE RECOMMENDATION FOR THE SEVENTIETH PASS: #22, and it is now the only item that costs less than
a track.** Give the clipboard test a `skipif` or a mock the next time `tests/` is opened — a test
that flips on another process holding the Windows clipboard is how a suite learns to be ignored, and
it has now produced a red in two separate passes' evidence blocks (64 and 68) that had to be
explained away rather than fixed. Everything else on the list is a batch.

---

# CLOSING STATE — 2026-07-28, sixty-eighth pass. **THE FIFTY-NINTH PASS'S OWN PROVER, RUN UNMODIFIED AGAINST THIS TREE, REPORTS `steps under the 16.7 ms floor: 0 ([])` WHERE IT REPORTED 5. THAT IS THE ACCEPTANCE TEST, AND IT IS THE INSTRUMENT THAT FILED THE ITEM RATHER THAN ONE WRITTEN TO AGREE WITH THE CURE.**

> Updated by the sixty-eighth pass (**#46 and #36 CLOSED**; nothing added). The sixty-seventh pass's
> closing block follows unchanged below; its table's stamps are current except where this block
> supersedes them. **The register's OPEN rows are now #2, #3, #22, #26, #30, #31, #34 and the APP
> half of the SPLIT row #32** — the last two items that MOVE SHIPPED CELLS are closed, and every
> remaining one is a track, a watch or an app question.

**THE ACCEPTANCE TEST, IN FULL.** `python prototypes/out/_p59_prove.py`, unmodified, §5:

| | pass 59 (as filed) | pass 68 (cured tree) |
|---|---|---|
| industrial `travel` | **15.0 ms UNDER** | 30.0 ms |
| solari `press` | **8.0 ms UNDER** | 20.0 ms |
| solari `travel` · `spin` · `flip` | **10.0 ms UNDER** ×3 | 20.0 ms ×3 |
| verdict line | `steps under the 16.7 ms floor: 5 (['industrial', 'solari'])` | `0 ([])` |

**That prover still RUNS, and that is the second half of the finding** — it subclasses three motion
builders, and the first form of this cure would have killed it. See the token/parameter argument
below.

---

## #36 — THE PER-STEP REFRESH FLOOR. A CEILING ON ELABORATION **PLUS** AN ABSOLUTE FLOOR, BECAUSE IT IS TWO CLAIMS

**THE ITEM PRESCRIBED ONE LEG AND THE TREE NEEDED TWO.** #36's text says the cure is "cap the gaps
at `tempo // refresh`". That closed form was written, measured and rejected, for a reason the item
could not have known: **`travel`'s frame count is the DISTANCE's** (pass 51's group scope), so its
gaps are not the language's to give back. A cap on the frame COUNT would have had to drop a WELL to
satisfy itself, which is the one thing the travel law forbids.

* **THE CEILING governs what the language CHOOSES.** It drops one `MOTION_STEPS` at a time and
  **rebuilds**, taking the largest elaboration whose derived step clears the floor. It **asks the
  builder** rather than restating each event's gap arithmetic at the ceiling: `press` adds one gap
  per step, `travel` adds one per **well crossed**, `spin` and `flip` one per mid frame. A closed
  form would have to know all four and go stale the day a fifth event lands — which is pass 66's
  shape-2 defect (a re-typed formula) wearing a ceiling's clothes.
* **THE FLOOR governs what the STRUCTURE owes.** `step = max(tempo / gaps, REFRESH_MS)`. At zero
  elaboration what is left is wells, and a long enough travel at a short enough tempo is under the
  floor with nothing to renounce. **There the pass RUNS LONG rather than the engine claiming a step
  the surface will not draw**: solari across four wells is 4 frames at 16.7 ms = 50 ms against its
  40 ms tempo. Measured, and **no shipped fixture reaches it** — all forty shipped transitions land
  on exactly one tempo, so "a transition's whole pass is one tempo" is still true everywhere it is
  drawn.

**THE FIRST FORM OF THE CEILING KILLED THE SUITE ON ITS FIRST MUTANT, AND THAT IS THE PASS'S SHARPEST
FINDING ABOUT ITS OWN INSTRUMENT.** The ceiling needs to ask "what would this look like at n-1
steps", and the obvious way is a `steps=` argument on the four builders. It ran for exactly one
mutant: `TypeError: _MOneFrame._motion_press() got an unexpected keyword argument 'steps'`. **The
battery's whole method is to SUBCLASS a builder** — six overrides in the suite, four more in
`_p59_prove.py` — so a ceiling that makes every override grow an argument is **a ceiling that taxes
the instrument measuring it**. What the ceiling varies is the language's own `MOTION_STEPS`, so it
varies exactly that, on a `copy.copy` of the kit, and every builder — overridden or not — is asked
the question in the only vocabulary it already speaks. **Zero builder signatures changed.**

**WHAT MOVED: FIVE STEPS, EXACTLY THE FIVE PASS 59 MEASURED — AND THE TEMPO IS UNTOUCHED.**

| language | tempo | event | PRE | POST | elaboration |
|---|---|---|---|---|---|
| solari | 40 ms | `press` | 6 frames @ 8.0 ms | **3 @ 20.0 ms** | 3 → 0 |
| solari | 40 ms | `travel` | 5 frames @ 10.0 ms | **3 @ 20.0 ms** | 3 → 0 |
| solari | 40 ms | `spin` | 5 frames @ 10.0 ms | **3 @ 20.0 ms** | 3 → 1 |
| solari | 40 ms | `flip` | 5 frames @ 10.0 ms | **3 @ 20.0 ms** | 3 → 1 |
| industrial | 60 ms | `travel` | 5 frames @ 15.0 ms | **3 @ 30.0 ms** | 1 → 0 |

**EVERY POST FRAME IS A PRE FRAME, VERBATIM — the ceiling SELECTS from what the language already
drew, it never redraws at a coarser elaboration**, and the first and last frames are byte-identical
in all five. A trim that invented a frame would be the ceiling designing the motion.

**THE JUDGEMENT, PER MOVER, because a trim either costs a language its character or it does not.**

* **`solari.spin`, the riffle: 3 in-transit frames → 1. NOT A LOSS, and it is the one that looked
  like one.** At 10 ms/step the compositor drew **one** of the three and chose which by coalescing —
  the riffle a user saw was already a single frame picked at random. It is one DETERMINISTIC frame
  now. The claim "solari's in-transit frames ARE the flap board's riffle" survives intact: what made
  it solari's was the `SPIN` token, never the count.
* **`solari.flip`: 3 mid positions → 1. NOT A LOSS.** The knob passed 0.25 / 0.50 / 0.75 of the track
  in 40 ms; it passes 0.50 now, and that POST frame is PRE frame 2 verbatim.
* **`solari.press`: a 4-frame hold → 1. THE ONLY ONE WORTH ARGUING WITH, and the storyboard settles
  most of it** — PRE frames 1,2,3,4 are the **same render four times**, so nothing visual is lost.
  What is lost is the hold/release RATIO: 32:8 ms becomes 20:20. It flattens because at a 40 ms tempo
  the surface has exactly two draws to give, and **a hold/release ratio finer than 1:1 is not
  expressible in this medium at this tempo**. The alternative is a ratio that exists only in the spec.
* **`solari.travel` and `industrial.travel`: the in-transit sample → gone. A REAL CHANGE, and
  honest.** The mark hops well to well, which is what `MOTION_STEPS = 0` means for swiss — these two
  arrive there **by measurement rather than by declaration**. Every well is still passed.
* **What none of them lost:** the tempo. `MOTION_STEPS` is a choice about elaboration and the ceiling
  takes that choice back; `tempo` is the language's own and no ceiling reads it. **Solari still snaps
  in 40 ms, the shortest of the ten.**

**THE REALIZABILITY LAW SURVIVES, AND THE TEMPO IS A LAW NOW.** A transition is at least two frames,
so at least one gap, so **a tempo under the refresh period could not be drawn at ANY elaboration** —
the floor and realizability would contradict each other. The honest outcome there is not a
renunciation (a cut is not a transition) but **a TEMPO the language may not have**, and that is
asserted across the ten with a control. The shortest is solari's 40 ms, which affords two gaps.

**AND THE PASS CAUGHT ITS OWN FLOOR LAW BEING VACUOUS BEFORE THE BATTERY DID.** The first form read
`m.step_ms >= REFRESH_MS` — and `step_ms` is a `max(..., REFRESH_MS)`, so **the law was reading the
seat's own clamp and could not go red while the clamp was there**. It measures the RAW quotient now
(the frames actually built, divided into the language's own tempo, with nothing protecting the
answer), which is what M4 reddens five times. Same disease as pass 66's shape 1, found in this
pass's own new laws.

---

## #46 — THE HALF CELL'S TRACK DOT. THE GLYPH IS **COMPOSED**, AND THE RENDER GRID COULD NOT SEE IT

**THE CURE IS THE RULE APPLIED, SO THE LAW SPELLS THE DERIVATION AND NEVER THE ANSWER.** The
two-unlit verdict's rule is that a half-cell fill inks every ADDRESSABLE sub-column. The cured glyph
is not a nicer glyph, it is that rule:

```
full cell  ⣿  dots [1,2,3,4,5,6,7,8]   its LEFT sub-column  [1,2,3,7]
track      ⠒  dots [2,5]               its RIGHT sub-column [5]
                                       OR  =  ⡗  dots [1,2,3,5,7]
```

`⡇` is the same left sub-column with **nothing** in the right one — the one cell in the whole bar
whose unrun half drew nothing. A law that compared the half cell to a literal would be a spelling;
this one composes it out of the two glyphs the mechanism already has, and a **control** proves the
composition refuses the glyph that shipped for sixty-seven passes.

**THE TONE IS THE RUN'S, and that is a decision rather than an accident.** A cell is one glyph and
carries one tone, so **the sub-cell resolution the FILL has, the TONE does not**: whichever span the
half cell joins, one of its two sub-columns is painted in the other's colour. It joins the LIT run,
because the lit sub-column is the DATUM and the track dot is chrome — a fill that under-reads its own
quantity by half a cell to keep chrome the right colour has the priority backwards.

**THE CENSUS FOUND THREE FILL SITES, NOT ONE.** `_meter_braille`'s bar (the site the item names),
`Instrument._flow_card_rows`'s bench readout, and `Instrument.trace_row`'s scope trace — where the
DATAVIZ microbar floor means **a task due TODAY draws a half cell and nothing else**. Two of the
three now read the `Instrument.HALF` seat (the bench readout was re-spelling `⣿` and `⡇` while
already reading `self.LATT` — the #45 shape at one-third strength); the third is a **module-level
mechanism no language owns**, and the census is what stands over it. **M1 is that sentence as a
measurement**: revert only the mechanism site and the composition law stays GREEN while the census
reds.

**AND THE CENSUS RUNS THE OTHER WAY TOO — four `⡇` seats are NOT fills and keep the glyph**, each
read off the shipped seat rather than listed: a **knob** whose sub-column carries STATE
(left=DEFAULT, right=`⢸`=FOCUSED) and not a quantity; a **caret**, one cell with no track behind it;
a gantt **today-LINE**, the `│` every other language draws at GANTT[2]; and **naught's `FINE`** ramp,
where `⡇` is the TOP of four heights and a right-column dot would make the ramp non-monotone in ink.

**THE FINDING ON THE WAY, AND IT IS ABOUT THE INSTRUMENT: PASS 62's 428-STRING RENDER GRID IS
`cmp`-CLEAN ACROSS THIS CURE.** 308 + 120 strings, zero movers, against a change that moves **every
half cell in the language**. The reason is measured and printed: **none of the five instrument meter
fixtures produces an odd dot count** — every one draws whole cells, so the grid never drew the cell
#46 is about. Three passes in a row were `cmp`-clean and read as "nothing moved"; this pass is
`cmp`-clean and 10 of 54 hand-built specimens moved. **A grid that reports zero because it never drew
the cell is the same failure as a law that cannot go red** — pass 66's sentence, arriving at the
fixture set instead of at a detector.

---

## Mutation — FOUR ARMS AT FOUR DIFFERENT JOINTS, all caught, none crashed

`python -u prototypes/out/_p68_mut.py M1 M2 M3 M4 --restored`. Baseline and restored both **9922 / 0**.

| mutant | what it breaks | PASS | FAIL | verdict |
|---|---|---|---|---|
| **M1** the dot removed at the MECHANISM site (seat untouched) | 9920 | **2** | CAUGHT by the CENSUS; composition law held, as predicted |
| **M2** render reverted **and the identity NARROWED to fit** | 9919 | **3** | CAUGHT by the CONTROL + CENSUS while the narrowed law passed |
| **M3** the FLOOR removed, the ceiling kept | 9921 | **1** | the STRUCTURAL leg RED — the ceiling alone was not the cure |
| **M4** the CEILING removed (#36 re-opened) | 9907 | **10** | raw-step floor ×5, trim table, one-tempo, riffle, and pass 49's duration identity |

**M2 IS THE ARM THIS PASS OWES ITSELF.** It reverts the render *and* rewrites the composition law to
compare the half cell to the literal that shipped — exactly what a maintainer does to a red they do
not understand. **The composition law goes GREEN on purpose**, and the control and the census red
anyway. If they had not, this pass's two #46 laws would be one law with two spellings.

**M3 IS THE ARGUMENT FOR THE SECOND LEG.** With the ceiling in place every shipped fixture clears the
floor, so exactly one thing can red — travel past the ceiling's reach. It reds. Had it not, the
`max()` would be decoration and the item's own closed-form prescription would have been enough.

## Verification — `verify_language` 9812 → **9923** (+111)

THREE back-to-back full runs, all six suites. "checks" is the count of `[PASS]` lines.

**AND THE THREE ROUNDS WERE RUN AT 9922, NOT AT 9923 — SAID HERE RATHER THAN ROUNDED OFF.** After the
rounds finished, a last read of the tree found a **fifth** exempt `⡇` seat the #46 census had missed
(instrument's `stepper.step` EDITED arrow pair, `⡇⢸`, where the sub-column is DIRECTION). The fix was
the exemption plus **one new leg that closes the list against the source** — every `⡇` left in
`language.py` outside a comment must be one of the five claimed seats, so a sixth is a fill site this
pass never found. That is +1 check and one comment; the shipped tree runs **9923 / 0, ALL PASSED**,
verified by a single full run, and **the three-round evidence below is about a tree one law short of
it**. Re-running three rounds would have gone over this increment's run budget, and a count quietly
reported as if the rounds had produced it is worse than a disclosed gap.

| suite | checks | sixty-seventh | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9922** (9923 shipped — see above) | 9812 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 · 137 · 136 + 1 FAILED** — see below |

**ROUND 3's PYTEST WENT RED AND IT IS SAID OUT LOUD RATHER THAN RE-ROLLED.**
`tests/test_app.py::test_win_clipboard_roundtrip`, `AssertionError: assert None == 'roundtrip 123 ABC
taskboard'`, with the cause in the captured stderr: **`Set-Clipboard : Requested Clipboard operation
did not succeed`** — the OS clipboard was held by another process for the length of that call, so the
test's own SETUP never happened. **This is the pass-64 failure byte for byte**, it is #22's standing
watch, and this increment touches no clipboard path (the diff is a meter glyph, a motion ceiling, the
suite and this file). Rounds 1 and 2 passed it. **Recorded, not re-run until it agreed.**

**THE SETTLE WATCH MOVED BACK, AND THAT IS ALSO RECORDED.** Pass 67 saw two `settle timeout` lines in
four runs and filed the movement; **this pass saw ZERO across three `verify_language` runs and three
`verify_aperture` runs**, plus five more full suite runs inside the mutation battery. That is
consistent with pass 67's load hypothesis and it is **not proof of it** — and #22 stays open, because
the machine being quiet is not the same as the test being independent of it.

**Diff scope, every mover named.** `taskboard/language.py`: the `⡗` composition at three fill sites
(two of them now via the `HALF` seat), `REFRESH_MS`, `Motion.elaboration`, the ceiling and floor in
`motion_frames`, `import copy as _copy`. **No builder signature moved.**
`prototypes/verify_language.py`: three frame-count laws re-pointed from the declared token to
`elaboration`, the riffle character law rewritten, the #46 identity law rewritten as a composition
plus a control and a two-way census, the #36 block (floor, ceiling maximality, tempo law, trim table,
structural leg) and three controls. **Render movers: exactly the 10 specimen lines in
`_p68_prove.py` §2 and the 5 storyboards in §4 — no other cell in the corpus moved**, and the 428-
string grid says so while being unable to see the first five.

**THREE OF THIS PASS'S OWN INSTRUMENTS WERE WRONG FIRST, AND ALL THREE ARE RECORDED RATHER THAN
QUIETLY FIXED.** (1) The `_steps` source law pinned the NUMBER of occurrences, got it wrong, and
would have reddened on a comment; it states SCOPE now (the one function, and no other app file).
(2) The prover's braille dot-number helper permuted the bit order and printed `⠒` as dots 2+4 instead
of 2+5 — **the two-unlit verdict's own glyph, misread by the prover written to explain it.** (3) The
#46 exemption census listed FOUR seats and there are FIVE; it was a hand-built list with no closure
against the source, which is the same shape as pass 66's detector reporting zero because it did not
look. It is closed against the source now. **None of the three changed a render; all three would have
gone into the record as evidence.**

**THE RECOMMENDATION FOR THE SIXTY-NINTH PASS: #3, THE RUNNABLE EXEMPLAR — and it is the answer now
rather than the alternative.** Every argument that has deferred it for six passes is spent. It was
"an exemplar of a suite containing an unknown number of laws that cannot fail" (pass 65) — the oracle
sweep censused that class and passes 66/67 cured it. It was "build it FROM the component track's
output" (pass 59) — that track closed, then the motion axis closed, and today the last two items that
move shipped cells closed with it. **The skill demands "render, don't label" of everyone but itself
and has thirteen documents of vocabulary with zero reference implementation.**

**WHAT IT NEEDS, stated so the pass can be scoped rather than discovered:**

1. **It must show a language changing STRUCTURE, not tone** — item 0's bar, and the one thing that
   makes it an exemplar rather than a palette demo. The measurable is available: the greyscale diff
   between two languages' exemplar renders must exceed what a tone-only swap could produce.
2. **Every glyph must come from a kit seat.** Pass 49 deleted eight hand-authored `flip_frames`
   because a picture goes stale the day the thing it pictures moves; an exemplar is that failure at
   full size. It composes through `Kit`, or it is a fourteenth document.
3. **It needs a home in a DIFFERENT repo** (`~/.claude/skills/tui-design/assets/exemplar.py`), so the
   five-file budget has to span two trees — which no pass in this series has done, and which should
   be decided before the increment rather than during it.
4. **It needs a law, and the skill has never had one.** An artifact nothing verifies is the exact
   shape this file spends every pass refusing. The cheapest honest form: a `verify_exemplar` that
   asserts (2) by source census and (1) by measurement, run from this repo against that file.

**THE SECOND CANDIDATE: #22, with the STALE PAINT line as the lead.** Unchanged from pass 67's
recommendation and now with one more data point — **zero timeouts in eleven suite runs on a quiet
machine**, against two in four on a loaded one. That is the strongest evidence yet that the watch is
about load rather than about seat reassignment, and it is still not proof.

**WHAT THIS PASS DID NOT DO, NAMED.** The `⡗` half cell is **not** verified against a real terminal —
its width and its rendering are asserted from Unicode properties and from the corpus's existing
braille usage, exactly as every braille glyph in this language has been since pass 61. And the
refresh floor is pinned at 60 fps because that is Textual's default cadence; **a terminal running at
30 fps would need twice the floor and this pass has no instrument that can measure the real one.**

---

# CLOSING STATE — 2026-07-28, sixty-seventh pass. **THE TWO MUTANTS THAT DIED IN PASS 66's CURED TREE NOW RUN TO THE VERDICT LINE AND REPORT 8 AND 19 REDS. THAT IS THE WHOLE POINT OF THE PASS, AND IT IS A MEASUREMENT, NOT A DESCRIPTION.**

> Updated by the sixty-seventh pass (**#47 and #48 CLOSED**; nothing added). The sixty-sixth pass's
> closing block follows unchanged below; its table's stamps are current except where this block
> supersedes them.

**THE ACCEPTANCE TEST, RUN WITH PASS 66's OWN BATTERY AND ITS OWN ANCHORS.** `python -u
prototypes/out/_p66_mut.py M2a M3a`, unmodified:

| arm | pass 66 (cured tree) | pass 67 (cured tree) |
|---|---|---|
| **M2a** instrument axis ORIGIN never drawn | 9216 PASS, **3** FAIL, **NO verdict line** | 9804 PASS, **8** FAIL, **verdict YES**, CAUGHT |
| **M3a** blueprint span field code renamed | 8598 PASS, **3** FAIL, **NO verdict line** | 9793 PASS, **19** FAIL, **verdict YES**, CAUGHT |

Both reached three reds before and then lost every remaining check. **The reds a dead run does not
print are not missing reds, they are the rest of the file unspoken** — and the difference between 3
and 19 is what that sentence costs.

**PASS 66's CENSUS WAS NOT THE CLASS, IT WAS THE PART ITS DETECTOR COULD SEE — AND BOTH MUTANTS DIED
OUTSIDE IT.** #47 was filed as "45 constructs at 23 sites" with M2a and M3a as its evidence. Neither
death site was in those 45:

* **M2a died at `ax_cols = sorted(... enumerate(ib[iax[0]]) ...)`** — a `[0]` in an ASSIGNMENT. Pass
  66 widened its setup scan's SCOPE to every node outside a law and left its SHAPE list at the named
  trap, so a bare `[0]` in a setup line was invisible. **And the comfort that hid it is the finding:
  three lines above sits `check(len(iax) == 1, ...)`. A `check` REPORTS and the run CONTINUES — that
  is what it is for — so a check above a setup line is not a guard.** Eleven sites sat behind exactly
  that comfort.
* **M3a died at `bp_span(1).split(BP.CLOSE)[1]`.** Pass 66 excluded `split` from the census
  WHOLESALE, with a correct argument for index 0 (`"".split(",")` is `[""]`) and **no argument at all
  for index 1**, which asserts the SEPARATOR IS PRESENT — precisely what the mutant removes.

**AND 21 OF THE 45 WERE THE DETECTOR FAILING TO READ THE FILE.** `guarded()` answered one question
(`in` tests, for `.index`) and the suite's authors write three others — `len(x) == 1 and x[0]`,
`bool(x) and x[0]`, `x[0] if x else ...`, `if not x: return`. Those are Python's short-circuit
semantics, not a heuristic, and a census that flags them is not finding a defect. **Net: the class is
33 constructs at 24 sites, smaller in count because 21 false positives went, LARGER in reach because
it now covers the two shapes the mutants actually died on. A census that shrinks and finds more is
the measurement, not the number.**

**#47 CLOSED. 31 CURED, 2 EXEMPTED, AND THE EXEMPTIONS ARE CHECKED IN BOTH DIRECTIONS.** The cure is
a third seat beside `at()` and `first_of()`:

```python
def nth(seq, i, default):        # `default` POSITIONAL AND REQUIRED
    return seq[i] if -len(seq) <= i < len(seq) else default
```

`default` has no fallback **on purpose**: `at()` had one right answer for 52 sites (-1) and `[0]` has
none, so no site may inherit another's sentinel by accident. The 15-row sentinel table is
`_p67_prove.py` §1; the two sentinels **rejected by measurement** are the argument:

* **`""` for the instrument bar's unlit was written first and would have MOVED the crash** —
  `mink("")` calls `ord("")` and raises `TypeError`. A sentinel must be TOTAL for every function its
  site hands it to. `" "` is total, is not a braille glyph (so both identity laws red) and inks 0.0
  (so the ceiling law reds).
* **One shared extent sentinel for solari's seam and band makes `band_ex == seam_ex` TRUE**, so all
  three extent laws PASS on a board with no grid at all — the `-1 == -1` trap pass 66 named for
  `at()`, wearing other clothes. They are `(-1,-1)` and `(-2,-2)`.

**A SEAT IS NOT A LAW, AND ONE SITE PROVES IT.** Blueprint's registration corners carry a NEGATIVE
claim — "the cells between the corners are blank" — and **an empty slice SATISFIES it**. No sentinel
can red that law; any value that keeps the run alive hands it an empty span and it passes vacuously
on the exact input it exists to refuse. That site (and instrument's `all(... for c in ax_cols)`,
which `all([])` made pass) carries an explicit non-emptiness LEG as well as the seat. **Mutant N3b is
that sentence as a number: same app mutation, leg removed, seat kept — the box law goes GREEN (BOX
red ×4 → ×0).**

**#48 IS WRONG AT THE ADDRESS IT NAMES, AND RIGHT ABOUT THE SHAPE.** The item says `mrows` can be
empty. Measured off the tree: `mrows` is `[kn.master_row(...) for i, (t, c) in enumerate(<3-tuple>)]`
— **no `if`, a literal three-element iterable, exactly 3 items on every input.** `range(len(mrows))`
is never empty and `isolated(mrows, 1)` goes TRUE the moment rows 0 and 2 come back blank. The law
can fire. **The one-line leg the item prescribed (`len(mrows) >= 2 and ...`) would itself have been a
leg that CANNOT FIRE — shape 5, added in the name of curing shape 5. It was written, measured and
reverted.** The shape IS real and the suite has it at **L10069**, one of the two neighbours #48 named
in passing and did not examine: `RAIL not in "\n".join(body_rows(boards[name]))` passes for a
language whose board rendered NOTHING, and eight of the nine languages are anchored by nothing.
Cured with `bool(_brows)`, a leg that can fire. **Fifth item in a row whose number was a claim.**

**THE PROVER WENT RED ON ITSELF AND IT IS RECORDED RATHER THAN QUIETLY FIXED.** `_p67_prove.py` §5
asks whether `ib[iax[0]]` still appears in the suite. First run: yes — **inside the comment the cure
writes explaining what M2a died on.** A source law answered by prose is the sweep's own shape 4,
negative form, committed by the prover written to certify a shape-3 cure. It now strips comments
through the sweep's own `code_only`, one definition, not a copy. **The marker scan had the same
disease in the same hour**: `# nth-exempt:` was a bare substring test and counted two comment lines
ABOUT the mechanism as two exemption claims; it is anchored to the start of a comment now.

**ZERO renders moved, and again it is a consequence rather than a hope: `taskboard/` was READ-ONLY.**
308 + 120 grid strings, `cmp`-clean against pass 66's POST. **9810 → 9812 (+2), and the +2 are the
two new standing laws about the suite itself; the other five suites did not move by one check.**

**FOUR MUTANTS OF THIS PASS'S OWN, each at a different joint of the cure** (`_p67_mut.py`):

| mutant | what it attacks | PASS | FAIL | verdict |
|---|---|---|---|---|
| **N1** M2a's app mutation + `iaxrow` reverted to `ib[iax[0]]` | was the cure load-bearing? | 9214 | 2 | **DEAD RUN** (`IndexError` L10588) — as predicted |
| **N2** a `# nth-exempt:` claim planted where nothing is flagged | is the exemption list measured? | 9811 | **1** | CAUGHT by the claimed-AND-used law, and by nothing else |
| **N3a** blueprint draws no registration corners | does the cured tree report in full? | 9796 | 16 | BRACKET red ×4, **BOX red ×4**, verdict reached |
| **N3b** ... with the `len(xs) == 2` leg removed, seat kept | is the LEG load-bearing? | 9800 | 12 | **BOX red ×0 — the law went GREEN** |

**N1 AND N3b ARE THE PASS'S TWO PRE ARMS AND THEY PROVE DIFFERENT THINGS.** N1 shows the seat was
needed (without it, a crash and 590 checks unspoken). **N3b shows the seat was not ENOUGH** — with
`nth` in place and only the leg gone, nothing raises, the run finishes, and a law about a title block
with no corners reports PASS. A cure that turns a crash into a silent green has moved the defect.

**THE BASELINE OF THIS PASS IS CONTAMINATED AND IS NOT USED AS EVIDENCE.** The first suite run was
launched while the sweep's `raise_trap()` was mid-edit, so it reported 9809 PASS / 1 FAIL against a
detector that existed for ninety seconds. Pass 66's recorded 9810 / ALL PASSED is the PRE figure, and
the three closing rounds below are the POST. Said out loud rather than re-rolled until it agreed.

**Suites at closure.** THREE back-to-back full runs at the sixty-seventh pass. "checks" is the count
of `[PASS]` lines.

| suite | checks | sixty-sixth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9812** | 9810 | **9812 · 9812 · 9812** — see the settle note below |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 · 137 · 137** |

**TWO OF THE THREE ROUNDS CARRIED A `settle timeout`, AND IT IS SAID OUT LOUD RATHER THAN RE-ROLLED
UNTIL IT AGREED.** Every round passed all **9812** laws. Rounds 1 and 2 each emitted ONE additional
FAIL from the capture gate — `capture settle timeout: board never painted`, at **two DIFFERENT
captures** (`seats instrument @118` in round 1, `instrument @118x30` in round 2), both with the same
cause line: `kb-card@91,20 STALE PAINT (composed at a seat it no longer has; seat is now 19)`. Round
3 was ALL PASSED, and a FOURTH run made alone with nothing else on the machine was ALL PASSED,
**9812 / 0**.

**WHAT IS AND IS NOT CLAIMED ABOUT IT.** This is **#22's watch** and the pass-46 pattern working as
designed — a named FAIL the run continues past, which is why all 9812 laws still reported in both
rounds. The three rounds were run back-to-back in a loop while other work was on the machine, and
the isolated run was clean; that is consistent with load, and it is **not proof of it**. What can be
said without guessing: **this pass's diff touches no capture, no `settle()`, and no app code at
all** — it is law expressions, setup assignments, the `nth` seat and the sweep's detector, and
`taskboard/` was read-only. **Pass 66 saw zero settle timeouts in eight runs; this pass saw two in
four. That is a movement in the watch and it is recorded as one, not explained away.**

**#47 and #48 are CLOSED. Nothing was added to the register this pass**, and the settle movement
above is deliberately NOT filed as a new item — **#22 already owns that watch** and a second number
for the same phenomenon is how a register stops meaning anything.

**THE RECOMMENDATION FOR THE SIXTY-EIGHTH PASS: #46, the half cell's missing track dot.** It is the
only open item whose fix is a RENDER change, and passes 65, 66 and 67 have every one been
`cmp`-clean on 428 strings. Three passes in a row without moving a cell is a suite growing away from
the thing it measures — and #46 is a defect the sixty-fifth pass's own two-unlit verdict already
declares (`⡇` leaves an ADDRESSABLE sub-column with no track dot; the mark that carries it is `⡗`).

**THE SECOND CANDIDATE, IF THE SETTLE MOVEMENT REPEATS: #22, and this time with the STALE PAINT line
as the lead rather than the clipboard.** Both of this pass's timeouts named the same cause —
`kb-card@91,20 composed at a seat it no longer has; seat is now 19` — which is a statement about
seat reassignment during compose, not about a slow machine, and no pass has yet read it as one.

**WHAT THIS PASS DID NOT DO, NAMED.** The `nth` census is STATIC: it proves no construct can raise on
an empty sequence, not that every law goes red on one. Only the sentinel table (§1, read by hand) and
the four mutants say that, and they cover 4 of the 24 sites. **Shape 5 is still sampled, never swept**
— and #48 is now the second sample finding in two passes that a tree-read overturned, which is worth
knowing about the instrument: a sample reports a hypothesis, not a defect.

---

# CLOSING STATE — 2026-07-28, sixty-sixth pass. **THE SUITE NOW HAS A LAW ABOUT ITSELF. 52 CONSTRUCTS AT 34 SITES COULD RAISE WHERE THEY SHOULD HAVE GONE RED — AND A RAISED LAW REPORTS NOTHING, SO EACH ONE WAS NOT A MISSING RED BUT THE REST OF THE FILE UNSPOKEN. ALL 52 ARE CURED AND A STANDING LAW HOLDS THEM AT ZERO.**

> Updated by the sixty-sixth pass (**the ORACLE SWEEP**; **#47** and **#48** added; nothing closed —
> this pass cured a class the item register had never named). The forty-seventh pass's grooming
> block follows unchanged below the table; the table's stamps are current as of the sixty-sixth.

**THE SWEEP FOUND ITS OWN BLIND SPOT AND A MUTANT IS WHAT FOUND IT.** The first census read `check()`
arguments and assignment statements: 48 constructs at 31 sites. Mutant M3a then died — in the CURED
tree, at 8598 checks, having reported three reds and no verdict line — on `def bp_len(s): return
s.index(BP.CLOSE) - ...`, a `.index` in a helper's RETURN, which the census had never looked at. The
scan is now every node in the file that is not already inside a `check()` argument, which is total by
construction, and it found four more at three sites. **A detector that reports zero because it did
not look is the same failure as a law that cannot go red.**

**THE PROOF IS TWO-ARMED AND ARM B IS THE FINDING.** M1b takes the same mutant as M1a and reverts ONE
law to the `.index()` form the sweep replaced: **8242 PASS, 0 FAIL, no verdict line — a DEAD RUN.**
Arm A on the cured tree: **11 reds.** Same defect, same tree, and before this pass the suite could
not say a word about it. M3b is the trap's other half (`StopIteration`, not `ValueError`) and dies
the same way.

**AND THE FIRST DRAFT OF ARM B PROVED NOTHING, WHICH IS RECORDED RATHER THAN QUIETLY REPLACED.** It
reverted the APP-LEVEL masthead law, whose pre-sweep form already carried a `bool(mh)` guard — and
M1 EMPTIES `mh` rather than corrupting it, so the guard short-circuited and the run stayed alive. A
revert that cannot raise is not a PRE arm, it is a second copy of arm A.

**SHAPES 1, 2 AND 6 CAME BACK EMPTY AND THE SWEEP SAYS SO WITH ITS COVERAGE, NOT WITH A SHRUG.** Zero
re-typed formulas (shape 2) — with a PLANTED alpha-renamed copy of `coverage_index`'s clamp proving
the detector can fire, because a detector reporting zero and a clean suite read identically. Zero
subject-free laws (shape 6). Twenty `==` comparisons whose oracle calls the seat (shape 1), all
hand-read and all legitimate difference or clamp laws — **but the sweep saw only 56.2 % of sites for
that shape, and it prints the fraction.**

**SHAPE 5 IS NOT SWEPT AND THIS INSTRUMENT REFUSES TO PRETEND OTHERWISE.** Deciding whether a
predicate can take the other value is not decidable from the tree. It is SAMPLED instead: N=24 drawn
with `Random(66)` from the 879 sites in the 48 pre-discipline sections, hand-audited one by one.
**One of twenty-four has no anchor** — `not any(isolated(mrows, i) for i in range(len(mrows)))` is
TRUE on an empty `mrows` and nothing asserts it is not — filed as **#48**.

**ZERO renders moved and it is a consequence rather than a hope: `taskboard/` was READ-ONLY this
pass.** 308 + 120 grid strings, `cmp`-clean against pass 65's POST, measured anyway. **9807 → 9810
(+3), and the +3 are the suite's law about itself; the other five suites did not move by one
check.** Seven mutants, five caught, two blocked by the filed remainder — which is the measurement
that makes **#47** real rather than described.

**THE HEADLINE OF THIS PASS: two byte-identical mutants (M1, M5) restore the exact bypasses this
pass cured, and BOTH are caught by ZERO pre-existing laws.** A signature compare, a snapshot, a
greyscale sweep and every pairwise law pass on either of them. That is what "the last two seats were
ungoverned" means as a measurement rather than as a description — and it is the argument for doing a
pass whose whole render diff is `cmp`-clean on 428 strings.

**#40d's ITEM DESCRIPTION WAS WRONG IN THE SAME DIRECTION AS THE THREE BEFORE IT.** It reads as
"`plot`'s per-row branches decide levels through neither quantiser". Measured: **not one of the
twelve decides a level.** The level is decided once per column, above the branches, by a re-typed
copy of `coverage_index` in three places — which made DATAVIZ law 3's own appointing sentence FALSE
for `plot` ("one copy means spending the floor reds this law in every language at once"; each copy
carried its own `max(1, ...)`). **Fourth item in a row whose number was a claim: #40's four
air-printing branches were one, #39's two band seats were three, #43's four collisions were one,
#40d's ad-hoc branches are zero.**

**THE TWO-UNLIT VERDICT IS DECLARED AND THE ARGUMENT IS AN IDENTITY.** `_meter_braille`'s bar row
draws `⠒` where its flow row draws `⠐` — one mechanism, two unlits, the #45 disease's exact shape.
It is not the disease: the bar is a HALF-CELL fill addressing two sub-columns per cell and the flow
row is undivided, so the bar's unlit **is** the flow row's unlit mirrored into the other sub-column
(dot 5 | dot 2 == dots 2+5), asserted with a control. **The argument produced a defect it does not
cure** — the half cell `⡇` carries no track dot in its own unrun sub-column — filed as **#46**.

**TWO OF THIS PASS'S OWN EDITS REDDENED STANDING LAWS AND BOTH WERE FIXED AT THE SOURCE**: a comment
spelling `⠐` inside the meter, and prose spelling `COVER_RAMPS[...]`. Teaching the laws to ignore
comments was the alternative, and it is exactly the move M4 exists to catch.

**ZERO renders moved (308 + 120 strings, `cmp`-clean vs pass 64's POST). 9725 → 9807 (+82); the
other five suites did not move by one check.** Six mutants, all caught, none crashed. **pytest 137 ×
3 with no flake — and #22 stays open**, because the machine being quiet is not the same as the test
being independent of it.

**THE HEADLINE OF THIS PASS: item #43 named four tone collisions on the meter's flow row, and the
instrument it cites has never reported more than ONE.** Pass 62's `collisions` drops letters and
figures on DATAVIZ law 5's authority — correct on the BAR row, blind on a row whose LEVEL MARKS are
themselves letters — so the other three exist only under an alnum-inclusive reading the item
described and never ran. Both readings are now asserted per mechanism, because which one is right IS
the question. **Third item in a row whose own number was a claim: #40's four air-printing branches
were one, #39's two band seats were three.**

**THE PER-MECHANISM ARGUMENT, ONE SENTENCE, FOUR APPLICATIONS.** A tone collision on a flow row is a
DECLARED IDIOM when both sides state the same datum (a FIGURE — law 5) or when one side is CHROME
that delimits rather than measures; it is a DEFECT when a LEVEL MARK collides with something that is
not a level. **`dimension` defends** (`├┤` bound every span in both tones; the quantity is the LENGTH
plus the figure on it), **`lcd` defends** (all digits, walled by brackets), **`odometer` defends**
(the solari precedent — the digits ARE the datum), **`step` is cured.**

**`_meter_step` DREW ITS LEVELS AS `. o O` IN A ROW CAPTIONED `flow`, so colour-stripped it carried
FIVE ramp marks for FOUR buckets** — a phantom datum, `gradient`'s phantom shoulder wearing letters.
**The collision was the symptom; the disease was a PRIVATE ALPHABET.** `. o O` is darkside's MOTION
family (`SPIN`, the `PHASES` doodle) while the registry already names `▁▂▄█` as this language's
coverage ramp, drawn by its own `spark`. The row now reads that row's `[0] [2] [3]`, its unlit is the
mark the bar one row above draws for an unrun cell (**pass 61's rule verbatim**), and **no level is a
letter, so no caption this row could ever carry can collide with its data.**

**THE CHEAP CURE WAS TRIED FIRST AND A STANDING LAW KILLED IT.** `o` → `◦` moved ONE level and was a
three-string diff — but `◦` is `NA.OFF`, naught's own unlit pixel, and a law forbids any other
language's board from drawing naught's lattice marks. **Narrowing that law to admit the cure is
exactly the move pass 62's M3 mutant exists to catch, one level up.** The law stood, the cure moved,
and hunting for a mark that was darkside's and nobody else's is what found the registry row.

**THE BATTERY FOUND THREE LAWS THAT COULD NOT REPORT THEIR OWN FAILURE.** Three mutants CRASHED the
suite before being caught — pass 63's seat readers raised on a moved seat, its preimage law raised on
an unreachable level 0, and this pass's own named laws raised on a collapsed ramp. **M1 took the run
down at 7591 checks with one red printed; after the fix it prints 23.** A run that dies reports no
reds at all, which is indistinguishable from a mutant nothing catches.

**#44 CLOSED AND ZERO RENDERS MOVED FOR IT.** `_meter_braille` names the registry's two ends; the
pass-63 VALUE law is kept unchanged as the stronger guard, and M3 proves the split — reverting the
naming reds four laws and **not one of them is the value law**, because the two still agree.

**12 renders moved, every one named** (4 of 308 on the language grid, 8 of 120 on the mechanism
grid — all `darkside`/`step`). **9650 → 9725 (+75); the other five suites did not move by one
check.** Six mutants, all caught, none crashed.

**THE HEADLINE OF THIS PASS: pass 60 exempted the band-threshold quantisers from the coverage
primitive on RENDER-RISK grounds — "routing would move cells" — and nobody ever asked whether the
mechanism as shipped obeys the LAWS.** That is the whole anatomy of grandfathering: an exemption
defended by the cost of curing it rather than by the conduct of the thing exempted. **Held to the
four laws and the two ceilings without routing it, the family passes 39 of 39 parity legs** — every
leg `cover[...]` asks of a ROUTED ramp, asked of the un-routed seats — so #39 closes as COMPLIANT BY
MEASUREMENT and the routing rejection stands on its own merits instead of on inertia.

**THE ITEM'S OWN CENSUS OF THE FAMILY WAS SHORT BY ONE SEAT.** #39 named `naught.dot_heat` and
`_meter_braille`'s flow row. A grep for the band constants finds **three**: `_meter_step`'s flow row
(`. o O`, darkside) is the same 3-level band quantiser. **Pass 62 saw that ROW — it is in item #43 —
and did not recognise the QUANTISER.** Same shape as pass 62's finding that #40's own measurement was
wrong: an item's description is a claim, not a census, so the census now counts the SOURCE.

**SEAT C COULD NOT HAVE BEEN AUDITED WITHOUT OPENING THE INK INSTRUMENT, and that is why it went
unnoticed.** `mink` returns 1.0 for any letter, because a printed FIGURE is a full cell of stated
value — so `.`, `o` and `O` all weighed exactly the same and **no ink law in this suite could order
them**. Three declarations, argued on the existing table's own logic, are what make C measurable at
all; a seat whose glyphs the instrument cannot weigh is a seat no law was ever really applying to.

**THE MUTATION BATTERY CAUGHT A LAW OF THIS PASS'S OWN BEING VACUOUS, and it was the central one.**
M1 inverts a band inside `naught.py` and **MONOTONE stayed GREEN** — because the first draft swept a
RE-TYPED copy of the arithmetic living in the suite, which a mutation to the code cannot reach. Every
per-seat law now reads the level OFF THE RENDERED STRING; the model survives as exactly one law (the
equality). M1 went from 3 reds to 6, and MONOTONE is now among them.

**M6 IS THE PROOF THAT THE NEW LAW IS LOAD-BEARING: 9649 PASS, 1 FAIL, and the one is the new law.**
It moves `fine`'s ink TIE from the (unlit, first-lit) pair to a pair of two DATA levels — distinct
glyphs, equal ink, indistinguishable in greyscale. **Every pre-existing law stays green**, because
the registry's monotone law is `a <= b`, its repeat census counts GLYPHS, and its law-4 legs only
look at index 0. What the exemption rests on is now pinned in the only place that could see it.

**THE DISAGREEMENT IS A DIFFERENCE, NOT A VIOLATION, and the record now says so with numbers.** The
bands and nearest-index disagree on **34.3%** of the domain at seat A and **9.0%** at B and C (pinned
as exact counts, red in both directions). Two quantisers that are each monotone, deterministic,
threshold-honouring and greyscale-separable may put their level changes in different places: the laws
constrain the SHAPE of a quantiser, they do not appoint one band layout.

**ZERO RENDERS MOVED, AND THAT IS THE VERDICT RATHER THAN A SIDE EFFECT.** The render signature is
**byte-identical** to pass 62's POST — no source file was opened, because none needed curing. **+69
checks on `verify_language` (9581 → 9650); the other five suites did not move by one check.** Six
mutants, all caught, none crashed.

**THE HEADLINE OF THIS PASS: corgi's shipped meter drew `▄▄ ` for its lit segment and `▄▄ ` for its
ghost, so `'▄▄ ' * n + '▄▄ ' * (segs - n)` was `'▄▄ ' * segs` at EVERY value.** Colour-stripped, the
bar at 0%, 38% and 100% was the same string three times; only the figure in the brackets moved.
**That is DATAVIZ law 1's named case in its most complete possible form — not a weak reading, no
reading — and pass 61's ramp laws could not see it because the meters do not route.** Cured: the
ghost is `░░`, the pair NAMED from `COVER_RAMPS["lcd"]`, which is what `plot`'s lcd branch had been
drawing correctly the whole time.

**THE CENSUS CAME FIRST AND IT FOUND A DEFECT NOBODY PREDICTED.** Four instruments (two per law)
over all twelve mechanisms: `lcd` red on both law-1 legs, `gradient` red on law 4 with a **3-of-34**
track — and **`_meter_decay`**, which nothing had flagged, red because its four-cell persistence
tail reached `░`, the track's own glyph in a brighter tone, putting a HOLE in the run in greyscale.
**12 of 12 clean after.**

**THE FIGURE HAD TO COME OUT OF THE INSTRUMENT BEFORE THE INSTRUMENT MEANT ANYTHING.** A right
aligned `{pct:>3}%` is `'  0'` at zero and `'100'` at full, so the first draft of the track law
reported **all twelve mechanisms red**. An instrument that reds everything is not strict, it is
broken.

**#40 WAS TAKEN, AND THE ITEM'S OWN MEASUREMENT WAS WRONG.** It claimed four `plot` branches print
air for a zero column; measured across all twelve, it was **one** — `boxed`, `dotgrid` and `decay`
draw their unlit lattice down the WHOLE column, and only `blocks` (nord's) drew nothing at all.

**THE EVIDENCE NOBODY LIKES: the five cures were run against the 9496-check suite BEFORE the new
laws were written, and it passed 9496/0.** Six shipped strings changed — including corgi's entire
visible bar at every value below 100% — and not one existing law noticed. The +85 checks are what
closes that hole.

**THREE OF THE NEW LAWS WENT RED ON CORRECT CODE and all three were the law being wrong** — one read
a glyph out of the method's own COMMENT, one asserted a single monotone sweep across a row whose
track follows its head, and one was defeated by the comment in `language.py` that documented it.
Same lesson as pass 61's two, three times.

**THE HEADLINE OF THIS PASS: pass 60 wrote "the law says track" in a comment directly above ten
ramps that drew no track.** Nine of the ten had a SPACE at index 0 — or braille's U+2800 BLANK,
which is a real codepoint with zero ink and the same defect wearing a glyph's clothes — so a
flat-zero series rendered as nothing at all (DATAVIZ law 4), and corgi's `lcd` was `' ▄▄█'`, two of
whose four levels were one glyph separated only by TONE (law 1, the case the skill cites BY NAME).
**Both cured, at the ONE registry seat, with a per-language argument each: the unlit glyph is the
mark the language ALREADY DRAWS for an empty position on its own meter, and where that mark already
occupies a lit level the ramp's own family supplies the step above it.**

**THE SECOND CEILING IS THE HALF THAT WILL BE TESTED.** Making index 0 visible invites the opposite
defect at once — a track heavy enough to be mistaken for a small value — so the unlit also carries
**at most a quarter of the cell**. M5 spends exactly that (a `▒` track, still monotone, still four
distinct glyphs, still inked) and **one check in 9496 goes red.**

**THE MOVING PIXELS WERE THE INCREMENT, SO THEY WERE MEASURED: 76 of 308 fixture renders moved, 232
held, and `plot` moved ZERO cells in every language** — its only routed seat is a partial top cell
that can never ask for index 0. **The four other suites did not move by one check**, which is the
second half of the diff-scope evidence.

**TWO LAWS OF PASS 60 WENT RED ON CORRECT CODE AND BOTH WERE THE LAW BEING WRONG.** The anti-dither
grep read a 4000-CHARACTER WINDOW above `coverage_index`, so a law about dithering went red because
somebody wrote a paragraph about ramps — restated as a named block. And "each ramp literal appears
once" caught a REAL fork the moment the cure created one: `phosphor` became `'░▒▓█'`, which is also
the literal `_meter_decay` slices for its persistence tail. The meter now names the registry row;
the tail is that ramp indexed by DISTANCE, not coverage, and the comment says so.

**THE CENSUSES ARE NOW THE CURE RATHER THAN THE DEFECT, and one of them locates instead of
counting.** `REPEAT_AT` pins the exact index pair `hairline` is allowed to repeat at, so an edit
that repeats a different pair cannot pass a census it still satisfies numerically. **M3 attacks the
LAWS rather than the code** — the exemption list widened by hand, `language.py` untouched, the way
a maintainer makes a red go away — and five checks fire, three of them because the exemption is
claimed and unused.

**AND THE PASS FOUND THE SAME TWO DEFECTS ALIVE AT THE MECHANISM NEXT DOOR — new item #41.**
`_meter_lcd` draws its lit and ghost segments with the SAME glyph in two tones, and
`_meter_gradient`'s unrun track is literal spaces. The meters do not route, so no ramp law can see
them. **That is the next increment.**

**THE HEADLINE OF THIS PASS: the ten languages each picked their data-viz glyphs from a ramp literal
written INSIDE the drawing method, so "what does 40% coverage look like here" was answered in nine
places and could drift in nine places.** What lands is **one function, one registry, and a routing
table that says out loud which mechanisms are NOT coverage-shaped**. Coverage anti-aliasing on a
pixel display is a BLEND; a cell has no blend, it has a glyph — so coverage stops being an alpha and
becomes an **INDEX into an ordered ramp**, with both ends NAMED rather than interpolated.

**AND THE ONE PLACE THE DESIGN DISAGREES WITH ITS OWN SOURCE RESEARCH IS THE INTERESTING PLACE.**
Coverage AA is free to drop faint ink below a low threshold — that is what the threshold is FOR.
DATAVIZ law 3 forbids it for DATA: "we have 1 overdue" may not render as "we have none". The skill
wins on conflict, so **`lo` defaults to 0.0 and the only coverage that earns blank is exactly
zero**; the `lo` seat stays open for STRUCTURE, which carries no such law. **M6 spends the floor
(`lo = 1/32`) and reds the PRE-EXISTING microbar law in all ten languages** — which is the proof
that the primitive is now the seat those older laws stand on.

**THE ANTI-DITHER RULING IS THE HALF THAT WILL ACTUALLY BE TESTED, so it is a grep law.** Error
diffusion is the obvious next move from coverage AA and it is refused, in the docstring, for two
reasons about this repo rather than about taste: a position-dependent glyph makes every
byte-identity law in `verify_language` unwritable, and a static surface that re-renders on a tick
would CHURN. **M5 deletes the sentence and the suite goes red.**

**THE SWEEP IS RENDER-NEUTRAL AND THAT WAS MEASURED, NOT ASSERTED: 258 rendered strings, PRE against
POST, ZERO divergences.** No cure was needed and none is claimed.

**THE MUTATION BATTERY IMPROVED A LAW OF THIS PASS'S OWN.** M3 (a mechanism reverting to its inline
ramp, render byte-identical) was caught by only ONE check, because the "each ramp literal appears
once" law counted `"..."` and the mutant's literal was `'...'` inside a double-quoted f-string. **A
source law that a quote character can walk around is not a source law.** Hardened to count both
styles, plus a new per-language law that the glyphs ON THE GLASS are the primitive's own return
values — 9443 → 9452, and M3 went from 1 red to 2.

**THREE DEFECTS WERE MEASURED AND DELIBERATELY NOT CURED — #37, #38, #39 — each pinned by a CENSUS
law that goes red in BOTH directions** (red if the defect spreads, red if somebody cures it without
saying so). The sharpest is **#38: corgi's `lcd` ramp is `' ▄▄█'`, so two of its four levels are the
same glyph separated only by TONE — which is the exact case `DATAVIZ.md` law 1 cites by name, still
live.** Curing any of the three is a RENDER change, and this increment's mandate was byte-identity.

**THE HEADLINE OF THIS PASS: the component family's four tempo debts were one question asked four
times, and what pays them is not four animations.** It is **one engine, five events, two disjoint
regimes** — `transition` ≤400 ms, `ambient` ≥2000 ms, the 400-2000 ms dead zone refused rather than
rounded — with the regime derived from the EVENT, the duration from the regime and the language's
`tempo`, and the per-language character carried by one renamed token (`FLIP_STEPS` → `MOTION_STEPS`,
because it governs five events now). **Every frame is a render composed by the seats this contract
already had**, which is pass 49's "no pictures" ruling turned into a source law. **Colour is not a
channel** (the reference corpus animates 241 things and none of them is a colour), and `dim_level`
turned out not to be a third channel in this medium at all — a ladder in colour is the forbidden
thing and a ladder in glyphs is `glyph_frame` under another name.

**AND THE PASS FOUND A LIVE DEFECT WHILE BUILDING THE SPIN.** industrial's `SPIN[3]` was `\`;
`Kit.spinner` emits `f"[tone]{glyph}[/]"`; a backslash in front of a `[` escapes it in BOTH parsers
(#31). **industrial's spinner had been putting a raw `[/]` on the gallery and the aperture every
fourth frame, for as long as that spinner has existed**, at a seat no `[/]` law ever ran over. Fixed
(`╲`), guarded by a both-parsers law over every motion frame and every spinner frame, and re-armed
as mutation M7.

**THE MOST VALUABLE THING THE MUTATION BATTERY PRODUCED WAS A CRASH, NOT A RED.** M3
(single-frame transition) killed the suite at check 90 with ZERO reds, because a pass-49 law indexed
`flip_frames`' output unguarded — safe for ten passes only because nothing could make that list
empty, and the motion engine can. **A dead run is not a green run and it is not a red one either.**
Guarded, re-run, 242 reds. Read the fifty-ninth pass for the mutation table, the storyboards and the
two live-seat races it closed.

**THE HEADLINE OF THIS PASS: the law landed, and building it found that pass 57's PRE measurement of
the prototype's queue was taken OFF THE GLASS.** `_p57_prove.py` §3 dumped `widget_slice/app.py:1404`
at 60x**30**. `#queue` sits at y=23..29 and is 10-12 rows tall, so at 30 rows every language's queue
runs off the bottom of the screen: the compositor drew 1 to 7 of its rows, the hazard was on none of
them, and the dump printed `heads_on_glass=[]` for all ten. **That is not a clean surface, it is no
surface** — and pass 57 recorded the trap in item #33 while its own PRE dump had already fallen into
it. The honest PRE exists now, from the mutation: driven at 60x44 with rich's `escape` back in place,
**10 of 10 languages EAT `[URGENT]` out of the prototype's queue**, exactly as the shipped aperture
did.

**What landed.** `verify_widget` grew the escape sweep's section over **both** prototype seats —
`:1404` (the queue title, user text) and `:799` (the config hint row, which needs no fixture because
two of that screen's bindings carry `key_display="["` and `"]"` and **the row contains its own
bracket span**). Ten languages × two surfaces, no-leak **and** no-deletion, a vacuity guard per
surface, plus the grep-able source rule. **24 → 97.** Item **#33 is CLOSED**.

**And the port found a defect in the law it was porting FROM — reported, not carried silently.** The
`mangled` helper is case-insensitive (it must be: darkside lower-cases titles, blueprint upper-cases
them), so `[urgent]` and `[URGENT]` fold to the SAME string and `verify_aperture`'s vacuity guard
`len(on_glass) >= 2` is **one hazard head counted twice, not two heads found**. It cannot tell "both
hazard titles rendered" from "one did". This pass's version counts the TAILS, which are genuinely
distinct, and requires exactly two. **`verify_aperture` still carries the weak form — new item #35.**

**Read the fifty-eighth pass for the mutation table and the 60x30 measurement; read the fifty-seventh
for the site table and the shipped-seat sweep.**

**This block and the classification table under it supersede the status of every item they name.**
Everything below them is the historical record. The passes are kept verbatim because the diagnoses
are the value of this file — but an item's CURRENT state is the stamp it carries in the table here,
not the last sentence written about it three thousand lines down. **Nothing in this file is open
except the rows stamped `OPEN` (#2, #3, #22, #26, #30, #31, #34, #36, #46) and the APP
half of the SPLIT row #32.** Every other item carries a `DEFERRED` or `CLOSED` stamp with a reason and a
trigger. The fifty-third pass added #26, #27 and #28; the fifty-fourth added #29; the fifty-fifth
added **#30** and closed **#1**; the fifty-sixth **closed #25** and added **#31** and **#32**; the
fifty-seventh **split #32** — design half closed, app half deferred — and added **#33** and **#34**;
the fifty-eighth **closed #33** and added **#35**; the fifty-ninth **closed #27 and #35** and added
**#36**; the sixtieth **closed P2** and added **#37**, **#38** and **#39**; the sixty-first
**closed #37 and #38** and added **#40**, **#41** and **#42**; the sixty-second **closed #40, #41
and #42** and added **#43**; the sixty-third **closed #39** and added **#44**; the sixty-fourth
**closed #43 and #44** and added **#45**; the sixty-fifth **closed #45 and #40d** — the data-viz
family's last two governance remainders — and added **#46**; the sixty-sixth **closed nothing in
this register and cured a class it had never named** (the ORACLE SWEEP: 52 raise-instead-of-report
constructs at 34 sites), adding **#47** and **#48**; the sixty-seventh **closed #47 and #48** and
added nothing — it cured the `[n]` class the sixty-sixth could only census, and found that census
had missed both of the constructs its own two dead mutants died on.

**#47 — `[0]` ON A POSSIBLY-EMPTY SEQUENCE (CLOSED by the sixty-seventh pass — 31 cured through the
`nth()` seat and explicit non-emptiness legs, 2 exempted with claimed-AND-USED markers, held at zero
by a standing law that reads laws, DETAILs AND setup lines. The count moved from 45/23 to 33/24
because the detector could not read four kinds of guard the suite's own authors write, and could not
see either construct its evidence mutants died on: a `[0]` in an assignment and a `split(...)[1]`.
THE ACCEPTANCE TEST: M2a and M3a, pass 66's own battery unmodified, now reach the verdict line and
report 8 and 19 reds against 3 each and a dead run. See the sixty-seventh pass's block at the top.)**
The
same disease as the named trap and the same cost — a raised law reports nothing and takes the rest of
the file with it — but it is NOT the same fix. `at()` has one right answer for every `.index` site
(-1, which no comparison in this suite is satisfied by once the `>= 0` legs are in). A `[0]` on an
empty list has **no single right sentinel**: each site needs a value that makes ITS OWN law red, and
thirty of those smuggled into one pass is exactly the un-reviewable edit this project refuses.

**IT IS MEASURED, NOT PREDICTED. Two of this pass's five arm-A mutants died on it in the CURED
tree** — M2a at `ax_cols = sorted(i for i, ch in enumerate(ib[iax[0]]) ...)` (`IndexError`, after
correctly reporting three reds including one of this pass's own cured laws) and M3a at
`bp_span(1).split(BP.CLOSE)[1]` (`IndexError`, after three reds). Both reached their reds and then
lost the verdict line. Sites, from `_p66_prove.py` §6 (line numbers as of this pass's POST):

`cond`: 3409 · 6650 · 6655 · 6668 · 6674 · 7024 · 7028 · 7033 · 7036 · 7226 · 8416 · 9245 (×2, incl.
`[1]`) · 9249 (×3) · 9927 · 9929 · 10268 (×3) · 10439 (×4) · 10557 · 10670 (×2) · 10676 (×2) ·
11126 · 11501.  `DETAIL`: 2596 · 6655 · 6668 · 7028 · 7036 · 9245 (×2) · 10439 · 10557 · 10670 ·
11126 · 11501. Trigger: **the next pass that writes laws in any of those sections**, or any pass
willing to spend an increment on per-site sentinels. Re-run `python prototypes/out/_p66_sweep.py
--full` for the live list; the addresses drift with edits, the shape does not.

**#48 — `not any(... range(len(X)))` IS TRUE ON AN EMPTY `X` (CLOSED by the sixty-seventh pass, and
REFUTED at the address it names. `mrows` is a comprehension over a literal three-element tuple with
no `if` — it has exactly 3 items on every input, `range(len(mrows))` is never empty, and the law CAN
fire. The prescribed leg would itself have been a leg that cannot fire. The shape is real and the
suite has it at what is now L10069 — `RAIL not in "
".join(body_rows(boards[name]))`, one of the two
neighbours this item named in passing and did not examine — which is where it was cured, with
`bool(_brows)`. The original text is kept verbatim below because a filed item that was wrong is
worth more than one quietly rewritten.)** At
`verify_language.py` L8085: `check("nord: ... and no MASTER row is (...)", not any(isolated(mrows, i)
for i in range(len(mrows))))`. If the split's master pane rendered nothing, `mrows` is empty,
`range(0)` is empty, `any([])` is False and the law passes — **on the exact input it exists to refuse
reasoning about**. No sibling asserts `mrows` is non-empty. The fix is one leg (`len(mrows) >= 2
and ...`) and it is a one-line edit; it is filed rather than folded in because it is the SAMPLE's
finding, not the swept class, and the sample exists to estimate a rate. **The rate it estimated: 1
in 24 with no anchor, 2 more anchored only implicitly.** Two neighbours worth reading when this is
taken: L8629 (`pen not in calm_page`) and L9963 (`RAIL not in "\n".join(...)`), both anchored today
by sibling positive laws but neither asserting its own non-emptiness.

**#46 — THE HALF CELL'S MISSING TRACK DOT (CLOSED by the sixty-eighth pass. The cured glyph is
`⡗` and it is COMPOSED rather than chosen — the full cell's LEFT sub-column OR the track's RIGHT one
— so the law spells the derivation and never the answer. THREE half-cell FILL sites, not one: the
meter mechanism, instrument's bench readout and its scope trace; two of the three now read the
`Instrument.HALF` seat and the third is module-level, held by a census. FOUR `⡇` seats are exempt
and each is read off the shipped seat: a knob whose sub-column is STATE, a caret with no track
behind it, a gantt today-LINE, and naught's FINE ramp where it is the TOP of four heights. THE
FINDING ON THE WAY: pass 62's 428-string render grid is `cmp`-CLEAN across this cure, because none
of its five instrument meter fixtures produces an odd dot count — the grid never drew the cell #46
is about. The original text is kept verbatim below.)** `_meter_braille`'s bar draws `⡇` for a
half-filled cell: the left sub-column full, and the right sub-column — which is UNRUN — carrying no
track dot at all. The two-unlit verdict (sixty-fifth pass) establishes the rule it violates: on a
half-cell fill the track inks every ADDRESSABLE sub-column, which is exactly why the bar's unlit is
`⠒` and not `⠐`. The mark that would carry it is `⡗`. **It moves shipped cells**, so it is a design
increment and not hygiene; deliberately not folded into a pass whose entire claim was a `cmp`-clean
render diff. Trigger: any pass willing to move the instrument language's meter.

**Suites at closure.** THREE back-to-back full runs at the sixty-sixth pass. "checks" is the count
of `[PASS]` lines.

| suite | checks | sixty-fifth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9810** | 9807 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 · 137 · 137** — no flake this pass |

**NO RED IN THE SIXTY-FIFTH PASS'S THREE ROUNDS, AND #22 STAYS OPEN ANYWAY.** The clipboard test
held 3/3 and zero `settle timeout` lines appeared across three suite runs and eight mutation runs.
The machine was quiet; that is not the same as the test being independent of it, and neither watch
is claimed cured. **The paragraph below is the sixty-fourth pass's record and is kept verbatim** —
it is the reason the item is open.

**THE ONE RED IN THE SIXTY-FOURTH PASS'S THREE ROUNDS, SAID OUT LOUD.** Run 2's pytest was **136 passed, 1 failed**:
`tests/test_app.py::test_win_clipboard_roundtrip`. The captured stderr carries the cause —
`Set-Clipboard : Requested Clipboard operation did not succeed` — so the OS clipboard was held by
another process for the length of that call and the test's own SETUP never happened. **It is
environmental, not a regression**: runs 1 and 3 passed it, it passes 3/3 re-run in isolation, and
this increment touched no clipboard path (the diff is two meter mechanisms, a registry comment, the
suite and this file). **Recorded rather than re-rolled until green** — a suite that is quietly
re-run until it agrees is not a suite.

**+69 on `verify_language`; the other five suites did not move by one check** — and this time the
diff-scope statement is the verdict itself: **no source file was opened**, so the render signature is
byte-identical to pass 62's POST. The +69: **+54** the per-seat audit (18 laws × 3 seats), **+15**
the family-level laws (the source census, the three seat anchors, the declared-ink census, the `fine`
ink-tie pin, A's registry identity, B's two-ended value law and its own middle, the zero-routing
recorder and its removal, cross-process determinism and its did-it-run guard, and pass 60's three
named disagreements re-measured off the glass).

**+85 on `verify_language`; the other four suites did not move by one check** — the same diff-scope
statement pass 61 made, after a pass that changed corgi's meter and nord's plot: no snapshot outside
`verify_language` was pinning either render. The +85: **+48** the meter census (4 instruments × 12
mechanisms, run on host kits because two mechanisms are worn by no language), **+24** #40's two laws
× 12, **+13** globals (the skill's named case at the meter seat, the pair's ink order, the meter/plot
pair as one definition, the source law that the meter NAMES the ramp, gradient's track and its two
shoulder laws, decay's two monotonicity laws, the phosphor-naming law, nord's zero column, the proof
the baseline cure cannot reach a column with data, and the census-count guard).

**THE CAPTURE RACE DID NOT FIRE AT THIS PASS** — zero `settle timeout` lines across fifteen suite
runs and eight mutation runs. The standing watch is not claimed cured; the machine was quiet.

**THE CAPTURE RACE FIRED TWICE TODAY AND IS NOT CLAIMED AWAY.** `capture settle timeout: board never
painted` appeared in **run 1 of 3** (`seats instrument @118`) and in the re-baseline run before it
(`legend instrument @118x30`), and **runs 2 and 3 were clean at 9452/0**. Across the pass's THIRTEEN
`verify_language` runs it fired **twice, both while a foreign python process (PID 3324, a day-old
job) was burning CPU and the machine sat at ~49% load**; the ten runs of the mutation battery, taken
earlier under a quiet machine, fired it zero times. **That is a correlation, not a diagnosis**, and
it is the standing capture-race watch rather than a new defect: this pass's renders are proven
byte-identical to the pre-pass ones at every routed seat (258 strings, 0 divergences), so a
render-caused regression is excluded — but a timing-caused one is not excluded by argument, and no
run was thrown away to make the table look better.

**THE PYTEST ROW HELD AT 137 IN ALL THREE RUNS**, `test_win_clipboard_roundtrip` included. That is
the second pass in a row it has passed and it does **not** close item #22 — the test's verdict still
depends on whether another process holds the Windows clipboard.

The +109 of the fifty-sixth are the escape sweep's own section. Before it, the +742 of the stepper entering the
contract, the scroll bar's +368, the text field's +730, the button's +592, the radio's +2343, the
checkbox's +621, the switch's +569, and the contract itself +351.

**THE HEADLINE: THE EIGHTH COMPONENT LANDED AND THE FAMILY IS CLOSED.** The registry now holds
slider · bar · switch · checkbox · radio · button · text field · scroll bar · **stepper**, with FIVE
anatomies (extent, presence, field, window, series), THREE declared facts in TWO families (`GRIPS`
about parts; `CHECKABLE` and `VIEWED` about the value), ONE group scope above the registry
(`group_states`), THREE mechanism seats (`value_pos`/`value_at`, `view_pos`/`view_start`,
`step_index`) and ONE composer. No component's states are hand-listed anywhere.

**THE STEPPER'S TWO RULINGS.** (1) **A stepper and a radio are ONE CHOICE with TWO MECHANISMS** —
two registry entries, because the registry describes ANATOMY and a word between two steps is not N
wells with a mark; one choice model, because `group_states` already owns "one index into a set" and
`Kit.stepper` reaches it, so the out-of-range refusal, the single-selection invariant and the shown
option's state all come from the seat the radio uses. It is the INVERSE of every collision this
registry had met: the switch and the scroll bar shared a tuple and differed in the VALUE, and were
separated by a declared fact. (2) **Wrap vs clamp is an ARGUMENT, not a registry fact** — a fact
would say something about every stepper, and wrap is true of every RING; this app already holds both
readings (`action_cycle_theme` wraps, `action_pick` clamps) and chooses per call site by what the
range MEANS. **The end is visible in SHAPE**: the composer asks `step_index` whether a step exists
and draws GROUND where one does not, so a clamped stepper at its floor SHOWS its floor and a
wrapping one never does, with no new state and no colour.

**ONE NEW PART, NO NEW DECLARED FACT — pass 54's warning answered rather than ignored.** `step` is a
single part whose EVEN glyph string is read at its two halves (the button's walls convention, read
for direction), `CHECKABLE` and `VIEWED` are byte-identical, and what grew was `GRIPS` — the seat
pass 53 built so that "which parts are grips" is a registry edit and never a term inside `actuator`.

**THE LIVE SEAT STOPPED RENOUNCING.** The narrow config screen used to print the worker group as a
WORD — the control given up because a radio set with options missing is a different set. That is
exactly what a stepper is for, so the narrow screen now changes MECHANISM: same set, same index,
same key, one option on screen, clamping because `action_pick` clamps. The threshold row was read
for and REFUSED (a magnitude on a floating scale with no ceiling is a slider being stepped, not a
stepper), and pass 54's prediction that `value_at` would get its first real caller is reported
**FALSIFIED**: a named set has no scale, so "the value at index i" is a list lookup.

**THE PYTEST ROW CHANGED AND IT IS NOT A FIX.** `test_win_clipboard_roundtrip` PASSED in all three
runs of this pass and FAILED in all three of each of the last five. Nothing in `tests/` or
`taskboard/app.py` was touched by this pass; the Windows clipboard was simply available this time.
**Item #22 stays OPEN** — a test whose verdict depends on whether another process holds the
clipboard is exactly the test that teaches a suite to be ignored.

**ROUND ONE OF THE MUTATION TABLE HAD FOUR DEAD RUNS AND ONE HOLE, and both are reported rather than
buried.** Three of the dead runs were the SAME instrument defect for the THIRD time — an oracle dict
keyed by the DERIVED axis, `KeyError` when a mutation shrinks it (pass 52's grew it, pass 53's shrank
it). The cure is not `.get()`: the membership IS the claim, so the laws assert it and read red. The
fourth was a `try/except ValueError` that a mutated call raised `IndexError` past — **catching only
the exception you expect lets the wrong one kill the run**, and the type is now part of the
assertion. The HOLE was the sharpest finding of the pass: a live seat drawn `wrap=True` while
`action_pick` CLAMPS survived every law, because every law asked the LANGUAGE what it draws and none
asked the SCREEN. Cured with a section that reads `action_pick`'s own source and asserts the live row
against it (30 red), which also took the default-flip mutation from 1 red to 31.

**THE VACUITY PROVER DELETED A DEFAULT.** M3 was first written against `step_index`'s own
`wrap=False` and the prover called it VACUOUS — correctly: no caller ever reached it, because both
composing seats state their reading. The default was removed rather than the mutation quietly
retargeted, and a law now asserts the seat takes none.

**Flake watch.** Nothing fired — not in the fifteen suite runs of the three sets, not in the
twenty-one mutation runs, not in the two vacuity-prover runs. Settle headroom stayed at **worst 4 of
40**, unchanged for six passes.

**Flake status — the suite is FLAKE-FREE.** The last live flake was the darkside capture race, cured
in the forty-sixth pass. The one env-dependency is `test_win_clipboard_roundtrip` (item #22), which
this pass saw pass and the five before it saw fail.

**The COMPONENT-CONTRACT track is COMPLETE.** What the contract does NOT yet cover is named in the
fifty-fifth pass's closing section and in items #26-#30: **select/dropdown** (the first component
whose value is off screen until it opens — a POPUP question), **tabs/segmented as the group scope's
next tenants** (still pre-contract kit methods), the **picking** half of the date/cell picker,
`invalid` as a `VALIDATABLE` bit (#26), and MOTION (#27), which the family now owes FOUR tempo
questions instead of three.

**Entry point for a fresh session — read in this order, and stop when you have what you need:**

1. **`PENDING.md`** — this block, then the classification table. Read further only if the table
   sends you to a pass by number.
2. **`RUN.md`** — how to run the app and every suite, the ten languages, the keys, and the
   `$env:PYTHONIOENCODING` requirement.
3. **`~/.claude/skills/tui-design/`** — the design language this code implements. `COMPONENTS.md`
   is this track's brief; `DATAVIZ.md` holds the laws the kits already obey.

`HANDOFF.md` §6 is still the trap list and is still worth ten minutes before touching geometry.

### Classification table — every open item, stamped

| # | item | stamp | why, and when it becomes relevant again |
|---|---|---|---|
| 1 | **Input components** — button, text field, checkbox, stepper, scroll bar per language | **CLOSED — fifty-fifth pass** | The component-contract track is COMPLETE. Increment 1 shipped the CONTRACT (parts registry + derived state axis) with **slider and bar**; 2 **switch** and the CHECKED product axis; 3 **checkbox** and the proof that CHECKABLE is a registry fact; 4 **radio** and a SIBLING-SCOPED seat (`group_states`); 5 **button**, the ACTUATOR, and the ruling that TEXT IS NOT A PART; 6 **text field** and the registry's first new part, `caret`, plus `GRIPS`, `has_interior` and the window; 7 **scroll bar** and `VIEWED` (the value's ARITY) plus `view_pos`/`view_start`; 8 **stepper** and the END of a range — `step`, `step_index`, and the ruling that **wrap vs clamp is the caller's argument and not a registry fact**, visible in SHAPE because a seat with no step draws GROUND. Eight components, five anatomies, three declared facts, zero hand-listed states. **What the contract does not yet cover is a NEW item, not this one:** select/dropdown and tabs-as-group-tenants are named in the fifty-fifth pass's closing section and in #30. |
| 2 | **The gallery should demo `plot` variants** (`g` screen) | **OPEN — partly served; the LAYOUT question is CLOSED** | The gallery carries the slider's five states, the bar's two, the switch's and checkbox's eight each, and the radio's four control states as a three-item set. The layout question passes 48 and 49 deferred is **decided and measured** in the fiftieth pass and applied again in the fifty-first: each block measures itself and reflows (radio: 5 rows across at 45 columns, 13 rows down at 28), and **the gallery scrolls by design**. `plot` variants are still owed. |
| 3 | **No runnable exemplar screen in the skill** (`assets/exemplar.py`, old item B.7) | **CLOSED — sixty-ninth pass** | Shipped to the SKILL repo: `~/.claude/skills/tui-design/assets/exemplar.py` (one screen, 426 code lines under 525 of citation) plus `assets/verify_exemplar.py`, **the first law this skill has ever had — 51 checks, ALL PASSED ×3**, six mutants at 1-5 reds each and none vacuous, baseline == restored. Structure-not-tone is measured by a token-mutation law with a **colour-only CONTROL** that must not move the greyscale render. See the sixty-ninth pass's block at the top. |
| 4 | **Board `Footer` is size-blind** — at 118 all 11 entries print, at 96 it clips after `a Add`, at 80 after `q Quit` | **DEFERRED** — design polish; needs a custom widget because Textual's `Footer` cannot degrade | Revisit **with the component track's legend work** — a degrading footer is a component with a contract, which is that track's whole subject. Mitigated today: `? Keys` and `q Quit` are printed FIRST so the two keys that must survive a clip do. |
| 5 | **Modals shadow the board's footer** while it advertises keys they consume | **DEFERRED** — same shape as #4; the fix (a Footer per modal) needs `modals.py` | Revisit with the component track's legend work. Not dangerous today: `ModalScreen` stops app bindings, so those keys are inert, not wrong. |
| 6 | **`CARD_OWN` double-spend** — every card row leaves two cells of its content box unused at the right | **DEFERRED** — cosmetic geometry | Fixing it widens every card by two cells and moves every app-level geometry assertion in the suite; it is a separate increment, not a grooming edit. **Revisit if cards ever feel narrow.** |
| 7 | **The language switch can render one stale frame** — `set_language` changes region widths and rows built before layout wrap inside the new composition (darkside's queue folds its date chips) | **DEFERRED** — cosmetic, exactly one frame; the 1 s tick heals it | **The cure is known and named: a width-CHANGE trigger, not a frame count.** A 2-frame `call_after_refresh` was tried, fired mid-layout, sent solari/ledger/blueprint's band laws red, and was reverted (bisected). Revisit if a user reports seeing it. |
| 8 | **`HERO_FONT` has no metrics table of its own** (pass 36's item 3, re-flagged in 44 and 45) | **DEFERRED** — belongs to the **drawn-type track** | Every other pixel base has measured metrics; `HERO_FONT` is measured ad hoc at each call site. Revisit when display type is reopened as a track of its own. |
| 9 | **"The hero is still a small mark in a wide field"** (pass 36's item 5) | **DEFERRED — this is a DESIGN JUDGMENT for the user, not a defect** | No test can settle it and none should try. The hero is correct at every seat it stands in; the question is whether the user wants it bigger. Revisit **when the user says so**, and treat their words as the spec. |
| 10 | **Settle condition C for `.col-head` / `.kb-empty`** (pass 46's suggested follow-up) | **DEFERRED — attempted this pass and declined on measurement, see the note under this table** | Revisit only if a head or empty seat is ever OBSERVED carrying a wrong width. The oracle it would need is a build-level one, not a widget shadow render. |
| 11 | **Ink-fraction floor** — all 8 languages measured under 35% at h=26, plus unexplained run-to-run variance on the board class (old item A.1) | **DEFERRED** — the number has nothing to be measured against | The 35% floor is unfalsifiable until `DENSITY.md` states its geometry (#12). The two move together or not at all. `verify_ink.py` stays a probe, never a gate. |
| 12 | **`DENSITY.md` does not state the geometry its 35% floor is measured at** (old item B.8) | **DEFERRED** — a skill edit, not an app edit | Revisit with #11, in a skill pass. |
| 13 | **hex vs Textual theme variables never reconciled** — `PALETTE.md` says hex, `NAVIGATION.md` uses `$accent` (old item B.9) | **DEFERRED** — documentation contradiction in the skill | Revisit the next time an app is scaffolded from `tui-design` by someone who is not the author — that is when the contradiction actually costs something. |
| 14 | **`SKILL.md.bak`** stale leftover in the skill directory (old item B.10) | **DEFERRED** — one deletion, outside this repo, needs the user's word | Revisit at the next `tui-design` edit. |
| 15 | **`/html-visualizer` was never refined** (old item C.11) | **DEFERRED — scope it as its own batch, not an increment** | The largest single outstanding item anywhere. Owed the treatment `tui-design` received: intake step, measured claims, verification discipline, reusable assets. Revisit when the TUI work is put down. |
| 16 | **Orphaned `clipboard-fix/` directory** in `<repo>/.claude/worktrees/`, not in `git worktree list` (old item C.13) | **DEFERRED** — not ours; deleting anything under `.claude/worktrees/` needs explicit approval | Revisit at a worktree cleanup, with the user present. |
| 17 | **`action_cycle_size` is one-way** — sets `self.forced` permanently, no route back to width-based sizing (old item A.4) | **DEFERRED** — a four-line binding change with no design question in it | Revisit when someone actually gets stuck in a forced size class and says so. |
| 18 | **`bases.wave` is barely used** (old item A.6) | **DEFERRED** — a base with no consumer | Revisit if a language wants a wave-based meter or a sparkline that is not `spark`. |
| 19 | **naught's `motion="bloom"`** (old item 0c) and **ledger's `motion="leader"`** (old item 5) | **DEFERRED — and its trigger fired without being taken, which is said rather than left implied** | Revisit if the MOTION axis is reopened. **The fifty-ninth pass reopened it and did NOT take these**, deliberately: both are SURFACE motions (a panel blooming in, a leader drawing itself), and what that pass built is the COMPONENT motion contract — an engine whose frames are component renders and whose regimes are derived from interaction events. A surface arrival is neither. They would now have somewhere to land (`MOTION_EVENTS` plus a builder), which is more than they had before, and they are still tokens no language declares and no user has asked for. |
| 20 | **A `reflow` token** — the page choosing between renouncing a column and shrinking it; `cols()` hardcodes the renunciation order (old item 6) | **DEFERRED** — no language has asked for it | Revisit when a language wants to shrink rather than renounce. |
| 21 | **scatter / line as braille fields** — the data-viz primitives stop at spark / plot / gauge | **DEFERRED** — no surface needs a scatter today | Revisit when one does; `DATAVIZ.md`'s laws already say how it would have to behave. |
| 22 | **`test_win_clipboard_roundtrip` has no skipif/mock** | **OPEN — and now PROVED env-dependent** | It FAILED in every run of passes 50-54 (`Set-Clipboard : MissingArgument`) and **PASSED in all three runs of pass 55**, with nothing in `tests/` or `taskboard/app.py` touched between them. That is the diagnosis completed rather than the defect fixed: the verdict depends on whether another process holds the Windows clipboard. A test that flips on someone else's process is how a suite learns to be ignored — **give it a skipif or a mock next time `tests/` is opened.** |
| 23 | **Kimi still-adoptables** — mode-switch by measured demand via `plain_width`; mascot height-pair check | **DEFERRED** — external suggestions, never adopted, never missed | Revisit if the COMPOSITION axis is reopened. |
| 25 | **~25 other `escape()` call sites in `language.py` carry the two-parser hazard** — card titles, notes, hero captions and tile values are escaped rich's way | **CLOSED — fifty-sixth pass** | Twenty-three sites / twenty-six calls, all routed through `mark`, the `rich.markup` import DROPPED, and the absence asserted so the rule is one grep. **The predicted defect was not the one found: it was not a `[/]` leak, it was SILENT DELETION** — rich escapes `[urgent]` and not `[URGENT]`, three languages upper-case their titles, and Textual ate the token, so corgi, solari and blueprint were printing ` SHIP IT` for a task titled `[urgent] ship it`. The no-leak law therefore grew a SECOND half (a tail without its head is deleted text), is case-insensitive because languages disagree about case, and now runs over board + config + gallery in all ten languages against a hazard fixture. +109 checks; five mutations caught on the glass. **What is still owed is two NEW items, not this one: #31 (the trailing backslash) and #32 (the other 44 sites).** |
| 31 | **Text ending in a single backslash cannot be rendered next to a close tag** — `escape` doubles it, `mark` does not, and under Textual BOTH print a raw `[/]` | **OPEN — measured, asserted, and not curable at this seat** | The only bracket-free string on which the two escapings disagree, found by the fifty-sixth pass's byte-identity check. Textual reads a `\` in front of a `[` as escaping the bracket whether or not another `\` precedes it, so at the seat every kit uses — `f"[tone]{text}[/]"` — no encoding closes the tag under both parsers (five searched, `_p56_prove.py` §3b). **The suite asserts the whole finding, including that both escapings leak**, so a future rich or Textual that changes the rule goes red here. A real cure means not putting a close tag immediately behind user text (a sentinel, or a `Content` object instead of a markup string) — a mechanism change, not an escaping change. **Revisit when a user's title or a Windows path in a note actually ends in a backslash**, or when the seat is rebuilt for another reason. |
| 32 | **The same escaping defect at 44 sites in the files the sweep could not reach** — `modals.py` (22), `views.py` (14), `views_widget.py` (4), `aperture.py` (1), the prototype's `app.py` (2), `hero.py` (1) | **SPLIT by the fifty-seventh pass. DESIGN half CLOSED (4 sites); APP half DEFERRED-to-real-app-work (40 sites)** | **CLOSED half — the design surface.** `aperture.py:386`, `hero.py:250` and the prototype's `app.py:1404, 800` all route through `mark`, both shipped modules dropped the `rich.markup` import and the absence is asserted. The census under-reported it twice: driven across all ten languages the queue defect is **10 of 10**, not the three pass 56 sampled, and `hero.py:250` is not an app literal — `sig_deadline` puts `t.title` in `Reading.detail`, so the hero prints the user's TITLE and swiss, industrial and darkside were eating it. `verify_aperture` +57 (151 → 208); four mutations caught on the glass. **DEFERRED half — the app surface.** `modals.py` (22) · `views.py` (14) · `views_widget.py` (4) = **40 sites, grep-verified at this pass**, untouched because this worktree is a design SHOWCASE and those are the real app's functional surfaces (the user's scope rule). **The recipe is proven twice and is named, so this is mechanical when the real-app work opens:** swap each site to `LG.mark`, drop the `rich.markup` import, assert its absence in that suite, then drive the hazard fixture (`[urgent] ship it` · `[URGENT] rotate keys` · `[BLOCKED] audit keys`, project `[QA] Web`) at the surface and assert the PAIR — no literal `[/]` and no bracketed head EATEN, case-insensitive, with a per-surface vacuity guard that the hazard is on the glass. **Do `modals.py` first**: 22 sites, every one text the user typed, at the surface where they type it. |
| 33 | **The prototype's two swept sites have no STANDING law** — `widget_slice/app.py:1404` (queue title) and `:799` (config hint) are cured but nothing asserts they stay cured | **CLOSED — fifty-eighth pass** | `verify_widget` grew the escape sweep's section over both seats: ten languages × two surfaces, no-leak AND no-deletion, a vacuity guard per surface, plus the grep-able source rule (`escape(` at zero sites, `rich.markup` not imported). **24 → 97.** The mutation proves the law bites — reverting `:1404` to rich's `escape` sends **12 checks red** (2 source-rule + the no-deletion leg in all ten languages) while every vacuity guard stays GREEN, which is the shape a working guard has. **The config seat needed no fixture**: two of that screen's bindings carry `key_display="["` and `"]"`, so the hint row derives `[ threshold - · ] threshold +` and IS its own hazard — and its no-deletion leg is a presence law, not `mangled`, because what Textual eats there is the span from `[` to `]` and it takes the LABEL with it, leaving no tail-without-head for `mangled` to see. **The recorded 60x30 trap was real and pass 57 had already fallen into it — see #35 and the fifty-eighth pass.** |
| 34 | **A queue row carrying a bracketed title renders ONE CELL SHORT of its column** — both queue seats escape and then slice (`mark(t.title)[:tw]:<{tw}`), and the backslash is a character to the slice and the pad but nothing to the parser | **OPEN — measured, not introduced by the sweep, and not cured** | Measured on naught at 118x34: 112 in a 113-cell budget for both hazard rows. `escape` did the same thing (it adds the same backslash to `[urgent]`); what the sweep changed is that the upper-cased case moved from *deleted at full width* to *intact and one cell short*, which is the trade the pass wanted. Pass 44's "every queue row closes EXACTLY on the panel's measure" law stands on the bracket-free fixture and is NOT weakened. **The cure is to slice before escaping and pad on VISIBLE width (`HERO.vis_w`), at both queue seats** — a mechanism change at a seat the fifty-seventh pass was explicitly told to touch surgically. Neighbours item #31: both are the same root, that a markup string's characters and its cells are not the same count. **Revisit when either queue seat is rebuilt, or when a user notices a ragged right edge on a bracketed title.** |
| 36 | **A transition's per-STEP duration can fall under the compositor's own refresh period** — solari derives 8-10 ms steps at a 16.7 ms floor, so frames are scheduled that will be coalesced | **CLOSED — sixty-eighth pass.** A CEILING ON ELABORATION plus an ABSOLUTE FLOOR — two legs, because it is two claims. The ceiling drops one `MOTION_STEPS` at a time and REBUILDS until the derived step clears the floor: it **ASKS THE BUILDER** rather than restating each event's gap arithmetic, because `press` adds one gap per step and `travel` adds one per WELL CROSSED, and a closed form would have to know both. It asks **through the TOKEN on a copy of the kit, not through a `steps=` parameter** — the first form gave every builder that argument and the suite died on its first mutant, because the battery's whole method is to SUBCLASS a builder. It trimmed **exactly the five steps pass 59 measured** (solari press/travel/spin/flip, industrial travel) and **the tempo is untouched**, so solari still snaps in 40 ms. The floor's SECOND leg is what a closed-form `tempo // refresh` cure would have missed: travel's frame count is the DISTANCE's, so at zero elaboration a long enough travel is still under the floor with nothing left to renounce — there the step is floored and the pass RUNS LONG rather than a well being dropped. Realizability survives, and **the tempo is a law now**: a tempo under the refresh period could not be drawn at ANY elaboration, so the honest outcome is a TEMPO a language may not have. The original text is kept verbatim below, including the prediction that it would trim "exactly one language's frame counts" — it trimmed two. | A transition's total is the language's `tempo` and its step is that total over the gaps between frames. Where the tempo is very short and the language elaborates, the step goes under ~16.7 ms and the surface cannot draw every frame. **This is TRUE OF THE SHIPPED FLIP TODAY and was not introduced by the motion pass** — solari has animated its switch at 10 ms steps since pass 49. Measured for every language and every event in `_p59_prove.py` §5. **The cure is a CEILING, and it is the kind this skill exists to state**: cap the gaps at `tempo // refresh`, so a language cannot elaborate faster than the surface can draw. It would trim exactly one language's frame counts — a shipped, green, per-language behaviour — which is an increment of its own, not a rider on the one that found it. **Revisit when the motion axis is next opened, or if solari's flip ever looks like it is skipping.** |
| 35 | **`verify_aperture`'s escape-sweep vacuity guard counts ONE hazard head twice** — `len(on_glass) >= 2` over `[urgent]` and `[URGENT]` against a case-folded blob | **CLOSED — fifty-ninth pass (rider)** | Counted on the distinct TAILS now (`ship it`, `rotate keys`) and required to be **exactly two** — three titles go in and `[BLOCKED] audit keys` rides a Done task that `_queue_markup` filters out. The same read `verify_widget` took in pass 58, so the two suites' guards are visibly one rule. **208 → 208**: the guard was replaced, not added, which is what a cure to an unfalsifiable check looks like. The hero leg was read at the same time and already counted tails. |
| 35d | **the diagnosis #35 carried while it was open, kept verbatim** — the passes are kept because the diagnoses are the value of this file | **CLOSED with #35** | `mangled` is case-insensitive and it has to be (darkside lower-cases titles, blueprint upper-cases them), so the guard's `h.lower() in qblob` tests the SAME string for both heads: the count is 0 or 2, never 1. It therefore cannot distinguish "both hazard titles rendered on this surface" from "one did", which is the exact question a vacuity guard exists to answer. It is not *wrong* today — the aperture's queue does render both — but it is **unfalsifiable in the interesting direction**, and an unfalsifiable vacuity guard is the failure this whole track keeps finding. **The cure is the one `verify_widget` now uses: count the TAILS (`ship it`, `rotate keys`), which are genuinely distinct, and require exactly two.** One line in `escape_laws`, plus the same read for the hero leg. **Revisit the next time `verify_aperture` is opened** — it was outside this pass's three-file budget and is reported rather than smuggled in. |
| 26 | **`invalid` is not a control state and is not built** — the skill's text-field row asks for it; the fifty-third pass ruled it is a SEVERITY on the value, not a state on the interaction axis, and refused to hand-list it | **OPEN — named shape, not started** | The registry can derive it from nothing, every existing state is an interaction state, and structurally it is a BIT that would combine with all four control states the way CHECKED does. **If it is built it belongs where CHECKABLE lives — a registry tuple of VALIDATABLE components — and it applies to slider, stepper and field alike.** Revisit when a surface actually has a value that can be wrong; the app has none today. |
| 27 | **FOUR things this contract owes the MOTION axis** — the button's press has no intermediate frames, the radio's mark does not travel between siblings, the caret does not BLINK, and (added by the fifty-fifth pass) **the stepper's option does not MOVE as it is spun** | **CLOSED — fifty-ninth pass** | All four paid in ONE increment, because they were one question asked four times. What landed is not four animations: it is **one engine (`motion_frames(component, event) -> Motion(frames, regime, step_ms)`), five events, and TWO DISJOINT REGIMES** — `transition` ≤400 ms, `ambient` ≥2000 ms, and the 400-2000 ms dead zone illegal. **A motion is a LIST OF RENDERS**, each one composed by the component seats the contract already had, so pass 49's "no pictures" ruling is enforced by a source law rather than remembered. **Regime and duration are DERIVED from the EVENT and the language's `tempo`; which motions a component HAS is derived from the parts registry; `travel` is NOT — it is a fact about a SET and its seat is the group's** (pass 51's finding, arriving on the motion axis). `FLIP_STEPS` became `MOTION_STEPS` because one token now governs five events, and `flip_frames` survives as a caller that drops frame 0 with **byte-identical output**, asserted per language. **Colour is not a channel**, stated as what it can enforce: the frames must move with the colour taken away and no consecutive pair may differ only in tone. **`dim_level` turned out not to be a third channel in this medium** — a ladder written in colour is the animation the corpus never publishes and one written in glyphs is `glyph_frame` under another name. **The pass found a live defect on the way**: industrial's `SPIN[3]` was `\`, which escapes the close tag in BOTH parsers, so its spinner had been putting a raw `[/]` on the gallery and the aperture every fourth frame — fixed, and guarded by a both-parsers law over every frame. **verify_language 8603 → 9192; seven mutants, all caught, none crashed** (the eighth attempt of M3 did crash and that is its own finding — see the pass). What is NOT closed by this is the per-step refresh floor — new item **#36**. |
| 28 | **The text field has no OVERFLOW MARK** — a scrolled window says nothing about the text behind it | **DEFERRED** — bounded, and priced | The cheap honest answer is a wall variant for "there is more that way", which multiplies each language's five ground forms by four. A design increment of its own. Revisit if a field ever holds a value a user loses track of. |
| 29 | **The contract has no AXIS fact** — a scroll bar is drawn along a row because the caller lays the cells out, and a language that wanted a different glyph VERTICALLY has nowhere to say so | **DEFERRED — bounded and priced** | `component_cells` returns a list; which axis it is stacked on is the caller's, exactly as it is for `bar`, and no language has asked for a second vocabulary. The price if one does: an axis argument threaded to `part_key` (a third scope level, `component.axis.part`), which doubles every scoped glyph table it touches. **Revisit when a language actually wants a vertical shaft that is not its horizontal one rotated** — not before, because a fact nobody uses is the dead metadata this file has refused three times. |
| 30 | **The component family is closed but the INVENTORY is not** — `COMPONENTS.md` still lists **select / dropdown** and **tabs · segmented** as owed, and the picker's PICKING state | **OPEN — named, argued, not started** | The stepper closed the row it shared with select, and select is the harder half: it is the first component whose value is OFF SCREEN until it opens, so it is a POPUP question (a second surface, its own focus, its own dismissal) before it is a component one, and nothing in this contract has ever drawn one. **Tabs/segmented are the cheaper one and the better next test**: the radio pass ruled they are the same fact about siblings wearing different glyphs, so bringing them in is a registry entry plus a glyph table each — and giving `group_states` a THIRD mechanism is the honest test of whether that seat is a seat or a radio feature with a general name. Revisit when the component axis is reopened; the motion batch (#27) and item #25 are both ahead of it. |
| P2 | **`coverage_to_glyph` — the shared DATAVIZ primitive** (the last approved-but-unbuilt Bodmer research proposal) | **CLOSED — sixtieth pass** | ONE function (`coverage_to_glyph` on `coverage_index`), ONE registry (`COVER_RAMPS` × `METER_RAMP`, plus `Kit.cover_ramp()` as the single dispatch seat), and a routing table that names the mechanisms that DO NOT route as loudly as the nine that do. **Nine of ten languages route; solari does not** — a flap board's quantity is a printed FIGURE, and the call recorder asserts it reaches the ramp **zero** times. Beyond spark: `plot`'s partial top cell and `_pulse` route; `plot`'s per-row branches, `gauge`, `bar` and **`Kit.head`'s count bucket** do not, and the last of those is asserted so it stays un-routed. **258 rendered strings, PRE vs POST, 0 divergences — render-neutral, no cure needed and none claimed** — with the arithmetic also frozen as three standing ORACLE laws so the diff is not a one-time measurement. `lo = 0.0` is a RULING: coverage AA may drop faint ink, DATAVIZ law 3 may not, and the skill wins. **The anti-dither refusal is a grep law and M5 proves it bites.** +251 checks; seven mutants, all caught, none crashed. **What is NOT closed by this is three NEW items — #37, #38, #39** — each one a defect this pass measured, declined to cure inside a render-neutral increment, and pinned with a census law that goes red in BOTH directions. |
| 37 | **Nine of the ten coverage ramps have an AIR unlit glyph** — DATAVIZ law 4's named trap, live in nine languages | **CLOSED — sixty-first pass** | **Cured at the ONE registry seat, per language, argued from each language's own meter.** The rule applied to all ten: the unlit glyph is the mark the language ALREADY DRAWS for an empty position on its own `meter`, and where that mark already occupies a LIT level the ramp's own family supplies the step above it (`step` moved `▁` down to index 0 and lifted level 1 to `▂`; `dimension` and the ledger's built ramp did the same with the leader dot). Two ceilings keep it honest and both are laws: the unlit carries INK (not merely "is not a space" — braille's U+2800 BLANK passed that for sixty passes while drawing nothing) and it carries **at most a quarter of the cell**, because a track that reads as data is worse than no track. **18 of 19 ramps now draw a track at coverage 0; `shades` is the ONE exemption and the argument is semantic, not budgetary** — it IS `bases.SHADES`, the BITMAP ramp, whose cell is a pixel of a sprite, and a sprite's ground is ABSENCE rather than a datum worth zero. **The vacuous law that hid this is upgraded under its own name**: "flat-zero series still renders the track" asserted `plot` returns h rows, which four rows of spaces satisfy; it now asserts the spark's every cell is the ramp's own unlit glyph. **76 of 308 fixture renders moved, all of them named**; M1/M4/M6 revert three different ramps and are caught 6/2/5. |
| 37d | **the pass-60 diagnosis, kept verbatim** | **CLOSED with #37** | Law 4: "every ramp needs a real unlit glyph at index 0", because a ramp whose index 0 is a SPACE renders a flat-zero series as *nothing at all* — the law says track, the code draws air. **Only naught's `fine` ramp passes** (`⠂`, ink 0.125). `braille`'s `⠀` is U+2800 BRAILLE PATTERN BLANK: a real codepoint with zero ink, the same defect wearing a glyph's clothes. The standing law only ever asserted `plot` returns **h rows**, which a row of spaces satisfies, so this was invisible for the whole life of the file. **Not cured because the cure is a RENDER CHANGE to nine shipped languages** — it moves every kit signature, every pairwise-greyscale law and every snapshot — and this increment's mandate was byte-identity. **The census law (`AIR_UNLIT`) is what makes it safe to defer:** an eleventh ramp with an air unlit glyph goes red, and so does a cure that lands without updating the record. **Revisit as a design increment of its own**, one ramp at a time, each with its own before/after. |
| 38 | **Two ramps REPEAT a glyph, so two of their four levels are one level in greyscale** — and one is the exact case `DATAVIZ.md` names | **CLOSED — sixty-first pass** | **corgi's `lcd` is `'░▄▆█'`.** The ghost is `░` — corgi's OWN unlit segment, which is exactly what `plot`'s lcd branch already draws for an unlit stack, because an LCD segment is never black, it is faint — and the three lit levels now climb in HEIGHT (`▄ ▆ █`, ink 0.50 / 0.75 / 1.00 strictly increasing), which is the cure the skill prescribes in the same sentence that names the defect. **Level 1 is unchanged, so corgi's spark keeps the glyph it has always drawn for a small sample and the diff is two cells wide.** The census is restated as `REPEAT_AT` — it now pins the exact INDEX PAIR allowed to repeat rather than counting that one does, so a future edit cannot repeat a *different* pair and pass. `hairline` keeps its declared two-weight idiom at (2, 3) and is the only entry left. **The named case is asserted BY NAME**, against the skill's sentence rather than against a set, so no census edit can retire it. M2 puts `' ▄▄█'` back and 9 checks go red. |
| 38d | **the pass-60 diagnosis, kept verbatim** | **CLOSED with #38** | `lcd` is `' ▄▄█'`: levels 1 and 2 are the same glyph and differ **only in TONE** (`dim` vs the theme's `screen`). DATAVIZ law 1 cites this by name — "an LCD spark whose lit and ghost segments share a glyph is invisible in greyscale; it needed segment HEIGHT" — and the skill's own example is still live in corgi. `hairline` (`' ─━━'`, levels 2 and 3) is the milder shape: a *declared* two-weight idiom, not a colour-only step, but still a 4-level scale with 3 forms. **This is a colour-carries-the-data violation and it outranks #37 in severity**, because #37 loses the zero row and this loses a level in the middle of the range. The cure for `lcd` is one glyph (`' ▁▄█'` or `' ▄▆█'`) and it changes corgi's spark. **Censused as `REPEATS`; revisit with #37, in the same increment, because both are ramp edits and both move the same snapshots.** |
| 39 | **A SECOND quantiser family lives in the repo and the primitive serves one of them** — nearest-index vs band-threshold | **CLOSED — sixty-third pass. COMPLIANT BY MEASUREMENT; routing unnecessary. And the item named TWO seats when there are THREE.** | The deferral was on RENDER-RISK grounds ("routing would move cells"), never on proven compliance — an exemption whose whole argument was that curing it is expensive. **This pass held the band family to the four laws and the two ceilings WITHOUT routing it, and it passes every leg the ROUTED family is measured by: 39 of 39 parity legs, 3 seats × 13 legs.** Read OFF THE RENDERED STRING at 4009 exact rational coverages per seat, band edges landed on exactly. **The family census found a THIRD seat #39 never named** — `_meter_step`'s flow row (`. o O`, darkside) is the same 3-level band quantiser; pass 62 saw that ROW under #43 and did not recognise the QUANTISER. **Seat C could not have been audited without opening the ink instrument**: `mink` weighs every letter 1.0, so `.`, `o` and `O` all weighed the same and no ink law could ORDER them; three declarations argued on the existing table's own logic (`·`=0.10 so a full stop is 0.10; hollow sits at 0.35; the heavy slot 0.55) are what make C measurable. **The DISAGREEMENT is a difference, not a violation** — 34.3% of the domain for A, 9.0% for B and C, pinned as numbers — because two quantisers that are each monotone, deterministic, threshold-honouring and greyscale-separable may put their level changes in different places; the laws constrain the SHAPE of a quantiser, they do not appoint one band layout. **ZERO renders moved** (signature byte-identical to pass 62's POST), because nothing was cured — that is the point of the verdict. **+69 checks; six mutants, all caught, none crashed.** The routing question stays CLOSED and the call recorder now asserts the three seats reach the primitive **zero** times, so "does not route" is a measured fact rather than an omission. What is NOT closed by this is **#44**. |
| 39d | **the pass-60 diagnosis, kept verbatim** | **CLOSED with #39, and its seat count is superseded by the row above** | Nearest-index (`coverage_index`): `round(n*c)` with a microbar floor. Band-threshold: `3 if c > .66 else 2 if c > .33 else 1 if c > 0 else 0`. **They disagree at c = 0.34, 0.40 and 0.67** (measured, `_p60_prove.py` §6c — re-measured off the glass in pass 63 and still true). Two seats: **`naught.dot_heat`** (the FINE dot scale — the reason `naught.py` was read for this increment and left alone) and **`language._meter_braille`**'s flow row (`⣿ / ⠶ / ⠐`). Routing either one moves real cells on a shipped surface, so it is not a refactor. **Two honest ends, and the choice is a design question, not a cleanup:** either give the primitive a declared BAND mode (a second quantiser with one name, which is more API than one unused mode deserves) or migrate the two seats to nearest-index and accept the render diff. **Revisit when either seat is opened for another reason**, or with #37/#38, since all three are the same increment's shape. |
| 44 | **`_meter_braille`'s flow row SPELLS the two registry glyphs its ends share instead of NAMING them** — the convention `_meter_lcd` and `_meter_decay` adopted in pass 62, not yet applied here | **CLOSED — sixty-fourth pass. Named, and the render is byte-identical** | The flow statement reads `ramp[0]` and `ramp[3]` off `COVER_RAMPS["braille"]`; the middle stays `⠶`, this row's own, because **a 3-level flow row on a 4-level coverage ramp is not a copy of it**. The registry comment is rewritten in the RIGHT direction: it was "`⠐` is what `_meter_braille` prints", which is the definition citing its reader. **The pass-63 VALUE law is kept unchanged and is still the stronger guard** — naming stops the meter drifting, a value law reds whichever side moves — and M3 proves the split: reverting the naming reds **4** laws and **not one of them is the value law**, because the two still agree. **Zero renders moved.** The claim is exactly as wide as the cure and the suite says so: **three other seats still spell `⠐`** (`Instrument.BLANK`, its `radio.main`, `plot`'s `off=`), they are the KIT's vocabulary and a third mechanism, and a law asserts there are four seats and none inside the meter. |
| 45 | **The flow row's ramp is read from a REGISTRY ROW at two seats and from `Kit.cover_ramp()` at none** — the one-seat dispatch the rest of the data-viz family uses | **OPEN — measured by the sixty-fourth pass, deliberately not taken** | `_meter_step` and `_meter_braille` now say `COVER_RAMPS["step"]` / `COVER_RAMPS["braille"]`, which is **the convention pass 62 set** for `_meter_lcd`, `_meter_decay` and `_meter_gradient` — so this pass conformed to it rather than forking a better one mid-increment (engineering rule 11). But `Kit.cover_ramp()` is documented as "**THE ONE SEAT that says what this language's coverage ramp is**", it dispatches on the same `meter` token, and it is what a mechanism hosted on an arbitrary kit ought to ask. Five `_meter_*` functions name a registry ROW directly and bypass that seat; `tally` is the reason the seat exists at all (a ledger BUILDS its ramp from a theme token), so a mechanism that hardcodes a row cannot be worn by a language that builds one. **Cosmetic to render today, byte-identical if done right** — five call sites, one increment. **Revisit when the meter family is next opened.** |
| 40 | **`plot`'s zero COLUMN draws nothing** — the same law-4 claim as #37, on the mechanism the ramp cure does not reach | **CLOSED — sixty-second pass, and the item's own count was wrong** | Cured in `Kit.plot`'s `else` branch: a zero column stands on `COVER_RAMPS["blocks"][0]` (`░`), the track `_meter_blocks` draws one row above, reached only when the column's eighths total is zero. **The item said FOUR branches printed air; measured across all twelve mechanisms (`_p62_prove.py` §3) it was ONE.** `boxed`, `dotgrid` and `decay` — three of the four it named — draw their unlit lattice down the WHOLE column, which is the opposite defect if it is one at all; six others already stood on a baseline; only `blocks` (nord's) drew h rows of nothing. Censused as `FULL_COLUMN`, two-directional, +24 checks. Moved **2 of 10** nord plot fixtures and nothing else. M5 reverts it, 2 reds; M4 widens its census by hand, 1 red. **The pass-61 diagnosis below is kept verbatim and its four-branch count is superseded by this row.** |
| 40d | **the pass-61 diagnosis, kept verbatim** | **CLOSED with #40** | `plot`'s per-row branches decide lit/unlit per ROW — a boolean, not a coverage — so they never route through the ramp, and #37's cure does not touch them. Six branches already print a baseline for a zero column (`step` a `▁` rail, `tally` and `dimension` a `·`, `hairline` its `─`, `gradient` a `▒` shoulder, `odometer` a literal `0`); **`blocks`, `boxed`, `dotgrid` and `decay` print air**, so `plot([0,0,0,0], 8, 4)` in nord is four rows of spaces — measured, `_p61_prove.py` §3. **This is a different seat, not a leftover**: curing it means giving `plot` a BASELINE ROW concept, which is a mechanism decision per language (does a drawing's chart stand on a rule or on nothing?) and would move the plot half of every kit signature. #37's increment moved 66 spark cells and **zero** plot cells, and keeping it that way is what made the diff scope readable. **Revisit when the plot mechanism is next opened**, or with #39 (both are "the row branches are a second quantiser family"). |
| 41 | **Two METERS carry the exact defects just cured on the ramps** — `_meter_lcd` repeats a glyph in tone alone, `_meter_gradient`'s track is air | **CLOSED — sixty-second pass** | Both cured at the seat, plus a THIRD the census found rather than predicted. `_meter_lcd`'s ghost is now `░░` — the pair NAMED from `COVER_RAMPS["lcd"]`, the same two glyphs `plot`'s lcd branch already drew — so corgi's bar stops being **byte-identical at 0%, 38% and 100% with the colour stripped**, which is DATAVIZ law 1's named case in its most complete form. `_meter_gradient`'s track is the phosphor row's own `░`, its shoulder narrows to two cells (the third step IS the track) and **draws nothing at all at zero**, because a fade out of an empty run is a phantom reading. `_meter_decay`'s persistence tail no longer reaches the track's glyph: it was four cells, so its dimmest `░` was the track in a brighter tone — a HOLE in the run in greyscale — now `▓█` above an `▒` trace, monotone in ink across all three tones. **A 4-instrument census over all 12 mechanisms (+48) plus 13 named laws; 12/12 clean POST, 3/12 red PRE.** Moved **4 of 5** corgi meter fixtures and 20 of 120 on the mechanism grid. Six mutants, all caught. **`decay` and `gradient` are worn by no shipped language** — cured and measured, but reaching no screen today. |
| 41d | **the pass-61 diagnosis, kept verbatim** | **CLOSED with #41** | `_meter_lcd` draws `'▄▄ ' * n` in the theme's `screen` and `'▄▄ ' * (segs - n)` in `dim`: **lit and ghost are the same glyph separated only by TONE**, which is DATAVIZ law 1's named case verbatim — the *spark* half of it is what #38 just cured, and the meter half has been live the whole time at a seat no ramp law runs over (the meters do not route; pass 60's routing table says so and asserts it). `_meter_gradient` ends its bar with `' ' * (bar_w - n - len(shoulder))` — the unrun track is literally spaces, which is law 4 at a meter. **Neither is reachable from `COVER_RAMPS`**, so this increment's laws cannot see them and did not claim to. The cure for the first is corgi's own ghost (`░░`, already in `plot`) or a shorter unlit segment; for the second it is `░`, which is what `_meter_decay` beside it already does. **Revisit as one increment over the METER family** — it is the same argument this pass made about ramps, applied to the mechanism next door, and it will move ten meter renders. |
| 42 | **`hero.py:107` cites a ramp literal that no longer exists** — the comment says level rides on SHAPE "(`' ▂▅█'`)" and the ramp is `'░▂▅█'` | **CLOSED — sixty-second pass** | One line. `hero.py` joined that pass's budget for this line and nothing else; the code was always correct (`hero.py` calls `kit.spark`, so the ramp reaches it) and only the prose was stale. |
| 43 | **The meter's FLOW / LOAD row is censused but not governed** — the bar row has four laws, the second row has none | **CLOSED — sixty-fourth pass. THREE DEFEND, ONE IS CURED — and the item's own count of four was a claim, not a census** | **The instrument #43 cites reports ONE, not four.** Pass 62's `collisions` drops letters and figures on law 5's authority; the four exist only under an alnum-INCLUSIVE reading the item DESCRIBED and never ran. Both readings are now asserted, because which is right IS the question. **The discriminating rule, one sentence:** a tone collision on a flow row is a DECLARED IDIOM when both sides state the SAME datum (a FIGURE — law 5) or when one side is CHROME that delimits rather than measures; it is a DEFECT when a LEVEL MARK collides with something that is not a level. **`dimension` DEFENDS** — `├┤` bound every span in both tones and the quantity is the span's LENGTH plus the figure standing on it. **`lcd` DEFENDS** — its collisions are entirely digits, and the channel index is walled by brackets that never appear around a count. **`odometer` DEFENDS** — the digits ARE the datum, the solari precedent. **`step` IS CURED**: its levels were `. o O` and its own caption is the word `flow`, so the colour-stripped row carried **five ramp marks for four buckets** — a phantom datum, `gradient`'s phantom shoulder wearing letters. **The collision was the symptom; the disease was a PRIVATE alphabet** — `. o O` is darkside's MOTION family (`SPIN`, the `PHASES` doodle) while the registry already names `▁▂▄█` as this language's coverage ramp, which its own `spark` draws. The row now reads that row's `[0] [2] [3]`, its unlit is the mark the bar one row above draws for an unrun cell (pass 61's rule, verbatim), and **no level is a letter, so no caption this row could ever carry can collide with its data**. New instruments: the flow-row reader, the RAMP-SCAN (ramp marks in the row vs buckets drawn), the two-reading census with SEMANTIC per-glyph exemptions, and `hairline`'s missing row DECLARED rather than silently passed. **+75 checks; 12 renders moved, every one named; six mutants, all caught.** |
| 24 | **The prototype's `t` tooltip named SEVEN languages** while `themes.ORDER` had ten | **CLOSED — forty-eighth pass** | Fixed as the rider on the component track's first touch of `app.py`, and fixed the way the legend law demands: the tooltip is now **DERIVED** — `" / ".join(TH.ORDER)` — so it cannot drift again when language eleven lands. |

**Note on #10 — why the settle extension was attempted and declined.** Pass 46 suggested extending
condition C to `.col-head` and `.kb-empty` because they compose from `build()`'s `avail`. The
extension was read for, and does not fit, for three measured reasons:

- **There is nothing to ask.** Condition C works on `TaskCard` because a card OWNS
  `render_card()` — a self-contained recompute that reads its own `self.size.width`, so the shadow
  render can ask "what would you draw now" with `update` intercepted. `.col-head` and `.kb-empty`
  are bare `Static` instances: their string was computed by `KanbanBoard.build()` and the widget
  keeps no reference to the kit, the phase name, the count or the seat.
- **Asking it would mean duplicating the renderer.** The harness would have to re-derive all three
  branches' width arithmetic — `avail - 1` (sections), `max(6, master_w - 3)` (split),
  `max(6, cw - 2)` + `weighted_widths` (columns) — inside the check. That is magic numbers and
  duplicated render logic in the oracle, which is exactly what pass 46 refused; the one time an
  assumption about kit padding was baked into a check it produced **158 false mismatches in a
  perfectly settled state**.
- **The failure mode is not even the same one.** A card goes stale against ITS OWN seat because it
  re-renders itself after layout. A head can only be stale against a stale BUILD (`avail` taking
  its pre-layout fallback), which `on_resize`/`_built_w` already cures at the source and which
  condition B would see as a frame that keeps changing, not as a static wrong one.

A grooming pass must not introduce risk, so this was left un-extended and `verify_language` stood
at **2178, unmoved** — until the forty-eighth pass, below.

---

## SIXTY-SIXTH PASS — THE ORACLE SWEEP — **three passes had each found ONE law that could not fail, by accident, while doing something else; this one asked all 1508 the same question on purpose and the answer was 52 constructs at 34 sites, none of which is a missing red — each is the rest of the file unspoken**

**What this pass is.** Passes 61, 63 and 65 each caught a standing law that could never go red — a law
reading a glyph out of a comment, a MONOTONE law sweeping a re-typed copy of the arithmetic, a floor
that lived in three places. Every one was found sideways. **A base rate of roughly one vacuous law
per pass in a suite of 9807 is a backlog, not a finding**, and the only move that converts an
accident rate into a finished job is to ask every law the one question — *what input makes this
red?* — mechanically.

`prototypes/out/_p66_sweep.py` is that instrument and **it stays**, documented at the top with when to
re-run it: before closing any pass that added laws, after any refactor that moves a seat out of
`taskboard/`, and whenever a law is NARROWED to make a red go away.

### THE SWEEP TABLE — six shapes, each with a precedent in this suite

| shape | precedent | hits | FIXED | FILED | what the detector could SEE |
|---|---|---|---|---|---|
| **1** oracle calls the seat | pass 53 defect 3 | **20** | 0 | 0 — all legitimate | 56.2 % of sites (only comparisons can have it) |
| **2** law sweeps a re-typed copy | pass 63's `_pure`; pass 65 M1/M6 | **0** | — | — | 100 % of expressions, BOTH trees |
| **3** law RAISES instead of reporting | passes 52 · 53 · 55 · 64 | **52 at 34 sites** | **52** | — | 100 % of sites, statically |
| **4** source law a comment walks around | pass 61; pass 65 (twice in a day) | **0 vacuous / 21 latent** | 1 renamed | 21 latent | 1.7 % of sites (only source laws) |
| **5** census that cannot fire | pass 58's `len>=2`; pass 65 M1/M5 | **1 of 24 sampled** | 0 | **#48** | **NOT SWEPT** — sampled at N=24 over 58.3 % |
| **6** subject not in the expression | the dev-flow C-40 shape | **0** | — | — | 37.5 % of sites (per-subject laws in loops) |
| — | the same disease, different cure | **45 at 23 sites** (`[0]` on possibly-empty) | 0 | **#47** | 100 % of sites, statically |

**SHAPE 3 IS THE WHOLE HARVEST AND IT WAS FIXED FULLY.** `.index` where `find` was meant, `.rindex`,
and `next()` with no default — in a law's CONDITION, in its `detail` (evaluated on every call, pass
or fail, and the easier one to write because it reads like a print statement), and in every helper
and setup line between them. Two shared seats replaced all 52: `at(hay, needle, last=False)` returns
-1 and never raises; `first_of(it, default=-1)` is `next` that cannot end a file.

### THE DETECTORS' OWN HONESTY, because a sweep is an instrument and instruments lie

**THE SHAPE-2 DETECTOR CARRIES A PLANTED CONTROL.** It reports zero, and a detector that reports zero
reads exactly like a clean suite. So an alpha-renamed copy of `coverage_index`'s clamp — pass 63's
defect, re-typed the way pass 63's was — is planted and must be SEEN. The suite asserts that control
as a standing law: `sweep: ... and the shape-2 detector is not blind`.

**THE COVERAGE FRACTIONS ARE PRINTED BECAUSE A DETECTOR THAT READS 1.7 % OF THE SUITE AND FINDS
NOTHING HAS FOUND NOTHING ABOUT THE OTHER 98.3 %.** Shape 4 resolves source variables by ASSIGNMENT,
so a law reading source through a helper's return value is invisible to it, and the sweep says so in
its own coverage statement rather than in this file.

**AND THE INSTRUMENT'S OWN TWO BUGS ARE IN ITS SOURCE, NOT SMOOTHED OVER.** Its comment stripper
first rebuilt files by joining token strings, which drops the whitespace BETWEEN tokens — so
`COVER_RAMPS = {` came back as `COVER_RAMPS={` and it reported **eleven** laws as "satisfied by
prose" when four were reading real code. Then it blanked ALL string tokens, which turns
`COVER_RAMPS["eighths"]` into `COVER_RAMPS[         ]` and cost three more. Prose is COMMENTS and
DOCSTRINGS; an inline string literal is the argument a seat is called with. **An instrument that
calls a green law vacuous is worse than no instrument**, and both drafts were caught by hand-checking
the hits against the source rather than by reading the output.

### THE MUTATION BATTERY — two arms, and ARM B is the argument

| mutant | what it does | PASS | FAIL | verdict line | verdict |
|---|---|---|---|---|---|
| M0 baseline (cured tree) | — | 9810 | 0 | YES | GREEN |
| **M1a** swiss masthead spacing GONE | `" ".join(name.upper())` → `name.upper()` | 9799 | **11** | YES | **CAUGHT** |
| **M1b** ... the KIT law reverted to `.index` | the same mutant, PRE-sweep | 8242 | **0** | ***NO*** | **DEAD RUN — as predicted** |
| M2a instrument axis ORIGIN never drawn | `cells[1] = (self.AXIS, tk)` | 9216 | 3 | NO | reds, then **#47** killed it |
| M3a blueprint span field code renamed | `"span"` → `"spn"` | 8598 | 3 | NO | reds, then **#47** killed it |
| **M3b** ... the bare `next` back | the same mutant, PRE-sweep | 8598 | 3 | ***NO*** | **DEAD RUN — as predicted** |
| **M4** a raw `.index()` back in ONE law | code untouched, no render change | 9809 | **1** | YES | **CAUGHT** — the standing law |
| **M5** the sweep instrument DELETED | code untouched | 9807 | **3** | YES | **CAUGHT** |

**M1b IS THE PASS.** Same mutant, same tree, one law reverted to the form the sweep replaced: **8242
PASS, 0 FAIL, no verdict line.** On any mutation driver that reads FAIL counts, that is
indistinguishable from "no law catches this" — and 11 reds is what the cured tree says about the
identical defect.

**THE MUTANTS HAD TO BREAK A DRAWING SEAT, NOT A CONSTANT, and the first draft did not.** Mutating
`ORIGIN = "├"` moves the render and the law's needle TOGETHER — `ki.ORIGIN` is read from the same
class that draws it — so no law could fail and the mutant would be vacuous, which is the thing a
prover exists to refuse. Every app-code mutant here breaks a seat that DRAWS.

**M2a AND M3a ARE NOT FAILURES OF THIS PASS, THEY ARE #47's EVIDENCE.** Both reached their reds —
including, for M2a, one of this pass's own cured laws going red instead of raising — and then died
at a `[0]` on a possibly-empty sequence further down the file. **The filed remainder is measured,
not assumed.**

**AND M5 CAUGHT A DEFECT IN THE NEW LAW'S SECOND LINE.** The first draft bound `_sweep =
module_from_spec(...)` BEFORE `exec_module`, so a deleted instrument left a non-None EMPTY module:
the presence law went red correctly and the trap law then died on `AttributeError`, taking the run
with it. **The law that exists to say "a raised law reports nothing" had that exact defect.** Cured
by binding after the exec and by `hasattr` on the read; M5 now reports 3 reds and reaches the verdict
line.

### THE SUITE NOW HAS A LAW ABOUT ITSELF, AND THE DETECTOR IS IMPORTED RATHER THAN RE-TYPED

Three checks at the tail of `verify_language.py`, +3 on the count:

* **the sweep is present and runs** — its existence is part of the CONDITION, so a missing
  instrument REDS instead of skipping (VERIFY.md's rule, and M5 is it run);
* **the named trap is ZERO** — no law and no setup line in the file can raise where it should go red;
* **the shape-2 detector is not blind** — the planted control, asserted here rather than trusted.

**Re-typing the trap census inside the suite would BE shape 2** — a law sweeping its own copy of the
thing, which the mutation cannot reach. One definition, imported, exactly as pass 65 imported pass
62's prover.

### WHAT WENT RED ON THE WAY, AND HOW

* **`first` was already a local in two law bodies.** The helper shadowed it and the run died at 8850
  checks with `TypeError: 'str' object is not callable`. Renamed `first_of`. A helper a section can
  shadow is a helper that fails nine thousand checks into the run.
* **`at()`'s own first draft used a GUARDED `.index`.** Correct — and it forced the standing law to
  carry an EXEMPTION for two lines of its own file, which is the shape a maintainer widens to make a
  red go away. Rewritten with no `.index` at all; the law has no exemptions.
* **One law was renamed, not narrowed.** `cover/rider: the motion channel list is TWO, not three` is
  satisfied by a COMMENT — correctly, the comment IS its subject — but its name read as a law about
  code, so the shape-4 detector called it vacuous. It is now `the module comment enumerating the
  motion channels says TWO, not three`. **The law did not change; the name now says which of the two
  things it is.**

### THE HAND-AUDIT SAMPLE — shape 5, and why it is sampled and not swept

Deciding whether a predicate can take the other value is not decidable from the tree, and the sweep
does not pretend it is. **Selection rule, stated so it can be re-drawn identically:** the sections
whose banner carries no pass-48-or-later attribution (the component contract began at pass 48 and the
vacuity discipline with it) are the PRE-DISCIPLINE sections — **48 of 62, holding 879 of 1508 sites
(58.3 %)**. From those, **N = 24 drawn with `random.Random(66)`**, a fixed seed, so a later pass
extends the draw rather than re-rolling it.

**Result: 21 of 24 can go red on an input a maintainer would recognise. One cannot** (#48). Two more
(`pen not in calm_page`, `RAIL not in "\n".join(...)`) are anchored only by sibling positive laws and
assert nothing about their own non-emptiness — named in #48 for whoever takes it.

### DIFF SCOPE

**`taskboard/` WAS READ-ONLY THIS PASS and no app file was opened**, so zero renders moved by
construction — measured anyway: 308 language-grid strings and 120 mechanism-grid strings,
`cmp`-clean against pass 65's POST. The mutation battery writes to `taskboard/language.py` and puts
it back, and its last line re-reads every file it touched and asserts byte-identity plus that the
renamed-aside sweep is back. `tree clean: YES` on every chunk.

**9807 → 9810 (+3), all three the suite's law about itself; the other five suites did not move by one
check** (208 · 97 · 22 · 12 · 137).

**BUDGET, STATED BECAUSE IT WAS EXCEEDED BY ONE.** The pass was bounded at ≤12 suite runs beyond the
final 3×. Thirteen were spent: two shakedowns, eight battery arms, one re-run of M1b after the first
arm B was found to prove nothing, one re-run of M5 after its defect was cured, and one over. **The
thirteenth is the M5 re-run and it is the one that must not have been skipped** — shipping a law
whose red path had failed once and was then edited would be exactly the "tests pass" claim this
project refuses.

### SUITES AT CLOSURE — three back-to-back full runs

| suite | checks | sixty-fifth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9810** | 9807 | ALL PASSED (×3) |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (×3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (×3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (×3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (×3) |
| `python -m pytest tests -q` | 137 | 137 | **137 · 137 · 137** — no flake this pass |

**`test_win_clipboard_roundtrip` passed in all three rounds and that does NOT close #22.** The
machine was quiet; fourth pass in a row it has held, and the item stays open for the reason it always
has. **THE CAPTURE RACE DID NOT FIRE** — zero `settle timeout` lines across three suite runs and
thirteen battery runs. Not claimed cured.

### WHAT THIS PASS DID NOT DO

* **It did not cure the `[0]` class.** That is **#47**, it needs a per-site sentinel that makes each
  law red rather than merely not-raise, and thirty of those in one increment is un-reviewable.
* **It did not touch the one sampled shape-5 law.** That is **#48** — a one-line fix, filed because
  the sample exists to estimate a rate and not to be cured mid-pass.
* **It did not narrow a single law to make a red go away.** One was renamed; none was weakened.

### NEXT

**#47, and it is now the sharp one.** Two of this pass's five arm-A mutants died on it, in the cured
tree, after reporting their reds — so the suite's ability to finish a mutated run is bounded by a
class that is fully censused with addresses and has no shared cure. Twenty-three sites, each needing
a sentinel chosen to make ITS law red; that is an increment, and it is the last structural obstacle
to a mutation battery that can be trusted to report rather than to die.

**The exemplar (#3) is the alternative and it is a better bet than it was.** The argument against it
last pass was that an exemplar written before the oracle sweep would be an exemplar of a suite
containing an unknown number of laws that cannot fail. That number is no longer unknown: it is 45
constructs of one shape, censused, plus one sampled law. **#47 first, then the exemplar.**

---

## SIXTY-FIFTH PASS — THE LAST TWO GOVERNANCE REMAINDERS (#45 + #40d) — **zero cells moved, and that is what made the pass necessary: the two defects it cured were invisible to every snapshot, every greyscale law and both signature grids, so nothing but a law could ever have seen them**

**What this pass is.** #45 and #40d's remainder were the last two seats in the data-viz family that
answer a governed question without going through the seat that governs it. Both cures are
**byte-identical** — 308 language-grid strings and 120 mechanism-grid strings, `cmp`-clean against
pass 64's POST — and that is the whole problem with them: **a cure that moves no render is
indistinguishable from a comment unless something can fail when it is undone.** M1 and M5 are that
something, and both are byte-identical mutants that only this pass's laws catch.

### THE VERDICT, BOTH ITEMS

**#45 CLOSED.** Five `_meter_*` functions named a `COVER_RAMPS` row directly. Measured before
anything was edited (`_p65_prove.py` §0): the seat returns the named row at **every one of the 13
kit/mechanism pairs** those five are ever drawn on — the shipped languages that wear them plus the
two hosts the mechanism grid uses. **Zero divergences**, so the cure is hygiene and not a render
change. The argument for doing it anyway is that a row named inside a mechanism is `cover_ramp()`'s
dispatch **re-typed by hand**, keyed on the same `meter` token: a language that changed mechanism
would move its spark and leave its meter behind, and nothing in a 9725-check suite could see it.

**#40d CLOSED, and the census answered a different question than the item asked.** The item reads as
"`plot`'s per-row branches decide levels through neither quantiser". Measured, **not one per-row
branch decides a level.** Every branch is handed `v` — the column's height — and decides only
lit/unlit against its own row index, which is the boolean the skill's refusal table already blesses.
**The level is decided ONCE per column, ABOVE the branches — by a re-typed copy of `coverage_index`,
in three places.** That is DATAVIZ law 3's named defect at its own seat, and the sentence law 3 uses
to appoint that seat was **false for `plot`**: "one copy means spending the floor reds this law in
every language at once" — each inline copy carried its own `max(1, ...)`, so the floor was safe by
being in three places rather than by being in its seat. **M6 is that sentence, run: 40 reds.**

**Fourth item in a row whose own description was a claim rather than a census** — #40's four
air-printing branches were one, #39's two band seats were three, #43's four collisions were one, and
#40d's "branches that decide levels" are zero.

### THE FINAL CENSUS — the family is fully governed

Every seat that decides a LEVEL or answers WHICH RAMP, and what governs it now:

| seat | decides | governed by |
|---|---|---|
| `Kit.spark` | 4-level coverage | `coverage_index` + `cover_ramp()` (pass 60) |
| `Kit.plot` — column height | `h` levels | **`coverage_index`** (this pass) |
| `Kit.plot` — braille sub-rows | `h*4` levels | **`coverage_index`** (this pass) |
| `Kit.plot` — blocks eighths | `h*8` levels | **`coverage_index`** (this pass) |
| `Kit.plot` — the 12 per-row branches | lit/unlit vs `pos` | a 2/3-level row cut, **audited by law** (below) |
| `Kit.plot` — lcd pair · blocks baseline · braille `off=` | which ramp | **`cover_ramp()`** (this pass) |
| the 5 `_meter_*` seats | which ramp | **`cover_ramp()`** (this pass, #45) |
| `naught.dot_heat` · `_meter_braille` flow · `_meter_step` flow | 3-level band | the band quantiser, **compliant by measurement** (pass 63, #39) |
| `Kit.plot` — the partial TOP CELL | 8 sub-levels | **`eighths` — a NAMED REFUSAL**, measured |
| `Kit.head` — the count bucket | a count | **a named refusal** (pass 60): a count is not a coverage |
| `_pulse` | 9-level coverage | `eighths`; a module function with no kit to ask |

**The two refusals are asserted as DIFFERENCES, not merely stated.** Routing the partial top cell to
`cover_ramp()` would move cells (3/8 draws `▃` on `eighths` and `▂` on nord's own ramp), so the law
pins the disagreement — a maintainer who "finishes the routing" reds before they touch a render.

### THE AUDIT — 12 of 12 per-row branches lawful, and the declaration was wrong by one

Each branch held to the legs a routed ramp is held to, every one read **off the rendered string**
(pass 63's finding kept: a law that sweeps a re-typed copy of the arithmetic is not a law about the
mechanism; the model survives as exactly ONE law, the equality).

| leg | result |
|---|---|
| INJECTIVE — the 5 levels draw 5 DISTINCT columns, colour stripped | 12/12 |
| MICROBAR FLOOR — level 1 does not draw level 0 | 12/12 |
| MONOTONE ink (fill family) | 10/10 |
| MARK family (declared) — ink FLAT, the mark MOVES | 2/2 |
| DETERMINISTIC — 50 renders are one string | 12/12 |
| no DOUBLE-WIDTH glyph | 12/12 |

**The mark family was declared with three members and the measurement sent one back.** `dimension`
*looks* like a mark family — one `─` at the measured height, never a filled column — but it stands
that mark on a **leader of dots that grows with the level**, so its ink is strictly monotone and it
belongs with the fills. The declaration was mine, it was a claim, and the census is what made it a
fact. The census is written `(measured) == (declared)` so it bites both ways: **M4 adds `dimension`
back, code untouched, and takes two reds.**

### THE TWO-UNLIT VERDICT: **DECLARED**, and the argument is an identity rather than prose

`_meter_braille` draws `⠒` as the bar row's unlit and the registry's `⠐` as the flow row's — two
unlit glyphs one row apart in one mechanism, which is the #45 disease's exact shape. **It is not the
disease. The two rows are two RESOLUTIONS of one idiom.** The bar is a HALF-CELL fill (`⣿` fills both
sub-columns of a cell, `⡇` only the left), so it addresses **two** sub-columns per cell, and a track
that inks one of them leaves the other drawing nothing at the very scale the bar can fill. The flow
row draws one bucket per cell, undivided, so **one** dot is its empty.

**Checkable rather than rhetorical, which is the whole point:** the bar's unlit **IS** the flow row's
unlit mirrored into the other sub-column — dot 5 `|` its mirror dot 2 `==` dots 2+5 — asserted as an
identity, with a control that shows the identity is false for a different unlit. Prose is what tied
the registry to this meter for three passes (#44); an identity cannot drift.

**Both clear law 4's two ceilings**: 0.250 and 0.125 ink against a quarter-cell limit.

**AND THE ARGUMENT PRODUCED A DEFECT IT DOES NOT CURE.** By the same rule, the half cell `⡇` should
carry the right sub-column's track dot — that sub-column is unrun — and it carries **zero** dots
there, so the one cell where the run ends is the one cell whose empty sub-column draws nothing. It
moves shipped cells, it is a different claim from "which unlit", and it is filed as **#46** rather
than smuggled into a hygiene pass. **M3 is the proof the verdict is load-bearing: taking the other
reading (one mechanism, one unlit) reds two laws and — the finding — reds NOTHING pre-existing,
because no snapshot in 9725 checks was pinning the braille bar's track glyph at all.**

### THE MUTATION BATTERY — six, all CAUGHT, none crashed

| mutant | what it breaks | FAIL | of which pass-65 | pre-existing |
|---|---|---|---|---|
| M0 baseline | — | 0 | — | — |
| M1 a BYPASS restored (**byte-identical render**) | the #45 seat law | **1** | 1 | **0** |
| M2 a PINNED plot branch saturates | injectivity + monotone + the census | **3** | 3 | **0** |
| M3 the TWO-UNLIT verdict taken the other way | the mirror identity | **2** | 2 | **0** |
| M4 a CENSUS widened UNEARNED (code untouched) | the mark-family census, both ways | **2** | 2 | **0** |
| M5 the LEVEL SEAT un-routed (**byte-identical render**) | the seat count + the FLOOR drive-check | **2** | 2 | **0** |
| M6 the FLOOR is SPENT at its seat | law 3's sentence, now true of `plot` too | **40** | 2 | 38 |

**M1 AND M5 ARE THE PASS'S ARGUMENT.** Both restore a bypass, both are **byte-identical to the
shipped tree**, and both are caught by **zero pre-existing laws**. A signature compare, a snapshot, a
greyscale sweep and a pairwise law all pass on either of them. That is what "the last two seats were
ungoverned" means as a measurement rather than as a description.

**M6's two pass-65 reds are the FLOOR drive-check and the model equality** — the only two legs whose
inputs cross a 1/32 threshold — and its 38 pre-existing reds are the microbar laws in all ten
languages plus the per-ramp registry legs. Before this pass, spending the floor left `plot` entirely
untouched; the drive-check is what turned that from a source grep into a behaviour.

**THE DRIVE-CHECK IS THE SHARP INSTRUMENT AND IT IS NEW HERE.** A source law can say the copies are
gone; it cannot say the seat is REACHED. The floor leg patches `coverage_index` at the seat, renders
a 1-in-100 column in all twelve mechanisms, and asserts every one of them moved — with a
did-it-actually-run guard beside it, because a patch nothing calls reports the same green. Restored
in a `finally`, so a red cannot leave the module monkeypatched (the pass-64 lesson: a law that
crashes reports no reds at all).

### WHAT WENT RED ON THE WAY, AND HOW IT WAS FIXED — the rule mattered twice

**Two of this pass's own edits reddened standing laws, and both were fixed at the source rather than
by narrowing the law.**

* The two-unlit ARGUMENT, written as a comment inside `_meter_braille`, **spelled `⠐`** — and pass
  64's law says that function's source no longer spells the registry's unlit. The comment now
  states the glyph **by dot number**. A source law a comment can walk around is not a source law
  (pass 61's quote-style finding, one shape on).
* The braille and step comments **spelled `COVER_RAMPS[...]`** in prose, which the new #45 law reads
  as naming a row. The prose now points at the seat, which is what it should have said anyway.

The alternative in both cases was to teach the law to ignore comments. **That is M4's move — a
maintainer widening an exemption, code untouched, to make a red go away — and this pass wrote M4.**

### DIFF SCOPE

**ZERO renders moved, and both grids are `cmp`-clean against pass 64's POST**: 308 language-grid
strings, 120 mechanism-grid strings, **0 movers on either**. Nine call sites changed in
`language.py` (five meter seats, three `plot` ramp seats, three `plot` quantiser copies — the lcd
seat is one site for two glyphs) and every one of them was proven equal before it was written.

**9725 → 9807 (+82) on `verify_language`; the other five suites did not move by one check**
(208 · 97 · 22 · 12 · 137). The +82, counted rather than estimated: **+72** the #40d audit (six legs
× twelve mechanisms), **+4** the #40d family laws (the mark-family census, the seat count, the FLOOR
drive-check and its did-it-run guard, the model equality), **+10** #45 (two legs × five meters
minus the two pass-62/64 naming laws it replaced, plus `plot`'s three-seat law and the `eighths`
refusal), **+5** the two-unlit verdict and its control, **−9** absorbed by laws this pass rewrote
rather than added.

### SUITES AT CLOSURE — three back-to-back full runs

| suite | checks | sixty-fourth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9807** | 9725 | ALL PASSED (×3) |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (×3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (×3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (×3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (×3) |
| `python -m pytest tests -q` | 137 | 137 | **137 · 137 · 137** — no flake this pass |

**`test_win_clipboard_roundtrip` passed in all three rounds and that does NOT close #22.** The
test's verdict still depends on whether another process holds the Windows clipboard; the machine was
quiet. Third pass in a row it has held, and the item stays open for the same reason it always has.

**THE CAPTURE RACE DID NOT FIRE** — zero `settle timeout` lines across three suite runs and eight
mutation runs. The standing watch is not claimed cured; the machine was quiet.

### WHAT THIS PASS DID NOT DO

* **It did not route a single per-row branch.** The skill refuses it and the audit found nothing that
  needed it: lit/unlit per ROW is a boolean, and twelve of twelve are lawful as they stand.
* **It did not cure the half-cell's missing track dot.** That is **#46** — it moves shipped cells and
  it is a design change, not hygiene.
* **It did not touch the partial top cell.** The `eighths` refusal is now measured instead of assumed,
  and that is the whole of what it deserved.

### NEXT

**The oracle sweep, and it is the stronger of the two.** Six passes have now written laws that read
the glass, and three of them (61, 63, 65) each found a standing law that could not fail — the
`len(plot(...)) == h` shape, the re-typed `_pure` copy, the floor that lived in three places. **Those
were found by accident, one per pass, while doing something else.** A sweep that takes every law in
`verify_language` and asks the one question — *what input makes this red?* — is the only move that
converts an accident rate into a finished job, and the mutation harness to run it already exists.
The measured base rate is roughly one vacuous law per pass in a suite of 9807.

**The exemplar is the weaker choice right now** and the reason is this pass: the data-viz family is
the first one in the package that is *finished* — every level-deciding seat governed, every refusal
named and measured, every exemption biting both ways. An exemplar written before the oracle sweep
would be an exemplar of a suite that still contains an unknown number of laws that cannot fail.

---

## SIXTY-FOURTH PASS — GOVERNING THE FLOW ROW (#43 + #44) — **the item said four collisions and the instrument it cited had never reported more than one; three of the four defend themselves, and the one that does not was a symptom of a private alphabet**

**What this pass is.** Pass 62 wrote four laws on the meter's BAR row and left the second row
censused and ungoverned, on honest grounds: telling a declared idiom from a defect needs a
per-mechanism argument, and pass 62 declined to pretend it had made one. Pass 63 built the
instruments. **This pass makes the argument — one verdict per collision — and unlike pass 63 it
moves cells.**

### THE VERDICTS

| mechanism | collides on | verdict | the argument |
|---|---|---|---|
| `dimension` | `0 ├ ┤` | **DEFEND** | `├┤` bound EVERY span in BOTH tones, so they are chrome that delimits and never measures. The quantity is the span's LENGTH plus the figure standing on it (law 5) — `├┤ 00 ├───┤ 02` recovers two spans, two lengths and two values with the colour stripped. |
| `lcd` | `2 4` | **DEFEND** | Every colliding glyph is a FIGURE. The channel index and its count are both STATED VALUES, walled apart by brackets that never appear around a count: `[1]4 [2]0 [3]2 [4]2`. |
| `odometer` | `0` | **DEFEND** | The solari precedent — the digits ARE the datum. The tone only repeats what `00` against `02` already says. |
| `step` | `o` | **CONDEMN — cured** | A LEVEL MARK against PROSE. Its levels were `. o O` and its own caption is the word `flow`, so the colour-stripped row carried **five ramp marks for four buckets**. |

**THE DISCRIMINATING RULE, one sentence and four applications:** *a tone collision on a flow row is a
DECLARED IDIOM when both sides state the SAME datum (a figure — law 5) or when one side is CHROME
that delimits rather than measures; it is a DEFECT when a LEVEL MARK collides with something that is
not a level, because then the colour-stripped row carries more marks than it has buckets and the
extra ones read as data.*

### THE ITEM'S OWN COUNT WAS A CLAIM — THE THIRD IN A ROW

#43 states four tone collisions. **The instrument it cites reports ONE.** Pass 62's `collisions`
drops letters and figures on law 5's authority — right for the BAR row, blind on a row whose level
marks are themselves letters — and the four exist only under an alnum-INCLUSIVE reading the item
DESCRIBED and never ran. Both readings are now asserted per mechanism, because **which one is right
IS the question, and a suite that quietly picks one has decided the thing it was supposed to prove.**
#40's four air-printing branches were ONE; #39's two band seats were THREE; #43's four collisions
were one under its own instrument.

### THE SHARP INSTRUMENT: THE RAMP-SCAN

The reader's position stated as a number. Take the mechanism's own ramp — **read off the glass**, not
declared — and count its marks in the colour-stripped row against the buckets drawn.

| seat | ramp | `[4,0,2,2]` | `[0,0,0,0]` | `[1,1,1,1]` | `[9,1,0]` |
|---|---|---|---|---|---|
| `braille` | `⠐⠶⣿` | 4/4 | 4/4 | 4/4 | 3/3 |
| `step` PRE | `.oO` | **5/4** | **5/4** | **5/4** | **4/3** |
| `step` POST | `▁▄█` | 4/4 | 4/4 | 4/4 | 3/3 |

**And the space is not the boundary a reader can trust:** FIVE of the twelve flow rows put spaces
INSIDE the data run (`dimension`, `dotgrid`, `lcd`, `odometer`, `tally`), so "the run is the first
space-free token" is not a rule this family supports. Measured, not asserted.

### THE CHEAP CURE WAS TRIED FIRST AND A STANDING LAW KILLED IT

`o` → `◦` moved ONE level and was a three-string diff — the minimal cure DATAVIZ law 1 asks for. **It
went red: `◦` is `NA.OFF`, naught's own unlit pixel, and a standing law forbids any other language's
BOARD from drawing naught's lattice marks** ("darkside: board carries no dot lattice"). That law's
BODY is stronger than its NAME (it excludes one instance of a codepoint, not a lattice), and
narrowing it to admit this cure is precisely the move pass 62's M3 mutant exists to catch, one level
up: **a maintainer widening an exemption, code untouched, to make a red go away.** The law stood and
the cure moved.

**AND THE BIGGER ARGUMENT CAME OUT OF THE REFUSAL.** Hunting for a mark that was darkside's own and
nobody else's led to the registry, which **already names this language's data ramp** — `▁▂▄█`, drawn
by its own `spark`, dispatched on the same `meter` token. **The row had a PRIVATE alphabet borrowed
from the SPINNER, and the tone collision was the symptom rather than the disease.** `. o O` is
darkside's MOTION and IDENTITY family (`SPIN`, the `PHASES` doodle, the port `(o)`); the flow row is
DATA, so it now reads `[0] [2] [3]` off the declared row. Its unlit is the mark the bar one row above
already draws for an unrun cell — **pass 61's rule verbatim, one mechanism later** — and **no level
is a letter, so no caption this row could ever carry can collide with its data.** A caption rename
would have cured `flow`; this cures the row.

**M5 IS THE PROOF THAT THE DISTINCTION IS LOAD-BEARING.** It takes the cheap cure — glyphs back,
caption renamed to a word with no `o` — so **every law about the SYMPTOM goes green** (no collision,
RAMP-SCAN exact) and **fifteen laws still red**, all of them about the disease: the ramp is a letter
alphabet, it is not the declared row, its unlit is not the bar's mark.

### THE BATTERY FOUND THREE OF THIS PASS'S OWN LAWS UNABLE TO REPORT THEIR FAILURE

**Three mutants CRASHED the suite before they were caught**, and a run that dies reports no reds at
all — indistinguishable from a mutant nothing catches. All three were laws that RAISED instead of
returning: pass 63's seat readers did `ramp.index(glyph)` (ValueError on a moved seat), its preimage
law did `_pre[0]` (KeyError when level 0 is unreachable), and this pass's own named laws did
`set(flow_ramp(...))` (TypeError when the ramp collapses to two glyphs). **M1 took the run down at
7591 checks with one red printed; after the fix it prints 23.** Same lesson as pass 63's vacuous
MONOTONE, found the same way — by the battery, not by review.

### THE SIX MUTANTS

| mutant | what it breaks | FAIL | of which pass-64/63 |
|---|---|---|---|
| M0 baseline | — | 0 | — |
| M1 the condemned cure is reverted | every law about `step` | **23** | 23 |
| M2 a defended exemption widened UNUSED | the census itself, code untouched | **2** | 2 |
| M3 the #44 naming is reverted | the naming law — **the value law cannot see it** | **4** | 4 |
| M4 the census weakened to the SHIPPED cut | the alnum-inclusive reading | **6** | 6 |
| M5 the CHEAP cure taken instead | the laws about the DISEASE, not the symptom | **15** | 15 |
| M6 the unlit made HEAVY | law 4's opposite half | **13** | 13 |

All CAUGHT, none crashed, restored green at 9725.

### #44 — THE COUPLING TURNED THE RIGHT WAY ROUND

`_meter_braille`'s flow row reads `ramp[0]` and `ramp[3]` off `COVER_RAMPS["braille"]`; the middle
stays `⠶`, this row's own, because a 3-level flow row on a 4-level coverage ramp is not a copy of it.
The registry comment is rewritten in the right direction — it read *"`⠐` is what `_meter_braille`
prints"*, which is a definition citing its reader. **The pass-63 VALUE law is kept unchanged and is
still the stronger guard**, and M3 proves the split: reverting the naming reds four laws and **not
one of them is the value law**, because the two still agree. **Zero renders moved.** The claim is
exactly as wide as the cure and the suite says so: three other seats still spell `⠐`
(`Instrument.BLANK`, its `radio.main`, `plot`'s `off=`) — the KIT's vocabulary and a third mechanism,
not this family — asserted as four seats with none inside the meter.

### DIFF SCOPE

**12 renders moved, every one named. `braille` moved ZERO** — #44 is a pure naming change.

| grid | moved | who |
|---|---|---|
| language grid (308) | **4** | `darkside\|meter` — all four fixtures that draw a flow row |
| mechanism grid (120) | **8** | `step` on both host kits × the same four fixtures |

The fifth meter fixture (`0, 0, [], 24`) draws an empty flow row and held. **9650 → 9725 (+75) on
`verify_language`; the other five suites did not move by one check** (208 · 97 · 22 · 12 · 137),
three back-to-back runs each, all green. The +75, counted rather than estimated: **+60** the
per-mechanism census (`flow[...]` — four legs over twelve mechanisms, plus the RAMP-SCAN's four
fixtures and two ceilings on the two ramped seats), **+12** the verdicts and the family-level laws
asserted BY NAME (`flow: `), **+3** #44. **The pass-63 band section did not move by one check** (69
before, 69 after) even though two of its three seats were re-anchored and three of its readers were
made unable to crash — the restatements replaced laws one for one, which is what a re-anchor should
cost.

### WHAT THIS PASS DID NOT DO

* **It did not route anything.** #39 stays closed on pass 63's terms.
* **It did not narrow the naught-lattice law**, which is what the cheap cure needed. The red was
  real and the law won.
* **It did not move the meter family onto `Kit.cover_ramp()`.** Five `_meter_*` functions name a
  registry ROW directly and bypass the one seat that is documented to answer that question — filed
  as **#45** rather than fixed mid-increment, because pass 62 set the convention this pass followed.

### NEXT

**#45, the `cover_ramp()` seat**, if a hygiene pass is wanted: five call sites, byte-identical if
done right, and it is the last place the data-viz family has two answers to one question. **The
design alternative is `plot`'s per-row branches** (#40d's remainder) — the last family that decides
levels without either quantiser.

---

## SIXTY-THIRD PASS — THE NAUGHT QUANTISER AUDIT (#39) — **the exemption was never measured, it was priced; and the item that granted it named two seats when there are three**

**What this pass is.** Passes 61 and 62 CURED. This one JUDGES. Pass 60 built the coverage primitive
and deferred the band-threshold seats on render-risk grounds — *"routing would move cells"* — which
is a statement about the cost of curing, not about the conduct of the thing exempted. Three passes
later that sentence was still the only thing standing between `naught.dot_heat` and the law. **The
mandate was to settle #39 by LAW, whichever way the evidence fell: no grandfathering, and no
crediting naught for having been praised in earlier passes.**

The routing question is not reopened. Pass 60 rejected routing because it moves real cells on a
shipped surface and that stands. **The question this pass asks is the only one that can settle an
exemption: does the mechanism AS SHIPPED satisfy the laws?**

### THE VERDICT

**COMPLIANT BY MEASUREMENT — routing unnecessary.** Not "naught is fine". The claim is narrower and
checkable: **the un-routed seats satisfy the identical law set the routed ramps are measured by.**

| | leg | A `dot_heat` | B `braille` flow | C `step` flow |
|---|---|---|---|---|
| 1 | MONOTONE index | PASS | PASS | PASS |
| 2 | MONOTONE in ink | PASS | PASS | PASS |
| 3 | GREYSCALE-SAFE, ends differ | PASS | PASS | PASS |
| 4 | THRESHOLD at/under `lo` → unlit | PASS | PASS | PASS |
| 5 | THRESHOLD at/over `hi` → terminal | PASS | PASS | PASS |
| 6 | THRESHOLD, only END indices outside `[lo,hi]` | PASS | PASS | PASS |
| 7 | DETERMINISTIC (50 renders + 3 processes) | PASS | PASS | PASS |
| 8 | MICROBAR FLOOR (law 3) | PASS | PASS | PASS |
| 9 | law-4 unlit carries INK | PASS | PASS | PASS |
| 10 | law-4 track ≤ a QUARTER cell | PASS | PASS | PASS |
| 11 | law-4 unlit is none of the LIT ones | PASS | PASS | PASS |
| 12 | law-1 no index pair repeats | PASS | PASS | PASS |
| 13 | no DOUBLE-WIDTH glyph | PASS | PASS | PASS |

**39 of 39.** The numbers behind them:

| | A `dot_heat` | B `braille` flow | C `step` flow |
|---|---|---|---|
| ramp | `⠂⡀⡄⡇` (the `fine` registry row) | `⠐⠶⣿` | `. o O` |
| ink per level | 0.125 · 0.125 · 0.250 · 0.500 | 0.125 · 0.500 · 1.000 | 0.10 · 0.35 · 0.55 |
| unlit ink (ceiling 0.25) | **0.125** | **0.125** | **0.10** |
| level-0 preimage | exactly `{0}` | exactly `{0}` | exactly `{0}` |
| band preimages over `[0,1]` | 1 / 1320 / 1320 / 1360 | 1 / 2640 / 1360 | 1 / 2640 / 1360 |
| flat-zero row ON THE GLASS | 28 drawn cells | 4 drawn cells | 4 drawn cells |
| divergence vs nearest-index | **1372 / 4001 = 34.3%** | **359 / 4001 = 9.0%** | **359 / 4001 = 9.0%** |

Every level in every one of those rows was read **off the rendered string with the colour stripped**,
at **4009 exact rational coverages** per seat, with the band edges (`0.33`, `0.330001`, `0.66`,
`0.660001`, `1e-9`, `0`, `1`) landed on exactly — a sweep that steps over `0.33` says nothing about
the boundary that decides the level.

### THE ITEM NAMED TWO SEATS AND THERE ARE THREE

`_meter_step`'s flow row is `"O" if x > (hi or 1) * 0.66 else ("o" if x else ".")` — the same 3-level
band quantiser as `_meter_braille`'s, wearing `. o O`, shipping in darkside. **#39 never listed it.**
Pass 62 *did* see the row — it is written into item #43, where `step`'s flow glyph `o` is noted
colliding with the letter `o` in its own label — **and read it as a tone-collision case rather than
as a member of the quantiser family.** The census now counts the SOURCE for the band constants, so a
fourth seat reds (M4 proves it) and a deleted one reds too.

### WHY C WAS INVISIBLE: THE INSTRUMENT COULD NOT WEIGH IT

`mink` returns **1.0 for any letter**, and it is right to — a printed FIGURE is a full cell of stated
value (DATAVIZ law 5), which is how `odometer` satisfies law 4 without drawing a track. The
consequence nobody had noticed: for a DATA ramp made of letters, `.`, `o` and `O` all weigh exactly
the same, **so no ink law in this suite could ORDER them**. Three declarations, argued on the
existing table's own logic — `·` is one dot at 0.10 so a FULL STOP is 0.10; a hollow mark sits at
0.35 (`▫`) so a small ring is 0.35; a large ring takes the heavy slot at 0.55 (`━`), under the filled
`▪` at 0.60 — are what make C measurable at all. **Kept LOCAL to the section rather than folded into
`_M_DECL`**, because a glyph's weight changing under the pass-62 meter laws to serve this section is
exactly the silent coupling this suite exists to refuse. **A seat whose glyphs the instrument cannot
weigh is a seat no law was ever really applying to** — that, and not the arithmetic, is what the
grandfathering was hiding.

### THE DISAGREEMENT IS A DIFFERENCE, NOT A VIOLATION

#39's entire content was *"they disagree"*. They do — re-measured off the glass, pass 60's three
named cases hold: `c=0.34` band 2 (`⡄`) vs nearest 1 (`⡀`); `c=0.40` band 2 vs nearest 1; `c=0.67`
band 3 (`⡇`) vs nearest 2 (`⡄`). **The record has to say whether that is a defect, and it is not.**
Both quantisers are monotone, deterministic, threshold-honouring and greyscale-separable — measured,
above — so this is a difference in WHERE the levels change. The laws constrain the SHAPE of a
quantiser (ordered, total, deterministic, both ends named); **they do not appoint one band layout.**
Pinned as exact counts so the claim stays a measurement: a band edge moving in either direction reds.

### WHAT THE EXEMPTION RESTS ON, AND THE LAW THAT PINS IT

A's greyscale leg passes on a subtlety worth stating plainly: **`fine`'s levels 0 and 1 are EQUAL in
ink** — `⠂` is U+2802 (dot 2) and `⡀` is U+2840 (dot 7), one dot each. They separate by dot POSITION,
not by dot count, which is precisely what the registry already declares for this ramp.

That tie is lawful **exactly where it is**: at the (unlit, first-lit) boundary — the track/data
boundary — and not between two data levels. And it was **completely ungoverned**. The registry's
monotone law is `a <= b`, its repeat census counts GLYPHS, and its law-4 legs only look at index 0,
so the tie could have been moved to (1,2) — two DATA levels indistinguishable in greyscale — with
every existing law staying green. **That is M6, and it reds exactly one check in 9650: the new one.**

It also settles a question the audit had to answer honestly: since A draws the routed `fine` ramp
itself, **any ink tie in A is a property of naught's declared single-column idiom, already censused
at the registry — not of the band quantiser.** Routing A would draw the identical glyphs. The tie can
never be an argument for routing.

### THE THREE COUPLINGS, MEASURED

* **A cannot fork.** `dot_heat` indexes `NA.FINE`, and `COVER_RAMPS["fine"]` *is* that tuple joined —
  one definition, asserted. The seat that does not route still cannot draw a different ramp.
* **B can.** Its two ends ARE the `braille` registry row's two ends, **spelled as literals rather than
  named** — and the coupling runs BACKWARDS: pass 61 set the registry's braille unlit *from this
  meter* and recorded it in a comment. Written as a **VALUE law** (the ends are EQUAL), which reds
  whichever side drifts; naming would only have caught the meter. Filed as **#44**.
* **"Does not route" is now a measured fact.** The call recorder asserts the three seats reach
  `coverage_to_glyph` **zero** times. The exemption is compliance-based, so what it is an exemption
  FROM had to be asserted too — if somebody routes these seats later, that reds and the record gets
  updated deliberately rather than silently.

### THE BATTERY CAUGHT A LAW OF THIS PASS'S OWN BEING VACUOUS

Six mutants, all CAUGHT, none crashed, restored green at 9650.

| mutant | what it breaks | FAIL | of which pass-63 |
|---|---|---|---|
| M0 baseline | — | 0 | — |
| M1 a band is inverted | MONOTONE at seat A | **6** | 6 |
| M2 determinism broken by `hash()` | DETERMINISTIC, in-process and across | **4** | 4 |
| M3 the level-0 ink is removed (U+2800) | law-4 / the ZERO-INK ceiling | **5** | 2 |
| M4 a FOURTH band seat appears | the family census | **1** | 1 |
| M5 the declared-ink table widened unused | the declaration census itself | **1** | 1 |
| M6 the ink tie moves to a DATA pair | what the exemption RESTS ON | **1** | **1 — and 0 pre-existing** |

**M1's first run is the finding.** It inverted a band inside `naught.py` and **MONOTONE stayed
GREEN**, catching only 3 incidental reds. The reason: the law swept `_pure`, a RE-TYPED copy of the
arithmetic living in the suite, which a mutation to the code cannot reach. **A law that cannot fail
when the mechanism changes is not a law about the mechanism** — engineering rule 9, found by the
battery rather than by review. Every per-seat law now reads the level off the RENDERED string; the
model survives as exactly one law, the equality that keeps it honest. M1 went 3 → 6 reds.

Two of the six attack the audit rather than the code (M4, M5), which is the pass-62 pattern kept: an
exemption defended by laws a maintainer can widen by hand is the same grandfathering one level up.

### DIFF SCOPE

**ZERO renders moved, and that is the verdict rather than a side effect.** The render signature
(`_p62_prove.py --sig`, 307 lines) is **byte-identical** to pass 62's POST — `cmp` clean. **No source
file was opened**: `naught.py` and `language.py` were read, audited and left exactly as they were,
because nothing in them needed curing. `verify_language.py` gained the laws; `PENDING.md` gained the
verdict.

**9581 → 9650 (+69). The other five suites did not move by one check** (208 · 97 · 22 · 12 · 137),
three back-to-back runs each, all green.

### WHAT THIS PASS DID NOT DO

* **It did not route anything.** Pass 60's rejection stands, now on its own merits.
* **It did not cure `_meter_braille`'s spelled ends.** That is #44 — cosmetic, pinned by a value law,
  and outside a verdict increment whose whole claim is that zero cells moved.
* **It did not govern the flow ROW as a surface** (#43 stays open). This pass governed the QUANTISER
  behind three of those rows; the row-level tone-collision question is still per-mechanism argument.

### NEXT

**#43 with #44, as one meter-family increment.** They are the same seats: #43 wants the flow row's
tone-collision census argued per mechanism, #44 wants two literals in `_meter_braille` replaced by
registry names, and this pass just built the instrument that reads flow rows off the glass and
declared the ink for the `. o O` family that #43's sharpest case (`step`'s `o` against its own label)
is made of. **The alternative, if a design pass is wanted instead of a hygiene one: `plot`'s per-row
branches (#40d's remainder), which are the last family that decides levels without either quantiser.**

---

## SIXTY-SECOND PASS — CURING THE METERS (#41 · #40 · #42) — **a bar that is byte-identical at 0% and at 100% with the colour stripped had been shipping for sixty-two passes, and no law could see it because the meters do not route**

**What this pass is.** Pass 61 cured the coverage RAMPS and named the two defects it had found alive
at the mechanism next door. This pass took the same argument to the METER family — and because the
meters do not route through `COVER_RAMPS`, no ramp law could reach them, so the first job was to
build an instrument rather than to write a cure. **The census came first, the cures were chosen from
what it measured, and it found a third defect nobody had predicted.**

### THE CENSUS — 12 mechanisms × 4 instruments, and why it is four and not two

Two defects, but each one splits into a leg that is easy to satisfy and a leg that is the actual
claim. `_p62_prove.py` §0, run PRE and POST:

| instrument | the claim | why the OTHER leg is not enough |
|---|---|---|
| **L1-move** | the bar row RESPONDS to the value colour-stripped, with the printed figure masked | every mechanism STATES its value (law 5), so the ROW always moves — masking the figure is what makes the question about the DRAWING |
| **L1-tone** | no drawn mark appears under TWO tones in the bar row | a bar can move colour-stripped and still separate two of its levels by tone alone |
| **L4-ink** | a flat-zero meter draws ink at all | — |
| **L4-trk** | the track occupies the run's cells: `ink(0%) >= ink(100%)` | "not blank" is satisfied by three shoulder cells against thirty-one spaces, which is exactly what `gradient` drew |

**THE FIGURE HAD TO BE REMOVED FROM THE INK COUNT BEFORE ANY OF IT MEANT ANYTHING.** A right-aligned
`{pct:>3}%` is `'  0'` at zero and `'100'` at full, so the row's ink moves by two cells for reasons
that have nothing to do with the track. The first draft of L4-trk reported **all twelve mechanisms
red**; dropping the tone runs that carry digits took it to three. **An instrument that reds
everything is not a strict instrument, it is a broken one.**

**AND THE INSTRUMENT EXCLUDES LETTERS AND FIGURES FROM L1-TONE ON PURPOSE.** A printed quantity is a
STATED value (law 5), not a level — without that scope `step`'s flow row reds because the glyph for
a low bucket is `o` and the row's label is the word `flow`.

### THE VERDICT — three red, and only two of them were the ones predicted

| mechanism | worn by | L1-move | L1-tone | L4-ink | L4-trk | PRE verdict |
|---|---|---|---|---|---|---|
| blocks | nord | ok | ok | ok | 34/34 | clean |
| boxed | industrial | ok | ok | ok | 34/34 | clean |
| braille | instrument | ok | ok | ok | 34/34 | clean |
| **decay** | *(library only)* | ok | **COLLIDE `░`** | ok | 34/34 | **RED — not predicted** |
| dimension | blueprint | ok | ok | ok | *(no track — declared)* | clean |
| dotgrid | naught | ok | ok | ok | 12/12 | clean |
| **gradient** | *(library only)* | ok | ok | ok | **3/34 AIR** | **RED — #41's law 4** |
| hairline | swiss | ok | ok | ok | 35/35 | clean |
| **lcd** | **corgi** | **AIR/SAME** | **COLLIDE `▄`** | ok | 20/20 | **RED — #41's law 1** |
| odometer | solari | *(figures — declared)* | ok | ok | *(no track — declared)* | clean |
| step | darkside | ok | ok | ok | 34/34 | clean |
| tally | ledger | ok | ok | ok | 25/25 | clean |

**POST: 12 of 12 clean.**

**THE LCD SPECIMEN IS THE WHOLE ARGUMENT AND IT NEEDS NO PROSE.** Corgi's shipped meter, colour
stripped, at three different values:

    PRE                                              POST
    0%   |▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ [  0%]|      |░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ [  0%]|
    38%  |▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ [ 38%]|      |▄▄ ▄▄ ▄▄ ▄▄ ░░ ░░ ░░ ░░ ░░ ░░ [ 38%]|
    100% |▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ [100%]|      |▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ [100%]|

**Three identical bars.** `'▄▄ ' * n + '▄▄ ' * (segs - n)` is `'▄▄ ' * segs` at every value, so the
only thing that moved was the figure in the brackets. That is not a weak reading, it is **no
reading** — DATAVIZ law 1's named case, in its most complete possible form, on a shipped surface.

### THE CURES — five in `language.py`, each argued from a glyph the language already draws

| # | seat | PRE | POST | argued from |
|---|---|---|---|---|
| 1 | `_meter_lcd` | ghost `▄▄` in `dim` | ghost `░░` | **`plot`'s lcd branch already drew `░░` for an unlit stack** — an LCD segment is never black, it is faint — and pass 61 put that same `░` at `COVER_RAMPS["lcd"][0]` for the spark. The meter now NAMES the row (`[0]` ghost, `[1]` lit) instead of spelling a third copy. It still does not ROUTE: a segment is lit or it is not, and **a boolean is not a coverage**. |
| 2 | `_meter_gradient` | track `' ' * …` | track `░` | the `phosphor` row's own unlit — the glyph `_meter_decay` beside it already draws for the same thing. |
| 3 | `_meter_gradient` | shoulder `▓▒░`, **drawn at 0% too** | `▓▒`, and **none at all when the run is empty** | two separate corrections and both are law 4: the shoulder ENDED on the glyph the track now draws (its last step would have vanished into it — two cells now, because **the third step IS the track**), and a fade out of a run of length ZERO is a **phantom reading**. `|▓▒░` against a blank track said "a little" when the datum said "none". |
| 4 | `_meter_decay` | tail `░▒▓█`, trace `▓` | tail `▓█`, trace `▒` | **the census found this one.** The tail was four cells, so its dimmest was `░` — the track's own glyph in a brighter tone, which is law 1 exactly, and in greyscale it put a HOLE in the run: `▓▓▓▓▓▓▓▓▓░▒▓█░░░` reads as a run, a gap, a rise. The tail now starts ABOVE the track and the older trace glows one level under it, so the bar is **monotone in ink across all three of its tones**: track `░` < trace `▒` < tail `▓█`. |
| 5 | `Kit.plot`'s `lcd` branch | `"▄▄" / "░░"` inline | named from `COVER_RAMPS["lcd"]` | byte-identical. This branch had the pair RIGHT while the meter had it wrong, for sixty-two passes; naming the row is what makes that **one definition instead of two that happen to agree**. |

Plus **`_meter_gradient`'s flow row**, which spelled the phosphor ramp **BACKWARDS** — a second
definition wearing a disguise the "each spelled ramp literal appears ONCE" law cannot see. Named,
byte-identical, and asserted.

### #40 — TAKEN, and the item's own measurement was wrong

**PENDING #40 said FOUR branches print air for a zero column. Measured across all twelve
mechanisms (`_p62_prove.py` §3), it was ONE.**

| what the branch does with a zero column | mechanisms |
|---|---|
| draws its unlit lattice down the WHOLE column | `boxed`, `braille`, `decay`, `dotgrid`, `lcd` |
| stands on a BASELINE row, air above | `dimension`, `gradient`, `hairline`, `odometer`, `step`, `tally` |
| **draws nothing at all** | **`blocks` — the `else` branch, nord's, and only it** |

`boxed`, `dotgrid` and `decay` were named in the item as air; they are not — they are the three
mechanisms whose *identity* is a visible unlit lattice, and they draw it in every row. **The cure was
therefore one branch and the same shape as the six that already had it**: `elif pos == 0:` draws
`COVER_RAMPS["blocks"][0]` (`░`), which is the track `_meter_blocks` draws one row above, so the
chart's zero and the meter's zero are one idiom. It is **reachable only by a zero column** — any
`u > 0` lands on `full` or on the partial cell — and that claim is a law, not a comment.

The census is recorded as `FULL_COLUMN`, two-directional, so the two families cannot silently swap.

### THE DIFF SCOPE — 6 of 308 on the shipped grid, and the grid was pass 61's VERBATIM

`_p62_prove.py` §1. **Pass 61's POST dump is this pass's PRE baseline**, which only works because
the fixture grid was copied rather than improved.

| language | spark | plot | meter | pulse | meter token |
|---|---|---|---|---|---|
| corgi | 0/15 | 0/10 | **4/5** | — | lcd |
| nord | 0/15 | **2/10** | 0/5 | — | blocks |
| *(the other eight)* | 0/15 | 0/10 | 0/5 | — | |
| **TOTAL** | **0** | **2** | **4** | **0** | |

The four corgi meters are the four fixtures with an unlit segment in them; **the 8/8 fixture did not
move**, because a full meter has no ghost. The two nord plots are the two fixtures with a zero
column.

**AND A SECOND GRID EXISTS BECAUSE THE FIRST ONE CANNOT SEE HALF THE FAMILY.** `decay` and
`gradient` are worn by NO shipped language (phosphor and bbs were retired), so a language-indexed
fixture set renders them zero times and a cure to them would be a claim rather than a change. The
MECHANISM grid drives all twelve on two host kits: **20 of 120 moved** — `lcd` 8, `gradient` 8,
`decay` 4, and **zero** on the other nine.

    gradient, flat zero    PRE  |▓▒░                                  0%|
                           POST |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0%|
    decay,    mid 3/8      PRE  |▓▓▓▓▓▓▓▓▓░▒▓█░░░░░░░░░░░░░░░░░░░░░  38%|
                           POST |▒▒▒▒▒▒▒▒▒▒▒▓█░░░░░░░░░░░░░░░░░░░░░  38%|
    nord plot([0,0,0,0])   PRE  ['        ', '        ', '        ', '        ']
                           POST [... , '░░░░░░░░']

### THE EVIDENCE NOBODY LIKES: the render moved and **not one existing law noticed**

The suite was run after the five cures and BEFORE the new laws were written: **9496 checks, 0
failures.** Six shipped strings changed — including the whole visible bar of corgi's meter at every
value below 100% — and the 9496-check suite was blind to all of it. That is the same finding pass 61
recorded from the other side: no snapshot had been pinning the broken render, so nothing broke, and
**nothing would have caught it going the other way either**. The +85 checks below are what closes
that hole.

### THE LAWS — 9496 → 9581 (+85), and the arithmetic is the section's shape

**+48** = the census, 4 instruments × 12 mechanisms, run on `host(mech)` kits rather than on the ten
languages **because two mechanisms have no language**. **+24** = #40's two laws × 12 (the baseline
carries ink; the rows above are air unless the mechanism DECLARES a full-column lattice). **+13**
globals: the skill's own case asserted by name at the meter, the pair's ink order, the meter/plot
pair being one definition, the source law that the meter names the ramp, gradient's track and its
two shoulder laws, decay's two monotonicity laws, the phosphor-naming law, nord's zero column, the
proof the baseline cure cannot reach a column with data, and the census-count guard.

**BOTH NEW CENSUSES SHIP EMPTY** (`TONE_COLLIDE = set()`), which is the strongest form a census can
take and the easiest one to widen by hand — which is what M3 does.

### THREE OF THE NEW LAWS WENT RED ON CORRECT CODE, and all three were the law being wrong

Pass 61 recorded two of these; this pass produced three, and they are the same lesson each time.

1. **"the lcd meter does not spell `▄▄`"** — the method's own COMMENT explains what it used to draw.
   A law that reads a glyph out of prose is reading prose. Restated against the string literal the
   code carried: `'"▄▄ "'`.
2. **"decay's bar is MONOTONE in ink"** — a single `a <= b` sweep across the row. The row is not one
   monotone sequence: the TRACK follows the head. Split into the two claims that were meant — the
   run rises to the head, and every track cell is lighter than every run cell.
3. **"gradient does not spell the ramp backwards"** — went red because the law's own explanation, in
   `language.py`, quoted the literal it was forbidding. **A source law can be defeated by the comment
   that documents it.** The comment stopped quoting; the law stayed.

### Mutations — six, all CAUGHT, none crashed, and two attack the LAWS

Baseline 9581/0; restored 9581/0. Chunks run in the FOREGROUND (`_p62_mut_A.txt`, `_p62_mut_B.txt`).

| # | what it breaks | red | which laws fired |
|---|---|---|---|
| M1 | **the lcd meter reverts to tone-only** — the ghost takes the lit glyph again | **3** | both law-1 legs on `lcd` + the skill's-own-case law by name |
| M2 | **the gradient track reverts to spaces** | **3** | law-4 both legs on `gradient` + the "the track IS the phosphor unlit" law (`[' ']`) |
| M3 | **an unused exemption is claimed** — `TONE_COLLIDE` grows to `{"lcd", "decay"}`, **code untouched** | **2** | both mechanisms' law-1 tone census, red **because the exemption is a lie**: they are cured, and `(defect) == (in the list)` bites the liar as hard as the defect |
| M4 | **a census is hand-weakened** — `FULL_COLUMN` gains `"blocks"`, **code untouched** | **1** | the #40 census, alone — and one red is the correct number, because that census is the only law in 9581 that can see which family a branch belongs to |
| M5 | **the #40 cure reverts** — `plot`'s baseline branch removed | **2** | `plot[blocks]` law-4 (`'        '`) + nord's zero-column law |
| M6 | **decay's tail reaches the track again** — 4 cells instead of 2 | **3** | law-1 tone census on `decay` + both monotonicity laws |

**M3 AND M4 ARE THE PAIR TO READ.** Neither touches `language.py`. Both are the move a maintainer
makes when a red is inconvenient: widen the exemption, widen the census. Three reds between them,
and every one of them fires because the list disagrees with the measurement — in the direction where
the CODE is fine and the LAW is lying.

### Verification — three full sets, back to back

| suite | checks | sixty-first | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9581** | 9496 | ALL PASSED (×3) — **+85**, arithmetic above |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (×3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (×3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (×3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (×3) |
| `python -m pytest tests -q` | 137 | 137 | **137 passed (×3)** |

**THE FOUR OTHER SUITES DID NOT MOVE BY ONE CHECK**, which is the same second-half diff-scope
evidence pass 61 recorded: a render change to corgi's meter and nord's plot that leaves the aperture,
the widget slice, the board and the variants suites at identical counts and zero reds means no
snapshot outside `verify_language` was pinning either render.

### Artifacts (`prototypes/out/`, outside the file budget)

`_p62_prove.py` (**§0 the census, §1 the two diff grids, §2 the specimens, §3 the #40 measurement,
§4 vacuity 15/15, §5 the verdict**) · `_p62_PRE.txt` / `_p62_POST.txt` · `_p62_sig_PRE/POST.txt` and
`_p62_mech_PRE/POST.txt` · `_p62_mut.py` + `_p62_mut_A.txt` / `_p62_mut_B.txt` ·
`_p62_r{1,2,3}_*.log`.

### Open, and honest

- **#43 (new)** — the flow/load ROW was censused and is NOT covered by a law. The bar row is; the
  second row's tone-collision reading has three declared-looking cases (`dimension`'s span
  terminators under two tones, `lcd`'s bracketed channel numbers, `odometer`'s digits) that are
  figures and structure rather than levels, and telling those apart needs a per-mechanism argument
  this pass did not make. **Measured in `_p62_prove.py` §0 and left visible rather than smoothed
  over.**
- **#39** (band-threshold quantiser) still did not ride along. `naught.dot_heat` was not opened.
- **`decay` and `gradient` are worn by no shipped language.** Both were cured and both are measured,
  but the render change they carry reaches no screen today. Said plainly rather than counted as
  shipped pixels.
- The two-cell gradient shoulder is a **deliberate narrowing** (three cells to two) and it is the
  one cure that changes a mechanism's proportions rather than its glyphs.

### Next

**#43, or the aperture.** #41 and #40 are closed and #42 is done, so the DATAVIZ law-1/law-4 sweep
is complete at every seat that draws a QUANTITY. What remains on this axis is the flow-row census
above, which is a smaller and better-understood question than either of the two this pass closed.

---

## SIXTY-FIRST PASS — CURING THE RAMPS (#37 · #38) — **the unlit glyph is the one a language already draws for an empty position, and a track heavy enough to read as data is worse than no track**

**What this pass is.** The first DELIBERATE render change to shipped languages on this track. Pass
60 built the ramp registry and measured two defects it refused to cure inside a byte-identity
increment: nine of ten ramps drew AIR at index 0 (DATAVIZ law 4 — a flat-zero series renders as
nothing at all) and two repeated a glyph, one of them the LCD case the skill cites BY NAME (law 1 —
a level that exists only in tone). **The moving pixels ARE the increment, so the job was to measure
exactly which cells move, prove every one was intended, and prove the cells that must NOT move did
not.** 76 of 308 fixture renders moved. The other 232 held, and so did every other suite.

### THE RULE, applied ten times rather than ten preferences

**The unlit glyph is the mark the language ALREADY DRAWS for an empty position on its own `meter`**
— so a spark's zero and the meter's unrun track are one idiom and not two — **and where that mark
already occupies a LIT level, the ramp's own family supplies the step above it** rather than a new
vocabulary being invented. Two ceilings, both laws: the unlit carries INK, and it carries **at most
a quarter of the cell**.

**THE SECOND CEILING IS THE ONE WORTH ARGUING FOR.** Curing law 4 by making index 0 visible invites
the opposite defect immediately: a track heavy enough to be mistaken for a small value. A zero row
that reads as data is worse than a zero row that reads as nothing, because the first one lies and
the second one only omits. M5 spends exactly that ceiling — `phosphor`'s unlit becomes `▒`, still
monotone, still four distinct glyphs, still ink at index 0 — and **exactly one check goes red**,
which is what a load-bearing law looks like in isolation.

**"NOT A SPACE" WAS NEVER THE CLAIM AND THAT IS WHY THE DEFECT SURVIVED SIXTY PASSES.** `braille`'s
index 0 was `⠀` U+2800 BRAILLE PATTERN BLANK — a real codepoint, a real glyph, zero ink. The law is
written on the INK INSTRUMENT (a popcount here), not on `!= " "`.

### THE VERDICTS — ten ramps, ten arguments from the language's own physics

| ramp (who) | PRE | POST | argued from |
|---|---|---|---|
| `eighths` (`_pulse`, `plot`'s partial cell) | `' ▁▂▃▄▅▆▇█'` | `'·▁▂▃▄▅▆▇█'` | level 1 is ONE EIGHTH — the lightest fill the block family has — so the track must come from outside it, and the leader dot is the faintest mark this module draws. **The arithmetic is untouched: 9 glyphs in, 9 glyphs out**, so `plot`'s partial-cell oracle is unmoved. |
| `shades` (= `bases.SHADES`) | `' ░▒▓█'` | **unchanged — the ONE exemption** | a BITMAP cell is a pixel of a SPRITE. A sprite's ground is ABSENCE, not a datum worth zero; inking it would put texture inside every empty pixel of every mascot. Law 4 is a law about DATA. **The semantic reason decides it; `bases.py` being outside the file budget is not the reason and is not offered as one.** |
| `braille` (instrument) | `'⠀⣀⣤⣿'` | `'⠐⣀⣤⣿'` | `⠐` is instrument's OWN unlit — it is what `_meter_braille`'s flow row prints for a zero bucket and what `plot` hands `BS.render` as `off=`. Zero new vocabulary. |
| `fine` (naught) | `'⠂⡀⡄⡇'` | **unchanged** | the one ramp that was already right, and the reason the defect was findable at all. |
| `blocks` (nord, industrial) | `' ▂▅█'` | `'░▂▅█'` | `░` is the track both `_meter_blocks` and `_meter_boxed` already draw one row above the spark. It TIES level 1 in ink (0.25) and differs from it in FORM — a texture against a solid foot — which is the distinction the greyscale law actually asks for. |
| `hairline` (swiss) | `' ─━━'` | `'┈─━━'` | the meter's track is `─`, but that glyph is this ramp's level 1 (a measured minimum), so the unlit is the same rule DASHED: a hairline chart's zero is not the absence of the rule, it is the rule with nothing standing on it. Levels 2/3 still repeat — declared idiom, censused at the pair. |
| `lcd` (corgi) | `' ▄▄█'` | `'░▄▆█'` | **the skill's named case.** `░` is corgi's own ghost (`plot`'s lcd branch draws exactly that for an unlit stack — an LCD segment is never black, it is faint) and the lit levels climb in HEIGHT, which is the cure named in the same sentence as the defect. **Level 1 is unchanged**, so the diff is two cells wide. |
| `phosphor` (decay, gradient) | `' ░▒█'` | `'░▒▓█'` | the full shade family: a CRT's unlit phosphor still glows, and `_meter_decay` already draws `░` behind the head for that reason. |
| `step` (darkside) | `' ▁▄█'` | `'▁▂▄█'` | `▁` is the language's DECLARED track — `_meter_step` fills with `█` against a `▁` rail precisely so fill and track differ by SHAPE, and its comment says so. The ladder rises above it; levels 2 and 3 are unchanged. |
| `dimension` (blueprint) | `' ·─━'` | `'·╌─━'` | four real drafting line types: the leader DOT (which `plot`'s dimension branch already prints, dim, for an unmeasured column), the broken line, the extension line, the heavy dimension line. |
| `tally` (ledger, BUILT from its theme token) | `' ·:▪'` | `'·:▫▪'` | `_meter_tally` prints `·` for every position it has not counted, so **the leader IS the track and the ramp had it at level 1**. The new level 2 is the terminal mark HOLLOW: pencilled in, not posted. |

**TWO PAIRS OF LANGUAGES NOW AGREE ABOUT THEIR ZERO, MEASURED AND ACCEPTED RATHER THAN HIDDEN.** On
a flat-zero series nord/industrial and corgi all print `░`, and blueprint and ledger both print `·`.
That is not drift: it is two pairs of MECHANISMS agreeing about what an empty cell looks like, and
each pair's lit half (`▂▅` vs `▄▆`; `╌─━` vs `:▫▪`) is where the languages speak. Every pairwise
greyscale law runs on non-zero data and none moved. **And nord carries two different zero glyphs on
one card** — `░` in the spark, `·` in the load row — because the load row is the 9-level `eighths`
ramp whose level 1 is one eighth, and the quarter-cell ceiling plus ink-monotonicity leave no block
glyph under it. Arithmetic, not inconsistency, and it is stated rather than smoothed over.

### THE DIFF SCOPE — the centrepiece, measured at 308 fixtures

`_p61_prove.py` §1, PRE captured before the edit, POST after. **76 of 308 strings moved, 232 held.**

| language | spark | plot | meter | pulse | ramp |
|---|---|---|---|---|---|
| naught | 0/15 | 0/10 | 0/5 | — | `'⠂⡀⡄⡇'` (unchanged) |
| corgi | **9/15** | 0/10 | 0/5 | — | `'░▄▆█'` |
| instrument | 6/15 | 0/10 | 0/5 | — | `'⠐⣀⣤⣿'` |
| swiss | 6/15 | 0/10 | 0/5 | — | `'┈─━━'` |
| industrial | 6/15 | 0/10 | **3/5** | — | `'░▂▅█'` |
| nord | 6/15 | 0/10 | **3/5** | — | `'░▂▅█'` |
| darkside | **11/15** | 0/10 | 0/5 | — | `'▁▂▄█'` |
| ledger | **11/15** | 0/10 | 0/5 | — | `'·:▫▪'` |
| solari | 0/15 | 0/10 | 0/5 | — | (none — figures) |
| blueprint | **11/15** | 0/10 | 0/5 | — | `'·╌─━'` |
| `_pulse` | — | — | — | **4/8** | `eighths` |
| **TOTAL** | **66** | **0** | **6** | **4** | |

**READ THE ZERO COLUMN.** `plot` did not move a single cell in any language, and that is a fact
about the design rather than luck: `plot`'s only routed seat is the partial TOP cell of the `blocks`
branch, which is reached with `part` in 1..7 and can never ask for index 0. Its per-row branches
decide lit/unlit per ROW — a boolean, not a coverage — so the cure does not reach them. **That is
now item #40**, named rather than left to be discovered.

**THE SIX MOVED METER STRINGS ARE ALL `_pulse`**, and they are the only cure that reaches a shipped
surface through something other than `spark`: nord's and industrial's flow row now draws a dotted
baseline under a bucket that measured zero instead of leaving the row blank.

**THE COUNTS DIVIDE CLEANLY BY WHICH LEVELS EACH RAMP MOVED.** 6/15 = the fixtures containing a
zero-coverage cell (instrument, swiss, nord, industrial: index 0 only). 9/15 = corgi (index 0 and
index 2, and its level 1 was preserved on purpose). 11/15 = darkside, ledger, blueprint, each of
which moved index 0 *and* an interior level, so every fixture with any data in it moved.

### ZERO-CASE SEMANTICS — the audit that decides where the cure must NOT reach

Making index 0 visible inks every seat that reaches the ramp with `c = 0`. That is correct only
where the blank meant "a datum worth zero". `_p61_prove.py` §3 asks it per seat, and the answers are
measured rather than assumed:

| seat | what one cell is | zero means | therefore |
|---|---|---|---|
| `Kit.spark` | a sample of the series | **coverage 0** | draws the track — cured |
| `Kit.spark([])` | no series at all | absence | returns `''`, never reaches the ramp |
| `_pulse` | one run per bucket | **coverage 0** | draws the track — cured |
| `_pulse([])` | no buckets | absence | returns `''`, never reaches the ramp |
| `Kit.head`'s load | a COUNT bucket | absence | `count == 0` short-circuits to `''` **before** the ramp — the mechanism already passes absence differently, and pass 60's honesty gate is the law that keeps it doing so |
| `plot`'s rows above a column | not a sample | absence | stays air (and must) |
| `plot`'s zero column, `blocks` branch | **coverage 0** | still air — the row branches do not route (**#40**) |
| `bases.shade` / `shades` | a pixel of a SPRITE | absence | stays air — the ONE declared exemption |

**THE ONE SEAT THAT ALREADY GOT THIS RIGHT IS THE MODEL FOR THE REST.** `Kit.head` does not hand the
ramp a coverage of 0 when there is nothing to draw; it returns an empty string. That is what "absence
is passed differently than zero" looks like in code, and it is why the cure could not damage it.

### THE LAWS — the two censuses turned inside out

**9452 → 9496 (+44), and the arithmetic is exactly the section's shape:** the two pass-60 census
laws became FOUR per-ramp laws (+2 × 19 ramps = **+38**) — the unlit carries ink (or is the declared
exemption) · the track stays under a quarter cell · the unlit is none of the LIT glyphs · **only the
declared INDEX PAIR repeats** — plus **+6** global: the skill's own case asserted by name (four
glyphs, and they climb in height), the exemption set is exactly the air set, the exempt row IS
`bases.SHADES`, no ramp glyph is double-width, and the anti-dither probe's new scope guard.

**A CENSUS THAT COUNTS IS WEAKER THAN A CENSUS THAT LOCATES.** `REPEATS` recorded *that* `hairline`
repeated a glyph. `REPEAT_AT` records that it repeats at `(2, 3)` and nowhere else, so an edit that
repeats a DIFFERENT pair cannot pass a census it still satisfies numerically.

**THE VACUOUS LAW WAS UPGRADED UNDER ITS OWN NAME.** `{name}: flat-zero series still renders the
track` asserted `len(k.plot(...)) == 4` — which four rows of SPACES satisfy, which is precisely what
law 4 forbids and precisely what nine languages drew. **A law whose name states the claim and whose
body states something weaker is worse than no law**, because it occupies the place where the real
one would go. It now asserts the spark's every cell IS the ramp's own unlit glyph (and that solari,
which draws figures, prints `0`s). M1, M2, M4 and M6 all red it.

### TWO LAWS OF PASS 60 WENT RED ON CORRECT CODE, and both were the law being wrong

**(1) The anti-dither grep read a CHARACTER WINDOW.** `getsource(LG).split("def coverage_index")[0][-4000:]` is
a proxy for "in the coverage block", and this pass's registry argument pushed `NEVER DITHERED` out
of the window: **a law about dithering went red because somebody wrote a paragraph about ramps.**
Restated as the block between its own banner and `def coverage_index`, with a second check that the
scope it read is really that block. Same lesson as pass 60's quote-style leak — **a source law that
a formatting change can walk around is not a source law.**

**(2) The `phosphor` cure collided with a real duplicate.** `'░▒▓█'` is now the registry row AND the
literal `_meter_decay` slices for its persistence tail, so "each spelled ramp literal appears ONCE"
went red — correctly. **The tail IS the phosphor ramp, indexed by DISTANCE FROM THE HEAD rather than
by coverage**, so the meter now names the registry row (`COVER_RAMPS["phosphor"][4 - tail:]`,
byte-identical output) and the comment states why that is not routing: a position is not a coverage.
**The law found a fork the moment one could exist**, which is the whole reason to count literals.

### Mutations — six, all CAUGHT, none crashed, and two attack the LAWS

Baseline 9496/0; restored 9496/0. Chunks run in the FOREGROUND (`_p61_mut_A.txt`, `_p61_mut_B.txt`).

| # | what it breaks | red | which laws fired |
|---|---|---|---|
| M1 | **a ramp reverts to air-less** — `blocks` back to `' ▂▅█'` | **6** | law-4 ink on `blocks`/`kit:nord`/`kit:industrial`, the global exemption-set law, and the upgraded flat-zero law in nord + industrial |
| M2 | **the lcd reverts to tone-only** — back to `' ▄▄█'` | **9** | both `REPEAT_AT` legs, both law-4 legs, **the skill's-own-case pair**, the exemption-set law, corgi's flat-zero law — and the literal-count law, because the registry comment records the old value |
| M3 | **the census is hand-weakened** — `AIR_EXEMPT` grows to the blocks family, **code untouched** | **5** | three per-ramp law-4 legs go red *because the exemption is claimed and unused*, plus the exemption-set law and "the exempt row IS bases.SHADES" |
| M4 | **the eighths track is lost** — `RAMP` back to a leading space | **2** | law-4 on `eighths` + the global exemption-set law |
| M5 | **the track ceiling is spent** — `phosphor` unlit becomes `▒` | **1** | the quarter-cell ceiling, **alone** — every other law of the cure still passes |
| M6 | **the built ramp reverts** — `cover_ramp`'s tally branch back to `' ·:'` | **5** | law-4 on `kit:ledger`, the exemption-set law, ledger's flat-zero law, the registry-row law, and the declared-glyph split (`▫` leaves the vocabulary) |

**M3 IS THE ONE TO READ.** Nobody reverts a ramp to bring the air back — they take an exemption.
M3 is that move: `verify_language.py` edited, `language.py` untouched, the exemption list widened by
hand the way a maintainer would widen it to make a red go away. **Five checks red, and three of them
are the per-ramp laws going red for the OPPOSITE reason** — the ramp is fine and the exemption is a
lie. A census written as `(defect) == (in the list)` bites the liar as hard as the defect.

**M5 IS THE PROOF THAT THE SECOND CEILING IS NOT ORNAMENT.** One red, and it is the only law in a
9496-check suite that can see a track heavy enough to read as data.

### Specimens

`_p61_PRE.txt` §2 against `_p61_POST.txt` §2 — every ramp swept 0% → 100%, and the flat-zero row in
three contrasting languages:

    PRE                                        POST
    nord       spark[0]*8 -> |        |        nord       -> |░░░░░░░░|
    corgi      spark[0]*8 -> |        |        corgi      -> |░░░░░░░░|
    blueprint  spark[0]*8 -> |        |        blueprint  -> |········|
    nord  meter flow row  -> |            |    nord  flow -> |············|

and the series `[0, 1, 2, 3, 5, 8, 13, 21]`, which carries a zero AND every interior level:

    PRE                       POST
    corgi       | ▄▄▄▄▄▄█|    corgi       |░▄▄▄▄▄▆█|
    instrument  |⠀⣀⣀⣀⣀⣀⣤⣿|    instrument  |⠐⣀⣀⣀⣀⣀⣤⣿|
    swiss       | ─────━━|    swiss       |┈─────━━|
    darkside    | ▁▁▁▁▁▄█|    darkside    |▁▂▂▂▂▂▄█|
    ledger      | ·····:▪|    ledger      |·:::::▫▪|
    blueprint   | ·····─━|    blueprint   |·╌╌╌╌╌─━|
    naught      |⠂⡀⡀⡀⡀⡀⡄⡇|    naught      |⠂⡀⡀⡀⡀⡀⡄⡇|  (unchanged — it was right)
    solari      |01111123|    solari      |01111123|  (unchanged — figures, no ramp)

### Verification — three full sets, back to back

| suite | checks | sixtieth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **9496** | 9452 | ALL PASSED (x3) — **+44**, and the arithmetic is above |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 97 | 97 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 passed (x3)** |

**FOUR SUITES DID NOT MOVE BY ONE CHECK AND THAT IS THIS PASS'S SECOND DIFF-SCOPE EVIDENCE.** A
render change to nine languages that leaves the aperture, the widget slice, the board and the
variants suites at identical counts and zero reds means no snapshot outside `verify_language` pinned
a ramp glyph — the cure reaches the shipped seats (`Kit.spark` is what `aperture.py:350` and
`hero.py:115` call) without any of those suites having been asserting the broken render.

**THE CAPTURE RACE DID NOT FIRE.** Zero `settle timeout` lines across all fifteen suite runs and the
eight mutation runs. The standing watch stays open (#10's neighbourhood); it is not claimed cured.

**THE PYTEST ROW HELD AT 137 IN ALL THREE RUNS**, `test_win_clipboard_roundtrip` included. It does
not close #22.

### Artifacts (`prototypes/out/`, outside the file budget)

`_p61_prove.py` (**§1 is the diff scope, §2 the specimens, §3 the zero-case audit, §4 vacuity 6/6,
§6 the per-ramp verdict**) · `_p61_PRE.txt` / `_p61_POST.txt` · `_p61_sig_PRE.txt` /
`_p61_sig_POST.txt` (the 308 strings) · `_p61_mut.py` + `_p61_mut_A.txt` / `_p61_mut_B.txt` ·
`_p61_r{1,2,3}_*.log` (the three full sets).

### Open, and honest

- **#40** — `plot`'s zero column still draws air in four branches. The ramp cure cannot reach it;
  it is a baseline-row question per language, and it is filed rather than half-done.
- **#41** — `_meter_lcd` repeats a glyph in TONE ALONE and `_meter_gradient`'s track is air: **the
  two defects this pass just cured, alive at the mechanism next door.** The meters do not route, so
  no law here can see them. This is the natural next increment.
- **#42** — `hero.py:107`'s comment cites the old `blocks` literal. One line, outside the budget.
- **#39** (band-threshold quantiser) did NOT ride along: `naught.dot_heat` was not opened, because
  the `fine` ramp needed no cure and there was no other reason to touch it.
- The two accepted zero-glyph agreements (nord/corgi on `░`, blueprint/ledger on `·`) and nord's
  two-glyph zero are design decisions, argued above, not oversights.

### Next

**#41, as one increment over the METER family.** It is the same argument this pass made about ramps,
applied to the mechanism next door, and it is now the sharpest open defect on the axis: corgi's
meter is still the exact case DATAVIZ law 1 names, at a seat no ramp law runs over. Expect it to
move ten meter renders and the meter half of every kit signature — measure PRE/POST the way this
pass did, and take #40 with it if `plot`'s baseline row is opened at the same time.

---

## SIXTIETH PASS — `coverage_to_glyph` (Bodmer P2) — **alpha is not a blend, it is an INDEX; and the refusal to dither is the load-bearing half**

**What this pass is.** The last approved-but-unbuilt research proposal, and the smallest one: the
ten languages each picked their data-viz glyphs from a ramp literal written inside the drawing
method, so "what does 40% coverage look like here" was answered in nine places and could drift in
nine places. What lands is ONE function, ONE registry, and a routing table that says out loud which
mechanisms are NOT coverage-shaped and therefore do not route.

### THE DESIGN, and the one place it disagrees with Bodmer

Coverage anti-aliasing on a pixel display is a BLEND: 40% of the ink mixed into the ground, with 256
steps to spend. **A cell has no blend. It has a glyph.** So coverage stops being an alpha and becomes
an INDEX into an ordered ramp, and the two ends are NAMED rather than interpolated:

    c <= lo    ramp[0]   — the ramp's own UNLIT glyph, never a hard-coded space
    c >= hi    ramp[-1]  — the terminal glyph
    between    ramp[max(1, round(n * c))]

**`lo` DEFAULTS TO 0.0 AND THAT IS THE DISAGREEMENT, STATED AS A RULING.** Coverage AA is free to
drop faint ink below a threshold — that is what the threshold is FOR, and it is the move the source
research is built around. DATAVIZ law 3 forbids it for DATA: "we have 1 overdue" may not render as
"we have none". The skill wins on conflict, so on the data axis **the only coverage that earns blank
is exactly zero**, and the `lo` seat is left open for STRUCTURE, which carries no such law. The
`max(1, ...)` in the middle band IS law 3, moved from nine copies into one.

**THE ANTI-DITHER RULING IS THE HALF THAT WILL ACTUALLY BE TESTED.** The obvious next move from
coverage AA is error diffusion — spread the quantisation residue into the next cell, or perturb the
index by a hash of the position, and the ramp reads smoother. It is refused, in the docstring, under
a grep law, for two reasons that are about this repo and not about taste: **(1)** a position-
dependent glyph makes the same value draw differently in two places, so every byte-identity law in
`verify_language` becomes unwritable and a snapshot suite can only say what a render *happened to
be*; **(2)** a static surface that re-renders on a tick would CHURN — the dither pattern moves while
the data stands still, which is motion with no event behind it. **M5 deletes the sentence and the
suite goes red**, which is the only thing that makes a docstring a ruling.

### THE ROUTING TABLE — and the honesty gate is the point of it

Derived, not remembered: `_p60_prove.py` §3 holds each cell position fixed, moves the value, and asks
whether the glyph set the mechanism draws is the registry's ramp.

| language | `meter` | routes? | ramp / why not |
|---|---|---|---|
| naught | `dotgrid` | **YES** | `'⠂⡀⡄⡇'` — the FINE sub-cell dot scale |
| corgi | `lcd` | **YES** | `' ▄▄█'` — segment height + ghost |
| instrument | `braille` | **YES** | `'⠀⣀⣤⣿'` — sub-cell fill |
| swiss | `hairline` | **YES** | `' ─━━'` — two weights and absence |
| industrial | `boxed` | **YES** | `' ▂▅█'` — declares no ramp of its own, inherits the conventional one |
| nord | `blocks` | **YES** | `' ▂▅█'` |
| darkside | `step` | **YES** | `' ▁▄█'` |
| ledger | `tally` | **YES** | `' ·:▪'` — **the one language that BUILDS its ramp**, from its own `tally` token |
| blueprint | `dimension` | **YES** | `' ·─━'` — the leader/line ladder |
| solari | `odometer` | **no** | **DIGITS: the figure IS the datum.** A flap board's quantity is printed, not filled — it never reaches the ramp, and the call recorder asserts **zero** calls |

Beyond `spark`, three more seats were read and two routed:

- **`Kit.plot`, the blocks branch — ROUTES.** Its top cell is a FRACTION of a cell (`RAMP[part]`),
  which is exactly what the primitive is for. Every other `plot` branch decides lit/unlit **per
  row** — a boolean, not a coverage — and does not route.
- **`_pulse` (the hero's load row) — ROUTES**, on the 9-level eighths ramp.
- **`Kit.head`'s load glyph — DOES NOT ROUTE, and the suite asserts that it still doesn't.**
  `RAMP[min(8, 1 + count // 3)]` is a COUNT bucket. It was the first thing the source law caught —
  a blanket "no `RAMP[` anywhere" rule went red here — and the fix was to narrow the LAW, not to
  route the seat. **A count is not a coverage.** The check is worded so the next reader who greps
  `RAMP[` finds the ruling before they "finish the routing".
- **`Kit.gauge` — does not route.** Track, needle and tick are SHAPES at POSITIONS, not densities.
- **`Kit.bar` — does not route.** A span fill; the length is the datum.

### BYTE IDENTITY: MEASURED, AND IT HELD

`_p60_prove.py` §1 dumps every routed seat as **raw markup** at a fixture grid built for the
boundaries the routing could break silently — empty series, flat zero, a microbar under a ceiling of
99, a sample **over** the ceiling, a negative sample, a one-cell width, and a series long enough to
resample. **258 strings, PRE against POST, 0 divergences.** The sweep is render-neutral: **no cure
was needed and none is claimed.**

A diff run once proves nothing about tomorrow, so the claim is also written as a standing law:
three ORACLE checks assert the primitive reproduces the exact arithmetic each routed seat used to do
inline (`0 if n <= 0 else max(1, min(3, round(3 * n / top)))`, `_pulse`'s 9-level form, and `plot`'s
partial cell), swept over six ceilings and the full value range of each.

**One divergence exists and is unreachable, so it is named rather than left to be discovered:**
`_pulse` used to read `0 if n == 0`, the primitive reads `c <= lo`. A NEGATIVE bucket count would
therefore draw the unlit glyph now and drew `RAMP[1]` before. `_pulse`'s inputs are task
cardinalities, so nothing can reach it — but it is a real difference in the function's domain and it
is on the record.

### THE LAWS — and one of them was wrong first

**+260 checks (9192 → 9452).** Per ramp (10 registry rows + 9 per-language ramps = 19): monotone index over a
dense 500-point grid that runs **outside** [0, 1] at both ends · monotone in INK · greyscale-safe
(the two ends differ in ink) · three threshold laws · deterministic over 100 calls · the microbar
floor · and two CENSUS laws (below). Per language: `cover_ramp()` is the registry row its `meter`
names · every spark glyph comes from that ramp · **the call recorder** — `spark` calls the primitive
exactly `len(_resample(series, w))` times and each call was handed THAT ramp · and **the glyphs on
the glass ARE the primitive's own return values**, in order, which is a second claim from the same
recorder ("it was called" and "what it returned is what got drawn" are not the same sentence).
Globally: the two
"ONE definition" laws (`COVER_RAMPS['shades'] is bases.SHADES`, `['eighths'] is RAMP`), the three
oracles, cross-process determinism, four source laws, and the #35-shaped rider law.

**THE SOURCE RULE AND THE CALL RECORDER ARE BOTH THERE ON PURPOSE, and M3 is why.** M3 reverts
instrument's braille spark to indexing `'⠀⣀⣤⣿'` directly. **The render is byte-identical** — no
greyscale law, no pairwise law, no snapshot can see it. Only the source rule and the recorder can. A
method can satisfy "contains no ramp literal" by importing one, and it can satisfy "calls the
primitive" while still drawing from a literal; neither check alone is the claim.

**THE THRESHOLD LAW WAS MIS-SPECIFIED ON THE FIRST RUN AND THE MISTAKE IS WORTH KEEPING.** It was
written as "no MIDDLE GLYPH appears outside [lo, hi]" and went red on `hairline` and `kit:swiss`.
The ramp is `' ─━━'`: its TERMINAL glyph is **also** its level-2 glyph, so the middle and the end
sets overlap and the question is unaskable of it. The claim was always about the **INDEX** — only
the two end indices are reachable outside the band — and the glyph is what the ramp does with it.
Restated as an index law it is strictly stronger and holds everywhere. **A law that goes red on
shipped, correct code is usually the law being wrong, and the cure is to say the true thing, not to
widen the assertion until it passes.**

### THE INK INSTRUMENT — and why it needed a provenance

The greyscale half of the contract needs a density per glyph, and a table somebody typed would make
the law circular. So density is **DERIVED wherever the codepoint carries it** — braille is a
popcount of `cp - 0x2800`, the block eighths are `(cp - 0x2580) / 8`, and the shade blocks are
ordered by their own Unicode names (LIGHT/MEDIUM/DARK SHADE) — and **DECLARED only for the five
glyphs Unicode gives no ordering to**: `·`, `:`, `─`, `━`, `▪` (box-drawing weight and punctuation).
**The split itself is asserted**: 3 of the 23 distinct glyphs in the registry are declared, and a
law says exactly which, so the derived half cannot quietly become a typed one.

### THREE THINGS THIS PASS MEASURED AND DID NOT CURE — each one now a CENSUS LAW

A census law goes red when it **grows** (the defect spread) and red when it **shrinks** (somebody
cured it and did not say so). That is the whole reason to write one instead of a comment.

- **(#37) NINE OF TEN RAMPS HAVE AN AIR UNLIT GLYPH.** DATAVIZ law 4 says every ramp needs a real
  unlit glyph at index 0, and names the trap by name: a ramp whose level-0 glyph is a SPACE renders a
  flat-zero series as *nothing at all* — the law says track, the code draws air. Measured: only
  naught's `fine` ramp (`⠂`, ink 0.125) satisfies it. `braille`'s `⠀` is U+2800 BRAILLE PATTERN
  BLANK — a real codepoint with zero ink, which is the same defect wearing a glyph's clothes. The
  existing law only asserted the plot returns **h rows**, which a row of spaces satisfies.
- **(#38) TWO RAMPS REPEAT A GLYPH, AND ONE OF THEM IS THE SKILL'S OWN NAMED EXAMPLE.** `lcd` is
  `' ▄▄█'`: levels 1 and 2 are the same glyph and differ only in TONE (`dim` vs `screen`). DATAVIZ
  law 1 cites exactly this — "an LCD spark whose lit and ghost segments share a glyph is invisible in
  greyscale; it needed segment HEIGHT" — and it is still here. `hairline` is `' ─━━'`, levels 2 and 3
  identical, which is at least a *declared* two-weight idiom rather than a colour-only step.
- **(#39) THERE IS A SECOND QUANTISER FAMILY AND THE PRIMITIVE SERVES ONE OF THEM.** Nearest-index
  (this primitive): `round(n * c)` with a microbar floor. Band-threshold: `3 if c > .66 else 2 if
  c > .33 else ...`. **They disagree at c = 0.34, 0.40 and 0.67** (measured in `_p60_prove.py` §6c),
  so routing the band family is a RENDER change, not a cure. Two seats: `naught.dot_heat` (the FINE
  scale) and `language._meter_braille`'s flow row.

**AND THE PRIMITIVE'S OWN ANCESTOR IS IN `bases.py`, LEFT WHERE IT IS.** `bases.shade` is literally
`SHADES[round(cov * (len(SHADES) - 1))]`, docstring "a soft, anti-aliased pixel instead of a hard
one" — the same idea, written before it, with **no microbar floor**. And that is CORRECT there: a
10%-lit pixel of a BITMAP genuinely is mostly ground, and law 3 is about data. `bases.py` was
outside this increment's file budget, and the registry names `BS.SHADES` rather than copying it so
the two cannot fork — **asserted, which is what makes that registry row a law and not decoration.**

### `naught.py` WAS READ AND NOT TOUCHED — the decision, stated

The brief allowed a sixth file if naught's FINE routing was *trivially clean*. It is not.
`naught.dot_heat` is the band-threshold quantiser above; routing it would move `c = 0.34` from level
1 to level 2 on every dot-heat cell naught draws. That is a render change to a shipped language
dressed as a refactor. **`naught.FINE` still reaches the primitive** — it is the `fine` registry row,
and naught's spark draws through it — so the tuple did not need to move for the routing to be real.
**Five files, not six.**

### Mutations — seven, all CAUGHT, none crashed

Baseline 9452 / 0. A mutant that crashes the suite is not a caught mutant (pass 59's finding); none
of these crashed.

| # | what it breaks | red | which laws fired |
|---|---|---|---|
| M1 | **ramp reordered** — `blocks` becomes `' ▅▂█'` | **3** | `MONOTONE in ink` on `blocks`, `kit:nord`, `kit:industrial` |
| M2 | **thresholds inverted** — `c <= lo` returns the terminal, `c >= hi` returns 0 | **59** | `MONOTONE`, both `THRESHOLD` legs, across every ramp |
| M3 | **a mechanism reverts to its inline ramp** (render byte-identical) | **2** | the two source rules — and nothing else CAN see it |
| M4 | **position-dependent perturbation** — `+ (hash(ramp) & 1)` | **14** | `DETERMINISTIC across processes`, 2 of the 3 oracles, 8 `THRESHOLD` legs, and one PRE-EXISTING law (`swiss: spark honours a SHARED hi`) |
| M5 | **the anti-dither refusal deleted** from the docstring | **1** | the grep law, exactly as designed |
| M6 | **the microbar floor spent** — `COVER_LO = 1/32` | **33** | the PRE-EXISTING `microbar floor` law in **all ten languages**, plus the primitive's own |
| M7 | **the rider reverted** — `DIM_LEVEL` back as channel 3 | **1** | the two-channel rider law |

**M1 IS THE ONE TO READ.** Swapping two middle glyphs of the `blocks` ramp visibly changes what nord
and industrial draw — a sparkline that reads backwards between 17% and 83% — and **only the new
ink-monotone law noticed.** No render law, no greyscale law, no pairwise law and no snapshot in a
9192-check suite could see it, because every language changed consistently with itself.

**M3 IS THE ONE THAT IMPROVED A LAW.** It was caught by ONE check on the first run; the "each ramp
literal appears once" law counted `"..."` and the mutant's literal was `'...'` inside a
double-quoted f-string. Hardened to count both quote styles. **And the call recorder does NOT catch
M3, which is worth stating rather than hiding**: `spark` computes its glyph list before the
mechanism dispatch, so instrument still CALLS the primitive the right number of times and simply
ignores the answer. Only a source rule can see that mutation, which is precisely why the section
carries both kinds.

**M4'S TARGET LAW WAS CONFIRMED FIRING, not assumed.** The chunked log truncates at 8 reds, so M4
was re-run alone with the full list captured (`_p60_m4_full.txt`): `cover: DETERMINISTIC across
processes (3 fresh PYTHONHASHSEEDs)` is in it. **The two M4 runs redded DIFFERENT ramps** —
`hash()` is seed-dependent, so which ramps get perturbed varies per process, which is itself
evidence the mutation does what it claims.

**THE BATTERY WAS KILLED MID-FLIGHT ONCE AND THE RECOVERY WORKED.** A detached run was terminated
during M4, leaving `language.py` mutated on disk with `_p60_mut.ORIG` beside it. The driver's
startup recovery restored it (`RECOVERED language.py from a previous run's backup`), all four
mutation anchors were re-verified present, and the byte-identity sweep was re-run to 258/0 before
anything else proceeded. **Pass 59 built that recovery after being bitten; this pass is the
evidence it pays.**

### Artifacts (`prototypes/out/`, outside the file budget)

`_p60_prove.py` (**the file to look at — §2 is the specimen sweep, §1 is the byte-identity verdict,
§6 is the three findings**) · `_p60_sig_PRE.txt` / `_p60_sig_POST.txt` (the 258 strings, before and
after) · `_p60_mut.py` + `_p60_mut_A.txt` / `_p60_mut_B.txt` / `_p60_mut_C.txt` (the mutation logs;
A was the run that got killed mid-M4) · `_p60_m4_full.txt` (M4 re-run alone, full FAIL list, the
determinism law shown firing) · `_p60_base.txt` · `_p60_r{1,2,3}_*.log` (the three full sets).

### Next

**#37 and #38 together, as one RENDER increment** — they are both ramp edits, both move the same
snapshots, and #38 (a level that exists only in colour) outranks #37 (a lost zero row) in severity.
Do them one ramp at a time with a before/after specimen each, and expect the kit signatures and the
pairwise-greyscale laws to move; that is the increment, not a side effect of it. **#39 rides along
if `naught.dot_heat` is opened anyway.** The census laws are what make it safe to have deferred all
three, and they are what will go red the moment the cure lands without the record being updated.

---

## FIFTY-NINTH PASS — THE MOTION AXIS (item #27) — **a motion is a LIST OF RENDERS, in one of two regimes, and the gap between them is illegal**

**What this pass is.** The component family's four tempo debts, paid in one increment because they
were one question asked four times: the button's press had no intermediate frames, the radio's mark
did not travel between siblings, the caret did not blink, and the stepper's option did not move as
it was spun. What lands is not four animations — it is **one engine, five events, and two regimes**,
with the per-language expression riding a token that already existed.

### THE DESIGN, and the corpus that settled it

The reference is the SquareLine/LVGL published-animation corpus: **241 animations, and ZERO of them
animate a colour.** Read against a terminal that number stops being trivia and becomes the
mechanism, because the terminal has no sub-cell position, no fractional weight and nothing to
interpolate. So:

* **A MOTION IS A LIST OF RENDER STATES** — discrete frames — **not a style transition.** Every
  frame is composed by the component seats this contract already has, at intermediate values. A
  frame that is a render cannot go stale the way the eight hand-authored `flip_frames` did (pass 49
  deleted them as pictures of a dead switch); a frame that is a picture always can.
* **TWO DISJOINT REGIMES.** `transition` — one-shot, **≤400 ms** (corpus median 300, p90 600; the
  ceiling captures 68%), easing biased to deceleration (the corpus runs ease_out over ease_in
  **5:1**). `ambient` — looping, period **≥2000 ms** (corpus median 3000). **The 400-2000 ms dead
  zone is ILLEGAL**: a one-shot slower than 400 makes the user wait on the designer's taste, a loop
  faster than 2000 twitches, and a spec that lands between them has not decided which it is. The
  suite refuses it rather than rounding it to the nearer one.
* **CHANNELS, in priority order:** `glyph_frame` (discrete substitution — the only continuous-medium
  primitive that survives translation intact), `cell_position` (quantised for free, because a cell is
  the only position there is), `dim_level`.
* **COLOUR IS NOT A CHANNEL.**

### THE FINDING THE CHANNEL LIST FORCED: `dim_level` is not a third channel here

The brief named a 3-4 step dim ladder as the third channel and in the same breath forbade colour.
Both cannot be true if a ladder is written in colour — and in a terminal a ladder is **written in
glyphs** (`█▓▒░`, naught's phosphor decay). So `dim_level` in this medium **collapses into
`glyph_frame`**, and this increment ships two channels rather than three: a ladder spelled in tone
would be the colour animation the corpus never publishes, and a ladder spelled in glyphs is already
the first channel under another name. Nothing was built for a third channel; the contract says why.

### THE ENGINE

```python
motion_frames(component, event, **kw) -> Motion(frames, regime, step_ms)
```

* **`frames[0]` IS THE RENDER THE MOTION LEAVES**, and it is in the list so a law can measure a
  motion against its own starting point instead of against a picture the oracle drew. A player does
  not DRAW it for a transition — it is already on the glass, which is what keeps the acknowledgement
  immediate. An AMBIENT has no "already there": it cycles, so **its period divides by the frame
  COUNT and a transition's by the GAPS between them.** That arithmetic difference is derived from
  the regime, and it is a law.
* **REGIME AND DURATION ARE DERIVED AND UNREACHABLE FROM A LANGUAGE.** The regime comes off the
  EVENT (`MOTION_EVENTS`) — ten languages may not disagree about whether pressing is one-shot any
  more than they may disagree about how many parts a slider has. The duration comes off the regime
  and the language's `tempo` token: **a transition's whole pass is one tempo**, which is byte for
  byte the arithmetic the config screen has been dividing by hand since pass 49.
* **WHICH MOTIONS A COMPONENT HAS IS DERIVED FROM THE PARTS REGISTRY**, the way its states are: an
  ACTIVE state means it can be pressed, a `step` part means it spins, a `caret` means it blinks, the
  CHECKABLE one with an indicator flips. Nothing reads a component's name.
* **AND `travel` IS NOT IN THAT DERIVATION — pass 51's finding arriving on the motion axis.** The
  registry describes ONE component and has nothing to say about siblings, so "the mark moves from
  that well to this one" can no more be derived from `COMPONENT_PARTS["radio"]` than the exactly-one
  invariant could. It is a fact about a SET, its seat is the group's, and `MOTION_GROUP_EVENTS`
  names the boundary instead of hiding it.

**`FLIP_STEPS` became `MOTION_STEPS`, and the rename is the increment.** One token governed the
switch; it governs five events now. A language that elaborated its switch and cut its button would
be two languages. **Renouncing ELABORATION is not renouncing the EVENT**: swiss declares 0 and still
gets two frames from every transition, because a one-frame transition is not a transition, it is a
cut — and that floor is the ENGINE's, which a language cannot reach.

`flip_frames` survives as a caller that drops frame 0 (its caller is already showing it) and its
output is **byte-identical** to what shipped, which is asserted per language rather than hoped.

### THE FOUR DEBTS, and how each one is drawn

| debt | regime | the channel, concretely |
|---|---|---|
| **button press** | transition | The extreme is reached on the FIRST drawn frame — the acknowledgement is never animated (MOTION.md: animate the consequence) — then the language's ACTIVE walls are HELD and the release lands on the last frame. **Its anchor and its rest are the same render**, which is what a press IS: nothing survives it. A flip, a travel and a spin all land somewhere else, and that difference is a law. |
| **radio travel** | transition | **The frame count is the DISTANCE's, not the language's** — the mark passes every well between the two it joins because those wells are THERE. What the language chooses is whether the mark is ever seen OFF a well. **The in-transit frame marks NOTHING and does not come out of `group_states`**: that seat exists to make "exactly one is marked" unreachable, and a frame between two states is a FRAME, not a state — pass 49's ruling, at the group scope. |
| **caret blink** | **AMBIENT — the contract's first loop** | Two frames, and the diff is **exactly one cell**: the caret's column wears the language's mark, then the RUNE its paper is made of. **The tone does not move** — the column is drawn from the caret's own tone in both frames — so this motion satisfies the strict reading of the colour rule and not merely the law's. `caret_on` is a MOTION argument on a render seat, not a sixth state: a blink is not a state, the field is being edited in both frames. |
| **stepper spin** | transition | **What stands between the two words is the language's own `SPIN`** — the frame-motion token every language already declares for its spinner, one phase further along per cell. Nothing is hand-authored and nothing is invented: on a split-flap board that token is a cell mid-turn, so **solari's in-transit frames ARE the riffle**; on the terminal's own idiom they are its quadrant marks; swiss never draws one. The steps are drawn at the DESTINATION, because the value moved on the key press and what is catching up is the WORD. |

### THE PASS FOUND A LIVE DEFECT — reported, not smuggled

Building the spin meant consuming every language's `SPIN`, and industrial's fourth mark was `\`.
`Kit.spinner` emits `f"[tone]{glyph}[/]"`, and **a backslash in front of a `[` escapes it in BOTH
parsers** (item #31), so `[tone]\[/]` closes nothing and puts a raw `[/]` on the glass —
**industrial's spinner row had been doing that on the gallery and the aperture every fourth frame,
for as long as that spinner has existed.** No `[/]` law ever ran over that seat. The glyph is now
`╲`, the rotation is unchanged, and the standing guard is a law over frames: **every motion frame
and every spinner frame must mean the same thing to rich and to Textual and put no close tag on the
glass.** Measured PRE/POST in `_p59_prove.py` §4; re-armed as mutation M7.

### WHAT IS WIRED LIVE, and what is honestly gallery-only

* **The config screen's `r`** plays the press's frame list. `_pressed` is GONE: it was a second
  state living beside the real one, could only ever say "flashing or not", and had no way to grow
  intermediate frames.
* **`left`/`right`** play the pick's motion **at the mechanism the screen is actually drawing** —
  wide it is a radio and the mark TRAVELS, narrow it is a stepper and the WORD spins. One choice,
  two mechanisms, two motions. A pick that changes nothing (the clamped end) plays nothing.
* **ONE MOTION SLOT for the whole screen**, replacing `_flip` and `_pressed`. MOTION.md's hardest
  rule is that only one thing may move at a time, and **two slots is how a surface grows a second
  moving element without anyone deciding to.** The single player advances an INDEX and divides
  nothing — the engine already decided the step.
* **The caret's blink is GALLERY-ONLY and that is stated rather than faked.** Pass 53 read this app
  for a live text seat, found none (nothing in the engine is TYPED) and refused to invent one. That
  ruling stands. The gallery hands the block its own clock (`GAL_FPS`, one seat for the repaint rate
  and the phase); called without a tick the caret is simply ON, which is why the blink could not
  move a single law that measured that block before it existed.

### The laws, and the mutants that prove they bite

`verify_language` grew the motion section: the contract and its derivations, the source rules
(**no motion builder holds a drawn glyph or names a colour token; no language declares a regime or a
duration**), then per language × per event — realizability, regime, dead zone, no-colour, no-jiggle,
deceleration, both-parsers — then the four debts one at a time, then the character laws (**all ten
languages' frame lists differ with the colour stripped, on every one of the four motions**), then
in-suite controls for every predicate, then the live seat driven with the clock PINNED and the
gallery's loop driven **by INDEX, never by wall clock** (a two-second period cannot be waited on
inside an acceptance suite).

**The no-colour law is stated as what it can enforce, and the difference matters.** The strict form
— "no tone changes across frames" — would send the SHIPPED flip red, because its mid frames are
drawn in ACTIVE and ACTIVE carries the accent. So the law is: **the frames must MOVE with the colour
taken away, and no consecutive pair may differ ONLY in colour.** Tone may ride along; it may not BE
the motion. The strict form is asserted where it is actually true (the blink).

**One instrument correction, measured while writing it:** the first form of the "no language
declares a regime" law grepped each kit's SOURCE for `AMBIENT`, and darkside's composition comment
calls its centred column "the AMBIENT register" — a word about a REGISTER. A law that reads prose
reports on prose. It asks the class NAMESPACE now.

### RIDER — item #35 cured

`verify_aperture`'s escape-sweep vacuity guard counted `[urgent]` and `[URGENT]` against a
case-folded blob, so it was **one hazard head counted twice**: the count was 0 or 2, never 1, and it
could not tell "both hazard titles rendered" from "one did". It counts the distinct TAILS now and
requires exactly two, which is the read `verify_widget` took in pass 58. **208 → 208** — the guard
was replaced, not added.

### THE STORYBOARDS — the four debts, three contrasting languages

Verbatim from `_p59_prove.py` §1. `solari` snaps (tempo 40, `MOTION_STEPS=3`), `swiss` renounces
elaboration (`MOTION_STEPS=0`, so every one-shot is a CUT), `naught` is the dot lattice (tempo 120,
3 steps).

```
--- PRESS  (button)
  `▁ Refresh ▁` -> `▂ Refresh ▂` -> `▂ Refresh ▂` -> `▂ Refresh ▂` -> `▂ Refresh ▂` -> `▁ Refresh ▁`
      8 ms/step · 6 frames · transition · 40 ms total · solari
  `│ Refresh │` -> `█ Refresh █` -> `│ Refresh │`
      120 ms/step · 3 frames · transition · 240 ms total · swiss
  `◦ Refresh ◦` -> `●●Refresh●●` -> `●●Refresh●●` -> `●●Refresh●●` -> `●●Refresh●●` -> `◦ Refresh ◦`
      24 ms/step · 6 frames · transition · 120 ms total · naught

--- TRAVEL  (radio)
  `▁●▁ api  ▁▁▁ web  ▁▁▁ ops` -> `▁▁▁ api  ▁▁▁ web  ▁▁▁ ops` -> `▁▁▁ api  ▁●▁ web  ▁▁▁ ops` -> `▁▁▁ api  ▁▁▁ web  ▁▁▁ ops` -> `▁▁▁ api  ▁▁▁ web  ▁●▁ ops`
      10 ms/step · 5 frames · transition · 40 ms total · solari
  `╵•╵ api  ╵ ╵ web  ╵ ╵ ops` -> `╵ ╵ api  ╵•╵ web  ╵ ╵ ops` -> `╵ ╵ api  ╵ ╵ web  ╵•╵ ops`
      120 ms/step · 3 frames · transition · 240 ms total · swiss
  `⊙ api  ○ web  ○ ops` -> `○ api  ○ web  ○ ops` -> `○ api  ⊙ web  ○ ops` -> `○ api  ○ web  ○ ops` -> `○ api  ○ web  ⊙ ops`
      30 ms/step · 5 frames · transition · 120 ms total · naught

--- SPIN  (stepper)
  `▁ lo ▼` -> `▲▔▀▄▁▼` -> `▲▀▄▁▔▼` -> `▲▄▁▔▀▼` -> `▲mid ▼`
      10 ms/step · 5 frames · transition · 40 ms total · solari
  `· lo ›` -> `‹mid ›`
      240 ms/step · 2 frames · transition · 240 ms total · swiss
  `· lo ●` -> `●∙◦◦◦●` -> `●◦∙◦◦●` -> `●◦◦∙◦●` -> `●mid ●`
      30 ms/step · 5 frames · transition · 120 ms total · naught

--- BLINK  (textfield)
  `▔na▮me▁▁▁▔` -> `▔na▁me▁▁▁▔`
      1000 ms/step · 2 frames · ambient · 2000 ms total · solari
  `┃na▏me···┃` -> `┃na·me···┃`
      1920 ms/step · 2 frames · ambient · 3840 ms total · swiss
  `○na◉me∙∙∙○` -> `○na∙me∙∙∙○`
      1000 ms/step · 2 frames · ambient · 2000 ms total · naught

--- FLIP  (switch, the motion the contract already had)
  `▼·· OFF` -> `█·· OFF` -> `▁█· OFF` -> `▁▁█ OFF` -> `▁▁▼ ON `
      10 ms/step · 5 frames · transition · 40 ms total · solari
  `│──` -> `━━│`
      240 ms/step · 2 frames · transition · 240 ms total · swiss
  `◉◦◦` -> `●◦◦` -> `∙●◦` -> `∙∙●` -> `∙∙◉`
      30 ms/step · 5 frames · transition · 120 ms total · naught
```

**Read the SPIN row twice.** solari's three in-transit frames are `▔▀▄▁` walking one phase per cell —
that is its split-flap `SPIN` token, the same one its spinner has always used, and it is the riffle
without a single glyph being authored for it. naught's are its lattice dots. swiss draws none.

### The per-language character table

Only the first two columns are DECLARED; everything after them is derived by the engine.

| language | `MOTION_STEPS` | `tempo` | press | travel | spin | blink | flip |
|---|---|---|---|---|---|---|---|
| naught | 3 | 120 | 6f / 120 ms | 5f / 120 ms | 5f / 120 ms | 2f / **2000 ms** | 5f / 120 ms |
| corgi | 1 | 80 | 4f / 80 ms | 5f / 80 ms | 3f / 80 ms | 2f / **2000 ms** | 3f / 80 ms |
| instrument | 3 | 160 | 6f / 160 ms | 5f / 160 ms | 5f / 160 ms | 2f / **2560 ms** | 5f / 160 ms |
| swiss | **0** | 240 | 3f / 240 ms | 3f / 240 ms | **2f** / 240 ms | 2f / **3840 ms** | **2f** / 240 ms |
| industrial | 1 | 60 | 4f / 60 ms | 5f / 60 ms | 3f / 60 ms | 2f / **2000 ms** | 3f / 60 ms |
| nord | 1 | 140 | 4f / 140 ms | 5f / 140 ms | 3f / 140 ms | 2f / **2240 ms** | 3f / 140 ms |
| darkside | 3 | 300 | 6f / 300 ms | 5f / 300 ms | 5f / 300 ms | 2f / **4800 ms** | 5f / 300 ms |
| ledger | 1 | 200 | 4f / 200 ms | 5f / 200 ms | 3f / 200 ms | 2f / **3200 ms** | 3f / 200 ms |
| solari | 3 | 40 | 6f / 40 ms | 5f / 40 ms | 5f / 40 ms | 2f / **2000 ms** | 5f / 40 ms |
| blueprint | 2 | 180 | 5f / 180 ms | 5f / 180 ms | 4f / 180 ms | 2f / **2880 ms** | 4f / 180 ms |

Every transition total is the language's own tempo (**max 300, ceiling 400**); every ambient is
sixteen beats of it taken to the **2000 ms** floor. **Travel is five frames in nine languages and
three in swiss** because its count is the DISTANCE's, not the language's — only the in-transit
samples are the language's to renounce.

### The mutation table — seven mutants, all caught, none crashed

Full log in `prototypes/out/_p59_mut.log`. Baseline and restored both **9192 / 0**.

| mutant | what it breaks | PASS | FAIL | verdict |
|---|---|---|---|---|
| M1 colour sneaks into a frame | the no-colour law | 9159 | **33** | CAUGHT |
| M2 dead-zone duration (+800 ms) | regime + dead zone | 9099 | **93** | CAUGHT |
| M3 single-frame transition | realizability | 8950 | **242** | CAUGHT |
| M4 blink faster than 2000 | the ambient floor | 9190 | **2** | CAUGHT |
| M5 travel skips the between-frame | the travel laws | 9173 | **19** | CAUGHT |
| M6 the anchor is drawn | deceleration + flip identity | 9123 | **69** | CAUGHT |
| M7 the backslash spinner, re-armed | the both-parsers law | 9188 | **4** | CAUGHT |

**M3's FIRST attempt did not fail — it CRASHED the suite at check 90 with zero reds, and that is the
most valuable thing the battery produced.** `verify_language:776` (a pass-49 switch law) did
`fl[-1]` on `flip_frames`' output, which was safe for ten passes only because nothing could make
that list empty. The motion engine can. A dead run is not a green run and it is not a red one
either — it is a suite with nothing to say, which is exactly how pass 49's own mutation table
learned to distrust a renderer that raises. Guarded, re-run, **242 reds.** Three more indexing seats
in the new laws were hardened the same way, before the battery, for the same reason.

**M4's two reds are the shape the law was built to have.** Dropping `AMBIENT_MIN_MS` to 500 does NOT
redden the per-language blink laws, because they READ that constant and stay self-consistent with
it. What fires is the check that PINS the two numbers, and the dead-zone control. A tunable
constant needs a law about the constant; a law that only reads it can be tuned into agreement.

### Two races found and closed while driving the live seats

1. **A stale timer chain could drive a NEW motion.** Pressing an arrow again mid-motion replaced the
   slot but left the old chain armed, so two chains advanced one index and a transition played at
   double speed. The player carries a GENERATION now and a superseded chain returns. The race was
   latent when only the switch animated; **driving four motions from three keys is what made it
   reachable.**
2. **A pre-existing law compared two RENDERS across a key press** (`the set CLAMPS at its last
   option`), and since arrows now start a motion, one capture could land on an in-transit frame and
   the other on a resting one. **It went red once in three runs** — worse than always-red, because
   an intermittent law is a law people learn to re-run. It settles on the language's own `tempo`
   now. (The rename that fix needed is its own small lesson: the local was first called `settle`,
   which shadowed the suite's `settle()` helper and turned every earlier use into a `NameError` —
   caught immediately because the suite stopped at 8272 instead of 9192.)

**One red observed that is NOT explained by this pass, reported rather than buried:** the same run 3
also carried `capture settle timeout: board never painted (instrument @118x30)`. It did not recur in
the six full `verify_language` runs after it (three stability runs plus the three-run battery), it is
the standing intermittent capture race this file already watches, and the settle-headroom gate
reports `worst 4 of 40 over 147 captures` — far from its bound. **It is a watch item, not a clean
bill of health.**

### Next

1. **The skill's motion law needs this pass.** `tui-design/MOTION.md` and `SKILL.md` still say
   "motion changes glyphs, not colours, ≤400 ms" as ONE rule. This increment split that ceiling into
   two regimes with an illegal gap between them, and the entry above is the source. **`MOTION.md`
   also owes the finding that `dim_level` is not a third channel in a terminal** — that is a claim
   the skill currently makes and this pass measured out of existence. Cheapest real work available,
   and it is a skill edit rather than an app one.
2. **Item #36** — the per-step refresh floor, the one thing this pass measured and did not cure. It
   is a CEILING question (`tempo // refresh`), it touches one language's shipped frame counts, and
   it belongs in the motion axis's next opening rather than in a rider.
3. **Item #30 — tabs/segmented as the group scope's next tenants.** Unchanged in priority, and now
   slightly cheaper: `motion_frames`'s `travel` is already group-scoped, so a tab bar arrives with
   its motion rather than owing one.

---

## FIFTY-EIGHTH PASS — THE PROTOTYPE'S TWO CURES GET A STANDING LAW (item #33) — **and the "before" they were measured against had never been on the glass**

**What this pass is.** One increment, three files, one debt. Pass 57 swapped the prototype's two
escape sites to `LG.mark` and filed #33 because `verify_widget` — their home — was outside its
budget. This pass writes the law.

### THE FINDING: pass 57's PRE dump was taken off the glass

`_p57_prove.py` §3 drove `widget_slice/app.py:1404` at **60x30** and printed, for all ten languages:

```
naught/proto-queue       heads_on_glass=[] EATEN=[] [/]-rows=0
corgi/proto-queue        heads_on_glass=[] EATEN=[] [/]-rows=0
...                      (ten of ten, identical)
```

That reads as "no hazard, no defect". It is neither. `#queue` composes only at the WIDGET size class
and it sits LOW. Measured at 60x30 with the same hazard fixture:

| language | `#queue` region | rows on the glass | hazard heads |
|---|---|---|---|
| naught | y=29, h=10 | **1** | none |
| corgi | y=28, h=10 | 2 | none |
| instrument | y=29, h=12 | **1** | none |
| swiss | y=26, h=12 | 4 | none |
| industrial | y=26, h=10 | 4 | none |
| nord | y=25, h=10 | 5 | none |
| darkside | y=25, h=12 | 5 | none |
| ledger | y=25, h=10 | 5 | none |
| solari | y=23, h=10 | 7 | none |
| blueprint | y=24, h=10 | 6 | none |

**Not one language got its queue fully composited, and the hazard rows — which sit below the
calendar block — were on none of them.** Pass 57 wrote the y=29 trap into item #33's stamp as a
warning to the next pass, and its own PRE dump had already fallen into it. The POST at 60x44 was
real; the PRE it was compared against was a blank region.

**The honest PRE is the mutation, below**: with rich's `escape` put back and driven at 60x44, all ten
languages eat `[URGENT]` out of the prototype's queue — the same 10-of-10 the shipped aperture
showed.

### THE LAW — `verify_widget.py`, `escape_laws()`

Ported from `verify_aperture`'s section, with two things changed for measured reasons.

**Surface 1 — `#queue` at 60x44** (`app.py:1404`, `LG.mark(t.title)`). Hazard fixture written by the
suite, not read, so it is order-independent and its due dates are relative to the day it runs.

**Surface 2 — `#cfg-body` on the config screen** (`app.py:799`, `LG.mark(hint_row(...))`), and this
one **needs no fixture at all**. Two of `ConfigScreen`'s bindings carry `key_display="["` and `"]"`,
so `hint_row` derives ` esc/q back · space toggle · [ threshold - · ] threshold + · r refresh` —
**the row contains its own bracket span**, and `[ ` is the worst case in the whole app because rich
never escapes it. The hazard is the row.

**Per language (ten), per surface, four legs:**

| leg | queue | config |
|---|---|---|
| **vacuity A** — the surface is ON the glass: all of its region's rows composited | yes | yes (+ `esc/q back` visible, since `#cfg-body` lives in a `VerticalScroll` and can scroll its hint row out) |
| **vacuity B** — the hazard really rendered | both open titles' tails on the glass | (folded into A: the hint row IS the hazard) |
| **no-leak** — no row carries a literal `[/]` | yes | yes |
| **no-deletion** | `mangled`, case-insensitive | presence of `[ threshold -` and `] threshold` |

Plus the grep-able source rule — `escape(` at zero sites, and `rich.markup` not imported — because
"this string happens to have no bracket in it" is a promise every future edit has to keep at every
call site, while "this module does not call rich's escape" is a claim one search settles.

**Why the config leg is a presence law and not `mangled`.** What Textual eats there is the span from
`[` to the first `]`, and that span CONTAINS the label: `threshold -` disappears with its bracket.
`mangled` looks for a tail surviving without its head, and here there is no surviving tail to find —
it would report clean on a broken row. Said here rather than left as an unexplained asymmetry.

**Why vacuity B counts TAILS and not heads — this is the defect in the law being ported from.**
`mangled` is case-insensitive and must be, because darkside lower-cases titles and blueprint
upper-cases them. That means `[urgent]` and `[URGENT]` fold to the same string, so a head count
against a lower-cased blob is **0 or 2, never 1** — `verify_aperture`'s `len(on_glass) >= 2` is one
hazard counted twice wearing the look of two hazards found. The tails (`ship it`, `rotate keys`) are
genuinely distinct, and exactly two is the right number: three titles go in and `[BLOCKED] audit
keys` rides a Done task, which `_queue_markup` filters out. **`verify_aperture` still carries the
weak form; it was outside this pass's three-file budget and is filed as item #35 rather than fixed
quietly.**

### MUTATION — `prototypes/out/_p58_mut.py`

Reverts `:1404` to pass 57's PRE state (`escape(t.title)` plus the local `from rich.markup import
escape`) and runs the suite. The original source is held in memory and rewritten in a `finally`, so
no `.bak` is left on disk and an exception cannot leave the prototype mutated.

| run | state | exit | PASS | FAIL | what went red |
|---|---|---|---|---|---|
| M0 | cured (baseline) | 0 | **97** | 0 | — |
| M1 | `LG.mark(t.title)` → `escape(t.title)` | 1 | 85 | **12** | 2 source-rule (`escape(` present, `rich.markup` imported) + **the no-deletion leg in all TEN languages** |
| M2 | restored | 0 | **97** | 0 | — |

**Every vacuity guard stayed GREEN in M1**, which is the shape a working guard has: the surface was
still on the glass, both hazard rows still rendered, and only the claim about their CONTENT was
false. A mutation that reds out the vacuity guards too would mean the law was measuring whether the
screen exists, not whether the text survived.

`app.py` restored and re-verified after the run: `LG.mark(t.title)` back at line 1403, zero `escape(`
call sites, file parses clean.

### Suites

| suite | checks | fifty-seventh | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | 8603 | 8603 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | 208 | 208 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | **97** | 24 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 passed (x3)** |

**DIFF SCOPE, measured:** four of the six suites did not move by one check, because nothing outside
`verify_widget.py` was edited. The +73 breakdown: 2 source-rule + 1 probe self-check + 10 languages ×
7 legs.

`test_win_clipboard_roundtrip` PASSED in all three runs (item #22 stays open: its verdict still
depends on whether another process holds the Windows clipboard).

### Open, and honest

* **`verify_aperture`'s vacuity guard is still the weak double-counting form** (new item **#35**).
  Named above, one line to cure, outside this pass's file budget.
* **The 40 app-surface sites are still unswept** — the app half of #32, unchanged.
* **The bracketed row still runs one cell short** (#34), unchanged.
* **The prototype's config seat is guarded at 60x44 only.** The hint row wraps at that width and the
  law reads `[ threshold -` and `] threshold` as contiguous strings; a much narrower screen could
  wrap between the bracket and its label and red-flag a healthy row. Not measured at other widths,
  and said rather than discovered later.

### Next

1. **Item #35** — the tail-count cure in `verify_aperture`, the next time that file is opened.
2. **Item #32's app half** — `modals.py` first (22 sites, all user text), in the real-app work.
3. **The motion batch, item #27** — four tempo questions, one increment, unblocked since pass 55.

---

## FIFTY-SEVENTH PASS — THE ESCAPE SWEEP'S **DESIGN-SURFACE REMAINDER** (item #32, split) — **the census under-reported it twice**

**What this pass is.** Pass 56 swept `language.py` and counted 44 more sites it could not reach
(item #32). This pass sweeps only the ones that belong to the DESIGN surface and classifies the
rest, on the user's scope rule: **this worktree is a design SHOWCASE**, so `modals.py`, `views.py`
and `views_widget.py` are the real app's functional surfaces and stay censused for the app work.
Four sites swept, forty re-stamped.

### THE FINDING — the census was right that these were unswept and wrong about how bad they were

Two corrections, both measured before anything was edited (`prototypes/out/_p57_prove.py`, PRE dump
kept at `_p57_pre.txt`):

1. **The aperture's queue is not a three-language defect, it is a TEN-language one.** Pass 56 drove
   naught, blueprint and nord and reported three. Driven across `themes.ORDER`, **all ten ate
   `[URGENT]` out of the queue** — every language this repo ships, on the surface the aperture calls
   "what's next".

2. **`hero.py:250` is not "the hero's detail line", it is the user's TITLE.** The census recorded it
   as one site without saying what text it carries. `engine.sig_deadline` builds its `Reading` with
   `detail=t.title` (`engine.py:100-105`), so **what the hero prints under its numeral is the
   nearest deadline's title** — class (a), user text, and it was live: swiss, industrial and
   darkside were each printing a bare `rotate keys` where `[URGENT] rotate keys` was typed.

```
PRE  (rich's escape)                          POST (mark)
naught     '◦  rotate keys        '           '◦  \[URGENT] rotate keys   '
corgi      '[1]  rotate keys      '           '[1]  \[URGENT] rotate keys '
darkside   '·  rotate keys    1d!'            '·  \[URGENT] rotate keys 1d!'   <- queue, 10/10
swiss      'rotate keys      ────────'        '\[URGENT] rotate keys ──────'   <- hero, 3/3
industrial 'rotate keys              '        '\[URGENT] rotate keys       '
```

(The `\[` is the escape in the MARKUP; the glass shows `[URGENT] rotate keys`.)

### THE FIXTURE HAD TO MOVE ONE DATE, and the reason is the law's own

Pass 56's hazard fixture gives its three titles ONE due date, so `sig_deadline`'s `min` hands the
hero the FIRST of them — `[urgent] ship it`, which is the title rich escapes **correctly** (`[u`
looks like a tag to it). Measured that way the hero's site reads clean while the queue beside it is
eating text, and a hero law written on that fixture is green and cannot fail. The upper-cased title
is the hazard rich passes through, so it is the one made nearest (`due -1`). **A fixture that
reaches a seat is not the same thing as a fixture that reaches its DEFECT**, and this is the second
time in two passes that the difference has been the whole finding.

### THE SITE TABLE — four swept, and one of them is class (b)

| file:line | seat | text it carries | class | PRE, driven |
|---|---|---|---|---|
| `taskboard/aperture.py:386` | `_queue_markup` row | `t.title` in the shipped queue | **(a)** | **10 of 10 EAT `[URGENT]`** |
| `taskboard/hero.py:250` | `draw`'s `detail` | the nearest deadline's TITLE | **(a)** | **3 of 10 EAT** (7 do not compose it) |
| `prototypes/widget_slice/app.py:1404` | the prototype's queue | `t.title` | **(a)** | **10 of 10 EAT**, at 60x44 |
| `prototypes/widget_slice/app.py:800` | config hint row | `hint_row(BINDINGS)` — key names | (b) | clean, and swept anyway |

Class (b) is swept for pass 56's reason, unchanged: "this literal happens to have no bracket in it"
is a promise every future edit must keep at every call site, and "this module does not call rich's
escape" is a claim ONE GREP settles. All three modules now have zero `escape(` calls and no
`rich.markup` import, and the two shipped ones have that asserted.

**The prototype's queue was never under any law, and the reason is worth recording**: `#queue`
composes only at the WIDGET size class (`app.py:1308`), and `verify_language`'s hazard leg drives
that app at 118 cells, where it is hidden. It is also invisible at 60x30 — the region starts at
y=29 — so the PRE dump had to be re-taken at 60x44. **A surface that is off the glass reports
clean.** That is the same instrument lesson as pass 56's case-sensitivity bug, met at the geometry.

### THE LAW — in `verify_aperture`, which is the shipped seat's home

A new section, `== THE ESCAPE SWEEP: the shipped seat calls ONE escaping`, **+57 checks (151 →
208)**:

* the **grep-able source rule** for both shipped modules (zero `escape(`, no `rich.markup` import);
* a probe self-check that the surface driven is the `ApertureScreen`;
* per language, over BOTH regions (`#ap-panel`, `#hero`): no literal `[/]` on the glass, and **no
  bracketed head EATEN** — a row showing a title's tail without its head is user text the parser
  deleted. Case-insensitive, for pass 56's measured reason;
* a **per-language vacuity guard** that the hazard is really on the queue's glass;
* a pin that the hero under test is the DEADLINE's reading and its detail is the typed title — which
  is the fact that makes `hero.py` escape at all, and the thing that would silently stop being true
  if `sig_deadline` ever stopped carrying a title.

**What the law does NOT cover, stated rather than implied.** Seven of the ten languages do not
compose the detail line into the hero panel at 118x34 — their row budget spends it elsewhere. Their
hero leg is a REGRESSION guard, not a hazard test. The vacuity check counts the three that do
(`3/10: swiss, industrial, darkside`) and names them, so a layout change that quietly drops the last
one turns this section red instead of turning it into decoration.

### MUTATION — five rows, four on the glass, and the control did its job

Base 208. As in pass 56 the driver carries a second column, because every revert also trips the
cheap source grep: `glass` counts reds whose NAME carries `/queue:` or `/hero:` — something a user
would have seen.

| mutation | red | on the GLASS |
|---|---|---|
| M1 the aperture's queue reverts (the live defect, put back) | 12 | **10** |
| M2 the hero's detail line reverts | 5 | **3** |
| M3 `hero`'s `mark` hollowed out to rich's escape, call site untouched | 4 | **3** |
| M4 the queue stops escaping at all (leaks a tag instead of eating one) | 21 | **20** |
| M5 [driver control] `_queue_markup` raises | — | DEAD RUN, correctly reported |

M1 is the row this pass came for: reverting one line turns ten languages red on the glass. M4 is the
other direction and turns twenty, because it fails BOTH halves of the law at once.

### A SHAPE THIS SWEEP DID NOT CHANGE, and it is measured rather than assumed

Both queue seats escape and THEN slice: `mark(t.title)[:tw]:<{tw}`. The backslash is nothing to the
parser and a character to the slice and the pad, so **a title with a bracket renders one cell short
of its column** — measured on naught at 118x34: `112` in a `113`-cell budget, for both hazard rows.
This was already true of `escape` (it adds the same backslash to `[urgent]`), so the swap neither
introduces nor worsens it — what the swap changed is that the upper-cased case moved from *deleted
at full width* to *intact and one cell short*, which is the trade this pass wanted. Pass 44's "every
queue row closes EXACTLY on the panel's measure" law stands on the bracket-free fixture and is not
weakened; the bracketed case is filed as **item #34** rather than fixed here, because fixing it
means slicing before escaping and padding on VISIBLE width — a mechanism change at a seat that was
explicitly out of surgical scope.

### Suites

| suite | checks | fifty-sixth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | 8603 | 8603 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | **208** | 151 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 24 | 24 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 passed (x3)** |

**DIFF SCOPE, measured:** `verify_language` did not move by one check. That is the evidence the swap
is a no-op for text with no bracket in it (pass 56 measured the byte identity) and that the seats
touched here — the aperture's queue and the hero's detail — are not seats that suite drives. The +57
are the new section, and the breakdown is 4 source-rule + 1 probe + 10 languages × 5 + 2 pins.

`test_win_clipboard_roundtrip` PASSED in all three runs again (item #22 stays open: its verdict
still depends on whether another process holds the Windows clipboard).

### Open, and honest

* **The prototype's two swept sites have no standing law** (new item **#33**). They are measured
  before and after in `_p57_prove.py` §3 (10 of 10 driven, cured), but `verify_widget` is their home
  and it was outside this increment's seven-file budget. A cure with no guard can regress.
* **Forty sites are still unswept** — the app-scope half of #32, re-stamped rather than closed.
* **The bracketed row runs one cell short** (new item #34), measured above.

### Next

1. **Item #33** — pin the prototype's two sites in `verify_widget` (one section, the fixture and the
   `mangled` helper already written twice).
2. **Item #32's app half** — `modals.py` first (22 sites, all user text, at the surface the user
   types it), in the real-app work. The recipe is proven twice now: swap to `LG.mark`, drop the
   import, assert its absence, and drive the hazard fixture at the surface with the no-leak AND
   no-deletion pair, case-insensitive, with a vacuity guard per surface.
3. **The motion batch, item #27** — four tempo questions, one increment, unblocked since pass 55.

---

## FIFTY-SIXTH PASS — THE ESCAPE SWEEP (item #25) — **and the defect was not the one that was predicted**

**What this pass is.** The last live defect this file knew about: twenty-three `rich.markup.escape`
call sites in `language.py`, escaping USER text with RICH's rules while the app renders with
TEXTUAL's parser. Item #25 predicted a `[/]` leak on a task titled `[urgent] ship it`, the way
industrial's switch chrome leaked for four passes. **The prediction was wrong in the direction that
matters: `escape` was not leaking a tag, it was DELETING the user's words.**

### THE FINDING, measured before anything was swept (`prototypes/out/_p56_prove.py`, PRE dump)

A title typed `[urgent] ship it` is escaped CORRECTLY by rich — `[u` looks like a tag to it, so it
comes out `\[urgent] ship it` and both parsers agree. **Then a language upper-cases it.** `[URGENT]`
does NOT look like a tag to rich (its rule is `[` followed by `[a-z#/@]`), so rich passes it through
untouched — and Textual, whose tokenizer is not rich's, reads it as a tag and swallows it. Three of
the ten languages upper-case their card titles, and all three were printing this, live, on the board:

```
corgi       '[1]  SHIP IT'          <- the task is titled `[urgent] ship it`
solari      '00   SHIP IT'
blueprint   'SHIP IT'
```

No leak. No error. No `[/]` anywhere — **which is exactly why the config screen's no-leak law could
never have caught it, and why widening THAT law alone would have closed the item without fixing the
defect.** The law had to grow a second half: a row that shows a title's TAIL without its bracketed
HEAD is user text the markup parser deleted.

### THE SITE TABLE — all twenty-three, classified, and why class (b) was swept anyway

Twenty-three lines, twenty-six calls (three lines call it twice). Class **(a)** carries text a user
typed; class **(b)** carries language or app literals that have no bracket in them today.

| # | line | seat | text it carries | class |
|---|---|---|---|---|
| 1 | 109 | `_fit` (module) | task titles + phase names, for NINE kits | **(a)** |
| 2 | 1039 | `Kit.card_rows` | `proj · phase` metadata row | **(a)** |
| 3 | 3357 | `Swiss._entry` | project name | **(a)** |
| 4 | 3906 | `Nord.detail_rows` | the title, LETTERSPACED — `display_cap` puts a space after the `[`, which is the worst case: rich never escapes `[ ` | **(a)** |
| 5 | 3913 | `Nord.detail_rows` | field values (proj / phase / prio) | **(a)** |
| 6-7 | 4276 ×2 | `Ledger._cell` | posting description = the title; account = the project | **(a)** |
| 8-9 | 4285, 4286 | `Ledger._leadered` | `title.upper()` | **(a)** |
| 10 | 4389 | `Ledger.sect` | section note (`"3 open"`, `"12 weeks · 1d/cell"`) | (b) |
| 11 | 4699 | `Solari.cell` | flap faces: due chips, two-digit figures, mode words | (b) |
| 12 | 4707 | `Solari.band_row` | section title/note, upper-cased | (b) |
| 13-14 | 4719 ×2 | `Solari._pad` | `title.upper()` | **(a)** |
| 15-16 | 5221 ×2 | `Blueprint._pad` | `title.upper()` | **(a)** |
| 17 | 5333 | `Blueprint.card_rows` | the span, built from this language's own glyphs | (b) |
| 18 | 5337 | `Blueprint.card_rows` | proj / phase / prio, upper-cased | **(a)** |
| 19-20 | 5395, 5397 | `Blueprint.sect` | section title and note | (b) |
| 21 | 5443 | `Blueprint.tile_row` | engine reading values | (b) |
| 22-23 | 5473, 5475 | `Blueprint._mode_strip` | the view names (`board`, `lanes`, …) | (b) |
| 24-26 | 5580, 5585, 5587 | `Blueprint.title_block` | `SHEET`, today's ISO date, the work figure, the mood word | (b) |

**Fourteen calls are class (a); twelve are class (b); all twenty-six were swept, and the reason is
the one that makes this checkable.** "This literal happens to have no bracket in it" is a promise
every future edit has to keep at every call site. "This module does not call rich's escape" is a
claim ONE GREP settles — so the import is gone, and the suite asserts its absence. A class-(b) seat
is exactly where the next `[` arrives without anyone thinking about it; industrial's switch chrome
WAS a class-(b) literal until someone put a bracket in a glyph table.

### THE BYTE-IDENTITY CHECK FOUND A REAL DISAGREEMENT, and it is reported rather than assumed away

The brief said to verify that `mark` and `escape` agree on bracket-free text. **They do not.** Rich's
`escape` has a rule `mark` does not: text ending in a single backslash gets a second one. It is the
ONLY disagreement on bracket-free text in the corpus, and the sweep ran anyway for a measured reason:

* the seat is always `f"[tone]{...}[/]"` — a close tag right behind the text;
* under TEXTUAL, `\` in front of `[` escapes the bracket whether or not another `\` precedes it, so
  **both** escapings print a raw `[/]` there;
* five encodings were searched (`_p56_prove.py` §3b) and none closes the tag under both parsers.

So the case is **glass-neutral**: the swap neither fixes nor worsens it. It is filed as **item #31**
rather than left in a comment, and the suite asserts the whole finding — including that both
escapings leak — so a future rich or Textual that changes it goes red here.

### THE LAW, WIDENED — and an instrument defect found while widening it

`verify_language` grew a section (`== THE ESCAPE SWEEP`) with four parts: the grep-able source rule,
the byte-identity measurement, three pure-function CONTROLS that reproduce the defect and its cure on
every run, and **the screens**. A hazard fixture (`_fixture_hazard.json`: titles `[urgent] ship it`,
`[URGENT] rotate keys`, `[BLOCKED] audit keys`, project `[QA] Web`) is driven through the board, the
config screen and the gallery in ALL TEN languages, with a probe self-check that names the screen
class it actually captured and a vacuity guard that the hazard is on the board's glass.

**The instrument defect:** the head/tail comparison was first written case-SENSITIVE, and it reported
darkside's perfectly intact `[urgent] rotate keys` as eaten — because darkside LOWER-cases titles and
the fixture's word is upper-case. A title is intact in whatever case its language prints it, so the
comparison is case-insensitive and says so.

**What the law does NOT cover, stated rather than implied.** The shipped APERTURE is not asserted
here: `taskboard/aperture.py:386` still escapes `t.title` rich's way and is outside this increment's
file budget. It is MEASURED in the prover (§5) instead — naught, blueprint and nord all EAT
`[URGENT]` out of the aperture's queue today — and filed as **item #32**.

### MUTATION — six rows, and one of them was the driver's own defect

Base 8603. The driver gained a column: every revert trips the cheap source-level grep, so a red count
alone proves nothing about the law this pass came for. The extra column counts reds whose NAME
carries `/board:`, `/config:` or `/gallery:` — i.e. something a user would have seen.

| mutation | red | on the GLASS |
|---|---|---|
| M1 `_fit` reverts (the shared title fitter, nine kits) | 8 | **6** |
| M2 solari's `_pad` reverts | 4 | **2** |
| M3 blueprint's `_pad` reverts | 4 | **2** |
| M4 [corrected] all 43 call sites back to rich's escape | 43 | **14** |
| M5 `mark` itself reverts to rich's escape (pass 52's M10) | 47 | **14** |
| M6 [driver control] `Kit.card_rows` raises | — | DEAD RUN, correctly reported |

**M4 was written wrong the first time and the driver said so instead of scoring it.** A global
`mark(` → `escape(` also renamed `wordmark(` and the function's own `def`, so the module raised on
import and the run died at 1 PASS. A mutation that breaks the build tests nothing; the corrected row
puts the two collateral names back so that what changes is exactly the ESCAPING and nothing else.
This is the same lesson pass 55 wrote down about dead runs, met from the other side.

### Suites

| suite | checks | fifty-fifth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **8603** | 8494 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | 151 | 151 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 24 | 24 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 passed (x3)** |

The +109 is this pass's section. **DIFF SCOPE, measured:** the sweep was run first and the suite
re-run BEFORE any new law was written — **8494, 0 FAIL, unchanged**. Not one existing check moved,
because the standing fixtures' titles have no bracket in them. The only renders that changed are
renders of text containing a bracket, which is the whole point. Settle headroom worst **5 of 40**
over 147 captures (was 4 of 40 over 137 — ten more captures, one more iteration).

`test_win_clipboard_roundtrip` PASSED in all three runs again (item #22 stays open: its verdict
still depends on whether another process holds the Windows clipboard).

### THE READ-ONLY CENSUS — the same class in the files this increment could not touch

Grep-verified, not edited:

| file | sites | what they carry |
|---|---|---|
| `taskboard/modals.py` | **22** | project names, task titles, notes, phases, urls — every modal the user types into |
| `taskboard/views.py` | **14** | titles and project names in agenda / gantt / swimlanes / calendar |
| `prototypes/widget_slice/views_widget.py` | 4 | the prototype's copies of the same views |
| `taskboard/aperture.py` | 1 | `t.title` in the shipped queue — **measured eating `[URGENT]` today** |
| `prototypes/widget_slice/app.py` | 2 | the prototype's queue title, and a hint row (app literal) |
| `taskboard/hero.py` | 1 | the hero's detail line |

That is **item #32**, and it is bigger than the one just closed: `modals.py` is where the user types
the text in the first place.

### Open, and honest

* **The trailing backslash is not cured** (#31) and cannot be, on Textual's side, at a seat where a
  close tag follows the text. It is asserted, not fixed.
* **The other 44 sites are not swept** (#32). This increment's budget was five files and it used all
  five.
* **The gallery and config legs of the new law are REGRESSION guards, not hazard tests** — board data
  does not reach those screens, and the vacuity guard is therefore asserted for the board only. Said
  in the section's own comment rather than left for a reader to discover.

### Next

1. **Item #32 — the census sweep**, `modals.py` first (22 sites, all user text, and the place the
   text is typed). Same mechanical swap, and the law is already written: point the hazard fixture at
   a modal and at the aperture.
2. **The motion batch, item #27** — four tempo questions, one increment, unblocked since pass 55.
3. **The exemplar screen, item #3.**

---

## FIFTY-FIFTH PASS — the COMPONENT CONTRACT, increment 8 (stepper · WRAP VS CLAMP) — **THE FAMILY IS CLOSED**

**What this pass is.** The eighth and last increment, and the first whose question is not what a
range IS but what happens at its **END**. Everything before it asked how a value is shown; this one
asks what the control says when there is nowhere left to go.

### THE FIRST RULING — a stepper and a radio are ONE CHOICE with TWO MECHANISMS

The brief's opening question, and the answer is the one the registry's own history predicts once you
say which half is which.

**TWO REGISTRY ENTRIES, because the registry describes ANATOMY.** A radio ITEM is a well and a mark
(`("main", "knob")`) drawn N times; a stepper is a WORD BETWEEN TWO STEPS, two affordances whatever
the set's size. Those are different slots in different numbers, and this registry's one standing
refusal is *identical parts with different anatomies*.

**ONE CHOICE MODEL, because `group_states` already owns it.** `Kit.stepper` reaches the radio's
seat with the set's size and its index, and takes the shown option's state from it. Three
consequences follow rather than being written: an out-of-range selection **raises here for the
reason it raises there** (a stepper showing no option is a set with nothing set); there is no per-
item boolean, so the two mechanisms cannot disagree about what is chosen; and the option's tone is
the group's answer, so a disabled stepper's word reads dead exactly as a disabled radio item's does.

**AND IT IS THE INVERSE OF EVERY COLLISION THIS REGISTRY HAS MET.** The switch shares the slider's
tuple and differs in the value's RANGE; the scroll bar shares the bar's and differs in its ARITY —
both were separated by a DECLARED FACT. Here the parts differ and the value model is the same, and
a shared value model is not a registry fact at all: it lives one level above the registry, exactly
where the radio put it. Same boundary, read from the other side.

### THE SECOND RULING — wrap vs clamp is an ARGUMENT, not a registry fact

A registry fact says something about EVERY instance of a component. Wrap is not true of every
stepper; it is true of every **RING**. The hours of a day wrap, a set of worker groups does not, and
both are steppers. **The codebase had already settled this before the seat existed** and holds both
readings today: `action_cycle_theme` and `action_move` take `% n` because a list of languages and a
column of rows are rings; `action_pick` clamps because "an N-of-M control's ends are where the set
ends". `WRAPPING = ("stepper",)` would have declared a property of the CALLER'S DATA in the
component's registry, which is the third-family smell pass 54 warned the next increment about.

**CLAMP IS THE DEFAULT** — a caller who says nothing does not get their choice teleported from the
last option to the first.

**AND THE END IS VISIBLE IN SHAPE, with no new state and no colour.** The composer asks `step_index`
whether a step EXISTS, and **a seat with no step draws GROUND** — `main`, the word this registry
uses for exactly that everywhere else. So a clamped stepper at its floor draws its floor, a wrapping
one never does, and the difference is a PART TAG before it is a glyph and a glyph before it is
anything else. Greyscale the two and they differ at the ends and agree in the middle.

**ONE SEAT FOR THE RENDER AND THE BEHAVIOUR.** `step_index(i, n, d, wrap) -> int | None` answers
both "where does this step go" and "is there one", so **a stepper cannot draw a live arrow that does
nothing** — not "does not", cannot, by construction, which is the switch's checked-bit discipline
applied to an end. The RAISE stays at `group_states` (arithmetic clamps; a renderer that died on a
caller's number would take the surface with it) and the two refusals are one refusal at the seat
that owns the invariant.

### THE ANATOMY — one new part, no new declared fact, and the halves are the directions

`COMPONENT_PARTS["stepper"] == ("main", "step")`. `step` is ONE new part and not two: the caret's
argument re-run and coming out the other way — a state cannot pick out one cell, but the two steps
are not at N seats, they are at exactly TWO, and **a two-cell part whose glyph is an EVEN string
read at its halves** is the convention this file already uses twice (the button's walls, the field's
ground). Declaring `less` and `more` would have bought two registry entries for a distinction the
cell's POSITION already carries.

**NO NEW DECLARED FACT, which is pass 54's warning answered rather than ignored.** `CHECKABLE` and
`VIEWED` are byte-identical to what the scroll bar left them. What grew was `GRIPS` — a step is
pressed, so it is the part under the finger — and that is the CHEAP kind of growth: a tuple gained
an entry and `actuator` did not gain a term. It is the seat pass 53 built for exactly this.

**Two derivations took a third term, and the pair they now make is the content ruling.**
`has_interior` = extent | field | **series** (three ways to say "there is more than one place the
value can be"); `has_value` = extent | **series** | bit. The one term in each that is not in the
other is the whole ruling: a **caret** indexes cells the CALLER fills, so a field has an interior and
holds no value; a **step** chooses among seats the REGISTRY counts, so a stepper holds one. Every
term is a PART already declared — an enumeration of ANATOMIES is bounded by the registry, where a
list of NAMES is not, and that is why a `RANGED` tuple was refused.

**EDITED IS THE STEPPER'S HOME, derived and not granted.** A grip AND an interior AND not a boolean.
On a slider EDITED means "the arrows now move the value"; here the arrows ARE the component, so this
is the state the axis was built for — and the one LVGL's touch corpus styles 0 times out of 1848.

**`wrap` IS A RANGE WORD, and the boundary is asserted off `inspect.signature`.** `caret` and `size`
default to `None` because they are STATE the caller may or may not have; a third of those would mean
restructuring (pass 54's warning). `wrap` defaults to `False` because it is a fact about the SCALE,
standing beside `lo` and `hi`. The law says the optional STATE arguments are still exactly two.

**AND THE SHOWN OPTION IS CONTENT** — the button's ruling at its third component (a label, a value,
an option). `has_value` is true and yet **nothing is printed beside it**: what a stepper reports is
standing in the middle of it, in the caller's own bytes, byte for byte, never recased and never
shortened. The field is reserved for the WIDEST option in the set (Bodmer T2), so spinning cannot
move the control's edges — the one defect only this component can have.

### THE LIVE SEAT — the narrow config row stops renouncing its control

Read for, and it was already there wearing a renunciation. The config screen's worker group is ONE
choice: wide, a radio set with every option named; narrow, `_group_word` — the group printed as
TEXT, the control given up, honestly, because a set drawn with options missing is a different set.
**A stepper is exactly that thing done as a control**, so the narrow screen now changes MECHANISM
instead of giving up: same `WORKER_GROUPS`, same single index, same `action_pick`, one option on
screen. It **clamps**, and not by preference — `action_pick` clamps, so the render is handed the
same reading, and at `fast` the step back is GROUND on the live screen.

**The threshold row was read for and REFUSED, and the verdict is said rather than assumed.** `[`/`]`
spin `s.threshold`, which looks like a stepper — but that value is a MAGNITUDE on a floating scale
(`hi = max(10, threshold * 2)`) with no ceiling, and it is already drawn on a slider whose EDITED
state says the keys are ranging through it. A stepper needs ends to have an end behaviour; that row
has one end and no other. Converting it would have been a demo.

**`value_at` DID NOT get its first real caller, and pass 54's prediction is reported falsified rather
than satisfied.** A stepper over a named set has no scale: its positions ARE the options, and
"the value at index i" is `options[i]`, a list lookup and not arithmetic. Inventing a numeric stepper
to give `value_at` a caller would have been the dead metadata this file has refused four times.
`value_at` remains inverse-only, used by the round-trip laws.

### Per-language mechanism — the STEP is not the KNOB, and the GROUND is where a step is not

Scoped `stepper.main` / `stepper.step` in all ten, five states each, both strings EVEN and the two
the SAME WIDTH in every state — the anti-jiggle reservation at the glyph table itself, because a
dead end that was narrower would move the word the moment you reached a floor.

| language | step | ground | the mechanism |
|---|---|---|---|
| nord | `-+` | `··` | inherits the environment — the terminal's own minus and plus, chevrons under the finger |
| naught | `●●` | `··` | **the language that cannot draw an arrow**, said out loud: the lattice is one round pixel at a size, so DIRECTION is the SEAT and the pixel carries the state |
| corgi | `▄▄▄▄` | `▁▁▁▁` | **its native habitat** — the parameter keys of a numbered panel, doubled; a GHOST segment where a key is dead, never hue |
| instrument | `⡄⢠` | `⠁⠁` | the register's detents: dot rows weighted to the side they step toward, on the baseline rail |
| swiss | `‹›` | `··` | the guillemet — punctuation before it is an ornament; weight (`██`) for the press |
| industrial | `<>` | `..` | ASCII and coded, and the ROUND BRACKET LAW reaches here too: `()` is DEAD, an absent step is a bare seat |
| darkside | `◂▸` | `▁▁` | the port seen edge-on — its radio's own mark, because it is the same choice; fill inversion under the press, nothing boxed |
| ledger | `▪▪` | `┊┊` | brought back / carried forward in a ruled column; the tally pointer arrives with the cursor |
| solari | `▲▼` | `▁▁` | the rank turning one card either way — caught mid-turn (`██`) on the press; an end is the bare seam |
| blueprint | `┤├` | `··` | terminators turned inward on a schedule; **nothing filled and nothing boxed** survives its sixth component |

### Verification — 7752 -> **8494** (+742)

Stepper laws: the registry (a new anatomy, no new fact, `GRIPS` grown, the parts-differ argument
against the radio) · the `has_value`/`has_interior` pair · the signature boundary (`wrap` is a range
word, the state args are still two) · registry CONTROLS (a probe tuple gets the whole axis; take
`step` out of `GRIPS` and the component becomes a readout) · `step_index` PROPERTY laws at four set
sizes (the ends have no step off, every interior seat has both, a ring has no end, the ends join,
the identity, every step lands inside the set, **walking the set reaches every seat and stops**,
walking a ring returns after exactly n) · the choice model (source + **call recorder** + the
unification at every index and control state + three out-of-range refusals **asserted by exception
TYPE**) · per language: scoped glyphs, even strings, equal widths, two channels in every state, two
cells, the tags at floor/middle/ceiling, wrap draws no ground anywhere, the two readings differ in
greyscale at the ends and agree in the middle, **the whole render composed from the DECLARED glyph
table** at every state × seat × reading, the word byte-for-byte, ONE WIDTH across the set, `w` as a
minimum both ways, five states pairwise distinct with EDITED ≠ FOCUSED, DISABLED shape-marked,
**the grip tone asserted against the SLIDER'S KNOB rather than against `accent`** (one language
rations its red and the ration must reach this component too), one accent at a clamped floor and two
on a ring, two-parser, nothing printed beside it · cross-language distinctness and stepper ≠ radio ·
three kit-subclass controls · the gallery seat · **the LIVE seat, asserted against `action_pick`'s
own source**.

**Mutation table: 14 real rows, ALL CAUGHT; 1 driver control, DEAD RUN as designed.** Vacuity-proved
first — all 15 CHANGE an observable signature (`prototypes/out/_p55_prove.py`, budgeted as a file of
this increment).

| # | mutation | red |
|---|---|---|
| M1 | end behaviour SWAPPED — the seat wraps whatever the caller asked | 60 |
| M2 | the affordance IGNORES the end — a live step at a clamped floor | 153 |
| M3 | the DEFAULT flipped to wrap on the kit method | 31 |
| M4 | the CHOICE MODEL desyncs — the stepper computes its own bit | 6 |
| M5 | the two HALVES swapped — the steps point the wrong way | 144 |
| M6 | `has_interior` forgets the series — EDITED taken away | 45 |
| M7 | `GRIPS` loses `step` — the stepper becomes a readout | 57 |
| M8 | the stepper is given the CHECKBOX'S TUPLE | 376 |
| M9 | `has_value` forgets the series — the index is refused | 125 |
| M10 | the field measured on the CURRENT option (jiggle) | 220 |
| M11 | the WORD is shortened to the field | 242 |
| M12 | nord's step drawn as its ground | 4 |
| M13 | the gallery block hand-lists its states | 10 |
| M14 | the LIVE SEAT wraps while `action_pick` clamps | 30 |
| M15 | *[driver control]* `Kit.stepper` raises | DEAD RUN detected |

**ROUND ONE HAD FOUR DEAD RUNS AND ONE HOLE, and both classes are lessons this file has already
written once.**

- **Four DEAD RUNS (M4, M6, M7, M8), and three of them were the SAME defect for the third time: an
  oracle dict keyed by the DERIVED axis.** Pass 52's mutation GREW the axis and threw `KeyError`;
  pass 53's SHRANK it and threw `KeyError`; this pass's three registry mutations shrank it again and
  a `greys[EDITED]` lookup killed the run before it could report anything. **The cure is not a
  `.get()` — the membership IS the claim**, so the laws now assert `{EDITED, FOCUSED} <= set(greys)`
  and read red instead of raising. The fourth (M4) was a `try/except ValueError` around a call that,
  mutated, raised `IndexError` instead: **catching only the exception you expect lets the wrong one
  kill the run.** The type is now part of the assertion, and an `IndexError` out of a list lookup
  reads red — which is also the sharper law, because it says WHERE the refusal comes from.
- **One HOLE, and it was the one that mattered (M14).** A live seat drawn `wrap=True` while
  `action_pick` CLAMPS survived every law in the block, because every one of them asked the LANGUAGE
  what it draws and none of them asked the SCREEN. **The stepper's whole ruling is that the render
  and the keys are one reading, and nothing was checking it.** Cured with a section that reads
  `action_pick`'s own source for the clamp and asserts the live row is byte-identical to this
  language's `wrap=False` stepper AND different from its `wrap=True` one — 30 red, and it took M3
  from 1 red to 31 on the way, because the live seat is the only caller that omits the default.

**THE VACUITY PROVER EARNED ITS BUDGET ON THE WAY IN.** M3 was first written against `step_index`'s
own `wrap=False` default and the prover called it **VACUOUS** — correctly: no caller ever reached
that default, because both composing seats state their reading. The default was therefore **deleted**
rather than the mutation retargeted quietly: it was dead metadata, and `step_index` now takes `wrap`
as a required argument, with a law asserting it has no default and that the two seats a caller
really does omit it at still do. The seat that DECIDES an end is always told which end it is
deciding.

**M12's 4 red is thin and is said so**, exactly as pass 54's M11 was: a one-language glyph collision
has few laws that can see it, because every per-language law reads PART TAGS and those survive a
language drawing two parts identically. The honest widening remains a cross-component greyscale law
rather than more stepper laws.

**A SENTENCE FROM PASS 51 WAS RETIRED RATHER THAN AVERAGED.** The radio's clamp law carried "a group
that wraps is a stepper". That is wrong, and this increment is what proves it: **what makes a control
a stepper is showing ONE option, not wrapping** — wrap belongs to the RANGE and is the caller's, and
this app's own stepper clamps at that very seat on that very key. The check now says so in place.

**Suites at closure — THREE back-to-back full runs, identical every time.**

| suite | checks | fifty-fourth | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **8494** | 7752 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | 151 | 151 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 24 | 24 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **137 passed (x3)** |

**THE PYTEST ROW CHANGED AND IT IS NOT A FIX — it is the environment.**
`test_win_clipboard_roundtrip` PASSED in all three runs of this pass and failed in all three of the
last five passes. Nothing in `tests/` or `taskboard/app.py` was touched; the Windows clipboard was
simply available this time. **Item #22 stays OPEN**: a test whose verdict depends on whether another
process holds the clipboard is exactly the test that teaches a suite to be ignored, and it still has
no skipif and no mock.

**Flake watch.** Nothing fired — not in the fifteen suite runs of the three sets, not in the
twenty-one mutation runs, not in the two vacuity-prover runs. Settle headroom stayed at **worst 4 of
40**, unchanged for six passes.

### THE COMPONENT FAMILY IS CLOSED — what the contract covers, and what is still OWED

**Covered, all eight in one registry with zero hand-listed states:** slider · bar · switch ·
checkbox · radio · button · text field · scroll bar · stepper. Five anatomies (extent, presence,
field, window, series), three declared facts in two families (`GRIPS` about parts; `CHECKABLE` and
`VIEWED` about the value), one group scope above the registry (`group_states`), three mechanism
seats (`value_pos`/`value_at`, `view_pos`/`view_start`, `step_index`), and one composer.

**Still OWED, read against the skill's own inventory (`COMPONENTS.md`, "the full inventory"):**

- **select / dropdown.** The skill's row pairs it with the stepper and only the stepper is built. It
  is the first component whose value is not on screen at all until it is opened — a POPUP, which is
  a surface question before it is a component one, and this contract has never drawn one.
- **tabs · segmented, as the group scope's next tenants.** They are shipped as pre-contract kit
  methods and the radio pass named them: "a segmented control and a tab bar are the same fact about
  siblings wearing different glyphs". Bringing them in is a registry entry plus a glyph table each,
  and it would give `group_states` a third mechanism — the honest test of whether that seat is a
  seat or a radio feature.
- **date / cell picker** — PARTIAL: the calendar grid exists (`cal_cell`), the PICKING state does not.
- **`invalid`** (item #26) — named, argued, not built: a severity on the value, structurally a BIT
  that combines like CHECKED, and it would belong in a `VALIDATABLE` tuple beside `CHECKABLE`.
- **Motion** (item #27) — the button's press has no intermediate frames, the radio's mark does not
  travel between siblings, the caret does not blink, and **the stepper adds a fourth: the option
  does not move as it is spun.** One tempo question now asked FOUR times.
- **An overflow mark for the text field** (#28) and **an axis fact** (#29) — both priced, both
  unasked-for.

### Next — three candidates, and the recommendation is the DEFECT before the features

1. **Item #25, the two-parser hazard at the other ~25 `escape()` sites** (recommended, first). The
   component seats are cured with `mark`; card titles, notes, hero captions and tile values are not,
   and **the text they carry is the USER'S** — a task titled `[urgent] ship it` leaks a raw `[/]`
   onto the glass exactly as industrial's switch chrome did for four passes. It is a mechanical swap
   plus widening the no-`[/]` law from the config screen to every screen the suite drives. A live
   defect on user data outranks a feature, and this is the last one this file knows about.
2. **The motion batch, item #27** (second). It is now unblocked by its own trigger — "revisit when
   the component track is otherwise closed", and it is closed. Four tempo questions, one increment,
   and `flip_frames` is the only motion the contract has.
3. **The exemplar screen, item #3** (third). The skill demands "render, don't label" of everyone but
   itself, and the exemplar was always meant to be built FROM this track's output. It is now
   buildable: eight components, ten languages, one gallery that already composes them.

**Not recommended next: the oracle sweep.** It is real work — the pass-53 lesson (an oracle that
moves with the code) has been designed in from pass 54 onward but the older component blocks predate
it — but nothing is known to be wrong there, and this pass's own evidence argues the opposite way:
the sharpest instrument defects found today were dead runs and a missing SURFACE law, neither of
which a sweep of existing oracles would have found.

---

## FIFTY-FOURTH PASS — the COMPONENT CONTRACT, increment 7 (scroll bar · THE VALUE THAT IS A WINDOW)

**What this pass is.** The seventh increment, and the first one whose question is about the
MECHANISM rather than the anatomy. Every component before this one has a value `value_pos` can
answer: one number in, one cell out, six components sharing the seat. A scroll bar's value is TWO
numbers — where the view is AND how big it is — and no amount of parts can make that one number.

### THE TWO-NUMBER RULING — the registry gains a FACT and the mechanism gains a SEAT, and both were needed

The brief offered them as alternatives. They are not: they answer different halves, and taking only
one leaves the other half hand-written at a seat.

**`COMPONENT_PARTS["scrollbar"] == ("main", "indicator")` — THE BAR'S EXACT TUPLE, and declaring no
new part is the finding.** The caret was a new part because a STATE cannot pick out one cell; a
thumb is not a new part because a scroll bar has no cell a bar does not have. It is a track and a
run on it. So the registry cannot tell them apart on their parts — and it has met that twice before
(slider/switch, checkbox/radio) and been right both times.

**What differs is the VALUE, and it differs in ARITY.** A bar's extent is anchored at cell 0: the
run measures `val` and always starts at the origin. A scroll bar's run is anchored nowhere — it
floats to where the view is, and its LENGTH is the second number made visible. **The parts registry
cannot see arity, because parts are SLOTS.** So the fact is DECLARED:

```python
VIEWED: tuple[str, ...] = ("scrollbar",)
```

**And that is not a third declared fact — it is the second member of a family that already
existed.** Pass 53 warned that a third fact would be a smell, and the warning is answered rather
than ignored: this registry now carries **two families, not three lists**. `GRIPS` is a fact about
PARTS (which slot the hand moves). `CHECKABLE` and `VIEWED` are facts about the VALUE that parts
cannot show — CHECKABLE says its RANGE is boolean, VIEWED says its ARITY is two. Same seat, same
reason, same shape. **No new grip was added and `GRIPS` is byte-identical to what the text field
left it**, which is the concrete form of that answer.

**The falsifiable consequence:** take the scroll bar out of `VIEWED` and it draws as a BAR — an
anchored extent whose length is its position — and grows a one-number readout beside a two-number
value. The suite drives exactly that (M6) and it goes **137 red**.

**THE SECOND SEAT: `view_pos(start, size, total, cells) -> (pos, span)`**, beside `value_pos` and not
instead of it. Widening `value_pos`'s return would have made all six of its callers carry a span they
have no use for. And it **invents no arithmetic**: it computes the SPAN and delegates the POSITION
straight to `value_pos` on the shortened track the thumb leaves behind, so there is still exactly one
place in this file that turns a number into a cell index (pass 43's "one measure", surviving a second
seat). The track the position runs over is `cells - span + 1`, not `cells` — **the off-by-one that
leaves a scroll bar unable to say "you are at the bottom"**, and it is asserted as exact CELLS at
three track widths and per language, not as a ratio.

**THE OTHER HALF OF THE SEAT WAS ALREADY IN THE BUILDING, WITH NO NAME.** Pass 53 computed a window
start inline in `Kit.textfield` — five lines nothing declared, that no other component could reach,
and that only the composer knew. That is the fork defect this repo has cured three times (the hero's
metrics, the head's width, the switch's frames): **a measure with one call site is not a measure yet,
it is a local variable.** It is now `view_start(total, size, focus, start)` and the field routes
through it. The arithmetic is unchanged, deliberately — **the pass-53 window laws pass untouched**,
which is the point of their independent oracle.

### THE READOUT RULING — no grip, and every consequence is DERIVED

**`actuator("scrollbar") is None`, so `component_states("scrollbar") == (default, disabled)` — the
BAR's axis byte for byte, with zero edits at any seat.** The argument is about this app and not
about scroll bars in general: **Textual's own scrollbars are draggable, and ours is not, because in
THIS keyboard TUI nothing is ever scrolled by grabbing.** The keys act on the CONTAINER; the bar
reports where the container got to. A `knob` added to make it feel operable would be exactly the dead
metadata this file has refused twice. The suite drives that too (M7, **29 red**).

**Two consequences follow the ruling rather than a preference.** (1) No control states — FOCUSED
would advertise an affordance the app does not have, which is the defect the bar's missing knob was
the first cure for. (2) **NO READOUT, and it is the arity again at a second seat**: `value_label`
prints ONE number and a window is two, so printing one would name the position and hide the size.
This is the first component whose value IS its own readout.

**`has_interior` is TRUE and there is still no EDITED**, which is the first time those two terms have
come apart. The interior term alone would have granted one; the ACTUATOR gate is what refuses.

### THE LIVE SEAT — Textual owns it, and ours DOCUMENTS rather than replaces

Read for, and reported plainly: the surfaces that really scroll here are `VerticalScroll` containers
(`#gallery-box`, `#cfg-scroll`) that draw and drag **Textual's own scrollbar chrome**. Replacing that
means overriding a framework widget, and the only channel a language could honestly take from it in
TCSS is **colour** — the one channel this contract forbids a state to ride alone. **So the scroll bar
is GALLERY-ONLY, like the text field, and for a different stated reason: the field has no live seat,
this one has a live seat that belongs to somebody else.** Priced, not faked.

**No axis fact, and that is deliberate.** The component composes a LIST OF CELLS; which axis they are
stacked on is the caller's, exactly as it is for `bar`. It is drawn along a row in the gallery. A
language wanting a different glyph vertically would need an axis fact in the registry, and none has
asked — item #29 below, priced.

### Per-language mechanism — the SHAFT is not the SCALE

Scoped `scrollbar.main` / `scrollbar.indicator` in all ten, two states each (a readout has two, and a
law forbids the table declaring a FOCUSED shaft it could never be asked for). The reason the pair is
scoped rather than inherited: **a slider's track is a SCALE (every cell is a value the knob could
take) and a scroll bar's is a SHAFT (every cell is somewhere the view could be)** — and they stand
side by side in the same gallery, so a language drawing them identically would be claiming the two
mean the same thing.

| language | shaft | thumb | the mechanism |
|---|---|---|---|
| nord | `░` | `█` | inherits the environment — Textual's own scrollbar vocabulary |
| naught | `·` | `●` | **the dot column** (the skill's own row): the lattice at its faintest pitch, the view at full pixel size |
| corgi | `░░` | `██` | a segment bank, doubled: GHOST segment vs DRIVEN, never hue |
| instrument | `⠄` | `⣿` | the register as a traverse — baseline rail vs cell driven full |
| swiss | `┄` | `▬` | weight, its only ornament: lightest rule vs heaviest |
| industrial | `-` | `#` | ASCII and coded, inside its bracketed chrome (`[--###----]`) |
| darkside | `▁` | `█` | fill inversion, its declared idiom; nothing boxed |
| ledger | `┊` | `▬` | the ruled column — leaves you are not on are rules, the leaf you are on is posted |
| solari | `▔` | `▄` | the rank of cards: seams ahead, flaps TURNED across the view |
| blueprint | `·` | `━` | **nothing is filled** (its law survives the new component) — leader vs extension line at drawing weight |

### Verification — 7384 -> **7752** (+368)

Scroll-bar laws: the registry and the arity collision · the readout ruling and its two derived
consequences · `view_pos` PROPERTY laws at three track widths (span rises with the view size, floor
1, cap = whole track, **ends exact as cells**, length constant while travelling, position monotone,
thumb wholly on track over a swept range, out-of-range clamps) · `view_start` laws (leaves a settled
window alone, pulls up to exactly the focus, down by exactly the shortfall, focus always inside,
idempotent, content that fits is not scrollable) · per language: scoped glyphs, two-channel in every
state, tiling, contiguity, **ends reachable asserted with no arithmetic in the oracle at all**, the
thumb moves, the length does not move with it, the length IS the view size, a full window fills the
shaft, three positions distinct in greyscale, the DECLARED COMPOSITION composed from the glyph table,
DISABLED shape-marked, nothing printed beside it, **no accent anywhere and every tone byte-identical
to the bar's**, two-parser · cross-language distinctness · four kit-subclass controls · the gallery
seat.

**ORACLE INDEPENDENCE, designed in rather than discovered (pass 53's third defect).** The seat is
pinned by PROPERTY laws that recompute nothing; the render laws then compose from the DECLARED glyph
table plus that pinned seat; and the ends are additionally asserted as first-cell/last-cell with no
arithmetic, so a mutation inside the seat cannot move the oracle and the render together. The
mutation table is the evidence: M2 and M3 both touch only `view_pos` and go 38 and 24 red.

**Mutation table: 12 real rows, ALL CAUGHT; 1 driver control, DEAD RUN as designed.** Vacuity-proved
first — all 13 CHANGE an observable signature (`prototypes/out/_p54_prove.py`, **budgeted as a file
of this increment**, which is the thing pass 53 had to confess after the fact).

| # | mutation | red |
|---|---|---|
| M1 | the thumb's LENGTH ignores the view size | 23 |
| M2 | the thumb's POSITION ignores the start | 38 |
| M3 | the classic OFF-BY-ONE (`cells - span` seats) | 24 |
| M4 | the run is ANCHORED at the origin again | 71 |
| M5 | the span FLOOR removed (thumb rounds to zero) | 5 |
| M6 | `VIEWED` emptied — the registry fact | 137 |
| M7 | the scroll bar is given a KNOB | 29 |
| M8 | the one-number READOUT comes back | 72 |
| M9 | the text field stops ROUTING through the seat | 2 |
| M10 | `view_start` ignores the focus | 43 |
| M11 | nord's thumb drawn as its shaft | 3 |
| M12 | the gallery block hand-lists its states | 10 |
| M13 | *[driver control]* `Kit.scrollbar` raises | DEAD RUN detected |

**M9 IS THE ROW THIS PASS EXISTS TO MAKE HONEST, and its 2 red is the design, not a weakness.**
Restoring the inline window arithmetic is behaviourally IDENTICAL by construction, so no render law
can see it. It is caught by exactly the two laws that can: a source law (`view_start(` is called and
no window arithmetic remains) and a **behavioural call recorder** that asserts the seat is reached
with the field's own numbers — because a source law can be satisfied by a call that is never made.
The vacuity prover's signature was extended to record the seat being REACHED for the same reason.

**ROUND TWO, and it is reported rather than buried.** M11 scored **1 red** in round one — a thumb
drawn as its own shaft was seen by exactly one law, because every other per-language law reads PART
TAGS, which survive a language drawing both parts identically. Two greyscale laws were added (three
positions pairwise distinct, big window differs from small) and it went to 3, M1 from 13 to 23. **3
red is still thin and is said so**: a one-language glyph collision has few laws that can see it, and
the honest widening would be a cross-component greyscale law, not more scroll-bar laws.

**Suites at closure — THREE back-to-back full runs, identical every time.**

| suite | checks | fifty-third | verdict |
|---|---|---|---|
| `prototypes/verify_language.py` | **7752** | 7384 | ALL PASSED (x3) |
| `prototypes/verify_aperture.py` | 151 | 151 | ALL PASSED (x3) |
| `prototypes/verify_widget.py` | 24 | 24 | ALL PASSED (x3) |
| `prototypes/verify_board.py` | 22 | 22 | ALL PASSED (x3) |
| `prototypes/verify_variants.py` | 12 | 12 | ALL CHECKS PASSED (x3) |
| `python -m pytest tests -q` | 137 | 137 | **136 passed, 1 FAILED (x3)** |

**THE PYTEST RED, said first among the reds because it is one.**
`tests/test_app.py::test_win_clipboard_roundtrip` fails in all three runs — the Windows clipboard is
unavailable in this environment. Item #22. **Five passes running now.** Not a regression from this
pass: neither `taskboard/app.py` nor `tests/` was touched.

**Flake watch.** Nothing fired — not in the fifteen suite runs of the three sets, not in the sixteen
mutation runs, not in the thirteen vacuity-prover runs. Settle headroom stayed at **worst 4 of 40**,
unchanged for five passes.

**Next: the STEPPER closes the family**, and its axis is **wrap vs clamp** — the first component
whose question is what happens at the END of a range rather than what a range IS. It is also the
first place `value_at` gets a real caller. Read `group_states` before starting: a stepper through a
NAMED set and a radio over the same set are the same choice with two different mechanisms, and
whether that is one registry entry or two is the increment's first question.

---

## FIFTY-THIRD PASS — the COMPONENT CONTRACT, increment 6 (text field · THE CARET BECOMES A PART)

**What this pass is.** The sixth increment, and the first one that grows the REGISTRY rather than
only reading it. The button ruled that TEXT is not a part; a text field asks the opposite question,
because a caret is not text. Three components' worth of laws hang off the answer, so it was argued
before it was drawn.

### THE CARET VERDICT — it IS a part, and the decisive reason is structural

**`COMPONENT_PARTS["textfield"] == ("main", "caret")`.** Three arguments, in ascending order of
force:

* **It passes the bar the LABEL failed, on all three tests.** A part is a slot the LANGUAGE draws,
  from its own glyph table, in every state it applies to. The caret's glyph is the language's
  (naught's lit lattice dot `◉`, instrument's braille tick `⡇`, blueprint's datum `╪`), never the
  caller's; where it stands is state; and nothing about it comes from outside. The label failed all
  three and that is why it is content.
* **A STATE CANNOT PICK OUT ONE CELL — this is the argument that settles it.** In this renderer a
  state is a property of the WHOLE component: `part_glyph(part, state)` answers once. So "main, but
  in EDITED" does not mean "one cell of main becomes a caret", it means the ENTIRE field becomes
  carets. The only thing that distinguishes one cell from its neighbours here is its PART TAG. A
  mark at one of N seats is therefore a part or it is nothing, and this is a fact about the
  composer, not a preference about anatomy.
* **AND IT IS NOT THE KNOB, which was the alternative that cost no new part.** `("main", "knob")` is
  the CHECKBOX's tuple. Letting a field wear it would make one tuple mean two mechanisms — a mark
  that is either THERE or not, and a mark that is at one of `w` PLACES. The slider and the switch
  legitimately share a tuple because they share an anatomy; this would have been two anatomies
  hiding under one. The suite drives that exact mutation (M8) and it goes **412 red**.

**The falsifiable consequence, in the button's own shape.** Because the caret is a part it must be
TAGGED in the render at the index it was handed, and because the value is content it must come back
out byte for byte. Those two only hold together if **the caret takes a COLUMN OF ITS OWN** — a block
caret sitting ON a character hides that character, and the only way to keep it readable underneath
is reverse video, which is colour, which this contract's states may never ride alone. So the
mechanism was chosen by the law rather than by taste, and the law is asked with the caret's own cell
lifted out of the render.

**The registry gained exactly one more fact and it is a tuple, not a seat.** `GRIPS = ("knob",
"caret")` — the marks a user MOVES. A knob rides a track and reports a MAGNITUDE; a caret rides
characters and reports an INDEX; they are different parts and the same thing to the hand and to the
accent rule. Declared, the way `CHECKABLE` is declared, rather than hidden inside `actuator` as an
`or "caret" in parts` — which is how a contract starts accumulating hand lists at its seats instead
of in its registry. The suite reads that off the source.

**`main` IS THE GROUND, and its glyph carries the walls with it.** One ODD string read at three
seats — the wall that opens, the RUNE the paper is made of, the wall that closes (`field_form`). The
button states the same "the walls are halves" rule as an EVEN length; this component has an interior
to put between them. One part, one string, one tone, because a language does not choose its walls
and its paper separately — it chooses the ground it lays under someone else's words. **The walls are
not optional**, and that is the button's physics again: a value may fill every cell, so a field with
no cells of its own would have nowhere to say DISABLED without editing the user's text.

### THE VALUE VERDICT — `has_value("textfield")` is FALSE, and that is the ruling

Not an omission. `has_value` means "the registry can read this component's value", and a text
field's value is **CONTENT** — which is exactly what the button said about a label, read at the
value instead of at the word. Two consequences fall out and both are law: **no readout is printed
beside a field** (the value is already visible IN the control; printing it again would be a lie
about where the value lives), and **the caret arrives as its own argument** rather than riding
`val`, because a field is a value AND an insertion index and two identical strings can be under edit
at two different places.

### THE STATE VERDICT — five states, EDITED among them, and no new registry fact bought it

`component_states("textfield") == (default, focused, EDITED, active, disabled)`.

**EDITED is gated on `has_interior`, and that term is the concept the EXTENT was standing in for.**
The button's pass wrote it as `"indicator" in parts`, which was true of every component that existed
then. A field has an interior and no extent, so the term is now: *an EXTENT (`indicator`) is a run
measured from an origin, a FIELD (`caret`) is a run indexed by a mark, and both are cells a cursor
moves between.* **Both of its terms are parts already declared** — the same correction the button
made to `knob` when it meant *the part you grab*, and it cost the registry nothing.

**EDITED finally means here what it always said.** On a slider it is "the arrows now move the
value"; here it is "the keystrokes now land IN the text", and the caret is the promise of exactly
that — which is why **the caret is drawn in EDITED and in no other state**. FOCUSED is the field
selected; EDITED is the field entered. A field showing an insertion point while the keyboard is
elsewhere is lying about where the next keystroke lands, and the suite says so (M2, 20 red).

### THE INVALID VERDICT — it is NOT a state, and the skill's row is honoured rather than refused

`COMPONENTS.md` asks for "caret + placeholder + invalid state". The first two shipped. **`invalid`
did not, and the argument is that it is not a control state at all:**

* **The axis is DERIVED from parts and CHECKABLE. Nothing in a field's anatomy makes it
  validatable**, and nothing in a slider's or a radio group's does either — yet a slider's value can
  be out of range and a group can be unset. The registry has nothing to derive `invalid` from, so
  adding it means HAND-LISTING, which is the defect this contract has refused six times.
* **Every existing state is an INTERACTION state** — where the user is relative to the control.
  Invalid is what the SYSTEM thinks of the value, which is a SEVERITY, and this codebase already has
  a severity channel: `ALERT_HUE`, `Reading.severity`, the card's overdue chip, `DATAVIZ.md`'s face
  and tone rules.
* **And structurally it is a BIT, not a state.** It would have to combine with all four control
  states the way CHECKED does (`invalid+focused`, `invalid+active`). So if it is ever built it
  belongs **where CHECKABLE lives — a registry tuple of VALIDATABLE components — and it applies to
  slider, stepper and field alike, not to the field alone.** That is a named future with a named
  shape, and it is new item #26 rather than a silent omission.

### THE PLACEHOLDER VERDICT — content, separated by TONE alone, and said out loud

The placeholder is the caller's words, so it may not be bracketed or recased any more than the value
may — shape is unavailable. And the distinction must exist, because a field showing `title` that the
user typed and a field showing `title` that is merely suggesting are two different states of the
model. **So it is separated by TONE, and this is the one place in this contract where colour carries
the whole distinction.** It is flagged rather than buried, with the reason it does not break the
"colour is the SECOND channel and never the only one" law: that law governs STATES, and this is
set-versus-unset — which is `check_tone` for the FOURTH component, lit when the user put the words
there and muted when the field did.

### THE WINDOW — overflow honesty, and the one reflow only this component can make

A value longer than the field is **never shortened**: the view moves, sliding the least it can to
keep the caret inside. Four laws hold it, per language: the caret is inside the field at every index
of a long value; **the character just BEFORE the caret is always visible** (what you just typed never
falls off the edge); **every index is reachable** (move the caret to it and the character is on
screen — the honest form of "nothing is lost"); and what the window shows is a **contiguous slice**,
so nothing is reordered and no ellipsis eats bytes to buy itself a cell. The gallery block then
reflows by NARROWING THE WINDOW, which only this component can do honestly — a smaller view shows
less of the value and loses none of it, where a shorter button would be a shorter word.

**What is owed and named: there is no OVERFLOW MARK.** When the window is scrolled, nothing on
screen says so. The honest cheap answer is a wall variant for "there is more that way", and it would
multiply each language's five ground forms by four — a design increment of its own, not a rider.

### Seat verdicts — ten languages, ten fields

Every ground form is ODD and one width across all five states (the frame cannot move under the
words), the five are pairwise distinct with colour stripped, and every caret glyph is one cell, is
not a space, and differs from the paper's rune in every state.

| language | default | focused | edited (caret at 2) | disabled | the commitment |
|---|---|---|---|---|---|
| **nord** | `[task    ]` | `▐task    ▌` | `▐ta▏sk▁▁▁▌` | `╌task╌╌╌╌╌` | the terminal's own input; the state is the bracket's weight and EDITED lays a ruled line under the paper |
| **naught** | `◦task····◦` | `○task····○` | `○ta◉sk∙∙∙○` | `⋅task⋅⋅⋅⋅⋅` | a LATTICE seat: the paper IS the lattice, EDITED tightens the weave, and the caret is the one LIT dot. Zero red — the ration reached it through the actuator |
| **corgi** | `▁▁task··▁▁` | `▔▔task··▔▔` | `▔▔ta▌sk▁▔▔` | `··task····` | FIVE cells, because this language doubles: two of wall a side and the rune in the middle, words milled into the channel |
| **instrument** | `⠇task⠒⠒⠒⠸` | `⠧task⠒⠒⠒⠼` | `⠧ta⡇sk⠤⠤⠼` | `⠄task⠁⠁⠁⠄` | braille RAILS with a braille RULE between them; the field is a measured span and the words lie along it |
| **swiss** | `│task    │` | `┃task    ┃` | `┃ta▏sk···┃` | `┆task    ┆` | **the language that would renounce the walls and cannot, a second time** — a value may fill every cell, so a bare field would separate its states on colour alone. Thinnest rule that carries one, and the ONLY paper here that is blank |
| **industrial** | `▐task····▌` | `▐task____▌` | `▐ta\|sk---▌` | `(task----)` | THE PLATE with a machined face, the same `▐ ▌` it stamps on every card; the dead plate keeps the round bracket, because here round brackets mean dead |
| **darkside** | `▬task    ▬` | `▮task    ▮` | `▮ta◆sk···▮` | `╌task╌╌╌╌╌` | FILL INVERSION as a ramp, no border drawn (its law) — the ends are a weight, and the caret is its own EDITED knob |
| **ledger** | `│task····│` | `▶task····│` | `▶ta▏sk∙∙∙│` | `╌task╌╌╌╌╌` | A RULED COLUMN whose paper is the DOT LEADER it rules every gap with; the tally pointer arrives with the cursor and the entry closes on both sides |
| **solari** | `▁task····▁` | `▔task····▔` | `▔ta▮sk▁▁▁▔` | `╌task╌╌╌╌╌` | A CARD in the row, seams above and below; the press is the flap caught mid-turn, exactly as on its button |
| **blueprint** | `├task····┤` | `╞task····╡` | `╞ta╪sk╌╌╌╡` | `╎task╌╌╌╌╎` | a TITLE-BLOCK CELL between two extension lines; the caret is this language's own datum tick |

**A LANGUAGE-CHARACTER IDEA CONSIDERED AND REFUSED, with its reason.** ledger's caret was first
drawn as the GAP in its dot leader — the break in the rule where the pen rests. It is the most
in-character mark in the set and it is **wrong**, because a gap is a SPACE, and a space is the one
character the user's own value certainly contains. A mark that can be confused with content is not a
mark. That refusal is now a law asked of all ten.

### The live seat — THERE IS NONE, and it is said rather than faked

The button found a real press target on the config screen (`r`, the engine's own refresh). This
component was read for one and **there is none**. Nothing in the engine is TYPED: `Signal.label`,
`help` and `group` are written by `default_signals()` and rebuilt at every start, so a rename would
edit a string no restart keeps and no behaviour reads — **a demo wearing a seat's clothes**, which is
the one thing this track has refused at every increment. The gallery draws all five states plus the
placeholder and the window; the live surface gets a text field the day the app has text to take. The
refusal and its reason are written at the call site, not only here.

### Verification — `verify_language.py` 6654 -> **7384** (+730)

Registry laws (the two parts; `caret` is declared by no other component; it is NOT the checkbox's
tuple; no indicator but an INTERIOR; `GRIPS` as a registry fact and every grip in it actually
declared by somebody; the actuator; the five-state axis; EDITED belonging to exactly the slider and
the field; `has_value` FALSE; `has_interior` as a TABLE over all seven) · derivation controls (a new
`("main", "caret")` probe gets the five states and the caret actuator with nothing hand-listed; a
probe with BOTH an extent and a field still gets five; declaring the field probe CHECKABLE takes
EDITED away again; **TAKE THE CARET AWAY and the field collapses into a button** — four states,
`main` as its own grip, which is the caret carrying the whole difference) · source-level laws
(`has_interior`, `actuator`, `component_states`, `field_form`, `component_cells`, `part_slots`,
`part_tone` name NO component; `Kit.textfield` names only itself; the composer's THIRD anatomy forks
on `"caret" in parts`; `has_interior` is the OR of two declared parts and nothing else; no readout
is reachable; `check_tone` is reused) · and per language: its own scoped glyphs, an ODD form of one
width across five states, five distinct forms, a one-cell caret that is not a space and not any
state's rune, no chrome, `w` columns exactly at every width, the caret TAGGED at the index it was
handed in every state, no caret when none is handed in, **the caret drawn in EDITED and nowhere
else**, the caret AT THE CELL THE MODEL SAYS at every index including both ends, an out-of-range
caret CLAMPING rather than raising, the value byte-for-byte with the caret's cell lifted out, once,
with nothing after the closing wall, a long value never shortened, the four WINDOW laws, one
rendered width across every state and value and caret position, **moving the caret one place
changing at most TWO cells**, the placeholder shown / gone / toned apart / byte-for-byte, DISABLED
shape-marked, EDITED ≠ FOCUSED in shape, five states pairwise distinct in greyscale, **the caret
wearing exactly what that language gives its slider's KNOB in all five states** (the accent law, a
sixth time), the two-parser law including a value carrying a BRACKET, and **the empty field composed
exactly as its DECLARED string says, read off the glyph table rather than through the code under
test**. Plus ten-way distinctness, five in-suite controls that drive the per-language laws red, and
six gallery laws.

**Mutations — fourteen injected, every one PROVEN to change an observable signature first.** The
vacuity guard (`prototypes/out/_p53_prove.py`) applies each mutant, renders every language in every
state at three values, derives a probe component's axis, and hashes the lot; a mutant whose
signature does not move is not evidence and is not run. **It caught one on its first pass** — M11's
placeholder tone was invisible to the signature until raw markup for an empty field was added to it,
which is the prover doing its job on itself.

| mutation | round 1 | after the cures |
|---|---|---|
| M1 the caret IGNORES its index — always at the start, so the mark stops being state | 50 red | — |
| M2 the caret is drawn in EVERY live state — a promise made where the keyboard is not | 20 red | — |
| M3 the language RESTYLES the caller's VALUE — the content ruling broken where it costs a user their own text | **170 red** | — |
| M4 the field TRUNCATES instead of windowing — the rest of the value is simply gone | 40 red | — |
| M5 the WINDOW never moves — the caret walks off the edge of a long value | 40 red | — |
| M6 EDITED is HAND-LISTED for this component — the derivation reverts to the extent | 6 red | — |
| M7 the caret is dropped from GRIPS — the accent leaves the mark under the finger | 45 red | — |
| M8 the caret is declared a KNOB — the shortcut that makes one tuple mean two anatomies | **DEAD RUN** | **412 red** |
| M9 the field collapses to ONE slot — `w` read as a budget rather than as a window | **DEAD RUN** | **400 red** |
| M10 the paper's RUNE is read off the WALL instead of the middle | **2 red — the oracle moved with the code** | **46 red** |
| M11 the placeholder is toned exactly like a typed value — its one channel, spent | 10 red | — |
| M12 the placeholder SURVIVES a value being typed — the field shows two answers | 10 red | — |
| M13 the gallery block HAND-LISTS the states — EDITED silently missing | 20 red | — |
| M14 **[control on the driver]** `Kit.textfield` raises on every call | **DEAD RUN — 4551 pass, 0 red, and the driver said so** | as designed |

**THE THREE INSTRUMENT DEFECTS, and they are the valuable half again.**

1. **`index` where `find` was meant — AGAIN.** Pass 52 cured this exact shape on the button; it came
   straight back on a new component, because `r.index(caret)` raises precisely when the caret is
   missing, which is the mutation the law exists to catch. Two DEAD RUNs (M8, M9) reporting nothing.
   `find` returns `-1` and goes red like a law.
2. **A per-language dict keyed by the DERIVED axis — the MIRROR of pass 52's.** Pass 52's fired when
   a mutation GREW the axis; this one fired when M8 SHRANK it (a field declared with a knob has no
   EDITED, so `drawn[EDITED]` threw `KeyError` and took the run down). Cured by asking `in` before
   `[]`, so a derivation defect goes red **at the derivation laws** instead of on its way past.
3. **THE ORACLE MOVED WITH THE CODE — new, and the sharpest of the three.** Every law that touched
   the field's paper asked `field_form`, which is the function under test. M10 makes the paper's
   rune come out of the WALL instead of the middle — a defect that visibly wrecks all ten languages
   — and it scored **2 red**, because nine tenths of the laws were reading the mutated form and
   agreeing with it. Cured with a law that re-derives the CONVENTION (odd string, middle is the
   paper) from the declared glyph string and composes the whole expected render itself. **46 red
   afterwards, and this is a probe-discipline lesson that applies well beyond this component.**

**And one law was WRONG on its first run, which is worth recording because the fix is the argument.**
The content law was first written as `value in render` and went **20 red against correct code** — the
caret legitimately sits BETWEEN two of the value's characters. The law had to be restated as *the
value comes back byte for byte once the caret's own cell is lifted out*, and that restatement IS the
mechanism argument: the caret takes a column of its own precisely so that no character is hidden
under it.

### LOOK — the gallery's text-field block, verbatim from `g`, colour stripped

Four contrasting languages. The value is the same four bytes down every column; what changes is the
ground, the paper and the mark.

```
industrial
textfield  task·caret 2
           ▐task······▌   default
           ▐task______▌   focused
           ▐ta|sk-----▌   edited
           ▐task######▌   active
           (task------)   disabled
           ▐title·····▌   placeholder
           ▐t windows|▌   window

ledger
textfield  task·caret 2
           │task······│   default
           ▶task······│   focused
           ▶ta▏sk∙∙∙∙∙│   edited
           ▶task······◀   active
           ╌task╌╌╌╌╌╌╌   disabled
           │title·····│   placeholder
           ▶t windows▏│   window

instrument
textfield  task·caret 2
           ⠇task⠒⠒⠒⠒⠒⠒⠸   default
           ⠧task⠒⠒⠒⠒⠒⠒⠼   focused
           ⠧ta⡇sk⠤⠤⠤⠤⠤⠼   edited
           ⣇task⠒⠒⠒⠒⠒⠒⣸   active
           ⠄task⠁⠁⠁⠁⠁⠁⠄   disabled
           ⠇title⠒⠒⠒⠒⠒⠸   placeholder
           ⠧t windows⡇⠼   window

swiss
textfield  task·caret 2
           │task      │   default
           ┃task      ┃   focused
           ┃ta▏sk·····┃   edited
           █task      █   active
           ┆task      ┆   disabled
           │title     │   placeholder
           ┃t windows▏┃   window
```

Three things to read off it. **The `edited` row is the only one with a mark inside**, and the mark
has its OWN column — `ta`, caret, `sk` — which is why `task` still comes back whole. **The
`placeholder` row prints `title` where the value would be**, identical in shape to a typed `title`
and different only in tone, which is the one colour-only distinction in this contract and is
declared as such. **The `window` row holds a 25-character value in a 10-cell field**: the view has
slid to `t windows` with the caret at the end, and every character of that value is reachable by
moving the caret — the field never shortened it.

### Open, and honest

* **No LIVE SEAT, and that is a refusal rather than an omission** — see above. Nothing in the engine
  is typed.
* **No OVERFLOW MARK.** A scrolled window says nothing about the text behind it. Named above with
  its cost (four wall variants per state per language).
* **No MOTION.** The caret does not BLINK. A blink is a tempo question like the button's press and
  the radio's mark-moving-between-siblings, and all three are still owed to the MOTION axis.
* **`invalid` is not built** — argued above, and filed as item #26 with the shape it would take.
* The **`escape()` sweep** (item #25) is still owed and is now more attractive: this pass added a
  law that a value carrying a BRACKET survives both parsers at the field's seat, which is the same
  claim the sweep would make everywhere else.
* **blueprint's `tabs` row is still 125 columns wide in a 52-column gallery box**, untouched for the
  third pass running, still the reason there is no whole-gallery width law.
* The **gauge** still carries its own copy of the value arithmetic (pass 48's note, unchanged).

### Next

1. **`scroll bar` — the first component whose VALUE IS A WINDOW.** It is the right next one for a
   specific reason rather than by order: this pass just built a window **in the composer, with no
   expression in the registry** — `Kit.textfield` computes a start offset that nothing declares and
   no other component can reuse. A scroll bar is that window made visible, and its axis is
   **TWO NUMBERS IN ONE CONTROL** (where the view is AND how big it is), which is the first thing
   `value_pos` — one value, one position, shared by six components — cannot answer. Either it grows
   a second seat honestly or the registry gains a `view` fact; both are findings.
2. Then **stepper**, whose axis is **WRAP vs CLAMP** — already named twice at the radio's live seat,
   where the group clamps and says so.
3. **Four instrument items owed:** `test_win_clipboard_roundtrip` needs a skipif or a mock (#22,
   firing for four passes), item #25's escape sweep, blueprint's `tabs` row, and the probe-discipline
   sweep this pass's third defect suggests — **any law whose oracle calls the function it is
   testing** is the same hole, and `field_form` will not be the only one.

---

## FIFTY-SECOND PASS — the COMPONENT CONTRACT, increment 5 (button · the control with NO VALUE)

**What this pass is.** The fifth increment, and the first component that answers from nothing. A
slider answers from its number, a checkable from its bit, a radio item from its sibling's. A button
has none of those — it has only an ACTUATION — so it was chosen for two questions the fifty-first
pass named: **(a)** does the state axis still fall out of the registry when there is nothing to be
EDITED or CHECKED, and **(b)** what are a button's PARTS, given that its label is INSIDE it where
every other component's word stands beside it. (b) is the real increment: the first time this
registry has had to decide whether text is a part.

### THE PARTS VERDICT — text is NOT a part, and the argument is what a part IS

**`COMPONENT_PARTS["button"] == ("main",)`. The label is CONTENT flowing over the main part's
ground; the main part is the WALLS the language draws and the field they enclose.** LVGL rules the
same way (a button has `main`; its label is a child object), but the reason to follow it here is
local and falsifiable rather than deferential:

* **A part is a slot the LANGUAGE draws, from its own glyph table, in every state.** The label's
  text comes from the CALLER. A language handed a word it did not choose can only "draw" it by
  mangling it — recasing, letterspacing, bracketing — and every one of those either destroys the
  caller's word or moves the field under it. A part every language would render identically is not
  a part, it is a payload.
* **The two laws only both hold if the label is content.** Because the state cannot ride the word,
  it must ride the cells the language owns: the four states are required to differ in the WALLS'
  SHAPE, and the word is required to come back out of the render byte for byte. Had the label been
  a part, those two laws would contradict each other — which is exactly why they were written as
  the test of this decision rather than as decoration on it.
* **The consequence is that a button spends at least one cell per side on itself.** A control whose
  label filled it would have nowhere to say "pressed" without editing the word. That is a physics
  constraint, not a style, and it is what makes `▓▓Save▓▓` (the walls eating the air) the honest
  terminal analogue of a press flash.

**The alternative was considered and refused for a named reason.** Declaring `("main", "knob")` —
the "keycap" inside the plate — would have kept the old one-line derivation and bought a lie: a
part invented to satisfy a derivation is dead metadata, the defect this file has cured twice
before ("a hardcoded mechanism makes its token dead metadata again"). The suite drives that exact
mutation (M8) and it goes **34 red**.

**And it is consistent with the fifty-first pass's label split, because both are now DERIVED from
one fact.** `has_value(name)` is true iff the component has an EXTENT (a number to measure) or is
CHECKABLE (a bit). A component that holds a value has a READOUT standing beside it — `value_label`,
`check_label`, the option's word. A component that holds none has nothing to report, and its only
text is the caller's name for the action, which stands inside. Two rules became one fact read at
two values; nothing is hand-listed, and `has_value` is asked of all six components in the suite.

### THE STATE VERDICT — four states, derived, but ONE LAW HAD TO MOVE

**`component_states("button") == (default, focused, active, disabled)`, and it is derived. The
skill's prediction that it would "fall out of `"knob" in parts` with no new registry fact" is HALF
right and the half that is wrong is worth stating plainly**: no new registry fact was added — no new
table, no hand list, nothing a language declares — but the derivation's one-line law had to be
refined, because with `("main",)` and no knob the old expression gave a button NO control states,
which is not a subtle error. A button IS a control.

**The refinement is one concept, `actuator(name)` — the part a user GRABS — and it replaced the
word `knob` at three seats that were all standing in for it:**

| component | actuator | why |
|---|---|---|
| slider · switch · checkbox · radio | `knob` | a grip is a grip wherever one is declared |
| **bar** | **None** | it holds a value and has no knob: the indicator reports a number nobody sets. That IS the readout law, unchanged |
| **button** | **`main`** | it holds no value and has no knob — nothing to report and nothing to grip separately, so the whole control is the grip: its ground |

The three seats: the **state derivation** (`if actuator(name)` gates the control block), the **tone
rule** (`part_tone` spends the accent on the actuator under interaction, not on a knob the button
does not have), and **four languages' overrides of that rule** (naught's red ration, darkside's
KMBlue-on-interaction, solari's amber, corgi's screen hue). Every other component's tones are
byte-identical afterwards, and the shipped accent laws passing unchanged is the proof.

**A second expression moved with it, and it corrects an over-attribution.** EDITED used to read
"unless CHECKABLE"; it now reads "an EXTENT that is not a boolean". The checkbox's missing EDITED
was credited to CHECKABLE in the fiftieth pass, and that was true of every component that existed
then — the button shows the real gate is the interior, not the bit. A knobbed component with no
extent takes no EDITED either, and the suite's probe says so.

### Seat verdicts — ten languages, ten buttons

Every wall string is EVEN and one width across all four states (the field cannot move under the
word), and the four are pairwise distinct with colour stripped.

| language | default | focused | active (the press) | disabled | the commitment |
|---|---|---|---|---|---|
| **nord** | `[ Save ]` | `▐ Save ▌` | `▓▓Save▓▓` | `╌ Save ╌` | the terminal's own button, inherited like everything else; the press EATS THE AIR, the closest a cell comes to inversion |
| **naught** | `◦ Save ◦` | `○ Save ○` | `●●Save●●` | `⋅ Save ⋅` | a LATTICE seat: unlit dots hold the word and the press lights all four. **Zero red** — the ration reached it through the actuator |
| **corgi** | `▁▁Save▁▁` | `▔▔Save▔▔` | `▄▄Save▄▄` | `··Save··` | an ENGRAVED KEY in this language's doubled cells; the word sits in the milled channel and the shoulders swell under the finger |
| **instrument** | `⠇ Save ⠸` | `⠧ Save ⠼` | `⣇⣀Save⣀⣸` | `⠄ Save ⠄` | braille RAILS, clinical register; the press BOTTOMS OUT along the lower dots — a travel shown without moving the label |
| **swiss** | `│ Save │` | `┃ Save ┃` | `█ Save █` | `┆ Save ┆` | **the one language that would renounce the walls and cannot**: a bare word is the honest swiss button, but the label is the caller's and may not be restyled, so with the walls gone the four states would separate on COLOUR ALONE. It takes the thinnest mark that carries a state |
| **industrial** | `▐ Save ▌` | `▐_Save_▌` | `▐#Save#▌` | `(-Save-)` | **THE PLATE**, which this language already stamps on every card (`▐ nn ▌`) — the button is that plate with a word instead of a number; the disabled plate keeps the round bracket, because here round brackets mean dead |
| **darkside** | `▬ Save ▬` | `▮ Save ▮` | `█ Save █` | `╌ Save ╌` | FILL INVERSION as a ramp, bar → block; no border is drawn (its law) — the shoulders are a weight, and the accent it spends is spent on interaction only |
| **ledger** | `│ Save │` | `▶ Save │` | `▶ Save ◀` | `╌ Save ╌` | AN ENTRY IN THE LEDGER: the tally pointer arrives with the cursor, and the press CLOSES the entry on both sides — a line posted |
| **solari** | `▁ Save ▁` | `▔ Save ▔` | `▂ Save ▂` | `╌ Save ╌` | a CARD in the row, seams top and bottom; the press is the flap caught mid-turn |
| **blueprint** | `├ Save ┤` | `╞ Save ╡` | `┣ Save ┫` | `╎ Save ╎` | a TITLE-BLOCK CELL between two extension lines — nothing is boxed here, and two verticals are a dimension, not a box |

### The live seats

* **Config screen (`c`): `r` is a REAL press target and it was already reaching this screen.** The
  key is the app's own refresh; binding it on the screen gives the press somewhere to be SEEN, and
  the action it runs is the same `Engine.run_all` the aperture runs. Nothing was invented for a
  demo. The suite presses the key and reads `Signal.runs` — **exactly the enabled signals recompute,
  and the one switched off earlier in the same drive stays untouched.**
* **Its DISABLED state is the engine's.** With every signal off there is nothing to recompute, so
  the button is dead — and the action refuses on the same condition the render reads.
* **What this seat honestly does NOT have is FOCUSED, and it is said rather than faked.** This
  screen's cursor ring is the signal list; putting a button in it would mean inventing a row for the
  cursor to land on. DEFAULT, ACTIVE and DISABLED are live; the gallery is where FOCUSED is drawn —
  the same split the radio's uncommitted cursor was given one pass ago.
* **Gallery (`g`):** a `button` block of five rows, one per control state, each drawing the SAME
  state twice with a short label and a long one. The pair is the point: the field grows with the
  word while the walls hold exactly still, which is "the label is content on the language's ground"
  made visible. It measures itself like the other two blocks and stacks to nine rows at 20 columns.

### Verification — `verify_language.py` 6062 -> **6654** (+592)

Registry laws (one part, no indicator, no knob, not checkable, the four-state axis, `has_value` and
`actuator` as TABLES over all six components, EDITED-iff-extent over all six) · derivation controls
(a new `("main",)` component gets the button's four states with nothing hand-listed; a knobbed
component with no extent gets the same four; declaring it CHECKABLE gives it the eight-state
product; **giving the button an extent turns it into a readout**) · source-level laws (`has_value`,
`actuator`, `component_states`, `part_tone` name no component; the gates are read off the code;
`Kit.button` reaches neither `value_label` nor `check_label` and does reuse `check_tone`) · and per
language: its own scoped glyph, one slot at every width, no chrome, EVEN walls of one width, four
distinct shapes, **press ≠ focus in shape**, disabled shape-marked, walls ≠ its own checkbox's box,
one part in every state, **a value handed in is ignored**, the word VERBATIM and once, the word
never escaping the walls, no readout printed, one rendered width across states, the field growing by
exactly the word, `w` as a minimum that never truncates, the ground wearing exactly what that
language gives its slider's KNOB (the accent law, a fifth time), and the two-parser law. Plus ten-way
distinctness, four in-suite controls that drive the per-language laws red, and four gallery laws.

**THE INSTRUMENT DEFECTS THIS PASS FOUND — three of them, and they are the valuable half again.**

1. **The oracle was the wrong parser** (see the closing block): `[[/]█|]` had been on the config
   screen for four passes. Cured, and two laws now hold it.
2. **Two laws RAISED instead of failing.** `r.index(label)` throws when the label is mangled — which
   is precisely the mutation it exists to catch — and a per-language dict keyed by the DERIVED axis
   threw `KeyError` when a mutation grew the axis. Both turned a red into a **DEAD RUN**, and a
   raised law reports nothing. Cured: `find` instead of `index`, and the per-language laws are keyed
   by the four states a language DECLARES, so a derivation defect goes red at the derivation laws
   instead of taking the loop down with it.
3. **A timing race in my own probe.** The press flash lasts the language's tempo — 60 ms for
   industrial — and reading the screen "just after" it is a coin toss, not a law. It passed twice
   and failed once. The probe now PINS the token for the duration of the press and restores it.

**Mutations — fifteen injected, and the table is read the way pass 51 learned to read it.**

| mutation | result |
|---|---|
| M1 the language RESTYLES the caller's word (the label treated as a part it may draw) | **103 red** |
| M2 the field TRUNCATES to `w` — a button shortening the word that says what it does | **103 red** |
| M3 the walls are ODD — the halves are no longer halves | 2 red |
| M4 the PRESS looks exactly like FOCUS in one language | 2 red |
| M5 the actuator refinement REVERTED — the axis gates on `knob in parts` again | **46 red** |
| M6 the TONE seat keeps the old word — a focused button wears nothing | 22 red |
| M7 EDITED gated on CHECKABLE again — the button grows a state it has no interior for | 24 red |
| M8 the button declares a decorative KNOB (the dead-metadata shortcut) | **34 red** |
| M9 the composer lets a caller hand a button a VALUE | 11 red |
| M10 `mark` reverts to rich's escape — the `[[/]` leak comes back | 5 red |
| M11 the live button ignores the engine — it never reports dead | 1 red |
| M12 a DEAD button still fires (the action guard alone) | **SURVIVED at first — see below**; 1 red after the cure |
| M12b [corrected] BOTH guards removed — it runs AND flashes | **2 red** (the seat law and the render law) |
| M13 the press never RELEASES — a flash that outlives the press | 1 red |
| M14 **[control on the driver]** `Kit.button` raises on every call | **DEAD RUN — 4087 pass, 0 red, and the driver said so** |

Round one also reported **three DEAD RUNs that were the suite's fault, not the mutants'** (M1, M2,
M7): `index` where `find` was meant, and a dict keyed by the derived axis. Both cured, and the same
three mutants now report 103, 103 and 24 red. That is the difference between a law and a crash.

**M12 IS THIS PASS'S VACUOUS MUTANT, and the diagnosis matters more than the row.** It reported
SURVIVED against the original laws, and it was not a hole: with every signal off, `run_all`
recomputes nothing whether it is called or not, and the render's own `and live` swallows the flash.
**Two guards, one observable** — the mutant changed the code and not one thing a user could see.
The cure is both halves: a law that counts the call at the ENGINE'S DOOR (the guard's intent is that
a dead control does not RUN, which is a seat-level claim and is labelled as one), and **M12b**, the
corrected mutant that removes BOTH guards — the only version of this defect a user could ever meet.
M12b then exposed the **third** instrument defect above: the flash law read the screen after the
press without pinning the tempo, so it caught nothing (1 red, not 2). With the clock pinned it goes
**2 red** and the second one is the user-visible half.

### LOOK — the gallery's button block, verbatim from `g`, colour stripped

Two labels per row, one short and one long: **the field grows with the word and the walls do not
move.** Four rows, one control state each.

```
industrial
  button     ok·Refresh  label INSIDE
             ▐ ok ▌  ▐ Refresh ▌   default
             ▐_ok_▌  ▐_Refresh_▌   focused
             ▐#ok#▌  ▐#Refresh#▌   active
             (-ok-)  (-Refresh-)   disabled

naught
  button     ok·Refresh  label INSIDE
             ◦ ok ◦  ◦ Refresh ◦   default
             ○ ok ○  ○ Refresh ○   focused
             ●●ok●●  ●●Refresh●●   active
             ⋅ ok ⋅  ⋅ Refresh ⋅   disabled

instrument
  button     ok·Refresh  label INSIDE
             ⠇ ok ⠸  ⠇ Refresh ⠸   default
             ⠧ ok ⠼  ⠧ Refresh ⠼   focused
             ⣇⣀ok⣀⣸  ⣇⣀Refresh⣀⣸   active
             ⠄ ok ⠄  ⠄ Refresh ⠄   disabled
```

Note the `active` row in all three: the walls **eat the air** (industrial's `#` seats the plate,
naught lights the lattice, instrument's rails close along the bottom). That is a shape event on the
two cells that touch the label — and the label itself is byte-identical down every column, which is
the decision this component was chosen to test.

**And the LIVE seat, verbatim from `c` at 118 columns** — the same button, dead and alive:

```
nord         [ Refresh ]     recompute every signal now
   pressed:  ▓▓Refresh▓▓     (runs: [2,2,2,2,1,1] -> [2,3,3,3,2,2] — the signal
                              switched off earlier is the one that did not move)
   dead:     ╌ Refresh ╌     nothing is enabled — nothing to recompute

industrial   ▐ Refresh ▌ / ▐#Refresh#▌ / (-Refresh-)
ledger       │ Refresh │ / ▶ Refresh ◀ / ╌ Refresh ╌
```

### Open, and honest

* **`RUN.md` is now two behaviours short** — the config screen's `left`/`right` (owed since the
  fifty-first) and its `r`. `r` is already documented as an app key and the binding's description is
  unchanged, so no legend law is broken; the file that tells a human what the keys do is just behind.
* **The button has no MOTION.** ACTIVE is a render state held for `tempo`, with no intermediate
  frames. `flip_frames` is the switch's (a knob crossing a track); a press is a different tempo
  question — the walls closing and reopening — and this pass does not answer it. The radio's
  mark-moving-between-siblings is still owed too.
* **The other ~25 `escape()` sites** carry the same two-parser hazard on USER text — new item #25.
* **blueprint's `tabs` row is still 125 columns wide in a 52-column gallery box**, untouched again,
  still the reason there is no whole-gallery width law. It has now been named as "the next gallery
  item" twice.
* `switch()`, `checkbox()`, `radio_group()` and now `button()` are siblings around one composer —
  duplication of a CALL, not of a decision. Still left alone deliberately.
* The **gauge** still carries its own copy of the value arithmetic (pass 48's note, unchanged).

### Next

1. **`text field` — the first component with a cursor INSIDE it.** The button proved text can be
   content; a text field asks whether a CARET is a part. It plausibly is: it is drawn by the
   language, it has its own state (blinking, at a position), and it is not the caller's. If so, the
   registry gains its first part since the contract was written — and the axis it introduces is
   EDITED as a *live* state rather than a styled one, plus a placeholder, plus INVALID, which is the
   first state that is not about interaction at all.
2. Then **stepper** (a set the arrows spin through — the wrap-vs-clamp axis, already named at the
   radio's live seat) and **scroll bar** (the first component whose value is a WINDOW, two numbers,
   not one).
3. **Three instrument items owed:** `test_win_clipboard_roundtrip` needs a skipif or a mock (#22,
   firing for three passes), item #25's escape sweep, and blueprint's `tabs` row.

---

## FIFTY-FIRST PASS — the COMPONENT CONTRACT, increment 4 (radio · the sibling test)

**What this pass is.** The fourth increment, and like the third it was chosen as an EXPERIMENT.
Every component up to now answers from its own value: a slider from its number, a switch and a
checkbox from their bit. A radio item is `checked` because a SIBLING is not — so the question was
whether a contract built entirely out of per-component facts can hold a state whose SCOPE is larger
than a component, and whether `with_checked` survives contact with an invariant ("exactly one of
these is set") that no single component owns.

### THE GROUP-SCOPE VERDICT, argued from where the fact had to live

**The contract CAN express sibling state, and the seat it needed is one function — but that seat is
NOT the parts registry, and the boundary is the finding.** `COMPONENT_PARTS["radio"]` is
byte-identical to the checkbox's `("main", "knob")`, and it is *right* to be: the registry describes
what one component is made of, and "my sibling is set" is not a part. Asking the registry to carry
the group would have been asking a per-component table to hold a per-set fact. So the scope landed
one level up, at **`group_states(n, selected, state, focus)`** — module-level, beside
`with_checked`, and **naming no component in its code**, which is the source-level law that makes
"the contract grew a scope" provable rather than claimed. A segmented control and a tab bar are the
same fact about siblings wearing different glyphs, and they will land at this seat too.

**The invariant is not CHECKED, it is UNREPRESENTABLE, and that distinction is the whole design.**
"Exactly one of these is set" is never validated anywhere: the bit is computed from `i == selected`,
and an integer cannot equal two values or none. There is no per-item boolean for a caller to
desynchronise — which is why **`radio_items` has no `on` parameter at all**, where `switch(on)` and
`checkbox(on)` both do. That missing argument IS the group scope, and the suite asserts its absence
off `inspect.signature` rather than trusting the prose.

**`with_checked` survived, and the precise reading is that its WRITER did not change while its
AUTHOR moved.** The bit is still written in exactly one place; what changed is who calls it. Before
this pass a caller handed a component its bit; now `group_states` derives it and the caller cannot
reach it. Zero edits to `component_states`, `control_of`, `with_checked`, `is_checked`,
`bool_value`, `state_chain`, `checked_pairs` — the fourth component in a row to inherit the
eight-state axis without being named at a derivation seat.

**What DID have to grow, and it was two seats, both about the LABEL rather than the state:**

1. **`_component` was split.** A checkable appends `check_label` — the language's own `ON` / `--` /
   `posted` word. A radio item's word is the **OPTION'S**, supplied by the group, so `posted` beside
   `fast` would be the language answering a question nobody asked. `_component_body` is now the
   control itself and `_component` is body + label; the radio uses the body and prints its own word.
2. **`check_tone` came out of `check_label`.** Two components print a word beside a checkable for
   two different reasons and both obey one tone rule (lit when set, muted when not, dim when dead).
   One seat, so the rule cannot fork.

Both are component-blind and the source-level law is asked of them, same as the composer seats.

**FOCUS IS THE SECOND THING THE GROUP INTRODUCED, and it is a real axis, not a rename.** The cursor
and the choice are two indices, and they may be on different items — both on screen at once, both
readable with colour stripped. That is the sibling-scoped version of the EDITED-is-not-FOCUSED
problem the state axis was built for, and it is asked of all ten languages at every control state.
Two matching decisions fell out and are asserted rather than assumed: **a group at rest draws no
cursor** (untouched siblings are identical, which is what makes the focused reading a signal rather
than decoration), and **a DISABLED group drops its cursor entirely** — a dead control does not hold
focus.

**And a set with nothing set RAISES rather than clamping.** An out-of-range `selected` is the one
way to ask for zero marks; a clamp would silently move the user's choice. The suite drives
`(-1, 3, 4, 99)` and `n=0` into it and requires `ValueError` each time.

### Seat verdicts — ten languages, ten radio sets

The rule the skill imposes is its one constraint on this component (`checkbox / radio set | distinct
from switch: N-of-M vs on/off`), and it is honoured on two channels: the well is a different SHAPE
FAMILY from the box where the language can afford one, and the set prints **every option's name at
once** where a switch prints one state.

| language | the well | the mark | vs its own checkbox | containment |
|---|---|---|---|---|
| **nord** | `( ) < > « » (╌)` | `(o) <o> «●» (╳)` | round where the box is square — the terminal's own convention, inherited like everything else here | **framed** |
| **naught** | `○ ◌ ◦ ⋅` | `⊙ ⊚ ● ⊗` | **the one language that CANNOT afford the family distinction** — the lattice dot is its whole vocabulary, so both are round; what it affords instead is a ring-with-a-centre against a filled dot | **span-only** |
| **corgi** | `▁◦ ▔◦ ▂◦ ·◦` | `▁● ▔● ▂● ·◌` | the LED beside the label (a parameter CHOSEN) against a segment driven (a setting): cell one carries the control state, cell two the choice | **span-only** |
| **instrument** | `⠐ ⠰ ⠘ ⠈` | `⠶ ⠾ ⠷ ⠦` | the register read as a RING (outer dots set) against the checkbox's LEVEL (driven bottom-up) | **span-only** |
| **swiss** | `╵ ╵ ╹ ╹ ▀ ▀ ╎ ╎` | `╵•╵ ╹•╹ ▀●▀ ╎·╎` | **the typographic distinction this language of all ten is entitled to**: round bullet marks a choice, square bullet marks a box; rules shortened to half-height so the well reads lighter | **framed** |
| **industrial** | `< > <_> <-> (-)` | `<O> <#> <@> (o)` | **could NOT take the round bracket** — this vocabulary already spends round brackets on "not an input", so the selector is angled and the DISABLED radio keeps the round bracket because here it still means dead | **framed** |
| **darkside** | `‹ › « » ▶ ◀ ┄ ┄` | `‹◦› «◉» ▶●◀ ┄▫┄` | **could not take it either, for the opposite reason**: the round bracket IS the port and the checkbox is standing in it, so the radio is the port seen edge-on | **framed** |
| **ledger** | `┊ ┊ ▶ ┊ ▶·┊ ╌ ┊` | `┊●┊ ▶●┊ ▶◉┊ ╌▫┊` | a cell POSTED against a cell STRUCK, right rule dotted; tally pointer still grows on focus | **framed** |
| **solari** | `▁▁▁ ▔▔▔ ▂▂▂ ╌╌╌` | `▁●▁ ▔◉▔ ▂█▂ ╌▫╌` | the WHOLE card (seam unbroken) against the checkbox's split seam — a departures board turns a card, it does not tick a box | **framed** |
| **blueprint** | `┤ ├ ╡ ╞ ┫ ┣ ╏ ╏` | `┤○├ ╡◉╞ ┫●┣ ╏╌╏` | the datum turned INWARD (a callout selecting from a schedule) against the checkbox's outward dimension; nothing is boxed, and the law survives the new component | **framed** |

**Seven framed, three span-only — the same split as the checkbox and for the same measured reason,
and it is printed by the suite rather than remembered.** A one-cell well has no interior, so the
"the well SURVIVES the mark" clause is only expressible where a language has three cells to spend.
**Two languages had their family choice OVERRULED by their own declared law** (industrial's round
brackets mean dead; darkside's round bracket is the port) — the skill loses to the language on its
own vocabulary, which is the rule this repo has followed since the double-line box family was ruled
out of a display type.

### The live seats

* **Config screen (`c`): the radio HAS a live seat, and it is the one the fiftieth pass said the
  checkbox could not honestly take.** Every signal runs in exactly one **worker group** — `fast` or
  `slow` — and which one decides whether the fast hero loop or the slow filesystem loop recomputes
  it. That is a real consequence, already in the model, not a field invented for a demo. The row's
  group cell was a printed word; it is now a set with both options named and exactly one marked.
  `left`/`right` (and `h`/`l`) cross it, **clamping at the ends** — a set the arrows spin through is
  a stepper. The keys needed **no new binding**: the app's arrows are `priority=True` and were
  already delegated DOWNWARDS to a screen with its own cursor, so the fix was the same delegation
  SIDEWAYS, three lines at the seat that already existed. A group nobody can cross is a picture of a
  control, and the suite presses the real keys and reads the ENGINE, not the render.
* **N=2, and that is stated rather than dressed up.** It is the weakest honest N-of-M in this app,
  and it was taken over inventing a richer one. What keeps it a radio and not a switch is exactly
  the skill's constraint: **both options are named on screen with one marked**, where a switch shows
  one bit. The suite asserts `len(WORKER_GROUPS) == 2` so nobody reads more into it than is there.
  The obvious richer seat — the LANGUAGE, ten options, exactly one active — is app state rather than
  config state and would be a new section on this screen; it is named here and not built.
* **The set is the ENGINE'S, held against its source.** `WORKER_GROUPS` is one declaration in
  `app.py`, and a check reads `Engine.run_all`'s own source for the group names it iterates and
  requires the two to be equal. A third loop cannot appear with no way to choose it, and a chooser
  cannot offer a loop nothing runs.
* **A WIDTH COST, measured, and REFLOWED rather than shipped as a regression.** A selection set
  costs the config row 13 cells over the word it replaces — ledger, the widest, goes **66 -> 79**,
  which is more than the `widget` size class (46-79 columns) has. Rather than wrap a row (a wrapped
  row puts the threshold slider under the wrong signal), `redraw` measures the assembled block and
  falls back to the printed word, ONE decision for the whole screen so the column cannot jitter.
  Measured: at 80 every language keeps the radio; at 70 five keep it and five fall back; at 60 all
  ten are back to **exactly the pre-pass widths (63-66)**. Zero regression below the fold.
* **Gallery (`g`):** a `radio` block of four rows, one per control state, every row drawing the same
  set with `mid` chosen and the cursor on `hi` — so what the eye must survive is not "what does
  focused look like" but "which of these is chosen while a different one is under the cursor". It
  measures itself the way `checkable_block` does: 5 rows across at 45 columns, reflowing to 13 rows
  down at 28 when it will not fit.

### Verification — `verify_language.py` 3719 -> **6062** (+2343)

Registry laws (the item's parts identical to the checkbox's, CHECKABLE, the axis identical for the
third time, no EDITED, `checked_pairs` shared) · **source-level laws on the new seats** —
`group_states`, `_component_body` and `check_tone` each read with `inspect.getsource` and required
to name NO component, plus `with_checked(` present in `group_states` (the bit's writer is unchanged)
and `group_states(` present in `radio_items` with **no `on` parameter anywhere**, against the
contrast that `switch` and `checkbox` both have one · the invariant over the **product** of group
size 1-6 x every selection x every control state x every cursor position, each requiring exactly one
checked and it on the selected item · the raise on `(-1, 3, 4, 99)` and on `n=0` · and per language:
its own glyph tables, one mark on the render at every combination, focused-vs-checked-vs-untouched
distinct after colour-strip at FOCUSED and ACTIVE, no cursor at rest, no cursor when disabled and
every item dimmed, the (well, mark) pair distinct from the (box, tick) pair at every state,
containment in both clauses with the framed count printed, eight states pairwise distinct, per-item
anti-jiggle across every selection and cursor position, one well width, single-slot paint per item,
every option's word printed, **CHECK_WORDS absent from a radio** in the three languages that have
them, the pass-48 accent law asked a fourth time, and the greyscale projection checked against
rich's parser on every radio string. Plus ten-way distinctness, radio-is-not-checkbox and
radio-is-not-switch per language, four gallery laws per language, three anti-drift laws on the live
set, and **four driven checks that press real keys and read the engine**.

**THE INSTRUMENT DEFECT THIS PASS FOUND, and it is the valuable half again.** Round one of the
mutations caught eleven of twelve — but **M8 (`radio_items` ignores the group and marks everything)
was caught by exactly ONE law, and that law was source-level.** The reason is that every behavioural
law composed `group_states` and `component_cells` *itself*, which measures the derivation and never
`radio_items` — **the seat the config screen and the gallery actually call was untested.** A
render-level count was added (strip each rendered item, classify its head cell as a well or a mark,
require exactly one mark on the selected item), gated by a precondition law that no well glyph is
also a mark glyph. **M8 went from 1 red to 361.** And `M8b` — a mutant that CALLS `group_states` and
then throws the result away, which the source law cannot see — is caught 360 red by the new law
alone. That is the difference between testing a design and testing a render.

**Mutations — twelve injected in round one, four more in round two.**

| mutation | result |
|---|---|
| M1 the out-of-range guard is dropped (a bad selection clamps instead of refusing) | 1 red |
| M2 TWO items checked — the bit becomes a neighbourhood, not a comparison | **1422 red** |
| M3 ZERO items checked — the mark never appears | **1430 red** |
| M4 focus FUSED to the selection — the cursor can no longer be off the chosen item | 21 red |
| M5 a DISABLED group keeps its cursor | **SURVIVED — and it was NOT a hole, see below** |
| M6 nord stops declaring its own radio well (falls back to the shared parts) | 16 red |
| M7 the radio IS the checkbox — one language copies the other's well and mark | 9 red |
| M8 `radio_items` takes the bit from a caller instead of the group | 1 red -> **361 red after the cure** |
| M8b it calls `group_states` and ignores the result (invisible to the source law) | **360 red** — the new law alone |
| M9 the live set WRAPS instead of clamping | 2 red |
| M10 the app stops delegating sideways — the live group goes inert | 2 red |
| M11 the config screen offers a group no worker runs | 3 red |
| M5b [corrected] a DISABLED group really does keep a live cursor | **11 red** |
| M12 **[control on the driver]** `group_states` raises on every call | **DEAD RUN — 1705 pass, 0 red, and the driver said so** |

**M5 IS THE LESSON OF THIS PASS AND IT IS A LESSON ABOUT MUTATION TESTING.** It reported SURVIVED,
which reads as a harness hole — and it was not one. The replacement guarded the DISABLED branch by
focus, so the focused item fell through to the `elif`, which assigns `base = ctl` — and `ctl` **is**
`DISABLED` there. The mutant emitted byte-identical states: **it changed the code and not the
behaviour.** A driver cannot tell a vacuous mutation from a missing law, exactly as pass 50's driver
could not tell a dead run from a clean one, and the same cure applies — write the mutation so it
fires, then look. `M5b` does keep a live cursor on a dead group and goes **11 red**. *Neither
SURVIVED nor 0-red is evidence on its own; the mutant has to be shown to change something first.*

### LOOK

The gallery's radio block, verbatim from `g`, colour stripped. Every row: **`mid` is chosen, the
cursor is on `hi`** — two different items, both readable, no colour doing any of the work.

```
nord
radio      lo·mid·hi  set=mid cursor=hi
           ( ) lo  (o) mid  ( ) hi   default
           ( ) lo  (o) mid  < > hi   focused
           ( ) lo  (o) mid  « » hi   active
           (╌) lo  (╳) mid  (╌) hi   disabled

ledger
radio      lo·mid·hi  set=mid cursor=hi
           ┊ ┊ lo  ┊●┊ mid  ┊ ┊ hi   default
           ┊ ┊ lo  ┊●┊ mid  ▶ ┊ hi   focused
           ┊ ┊ lo  ┊●┊ mid  ▶·┊ hi   active
           ╌ ┊ lo  ╌▫┊ mid  ╌ ┊ hi   disabled

instrument   (span-only: the well is ONE braille cell)
radio      lo·mid·hi  set=mid cursor=hi
           ⠐ lo  ⠶ mid  ⠐ hi   default
           ⠐ lo  ⠶ mid  ⠰ hi   focused
           ⠐ lo  ⠶ mid  ⠘ hi   active
           ⠈ lo  ⠦ mid  ⠈ hi   disabled
```

Note the `default` row in all three: the cursor is INVISIBLE at rest, which is the law that makes
the `focused` row's third item mean something.

**And the LIVE seat, verbatim from `c` at 118 columns** — the cursor is on the first row (its help
line shows), every signal is in exactly one group, and the last two sit in `slow`:

```
nord
    ██▌ ! Overdue count        (o) fast  ( ) slow    2s   2
    ██▌ ~ Work in flight       (o) fast  ( ) slow    2s   6 ██▌───── 3
    ██▌ x Blocked              (o) fast  ( ) slow    3s   2
    ██▌ $ Workday budget       ( ) fast  (o) slow   30s  17 ████▌─── 18
    ██▌ # Board file           ( ) fast  (o) slow   20s   1

ledger   (the switch prints `posted`; the RADIO prints the option, never CHECK_WORDS)
    ──▪ posted o/d Overdue count        ┊●┊ fast  ┊ ┊ slow    2s   2
    ──▪ posted w/p Work in flight       ┊●┊ fast  ┊ ┊ slow    2s   6 ──▪····· 3
    ──▪ posted hld Blocked              ┊●┊ fast  ┊ ┊ slow    3s   2
    ──▪ posted day Workday budget       ┊ ┊ fast  ┊●┊ slow   30s  17 ────▪··· 18
    ──▪ posted led Board file           ┊ ┊ fast  ┊●┊ slow   20s   1
```

### The checkable family is CLOSED

switch (a boolean read as a POSITION) · checkbox (a boolean read as PRESENCE) · radio (a bit that is
not the item's own). Three anatomies, one axis, one derivation, one bit-writer. What the family
still does not have is **motion** — `flip_frames` names `switch` literally and walks a knob across a
track; a checkbox's transition is a mark appearing and a radio's is a mark MOVING BETWEEN SIBLINGS,
which is a third tempo question and the first one that is about a group. Not built, not faked, and
no language is missing anything a user has named.

### Open, and honest

* **`RUN.md` does not document the config screen's new `left`/`right`.** They were already bound
  app-wide as motion keys (`show=False`, listed in the `?` map), so no legend law is broken and no
  key is advertised that does not fire — but the file that tells a human what the keys do is now one
  behaviour short. It was outside this increment's five-file budget. **Fix it at the next `RUN.md`
  touch.**
* **The config screen still does not route on size class.** The reflow added here is a width
  MEASUREMENT at one seat, not size-class routing; the screen has always been size-blind (item #4's
  family) and still is. What changed is that it now degrades instead of wrapping.
* **blueprint's `tabs` row is still 125 columns wide in a 52-column gallery box** — measured by the
  fiftieth pass, untouched by this one, still the reason there is no whole-gallery width law. **It
  should be the next gallery item.**
* **The radio has no `flip_frames`** — see above.
* `switch()`, `checkbox()` and now `radio_group()`/`radio_items()` are thin siblings calling one
  composer. Still duplication of a CALL and not of a decision; still left alone deliberately.
* The **gauge** still carries its own copy of the value arithmetic (pass 48's note, unchanged).

### Next

1. **`button` — the control with NO VALUE.** Every component in the registry so far has one: a
   slider's number, a checkable's bit, a group's index. A button has none — it has only an
   ACTUATION, so the axis it introduces is the one LVGL calls PRESSED and this contract has been
   calling ACTIVE without ever having a component for which ACTIVE is the *whole point*. Two
   questions it will force: (a) does `component_states` still derive honestly when there is no value
   to be EDITED or CHECKED — i.e. is the axis `default / focused / active / disabled` and nothing
   else, falling out of `"knob" in parts` with no new registry fact; and (b) what are a button's
   PARTS, given that its label is inside it rather than beside it, which no component so far has had
   (`value_label` and the option word both stand OUTSIDE the control). That second one is the real
   increment: it is the first time the registry has to decide whether text is a part.
2. Then text field (a caret and a placeholder — the first component with a cursor INSIDE it),
   stepper, scroll bar.
3. **Two instrument items still owed:** `test_win_clipboard_roundtrip` needs a skipif or a mock
   (#22, firing for two passes now), and blueprint's `tabs` row needs to come down to the gallery's
   width.

---

## FIFTIETH PASS — the COMPONENT CONTRACT, increment 3 (checkbox · the generalisation test)

**What this pass is.** The third increment, and the one that was chosen as an EXPERIMENT rather than
as a feature. A switch is a slider whose range is boolean — same three parts, same track, the
checked bit read as a POSITION. If `CHECKABLE` and the product state axis only worked because of
that geometry, the first checkable with NO extent would break them. The checkbox is that component:
a box and a mark, `("main", "knob")`, no indicator, a mark that APPEARS rather than travels.

### THE VERDICT, argued from which seats had to change

**CHECKABLE is a real registry fact. The product state axis generalised with ZERO edits.** Adding
`"checkbox"` to one tuple gave it the whole eight-state axis —
`default · focused · active · disabled` × the checked bit, EDITED dropped — and not one line of
`component_states`, `control_of`, `with_checked`, `is_checked`, `bool_value`, `state_chain` or
`checked_pairs` moved. `CHECK_WORDS` came along for free too: corgi, ledger and solari print their
word beside the checkbox because `_component` asks `name in CHECKABLE`, and nobody told it about a
checkbox. This is not asserted from memory — it is a **source-level law**, pass 44's discipline:
each of those seven functions is read with `inspect.getsource`, docstrings and comments stripped,
and must contain **no component name at all**. A derivation that says `if name == "switch"` passes
every behavioural check and is still a special case wearing a contract's clothes.

**What did NOT generalise was the COMPOSER, and naming it precisely is the finding.** Three seats
had to grow, and all three are about GEOMETRY, none about state:

1. **`component_cells` assumed every component has an extent.** It walked the slots comparing them
   to a value POSITION. Run that with `("main", "knob")` and it emits `indicator` — a part the
   checkbox does not declare — and marches the mark along a track. It now has two compositions:
   *extent* (the value picks a position) and *no extent* (the value picks PRESENCE, answered by the
   same `value_pos` so an inverted scale still inverts and no second arithmetic is born).
2. **`part_slots` had a two-slot floor**, which is a fact about tracks. A component with no
   indicator gets exactly ONE slot and **the width request dies at that boundary** — which is why
   `checkbox(on, state)` takes no `w` at all. A wide box with a mark loose in it is a track, and a
   track is the switch, one method up.
3. **Glyphs needed a COMPONENT SCOPE.** `PART_GLYPHS` was keyed by part alone, so a checkbox would
   have had to draw its box with the slider's track glyph. `component.part` now wins over `part`
   (`"checkbox.main"`, `"checkbox.knob"`), additively — nothing in the value family moved.

**And the branch is on the REGISTRY, not on a name.** `"indicator" in parts` is what selects the
composition, the slot count AND the chrome (chrome fixes the ENDS OF A TRACK; industrial and
blueprint would otherwise have double-boxed their own boxes). One registry fact, three consequences,
one seat each — and the source-level law is asked of the composer too, so "the contract grew an
anatomy" is provable rather than claimed.

**So the honest split is:** *the state axis belongs to CHECKABLE; reading a boolean as a POSITION
belonged to the switch.* The pass-49 sentence "checked vs unchecked is carried by the knob's
POSITION, shape in all ten for free" was TRUE OF THE SWITCH ONLY. On a checkbox the bit is carried
by the mark's PRESENCE, and that costs each language a real glyph table instead of nothing.

**The checkbox's completeness law is DIFFERENT from the switch's, and that difference is the
anatomy talking.** A switch draws its knob in all eight states and collapses an extent; a checkbox
has no extent to collapse, so what it collapses is the MARK: **zero knobs unchecked, exactly one
checked.** Over the pair both declared parts appear — the same "zero extent at an instant, whole
over the pair" the switch's indicator taught, with a different part doing it.

### Seat verdicts — ten languages, ten checkboxes

| language | the box | the mark | containment |
|---|---|---|---|
| **nord** (base) | `[ ]` → `▐ ▌` → `▓ ▓` → `╌ ╌` (bracket weight carries the control state) | `x`, `╳` when dead | **framed** — the terminal's own `[x]` / `[ ]` |
| **naught** | ONE lattice dot, hollow: `◦ ○ ◌ ·` | inked: `◉ ● ◍ ◎` | **span only** — the lattice has no chrome, and wrapping the dot in brackets would be drawing another language's checkbox |
| **corgi** | the baseline LCD segment `▁▁ ▔▔ ▂▂ ··` | the same cell driven full: `██ ▛▜ ▓▓ ▒▒` | **span only** (two cells, no interior) |
| **instrument** | one braille register cell `⠒ ⠛ ⠤ ⠁` | driven: `⣿ ⣶ ⣤ ⠿` | **span only** — the eight dots ARE the box |
| **swiss** | two rules, by weight: `│ │ ┃ ┃ █ █ ┆ ┆` | `▪` / `▮` set between them | **framed** |
| **industrial** | `[ ] [_] [-]`, and `(-)` when dead — round brackets say "not an input" | `X # *`, `x` | **framed** — the `[X]` its switch was already quoting |
| **darkside** | the port: `( ) [ ] { } ╌ ╌` | `O ◎ ●`, `x` | **framed** |
| **ledger** | a ruled cell `│ │`, with the tally pointer `▶` on the focused row | `×`, `●` live, `▫` dead — plus `open`/`posted` from CHECK_WORDS | **framed** |
| **solari** | one flap, seams above and below: `▁ ▁ ▔ ▔ ▁·▁ ╌ ╌` | the face turned: `▼ ▲ █ ▽` — plus `OFF`/`ON ` | **framed** |
| **blueprint** | **NOT A BOX** — a datum between terminators: `├ ┤ ╞ ╡ ┣ ┫ ╎ ╎` | the note `╪` entered between them | **framed**, and its "nothing is boxed" law is intact |

**Containment is stated in two clauses because only one of them is universal.** *(a)* the mark
occupies exactly the box's span — every language answers it; *(b)* the box SURVIVES the mark, first
and last cell unchanged and the difference strictly interior — expressible only where a box has an
interior. **Seven of ten are framed; naught, corgi and instrument are span-only, and the suite says
which rather than pretending the weaker clause is the strong one.** A law that cannot fail is worse
than a law that admits its reach.

### The live seats

* **Config screen (`c`): NO checkbox, and that is a decision, not an omission.** The row has exactly
  one boolean and the switch already owns it honestly; two controls for one bit is a demo, not a
  seat. The distinction between them is real — a switch is a setting that acts at once, a checkbox
  is a SELECTION WITHIN A SET — and this screen has no set to select from. What would earn the
  checkbox a live seat is a multi-select, which is the radio/group component. The reason is written
  at the seat in `app.py` so a later pass does not "fix" the absence.
* **Gallery (`g`): the layout question is ANSWERED, not deferred a third time.** switch and checkbox
  share the ROW UNIT because they share the AXIS (`checked_pairs` returns the same four pairs for
  both). Whether they share the ROW is **measured per language**: paired costs 5 rows for two
  components, stacked costs 8. Seven languages fit the paired block in the box's 52 columns; corgi
  (54), solari (56) and ledger (68) print a word beside the control and stack. The check reads the
  screen's OWN seat (`app.checkable_block`) instead of rebuilding the arithmetic — and it proves the
  choice is the measurement's by asking the same function at w=200 (must pair) and w=20 (must
  stack), plus a completeness law at every width so a layout can never fit by dropping a state.

**AND THE GALLERY STILL SCROLLS, which is now a MEASURED decision rather than an open item.** At
118x30 the box is 22-24 rows and the guide is 39-57:

| naught | corgi | instrument | swiss | industrial | nord | darkside | ledger | solari | blueprint |
|---|---|---|---|---|---|---|---|---|---|
| 53 / 22 | 53 / 22 | 54 / 22 | 41 / 22 | 50 / 22 | 57 / 22 | 39 / 22 | 46 / 24 | 42 / 24 | 47 / 24 |

Pairing saved 3 rows against an overflow of 17-35. **Tiering cannot solve this and pretending it
could is why it was deferred twice**: a complete style guide for a language — brand, ten components,
five data-viz primitives, a card, a head — does not fit in a terminal, and the honest response is a
box that scrolls rather than a guide that lies about being complete. The layout work that WAS worth
doing is the one that keeps rows from wrapping, and that is measured above.

### Verification — `verify_language.py` 3098 → **3719** (+621)

Registry laws (two parts, no indicator, CHECKABLE, the axis identical to the switch's, no EDITED,
`checked_pairs` shared) · **seven source-level laws on the derivation seats and six on the composer
seats**, each asserting the CODE names no component · no-extent laws (one slot at every width, no
chrome, while the slider keeps the chrome it declares) · and per language: its own glyph tables,
zero-marks-unchecked / one-marked, never an indicator in any state, both parts across the pair,
shape difference at every control state, all eight states pairwise distinct after colour-strip,
`checked+disabled` distinct from both halves, containment in both clauses with the framed count
printed, one width across all eight states with the printed word included, the mark's seat stable
AND present, single-write paint, the bit-cannot-disagree law, disabled shape-marked and dimmed, the
pass-48 accent law asked a third time, and **the greyscale projection checked against rich's own
parser on every string**. Plus ten-way distinctness, checkbox-is-not-switch per language, four
gallery laws per language, and three in-suite controls (an escaped mark, a colour-only mark, an
always-marked box).

**TWO INSTRUMENT DEFECTS FOUND, and they are the more valuable half of this pass.**

1. **`grey()` was not rich's parser and the checkbox proved it.** The projection stripped anything
   shaped like `[...]`. rich reads a bracket as markup **only** when the next character is
   `[a-z#/@]` (`rich.markup.RE_TAGS`), so `[ ]`, `[X]`, `[-]` and `[◎]` are LITERAL TEXT on screen.
   The instrument measured nord's three-cell box as **zero cells wide** — it would have certified an
   invisible control and a gallery row that fits. Fixed to rich's definition, and `grey_is_rich`
   now checks the projection against `Text.from_markup` on every component string. *(Using rich's
   parser directly was tried first and DIED: the hero hands `grey` single ROWS of a block whose tags
   span lines, and rich raises `MarkupError` on a fragment with an orphan `[/]`. So the projection
   stays fragment-safe and is held to rich by a law instead.)* Swapping it moved **zero** of the
   3098 existing checks, which is what makes it a safe correction rather than a rewrite.
2. **The suite was reading the user's live `board.json`** — see the closing block above. Found by
   chasing a red that turned out to be a clock.

**Mutations — six injected plus one control ON THE DRIVER.** The driver reports the exit code, the
PASS count, and whether the suite **reached its own verdict line**, because pass 49's driver counted
reds only and a dead run looked exactly like a clean one.

| mutation | result |
|---|---|
| M1 checkbox no longer declared CHECKABLE | 107 red |
| M2 the checkbox declares an INDICATOR (an extent it does not have) | 125 red |
| M3 the mark stops reading the value (always present) | 113 red |
| M4 nord stops declaring its own checkbox glyphs (falls back to the slider's) | 12 red |
| M5 a no-extent component gets TWO slots (a box with room to wander) | 22 red |
| M6 a declared part is renamed — the composer draws a part nobody declared | 82 red |
| M7 **[control on the driver]** glyph scoping loses its fallback, so rendering RAISES | **DEAD RUN — 1 pass, 0 red, and the driver said so** |

**M1 exposed a raising law, and that is the pass-49 lesson repeating one level down.** The
mark-does-not-travel check indexed the first knob (`[0]`); a checkbox with no checked bit draws no
mark, so the law **crashed instead of going red** — and a raised law reports nothing. The seat is a
tuple now, so its presence is part of the condition. *The driver's first verdict heuristic was also
wrong and was corrected: "fewer checks than baseline" is NOT evidence of death, because a registry
with fewer states legitimately runs fewer laws. The suite's own verdict line is the evidence.*

### LOOK

The checkable block, verbatim from `g` — nord and blueprint PAIRED, ledger STACKED:

```
nord
checkable  switch    checkbox  off·on
           ▌──  ██▌  [ ]  [x]   default
           ▐──  ██▐  ▐ ▌  ▐x▌   focused
           ▓──  ██▓  ▓ ▓  ▓x▓   active
           ╳╌╌  ▒▒╳  ╌ ╌  ╌╳╌   disabled

blueprint
checkable  switch    checkbox  off·on
           ├┤·  ├─┤  ├ ┤  ├╪┤   default
           ├╡·  ├─╡  ╞ ╡  ╞╪╡   focused
           ├┫·  ├─┫  ┣ ┫  ┣╪┫   active
           ├╎╌  ├┄╎  ╎ ╎  ╎╌╎   disabled

ledger  (68 columns paired — it stacks, and keeps its printed word)
switch     ▪·· open    ──▪ posted   default  off·on
           ▶·· open    ──▶ posted   focused
           ●·· open    ──● posted   active
           ▫╌╌ open    ┄┄▫ posted   disabled
checkbox   │ │ open    │×│ posted   default  off·on
           ▶ │ open    ▶×│ posted   focused
           ▶·│ open    ▶●│ posted   active
           ╌ ╌ open    ╌▫╌ posted   disabled
```

The layout, before and after: pass 49 shipped four `switch` rows with the label in column one. This
pass replaces them with a **labelled two-column block** — a header row naming both components,
then one row per control state — where it fits, and with two four-row blocks where it does not.
Net cost of a whole new component: **+1 row** in seven languages, +4 in three.

### Open, and honest

* **A pre-existing gallery defect this pass MEASURED but did not fix: blueprint's `tabs` row is 125
  columns wide** in a 52-column box (three rows over: 125, 114, 114). It is blueprint's title-block
  treatment escaping the modal, it predates this pass, and fixing it is not a checkbox increment. It
  is the reason the suite has a per-language checkable-block fit law and **not** a whole-gallery
  width law — a whole-gallery law would be red today. **It should be the next gallery item.**
* **The checkbox has no MOTION.** `flip_frames` names `switch` literally and walks a knob across a
  track; a checkbox's transition is a mark appearing, which is a different tempo question. Not
  built, not faked, and no language is missing anything a user has named.
* **`switch()` and `checkbox()` are two one-line siblings**, both calling `_component` with
  `with_checked`. The bit is still written in exactly one place, so this is duplication of a call,
  not of a decision. Left alone deliberately: an abstraction over two lines would be premature.
* **Three languages are span-only on containment** (naught, corgi, instrument), stated above.
* The **gauge** still carries its own copy of the value arithmetic (pass 48's note, unchanged).

### Next

1. **`radio` — and it should be next, ahead of button.** Reason: it is the first component whose
   state depends on its SIBLINGS, and that is the axis the registry has never been asked about. Every
   component so far answers from its own value; a radio in a group of four is `checked` because
   another one is not, so the question is whether the contract can express a component whose state
   has a SCOPE larger than itself — and whether `with_checked` survives contact with an invariant
   ("exactly one of these is set") that no single component owns. It also buys the config screen a
   real live seat, which the checkbox honestly could not take. Button introduces a different axis (a
   control with NO value at all) and is cleaner once the checkable family closes with its group form.
2. Then button, text field, stepper, scroll bar.
3. **Two instrument items this pass created work for:** give `test_win_clipboard_roundtrip` a skipif
   or a mock (#22, now firing), and take blueprint's `tabs` row down to the gallery's width.

---

## FORTY-NINTH PASS — the COMPONENT CONTRACT, increment 2 (switch · CHECKED)

**What this pass is.** The second increment. The first CHECKED-bearing component, and the first
test of whether the pass-48 state derivation generalises past the value family. It does — but only
after the derivation grew one seat, and the growth is the finding.

### THE REGISTRY DECISION, argued

```python
COMPONENT_PARTS["switch"] = ("main", "indicator", "knob")   # the SAME three as slider
CHECKABLE = ("switch",)                                     # the one fact that differs
```

**The switch declares THREE parts, not two, and it declares the SAME three the slider does.** The
brief left this open — `(main, knob)` or `(main, indicator, knob)` — and offered the reading that a
switch's indicator "collapses into the knob's position". Measured, that reading is half right and
the half it gets wrong is the important half.

*The argument is the composer, not LVGL's authority.* Run the shipped `component_cells` with
`lo=0, hi=1` and the terminal's conventional switch falls out with **no special case**: the knob
lands at one end or the other, the cells behind it are indicator, the cells ahead of it are track.
At three slots that is `██▌` / `▌──` — which is, cell for cell, the switch nord was already
shipping by hand. The registry cannot tell a switch from a slider **because on the axis the
registry measures they are the same thing**: a switch is a slider whose range is boolean. Declaring
two parts would have been declaring a picture.

*What the indicator actually does.* It does not collapse into the knob. It collapses to **zero
extent** — and so does the track, at the other position. At any instant a switch draws two of its
three parts; over the pair it draws all three. That is precisely what "a range with no interior"
means, and it is now a law in both directions (`all three across the two positions`, `exactly one
of main/indicator empty at either`).

**THE CONSEQUENCE FOR DERIVED STATES, which is where the pass earned its keep.** `CHECKABLE` is one
registry fact with two consequences, and both are derived:

1. **CHECKED is a BIT that combines, so the axis is a PRODUCT.** LVGL styles `CHECKED|PRESSED` as
   first-class; a flat six-entry list cannot say that. `component_states` now returns the control
   block, then the same block with the bit set:
   `default · focused · active · disabled · checked · checked+focused · checked+active ·
   checked+disabled` — **eight states, none of them hand-written.**
2. **A switch has NO EDITED state.** EDITED means "focused AND the arrows now RANGE through the
   value". A boolean has no interior to range through: the press toggles at once, and that is
   ACTIVE. So the checkable block drops EDITED — and the slider keeps it, from the same expression,
   which is what proves the removal is derived from CHECKABLE and not from the component's name.
   *(This is the one interpretation call of the pass. It is stated as a law with a control beside
   it: declaring the SLIDER checkable takes ITS edited away too.)*

The bit is written in exactly one place (`with_checked`), read in one place (`is_checked`), and the
renderer takes the switch's VALUE from the state (`bool_value`) rather than from a second argument.
That is why `switch()` cannot render CHECKED with its knob at the off position — not "does not",
**cannot**, and there is a law that says so by construction.

**Nothing new was invented for the render.** No language declares a CHECKED glyph and none needs
one: **checked vs unchecked is carried by the knob's POSITION**, which the pass-48 value model
already moves. Shape, in all ten, for free.

### Seat verdicts — TEN of ten switches violated the contract

Every language had a hand-drawn `switch()`. Judged against the contract, **nine had no knob at all**
and the tenth (nord) had one but no state axis. The one thing a switch IS — a control whose grip
MOVES — was the one thing the axis was not saying.

| language | verdict on the shipped switch | what it became |
|---|---|---|
| **nord** (base) | knob present, but a FIXED string per position and no state axis | the three-part composition; `██▌` / `▌──` is what it was already drawing |
| **naught** | **no knob** — four lit dots vs four unlit dots, a BAR not a switch | knob dot with an eye at either end (`◉◦◦` / `∙∙◉`) |
| **corgi** | **no knob** (`▐█▌ON` / `▐░▌--`: the mark changed glyph, it never moved) | segment height + a moving knob; the printed word survives as `CHECK_WORDS` |
| **instrument** | **no knob** — `⣿⣿` vs `⠒⠒`, fill only | braille knob travelling the register (`⡇⠒⠒` / `⣿⣿⡇`) |
| **swiss** | **no knob** — `━━` vs `──`, weight only | weight kept as the indicator, hairline knob added (`│──` / `━━│`) |
| **industrial** | **no knob**, `[X]` / `[ ]` — a coded mark in a fixed box | brackets stay chrome, the ASCII knob travels (`[\|·]` / `[█\|]`) |
| **darkside** | **no knob** — `(O)` / `( )`, the mark in a fixed port | the STEP indicator and a travelling knob (`O──` / `▬▬O`); KMBlue still reaches only the knob |
| **ledger** | **no knob** — mark + word, two channels but no position | ruled extent, leaders, travelling tally; the WORDS become `CHECK_WORDS = ("open  ", "posted")` |
| **solari** | **no knob** — the flap word `ON `/`OFF` and nothing else | flaps-already-turned as indicator, travelling knob, `CHECK_WORDS = ("OFF", "ON ")` |
| **blueprint** | **no knob** — `├─┤` vs `···`, a span drawn or not drawn | the closing terminator IS the knob and now travels (`├┤·` / `├─┤`) |

**The printed word was never a part and now says so.** Four languages had a word inside their switch
string (`ON`, `--`, `posted`, `open`, `OFF`). That is `value_label`'s seat, which pass 48 already
established stands BESIDE the component; it is declared as `CHECK_WORDS` in three lines and guarded
by an anti-jiggle law (both words the same width, with a control that proves the law fires).

**A conflict surfaced, not averaged — and the language's own test settled it.** The base tone rule
spends `accent` on a knob under interaction. **naught's accent IS red**, and naught's standing law
is that a calm surface carries zero red. The switch's ACTIVE flip frames are the first cell where
the two rules met, and naught's calm-surface check went red the moment they did. The ration wins:
naught now carries a four-line `part_tone` override spending `ink` on the live knob, and its five
knob SHAPES carry the state alone. Darkside and solari keep their opposite override from pass 48.

**A real defect the new laws found in the OLD code.** Corgi, darkside and solari's `part_tone`
overrides compared `state != DISABLED` on the raw string. A COMBINED `checked+disabled` is not equal
to `"disabled"`, so a dead control kept its lit hue / its accent. All three now ask `control_of`.
This was not visible before because there were no combined states to be blind to.

### The live seats

* **Config screen** (`c`): the toggle row is the CHECKED seat, wired honestly.
  `KIT.switch(s.enabled, 3, FOCUSED if selected else DEFAULT)` — so the cursor row renders
  `checked+focused` and the rest render `checked` or `default`. **The switch is never DISABLED here
  and that is not an omission:** a signal you can still switch on is operable by definition. It is
  the THRESHOLD that goes unreachable, and the slider beside it already says so.
* **Gallery** (`g`): pass 48 warned the next component would turn the scrolling box into a defect.
  Eight states at one row each would have cost eight rows. They cost **four**: one CONTROL state per
  row with both bits SIDE BY SIDE, which is not merely frugal — what is worth seeing about a switch
  is what CHECKED does at each state, so the pair IS the comparison. Net growth over the row it
  replaced: **+3**. The 52-column fit is MEASURED per language in the suite, not assumed (ledger
  came out at 53 with the first caption and the legend was shortened to `off·on`).
* **The flip is DERIVED.** Eight languages carried a hardcoded PICTURE of their old switch in
  `flip_frames`; those pictures went stale the instant the switch entered the registry and would
  have animated between two different widths. `flip_frames` now walks the knob across the track in
  ACTIVE and ends on the state. A language keeps its TEMPO (`FLIP_STEPS`, one line — swiss's
  renunciation is `FLIP_STEPS = 0`) and its CHARACTER (its own ACTIVE knob glyph). A
  no-repeated-frame law caught naught and darkside spending a tick on a duplicate frame at two
  steps; both are three now.

### Verification — `verify_language.py` 2529 → **3098** (+569)

Registry laws for the switch (parts, sameness with slider, CHECKABLE, the product axis, no EDITED,
first-class combinations) · the state ALGEBRA (`control_of` / `with_checked` / `is_checked` /
`state_chain`, including "not a substring match") · and per language: part completeness across the
pair, exactly one knob in all eight states, **checked vs unchecked differ in SHAPE at every control
state**, the knob at the two ENDS, the knob position STABLE across control states (a drifting knob
fails even though every state would still look distinct), all eight states pairwise distinct after
colour-strip, `checked+disabled` distinct from both its halves, knob-vs-fill and fill-vs-track shape
distinctness in every state, one width across every state and both positions with the printed word
included, single-write paint, the bit-cannot-disagree law, three flip laws, and **the pass-48 accent
laws re-asked on the new component** (each language spends the accent on exactly the parts its
slider does). Plus the gallery-fit measurement, ten-way switch distinctness, and four in-suite
controls.

**Mutations — five injected into `language.py`, and one of them exposed a HARNESS GAP.**

| mutation | result |
|---|---|
| M1 swiss's ACTIVE knob collapsed onto its FOCUSED knob | 3 FAIL (slider pairwise, EDITED-vs-ACTIVE, switch pairwise) |
| M2 the switch is no longer declared CHECKABLE | **first run: 0 FAIL — AND IT WAS NOT A PASS** |
| M3 the checked bit stops driving the value (knob pinned on) | 118 FAIL |
| M4 EDITED given back to the checkable block | 14 FAIL |
| M5 the glyph chain forgets the CONTROL bit | 31 FAIL |

**M2 is the honest story of this pass.** It reported 0 FAIL. It had not passed — the suite **CRASHED**
(`TypeError`, exit 1) on its very first switch render, and the mutation driver counted `[FAIL]` lines
only, so **a dead run looked exactly like a clean one**. Three fixes, all of them earned:

1. **The driver now reports the exit code and the PASS count** and shouts when a run dies early. A
   mutation table that cannot tell a crash from a clean sheet is telling you nothing.
2. **The composer degrades instead of dying.** The `val is None` substitution is no longer guarded
   by `name in CHECKABLE`, so an un-checkable switch draws a WRONG switch rather than no switch.
3. **Two per-language laws were made non-vacuous.** They indexed a combined state directly and
   would have raised `KeyError` under the mutation; the state's existence is now part of the
   CONDITION, so a registry that stops declaring the combination goes RED instead of skipping.

After the fixes M2 produces **141 FAIL over a complete run**. *A mutation test that finds nothing has
told you nothing — this one found a hole in the instrument, which is the only thing worse than a
hole in the code.*

### LOOK

Gallery, `g`, at the box's 52 columns — three contrasting languages:

```
nord          switch     ▌──  ██▌   default  off·on
                         ▐──  ██▐   focused
                         ▓──  ██▓   active
                         ╳╌╌  ▒▒╳   disabled

ledger        switch     ▪·· open    ──▪ posted   default  off·on
                         ▶·· open    ──▶ posted   focused
                         ●·· open    ──● posted   active
                         ▫╌╌ open    ┄┄▫ posted   disabled

instrument    switch     ⡇⠒⠒  ⣿⣿⡇   default  off·on
                         ⢸⠒⠒  ⣿⣿⢸   focused
                         ⣤⠒⠒  ⣿⣿⣤   active
                         ⠄⠁⠁  ⠶⠶⠄   disabled
```

The live seat, `c`, before and after `down` then `space` (row 1 toggled OFF while focused):

```
solari      ▼ ▁▁▲ ON  DEP Nearest deadline     fast     1s   2     <- checked+focused
              ▁▁▼ ON  LATE Overdue count       fast     2s   2     <- checked
            ▼ ▼·· OFF LATE Overdue count       fast     2s   2     <- focused (unchecked)

blueprint   ┌ ├─╡ DIM Nearest deadline         fast     1s   2     <- checked+focused
              ├─┤ OVR Overdue count            fast     2s   2     <- checked
            ┌ ├┤· OVR Overdue count            fast     2s   2     <- focused (unchecked)
```

### Open, and honest

* **The gallery still scrolls**, and this pass added 3 rows to it rather than 8. The tier-or-second-
  column question from pass 48 is DEFERRED, not solved — it becomes real when button and text field
  land, because neither of those pairs the way the switch did.
* **`w` is a request, not a guarantee**, and corgi shows it: its slots are two cells wide, so a
  switch asked for 3 columns renders 8 (`██ ▁▁ --`). That is the pass-48 `part_slots` floor
  (minimum two slots) behaving as designed, and the anti-jiggle law holds because the width is
  constant. Worth naming because a caller who budgets 3 columns for corgi will be wrong.
* **Solari's `CHECK_WORDS` is drawn in a plain tone, not through its `cell()` flap face.** Its
  `value_label` uses the flap; its check label does not. Cheap to align, not owed.
* **The flip's mid frames can land on the resting position** at two slots (corgi, industrial,
  blueprint) — they are distinguished by the ACTIVE knob glyph, not by travel. Honest, and the
  no-repeated-frame law is what keeps it from being a wasted tick.
* The **gauge** still carries its own copy of the value arithmetic (pass 48's note, unchanged).

### Next

1. **`checkbox` — and it should be next, ahead of stepper.** Reason: it is the cheapest possible test
   of whether CHECKABLE is a real registry fact or a switch-shaped special case. A checkbox is
   `("main", "knob")` — a box and a mark, with **no indicator**, because there is no extent between
   an origin and the mark — so it lands as the FIRST checkable that is not a boolean *slider*, and
   it will tell us in one increment whether `bool_value` and the product axis belong to CHECKABLE or
   were quietly co-designed with the switch's geometry. Stepper is a value component and would test
   nothing the slider has not already tested; button introduces a new axis (a control with no value
   at all) and is better taken after the checkable family closes.
2. Then radio (an N-of-M checkable — the first component whose state depends on its SIBLINGS),
   button, text field, stepper, scroll bar.
3. **Per-language refinements as opt-ins**, unchanged from pass 48 and still owed to nobody:
   corgi's LCD ghosting, solari's flap TURN as knob motion, naught's flip frames on the knob,
   blueprint's off-scale BREAK flag.

---

## FORTY-EIGHTH PASS — the COMPONENT CONTRACT, increment 1 (slider · bar)

**What this pass is.** The first increment of the component-contract track. The approved philosophy:
**contract first, ONE reference implementation, per-language refinement later as cheap opt-ins.**
Not ten hand-drawn sliders — one contract that all ten languages inherit working, and a place for
each to say the only thing a language is allowed to say about a control.

### The contract as shipped (`taskboard/language.py`, module level)

```python
COMPONENT_PARTS = {"slider": ("main", "indicator", "knob"),
                   "bar":    ("main", "indicator")}
STATES = ("default", "focused", "edited", "active", "checked", "disabled")
COMPONENT_STATES = {"slider": ("default", "focused", "edited", "active", "disabled"),
                    "bar":    ("default", "disabled")}
```

Two claims, and they are the whole track:

1. **Parts are universal.** No language may add or remove a part. A language expresses itself in HOW
   each part is drawn, never in WHICH parts exist. Transcribed from LVGL's own decomposition, which
   is the one professional corpus that publishes a control's anatomy as DATA rather than as a picture.
2. **States are DERIVED from parts, not hand-listed.** `component_states(name)` reads the registry:
   a component with a knob takes FOCUSED / EDITED / ACTIVE, one without takes neither. This is the
   contract's sharpest edge and it is the reason `bar`'s state set is two entries long —
   **a bar is not "a slider we chose not to make focusable"; it has no knob, so it has no affordance
   of control, so those states do not exist for it.** One seat, and it is the parts registry.
   *(This is the one interpretation call in the pass: the brief listed four meaningful states for
   "slider/bar" together. Deriving them instead makes the registry self-consistent and gave the
   suite a control that a hand-written table could not pass — see below.)*

**EDITED is why this axis matters here.** LVGL defines it — "focused AND the arrow keys now mutate
the value rather than move focus" — and the touch corpus styles it **0 times out of 1848**, because
on a touch surface it never happens. On a keyboard surface it is the normal case, so on this board it
is a first-class state with a non-colour render in all ten languages.

**The value model is one function**, `value_pos(val, lo, hi, cells)`, shared by both components and
every language. `lo > hi` is an inverted scale (LVGL's `_invert`) and takes **no branch**: the span
goes negative and the fraction runs the other way. `value_at` is its inverse; the round trip that is
exact is position → value → position, and the suite says so in those words rather than claiming the
other direction (which quantizes).

**The renderer is one seat too.** `Kit.component_cells(name, …)` returns `[(part, glyph, tone)]` —
one entry per slot, **tagged with the part it belongs to**. That tagging is what lets the acceptance
check read a part's extent off the render itself instead of recomputing the width arithmetic inside
the oracle, which is the duplicated-render defect that cost pass 46 a hundred and fifty-eight false
mismatches. Bodmer T4 holds by construction: the whole region including its ground is composed here
and assigned once, never cleared and redrawn.

**NAME COLLISION, said out loud.** `Kit.bar()` was already the agenda/gantt/lanes quantity SPAN — a
run of `span` cells, no value, no scale, ten overrides, two view call sites. The registry keeps
LVGL's name `bar`; the method that draws it is **`readbar()`**. One object, two names. The gallery
row for the old one is relabelled `span`.

### Seat verdicts — nine of ten sliders violated the contract

Every language had an ad-hoc `slider()`. They were read, judged against the contract, and replaced by
a `PART_GLYPHS` table each (plus a `part_tone` or `value_label` override where the language had a real
mechanism to keep). **The contract won every conflict.** Verdicts:

| language | verdict on the shipped slider | what it became |
|---|---|---|
| **nord** (base) | CONFORMS — three parts, all shape-distinct | the reference table |
| **naught** | **two defects.** The knob was the lit dot in a *brighter grey* — a colour-only knob — and **at value 0 there was no knob on the screen at all** | knob is a round dot with an EYE (`◉ ◍ ◎ ● ◌`), present at every value |
| **corgi** | **no knob** (a filled run of `▄▄` and nothing to grab) and passed-vs-remaining separated by **hue alone** | segment HEIGHT carries the reading (`▁▁` track, `▄▄` fill, `██` knob), the numbered readout kept |
| **instrument** | **no knob** — a bar wearing a slider's name | braille knob (`⡇ ⢸ ⠿ ⣤ ⠄`) on the `⣿`/`⠒` register |
| **swiss** | **no indicator** — the same `─` on both sides of the knob | weight is the mechanism: `━` passed, `─` remaining |
| **industrial** | **no knob**; a filled run inside brackets | brackets kept as chrome, ASCII knob (`\| I X # x`) in the family of its `[X]` switch |
| **darkside** | **no indicator**, declared in a comment as "POSITION-ONLY, no fill" | a part is not a language's to renounce: grey STEP `▬` as the indicator. KMBlue still reaches only the knob |
| **ledger** | indicator separated from track by **hue alone** (leader dots in two greys) | ruled `─` for the measured extent, leaders `·` for the unmeasured, tally `▪` for the mark |
| **solari** | **no indicator** (same `·` both sides) | the indicator is the row of flaps ALREADY TURNED (`▁`), never a filled length — its "digits, never bars" law kept |
| **blueprint** | CONFORMS in spirit — the moving `┤` really was a knob | opening `├` becomes chrome, `─` the extension, `┤` the knob; four terminator states |

**The two languages whose accent law contradicted the base tone rule were surfaced, not averaged.**
Base: the knob is `ink` at rest and `accent` only under interaction (naught's red ration). Darkside
and solari declare the opposite — "the knob IS the interaction" — so each carries a four-line
`part_tone` override. Both languages' existing accent-ration checks stayed green, which is how the
conflict was settled: by their own tests.

### The live seats

* **Config screen** (`c`): the state axis is wired to what is actually true of a row. `[`/`]` mutate
  the SELECTED row's threshold, so a selected slider renders **EDITED** — not merely focused, and
  that is LVGL's definition. A signal switched off owns a value nothing can reach: **DISABLED**.
  Honest limit: this screen has no FOCUSED-without-EDITED seat, because focus here always arms the
  value. That state lives in the gallery.
* **Gallery** (`g`): slider's five states and bar's two, **one state per row** so the knob column
  lines up. Side by side was tried first and WRAPPED at the box's 52 columns — measured on the
  composited frame in all ten languages, not assumed.
* **`t` tooltip**: item #24, now derived from `themes.ORDER`.

### Verification — `verify_language.py` 2178 → **2529** (+351)

Registry laws · value-model laws (ends, clamping, inversion, exact round trip, monotonicity, zero
span) · one-seat greps paired with their negative controls · and per language: part completeness,
"exactly one knob at every value including the ends", "the bar has none", "bar == slider minus the
knob cell for cell", knob-vs-fill and fill-vs-track shape distinctness in every state, mechanism
invariance (0.25 → 0.75 touches only indicator and knob cells), the five states pairwise distinct
**after colour is stripped**, EDITED ≠ FOCUSED called out by name, DISABLED shape-marked AND dimmed,
one-width-across-every-state, the knob landing where the shared model says at every cell, the same on
an inverted scale, and the single-write contiguous region.

**Controls, and they are the point.** Six laws were driven RED on purpose:
a colour-only knob table (state law), a two-cell knob (anti-jiggle), hand-built cells with a moved
track cell *and* a moved indicator cell (the invariance predicate reports one and stays silent on the
other), a bar given a knob in the registry, and two probe components proving the state set is derived.
Then four real mutations were injected into `language.py` and each went red where it should:

| mutation | result |
|---|---|
| swiss's EDITED knob collapsed onto FOCUSED | 2 FAIL — the pairwise law and the EDITED≠FOCUSED law |
| `value_pos` loses its inversion (`max(1e-9, hi-lo)`) | 19 FAIL across the value-model block |
| `bar` given a knob in the registry | 35 FAIL — three bar laws x ten languages, plus both derivation controls and the leak guard |
| ledger's indicator collapsed onto its track | **initially 0 FAIL — a real gap in the harness** |

That last one **found a missing law**: nothing checked that the indicator differs in SHAPE from the
track, which is the two-channel law one cell in and is exactly what three languages were shipping.
The law was added (`the <state> indicator differs in SHAPE from the track`, 5 per language) and the
mutation then produced 4 FAIL. *A mutation test that finds nothing has told you nothing; this one
earned its run.*

### Open, and honest

* **Reachability, said plainly:** the gallery box **scrolls** (it has since pass 41). For the
  tall-wordmark languages the component rows sit below the fold at 30 rows and are reached by
  scrolling. This pass added 6 rows to that box. Not a defect, but the next component to land will
  make it one — the gallery wants a tier or a second column before switch + button arrive.
* `test_win_clipboard_roundtrip` failed in one intermediate run and passed in the final three. It is
  item #22 — the Windows clipboard was busy — and it touches nothing this pass changed.
* The **gauge** (`gauge()`) is the slider's read-only twin and still carries its own copy of the
  value arithmetic. It was left alone deliberately: it is a data-viz primitive with its own shipped
  laws, and folding it onto `value_pos` is its own increment.

### Next

1. **`switch` into the registry** — `("main", "knob")` plus CHECKED, which is the first component to
   exercise the `CHECKABLE` seat the registry already carries and the first to test that the state
   derivation generalises past the value family.
2. Then button / text field / checkbox / stepper / scroll bar (item #1), each as a registry entry
   and a per-language glyph table, never a per-language method.
3. **Per-language refinements as opt-ins**, in priority order by how much of the language they carry:
   corgi's LCD ghosting, solari's flap TURN as knob motion, naught's flip frames on the knob,
   blueprint's off-scale BREAK flag on a clipped slider. None of these are owed; all are cheap.

---

Ordered by value. **Item 0 is new, it is the user's own verdict on the work, and it supersedes the
framing of items 1 and 2.** Everything below item 0 is carried over from the previous session.

> **HISTORICAL FROM HERE DOWN (2026-07-27).** The closing state block above is the authority on what
> is open. Read what follows for diagnoses, not for status.

Read this file with `HANDOFF.md` (the brief, the traps, the ADD-don't-replace plan). Where the two
disagree about the *shape* of the density problem, this file is the measured one.

---

## 0. THE LANGUAGE AXIS IS NOT IMPLEMENTED — it is a palette swap  [user verdict, 2026-07-25]

> **RESOLVED 2026-07-26.** The axis is now real code: `taskboard/language.py` defines a structure
> KIT per language (8 kits — head, card, tile, meter, agenda/gantt/lanes bars, section headers,
> calendar cells, queue markers, focus-chrome CSS). Every surface listed below as theme-invariant
> now renders through the active kit. `frame`, `numbered`, `dot_w` are wired and dispatched
> (`meter` picks the quantity MECHANISM from `language.METERS`; `sel` styles the focus border);
> `hero_gap` was deleted. The acceptance test demanded below exists and passes:
> `prototypes/verify_language.py` — 121 checks: greyscale pair test (all 28 pairs, kit level AND
> app level with the hero region MASKED), plus mutation of every structural token each language
> declares. All four suites green: 137 pytest · verify_widget · verify_board · verify_language.
> The audit table and text below are kept as the historical record of the defect.

> "Los temas o lenguajes de diseño se sienten todavía como cambio de paleta de colores únicamente.
> Sólo modificas el número que se presenta de frente pero es lo único que hace un cambio y es
> decepcionante."

**This is correct, and it is mechanically provable.** `themes.py:3` promises each entry is "a full
commitment (tui-design/LANGUAGES.md), **not a recolour**". The code does not keep that promise.

**Token audit — which non-colour tokens the code actually reads:**

| token | read? | where |
|---|---|---|
| `hero` | yes | `app.py:93` — Hero widget only |
| `base` | yes | `app.py:192, 220, 232` — Hero numeral only |
| `meter` | yes | `app.py:292` — one call site |
| `airy` | yes | `app.py:204` — inside the Hero |
| `border` | yes | `themes.py:118`, one TCSS `#hero:focus` rule |
| **`frame`** | **NEVER** | `app.py:218` reads `hero`, not `frame`. Dead. |
| **`numbered`** | **NEVER** | dead |
| **`dot_w`** | **NEVER** | hardcoded literals `dot_w=2` / `dot_w=1` at `app.py:164, 182` |
| **`hero_gap`** | **NEVER** | dead |

**Every live structural token is consumed inside the Hero widget.** Cards, column heads, agenda,
gantt, swimlanes, footer and chrome render **identically across all eight languages**; only the
palette substitutes. Switching language changes the hero numeral's pixel base and the colours. That
is the entire effect.

Corroborating measurement: at height 12, `industrial` and `swiss` produce **identical ink fractions
in all three size classes** (34.4 / 23.1 / 24.2) despite being defined as opposite languages — airy
Swiss with one hairline rule versus flat functional industrial. Not proof on its own (they diverge at
height 26), but it is the signature of two languages rendering the same layout.

**What fixing this actually requires** — not a patch:

- Every widget that draws (cards, column heads, meters, agenda bars, gantt bars, footer) must take
  the active language's tokens and change **structure**, not just colour: pitch, frame treatment,
  label mechanism, meter mechanism, whether labels are drawn or cell text.
- `frame`, `numbered`, `dot_w`, `hero_gap` must be **wired or deleted**. `LANGUAGES.md`'s own added
  rule says a language definition is code, not a manifest. Right now it is a manifest.
- The acceptance test is not a screenshot. It is: **mutate one language's structural tokens and
  assert the rendered strips change outside the hero region.** If they do not, the axis is still
  fake. No such test exists today.

**Item 1 (density) and item 2 (Naught's lattice) are symptoms of this, not peers of it.** Item 2 says
"Naught applies its language to the hero and falls back to plain cell text everywhere else" — that is
true of *all eight*, not just Naught.

---

## A. Prototype / app

1. **Ink-fraction floor — the previous framing was wrong. Re-measured.**

   PENDING previously claimed "`nord` (20%) and `instrument` (22%) fail the floor", implying only two
   languages failed. **Measured with `prototypes/verify_ink.py` (new, self-checking):**

   | height | naught | corgi | swiss | industrial | phosphor | bbs | instrument | nord |
   |---|---|---|---|---|---|---|---|---|
   | **h=12, glance** | 55.4% | 45.0% | 34.4% | 34.4% | 32.9% | 32.3% | 29.2% | **22.5%** |
   | **h=26, glance** | 29.4% | 24.6% | 19.5% | 15.9% | 19.0% | 18.8% | 17.3% | **14.2%** |

   Three corrections to the record:

   - **At h=26 all 8 languages fail the 35% glance floor**, including `naught` and `corgi`, which the
     previous note credited with "the density treatment". At h=12, 6 of 8 fail.
   - **Screen height dominates the result and no one fixed it.** A 35% floor is unfalsifiable until
     `DENSITY.md` states the geometry it is measured at. This is a gap in the skill, not only in the app.
   - **The old numbers were the wrong size class.** "nord 20%, instrument 22%" matches neither glance
     column but sits almost exactly on the *widget* column at h=26 (21.9%, 24.0%). The previous
     session most likely measured the widget class and labelled it glance.

   **Unresolved:** run-to-run variance of several points on the board class (`naught` gave 38.0% and
   44.2% at one geometry). Animation phase is the suspicion; **it was not verified.** Pin this before
   treating any of these numbers as an acceptance threshold.

2. **Naught quantization — DONE 2026-07-26 (eighth pass closed the card half).** Column-head counts
   are drawn 3x5 sprites (`naught.label()`), agenda bars are lit-dot rows, card markers are lattice
   dots with dot leaders, calendar cells are lattice dots. Cards now have a second row ON the
   lattice: phase progress as lit dots + the state as naught's 2-dot icon. The literal 3x5 sprite
   still needs 5 rows and therefore does NOT fit a 2-row card — the dot meter is the honest 2-row
   form; rendering the sprite through braille would fork the pixel base (decided against).

3. **The hero's dead columns — DONE 2026-07-26 (seventh pass).** At board size the hero now carries
   the 8-week load plot in its dead columns, drawn per-language via `Kit.plot` (meter family), with
   the caption inside the visible row band (short heroes grow empty rows first — industrial's 4-row
   readout was silently renouncing the plot). Enforced: verify_language "dead columns" checks
   (nord/naught/industrial, deterministic seeded fixture board).

4. **`action_cycle_size` is one-way.** It sets `self.forced` permanently (`app.py:548-553`), leaving
   no route back to automatic width-based sizing — contradicting the module's own "adapts to its own
   width" thesis. Add a fourth `auto` state to the cycle.

5. **Dead tokens — DONE 2026-07-26.** `frame`, `numbered`, `dot_w` wired (read by the kit and the
   hero); `hero_gap` deleted; `meter` now dispatches a real mechanism; `sel` (focus border style)
   added and read by `themes.tcss()`. Enforced by `verify_language.py`'s mutation pass.

6. **Minor — mostly DONE 2026-07-26:** dead `render.py` imports removed from `app.py`; the `t`
   tooltip lists all 8 languages. Still barely used: `bases.wave` (waiting on item 3's sparkline).

## B. The skill — `~/.claude/skills/tui-design/`

7. **No runnable exemplar screen.** Thirteen documents of vocabulary, zero reference implementation.
   The skill's own *"render, don't label"* rule applied to itself demands a ~60-line app showing hero
   + brightness ladder + focus border + curated footer + one `level="basic"` animation. Suggested
   home: `assets/exemplar.py`. **Item 0 raises the bar for this:** the exemplar must demonstrate a
   language changing *structure*, or it will model the same mistake.

8. **`DENSITY.md` does not state the geometry its 35% floor is measured at.** New, from item 1. The
   rule cannot be satisfied or refuted as written.

9. **hex vs Textual theme variables never reconciled.** `PALETTE.md` says design 4-6 hex values;
   `NAVIGATION.md`'s example uses `$accent`. Nothing states when tokens should map to Textual's theme
   system versus hardcoded hex — an agent following `PALETTE.md` literally fights the framework.

10. **`SKILL.md.bak`** is a stale leftover in the skill directory. Pre-dates this work. Delete if unwanted.

## C. Elsewhere

11. **`/html-visualizer` was never refined.** Deferred in the first message of that session ("dejemos
    eso para cuando terminemos con TUIs") and the TUI work never ended. Owed the same treatment
    `tui-design` received: an intake step, measured claims, a verification discipline, reusable
    assets. **The largest single outstanding item — scope it as its own batch, not an increment.**

12. **`RUN.md` — DONE.** Its `## Checks` section used to point at dead paths under a
    deleted job tmp directory. It now points at `prototypes/verify_widget.py`,
    `verify_board.py` and the new `verify_ink.py`, and it must document that Windows needs
    `$env:PYTHONIOENCODING = "utf-8"` in PowerShell or the verify scripts die with
    `UnicodeEncodeError` before printing a verdict. **Fixed 2026-07-25:** now points at the three verify scripts and documents the PowerShell encoding requirement.

13. **Orphaned `clipboard-fix/` directory** in `<repo>/.claude/worktrees/` — not registered in
    `git worktree list`, left by an earlier session. Not ours; left untouched.

---

## State of the work

**Open items owed after the twenty-second pass (naught's `layout="lattice"`), in the order
they should be taken:**

0. **Roll `layout` out to the remaining languages — DONE 2026-07-27 (thirty-second pass).
   Coverage is 8 of 8**: darkside `rail` · ledger `ruled` · naught `lattice` · industrial
   `panel` · swiss `editorial` · nord `split` · instrument `trace` · **corgi `strip`**.
   Every language's board composition is now its own token, and no language takes the base
   default `flow` any more. See the thirty-second-pass entry for what corgi's costs.
0e. **nord's law-03 HERO defect — DONE 2026-07-27 (thirty-ninth pass). CLOSED at the SHIPPED
   seat.** The split cured the BOARD; the panel above it had no fixation of its own — the
   8-week load chart out-inked and out-shone the headline numeral, which the row budget was
   also CLIPPING. Cured in `taskboard/hero.py` + two nord tokens: the figure is drawn to FIT
   (`hero_fit`) and the load drops to an ambient one-row spark (`hero_plot`). **One residual,
   named: the widget-slice PROTOTYPE forks `Hero.show` and is not cured** — see the entry.
0b. **naught's `hero="naught7"`** — **DONE 2026-07-27 (twenty-third pass)**, see below. Declared,
   dispatched and mutation-tested. Read the entry's *reachability* paragraph before assuming the
   user can see it: the drawn caption tier needs 13 hero rows and no composition gives more than 11.
0c. **naught's `motion="bloom"`** — out of scope this pass; not declared for the same reason.
0d. **naught's head-count sprites take the STROKE** — **DONE 2026-07-27 (twenty-fourth pass)**,
   see below. This was the user's actual defect: the drawn letters they called "hard to read,
   somewhat separated" are the BOARD's head counts, not the hero's. Cured at the head and at
   `sect()`; the wordmark is the one drawn seat still sparse (it takes no width argument).
1. **The slab HERO for ledger — DONE 2026-07-27 (thirty-sixth pass), together with solari's
   `flap`.** Both are real pixel BASES in `bases.py` reached through `hero="dot"`, not new hero
   branches. See that entry for what renders where and for the one cost (ledger's caption at the
   board seat). **Blueprint's `stencil` — DONE 2026-07-27 (thirty-seventh pass), the same way.
   THE DISPLAY-TYPE AXIS IS CLOSED AT 10 LANGUAGES**: nine draw a hero of their own and swiss's
   `plain` is a deliberate renunciation, not a placeholder.
2. **The darkside capture race — DONE 2026-07-27 (forty-sixth pass). WATCH CLOSED.** The
   evidence dump fired and named it: not a fixture race, not a scroll, not a rebuild — a
   **stale-width card bake that `settle()` signed off on**. `TaskCard.render_card` falls back
   to a 20-cell seat before its first layout, baking an 18-cell row that is INK (so settle's
   condition A passed) and static (so condition B passed). Cured harness-side with settle
   condition C, a non-mutating shadow render. Reproduced 17/30 amplified, 0/30 after. See that
   entry.
3. **`aperture._queue_markup` overflows its panel by one cell — DONE 2026-07-27 (forty-fifth
   pass). CLOSED.** The row was built as `marker + 1 + (w - 8) + 5`, which closes on `w` only
   for a 2-cell marker; corgi and industrial draw `[1]` and spent `w + 1` at every width.
   Cured at the source: the marker is MEASURED (`hero.vis_w`), the widest one in the batch sets
   the column, and the title takes what is left. Held by a compositor law over all ten
   languages plus a pre-cure control. See that entry.
4. **`kanban.py`'s section-head width — DONE 2026-07-27 (forty-third pass). CLOSED.** The head
   was handed `avail - 4` while a card sized itself from its own content box, so the two
   surfaces were measured apart and six languages carried a private compensation for the
   one-cell lie. Cured at the source: `kanban.py.row_width` is the board's ONE measure and
   `.col-head`/`.kb-empty { padding-left: 1 }` (base kit tcss) is its one origin. Six
   workarounds retired, the bounded `<=1` / `<=2` checks are now EXACT agreement, and two
   mutation-proven app-level laws hold it. See that entry.
5. **Ledger's `motion="leader"`** (leaders drawn in, left to right, as a row is posted) — out
   of scope this pass, and cheap: it is precomputed frame motion.
6. **A `reflow` token** (the page choosing between renouncing a column and shrinking it) — out
   of scope; `cols()` currently hardcodes the renunciation order.
7. **The empty state's seat in the SECTIONS layout — DONE 2026-07-27 (thirty-eighth pass).
   CLOSED.** All three branches of `KanbanBoard.build()` now mount `k.empty()`, and the six
   sections languages (corgi · swiss · darkside · ledger · solari · blueprint) show the
   language's own voice on an empty phase instead of nothing. See that entry for the two
   findings it produced (the mascot split, and the double-`grey()` defect the render caught).

## State of the work — SESSION CLOSED 2026-07-26 (user: "está bien por ahora")

**Where this stands after 17 passes.** SEVEN living languages (naught · corgi · instrument ·
swiss · industrial · nord · darkside — phosphor/bbs retired by curation, darkside and naught the
user's favourites, instrument the polish benchmark). The language axis is REAL code end to end:
structure kits with components, identity, motion, composition, display type, card anatomy and
three data-viz primitives (spark/plot/gauge, shared-hi + reflow + microbar laws); per-posture
composition with sections boards for darkside/swiss; geometry-based lateral nav. **The aperture
runs in the REAL app behind the `6` key** (launcher; full per-language TCSS; views.py untouched).
Suites at close, all green: verify_language **356** · verify_aperture **16** · verify_widget ·
verify_board · pytest **137/137**. Skill: COMPONENTS.md (inventory + DATAVIZ pointer) +
DATAVIZ.md (the laws) written. Nothing committed, all local in this worktree.

**Owed to a next session (code folds, deliberately not rushed at closure):** ~~fold the prototype
Hero's drawing onto `taskboard/hero.py` (duplicated today)~~ **DONE, forty-fourth pass**; gallery could demo `plot` variants;
input components from the COMPONENTS.md inventory (button, text field, checkbox, stepper, scroll
bar); scatter/line as braille fields; a skipif/mock for `test_win_clipboard_roundtrip`; retire
`verify_ink`'s variance question (PENDING item 1); the darkside capture-race watch; Kimi
still-adoptables (mode-switch by measured demand via `plain_width`, mascot height-pair check).

**Done 2026-07-27 (forty-sixth pass) — THE DARKSIDE CAPTURE RACE IS DIAGNOSED AND CURED. WATCH
CLOSED.** The suite's last open watch, ~1 full-suite run in 12 since pass 17, four failing checks
every time and never once reproduced in isolation (0/12 at pass 21, 0/30 since). One file:
`prototypes/verify_language.py`. **The app was never wrong** — the harness was reading a frame the
app had not finished composing, and pass 30's evidence dump is what finally said so.

**What the dump showed.** `_race_darkside.txt`, written the moment the probe self-check trips.
The failing frame is **118×30 — the right size, the right fixture, the right theme, the right
section, the right card count, the rail present and on one column**. Diffed against a healthy
`capture("darkside", fx)` it is **25 of 30 rows identical**. The five that differ are one signal
counter (a file count, expected to drift) and the four card TITLE rows:

    EVIDENCE |   ▏  shut down … 8d
    HEALTHY  |   ▏  shut down legacy servers                              8d

That forks the tree immediately and kills all three standing suspects. Not a wrong board (the
fixture is right), not a scrolled-away card (the card is on screen, at the right row), not an
empty sections list (all four sections and all their cards are there). The cards are simply drawn
**narrow** — and the card SUBTITLE rows (`backlog · d3`) are byte-identical to the healthy frame,
because they are short enough not to notice the width.

**The mechanism, pinned to a single integer.** `kanban.py.render_card` opens with

    w = max(8, (self.size.width or 20) - 2)

Feeding the darkside kit every width from 8 to 40 shows `renew tls … 3d` is produced at **w=18 and
at no other width**. And `w == 18` has exactly one preimage: `self.size.width == 0`, the
un-laid-out widget taking its 20-cell fallback. So the failing frame is a card that painted
**before its first layout** and was still holding that paint when the capture read the screen.
Logging every `render_card` call confirms the life cycle: the live cards go `0 → 112 → 112 → 111`,
and **the corrective renders land during `settle()`**, not before it.

**Why `settle()` could not see it — the real defect.** Settle's two conditions are (A) every board
content widget the compositor draws has painted pixels in its clipped area, and (B) the frame is
identical on two consecutive reads. An 18-cell bake **satisfies both**: it is ink, so A is happy,
and the frame is genuinely static in the gap before the re-render, so B is happy. Settle did not
time out on these runs — **it succeeded, on the wrong frame.** That is exactly consistent with
pass 30's positive exclusion (healthy headroom, worst 4 of 40, no timeout when the race fired),
which had been read as evidence AGAINST a paint problem and was in fact the signature of one.

**Amplified, with a control, before anything was changed.** The hypothesis "the corrective render
is late and settle signs off first" was amplified by deferring every nonzero-width `render_card`
by 50 ms and leaving the width-0 bake on time — the mechanism, nothing else:

    corrective render on time (control)   30 captures    0 illegible
    corrective render 50 ms late          30 captures   17 illegible  (all 18-cell)

and the amplified failure frame is **byte-identical to the saved evidence dump on the card rows**.
Mechanism proven, not guessed.

**The cure is harness-side, because the harness is what is wrong.** The app corrects itself within
a beat and a human never sees the narrow frame; the app does not lose the card (that was pass 31,
a different bug). So `settle()` gained a third condition rather than `kanban.py` gaining a
workaround:

  C. every drawn `TaskCard`'s paint must have been composed at the seat it currently HAS.

Asked as a **shadow render** (`_stale_paint`): the card is asked what it would draw now with
`update` intercepted into a list, so the answer is collected and never applied. This **measures
and does not repair** — a settle that silently re-rendered the board would mask the very class of
bug it exists to catch, and would have turned this watch into a green lie. No magic numbers, no
duplicated render logic, no per-language special case.

**The oracle was validated in both directions before it shipped**, because a settle condition that
can't fail is worse than none:

    settled state, 10 languages × {118, 80, 60}   false positives   0
    amplified narrow frames                        missed            0  (caught 2/2)

An exact `content width == row_width` rule was tried first and **rejected**: the kits pad
differently (naught −1, corgi −2, industrial −3, swiss and blueprint not at all), so it produced
158 false mismatches in a perfectly settled state. The shadow render needs no such assumption.

**Proof of the cure.**

    amplified probe (50 ms late), cured settle    30 captures    0 illegible, 0 timeouts
    control (0 ms), cured settle                  30 captures    0 illegible
    full verify_language, back to back            12 runs        2178/2178, FAIL=0, rc=0 every run
                                                                 no `_race_darkside.txt` written

Settle headroom is unchanged at **worst 4-5 of 40 over 137 captures**, so condition C costs no
extra iterations in the settled case; run time held at 75-78 s. **No check was weakened or
removed** — the state count is exactly 2178, the same as before the pass. The only other edit is
the timeout detail string, now `not settled:` instead of `unpainted:`, since the list can name a
stale card as well as a blank one.

**Bounded budgets spent, as required by a race hunt:** 30-rep amplification, 30-rep control,
30-rep cured amplification, 30-rep cured control, 10 languages × 3 widths for the oracle
validation, and 12 full-suite runs. No unbounded loops.

**The trap worth keeping.** *A settle condition that only asks "is there ink, and is it still"
cannot tell a finished frame from a frame composed against the wrong geometry.* Both of this
suite's settle bugs are that same shape — pass 29's blank detail pane failed A, this one passed
A and B while being wrong. The general form of the question is not "has it painted" but "is what
is painted what this widget would paint right now".

**Done 2026-07-27 (forty-fifth pass) — THE LAST TWO SHIPPED-SEAT GEOMETRY DEFECTS. BOTH CLOSED.**
Pass 44's finding (the hero renounces a plot row) and PENDING item 3 (the queue overflows its
panel), taken together because they are the same mistake pointing in opposite directions: **a
region built against a budget that is not the one it stands in.** One renounced a cell, the other
stole one. Three files: `taskboard/hero.py`, `taskboard/aperture.py`, `prototypes/verify_aperture.py`.

**(A) THE TRIM ORDER WAS NEVER THE CAUSE — say this first, because pass 44 named the wrong
mechanism and the next reader will otherwise re-diagnose it.** Pass 44 read the defect as
`draw()` trimming VISUAL rows *before* `_beside_plot` joins the load, and prescribed moving the
trim after the join. **Moving it would have been a no-op**: `_beside_plot` never returns more rows
than it is given (it pads only up to `min(7, max_rows)`), so the join already sees the panel's
post-trim height. The defect is one line of the join's own arithmetic:

```python
ph = min(7, len(rows) - 1)        # the caption's row, reserved
prows = kit.plot(series, plot_w, ph - 1)
prows.append(PLOT_CAP)            # ... and reserved AGAIN
```

The band is data rows **plus** its caption and both stand in rows the panel already has, so
`ph = min(7, len(rows))`. 7 is the band's own cap, not a budget. The trim site now carries the
no-op proof in a comment so the order is not "fixed" by a future pass.

**THE DIFF SCOPE — pre/post shipped-aperture dumps for all ten languages at 118x34**
(`prototypes/out/_p45_pre.txt`, `_p45_post.txt`; guarded fixture, `settle`, hero AND panel regions
sliced off the compositor, plus each language's queue rows as BUILT so an overflow is visible
before the compositor clips it):

| language | hero | queue | why |
|---|---|---|---|
| **industrial** | **MOVED** | **MOVED** | the ONLY hero mover: a `plain` hero of 4 rows padded to 7, so the old `min(7, 6)` band drew **5 data rows + caption and left row 6 blank**. Now 6 + caption, closing on the panel's last row. Its `[1]` marker also overflowed: 116 in a 115-cell panel |
| **corgi** | identical | **MOVED** | the other 3-cell marker: **114 in a 113-cell panel**, pass 21's 93-in-92 at this width. Its hero is 9 rows, so the band was already at its 7-row cap |
| naught, instrument, swiss, nord, darkside | identical | **MOVED** | 1-cell markers: the row was one cell SHORT of its measure and now closes on it exactly (the title column gains the cell, the chip moves one right) |
| ledger, solari, blueprint | identical | identical | byte-identical — 2-cell markers, which is exactly the width the old `- 8` assumed (ledger cut its folio to two cells *because* of this defect) |

**The drawn figures did not move anywhere.** industrial's numeral, label and detail rows are
byte-identical pre/post; what changed is the load column re-quantising the same series over 6 rows
instead of 5. naught/instrument/ledger — the three pass 44 predicted would move — did **not**: at
the shipped seat `max_rows = 9`, so their band was already at the cap. Pass 44's movers were the
PROTOTYPE's (7 content rows); the shipped seat's mover is industrial. darkside draws no
dead-columns plot at all here — its centred 46-cell column is under `draw()`'s 72-cell threshold —
and that is now asserted rather than skipped.

**(B) THE QUEUE ROW IS ONE MEASURE**, the same move as pass 43's `row_width`. `queue_marker` is
MARKUP and its width is per language (1, 2 or 3 visible cells), so the row measures it:

```python
mw = max(vis_w(marker) for each row)          # the widest in the batch sets the column
tw = max(1, w - mw - QUEUE_GAP - QUEUE_CHIP)  # ... and the title takes what is left
```

`QUEUE_GAP = 1` / `QUEUE_CHIP = 5` name the two fixed columns that `- 8` had spelled into a format
string. The widest marker sets the column **for every row** (each marker is padded to it) — a
per-row budget would fit and then stagger the chips. `hero._vis_w` became **`hero.vis_w`**, public,
because it is now the one measure for anything closing on a panel edge; it was internal to
`hero.py` and has no other callers.

**THE TWO NEW LAWS — `verify_aperture.py` 112 → 151 checks (+39, nothing shrank, nothing renamed).**
No existing check moved: the cures change row CONTENT, never row COUNT, so the hero's `<= 12` wrap
budget and every legend/launcher law are untouched. The arithmetic: **11** for the load band
(9 languages measured + darkside's asserted absence + a non-vacuity guard), **4** for its control,
**21** for the queue (10 x {the panel really drew a queue, no row exceeds its measure} + one global
exact-fit), **3** for its control.

- *the load band renounces no row of its panel* — measured on the composited `#hero` region: the
  band is at its 7-row cap **or** every row under the caption is used. Stated as the defect, not as
  the formula, so a panel that grows a row cannot pass by re-deriving the same mistake. nord's
  ambient one-row spark answers a different law (it must ride the hero's LAST drawn row).
- *every queue row closes inside the panel it stands in* — `len(row.rstrip()) <= region.width - 1`
  (what `redraw`'s `wof()` actually hands the queue), per language, plus one global check that they
  close on it **exactly**: a row one cell short is the same missed measurement as a row one cell
  over, pointing the other way.

**BOTH LAWS HAVE A CONTROL THAT SHOWS THEM FAILING**, because a law nobody has seen fail is a law
nobody has tested:

- **A, live mutation in-suite:** the old join is re-installed over `HERO._beside_plot`, industrial
  is re-rendered, and the suite asserts the band collapses to **6 of 7 rows with the bottom row
  blank** — then restores the cure and asserts the panel comes back. Output: `MUTATION: with the
  old join back, industrial's bottom panel row goes blank again and the law FAILS  band 6 of 7`.
- **B, in-suite:** the old row form is rebuilt against corgi's *real* measured panel and asserted to
  overflow — `the OLD row arithmetic overflows this very panel by a cell  114 in 113`.
- **B, throwaway whole-file control** (`prototypes/out/_p45_aperture_precure.py`, the cured file
  with only `_queue_markup` reverted; swapped in, run, swapped back, `diff` verified IDENTICAL):
  the new suite goes **4 FAILURES** — corgi `over: [(1,114)...(8,114)]` in a 113-cell panel,
  industrial `[(1,116)...(8,116)]` in 115, the exact-fit law naming all seven non-2-cell languages,
  and the cured-row check reading `built [114] against 113`. Log: `_p45_control_precure.log`.

**Runs.** `verify_aperture` 3x back-to-back: **151 / 151 / 151, ALL PASSED** (`_p45_ap_run{1,2,3}.log`).
`verify_language` **2178, ALL PASSED on the first run** — no darkside race this time, and **no check
moved**, which was the pass's stop condition (the prototype hero now folded onto the seat renders
one more plot row only where its panel affords it, and no check pinned the old 5-row band).
`verify_widget` **24**, `verify_board` **22**, `pytest tests` **137 passed**, no clipboard flake.
`flake8` on the three touched files: no new findings (two pre-existing, `hero.py:265 E741` and
`verify_aperture.py:166 E302`).

**Owed, small and named:** `language.py` carries two now-stale comments that say the overflow is
"pre-existing" and "the fix is app-side" — ledger's `queue_marker` (~line 2715) and blueprint's
(~line 3160). Both are true statements about why those markers are two cells wide and both should
now read as history; `language.py` was outside this pass's four-file set.

**Open after this pass:** `HERO_FONT` still has no metrics table of its own (pass 36's item 3);
the hero is still a small mark in a wide field (pass 36's item 5); the two stale comments above.

**Done 2026-07-27 (forty-fourth pass) — THE HERO FORK IS FOLDED. ONE DRAWING SEAT, EVERYWHERE.**
The oldest structural debt on this board, owed since pass 13 and re-flagged in 35, 36 and 39:
`prototypes/widget_slice/app.py` carried its own copy of the hero drawing. `Hero.show` is now a
**nine-line adapter** — it gathers the widget's real width and height, calls
`taskboard.hero.draw()`, places the result, and keeps the severity flash, which is the one thing
that belongs to a widget and not to a renderer. 207 lines of forked drawing deleted, and with them
the `render._GLYPHS` / `naught` / `bases` / `re` imports the fork needed.

**THE FOUR DRIFTS THE FORK HAD ACCUMULATED, and what the fold did to each:**

| # | drift | owed since | cured how |
|---|---|---|---|
| a | the `4 * sx` caption wrap — metrics-blind, deleted from the seat in pass 35 | 35, item 3 | the seat's `_wrap` measures through `NA.plain_width` |
| b | its own `naught7` dispatch (a second copy of the branch) | 23 | one branch, in `hero.py` |
| c | the `dot` branch drew flap FIGURES and never called `flap_paint` — solari's card faces unlit | 36, finding 1 | the seat paints them |
| d | it read neither `hero_plot` nor `hero_fit`, so the prototype's nord panel still had the pass-28 fixation defect | 39, residual | the seat reads them |

**(a) was latent, not theoretical, and it is worth recording exactly.** The alphabet's advances went
per-glyph in pass 35 (a digit steps 5 columns where a letter steps 4), so `4 * sx` under-measures
any caption with a digit in it. Measured against the fork's arithmetic verbatim: at `sx=2`, w=118,
`"12 DAYS OVERDUE"` — the fork drew it as ONE band that `plain_width` measures at **122 cells inside
a 118-cell hero**, which is the hero's oldest trap (a frame built wider than its widget wraps, and
every line doubles). Today's captions are letters-only, so it never fired. It cannot now.

**THE DIFF SCOPE — pre/post prototype hero dumps for all ten languages** (`prototypes/out/_p44_pre.txt`,
`_p44_post.txt`, guarded fixture + settle, board render captured alongside):

| language | hero | board | why |
|---|---|---|---|
| nord | **MOVED** | identical | the pass-39 cure lands: `hero_fit (5,2)` gives a 10x7 fitted numeral where a clipped 11-row quadrant figure stood, and the 6-row accent chart becomes a **one-row `mut` spark** (`█▅▂`) beside `LOAD · 8 WK` |
| naught, instrument, ledger | **MOVED** | identical | the visual-row trim (see the finding below) — the load band loses its bottom data row |
| solari | identical *(text)* | identical | the faces are a COLOUR channel: the hinge band `seam` `#1f1f22` now appears in the hero region and leaves with `flap_paint`, measured on the compositor |
| corgi, swiss, industrial, darkside, blueprint | identical | identical | byte-identical, as required |

**A FINDING, and it is a red I am NOT fixing in this pass — say it loudly.** **[CLOSED, forty-fifth
pass — but the mechanism named below is WRONG: the trim order was a red herring and moving it would
have been a no-op. The defect was the join's own double-reserved caption row. Read the forty-fifth
entry, not this paragraph.]** `hero.draw` trims to
`max_rows` VISUAL rows **before** `_beside_plot` joins the load; the fork trimmed list ENTRIES,
which is a no-op when entry 0 is a seven-row block, so the plot saw the untrimmed row count. Net
effect at a 7-row hero: `ph = min(7, len(rows) - 1)` falls from 7 to 6, so the load band renders
**5 data rows + caption instead of 6 + caption** and the hero's bottom visible row goes empty. That
is what naught, instrument and ledger moved by. **It is the SHIPPED seat's behaviour** — the
prototype now matches `aperture.py` rather than diverging from it, which is the fold working — but
the shipped seat is renouncing one row of its own dead columns and nobody had noticed, because the
only surface that showed the alternative was the fork. Fixing it means moving `hero.py`'s trim
after the join, which moves the shipped aperture's render and its 112 checks: **a pass of its own.**

**A SECOND, SMALLER ONE:** at the prototype's hero geometry (7 content rows) nord's caption
`DAYS OVERDUE` does not fit under the fitted numeral and is trimmed away. That is pre-existing —
the fork lost it too, to clipping — and the shipped aperture (`max_rows = 9`) keeps it. Recorded so
the next reader does not diagnose the fold for it.

**THE ANTI-REGRESSION LAW — `verify_language.py` 2151 → 2178 checks (+27, nothing shrank).**
One check REPLACED in place, same slot: "the widget-slice prototype's HERO is identical with and
without both hero-panel tokens — it forks `Hero.show`" became "... **MOVES** when the hero-panel
tokens are taken away — pass 44 folded it, so the prototype now READS them". Net zero, arithmetic
visible. The 27 new ones:

- **20** — a SOURCE law, ten fork markers (`HERO_FONT`, `draw_numeral`, `seven_seg`, `dense_type`,
  `dense_rule`, `flap_faces`, `_beside_plot`, `"naught7"`, `"corgi"`, `"framed"`) each asserted
  ABSENT from `widget_slice/app.py` **and PRESENT in `taskboard/hero.py`**. The paired control is
  the point: a grep law that passes because the symbol was renamed everywhere is a vacuous law.
- **1** — the prototype's hero CALLS the seat (`HERO.draw(`), so a file that merely stopped drawing
  cannot pass the twenty above.
- **6** — solari's faces on the live prototype frame: the `seam` band is in the hero region, it
  LEAVES when `flap_paint` is neutered (the control — solari's `flap` hex is also the hero widget's
  own TCSS ground, so the face alone cannot discriminate and the hinge band can), the painter
  restores, and ledger/blueprint/nord still paint no face.

`capture_ap_bg`'s docstring, which said the prototype forks the dispatch, was corrected — it is
now the seat that answers for the shipped SURFACE, not for the hero mechanism.

**Runs.** `verify_language` 3× back-to-back: **2178 / 2178** twice, and once the named darkside
race (its exact 4-check signature) which cleared on the single allowed rerun — **2178 green**.
`verify_aperture` **112**, `verify_widget` **24**, `verify_board` **22**, `verify_variants` **12**,
`pytest` **137 passed**. `taskboard/hero.py` and `taskboard/aperture.py` untouched.

**Open after this pass:** ~~the visual-row-trim finding above (the shipped seat renounces one plot
row)~~ **[CLOSED, forty-fifth pass]**; `HERO_FONT` still has no metrics table of its own (pass 36's
item 3, still open); the hero is still a small mark in a wide field (pass 36's item 5).

**Done 2026-07-27 (forty-third pass) — THE HEAD AND ITS CARDS ARE ONE MEASURE. ITEM 4 CLOSED.**
Twenty-two passes carried this: `kanban.py` handed a section head `avail - 4` while a card sized
itself from its own content box, so the two surfaces were **measured apart** and six languages
each grew a private compensation for the same one-cell lie. Cured at the source, in one place.

**THE LAW, stated once in `kanban.py`.** Every surface a phase draws — head, card, empty seat —
stands in the same SEAT (what `width: 1fr` resolves to inside the scrolling list) and must close
on the same cells:

```python
CARD_BOX = 2      # `.kb-card { padding: 0 1 }` — what Textual takes off the seat
CARD_OWN = 2      # ... and what `render_card` takes off `size.width` again

def row_width(seat_w: int) -> int:
    return max(8, seat_w - CARD_BOX - CARD_OWN)
```

The card is the REFERENCE, not an ideal. Measured on the compositor (`_probe43.py`), a card at 118
gets `outer=113 size=111` — **`Widget.size` is already the content box**, and `render_card` then
spends the padding a SECOND time (`size.width - 2`), so a card ROW is 109 cells and starts one
cell in. `CARD_OWN` names that second spend instead of hiding it: 109 is what is on screen and
what every language is drawn against, so it is what the head must be handed too. All three
branches now derive their seat explicitly and call `row_width` on it — sections `avail - 1`,
columns `cw - 2`, split `master_w - 3` (each reserving its scrollbar cell, the safe direction).

**AND ONE ORIGIN**, in `language.py`'s BASE kit tcss: `.col-head { padding-left: 1 }` +
`.kb-empty { padding-left: 1 }`. The head now opens on the card's own left edge for every
language, which is the half of the problem no width number could fix.

**WHY THE OLD RIGHT EDGE LOOKED FINE — arithmetic luck, and it is worth recording.** With a
scrollbar the head drew 110 cells from x and the card drew 109 from x+1: the closing edges met by
coincidence. The day the list does not overflow, the head still gets `avail - 4` (it never knew
about the scrollbar) and the card gets one more — and the edge splits. Ledger's rule did not even
have the luck: it **overshot** the postings' closing rule by one (`3..112` against a closing rule
at `111`), which the suite had bounded at `<=2` and the old note had mis-recorded as "one short".

**Per-language verdicts — removed only what the mismatch FORCED:**

| language | workaround | verdict |
|---|---|---|
| **instrument** | `HEAD_PAD = 1` (origin) + `HEAD_TRIM = 4` (length), two constants for two wrong answers | **BOTH DELETED.** The axis takes its whole measure and is indented by the trace's own `IND`. |
| **industrial** | the legend's leading cell paid in the markup (`" [on plate]…"`, `w - 1`) | **REMOVED.** Its own note said TCSS padding WRAPPED this legend — true only while the head was also handed the wider number; `row_width` leaves it 3 cells of slack. |
| **swiss** | the masthead's leading cell paid in the markup (`" " + …`, `m = w - 1`), plus a leading space on the hairline | **REMOVED.** The masthead sets on the grid's OWN origins now (`hl0.index("B A C") == g105[0][0]`, was `1 + …`). |
| **swiss (grid)** | flush-LEFT placement, chosen because right edges could not agree | **KEPT — now a free choice.** `grid()` is untouched: an editorial spread sets flush left because that is what it is, and the same-origins law (`grid(105)` origins == `grid(107)` origins) is still asserted. |
| **ledger** | `.col-head { padding-left: 1 }` in its own composition | **REMOVED as a local copy** — the base kit declares it for everyone. `margin-bottom: 0` stays; that is the language's pitch, not a compensation. |
| **darkside** | the same local `.col-head { padding-left: 1 }` (for its rail) | **REMOVED, same reason.** The rail's zigzag stays cured, by the base rule. |
| **solari** | none — a victim. `head()` called `fields(110)` while a row called `fields(109)`, and the band/seam agreement was luck | **NOTHING TO REMOVE.** One measure now, so the captions stand on the rows' own field origins by construction. |
| **blueprint** | none — a victim, same shape (`field(w)` at two different `w`) | **NOTHING TO REMOVE.** |
| **corgi · nord · naught** | none | untouched; they gain the shared origin. |

**THE SHARED EDGE, before and after (verbatim, `_edges43.py` over the suite's own dumps):**

```
BEFORE                                            AFTER
ledger @118: rule 3..112 | closing rule 111       ledger @118: rule 3..111 | closing rule 111
ledger  @80: rule 3..74  | closing rule  73       ledger  @80: rule 3..73  | closing rule  73
solari @118: seam 3..111 | head text 3..110       solari @118: seam 3..111 | head text 4..110
solari  @80: seam 3..73  | head text 3..72        solari  @80: seam 3..73  | head text 4..72
```

Solari's head TEXT moves right one cell because the gate legend opens with its own space; what
matters is the BAND, which the suite measures off the compositor's grounds and which now opens and
closes on the seam's own cells (`band == seam`, both edges, at 118 and 80 — it used to assert
`0 <= seam[0] - band[0] <= 1`). The solari board at 118 after the cure, head over first row:

```
   GATE BACKLOG 07                                                                 STATUS    PROJ          PRI
  03  RENEW TLS CERTIFICATE                                                        BOARDING  --            HIGH
  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
```

`STATUS`/`PROJ`/`PRI` sit exactly over `BOARDING`/`--`/`HIGH`. Instrument at 118, axis over trace
— origin cell 9 in both rows, the ticks on the same cells:

```
    BACKLOG                               7      DOING                             6      DONE           2
      ─├────7d┴───14d┴───21d┴                      ─├────7d┴───14d┴───21d┴                  ─├────7d┴
    ⣿ Renew TLS certificate············ 3d       ⣿ Fix checkout 500 error······ blk       ⠂ Set up C… done
      ⠒⣿⣿⣿⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊ 3d                   ⣿⠒⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊ -2d              ⠒⠒⠒⠒⠒⠒⠒⠒┊⠒ --
```

**THE CHECKS ARE EXACT NOW, and two of them are new laws read off the COMPOSITOR.**
`verify_language` **2087 → 2151, +64**, arithmetic in full: the new *ONE MEASURE* block is 10
languages × 2 widths × 3 checks = **+60** (a self-check that a head AND a card were mounted, then
`head.content_region.x == card.content_region.x` and
`row_width(head.outer_size.width) == card.size.width - CARD_OWN`); instrument's kit pair became
three (**+1**); industrial's legend check gained a fills-its-measure partner (**+1**); solari's
one bounded band check became two exact ones, at two widths (**+2**). Nothing was deleted — every
upgraded check replaced one of the same name:

- ledger `<=2` → `start + len(run) - 1 == cells[-1]` (exact, 118 and 80)
- solari `0 <= seam[0] - band[0] <= 1` → `seam[0] == band[0]` **and** `band == seam` (118 and 80)
- blueprint `abs(hx - ix[0]) <= 1` → `hx == ix[0]` (118 and 80)
- instrument `reticle(hw - HEAD_TRIM)[0] <= reticle(cw)[0]` over six hand-tabulated pairs →
  origin equality and tick-cell equality at **every** reticled width class, plus a self-check that
  the class list is not empty (three widths qualify, so neither law can pass vacuously)
- swiss `1 + g105[0][0]` → `g105[0][0]`
- industrial `startswith(" ▐▌ ")` → `startswith("▐▌ ")`

**THE NEW LAWS ARE MUTATION-PROVEN** (`_mut43.py`, throwaway, in no suite) — a check that cannot
fail is dead metadata, and both of these are one line of arithmetic away from being tautologies:

```
baseline            (3, 3, 109, 109) origin_ok True  measure_ok True
mut head inset=0    (2, 3, 109, 109) origin_ok False measure_ok True
mut card padding=2  (3, 4, 109, 107) origin_ok False measure_ok False
```

Dropping the head's inset breaks the ORIGIN law; changing what `.kb-card`'s box costs breaks the
MEASURE law (it compares what Textual actually gave the card against what the law predicts from
the head's own seat, so any language that restyles either seat trips it).

**RIDER — `verify_aperture`'s `P` check, the forty-second pass's own flag.** "`P` is no longer
SHOWN anywhere" queried `binding_map(screen, shown=True)` and, with `P` unbound, passed
**vacuously**. It now asserts `P` is absent from `binding_map(screen)` entirely — the fact the
pass-42 probe demonstrated. Count unchanged at **112** (one line, same check).

**One thing NOT done, deliberately, and it is the honest residual:** the empty seat is aligned and
measured with the others now, but the CARD'S OWN double spend (`CARD_OWN`) is untouched — every
card row leaves two cells of its box unused at the right. Fixing that widens every card by two and
moves every app-level geometry assertion in the suite; it is a separate increment, and this one
was about the head and the card agreeing, not about which of them is generous.

**Files (5, the exact budget):** `prototypes/widget_slice/kanban.py` · `taskboard/language.py` ·
`prototypes/verify_language.py` · `prototypes/verify_aperture.py` (the 1-line rider) · this file.
`widget.tcss` was NOT touched — the padding law went into the base kit's `tcss()`, which is where
the two languages that already had it kept theirs.

**Runs, three times back to back, all green, no flake fired:** `pytest` **137 passed** (27.4 /
28.0 / 28.4 s) · `verify_widget` **24** · `verify_board` **22** · `verify_language` **2151** ·
`verify_aperture` **112** — 0 FAIL in all twelve runs. Neither named flake (the darkside capture
race, `test_win_clipboard_roundtrip`) appeared. Nothing committed, all local in this worktree.

**Done 2026-07-27 (forty-second pass) — THE LEGACY `P` DOOR IS CLOSED.** This closes the first
debt bullet of the forty-first pass ("**`P` is still bound**"): the shifted door survived only
because `tests/test_app.py` pressed `"P"` in five places, i.e. the tests encoded the very defect
the user reported. This is the FIRST pass allowed to touch `tests/`, and it spends that permission
on exactly those five key presses — nothing else in the suite was edited.

**The three edits:**
- `taskboard/app.py` — deleted `Binding("P", "manage_projects", "Projects (old P)", show=False)`.
  Its row left the `?` map with it: `HelpScreen`'s content is built from `binding_map(screen)`,
  i.e. from `active_bindings`, so removing the binding removes the row — no second edit, and no
  hand-written list could have drifted here. The comment above `m` was rewritten to state the law
  rather than the exception.
- `tests/test_app.py` — `pilot.press("P")` → `pilot.press("m")` at lines **130, 154, 179, 202,
  221**, in `test_manage_projects_edit_status_persists`, `_archive_hides_and_persists`,
  `_delete_moves_tasks_to_inbox`, `_empty_state_no_crash`, `_escapes_markup_name`. Every one of the
  five was a plain key press with no other coupling to `P`; each test still asserts exactly what it
  asserted before (the ProjectPicker opens, then edit/archive/delete/empty/markup behaviour). They
  pass for the right reason — see the probe below, which proves `m` is what opens the modal now.
- this file.

**The proof the door is CLOSED, not merely unadvertised** (`prototypes\out\_probe_p_door.py`,
throwaway, in no suite) — pass 41 could only claim `P` was "no longer SHOWN":

```
  board screen: Screen  stack=1
  P in the register?  []
  after P: screen=Screen  stack=1  -> NOTHING HAPPENED (door closed)
  after m: screen=ProjectPicker  stack=2  -> MODAL OPEN
```

**The register law now holds with ZERO exceptions in the shipped app** — no key in `taskboard/`
requires shift, and none is bound-but-unreachable. `verify_aperture` needed no edit and its count
is unchanged at **112**: it never carried a carve-out for legacy `P`. Its two `P` references still
hold, one of them now for a stronger reason — the aperture probe (`P` among the board keys pressed
one at a time, asserted to do nothing and to be absent from `active_bindings`) now passes because
`P` is not bound anywhere, and the board check "`P` is no longer SHOWN anywhere" is now true
vacuously. **That second check is weaker than the fact it guards** and should be tightened to
"`P` is not in `binding_map(screen)` at all" — `prototypes/` was out of this pass's budget.

**Runs:** `pytest` **137 passed** (30.6 s, no flake, no skip) · `verify_aperture` **112, ALL
PASSED, 0 FAIL** · `verify_language` **2087, ALL PASSED, 0 FAIL** (untouched files — the run is the
coupling check; the darkside capture race did not fire) · `verify_widget` ALL PASSED ·
`verify_board` ALL PASSED. Nothing committed, all local in this worktree.

**Done 2026-07-27 (forty-first pass) — THE LEGEND CURE LANDS AT THE SHIPPED SEAT.** The fortieth
pass cured the mock and measured the same defect, worse, in `taskboard/` (its deferred finding).
This pass cures it there. Nothing in `views.py`, `language.py`, `hero.py` or `tests/` was touched.

**What was cured, against the fortieth pass's own measurements:**

| defect (measured, `out\_realapp40.py`) | cure |
|---|---|
| the aperture (`6`) composes NO Footer: **22 shown bindings**, one hand-written row naming four | a DERIVED legend in `#ap-foot`; the aperture's key surface is now **9 shown bindings**, all printed |
| `q` on the aperture **quit the app**, unindicated | `q,escape,6` → Back. Quit stays on the board's `q`; `ctrl+q` is still the door from anywhere |
| `a e d x v o i c p f enter delete` live on the aperture, indicated nowhere; `d` opened a delete-confirm for a task nobody could see | `App.BOARD_ACTIONS` + `check_action` **drop** them there (**False**, not None) — the aperture is the ambient face of the board, not the board |
| **`P` → Projects was `show=True` and needed SHIFT** (the user's exact symptom) | the unshifted door is **`m`**; `P` survives only as a `show=False` legacy alias, printed in the map |
| main footer: 29 shown bindings, **12 printed at 118**, `q Quit` clipped off the edge | 11 shown, **all 11 print at 118 with ~12 columns of slack**; the other 21 keys are `show=False` WITH their words in the new `?` map |

**The legend surface: a derived hint row, not a `Footer` — stated because it was a choice.** A
docked Textual `Footer` would wear the app's palette inside a surface the LANGUAGE owns, and the
languages that narrow the ambient column (darkside's centred 46) would squeeze it; the Footer also
prints only the FIRST key of a multi-key binding and lets a group label eat every description
(pass 40's traps). `#ap-foot` already existed — it now carries `legend_row`-style output derived
from `binding_map(screen)`, i.e. from `active_bindings`, so it cannot drift and cannot lie about
what `check_action` dropped. Three tiers, because the row is ONE row high and a row that does not
fit is clipped, not wrapped: words (`1 lanes · 2 cols · … · q/esc/6 back · ? keys`, 118 cols) →
the numbered family under one label (`1 2 3 4 5 views · …`, 96 and 80) → the two doors
(`q/esc/6 back · ? keys`, 60 and below). Aliases print as `q/esc/6`, `d/del`, `↑/k` — hjkl and the
`delete` key were indicated on NO surface before.

**`?` is a new tier, shared by both surfaces:** `HelpScreen` builds the FULL map of whatever screen
is in front (shown + `show=False`), in two columns balanced by line count, snapping the split to a
section boundary and repeating the heading as `(cont.)` when it cannot. It prints 36 rows on the
board — including the 6 scroll keys and `ctrl+q`/`ctrl+p`, which no BINDINGS list here owns — and
its own way out rides on the title (`KEYS   esc/?/q close`), because as a bottom row it was the
line the map's height pushed off the screen.

**A REAL defect the new law found, invisible in code:** in **instrument, swiss, darkside and
blueprint** the legend was rendered at `region.y = 45, 39, 45, 33` **on a 34-row screen** — the
stacked panel above it overflows and took the key row below the fold (naught too, at 60 columns).
`#ap-foot` is now `dock: bottom`. Side effect, verified: darkside's centred column now actually
centres (x=36, was x=2).

**THE LEGEND LAW, in `prototypes/verify_aperture.py`** (+93 checks, **19 → 112**): per language, on
the COMPOSITED frame — every entry starts with a live key and carries a word (a phantom is caught
by NAME, not by count); every shown key is printed; no printed key needs shift; the row never
exceeds its one row; all 10 languages promise the identical key set. Then: the three tiers at
118/96/60; the board keys asserted DEAD on the aperture (pressed one at a time) and absent from
`active_bindings`; a DRIVE of every printed key unshifted (1-5 exit into the right view, `t`, `r`,
`esc`, `q` → back with the app still running); the `?` map asserted to list every live key of the
surface behind it; the board's footer asserted to print all 11 shown entries plus `q Quit`/`? Keys`;
`m` asserted to really open the picker; and both quit paths on their own app instances.

**The law has teeth — proven, not assumed** (`out\_control41.py`, throwaway): a phantom entry, a
deleted working key, a shifted key restored, the legend UNDOCKED (the off-fold defect above), and
the board keys re-enabled on the aperture — **all five go red**. In-file self-checks cover the
parser cases cheaply. One case taught the control something: patching `BINDINGS` after import does
nothing (Textual freezes them into `_bindings` at class creation) — bind on the instance.

**Runs:** `verify_aperture` **112, ALL PASSED, three back-to-back, no flake** · `verify_language`
**2087, ALL PASSED** (untouched files — the run is the coupling check) · `verify_widget` 24 ·
`verify_board` 22 · `pytest` **137 passed** (one run hit the named `test_win_clipboard_roundtrip`
flake — WinError 206 from the PowerShell clipboard round-trip — and passed on rerun). Looked at:
naught, ledger and darkside apertures at 118×34 (`out\_ap41_*.txt`) plus the `?` map over the
aperture — legend on the last row in all three, nothing wrapped, language theming intact.

**Behaviour changes, stated:** (1) `q` on the aperture no longer quits — it goes back; (2) the
board's editing keys no longer fire on the aperture; (3) the board's footer shows 11 keys instead
of 29-listed/12-printed — `x v o i c p m f enter tab` and the motion keys moved to `?`; (4) `P`
is no longer advertised anywhere.

**Debt, honest:**
- **`P` is still bound.** Five tests in `tests/test_app.py` press `"P"` to open the project manager
  (lines 130, 154, 179, 202, 221) — the test encodes the defect. `tests/` is out of this pass's
  budget, so the shifted door is kept as a documented `show=False` alias. Closing it is a 5-line
  test edit plus deleting one binding.
- **The board's Footer is still size-blind.** At 118 all 11 entries print; at 96 it clips after
  `a Add`, at 80 after `q Quit`. The order was chosen for that: `? Keys` and `q Quit` are printed
  BEFORE the letter actions, so the two keys that must survive a clip do. A size-aware footer needs
  a custom widget (Textual's `Footer` cannot degrade) — still owed, on both surfaces' behalf.
- **The language switch can render one stale frame.** `set_language` changes the regions' widths,
  and rows built before the layout runs wrap inside the new composition (darkside's queue folds its
  date chips). The 1 s tick heals it. A 2-frame `call_after_refresh` looked like the cure in a hand
  probe and **was not**: it fires while the layout is running, `redraw`'s `wof()` then measures
  transient widths, and verify_language's solari/ledger/blueprint band laws went red on the frames
  it produced (bisected, reverted). The real cure is a width-CHANGE trigger, not a frame count.
- Modals still shadow the board's footer while it advertises keys they consume (`ModalScreen` stops
  app bindings, so those keys are inert, not dangerous). The mock's answer — a Footer per modal —
  needs `modals.py`, out of budget.

**Done 2026-07-27 (fortieth pass) — THE BINDINGS/LEGEND CURE. User defect, verbatim: "I got
lost with the bindings last time I navigated the languages mock. Now it's ctrl+q to quit and
shift+binding to use the application — there was no indication sustaining this."** All three
halves reproduced by measurement before anything was changed. App-global, so every language was
equally affected — nothing here is a language's fault.

**THE AUDIT — the mock's real key surface vs. what any surface showed** (`prototypes\widget_slice\
app.py`, textual 8.2.8, 118×30, fixture board):

| key | action | worked? | shown where | verdict |
|---|---|---|---|---|
| `V` | cycle_size | yes, **shift only** (`v` dead) | footer, as bare `V` | **the shift defect** |
| `q` | quit | aperture ✓ · config ✓ (**killed the app**) · gallery ✗ · help ✗ | footer, as bare `q` | **dead on both modals** |
| `ctrl+q` | quit | **everywhere** (priority=True) | **nowhere** | the only door out of a modal |
| `c ? V r t g q` | seven actions | yes | footer as `c ? V r t g q Widget` | **descriptions eaten by the group label** |
| `1 2 3 4` | views | yes | footer as `1 2 3 4 Navigation` | label lied: motion is hjkl, not 1-4 |
| `←→↑↓ h j k l` | nav | yes | **nowhere** (`show=False`, and `?` skipped `show=False`) | unindicated |
| `tab` / `shift+tab` | focus | yes | **nowhere** | unindicated |
| `ctrl+p` | palette | yes | footer, docked right | ok |
| `bracketleft` / `bracketright` | threshold ± | yes (`[` / `]`) | config footer as **`bracketleft`** | a key name nobody can type |
| `space,enter` | toggle | both | config footer as `space` only | `enter` unindicated |
| gallery `t language · esc close` | — | **`t` was DEAD there** | hand-written, below the box fold | **a printed lie, 3 passes old** |
| aperture footer, seen *through* a modal | — | those keys are shadowed | visible, dimmed | **a legend advertising dead keys** |

The reproduction of the user's exact sentence: `g` → `q` does nothing → only `ctrl+q` closes.
Measured, not inferred (`out\_audit40c.py`): aperture+`q` → app stops; gallery+`q` → still
running; gallery+`ctrl+q` → stops.

**Root cause of the missing descriptions, and a Textual trap worth recording:** `Footer.compose`
(textual 8.2.8 `_footer.py:269`) renders a *grouped* binding with `description=""` — the group
label replaces every key's word. `Footer.combine_groups` is a reactive that `compose()` never
reads: **dead metadata, it cannot be turned off.** A group is only affordable where the keys are a
numbered family one label can honestly name.

**THE CURE.** One law, stated so it can be tested: *every key that fires an action on a surface is
printed on that surface, and every key printed on a surface fires there. No shown key needs shift.*

- **`V` → `v`.** `v` was unclaimed. **No shown binding in the mock needs shift any more**, asserted
  per binding, and pressing `V` is asserted to do *nothing* (the old door is closed, not aliased).
- **The letter keys carry their own words**: `c Signals  ? Keys  v Size  r Refresh  t Language
  g Gallery  q Quit`. Only `1 2 3 4 Views` stays grouped — a numbered family, relabelled from
  "Navigation" (which named the hjkl keys it did not list).
- **`q` closes the surface in front of you, everywhere.** Gallery/help/config bind it themselves,
  so it is never dead; on the aperture it still quits. `ctrl+q` remains the universal fallback and
  is now *printed*, in `?`.
- **The modals grew their own `Footer`.** A modal floats over the aperture's legend, which
  advertises keys it shadows; the legend now belongs to the surface in front.
- **`?` lists everything** — `show=False` motion keys included, plus `ctrl+q`/`ctrl+p` which no
  BINDINGS list here owns. Two columns, because one column of the full map is 32 rows on a 30-row
  screen and the hidden keys were exactly the ones scrolled off (`#help-box` 46 → 62 wide).
- **`App.check_action`** drops the aperture-only actions on pushed screens. They used to fire —
  `1` switched a view nobody could see, `c` pushed a *second* config screen — and they ate the
  footer width that clipped the config screen's own keys off the right edge at 118. **`False`, not
  `None`:** `screen.py` drops a binding only on `is False`; `None` leaves it listed and merely
  disabled, i.e. the defect one layer down.
- **Every hand-written hint row is now DERIVED** from that screen's own `BINDINGS` (`hint_row()`),
  through Textual's own `format_key` — which is why `bracketleft` became `[`. A hand-written hint
  drifts the moment a binding moves; this one cannot.

**THE LEGEND LAW, in `verify_language.py`** (+97 checks, **1990 → 2087**): per language, on the
composited frame — every shown binding's key is on the legend row; the row promises nothing that is
not bound (vocabulary check, so a phantom entry is caught *by name*); the row names what each key
does; and all 10 languages promise the identical key set (a language may restyle the legend, it may
not change the keymap). Then app-global: the register law per binding; a **drive** of every printed
key by pressing exactly that key with no shift (`t v r 1 2 3 4 g c ?`, plus `V` asserted inert);
the same two-halves law re-run on each modal's own footer; `q` asserted to leave each screen; the
`?` map asserted to list every binding including the hidden ones; and the quit path on its own app
instance (`q` → the app stops), so the suite is never killed mid-run.

**The law has teeth — proven, not assumed** (`out\_control40.py`, a throwaway, not left in the
suite): injecting (A) a phantom legend entry, (B) a working key deleted from the row, (C) the `V`
binding restored, and (D) a press of `V` — all four go red. In-file self-checks cover the same
three cases cheaply.

**Runs:** `verify_language.py` **2087 checks, ALL PASSED, three back-to-back runs, no flake** (the
darkside capture race did not fire; settle worst 4 of 40 over 111 captures). `verify_aperture` 19 ·
`verify_widget` 24 · `verify_board` 22 · `pytest` **137 passed**. Files: `app.py`, `widget.tcss`,
`verify_language.py`, `PENDING.md`.

**FINDING, DEFERRED — the SHIPPED app has the same defect, worse** (measured only,
`out\_realapp40.py`; nothing in `taskboard/` was touched):

- **`taskboard/aperture.py` (the `6` screen) composes NO `Footer` at all.** 22 `show=True` bindings
  are active there and its entire key surface is one hand-written line: `1-5 views · t language ·
  r refresh · esc back`. Unindicated and working: `q` (**quits the app**), `a` `e` `d` `x` `v` `o`
  `i` `c` `p` `f` `enter` `delete`.
- **`P` → Projects is `show=True` and needs SHIFT** — the user's "shift+binding", in the app that
  ships. (`taskboard/modals.py`'s other shift keys are Textual's own text-editing bindings,
  `show=False`, and are fine.)
- The main screen's footer is honest per key but **clipped**: 29 shown bindings, 12 printed at 118
  columns; `q Quit` is among those off the right edge.
- A cure there is the same three moves (footer on the aperture, `P` → lowercase or the `?` tier, a
  size-aware legend) but it is `taskboard/` code and out of this pass's budget.

**Known limit, stated rather than hidden:** the cured legend fits at 118 columns with ~11 columns
of slack. Below roughly 84 the `Footer` scrolls and clips — the same failure class this pass cured,
at a width the mock is not judged at. A size-class-aware legend (drop to `? keys · q quit` at
glance/widget) is the honest next increment.

**Done 2026-07-27 (thirty-ninth pass) — NORD'S HERO PANEL GETS A FIRST FIXATION. PENDING item
0e is CLOSED at the seat that ships.** The twenty-eighth pass cured the BOARD with the split and
left the panel above it measured but untouched. Two nord tokens and one `hero.py` seat later, the
panel's headline is the only element that owns rows of its own — and the panel draws **less ink
than before**, which is the direction the empty-space-earned law wants.

**Before / after, the shipped aperture at 118×30, the hero panel verbatim** (`_cmp39.txt`):

```
  BEFORE (overdue)                                   AFTER (overdue)
         ▐██▌                         ███                   ▐████▌
        ▄▞▀▀▚▄                        ███                 ██▌    ▐██
        █▌  ▐█                        ███▅▅▅                     ▐██
            ▐█                        ██████                   ██▌
           ▄▞▀                        ██████▂▂▂            ▐██
           █▌                         █████████          ██▌
         ▐█                           LOAD · 8 WK        ██████████
        ▄▞▀
        █▌                                            DAYS OVERDUE      █▅▂   LOAD · 8 WK
```

**THE DEFECT WAS TWO DEFECTS WEARING ONE NUMBER, and the second one is the finding.** Pass 28
recorded "25 cells against 61" and read it as a ranking problem. Re-measured at the shipped seat
it is also a GEOMETRY problem: **`bases.BASE_SCALE` gives quadrant `(3, 3)`, so a seven-row font
draws ELEVEN cell rows into a NINE-row hero.** The trim at the end of `hero.draw` then cut the
figure's own baseline off — the `2` above loses `██████` / `▀▀▀▀▀▀` and reads as a fragment — and
**the caption never drew at all** at this seat. The panel's headline was an incomplete mark with
nothing naming it, standing beside a six-row chart in the accent. A base's global scale knows
nothing about the panel it lands in; that is what `hero_fit` fixes.

**THE MEASURED WINNER TABLES, pass 28's own instrument** (ink cells grouped by foreground hex,
ranked by the weighted channel sum `0.2126R + 0.7152G + 0.0722B` — a perceptual PROXY, named as
one). Every row is captured on this run, the pre-cure one by taking the two tokens away at
runtime rather than quoting a previous pass (`_panel39.txt`):

| | ink | lum | cells | extent | panel rows |
|---|---|---|---|---|---|
| **PRE-CURE, overdue** | load chart (accent) | 181.2 | **36** | 54 | 0-5 |
| | hero numeral (alert) | 117.6 | **28** | 54 | 0-8 |
| | plot caption (dim) | 85.3 | 8 | 11 | 6 |
| **CURED, overdue** | caption + spark (mut) | 135.0 | 14 | 35 | 8 |
| | **hero numeral (alert)** | 117.6 | **34** | **70** | **0-6** |
| | load caption (dim) | 85.3 | 8 | 11 | 8 |
| **CURED, calm** | **hero numeral (warn)** | **205.2** | **29** | **56** | **0-6** |
| | caption + spark (mut) | 135.0 | 11 | 34 | 8 |
| | load caption (dim) | 85.3 | 8 | 11 | 8 |

Panel ink **72 → 56 cells overdue (−22 %)** and **72 → 48 calm (−33 %)**. The fixation is bought
with empty space, not with more marks — asserted on both fixtures.

**THE CURE, and why each half was chosen by measuring rather than by taste.**

- **`hero_plot=("mut", 2)` — the load surrenders brightness AND rank.** The brief's cheapest
  lever was "demote the chart to `mut`", and the measurement says that alone is **not**
  sufficient: with the chart still six rows tall it keeps rows the numeral also paints, so
  NOTHING in the panel is isolated and the law still has no winner. So the load drops a
  PRIMITIVE as well as a tier — it becomes DATAVIZ's one-row `spark`, which is the same meter
  family (the dispatch law is intact) with level still riding on SHAPE (`' ▂▅█'`). It rides the
  caption row, tight to its label, Nothing-style. **The accent now appears NOWHERE in the
  panel** — asserted — which is the point HIERARCHY.md makes about spending the identity hue on
  ambient data.
- **`hero_fit=(5, 2)` — the numeral gains area inside the budget it already had.** 7 cell rows
  instead of 11, so the figure lands complete with its blank row and its caption under it
  (7 + 1 + 1 = 9, the aperture's pin exactly). The rows it gives up are spent on WIDTH, which is
  also the honest direction: a terminal cell is ~1:2, and at `(3, 3)` the figure's visual aspect
  was **0.27** against the [0.55, 0.80] bracket the display-type passes hold every digit to. It
  is **0.71** now — inside the bracket that slab and stencil were measured against.
- **The panel did NOT grow.** `#hero` is 9 rows before and after; `verify_aperture` reads
  nord at `h=9`, inside its 12-row budget.

**THE BRIGHTNESS AXIS IS A DECLARED PAIR, not a claim that quietly picks its fixture.** On the
CALM board the numeral's ink is strictly the brightest in the panel (**205.2 vs 135.0**) and that
is asserted. On the OVERDUE board it cannot be, and the reason is a property of this palette
rather than of this design: **nord's `alert` (#bf616a, 117.6) is DARKER than its label grey
`mut` (#7b88a1, 135.0)**, and demoting the label to `dim` to win the comparison would have put
it at 1.69:1 against the ground — asserting the caption away. So the reason is itself a check
(`chan_lum(alert) < chan_lum(mut)`), and what the overdue frame asserts is the ladder: the
numeral wears a RESERVED SEMANTIC hue and **no passive element in the panel is brighter than the
label tier**. Same shape as blueprint's `warn == mut` skip (pass 37), and the same discipline —
**both fixtures' truth is checked before the law is written** (`_fixture_board.json` really has
two past-due tasks; `_fixture_calm.json` really has none).

**THE ONE RESIDUAL, and it is asserted rather than implied: the PROTOTYPE is not cured.**
`prototypes/widget_slice/app.py` still forks `Hero.show` (pass 35's open item 3), so neither
token reaches it and its panel renders exactly as pass 28 measured it. **[CLOSED, forty-fourth
pass: the fork is folded onto `hero.py` and the prototype reads both tokens.]** Pass 36 made this same
call for the flap faces and named the reason — **the shipped aperture is the seat that matters**
— and app code was outside this pass's file set either way. Two checks state it out loud: the
prototype's hero AND nord's board are byte-identical with both tokens force-cleared. That second
one is also how "nord's board render is otherwise unchanged" is proved: **the board renders only
at the forked seat, so it cannot have moved.** Unreachability, not a diff.

**BYTE-IDENTITY FOR THE OTHER NINE, the pass-36 form.** Rather than diffing against a stored
baseline, the tokens are TAKEN AWAY at runtime and every language that does not declare them
must render identically either way — nine checks plus the control that **nord MOVES** when they
are cleared, so the nine cannot pass for the wrong reason. Each of the nine is also asserted to
declare neither token.

**Counts: verify_language 1930 → 1990 (+60), 3 of 3 BACK-TO-BACK GREEN** (`_run39_{0,1,2}.txt`,
rc=0, ALL PASSED ×3, 1990 checks each). **0 checks removed, 0 replaced.** The 60: the pre-cure
control (6 — the old ranking, the empty isolated set, the 11-rows-into-9 fact and the missing
caption), the fit's own geometry (3), then per fixture the truth check, the isolation pair, both
area measures, the accent's absence, the caption's return, the no-wrap fit, the ink drop and the
severity half (23 across the two), the data-survival block (6 — different series moves it, moves
in GREYSCALE, the microbar floor, the `meter` dispatch, the declared tone, the reserved caption
width), and the isolation-of-the-change block (22 — nine languages × two, nord's own declaration,
the moves-when-cleared control, and the two prototype/board unreachability checks). **The
darkside race did NOT fire on any of the three**, which is not evidence it is gone.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** (nord h=9) ·
`verify_widget` **ALL PASSED**, full redraw median **1564 µs = 9.39 %** of a 60 fps frame ·
`verify_board` **ALL PASSED** (headroom worst 5 of 40 over 62 settles) · `pytest tests`
**137 passed**. verify_language settle headroom worst **4 / 5 / 4 of 40 over 98 captures** across
the three runs — the capture count rose from 94 because this pass opens 5 more apps, and the
worst case moved by one on one run.

**Open after this pass, each with why it was not taken.**

1. **The PROTOTYPE panel still carries the whole defect** (above). Curing it means either
   `prototypes/widget_slice/app.py` or the long-owed FOLD of that fork onto `taskboard/hero.py`,
   which is on the closing list already and is bigger than an increment.
2. **`hero_fit` is a second place a glyph's scale can be declared** — `bases.BASE_SCALE` is the
   first. This is the same shape of fact as `BASE_GLYPH` (pass 36's open item 3) and it is the
   third signal that the drawn-type stack wants one metrics seat rather than three.
3. **The spark blanks a zero week** (`' ▂▅█'[0]` is a space), so a flat-zero series draws no
   unlit track — DATAVIZ law 4 asks for one. That is `Kit.spark`'s pre-existing property, shared
   by every blocks language, and `language.py` was outside this file set. The microbar floor
   (law 3) IS asserted and holds.
4. **The demotion swaps `accent` for the ambient tone around the call.** It is exact for nord's
   `blocks` spark, which draws no other hue, and it would be partial for a mechanism keyed off
   `ink` or `mut`. Documented at the seat; no second language declares the token.
5. **`RUN.md` still advertises `verify_language` at 356 checks** — stale since the twenty-eighth
   pass, outside the file budget for the sixth time.

**Artifacts (`prototypes/out/`, outside the file budget):** `_cmp39.py` / `_cmp39.txt` (**the
panel before and after, both fixtures, same seat — this pass is judged by eye and that is the
file to look at**) · `_probe39.py` / `_probe39.txt` (the two seats measured side by side, which
is where the prototype fork was caught) · `_panel39.txt` (written by the suite: the three winner
tables) · `_run39_{0,1,2}.txt` and `_run39_verify_{aperture,widget,board}.txt`.

**Done 2026-07-27 (thirty-eighth pass) — THE EMPTY-STATE SEAT IN THE SECTIONS LAYOUT.
PENDING item 7 is CLOSED.** Six languages stop showing NOTHING for an empty phase. Nine lines
of `kanban.py` mirroring the split branch, and it repaid every language on the sections
branch at once — the cheapest item on the list, exactly as it was scoped.

**WHAT WAS WRONG, as the code rather than as an impression.** `KanbanBoard.build()` has three
branches. The columns branch has mounted `k.empty()` since the beginning and the split branch
took one deliberately when nord recomposed (the twenty-eighth pass wrote the comment saying
so). The sections branch never had one: it looped the bucket and mounted a card per task, so a
bucket of zero mounted zero widgets and the phase head was followed by the next phase head.
As the `layout` token rolled out (passes 32-34) the branch went from two languages to **six**,
and corgi actively LOST a seat it used to have.

**THE FIX IS THE SPLIT BRANCH'S SHAPE, deliberately, because the discipline is what matters
here.** `if not bucket: sc.mount(Static(k.empty(ew), classes="kb-empty"))` / `else:` around
the existing sort-and-mount loop. Mounted on the reference `build()` already holds (`sc`), never
looked up by id after a rebuild — the thirtieth pass's zombie-pane lesson, which is law in this
file. `self.cards.append(col_cards)` still runs for the empty phase, so the nav model is
untouched and `move()` keeps skipping empty columns exactly as before.

**THE WIDTH IS THE SEAT'S OWN CONTENT BOX AND NOT THE HEAD'S**, and the difference is the point.
`.kb-empty` takes no padding and the flat list reserves one cell for its scroll bar
(`scrollbar-size: 1 1`), so the honest number is `avail - 1`. The head's `avail - 4` was NOT
copied: that number is already known to be one cell off the card's content box (open item 4
below), and propagating it would have spread a measured defect to a second surface. Where the
list does not overflow this under-claims by the one scrollbar cell — the safe direction, since
the seat is never told it is wider than it is.

**THE SURFACE THE COLUMNS LANGUAGES CANNOT AFFORD, and the finding is that four languages
refuse it anyway.** `empty()` draws the mascot only at `w >= 14`, and a weighted column is
routinely narrower — so a sections row, being the full board width, ALWAYS clears the gate.
The prediction going in was that all six would gain the creature. **Measured, two do:**

| | mascot rows | seat at 118 | what the seat draws |
|---|---|---|---|
| **corgi** | 6 | 113x7 | the creature + `[0] NO TASKS` |
| **blueprint** | 6 | 113x7 | the creature through `stencil` + `NO ITEMS ON SHEET` |
| swiss | **0** | 109x1 | `nothing here` |
| darkside | **0** | 113x1 | `nothing here` |
| ledger | **0** | 113x1 | `nil balance` |
| solari | **0** | 113x1 | `NO DEPARTURES` |

The four zeros are **declared renunciations, not omissions** — `Swiss.mascot` returns `[]`
("no ornament"), `Darkside.mascot` ("identity is the doodle, recessive"), `Ledger.mascot` ("a
ledger keeps no pet"), `Solari.mascot` ("a departure board keeps no pet"). The suite asserts
both halves in the direction each language declares (`type(k).mascot is not Kit.mascot` for the
renouncing four), so a language that renounces can never be confused with a seat that failed to
draw. Blueprint's creature comes out through the thirty-seventh pass's hollow base — `▌▄▄▐`
ears, no solid block — which is the axis composing with itself and cost nothing.

**REACHABILITY IS ASSERTED, not assumed — the twenty-third pass's lesson applied.** A sections
list stacks its phases and the emptied one (`Done`) is last, so at 118x30 **every one of the six
seats starts BELOW THE FOLD**. "It is mounted" and "the user can see it" are different claims
and this pass makes both: the contents are asked of the widget TREE, then the flat list is
scrolled to its end and the voice is asserted **on the composited SCREEN**. The below-the-fold
fact is carried in each check's own detail rather than hidden.

**A DEFECT THE RENDER CAUGHT, and it is the kind that would have passed for the wrong reason.**
The first version read the seat with `grey(str(seat.render()))`, copying the neighbouring nord
check. `Static.render()` returns a `Content` and **`str()` of it is ALREADY plain** — the markup
was resolved on the way in — so `grey()` runs its tag regex over literal text. Corgi's voice is
`\[0] NO TASKS`, whose escape is gone by that point, so the regex ate the `[0]` and the check
went red on a seat that was drawing perfectly. Only the VOICE literal is grey'd now, because
that one really is markup. **The same latent over-strip is still in the nord split check two
blocks up** — it passes because nord's voice is the bracket-free word `empty` — and it is named
here rather than fixed, because that check is correct today and this was not its increment.

**BYTE-IDENTITY FOR EVERY OTHER RENDER IS PROVED BY UNREACHABILITY**, which is the same form
pass 36 used and the stronger one. The added branch cannot execute unless a bucket is empty, so
the suite asserts per language, on the NORMAL fixture and through the real app, that **zero
`.kb-empty` seats are mounted** — no board captured on `fx` anywhere in the suite can have
moved. The pixel-level negative control is kept too (the voice is absent from `boards[name]`).

**Counts: verify_language 1883 → 1930 (+47), 3 of 3 BACK-TO-BACK GREEN** (`_run38_{0,1,2}.txt`,
rc=0, ALL PASSED ×3, 1930 checks each). **0 checks removed; 1 replaced** — "corgi: NO
empty-state seat is mounted at all" was the recorded COST of this gap and had to go when the
gap closed; it is replaced by the stronger pair (the head still states its count AND the seat is
back beneath it), so corgi's compensation is not silently dropped along with the defect. The
47: the sections roster, then per language the mascot gate or its renunciation, the mount, the
voice, the mascot/voice-alone contents, the no-wrap fit, the scrolled reachability, the
mounted-zero unreachability control and the pixel negative control.

**THE DARKSIDE RACE FIRED ONCE** on run 2, with its exact 4-check signature (`darkside:
sections board keeps titles legible` · `the fixture card is on screen (probe self-check)` · `the
rail LEADS the card row` · `the title survives the rail INTACT`) and **no settle timeout**;
rerun once, green, per the standing protocol. Reported, not chased.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** · `verify_widget`
**ALL PASSED**, full redraw median **1311 µs = 7.87 %** of a 60 fps frame · `verify_board`
**ALL PASSED** (headroom worst 5 of 40 over 62 settles) · `pytest tests` **137 passed**.
verify_language settle headroom worst **4 of 40 over 94 captures**, all three runs — the count
rose from 76 to 94 because this pass opens 12 more apps, and the worst case did not move.

**Judged by eye, which is the acceptance bar** (`_probe38.txt`, one seat per language with two
rows of context above it). Verbatim, and the two ends of the range:

```
===== darkside   layout=sections  seat 113x1  mascot_rows=0
 |   ▏  done 0
 |
>|   nothing here

===== solari   layout=sections  seat 113x1  mascot_rows=0
 |
 |   GATE DONE 00
>|   NO DEPARTURES

===== corgi   layout=sections  seat 113x7  mascot_rows=6
 |  [3] D O N E  0
 |  ──────────────────────────────────────────────────────────────────────────────
>|   ██    ██
>|   ██    ██
>|
>|  █        █
>|   █      █
>|    ██████
>|   [0] NO TASKS
```

Nothing wraps at any seat (widest row 20 cells of 113, asserted per language), the voice sits
under its own phase head, and the two creatures are seated whole.

**Open after this pass, each with why it was not taken.**

1. **The seat starts BELOW THE FOLD for all six** at 118x30, because the emptied phase is the
   last one. That is the sections layout's own property (corgi's head had the same fact
   recorded before this pass) and curing it means a composition decision — which phase leads,
   or whether an empty phase collapses — not a mount. Asserted and reported, not hidden.
2. **The nord split check still double-`grey()`s its render** (above). Correct today by luck of
   a bracket-free voice; the fix is deleting one call, and it was not this increment's.
3. **`empty()` still ignores `w` except as the mascot gate** — the voice is never wrapped or
   truncated. Harmless at 113 cells and latent at a narrow one; the columns branch is where
   that would bite, and it did not bite here.
4. **`RUN.md` still advertises `verify_language` at 356 checks** — stale since the twenty-eighth
   pass, outside the file budget for the fifth time.

**Artifacts (`prototypes/out/`, outside the file budget):** `_probe38.py` / `_probe38.txt` (**the
six seats, scrolled into view, with their phase heads above them — this pass is judged by eye
and that is the file to look at**) · `_run38_{0,1,2}.txt` (the three runs; run 2's first attempt
is the darkside race and was rerun) · `_run38_verify_{aperture,widget,board}.txt`.

**Done 2026-07-27 (thirty-seventh pass) — BLUEPRINT'S `stencil`: THE HOLLOW, BRIDGED DRAWING
NUMBER, and with it the DISPLAY-TYPE AXIS IS CLOSED.** The last placeholder `hero="plain"` is
gone. Nine of ten languages now draw a hero of their own; swiss's `plain` is the one renunciation
in the set and it is a decision, not an unfinished cell.

**IT IS A PIXEL BASE, exactly as the thirty-sixth pass predicted, and the road it paved held.**
No new hero branch, no `hero.py` edit, no paint support: `hero="dot"` + `base="stencil"` reaches
`BS.draw_numeral`, and everything this figure claims it claims with SHAPE. Four files, the exact
budget: `bases.py`, `themes.py`, `verify_language.py`, `PENDING.md`.

**WHAT A STENCIL IS HERE, as three pixel ROLES rather than as a look.** `slab` asks what a pixel
is FOR and `flap` asks what it is printed ON; this one asks what its INTERIOR is, because on a
drawing sheet the figure is the CUT:

- a pixel with ink on all four sides is **INTERIOR and draws NOTHING** — in a stroke thick enough
  to afford it that is a real cell of ground running down the middle;
- a pixel of a **VERTICAL stroke draws a RAIL on each side that faces ground**: `▌` west, `▐`
  east. At the digits' one-pixel strokes that pair IS the stroke, so the ink hugs the two outer
  half-cells and a full cell-width of ground runs between them;
- everything else — a horizontal run, and the side of a stem with ink beside it — draws the row's
  **single RAIL**, `▄` above the waist and `▀` below it.

**THE HONEST READING, stated because it is the measurement and not an apology.** A row is one
cell tall and no glyph carries ink at its top AND its bottom with ground between, so **a
horizontal stroke cannot be cut at all** — it gets ONE edge, and the cut of a one-pixel stem is
HALF a cell wide rather than a whole one. The cut only becomes a real cell of ground where the
stroke is thick enough to have an interior, which the mascot is and no digit is. This is the same
shape of fact as flap's hinge-as-unlit and naught's dark dots: **counter/ink is therefore measured
with the stroke interiors counted as INK**, and it still reads **0.50 on every closed glyph**.

**WHICH edge a horizontal draws is not a preference, and the render is what settled it.** It is
the **counter-facing** one — the inverse of `slab`'s outside-hugging rule — because that edge
lands against the stem rails that continue the outline, so **the figure CLOSES**. The first
version hugged the outside and left half a cell of ground at every corner: `3` printed
`▄▄▄▄▄▄ ▐` and `5` printed `▌ ▄▄▄▄▄▄`, an outline in pieces. Both are continuous now.

**A DEFECT THE THICK-STROKE CONTROL CAUGHT, and it would never have shown on a digit.** The first
rule said "a pixel with a vertical neighbour draws only its exposed W/E rails", which is right for
a one-pixel stroke and silently WRONG for a thick region: every top-row pixel has ink below and
ink on both sides, so **the top and bottom edges of a thick figure drew nothing at all**. The
mascot renders through this base (`Kit.mascot` reads `base`, and blueprint overrides `wordmark`
but not `mascot`), so the defect was live. The rule is one rule now — rail where a side is
exposed, the row's edge otherwise — and a 6x5 solid mask is kept as the control that the outline
closes on all four sides with real ground inside it.

**THE BRIDGES, and why they are an algorithm rather than a per-glyph table.** A stencil is a sheet
with the figure cut out, so a counter's island would fall away; the bridge is the uncut strip that
holds it, and what you see in the PAINT is a **gap in the stroke**. `stencil_bridges` floods the
unlit cells from the border, groups what it cannot reach into counters, and cuts **the ring pixel
directly NORTH of each counter's north-west-most cell** — one rule, so the gaps land on the same
shoulder of every figure and read as a property of the face rather than as damage to a glyph. The
pixel it names is provably lit and in bounds (the counter's top row is minimal, and a counter that
reached the border would not be a counter). Measured: `0 4 6 9` take one cut, **`8` takes two**,
`1 2 3 5 7` take none because they have no ring to break, and `18` cuts only inside the `8`.

**Per-digit metrics, MEASURED on the rendered form** (`_probe37.txt`):

| | ink cells | aspect | counter/ink | rows | bridges |
|---|---|---|---|---|---|
| `0` `4` `6` `9` | 8 | 0.57 | **0.50** | 7 | **1** |
| `8` | 8 | 0.57 | **0.50** | 7 | **2** |
| `2` `3` `5` | 8 | 0.57 | 0.50 (open figure) | 7 | 0 |
| `1` `7` | 8 | 0.57 | — (open) | 7 | 0 |

**Two things worth saying out loud about that table.** First, **the aspect has NO spread** (0.57
for all ten) where slab's had real spread — a serif foot widens a figure and a rail does not, so
for this base the bracket really is the assertion "no digit is wider than its box", which pass 35
already named as the check's weakness. Second, **the `1` needed the same per-BASE correction**
slab and flap took (`BASE_GLYPH`): the shared `HERO_FONT` `1` inks 3 of the 4 columns it advances,
0.43 at 7 rows, and the font is instrument's and nord's too.

**THE HOLLOW LAW IS A VOCABULARY, and that is what makes it falsifiable.** "It draws a rail"
proves nothing, and this is MEASURED rather than suspected: **nord's `quadrant` hero draws
`▌` and `▐` too** (its glyph set on the same seat is `▀ ▄ █ ▌ ▐ ▖ ▗ ▘`), so a bare rail test would
have named the wrong language. What this base earns is that **every mark in the specimen is one of
`▌ ▐ ▄ ▀` and not one cell of it is a solid block** — asserted per digit, with `block2`, `slab`
and `flap` as three controls that all put `█` on the screen, and with `▐▌` (ink filling the
middle) asserted to appear nowhere. The per-language leak check states which of its two claims it
made: the five languages whose hero draws a figure must have a solid mark in it; the five that
renounce drawing are asserted to draw nothing, out loud, so the pass is not a silent one.

**AND THE LANGUAGE CONSTRAINED ITS OWN DISPLAY TYPE, which is the finding of this pass.** The
obvious hollow stroke in a terminal is the DOUBLE-LINE box family — `═` is literally two rails
with ground between them, `║` the same turned ninety degrees, and the junctions join. It is
unusable here: blueprint's own law allows the sheet exactly TEN box-drawing glyphs, **none of them
a vertical stroke or a junction**, so a display type made of `║` and `╬` would break the language
it was drawn for — and it would have broken it at a kit surface, because the mascot renders
through `base`. The half-block family is what is left, and the pass asserts that **not one
box-drawing codepoint reaches the stencil**.

**THE SHIPPED APERTURE, measured with `capture_ap_bg`:** the cut figure reaches the composited
frame, **not one cell of the hero band is a solid block**, every mark in the figure band is in the
hollow vocabulary, **the figure stands on ONE ground — the sheet — with no face and no plate
anywhere** (a painted face is a containing box drawn in background, which this language forbids),
and the hero puts **zero knockout** on the view, so the sheet's one reverse-video element is still
the title block's STATE cell. Hero height **9** (7 figure + air + caption), inside the 12-row
budget, and unlike ledger nothing pins it — **blueprint keeps its caption at every seat**.

**SEVERITY, and one skip that is DECLARED rather than quietly widened.** The calm half is asserted
at draw level where the tone is an argument: a calm hero carries zero `alert`. `warn` is skipped
there, and the reason is measured — **blueprint's `warn` IS `mut` (`#7fa8c4`)**, because this
language's near-due step is BRIGHTNESS and the caption is set in that same cyan grey; a ration
check on it would be asserting the caption away. The skip is itself a check (`warn == mut`). On
the shipped frame the claim is the one a composited render can make: every ink on the figure comes
from the severity ladder and the caption's own greys, and nowhere else.

**A PREDICATE THE HOLLOW FIGURE BROKE, reported because it is the kind that passes for the wrong
reason.** `hole()` derived its ink from a hardcoded `{█ ▀ ▄}` — every mark slab and flap make, and
NEITHER of the two rails a hollow stem is built from. A `0`'s counter would have measured 0
through a predicate that could not see its own walls. `INK` is per base now, its slab and flap
entries are exactly the sets that expression produced (so neither base's numbers move), and the
suite self-checks that each base's vocabulary is the one it actually draws. The `blocks()` filter
in the draw-level section had the same blind spot and counted 5 rows of a 7-row figure.

**Counts: verify_language 1772 → 1883 (+111), 3 of 3 BACK-TO-BACK GREEN** (`_run37_{0,1,2}.txt`,
rc=0, ALL PASSED ×3, 1883 checks each). **0 checks removed, 0 replaced** — the two widenings above
are predicates gaining a vocabulary, not claims being weakened, and both keep their controls.
**THE DARKSIDE RACE FIRED ONCE** on the second run, with its exact 4-check signature
(`darkside: sections board keeps titles legible` · `the fixture card is on screen (probe
self-check)` · `the rail LEADS the card row` · `the title survives the rail INTACT`) and no settle
timeout; rerun once, green, per the standing protocol. It is reported, not chased.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** (blueprint h=9, inside
the 12-row budget) · `verify_widget` **ALL PASSED**, redraw **1774-2070 µs = 10.6-12.4 %** of a
60 fps frame across two runs (quoted as the range it actually measured, not the friendlier
number) · `verify_board` **ALL PASSED** (headroom worst 5 of 40 over 62 settles) · `pytest tests`
**137 passed**. verify_language settle headroom worst **4 of 40 over 76 captures**, all three runs.

**Judged by eye, which is the acceptance bar** (`_spec37.txt`, `_cmp37.txt`). The posture being
replaced printed `DAYS OVERDUE` / `12` / `backlog - 3 open` as CELL TEXT — a hero that LABELS its
metric, the one thing HIERARCHY.md says a hero must not do. The drawn form reads as a stencilled
drawing number: hollow rails, bridges visible on the top-left shoulder of `0 8 9` and on the waist
of `6`, and no possibility of confusing it with slab (solid stems, serif feet), flap (solid blocks
cut by a hinge) or naught7 (round dots). It does not read worse than `plain`, so it shipped.

**Open after this pass, each with why it was not taken.**

1. **THE BRIDGE COSTS `4` ITS SHOULDER.** The `4`'s counter is a three-cell wedge whose NW-most
   cell is `(2,2)`, so the cut lands on `(1,2)` and the upper diagonal loses a pixel; the figure
   still reads by its crossbar and stem, but it is the weakest of the ten. Curing it means either
   a per-glyph bridge table (a second place a glyph can be declared — the defect `BASE_GLYPH`
   already is) or editing the shared `HERO_FONT`, which instrument and nord also draw from. Both
   are bigger than this increment. Visible in `_spec37.txt`'s bridged/bridgeless columns.
2. **`0`, `8` and `9` lose half their top bar to the bridge** — the remaining two cells are
   orthogonally isolated and touch the right stem only at the corner. That is what a real stencil
   does, and `0` stays distinct from `8` (they differ at the waist row), but it is a legibility
   cost and it is named rather than discovered later.
3. **A 2-pixel-thick stroke is not cut** (the mascot's ears render `▌▄▄▐`): two columns are both
   edges, so there is no interior to clear. Only 3-pixel and thicker strokes get a real cell of
   ground. Correct by construction, worth knowing before a mask is drawn for this base.
4. **The prototype renders the figure** (its forked `Hero.show` reaches the same `draw_numeral`)
   **and needs nothing else**, because this base paints no ground — unlike flap. Pass 36's open
   item 1 is therefore not made worse by this pass, and it is not fixed by it either.
5. **`HERO_FONT` still has no metrics table of its own** (pass 36's open item 3, now with a third
   consumer). The `1` correction is a per-base patch for the third time, which is honest and is
   also the signal that the font wants the `naught.METRICS` treatment.
6. **The hero is still a small mark in a wide field** — pass 36's open item 5, the pre-existing
   `dot` composition, not this pass's.
7. **`RUN.md` still advertises `verify_language` at 356 checks** — stale since the twenty-eighth
   pass, outside the file budget for the fourth time.
8. **The skill's `COMPONENTS.md` owes the display-type note** (the base as stroke logic; and now
   the finding that a language's own glyph law can rule a whole glyph family out of its display
   type) — outside this worktree.

**Artifacts (`prototypes/out/`, outside the file budget):** `_spec37.py` / `_spec37.txt` (**the
specimen: 0-9 through the stencil, the banks, the bridged/bridgeless columns, the four drawn bases
side by side, the thick-stroke control and the mascot — this pass is judged by eye and that is the
file to look at**) · `_probe37.py` / `_probe37.txt` (the hero at five seats, the per-digit metric
table, the tabular evidence, the bridge table, the glyph-vocabulary audit) · `_cmp37.py` /
`_cmp37.txt` (the drawn base beside the `plain` posture it replaces, same seat) ·
`aperture_blueprint_hero.txt` (written by the suite, the SHIPPED band) · `_run37_{0,1,2}.txt` (the
three runs; run 1's first attempt is the darkside race and was rerun).

**Done 2026-07-27 (thirty-sixth pass) — THE DRAWN DISPLAY TYPE FOR LEDGER AND SOLARI: `slab` and
`flap`, and the finding that both are PIXEL BASES rather than hero branches.** Two languages stop
borrowing `hero="plain"` and start drawing. Eight of ten languages now render a hero of their own;
blueprint's stencil and swiss's deliberate renunciation are what is left.

**THE DECISION THAT MADE THIS ONE PASS INSTEAD OF TWO, and it is the load-bearing one.** The brief
called slab and flap "a new stroke logic in the hero pipeline". Measured against the code, the
pipeline already had the seat: `hero="dot"` draws `BS.draw_numeral(val, st["base"], HERO_FONT)`,
so the difference between an engraved figure and a flap card is entirely **what a lit pixel turns
into** — which is `bases.py`'s job and LANGUAGES.md's own definition of the pixel base ("a
language's shape scale"). Neither language needed a hero branch; both needed a base. That single
choice is why the file budget held, and it bought something a new branch could not: **the
widget-slice prototype's forked `Hero.show` reaches the same `draw_numeral`, so the prototype
renders the SAME FIGURES without app.py being touched** (it renders them without the flap's face
ground — see the cost list).

**`slab` (ledger) — the engraved figure, and what makes it typography rather than a fat bitmap.**
Every other base draws one mark per lit pixel. This one asks what the pixel is FOR:

- a pixel with ink above or below is a **stem** — two cells of `█`;
- a pixel with ink only beside it is a **hairline bar** — a half block (`▀` above the waist, `▄`
  below), so a horizontal reads at HALF a stem's weight. This is measured, not stylistic: a
  terminal cell is ~1:2, so one ROW is already as thick as two COLUMNS, and drawing a bar
  full-cell would make the horizontals the heaviest strokes in the figure — the opposite of a
  slab. The bar hugs the outside of the glyph, which keeps the counters as open as the mask allows;
- a stem landing on the **baseline** grows **serif feet** — half-pixel flares left and right of
  its foot's run. `0 3 5 6 8 9` get none, because their bowls close above the baseline and there
  is no stem to stand on. That is what a real slab face does, and it is also the control that the
  flare is conditional rather than sprayed on every glyph — **asserted in both directions against
  the same digit drawn through `block2`.**

**`flap` (solari) — the card, and the hinge that must not erase what it cuts.** Two-cell blocks,
seven rows, cut at row 4 by a SEAM that crosses the whole face: `▔` where the face is bare, `▀`
where the numeral passes through. Both hug the top of the seam row, so they form ONE line that
thickens over the ink. **The first design drew the seam as a full rule and the counter law caught
what that costs: it takes the waist off the `8` and leaves it identical to the `0`.** The shipped
form keeps the waist and is asserted to (`drawn('8')[seam] != drawn('0')[seam]`). The seam is a
SHAPE before it is a colour, which is why the prototype — which paints no face — still renders a
flap board.

**Per-digit metrics, MEASURED on the rendered form** (`_probe36.txt`), the pass-35 discipline
applied to two new bases:

| | slab ink cells | slab aspect | slab counter/ink | flap ink cells | flap aspect | flap counter/ink |
|---|---|---|---|---|---|---|
| `0` | 8 | 0.57 | **0.50** | 8 | 0.57 | **0.50** |
| `1` | 10 | 0.71 | — (open) | 8 | 0.57 | — (open) |
| `2` | 10 | 0.71 | **0.40** | 8 | 0.57 | **0.50** |
| `3` | 8 | 0.57 | **0.50** | 8 | 0.57 | **0.50** |
| `4` | 9 | 0.64 | **0.44** | 8 | 0.57 | **0.50** |
| `5` `6` `8` `9` | 8 | 0.57 | **0.50** | 8 | 0.57 | **0.50** |
| `7` | 8 | 0.57 | — (open) | 8 | 0.57 | — (open) |

**Two things in that table are worth saying out loud.** First, **slab's aspect bracket has real
spread (0.57 to 0.71) where the alphabet's had none** — pass 35 recorded that its own [0.55, 0.80]
check was "a weak check dressed as a range" because a 4-column box produces exactly 0.80. Here a
serif foot widens the figure and a bowl does not, so the bracket is measuring something. Second,
**flap's counter is measured with the hinge counted as UNLIT**, because `▔` is drawn face, not
ink — the same reading naught's lattice already gets for its dark dots. Counted as ink, the `4`
reads 0.20 and the measurement would be lying about a hole that is plainly there.

**THE TABULAR `1`, and why the correction is per-BASE.** `HERO_FONT`'s `1` inks 3 of the 4 columns
it advances — aspect 0.43 at 7 rows, under the 0.55 floor. The font is shared with instrument and
nord, whose heroes must not move, so `bases.BASE_GLYPH` gives slab and flap their own `1` with a
full-width base bar and nobody else's changes. `bases.BASE_GAP` does the same for the inter-glyph
gap (2 columns, so a serif foot has ground to flare into and two cards do not merge). Both are
read by `draw_numeral`, which is the ONE seat both call sites share.

**BYTE-IDENTITY FOR THE OTHER EIGHT IS PROVED BY UNREACHABILITY, not by a stored baseline — and
that is the stronger form.** There was no hero dump to diff against (pass 35's `_sig35_post.txt`
is a KIT dump). So the suite empties `BASE_GLYPH` and `BASE_GAP` at runtime and asserts that
**every language whose base is not slab/flap renders byte-identically, while ledger and solari
move.** Ten checks, one per language, and the probe restores what it borrowed. Separately, the
kit signature dump was re-run unmodified: **all TEN kits are TEXT-IDENTICAL to pass 35, ledger and
solari included** (`_sig36_post.txt` vs `_sig35_post.txt`, 1125 lines, **0 changed**) — the `base`
token reaches no kit surface here, because both languages already override `mascot` and `wordmark`.

**THE FACE IS A GROUND, and that forced this pass to leave the prototype for the first time.** A
card's face cannot be carried by a glyph, so `hero.flap_paint` emits real `[fg on bg]` runs — and
the only composited seat that runs `taskboard/hero.py` is the SHIPPED aperture (`aperture.py`).
The widget-slice prototype forks the style dispatch (pass 35's open item 3) — **[CLOSED, forty-
fourth pass]**. So the suite gained
`capture_ap_bg()`: the real `TaskboardApp`, `6`, the language set, `settle()`, and the same
per-cell `(fg, bg)` map `capture_bg` builds. **Measured on the shipped frame: 6 of the figure's 7
rows stand on the `flap` ground, exactly 1 is the `seam` band, and it is the row the base
declared; face and band are the same width; ledger's hero has ONE ground under all of it and no
face anywhere.**

**A COLOUR DEFECT THE RENDER CAUGHT, and it is why the hinge line is `mut`.** The first version
drew the seam in the `seam` token, which is what the brief asked for. Measured: `seam` (#1f1f22)
against the face (#17171a) is **1.06:1 — invisible**. `seam` is defined one step off the GROUND,
and a lit face is not the ground. So `seam` is spent where it can be seen (the band the hinge row
is painted on) and the LINE on it is `mut`, **3.2:1**. Both are asserted on the markup and again
on the composited frame, and the two must agree.

**ONE CHECK REPLACED, and the replacement is stronger.** "solari @60: not one bar or braille glyph
on the widget posture" scanned the whole frame — sound while solari's hero was `plain`, wrong the
moment it DREW, because a numeral built out of block glyphs is TYPE, not a bar. (The board-region
form of the same law already scoped itself to the seam grid for exactly this reason.) It is now
asserted with the display type taken away (`hero` mutated to `plain`: not one bar survives, so the
QUANTITY mechanism is still digits) plus the harder claim that **every bar-family glyph on the
real posture belongs to the flap vocabulary** — nothing else on the screen drew one.

**A PROBE THAT HAD THE SEVERITY LAW BACKWARDS, reported because it is the finding.** The first
app-level check asserted "a calm ledger hero carries zero red" and went RED. The fixture is
genuinely overdue (its queue reads `2d!`), so the ledger headline IS debt and the red pen is
CORRECT there. The law is a pair and both halves now exist at the level that can answer them: the
CALM half at draw level, where the tone is an argument (`calm` tone → zero alert, zero amber;
`alert` tone → the figure wears it), and at app level the claim a composited frame can actually
make — **every ink on the figure comes from the severity ladder and nowhere else**, plus the
ration never reaching PASSIVE STRUCTURE (no card face and no hinge band is amber, whatever the
reading's severity). `_fixture_calm.json` was tried and rejected for this: it is calm for the
BOARD (nothing overdue, which is what blueprint needed) and still drives this hero to WARN.

**Counts: verify_language 1593 → 1772 (+179), 3 of 3 BACK-TO-BACK GREEN** (`_run36_{0,1,2}.txt`,
rc=0, ALL PASSED ×3, 1772 checks each; **the darkside race did not fire**, which is not evidence
it is gone). **0 checks removed; 1 replaced** (the solari @60 bar scan, above). The 179: the type
level for both bases (the tabular/advance contract with its gap control, the counter floor per
closed glyph with a 3-column negative control through the same base, the aspect bracket per digit,
the row height), slab's stroke-contrast and per-digit foot test with `block2` as the footless
control in BOTH directions, flap's hinge (position, full-face coverage, no leak to other rows, the
waist that survives, the face geometry), the draw level (dispatch on `hero` AND on `base`,
severity, five width classes each, the face/band/hinge markup, `flap`/`seam` mutation), the
ten-language unreachability control, and the shipped-aperture section.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** (ledger h=7, solari h=9,
both inside the 12-row budget) · `verify_widget` **ALL PASSED**, redraw **1371 µs = 8.23 %** of a
60 fps frame · `verify_board` **ALL PASSED** · `pytest tests` **137 passed**. verify_language
settle headroom worst **4 of 40 over 75 captures**.

**THE ONE REAL COST, measured and named: ledger renounces its hero CAPTION at the board seat.**
`Ledger.composition()` pins `Screen.sz-board #hero { height: 7 }` — its own commitment, written
when the plain hero was four rows — and the drawn figure is exactly 7 rows, so "DAYS OVERDUE" is
clipped. This is the same shape of fact as naught's drawn caption (pass 23: needs 13 rows, no
composition gives more than 11), and curing it means `language.py`, outside this file set. It is
**asserted rather than left to rot** (the check states the renunciation and its cause), and the
WIDGET seat is asserted to bring the caption back, so the loss is one composition's and not the
base's. Solari has no such pin and keeps its caption at every seat.

**Judged by eye, which is the acceptance bar** (`_cmp36.txt`, the same 59×7 seat both ways). The
posture being replaced printed `DAYS OVERDUE` / `12` / `backlog - 3 open` as **cell text** — a
hero that LABELS its metric, which is the one thing HIERARCHY.md says a hero must not do. Both
drawn forms read as what they claim: slab as engraved bookkeeping figures (feet visible on `1 2 4
7`, counters open, horizontals visibly lighter than the stems), flap as a bank of departure cards
(one card per digit, ground between them, the hinge continuous across each). Neither reads worse
than what it replaced, so both halves shipped.

**Open after this pass, each with why it was not taken.**

1. **THE PROTOTYPE RENDERS THE FIGURES BUT NOT THE FACES.** `prototypes/widget_slice/app.py` has
   its own copy of the style dispatch, so its `dot` branch reaches the same `draw_numeral` (same
   shapes, byte for byte) but never calls `flap_paint` — solari's cards there are unlit. This is
   pass 35's open item 3 with two more consumers, and app.py was outside the file set.
   **[CLOSED, forty-fourth pass: the prototype's faces are painted and measured.]** Everything
   the faces claim is measured on the SHIPPED aperture instead, which is the seat that matters.
2. **Ledger's board-seat caption** (above) — needs `language.py`.
3. **`HERO_FONT` still has no metrics table of its own.** Pass 35 measured it (4 ink columns, 7
   rows, counter 0.50, aspect 0.57) and left it alone; this pass measures the two bases it feeds
   but does not give the font the `naught.METRICS` treatment. The `1` correction is a per-base
   patch (`BASE_GLYPH`), which is honest but is a second place a glyph can be declared.
4. **Slab's `2` sits exactly on the 0.40 counter floor** and its diagonal is drawn as two isolated
   hairline pixels (the mask gives them no vertical neighbour), so it is the lightest figure in
   the set. Visible in `_spec36.txt`; not cured, because curing it means editing the shared font.
5. **The hero is still a small mark in a wide field** — at 118 the figure is ~22 cells of ~60.
   That is the pre-existing `dot` composition (nord and instrument have it too), not this pass's.
6. **`RUN.md` still advertises `verify_language` at 356 checks** — stale since the twenty-eighth
   pass, and outside this pass's file budget for the third time.
7. **The skill's `COMPONENTS.md` owes a display-type note** (the base as stroke logic, the
   stem/hairline contrast, the hinge-that-does-not-erase law) — outside this worktree.

**Artifacts (`prototypes/out/`, outside the file budget):** `_spec36.py` / `_spec36.txt` (**the
specimen: 0-9 through both bases, plus the banks `12 07 3 18` — this pass is judged by eye and
that is the file to look at**) · `_probe36.py` / `_probe36.txt` (the heroes at five seats, the
per-digit metric tables above, the tabular evidence, and the footless control) · `_cmp36.py` /
`_cmp36.txt` (the drawn base beside the `plain` posture it replaces, same seat) · `_apshot36.py` /
`_apshot36.txt` (the SHIPPED aperture with its per-row ground map) · `aperture_ledger_hero.txt` /
`aperture_solari_hero.txt` (written by the suite) · `_sig36_post.txt` (the kit dump, 0 lines
changed against `_sig35_post.txt`) · `_run36_{0,1,2}.txt` (the three runs).

**Done 2026-07-27 (thirty-fifth pass) — THE METRIC-BEARING NUMERAL ALPHABET (Bodmer P1): the
drawn alphabet stops being a uniform 3x5 box and starts carrying PER-GLYPH METRICS, with
TABULAR digits and counters wide enough to read.** No new language; this is a typographic
correction to the one alphabet all the drawn type in the set is made of.

**THE DEFECT, as a number rather than an impression.** A terminal cell is ~1:2, so a glyph N
columns wide by M rows reads at a visual aspect of N/(2M). The dense standard from passes 23-24
(sx=2, dot_w=1, gap=0, full-bleed unlit fill) put every glyph on a 3-column box, which is aspect
**0.60** against Bodmer Font16's **0.70** reference — and the narrowness landed where legibility
actually dies, on the **COUNTER**. A closed figure's counter was ONE column: **2 cells of a
6-cell glyph, 33% of the ink width, against the reference's 71%.** That is why `0`, `8` and `6`
were near-identical silhouettes at the head of a column. **Integer scaling can never cure it** —
`sx` multiplies stroke and counter together, so the ratio is invariant under the one axis the
previous two passes had.

**THE CONTRACT.** `naught.METRICS[glyph] = (ink_rows, ink_cols, advance)`, **MEASURED off the
masks by `_metrics()`, never declared**, and `ALPHA_ROWS` is now **DERIVED** (the tallest inked
row in the set) instead of the constant `5` it had been. `advance` is the glyph's own box plus
`GLYPH_GAP` — the distance from this glyph's origin to the next one's — and it is a **separate
number from the ink**, which is the whole point:

| class | ink_cols | advance | aspect at sx=2 | counter/ink at sx=2 |
|---|---|---|---|---|
| digits `0 2 3 4 5 6 7 8 9` | 4 | **5** | 0.80 | **0.50** (closed set) |
| digit `1` | **3** | **5** | 0.60 | n/a (open) |
| letters `A`-`Z`, space, `-`, `?`, `!` | 3 | 4 | 0.60 | n/a |
| period `.` | 1 | **3** | n/a | n/a |

Three distinct advances, so the table is a table and not a constant in a table's clothes. **All
ten digits share one advance including the `1`, whose ink is 3 columns inside a 4-column box** —
that is TABULAR figures, exactly what Font16 does (proportional text, monospaced digits), and it
is the thing a scale factor cannot express. **Measured consequence: the glyph that follows a
digit is BYTE-IDENTICAL whichever digit precedes it** (10 renders of `d8`, one distinct form),
with a negative control that the probe can see a shift (a period advances 3 and does move it).

**Per-digit numbers, measured on the rendered sx=2 form and not computed from the masks:**
counter/ink is **0.50 for every one of `0 4 6 8 9`** (4 cells of 8) against the floor of 0.40 and
the old form's 0.33; the aspect is **0.80** for the nine 4-column digits and **0.60** for the
`1`. **The bracket's ceiling, [0.55, 0.80], is EXACTLY what a 4-column box produces, so that
check has zero headroom above and is really the assertion "no digit is wider than its box".**
Said plainly because it is a weak check dressed as a range.

**THE `1` ALREADY HAD ITS BASE SERIF and this pass did not add one — what it added is the check.**
The old 3-wide `1` carried flag and foot; the honest new fact is that the foot now survives
*inside a digit advance* without the glyph being padded to 4 columns of ink, which is what a
per-glyph table buys. The serif check's first control was wrong and the render is what caught it:
"no other digit's bottom row is wider than its middle" went RED, because `2` and `3` also end on
a wide bar — the predicate was about bars, not serifs. It was **replaced** (not deleted) by the
same predicate run on a footless stem, which must go red and does.

**THE CHANGE COST TWO FILES OF CODE, and the reason is the interesting part: THE ADVANCE IS
CARRIED BY THE MASK WIDTH.** A digit's mask is 4 columns, a letter's 3, the period's 1, so
`BS.from_font(..., gap=GLYPH_GAP)` composes the metric boxes with **no signature change in
`bases.py` and no call-site change in `language.py`** — neither file was touched, and neither was
in the final set. `plain_width()` was rewritten to sum advances instead of multiplying a constant
4 by the character count, and it is **exact for letters by construction**, which is why every
letter-drawing seat is byte-identical.

**CONSUMERS RE-MEASURED, all of them, because a wider digit is a width budget spent:**

- **naught's column-head count sprites** — the seat the user actually reads. 6 rows at all five
  size classes (14 / 20 / 28 / 40 / 60), no wrap, no truncation, cards-per-column unchanged.
  **The x2 tier now costs 18 cells for two digits where it cost 14, so the progressive flip moved
  from w>=15 to w>=19** — asserted at the exact cell (19 buys x2, 18 refuses it), and the stale
  `SX2_MIN = 15` in the suite was corrected rather than left to pass by luck on a width set that
  happened to skip 15-18. Every TWO-digit count draws one width and every ONE-digit count draws
  one width, so **a board's heads never reflow because a count changed**.
- **naught's `sect()` drawn titles, naught's wordmark, `Kit.wordmark` (all ten languages) and
  `Instrument.sect`'s braille titles** — all letter-only seats, all **byte-identical**.
- **the hero (`naught7`)** — its caption wrap hardcoded `4 * sx` columns per character, which was
  a fork of the metrics that happened to be right only for letters. It now measures through
  `plain_width` (`hero._wrap`). For letter captions the result is identical by construction, and
  the suite's hero geometries (46x12, 54x11, 54x13, 60x8, 92x16, 118x12, 118x20) all still render
  the same rows. `verify_aperture` ALL PASSED — the 12-row wrap budget is untouched.

**Byte-identity, DIFFED AS TEXT** (`_sigdump32.py` re-run unmodified against `_sig34_post.txt`,
compared section by section by `_sigdiff35.py`): **9 of 10 languages TEXT-IDENTICAL** — corgi
3747 · instrument 3714 · swiss 2802 · industrial 3365 · nord 3324 · darkside 2113 · ledger 4982 ·
solari 3405 · blueprint 3903, every byte count matching the thirty-fourth pass's. **naught moved,
3305 -> 3585 bytes**, and the diff's scope was measured rather than asserted (`_sigscope35.py`):
322 changed lines, **280 of them pure lattice rows (the drawn count sprites) and the remaining 42
the identical `BACKLOG` caption line re-aligned around them — zero changed lines anywhere else.**

**Counts: verify_language 1560 -> 1593 (+33), 3 of 3 BACK-TO-BACK GREEN** (`_run35_{0,1,2}.txt`,
rc=0, ALL PASSED ×3; the darkside race did not fire, which is not evidence it is gone). **0 checks
removed; 1 replaced** (the serif control, above). The 33: the metrics table and its controls (5),
the counter floor per closed glyph (5) with the 3-wide form as a negative control on both (2), the
aspect bracket per digit (10), anti-jiggle plus its control (3), the serif plus its control (2),
the pass-23/24 density laws re-stated PER GLYPH so a single new digit can regress them alone (2),
and the head's exact flip cell plus its tabular width claims (4).

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** · `verify_widget`
**ALL PASSED**, redraw **1475 µs = 8.85 %** of a 60 fps frame · `verify_board` **ALL PASSED**
(headroom worst 5 of 40 over 62 settles) · `pytest tests` **137 passed**. verify_language settle
headroom worst **4 of 40 over 71 captures**.

**Open after this pass, each with why it was not taken.**

1. **LETTERS STAY ON A 3-COLUMN BOX (aspect 0.60), deliberately.** This increment is the
   NUMERALS. Widening letters moves the width budget of every drawn-title seat at once —
   `Naught.sect`'s `w - 2`, `Instrument.sect`'s `len(bm[0]) // 2 <= w - 10`, and `Kit.wordmark`
   through seven pixel bases — and none of those was measured here. It is a pass of its own.
2. **`Kit.wordmark` and `Instrument.sect` reach the alphabet through `BS.from_font`'s uniform
   gap, not through `plain_width`.** For letters the two routes are identical by construction
   (3 ink + 1 gap = the letter advance), which is why they are byte-identical — but a digit in a
   wordmark would draw non-tabular. Cheapest cure is to route both through one naught helper;
   `language.py` was outside the final file set.
3. **`prototypes/widget_slice/app.py` still holds its own copy of the `naught7` branch**, wrap
   arithmetic and all, including the `4 * sx` per character this pass deleted from `hero.py`.
   Letters-only today, so it renders the same; it is the same fold the closing note already owes
   ("fold the prototype Hero's drawing onto `taskboard/hero.py`").
4. **`HERO_FONT` (the 4x7 hero numeral) is a SEPARATE font and was left alone.** Measured for the
   record so the decision is not a guess: 4 ink columns, 7 rows, counter 2 columns -> at the
   hero's own x2 the counter is 4 cells of 8 (**0.50**) and the aspect is 8/14 (**0.57**). It is
   already inside both laws this pass wrote, which is exactly why it was not touched — and it has
   no checks of its own yet.
5. **The aspect ceiling has no headroom** (above), and the counter measurement is HORIZONTAL —
   the widest interior unlit run with ink on both sides in the same row. It does not prove the
   counter is enclosed vertically, which is why the check runs on a DECLARED closed set
   (`0 4 6 8 9`) rather than on whatever a predicate happens to find.
6. **The skill's `COMPONENTS.md` owes a metrics-contract note** (ink vs advance, tabular figures,
   the counter floor) — outside this worktree, so outside this pass.
7. **`RUN.md` still advertises `verify_language` at 356 checks.** Stale since the twenty-eighth
   pass; it was outside this pass's file budget.

**Artifacts (`prototypes/out/`, outside the file budget):** `_probe35.py` / `_probe35.txt` (the
metrics table, the per-digit counter and aspect measurements, the tabular evidence, and the head
and hero renders the consumers were re-measured on) · `_spec35.py` / `_spec35.txt` (**the
specimen: 0-9 at sx=2, old 3-column box beside the new metric box — this pass is judged by eye
and that is the file to look at**) · `_sig35_post.txt` (the byte-identity dump) · `_sigdiff35.py`
and `_sigscope35.py` (the text diff and the scope measurement) · `_run35_base.txt` (the 1560-check
baseline taken before any edit) · `_run35_{0,1,2}.txt` (the three runs) ·
`lattice_naught.txt` (naught's board frame, rewritten by the suite — the heads read 7 / 6 / 2).

**Done 2026-07-27 (thirty-fourth pass) — BLUEPRINT, the TENTH language: the cyanotype TECHNICAL
DRAWING, where the frame stops CONTAINING and starts MEASURING.** Set is now **10 of the
design's 12**. It is the first language in the set whose whole frame budget is spent in ONE
place — a title block docked to the bottom corner — and the first whose emphasis is a KNOCKOUT
rather than a hue.

**What blueprint is, in one sentence each.** Quantity is a DIMENSION SPAN (`├─ 03D ─┤`) with the
figure standing on the span, drawn on a scale that is a declared CONSTANT; an item lies on an
open FIELD and hangs its metadata off an EXTENSION LEADER (`·── PROJ ── BACKLOG ── HIGH`);
nothing anywhere is boxed; held work is HATCHED rather than coloured; and the sheet's one
KNOCKOUT — a reverse-video plate in the title block — is the first fixation, which is why the
palette carries almost no chroma at all.

**The 118×30 board, verbatim** (`prototypes/out/sheet_blueprint_118.txt`, the late fixture,
trailing air trimmed):

```
  WORK ├ 02/15  13% ─┤
  ├─ 09 ─┤ ├───┤ 04 ├─┤ 02 LOAD

   DIM 2 ── NEAREST   OVR 2 ── OVERDUE   WIP 4 ── WORK IN   ╱╱ 1 ── BLOCKED    DAY 3 ── WORKDAY

  BACKLOG                                                                       ├─── 09 ───┤
   FIX CHECKOUT 500 ERROR                                                       ├╱╱╱╱ HELD ╱╱╱╱┤
   ·── WEBSITE REDESIGN ── BACKLOG ── HIGH
   COMPRESS DATABASE BACKUPS                                                    ├─┤ 01D!
   ·── DATA WAREHOUSE ── BACKLOG ── NORM
   RENEW TLS CERTIFICATE                                                        ├───┤ 03D
   ·── BACKLOG ── HIGH
   WRITE API REFERENCE                                                          ├ 05D ┤
   ·── API PLATFORM ── BACKLOG ── NORM
  ┌     ┐                                    ──────────────────────────────────────────────────
   BOARD  lanes  agenda  gantt               SHEET TASKBOARD  REV 2026-07-27  WORK 02/15  ├ OVERDUE ┤
  └     ┘                                    ──────────────────────────────────────────────────
```

**And at 80** (`sheet_blueprint_80.txt`) — the title block sheds its SHEET cell, the spans keep
their scale, and every title still reads whole:

```
  BACKLOG                                                 ├─── 09 ───┤
   FIX CHECKOUT 500 ERROR                                 ├╱╱╱╱ HELD ╱╱╱╱┤
   ·── WEBSITE REDESIGN ── BACKLOG ── HIGH
   COMPRESS DATABASE BACKUPS                              ├─┤ 01D!
   ·── DATA WAREHOUSE ── BACKLOG ── NORM
   RENEW TLS CERTIFICATE                                  ├───┤ 03D
   ·── BACKLOG ── HIGH
  ┌     ┐                              ───────────────────────────────────────
   BOARD  lanes  agenda  gantt         REV 2026-07-27  WORK 02/15  ├ OVERDUE ┤
  └     ┘                              ───────────────────────────────────────
```

**"NO CONTAINING BOXES" IS A MEASUREMENT HERE, NOT AN IMPRESSION, and that is the load-bearing
idea of the pass.** The law is stated as a VOCABULARY: every box-drawing codepoint is in scope,
and this language is allowed exactly TEN of them — `─ ━ ├ ┤ ╌` (the dimension line at two
weights, the two terminators, the clip break), `┌ ┐ └ ┘` (registration marks) and the hatch.
Not one of the ten is a vertical stroke or a junction, and a rectangle needs one or the other,
so a box on this sheet is not merely absent — it is **unconstructable**. The check scans every
kit surface at seven widths and the live board region at two, and it has a negative control:
the same predicate names stray glyphs on every other language's card.

- **`themes.py`**: a `blueprint` entry, plus **two new tokens** — `hatch` (the stroke a held
  span is filled with) and `knockout` (emphasis reverses to a pale ground). Both documented in
  the module's token list, both read by the renderer, both mutation-tested. `frame="titleblock"`
  and `layout="field"` are documented as new values of existing tokens.
- **ONE GEOMETRY SEAT: `Blueprint.field(w) -> [(origin, code, width)]`**, read by the card, by
  the HEAD and by every acceptance check (the `Ledger.cols` / `Swiss.grid` / `Nord.panes` /
  `Instrument.reticle` / `Corgi.slots` / `Solari.fields` precedent). It is what puts a phase's
  load span and its items' due spans in the same column, which is what makes the page read as
  one drawing rather than as a list with decorations.
- **THE SHARED SCALE IS A DECLARED CONSTANT, and that is DATAVIZ law 2 solved for a mechanism
  whose caller cannot pass a `hi`.** A kit method is handed one row at a time and can never see
  its siblings' maximum, so self-normalizing would make every span on the page a lie. The
  ceilings (`SCALE_DAYS = 14`, `SCALE_COUNT = 12`) are constants, and the check proves what that
  buys: **the same quantity draws the same length at 118, 96, 60, 44 and 38 cells.**
- **CLIP AND FLAG, NEVER CLAMP.** Past the scale the run stops and its first cell becomes a
  BREAK (`├╌─── 40D ─────┤`), so an off-scale span says so and the figure on it stays the truth.
  Asserted at the cell: 40 days and 90 days draw the same LENGTH and different FIGURES.
- **THE LABEL RIDES ON THE SPAN — and steps outside it when the run cannot letter it**, which is
  what a draftsman does with a dimension too small, and is asserted in both directions.
- **THE DECLARED DEGRADE, in two steps and no more**, asserted at the exact cell: **38 cells buy
  the dimension field, 37 renounce it whole** (the reading moves onto the extension leader — the
  sheet loses a dimension, never the datum, and the head keeps its count so an empty phase still
  reads `00`), **20 keep the sheet, 19 renounce it** and the row falls back to the generic card
  byte for byte. A span is never squeezed: a run shorter than its own terminators measures
  nothing.

**THE KNOCKOUT IS THE TITLE BLOCK'S STATE CELL AND NOT THE MOST OVERDUE ITEM, which is a
deviation with a mechanical reason rather than a preference.** A kit method is handed one card
at a time and has no cross-card knowledge, so "the single most urgent item" cannot be identified
without ranking the cards in `kanban.py` — the exact shape of nord's selection problem, and
`kanban.py` was outside this pass's file set. The one seat that DOES see the whole board is
`Kit.mood`, which the app computes from the real task list (anything overdue and not done), and
the title block is where it lands. **Measured on the composited frame with `capture_bg`: exactly
ONE reversed cell run on the view at 118 and at 80, and ZERO on a fixture with nothing
overdue** — the knockout means attention, so a calm sheet carries none and still states its
condition.

**AND THE KNOCKOUT CARRIES TWO CHANNELS, because reverse video alone is a colour.** Under the
token the state is DIMENSIONED — `├ OVERDUE ┤`, a real span with the word riding on it — and the
reverse is then spent on attention alone. Without the shape channel the knockout would have been
invisible to every greyscale check in the suite, which is COMPONENTS.md's two-channel law
applied to the one element this language exists to make unmissable. It is also what keeps
`knockout` out of dead metadata: `kit_sig` builds a fresh kit whose mood is always `"clear"`, so
a mood-gated token would have mutated to no visible change.

**THE TITLE BLOCK COSTS THE FIELD NOTHING, and it is measured both ways rather than argued.**
The block is THREE rows docked to `#ap`'s bottom where the mode strip it replaced was two
(`margin-top: 1` plus one content row), so it is one row dearer; `#kb` gives up its own
`margin-top` to pay for exactly that row, and the argument is not a density wish — `.col-head`
already spends a row of air ABOVE itself (where it groups features instead of separating a head
from its items), so `#kb`'s margin would stack a second blank row on the first. **Measured: the
board region is 10 rows with the title block and 10 rows under the generic composition**
(`capture_styled`, the same fixture, `frame` mutated to take the dock away).

**THE MODE STRIP SURVIVES, and it is where the registration marks live.** NAVIGATION.md tier 1
says nothing is discoverable until you show it, and the corgi pass measured what renouncing the
strip costs. The block keeps all four modes and marks the one on screen with `┌ ┐` above and
`└ ┘` below — four separate corners that never join, so the selection mark is not a border and
not a box. Asserted for every mode: exactly four marks, one of each, bracketing the active word,
with the cells between them blank on both rows, and moving when the selection moves.

**THE TITLE BLOCK'S DECLARED DROP ORDER**, `("sheet", "rev", "work")`, asserted at the exact
seat width: **114 buys four cells, 76 buys three, 56 buys two, 42 buys one.** STATE never drops,
because STATE is the knockout. Below that the strip degrades in two further tiers (modes the
sheet is not on, then the strip entirely) — the block is the sheet's identity and is not cut for
a nav row.

**HOW THE BLOCK KNOWS ANYTHING ABOUT THE BOARD, stated because it is the one indirect thing in
this language.** `tabs()` is handed only the mode list, so the block reads its tally and its
measure from `meter()` — the ONE call the app makes with the board's whole tally and with the
aperture's content width, and the call `app._after_hero` makes immediately before it. This is
the `self.mood` precedent (render-pipeline state on the kit), it is declared, and it degrades
honestly: before the first meter call the cell reads `--/--` and the block falls back to its
narrowest live seat. Asserted from both ends — the block's figure equals the meter row's on the
live render, and the `--/--` form is asserted on an un-driven kit.

**THREE DEFECTS THIS PASS FOUND, all of them by LOOKING at a render or by a check refusing to
stay green.**

1. **The instrument reticle checks were single-GLYPH tests, and they were wrong, not merely
   narrow.** Both asked for `Instrument.ORIGIN` — `├` — and nothing else. That glyph is also a
   dimension terminator, so a language with no scope, no axis and no trace in it went red on
   two checks. Widened to the reticle SIGNATURE (an origin carrying its week ticks, or a trace
   hanging its graticule off one), with a negative control on instrument's own board so the
   widening cannot be a weakening, and a second control naming the collision explicitly.
2. **The calm board caught a red `OVR` standing beside a count of ZERO.** `icon("overdue")` was
   painting the alert hue on a LABEL — the hue meaning "this word is about lateness" rather than
   "this thing is late" — and it was the only alert cell on the whole calm frame. No icon is
   alert now; the ration is spent on the span of a row that is genuinely past its date, and the
   check that used to bless the icon was replaced by one that forbids it plus a negative control
   that the hue is not simply unused.
3. **The render at 60 caught the calendar's `over` and `multi` differing by COLOUR ALONE** (the
   same glyph pair in two hues). All four day states differ in shape now, and the two-channel
   law has a check on that seat.

**Counts: verify_language 1294 -> 1560 (+266), and every step of the arithmetic was MEASURED on
a run rather than hand-counted.** Adding the language and nothing else took it to **1381 (+87
with no new check written)** — the pairwise, per-language and mutation loops all read `TH.ORDER`,
so a tenth language scales them on its own. Then: the **kit-level blueprint section plus the two
widened instrument checks and their controls, +119** (1381 -> 1500); the **app-level section,
+58** (1500 -> 1558); the **calendar two-channel pair, +2** (1558 -> 1560). **0 checks were
removed**; three were REPLACED by stronger forms (the two instrument leak predicates, and the
"RED reaches exactly one icon" assertion that the render proved was blessing a defect).

**Runs: 1560 checks, 3 back-to-back — 2 of 3 ALL PASSED, and the third was the darkside race**
(`_run34_0.txt` … `_run34_2.txt`). Run 2 failed with the characterized 4-check signature
(`0 row(s)`, no settle timeout at its capture); **rerun once, ALL PASSED**, and `_run34_2.txt`
holds the rerun. The watch stays open and unexplained. Settle headroom worst **4 of 40 over 71
captures**.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** (the cycle checks
read `ORDER`, so 9 -> 10 needed only the docstring; blueprint's hero is 7 rows, inside the
12-row wrap budget) · `verify_widget` **ALL PASSED**, redraw **1878 µs = 11.27 %** of a 60 fps
frame (**1328 µs = 7.97 %** on an earlier run of the same code — the spread is this probe's own,
and both numbers are printed here rather than the flattering one) · `verify_board` **ALL
PASSED** · `pytest tests` **137 passed**.

**Byte-identity, DIFFED AS TEXT this time and not as byte counts** (`_sigdump32.py` re-run
unmodified, output compared section by section against `_sig33_post.txt`): **9 of 9 pre-existing
languages are text-identical** — naught 3305 · corgi 3747 · instrument 3714 · swiss 2802 ·
industrial 3365 · nord 3324 · darkside 2113 · ledger 4982 · solari 3405. blueprint is 3903. The
only shared code this pass touched is one `if mech == "dimension"` branch each in
`spark`/`plot`/`gauge`, one `LIN` row and one new `METERS` entry, all unreachable for a language
that does not declare the token.

**NO SIDE EFFECT IN THE SHIPPED APP, and it was checked rather than assumed.** `aperture.py`
injects `kit.tcss()` app-wide, which is how corgi's margin reclamation reached the product. Every
selector blueprint's composition emits (`#tabs`, `#kb`, `.col-head`, `.kb-card:focus`,
`.tile:focus`) was grepped against `taskboard/taskboard.tcss` and `taskboard/aperture.py`: none
of them exists outside the prototype's widget tree. The aperture mounts `#hero`, `#meter`,
`#tiles`, `#ap-panel`, `#ap-foot` and nothing else.

**Measured, and reported because they are costs.**

1. **THE SHEET SHOWS 4 ITEMS OF 15 AT 118×30**, which is the thinnest density in the set. Two
   rows per item (the item and its leader) plus one row of air above each head, against a board
   region of 10 rows. The leader row is not negotiable — it is the language — and the title
   block is already free. **The honest cure is not layout, it is the app**: the board region is
   10 rows out of 30 because the hero holds 9 it barely uses, which is `hero.py`. Solari
   reported the same shape of cost and bought its rows by reclaiming `#meter`/`#tiles` margins;
   blueprint did not, because it has no argument of its own for taking them and borrowing
   another language's is how a set stops being ten languages.
2. **THE HEAD'S SPAN STANDS ONE CELL OFF ITS ITEMS' SPANS**, and the cell is `kanban.py`'s: the
   head is handed `avail - 4` while a card sizes itself from its own content box (**PENDING item
   4, now a SIXTH language**). Asserted bounded (`<= 1`) and printed, so a real drift fails.
3. **Blueprint has NO empty-state seat** — it is a sections language, and the sections branch of
   `kanban.py` is the one branch that never mounts `k.empty()`. **PENDING item 7 now covers SIX
   languages.** What it keeps is the head's own figure, which reads `00` on an empty phase.
4. **The 118-cell sheet has a ~60-cell void inside the item field**, the same surplus-width cost
   corgi and solari reported. A drawing sheet is genuinely airy, so it reads better here than it
   does there, but it is the same unspent measure — and it is where a second dimension (a start
   date, a phase age) would go if one were wanted.
5. **`hero` is `"plain"` and that is a posture, not a placeholder** — the swiss / ledger /
   darkside / solari position. The stencil hero (a drawn numeral in a hatched stencil field)
   needs `taskboard/hero.py`, which was outside this pass's file set.

**Deviations from the spec, each with its reason.** `sel="none"` instead of `sel="registration"`
(`sel` is emitted verbatim as a Textual BORDER STYLE and "registration" is not one — it would
raise on the stylesheet rather than render a mark; and a registration mark is not a border, which
is the point of it. Solari's `sel="band"` deviation, verbatim). `pitch=1` instead of `2` (the
air a pitch of 2 would spend is already spent, and spent better: the second row of every card IS
the extension leader, so the sheet annotates its white space instead of leaving it blank — at
pitch 2 a card would be three rows and the board would show three items). The leader is
`·── meta ── meta`, not the spec's `└─ meta ── meta` (the corner glyphs are reserved to the
registration vocabulary, and a leader borrowing one would break both the exactly-four-marks law
and the no-box law). The knockout is the title block's state cell rather than the most overdue
item (above). Registration marks bracket the MODE ON SCREEN rather than the focused card
(kit-level focus is unreachable without `kanban.py` — the nord precedent — so the deterministic
version shipped and the per-card version is named below). Motion `plot` and the stencil hero are
**out of scope** as briefed.

**Open after this pass:** (a) the **stencil HERO via `hero.py`** — the named follow-up, and the
one thing that would make blueprint's display type RENDER rather than borrow; (b) **per-item
registration marks and a per-item knockout**, both of which need `kanban.py` to rank the cards
(the nord precedent) — the deterministic versions shipped and are asserted for what they are;
(c) `motion="plot"` (the sheet drawn in, leader then span then figure) — cheap precomputed frame
motion, not attempted; (d) the density cost (1), curable only by giving the board region rows the
hero is not using; (e) PENDING item 7 is now **six** languages and item 4 is now **six**;
(f) the darkside capture race is unchanged and still unexplained — it fired once in three runs
here, which is inside its characterized ~1-in-12 and is not new evidence; (g) the set is
**10 of the design's 12**.

**Artifacts (`prototypes/out/`, outside the file budget):** `_probe34.py` (the frames the design
was read from, and the row-cost measurement made before the checks were written) ·
`sheet_blueprint_{118,80,60}.txt` and `sheet_blueprint_calm.txt` (the renders) ·
`_fixture_late.json` / `_fixture_calm.json` (**the two fixtures the standard seed could not
replace: its only past-due tasks are ALSO blocked, so the sheet hatches them and no row is ever
alert, and both sit below the fold at 30 rows**) · `_sig34_post.txt` (the byte-identity dump,
diffed as text against `_sig33_post.txt`) · `_run34_{0,1,2}.txt` (the three runs; `_2` is the
rerun after the darkside race).

**Done 2026-07-27 (thirty-third pass) — SOLARI, the NINTH language: the split-flap DEPARTURE
BOARD, where the board becomes ONE SCHEDULE and quantity is DIGITS instead of a bar.** The
first language added since the set was curated to eight, and the first whose identity is a
QUANTITY MECHANISM rather than a structure device: `meter="odometer"` states a figure where
the other eight draw a length. Set is now **9 of the design's 12**.

**What solari is, in one sentence each.** A task is a ROW; a phase is a GATE and the gate is
the reverse-video BAND that heads its block; the task's state is a WORD in a status column
(`ON TIME` · `BOARDING` · `LATE` · `HELD` · `DEPARTED` · `OPEN`); the days-to-due is an
odometer figure on a flap cell; and the `▁` seam under every row is the entire divider
vocabulary — no rules, no boxes, no frames anywhere on the surface.

**The 118×30 board, verbatim** (`prototypes/out/schedule_solari_118.txt`, trailing air
trimmed):

```
 GATE BACKLOG 07                                       STATUS    PROJ          PRI
 03  RENEW TLS CERTIFICATE                             BOARDING  --            HIGH
 ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
 05  WRITE API REFERENCE                               ON TIME   API PLATFORM  NORM
 ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
 08  SHUT DOWN LEGACY SERVERS                          ON TIME   LEGACY SUNS…  NORM
 ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
 09  DEPRECATE V1 ENDPOINTS                            ON TIME   API PLATFORM  HIGH
```

**THE DECISION THAT SHAPED EVERYTHING, and it was forced by a MEASUREMENT, not by taste:
SEVERITY IS THE CELL FACE, NEVER THE INK.** The first draft printed the status word in the
severity hue — `BOARDING` in amber, `LATE` in red — which is what every other language in
this set does. Then the selection band was measured off the composited frame
(`capture_bg`, new): the selected row's ground is amber, so a `#f5a300` word was painting on
a `#f5a300` ground at **1:1 — invisible**, and the calm fields came out at **1.8:1**.
Rewritten so that a boarding departure LIGHTS ITS CELL (an amber flap face with dark digits)
and every glyph on a schedule row is neutral (`ink · mut · dim · ground`). This is more
faithful — a flap board lights the row, it does not recolour the letters — and it is what
makes the band work: with no coloured foregrounds there is nothing an inverted ground can
hide. **Measured after: worst contrast on the selected row is 2.60:1** (`mut` on amber),
gated at 2.5 by a check that prints the offending glyph.

- **`themes.py`**: a `solari` entry, plus **two new colour tokens** — `flap` (the cell face,
  one step off the ground) and `seam` (the `▁`, this language's whole divider vocabulary).
  Both documented in the module's token list, both read by the renderer, both
  mutation-tested. `frame="flaps"` is documented as the one frame value that turns FACES on
  and rules OFF (`rule_line()` returns `None`). `band` now carries a documented second
  payload: ledger names the hex of its every-5th-line tint, solari names the MECHANISM
  (`"reverse"`) — a band is a ROLE, and naming it that way needs no surgery on the ALT
  table, which is why it beat the spec's `band=True` (a bool would have collided with
  ledger's hex flip and read as a dead token).
- **ONE GEOMETRY SEAT: `Solari.fields(w) -> [(origin, code, width)]`**, read by the row, by
  the band and by every acceptance check (the `Ledger.cols` / `Swiss.grid` / `Nord.panes` /
  `Instrument.reticle` / `Corgi.slots` precedent). It fills the measure EXACTLY at every
  width, which is a check rather than a claim.
- **THE DECLARED REFLOW DROP ORDER — the law this language exists to show.**
  `DROP = ("proj", "pri", "stat")`, read by the seat and asserted at the exact cell:
  **58 buys five columns, 57 buys four, 44 buys four, 43 buys three, 38 buys three, 37 buys
  two, 28 buys two, 27 renounces.** ITEM is never cut below `ITEM_MIN = 24` and no fixed
  field is ever squeezed — a narrow page sheds a whole column instead.
- **GATE IS NOT A COLUMN, against the spec's four**, and the reason is the corgi pass's own
  finding: under a sections board every row of a block shares one phase, so a GATE column
  would print the same word down the whole block — the constant-column defect. The BAND
  states the gate once, which is what a real flap board does.
- **THE DEGRADE HAD TO BE REWRITTEN, and the pairwise check is what caught it.** The first
  draft stopped the drop order at `("proj", "pri")` and let the row fall through to
  `super().card_rows()` below the floor. Measured: at 28 cells **solari rendered NORD's card
  anatomy**, and "no two languages share a card anatomy" went red. A language may renounce a
  COLUMN; it may not renounce being itself. `stat` joined the drop order and the narrow card
  keeps its digits and its seam.
- **THE ROW BUDGET, and it comes from the language's own law rather than a density wish.**
  widget.tcss spends `margin-top: 1` above `#meter`, `#tiles`, `#tabs` and `#kb`; under a
  language whose one statement about itself is "the seam is the only divider", a blank row IS
  a divider drawn in air. All four are reclaimed and exactly ONE row of air is given back to
  `.col-head`, where it groups GATES instead of separating rows. **Measured: the board region
  goes 10 rows to 14 at 30 screen rows, and the schedule prints 6 departures instead of 4.**

**Counts: verify_language 1033 -> 1294 (+261), and the total is what three back-to-back runs
printed, not a hand count.** The growth has two sources and both are named: the pairwise,
per-language and mutation loops all read `TH.ORDER`, so a ninth language scales them on its
own (**1033 -> 1119, +86, with no new check written**), and then the solari sections —
**kit level +129 · app level +46 = 175**. **0 checks were removed**; two generic ones were
REPLACED by stronger language-specific branches (the card-anatomy metadata assert, because
solari's second row is the SEAM and a constant by design — the metadata assert moved to row
1 at a width that bought the columns, and row 2 gained the harder claim that it is the
divider and nothing else).

**Runs: 1294 checks, 3 of 3 BACK-TO-BACK GREEN** (`_run33_0.txt` … `_run33_2.txt`): rc=0,
**ALL PASSED** ×3. **Zero settle timeouts, and the darkside race did not fire in any of the
three** — which is not evidence it is gone (it is ~1-in-12); the watch stays open. Settle
headroom worst **3 / 5 / 4 of 40 over 62 captures**.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** (the cycle checks
read `ORDER`, so 8 -> 9 needed only a docstring correction; solari's hero is 7 rows, inside
the 12-row wrap budget) · `verify_widget` **ALL PASSED**, redraw **1492 µs = 8.95 %** of a
60 fps frame · `verify_board` **ALL PASSED** (headroom worst 5 of 40 over 62 settles) ·
`pytest tests` **137 passed**.

**Byte-identity, measured with the THIRTY-SECOND pass's own instrument** (`_sigdump32.py`,
re-run unmodified): naught **3305** · corgi **3747** · instrument **3714** · swiss **2802** ·
industrial **3365** · nord **3324** · darkside **2113** · ledger **4982** — **all eight
match the byte counts that entry recorded, 8 of 8**. The only shared code this pass touched
is three `if mech == "odometer"` branches inside `spark`/`plot`/`gauge` and one `LIN` row,
all unreachable for a language that does not declare the token. Full dump kept at
`_sig33_post.txt` so the next pass can diff text rather than sizes.

**Measured, and reported because they are costs.**

1. **THE SEAM COSTS A ROW PER DEPARTURE.** A schedule row is two screen rows, so at 118×30
   the board shows **6 departures of 15 tasks** where the densest languages show 7-8 in the
   same band. The reclaimed margins bought 4 -> 6 and that is where the cheap rows ran out.
   The honest cure is not layout, it is the app: the board region is 14 rows out of 30
   because the hero still holds 3 blank rows it does not use, which is `hero.py`.
2. **THE BAND RUNS ONE CELL WIDER THAN THE SEAM ON THE LIVE BOARD — 110 cells against 109 —
   and the cell is `kanban.py`'s, not solari's.** The head is handed `avail - 4` while a card
   sizes itself from its own content box (**PENDING item 4, now a FIFTH language**). At kit
   level the law is EXACT and has a negative control (a band built one cell wider fails the
   same predicate). At app level what is asserted is what is true and load-bearing: every
   band shares one extent, every seam shares one extent, **the two CLOSE on the same cell**
   (which is the edge the STATUS/PROJ/PRI columns ride), and the left edges differ by at most
   one — printed, so a real drift fails. **The right-edge agreement is arithmetic luck, not
   design**: the head's extra cell of width exactly cancels its extra cell of origin. It will
   stop being true the day the board has no scrollbar.
3. **The 118-cell board has a ~50-cell void inside ITEM**, the same surplus-width cost corgi
   reported. A departure board is genuinely airy, so this reads better here than it does
   there, but it is the same unspent measure.
4. **Solari has NO empty-state seat** — it is a sections language, and the sections branch of
   `kanban.py` is the one branch that never mounts `k.empty()`. **PENDING item 7 now covers
   FIVE languages** (swiss · darkside · ledger · corgi · solari). What solari keeps is the
   band's own count, which reads `00` on an empty gate.
5. **The scrollbar and the seam share a glyph family.** Textual draws its thumb with the
   `▁▂▃…` ramp, so a bright thumb reads as a stray seam mark standing outside the grid — seen
   in the render at 118 before it was toned. It is now drawn in the `seam` tone at rest and
   lifts to full ink on hover / accent on drag, so the affordance is not renounced.
6. **`hero` is `"plain"` and that is a posture, not a placeholder** — the swiss / ledger /
   darkside position. The odometer hero (a departure figure flipped across a full-width bank
   of flap cells) needs `taskboard/hero.py`, which was outside this pass's file set.

**Deviations from the spec, each with its reason.** `sel="none"` instead of `sel="band"`
(`sel` is emitted verbatim as a Textual BORDER STYLE and `"band"` is not one — it would raise
on the stylesheet rather than render a band; the band is not a border in any case, which is
the point of it). `pitch=1` instead of `2` (pitch 2 puts a blank row between a seam and the
next row, so the page would carry two dividers and lose a third of its density — the same
argument as the reclaimed margins). `band="reverse"` instead of `band=True` (above). No
`base` token (solari renounces the mascot and overrides the wordmark, so a `base` would be
the dead metadata this codebase deleted `hero_gap` for). Riffle motion is **out of scope** as
briefed; `flip_frames` does carry the language's own settle (three precomputed frames landing
left to right), because that is the component library's contract and it costs nothing.

**Open after this pass:** (a) the **odometer HERO via `hero.py`** — the named follow-up, and
the one thing that would make solari's signature RENDER rather than borrow; (b) the seam's
row cost (1), curable only by giving the board region rows the hero is not using; (c) PENDING
item 7 is now **five** languages; (d) `kanban.py`'s head budget is now a **fifth** language's
workaround and the right-edge agreement above is luck; (e) the darkside capture race is
unchanged and still unexplained; (f) the set is **9 of the design's 12**.

**Artifacts (`prototypes/out/`, outside the file budget):** `_probe33.py` (the frames the
design was read from) · `_probe33b.py` (**the widths measured off the real widget tree — how
the stray `▁` was identified as the scroll bar rather than a wrap**) · `_sig33_post.txt` (the
byte-identity dump) · `schedule_solari_{118,80,60}.txt` and `probe33_solari_{118,80,flow}.txt`
(the renders) · `_run33_{0,1,2}.txt` (the three runs).

**Done 2026-07-27 (thirty-second pass) — CORGI's `layout="strip"`: the board becomes ONE
FULL-WIDTH SPEC SHEET under a numbered MODE STRIP, and the strip turns out to have been
rendering on NO SCREEN ROW AT ALL.** Step 8 of rolling `layout` out, and the last one:
**coverage is 8 of 8.** The gate ran first and it OPENED at 4 files; its reasoning is below,
because it is what shaped the design, and because it turned up a live defect nobody was
looking for.

**THE GATE, and its verdict.** The spec assigns corgi `layout="modes"` — "each mode takes the
whole screen; numbered params become a real strip". Read as APP-LEVEL modes (board/lanes/
agenda/gantt as full screens driven by a mode strip), that is not a kit-level change: the app
ALREADY swaps `#kb` and `#view` so exactly one mode is on screen, and the strip already has a
live seat (`#tabs`, fed `KIT.tabs(["board","lanes","agenda","gantt"], self.view)` from the
app's own view state, with `1`-`4` really bound to those views). **So the honest kit-level
version is the LARGEST one that still owns real mechanisms**, and it is what shipped:

1. **The mode strip becomes REAL** (`tabs`), and this is where the gate found something.
   Corgi's previous `tabs()` renounced the other three modes on purpose ("each mode takes
   over the screen — no persistent nav chrome"). **Measured on the 118x30 frame, it renounced
   more than that: `#tabs` is `height: 1` in `widget.tcss` and corgi's own `composition()`
   puts a `border-top` on it, so the aluminium rule ate the widget's ONLY content row.
   `[1] B O A R D` was in the renderable and on NO screen row, at any size, for as long as
   that composition has existed.** The strip was not minimal, it was invisible.
2. **The board becomes ONE full-width mode surface** (`board_layout` -> `sections`,
   `card_rows` -> a one-row param strip): the board mode really does take the screen.
3. **The row budget** (`composition`): the mode surface is paid for out of dead air.

**Before / after, the 80x30 board, verbatim** (`prototypes/out/probe32_flow_corgi_80.txt` vs
`probe32_corgi_80.txt` — 80 is the width that decides it):

```
  before (flow — three columns)                    after (strip — one spec sheet)
  [1] B A C K L O G  7   [2] D O I N G  6 …        [1] B O A R D [2]LANES [3]AGENDA [4]GANTT
  ───────────────────    ─────────────────         ──────────────────────────────────────────
                                                   [1] B A C K L O G  7
   [1] RENEW TLS CERTIF…3d  [1] FIX CHECKOU…blk    ──────────────────────────────────────────
       DUE 3D  PH BACKLOG       DUE -2D PH DOING    [1] RENEW TLS CERTIFICATE    DUE 3D    PR HIGH  ST OPEN
   [2] WRITE API REFERE…5d  [2] COMPRESS DA…blk     [2] WRITE API REFERENCE      DUE 5D    PR NORM  ST OPEN
       DUE 5D  PH BACKLOG       DUE -1D PH DOING    [3] SHUT DOWN LEGACY SERVERS DUE 8D    PR NORM  ST OPEN
   [3] SHUT DOWN LEGACY…8d  [3] DESIGN HOMEP…0d     [4] DEPRECATE V1 ENDPOINTS   DUE 9D    PR HIGH  ST OPEN
  (8 tasks, EVERY title cut,                        [5] ADD PUSH NOTIFICATIONS   DUE 18D   PR NORM  ST OPEN
   2 of 3 params, and the mode                      [6] PLAN Q3 ROADMAP          DUE --    PR NORM  ST OPEN
   strip is on no row at all)                       [7] UPDATE ONBOARDING COPY   DUE --    PR NORM  ST OPEN
                                                   [2] D O I N G  6
                                                   (7 tasks, every title WHOLE, 3 params
                                                    each, on one shared geometry)
```

**THE JUDGMENT ASKED FOR: yes, this reads more like a Teenage Engineering device**, and the
argument is not the glyphs, it is the two things the panel now has that it did not.
**A BUTTON ROW**: a TE panel shows its numbered buttons at all times and commits ONE SCREEN
to the mode they select — corgi previously renounced both halves, so three of four modes were
invisible (NAVIGATION.md tier 1: nothing is discoverable until you show it). **AND ENGRAVED
COLUMNS**: every value now stands in the same cell down the whole page, which is what a spec
sheet IS; three scrolling columns of truncated two-row cards is a web kanban.

**THE TRADE, stated plainly and asserted rather than spun: 8 task rows on screen become 7.**
A sections board cannot amortize its phase heads across three columns the way a columns board
can, and the reclaimed rows buy back almost — not quite — what the stacking costs. The check
is named for that ("costs at most ONE task row") and prints both numbers; an earlier draft of
it was named "more task rows reach the screen", which was FALSE, and it was rewritten rather
than left green. What the 7 buy: every title whole at BOTH widths (the columns cut all eight
at 80), three params each instead of two, and one shared geometry.

- **`themes.py`**: corgi gains `layout="strip"`; `strip` documented in the module's token
  list. **No new colour token** — the strip is drawn in `alu`, `screen` and `dim`, which corgi
  already declares. No other theme touched.
- **ONE GEOMETRY SEAT: `Corgi.slots(w) -> [(origin, code, value_w)]`**, read by the renderer
  and by every acceptance check (the `Ledger.cols` / `Swiss.grid` / `Nord.panes` /
  `Instrument.reticle` precedent). Right-flushed, so **width buys TITLE MEASURE and nothing
  else** — the slot block is the same size at 118 and at 80, which is a check, not a claim.
- **THE PARAM THAT WAS DELETED, and it is the load-bearing edit.** The flow sub-row printed
  DUE / PH / PR. **`PH` is gone: under a sections board the phase is stated by the section
  head one row above, so `PH BACKLOG` on every row of the BACKLOG section is a CONSTANT** —
  the exact defect the trace pass named in instrument's sub-row. `ST` takes its cells and
  actually varies (a blocked task inside DOING reads `BLK` beside its open siblings).
- **NOTHING WAS LOST WITH THE ROW.** The right-flushed chip is gone, and its three readings
  are not: `blk` -> `ST BLK`, `done` -> `ST DONE`, the day count -> `DUE`. The chip's SEVERITY
  TONE moved onto the DUE value, so the colour now lands on the reading rather than beside it.
  Asserted in three checks.
- **THE DROP RULE, derived from `TITLE_MIN = 24` rather than tabulated**, and asserted at the
  exact cell: **56 cells buy three slots, 55 buy two, 47 buy two, 46 buy one, 38 buy one, 37
  buy none** — and at none the two-row flow card comes back, byte for byte, so the degrade
  lands on the form the strip replaced and can never be worse than it (swiss's grid law).
  Measured at five width classes (30 / 40 / 56 / 74 / 112): nothing wraps at any of them.
  **Stated rather than hidden: the ladder is exercised at KIT level only.** The board class
  starts at 80 screen cells, which gives a card 74, so on any real screen all three slots
  always show.
- **THE MODE STRIP'S OWN CEILING, measured before it was coded.** `#tabs` is `width: 1fr`
  inside `#ap`'s `padding: 1 2`, so its narrowest live seat is the widget class at 46 screen
  cells => **42 cells** (measured at 46/50/60/79/80/96/118). The full strip comes out at
  **40-41** for the app's four modes — **one cell of headroom**, which is why `STRIP_MAX` is a
  constant with a three-tier ladder under it rather than a comment: **tier 1** letterspaces
  the active mode; **tier 2** (a list that can no longer afford it — exercised with
  `timeline` in place of `gantt`, the label that pushes the spaced form over 42 and not the
  tight one) gives up the letterspacing and marks the active mode with a lit segment instead;
  **tier 3** falls back to the previous active-only form. **Every tier keeps TWO channels on
  "which mode is on screen", so the answer never rides on colour alone.**
- **THE ROW BUDGET, and where it came from: dead air, not the hero.** On a TE panel the
  HAIRLINE is the separator, so a blank row above a rule is a separator drawn twice. Under
  `strip` every module carrying a `border-top` gives up its `margin-top`, and `.col-head`
  gives up its `margin-bottom` for the same reason (instrument's "the reticle pays for
  itself"). **Measured: the board region goes 9 rows -> 12 at 30 screen rows, +33%**, and that
  is what lets one section print all seven of its rows. The hero was NOT shrunk — it is
  corgi's signature and `Screen.sz-board #hero { min-height: 9 }` would have had to be fought.

**A SIDE EFFECT IN THE SHIPPED APP, stated because it is one.** `aperture.py` injects
`kit.tcss()`, so corgi's margin reclamation reaches the real app's aperture screen on the two
ids that exist there (`#meter`, `#tiles`): corgi's aperture loses two blank rows. The same
argument applies on the same widgets, and `verify_aperture` is **ALL PASSED**, but it is a
change to the product, not only to the prototype.

**Byte-identity, measured twice rather than assumed.** With the token live, kit signatures
(`card_row`, `card_rows` and four `head` indices at w = 14/20/28/40/47/60/105, plus `sect` in
both registers, the meter, the calendar, the tile, `tcss()`, `empty` — and now `tabs` in four
active states): **the other 7 languages are byte-identical, 7 of 7** (naught 3305 · instrument
3714 · swiss 2802 · industrial 3365 · nord 3324 · darkside 2113 · ledger 4982 bytes); corgi
moves 3614 -> 3747. **And with `layout` forced back to the base default the WHOLE pre-change
dump comes back byte-exactly for all EIGHT** (`_corgi32_flowA.txt` == `_instrument_post.txt`,
the twenty-ninth pass's baseline, `8 of 8`) — the previous composition is preserved as
`_flow_composition` / `_flow_card_rows` / `_flow_tabs`, not deleted.

**THE SPEC'S COLLISION CLAIM, RE-MEASURED — and the strip RECOVERED the 2.2 points the plates
cost and then some.** The industrial-vs-corgi distance, as the fraction of board cells that
differ: **47.5% before the plates -> 45.3% after them (the twenty-fifth pass) -> 52.9% now.**
Both languages were indenting their card rows into columns; a full-width corgi surface undoes
that, exactly as predicted. Printed by the check, so it moves with the code.

**Counts: verify_language 951 -> 1033 (+82), and the arithmetic was DIFFED rather than
hand-counted** (a script that compares the check NAMES of the two runs, because a hand count
of eighty-two is a hand count that is wrong). **Adding the token alone left the total at 951**,
which is a coincidence worth naming: the ALT table gained `corgi.layout` (`is live` ·
`restores cleanly`, **+2** — corgi declared no `layout` before this pass) at the same moment
`column_langs` dropped corgi and took its two empty-column checks with it (**-2**). Then the
checks this pass wrote: **kit level +49 · app level +29 · the empty-column section +4 = 82**,
and **0 checks were removed**.

**Runs: 1033 checks, 3 of 3 BACK-TO-BACK GREEN, and the bar was MET this time.** Full
`verify_language` on the final state (`_run32_0.txt` … `_run32_2.txt`): rc=0, 1033 checks,
**ALL PASSED** ×3. **Zero settle timeouts, and the darkside race did not fire in any of the
three** (it is ~1-in-12, so three runs is not evidence it is gone — the watch stays open).
Settle headroom worst **4 of 40 over 54 captures** (47 before this pass).

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** · `verify_widget`
**ALL PASSED**, redraw **1478 µs = 8.87 %** of a 60 fps frame (1402 µs on an earlier run of
the same code — the sheet's cost is inside this probe's own run-to-run spread) ·
`verify_board` **ALL PASSED** (headroom worst 5 of 40 over 62 settles) · `pytest tests`
**137 passed**.

**Measured, and reported because they are costs.**

1. **The 118-cell board has a ~40-cell VOID between the title column and the value block.**
   Right-flushing is what makes the geometry stable across sections, so the surplus width has
   to land somewhere, and it lands in the middle. At 80 the sheet is tight and reads well; at
   118 it reads airy — which is swiss's register, not corgi's. **The obvious cure is data, not
   layout: an LCD segment bar for DUE in that gutter, drawn with corgi's own `bar()`
   mechanism.** That is a data-viz element with its own laws (shared scale, microbar floor,
   clip-not-clamp) and it is a whole increment, so it was NOT smuggled into this one.
2. **The DOING head can be the last thing on the page, with nothing under it.** At 30 rows the
   sheet prints BACKLOG whole and then a stranded head. It is not dishonest — the head states
   `6` and `.kb-flat` shows a scrollbar — but it reads like a cut page. Dropping the per-head
   rule under `strip` (swiss's "ONE hairline for the whole spread" argument) would give back
   one row per phase and is the cheapest next move on this surface.
3. **Corgi lost its empty-state seat**, because the sections branch of `kanban.py` is the one
   branch that never mounts `k.empty()`. PENDING item 7 now covers FOUR languages. What corgi
   keeps is the head's count, which reads `0` on an empty phase — asserted, along with the
   fact that there is no seat and that the phase is below the fold at 118x30 anyway.
4. **The head rule still stops a cell short of the sheet's right edge** — the standing
   `avail - 4` head budget mismatch (PENDING item 4), now carried by a FOURTH language.
5. **`layout="flow"` leaves corgi's tab strip invisible**, because the row-eating defect lives
   in the flow composition and byte-exact restore is the discipline. The shipped corgi is
   `strip`, so no user sees it; the check that asserts it is named for what it is.

**Open after this pass:** (a) the `layout` roll-out is **DONE, 8 of 8** — the axis is closed;
(b) the 118-cell void and the stranded head, above — both are the next moves on this surface,
and (b1) is the more interesting one because it is a data question; (c) PENDING item 7 is now
the cheapest item with the widest reach (four lines, four languages); (d) the darkside capture
race is unchanged and still unexplained — it did not fire in this pass's three runs, which is
not evidence; (e) `kanban.py`'s head budget is now a FOURTH language's workaround.

**Artifacts (`prototypes/out/`, outside the file budget):** `_probe32.py` (the frames the
design was read from) · `_probe32b.py` (**the feasibility probe — monkeypatched, no file
edits, the row budget measured before a line of it was written**) · `_probe32c.py` (the
`#tabs` seat measured at seven widths — where `STRIP_MAX` comes from) · `_probe32d.py` (the
BEFORE frames) · `_sigdump32.py` / `_flowdump32.py` / `_flowdump32_29.py` / `_cmp32.py` (the
byte-identity instruments) · `probe32_corgi_{118,80}.txt`, `probe32_flow_corgi_{118,80}.txt`,
`strip_corgi_{118,80}.txt`, `strip_corgi_flow.txt` (the renders) · `_corgi32_{post,flow,
flowA}.txt` · `_run32_{0,1,2}.txt` (the three runs).

**Done 2026-07-27 (thirty-first pass) — the app bug the thirtieth pass located is FIXED, the vacuous
check that hid it is de-vacuated, and the nord `capture_styled` watch is CLOSED after seven passes.**
Four lines of `kanban.py`, and the evidence is the 12-run table rather than an argument.

**THE FIX, and it is the one that was measured before it was written.** `KanbanBoard` now HOLDS the
detail pane it mounted instead of asking the DOM for it:

```python
self._detail: Static | None = None   # __init__ and the top of build()
...
row.mount(detail); self._detail = detail          # the split branch
...
pane = self._detail                               # _drive
if not self._detail_w or pane is None:
    return
```

The `try/except` around `query_one("#kb-detail")` is gone with it — and that matters as much as the
reference does. **The lookup could not fail loudly, so it failed silently**: during a rebuild
`remove_children()` is asynchronous, the board holds the PREVIOUS build's pane for a beat, and
`query_one` answered with that one. The text went into a widget about to be removed; the live pane
was never written; and because `_drive` sets `self._cursor` on the line BEFORE the write,
`_seed_detail`'s `if self._cursor is None` guard turned every later seed into a no-op. Permanently
blank. A held reference cannot be stale, because `build()` is the only thing that writes it and it
writes it in the same statement that mounts the pane.

**THE 12-RUN BAR: 11 of 12 green, and the twelfth is the darkside race, excluded by prior
agreement.** Full `verify_language`, back-to-back on the final state, **951 checks every run**:

| run | rc | result |
|---|---|---|
| 0-3 | 0 | **ALL PASSED** ×4 |
| 4 | 1 | the darkside 4-check race (`0 row(s)`) — the characterized signature, no settle timeout |
| 5-11 | 0 | **ALL PASSED** ×7 |
| 4 (rerun) | 0 | **ALL PASSED** |

**ZERO settle timeouts in 12 runs, against 8 of 12 before the fix.** That is the number this pass
turns on: the widened `settle()` from the thirtieth pass is unchanged and still watching, so the
green is a green the harness was actively trying to break. The check count is back to a flat 951 —
no timeout lines — which is the same fact stated arithmetically.

**THE VACUOUS CHECK, de-vacuated and MUTATION-TESTED — this is the part worth keeping.** `nord nav:
the detail is driven at rest` asserted `kb._cursor is not None` while being named *"the pane is never
blank"*. It now reads the painted rows of the pane's own region off the composited frame (region
taken from the widget, so it follows a recomposition). Both oracles were then run against two
mutants in a throwaway probe (`_probe31_mut.py`, not left in the suite):

| | painted rows | OLD oracle | NEW oracle |
|---|---|---|---|
| unmutated | 6 | PASS | PASS |
| mutant A — `_seed_detail` neutered | 0 | FAIL | FAIL |
| **mutant B — `_drive`'s write goes nowhere** (the real bug) | **0** | **PASS** | **FAIL** |

**Mutant B is the whole point: the old oracle passes on the exact defect the check exists to catch.**
It was not weak, it was blind — and it was green through all four of the thirtieth pass's blank-pane
runs. VERIFY.md's rule ("mutation-test every assert") would have caught this at birth.

**The aperture was checked for the same pattern and does not have it.** `taskboard/aperture.py`
contains no `kb-detail`, no `board_layout`, no `KanbanBoard` — grep-verified — so nord's split branch
is not on its path and `verify_aperture`'s green never covered it (stated so the green is not
over-read). Wider: **`remove_children()` appears in exactly ONE place in the whole codebase**,
`KanbanBoard.build()`, so the zombie-widget shape cannot occur elsewhere; and the only other
`call_after_refresh` outside kanban.py is `aperture.py:91`'s `self.redraw`, which defers a redraw of
itself with no rebuild and no id lookup. Different shape, no risk. Nothing to report, nothing fixed.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** · `verify_widget` **ALL
PASSED**, redraw **1363 µs = 8.2 %** of a 60 fps frame · `verify_board` **ALL PASSED** (headroom
worst 5 of 40 over 62 settles) · `pytest tests` **137 passed**.

**WATCHES: the nord one CLOSES, the darkside one stays open.** nord `capture_styled` — opened in the
28th pass as "a red that was never isolated", promoted to the suite's dominant flake in the 29th,
mechanised in the 30th, fixed here. The evidence for closing it: 0/30 in isolation with the fix
(`_probe30g.py` measured the same change before it was written), 0 settle timeouts in 12 full runs,
and a check that now fails on the defect. **Closed.** The darkside race stays **open**: it fired once
in 12 (run 4), same 4-check signature, and — the thirtieth pass's contribution — **with no settle
timeout at its own capture**, so its cards, heads and empty seats were all painted and the frame was
stable. Unpainted widgets are positively ruled out for it; it is something else, and it is next.

**Cost, stated: nothing measurable.** The fix removes a DOM query per cursor move and adds an
attribute. `_detail` is a second piece of state beside `_detail_w`, which is the one thing to dislike
— two fields describing the same pane, and they are written in the same two places.

**Artifacts:** `_probe31_mut.py` (the mutation test), `_run30.py` re-used for the table
(`_run30_00.txt` … `_11.txt`, overwritten with this pass's runs).

**Done 2026-07-27 (thirtieth pass) — the nord `capture_styled` flake is NOT a harness race. It is an
APP BUG, and the widened `settle()` is what made it say so.** The twenty-ninth pass's hypothesis was
tested first and cured second, in that order — and the cure did not do what it was expected to do,
which is the whole point of this entry.

**THE HYPOTHESIS: CONFIRMED, exactly as written.** The 29th pass proposed that `settle()` signs off
on frames whose split detail pane is still blank, because it interrogated `app.query(TaskCard)` and
the pane is a `Static` filled by `_seed_detail`, which `build()` defers with `call_after_refresh`.
Measured in isolation before touching anything (`prototypes/out/_probe30.py` — 30 nord captures, the
SHIPPED settle condition verbatim, the detail pane's painted rows read at the instant it fired):
**4 of 30 runs fired on a frame with ZERO painted detail rows.** That is the observed red, reproduced
outside the suite, in ~2 minutes. The mechanism named in the 29th pass is real.

**THE CURE, and it is not a nord special case.** `settle()`'s condition A was "every card the
compositor says it is drawing has painted pixels". It is now "every CONTENT WIDGET the board mounts
and the compositor says it is drawing has painted pixels", where the set is named by the classes
`KanbanBoard.build()` itself attaches:

```python
BOARD_CONTENT = ("kb-card", "col-head", "kb-empty", "kb-detail")
```

That list is the renderer's own strings (grep-verified: nothing outside `build()` mounts any of the
four), so it cannot drift from what the board draws, and it widens the wait for the sections and
columns branches too — their phase heads and empty-state seats were never waited on either. Two
smaller changes ride along: the loop now collects ALL unpainted widgets instead of breaking on the
first, so the timeout FAIL can NAME them (`unpainted: kb-detail@36,18 80x10`) instead of saying "the
board"; and the widget's own `renderable` is deliberately not consulted — it reads empty on this
Textual version even for a pane that HAS painted (`renderable chars=0` on all 30 probe runs, blank
and painted alike), so the composited frame stays the only oracle.

**AND THEN THE CURE FAILED — in the informative direction. The pane never paints AT ALL.** Widened
settle, same 30 runs (`_probe30b.py`): **7 of 30 TIMED OUT** rather than settling late. Given 80 more
pauses after the timeout (`_probe30f.py`, 24 runs): **1 timed out, 0 of those were merely late — the
blank is PERMANENT.** So this was never a deferral the harness could wait out.

**THE BUG, located.** At the timeout the board's own state says the seed already ran
(`_probe30c.py`): `_cursor` is a `TaskCard`, `_detail_w=77`, exactly ONE `#kb-detail` in the DOM,
compositor-visible — and its region on the frame is blank. So `_drive` wrote the detail text
somewhere else. `_probe30e.py` caught it: on the failing run the log reads

```
BAD run 8 i=-1 live=[83712]: drive: 1 pane(s) ... writing to 35792 | drive: 2 pane(s) ... writing to 35792
```

**`build()` calls `remove_children()`, which is ASYNCHRONOUS, and then mounts a fresh pane. For a
beat the board holds TWO `#kb-detail` widgets, and `_drive`'s `self.query_one("#kb-detail")` answers
with the one the PREVIOUS build left behind.** The text lands in a widget about to be removed; the
live pane is never written to; and because `_drive` sets `self._cursor` before that write,
`_seed_detail`'s `if self._cursor is None` guard makes every later seed a no-op. Blank forever, until
some other event drives the cursor again.

**The counterfactual, measured rather than argued.** `_probe30g.py` emulates the candidate fix from
OUTSIDE the app (wraps `build` to remember the pane it just mounted, and `_drive` to write to that
object instead of asking the DOM): **0 of 30 timeouts**, against 4-7 of 30 without it. kanban.py was
not edited — this pass's file budget is the harness and this entry is a finding, not a fix.

**THE USER-VISIBLE SYMPTOM, stated plainly: nord's detail pane can come up permanently blank.** Every
rebuild is a chance — and a resize is a rebuild, on a desktop widget the user drags. It heals only
when something moves the cursor. This is not a test artifact.

**THE 12-RUN BAR WAS NOT MET: 4 of 12 green.** Full `verify_language`, back-to-back on the final
state, ~34 s each (`_run30_00.txt` … `_11.txt`):

| run | rc | checks | result |
|---|---|---|---|
| 0 | 1 | 953 | settle timeout ×2 — `nord nav`, `nord nav enter` (`kb-detail@36,18`) |
| 1 | 1 | 952 | settle timeout — `nord @118x30` |
| 2 | 0 | 951 | **ALL PASSED** |
| 3 | 0 | 951 | **ALL PASSED** |
| 4 | 0 | 951 | **ALL PASSED** |
| 5 | 1 | 953 | darkside 4-check race + settle timeout ×2 (`nord nav`) |
| 6 | 1 | 953 | settle timeout ×2 — `nord nav`, `nord nav enter` |
| 7 | 1 | 952 | settle timeout `nord styled @118x30` + its 7 dependents |
| 8 | 1 | 952 | settle timeout `nord styled @118x30` + its 7 dependents |
| 9 | 1 | 953 | settle timeout ×2 — `nord nav`, `nord nav enter` |
| 10 | 0 | 951 | **ALL PASSED** |
| 11 | 1 | 952 | settle timeout — `nord empty` |

**The red rate went UP, from ~24 % to 8 of 12, and that is a detection change, not a stability
change.** The app bug fires per CAPTURE at roughly 5-15 %; the suite takes ~8 nord captures, and the
old condition only ever noticed the ones a pixel-reading check happened to land on. Runs 0/6/9 are
the proof: the timeout fired, and every `nord nav` check still PASSED — the blank healed on the next
keypress, before any check looked. **The suite was blind there.** Baseline for the check count is
951; each settle timeout adds one line, which is why the count moves.

**A VACUOUS CHECK, found by accident and worth more than the flake.** `nord nav: the detail is driven
at rest, before any key (probe self-check — the pane is never blank)` asserts `kb._cursor is not
None`. In this bug `_cursor` is ALWAYS set — it is set on the line before the write that goes
astray — so the check passes on precisely the frames where the pane IS blank. It is named "the pane
is never blank" and cannot fail when the pane is blank. Not fixed here (budget); recorded as the
next honest target.

**The darkside race is a DIFFERENT mechanism, and the watch stays open.** It fired once in 12
(run 5), with its familiar 4-check signature and **no settle timeout at its own capture** — so
darkside's cards, heads and empty seats were all painted and the frame was stable, and the fixture
card still was not on screen. The widening covers unpainted widgets; whatever darkside is doing is
not that. The 21st pass's "cards mounted but unpainted" diagnosis is now positively excluded for it.

**The other suites, on the final state:** `verify_aperture` **ALL PASSED** · `verify_widget` **ALL
PASSED**, redraw **1282 µs = 7.69 %** of a 60 fps frame · `verify_board` **ALL PASSED** (its own
settle is untouched; headroom worst 5 of 40 over 62 settles) · `pytest tests` **137 passed**.
Settle headroom in `verify_language` is unchanged at worst 3-5 of 40 on the runs that settle.

**Watches after this pass — one closed, one narrowed, one open.** The nord `capture_styled` watch is
**NOT closed, but it is no longer a mystery**: it is `_drive`'s DOM lookup racing `remove_children`,
reproducible in isolation in ~30 runs, with a 4-line candidate fix measured at 0/30. It CANNOT be
closed from the harness — it needs kanban.py, which was outside this pass's budget. The darkside
watch stays **open and unexplained**, now with one mechanism ruled out. And the suite is red about
two runs in three until the app fix lands, which is a real cost of shipping this widening and the
reason the user should decide whether to take the app fix next or revert `kb-detail` out of
`BOARD_CONTENT` (the other three classes have never blocked a settle).

**Artifacts (`prototypes/out/`, outside the file budget):** `_probe30.py` (the shipped condition,
4/30 blanks) · `_probe30b.py` (widened, 7/30 timeouts) · `_probe30c.py` (board state at the timeout)
· `_probe30d.py` (build/seed/drive trace) · `_probe30e.py` (**the object-identity proof**) ·
`_probe30f.py` (late vs permanent) · `_probe30g.py` (**the candidate fix, 0/30**) · `_run30.py` and
`_run30_00.txt` … `_run30_11.txt` (the 12 runs).

**Done 2026-07-27 (twenty-ninth pass) — INSTRUMENT's `layout="trace"`: the phase head becomes a
LABELLED DAY RETICLE and every task hangs a braille sample off it.** Step 7 of rolling `layout`
out; coverage **7 of 8**, corgi the last gap. instrument is the user's polish benchmark, so the
bar was "is this MORE instrument", not "does it pass" — the argument is below, and it is about
what the trace REPLACED.

**Before / after, the 118×30 board, the leading column verbatim** (`prototypes/out/
trace_instrument_flow.txt` vs `trace_instrument_118.txt`):

```
  before (flow — the bench readout)                after (trace — the scope reticle)
  BACKLOG 7⣿⣿⣿⣿                                    BACKLOG                             7
                                                      ─├────7d┴───14d┴───21d┴
   ⣿ Renew TLS certificate············ 3d           ⣿ Renew TLS certificate········ 3d
     ⣿⣿⠒⠒⠒⠒ 3d                                        ⠒⣿⣿⣿⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊ 3d
   ⠂ Write API reference·············· 5d           ⠂ Write API reference·········· 5d
     ⣿⣿⠒⠒⠒⠒ 5d                                        ⠒⣿⣿⣿⣿⣿⠒⠒┊⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊ 5d
   ⠂ Shut down legacy servers········· 8d           ⠂ Shut down legacy servers····· 8d
     ⣿⣿⠒⠒⠒⠒ 8d                                        ⠒⣿⣿⣿⣿⣿⣿⣿⣿⠒⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊ 8d
   ⠂ Deprecate v1 endpoints··········· 9d           ⠂ Deprecate v1 endpoints······· 9d
     ⣿⣿⠒⠒⠒⠒ 9d                                        ⠒⣿⣿⣿⣿⣿⣿⣿⣿⣿⠒⠒⠒⠒⠒┊⠒⠒⠒⠒⠒⠒┊ 9d
  (four IDENTICAL bars — the sub-row drew            (four DIFFERENT lengths on one shared
   PHASE progress, a property of the column,          scale; measured on the render, fills
   restated four times, beside a number that          = [3, 5, 8, 9])
   restated the chip)
```

**THE ARGUMENT, stated plainly: the row the trace replaced was a CONSTANT.** The flow sub-row drew
phase progress — a property of the PHASE, not of the task — so every card in a column rendered the
identical `⣿⣿⠒⠒⠒⠒`, four times over, next to a figure that restated the due chip one row above it.
The reticle spends those same two rows on a quantity that actually varies down the column, and the
board now answers "which of these is nearest, and by how much" at a glance. This is asserted rather
than asserted-about: the check that the flow bar is identical for a 3-day and a 9-day task is a
live check, not a claim in this file.

**A second data defect cured inside the token's boundary: the head's spark SATURATED.** The flow
head drew `count` as `FULL * min(4, count)` — so BACKLOG 7 and DOING 6 and a phase of 4 all drew
the same four cells. Under `trace` the head states its count as a figure (DATAVIZ law 5: position
is not a reading) and spends the row on a real scale instead of a bar that could not tell 4 from 7.

**What the token owns, stated precisely** (an undefined boundary is an unfalsifiable check): the
**phase head** and the **card's second row**. It does NOT own `card_row` (the title row is
untouched — the dot marker, the dotted leaders and the chip are verified identity), `sect()`, the
braille meter, the calendar cells, `tile_row`, or any component. The flow degrade asserts all of
them come back byte-exactly.

- **`themes.py`**: instrument gains `layout="trace"`, `tick="#333c47"` (the graticule's stroke) and
  `unit="#6b7785"` (readings and axis labels); all three documented in the module's token list. The
  two colours coincide with `dim` and `mut`, which is the **`darkside.rail` precedent** (`rail` ==
  `dim` there too): a token names a ROLE, and naming the graticule separately is what lets it be
  retuned without moving every dim thing on screen. Both are read by the renderer and both are
  mutation-tested, so neither is a manifest entry. No other theme touched.
- **ONE GEOMETRY SEAT: `Instrument.reticle(w) -> (span, ticks)`**, read by the head, by every trace
  row and by every acceptance check (the `Ledger.cols` / `Swiss.grid` / `Nord.panes` precedent).
  Cell 0 is the **underflow cell**, the origin is cell 1, day `d` lands on cell `1 + d`.
- **ONE CELL IS ONE DAY, AND IT IS A CONSTANT, NOT A TOKEN.** This is the load-bearing decision.
  A per-column scale is exactly the "siblings lie" failure DATAVIZ.md law 2 names — a 3-day task
  would render longer in the narrow column than a 9-day task in the wide one. Width therefore buys
  **HORIZON, never resolution**, and the check asserts a 3-day sample is three cells at w=39 and at
  w=21. The horizon is capped at **21 days (three weeks)**, so every column that can afford it
  shows the *same* three weeks.
- **CLIPPING, NEVER CLAMPING, AT BOTH BOUNDARIES** (the Bodmer law, and it applies at both ends).
  An overdue task lights the underflow cell in the alert tone and leaves the origin dark — clamping
  it onto the origin would print an overdue task as "due today". A task past the horizon fills the
  field and ends in `⠿`, **a glyph the fill itself never emits** (the fill knows only `⣿`, `⡇`,
  `⠒`), so it can never be confused with a sample that merely reaches the last cell; a check
  asserts `⠿` appears for none of days 0-21. Both readings still state the true number.
- **MONOTONE FILL FROM A FIXED ORIGIN, no needle** (the other Bodmer law): length is the reading,
  and the eye compares lengths down the column.
- **MICROBAR FLOOR (DATAVIZ law 3):** due TODAY lights a braille HALF cell — `⡇`, sub-cell
  precision being this language's whole point — so it can never be read as "nothing due".
- **THE DROP RULE, derived from the constants rather than tabulated.** `SPAN_MIN = 9` (underflow +
  origin + one whole week + its tick) gives a threshold of **w = 16**, and the checks assert
  `reticle(16)` buys the scale and `reticle(15)` returns `(0, [])` — the exact cell. Below it the
  scale is **RENOUNCED, never squeezed**, and the degrade lands on the bench readout it replaced,
  asserted by equality. Measured at five size classes: **w=13 → renounced · 16 · 21 · 39 · 105 →
  reticle**, nothing wrapping at any of them. **The narrow board is a real regime: at 80×30 the
  DONE column falls under the threshold and gives its scale up** while the other two keep theirs.

**THE RENDER CAUGHT THREE DEFECTS THAT GREEN KIT-LEVEL CHECKS HAD NOT** (the seventh pass of this
lesson, and the reason the brief says to look with your own eyes):

1. **`HEAD_LEAD` was one constant doing two jobs, and one of the two answers was wrong.** The head
   and its cards start on the same screen column but `.kb-card` pays `padding: 0 1` and the head
   pays none, so the ORIGIN offset is 1 — while `head_w` runs **3 or 4** cells wider than the
   card's content box, the 4th appearing only when the column overflows and Textual spends a cell
   on its scrollbar. Measured, not inferred: **43/39, 39/35, 20/17 at 118; 25/21, 23/19, 16/13 at
   80.** With one constant the head's axis advertised a horizon the samples under it did not have.
   Now `HEAD_PAD = 1` (origin) and `HEAD_TRIM = 4` (length, trimmed by the MAXIMUM — an axis longer
   than its data is a lie, an axis a cell short of it is merely modest).
2. **The head shrank to one row in the narrow column, and the board looked broken.** At 80 the DONE
   column renounced its scale, its head became one row, and its card stack started a row ABOVE its
   neighbours'. A kanban is read ACROSS its columns. The head is now **always two rows** under
   `trace`; the renounced form is a blank row, not a stub axis — a baseline with no gradations
   would advertise a scale the samples beside it do not use.
3. **The axis row cost the board a card.** The head grew by a row and the fourth card fell under
   the fold. Cured inside the composition: `.col-head`'s blank row is exactly what the reticle is
   FOR — a graticule already separates a legend from the traces under it — so `trace` sets
   `margin-bottom: 0` and the reticle pays for itself. **Measured on the render: the same number of
   card rows reach the screen as before, and it is a check, not a claim.**

**A GLYPH COLLISION THE SUITE CAUGHT, and the fix is the finding.** The graticule was first drawn
with `│` — and **`Ledger.RULE_V` is `│`**, so ledger's own dispatch check ("money-column rules
render IFF `layout=ruled`") went red the moment instrument borrowed the glyph. The check was right
and it was not weakened: the graticule is now `┊`, the dashed form, which is what a graticule
should be anyway (fainter than a divider). **Channel split, stated as an assumption:** STRUCTURE
(origin `├`, week tick `┴`, graticule `┊`) is box drawing; DATA (`⣿ ⡇ ⠒ ⠿`) is braille, which
DENSITY.md measures as the only fully width-safe density mechanism. The box-drawing half is safe
**by convention, not by guarantee** — the same assumption `─` and `│` already carry throughout this
app. **`┊` U+250A is the one glyph here with no prior use in the codebase: worth an eyeball in the
user's own terminal before this is called closed.**

**THE GROUND COLOUR: the spec's `#080c14` was EVALUATED AND DECLINED, with the number.** Instrument
keeps `#0a0d12`. The weighted channel sum (`0.2126R+0.7152G+0.0722B`, the same proxy the law-03
work uses) is **12.7 for `#0a0d12` and 11.7 for `#080c14`**; the nearest other ground is corgi's
`#0d0d0d` at 13.0, so the darker value would buy about one point of separation from a language it
already differs from on every structural axis. Against that: **grounds never enter the greyscale
pair test at all** (`kit_sig` strips hex from the stylesheet, on purpose), so the suite cannot
measure a benefit; the change is outside this token's boundary; and this ground is verified
identity on the benchmark language. **Deviation from the spec, flagged rather than silently taken.**

**THE SPEC'S LAW-01 CLAIM, RE-MEASURED RATHER THAN QUOTED.** The spec assigned this token by saying
instrument "collides with darkside in greyscale". The darkside-rail pass already refuted it; the
number is now recomputed inside the suite so it moves with the code. **Instrument and darkside
differ on 23.4% of board cells after the trace, against 18.4% under flow** — the trace moved the
two languages FURTHER apart, not closer, and both figures are printed by the check.

**Byte-identity, measured rather than assumed.** Kit signatures (`card_row`, `card_rows` and four
`head` indices at w = 14/20/28/40/47/60/105, plus `sect` in both registers, the meter, the calendar,
the tile, `tcss()` and `empty`) were dumped before the change to `prototypes/out/_instrument_pre.txt`
and compared after (`_instrument_post.txt`): **the other 7 languages are byte-identical, 7 of 7**
(naught 2993 · corgi 3508 · swiss 2499 · industrial 3046 · nord 3019 · darkside 1767 · ledger 4643
bytes, unchanged); instrument moves 1829 → 3436. **And `layout="flow"` restores the WHOLE
pre-change dump byte-exactly** (`_instrument_flow.txt` == `_instrument_pre.txt`, all eight
languages, `True`) — the previous composition is preserved as `_flow_head` / `_flow_card_rows`, not
deleted.

**A CRASH IN NORD'S SECTION TURNED INTO A LOUD RED, and it needs saying because it is not my
token.** `verify_language`'s law-03 block indexed `ttl_rows[0]` unguarded. When the twenty-eighth
pass's named `capture_styled` watch fires, the detail pane comes back unpainted, `ttl_rows` is
empty, and the run died with `IndexError` — **killing the run and hiding every check after it**.
It fired once in this pass's first batch of three. The index is now guarded and the race is what it
should always have been: a named FAIL the run continues past, the same discipline `settle()`'s
timeout already carries. **This is harness hardening inside the budget file, not a fix for the
race, which is still unexplained.**

**Counts: verify_language 887 → 951 (+64), and the arithmetic closes.** Kit level **+34**: the
tokens declared (1), the tick grid + the capped horizon (2), the threshold at the exact cell + the
narrow tier IS the previous form (2), **five size classes** (5), the head's reticle + the saturating
spark gone (1), the head is always two rows (1), the origin cell (1), the axis never longer than its
samples (1), the trace is DATA where the old row was constant (1), the shared scale (1), the
microbar floor (1), **clip-not-clamp low + high + the flag's glyph is unreachable by the fill** (3),
units in the unit tone + the trace in the accent (2), **the dispatch law across all 8** (8), and
four degrade checks (flow restores the readout · `sect`/meter/calendar/tile untouched · the margin
comes back · the composition is restored). App level **+24**: the fixture on screen + the reticle on
the board + the traces hang off it (3), the origin column and the graticule cells read off the
COMPOSITED FRAME (2), **four different lengths on the render** (1), the overdue flag (1), no wrap at
118 (1), the vertical cost is zero (1), the flow degrade in three (3), **seven no-leakage checks**
(7), the collision re-probe (1), and the narrow regime in four — no wrap, the drop FIRED, the
renounced column falls back, every column's stack starts on one row (4). **+6** falls out of the ALT
table now covering `instrument.layout`, `instrument.tick` and `instrument.unit` (`is live` ·
`restores cleanly` each) — instrument declared none of the three before this pass.
34 + 24 + 6 = 64.

**Runs: 951 checks every single run, and the flake record is given in full rather than summarised,
because the headline number moved the wrong way.** **17 runs on the final code: 12 green, 5 red —
and EVERY red is one of the two named watches**, never a check this pass wrote:

| watch | fired | signature |
|---|---|---|
| **nord `capture_styled`** (28th pass's watch) | **4 of 17 (~24 %)** | the detail pane comes back with 0 rows — 7 reds when it hits at 118, 1 red when it hits at 80 |
| darkside capture race | 1 of 17 (~6 %) | the named 4-check signature (probe self-check + its three dependents) |

**THE NORD WATCH IS NO LONGER A ONE-OFF, and that is the loudest thing in this entry.** The
twenty-eighth pass recorded it as a single red that "was never isolated" and passed four consecutive
times afterwards. It has now fired **four times in seventeen runs**, at both widths, and once —
before the guard existed — as a fatal `IndexError` that killed the run. **This increment adds two app-level
captures** (instrument's flow degrade and its 80×30 regime), so the suite's load is up and both races
are load-sensitive: **it is entirely possible this pass raised the rate rather than merely observing
it, and that possibility is not being smoothed over.** See open item (d) for a concrete hypothesis.

Settle headroom **worst 4-5 of 40 over 48 captures** (46 before this pass). The darkside evidence
dump `_race_darkside.txt` is still the stale 10:29 copy — timestamps checked, not assumed.

**THE "3× BACK-TO-BACK GREEN" BAR WAS NOT MET, and saying so is the point of the bar.** Every red
was a named watch and none was a check this pass wrote — but the nord watch fires often enough now
that three fully-green runs in a row did not happen inside seventeen attempts. The longest green run
observed was **two**. Read that as a statement about the SUITE's stability, not about this token:
**the instrument checks were green in 17 of 17 runs.**

**The other suites, run on the final state:** `verify_aperture` **ALL PASSED** — instrument's
reticle does not appear there at all (`aperture.py` calls no `head`/`card_rows`; grep-verified), so
the aperture's no-wrap law is untouched rather than newly satisfied, which is the honest statement ·
`verify_widget` **ALL PASSED**, redraw **1435 µs = 8.6 %** of a 60 fps frame (H ≥ 5 holds; it was
1297 µs / 7.78 % on an earlier run of the same code, so the reticle's cost is inside this probe's
own run-to-run spread rather than measurable above it) · `verify_board` **ALL PASSED** ·
`pytest tests` **137 passed**, no clipboard flake.

**Measured, and reported because they are costs.**

1. **The dim tier got much denser.** A trace field is 23 cells of mostly-unlit lattice per card
   against the old sub-row's 6. It is entirely in the `tick`/dim tone with the sample in the accent
   above it, so the brightness ladder is intact — but the board carries a lot more faint ink, and
   whether that reads as "scope screen" or as "noise" is a taste call the user should make.
2. **The horizon is longer than the data.** The fixture's tasks live in −2…9 days on a 21-day axis,
   so the samples cluster in the left third and most of the field is graticule. That is honest (the
   data really is clustered) and it is what makes the third week's tick meaningful when something
   IS out there — but a shorter horizon would spend fewer cells on emptiness.
3. **An off-scale-low sample does not encode its magnitude.** `-1d` and `-2d` render the identical
   underflow cell; only the reading distinguishes them. That is what clipping MEANS, and DATAVIZ
   law 5 (a gauge states its value) covers it — recorded so it is not discovered later as a bug.
4. **The head's axis is one cell short of its samples in a column that does not scroll** (the
   `HEAD_TRIM = 4` decision above). Deliberate, and stated in the code.

**THE BENCHMARK JUDGMENT, stated explicitly because the brief asked for it: this deepens
instrument.** It is more clinical (a labelled scale with unit suffixes where there was an unlabelled
bar), more braille-dense (the field is braille; only the graticule is not), and more precise
(sub-cell half-cells now carry a real case, "due today"). Above all it turned a constant into a
variable: the two rows a card spends now say something different about every card. The one thing
that could argue the other way is cost 1 above — the density of the dim lattice — which is a look
call, not a correctness one.

**Open after this pass:** (a) the `layout` roll-out is **7 of 8** — **corgi** is the last gap;
(b) `┊` U+250A has no prior use in this codebase and should be eyeballed in the user's own terminal;
(c) the dim-lattice density and the long horizon, above — both are dials (`HORIZON`, and whether the
unlit field is drawn at all) if the user reads the field as noise; (d) **the nord `capture_styled` watch is no longer a one-off — it is now the suite's dominant
flake, and there is a concrete HYPOTHESIS worth testing next session.** `settle()` decides a frame is
painted by interrogating `app.query(TaskCard)` and nothing else. **The split's detail pane is a
`Static`, not a `TaskCard`**, and it is filled by `_seed_detail`, which `KanbanBoard.build()` defers
with `call_after_refresh`. So a frame can satisfy settle's condition — every card painted, two
identical reads — at a moment when the deferred seed has not run and the pane is still blank, which
is exactly the observed symptom ("0 detail row(s)"). **Not chased, not fixed, and stated as a
hypothesis rather than a diagnosis**: the cheap next step is to widen settle's painted-check to any
widget the capture is about to read, and the cheap test is whether the reds stop. (e) the
darkside race fired once in this pass's runs, unchanged; (f) `kanban.py`'s head budget still does not match
the card's content box — this is now the THIRD language carrying a workaround for it (ledger's rule,
swiss's left-flush grid, and now `HEAD_TRIM`), and it is worth curing at the source; (g) the
instrument↔darkside distance is reported at 23.4 %, which is a magnitude, not a threshold — the
0.20 floor in that check is calibrated by hand and would be better derived from the pair matrix.

**Artifacts added (render dumps and probes under `prototypes/out/`, the standing convention, outside
the file budget):** `probe29_instrument_118.txt` / `_80.txt` (the frames the design was read from),
`trace_instrument_118.txt`, `trace_instrument_80.txt`, `trace_instrument_flow.txt`,
`_instrument_pre.txt` / `_instrument_post.txt` / `_instrument_flow.txt` (the byte-identity dumps),
`_probe29.py` / `_sigdump29.py` / `_flowdump29.py` / `_widths29.py` (the probes; `_widths29.py` is
the one that measured the head/card budget mismatch), `_run29_*.txt` (the runs).

**Done 2026-07-27 (twenty-eighth pass) — NORD's `layout="split"`: the board becomes a MASTER/DETAIL
pair, and nord gets a first fixation it measurably did not have.** Step 6 of rolling `layout` out;
coverage **6 of 8**. This pass ran in two halves: a feasibility gate that CLOSED at 4 files, and —
after the file set was widened to 5 by approval — the implementation. Both halves are recorded,
because the gate's reasoning is what shaped the design.

**Before / after, the 118×30 board, rows 18-27 verbatim** (`prototypes/out/split_nord_flow.txt` vs
`split_nord_118.txt`):

```
  before (flow — three columns, no subject)          after (split — a driving list and a subject)
  BACKLOG 7▃        DOING 6▃        DONE 2▁          BACKLOG 7▃
  ───────────────   ─────────────   ──────────       ──────────────  R E N E W   T L S   C E R…
   Renew TLS cert…      3d   Fix checkout…  blk
     Backlog              Website Redesign · Doing    ▸ Renew TLS certificate   3d   PHASE    Backlog
   Write API refer…     5d   Compress data… blk         Write API reference     5d   DUE      3d
     API Platform · Backlog                             Shut down legacy serve… 8d   PRIORITY high
   Shut down legacy…    8d   Design homepa…  0d         Deprecate v1 endpoints  9d   STATE    open
     Legacy Sunset · Backlog                            Add push notifications 18d
   Deprecate v1 end…    9d   Review pull r…  1d         Plan Q3 roadmap         --   PROGRESS ▇▇▇▇▇▇▇░░ 1/3
  (10 tasks on screen, 10 equal elements,             Update onboarding copy  --
   nothing to look at first)                         (7 tasks + ONE subject; the title is the fixation)
```

**THE INFORMATION TRADE, stated plainly and not buried: 10 tasks on screen become 7.** The split
buys a subject with three task rows. That is the pattern's cost and it is not a rounding error.

**Step 1 — the probe, and the spec's law-03 claim is TRUE.** nord's board captured at 118×30 on a
fresh seeded fixture (`prototypes/out/probe28_nord_118.txt`; the same guarded recipe every suite
uses — explicit fixture path, settle-until-painted, painted after 3 iterations, the live board.json
never opened).

**Verdict: nord has NO first fixation.** HIERARCHY.md's self-check asks *"can you name the one thing
the eye should hit first, and is it the largest **and** brightest?"* — nord fails on both halves, and
each half was measured, not eyeballed. Ink was totalled per (foreground hex, bold) across the whole
composited frame; "brightness" below is the weighted channel sum `0.2126R + 0.7152G + 0.0722B` on
the 0–255 sRGB values — a perceptual proxy, not true relative luminance, and stated as such:

| element | hex | brightness | cells | instances |
|---|---|---|---|---|
| card titles | `#eceff4` (ink) | **238.7** | 200 | **10** |
| due chips (warn) | `#ebcb8b` | 205.2 | 9 | 3 |
| hero 8-week load plot | `#88c0d0` (accent, bold) | 181.2 | **61** | 1 |
| tab row / meter pct | `#7b88a1` (mut) | 135.0 | 108 | many |
| **hero numeral "2"** | `#bf616a` (alert, bold) | **117.7** | **25** | 1 |
| meter + head rules | `#4c566a` (dim) | 85.4 | 366 | many |

The hero numeral — the only element that wins **isolation** (its own bordered panel, air around it)
— is the **fifth** brightest ink on screen and holds **25 cells against the load plot's 61 inside the
same panel**. The brightest ink on screen belongs to ten repeated card titles, and a repeated element
cannot be a fixation. So no element wins size + brightness + isolation together; the eye is offered a
red glyph, a larger and brighter cyan plot beside it, and a field of the brightest text below.

**One honesty qualifier on that verdict.** The numeral's tone is *severity-driven* (this fixture's
engine hero is the overdue-count signal at ALERT), so the brightness column would shift on a calm
board. **The area finding is severity-independent** — 25 cells against 61 in the same panel — and
area alone already denies the numeral the "largest" half of the law. The verdict does not rest on the
fixture's mood.

**Step 2 — the feasibility gate. It CLOSED at the 4-file budget, and the reasoning below is what
shaped the design that was then approved at 5. Three measured facts, in the order they bite.**

1. **`board_layout()` has exactly ONE consumer, and it is a binary test.**
   `prototypes/widget_slice/kanban.py:181` reads `if k.board_layout() == "sections":`. Every other
   value — including `"split"` — falls through to the columns branch. **There is no third pane
   geometry a kit can ask for.** Grep-verified: the only other occurrences are the three kit
   definitions and one line of `verify_language.py`.
2. **No board-wide TASK data ever reaches kit level, and the detail pane is made of task data.**
   The kit's board primitives are `head(name, count, w, idx)` and
   `card_rows(title, chip, tone, w, idx, urgent, meta)` — `meta` carries exactly ONE task's fields
   (`kanban.py:82-91`). The only board-wide state ever pushed onto a kit is **`KIT.mood`, a 3-value
   string**, set at `prototypes/widget_slice/app.py:870` and `taskboard/aperture.py:175` — both
   outside the budget. (`meter()` does receive board aggregates — `done`, `total`, `counts` — but
   counts are not tasks: no title, no due date, nothing a detail pane could expand.)
3. **The authorised static fallback dies on the same fact.** The brief permitted the detail pane to
   show a DETERMINISTIC default — "the board's most urgent item", reusing existing hero-pick logic.
   **No such logic exists** (grep: no `hero_pick`, no shared "most urgent" selector; the hero's
   subject is chosen by `engine.hero`, app-side). More decisively: **picking the most urgent requires
   comparing tasks, and a kit primitive sees exactly one.** A per-card predicate over its own `meta`
   cannot be unique — on this very fixture two cards are `blocked` with no due date (`Fix checkout
   500 error`, `Compress database backups`), so any "am I the urgent one?" test written from a
   single card's fields fires twice. The two checks the brief demanded — *`▸` appears exactly once*
   and *the detail title is the **unique** first fixation* — would have been unprovable, or provable
   only by a tautology. That is the vacuous-check failure mode this harness was built to prevent.

**The escape hatch was tried and does not exist.** `composition()` returns TCSS and kits already use
it for real geometry (swiss's `max-width: 78`, darkside's centring). But in sections mode the widget
tree is a flat sequence `VerticalScroll.kb-flat > [Static.col-head, TaskCard, TaskCard, …]`, and TCSS
can neither route one specific child into a right-hand pane (`layout: grid` would checkerboard them)
nor select "the most urgent card" — and above all it cannot change a widget's **content**, which is
what a detail pane is.

**A conflict resolved in the SKILL's favour, and it is the same conflict.** HIERARCHY.md defines the
pattern the spec asked for — *"Sidebar + detail — a narrow list (25-30 %) driving a wide detail pane.
**The list keeps selection state**; the detail pane is the only thing that changes."* Selection state
is **constitutive** of the pattern, not an enhancement to defer. The brief's static-default detail
would have been a degraded form of a pattern the skill defines by its selection behaviour — and even
that degraded form is unreachable per fact 3. Skill wins over spec: build it with selection, or do
not call it master/detail.

**A second spec/brief error worth recording, because it changes the next attempt's shape.** The brief
referred to "the FULL Nord kit". **There is no Nord kit.** `language.py:2345` maps `"nord": Kit` —
nord IS the base class, on purpose (`Kit`'s docstring: *"Base kit = the `nord` language: deliberately
the terminal's own conventional idiom (base16 doctrine)"*). All seven other languages subclass and
override `head`/`card_rows`. Consequence for the next attempt: **`class Nord(Kit)` must be created
first**, or a `layout=="split"` branch written into `Kit` would sit in the class every other language
inherits. That is two lines and is not itself a blocker — but writing the split into `Kit` without
noticing this would have been a real defect.

**The minimal file set this actually needs — 5 files, and the fifth is the one that was excluded.
This was reported, approved, and then built exactly as scoped:**

1. `taskboard/themes.py` — nord gains `layout="split"` + a master-width token.
2. `taskboard/language.py` — `class Nord(Kit)` + `KITS["nord"] = Nord`; `board_layout() ->
   "split"`; ONE shared `Nord.panes(w)` geometry function (the `Ledger.cols` / `Swiss.grid`
   precedent, read by renderer and checks alike); a compact `master_row()`; a `detail_rows()`;
   the flow fallbacks preserved verbatim.
3. **`prototypes/widget_slice/kanban.py`** — a third branch in `build()`: mount a
   `Horizontal(classes="kb-split")` holding a master `VerticalScroll` and a detail `Static`, keep
   `self.cards` populated so `move()` still works, and re-render the detail on focus change.
4. `prototypes/verify_language.py` — the checks.
5. `PENDING.md` — the record.

**Good news for that increment, verified rather than assumed: `app.py` is NOT needed.** `CardFocused`
is a bubbling `Message` posted by `TaskCard.on_focus` (`kanban.py:100`); `KanbanBoard` is an ancestor
of every card, so `KanbanBoard.on_card_focused` fires without touching the app's own handler at
`app.py:742`. **Live focus wiring is reachable from `kanban.py` alone** — the split can ship with
real selection state, which is what makes it the skill's pattern instead of a static imitation. So
the honest recommendation is **not** "do it statically in 4 files"; it is **"do it properly in 5"**.

**Good news for that increment, verified rather than assumed: `app.py` is NOT needed.** `CardFocused`
is a bubbling `Message` posted by `TaskCard.on_focus` (`kanban.py:100`); `KanbanBoard` is an ancestor
of every card, so `KanbanBoard.on_card_focused` fires without touching the app's own handler at
`app.py:742`. **Live focus wiring is reachable from `kanban.py` alone** — the split ships with real
selection state, which is what makes it the skill's pattern instead of a static imitation.

---

## The implementation (after the 5-file set was approved)

**What the token owns, stated precisely** (an undefined boundary is an unfalsifiable check): the
board's **pane geometry**, the **master row** and the **detail pane**. It does NOT own `sect()`, the
`blocks` meter, the calendar cells, `tile_row`, the hero, or anything in the ambient chrome — the
flow degrade asserts the base kit comes back byte-exactly, which covers all of them at once.

- **`themes.py`**: nord gains `layout="split"` and `split=(28, 34)` — the **(master floor, detail
  floor)** in cells. Both documented in the module's token list. No other theme touched.
- **`class Nord(Kit)` exists at last, and `KITS["nord"]` points at it.** This was the gate's second
  finding: nord had been mapped to the bare base class, so it was the one language that could not own
  a composition without changing all eight. The subclass **overrides nothing but the split** — a
  check asserts `Nord.head is Kit.head` and the same for nine other primitives, so "the base kit is
  still the truth underneath" is proved, not claimed.
- **ONE geometry seat: `Nord.panes(w) -> (master, detail)`**, read by the renderer AND by every
  acceptance check (the `Ledger.cols` / `Swiss.grid` precedent). The master owns `[0, master)`, the
  gutter `[master, master+3)`, the detail's content begins at `master+3`. The checks recompute the
  spans from `panes()` and then assert the render lands there, so the two cannot drift.
- **The gutter is SPACE, not a rule.** HIERARCHY.md ranks proximity above a stroke, and nord already
  spends its one `frame="rule"` under the phase heads. Asserted as *no cell in the gutter is ever
  painted, in either pane, at either width*.
- **THE DROP RULE, derived from the token rather than tabulated.** `master_floor + GUTTER +
  detail_floor = 65`, and the checks assert `panes(65) == (28, 34)` and `panes(64) == (64, 0)` —
  the exact cell where the split is bought. Below it the master takes the **whole width**; the split
  is renounced, never wrapped. Measured at five size classes: **w=14 · 28 · 64 → master-only ·
  65 · 118 → split**, nothing wrapping at any of them.
- **The master share is 30 %, and it is a CONSTANT, not a token.** HIERARCHY.md's own figure for a
  driving list is 25-30 %; that is the pattern's law, not a choice this language gets to make.
  Measured on the real board: **34 of 114 cells = 30 %**.

**LAW 03, ENCODED — and this is the check the whole pass exists for.** *Exactly one element wins
AREA and BRIGHTNESS and ISOLATION.* Asserted twice, at kit level on the returned rows and at app
level on the composited frame via a per-cell (colour, bold) map read from the compositor:

- **area** — the detail title, letterspaced through `display_cap()` (the base kit's own display
  register), spans **41 cells** against the widest master row's 28.
- **brightness** — it is the **only bold ink on the board**; master rows are `mut`, the driven row
  brightens to `ink`, and bold is spent exactly once.
- **isolation** — a blank row above and below it, and **no master row has both** (the list is
  contiguous by design).
- The check computes the winners set and asserts it is a **single element and that it is the title**.
  Negative control: the base kit's card, at the width the master actually gives it, wins none of the
  three (spans 33, no bold).

**THE AREA MEASUREMENT WAS WRONG ON THE FIRST TRY, AND THE FIX IS THE FINDING.** Area was first
measured as *painted-cell count*. That instrument ranks a dense dim block above a heading — backwards
— and scores letterspacing at **zero**, when letterspacing is precisely how a terminal enlarges type.
The app-level law-03 check came back `winners=[]` and it was the instrument, not the render. Area is
now **EXTENT** (first painted cell to last), which is HIERARCHY.md's own wording ("a thing that
occupies more cells"), and the weaker ink count is still printed beside it so the softer number is
not hidden.

**Two more defects the RENDER caught that green checks had not** (the sixth pass of this lesson):

1. **`DUE  blk` was on screen.** The chip is a due chip OR a state word, and a state word printed
   under a DUE label is a lie. The field is now dropped when the chip is `blk`/`done`/`--`, and the
   state has its own row. Now a check, with `META_B` (a blocked task) as its fixture.
2. **The first `▸` search found the TAB ROW.** `Kit.tabs` renders `▸board │ lanes …`, so a
   whole-frame cursor count is `>= 1` in every language and the flow negative control could never
   fail. Every cursor count is now restricted to the **master pane of the board region** — the same
   lesson `body_rows()` already carries for the Footer's `▏`.

**Navigation survived the third branch, driven rather than assumed.** A bounded pilot probe presses
keys against the real app: `down` advances the cursor one master row (row 0 → 1) **and the detail
follows it**; `right` still crosses to the next phase (col 0 → 1) through the stacked tree, i.e. the
geometry-based lateral move did not break; and **exactly one cursor exists after each move**. The
first `down` merely moves focus off the hero and onto the board — pre-existing app behaviour this
pass did not touch — so the probe presses it once to enter and measures the move after that. Stated
because the first version of the check did not know it and went red.

**One cursor is impossible to duplicate by construction.** `KanbanBoard._drive()` is the only writer:
it clears the previous card and sets the new one. `on_card_focused` **deliberately does not stop the
message**, so app.py's hero still follows the cursor too.

**nord's empty-state seat SURVIVED the recomposition, and its reachability is stated rather than
implied.** The split branch mounts `k.empty()` for an empty phase, asserted against the **widget
tree** (`query(".kb-empty")` → 1 seat, speaking nord's own voice). A third check asserts it is
**below the fold at 118×30** — the master is a scrolling list, so "it exists" and "the user can see
it" are different claims (the twenty-third pass's reachability lesson). The pixel-search loop for the
other languages would have gone red on the FOLD, not on the seat, which is why nord is asked
separately.

**Byte-identity, measured rather than assumed.** Kit signatures (every primitive in `kit_sig` plus
`board_layout()` and the board measure) were dumped before the change to `prototypes/out/_nord_pre.txt`
and compared after (`_nord_post.txt`): **the other 7 languages are byte-identical, 7 of 7** (naught
8429 · corgi 5404 · instrument 4651 · swiss 3471 · industrial 4769 · darkside 3008 · ledger 6420
bytes, unchanged); nord moves 4755 → 4917. **And `layout="flow"` restores the BASE KIT byte-exactly**
— asserted directly against a freshly constructed `LG.Kit("nord")`, which is a stronger statement
than the `_flow_*` fallbacks the other passes use: nord's fallback IS the base class.

**Counts: verify_language 808 → 887 (+79), and the arithmetic closes.** Kit level **+40**: the kit
exists / the tokens are declared / the base kit is untouched underneath (3), the panes tile exactly +
the 30 % share + the detail is the wider pane (3), the threshold at the exact cell + master-only
below it (2), **five size classes** (5), the cursor + the brightening + the compact row (3), **law 03
in four parts plus its negative control** (5), the fields + the meter family + no state-under-DUE
(3), **the dispatch law across all 8** (8), the `split` mutation — geometry, min-widths, threshold,
restore (4), and the flow degrade + byte-exact base-kit restore + composition restore (3). App level
**+34**: the split regime + the fixture on screen (2), the empty gutter + the detail paints (2), one
cursor + one bold row + they name the same task (3), **law 03 on the render in four parts** (4), no
wrap (1), **seven no-leakage checks** (7), the narrow 80×30 regime in five (5), the flow degrade in
four (4), and **six navigation checks** (6). Empty state **+3**. **+4** falls out of the ALT table
now covering `nord.layout` and `nord.split` (`is live` · `restores cleanly` each) — nord declared no
`layout` before this pass, so both are new. **−2** because the empty-state VOICE loop now runs over
4 columns languages instead of 5. 40 + 34 + 3 + 4 − 2 = 79.

**Runs: 3/3 back-to-back green on the final state, 887 checks each, exit 0.** `verify_aperture` **ALL
PASSED** · `verify_widget` **ALL PASSED**, redraw **1584 µs = 9.51 %** of a 60 fps frame (H ≥ 5
holds) · `verify_board` **ALL PASSED** · `pytest tests` **137 passed in 31.0 s**, no clipboard flake.
Settle headroom **worst 4 of 40 over 46 captures**, identical in all three runs (7 more captures than
the previous pass, same worst case).

**The darkside race did NOT fire in any run this pass.** `prototypes/out/_race_darkside.txt` is still
timestamped **10:29** — the twenty-seventh pass's intermediate run, the stale copy — against runs at
10:44–11:15. Timestamps checked, not assumed.

**ONE RED THAT DID NOT REPRODUCE, recorded rather than dismissed.** On an intermediate run the
combined check `nord @80: still exactly one cursor, still a bold title` went red once. It was split
into its two halves for diagnosis and **both halves have passed in every run since (4 consecutive,
including the three final ones)** — so the failure was never isolated and its cause is unknown. It is
in the same class as the darkside race (a capture reading a frame in an unexpected state) but in a
NEW code path (`capture_styled`), so it does not inherit that watch's evidence. **Watch it.**

**Measured, and reported because two numbers moved the wrong way.**

1. **Tasks on screen at 118×30: 10 → 7.** The split spends three task rows on a subject. Not a
   rounding error, and not hidden.
2. **The detail pane is sparsely filled — 5 fields in a 77-cell measure at 118 (~35 % used).** A
   sixth datum would need a field `TaskCard` does not receive today, which is exactly the finding
   swiss's third column produced. Deliberately NOT cured by capping the pane: the emptiness around
   the title IS its isolation, and isolation is one of the three levers law 03 is won on. Capping the
   measure would have traded the fixation for tidiness.

**Open after this pass:** (a) **nord's HERO still fails law 03 on its own** — the load plot out-inks
the numeral 61 to 25 inside the same panel; separate item 0e above, and deliberately out of this file
set; (b) the detail pane's sparseness, above — it needs a richer `meta`, not a narrower pane;
(c) the empty state is mounted but below the fold in the scrolling master at 30 rows; (d) the one-off
80×30 red, above; (e) `corgi` and `instrument` are the last two `layout` gaps; (f) Textual's 2-cell
vertical scrollbar sits at the master's right edge (the `▆▆` in the dumps) — it is budgeted for
(`master_w - 3`, nothing wraps) and it is the honest affordance for a list that really does scroll,
but it is chrome inside the composition and worth a look if the master is ever widened.

**Artifacts added (render dumps under `prototypes/out/`, the standing convention, outside the file
budget):** `probe28_nord_118.txt` (the frame the law-03 verdict was read from), `split_nord_118.txt`,
`split_nord_80.txt`, `split_nord_flow.txt`, `_nord_pre.txt` / `_nord_post.txt` (the byte-identity
dumps), `_run28_1..3.txt` (the three final runs).

**Done 2026-07-27 (twenty-seventh pass) — SWISS's `layout="editorial"`: the board becomes a
3-COLUMN TYPE GRID under ONE hairline.** Step 5 of rolling `layout` out; coverage **5 of 8**.
This is a real recomposition, and it cures a promise the code was not keeping: `themes.py` has
described swiss as *"one rule"* since it was written, and the board printed **one rule per phase
head**.

**Before / after, the second masthead at 118×44, verbatim** (`prototypes/out/editorial_swiss_flow.txt`
vs `editorial_swiss_118.txt`):

```
  before (flow)                                             after (editorial)
  D O I N G                                6                D O I N G                          6
  ──────────────────────────────────────────                (no rule — the hairline is spent once)
                                                            Fix checkout 500 error   Website Redesign   blk
  Fix checkout 500 error                 blk                Compress database backups Data Warehouse    blk
                                                            Design homepage mockups  Website Redesign    0d
  Compress database backups              blk
  (2 cards; the rule costs the phase a row)                 (3 cards; the reclaimed row is a card)
```

**What the token owns, stated precisely** (an undefined boundary is an unfalsifiable check): the
**phase head** and the **entry rows** — the same boundary the rail, the ruling, the lattice and the
plate draw. It does NOT own `sect()`, the `hairline` meter, the calendar cells, `tile_row`, or
`composition()`'s editorial measure (`max-width: 78`, hero 9 rows at board size). The flow degrade
asserts all four survive untouched.

- **`themes.py`**: swiss gains `layout="editorial"` and `columns=3`; both documented in the module's
  token list. No other theme touched.
- **The grid.** `Swiss.grid(w)` returns `(origin, measure)` per column and is read by the renderer
  AND by the acceptance check, so "the elements and the columns share the same cells" is true by
  construction (`Ledger.cols`'s precedent). Equal columns, `GUTTER = 3` — in this language the
  gutter is what a rule would have been.
- **The roles, and the order they are renounced in.** 3 columns = **subject · byline · figure**
  (title · project · due chip). 2 columns drop the **byline** first: it is the only one of the three
  that is neither the thing named nor its datum (the ledger tile's law — a clipped row keeps its
  figure). 1 column **is the flow row, verbatim** — the drop rule degrades towards the form it
  replaced and can never be worse than it. Asserted by equality, not by eye.
- **THE DROP RULE, derived from two constants rather than tabulated.** `MEASURE_MIN = 24` (the
  seeded board's titles run 19–24 characters; 24 is the measure at which none is cut) and
  `GUTTER = 3` give the thresholds **3 columns at w ≥ 78, 2 at w ≥ 51, 1 below** — and the checks
  assert `grid(78)==3 / grid(77)==2` and `grid(51)==2 / grid(50)==1`, i.e. the exact cell where each
  column is bought. Measured at five size classes: **w=14 → 1 · 28 → 1 · 51 → 2 · 68 → 2 · 105 → 3**,
  nothing wrapping at any of them. **The narrow board is a real regime, not a hypothetical: the 80×30
  board comes out at 2 columns** (`editorial_swiss_80.txt`), byline renounced, figure kept.
- **The hairline's seat is a decision, not a repetition.** ONE rule for the whole spread, under the
  **leading** phase — the masthead rule. Encoded twice: at kit level *1 of 4 heads carries a rule*,
  and at app level *exactly one rule row in the rendered spread*, with `layout="flow"` as the
  negative control that puts a rule back under **every** masthead (2 of 2 on screen).
- **Flush LEFT on the grid, and that is the load-bearing decision.** `kanban.py` budgets the head
  `avail - 4` and the card its own content box, so the two surfaces are measured apart. Their column
  ORIGINS are identical (`grid(105)` and `grid(107)` agree); their right edges are not. A
  right-flushed figure would therefore land in a different cell in the head than in the entries under
  it, and alignment is this language's entire structure. Asserted on the real board: the masthead's
  count and the entries' figures share a column at 118 **and** at 80.

**The byline took a COLUMN, not a ROW.** Swiss's renunciation of the second card row (a law since the
kit was written) is untouched and still checked — the project it had nowhere to put now has a seat
because the grid gave it one. Before this pass ~70% of every entry's measure was empty.

**Byte-identity, measured rather than assumed.** Kit signatures (head at idx 0–3, `card_row`,
`card_rows`, `sect`, `meter`, `tile_row` at 14/20/28/40/60/105 plus `tcss()`) were dumped before the
change to `prototypes/out/_swiss_pre.txt` and compared after: **the other 7 languages are
byte-identical, 7 of 7** (naught 11314 · corgi 9869 · instrument 6126 · industrial 8409 · nord 7547 ·
darkside 4540 · ledger 13840 bytes, unchanged); swiss moves 8647 → 5728, the loss being 18 rule rows
the spread no longer prints. **And `layout="flow"` restores the pre-change swiss signature
BYTE-EXACTLY** — the previous composition is preserved as the flow path (`_flow_head`,
`_flow_head_line`, `_flow_card_row`), not deleted.

**One thing the harness could not see, and it was a real hole.** `mut_sig` fingerprints every kit
primitive at **column-sized widths only (14–50)** — the whole surface a *columns* language ever gets.
A **sections** language composes a full-width spread, so `swiss.columns` (which needs 78 cells to
show 3 columns) mutated 3 → 2 **with no change at all** and read as dead metadata: the check went red
on the first run and it was the instrument, not the token. `mut_sig` now also fingerprints the BOARD
measure (entry at 105, heads at 106 × idx 0–2). This widens the mutation net for all eight languages.

**Counts: verify_language 739 → 808 (+69), and the arithmetic closes.** Kit level **+45**: the token
declaration (1), 3 columns at board measure + equal-and-guttered + head/entry origins agree (3), the
entry and the masthead set on the grid's origins (2), ONE hairline + it is the masthead's (2), the
byline is a column not a row + it is information flow had nowhere to put (2), **the drop rule at five
size classes, each asserted twice** (grid tier + nothing wraps; the figure survives) (10), the two
thresholds asserted at the exact cell (2), no column below `MEASURE_MIN` (1), the 1-column tier IS
the flow row (1), first fixation — the masthead takes the entries' ink, takes no accent, and the
loudest element is the smallest (3), `columns=2` mutation live + renounces the byline first +
restores (3), **the dispatch law across all 8** (rule-under-the-leading-phase-alone IFF token) (8),
and seven degrade checks including *`sect` is left alone*, *the hairline meter is left alone*, *the
calendar is left alone* and *the composition restores*. App level **+20**: two mastheads on screen
(probe self-check), exactly one hairline, the fixture entry on screen, the three elements on the
grid's origins, the masthead's left edge and its count's column (6); the air rows survive (1); ink
fraction under industrial's and inside the airy band (2); no wrap at 118×44 (1); the flow degrade —
board kept, **every masthead ruled again as the negative control**, bylines stripped, board changed
(4); `columns=2` reaches the live board (1); and the narrow regime at 80×30 — no wrap, the drop
FIRED, the figure on the second column's origin, masthead/figure share the column, still one hairline
(5). **+4** falls out of the ALT table now covering `swiss.layout` and the new `swiss.columns`
(`is live` · `restores cleanly` each). 45 + 20 + 4 = 69. Three permanent render dumps added:
`editorial_swiss_118.txt`, `editorial_swiss_80.txt`, `editorial_swiss_flow.txt`.

**Measured, and reported because it moved the wrong way in one place.** The board's ink fraction at
118×30 is **10.4% for swiss against 37.6% for industrial** — swiss remains the airy one by a factor
of 3.6. Restricted to the *spread* at 118×44 the editorial grid is **14.6% against the flow render's
14.2%**: the bylines add ink and the deleted rule rows take it away, and the two nearly cancel. There
is no airiness *improvement* to claim; the claim is that the measure now carries information where it
carried nothing, at unchanged ink.

**Runs: 3/3 back-to-back green on the final state, 808 checks each, exit 0.** `verify_aperture` **17
ALL PASSED** — swiss's grid does not appear there at all (`aperture.py` calls no `head`/`card_rows`;
grep-verified), so the aperture's no-wrap law is untouched rather than newly satisfied; that is a
weaker statement than "the grid degrades correctly in the aperture" and is the honest one.
`verify_widget` **24 ALL PASSED**, redraw **1348 µs = 8.09%** of a 60 fps frame (H ≥ 5 holds) ·
`verify_board` **22 ALL PASSED** · `pytest tests` **137 passed**, no clipboard flake.

**The darkside capture race DID fire once this session, and not on the final state.** It hit an
intermediate run at 10:29 (4 checks red — the probe self-check plus its three dependents, exactly the
named signature; 737 of 741 passed) and wrote `prototypes/out/_race_darkside.txt`, which is left in
place as evidence. It did not fire in the six runs after it, including the three final ones. Not
chased, per the standing instruction.

**Open after this pass:** (a) the `layout` roll-out is **5 of 8** — corgi and instrument are the
remaining real gaps (nord's `flow` is honest); (b) **`kanban.py`'s head budget (`avail - 4`) still
does not match the card's content box**, which is why the grid is anchored left rather than right —
this is the same defect already recorded for ledger's head rule (item 4 below), now with a second
language depending on the workaround; (c) swiss's spread still has no seat for the empty state (the
sections branch of `kanban.py` never mounts `k.empty()`) — unchanged, item 7 below; (d) the third
column is sparsely filled (a due chip in a 33-cell measure); giving it a second datum would need a
field the card does not receive today.

**Done 2026-07-27 (twenty-sixth pass) — `verify_board` GETS THE TWENTIETH PASS'S CURE: fixture,
settle, guard.** Closes the twenty-fifth pass's open item (d). No app code touched; this is entirely
harness work on `prototypes/verify_board.py`.

**What it was.** Every one of the seven apps this suite launched was `TaskboardWidget()` with no
argument, i.e. `default_board_path()` — **the user's live `~/.taskboard/board.json`**, which the
desktop app rewrites underneath a running suite. Every frame read was a single `pilot.pause()`. That
is exactly the recipe the twentieth pass measured at ~1 red in 3 for `verify_language`, and it is why
`board still readable with animations disabled` went red once here and then passed 13 of 14.

**What it is now**, the same three pieces `verify_language` carries:

- **`seed_fixture()`** writes `prototypes/out/_fixture_board_vb.json`, unlinking it first so
  `Board.load`'s today-anchored `seed_data()` runs fresh every time. It then **empties the middle
  phase into the first** (Backlog 13 · Doing 0 · Done 2), because the cursor checks were written
  against a live board that had an empty column — without that shape the `right` check has nothing
  to skip.
- **`launch(board_path=None, **kw)`** is the only place a `TaskboardWidget` is constructed in this
  file (grep-verified: one call site), and it **raises** on `board_path=None` —
  `"launch() requires an explicit fixture board_path; probing the live board.json is forbidden"`,
  mirroring `capture()`'s message. An unfired guard is a comment, so the guard is itself a check.
- **`settle(app, pilot, label)`** — a local copy of `verify_language`'s, deliberately: the two files
  share no helpers today (each defines its own `screen_text`) and importing across them would make
  one file's probe discipline depend on the other's imports. Same condition (every compositor-visible
  card has painted pixels in its clipped area · two identical consecutive frames), same
  `SETTLE_MAX = 40`, same loud-timeout-is-a-FAIL, same headroom canary. **The file now contains
  exactly one `pilot.pause()`, and it is inside `settle`.**

**Counts: 18 → 22 checks (+4), and the arithmetic closes.** +3 probe self-check (the fixture seeded
work · the fixture really leaves a phase empty · the guard fires) and +1 settle headroom. No check
was removed.

**Two check MEANINGS changed, and neither is a silent shrink:**

1. **`` `right` skipped the empty phase `` was VACUOUS and is now real.** As written it asserted
   `len(kb.cards[after.col]) > 0` — a landing column with cards, which says nothing about a skip. It
   now asserts `after.col > before.col + 1` as well, and the fixture is shaped to give it an empty
   column to jump. Measured: `col 0 -> 2`, `cards in the skipped column: 0`.
2. **The motion sample went from 8 ticks to a FULL PERIOD (20).** `motion.build_flow` precomputes 20
   frames and sweeps the packet across the whole span in those 20, so a short bar sits inside the
   packet's path for only a few of them. The live board carried a project whose bar spanned most of
   the axis (measured: 8/8 distinct renders), and 8 ticks caught it; the fixture's projects span
   weeks, not months, and **8 ticks sampled a stretch of axis their bars never touch — the gantt
   check went red on the first fixture run, and it was the fixture, not `settle`** (isolated by
   calling `render_gantt` directly: the fixture gives 6 distinct renders over 8 ticks at the row
   level, but the two project rows the screen actually shows are not among the movers). `TICKS` is
   read from `len(MO.build_flow(10))`, so it cannot drift from the motion module. Sampling the period
   is what the check always meant.

Numbers that move with the fixture, same laws: 28 cards / 4 phases → **15 cards / 3 phases**; the
frame-integrity widths report 3 columns instead of 4 (`w=80 [40,13,17]` … `w=200 [144,13,33]`).

**Runs: 10/10 back-to-back green, 22 checks each, exit 0** — the bar for a probe measured at ~1-in-14
flaky:

| run | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| exit | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| checks | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| verdict | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED | ALL PASSED |

Settle headroom **worst 5 of 40 over 62 settles**, identical in all ten runs — the loop is
load-bearing (5 iterations, not 1) and there is 8× margin to the bound. Runtime 9.3 s per run.

**The other suites, run once each after the change:** `verify_language` **739 ALL PASSED** (unchanged
— the coupling check; the darkside race did not fire, its own headroom worst 4 of 40 over 35
captures) · `verify_aperture` **17 ALL PASSED** · `verify_widget` **24 ALL PASSED**, redraw
**1470 µs = 8.82%** of a 60 fps frame (H ≥ 5 holds) · `pytest tests` **137 passed**, no clipboard
flake.

**Open after this pass:** (a) `verify_ink.py` and `verify_widget.py` were NOT audited for the same
live-board probe — they were outside this increment's file budget and neither has been seen to flake,
but the class is now known and cheap to check; (b) the two `settle` implementations are duplicated
across `verify_language.py` and `verify_board.py` — folding them into a shared
`prototypes/_harness.py` is a real cleanup, deliberately not taken here (it would touch
`verify_language.py`, which this increment was told to leave alone); (c) the darkside capture-race
watch is unchanged.

**Done 2026-07-27 (twenty-fifth pass) — INDUSTRIAL's `layout="panel"`: the box frame goes, FUNCTION
PLATES arrive.** Step 4 of rolling `layout` out. Unlike naught's formalization this is a real
recomposition — and the claim that motivated it in the external spec is FALSE, so the framing below
is identity deepening, not a rescue.

**THE COLLISION CLAIM WAS PROBED FIRST AND IS FALSE.** The spec asserted industrial "reads as corgi"
in greyscale (a law-01 failure). Colour-stripped 118×30 board captures of both
(`prototypes/out/probe25_industrial.txt` · `probe25_corgi.txt`) share nothing at a glance:
**industrial** is boxed readouts (`┌───┐` around meter and tiles), `▪` bullet cards, mixed-case
titles and a bracketed tag row (`[PH:BACK][DUE:3D][PR:H]`); **corgi** has no box anywhere — full-width
aluminium hairlines between modules, `▄▄` LCD segment bars, letterspaced `B A C K L O G` heads,
`[1]`-numbered ALL-CAPS cards and a printed spec line (`DUE 3D  PH BACKLOG PR H`). Measured:
**20 of 30 board lines and 47.5% of board CELLS differed before this pass**, and the harness's own
`corgi != industrial` pair check has been green throughout. The recomposition landed anyway, on a
different and real defect: industrial's board composition was the base skeleton plus a `frame` rule,
i.e. a composition its tokens did not own — PENDING item 0's exact shape.

**The honest after-number, which moved the WRONG way: 47.5% → 45.3% of cells differ (−2.2 points).**
Both languages now indent their card rows, so more blank cells line up. There is no distinctness
improvement to report. It remains an order of magnitude away from a collision, and the check that
encodes it (`> 0.30`) is a law a real collision would break, not a tautology.

**What `layout="panel"` owns, stated precisely** (an undefined boundary is an unfalsifiable check):
the **column head** and the **card rows** — the same boundary the rail, the ruling and the lattice
draw. It does NOT own `sect()`, the boxed `meter` (that answers to `meter`, and the flow degrade
asserts it comes back byte-identical), the bracketed icons/chips, or the `#meter`/`#tiles` borders in
`composition()` — those are panel chrome, not the board.

- **`themes.py`**: industrial gains `layout="panel"` and `plate="#2e2e2e"`; both documented in the
  module's token list. No other theme touched.
- **The legend.** The head's `frame="single"` rule is GONE. A phase now names its stack from a solid
  `plate`-toned band led by a `▐▌` tab — HIERARCHY.md ranks a shared background (mechanism 2) above
  a rule (mechanism 3), and a rule cost the board a whole row.
- **The plate.** Every card is a two-row block on the plate ground, stamped `▐ 01 ▌` with its
  position code (`idx` from `TaskCard.row`, the seat corgi numbers from). The tag row hangs under
  the plate's right edge on the same ground, so a task reads as ONE block.
- **Progressive, and the tight tier KEEPS ITS NUMBER: `▐ nn ▌ ` (7 cells) → `▐nn ` (4).** Both come
  out of the content budget. Threshold `CODE_MIN = 24`; `plate_w(w)` predicts the width before the
  row is drawn (naught's `plain_width` lesson) and the acceptance check asserts the prediction.

**Three defects the RENDER caught that green checks had not** (the fifth pass of this lesson):

1. **The first tier design renounced the code below the threshold**, and the 118 board came back with
   BACKLOG wearing `▐ 01 ▌` beside DONE wearing a bare `▐`. Two adjacent columns in different plates
   reads as a bug, not a decision. The tight tier now gives up three cells of plate, never the number.
2. **`.col-head { padding-left: 1 }` WRAPPED the legend.** That is how darkside's rail cured its
   zigzag, and it is wrong here: this legend fills its measure exactly and has no slack to absorb a
   narrower content box, so `[ 7]` folded to a second line and cost the board a row — the same trap
   `#ap { padding: 1 3 }` sprang on the ledger page. The cell is now paid IN THE MARKUP (the legend
   opens with a space and budgets `w - 1`), and the edge is asserted, not eyeballed.
3. **The app-level code check read the wrong column.** `str.index` on a shared board row returns
   whichever column happens to hold a card there; it is now anchored to the leading column's edge.

**One deviation from the approved external spec, because the SKILL and the palette overrule it.**
The spec's component table says *"the focused plate turns accent"*. Declined, and flagged rather
than silently taken: industrial's `accent` and `alert` are **the same hex (`#ff4b1f`)**, so an
accent-ground plate would be indistinguishable from an overdue one — HIERARCHY.md's reservation rule
says a semantic hue is used for nothing else. Mechanically it is also impossible as specified: the
plate is painted in the MARKUP, which composites over the widget background, so a TCSS `:focus`
background never reaches those cells. Selection therefore stays `sel="solid"` — the accent left
border, which is the mechanism HIERARCHY.md **reserves** for focus, and which survives the plate on
two channels (an edge glyph the unfocused rows lack, plus the hue).

**Byte-identity, measured rather than assumed.** Kit signatures (head · card_row · card_rows at
14/20/28/40/60, plus `sect`, `meter` and `tcss()`) were dumped before the change to
`prototypes/out/_industrial_pre.txt` and compared after: **the other 7 languages are byte-identical,
7 of 7** (naught 3902 · corgi 2493 · instrument 1901 · swiss 1704 · nord 1539 · darkside 1812 ·
ledger 3706 bytes, unchanged); industrial moves 2219 → 2679. **And `layout="flow"` restores the
pre-change industrial signature BYTE-EXACTLY** — the previous boxed composition is preserved as the
flow path (`_flow_head` / `_flow_card_row` / `_flow_card_rows`), not deleted.

**Counts: verify_language 678 → 739 (+61), and the arithmetic closes.** Kit level **+35**: the token
declaration (1), every card stamped + codes two-digit/sequential/unique (2), the legend tab (1),
**the box frame is gone** (1), the solid-block and code-survives laws at five size classes (10), the
wide tier / tight tier / `plate_w` prediction (3), the floor-width plate keeps its CHIP (1), both
card rows + the legend on the `plate` ground (2), the plate survives greyscale on SHAPE not ground
(1), the dispatch law across all 8 (plate-IFF-token) (8), and five degrade checks including *the
boxed meter is left alone* and *the composition restores cleanly*. App level **+22**: the card is on
screen (probe self-check), the plated rows, one legend per phase, the leading column's codes, the
ONE unbroken edge, the box frame gone from the REAL board, no wrap at 118 (7); the flow degrade on
the live board — board kept, **the rule row comes BACK as the negative control**, plates stripped,
board changed (4); **seven no-leakage checks** (no other language emits a plate or a `▐▌` legend);
the corgi cell-distinctness law (1); and the narrow regime at 80×30 — no wrap, every card still
coded, legends still banding (3). **+4** falls out of the ALT mutation table now covering
`industrial.layout` and the new `industrial.plate` (`is live` · `restores cleanly` each). 35 + 22 +
4 = 61. Three permanent render dumps added: `panel_industrial_118.txt`, `panel_industrial_80.txt`,
`panel_industrial_flow.txt`.

**Runs: 3/3 back-to-back green on the final state, 739 checks each, exit 0 — and the darkside capture
race did NOT fire in those three** (settle headroom worst **4 of 40** over 35 captures, unchanged).
**It DID fire once earlier in the session**, on an intermediate state, with exactly the four named
checks (`darkside: the fixture card is on screen (probe self-check)  0 row(s)` plus the three that
depend on it); the evidence dump was written and then cleared before the final runs. Not chased, per
the standing instruction. `verify_aperture` ALL PASSED · `verify_widget` ALL PASSED, redraw
**1344 µs = 8.06%** of a 60 fps frame (H ≥ 5 holds) · `pytest tests` **137 passed**, no clipboard
flake.

**`verify_board` went red ONCE and it is NOT attributable to this pass — but it is new and is
recorded, not dismissed.** The check was `board still readable with animations disabled`, which
reads the **live board.json** (verify_board has no `capture()` guard and no `settle()` — it takes a
single `pilot.pause()`), and `app.py`'s module default `THEME = "instrument"` is the language under
test there; instrument's kit is byte-identical pre/post. **13 of 14 runs green** since. It is the
same mounted-but-unpainted class as the darkside race, in a suite that never got the twentieth
pass's cure. **Owed: give `verify_board` the fixture + `settle()` discipline.**

**Open after this pass:** (a) the `layout` roll-out is **4 of 8** — corgi, instrument and swiss are
the real remaining gaps (nord's `flow` is honest); (b) industrial↔corgi cell-distinctness dropped
2.2 points and the `▐`/`▌` half-block pair is also corgi's switch idiom (different surface, but the
glyph family is now shared — watch it if corgi ever gets a `layout`); (c) the plate covers the
`.kb-card:focus` background, so selection rests on the accent border alone; (d) `verify_board`'s
live-board probe, above.

**Done 2026-07-27 (twenty-fourth pass) — THE STROKE LANDS WHERE THE USER LOOKS: naught's column-head
count sprites.** The twenty-third pass proved the cure and then measured that its seat was
unreachable (the hero's drawn caption needs 13 rows; no composition gives more than 11). This pass
moves the same mechanism to the seat every naught screen actually shows — the board's head counts —
and the change IS visible.

**Before / after, the 118x30 board, rows 18-22 verbatim** (`prototypes/out/_head_board_pre.txt` vs
`lattice_naught.txt`):

```
  before                                    after
  ∙∙∙        ∙∙∙        ∙∙∙                 ∙∙∙∙∙∙     ∙∙∙∙∙∙     ∙∙∙∙∙∙
  ◦◦∙        ∙◦◦        ◦◦∙                 ◦◦◦◦∙∙     ∙∙◦◦◦◦     ◦◦◦◦∙∙
  ◦◦∙        ∙∙∙        ∙∙∙                 ◦◦◦◦∙∙     ∙∙∙∙∙∙     ∙∙∙∙∙∙
  ◦◦∙        ∙◦∙        ∙◦◦                 ◦◦◦◦∙∙     ∙∙◦◦∙∙     ∙∙◦◦◦◦
  ∙∙∙        ∙∙∙        ∙∙∙                 ∙∙∙∙∙∙     ∙∙∙∙∙∙     ∙∙∙∙∙∙
  (7 · 6 · 2 — 3 cells wide, one-cell       (the same 7 · 6 · 2 — 6 cells wide,
   strokes, letters parted by a BLANK)       every stroke 2 cells, parted by UNLIT dots)
```

**The mechanism, in one seat so it cannot fork.** `taskboard/naught.py`'s `label()` gains
`sx` (the horizontal pixel) and `fill` (stand on the continuous lattice instead of padding with
blanks); `plain_width()` mirrors both, so the caller can ASK how wide a form will be before
choosing it. `fill=True` goes through the same `BS.from_font -> BS.scale -> field` path
`hero.dense_type` uses, so the head and the hero draw the same letters. The legacy branch
(`sx=1, fill=False`) is preserved verbatim and is still the default — which is why the twenty-third
pass's negative control ("the form it replaced DID have one-cell strokes") still fires.

**The width-budget rule, stated so it can be disproved: progressive, x2 -> x1, never wrapped.**
A sprite wider than its column would wrap, and a wrapped head costs the board a CARD ROW. So
`Naught.head` asks `plain_width(digits, dot_w, gap, 2, True) <= w - 1` and takes x2 only when the
column pays for it; otherwise x1, which is 7 cells — the exact width the sparse form already had,
so the fallback can never be wider than what it replaces. Measured at the five size classes
(2-digit count, `dot_w=1`, `gap=0`): **w=14 -> x1 (7 cells) · w=20/28/40/60 -> x2 (14 cells)**, row
count 6 (caption + 5) at every one of them. In the real app the narrowest column is ~26 cells
(80-wide board), so **every screen gets x2**; the x1 tier exists for the kit's floor, and is
checked there.

**Seats cured: the head (`Naught.head`) and the drawn section titles (`Naught.sect`).** sect takes
the same progressive rule against its own measure — "AGENDA" is 46 cells at x2 and fits w=50,
falls to x1 (23 cells) at w=30. **Seat NOT cured, and why: the wordmark** (`Naught.wordmark`) takes
no width argument, so no progressive rule can be written for it without changing its signature and
its one caller (`prototypes/widget_slice/app.py`'s gallery, outside this file set). It is the last
sparse drawn seat; it is off the real app's screens.

**Cards per column did NOT change, measured two ways:** the head still costs the board exactly 6
rows (caption + 5 sprite rows — the stroke widened the sprite, it did not lengthen it), and the
third card ("Shut down legacy servers") still has its seat at 118x30, 92x30 and 80x30. Both are
now checks, not claims.

**Byte-diff scope, measured rather than assumed.** The pre-change `Naught.head`/`Naught.sect`
bodies were rebound at runtime and every language's kit signature (head at 4 widths, sect typographic
+ display, wordmark, card rows, meter, tcss) compared: **the other 7 languages are byte-identical,
7 of 7** (corgi 1728 · instrument 1223 · swiss 1254 · industrial 1533 · nord 1088 · darkside 1080 ·
ledger 2344 bytes, unchanged); naught moves 3107 -> 3458. On the rendered 118x30 board the diff is
**exactly rows 18-22**, the five sprite rows, total board bytes unchanged at 3540.

**Counts: verify_language 630 -> 678 (+48), and the arithmetic closes.** Kit level **+37**: the
sprite renders (1), no one-cell stroke (1), no plain cell (1), round dots only (1), the two negative
controls — the replaced form fails BOTH laws (2), the doubled width (1); the width budget at five
size classes, each asserted twice (fit-and-row-count, and `plain_width` predicting the drawn width)
(10); the x1 tier engages / stays on the lattice / x2 taken at w=20 / one-digit count / empty column
(5); **the no-wrap law generalised to all 8 languages at all 5 size classes** (8); the flow degrade
and its restore (2); sect's five (5). App level **+11**: the head band on the real board (probe
self-check), no one-cell stroke, round dots only, each sprite one solid run of >= 6 cells, three
sprites and no more (5); the head still costs 6 rows and the third card keeps its seat (2); and the
narrow regime at 80x30 — band renders, stroke holds, three sprites that do not run together, three
cards (4). 37 + 11 = 48. New permanent render dump: `prototypes/out/lattice_naught_80.txt`.

**Runs: 3/3 back-to-back green, 678 checks each, exit 0 — the darkside capture race did NOT fire**
(`prototypes/out/_race_darkside.txt` never written; settle headroom worst **4 of 40** over 33
captures, unchanged from the previous pass). `verify_aperture` ALL PASSED · `verify_widget` ALL
PASSED, redraw **1387 us = 8.32%** of a 60 fps frame (H >= 5 holds) · `verify_board` ALL PASSED ·
`pytest tests` **137 passed**, no clipboard flake.

**Open after this pass:** (a) the **wordmark** is the last sparse drawn seat (needs a width
argument); (b) the hero's row budget, if its drawn caption is ever to be seen (13 rows against
today's 11) — unchanged by this pass; (c) `motion="bloom"` still undeclared; (d) `hero.dense_type`
could now be a two-line call into `naught.label(..., fill=True)`; it was left alone because
`taskboard/hero.py` was outside this increment's file budget.

**Done 2026-07-27 (twenty-third pass) — `hero="naught7"`, the DENSE display type. And the finding
that matters more than the code: THE USER'S DEFECT IS NOT IN THE HERO.**

User verdict: *"the pixels of the larger letters should be a bit denser — I find them hard to read,
they're somewhat separated."* This pass built the cure and then **measured where the defect actually
is**. Both halves are below; the second one is the one to act on.

**What was built — `naught7`, a real base.** `themes.py` naught: `hero="naught"` → `hero="naught7"`
(the token doc lists the mechanism). `taskboard/hero.py` gains two primitives both seats call, so
the drawing cannot fork again: `dense_type(text, on, off, width, dot_w, gap, sx)` — a word drawn
through the 3x5 dot alphabet on the **full-bleed lattice**, and `dense_rule(width, off, ...)` — the
band separator as an **unlit lattice row**. The naught7 branch composes numeral band + separator +
caption band(s) into ONE panel in which **no cell is a plain space**: every cell is `∙` or `◦`, the
EAW-Neutral pair, unchanged. `prototypes/widget_slice/app.py` (the seat `RUN.md` launches) now
dispatches `naught7` and calls the same two functions instead of keeping a third copy of the
drawing.

**The mechanism, stated so it can be disproved.** The form it replaces (`naught.label`) puts a
BLANK cell between letters, pads the band with spaces and draws one cell per pixel, so every stroke
is a single cell — that is what "separated" means, mechanically. `dense_type` at pixel `sx=2` gives
the cell's 1:2 aspect back: **every stroke is 2 cells wide** and the surround is unlit dots, not
void. Progressive, all-or-nothing per tier: **x2 dense → x1 dense → typographic**. The middle tier
exists because at 92 cells the x2 caption wraps to two bands and the old code **silently dropped the
second one** — the hero printed "DAYS" where the fact was "DAYS OVERDUE". That is a real latent bug
this pass killed; drawing half a caption is now impossible by construction.

**THE REACHABILITY FACT — read this before believing the fix is visible.** A drawn band costs its
separator + 5 rows on top of the 7-row numeral: **13 content rows**. Measured in the running apps,
naught's hero gets **7** content rows at board size (`widget.tcss:113` / `language.py:1241` set
`height: 9`, less the focus border) and **11** at widget size (`max-height: 15`). The real app's
aperture is capped at **12** by `verify_aperture`'s own no-wrap law. **So no seat in either app
reaches the drawn caption — before this pass or after it.** naught's drawn hero caption has been
dead code since the thirteenth pass wrote it; what every screen actually shows is the 7-row numeral
plus a *typographic* caption. The renunciation is correct (type clipped mid-glyph is mush), and it
is now asserted rather than assumed. **Consequence, stated plainly: the user will see no change in
the app from this pass.** Raising the budget means the hero's height in `widget.tcss` /
`language.composition()`, which is composition and was outside this file set.

**Where the user's defect actually is — LOOK at `prototypes/out/lattice_naught.txt`.** The drawn
glyphs on screen are the board's **column-head COUNT sprites** (`naught.label()` via
`Naught.head`), and they are **3 cells wide by 5 rows** at `dot_w=1` — in a 1:2 cell aspect that is
a 3×10 sliver with one-cell strokes and a blank cell between letters. Same for `sect()`'s drawn
titles and the wordmark. **That is the "larger letters, hard to read, somewhat separated".** All of
it lives in `taskboard/language.py`, which this increment was told to treat as read-only. The cure
is already written and proven: give `naught.label` (or `Naught.head`) the same `sx` pixel
`dense_type` uses. **This is the named next increment.**

**Counts: verify_language 581 → 630 (+49), and the arithmetic closes.** Draw level **+34**: the
token declaration (1), the 7-row numeral (1), the density law — no plain cell in the glyph field
(1), the round-dot-only law (1), **no one-cell stroke** (1, the check that encodes the user's own
words) with the replaced form as its **negative control** (1) and the doubled letter width (1), the
caption drawn on the same field (1), the separator is an unlit row (1), the typographic fallback and
its budget (2), all-or-nothing (1), the x1 tier (2), the reachability fact (1), no-wrap at 5
geometries (5), `dim` mutation is live + restores + tone + zero-red calm (4), `hero` dispatch +
degrade + restore (3), and no-fill-leak for the other 7 languages (7). App level **+15**: the hero
paints its band (probe self-check), the rendered field has no plain cell, is round dots only, has no
one-cell stroke, is full-bleed to the hero's left edge (5), seven no-leak checks on the other
languages' *hero regions* (7), and three live-hero dispatch checks — `hero=plain` removes the
display type, **keeps the load plot's dots** (they answer to `meter`, the same boundary `layout`
draws), and still paints. 34 + 15 = 49. New permanent dump: `prototypes/out/naught7_hero.txt`.

**Byte-identity, measured rather than assumed: 30 of 32 hero renders unchanged.** All 8 languages ×
4 geometries were dumped to `prototypes/out/_hero_pre.txt` before the change and compared after:
**the 7 other languages are byte-identical at 28 of 28**, and naught is identical at the two
geometries whose budget renounces the drawn caption (46×12, 60×8). Only naught 92×16 and 118×20 —
the geometries where the band fits — differ, which is the whole intended blast radius.

**Runs: 3/3 back-to-back green, 630 checks each, exit 0 — and the darkside capture race did NOT
fire** (`prototypes/out/_race_darkside.txt` was never written). `verify_aperture` ALL PASSED (the
hero ≤ 12 no-wrap law holds with the 7-row type) · `verify_widget` ALL PASSED, redraw **1589 µs =
9.5%** of a 60 fps frame (H ≥ 5 holds) · `verify_board` ALL PASSED · `pytest tests` **137 passed**,
no clipboard flake this session.

**Open after this pass:** (a) the head-count sprites above — the real defect, next increment;
(b) the hero's row budget, if the drawn caption is ever to be seen (13 rows against today's 11);
(c) `motion="bloom"` still undeclared, for the same reason as ever: no renderer reads it;
(d) the prototype Hero and `taskboard/hero.py` still duplicate the OTHER five hero mechanisms —
only naught7's drawing was folded onto shared functions this pass.

**Done 2026-07-27 (twenty-second pass) — NAUGHT's composition becomes a TOKEN: `layout="lattice"`.**

Step 1 of rolling `layout` out to all eight languages. Naught already rendered the round-dot
lattice; this pass FORMALIZES it so law 04 holds — *composition is a token, not a constant*.
Nothing about the look changed, which is the point: the mechanism moved from the class name to
the theme entry, where it can be mutated, dispatched and disproved.

- **`themes.py`**: naught gains `layout="lattice"` (one line). No other theme touched. Coverage
  is now **3 of 8** — darkside `rail` · ledger `ruled` · naught `lattice`.
- **`language.py`**: `Naught.lattice` (a property, the same dispatch shape as `Darkside.rail_width`
  and `Ledger.ruled`) now gates the three BOARD surfaces — `head`, `card_row`, `card_rows`. Under
  any other value they fall through to `super()`, i.e. the generic flow composition.

**What the token owns, stated precisely** (an undefined boundary is an unfalsifiable check):
the head's count as a DRAWN 3x5 sprite standing on unlit dots (6 rows), the card's gap closed by
dot LEADERS instead of blank cells, and the card's second row riding the lattice (phase pips +
the 2-dot state icon). It does NOT own the dots that carry QUANTITY or IDENTITY — the dotgrid
meter, the calendar cells, the queue marker, the tabs, the icons, `sect`'s drawn display type.
Those answer to `meter`, `frame` and their own mechanisms, and the flow render is asserted to
KEEP them. Same boundary darkside's rail draws (head + card rows, `sect` untouched).

**Byte-identity, measured both ways, not assumed:**

- **Kit level: identical, 9173 bytes.** `head`/`card_row`/`card_rows`/`sect` at five widths
  (14/20/28/40/60) plus `meter` and `tcss()`, dumped before the change to
  `prototypes/out/_naught_pre.txt` and compared after — equal.
- **App level: identical, 4029 bytes.** The 118x30 hero-masked board frame, captured by the
  suite itself before and after (`prototypes/out/_naught_board_pre.txt` vs
  `lattice_naught.txt`) — equal. The other 7 languages' app-level renders are covered by the
  existing pairwise section, which stayed green at the same count.

**The degrade is real and was LOOKED AT** (`prototypes/out/lattice_naught_flow.txt`): at
`layout="flow"` the heads print `BACKLOG 7▃` instead of six rows of drawn dots, the leaders are
gone, the second row becomes the base `project · phase` text — and, because the head drops from
6 rows to 1, the board fits **five** cards per column instead of three. The tabs row and the
signal tiles keep their dots, exactly as specified above.

**Counts: verify_language 548 → 581 (+33), and the arithmetic closes.** Kit level **+18**: the
token declaration (1), the three signature commitments (3), the gap-0 density law (1), the
dispatch law across all 8 languages (8 — lattice-IFF-token, the shape the rail and the ruling
are already held to), and five degrade checks including *the meter's dots survive* and *the
composition restores cleanly*. App level **+13**: the card is on screen (probe self-check), it
wears its leaders on the real board, the sprite rows reach it, **seven no-leakage checks** (no
other language emits `∙`/`◦` anywhere on its board), and three live-board dispatch checks —
`naught.layout=flow` strips the leaders from the SAME card row while the row itself stays on
screen. **+2** falls out of the ALT mutation table now covering `naught.layout` (`is live` ·
`restores cleanly`). 18 + 13 + 2 = 33. Two permanent render dumps added
(`lattice_naught.txt`, `lattice_naught_flow.txt`), the ledger_{w}.txt pattern.

**Runs: 4/4 back-to-back green on the final state, 581 each, exit 0 — and the darkside capture
race did NOT fire** (5 post-change runs including one intermediate; zero occurrences,
`prototypes/out/_race_darkside.txt` was never written).
`verify_aperture` ALL PASSED · `verify_widget` ALL PASSED, redraw **1375 µs = 8.25%** of a 60 fps
frame (H ≥ 5 holds) · `verify_board` ALL PASSED · `pytest tests` **137 passed**, no clipboard
flake in this session's runs.

**Not implemented, deliberately, and recorded as open items rather than declared as tokens:**
the spec's `hero="naught7"` (7-row numeral — needs `taskboard/hero.py`, outside the file budget)
and `motion="bloom"`. Declaring a token no renderer reads is PENDING item 0's exact defect.

**Done 2026-07-27 (twenty-first pass) — LEDGER, the 8th language, and the ONE light ground.**

Double-entry bookkeeping as a design language. It is the only theme printed on paper
(`ground=#e9e1cf`), and that single decision is what makes it unmistakable with the colour
stripped off — every other language glows, this one is read. Measured, not asserted:
luminance 0.76 against a brightest-other of 0.03 (naught/darkside are pure black), ink-on-paper
contrast **14.1:1**.

**The mechanisms** (all in `taskboard/language.py`, class `Ledger` + `_meter_tally`):

- **The ruling.** Structure is money columns, not boxes: a folio gutter, then vertical rules
  between description · account · figure. Every rule position comes from ONE function,
  `Ledger.cols(w)`, which the renderer and the acceptance check both read — so "the rules and
  the content share the same cells" is true by construction and asserted at 40/80/118 (the
  check compares the actual `│` indices against `cols()`, and the row length against `w`).
  Narrow pages RENOUNCE columns rather than crush them (4 fields at 120 → 3 at 28 → 2 at 14).
- **Dot leaders** close every gap between a name and its figure — the postings, the account
  headings, the section captions, the tiles. Law: inside the description field there is no run
  of two spaces. On a ledger page an open gap is where a figure could be forged.
- **Double entry.** Every task posts TWO lines: the debit line (title · phase account · figure)
  and the contra line (the project, indented, with the state code). `card_rows` is the anatomy.
- **The tally** (`meter="tally"`, a new METERS entry): marks in groups of five, capped at six
  groups — past thirty marks nobody counts, they estimate, and estimating is what a bar is for.
  Unlit positions keep a leader dot, so fill and track differ by SHAPE (DATAVIZ law 1). The
  same family drives `spark` (ramp `" ·:▪"`), `plot` (marks on a leader baseline) and `gauge`.
- **The band.** Every 5th LINE of the page carries the `band` tint — lines, not entries: a
  posting spends two of them. Verified in the RENDERED FRAME, not just the markup: at 118×30
  the compositor paints 214 cells of `#e0d7c2` (exactly the two banded lines).
- **Red is literal debt.** `alert` appears on overdue postings, the overdue calendar day and the
  `o/d` icon — nowhere else. Law: a page with nothing overdue contains ZERO of the alert hex
  (the naught ration pattern, 19 primitives on one calm surface).
- **Selection is a MARGIN mechanism**: `sel="none"` — the language spends no border at all, so
  focus is the row's tint plus its weight. Asserted by parsing `themes.tcss("ledger")` and
  requiring every `border`/`border-left` style to be `none`, with naught as the control that
  proves the check can fail.

**Three deviations from the approved external spec, each because the SKILL or the codebase
overruled it. Flagged, not silently taken:**

1. **`accent` is the clerk's blue-black pen (#2b3a67), not the red.** The spec set
   `accent = warn = alert = #a8261f`. This codebase spends `accent` on chrome that carries no
   meaning — the Footer key glyphs, the config cursor, the focus edge — so an accent-red ledger
   would print red on decoration and the hue would stop meaning "owed". HIERARCHY.md is
   explicit: a reserved semantic hue is used for nothing else. Keeping the red for debt alone
   is what makes the zero-red law true rather than decorative.
2. **`hero="plain"`, `base="ascii"`** — not `hero="figure"`, `base="slab"`. Those need
   `taskboard/hero.py`, which was out of the file budget; declaring tokens no renderer reads
   would have recreated PENDING item 0's exact defect (a manifest, not code). The drawn slab
   numeral is the named next increment.
3. **The meter's figure sits TIGHT against its marks**, un-leadered. Leaders bind a name to a
   DISTANT figure; here the figure is already adjacent, and filling the gap with the same dot
   the unlit tally uses hid where the count ended — measured: the groups of five stopped being
   readable, and the check I had already written caught it.

**Four defects the RENDER caught that green checks had not** (the fourth pass of this lesson):

- **The tile lost its figure.** `tile_row` padded to the full width, so app.py's 4-cell icon
  prefix pushed the value off the clipped end — the widest size class showed six chrome labels
  and no data, which is the exact bug app.py's own comment records from an earlier session. The
  row now budgets `ICON_W` out of its own width, the same move as darkside's rail, and the law
  is encoded: *a clipped tile keeps its FIGURE* (leaders may go, data may not).
- **`#ap { padding: 1 3 }` folded the whole aperture queue.** Changing that padding changes
  every region's WIDTH, and a region re-measured a frame after its rows were built wraps them.
  Every ledger row is filled to its full measure by leaders, so this is the one language with
  no slack to absorb a stale width. The page margin was dropped — a decision, now documented in
  `composition()`.
- **A pre-existing off-by-one in `aperture._queue_markup`**, found while chasing that: the row
  is built as `marker + 1 + (w - 8) + 5`, which is **w + 1 for every 3-cell marker in the set**
  (measured: corgi 93 cells in a 92-cell panel; ledger 91 in 90). corgi and industrial have
  been overflowing by a cell all along. Ledger's folio marker is 2 cells and declines to step
  on it; **the fix is app-side (`aperture.py`) and is owed.**
- **Focus would have zigzagged the ruling**: widget.tcss shifts a focused row's padding to make
  room for a focus border, and this language spends none. Corrected in `composition()`.

**Counts: verify_language 407 → 548** (+141: the ledger law section, the ruling asserted at
three widths, the pairwise/greyscale/data-viz/component/anatomy laws all scaling from 7 to 8
languages). `verify_aperture` ALL PASSED with 8 (its cycle checks already read `ORDER`; only
the "nine" labels were stale). `verify_widget` ALL PASSED, redraw **1289 µs = 7.7%** of a
60 fps frame (H ≥ 5 holds). `verify_board` ALL PASSED. `pytest tests` **137 passed**, no
clipboard flake in this session's runs.

**Dark-patch audit (the light ground's real risk), measured rather than eyeballed:** every
painted cell of the ledger frame is light — at 118×30 the compositor reports 3200 cells of
paper, 214 of band, 118 of panel, 8 of scrollbar, and **zero cells below 0.25 luminance**;
same at 80×24 and in the aperture at 96×30. The scrollbar needed its own rules (`surface()`),
because no colour token reaches it. **Not covered:** `GalleryScreen`/`HelpScreen` use a
`#000a` modal scrim from widget.tcss — a dark wash behind the `g` and `?` overlays only. Out
of budget (widget.tcss), and it is a scrim, not a surface.

**Known, bounded, and asserted rather than hidden: the head rule ends 1 cell short of the
postings' closing rule.** `kanban.py` hands the section head `avail - 4` while a card sizes
itself from its own content box, so the two right edges differ by a cell. The LEFT edge — the
one the eye tracks — is exact and asserted (`the head rule starts where the postings start`);
the right edge is asserted to within 2 cells so a real drift still fails. Closing it needs
`kanban.py`, out of this increment's budget.

**THE DARKSIDE CAPTURE RACE IS NOT CLOSED — it reproduced, and the twentieth pass's 10/10 was
not the whole story.** Measured this session: **2 failures in ~11 full-suite runs**, always the
same four checks (`darkside: the fixture card is on screen (probe self-check) 0 row(s)` plus
the three that depend on it), and always with `settle()` reporting healthy headroom (worst 4 of
40) — so **settle() is not timing out, it is returning a frame it believes is painted.** New
evidence from the failing run, which narrows it further than the nineteenth pass did: in the
same failing run the rail check `ONE unbroken edge columns=[3]` PASSED and the LATER 118-wide
darkside capture found the card (`rail present wherever the board is board=yes`). So the board
is mounted and drawn, the head is there, and only the card's TEXT is missing from that one
frame. The suspect the settle condition cannot currently distinguish: a board whose cards are
mounted-but-not-yet-content-rendered is indistinguishable from a board that legitimately has no
cards (condition A is vacuously true, and condition B settles an empty frame just as happily).
This pass added an **evidence dump** — the failing frame is written to
`prototypes/out/_race_darkside.txt` — so the next session diagnoses a real frame instead of
reconstructing one. It has not fired yet (the race did not recur in 11 later runs).
**Treat the suite as ~1-in-6 flaky on that one probe until this is closed.**

**Done 2026-07-27 (twentieth pass) — the capture race is FIXED; the sixteenth-pass watch is CLOSED.**
`capture()` no longer guesses at timing. `settle(app, pilot, label)` waits on a CONDITION, bounded
to `SETTLE_MAX = 40` iterations:

  A. every card the compositor says it is drawing has painted pixels inside its own clipped area
  B. the rendered frame is identical on two consecutive reads

and a timeout is a **FAIL** — `capture settle timeout: board never painted (<language> @<w>x<h>)` —
never a quiet proceed, because a capture that silently returns a blank board turns every check
reading it into a lie.

**Two wrong versions preceded the right one, and both were caught by running it rather than
reasoning about it.** (i) Asking the widget for its content — `TaskCard` has no `.renderable` in
textual 8.2.8; it raised immediately. (ii) Slicing the card's `region` out of the frame — a card's
region is in SCREEN space and keeps growing past the fold, so the card at `y=29` was measured
against **the Footer**, whose text scored as "painted". That false positive would have masked the
exact bug the function exists to catch, and the suite reported 14 loud settle timeouts rather than
pretending. The sound instrument is the compositor's own `visible_widgets` map: it holds only the
widgets it actually draws, each with its clip, so cards under the fold drop out instead of lying
(measured: 8 of 15 cards drawn at 118×30 for naught).

*The condition is generic, not a darkside special case.* It interrogates the widget tree, so where a
size class shows no board there are simply no cards, A is vacuously true, and B settles the frame on
its own — the same code serves the 60-column regime and the 118-column one.

**Proof against the measured base rate.** The old recipe was measured at roughly 1 red in 3 full
runs. Ten back-to-back runs of the full suite: **10/10 green, 407 checks each, exit 0.** Under the
old rate ten clean runs would happen about 1.7% of the time ((2/3)^10), and the mechanism explains
why: we now wait for real paint instead of a fixed pause count. `verify_aperture.py` — untouched,
its own settled-frame logic left alone — `ALL PASSED`.

**The gate now watches itself** (+1 check, 406 → 407). `settle()` records the iterations it consumes
and the run ends by asserting headroom: **worst 4 of 40 across all 25 captures, identical in all ten
runs.** That number does two jobs. It shows the loop is load-bearing rather than decorative — the old
recipe was worth about one pause, and settling genuinely needs up to four — and it gives the next
eight increments a canary: if the worst climbs toward 40, the bound is being outgrown and the reds
that follow will be timing, not design. The check fails while there is still 2× margin, not after.

**Done 2026-07-27 (nineteenth pass) — harness hardening, and the capture race CAUGHT IN THE ACT.**
Two pieces in `prototypes/verify_language.py`. (1) **Guard**: `capture()` now raises
`ValueError("capture() requires an explicit fixture board_path; probing the live board.json is
forbidden")` when `board_path` is None. The default stays on the signature so no call site changes
shape; it can only raise. The guard is itself checked — an unfired guard is a comment — by a probe
self-check that awaits `capture("naught")` and asserts the raise. (2) **Empty-phase fixture**:
`_fixture_empty.json`, derived from the seeded board with the `Done` phase emptied, restores the
app-path coverage of `empty()` (mascot + VOICE) that was lost when the suite stopped opening the
live board — where an empty phase was present or absent by luck, which is not coverage. Each
columns language is captured on it and must speak its own `VOICE["empty"]`, plus a **negative
control**: the same word must be ABSENT when no phase is empty (an assert that cannot fail is
decoration). Checks **392 → 406**.

Two findings from doing it. **The empty state has no seat in the SECTIONS layout**: `kanban.py`
mounts `k.empty()` only in the columns branch, so darkside and swiss cannot render their empty
voice through the app at all — the check therefore covers the five columns languages
(naught · corgi · instrument · industrial · nord) and the gap is recorded below rather than blessed
with an assertion. **The voice WRAPS**: corgi's `[0] NO TASKS` comes out of a floor-width empty
column as `[0] NO` / `TASKS`, so the check asserts the voice's longest word, not the whole string.

> **CLOSED in the twentieth pass** (condition-based settle; 10/10 green against a ~1-in-3 base
> rate). The diagnosis below is what made the fix possible — keep it as the record of how the bug
> was cornered.

**THE RACE REPRODUCED — the watch stays OPEN.** Three back-to-back runs: 406 · 406 · **402 + 4
FAIL**. The failures were `darkside: the fixture card is on screen (probe self-check)  0 row(s)`
plus the three checks that depend on it. This is the sixteenth pass's darkside capture-race, and it
is now much better characterised:

- It is **not** the live board. It happened on the deterministic fixture, with the guard in force.
- The board was **partly** rendered: in the same failing capture the rail on the section head passed
  and `ONE unbroken edge columns=[3]` passed, while zero card titles were present. So the cards were
  mounted-but-unpainted, not missing — consistent with `TaskCard.on_mount`'s
  `call_after_refresh(render_card)` landing one refresh after the captured frame.
- A **later, identical 118-wide capture in the same run saw the card** (`rail present wherever the
  board is  board=yes`). Same size, same fixture, seconds apart, different answer.
- It needs full-suite context: an isolated bounded loop of 12 darkside captures missed **0/12**, and
  a candidate fix (pause until `screen_text` stops changing, bounded to 10 iterations) also scored
  0/12 — i.e. **the fix candidate is unproven**, because the isolated harness cannot produce the
  failure it is meant to cure.

Next task, with the evidence to judge it by: make `capture()` settle on a *condition* rather than a
fixed number of pauses — bounded, and failing loud if the condition never arrives — then prove it by
running the full suite ~10× and comparing against today's measured base rate of roughly 1 in 3.
Until that is done, treat any single green run of this suite as weak evidence.

**Done 2026-07-26 (eighteenth pass) — the harness stops probing the LIVE board.** Surgical fix to
`prototypes/verify_language.py` only. The app-level pair section (`capture(name)` with no
`board_path`) opened the user's real `board.json` via `Board.load(default_board_path())` — the file
the desktop app rewrites underneath a running suite. Every app-level comparison was therefore a race
against a moving board, which is the standing explanation for legibility reds that appear once and
never reproduce. The fixture is now seeded **once**, before the first capture, and all **7** capture
sites use it; the later block no longer re-`unlink`s it mid-suite (a reset between captures is the
same class of bug). Verified by grep: zero `await capture(` calls without `board_path=str(fx)`.

**The trap inside the fix.** Moving only the baseline would have made four checks *vacuous*: the
token-mutation block compares `mb != boards[name]`, so a mutated **fixture** render against a
**live** baseline passes because the task lists differ, not because the token is live. Baseline and
mutation captures were moved together; that block's heading is now "reaches the rendered board".

**Runs: 3/3 back-to-back green, 392 checks each, exit 0** — count unchanged, so nothing was added,
removed or silently skipped; only the board underneath the same 392 assertions changed. Aperture
`ALL PASSED` (it shares the capture plumbing).

*Did the fixture weaken anything?* It holds 16 tasks over 3 phases (Backlog 8 · Doing 6 · Done 2),
6 projects, 2 blocked, 12 with due dates — enough that **all 21 app-level pairs still differ**, which
is what the section exists to prove, and it now proves it reproducibly instead of against a board
that could change between two captures. One real coverage delta, stated plainly: the fixture has
**no empty phase**, so the app-mounted empty-column state (`k.empty()` — mascot + VOICE) is not
exercised through the app path. It is still covered at kit level — `kit_sig` includes `k.empty(16)`,
so the greyscale pair law over the empty state is intact. Whether the live board ever had an empty
phase is unknowable without reading it, which is the thing this pass exists to stop doing.

> **CORRECTION (nineteenth pass).** The "root cause removed" framing below is **wrong for the
> darkside red**. Dropping the live board was right and stays — but the intermittent darkside
> legibility failure **reproduced on the fixture** (1 of 3 runs). The live board was a real hazard;
> it was not this bug's cause. The watch stays open, now with better evidence.

*The capture-race watch (sixteenth pass): root cause REMOVED, but not declared closed on 3 runs.*
The shared mutable resource is gone from the harness, which is a mechanistic argument rather than a
statistical one — and the mechanistic argument is the stronger of the two here. But an intermittent
red whose base rate was never characterized (this session it reproduced 2/2 at baseline, then went
green before this fix) is not retired by three runs. **Leave the watch open for one more session;**
if the suite stays green across it, close it then.

**Done 2026-07-26 (seventeenth pass) — DARKSIDE gets a passive RAIL (`layout` token).** New
structural token pair in `themes.py`, darkside only: `layout="rail"` + `rail="#262626"`. The kit
reads them through `Kit.layout` (base default `"flow"` = every language's previous behaviour) and
`Darkside.rail_prefix()/rail_width`: the section head and both card rows are prefixed with `▏` plus
two cells of air, and those 3 cells come **out of the content budget**, exactly like the card's own
padding — a rail that widened the row would wrap it. Grounded in the tui-design skill, not the
mockup: HIERARCHY.md ranks grouping proximity → background → **rule** → border, so the rail is the
third mechanism (one stroke), chosen so the border stays reserved for focus and keeps meaning
something.

*The collision claim was PROBED FIRST and is FALSE.* The external design spec asserted that
instrument and darkside "collide in greyscale". Colour-stripped board captures at 118×30 (both
written to `prototypes/out/probe_*.txt`) share nothing: darkside is a full-width **sections** list
of lowercase titles with no fill glyphs; instrument is a 3-column weighted kanban with braille fill
bars (`⣿⠒`), dotted leaders and uppercase titles. The harness's own `instrument != darkside` pair
check has been green throughout. **No code was changed on account of that claim** — the rail is
justified by a different, real defect: darkside declares `frame="none"` and so its sections board
had *no* structure device at all, and its card stack floated under the head.

Two defects the first render caught that green checks had not: at 60 cols the app is below the
board size class and shows **no board** (so "the rail renders at 60" was a wrong check, not a bug —
the law is now *rail present wherever the board is*), and the rail **zigzagged** one cell between
head (col 2) and cards (col 3) because `.kb-card` has `padding: 0 1` and `.col-head` has none.
Fixed with one rule in darkside's own `composition()` (`.col-head { padding-left: 1 }`); the check
now asserts a single rail column rather than `lstrip().startswith()`, which had hidden it.

verify_language **392** checks (was 356; +rail dispatch-IFF-token for all 7 languages, +budget law
at 4 widths, +one-unbroken-edge, +frame law and rail-presence at 60/80/118, +`layout`/`rail` in the
ALT mutation table). `mut_sig` now also carries the **coloured** card markup — colour-stripped, a
recoloured rail is invisible and `rail` would have read as dead metadata. Suites: verify_language
392 ALL PASSED · aperture ALL PASSED · widget ALL PASSED (budget 1360 vs 3333, H≥5) · board ALL
PASSED · pytest **137 passed** (no clipboard flake this run). Render read by eye at 60/80/118 —
`prototypes/out/rail_darkside.txt`.

Open items from this pass: (a) the rail is darkside-only — rolling `layout` out to the other six is
a future increment, and the token is deliberately not declared by them so they render byte-identical;
(b) `rail="#262626"` is currently the *same value* as darkside's `dim` — a separate token so it can
be tuned and mutation-tested, but if it never diverges it should be collapsed; (c) **KMBlue is not
"once per view"**: a 118×30 darkside frame carries 33 accent segments — the focused hero's border
box (20), the active tab `(O)` (1) and 12 Footer key glyphs. All are interactive affordances, so the
accent-is-interaction law holds, but the stricter once-per-view reading does not; pre-existing, not
touched here; (d) the rail was NOT extended to the hero/meter/tabs rows (the design mockup's
continuous full-screen edge) — those live in darkside's centred 46-col ambient column, and an edge
on every region spends the divider on nothing (HIERARCHY.md); (e) not implemented, deliberately:
motion `breathe`, a `base="block"` hero, and the circuit/score languages.

**Watch — a pre-existing harness red that vanished.** The first two baseline runs of this session
(*before any edit*) both failed `swiss: sections board keeps titles legible`; an isolated repro of
the exact fixture sequence showed the title present, and after this pass it is green in a full run.
So it is full-run **ordering state**, not an app regression — same family as the sixteenth pass's
darkside capture-race watch. Prime suspect: `capture(name)` with `board_path=None` opens the user's
**live** `board.json` (`Board.load(default_board_path())`) for the whole app-level pair section,
which the desktop app rewrites mid-run. Moving those captures onto the fixture is a cheap next task.

**Done 2026-07-26 (sixteenth pass) — SWISS gets the darkside cure.** User: "swiss tiene el mismo
problema". Same posture split: the 78-col editorial MEASURE stays on the ambient block only; the
board takes the page and commits to **sections** (the editorial list — letterspaced header, one
rule, airy full-width rows: the most swiss form possible). Plus the real fold fix: at BOARD size
the ambient yields rows (hero 11→9; tiles-as-list moves to widget size only) — at 30 rows the
board went from ZERO visible cards to four full-title cards. Legibility laws for both sections
languages on the seeded fixture (probe lesson ×3 now: legibility ≠ visibility-under-scroll; judge
what IS on screen; never probe the live board). verify_language **356** · board · widget ·
aperture 16 · pytest 137/137, renders looked at. The earlier one-run darkside legibility FAIL did
not reproduce (4-language sequential repro + two full suite runs green) — filed as capture-race
watch, same family as the settled-frame trap.

**Done 2026-07-26 (fifteenth pass) — LEGIBILITY + VISUAL NAV (two user-reported defects).**
1. **Darkside's tasks were "casi ilegible"** (6 kanban columns inside its 46-col cage, ~7 chars of
   title). Fix in two commitments: (a) **composition per POSTURE** — the centred 46-col column now
   applies only to the AMBIENT register (#top/#tiles/#tabs/#queue/#ap-panel, Moonshot's chat
   column); data surfaces get full width; (b) **`Kit.board_layout()`** — "columns" default,
   darkside commits to **"sections"**: a flat vertical list, full-width lowercase phase headers +
   full-width cards (its faithful form). Law, fixture-based: a 24-char title renders INTACT on
   darkside's board. Also a candidate for swiss later.
2. **Arrow navigation felt wrong** ("parece que hay algo en medio pero no hay selección"):
   diagnosed by stepping focus — the model was sane (card→card) but lateral moves kept the INDEX
   row, not the SCREEN row, so with scrolled/uneven columns you landed far from the visual
   neighbour; empty columns also skip whole regions (correct, but reads as "something in between").
   Fix: lateral movement is now GEOMETRY-based — land on the card whose screen row is nearest
   (visible cards preferred). Works identically in columns and sections layouts.
verify_language **355** (legibility law on the seeded fixture — the live-board probe lied again) ·
verify_board · verify_widget · verify_aperture 16 · pytest 137/137. Looked at: darkside sections
render (full titles, meta `backlog · d3` under each).

**Done 2026-07-26 (fourteenth pass) — CURATION + THE FULL LANGUAGE IN THE APERTURE + the Kimi
responsive harvest.** Three pieces:
1. **phosphor and bbs RETIRED** (user: "horribles"; darkside loved without knowing its name,
   naught "excelente"). Kits + themes deleted; ORDER = 7 (naught · corgi · instrument · swiss ·
   industrial · nord · darkside); their decay/gradient mechanisms remain in METERS as library
   options. Incident, recorded honestly: the theme-dict surgery cut swiss/industrial/nord too
   (file order ≠ ORDER); recovered byte-exact from `__pycache__` (the compiled module carried the
   full dict) — with nothing committed, the pycache was the only backup. Lesson: bracket deletions
   by KEY, not by line ranges.
2. **The aperture now wears the FULL language:** ids renamed to the prototype's (#ap/#top/#hero/
   #meter/#tiles — none exist in the real app's main screen), per-language TCSS injected with
   `Screen`→`ApertureScreen` rewritten, size classes set on the screen. naught's grid puts the
   meter BESIDE the hero (verified by region); darkside gets its centred 46-col column. Found and
   fixed the wrapped-frame bug AGAIN: regions built rows from the SCREEN's width — inside
   darkside's column the 92-cell hero wrapped into ███ fragments; every region now measures its
   OWN width (`wof()`, plus `call_after_refresh` for the 0-width mount frame).
3. **Kimi responsive harvest** (their post-11:00 work, explored read-only): what the operator liked =
   resize re-renders CONTENT (we already do), the HEIGHT axis as renunciation (we already apply),
   and one real gap adopted: **reflow-never-truncate** — `spark`/`plot` now `_resample()` (bucket-
   max) instead of `series[:w]`, which silently dropped the calendar's last week; law added per
   language ("the tail survives"). Plus the **nothing-wrapped assertion** their gate lacked
   (hero height <= 12 across all 7 languages at frame level; real wraps measured 15-21). Their
   V-forced-preview-without-rebuild and hardcoded-44 centering were already avoided here.
verify_aperture **16** · verify_language **354** · verify_widget · verify_board · pytest 137/137.

**Done 2026-07-26 (thirteenth pass) — THE APERTURE LANDS IN THE REAL APP (HANDOFF §4 Increment 2,
the prototype→product jump).** ADD-don't-replace, exactly as corrected: `views.py` untouched, its
137 tests green. New: **`taskboard/hero.py`** (the drawn hero extracted as a real module — 6
per-language mechanisms + the dead-columns plot + the 4x7 font; now trims VISUAL rows, not entries
— the prototype's latent clip bug, region-measured in the aperture; naught's drawn caption applies
progressive disclosure: 5-row type only when it fits, typographic fallback otherwise) and
**`taskboard/aperture.py`** (`ApertureScreen` behind the **`6` key**: hero + meter + signal tiles
with icons/gauges + due-calendar/up-next queue, engine on 1s/5s cadences, `t` cycles the NINE
languages — choice persists across opens — and the number keys **exit INTO that view**: the
aperture is a launcher, the widget thesis landing in the product). Row-budgeted: glance <46 shows
the hero alone; the panel prioritizes the QUEUE over the calendar when height is tight. Acceptance:
**`prototypes/verify_aperture.py`** (new, 9 checks): the 6 key opens it, the hero renders, nine
languages reachable and pairwise-distinct at frame level, language persists, launcher jump works,
the board's priority arrows never move the hidden selection. All green + pytest 137/137 (clipboard
freed this run). **Honest V1 limits:** kit MARKUP carries the language, kit surface/composition
TCSS not injected yet (selectors target prototype ids — next increment of this view aligns them);
no embedded kanban (keys 1-5 ARE the board postures — by design, not omission); prototype's Hero
still has its own copy of the drawing code (fold it onto taskboard/hero.py next time widget_slice
is in budget). RUN.md still prototype-only; the real app's `6` key is documented here.

**Done 2026-07-26 (twelfth pass) — DARKSIDE, the 9th language.** Ported from the Kimi fork and
held to this repo's laws. Commitments: achromatic greys with **KMBlue spent EXCLUSIVELY on
interaction** (switch (O), active tab, slider knob, the focus border) — passive data is grey
STEPS; `meter="step"` mechanism (fill █ vs track ▁ — the fork's grey-on-grey meter died in
greyscale, fixed to SHAPE per DATAVIZ law 1); position-only slider; (O)/( ) fill-inversion idiom
on switch AND tabs (active view survives greyscale as a glyph); lowercase register everywhere
(`display_cap` — a new KIT method, base = letterspaced caps, so the register is code not a dead
token); date-driven moon doodle on a recessive wordmark (#3a3a3a); depth by grey-step background,
never a border; composition = ONE centred column (max-width 46, `align-horizontal: center`) —
ADAPTIVE, fixing the fork's hardcoded-44 wrap-below-46 bug. tempo=300/easing=in_out_cubic (a slow
breath). Laws added: passive-carries-zero-accent (incl. bar() remapping caller-passed accent to
grey), interaction-wears-accent, doodle-on-wordmark, lowercase register, step-meter-greyscale.
Pairwise counts un-hardcoded (== len(ORDER)). verify_language **461 checks**; verify_widget
(1434 µs) + verify_board green; pytest 136/137 (clipboard flake only). Known limit, honest: the
centred 46-col column compresses the 6-column kanban hard (titles truncate to ~6 chars) — the
fork's truer form is a vertical section list; candidates: darkside-specific board layout when the
aperture (Inc 2) lands. RUN.md still says 8 languages (1-line fix owed).

**Done 2026-07-26 (eleventh pass) — KIMI-1 CLOSED (series laws · drive-checks · DATAVIZ.md) + a
real bug killed.** The verify half of the Kimi harvest landed: per-language DATA-VIZ LAWS (shared
`hi` on spark/plot, microbar floor, empty/flat safety, gauge zero-range safety, gauge-states-its-
value, threshold tick renders and moves) and APP-LEVEL DRIVE-CHECKS (focus-at-mount; actuate the
config switch and assert the render moved; walk the cursor; move the threshold slider; hammer it
30x past the floor and assert it CLAMPS). **The drive-check caught a real, 3-pass-old app bug:**
the ConfigScreen's up/down cursor was DEAD — the App's board-nav bindings are priority=True and
Textual resolves priority bindings APP-FIRST, so the screen never saw the arrows; every render-
level check had blessed it. Fix: `action_nav` now DELEGATES to any screen exposing `action_move`.
The probe itself also got a law: navigation loops are BOUNDED (an unbounded `while` hung a whole
run when the arrows were dead). Skill: **`DATAVIZ.md` written** (the fork's phantom citation now
exists — dispatch law + 8 data laws + verification recipe; COMPONENTS.md holds the inventory).
verify_language **399 checks**; verify_widget + verify_board green; pytest 136/137 (the named
clipboard flake only). Files: verify_language.py · app.py · DATAVIZ.md (new, skill) · PENDING.md.

**Done 2026-07-26 (tenth pass) — NAUGHT RE-GROUNDED IN NOTHING (user verdict: too red, too square,
mascot pointless; instrument is the bar).** Three corrections, all measured: (1) **The pixel is
ROUND now** — `naught.py` ON/OFF went `█/░` → `∙/◦` (U+2219/U+25E6, both measured EAW **Neutral**
— safer than the Ambiguous blocks they replace); theme `dot_w` 2→1; hero numeral drawn at x2 scale
so the digit stays LARGE on the panel like Nothing's. SPIN/ICONS/GANTT rounded. (2) **Red is
RATIONED**: 70 accent hits on the kit surface → **7**, all semantic (urgent chips, overdue tile,
overdue calendar day). Decorative accent → ink everywhere (heads, tabs, switch, slider, spinner,
bars, meter, spark/plot/gauge); new `calm` theme token — CALM/NOTICE severity renders INK, the hero
numeral is white unless something is genuinely wrong; the red focus edge (`sel=outer`) SURVIVES as
the one element of interest; naught's gauge tick is grey (shape marks it). Law: "a CALM naught
surface carries ZERO red" — enforced. (3) **The mascot has a JOB**: `Naught.face(mood)` — clear /
busy / alert expressions, fed by the real board (`KIT.mood`, set each redraw from overdue/open
state), grounded on the unlit lattice; wordmark now drawn through the round lattice alphabet too.
verify_language **317 checks** (+round-pair EAW law, red-ration law, alarm-still-red, 3-expression
face, grounded face, mood-follows-board; naught dot_w mutation updated to 1→2). All four suites
green; budget 1604 µs. Kimi-1 kit code (hi=/microbar/gauge-tick) remains in and green; its verify
laws + DATAVIZ.md are still the OPEN half — next increment.

**Addendum (same day) — LATTICE PITCH.** User: correct vibe, but the dots felt too separated. New
`gap` token (naught: cells of air between dots, default **0 = dense LED panel**) — the round pixel
carries its own air, so adjacency stays legible (the block pixel NEEDED the space; the round one
doesn't). Wired through `naught.py` (`_runs`/`label`/`dot_meter`/`dot_heat`/`plain_width` gained
`gap=`), the Naught kit (field, leaders, sect lattice, bar, slider, SPIN — now a property at the
lattice pitch —, face, wordmark, plot/gauge dotgrid, meter) and the hero. Letters always keep >=1
separation; calendar cells stay 2-wide (layout contract); phase pips keep their spacing (they are
indicators, not field — Nothing's streak dots). Mutation-tested (`ALT["gap"]`). verify_language
**319**; all suites green.

**Addendum 2 (same day) — THE FINE DOT SCALE + one texture block.** User: study how instrument gets
its density; even a texture swatch can read as denser pixels. Nothing mixes TWO dot scales (large
structure dots · tiny data dots — the step counter's rows), so naught now does too: `naught.FINE`
("⠂⡀⡄⡇" — a SINGLE sub-cell braille column, round, distinct from instrument's continuous 2-wide
fills) carries the DATA surfaces: the spark and the meter's flow/heat row; structure (numerals,
lattice, plot columns, bars) stays on ∙/◦. Plus ONE texture block: the meter panel wears
`hatch: cross #101010 35%` — near-black, grounds without competing. Laws: data-wears-fine,
structure-keeps-large, the-two-scales-differ. verify_language **322**. **The pytest flake is now
NAMED:** `tests/test_app.py::test_win_clipboard_roundtrip` — round-trips the real Windows
clipboard via PowerShell; fails whenever another process holds the clipboard (fails solo when the
machine's clipboard is busy, passed 6+ full runs earlier). Environment-dependent by construction,
pre-dates this work, `tests/` untouched by policy — fix candidate for a future increment: skip or
mock when `OpenClipboard` is unavailable.

**Done 2026-07-26 (ninth pass) — DISPLAY TYPOGRAPHY (axis 3) + gallery scroll + the Kimi harvest.**
`sect(title, note, w, h=0)`: h is the surface's ROW BUDGET and display type is a luxury it must
afford — naught draws titles in 3x5 lattice dots (5 rows, h>=16), bbs in solid block letters with a
gradient underline (h>=16), instrument in 2-row braille caps (h>=10, the clinical register); swiss/
corgi/industrial/phosphor/nord RENOUNCE drawn type (verified: h changes nothing for them). Wired:
the three views pass their height; ConfigScreen (full-height) draws; at 30-row screens the views
stay typographic (h=14 < 16) — honest degradation, not a missing feature. Gallery: card demo is now
the 2-row `card_rows`, and the box SCROLLS (max-height 90%) — the guide had outgrown 30-row screens
and clipped its bottom sections since the plot pass. verify_language 311 checks (+display laws:
drawn rows, progressive short-form, renunciation, three distinct drawn faces; config probe now
checks the hint line, not the title text — drawn titles aren't text). **verify_board flake
DIAGNOSED:** its probes read the USER'S LIVE board.json (the desktop taskboard rewrites it), so
runs are nondeterministic by design — port verify_board to the seeded fixture like verify_language.

**The Kimi harvest (fork reviewed read-only at C:\Users\jjgh8\kimi\taskboard-overhaul).** Their copy
forked from our SECOND pass — passes 3-9 (composition, motion, icons, spark/plot/gauge, card
anatomy, display type) exist only here; nothing of their base is worth merging back. Four genuinely
new things worth adopting, ranked:
1. **`hi=` shared normalization** on spark/plot (+ series laws: microbar floor, empty/flat safety,
   gauge div-by-zero, "a gauge must state its value") — our sibling sparklines self-normalize and
   are silently incomparable. Cheapest, highest value.
2. **Component drive-checks** (focus-at-mount, actuate-and-assert-render-moved, clamp-at-bound) —
   our suite proves components RENDER per-language, never that one WORKS.
3. **`darkside`** — a real 9th language (Moonshot brand): achromatic + accent reserved for
   INTERACTIVITY only, depth by grey-step (no borders), `step` meter, position-only slider,
   (O)/( ) fill-inversion idiom, centered search-hero composition, date-driven doodle. Port needs
   tempo/easing tokens added + their hardcoded 44-col centering fixed (wraps at <46 cols).
4. **Paired-aperture capture ritual** (each language at 80x26 AND 40x14 from one script) — the
   pair is what makes renunciation legible. Plus: add a "nothing wrapped" assertion to geometry
   checks (their `len(row)==width` passes wrapped content; ours would too).
Also: gauge threshold-tick arg; the (O)/( ) glyph-invariant tabs law for COMPONENTS.md. Their
`prototypes/overhaul/` bench app is a weaker widget_slice — mine only the ~50-line live
KitSwitch/KitSlider pattern. They cite a `DATAVIZ.md` skill doc that does not exist (phantom
citation — the laws are real, the doc was never written; candidate: write it as part of adopting 1).

**Done 2026-07-26 (eighth pass) — CARD ANATOMY (the variety lever).** User verdict on pass 7: "es
una mejora pero falta aún variedad". The card is the board's largest surface, so variety was built
there: `Kit.card_rows(...)` makes the card a per-language MINI-WIDGET — row count, field CHOICE and
mechanism are commitments, not one 2-row layout restyled. naught = row 2 on the lattice (phase dots
+ 2-dot state icon; the 3x5 sprite needs 5 rows — dot meter is the honest form, item 2 closed);
corgi = engraved spec line (DUE/PH/PR, values on screen-green); instrument = braille progress bar +
due; swiss = the second row RENOUNCED (1 row, space is the structure — verified as a law);
industrial = everything bracketed \[PH:][DUE:][PR:]; phosphor = nearness as GLOW (due-date proximity
sets the trail's brightness tier); nord = the two-line list convention (project · phase); bbs =
gradient shoulder + CP437 caps. Metadata rows use `_fit_parts` progressive disclosure (fields that
don't fit are DROPPED, never wrapped — corgi's narrow-column orphan caught in the render). Cards are
`height: auto; max-height: 3` and the width passed to kits now subtracts the card's own padding
(with height:1 the overflow was silently clipped; with auto it wrapped a phantom row). verify: 299
checks (+anatomy laws: swiss 1-row renunciation, 2-row languages respond to metadata in greyscale,
no two share an anatomy, row counts diverge). Budget: redraw ~2.0 ms (12% of a 60 fps frame) —
gate passes, but three passes of growth (1.4 → 1.7 → 2.0) says measure before adding more per-tick
work. **Flake note:** one `pytest tests` run failed 1/137 once, passed 137/137 on immediate rerun
and in every other run today — not reproduced, likely time/worker timing; watch it. **New open
item: swiss at board size starves the board** — hero 11 rows + tiles-as-list spend ~17 rows, so at
a 30-row screen the cards sit below the fold (pre-existing composition choice, visible now that
cards matter; decide: cap tiles list or shrink the swiss hero at sz-board). Gallery still demos the
1-row `card_row` — swap to `card_rows` next time app.py is in an increment's file budget.

**Done 2026-07-26 (seventh pass) — DATA-VIZ second wave (axis 7) + the full-inventory map.**
User directive mid-pass: a design language must sort out the WHOLE component inventory — input
(buttons, text boxes, scroll bars…) AND data display (bar/scatter/pie/gauges/KPI), the way Nothing
re-imagines all of them. Shipped: `Kit.plot(series, w, h)` (h-row column chart) and
`Kit.gauge(val, lo, hi, w)` (read-only KPI dial), both dispatched on the `meter` token like
`spark`; the hero's dead columns now carry the 8-week load plot at board size (item 3 CLOSED, incl.
short-hero fix for industrial); tiles gain a value-vs-threshold gauge when wide; gallery shows
plot + gauge. Skill: COMPONENTS.md gained "The full inventory" — input + data-display checklists
with status (shipped / owed / renounced: pie is a RENOUNCE with the fraction-bar replacement,
scatter/line owe a braille field) and the Nothing lesson stated once (all their charts are ONE
mechanism — which is why charts dispatch on `meter`). verify_language 282 checks (+plot/gauge laws,
+no-two-share, +dead-columns app checks on a seeded fixture; captures now take a SETTLED frame —
`Hero.show` reads its own height one redraw behind a theme switch). Budget: redraw ~1.7 ms
median (10.3% of a 60 fps frame), gate H>=5 still passes. Remaining from the 7-axis map: display
typography beyond the wordmark, per-card 2-row compositions, line/scatter braille field, and the
OWED input components (button, text field, checkbox, stepper, scroll bar — see COMPONENTS.md
inventory).

**Done 2026-07-26 (sixth pass) — ICONOGRAPHY (axis 4) + DATA-VIZ spark (axis 7).** `Kit.icon(kind)`
over the signal vocabulary (deadline/overdue/wip/blocked/workday/boardfile) with one mechanism per
language (corgi engraved DL/OV codes · industrial [D] brackets · instrument braille patterns ·
phosphor brightness-coded glyphs · naught 2-dot lattice · nord ASCII · bbs CP437 · swiss renounces);
wired into tiles, ConfigScreen rows, gallery. `Kit.spark(series, w)` dispatched on the `meter` token
(same quantity family as the meter); wired into the calendar's 4-week load row + gallery; greyscale
law enforced (LCD spark needed segment HEIGHT, caught by the suite). verify_language 254 checks.
Remaining from the 7-axis map: display typography beyond the wordmark, richer data-viz (plots/
canvas/3D — course M15-M21), per-card 2-row compositions, hero dead-columns spark (item 3).

**Done 2026-07-26 (fifth pass) — MOTION PER COMPONENT (axis 5).** New motion tokens `tempo`+`easing`
in every theme (industrial 60ms linear · phosphor 400ms out_expo · bbs 100ms out_bounce · swiss
240ms in_out_cubic...), read by: kit tcss `transition:` rules on card/tile/hero, the hero severity
flash and the view-change fade (imperative animates now use KIT.tempo_s/KIT.easing), and
`flip_frames(on)` — per-language switch-flip frames animated in ConfigScreen via set_timer (naught
dot-fill, corgi ghost snap, instrument braille roll, phosphor bloom, bbs double flash, industrial
relay tick, swiss single frame = renounced). Degraded path verified: animation_level="none" skips
frames, never the state. verify_language now 236 checks (+flip laws, +tempo/easing mutations).
Budget back at ~850 us (5.1%).

**Done 2026-07-26 (fourth pass) — COMPOSITION (axis 6).** `Kit.composition()` returns layout TCSS;
new `#top` wrapper (hero+meter) whose layout the language owns. Board-size compositions: naught =
widget grid (meter panel BESIDE the hero) · swiss = one editorial column (max-width 78, flush
left) · corgi = modules under aluminium border-top rules · industrial = compact boxed panel (hero
7 rows) · phosphor = monitor (hero 13 rows) · bbs = one double frame around the whole screen ·
instrument = symmetric inset · nord = the conventional skeleton (its commitment). Startup now runs
`set_theme(THEME)` so the full language applies from launch (it used to skip the kit stylesheet).
Acceptance: verify_language "COMPOSITION" section — region GEOMETRY per language (>=5 distinct hero
regions, naught beside-check, swiss width, phosphor/industrial heights, bbs frame). Lesson recorded
in COMPONENTS.md: grid rows misSize when display:none children still create cells — use a wrapper
container. Budget after all four passes: redraw median ~1.4 ms = 8.7% of a 60 fps frame (gate H>=5
still passes).

**Done 2026-07-26 (third pass) — SURFACE + IDENTITY axes + gallery.** User: "aún se sienten muy
simples". Added: `g` COMPONENT GALLERY (per-language style guide, `t` cycles inside); surface axis
(`Kit.surface()`: bbs solid blue panels, corgi green-black display region, phosphor `hatch:`
scanlines, naught pure black, swiss emptiness); identity axis (`mascot()` — one mask through each
language's pixel base, `wordmark()` — 3x5 alphabet through the base, `VOICE` microcopy — "NO
CARRIER" phosphor, "*** EMPTY ***" bbs, silence swiss) wired into gallery + column empty states.
Skill: COMPONENTS.md gained the 7-axis expansion map (surface/identity/type/icons/motion/
composition/data-viz). All suites green. **The remaining ceiling is COMPOSITION (axis 6): all
languages share one layout skeleton — that is HANDOFF Inc 2 (the aperture), where layout itself
becomes a language commitment.**

**Done 2026-07-26 (second pass) — the COMPONENT LIBRARY.** User verdict on the first pass: "siguen
siendo mayormente cambios de paleta... falta todo lo que comprende un lenguaje de diseño (switches,
sliders, progress indicators...)". Fix: new skill doc `tui-design/COMPONENTS.md` (taxonomy, anatomy,
8-language glyph matrix, grounded in the Nothing OS widget sheet in `G:\My Drive\Style_info` — its
toggle is a FILL INVERSION, not track+knob) + kit components `switch/slider/spinner/tabs/CUR` in
`language.py`, wired into the three call sites: **ConfigScreen** (per-language switch, slider,
cursor, section header — was fully theme-blind), **#tabs view switcher** (new row; corgi commits to
showing only the active mode), **tile pending state** (per-language spinner instead of "...").
`verify_language.py` grew to **183 checks**: per-component 2-channel law (on/off must differ in
greyscale), sliders move, spinners animate and differ across languages, config screen pairwise
distinct at app level. Captures: `prototypes/out/cfg_*.txt` + `lang_*.txt`, looked at.

**Done 2026-07-26 (first pass) — item 0, the language axis.** New `taskboard/language.py` (8 structure kits +
dispatched meter mechanisms). Wired through `prototypes/widget_slice/` `app.py` / `kanban.py` /
`views_widget.py`; `taskboard/themes.py` tokens sanitized (every key is now read; `sel` and `pitch`
added; `hero_gap` deleted). New acceptance test `prototypes/verify_language.py` (121 checks).
Also fixed: stale card width at mount (`call_after_refresh`), head-rule wrap in scrolled columns,
`verify_board.py` probes that assumed the old universal glyphs (`▬`, `█`) — probes now assert
content, not a glyph model. Text renders of all 8 languages: `prototypes/out/lang_*.txt` — looked
at, per VERIFY.md.

**Done previous session — HANDOFF.md §4 Increment 1.** `engine.py`, `themes.py`, `bases.py`,
`motion.py`, `naught.py` moved from `prototypes/widget_slice/` into `taskboard/` as real modules.

Verified after both: `pytest tests -q` → **137 passed**; `verify_widget.py`, `verify_board.py`,
`verify_language.py` → **ALL PASSED**. `views.py`, `models.py`, `app.py`, `modals.py` untouched.

**Not done — HANDOFF.md §4 Increment 2** (the aperture as a fifth view). Not started. The item-0
blocker ("decide what a language means in code first") is now cleared — the aperture can consume
the kits directly.

**Probe:** `prototypes/verify_ink.py` — the ink-fraction probe, self-checking on both arithmetic
and capture. Run it as `python prototypes\verify_ink.py [height]`.

## How to run anything here

```powershell
cd "C:\Users\jjgh8\OneDrive\Documents\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"      # once per terminal; without it the verify scripts crash

python -m pytest tests -q              # 137 passed
python prototypes\verify_language.py   # 2178 checks, ALL PASSED (~75-80 s, the slow one)
python prototypes\verify_aperture.py   # 151 checks,  ALL PASSED
python prototypes\verify_widget.py     # 24 checks,   ALL PASSED
python prototypes\verify_board.py      # 22 checks,   ALL PASSED
python prototypes\verify_variants.py   # 12 checks,   ALL CHECKS PASSED
python prototypes\verify_ink.py 12     # ink fractions at height 12 (a probe, not a gate)
python prototypes\widget_slice\app.py
```

`RUN.md` carries the same list with what each suite is FOR. Counts are the number of `[PASS]` lines.

## Standing constraints (unchanged)

- **No commits, no push, no PR** unless the user says otherwise. `main` is at `b3cc60d`; all work is
  local and uncommitted in the `kanban-variants` worktree.
- Supervised increments: propose → approval → ≤5 files → review packet → stop.
- Spanish for conversation, English for code and technical artifacts.

## Traps — do not rediscover these

Full list in `HANDOFF.md` §6. The three that bit again this session:

- **Verify the probe before believing the verdict.** The ink probe reported 0.0% for all 8 languages;
  that was a broken capture, not an empty app. Both self-checks in `verify_ink.py` exist because of it.
- **Do not edit Python with `sed`.** It split an f-string across a literal newline and produced a
  syntax error. Use the Write/Edit tools.
- **Windows console encoding.** cp1252 turns a passing verify run into a `UnicodeEncodeError`
  traceback that reads like an app failure.

# 02 — QA cross-review · batch `2026-08-03-batch-03`

**Repo:** `C:\Users\jjgh8\Github\taskboard` · **branch** `main` · **base ref** `f237cb3` (verified:
`git log --oneline -1` → `f237cb3 Close the vertical-fill batch and reconcile a day-stale backlog`)
**Reviewer:** `qa-reviewer` (Phase-2), reviewing `01-requirements.md` (architect) and
`01b-qa-validation-plan.md` (a *different* `qa` instance) adversarially.
**Probes:** read-only, executed from `C:\Users\jjgh8\AppData\Local\Temp\qa2rev`. No file under
`taskboard/` or `tests/` was written. All output below is pasted from an executed run.
**Regime for every figure:** `TODAY = 2026-07-30`, `lane_geometry(94, 30)` (= inner at `width=96`)
unless the line states otherwise, `show_archived=False`, `tick=0`.

---

## Verdict

**GATE: BLOCKED.** 4 blockers · 7 majors · 6 minors.

The two artifacts are individually strong and the adversarial work in `01b` is real — its rejection of
"braille appears iff selected" is correct and its byte-identity falsifiability evidence **reproduces**.
But the batch cannot enter Phase 3 as written, for four reasons that are each a definitional blocker:

1. the two Phase-1 artifacts use **the same `AT-NNN` ids for different tests**, so neither traceability
   chain resolves;
2. `LLR-003.5`'s numeric threshold **fails on the repo's own fixtures under correct code**, and its
   C-40 mutation moves the predicate in the **wrong direction** — measured, 21/21 synthetic cases;
3. the empty-curve lane (`AT-014`) is a **requirement gap that survived into `01-requirements.md`** —
   two LLRs contradict each other on a board the repo already ships as a fixture;
4. `HLR-003`'s acceptance block names **`App._line_map` as its observation** — an internal symbol in a
   black-box AT.

The most important single correction: **the operator-accepted "Evidence gap" is misdiagnosed.**
Phase 3 does not owe a fixture. The fixture already exists on disk (§5 below). What Phase 3 owes is a
**different observable**, because the declared one is invariant under the mutation it is supposed to gate.

---

## Blockers

### BLK-1 — `AT-NNN` identifier collision: neither traceability chain resolves

`01-requirements.md` §3 / §5.2 and `01b-qa-validation-plan.md` §4 both mint `AT-001`…`AT-004`, with
**different subjects**:

| id | `01-requirements.md` §3 means | `01b` §4 means |
|---|---|---|
| `AT-001` | US-A golden path — row states `8 open`/`2 over`/`-3d` | US-A golden path (**agrees**) |
| `AT-002` | US-A boundary + negative + width sweep | US-A **undated** boundary |
| `AT-003` | **US-B** — disclosure present-iff-selected via cursor keys | US-A **narrow-width** honesty |
| `AT-004` | **US-B** — the four refusal classes | US-A — the **legend** adds an entry |
| `AT-005` | US-B — legend | *(not minted)* |
| `AT-006` | US-A — the docstring grep | *(not minted)* |
| `AT-010`…`AT-016` | *(not minted)* | US-B differential, negative, shed, blocked pair, C-12, pilot |

`01-requirements.md` §5.2's behavioural table routes **US-B → `AT-003`**. `01b` §10's exit criteria
require **`AT-001..AT-012, AT-015, AT-016`** to exist and pass. Under `01b`'s numbering, `AT-003` is a
US-A test; under the requirements' numbering, `AT-005`/`AT-006` are required and `01b` never mints them,
while `AT-010`–`AT-016` have no requirement pointing at them.

**Both chains are incomplete.** *Blocker by the stated definition ("either traceability chain
incomplete").*

**Fix:** one register wins. Recommend `01b`'s (it is the one with executed set-derivations and reddening
mutations), renumbered so US-A owns a contiguous block and US-B another; then `01-requirements.md`
§3/§5.2 is rewritten to cite those ids. Do not fold by hand-matching subjects — the `AT-003`/`AT-004`
swap is exactly the kind of silent mis-fold that survives review.

---

### BLK-2 — `LLR-003.5`: the predicate is invariant-then-inverted under its own C-40 mutation

`LLR-003.5` declares: *Numeric pass threshold — the disclosure row contains **≥ 4 distinct** braille
glyphs*, and *C-40 mutation — normalise to `len(lane.open)` instead of `lane.total` … Atlas's curve
saturates and its **distinct-glyph count drops***.

Both halves are measurably wrong. Executed (`p5.py`, `p6.py`, `lane_geometry(94,30)`, `rows=1`):

```
=== LLR-003.5 C-40 MUTATION run in-regime: normalise to `total` (correct) vs `open` (mutant) ===
    metric = distinct braille glyphs on the rows=1 disclosure row  (threshold: >= 4)
  --- occupancy typical ---
     Project 0   open=4 total=5  distinct: total-norm=4  open-norm=4   IDENTICAL - vacuous
     Project 1   open=3 total=4  distinct: total-norm=3  open-norm=3   IDENTICAL - vacuous
     Project 2   open=3 total=4  distinct: total-norm=4  open-norm=4   IDENTICAL - vacuous
     Project 4   open=3 total=4  distinct: total-norm=4  open-norm=4   IDENTICAL - vacuous
     Project 3   open=3 total=4  distinct: total-norm=3  open-norm=3   IDENTICAL - vacuous
  --- occupancy extreme ---
     Project 1   open=4 total=6  distinct: total-norm=4  open-norm=4   IDENTICAL - vacuous
     Project 0   open=4 total=6  distinct: total-norm=5  open-norm=5   IDENTICAL - vacuous
     Project 2   open=4 total=6  distinct: total-norm=5  open-norm=5   IDENTICAL - vacuous
     Project 4   open=4 total=5  distinct: total-norm=5  open-norm=5   IDENTICAL - vacuous
     Project 5   open=4 total=5  distinct: total-norm=3  open-norm=3   IDENTICAL - vacuous
     Project 6   open=4 total=5  distinct: total-norm=5  open-norm=5   IDENTICAL - vacuous
     Project 3   open=4 total=6  distinct: total-norm=4  open-norm=4   IDENTICAL - vacuous
     Project 7   open=4 total=5  distinct: total-norm=4  open-norm=4   IDENTICAL - vacuous
```

And on a swept synthetic ladder, where the mutation *does* change the raster, the distinct-glyph count
moves the **wrong way** — the mutant is always ≥ the correct code:

```
=== SEARCH: what open/total ratio makes the rows=1 raster differ AND the >=4 metric flip? ===
  open done  total  raster-differs  distinct(total-norm)  distinct(open-norm)
      4    0      4  False                             7                   7
      4    2      6  True                              6                   7
      4    4      8  True                              5                   7
      4    8     12  True                              3                   7
      4   12     16  True                              3                   7
      6    0      6  False                             8                   8
      6    4     10  True                              5                   8
      6   12     18  True                              3                   8
      8   12     20  True                              4                   6
      8   16     24  True                              3                   6
      8   24     32  True                              3                   6
```

Two independent failures:

- **C-40 limb 1 fail.** The declared subject (the denominator) *is* in the expression, but the predicate
  is **monotone in the wrong direction**: a larger denominator flattens the curve and *reduces* distinct
  glyphs. The mutation makes the test **greener**. A mutation that cannot redden its assertion is not
  falsifiability evidence.
- **The threshold fails on correct code.** `≥ 4 distinct` is violated by **3 of 13** occupancy lanes
  (`typical/Project 1` = 3, `typical/Project 3` = 3, `extreme/Project 5` = 3) at `w=96, h=30` — fully
  in-regime, not the `w<72` case `R-8` flags. The architect's "all ≥ 4, smallest margin on Delta (4)"
  was measured only on its own Phase-1 probe fixture, which is **not on disk**.

**Fix (specified, so Phase 3 is not blocked on judgement):** replace the observable with one that is
monotone in the denominator — **the presence of the full-height cell `⣿` (U+28FF)**. Executed:

```
=== PROPOSED replacement observable: presence of the FULL-HEIGHT cell U+28FF ===
   open done total | correct(total-norm) has ⣿ | mutant(open-norm) has ⣿  | reddens?
      4    0     4 | True                     | True                    | no
      4    2     6 | False                    | True                    | YES
      4    4     8 | False                    | True                    | YES
      4    8    12 | False                    | True                    | YES
      6    0     6 | True                     | True                    | no
      6    6    12 | False                    | True                    | YES
      6   12    18 | False                    | True                    | YES
      8    8    16 | False                    | True                    | YES
      8   16    24 | False                    | True                    | YES
```

Restated predicate, black-box and two-branched: *on a lane where `open < total`, the disclosure row
carries **no** `⣿`; on a lane where `open == total` and the curve reaches its edge, it **does**.* Both
branches are glyphs the reader sees. The `open == total` branch is the anti-vacuity companion — without
it, "no `⣿`" passes on a blank row.

---

### BLK-3 — `AT-014` (the empty-curve lane) is a requirement gap that survived into `01-requirements.md`

`01b` marks `AT-014` BLOCKED on `F-6`. **The block is genuine and the requirements document did not
close it.** Reproduced:

```
=== AT-014: the empty-curve lane (01b's Delta measurement) ===
   Atlas    due_in=20 open=2 wave_edge=62 today_dc=42  lit braille cells on a rows=1 disclosure row = 16
   Delta    due_in=-9 open=1 wave_edge=42 today_dc=42  lit braille cells on a rows=1 disclosure row = 0
      -> disclosure row would be: '·····················╎······················' ... ALL GROUND, no curve
```

Mechanism, now named: when a project's own due date is in the past, `wave_edge` clamps to
`geo.today_dc` (measured, `42 == 42`), and `load_curve` skips every `x > edge`, so the only columns it
may fill are at or before today — where a *future*-dated open task contributes nothing. `Delta` is not
hypothetical: it is a lane of `tests/test_swimlanes.py::typical`, on disk today.

`LLR-003.3` enumerates **four** refusal classes — `titles < 2` with the single title selected, the lead
lane, a resting lane, a lane shed off-screen. **A lane with dated open work whose curve rasterises to
zero lit dots is in none of them.** So on that board the requirements contradict themselves:

- `HLR-003` threshold: *"exactly **1** disclosure row exists"* → satisfied (a row is drawn);
- `LLR-003.5` threshold: *"**≥ 4 distinct** braille glyphs"* → **0** glyphs → fails;
- `C5` (*never a zero standing in for a blank*) and `C6` (*the legend may not describe a mark the view
  is not drawing*) both bite: the legend entry from `HLR-004` would be present while the mark is absent.

*Blocker: an output-producing requirement whose observable deliverable is undefined on a shipped
fixture. No AT can be written against an undefined expected outcome, and I will not invent one.*

**What unblocks it:** one ruling, in `01-requirements.md`, adding a **fifth** refusal class to
`LLR-003.3` — *a lane whose `rows=1` bitmap has zero lit dots draws no disclosure row and earns no
legend entry* — or, if the operator prefers the row to appear, a stated form for what it says. The
first is one line and is consistent with `D-5` (silent refusal) and with `C5`.

---

### BLK-4 — `HLR-003`'s acceptance block observes through an internal symbol

`01-requirements.md` §3 `HLR-003`, *Deliverable + observation*:

> the rendered screen; the row directly below the focused project's row contains ≥1 character in
> `U+2800–U+28FF`; **and that row's index is absent from `App._line_map` (`app.py:275`)**.

`App._line_map` is a private attribute of the app object. An `AT` whose predicate reads it is white-box.
*Blocker by the stated definition ("an `AT` that references an internal symbol").*

Compounding it, and measured: **the shipped surface's plain text is selection-invariant**, so the
non-navigability cannot simply be re-expressed as "the cursor does not stop there" by reading the screen:

```
== BYTE-IDENTITY CHECK (01b claim: 'measured today: byte-identical, curve delta 0') ==
  sel=Fix the ingest path            identical=True
  sel=Write the v2 reference         identical=True
  sel=Ship the migration             identical=True
  sel=Harden the search index        identical=True
  sel=Deprecate v1 endpoints         identical=True
  sel=Retire the old host            identical=True
  -> renders differing from the None render: 0 of 6
```

**Fix:** split it. Non-navigability is a *behaviour*, and it has a black-box form: *drive the cursor key
from `taskboard/keymap.py` through every position of the lane and assert the selection never lands such
that the highlighted row is the curve row.* Locate the highlight through the Pilot's **styled** screen
(`Strip`/segment style), not `.plain` — because `.plain` discards it. Keep the `_line_map` assertion,
demoted to a `TC-NNN` at Layer A where reading an internal is legitimate. `LLR-003.4` already has the
right differential shape for that.

---

## Majors

### MAJ-1 — The operator-accepted Evidence gap (`R-9`) is misdiagnosed; the stated fixture premise is false

`R-9`, `PLAN.md` decision log (2026-08-03, *"Phase 1 approved with a named Evidence gap"*), and the
brief given to me all assert *"every busy fixture has `open == total`"*. Measured — **false on 15 of 16
lanes across three fixtures that are already on disk**:

```
=== R-9 / PLAN 'Evidence gap' CHECK: is `open == total` really true everywhere? ===
  tests/test_swimlanes.py::typical  (the repo's own lanes fixture):
     Atlas      open=2 total=3 done_n=1  open<total? True
     Cinder     open=1 total=1 done_n=0  open<total? False
     Beacon     open=1 total=1 done_n=0  open<total? False
     Delta      open=1 total=1 done_n=0  open<total? False
  tests/test_occupancy.py::fixture('calm'):
     Project 0    open=2 total=3 done_n=1  open<total? True
     Project 1    open=2 total=2 done_n=0  open<total? False
  tests/test_occupancy.py::fixture('typical'):
     Project 0    open=4 total=5 ... True      (5 of 5 lanes True)
  tests/test_occupancy.py::fixture('extreme'):
     Project 1    open=4 total=6 ... True      (8 of 8 lanes True)
```

The cause is one line of `tests/test_occupancy.py::fixture`: phases cycle
`["Backlog","Doing","Done"][j % 3]`, so one task in three is Done. The architect's claim is narrowly
true of its **own Phase-1 probe fixture** (5 projects, 5–8 open) and was generalised into `R-9` as a
property of "any current fixture".

Consequence: **the operator approved a gap that does not exist, and the gap that *does* exist (BLK-2)
was not surfaced.** Phase 3 must not "build a fixture with done work" and report the mutation as run —
that would discharge the wrong debt while the mutation still fails to redden.

### MAJ-2 — `tests/test_occupancy.py` has the same selection hole as `tests/test_vertical_fill.py`, and it is a **declared gate**

`01b`'s `F-7` names `tests/test_vertical_fill.py` as rendering only with `selected_id=None`. Confirmed
(`tests/test_vertical_fill.py:52, :94, :111`). But so does the occupancy census:

```
tests/test_occupancy.py:93:    return str(render_view("swimlanes", b, False, None, TODAY,
```

`LLR-002.5`'s numeric pass threshold — *`census(...)["marked"] >= 45 %` on all three `LOADS` fixtures* —
is therefore **measured in a state US-B never produces**. Since US-B removes 114 cells of wave from the
project rows and adds them back on **at most one** row, the selected state is the *worse* case for
occupancy, and it is the one the gate does not see. `01b`'s `AT-015` gestures at this ("with a task
**selected**, the lanes still spend the height exactly") but its occupancy half still names the
standing floors without saying the census must be re-run **selected**.

Ruling requested in §6 below.

### MAJ-3 — `AT-011`'s completeness companion is circular

`01b` `AT-011`, *completeness companion*: *"that set is asserted to have **≥ 2** members and to cover
every stacked project name **in the render**"*. The set is **derived from the render** in the line
above. Asserting a render-derived set covers every name in the render asserts the set equals itself.

**Mutate the set:** drop a real element — e.g. a lane pushed off-screen by the block loop, or a lane
whose spine the classifier missed. The derived set silently shrinks to `n-1`, the `≥ 2` guard still
holds at `n ≥ 3`, and **the AT stays green**. `AT-001` gets this right (it compares against
`board.visible_projects(False)` plus the `"not shown"` guard); `AT-011` must borrow that companion
verbatim.

### MAJ-4 — `HLR-001`'s and `LLR-001.1`'s thresholds are pinned to a fixture that is not on disk

`HLR-001`: *"for every active non-lead lane of the **busy fixture** (5 lanes) … **5/5 lanes, 3/3
figures**"*. `LLR-001.1`: *"the formatter returns exactly `("8 open","2 over","-3d")` for Atlas and
`("6 open", None, "+0d")` for Cinder … the `over` figure is `None` for the **4** lanes with
`len(lane.late) == 0`"*.

The "busy fixture" is a Phase-1 probe artifact described only in prose (§2.7: *"5 projects, 5–8 open"*).
`5`, `4`, `8 open`, `2 over`, `-3d`, `+0d` are all **hand-listed constants keyed to it**. Phase 3 cannot
reconstruct it from that description — the *dates* are what produce `-3d`/`+0d` and they are nowhere
stated. Either the fixture lands on disk as part of this batch with its dates, or every constant in
those two thresholds is unverifiable. `01b`'s `C-39` discipline (measure the baseline at run time,
never write the count into the assertion) is the right pattern and should be applied here too.

### MAJ-5 — `HLR-004`/`LLR-004.2`: `selected_id` alone cannot answer "is a disclosure row being drawn"

`LLR-004.1` conditions the legend entry on *"only while a disclosure row is being drawn"*, and
`HLR-004`'s boundary catalog requires *"selection exists but is in a refusal class → **no** entry"*.
`LLR-004.2` threads only **`selected_id`** into `legend_entries`.

To honour that, `legend_entries` must recompute the entire refusal chain of `LLR-003.3` — is the
selection's lane drawn? is it the lead? is it resting? does it have a sheddable non-selected title? was
it shed off-screen by the block loop? — from `board`, `width`, `height` alone. That is a **second copy
of `render_swimlanes`' shed logic**, and the codebase already names that failure class:
`swimlane_plan`'s docstring (`views.py:2113–2115`) — *"asking it twice with different numbers is how a
cursor ends up on an undrawn task"*. `D-4` weighs threading-vs-reachability but never addresses
duplication.

Also relevant, and `01b`'s `F-1` has it right: `App._select_first()` guarantees a selection whenever the
board has any visible task, so `LegendModal` will receive a non-`None` `selected_id` on essentially every
real board. **`selected_id is not None` is therefore not a usable gate** — the entry would be near-always
on, which is the ghost `C6` forbids. Requires an architect ruling: either the renderer *returns* whether
it drew a disclosure row (and the legend reads that answer), or `HLR-004` weakens to reachability and
`D-4`'s rejected alternative is reinstated with its weakness recorded.

### MAJ-6 — `AT-016`'s predicate is unrealisable as written, yet it is an exit criterion

`01b` §10.1 requires `AT-016` to exist and pass. `AT-016`'s predicate says *"press the cursor key that
moves the selection into a stacked lane … assert the disclosure row appeared adjacent to the row now
carrying the selection"*. Two unresolved dependencies:

- **which key, and how many presses**, is undefined because `01b`'s own `F-4` (*"on app start the
  focused project is undefined in the drawn sense"*) is listed in §8 as **still needing a ruling** and
  appears in no requirement in `01-requirements.md`;
- **"the row now carrying the selection"** cannot be located from screen text (byte-identity above);
  it must be located by the task's title string, and the AT does not say so.

An exit criterion that depends on an unruled finding is a Phase-3 stop waiting to happen. Either rule
`F-4` in `01-requirements.md` or move `AT-016` out of the exit set with the reason recorded.

### MAJ-7 — `01b` §5's `TC-006` carries a fact `P-6` already corrected

`TC-006` note: *"`wave.load_curve(bm, steps, total, edge)` — **`views.py:986` is its only caller
today**"*. `P-6` in `01-requirements.md` corrected this to **two** callers (`views.py:986` **and**
`report.py:137`). Given as known state in my brief. A `TC` written against "the only caller" will not
check that `report.py:_curve_svg` still gets the contract it expects. Low blast radius (`report.py` is
out of scope for editing) but the `TC`'s stated basis is false and must be re-pointed.

---

## Minors

- **MIN-1 — the classifier's title-braille limitation is misdescribed.** `01b` §7: *"a title
  **beginning** with a braille character would fool the classifier"*. Measured, it is the title's
  **last** character that flips the classification, and only when `gap == 0` (§1 below). The stated
  mitigation ("fixtures assert ASCII titles") is adequate; the stated *mechanism* would lead Phase 3 to
  guard the wrong end. Guard should be `assert t.title.isascii()` over **every** fixture task, not the
  first character.
- **MIN-2 — `01b` §9 checklist item 1 is marked `[x]` while its own text says `✗ deliberately not`.**
  The prose is honest; the checkbox contradicts it. Should be `[ ]` with the waiver, or the item is a
  false green in an evidence checklist.
- **MIN-3 — `01b` §1's geometry baseline omits its height.** *"geometry @96 wide: `label_w=15 ·
  field_w=71 · figs_w=7`"* holds at `h ≥ 30`; at `h ≤ 24` it is `label_w=12 · field_w=74`. Measured
  across the ladder: `w=96 h12:lw12/fw74 h14:lw12/fw74 h24:lw12/fw74 h30:lw15/fw71 h44:lw15/fw71`.
  `AT-003` sweeps widths at `h=30` only, so the narrow-height regime is unswept.
- **MIN-4 — `AT-003`'s width set has no completeness companion.** Importing `WIDTHS` from
  `tests/test_swimlanes.py` is the right derivation (C-31 satisfied on provenance), but if `WIDTHS`
  were ever reduced to `(96,)` the AT would still pass. Add `assert min(WIDTHS) <= 25 and len(WIDTHS) >= 8`.
- **MIN-5 — `AT-004`'s legend completeness companion asserts only "non-empty".** Per C-10 that is the
  weak form. It should assert the swimlanes entry list covers a derived set of the marks the render
  actually contains, which is `R-7`'s converse and the thing this batch is fixing for one mark.
- **MIN-6 — `LLR-005.1`'s set is derived from a string, not from the claim.** `grep "own wave"` finds
  exactly the 3 pinned sites (re-executed: `views.py:903`, `views.py:1100`,
  `tests/test_swimlanes.py:164`), so the pre-state pin of 3 is sound and `AT-006` is **non-vacuous**.
  But a paraphrase — "the project row already draws its progress" without the literal words — is outside
  the set. Add a second grep term (`progress` near `row`) or state the limitation.

---

## The six stress-tests, answered

### 1. The curve-ink classifier — attacked, and it survives on the app's own marks

I implemented `01b` §2's classifier **verbatim** (`braille cell is curve ink iff ≥1 horizontal neighbour
is braille or one of `· ╎ ╽ ╿``) and audited it against ground truth over 2 honest boards × 11 widths ×
3 heights = 66 renders:

```
=== ATTACK 1: honest ASCII titles, full width x height sweep ===
repo lanes fixture (ASCII titles)                    misclassifications: 0
busy fixture, 5 projects / 35 tasks                  misclassifications: 0
```

**"Is there a board state where a phase glyph sits adjacent to field ground and is misclassified as
curve?" — No, and it is structural, not luck.** `_title_row` (`views.py:1088–1091`) composes the row as
the literal `c("▎",…) + "  " + c(glyph,…) + " " + c(body,…)`. The phase glyph is therefore pinned at
**visible index 3**, and indices **2 and 4 are hard-coded spaces** regardless of geometry, title, hue or
archive state. The nearest ground character can begin no earlier than `max(geo.label_w, tail_from)`, and
`lattice_tail` starts at `max(geo.label_w, from_col)` — measured minimum `label_w` over the ladder is
**7**. 3 < 7, with two literal spaces in between. The glyph can never abut ground.

**"Is there a board state where a curve cell is isolated between spaces and misclassified as a glyph?"
— No, and it is also structural.** `field_rows` (`views.py:173–200`) writes **every one** of `geo.field_w`
cells: a lit cell becomes braille, an unlit cell becomes `LATTICE` or a `RULE_PHASES` glyph. It never
emits a space inside the field. Only `out[0]`/`out[-1]` (`◂`/`▸`) and `lead_band`'s single `_put_cell`
`◆` overwrite a cell, and each overwrites at most one — so with `field_w ≥ 3` every interior braille cell
retains at least one in-field neighbour. Measured floor:

```
  w=  24  h12:lw7/fw7  ...          w=  25  h12:lw7/fw8 ...
  -> min field_w over the ladder = 7 ; min label_w = 7
```

`field_w ≥ 7` at every supported width. **Vector closed.**

**The counterexample that does exist — and it is not the phase glyph.** A *task title* whose last
character is braille is misclassified, and the bucket it lands in depends on the title's **length**:

```
=== ATTACK 2: a task title that ENDS in a braille character ===
   row : '▎  ⠤ progress bar ⣿·················╎·························'
        curve idx [18]  glyph idx [3]   <- U+28FF at 18
   row : '▎  ⠤ bar ⣿     ·····················╎·························'
        curve idx []  glyph idx [3, 9]   <- U+28FF at 9
```

Same character, same board, same render. `progress bar ⣿` is 14 cells → `tail_from = 5+14 = 19 ≥
label_w` → `gap == 0` → the `⣿` abuts the lattice tail → **classified curve**. `bar ⣿` is 5 cells →
`gap > 0` → the `⣿` sits between spaces → **classified glyph**. The threshold is `vis(title) ≥ label_w − 5`
(= 10 at `label_w=15`).

**Blast radius, stated honestly:** this does **not** break `AT-010`'s differential — a curve-bearing
title row appears in *both* renders and cancels in the set difference. It **does** break two things:
(a) `01b`'s anti-vacuity companion 3 (*"undated fixture → 0 curve cells"*) goes red on a legitimate
board; (b) if the **shed** title happens to be one of these, it leaves `rows_none` and not
`rows_selected`, so `rows_selected == rows_none ∪ {i}` fails **on a correct implementation**. Both are
closed by the ASCII-title fixture guard — provided it guards the whole title (MIN-1).

**Verdict on the classifier: sound, and better than `01b` claims.** Keep it. Fix the description of its
one limitation.

### 2. C-31 on every set-quantified AT — mutate the set, does it redden?

| AT | the set | derived or hand-listed? | drop a real element → | verdict |
|---|---|---|---|---|
| `AT-001` (`01b`) | project rows recovered by spine glyph | **derived** from the render, completeness against `board.visible_projects(False)` + `"not shown"` guard | completeness companion fails | **PASS** |
| `AT-003` (`01b`) | `WIDTHS` | **derived** — imported from `tests/test_swimlanes.py` | AT still passes if `WIDTHS` shrinks | **weak** → MIN-4 |
| `AT-004` (`01b`) | swimlanes legend entries | **derived** from the return value | only "non-empty" asserted; a 1-entry list passes | **weak** → MIN-5 |
| `AT-010` (`01b`) | curve-bearing row indices | **derived** — classifier output over all lines | n/a (differential, both sides derived the same way) | **PASS** |
| `AT-011` (`01b`) | stacked lanes minus the selected one | **derived**, but companion compares it to **the render** it came from | set shrinks silently, `≥ 2` still holds, AT stays green | **FAIL** → MAJ-3 |
| `AT-012` (`01b`) | title rows of the focused lane | **derived**, baseline `n0` measured at run time, `n0 ≥ 2` fixture guard | drift to `titles==1` reddens by design | **PASS** — the strongest one here |
| `HLR-001` (reqs) | "5 lanes", "3 figures", "4 lanes with no late" | **hand-listed**, keyed to an off-disk fixture | nothing reddens; the constants are unverifiable | **FAIL** → MAJ-4 |
| `LLR-003.4` (reqs) | 4 fixtures × `h ∈ {24,30,44}` = 12 comparisons | **hand-listed count**, but the comparison is differential byte-equality | dropping a fixture silently reduces coverage; no completeness assert | **weak** |
| `LLR-005.1` / `AT-006` (reqs) | 3 `"own wave"` grep hits | **derived** from the grep, pre-state **pinned at 3** (re-executed, still 3) | a 4th site would break the pin | **PASS** |

### 3. C-40 limb 1 on every predicate — is the subject in the expression?

Verified the load-bearing one first, as instructed. **`01b`'s byte-identity claim reproduces exactly**
(output pasted in BLK-4): `str(render_view(… None …)) == str(render_view(… selected …))` is `True` for
**6 of 6** selectable tasks on the repo's own lanes fixture. US-B's predicate **is red on the unmodified
tree** and can only go green by the change. That is the best falsifiability evidence available and it
stands.

One caveat `01b` does not state: the identity holds for the **plain** projection only. Selection *is*
present in the markup (`_title_row` wraps the selected title in `[reverse]`). So the evidence is valid
for a `.plain`-based predicate, and any AT that needs to *locate* the selection must do it by title
string, never by highlight — which is exactly the constraint MAJ-6 says `AT-016` fails to state.

Remaining limb-1 findings:

- **`LLR-003.5` — FAIL**, and worse than invariant: **inverted**. BLK-2.
- **`LLR-002.3` — degenerate but acceptable.** *"`rg -n "^WAVE_ROWS|^DISCLOSURE_ROWS"` returns 0"*
  passes on the unmodified tree. It is a **prohibition**, and a prohibition that is green before the
  change is not a vacuous check — it is a tripwire. Recorded, not raised.
- **`LLR-001.3` — PASS, and unusually well done.** The architect noticed its own mutation was
  out-of-regime and re-specified it at `w=40` rather than `w=96`. That is the probe-regime rule applied
  correctly and it should survive review untouched.
- **`LLR-002.1` — PASS.** "charge `0` instead of `1` per project lane" changes `need` by `len(opens)`
  and the height sweep sees blank rows. Subject is in the expression.
- **`LLR-004.2` — PASS as a mutation** (truthy default → no-ghost goes red), but the *requirement* it
  gates is unsatisfiable as written. MAJ-5.
- **`AT-012` (`01b`) — PASS**, four mutations each hitting a distinct clause.

### 4. The two BLOCKED ATs

**`AT-013` (`titles == 1`) — the block is STALE, not real. Unblock it now.** The measurement is
reproduced:

```
   lanes fixture (Atlas lead; 3 stacked 1-open lanes)   h= 24 -> allocate = (1, 5, 4)
   lanes fixture (Atlas lead; 3 stacked 1-open lanes)   h= 30 -> allocate = (1, 8, 5)
   lanes fixture (Atlas lead; 3 stacked 1-open lanes)   h= 44 -> allocate = (1, 10, 9)
   occupancy extreme                                    h= 24 -> allocate = (1, 6, 1)
```

`titles == 1` is real at every size on the repo's own lanes fixture and at `h=24` on occupancy-extreme.
But `01b` was authored in parallel with the ruling, and **the ruling exists**: `O-1` (PLAN decision log,
2026-08-03; `LLR-003.3`) = *silent refusal*. That is `01b`'s own option **(i)** — *"no disclosure row is
shown when the lane cannot pay, and the lane renders exactly as with `None`"*. `01b` says each option is
"a one-line predicate". **Write it.** `AT-013` becomes: render the lanes fixture with the single title
of a stacked lane selected; assert the focused lane's row block is byte-identical to the `None` render's,
and that `rows == h`, `blank == 0`, and `"not shown"` is absent. Nothing further is owed.

**`AT-014` (empty curve) — genuinely blocked, by measurement, and the requirements did not close it.**
Full analysis in BLK-3. **What unblocks it:** a fifth refusal class in `LLR-003.3`. One line, one gate.

Neither block is "missing effort". `01b` was right to refuse to invent the expected outcome for both;
it is wrong only in that one of the two has since been ruled.

### 5. The `LLR-003.5` fixture — the specification you asked for

**The premise is false; the fixture already exists.** See MAJ-1 for the measurement (15/16 lanes have
`open < total`, including 5/5 on `tests/test_occupancy.py::fixture("typical")` and 8/8 on `"extreme"`).
The raster genuinely differs under the mutation on those lanes — hamming distance 2–33 cells:

```
=== is the CURVE identical, or is the >=4-distinct-glyph METRIC blind? ===
  typical  Project 0   o=4 T=5 raster-identical=False  hamming=2
  typical  Project 4   o=3 T=4 raster-identical=False  hamming=13
  extreme  Project 7   o=4 T=5 raster-identical=False  hamming=33
```

So the mutation **is** runnable in-regime today. It fails to redden because the *observable* is blind,
not because the fixture is missing (BLK-2).

**Nevertheless, the existing fixtures are a poor gate — their `open/total` ratios (4/5, 3/4, 4/6) sit in
the band where the 4-dot-row quantisation swallows the difference.** So Phase 3 does owe a fixture, for
a different reason: **margin**. Specified exactly, so nothing is left to judgement:

> **Fixture `ledger` — for `LLR-003.5`'s C-40 mutation only.**
> - **1 project**, `name="Ledger"`, `color="lime"`, `status="on_track"`, **`due_date = TODAY + 14d`**
>   (must be in the **future** — a past project due date clamps `wave_edge` to `today_dc` and produces
>   the zero-lit row of BLK-3).
> - **4 open tasks**, `phase="Doing"`, `priority="normal"`, **`due_date = TODAY + {1, 4, 8, 12}d`** —
>   strictly after today and strictly at or before the project's due date, so every one of them lands
>   inside `[today_dc, wave_edge]` and the cumulative curve actually rises across the window.
> - **8 done tasks**, `phase="Done"` (the board's last phase — this is what makes `board.is_done` true),
>   `due_date = TODAY − 2d`. They contribute to `total` and to nothing else.
> - **0 archived tasks** (archived work is excluded from `open` *and* counted in `total`, which would
>   confound the ratio).
> - Resulting lane facts, to be asserted in the fixture's own guard so drift reddens:
>   **`len(lane.open) == 4`, `lane.total == 12`, `lane.done_n == 8`, `lane.due_in == 14`.**
> - A **second project** with ≥1 open task is required so the lane under test is a *stacked* lane and
>   not the lead — give it 1 open task due `TODAY + 3d` and its own future due date.
>
> **Why 4/12 and not 4/5:** measured, `4 open / 8 done / total 12` is the first point on the swept
> ladder where the correct code drops the full-height cell while the mutant keeps it, with the
> distinct-glyph count also separating 3 vs 7 — a 4-glyph margin instead of 0.
>
> **Predicate to run against it** (replacing `LLR-003.5`'s threshold, per BLK-2):
> the `Ledger` disclosure row contains **no** `⣿` (U+28FF) — and, as the anti-vacuity companion, the
> same board's *second* project (`open == total`) **does**. Mutating `max(1, lane.total)` →
> `max(1, len(lane.open))` makes `Ledger` grow a `⣿` and the assertion goes red.

### 6. Ruling on `tests/test_vertical_fill.py`

**Ruling: NOT a blocker for US-B's acceptance. It is a MAJOR gap that must be closed in Phase 3, and it
is larger than `01b` states.**

Reasoning:

- The never-pads law is **pre-existing**, not created by US-B. US-B does not change the law; it enlarges
  the state space over which the law must hold. A pre-existing law that does not yet cover a new state is
  a coverage gap, not an unmet acceptance criterion — and `HLR-002`'s own acceptance already commits to
  `rows == h, blank == 0` as a batch gate, so the obligation is on the books.
- **But**: `LLR-002.4`'s Statement says *"For **every** board and **every** height"* with no selection
  qualifier. If Phase 3 discharges it by sweeping only `selected_id=None`, it discharges an LLR whose
  quantifier it did not honour — a vacuous close, which rule 12 forbids.
- And the hole is **two files, not one**: `tests/test_occupancy.py:93` renders with `None` as well, and
  that file *is* `LLR-002.5`'s declared gate (MAJ-2). The selected state is the occupancy-adverse case,
  so the gate as written cannot see the risk it exists to catch.

**Therefore, as a Phase-3 exit condition (not a Phase-2 blocker):**

1. `tests/test_vertical_fill.py`'s swimlanes sweep gains a **second pass with a stacked-lane task
   selected**, task chosen from the render at run time (never a hard-coded id), asserting the same
   `rows == h`, `blank == 0`, `pinned == 1`.
2. `tests/test_occupancy.py::render` gains a `selected_id` parameter defaulting to `None` (so all
   existing call sites are untouched), and `LLR-002.5`'s threshold is restated as
   **`census(...)["marked"] >= 45 %` on all three `LOADS` × {`None`, selected}** — six readings, not three.
3. Both are named in `01-requirements.md` under `LLR-002.4`/`LLR-002.5` before Phase 3 starts, so they
   are requirements rather than a reviewer's suggestion.

`01b`'s `AT-015` is the right instinct and covers roughly half of this; it must be extended to the
occupancy census explicitly.

---

## What must happen before the Phase-2 gate closes

| # | Owner | Action | Blocks |
|---|---|---|---|
| 1 | `qa` + `architect` | Collapse the two `AT-NNN` registers into one; rewrite `01-requirements.md` §3/§5.2 and `01b` §4/§10 against it. | BLK-1 |
| 2 | `architect` | Replace `LLR-003.5`'s threshold with the `⣿` predicate and its `open == total` companion; correct the C-40 mutation's stated direction. | BLK-2 |
| 3 | `architect` | Add the **fifth refusal class** to `LLR-003.3` (zero-lit-dot lane) and mirror it in `HLR-003`'s boundary catalog and `HLR-004`'s. | BLK-3 |
| 4 | `architect` | Rewrite `HLR-003`'s *Deliverable + observation* so no `AT` reads `App._line_map`; demote that assertion to `LLR-003.4`'s `TC`. | BLK-4 |
| 5 | `architect` | Correct `R-9` and the `PLAN.md` decision-log row: the fixture premise is false; the debt is a predicate, not a fixture. Land the `ledger` fixture spec from §5. | MAJ-1 |
| 6 | `architect` | Rule `MAJ-5`: how the legend learns a disclosure row was drawn, without a second copy of the shed logic. | MAJ-5 |
| 7 | `architect` | Rule `F-4` (initial frame) or descope `AT-016` from the exit set, in writing. | MAJ-6 |
| 8 | `architect` | Land the `ledger`/busy fixtures on disk with their **dates**, or convert `HLR-001`/`LLR-001.1`'s constants to run-time-measured baselines. | MAJ-4 |
| 9 | `qa` | `AT-011` borrows `AT-001`'s model-side completeness companion. Unblock `AT-013` against `O-1`. Fix MIN-1…MIN-6. | MAJ-3, minors |
| 10 | `architect` | Add the selected-state sweep to `LLR-002.4` and the six-reading census to `LLR-002.5`. | §6 ruling |

**Not raised, deliberately:** `O-1` and `O-2` are operator rulings already recorded in `PLAN.md`'s
decision log and I do not reopen them. `R-5` (P-1/P-2 carried, not re-executed) is correctly recorded as
carried and neither premise, if it flipped, changes a requirement — agreed, not blocking. `R-6`
(`report.py`'s docstring) is correctly deferred to the post-mortem. `R-7` (the no-ghost law's asymmetry)
is the right control candidate and belongs in `dev-flow-lessons`, not in this batch.

---

## Evidence checklist (`qa-reviewer`, Phase 2)

- [x] **Acceptance criteria use Given/When/Then** — ✗ **deliberately not, and I agree with `01b`'s
  waiver for the same reason it gave.** These are differential render predicates; G/W/T would hide that
  the assertion compares two renders. Flagged here rather than silently reformatted — but `01b` §9 marks
  this item `[x]` while its own text says `✗`, which is MIN-2.
- [x] **Test cases have explicit Expected, not vague "works"** — every finding names the compared
  quantity and the direction it must move (BLK-2 names `⣿` present/absent; §5 names `open==4, total==12`).
- [x] **Edge cases include empty, boundary, invalid, error** — empty curve (BLK-3), `titles==1` boundary
  (§4), inverted-mutation invalid (BLK-2), classifier error states swept over 66 renders (§1).
- [x] **Regression checklist exists** — §6's three Phase-3 exit conditions; MAJ-2's occupancy re-gate;
  MAJ-7's `report.py` contract.
- [x] **Exit criteria stated** — the 10-row table above; the gate does not close until rows 1–4 land.
- [x] **No real PII / secrets** — every probe built synthetic `Project`/`Task` objects in
  `tempfile.mkdtemp()`. **No probe read the operator's real board.**
- [x] **Test results section left blank** — nothing here is reported as a test outcome. Every figure is a
  **measurement of the current tree at `f237cb3`**, labelled as such, with the producing script named.
- [x] **Layer B (black-box)** — every blocker is stated in terms of what is observable through
  `render_view` / `App.run_test()`; BLK-4 exists *because* an AT reached past that surface.
- [x] **Bidirectional surface-reachability** — inputs (`selected_id`, width, height, board shape,
  `show_archived`) and outputs (row readout, disclosure row, legend entry, occupancy census) were each
  traced to an observation method; MAJ-2 and MAJ-5 are the two places the trace broke.
- [x] **No unfilled template** — no `<...>`, no `TC-NNN` stubs, no empty required rows. BLK-3 and MAJ-5
  are open **rulings** with the exact one-line fix specified, which is a filled row.
- [x] **Read-only** — `git status --short` over `taskboard/` and `tests/` is clean; the only file this
  review wrote is `.dev-flow/02-review-qa.md`.

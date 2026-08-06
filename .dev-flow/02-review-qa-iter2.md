# 02 — QA RE-REVIEW (iteration 2) · batch `2026-08-03-batch-03`

**Repo:** `C:\Users\jjgh8\Github\taskboard` · **branch** `main` · **base ref** `f237cb3`
(verified: `git log --oneline -1` → `f237cb3 Close the vertical-fill batch and reconcile a day-stale backlog`;
`git status --short` over `taskboard/` and `tests/` is empty).
**Reviewer:** `qa-reviewer`, second pass, reviewing the amended `01-requirements.md` (966 lines, 18 amendments in §6.5)
against the two Phase-2 cross-reviews it answers.
**Probes:** read-only, executed 2026-08-06 from `C:\Users\jjgh8\AppData\Local\Temp\qa2it2`. Every board is a synthetic
`Board`/`Project`/`Task` built in a temp dir. **No probe read the operator's real board. No file under `taskboard/` or
`tests/` was written.** The post-change renderer is simulated by monkeypatching `views.allocate` / `views.project_wave`
**in memory** — post-change is exactly the current renderer with `wrows` pinned to 1, because `stack_block` already
draws `wrows + min(titles, o)` rows.
**Regime for every figure:** `TODAY = 2026-07-30`, `show_archived=False`, `tick=0`, geometry stated per measurement.

---

## Verdict

**GATE: STILL BLOCKED.** 3 blockers · 6 majors · 5 minors.

Three of the five prior blockers are genuinely closed and I reproduced their evidence. The other two are not, and the
amendment introduced one blocker of its own — which is the headline.

**The single most important sentence in this review:** the batch's flagship correction, amendment **A-6**, is
**backwards**. `swimlane_plan` already subtracts the lead band's two extra rows *at the call site*
(`views.py:2126`: `allocate(..., h - 2 - (2 if active else 0))`). There is no undercount. Charging `prof + 2` inside
`need` while leaving that call site alone double-counts those two rows and **pads 28 blank rows over 18 renders** —
a direct violation of C2, LLR-002.4 and the batch's own acceptance criterion. The `44 blank / 18-of-18 shed` figure is
reproducible **only** if `room` is silently changed to `h - 2`, and no requirement in the artifact says to change it.

| # | Prior blocker | Verdict |
|---|---|---|
| 1 | `AT-NNN` id collision (BLK-1 / A-18) | ✅ **CLOSED** — with one major left behind (M-A) |
| 2 | `LLR-003.5`'s inverted predicate (BLK-2 / A-10) | ✅ **CLOSED on direction** — 13/15 reproduced exactly — but the replacement carries two new defects (M-B, M-C) |
| 3 | `HLR-003` naming `App._line_map` (BLK-4 / A-3) | ✅ **CLOSED** |
| 4 | `AT-011`'s circular completeness companion (MAJ-3 / `AT-024`) | ✅ **CLOSED in effect** — but not by the half the artifact credits (M-D) |
| 5 | The refusal set R0–R6's totality (BLK-3 / A-8) | 🚨 **STILL OPEN** — an eighth reachable state, measured on an on-disk fixture |

---

## 1. Prior blocker 1 — the `AT-NNN` id collision · **CLOSED**

**Executed.** Enumerated every `AT-NNN` token in the amended artifact and diffed subjects:

```
     10 AT-001      9 AT-002     15 AT-003     18 AT-004      4 AT-005      6 AT-006
      1 AT-010      1 AT-011      1 AT-012      2 AT-013      2 AT-014      1 AT-015      2 AT-016
      5 AT-020      3 AT-021      4 AT-022      4 AT-023      4 AT-024      2 AT-025
      8 AT-026      9 AT-027      3 AT-028
```

The canonical register (§3.0) mints exactly **15** ids: `AT-001`…`AT-006` + `AT-020`…`AT-028`. Every occurrence of
`AT-010`…`AT-016` was read in context — **all 12 are explicit `01b`-legacy references** at `:203, :204, :205, :206,
:207, :208, :215, :759`, each of the form *"(was `01b` AT-0NN)"* or *"`AT-013` and `AT-014` of the old QA numbering"*.
**No id appears twice with different subjects.** §5.2's behavioural table has 15 rows and §5.3's split (US-A 6 · US-B 8 ·
shared 1 = 15) reconciles. Both retirements (`01b AT-001` → `AT-001`, `01b AT-016` → `AT-003`) cite both origins.

### 🟠 M-A (major, NEW) — `HLR-001`'s boundary catalog still routes to an `AT` whose subject changed

The register was canonicalised (A-18) but `HLR-001`'s **Boundary catalog (QC-3)** was not re-pointed. All four entries
cite `AT-002`:

> ☑ empty — *"Covered by `AT-002` asserting no D-text appears on a `▏` row"*
> ☑ boundary — *"0 overdue … exactly 1 open task … all undated. `AT-002`."*
> ☑ invalid — *"`+0d` is a real distance and **shall** be drawn. `AT-002`."*
> ☑ error — *"narrow widths … `AT-002` sweeps `WIDTHS`."*

`AT-002`'s canonical subject in §3.0 is: *"The panel is exactly `h` rows with **0** blank rows and every line exactly
`max(24, w)` cells."* It asserts **nothing** about D-text on a resting row, about the `over` figure being absent, about
`+0d`, or about token-dropping. Those subjects belong to `AT-001`, `AT-020` and `AT-021`, which exist and are unused by
this catalog. **US-A's black-box boundary evidence therefore points at a test that cannot produce it** — which is the
same class of defect BLK-1 was raised for, surviving one layer down.

### 🔵 m-A (minor, NEW) — `01b-qa-validation-plan.md` still carries the colliding register on disk

The artifact states `01b` is *"retained on disk only as the origin record"*, but the file itself carries no supersession
header, and its §10 exit criteria still require `AT-001..AT-012, AT-015, AT-016` to exist and pass. Phase 3 reading
`01b` directly would re-collide. One line at the top of `01b` closes it.

---

## 2. Prior blocker 2 — `LLR-003.5`'s inverted predicate · **CLOSED on direction, two new defects**

**Executed.** Re-ran the `⣿` (U+28FF) sweep myself on the `rows=1` disclosure row, correct (`max(1, lane.total)`) vs
mutant (`max(1, len(lane.open))`), over the `ledger` fixture as LLR-003.7 specifies it plus `tests/test_occupancy.py::
fixture("typical")` and `("extreme")`, at `lane_geometry(94, 30)`. The non-mutant path was checked byte-for-byte against
the shipped `project_wave(lane, geo, TODAY, 1)` path — **0 fidelity mismatches**, so the probe measured the shipped code:

```
  fixture      lane           o/T   correct-has-FULL  mutant-has-FULL  reddens
  ledger       Ledger         4/12          False             True      YES
  ledger       Mirror         3/3            True             True no (companion)
  typical(occ) Project 0      4/5           False            False       no
  typical(occ) Project 1      3/4           False             True      YES
  typical(occ) Project 2      3/4           False             True      YES
  typical(occ) Project 4      3/4           False             True      YES
  typical(occ) Project 3      3/4           False             True      YES
  extreme(occ) Project 1      4/6           False             True      YES
  extreme(occ) Project 0      4/6           False             True      YES
  extreme(occ) Project 2      4/6           False             True      YES
  extreme(occ) Project 4      4/5           False             True      YES
  extreme(occ) Project 5      4/5           False             True      YES
  extreme(occ) Project 6      4/5           False             True      YES
  extreme(occ) Project 3      4/6           False             True      YES
  extreme(occ) Project 7      4/5           False             True      YES
  -> reddens on 13 of 15 lanes swept (correct-path fidelity mismatches: 0)
```

**13 of 15 reproduces exactly, lane for lane.** The direction is now correct: the mutant grows a `⣿` the correct code
does not draw. BLK-2's first limb is closed.

The plateau refinement also reproduces, and it is a real refinement:

```
  dues=(2, 5, 9) projdue=+10  open==total==3  full dot-cols=2   has U+28FF=False
  dues=(1, 2, 3) projdue=+10  open==total==3  full dot-cols=8   has U+28FF=True
  dues=(1, 2, 3) projdue=+14  open==total==3  full dot-cols=12  has U+28FF=True
  dues=(2, 5, 9) projdue=+14  open==total==3  full dot-cols=6   has U+28FF=True
```

`open == total` alone is **not** sufficient — confirmed. Note the fourth row, which the artifact does not state: the
same dues `(2,5,9)` **do** produce a `⣿` once the project's due date moves to `+14`, so the companion depends on the
project due date as well as on the plateau. `LLR-003.7`'s `Mirror` (dues `1,2,3`, project due `+14`, 12 full columns) is
well clear of the knife edge; the spec is sound. Recorded so Phase 3 does not read "a plateau" as the only variable.

### 🟠 M-B (major, NEW) — the artifact mis-names its own two non-reddening lanes

`LLR-003.5` and P-20 both assert: *"The two non-reddening lanes are exactly the two with `open == total` — which is the
anti-vacuity companion, not a miss."*

**Measured, that is false, and it is arithmetically impossible.** The swept set contains exactly **one** `open == total`
lane (`Mirror`, 3/3). The second non-reddener is **`occupancy typical / Project 0` at `open=4, total=5`** — an
`open < total` lane where the **mutant also draws no `⣿`**, so the mutation is simply invariant there. The artifact's
own pasted table in `LLR-003.5` lists 14 rows and silently omits `Project 0`, which is the 15th. The consequence is not
cosmetic: it means the mutation is invariant on **1 of the 13** `open < total` lanes swept, and Phase 3 told that the
only non-reddeners are companions will read an invariant case as a designed one.

### 🟠 M-C (major, NEW) — the replacement predicate is a `shall` that correct code violates

`LLR-003.5`'s Statement is normative: *"on a lane where `len(lane.open) < lane.total`, the disclosure row **shall**
contain **no** full-height cell `⣿`"*.

`load_curve` lights `round(bm.h * v / total)` dots and `bm.h = 4` at `rows=1`, so a full column needs
`round(4·open/total) == 4`, i.e. `open/total >= 0.875`. Executed on synthetic single-project boards, all dated inside
the window:

```
  open done total  open/total  round(4*o/T)  correct code has U+28FF ?  predicate
     4    1     5      0.800        3          False                   HOLDS
     6    1     7      0.857        3          False                   HOLDS
     7    1     8      0.875        4          True                    *** VIOLATED by correct code ***
     9    1    10      0.900        4          True                    *** VIOLATED by correct code ***
    15    1    16      0.938        4          True                    *** VIOLATED by correct code ***
     3    1     4      0.750        3          False                   HOLDS
     4    4     8      0.500        2          False                   HOLDS
```

This is **the same class of defect as the one it replaces** — the old `≥ 4 distinct` false-failed 3 of 13 in-regime
lanes; this one false-fails any lane at `open/total ≥ 0.875`. It is narrower (no current fixture reaches it) but it is a
`shall`, and `tests/test_occupancy.py::fixture` cycles a `Done` phase every third task, so a fixture edit that changes
that cadence walks straight into it. **Fix, one clause:** scope the predicate to `round(4·open/total) < 4`, or state it
**differentially** — *"the correct render and the `open`-normalised render differ in whether the row carries `⣿`"* —
which is what the 13/15 sweep actually measures.

---

## 3. Prior blocker 3 — `HLR-003` naming `App._line_map` · **CLOSED**

Read the amended `HLR-003` *Deliverable + observation* (§3, A-3). The `_line_map` clause is deleted, and the three
replacements are genuinely screen-only:

1. curve ink by the §3.0.1 adjacency classifier over the rendered row — references no internal symbol;
2. the anchor row located by **the selected task's title string** — a search over rendered text;
3. non-navigability observed as a **behaviour**, driving the cursor key and reading the highlight from the Pilot's
   **styled** screen (segment style).

The `_line_map` assertion is re-homed to `TC-018` under `LLR-003.4` at Layer A (§4, §5.2 row for LLR-003.4), where
reading an internal is legitimate. The supporting measurement reproduces:

```
plain identical to the None render: 6 of 6
markup DIFFERS from the None render: 3 of 6
```

Observation (3) is sound: the highlight **is** in the markup, so the styled screen can see it while `.plain` cannot.

### 🔵 m-B (minor, NEW) — observation (3) has three dead positions on the fixture it will run on

The markup differs for only **3 of 6** selectable tasks on the repo's lanes fixture — the other three are `R4` (the task
is selectable but not drawn as a title row). `AT-003`'s predicate says *"driving the cursor key through **every**
position of the lane"*; on that fixture three of six cursor positions produce no observable change at all. Not a
defect, but Phase 3 must not read "no highlight moved" as a failure. State it in `AT-003`.

---

## 4. Prior blocker 4 — `AT-011`'s circular completeness companion · **CLOSED in effect**

**Executed the mutation the brief asks for: lose a real lane from the render** (by shrinking the height until the block
loop sheds one), and evaluated the amended companion — derived-from-render set vs
`{p.name for p in board.visible_projects(False)}` (+ `"Inbox"` iff orphans) **and** `"not shown"` absent in both
renders:

```
  board    w x h  labels found/model 'not shown'  verdict  lost
  extreme  96x44       8     8/8     False       GREEN  []
  extreme  96x30       8     8/8     False       GREEN  []
  extreme  96x24       8     8/8     False       GREEN  []
  extreme  96x20       8     8/8     False       GREEN  []
  extreme  96x16       8     8/8     False       GREEN  []
  extreme  96x14       8     8/8     False       GREEN  []
  extreme  96x12       7     8/8     True        RED    []
  (calm and typical: GREEN at every swept size)

  the OLD circular companion on the SAME renders (>= 2 members, covers the render):
  extreme  96x30  |set|=8  old companion -> GREEN (blind)
  extreme  96x16  |set|=6  old companion -> GREEN (blind)
  extreme  96x12  |set|=5  old companion -> GREEN (blind)
```

**The amended companion reddens where the old one stayed green.** MAJ-3 is closed. But it is closed by the
`"not shown"` guard, **not** by the set-equality half the amendment emphasises — and that matters:

### 🟠 M-D (major, NEW) — the set-equality half is not evaluable at `h ≤ 24`

The rendered project label is clipped to `geo.label_w` **with an ellipsis**, and on the occupancy fixtures every project
name shares a 7-character prefix. Executed, same board, two heights:

```
--- calm 96x30 ---           (label_w = 15)
'▌ PROJECT 0    ·····················╎···'
'▎ Project 1    ·····················╎·⢸⣿'
--- calm 96x24 ---           (label_w = 12)
'▌ PROJECT 0 ······················╎·····'
'▎ Projec…   ······················╎·⢸⣿⣿⣿'
```

`Projec…` prefix-matches **all eight** `Project N` names, so a name-based derived-vs-model comparison **over-matches**
and goes green regardless of which lanes are present — exactly the blindness MAJ-3 set out to remove. It is only
above `h ≥ 30` (`label_w = 15`, `"Project 0"` fits whole) that the half works. This affects `AT-024` **and `AT-001`**,
whose completeness companion is specified the same way, and `AT-021` explicitly sweeps `h ∈ {12, 24, 30, 44}`.

The good news, and it is worth stating so the fix is cheap: **`"not shown"` is a complete detector of lane loss.** A
lane can only leave the render through the block loop, and that path always sets `shed > 0` and prints the note
(`views.py:1294–1300`). So the honest specification is: *the `"not shown"` guard is the completeness companion*; the
name-set comparison is a redundant cross-check that must be scoped to `h ≥ 30` or matched clip-aware.

---

## 5. Prior blocker 5 — the refusal set R0–R6's totality · 🚨 **STILL OPEN**

The artifact argues totality from three checked facts (every predicate total · the lane taxonomy is closed · a drawn
lane is drawn whole) rather than from enumeration. **The logic is sound and I did not break it.** What I broke is
clause 7.

I could not construct a state that reaches none of R0–R6 and is *not* payable — the refusal set is the literal
complement of a seven-way conjunction, so that is a tautology and I say so rather than dressing it up. So I attacked
the question that decides whether the conjunction is the *right* one: **is there a state that passes all seven clauses
and still puts a curve-less stripe under the cursor — R6's exact failure mode, reached through a door R6 does not
watch?**

Yes. Clause 7 is `project_wave(lane, geo, today, 1).lit() > 0` — a property of the **bitmap**. What the reader sees is
the **drawn row**, and `field_rows` overwrites `out[0]` / `out[-1]` with the off-window marks `◂` / `▸`
(`views.py:173–200`, `_off_window` at `views.py:999`). The two disagree:

```
=== clause 7 (`bm.lit() > 0`) vs what the row DRAWS ===
  fixture      lane        w x h    bm.lit  braille-in-row  offL/offR
  lanes::typical Beacon       24x12       4              0   False/True   *** DISAGREE ***
  occ typical   Project 2    24x12       3              0   False/True   *** DISAGREE ***
  occ typical   Project 4    24x12       3              0   False/True   *** DISAGREE ***
  occ typical   Project 3    24x12       3              0   False/True   *** DISAGREE ***
  occ extreme   Project 4    40x20       3              0   False/True   *** DISAGREE ***
  occ extreme   Project 5    40x20       3              0   False/True   *** DISAGREE ***
  occ extreme   Project 6    40x20       3              0   False/True   *** DISAGREE ***
  occ extreme   Project 2/3/4/5/6  24x12  3             0   False/True   *** DISAGREE ***
  -> disagreements over the swept fixtures/sizes: 12
```

Then I evaluated the **full seven-clause conjunction**, post-change, over every selectable task on five fixtures × 16
sizes — lane in `body`, not lead, not resting, selected task among the drawn titles, ≥ 1 other drawn title,
`bm.lit() > 0`:

```
payable tasks whose disclosure row would draw ZERO braille:
  fixture      w x h  lane        task                     bm.lit  drawn
  occ typical    32x24  Project 4   Task 4-0 something real       3      0
  occ typical    32x24  Project 4   Task 4-1 something real       3      0
  occ typical    32x24  Project 4   Task 4-3 something real       3      0
  occ typical    25x20  Project 2   Task 2-0 something real       4      0
  occ typical    25x20  Project 2   Task 2-1 something real       4      0
  occ typical    25x20  Project 4   Task 4-0 something real       3      0
  occ typical    25x20  Project 4   Task 4-1 something real       3      0
  occ typical    25x20  Project 3   Task 3-0 something real       3      0
  occ typical    25x20  Project 3   Task 3-1 something real       3      0
  occ typical    24x30  Project 2   Task 2-0 something real       3      0
  occ typical    24x30  Project 2   Task 2-1 something real       3      0
  occ typical    24x30  Project 2   Task 2-3 something real       3      0
  -> payable (task, size) pairs evaluated: 448
  -> of those, disclosure row draws ZERO braille: 82
```

**82 of 448.** The mechanism, printed for `occupancy typical / Project 2`:

```
25x20 field_w=8  dot_w=16  lit=4  offL=False offR=True
   with off marks : '··╎····▸'
   without marks  : '··╎····⣰'
32x24 field_w=12 dot_w=24 lit=20 offL=False offR=True
   with off marks : '···╎····⣠⣴⣶▸'
   without marks  : '···╎····⣠⣴⣶⣶'
96x30 field_w=71 dot_w=142 lit=41 offL=False offR=False
   with off marks : '·····················╎····⣠⣴⣶⣶⣶⣶⣶⡆·······…'
```

At narrow widths the whole one-row curve collapses onto the last cell, and `off_right` replaces it with `▸`.
**The reader sees a lane row, then a blank stripe, and a real named task has been shed to pay for it** — C5 (*never a
zero standing in for a blank*) and C6 (the legend names an absent mark) both bite, which is precisely the argument that
made R6 a blocker in the first review.

This is **reachable on `tests/test_occupancy.py::fixture("typical")`, on disk today, at widths 24 / 25 / 31 / 32 — all
four inside the `WIDTHS` ladder `tests/test_swimlanes.py:88` already sweeps** and that `AT-002` / `AT-021` will sweep.
It is not the `w < 72` "assumed — verify in Phase 3" of R-8; R-8 says the *distinct-glyph count may flatten*. This says
**the refusal predicate is wrong**.

🚨 **B-1 (blocker, NEW).** `LLR-003.3` clause 7 must observe the **drawn row**, not the bitmap:
*"`field_rows(project_wave(lane, geo, today, 1), geo, lane.hue, off_left=…, off_right=…)` contains at least one
character in `U+2800–U+28FF`."* One clause, same shape, and it makes `AT-027`'s predicate and `AT-003`'s positive
predicate agree instead of contradicting each other on 82 states. Note the artifact's own totality argument survives the
fix untouched — the conjunction stays seven-way and stays total; only clause 7's *object* changes.

---

## 6. The headline — `LLR-002.1` / A-6 · 🚨 **STILL OPEN, and the number is inverted**

**My derivation does not agree with the artifact's, and the disagreement is not in the arithmetic — it is in what
`room` is.**

`swimlane_plan` (`views.py:2126`) calls:

```python
titles, prof, wrows = allocate(
    geo, nameable,
    len([ln for ln in lanes if ln.resting]), h - 2 - (2 if active else 0))
```

**The `- (2 if active else 0)` term IS the lead band's head row and worst-late tail row.** They are already subtracted,
at the call site, from the room the search may spend. `need` charging `prof` is therefore not an undercount — it is the
matching half of a two-part accounting that is already correct. P-16's premise is false.

I confirmed `lead_band` does render `prof + 2` (this half of P-16 is true):

```
len(lead_band(prof=4))  = 6    (prof+2 = 6)
len(lead_band(prof=10)) = 12   (prof+2 = 12)
len(lead_band(prof=24)) = 26   (prof+2 = 26)
len(lead_band(prof=33)) = 35   (prof+2 = 35)
```

Then I swept 3 boards (`occupancy` calm / typical / extreme) × 6 sizes (96×24, 96×30, 96×44, 96×60, 72×30, 72×24) = 18
renders, over all four combinations of *(what `need` charges)* × *(what `room` is)*:

```
charges          room passed         blank  shed/18
prof (+wrows)    h-4 (disk)              0   0/18     <- pre-change baseline, unpatched tree
prof + 0         h-4 (disk)              0   0/18     <- LLR-002.1 AS FIRST WRITTEN, against the real call site
prof + 0         h-2 (call site moved)    40  18/18   <- the artifact's 44/18 figure, reproduced
prof + 2         h-4 (disk)             28   0/18     <- AMENDMENT A-6, against the real call site
prof + 2         h-2 (call site moved)     0   0/18
```

Per-render detail for the amendment as written (`prof + 2`, real call site):

```
   calm      96x24  rows=24  blank=2  shed=False      typical   96x24  rows=24  blank=1
   calm      96x30  rows=30  blank=2  shed=False      typical   96x30  rows=30  blank=1
   calm      96x44  rows=44  blank=2  shed=False      typical   96x44  rows=44  blank=2
   calm      96x60  rows=60  blank=2  shed=False      typical   96x60  rows=60  blank=2
   calm      72x30  rows=30  blank=2  shed=False      extreme   96x24  rows=24  blank=1
   calm      72x24  rows=24  blank=2  shed=False      extreme   96x60  rows=60  blank=2
   => TOTAL blank rows = 28 ; renders shedding = 0/18
```

**Plainly:**

- The claimed **44 blank / 18-of-18 shed** for the as-first-written model is reproducible (I measure 40 / 18-of-18 on my
  size set) **only** under `room = h - 2` — i.e. only if `swimlane_plan`'s room argument is *also* changed. **Nothing in
  the artifact says to change it.** `LLR-002.2` changes only the return arity; `LLR-002.3`'s touched-symbol list names
  the `height or 24` sites but not the room expression; the §6.5 A-6 row states only the `need` formula.
- Against the tree as it actually is, **LLR-002.1 as first written was already correct**: 0 blank, 0 shed, 18/18,
  identical to the pre-change baseline.
- **The amendment is the defect.** Implemented as written, it pads **28 blank rows over 18 renders — 2 on every calm
  render, 1–2 on every other** — which fails C2 (*the view fills the height it is given and never pads*, a shipped law
  with a 0/18 pre-change baseline), fails `LLR-002.4`'s own `blank == 0` threshold, and fails §5.3's batch acceptance
  criterion.

🚨 **B-2 (blocker, NEW).** A-6 is correct **only** jointly with an unstated change to `swimlane_plan`'s `room`
argument. Either (i) withdraw A-6 and restore `need = prof + Σ(1 + min(titles,o)) + n_rest` — the disk-consistent form,
which is what the pre-change tree already does correctly — or (ii) keep `need = prof + 2 + …` **and** amend
`LLR-002.2` to require `swimlane_plan` to pass `room = h - 2`, with the two changes named as one atomic edit and the
0-blank sweep re-run. Option (i) is one deletion; option (ii) is two coupled edits to the batch's highest-risk symbol.
Either way, **`P-16`, `A-6`, `R-10` and the §6.5 mermaid diagram all state a defect that does not exist on this tree**,
and R-10's proposed `dev-flow-lessons` control — *"a cost model and the function that spends it must be reconciled by
execution"* — is a good control that was, ironically, not applied to the call site.

---

## 7. `LLR-002.6` — the `prof` budget ceiling under O-3

### 7.1 The 840/840 vs 0/808 check — **reproduces exactly, and inherits B-2**

Swept the retired law's own space extended as `LLR-002.6` specifies: `room ∈ range(4, 60)` × 8 `opens` shapes
(`[1], [2], [1,1,1], [2,2], [4,4,4,4], [8], [12,9,7], [2,2,2,2,2]`) × `n_rest ∈ {0, 2}` = **896 points** per geometry,
infeasible plans (`best_score[0] <= 0`) excluded by an explicit guard **and counted**:

```
=== LAW: feasible => prof <= room - 2 - sum(1+min(titles,o)) - n_rest ===
  need charges prof   (LLR-002.1 as first written) geo=96x30: violations 840/840 (infeasible skipped 56)
  need charges prof   (LLR-002.1 as first written) geo=96x44: violations 840/840 (infeasible skipped 56)
  need charges prof   (LLR-002.1 as first written) geo=72x24: violations 869/869 (infeasible skipped 27)
  need charges prof+2 (amendment A-6)              geo=96x30: violations   0/808 (infeasible skipped 88)
  need charges prof+2 (amendment A-6)              geo=96x44: violations   0/808 (infeasible skipped 88)
  need charges prof+2 (amendment A-6)              geo=72x24: violations   0/840 (infeasible skipped 56)
```

The artifact's figures are **exactly right** — 840/840, 0/808, 869/869, 0/840, and even the skip counts. But read them
against §6: the law is **red on the allocator that renders correctly** and **green on the one that pads 28 blank rows**.
The `- 2` in the bound is the same double subtraction as A-6. I swept the two neighbouring slacks:

```
=== slack 1: feasible => prof <= room - 1 - sum(1+min(titles,o)) - n_rest ===
  need charges prof  geo=96x30: 256/840   geo=96x44: 256/840   geo=72x24: 221/869
  need charges prof+2: 0/808, 0/808, 0/840
=== slack 0: feasible => prof <= room - 0 - sum(1+min(titles,o)) - n_rest ===
  need charges prof  geo=96x30:   0/840   geo=96x44:   0/840   geo=72x24:   0/869
  need charges prof+2: 0/808, 0/808, 0/840
```

**The tight, non-vacuous bound on the disk-consistent allocator is slack 0**:
`prof <= room - Σ(1 + min(titles, o)) - n_rest`. It is green on correct code and it still has teeth — it is violated by
any change that lets rung four outbid the lanes. 🚨 **B-3 (blocker, NEW):** as written, `LLR-002.6` is red on correct
code. It is one constant, and it is the same constant as B-2 — fix them together or neither.

### 7.2 The saturation claim — **qualitatively confirmed, absolute figures NOT reproduced**

Swept `project_wave(lead, geo, TODAY, prof)` on all three `LOADS` leads, `prof ∈ {1,2,3,4,6,8,10,12,16,24,32,52}`,
counting distinct non-zero column heights in the raster:

```
without carve_count (stack path)          p1 p2 p3 p4 p6 p8 p10 p12 p16 p24 p32 p52
  calm      2  2  2  2  2  2  2  2  2  2  2  2      lit 16 -> 764  (p3->p52: 17.4x)
  typical   3  5  5  5  5  5  5  5  5  5  5  5      lit 14 -> 705  (p3->p52: 17.6x)
  extreme   2  4  5  6  6  6  6  6  6  6  6  6      lit 68 -> 3327 (p3->p52: 18.0x)

with carve_count=True (the real lead_band path)
  calm     [2, 2, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3]
  typical  [3, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6]
  extreme  [2, 4, 7, 6, 7, 6, 7, 7, 7, 7, 7, 7]
```

**The claim holds in substance:** discriminable content maxes out at `prof = 2–4` and is unchanged through `prof = 52`
while lit dots grow ~17–18× (the artifact says 16×). **The stated absolutes do not reproduce:** the artifact reports
*"calm 5→5, typical 8→8, extreme 8→8"*; I measure `2/5/6` on the stack path and `3/6/7` on the lead's own
`carve_count=True` path. 🔵 **m-C (minor, NEW)** — the O-3 recommendation rests on the *shape*, which is confirmed, so
this does not move the ruling; but the three numbers are quoted in §6.3's recommendation and in the §Evidence
checklist's "executed at this iteration" list, and they are not what the tree produces.

### 7.3 The question the artifact did not ask — executed

*With no share cap, is there a board+size where the budget ceiling alone lets `prof` exceed the panel, or drives another
lane to zero rows?*

Swept 3 boards × 3 widths (72, 96, 130) × 9 heights (12, 16, 20, 24, 30, 44, 60, 80, 120) = **81 renders**, on the
disk-consistent allocator, measuring the **rendered band** (`prof + 2`, what `lead_band` actually emits) against the
panel, plus blank rows, the `+N not shown` note, and lanes drawn vs lanes in the model:

**Answer: no, on both counts — but the share curve is worse than the operator was shown.**

- **`prof` never exceeds the panel.** The band is bounded by the room by construction; `blank == 0` on 81/81 and
  `rows == h` on 81/81.
- **No lane is driven to zero rows by a fat bench.** The single lane loss in the sweep is `extreme 72×12`
  (7 of 8 lanes drawn) and it is the pre-existing block-loop shed **with the honest `+N not shown` note** — the
  lane is counted, not dropped in silence. Every other combination draws every lane.
- **But the share keeps climbing past where O-3 stops looking.** The measured band share on the calm fixture:

```
  calm  h=12: 58%   h=16: 62%   h=20: 70%   h=24: 75%   h=30: 80%
        h=44: 86%   h=60: 90%   h=80: 92%   h=120: 95%   (identical at w=72, 96, 130)
```

O-3's table stops at `h = 60` and quotes **87 %** (`prof/h = 52/60`). The figure the operator is actually accepting at
`h = 60` is **90 %** once the band's own head and tail rows are counted — `lead_band` renders `prof + 2` — and at
`h = 120` it is **95 %**, i.e. a two-project board showing one project and a single row. 🟠 **M-E (major, NEW):** the
O-3 ruling was requested on `prof/h`, but the thing on screen is `(prof + 2)/h`, and the curve was truncated at the
height where it still reads as tolerable. The recommendation may well survive a corrected table — this is not an
argument for a share cap — but **the operator should be asked again against `(prof+2)/h` out to `h = 120`**, because
O-3 is the one item in this batch the operator is being asked to accept as a permanent visual consequence.

---

## 8. O-4 — unruled by the operator. **Is the measured default safe to build on?**

**Yes for the mechanism; no for the signature — and the signature is the hard-to-reverse half.**

`LLR-004.2`'s specified default is: `render_swimlanes` reports whether it drew a disclosure row through an
**out-parameter of the same kind it already uses for `line_map`**, and the legend reads that answer. Assessed:

- **The mechanism is right and the reasoning is sound.** I verified the two facts it rests on. `selected_id is not None`
  is genuinely not a usable gate — `App._select_first` (`app.py:217–222`) runs at the top of every `refresh_view`. And
  re-deriving payability inside `legend_entries` would be a second copy of the shed logic, which `swimlane_plan`'s own
  docstring names as a known failure (`views.py:2113–2115`). The out-parameter keeps one source of truth. **This is the
  correct call and I would not reopen it.**
- **It is cheap to reverse *inside* the renderer.** An out-parameter is additive; if the answer turns out to be wrong,
  what it reports can change without touching any caller.
- **It is NOT cheap to reverse across the signatures.** `LLR-004.2` changes **four** signatures at once —
  `legend_entries`, `LegendModal.__init__`, `LegendModal.compose`, `App.action_legend` — across three files, against
  **17 reference lines / 8 call sites** in `tests/test_legend.py` and `tests/test_archive.py`. The keyword-with-`None`-
  default discipline keeps them all compiling, which is why the LLR is implementable; but if O-4 is later ruled the
  other way (reachability, D-4's rejected alternative), those four signatures come back out.

**Judgement: safe to build on, provided Phase 3 sequences it so the reversible part lands first.** Concretely — build
the renderer's answer and `TC-023` (the entry appears/disappears with the drawn row) **before** the four signature
changes, and keep the `LegendModal`/`App` half in its own increment. That way an O-4 reversal costs one increment, not
the batch. **The artifact does not say this**, and its §5.2 rolls `LLR-004.2` into a single `TC-024`. 🔵 **m-D (minor,
NEW):** name the increment boundary in `LLR-004.2`, or the "not blocked" claim is true only in the sense that Phase 3
can start — not in the sense that it can back out.

---

## 9. R-11 — `tests/test_span_economy.py`. **Deferral is ACCEPTABLE. The stated reason is wrong.**

I measured it rather than judging it. Two findings.

**(a) The file has no lanes run-count assertion to break.** Read end to end: its only run-count threshold is
`test_collapse_removes_the_redundant_runs`, and that is measured on the **gantt** at 120×40 (*"The gantt is the worst
offender, so it sets the bar"*), which this batch does not touch. Everything the file asserts about **swimlanes** is
the *equivalence* property — plain text **and** per-character style, markup vs `collapse_runs(markup)` — which is
invariant to how many cells a lanes row uses.

**(b) Executed under the simulated change** (wave removed from stacked rows + post-change allocator), swimlanes only,
3 sizes × selections `{None, first, middle}` × `show_archived` both ways:

```
   equivalence (text + per-char style) failures post-change: 0
   like-for-like, selected_id=None, swimlanes only:
     68x20 : raw spans   808 ->   808 ; after collapse_runs 112 -> 112
     120x40: raw spans  3635 ->  3528 ; after collapse_runs 211 -> 191
     200x60: raw spans 10012 ->  9988 ; after collapse_runs 251 -> 251 (…281 -> 251)
```

The run profile barely moves — a ~1–10 % *reduction* after collapse, not the "changes the run profile the file counts"
R-11 describes. **R-11's premise is wrong**: the ~114→~20 cell swap is not what could redden that file.

**What actually could**, and what `TC-004` should therefore watch: `LLR-001.2`'s A-13 composition rule is
*segment-per-character*, and the file's real hazard is **markup well-formedness under a new composition idiom** —
unbalanced tags, or `escape()` not being applied to the readout, would break `same_drawing()` on every view at once
(`test_escaped_brackets_are_not_tags` exists for exactly that reason). Deferring the *measurement* to `TC-004` is fine;
deferring it under the *wrong hypothesis* means Phase 3 will measure span counts, see them unchanged, and report the
risk discharged while the real hazard was never looked at. 🔵 **m-E (minor, NEW):** re-point R-11 at markup
well-formedness and `escape()`, keep the deferral.

---

## 10. The two corrections the iteration made to the reviews

### 10.1 `tests/test_prism_laws.py:147` falling 35 → 20 rather than collapsing — **direction right, numbers NOT reproduced**

Ran the law's own predicate on the law's own board at 120×44, counting rows carrying an identity-hued `FIELD_GLYPHS`
span, and separated the two ingredients of the change:

```
  pre-change (disk)                          rows= 35  spine-led= 27  mixed=0
  wave removed ONLY (allocator unchanged)    rows= 17  spine-led=  9  mixed=0
  wave removed + post-change allocator       rows= 30  spine-led=  9  mixed=0
  guard `assert per_row` still satisfied in both post-change variants: True
```

- **The pre-state 35 reproduces exactly.**
- **The correction of M-2 is CORRECT and I uphold it.** The law does **not** collapse to the lead alone: `_title_row`
  paints the phase glyph in `lane.hue` and those glyphs are in that file's `FIELD_GLYPHS`, so spine rows keep
  contributing (9 of them), and the `assert per_row` guard stays satisfied. The architect's mechanism is right.
- **The figure `35 → 20 (−43 %)` and `▎-led 27 → 12` do not reproduce.** I get **35 → 17** (wave removed only) or
  **35 → 30** (wave removed + post-change allocator), with spine-led **27 → 9** in both. Neither is 20/12.

🟠 **M-F (major, NEW).** `LLR-001.2` **rules** this figure — *"Ruled: the law is retained unchanged and this figure is
recorded as its post-change coverage"* — and §6.1 pins it as a verdict. A pinned figure that does not reproduce will
either fail in Phase 3 or, worse, be quietly re-derived to whatever comes out. And note *why* it is unstable: the
post-change count depends on `prof`, which depends on the cost model — **the very thing B-2 puts in dispute**. The
figure cannot be pinned before §6 is resolved. Recommend: state the post-change coverage as a **range with its
ingredient named** (17 without the bench growth, 30 with it), or defer the pin to Phase 3 with the measurement recipe.

### 10.2 The classifier counterexample being a title **ENDING** in braille — **CONFIRMED exactly**

Implemented §3.0.1's classifier verbatim and swept titles ending in `⣿` at every visible length, on a real render at
96×30 (`label_w = 15`):

```
  vis(title)  title                    verdict
          9  'xxxxxxx ⣿'               glyph (correct)
         10  'xxxxxxxx ⣿'              CURVE (fooled)
         11  'xxxxxxxxx ⣿'             CURVE (fooled)
         …   (fooled at every length 10..15)
  control: a title BEGINNING with braille
  vis= 5 / 12 / 15  -> glyph (correct) in 3 of 3
```

**The threshold is exactly `vis(title) >= 10` at `label_w = 15`, i.e. `label_w − 5`, and it is the LAST character.**
A title beginning with braille is never misclassified. A-18's correction of MIN-1 is right, its threshold is right, and
the mitigation it derives — `assert t.title.isascii()` over **every** fixture task rather than the first character —
is the correct guard. **Closed, no further action.**

---

## 11. Also verified clean (stated so the blockers read against a fair baseline)

| Check | Result |
|---|---|
| A-5's token pin closes `tests/test_palette_ration.py:276` | ✅ Read on disk: `assert marks["swimlanes"] == [(HEX["ink"], "!1")]` — **exact list equality** over `!`-prefixed marks. A `!2` readout would redden it; `f"{n} over"` does not. M-3 correctly closed. |
| `lead_band` renders `prof + 2` | ✅ Executed at `prof ∈ {4,10,24,33}` → 6/12/26/35. The half of P-16 that is true. |
| `LLR-003.5`'s correct path == the shipped path | ✅ 0 fidelity mismatches across 15 lanes — the `⣿` probe measured `project_wave`, not a re-implementation. |
| `.plain` selection-invariance (A-3's supporting measurement) | ✅ 6 of 6 identical; markup differs on 3 of 6. |
| Pre-change never-pads baseline | ✅ 0 blank rows, 0 shed over 18 renders on the unpatched tree — C2 confirmed independently, not carried. |
| `LLR-003.7`'s `Mirror` companion | ✅ 12 aligned full-height columns at dues `(1,2,3)` / project due `+14` — well clear of the 2-column knife edge. |

---

## 12. Findings summary

| id | Class | Finding |
|---|---|---|
| **B-1** | 🚨 blocker | `LLR-003.3` clause 7 observes the **bitmap**, not the drawn row. **82 of 448** payable (task, size) pairs draw a disclosure row with **zero** braille, on `tests/test_occupancy.py::fixture("typical")` at widths 24/25/31/32 — R6's failure mode through a door R6 does not watch. C5 + C6 both violated, and a named task is shed to pay for the blank stripe. |
| **B-2** | 🚨 blocker | **Amendment A-6 is inverted.** `swimlane_plan` already subtracts the lead band's 2 rows at the call site (`views.py:2126`). As written, `need = prof + 2 + …` pads **28 blank rows over 18 renders**; the as-first-written form renders **0 blank / 0 shed**, matching the pre-change baseline. The artifact's 44/18 figure requires an unstated change to `room`. |
| **B-3** | 🚨 blocker | `LLR-002.6`'s bound carries the same double subtraction: **red 840/840 on the allocator that renders correctly**, green only on the one that pads. The tight bound is `prof <= room - Σ(1 + min(titles,o)) - n_rest` (slack 0, **0/840**). |
| **M-A** | 🟠 major | `HLR-001`'s boundary catalog still routes all four entries to `AT-002`, whose canonical §3.0 subject is panel height/width exactness and asserts none of them. `AT-001`/`AT-020`/`AT-021` exist and are unused there. |
| **M-B** | 🟠 major | *"The two non-reddening lanes are exactly the two with `open == total`"* is false — only **one** such lane exists in the sweep; the second is `typical/Project 0` at **4/5**, where the mutation is simply invariant. |
| **M-C** | 🟠 major | `LLR-003.5`'s replacement predicate is a `shall` that **correct code violates at `open/total >= 0.875`** (7/8, 9/10, 15/16 all draw `⣿`). Same defect class as the one it replaced. |
| **M-D** | 🟠 major | `AT-024`'s (and `AT-001`'s) set-equality completeness half is **not evaluable at `h ≤ 24`**: the label clips to a non-unique prefix (`Projec…`), so it over-matches and goes green. What actually reddens is the `"not shown"` guard. |
| **M-E** | 🟠 major | O-3 was ruled on `prof/h` truncated at `h = 60` (87 %). The rendered band is `(prof + 2)/h` — **90 % at h=60, 95 % at h=120**. The operator accepted a number lower than the one on screen, on a curve that was cut short. |
| **M-F** | 🟠 major | `test_prism_laws.py:147`'s post-change coverage `35 → 20 (−43 %)` does **not** reproduce (I measure 35→17 or 35→30 depending on the cost model, spine-led 27→9). `LLR-001.2` **rules** and pins this figure, and it cannot be pinned before B-2 is resolved. |
| **m-A** | 🔵 minor | `01b-qa-validation-plan.md` carries no supersession header; its §10 exit set still names the retired ids. |
| **m-B** | 🔵 minor | `AT-003`'s *"every position of the lane"* has 3 dead positions of 6 on the repo lanes fixture (they are R4). State it. |
| **m-C** | 🔵 minor | P-18's absolute figures (*calm 5→5, typical 8→8, extreme 8→8*) do not reproduce (I measure 2/5/6, or 3/6/7 with `carve_count=True`). The saturation **shape** — max at prof 2–4, flat through 52, lit ×17–18 — is confirmed. |
| **m-D** | 🔵 minor | O-4's default is sound but changes **four** signatures across three files. Name the increment boundary so a reversal costs one increment, not the batch. |
| **m-E** | 🔵 minor | R-11's stated hazard (run-profile counts) is wrong — the file's only run-count assertion is on the **gantt**, and the measured swimlanes profile barely moves. Re-point it at markup well-formedness / `escape()`; keep the deferral. |

---

## 13. What must happen before the Phase-2 gate closes

| # | Owner | Action | Blocks |
|---|---|---|---|
| 1 | `architect` | Resolve the `room` accounting **once**: either withdraw A-6 (restore `need = prof + Σ(1 + min(titles,o)) + n_rest`) **or** keep it and amend `LLR-002.2` so `swimlane_plan` passes `room = h - 2`. Re-run the 18-render blank/shed sweep on whichever is chosen. Correct P-16, R-10 and the §6.5 diagram. | **B-2** |
| 2 | `architect` | Re-state `LLR-002.6`'s bound against the resolution of row 1 — slack 0 if A-6 is withdrawn. Re-run the 896-point sweep and paste the new violation counts. | **B-3** |
| 3 | `architect` | `LLR-003.3` clause 7 observes the **drawn row**, not the bitmap. Mirror it in R6, in `HLR-003`'s boundary catalog, in `AT-027` and in `AT-003`'s positive predicate. | **B-1** |
| 4 | `qa` + `architect` | Re-point `HLR-001`'s four boundary entries to `AT-001` / `AT-020` / `AT-021`. | M-A |
| 5 | `architect` | Scope `LLR-003.5`'s predicate to `round(4·open/total) < 4`, or restate it differentially; correct the "two non-reddening lanes" sentence. | M-B, M-C |
| 6 | `qa` | Make `"not shown"` the named completeness companion of `AT-024`/`AT-001`; scope the name-set comparison to `h ≥ 30` or specify clip-aware matching. | M-D |
| 7 | `architect` → operator | Re-ask O-3 against `(prof + 2)/h` out to `h = 120` (90 % @ 60, 95 % @ 120). The recommendation may stand; the number the operator accepted should be the number on screen. | M-E |
| 8 | `architect` | Un-pin `test_prism_laws.py:147`'s post-change figure until row 1 is resolved; record it as a range with its ingredient named. | M-F |
| 9 | `qa` | Fix m-A…m-E. | minors |

**Not raised, deliberately.** O-1, O-2 and O-5 are closed rulings and I do not reopen them — B-1 is not a reopening of
O-1, it is a defect in the predicate that implements it. P-1/P-2 remain correctly recorded as carried (R-5). R-6
(`report.py`'s known-false docstring) is correctly scoped out and carried to the post-mortem; I verified nothing in this
batch can break `_curve_svg`'s code path. The G/W/T waiver (§5.1) is honest and I agree with it for the same reason.

---

## Evidence checklist (`qa-reviewer`, Phase-2 re-review)

- [x] **Acceptance criteria use Given/When/Then** — ✗ **deliberately not**, and the artifact's §5.1 waiver is now
  explicit and honest (MIN-2 closed). These are differential render predicates; G/W/T would hide that the assertion
  compares two renders. Flagged, not silently reformatted.
- [x] **Test cases have explicit Expected, not vague "works"** — every finding names the compared quantity and the
  direction it must move (B-2: 28 blank vs 0; B-3: 840/840 vs 0/840; B-1: 82 of 448; M-C: `open/total >= 0.875`).
- [x] **Edge cases include empty, boundary, invalid, error** — zero-ink drawn row (B-1), `open/total` boundary at 0.875
  (M-C), label clipping at `h = 24` (M-D), narrow widths 24/25/31/32 (B-1), `h = 120` (M-E).
- [x] **Regression checklist exists** — §13's nine rows, each with an owner and the blocker it clears.
- [x] **Exit criteria stated** — the gate does not close until rows 1–3 land.
- [x] **No real PII / secrets** — every probe built synthetic `Project`/`Task` objects under `tempfile.mkdtemp()`.
  **No probe read the operator's real board.**
- [x] **Test results section left blank** — nothing here is reported as a test outcome. Every figure is a
  **measurement of the tree at `f237cb3`** (or of an in-memory simulation of the post-change tree, labelled as such),
  with the producing probe named.
- [x] **Layer B (black-box)** — B-1 is stated as what the reader sees on the drawn row; B-2 as blank rows in
  `render_view` output; M-D as what can be recovered from the render. B-1 exists *because* the requirement's predicate
  observes an object the reader does not.
- [x] **Bidirectional surface-reachability** — inputs (`selected_id`, width, height, board shape, `open/total` ratio,
  project due date) and outputs (disclosure row, blank rows, `+N not shown`, legend entry, lane label) were each traced
  to an observation method through the shipped `render_view` / `swimlane_plan` path. The two places the trace broke are
  B-1 (clause 7 observes the bitmap) and M-D (the label cannot be inverted to a name at `h ≤ 24`).
- [x] **No unfilled template** — no `<...>`, no `TC-NNN` stubs, no empty required rows.
- [x] **Nothing reconstructed from reasoning** — every number above was produced by an executed probe whose output is
  pasted. Where a figure in the artifact did **not** reproduce (P-18's 5/8/8; `test_prism_laws.py:147`'s 20/12), I state
  my measurement and say plainly that theirs did not reproduce, rather than reconciling them.
- [x] **Read-only** — `git status --short` over `taskboard/` and `tests/` is empty. The only file this review wrote is
  `.dev-flow/02-review-qa-iter2.md`.

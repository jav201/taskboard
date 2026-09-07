# Increment 55 — a confirm never covers the gate it names (ruling F)

**Batch:** `rework-5b`, opening increment · carries out **Ruling F** on
`PROTOTYPE-inheritors-2.md` §6 decision (F) / §5 **C3**, which `inc50.md` §4 came within one design
decision of and stopped at · also records **Ruling D (addendum)** and **Ruling E** verbatim, and writes
E into the kit and into the round
**Files:** `taskboard/language.py`, `prototypes/components/screens.py`,
`prototypes/components/fixture.py`, `tests/test_components.py`,
`prototypes/components/PROTOTYPE-inheritors-2.md` — **5 files** (4 source + the round's decisions
table), plus 2 regenerated frame artefacts and this packet.

**inc40 anchored solari's announcement at the head of the SCHEDULE and inc50 shrank it to its content,
and at both anchors it landed on `GATE BACKLOG 05` — the gate the confirm's own words name. `inc50.md`
§4 wrote down why an announcement at the schedule's head cannot avoid it (the gate header IS the
schedule's first row), named the three ways out as design decisions, and recorded that it was not
taking any of them. This takes the first: `Kit.overlay` gains an optional `about=` the SHEET fills
with `F.MODAL_ABOUT` — the column as DATA, so no kit parses the fixture's English — and
`Solari.band_head` places the band at the head of the first gate block the confirm does NOT name.
`GATE BACKLOG 05`, `AUDIT THE THEME TOKENS` and `DROP THE LEGACY SHIM` are on the frame while the
question is asked, and so are five rows of the detail pane that were under the band before. The cost
is declared and not buried: inc50's clause 2 changes ends, and the row under the band is a departure's
orphan seam again. Frames: `solari_S4` only. Suite 1083 → 1086.**

---

## 0. Rulings (orchestrator, 2026-09-06, on the operator's delegation)

Recorded verbatim, all three, because a ruling that lives only in a chat is a ruling nobody can argue
with later. Only **F** is implemented in this increment; **D (addendum)** and **E** are recorded, and
E's second half — *write it down at the seat* — is done here.

> **D, addendum.** Ruling D governs two *different meanings* that share a shape. A ladder is one
> meaning at monotone intensities and is one declaration: industrial's severity `▫▫ ▪▪ ■■` passes from
> hollow to filled (weight) and grows (size) in the same direction, so it stands. Swiss's button ladder
> `▫ ▪ ■` likewise. Rotation counts as a channel when it is direction the language already spends
> (opener/closer, up/down), not otherwise.

> **E.** For darkside the SVG is the artefact of record, not the txt; a darkside frame's grey step is a
> real signal. `darkside_S1` is not reworked on the txt's evidence. Write it into
> `MODAL_BORDER_REFUSED`'s neighbour comment or the kit docstring, and into
> `PROTOTYPE-inheritors-2.md`'s decisions section as "ruled".

> **swiss vs darkside resolved in opposite directions in inc52**: accepted as is; the earlier
> declaration in each kit won, and both kits say so.

> **inc55 · Ruling F: a confirm never covers the gate it names.** `solari_S4`'s band sits at the head
> of the schedule and covers `GATE BACKLOG 05`, the gate the confirm names. Rule: the band is placed at
> the head of the first gate block the confirm does NOT name; if every gate is named or the page has
> one gate, the band goes to the foot of the schedule (above the plate's closing seam, if any).
> Implement in `Solari.overlay_instead` by reading the gate the modal text names (the sheet passes the
> title; find a way that does not parse prose: give `overlay` an optional `about=` argument the sheet
> fills, falling back to the head when absent, and let every other language ignore it). Law: while the
> band is up, the named gate's header row and its task rows are byte-identical to the page's at their
> own index; inc50's contiguity and head laws still hold. Teeth as usual. Frames changed: `solari_S4`
> only; explain any other.

### 0a. Where D's addendum and E landed, and what each cost

**D's addendum needed no code and got none.** It ratifies two ladders `inc53.md` §12 flagged as the
sharpest thing that batch left open — industrial's `▫▫ ▪▪ ■■` and swiss's `▫ ▪ ■` — and its argument
(*"a ladder is one meaning at monotone intensities and is one declaration"*) is the census's existing
`DANGER_IS_THE_TOP_RUNG` reasoning applied one level up. **The census's `HOMOGLYPHS` table already
implements it correctly**: the check is ASYMMETRIC (one side a meaning, one side chrome, `inc53.md`
§2), so two rungs of one ladder can never produce a row. `▪ ■` is in the table and scores zero, which
is the addendum's own prediction. No line moved and none was needed; recorded so the next reader does
not go looking for the fix.

**The rotation half of D is now answered too** — *"rotation counts as a channel when it is direction
the language already spends"* — which is what inc49 refused a homoglyph move on and what
`spec.md` §13.7 listed as *"that half of D is still open"*. It closes without a code change for the
same reason: `DIRECTION` was already one of the four channels `collision_census.py`'s header names,
and industrial's `▪ → ▶` is already listed there as spending it.

**E is written at the seat.** `Darkside.pane_split_instead`'s docstring — the method that draws the
grey step and the one place that already said *"a background is not a cell"* — now carries the ruling
in full, and `PROTOTYPE-inheritors-2.md` §6 E is marked **RULED**. What E does NOT close is written
with it: the rail's fourteen strokes elsewhere on `darkside_S1` (inc48 held `▏` at 16 and took `▬` 6 →
0) and **E2**, the `.svg` carrying no font metric.

---

## 1. What was there, and why inc50 could not fix it

`solari_S4` before this increment, rows 3–14 (0-based), against `solari_S1` at the same indices:

```
 3 |                                       <- the band's bar
 4 | Delete 3 tasks?                          THE PAGE'S ROW 3 IS:
 5 | 3 tasks will be removed from BACKLOG.      GATE BACKLOG 05   STATUS  PROJ  PRI
 6 | This cannot be undone.                     21  AUDIT THE THEME TOKENS   ON TIME  LOW
 7 | ▔  ▀Delete▄  ▔   ▁   Cancel   ▁            30  DROP THE LEGACY SHIM     ON TIME  NORM
 8 | ▁▁▁▁▁ (the band's closing seam)
 9 | ▼  GATE DOING 04  ...                   <- the schedule resumed on a HEADER (inc50 clause 2)
```

**The confirm said "3 tasks will be removed from BACKLOG" and BACKLOG was the one thing under the
band.** inc40 moved the band off the station's plate; inc50 shrank it from eight rows to six so the
schedule resumed on a gate header instead of an orphan seam. Neither could move it OFF the named gate,
because both anchored on `schedule_head` — *the row after the board's head seam* — and on this page
that row is `GATE BACKLOG 05`. `inc50.md` §4 states it in those words and names the three ways out:
place the band below the first gate, insert instead of overlay, or let the announcement name a gate it
does not cover. **The first is the only one that is still an overlay and still honest, and it is what
ruling F orders.**

## 2. The mechanism, in three seats and no more

**(a) The fixture states the fact as data.** `prototypes/components/fixture.py`:

```python
MODAL_ABOUT = COLUMNS[0][0]
```

read off `COLUMNS` rather than typed, so a fixture that renames its first column cannot leave the
sentence and the datum disagreeing. **The ruling's own warning is the reason this exists**: the gate is
already in `MODAL_BODY` as English, and a kit that had to learn it from there would be eleven parsers
of one fixture's wording.

**(b) The sheet hands it over.** `screens.s4` and `screens.s4_blueprint` call
`k.overlay(rows, W, H, under, about=F.MODAL_ABOUT)`. `screens.py` is the one place that knows both the
words and the board behind them, which is what makes it the place that can say this without a kit
reading prose.

**(c) `Kit.overlay` carries it and ten languages ignore it.** The signature grows
`about: str | None = None` on `overlay`, `overlay_box` and `overlay_instead`, and on all seven
subclass overrides of `overlay_instead`. **One signature for both branches, deliberately**: a lid is
centred and cannot be moved by what the question is about, so `overlay_box` accepts and ignores it —
and a language added later that overrides either branch cannot be handed an argument it did not
declare, which is the loud failure this file prefers to a silent `**kw`.

**(d) `Solari` places the band.** Three small methods, each read off the page rather than counted:

```python
def gate_of(self, row):        # ` GATE {NAME} {NN} ` -- this kit's own head() format
def schedule_foot(self, under, depth)   # the fallback: above a closing seam, if any
def band_head(self, under, depth, about=None)
```

`band_head` walks the gates the page declares and returns the index of the first header whose name is
not `about`; every gate named (or one gate) falls to `schedule_foot`; `about=None` falls to
`schedule_head`, which is inc40's answer and is what keeps every existing caller and every other
language byte-identical.

**`gate_of` locates the word `GATE` rather than assuming it is first**, and that is not defensive
coding — it is the one row the method must not miss. A gate the cursor stands in carries `CUR` in the
gutter (`▼  GATE DOING 04`), so `parts[0]` is the flap indicator on exactly the gate the operator is
looking at.

## 3. The law

> **A confirm never covers the gate it names.** While the band is up, the named gate's HEADER ROW and
> every row of its BLOCK are byte-identical to the page's at their own index, and no index of that
> block is in the band.

`test_a_solari_confirm_never_covers_the_gate_it_names`, and it is asked **twice**:

1. **Off the shipped frame.** `solari_S4.txt` against `solari_S1.txt`, with the named gate's whole
   block asserted intact.
2. **Of the mechanism, once per gate on the page.** `k.overlay(..., about=gate)` for all four gates in
   turn, each asserting that gate's block survived. **This is what stops clause 1 being a lucky
   fixture**: a placement that happened to miss BACKLOG while eating whichever gate it was pointed at
   passes the first reading and fails the second.

**THE GATE'S NAME IS INTERSECTED, NOT PARSED.** `tests/test_components.py` does not import the
prototype fixture (its header says why), and a regex over *"removed from BACKLOG"* would make the law
a reader of one sentence's English. The gates the PAGE declares are a set; the words the BAND says are
a string; the named gate is the one member of the first that appears in the second, and **there is
asserted to be exactly one**. A fixture that renamed its columns moves both halves together.

**A BLOCK AND NOT A HEADER**, because leaving `GATE BACKLOG 05` on the frame and taking the two
flights under it would still have hidden what the confirm is about. `gate_blocks()` reads the header
and everything down to the row before the next header.

### 3a. inc50's clause 2 changed ends, and that is the cost of the ruling

`test_solaris_band_is_its_content_and_the_board_under_it_opens_on_a_gate` is renamed
`test_solaris_band_is_its_content_and_stands_at_a_gates_head`, and its middle clause is now:

```
inc50 clause 2   the row immediately BELOW the band is a gate header
inc55 clause 2   the row the band STARTS on is a gate header
```

**Both are the same sentence read from opposite ends** — *a band takes a gate's head, not the middle
of one*. inc50 could only assert the foot, because the band stood at the schedule's head, where the
head is the plate's business and not a gate's. Ruling F makes the head assertable and **puts the foot
inside the gate the band moved onto**: the band is six rows, `GATE DOING 04`'s block is ten, so the
row under the band is `PORT THE CSV IMPORTER`'s seam and two departures stand under a header that is
gone. **That is the orphan seam inc50 removed, moved down the page.** It is stated in the test's
docstring, in `Solari.overlay_instead`, in the round's §6 F, and again in §6 below. Clauses 1 and 3
are inc50's word for word.

`solari_s4_rows()` — the teeth helper that rebuilds the words `screens.s4` hands over — sliced `[4:8]`,
which was the band's seat while the band stood at the schedule's head. It now finds the band with
`modal_band` and asserts it got four rows. **A hard-coded slice would have gone on returning four rows
of BOARD without failing.**

## 4. Teeth

**`test_the_bands_old_anchor_ate_the_gate_the_confirm_names`** — `band_head` monkeypatched back to
`schedule_head`, which IS the inc50 body, and the arm names the gate and both of its departures:

```python
assert any("GATE BACKLOG 05" in r for r in eaten), eaten
assert any("AUDIT THE THEME TOKENS" in r for r in eaten), eaten
assert any("DROP THE LEGACY SHIM" in r for r in eaten), eaten
```

and a third arm asserts the documented default rather than trusting it: with no `about`, the band is
inc50's, at the schedule's head.

**`test_a_page_whose_every_gate_is_named_puts_the_band_at_the_foot`** — the fallback **no frame in this
repo reaches**, exercised on a synthetic one-gate page: `band_head(under, 6, "BACKLOG")` returns the
foot, `band_head(under, 6, "DOING")` returns the gate, `band_head(under, 6, None)` returns
`schedule_head`, and the composed page keeps its closing seam and its plate. Said out loud in the
method's own docstring too, so nobody discovers later that the fallback was never run.

**AND THE LAW WAS WATCHED FAIL BY HAND ON THE REAL DECLARATION.** `y = self.band_head(...)` reverted to
`y = self.schedule_head(under)`, `render.py` re-run, the law run against the frame that produced:

```
$ python -X utf8 -m pytest tests/test_components.py -q -k "never_covers or stands_at_a_gates_head"
>           assert s4[i].rstrip() == s1[i].rstrip(), (named[0], i, s4[i], s1[i])
E           AssertionError: ('BACKLOG', 3, '                              ',
E                            '   GATE BACKLOG 05   STATUS    PROJ    PRI   DETAIL  FIX LOGIN REDIRECT')
E           -    GATE BACKLOG 05              STATUS    PROJ          PRI     DETAIL  FIX LOGIN REDIRECT
1 failed, 1 passed, 729 deselected in 0.49s
```

**It names the language's gate, the row index, and the row that should have been there.** The
renamed clause-2 law passed under the same revert — which is the point of writing the new law at all,
and is recorded rather than glossed: clause 2 in either form does not catch ruling F's violation.
`language.py` was restored from a byte copy taken before the edit and `render.py` re-run.

## 5. Frames changed — `solari_S4` only

```
 M prototypes/components/solari_S4.svg
 M prototypes/components/solari_S4.txt
```

```
row   before                                          after
 3    (the band's bar)                                    GATE BACKLOG 05   STATUS  PROJ  PRI   DETAIL …
 4    Delete 3 tasks?                                      21  AUDIT THE THEME TOKENS    ON TIME  LOW
 5    3 tasks will be removed from BACKLOG.                ▁▁▁▁▁ …   PROJECT ▁▁▁▁ Web
 6    This cannot be undone.                               30  DROP THE LEGACY SHIM      ON TIME  NORM
 7    ▔  ▀Delete▄  ▔   ▁   Cancel   ▁                      ▁▁▁▁▁ …   DUE ▁▁▁▁ 3d
 8    ▁▁▁▁▁ (closing seam)                                           PRIORITY ▁▁▁▁ high
 9    ▼  GATE DOING 04 …  STATUS ▁▁▁▁ open              (the band's bar)
10    ▼   03  FIX LOGIN REDIRECT …  OWNER ▁▁▁▁ jav201   Delete 3 tasks?
11        ▁▁▁▁▁                                        3 tasks will be removed from BACKLOG.
12        02  RATE-LIMIT THE API …  DONE 007 OF 016     This cannot be undone.
13        ▁▁▁▁▁                                        ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
14        09  PORT THE CSV IMPORTER   ON TIME  NORM     ▁▁▁▁▁ (closing seam)
```

**The gate the confirm is about is on the frame, with both of its departures and both of their seams.**
So are five rows of the detail pane that the band used to cover — `DETAIL FIX LOGIN REDIRECT`,
`PROJECT Web`, `PHASE doing`, `DUE 3d`, `PRIORITY high` — which is a second answer the round could not
get from the old frame and is worth naming: the band moved onto rows whose right-hand side is the
detail pane's `STATUS`, `OWNER` and `DONE`, so **three detail rows were traded for five.** Ink 26.8% →
**29.4%**.

**Gallery: 0 of the 22.** `overlay_instead` is not on the board path — the same reason inc50 gave.
**Census: 33 → 33, homoglyph rows 4 → 4** — no declaration changed; this is a composition increment.
**Of the eight gallery frames installed in the skill, none moved**: `solari_S4` is not one of them,
and `47_solari-list-gate-seam`'s source is `solari_S1`.

## 6. Risks, and the one that is a real regression

- **THE ORPHAN SEAM IS BACK, ONE GATE LOWER.** The band's foot lands inside `GATE DOING 04`'s block,
  so row 15 is `PORT THE CSV IMPORTER`'s seam and rows 16–17 are `REWRITE THE ONBOARDING` and its seam,
  under a header the band covers. **This is exactly the defect inc50 removed**, moved from the top of
  the schedule to the middle of it. It is not hidden anywhere: the ruling's rule fixes the band's HEAD,
  the band's depth is inc50's law, and six does not divide ten. **The operator's one-line alternatives
  are (i) take the foot placement always (`schedule_foot`, already implemented and tested), or (ii)
  let the band take whole gate blocks, which revokes inc50 clause 1.** Neither is taken here.
- **The band is now lower on the page than the mode strip suggests.** A question at row 9 rather than
  row 3 is further from where a reader's eye starts on a departure board. The defence is that the
  subject of the question is now above it; the objection is available and it is a design call.
- **`about` is a string the caller must get right.** A caller that passes a gate name the page does not
  declare gets inc40's anchor (the first header that is not that name — the head), which is a silent
  fallback rather than an error. It is the same shape as `schedule_head`'s "a page with no seam has no
  plate to protect", and it is named here rather than defended.
- **`gate_of` reads the page.** A task whose title contained the word `GATE` followed by a name and two
  digits would be read as a header. The fixture has none; the risk is real and is the same class as
  `schedule_head`'s full-measure-seam scan, which has stood since inc40.

## 7. Found by looking, not fixed

- **The other ten languages cannot be asked ruling F's question at all**, and that is why the law is
  scoped to solari by name rather than parametrised over eleven with ten vacuous passes. A box is
  centred and covers a RECTANGLE; "does it cover the gate it names" is only answerable for a language
  that posts its question ACROSS the page. `MODAL_BORDER_REFUSED` is the registry that tells the two
  apart, and solari is the only one of its seven members whose board has gates.
- **The renamed clause 2 passes under the reverted body** (§4). Two laws that look like they cover the
  same ground cover different halves of it, and only the intersection test proves which.
- **`solari_S4`'s ink went UP again while the band moved** (26.8% → 29.4%), for the third increment
  running. inc50 §9 said density on this language measures board coverage; this is the same reading
  with the sign the other way, and it is now a habit rather than an observation.
- **`test_win_clipboard_roundtrip` was GREEN in every run of this increment**, including the baseline
  at `5d6bfbe`. It is environment-coupled (spec §10.6, §13.8) and moved in both directions during
  `rework-5a`. **Reported, not counted, not touched — `1086 passed` is not evidence that it is fixed.**

## 8. Gates, verbatim

```
$ python -X utf8 -m pytest -q                                              exit 0
1086 passed, 2 skipped, 4 warnings in 43.58s          (baseline 1083 at 5d6bfbe)

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

**`1083 → 1086`:** the ruling-F law, its teeth, and the foot fallback.

## 9. Pending — not this increment

- **inc56 — ruling G**, the S2 fixture's alert-mood item.
- **inc57 — the hygiene the rounds named**: darkside's `(O)` outside `PART_GLYPHS`, the `LEVELS`
  comment citing a `CUR` that moved in inc45, `capture_languages.py`'s stepper claim, and the eleven
  `field_row` leaders the census cannot reach.
- **Decision A** (corgi, prism, blueprint never judged) and **K2**, **K4**, **L1–L6**, **C2**, **C4**–
  **C7**, **E2**, **E3** are untouched.

## 10. Suggested next task

**inc56 — ruling G: the S2 fixture carries one alert-mood item for all eleven.**

---

## Evidence checklist

- [x] **Tests/type checks/lint pass.** `1086 passed, 2 skipped` (baseline 1083), **no red at all this
      increment**; `test_win_clipboard_roundtrip` green in every run and named anyway (§7).
      `verify_language.py` ALL PASSED exit 0. `render.py` 66/330/0. `matrix.py` 66 of 66, refusals `[]`.
      `capture_languages.py` 22 captures, 0 moved. `collision_census.py` both self-checks green,
      33 → 33, homoglyphs 4 → 4.
- [x] **No secrets in code or output** — three kit methods, one signature widened in eleven places, one
      fixture constant, two call sites, four tests. No network, no new dependency, no path outside the
      worktree.
- [x] **No destructive commands run without approval** — none. No checkout, no reset, no delete, no
      force, no process killed. The watch-it-fail experiment used a byte copy of `language.py`
      (`prototypes/out/_b55_lang.bak`) and restored from it; `git status` confirms the tree.
- [x] **File count within cap** — **5**: `taskboard/language.py`, `prototypes/components/screens.py`,
      `prototypes/components/fixture.py`, `tests/test_components.py`, and
      `prototypes/components/PROTOTYPE-inheritors-2.md` (ruling E's second half, which the ruling asked
      for by name). The 2 frame artefacts are written by `render.py`.
- [x] **Review packet attached** — this document.

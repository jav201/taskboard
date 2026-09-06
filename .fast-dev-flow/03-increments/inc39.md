# Increment 39 — `INVALID` by orientation: one base defect, inherited four times

**Batch:** `rework-1` · `PROTOTYPE-inheritors.md` §2.4(b), §7 q1 and q7 — the round's own structural finding
**Files:** `taskboard/language.py`, `tests/test_components.py` — **2 source files.**

**Four of the eleven spelled "this value was rejected" by EXCHANGING the two walls of the field and by
nothing else: `nord_S2` drew `]12/09/26   [`, `instrument_S2` `⠸…⠇`, `industrial_S2` `▌…▐`, `blueprint_S2`
`┤…├`. nord declares no `PART_GLYPHS` at all, so its flip was `Kit`'s own — which is what moves this from
four arguable design decisions to one base answer that three other languages copied. All four are fixed at
the declaration seat; the law is written once, over all eleven, at three widths, and it goes red on exactly
those four when the old declarations are put back.**

---

## 1. What the round claimed, and what looking actually found

§2.4(b) says the defect is `Kit`'s because *"nord no override nada de esto"*, and infers that fixing `Kit`
fixes the four. §5.8 of the same document flags that inference as **an inference and not a measurement**
(*"hay que rendirla antes de creerla"*). It is rendered here, and **the round is right about the
attribution and wrong about the arithmetic**:

```
language     owns PART_GLYPHS?   keys    textfield.main DEFAULT / INVALID
nord              NO             (Kit)   [ ]   /   ] [        <- Kit's own line
instrument        YES             14     ⠇⠒⠸  /   ⠸⠶⠇
industrial        YES             14     ▐·▌  /   ▌/▐
blueprint         YES             14     ├·┤  /   ┤·├
```

Ten of the eleven declare a full 14-key table of their own. So **`Kit`'s line is the origin, not the shared
object**: patching `Kit` alone moves `nord_S2` and nothing else. That is asserted, not assumed — the teeth
test's nord arm patches `Kit` and requires the other ten to stay green (§4).

The seven that were already right did not get there by keeping DEFAULT's walls. They changed the wall's
**form**:

```
naught ◑·◑    corgi ▄▀·▀▄    swiss ╲ ╱    darkside Ø Ø    prism ⣹⠀⣏    ledger ‡·‡    solari ═·═
```

That is the correct answer and it had to survive the law, which is why the law is not "INVALID keeps
DEFAULT's walls".

---

## 2. Why orientation is not a channel here

Context of use: the operator has filled the form and is looking for the field that is blocking `Save`.
The observable criterion is the round's — **cover the error line and point at the invalid field reading
only the walls.** The two marks sit at opposite ends of a 34-cell row, so answering it means holding a
convention in memory and comparing both ends of the row against it. There is no local cue: at the left
edge alone, `]` and `[` are equally plausible openings.

nord is the sharpest case and its own doctrine says why. Nord exists to inherit the terminal's
conventions; `] [` **is not a terminal convention of any kind**, so the one language defined by being
unsurprising had the most surprising field chrome of the seven in the round.

---

## 3. The mechanism, and the one rule that produced all four answers

The seat is `Kit.field_form` — *"an ODD string: wall, RUNE, wall"*, split `g[:h], g[h], g[h+1:]`. Nothing
in the composition layer needed to change: **the strings were wrong, not the split.**

The rule applied, stated so it can be argued with:

> **Restore the language's declared handedness. Where un-flipping alone would collide byte-for-byte with
> another state, the walls take that language's own `DANGER_FORM` — the seat swiss (`╲ ╱`) and darkside
> (`Ø Ø`) already spend theirs on, and which darkside's kit already names *"its own INVALID wall"*.**

| language | before | after | which arm, and why |
|---|---|---|---|
| instrument | `⠸⠶⠇` | `⠇⠶⠸` | un-flip only. The full-dot paper `⠶` was already a channel and is now the only one. No collision. |
| industrial | `▌/▐` | `▐/▌` | un-flip only. The plate's ink faces the content again — *"the ink looks at the content"* is what makes a plate read as a plate — and the hatch `/` carries the state, exactly where this table already puts `·`, `_`, `-` and `#`. |
| nord (`Kit`) | `] [` | `! !` | un-flipping gives `[ ]` = DEFAULT byte for byte, so the walls take `DANGER_FORM`: the terminal's own shout. |
| blueprint | `┤·├` | `━·━` | un-flipping gives `├·┤` = DEFAULT byte for byte, so the terminators take `DANGER_FORM`: the heavy rule, which is this language's `LEVELS["error"]` and the ladder S5 already reads. |

Both `DANGER_FORM` answers land the field's walls in the same family as the error line directly beneath
it, which is a gain the minimal fix did not have to buy:

```
nord        due*          !12/09/26                          !
                          !! expected YYYY-MM-DD

blueprint   due├          ━12/09/26··························━
                          ━━ expected YYYY-MM-DD
```

---

## 4. The law, and what it can and cannot bite

`tests/test_components.py`, three tests.

**The law** — `test_an_invalid_field_is_not_a_field_with_its_walls_exchanged`, parametrized over all
eleven. It derives each language's opening and closing vocabularies from its **five other** field states
and asserts:

```python
assert op not in (closes - opens)
assert cl not in (opens - closes)
```

*The invalid opening mark may not be one this language uses ONLY to close, and the closing mark may not be
one it uses ONLY to open.* A new form passes; a turned pair does not. Then, at **three widths** — `w=1`
(no room for anything but the walls), `w=12` (this file's default), `w=34` (what `screens.py` gives S2's
`due` field, the frame the defect was read off) — the rendered field is asserted to open with `op` and
close with `cl`, because `field_form` is width-free but the render is not and the render is the artefact.

**The vacuity seat** — `test_the_field_law_can_only_bite_where_the_walls_have_a_hand`. Six of the eleven
give a field the SAME mark on both sides in every state (corgi `▁▁ ▁▁`, darkside `▬ ▬`, solari's seam), so
they have no handedness to violate and the law is vacuously true there. The handed roster is **derived**
and compared against a written one:

```python
HANDED_FIELDS = ("instrument", "industrial", "nord", "ledger", "blueprint")
```

so "eleven passed" is not mistaken for "eleven were asked", and a language that later gives its field a
left mark and a right mark joins the set where somebody has to look at it.

**The teeth** — `test_exchanging_the_field_walls_back_makes_the_law_go_red`. One arm per language, each
restoring its pre-inc39 string byte for byte from a constant that lives in the test. Each arm asserts the
law goes red **and that the other ten stay green under the same patch** — which is the half that proves
the four are four independent declarations, and the half that says something real about nord, whose arm
patches `Kit` itself.

### The exemption, named rather than left silent

**Blueprint's `radio.main` turns its terminators on purpose and the kit says so**, so the same law over
`radio.main` would be red on doctrine:

> `"radio.main": {DEFAULT: "┤ ├", …}` — *"THE DATUM TURNED INWARD. The checkbox's terminators point out
> (a dimension measured across a gap); the radio's point IN, which on a drawing is a callout selecting one
> item from a schedule."*

That is a **declared** use of orientation as a channel *between two components*, with a citation. This
increment scopes the law to the field and does not extend it there. `PROTOTYPE-inheritors.md` §2.7 reads
blueprint's radio/checkbox pair as a defect; **on the evidence in the kit it is doctrine, and it is left
alone.** Question 7 of §7 (*"¿Se prohíbe la orientación como único canal de estado?"*) is still the
operator's, and answering it yes would have to answer blueprint's radio too.

---

## 5. Teeth, run

The four INVALID strings reverted in `taskboard/language.py`, the law run alone:

```
4 failed, 7 passed, 590 deselected in 0.67s

E       assert '⠸' not in ({'⠄', '⠸', '⠼', '⣸'} - {'⠄', '⠇', '⠧', '⣇'})     instrument
E       assert '▌' not in ({')', '▌'} - {'(', '▐'})                          industrial
E       assert ']' not in ({']', '╌', '▌', '▓'} - {'[', '╌', '▐', '▓'})      nord
E       assert '┤' not in ({'┤', '┫', '╎', '╡'} - {'├', '┣', '╎', '╞'})      blueprint
```

**Exactly the four, named by the exact glyph; the other seven stayed green.** Fix restored, re-run green.

---

## 6. Frames changed

Eight files, and no others — `git status --short prototypes/components/` after `render.py`:

```
 M prototypes/components/blueprint_S2.svg      M prototypes/components/blueprint_S2.txt
 M prototypes/components/industrial_S2.svg     M prototypes/components/industrial_S2.txt
 M prototypes/components/instrument_S2.svg     M prototypes/components/instrument_S2.txt
 M prototypes/components/nord_S2.svg           M prototypes/components/nord_S2.txt
```

`8 files changed, 12 insertions(+), 12 deletions(-)` — **one row per `.txt`, two `<text>` runs per `.svg`.**
S2 is the only screen that renders an INVALID field (`screens.py` line 348, the only `INVALID` call site in
the sweep), which is why nothing else moved.

```
before   due*          ]12/09/26                          [
after    due*          !12/09/26                          !

before   due⠁          ⠸12/09/26⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠇
after    due⠁          ⠇12/09/26⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠸

before   due▐          ▌12/09/26//////////////////////////▐
after    due▐          ▐12/09/26//////////////////////////▌

before   due├          ┤12/09/26··························├
after    due├          ━12/09/26··························━
```

The `.svg` followed the `.txt` at the same seat, which is the check that the exporter is not a second
opinion:

```
-<text x="144.4" y="108.3" fill="#4c566a">]</text>
+<text x="144.4" y="108.3" fill="#4c566a">!</text>
```

---

## 7. Gates, verbatim

```
$ python -X utf8 -m pytest -q
955 passed, 2 skipped, 4 warnings in 33.41s
```
(baseline 942 + 13: eleven parametrized law cases, the vacuity seat, the teeth.)

```
$ python -X utf8 prototypes/verify_language.py                                   exit 0
  [PASS] sweep: ... and every `# nth-exempt:` claim is USED — an exemption no hit sits under is an
         exemption widened past its evidence  2 claimed, 0 unused

== THE GATE ITSELF: settle headroom
  [PASS] settle() keeps headroom under its bound (a gate near its limit is a gate about to rot)
         worst 4 of 40 over 155 captures

ALL PASSED
```

```
$ python -X utf8 prototypes/components/render.py                                 exit 0
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
```

```
$ python -X utf8 prototypes/components/matrix.py                                 exit 0
11 rows x 6 screens, every cell `implementa -`
--- per screen: which primitive is missing in how many languages ---
S1:   S2:   S3:   S4:   S5:   S6:            (all empty)
--- refusals, by language ---
naught [] corgi [] instrument [] swiss [] industrial [] nord []
darkside [] prism [] ledger [] solari [] blueprint []
```

`capture_languages.py` was **not** run: no kit's board rendering changed. The only declaration touched is
`textfield.main[INVALID]`, and the board draws no invalid field — the eleven `gallery_*` and `board_*`
artefacts are untouched on disk.

---

## 8. Risks

- **`!` now carries a third meaning in nord.** It was `LEVELS["warn"]` in the log and `DANGER_FORM` on the
  destructive button; it is now also the invalid field's wall. The round already logged the first
  collision (§2.4 `nord_S5`: *"el entorno no arregla el defecto: lo blanquea"*) as evidence against `Kit`.
  This increment **does not reduce that overload and arguably widens it** — the defence is that all three
  uses are one claim ("something here is wrong") and that darkside's `Ø` sets exactly this precedent with
  a citation. If the operator answers §7 q5 by forbidding cell reuse across registers, this line is one of
  the ones that has to move.
- **`━` now carries a fifth meaning in blueprint** — sparkline peak, log error rung, destructive-button
  bracket, `LEVELS["error"]`, and now the invalid field's terminators. Same defence (one claim, one
  weight), same exposure to §7 q5.
- **industrial's and instrument's invalid channel is now the PAPER alone.** With the walls un-flipped,
  `▐/▌` differs from `▐·▌` only in the rune, so a value that fills every cell of the field would show the
  same walls as a good one. That is already true of those languages' FOCUSED / EDITED / ACTIVE states, so
  it is their declared idiom rather than a regression — but swiss's own kit argues the opposite position
  in a comment (*"a value may fill every cell, so a walled-off field is the only place a full one can say
  DISABLED without colour"*), and the two positions have never been reconciled.
- **The law is scoped to `textfield` and can be walked around.** `stepper.step` carries `INVALID: "]["` in
  `Kit` — the same turn, on a component whose halves are *directions* rather than walls (§9). The law does
  not reach it and was not extended to it.
- **The four moved frames have not been judged.** No round, no operator verdict — same standing as the 36
  frames inc37 shipped and the four inc38 moved.

## 9. Pending — found by looking, not fixed

- **`prototypes/out/_b37_test.py` makes `pytest -q` MUTATE THE SUITE.** The filename matches pytest's
  default `python_files = test_*.py *_test.py`, so bare `pytest` from the repo root **collects it and
  runs its module body**, which appends the inc37 block to `tests/test_components.py`. HEAD already
  carries **three** copies of `FRAMES` and of the three inc37 tests — three prior gate runs. The count
  stays 942 because the duplicate `def`s shadow each other, so it has never gone red. inc38 §7 recorded
  the *symptom* ("defined twice"); this is the cause. It was neutralised by hand for every commit in this
  batch (snapshot before `pytest`, restore after) so the append is not committed. **The fix is one line —
  `testpaths = ["tests"]` in `pyproject.toml`, or rename the probe — and it is not in this increment's
  scope.** It should be the next thing anybody does.
- **`Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`** is the same defect on the stepper: `]` is the step
  BACK and `[` the step FORWARD, against `-+` / `◂▸` / `◄►` / `◀▶`, which all point outward-left then
  outward-right. Not fixed: a stepper's halves are directions, not walls, so it needs its own law, and no
  frame in the sweep renders an invalid stepper.
- **industrial's `▐` is still both `REQUIRED` and the field's wall** (`due▐          ▐12/09/26…`), which
  the round names in §2.3 and §7 q6. Untouched — it is a language-level question about the obligation
  mark, not about handedness.
- **The round's `blueprint_S2` objection to radio-vs-checkbox orientation is doctrine, not a bug** (§4
  above), with the citation in the kit. Left alone.

## 10. Suggested next task

inc40 — `solari_S4`, where the modal shifted the page instead of overlaying it (row 9 of `solari_S4.txt`
equals row 9 of `solari_S1.txt` byte for byte). Same shape as this one: determine whether it lives in
solari's `overlay_instead`, in `screens.py`'s sheet, or in `Kit.overlay`'s composition, then write the law
— *an overlay never changes what is above it* — over all eleven.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `955 passed, 2 skipped` (§7). `verify_language.py` **ALL PASSED**,
      exit 0. `render.py` 66 frames / 330 pairs / 0 hand-drawn, exit 0. `matrix.py` 66 of 66, no refusals,
      exit 0. Teeth run and reported verbatim in §5, not claimed.
- [x] **No secrets in code or output** — four glyph-table entries, four comments, three tests. No network,
      no dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. Every artefact rewritten was rewritten by
      the script that owns it; the eight that moved are listed byte-wise in §6. `tests/test_components.py`
      was restored from a snapshot after each `pytest` run to undo the self-append described in §9 — a
      restore of the file's own pre-run content, nothing deleted.
- [x] **File count within cap** — 2 source files (`taskboard/language.py`, `tests/test_components.py`),
      plus this packet and the `spec.md` `rework-1` amendment: 4. Frames are generated artefacts.
- [x] **Review packet attached** — this document.

# Quick Spec — taskboard · batches `observe-once` and `inheritors-2`

**Batch:** `2026-09-05-fastflow-16` (two batches, run in sequence) · **Base:** worktree
`kanban-variants`, HEAD `c3e1760`, pushed. Predecessor `kits-learn-4` closed 2026-09-05, §8 filled,
archived verbatim to `archive/spec-20260905-kits-learn-4-closed.md`. Language: English.
Increments continue the worktree's single sequence: **… inc33 · inc34 · inc35 · inc36 · inc37**.

**A DEVIATION, NAMED FIRST.** This file was written at the CLOSE, not at Phase A. The operator's brief
was complete enough to act on — it named the findings, the files, the counts to produce and the gates —
and the increments were run straight off it. What is below is therefore a RECORD of a spec rather than a
spec that gated anything, and the honest consequence is that no acceptance criterion here was falsifiable
before the work started. Every criterion is marked with the evidence that closed it, and the packets
(`03-increments/inc34.md` … `inc37.md`) are the primary documents.

---

## 1. Objective (1 line)

Close **F-18** at the seam the evidence points to, and pay `kits-learn-4` §5's declared inheritance debt —
`required` and `pane_split` for the six languages that never chose them — then **photograph all eleven**,
which is what nobody had done.

---

## 2. User stories

- As **the person who has to trust a flaky acceptance test**, I want F-18 diagnosed with counts and
  repaired at the seam the counts point to, so that "re-run it, it passes" stops being the procedure.
- As **a language that was never asked**, I want my own answer to `required` and `pane_split`, because a
  seat with five implementations and six holes is the palette-swap failure with a longer fuse.
- As **the operator judging these frames**, I want to be able to LOOK at all eleven languages, because
  thirty-eight mechanisms held by property tests and by nothing anyone can see is a claim, not a design.

---

## 3. Acceptance criteria (observable)

- [x] **AC-1 · inc34 · F-18 reproduced with counts, and repaired at the right seam.** 60 isolated runs
  and 10 full-suite before and after; a probe that establishes when the old `.col-head` generation is
  gone and whether the SCREEN ever holds two. → **4/60 → 0/60 isolated; the compositor never drew two
  generations in 30 runs, so the seam is the test's observation point.** `inc34.md` §1, §2, §5.
- [x] **AC-2 · inc35 · `required` for the six.** One cell in the ink tier per language, each cited from
  `LANGUAGES.md`. Property test: **11 / 11 distinct, never a digit, survives greyscale**, and `*`
  surviving in exactly one language — the one whose commitment is to inherit the environment.
  `inc35.md` §2, §3.
- [x] **AC-3 · inc36 · `pane_split` for the six.** Mechanisms or declared refusals, through
  `pane_split_rule` / `pane_split_instead` and never by overriding `pane_split`; registry teeth **both
  ways**. Property test: **pairwise-distinct among the six that draw**; the closure law on every seat at
  six widths. `inc36.md` §2, §5.
- [x] **AC-4 · inc37 · frames for the inheritors.** The six screens through all eleven languages: **66
  frames at 100×32**, sidecars regenerated, the matrix at **11 × 6**, every cell `implementa` or a
  declared refusal, **no hand-drawn element anywhere**. `inc37.md` §1, §2.
- [x] **AC-5 · nothing else moves.** Suite green after every increment (**878 baseline → 933**).
  `verify_language.py` **ALL PASSED** (10857) after every increment. The `--surface` sweep run **plain and
  alone** (F-8) leaves its 11 frames unchanged. → §4 below.
- [x] **AC-6 · export.** `python prototypes/export_to_skill.py "C:/Users/jjgh8/.claude/skills/tui-design"`
  at the close, output reported, the skill **never hand-edited**; plus gallery candidates *proposed* with
  a draft `Limit` line each. → §4, §8.

---

## 4. Validation strategy — and what it returned

```
python -X utf8 -m pytest -q                        933 passed, 2 skipped      (baseline 878)
python -X utf8 prototypes/verify_language.py       10857 PASS · ALL PASSED    (baseline 10857)
python -X utf8 prototypes/components/render.py     66 frames · 330 pairs, none identical · 0 hand-drawn
python -X utf8 prototypes/components/matrix.py     66 of 66 implementa
python prototypes/capture_languages.py --surface   11 surfaces · 55 pairs · working tree CLEAN
python prototypes/export_to_skill.py <skill>       languages.py 22 KB · 11 languages · 66 captures identical
```

Headless stdout goes **to a file, never `DEVNULL`** (L-42) — `prototypes/out/_f18_*.log`,
`_b3*_*.log`, `_b_surface.log`, `_b_export.log`. `--surface` was run **plain and alone** (F-8) and left
the working tree clean. No terminal process was killed. Git: committed per increment, pushed at the close.

**The one red that is not this batch's:** `tests/test_app.py::test_win_clipboard_roundtrip` (PENDING #22,
environment-dependent) went red in 2 of the 10 full-suite runs inc34 measured. Named, not filtered.

---

## 5. Non-goals (what is OUT)

- **A PROTOTYPE round on the six inheritors' 36 new frames.** They are correct by every law this repo can
  run and they have not been judged. That is the honest next batch.
- **The skill's prose and gallery.** `export_to_skill.py` writes what it writes; the eight gallery
  candidates in §8 are **proposed**, not installed.
- **`verify_ink.py` over the 66 frames.** Not run, named in `inc37.md` §5.
- ~~**`Kit.button`'s walls for swiss.** Found by looking at `swiss_S4` and recorded in §8, not fixed.~~
  **No longer a non-goal — inc38 closed it** on the operator's verdict of 2026-09-05. §8.
- **pulso, GBL, the course, the main checkout.** Untouched.

---

## 6. Detected security flags

None fires. Every change is a test file, a pure-render method on a kit, a prototype sweep's language list,
or rendered frames of a fixture board. No network, no new dependency, no destructive command, no secret,
no path outside the worktree except the skill directory the exporter already writes and which the operator
named.

---

## 7. Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — see the note at the top; the brief was the spec and this file is the record |
| Phase B (implement) | **done** — inc34 (`observe-once`) · inc35 · inc36 · inc37 (`inheritors-2`) |
| Phase C (close) | §8 — **done** |
| Notes | **6 source files across 4 increments, one agent.** `tests/test_board_seat.py` (inc34); `taskboard/language.py` + `tests/test_components.py` (inc35, inc36); `prototypes/components/render.py` + `matrix.py` + `tests/test_components.py` (inc37); plus this spec, the archived predecessor, four packets and 108 new frame artefacts. |

---

## 8. Close

### What changed

| inc | what | the defect it removed |
| --- | --- | --- |
| 34 | `settled_heads()` at four sample points, and two tests for the screen | a test that sampled the widget tree one `pilot.pause()` after a resize and caught both generations of `.col-head` |
| 35 | `REQUIRED` for five of the six; nord declares | six languages marking an obligation with the base kit's `*` |
| 36 | `PANE_SPLIT_REFUSED` 2 → 5; two new drawing mechanisms; nord declares | six languages ruling a pane seat with the terminal's hairline, three of them against their own commitment |
| 37 | `render.py` / `matrix.py` read `LG.KITS`; three sweep laws move into the suite | a typed list of five languages, stale for three batches |
| 38 | swiss's `button.main` becomes its own weight ladder (`·` `•` `●`, DISABLED air); five laws, one parametrised off `PANE_SPLIT_REFUSED` | `│   Cancel   │` — a border-shaped mechanism in the language whose commitment is "no boxes, at any width" |

### F-18, in one paragraph

**It is the test's observation point, and the measurement is what says so.** `build()` calls
`remove_children()`, which is asynchronous, then mounts the new generation without awaiting the removal —
and it *cannot* await it, because `render()` is its other caller. So the DOM holds six heads where the
board has three, in **2 of 30 runs at the first pause**. The compositor never draws more than three, in
**0 of 30** — a user cannot see it. Repairing `build()` would have meant undoing inc23's F-16 fix to close
a window that never reaches the screen. Isolated reds: **4 in 60 → 0 in 60**.

### The matrix, before and after

```
BEFORE (kits-learn-4 close)              AFTER
30 of 30 implementa, 5 languages         66 of 66 implementa, ELEVEN languages
6 languages rendered in no frame         0 languages rendered in no frame
required:   5 answered, 6 at `*`         11 answered, `*` in exactly one and named
pane_split: 5 answered, 6 at `│`         11 answered, 6 draw distinctly, 5 refuse with a citation
```

### What was found by looking, that no test had asked

- **A closure defect in blueprint's pane seat**, live since inc28: at `w=1` it returned two cells for a
  one-cell seat. Found by inc36's width sweep, fixed there. The only width anyone had ever tested was the
  only width anyone calls.
- **Swiss took `Kit.button`'s wall-shaped mechanism** (`│   Cancel   │`, visible in `swiss_S4`) — a
  border in the language whose commitment is "no boxes, at any width", and the very stroke swiss is in
  `PANE_SPLIT_REFUSED` for refusing between two panes. `button` was not among the seven mechanisms inc32
  scoped, nor among this batch's two, so it was **recorded as the next inheritance debt** rather than
  smuggled in. It is exactly the class of thing that only a frame reveals, which is the argument for
  inc37.
  **CLOSED by inc38**, on the operator's verdict of 2026-09-05. Swiss's `button.main` is now a weight
  ladder of marks it already spends — `·` (`LEVELS["info"]`), `•` (`REQUIRED`), `●` (its own radio
  knob's pressed cell) — set ONCE, on ONE side, with DISABLED left as air; a single cell closes no
  corner at any width, and weight is a shape channel, so the four states never touch colour. It was
  **not** done with a `BUTTON_REFUSED` registry: `Kit.button` already dispatches per language through
  `PART_GLYPHS`, so the precondition that made `pane_split`'s and `overlay`'s tables necessary — an
  entry point that draws a SHARED default — is absent here (inc38 §2). The other ten were measured at
  the same time against `PANE_SPLIT_REFUSED`, and **swiss was the only one**; ledger's `│` is the one
  other hit and it is legal, because ledger draws pane rules (inc38 §3). Four frames moved, all swiss:
  `swiss_S2`, `swiss_S3`, `swiss_S4`, `gallery_swiss`.

### Gallery candidates — PROPOSED, not installed

Eight of the 36 new frames, all `compositor` provenance, all zero hand-drawn, all 100×32. Numbering
continues the gallery's own (`30 · ledger-settings-danger`, `31 · corgi-settings-legend` are the last
two). Each gets a draft `Limit` line in the gallery's shape; the two commitment bullets are for whoever
installs them.

| # | frame | ink | why it earns a seat | draft `Limit:` |
| --- | --- | --- | --- | --- |
| a | `instrument_S1` | 36.0 % | the graticule is the whole structure device in one screen — across the field rows (`⠒`), down the pane gutter (`⠸`) and under the bars (`⣿`) | the densest frame in the sweep, and the `.txt` cannot show that the graticule is DIM and the figures are not; read the SVG for the tier, or the frame reads as one weight |
| b | `industrial_S1` | 24.0 % | one plate convention across three seats in a single view — `▐up▌` keys, `▐ 12/09/26 ▌` figures, and the `▌ ▐` gutter that closes one pane and opens the next | the gutter spends two of three cells, so at any narrower seat the two plates touch; legal by the closure law and untested against a small terminal |
| c | `swiss_S1` | 16.4 % | the counter-frame to (b): the same screen where the divider is NOTHING, and the right pane starts at the next column | the divider is nothing and the reader has to be told so: the `.txt` shows air where every other language shows a mark, and a frame whose mechanism is an ABSENCE cannot be read without its commitment beside it (the button's walls this line used to name were closed by inc38) |
| d | `solari_S1` | 33.5 % | the product becoming ONE SCHEDULE — a task is a row, a phase is a gate, a state is a word in a status column, and the seam is under all of it | the seam runs the full measure on every row, so the frame's ink is structural rather than informational; a reader counting ink will over-read this language's density |
| e | `industrial_S4` | 23.0 % | `MODAL_BOX = DISPLAY_BOX`: the only one of the eleven whose commitment asks for a box draws its lid in half-cell plate (`▛▀▜` / `▙▄▟`) and not the terminal's hairline | half-cell chrome has a different glyph at the top of a box than at the bottom, so this lid cannot be read as a four-corner box; the eight-cell `MODAL_BOX` is why |
| f | `darkside_S4` | 14.4 % | the one language that RESERVES borders for modals, spending the reservation — a rounded lid (`╭╮╰╯`) over a page that separates by a grey step everywhere else | the backdrop's ±1 grey step is a BACKGROUND and a cell grid shows spaces; the `.txt` proves the lid and not the depth behind it |
| g | `solari_S2` | 13.7 % | severity PRINTED, not drawn — `CNX` where the other ten put a glyph, on the board that already argues you read `07` rather than estimate a bar | a three-letter rung costs three cells where a glyph costs one, so this language's error row starts further right than any other's and the columns do not line up across the eleven |
| h | `instrument_S5` | 14.6 % | the dot-count ladder doing its whole job down one log — `⠂⠂ / ⠆⠆ / ⠇⠇`, severity by how much of the cell is lit | and it is the frame that justifies inc36's gutter choice: `⠇` is the ERROR rung here, so the pane rule had to be the other column (`⠸`) or the divider would read as a rejection |

**Nord's six frames are deliberately not proposed.** Nord's commitment is to be the environment, so its
frames are the base kit rendered — admissible as a baseline, not as a language.

### What was NOT done, and why

- **The 36 new frames have not been judged.** No PROTOTYPE round, no operator verdict. §5.
- **No ink-floor law was applied to the 66.** `verify_ink.py` was not a gate here; darkside's S6 at
  8.3 % is the sweep's floor and is named.
- **The skill was not hand-edited.** `export_to_skill.py` ran; the gallery candidates above are proposed.

---

## 9. Batch `rework-1` — the three findings of `PROTOTYPE-inheritors.md` that are not language-level

> **§9.5 was corrected by batch `rework-2` (§10). Two of its three "found by looking" items are
> closed and ONE OF THEM WAS DIAGNOSED WRONG — read §10.3 before acting on §9.5.**

`PROTOTYPE-inheritors.md` (2026-09-05) judged 42 frames and proposed **19 `rework`**. It also argued that
those nineteen are not nineteen defects: nord — the language that overrides nothing — proves that several
of them live in `Kit` or in the composition layer, and its §7 q1 asks whether `Kit` is opened **before**
any language is touched. **This batch is that: three increments, one base-level defect each, no language
given its own answer.** The sixteen remaining `rework` frames are listed in §9.4 and are untouched.

### 9.1 What each increment fixed

| inc | the defect | the level it lived at | frames moved |
| --- | --- | --- | --- |
| 39 | `INVALID` spelled by EXCHANGING the two walls of a field — `nord ] [`, `instrument ⠸⠶⠇`, `industrial ▌/▐`, `blueprint ┤·├`. Orientation is not a channel a reader can use: the two marks sit at opposite ends of a 34-cell row. | **`Kit.PART_GLYPHS["textfield.main"]`** — nord declares no `PART_GLYPHS` at all, so its flip was the base's, and three languages had re-declared the same turn. Fixed at the declaration seat in all four; the law is written once over all eleven. | `nord_S2`, `instrument_S2`, `industrial_S2`, `blueprint_S2` (txt + svg) |
| 40 | `solari_S4` opened on a blank row: the announcement band was anchored at screen index 0, so the mode strip, the masthead and the head seam were gone and the frame could not say which mode it was in. | **`Solari.overlay_instead`** — *not* `Kit.overlay` and *not* `screens.py`, which ten languages share and ten leave their page intact through. The band still takes the head of the board; `schedule_head` now says which head, by finding the first full-measure seam. | `solari_S4` (txt + svg) |
| 41 | **none — the premise inverted.** The knockout on `blueprint_S4`'s `DELETE` is operator **ruling 10** of 2026-09-04, recorded verbatim in the archived spec §6.1, implemented by inc17 and cited at two seats; the `.txt` not carrying it is the limit `knockout_cell`'s own docstring publishes. Measured over all 66 frames, the exporter paints exactly the grounds the kits declare. | — | none |

**The rule inc39 applied, stated so it can be argued with:** restore the language's declared handedness;
where un-flipping alone would collide byte-for-byte with another state, the walls take that language's own
`DANGER_FORM` — the seat swiss (`╲ ╱`) and darkside (`Ø Ø`) already spend theirs on. So
`instrument ⠇⠶⠸` and `industrial ▐/▌` (un-flip only), `nord ! !` and `blueprint ━·━` (walls to
`DANGER_FORM`, because un-flipping would have made INVALID byte-identical to DEFAULT).

### 9.2 The laws this batch added

- **inc39** — an invalid field's opening mark may not be one the language uses ONLY to close, and its
  closing mark may not be one it uses ONLY to open; asked of all eleven at three widths (1, 12, 34). Its
  own vacuity is asserted: six languages give a field the same mark on both sides in every state and have
  no handedness to violate, so the law bites on exactly five (`instrument`, `industrial`, `nord`,
  `ledger`, `blueprint`). Teeth: the four old declarations restored byte for byte go red, the other seven
  stay green.
- **inc40** — the rows a modal changes form ONE contiguous band, and that band never takes the page's
  first row. `corgi` is exempt by its own citation (*"a confirm is a MODE and the board is gone"*),
  asserted word for word and checked to be doing work. Teeth: `schedule_head → 0` IS the pre-inc40 body,
  and under it the mode strip is gone and row 9 is row 9 again.
- **inc41** — the `.svg` paints exactly the grounds the kit declared, over all 66 frames, with the
  13-frame evidence roster written down; and the STYLE tier (`bold` / `underline` / `reverse`) is asserted
  to reach neither artefact — 66 declared match runs across the eleven S6, none painted. The pair is its
  own teeth: the same comparison comes out equal on one tier in 66 of 66 and unequal on the other in
  11 of 11.

### 9.3 Three answers to `PROTOTYPE-inheritors.md` §7, given by looking rather than by verdict

- **q1 (`Kit` before the languages)** — answered by measurement, and the round's arithmetic was off. The
  attribution is right (`Kit`'s line is the origin) but the fix is not one edit: ten of the eleven declare
  a full 14-key `PART_GLYPHS`, so patching `Kit` moves `nord_S2` and nothing else. §5.8 of the round flags
  its own inference as unrendered; it is rendered in inc39 §1.
- **q2 / §0b (blueprint's ruling 10)** — **the round is wrong on the record.** `PROTOTYPE.md` §4 is the
  list of questions PUT to the operator; all ten were answered on 2026-09-04 and §6.1 of
  `spec-20260905-kits-learn-3-closed.md` records them. Question 10 was answered **yes**. The exporter
  decided nothing. Whether to *reconsider* the ruling is still the operator's; this batch does not
  prejudge it.
- **q3 (blueprint's first fixation not rendered in five of six)** — doctrine. `_state_cell` fires the
  reverse on the `alert` mood alone and the seeded board is calm, so the title block's knockout is
  **unspent, not missing** — which is precisely what makes ruling 10's move legal without breaking
  "exactly one per view". Exercised in both moods in inc41.
- **q7 (orientation as the only channel of a state)** is answered for the FIELD and left open elsewhere.
  **Blueprint's `radio.main` turns its terminators on purpose, with a citation in the kit** (*"a callout
  selecting one item from a schedule"*), so inc39's law is scoped to `textfield` and exempts it by name.
  The round reads blueprint's radio/checkbox pair as a defect; on the evidence in the kit it is doctrine.

### 9.4 The `rework` frames this batch did NOT touch — language-level, still open

Sixteen of the round's nineteen. Each is one language's own declaration, and none of them is fixable at
the base:

| frame | the finding, in one line | the §7 question it belongs to |
| --- | --- | --- |
| `instrument_S2` | the ERROR rung `⠇` opens the SAFE button; severity inverted in the controls | q5 (cell overload) |
| `instrument_S3` | `⠁` is `REQUIRED` in S2 and `DISABLED` here — two meanings, no cue | q6 (the obligation mark) |
| `instrument_S4` | the only severity cell in a destructive confirm sits on `Cancel` | q5 |
| `swiss_S2` | `Save` (DISABLED) is typographically a caption; four walled controls beside one bare one | inc38's own §7 |
| `swiss_S3` | `·` (`LEVELS["info"]`) prefixes `╲Delete all╱` — the lowest rung on the most dangerous control | q5 |
| `swiss_S4` | `•` (`REQUIRED`) is the focus ring on the irreversible button; the modal opens and never closes | q6 |
| `industrial_S2` | `▐` is both `REQUIRED` and the field's wall, eight spaces apart on one row | q6 |
| `industrial_S3` | the danger-zone CAPTION is plated exactly like the button beside it | q8 (caption vs control) |
| `nord_S1` | the load plot beats the declared subject in the pane the split exists to give one subject | — (nord's own metric) |
| `darkside_S1` | the `.txt` has no pane separation at all; only the `.svg` shows the grey step | q10 (the `.txt` as the work) |
| `darkside_S3` | caption and destructive button open with the same `▬` on consecutive rows | q8 |
| `darkside_S6` | `bold {ink}` in an achromatic language — probably unobservable even in a real terminal | q9 |
| `solari_S2` | `▁` does nine jobs in one screen; "point at the required fields" has no non-positional reading | q6 |
| `blueprint_S1` | the first-fixation law is unspent on a calm sheet (see §9.3 q3 — **doctrine, not a bug**) | q3 |
| `blueprint_S2` | `├` is both `REQUIRED` and the dimension's opening terminator; radio and checkbox differ only by orientation (**the second half is doctrine** — §9.3 q7) | q6 / q7 |
| `blueprint_S3` | on and off differ by ONE hairline cell (`├─┤` vs `├┤·`) | q5 |

### 9.5 Found by looking, not fixed — and one of them is urgent

- **`pytest -q` MUTATES THE SUITE.** `prototypes/out/_b37_test.py` matches pytest's default
  `python_files = test_*.py *_test.py`, so a bare `pytest` from the repo root **collects it and runs its
  module body**, which appends the inc37 block to `tests/test_components.py`. HEAD already carries
  **three** such copies — three prior gate runs — and the test count never moved because the duplicate
  `def`s shadow each other. inc38 §7 recorded the symptom; this is the cause. Neutralised by hand
  (snapshot before `pytest`, restore after) for all three commits in this batch. **The fix is one line:
  `testpaths = ["tests"]` in `pyproject.toml`, or rename the probe.**
- **`prototypes/gallery/gallery_darkside.{txt,svg}` are stale on disk**, last baked at inc21 while
  `language.py` has been edited a dozen times since; `capture_languages.py` renders a radio as `( )` where
  the committed frame has `(.)`. **Proved not this batch's doing** by checking `language.py` out at the
  pre-batch commit `8604607`, re-running the capture, and getting the identical diff.
- **`blueprint_S4`'s destructive control carries no danger mark and no focus mark in either tier.**
  `screens.s4_blueprint` builds it with `knockout_cell(" DELETE ")` instead of `button(..., FOCUSED,
  danger=True)`, so it loses its walls, its `DANGER_FORM` and its focus and gains the reverse. Ruling 10
  moved the KNOCKOUT; it did not say the default answer stops being a button. Fixing it needs
  `knockout_cell` and `button` to compose, which is a new kit seat — named, not invented.
- **`Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`** is inc39's defect on the stepper (`]` as the step
  BACK against `-+` / `◂▸` / `◄►` / `◀▶`). Not fixed: a stepper's halves are directions, not walls, so it
  needs its own law, and no frame in the sweep renders an invalid stepper.

### 9.6 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc39 · inc40 · inc41 |
| Phase C (close) | this section |
| Notes | **2 source files across 3 increments, one agent.** `taskboard/language.py` (inc39, inc40) and `tests/test_components.py` (all three), plus three packets, this section and 10 frame artefacts. `capture_languages.py` was run once and confirmed no board rendering changed. |

---

## 10. Batch `rework-2` — the tooling the language rework needs, and two wrong diagnoses corrected

`rework-1` closed three base-level defects and left three items "found by looking" plus sixteen
language-level `rework` frames. **This batch is the tooling: stop the suite corrupting itself, make the
`.svg` show the tier it was dropping, and build the census that turns sixteen taste arguments into one
measured question.** No language was changed and no frame was judged.

### 10.1 What each increment did

| inc | the defect | the level it lived at | artefacts moved |
| --- | --- | --- | --- |
| 42 | `pytest -q` **appended a block to `tests/test_components.py` on every run**. `prototypes/out/_b37_test.py` matched pytest's default `python_files`, and collecting a module runs its body. HEAD carried three copies. | `pyproject.toml` had no `testpaths`, and the probe was named like a test. **Both closed** — `testpaths = ["tests"]` and a rename. Proved by an md5 that does not move across a full run. | `tests/test_components.py` −116 lines; 995 collected before and after |
| 42 | `gallery_darkside` "stale since inc21" | **wrong diagnosis — see §10.3.** It is calendar-dependent, and was one day old. | `gallery_darkside.{txt,svg}` |
| 43 | the `.svg` painted **0** of the **66** style runs the eleven S6 sheets declare. `bold`/`underline` never reached it; `reverse` reached Rich as a style FLAG with colour and bgcolor still in declared order, so an exporter reading `bgcolor` saw the page ground. | `capture_languages.cell_grid` (the swap) and `svg_from_grid` (the two attributes). **Not `screens.py` and not a kit.** | the eleven `*_S6.svg`, and the 22 gallery `.svg` the same exporter takes. **All 88 `.txt` byte-identical.** |
| 44 | `verify_ink.py` printed a bare table that was then quoted as if it measured the 66 frames. It measures the LIVE widget, 11×3, and drifts. | the script's own naming, plus a missing mode. Now `glance ink, 11x3, live` and `frame ink, 66 frames, static`. **Neither is a gate.** | none |
| 44 | the sixteen language-level findings had no common measurement | **`prototypes/collision_census.py`** — 54 cells across the eleven that carry more than one role. | `prototypes/out/collision_census.txt` |

### 10.2 The laws and tools this batch added

- **inc43** — *the `.svg` paints exactly the style runs the kit declared*, over the eleven S6: six declared
  and six painted each, 66 = 66, **and the word must match too** (a `bold` language's S6 carries no
  `text-decoration` anywhere). Its teeth are the two `reverse` kits: each of their six runs paints the
  query in the CELL'S OWN GROUND on a rect of the kit's hue — painting the hue as ink would keep the count
  and mean nothing was fixed — and the SEVENTH `re` in every frame (the search field) is asserted to be
  excluded, because a measurement that counted text content would score 7.
- **inc43** — `declared_grounds` learned that **`[reverse #456]` is `[… on #456]` said backwards**. The
  vacuity roster is 13 → **14**: `industrial_S6` declared six grounds the whole time and neither the
  census nor the exporter could see them. Two blind spots facing each other read as agreement.
- **inc44** — `verify_ink.py --frames`, deterministic, floor `corgi_S4` 2.7% and ceiling `ledger_S4`
  48.8%. **One formula for both modes, and it now discards U+2800 BRAILLE PATTERN BLANK** — an empty
  braille cell is a space that lives in the braille block. Seven frames move by up to 1.9 points, and
  **`instrument_S1` crosses DENSITY.md's 35% line the wrong way (36.0% → 34.3%): it was over the floor on
  padding.**
- **inc44** — `prototypes/collision_census.py`, with the five collisions the round found by hand asserted
  as a self-check before any table is printed.

### 10.3 `gallery_darkside` was never stale, and §9.5 says the opposite

`Darkside.wordmark()` calls `doodle()`, which is `PHASES[date.today().day % 6]` — *"identity is a
date-driven moon doodle"*, the last clause of its own class docstring.

```
baked 2026-09-05 (inc21)   day 5 -> 5 % 6 = 5 -> PHASES[5] = "(.)"     the committed cell
re-baked 2026-09-06        day 6 -> 6 % 6 = 0 -> PHASES[0] = "( )"     what the sweep now writes
```

**One day old, not four months.** And §9.5's own probe had already proved it: reverting `language.py` to
`8604607` and getting the identical diff means the source is not involved *at all*, which was read as "not
this batch's doing" instead. **The re-bake is committed and closes nothing** — on 2026-09-07 the committed
frame is wrong again. Closing it needs a pinned date (as the fixture is pinned) or the doodle cell exempted
from the comparison: **a design change, so it is the operator's.**

### 10.4 The sixteen language-level frames, now with their census rows

Still open, still untouched. The census column is the cell's own row from `collision_census.txt`; a blank
one is a finding the census **cannot** see, which is as useful to know.

| frame | the finding | census row |
| --- | --- | --- |
| `instrument_S2` | ERROR rung `⠇` opens the SAFE button | **`⠇` (4)** LEVELS[error] · INVALID textfield.main open · button.main open · textfield.main open — **and its mirror `⠸` (3)** on both closers |
| `instrument_S3` | `⠁` is REQUIRED in S2 and DISABLED here | **`⠁` (5)** REQUIRED · checkbox.main (disabled) · stepper.main · switch.main (disabled) · textfield.main (disabled) |
| `instrument_S4` | the only severity cell in a destructive confirm sits on `Cancel` | **`⠛` (2)** DANGER_FORM · checkbox.main (focused) — the danger form IS the focused checkbox |
| `swiss_S2` | `Save` (DISABLED) is typographically a caption | — (a weight/type finding; no cell carries two roles) |
| `swiss_S3` | `·` (`LEVELS["info"]`) prefixes `╲Delete all╱` | **`·` (6)** LEVELS[info] · button.main open (default) · checkbox.knob · radio.knob · stepper.main · textfield.main |
| `swiss_S4` | `•` (REQUIRED) is the focus ring on the irreversible button | **`•` (3)** REQUIRED · **button.main open (focused)** · radio.knob — the round's finding, verbatim |
| `industrial_S2` | `▐` is both REQUIRED and the field's wall | **`▐` (4)** REQUIRED · INVALID textfield.main open · button.main open · textfield.main open — **and `▌` (3)** on both closers |
| `industrial_S3` | the danger-zone CAPTION is plated like the button beside it | — (a composition finding; the caption is not a `PART_GLYPHS` slot) |
| `nord_S1` | the load plot beats the declared subject | — |
| `darkside_S1` | the `.txt` has no pane separation at all | — |
| `darkside_S3` | caption and destructive button open with the same `▬` | — **and this is the census's own limit**: `▬` is drawn outside `PART_GLYPHS`, so set B cannot reach it |
| `darkside_S6` | `bold {ink}` in an achromatic language | — the tier now reaches the `.svg` (inc43); whether the weight is observable is still open |
| `solari_S2` | `▁` does nine jobs in one screen | **`▁` (7 families, 18 declared seats)** REQUIRED · button · checkbox · radio · stepper · switch · textfield. The round counted per SCREEN; the census counts per KIT, and it is the widest single cell in the corpus |
| `blueprint_S1` | first fixation unspent on a calm sheet | — doctrine (§9.3 q3) |
| `blueprint_S2` | `├` is both REQUIRED and the dimension's opening terminator | **`├` (7)** REQUIRED · INVALID stepper.step open · button · checkbox · radio · stepper · textfield — **and `┤` (7)** on the closers |
| `blueprint_S3` | on and off differ by ONE hairline cell | — (a contrast finding between two states of one part) |

**Five of the sixteen have an exact census row, four more have a partial one, seven have none.** The seven
are composition and typography findings, and they say what the census is not: it reads DECLARATIONS, not
frames.

### 10.5 What the census found that the round did not — and the languages with no frame in §10.4

`collision_census.txt`, 54 cells over eleven languages, **zero languages clean**. The rows the sixteen
never named:

- **`naught ∙` (6 families)** — `LEVELS[error]` **and** `LEVELS[warn]` **and** `DANGER_FORM` **and**
  `REQUIRED` **and** `CUR` **and** the switch indicator. Five meanings on one dot, and **naught has no
  frame among the sixteen at all.** By family count it is the worst cell in the corpus.
- **`naught ◦` (6)** — info **and** warn, plus both button walls, the checkbox and the radio.
- **`corgi ▁ ▄ ▀ █` (7/7/4/4)** — corgi spends its four-step block ramp twice: once as `LEVELS`, once as
  chrome. **corgi also has no frame among the sixteen.**
- **`ledger †` (2)** — `LEVELS["warn"]` **is** `REQUIRED`. One dagger, two meanings, and ledger has no
  frame among the sixteen either.
- **`darkside O` (4)** — `LEVELS["error"]` **is** `CUR`, and both knobs.
- **`prism ⣿` (7)** — error **and** `DANGER_FORM` **and** all three button walls.
- **`nord [ ]` (4 each)** — the stepper's INVALID step **is** the button's wall and the checkbox's well.

**AND THE CENSUS FLAGS inc39's OWN FIX.** `swiss ╱ ╲`, `nord !`, `blueprint ━`, `corgi ▄`, `darkside Ø`
and `ledger ‡` all show `DANGER_FORM` sharing cells with the INVALID textfield walls — **which is exactly
the rule inc39 applied on purpose** (§9.2). The census cannot tell a deliberate alignment from an accident;
it asks the question and the answer is the operator's. That limit is stated in the script's own docstring.

**The B×B boundary is a decision, not an oversight.** Two controls sharing a wall form is how a language
reads as one language, so chrome-only sharing is counted and not listed; the count is printed per language
so the choice can be reversed by whoever disagrees.

### 10.6 Found by looking, not fixed

- **`gallery_darkside` is calendar-dependent** (§10.3). Live, and no amount of re-baking closes it.
- **`instrument_S1` is under DENSITY.md's glance floor** once the braille blank stops counting as ink
  (36.0% → 34.3%). It was over the floor on padding.
- **`verify_ink.py`'s live mode drifts** — `industrial board` 50.8% then 51.5% back to back, `nord board`
  29.2% then 29.3%, the other 31 cells identical. Cause not established; on that pair the drift stayed out
  of the `glance` column the floor is read off. **Not a gate, deliberately.**
- **`test_win_clipboard_roundtrip` is environment-coupled.** It drives the real Windows clipboard through
  PowerShell and fails when anything else on the desktop holds it — `Set-Clipboard` itself returns
  *"Requested Clipboard operation did not succeed"*. It is the one test in the suite whose result depends
  on the machine's GUI state.
- **`blueprint_S4`'s destructive control has no danger mark and no focus mark in either tier** (inc41 §8).
  Untouched.
- **The gallery boards carry 15–48 bold runs each and nobody has judged those pictures** (inc43 §9). They
  are more faithful than what they replace, which is not the same as saying anyone has looked.

### 10.7 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc42 · inc43 · inc44 |
| Phase C (close) | this section |
| Notes | **7 source files across 3 increments, one agent** (`pyproject.toml`, `tests/test_components.py`, `prototypes/capture_languages.py`, `prototypes/verify_ink.py`, `prototypes/collision_census.py`, `.gitignore`, `tests/test_scratch_cannot_be_committed.py`), plus 35 regenerated artefacts, the census table, three packets and this section. **No kit and no screen was changed; not one of the 88 `.txt` moved.** |

---

## 11. Batch `rework-3` — the language-level rework

`rework-1` closed three base-level defects, `rework-2` built the instrument. **This batch is the rework
itself: four increments, the sixteen language-level `rework` frames of §9.4 answered one by one, and the
operator's rule written once and then enforced by three property laws over all eleven languages.**

### 11.0 The rule this batch enforces, and where it is written

> A cell that carries a **meaning** — a severity rung `LEVELS[*]`, the `DANGER_FORM`, `REQUIRED`, `CUR`,
> or a declared `INVALID` mark — may not carry a second meaning in the same language **unless the two are
> distinct on a channel that language declares** (count, weight, tier, position); and it may not stand at
> a position in control chrome where a reader would take it for that meaning: **the opener of a control,
> the indicator of a switch, a disabled mark**. Chrome-on-chrome (B×B) is an ALPHABET and is not a
> collision. **Every exemption is by name with a citation in the kit; silence is not an exemption.**

Written in full in `inc45.md` §0, with `VERIFY.md`'s *"assert distinctness on the channel that is left"*
as its authority. It is enforced by three laws, each parametrised over all eleven and each with a teeth
test that must name the LANGUAGE and the two roles:

| law | clause | added | state |
| --- | --- | --- | --- |
| `test_a_languages_meaning_marks_do_not_share_a_cell` | meaning × meaning | inc45 | **11 of 11 pass** |
| `test_a_meaning_never_stands_at_a_disabled_or_indicator_seat` | the switch indicator, the disabled mark | inc46 | 7 of 11 pass; the other four counted by name |
| `test_no_control_opens_with_a_mark_that_means_something` | the opener | inc48 | 7 of 11 pass; the other four counted by name |

### 11.1 What each increment did

| inc | languages | the defect | frames moved |
| --- | --- | --- | --- |
| 45 | naught · corgi · nord · swiss · industrial · darkside · ledger | **two MEANINGS on one mark.** `naught ∙` was severity + danger + obligation + position; `nord !` warn + destruction; `swiss ━` error + cursor; `industrial ▪` warn + cursor; `darkside O` error + cursor; `ledger † ‡` obligation and refusal + the two severity rungs. **corgi `▄` was found by the law, not by the round** — the danger form one rung DOWN its own ladder. | 24 |
| 46 | instrument · swiss | **a meaning at a named seat.** instrument's error rung `⠇` OPENED every button and field and its obligation `⠁` was the dead switch, dead track, dead checkbox and dead paper; swiss's `━` was the switch's ON indicator, its `•` the focus ring on an irreversible button and the radio's knob, its `·` — the lowest rung — opened `╲Delete all╱`. Four swiss controls still enclosed in the language committed against boxes. | 9 + 2 gallery |
| 47 | solari · nord | **the widest cell in the corpus, and a docstring's own metric.** `solari ▁` was `REQUIRED` and the seam and every control's DEFAULT rung — 139 occurrences on `solari_S2`, two of them the answer. nord's load plot was 27 near-solid block cells beating the declared subject in the pane the split exists to give one subject. | 2 + 2 gallery |
| 48 | industrial · darkside | **a caption plated as a control**, in each language's own `field_row` and not in the sheet; `industrial ▐` obligation + the plate's opening half; `darkside bold {ink}` in an achromatic language. Plus the opener law over all eleven. | 7 (+1 svg-only) |

**14 source-file edits across 4 increments, one agent.** `taskboard/language.py` (all four),
`tests/test_components.py` (all four), `prototypes/collision_census.py` (45, 46, 47),
`prototypes/verify_language.py` (47).

### 11.2 The census: 54 → 48, and the number that matters more

```
language      HEAD  inc45  inc46  inc47  inc48      live meaning x meaning
naught           3      5      5      5      5      1  ->  0
corgi            5      5      5      5      5      2  ->  2
instrument       8      8      7      7      7      1  ->  1
swiss            8      9      5      5      5      1  ->  0
industrial       5      4      4      4      4      2  ->  1
nord             5      4      4      4      4      1  ->  0
darkside         3      3      3      3      3      1  ->  0
prism            5      5      5      5      5      1  ->  1
ledger           4      2      2      2      2      2  ->  0
solari           3      3      3      3      3      0  ->  0
blueprint        5      5      5      5      5      3  ->  3
TOTAL           54     53     48     48     48     15  ->  8
```

**Two numbers, and the right-hand pair is what the rule is about.** The left counts every cell that does
more than one job, meanings AND chrome together. The right counts only cells carrying two or more
MEANINGS, with the batch's two named exemptions subtracted — and **every one of the eight left involves
`INVALID`**, which is inc39's ruling (§9.2) and not this law's territory.

**The census's own limits showed twice and both are recorded.** `naught` went 3 → 5 and `swiss` 8 → 9 in
inc45 because the marks their obligation and position moved ONTO were already spent on chrome — those are
A×B rows, which the census calls *questions* and the rule permits. And inc47 and inc48 each moved the
total by ZERO while closing the two sharpest findings in §9.4: solari traded a seven-family row for a
two-family row (the census counts rows, not families) and darkside's caption-as-button was never a census
row at all, because `▬` carries no A-family — which §10.4 predicted in writing.

**The three rosters that carry what is left**, each asserted exactly so it can only move when somebody
edits it:

| roster | clean | still failing |
| --- | --- | --- |
| `MEANING_AT_A_NAMED_SEAT` (inc46) | 7 | naught 8 · corgi 8 · prism 8 · blueprint 8 |
| `MEANING_AT_AN_OPENER` (inc48) | 7 | corgi 31 · prism 19 · blueprint 6 · naught 2 |
| `HANDED_FIELDS` (inc39, grew in inc46) | — | six languages have no handedness; swiss joined the five that do |

### 11.3 The sixteen, one by one

| frame | §9.4's finding | inc | state |
| --- | --- | --- | --- |
| `instrument_S2` | the ERROR rung `⠇` opens the SAFE button | 46 | **fixed** — the rails mirror; the opener takes the gutter's column, the column inc36 chose for this exact reason. `⠇` is now the closer, which is a **declared cost**: the left braille column IS the ladder's column, and the only four-dot alternative is this language's caret |
| `instrument_S3` | `⠁` is `REQUIRED` in S2 and `DISABLED` here | 46 | **fixed** — five dead seats moved to `⠄` / `⠈`, rungs this language already spends on dead things. `⠁` means obligation and nothing else; its census row is gone |
| `instrument_S4` | the only severity cell in a destructive confirm sits on `Cancel` | 46 | **fixed at the opener.** The round called it *"severidad invertida"* and that half was **wrong**: counted in dots the focused (destructive) button is heavier, 4 against 3, and the danger form `⠛` is heavier than the error rung. What was real is the rung on `Cancel`, and it is off the opener |
| `swiss_S2` | `Save` (DISABLED) is typographically a caption | 46 | **partly fixed, and honestly.** The four controls beside it lost their walls so the screen is consistent — but the dead button is still air. There is nothing lighter than `▫` in this alphabet that is not a dashed rule (the shape being given up) or `·` (a severity rung, which the new law forbids at exactly this seat). **Still open** |
| `swiss_S3` | `·` (`LEVELS["info"]`) prefixes `╲Delete all╱` | 46 | **fixed** — the button's ladder is one shape at three weights (`▫ ▪ ■`) and no rung is a declaration |
| `swiss_S4` | `•` (`REQUIRED`) is the focus ring on the irreversible button; the modal opens and never closes | 46 | **half fixed.** Obligation keeps `•` and focus took `▪`. The unclosed modal is a composition finding in `overlay_instead` and is **still open** |
| `industrial_S2` | `▐` is both `REQUIRED` and the field's wall | 48 | **fixed** — the plate keeps the cell (it is this language's whole notation) and obligation takes `!`, the register's own stencil |
| `industrial_S3` | the danger-zone CAPTION is plated like the button | 48 | **fixed** — and the brief's question is answered: the sheet does NOT call `button` for a caption; `field_row` plates the value, and industrial's plate was byte for byte its DEFAULT button. `nord_S3` is the reference and the caption is bare |
| `nord_S1` | the load plot beats the declared subject | 47 | **fixed** — both quantity seats (`_meter_blocks`, the base's, and `Nord.detail_rows` inline, which is the one the docstring measured) draw the terminal's own progress bar and the figure leads. **Block-element cells in the frame: 27 → 0**, and it is a `verify_language` check now |
| `darkside_S1` | the `.txt` has no pane separation at all | 48 | **doctrine, cited — and the ruling is the operator's**, which is the round's own last sentence. The grey step is written down at `pane_split_instead` (*"a background is not a cell"*) and the `.svg` carries 28 rects of it; the rail is one mark on one side under inc38's principle. What this batch did was make sure it did not get WORSE: `▏` 16 → 16, `▬` 6 → 0 |
| `darkside_S3` | caption and destructive button open with the same `▬` | 48 | **fixed** — the caption's seat is `◦`, the lightest cell this alphabet has; not `▏`, because that took `darkside_S1` from 16 strokes to 22 |
| `darkside_S6` | `bold {ink}` in an achromatic language | 48 | **fixed** — `reverse {mut}`, a ±1 grey STEP of ground, which is the channel §8 declares. `GROUNDED_FRAMES` 14 → 15, the reverse kits 2 → 3, both asserted |
| `solari_S2` | `▁` does nine jobs in one screen | 47 | **fixed** — obligation takes `▮`, the flap standing. **Re-measured: `▁` 139 → 137, of which mean REQUIRED 2 → 0.** The round undercounted ("more than sixty"); both readings reach the same verdict |
| `blueprint_S1` | first fixation unspent on a calm sheet | — | **doctrine**, closed by §9.3 q3 before this batch |
| `blueprint_S2` | `├` is `REQUIRED` and the dimension's opening terminator | — | **still open.** blueprint had no increment in this batch; it is 6 on the opener roster and 8 on the named-seat roster |
| `blueprint_S3` | on and off differ by ONE hairline cell | — | **still open** — a contrast finding between two states of one part, which no law in this batch reaches |

**Twelve fixed, two doctrine-with-citation, and `swiss_S2` / `swiss_S4` / `blueprint_S2` / `blueprint_S3`
carrying named residue.**

### 11.4 The skill's gallery — five frames are stale and must be re-installed

`export_to_skill.py` writes `assets/languages.py`, `assets/languages/` and `SURFACES.md`. **It does not
touch `assets/gallery/`**, where frames 44–51 were installed. Five of the eight no longer match their
source and are a MANUAL install:

| # | gallery frame | source | |
| --- | --- | --- | --- |
| 44 | `44_instrument-list-graticule` | `instrument_S1` | identical |
| **45** | `45_industrial-list-plate` | `industrial_S1` | **stale** — inc45 (cursor `▪`→`▶`) and inc48 (`field_row` loses the plate) |
| **46** | `46_swiss-list-next-column` | `swiss_S1` | **stale** — inc45 (cursor `━`→`▮`) |
| 47 | `47_solari-list-gate-seam` | `solari_S1` | identical |
| **48** | `48_industrial-modal-plate-lid` | `industrial_S4` | **stale** — inc45 (cursor) |
| **49** | `49_darkside-modal-rounded-lid` | `darkside_S4` | **stale** — inc45 (cursor `O`→`▊`) |
| **50** | `50_solari-form-printed-severity` | `solari_S2` | **stale** — inc47 (obligation `▁`→`▮`) |
| 51 | `51_instrument-monitor-dot-ladder` | `instrument_S5` | identical |

**Two of the eight draft `Limit:` lines in §8 are now wrong** and go with the re-install: (b)
`industrial_S1`'s cites *"`▐ 12/09/26 ▌` figures"* — the figures are no longer plated; (c) `swiss_S1`'s
already carried one correction (inc38) and needs a second (the cursor is `▮`, not `━`).

`assets/languages/` moved in 6 files across the batch — `board_nord.{txt,svg}` (inc47),
`gallery_instrument.{txt,svg}` and `gallery_swiss.{txt,svg}` (inc46) — all written by `export_to_skill.py`
and verified idempotent on a second run (`0 written, 66 already identical`). **The skill repo was not
committed.**

### 11.5 Found by looking, not fixed

- **corgi has never had a frame judged and is the worst language in the corpus by every roster this batch
  built**: 31 opener seats, 8 named seats, 2 live meaning×meaning rows. Its four-step block ramp is
  `LEVELS`, the chrome ladder, the danger form and the obligation mark at once. `prism` (19 / 8 / 1) and
  `blueprint` (6 / 8 / 3) are the same shape, narrower.
- **`naught` and `solari` have no unspent cell left.** Both had to put a meaning on a mark their own caret
  already wears (`◉`, `▮`), and both are argued at the seat as ONE meaning at two seats rather than two
  meanings on one cell. That argument is available exactly twice and it has been spent twice.
- **The stepper has no law.** inc39 declined to extend its INVALID law there (*"a stepper's halves are
  directions, not walls"*, §9.5) and inc48's opener law excludes it for the same reason. It costs the
  opener law swiss's and nord's `stepper.main` — five seats each — and
  `Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["` is still the base's unfixed flip.
- **`verify_language` caught two things the suite could not.** instrument's dead track colliding with its
  dead KNOB (*"a knob drawn like the fill is not a knob"*), and swiss's first indicator answer making its
  bar byte-identical to darkside's. Both were caught by laws written for other batches.
- **A fallback is not a declaration, and both instruments had to learn it separately.** The census learned
  it in inc44 (`invalid`); `meaning_marks_at_named_seats` learned it in inc47 (`disabled`), from a false
  positive that reported solari's CARET as a disabled mark. naught's named-seat count fell 9 → 8 on that
  correction.
- **`ledger` is the batch's cheapest fix and the only language that came out clean on every roster**:
  one declaration (`LEVELS`) moved to `*` / `**`, and its census count halved, 4 → 2.
- **`test_win_clipboard_roundtrip` is environment-coupled** (§10.6) and was red at HEAD before the batch
  began, in every run of all four increments.

### 11.6 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc45 · inc46 · inc47 · inc48 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1004 → 1040 passed** (+36: three laws × 11 parametrisations + three teeth tests), the clipboard red throughout and named in every packet. `verify_language.py` **ALL PASSED** after every increment. `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` 66 of 66. `capture_languages.py` run after every increment; 4 gallery artefacts moved in total. `collision_census.py` self-check green; **4 of the round's 5 hand-found collisions are asserted CLOSED and cannot grow back**, 1 is live with its reason. `export_to_skill.py` run at the close, idempotent on re-run. |
| Notes | **4 source files across 4 increments, one agent** (`taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`, `prototypes/verify_language.py`), plus 42 regenerated frame artefacts, 4 gallery artefacts, the census table, four packets and this section. |

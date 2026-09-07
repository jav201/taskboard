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

---

## 12. Batch `rework-4` — the three items on the re-judged round that are defects and not decisions

`PROTOTYPE-inheritors-2.md` (2026-09-06) re-judged the same 42 frames after `rework-1/2/3` and returned
**keep 14 · nota 21 · rework 7**. Its §5 groups what is left by who fixes it and its §6 puts seven
questions to the operator. **This batch is the intersection: the items that are DEFECTS ON THE RECORD and
need no operator ruling — K1, C3, K3. Three increments, one agent. Nothing in §6 was decided and nothing
in §6 was touched.**

### 12.1 What each increment did

| inc | the finding | the level it lived at | frames moved |
| --- | --- | --- | --- |
| 49 | **K1 — the named-seat law never looked at `switch.knob`.** inc46 wrote its clause as `comp == "switch" and part == "indicator"`, and in these kits the indicator is the TRACK. `darkside_S3` drew five switch knobs with `O` = `LEVELS["error"]` (`▬▬O`, `O──`) while the roster said **0**; the census saw it and the law did not. The same hole hid `naught ◉` and `corgi ██`/`▀▀`. | the CLAUSE, in `tests/test_components.py`; plus one kit's declaration (`Darkside.PART_GLYPHS`) | `darkside_S2`, `darkside_S3` (txt + svg), `gallery_darkside` (txt + svg) |
| 50 | **C3 — `solari_S4`'s band slid three rows instead of shrinking.** inc40 gave back the mode strip, the masthead and the head seam and took `GATE DOING 04` and `FIX LOGIN REDIRECT`, so the surviving schedule opened on the SEAM of a departure the band had taken, five task rows under no gate header. | **`Solari.overlay_instead`** — not `screens.py`, whose six dialog rows are shared by all eleven | `solari_S4` (txt + svg) |
| 51 | **K3 — the stepper had no law and `Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["`.** Six kits spelled REJECTED by exchanging their two direction marks; inc39 deferred it in §9.5 and inc48 then used that deferral as the reason to exclude the stepper from the opener law. | **`Kit`** (nord's line) plus five kits' own; the two exclusions in `tests/test_components.py` | **none** |

### 12.2 The laws this batch added or widened

- **inc49** — `test_a_meaning_never_stands_at_a_disabled_or_indicator_seat` now covers **every knob the
  registry declares** (`switch.knob`, `checkbox.knob`, `radio.knob`) as well as the switch indicator and
  every disabled mark. The seat set is written as `KNOB_SEATS` so the slider's absence is legible as the
  census's boundary and not as a claim. **No new test function**: the law that existed now reaches four
  seats it could not see, which is why `pytest` stayed at 1040 across that increment. Teeth grew a third
  arm that restores `Darkside.PART_GLYPHS["knob"][DEFAULT] = "O"` and must name `switch.knob` and the
  error rung.
- **inc50** — *the band is its content, and the schedule under it opens on a GATE HEADER.* Three clauses
  measured on the shipped `solari_S4.txt` against the shipped `solari_S1.txt`: depth is
  `1 + the rows that say something + 1` with no air between the first word and the closing seam; the row
  below the band is a header at its own index; every row outside the band is the page's row at the same
  index (inc40's second half, re-asserted, because a shrink implemented by INSERTING would satisfy the
  second clause and push the board down). Teeth restore the pre-inc50 body with the real six-row block and
  name `GATE DOING 04`, `FIX LOGIN REDIRECT` and the orphan seam, **with the band's HEAD asserted
  unmoved** — a length finding, not a re-run of inc40's anchor finding.
- **inc51** — *a stepper's halves are DIRECTIONS.* Two clauses over all eleven: no state may be another
  state with its halves exchanged (a symmetric pair has no handedness and cannot violate it), and
  `stepper.step[INVALID]` must be drawn from the cells that kit already spends on a rejected value at its
  `knob` and its `textfield`. **Both clauses are load-bearing and the teeth prove it**: five of the six
  turns go red on clause 1, and `nord ][` goes red on clause 2 alone — `[` and `]` are the button's walls
  and the checkbox's well, a pair the stepper never declares, so a law with the orientation clause alone
  would have left the BASE's own defect standing. A seventh arm (`≠≠`, a mark no kit declares) is clause
  2's own teeth.
- **inc51** — `OPENING_CONTROLS` gained `stepper`. inc39's ruling was right about ENCLOSURE and wrong
  about ANNOUNCEMENT: whatever cell stands first is what a reader meets first, whether it is a wall or an
  arrow.

### 12.3 The rosters, before and after

```
MEANING_AT_A_NAMED_SEAT      rework-3   inc49        MEANING_AT_AN_OPENER    rework-3   inc51
  naught                          8       12           naught                     2        3
  corgi                           8       16           corgi                     31       40
  prism                           8       16           prism                     19       25
  blueprint                       8       12           blueprint                  6       12
  darkside                        0        0 *         swiss                      0        0 **
  the other six                   0        0           nord                       0        0 **
                                                       the other five             0        0
```

`*` darkside read 0 only because the law was blind; it read **4** under the widened clause and was fixed
at its own declaration back to 0 — the grip ramp starts one rung up (`O ◎ ●` → `◎ ◉ ●`, `(O)` → `(◎)`),
on two cells this kit already declared, and **deliberately not on a geometric `○`**, which is the
homoglyph move the round documents five times in §0b/§4.

`**` swiss and nord stayed at zero through the stepper's arrival because **the bill inc48 §5 published in
advance was PAID rather than exempted**: swiss's `stepper.main` dead end takes `▫` (the lightest rung of
the one-shape ladder inc46 built it) and nord's takes `░` (the lightest rung of the shade ramp `Kit`
already owns).

**The four languages that grew on both rosters — naught, corgi, prism, blueprint — were already failing
both laws before this batch widened them.** Three of the four have never had an increment, which is
decision **A**; the fourth has no unspent cell, which §11.5 says in writing. Counted by name with their
reason, not fixed and not exempted.

### 12.4 The census, and the number that matters more

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

**48 → 36, and eleven of the twelve are inc51's.** `rework-3` moved the total by 6 across four
increments; the stepper's turns were worth 11 in one, because each turn made a cell carry
`INVALID stepper.step open` and `stepper.step close` at the same time. `nord` is now **1**, the cleanest
language in the corpus. `zero collisions: NONE` still holds for all eleven.

**Live meaning × meaning — the number §11.2 says the rule is actually about — falls 8 → 6.** Both closures
are inc51's: `prism ⡀` and `blueprint ├` were `REQUIRED` sharing a cell with an `INVALID stepper.step`,
two of the eight rows §11.2 noted *"every one of the eight left involves `INVALID`"*.

### 12.5 Frames changed, by name

| inc | frames (`.txt` + `.svg` unless said) | gallery |
| --- | --- | --- |
| 49 | `darkside_S2`, `darkside_S3` | `gallery_darkside` (2 of 22) — checked against the calendar trap of §10.3: the diff is the two knob rows, the moon doodle cell is unchanged |
| 50 | `solari_S4` | 0 of 22 |
| 51 | **none** | 0 of 22 |

**Three frames in the whole batch.** inc51 changed eight declarations across seven kits — two of them
`stepper.main[DEFAULT]`, the string every LIVE state of the ground falls back to — and not one of the 88
`.txt` moved, which is a stronger statement than the round's *"no frame renders an invalid stepper"*:
**no artefact in this repo draws a stepper at all.** (A stepper drawn only in DISABLED would escape that
argument; it is named in `inc51.md` §7 as the one hole in it.) `capture_languages.py`'s docstring claims
the component sheet carries *"and stepper, each in the states the registry derives"* — at 118×34 it is
cut off after the switch and checkbox rows. **So the stepper's law stands on the property test alone**,
stated rather than glossed.

**The skill's installed gallery frames 44–51: NONE changed byte-wise in this batch, and all eight are
currently byte-identical to their sources.** This batch's three moved frames (`darkside_S2`,
`darkside_S3`, `solari_S4`) are not the source of any of the eight. The five that §11.4 listed as stale
(45, 46, 48, 49, 50) carry an mtime of 2026-09-06 12:54, before this batch's first commit — **the manual
re-install §11.4 asked for was done outside this batch**, and it is recorded here rather than claimed.

### 12.6 What was NOT touched, by name

**Every item in `PROTOTYPE-inheritors-2.md` §6 is the operator's and none of them was decided:**

| | the question | this batch's contact with it |
| --- | --- | --- |
| **A** | corgi, prism and blueprint have never had an increment; 12 of the 66 frames are unjudged | **made their rosters bigger and more precise, fixed none of them** |
| **C** | `INVALID` takes the `DANGER_FORM` (inc39's ruling) | **applied a sixth and seventh time** (swiss `╲╲`, blueprint `━━`), because it is the ruling of record; if C is reverted those two lines revert with it |
| **D** | are diameter and rotation channels a language declares? | **inc49 refused a homoglyph move on that ground and said so at the seat** — it did not answer the question |
| **E** | `darkside_S1`: the rail, or the `.txt` stops being the work | untouched |
| **F** | may a solari confirm eat the gate it names? | **inc50 came within one design decision of it and stopped.** At 100×32 an overlay band at the head of the schedule cannot avoid `GATE BACKLOG 05`, because the gate header IS the schedule's first row; the three ways out are all design changes and `inc50.md` §4 names them |
| **G** | blueprint's first-fixation law is in a test and in no image | untouched |
| **C1** | `blueprint_S4`'s destructive control is built with `knockout_cell` instead of `button` | untouched — named in inc41 §8, in §10.6, in §11.3 and now here |

Also still open and outside this batch's scope: **K2** (the three laws compare code points and the
reader's channel is shape), **K4** (no law compares two states of one part), **L1–L6**, **C2**, **C4**,
**C5**, **C6**, **C7**, **E2** (the `.svg` carries no font metric, so no homoglyph objection can be
*resolved* from the artefact) and **E3** (`gallery_darkside` is calendar-dependent).

### 12.7 Found by looking

- **`capture_languages.py`'s docstring overstates the component sheet.** The one component all eleven
  declare is the one component nobody has ever seen rendered (§12.5).
- **`Darkside.tabs()` and `wordmark()` still print `(O)`** — the error rung marking the active tab, and
  the moon doodle at one of six phases — both drawn outside `PART_GLYPHS` where neither the census nor any
  of the four laws can reach them. The same limit §10.4 published for `▬`.
- **`Darkside.LEVELS`' own comment cites a `CUR` that moved in inc45** (*"a dimming ladder made of its own
  cursor. `CUR` is `O`"*; `CUR` has been `▊` since inc45).
- **inc49's blind spot was structural, not a typo.** `COMPONENT_PARTS` gives `switch` the same three parts
  as `slider` on purpose; the clause that named `indicator` was written from the word rather than from the
  registry. The rule's two other clauses (`dead`, and inc48's opener) are derived from the registry and
  were never wrong.
- **`solari_S4`'s ink went UP 4 points (22.8 → 26.8) while its modal got smaller** — density on this
  language measures board coverage, not modal size.
- **`test_win_clipboard_roundtrip` is environment-coupled** (§10.6) and was red at `a8a7a5d` before this
  batch began, in every run of all three increments. **Reported, not counted, not touched.**

### 12.8 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc49 · inc50 · inc51 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1040 → 1040 → 1042 → 1054 passed** (inc49 widened a law without adding a test function; inc50 +2; inc51 +12), the clipboard red throughout and named in every packet. `verify_language.py` **ALL PASSED** after every increment. `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` 66 of 66. `capture_languages.py` after every increment; **2 gallery artefacts moved in total**. `collision_census.py` self-check green after every increment; **TOTAL 48 → 36**. `export_to_skill.py` at the close: `2 written, 64 already identical`, re-run `0 written, 66 already identical`. **The skill repo was not committed.** |
| Notes | **2 source files across 3 increments, one agent** (`taskboard/language.py`, `tests/test_components.py`), plus 6 regenerated frame artefacts, 2 gallery artefacts, the census table, three packets and this section. **Every increment's law was watched failing BY HAND on the real declaration, with the output quoted verbatim in its packet**, in addition to its monkeypatched teeth. |

## 13. Batch `rework-5a` — three of the seven questions `PROTOTYPE-inheritors-2.md` §6 put to the operator

`rework-4` closed the three items that were defects on the record and left **every** §6 question
untouched — §12.6 is the table of what it did not decide. **The operator then delegated those decisions
to the orchestrator ("confío en tu juicio"), and this batch is three of them carried out: C, D and C1.
Three increments, one agent. The rulings are quoted verbatim in each packet's §0 and are reproduced here,
because a ruling that lives only in a chat is a ruling nobody can argue with later.**

### 13.1 The three rulings, as given

> **C — `INVALID` never takes `DANGER_FORM`.** "Does not parse" and "destroys data" are two meanings.
> inc39's rule ("where un-flipping collides, the walls take the language's DANGER_FORM") is revoked.
> Apply inc51's clause 2 to the text field: `textfield[INVALID]` walls and `stepper.step[INVALID]` draw
> from the cells the kit already spends on a rejected value at its knob (the declared invalid channel),
> never from `DANGER_FORM`, `LEVELS` or `REQUIRED`.

> **D — channels are count, weight, position and direction; diameter alone is not a channel.** Write it
> into the rule's docstring in `tests/test_components.py` and into `collision_census.py`'s header. Add a
> homoglyph table to the census so it flags a meaning mark whose homoglyph is chrome; print the rows it
> adds and fix the ones this ruling covers.

> **C1 — the destructive default answer is a button that carries the knockout.** Ruling 10 of 2026-09-04
> moved the knockout to the default answer; it did not say the default answer stops being a button.

The full text of each, with its by-name lists and its teeth clause, is in `inc52.md` §0, `inc53.md` §0 and
`inc54.md` §0 under the heading **"Ruling (orchestrator, 2026-09-06, on the operator's delegation)"**.

### 13.2 What each increment did

| inc | ruling | what moved | frames |
| --- | --- | --- | --- |
| 52 | **C** | **Ten declarations in four kits, and one kit's `DANGER_FORM` instead.** swiss `╲` → `║` (knob, field, stepper); blueprint `├`/`━` → `╱`; corgi `▀▄` → `░░`; instrument `⠸⠶⠇` → `⠶⠶⠶`; **darkside's `DANGER_FORM` `("Ø","Ø")` → `("▚","▞")`**, because that kit's own comment says the danger form took `Ø` FROM the invalid wall. `invalid` becomes the fifth family of the one-mark-one-meaning law; the opener law's now-groundless INVALID exemption is deleted. | `blueprint_S2` `corgi_S2` `instrument_S2` `swiss_S2` `darkside_S3` `darkside_S4` |
| 53 | **D** | The word **channel** is defined in both instruments. The census gains `HOMOGLYPHS` (five adjacent-size pairs), `homoglyph_rows()`, a `HOMOGLYPH_ROSTER` over all eleven and a second self-check. Five rows on first run; two fixed — swiss's chosen option `●` → `▪` and darkside's field leader `◦` → `▔`. The four accepted homoglyph moves are written into the table with the channel each spends. | `swiss_S2` `darkside_S1` `darkside_S3` `darkside_S4` · gallery `gallery_swiss` |
| 54 | **C1** | `Kit.button` gains a `knockout` keyword (**not** a composition — `mark()` would escape the button's own tags), one span over the whole seat. `Blueprint.knockout` moves up to `Kit` so ten languages can refuse. `screens.s4_blueprint` composes a button. New law over all eleven S4s, read off the shipped frames. | `blueprint_S4` |

### 13.3 The laws this batch added, widened or deleted

- **inc52 — `invalid` is a MEANING.** `_meaning_marks` gains a fifth family built by `_invalid_marks()`
  from `knob[INVALID]`, the two **WALLS** of `textfield.main[INVALID]` and `stepper.step[INVALID]`. **The
  RUNE is excluded by name and has its own test**: a field's glyph is *"wall, RUNE, wall"* and the rune is
  the paper the value lies on in every state, so counting it would have turned "what a field is made of
  here" into "your value is wrong". `DANGER_IS_THE_TOP_RUNG` survives and its scope is written down: it
  covers `danger` against `ladder` and nothing else, because a rung set as a form is a TIER of one
  declared channel and a rejection is not a tier of a destruction. **Teeth: ten parametrised arms, one per
  moved declaration, each naming the language and the two roles and holding the other ten still; an
  eleventh arm for darkside's restored `DANGER_FORM`; a twelfth for the rune exclusion in both
  directions.**
- **inc52 — one exemption DELETED.** `meaning_marks_at_an_opener`'s *"a field whose INVALID walls are that
  language's own `DANGER_FORM`"* had inc39's ruling under it and now has nothing. **Measured firing ZERO
  times before it was removed**, so the rosters are unchanged by the deletion and corgi's −2 is the
  declarations moving.
- **inc53 — the four channels, written into `tests/test_components.py`'s section head and
  `collision_census.py`'s module docstring**, each with the increment that spent it. `tier` is not one of
  the four and survives in exactly one place, by name: the `DANGER_IS_THE_TOP_RUNG` exemption.
- **inc53 — the homoglyph check is ASYMMETRIC** (one side a meaning, one side chrome), its rows are
  **never folded into the per-language counts**, and the pairs are **adjacent sizes only**: chaining
  `· ∙ • ●` into a transitive family was measured at **19 rows against 5** and refused.
- **inc54 — the destructive default answer.** *In every language's S4 the irreversible default answer
  carries this language's DANGER FORM, this language's FOCUSED WALLS, and — where the registry spends a
  knockout — the KNOCKOUT TIER over the whole seat, in the `.txt` and in the `.svg`.* Read off the shipped
  frames with a pattern built from the KIT's declarations, so it is not `screens.py` asserting that it
  equals itself. It **extends inc41's tier comparison**: inc41 asserts *declared == painted* over all 66
  frames as SETS; this asserts which run carries the ground and what is inside it.

### 13.4 The census, and the number the batch is about

```
language      rework-4   inc52   inc53   inc54            homoglyph rows (inc53 on)
naught             5        5       5       5               naught     2
corgi              5        5       5       5               darkside   1
instrument         5        4       4       4               ledger     1
swiss              3        2       2       2               the other eight  0
industrial         2        2       2       2               -----------------
nord               1        1       1       1               TOTAL      4
darkside           2        1       1       1
prism              4        4       4       4
ledger             2        2       2       2
solari             3        3       3       3
blueprint          4        4       4       4
--------------------------------------------
TOTAL             36       33      33      33
```

**And the number that matters more — PAIRS of meanings sharing a cell, with the four
`DANGER_IS_THE_TOP_RUNG` exemptions held aside — falls 8 → 0.** Measured with the law's own reader on
HEAD's ten strings and darkside's `("Ø","Ø")` put back:

```
before   corgi invalid×ladder ▄ · corgi invalid×required ▀ · instrument invalid×ladder ⠇
         swiss danger×invalid ╲ · darkside danger×invalid Ø
         blueprint danger×invalid ━ · blueprint invalid×ladder ━ · blueprint invalid×required ├
         ------------------------------------------------------------ 8 live, 4 exempt
after                                                                 0 live, 4 exempt
```

**After `rework-5a` no language has two meanings on one cell that the exemption does not cover. That is
the first time it has been true in the corpus.** The four that remain are `naught ∙`, `corgi █`,
`prism ⣿` and `blueprint ━` — the danger form as the ladder's TOP rung, each with the citation its kit
carries.

### 13.5 The rosters

```
MEANING_AT_AN_OPENER    rework-4   inc52          MEANING_AT_A_NAMED_SEAT   unchanged, all eleven
  corgi                     40       38             (knob[INVALID] is not a state `component_states`
  naught                     3        3              derives for a checkbox, a radio or a switch,
  prism                     25       25              so no knob seat moved)
  blueprint                 12       12
  the other seven            0        0
```

corgi's −2 is `▄▀·▀▄` (opening on the warn rung) and `▀▄▄▀` (opening on `REQUIRED`) moving onto the
ghost. **The three languages that have never had an increment still carry the three biggest rosters**,
which is decision **A** and is still open.

### 13.6 Frames, and what the skill holds

**Eight distinct frames moved across the batch** (`darkside_S4` twice, `darkside_S3` twice,
`swiss_S2` twice):

```
inc52   blueprint_S2  corgi_S2  instrument_S2  swiss_S2  darkside_S3  darkside_S4
inc53   swiss_S2  darkside_S1  darkside_S3  darkside_S4
inc54   blueprint_S4
```

**Gallery: 2 of the 22 — `gallery_swiss.{txt,svg}`**, the component strip's four radio rows. No board
draws an invalid field, a destructive button or a field row, which is why nothing else moved.

**The skill's installed gallery frames 44–51: ONE changed byte-wise —
`49_darkside-modal-rounded-lid.txt`, whose source is `darkside_S4`.** It is stale in TWO places at once:
the danger form (`ØDeleteØ` → `▚Delete▞`, inc52) and the six field-row leaders (`◦` → `▔`, inc53). The
other seven — `44_instrument-list-graticule`, `45_industrial-list-plate`, `46_swiss-list-next-column`,
`47_solari-list-gate-seam`, `48_industrial-modal-plate-lid`, `50_solari-form-printed-severity`,
`51_instrument-monitor-dot-ladder` — were compared byte for byte against their sources and are identical.

**And 49 was NOT re-installed by this batch, deliberately.** `export_to_skill.py` copies
`prototypes/gallery/*` into `assets/languages/` and does not touch `assets/gallery/` — that curated set
has always been installed by hand (§12.5 records the same for the five §11.4 listed). The batch's
constraint is *"the skill is edited only through `export_to_skill.py`"*, so the copy was not made.
**`49_darkside-modal-rounded-lid` is stale and somebody has to re-install it or teach the exporter that
directory.**

### 13.7 What was NOT touched, by name

| | the question | this batch's contact with it |
| --- | --- | --- |
| **A** | corgi, prism and blueprint have never had an increment | **edited corgi's and blueprint's invalid channels and judged no frame of either.** Their rosters are still the three biggest |
| **C** | `INVALID` takes the `DANGER_FORM` | **DECIDED — revoked (inc52).** inc51's two applications (swiss `╲╲`, blueprint `━━`) are reverted along with five others |
| **D** | are diameter and rotation channels a language declares? | **DECIDED — count, weight, position, direction; diameter alone is not one (inc53).** Rotation was NOT decided: the ruling names four channels and rotation is not among them, and inc39's field law already forbids orientation as the ONLY channel of a field's state while blueprint's radio spends it on purpose with a citation. **That half of D is still open** |
| **E** | `darkside_S1`: the rail, or the `.txt` stops being the work | **untouched, and inc53 stayed off the vertical stroke to keep it that way** — the ruling suggested `▏` for the field leader and inc48's measurement (16 → 22 vertical strokes on that very frame) is why `▔` was taken instead |
| **F** | may a solari confirm eat the gate it names? | untouched |
| **G** | blueprint's first-fixation law is in a test and in no image | **untouched, and inc54 made the knockout BIGGER** (8 cells → 12) without answering it |
| **C1** | `blueprint_S4`'s destructive control is built with `knockout_cell` | **DECIDED — it is a button now (inc54)** |

Also still open and outside this batch: **K2** (the laws compare code points — inc53's homoglyph table is
the first crack in it, and it is a table of code points too), **K4**, **L1–L6**, **C2**, **C4**–**C7**,
**E2** (the `.svg` carries no font metric, so no homoglyph objection can be *resolved* from the artefact)
and **E3**.

### 13.8 Found by looking

- **Ruling D reaches two LADDERS this batch did not touch, and it is the sharpest thing it leaves open.**
  swiss's button ladder is `▫ ▪ ■` (inc46: *"ONE SHAPE AT THREE WEIGHTS"*) and **industrial's SEVERITY
  ladder is `▫▫ ▪▪ ■■`** — one square at three DIAMETERS. LANGUAGES.md §3 says industrial's palette
  *"FAILS WHEN COLOUR MUST CARRY SEVERITY"*, so the square's size is all it has; ruling D says size alone
  is not a channel. **Both statements cannot be right.** No instrument here reaches it — a ladder is one
  declaration everywhere in this corpus — so the batch did not have to choose and did not.
- **`╳` is this corpus's DEAD mark and it was refused three times in inc52** (swiss, blueprint, corgi),
  where it was the obvious answer each time. `Kit` spends it at four disabled seats and corgi and nord
  re-declare it. Dead and refused are two claims — inc45 §7 refused `×` for nord on the same ground.
- **`field_row` is drawn outside `PART_GLYPHS` in all eleven**, so the census can reach none of the eleven
  field leaders. Only darkside's was named by a ruling; ten others are unmeasured by any instrument here.
- **`◦` was `LG.NA.OFF`, naught's own unlit pixel, on six rows of every darkside detail pane**, just
  outside `verify_language`'s *"naught's pixel pair is exclusive to naught on the board"* — which is
  scoped to the meter. A second, independent reason for inc53's move, found while writing its test.
- **The ruling's frame predictions were wrong twice in inc53** (`swiss S3/S6` and `darkside S1/S2`), and
  the call sites in `screens.py` explain both: `radio_group` is called only in `s2`, and `field_row` in
  `s1` (which `s4` overlays) and in `s3`'s danger-zone CAPTION.
- **There are now TWO ways to reverse a cell** — `knockout_cell` (the title block) and
  `button(knockout=True)` (a control) — and the difference between them is exactly the distinction inc54
  exists to draw. A caller who reaches for the wrong one gets C1 back, and only inc54's law is watching.
- **`test_win_clipboard_roundtrip` moved in BOTH directions this batch.** It was RED at `6970cac`, GREEN
  on every reported gate run, and RED once mid-inc54 between two green runs of the same tree. It drives
  the real Windows clipboard through PowerShell (§10.6). **Reported, not counted, not touched — and
  `1083 passed` is not evidence that it was fixed.**

### 13.9 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc52 · inc53 · inc54 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1054 → 1067 → 1070 → 1083 passed** (inc52 +12 tests +1 clipboard; inc53 +3; inc54 +13), the clipboard test named in every packet. `verify_language.py` **ALL PASSED** exit 0 after every increment. `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` 66 of 66, refusals `[]` for all eleven. `capture_languages.py` after every increment; **2 gallery artefacts moved in total**. `collision_census.py` **both** self-checks green after every increment; **TOTAL 36 → 33**, homoglyph rows **4**. `export_to_skill.py` at the close: `2 written, 64 already identical`, re-run `0 written, 66 already identical`. **The skill repo was not committed.** |
| Notes | **4 source files across 3 increments, one agent** (`taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`, `prototypes/components/screens.py`) — never more than 3 in one increment — plus 11 regenerated frame artefacts over 8 distinct frames, 2 gallery artefacts, the census table, three packets and this section. **Every increment's law was watched failing BY HAND on the real declaration or the real composition, with the output quoted verbatim in its packet**, in addition to its monkeypatched teeth. |

---

## 14. Batch `rework-5b` — three more of the questions `PROTOTYPE-inheritors-2.md` §6 put to the operator

`rework-5a` carried out C, D and C1 and left E, F and G untouched (§13.7). **The operator delegated the
remaining decisions to the orchestrator on 2026-09-06 ("confío en tu juicio"), and this batch is three
of them plus the hygiene four rounds had named and nobody had done: F and G as increments, E as a
ruling written at the seat, and D's addendum recorded. Three increments, one agent. The rulings are
quoted verbatim in each packet's §0 and are reproduced here, because a ruling that lives only in a chat
is a ruling nobody can argue with later.**

### 14.1 The rulings, as given

> **D, addendum.** Ruling D governs two *different meanings* that share a shape. A ladder is one meaning
> at monotone intensities and is one declaration: industrial's severity `▫▫ ▪▪ ■■` passes from hollow to
> filled (weight) and grows (size) in the same direction, so it stands. Swiss's button ladder `▫ ▪ ■`
> likewise. Rotation counts as a channel when it is direction the language already spends
> (opener/closer, up/down), not otherwise.

> **E.** For darkside the SVG is the artefact of record, not the txt; a darkside frame's grey step is a
> real signal. `darkside_S1` is not reworked on the txt's evidence. Write it into
> `MODAL_BORDER_REFUSED`'s neighbour comment or the kit docstring, and into
> `PROTOTYPE-inheritors-2.md`'s decisions section as "ruled".

> **swiss vs darkside resolved in opposite directions in inc52**: accepted as is; the earlier
> declaration in each kit won, and both kits say so.

> **F.** A confirm never covers the gate it names. The band is placed at the head of the first gate
> block the confirm does NOT name; if every gate is named or the page has one gate, the band goes to the
> foot of the schedule (above the plate's closing seam, if any). Implement in `Solari.overlay_instead`
> by reading the gate the modal text names, without parsing prose: `overlay` gains an optional `about=`
> the sheet fills, falling back to the head when absent, and every other language ignores it.

> **G.** The S2 fixture carries one alert-mood item for all eleven, so blueprint's first-fixation law
> (`├ OVERDUE ┤`, reverse on the `alert` mood) appears in a picture instead of only in a test.

The full text of each, with its by-name lists and its teeth clause, is in `inc55.md` §0 (D-addendum, E,
swiss-vs-darkside and F), `inc56.md` §0 (G) and `inc57.md` §0 (the hygiene brief), under the heading
**"Ruling (orchestrator, 2026-09-06, on the operator's delegation)"**.

### 14.2 What each increment did

| inc | ruling | what moved | frames |
| --- | --- | --- | --- |
| 55 | **F** (+ **E** written, **D-addendum** recorded) | `Kit.overlay` gains `about=`, filled by the sheet from a new fixture constant `MODAL_ABOUT` (the column as DATA, so no kit parses the fixture's English) and ignored by ten languages; `Solari.band_head` / `gate_of` / `schedule_foot` place the band at the head of the first gate the confirm does not name. **inc50's clause 2 changes ends** and the cost is declared. Ruling E written at `Darkside.pane_split_instead` and marked **RULED** in the round's §6. | `solari_S4` |
| 56 | **G** | `fixture.MOOD` DERIVED from the fixture's own tasks (it has had an overdue one since it was written) and handed over by `screens.s2`. `GROUNDED_FRAMES` 15 → 16. **S2 only, for an arithmetic reason: an alert mood on S4 would light the title block as well as the confirm's `DELETE` and break operator ruling 10's own condition.** | `blueprint_S2` |
| 57 | the hygiene four | `Kit.FIELD_LEAD` (eleven field leaders, four of them AIR by commitment) and `Kit.IDENT_GLYPHS` (darkside's moon and active tab) declared and READ BY THE CENSUS; darkside's `(O)` moved onto its own grip ramp; the `LEVELS` comment corrected; `capture_languages.py`'s stepper claim corrected. | `darkside_S1`–`S6` |

**7 source files across 3 increments, one agent** — `taskboard/language.py` (55, 57),
`prototypes/components/screens.py` (55, 56), `prototypes/components/fixture.py` (55, 56),
`tests/test_components.py` (all three), plus `prototypes/collision_census.py`,
`prototypes/capture_languages.py` and `prototypes/verify_language.py` in inc57 — never more than 5 in
one increment.

### 14.3 The laws this batch added or changed

- **inc55 — a confirm never covers the gate it names.** Asked TWICE: off the shipped frame (the named
  gate's whole BLOCK byte-identical, and no index of it inside the band) and **of the mechanism, once
  per gate on the page**, which is what stops the first reading being a lucky fixture. The gate's name
  is **intersected, not parsed** — the gates the page declares are a set, the words the band says are a
  string, and exactly one member of the first appears in the second. Teeth: the old anchor restored,
  naming `GATE BACKLOG 05`, `AUDIT THE THEME TOKENS` and `DROP THE LEGACY SHIM`; the `about=None`
  default asserted rather than trusted; and the foot fallback, **which no frame in this repo reaches**,
  exercised on a synthetic one-gate page.
- **inc55 — inc50's clause 2 CHANGED ENDS, and it is written down in the test.** *"The row immediately
  BELOW the band is a gate header"* became *"the row the band STARTS on is a gate header"*. Both are the
  same sentence read from opposite ends; inc50 could only assert the foot because the band stood at the
  schedule's head. **The declared cost: the band's foot now lands inside the gate it moved onto, so the
  row under it is a departure's orphan seam again — the defect inc50 removed, one gate lower.** Named in
  `inc55.md` §6, in `Solari.overlay_instead`, in the test docstring and in the round's §6 F, with the
  operator's two one-line alternatives.
- **inc56 — blueprint's first fixation is painted on the form.** Exactly one ` on ` tag on
  `blueprint_S2`, it is the state cell, the `.txt` reads `├ OVERDUE ┤`, and the `.svg` paints a rect of
  the kit's INK with the text inside it in the kit's GROUND — matched **at the rect's own x**, because
  the state cell is the fourth thing on that row. **It extends inc41's tier comparison the way inc54
  did**: inc41 asserts declared == painted as SETS, this asserts which run carries the ground and what
  is inside it. Teeth patch the FIXTURE and not the kit, because the finding is that nobody ever WROTE
  to `Kit.mood`; the other ten are asserted byte-identical either way.
- **inc57 — a field row draws exactly the leader it declares**, over all eleven, with the caller's words
  subtracted in all three registers. **A constant nothing checks is a comment.** Watched fail by hand on
  a real drift: `('darkside', {'▁'}, '▔')`.
- **inc57 — the census reaches every mark declared outside the glyph tables.** Its teeth are the
  counterfactual: the old identity alphabet put back takes darkside from 1 colliding cell to 3 and the
  census TOTAL from 33 to **35**, with `severity` and `identity` named on both `o` and `O`.

### 14.4 The census, and the number that matters more

```
language      rework-5a   inc55   inc56   inc57        homoglyph rows
naught             5         5       5       5           naught     2
corgi              5         5       5       5           darkside   1
instrument         4         4       4       4           ledger     1
swiss              2         2       2       2           the other eight  0
industrial         2         2       2       2           ------------------
nord               1         1       1       1           TOTAL      4
darkside           1         1       1       1
prism              4         4       4       4
ledger             2         2       2       2
solari             3         3       3       3
blueprint          4         4       4       4
--------------------------------------------
TOTAL             33        33      33      33
```

**Flat, and that is a finding rather than the absence of one.** inc55 and inc56 are composition
increments and changed no declaration. inc57 changed what the census can SEE without changing what any
language MEANS: four existing rows gained a `field.leader` family (`naught ◦`, `prism ⡀`, `ledger ·`,
`blueprint ·`), two languages' B×B alphabet counts grew (instrument 12 → 14, blueprint 8 → 9), and **no
new collision was revealed in a language already touched by rework.** The one candidate — ledger's dot
leader sharing a cell with the field's RUNE — is the exclusion `inc52.md` §0 wrote by name, so nothing
moved on that ground. The other three are `5c`'s.

**And the instrument itself was measured: `IDENT_GLYPHS` reads 35 under the counterfactual.** Declaring
darkside's identity alphabet WITHOUT moving it adds two rows, `o` (warn × identity) and `O`
(error × identity). That is the first time in this worktree the census has been shown catching a defect
it could not previously see, on the real declaration, with both numbers printed.

### 14.5 Frames, and what the skill holds

**Eight distinct frames moved across the batch, and every one of them by a single row:**

```
inc55   solari_S4        the band leaves GATE BACKLOG 05 and takes GATE DOING 04's head
inc56   blueprint_S2     ├ CLEAR ┤ -> ├ OVERDUE ┤, knocked out
inc57   darkside_S1 S2 S3 S4 S5 S6      (O)mode -> (●)mode, the active tab
```

**Gallery: 1 of the 22 — `board_darkside`**, the same mode strip. **`gallery_darkside` did NOT move,
and the reason is E3**: the moon doodle is `PHASES[day % 6]`, today is day 6, and `PHASES[0]` is `"( )"`
in the old alphabet and in the new one alike. On 29 days in 30 it would have moved. **E3 is alive and
this batch is its second measurement.**

**The skill's installed gallery frames 44–51: ONE changed byte-wise —
`49_darkside-modal-rounded-lid.txt`, whose source is `darkside_S4`.** It was already stale from
`rework-5a` (§13.6: the danger form and the six field-row leaders) and is now stale in a third place,
the active tab. The other seven — `44_instrument-list-graticule`, `45_industrial-list-plate`,
`46_swiss-list-next-column`, `47_solari-list-gate-seam`, `48_industrial-modal-plate-lid`,
`50_solari-form-printed-severity`, `51_instrument-monitor-dot-ladder` — were compared byte for byte
against their sources at the close and are identical.

**49 was NOT re-installed, deliberately and for the third batch running.** `export_to_skill.py` copies
`prototypes/gallery/*` into `assets/languages/` and does not touch `assets/gallery/`; the batch's
constraint is *"the skill is edited only through `export_to_skill.py`"*. **Somebody has to re-install it
by hand or teach the exporter that directory.**

### 14.6 What was NOT touched, by name

| | the question | this batch's contact with it |
| --- | --- | --- |
| **A** | corgi, prism and blueprint have never had an increment | **untouched, and made two of their census rows wider** (inc57's field leaders). Their rosters are still the three biggest |
| **D** | are diameter and rotation channels? | **the addendum is recorded and it needed no code**: the census's `HOMOGLYPHS` check is ASYMMETRIC (one side a meaning, one side chrome), so two rungs of one ladder can never produce a row — the addendum's own prediction, and `▪ ■` sits in the table scoring zero. The ROTATION half closes for the same reason: `DIRECTION` was already one of the four channels the census's header names |
| **E** | `darkside_S1`: the rail, or the `.txt` stops being the work | **DECIDED — the `.svg` is the artefact of record for this language (inc55)**, written at `Darkside.pane_split_instead` and marked RULED in the round. What it does NOT close is written with it: the rail's fourteen strokes, and E2 |
| **F** | may a solari confirm eat the gate it names? | **DECIDED — no (inc55)**, with inc50's clause 2 changing ends as the declared cost |
| **G** | blueprint's first fixation is in a test and no image | **DECIDED — it is in `blueprint_S2` now (inc56)**, and the ruling's frame count was not met: ONE S2 frame moved, not eleven |
| **C1**, **C**, **K1**, **K3**, **C3** | | closed in `rework-4` and `rework-5a` |

Still open and outside this batch: **K2** (the laws compare code points), **K4**, **L1–L6**, **C2**,
**C4**–**C7**, **E2** and **E3**.

### 14.7 Found by looking

- **RULING G'S FRAME PREDICTION WAS WRONG AND THE REASON IS THE BIGGER FINDING.** It expected eleven S2
  frames; one moved. `self.mood` is read at exactly two places in `taskboard/language.py` —
  `Naught.face` and `Blueprint._state_cell` — and naught's reaches a frame only through `mascot()` →
  `Kit.empty_state()`, which S2 does not compose. **Nine of the eleven languages have no board-wide
  channel at all.** Measured by setting the mood globally in a probe: seven of the 66 frames move
  (`blueprint_S1`–`S6` and `naught_S6`), and `naught_S2` is not among them.
- **A global alert mood would break operator ruling 10.** `blueprint_S4` would carry the title block's
  knockout AND the confirm's. The arithmetic that makes ruling 10 legal is a property of the fixture
  being calm, and it has now been measured rather than assumed.
- **`Darkside.SPIN = (".", "o", "O", "o")` is inc57's collision one family over**, and no language's
  `SPIN` is censused. Defensible — a spinner is motion — and a decision nobody has made in writing.
- **`prototypes/widget_slice/app.py` has never been edited by any batch in this worktree**, and it is
  where the component sheet's contents are decided. The stepper is composed there and photographed
  nowhere, which is what `capture_languages.py`'s docstring was really claiming.
- **`verify_language` caught something the pytest suite could not, for the third time.** Its `. o O`
  check went red on inc57's real change; the law was not deleted but told where the doodle went, and
  the spinner keeps that family.
- **`solari_S4`'s ink went UP for the third increment running** while the modal moved (22.8 → 26.8 →
  29.4). Density on this language measures board coverage, which is now a habit rather than an
  observation.
- **`test_win_clipboard_roundtrip` moved in both directions again.** Green through all of inc55 and the
  inc56 gate run, RED in the identical re-run of the same tree after inc56's watch-it-fail restore, and
  RED in both full-suite runs of inc57. It drives the real Windows clipboard through PowerShell (§10.6).
  **Reported, not counted, not touched — and `1100 collected` is not a claim about it either way.**

### 14.8 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc55 · inc56 · inc57 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1083 → 1086 → 1088 → 1100** (inc55 +3, inc56 +2, inc57 +12), with the clipboard test red in inc57's runs and named in every packet. `verify_language.py` **ALL PASSED** exit 0 after every increment — and RED first in inc57, on its own `. o O` law, reported rather than skipped. `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` 66 of 66, refusals `[]` for all eleven. `capture_languages.py` after every increment; **1 gallery artefact moved in total**. `collision_census.py` both self-checks green after every increment; **TOTAL 33 → 33**, homoglyph rows **4**, and **35 under the counterfactual**. `export_to_skill.py` at the close: `2 written, 64 already identical`, re-run `0 written, 66 already identical`. **The skill repo was not committed.** |
| Notes | **7 source files across 3 increments, one agent** (`taskboard/language.py`, `prototypes/components/screens.py`, `prototypes/components/fixture.py`, `tests/test_components.py`, `prototypes/collision_census.py`, `prototypes/capture_languages.py`, `prototypes/verify_language.py`) — never more than 5 in one increment — plus 16 regenerated frame artefacts over 8 distinct frames, 2 gallery artefacts, the census table, the round's decisions section, three packets and this section. **Every increment's law was watched failing BY HAND on the real declaration or the real composition, with the output quoted verbatim in its packet**, in addition to its monkeypatched teeth. |

---

## 15. Batch `rework-5c` — decision **A**: the five languages that never had an increment

`rework-5a` and `rework-5b` carried out six of the seven questions `PROTOTYPE-inheritors-2.md` §6 put
to the operator and left **A** untouched twice, each time widening it (§13.7, §14.6). **The operator
delegated the remaining decisions to the orchestrator on 2026-09-06 ("confío en tu juicio"), and this
batch is A: five increments, one language each, guided by the three laws. One agent. The ruling is
quoted in each packet's §0 and reproduced here, because a ruling that lives only in a chat is a ruling
nobody can argue with later.**

### 15.1 The ruling, as given

> **A — the five languages that never had an increment get one each, guided by the laws.** Each
> increment ends with that language's rosters at zero or with every remaining row exempted by name and
> citation.

And the brief's own instruction, which decided the shape of every increment:

> …or whether the language's answer is a by-name exemption for the whole ramp as
> `DANGER_IS_THE_TOP_RUNG` already is: **but an exemption must leave the opener of a control distinct
> from an error rung in the frame, so measure the frames before deciding.**

**The blanket exemption was drafted twice and the FRAME refused it both times**, which is this batch's
method in one sentence:

| language | the measurement that refused it |
| --- | --- |
| corgi | `corgi_S3` draws `██` as the SLIDER'S KNOB twelve rows above `▁▁█Delete all█▁▁`; `corgi_S2` draws `██` as the error message's own leader three rows under `██ ON ui`, a CHECKED checkbox |
| naught | `naught_S3` renders every live switch as `∙∙◉` — the composer draws that track TWO cells wide, so `∙∙` is `LEVELS["error"]` and the `DANGER_FORM` byte for byte, twelve rows above `◦ ∙Delete all∙ ◦` |

### 15.2 What each increment did — and it was the SAME defect four times

**Every one of the four languages had TWO registers and had never said which was which.** Three of the
four already carried the sentence in their own kit, applied to ONE part and to no other.

| inc | language | the ruling, in the kit's own terms | the sentence it widened |
| --- | --- | --- | --- |
| 58 | **corgi** | **The bank is the reading, the panel is the metal.** The four DRIVEN heights (`▁ ▄ ▀ █`) carry the meanings; the shade ramp and the quadrants carry every control | `field_row`: *"the frontier is the two REGISTERS — engraved aluminium against driven glass"* |
| 59 | **prism** | **The ember is read from the bottom; a control is read from the top.** The same four dot-rows at the opposite POSITION in the cell, stopping one row short of `⣿` by construction | `knob`: *"every state is a BROKEN field … precisely so the knob can never be mistaken for a full cell of fire"* |
| 60 | **blueprint** | **The terminators are chrome and nothing else; a meaning is a LINE TYPE.** Obligation left `├` for a doubled run; every dead run left the warn rung for a finer dash count | — (the kit argued the opposite, and `inc60.md` §1 overturns it with the frame) |
| 61 | **naught** · **ledger** | **The lattice counts; the pixel charges.** `NA.ON` belongs to the count; the switch's live track is scoped and obligation leaves the charge ramp. ledger stops banking its paper up BY SIZE | §0: *"how many are lit is the signal"* |

**Three source files across five increments, one agent** — `taskboard/language.py` (all five),
`tests/test_components.py` (all five), `prototypes/collision_census.py` (inc61). Never more than 3 in
one increment.

### 15.3 The rosters — and the first clean sweep in this corpus

```
MEANING_AT_AN_OPENER      067400c  inc58  inc59  inc60  inc61
  corgi                       38      0      0      0      0
  prism                       25     25      0      0      0
  blueprint                   12     12     12      0      0
  naught                       3      3      3      3      0
  the other seven              0      0      0      0      0
  ----------------------------------------------------------
  TOTAL                       78     40     15      3      0

MEANING_AT_A_NAMED_SEAT
  corgi                       16      0      0      0      0
  prism                       16     16      0      0      0
  blueprint                   12     12     12      0      0
  naught                      12     12     12     12      0
  ----------------------------------------------------------
  TOTAL                       56     40     24     12      0
```

**All eleven languages are ZERO on both seat rosters, and it is the first time in this corpus.** The
three laws pass **11 of 11 each** — 33 parametrised arms — and two exemptions carry it, both by name
and both with a citation:

| exemption | scope | since |
| --- | --- | --- |
| `DANGER_IS_THE_TOP_RUNG` | `danger` × `ladder`, four languages (`naught ∙∙`, `corgi ██`, `prism ⣿⣿`, `blueprint ━━`) | inc45, untouched |
| `THE_GROUND_IS_NOT_A_MARK` | naught's `NA.OFF` at the two seat laws only | **inc61 — and it is `BLANKS` extended, not the rule bent** |

**The second is the argument `MEANING_AT_AN_OPENER`'s comment carried unresolved from inc48**, which
said in writing *"an exemption is the operator's, and silence is not one"*. Ruling A is the authority
it was waiting for. **And it is PRICED**: emptying it on the shipped kit reads `(7 openers, 2 named
seats)`, asserted as `GROUND_EXEMPTION_IS_WORTH`, so a later increment that leans more weight on it
has to edit that line. **Five of those seven are inc61's own doing** — retiring `·` pushed
`stepper.main`'s live rail onto `◦◦` — so without the exemption naught would read 7, worse than the 3
it started at. That number is in the packet, in the constant and in a test.

### 15.4 The census

```
language      rework-5b   inc58   inc59   inc60   inc61        homoglyph rows
naught             5        5       5       5       4            naught  2 -> 0
corgi              5        2       2       2       2            ledger  1 -> 0
instrument         4        4       4       4       4            darkside     1
swiss              2        2       2       2       2            ----------------
industrial         2        2       2       2       2            TOTAL   4 -> 1
nord               1        1       1       1       1
darkside           1        1       1       1       1
prism              4        4       2       2       2
ledger             2        2       2       2       2
solari             3        3       3       3       3
blueprint          4        4       4       2       2
--------------------------------------------------
TOTAL             33       30      28      26      25
```

**Two costs are declared rather than absorbed, and the instrument printed both itself.** corgi's,
prism's and naught's SWITCHES were scoped away from the slider's tables, so the base `main` /
`indicator` are now reached by the slider and the bar alone — which the census excludes from its B set
**by the operator's own request**. The census's own last line says what that hid:

```
corgi   "... N further cells would collide if slider/bar/scrollbar were in the B set"   1 -> 3
prism                                                                                   0 -> 2
blueprint                                                                               0 -> 1
```

`▁` and `▄` are still corgi's info and warn rungs and still its slider's shaft and fill; `⣀` and `⣿`
are still prism's; `╌` is still blueprint's scroll-bar break. **Named in three packets so the drop
from 33 to 25 is not read as more cells moving than moved.** It is also doctrinally deliberate: in all
three languages a QUANTITY is a READING, so it belongs on the reading's register.

### 15.5 What is left, and it is ONE function

**The RUNE of the field is the last remaining census row in FIVE languages** — naught `⋅`, corgi `·`,
blueprint `·`, ledger `·`, solari `·`. `_invalid_marks` excludes it by name since inc52 (*"a field's
glyph is wall, RUNE, wall and the rune is the PAPER the value lies on in every state"*); the census
counts it. **The two instruments have disagreed about the rune since inc52, and this batch named the
disagreement in three separate packets before deciding not to close it**: it is one function in
`collision_census.py`, and closing it drops five languages' counts at once for a reason that is *the
reader changed*, which deserves its own increment and the operator's eye.

The other rows still standing, all named: the four `DANGER_IS_THE_TOP_RUNG` cells; `CUR` against
chrome in naught (`●`), ledger (`▶`), instrument (`⣿`) and solari; naught's `◦` ground (exempt at the
laws, counted by the census on purpose — its own header calls a row *a question*); and prism's
`REQUIRED` against its field leader, **exempted with a citation the increment itself argues against in
writing** (`prism_S1` draws that leader on six rows that are neither compulsory nor empty).

### 15.6 Frames, gallery and the skill

**Seventeen distinct component frames moved:**

```
inc58   corgi_S2 S3 S4 S6              · gallery_corgi   · gallery_darkside (E3, below)
inc59   prism_S2 S3 S4 S6              · gallery_prism
inc60   blueprint_S2 S3 S5 S6          · gallery_blueprint
inc61   naught_S2 S3 S6 · ledger_S2 S6 · gallery_naught · gallery_ledger
```

**`gallery_darkside` moved in inc58 and it is E3 firing for the first time in this worktree.** The
moon doodle is `PHASES[date.today().day % 6]`; the calendar day rolled 6 → 7 mid-session, `PHASES[0]`
is `"( )"` and `PHASES[1]` is `"(◎)"`, and the diff is that one cell on that one row. §14.5 predicted
it in writing — *"On 29 days in 30 it would have moved. E3 is alive and this batch is its second
measurement"* — and this is its **third measurement and its first actual fire**. No darkside
declaration was touched by this batch.

**The skill's installed gallery frames 44–51: ONE differs byte-wise, `49_darkside-modal-rounded-lid`,
and NOT for a reason this batch created.** All eight sources were compared byte for byte at the close
and `git log 067400c..HEAD` confirms **none of the eight moved during `rework-5c`**. 49 has been stale
since `rework-5a` (§13.6: the danger form and the six field-row leaders) and gained a third staleness
in `rework-5b` (§14.5: the active tab). **It is stale for the fourth batch running, and somebody has
to re-install it by hand or teach `export_to_skill.py` that directory.**

`export_to_skill.py` at the close: **`12 written, 54 already identical`**, re-run **`0 written, 66
already identical`**. The 12 are this batch's ten gallery artefacts plus `gallery_darkside`'s two;
`board_darkside` and `gallery_swiss` also show modified against the skill repo's HEAD because **the
skill repo has not been committed since `rework-5a`** and carries those batches' writes too. **The
skill repo was not committed.**

### 15.7 Found by looking

- **`verify_language` caught what the pytest suite could not, THREE MORE TIMES, and twice it wrote the
  fix.** inc59: prism's first stepper answer spelt `⠐`, a CLOSED counted seat whose check asserts
  exactly three occurrences in the package — and then the COMMENT explaining the first red went red
  too, because that law counts comments, which is what its own text says it does. inc60: sending every
  blueprint dead run to one mark collapsed the switch's dead TRACK into its dead INDICATOR, four
  failures at once, and the split into TWO dead runs is the law's answer rather than a preference.
  **The law was never narrowed** — its own comment forbids it (*"the fix for a red is never to narrow
  the law that found it"*) — and `verify_language.py` was not edited in any of the five increments.
- **AN EXCLUSION WHOSE TEETH DEPEND ON A DEFECT BEING PRESENT DIES THE DAY THE DEFECT IS CURED, AND IT
  DIES GREEN.** `test_the_rune_is_excluded_from_the_invalid_channel_by_name` rode on blueprint's rune
  being `·` while `LEVELS["info"]` was `··`. inc60 sent that info rung to air and **the corpus now has
  no language left whose rune is a meaning** — measured, all eleven, and asserted in the rebuilt test,
  which patches the meaning in rather than borrowing one.
- **A TEETH ARM CAN PASS FOR THE WRONG REASON AFTER A LATER CURE.** inc52's blueprint-knob arm restores
  `├` and asks for `("required","invalid")`; with obligation moved to `═` it collided with nothing and
  went green. `INVALID_CHANNEL_BEFORE` gained a fifth field so the arm restores the whole pre-inc52
  state. **inc51's arm over the same declaration did NOT break**, because it is about ORIENTATION and
  is blind to what the cell means — two teeth tests over one seat, and only one of them noticed.
- **THE OPENER LAW HAS A HOLE THE WIDTH OF A ONE-CELL GLYPH.** `if len(glyph) < 2: continue` — a
  language that draws its controls in SINGLE cells is invisible to it. prism's `switch.main` was
  `LEVELS["info"]` and scored ZERO on both rosters; it moved under the ruling, not under a law. The
  exclusion is defensible (a one-cell glyph has no first cell distinct from itself) and is now
  measured rather than assumed.
- **A ONE-CELL GRIP MARK IS NOT A FIFTEEN-CELL PAPER, and the same mistake was made and caught twice in
  one increment.** inc61's first answers for naught's and ledger's EDITED field paper were each that
  kit's own EDITED mark (`◍`, `◆`) — correct at a knob, and a wall of filled circles or diamonds across
  the whole measure on the rendered row. Both were caught by looking at the frame, not at the table.
- **THE PREDICTION IN A TEETH CONSTANT WAS WRONG ONCE AND IS RECORDED AS WRONG.** inc60's
  `BLUEPRINT_TABLES_WORTH` was drafted `(0, 0)` on the reasoning that restoring the chrome alone would
  light nothing. It scores `(1, 8)`: inc60 left `LEVELS["warn"]` where it was and moved the DEAD RUNS
  off it, so the dead datums light the named-seat law with no meaning restored at all.
- **FOUR LANGUAGES DRAW MARKS NO INSTRUMENT IN THIS REPO CAN SEE**, and each was named rather than
  quietly fixed: `Corgi.PANE_RULE = "█"` (the danger form, sixteen cells down `corgi_S1`),
  `Corgi.DISCLOSE` / `LIT` (`▄`, the warn rung), `Blueprint.ERROR_FILL = "╌"` (the WARN rung ruling the
  ERROR row out to the margin — two severities on one row of `blueprint_S2`), `Blueprint.REG`, and
  `Prism.SPIN` (the whole ember ramp, both meaning rungs, breathing once a frame). All are constants
  outside `PART_GLYPHS` — the blind spot inc57 closed for `FIELD_LEAD` and `IDENT_GLYPHS` and did not
  close for these. **`Blueprint.ERROR_FILL` is the sharpest of them.**
- **`HANDED_FIELDS` GREW AND NOBODY DECIDED IT — the derivation noticed.** corgi's field walls were a
  bank at a height and a bank has no hand; they are the engraved key's two SHOULDERS now, mirror images
  by construction, so the invalid-walls law can fire on corgi for the first time. It passes. Same
  event, and the roster's comment says the same words, as swiss in inc46.
- **A LANGUAGE'S OWN MARK COUNT CAN BE WRONG IN ITS OWN DOCSTRING.** blueprint said TEN and was drawing
  eleven — `┄` had been at `indicator[DISABLED]` all along and the list had never noticed. With inc60's
  two additions the count is TWELVE and the docstring says so; neither addition is a vertical or a
  junction, so *"a containing box here is unconstructable"* survives, which is the whole reason they
  were affordable.
- **`test_win_clipboard_roundtrip` was RED in every gate run of all five increments**, including the
  baseline at `067400c`. It drives the real Windows clipboard through PowerShell (§10.6). **Reported,
  not counted, not touched — and `1111 passed` is not a claim about it either way.**

### 15.8 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc58 · inc59 · inc60 · inc61 |
| Phase C (close) | inc62, this section |
| Gates | `pytest -q` **1099 → 1101 → 1103 → 1106 → 1111 passed** (+2, +2, +3, +5), the clipboard test red in every run and named in every packet. `verify_language.py` **ALL PASSED exit 0 after every increment — and RED FIRST in inc59 (twice) and inc60 (four checks at once)**, reported rather than skipped, fixed in the kit and never by narrowing the law. `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` 66 of 66, refusals `[]` for all eleven. `capture_languages.py plain` after every increment, 22 grids identical across two processes each time; **12 gallery artefacts moved in total.** `collision_census.py` both self-checks green after every increment — **and the homoglyph self-check went RED first in inc61**, on the roster it exists to protect. **TOTAL 33 → 25**, homoglyph rows **4 → 1**. `export_to_skill.py` at the close: `12 written, 54 already identical`, re-run `0 written, 66 already identical`. **The skill repo was not committed.** |
| Notes | **3 source files across 5 increments, one agent** (`taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`) — never more than 3 in one increment — plus 24 regenerated component artefacts over 17 distinct frames, 12 gallery artefacts, the census table, the round's decisions section, five packets and this section. **Every increment's law was watched failing BY HAND on the real declaration, one at a time, with the per-declaration counts quoted verbatim in its packet**, in addition to its monkeypatched teeth. |

---

## 16. Batch `rework-6a` — the first four items of `PROTOTYPE-inheritors-3.md`

`PROTOTYPE-inheritors-3.md` (2026-09-07, at `abd5193`) judged **all 66 frames for the first time** and
returned **keep 15 · note 40 · rework 11**, with eight new objections (K5, L7–L10, C8–C10, E4) and six
disagreements with standing rulings. **The operator delegated the decisions to the orchestrator, and
this batch is four of them: E4, F amended, C8 and C2 with ruling C's follow-through. Four increments,
one agent. The rulings are quoted verbatim in each packet's §0 and are reproduced here, because a ruling
that lives only in a chat is a ruling nobody can argue with later.**

### 16.1 The rulings, as given

> **E4:** the exporter reads the kit's declared `ground` and `ink`; it never infers them from frequency.

> **F, amended:** the band never covers a gate HEADER row, of any gate; it covers task rows of the first
> gate the confirm does not name, below that gate's header, and goes to the foot of the schedule when no
> such rows exist. A frame must never show a task under a gate it does not belong to.

> **G vs ruling 10:** on S4 the fixture mood is calm; G applies to S2 only. Recorded, no code.

> **inc60 info to air:** doctrine for blueprint and ledger (a line-type ladder where absence is the calm
> state, LANGUAGES.md §11 and #9). Recorded, no code.

> **C, follow-through:** the channel C freed on swiss gets filled: the invalid text field has a wall,
> paper and a closer from swiss's own alphabet.

**Two of the five are RECORDED AND NOT IMPLEMENTED, on purpose.** *G vs ruling 10* settles §7.4 of the
round — the two rulings cannot both bind on S4, and the answer is that the fixture's S4 mood is calm so
G binds on S2 alone; nothing in the code had to move for that to be true, and `screens.s4` was measured
to confirm it. *inc60 info to air* settles §7.5 — `LEVELS["info"]` being air in blueprint and ledger is
doctrine (a line-type ladder in which ABSENCE is the calm state), not a defect inherited from an unjudged
frame. Both are here so that the next round argues with a written ruling instead of re-opening them.

### 16.2 What each increment did

| inc | ruling | what moved | frames |
| --- | --- | --- | --- |
| 63 | **E4** | `cell_grid(app, ground)` takes the kit's declared `THEMES[lang]["ground"]`; the frequency count is deleted and `write()` raises rather than guess. `render.py` and `sweep_surfaces()` declare the ground in the Screen CSS, BEFORE compose — a background assigned after the first paint never reaches the strips the compositor has cached. | **all 66 `.svg`**, 0 `.txt`, 0 gallery |
| 64 | **L8, L9** | prism's `checkbox.main` / `checkbox.knob` centres swapped (ticking a box added ink for the first time in this kit); `_meter_ember`'s bitmap loop flipped so the DONE side is the fire. | `prism_S1` `prism_S2` · gallery `board_prism` `gallery_prism` |
| 65 | **F amended, C8** | `Solari.band_head` anchors one row BELOW the first unnamed gate's header and checks the next header's index before taking a gate; `Corgi.overlay_instead` keeps `under[0]`. inc40's head law loses its exemption and is asked of all eleven. | `solari_S4` `corgi_S4` · 0 gallery |
| 66 | **C2, C follow-through** | ledger's `button.main` FOCUSED `▶  │` → `▶  ◀` and ACTIVE `▶  ◀` → `▶──◀`; `Swiss.overlay_instead` closes its band on a second rule; swiss's `textfield.main[INVALID]` `"║  "` → `"║┆║"`. | `ledger_S4` `swiss_S2` `swiss_S4` · gallery `gallery_ledger` |

### 16.3 The laws this batch added and the ones it repaired

**Added — six laws and six teeth, all over all eleven:**

- **inc63 — the canvas is the kit's declared ground.** Three clauses over the 66 `.svg`: the canvas rect
  equals `THEMES[lang]["ground"]`; `contrast(ink, ground) >= 4.5` (WCAG 1.4.3, computed in the test from
  the two hexes); and **once every background run is subtracted, no colour has more area left than the
  declared ground** — the clause that stops the first one being satisfied by a full-bleed repaint. Teeth
  on the real bytes of `ledger_S6.svg`, both failure shapes.
- **inc64 — a ticked box is never lighter than an empty one** (L8), measured on the BOX and not the
  control (three kits spend a word at `check_label` and counting it makes the law measure how long the
  English is), and only on the cells that move (the walls are identical between the two tables in every
  language). `>=`, because naught ticks by SHAPE at equal weight.
- **inc64 — a language's fill direction is one declaration** (L9), at the meter, the slider and the
  readbar, each rendered at its floor and its ceiling. Two skips, written down as
  `RAMPLESS_METERS`: solari (`odometer` — quantity is digits) and blueprint (`dimension`), and the law
  **asserts they are still unweighable** so a third arrival goes red.
- **inc65 — no departure is filed under a gate it is not in** (F amended), over `solari_S4` and over
  `solari_S1` as the control. Membership from `fixture.py` loaded by path, position from the frame,
  neither side typed into the test.
- **inc65 — no gate header stands inside solari's band**, the amendment's absolute half.
- **inc66 — both answers open and close with their declared pair, at three widths**, where a pair is
  the same mark or that mark's declared mirror (`WALL_MIRRORS`, derived once from the eleven).
- **inc66 — every confirm says where it ends**: the last row a confirm changes must say something.
  Deliberately weak, because eleven languages close a question eleven ways.
- **inc66 — swiss's rejected field spends a wall, a paper and a closer**, all from weights the kit
  already owns at that part, and none of them the `DANGER_FORM`.

**Repaired — three existing laws, and every repair is written into the test:**

- **inc63 — the reverse-kit style law was RESTING ON THE DEFECT.** It read *"no text run anywhere in
  this sheet is painted in the ground colour except the six match runs"*, and that held only because the
  canvas was `#121212`, a colour no kit declares, so every legitimate knockout fell outside the query by
  accident. With the declared ground in place solari's masthead plates paint ink in `#0b0b0c` too. It is
  repaired by PAIRING ON COORDINATE — a text baseline sits 0.78 of a line below its row's background
  rect — which is stronger than what it replaced. Measured: industrial 6 hue rects, darkside 6,
  **solari 8**, the two extra being the plates that broke the old assertion.
- **inc65 — inc40's head law lost its exemption.** `MODAL_KEEPS_NOTHING` became
  `MODAL_KEEPS_ONLY_THE_HEAD` and the refusal's citation moved to the test that asserts corgi's board is
  still gone. **A citation check is not a scope check**: the exemption was written correctly, cited
  correctly and asserted word for word for five batches, and nobody asked whether the sentence it cited
  ("the board is gone") covered the thing it was exempting (the mode strip).
- **inc66 — the contiguity law is strengthened.** `modal_band` reads the rows that DIFFER, and swiss's
  band gained air that landed on the page's own air, so the run came back with two holes in it. The run
  is now measured END TO END and every row inside it that did not change must be blank on BOTH sides.

### 16.4 The census, and the one row that moved

```
language      abd5193   inc63   inc64   inc65   inc66
swiss              2       2       2       2       3
ledger             2       2       2       2       2
the other nine     unchanged
--------------------------------------------------------
TOTAL             25      25      25      25      26
homoglyph rows     1       1       1       1       1
```

**The +1 is swiss's new invalid PAPER, and it is unavoidable for any paper at all.** `┆` was spent at
six of swiss's control seats and carried no A-family, so it sat in the "shared between two CONTROLS only
(alphabet, not counted)" bucket; giving the rejected field a paper adds the `invalid` A-family to it and
the census counts a cell as colliding the moment it carries an A-family plus anything else. Every
candidate cell in swiss's declared alphabet is already spent somewhere, so the only zero-cost option was
to paper the field in `║` itself — not a third weight, and not what the ruling asked for.

**And the row exists because the CENSUS counts the invalid RUNE as a meaning while the LAW does not.**
`_invalid_marks` has excluded the rune by name since inc52; §15.5 already records this discrepancy as
*"the one row five languages have left"*. swiss is the sixth. **The law's own number is unchanged: live
meaning × meaning pairs are still 0**, four exempt. The day the census adopts the law's exclusion, all
six rows go at once.

**One near-miss is recorded because it was measured rather than guessed:** ledger's button ACTIVE was
first drafted `▶··◀`, which would have taken the `·` row from six families to seven for nothing. `─`
carries none — the kit's own words: *"the same stroke the bar's fill draws, and it carries no meaning
anywhere"* — and ledger's count is unmoved at 2.

### 16.5 Frames, and what the skill holds

**Seven distinct component frames moved in the `.txt`:**

```
inc64   prism_S1  prism_S2
inc65   solari_S4  corgi_S4
inc66   ledger_S4  swiss_S2  swiss_S4
```

**And all 66 moved in the `.svg`, once, in inc63** — every language's canvas went from Textual's
`#121212` to the kit's declared ground. Ten dark languages had survived that by luck; ledger, the only
light-paper kit, had been shipping `#1c1a15` on `#121212` at **1.08:1** for the whole programme, with the
dot leaders (9.62:1) the only legible thing on the page.

**Gallery: 3 of the 22 artefacts** — `board_prism` (the ember meter), `gallery_prism` (the component
sheet's four checkbox rows) and `gallery_ledger` (its button row). `gallery_swiss` did not move and that
is checkable: the sheet is cut at 118×34 before its invalid-field row, the same cut §12.5 records for the
stepper. **The 22 gallery `.svg` came back byte-identical after inc63** — those captures already carried
the declared ground because `set_theme` runs before the app's first paint — which is the closest thing
this batch had to a control arm for the exporter fix.

**The skill's installed gallery frames 30–51: NONE changed byte-wise.** All 22 were compared cell for
cell against their sources at the close of the batch and every one is identical:

```
30 ledger_S3 · 31 corgi_S3 · 32 prism_S3 · 33 naught_S5 · 34 blueprint_S5 · 35 corgi_S6
36 ledger_S6 · 37 corgi_S1 · 38 ledger_S1 · 39 naught_S2 · 40 ledger_S2 · 41 blueprint_S2
42 naught_S4 · 43 prism_S4 · 44 instrument_S1 · 45 industrial_S1 · 46 swiss_S1 · 47 solari_S1
48 industrial_S4 · 49 darkside_S4 · 50 solari_S2 · 51 instrument_S5
```

None of the seven frames this batch moved is a source for any of them. **`49_darkside-modal-rounded-lid`,
stale since `rework-5a` (§13.6) and named as open for four batches (G1), is identical again.** This
batch did not install it and `export_to_skill.py` still does not touch that directory. **G1 is closed,
and the skill repo's own log says by whom:** its last commit is `0a241c4 tui-design gallery: twelve
entries re-installed after rework-3..5c; languages re-exported`. Recorded because a G1 that quietly
closed is as worth writing down as one that did not, and because the next round will otherwise
re-report it. **G2 is NOT closed:** the skill repo is dirty again after this batch's export (six files
under `tui-design/assets/languages/`) and was not committed, per the batch's constraint.

**And the skill's own `render_svg.py` already read the declared ground** —
`assets/gallery/svg/30_ledger-settings-danger.svg` grounds its page in a light paper. The skill was
right about ledger and the prototype's exporter was not, for the whole programme, and nobody had put the
two side by side until E4.

### 16.6 What was NOT touched, by name

| | the objection | this batch's contact with it |
| --- | --- | --- |
| **K5** | no law and no instrument reads a QUANTITY widget | **the largest thing left open.** inc64 fixed prism's bar by hand and added the first law that reaches a meter, a slider and a bar at all — but only for DIRECTION. `prism_S3`'s slider still draws nine `⣿` four rows above `⣿Delete all⣿`, and the slider/bar/scrollbar are still outside set B by the operator's own request |
| **K2** | the laws compare code points; `HOMOGLYPHS` is five fixed pairs | untouched, third round |
| **K4** | no law compares two states of one part | **cracked, not closed.** inc64's box law is the first law here to compare two states of one part; blueprint's three-state ladder (`├─┤` / `├┤·` / `├╎┈`) is a different shape and is untouched |
| **L2** | swiss's `Save` is air next to a `Cancel` with a mark | **untouched, and this batch worked two seats away from it.** inc66 filled the FIELD's freed channel; the disabled button is a different seat, three rounds and six batches old |
| **L6, L7, L10** | sparkline on the top rungs · `info` is air · naught's radio vs checkbox | untouched; L7 is **RULED as doctrine** (§16.1) rather than fixed |
| **C5, C6, C7** | nord's sparkline mullion · the search's empty state · instrument's three identical rules | untouched |
| **C9** | the destructive caption is drawn as a field row | untouched, three languages |
| **C10** | the fixture renders two different facts about the same board | **RULED (G vs ruling 10)**, no code |
| **E2** | the `.svg` carries no font metric | untouched, and it is why `CELL_INK`'s eight declared weights are ordinal rather than measured |
| **E3** | `gallery_darkside` is calendar-dependent | untouched; did not fire this batch |
| **G2** | the skill repo is dirty and uncommitted | **still true.** `export_to_skill.py` ran; the skill repo was not committed, per the batch's constraint |

### 16.7 Found by looking

- **The exporter was wrong on ALL ELEVEN languages, not on ledger.** The round reported ledger because
  ledger is the only kit whose ground is far enough from `#121212` for the eye to catch it. Every one of
  the 66 canvases was wrong, and the gallery's 22 were right — a frequency count that returns the right
  answer on one pipeline and the wrong one on another is not measuring a ground, it is measuring which
  pipeline set its background before the first paint.
- **The frequency count was SELF-CONFIRMING.** `svg_from_grid` suppresses a background rect whenever
  `bg == ground`, so the more completely a mistake covered the frame, the more certainly the exporter
  agreed with it and the fewer rects it wrote to leave a trace. The old `ledger_S6.svg` contains **zero**
  background rects.
- **Ruling E is now audited and it holds.** §7.3 of the round objected that promoting the `.svg` to
  darkside's artefact of record presupposed a faithful exporter and that darkside's survival was luck.
  It was luck — darkside declares `#000000` and shipped `#121212`. It is measured now.
- **`mut` against the declared ground is below 4.5:1 in FIVE of the eleven** — nord 3.50, solari 3.65,
  instrument 4.26, darkside 4.43, ledger 4.45 — and most body text in these sheets is `mut`, not `ink`.
  The ruling names `ground` and `ink`, so the law asks about `ground` and `ink`. Measured while writing
  it, not fixed, and not asserted: moving a `mut` is a design change in five kits at once.
- **A law's first draft was measured wrong and prism is why.** inc66's pair clause was first written as
  *"the dangerous answer's closer is not the safe answer's opener"* and went red on prism, which closes
  on `⠿` and opens on `⠿` and is perfectly readable because each seat is symmetric about its own word.
  **Symmetry closes a seat; difference from a neighbour does not.** The clause became "same mark or its
  declared mirror" and the wrong draft is in the test's docstring.
- **`solari_S4` was not silent, it was WRONG, and that is a different class of defect.** inc55 declared
  one cost in writing (the orphan seam) and shipped a second it did not name: a departure filed under a
  gate it is not in. Asked "which gate is `REWRITE THE ONBOARDING` in?", the frame answered `BACKLOG`.
  **A frame that asserts something false is worse than one that says nothing**, and no law in the corpus
  could see it because membership had never been compared against the fixture.
- **An exemption outlived its scope for five batches while being cited correctly every time.** corgi's
  head-law exemption quoted *"the board is gone"* word for word and asserted the quotation. Nobody asked
  whether the sentence covered a mode strip. `corgi_S4.svg` held **seven text runs**.
- **inc59 moved two tables in one increment and preserved an inversion between them.** prism's checkbox
  had been backwards since before inc59 and inc59 rewrote both halves without noticing, because nothing
  in this repo compares two states of one part. The frame said it plainly — the fixture's two ticked tags
  drawn as empty boxes — and eleven months of property tests could not.
- **`test_win_clipboard_roundtrip` was RED in every gate run of all four increments**, including the
  baseline at `abd5193`. It drives the real Windows clipboard through PowerShell (§10.6). **Reported,
  not counted, not touched — and `1165 passed` is not a claim about it either way.**

### 16.8 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc63 · inc64 · inc65 · inc66 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1111 → 1123 → 1147 → 1151 → 1165 passed** (+12, +24, +4, +14), the clipboard test red in every run and named in every packet. `verify_language.py` **ALL PASSED exit 0 after every increment.** `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` 66 of 66, refusals `[]` for all eleven. `capture_languages.py plain` after every increment, 22 grids identical across two processes each time; **6 gallery artefacts moved in total** (3 frames), and **0 moved in inc63**, which is the exporter fix's control arm. `collision_census.py` both self-checks green after every increment. **TOTAL 25 → 26**, accounted for in §16.4; homoglyph rows **1**, unchanged. `export_to_skill.py` at the close: `6 written, 60 already identical`, re-run `0 written, 66 already identical`. **The skill repo was not committed.** Gallery 30–51: **0 of 22 changed byte-wise.** |
| Notes | **5 source files across 4 increments, one agent** (`prototypes/capture_languages.py`, `prototypes/components/render.py`, `prototypes/race_probe.py`, `taskboard/language.py`, `tests/test_components.py`) — never more than 4 in one increment — plus **66 regenerated `.svg` and 14 regenerated component artefacts over 7 distinct frames**, 6 gallery artefacts, the census table, four packets and this section. **Every increment's law was watched failing on the REAL declaration or the REAL bytes** — inc63 on `ledger_S6.svg` and on four frames restored from `abd5193`, inc64 on inc59's two tables and on the pre-inc64 `_meter_ember` re-installed into `LG.METERS`, inc65 on inc55's `band_head` body verbatim, inc66 on ledger's shipped `▶  │` — in addition to the monkeypatched teeth. |

## 17. Batch `rework-6b` — K5, K2, K4, L2 and the `mut` floor

`rework-6a` (§16) took the first four items of `PROTOTYPE-inheritors-3.md` and named what it did not
reach: **K5 ("the largest thing left open"), K2 (untouched, third round), K4 (cracked, not closed) and
L2 (untouched, and that batch worked two seats away from it)**. `rework-6b` is those four plus the
`mut` measurement §16.7 published and declined to act on. **The operator delegated the decisions to the
orchestrator; four increments, one agent.** The rulings are quoted verbatim in each packet's §0 and are
reproduced here, because a ruling that lives only in a chat is a ruling nobody can argue with later.

### 17.1 The rulings, as given

> **A, amended (K5):** the census's B set reaches every quantity widget: slider, bar, scrollbar, meter,
> sparkline, pager, mascot. Their fill and track cells are chrome; a fill cell may not be a meaning mark
> of its language.

> **D, amended (K2):** the homoglyph list is derived, not enumerated: two cells are homoglyphs when they
> are the same base shape at a different size or fill (ring/disc, dot sizes, dash counts within a
> family), and the named four join it now: naught `⊙`/`◉` and `○`/`◦`, ledger `†`/`‡`, blueprint
> `╌ ┄ ┈`.

> **L2:** a disabled control always carries a mark; air is not a state.

> **`mut` contrast:** `mut` is body text and must reach 4.5:1 against the declared ground in every kit,
> with the ladder `ink > mut > dim` kept ordered.

### 17.2 What each increment did

| inc | ruling | what moved | frames |
| --- | --- | --- | --- |
| 67 | **A amended (K5)** | `Kit.quantity_glyphs()` declares the meter, the spark and the mascot (all derived: `METER_CELLS` keyed on the `meter` token, `cover_ramp()`, `base_pixel()`); the census's set B gains slider, bar, scrollbar, that declaration and `PANE_RULE`; naught's meter charges instead of lighting, corgi's partition and creature are milled metal, prism's slider takes the toggle's tables and its pager's thumb follows its shaft off the ember | `naught_S1` `corgi_S1` `corgi_S6` `prism_S1` `prism_S3` `prism_S4` · gallery `board_naught` `gallery_corgi` |
| 68 | **D amended (K2), K4** | `HOMOGLYPH_FAMILIES` replaces five hand-picked pairs (48 derived pairs); `homoglyph_rows` reports MEANING × MEANING with the ladder exclusion by name; naught's scroll shaft leaves the pixel inc61 retired. `state_channel()` gives K4 its first general law plus an ordering clause on the two ladders that are arithmetic | `naught_S1` `naught_S4` · 0 gallery |
| 69 | **L2** | swiss's `button.main[DISABLED]` `"    "` → `"╎   "`, derived from `stepper.main`'s dead cell; `is_wall` excludes dashed strokes and gains an enclosure clause | `swiss_S2` · gallery `gallery_swiss` |
| 70 | **`mut`** | four `mut` values raised to ≥ 4.5:1 by the smallest hue-preserving step; solari exempt by name with an impossibility proof; `dim` measured into a roster instead of floored | 24 `.svg`, **0 `.txt`** (darkside, instrument, ledger, nord) · gallery 8 `.svg` |

### 17.3 The laws this batch added and the ones it repaired

**Added — eight laws, all over all eleven, each with teeth on a real declaration:**

- **inc67 — a fill cell is never a `LEVELS`/`DANGER_FORM`/`REQUIRED` mark**, over six seats (three from
  `PART_GLYPHS`, three from the new declaration). A ROSTER on inc48's precedent: **22 rows before, 16
  after**, each written out with the language that owns it (L6 carries five). One exemption by name in
  two languages — *the meter IS the severity device* — refused for prism's slider and pager because
  ruling A's own condition is that an exemption leave a control's fill distinct from an error rung IN
  THE FRAME, and `prism_S3` refuses it.
- **inc67 — a quantity widget draws what it declares**, rendering each at its floor and its ceiling.
  This is what makes `quantity_glyphs()` a declaration rather than dead metadata.
- **inc67 — the knob law reaches `slider.knob`** (0 for all eleven) and **the opener law reaches the
  meter's bracket** (0 for all eleven). Both free, both real.
- **inc68 — two states of one part are told apart on a channel**, where a channel is ruling D's four and
  `None` is a REFUSAL. Roster: naught 8, darkside 1, nine clean.
- **inc68 — the two doctrine-ordered ladders climb**: prism's four braille rungs, blueprint's three dash
  counts. Only two, and the reason is E2: a braille cell's dots and a dash glyph's dashes are properties
  of the CODE POINT, so no font metric is needed.
- **inc69 — no control state is drawn as air**, over the 110 seats the registry derives per kit, and
  **none renders as air at three widths** with the caller's own word removed. Two clauses, because a kit
  can declare nothing *and* a composer can pad a declaration out of the frame.
- **inc70 — `ink` and `mut` clear 4.5:1 against the declared ground and `ink > mut > dim`**, strict, all
  eleven including the exempt kit — a floor may be unreachable, an order never is.
- **inc70 — `dim` against its ground is measured and recorded**, eleven numbers to two decimals.

**Repaired — three, and every repair is written into the test:**

- **inc67 — `verify_language.py` took its first edit in the programme**, and it is a strengthening. Its
  naught check asserted `NA.ON in fl_meter` — the right answer for the wrong reason, since the claim is
  *"the meter keeps its dots"* and not *"the meter keeps that cell"*. It asks `quantity_glyphs()` now.
- **inc68 — `homoglyph_rows`'s asymmetry was an ARGUMENT and the argument was wrong.** *"Two meanings
  that are one drawing are a question this file already asks of the cell itself"* — the cell-level
  question cannot reach two different cells, which is why ledger's `†`/`‡` read zero for three rounds.
- **inc69 — `is_wall` excludes dashed strokes** on the diagonals' own argument (a broken stroke closes no
  corner either), **paid for with a clause the old rule could not make**: no button seat is marked at
  both ends. `▪ Cancel ▪` is an enclosure and passed a codepoint rule at every width.

### 17.4 The census, and every number in it

```
                     a113385   inc67   inc68   inc69   inc70
collisions              26       35      35      35      35
homoglyph pairs read     5       5       48      48      48
homoglyph rows           1        2      30      30      30
```

**The +9 collisions are the K5 surface becoming visible and NOT ONE KIT GETTING WORSE.** Every one of the
nine is a cell already spent where it is spent, in a widget the census had been told not to read; per
language, corgi +3, swiss +2, prism +2, solari +1, blueprint +1. The four frames inc67 fixed
*subtracted* from what the count would otherwise have been — `prism_S3`'s slider and `prism_S1`'s pager
would have put `⣿` on the same row as `LEVELS["error"]` and the danger form.

**The homoglyph rows went 1 → 30 for the same reason, twice over**: a derived table instead of five
hand-picked pairs, and a reader that stopped skipping meaning × meaning. Grouped by cause, because
thirty rows read one at a time are thirty taste arguments:

```
 6  THE INVALID RUNE  -- the census counts a field's paper as a rejection mark
                         and the LAW does not (§15.5, §16.4).  Six collision rows
                         have the same cause.  TWELVE ROWS ON ONE DECISION.
 5  naught's GROUND   -- exempt by name at the two seat laws, not at the census
 4  naught's `⊛`      -- ruling D amended against §2.8, which calls it the best
                         obligation mark in the corpus.  Both positions written.
 8  darkside's RINGS  -- inc49's accepted COUNT move, a row under the amendment
 4  one pair each     -- swiss, nord, LEDGER's `†`/`‡` (the tightest in the
                         corpus, invisible until inc68), naught
 2  blueprint's DASHES
 1  SOLARI, and it is the census's own FALSE POSITIVE: `LEVELS` here is three
    WORDS and `_cells` splits a word into letters, so the `O` of `OK` is read as
    a severity mark.  A language whose ladder is words declares no severity cell.
```

**Two rows were closed at their declarations**: naught's `scrollbar.main` (the pixel inc61 retired and
could not reach, because the scroll bar was outside set B) and, in inc67, the four fill rows.

### 17.5 Frames, and what the skill holds

**Nine distinct component frames moved in the `.txt`:**

```
inc67   naught_S1  corgi_S1  corgi_S6  prism_S1  prism_S3  prism_S4
inc68   naught_S1  naught_S4
inc69   swiss_S2
inc70   none -- 24 .svg in four languages, and not one .txt in the corpus
```

`naught_S1` moved twice, once for its meter and once for its pager.

**Counts the round can check by hand:** `█` in `corgi_S1` **47 → 2**; `█` in `corgi_S6` **18 → 0**; `⣿`
in `prism_S3` **11 → 2**, and the two are `⣿Delete all⣿`; `⣿` in `prism_S1` 28 → 24; `∙` in `naught_S1`
70 → 57.

**Gallery: 11 of the 22 artefacts** — `board_naught`, `gallery_corgi`, `gallery_swiss` (with their
`.txt`), and `board_`/`gallery_` for darkside, instrument, ledger and nord (`.svg` only).

**The skill's installed gallery frames 30–51: FIVE are now stale** —

```
32 prism_S3 · 35 corgi_S6 · 37 corgi_S1 · 42 naught_S4 · 43 prism_S4
```

**G1 is re-opened.** §16.5 closed it after four batches with the skill repo's own log; this batch moved
five of the twenty-two sources and `export_to_skill.py` still does not touch `assets/gallery/`, so the
same defect is back for the same reason. **Nothing was hand-installed**, per the batch's constraint.

**G2 is still open:** `export_to_skill.py` ran (`14 written, 52 already identical`, re-run `0 written, 66
already identical`) and **the skill repo was not committed.**

### 17.6 What was NOT touched, by name

| | the objection | this batch's contact with it |
| --- | --- | --- |
| **K5** | no law reads a quantity widget | **CLOSED as an instrument, OPEN as a finding.** The widget is in set B and under a law; sixteen rows stand, rostered and owned |
| **K2** | the laws compare code points | **CLOSED as an instrument.** 48 derived pairs, meaning × meaning read; 30 rows stand |
| **K4** | no law compares two states of one part | **CLOSED.** `state_channel()` over every part table, plus the ordering clause. 9 rows stand, in two languages |
| **L2** | swiss's `Save` is air | **CLOSED**, and the law is over all eleven at three widths |
| **`mut`** | five kits under 4.5:1 | **four closed, solari blocked on a ruling** — the two floors provably do not overlap (inc70 §3) |
| **L6** | the sparkline on the top rungs | **counted for the first time** — five of `FILL_IS_NOT_A_MEANING`'s sixteen rows are L6, in three languages. Not fixed |
| **L7, L10** | `info` is air · naught's radio vs checkbox | untouched; L10 is now measured as 8 K4 rows and 9 homoglyph rows |
| **C5, C6, C7, C9, C10** | | untouched |
| **E2** | the `.svg` carries no font metric | untouched, and it is why `state_channel` returns a REFUSAL rather than a pass for an unweighed pair |
| **E3** | `gallery_darkside` is calendar-dependent | untouched; did not fire |
| **G1** | the installed gallery goes stale | **RE-OPENED**, five entries, same cause |
| **G2** | the skill repo is dirty | **still true** |

### 17.7 Found by looking

- **The pager was never a separate widget.** Three rounds of documents call `corgi_S1` f31 and
  `prism_S1` f31 "the pager"; `screens.s1` draws it with `k.scrollbar(...)`, a component that has been in
  `PART_GLYPHS` since the registry was written. **The declaration existed and the reader was told to skip
  it** — the whole of K5 for that widget was one tuple in one file.
- **inc59 scoped the toggle off prism's ember and left the slider on it**, in an increment whose ruling
  is *"a control is read from the TOP"* — and `COMPONENT_PARTS` says in as many words that a switch IS a
  slider whose range is boolean. **The registry had already stated the fact that made the omission an
  inconsistency**, and nothing read the registry against the declaration.
- **corgi's partition was the error rung because its BASE cannot draw.** `segment` is a digit base, so
  anything pictorial falls back to `block`, whose pixel is `█`. The fallback was chosen for legibility
  and nobody asked what cell it landed on.
- **A law's own writing found the next law, twice in two batches.** inc63 wrote `contrast(ink, ground)`
  and measured `mut` while it was there; inc70 wrote `contrast(mut, ground)` and measured `dim` while it
  was there. Both published the number and declined to act; both times the next ruling came from the
  published number.
- **`verify_language.py` caught two this batch and it has now caught five in the programme.** In inc67 it
  caught a check of its own that spelled a cell where it meant to ask a seat; in inc70 it caught solari's
  selection band, which **nothing in pytest could have** — the conflict is between a token and a
  background the APP paints, and only the headless capture puts the two on one cell.
- **The four kits whose `mut` moved cleanly did so because none of them paints a second ground under body
  text.** Luck of composition, not a property anyone had asserted.
- **Three separate rosters now record one discrepancy.** The invalid RUNE is a meaning to the census and
  not to the laws: §15.5 named it for five languages, §16.4 for six collision rows, inc68 for six
  homoglyph rows. **Twelve rows in one repo waiting on one decision.**
- **Every part table in all eleven kits already had pairwise-distinct glyphs.** Measured before K4's law
  was written, and it is why the law had to be about CHANNELS: a distinctness law would have passed
  eleven for eleven on day one and proved nothing.
- **A commitment and its enforcement written in the same breath can close a door nobody meant to close.**
  inc38 declared swiss's disabled button as air *and* the no-wall law in one pass, leaving the kit with
  no legal way to mark a dead button for six batches.
- **`test_win_clipboard_roundtrip` was RED in every gate run of all four increments**, including the
  baseline at `a113385`. It drives the real Windows clipboard through PowerShell (§10.6). **Reported, not
  counted, not touched — and `1248 passed` is not a claim about it either way.**

### 17.8 Two decisions this batch surfaced and could not take

1. **solari's `mut`.** The selection band is a second ground; satisfying the ruling means giving the
   banded row its own ink, which `_sched_row` cannot see today. `THE_BAND_IS_A_SECOND_GROUND`, by name,
   with the arithmetic.
2. **Whether the census adopts the laws' exclusion of the invalid RUNE.** It would clear six collision
   rows and six homoglyph rows at once, and the discrepancy is now three batches old.

### 17.9 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc67 · inc68 · inc69 · inc70 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1165 → 1188 → 1202 → 1225 → 1248 passed** (+23, +14, +23, +23), the clipboard test red in every run and named in every packet. `verify_language.py` **ALL PASSED exit 0 after every increment** — and RED twice during the work, in inc67 and inc70, both written up. `render.py` 66 frames / 330 pairs / 0 hand-drawn after every increment. `matrix.py` refusals `[]` for all eleven. `collision_census.py` both self-checks green after every increment; **TOTAL 26 → 35**, accounted for in §17.4; **homoglyph rows 1 → 30**, likewise. `capture_languages.py plain` after every increment, 22 grids identical across two processes each time; **11 gallery artefacts moved in total**. `export_to_skill.py` at the close: `14 written, 52 already identical`, re-run `0 written, 66 already identical`. **The skill repo was not committed.** Gallery 30–51: **5 of 22 are stale** (32, 35, 37, 42, 43) and none was hand-installed. |
| Notes | **6 source files across 4 increments, one agent** (`taskboard/language.py`, `taskboard/naught.py`, `taskboard/themes.py`, `prototypes/collision_census.py`, `prototypes/verify_language.py`, `tests/test_components.py`) — **never more than 5 in one increment**, and 5 only in inc67 — plus **9 distinct component frames** regenerated (`.txt` and `.svg`), 24 further `.svg`, 11 gallery artefacts, the census table, four packets and this section. **Every increment's law was watched failing on a REAL declaration**: inc67 on `METER_CELLS["dotgrid"]`, prism's shipped `scrollbar.indicator` and corgi's base fallback; inc68 on inc59's dimming walls and inc64's inversion; inc69 on inc38's four spaces, byte for byte; inc70 on the four `mut` hexes with the ratios they shipped at. |

---

## 18. Batch `rework-6c` — one definition for the field's rune, and the solari `mut` doctrine recorded

`rework-6b` (§17.8) surfaced two decisions it could not take: solari's `mut` (blocked on a per-row-ink
change outside this programme) and whether the census adopts the laws' exclusion of the invalid RUNE (a
discrepancy `spec.md` had already named in §15.5, §16.4 and §17.4/§17.8, three batches running). **The
operator delegated both to the orchestrator; one increment, one agent.** The ruling is quoted verbatim in
`inc71.md` §0 and reproduced here.

### 18.1 The rulings, as given

> **One definition.** The invalid field's RUNE (its paper, the middle cell) is chrome, not a meaning; the
> census adopts the laws' exclusion. Move the definition to one place both files import (a small function
> or constant in `taskboard/language.py` or a shared module under `prototypes/`, whichever the two already
> share), so the census and the laws cannot disagree again.

> **solari's `mut`** stays exempt by name with the arithmetic (`L ≥ 0.19021` against the ground, `L ≤
> 0.14960` against the band): the selection band is a second ground and a per-row ink is app CSS work
> outside this programme. Recorded as doctrine in the kit docstring and in `spec.md`; the exemption's
> stale check stays.

### 18.2 What the increment did

`taskboard/language.py` gains `split_field_glyph(glyph) -> (opener, rune, closer)`, module-level, and
`Kit.field_form` now delegates to it instead of carrying its own copy of the same arithmetic.
`tests/test_components.py::_invalid_marks` calls it for the `textfield.main` branch (dropping the rune,
keeping the two walls, same behaviour as before — only the source of the split changed).
`prototypes/collision_census.py::role_map` gains the branch that had never existed: for a field's `main`
part in the `invalid` state, the rune is credited to the component's own chrome family instead of to
`invalid`, exactly as every other state's rune already is three lines above it. One teeth test
(`test_the_census_and_the_law_read_the_rune_off_one_function`) loads `collision_census.py` as a module and
proves both readers move together under the same monkeypatch of the shared function.

solari's `mut` ruling asked for no code: the doctrine it names — the two inequalities and the "the two
floors do not overlap" conclusion — was already written into `taskboard/themes.py` (lines 134–190) by
inc70, and `THE_BAND_IS_A_SECOND_GROUND`'s stale-exemption check (`tests/test_components.py`) already
stands. This section is the `spec.md` half of "recorded as doctrine ... in spec.md."

### 18.3 The census, and the two rows the four-batch-old prediction missed

**Collisions 35 → 30. Homoglyph rows 30 → 26.** Both predictions on record (§15.5, §17.4, §17.8) expected
35→29 and 30→24 — six rows closing on each side, one per affected language. Measured, four languages close
cleanly on both counts (corgi, ledger, solari, blueprint: their rune's homoglyph/collision partner carries
no A-family of its own, so once the rune stops being a meaning neither side of the pair is one) and two do
not, for two different and real reasons:

```
                    collisions          homoglyph rows
language          before   after       before   after
naught                 4       3           12      12
corgi                  5       4            1       0
instrument             4       4            0       0
swiss                  5       4            1       1
industrial             2       3            0       0
nord                   1       1            1       1
darkside               1       1            8       8
prism                  4       4            0       0
ledger                 2       1            2       1
solari                 4       3            2       1
blueprint              3       2            3       2
----------------------------------------------------------
TOTAL                 35      30           30      26
```

- **naught's two homoglyph rows reclassify rather than close.** Its rune (`⋅`) pairs with `∙`
  (`DANGER_FORM`+`LEVELS[error]`) and `●` (`CUR`) — both REAL meanings, not bare chrome — so the pair still
  reads, now as meaning-×-chrome instead of the manufactured meaning-×-meaning it used to be. Its
  collision count still drops by one, because `⋅` itself stops carrying an A-family and so stops being a
  colliding CELL even though its homoglyph partners still list it.
- **industrial GAINS a collision row, and it is real.** `/` is industrial's field paper under `INVALID`
  AND its own declared invalid mark at `slider.knob`/`stepper.step` (inc52 §9 already named industrial as
  a kit whose invalid walls never change, only the paper does). Both uses used to land in the same
  `invalid` family, which the census's own rule reads as no collision (one family, however many
  declarations). Split correctly, the field's use is chrome and the knob/stepper's use is still `invalid`
  — a genuine two-role cell, invisible until this increment's fix stopped merging them by accident.

Net **−5 on collisions (6 removed, 1 revealed), −4 on homoglyph rows (4 removed, 2 reclassified in
place)**. `inc71.md` §4 and §9 have the full account, including that nobody had checked the six-row
prediction's arithmetic against the actual partner families before this increment ran it.

### 18.4 Frames, gallery and the skill

**Zero.** No glyph table moved — only which family a rune's cell is filed under — so `render.py` (66
frames), `matrix.py` (66 implementa) and `capture_languages.py` (22 grids) all report no change, confirmed
by `git status --short` on `prototypes/components/` and `prototypes/gallery/` returning nothing.
`export_to_skill.py` was not run: nothing moved to export, and the skill repo's standing dirty state (G2,
§17.5) is unchanged by this batch.

### 18.5 What was NOT touched, by name

| | the objection | this batch's contact with it |
| --- | --- | --- |
| **the invalid-RUNE discrepancy** | census and laws disagreed about the rune | **CLOSED as an instrument** — one function, both files read it, teeth prove they move together |
| **industrial's `/`** | field paper doubles as the knob/stepper's invalid mark | **newly measured, not ruled on** — §18.3, `inc71.md` §11 |
| **solari's `mut`** | the banded row has no ink of its own | **doctrine recorded** (already written in `themes.py`/`inc70.md`); still blocked on the per-row-ink decision, which is app CSS work outside this programme |
| **L6, L7, L10, C5–C10, E2, E3, G1, G2** | | untouched, carried from `rework-6b` (§17.6) |

### 18.6 Found by looking

- **A discrepancy can be named correctly in four separate packets across three batches and still not be
  fixed, because naming the PRINCIPLE ("the rune is chrome") is not the same work as making two files'
  CODE say so in one place.** `inc52.md` §0a already stated the principle exactly right; the plumbing gap
  lived on for four batches after the principle was settled.
- **A published prediction that nobody ran is a guess with a byte count.** The six-row forecast assumed
  every rune's homoglyph/collision partner was bare chrome; two of six (both naught's) are real meanings,
  and only running the fix found that.
- **A census bug can hide a real collision as easily as it manufactures a false one.** industrial's `/`
  collision was invisible for the same reason the false ones were visible: the rune's mis-classification
  happened to land in the SAME family as a genuine declaration at that cell, so the two merged into what
  looked like one harmless fact instead of two roles worth flagging.

### 18.7 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc71, the whole batch |
| Phase C (close) | this section |
| Gates | `pytest -q` **1248 → 1249 passed** (+1, the new teeth test), the clipboard test red at the baseline and named in the packet. `verify_language.py` **ALL PASSED exit 0**, unaffected by construction. `render.py` 66 frames / 330 pairs / 0 hand-drawn, **0 of 66 moved**. `matrix.py` 66 of 66 implementa, refusals `[]` for all eleven. `capture_languages.py plain` 22 grids identical across two processes, **0 of 22 moved**. `collision_census.py` both self-checks green; **TOTAL 35 → 30** and **homoglyph rows 30 → 26**, both accounted for in §18.3 against a four-batch-old prediction that was two rows short on each side. `export_to_skill.py` not run — nothing moved. |
| Notes | **3 source files, one increment, one agent** (`taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py`) — no component frame and no gallery artefact regenerated differently, because this batch moved a classification, not a glyph. The teeth test was watched proving both directions on the same monkeypatch, not merely asserting the post-fix state (`inc71.md` §3). |

---

## 19. Batch `rework-7a` — the four reworks, the four contrast rulings, and two rulings that corrected two of them

`PROTOTYPE-inheritors-4.md` (2026-09-07, at `4089eda`) judged all 66 frames for the fourth time and
returned **keep 11 · note 51 · rework 4** — the first round in which a label went DOWN, and it did so
four times for one reason: inc63 made the exporter honest about the ground, so for the first time the
corpus could be MEASURED and the measurement was worse than the reading. **The operator delegated the
decisions to the orchestrator, and this batch is four increments and nine rulings, two of which the
orchestrator issued to correct two of its own after the increment reported the arithmetic back.**

### 19.1 The rulings, as given

The seven of the brief, verbatim in every packet's §0:

> **K6:** contrast is measured against the background actually under the run (the second grounds:
> selection bands, plates, match rects), not only the canvas. `ink` and `mut` ≥ 4.5:1 against every
> ground they are painted on; `focus` ≥ 3:1.

> **K7:** `dim` ≥ 3:1 wherever it classifies (a severity rung on a log row, a dash count, a state
> mark); a purely decorative leader or seam is exempt by seat, named. `alert` ≥ 4.5:1 against every
> ground it is painted on, all eleven.

> **Match tier:** `accent` (or the match ink) against `mut` and against `ink` ≥ 3:1, all eleven, so
> raising `mut` cannot silently erase the match.

> **L7 measured:** the `info` rung may be air (blueprint, ledger, doctrine) or drawn; if drawn it
> obeys K7 (≥ 3:1). Nine languages draw it under 2:1: fix each.

> **C8, second half:** corgi's confirm gets walls from its display frame (`▓`, inc67's register
> ruling) with the board still gone; thirty blank rows with no opener or closer is not a modal.

> **swiss `╎`:** stands; consistency with the kit's own dead cell beats one fewer vertical.
> Recorded.

> **industrial `/`:** the value's separators and the field paper may not be one glyph: the paper
> becomes a cell that no value can contain (cite industrial's alphabet), the invalid marks at
> slider.knob/stepper.step stay.

And the two the orchestrator issued mid-batch, correcting itself:

> **Ruling on the match tier** (replaces the "≥ 3 vs mut and vs ink" clause, which is unsatisfiable:
> contrast(ink,ground) = contrast(ink,mut) × contrast(mut,ground), so it demanded 40.5:1 against a
> physical maximum of 21:1). The match run must be legible and distinct, and the two are measured on
> different channels: (a) legible: match ink ≥ 4.5:1 against the ground it is actually painted on
> (for `reverse` that ground is the swapped rect); (b) distinct: by the channel the kit declares in
> `MATCH_STYLE`. Where the channel is weight or decoration, the svg run must carry
> `font-weight`/`text-decoration` (structural assertion, no luminance clause: 1.00 by construction
> is correct). Where the channel is `reverse`, the rect must exist under exactly the match cells.
> Where the channel is a hue (`bold {accent}` in nord etc.), assert hue distance: the accent's hue
> angle differs from `mut`'s and `ink`'s by ≥ 30° in HLS, or, for achromatic kits, the accent
> differs from `mut` by ≥ 1.5:1 in luminance. nord's 1.38 is then judged on hue, and if nord's
> accent is achromatic it is the 1.5 clause. Report which kits fall in which branch and which fail.

> **Ruling on industrial's focus:** a token has exactly one role. Ground-role tokens (ground, band,
> plate, match rect) and ink-role tokens (ink, mut, dim, focus, alert, accent) are disjoint sets in
> `THEMES`, asserted by a test over all eleven. Industrial's plate becomes its own token `plate`
> (= `#2e2e2e` today), the focus bracket keeps `focus` as ink and moves to a value that clears 3:1
> on both grounds it is painted on. Check the other ten for the same double role while you are there
> (solari's band already has a name; darkside's grey steps?).

**`swiss ╎` IS RECORDED AND NOT IMPLEMENTED, on purpose.** The ruling says the sixth vertical stands
because consistency with the kit's own dead cell beats one fewer vertical; nothing in the code had to
move for that to be true, and it is here so the next round argues with a written ruling.

**THE TWO CORRECTIONS ARE THE BATCH'S OWN FINDING, and both were reported before a token moved**,
which is what the brief asked for in its own words (*"report the failing runs by language and tier
before any token moves"*). §19.5 carries the arithmetic.

### 19.2 What each increment did

| inc | ruling | what moved | frames |
| --- | --- | --- | --- |
| 72 | **the four reworks** | `Ledger.overlay_instead` builds `[rule] + rows + [rule]` and cuts the page to fit, so the posting closes and `(Delete)` leaves row 32; naught's band is bounded by `NA.OFF` instead of the `DANGER_FORM`; naught's radio DEFAULT/FOCUSED trade places so its resting pair leaves the checkbox's ring family; blueprint retires `┄` and `┈` and moves `LEVELS["warn"]` off `╌` to `"━ "`. | `ledger_S4` `naught_S2` `naught_S4` `blueprint_S3` `blueprint_S5` txt+svg · gallery `gallery_naught` `gallery_blueprint` |
| 73 | **K6, K7's `alert`, the match tier, the role ruling** | `painted_runs()` reads the ground under every run of the 66 svgs; ten tokens move in seven kits; `focus` joins `Kit.__init__`'s ink set and `Industrial.keyhint` stops painting glyphs in a ground name. | **svg only** — 30 component, 11 gallery |
| 74 | **K7's `dim`, L7** | `DIM_CLASSIFIES`, eight seats, three verdicts. `log_row`'s tone ladder `dim/mut/ink` → `mut/mut/ink`; ledger's and corgi's inactive mode labels leave `dim`. **Zero tokens moved.** | **svg only** — 20 component, 2 gallery |
| 75 | **C8's second half, the `/` ruling** | `Corgi.overlay_instead` wraps its question in two full-measure `PANE_RULE` bars; industrial's rejected field is papered in `░`. | `corgi_S4` `industrial_S2` txt+svg · 0 gallery |

### 19.3 Every token moved, with every ratio

All in inc73; inc72, inc74 and inc75 moved **no token at all**.

| kit | token | old | new | clause | before → after |
| --- | --- | --- | --- | --- | --- |
| industrial | `mut` | `#8f8f8f` | `#959595` | K6, on the plate | 4.20 → **4.53** |
| industrial | `alert` + `accent` | `#ff4b1f` | `#ff6039` | K7, on the plate | 4.06 → **4.52** |
| industrial | `focus` | `#2e2e2e` | `#777777` | role ruling | 1.28 → **3.03** on ground, **3.03** on plate |
| ledger | `mut` | `#6a6458` | `#635e52` | K6, on the band | 4.10 → **4.51** |
| nord | `alert` | `#bf616a` | `#cf888f` | K7 | 3.05 → **4.50** |
| nord | `accent` | `#88c0d0` | `#8fbcbb` | match tier, hue | 25.4°/24.2° → **40.0°/38.8°** |
| corgi | `alert` | `#d92b1a` | `#e53524` | K7 | 3.99 → **4.50** |
| naught | `alert` + `accent` + `warn` | `#d71921` | `#e51b24` | K7 | 4.05 → **4.51** |
| swiss | `alert` + `accent` + `warn` | `#e2231a` | `#e7372e` | K7 **and** match legibility | 4.07 → **4.52** |
| swiss | `mut` | `#8a8a8a` | `#9b9b9b` | match tier, achromatic fallback | 1.36 → **1.52** vs the match |

**Ten values in seven kits, and every one is the smallest HLS lightness step that clears every clause
at once with hue and saturation held exactly** — inc70's declared method — **except nord's `accent`**,
which is a hue move by definition and takes `#8fbcbb`, Nord's own published frost-0, so the scheme
does not leave its palette to gain the channel. **Three kits move `accent` with `alert` because the
two are one hex by declaration**; splitting them to reach a floor would have turned a one-colour
ration into two. **swiss moved the GREY and not the RED** at the match clause: reaching 1.5:1 by
moving the red costs the kit its signature colour.

**solari's `mut` stays under the floor**, on the impossibility proof `THE_BAND_IS_A_SECOND_GROUND`
has carried since inc70, and inc73's law asserts the exemption is real and that `mut` is the only
tier that fails there.

### 19.4 The laws this batch added, replaced and re-measured

**Added — twelve laws and eight teeth, all over all eleven:**

- **inc72 — ledger's confirm opens and closes on the same rule** and its destructive answer is not on
  the sheet's last row; **naught's band adds no lit dot of its own** (the `DANGER_FORM` count inside
  it equals what the question spends); **naught's two option controls do not rest on one drawing**
  (L10, asked of the RESTING pair and of the shipped frame); **blueprint's dead runs turn instead of
  counting dashes** (four clauses: `┄`/`┈` gone, the two dead runs, no dead run is the warn rung or
  its homoglyph, a dead datum is never its own walls) plus the severity ladder's drawn-cell counts
  `[0, 1, 2]`.
- **inc73 — every painted run clears its tier's floor on its own ground**, per character over the 66
  svgs (`TIER_FLOOR`, and `dim` is deliberately absent); **the match run is legible and distinct on
  its declared channel**, four branches; **a token has exactly one role**, over `THEMES`; **and this
  file's picture metrics are the exporter's**, checked against `capture_languages.py`'s source rather
  than imported.
- **inc74 — a `dim` run that classifies is legible or has moved** (`DIM_CLASSIFIES`, eight seats,
  three verdicts, with a vacuity arm that runs the `carried` branch's cited law); **the `info` rung
  is air by doctrine or legible by tier** (`INFO_RUNG_IS_AIR`).
- **inc75 — a confirm opens and closes on marks of its own** (DRAWN rows, not CHANGED ones); **a
  rejected field's paper is a cell no value can contain**, against `fixture.py` read by path.

**Replaced — one law, and the replacement is the batch in one line:**

- **inc72 retired `test_blueprints_dash_ladder_is_monotone_in_its_count`.** It asserted the ladder
  CLIMBS, which was the honest limit of what inc60 could ask; round four answered it by measuring the
  three runs at 1.24:1. **A count you cannot resolve is not a channel however well it is ordered**,
  and the teeth make the point in arithmetic: with inc60's table restored the OLD law still passes
  and the new one goes red.

**Re-measured — three constants, and each measurement is a finding:**

- **`BLUEPRINT_TABLES_WORTH` `(1, 8)` → `(0, 0)`** and `BLUEPRINT_SHEET_BEFORE[REQUIRED]`
  `(8, 12)` → `(7, 4)`. The same cells at the same seats are worth eight rows or none depending on
  where one meaning sits — inc60's ruling (ii) stated as arithmetic. The end point is unchanged at
  `(13, 12)`.
- **L7's count is EIGHT, not nine.** inc74's teeth restore the `dim` rung for all eleven and collect
  the red list: instrument, swiss, industrial, nord, darkside, naught, corgi and **solari** (three
  WORDS at 1.20:1, which round four listed under "words" without measuring). **prism is not in it**
  — 3.25:1, the only kit of the eleven over the floor.
- **`STATES_TOLD_APART_BY_SIZE["naught"]` did NOT move and stays 8**, which inc72's packet states
  against its own first draft: the `○`/`◦` pair moved from DEFAULT-vs-ACTIVE to FOCUSED-vs-ACTIVE.
  What changed is the pair of cells a FORM draws, which is what L10 was raised about.

### 19.5 The two arithmetic findings that produced the corrections

**The match tier as first ruled was unsatisfiable in every kit at every token value.** WCAG's ratio is
exactly multiplicative — every term is a ratio of `L + 0.05` — so

```
contrast(ink, ground) == contrast(ink, mut) x contrast(mut, ground)
```

A match ink 3:1 from both `mut` and `ink` forces `contrast(ink, mut) >= 9`, and with K6's
`mut >= 4.5` that forces `contrast(ink, ground) >= 40.5` **against a physical maximum of 21:1**. The
corpus's best `ink/mut` headroom, with `mut` sitting exactly on the K6 floor, is darkside's **4.28**.
And the two clauses fight: inc73's K6 fix for ledger moved the match tier 2.96 → 2.69, which is round
four's §7.1 objection reproduced as arithmetic rather than as a complaint.

**industrial's `focus` was a defect no floor could catch.** `plate` and `focus` were one hex and
`Industrial.keyhint` painted the plate's WALLS in `self.plate`, so a ground-role value was drawn as
ink at **1.28:1**, eight cells. `contrast(token, ground) >= 3` cannot tell which role a token has.
**The other ten were checked: one clash in eleven kits, and it is the one the ruling names.**

**And the corpus's tightest number now has no clause at all**, which is recorded rather than left to
be discovered: after this batch swiss's `ink/mut` is 2.53 and nord's 2.40. The proof above says no
match clause can constrain it, and whether `ink > mut` is a VISIBLE ladder at 2.4:1 is a question no
law here poses.

### 19.6 The census, across the four increments

```
                   4089eda   inc72   inc73   inc74   inc75
NAUGHT   colliding      3       3       3       3       3
BLUEPRINT colliding     2       1       1       1       1
INDUSTRIAL colliding    3       3       3       3       2
the other eight      unchanged
-----------------------------------------------------------------
TOTAL colliding        30      29      29      29      28
TOTAL homoglyph rows   26      24      24      24      24
```

**Two rows closed and both were closed by RETIRING CELLS rather than by widening the reader**, which
is the first time in this programme. blueprint's `╌`/`┄` and `╌`/`┈` went because `┄` and `┈` left the
kit and the warn rung left `╌`; industrial's `/` stopped colliding because the fix took its CHROME
half away and one A-family alone does not collide — **the accounting inc66 predicted in the other
direction** when swiss's new paper cost exactly one row. The instrument is consistent in both
directions.

### 19.7 Frames, and what the skill holds

**`.txt` — 7 of the 66 moved**, and every one is a glyph decision:

```
blueprint_S3  the dead switch `├╎┈` -> `├╎╌`
blueprint_S5  the warn rung appears: `09:41:09    3 tasks` -> `09:41:09 ━  3 tasks`
corgi_S4      two full-measure `▓` bars at rows 13 and 20
industrial_S2 `▐12/09/26//////…▌` -> `▐12/09/26░░░░░░…▌`
ledger_S4     the posting closes on row 32; `(Delete)` moves to row 31
naught_S2     `○ low  ○ norm  ⊙ high` -> `◌ low  ◌ norm  ⊚ high`
naught_S4     rows 13 and 20: 100 `∙` -> 100 `◦`; `∙` on the sheet 237 -> 37
```

**`.svg` — 42 of the 66 moved**, the 7 above plus 35 that changed colour only. inc73 and inc74 are
**svg-only increments** and that is checkable rather than claimed: ten token moves and two seat moves
left every `.txt` byte-identical, which is the strongest available statement that this corpus judges
colour on a separate artefact.

**Gallery — 14 of the 22 artefacts moved:** `board_corgi` `board_industrial` `board_ledger`
`board_naught` `board_nord` `board_swiss` (svg) · `gallery_industrial` `gallery_ledger` `gallery_nord`
`gallery_swiss` (svg) · `gallery_blueprint` and `gallery_naught` (txt AND svg).

**`export_to_skill.py`:** `11 languages, every token, doc and family round-trips` ·
**captures 14 written, 52 already identical** · `SURFACES.md (11 postures)`. The fourteen written are
exactly the fourteen named above — the skill's gallery 30–51 changed byte-wise in those names and
nowhere else. **The skill repo is not committed**, per the batch's own standing instruction.

### 19.8 What was NOT touched, by name

- **solari's `mut`** — 3.65:1 against its canvas, exempt by an impossibility proof four batches old.
  Its resolution is a per-row ink for the banded row, which `_sched_row` cannot see because the band
  is painted by the app's own CSS. **Still a request for a ruling, not a verdict.**
- **`Kit.depth_ground()`** reads `t["focus"]` as a GROUND, for darkside and prism. The role law is
  green because those kits' values are disjoint from their ground tokens; the CODE still has the
  double role the ruling is about.
- **nord's and darkside's rejected fields are papered in AIR** (`"? ?"`, `"Ø Ø"`). An L2-shaped
  reading at a seat L2 did not reach; both are named in inc75's law rather than skipped, so a third
  cannot join them unnoticed.
- **`/` survives at `knob[INVALID]` and `stepper.step[INVALID]`** and neither is drawn in the 66 —
  preserved by the ruling, and round four's §7.6 point is unchanged.
- **`STATES_TOLD_APART_BY_SIZE`** — naught 8, darkside 1. Closing them is still "a second channel for
  this alphabet, which is a language-level increment".
- **`log.time` is `dim` in all eleven** and `DIM_CLASSIFIES` calls it decorative. The ruling's example
  list does not name it and this batch did not widen it on its own authority.
- **C5, C6, C7, C9, C10, E2, E3, G1, G2, L4, L6** — open.

### 19.9 Found by looking

- **A ruling can be arithmetically impossible and read perfectly.** The match-tier clause named a
  real defect (raising `mut` erases the match), asked for the obvious remedy, and demanded 40.5:1
  where 21:1 is the ceiling. It was caught by writing the identity down, not by trying values.
- **A floor cannot catch a role.** industrial's `#2e2e2e` was correct as a ground and wrong as ink,
  and two batches of contrast law were green on it. The law that caught it asks a different question.
- **`self.c` was the evidence and nobody read it.** `Kit.__init__` built the ink set from six keys and
  `focus` was not one of them — which is exactly why `keyhint` reached for `plate`: the token it
  wanted was not in the dict it paints from. The bug and its diagnosis were four lines apart.
- **A case-sensitive reader passed a kit that had the defect.** inc74's first draft searched for the
  mode label as written and corgi UPPERCASES its legend, so the law found no seat and said nothing.
  Recorded in the reader's own comment. **A law that looks in the wrong place is worse than no law**,
  because it also reports.
- **inc60's dash count was forced by a constraint nobody restated.** The dead runs left `╌` because
  `╌` was the warn rung; three batches later the cheaper move was to send the MEANING away instead,
  and the same tables that were worth `(1, 8)` became worth `(0, 0)`. **The constraint was in a
  comment and the alternative was never priced.**
- **Two exemptions in this file already turn on "a ground is not a mark"** — `THE_GROUND_IS_NOT_A_MARK`
  and `THE_BAND_IS_A_SECOND_GROUND` — and inc75 added a third, solari's confirm edge. Nobody has asked
  whether that is one idea or three.
- **The `.txt` cannot show colour and the `.svg` cannot show a keystroke.** Two of this batch's four
  increments are invisible in the artefact three rounds judged the corpus on.

### 19.10 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc72, inc73, inc74, inc75 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1249 → 1338 passed** (+89), the clipboard test red at the baseline and named in every packet — environment-coupled (§10.6), reported, not counted, not touched. `verify_language.py` **ALL PASSED exit 0** at every increment (and RED three times inside inc72, on the first draft of the blueprint fix — §19.9). `render.py` 66 frames / 330 pairs / 0 hand-drawn. `matrix.py` 66 of 66, refusals `[]` for all eleven. `capture_languages.py plain` 22 grids identical across two processes at every increment. `collision_census.py` both self-checks green; **TOTAL 30 → 28**, **homoglyph rows 26 → 24**. `export_to_skill.py` **14 written, 52 identical**. |
| Notes | **Four increments, one agent, 2–3 source files each** (`taskboard/language.py`, `taskboard/themes.py`, `tests/test_components.py`, `prototypes/collision_census.py`). Twelve laws, eight teeth, one law retired, three constants re-measured. **Two of the brief's seven rulings were reported back with arithmetic and corrected by the orchestrator before any token moved**, which is the batch's own finding and is why §19.5 exists. |

---

## 20. Batch `rework-7b` — the instrument the fifth round was refused three times

`PROTOTYPE-inheritors-4.md` §9d ends with a recommendation and not a rework list: *«parar la ronda y
cambiar el instrumento … construir el raster (E2) y solo entonces correr la ronda cinco, contra el
raster y a dos anchos.»* **This batch is that instrument and nothing else.** Three increments, one
agent, 2–3 source files each. **No kit was edited, no token moved, no frame moved:** the 66 `.txt`,
the 66 `.svg` and the census's `28 / 24` are byte-for-byte what `0ec5904` shipped.

### 20.1 The ruling, as given

> **The fifth round runs against a raster at real cell size, not against svg attributes; the raster is
> an instrument the suite owns.** (orchestrator, 2026-09-07, on the operator's delegation)

Three sub-rulings, one per increment: the font is a **declared constant, never inferred**; the
legibility floor is **proposed, not enforced**; the second width **judges and does not fix** —
*"Do not fix languages here; the round judges."*

### 20.2 What each increment did

| inc | ruling | what it built | artefacts |
| --- | --- | --- | --- |
| 76 | **E2**, three rounds open | `raster.py`: 66 PNGs at **Cascadia Mono 16 px, 9×19 px per cell**, measured off the font, byte-identical across two processes. `render.one()` splits into `frame()` + two `write_text` calls so the PNG and the SVG come out of one `cell_grid`. | **66 png + 66 json** · 0 of 132 existing artefacts moved |
| 77 | the four measures | `legibility.py` → `prototypes/out/legibility.txt` (591 lines): ink area per glyph, homoglyph XOR distance, per-cell coverage and effective contrast, coverage × effective for all 79 meaning marks. | **1 report** · 0 artefacts moved |
| 78 | a second width | `second_width.py`: the same six screens at **80×24**, txt + svg + png + json, and 79 law-arms asked of them. | **264 in `w80/`** · 0 artefacts moved |

### 20.3 The five findings the batch produced, in the order they landed

1. **`•` U+2022 and `∙` U+2219 are LITERALLY ONE DRAWING** in this face: XOR area `0.0`, not `0.004`,
   found by sweeping all **20 706** pairs of the corpus's painted glyphs rather than by reading a
   family list. `HOMOGLYPH_FAMILIES` puts them in one row on the strength of a reading and this is the
   first artefact that can say the reading was not a guess. **No kit draws both** — naught spends `∙`
   134 times (danger + severity), swiss spends `•` twice (required) — so it is two languages holding
   one drawing for incompatible meanings, and it is stated that way rather than as a collision.
2. **Seven of the ten pairs four rounds argued about are 15–27 % of a cell apart.** `• ●` 21.64,
   `○ ◦` 22.81, `◎ ◉` 21.42, `▪ ■` 26.52, `▬ ◦` 17.09, `⠇ ⠸` 15.13. The three that survive the
   measurement are the dash ladder (`┄ ┈` 2.79, `╌ ┄` 4.09, `╌ ┈` 4.46) and `† ‡` at 4.87 — which is
   the set the rounds treated as tightest. **The instrument agrees with the reading where the reading
   was careful and contradicts it where it was not.** And the census's tightest row is **darkside
   `▪ ▫` at 3.20 %**, not ledger's `† ‡` at 4.87 — the ranking three documents assert is wrong by one
   place.
3. **Ruling F fails for solari at 24 rows.** *A confirm never covers the gate it names*: at 32 rows a
   confirm about `DOING` puts its band at 24–28, clear below `DOING`'s block; at 24 rows there is no
   below, the band lands at 17–22 and eats rows 17 and 18, which are `DOING`'s own departures. **The
   placement rule was written, and tested, on a page that always had somewhere to go.**
4. **`⠀` U+2800 draws nothing and `capture_languages.ink()` counts it as ink 421 times** — instrument
   174, prism 247. Every density argument four rounds made about those two kits counts 421 cells of
   nothing. A defect of the DENSITY MEASURE, not of the kits; not fixed, because `ink()` is shared with
   the board sweep.
5. **A law's magic number outlived the width it was measured at.**
   `test_a_confirm_opens_and_closes_on_marks_of_its_own` spells "at full measure" as `any(w > 800)`;
   800 is 100 cells × 8.4 units. At 80 columns solari's plate is 672 units and IS at full measure.
   **The frame is correct and the law is wrong**, and the fix is deliberately not taken in the
   increment that found it.

### 20.4 The laws this batch added

**Eleven laws and two teeth, all reading artefacts as bytes** — no increment imports `raster.py` or
`legibility.py` into the suite, on the stance `test_this_files_picture_metrics_are_the_exporters`
already takes: the instrument's declarations are restated in the test file and checked against the
artefact it shipped, so the two can only agree by being right.

- **inc76** — the raster's declarations are the ones the suite measures against (source + all 66
  sidecars); cells × box = pixels, read out of the **IHDR by hand**; **every pixel of every distinct
  cell lies on the segment between that cell's two declared colours**, within one unit per channel
  (7081 distinct cells, worst error 1), with tile identity as the no-bleed clause; the face's full
  block leaves a seam. **Teeth on three mutants of `instrument`'s shipped PNGs**, including inc63's
  wrong-ground defect reproduced in the new artefact.
- **inc77** — a homoglyph distance is zero only when the drawings are one (20 706 pairs, exactly one
  zero, named); the ten argued pairs measured independently AND parsed out of the shipped report; the
  report on disk is the one this corpus produces. **Teeth: the swap the brief named** — make ledger's
  `‡` the same drawing as its `†` and the corpus's zero-pair sweep returns two where it returned one.
- **inc78** — the 80×24 corpus is the rectangle it claims; **53 law-arms re-run with `FRAMES` pointed
  at `w80/`, with a control arm that runs the same 53 at 100×32 first**; and ruling F's failure stated
  in arithmetic rather than in a test id.

### 20.5 What the batch refused to do, and why each refusal is written down

- **The floor is proposed and not enforced.** Coverage × effective contrast has no published precedent
  (WCAG 1.4.3 and 1.4.11 are both ratios), half of what it would fail is decoration and no instrument
  can tell which half, and the face is not the terminal. **45 of the 79 meaning marks are under 3:1 on
  declared contrast at the seat the report picks** — labelled in the report itself as **the size of the
  question and not a count of violations**, because inc74 judged those seats one at a time and
  `DIM_CLASSIFIES` is the shape that answer takes.
- **Three questions are left for a ruling:** is it coverage × effective or two clauses with two floors;
  does it bind every meaning mark or only the ones a `DIM_CLASSIFIES`-shaped list says classify; is a
  mark judged at its worst seat or its declared one — **the answer changes which kits are in the top
  ten.**
- **solari's ruling-F failure is recorded and not fixed**, and so is the `w > 800` clause. Changing a
  law to make a red go away in the increment that found it is how a gate stops meaning anything.
- **No new dependency.** `fontTools` would have been the obvious way to ask which glyphs a face covers;
  the question is asked of FreeType instead — a glyph is missing when its bitmap equals what two absent
  codepoints draw — and the two methods were cross-checked (identical answers on four faces,
  4 / 4 / 64 / 87) before the dependency was declined.

### 20.6 The instrument, in numbers

```
face        Cascadia Mono 16 px, C:\WINDOWS\Fonts\CascadiaMono.ttf   (Windows Terminal's default)
cell        9 x 19 px, measured: advance 9.0, ascent 15, descent 4   (the .svg's 8.4 x 17 is nominal)
bold        the variable font's `Bold` instance, not a synthetic stroke
fallback    Segoe UI Symbol for the 4 cells Cascadia lacks -- the three circled operators and the dot
            operator -- at 11/11/11/16 px, centred
rejected    Cascadia Code (ligatures), Consolas (64 cells missing), Lucida Console (87)
corpus      206 distinct cells, 205 painted, 36 993 painted cells, 7081 distinct drawings
artefacts   66 png + 66 json (2.6 + 1.0 MB) - 1 report (591 lines) - 264 files at 80x24 (4.1 MB)
```

### 20.7 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief was the spec; this section is the record |
| Phase B (implement) | **done** — inc76, inc77, inc78 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1338 → 1370 passed** (+32), the clipboard test red at the baseline and named in every packet — environment-coupled (§10.6), reported, not counted, not touched. `verify_language.py` **ALL PASSED exit 0** at every increment. `render.py` 66 frames / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `collision_census.py` **TOTAL 28, homoglyph rows 24 — unchanged at every increment**. `raster.py` **66 PNGs identical across two PROCESSES**. `legibility.py` **byte-identical across two PROCESSES**. `second_width.py` 0 rows cut, 330 pairs distinct. `capture_languages.py` and `export_to_skill.py` **not run** — no kit, token or gallery artefact was touched, and running them would have been the only way to move one. |
| Notes | **Three increments, one agent, 2–3 source files each.** Eleven laws, two teeth, **zero kit edits**. The 66 `.txt`, the 66 `.svg`, the 22 gallery artefacts and the census are byte-identical to `0ec5904`. **E2 is closed as an instrument and none of the seven objections it was blocking has a verdict** — that is the fifth round's job, and this batch exists so it can fail in a way the fourth could not. |

## 21. Batch `rework-7c` — two defects `rework-7b` found by looking and did not fix

`rework-7b`'s own increments (inc77 §7.1, inc78 §5) named two defects in the INSTRUMENT itself — not in
a language — and declined to fix either inside the increment that found it, on the batch's own stated
principle: *"changing a law to make a red go away in the increment that found it is how a gate stops
meaning anything."* This batch is those two fixes, judged separately and later, by the same reasoning
that makes a postponed fix trustworthy: nobody was grading their own homework in the same breath they
wrote it.

### 21.1 What each increment did

| inc | defect | fix | files |
| --- | --- | --- | --- |
| 79 | `capture_languages.ink()` counted U+2800 BRAILLE PATTERN BLANK as ink — 421 cells over the 66 frames, instrument 174 and prism 247 — because it never read a `BLANKS` constant at all (it excluded space + U+00A0 NBSP, a set matching 0 characters in the corpus). `verify_ink.py`'s own `BLANKS` (inc44) already excluded the right pair. | `BLANKS` declared once in `capture_languages.py`, `ink()` reads it; a new law checks `verify_ink.py`'s own `BLANKS` against it by source text (restated and checked, not imported — importing `capture_languages` into `verify_ink.py` would pull in Textual and its `TEXTUAL_ANIMATIONS=none` side effect, changing the exact live-widget subsystem `verify_ink.py`'s own docstring names as an open, undiagnosed drift). | `prototypes/capture_languages.py`, `tests/test_components.py` |
| 80 | `test_a_confirm_opens_and_closes_on_marks_of_its_own`'s solari arm asserted "full measure" as `any(w > 800)` — `100 cols x 8.4 CW` with room to spare, true only at 100 columns. At 80 columns the page itself is 672 units and 800 is larger than the page, so the law read RED against a frame inc78 confirmed was correct. | The predicate reads the frame's own page width off its own canvas rect (`page_w = canvas_w - 2*PAD`) instead of a fixed constant, so it asks the same question at every width. `SECOND_WIDTH_RED` drops the now-green entry; the recorded-set test that pins it was checked by hand to still have teeth (staled the set back on a scratch copy, confirmed RED, reverted). | `tests/test_components.py` |

### 21.2 What this batch refused to do, and why each refusal is written down

- **inc79 deviated from the brief's literal instruction** ("move `BLANKS` to the module both already
  import") because no such module exists without either editing a kit file (`taskboard/themes.py`,
  explicitly off-limits) or importing `capture_languages` into `verify_ink.py` and inheriting a side
  effect (`TEXTUAL_ANIMATIONS=none`) onto a subsystem (`verify_ink.py`'s live mode) this batch was not
  asked to touch. The deviation — one definition enforced by a checked restatement instead of a runtime
  import — is named in `inc79.md` §0 for the round to overrule if it disagrees.
- **inc80 did not fix solari's ruling-F failure at 24 rows** (inc78's other red arm) — that is a HEIGHT
  finding about a language's placement rule, not a width-bound instrument defect, and the brief for
  `rework-7b` already ruled *"do not fix languages here; the round judges."* It remains red, on
  purpose, in `SECOND_WIDTH_RED`.
- **inc79 did not unify `collision_census.py`'s and `test_components.py`'s own `BLANKS` definitions**
  (a third and fourth copy of the same two-character constant) — both are already correct and neither
  consumes `capture_languages.ink()`; folding them in would have been scope beyond the brief's own two
  named files.

### 21.3 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief (this worktree's own instructions) was the spec; this section is the record |
| Phase B (implement) | **done** — inc79, inc80 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1370 → 1371 passed** (+1, inc79's law; inc80 adds none). The clipboard test red at the baseline and named in every packet — environment-coupled (§10.6), reported, not counted, not touched. `verify_language.py` **ALL PASSED exit 0** at both increments. `render.py` 66 frames / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `collision_census.py` **TOTAL 28, homoglyph rows 24 — unchanged**. `raster.py` **66 PNGs identical across two PROCESSES**. `second_width.py` 0 rows cut, 330 pairs distinct. `git status --porcelain` empty on every regenerated artefact directory (`prototypes/components/`, `.../png/`, `.../w80/`, `prototypes/gallery/`) at both increments. |
| Notes | **Two increments, one agent, 1–2 source files each, zero kit edits, zero frame/PNG/JSON changes.** Both fixes are to INSTRUMENTS the fifth round will use (a density reading, a suite law), not to a language. 421 ink cells reclassified as blank (console-printed density numbers only — instrument and prism, nothing else); one law-arm out of 79 flips from RED to GREEN, leaving solari's ruling-F failure at 24 rows as the one arm still red, on purpose. `rework-7b`'s close already named the fifth round as the next task; this batch changes nothing about that except making the instrument's own numbers trustworthy before the round reads them. |

## 22. Batch `rework-8` — the six reworks of `PROTOTYPE-inheritors-5.md`, and the three questions it answered

`PROTOTYPE-inheritors-5.md` is the first round in this programme that **looked**: 132 PNGs at Cascadia
Mono 16 px in a 9×19 box, at two widths. It returned **keep 14 · note 46 · rework 6**, refuted five
objections three rounds had treated as settled, inverted one, and raised four that only a raster can
raise. It also answered the three questions `legibility.py` §E had left open and recommended a
placement fix for solari. **This batch is those answers, taken.**

### 22.1 The rulings, as given

> (orchestrator, 2026-09-07, on the operator's delegation — all adopted from round five's own
> recommendations)
>
> **Q1** the legibility floor is two clauses, not a product: coverage ≥ 15 % of the cell AND effective
> contrast ≥ 3:1, both at the declared seat.
> **Q2** runs of 1–4 cells carrying an A-family role are bound by the floor; runs of ≥ 8 cells of one
> glyph are structure, bound only to "not equal to the ground"; 5–7 named per seat like
> `DIM_CLASSIFIES`.
> **Q3** the floor is judged at the declared seat; the worst seat is reported as a notice, never red.
> **F at 24 rows** the band takes the nearest full-measure position that cuts no gate block, below
> first then above; if neither fits, the band is the whole page (a full-screen confirm);
> `LANGUAGES.md` gets no minimum height.
> **K8/E6** a run of blank cells on a non-ground background is ink; the census, `painted_runs()` and
> `legibility.py` count it (18 runs in 3 kits today); it obeys Q2 as structure.
> **Greyscale** `raster.py` also writes a greyscale PNG per frame (luminance only); L12's three
> hue-only match channels are judged on it, and a match that vanishes in grey is recorded as a Limit
> of the language, not fixed.

### 22.2 What each increment did

| inc | ruling | what it did | frames |
| --- | --- | --- | --- |
| 81 | **Q1 Q2 Q3 · K8 E6** | the floor stops being a proposal. The DECLARED seat is derived from each kit's own contract methods — five calls, not fifty-five rows — intersected with the census's `role_map`; Q2's run classes are read off the `.txt`; `painted_runs()` walks the RECTS so a run with no glyph can be named. `legibility.txt` gains §F (the floor as law) and §G (the glyphless run). | **0** |
| 82 | **Q1**, the two marks the round returned | instrument `⠁` → `⣉` (5.8 % → 23.4 % coverage), prism `⡀` → `⣆` (5.3 % → 21.6 %). Both from the language's own alphabet, both AREA and only area; the declared ratios (16.52:1, 16.02:1 — the two **best** of the eleven) untouched. | **4** |
| 83 | **F at 24 rows · K10** | `Solari.band_head` stops walking gates and scans POSITIONS, below the named block then above, taking the whole page when neither fits. blueprint's four modal corners become a crosshair: a corner promises two walls at 44 cells' distance and a crosshair promises nothing. | **2** |
| 84 | **C12 C13 · greyscale** | the S6 key bar is DOCKED — a footer, at any height. `Kit.elide` marks a cut with the language's own `DISCLOSE`. `raster.py` writes 66 greyscale PNGs at WCAG relative luminance and `legibility.txt` gains §H. | **30** |

### 22.3 The findings, in the order they landed

1. **The round's own prediction is wrong by one, and it is the round's own arithmetic.** §7 Q1 says
   *«los once obligatorios pasan el contraste y dos fallan la cobertura»*. Measured at the declared
   seat, **three** fail: swiss `•` at **14.0 %**, one point under the 15 % the round set — on a mark
   the same round recorded as visible (§2.2 `swiss_S2`) in a document whose §7 also finds `naught ◦`
   at **13.5 %** by eye. **Neither the floor nor the mark was adjusted.** It is named in
   `OBLIGATION_UNDER_THE_FLOOR` with its measurement and handed back.
2. **Two floors in one repo contradict and nobody has ruled on which wins.** 29 of the 41 seats under
   Q1 miss the effective-contrast clause **only**, and they are overwhelmingly `mut` and `dim`: the
   severity rung inc74 moved to `mut`, and the invalid field's walls, which nine kits draw in `dim` as
   PAPER. K6 asks `mut` for **4.5:1 declared**; a thin glyph at 4.5:1 declared lands near **2:1
   effective**. Q1 is strictly the harder floor for anything that is not solid.
3. **The two clauses and the eye agree exactly where §7 said they would.** The 8 seats that miss BOTH
   are the marks round five listed as *"no se encuentra a ojo"*: the three `·` severity rungs,
   instrument `⠂`/`⠆`, prism `⣀`, naught `◦`.
4. **The glyphless run has two honest counts.** The sidecar's colour-run unit — the unit round five
   counted — gives **18** runs of ≥ 8 blank cells in 3 kits; the rect sweep, which subtracts the cells
   a glyph lands in, gives **60** in the same 3 kits. Both are true; the ruling names the first. And
   `solari_S4` row 10 has **no `<text>` element at all**, so every instrument that walks `<text>` was
   structurally incapable of reaching it — E6, as an assertion instead of a complaint.
5. **The shipped solari frames did not have to move.** The new position scan reproduces inc55's and
   inc65's anchors wherever they were already right, so `solari_S4` is byte-identical at both widths.
   What changed is two mechanism arms nobody could see (`about=BLOCKED` 10 → 23 at 32 rows,
   `about=DONE` 10 → 13) and the one that was red: at 24 rows a confirm about `DOING` now takes the
   whole page. **A rule can be wrong in three places and only fail in one.**
6. **The greyscale capture amends L12 rather than closing it.** Round five wrote *«en escala de grises
   no queda nada»* and could not check it. Checked: **none** of the hue kits reaches 1.00:1. A
   luminance step survives — nord 1.34, swiss 1.52, prism 1.59, instrument 2.34 against the body they
   stand in — thin, and **all four under 3:1**. Right in shape, wrong in degree. And there are **four**
   hue-only kits, not three: swiss has the same branch and round five discussed it without adding it.
7. **C13 reaches 21 frames at 80 columns, not 11.** The detail panel is drawn on `S1` **and on the
   board behind `S4`**, so the silent cut was in eleven `S1` and ten `S4` (corgi's confirm keeps no
   board).
8. **The key bar's position was wrong in all eleven, not four.** Round five counted the four that LOSE
   it at 24 rows; with `dock` reverted to `row` the bar is off the last row in **every** kit at 32 rows
   too. It was simply not fatal there.
9. **`test_win_clipboard_roundtrip` is demonstrably flaky, not deterministically red.** Five full-suite
   runs across this batch: **red, red, green, green, green**, with nothing it touches edited. It is the
   environment-coupled test this worktree's brief names — reported, not counted, not touched.

### 22.4 The laws this batch added

**Twenty-one laws and eight teeth**, `pytest -q` **1371 → 1449 (+78)**, and no increment imports
`raster.py` or `legibility.py` into the suite — the stance `test_this_files_picture_metrics_are_the_
exporters` has taken since inc73: the instrument's arithmetic is restated in the test file and checked
against the artefact it shipped, so the two can only agree by being right.

- **inc81** — Q1/Q2/Q3 over every meaning mark at its declared seat, with `BELOW_THE_FLOOR` as a
  recorded set (43 rows) asserted in both directions; the two clauses and the two run boundaries read
  off `legibility.py`'s SOURCE; Q2's middle band named per seat and every named row required to be
  reached; the 18 glyphless runs and Q2's structure clause; E6 as an assertion. **Teeth:** two rows of
  the recorded set removed one at a time; the plate repainted at the ground's own colour **in the
  sidecar, never in the corpus**.
- **inc82** — every REQUIRED mark clears Q1 at its own declared seat, with the exemption roster
  asserted in both directions; the before-mark **re-measured** through the same restated arithmetic.
  **Teeth:** the roster parked and emptied; and inc81's tooth **re-pointed**, because its original
  mutants were the two rows this increment removed — *a tooth whose mutant has been fixed is a tooth
  that bit.*
- **inc83** — ruling F two-branched over every gate at both heights, with `SOLARI_TAKES_THE_PAGE`
  recording the single whole-page case; K10 as a law about a PROMISE and not a distance (a kit in
  `MODAL_BORDER_REFUSED` spends none of the four CORNER cells of its own `MODAL_BOX` — corners, not
  strokes, because swiss and ledger rule their bands with `─` and neither claims a box).
  **Teeth:** inc55's placement rule re-installed and watched producing the old arithmetic (rows 17 and
  18 at 80×24, nothing at 100×32); blueprint's corners put back.
- **inc84** — the key bar present and last at both widths; `elide` marks with the language's own
  disclosure; no detail title cut without saying so at either width; the greyscale pass is the declared
  transform, pixel by pixel and colour by colour; L12 measured. **Teeth:** `dock` reverted to `row`;
  `elide` reverted to a bare slice.

### 22.5 What this batch refused to do, and why each refusal is written down

- **swiss `•` was not fixed and the floor was not lowered.** The brief named two marks; this is a
  third, and both available moves would have been an increment grading its own homework in the same
  breath it wrote it — `rework-7c`'s founding principle.
- **`collision_census.py` does not count the glyphless run and cannot.** It reads DECLARATIONS and
  never opens a frame; its `TOTAL` is a count of cells a kit declares, and a run that exists only in a
  picture has no declaration to be counted in. The frame-side count lives in `legibility.py` §G and in
  the suite. Named in `inc81.md` §7 for the round to overrule.
- **K10 is enforced as a promise, not as a distance.** A threshold would have to be invented inside the
  increment, would differ per glyph and per face, and round five's own §7 warns against exactly that.
  The 44-cells-versus-2 measurement is in the docstring as evidence and nowhere as a constant.
- **The one-gate fallback still lets solari's band sit inside the named gate.** That is inc55's second
  sentence, untouched, unreachable from any shipped frame, and asserted by its own law.
- **No minimum height was added to `LANGUAGES.md`**, per the ruling. solari renders at 24 rows; what it
  does there is take the screen.
- **The greyscale pass does not model colour vision deficiency**, and §H says so at length.

### 22.6 The artefacts

```
census        TOTAL 28 -> 27 (prism's `⡀` was REQUIRED and FIELD_LEAD's opener at once);
              homoglyph rows 24, unchanged
legibility    591 -> 870 lines; sections F (the floor as law), G (the glyphless run),
              H (the match in greyscale); MEANING_MARKS 45 -> 44 under 3:1 declared
raster        66 png + 66 grey.png + 66 json, 132 identical across two PROCESSES
frames        36 changed: 100x32 -- instrument_S2, prism_S2, blueprint_S4, 11 x S6
                          80x24  -- the same four, plus 11 x S1, 10 x S4, 9 x S6
gallery       30-51: NONE changed byte-wise.  `capture_languages.py` run plain at every
              increment that touched a kit; `git status --porcelain` empty on
              `prototypes/gallery/` every time.  The board and gallery frames draw no
              obligation mark, no modal and no key bar.
skill         `export_to_skill.py`: 11 languages round-trip, captures 0 written /
              66 already identical, SURFACES.md 11 postures.  The skill repo is not
              committed from here.
```

### 22.7 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief (this worktree's own instructions) was the spec; this section is the record |
| Phase B (implement) | **done** — inc81, inc82, inc83, inc84 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1371 → 1449 (+78)**. `test_win_clipboard_roundtrip` red at the baseline and in inc81/inc82, **green in inc83 and inc84** — environment-coupled, reported, not counted, not touched (§22.3.9). `verify_language.py` **ALL PASSED exit 0** at every increment. `render.py` 66 frames / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `collision_census.py` TOTAL **27**, homoglyph rows 24. `raster.py` **132 PNGs identical across two PROCESSES**. `legibility.py` **byte-identical across two PROCESSES**. `second_width.py` 0 rows cut, 330 pairs distinct, and **`SECOND_WIDTH_RED` is now empty** — 0 red, both solari arms. `capture_languages.py` 22 grids identical across two processes, gallery unchanged. `export_to_skill.py` clean. |
| Notes | **Four increments, one agent, 2–5 source files each.** Three of the six `rework` frames the round returned are answered (`instrument_S2`, `prism_S2`, `blueprint_S4`) and `solari_S4`'s two axes are both addressed without the frame moving. **`naught_S2` and `naught_S4` are untouched** — L10 and the `DANGER_FORM` frame are not in this brief and remain the round's oldest open reworks. Three questions go back: swiss `•` at 14.0 %, K6 against Q1, and L12 in its thin form. |

## 23. Batch `rework-8c` — the three questions `rework-8` handed back, and the programme's rulings in one table

`rework-8` (§22) closed with three things it deliberately did not do: swiss `•` at 14.0 % coverage,
K6 against Q1 on 29 seats, and L12 in the thinner form the greyscale capture proved. **The operator
delegated all three to the orchestrator; two increments, one agent.** The rulings are quoted verbatim
in each packet's §0 and are reproduced here, because a ruling that lives only in a chat is a ruling
nobody can argue with later.

### 23.1 The rulings, as given

> (orchestrator, 2026-09-07, on the operator's delegation)
>
> **swiss `•`:** the floor stays at 15 %; swiss's obligation mark is exempt by name (`SEEN_BY_EYE`)
> with round five's eye-read as the evidence and the human session as the review that can revoke it.
> Neither the floor nor the mark moves.
>
> **Q1 over K6 for marks:** Q1 governs meaning marks (runs of 1–4 cells carrying an A-family role);
> K6 governs text runs. Where a meaning mark is painted in `mut` or `dim` and fails Q1's effective
> contrast at its declared seat, the mark takes `ink` at that seat (inc74's `log_row` precedent),
> never a token move. Decorative seats (Q2's ≥ 8 structure and the named 5–7 table) are untouched.
>
> **L12:** a hue-only match channel that falls under 3:1 in grey is a Limit of that language,
> recorded in the kit docstring and in `spec.md`, not fixed.

### 23.2 What each increment did

| inc | ruling | what it did | frames |
| --- | --- | --- | --- |
| 85 | **Q1 over K6** | **26 seats leave the quiet tier for `ink`, no token moves.** 13 severity rungs through the module-level roster `language.RUNG_TAKES_INK` (eight kits, each row with its measurement); 13 invalid field WALLS through `Kit.field_wall_tone`, in all eleven, because all eleven missed — `═` at 1.11:1 effective, `░` at 1.05, `╲` at 1.14, `◑` and `Ø` at 1.18. The field's PAPER and the log MESSAGE both keep the quiet tier: they are structure and text, which is K6's half of the same ruling. | **19** at each width + 2 gallery |
| 86 | **swiss `•` · L12** | `SEEN_BY_EYE` — the programme's first exemption granted by a READING rather than a measurement, with three fields (the clause, the evidence and its citation, the review that can revoke it) and a STALE CHECK that goes red the moment the mark passes or the clause changes. L12 written as a LIMIT into the four hue-only kits' own docstrings with each kit's own grey number, and asserted against `MATCH_IN_GREY`. | **0** |

### 23.3 The findings, in the order they landed

1. **The one `mut` survivor of inc85 is not a mark at all — it is prose.** After the move,
   `darkside severity o #757575` is still under the effective clause, but its RUNG moved and measures
   8.34. What the row measures is the letter `o` of `form`, `log` and `fix login redirect`: **darkside
   is the only kit of eleven whose severity rung is a LOWERCASE LETTER**, so the census credits every
   `o` in the corpus to the severity family and the declared-seat derivation picks up the log MESSAGE.
   `legibility.py`'s own docstring claims the intersection with `role_map` prevents exactly this and it
   does not, because `role_map` is keyed by CHARACTER. **Before inc85 the defect was invisible** — the
   rung produced the same `(o, mut)` pair, so the row looked like a rung. Recorded, handed back as an
   instrument question, **not fixed inside the increment that found it**.
2. **Two seats moved and were not cured, and both are facts about the DRAWING rather than the tone.**
   `corgi ░` goes 1.05 → **1.44** in `ink` at 17.36:1 declared, because `░` is a DITHER and at 9×19 its
   lit pixels are almost all partway back to the ground. `ledger *` goes 1.91 → **2.86**, onto the row
   its own error rung already occupied, on the corpus's one light ground where `ink` is the loudest
   neutral there is. **No tier fixes either; only another cell would.**
3. **One seat moved that no measurement condemned, and the reason is the ladder.** industrial's rungs
   are `▫▫ / ▪▪ / ■■` and the HOLLOW square is thinner than the FILLED one at the same tier, so `info`
   missed at 2.77 where `warn` cleared at 3.73. Moving `info` alone would have shipped `ink / mut /
   ink` — the calm rung louder than the one above it. **A ladder that descends is not a ladder.**
4. **The bound-seat count FELL, 89 → 86, and it is arithmetic and not attrition.** A seat drawn in two
   tones is two rows; `ledger *`, `nord !` and `darkside o` each collapsed to one when the quiet copy
   moved onto the loud one. Both counts are asserted so that a seat which stops being DRAWN can never
   be mistaken for a seat that passed.
5. **The gallery is not immune this time, and exactly two grids moved.** Every `rework-8` increment
   could report *"gallery 30–51: none changed byte-wise"* because the board frames draw no obligation
   mark, no modal and no key bar. **They do draw an invalid field — in two of the eleven** — so
   `gallery_darkside.svg` and `gallery_solari.svg` changed and no other. Counted by looking for the
   mark, not inherited from the last four increments.
6. **`instrument ⠶` is the one kit where a field's wall and its paper are the SAME GLYPH**, so the seat
   split inc85 makes is visible inside a single field: `⠶` in `ink` at both ends, `⠶` in `dim` for the
   six paper cells between them, out of one contract call. It is the cleanest demonstration in the
   corpus that what moved is a SEAT and not a token.
7. **The eye exemption needed more machinery than a comment, and the reason is one sentence.** An
   instrument re-derives its own numbers every run; an eye cannot. So `SEEN_BY_EYE` carries WHO SAW IT
   and WHO CAN TAKE IT BACK as required fields, and the stale check is what retires it — because an
   exemption that can only be withdrawn by somebody remembering it is a hole with a citation.

### 23.4 The laws this batch added

**Six laws and two teeth**, `pytest -q` **1449 → 1466 (+17)**, and neither increment imports
`raster.py` or `legibility.py` into the suite — the stance this file has taken since inc73.

- **inc85** — `test_no_meaning_mark_that_only_misses_the_contrast_clause_is_left_quiet` (×11), the
  ruling's own sentence turned into a red, judged on the shipped pixels with the tier read off the
  theme and **symmetric** against `EFFECTIVE_UNCURED`;
  `test_every_seat_the_ruling_moved_is_drawn_in_ink_and_measured_there`, all 26 seats from both ends
  (tier from the kit, numbers from the pixels) with four clauses including *the move CLEARS the clause
  except where the roster says otherwise*, so a seat that moved and did not help cannot be counted as a
  fix; `test_the_uncured_table_covers_what_it_claims_to`, the roster's vacuity arms. **Teeth:** swiss
  removed from `RUNG_TAKES_INK` — and the arm had to be FOUND, because blueprint's warn and error are
  both `━` and nord's and ledger's warn rungs are the error glyph with a space, so reverting any of
  those three leaves the `(family, cell, ink)` triple standing on the error rung and the mutant passes
  with the seat quiet.
- **inc86** — `test_the_eye_exemption_is_named_measured_and_still_needed`, four clauses including *the
  two tables about this mark name the same mark* (`OBLIGATION_UNDER_THE_FLOOR` is inc82's measurement
  of it, `SEEN_BY_EYE` is inc86's exemption of it, and two tables drifting apart about one row is the
  failure `test_the_homoglyph_table_is_one_table_in_two_files` exists against);
  `test_the_hue_only_limit_is_written_into_the_kit_that_carries_it`, L12 in the four kits that have it
  and in no other, each with its own number to two decimals and the word LIMIT beside it. **Teeth:**
  the stale check, in two arms — the corpus with swiss's mark PASSING, and the corpus with swiss's mark
  missing a SECOND clause. Both must go red, because an exemption for a mark that no longer needs one
  and an exemption for a mark round five did not read are the same kind of stale.

### 23.5 L12, recorded as a Limit in the four kits that carry it

The ruling asks for the record, not the fix. Each number is the match ink against the body it stands
in, **on the greyscale PNGs**, and each is written into that kit's own class docstring beside the word
LIMIT and asserted against `MATCH_IN_GREY`:

```
instrument  2.34:1   the highest of the four, and the only one over 2:1
prism       1.59:1   the kit that already moved PRIORITY off hue for a nine-unit collision
swiss       1.52:1   round five's "la peor cifra del corpus", and a limit the kit's own
                     founding rule produces: no boxes, no markers, no drawn type
nord        1.34:1   the thinnest, and the one kit where the limit is DOCTRINE -- base16
                     inherits the user's palette and has by construction no identity of its own
```

**None of them reaches 1.00:1**, which is what inc84's capture already established against round five's
*"en escala de grises no queda nada"*; all four are under 3:1, which is why the objection survives in a
thinner form. What this batch adds is the DISPOSITION: a language may keep a channel it cannot widen,
provided the language says so where a reader will find it.

### 23.6 The programme's rulings, in one table

Every ruling this programme has taken, with the batch that issued it and the packet that carries it. A
ruling **recorded** is one that needed no code and says so; the section named is where it lives.

| ruling | batch | what it settles | carried by |
| --- | --- | --- | --- |
| **C** | `rework-5a` | a language's INVALID mark is its own, not a red glyph in eleven costumes | `inc52.md` |
| **C, follow-through** | `rework-6a` | the channel C freed on swiss gets filled: wall, paper, closer from swiss's own alphabet | `inc66.md` |
| **C1** | `rework-5a` | the knockout is a TIER over a whole seat, not a cell — `Kit.button(knockout=)` | `inc54.md` |
| **C2** | `rework-6a` | ledger's button states get their own two ends | `inc66.md` |
| **D** | `rework-5a` | a CHANNEL is defined in both instruments; the homoglyph roster is one table | `inc53.md` |
| **D, addendum** | `rework-5b` | recorded with `E`, on what a homoglyph pair may share | `inc55.md` |
| **D, amended (K2)** | `rework-6b` | the homoglyph list is DERIVED, not enumerated (48 pairs from families) | `inc68.md` |
| **E** | `rework-5b` | written: the exporter's own reading of ground and ink | `inc55.md` |
| **E4** | `rework-6a` | the exporter reads the kit's DECLARED ground; it never infers it from frequency | `inc63.md` |
| **E2** | `rework-7b` | the pairs four rounds argued about are irresoluble from the svg — build the raster | `inc76.md` |
| **E6** | `rework-8` | a frame row with no `<text>` element at all: asserted, not complained about | `inc81.md` |
| **F** | `rework-5b` | solari's band covers task rows of the first gate the confirm does not name | `inc55.md` |
| **F, amended** | `rework-6a` | the band never covers a gate HEADER row, of any gate | `inc65.md` |
| **F at 24 rows** | `rework-8` | the nearest full-measure position that cuts no gate block; the whole page if neither fits | `inc83.md` |
| **G** | `rework-5b` | the fixture's MOOD is derived from its own tasks, not asserted by a screen | `inc56.md` |
| **G vs ruling 10** | `rework-6a` | **recorded, no code**: the S4 fixture mood is calm, so G binds on S2 alone | `spec.md` §16.1 |
| **A** | `rework-5c` | the five languages that never had an increment get one each, guided by the laws | `inc58–61.md` |
| **A, amended (K5)** | `rework-6b` | the census's B set reaches every quantity widget; a fill cell is not a meaning | `inc67.md` |
| **L2** | `rework-6b` | a disabled control always carries a mark; air is not a state | `inc69.md` |
| **L7, measured** | `rework-7a` | the info rung is air by doctrine or legible by tier | `inc74.md` |
| **L8, L9** | `rework-6a` | prism's checkbox adds ink when ticked; the ember's DONE side is the fire | `inc64.md` |
| **`mut` contrast** | `rework-6b` | `mut` is body text: ≥ 4.5:1 against the declared ground, ladder kept ordered | `inc70.md` |
| **one rune** | `rework-6c` | the invalid field's RUNE is chrome; census and laws read it off ONE function | `inc71.md` |
| **solari `mut`** | `rework-6c` | **recorded as doctrine**: exempt by name with the arithmetic; the stale check stays | `inc71.md`, `spec.md` §18 |
| **K6** | `rework-7a` | contrast is measured against the background actually UNDER the run | `inc73.md` |
| **K7, `alert`** | `rework-7a` | `alert` ≥ 4.5:1 against every ground it is painted on, all eleven | `inc73.md` |
| **K7, `dim`** | `rework-7a` | `dim` ≥ 3:1 wherever it CLASSIFIES; a decorative seat is exempt by name | `inc74.md` |
| **match tier by channel** | `rework-7a` | legible against its own ground; DISTINCT on the channel `MATCH_STYLE` declares | `inc73.md` |
| **one token, one role** | `rework-7a` | ground-role and ink-role tokens are disjoint sets in `THEMES` | `inc73.md` |
| **C8, second half** | `rework-7a` | corgi's confirm gets walls from its display frame; blank rows are not a modal | `inc75.md` |
| **industrial `/`** | `rework-7a` | a field's paper and a value's separators may not be one glyph | `inc75.md` |
| **swiss `╎`** | `rework-7a` | **recorded, no code**: consistency with the kit's own dead cell stands | `spec.md` §19.1 |
| **inc60 info to air** | `rework-6a` | **recorded, no code**: absence is the calm state for blueprint and ledger | `spec.md` §16.1 |
| **K10** | `rework-8` | a modal border is a PROMISE, not a distance; four corners promise two walls | `inc83.md` |
| **K8 / E6** | `rework-8` | a run of blank cells on a non-ground background is INK, and is counted | `inc81.md` |
| **Q1** | `rework-8` | the floor is TWO CLAUSES: coverage ≥ 15 % **and** effective ≥ 3:1, at the declared seat | `inc81.md` (law), `inc82.md` (the two marks) |
| **Q2** | `rework-8` | runs of 1–4 are bound; ≥ 8 of one glyph is structure; 5–7 named per seat | `inc81.md` |
| **Q3** | `rework-8` | the floor is judged at the DECLARED seat; the worst seat is a notice, never a red | `inc81.md` |
| **C12, C13** | `rework-8` | the key bar is a footer and is DOCKED; a cut says so in the language's own mark | `inc84.md` |
| **greyscale** | `rework-8` | `raster.py` writes a grey PNG per frame at WCAG relative luminance | `inc84.md` |
| **Q1 over K6** | `rework-8c` | Q1 governs meaning marks, K6 governs text runs; a quiet mark takes `ink` at the seat | `inc85.md` |
| **swiss `•`** | `rework-8c` | the floor stays at 15 %; the mark is exempt by name, by an EYE, revocable by review | `inc86.md` |
| **L12** | `rework-8c` | a hue-only match under 3:1 in grey is a LIMIT of that language, recorded not fixed | `inc86.md` (measured in `inc84.md`) |

**Forty-three rows and four of them are `recorded, no code`.** That proportion is the point of the
table: a programme that only wrote down the rulings it implemented would have no record of the four
questions it answered by deciding nothing had to move.

### 23.7 The artefacts

```
legibility    870 -> 867 lines; section F re-measured -- 89 bound seats / 41 fail
              becomes 86 / 18, with effective-only 29 -> 6.  MEANING_MARKS 44 -> 38
              at the worst seat (Q3's notice), which moves independently of the
              declared-seat count and is asserted separately.
census        TOTAL 27, homoglyph rows 24 -- BOTH UNCHANGED.  A tier is not a
              declaration `collision_census.py` counts.
raster        132 identical across two PROCESSES (66 colour + 66 grey)
frames        19 changed at each width -- 11 x S2 (the invalid field, all eleven)
              and 8 x S5 (the rung, the eight kits in RUNG_TAKES_INK).
              ZERO .txt moved, at either width: colour only, which is what a tier
              move is.  corgi_S5, naught_S5 and instrument_S5 did not move.
gallery       gallery_darkside.svg and gallery_solari.svg -- the only two of the
              22 grids that draw an invalid field.  The other 20 byte-identical.
skill         `export_to_skill.py`: 11 languages round-trip, captures 2 WRITTEN and
              64 already identical -- the two gallery grids inc85 moved -- and
              SURFACES.md 11 postures.  The skill repo is not committed from here.
```

### 23.8 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief (this worktree's own instructions) was the spec; this section is the record |
| Phase B (implement) | **done** — inc85, inc86 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1449 → 1466 (+17)**, **zero failed** at both increments; `test_win_clipboard_roundtrip` green in both runs — environment-coupled, reported, not counted, not touched. `verify_language.py` **ALL PASSED exit 0**. `render.py` 66 frames / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` for all eleven. `collision_census.py` TOTAL **27**, homoglyph rows **24**, both unchanged. `raster.py` **132 PNGs identical across two PROCESSES**. `legibility.py` **byte-identical across two PROCESSES**. `second_width.py` 0 rows cut, 330 pairs distinct. `capture_languages.py` 22 grids identical across two processes. `export_to_skill.py` at the close: 11 languages round-trip, **captures 2 written / 64 already identical** (the two gallery grids inc85 moved), SURFACES.md 11 postures. The skill repo is not committed from here. |
| Notes | **Two increments, one agent, ≤ 4 source files each.** All three of `rework-8`'s handed-back questions are answered. What goes back to the round: the `darkside o` derivation defect (§23.3.1, an instrument question this batch found and refused to fix in the increment that found it); the three cursors in `accent`, which fail Q1's effective clause as a FAMILY and which the ruling does not reach; `corgi ░` and `ledger *`, which no tier in their own kit can fix; and the eight seats that miss BOTH clauses, which want inc82's kind of move — a glyph out of the language's own alphabet. **`naught_S2` and `naught_S4` remain untouched**, as they have since `rework-8`: L10 and the `DANGER_FORM` frame are the round's oldest open reworks and are in no brief yet. |

---

## 24. Batch `rework-9` — the floor emptied of everything but area, and the one alphabet that ran out

`rework-8c` (§23) closed with five things handed back to the round. **The operator delegated all five
to the orchestrator; four increments, one agent.** This section is the record. Every ruling is quoted
verbatim in each packet's §0 and reproduced here, because a ruling that lives only in a chat is a
ruling nobody can argue with later.

### 24.1 The rulings, as given

> (orchestrator, 2026-09-07, on the operator's delegation)
>
> **Declared seat by seat, not by character:** the declared-seat derivation intersects the mark with
> the seat its contract method paints (`log_row`'s rung column, not any cell with the same
> character); prose never counts.
>
> **Cursors are marks:** the three cursors in `accent` (instrument `⣿` 2.94, swiss `▮` 2.57,
> industrial `▶` 2.97) obey Q1's effective clause; fix by the smallest hue-preserving lightness step
> of `accent`, and re-run the match-tier law (inc73) since `accent` is a match ink in some kits: both
> must hold.
>
> **Drawing problems are fixed by drawing:** corgi's invalid wall `░` (1.44 in ink, a dither) takes
> the heavy shade `▓` (panel register, inc67), and ledger's warn rung `*` (2.86 on light paper) takes
> a heavier printer's mark by area from ledger's own alphabet (`¶`, `§`, `※` or `**`'s sibling; cite
> #9 and keep error distinct), both judged by Q1 at the seat.
>
> **Both-clause seats move by area** (inc82's kind): the eight seats failing coverage AND contrast
> take a bigger glyph from their language's alphabet; `naught ◦` (13.5 %) is among them and gets no
> eye exemption.
>
> **naught_S2 L10:** the 12 homoglyph rows and 8 state rows on naught's form are fixed by SHAPE and
> COUNT (the lattice counts, the pixel charges: inc61), so the form's marks stop resting on one
> drawing.
>
> **inc84 §6 correction:** the packet's claim "gallery 30–51 none changed" was read off
> `prototypes/gallery/` (boards), not the component grids; entries 35 and 36 did change. Correct the
> packet in place with a dated note, never silently.

### 24.2 What each increment did

| inc | ruling | what it did | frames |
| --- | --- | --- | --- |
| 87 | **declared seat · inc84 §6** | The derivation intersected `role_map` (keyed by CELL) with every character of every toned run, so darkside — the one kit of eleven whose rung is the letter `o` — had the `o` of `board loaded` credited to severity. Each contract call now declares the PROSE it hands in; the columns that text fills are struck before the intersection. **Two rows left the floor table and neither was a mark.** `inc84.md` §6 corrected in place, dated: two directories in this repo are called "gallery" and the packet checked the wrong one. | **0** |
| 88 | **cursors · corgi `░` · ledger `*`** | The three cursors take the smallest hue-preserving lightness step of `accent`, walked at 0.0002 of a turn so every smaller step is measured and misses. corgi's invalid wall goes `░░·░░` → `▚▚·▞▞` — **the ruling's `▓` was refused, measured**. ledger's rung advances along its own printer's order, `* † ‡ § ‖ ¶`, to `§`. **The `EFF`-only column empties.** | **3** `.txt` + 21 `.svg` at each width |
| 89 | **both-clause seats** | Five of the six severity ladders take a bigger cell out of their own alphabet, each along the axis its kit declares; the area move drags the tier with it and `RUNG_TAKES_INK` goes 8 kits to 10. **naught is refused by an enumeration** — the ruling's move was made, measured and rejected by two standing laws. **The both-clause column empties.** | **6** `.txt` at each width |
| 90 | **naught_S2 L10** | L10 enumerated: twenty rows on **nine drawings**, fourteen pairs with the distance between each, three channels and the reason the language can spend none of them. The refusal is a roster with teeth, not a sentence. | **0** |

### 24.3 The findings, in the order they landed

1. **The ruling named one kit and the mechanism found a second, in a family nobody was looking at.**
   `industrial invalid / #f2f2f2` was **passing** at 5.02 — and the cells it was passing on were the
   two slashes of the date `12/09/26` the field had been handed. industrial declares `/` as the
   INVALID mark of its slider knob and its stepper step, and those two seats have **no contract call
   of their own**, so the mark had never been measured at its own seat and still has not been.
2. **inc84 checked the wrong directory and the mistake is structural, not careless.**
   `prototypes/gallery/` holds the 22 board and component GRIDS `capture_languages.py` writes; the
   skill's `assets/gallery/` holds the 22 numbered frames **30–51**, each a copy of one sheet in
   `prototypes/components/`. Entries **35 `corgi_S6`** and **36 `ledger_S6`** did change. Verified two
   ways and cross-read against the four entries `inc67.md` names and the one `inc69.md` corrects.
3. **The cell the ruling named for corgi would have re-created the defect inc52 fixed, and the census
   said so in one number.** `▓` clears Q1 comfortably and is the cell corgi's textfield already wears
   when it is ACTIVE — and seven other components'. Taking it put the census at **28** with `▓`
   carrying **nine families**. That is ruling C reversed. The criterion inc52 stated was kept and the
   family moved instead.
4. **And the cell taken instead closed a collision nobody was aiming at.** `░` was never as free as
   inc52's comment claimed: `meter.track`, `spark.floor` and `scrollbar.main` all spend it, and
   inc67's ruling A-amended brought those into the census two batches AFTER inc52 wrote the sentence.
   corgi 4 → 3 colliding cells; **TOTAL 27 → 26**.
5. **swiss's one red cannot be both inks, and the arithmetic is a scissors.** Q1 pushes the cursor's
   ink UP in lightness; inc73's achromatic fallback asks the match ink to stay 1.5:1 away from `mut`,
   which pushes it DOWN. The whole-token move was made first and measured — the match law went red at
   **1.26** against a floor of 1.5 — so `accent` moved alone. The kit still spends one HUE at two
   lightnesses, which is what its own grey ladder does three times over.
6. **`‖` is not in the measured face, and the fallback box is how you can tell.** Eleven candidate
   glyphs return **39.2 % coverage at 6.24 effective**, to six digits, because they are all the same
   tofu rectangle. `raster.py` declares the four the corpus uses and asserts the set is exactly those,
   so the gate would have caught a twelfth — but not a candidate chosen from a list read by eye, and
   this batch came within one row of taking `‖` as ledger's next printer's mark for that reason.
7. **The invisible calm rung was also the wrong drawing, and only one of those two facts had an
   instrument.** Three of the six calm rungs were the identical character `·` in three languages that
   share no other cell, and `·` is a homoglyph of `●` — what a radio and a checkbox rest on. Fixing
   the one that could be MEASURED (area) closed the one that could only be argued (shape): census
   26 → **23**, homoglyph rows 24 → **22**.
8. **darkside is the first language of the eleven with NO cell doing two jobs.** Its colliding-cell
   count goes 1 → 0 and the census's own line changes from *"zero collisions: NONE — all eleven
   overload at least one cell"* to *"zero collisions: darkside"*. Eleven batches of ruling D reached
   one; a ruling about legibility reached the last one.
9. **Closing the last live `FOUND_BY_HAND` row tripped that roster's vacuity guard, and the guard was
   right.** Two live rows were added the way the original five were found — by opening a frame and
   looking — rather than by relaxing the guard: `blueprint ━` and `corgi █`, where the error rung and
   the danger form are one cell.
10. **naught's alphabet ran out, and it had said so four batches ago.** The ruling's move
    (`○○ / ⬤○ / ⬤⬤`) was made and measured before it was refused: `○` OPENS four controls and that
    law has had no exemptions since inc52, and the three circles the face has that naught does not
    spend are **all larger than its gravest rung**. `spec.md` §11.5 wrote the limit long before:
    *"naught and solari have no unspent cell left."*
11. **L10 is twenty rows on nine drawings, and that is this language's founding rule measured.**
    Three solid dots at three sizes (`⋅ ∙ ●`) and six ringed things at six diameters and fills
    (`◦ ○ ◎ ◉ ⊙ ⊛`). The tightest pair is **`○` against `◉` at 5.82 %** — `stepper.step` focused
    against active — within a point of the tightest pair in the whole corpus.
12. **Three teeth in three increments had to be re-pointed, and every one was a tooth that bit.**
    `test_the_floor_law_bites_on_a_row_of_the_recorded_set` has now been re-aimed twice; the invalid
    channel's and the opener's each needed a second restore, because the historical declaration they
    put back no longer collides with a ladder that has moved. All three now restore the pre-inc89
    `LEVELS` alongside the pre-inc52 or pre-inc46 table.

### 24.4 The floor, batch to batch

```
                        bound   pass   FAIL    COV   EFF  COVEFF
rework-8c close (inc86)    86     68     18      4     6       8
inc87 (derivation)         84     67     17      4     5       8
inc88 (hue and drawing)    85     73     12      4     0       8
inc89 (area)               83     79      4      4     0       0
```

**`BELOW_THE_FLOOR` is 18 rows → 4, and the four are one number.** Every remaining seat measures
**exactly 14.0 %** of the cell — one point under a clause the round set at 15 % — and it is asserted,
because a reader who does not know it will read four failures where there is one:

```
naught      severity ∙ #f5f5f5  COV   14.0%   9.66   the disc
naught      severity ◦ #f5f5f5  COV   14.0%   5.68   the ring; §24.3.10
naught      danger   ∙ #f5f5f5  COV   14.0%   9.66   DANGER_FORM, in no brief
swiss       required • #f4f4f4  COV   14.0%   9.13   exempt by EYE (inc86)
```

**Three of the four are one kit's, and they are one alphabet's ceiling rather than three defects.**

### 24.5 The laws this batch added

**Eleven laws and seven teeth**, `pytest -q` **1466 → 1499 (+33)**, and no increment imports
`raster.py` or `legibility.py` into the suite — the stance this file has taken since inc73.

- **inc87** — `test_the_declared_seat_is_a_column_the_contract_paints_not_a_character` (×11): the
  mechanism strikes columns and the law never mentions columns. It swaps the caller's words twice —
  once for text the kit credits to nothing, once for **the kit's own severity ladder repeated to the
  same twelve columns** — and requires the seats to be identical both times. **Teeth:** the strike
  itself is mutated back to the character scan, and three separate laws must notice.
- **inc88** — `test_the_cursor_took_the_smallest_hue_preserving_step_that_clears` (×3), whose fifth
  clause is the word SMALLEST: every colour the hue's own ray can reach between the two must still
  miss. `test_the_swiss_red_is_one_hue_at_two_lightnesses_and_says_why`.
  `test_a_mark_no_tier_could_fix_took_another_cell_of_its_own_alphabet` (×3), whose fourth clause is
  ruling C measured. `test_the_cell_the_ruling_named_is_one_the_census_refuses` — a refusal that is a
  COUNT. **Teeth:** an overshoot by ONE colour on the same ray, and corgi's wall set to the cell the
  ruling named.
- **inc89** — `test_a_severity_ladder_that_missed_by_area_took_a_bigger_cell` (×5), which records
  BOTH coverage tables because "bigger" is a comparison; `test_the_ladder_naught_could_not_move_is_refused_by_an_enumeration`,
  which walks the refusal. **Teeth:** each ladder put back and re-measured, and **the raid the
  refusal refuses, executed** — naught's ladder set to `○○ / ⬤○ / ⬤⬤` with the four opener hits
  named.
- **inc90** — `test_l10_is_twenty_rows_on_nine_drawings_and_names_why_each_stands` and
  `test_the_two_channels_the_l10_ruling_names_are_both_blocked`. **Teeth:** the roster in both
  directions, and one control seat made to draw the lit lattice dot — inc61's rule executed rather
  than quoted.

### 24.6 What this batch refused to do, and why each refusal is written down

- **corgi's `▓`.** §24.3.3. The refusal is a number (nine families, census 27 → 28), a law, and a
  tooth that takes the cell.
- **naught's `○`.** §24.3.10. The refusal is an enumeration, a law that walks it, and a tooth that
  performs the raid.
- **L10's redrawing.** The ruling names two channels; **this language can spend neither** and inc90
  proves both blocked. What L10 needs is a cell naught does not have, and the one real second channel
  it does have — the circled operator's interior mark — has three of its five members outside the
  measured face already. **Widening `FALLBACK_CELLS` is a new alphabet for a language and needs a
  round, not an increment.**
- **`slider` and `stepper` get no seat call.** §24.3.1. Adding two would change the bound count in
  the same increment that changed the derivation, and the two effects would be unreadable apart.

### 24.7 The artefacts

```
legibility    867 -> 876 lines.  Section F: 86 bound / 18 fail -> 83 / 4, with
              effective-only 6 -> 0 and both-clause 8 -> 0.  MEANING_MARKS
              (79, 38) -> (80, 32).
census        TOTAL 27 -> 23; homoglyph rows 24 -> 22; darkside 1 -> 0
              colliding cells, the first zero in eleven languages.
              FOUND_BY_HAND: instrument `⠇` closed by inc89, two live rows
              added by looking because the vacuity guard demanded them.
raster        132 identical across two PROCESSES (66 colour + 66 grey)
frames        inc87 0 · inc88 3 .txt + 21 .svg at each width · inc89 6 .txt at
              each width · inc90 0.  Nine `.txt` in total, at both widths.
gallery       inc88 6 artefacts (3 frames: industrial, instrument, swiss);
              inc87, inc89 and inc90 none.
gallery 30-51 read off `prototypes/components/`, and byte-wise in `.txt`:
              inc87 none · inc88 entry 40 `ledger_S2` · inc89 entry 51
              `instrument_S5` · inc90 none.  inc84's own claim corrected in
              place: entries 35 `corgi_S6` and 36 `ledger_S6`.
skill         `export_to_skill.py` at the close: 11 languages round-trip,
              captures 6 WRITTEN and 60 already identical (the six gallery
              artefacts inc88 moved), SURFACES.md 11 postures; re-run gives
              0 written / 66 identical.  The skill repo is not committed.
```

### 24.8 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief (this worktree's own instructions) was the spec; this section is the record |
| Phase B (implement) | **done** — inc87, inc88, inc89, inc90 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1466 → 1478 → 1488 → 1496 → 1499 (+33)**. `test_win_clipboard_roundtrip` is environment-coupled: green in the inc87 and inc88 runs, red in the inc89 and inc90 runs, **reported in every packet, counted in none, and not touched**. `verify_language.py` **ALL PASSED exit 0** after every increment. `render.py` 66 `.txt` + 66 `.svg` / 330 pairs / 0 hand-drawn, every time. `raster.py` **132 PNGs identical across two PROCESSES** (66 colour + 66 grey), every time. `legibility.py` **byte-identical across two PROCESSES**, every time; 867 → 876 lines. `second_width.py` 0 rows cut in 0 frames, 330 pairs distinct. `matrix.py` refusals `[]` for all eleven. `collision_census.py` TOTAL **27 → 23**, homoglyph rows **24 → 22**, both self-checks green. `capture_languages.py` run plain at inc88 and inc89: 22 grids identical across two processes. `export_to_skill.py` at the close: **6 written / 60 identical**, re-run **0 / 66**. |
| Notes | **Four increments, one agent, ≤ 4 source files each.** All five of `rework-8c`'s handed-back questions are answered — four by a fix and the fifth (§23.8's `naught_S2`) by an enumeration with teeth. What goes back to the round: **naught's three 14.0 % rows and L10**, which are one alphabet's ceiling and want a cell the language does not have; the **slider's and the stepper's invalid marks**, which have no contract call and are therefore unmeasured at their own seat; the **census total**, which moved twice in this batch and is pinned by no law; and **`naught_S4`**, the `DANGER_FORM` frame, which has still been in no brief. |

---

## 25. Batch `rework-10` — the round that pressed a key, and the four rounds' worth of objections it found in one afternoon

`PROTOTYPE-inheritors-5.md` converged on a single sentence rather than a list: *«una tecla:
`App.run_test()` + `Pilot`, cinco rondas sin usar; un frame no puede fallar en foco porque un frame no
tiene foco.»* `SESION-PERSONA.md` §7.3 said the same from the other side, in the list of what a human
session cannot see. **The operator delegated it to the orchestrator; three increments, one agent.**
This section is the record. Every ruling is quoted verbatim in each packet's §0 and reproduced here,
because a ruling that lives only in a chat is a ruling nobody can argue with later.

### 25.1 The rulings, as given

> (orchestrator, 2026-09-07, on the operator's delegation)
>
> **A frame has no focus; the round presses keys.** The instrument is `App.run_test()` + `Pilot` on
> the widget slice, per language, driving a fixed script and capturing the screen after each key
> through the same `cell_grid` the raster uses.
>
> **L12 corrected:** the match channel in grey is weight or decoration where the kit declares it, and
> the grey test reads the sidecar's `bold`/`underline` flags, not colour tokens; a kit is hue-only in
> grey only if its match run carries neither.

### 25.2 What each increment did

| inc | ruling | what it did | frames |
| --- | --- | --- | --- |
| 91 | **the key instrument** | `prototypes/components/keys.py`: the real `TaskboardWidget` driven through six steps in eleven languages at 100×32, read through `capture_languages.cell_grid`. 66 frames × `.txt` + `.svg` + `.png` + a sidecar carrying the focused widget's id, class and screen RECTANGLE, the modal box's rectangle and the settle read count. **44 of 66 laws hold; K5 and K6 fail in all eleven and neither failure is language-shaped.** Recorded with a stale check, not fixed. | **66 new** |
| 92 | **L12 corrected** | `match_branch()` read `MATCH_STYLE`'s TOKEN and returned `hue` in a branch that never looked at the STYLE WORD, so four kits were filed as hue-only while all four are painted with a second channel the raster's sidecar has recorded since inc43. Read off the paint now; the grey law is three clauses measured on the grey PNG. **Eleven of eleven have weight, decoration or both; the hue-only Limit has no members.** | **0** |
| 93 | **the two defects** | `Kit.palette()` — the command palette in the language, with the match highlight DERIVED from `MATCH_STYLE`. `ConfigScreen`'s threshold gets a keyboard, so the INVALID state eleven kits draw is reachable by a key for the first time. **66 of 66 laws hold.** And `PROTOTYPE-inheritors-6.md`: **keep 33 · nota 12 · rehacer 21.** | **22** (`K5`, `K6` ×11) |

### 25.3 The findings, in the order they landed

1. **Two of the six steps could not be pressed at all, and both were states the corpus DRAWS.** The
   INVALID mark eleven kits declare at `S2` — whose two walls inc85 moved into `ink` in every one of
   them because a refusal is a meaning mark — was reachable by no key in any language. Eleven
   languages drew a refusal nobody could provoke, and `textfield_block`'s docstring had said why since
   pass 53: *"nothing in the engine is TYPED."*
2. **The command palette was byte-identical in all eleven.** Its eight rows, run-encoded, collapse to
   ONE distinct block: Textual's `#141f27` slab, its `#0e395a` cursor row, and a `bold underline`
   highlight on a colour no kit declares. On ledger, the corpus's one light-paper kit, that was a
   night-mode slab laid across the middle of the page.
3. **`match_branch()` returned before it used its own second variable, for two batches.** inc84
   measured L12 and inc86 recorded it in four kit docstrings; both used a classification that read the
   token and never the word. **The evidence had been on disk since inc43**, when `cell_grid` started
   returning `bold` and `underline` — *"66 declared runs across the eleven S6 sheets, none painted"* is
   that increment's own line — and the measurement three batches later went round it to the tokens.
4. **swiss is the one seat in the corpus where AREA and DEPTH disagree.** Its match covers 1.21× the
   lit area of the body beside it and carries 1.07× its ink, because its red falls darker than the
   grey of that body. A single number would have had to choose between *"heavier"* and *"fainter"* and
   both are true of different halves of the same measurement.
5. **The notice that started inc92 does not reproduce, and the way it fails is informative.**
   `SESION-PERSONA.md` §3 measured four ink ratios; this tree's are **1.28–1.30× higher on all four**,
   one constant factor, same ordering. The two measurements differ by a definition and not by a
   reading — and the one place it matters is swiss, where the notice says FAINTER and the tree says
   barely HEAVIER, which is exactly why the ruling did not rest swiss on the number.
6. **The K5 law was wrong twice, in opposite directions.** Asked as a character scan it passed on
   instrument (5 cells) and industrial (2) on a screen with NO field — `spec.md` §23.3.1 one
   instrument out. Asked as wall + PAPER + wall, `field_wall_tone`'s own doctrine, it found nothing at
   all, because a field showing an eight-character value in an eight-cell window draws no paper. It
   asks for wall + THE VALUE + wall, which no kit's chrome can satisfy because no kit's chrome spells
   `12/99/26`.
7. **The typed seat ate its own screen's `r`, and the new instrument was blind to it.** Taking any
   printable character swallowed the refresh key; `verify_language.py`'s drive-check went red in four
   clauses at once. **No step of the key script presses `r`**, so the instrument this batch built could
   not see the defect the batch introduced, and the older instrument caught it.
8. **Focus in this app is ONE CSS rule and ONE token, and the token fails in two opposite ways.**
   Measured on the seat that takes focus: eight kits move one glyph (the border cell) and a row of
   grounds; ledger, solari and blueprint move NONE — `sel: none`, so focus is colour alone, against
   this corpus's *"states may never ride colour alone"* and against ruling L2. And on the hero the
   ring is a full border, so **letting go of focus redraws the hero's content in eight of eleven, up
   to 342 cells.** No kit declares a focus mark; there is no `Kit.FOCUS` as there is a `Kit.CUR`.
9. **The one modal the app has breaks the law the sheet sweep enforces.** `render.py`: *"for each
   screen, no two languages may render byte-identically."* The eleven `K3` frames are **four texts**,
   and the largest group has **five members**. The cause is structural: `HelpScreen` composes the
   App's own `BINDINGS` through `LG.mark()`, so a kit reaches the modal only where it transforms text.
10. **`reverse` does not reach the palette, and it is Textual's limit.**
    `Widget.get_visual_style(..., partial=True)` builds its `VisualStyle` from five flags and `reverse`
    is not among them; an opaque background in a partial style resolves to transparent by that
    function's own blend. Three kits lose the channel they declare and **solari loses the distinction
    entirely**: its match ink is the ink of the row it stands in.
11. **The corpus met its first double-width cell, and nobody chose it.** The palette's prompt is
    `U+1F50E` — two columns, absent from the measured face, and the only cell in 66 key frames that
    neither a kit nor a screen picked. `keys.py` widens the grid so column N of the raster is column N
    of the terminal, and the glyph itself is left for a contract seat that does not exist.
12. **The frame is deterministic and the number of looks it takes to settle is not.** 264 artefacts
    are byte-identical across two processes; `settle_reads` lands on 8, 9, 10 or 12. It is in the
    sidecar, it is masked from the bargain by a named constant (`UNPINNED`), and it is the one thing
    in this corpus that changes on disk without anything having moved.

### 25.4 The key round, step by step

```
                        K1     K2     K3     K4     K5     K6
inc91 (recorded)     11 ok  11 ok  11 ok  11 ok   0 ok   0 ok    44 / 66
inc93 (fixed)        11 ok  11 ok  11 ok  11 ok  11 ok  11 ok    66 / 66
```

And the ROUND's verdicts over the same 66, which are not the same question:

```
                       keep   nota   rehacer
K1 initial                0      8         3
K2 focus                  8      0         3
K3 modal                  1      0        10
K4 escape                11      0         0
K5 invalid                5      3         3
K6 match                  8      1         2
                    -------------------------
                         33     12        21
```

**Only `K5` and `K6` are shared out by language.** The other four steps have one verdict per CAUSE,
and the four causes live in `themes.tcss()`, in `HelpScreen` and in Textual. A round that set out to
judge eleven languages found that **four of its six columns are not about the languages**.

### 25.5 L12, corrected and re-measured on the grey PNG

```
kit         declared            painted     eff    ink    cov   carried by
naught      bold {ink}          bold       3.33   2.50   1.22   effective + weight
corgi       bold {ink}          bold       2.70   2.29   1.22   weight
instrument  underline {accent}  underline  2.31   2.42   1.30   weight + decoration
swiss       bold {alert}        bold       1.17   1.07   1.21   weight (coverage arm)
industrial  reverse {accent}    reverse    1.60   5.16   3.60   weight + decoration
nord        bold {accent}       bold       1.44   1.74   1.22   weight
darkside    reverse {mut}       reverse    1.61   5.14   3.60   weight + decoration
prism       bold {accent}       bold       1.76   1.82   1.22   weight
ledger      underline {ink}     underline  2.24   2.21   1.30   weight + decoration
solari      reverse {ink}       reverse    6.25  12.21   3.60   effective + weight + decoration
blueprint   bold {ink}          bold       2.27   2.47   1.22   weight
```

**0 kits carry the match on HUE ALONE.** What survives is thinner and is written into the four
docstrings inc86 wrote the false version into: none of those four clears the EFFECTIVE clause in grey
(2.31, 1.76, 1.44, 1.17 against a floor of 3), so **the match is found in grey by 21–30 % of AREA and
not by tone**. Whether an eye finds 21 % of area is the human session's question and nobody has asked
it — and `SESION-PERSONA.md`'s `F15`–`F22` were chosen off the reading this batch corrects, so **the
eight frames are still the right eight and the question they ask has changed**.

### 25.6 The laws this batch added

**Nineteen laws and six teeth**, `pytest -q` **1499 → 1561 total (+61: inc91 +37, inc92 +1, inc93
+24)**, and no increment imports `raster.py`, `legibility.py` or `keys.py` into the
suite — the stance this file has taken since inc73.

- **inc91** — `test_the_key_script_the_frames_were_taken_with_is_the_one_declared` (the script
  declared a second time, so the two can only agree by somebody editing both);
  `test_the_seat_that_holds_focus_is_drawn_differently_when_it_holds_it` (×11), the first law in this
  corpus that could ever fail on focus; `test_a_modal_draws_a_band_and_the_band_is_the_kits_own_panel`
  (×11); `test_escape_gives_back_the_page_the_modal_covered` (×11), whose second clause is its own
  tooth (K4 ≠ K1, or the app threw the focus walk away);
  `test_the_two_states_no_key_can_reach_are_recorded_with_a_stale_check`;
  `test_the_live_search_seat_prints_a_cell_the_measured_face_has_not_got`. **Teeth:** the record law's
  vacuity arm, which builds the frames the app does NOT produce out of each kit's own `field_form` and
  `MATCH_STYLE` and requires both measurements to find them.
- **inc92** — `test_the_match_channel_in_grey_is_weight_or_decoration_and_not_hue`, five clauses
  including *exactly one kit needs the coverage arm and it is swiss*;
  `test_the_four_kits_the_old_table_named_carry_the_corrected_limit`, whose last clause is that the
  sentence inc92 disproved is GONE from the docstring. **Teeth:**
  `test_the_grey_match_measurement_can_tell_a_channel_from_no_channel` — the run against itself must
  read 1.00×, and the comparison turned round must read under one, so the number has a direction.
- **inc93** — `test_the_invalid_state_is_reachable_by_a_key_in_every_language` (×11);
  `test_the_palette_paints_the_match_in_the_kits_own_ink` (×11), row-bound;
  `test_the_palettes_one_missing_channel_is_the_frameworks_and_is_named`;
  `test_the_focus_ring_is_a_ground_in_eleven_and_a_glyph_in_only_eight`;
  `test_the_one_modal_the_app_has_breaks_the_law_the_sheets_obey`. **Teeth:**
  `test_the_two_seats_inc93_fixed_are_measured_and_not_assumed`, whose second arm is why the match law
  is row-bound — written frame-wide it went red on swiss, whose match ink is `alert` and whose
  aperture spends `alert` bold on an overdue chip.

### 25.7 What this batch refused to do, and why each refusal is written down

- **The palette's prompt glyph.** `U+1F50E` is coloured and not replaced. Giving it a language is a new
  contract seat (`Kit.SEARCH`) in eleven kits, which is a round's decision and not a stylesheet's.
- **A second channel for the three `reverse` kits.** The framework cannot spend a plate in that seat;
  choosing another channel for them would be the APP choosing what the KIT did not declare, which is
  what the *match tier by channel* ruling forbids in as many words.
- **The focus ring.** Two measured defects, both in `themes.tcss()`, both handed to
  `PROTOTYPE-inheritors-6.md` §4 with a roster and teeth rather than fixed inside an increment that
  was not briefed for them.
- **`HelpScreen`.** Four texts for eleven languages is a screen rewritten, not a rule added.

### 25.8 The artefacts

```
keys          NEW. 66 .txt + 66 .svg + 66 .png + 66 .json, identical across
              two PROCESSES.  inc93 moved 22 of them (K5 and K6 in all
              eleven); K1-K4 are byte-identical to inc91's in every picture.
              settle_reads is the one field outside the bargain.
legibility    1065 -> 1202 lines.  Section H rewritten: measured on the grey
              PNG over the seat `Kit.match` paints, three clauses, eleven rows
              where there were four.
census        TOTAL 23, homoglyph rows 22 -- BOTH UNCHANGED in all three
              increments.  A stylesheet is not a declaration the census counts.
raster        132 identical across two PROCESSES (66 colour + 66 grey), every
              time.
frames        ZERO component sheets moved in the whole batch, at either width.
gallery       ZERO board or component grids moved.
gallery 30-51 none changed byte-wise in inc91, inc92 or inc93, read off
              `prototypes/components/`: no sheet moved in `rework-10` at all.
round         `PROTOTYPE-inheritors-6.md`, 66 blocks, keep 33 / nota 12 /
              rehacer 21, and the page `ronda-teclas.html` (3.97 MB, 66 PNGs
              at 1:1, zero external URLs, zero console errors).
```

### 25.9 Batch status

| | |
| --- | --- |
| Phase A (spec) | **deviation** — the operator's delegated brief (this worktree's own instructions) was the spec; this section is the record |
| Phase B (implement) | **done** — inc91, inc92, inc93 |
| Phase C (close) | this section |
| Gates | `pytest -q` **1499 → 1535 → 1536 → 1560 passed**; `test_win_clipboard_roundtrip` is environment-coupled, **red in every run of this batch**, reported in every packet, counted in none, not touched. `keys.py` **44 of 66 → 66 of 66 laws**, 264 artefacts identical across two processes at every run. `verify_language.py` **ALL PASSED exit 0** — with one observed flake, §25.10. `render.py` 66 `.txt` + 66 `.svg` / 330 pairs / 0 hand-drawn, nothing changed on disk, every time. `raster.py` 132 PNGs identical across two processes. `legibility.py` byte-identical across two processes. `second_width.py` 0 rows cut, 330 pairs distinct. `matrix.py` refusals `[]`. `collision_census.py` TOTAL 23, homoglyph rows 22. `capture_languages.py` run at inc93: 22 grids identical across two processes, no two boards identical. `export_to_skill.py` at the close. The skill repo is not committed from here. |
| Notes | **Three increments, one agent, ≤ 5 source files each.** |

### 25.10 One flake, named

`verify_language.py` failed once, in one run, on a single clause — *"nord's BOARD is identical either
way"*, which compares two board captures — and passed in the runs before and after it with the same
tree. It is the ~10 % loud failure `capture_languages.settle`'s own docstring predicts for the columns
branch, and it is recorded here rather than smoothed over: **a gate that failed once is a gate that
can fail, and a batch that saw it and did not say so would be hiding a coin flip.**

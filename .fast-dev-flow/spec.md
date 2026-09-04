# Quick Spec — taskboard · batch "kits-learn" (L-31, L-32, L-34)

**Batch:** `2026-09-04-fastflow-08` · **Base ref:** `ea64fdf` (branch `kanban-variants`, tree clean at Phase A) ·
Predecessor `chrome-on-raster` (F-4) archived 2026-09-04 to `archive/spec-20260904-chrome-on-raster-closed.md`,
verbatim and with its §8 unfilled — the same way `surface` and `prev` were archived before it. Language: English.

**Input:** three findings written by the agent that made `tui-demos/lab-emersio` carry Corgi and Blueprint —
`tui-demos/.fast-dev-flow/LIMITS.md` **L-31**, **L-32**, **L-34**. Each ends in a "For the skill" paragraph, and
that paragraph is the requirement. This batch is the reference kit *learning from its first outside consumer*:
every item is a gap the lab found by trying to use the language and having to work around it.

---

## 1. Objective (1 line)

Close the three gaps the first non-board consumer of `language.py` hit — a posture that ignores the argument it is
given (L-31), a frame mechanism that names its first caller's domain (L-32), and a language with no answer for a
series (L-34) — so that emersio-lab's two workarounds become **deletable** and `LANGUAGES.md` §11 becomes **true**.

---

## 2. User stories

- As **any app that is not taskboard**, I want blueprint's title block to take my identity and my state as *data*,
  so that I do not have to invent a fake mode strip or rebuild the language's single most identifying mark.
- As **a consumer that renders a real figure**, I want the `tint` posture to say what the pixels *are* beside what
  they *measure*, so that I stop drawing a third dimension span the kit should have drawn.
- As **an app with a convergence curve**, I want blueprint to have a declared answer for a series, so that I either
  get the language's own trace or a refusal I can read — and not a chart axis in glyphs the language forbids.
- As **the operator**, I want nothing that already renders to move except where a decision moves it on purpose.

---

## 3. Acceptance criteria (observable)

- [ ] **AC-1 · L-31 · the posture reads the argument, and the argument is tested everywhere.**
  `_surface_tint` uses `label` when it is given: the sheet carries a **third span above its two**, stating what the
  pixels *are* (`├── 60 X 20 CELLS ──┤`) beside what they *measure* (`480px` / `160px`), built through the kit's own
  `dimension()` — one span mechanism, never a second. `image_box` moves down one row with it, so `chrome` still
  punches exactly the glass. With **no** label the render is byte-identical to `ea64fdf`.
  Plus the general rule, as a test: **`test_every_optional_argument_is_read_or_declared_refused`** — for every
  declared posture, `raster_region(img, w, h, label=X)` either differs from `raster_region(img, w, h)`, or the
  posture appears in a **declared, in-code refusal registry** with the commitment that refuses it. A posture in
  neither set fails. (An optional argument no implementation reads is a comment — and a *declared* refusal is an
  implementation reading it.)
- [ ] **AC-2 · L-32 · the frame takes content as data.** A new `Blueprint.stamp(rows, w, strip=None)` takes the
  block's content as **rows of `(caption, value, knocked)` cells** and its selection as an **optional extra**
  (`strip=(options, active)`, `None` for an app with no mode strip). `title_block(options, active, w)` survives as a
  **thin adapter** over it. Observable: the 22 board/gallery frames are **byte-identical** to the baseline, and a
  test renders a stamp from cells alone — no mode strip, two body rows — and asserts it draws the two rules, the
  knockout, and **no `REG` marks** (nothing to register when nothing is selected).
- [ ] **AC-3 · L-34 · the language has a declared answer for a series, and it is implemented.** Decision and
  reasoning in **§6.1**. Implemented as `Blueprint.series(...)`, drawn **only** from the ten permitted glyphs — a
  test asserts the rendered character set is a subset of blueprint's declared alphabet and that `│` and `└` are
  **absent**. The kit's class docstring stops saying the language has no answer, which is what makes §11's amended
  paragraph true.
- [ ] **AC-4 · nothing else moves.** The **44** named frames (22 board/gallery `.txt` + 11 `surface_*.txt` + 11
  `surface_*.svg`) are byte-identical to the baseline swept at `ea64fdf` **before any edit**
  (`.fast-dev-flow/baseline-kits/`, 66 files, taken 2026-09-04), **except** the frames named in §6.2 — each named
  there in advance, with the reason.
- [ ] **AC-5 · the mutation table stays green.** The 77-swap `test_mutation_changes_the_render` table and its chrome
  limb still pass, with `FRAME_TWINS` neither widened nor narrowed.
- [ ] **AC-6 · the workarounds are deletable, and it is proved by rendering.** In a **temp copy** of
  `tui-demos/lab-emersio` (`tui-demos` is READ-ONLY this batch), `_blueprint_titleblock` and `_cell_span` are
  deleted, replaced by calls to `stamp()` and by the label `raster_region()` now reads, and the lab's blueprint
  sheet still renders **the same sheet**: the same content in the same cells, the block docked bottom-right, two
  rules and exactly one knockout, no glyph outside blueprint's ten.
  **It will NOT be byte-identical, and that is the finding rather than a miss.** The lab's block padded its rules
  by 2 cells (`bw = max(plain) + 2`) and put 3 spaces where the kit's `GAP` is 2 — hand arithmetic the kit already
  owned, which is exactly what L-32 says a second implementation costs. The diff is reported cell-by-cell and every
  differing cell must be attributable to the lab adopting the kit's arithmetic; a difference in **content** or in
  **marks** fails this AC.
- [ ] **AC-7 · the export is staged, not shipped.** `export_to_skill.py` is run into a **staging directory**; the
  diff of the generated `assets/languages.py` and `assets/languages/SURFACES.md` against the live skill is reported.
  The real export stays the orchestrator's call.

---

## 4. Validation strategy

`python -m pytest -q` is the gate for AC-1/2/3/5 (baseline at `ea64fdf`: **285 passed, 2 skipped, 4 warnings**).
AC-4 is a byte comparison against `.fast-dev-flow/baseline-kits/`, refreshed by
`python prototypes\capture_languages.py` and `... --surface` run **plain** — F-1 makes the board sweep red about one
run in three (it took **3 runs** to get a green baseline here: `board_instrument.txt`, then `board_prism.txt`, then
green), and F-8 blocks `--surface` when its output is redirected inside a compound command, so both are run alone
and the count is recorded. AC-6 is a rendered diff from a temp copy of the lab. AC-7 is a directory diff. No test is
skipped silently; the two already-skipping tests are the numpy/`.npy` sweep-image pair and they are named.

---

## 5. Non-goals (what is OUT)

- **A series mechanism for every language.** §6.1's decision is blueprint's. A `Kit.series()` base — the eleven-way
  question of what each language does with a trace — is a batch of its own, and inventing it here would be the
  eleven-language redesign this batch is not.
- **Fixing F-1.** Still open, now with a fifth implicated frame (`board_instrument.txt`, new this batch). Recorded,
  re-run around, not investigated.
- **Any edit to `tui-demos`.** Read-only. AC-6's patch lives in a temp copy and is thrown away.
- **The real export to `~/.claude/skills/tui-design/`**, and the hand-written `LANGUAGES.md` §11 rewrite — both are
  the orchestrator's call. This batch produces the §11 replacement paragraph as *text in the increment*, staged, and
  says plainly that it did not write it into the skill.
- **The remaining LIMITS findings.** L-33 is explicitly "recorded rather than resolved" by its own author. L-35–L-37
  are `tui-demos`' capture harness, not this repo's kits.

---

## 6. Detected security flags

- [ ] Auth / identity · [ ] Secrets / config · [ ] External integrations · [ ] Sensitive data
- [ ] Destructive DB · [x] Input / attack surface · [ ] Network / exposure

**`security_required`:** `true` (one flag, narrow)

**Risk summary:** the only surface is **caller text interpolated into a markup row**. `_surface_tint` starts reading
a caller's `label`, and `stamp()` starts taking a caller's cell values — both land inside Textual markup, which is
this module's documented pitfall A1: escaping changes a string's *character* count and not its *cell* count, so a
mechanism that pads the escaped string hands back a rectangle one cell short. Rule: **width math before `mark()`,
always**, the way `Blueprint._pad` already does it. `test_a_label_cannot_inject_markup_or_steal_a_cell` already
parameterises over every declared posture and will now actually exercise `tint`; the stamp gets the same assertion.

### 6.1 · The L-34 decision — a **declared series mechanism**, not a renunciation

**Decision: blueprint gets a series, drawn as an ORDINATE DIMENSION STACK from a common datum.**

**Why not renunciation.** Ledger and Solari may renounce images because each has a *sentence* that forbids one:
ledger's "a figure is audited, not shown" follows from double-entry, solari's "one shape, the row; an image cannot
flip" follows from the machine it imitates. **Blueprint has no such sentence about a series, and its doctrine points
the other way**: *"the frame stops CONTAINING and starts MEASURING"*, *"the only language here where the chrome IS
the data-viz"*, *"Fits: anything spatial, anything with extents and tolerances."* A convergence curve is a sequence
of extents. Renouncing plots would renounce the language's own declared subject, and it would be the first
renunciation here adopted for lack of a glyph rather than out of a commitment. **A renunciation has to be a
consequence of something the language believes; this one would only be a consequence of the alphabet being short.**

**Why the impossibility in L-34 is real and narrower than it reads.** L-34 is exactly right that `│` and `└` are
unconstructable, and this batch does not smuggle them in. But what is unconstructable is a **conventional axis**,
and *a series is not an axis*. A drawing office does not plot with an axis box; it draws a **schedule of ordinate
dimensions from a common datum** — every sample a run from the same left terminator, its length the value, the
figure standing on the run. Stack those rows and **the locus of the closing terminators IS the trace**: the curve is
drawn in `┤`, the datum in `├`, the run in `─`, the off-scale flag in `╌`. The vertical the plot appears to need is
never drawn — it is the column the terminators happen to fall in, which is precisely what an ordinate dimension
looks like on paper. **Nothing is admitted to the ten glyphs, and nothing is boxed.**

**What it fixes that `dimension()` could not.** `dimension()` measures one quantity against a *declared* ceiling,
because DATAVIZ law 2 forbids normalising a row to itself and a kit method is handed one row at a time. A series is
the one case where the siblings ARE in hand — so `series()` may derive its ceiling, and therefore **must state it**,
which on this sheet is a dimension. The scale becomes a mark on the drawing instead of an assumption, which is the
same law arriving at the opposite mechanism because the input changed.

**Cost of being wrong:** if the stack does not read as a trace at real width, the fallback is the renunciation, and
it costs one method and one paragraph. That is cheap enough that implementing is the better way to find out.

### 6.2 · Frames that move on purpose (named in advance)

| frame | why | which AC |
| --- | --- | --- |
| `surface_blueprint.txt` | the tint sheet gains its third span, because the sweep passes `label="mbb rho final"` | AC-1 |
| `surface_blueprint.svg` | same render, other transport | AC-1 |

**Two frames, and they move for L-31 rather than for L-34.** This is a **correction to the acceptance as briefed**,
which permitted only "the frames your L-34 decision moves". L-34 moves **none**: no board or surface sheet draws a
series, so `series()` adds a mechanism and changes no existing rendering. L-31 moves two, and it cannot not: the
sweep hands `tint` a label, so a `tint` that reads its label renders differently *by definition* — that is the whole
content of the finding. The other **42** frames stay byte-identical.

---

## 7. Batch status

| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-09-04 |
| Closed | 2026-09-04 |
| Promoted to /dev-flow | no |
| Notes | **≤ 4 source files per increment, one agent, sequential.** Inc 1: L-32, `stamp()` + adapter + its test. Inc 2: L-31, `_surface_tint` reads `label` + the refusal registry + the optional-argument test + the two recaptures. Inc 3: L-34, `Blueprint.series()` + its glyph-alphabet test + the docstring that stops being false + the §11 replacement text. Inc 4: AC-6 (temp-copy lab proof) and AC-7 (staged export + diff). |

---

## 8. Close (filled in phase C)

### What changed

The reference kit learned three things from its first outside consumer. Blueprint's title block
became **`stamp(rows, w, strip=None)`** — content as rows of cells, selection as an optional extra
— with `title_block()` surviving as a three-line adapter. The **`tint` posture reads its `label`**
and letters it onto a third dimension span, so the sheet states what the pixels ARE above what they
MEASURE, and every posture's treatment of that argument is now either a render or a **declared
refusal** in `LABEL_REFUSED`. And blueprint gained **`series()`** — a declared answer to L-34,
implemented as an ordinate dimension stack whose closing terminators are the trace, chosen over a
renunciation because a renunciation must follow from a commitment and this one would only have
followed from a short alphabet.

### How it was tested

- `python -m pytest -q` — **315 passed, 2 skipped, 4 warnings** (baseline at `ea64fdf`: 285 passed).
  30 new tests: 18 in `tests/test_frame.py`, 12 in `tests/test_surface.py`.
- Both capture sweeps re-run plain and alone after every increment; 66 frames byte-compared against
  a baseline swept **before any edit** into `.fast-dev-flow/baseline-kits/`.
- The unlabelled render was compared against `taskboard/language.py` **as it stands at `ea64fdf`**,
  loaded side by side — not inferred.
- AC-6 rendered from a throwaway copy of `lab-emersio` in `%TEMP%`; `tui-demos` never written to.

### Evidence per AC

| AC | verdict | evidence |
| --- | --- | --- |
| AC-1 · L-31 | **met** | `inc8.md` §1, §4 — the third span renders; `LABEL_REFUSED` + `LABEL_REFUSED_BY_LANGUAGE`; `test_every_optional_argument_is_read_or_declared_refused` (×11) and `test_the_declared_refusals_name_postures_that_exist`; no-label render identical to `ea64fdf` for all 11 languages |
| AC-2 · L-32 | **met** | `inc7.md` §1, §4 — `Blueprint.stamp()`; `tests/test_frame.py` 9 tests incl. the no-strip stamp and the no-registration-marks assertion; 44/44 board frames byte-identical |
| AC-3 · L-34 | **met** | `inc9.md` §1–§4 and spec §6.1 — `Blueprint.series()`; `test_a_series_smuggles_in_no_vertical_stroke`, `test_the_trace_is_the_locus_of_the_closing_terminators` + 7 more; the kit docstring ships the commitment |
| AC-4 · nothing else moves | **met** | `inc10.md` §5 — `64 / 66` identical; MOVED = `surface_blueprint.txt`, `surface_blueprint.svg`, both named in §6.2 in advance |
| AC-5 · mutation table | **met** | in the 315; `FRAME_TWINS` untouched, the 77-swap table and its chrome limb green every run |
| AC-6 · deletable | **met** | `inc10.md` §1 — identical token multiset, 1 knockout, `─` only, nothing outside the ten; the only deltas are the 3 cells of the lab's own arithmetic, as the corrected AC required |
| AC-7 · staged export | **met** | `inc10.md` §2 — 5 files differ from the live skill, each attributed by three-way comparison; the real export not run |

### Open risks / pending

- **The real export** and the **`LANGUAGES.md` §11 rewrite** are the orchestrator's call. §11's
  replacement text is staged at `.fast-dev-flow/staging/LANGUAGES-11-replacement.md`.
- `gallery_darkside.*` is stale in the live skill from a previously blocked export — **not** this
  batch; proved byte-identical to the pre-edit baseline.
- **F-12** (new): `surfaces_index()` promises its table describes the frame it names and nothing
  checks it. Caught here in staging; not fixed.
- **F-9**, **F-10**, **F-11** — recorded in `inc7.md`, `inc8.md`, `inc9.md`.
- **F-1** still open, now with five implicated frames (`board_instrument.txt` added today);
  3 red in 8 sweep runs this batch. **F-8** unchanged; no terminal process was ever killed.
- A stated limit of the series: below the width its own figure needs a sample draws bare, so a
  converging trace loses its tail figures. The published scale row is the mitigation.

### Security flags — handling

One flag fired (input / attack surface), and it was the only one: caller text interpolated into
markup rows, on two new surfaces. Both do width math on the plain string and `mark()` on the way
out. `test_a_label_cannot_inject_markup_or_steal_a_cell` now genuinely exercises `tint`, and
`test_a_stamp_cell_cannot_inject_markup_or_steal_a_cell` covers the stamp with two payloads —
including `[URGENT]`, the case `mark()`'s docstring records as the one `rich.markup.escape` gets
wrong. No secrets, no external calls, no destructive commands, no new dependency.

### Suggested commit message

```
kits-learn(L-31,L-32,L-34): the kit learns from its first outside consumer

stamp(rows, w, strip=None) takes the title block's content as data and its
selection as an optional extra; title_block() is a three-line adapter over it,
so the board's 44 frames are byte-identical.

_surface_tint reads the label it is given and letters it onto a third dimension
span -- what the pixels ARE above what they MEASURE. Every posture that does
NOT read it now says so in LABEL_REFUSED, and a test checks the declaration in
both directions.

Blueprint gets series(): an ordinate dimension stack whose closing terminators
are the trace. A renunciation must follow from a commitment, and this one would
only have followed from a short alphabet -- so the language draws a series the
way a drawing office does, in its own ten glyphs, with no vertical smuggled in.

Moved on purpose: surface_blueprint.txt/.svg (the caption span). 64/66 frames
byte-identical against a baseline swept before any edit.
```

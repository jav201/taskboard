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
- **`Kit.button`'s walls for swiss.** Found by looking at `swiss_S4` and recorded in §8, not fixed.
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
- **Swiss still takes `Kit.button`'s walls** (`│   Cancel   │`, visible in `swiss_S4`) — a border-shaped
  mechanism in the language whose commitment is "no boxes, at any width". `button` was not among the
  seven mechanisms inc32 scoped, nor among this batch's two, so it is **recorded as the next inheritance
  debt** rather than smuggled in. It is exactly the class of thing that only a frame reveals, which is
  the argument for inc37.

### Gallery candidates — PROPOSED, not installed

Eight of the 36 new frames, all `compositor` provenance, all zero hand-drawn, all 100×32. Numbering
continues the gallery's own (`30 · ledger-settings-danger`, `31 · corgi-settings-legend` are the last
two). Each gets a draft `Limit` line in the gallery's shape; the two commitment bullets are for whoever
installs them.

| # | frame | ink | why it earns a seat | draft `Limit:` |
| --- | --- | --- | --- | --- |
| a | `instrument_S1` | 36.0 % | the graticule is the whole structure device in one screen — across the field rows (`⠒`), down the pane gutter (`⠸`) and under the bars (`⣿`) | the densest frame in the sweep, and the `.txt` cannot show that the graticule is DIM and the figures are not; read the SVG for the tier, or the frame reads as one weight |
| b | `industrial_S1` | 24.0 % | one plate convention across three seats in a single view — `▐up▌` keys, `▐ 12/09/26 ▌` figures, and the `▌ ▐` gutter that closes one pane and opens the next | the gutter spends two of three cells, so at any narrower seat the two plates touch; legal by the closure law and untested against a small terminal |
| c | `swiss_S1` | 16.4 % | the counter-frame to (b): the same screen where the divider is NOTHING, and the right pane starts at the next column | `Kit.button`'s walls (`│   Cancel   │`) are inherited and are boxes in the language that has none — a real inheritance debt, visible in this frame's sibling `swiss_S4` and unfixed |
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

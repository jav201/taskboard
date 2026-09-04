# Increment 8 — L-31: the posture that captions hardest can be told what it is captioning

Batch `2026-09-04-fastflow-08` ("kits-learn") · increment 2 of 4 · base ref `ea64fdf`.
Scope: *`_surface_tint` reads the `label` it is given; the general rule becomes
a test; the two frames named in spec §6.2 move and nothing else does.*
No git operations. `spec.md` untouched this increment.

## 1. What changed

**`_surface_tint` letters the label onto a third span, above its two.** The two
existing spans are built from `img.size` — `480px` and `160px`, an image's
pixel extent, which is a fact about the ENCODER. A drawing's dimension is a
fact about the THING DRAWN, and on this sheet they are different numbers in
different units. So a given label becomes `├─ 60 X 20 CELLS ─┤` over `480px`
over the glass over `160px`: **what the pixels ARE, above what they MEASURE.**

    bare  ├──────── 64px ────────┤      told  ├─── 60 X 20 CELLS ────┤
          ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀            ├──────── 64px ────────┤
          ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀            ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    image_box (0, 1, 24, 6)                   image_box (0, 2, 24, 5)

**The caption is PAID FOR out of the rectangle, not added to it.** The region
is reserved (CEILINGS §7), so the glass moves down one row and loses one — and
`image_box` moves with it, which is what keeps `chrome` punching exactly the
glass and no more. Three decisions worth naming:

- built through `_span_text` and **not** through `k.dimension()`. A mechanism
  is dispatched on a token and can be reached by a kit with no `dimension()`
  method; `dimension()` is a two-line delegation to that same function, so the
  mark is the language's either way and there is still only ever one;
- lettered in **caps** — this sheet's figures are `03D`, `HELD`, `DONE`, and a
  lowercase callout would be the one piece of typing on the drawing that was
  not drafted;
- `mark()` **after** the width math, never before (pitfall A1).

**The general rule became two tests and a declared table.** L-31's portable
form is *an optional argument that no implementation reads is not an argument,
it is a comment*. Taken literally — "every optional argument of every posture
changes the render when set" — **five postures fail it on purpose**: untinted
draws no frame, lattice's unlit dots are the picture, display's legend belongs
to the machine, frame renounces captions by name, depth draws no chrome at all.
The honest form is that the argument must **reach the render OR the refusal
must be declared**, so `LABEL_REFUSED` names each of the five with the
commitment it follows from, and `test_every_optional_argument_is_read_or_declared_refused`
checks the declaration **in both directions**: a posture in the table whose
render moves fails too, because that means the table is stale.

**One refusal is a language's and not a posture's, and it needed its own
table.** `refuse` *does* read the label — ledger letters it on the exhibit's
caption — but solari's `exhibit()` shows nothing, so the label dies inside a
posture that generally honours it. Filing that under `"refuse"` would have
reported ledger's behaviour as solari's, so it is keyed by language
(`LABEL_REFUSED_BY_LANGUAGE`).

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/language.py` | source | `_surface_tint` reads `label`; `LABEL_REFUSED`; `LABEL_REFUSED_BY_LANGUAGE` |
| `tests/test_surface.py` | source | `test_every_optional_argument_is_read_or_declared_refused` (×11), `test_the_declared_refusals_name_postures_that_exist` |
| `prototypes/gallery/surface_blueprint.txt` | artefact | recaptured |
| `prototypes/gallery/surface_blueprint.svg` | artefact | recaptured |

**2 of 4 source files used.** No new dependency.

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    $env:PYTHONIOENCODING = "utf-8"
    python -m pytest -q
    python prototypes\capture_languages.py --surface

## 4. Test results

**Suite:** `306 passed, 2 skipped, 4 warnings in 27.74s` (was 294 after
increment 7; +12 is exactly the new parametrised test and its table check).
The 77-swap mutation table and its chrome limb are green, `FRAME_TWINS`
untouched.

**The test caught the stale artefact before the sweep did**, which is the
check working:

    AssertionError: blueprint: the shipped capture is not what raster_region renders
    At index 0 diff: '├──── 360px ────┤' != '├──── MBB RHO FINAL ────┤'

**AC-1's "with no label, nothing moves" — proved against the base ref
directly**, not by inference. `taskboard/language.py` at `ea64fdf` was loaded
beside the working copy and both were asked to render every language with no
label:

    no-label render vs ea64fdf: naught True · corgi True · instrument True ·
    swiss True · industrial True · nord True · darkside True · prism True ·
    ledger True · solari True · blueprint True     -> ALL IDENTICAL

(`blob()` covers rows AND pixels, so this is both surfaces.)

**AC-4 — the frames, against the pre-edit baseline:**

| group | identical |
| --- | --- |
| 22 board/gallery `.txt` + 22 `.svg` | 44 / 44 |
| 9 other languages' `surface_*` `.txt`/`.svg` | 20 / 20 |
| **`surface_blueprint.txt` / `.svg`** | **MOVED — declared in §6.2** |
| every other file the sweeps write | 64 / 64 |

The moved rows, in full — one row gained, one row of glass lost:

    row 2  - ├──────── 360px ────────┤
           + ├──── MBB RHO FINAL ────┤
    row 3  - ▀▀▀▀▀▀▀▀▀▀ (glass)
           + ├──────── 360px ────────┤

**F-1's count:** the `--surface` sweep is not subject to F-1 (it has no
determinism arm) and went green first time, run plain and alone per F-8. No
board sweep was needed this increment — the board draws no raster region, and
the 44 board/gallery frames above are from increment 7's post-edit sweep.

## 5. Findings

**F-10 · NEW · the literal form of L-31's rule is unimplementable, and the
gap is where the value is.** "Every optional argument changes the render when
set" fails for five of eight postures *correctly*. The rule that survives
contact is **read it or declare the refusal** — and the declaration has to be
data, because a refusal written in a docstring is exactly as invisible to a
test as the bug it is distinguishing itself from. **Portable: the useful form
of "no dead arguments" is "no UNDECLARED dead arguments"; the table is the
deliverable, not the assertion.**

**A correction to L-31.** The finding says `_surface_tint` "builds both of its
dimension spans from `img.size` alone" — correct — and describes the lab's
workaround as "a third span, `├─ 60 x 20 CELLS ─┤`, immediately above the kit's
two". That is exactly what the kit now draws, so the workaround was the right
shape. What the finding does not say is that the third span **costs a row of
glass**: the rectangle is reserved, so the lab's own sheet was one raster row
shorter than it looks, and any consumer adding the span by hand paid that
silently. Stating it in the kit makes the cost visible in `image_box`.

**Nothing in L-31 turned out wrong.** Its diagnosis, its example and its
proposed fix all held.

## 6. Pending

- AC-3 (L-34), AC-6 (the lab proof), AC-7 (the staged export).
- F-1, F-8 unchanged.

## 7. Suggested next task

Increment 3 — L-34: `Blueprint.series()`, the ordinate dimension stack decided
in spec §6.1, its glyph-alphabet test, the class docstring that stops being
false, and the §11 replacement paragraph as stageable text.

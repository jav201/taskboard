# Increment 1 — the primitive, the registry, and three postures

Batch `2026-09-03-fastflow-06` ("surface") · phase B · one agent, sequential.
Scope from spec §7: *base primitive + registry + `lattice`/`display`/`tint`
(Naught, Corgi, Blueprint) + the AC-1 mutation test.*

## 1. What changed

**A `surface` token, read by exactly one dispatcher.** `Kit.raster_region(img,
w, h) -> RenderResult` resolves its mechanism through `SURFACES[t["surface"]]`,
the same lenient `.get(token, default)` shape `Kit.meter` uses for `METERS`.
`Kit.posture` is the token's only reader.

**`RenderResult` carries BOTH surfaces (AC-3).** `rows` (glyph side, any
terminal), `pixels` (the same posture applied to the actual pixels, for
`textual_image`), `reserved` (the opaque cell rectangle the layout must give
it — CEILINGS §7), and `blob()`, which is what the mutation check compares.
`blob()` covers the pixels on purpose: a posture that restyled the cells and
handed `textual_image` the untouched source would pass a glyph-only diff while
breaking AC-3.

**Four mechanisms, plus two that refuse by name.** `untinted` (base default —
nord's posture, and literally "no frame"), `lattice` (naught, instrument),
`display` (corgi, industrial), `tint` (blueprint). `phosphor` and `bbs` are
registry entries that raise `NotImplementedError` naming themselves and saying
CATALOGUE-ONLY (AC-7) rather than being aliased to a posture that looks similar.

**Per-language differences live on the kit, not in the mechanism.**
`lattice_grid` / `lattice_rows` / `display_chrome` / `display_label` /
`tint_pair` / `exhibit` are hooks; a mechanism never branches on a kit's name.
Corgi overrides `display_chrome` to its aluminium box on the same green-black
glass its `surface()` already puts under the hero and the meter.

**`taskboard/raster.py` is new** and holds only arithmetic: NEAREST resample,
the half-block glyph pass with run coalescing (LIMITS L-1), an ordered 4x4
Bayer dither, `duotone`, `quantise`, `step`, and the transport report. PIL
only — `pyproject.toml` does not declare numpy and the shipped package stays on
its declared dependencies.

**Naming, stated because it is a trap.** `Kit.surface()` already existed and is
a *different* axis (TCSS ground). The new token is also called `surface`
(LANGUAGES.md names the axis). They do not collide technically (dict key vs
method), and the token is read through `Kit.posture` so no call site has to
guess. Documented in `themes.py`'s key list.

## 2. Files modified

| file | source? | what |
| --- | --- | --- |
| `taskboard/raster.py` | **new source** | the pixel side: resample, half-block, dither, duotone, quantise, transport report |
| `taskboard/language.py` | source | `RenderResult`, `Kit.raster_region` + six hooks, `SURFACES`, `LIVE_SURFACES`, four mechanisms, `Corgi.display_chrome` |
| `taskboard/themes.py` | source | `surface` token on six languages + the key's documentation |
| `tests/test_surface.py` | **new test** | 30 tests (outside the file cap per the batch brief) |

**3 of 4 source files used.** No new dependency.

## 3. How to test

    cd C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants
    python -m pytest -q                        # whole suite
    python -m pytest tests/test_surface.py -q  # this increment
    $env:PYTHONIOENCODING = "utf-8"
    python prototypes\capture_languages.py     # AC-6: existing captures unmoved

AC-6 was checked against a **control sweep that pops the `surface` token from
every theme before any kit is built** (a throwaway script under the temp dir
that edits no repo file), so the comparison is against a render that literally
cannot read the new token.

## 4. Test results

    194 passed, 3 warnings in 28.83s          (164 before this increment, +30)
    tests/test_surface.py: 30 passed in 0.20s

The 3 warnings are Pillow 12's `getdata()` deprecation, in the tests only.

**AC-1 mutation table** — every declared language, every swap, 24x8 region,
synthetic gradient probe:

| language | token | swapped to | bytes differ |
| --- | --- | --- | --- |
| naught | lattice | untinted / display / tint | YES / YES / YES |
| corgi | display | untinted / lattice / tint | YES / YES / YES |
| instrument | lattice | untinted / display / tint | YES / YES / YES |
| industrial | display | untinted / lattice / tint | YES / YES / YES |
| nord | untinted | lattice / display / tint | YES / YES / YES |
| blueprint | tint | untinted / lattice / display | YES / YES / YES |

18 swaps, 18 differ, and every restore came back byte-identical. **No dead
metadata in this increment.**

**AC-6 byte identity** — 22 captures, four control sweeps:

| control run | identical | differed |
| --- | --- | --- |
| out1 | **22 / 22** | — |
| out (first) | 21 / 22 | `board_solari.txt` |
| out2, out3 | 21 / 22 | `gallery_blueprint.txt` |

Both deviations are **pre-existing capture non-determinism, not renders that
changed** — see Risks. One control run matched all 22 bytes for bytes.

## 5. Risks and findings

**F-1 · `capture_languages.py` is intermittently non-deterministic, in two
places, and its header says one of them is cured.** The header records solari
flipping on the `DAYS OVERDUE` row and claims `TEXTUAL_ANIMATIONS=none` fixed
it. It has not: `board_solari.txt` still flips that exact row, and
`gallery_blueprint.txt` flips a switch segment between `▅▅` and `▁▁` (an
animation caught mid-transition). Both were observed on sweeps that had the new
token **popped**, so neither is caused by this batch. Cause is `settle()`'s
three-identical-frames condition passing on a stalled animation frame —
condition A of the real harness (every mounted widget has painted inside its
clipped area) is deliberately not reimplemented there, and this is what that
costs. The sweep's own reproducibility check turns this into an intermittent
red exit, which will make AC-4 and AC-6 flaky in increment 3.

**F-2 · The shipped skill captures were already stale before this batch
started.** All ten `board_*.txt` in the skill's `assets/languages/` differ from
a fresh sweep of unmodified code — dates and counts, e.g. swiss `7d!` -> `1d!`.
Cause: `prototypes/out/_fixture_late.json` was edited 2026-08-03 10:38, after
the 08:47 sweep that produced them. The AC-6 baseline used here is therefore
the **fresh pre-change sweep**, as the batch brief directs, not the shipped
assets.

**F-3 · `prism` exists in the code and in neither asset.** `THEMES`/`ORDER`
carry eleven languages; `assets/languages.py` `ORDER` and `assets/languages/`
carry ten. Running `export_to_skill.py` will add prism to the skill — a change
this batch did not ask for. Flagged now; decision needed before increment 3.

**R-1 · `Instrument` currently renders naught's dot alphabet.** It shares
`lattice` (AC-2 says it should) but has no `lattice_rows` override yet, so it
draws `∙`/`◦` instead of braille. Its `base` token is `braille` and
LANGUAGES.md says "the dot grid is the identity" — borrowing naught's
vocabulary is a fidelity defect. Fixed in increment 2.

**R-2 · `Industrial` renders with the base display chrome.** It declares
`display` and works, but AC-2 wants "their own frames". Increment 2.

**R-3 · The lenient dispatch can hide a typo.** `SURFACES.get(token, untinted)`
renders an unknown posture plausibly and forever. Guarded by
`test_every_declared_token_has_a_mechanism`, which checks the declared set
against the registry rather than trusting the default.

**Bug found and fixed inside this increment:** the first `duotone` built a
256-entry palette and called `luma(img).convert("P")` to index it.
`convert("L" -> "P")` *re-quantises*; it does not index. The `putpalette()`
then decorated a mapping already thrown away and the output came back
near-greyscale — it read correct and rendered the source. Caught by the
display/tint property tests, not by the mutation test (which it passed).
Replaced with `ImageOps.colorize`, and the failure is recorded in the
function's docstring.

## 6. Pending

- Increment 2: `refuse` (ledger's ruled exhibit, solari's nothing), `frame`,
  `depth` (darkside, prism), `figure` (swiss); `Instrument.lattice_rows`
  (R-1); `Industrial.display_chrome` (R-2); tokens for the remaining five.
- Increment 3: the `--surface` sweep, AC-5 WT/Sixel captures, export,
  INDEX.md, AC-6 re-check. **F-3 needs a decision first.**
- Not done and not in scope: no existing screen renders a region (spec §5).

## 7. Suggested next task

Increment 2 as specified — the remaining five mechanisms and the two fidelity
overrides, one source file (`language.py`) plus `themes.py`, tests extended.

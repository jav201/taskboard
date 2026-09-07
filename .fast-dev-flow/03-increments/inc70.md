# Increment 70 — `mut` is body text

**Batch:** `rework-6b`, increment 4 of 4 · the **`mut` contrast** ruling.
**Files:** `taskboard/themes.py`, `tests/test_components.py` — **2 source files**, plus 24 regenerated
component `.svg` (0 `.txt`) and 8 regenerated gallery `.svg`.

**Most of the body text in these sheets is `mut`, not `ink`, and five kits had it under WCAG 1.4.3's
floor.** inc63 taught the exporter to read the kit's DECLARED ground (ruling E4) and asserted
`contrast(ink, ground) >= 4.5`; writing that law is what turned up the next one, and §16.7 wrote down
both the measurement and the refusal to act on it: *"moving a `mut` is a design change in five kits at
once."* **Four of the five moved.** The fifth is solari, and it does not move because it **cannot** —
its selection band is a second ground and the two floors provably do not overlap. Suite **1225 → 1248**.
**0 `.txt` changed in the whole corpus.**

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

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

This increment carries out the **`mut`** ruling.

---

## 1. What moved, and every move is the smallest one

| kit | `mut` before | :1 | `mut` after | :1 | one step less | `ink` :1 | `dim` :1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nord | `#7b88a1` | **3.50** | `#919cb0` | **4.51** | `#909baf` → 4.46 | 10.84 | 1.69 |
| solari | `#6e6a60` | **3.65** | *not moved* | **3.65** | — see §3 | 16.81 | 1.20 |
| instrument | `#6b7785` | **4.26** | `#6e7b89` | **4.50** | `#6d7a88` → 4.44 | 16.52 | 1.74 |
| darkside | `#737373` | **4.43** | `#757575` | **4.56** | `#747474` → 4.49 | 19.26 | 1.39 |
| ledger | `#6b6558` | **4.45** | `#6a6458` | **4.51** | `#6b6458` → 4.50 | 13.36 | 1.50 |

**"Smallest" is arithmetic, not taste.** Each colour was converted to HLS, its **hue and saturation held
exactly**, and its lightness stepped one increment at a time until the ratio reached 4.5 — so the hue
family is preserved *by construction* rather than by eye, and the "one step less" column is the proof
that nothing smaller clears the floor.

**Ledger moves the other way**, by a single unit, because it is the one light-paper kit in the set: its
body grey gets **darker**. That is the same asymmetry `ledger_S6` made visible when E4 was fixed.

**`instrument.unit` moved with `mut`.** The two were byte-identical (`#6b7785`) and the coupling is
deliberate — the axis-label grey **is** the body grey in this kit — so leaving one behind would have split
one colour into two almost-identical greys, and `unit` is text as well (*"readings and axis unit
labels"*).

---

## 2. The law, over all eleven

```
ink >= 4.5:1   ·   mut >= 4.5:1   ·   ink > mut > dim
```

against the ground the kit **declares** — which is a sentence that only became measurable in inc63, when
the exporter stopped inferring a ground from pixel frequency. `contrast()` is the same WCAG
relative-luminance function inc63's canvas law uses, on the same two hexes, so the two laws cannot
disagree about what a ratio is.

**The order clause is not decoration.** A kit could clear 4.5 by lightening `mut` past `ink` — satisfying
the floor and destroying the hierarchy the three tokens exist to carry. It is strict (`>`), so a tie
fails, and it is asked of **all eleven including the exempt one**: a floor may be unreachable, an order
never is.

---

## 3. Solari does not move, and the exemption is a proof

**A gate caught the first attempt.** `verify_language.py` went red:

```
[FAIL] solari: every glyph on the SELECTED row clears 2.5:1 against its own ground
       (the defect that moved severity onto the cell face)  worst 2.10:1 — 'B' #7d796d on #f5a300
```

**Solari paints a second ground.** The selected departure inverts to amber (`#f5a300`), and that check
exists because an earlier draft of this kit printed `#f5a300` on `#f5a300` — 1:1, invisible — and its calm
fields came out at 1.8:1. `Solari._tones`'s own docstring is the commitment: *"with severity on the face,
every glyph on a schedule row is neutral (ink · mut · dim), so inverting the row's ground can never hide
a word."* Lightening `mut` to `#7d796d` took it to **2.10:1** against the band.

**No grey can do both, and the arithmetic says so rather than the eye:**

```
4.5:1 against #0b0b0c  ->  L(mut) >= 4.5 * (0.00338 + 0.05) - 0.05  ->  L(mut) >= 0.19021
2.5:1 against #f5a300  ->  L(mut) <= (0.44900 + 0.05) / 2.5 - 0.05  ->  L(mut) <= 0.14960
```

and a `mut` **lighter** than the amber would need `L >= 1.1475`, off the top of the scale. **The two
floors do not overlap.**

**What satisfying the ruling here would actually take is a per-row ink for the banded row**, and
`_sched_row` cannot see that a row is selected: the band is painted by the app's own CSS and the row is
composed with a foreground only, so `stat`, `proj` and `pri` sit on whatever ground is behind them —
while `due`, which carries its own face through `Kit.cell`, is immune. **That is a design decision about
solari's selection mechanism and no ruling has taken it.** It is `THE_BAND_IS_A_SECOND_GROUND`, one
language, by name, with the proof and with a stale-exemption check: the law asserts solari is *really*
under the floor, so the day it is fixed the exemption goes red rather than sitting there.

**This is the one item of the batch that is blocked on a decision rather than on work.**

---

## 4. `dim` is measured, not floored — and the brief's third clause is why

The brief that carried the ruling proposed `dim >= 3.0:1` (WCAG 1.4.11, the non-text floor).
**Measured first, as this batch measures everything: TEN OF THE ELEVEN are under it**, most far under.

```
naught 1.35 · darkside 1.39 · ledger 1.50 · nord 1.69 · corgi 1.71 · instrument 1.74
swiss 1.75 · industrial 1.96 · solari 1.20 · blueprint 1.24 · prism 3.25  (the only one over)
```

**`dim` is not text and it is not a component boundary either.** It is naught's unlit lattice
(LANGUAGES.md §0, quoted at `THE_GROUND_IS_NOT_A_MARK`: *"the unlit grid is visible … that faint lattice
IS the signature"*), solari's seam (*"the ONLY divider"*, one step off the flap face by construction),
blueprint's paper grid, ledger's dot leaders — the token every language spends its **ground** on. Raising
it to 3.0 in ten kits is a design change an order of magnitude larger than this increment's, and no ruling
has asked for one.

**So the clause is a ROSTER and not a floor**: `DIM_AGAINST_GROUND`, eleven numbers to two decimals,
asserted so they cannot move without somebody editing them — and the ladder clause (`mut > dim`, strict,
all eleven) does the work the floor would have done badly. **Measured, named, left**, exactly as §16.7
left `mut`.

---

## 5. Teeth

`test_the_tone_ladder_law_goes_red_on_the_five_declarations_inc70_moved`:

* **Four arms on the REAL hexes** — nord `#7b88a1`, instrument `#6b7785`, darkside `#737373`, ledger
  `#6b6558`, restored one at a time. Each arm asserts **the ratio it shipped at** (3.50, 4.26, 4.43,
  4.45) before asserting the law goes red, and checks the other ten stay green — so an arm cannot pass
  by breaking something else.
* **The order arm**, which is the half a floor cannot catch: nord's `mut` set to its own `ink`. It
  **clears 4.5** and the law still goes red, because the ladder inverted.
* **The exemption arm, both ways**: it names exactly one kit; emptied, solari goes red and the other ten
  do not.

`test_dim_against_its_ground_is_measured_and_recorded` is its own teeth — an eleven-row table of
two-decimal ratios that only moves when a token does.

---

## 6. Frames changed

**Exactly what the brief predicted: `.svg` only, `.txt` identical everywhere.**

```
24 component .svg   darkside S1-S6 · instrument S1-S6 · ledger S1-S6 · nord S1-S6
 0 component .txt   in the whole corpus
 8 gallery .svg     board_ + gallery_ for the same four
 0 gallery .txt
```

A tone change cannot move a cell, and the render confirms it rather than the packet claiming it: 66
frames re-rendered, 24 files different, none of them a `.txt`. **Solari's six did not move**, which is
the visible consequence of §3.

**Skill gallery 30–51: NONE changed byte-wise in `.txt`.** Seven of the twenty-two have a source among
the four languages (30 `ledger_S3`, 36 `ledger_S6`, 38 `ledger_S1`, 40 `ledger_S2`, 44 `instrument_S1`,
49 `darkside_S4`, 51 `instrument_S5`) and every one of them is a `.svg`-only change.

---

## 7. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1248 passed, 2 skipped, 4 warnings in 34.37s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

inc69 closed at `1 failed, 1225 passed`. **+23.** `test_win_clipboard_roundtrip` drives the real Windows
clipboard through PowerShell; **environment-coupled, reported, not counted, not touched.**

```
$ python -X utf8 prototypes/verify_language.py
ALL PASSED                                          (exit 0)
   -- and it was RED on the first attempt, on solari's selection band. See §3.

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> …/prototypes/components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)

$ python -X utf8 prototypes/components/matrix.py          (exit 0)
  --- refusals, by language ---   all eleven []

$ python -X utf8 prototypes/collision_census.py
self-check  1 of the 5 collisions the round found by hand still come back out of the census; 4 are asserted CLOSED and cannot grow back
self-check  the homoglyph roster is exact for all eleven (30 rows, 8 languages)
TOTAL                       35
TOTAL homoglyph rows            30

$ python -X utf8 prototypes/capture_languages.py plain
  22 grids identical across two PROCESSES
  no two boards identical
```

The census is untouched by a tone change **by construction** — it reads glyph tables, not colours — and
it is run anyway, because a batch that only runs the gates it expects to move is a batch with no control
arm.

---

## 8. Risks

1. **Four kits' body grey is lighter, and three of them are near-monochrome languages whose hierarchy is
   built on the ink/mut/dim spread.** The order clause holds (`ink > mut > dim`, strict), but the SPREAD
   narrowed: darkside's `mut` moved 4.43 → 4.56 against a `#000000` ground while `dim` stayed at 1.39, so
   the gap `mut`↔`dim` widened and `ink`↔`mut` narrowed. Nothing measures "the ladder is evenly spaced"
   and nothing here claims it is.
2. **`nord`'s move is the largest (3.50 → 4.51) and nord's palette is Nord's.** `#919cb0` is not a Nord
   palette entry; it is `#7b88a1` at the same hue and saturation, lifted. A kit whose whole
   commitment is *"inherits the terminal's world"* now carries one colour that is not in that world, and
   the alternative was body text at 3.50:1.
3. **The exemption is a request for a decision, not a fix.** solari ships at 3.65:1 and the packet is
   explicit that this increment did not carry out the ruling for that kit. If the answer is "the band
   gets its own ink", it is a `Solari` change, not a `themes.py` one.
4. **`DIM_AGAINST_GROUND` is eleven hard numbers at two decimals.** It will go red on any tone change to
   `dim` or `ground` — which is the point — but it makes any future ground change a two-file edit.

---

## 9. Found by looking, not fixed

* **A law's own writing found the next law, twice in two batches.** inc63 wrote `contrast(ink, ground)`
  and measured `mut` while it was there; inc70 wrote `contrast(mut, ground)` and measured `dim` while it
  was there. Both times the measurement was published and not acted on, and both times the next ruling
  came from the published number. **That is the pattern worth keeping**, and `DIM_AGAINST_GROUND` is this
  increment's contribution to it.
* **`verify_language.py` caught the fifth kit, and it is the fifth time in the programme.** Nothing in
  `pytest` could have: the conflict is between a token and a background the APP paints, and only the
  headless capture puts the two on the same cell. It also means the four kits that passed did so because
  none of them paints a second ground under body text — **luck of composition, not a property anyone
  asserted.**
* **Solari's `due` field is immune and its three tagged fields are not**, for a reason that is one method
  call: `cell(text, ink, face)` carries a background and `f"[{tone}]…"` does not. The kit already knew
  the answer for one of its four fields.
* **`instrument.unit` was `mut` spelled twice**, and nothing asserted the two were equal. They are equal
  again after this increment because a human noticed; a law that a language's declared sub-tones are
  drawn from its declared tones does not exist.
* **prism is the only kit whose `dim` clears 3:1, and it is not by design** — `#5b6675` on `#0d1117` at
  3.25 is the same "one step off the panel" idea every other kit spends at 1.2–1.9. The outlier is
  arbitrary, which is worth knowing before anybody cites it as precedent.
* **`test_win_clipboard_roundtrip` was RED in this increment's run**, as in the baseline. Reported, not
  counted, not touched.

---

## 10. Pending — not this increment

* **solari's `mut`** — blocked on a ruling about the selection band's ink (§3).
* **`dim` against the ground** — 10 of 11 under the non-text 3:1, measured and rostered (§4).
* **The invalid-rune discrepancy** — 12 rows across two instruments, waiting on a ruling.
* **L6, L7, L10, C5–C10, E2, E3, G2** and the language-level alphabet work naught and darkside need —
  untouched.

## 11. Suggested next task

**Close the batch:** `export_to_skill.py`, `spec.md` §17, and push. Then the two decisions this batch
surfaced and could not take: solari's band ink, and whether the census adopts the law's exclusion of the
invalid rune (which would clear six collision rows and six homoglyph rows at once).

---

## Evidence checklist

- [x] **Tests / type checks / lint pass** — `pytest -q` **1248 passed**, 1 failed
  (`test_win_clipboard_roundtrip`, environment-coupled, red in the baseline, named in §7).
  `verify_language.py` **ALL PASSED, exit 0** — and it was RED on the first attempt, which is §3.
  `render.py` 66/330/0. `matrix.py` refusals `[]` × 11. `collision_census.py` both self-checks green.
- [x] **No secrets in code or output** — colour hexes and ratios only; no credential, token or
  out-of-worktree path.
- [x] **No destructive commands run without approval** — no `rm`, no force push, no rename.
- [x] **File count within cap** — **2 source files**: `taskboard/themes.py`, `tests/test_components.py`.
  Regenerated artefacts (24 component `.svg`, 8 gallery `.svg`) are gate outputs.
- [x] **Review packet attached** — this file.

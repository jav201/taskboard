# Increment 73 — K6, the `alert` floor, the match tier, and the ruling that a token has one role

**Batch:** `rework-7a`, increment 2 of 4 · **K6**, **K7's `alert` clause**, **the match tier** and
**the role ruling**.
**Files:** `taskboard/themes.py`, `taskboard/language.py`, `tests/test_components.py` — **3 source
files**, plus 30 regenerated component `.svg` and 11 regenerated gallery `.svg`. **No `.txt` moved,
in any of the 66 or the 22** — this increment is colour only, and that is checkable rather than
claimed.

**inc70 asked one number per kit against the CANVAS. Five kits paint a second ground.** Round four
measured what that hid — ledger's `mut` at 4.10:1 on its band, industrial's at 4.20:1 on its plate,
industrial's `focus` at **1.28:1** and its `alert` at 4.06:1 — and its §7.2 wrote the general form:
*"a floor reached by the smallest possible step breaks against the first rect somebody paints under
it."* This increment builds the instrument that reads the ground under every painted run in the 66
sheets, reports what fails, and moves ten tokens in seven kits.

**And it reports two clauses of the original brief back to the orchestrator with arithmetic, both of
which were then re-ruled.** The match tier as first written was unsatisfiable in every kit at every
token value; industrial's `focus` was a defect no floor could catch, because the value was correct
as a ground and wrong as ink.

Suite **1252 → 1289**. Census unchanged (**29** colliding cells, **24** homoglyph rows) — no glyph
moved.

---

## 0. Rulings

### 0a. The four carried from the batch brief (orchestrator, 2026-09-07, on the operator's delegation)

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

This increment carries out **K6**, **K7's `alert` clause** and **the match tier**. K7's `dim` clause
and L7 are inc74.

### 0b. Two rulings correcting the above (orchestrator, 2026-09-07, on the operator's delegation)

Both were issued after this increment reported the arithmetic in §2 and §3. They are quoted verbatim
because a clause withdrawn without its reason comes back.

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

---

## 1. The instrument, and what it found before any token moved

`painted_runs(svg)` splits every `<text>` element wherever the `<rect>` beneath it changes, **cell by
cell**, and returns `(ink, ground, text, bold, underline)`. Attribution is by coordinate: the
character's own centre against the rect's span, using the exporter's `ry = PAD + y*LH` and
`ty = ry + 0.78*LH` — which a second law asserts against `capture_languages.py`'s source, so the
reader and the writer cannot drift.

**Per character and not per run, and round four's §8.3 is why:** its own first pass attributed whole
runs to two-cell plates and produced contrasts of 1.00:1 and 1.03:1 that were the measurer's
artefacts. Reported here because a measurement that does not publish its own false positive is not a
measurement.

**The report, at `3b94867`, before anything moved:**

```
corgi       alert     2 runs  worst 3.99  on #0d0d0d              S1 S2
industrial  alert    11 runs  worst 4.06  on the plate #2e2e2e    S1
industrial  focus     8 runs  worst 1.28  on #1a1a1a              S6
industrial  mut      28 runs  worst 4.20  on the plate #2e2e2e    S1
ledger      mut      10 runs  worst 4.10  on the band  #e0d7c2    S1 S4
naught      alert    17 runs  worst 4.05  on #000000              S1 S2 S3 S6
nord        alert     2 runs  worst 3.05  on #2e3440              S1 S2
solari      mut      81 runs  worst 3.65  on #0b0b0c              all six   (EXEMPT)
swiss       alert    31 runs  worst 4.07  on #101010              all six
```

**Every number round four published reproduces exactly.** The one it did not name is
`industrial alert 4.06` on the plate, which is the fifth `alert` its §7.3 counted without listing.

---

## 2. Why the match-tier clause had to be re-ruled, and the arithmetic that did it

For any three colours ordered by luminance, WCAG's ratio is exactly multiplicative — every term is a
ratio of `L + 0.05`:

```
contrast(ink, ground)  ==  contrast(ink, mut) x contrast(mut, ground)
```

A match ink 3:1 from **both** `mut` and `ink` therefore forces `contrast(ink, mut) >= 9`, and with
K6's `mut >= 4.5` it forces `contrast(ink, ground) >= 40.5`. **The physical maximum is 21:1**, white
on black. Measured headroom, and the best reachable if `mut` sat exactly on the K6 floor:

```
kit          ink/gr  mut/gr  ink/mut   best possible ink/mut
instrument    16.52    4.50     3.67          3.67
swiss         17.30    5.51     3.14          3.84
industrial    15.55    5.38     2.89          3.45
nord          10.84    4.51     2.40          2.41
darkside      19.26    4.56     4.23          4.28   <- corpus maximum
solari        16.81    3.65     4.61          3.73
blueprint     10.60    4.65     2.28          2.36
naught        19.26    6.08     3.17          4.28
corgi         17.36    6.91     2.51          3.86
prism         16.02    6.43     2.49          3.56
ledger        13.36    4.51     2.96          2.97
```

**Not eleven exemptions — the clause.** And the two clauses actively fight: this increment's K6 fix
for ledger (`mut` `#6a6458` → `#635e52`) moves the match tier **2.96 → 2.69**, which is round four's
§7.1 objection reproduced as arithmetic rather than as a complaint.

Seven kits also spell `MATCH_STYLE` with the token `ink`, so "match ink vs `ink`" is **1.00 by
construction** there and no value could change it — the channel is weight, which is operator ruling
9's own position (*the emphasis may not add a cell*).

---

## 3. Why industrial's `focus` was a defect no floor could catch

`THEMES["industrial"]` declared `plate = "#2e2e2e"` **and** `focus = "#2e2e2e"`, and
`Industrial.keyhint` painted the key plate's WALLS in `self.plate`:

```python
return "   ".join(f"[{self.plate}]{mark('▐')}[/]" ...       # a GROUND name, as INK
```

So one hex was a rect's fill in sixteen places and a glyph's colour in eight, and as a glyph it stood
at **1.28:1** on `#1a1a1a` — the eight cells round four's §2.3 found. **A floor law cannot catch
this**: the value is correct as a ground and wrong as ink, and `contrast(token, ground) >= 3` cannot
tell which the token is.

**The other ten were checked, as the ruling asked. One clash in eleven kits, and it is the one the
ruling names.** solari's second ground already has a name (`flap`; `band = "reverse"` is a style word
and not a colour); darkside's grey steps are `dim` and `rail` at one hex, both INK-role, which is an
alias and not a double role.

---

## 4. Every token moved, with every ratio

| kit | token | old | new | clause | before → after |
|---|---|---|---|---|---|
| industrial | `mut` | `#8f8f8f` | `#959595` | K6, on the plate | 4.20 → **4.53** (canvas 5.38 → 5.72) |
| industrial | `alert` + `accent` | `#ff4b1f` | `#ff6039` | K7, on the plate | 4.06 → **4.52** (canvas 5.20 → 5.79) |
| industrial | `focus` | `#2e2e2e` | `#777777` | role ruling + K6 | 1.28 → **3.03** on `#1a1a1a`, **3.03** on `#2e2e2e` |
| ledger | `mut` | `#6a6458` | `#635e52` | K6, on the band | 4.10 → **4.51** (page 4.51 → 4.96, panel 4.98 → 5.48) |
| nord | `alert` | `#bf616a` | `#cf888f` | K7 | 3.05 → **4.50** |
| nord | `accent` | `#88c0d0` | `#8fbcbb` | match tier, hue | hue gap 25.4°/24.2° → **40.0°/38.8°**; legible 6.24 → 5.99 |
| corgi | `alert` | `#d92b1a` | `#e53524` | K7 | 3.99 → **4.50** |
| naught | `alert` + `accent` + `warn` | `#d71921` | `#e51b24` | K7 | 4.05 → **4.51** |
| swiss | `alert` + `accent` + `warn` | `#e2231a` | `#e7372e` | K7 **and** match legibility | 4.07 → **4.52** |
| swiss | `mut` | `#8a8a8a` | `#9b9b9b` | match tier, achromatic fallback | vs match 1.36 → **1.52**; ground 5.51 → 6.85 |

**Every move is the smallest HLS lightness step that clears every clause at once**, hue and
saturation held exactly — the same method inc70 declared — except nord's `accent`, which is a HUE
move by definition and takes `#8fbcbb`, **Nord's own published frost-0**, so the scheme does not
leave its palette to gain the channel.

**Three kits move `accent` with `alert` because the two are one hex by declaration** (industrial's
comment: *"the language's one loud colour does identity AND severity"*; naught's ration; swiss's one
red). Splitting them to satisfy a floor would have turned a one-colour ration into two.

**swiss took two moves and the second one moved the GREY, not the RED.** Its `mut` and `ink` are
achromatic (saturation 0.00), so the ruling's hue clause cannot apply and its fallback does: the
match ink must differ from body text by 1.5:1 and it was 1.36. Reaching 1.5 by moving the red takes
it to about `#ff8c7d` — a salmon — and costs the kit its signature colour. The grey moved instead.

**solari is exempt and the exemption is the one already written.** `THE_BAND_IS_A_SECOND_GROUND`
carries an impossibility proof from inc70: 4.5:1 against `#0b0b0c` needs `L(mut) >= 0.19021`, 2.5:1
against the amber band needs `L(mut) <= 0.14960`, and the two floors do not overlap. A `mut` under
the floor against its own canvas cannot clear it against anything, so the new law asserts the
exemption is real and that **`mut` is the only tier that fails there**.

---

## 5. The match tier, by branch — which kit is in which, and what each is asked

| branch | kits | legible (a) | distinct (b) |
|---|---|---|---|
| weight | blueprint 10.60 · naught 19.26 · corgi 17.36 | ✓ | the S6 run carries `font-weight`, and the styled runs are the match ink |
| decoration | ledger 13.36 | ✓ | the S6 run carries `text-decoration` |
| reverse | industrial **5.79** · darkside 4.56 · solari 16.81 | ✓ | a rect of the declared colour exists and the runs on it are the knockout |
| hue | instrument 10.45 (38.7°/37.5°) · nord **5.99** (40.0°/38.8°) · prism 10.17 (37.5°/35.2°) | ✓ | hue ≥ 30° from `mut` and from `ink` |
| hue, achromatic comparands | swiss **4.52** (1.52:1 vs `mut`) | ✓ | the 1.5:1 luminance fallback |

**Two failed and both are fixed above:** nord on hue (25.4°) and swiss on legibility (4.07) *and* on
the achromatic fallback (1.36). Bold values are the ones this increment moved.

**darkside's `reverse {mut}` reads 1.00:1 against `mut` and that is correct**, not a failure: the
match ink IS `mut` and the channel is the rect it stands on. The retired clause would have called
this the worst reading in the corpus.

---

## 6. The laws

**`test_this_files_picture_metrics_are_the_exporters`** — the coordinate reader is wrong the moment
the exporter's cell box changes, so `_CW/_LH/_PAD/_BASE_FRAC` are checked against
`capture_languages.py`'s own source lines rather than trusted. Declared and not imported, because
that module pulls in Textual and this file reads the pictures as bytes on purpose.

**`test_every_painted_run_clears_its_tiers_floor_on_its_own_ground`** — K6, over all 66 sheets, per
character. `TIER_FLOOR = {ink 4.5, mut 4.5, alert 4.5, focus 3.0}`, each asked against the ground the
run actually sits on. `dim` is deliberately absent: K7 asks it only where it CLASSIFIES, which is a
seat table and inc74's.

**`test_the_match_run_is_legible_and_distinct_on_its_declared_channel`** — the re-ruled match tier,
four branches, derived from `MATCH_STYLE` rather than typed. The weight and reverse branches are
STRUCTURAL assertions on the shipped `.svg`: no luminance clause, because 1.00:1 against `ink` is
correct for a kit whose match is its own ink made bold.

**`test_a_token_has_exactly_one_role`** — the role ruling, over `THEMES`, all eleven. Asked of the
VALUES and not the names, because that is where the defect lived. A last clause ties `INK_ROLE` to
`Kit.__init__`'s own `self.c`, so the set a law asks about and the set a kit paints with cannot
drift.

**`reverse` is excluded from the ground-role set by name**, and the exclusion is deliberate: it swaps
a run's declared pair at composition time (`cell_grid`, inc43), so the rect is the run's own ink
turned inside out for the length of a match, not a colour the theme names twice. The match law's
`reverse` branch is what asserts that rect exists.

## 7. Teeth

**`test_the_second_ground_law_bites_on_the_four_runs_round_four_measured`** restores each old hex and
asserts, for every one, the ratio round four measured, that it is under its floor, that the shipped
value is not it, and that the shipped value clears. **The arm that matters most is industrial's
`mut`:** `#8f8f8f` cleared **5.38:1** against the canvas and inc70's law was green on it for two
batches. It is the plate that catches it, which is the whole of K6.

**`test_the_match_tier_law_bites_on_the_two_declarations_inc73_moved`** — two arms, two branches.
nord's `#88c0d0` is restored and the hue gap is asserted at exactly 25.4° before the law goes red.
swiss's `alert` and `mut` are restored **one at a time**, because they failed different clauses.

**`test_the_role_law_bites_on_the_declaration_industrial_shipped`** restores `focus = "#2e2e2e"`,
asserts the reading that makes it matter (**1.28:1** on this kit's ground), and asserts the other ten
stay green — so the law is not passing on a global accident.

## 8. One structural change in the kit, and it is the ruling's

`Kit.__init__`'s `self.c` gains `focus`. It held `ink mut dim accent warn alert` — the set a kit
paints WITH — and `focus` was outside it, which is exactly why `keyhint` reached for `plate`: the
ink-role token it wanted was not in the dict it paints from. `Industrial.keyhint` now draws its
walls in `c["focus"]`; the plate keeps its hex and its rect.

## 9. Frames changed — **svg only, and that is checkable**

**0 `.txt` moved, of the 66 and of the 22.** 41 `.svg`:

| | files |
|---|---|
| components (30) | all six of `industrial`, `ledger`, `nord`, `swiss`; `naught` S1 S2 S3 S6; `corgi` S1 S2 |
| gallery (11) | `board_corgi` `board_industrial` `board_ledger` `board_naught` `board_nord` `board_swiss` · `gallery_industrial` `gallery_ledger` `gallery_naught` `gallery_nord` `gallery_swiss` |

`naught` S4 and S5 and `corgi` S3–S6 do not paint a moved token; `instrument`, `darkside`, `solari`,
`prism`, `blueprint` moved nothing at all.

**Gallery 30–51 in the skill:** the batch close runs `export_to_skill.py`; see §13.

## 10. Gate tails, verbatim

```
$ python -X utf8 -m pytest -q
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
1 failed, 1289 passed, 2 skipped, 4 warnings in 33.70s

$ python -X utf8 prototypes/verify_language.py
ALL PASSED
                                                        (exit 0)

$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> ...\prototypes\components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                        (exit 0)

$ python -X utf8 prototypes/components/matrix.py
  66 of 66 · refusals [] for all eleven                 (exit 0)

$ python -X utf8 prototypes/collision_census.py
TOTAL                       29
TOTAL homoglyph rows            24
                                                        (exit 0)

$ python -X utf8 prototypes/capture_languages.py
  22 grids identical across two PROCESSES
  22 captures -> ...\prototypes\gallery
  no two boards identical
                                                        (exit 0)
```

Suite **1252 → 1289** (+11 K6 arms, +11 match arms, +11 role arms, +1 metrics, +3 teeth). Census
**unchanged**: no glyph moved.

## 11. Risks

1. **Ten tokens moved in seven kits and the only artefact that can show it is a picture.** The
   `.txt` are byte-identical by construction, so the entire visible cost of this increment lives in
   41 `.svg` and nowhere else. Round five judges colour on those files.
2. **swiss's `mut` is 6.85:1 now**, the highest body grey in the corpus. It buys the match's 1.5:1
   and it narrows `ink/mut` from 3.14 to 2.53 — the channel round three used to read swiss's
   hierarchy by. No clause covers that ratio any more, deliberately (§2).
3. **industrial's `focus` is `#777777`, a mid grey, and it is drawn as a key plate's walls.** It
   reads as a lighter bracket than the plate it used to match. The plate's rect is unchanged, so
   `industrial_S1`'s plates look exactly as they did; only the S6 key legend changed weight.
4. **nord left `#88c0d0`.** That hex is Nord's frost-2 and has been this kit's accent since the first
   pass. `#8fbcbb` is frost-0 — still Nord, still cool, and a different colour. It is the largest
   identity change in this increment and it is the one a reader will notice first.
5. **`focus` is now in `self.c` and `depth_ground()` still reads `t["focus"]` as a GROUND** for
   darkside and prism (§12). The role law does not catch it because those two kits' values are
   disjoint from their ground-role tokens; it is a code-path double role, not a token one.
6. **The coordinate reader assumes one rect layer.** If the exporter ever nested backgrounds, the
   first matching rect would win and the reading would be wrong without going red. The metrics law
   guards the cell box, not the layering.

## 12. Found by looking, not fixed

- **`Kit.depth_ground()` returns `t.get("focus")`** — an ink-role token read as a ground, for
  darkside and prism, the two `depth` surface kits. The values happen to be disjoint from those kits'
  ground tokens so the new law is green; the *code* still has the double role the ruling is about.
- **solari's `mut` is the last K6 failure and its resolution is not a token change.** The exemption's
  own note says so: a per-row ink for the banded row, which `_sched_row` cannot see because the band
  is painted by the app's CSS. Still a request for a ruling, four batches on.
- **`ink/mut` headroom is now the corpus's tightest number and nothing asks about it.** After this
  increment swiss reads 2.53 and nord 2.40. §2 proves no match clause can constrain it; whether
  `ink > mut` is still a *visible* ladder at 2.4:1 is a question no law here poses.
- **industrial's `warn` `#ffd400` was never measured** — it is not in `TIER_FLOOR`, because no ruling
  names it. It reads 12.4:1 on the canvas and 9.6:1 on the plate, so it would pass; the point is that
  nothing asks.
- **The `.txt` cannot show any of this.** Six of the eleven kits' component sheets are byte-identical
  before and after ten token moves, which is the strongest statement available that colour is a
  channel this corpus judges separately.

## 13. Pending — not this increment

- inc74 (K7's `dim` clause and L7), inc75 (C8's second half and industrial's paper).
- The batch close: `export_to_skill.py`, `spec.md` §19.
- solari's per-row band ink; `depth_ground()`'s role.

## 14. Suggested next task

inc74: `DIM_CLASSIFIES` — the per-seat table separating a `dim` run that classifies (a severity rung,
a dash ladder, a state mark, ledger's inactive mode labels) from one that decorates (a leader, a
seam, a rail, a pager), and the nine `info` rungs painted under 2:1.

## Evidence checklist

- [x] **Tests/type checks/lint pass — WITH ONE RED, NAMED.** `1289 passed, 2 skipped, 1 failed`
      (inc72 closed at `1252 passed`). The failure is
      `tests/test_app.py::test_win_clipboard_roundtrip`, environment-coupled (spec §10.6) —
      **reported, not counted, not touched.** `verify_language.py` ALL PASSED exit 0.
      `render.py` 66 `.txt` + 66 `.svg` / 330 pairs / 0 hand-drawn. `matrix.py` refusals `[]` ×11.
      `collision_census.py` both self-checks green, TOTAL 29 and 24 homoglyph rows, **both
      unchanged** — no glyph moved. `capture_languages.py` plain: 22 captures, 22 grids identical
      across two processes, 11 artefacts moved.
- [x] **No secrets in code or output** — ten token values, one dict key, one kit method, four laws,
      three teeth. No network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none.
- [x] **File count within cap** — **3 source files**: `taskboard/themes.py`, `taskboard/language.py`,
      `tests/test_components.py`.
- [x] **Review packet attached** — this document.

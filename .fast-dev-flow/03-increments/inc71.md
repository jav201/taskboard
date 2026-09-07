# Increment 71 — one definition for the field's rune, and the census stops arguing with the law

**Batch:** `rework-6c`, the whole of it · one increment.
**Files:** `taskboard/language.py`, `tests/test_components.py`, `prototypes/collision_census.py` —
**3 source files**, plus the regenerated `prototypes/out/collision_census.txt`. **0 component frames, 0
gallery artefacts** — this increment moves no glyph, only which family a cell's rune is read into.

**The census and the law have disagreed about one cell since inc52: a rejected field's glyph is
wall-RUNE-wall, and `_invalid_marks` excludes the RUNE by name while `collision_census.py`'s `role_map`
counted it as a rejection mark anyway.** Both files split the same string by hand, in two places, and the
two splits could drift — and did, for five languages at inc52 and a sixth at inc66 (`swiss`, inc66 §8).
`spec.md` §15.5, §16.4, §17.4 and §17.8 named the discrepancy in four separate packets across three
batches without closing it. This increment moves the split into one function, `taskboard/
language.py::split_field_glyph`, that `Kit.field_form`, `_invalid_marks` and `collision_census.py::
role_map` all call. **Collisions 35 → 30, not the predicted 35 → 29. Homoglyph rows 30 → 26, not the
predicted 30 → 24 — both short of the prediction by the same two rows, and §4 below is why.** Suite
1248 → 1249.

---

## 0. Rulings (orchestrator, 2026-09-07, on the operator's delegation)

> **One definition.** The invalid field's RUNE (its paper, the middle cell) is chrome, not a meaning; the
> census adopts the laws' exclusion. Move the definition to one place both files import (a small function
> or constant in `taskboard/language.py` or a shared module under `prototypes/`, whichever the two already
> share), so the census and the laws cannot disagree again.

> **solari's `mut`** stays exempt by name with the arithmetic (`L ≥ 0.19021` against the ground, `L ≤
> 0.14960` against the band): the selection band is a second ground and a per-row ink is app CSS work
> outside this programme. Recorded as doctrine in the kit docstring and in `spec.md`; the exemption's
> stale check stays.

This increment carries out the **first** ruling. The **second** ruling asks for nothing to move: the
doctrine it names is already written, verbatim arithmetic included, in `taskboard/themes.py` lines 134–190
(inc70's own commit) and in `inc70.md` §3. §6 below records it here as the ruling asked, and no code
changed for it — `THE_BAND_IS_A_SECOND_GROUND` (`tests/test_components.py`) and its stale-exemption check
are untouched, exactly as instructed.

---

## 1. Where the two readers disagreed, read off the source

`Kit.field_form` already had the split (`taskboard/language.py`, unchanged in shape until this increment):

```python
def field_form(self, state: str, name: str) -> tuple[str, str, str]:
    g = self.part_glyph("main", state, name)
    h = len(g) // 2
    return g[:h], g[h], g[h + 1:]
```

`tests/test_components.py::_invalid_marks` (the law) had its own copy of the same arithmetic:

```python
if key == "textfield.main":
    h = len(g) // 2
    out += [g[:h], g[h + 1:]]          # the two WALLS, not the rune
```

`prototypes/collision_census.py::role_map` (the census) had **no copy at all** — it read every cell of
`part_glyph(part, state, comp)` for `state == "invalid"` into the `invalid` family, rune included, because
nothing there knew a field's glyph had a middle cell that meant something else. Three readers, one of them
blind to the rune's existence, the other two each trusting their own arithmetic to agree with a
declaration neither imports from the other.

## 2. The one function

`taskboard/language.py`, placed at module scope so both a `Kit` method and two other files can call it
without an instance:

```python
def split_field_glyph(glyph: str) -> tuple[str, str, str]:
    """A field's glyph split into `(opener, RUNE, closer)` — the wall that
    opens it, the RUNE its paper is made of, and the wall that closes it. An
    ODD length, so the two walls are halves of what is left when the rune is
    taken out of the middle.

    THE ONE PLACE THIS SPLIT IS MADE (rework-6c). `Kit.field_form` calls it
    to read a live declaration; `tests/test_components.py::_invalid_marks`
    and `prototypes/collision_census.py::role_map` call it to agree on which
    cell of a rejected field is a REJECTION MARK (the two walls) and which is
    CHROME (the rune -- the paper every other state of the field lies on
    too)."""
    h = len(glyph) // 2
    return glyph[:h], glyph[h], glyph[h + 1:]
```

`Kit.field_form` now delegates to it instead of carrying its own copy. `_invalid_marks` calls it for the
`textfield.main` branch and keeps the two walls, dropping the rune exactly as before — same behaviour,
one definition. Two other call sites in `tests/test_components.py` that split a field glyph by hand
(`test_the_rune_is_excluded_from_the_invalid_channel_by_name`'s two `g[len(g)//2]` reads) were moved onto
the same function while they were being read anyway, so the whole file has no second copy of the
arithmetic left.

`collision_census.py::role_map` gains the branch that reads it:

```python
if state == "invalid" and comp == "textfield" and part == "main":
    op, rune, cl = LG.split_field_glyph(glyph)
    for wall in (op, cl):
        for cell, pos in _cells(wall):
            add(bag, cell, "invalid", f"INVALID {comp}.{part} {pos}")
    for cell, pos in _cells(rune):
        add(bag, cell, comp, f"{comp}.{part} {pos} [{state}]")
    continue
```

The rune is now credited to `comp`'s own chrome family (`"textfield"`) — exactly where every *other*
state's rune already lands, three lines above this branch, unchanged. Before this increment the rune
counted **twice under one name**: once as chrome (every non-invalid state) and once as `invalid` (the
invalid state only), which is what let it read as a manufactured collision.

## 3. Teeth: the two readers move together, or they haven't agreed

`test_the_census_and_the_law_read_the_rune_off_one_function` (`tests/test_components.py`), on blueprint's
live declaration:

```python
k = LG.kit("blueprint")
glyph = k.PART_GLYPHS["textfield.main"][LG.INVALID]
op, rune, cl = LG.split_field_glyph(glyph)
assert rune == "·", (op, rune, cl)

assert "·" not in _invalid_marks(k)
named, _ = census.role_map("blueprint")
assert "invalid" not in named.get("·", {}), named.get("·")

monkeypatch.setattr(LG, "split_field_glyph", lambda g: ("", g[0], g[1:]))
assert "·" in _invalid_marks(k)
named2, _ = census.role_map("blueprint")
assert "invalid" in named2.get("·", {}), named2.get("·")
```

It loads `collision_census.py` as a module (the same `importlib` pattern
`test_the_homoglyph_table_is_one_table_in_two_files` already uses to compare the two files' tables) and
asserts the boundary in both directions on the SAME monkeypatch: today neither reader treats the rune as a
rejection mark, and after breaking `split_field_glyph` so it reads one cell early, **both readers see the
displaced rune as a wall at once** — not one of them, which is what "one definition" has to mean to be
worth writing.

## 4. The census, before and after, and the two rows the prediction missed

**Collisions, per language:**

```
language      before   after
naught             4       3
corgi              5       4
instrument         4       4
swiss              5       4
industrial         2       3
nord               1       1
darkside           1       1
prism              4       4
ledger             2       1
solari             4       3
blueprint          3       2
--------------------------------
TOTAL             35      30
```

**Homoglyph rows, per language:**

```
language      before   after
naught            12      12
corgi              1       0
instrument         0       0
swiss              1       1
industrial         0       0
nord               1       1
darkside           8       8
prism              0       0
ledger             2       1
solari             2       1
blueprint          3       2
--------------------------------
TOTAL             30      26
```

**Six languages' rune stopped being a false meaning (naught, corgi, swiss, ledger, solari, blueprint), and
the prediction in `spec.md` §17.4/§17.8 was that each of the six would drop a collision row and, for five
of them, a homoglyph row too. Measured, four of the six behave exactly that way and two do not — and both
exceptions are real findings, not slippage:**

- **corgi, ledger, solari, blueprint** — CLOSE on both counts. Each rune's collision partner and homoglyph
  partner is a cell with **no A-family membership of its own** (a bare `●`, in every one of the four). Once
  the rune stops carrying `invalid`, neither side of the pair has a meaning left, and the row disappears —
  both the collision and, where one existed, the homoglyph.
- **naught's two homoglyph rows do NOT close — they reclassify, and the collision count still drops by
  one.** naught's rune (`⋅`) pairs with `∙` (`DANGER_FORM` + `LEVELS[error]`) and `●` (`CUR`), and **both
  of those ARE real A-family meanings**, not bare chrome. Before this increment the pair read as
  meaning-×-meaning (`⋅`'s manufactured `invalid` against `∙`/`●`'s real family); after it, `⋅` is chrome
  and the same two rows read the other way round — a real meaning against `⋅`'s own chrome — which is the
  same MEANING-×-CHROME shape every other row in `HOMOGLYPH_ROSTER` already has. The row is not wrong
  either way; only its *cause* moved. naught's **collision** count still drops by one, because `⋅` itself
  stops being a colliding CELL (it now carries no A-family at all, only chrome, so `collides()` no longer
  flags it) even though the *homoglyph* table still lists its partners.
- **industrial GAINED a collision row, and it is a real one the old bug was hiding.** industrial's field
  walls (`▐`/`▌`) never change under `INVALID` — inc52 §9 already named industrial as one of the two kits
  whose invalid walls are its DEFAULT walls, only the paper changes — and that paper, `/`, is **also**
  industrial's own declared invalid mark at `slider.knob` and `stepper.step`. Before this increment both
  uses landed in the same `invalid` family, so the cell showed one family and no collision (the census's
  own rule: two declarations sharing one family is not a collision, the same reasoning that keeps a
  language's own severity ladder from tripping itself). After the fix, the field's use of `/` is chrome and
  the knob/stepper's use is still `invalid` — genuinely two different roles on one cell, correctly flagged
  now: `/  [2 families]  INVALID slider.knob mark + INVALID stepper.step close + INVALID stepper.step open
  · textfield.main mark (invalid)`. **The old classification was hiding a real A-×-B collision behind a
  coincidental same-family merge; this is the fix working as intended, not a regression.**

Net: **6 collisions removed by the fix, 1 added by the fix it also revealed = −5 (35 → 30).** **4
homoglyph rows removed, 2 reclassified in place = −4 (30 → 26).**

## 5. `collision_census.py`'s own bookkeeping, updated in place

The `HOMOGLYPH_ROSTER` dict and its explanatory bucket (the "THE INVALID RUNE" paragraph inside the
`HOMOGLYPH_FAMILIES` docstring block) are rewritten to match §4 rather than deleted — the file's own rule
is that a closed row STAYS in its explanation with the increment that closed it (`FOUND_BY_HAND`'s
`closed_by` field, same bargain). The rewritten paragraph names which four kits close, why naught's two do
not, and corrects the six-row prediction to the four-plus-two split measured here.

```python
HOMOGLYPH_ROSTER = {"naught": 12, "corgi": 0, "instrument": 0, "swiss": 1,
                    "industrial": 0, "nord": 1, "darkside": 8, "prism": 0,
                    "ledger": 1, "solari": 1, "blueprint": 2}
```

`self_check()`'s `FOUND_BY_HAND` roster needed no edit — none of its five hand-found rows touch a field's
rune.

## 6. solari's `mut` — the second ruling, recorded and not acted on

No code moved. The doctrine the ruling asks to be recorded is already present, verbatim:

- **`taskboard/themes.py` lines 134–190** carries the full arithmetic — `4.5:1 against #0b0b0c -> L(mut)
  >= 0.19021` and `2.5:1 against #f5a300 -> L(mut) <= 0.14960` — and the conclusion, "the two floors do not
  overlap."
- **`inc70.md` §3** is the packet that derived it, with the same two inequalities and the naming of
  `THE_BAND_IS_A_SECOND_GROUND` (`tests/test_components.py`) as the exemption that stands until a
  `Solari`-specific per-row ink exists.
- **`spec.md` §18** (below) is this batch's own record of the ruling, so a reader does not have to open
  `inc70.md` to find why solari is still at 3.65:1.

`THE_BAND_IS_A_SECOND_GROUND`'s stale-exemption check (`tests/test_components.py`, asserted against
`solari` by name) is untouched — it still asserts solari is *really* under the floor, so the day someone
gives `_sched_row` a per-row ink the check goes red on its own rather than sitting there unnoticed.

## 7. Gates, verbatim

```
$ python -X utf8 -m pytest -q
1 failed, 1249 passed, 2 skipped, 4 warnings in 36.39s
FAILED tests/test_app.py::test_win_clipboard_roundtrip - AssertionError: assert None == 'roundtrip 123 ABC taskboard'
```

`1248 → 1249`, **+1** (the new teeth test, §3). `test_win_clipboard_roundtrip` drives the real Windows
clipboard through PowerShell and was red at the `rework-6b` baseline too (`inc70.md` §7); environment-
coupled, reported, not counted, not touched.

```
$ python -X utf8 prototypes/verify_language.py
ALL PASSED                                                                    (exit 0)
```

Unaffected by construction — it reads live kit declarations through `field_form` and `part_glyph`, neither
of which changed what they return; only a metadata reader three files away learned to call the same split.

```
$ python -X utf8 prototypes/components/render.py
  66 .txt + 66 .svg -> …/prototypes/components
  66 candidates files
  no two frames identical within a screen (330 pairs)
  0 hand-drawn elements declared (0 refused, 0 evoked)
                                                                                (exit 0)
$ git status --short prototypes/components/ prototypes/gallery/
(nothing)
```

**0 of 66 frames moved, 0 of 22 gallery artefacts moved** — expected: no glyph table changed, only which
family a rune's cell is filed under.

```
$ python -X utf8 prototypes/components/matrix.py
  66 of 66 implementa · refusals [] for all eleven                            (exit 0)

$ python -X utf8 prototypes/capture_languages.py plain
  22 grids identical across two PROCESSES
  22 captures -> …/prototypes/gallery
  no two boards identical                                                     (exit 0)

$ python -X utf8 prototypes/collision_census.py
self-check  1 of the 5 collisions the round found by hand still come back out of the census; 4 are asserted CLOSED and cannot grow back
self-check  the homoglyph roster is exact for all eleven (26 rows, 7 languages)
TOTAL                       30
TOTAL homoglyph rows            26
                                                                                (exit 0)
```

Both self-checks green **on the first run** — the rewritten `HOMOGLYPH_ROSTER` and the reclassified
`FOUND_BY_HAND` reads (none needed editing) matched the measured numbers without a second pass.

## 8. Risks

1. **The two-row shortfall against the prediction is explained, not merely observed** (§4), but the
   explanation rests on reading `role_map`'s output by hand for naught and industrial. Nobody re-derived
   the six original rows' partners independently before this increment to confirm the prediction's
   arithmetic; §4's account is this increment's own reading of the diff.
2. **`split_field_glyph` is now load-bearing for three files instead of documentation for one.** A future
   change to how a field's glyph is laid out (say, an even-length field with no single rune cell) would
   need this function's contract to change too, and all three callers would need re-reading — the same
   cost any shared primitive has, traded for the one-definition guarantee the ruling asked for.
3. **industrial's new collision row is a real finding with no ruling over it.** `/` doing double duty as
   the field's paper and the knob/stepper's rejection mark is not fixed here — only correctly counted for
   the first time. It joins the pile of language-level findings this programme keeps surfacing and not
   acting on (L6, L7, L10, C5–C10, E2, E3, G1, G2, and now this).
4. **The rewritten `HOMOGLYPH_ROSTER` bucket paragraph is long** — five sentences longer than the six-row
   version it replaces — because it now has to explain two outcomes (close vs. reclassify) instead of one.
   Future readers inherit a denser comment for a more accurate one.

## 9. Found by looking, not fixed

- **The six-row prediction itself was written before anyone ran the fix, in three separate packets
  (`inc52.md` §0a, `inc66.md` §8, `inc70.md` §10, folded into `spec.md` §15.5/§17.4/§17.8), and none of
  them checked whether the rune's homoglyph or collision PARTNER carried an A-family of its own.** The
  prediction assumed every rune paired with pure chrome; two of six (both naught's) do not, and that is
  the whole of the two-row gap. **A number published without running the code is a guess with a byte
  count**, and this increment is the first time anyone ran it.
- **industrial's `/` has been doing two jobs since at least inc39** (the earliest declaration of
  industrial's invalid channel this repo's history reaches) and no instrument saw it until the census
  stopped merging the rune into the same family as the knob's real declaration. The collision was always
  there; only the census's own arithmetic was hiding it from itself.
- **`_invalid_marks`'s docstring already called the rune "the PAPER the value's own cells are laid on"
  four batches ago (inc52 §0a) and named the exclusion by principle.** The census's blind spot was never a
  disagreement about the PRINCIPLE — every packet that touched this agreed the rune is chrome — it was
  that nothing made the two files' CODE say so in the same place. The four-batch delay was a plumbing gap,
  not a standing disagreement.

## 10. Pending — not this increment

- **industrial's `/` collision** (§4, §8.3) — a real finding, no ruling.
- **L6, L7, L10, C5–C10, E2, E3, G1, G2** — untouched, carried from `rework-6b` (`spec.md` §17.6).
- **solari's `mut`** — blocked on the per-row-ink decision `inc70.md` §3 named; this increment recorded the
  doctrine and moved nothing (§6).
- **The skill repo** — `export_to_skill.py` was not run this increment (no `.txt`/`.svg` moved, so nothing
  to export); its own dirty-repo state from `rework-6b` (`spec.md` §17.5, G2) is unchanged.

## 11. Suggested next task

**industrial's `/` collision** (§4, §8.3, §10) — the field's paper and the knob/stepper's rejection mark
share one cell for a real reason (industrial's whole idiom is DEFAULT walls with a changed paper, inc52
§9), and now that the census can see it, it is the operator's to rule on: give the field a different paper,
or accept the double duty by name the way `DANGER_IS_THE_TOP_RUNG` accepts the ladder's top rung sharing a
cell with `danger`.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `pytest -q` **1249 passed**, 1 failed
      (`test_win_clipboard_roundtrip`, environment-coupled, red at the `rework-6b` baseline too, named in
      §7). `verify_language.py` **ALL PASSED, exit 0**. `render.py` 66/330/0, 0 of 66 moved.
      `matrix.py` 66 of 66 implementa, refusals `[]` × 11. `capture_languages.py plain` 22 grids identical
      across two processes, 0 of 22 moved. `collision_census.py` both self-checks green, **TOTAL 35 → 30**,
      **homoglyph rows 30 → 26** — both accounted for in §4, differing from the pre-registered prediction
      by two rows each, explained rather than forced to match. The new teeth test was watched fail by hand
      via its own monkeypatch before the fix existed (run against the pre-edit `collision_census.py` during
      development, not re-verified redundantly here since the committed test only encodes the POST-fix
      state plus the monkeypatch reversal — both directions are in the test body, §3).
- [x] **No secrets in code or output** — glyph-table splits, family labels and one shared function. No
      network, no new dependency, no path outside the worktree.
- [x] **No destructive commands run without approval** — none. `git stash` / `git stash pop` were used
      twice, non-destructively, to diff the pre-fix census against the post-fix one for §4's table, and
      both stashes were popped back cleanly in the same command.
- [x] **File count within cap** — **3 source files**: `taskboard/language.py`,
      `tests/test_components.py`, `prototypes/collision_census.py`. `prototypes/out/collision_census.txt`
      is a gate output, not hand-written.
- [x] **Review packet attached** — this document.

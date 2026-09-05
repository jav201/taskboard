# Increment 26 — F-15 not reproduced, bounded to one mechanism and detected at every seat; F-18 found

**Batch:** `harness-hygiene` · **AC-5** · `archive/spec-20260905-kits-learn-3-closed.md`, `race-probe.md` §9
**Files:** `tests/test_surface.py` — **1 source file**.

**F-15 did not reproduce in 50 suite runs or 4865 per-test evaluations, and the cause was not found. What
was found is that it has exactly ONE possible mechanism, that nothing in the repo can reach it today, and
that reading `finally` blocks was the only thing standing behind that claim. A detector now stands there
instead. The same runs surfaced a DIFFERENT flake, reproduced 2 times in 50, and it is not F-15.**

---

## 1. What F-15 was

From `kits-learn-3`'s close:

> "On the sixth full-suite run of this batch, `test_lattice_pixels_are_two_colours` failed on
> `len(set(res.pixels.getdata())) == 2`; the file passes 159/159 in isolation and the full suite then ran
> three consecutive times at 682 passed."

One observation, never explained, carried through five packets.

---

## 2. The instrument: what the assertion is a function of

`prototypes/out/_hh_f15_probe.py`. The whole chain, read and then measured:

```
naught.raster_region(probe(), 24, 8).pixels
  -> SURFACES[THEMES['naught']['surface']]                       # dispatch
  -> RS.quantise(img, *lattice_grid(24, 8), k.c['ink'], k.c['dim'])
  -> RS.bitmap(img, cols, rows)  ->  putdata(two hexes)  ->  resize(NEAREST)
```

```
== A. the assertion's inputs, live
  posture          'lattice'    ink / dim   #f5f5f5 / #242424
  dot_w / gap      1 / 0        lattice_grid (24, 8)
  bitmap lit/total 136/192      (both values present: True)
  colours          2

== B. determinism, in-process
  200 consecutive calls -> distinct results: [2]
```

**No clock, no RNG, no filesystem read, no import order, no async, no Textual.** The probe image is a
constant expression; the grid comes from two theme tokens; `quantise` paints exactly two hex colours onto
a nearest-neighbour resize.

### 2a. The failure map — every state that changes the number

```
  the posture token — the one that dispatches:
  RED   surface = 'depth'                        -> 57
  RED   surface = 'display'                      -> 64
  RED   surface = 'figure'                       -> 64
  RED   surface = 'frame'                        -> 64
  RED   surface = 'refuse'                       -> raised AttributeError
  RED   surface = 'tint'                         -> 64
  RED   surface = 'untinted'                     -> 64

  the two colours the lattice paints:
  RED   dim = ink (the two hexes collide)        -> 1
  RED   ink = dim (same collision, other way)    -> 1

  the grid the bitmap is sampled onto:
  green dot_w = 64, gap = 0                      -> 2
  green dot_w = 1,  gap = 64                     -> 2
  RED   dot_w = 0,  gap = 0                      -> raised ZeroDivisionError

  control:
  green surface = 'lattice' (no-op)              -> 2
```

**So the only way this assertion goes red is a mutated theme token.** Nothing else in its input chain can
vary between two runs of the same code.

### 2b. And no committed tree has ever been in one of those states

The assertion replayed against every commit from `kits-learn-2` (where the test was last touched) to this
one, each tree extracted with `git archive` into a scratch directory and imported on its own path:

```
  green c8f58d5  kits-learn-2 …            2 lattice #f5f5f5 #242424 1 0
  green 2455fcf  prototype round …         2 lattice #f5f5f5 #242424 1 0
  green d47abff  kits-learn-3 …            2 lattice #f5f5f5 #242424 1 0   <- the batch it was seen in
  green 16792b5  race probe …              2 lattice #f5f5f5 #242424 1 0
  green 7462881  capture-settle inc20 …    2 lattice #f5f5f5 #242424 1 0
  green 2817550  capture-settle inc21 …    2 lattice #f5f5f5 #242424 1 0
  green 4f05649  wedge inc22 …             2 lattice #f5f5f5 #242424 1 0
  green e3f1312  push-paint inc23 …        2 lattice #f5f5f5 #242424 1 0
  green 4a22a0a  harness-hygiene inc25 …   2 lattice #f5f5f5 #242424 1 0
```

Nine trees, identical tokens, all green. **The red state has never existed in a commit** — which is worth
saying plainly, because F-15 was observed *during* `kits-learn-3`, in a working tree that was being edited
between runs and that git does not carry.

---

## 3. Reproduction: the counts

### Before (at this batch's base, `e3f1312`)

```
tests/test_surface.py, isolated, 40 runs   ->  40 x "159 passed, 2 skipped"   0 red
full suite, 10 runs                        ->  10 x "692/693 passed"          0 red
```

(Runs 1-5 at 692 tests; runs 6-10 at 693, having picked up inc24's new test mid-sequence. Neither number
involves the lattice test, which passed in all ten.)

### The per-test audit — the strongest arm

Reading eight `finally` blocks is not a measurement. `prototypes/out/_hh_themes_audit.py` is a pytest
plugin that, **after every single test in the suite**, snapshots the five load-bearing tokens for all
eleven languages and evaluates the lattice assertion:

```
== F-15 AUDIT ==============================================
  tokens watched: ('surface', 'ink', 'dim', 'dot_w', 'gap'), all 11 languages
  tests observed: 695
  colours at session start: 2   at session end: 2
  tests after which a watched token differed from the session baseline: 0
  tests after which the lattice pixel count was NOT 2: 0
============================================================
693 passed, 2 skipped, 700 warnings in 32.18s
```

Seven full suite runs under the audit, identical every time:

```
audit run 2..7 | tests observed: 695 | token drift 0 | not-2 count 0 | 693 passed, 2 skipped
```

**695 x 7 = 4865 evaluations of F-15's assertion at 695 different points in the session. Not one of them
returned anything but 2, and not one test left a watched token mutated.**

### After (this tree)

```
tests/test_surface.py, isolated, 40 runs   ->  40 x "159 passed, 2 skipped"   0 red
full suite, 10 runs                        ->  8 green, 2 red — NEITHER is F-15 (§5)
```

**Grand total: 80 isolation runs, 27 full-suite runs, 4865 in-session evaluations. F-15 did not
reproduce once.**

---

## 4. What changed, and why it is a detector rather than a fix

Nothing was widened. The assertion still says `== 2`.

**The cause is unfindable and the mechanism is knowable, which is exactly when a detector beats a fix.**
§2 proves the only path to a red is a leaked theme token; §2b proves no commit has ever carried one; the
audit proves no test leaks one today. What stood behind "no test leaks one" was a human reading eight
`finally` blocks. That is now asserted.

**`themes_are_restored`**, an autouse fixture in `tests/test_surface.py` — the only file in `tests/` that
writes `THEMES` at all. It snapshots the five tokens before each test and asserts they come back. It
errors **on the leaking test**, not on the distant victim three hundred tests later, which is the shape
F-15 arrived in and the reason it was unattributable.

**Two literal restores closed.** `test_catalogue_postures_refuse_by_name` and
`test_frame_is_a_heavy_box_around_untouched_pixels` both restored `THEMES["nord"]["surface"]` to the typed
literal `"untinted"` rather than to the value they saved. That is correct **only for as long as
`"untinted"` stays nord's declared surface** — and the day it does not, those two tests silently rewrite a
language for every test after them. It is the one place in the repo that could still produce F-15's
symptom, latent rather than active, and it is now `original = THEMES["nord"]["surface"]` on both.

This is not claimed as the cause. It is the only mechanism, and it is closed.

### 4a. The detector, red then green

Green, as the file now stands:

```
$ python -X utf8 -m pytest -q tests/test_surface.py
159 passed, 2 skipped, 4 warnings in 1.66s
```

Red, with a leak planted in exactly the place §4 hardened — `finally: THEMES["nord"]["surface"] = "tint"`:

```
ERROR tests/test_surface.py::test_catalogue_postures_refuse_by_name[phosphor]
E   AssertionError: this test left THEMES mutated, so every test after it ran against a
    language it did not declare:
    {'nord': {'surface': ('untinted', 'tint'), 'ink': ('#eceff4', '#eceff4'),
              'dim': ('#4c566a', '#4c566a'), 'dot_w': (None, None), 'gap': (None, None)}}

FAILED tests/test_surface.py::test_untinted_hands_over_the_source_pixels_unchanged
FAILED tests/test_surface.py::test_chrome_preserves_the_frame_the_shipped_capture_shows[nord]
FAILED tests/test_surface.py::test_check_box_matches_shipped_is_green_for_all_eleven_frames[nord]
3 failed, 156 passed, 2 skipped, 1 error in 1.86s
```

**Read that output as the whole argument for the fixture.** One planted leak, three distant victims, and
the ERROR is the only line that says which test did it and which token moved. Without the fixture a
reader gets three unexplained failures in unrelated postures — F-15's experience exactly. The plant was
reverted and the file re-run at `159 passed, 2 skipped`.

---

## 5. F-18 (NEW) — the two reds in the "after" arm, and neither is F-15

```
after full run  5  rc=1 :: 1 failed, 692 passed  -> tests/test_board_seat.py::
                                                    test_the_next_paint_builds_at_the_new_seat_columns
after full run  9  rc=1 :: 1 failed, 692 passed  -> tests/test_app.py::test_win_clipboard_roundtrip
```

**Run 9 is the documented environment-dependent clipboard test** (PENDING #22, `RUN.md`: "fails if the
clipboard is busy"). Not a finding.

**Run 5 is new, and it is inc23's own F-16 regression test.** Characterised rather than reported:

```
tests/test_board_seat.py ALONE, 40 runs        ->  1 red  (run 32, same assertion)
tests/test_app.py + tests/test_board_seat.py,
  20 runs                                      ->  0 board_seat red
                                                   (1 red, and it is the clipboard test)
full suite, 27 runs this batch                 ->  1 red
```

**It reproduces in isolation**, so it is a timing race, not order- or state-dependence.

**The mechanism, measured.** The failing assertion is `heads(board) == got` at
`tests/test_board_seat.py:205`, and `got` — captured one `pilot.pause()` after the resize — holds **six**
column heads where a board has three:

```
'▐▌ [1]TODO                 [ 3]'      <- the WIDE measure
'▐▌ [2]DOING                [ 3]'
'▐▌ [3]DONE                 [ 3]'
'▐▌ [1]TODO   [ 3]'                    <- the NARROW measure
'▐▌ [2]DOING  [ 3]'
'▐▌ [3]DONE   [ 3]'
```

Both generations of `.col-head` were in the widget tree at once. `narrow()` does a single
`await pilot.pause()`; the rebuild mounts the new heads and has not yet removed the old ones when
`heads(board)` samples the tree.

**It is the TEST's observation point, not inc23's repair**, and the run says so: the three assertions
before it all passed on that same run — `seen` non-empty, `board._built_w == NARROW`, and
`got != wide`. The board had rebuilt at the right seat. Only the sampling caught it mid-swap.

**Not fixed here.** It belongs to `tests/test_board_seat.py`, it is the acceptance test that gated the
previous batch, and changing it needs its own before/after counts — the same discipline this increment
just spent on F-15. Filed as **F-18**. The cure is almost certainly the one `capture_languages.py` already
learned as condition C in `inc20.md`: settle until the tree stops changing, rather than assume one pause.

---

## 6. Test results

```
python -X utf8 -m pytest -q tests/test_surface.py
159 passed, 2 skipped, 4 warnings in 1.81s

python -X utf8 -m pytest -q
693 passed, 2 skipped, 4 warnings          (8 of the 10 "after" runs; §5 names the other two)
```

No test was added or removed — the fixture is autouse machinery, so the count is unmoved at 693.

---

## 7. Risks

- **F-15 is closed WITHOUT a cause.** The honest state is: bounded, detected, not explained. If it ever
  returns, the fixture will name the culprit — unless the mechanism was never a theme leak at all, in
  which case §2's whole argument is wrong and the return will say so.
- **The fixture reports twice on an already-red test.** A test that legitimately fails mid-mutation now
  produces a failure and an error. Noise on a run that is already red, and the second line is the useful
  one; still, someone will read it as two defects.
- **It watches five tokens, not the whole theme.** They are the five §2a proves are load-bearing *for this
  posture*. A leak of `accent` or `layout` passes this fixture and could still redden something else in
  the file.
- **It guards one file.** No other file in `tests/` writes `THEMES` today, and nothing enforces that.
- **The audit plugin is scratch, not suite.** `_hh_themes_audit.py` lives in the gitignored yard and is
  not carried; what is carried is the per-file fixture, which is weaker (it cannot see a leak from another
  file) and cheaper.
- **F-18 is open and its test is green most of the time**, which is the condition under which a flaky
  acceptance test gets re-run until it passes and forgotten. It is recorded with a rate.

## 8. Pending

- **F-18 (new)** — §5. `tests/test_board_seat.py:205` samples the widget tree one `pilot.pause()` after a
  resize and can catch both generations of `.col-head`. 1 red in 40 isolated runs, 1 in 27 full-suite runs.
- **F-8** — `--surface` plain and alone. Run at the batch close, not here.
- **`RUN.md` is stale in two places**: "flake-free since the forty-sixth pass" (F-15 and now F-18 both
  contradict it) and "`verify_language.py` … 2178 checks" against a run that now reports 10857
  (`inc25.md` §7). Neither is this increment's file; both are named.
- **`export_to_skill.py:copy_captures`'s docstring** still describes F-17's symptom in the present tense
  (`inc24.md` §6).

## 9. Suggested next task

**F-18**, with the same shape this increment used: reproduce, count, fix the observation point rather than
the tolerance, count again.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `tests/test_surface.py`: `159 passed, 2 skipped` (§4a). Full
      suite: `693 passed, 2 skipped` in 8 of 10 "after" runs; the other two are named, characterised and
      neither is this increment's (§5). The detector is red-then-green against a planted leak (§4a).
- [x] **No secrets in code or output** — one autouse fixture and two save-and-restore lines in a test
      file. No path, no network, no dependency, no new I/O.
- [x] **No destructive commands run without approval** — no `rm` outside the gitignored scratch yard's own
      per-run logs, no force, no terminal process killed. The planted leak was written to
      `tests/test_surface.py` and reverted from a copy taken immediately before (§4a), verified by
      re-running the file green.
- [x] **File count within cap** — 1 source file, plus this packet: 2.
- [x] **Review packet attached** — this document.

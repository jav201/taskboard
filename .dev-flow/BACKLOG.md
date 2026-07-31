# BACKLOG — taskboard (canonical, cross-batch)

Shared by `/dev-flow` and `/fast-dev-flow`. Every open item lives here exactly once.
No `docs/engineering-rules.md` exists in this repo, so this is the default location.

**Base ref:** `b3cc60d` (main) · **Last refresh:** 2026-07-30
**Status:** the Prism roadmap (PROPOSAL.md §9, rows 1-6) is COMPLETE — seven commits,
`a06a635`..`0b635e3`, none pushed. 226 tests green.

## Shipped

- **DONE** · Prism increment 1 — the colour ration: four colliding project hues
  retired (amber 0.0 / cyan 48.3 / orange 51.0 / rose 63.8 from a reserved hue),
  deterministic injective remap on load, high-priority marker moved from the amber
  `◉` to the neutral glyph `!`. 15 new tests, 152 green, 4 mutants killed.
  (`a06a635` — see `.fast-dev-flow/spec.md`)
- **DONE** · Prism increment 2 — `taskboard/wave.py`: the REV2 dot engine ported
  as a pure, view-independent module (2x4 dots per cell, braille packed last,
  carve/notch, 4x7 font). Behaviour verified identical to the proposal's module
  over 400 randomized differential trials. 16 new tests, 168 green, 4 mutants
  killed. **No view imports it yet — that is increment 3/4.** (this batch)
- **DONE** · R5 (render cost of the field) — **measured**, no optimisation done:
  at 96x30 with the proposal's L-step geometry (68-day window, leader bench 10
  rows), the engine costs **1.37 ms (calm) / 1.84 ms (typical) / 2.24 ms
  (extreme)** per frame for 748 / 952 / 1156 braille cells. Against increment 6's
  700 ms ambient tick that is 0.3 %. Engine only — markup, styling and Textual
  compositing are NOT in these numbers, so the view's real cost is still unmeasured.

- **DONE** · Prism increment 3 (roadmap row 2) — the shared day axis + field
  lattice as pure helpers (`field_geometry`, `day_col`, `off_window_glyph`,
  `field_rows`); the clip/flag vocabulary finally gets a MARK. 14 tests,
  182 green, 4 mutants killed. (`d3061e4`)
- **DONE** · Prism increment 4 (roadmap row 3) — the new lanes row replaces the
  two per project; scale row; nav follows what is drawn. 18 tests, 202 green,
  5 mutants killed. (`f433e19`)
- **DONE** · Prism increment 5 (roadmap row 4) — pressure ranking, leader's
  bench with its carved count and `◆`, resting row, height allocator, "+N not
  shown". 25 tests, 207 green, 5 mutants killed — **three of which were vacuous
  on the first run and were fixed**. (`f3509ea`)
- **DONE** · Prism increment 6 (roadmap row 5) — momentum: `Task.phase_changed`,
  `Board.set_task_phase`, `days_in_phase` (None = unknown, never zero), the
  lead's `Nd in phase · N unaged` figure. 13 tests, 219 green, 4 mutants killed.
  (`e9f36be`)
- **DONE** · Prism increment 7 (roadmap row 6) — the ambient: the today rule
  rotates through 4 glyphs on the app's one shared clock; nothing else moves and
  no colour changes. 7 tests, 226 green, 4 mutants killed. (`0b635e3`)

## Open — Prism roadmap

**Nothing.** Rows 1-6 of `_tui_prism_proposal/PROPOSAL.md` §9 are all shipped.

## Open — findings raised while shipping increment 1

- **`ribbon.py:49` paints the ISO week number in `amber` (#fbbf24)** — the reserved
  *due today* hue worn by a mark that is neither identity nor severity. Same class
  of collision the ration just fixed, one file away. Small, self-contained.
- **`views.py:177` paints the image indicator `▤` in `sky`** — `sky` is an
  *identity* hue (a project colour), so a task attribute is wearing the house that
  names projects. Decide: move it to a neutral tone, or accept and document.
- **The `!` marker is per-card only.** The proposal's `!N` aggregate (count of
  high-priority open tasks per project) belongs to the new lanes row — increment 3.
- **Columns / agenda / gantt render no priority at all.** Not a regression (they
  never did), but if priority matters at a glance, three of five views omit it.
- **`sky` survives the ration by 7.4 units** (62.4 vs the 55 accent band). If
  `accent` #2dd4bf is ever retuned, re-run the oracle in `tests/test_palette_ration.py`.
- **`modals.py:322-324` would raise `InvalidSelectValueError`** if an in-memory
  `Project` ever carried a retired hue (only reachable by constructing `Project`
  directly in code — the loader always returns a lawful hue). Left unguarded on
  purpose; revisit if any code path starts building projects from raw data.
- **`.venv` cannot run the suite** — `ModuleNotFoundError: No module named 'PIL'`
  makes 5 image tests error there; the suite is green under system python. Either
  install Pillow into `.venv` or mark those tests as requiring it.

## Open — findings raised while porting the wave engine (increment 2)

- ~~`taskboard/wave.py` is imported by nothing but its tests.~~ **RETIRED** —
  `views.field_rows` draws with it as of increment 3.
- **`field_geometry` does not fit below 32 columns** (increment 3, measured and
  pinned by `test_the_ported_geometry_does_not_fit_below_32_columns`): `field_w`
  has a floor of 8, so at 24-31 columns label + field + figures exceed the width
  by 32-w cells. Inherited from the proposal's `Geo`; harmless while no view
  calls it, and it must be resolved by whoever wires the lanes row at MIN_WIDTH.
- **The proposal's §4.1 budget table says the L step shows a "68-day window";
  the code shows 134 days** (67 field cells x 2 days per cell). The table counts
  cells, the code counts days. Code governs; the table is wrong.
- **`carve_text` carries prototype-grade edges, kept for port fidelity:** its
  returned width includes the trailing inter-glyph gap (`"40"` -> 10, not 9), the
  loop index `i` is unused, and the returned height is the constant 7 rather than
  the glyph's real extent. Behavioural changes, so they were NOT "cleaned" —
  decide deliberately when a caller exists.
- **The engine has no clip/flag vocabulary of its own.** `verify_prism.py` law 12
  ("a date beyond the window is FLAGGED, not clamped") lives in the prototype's
  `Geo`, not in `wave.py`; increment 2's helpers must carry that, not the engine.

- **DONE** · The occupancy harness — `tests/test_occupancy.py` measures the
  rebuilt lanes view by AUDIT.md's own method at its own reference size and
  compares against its numbers. 11 laws, 235 green, 3 mutants killed.

- **DONE** · The world-city catalog — `CITY_ZONES` 75 -> 340 cities / 243 zones,
  all 40 UTC offsets in use covered, every zone resolved through `zoneinfo` by
  the test suite; `resolve_city` is accent-blind on a fallback. 14 laws + 1 app
  test, 250 green, 5 mutants killed. (`9ed055b`)
- **DONE** · Gantt ordering + auto-archive — open work first, done work at the
  tail; `AUTO_ARCHIVE_DAYS = 20` sweeps long-finished work into the existing
  `archived` flag at startup, but only when the completion date is KNOWN.
  16 laws, 266 green, 5 mutants killed. (`db31a5c`)

- **DONE** · The key-bar contract — `taskboard/keymap.py` is the one seat;
  `BINDINGS` and the bar are both generated from it. Replaced Textual's `Footer`,
  which mounted zero children and painted a BLANK row while 24 bindings were
  live. 17 laws, 283 green, 6 mutants killed. (`68e85b4`)

- **DONE** · REV5 #17 columns retirement (`17c705b`) · #18 lanes due meter
  (`c3ff23d`) · #19 gantt meter + field titles (`52349ff`) · #20 agenda laws
  (`889e812`) · #21 the `?` legend (`0259948`). 320 green.
- ~~Until a legend key exists, `+N` is the fallback below ~50 columns.~~
  **CLOSED** — `?` ships declared `universal=True`.

- **DONE** · REV5 #22 — the 17 prototype laws reconciled into the suite under a
  disk-checked MANIFEST; attribution and register ported; the register law found
  a real second-person string in the app's voice. (`90a7f4f`)
- **DONE** · The gantt FIELD redesign (REV3) — two bands, the slip as a length,
  an axis with a past. **Carrying 71.4 % at typical (target 71.1 %) and ink now
  MONOTONE: 25.0 % -> 25.9 % typical to extreme, where the old view inverted
  23.3 % -> 21.0 %.** Chrome 21.2 % -> 7.8 %. (`c17dded`)
- ~~The gantt's field redesign is not done.~~ **CLOSED** by `c17dded`.

## Open — raised by the gantt field redesign

- **The closure law stays red** (`test_the_closure_law_is_knowingly_unmet`): all
  four views still draw a box. The gantt's chrome fell from 21.2 % to 7.8 % by
  removing the divider rows, so what remains IS the frame. Removing it is now
  the single largest occupancy win left in the app.
- **`calm` gantt is 67.8 % dead.** The two-band field needs data to fill; a
  near-empty board has little to draw. Same honest weakness the proposal records
  for calm lanes.
- **The gantt sheds rows at short heights** and counts them (`+N not shown`),
  which the old view did not do — it simply drew fewer. Consistent with lanes
  now, but it is a behaviour change worth knowing.

## Open — raised by the REV5 roadmap

- **REV5 #22 (the 90 laws ported to `tests/`) was NOT attempted** — it was not
  in the approved list.
- **The gantt's field redesign is not done.** #19 ported the RULING (meter at the
  edge, titles over the field, one severity seat) onto the existing week-grid
  gantt. The frames show a lanes-style dot field with compact marks near each due
  date; that is a separate redesign and is not claimed.
- **The proposal's title targets did not transfer**, in three views: its numbers
  (lanes 77→83, gantt 11→33, agenda 12→19) describe a prototype whose titles were
  boxed inside a label column. Measured here BEFORE the pass: lanes 83-85,
  agenda 30, gantt 27. The freed width in lanes went to the FIELD (+6 L / +4 S)
  instead, and gantt titles now grow +6 per empty week in front of their bar.
- **Task rows in lanes lost 2 cells** to the meter (6 cells vs the `+12d` token's
  4) — the trade the proposal names explicitly.
- **At narrow gantt widths the percent drops and the meter stays** — a drop-order
  the proposal legislates only for the wide case.
- **The agenda's ink ceiling is nowhere near breached** (38.3 % vs 85 %), so the
  designed half-density reach lattice is deliberately NOT applied. Pinned by law
  so a future widening cannot cross it silently.

## Open — raised by the key-bar contract

- **REV5's remaining items are NOT started, by instruction**, pending Javier's
  review of the prototype: the `?` legend popup, the columns retirement, the
  meters, the title widths.
- **Until a legend key exists, `+N` is the fallback below ~50 columns.** Once `?`
  ships it must be declared `universal=True` so it sorts beside `q` and can never
  be the key that drops — the seat already supports it.
- **`o` (URL) and `i` (Images) are shown always but do nothing unless the
  selected task has one.** That is "live but a no-op", not a dead key, and
  hiding them would violate the standing instruction not to hide keys — but if
  the contract is ever tightened to per-selection state, they are the two
  entries that need a rule.

## Open — raised by the archive increment

- **Auto-archive does nothing on Javier's existing board, by design.** Every
  finished task there predates `phase_changed`, so its age is unknown and it is
  left alone (measured: a 30-done legacy board sweeps 0). If he wants the old
  ones gone he must archive them by hand (`x`) — or we add an explicit,
  opt-in "treat everything done before <date> as archived" action, which would
  be a deliberate one-time decision rather than a guess.
- **Reordering phases can make a task "done" while carrying an older stamp**, so
  the next start may sweep it. It cannot touch a legacy board (no stamp), but if
  phase reordering becomes common, consider re-stamping on `move_phase`.
- **The sweep runs only at startup.** A long-running widget will not archive work
  that ages past 20 days while it is open, until the next launch.

## Open — raised by the occupancy measurement

- **PROPOSAL §4.3's ">= 45 % marked at typical/extreme" is met at typical
  (45.4 %) and MISSED at extreme (44.7 %)** — by 0.3 points. Pinned by
  `test_the_proposals_own_45_percent_floor_is_met_at_typical_and_missed_at_extreme`
  so it cannot quietly widen. The frame alone costs ~7.6 %; removing it would
  clear the floor at both loads.
- **"Wider is worse" is reduced, not cured.** Stepping 72x24 -> 96x30 still adds
  dead space at typical (+1.3 points) and extreme (+11.1), against the old
  view's +10.9 and +15.9. Cause: named-task rows are short strings that gain only
  blanks as the widget widens, while the field is what spends width. A calm board
  now INVERTS (it gets better as it widens). Fix candidate: let a title row carry
  something on its right at wide sizes, or give the lead more bench rows instead
  of more titles.

## Open — raised while finishing the roadmap (increments 4-7)

- **The box frame and the `◆ TASKBOARD` header survive**, so PRISM's measured
  "0 % chrome" is NOT reached. The roadmap allocates no increment to the frame,
  so it was not mine to remove. Decide deliberately: the frame is ~2 columns and
  2 rows of every render.
- **The proposal's open items, untouched by design** (they are not roadmap rows):
  the Inbox is drawn as an ordinary lane rather than designed (R6 — it works, it
  just was never designed); only two size steps exist (S/L); and `calm` boards
  still leave a lot of empty field. Recorded, not solved.
- **The 21 laws of `verify_prism.py` were adapted, not ported wholesale.** Laws
  that measure the PROTOTYPE's composed frame (occupancy floors, tone histogram,
  ink percentages) have no meaning against the real app's framed render, so the
  laws about mechanism (resolution, carving, attribution, ordered coverage,
  clip-and-flag, motion) were reproduced in `tests/` and the frame-occupancy
  ones were not. A real occupancy harness for the app is still missing.
- ~~**`progress_bar`, `sparkline` and `_lane_junctions` are now unused**~~
  DONE: `_lane_junctions` had already died with the lanes rewrite; `progress_bar`,
  `sparkline` and `_SPARK` deleted (zero callers, zero test references, verified
  by grep). The README's view-2 line promised "throughput sparklines" that no
  code drew — corrected in the same commit.
- **The gantt's own `_flowing` animation and the lanes ambient now share one
  clock**, so a future change to `TICK_SECONDS` moves both. The motion laws read
  the constant, so the illegal-band failure will be caught, but the gantt's
  speed is not pinned by any test.
- **`sitting()` reports the lead only.** Every other lane's momentum is computed
  (`days_in_phase`) but not shown; a drawn stagnation channel remains open, and
  it now has data to draw from.

## Housekeeping

- Untracked in the working tree, pre-existing and NOT part of this batch:
  `_tui_prism_proposal/` (a concurrent design agent owns it), `.claude/`, `.s19tool/`.
  Decide what to commit / ignore.

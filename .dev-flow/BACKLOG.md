# BACKLOG — taskboard (canonical, cross-batch)

Shared by `/dev-flow` and `/fast-dev-flow`. Every open item lives here exactly once.
No `docs/engineering-rules.md` exists in this repo, so this is the default location.

**Base ref:** `eec625b` (origin/main) · **Last refresh:** 2026-07-31 (batch-02 open)
**Status:** the Prism roadmap is complete and SHIPPED; the frame is gone, the report
batch (`2026-07-31-batch-02`) is in flight under `/fast-dev-flow`. 345 tests green.

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

- **DONE** · The frame removed — the closure law is GREEN and chrome is 0.0 % in
  lanes and gantt. Marked +2.5 points at typical and extreme (the extreme margin
  over the 45 % floor went 2.4 -> 4.9). (this batch)
- ~~The closure law stays red.~~ **CLOSED.**

- **DONE** · The deliberate one-time archive (`X`) + archive from the task
  editor. Closes the "auto-archive does nothing on Javier's board" carry-over:
  the timer owns dated work, `X` owns everything older, and neither invents a
  date. 12 laws, 343 green, 6 mutants killed. (this batch)
- ~~Auto-archive does nothing on Javier's existing board, by design... he must
  archive them by hand — or we add an explicit, opt-in one-time action.~~
  **CLOSED**: that action is `X`.

- **DONE** · The board report (batch `2026-07-31-batch-02`) — self-contained HTML,
  whole board or one project, `R` in the app and `taskboard --report [PROJECT]`.
  Read-only by law. 18 laws, 363 green, 8 mutants killed. (this batch)

## Open — raised by the report batch

- **Increment 22b (REV6's spend ladder) is APPROVED AND QUEUED** — the allocator
  prohibition, the lattice behind title rows, the absence line. The prototype's
  `law_spend` is already in `verify_prism.py` and is recorded QUEUED in the
  prism-laws manifest. REV6 also carries its own open defect to check for in the
  app: extreme sat 0.5pt below typical in marked cells (an ink-monotone violation).
- **The report has no `--format svg`.** Struck deliberately in the spec (an SVG
  container cannot reflow); if a single pasteable figure is ever wanted, it is a
  small follow-on, not a redesign.
- **The report is not linked from the app's legend.** `?` explains marks in the
  views; it says nothing about `R`. Minor, and arguably correct — the legend is
  about marks, not actions.

## Open — process / operator actions

- **`/dev-flow-sync` was never run for batch `2026-07-18-batch-01`.** That batch is
  now explicitly CLOSED in `state.json` (its work merged and shipped on 2026-07-18);
  the only unfinished step is uploading its artifacts to the Obsidian vault.
  **This one is Javier's to run** — it writes to his vault, which is outside this
  repo and not an agent's call. Until then the batch's artifacts live only in
  `.dev-flow/`.

## Open — raised by the report batch's Phase 0 (measured)

- **The 8 project hues fail as a CATEGORICAL palette — identity-vs-identity was
  never measured.** The colour ration checked every identity hue against the hues
  that JUDGE (>=70 from over/soon, >=55 from accent) and never checked the identity
  hues against EACH OTHER. Run through `dataviz/scripts/validate_palette.js` on
  both the dark surface (`#0d1117`) and light:
  - `fuchsia #e879f9` vs `violet #a78bfa` — **dE 0.4 for protanopia**: identical to
    a red-blind reader.
  - `violet #a78bfa` vs `indigo #818cf8` — **dE 5.4 normal vision**, against a floor
    of 15: hard to tell apart *with full colour vision*.
  In the TUI this is survivable (a project is also its row, its spine and its name),
  which is why it never surfaced. It would NOT be survivable in a chart that encodes
  a project by hue alone — hence the report's design rule (direct labels + a table
  view, never hue-alone). **Fixing the palette itself is a separate decision**: it
  means re-stepping two of the eight hues and remapping existing boards, exactly the
  cost the original ration paid.

## Open — raised by the one-time archive

- **`x` cannot undo itself from the board.** Archiving hides the task, so the
  selection moves on; bringing it back is `v` then `x`. Correct but two-step,
  and now the confirm text says so explicitly. If it trips people up, an undo
  toast on the archive notification is the small fix.
- **The purge is board-wide.** There is no per-project variant; `P` archives a
  whole project but not "this project's finished work". Nobody has asked.

## Open — raised by removing the frame

- **Most of the reclaimed 7.6 % became DEAD, not marked.** The frame was on the
  perimeter: the content gained two columns (~0.5 points) and the spent bottom
  row gave +2.5, but the rest is blank space nothing has been designed to use.
  It is available headroom, measured and unspent.
- **Box-drawing survives in two places, deliberately**: kanban's phase-column
  dividers (chrome 4.4 %) and the agenda's "no date" section rule (7.3 %). They
  are internal structure — they say WHICH column and WHICH group — not an
  enclosure. Whether the closure law should eventually reach them is a design
  question, not an oversight.
- **`calm` is now 65.5 % dead in lanes and 74.8 % in gantt.** Removing the frame
  raised both, since a quiet board has nothing to put in the reclaimed cells.
  Same honest weakness the proposal records for calm.

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

## From increment 22b — the REV6 spend ladder

- **A mutation battery can poison `__pycache__`.** M6 mutated `range(0, 4)` to
  `range(0, 1)` — the SAME number of bytes — and the restore landed inside the
  same second. Python keys a `.pyc` on (source mtime, source size), so both
  matched and the cache survived: the next full-suite run executed the MUTANT
  from a byte-identical working tree, 13 tests failing with no diff to explain
  them. The hash-verified restore is not sufficient on its own; the batteries
  must run with `PYTHONDONTWRITEBYTECODE=1`. Batteries live in `%TEMP%` and are
  rewritten per increment, so this is a habit to keep, not a file to fix.
- **A clause is not a signature.** `test_the_absence_line_yields_when_rows_were_shed`
  asserted `"nothing late" not in out`, but the shed fixture HAS late work, so
  the line reads "12 late" and the assertion held whether or not the line was
  drawn. Fixed to match the line's own shape. When asserting a thing is ABSENT,
  assert on text the thing always emits — not on the branch the fixture avoids.
- **`calm` misses REV6's dead-space number: 55.1 % here vs 50.9 % reported.**
  Typical (19.2 % vs 25 % ceiling) and extreme (ink-monotone) both hold, so the
  increment is accepted, but a nearly-empty board still spends more of the
  screen on blank than the design says it should. The third rung buys one row;
  the calm case has more than one row to spend.

## From the closure batch (increments 1-4)

- **`sitting()` beyond the lead: STOPPED, not implemented.** The data exists for
  every lane (`days_in_phase`), but there is nowhere lawful to put the figure. A
  stack row's free gap is **exactly 1 cell at every width measured** (60, 80, 96,
  120, 160) — the geometry expands the field to fill whatever the label and the
  meter leave, so `12d in phase` cannot be drawn without taking ~13 cells from
  the field of every project, permanently. Printing it INSIDE the field is worse
  than clutter: the field is a shared day axis, so a figure sitting at column X
  reads as belonging to that DATE.
  And the app's own order of loss already answers the question. `lead_band` sheds
  its right-hand block from the left and momentum goes FIRST, because "it is
  context" — on a row with strictly less room than the lead's, momentum is
  precisely the figure that does not survive. Drawing it anyway would need either
  a permanent field-width tax on every project or a new mark, and both are design
  decisions for the owner rather than defects to fix.
  **Open question if it is ever wanted:** is stagnation worth ~13 cells of every
  stack lane's curve? If yes, the honest form is the lead's existing figure in the
  lead's existing tone, and the field shrinks for everyone.

- **The identity-vs-identity collision is NOT curable at 8 hues.** Measured with
  the dataviz validator, `--pairs all`, both modes: the shipped palette fails
  three checks (violet↔blue ΔE 0.3 deutan; normal-vision floor 5.4 against a
  floor of 15). No subset of the current family passes at ANY size down to 5,
  because `Lightness band` fails listing all eight — the Tailwind-400 family is a
  tonal step too light for the surface, and it is crowded into the cool half of
  the wheel exactly because the ration reserved the warm half for severity.
  Searching a lawful pool (reference-theme slots outside the reserved bands), the
  ceiling for `--pairs all` in both modes is **four** hues. Even the dataviz
  reference theme fails all-pairs at 8 — its own docs claim only the *adjacent*
  pairlist — and 3 of its 8 slots sit inside the app's reserved bands.
  Mitigating fact: colour is NOT the sole identity channel here. Every project is
  named in text beside its bar, which is the secondary encoding the palette rules
  ask for. The failure is real but it is "two projects can share a colour", not
  "the board is unreadable".
  **DECIDED 2026-07-31 — Option A accepted by Javier ("Acepto la opción A"): the 8
  shipped hues stay.** The standing conditions of the acceptance: text remains a
  mandatory identity channel beside every hue-bearing mark (already law in the
  report: no figure encodes a project by hue alone), and this item is CLOSED — do
  not reopen the palette unless the hue family itself changes, at which point the
  all-pairs measurement above is the gate to re-run.

- **Two process findings, both from mutants that stayed green.** A test asserting
  a thing is ABSENT must assert on text the thing ALWAYS emits — `"nothing late"`
  passed whether or not the absence line was drawn, because the fixture had late
  work. And a motion test must use a fixture long enough to observe speed: over a
  two-cell reach, a packet stepping 3 and one stepping 1 are the same animation
  (3t mod 2 == t mod 2), so the first version of the gantt-speed law could not
  have failed.

- **`.gitignore` near-miss.** Rewriting it instead of appending dropped
  `board.json` — the rule that keeps a local copy of the real board out of the
  repo. Caught by diffing before the commit. Rewriting a tracked file without
  reading it first is the whole error; there is no second control that would have
  caught it.

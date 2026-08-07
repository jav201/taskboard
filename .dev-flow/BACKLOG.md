# BACKLOG — taskboard (canonical, cross-batch)

Shared by `/dev-flow` and `/fast-dev-flow`. Every open item lives here exactly once.
No `docs/engineering-rules.md` exists in this repo, so this is the default location.

**Base ref:** `5057c6a` (local HEAD; `origin/main` == `caa4bab`, **5 commits behind**)
· **Last refresh:** 2026-08-07
**Status:** **767 tests green** on `main`, with `kanban-variants` MERGED
(`ecde0da`) and a pre-commit privacy gate wired. Nothing pushed — the operator
pushes.

## Open — after `2026-08-07-fastflow-06`

- **`main`'s HISTORY still carries board data, and this is now an ACCEPTED
  RISK, not a task.** Operator ruling 2026-08-07: *"el main, ni hablar"* — no
  rewrite, no force-push. Two project names and one task title sit in
  `.fast-dev-flow/archive/20260724-025459-spec.md` in every commit from
  `5ae4d42` back-to-front, on a **PUBLIC** remote. The tips are clean and the
  pre-commit gate stops new ones. Re-open only if the operator changes the
  ruling.
- **The global git identity still carries the address.** Repo-local is set
  (`46639531+jav201@users.noreply.github.com`, verified on `5057c6a`); the
  global remains `jjgh89@msn.com`, deliberately untouched — changing it retags
  every repository on the machine, including ones whose remotes may require a
  verified address. One line when wanted:
  `git config --global user.email "46639531+jav201@users.noreply.github.com"`
- **The gate is local only.** `--no-verify` bypasses it, as it bypasses every
  hook, and a fresh clone must run `git config core.hooksPath .githooks` (a test
  says so rather than leaving it silent). A server-side or CI equivalent was NOT
  built.
- **`prototypes/` and `_prototypes/` now co-exist** on `main` after the merge.
  Not a defect, but two directories with the same purpose and different
  vintages is a decision waiting to be made.
- **8 more app symbols are still imported by `prototypes/kanban_variants.py`**
  (`HEX`, `blank_line`, `bottom`, `fill_height`, `fit`, `header`, `line`,
  `phase_buckets`, …). Two of them broke on this merge and became local copies;
  the rest are the same exposure, unbroken so far.
- **A stale worktree registration `clipboard-fix`** could not be pruned by
  `git gc` (permission denied on `.git/worktrees/clipboard-fix`). Harmless,
  cosmetic, and it will keep printing an error on every gc.
- **`docs/sample/report-example.html` is clear but ungoverned** — synthetic
  today, with no law tying it to a fixture. `taskboard/report.py` is the writer
  to watch.

## Superseded — the privacy work as it stood before the merge

- **`main`'s HISTORY still carries the operator's board data.** `caa4bab` and
  `ff733ec` are clean and `6083c01` is clean, but `694f38a` and every commit
  back to `5ae4d42` (2026-07-24) still contain **two project names and one task
  title** from the operator's board in
  `.fast-dev-flow/archive/20260724-025459-spec.md` — not quoted here, because
  AC6 forbids this file from carrying them and writing this entry tripped that
  law on its first draft. Run the sweep to see them. **This remote is PUBLIC.**
  `git log -S` finds them in 6 commits. Excising them needs a history rewrite
  and a force-push — the operator's call, and GitHub retains unreachable
  objects for a while afterwards, so forks and caches are not covered by it
  either. **Verified by `tools/privacy_sweep.py` over every commit in
  `7de3ad6..caa4bab`.**
- **`kanban-variants` is NOT merged, deliberately.** Attempted and aborted:
  **80 files / 44 132 insertions**, 4 conflicts, and it would create
  `prototypes/` alongside the existing `_prototypes/` while resurrecting the
  inline `HelpScreen` that `taskboard/keymap.py` replaced. The operator ruled
  against merging on 2026-08-07 and the measured scope confirms it. **The
  portable part — the detector — was cherry-picked instead** (`6083c01`). If
  anything else from that branch is wanted, it is a cherry-pick, not a merge.
- **The operator's name and address remain in every commit's AUTHOR metadata.**
  Accepted by the operator for existing commits; he asked that it not appear
  going forward. That is a git identity change (a GitHub `users.noreply`
  address), **operator-level config, not a repo change — NOT DONE HERE.**
- **`docs/sample/report-example.html` was cleared, not fixed.** It is synthetic
  (fixture vocabulary, 0 verbatim matches) but there is no law tying it to a
  fixture, so a regenerated sample could quietly come from the live board.
  `taskboard/report.py` is the writer to watch.
- **The sweep is a command, not a gate.** Nothing runs `tools/privacy_sweep.py`
  against the real board automatically, by design — but that means a leak is
  caught only when someone runs it. A pre-commit hook is the obvious next step
  and was NOT built.

> **The header sat at `eec625b` / 2026-07-31 for a whole day of shipping.** The
> close step that owns this line did not run when batch-02 closed, which is the
> failure the carry-over contract exists to prevent, and it is now the second
> recorded instance (the first: 2026-07-20 operator audit, ~10 batches stale).
> Nine commits are reconciled below at once; a backlog read between those dates
> would have reported an empty queue that looked like "nothing pending".

## Shipped

- **DONE** · `2026-08-07-fastflow-06` — **the branch lands and the gate goes
  up.** `kanban-variants` merged (80 files / 44 132 insertions, 4 conflicts each
  resolved toward `main` with a stated reason); a **pre-commit hook** that reads
  the INDEX, refuses a commit carrying board data, and **fails closed** when it
  cannot read the board; the repo-local author address moved to GitHub
  `users.noreply`; and the four backup refs deleted after the merge was green,
  verified by object id — the 19 077-byte blob holding 25 real task titles no
  longer exists locally. **767 green.** (`ecde0da`…`5057c6a`, local — **not
  pushed**)
  · *The merge's real cost was NOT in the conflicts: git auto-merged into 31
  failures. The worst was invisible in any diff —
  `prototypes/kanban_variants.py` monkeypatched `views.render_kanban` AT IMPORT
  TIME, so importing a prototype rewrote a shipping function for the whole
  process (22 unrelated failures, green in isolation). The auto-merge had also
  taken the branch's `m` binding into five of main's modal tests while the app
  binds `P`.*

- **DONE** · `2026-08-07-fastflow-05` — **the live board becomes unreachable
  from anything committable.** `tools/privacy_sweep.py` + 8 tests, matching
  truncated forms down to a stated 10-char floor because the failure that
  happened was a name reaching a file ONE LETTER short through an ellipsising
  label column — a first hand scrub replaced the whole token and called six
  rewritten commits clean while all six still carried it. Tested against a
  planted leak in both directions, 7 mutations all killing. Executed: main's
  tracked tree 99 files / 0 leaking. `tests/test_requirements.py` widened
  (hand-written first-party tuple → discovery; `tools/` had been outside its
  sweep entirely). **739 green.** (`6083c01`, local — **not pushed**)
  · *Three defects the flow caught that the hand work had not: the truncated
  residue in 6 commits; the batch's own spec quoting a real task title; and
  the detector's own test file using three real project names as fixture
  constants — invisible to its first sweep because the file was still
  untracked. Two of the batch's own tests were vacuous on their first mutation
  run (`board_strings` sort order, and `git check-ignore` answering from the
  INDEX so every `.gitignore` negation went untested).*
  · *Branch-side work — capture scripts, the widget constructor, the scratch
  `.gitignore` — landed on `kanban-variants` (`f5f0e81`, 164 green), which is
  NOT merged; see above.*

- **DONE** · `2026-08-06-fastflow-04` — **the gantt gets its gauge.** The three
  parts of the approved prototype that never shipped when its texture did
  (`81dcb66`): a 2-cell `GUTTER` so a truncated title stops touching its own bar
  (measured 0 cells of separation on 5 of 5 long-title rows at 104x30 / 102x16 /
  96x30 / 120x40, now >= 2 at all four); a **week guide** `┆` at every monday
  column and **month names** on the bottom axis beside the day figures; and
  `FIELD_REACH` `█` -> `━`, so a project span is a rule instead of a slab.
  Occupancy improved (`dead` 23.1 -> 21.5 %, `marked` 76.9 -> 78.5 %, chrome
  still 0.0); span economy 135 -> 155 runs against a 594.7 ceiling. 5 new tests,
  **730 green**, 9 mutations each verified to redden their predicate.
  (local commit — **not pushed**; see `.fast-dev-flow/spec.md`)

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
  editor. Closes the "auto-archive does nothing on the operator's board" carry-over:
  the timer owns dated work, `X` owns everything older, and neither invents a
  date. 12 laws, 343 green, 6 mutants killed. (this batch)
- ~~Auto-archive does nothing on the operator's existing board, by design... he must
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

- **DONE** · **`/dev-flow-sync` for batch `2026-07-18-batch-01`** — run 2026-07-31 on
  the operator's authorization, 13 days after the batch closed. The four phase artifacts
  plus `06-docs/` (9 files) are now in the vault at
  `G:\My Drive\ConsultIA\Obsidian_Vaults\AI-Consulting-Brain\01 - Proyectos\taskboard\dev-flow-batches\2026-07-18-batch-01\`,
  with a frontmatter-carrying `2026-07-18-batch-01-README.md` index and a project
  `Dashboard.md`. This created the vault's `taskboard` project folder — it had none.
  `03-increments/` deliberately not synced (vault convention since batch-04), so the
  increment records remain repo-only. Folder named from the artifacts' own
  self-identification, NOT `state.json`'s `batch_id` — see the state.json note below.

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

- **REV5's remaining items are NOT started, by instruction**, pending the operator's
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

- **Auto-archive does nothing on the operator's existing board, by design.** Every
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

## Open — raised by the gantt gauge batch (`2026-08-06-fastflow-04`)

- **The week guide is dense, and its rhythm is irregular.** One cell is two days,
  so a week is 3.5 cells and the guides alternate 3 and 4 cells apart:
  `·┆···┆··┆···┆··┆`. It reads closer to texture than to a ruled gauge. It is the
  approved prototype's own density and it SHIPPED as approved — but if the operator
  reads it as noise, the cheap levers are a guide every fortnight, or guides only
  at month boundaries. **Decide with the render in front of you, not from this
  line.**
- **`AUG` is dropped from the axis whenever the month starts within ~3 cells of
  today.** The day figures are the anchors and a month that cannot stand clear is
  dropped whole (a half-printed month is a wrong date). At `TODAY = 2026-07-30`
  the axis reads `-48d  JUL  today  SEP  OCT  NOV +111d` — the month immediately
  ahead is the one you cannot see. Options if it matters: let the month win over
  `today` (it has the today RULE in the field already), or shorten the day
  figures.
- **`NOV +111d` sits with a single space between them** at 104 wide. The
  one-blank-either-side rule held, but it is tight; consider two.
- **`tests/test_gantt.py:121` is dead code** — `set(seg) <= {"⣿","⣤","⡄","⣀"," "}`
  tests the braille alphabet the field stopped using two batches ago, so the loop
  body never executes. Found while mapping the laws; NOT fixed here (out of
  scope). Same class: `tests/test_app.py:1542` (`assert "⣤" not in …`, trivially
  true).
- **`tests/test_app.py::test_win_clipboard_roundtrip` is flaky, not broken.** It
  failed on the first baseline run of this session (`Set-Clipboard` with no
  clipboard in a non-interactive shell) and passed on every run after. Worth a
  skip-marker when there is no clipboard, so a baseline count stops depending on
  which shell ran it.

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
  **DECIDED 2026-07-31 — Option A accepted by the operator ("Acepto la opción A"): the 8
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

## From the 2026-08-03 session

Nine commits, `a16608b`..`bd935ff`, all on `main` and pushed. Reconciled in one
pass because the header had gone a day stale (see the note at the top).

### Shipped

- **DONE** · **Run economy.** The board coloured cell by cell, so a 60-cell band
  left 60 `[#hex]…[/]` pairs. `Text.from_markup` was **88 % of render time**.
  `collapse_runs` + `to_text` as the one seam: gantt **139 ms → 0.3 ms** net per
  keypress, 2,880 → 302 segments, idle tick 4.9 % → 1.1 % of a core. Verified on
  the real board across 256 configurations, 0 mismatches. (`a16608b`)
- **DONE** · **Width is measured in cells.** `fit`/`clip`/`header`/`_pad` and ten
  callers used `len()` — codepoints, not cells. A title holding `:bug:` made its
  row 93 cells in a 96-cell view. `vis()` is now the only ruler; `set_cell_size`
  cuts on glyph boundaries. `emoji=False` is load-bearing (see the law below).
  New `tests/test_cells.py`, 213 cases, failed 136× against the old arithmetic.
  (`6ddc574`)
- **DONE** · **Ctrl+E emoji picker** in both text editors, inserting the glyph.
  (`efe6060`)
- **DONE** · **Tests stop reading the developer's live board.** `TaskboardApp()`
  with no path loads `~/.taskboard` and `on_mount` SAVES it. (`38ce312`)
- **DONE** · **The kanban rule crosses where the columns divide.** Headers split
  at 30/60/90, the rule crossed at 31/61/91 — a framed-era builder reserving
  column 0 for `├`. Also closed a hole in the closure law, which checked only
  `│` and so let `├`/`┤` survive the frameless pass. (`530a7a5`)
- **DONE** · **The emoji picker offers only unambiguous widths** — 1,483 of
  3,608. Every other class disagrees between rich and the terminal (ZWJ: 2 vs 4;
  variation selector: 2 vs 1; EAW=N/A: 1 vs 2). (`ccd4018`)
- **DONE** · **The gantt field draws in shade, not scatter** — braille bought
  sub-cell resolution a *span* does not need. Reach `█`, progress `▓`, task `▒`,
  half `▌`, phase tip as a rising fill. Lanes untouched. (`81dcb66`)
- **DONE** · **The right edge says the number** — `···▲3d` / `····4d` / `··done`
  / `·····—`. The bar stood for a BAND, so 4 days and 5 days drew the same two
  cells. Two laws reversed in place rather than deleted. (`e8dabba`)
- **DONE** · **Short content stays at the top** — `fill_height` pinned the last
  row assuming every view closes with an axis; the kanban and the agenda close
  with a TASK, so 84 kanban and 44 agenda sizes stranded a row at the bottom of
  the viewport. An axis is now declared. `tests/test_vertical_fill.py`,
  mutation-checked against both ways of breaking it. (`bd935ff`,
  `.fast-dev-flow/spec.md`)

### Open — carried from this session

- **Lanes geometry off-by-one.** `lane_geometry(120, …)` reports
  `today_cell = 44` while the today rule is drawn at column **43**, and
  `label_w + field_w + figs_w = 119` against a width of 120 — one cell
  unassigned. Not yet decided whether it is a defect or deliberate
  compensation; **no view misrenders because of it today**, which is why it was
  reported rather than "fixed" blind.
- **`test_win_clipboard_roundtrip` is flaky.** Its restore step
  (`Set-Clipboard -Value $prior`) raises `PositionalParameterNotFound` and leaves
  the clipboard in a state that fails the *next* run. Bug in the test, not the
  code; pre-existing.
- **The gantt meter vs the field speak two alphabets.** The right-edge reading is
  now text, but `due_meter` is shared with the lanes, so any further change to it
  moves both views. Deliberate boundary, recorded so the next reader knows it was
  a choice.
- **`emoji=False` is load-bearing and easy to "fix" wrongly.** Re-enabling
  substitution to support `:shortcodes:` turns
  `test_a_shortcode_is_drawn_as_itself_not_as_a_glyph` red *and* the row-width
  invariant with it. Whoever wants shortcodes must substitute BEFORE the width
  math (13 sites where user text enters the views), not after.

### Open — process (not this repo)

- **`~/.claude/docs/FLOW-VERSION.md` is stale by one control.** `f3d4fba` added
  **C-46** to `dev-flow-lessons/SKILL.md` (641 lines vs the 620 recorded) and is
  already pushed, but the manifest still declares `controls: C-1 … C-45` and the
  pre-C-46 hash. 11/12 files verify byte-for-byte; the twelfth is the manifest's
  own bookkeeping. Per its own rule — "if you edit a flow file, you own the bump"
  — this needs a rev2. **Different repo (`claude-config` + `claude-skills`), so
  it is not fixable from this batch's commit.**

## From 2026-08-03-batch-03 (CLOSED AT PHASE 2, nothing implemented)

The batch derived a full requirement set for "lanes row states its demand; the curve moves to a
disclosure row" and closed without code. `taskboard/` and `tests/` are byte-identical to `f237cb3`.
Full account in `.dev-flow/05-postmortem.md`.

### The next batch, and it is deliberately small

- **DONE** (2026-08-06, `/fast-dev-flow`) · **FIX AND VERIFY THE ROW COST MODEL, ALONE, WITH NO VISUAL CHANGE.** Every substantive
  disagreement across two iterations reduced to `room` / `prof` / the lead band's ±2. There is no
  single verified cost model, so each agent measured against its own and the conflicts only
  surfaced when a later agent re-derived an earlier one's number. Establish one — executed, pinned
  by a test, with `views.py:2127`'s `h - 2 - (2 if active else 0)` and `lead_band`'s `prof + 2`
  reconciled explicitly — and the rest of the design becomes row substitution.

### The design, decided and still standing (do not re-litigate)

- **Mechanism D in the project row** (`N open · ▲N late · next Nd`), **mechanism A on the
  disclosure row** (the cumulative curve). Operator-decided after seeing A/C/D rendered on the real
  board; C was rejected as answering the least actionable question.
- **Option (a)** pays for the disclosure row: the focused project sheds one title.
- **O-1: silent refusal** when the shed cannot be paid.
- **O-2 refined to option 2:** supersede `tests/test_spend.py:81` and `:277`; **REPLACE** `:238`
  with an explicit ceiling on `prof` — its subject (an upper bound on `prof`) survives the change.
- **O-3: no share cap.** ⚠ **Ruled on an understated number** — the operator was told 87 % of the
  panel; the band is `(prof+2)/h`, so it is **90 % at h=60 and 95 % at h=120**. The ruling's logic
  (the panel has only two sinks for surplus) is unaffected, but the next batch must re-present it.
- **O-3 RULED 2026-08-06: no share cap, confirmed after the correction.** The operator was
  re-presented the corrected figures — the band is `(prof+2)/h`, so **90 % at h=60 and 95 % at
  h=80**, not the 87 % he first ruled on — *and* the finding that this share is **already shipped
  behaviour on HEAD** (a calm board's bench is 93.3 % at h=60 today, driven by how many active
  lanes exist, not by `wrows`). He kept the ruling. Rationale on the record: the panel has only two
  sinks for surplus, the bench stops informing past ~4 rows (distinct column heights saturate at
  `prof = 3–4` and are unchanged through 52 while lit dots grow 16×), and the measured alternative
  `(2·room)//3` buys a 58–64 % bench for **51 blank rows over 24 renders** — retiring the shipped
  "never pads" law to install another.
- **O-4 RULED 2026-08-06: the view reports what it drew.** `render_swimlanes` returns what it
  actually drew through an out-parameter of the same kind as `line_map`, and `legend_entries` reads
  that answer. Costs four signature changes; the 8 existing call sites keep compiling on a `None`
  default. Both alternatives rejected on the record: recomputing payability inside `legend_entries`
  gives **two answers to one question** — the failure `swimlane_plan`'s own docstring names — and
  weakening the entry to *reachability* shows it when nothing is drawn. Note the gate that does NOT
  work: `selected_id is not None` is near-always true, because `App._select_first` runs at the top
  of every `refresh_view`.

### Findings that outlived the batch

- **The legend has never described the wave** (verified by sweeping every `out.append` in
  `legend_entries`). This is the direct cause of the operator's *"I am not certain what they do"*.
  **Candidate control:** the ghost-mark law verifies that every legend entry is drawn but **not that
  every drawn mark is explained**. That asymmetry is a hole in a shipped law.
- **`_figures`' docstring is one of 26 claim-bearing prose lines** that would go false; `grep "own
  wave"` catches only 3. `views.py:720` and `:2112` are the return contracts of the two functions
  the change re-signs.
- **`report.py:122` carries a false claim on disk today** — post-change the report would draw a
  curve for every project unconditionally while the app draws at most one.
- **`test_vertical_fill.py` and `test_occupancy.py:93` both render only `selected_id=None`** — so
  the never-pads law and the occupancy floor are measured in the one state the disclosure row would
  create. Two files, not one.
- **`lead_band`, `stack_block`, `project_wave` have zero direct test guards.**
- `tests/test_span_economy.py` is unmeasured against a ~114→~20 cell swap.

### Process items

- **`~/.claude/docs/FLOW-VERSION.md` is stale by one control.** C-46 landed in `f3d4fba` (pushed)
  and the manifest still declares `C-1 … C-45` with the pre-C-46 hash. 11 of 12 files verify
  byte-for-byte. Its own rule: whoever edits a flow file owns the bump. **Different repos**
  (`claude-config` + `claude-skills`), so not fixable from this one.
- **Orchestration lesson, encoded:** fix the `AT`/`TC` identifier register BEFORE dispatching
  parallel agents. Two Phase-1 agents in parallel minted colliding ids and broke the behavioural
  traceability chain.

## From 2026-08-06-fastflow-03 — the row cost model (SHIPPED, no visual change)

`/fast-dev-flow`, one increment, three files. **No behaviour change**: the `taskboard/views.py`
diff is two docstrings, proven prose-only by comparing the AST with every docstring stripped.
707 → 725 tests. Spec + probes: `.fast-dev-flow/spec.md`, `.fast-dev-flow/probes/`.

### What it settled

- **THE COST MODEL HAD NO DEFECT.** `swimlane_plan`'s `h - 2 - (2 if active else 0)` and
  `lead_band`'s `prof + 2` are the two halves of ONE correct identity, verified **124/124**
  in regime over 160 renders (5 boards × 4 widths × 8 heights, frozen clock, synthetic boards):

      room = h - 2 - 2*[active]      need = prof + Σ(wrows + min(titles,o)) + n_rest
      BODY == need + 2*[active]      2 + BODY + ABSENCE == h

  **The two `2`s are different**: `h - 2` is the panel's own chrome (header + axis, the close
  being frameless); `- 2*[active]` is the lead band's head and tail. Batch-03's headline claim
  ("the cost model undercharges `prof`") is **FALSE by execution**, and so is its inverse.
- **Pinned** by `tests/test_row_cost.py` (18 tests, laws L1–L9), and the model is now written
  down in the docstrings of `allocate` and `swimlane_plan` **with its regime**.
- **Every law is answerable to a mutation that reddens it** — 5 source mutations applied to
  `taskboard/views.py` for real (not monkeypatched), each killed, `views.py` restored
  byte-identical: `room = h-2` (6 failed) · `room = h-6` (2) · `lead_band ±1 row` (7 / 5) ·
  rung four dropping its `- 1` (1). Runner kept at `.fast-dev-flow/probes/_mutate_check.py`.

### Findings

- **A claim this repo shipped was FALSE, and is corrected.** `tests/test_vertical_fill.py:91`
  said *"the lanes never pad at all — their allocator spends the whole height it is given"*.
  It holds **only while a project is active**. On an all-resting board nothing draws the bench,
  `prof` is billed for it anyway, and the view pads **exactly `h - 3 - n_rest`** rows (verified
  across 5 lane counts × 4 widths × 8 heights). The operator reproduced this independently and
  ruled: **document the regime, do not change the behaviour.** Done.
- **`prof` is billed and never drawn when no lane is active.** Dead budget, harmless in effect
  (nothing else could spend it) but it makes the model's A=0 branch vacuous. **Deliberately left
  alone** — fixing it is a behaviour change, out of a "no visual change" batch. Carried below.
- **A vacuity trap that hid 2 of 5 mutations, and it was live in the first draft of this batch's
  own test.** Selecting the sample on `feasible = charge <= room` — a quantity computed from the
  code under test — makes M1 (call site never pays for the lead band) and M4 (no absence row
  reserved) pass **vacuously**; M1 leaves the sample EMPTY. The off-regime exclusion must be
  **static** (named fixture + height), and feasibility must be **asserted**, never selected on.
  Measured both ways. **Candidate control** for `dev-flow-lessons`: *an exclusion predicate
  computed from the code under test is a vacuous check wearing a filter's clothes.*
- **The bench share was already shipped behaviour, not change-induced.** On HEAD today, a calm
  board's bench is 86.7 % at h=30, **93.3 % at h=60, 95.0 % at h=80**; by board shape the max is
  `calm` 95.0 % · `typical` 73.8 % · `huge` 44.4 % · `busy` 41.2 %. The driver is **how many
  active lanes exist**, not `wrows`. Fed into the O-3 re-presentation above; the operator kept
  the ruling. The **post-change** share remains `NOT MEASURED` — it belongs to the redesign batch.
- **`fa821ae` was unpushed** when this batch opened, though the handoff asserted
  `HEAD == origin/main == fa821ae`. Resolved by the operator mid-batch: amended and pushed as
  `6b7c4c3` (which also made `_prototypes/` render a **synthetic** board on a frozen clock
  instead of carrying real project names and task titles into committed files), then `3b0f011`.
  **Standing practice, now explicit: no artifact may carry the operator's board data.** This
  batch's probes and fixtures are synthetic and in-memory throughout.

### Carried forward from this batch

- **`prof` is billed for a bench nothing draws when no lane is active.** A behaviour change, so
  out of scope here. Whoever opens it must keep `tests/test_row_cost.py::test_L8...` honest —
  it currently pins the pad as `h - 3 - n_rest`, which is what would change.
- **`lead_band`, `stack_block`, `project_wave` still have no direct test guards** beyond the
  arity/accounting ones this batch added. `project_wave` remains entirely unguarded.
- **The redesign batch is unblocked**: with the model fixed and pinned, "the project row states
  its demand; the curve moves to a disclosure row" becomes row substitution against a known
  budget. O-1, O-2, O-3, O-4 are all ruled; nothing in this batch reopened them.

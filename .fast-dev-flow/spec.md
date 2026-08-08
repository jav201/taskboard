# Quick Spec — `2026-08-07-fastflow-07`: the gantt gets a line and a rationed circle

**Base ref:** `c25d8e1` (main == `origin/main`, clean) · **Language:** English
**security_required: FALSE** (no flag fired — see §6)

## 1. Objective

Ship variant **A′** and the **rationed pulse**, both chosen by the operator from
prototypes he saw rendered:

1. The project's progress mark stops being a second row of shaded blocks
   (`▓▓▓▌`) and becomes a **circle riding on the reach line**. The band row at
   `taskboard/views.py:1938` goes away — that is the row the tasks get back.
2. The span line goes **thin**.
3. Task textures lighten: `▒`→line, `▌`→`╴`, phase tips `▃▅▆▇`→`○◔◑◕`.
4. The circle **pulses only when the project is BEHIND** — progress below the
   elapsed fraction of its span. Every other circle stays `●`, still.

## 2. THE BLOCKER, measured before any code

Lightening every texture moves the occupancy numbers, and two laws break.
Measured with `tests/test_gantt.py`'s **own** `_census` on its **own** fixtures
at 96×30, current code vs a patched module:

| law | today | A′+L with `─` | A′+L with `╌` |
|---|---|---|---|
| `marked >= 68.0` (typical) | 78.5 | **67.8 ✗** | **72.9 ✓** |
| `chrome < 10.0` (typical) | 0.0 | 5.0 | **0.0** |
| `dead <= 25.0` (typical) | 21.5 | **27.1 ✗** | **27.1 ✗** |
| `dead` (EXTREME) | 21.5 | 20.0 | **20.0** |
| `marked` (EXTREME) | 78.5 | 74.8 | **80.0** |

**Two independent causes, and they need different answers.**

### 2a. `─` is counted as FURNITURE

`_census`'s frame set is `╭─╮│╰╯├┤┬┴┼` and `─` is in it. Using it for a span
reclassifies data-ink as chrome, which is where the whole 5.0 and most of the
`marked` loss comes from. Same defect class as the `│`-vs-`┆` decision this
project already took for the week guide.

**Rendered, `╌` and `┄` are worse**: both are dashed, so they compete with the
`┆` guides and the `·` lattice and the span stops reading as a continuous
duration. The glyph is not the thing that is wrong — the census is.

### 2b. `dead` rises because the freed rows are SLACK, not waste

Typical (5 projects / 21 tasks) at 96×30 no longer has enough content to fill
the viewport, so 27.1 % is blank. On EXTREME (8 / 44) the same code measures
**20.0 %, better than today's 21.5 %**. The law cannot tell "wasting screen"
from "ran out of content", and this design makes that distinction matter for
the first time.

## 3. Acceptance criteria (observable)

- [ ] **AC1 — the row comes back.** At 104×26 on the synthetic board the view
  draws **0** `+N not shown` where today it draws 1, and every task fits.
  Observable: the rendered text contains no `not shown` figure.
- [ ] **AC2 — one row per project.** No project contributes a second field row.
  Observable: project rows == number of visible projects.
- [ ] **AC3 — the circle marks progress.** At progress `p` the circle sits at
  the cell `p` of the way along the span, and `◆` still marks due. Observable
  at p = 0.0 / 0.5 / 1.0 with a fixture, cell index asserted.
- [ ] **AC4 — the pulse is RATIONED.** On a board where one project is behind
  and others are not, exactly **one** circle changes glyph across a tick cycle.
  **And on a board where NO project is behind, NOTHING changes between ticks.**
  Both halves required: the second is what stops the pulse becoming ambient.
- [ ] **AC5 — the pulse obeys the house motion laws.** Cycle ≥ 2 s at the app's
  own `TICK_SECONDS` (no private constant), glyph-only, and **no style changes
  between ticks**. Observable by comparing `text.spans` across a cycle.
- [ ] **AC6 — width is still exact.** Every row is exactly `width` cells at
  80/96/104/120, with the ambiguous-width circles on screen.
- [ ] **AC7 — the occupancy laws pass, or are amended with their numbers.** No
  threshold is retuned silently; any amendment carries the measurement and the
  reason in the test's own docstring.

## 4. Open decisions — these block Phase B

| # | decision | options |
|---|---|---|
| **O-1** | ~~the span glyph~~ **RESOLVED WITHOUT THE AMENDMENT.** Splitting the two rules (`FIELD_REACH` `─` solid, `FIELD_TASK` `╌` dashed) restored the reach > task hierarchy AND moved most `─` cells out of the census frame set: chrome 5.0 → 3.1, marked 67.8 → **69.8**, over its floor. The census was never touched. |
| ~~O-1 (original options)~~ | the span glyph | **(a)** keep `─` and amend `_census`: this app is frameless (chrome is 0.0 precisely because the frame was removed), so `─` here is always data. Guard the amendment with a law that reddens if box CORNERS `╭╮╰╯` ever reappear, i.e. if a frame comes back. **(b)** use `╌` — numbers pass untouched, but the span reads dashed and competes with the field. **Recommend (a):** the render is what the operator approved, and the census is the thing that is now wrong. |
| **O-2** | the `dead` law | **(a)** narrow it to what it means: assert `dead <= 25` on a board whose content EXCEEDS the viewport (where slack is impossible), and on a short board assert instead that **nothing is hidden** — the property that actually matters there. **(b)** relax the threshold to 28. **Recommend (a):** (b) is a law weakened because it became inconvenient, which is how laws die. |

## 5. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| P1 the band row is at `views.py:1938` | premise | ✅ TRUE | `grep -n 'band_row(" " \* geo.label_w'` → 1938 |
| P2 `_span_bands` takes no tick | premise | ✅ TRUE | `views.py:1720-1721`, signature ends at `progress: float` |
| P3 lightening the textures breaks occupancy laws | **hypothesis** | ✅ TRUE | the table in §2, run through `test_gantt._census` on `test_gantt._load` fixtures |
| P4 `─` is in the census frame set | premise | ✅ TRUE | `test_gantt.py:198` `frame = set("╭─╮│╰╯├┤┬┴┼")`; swapping to `╌` moves chrome 5.0 → 0.0 and marked 67.8 → 72.9 |
| P5 the blank rows are slack, not waste | **hypothesis** | ✅ TRUE | EXTREME fixture: dead **20.0** vs today's 21.5, marked **80.0** vs 78.5 — with more content the same code is DENSER than today |
| P6 `● ◉ ◎` are width-1 but East-Asian AMBIGUOUS | premise | ✅ TRUE | `cell_len` = 1 for all three; `east_asian_width` = A for `●◎`, N for `◉`. **Not new exposure**: `◆ ━ ▓ ▒ ▌ ┆ ▲` already ship and are all A |
| P7 the gantt already has a moving element | premise | ✅ TRUE | `tests/test_motion.py:124-175` — the flow packet `▬` advances exactly one cell per tick |
| P8 `TICK_SECONDS = 1.0`, `RULE_PHASES` has 4 phases | premise | ✅ TRUE | executed import: cycle = 4000 ms, clears the 2000 ms illegal band |
| P9 the prototype's 15/0/3 reproduces | **hypothesis** | ✅ TRUE | `_prototypes/gantt_line_circle.py` at 104×26: drawn 15, hidden 0, blank 3 vs today 14/1/0 |

## 6. Security flags

No pattern fired. This batch renders glyphs from already-loaded data: no auth,
no secrets, no integration, no new input surface, no persistence change.
`security_required: false`. The privacy gate stays live regardless
(`core.hooksPath .githooks`) and no artifact of this batch may carry board data.

## 7. Increments (≤5 files each)

1. **The row and the circle** — `_span_bands` returns a span carrying `●`, the
   band row goes, the thin span lands (AC1–AC3) + tests.
2. **The rationed pulse** — `tick` threaded, behind-ness computed, glyph cycle
   (AC4–AC5) + the `test_motion.py` amendment.
3. **The laws** — occupancy re-measured and O-1/O-2 landed as amendments with
   their numbers (AC6–AC7).

## 8. Batch status

| AC | verdict | evidence |
|---|---|---|
| AC1 no `+N not shown` | ✅ | 104x26 demo board: absent. Old shape hid 1 |
| AC2 one row per project | ✅ | 5 project rows for 5 projects |
| AC3 the circle is a READING | ✅ | `_span_bands` at p = 0.0/.25/.5/.75/1.0: on the start cell at 0, on the `◆` cell at 1, monotone between |
| AC4 the pulse is rationed | ✅ | one behind + one on time -> exactly 1 breathes; behind removed -> 8 ticks byte-identical |
| AC5 house motion laws | ✅ | 4 x `TICK_SECONDS` = 4 s; one phase per tick through a distinguishable alphabet; styles identical across 8 ticks |
| AC6 width exact | ✅ | 80 / 96 / 104 / 120, every row, with the pulse on screen |
| AC7 occupancy | ✅ | `marked` 69.8 (floor 68). `dead` moved to the fixture where it means what it says; both amendments carry their numbers in their own docstrings |

## 9. Batch status

| field | value |
|---|---|
| Current phase | **CLOSED 2026-08-07** |
| Tip | `main` local, 776 green, **not pushed** |
| Smoke | 4 views + `?` legend; gantt 38 rows all 120 cells; live board untouched |

## 10. What the harness found that review would not have

1. Both rules were `─` for one commit — the hierarchy reach > task collapsed.
2. Removing the band row made the TODAY RULE vanish from the view; the legend's
   ghost-mark law named it immediately.
3. `test_the_pulse_rides_the_ONE_shared_clock` could not see a private
   multiplier, because `PULSE_PHASES` is a palindrome and `tick*3` through a
   palindrome yields the identical sequence. The symmetry that makes the motion
   read as a breath is what blinded the observable.
4. The substitute alphabet was first four digits — and the view is full of
   numerals, so the counter counted the axis.
5. `test_backlog_bar_is_static_across_ticks` was narrowed wrong twice: onto
   plain text (dropping the recolour channel the packet uses) and onto tick 0
   vs 7 on a seven-cell reach (`0 % 7 == 7 % 7`). **That aliasing pre-dated this
   batch**: the law passed because the gate held, not because it could see.
6. `test_nothing_is_hidden...` was first written at a size where the NEW shape
   hides too — it asserted something false and said so on its first run.

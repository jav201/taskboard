# Prototype notes — lanes_gauge

**Question.** After the load-strip round was rejected, the user set the
direction: **projects as COLUMNS, tasks as a plain list, and a needle
instrument** (KPI-cluster / car-cluster style) instead of any cumulative
chart. The rounds so far: R1 picked the dial semantics (C · countdown won);
R2 tried polygon dials (rejected on sight); R3 shaded a 3D torus per the M21
course module (textures won, small-dial resolution lost); R4 split into
single-purpose instruments (hourglass / mercury / sediment); R5 — the
current page — stacks the layout into a grid of roomier panels carrying both
the mercury spine and the sediment bar.

**Location.** `prototypes/lanes_gauge/out/lanes-gauge.html` — open in browser.
←/→ switches variants. Each section: the animated entry sweep (flipbook of 4
real renders) on the late fixture, the calm fixture, and the 68×24 narrow
render.

## Round 5 — the grid (the current page)

The verdict that drove it: mercury (E2) was liked but loses the time
measurements; sediment (E3) holds them but is cramped. The user's fix, and it
is the right one: **fewer columns, stacked layers, roomier panels.**

Each panel packs BOTH instruments plus the text back:

- **Mercury spine** (2 cells, left edge): the project's window (start at the
  bottom, due at the top), mercury = time consumed with grain texture, red
  with a ▲ cap when overdue, `▪` notches for landings.
- **Sediment bar** (full panel width): the countdown to the next landing,
  `▓▒░` grain ramp with zone tints, `╎` today rule, `▄` studs per task,
  `◂/▸` off-window flags. At 36-54 cells it is no longer cramped.
- **Task rows with their text back**: full-ish titles, indicators `! ▤ ↗`,
  and the absolute date chip. Overflow reads `+N more`.
- **Done tally** pinned to the panel's foot.

Two geometries on the page: **G1 · 3×2** (all six fixture projects at a
glance) and **G2 · 2×3** (maximum text room, layer rules between). Overflow
beyond the grid would be a `+N lanes` note in the header. Narrow (68 cols)
degrades to 2×3 with `+N more` per panel — verified.

The entry sweep animates both instruments at once (mercury rises, sediment
fill grows).

## Round 4 — single-purpose instruments (superseded by the grid)

The 3D torus's textures landed, but the dial's resolution did not ("se ve
bien la textura, pero la resolución no ayuda"). This round keeps the
countdown/clock semantics and changes the INSTRUMENT to mechanisms that
exploit what the terminal does well: straight edges, grain texture, vertical
resolution.

- **E1 · Hourglass (reloj de arena)** — the time-measuring object itself.
  Straight glass walls quantize cleanly in braille (the circle's failure mode
  is absent by construction); the sand carries the texture (deterministic
  grain noise + light wash). Upper sand = time remaining in the project's
  start→due window, lower pile = time spent, and an overdue project turns the
  pile `over`-red and backs it up the funnel. Task landings are studs on the
  left wall at their date height — a late task's stud sits in the spent sand,
  red. Entry animation drains the sand to the current level.
- **E2 · Mercury (vertical gauge)** — the column is narrow but TALL: a
  2-cell strip gets ~100 levels in the dimension the layout actually has.
  The strip maps the project's window (start at the bottom, due at the top),
  the mercury = time consumed rising from the bottom; overdue = the whole
  column goes red with a ▲ cap on the rail. Task landings are rail notches.
  Zero extra rows: the task list starts right under the header.
- **E3 · Sediment bar** — the countdown window (−7d…+21d) as a 2-row
  textured band: consumed runway as a `▓▒░` grain ramp with zone tints, today
  as the accent rule, landings as `▄` studs in the second row. The pragmatic
  minimum.

E1/E2 use the project's own window (start→due — B's semantics); E3 keeps the
next-landing countdown (C's semantics). The page shows both fixtures so the
difference is visible.

## Round 3 — the circle as a 3D torus (textures won, resolution lost)

The polygons looked wrong to the user; the circle was right. The 3D question
was answered from the course module `M21-3d-data-landscapes.html`:

- **Half-block `▄` = 2 colours per cell → shaded solids; braille is boolean →
  wireframe only.** Two folds of the same render are on the page.
- **Lambert multiplies: `final = zone_hue × max(amb, n·l)`** — hue and relief
  are not two free channels. The light stays near top-down (ambient floor
  0.35) precisely so the red/amber zones survive the multiply (M21 §4).
- **Budget is a non-issue at dial size**: ~2.5k surface samples per dial,
  analytic normals (no triangle z-buffer — the face-on tube cross-section is
  exact), microseconds per frame. In the app: precompute the 4 sweep frames
  once per data change; never re-derive per tick.

The build: `_torus_buf` splats the annular tube at (tilt ≈ 0.28 rad), shades
by the analytic tube normal, and folds two ways:

- **D1 · torus (half-block)** — true truecolor gradient, glossy pill ring.
  Softer silhouette, richest relief.
- **D2 · torus (braille wash)** — full 2×4 dot resolution for the shape,
  per-cell mean shade (one ink per cell). Crisper ring, grittier texture.

The needle is a raised bar (full accent face + shadow edge at ×0.45) and
pegs against the rim in the red; task landings are studs on the tube's inner
rim. Countdown semantics unchanged from round 2 (span −7d…+21d, red band at
the left, `◂/▸` off-dial flags, hub `Aug 1 ▲16d ·3`).

## Round 2 — faceted polygons (REJECTED by the user: "se ve mal")

The polygons landed on meaningful days and shaded cleanly, but the shape read
wrong next to the circle — kept in `proto.py` (`oct`/`hex`) for the record.
Their vertex-alignment finding survives in the C family's span choice.

- **A polygon's straight edges quantize cleanly** on a dot lattice; a circle's
  curve never can at this size.
- **The vertices are free tick seats** — and with the countdown span chosen
  right, they land on MEANINGFUL days, so geometry and semantics fuse:
  - **C1 octagon**, span −7d…+21d → vertices at **today, +7d, +14d**.
  - **C2 hexagon**, span −7d…+14d → vertices at **today, +7d**.
  The left facet IS the red overshoot band; the next facet IS "this week".
- **The relief is facet shading** — one flat brightness per face (light from
  the top-left), `_sh(zone_hex, k)`. On a circle the same treatment degrades
  to per-cell dither mud; on a polygon each face is constant by construction.
  This is the honest terminal version of "shaders con relieve".

Also new this round (C's blind spots, called out in round 1):

- **Every open task is a tick on the dial** (over / accent / project hue),
  not just the next one. Work off the dial is flagged with the app's own
  `◂`/`▸` convention at the matching end label.
- **The needle pegs against the bezel** (length r instead of r−2) when it
  enters the red band.
- **Dial direction flipped to the app's law** (past left → future right):
  late at the left end, FULL at the right. Round 1's render had it backwards
  against its own NOTES; this round is consistent.
- The hub tightened to `Aug 1 ▲16d ·3` so it never overflows the column.

**C0 (round flat)** stays on the page as the shape reference.

## Round 1 — kept for the record (in `proto.py`, off the page)

- **A · Pressure** — needle = 0.6 × late fraction + 0.4 × next-due proximity.
  Legible KPI, opaque formula.
- **B · Project clock** — the dial IS the calendar (arc = start→due, needle =
  today, ticks = landings). The purest answer to "where do the dates live".

## Shared layout law (all variants)

Column width adapts: `n_cols = inner // 19`, columns widen to fill (18 cells
at 118, 21 at 68 → 3 columns + a `+N lanes` header note, the `_phase_window`
convention). Task rows drop indicators at column width — the date chip
outranks them; blocked keeps its `▲` prefix. A per-column `n/N done` tally
pins to the last body row so a short column's void says something.

**Motion spec (for the real implementation).** 4-frame out-cubic sweep on
view entry (~600 ms, precomputed — style motion); a needle parked in the red
trembles ±1 dot on the app's 4 s ambient clock (the `RULE_PHASES` mechanism).
Both free by BUDGET.md's cost classes.

**Model changes required: none** (C family reads due dates only; B would want
`start_date` carried on `LaneFacts`).

**Status.** Concept-only, not wired to the real app.

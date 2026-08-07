# Quick Spec — taskboard · the gantt gets its gauge

| Field | Value |
|-------|-------|
| Batch id | `2026-08-06-fastflow-04` |
| Base ref | `7de3ad6` — **verified `HEAD == origin/main`** (`git rev-parse HEAD origin/main` → same SHA, after `git fetch --all`) |
| Predecessor | `.fast-dev-flow/archive/2026-08-06-fastflow-03-spec.md` — CLOSED 2026-08-06 (lanes row cost model, no visual change) |
| Flow revision | `~/.claude/docs/FLOW-VERSION.md` declares `C-1 … C-45`; C-46 landed unbumped in `claude-skills`/`claude-config` (carried from batch-03, different repos, not chased here) |
| Language | English |
| Phase | **C — implemented, validated, committed locally. NOT pushed.** |

---

## 1. Objective

The gantt shows bars measured against **nothing**. The operator:

> *"No estoy viendo en GANTT la implementación que decía el prototipo. Los bloques
> siguen siendo muy grandes y se empalman con el texto."*
> …and, from the start: *"atraen la vista a barras sin sentido, no hay gauges de
> semana y mes"*.

Only the prototype's **texture** shipped (`81dcb66`) — the heavy half. The three
parts that made `_prototypes/proto.py::hybrid` legible never did. Bring them over:
a real gutter, a week/month gauge, and a lighter project reach.

**Non-goal:** re-partitioning `label_w`/`field_w`/`figs_w`. See §5 — the change is
deliberately width-neutral.

---

## 2. What the prototype actually does (read, then rendered)

`_prototypes/proto.py::hybrid(screen="gantt")`, lines 322-380, rendered to text
in-session (the `file://` URL is blocked for the browser tool, so the prototype's
own `Grid` was dumped directly — same pixels, no HTML layer):

```
|  PROJECT / TASK                            AUG         SEP         OCT         NOV         DUE         |
|  ATLAS PLATFORM                        ━━━━━━━━━━━━━━━━  │  │  │ │  │  │  │ │  │  │     50%            |
|    Migrate the ingest workers · · · ·    │ ─  │  │  │ │  │  │  │ │  │  │  │ │  │  │               ▲3d  |
|  ▎ Retire the v1 scheduler  · · · · ·    │ │──│  │  │ │  │  │  │ │  │  │  │ │  │  │                2d  |
```

| # | Prototype mechanism | Line |
|---|---|---|
| 1 | dot leaders `"·" if x % 2 else " "` from title end to `FIELD_X-2` — the field starts at a FIXED column | `proto.py:359-360` |
| 2 | week guide `│` at every Monday column, drawn **before** the bar so the bar overwrites it | `proto.py:337-339` (project) · `353-355` (task) |
| 3 | month label `%b`.upper() at each month-start column, on the header row | `proto.py:327-330` |
| 4 | project reach `━` **in the project hue, low weight** — not a slab | `proto.py:345` |

---

## 3. Acceptance criteria (observable)

| id | criterion |
|---|---|
| **AC-1** | When a task's title is long enough to be truncated and its reach starts left of today, the rendered row shall place **at least 2 cells that are not title glyphs** between the last title glyph and the first bar glyph. (Today: 0 — measured, §4 P2'.) |
| **AC-2** | When a project's name is long enough to be truncated, the same ≥2-cell separation shall hold between the name and the first field glyph. (Today: 0 — `▎ Data Warehou…◂████`, §4 P0.) |
| **AC-3** | When the window contains a Monday, the field shall draw a week guide in that Monday's cell **on every body row**, in the lattice's own tone, and it shall never occupy the today column. |
| **AC-4** | When the window contains a 1st-of-month, a header row directly under `◆ GANTT` shall carry that month's 3-letter name starting at that month's cell. |
| **AC-5** | `FIELD_REACH` shall render as a thin rule, not a full block; `FIELD_PROGRESS`/`FIELD_TASK` are unchanged, so the three-weight hierarchy survives with its top weight lowered. |
| **AC-6** | Every rendered row shall remain **exactly** the requested width in cells (`rich.cells.cell_len`) at every width/height the suite sweeps. |
| **AC-7** | The gantt legend shall describe the week guide and the month label, and shall describe no mark the view stopped drawing. |

---

## 4. Premise table (C-43) — every verdict from an EXECUTED probe

Probes: `.fast-dev-flow/probes/_probe_gantt.py`, `_probe_premises.py`,
`_probe_collision.py`. All boards built in process from `seed_data()` or
`Project`/`Task` literals; **none reads `~/.taskboard/board.json`**. `TODAY` frozen
at 2026-07-30.

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| Base ref `7de3ad6` == `origin/main`, tree clean | premise | ✅ TRUE | `git fetch --all; git rev-parse HEAD origin/main` → both `7de3ad615c5d…`; `git status --short` → empty |
| Baseline is "725 passing" | premise | ❌ **FALSE** | `python -m pytest tests/ -q` → **`1 failed, 724 passed`**. The failure is `tests/test_app.py::test_win_clipboard_roundtrip` — `Set-Clipboard` has no clipboard in a non-interactive shell (`MissingArgument,…SetClipboardCommand`). **Pre-existing and environmental**, observed before any edit. Working baseline for this batch = **724 pass / 1 env-fail**. |
| "The gantt truncation collides with the bar, gutter = 0" | hypothesis | ✅ TRUE | `_probe_collision.py` P2': **5 of 5** long-title rows show `…` directly abutting `▬`/`▒`, at **104x30, 102x16, 96x30 and 120x40**. e.g. `▎  Telemetry_Ingestion_Name…▬▒▒▅······╎`. Requires the reach to start LEFT of today; when it starts right of today the today rule already separates them. |
| "`gantt_geometry(102,16)` → `label_w=12 · field_w=78 · figs_w=11`" | premise | ✅ TRUE | `_probe_premises.py` P1: `102x16: label_w=12 field_w=78 figs_w=11`. Note `large` needs `w>=88 and h>=26`, so at `104x30` it is instead `label_w=15 field_w=77 figs_w=11`. |
| "The project reach draws as `█`" | premise | ✅ TRUE | `views.py:1513` `FIELD_REACH = "█"`; rendered: `▎ Legacy Sunset······██████████████████◆` |
| "Occupancy law is `marked >= 45%`, today 72.3/80.9/83.8" | premise | ❌ **FALSE for the gantt** | Those are `tests/test_occupancy.py`, which renders **`"swimlanes"`** (`test_occupancy.py:93`), not the gantt, and its floors are `calm 29 / typical 46 / extreme 45`. The **gantt's** occupancy law is `tests/test_gantt.py:248` `marked >= 68.0` and `:249` `dead <= 25.0`. **Executed now:** typical(5/21) `marked=76.9 ink=26.7 dead=23.1 chrome=0.0`; extreme(8/44) `marked=76.8 ink=27.3 dead=23.2 chrome=0.0`. |
| Dead-space headroom on the gantt is comfortable | premise | ❌ **FALSE — it is 1.9 points** | `dead=23.1` against the `<= 25.0` ceiling (`test_gantt.py:249`). Any change that converts lattice into blanks has almost no room. |
| `test_gantt.py:238` `extreme.ink > typical.ink` has a wide margin | premise | ❌ **FALSE — 0.6 points** | `27.3` vs `26.7`. **This is the tightest law this change touches** (see §7 R1). |
| `test_gantt.py:164` pins title widths to exactly `(27, 30)` | premise | ✅ TRUE | `_probe_collision.py` P4': `near.count('B')+1 = 27`, `far.count('A')+1 = 30` — reproduced exactly. **This test WILL go red** and must be re-pinned deliberately. |
| Span-economy has headroom for extra runs | premise | ✅ TRUE | P8, gantt @120x40: `runs before=1740 after=135`, ceiling `before/3 = 580.0`. **x4.30 headroom.** |
| Week guides never land on the today column | premise | ✅ TRUE | P5 at 96x30, 104x30, 120x40: `week cell collides with today? False` at all three. (Code will still guard — the probe is 3 sizes, not a proof.) |
| The window always contains month boundaries | premise | ✅ TRUE | P5: 96x30 → 5 months (`JUL AUG SEP OCT NOV`) at cells `[5,21,36,51,67]`; 120x40 → 6. Window is 138-186 days wide. |
| `━` and `┆` are unused by any other view's legend | premise | ✅ TRUE | P7: agenda swatches are exactly `['●','─','┃']`; `'━' present? False`, `'┆' present? False` for gantt/agenda/swimlanes. So `test_legend.py:169` (`FIELD_REACH not in agenda`) survives `█`→`━`. |
| Every candidate glyph is exactly 1 cell | premise | ✅ TRUE | `cell_len`: `█ ━ ┆ ┊ · ╎ ─ │ ▒ ▓ ▌` → all `1` |
| The prototype's week guide `│` is safe to copy literally | hypothesis | ❌ **FALSE** | `│` is in the census FRAME set (`test_gantt.py:194`), guarded by `:258` `chrome < 10.0`, and chrome is **0.0 today** — the frame was deliberately removed. ~22 guides x ~25 rows ≈ 17 % chrome. **Must deviate from the prototype's glyph** — see §6 D1. |
| `test_row_cost.py` touches the gantt | premise | ❌ FALSE | Zero occurrences of "gantt"; imports are swimlanes-only (`test_row_cost.py:43-44`). Not at risk. |
| `test_vertical_fill.py` touches the gantt | premise | ✅ TRUE | `PINNED = {"gantt": 1}` (`:34`); asserts exactly 1 non-blank row below the blank pad (`:113`). **A month row must go at the TOP, never the bottom.** |
| Post-change census / title widths / run counts | hypothesis | ❓ **NOT MEASURED** | Cannot be measured before the code exists. Measured and pasted at the Phase-B gate. |

---

## 5. THE WIDTH ARITHMETIC — where this change works or breaks

**I re-partition nothing. `gantt_geometry` is not touched.** The cell-width law
(`tests/test_cells.py:83-86`, `cell_len`, widths 68/96/120) is protected by
construction rather than by re-measurement.

The invariant, executed at 7 sizes (P1) — `label_w + field_w + 1 + figs_w == inner`
holds at 68x24, 96x24, 96x30, 104x30, 102x16, 120x40, 94x30.

The gutter does **not** come out of that partition. It comes out of `over`, which is
not a partition term at all — it is a **loan of already-owned field cells to the
title** (`views.py:1834-1837`, the REV5 #19 ruling). Per row:

```
prefix width = spine(2) + " "(1) + title(label_w - 3 + over)   = label_w + over
band   width = len(reach[over:])                                = field_w - over
                                                                  ─────────────
prefix + band                                                   = label_w + field_w
+ " " + figures                                                 = 1 + figs_w
                                                                  ─────────────
total                                                           = inner   ∀ over
```

**The total is independent of `over`.** So changing

```python
over = max(0, min(_reach_start(t, geo, today), geo.today_dc // 2))          # now
over = max(0, min(_reach_start(t, geo, today), geo.today_dc // 2) - GUTTER) # proposed
```

moves `GUTTER` cells from the title back into the field, where `_band_markup`
already paints them as `LATTICE` (`views.py:1748`) — **the dot leaders are free,
because `LATTICE` is already `"·"` (`views.py:117`), the exact glyph the prototype
uses.** No new leader code, no width change.

The other two changes are width-neutral for simpler reasons:

- **week guide** — replaces one existing lattice cell with one guide cell inside
  `_band_markup`. 1 cell → 1 cell (`cell_len` verified).
- **`FIELD_REACH` `█`→`━`** — 1 cell → 1 cell (verified).
- **month row** — a new *line*, `_pad(…, inner)` like every other. Costs one row of
  **vertical** budget (`rows[:h-2]` → `rows[:h-3]`), **zero columns**.

The one place the partition *is* consumed differently: **AC-2**, the project row.
Its label is already exactly `label_w` cells (`fit(clip(name, label_w-2), label_w-2)`
after a 2-cell spine), so it has no `over` to borrow from. There the gutter must be
taken from the **name's own clip**: `clip(name, label_w - 2 - GUTTER)` still padded
by `fit(…, label_w - 2)`, so the prefix stays exactly `label_w`. Width-neutral;
the project name loses `GUTTER` characters.

**GUTTER = 2**, matching the prototype (leaders stop at `FIELD_X-2`).

---

## 6. Proposed change set (Phase B — for approval, NOT implemented)

**One increment, 3 files** (limit is 5).

| # | File | Change |
|---|---|---|
| D1 | `taskboard/views.py` | `FIELD_REACH = "━"`; add `FIELD_WEEK = "┆"`; add `GUTTER = 2` |
| D2 | `taskboard/views.py` | `_band_markup`: where a cell is empty and is not the today column, paint `FIELD_WEEK` instead of `LATTICE` if that cell holds a Monday — **in the lattice's own tone** (`ash` past / `dim` ahead) |
| D3 | `taskboard/views.py` | `render_gantt`: subtract `GUTTER` from `over` (both task loops); clip the project name by `GUTTER`; add the month-label row; `rows[:h-2]` → `rows[:h-3]` |
| D4 | `taskboard/views.py` | `legend_entries("gantt")`: add the week-guide and month-label entries (AC-7) |
| D5 | `tests/test_gantt.py` | re-pin `:164` to the measured post-gutter widths, **keeping** the `>` intent assertion at `:163`; add the AC-1/AC-2 gutter test and the AC-3/AC-4 gauge test |
| D6 | `tests/test_legend.py` | extend the gantt swatch set if D4 requires it |

### D1 — the deliberate deviation from the prototype, and why

The prototype rules weeks with `│`. **Copying it literally is measured to be wrong
here**: `│` is a census FRAME character, the gantt's chrome is `0.0 %` today, and
the design deliberately removed the frame. `┆` (U+2506) is a dashed vertical, is
not in the frame set, is quieter than the today rule `╎`, and is unused by every
other view's legend (P7). **Painting it in the lattice's own tone** — glyph changes,
colour does not — is what protects `test_span_economy.py:125`: run coalescing is by
style, so a same-tone guide costs **zero** extra runs.

This deviation needs the operator's yes: it is a visual difference from the approved
prototype, chosen because the prototype's own glyph would violate a law the
prototype was never measured against.

---

## 7. Risks

- **R1 — the tightest law is `test_gantt.py:238`, `extreme.ink > typical.ink`,
  margin 0.6 points (27.3 vs 26.7).** Week guides land only on *empty* field cells,
  and the typical board has more empty cells than the extreme one, so guides raise
  typical's ink slightly more than extreme's. This is the single most likely red.
  **Mitigation:** measured first at the Phase-B gate; if it reddens I stop and report
  rather than weaken the law.
- **R2 — `dead <= 25.0` sits at 23.1**, 1.9 points of room. The gutter converts title
  cells (ink) into lattice (field) — both are "marked", so `dead` should not move —
  but it is measured, not assumed.
- **R3 — `test_gantt.py:164` will go red by design.** Re-pinning a hard-coded
  expectation is exactly how a test quietly stops testing; D5 keeps the intent
  assertion (`far > near`) alongside the new pin.
- **R4 — `test_app.py:1557`** requires the today column to hold `RULE` or a `FIELD_*`
  glyph. The guide must never take that column (AC-3 states it; P5 shows it does not
  happen at 3 sizes; the code will guard anyway).
- **R5 — one less body row** at every height. At `h=20` the fixture needs 5 rows and
  has 17; no boundary is near, but `test_gantt.py:68` (`len(body) >= 5`) is the one
  to watch.

---

## 8. C-40 — the mutation that reddens each new predicate

Every acceptance test below gets its mutation **executed** at the Phase-B gate; a
predicate that survives its mutation is inert and will be rewritten.

| Test for | Mutation that must redden it |
|---|---|
| AC-1 gutter (task) | `GUTTER = 0` in `views.py` |
| AC-2 gutter (project) | drop the `- GUTTER` from the project name's `clip` |
| AC-3 week guide | `FIELD_WEEK = LATTICE` (guide becomes indistinguishable from ground) |
| AC-3 not-on-today | remove the today-column guard in `_band_markup` |
| AC-4 month row | return the header row without the month labels |
| AC-5 lighter reach | `FIELD_REACH = "█"` |
| AC-6 cell width | already covered by `test_cells.py`; mutation = `GUTTER = 3` with the project clip left at `label_w - 2` |

---

## 9. Non-goals (OUT — do not grow this batch)

- No change to `gantt_geometry`, `lane_geometry`, or `field_geometry`.
- No change to the swimlanes, agenda, or kanban views.
- No change to `FIELD_PROGRESS`, `FIELD_TASK`, `FIELD_HALF`, `FIELD_PHASE_TIP`.
- No fix for `test_win_clipboard_roundtrip` (pre-existing, environmental).
- No re-language of the bottom axis row (`-46d today +107d` stays).

---

## 10. Open questions for the operator

1. **`┆` instead of the prototype's `│` for the week guide** (§6 D1) — approve the
   deviation? The prototype's glyph is measured to break `chrome < 10.0`.
2. **The month row costs one body row** at every height. Acceptable, or should the
   months share the existing bottom axis row instead?
3. **GUTTER = 2.** Prototype-faithful. Bigger reads calmer but costs title
   characters on every task row.

---

## 11. Detected security flags

Scanned objective + criteria + change set against the fast-flow pattern list.

| Category | Match | Note |
|---|---|---|
| Auth / identity | none | — |
| Secrets / config | none | — |
| External integrations | none | — |
| Sensitive data | **`~/.taskboard/board.json`** | Not a flow flag, but the batch's hard rule: no artifact may carry the operator's real board. Every probe here builds its board in process; `_probe_gantt.py` uses `seed_data()` with a temp path that is **never written**. Verified by reading the probes, and no probe calls `Board.load` on the real path. |
| Destructive DB | none | — |
| Input / surface | none | — |
| Network / exposure | none | — |

**`security_required: false`.** No new external action surface; the change is
pure-render.

---

## 12. The operator's rulings on §10 (Phase-A gate, APPROVED)

1. **`┆` instead of `│` — ACCEPTED.** The finding was verified independently
   against `tests/test_gantt.py:192`.
2. **Months SHARE the bottom axis; no row of their own.** Chosen against advice
   and settled. Implemented as two scales on one row, in two tones (`mut` for the
   months, `dim` for the day figures), day figures anchored and month names
   dropped whole when they cannot stand clear.
3. **`GUTTER = 2` — ACCEPTED.**

---

## 13. Close — what was measured, after the fact

### 13.1 The laws, re-executed (never predicted)

| law | before | after | verdict |
|---|---|---|---|
| `test_gantt.py:248` `marked >= 68.0` (typical) | 76.9 | **78.5** | ✅ |
| `test_gantt.py:249` `dead <= 25.0` (typical) | 23.1 | **21.5** | ✅ improved |
| `test_gantt.py:258` `chrome < 10.0` | 0.0 | **0.0** | ✅ `┆` is not a frame char |
| `test_gantt.py:238` `extreme.ink > typical.ink` | 27.3 > 26.7 | **41.9 > 41.4** | ✅ **R1 did not materialise** |
| `test_span_economy.py:125` `after < before/3` | 135 < 580.0 | **155 < 594.7** | ✅ same-tone guide cost 20 runs |
| `test_gantt.py:164` title widths | (27, 30) | **(25, 28)** | 🔁 re-pinned, intent kept |
| `test_cells.py` cell-width law | green | **green** | ✅ nothing re-partitioned |
| full suite | 725 collected | **730 passed, 0 failed** | ✅ 725 + 5 new |

The clipboard test failed on the FIRST baseline run and passed on every run since
— it is flaky, not broken. Recorded in the backlog.

### 13.2 AC-1, the defect itself

`.fast-dev-flow/probes/_probe_collision.py`, long titles whose reach starts left
of today, at 104x30 / 102x16 / 96x30 / 120x40:

```
before   ▎  Telemetry_Ingestion_Name…▬▒▒▅······╎        COLLISIONS: 5 of 5
after    ▎  Telemetry_Ingestion_Na…┆·▬▒▒▅·┆··┆·╎·┆     COLLISIONS: 0
```

### 13.3 C-40 — every predicate's mutation, EXECUTED

`.fast-dev-flow/probes/_mutate.py` patches `views.py`, runs the one test, reverts.
**9 of 9 redden.** Two did not on the first pass, and both were real:

- **`FIELD_WEEK = LATTICE` survived** → the guide test would have passed on the
  lattice's own dots. Fixed by asserting `FIELD_WEEK != LATTICE` first.
- **removing the today-column guard survived** → `TODAY` is a **Thursday**, so the
  today cell can never hold a monday and the assertion was vacuous. Fixed by
  re-asserting the guard at `2026-08-03` (a monday) and `2026-08-02` (a sunday,
  the other half of the cell).

Two of my own acceptance predicates were also inert as first written: `got >=
GUTTER` and `tail.endswith(" " * GUTTER)` are both trivially true when `GUTTER`
is 0 — the exact mutation they exist to catch. Both now use the literal `2`.

### 13.4 What changed

| file | change |
|---|---|
| `taskboard/views.py` | `FIELD_REACH` `█`→`━`; new `FIELD_WEEK`, `GUTTER`; new `gantt_gauge`; `_band_markup` takes `weeks`; `_scale_row`/`_scale_with_note` take `months` via new `_scale_cells`/`_tone_runs`; `render_gantt` applies the gutter to task rows and the project name; two legend entries derived from the drawing functions themselves |
| `tests/test_gantt.py` | `:164` re-pinned to `(25, 28)` with the intent assertion kept above it; 5 new tests (AC-1…AC-5) |
| `.dev-flow/BACKLOG.md` | batch marked DONE; 5 carries appended; base ref bumped to `7de3ad6` |
| `.fast-dev-flow/probes/*.py` | 4 probe scripts (repo convention: prior batches' probes are tracked) |

**`gantt_geometry` was not touched.** No re-partition, so the cell-width law was
never in play — which is what §5 predicted and the green `test_cells.py` confirms.

### 13.5 Open — carried to the backlog, not fixed here

The week guide's density and irregular 3/4-cell rhythm; `AUG` dropped from the
axis when it collides with `today`; `NOV +111d` one space apart; two dead braille
assertions found while mapping the laws; the flaky clipboard test.

---

## 14. Batch status

| Field | Value |
|---|---|
| Current phase | **C — closed, awaiting the operator's review, push and merge** |
| Tests | **730 passed, 0 failed** |
| Commit | local only — **no push, no merge** |
| Security | `security_required: false`; no artifact carries the operator's board |

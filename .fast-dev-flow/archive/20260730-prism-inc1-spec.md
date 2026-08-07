# Quick Spec — Prism Increment 1: the colour ration

**Status:** CLOSED 2026-07-30 · **Base ref:** `b3cc60d` (main) · **Flow:** fast-dev-flow · **Language:** English
**Result:** all six acceptance criteria met. 152 tests green (137 pre-existing + 15 new),
4 mutants killed (M1 re-add amber, M2 non-optimal remap, M3 oscillating load, M4 revert
the glyph), every mutated file restored byte-identical. `~/.taskboard` md5+mtime unchanged
across all 11 files. Carry-overs recorded in `.dev-flow/BACKLOG.md`.
**Source of truth:** `_tui_prism_proposal/PROPOSAL.md` §9 row 1, measurements in `AUDIT.md` §5.

## 1. Objective
Give every hue exactly one job. Today `amber` is simultaneously a project identity
hue and the hue the app uses for *due today* / *high priority* — rgb distance 0.0,
the same colour meaning two things in all five views. Drop the four identity hues
that collide with a judging hue, remap old boards deterministically, and move the
high-priority marker out of the colour houses into the glyph house.

## 2. User stories
- As a user, when a mark is amber I want to know it means *urgency*, never *which project*.
- As a user with an existing board, I want it to keep loading — my projects get a
  lawful colour automatically, and the same one every time.
- As a user, I still want to see which tasks are high priority, without that mark
  borrowing the urgency colour.

## 3. Acceptance criteria (observable)
- **AC1 (ration).** For every name in `PROJECT_COLORS`, the rgb distance from
  `HEX[name]` to each judging hue is above its house's band: >=70 from `over`
  (#f43f5e) and `soon` (#fbbf24); >=55 from `accent` (#2dd4bf). Measured, not a
  name list. `PROJECT_COLORS` has 8 entries and contains none of
  `rose`/`orange`/`amber`/`cyan`.
- **AC2 (remap).** `Project.from_dict({"color": "amber"})` yields `lime`;
  `rose`->`pink`, `orange`->`fuchsia`, `cyan`->`sky`. An unknown colour still falls
  back to `violet`. The map is injective — two projects that differed still differ.
- **AC3 (stability).** load->save->load->save of a board containing all four dropped
  hues produces byte-identical JSON on the second and third passes (fixed point,
  no oscillation).
- **AC4 (no collateral).** A board whose projects use only surviving hues is
  byte-identical after a load->save round trip.
- **AC5 (glyph house).** The high-priority marker rendered by `card_cell` is `!`
  in a neutral (`ink`) tone; `HEX["soon"]`/`#fbbf24` appears nowhere in the markup
  of a high-priority card, and `◉` is gone. Verified through the real renderers of
  the views that draw it (swimlanes, kanban).
- **AC6.** All 137 existing tests stay green (system python; see §5 note), and the
  one test that encodes the *old* 12-colour law is rewritten to the new law rather
  than deleted.

## 4. The measured law (recomputed on this repo, not copied)

`python -c` over `taskboard.models.PROJECT_COLORS` x `taskboard.views.HEX`,
euclidean rgb — the same metric `_tui_prism_proposal/audit_capture.py:146` uses:

| identity hue | over | soon | accent | done | verdict |
|---|---|---|---|---|---|
| amber #fbbf24 | 140.7 | **0.0** | 258.7 | 204.7 | **DROP** — identical to *due today* |
| orange #fb923c | 90.0 | **51.0** | 252.9 | 194.5 | **DROP** |
| rose #fb7185 | **63.8** | 124.5 | 235.8 | 194.3 | **DROP** |
| cyan #22d3ee | 294.5 | 297.1 | **48.3** | 143.2 | **DROP** — reads as the today-rule teal |
| sky #38bdf8 | 273.7 | 288.1 | 62.4 | 143.0 | keep (thin: 7.4 over the accent band) |
| green #4ade80 | 235.2 | 201.9 | 70.1 | 69.6 | keep (`done` is a check tint, not a field — no band) |
| lime, blue, indigo, violet, fuchsia, pink | >=165.9 | >=97.7 | >=91.1 | >=136.4 | keep |

**Deviation from the proposal, stated up front.** PROPOSAL.md §9 phrases the
criterion as *"ninguna distancia identidad<->severidad < 70"*. That single threshold
is not consistent with the drop list it names in R1: at a flat 70 over all four
judging hues, `sky` (62.4) and `green` (69.6) would fall too — six drops, not four.
The measured numbers govern, so the law is written as **two bands**: judging hues
(`over`, `soon`) get the wide band 70; the attention hue (`accent`) gets 55, which
is the only band that separates the measured pair cyan 48.3 / sky 62.4; `done` gets
none. That reproduces exactly the four drops the operator approved. The 55 band is
calibrated, and its margin is thin — recorded as a risk, not hidden.

**Remap.** Injective assignment minimising total rgb distance (brute-forced over
all 1680 injective maps; the optimum is unique, runner-up +3.04):
`rose->pink 49.5` · `cyan->sky 32.7` · `amber->lime 97.7` · `orange->fuchsia 191.6`.
Injective *by requirement*: nearest-with-reuse would send both amber and orange to
`lime`, making two previously-distinct projects indistinguishable — which destroys
the very house the ration protects.

## 5. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| `PROJECT_COLORS` is a 12-tuple in `models.py` | premise | TRUE | `taskboard/models.py:19-20` |
| The four names in PROPOSAL R1 exist in this code | premise | TRUE | grep: rose/orange/amber/cyan all at `models.py:19` |
| amber == the due-today hue, distance 0.0 | premise | TRUE | recomputed: `amber #fbbf24` vs `soon #fbbf24` -> 0.0 |
| "no distance < 70" selects exactly those four | hypothesis (from the design batch) | FALSE | at 70, `sky` 62.4 and `green` 69.6 also fall -> §4 two-band law |
| The high-priority marker is rendered in all 5 views | hypothesis | FALSE | `◉` occurs once in source: `views.py:175` (`card_cell`), used by swimlanes (`views.py:413`) and kanban (`views.py:1040`) only; columns/agenda/gantt never render priority |
| The colour *ration* affects all 5 views | premise | TRUE | project hues are painted in all five (`views.py:425`, `459`, agenda/gantt chips) |
| Old colours are validated on load in one place | premise | TRUE | `models.py:374` `color=... if ... in PROJECT_COLORS else "violet"` |
| Baseline is 137 green | premise | TRUE | `python -m pytest tests -q` -> `137 passed in 33.19s` |
| `.venv` can run the suite | premise | FALSE | `.venv` python -> `5 failed` (`ModuleNotFoundError: No module named 'PIL'`); use system python |
| No `docs/engineering-rules.md`, no backlog file exists | premise | TRUE | `Test-Path` -> False; `.dev-flow/` has no BACKLOG.md -> create the default |

## 6. Security flags
Scan of objective + criteria: **none fired.** No auth, secrets, network, external
integration, or user-input surface. The only data-safety concern is the live board,
handled by the standing rule: `~/.taskboard/board.json` is never opened — md5+mtime
of all 11 files under `~/.taskboard` baselined before the batch and re-verified at
close. `security_required: false`.

## 7. Non-goals (stated, not silently skipped)
- Adding a priority marker to columns / agenda / gantt (they show none today — new
  feature, not a ration).
- The `!N` *aggregate* per project row — that is Increment 3's lanes row; a task
  card carries one task, so N is always 1 and the mark is `!`.
- Removing the four hexes from `views.HEX`: they stay as palette constants (tests
  and code construct `Project("X","cyan")` directly; the ration is defined on
  `PROJECT_COLORS`, which is what the picker and the loader read).
- `ribbon.py:49` paints the ISO week in `amber` — a non-identity mark wearing the
  reserved hue. Real finding, outside this increment -> backlog.
- Views 2-5 layout, the lanes redesign (Increments 2-6).

## 8. Files (5 code + 2 flow artifacts)
`taskboard/models.py` · `taskboard/views.py` · `tests/test_palette_ration.py` (new)
· `tests/test_app.py` (rewrite the old 12-colour law) · `README.md`
· `.fast-dev-flow/spec.md` · `.dev-flow/BACKLOG.md` (created at close)

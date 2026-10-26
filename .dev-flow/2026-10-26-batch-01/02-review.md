# Phase 2 Review — taskboard — Batch 2026-10-26-batch-01 (audit of shipped f4b53cc)

> **Artifact language.** English. **Mode:** audit — the review lenses evaluate a change that
> already shipped; no code change is applied in this batch. Each lens ran as an **independent
> spawned sub-agent** carrying its role file from `agents/` of the dev-flow bundle
> (`C:/Users/jjgh8/.claude/skills/dev-flow/`): `spawned — generic agent with agents/<role>.md`.
> Every finding carries an id and a severity; HIGH findings carry a proposed fix (NOT applied —
> the orchestrator decides).

## Lens 1 — architect — spawned with agents/architect.md

**Verdict: iterate-to-refine** — the `done_rows` seam is APPROVED (minimal, default-off, exactly
three setters, nav/render parity); the records layer must iterate (AX-1, AX-2, AX-3).

- **AX-1 | HIGH |** The live requirements canon still encodes the reversed law, and no ledger
  entry records the 2026-10-26 reversal — `REQUIREMENTS.md:27` (HLR-102 «shall never draw a row
  for rest work»), `:29` (HLR-104), `:39` (LLR-101.3), `:139` (LLR-602.1 rows = open + reached
  milestones only).
  *Proposed fix:* one canon amendment (e.g. LED-2026-10-26) restating HLR-102/104 and
  LLR-101.3/602.1 to the new law (done, not-archived, non-milestone rows at the tail when the
  board gantt asks; archived never draws; folding budget counts drawn rows; nav walks them).
  History stays (batch artifacts and BACKLOG.md:631 header remain records of their time).
- **AX-2 | HIGH |** The shipped toast still tells the user a finished task «folded into ✓N» while
  it now keeps its row — the code's own docstring contradicts its message —
  `taskboard/app.py:2313` (string) vs `taskboard/app.py:2297-2300` (docstring); the wording is
  pinned by `REQUIREMENTS.md:61` (HLR-206) and `:74` (LLR-206.1) and asserted by
  `tests/test_gantt_polish.py` (AT-206/TC-208).
  *Proposed fix:* reword the toast, e.g. `{title} done · kept on the gantt · u undo` (mention
  `✓N` only as a count summary), revise HLR-206/LLR-206.1, update the asserting tests.
- **AX-3 | MEDIUM |** Gantt legend gloss misdescribes finished work and its swatch tone ≠ the
  drawn chip tone — `taskboard/views.py:8702` («finished work, folded into a count», swatch
  `done` #3f9c6d) vs the done-row chip painted `reached` (`taskboard/views.py` ~3403).
  *Proposed fix:* reword to «finished work: a quiet row, also counted in ✓n»; paint the swatch
  `c("✓", "reached")`.
- **AX-4 | LOW |** Pre-existing nav/frame body-height gap (nav gantt body = height−1−RULER
  `views.py:8367`; frame also subtracts the legend strip `views.py:3303-3304`; active gantt
  search draws at bar_h = height−2 `views.py:7954,7981` while app nav adjusts height for kanban
  only `app.py:2061-2065`) — with done tails `len(rows)` grows, so a 2-row difference can flip
  unfold decisions screen-vs-cursor (F-3 parity edge).
  *Proposed fix:* pass the strip/search-adjusted body height into `nav_model`'s gantt branch.
- **AX-5 | LOW |** `tests/test_gantt_board.py:10` module docstring still narrates done folding to
  `✓n` — historical field report now misleading.

**Censuses (architect):** stale live-contract rows: 4 (+2 encoded wordings); stale shipped
strings: 2 (`app.py:2313`, `views.py:8702`); stale test narrative: 1. All updated in-code
comments/docstrings accurate. Call-site census COMPLETE: exactly three `done_rows=True` sites
(`views.py:3263` render_gantt, `:8369` nav_model gantt, `:8659` legend); `gantt_link_order`
(`:8822`), `gantt_link_frame` (`:8837`), `_notify_folded` (`app.py:2303`) correctly leave the
default; presentation and exports never touch the seats — G4 structurally kept. Structural fit:
folding spends `len(rows)` (done tails in height), pressure stays open-only, `gantt_window`
open-only, off-window done bars clip with `◂▸` — exactly G3.

## Lens 2 — code-reviewer — spawned with agents/code-reviewer.md

**Verdict: OK-TO-ADVANCE** — no HIGH findings; drawing core, flag seam, and test restatements
faithful to G1–G5; verified by 3280/3280 suite plus targeted re-runs (23 + 7 nodes green).

- **CR-1 | MEDIUM |** Toast and legend copy still say finished work is «folded into a count»
  while the task keeps its row (same defect as AX-2/QA-1; severity MEDIUM on this lens).
  *Proposed fix:* reword toast + legend entry; update pinned strings in `test_gantt_polish.py`.
- **CR-2 | MEDIUM |** `test_more_data_no_longer_produces_less_screen` restated post-change: the
  at-height ink-direction arm was dropped and the dead bound loosened 25.5→29.5 (declared
  rebaseline); the replacement height-0 arms + `len(done)==5` arm are strong and still guard
  the original defect — `tests/test_gantt.py:290-310`. Accepted as a declared rebaseline;
  recorded so the loosening is visible to the next batch.
- **CR-3 | LOW |** Stale citations of retired rule G-A in `_gantt_frame` docstring title
  (`views.py:3280`) and legend comment (`views.py:8655`).
- **CR-4 | LOW |** TC-118 moved 118x30→118x40 (`tests/test_colour_budget.py:144`); chain
  rendering at the operator's production size no longer pinned; legend row at 118x30 consumed
  by done rows (TC-110) — documented consequences of G1+G3, not silent.
- **CR-5 | LOW |** AT-207 highlight up-move pins loosened +1 with documented rationale; still
  regression pins — `tests/test_gantt_polish.py:515`.

Correctness pass (clean): `_gantt_done_bar` mirrors `_gantt_bar` exactly except the
G2-justified divergences; `phase_index` never None (`models.py:1166-1170`); `done_tail` is
exactly G1 with no aliasing (undated done tasks sink via `date.max`); painter done branch keeps
the dep mark, respects `chip_w==0`, dims the selected title identically to reached milestones;
archived tasks cannot reach the branch.

## Lens 3 — qa-reviewer — spawned with agents/qa-reviewer.md

**Verdict: PASS — no HIGH findings. GOLDEN-FILE VERDICT: CLEAN.**

**Golden-file verdict (the batch's key risk, trigger B3):** the regenerated sealed oracle
`.dev-flow/2026-10-20-batch-01/evidence/frames-base.json` moves **exactly 4 of 40 frames —
`gantt@{40,80,118,160}`, `.plain` field only** (`row0_spans` untouched); the other 36 frames
are byte-identical; regenerating at HEAD reproduces the committed golden exactly; the
`frames_base.py` +3 lines are **docstring-only** (no `done_rows` logic, no view bias). The
claim in the shipped commit message is verified true.

- **QA-1 | LOW |** Finish-toast copy stale (same string as AX-2/CR-1).
  *Proposed fix:* message «… done · keeps its row, counted in ✓{rest} · u undo» + update the
  two asserting tests.
- **QA-2 | LOW |** TC-118 chain check moved 118x30→118x40 (Mobile App folds at x30 now).
  *Proposed fix:* keep the 118x40 assertion and add an 118x30 companion asserting the folded
  group draws no `━` reaches and no accent hue.
- **QA-3 | LOW |** AT-207 up-move bounds loosened 2→3 / 1→2; justified (+1 row per done tail,
  RED-on-base retained) — accepted.
- **QA-4 | LOW |** Emptiness bound 25.5→29.5 (measured 28.54; margin 0.96); loosening
  justified by G3, compensated by the new `len(done)==5` arm + height-0 anti-runaway asserts —
  accepted.

**WH-encoding:** strong — test docstrings quote the operator's words and cite G1–G5
(`tests/test_gantt.py:84`, `tests/test_gantt_board.py:606`, `taskboard/views.py:2473` quotes
the Spanish verbatim). **Commissioned coverage:** all four cases present (archived-hidden,
all-done project, cursor-by-keys, presentation byte-identity) — none missing. **Executed:**
import probe → worktree path (`evidence/import-probe.txt`); targeted 123 passed + 62 passed,
0 failed (`evidence/suite-targeted.txt`, `evidence/suite-targeted2.txt`). **Consumed:** the
change's own three chunk transcripts 1440+961+879 = **3280 passed, 0 failed** (now at
`evidence/scratch-evidence/`).

## Lens 4 — ux-reviewer — spawned with agents/ux-reviewer.md

**Verdict: PASS** — every painted criterion of G1/G2/G3 holds on the real shipped surface; no
HIGH or MEDIUM findings. Real Windows Terminal captures (harness adapted from the 2026-10-21
batch; every window a unique `ga-` title, launched with `NO_COLOR` cleared and
`COLORTERM=truecolor`, closed by title; `JJ_WORKPC: dev-flow` never touched; no process
killed):

| # | File (under evidence/captures/) | Size | Proves |
|---|---|---|---|
| 1 | `png/gantt_118x30.png` | 118x30 | G1+G2: done rows visible and quiet (dimmed titles, reached-tone bars, `✓` chips, no `▲Nd`); the all-done project shows its rows; the archived task appears NOWHERE; spans count done work. |
| 2 | `png/gantt_80x24.png` | 80x24 | Same board at production-narrow size — quiet done rows fit; archived still absent. |
| 3 | `png/busy_80x24.png` | 80x24 | G3: done rows consume fold room — only 2/8 groups unfold on the busy board. |
| 4 | `png/busyoff_80x24.png` | 80x24 | Flag-off comparison (done work archived): 6/8 groups unfold — the pre-change fold; matches the `done_rows=False` render oracle exactly. |

Window-cleanup assertion: **PASS** (no `ga-*` window left; re-verified after the last capture).
Colour checks: all PASS (458 / 433 / 374 / 359 distinct colours per PNG; none all-black).

- **UX-1 | LOW |** On busy boards at 80x24 done rows crowd out other projects' open work (6
  groups folded while 2 unfolded groups spend 3 of 5 rows on finished tasks). This is exactly
  the G3 trade-off the orchestrator specified, not a defect — shown side by side for the
  operator's confirmation.
- **UX-2 | LOW |** First-run «View keys renumbered» toast overlays the gantt's bottom-right in
  every capture (fresh temp home per scene); never covers labels, fold arrows or `✓` chips.

Not covered (named, not smoothed): keyboard walkthrough and G4 byte-identity are the qa lens's
seats (covered there); evaluation with real users — not performed (one-person team).

## Consolidation (orchestrator)

- The batch's two HIGHs (AX-1 canon, AX-2 toast) are **records-layer defects**, not drawing
  defects: the shipped code is faithful to G1–G5 and verified green three ways (suite, targeted
  re-runs, real-terminal paint). They ride to the backlog as open findings with proposed fixes;
  per the standing authorization the audit applies nothing.
- CR-1/QA-1 duplicate AX-2; consolidated in the backlog as one item.
- Route: approve the audit record; P4 validation next; no iterate-to-P1 (the requirements
  written retroactively survived all four lenses — one correction, the order-test file path,
  was fixed in place at the P1 gate).

# Quick Spec — the lane row says what it asks of you; the curve moves to the selection

**Status:** PROMOTED to `/dev-flow` 2026-08-03 (operator-approved). Phase A's premise table
survives and carries forward — P1/P2 were disproven with executed evidence, P3 was decided as
option (a), P6 turned up that the legend never described the wave at all. The promotion trigger:
phase B is not a visual swap but a LAYOUT-ENGINE change, 39 coupled call sites through
`allocate()`, and lanes spends its height exactly so the row budget moves with it.
**Original status:** phase A (gate) · **Base ref:** `f237cb3` (origin/main) · **Batch:** `2026-08-03-fastflow-02`
**Flow:** `2026.07.28-rev1` — 11/12 files hash-verified. The twelfth (`dev-flow-lessons/SKILL.md`)
is a **stale manifest**, not local drift: C-46 landed in `f3d4fba` and nobody bumped
`FLOW-VERSION.md`. Carried in the backlog; unchanged since the last batch.

---

## 1. Objective

In the lanes view, a project row states **what the project asks of you now** in words, and the
cumulative load curve moves to the row that opens when a task is selected.

---

## 2. User stories

- As the board's owner **operating** the board, I want each project row to tell me open count,
  overdue count and the next deadline, so I can triage without decoding a mark.
- As the board's owner **stopping on a project**, I want its load curve where I am already looking,
  so the shape answers a question I just asked instead of decorating a row I am scrolling past.

---

## 3. Acceptance criteria (observable)

- **AC1.** When the lanes view renders a project row, it shall contain the open count, the overdue
  count (or an on-time token) and the next due distance, as TEXT.
- **AC2.** When no task is selected, the lanes view shall draw **no cumulative curve anywhere**.
- **AC3.** When a task is selected, exactly **one** row shall carry that project's cumulative curve,
  and it shall be adjacent to the selected row.
- **AC4.** The curve shall keep `load_curve`'s semantics unchanged: cumulative, normalised to the
  project's TOTAL task set, and **stopping at the project's due date**.
- **AC5.** When the lanes view renders at any height, it shall still spend exactly that height, with
  or without a selection — the disclosure row may not push the view past its viewport.
- **AC6.** The legend shall describe the curve where it is actually drawn and shall not advertise it
  on the project row (the ghost-mark law).
- **AC7.** Occupancy shall stay above its floors at every load class.

---

## 4. Validation strategy

Rendering-level tests over the lanes view with and without a selection, at several heights. The
curve's semantics get a direct unit check against `load_curve` rather than a redraw comparison.
Occupancy re-measured with the existing census. Mutation: blanking the disclosure must turn AC3 red,
and drawing the curve on every row must turn AC2 red.

---

## 5. Non-goals

- The gantt. This batch is the lanes row only; the gantt prototype work is separate.
- Any new visual language. Ledger/Darkside/Naught stay prototypes in `_prototypes/` (uncommitted).
- Deleting `wave.py` or `load_curve`. The curve **moves**; it does not die.
- The lanes geometry off-by-one (`today_cell` 44 vs rule at 43) — still open in the backlog.

---

## 6. Detected security flags

Scanned sections 1-4. **No match** — the batch renders counts and a curve from data already loaded.

- [ ] Auth — [ ] Secrets — [ ] Integrations — [ ] Sensitive data — [ ] Destructive DB
- [ ] Input surface — [ ] Network

**`security_required`: false**

---

## 7. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| **P1** Removing the wave from project rows breaks the occupancy floor | Hypothesis (I raised it) | ❌ **FALSE** | `test_occupancy.census` on the real fixtures: marked **72.3 / 80.9 / 83.8 %** against a floor of **45 %** — 27-38 points of headroom. The wave is **114 cells, 4.0 %** of a 96x30 render. The risk was real to check and small once measured. |
| **P2** The disclosure row costs a reflow on every arrow key | Hypothesis (I raised it 3x) | ❌ **FALSE** | Marginal cost of one extra row: **−0.17 ms** (4.51 → 4.34 ms, noise). Structural reason: `app.refresh_view()` already re-renders the WHOLE view on every keypress, so a disclosure row is not a new cost class. I over-warned. |
| **P3** The height allocator can absorb a row that appears with the selection | Hypothesis | ❓ **UNDECIDABLE — blocks** | `allocate()` returns *(titles, lead bench rows, **wave rows each**)* and lanes **never pads** (measured: 0 blank rows at h=30/45/60). So the height is spent exactly, and the disclosure row has no source. **Where its row comes from is a design decision this batch must make, not discover.** |
| **P4** The allocator's doctrine supports the change | Premise | ✅ TRUE | `allocate()` docstring: ties break *"toward titles first (a named task outranks a taller curve on a mission-control surface)"*. |
| **P5** `load_curve` can be called for one project without the lane machinery | Premise | ✅ TRUE | `wave.load_curve(bm, steps, total, edge)` takes a Bitmap and plain lists; `views.py:986` is its only caller. |
| **P6** The legend advertises the wave today | Premise | ❓ **UNDECIDABLE** | Not yet grepped for the swimlanes branch. Must be resolved before AC6 can be written as done — the ghost-mark law already caught one stale swatch this session (`⣤⣤⡄`). |

### P3 — the decision this gate needs from the operator

Lanes spends its height exactly, so the disclosure row must be paid for. Three ways:

- **(a) The focused project sheds one title.** The row count stays constant; the disclosure replaces
  a named task in that lane only. Cheapest, and consistent with "space is
  information-proportional" — you traded a name you are not looking at for a curve you asked for.
- **(b) The allocator reserves one row permanently.** Simple and stable, but pays the cost even
  when nothing is selected, which is the waste this whole batch is removing.
- **(c) The disclosure overlays the row below.** No arithmetic changes; but it hides a real row,
  and this app has a law against a mark that lies about what is there.

**Recommendation: (a).** It is the only one that spends nothing when you are not asking.

---

## 8. Batch status

| Field | Value |
|-------|-------|
| Current phase | A — awaiting gate |
| Started | 2026-08-03 |
| Closed | — |
| Promoted to /dev-flow | no |

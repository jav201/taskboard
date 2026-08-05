# Quick Spec — short content stays at the top

**Status:** phase C · **Base ref:** `e8dabba` · **Batch:** `2026-08-03-fastflow-01`
**Flow:** `2026.07.28-rev1` — 11/12 files hash-verified against
`~/.claude/docs/FLOW-VERSION.md`; the twelfth is a **stale manifest**, not local
drift (see premise P7).
**Route note:** invoked AFTER the fix was already implemented and committed
(`bd935ff`). Phases A and B are therefore written **retroactively**; the value
this run adds is the premise table, the close artifact and the backlog
reconciliation. Recorded rather than dressed up as a normal batch.

---

## 1. Objective

A view whose content is shorter than the viewport must draw its rows contiguously
from the top; only a day axis may sit at the bottom.

---

## 2. User stories

- As the board's owner, I want a half-empty kanban to read as a list that ended,
  **not** as a list with one task marooned at the bottom of the screen.
- As the board's owner, I want the lanes and the gantt to keep their day axis
  pinned to the bottom edge, because that axis is the ruler every row is read
  against.

---

## 3. Acceptance criteria (observable)

- [x] **AC1.** When a view is rendered with more height than content, the kanban
  and the agenda shall draw **no row below the blank pad**.
  → `tests/test_vertical_fill.py::test_no_row_is_stranded_below_the_blank_pad`
- [x] **AC2.** When the lanes or the gantt are rendered at any height, the **last
  row shall be non-blank**, and when those views pad, **exactly one** row shall
  sit below the pad.
  → `tests/test_vertical_fill.py::test_a_view_that_declares_an_axis_keeps_it_at_the_bottom`
- [x] **AC3.** When any view is rendered at height H, the output shall be
  **exactly H rows** — the fix may not be "stop padding".
  → `tests/test_vertical_fill.py::test_the_view_still_spends_the_whole_viewport`
- [x] **AC4.** When `fill_height` is mutated back to always-pin, **or** to
  never-pin, the suite shall turn **red** in both cases.
  → executed: 30 failed / 3 failed respectively (P4).

---

## 4. Validation strategy

Rendering-level tests over the four views × 2 kanban presentations × 5 heights ×
2 widths, asserting rows-after-the-first-blank. Plus a live sweep over the real
board (heights 14-80, four widths) as the discovery instrument. Both mutations of
the fix are executed to prove neither half of the law is vacuous. Evidence to
close: full suite green + both mutants dead.

---

## 5. Non-goals

- The lanes' own row allocator. It never pads (it spends the whole height), so it
  was never affected; measured clean at every swept size.
- The `today_cell` 44-vs-43 discrepancy in the lanes geometry — a separate open
  finding, carried to the backlog rather than fixed here.
- The flaky `test_win_clipboard_roundtrip` — pre-existing, carried.
- Bumping the stale `FLOW-VERSION.md` manifest — different repo, C-45 territory,
  carried.

---

## 6. Detected security flags

Scanned sections 1-4 against the pattern list. **No match.** The batch touches
vertical padding of already-rendered rows: no auth, secrets, integrations,
personal data, DB, input surface or network exposure.

- [ ] Auth / identity — [ ] Secrets / config — [ ] External integrations
- [ ] Sensitive data — [ ] Destructive DB — [ ] Input / attack surface
- [ ] Network / exposure

**`security_required`: false**

---

## 7. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| **P1** Before the fix, `fill_height` pinned the last row unconditionally | Premise | ✅ TRUE | `git show bd935ff^:taskboard/views.py` → line 482: `return lines[:-1] + [blank_line(w)] * pad + [lines[-1]]`, docstring line 477 asserts "the axis every view closes with" |
| **P2** Lanes and gantt close with an axis; kanban and agenda close with a task | Premise | ✅ TRUE | probe over the 4 views: lanes `'-34d today +81d'`, gantt `'-32d today'`, agenda `'▊ tarea 4 … ┃───●'`, kanban `'▊ tarea 4 │ │ │'` |
| **P3** The strand was reachable on the operator's real board | Premise | ✅ TRUE | sweep h=12..80 × w∈{80,100,120,160}: kanban 84 sizes, agenda 44 sizes; lanes 0 |
| **P4** Declaring the axis fixes the strand **without** unpinning the gantt | Hypothesis | ✅ TRUE | post-fix sweep: all 5 view/presentation combos `ok`; mutants `keep = 1 if len(lines) else 0` → 30 failed, `keep = 0` → 3 failed |
| **P5** The suite is green at the fix commit | Premise | ✅ TRUE | `python -m pytest -q` → `707 passed` |
| **P6** `.dev-flow/BACKLOG.md` is this project's canonical backlog | Premise | ✅ TRUE | `ls docs/engineering-rules.md` → absent, so no lane routing; `.dev-flow/BACKLOG.md` exists |
| **P7** The local flow is current | Premise | ✅ TRUE **with a finding** | 11/12 files match the manifest byte-for-byte. `dev-flow-lessons/SKILL.md` is 641 lines vs 620 recorded — because `f3d4fba` added **C-46** and is **already pushed** (0 unpushed). I am not behind; the **manifest** was never bumped, the exact failure `FLOW-VERSION.md` warns about. |

**Note on P2 and the report.** The operator named "lanes y kanban". Lanes measured
clean at every swept size. What occupies that seat in his reading is the
**agenda** (view `2`), which had the same defect. The report was right about the
symptom and one view off about the location — recorded because a premise taken
from a bug report is a **hypothesis**, not an axiom.

---

## 8. Batch status

| Field | Value |
|-------|-------|
| Current phase | C |
| Started | 2026-08-03 (retroactive: code landed at `bd935ff`) |
| Closed | `<pending final gate>` |
| Promoted to /dev-flow | no |
| Notes | Invoked after implementation; phases A/B written retroactively. |

---

## 9. Close (phase C)

### What changed

`fill_height` no longer infers which row is an axis from its position. Views that
close with one now say so (`to_text(..., pinned=1)` from the lanes and the
gantt); everything else pads below its content. The kanban and the agenda, which
close with a task, stop marooning their last row at the bottom of the viewport.

### How it was tested

- `tests/test_vertical_fill.py` — 61 cases: 4 views × 2 kanban presentations ×
  5 heights × 2 widths for AC1, plus AC2 and AC3.
- Both mutations executed: always-pin → 30 failed; never-pin → 3 failed.
- Full suite: **707 passed**.
- Live sweep over the real board before and after (84 + 44 stranded sizes → 0).

### Open risks / pending

1. **Lanes geometry off-by-one** — `lane_geometry` reports `today_cell = 44` while
   the rule is drawn at column 43, and `label_w + field_w + figs_w = 119` at
   width 120. Unresolved; may be deliberate compensation. → backlog.
2. **`FLOW-VERSION.md` is stale by one control** (C-46 landed, manifest not
   bumped). Different repo. → backlog.
3. **`test_win_clipboard_roundtrip` is flaky** — its restore step raises
   `PositionalParameterNotFound` and leaves the clipboard broken for the next
   run. Pre-existing. → backlog.

### Security flags — handling

`security_required: false`; nothing to handle.

### Suggested commit message

Already committed as `bd935ff` — *"Short content stays at the top; only an axis
sits at the bottom"*.

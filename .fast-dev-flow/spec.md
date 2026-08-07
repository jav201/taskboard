# Quick Spec — taskboard · lanes row cost model

| Field | Value |
|-------|-------|
| Batch id | `2026-08-06-fastflow-03` |
| Base ref | `fa821ae` (**local HEAD; NOT pushed** — `origin/main` = `f237cb3`, verified by `git ls-remote`) |
| Flow revision | `~/.claude/docs/FLOW-VERSION.md` declares `C-1 … C-45`; **C-46 landed unbumped** in the `claude-skills`/`claude-config` repos. Recorded, not chased — different repos. |
| Predecessor | `.dev-flow/2026-08-03-batch-03` — CLOSED AT PHASE 2, no code |
| Language | English |

---

## 1. Objective

Establish, execute and pin **one** row cost model for the lanes view — reconciling `swimlane_plan`'s
`h - 2 - (2 if active else 0)` with `lead_band`'s `prof + 2` — so that no later batch measures against
its own. **No visual change.**

---

## 2. User stories

- As the **operator**, I want the lanes view's row arithmetic stated once and guarded by a test, so
  that the next design batch spends rows instead of re-deriving what a row costs.
- As a **later agent**, I want the model's regime of validity written down, so that I do not report a
  measurement taken outside that regime as a defect (or a defect as normal).

---

## 3. THE COST MODEL — executed, not argued

All figures below come from `_probe_identity.py` / `_probe_cost.py`: **160 renders**, 5 boards
× 4 widths (72/96/120/200) × 8 heights (10/14/18/24/30/45/60/80), fixed `TODAY = 2026-07-30`,
boards built in-process (never reads a real board).

### 3.1 The two `2`s are different, and they compose

```
PANEL (h rows)                          BODY
  1   header                              lead    = prof + 2      [only when active]
  B   body rows                           stack_i = wrows + min(titles, nameable_i)
  A   absence line   A ∈ {0,1}            rest    = n_rest
  1   axis / scale row
  0   close  (bottom() returns "" — frameless, views.py:470-472)

ALLOCATOR CHARGE   need = prof + Σ(wrows + min(titles, o)) + n_rest
ROOM               room = h - 2 - 2·[active]     (views.py:2127)
```

- the `h - 2` is the **panel's own chrome**: header + axis (the close is empty).
- the `- 2·[active]` is **`lead_band`'s head + tail** — the two rows `prof` does not count.

### 3.2 The five invariants, and the regime they hold in

| id | invariant | in regime (n=124) | all renders (n=160) |
|----|-----------|-------------------|---------------------|
| I1 | `BODY == CHARGE + 2·[active]` | **124/124** | 128/160 |
| I2 | `CHARGE <= ROOM` | **124/124** | 156/160 |
| I3 | `BODY <= h - 2` | **124/124** | 156/160 |
| I5 | `0 blank rows` | **124/124** | 128/160 |
| I6 | `lead == prof + 2` | **124/124** | 160/160 |
| I7 | `2 + BODY + ABSENCE == h` | **124/124** | 124/160 |

**Regime = (a) the board has ≥1 active lane, and (b) the allocator found a feasible allocation.**
`lead_band` arity re-measured at `prof = 3, 5, 8, 12, 19, 33 → 5, 7, 10, 14, 21, 35`.

Also executed: `ABSENCE == 1 ⟺ BODY <= h-3 ⟺ slack == 1` — **124/124 agreement**, 48 of 124.
Rung four's `- 1` (`views.py:772`) is exactly what reserves that row.

### 3.3 The two off-regimes — both real, both previously unmeasured

**OFF-REGIME 1 — no active lane (32/160 renders).** Every project resting.
`prof` is **charged but never drawn** (`allrest` @ h=14: `room=12 charge=11 prof=9 CHARGED, lead=0
DRAWN, body=2`), and **the view pads**: 5 / 9 / 13 blank rows at h = 10 / 14 / 18. Rendered panel
verified line-by-line — rows 4-12 blank, axis correctly pinned at row 13.

> ⚠ **This falsifies a claim on disk.** `tests/test_vertical_fill.py:91` states *"the lanes never pad
> at all — their allocator spends the whole height it is given, so a pad-shaped assertion would be
> vacuous exactly there"*. That is the stated justification for the shape of a shipped test, and it
> is **false on an all-resting board**. The handoff's "Lanes NEVER pads, 0 blank rows at h=30/45/60"
> was measured only on boards with an active lane.

**OFF-REGIME 2 — allocator infeasible (4/160).** `huge` board @ h=10: no `(titles, prof, wrows)`
satisfies `need <= room`, so `allocate` returns its floor `(0, floor, 1)`, `charge=10 > room=6`, and
the renderer **sheds** blocks and prints `+N not shown`. Designed fallback; works.

### 3.4 Verdict

**There is no defect in the cost model.** `views.py:2127`'s subtraction and `lead_band`'s `prof + 2`
are the two halves of one correct identity; the closed batch's headline claim (#1, "the cost model
undercharges `prof`") is confirmed **FALSE** by execution, and so is its inverse. What is missing is
not a fix — it is a **written, guarded statement** of the model and of its regime.

---

## 4. Acceptance criteria (observable)

- [ ] **AC-1** — When the lanes view is rendered on a board with ≥1 active lane at a size where the
      allocator is feasible, `len(lead_band(...)) == prof + 2`, and the sum of the drawn blocks
      equals `allocate`'s charge plus 2.
- [ ] **AC-2** — When the same, the drawn body is `<= h - 2` and the rendered panel contains **0**
      blank rows.
- [ ] **AC-3** — When the same, `2 + body + absence == h` exactly.
- [ ] **AC-4** — When every project on the board is resting, the view renders with the axis last and
      **pads** — and the test states this as the known off-regime rather than asserting it away.
- [ ] **AC-5** — When `allocate` cannot fit any allocation, the render sheds and says `+N not shown`.
- [ ] **AC-6** — `taskboard/views.py` and `tests/test_vertical_fill.py` carry no prose asserting the
      lanes never pad, without its regime.
- [ ] **AC-7** — The whole existing suite stays green (**baseline: 707 passed**, executed at `fa821ae`).

---

## 5. C-40 — the mutation that reddens each criterion (EXECUTED)

Applied by monkeypatch; nothing on disk edited; baseline verified restored after each.

| mutation | what it simulates | reddens |
|---|---|---|
| **M1** `room = h-2` | the call site forgets to pay for the lead band | I3 (124), I5 (64), I7 (124) |
| **M2** `room = h-6` | the call site pays for the lead band twice | I5 (112), I7 (112) |
| **M3** `lead_band → prof+3` | the writer grows a row, charge unchanged | I1 (124), I3 (76), I5 (124), I6 (124), I7 (76) |
| **M4** rung four drops its `- 1` | no row reserved for the absence line | I3 (76), I5 (56), I7 (76) |
| **M5** `lead_band → prof+1` | the writer sheds a row, charge unchanged | I1 (124), I5 (48), I6 (124), I7 (48) |

**Every invariant is reddened by ≥1 mutation, and every mutation is caught by ≥1 invariant.**

> **A vacuity trap was found and must be encoded in the test.** Filtering the sample on
> `feasible = charge <= room` — a quantity *computed from the code under test* — makes **M1 and M4
> pass vacuously** (M1 leaves `n=0` in-sample; M4 leaves `n=48`). The exclusion of off-regime renders
> **must be static** (named fixture + height), never derived from the quantity being asserted.
> Measured both ways; the circular filter is what hid two of five mutations.

---

## 6. Premise table (C-43)

| Premise | Tier | Verdict | Executed evidence |
|---|---|---|---|
| `views.py:2127` passes `h - 2 - (2 if active else 0)` | premise | ✅ TRUE | source read `views.py:2125-2127` |
| `lead_band` draws `prof + 2`, constant | premise | ✅ TRUE | re-executed at prof=3,5,8,12,19,**33** → 5,7,10,14,21,35 |
| `bottom()` returns `""` (frameless) | premise | ✅ TRUE | `views.py:470-472` |
| `fill_height` never truncates | premise | ✅ TRUE | `views.py:490-491` returns `lines` when `len >= height` |
| The two `2`s compose to one correct identity | hypothesis | ✅ TRUE | I1/I2/I3 124/124 in regime |
| "The cost model undercharges `prof`" (batch-03 #1) | hypothesis | ❌ **FALSE** | I1 124/124; charge+2 == body exactly |
| Lanes NEVER pads (0 blank rows) | axiom (shipped law) | ❌ **FALSE — INCOMPLETE** | all-resting board pads 5/9/13 rows at h=10/14/18; law needs its regime, `tests/test_vertical_fill.py:91` |
| Occupancy 72.3 / 80.9 / 83.8 % vs 45 % floor | premise | ⬜ **NOT RE-EXECUTED** | inherited from `.dev-flow/01-requirements.md`; not load-bearing for this batch |
| One extra row costs −0.17 ms | premise | ⬜ **NOT RE-EXECUTED** | inherited; no row is added by this batch |
| `titles` on the real board = 8 / 6 / 17 | premise | ⬜ **NOT RE-EXECUTED, DELIBERATELY** | reading the operator's real board is non-deterministic and a data leak into artifacts; fixtures used instead |
| `load_curve` has two callers | premise | ✅ TRUE | `taskboard/views.py:986`, `taskboard/report.py:137` |
| Base `HEAD == origin/main == fa821ae` | premise | ❌ **FALSE** | `git ls-remote origin main` → `f237cb3`; **`fa821ae` is committed but UNPUSHED** |
| Bench share is 90 % @ h=60 / 95 % @ h=120 | premise | ⚠ **RESTATED** | see §7 |
| Working tree clean at start | premise | ✅ TRUE | `git status --short` → only my 3 untracked probe files |
| Baseline suite green | premise | ✅ TRUE | `707 passed in 40.84s` |

---

## 7. The bench-share number, re-presented to the operator (O-3)

The operator ruled **O-3 (no share cap)** having been told the bench occupies **87 %** of the panel.
The postmortem corrected that to 90 % @ h=60 / 95 % @ h=120 — **and framed it as a consequence of the
proposed change.** Measurement says otherwise.

**On HEAD, today, with no change at all**, the lead's bench on a **calm board (one active lane)**:

| h | 10 | 14 | 18 | 24 | 30 | 45 | 60 | 80 |
|---|----|----|----|----|----|----|----|----|
| share | 70.0 % | 71.4 % | 77.8 % | 83.3 % | 86.7 % | 91.1 % | **93.3 %** | **95.0 %** |

Max share by board shape, HEAD: `calm` **95.0 %** · `typical` **73.8 %** · `huge` **44.4 %** ·
`busy` **41.2 %**. The driver is **how many active lanes exist**, not the pending change: with one
active lane there is no stack to compete for surplus, so the bench already absorbs it.

**The post-change share is `NOT MEASURED`** — that belongs to the batch that retires `wrows`.
What is measured is that the 90-95 % band **is already shipped behaviour on a calm board**, so
O-3's ruling was not made on a number the change would introduce.

---

## 8. Non-goals (OUT — do not grow this batch)

- **No visual change.** The wave does not move. No disclosure row. `_figures` untouched.
- No change to `allocate`'s search, its rungs, or the returned tuple's arity.
- No retirement of `wrows`; no touching `tests/test_spend.py:81 / :238 / :277`.
- O-4 (how the legend learns of the disclosure row) is not opened.
- The `FLOW-VERSION.md` C-46 bump — different repos, cannot be done from here.
- Pushing `fa821ae`, or anything else. **The operator merges and pushes.**

---

## 9. Proposed change set (Phase B, ≤5 files — for approval, NOT yet implemented)

| # | file | change | kind |
|---|------|--------|------|
| 1 | `tests/test_row_cost.py` **(new)** | the pinning test: I1/I2/I3/I5/I6/I7 over the static fixture×size matrix, plus the two off-regimes asserted as themselves (AC-1…AC-5). Static exclusion only. | test |
| 2 | `taskboard/views.py` | docstring of `allocate` and `swimlane_plan` gains the model + its regime. **Prose only — zero behaviour change.** | doc |
| 3 | `tests/test_vertical_fill.py` | line 91's false claim corrected to state the regime (AC-6). Assertions untouched. | doc |
| 4 | `.dev-flow/BACKLOG.md` | reconcile (Phase C, mandatory) | doc |

**Recommendation: implement 1-3 as a single increment.** It is one idea, the only executable
artifact is #1, and #2/#3 are the prose that #1 makes true.

---

## 10. Open questions for the operator

1. **The all-resting pad (§3.3).** Three options: **(a)** document the regime and let the pad stand
   — the view genuinely has 2 rows of content, and the axis pins correctly; **(b)** stop charging
   `prof` when there is no active lane (a real behaviour change, out of this batch's "no visual
   change" scope); **(c)** log it to the backlog untouched. **I recommend (a) + (c).**
2. **`fa821ae` is unpushed.** The handoff believed it was on `origin/main`. Push is his call.
3. **Does the bench-share restatement (§7) change the O-3 ruling?** It should not — the number is
   pre-existing rather than change-induced — but he ruled on 87 % and is owed the corrected figure.

---

## 11. Detected security flags

- [ ] Auth / identity · [ ] Secrets / config · [ ] External integrations · [ ] Sensitive data
- [ ] Destructive DB · [ ] Input / attack surface · [ ] Network / exposure

**`security_required`: `false`** — the batch adds one test file and edits two docstrings. No auth,
no secrets, no integration, no new input surface, no persistence change. (Same finding as batch-03,
re-derived rather than inherited.)

---

## 12. Batch status

| Field | Value |
|-------|-------|
| Current phase | **C — closed, awaiting the operator's merge** |
| Started | 2026-08-06 |
| Closed | 2026-08-06 |
| Promoted to /dev-flow | no |
| Base ref | moved twice mid-batch: `fa821ae` → `6b7c4c3` (pushed) → `3b0f011`. `taskboard/` and `tests/` are **byte-identical across the move** (`git diff --stat fa821ae 3b0f011 -- taskboard tests` is empty), so every Phase-A measurement stands. |

### Gate rulings (operator, 2026-08-06)

| # | question | ruling |
|---|---|---|
| 1 | the all-resting pad | **document the regime, do not change behaviour** |
| 2 | `fa821ae` unpushed | amended + pushed by the operator; artifacts must never carry his board data |
| 3 | bench share vs O-3 | **O-3 stands** — no share cap, after both corrections |

---

## 13. Close

### What changed

`taskboard/views.py` gains the row cost model in the docstrings of `allocate` (the charge, and
that it is only half the model) and `swimlane_plan` (the whole identity, the two different `2`s,
and the regime). **Prose only — proven by comparing the module's AST with every docstring
stripped, before and after: identical.** `tests/test_row_cost.py` is new and pins the model with
18 tests. `tests/test_vertical_fill.py` loses a false sentence: *"the lanes never pad at all"* now
carries the clause that makes it true.

### How it was tested

- `tests/test_row_cost.py` — **18 passed**. Laws L1–L7b in regime (124 cells), L8/L9 off-regime.
- **Full suite: 707 → 725 passed.** The delta is exactly the 18 new tests; no existing test
  changed its result.
- **Mutation testing, C-40, executed on the real source** (`.fast-dev-flow/probes/_mutate_check.py`):
  all 5 mutations killed, `views.py` restored byte-identical and re-verified green.

| mutation | result |
|---|---|
| `room = h-2` — call site never pays for the lead band | **6 failed** |
| `room = h-6` — call site pays twice | **2 failed** |
| `lead_band` draws one row more | **7 failed** |
| `lead_band` draws one row fewer | **5 failed** |
| rung four drops its `- 1` | **1 failed** |

- Prose claims verified by execution, not assertion: `blank == h - 3 - n_rest` on all-resting
  boards, checked across 5 lane counts × 4 widths × 8 heights before it was written down.

### Open risks / pending

- **`prof` is billed for a bench nothing draws when no lane is active.** Left deliberately; a fix
  is a behaviour change. Carried in `.dev-flow/BACKLOG.md`.
- `project_wave` still has no direct test guard.
- **`~/.claude/docs/FLOW-VERSION.md` is stale by one control (C-46)** — different repos, not
  fixable from here. Recorded, not chased.
- **Candidate control for `dev-flow-lessons`** (not yet pushed upstream, different repo): *an
  exclusion predicate computed from the code under test is a vacuous check wearing a filter's
  clothes.* Measured here: it hid 2 of 5 mutations, one of them by emptying the sample entirely.

### Security flags — handling

`security_required: false`, re-derived rather than inherited. Nothing in the change set touches
auth, secrets, integrations, persistence or input surface: one new test file and two docstrings.

### Suggested commit message

```
The lanes cost model is one model, and it says which two rows it does not bill

`swimlane_plan` hands the allocator `h - 2 - (2 if active else 0)` and
`lead_band` draws `prof + 2`. Both were true, neither was written down beside
the other, and the batch that tried to spend those rows closed at Phase 2
without code because every reviewer measured against a model of their own.

There was no defect. The two are halves of one identity, and this pins it:
BODY == need + 2*[active], 2 + BODY + ABSENCE == h, exact on 124 cells. The
two `2`s are different -- `h - 2` is the panel's chrome, `- 2*[active]` is the
lead band's head and tail -- which is precisely what a reader collapsing them
gets wrong, in whichever direction they collapsed.

Also retires a false sentence. "The lanes never pad at all" holds only while a
project is active; on an all-resting board the bench is billed, never drawn,
and the view pads exactly `h - 3 - n_rest`. The regime is now stated wherever
the claim is made. Behaviour is unchanged -- the views.py diff is two
docstrings, and the AST with docstrings stripped is identical.

707 -> 725 tests. Five mutations of the real source, all killed.
```

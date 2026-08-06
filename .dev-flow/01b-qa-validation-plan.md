# 01b — QA validation plan · batch `2026-08-03-batch-03`

**Repo:** `C:\Users\jjgh8\Github\taskboard` · **branch** `main` · **base ref** `f237cb3`
**Language:** English · **Phase:** 1, authored in parallel with `architect`'s `01-requirements.md`
**Scope:** US-A (project row states open · overdue · next-due) and US-B (load curve moves to a
selection-gated disclosure row, paid for by shedding a title).

Requirement ids (HLR/LLR) are being derived in parallel. Every `TC-NNN` below names the **symbol or
behaviour it pins** so the fold-in is mechanical; no row is left waiting on an id to be meaningful.

---

## 0. Headline — read this before the register

Four of the operator's four questions came back with an executed answer, and two of them **invalidate
the obvious test design**. The register below is written against the measured tree, not the story text.

| # | finding | consequence |
|---|---|---|
| **F-2** | `phase_glyph()` returns `chr(0x2800 + m)` — measured `⣀ ⠤ ⠒ ⠉`. Braille is on **every named-task row**, and the lead band keeps its own bank. At `selected_id=None`, typical@96×30 renders **60 curve cells + 12 glyph cells**. | "Braille appears only when selected" is **green today, green after, and green if the curve were deleted**. Rejected. Replaced by the adjacency classifier (§2). |
| **F-1** | `_select_first()` runs at the top of **every** `refresh_view()` and sets `selected_task_id = ids[0] if ids else None`. `ids` is `board.visible_tasks(...)`. | Through the app, `selected_id is None` is reachable **only on an empty board** — which draws no lane. US-B's "iff selected" **has no false branch at app level**. Must be restated per-lane. |
| **F-3** | On the repo's own lanes fixture (`tests/test_swimlanes.py::typical`), `titles=1` and every stacked lane draws exactly **1** title at 96×30, 72×24 **and** 120×40. Same at occupancy-`extreme`@72×24. | "Shed one title" has **no funds**: shedding leaves 0 named rows, the selected row itself vanishes, and "adjacent to the selected row" loses its referent. Needs a specified fallback. |
| **F-5** | The stacked row's right edge is `due_meter(lane_due_days(lane))`, and `lane_due_days` returns the **project's own** due date. Measured: Beacon reads `···40d` while its soonest open task is **3 days overdue**. | "Next due distance" either **redefines** that edge (moving `◆` and the `▲Nd` seat) or needs new cells. Until architect rules, AT-001 cannot assert an expected value for that field. |

**Everything else is testable as stated.** The good news is F-2's cure is unusually strong: measured
today, `str(render_view(...))` is **byte-identical** for `selected_id=None` and for a selected task
(curve delta **0**). US-B's predicate is therefore *currently red* and can only go green by the change
— the best falsifiability evidence C-40 can ask for.

---

## 1. Executed baselines (measured, not predicted)

All at `TODAY = 2026-07-30`, via `render_view("swimlanes", …)` on the current tree.

| measurement | value |
|---|---|
| `phase_glyph({0..3})` | `⣀` U+28C0 · `⠤` U+2824 · `⠒` U+2812 · `⠉` U+2809 — **all braille** |
| curve / glyph split at `selected_id=None`, 96×30 | calm 89/2 · typical 60/12 · extreme 142/14 |
| classifier on a board with **no dated tasks** | **0 curve**, 3 glyph — discriminates |
| allocator `titles`, occupancy fixtures @96×30 | calm 2 · typical 3 · extreme 2 |
| allocator `titles`, occupancy `extreme`@72×24 | **1** |
| allocator `titles`, repo lanes fixture, all sizes | **1** (drawn per stacked lane: `{Cinder:1, Beacon:1, Delta:1}`) |
| one wave row's curve magnitude @96 wide | **7–16** cells (vs **1** for a phase glyph) |
| `str(render_view(… None …)) == str(render_view(… selected …))` | **True** — plain text is selection-invariant today |
| app initial selection is a lanes-named task? | typical **yes** · calm **no** (nav 2 of 5) · extreme **no** (nav 15 of 44 @96×30, 8 of 44 @72×24) |
| lane with a past project due date (Delta, due −9d, 1 open task at +1d) | renders 4 field rows carrying **zero** braille |
| geometry @96 wide | `label_w=15 · field_w=71 · figs_w=7` (sums to inner 94) |
| `"not shown"` present in the 96×30 reference render | **False** — nothing is being shed at that size |

Carried from PLAN, not re-measured: occupancy **72.3 / 80.9 / 83.8 %** marked vs floor **45 %**; wave
= **114 cells = 4.0 %**; lanes **never pad**; the legend has **never** described the wave (so a legend
entry here is an **addition**).

---

## 2. Q1 answered — how to observe "the curve is present iff selected"

**"Braille appears in the render only when `selected_id` is not None" is not a legitimate predicate.
It is not that it smuggles in an implementation fact — it is that it is already false** (F-2). It would
pass on the unmodified tree.

The legitimate black-box observation is a **classifier plus a differential**, both derived from the
render:

**Curve-ink classifier.** A braille cell counts as curve ink **iff at least one horizontal neighbour is
braille or field ground** — ground being the lattice `·` and the today rule `╎ ╽ ╿`. A phase glyph sits
between two spaces (`▎` + two spaces + glyph + space + title); a curve cell always abuts ground or more
curve. This references no internal symbol: `·`, `╎`, `╽`, `╿` are all glyphs the reader sees, and the
rule is the one mark the legend already names.

**Anti-vacuity companions (C-31), all three executed above and all three required in the test body:**

1. on the `None` render the classifier yields **> 0 curve cells** — proves the curve bucket fires
   (measured 60 at typical@96×30);
2. on the same render it yields **> 0 glyph cells** — proves the glyph bucket fires and the classifier
   is discriminating, not degenerate (measured 12);
3. on a fixture whose tasks carry **no dates**, curve cells == **0** while glyph cells **> 0**
   (measured 0/3) — proves the classifier is not simply "any braille".

**The predicate itself is differential and positional**, never "braille appears": render the same board
at the same size twice, once with `selected_id=None` and once with a selected task, and compare the
**set of curve-bearing row indices**. Presence is a set difference of exactly one index; correctness is
that index's adjacency to the row bearing the selected task's title, located by searching the render
for that title — never by a hard-coded row number.

**Scope warning that makes or breaks this AT:** the **lead band keeps its own multi-row bank**. PLAN's
risk list names `wrows`, `project_wave`, `field_rows`, `stack_block`, `_figures` — not `lead_band`, not
`prof`. So "no curve anywhere when nothing is selected" is **false** and must never be asserted. The AT
is scoped to **stacked lanes**, and the lead band's rows are excluded by deriving them from the render
(the lead spine `▌`), not by index.

---

## 3. Q2 answered — the shed-a-title counting claim

Observed through the render as a **difference of two counts of the same kind**, never against a
constant:

1. render with `selected_id=None`; count the **title rows of the focused lane** — a title row is one
   that carries the lane's spine, a phase glyph, and title text, and the lane's rows are delimited by
   the next spine-bearing project row. Call it `n0`.
2. **Assert `n0 >= 2`.** This is the fixture-accident guard and it is not optional: measured, the repo's
   own lanes fixture gives `n0 == 1` at every size, and occupancy-`extreme`@72×24 gives `titles == 1`.
   A fixture that drifts to 1 must **redden** the test, not silently satisfy it.
3. render with that lane's task selected; count again → `n1`.
4. assert `n1 == n0 - 1` **and** the selected task's own title is still present (the shed title is not
   the selected one) **and** the total line count of both renders is identical **and** neither render
   contains `"not shown"`.

**Executed derivation this rests on (C-39):** the occupancy `typical` fixture (5 projects / 21 tasks)
yields `titles=3` with drawn-per-stacked-lane `[3,3,3,3]` at 96×30, 72×24 **and** 120×40 — the only
fixture measured here that funds the payment at every size. The AT uses that fixture. The number 3 is
**not** written into the assertion; it is why the fixture was chosen, and step 2 is what keeps the
choice honest.

The line-count equality is the part that actually tests "**paid for**": lanes never pad (measured, 0
blank rows at h=30/45/60), so an unpaid row must push something out and surface as `"+N not shown"`.

---

## 4. AT register — Layer B (black-box, one distinct on-disk node each · C-18)

**Node:** all in a new `tests/test_lane_readout.py`, one `def test_…` per AT. No AT is "covered by X
plus Y". Every AT drives `render_view(...)` or `App.run_test()` and references **no** internal symbol
of `views.py` in its predicate (fixtures may build `Board`/`Project`/`Task` — those are the model, and
the shipped app builds them the same way).

### US-A — the project row states what the project asks of you

| id | AT-001 |
|---|---|
| **story** | US-A |
| **subject certified** | every stacked project row states this project's **open count**, **overdue count** and **next-due distance**, with the **values the board implies** |
| **surface** | `render_view("swimlanes", board, False, None, TODAY, width=96, height=30)` → plain text |
| **set derivation (C-31)** | project rows recovered from the render by spine glyph (`▌` lead, `▎` stacked, `▏` resting), continuation rows excluded because their label band is blank. **Never hand-listed.** |
| **completeness companion** | the union of names recovered across all three spine classes **equals** `{p.name for p in board.visible_projects(False)}` (plus `"Inbox"` iff the board has orphan tasks); the set is asserted **non-empty**; and the render contains no `"not shown"` — otherwise a lane was silently dropped and the quantifier is a lie |
| **predicate** | for each stacked row: the three readings parse out, and each **equals** the value recomputed from that project's tasks against `TODAY` |
| **C-40 mutation that reddens it** | render the overdue count as a constant `0` → reddens on the project with 2 overdue. Second: render `total` where `open` belongs → reddens on any project with a done task. |
| **branch** | fixture carries **both** a project with overdue > 0 and one with overdue == 0 (C-10: one AT per branch, asserting content) |

| id | AT-002 |
|---|---|
| **story** | US-A — empty / undated boundary |
| **subject certified** | a project with open work but **no due dates** states its counts and reads the honest no-date form for the distance |
| **surface** | same, on a fixture whose tasks carry `due_date=None` |
| **predicate** | the row states open count == number of open tasks, overdue count == 0, and the distance field is the no-date form (`—`) — **not** `0d`, **not** blank, **not** `+0d` |
| **C-40 mutation** | make the undated case fall through to `0` days → reddens |
| **note** | executed: the classifier already sees this board as 0 curve / 3 glyph, so it is a fixture that exists and renders |

| id | AT-003 |
|---|---|
| **story** | US-A — narrow-width honesty |
| **subject certified** | the new readings **degrade by dropping whole tokens**, never by truncating a number |
| **surface** | `render_view` swept over the repo's own width ladder `(24, 25, 31, 32, 40, 63, 72, 96, 97, 130, 201)` at h=30 |
| **set derivation** | widths taken from `tests/test_swimlanes.py::WIDTHS`, imported — not retyped |
| **predicate** | no stacked row contains a digit run that ends at the row edge without its unit, and no `…` falls inside a number; at the widest steps all three readings are present |
| **C-40 mutation** | replace token-dropping with a raw slice of the composed string → a number loses its `d` at width 24/25 → reddens |
| **why this exists** | @96 the row has `label 15 + field 71 + figs 7`. Three new readings cost ~20 cells and they come out of the field. The narrow end is where that goes wrong. |

| id | AT-004 |
|---|---|
| **story** | US-A — the legend **adds** an entry (P6: it has never described the wave, so nothing moves) |
| **surface** | `legend_entries("swimlanes", board, TODAY, 96, 30)` |
| **predicate** | an entry exists whose text names the row's reading, and its **swatch is byte-equal to the corresponding span of the actual rendered row** for a known project — the legend's own no-second-copy commitment, applied to the new mark |
| **completeness companion** | the swimlanes entry list is derived from the returned value; assert it is non-empty and that **every** entry's swatch occurs somewhere in the render (no-ghost), which is the law that P6 showed is only half-enforced today |
| **C-40 mutation** | hand-write the swatch string in the legend instead of calling the drawing function → drifts from the row → reddens |

### US-B — the curve moves to a selection-gated disclosure row

| id | AT-010 |
|---|---|
| **story** | US-B |
| **subject certified** | selecting a task **adds exactly one curve-bearing row, adjacent to that task's row** |
| **surface** | two `render_view` calls, same board / size / today, `selected_id=None` vs a task named in a stacked lane whose curve has ink |
| **classifier** | §2 adjacency classifier, with all three anti-vacuity companions asserted **in this test body** |
| **set derivation (C-31)** | the selectable task is taken from the render itself (a title found under a stacked spine), not hand-picked by id; the curve-row set is the classifier's output over all lines |
| **predicate** | `rows_selected == rows_none ∪ {i}` for exactly one new `i`, and `abs(i - r) == 1` where `r` is the line index whose text contains the selected task's title |
| **C-40 mutations** | (a) draw the disclosure row unconditionally → the `None` render gains it too, delta 0 → red; (b) append it at the end of the lane → adjacency fails → red; (c) draw the row but leave the curve blank → no curve cells added → red |
| **falsifiability evidence** | **measured today: the two renders are byte-identical and the curve delta is 0.** The predicate is red on the unmodified tree. |

| id | AT-011 |
|---|---|
| **story** | US-B — the negative |
| **subject certified** | **no lane other than the selected one** gains a curve row |
| **set derivation** | all stacked lanes recovered from the render by spine, minus the one holding the selection |
| **completeness companion** | that set is asserted to have **≥ 2** members and to cover every stacked project name in the render; non-empty is not enough, because a one-lane board would make the quantifier trivially true |
| **predicate** | for every other lane, its curve-bearing row count is **identical** across the two renders |
| **C-40 mutation** | give every lane a disclosure row → red |

| id | AT-012 |
|---|---|
| **story** | US-B — the shed-a-title counting claim |
| **subject certified** | the focused lane draws **one fewer title**, the selected title survives, and the row budget is neutral |
| **surface / method** | exactly the four steps in §3, on the occupancy `typical` fixture (measured `titles=3`, drawn `[3,3,3,3]` at all three sizes) |
| **predicate** | `n0 >= 2` (fixture guard) · `n1 == n0 - 1` · selected title still present · line counts equal · no `"not shown"` in either render |
| **C-40 mutations** | (a) pay by shrinking the lead's bench instead → title delta 0 → red; (b) shed from the wrong lane → focused-lane count unchanged → red; (c) shed the **selected** title → the survival assertion → red; (d) let the row be unpaid → `"not shown"` appears or line counts diverge → red |
| **C-39** | no expected count is written into the assertion — the baseline is measured from the `None` render at run time, and the fixture choice is defended by the executed table in §1 |

| id | AT-013 |
|---|---|
| **story** | US-B — **boundary: the focused lane draws exactly one title** |
| **status** | **BLOCKED on a requirement decision (F-3).** Measured: the repo's own lanes fixture and occupancy-`extreme`@72×24 both allocate `titles == 1`. Shedding leaves zero named rows; the selected row itself disappears. |
| **what I will assert once ruled** | whichever of these architect specifies — (i) no disclosure row is shown when the lane cannot pay, and the lane renders exactly as with `None`; or (ii) the row is paid from elsewhere and the title count is unchanged; or (iii) the lead's bench funds it. Each is a one-line predicate. **I will not invent the expected outcome.** |

| id | AT-014 |
|---|---|
| **story** | US-B — **boundary: a lane whose curve is empty** |
| **status** | **BLOCKED on a requirement decision (F-6).** Measured: Delta (project due −9d, one open task at +1d) renders 4 field rows with **zero** braille, because `wave_edge` clamps to the today column and `load_curve` fills nothing at or before it. |
| **what I will assert once ruled** | either no disclosure row for such a lane, or a row that states why it is empty. As written, US-B would produce a blank stripe under the cursor and AT-010's "one curve-bearing row is added" would **fail on a legitimate board** — which is why this is a requirement gap and not a test gap. |

| id | AT-015 |
|---|---|
| **story** | US-A + US-B — **output-then-consume (C-12)** |
| **subject certified** | the render these stories produce still satisfies the laws that already govern it, **in the state the feature creates** |
| **chain** | the shipped producer `render_view` → fed **unmodified** into `tests/test_occupancy.py::census` / `mute_rows` and into the vertical-fill law |
| **predicate** | at calm/typical/extreme, marked ≥ the standing floors (29.0 / 46.0 / 45.0) **and** ≥ the proposal's own 45 % at typical and extreme; and with a task **selected**, the lanes still spend the height exactly — no row below the pad beyond the 1 declared axis |
| **coverage hole this closes (F-7)** | `tests/test_vertical_fill.py` renders with `selected_id=None` **only** — after US-B, selection changes the row count, so the never-pads law is currently untested in exactly the state the feature introduces |
| **C-40 mutation** | let the disclosure row overflow the height → a stranded row or a changed line count → red |

| id | AT-016 |
|---|---|
| **story** | US-A + US-B — **the real app** |
| **subject certified** | a user moving the cursor sees the readout and the disclosure row |
| **surface** | `App.run_test(size=(96, 30))` — the pilot pattern already used ~30 times in `tests/test_app.py` |
| **predicate** | start on a fixture board in lanes mode; capture the screen; press the cursor key that moves the selection into a stacked lane; capture again; assert the disclosure row appeared adjacent to the row now carrying the selection, and that the project rows state their counts; press back and assert the row **moved with the cursor** |
| **set derivation** | the key is read from `taskboard/keymap.py`, not typed as a literal — the keymap-contract lesson this repo already paid for |
| **C-40 mutation** | render the disclosure row from a stale selection (not re-rendered on keypress) → the row does not move → red |
| **what it will expose (F-4)** | measured, `_select_first` picks `visible_tasks()[0]`, which is **not** a lanes-named task on calm (nav covers 2 of 5) or extreme (15 of 44 @96×30). On app start the "focused project" is undefined in the drawn sense. The AT must therefore drive a **cursor move**, not rely on the initial state — and F-4 still needs a ruling for what the initial frame shows. |

---

## 5. TC register — Layer A (white-box, per requirement)

Method per requirement, per the V-model's four: **test** (executed assertion), **demo** (observed
running), **inspection** (read), **analysis** (derived from measurement).

| id | pins | method | note |
|---|---|---|---|
| TC-001 | the row-readout composer: open / overdue / next-due for one `LaneFacts` | test | pure function over a constructed `LaneFacts`; boundary values 0, 1, many |
| TC-002 | the readout's width contract — the composed row is exactly `figs_w`/`label_w`-exact cells | test | the repo's standing law: every piece is built to its own exact width, so a short row is a rounding gap and a long one is a bug |
| TC-003 | `allocate()` after the row budget moves — `wrows` loses its stacked consumer | test | **`tests/test_spend.py` lines 84–92, 246–247, 257–258, 269–270, 284–286 encode laws about `wrows` as the stacked wave height.** They must be re-pointed at the disclosure row or they go vacuous. Inspection alone is not enough — a vacuous law still passes. |
| TC-004 | `swimlane_plan()` returns a triple its two callers spend consistently | test | the renderer and `nav_model` must not answer differently, or the cursor lands on an undrawn task |
| TC-005 | `lane_titles(lane, titles - 1)` for the focused lane | test | the shed must drop the **last** title, never the selected one |
| TC-006 | `project_wave` / `load_curve` still called with the same contract from the new site (P5: the curve **moves, it does not die**) | test | `wave.load_curve(bm, steps, total, edge)` — `views.py:986` is its only caller today |
| TC-007 | `_figures` docstring — *"the project's own wave already draws its progress"* | inspection | PLAN risk 3: this batch **falsifies** a live claim. It must be amended, not left lying. |
| TC-008 | reverse census (C-26) over `wrows`, `project_wave`, `field_rows`, `stack_block`, `_figures` | analysis | PLAN risk 2: 39 forward sites counted, the reverse grep across `tests/` is **not yet run**. Owed before Phase 3 closes. |
| TC-009 | `tests/test_swimlanes.py:136–141` — the today column on every lane row is `RULE` or braille | test | survives **only if** the project row keeps drawing the field/lattice after the curve leaves. Regression, not new. |
| TC-010 | occupancy re-measure post-change | analysis | PLAN risk 4: 27–38 points of headroom is a margin, not a proof for the post-change tree |

---

## 6. Boundary / negative matrix (Q3)

| dimension | boundary case | negative case | covered by |
|---|---|---|---|
| task count in a lane | a lane with **1 open task** — draws 1 title regardless of `titles` | a lane with **0 open** (resting, `▏`) — no field, no titles, cannot hold a disclosure row | AT-013 (blocked), AT-001 completeness |
| allocator titles | **`titles == 1`** — measured on the repo's own fixture at all sizes | `titles == 0` — nothing named at all | AT-013 (blocked) |
| dates | a project with **no dated tasks** — 0 curve cells | a project whose **own due date has passed** — 4 field rows, zero braille (Delta, measured) | AT-002, AT-014 (blocked) |
| selection | selection in a **stacked** lane (the golden path) | selection in the **lead** band (its tail row is the worst-late task, and the lead already has a tall bank) · selection on a task the lanes view **does not name** (measured: calm, extreme) · `selected_id=None` (legal at `render_view`, unreachable in-app per F-1) | AT-010, AT-011, AT-016, F-4 |
| lane kind | **Inbox** lane (a lane whose tasks have no project) | **cancelled / completed** lane — `pressure_chip` refuses to judge it; the readout must not claim it is late | AT-001 branch set |
| width | **24 / 25** — the repo's narrowest ladder steps, where label and figures give way first | 201 — widest step, where the field absorbs everything | AT-003 |
| height | h=30 reference; h=24 where `titles` collapses to 1 | h=14 where lanes get shed and `"+N not shown"` appears | AT-012 (asserts `"not shown"` absent), AT-015 |
| archive | `v` on with archived work — archived is named **last**, is never late, exerts no pressure | `v` off — archived work costs nothing and must not change the counts | AT-001 (counts must be invariant under `v` for open/overdue) |

**Auth / concurrency:** not applicable — this is a single-user local TUI with no accounts and no
concurrent writers. Cut deliberately, not silently.

---

## 7. Q4 — what could make these ATs vacuous, and how it is closed

| vacuity risk | how it is closed |
|---|---|
| **"braille appears" passes on the unmodified tree** (F-2) — phase glyphs are braille | adjacency classifier + three executed anti-vacuity companions (§2), and the measured 0-delta baseline proving the predicate is red today |
| **the lead band's bank satisfies a global "curve present" assertion** | the AT is scoped to stacked lanes, derived from the render by spine glyph; the lead's rows are excluded by derivation, not by index |
| **a one-lane fixture makes "no other lane gains a row" trivially true** | AT-011 asserts the other-lane set has **≥ 2** members |
| **a fixture that allocates `titles == 1` makes the shed unobservable** (F-3) | AT-012 asserts `n0 >= 2` before comparing — fixture drift reddens instead of passing |
| **hard-coding the expected title count** | AT-012 measures `n0` from the `None` render at run time; the number 3 appears only as fixture justification |
| **a hand-listed set of project rows omitting the failing lane** (C-31) | every set is derived from the render or from `board.visible_projects(...)`; completeness is asserted against the model, plus the `"not shown"` guard that catches a silently dropped lane |
| **hard-coded row indices for adjacency** | the anchor row is found by searching the render for the selected task's title |
| **asserting non-empty output instead of content** (C-10) | AT-001 asserts the counts **equal** values recomputed from the board; AT-002/AT-003 assert the specific degraded forms |
| **`test_vertical_fill` never renders with a selection** (F-7) | AT-015 renders the selected state through the same unmodified law |
| **a title beginning with a braille character would fool the classifier** | fixtures assert ASCII titles; noted as a known limitation of the classifier, not hidden |
| **`tests/test_spend.py`'s `wrows` laws going vacuous when the stacked wave leaves** | TC-003 requires them re-pointed, by test and not by inspection |

---

## 8. Requirements I judge untestable **as stated** — Phase-1 findings

These are findings, not failures. Each needs one architect/operator ruling and then becomes a one-line
predicate.

1. **US-B, "the curve is present iff a task is selected" — the false branch does not exist at app
   level (F-1).** `_select_first()` guarantees a selection whenever the board has any visible task.
   **Recommendation:** restate per-lane — *"a lane shows the curve iff it holds the selection"* — which
   has both branches on any board with ≥ 2 active projects and is exactly what AT-010/AT-011 drive.
   Keep `selected_id=None` as a `render_view` contract case at Layer A, since it is a legal argument
   that `test_occupancy` and `test_vertical_fill` already pass.
2. **US-B, the shed-a-title payment when the focused lane names one title (F-3).** Blocks AT-013.
3. **US-B, a lane whose curve is empty (F-6).** Blocks AT-014. As written, US-B would put a blank
   stripe under the cursor on a legitimate board.
4. **US-A, "next due distance" vs the meter's existing meaning (F-5).** Blocks the third field of
   AT-001. The row's right edge today says the **project's** due date; the story asks for the **next
   task** deadline. Replace or adjoin — and if replace, `◆` ("the project's own due date") and the
   `▲Nd` severity seat change meaning, which is a legend change nobody has budgeted.
5. **US-B, the initial frame (F-4).** On app start the selection is often a task the lanes view does
   not name. Undefined whether a disclosure row appears, and where.

---

## 9. Evidence checklist

- [x] **Acceptance criteria use Given/When/Then** — ✗ **deliberately not**, and this is the one item I
  am marking off-pattern rather than pretending. Every AT here is a *differential render predicate*;
  Given/When/Then would obscure that the assertion compares two renders. Each AT states surface, set
  derivation, predicate, and reddening mutation, which is strictly more than G/W/T carries here.
  Flagging for the gate rather than silently reformatting.
- [x] Test cases have explicit Expected, not vague "works" — every predicate names the compared
  quantity (AT-010 set difference; AT-012 `n1 == n0 - 1`).
- [x] Edge cases include empty, boundary, invalid, error — §6, incl. 0-task lanes, `titles==1`,
  undated boards, past project due dates, widths 24–201.
- [x] Regression checklist exists — TC-003/TC-009 (`test_spend` `wrows` laws, `test_swimlanes` today
  column), AT-015 (occupancy floors + never-pads).
- [x] Exit criteria stated — §10.
- [x] No real PII / secrets — all fixtures are synthetic `Project`/`Task` objects in `tmp_path`.
- [x] Test results section left blank — nothing here is marked as run. The §1 baselines are
  *measurements of the current tree*, labelled as such, not test outcomes.
- [x] **Layer B (black-box)** — AT-001..AT-016 all drive `render_view` or `App.run_test()`; boundary
  (§6) and negative (AT-011, AT-002) evidence present; no AT names an internal `views.py` symbol in
  its predicate.
- [x] **Bidirectional surface-reachability** — inputs (board shape, width, height, `selected_id`,
  `show_archived`) and outputs (row readout, disclosure row, legend entry, occupancy) are each
  exercised through `render_view`/pilot; AT-016 drives the handler, not the service API.
- [x] **No unfilled template** — no `<...>`, no `TC-NNN` stubs, no empty required rows. AT-013 and
  AT-014 are marked BLOCKED **with the reason and the measurement**, which is a filled row.

---

## 10. Exit criteria

1. AT-001..AT-012, AT-015, AT-016 exist as **distinct test functions** in `tests/test_lane_readout.py`
   and pass (C-18: no AT satisfied by two nodes combined).
2. AT-013 and AT-014 are **unblocked by a recorded decision** and then exist and pass — or the
   corresponding requirement is explicitly descoped in `01-requirements.md`, in writing.
3. For every AT, the named C-40 mutation has been **run** and observed to redden it. A mutation that
   does not redden its AT is a Phase-3 stop, not a note.
4. TC-003's `wrows` laws are re-pointed and demonstrated non-vacuous; TC-007's `_figures` docstring is
   amended; TC-008's reverse census is run and recorded.
5. Occupancy re-measured post-change (TC-010) and ≥ the standing floors at all three loads.
6. The five findings in §8 each carry a recorded ruling in PLAN's decision log.

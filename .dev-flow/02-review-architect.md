# 02 — Phase-2 cross-review · `architect` (adversarial)

**Batch:** `2026-08-03-batch-03` · **Repo:** `C:\Users\jjgh8\Github\taskboard` · **Branch:** `main`
**Base ref verified at review:** `git log --oneline -1` → `f237cb3 Close the vertical-fill batch and reconcile a day-stale backlog` ✓ (tree clean apart from `.dev-flow/` + untracked `_prototypes/`)
**Reviewer stance:** I did not author these requirements. Everything below is checked against disk, not against the document's own citations.
**Artifacts reviewed:** `.dev-flow/01-requirements.md` (623 lines) · `.dev-flow/01b-qa-validation-plan.md` · `.dev-flow/2026-08-03-batch-03/PLAN.md`

**Verdict: DO NOT PASS THE GATE.** 7 blockers, 11 majors, 6 minors. Two of the blockers (B-1, B-3) mean US-B is **underivable as written** — not merely under-specified. The mandatory C-26 reverse census, run here for the first time, found the requirements' own census (§6.1) covers **2 of the 16 test files that render the lanes view**.

---

## 0. What I checked and what came back clean

Stated first so the blockers below are read against a fair baseline. These were adversarially verified and **passed**:

| Check | Result |
|---|---|
| **C-24** — does any byte-identity golden capture the lanes render? | ✅ **No.** No `*.golden`, no snapshot dir, no `read_text() ==` against a render. The three "byte-identical" hits (`test_palette_ration.py:135`, `test_report.py:4`, `test_span_economy.py:11`) are about *board JSON stability*, *the report not writing*, and *span-run counts* — none captures render bytes. The batch is free of golden-churn. |
| LLR-002.1's `need` expression vs disk | ✅ Disk `views.py:755` = `need = prof + sum(wrows + min(titles, o) for o in opens) + n_rest`. LLR-002.1's post-change form correctly preserves `+ n_rest`. Verified, not assumed. |
| `ceil = 10 if geo.large else 6` (`views.py:734`), `floor = geo.profile_rows` (`:727`) | ✅ DEFINED on disk at the cited lines. C-36 reconciliation holds. |
| P-13's claim `project_wave` / `stack_block` → **0 test files** | ✅ Confirmed by `grep -rc` across all of `tests/`. |
| `wrows` and `allocate` confined to `tests/test_spend.py` | ✅ Confirmed. 7 `allocate(` call sites at exactly `:89, :102, :234, :246, :257, :269, :284` — LLR-002.1's list is correct. |
| P-6's correction (`load_curve` has two callers) | ✅ Confirmed. `report.py:137` inside `_curve_svg`. **And the report is functionally safe**: `_curve_svg` builds its own `cols`/`steps`/`span`/`Bitmap(span,32)` and calls neither `project_wave`, `wave_edge`, `allocate` nor `swimlane_plan`. Nothing in the batch can break it. See M-9 for the documentation consequence. |
| `test_swimlanes.py:224` (lead-bench braille bound) | ✅ Survives. It slices `out[head+1:head+1+prof]` using the **allocator's** `prof`, so a bench growing 8→19→33 keeps the slice correct; `lead_band(prof=33)` returning 35 rows means the slice never overruns. Only its arity unpack at `:208` breaks. |

---

## 1. THE C-26 REVERSE CENSUS (this phase's owed item — run here)

Method: `grep -rn <symbol> tests/` over the **whole** tree, then every hit read and re-validated **independent of which requirement claims to own it**. `__pycache__` excluded.

### 1.1 Symbol × test file × verdict

| Symbol | Test file(s) touching it | Sites | Verdict | Evidence |
|---|---|---|---|---|
| `wrows` | `tests/test_spend.py` **only** | `:84, :89, :91, :92, :102, :234, :235, :246, :247, :257, :258, :269, :270, :284, :285, :286` (16 lines / 7 unpack sites) | **BREAKS — signature.** 3 tests superseded, 3 retargeted, 1 (`:98`) **goes vacuous** (see B-6) | line-level grep |
| `allocate` | `tests/test_spend.py` **only** | `:28` (import) + 7 call sites | **BREAKS — signature** | grep |
| `swimlane_plan` | `tests/test_swimlanes.py` **only** | `:207, :208, :436, :439, :440` | **PARTIAL BREAK.** Only `:208` unpacks (`_l,_g,_t,prof,_w` = **five** values). `:439`/`:440` bind whole tuples and index `[1][2][3]` — **survive untouched** | `sed -n '200,215p'`, `'430,450p'` |
| `field_rows` | `tests/test_field.py` | `:11, :93, :140, :153, :162, :174, :187` | **SURVIVES** — called directly with its own `Bitmap`, independent of lanes | grep |
| `_figures` | `tests/test_swimlanes.py` | `:544, :555` | **SURVIVES** — behaviour unchanged (D-text goes in the *field*, not the right edge; C4 preserved). Docstring-only change | `sed -n '540,560p'` |
| `stack_block` | **0 test files** | — | **NO DIRECT GUARD.** Coverage is entirely indirect via rendered output | `grep -rc` returns nothing |
| `project_wave` | **0 test files** | — | **NO DIRECT GUARD.** Same | `grep -rc` returns nothing |
| `lane_titles` | `tests/test_swimlanes.py` | `:19` (import only) | **SURVIVES** — imported, never called in an assertion. Weaker than §6.1 implies | grep |
| `legend_entries` | `tests/test_legend.py` (11), `tests/test_archive.py` (6) | 17 lines | **SURVIVES iff** the new param is keyword-with-`None`-default (LLR-004.2). Note: 17 lines, not the "8 call sites" §6.1 claims — the extra are imports/asserts | grep |
| `load_curve` | `tests/test_wave.py` | `:12, :58, :168, :187, :196, :208, :217` | **SURVIVES** — not edited | grep |
| `lead_band` | **0 test files** | — | **NO DIRECT GUARD** — and LLR-002.5 declares it touched ("newly exercised at bench heights it has never been rendered at"). **Absent from §6.1's census table entirely** (M-10) | `grep -rc` returns nothing |

### 1.2 The part the requirements' census does not reach

`grep -rln swimlanes tests/` returns **16 files**. §6.1's predicted-red set names **2**. The other 14 render the lanes view and were never re-validated. Re-validated here:

| File | What it observes | Verdict |
|---|---|---|
| `tests/test_prism_laws.py:128` `test_every_lit_field_cell_carries_a_declared_hue` | every coloured span in the swimlanes render vs `HEX.values()` | **AT RISK — goes red** if the new D-text is painted in any hue outside the declared set. Unnamed by any requirement (M-1) |
| `tests/test_prism_laws.py:147` `test_no_row_mixes_two_identity_hues_in_its_field` | per-row identity hues over spans intersecting `FIELD_GLYPHS` (all braille) | **GOES NEAR-VACUOUS.** Renders at `selected_id=None`, so post-change **only the lead band** contributes braille. Its own guard `assert per_row, "vacuous: …"` is satisfied by the lead alone and **cannot detect the collapse** (M-2) |
| `tests/test_palette_ration.py:276` | `marks["swimlanes"] == [(HEX["ink"], "!1")]` — **exact list equality** over marks starting `!` | **SURVIVES ONLY BY LUCK.** LLR-001.1 marks the `over` literal "NEW — created in Phase 3". If Phase 3 renders it `!2` instead of `2 over`, this hard equality goes red (M-3) |
| `tests/test_span_economy.py` | run/span counts over `render_view` for all 4 views incl. swimlanes | **AT RISK** — removing 114 braille cells and adding ~20 text cells per row changes the run profile. Not re-validated by the batch |
| `tests/test_swimlanes.py:136–141` | today column is `RULE_PHASES` or braille on every lane row | **SURVIVES** — correctly claimed by LLR-001.3/C3. This is the one the requirements got right |
| `tests/test_occupancy.py`, `tests/test_vertical_fill.py` | occupancy floors, never-pads | **SURVIVE** as laws; re-measure owed (R-4). QA's F-7 correctly notes `test_vertical_fill` renders `selected_id=None` only |
| `tests/test_momentum.py:113,128,164`, `tests/test_motion.py:39,44`, `tests/test_cells.py:39`, `tests/test_app.py`, `tests/test_archive.py`, `tests/test_emoji_picker.py`, `tests/test_keymap.py`, `tests/test_report.py` | render lanes for unrelated properties | **PROBABLY SURVIVE** — no wave/row-count dependence found. Recorded as swept, not as guaranteed |

### 1.3 C-14 — tests observing an artifact whose shape changes

The changing artifact is **the lanes render** (row composition + row count + span profile). Observers: `test_span_economy.py`, `test_prism_laws.py`, `test_palette_ration.py`, `test_occupancy.py`, `test_vertical_fill.py`, plus the two named files. **The requirements name two of seven.** The HTML report (`report.py`) is a second artifact but is provably decoupled (§0).

---

## 2. O-1 (silent refusal) — **NOT specified totally**

The ruling itself is DECIDED and I do not reopen it. Testing its consequences:

### 2.1 States that reach the refusal — enumerated, vs LLR-003.3's coverage

| # | State | Covered? |
|---|---|---|
| 1 | `titles==1`, the lane's single drawn title **is** the selection | ✅ LLR-003.3 clause 1 (correctly phrased on *drawn* count, not on `titles` — so a lane with `titles=3` but only 1 open task is also caught) |
| 2 | Selection is in the **lead** lane | ✅ clause 2 |
| 3 | Selection is in a **resting** lane | ✅ clause 3 |
| 4 | Selection's project **shed off-screen** (`+N not shown`) | ✅ clause 4 |
| 5 | `selected_id is None` | ✅ HLR-003's negative limb |
| 6 | **Selection's lane draws a curve with ZERO ink** (QA F-6: Delta, project due −9d, 4 field rows, 0 braille — *measured*) | ❌ **NOT COVERED — blocker B-3** |
| 7 | **The Inbox pseudo-lane** (tasks with no project) holds the selection | ❌ **NOT COVERED.** QA §6 names Inbox as a lane kind; no requirement says whether it is a stacked lane, whether it has a hue for LLR-003.6, or whether it has a `total` for the curve's normalisation |
| 8 | Selection is an **archived** title (`show_archived` on) — `lane_titles` order is `dated + undated + archived` | ❌ **NOT COVERED.** LLR-003.2 sheds "the last not-selected", which with archived work present is an archived title. Whether that is the intended victim is unstated |
| 9 | Lane draws ≥2 titles but the **selected task is not among them** (measured by QA F-4: nav covers 2 of 5 on calm, 15 of 44 on extreme) | ⚠️ **Covered arithmetically, broken semantically.** HLR-003 fires (project drawn, sheddable title exists), so the curve appears — **next to a row the cursor is not on**. US-B's whole premise ("where I am already looking") fails in this state. Unstated. |

**Verdict: O-1's refusal is specified for 4 of 9 reachable states.** States 6, 7, 8 are gaps; state 9 is a silent semantic inversion.

### 2.2 Does anything elsewhere assert the curve appears unconditionally? — **YES**

Three sites, and one of them is an acceptance definition:

1. **§2.6, US-B Evaluability (T):** *"When the owner selects a task belonging to a drawn stacked project, the owner observes one new row directly under that project's row carrying braille curve glyphs"* → **`AT-003`**. No sheddability condition. On the calm board (`titles=1`, measured 5/5 regimes) this **fails**. This is the *definition of US-B's acceptance test* contradicting LLR-003.3. → **B-1**
2. **§2.2 Product function 3:** *"While a task is selected, a disclosure row under its project's row draws that project's cumulative load curve."* Unconditional. → **B-1**
3. **HLR-003 Acceptance → Observable outcome:** *"Selecting a task makes one new row of braille curve glyphs appear directly under its project's row."* Unconditional in the outcome line; the refusal appears only later in the boundary catalog. → **B-1**

HLR-003's **Statement** and HLR-004's **Statement** are both correctly conditioned. The contradiction is entirely in the acceptance/description layer — which is the layer the black-box chain is built on, so it is not cosmetic.

---

## 3. O-2 (supersede `tests/test_spend.py:277`) — **NOT scoped; it takes neighbours**

The ruling is DECIDED. Testing its blast radius:

**The ruling names exactly one law.** The requirement set supersedes **three** and mis-classifies a fourth:

| Test | §6.1 verdict | My verdict (executed) |
|---|---|---|
| `:277` `test_the_calm_board_buys_RESOLUTION_and_not_just_a_taller_hero` | Supersede | ✅ **Agreed** — this is O-2's named subject |
| `:81` `test_the_field_never_grows_while_a_task_is_unnamed` (THE PROHIBITION) | Supersede | ⚠️ **Defensible but outside the ruling.** Intent preserved (`titles` unchanged 12/12). Needs its own ruling, not O-2's |
| `:238` `test_the_lead_is_still_the_hero_when_the_wave_may_grow` (`assert wrows < prof`) | Supersede | 🚨 **BLOCKER B-5.** This is **the only existing upper bound on `prof`**. Retiring it at exactly the moment `prof` becomes unbounded (8→19 @96×30, 10→33 @96×44 — the document's own executed figures) removes the guard against the precise outcome O-2 makes possible. O-2 authorises superseding a law about *where surplus goes*; it does not authorise retiring the *ceiling on the hero* |
| `:98` `test_when_naming_is_exhausted_the_cells_buy_resolution` | **"Retarget — assertions survive verbatim"** | 🚨 **BLOCKER B-6 — WRONG.** Executed post-change simulation: `allocate(lane_geometry(96,30), [2,1], 0, 30)` → `titles=2, prof=24`, `profile_rows=4`, so `prof > geo.profile_rows` is `24 > 4` → **green**. But green *for the opposite reason*: post-change nothing buys "the extra field" — rung four dumps surplus into `prof` unconditionally. The docstring *"the allocator DOES take the extra field"* becomes **false**, and the assertion loses all power against the failure it was written for. Correct verdict: **goes vacuous**, not "retarget" |
| `:250` `test_rung_four_never_outbids_a_rung_above_it` | Retarget, rewrite to `prof + 1 + min(titles,2) <= 26-1` | ⚠️ **Survives with ZERO margin.** Executed: post-change `allocate(geo,[2],0,26)` → `titles=2, prof=22`; rewritten LHS = `22+1+2 = 25 <= 25` → passes **exactly at the bound**. Any drift reddens it. Not stated anywhere (M-7) |
| `:234` `test_naming_is_never_capped_below_what_a_lane_holds` | Retarget | ✅ Agreed — pure unpack change, `titles >= 8` survives |

**Count contradiction:** §6.1's header says *"the **four** laws"*, the table lists **six** rows, HLR-002's rationale says *"supersedes **three** shipped laws"*. Three different numbers for the same set (M-5).

**Verdict: O-2's supersession is NOT scoped.** It silently carries `:81` and `:238`, and `:98` is mis-verdicted on evidence the document never executed.

---

## 4. Findings

### BLOCKERS

**B-1 — US-B's acceptance definition contradicts O-1.**
§2.6 US-B Evaluability (→`AT-003`), §2.2 function 3, and HLR-003's "Observable outcome" all assert the curve appears whenever a task in a drawn stacked project is selected. LLR-003.3 says it sometimes silently does not. Per this phase's own blocker rule, an unconditional assertion of "the curve appears on selection" alongside a silent refusal is a blocker. **`AT-003` as defined would fail on the calm board — the board O-1 exists for.**
*Fix direction:* re-state all three with the sheddability precondition; move the calm-board case to `AT-004` explicitly.

**B-2 — `AT-NNN` id collision between the two Phase-1 artifacts.**
`01-requirements.md` §5.2 defines `AT-001`…`AT-006`. `01b-qa-validation-plan.md` §4 defines `AT-001`…`AT-004` + `AT-010`…`AT-016` with **different subjects for the same ids**: requirements `AT-003` = "disclosure present-iff-selected", QA `AT-003` = "narrow-width honesty"; requirements `AT-004` = "the refusal classes", QA `AT-004` = "the legend adds an entry". The behavioural traceability chain in §5.2 therefore points at ids that mean something else in the artifact that will implement them. **The two-layer traceability requirement is not satisfied.**

**B-3 — F-6 is unresolved and makes HLR-003 self-contradictory (US-B underivable as written).**
QA measured a legitimate lane (Delta: project due −9d, 1 open task at +1d) rendering **4 field rows with zero braille**, because `wave_edge` clamps to the today column. On such a lane:
- HLR-003 **mandates** drawing the disclosure row (project is drawn, has a sheddable title);
- LLR-003.5's numeric threshold **requires ≥4 distinct braille glyphs** on that row;
- the row will contain **none**.

The result is a blank stripe under the cursor, paid for by shedding a real named task. `AT-014` remains BLOCKED, and the QA plan's exit criterion 2 cannot be met. **Not a test gap — a requirement gap.** LLR-003.3's refusal enumeration must gain a fifth clause (empty curve → refuse), or LLR-003.5's threshold must be restated as conditional, or a "nothing to draw" register must be specified.

**B-4 — HLR-005's pass threshold provably cannot detect the false claims the batch creates.**
Statement: *"the repository **shall** contain no docstring or comment asserting that a stacked project's own row draws its wave or its progress."* Threshold: `grep -rn "own wave"` → **3 → 0**.

Executed on disk, the batch falsifies **at least four more sites that grep does not match**:

| Site | Text | Caught by `"own wave"`? |
|---|---|---|
| `taskboard/views.py:720` | `"""(titles per stacked project, rows for the lead's bench, **wave rows each**)."""` | ❌ |
| `taskboard/views.py:724–725` | *"toward a taller LEAD before **taller stack waves** — five equal waves would be a tie of near-equals"* | ❌ |
| `taskboard/views.py:750–752` | *"THE LEAD STAYS THE HERO: **a stack wave may never reach the lead's own bench**"* | ❌ |
| `taskboard/views.py:2112` | `"""(lanes ranked, geometry, titles, lead rows, **wave rows**) — the single answer` | ❌ |
| `tests/test_spend.py:84` / `:98` docstrings | *"`wrows` must still be 1"* / *"the allocator DOES take the extra field"* | ❌ |
| `views.py:903`, `views.py:1100`, `tests/test_swimlanes.py:164` | *"own wave"* | ✅ (the 3 named) |

`views.py:720` and `views.py:2112` are the **return-value contracts of the two functions this batch re-signs**. HLR-005 will report `3 → 0` and PASS while leaving them lying. **Requirement and its own verification disagree.**

**B-5 — O-2's supersession silently retires the only ceiling on `prof`.** See §3. `test_spend.py:238`'s `assert wrows < prof` is superseded under a ruling that named `:277` only, at exactly the moment `prof` grows 10→33 on a 44-row panel. Requires its own operator ruling.

**B-6 — `test_spend.py:98` mis-classified "Retarget"; executed evidence says it goes vacuous.** See §3 table. The C-26 verdict set (survives / needs updating / goes vacuous) has no "vacuous" row in §6.1 at all — the census cannot express the failure mode it most needs to.

**B-7 — §5's functional traceability chain is empty at gate time.** Every `TC-NNN` cell in §5.2's functional table reads *(qa-reviewer)*, and §5.1/§5.3 are unfilled. The authorship split (§ preamble) is legitimate, but the gate rule requires **BOTH** chains to exist. As delivered, US→HLR→LLR→TC terminates at LLR. The QA plan supplies `TC-001`…`TC-010` but **maps them to symbols, not to LLR ids** — so the join is manual and, given B-2, ambiguous.

### MAJORS

**M-1 — The §6.1 census covers 2 of 16 files that render the lanes view.** §1.2 above. It is labelled "change-first, per the census-completeness principle", but change-first over *edited files* misses tests that observe the *artifact* those files produce. The `assumed — verify in Phase 2` flag on `test_prism_laws.py` / `test_requirements.py` is discharged here — and it found two real hits.

**M-2 — `test_prism_laws.py:147`'s anti-vacuity guard cannot detect its own collapse.** Post-change, at `selected_id=None`, only the lead band contributes braille; `assert per_row` passes on the lead alone. The law's coverage silently drops from all lanes to one.

**M-3 — `test_palette_ration.py:276` is a hard equality hostage to a literal LLR-001.1 leaves free.** `marks["swimlanes"] == [(HEX["ink"], "!1")]` filters marks starting `!`. LLR-001.1 declares the `over` literal "NEW — created in Phase 3". Phase 3 choosing `!2` reddens an unnamed shipped law. The requirement must pin the token shape, or name this file.

**M-4 — LLR-002.2 misstates which sites break.** It says *"only its unpacking neighbours at `:208` and `:439` need touching"*. Disk: `:439` is `short = swimlane_plan(...)` — a whole-tuple bind, no unpack, **survives**. `:208` is the only unpack site (and it unpacks **five**, confirming the pre-state). Minor factual error in a C-26 declaration, which is the wrong place for one.

**M-5 — Three different counts for the superseded set** (§6.1 header "four" / table six rows / HLR-002 "three").

**M-6 — LLR-001.2 and LLR-001.3 do not specify how the D-text and `field_rows`' output compose.** LLR-001.2 says the row is built from an **empty** bitmap and rendered by `field_rows` (which returns per-cell-coloured markup); LLR-001.3 says the text is placed in the field right of the today rule. Nothing says whether the text **overwrites** field cells, is **composited** into the markup, or replaces the field slice — and each choice has a different consequence for `test_prism_laws.py:128` (declared hues) and `test_span_economy.py` (run counts). This is the single most consequential unstated mechanism in the batch.

**M-7 — `test_spend.py:250`'s retarget passes with zero margin.** Executed: `22 + 1 + 2 = 25 <= 25`. Stated nowhere; a future `profile_rows` or `ceil` change reddens it without warning.

**M-8 — O-1 totality gaps: Inbox lane, archived-title shed, cursor-on-undrawn-task.** §2.1 states 6, 7, 8, 9.

**M-9 — HLR-005's "the repository shall" contradicts §1.2's `report.py` carve-out.** `report.py:119`'s docstring — *"One engine, two rasterisers — so the document cannot describe a shape the app stopped drawing"* — becomes materially false, not merely narrowed as R-6 claims: post-change the report draws a curve for **every** project unconditionally while the app draws it for **at most one**, and only while selected. Either HLR-005's quantifier is scoped to `views.py`/`tests/` in writing, or `report.py:119` is in scope.

**M-10 — `lead_band` and `tests/test_occupancy.py::census` are declared touched (LLR-002.5) but absent from the §6.1 census.** C-26 requires declared → reverse-grepped. `lead_band` reverse-greps to **0 test files** — which is itself the finding: the function about to be rendered at 3× its historical height has no direct guard.

**M-11 — `swimlane_plan`'s docstring (`views.py:2112`) is a return-contract that LLR-002.2 changes and no requirement amends.** Same class as B-4 but attributable to LLR-002.2 specifically, which lists edited line ranges without including `:2112`.

### MINORS

- **m-1** — §6.1 says `legend_entries` has "8 call sites" in tests; grep returns 17 lines across the two files. The count is of call sites, not lines, but the document does not say so.
- **m-2** — §6.1 says `lane_titles` is referenced in `test_swimlanes.py`; disk shows **import only** (`:19`), never called in an assertion. LLR-003.2's shed order therefore has *no* existing guard, which strengthens R-3 rather than weakening it.
- **m-3** — QA F-4 (the initial frame: `_select_first` picks a task the lanes view often does not name) carries no ruling in the PLAN decision log, though §6.3 lists O-1/O-2 only. QA's exit criterion 6 requires all five §8 findings ruled; three are (F-1 via HLR-003's per-lane phrasing, F-3 via O-1, F-5 via D-1), **F-4 and F-6 are not**.
- **m-4** — §2.7's gate summary says *"No premise is ❓"* — true, but P-1 and P-2 are ❌ **carried, not executed** (R-5 admits this). C-43's own standard is that a citation of another document is not evidence. Acceptable as flagged; noted for the postmortem.
- **m-5** — The evidence checklist marks *"Diagram included"* ✗ with a reason. I accept the reason (single synchronous render path) but note that the **row-budget arithmetic** — where a shed row goes and who pays — is exactly the non-trivial flow a diagram would serve, and it is the thing three blockers concern.
- **m-6** — `.dev-flow/state.json` is modified in the working tree and `.fast-dev-flow/spec.md` is deleted but uncommitted. Not this review's scope; flagged so the Phase-3 diff is not read as containing them.

---

## 5. Is anything underivable as written?

**Yes — US-B, in two independent ways.**

1. **B-3 (empty curve).** There is no set of Phase-3 edits that satisfies HLR-003 (draw the row), LLR-003.5 (≥4 distinct braille glyphs), and C5/C6 (never a mark that means nothing) simultaneously on Delta-shaped lanes. One of the three must be amended. Phase 3 cannot pick which — that is a requirement decision.
2. **B-1 (unconditional acceptance).** `AT-003`, as defined in §2.6, is **unsatisfiable on the calm board** given LLR-003.3. An implementer following the LLRs produces code that fails the AT the same document derives from the same story.

US-A is derivable, with M-6 as the one genuine mechanism gap.

---

## 6. What I recommend for the gate

Not a rewrite — six targeted amendments, none of which reopens O-1 or O-2 as *decisions*:

1. Re-state §2.2 fn 3, §2.6 US-B Evaluability, and HLR-003's Observable outcome with the sheddability precondition; re-point `AT-003`/`AT-004` (B-1).
2. Reconcile the AT id space between `01-requirements.md` and `01b-qa-validation-plan.md` — one register, one owner (B-2).
3. Add the empty-curve clause to LLR-003.3's refusal enumeration, or condition LLR-003.5's threshold (B-3). This unblocks `AT-014`.
4. Replace HLR-005's `grep "own wave"` threshold with one that covers `views.py:720`, `:724–725`, `:750–752`, `:2112` and the `test_spend.py` docstrings — e.g. `grep -rn "wave\|curve" ` over the touched functions, read each hit (B-4, M-11).
5. Ask the operator to rule **separately** on superseding `test_spend.py:238` (the `prof` ceiling) and `:81` (the prohibition), and re-verdict `:98` as vacuous with a replacement law (B-5, B-6).
6. Extend §6.1's census with the 14 unnamed lanes-rendering files, at minimum `test_prism_laws.py`, `test_palette_ration.py`, `test_span_economy.py` (M-1, M-2, M-3) — and specify the text/field composition mechanism (M-6), because three of those verdicts depend on it.

---

## Evidence checklist (this review)

- [x] **Constraints stated explicitly** — reviewed against §2.4's eight; C1/C3/C4 re-verified on disk (`views.py:817`, `tests/test_spend.py:135`, `tests/test_swimlanes.py:88`).
- [x] **At least 2 alternatives considered** — §6 offers amendment paths per blocker rather than a rewrite; B-3 names three mutually exclusive resolutions and declines to pick, because that is the operator's ruling.
- [x] **Recommendation has rationale tied to constraints** — every blocker is tied to a named gate rule (modal `should`, missing acceptance, unnamed deliverable, unverified symbol, C-36 literal) or to an executed disk fact.
- [x] **Risks listed** — B-5 (one-way door: retiring the only `prof` ceiling), M-3 (Phase-3 literal reddening an unnamed law), M-6 (unspecified composition mechanism), m-6 (dirty tree).
- [x] **Cost / latency estimated where relevant** — N/A for a review; the batch's own figures (−0.17 ms, 114 cells / 4.0 %) were **carried not re-executed** and are flagged m-4.
- [x] **Diagram included when flow is non-trivial** — ✗ deliberately. The findings are a census and a contradiction set; a table carries both without loss. Recorded as a choice, per m-5's own standard.
- [x] **What would change the recommendation is stated** — §6. If B-1/B-3 are amended and the O-2 scoping gets its own ruling, the remaining findings are majors that Phase 3 can carry.
- [x] **Two-layer requirements** — assessed and **FAILED**: see B-2 (behavioural chain ids collide) and B-7 (functional chain terminates at LLR, TC column empty).
- [x] **No file under `taskboard/` or `tests/` was modified.** Verified: `git status --porcelain` shows only `.dev-flow/` paths, the pre-existing `.fast-dev-flow/` changes and untracked `_prototypes/`. All probing was read-only (`grep`, `sed -n`, and one `python -c` that imported `lane_geometry` and simulated `allocate` in memory).

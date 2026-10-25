# Design proposal — taskboard — Batch 2026-10-25-batch-01

> Filled by the orchestrator from the P2-approved requirements
> (`.dev-flow/2026-10-25-batch-01/01-requirements.md`, as amended at P2 round 2).
> The forward-applicability rule applies: every section names its consumer.

| Field | Value |
|---|---|
| Id | `PDR-2026-10-25-batch-01` |
| Requirements covered | HLR-2801..HLR-2804 · LLR-2801.1..LLR-2803.1 (v2, post-LED-2801/2801.1) |
| Modules touched (from `docs/ARCHITECTURE.md`) | `app` (its stylesheet `taskboard.tcss`) · `tests` (one new file) |
| Triggers that fired | A2 · B1 · D1 |
| Author / reviewers | orchestrator · `architect` · `qa-reviewer` · `ux-reviewer` (D1 fired) |

---

## 1 · Objective and scope

Give `MilestoneOffer` and `TeamIdentityPicker` the shared translucent backdrop
(`background: #0007`) so the board beneath shows through dimmed at start, on the
single-board, home (`enter`) and team paths, at 118x30 and 80x24 — the user-visible
outcome of SB-2. Mechanism (measured, not hypothesised): one **background-only**
declaration naming the two classes in `taskboard/taskboard.tcss`; no timing change,
no deferral, no other property.

Will NOT do (SB-3, HLR-2804): touch any other rule or screen; touch `modals.py` or
`app.py`; change the push order (picker first, offer last, D-615); change any
modal's content, keys or answers; dim the ~16 unlisted `ModalScreen` subclasses
(§6.3 of the contract — a backlog carry, not this batch).

## 2 · Modules and boundaries

| Module | What it owns here | What it exposes | What it must NOT reach into |
|---|---|---|---|
| `app` | the new declaration in `taskboard.tcss` | nothing new | `views` rendering (unchanged), `modals` (unchanged) |
| `tests` | `tests/test_startup_backdrop.py` (new) | — | shipped code |

- Boundaries respected as declared in `docs/ARCHITECTURE.md`: ✓ — the `app` layer
  owns its stylesheet; no boundary moves.

## 3 · Diagrams

None owed: the change is one CSS declaration; the information viewpoint lives in
the contract's IFC Part A flow, and the interaction viewpoint is the existing
mount-tick push order (unchanged). A diagram here would be a picture of one line.

## 4 · Interfaces that change — and which ones FREEZE

| Interface | Current | After | Consumers | **Frozen for the fork?** |
|---|---|---|---|---|
| none | — | — | — | n/a — one lane, no fork; no interface changes shape |

## 5 · Proposed test cases

All in `tests/test_startup_backdrop.py` (new; no existing test file is modified —
C-27's frozen-TEST routing has nothing to route). Fixture pattern: the kg board
(`kg_board.one_day(kg_board.shifted(path), date.today())` + the renumber key) and
the `multi_board_fixture` home pattern of `tests/test_home_deferred_start.py`.
Every node drives the real surface by keys and asserts the composited
full-screen-stack render (the `App.export_screenshot` source), with the vacuity
guard: the modal must be the top screen and the box title row must be located
before any row counting — a missing modal or unlocated box fails the node.

| Id | Layer (0 unit / A white / B black / UX) | What it asserts | **The mutation that would turn it RED** |
|---|---|---|---|
| `test_AT_2801_the_offer_opens_over_the_painted_board[size]` | B (118x30, 80x24) | Single-board start with candidates: `MilestoneOffer` is the top screen; the «◆ Milestones · convert one-day tasks?» box is located; > 0 non-blank rows outside the box border in the full-stack render | Deleting the new declaration (returns the opaque `#0d1117`; 0 rows outside) — the battery's kill node |
| `test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board[size]` | B (118x30, 80x24) | Two boards, `enter` on the default card: the offer is the top screen over the board (no `BoardsHome` beneath); box located; > 0 rows outside it | Same declaration delete (the home path reuses the identical rule) |
| `test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order[size]` | B (118x30, 80x24) + one geometry arm (118x30) | Team-shared board, no identity: stack tail `TeamIdentityPicker`, `MilestoneOffer`; > 0 rows outside the offer box; and with the picker alone on screen (the offer mark pre-set in the fixture — the gating of `taskboard/app.py:1557-1558`, not an empty-candidate board, so the arm carries no start-up write), the picker box region is row 0, columns 0-61, **height 11** — its full pre-batch geometry (`Region(0, 0, 62, 11)`, P2 probe; the height pin catches a vertical-grow regression the three-edge wording would miss) | Same declaration delete; a recentered-picker regression (the A1 shape) would trip the geometry arm |
| `test_TC_2801_quitting_with_the_picker_open_writes_nothing` | A | Team-shared board, no identity, picker up: exiting **via the `run_test` context exit** (the TC-616 quit precedent, `tests/test_milestone_offer.py:399-402` — a keypress would reach the modal's `escape` binding, not quit) without answering writes no board change (byte-identical board file) and persists no `team_user_id` (observable by loading the board file), and leaves the team dir byte-identical to a snapshot taken **before the app starts** (qa round-2 note) | Not mutation-bound to the css (a stylesheet cannot change writes) — a pin per LLR-2801.3; it is labelled a pin, not a gate (C-40 corollary) |

Plus one battery arm owned by P3's mutation runner (qa condition C1, named `QA-P4-B01-flake`): run the AT-2801 node 50× at 80x24 and record the minimum outside-box row count across runs ≥ 3 — a composite-timing flake guard; its transcript lives beside `evidence/mutation-001.txt` and its verdict is recorded in increment 001's packet. AT-2802's node additionally asserts no `BoardsHome` remains beneath the offer, which reaches `app.screen_stack` — a white-box touch inside a Layer-B node, recorded here per house precedent (`tests/test_milestone_offer.py:344-345`) and to be named in the node's docstring.

## 6 · Risks and rejected alternatives

| Alternative considered | Why it was rejected |
|---|---|
| Append the two classes to the existing shared rule (`taskboard.tcss:309-312`) | Its `align: center middle` would move `TeamIdentityPicker` off its top-left placement — a user-visible, unpinned side effect (P2 round-1 blocker A1, probe-verified round 2). Rejected. **Disposition (PDR, all three lenses): the top-left placement is blessed for this batch** — it is pinned by HLR-2803's geometry arm and was probe-verified byte-identical, and centering it here would exceed SB-3 — **and a named UX backlog item («center `TeamIdentityPicker`, or codify top-left as the first-run convention») is filed at the batch close** so the app's sole non-centered modal is a decided state, not drift. |
| Defer the pushes with `call_after_refresh` (the commission's anticipated mechanism, SB-2) | The hypothesis it answers — an unpainted board at push time — is refuted by measurement (§2.7 row 2: 23-29 painted rows beneath the modal). Deferral would change quit-while-open and started-record timing for no user-visible gain. Rejected per SB-1 (the fix follows the cause). |
| Rely on Textual's `ModalScreen` default (`$background 60%`) by clearing the `Screen` rule | The `Screen { background: #0d1117 }` rule is load-bearing for every screen; removing or excepting it changes far more than D-12, and 60% vs the app's 47% (`#0007`) would dim the start-up modals differently from every named modal. Rejected. |

## 7 · Forward-applicability table — **the section that makes this document honest**

| Output of this PDR | Named consumer downstream | Where the consumer will read it |
|---|---|---|
| design characteristics (background-only declaration; picker geometry pinned; shared rule byte-identical) | the Phase-3 increment | increment 001's packet §1/§2; the `git diff` inspection of LLR-2801.2 |
| enablers (kg-board fixture pattern; the two-board home pattern; the full-stack render oracle; the vacuity guard; the team-dir-before-start snapshot) | Phase 3 and validation | `tests/test_startup_backdrop.py`'s bodies; the mutation battery's runner beside `evidence/mutation-001.txt` |
| proposed test cases (the four nodes of §5, each with its named reddening mutation) | layers A/B and the DDR | the nodes themselves; the DDR's qa/ux lenses re-derive their probes from §5 |
| design → requirement traceability (HLR-2801..2804 ← the declaration + the four nodes) | the matrix and the DDR | contract §3/§4 ↔ §5 of this proposal; `ATLAS-TRACE.md` derives it |

- ⚠ Any row whose consumer column is empty: none — every row names its consumer.

## 8 · Parallelisation plan *(only if the batch forks)*

Not owed — one lane (§2.8 of the contract declares the empty per C-52).

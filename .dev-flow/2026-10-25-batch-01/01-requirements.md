# Requirements — taskboard — Batch 2026-10-25-batch-01

> The live contract. Current state only — no strikethrough, no amendment bullets,
> no measurement inside a normative sentence. The append-only reason log is
> `01-requirements-ledger.md`. Field guide: `templates/guides/req-template.md`
> (ships with the flow, never copied here).

## 1. Introduction

### 1.1 Purpose

Specify the D-12 fix: the start-up modals (the one-time milestone offer and the
team identity picker) open with the board visible behind them, dimmed by the same
translucent backdrop every other modal uses.

### 1.2 Scope

The rendering of the two start-up modal screens at start (single-board, the home's
deferred `enter`, and team mode). Out of scope per the commission (SB-3): no
modal's content, keys or answers; the deferred-start behaviour of batch
2026-10-24-batch-02 (HD-1..HD-4); quitting-while-open write behaviour; every other
modal's timing and backdrop.

### 1.3 Definitions, acronyms, abbreviations

- **the start-up modals** — `MilestoneOffer` and `TeamIdentityPicker`
  (`taskboard/modals.py`), pushed by `TaskboardApp._open_board`
  (`taskboard/app.py:1459,1462`).
- **the shared backdrop** — the `#0007` translucent screen background declared for
  the other modals at `taskboard/taskboard.tcss:309-312`.
- **the offer box** — the bordered `#offer-box` region of `MilestoneOffer`
  (`taskboard/modals.py` DEFAULT_CSS), whose title row reads
  «◆ Milestones · convert one-day tasks?».
- **D-12** — the backlog defect «the blank screen behind the start-up modals»
  (`.dev-flow/BACKLOG.md`, 2026-10-20 round; measured by QA-P4-04 of batch
  2026-10-24-batch-02).

### 1.4 References

- `.dev-flow/COMMISSION-startup-backdrop.md` (decisions SB-1..SB-3, the acceptance
  AT-a..AT-d, the evidence clauses).
- `.dev-flow/BACKLOG.md` (D-12).
- `.dev-flow/2026-10-24-batch-02/04-validation.md` (QA-P4-04: 0 text rows above
  the offer box on the deferred `enter` path and on a plain single-board start;
  captures `offer_118x30.png`, `offer_80x24.png`).
- `taskboard/taskboard.tcss` (the `Screen` background rule, line 3; the shared
  `#0007` backdrop rule, lines 309-312).
- `docs/ARCHITECTURE.md` §2 (the `app` layer owns `taskboard.tcss`).

### 1.5 Document overview

§2 the story and its premises · §3 the high-level requirements with their
black-box acceptance · §4 the low-level decomposition · the Information Flow
Contract · §5 the validation strategy.

## 2. Overall description

### 2.1 Product perspective

taskboard is a local single-user Textual TUI (see `docs/ARCHITECTURE.md` §1). This
batch changes one screen-style rule of the `app` layer; no module boundary, data
file or interface changes.

### 2.2 Product functions

At start, a board's start may open up to two modals: the team identity picker
(when the board is team-shared and the user has no identity yet) and the one-time
milestone offer. Every other modal in the app opens over the visible board, dimmed
by the shared `#0007` backdrop; the start-up modals are the exception (D-12).

### 2.3 User characteristics

The taskboard user at start-up, answering one or two one-time questions before
working the board.

### 2.4 Constraints

The order of the pushes is contractual: the identity picker first, the offer last,
so the offer covers whatever the start opened (D-615, unchanged). The fix follows
the diagnosed cause (SB-1), not the commission's hypothesis when the two disagree.

### 2.5 Assumptions and dependencies

Textual 8.2.8 (`textual.__version__` probed at P1). The suite's harness drives the
app headless with `run_test(size=(w, h))`; the full-stack render oracle is the
compositor's `render_update(full=True, screen_stack=app._background_screens)`,
the same source `App.export_screenshot` uses.

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-001 | As a user starting the app, I want the milestone offer and the team identity picker to open over the visible board — dimmed by the same backdrop every other modal uses — so that I keep my context while I answer them. | D-12 in `.dev-flow/BACKLOG.md` (2026-10-20 backlog round); commissioned by `.dev-flow/COMMISSION-startup-backdrop.md` | READY |

#### Refinement log (one block per story)

**US-001 — the board shows behind the start-up modals**
- **INVEST:** I ✓ · N ✓ · V ✓ · E ✓ · S ✓ · T ✓
- **Functionality (V, N):** user = the taskboard user at start-up · outcome = the MilestoneOffer and TeamIdentityPicker open over the painted board, dimmed by the shared `#0007` backdrop, exactly like every other modal · why = the blank screen behind the start-up modals loses the user's context (the defect as measured by QA-P4-04 in 2026-10-24-batch-02: 0 text rows above the offer box) · out of scope = no modal's content, keys or answers; the deferred start from the home (HD-1..HD-4); quitting-while-open write behaviour; any other modal's timing.
- **Feasibility (E, S):** implementation path = diagnosed at P1: the two start-up modal classes join the shared `#0007` backdrop rule in `taskboard/taskboard.tcss`; the board beneath already paints in the same first composite as the modal, so no deferral mechanism is needed · dependencies/unknowns = none open — the cause is measured, not hypothesised (§2.7 rows 2 and 5) · fits one batch? = yes — one increment, one source file (`taskboard/taskboard.tcss`, owned by the `app` layer).
- **Evaluability (T) — behavioral, black-box:** "When the app starts (single-board, or `enter` on the home's default card, or in team mode) and a start-up modal opens, the user observes the board's text rows behind the modal's dimmed backdrop." → AT-2801..AT-2803.
- **Open questions:** none — the mechanism was settled by the P1 measurement, not deferred to the PDR.
- **Classification:** `READY` — observable through the shipped surface at two terminal sizes; INVEST closed on all six axes.

### 2.7 Premise evaluation (C-43) — MANDATORY, one row per premise

| # | Premise, as a truth-apt proposition | Tier (axiom · hypothesis · premise) | Verdict | Executed evidence (command output / `file:line` — **NOT** a citation of another document) | Disposition |
|---|---|---|---|---|---|
| 1 | A board's start pushes the start-up modals synchronously inside the mount/switch tick: `_open_board` calls `_init_team_mode()` at `taskboard/app.py:1459` and `_offer_milestones()` at `taskboard/app.py:1462`, both of which `push_screen`. | premise | ✅ TRUE | `grep -n "_init_team_mode()\|_offer_milestones()" taskboard/app.py` → `1459` · `1462` (read at P1) | the defect's pre-image; the commission's SB-2 deferral hypothesis targets this tick |
| 2 | The commission's hypothesis — «the board view has not been laid out or painted at its real size when the modal goes up» — is FALSE: with the offer on screen, the board screen beneath holds 23-29 painted non-blank rows at 118x30 and 80x24, on the single-board, home and team paths alike. | hypothesis | ❌ FALSE (refuted) | P1 probe `.scratch/probe_red.py` → `evidence/red-p1.txt`: `board_paint.nonblank_rows` = 29 / 23 / 29 / 26 with `MilestoneOffer` (or the picker+offer stack) on top | SB-1 honoured: the fix follows the cause, not the hypothesis; no `call_after_refresh` deferral is added |
| 3 | The emptiness is the modal screens' own opaque background: the app-level rule `Screen { background: #0d1117; }` (`taskboard/taskboard.tcss:3`) matches the start-up modal screens (Textual type selectors match subclasses; `ModalScreen` in their `_css_type_names`, probed live), and the shared `#0007` backdrop rule (`taskboard/taskboard.tcss:309-312`) does not name `MilestoneOffer` or `TeamIdentityPicker`. | premise | ✅ TRUE | `MilestoneOffer.styles.background` resolves to `Color(13, 17, 23)` = `#0d1117` (probe, `evidence/red-p1.txt` `modal_background`); the selector list at `taskboard.tcss:309` read at P1 names every other modal and not these two | the fix site: adding the two classes to that rule makes the resolved background `Color(0, 0, 0, a=0.467)` and the outside-box rows > 0 (scratch positive check at P1: 8/20 rows at 118x30, 4/3 at 80x24) |
| 4 | The board beneath the start-up modals is composited dimmed, not hidden, once the screen background carries alpha: Textual's `ModalScreen` default is `$background 60%` and the shipped rule uses `#0007` for the other modals over the same compositor path. | hypothesis | ✅ TRUE | probed at P1: with the two classes added (scratch copy), the full-stack render shows the board's rows around the offer box — 8 above / 20 below at 118x30, 4 above / 3 below at 80x24 (probe output, P1 scratch run) | the AT thresholds derive from this measured regime |
| 5 | The suite's baseline at this batch's base is 3248 passed + 1 environmental skip (TC-1902, the clipboard arm), so P4 expects the same plus this batch's new nodes, in 3 sequential chunks. | premise | ✅ TRUE (pending P4) | asserted by the commission (§Evidence, the batch-02 close numbers); re-verified by the P4 chunks themselves | P4's expected totals derive from it |
| 6 | Tests run from the worktree import the worktree's `taskboard/`: `python -m pytest` from the worktree root puts the root on `sys.path` ahead of the editable finder, which still maps `taskboard` to the main checkout — standalone `python .scratch/x.py` probes therefore need `PYTHONPATH=<worktree>` to measure this tree. | premise | ✅ TRUE | import probe `env -u NO_COLOR python -m pytest .scratch/probe_import_test.py -q -s` → `taskboard.__file__ = C:\Users\jjgh8\Github\taskboard-wt\backdrop\taskboard\__init__.py`; `app.css_path` under a bare-script probe resolves to the main checkout's tcss (measured at P1) | every probe and test run in this batch names its interpreter invocation accordingly |

- **Premise evaluation:** 6 premise(s) · ✅ TRUE ×5 · ❌ FALSE ×1 (the commission's own hypothesis, refuted by measurement — recorded per SB-1) — the batch's derivation stands on the five TRUE rows; rows 2-4 and 6 are measured, not asserted.

### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork

| # | Condition (`C-52`) | Discharged? | The executed evidence |
|---|---|---|---|
| 1 | **Frozen contract** — no shared interface is touched inside a lane; one that must change returns to the trunk (trigger A3) | ✅ | not applicable — one lane; the change is one screen-style rule inside the `app` layer's own stylesheet, no interface is re-signed (A3 judged not fired at intake) |
| 2 | **Disjoint FILE sets**, not just modules — two lanes may not edit the same file, not even different regions | ✅ | not applicable — one lane; one increment |
| 3 | **Crossed reverse census** — family B run per lane and **shared before starting**; the trunk's act, impossible from inside a lane | ✅ | not applicable — one lane; the B1 probe at intake (`grep -rl _offer_milestones tests/` → `tests/test_boards.py` · `grep -rl _init_team_mode tests/` → `tests/test_boards.py`, `tests/test_markup_sites.py`) is the batch-wide census, re-run per family B's rule at the increment cut |
| 4 | **One owner of the trunk** — requirements, traceability, backlog and spec are never written from a lane | ✅ | the orchestrator owns the trunk; no lane exists |

- **Fork preconditions:** none — this batch runs one lane (declared empty per C-52).

---

## 3. High-level requirements (HLR)

**The chains, one line each:** US-001 → HLR-2801, HLR-2802, HLR-2803 (the commission's AT-a..AT-c) and the regression pin HLR-2804 (AT-d).

### HLR-2801 — the single-board start's offer shows the board behind it
- **Traceability:** US-001
- **Ledger:** none
- **Statement:** When the app starts with a single active board whose board has milestone candidates, the system shall open the milestone offer with the board's painted rows visible outside the offer box — dimmed by the same translucent backdrop the other modals use — at 118x30 and at 80x24.
- **Rationale (informative):** D-12 as measured by QA-P4-04: «0 text rows above the offer box … on a plain single-board start». The P1 probe reproduces it (`evidence/red-p1.txt`: 0 rows above and 0 below the box at both sizes, board painted beneath, modal background opaque `#0d1117`).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_startup_backdrop.py -k AT_2801` (node minted at P3; P1 RED probe executed at `base_ref`, `evidence/red-p1.txt`)
- **Numeric pass threshold:** with `MilestoneOffer` the top screen, text rows outside the offer box's border > 0 at 118x30 AND at 80x24 (the P1 probe measured 0 and 0; the scratch positive check with the fix applied measured 8 above / 20 below at 118x30 and 4 above / 3 below at 80x24).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the offer opens over the dimmed board — the board's rows are readable around the offer box, exactly like the task editor's backdrop.
  - **Shipped surface:** `MilestoneOffer` over the main board screen at start (`TaskboardApp.on_mount` → `_open_board(at_mount=True)`).
  - **Acceptance test(s):** AT-2801
  - **Boundary catalog (QC-3):** ☐ empty (no candidates — the offer does not open; the existing offer suite covers it, unchanged) ☐ boundary (none new — the rule change has no input surface) ☐ invalid (an unreadable board file gets no offer — `test_TC_616_no_offer_on_an_unreadable_load`, unchanged) ☐ error (none new)
  - **Negative control:** executed at P1 against `base_ref` — 0 text rows outside the box at both sizes (`evidence/red-p1.txt`, probe AT-2801). The node-minted RED lands in increment 001's mutation battery (C-40): removing the two classes from the `#0007` rule again turns AT-2801 red.

### HLR-2802 — the home path's offer shows the chosen board behind it
- **Traceability:** US-001
- **Ledger:** none
- **Statement:** When the app starts with two boards and the user presses `enter` on the home's default card, the system shall open the milestone offer over the chosen board with that board's painted rows visible outside the offer box, dimmed by the shared backdrop.
- **Rationale (informative):** the deferred `enter` path is where QA-P4-04 measured the empty backdrop first; batch 2026-10-24-batch-02 fixed the stack (the board beneath, the home gone) but not what the user sees — this HLR completes D-12 on that path.
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_startup_backdrop.py -k AT_2802` (node minted at P3; P1 RED probe executed at `base_ref`, `evidence/red-p1.txt`)
- **Numeric pass threshold:** same oracle as AT-2801: text rows outside the offer box > 0 (P1 probe: 0; positive check with the fix: 8 above / 20 below at 118x30).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** after `enter` on the default card, the offer opens over the chosen board, dimmed — the board's rows are readable around the box.
  - **Shipped surface:** `MilestoneOffer` over the board screen after `BoardsHome`'s `enter` (the deferred start of batch 2026-10-24-batch-02, re-timed nowhere).
  - **Acceptance test(s):** AT-2802
  - **Boundary catalog (QC-3):** ☐ empty (a default board without candidates — no offer, covered by the offer suite's arms on this path) ☐ boundary ☐ invalid ☐ error (none new)
  - **Negative control:** executed at P1 against `base_ref` — 0 rows outside the box on the `enter` path (`evidence/red-p1.txt`, probe AT-2802).

### HLR-2803 — team mode shows the board behind both start-up modals, in today's order
- **Traceability:** US-001
- **Ledger:** none
- **Statement:** When the board is team-shared and the user has no identity yet, the system shall open the team identity picker over the visible board; when the start also owes the milestone offer, the system shall open the offer over the picker, with the board's painted rows visible outside the picker box and the offer box; the order shall be the identity picker first and the offer last.
- **Rationale (informative):** D-615's cover rule («the offer covers whatever the start opened») and the picker's own backdrop share the same defect; the order is contractual and unchanged (SB-2).
- **Validation:** `test`
- **Executed verification:** `env -u NO_COLOR python -m pytest -q tests/test_startup_backdrop.py -k AT_2803` (node minted at P3; P1 probe executed at `base_ref`, `evidence/red-p1.txt`)
- **Numeric pass threshold:** with the offer on top, the screen stack's tail is `TeamIdentityPicker` then `MilestoneOffer` (unchanged from `test_TC_616_the_offer_covers_the_identity_picker_until_answered`), and text rows outside the offer box > 0 (P1 probe: 0; positive check with the fix: 8 above / 20 below at 118x30). The picker's own box takes the same backdrop (same rule, one declaration).
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** the picker opens over the dimmed board; the offer opens over the dimmed picker; both boxes keep the board readable around them.
  - **Shipped surface:** `TeamIdentityPicker` and `MilestoneOffer` pushed by `_init_team_mode` / `_offer_milestones` in team mode.
  - **Acceptance test(s):** AT-2803
  - **Boundary catalog (QC-3):** ☐ empty (a roster-less shared dir identifies no one — no picker, unchanged) ☐ boundary ☐ invalid ☐ error (none new)
  - **Negative control:** executed at P1 against `base_ref` — 0 rows outside the box with the stack tail already `TeamIdentityPicker`, `MilestoneOffer` (`evidence/red-p1.txt`, probe AT-2803: the order is right today, the backdrop is the defect).

### HLR-2804 — nothing else changes (the regression pin)
- **Traceability:** US-001
- **Ledger:** none
- **Statement:** When any path not named in HLR-2801..HLR-2803 runs — a single-board start without candidates, `--open PATH`, `B` after the start, quitting while a start-up modal is open, every existing modal other than the two named — the system shall behave exactly as before this batch, byte-for-byte in every file it writes and pixel-for-pixel in every frame it paints except the two start-up modals' screen backgrounds.
- **Rationale (informative):** SB-3. The change is one selector list in one stylesheet rule; everything it could touch is pinned by the existing suite.
- **Validation:** `test`
- **Executed verification:** the P4 full suite in 3 sequential chunks (the commission's §Evidence), baseline 3248 passed + 1 environmental skip (TC-1902) plus this batch's new nodes.
- **Numeric pass threshold:** the P4 chunks hold the baseline + new-node count with no other skip or fail; the offer suite (`tests/test_milestone_offer.py`), the home suite (`tests/test_home_deferred_start.py`, `tests/test_boards_home.py`), the team suites and the presence suites stay green unchanged.
- **Priority:** high
- **Acceptance (black-box) — the user-verified outcome (the WHAT):**
  - **Observable outcome:** no user-visible difference anywhere except the two start-up modals' backdrops.
  - **Shipped surface:** the whole app.
  - **Acceptance test(s):** AT-2804 (the P4 suite; every existing arm is a pin)
  - **Boundary catalog (QC-3):** none — this HLR pins behaviour; it adds no input surface.
  - **Negative control:** not due — a regression pin, not a gate (C-40's corollary): its predicate is invariant under the change it certifies by construction, and it is labelled a pin, not the gate.

---

## 4. Low-level requirements (LLR)

> Each LLR decomposes an HLR into a verifiable property at the implementation level.

### LLR-2801.1 — the start-up modals join the shared backdrop rule
- **Traceability:** HLR-2801, HLR-2802, HLR-2803
- **Ledger:** none
- **Statement:** The shared translucent backdrop rule at `taskboard/taskboard.tcss:309-312` shall name `MilestoneOffer` and `TeamIdentityPicker` alongside the other modals, so both start-up modal screens render `background: #0007` and the board screen beneath shows through dimmed; no other rule, screen or declaration in the stylesheet shall change.
- **Validation:** `test`
- **Executed verification:** AT-2801..AT-2803's nodes (P3) and the resolved-style probe: `MilestoneOffer(...).styles.background` → a colour with alpha < 1 after the change (P1 scratch check: `Color(0, 0, 0, a=0.467)`).
- **Numeric pass threshold:** the full-stack render shows > 0 text rows outside the offer box at 118x30 and 80x24 (AT-2801's numbers).
- **Negative control:** removing the two names from the selector list returns the resolved background to `Color(13, 17, 23)` and the outside-box rows to 0 — the increment's RED counterfactual (C-40), executed in the mutation battery.

### LLR-2801.2 — no timing change: the pushes stay in the mount tick, in today's order
- **Traceability:** HLR-2801, HLR-2802, HLR-2803, HLR-2804
- **Ledger:** none
- **Statement:** The start-up modals shall be pushed from `_open_board` in the same tick, in the same order (the identity picker by `_init_team_mode`, then the offer by `_offer_milestones`) with no deferral, callback or `call_after_refresh` added; the board beneath paints in the same first composite as the modal (the P1 measurement, §2.7 row 2), so no sequencing mechanism is needed or allowed.
- **Rationale (informative):** the commission's likely mechanism (`call_after_refresh`) was written against the refuted hypothesis; SB-1 sends the fix where the cause is. Keeping the mount tick synchronous also keeps quitting-while-open and the started-board record semantics byte-identical (HLR-2804).
- **Validation:** `inspection` + `test`
- **Executed verification:** `git diff` of the increment shows no change under `taskboard/app.py` (inspection, the packet's §2); the existing TC-616/TC-617 arms re-run green unchanged (test).
- **Numeric pass threshold:** the offer suite passes unmodified; the stack-shape assertion of `test_TC_616_the_offer_covers_the_identity_picker_until_answered` holds.

### LLR-2801.3 — modal contents, keys and answers are byte-unchanged
- **Traceability:** HLR-2804
- **Ledger:** none
- **Statement:** Neither `MilestoneOffer` nor `TeamIdentityPicker` shall change in `taskboard/modals.py`: their compose trees, bindings, answer handling, candidate rows and wording stay exactly as shipped; quitting while either is open writes the same files as today.
- **Validation:** `test`
- **Executed verification:** `tests/test_milestone_offer.py` and the picker/team suites re-run green with no modification (AT-d); `test_TC_616_quitting_unanswered_leaves_the_board_unmarked` among them.
- **Numeric pass threshold:** 0 test files outside `tests/test_startup_backdrop.py` (new) are modified by the increment.

### LLR-2802.1 — the home path opens the offer over the chosen board with the same backdrop
- **Traceability:** HLR-2802
- **Ledger:** none
- **Statement:** After `enter` on the home's default card, the deferred start's `_offer_milestones` push shall render with the shared backdrop over the chosen board's painted frame, exactly as the single-board start does; the home's pop and the stack shape of batch 2026-10-24-batch-02 (LLR-2704.1) are untouched.
- **Validation:** `test`
- **Executed verification:** AT-2802 (P3) and the re-run `tests/test_home_deferred_start.py` arms (AT-2705's stack assertions among them).
- **Numeric pass threshold:** AT-2802's > 0 rows outside the box; the home suite green unchanged.

### LLR-2803.1 — team mode keeps the cover order and gains the same backdrop on both modals
- **Traceability:** HLR-2803
- **Ledger:** none
- **Statement:** In team mode the picker shall open first and the offer last (D-615's cover rule, unchanged), and both screens shall carry the shared backdrop, so the board stays visible around whichever box is on top.
- **Validation:** `test`
- **Executed verification:** AT-2803 (P3) and the re-run `test_TC_616_the_offer_covers_the_identity_picker_until_answered` (its stack assertion) plus the team suites.
- **Numeric pass threshold:** AT-2803's stack tail and > 0 rows outside the box.

## Information Flow Contract (IFC) — C-54

> Part A in every batch; Part B when the system's boundary has components a consumer can address independently. The block syntax, its fields and the rules that read them are in `templates/ifc-template.md`, which ships with the flow and is not copied into this batch.

- **Part A — flows:**

```
FLOW: the board's painted frame beneath the start-up modals
  SOURCE : the board screen's composite — BoardView's content (app.refresh_view →
           views.render_view) laid out and painted at the terminal's real size in
           the same composite that raises the modal
  NODES  :
    - fn    : the shared #0007 backdrop rule (taskboard.tcss:309-312) naming
              MilestoneOffer and TeamIdentityPicker — the translucent screen
              background both start-up modals render with
      owner : LLR-2801.1
    - fn    : the unchanged mount-tick push order (_init_team_mode then
              _offer_milestones, _open_board taskboard/app.py:1459,1462) — no
              deferral; the board beneath paints in the same first composite
      owner : LLR-2801.2
  SINK   : the terminal frame around the offer/picker box — the board's rows
           visible, dimmed by #0007 (AT-2801..AT-2803's oracle rows)
```

- **Part B — boundary decomposition:** `no — every flow is the app's own, addressed through its keys and its files` (the same answer as batches 2026-10-24-batch-01 and 2026-10-24-batch-02: one TUI process; the screens are not independently addressable components)

---

## 5. Validation strategy

### 5.1 Methods

> **Two layers** (per the Two-layer validation rule). Every batch declares BOTH:
> - **Layer A — white-box / functional (`TC-NNN`):** validates the HLR/LLR mechanism (the HOW). Methods: `test`, `inspection`, `analysis`.
> - **Layer B — black-box / behavioral acceptance (`AT-NNN`):** validates the user story's outcome through the shipped surface (the WHAT). Method: `acceptance`.

Layer A: `inspection` — the increment's diff touches one selector list in
`taskboard/taskboard.tcss` and nothing else (LLR-2801.2's `git diff` check is the
mechanism's proof); `test` — the resolved-style probe
(`MilestoneOffer.styles.background` carries alpha after the change) plus every
re-run arm of the offer, home, team and presence suites (the pins, AT-d/HLR-2804).
Layer B (all NEW, minted at P3): `tests/test_startup_backdrop.py::test_AT_2801_the_offer_opens_over_the_painted_board`
(parametrized 118x30 and 80x24), `::test_AT_2802_enter_on_the_home_opens_the_offer_over_the_chosen_board`,
`::test_AT_2803_team_mode_shows_the_board_behind_both_modals_in_todays_order`. The
P1 RED probe of the same oracle was executed at `base_ref` and lives at
`evidence/red-p1.txt` (its scratch script stays in `.scratch/`, git-excluded, per
the batch rules).

### 5.2 Batch acceptance criteria
- 100% of HLRs/LLRs covered by at least one Layer B node with pass result (AT-2801..AT-2803), the Layer A checks green, and the regression pin HLR-2804 held by the P4 suite.
- Every new test mutation-checked (C-40): reverting LLR-2801.1 (the two names out of the `#0007` selector list) turns AT-2801 red; the RED counterfactual, per-node verdicts and restore digest are recorded in increment 001's packet.
- The P4 full suite: the baseline 3248 passed + 1 environmental skip (TC-1902, the clipboard arm) plus this batch's new nodes, in 3 SEQUENTIAL chunks, never in parallel with anything; any other skip or fail blocks the close.
- The real Windows Terminal capture pair (118x30 and 80x24) of the offer over the visible board — the single-board start and the home path — `b01-` window titles, each window closed by title right after its shot and verified gone, never another window (`JJ_WORKPC: dev-flow` among them), black shots and shots with fewer than 8 colours rejected, and a final assertion that no `b01-` window is left.

---

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions

- **SB-1 (diagnose first):** executed at P1 — the reproduction is `evidence/red-p1.txt` (0 text rows outside the offer box at 118x30 and 80x24, single-board, home and team paths). The cause with file:line: `taskboard/taskboard.tcss:309-312` — the shared `#0007` backdrop rule does not name `MilestoneOffer`/`TeamIdentityPicker`, so the app-level `Screen { background: #0d1117 }` (`taskboard.tcss:3`, matching the modal screens as a superclass) paints them opaque and hides the board beneath. The commission's hypothesis (unpainted board at push time) is refuted by measurement (§2.7 row 2) and is recorded as FALSE, per SB-1's «if the hypothesis is wrong, say so».
- **SB-2 (the fix):** the two classes join the shared backdrop rule; the board beneath already paints at its real size, so the user sees it dimmed behind the modals. No deferral is added — the mechanism the commission anticipated is unnecessary because the cause is elsewhere; the order (picker first, offer last, D-615) is untouched.
- **SB-3 (nothing else changes):** one selector list, one file (`taskboard/taskboard.tcss`); no modal content, keys or answers; the deferred start behaves exactly as batch 2026-10-24-batch-02 shipped; quitting while a start-up modal is open writes the same things.

### 6.3 Open risks

- **The 60%-vs-47% blend.** Textual's `ModalScreen` default is `$background 60%`; the shipped rule uses `#0007` (47% alpha) for every other modal. The fix puts the start-up modals on the app's existing convention (`#0007`), not the framework default — a deliberate consistency choice, flagged for the ux lens at the DDR (a different dim level on these two modals would itself be an inconsistency).
- **Screens without the backdrop.** Other `ModalScreen` subclasses not in the `#0007` list (e.g. the help and palette screens, if any) share the opaque-background trait by the same `Screen` rule. They are out of scope (SB-3) and are NOT changed; if the operator wants them dimmed too, that is a new backlog item.
- **Security scan (family C) — the verdict recorded:** `python C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-scan-spec.py C:/Users/jjgh8/Github/taskboard-wt/backdrop/.dev-flow/2026-10-25-batch-01/01-requirements.md` → exit 0, `flags: none`, `security_required: false`, all 5 control rows ok (run at the P1 gate, 2026-10-25). No auth, secrets, external integration, sensitive data, destructive-DB, input-surface, network or markup-rendering pattern fires — the change is a CSS selector list.

### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The live ledger is `01-requirements-ledger.md`, seeded empty; it gains its first
entry only when a requirement here is amended. Every requirement above names its
entries (`**Ledger:** none` today); `V26` compares the two sets of pairs both ways.

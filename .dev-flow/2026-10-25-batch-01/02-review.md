# Review — taskboard — Batch 2026-10-25-batch-01

> Phase-2 cross-agent review of `.dev-flow/2026-10-25-batch-01/01-requirements.md`.
> Lenses executed as independent sub-agents carrying the flow's role files
> (`agents/architect.md`, `agents/qa-reviewer.md`) — the spawn record is the
> batch plan's §Gate notices and runtime absences. Family C did not fire at
> intake, so the `security-reviewer` lens is not run in this core batch; the
> family-C scan (`devflow-scan-spec.py`) is the mechanised security check and
> its P1 verdict is folded in §Security review summary.

## ✅ Verdict (read first)

- **Round 1:** `iterate-to-refine` — one blocker (A1), one major (A2), seven
  minors (A3, A4, A5, Q1, Q2, Q3, Q4). Both lenses agree the diagnosis and the
  mechanism are sound; the block is on what the fix's selector list silently
  drags in, and on one false measured sub-claim.
- **Round 2 (full re-review of the amended contract):** both lenses
  PASS-WITH-FINDINGS — the blocker and the major are folded and probe-verified;
  five mechanical findings (R2-1..R2-5 architect; R1, R2 qa) were folded in the
  same pass: §2.2's restored sentence, the three «every other modal» survivors,
  the IFC node rewrite, the picker-pin number correction (left column 0, width
  62 — 61 was the rightmost column), and the ledger pairing LED-2801.1
  (HLR-2802 · LLR-2801.3).
- **Gate:** `approve` → PDR. The PDR inherits one recorded design note: with the
  shared rule untouched, `TeamIdentityPicker` is now the app's only non-centered
  modal — bless the top-left placement there or file a UX backlog item to centre
  it (architect round 2). P3 inherits one implementation note (qa R2): the
  team-dir snapshot for `test_TC_2801_quitting_with_the_picker_open_writes_nothing`
  is taken before the app starts.

## Detail (reference)

### Findings

| id | lens | class | finding | evidence | fold |
|----|------|-------|---------|----------|------|
| A1 | architect | blocker | The fix as specified (both classes join the shared rule at tcss:309-312) also applies that rule's `align: center middle` to `TeamIdentityPicker`, which today renders top-left (no align of its own) — an unpinned, unasserted user-visible move, contradicting HLR-2804's pixel pin. | tcss:309-312; modals.py TeamIdentityPicker DEFAULT_CSS (no align); live resolved-style probe this review | Folded at P1: the fix becomes a **background-only** declaration for the two classes (no `align` or any other property); HLR-2803 and LLR-2801.1 carry the picker's unchanged position explicitly; AT-2803 gains a box-position pin; the PDR keeps the alternative (authorize recentering as the consistent choice) as a named, rejected-with-reason option. |
| A2 | architect | major | Premise row 3 and the US/§2.2 wording claim the `#0007` rule «names every other modal» — false: ~16 other `ModalScreen` subclasses are unlisted (HelpModal, CommandPalette, StandupModal, PhaseEditor, MarkForm, PersonForm, TextPrompt, ClockModal, PresentKeys, GanttLinkMode, EmojiPicker, LinkPicker, TemplatePicker, TemplateEditor, HelpScreen, PresentScreen); GanttLinkMode's opacity is deliberate (its own `#0b0f17`). | census by the architect lens over modals.py/app.py | Folded at P1: row 3 and the «every other modal» wording corrected to name what the rule names; §6.3 carries the confirmed census, GanttLinkMode's deliberate opacity, and a backlog carry for the rest (out of scope per SB-3). |
| A3 | architect | minor | Positive-check numbers at 80x24 exist only for the single-board path; HLR-2802/2803 cite 118x30 only. | 01-requirements §2.7 rows 3-4 | Folded at P1: §5.1 states AT-2802/AT-2803 run at 118x30 **and** 80x24 (parametrized), symmetric with AT-2801. |
| A4 | architect | minor | Under `TEXTUAL_ANSI`, `ModalScreen`'s `&:ansi { background: transparent }` makes the whole backdrop question moot framework-side; the contract assumes truecolor silently. | textual 8.2.8 DEFAULT_CSS probe | Folded at P1: one §6.3 line names the ANSI-mode no-op; no test action. |
| A5 | architect | minor | The worktree tcss shows a git-dirty line-ending phantom (autocrlf); the increment's `git diff` inspection could trip on noise. | `git status` vs `git diff HEAD` this review | Carried to the increment packet (not a contract matter): the LLR-2801.2 diff check compares content and ignores line-ending normalization. |
| Q1 | qa | minor | «Quitting while a start-up modal is open writes the same things» is pinned only for the offer; no test quits with the picker open; LLR-2801.3 over-cites. | tests grep this review | Folded at P1: LLR-2801.3 narrowed to what the cited test proves (the offer) and a new P3 node `test_TC_2801_quitting_with_the_picker_open_writes_nothing` named in §5.1. |
| Q2 | qa | minor | The AT vacuity guard (modal must be the top screen and the box title row must be located before counting) is stated in a threshold but not nailed into the node spec. | 01-requirements §3 HLR-2801; house pattern test_milestone_offer.py | Folded at P1: §5.1 Layer B carries the guard sentence verbatim. |
| Q3 | qa | minor | The commission mutation-checks every new test; §5.2 names only AT-2801 as the kill node without scoping the per-node verdicts. | COMMISSION §Evidence | Folded at P1: §5.2 names AT-2801 as the kill node and records per-node verdicts for AT-2802/AT-2803 under the same single-selector revert, with the justification (one rule, three oracle reuses). |
| Q4 | qa | minor | The commission's validator clause (`--brief` 0 BLOCK at start and close) is not carried into §5.2. | COMMISSION §Evidence | Folded at P1: §5.2 gains the bullet. |

### shall / should check

Both lenses grep-verified the contract: every HLR/LLR statement is `shall`;
no `should`/`debería` anywhere. Clean — no blocker of that class.

### Two-layer acceptance review (blockers)

(a) Every story has a black-box `AT` (AT-2801..AT-2803 + the HLR-2804 pin). (b)
Every output-producing requirement names its observable deliverable and the
observation method (the composited full-screen-stack render, the same source
`App.export_screenshot` uses). (c) Both traceability chains are complete:
US-001 → HLR-2801..2804 → LLR-2801.1..2803.1 → AT/TC. (d) The ATs drive the
real surface by keys (`enter` on the home card) and assert the rendered
outcome; the only internals referenced are Textual framework seams
(`_compositor`, `_background_screens`, `screen_stack`) that match the house
convention (`_painted`, the D-615 stack assertion) — no app-internal symbol is
referenced. PASS on all four limbs, conditional on Q2's guard being folded
(it was, round 2 to confirm).

### Supersession census (change-first)

Planned touch set: `taskboard/taskboard.tcss` (one new declaration) and
`tests/test_startup_backdrop.py` (new). Reverse-grep of the declared symbols
(`MilestoneOffer`, `TeamIdentityPicker`, the `#0007` selector) across `tests/`
lands only in tests this batch mints or re-runs; the B1 probe of intake
(`grep -rl _offer_milestones tests/` → `tests/test_boards.py`;
`grep -rl _init_team_mode tests/` → `tests/test_boards.py`,
`tests/test_markup_sites.py`) asserts no offer/picker test asserts the screen
background, so no existing assertion is invalidated by the rule change.
Best-effort + gate-confirmed; the increment gate is the completeness
guarantee (never stamped VERIFIED COMPLETE).

### Security review summary

Family C did not fire at intake (trigger evaluation, PLAN.md §Triggers), so
the `security-reviewer` lens does not run in this core batch — declared, not
skipped silently. The mechanised family-C check ran at P1:
`devflow-scan-spec.py` over the contract → exit 0, `flags: none`,
`security_required: false`. The change under review is a CSS selector list;
no attack surface, sensitive data, auth or authorization is touched.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer

- **architect** (round 2): verdict PASS-WITH-FINDINGS — round-1 blocker A1
  probe-verified folded (background-only declaration; picker region and align
  identical in both states, back-to-back run against the real tcss); findings
  R2-1..R2-5 folded (all editorial/mechanical; R2-4's pin-number correction has
  downstream force and landed before P3). Residual named open: the picker's
  sole-non-centered-modal design note → PDR.
- **qa-reviewer** (round 2): verdict PASS-WITH-FINDINGS — Q1-Q4 confirmed
  folded; R1 (the stale IFC node) folded; R2 is a P3 implementation note
  (team-dir snapshot before start). GO for the PDR, conditional on the IFC fold
  (done in the same pass).
- **security-reviewer:** not run — family C not fired; the scanner's verdict
  stands in its place (above).

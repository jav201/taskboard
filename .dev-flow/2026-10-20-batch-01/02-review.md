# Review — taskboard — Batch 2026-10-20-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — iteration 1 `iterate-to-refine` (architect, qa-reviewer (QA-1 blocker), ux-reviewer, security-reviewer `BLOCK-UNTIL: S-1, S-2`) → LED-2026-10-20-batch-01.2; iteration 2 `iterate-to-refine` (architect A-27..A-29, qa QA-20 blocker and QA-21/QA-23, ux UX-10; security approve with conditions) → LED-2026-10-20-batch-01.3; iteration 3 `approve` (all four reviewers), the residues folded at once (A-33, S-12, QA-26)
- **Out-of-scope findings:** 4 named and routed below — UX-5 (start-up modals over the home) → §6.3 risk, accepted; UX-8 (home read speed) → §6.3, out of scope; ux's note on `ConfirmModal` (no hint that `tab` reaches the button, shared with the projects' delete) → `BACKLOG.md`; N2 (no chip in the presentation, D3) → the close, for the operator
- **Findings:** iteration 1: 2 blocker-class (QA-1; S-1/S-2 HIGH as one block) · 19 major · 40 minor; iteration 2: 1 blocker (QA-20) · 6 major (A-27..A-29, QA-21, QA-23, UX-10) · 12 minor; iteration 3: 0 blocker · 0 major · 4 minor (A-33, S-12 residue, QA-25 this record, QA-26 the oracle's note — fixed)
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box (they drive `open_app` and keys)
- **Census (change-first):** done — best-effort + gate-confirmed
- **Security:** ⚠ 13 findings (S-1, S-2 high; S-3..S-6 medium; S-7..S-13 low) — every one carried into the contract; forward `BLOCK-UNTIL: S-1, S-2` at increment 004 (PDR PC-2)
- **Evidence checklists (architect / qa / security):** ✓ all complete (in the reviewers' returns; ux-reviewer too)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C1, C5, C6, C8 fired) — each spawned as a generic agent with its `agents/<role>.md` role, read-only, in parallel, 2026-10-20, three iterations; each reviewed the ARQ amendment, the requirements (P2) and the design proposal (PDR) in one pass (declared in `PLAN.md` §Key decisions). Probes: qa — the fixture's counts and ids, `tc1` Done, the strip widths, the 118-column capture's row 3; architect — `ConfirmModal`'s initial focus headless, `copy.deepcopy(Board)`, the 15 head-row sites; security — the narrow head row's `@click` through `_strip`; ux — the key bar with `B` injected. None edited a file.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | major | ARQ §3/§4 | no owner for the move's team ids (`boards` cannot read `team_sync`) | `app.move_team_ids` | fixed — module map, LLR-2206.1 |
| A-2..A-5 | architect | minor | ARQ | `after_move`, `due_strip` missing; folders `in / out`; `boards.py` "new" | add | fixed — module map |
| A-6 | architect | major | HLR-2202 | a failed migration at a switch stops the app | keep the open board | fixed — LED .2, .3 |
| A-7 | architect | major | HLR-2201 | a corrupt registry overwritten at the launch that found it | no write after an unreadable read; `.corrupt-N` | fixed — LED .2 |
| A-8 | architect | major | LLR-2203.1 | the narrow fallback re-activates markup | escape it | fixed — LED .2 |
| A-9 | architect | major | LLR-2204.1 | keys live behind the home's modals; `enter` order | block while on the stack; pop first | fixed — LED .2, narrowed to the seat (LED .3) |
| A-10 | architect | major | LLR-2206.1 | the move's failure states | copies; target before source | fixed — LED .2 |
| A-11 | architect | major | HLR-2206 | "team mode" undefined | `team_shared_dir`, fresh `team.json` | fixed — LED .2 |
| A-12..A-18 | architect | minor | various | setup row width, missing-target KeyError, clear/keep lists, minutes, ConfirmModal focus, interval order, P-10 diff | as named | fixed — LED .2 (A-16 → A-28) |
| A-19..A-25 | architect | major/minor | PDR §5 | vacuous mutations (width, save order), README timing, `exist_ok`, attribution, key count, §7 | real mutations | fixed — design, LED .2 |
| A-26 | architect | minor | PDR | the seam's blast radius | a suite run | fixed — `evidence/suite-seam.txt` 2819 passed |
| A-27 | architect | major | HLR-2206 | a failure past the source save leaves the live board stale | hand the new source over | fixed — LED .3 |
| A-28 | architect | major | AT-2205 | `enter` cannot confirm `ConfirmModal` | `tab`, `enter` | fixed — LED .3 |
| A-29 | architect | major | HLR-2202 | a missing file at start | pass over it | fixed — LED .3 |
| A-30..A-33 | architect | minor | ARQ, PDR, seam | stale rows; design drift; session-wide seam; the guard row | align; per-test seam | fixed |
| QA-1 | qa-reviewer | blocker | AT-2202 | `]` on a Done task writes no history | `[` on `tc1` | fixed — LED .2 |
| QA-2..QA-19 | qa-reviewer | major/minor | various | clock seam, narrow markup, start sequence, peek quarantine, vacuous predicates, inert keys, README timing, error class, slug, crops | as named | fixed — LED .2 |
| QA-20 | qa-reviewer | blocker | AT-2203 | after `0` the switch lands on People | `esc`, `1` first | fixed — LED .3 |
| QA-21 | qa-reviewer | major | HLR-2204 | the drop rule contradicts the 118 capture | the round's rule; inner-53 arm | fixed — LED .3 |
| QA-22..QA-24 | qa-reviewer | major/minor | PDR, LLR-2205.1 | design drift; a surviving mutation; the oracle's arguments | align; settings arm; name them | fixed — LED .3, design |
| QA-25, QA-26 | qa-reviewer | minor | process, TC-2203 | the findings not on record; the frozen oracle tied to the fixture | this table; regenerate note | fixed — this record; `evidence/frames_base.py` docstring |
| UX-1..UX-3 | ux-reviewer | major | HLR-2204/2205/2206 | missing-file card; `Delete` button; confirmation at 80×24 | state; `Archive`; scroll | fixed — LED .2 |
| UX-4, UX-6, UX-7 | ux-reviewer | minor | HLR-2205/2206 | undo wording; archived notice; long file line | as named | fixed — LED .2 |
| UX-5 | ux-reviewer | minor | D11 | board modals over the home name no board | — | accepted — §6.3 |
| UX-8 | ux-reviewer | minor | §5 | no slow-state criterion | — | out of scope — §6.3 |
| UX-9..UX-13 | ux-reviewer | major/minor | HLR-2202/2204/2206 | §6.3 contradiction; missing file at start; `enter` on a missing card; failed-migration state; refusal texts | as named | fixed — LED .3 |
| S-1, S-2 | security-reviewer | high | HLR-2206 | traversal through task ids; failure states of the move | id refusal, containment; copies, order | fixed — LED .2; forward `BLOCK-UNTIL` at 004 (PC-2) |
| S-3..S-9 | security-reviewer | medium/low | HLR-2201/2203/2204/2205/2206 | narrow markup; border titles and notices; registry cleaning; target-side team; backups and logs; quarantine; slugs and the seam | as named | fixed — LED .2 |
| S-10..S-13 | security-reviewer | low | ARQ, PDR, tests | stale rows; `touch` order; stamp and hard links; subprocess home | align; `(mtime, size)`, `samefile`; `HOME`/`USERPROFILE` | fixed — LED .3, `tests/test_report.py` (increment 001) |

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean — `grep -n "should" 01-requirements.md` hits informative text only (architect, iteration 1).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2201 | yes (AT-2201, AT-2202) | yes | yes | yes — `open_app`, keys, files | ✓ |
| US-2202 | yes (AT-2203, AT-2204) | yes | yes | yes — the screen, the captures | ✓ |
| US-2203 | yes (AT-2205) | yes | yes | yes — keys, files | ✓ |
| US-2204 | yes (AT-2206) | yes | yes | yes — keys, files | ✓ |

### Supersession census (change-first)

Planned files: `taskboard/boards.py` (new), `models.py`, `views.py`, `app.py`, `__main__.py`, `modals.py`, `keymap.py`, `taskboard.tcss`; `tests/conftest.py`, `tests/test_report.py`, `tests/test_colour_budget_app.py` (law-driven), `README.md`. Families run: B1 reverse greps (`PLAN.md` §Triggers), the measured blast radius of `B` (`evidence/suite-keyb.txt`: 3 failed — one law-driven literal table, two satisfied by increment 002), the seam's (`evidence/suite-seam.txt`: 0 failed), the head row's byte identity without a label (`evidence/frames-base.json`). Reservations: the key-bar captures of other batches' evidence are frozen evidence, not tests. The increment gates confirm.

### Security review summary
security-reviewer (C1, C5, C6 by the P1 scan; C8 judged): iteration 1 `iterate-to-refine`, `BLOCK-UNTIL: S-1, S-2`; iteration 2 approve with conditions (S-10..S-13); iteration 3 approve (S-12 residue folded). Forward: `BLOCK-UNTIL: S-1, S-2` at increment 004 until TC-2206/AT-2206 pass and the reviewer re-verifies (PDR PC-2). C2, C3, C4, C7: not fired.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
Each reviewer returned its checklist with its findings (iterations 1–3): every finding with what/where/why/fix ✓; severities ✓; no secrets ✓; verdicts explicit ✓; qa: edge classes and vacuity ✓ after iteration 2 (✗ in iterations 1–2 for QA-11, QA-1/6/7/13, QA-20/21/23, each fixed).

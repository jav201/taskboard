# Review — taskboard — Batch 2026-10-24-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3 (three rounds: round 1 `iterate-to-refine`, rounds 2–3 re-reviews of the amended contract; final round both lenses PASS)
- **Out-of-scope findings:** none

- **Findings:** 1 blocker (round 1, fixed) · 4 majors (rounds 1–2, all fixed) · 12 minors (rounds 1–3, all fixed or named)
- **shall/should check:** ✓ clean (checked all three rounds, including the amended text)
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box
- **Census (change-first):** done — best-effort + gate-confirmed (the qa lens's census of every multi-board app start and every `switch_board` call in `tests/` was declared exhaustive at round 2)
- **Security:** not run — trigger family C did not fire in `core` (the C1–C8 probes are tabled in PLAN.md §Triggers; the scanner's two flag words are answered in the contract's §6.3)
- **Evidence checklists (architect / qa / security):** ✓ all complete (security: not owed)

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| B1 | architect | blocker | LLR-2701.1 / LED-2701.1 | `_announce_renumbering` is a board writer (sets the flag and saves, `app.py:1583-1594`) mis-classified as read-only; the contract was unimplementable against its own AT-2701 byte-equality | move it to the deferred set; keep the rescue notice (read-only) at mount | fixed (LED-2701.1r1) |
| M1 | architect | major | HLR-2706 / LLR-2706.3 | the `/` search seat named in the statement had no black-box assertion | assert the search surface in AT-2706 | fixed (LED-2706.3r1) |
| M2 | qa | major | HLR-2702 error boundary | the deferred start's failure posture unspecified (record on failure? user where?) | pin it in a new LLR with a node | fixed (LLR-2702.4, LED-2702.4, TC-2703) |
| M3 | qa | major | HLR-2706 / LLR-2706.3 | same seat hole: no test would redden a missing search re-read | same as M1 | fixed |
| M4 | qa | major | HLR-2708 | the regression pin's permitted-diffs list mis-enumerated the arms HD-1 breaks — `test_boards.py`'s mount-order TC and the TC-2409 lifecycle arms were unnamed, so their required updates were forbidden | extend the named list | fixed (round 1; LED-2708 implicitly, entry below) |
| M5 | qa | major | HLR-2708 | round-2 residual: `test_TC_2202_switch_board_starts_the_other_board_over`'s same-board no-op assertion meets a pending start | name it; the arm leaves the home first (LLR-2702.3) | fixed (LED-2708r1; census declared exhaustive) |
| m1 | architect | minor | LLR-2706.3 | dropped the `@`/`#` query qualifier (stricter than the HLR) | bind the search seat to `@…`/`#…` queries | fixed (LED-2706.3r1) |
| m2 | architect | minor | LLR-2702.1 | record's restore-writer and partial-start semantics unspecified | pin: written only on a completed start; restore writes back the previous id | fixed (LED-2702.1r1) |
| m3 | architect | minor | LED-2703.1 | `peek_board` line-reference slip (defined `boards.py:614`) | correct the citation | fixed (LED-2703.1r1) |
| m4 | both | minor | LLR-2701.2 / HLR-2702 | garbled/ambiguous threshold wordings ("= 1", "changed by the sweep exactly") | reword with measurable clauses | fixed (LED-2702.1r2) |
| m5 | qa | minor | §5.1 / LLR-2702.1 | the Layer A list thinner than the LLRs; the LLR's verification named no unit node | name TC-2703 everywhere | fixed |
| m6 | qa | minor | premise 4 | verdict TRUE on a deferred check | re-tier as hypothesis | fixed |
| m7 | architect | minor | HLR-2702 threshold | the "iff" had an unpinned fixture precondition | pin `RENUMBER_NOTICE_KEY` + completed migration | fixed (LED-2702.1r2) |
| m8 | architect | minor | HLR-2702 threshold (round 3, n4) | the fixture clause omitted the milestones mark — `run_milestone_offer(board, [])` writes when the mark is absent (`models.py:1792-1795`) | add the third pin | fixed (LED-2702.1r3) |
| m9 | architect | minor | HLR-2706 | the `#` half of the search seat has no named assertion (single-arm coverage gap) | named open — bounded by the shared per-seat re-read call and the `#` manager/editor arms; accepted, recorded here |

### shall / should check

✓ clean — all three rounds; every HLR/LLR statement is `shall`-normative, no modal `should`; the amended text re-checked at rounds 2 and 3.

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2701 → HLR-2701..2705, 2708 | yes | yes | yes | yes | ✓ |
| US-2702 → HLR-2706, 2707 | yes | yes | yes | yes | ✓ |

### Supersession census (change-first)

Planned touched files: `taskboard/app.py` (increment 001), `taskboard/people.py` + `taskboard/marks.py` + `taskboard/app.py` (increment 002), tests uncapped. The qa lens ran the reverse census change-first (family B, trigger B1): every multi-board app start and every `switch_board` call in `tests/` checked — the found arms are the M4/M5 rows above, all named in HLR-2708's permitted diffs. Reservations: none beyond the named m9 (single-arm coverage). The increment gate must confirm: the named existing suites re-run green at P3/P4 with only the permitted diffs.

### Security review summary

Not run — trigger family C did not fire in `core` (C1–C8 judged at intake, tabled in PLAN.md §Triggers with probe outputs). The Phase-1 pattern scan's two flag words (`migration`, `expose`) are answered in the contract's §6.3; no auth surface, secrets, external integration, sensitive data, destructive DB op, network exposure or new markup rendering exists in this change.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer

- **architect:** ✓ contract read whole; every cited symbol verified against disk by range/grep (`on_mount` 1301, `_open_board` 1405, `switch_board` 1453/1458, `_announce_renumbering` 1583-1594, `_warn_if_rescued` 1609-1626, `run_milestone_offer` `models.py:1792-1795`, `peek_board` `boards.py:614`, the named test arms); V26 pairs re-verified each round.
- **qa-reviewer:** ✓ every threshold checked for measurability and subject-presence (C-40); the AT nodes checked drivable through the real surfaces (home keys, `notifications=True`, screen stack); the seam's `milestone_offer` marker acknowledged for AT-2705; the existing-test census run three times, declared exhaustive at round 2.
- **security-reviewer:** not owed (family C not fired).

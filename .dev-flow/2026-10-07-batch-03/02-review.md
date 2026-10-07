# Review — taskboard — Batch 2026-10-07-batch-03

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3  /  `iterate-to-refine` → Phase 1 (blockers present, or a requirement-defect major)
- Out-of-scope findings: `2` named and routed below  /  `none`

- **Findings:** `0` blocker · `0` major · `2` minor
- **shall/should check:** ✓ clean  /  ✗ misuse (blocker)
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box  /  ✗ `<none>`
- **Census (change-first):** done — best-effort + gate-confirmed  /  ⚠ incomplete   (NEVER stamp "VERIFIED COMPLETE")
- **Security:** ✓ no findings  /  ⚠ `<N>` findings
- **Evidence checklists (architect / qa / security):** ✓ all complete  /  ✗ `<missing>`

> The P2 history in one line: iteration 1 the four lenses FAIL (qa · ux) / PASS-WITH-NOTES
> (architect · security) on the contract's wording — CL-1..CL-9 folded in LED .2 and verified by
> re-reading; iteration 2 (the close-out re-read of the SHIPPED tree, this artifact's record):
> approve, 0 blocker · 0 major · 2 minor. Reviewer pool: `coordinator` — the orchestrator's own
> review; the lens files self-executed by the close-out coordinator (the runtime spawned nobody;
> that self-execution is named here once, per the runtime rule, and every other artifact points
> at it). Lens transcript: `evidence/close-review.log` (sha256
> `3d03e2a0e40f45cec7758ccc30cdcd759619a7c8ff8599e68a5e6282d5412570`).

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| F1 | coordinator (close-out lens pool) | minor | `team_sync.py` hygiene (HLR-902 adjacent) | `taskboard/team_sync.py:226` — `if not isinstance(task.title, str):` is dead code post-S-9 (a title is always text after the load boundary) | remove it at a future touch of `team_sync.py`; no behaviour either way — the implementation is frozen this batch | open — noted, not blocking; declared in `05-close.md` §What was NOT done |
| F2 | coordinator (close-out lens pool) | minor | `PLAN.md` (the living plan) | the batch PLAN still carries template placeholder cells at close (its Premises / Triggers / status rows) | fill at the next rollover's plan refresh; the load-bearing facts live in the contract §2.7 and the close | open — declared in `05-close.md` §What was NOT done |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a finding nobody raised. Write your own rows in the table above.

```text
| *(example)* F1 | architect | blocker / major / minor | | | | open / fixed |
```

**Folded P2 iteration-1 findings (history, closed in LED .2 — kept for the record):**

| ID | Reviewer | Severity | What | Fold |
|----|----------|----------|------|------|
| CL-1 | architect ∥ security | blocker (convergent) | the contract said the migration "re-raises" while its own reference (the offer) RETURNS `result.error` — and the increment already shipped the offer's shape | LED .2: HLR-901/LLR-901.1 restated to the `result.error` convention |
| CL-2 · CL-4 | qa ∥ ux | blocker (convergent) | AT-901/902/903 were pointers to nothing; AT-903 was circular | LED .2: the three ATs DEFINED — AT-903's four arms, each a painted-frame read (C-32), the shared drawn-band computation (CL-7), the `N open` head, the `▼ N below · ▲1 ◆` marker (as the BACKLOG then wrote it), the marker-only scope (CL-9), the swimlanes arm (CL-5) |
| CL-3 | qa ∥ security | blocker (convergent) | S-9's container arm shipped the title's repr — not a title, and can blow the cell widths | LED .2: containers and null read `Untitled`; TC-902's exact strings for all five shapes; the stale team_sync expectation folded to `["Good", "123"]` |

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

CLEAN — `grep -n "should\|shall" 01-requirements.md` returns 6 statements, every modal a
`shall` inside a Statement; `should` appears nowhere (transcript: `evidence/close-review.log`
LENS 1). The negative-control and boundary-catalog bullets are separate labelled fields, not
modal prose.

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-901 / HLR-901 | yes — AT-901 | yes — the board on disk (bytes + `links_marked`) and the app's exit message, observed via `run_test` + `capsys` | yes — US-901→HLR-901→LLR-901.1→TC-901 | yes — drives the app at 118×30 and reads the exit text + the file bytes; the only monkeypatched seams are the OS's (`os.replace`, `Path.unlink`) | ✓ |
| US-902 / HLR-902 | yes — AT-902 | yes — the opened board's task row, observed on the painted kanban frame + the app's task list | yes — US-902→HLR-902→LLR-902.1→TC-902 | yes — a board file in, the rendered frame out; the load boundary is the shipped surface | ✓ |
| US-903 / HLR-903 | yes — AT-903 (×4 arms) | yes — the painted frames of kanban/lanes/agenda/focus and the `?` legend lines | yes — US-903→HLR-903→LLR-903.1→AT-903's arms (+ the TC-311 census for the fold literal) | yes with the C-32 reading — the arms assert the compositor's painted cells / the renderer's emitted text, never models-internals; arm 1 presses the real `?` key and reads the same legend seat the modal reads (`legend_entries` is the legend's shipped seat, folded there by batch B2a) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

4 files × 4 families, best-effort + gate-confirmed: `taskboard/models.py` · `taskboard/app.py`
· `taskboard/views.py` · `tests/test_team_sync.py` (+ new `tests/test_cleanup.py`).
**Behavioral-placeholder** — `grep -rn "TODO\|FIXME\|XXX\|NotImplemented" taskboard/` over the
diff: 0 planted placeholders; the supersession inspections in both packets name the three
superseded markers (the raw-title seat, the pre-S-4 handler order, the renamed fold seat) with
0 surviving positive refs. **Structural/placement** — `_coerce_title` sits beside
`project_color_on_load` at the models boundary; the kanban-? branch sits in the existing
HelpModal seat chain; `_fold_keep`/`_kanban_band_geometry`/`_kanban_high_rows` sit beside
`_kanban_grouped`; the marker sites are per-renderer locals. **AST-composition** — no
monkeypatching of shipped functions by product code (only tests patch OS seams); no dynamic
imports added; `_milestone_title` is a pure formatter. **Frozen-module** — the frozen seats
(the board-file loader, `Board.save_atomic`, the render dispatch) untouched; the
no-live-board/no-scratch guards green in the close suite. Reservations: the dead
`isinstance` guard (F1) and the PLAN placeholders (F2) — named, non-blocking. What the
I-gate confirmed: both packets' 16-row checklists, signed ✓ with transcripts and digests.

### Security review summary
No findings at the close-out pass. The executed diff read (`git diff HEAD -- taskboard/
tests/` — `evidence/close-review.log` LENS 4): 4 files, +174/−56; no new
eval/exec/subprocess/network surface, no secrets, no path echoes beyond the shipped basename
convention; tests use synthetic `tmp_path` boards only. The batch's security CONTENT is the
closure of the two filed findings themselves — S-4 (restore-first, the refusing-unlink arm)
and S-9 (the load-boundary coercion) — both now pinned by TC-901/TC-902. Verdict: OK,
0 HIGH.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

**`architect` (self-executed by the coordinator — close-out):**
- [x] Constraints stated explicitly — the contract §2.4 carries the four constraints; each `executed` (the base tip, the frozen surface) — `01-requirements.md:78-81`
- [x] 2+ alternatives considered WHERE A REAL DECISION EXISTS — `n/a — the decisions were already made by the findings that filed the items (the offer's order for S-4; the shipped `Untitled` convention for S-9; the C-2b-style painted-frame reads)`; the one live decision (the fold literal) has its alternatives recorded in LED .3 (the `▾ N more` rename, tried and reverted)
- [x] Constraints that do not apply marked `n/a` — §1.2 names what the batch does NOT cover
- [x] Recommendation rationale tied to constraints — every HLR cites its finding
- [x] Risks listed — `04-validation.md` §Gaps: none; the packets' §5 carry the residual risks
- [x] Cost/latency — `n/a — no runtime cost change: two boundary checks per load, one legend recompute per `?` press`
- [x] Diagram when flow non-trivial — the IFC Part A names the one touched flow's nodes
- [x] What would change the recommendation — the packets' §5/§6 name it (a real clipped-suffix board; a bypassing render path)
- [x] Two-layer requirements — the §Two-layer table above, both chains complete

**`qa-reviewer` (self-executed by the coordinator — close-out):**
- [x] Acceptance criteria observable — AT-901/902/903 assert painted frames, file bytes, exit text — no "works"
- [x] Test cases have explicit Expected — TC-902's five exact strings; AT-903's exact legend lines and the `▼.*▲1 ◆` regex
- [x] Edge cases empty/boundary/invalid/error — the Boundary catalog fields: ☑ invalid (the three non-text shapes) · ☑ error (the refusing unlink) · ☑ empty (no-cards) · ☑ boundary (the exactly-full fold)
- [x] Regression checklist exists — the reverse census (5 probes × 2 increments) + the folded team_sync expectation + the 7-fold census; the close suite is the full regression
- [x] Exit criteria stated — §5.2's five criteria
- [x] No real PII/secrets — synthetic boards in `tmp_path` (the test file's docstring)
- [x] Mode declared — this artifact is the review record; the validation record declares its mode (`04-validation.md`)
- [x] Layer B through the shipped surface + bidirectional reachability — the reachability matrix in `04-validation.md`
- [x] No unfilled template — the close-out filled the contract's 12 placeholder cells; the two minors (F1/F2) are named

**`security-reviewer` (self-executed by the coordinator — close-out):**
- [x] Each finding: what · where · why · recommendation — F1/F2 above; the P2 history table keeps CL-1..CL-9
- [x] Each finding severity-rated — minor ×2 (current); the P2 blockers carry their folded status
- [x] No secret values in the output — none (the diff grep for secret patterns: 0 hits)
- [x] Verdict explicit, every HIGH ABSENT or verified — verdict OK, 0 HIGH; the two blockers this batch closes (S-4/S-9) carry their applied-and-verified evidence (TC-901/TC-902 + the M1/M2 kills)
- [x] New tool/integration scope — `n/a — no new tool or integration`

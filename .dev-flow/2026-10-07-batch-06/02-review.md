# Review — taskboard — Batch 2026-10-07-batch-06

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3
- **Out-of-scope findings:** `none`

- **Findings:** `0` blocker · `0` major · `0` minor
- **shall/should check:** ✓ clean — every HLR/LLR statement is `shall`-normative; rationales are informative and modal-free
- **Two-layer (blockers):** ✓ every story has an `AT` (US-1201 → AT-1201 · US-1202 → AT-1202) · output reqs name deliverable+observation (the painted tile rows + the amended frames; the phase-head row + the help bullet) · both trace chains complete (US → HLR-1201/1202 → LLR-1201.1/.2 · LLR-1202.1 → the named TC files; US → AT → the outcomes through the shipped surface) · ATs are genuinely black-box (AT-1201 drives keys through the app pilot and asserts the painted surface + the board state; AT-1202 renders the shipped surface and reads the emitted rows)
- **Census (change-first):** done — best-effort + gate-confirmed (the increment gates carry the five reverse-census probes per packet)
- **Security:** ✓ no findings — the new tile strings are S1-escaped via the shipped seams: `_chainmap_open_tile` clips by visible width and the `_ChainmapCanvas.line()` escapes every run (`views.py:5659-5668`), verified by the hostile-title arm family staying green (TC-807 + the session's 80-cell hostile-tile probe in `evidence/inc001-run.log`); the window markers/help bullet carry no user text
- **Evidence checklists (architect / qa / security):** `core` mode — the coordinator's lens covered the contract; the increment packets carry the evidence tables

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| — none — | | | | | | |

**TWO declared observations** (not findings — writing/process notes the gate records, both folded):

| # | Observation | Folded where |
|---|-------------|--------------|
| (a) | The contract specified the window-marker glyphs (`◂` / `▸ N`) without checking the shipped chrome: the product had hidden-phase marks in a prior form (`◀ N` / `N ▶`), pinned by `test_app.py`'s window test. A writing defect caught at review — the batch refines rather than invents (form refined, count kept, left-edge case + `?` bullet added; the operator's real gap was discoverability). | increment-001's packet §1 · the close's lessons |
| (b) | Three pinned tests reddened by LAYOUT, not mechanism, when the tiles landed — each update is law-driven and named: **TC-810** (fixture now pdwh-only + 6 added chains for a deterministic partial band; the cap's N counts chains AND tiles), **AT-802** (pilots (118,30) → (118,32) — Data Warehouse's band grew two tile rows), **AT-801c** (reselects API's `ta4`; the old fixture's 4 added chains removed — DWH itself no longer fits at 80×24). Assertions on the laws' thresholds were not weakened anywhere. | increment-002's packet §4 |

**A worked example — text to read, never rows of your record.** It sits in a fence so that nothing has to be deleted: a row copied out of it would claim a finding nobody raised. Write your own rows in the table above.

```text
| *(example)* F1 | architect | blocker / major / minor | | | | open / fixed |
```

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean — HLR-1201/1202 and LLR-1201.1/.2 · LLR-1202.1 are `shall`-normative throughout; the
rationales and the boundary-catalog notes are informative and modal-free.

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing requirement names its observable deliverable + observation method; (c) BOTH traceability chains complete (behavioral US→AT→outcome + functional US→HLR→LLR→TC); (d) each `AT` is genuinely black-box — drives the surface, asserts the outcome, references NO internal symbol.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-1201 / HLR-1201 / LLR-1201.1/.2 | yes (AT-1201) | yes (the painted `○` tiles + the amended frames' bytes, observed through the app pilot and the byte-exact frame arms) | yes (US-1201 → HLR-1201 → LLR-1201.1/.2 → `test_chainmap{,_app}.py`) | yes (keys through `run_test`; the `line_map`/`depends_on` reads are the observed surface state) | ✓ |
| US-1202 / HLR-1202 / LLR-1202.1 | yes (AT-1202) | yes (the phase-head row + the `?` bullet, observed on the rendered surface) | yes (US-1202 → HLR-1202 → LLR-1202.1 → `test_kanban_window.py`) | yes (renders the shipped kanban/help; no internal symbol) | ✓ |

### Supersession census (change-first)
> Planned new/moved/edited files checked against EVERY guard family (behavioral-placeholder · structural/placement · AST-composition · frozen-module). State reservations; the increment gate is the completeness guarantee, not this census.

`views.py` (edited) × `tests/test_chainmap.py` · `tests/test_chainmap_app.py` ·
`tests/test_app.py` · `tests/test_kanban_readable.py` (edited) × `tests/test_kanban_window.py`
(new): families run — the frozen-module family is clean (no frozen interface's signature moved:
`_phase_window`'s return, `_chainmap_nav`'s column-list shape, the picker/unlink seats in app.py
untouched); the AST-composition family is clean (`_chainmap_plan`'s 3-tuple bands' three unpack
sites all updated in the same edit — `views.py:5794,5977,6012`; the session's leftover-2-tuple
probe found none); the behavioral-placeholder family is clean (the `no links` row survives only in
the `bare` branch; the amended frames carry no instance of it); the structural/placement family is
clean (the `FRAMES` path moved with the LED cited; the sealed batch-02 path has 0 surviving refs).
Reservations: none. The increment gates carry the five reverse-census probes per packet.

### Security review summary
✓ no findings — `human:coordinator` self-executed the security lens (trigger family C; the runtime
spawned nobody). The only new user-text surface is the `○` tile row; it is clipped by visible width
and escaped through the shipped `_ChainmapCanvas` seams (`views.py:5751-5769` · `:5659-5668`), the
hostile-title arm family stayed green (TC-807 + the session's doubled-`[bold]` 80-cell probe), and
the window markers / help bullets carry no user text. The picker/unlink paths are the shipped,
previously-reviewed seats.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
> Attach each reviewer's completed evidence checklist (items in their agent files), ✓/✗ + one-line evidence.

`core` mode — self-executed by the close-out coordinator (`human:coordinator`): the contract lens
(shall/should · two-layer · supersession · security above) is complete; the per-increment evidence
tables (instruments · mutations · emitted forms · evidence files with sha256 · load-bearing
emptiness · reverse census) live in the two packets; the validation evidence checklist is in
`04-validation.md`. Reviewer: `human:coordinator`.

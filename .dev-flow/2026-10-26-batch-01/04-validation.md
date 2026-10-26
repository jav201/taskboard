# Validation — taskboard — Batch 2026-10-26-batch-01 (audit of shipped f4b53cc)

> **Artifact language.** English. Phase 4 artifact of an AUDIT batch: the orchestrator consumed
> the change's own gate evidence and the audit's targeted re-runs; the qa and ux lenses
> evaluated. The ONE complete gate-suite evidence is the change's three sequential chunk
> transcripts (consumed, not re-run — the operator's rule: the change's 3 chunks are its
> evidence; full-suite re-runs are not owed by the audit).

**`Mode`:** `validation`

## ✅ Verdict (read first)

- **Result:** PASS-WITH-NOTES
- **Gate run (consumed):** the change's own three sequential chunks at HEAD `f4b53cc` —
  1440 + 961 + 879 = **3280 passed, 0 skipped, 0 failed** = baseline 3278 + 2 new nodes
  (`evidence/scratch-evidence/suite-chunk0{0,1,2}.txt`).
- **Targeted re-runs (executed by this audit, qa lens):** import probe → worktree
  (`evidence/import-probe.txt`); `tests/test_gantt.py tests/test_gantt_board.py
  tests/test_archive.py` → **123 passed, 0 failed** (`evidence/suite-targeted.txt`);
  supplemental diffed files (`test_gantt_polish.py`, `test_colour_budget.py`,
  `test_milestone_marks.py`) → **62 passed, 0 failed** (`evidence/suite-targeted2.txt`).
  All with `env -u NO_COLOR python -m pytest` after the import probe, from the worktree root.
- **Golden-file verdict (trigger B3, the batch's key risk): CLEAN** — the regenerated sealed
  oracle `.dev-flow/2026-10-20-batch-01/evidence/frames-base.json` moved exactly **4 of 40
  frames (`gantt@{40,80,118,160}`, `.plain` field only; `row0_spans` untouched)**; the other
  36 frames byte-identical; HEAD regeneration reproduces the committed golden exactly; the
  `frames_base.py` +3 lines are docstring-only. Intermediate regen artifacts:
  `evidence/qa-regen-baseref.json`, `evidence/qa-regen-head.json`, `evidence/qa-tmp-base.json`,
  `evidence/qa-tmp-head.json`.
- **Real-terminal layer (ux lens):** 4 captures at `evidence/captures/png/` — 118x30 and 80x24
  of a board with open+done+archived work, and a busy board at 80x24 flag-on vs flag-off (G3).
  Window-cleanup assertion PASS; colour checks PASS (≥8 colours, none black; 358-458 distinct
  colours per PNG).
- **Requirements:** 5/5 HLR pass retroactively (AT-3001..AT-3006 map to existing nodes; the
  four commissioned coverage cases all present). 0 blocker fails.
- **Why PASS-WITH-NOTES and not PASS:** two HIGH records-layer findings (AX-1 stale canon,
  AX-2 stale toast string) and one MEDIUM (AX-3 legend gloss) are open against the shipped
  change; none invalidates the behaviour, all carry proposed fixes, all are queued in
  `.dev-flow/BACKLOG.md` — the orchestrator decides.

## Evidence checklist

| Evidence | State | Executor |
|---|---|---|
| `evidence/scratch-evidence/suite-chunk0{0,1,2}.txt` (3280 passed) | consumed (moved here by `git mv` from `.scratch-evidence/`, committed with the change) | the change's own run |
| `evidence/import-probe.txt` | executed — worktree path | qa lens |
| `evidence/suite-targeted.txt` (123 passed) / `suite-targeted2.txt` (62 passed) | executed | qa lens |
| `evidence/qa-regen-*.json`, `evidence/qa-tmp-*.json` | executed — golden regen at base_ref vs HEAD | qa lens |
| `evidence/captures/png/*.png` (4) + `evidence/captures/README.md` + `capture-log.txt` | executed — real Windows Terminal | ux lens |
| `evidence/gate-p1.txt` | executed — 0 block at P1 | orchestrator |
| `evidence/gate-p2.txt`, `evidence/gate-p4.txt`, `evidence/gate-final.txt` | executed at the gates | orchestrator |

## Requirement verdicts

| Requirement | Verified by | Verdict |
|---|---|---|
| HLR-3001 (rows, G1) | AT-3001/3002/3005 + suite + captures 1-2 | pass |
| HLR-3002 (quiet look, G2) | AT-3001/3006 arms (✓ chip, no ▲, dimmed, no `over`) + capture 1 | pass |
| HLR-3003 (unchanged parts, G3) | fold/pressure arms + captures 3-4 (flag-on vs flag-off fold) | pass |
| HLR-3004 (presentation, G4) | AT-3004 + golden verdict CLEAN (36/40 frames byte-identical) | pass |
| HLR-3005 (nothing else + cursor) | AT-3003/AT-3006 + diff census (13 files, 2 source) | pass |

## Notes and named deltas

- TC-1902 (clipboard): not applicable to the audit's targeted runs; the consumed chunks report
  0 skips — the machine allowed Set-Clipboard that day (same convention as 2026-10-25-batch-02).
- Test rebaselines (CR-2/CR-4/CR-5, QA-2/QA-3/QA-4) are declared in the test docstrings with
  rationale; none is a silent weakening — each loosened pin carries a compensating arm or a
  documented G3 cause.
- `dev-flow-sync` (vault export): not-run — this bundle declares no `vault_root` deployment row.

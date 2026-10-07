# Close — taskboard — Batch 2026-10-06-batch-01

## Objective outcome

**US-604 shipped: moving a task's dates moves what waits on it** — the cascade engine
(`push_delta` by the added overlap, default; ONE measure, the shipped `link_overlap`), the
`+`/`-` bump and the task editor routed through it (one undo entry, atomic when >1 task, the
plain-text C-3 toast), `m` re-applying the last move under the next mode, and the per-project
`date_links` setting in the project editor. Three increments, each with a code review (two
revisions on 001 and 002/003), a 8-10 mutant battery (0 survived each), and a green gate.

## Numbers

- Suite at close: **2512 passed, 0 failed** (`evidence/close-gate.txt`); G-011 (the clipboard
  environment flake) did not fire.
- Tests added: 23 nodes in `tests/test_cascade.py` (TC-618..630) + `tests/test_cascade_app.py`
  (AT-607..611, TC-631..638).
- Contract: US-604, HLR-604, LLR-604.1-.5, AT-607..611, TC-618..638, D-626..D-634; ledger
  LED-2026-10-06-batch-01.1..8; canon folded (6 rows).
- Mutants: 10 + 8 + 9 = 27 killed across the three batteries, 0 survived.

## The operator's visual verdict (2026-10-07)

`taskboard-veredicto-b2b.json` (Downloads): **PV-612, PV-613, PV-614, PV-615, UXV-6 — all
accepted, no change requests.** The toast, `m`'s re-apply semantics, the 80-column form, the
select's placement (the D-627 re-siting) and the rule's visibility deferral to batch C are the
operator's own calls, on the close captures.

## How the work was done (a first for this repo)

Increment 003 was implemented by an external agent — **DeepSeek V4 Pro via OpenCode** — under a
coordinator-written brief (paths, contract sections, exact numbers, the discipline), with the
coordinator verifying scope, running the gates, and folding every review finding. A second
DeepSeek instance (V4.1 Flash) reviewed increments 001+002 read-only and found DS-1..DS-7, all
executed. The flow's own code-reviewer role passed each increment twice. The coordinator ran
the orchestration, the P2/P4 lens swarms, and every gate; the operator gave the kickoff
commission, answered the visual verdict, and owns the commit+push trigger.

## Human review ledger

| Artifact | Human review |
|---|---|
| The commission and the B2a/B2b split | ✅ the operator's own words, by authorization |
| The visual verdict (PV-612..615, UXV-6) | ✅ 2026-10-07, all accepted |
| The code | ❌ machine review only (code-review ×2 revisions per increment, a second-model review, three mutant batteries, four P4 lenses) |

## Carried to BACKLOG (the P4 residue + this batch's lessons)

- DS-5 (restore loops vs the tested primitive) · `bump_due` without a production caller ·
  `Plan.conflicts` unconsumed · the C-5 arm unreachable by construction · toast rungs below 80
  unpinned (degrade by design).
- Lessons: `NO_COLOR` must be UNSET (`env -u`), not empty — three lenses hit it; the mutation
  harness must restore-on-abort (a decode bug left a mutant applied once — caught by the
  baseline control and restored by hand); outside pytest, the offer seam must be replicated or
  the one-time offer eats the keys.

## Standing constraints honored

No commits/pushes/stashes by the implementing agents; the coordinator commits and pushes once,
after the operator's visual verdict — this document is written at that gate.

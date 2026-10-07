# PLAN — taskboard — Batch 2026-10-06-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 in both modes; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/docs/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-06-batch-01 |
| Objective | Batch B2b of the kg_mejoras plan (US-604, the D-601 pre-authorized B2a/B2b split): moving a task's dates moves what waits on it -- push by default (push_delta), a per-project setting (date_links), m per move; the cascade wraps bump_due / set_milestone; a milestone's due is authoritative (its start follows) |
| Standing authorization | Operator (Javier), 2026-10-06, commissioning B2b with "Adelante" in reply to the coordinator's offer to start it, after batch 2026-10-04-batch-02 closed under the terms the operator set at its kickoff; the B2a/B2b split itself was pre-authorized (D-601). Read from that commission chain: **Gates** — autonomous over this batch's gates, same two exceptions: a HIGH ONLY in tests/evidence (reviewer confirms product correct) OR a HIGH in the increment UNDER CONSTRUCTION may be fixed without stopping, RED-first, recorded and re-reviewed; STOP and report on a HIGH in code already approved or shipped, any security HIGH, any HIGH touching the operator's data. **Git** — the coordinator commits and pushes after verification and the operator's visual verdict; the implementing agent does NOT commit, push, stash, reset or checkout anything; merge: false (no PR). **Data safeguard** — date moves convert nothing the operator did not ask for key by key; tests and synthetic boards only; never open, read or write the operator's real board |
| First gate | exit 0 · `V7` did not fire — the installed bundle matches its manifest (0 block · 55 notice, every notice inherited from closed batches and declared there; `V15`/`V16`/`V17` not-run — no canon tree, no checkout table, no hooks on this runtime; `V30` half-run from the bundle, declared). Re-run after the rollover: 0 block — `V29` readback clean, the active batch's `decisions_log` is empty and the outgoing 17 entries sit in `.dev-flow/2026-10-04-batch-02/decisions-log.json` |
| Premises / RC-1 | `origin/main` == `HEAD` == `e085cef` (fetched 2026-10-06, nothing to rebase); RC-2: `git ls-remote --exit-code --heads origin` answered 2026-10-06. RC-1 (b): `git grep push_delta/date_links/plan_move origin/main` hits only closed dev-flow records — US-604's outcome is NOT already shipped |

## Triggers

Evaluated 2026-10-06 at P0 (`devflow-init.py --fired … --not-fired …`); probes in `evidence/p0-probes.txt`.

| Id | Verdict | Probe output |
|---|---|---|
| B1 | fired | reverse census: `bump_due` → test_milestones, test_momentum; `set_milestone` → test_milestones; `open_predecessors` → test_links, test_details_links; `depends_on` → 11 test files (kg_board, test_app, test_dependencies, test_details_links, test_gantt, test_gantt_board, test_gantt_link, test_links, test_link_migration, test_link_picker, test_milestones, test_setup_help) — re-validated per increment |
| B2 | not fired | no file moves planned; the cascade lands beside its primitives in `models.py` |
| B3 | not fired | `ls tests/goldens` → no such directory |
| B4 | fired | a move writes the board file the next render, the next load, the undo stack and team sync consume → output-then-consume AT (C-12) |
| A1–A4 | not fired (judged) | `docs/ARCHITECTURE.md` absent (no module map to probe — the family says "judged and said so"); no module created or moved: the cascade wraps `bump_due`/`set_milestone` in `models.py`, the keys in `app.py`; the same judgement as batches 2026-10-02-01..04 and 2026-10-04-01..02 (D-502, D-602) |
| C5 | fired | a cascade rewrites dates across the operator's board file in one save — a data write; undo in one step (the prototype's snapshot/restore) is part of the contract |
| C6 | fired | a new per-project setting (`extra["date_links"]`) — project fields ride team sync to teammates' boards |
| C8 | fired | new surfaces paint file-derived text (move toasts name tasks; the chain map names projects) → S1 Text pieces; scan at P1 |
| C1–C4, C7 | not fired | no auth, secret, external service, sensitive personal data or network surface added |
| D1 | fired | user-visible: `m` per-move override, the per-project setting, toasts, bars moving → ux-reviewer at P2/P4; captures 118×30 and 80×24 |
| D2 | fired | the round-6 verdict frames (C-1a/b/c/d, C-2, C-3) come from a rich-rendered prototype, not Textual: `m` and the setting are verified through the real app (C-16) |
| E1 | fired | ≥ 3 increments (architect note A-14 on the BACKLOG item: no move mode exists at base, P-17) |
| E2, E3 | not fired | no high risk declared beyond the board write family C covers; not a client deliverable |
| F2 | fired | `BACKLOG.md` header base ref `0447070` ≠ HEAD `e085cef` → reconcile at close |
| F1 | not fired | `V7` clean on the installed rev100 bundle |

## Where we are

**P4, the validation gate PASSED (2026-10-06)** — all four lenses PASS-WITH-NOTES, the
cross-increment threads verified, the coverage pins landed (TC-636/637/638), the captures
taken, the operator's visual verdict sheet built (`evidence/veredicto-b2b.html`, questions
PV-612..PV-615 + UXV-6). P3 history: Done: the rollover, P0 (triggers, US-604 READY),
P1 (4 iterations — every threshold executed, the ONE measure is the shipped `link_overlap`,
D-633), P2 (4 lenses, PASS iteration 4), increment 001 (the engine, TC-618..630, 10/10 mutants
killed), increment 002 (the `+`/`-` bump through the cascade with the plain-text C-3 toast and
one undo entry, `m` re-applying the last move under the next mode, AT-607/608 + TC-631, 8/8
mutants killed; gate 2501 passed + the declared G-011 flake). **Stopped per the operator:**
increment 003 (the editor's date save + the `date_links` setting in the project editor,
AT-609/610) comes next, then P4 and P5. All work is uncommitted by design — the coordinator
commits+pushes after the operator's visual verdict.

## Objective

Batch B2b of the kg_mejoras plan (US-604, the D-601 pre-authorized B2a/B2b split): moving a
task's dates moves what waits on it — push by default (`push_delta`: a dependent moves only by
the overlap the move ADDED), a per-project setting (`extra["date_links"]`: flag / push_delta /
together), `m` per-move override; the cascade wraps `bump_due` / `set_milestone`; a milestone's
due is authoritative (its start follows); done/archived never move and stop the chain;
`+`/`-` bumps and the editor's date saves follow the same rule.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-604 | READY | the only commissioned story; refinement in `01-requirements.md` §2.6 |
| P0 | in gate | this evaluation |

## Roadmap + increment plan

Provisional, sized at P1 — the architect note (A-14) estimates ≥ 3 increments:

- 001: the cascade engine in `models.py` (`plan_move`, `resolve_mode`, snapshot/restore, ONE
  overlap measure) ported from `cascade.py` against the shipped `Task.milestone`, proved by the
  prototype's own scenarios re-run as tests.
- 002: the move surfaces — `+`/`-` and the editor's date saves route through the cascade;
  `m` cycles the per-move override; toasts say what moved.
- 003: the per-project `date_links` setting surface (the C-2 frame's home) and its sync.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-06 | B2b opened by rollover from 2026-10-04-batch-02 | D-601's pre-authorized split; the operator's "Adelante" |
| 2026-10-06 | The rollover's one-commit rule lands at this batch's close commit instead of at P0 | the established practice of the last two cycles (batch-02's rollover landed in `f391be7` at its close); the coordinator's git authority opens after the operator's visual verdict, and the validator reads disk, not commits — no ghost window on disk |

## Risks / watch-items

- The cascade touches dates on the operator's real board at runtime (C5) · medium · per-move
  undo in one step (snapshot/restore), toasts that say what moved, the operator's data never
  opened by any test.
- `extra["date_links"]` rides team sync (C6) · low · lenient model: an unknown value reads as
  the default, never raises.
- The prototype predates `Task.milestone` (it reads `extra["milestone"]`) · low · A-14: re-derive
  the frames against the shipped field at P1.

## Conventions honored

- No commits, no push by the implementing agent; the coordinator commits+pushes after the
  operator's visual verdict (the standing authorization's Git clause).
- Supervised increments: propose → the gate → ≤4 source files with the reason declared · review
  packet → stop.
- Spanish for conversation, English for code and technical artifacts.

## Out-of-scope carries

- The chain map (kg_mejoras batch C) — BACKLOG.
- The link migration's cleanup-before-restore order (S-4) — BACKLOG.
- A task whose title is not text crashes the app (S-9) — BACKLOG.
- The kanban `?` legend reads the unfiltered board (K2-1) — BACKLOG.
- A late milestone below the kanban fold (UX2-2) — BACKLOG.
- A project with only milestones draws no kanban band (D-623) — BACKLOG.
- Milestones in lanes/agenda/focus draw as plain tasks — BACKLOG.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest tests -q` | 2026-10-06 | 2486 passed (the tree this batch opens on, `e085cef`) |

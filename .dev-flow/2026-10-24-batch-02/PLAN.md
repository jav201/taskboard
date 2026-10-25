# PLAN — taskboard — Batch 2026-10-24-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language.
> **Owed in.** `core` ✓ · `full` ✓
> Seeded by `/dev-flow-init` step 4 at both levels; the living plan is owed at every gate
> that follows (`/dev-flow` §Living plan is the rule's home).

> **Field guide:** `templates/guides/plan-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.
> **Two header labels are read literally and are never translated:** `Standing authorization` and `Last updated`; the field guide names their readers.

The living compendium of this batch: where-we-are · objective · per-story/per-station status ·
roadmap + increment plan · key decisions · risks/watch-items · conventions honored ·
out-of-scope carries · test ledger · decision log (the human-readable mirror of `state.json`).
**Create at batch open and update at every gate and significant checkpoint** — the
orchestrator presents the full plan in-conversation at each phase gate.

## Header

| Field | Value |
|---|---|
| Project | taskboard |
| Batch | 2026-10-24-batch-02 |
| Objective | The home defers the board's start; the directories stay fresh: with BoardsHome shown at start, the default board's start is deferred (no migration, sweep, presence marker, team start or milestone offer, and no write to the board file, until the user leaves the home onto a board); the start-up modals open over the chosen board; the open-twice notice fires only when a board is actually opened; single-board, --open and later-B paths unchanged; self.people and self.marks re-read their files cheaply on mtime/size change when the task editor, people directory, marks manager or /@#/ search open, and a failed re-read keeps the in-memory directory and notifies once (HD-1..HD-5) |
| Last updated | P5 · 2026-10-25 |
| Standing authorization | The commission `.dev-flow/COMMISSION-home-deferred-start.md`, quoting the operator's approval of 2026-10-24: «Ok, arréglalo.» — runtime cannot prompt; the commission is the standing authorization for every gate of this batch. Read from silence (commission names neither kickoff question): autonomy over the gates it commissions; merge NOT granted — the operator instructed «Do NOT push or merge.» Every autonomous decision is recorded in this plan's decision log, `state.json.decisions_log` and `05-close.md`. |
| First gate | Step-1 run of 2026-10-24 (before batch open): exit 0 — `0 block · 140 notice · 63 not applicable`. `V7` reported no file whose bytes disagree with the manifest (no `V7` line printed): the bundle is the revision it claims. |
| Premises / RC-1 | RC-1 (a) 2026-10-24: `git fetch origin` done; `origin/main` tip `ffedf0268c4ad9c5cfbb1553c23a693bf77d0308` is an ancestor of HEAD `4a647ab63bb234dc4db4e402ed41c6684f88e96a` — already rebased, no rebase needed; `base_ref` stamped `4a647ab63bb234dc4db4e402ed41c6684f88e96a`. RC-1 (b): already-shipped check per story — none of HD-1..HD-5 greps on `origin/main` (batch-03 item 8 A / D-12 are the pre-image defects, not shipped fixes). RC-2 2026-10-24: `git ls-remote --exit-code --heads origin` answered (exit 0, newest refs pushed within window). Batch opened by rollover from `2026-10-24-batch-01` (decisions log archived at `.dev-flow/2026-10-24-batch-01/decisions-log.json`), per `stations/shared-batch.md` §Batch rollover. |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| A1 | not fired | judged — no module is created and no boundary moves; the change stays inside `taskboard/app.py`, `taskboard/people.py`, `taskboard/marks.py` |
| A2 | fired | judged — the batch touches ≥2 modules: `taskboard/app.py` plus `taskboard/people.py` and `taskboard/marks.py` (increment 002 per the commission) → ARQ, PDR and DDR stand up |
| A3 | not fired | judged — no consumed interface changes: the deferred start refactors `TaskboardApp` internals (`on_mount`, `_open_board`, `switch_board`, `BoardsHome` actions) and ADDS re-read helpers to the directories; nothing another module consumes is re-signed |
| A4 | not fired | judged — the commission runs increments 001 and 002 sequentially, not in parallel |
| B1 | fired | `grep -rln "_open_board\|switch_board\|_enter_presence\|_init_team_mode\|_offer_milestones\|BoardsHome" tests/` → `test_boards_home.py`, `test_boards.py`, `test_boards_concurrency.py`, `test_people_directory.py`, `test_marks_manager.py`, … — symbols asserted by tests of other requirements → reverse census owed at P2/P3 |
| B2 | not fired | judged — no file changes location on disk |
| B3 | not fired | `ls tests/` and `grep -rln golden tests/*.py` → no `tests/goldens/` capture set; the hits are fixture names (`people_round_fixture.py`), not byte-identical golden captures of a touched source |
| B4 | not fired | judged — the change emits no artifact another component consumes |
| C1–C8 | not fired | judged — `devflow-scan-spec.py` families read at P1: no auth, secrets, external integration, sensitive data, destructive DB, network; C6 no new input surface (the re-reads are the two directory files the mount already reads); C8 no new markup/ANSI/HTML rendering over file-derived text (pickers render through the unchanged pipeline) |
| D1 | fired | judged — the change alters what the user sees and touches: the home at start, the timing of the start-up modals (now over the board), the disappearance of the false open-twice notice |
| D2 | not fired | judged — no prototype is built; the operator approved the fix as described, no prototype needed |
| E1 | not fired | judged — 2 planned increments, 1 story set (HD-1..HD-5) |
| E2 | not fired | judged — no high risk declared at intake |
| E3 | not fired | judged — not a client deliverable or regulated context |
| F1 | not fired | from a bundle — `V7`'s bundle-identity line is the probe: step-1 gate printed no `V7` disagreement (exit 0), so the bundle is the revision it claims |
| F2 | not fired | judged — `.dev-flow/BACKLOG.md` was refreshed at batch-01's close (commit `ffedf02` reconciles it); carries open carries this batch reads at intake |

## Where we are

P0 intake, complete: the batch opened 2026-10-24 by rollover from `2026-10-24-batch-01` (decisions
log archived); RC-1 verified against `origin/main ffedf02`, RC-2 answered; triggers evaluated (A2, B1,
D1 fired — ARQ, PDR and DDR stand up); both stories READY. Owed next: ARQ (the module map against the
real tree), then P1 requirements.

## Objective

The home defers the board's start; the directories stay fresh (HD-1..HD-5 of the commission): no
migration, sweep, presence marker, team start or milestone offer — and no write to any board file —
runs until the user leaves `BoardsHome` onto a board; the start-up modals open over the chosen board;
the open-twice notice fires only when a board is actually opened; the single-board, `--open` and
later-`B` paths are unchanged; `self.people`/`self.marks` re-read their files (mtime/size-gated) when
the editor, the people directory, the marks manager or the `@`/`#` search open, and a failed re-read
keeps the in-memory directory and notifies once.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-2701 (HD-1..HD-4, increment 001) | READY | the false open-twice notice + the deferred start; closes BACKLOG D-12 (blank screen behind the start-up modals) |
| US-2702 (HD-5, increment 002) | READY | fresh directories at the four open sites; closes BACKLOG A-7 |
| P0 | done | this commit |
| ARQ / PDR / DDR | up (trigger A2) | stations seeded; PDR reviews the design proposal with the architect, DDR with qa + ux |

## Roadmap + increment plan

1. **ARQ** — the module map in `docs/ARCHITECTURE.md` against the real tree (row 6a).
2. **P1** — requirements: HLRs/LLRs for HD-1..HD-5, ATs a–f keyed to test nodes, the IFC block, the
   security scan (`devflow-scan-spec.py`).
3. **P2** — the two-lens review (architect + qa lenses, per `02-review.md`).
4. **PDR** — `design/design-proposal.md` with the architect sub-agent; conditions folded into the
   increments.
5. **P3** — increment 001 (`taskboard/app.py`, HD-1..HD-4) then increment 002 (`people.py`,
   `marks.py`, `app.py`, HD-5), each with its packet, mutation battery and `code-reviewer` pass;
   then **DDR** (`qa-reviewer` + `ux-reviewer` over the shipped design).
6. **P4** — the full suite in 3 sequential chunks + the real Windows Terminal capture pair
   (118x30, 80x24) of the milestone offer over the chosen board, `h01-` titles, closed by title.
7. **P5** — close: fold the canon, the BACKLOG reconciliation, the validator's final run.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-24 | Trigger A2 fired → ARQ, PDR and DDR stand up; B1 (reverse census) and D1 recorded | the batch touches ≥2 modules and alters what the user sees; the operator's swarm spec names the architect at the PDR and qa/ux at the DDR |
| 2026-10-24 | A3 judged not fired | no consumed interface is re-signed; the directories only gain re-read helpers |
| 2026-10-24 | Standing authorization quotes «Ok, arréglalo.»; merge NOT granted | the commission is the kickoff answer on a runtime that cannot prompt; the operator forbade push/merge |

## Risks / watch-items

- The full-suite baseline carries one environmental skip (clipboard arm TC-1902 / G-001, machine-wide
  clipboard fault at batch-01's P4); if it fires again at this P4 it is declared environmental like
  batch-01's — any OTHER skip or fail blocks the close.
- `switch_board`'s same-board early return must still run the deferred start once (HD-1) — a double
  start would re-announce presence; AT-b pins "exactly once".
- Increment 001 touches `taskboard/app.py` alone; the commission allows `boards.py` only if the
  presence helper needs it — the budget is 4 SOURCE files per increment, tests uncapped.

## Conventions honored

- Code, artefacts and commits in English; synthetic data only; the operator's placeholder is
  `username_subject`.
- pytest under `env -u NO_COLOR`; `PYTHONDONTWRITEBYTECODE=1` and `PYTHONIOENCODING=utf-8` in every
  flow-script shell call.
- No destructive git; no push, no merge; every commit trailer
  `Co-Authored-By: Kimi (kimi-for-coding) via Claude Opus 5.5 orchestration <noreply@anthropic.com>`.
- Scratch in `.scratch/` (git-excluded), deleted at close.

## Out-of-scope carries

- The home's other behaviours (due-strip overflow, `file unreadable` card path) — BACKLOG, untouched.
- A plain board save taking no lock, the team-pull unarchive rank — BACKLOG lanes of earlier batches.
- `check_action`'s widened refusal (batch-01 DDR notice) — already shipped there; the operator
  confirms the behaviour change.

## Gate notices and runtime absences

Runtime mechanisms unavailable on this runtime (named once, per `SKILL.md` step 5): no slash commands,
no named reviewer roles registered with the host, no flow-guard hooks, no operator prompt channel —
the batch therefore runs UNGUARDED except the validator, and the gates close under the standing
authorization declared in the header. Reviewer roles ARE executed as independent generic sub-agents,
each spawned with its role file from the bundle's `agents/` (an author never reviews their own work);
each packet's §4b names the role and how it ran. Rules that genuinely cannot run from a bundle are
recorded `not-run` with the printed reason: `V15`, `V16`, `V17` (no canon tree / checkout table /
settings.json hook); `V30` runs half (witnesses the interpreter; the three derived floors are not
derivable from a partial file set — declared, not a pass). `V25` (no `origin` remote) does not fire
here — `origin` exists and answered RC-2. `commands/dev-flow-sync.md` is `not-run`: no `vault_root`
deployment record ships with a bundle.

Per-gate NOTICEs, as the runbook's §*Expected NOTICEs* table predicts, and why they stand:

- **Step 1 (flow identity):** `V18`, `V27`, `V42` — no batch existed yet; `V40` — the inherited
  `state.json` named another checkout (`ms-impl`); all leave at this batch's open. `V30` stands at
  every gate (bundle install). `V57` on batch-01's close record — expected the moment its close
  commit landed; historical.
- **Step 3 (batch open):** `V9`, `V27`, `V31`–`V38`, `V41`, `V43`–`V51`, `V54` on the freshly seeded
  placeholders — each leaves when the row whose page fills that field is done. `V42` leaves with this
  open commit. `V60` does not fire: the trigger evaluation is recorded before any `--station` move.
- **Historical corpus notices** (`V9`/`V13`/`V22`/`V23`/`V42`/`V53` lines over batches closed before
  this one): read and declared as history — `shared-controls.md` says the validator lights up on
  records written before rules existed, and re-anchoring a closed record would be editing the past.
  None names this batch's record.
- **Increment gates (expected):** `V53` (records naming test nodes Phase 3 has not written yet),
  `V27`/`V36`/`V56` at step 9 per the table, `V62` between a `--station` move and this plan's rewrite.
- **Close (expected):** `V57` `1 commit(s)` right after the close commit.

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `env -u NO_COLOR python -m pytest -q <increment nodes>` (per increment) | not yet — P3 | — |
| full suite, 3 sequential chunks at P4 | not yet — P4 | baseline from batch-01: 3235 passed + 1 environmental skip (G-001) |

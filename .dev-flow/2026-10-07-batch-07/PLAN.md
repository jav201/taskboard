# PLAN — taskboard — Batch 2026-10-07-batch-07

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
| Batch | 2026-10-07-batch-07 |
| Objective | Templates batch: process/chain templates insertable into a project -- user templates live in the board's settings (portable), factory presets ship as examples; key `I` opens the picker (the contract's original `T` was corrected under LED-2026-10-07-batch-07.2 before the first edit -- `T` ships `project_pin_toggle`); the insert creates the tasks in the selected task's project with their depends_on chains, ONE undo step, no invented dates; v1 edits templates in the board JSON (the ? documents it); 'save this chain as a template' is a v2 carry |
| Standing authorization | Operator (Javier), 2026-10-07: "Creo que falta algo que no vi y es el crear templates de procesos o templates de cadenas que se reflejan en tareas que se pueden insertar a proyecto." Read with the established chain: Gates -- autonomous with the two exceptions; Git -- the COORDINATOR commits and pushes at each close (no PR); data safeguard -- synthetic boards only; implementing agents (DeepSeek instances under coordinator briefs) do NOT commit/push/stash; the batch-06 visual re-verdict stays pending in the backlog. This batch runs in the MAIN checkout. (Verbatim in `state.json` `standing_authorization.operator_words`.) |
| First gate | the batch opened by rollover from 2026-10-07-batch-06 (`1cf2f74`); the seed readback was clean (state.json `batch_id` rolled to 2026-10-07-batch-07, the ledger seeded with LED-2026-10-07-batch-07.1); the validator baseline at the seed (re-run at this close, before the record fills) read **1 block · 51 notice · exit 1** — the one block `V26`: the ledger's LED .2 pairings existed only in the ledger, the live contract's HLR-1301/LLR-1301.2 `Ledger:` fields named .1 alone; fixed at this record pass (both fields now name `.1 · .2`) |
| Premises / RC-1 | RC-1: local HEAD `1cf2f7475f8a1981b03e88478eda7dcbe92f2fde` == `origin/main` as of the batch's open (pushed at batch-06's close; re-verified at this close by `git rev-parse HEAD origin/main`); premises P-1..P-2 in `01-requirements.md` §2.7, all TRUE with executed evidence (P-1: the shipped patterns cover every mechanism — the LinkPicker family, the milestones one-step undo, the presentation's project resolution, batch-06's `○` tiles; LLR-1301.2 composes them, nothing invented · P-2: a template's `wait` chain is forward-only by construction — cycles impossible, a malformed index degrades to one unlinked task, pinned by the lenient-read arm) |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| — | not evaluated | `state.json`'s trigger block still reads "NOT EVALUATED" at this close — the P0 trigger evaluation was not rewritten this batch; no trigger fired on the evidence available (the batch's work came from the operator's direct request, not a trigger probe) |

## Where we are

Batch CLOSED at the record level, 2026-10-07: increment 001 (the whole batch) implemented across
two sessions — the first STOPPED before writing code and named the `T`-key conflict, the second
shipped green after the contract correction to `I` (LED-2026-10-07-batch-07.2). Suite green at
2575 (the shipping session's full run, 423.20s; re-collected at 2575 by the close-out), the
coordinator's mutation battery M13-M15 all KILLED, the record filled (packet · review `approve` ·
validation PASS · this close). Owed next: the orchestrator's ONE C-25 run; the coordinator's
commit + push + `--fold-canon` (the V22 discharge); and the standing carries — the batch-06 visual
re-verdict (still PENDING) and template authoring v2 (the declared carry, now in the backlog).

## Objective

Restated: press `I`, pick a template, and the project's chain of tasks exists — linked exactly
as the template declares, named, no invented dates, undoable in ONE step, with the outcome toast.
User templates live in the board's `settings["templates"]` (portable; edited in the board JSON at
v1, documented in the `?` help); the `Simple chain` and `Bugfix` presets ship as examples;
`T` was never available — the key is `I`.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1301 (templates insertable into a project) | ✅ done — AT-1301 green | the store + the picker + the insert + one-step undo + the toast; 9 arms; M13/M14/M15 KILLED; LED .1 (the contract) + LED .2 (the T→I correction) |
| P0..P5 stations | closed at the record level | two implementing sessions under one brief (the first wrote nothing); the coordinator's review gate `approve` (0 blocker · 0 major · 1 minor, F1 fixed); validation PASS |

## Roadmap + increment plan

Increment 001 — the whole batch (HLR-1301 · LLR-1301.1 the store · LLR-1301.2 the insert).
Executed as planned; the only deviation from the first brief was its `T` key, corrected under
LED .2 before the first edit.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-07 | the templates key is `I`, not `T` (LED-2026-10-07-batch-07.2) | `T` ships `project_pin_toggle` (keymap.py:86), pinned by test_focus.py:46/:151 and test_markup_sites.py:267; the implementing agent's stop gate caught it before any code; re-keying `project_pin_toggle` would have touched files outside the budget without a verdict |
| 2026-10-07 | a malformed task skips the WHOLE template entry; a bad `wait` drops only that link | dropping a mid-chain task would silently rewire the `wait` indices; a bad link degrades to one unlinked task (P-2) — reasoned in the session's report, pinned by the store arms, recorded in `evidence/mutations.log`'s review notes |
| 2026-10-07 | the README `I` row ships inside the increment | the shipped census test `test_keymap.py:404` enforces every bound key documented; the row is `doc`, outside the source budget — declared, accepted |
| 2026-10-07 | v1 authoring stays in the board JSON; "save this chain as a template" is a v2 carry | the operator asked for insertion; authoring is a separate surface with its own contract — declared in HLR-1301, landed in the backlog at close |

## Risks / watch-items

- a user template named exactly `Simple chain`/`Bugfix` shadows the preset silently (the pick resolves by name, user first) — declared in increment-001's packet §5
- a fat-fingered `settings["templates"]` list degrades silently (the lenient read skips — by design, M15-pinned); the `?` bullet is the documentation seat until v2 authoring lands
- the undo branch removes created ids wholesale — the same dangling-`depends_on` exposure the shipped milestones undo carries; inherited, declared

## Conventions honored

- synthetic boards only (every fixture in `tmp_path`; no operator board data)
- the stop-and-name gate: "if anything outside your files reddens, STOP and name it" — executed to the letter (the first session stopped BEFORE writing code)
- English artifacts; reserved field names literal; no git mutations by the implementing sessions or this close-out

## Out-of-scope carries

- template authoring from the app ("save this chain as a template") = v2 — declared in HLR-1301, landed in `.dev-flow/BACKLOG.md` at close
- the batch-06 visual re-verdict (amended C-2b frames + the new chrome) — PENDING in the backlog, not this batch's gate

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest tests/test_templates.py tests/test_templates_app.py -q` (the shipping session) | 2026-10-07 | 9 passed, 0 failed (2.17s — `evidence/inc001b-run.log`) |
| `python -m pytest tests -q` (the shipping session's one full run) | 2026-10-07 | 2575 passed, 0 failed (423.20s — `evidence/inc001b-run.log`); the orchestrator's C-25 owns the ONE final clean-tree run |
| `python -m pytest tests --collect-only -q` (the close-out) | 2026-10-07 | 2575 tests collected |
| the coordinator's battery M13-M15 (byte-level, restores sha256-verified) | 2026-10-07 | 3 mutants, all KILLED (`evidence/mutations.log`) |

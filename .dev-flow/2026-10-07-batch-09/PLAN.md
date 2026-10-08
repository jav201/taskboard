# PLAN — taskboard — Batch 2026-10-07-batch-09

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
| Batch | 2026-10-07-batch-09 |
| Objective | Templates v3: authoring from scratch — the `I` picker gains a leading `New template...` row (reserved id `__new__`, not a template): a small editor (ONE name field + ONE multi-line tasks field, one task per line) saves a linear-chain template into `settings["templates"]` through the batch-08 save/toast contract verbatim; empty lines skipped, lines trimmed; an all-empty edit saves nothing and says why in one line; esc cancels with nothing written; the `?` bullet notes notes stay JSON-only at this version |
| Standing authorization | Operator (Javier), 2026-10-07/08: "No puedo hacer una plantilla desde cero tambien?" — template authoring from scratch. Read with the established chain: Gates — autonomous with the two exceptions; Git — the COORDINATOR commits and pushes at each close; data safeguard — synthetic boards only; DeepSeek implements under coordinator briefs; this batch runs in the MAIN checkout. (Verbatim in `state.json` `standing_authorization.operator_words`.) |
| First gate | the batch opened by rollover from 2026-10-07-batch-08 (`5c4c28a`); the seed readback was clean (`state.json` `batch_id` rolled to 2026-10-07-batch-09, the ledger seeded with LED-2026-10-07-batch-09.1); the validator baseline at the seed (re-run at this close, before the record fills, over the unchanged seed files) read **0 block · 52 notice · exit 0** — the 52 notices all historical or placeholder-class (V31-V44/V47-V51/V54 over the unfilled seeds, cleared by this record pass) |
| Premises / RC-1 | RC-1: local HEAD `5c4c28ad075ded9152251604d490dc244f293169` == `origin/main` as of the batch's open (`state.json` `base_ref`; re-verified at this close by `git rev-parse HEAD origin/main` — both still at `5c4c28a`); premises P-1 in `01-requirements.md` §2.7, TRUE with executed evidence (P-1: the v1 store + the `I` picker + the batch-08 save ship and green — scratch authoring reuses the store/picker seats and the same save/toast contract, verified by `git show 979cf59 --stat` + the green suite) |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| — | not evaluated | `state.json`'s trigger block still reads "NOT EVALUATED" at this close — the P0 trigger evaluation was not rewritten this batch; no trigger fired on the evidence available (the batch's work came from the operator's follow-up, not a trigger probe) |

## Where we are

Batch CLOSED at the record level, 2026-10-08: increment 001 (the whole batch) implemented in ONE
shipping session (DeepSeek V4 Pro under the coordinator's brief) — the picker row (`modals.py:933-985`,
reserved id `__new__` at `:967`), the editor (`modals.py:987-1031`), the route + save
(`app.py:741-746` · `:814-843`, the `wait` chain at `:835`), the `?` bullet (`views.py:6837-6838`),
the 6-arm test file. Suite: the session's full run reported `5 failed, 2587 passed` — all five
pre-existing picker-shape arms the contract's FIRST-row law reddened; the session STOPPED and named
them; the coordinator's five law-driven fixture updates closed them (15/15 template arms green;
`evidence/mutations.log`). The coordinator's close-out battery M18 KILLED; the record filled
(packet · review `approve` · validation PASS · this close); the suite re-collected at 2592.
Owed next: the orchestrator's ONE C-25 run; the coordinator's commit + push + `--fold-canon`
(the V22 fold-back the final gate fired for `HLR-1501` · `LLR-1501.1` — the close's §0 records
the pair as the coordinator's standing discharge).

## Objective

Restated: `I` → `New template...` → a name + the tasks one per line → the template exists from
then on. The saved template lives in the board's `settings["templates"]` as a linear chain, lists
in the `I` picker after the authoring row, and inserts through the batch-07 insert; an all-empty
edit saves nothing with a one-line why; esc cancels with nothing written; the toast reads
`Template '<name>' saved — <N> tasks`; authoring is not an undo step; notes stay JSON-only at this
version.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1501 (author a template from scratch) | ✅ done — AT-1501 green | the picker row + the editor + the route/save + the `?` bullet; 6 arms; M18 KILLED; LED .1 (the contract); the five law-driven fixture updates as the contract-ripple record |
| P0..P5 stations | closed at the record level | one implementing session under one brief; the coordinator's review gate `approve` (0 blocker · 0 major · 0 minor, one declared observation); validation PASS |

## Roadmap + increment plan

Increment 001 — the whole batch (HLR-1501 · LLR-1501.1 the editor modal and the linear-chain
shape). Executed as planned; the only deviation from a green first pass was the contract's own
ripple — the FIRST-row law reddened 5 pre-existing pinned tests, which the session named and the
coordinator updated law-driven (declared in the packet and `02-review.md` observation (a)).

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-07 | the authoring row carries the reserved id `__new__`, not a template index | the house pattern the `L` link picker's "+ create" row already ships (`modals.py:872`/`:922`): the selection handler recognises the id instead of indexing into `_templates`; template rows keep stable index ids |
| 2026-10-07 | the editor is the lightest house-consistent composition | `VerticalScroll(id="modal-box", classes="modal")` + `Input` + the app's shipped `TextArea` + buttons, ONE `DEFAULT_CSS` rule, no `.tcss` touched — `TextArea` already ships (TaskModal's notes), the shell is `ProjectModal`/`TextPrompt`'s (the session's tcss census, `evidence/inc001-run.log:20-47`) |
| 2026-10-07 | the save rides the batch-08 contract verbatim | the same `settings.setdefault("templates", []).append(...)` seam, `save()`, the pinned toast literal, `markup=False`; the linear chain is the only new shaping (`entry["wait"] = i - 1`, `app.py:835`) — one contract, two authors |
| 2026-10-07 | the five pre-existing reds are the coordinator's law-driven fixture updates, not the session's | the brief's "Nothing else" cap; the session STOPPED and named all five; the coordinator enumerated the population before the first edit and updated assertions without weakening them (`evidence/mutations.log`) |
| 2026-10-07 | authoring is NOT an undo step; notes stay JSON-only | the batch-08 rule (settings, not tasks), docstring-pinned at `app.py:814-822`; v1 scope declared in HLR-1501 and the `?` bullet |

## Risks / watch-items

- a scratch template named exactly `Simple chain`/`Bugfix` shadows the preset silently (the pick resolves by name, user first) — inherited from batch-07, declared
- the degenerate one-task save toasts `1 tasks` — the pinned literal the app arm asserts; changing it reddens the arm
- the FIRST row changes every future picker fixture — the cost the five updates paid; named in the packet
- authoring is unreachable without a resolvable project (the batch-07 `No project to insert into.` guard runs first) — the shipped seat's semantics, declared

## Conventions honored

- synthetic boards only (every fixture in `tmp_path`; no operator board data)
- the seat census before the write: the session's greps over the picker/tests seats (`evidence/inc001-run.log:100-113`), re-run at this record
- English artifacts; reserved field names literal; no git mutations by the implementing session or this close-out

## Out-of-scope carries

- none — the batch's only item (the operator's scratch-authoring follow-up) shipped; the backlog's Open-after-batch-09 section reads "nothing new"; the G-011 flake stands as the only standing item

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest tests/test_template_new.py -q` (the shipping session) | 2026-10-07/08 | 6 passed, 0 failed (3.50s — `evidence/inc001-run.log:440`) |
| `python -m pytest -q` (the shipping session's one full run) | 2026-10-07/08 | `5 failed, 2587 passed` (455.47s — `evidence/inc001-run.log:483`; the 5 failures ALL pre-existing picker-shape arms, named at `:529-537`; NOT the G-011 flake); the coordinator's five law-driven fixture updates then closed them (15/15 template arms green — `evidence/mutations.log`); the orchestrator's C-25 owns the ONE final clean-tree run |
| `python -m pytest tests --collect-only -q` (the close-out) | 2026-10-08 | 2592 tests collected (2586 − 0 + 6; 0.62s) |
| the coordinator's battery M18 (byte-level, restore sha256 OK) | 2026-10-08 | 1 mutant, KILLED (`evidence/mutations.log`) |

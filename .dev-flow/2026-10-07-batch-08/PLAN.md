# PLAN — taskboard — Batch 2026-10-07-batch-08

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
| Batch | 2026-10-07-batch-08 |
| Objective | Templates v2: authoring — save a chain as a template from the app: on the chain map, `,` on a selected tile opens the one-line name prompt (prefilled with the chain's first title); typing a name + enter stores the tile's whole open component — BFS both directions through `depends_on` within the project, open tasks only, deterministic topological order by (depth, board order), a fan-in keeps its FIRST predecessor (dropped rest, declared) — into `settings["templates"]` under that name; the board is saved, the pinned toast renders, and the template lists FIRST in the `I` picker from then on; saving is NOT an undo step (declared) |
| Standing authorization | Operator (Javier), 2026-10-07: "si no hay nada que decidir continua junto con deepseek lo que sigue" — the queued carry is template authoring v2. Read with the established chain: Gates — autonomous with the two exceptions; Git — the COORDINATOR commits and pushes at each close; data safeguard — synthetic boards only; DeepSeek implements under coordinator briefs; the batch-06 visual re-verdict sheet shipped with this batch's open and was folded by the coordinator (commit `762d18c`, all four accepted) before this close. This batch runs in the MAIN checkout. (Verbatim in `state.json` `standing_authorization.operator_words`.) |
| First gate | the batch opened by rollover from 2026-10-07-batch-07 (`9a13c12`); the seed readback was clean (`state.json` `batch_id` rolled to 2026-10-07-batch-08, the ledger seeded with LED-2026-10-07-batch-08.1); the validator baseline at the seed (re-run at this close, before the record fills, over the unchanged seed files) read **0 block · 52 notice · exit 0** — the 52 notices all historical or placeholder-class (V31-V44/V47-V51/V54 over the unfilled seeds, cleared by this record pass) |
| Premises / RC-1 | RC-1: local HEAD `9a13c12b5116e75c76b2b7978e995eb874045e38` == `origin/main` as of the batch's open (`state.json` `base_ref`; re-verified at this close by `git rev-parse HEAD origin/main` — both now at `762d18c`, the batch-06 verdict commit the coordinator landed on top of the base, docs-only); premises P-1 in `01-requirements.md` §2.7, TRUE with executed evidence (P-1: the batch-07 store + picker + insert ship — authoring only writes `settings["templates"]` and reuses the read/insert seats, verified by `git show bafa1e3 --stat` + the green suite) |

## Triggers

The trigger evaluation `state.json`'s `triggers.record` points at: one row per trigger evaluated, fired or not.

| Id | Verdict | Probe output |
|---|---|---|
| — | not evaluated | `state.json`'s trigger block still reads "NOT EVALUATED" at this close — the P0 trigger evaluation was not rewritten this batch; no trigger fired on the evidence available (the batch's work came from the operator's queued carry, not a trigger probe) |

## Where we are

Batch CLOSED at the record level, 2026-10-07: increment 001 (the whole batch) implemented in ONE
shipping session (DeepSeek V4 Pro under the coordinator's brief) — the component walk
(`models.chain_template`), the action + named callback (`app.action_chain_template_save` /
`_on_chain_template_named`), the view-scoped `comma` key, the `?` bullet, the README row (forced
by the shipped census test). Suite: the session's settled full run passed 2585 with the one
declared G-011 environmental flake (437.37s); re-collected at 2586 by the close-out. The
coordinator's close-out battery M16-M17 both KILLED; the record filled (packet · review `approve`
· validation PASS · this close). Owed next: the orchestrator's ONE C-25 run; the coordinator's
commit + push + `--fold-canon` (the V22 fold-back the final gate fired for `HLR-1401` ·
`LLR-1401.1` — the close's §0 records the pair as the coordinator's standing discharge).

## Objective

Restated: on the chain map, `,` on a selected tile → type a name → the chain is a template from
then on. The saved template lives in the board's `settings["templates"]`, lists first in the `I`
picker, and inserts through the batch-07 insert; esc/empty cancels with nothing written; the toast
reads `Template '<name>' saved — <N> tasks`; saving is not an undo step.

## Per-story / per-station status

| Story / station | Status | Notes |
|---|---|---|
| US-1401 (save a chain as a template) | ✅ done — AT-1401 green | the walk + the action + the view-scoped key + the doc seats; 11 arms (7 unit + 4 app); M16/M17 KILLED; LED .1 (the contract) |
| P0..P5 stations | closed at the record level | one implementing session under one brief; the coordinator's review gate `approve` (0 blocker · 0 major · 0 minor, two declared observations); validation PASS |

## Roadmap + increment plan

Increment 001 — the whole batch (HLR-1401 · LLR-1401.1 the component walk and the template shape).
Executed as planned; the only deviations from the brief were its group guess (`chains` → the
shipped `task`) and the unlisted README row (forced by the shipped census test), both declared.

## Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-10-07 | the key NAME is `comma`, the display is `,` | a literal `,` in Textual's binding grammar is the alias separator — the first construction died at collection (`InvalidBinding: Can not bind empty string`); the session probed Textual's key machinery and bound the canonical name (`evidence/inc001-run.log:978-1052`) |
| 2026-10-07 | the order is (depth, board order); the fan-in keeps the FIRST predecessor | depth = the longest `depends_on` path from a chain head (the chain map's own column rule) makes every `wait` point backward deterministically; the template shape holds one link per task, so the drop is declared, not silent (LLR-1401.1) |
| 2026-10-07 | the in-frame chainmap footer key-hints stay untouched | the footer row is byte-golden in the C-2b frames (`test_TC_801`/`test_TC_802`); the `,` key is discoverable via the docked keybar + the `?` bullet — declared notice, the close's lesson |
| 2026-10-07 | the README `comma` row ships inside the increment | the shipped census test `test_keymap.py:404` enforces every bound key documented; the row is `doc`, outside the source budget — declared, accepted |
| 2026-10-07 | saving is NOT an undo step | it writes settings, not tasks (HLR-1401's declared semantics); no undo entry exists to assert against — docstring-pinned at `app.py:767-777` |

## Risks / watch-items

- a saved template named exactly `Simple chain`/`Bugfix` shadows the preset silently (the pick resolves by name, user first) — inherited from batch-07, declared
- the degenerate one-task save toasts `1 tasks` — the pinned literal the app arm asserts; changing it reddens the arm
- the fan-in drop is silent (the toast's count is the only signal) — declared in LLR-1401.1, pinned by the round-trip arm
- the `,` key is view-scoped: silent no-op off the chain map (the shipped `action_kanban_sort` style)

## Conventions honored

- synthetic boards only (every fixture in `tmp_path`; no operator board data)
- the seat census before the write: `grep 'Key(","' taskboard/keymap.py` → 0 before the key landed (the brief's discipline order, executed)
- English artifacts; reserved field names literal; no git mutations by the implementing session or this close-out

## Out-of-scope carries

- none — the batch's only carry (authoring v2) shipped; the backlog's Open-after-batch-08 section reads "nothing new"
- the batch-06 visual re-verdict item was CLOSED by the coordinator's fold (`762d18c`, operator "Se ve bien." 2026-10-08) — recorded in the backlog, not reopened

## Test ledger

| Suite / command | Last run | Result |
|---|---|---|
| `python -m pytest tests/test_template_save.py tests/test_template_save_app.py -q` (the shipping session) | 2026-10-07 | 11 passed, 0 failed (2.66s — `evidence/inc001-run.log:1065`) |
| `python -m pytest tests -q` (the shipping session's full runs) | 2026-10-07 | first attempt `2 failed, 2584 passed` (441.25s — the README census the increment then shipped + the G-011 flake); settled run `1 failed, 2585 passed` (437.37s — `evidence/inc001-run.log:1293`; the one failure the G-011 environmental flake); the orchestrator's C-25 owns the ONE final clean-tree run |
| `python -m pytest "tests/test_app.py::test_win_clipboard_roundtrip" -q` (isolated, the coordinator's G-011 verification) | 2026-10-07 | 1 failed in 4.19s — SETUP failed, the environment not the code (`evidence/inc001-run.log:1251-1266`) |
| `python -m pytest tests --collect-only -q` (the close-out) | 2026-10-07 | 2586 tests collected |
| the coordinator's battery M16-M17 (byte-level, restores sha256-verified) | 2026-10-07 | 2 mutants, all KILLED (`evidence/mutations.log`) |

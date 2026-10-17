# Handoff — batch 2026-10-16-batch-01 (present v2)

Written at the end of P3, when the implementing session reached its context budget. All
three increments are implemented, tested, reviewed and committed. The DDR, P4 and the P5
close are left. Do not redo the increments.

## Where it stands

- Branch `present-v2`, created from `origin/main` `64443be`. Local `main` was left
  untouched (see the PLAN Key decisions, RC-1). **Nothing has been pushed**, and the
  commission forbids a push.
- `state.json`: `current_station: P3`, `in-progress`. `stations_active` holds P0, ARQ, P1,
  P2, PDR, P3, DDR, P4, P5. The decisions are logged for P0, ARQ, P1, P2 (iterate + approve),
  PDR, and P3 increments 001/002/003.
- Commits on `present-v2` after the base:

  | Commit | What it is |
  |---|---|
  | `02825b8` | rollover / seed |
  | `786a07f` | ARQ/P1/P2/PDR record |
  | `ea002aa` | increment 001: ruler + chips |
  | `d30aa8e` | increment 002: hide flag |
  | `2292e63` | increment 003: `?` keys |

- Full suite at `2292e63`: **2625 passed, 2 failed**, in `evidence/suite-003.txt`. The 2 failures
  are `tests/test_team_views.py` standup ×2. They already fail at `base_ref`
  (`evidence/preexisting-base-failures.txt`), because the 2026-10-11 name scrub broke them, and
  they are carried in `BACKLOG.md`.
- The gate (`devflow-validate.py --brief`) shows **0 block**. Every NOTICE left is either
  historical or a placeholder in a seed that is still unfilled (04, 05, DDR).

## What is left (runbook rows 9a → 12)

1. Move into the DDR:
   `python <bundle>/scripts/devflow-init.py --root <root> --decision "standing authorization — P3 closed: increments 001-003 committed; DDR next" --station DDR --status in-progress`.
   Then rewrite the PLAN's `Last updated` cell.
2. **DDR** (`stations/p4-validation.md` §DDR). Spawn `architect` and `qa-reviewer`, each with
   its role file. Software-dev is the orchestrator. Fill `design/DDR-2026-10-16-batch-01.md`
   section B, re-reading **PC-1..PC-11** of the PDR record against the artifacts:
   - PC-1/6: `tests/test_present.py` `FRAMES` → this batch's `PRES-R-*`.
   - PC-2: AT-1001's frame arm.
   - PC-3: TC-1601 `over` arm, TC-1605 80×24, AT-1602 export arm, TC-1604 (a)–(k).
   - PC-4: `present_span_label` appears in proposal §4 and in the map §4.
   - PC-5: `gen_frames.py` came before the repoint (increment 001).
   - PC-7: TC-1603's `0` arm, plus mutant N2 KILLED.
   - PC-8: TC-1607's injected key, plus P2 KILLED.
   - PC-9: M4/M5 KILLED.
   - PC-10: TC-1604 (h).
   - PC-11: TC-1605's `#f-title` ≥ 20.

   Also check that every AT realizes in exactly one node:

   | AT | Node |
   |---|---|
   | AT-1601 | `tests/test_present_rulers.py::test_AT_1601_...` |
   | AT-1602 | `tests/test_present_hide.py::test_AT_1602_...` |
   | AT-1603 | `tests/test_help_keys.py::test_AT_1603_...`, parametrized ×2 sizes, one node id |

   The design changes made at P3 relative to the PDR, which the DDR must review:
   - LED .7: the cross-check's third delta, D3.
   - `#help-cols` height auto.
   - `scrollbar-size-vertical: 1`.
   - The band is composed at an estimated width.
   - The hint row is a `Text` (markup census).
   - The `_present_pool` helper.
3. **P4** (`stations/p4-validation.md`). The orchestrator runs the complete suite once more
   (C-25). `qa-reviewer` reconciles both layers. Fill `04-validation.md`, then record the P4
   decision without a move.
4. **P5** (`stations/p5-postmortem.md` §Core close):
   - Run `--fold-canon`, then `--station P5 --status closed`.
   - Fill `05-close.md`. Its §3 *Found before the batch* lists:
     - `.gitattributes` and the two line-ending phantoms `.dev-flow/2026-10-07-batch-0{8,9}/evidence/inc001-brief.md`;
     - the untracked `decisions-log.json` files of batches 05–08;
     - batch 06's evidence extras;
     - `rollover_batch{g..j}.py`.
   - Run `devflow-evidence.py --close`, then the final gate.
   - `V57` is expected (1 commit). `V25` does not apply, because origin exists.

## Owed to the operator, named rather than buried

- The visual verdict on the 80-column oracle frame (⏸ DEFER, `BACKLOG.md`).
- Two prototype-capture differences were kept as shipped, on purpose:
  - the header's ` — hybrid` suffix;
  - the in-frame keys row.
- The branch decision. `present-v2` is built on the scrubbed `origin/main`. Local `main` is on
  the pre-rewrite history and should probably be reset to `origin/main`. That step is
  destructive and needs the operator.
- Evidence lives in `.dev-flow/2026-10-16-batch-01/evidence/`:
  - `gen_frames.py`, `mutate.py` and `capture_app.py` regenerate everything;
  - the captures are in `captures/app-00{1,2,3}-*.svg`.

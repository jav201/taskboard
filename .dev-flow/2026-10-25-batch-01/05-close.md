# Batch close — taskboard — Batch 2026-10-25-batch-01

> **Artifact language.** Canonical English scaffold; the batch's language is `en`.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 164 notice · 2026-10-25 |
| Gated tree | `d8e83885cb53e4cab7b9c270492dbebd06d6d97d` · dirty — .dev-flow/BACKLOG.md (the close record itself excluded) |
| Requirements canon | `repo:REQUIREMENTS.md` — the 9 ids this batch's `01-requirements.md` declares (`HLR-2801..HLR-2804` + `LLR-2801.1/2801.2/2801.3`, `LLR-2802.1`, `LLR-2803.1`) are folded tokens in it (step 1: `canon: REQUIREMENTS.md -- 9 folded`) |

---

## 1 · What changed

The start-up modals — the one-time milestone offer (`MilestoneOffer`) and the
team identity picker (`TeamIdentityPicker`) — now open over the visible board,
dimmed by the same `#0007` translucent backdrop the working modals use, on every
start path (single-board, the home's `enter`, team mode) at 118x30 and 80x24.
The user reaches this at every app start that owes a start-up modal; D-12 is
cured. Mechanism: one background-only declaration in `taskboard/taskboard.tcss`
(`PDR-2026-10-25-batch-01#D2`); the diagnosis refuted the commission's
unpainted-board hypothesis (the board beneath already paints; the modal screens
were opaque). One source file; no timing, order, content, keys or answers
changed; the picker's top-left placement preserved (`#D1`).

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-2801` | v2 | `AT-2801` (both sizes) | pass |
| `HLR-2802` | v2 | `AT-2802` (both sizes) | pass |
| `HLR-2803` | v2 | `AT-2803` (both sizes + the geometry arm) | pass |
| `HLR-2804` (pin) | v1 | `AT-2804` + the P4 gate suite | pass |
| `LLR-2801.1` | v2 | the six killed AT arms + the emitted-form probe | pass |
| `LLR-2801.2` | v1 | the diff inspection (packet §2) + TC-616/617 re-runs | pass |
| `LLR-2801.3` | v2 | `TC-2801` + the offer suite | pass |
| `LLR-2802.1` | v1 | `AT-2802` + the home suites | pass |
| `LLR-2803.1` | v1 | `AT-2803` + the D-615 stack assertion | pass |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

**The four landings — record which ones actually happened:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the command | n/a | — |
| 2 | its artifact | n/a | — |
| 3 | the catalog entry | n/a | — |
| 4 | committed and pushed | n/a | — |

- **New controls:** `none — this batch minted no portable control. The one candidate lesson (a standalone python probe against an editable-installed package imports the MAIN checkout, not the worktree; only python -m pytest from the root — or an explicit PYTHONPATH — measures the worktree) is project-stack specific and is recorded in the contract's premise 6 and the P1 gate's import probe; it does not reach the flow's global command.`

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/taskboard.tcss` | ✅ committed on `fix/startup-backdrop`; **not pushed — the commission forbids a push**; the operator merges | commit `ce89030` |
| `tests/test_startup_backdrop.py` (new) | ✅ committed, same branch | commit `ce89030` |
| `tests/test_milestone_offer.py` (one node scoped) | ✅ committed, same branch | commit `ce89030` |
| `REQUIREMENTS.md` (the canon fold) | ✅ committed, same branch | this close's deliverable commit |
| `.dev-flow/` batch record | ✅ committed, same branch | the batch's commits |
| `05-close.md` (this record) | 📋 committed in the close commit that follows the gate (step 8's order) | this close's close commit |
| `.dev-flow/BACKLOG.md` (D-12 done + the carries) | 📋 committed in the close commit | this close's close commit |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (the worktree was clean at the commission commit; the rollover's temporary move-aside of `.dev-flow/` was part of the batch's own open, not a pre-batch modification)

### Conditional-gate discharge

- **Conditional-gate discharge:** `3 condition(s) · ✅ all discharged`

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PDR 1 / DDR C-1 — the picker-placement backlog item filed | ✅ | `.dev-flow/BACKLOG.md` §Open after 2026-10-25-batch-01, item 2 («the picker's placement is blessed, not decided») |
| PDR 2 — the increment packet states the corrected touch set | ✅ | `03-increments/increment-001.md` §2 (discharged at P3, re-read at the DDR) |
| PDR 3 / DDR C-3 — the dimness hardening note filed | ✅ | `.dev-flow/BACKLOG.md` §Open after 2026-10-25-batch-01, item 3 |
| PDR 4/5 + DDR C-2 | ✅ | folded at intake (proposal §5/§6) and at P4 (the captures' scripted content check) — re-read at the DDR |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| D-12, the blank screen behind the start-up modals | Open → **Done** (done line written in place in the 2026-10-20-batch-03 section + this batch's section) | `2026-10-25-batch-01` increment 001 |
| the picker's placement: center it or codify top-left | **Carried** — new item | PDR `2026-10-25-batch-01#D1` |
| the AT oracle asserts visibility, not dimness | **Carried** — new item | qa DDR note D1 |
| the ~16 unlisted `ModalScreen` subclasses render opaque | **Carried** — new item | contract §6.3 census |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-25-batch-01
mode: core
verdict: pass
increments: 1
source_files_max: 1
notices_raised: 4            # V25, V30, V57, V62 — declared in PLAN.md §Gate notices
rework_returns: 1            # P2 round 1 returned iterate-to-refine (A1 blocker, A2 major)
triggers_fired: "A2,B1,D1"
tests_base_to_post: "3248 -> 3258"   # +9 new nodes; the environmental clipboard skip ran and passed (+1), named in 04-validation
new_control: none
open_items_next: 3           # the three carries of §4
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + ledger | gate `V26` green at every gate · scan 0 flags | ❌ | `none — the operator's standing authorization commissioned the flow's lenses; the contract was reviewed by two independent lens agents at P2 (twice)` | |
| Test cases / ATs | the mutation battery: 6 arms KILLED, per-arm verdicts, restore hash verified | ❌ | `none — code-reviewer and the DDR's qa lens audited the oracles; the flake arm ran 50×` | |
| Evidence bytes | `V41` — every cited digest re-hashes; the P4 qa lens re-derived all 9 packet digests | ❌ | `none` | |
| Code (the one-line declaration) | gates + `code-reviewer` PASS-WITH-NOTES, 0 HIGH | ❌ | `none — the diff is 7 lines beside a byte-identical shared rule` | |
| The six capture PNGs | scripted content checks (rows outside the box at capture time) + colour/byte floors | ❌ | `none — a human eyeball of all six PNGs agreed with the script (recorded in the captures README)` | |

- **Human perimeter:** the operator owns what this flow does not cover: the merge decision (NOT granted by the commission — nothing is pushed), the three backlog carries' disposition, and any evaluation with users (none exist outside the one-person team — the ux lens's declared answer).
- **Human review ledger:** `none — every review in this batch was an independent sub-agent lens carrying the flow's role files (9 reviewer agents in all: 2 at P2 × 2 rounds, 3 at the PDR, 1 code-review, 2 at the DDR, 1 at P4); no human read the artifacts at a gate. The operator's reconstruction path is the decisions_log + this record.`

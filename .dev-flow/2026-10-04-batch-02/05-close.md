# Batch close — taskboard — Batch 2026-10-04-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/docs/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER`
> **And the §6 DEPTH tokens — cell VALUES rather than field names, reserved for the same reason:**
> `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`. A CLOSED set, declared closed by the first
> revision that ships it — so the vocabulary a later promotion of `V54` to BLOCK will need already exists,
> instead of being introduced over a free-text field that six authors have by then written six ways.
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied
> **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `cd ~/.claude/skills/dev-flow && python scripts/devflow-validate.py <repo>` with the installed rev100 bundle (skills HEAD `1d3c364`; no pin snapshot was needed, V7 never failed). Exit 0, **0 block · 37 notice · 61 not applicable** (`evidence/validator-close.txt`), 2026-10-05 |
| Gated tree | `4b2c13ae6ab2ad66ceaa6b54e2f9abbc8900f7d2` · dirty: every change is still in the working tree, waiting for the coordinator's commit (standing authorization: the coordinator commits and pushes after the operator's visual verdict; this agent does not commit). Files: `taskboard/models.py`, `taskboard/app.py`, `taskboard/modals.py`, `taskboard/views.py`, `taskboard/keymap.py`, `README.md`, `REQUIREMENTS.md`, `.gitattributes`, `tests/kg_board.py`, `tests/test_app.py`, `tests/test_colour_budget_app.py`, `tests/test_edit_window.py`, NEW `tests/conftest.py`, `tests/test_milestones.py`, `tests/test_gantt_milestones.py`, `tests/test_kanban_milestones.py`, `tests/test_milestone_offer.py`, `tests/test_milestone_offer_seam.py`; `.dev-flow/state.json`, `.dev-flow/BACKLOG.md`, NEW `.dev-flow/2026-10-04-batch-01/decisions-log.json`, NEW `.dev-flow/2026-10-04-batch-02/` |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with `devflow-init.py --fold-canon`: 16 folded, 0 kept, 0 refused (`evidence/p5-fold-canon.txt`). Every HLR/LLR heading of `01-requirements.md` is a row there. LLR-001.3 is amended from 17 to 18 widget ids (`#f-milestone`, LLR-601.3) |

---

## 1 · What changed

**A task can now be a milestone — one date, no duration — and the board treats it as a commitment, not as work.**
- **Marking.** `M` (gantt, kanban, lanes, agenda, focus) or the editor's new `milestone` box marks a task. Its start follows its due, and a task with no date is refused with a reason. `u` undoes it, and team sync carries the flag (read only as a real `true`).
- **Gantt.** A milestone is a ` ◆ title` row with `◆ Mon D` on its date and a chip (`in Nd`, `today`, `▲Nd`, `✓ done`), never a bar. Reached milestones stay as quiet `◆✓` rows in ash while their project has open work. The month ruler marks the selected project's milestones, and the legend, map and help name both marks.
- **Kanban.** Milestones leave the columns, the counts and the selection, and ride their project's band rule: late first, then upcoming, then the last reached, with dates only and `+N ◆` when the width runs out.
- **The one-time offer.** On the first start of this version, a board holding one-day or due-only tasks is offered to convert them. One-day tasks are pre-ticked and due-only tasks are not; nothing the user did not tick is converted. Converting first takes a backup (`‹board›.pre-milestones`) and a log (`‹board›.milestones-log`), then saves atomically, marks the board so it is never asked again, and can be undone with `u` in one step. `esc` means "not now" and is also never asked again. A failure changes nothing, says so, and offers again next start. New boards are created already marked.

Moving linked dates (US-604) is not in this batch. It is B2b in BACKLOG (D-601).

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-601 / LLR-601.1–601.3 | v1 | AT-601 · TC-601..608 | pass |
| HLR-602 / LLR-602.1–602.3 | v1 | AT-602 · TC-609..611 | pass |
| HLR-603 / LLR-603.1–603.2 | v1 (LED .7, .8) | AT-603 · TC-612, TC-613 | pass |
| HLR-605 / LLR-605.1–605.4 | v1 (LED .9, .10) | AT-604..606 · TC-614..617 | pass |
| LLR-001.3 (canon) | amended | `tests/test_edit_window.py` | pass |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — | — | — |

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a | none minted |
| 2 | its **artifact** (a template section) | n/a | none minted |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a | none minted |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a | none minted |

- **New controls:** none — this agent never edits `~/.claude`, so minting is the flow owner's call. Two candidate lessons are recorded:
  - (a) A census threshold must name its measure. P1's 274 counted unmarked boards before seeding existed, so P4's first count of 140 looked like a fail until both counts were taken on the same definition (`04-validation.md` §census reconciliation).
  - (b) An AT arm that "finds any mark of colour X" passes on a pre-existing mark of the same colour. The P4 V2 mutant survived exactly that way.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in §0 *Gated tree* | 📋 ready to commit — the coordinator commits and pushes after the operator's visual verdict (standing authorization "Commit + push tras tu veredicto visual", `merge: false`); this agent does not | `git status --short` |
| `y.json` (repo root, untracked) | 🗑️ a stray synthetic board one of this batch's probes wrote; moved to the session scratchpad (not deleted), never committed | decisions log 2026-10-05 |
| `~/.claude` | not touched by this batch (flow read from the installed rev100 bundle) | — |
| scratch exports, batteries, probes | outside the repo (session scratchpad), not part of the record | — |
| inherited home-path strings (`.dev-flow/state.json` `owner`; one BACKLOG line naming an email) | 📋 present at HEAD before this batch; not this batch's to change — noted for the coordinator | `git show HEAD:.dev-flow/state.json` |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

### Conditional-gate discharge

- **Conditional-gate discharge:** 9 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| P2 iteration 1 iterate-to-refine (Q-1, A-1 blockers) | ✅ | `02-review.md` iteration 3 — approved |
| increment 001 code review F2-1 (HIGH, product, increment under construction — second exception) | ✅ | `03-increments/increment-001.md` §4b; `evidence/inc001-f2-1-red.txt` → `-green.txt` |
| increment 002 G2-1 (reporting error) | ✅ | `03-increments/increment-002.md` |
| increment 003 K-1 (MED, product) | ✅ | `03-increments/increment-003.md` §4b; `evidence/inc003-k-red.txt` |
| increment 004 O-1 (MED, product) and S4-1 (LOW) | ✅ | `03-increments/increment-004.md` §4b; `evidence/inc004-r2-red.txt` → `-green.txt` |
| P4 qa F-1, F-2 (MED, tests) | ✅ | `04-validation.md` §Orchestrator fold; `evidence/p4-mutations-before.txt` → `-after.txt` |
| P4 ux UXV-1 (MED, evidence) | ✅ | `evidence/captures/close-editor-*`, `close-details-*` |
| P4 qa Q-9 (the seam census `not-run`) | ✅ | `04-validation.md` §census reconciliation; `evidence/p4-offer-census.json` |
| security close S5-1 (home path in evidence) | ✅ | `grep -rl <username> .dev-flow/2026-10-04-batch-02/` → none |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| Batch B2 (B1's entry) | B2a ✓ done here; B2b carried | `.dev-flow/BACKLOG.md` §after batch-01 |
| B2b — moving linked dates (US-604, A-14) | added | §after `2026-10-04-batch-02` |
| S-4 pattern in `run_link_migration`; S-9 non-string title crash; S5-3 partial backup | added | same |
| K2-1 legend scope; UX2-2 fold-row marker; D-623 rule-only band; milestones in other views | added | same |
| UXV-3 silent `u`; UXV-6 help cut at 80; qa F-3..F-5 test strength; F-6 `_md` copies | added | same |
| G-011 clipboard flake | carried | same |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-04-batch-02
mode: core
verdict: pass
increments: 4
source_files_max: 4
notices_raised: 37               # the closing validator's notice count (31 inherited at kickoff)
rework_returns: 10               # P1 ×2, P2 ×2, 001 r2+r3, 002 r2, 003 r2, 004 r2, the P4 fold
triggers_fired: "B1,B4,C5,C6,C8,D1,D2,E1,F2"
tests_base_to_post: "2306 -> 2486"
new_control: none
open_items_next: 13
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| The commission and its standing authorization | — | ✅ the operator's own words, relayed by the coordinator | `spot-check` | — |
| The B2a/B2b split (D-601) | `01-requirements.md` | ✅ pre-authorized by the operator in the commission | `spot-check` | — |
| PV-601..PV-611 and the P4 ux notes on the captures | `04-validation.md` UX walkthrough | ✅ verdict 2026-10-06 (`taskboard-veredicto-b2a.json`): PV-601..611 all accepted; UXV-5 → reached grey `#7a828c` applied (LED .11) | `visual verdict on the captures` | the code |
| Code, tests, evidence | gates + code/qa/ux/security reviewer verdicts | ❌ | `none — machine review only` | all of it |

- **Human perimeter:** the operator owns the following, and this flow does not cover them:
  - the look of the close captures: PV-601..PV-611, plus UXV-2, UXV-4, UXV-5, UXV-7 and UX-12 — **verdict delivered 2026-10-06**: all PV accepted, UXV-5's lightening applied (LED .11);
  - the first start of the new version on the real board. The offer appears once; converting takes a backup `‹board›.pre-milestones` and a log, and `u` undoes it. This agent never opened that board;
  - the commit and push, done by the coordinator.
- **Human review ledger:** human:Javier — 3 artifact(s) reviewed (the commission and the split, by authorization; the visual verdict 2026-10-06), 0 rigorous · 1 declared not-reviewed (the code)

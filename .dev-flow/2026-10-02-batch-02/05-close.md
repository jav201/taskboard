# Batch close — taskboard — Batch 2026-10-02-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/docs/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `⏸ DEFER`
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
| Gate record | `cd <scratchpad>/devflow-rev98-48154ab/dev-flow && python scripts/devflow-validate.py <project>` (the PINNED rev98 bundle, skills `48154ab`, operator ruling "Fijar el batch a rev98") · exit 0 · **0 block** · 18 notice · 62 n/a · 2026-10-02 · `evidence/validator-close.txt`. Notices: the 17 inherited ones declared in `PLAN.md` (V9 ×8, V13, V22 ×2, V23, V26, V30, V53, V57); this batch's own: V9 on increment 002 (4 SOURCE files — at the cap, the reason declared in its §2; V9 notices every packet at 4 by design), V13 (its IFC address is computed), V22 (LLR-201.3 constrains and transforms no node), V57 the dirty tree — declared in the next row |
| Gated tree | `a0e7d9a7c76d51859a53400dc195d74182342873` · dirty — every change is in the working tree for the coordinator's commit (standing authorization: this agent does not commit): `taskboard/views.py`, `taskboard/app.py`, `taskboard/modals.py`, `taskboard/keymap.py`, `taskboard/ribbon.py`, `taskboard/team_sync.py`, `taskboard/taskboard.tcss`, `tests/kg_board.py`, `tests/test_colour_budget_app.py`, `tests/test_english.py`, `tests/test_gantt_polish.py`, `tests/test_cells.py`, `tests/test_colour_budget.py`, `tests/test_flow_view.py`, `tests/test_gantt_board.py`, `tests/test_keymap.py`, `tests/test_setup_help.py`, `tests/test_team_views.py`, `.gitattributes`, `REQUIREMENTS.md`, `.dev-flow/state.json`, `.dev-flow/BACKLOG.md`, `.dev-flow/2026-10-02-batch-01/decisions-log.json`, `.dev-flow/2026-10-02-batch-02/**` |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with the pinned `devflow-init.py --fold-canon`: 23 folded (10 HLR + 13 LLR), 0 refused; a second run: 0 folded, 23 kept |

---

## 1 · What changed

The operator's twelve answers are in the app. **Teal now means only what is being operated on,
plus today**, on every view, the key bar, the ribbon and the dialogs: titles and keys are bold
bright, Setup paints its rows with their styles again (they had been plain), soon-due tokens are
amber, and the moving gantt packet is quiet. **The app speaks English** — the help, the flow view,
Setup and the team filter — with stored values unchanged. **The gantt says what it is not
showing**: a dim `▲ N above / ▼ M below` row under a paged project, and a short notice when `]`
finishes a task. **It folds more predictably**: the project just left stays open while it fits, and
urgent projects — work due today counts — are offered rows first, so Ops & Security opens at 80×24.
**Weekends are shaded** at a day per cell in a background that survives 256 colours, and the
ruler's echo shows `◂`/`▸` where a task runs past the window. Along the way the key bar's `;` toggle
works again (it never reached the `more` layer, D-218).

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-201 | v3 | AT-201 · TC-201, TC-202, TC-213 (`04-validation.md` Layer A) | pass |
| HLR-202 | v2 | AT-202 · TC-203, TC-204 | pass |
| HLR-203 | v4 | AT-203 · TC-205 | pass |
| HLR-204 | v3 | AT-204 · TC-206 | pass |
| HLR-205 | v2 | AT-205 · TC-207 | pass |
| HLR-206 | v2 | AT-206 · TC-208 | pass |
| HLR-207 | v4 | AT-207 (one node, two arms) · TC-209, TC-210 | pass |
| HLR-208 | v4 | AT-208 · TC-209 | pass |
| HLR-209 | v2 | AT-209 · TC-211 | pass |
| HLR-210 | v2 | AT-210 · TC-212 | pass |

Version = 1 + the item's entries in `01-requirements-ledger.md` (LED .1–.19). The 13 LLRs pass with
their parents (`04-validation.md` iteration 2: 23/23, 0 blocker); HLR-203 was amended at P4 (LED .19).

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| none | — | — |

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a — no control minted | — |
| 2 | its **artifact** (a template section) | n/a — no control minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a — no control minted | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a — no control minted | — |

- **New controls:** none — every failure this batch was caught by an existing control: C-31 (the hand-picked lexicon, increment 003), C-18 (AT-207 on two nodes, P4), C-40 (mutants proving each test can fail, and catching a false kill claim), C-39 (a guessed frozen key-bar string, replaced by one read off the base tree), the code-review freeze rule (a fold that deleted a node), the app's own laws (second person, declared hue, span economy) and V7 (the flow bundle moved mid-batch). Two process lessons are recorded for the flow owner rather than minted: a Git Bash heredoc collapses `\\` in Python source (write scripts with a file tool), and `Path.write_text` turns LF into CRLF on Windows (the byte-exact `evidence/mutate_bytes.py`).

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in §0 *Gated tree* | 📋 ready to commit — the coordinator commits and pushes to `main` without a PR (standing authorization, `merge: false`); this agent does not | `git status --short` |
| `~/.claude/skills/dev-flow/**` (rev99-wip) | 📋 not this batch's — the flow owner's work in progress; never edited here (operator ruling) | `PLAN.md` header "Flow pin" |
| scratch copies, mutation trees, the pinned rev98 snapshot | 🗑️ outside the repo (session scratchpad); harness sources kept in `evidence/mutate.py`, `evidence/mutate_bytes.py` | `evidence/inc00*-mutations.txt` |

### Conditional-gate discharge

- **Conditional-gate discharge:** 6 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| code-reviewer BLOCK-UNTIL R2-F1 (increment 001) | ✅ | `03-increments/increment-001.md` §4b round 3 OK; M9b KILLED in `evidence/inc001-mutations.txt` |
| code-reviewer BLOCK-UNTIL F1 (increment 002) | ✅ | `03-increments/increment-002.md` §4b round 2 OK; MG KILLED by AT-202 |
| code-reviewer BLOCK-UNTIL F1 (increment 003) | ✅ | `03-increments/increment-003.md` §4b round 2 OK; X1–X3 KILLED |
| V7 BLOCK (the flow bundle became rev99-wip) | ✅ | `PLAN.md` header "Flow pin" — operator ruling, pinned rev98 bundle V7 clean |
| qa-reviewer P2 / ux-reviewer P2 FAIL (iteration 1) | ✅ | `02-review.md` §Iteration 2: both PASS-WITH-NOTES |
| qa-reviewer P4 FAIL (G-001..G-003) | ✅ | `04-validation.md` iteration 2 `**Result:** PASS-WITH-NOTES`, G-001..G-004 closed; G-009/G-010 discharged (BACKLOG entry; increment-006 §4b) |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| colour budget app-wide (UXV-9 included), D4, D10, D12, D13, HELP, SOON, PKT | shipped (uncommitted) | increments 001–003; BACKLOG items marked ✓ done |
| D9 page hint, D14 toast, D5 weekend shading, UXV-2, UXV-3, UXV-7 | shipped (uncommitted) | increments 004–005 |
| the operator's verdicts on D-203/204/205/208/211/213/214/217; UXV2-1 (`date_chip`), UXV2-2 (key-bar groups), UXV2-8 (`today` tones); stale previous group; other-side clip; security L1 and S-5; cleanups (group_of, HEAT, F6, param ids, lattice bullet); Setup wrap at 80×24 | added | `.dev-flow/BACKLOG.md` §Open — after `2026-10-02-batch-02` |
| Batch A2 and everything else in BACKLOG | carried | `.dev-flow/BACKLOG.md` |
| header refresh | done — 1677 tests, base `a0e7d9a`; the base ref moves when the coordinator commits | `.dev-flow/BACKLOG.md` header |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-02-batch-02
mode: core
verdict: pass
increments: 6
source_files_max: 4
notices_raised: 18
rework_returns: 2
triggers_fired: "B1,B4,C,D,E,F2"
tests_base_to_post: "1611 -> 1677"
new_control: none
open_items_next: 11
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` | P2 qa / ux PASS-WITH-NOTES iteration 2; security PASS-WITH-NOTES (`02-review.md`) | ❌ | `none` | the operator has not reviewed yet; this batch ends at his commit gate |
| Code (7 source files) | code-reviewer OK per increment (6 increments, 13 rounds) · mutants 21, 16, 14, 15, 16, 1 KILLED | ❌ | `none` | as above |
| Tests / ATs | `04-validation.md` iteration 2: 23/23, C-18 ✓, ledger 1677 | ❌ | `none` | as above |
| Captures (`evidence/captures/close-*` beside `base-*`) | ux-reviewer P4 walkthrough PASS-WITH-NOTES (13 items) | ❌ | `none` | as above |

- **Human perimeter:** the operator (Javier) owns: the visual verdict on the close captures at 118×30 and 80×24 against the base ones; the provisional decisions D-203, D-204, D-205, D-208, D-211, D-213, D-214, D-217 and the UXV2 questions in BACKLOG (all twelve answers were the recommended option, D-216); whether `date_chip` and `today` follow the amber; the commit itself.
- **Human review ledger:** none — no human has reviewed this batch yet; it ran autonomously under "Autónomo, agente Opus" and ends at the coordinator's commit.

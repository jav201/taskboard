# Batch close — taskboard — Batch 2026-10-07-batch-09 (templates v3: scratch authoring)

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` — seed baseline (before any close-out fill, over the unchanged seed files): **0 block · 52 notice · exit 0** · 2026-10-08 · mid-loop (packet + validation + review filled; the close still its seed): **0 block · 41 notice · exit 0** · 2026-10-08 · **final loop over the complete record: 2 block · 38 notice · exit 1** · 2026-10-08. The seed carried no block: the 52 notices were the unfilled-seed placeholders (V31-V44/V47-V51/V54 — cleared by this record pass) over the historical and runtime/standing lines. **The 2 remaining blocks are ONE class, OUTSIDE the close-out's writable set: 2 × V22 — the canon fold-back** (`HLR-1501` · `LLR-1501.1` are declared as headings in the active batch's `01-requirements.md` but are not yet tokens in the living canon `REQUIREMENTS.md`; the rule fires only once the close exists): discharge = `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` at the coordinator's commit step, then re-run — the same class batch-2026-10-07-batch-08 recorded and discharged at its commit; this close-out does not edit `REQUIREMENTS.md`, per the commission. **No `V2` finding fires** — the AT-1501 dash token the rule reads sits in `tests/test_template_new.py`'s docstring (line 4, verified: `HLR-1501 / LLR-1501.1 · AT-1501.`). The 38 notices: the historical/standing set (V9/V13/V22/V23/V27/V30/V42/V53 over older sealed batches and the runtime floor) **plus V57's dirty-tree notice** — expected, the `Gated tree` row below declares the dirty set by design, uncommitted until the coordinator's commit. No `V56` fired: the packet names the failing transcript proactively (`5 failed, 2587 passed` at `evidence/inc001-run.log:483`, the five picker-shape arms tabled in increment-001 §4), so the rule's under-report branch had nothing to report | **Final run after the fold-canon discharge: the coordinator's step at the commit — the same standing discharge batch-08 recorded; the pre-fold final state is 2 block (V22 ×2) · 38 notice · exit 1, both blocks the fold-back class** |
| Gated tree | `5c4c28ad075ded9152251604d490dc244f293169` · dirty — `taskboard/{modals,app,views}.py` (the batch's edits) · `tests/test_template_new.py` (new) · `tests/test_templates_app.py` · `tests/test_template_save_app.py` (the coordinator's law-driven fixture updates) · `.dev-flow/2026-10-07-batch-09/` (the batch record, incl. `evidence/`) · `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` (the batch-09 evidence `-text` line — verified present at `.gitattributes:17`) · `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json` · `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}` · `.dev-flow/rollover_batch{g,h,i,j}.py` — uncommitted **by design**: the coordinator commits and pushes once per batch under the operator's commission, after the verdict |
| Requirements canon | `repo:REQUIREMENTS.md` — the living-canon fold-back for this batch's ids (US-1501 · HLR-1501 · LLR-1501.1) is the coordinator's `--fold-canon` step at the commit when the rule fires it (this close-out does not edit `REQUIREMENTS.md`, per the commission) |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (RC-1: local
  `5c4c28a` == `origin/main` at the open, `state.json` `base_ref`; re-verified at this close by
  `git rev-parse HEAD origin/main` — both still at `5c4c28a`). The untracked `decisions-log.json`
  files (batch-05/06/07/08), `rollover_batch{g,h,i}.py`, and the batch-06 verdict-sheet evidence
  predate the batch — the coordinator's carried bookkeeping, listed in the dirty set; the
  batch-09 rollover's own files (the batch dir, `rollover_batchj.py`, the `.gitattributes` line,
  the rolled `state.json`) are the batch's.

---

## 1 · What changed

*(BLUF. What the user can now do that they could not before, and through which surface. Then the mechanism.)*

**`I` → `New template...` → type a name, type the tasks one per line → saved.** The `I` picker now
opens with a leading `New template...` row; choosing it opens a small editor — ONE name field, ONE
multi-line tasks field. `Save` appends the template to the board's `settings["templates"]` as a
linear chain (task i waits on i−1; blank lines skipped, lines trimmed), saves the board, and
toasts the batch-08 literal `Template '<name>' saved — <N> tasks`. The template lists in the picker
from then on (right after the authoring row) and inserts with `I` like any other, reproducing the
chain. An all-empty edit saves nothing and says why in one line; `esc` cancels with nothing
written — the board file's bytes are untouched. Authoring is NOT an undo step (declared,
docstring-pinned): it writes settings, not tasks. Notes stay JSON-only at this version — the `?`
bullet says so. The editor is the lightest house-consistent composition — the `ProjectModal`/
`TextPrompt` modal-box shell with an `Input` and the app's shipped `TextArea`, one `DEFAULT_CSS`
rule, no `.tcss` touched.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1501 (author a template from scratch in the app) | v1 | AT-1501's 6 arms · M18 | pass |
| LLR-1501.1 (the editor modal and the linear-chain shape) | v1 | the 6 arms through the app pilot · M18 | pass |

**How the work was done.** ONE implementing session (DeepSeek V4 Pro under the coordinator's brief —
`evidence/inc001-brief.md`) executed the batch's single increment in the MAIN checkout: the picker
row (`modals.py:933-985`, the reserved id `__new__` at `:967`), the editor (`modals.py:987-1031`),
the route + the save (`app.py:741-746` · `:814-843`, the `wait` chain at `:835`), the `?` bullet
(`views.py:6837-6838`), and the test file — reporting its targeted 6-passed run and its one
full-suite run at `5 failed, 2587 passed` (`evidence/inc001-run.log`). The 5 failures were ALL
pre-existing arms pinning the old picker shape: the session STOPPED and named them instead of
touching them (the brief's "Nothing else" cap), and the coordinator then made the five law-driven
fixture updates (named in `evidence/mutations.log`), after which the 15 template arms across the
three files stand green. The coordinator then ran the close-out mutation battery M18 (byte-level,
restore sha256-verified), reviewed the increment (`02-review.md` approve), and filled this record.
No implementing agent committed, pushed, or stashed anything; this close-out ran no test suite —
only `pytest tests --collect-only -q` for the ledger (2592) and read-only greps.

**The G-011 declaration** (exactly as the backlog states it): `test_win_clipboard_roundtrip`
remains an intermittent environmental flake (G-011): it fails on its own clipboard SETUP in B2 gate
runs (the test's own message: `SETUP failed — this is the environment, not the code under test`,
the PowerShell `Set-Clipboard` ExternalException). The BACKLOG has carried it since batch B2; the
increment touched no clipboard seat. It did NOT fire in this batch's recorded full-suite run (the 5
failures were the picker-shape arms); it is declared, expected in any full run.

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — (candidate, not minted) — the stop-and-name rule: when a full-suite run reddens pre-existing tests OUTSIDE the brief's file set, the implementing session stops and names them and touches nothing; the correction population is then enumerated and executed law-driven (assertions not weakened) | a session "fixing" shared pinned tests to make its run green — silently re-basing the contract's ripple into weakened assertions; this batch's 5 reds were the contract's own FIRST-row law, named, then updated law-driven (`evidence/mutations.log`) | THREE consecutive batches deep: batch-07 (the README census row outside the brief), batch-08 (the census failure + the `,` grammar trap), batch-09 (the FIRST-row law's 5-test ripple) |
| — (candidate, not minted) — the correction-population-in-the-brief rule: a contract that reshapes a SHARED pinned surface (a picker listing, a help table) carries its expected correction population in the brief, so the session ships the fixture updates in the same pass instead of STOPping at the gate | a batch gate surprised by its own contract: the FIRST-row law's cost (5 fixture updates) was discoverable at contract time — the pre-batch tests that pin the picker's shape are enumerable by grep | this batch's executed evidence (the session's run reddened exactly the enumerable set; `02-review.md` observation (a)) |

**The four landings — record which ones actually happened:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | not landed — nothing minted this batch | — |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | not landed — nothing minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | not landed — the lessons are recorded below; the catalog lives in the flow bundle, outside this close-out's writable tree | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | not landed — nothing minted | — |

- **New controls:** `none — this batch minted no control: the stop-and-name rule (now three batches
  deep) and the correction-population-in-the-brief rule are recorded as candidates above with their
  measured origins; minting them into the flow's catalog is the operator's ruling at the next
  aperture`

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/{modals,app,views}.py` · `tests/test_template_new.py` · `tests/test_templates_app.py` · `tests/test_template_save_app.py` | 📋 left on purpose — the batch's edits + the new test file + the coordinator's law-driven fixture updates, uncommitted by design; the coordinator commits + pushes under the commission after the operator's verdict | the gate's dirty list above; the diffs read in the increment packet |
| `.dev-flow/2026-10-07-batch-09/` | 📋 left on purpose — the batch record (this close) | the artifacts themselves |
| `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-0{5,6,7,8}/decisions-log.json` · `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}` · `.dev-flow/rollover_batch{g,h,i,j}.py` | 📋 left on purpose — the batch's bookkeeping (the header refresh + the done entry, the rolled state, the evidence `-text` line verified, the carried decisions logs + verdict-sheet evidence + rollover helpers) | `git status --short` |

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally` (no V-block was discharged
  to pass; the canon fold-back the final gate fired for `HLR-1501` · `LLR-1501.1` — 2 × V22 — is
  the coordinator's standing discharge, `--fold-canon` at the commit, as batch-08's, and the
  AT-1501 dash token already sits in the test file's docstring — `tests/test_template_new.py:4`)

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| — | — | — |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| US-1501 — author a template from scratch in the app (the operator's follow-up 2026-10-08: "No puedo hacer una plantilla desde cero tambien?") | ✅ done in `2026-10-07-batch-09` (the picker row + the editor + the route/save + the `?` bullet; AT-1501's 6 arms; M18 KILLED; the five law-driven fixture updates as the contract-ripple record) | BACKLOG · `03-increments/increment-001.md` |
| the five pre-existing picker-shape reds (the session's STOP-and-name) | ✅ **CLOSED** — the coordinator's law-driven fixture updates (assertions not weakened), named in `evidence/mutations.log` | `evidence/mutations.log` · increment-001 §4 Correction population |
| carries | NOTHING new open — the "Open — after `2026-10-07-batch-09`" section reads "Nothing new from this batch"; the G-011 environmental flake line stands as the only standing item | the "Open — after `2026-10-07-batch-09`" section in `.dev-flow/BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-07-batch-09
mode: core
verdict: pass
increments: 1
source_files_max: 2          # highest source-file count in any one increment
notices_raised: 2            # ⚠ declared across the batch (views.py-as-doc — the THIRD consecutive, now named for rule-or-retire · no-4-source-file pressure)
rework_returns: 0            # items that came back, per QA's phase checklists (the 5-test ripple was the contract's own cost, closed law-driven in the same batch — not a rework return)
triggers_fired: "none"
tests_base_to_post: "2586 -> 2592"
new_control: none
open_items_next: 0
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + the ledger | LED-2026-10-07-batch-09.1 ↔ requirements pairings both ways (no V26 finding at the gate) · the P2 gate `approve` | ❌ | `none` | — |
| `02-review.md` (the lenses) | 0 blocker · 0 major · 0 minor — one declared observation | ❌ | `none` | — |
| `03-increments/increment-001.md` | the 16-row gate signed · M18 executed per the transcript · digests verified | ❌ | `none` | — |
| `04-validation.md` | `Result: PASS` · the ledger reconciles 2586 − 0 + 6 = 2592 (measured) | ❌ | `none` | — |
| `05-close.md` | the `Gated tree` row binds `5c4c28a` · C-44/C-45 answered | ❌ | `none` | — |
| The code | the targeted run 6 passed · the one full run's 5 reds all named and closed law-driven · M18 KILLED | ❌ | `none — not audited line by line beyond the packet's diff reads` | the untouched regions of the product files outside the diff hunks |
| The commission (the operator's request) | recorded in `PLAN.md` + `state.json` | ✅ | — | the operator's own words |

- **Human perimeter:** `the operator's 2026-10-07/08 words are the commissioning input — "No puedo
  hacer una plantilla desde cero tambien?" — read with the established chain: the gates run
  autonomously under the two exceptions; the COORDINATOR commits and pushes at each close (no PR);
  synthetic boards only; DeepSeek implements under coordinator briefs. The batch runs in the MAIN
  checkout. The operator owns the commit/push, the first-eye verdict on the new editor surface,
  personnel, and business judgement — the flow covers the record, the gates, and the suite.`
- **Human review ledger:** `human:coordinator — every artifact self-executed under the named lenses;
  no other human audited these artifacts. The ✅ row is the operator's commissioning words,
  accepted as the batch's authorization, not a review of the record.`

## Lessons carried

- **Stop-and-name caught a spec-adjacent defect for the third consecutive batch.** Batch-07: the
  session named the README-census row the brief never listed. Batch-08: the census failure and the
  `,` grammar trap, named before any test ran. Batch-09: the contract's OWN "`New template...`
  FIRST" law rippled into exactly 5 pre-existing pinned tests — the session STOPPED, named all five
  (`evidence/inc001-run.log:529-537`), and touched nothing outside its brief. The discipline is
  invariant and it keeps paying: a red suite outside your files is a fact to name, not a fixture to
  "fix". The candidate control is three batches deep — the operator rules at the next aperture.
- **A shared-surface contract change IS a correction, with a population.** The FIRST-row law's cost
  was enumerable at contract time (grep the tests pinning the picker's shape); the coordinator
  enumerated it from the run's failure list BEFORE the first edit, updated all 5 sites law-driven
  (same outcomes, new shape — never weakened), and recorded it as the batch's correction entry. The
  candidate rule: the brief carries the contract's expected correction population.
- **Reserved ids over index arithmetic for non-option rows.** The authoring row carries the
  reserved id `__new__` — the house pattern the `L` link picker's "+ create a new task" row already
  ships (`modals.py:872`/`:922`) — so the selection handler recognises it without indexing into
  `_templates`, and template rows keep their stable index ids. The lightest composition won again:
  the editor is the shipped modal-box shell + `Input` + the app's own `TextArea`, one
  `DEFAULT_CSS` rule, zero `.tcss`.
- **Measure and write the truth — the ledger pre-computed 2586, the collect measured 2592.** The
  brief's arithmetic assumed a 2586 base and read the fixture updates as node-neutral; the measured
  truth at this close is 2592 (= 2586 − 0 + 6), cross-checked by the session's own run (2587
  passed + 5 failed = 2592 collected). The record states the measured number and shows the
  arithmetic.
- **A help-only `.py` change is `doc` — third consecutive.** Batch-07, batch-08, and batch-09 all
  read a `?`-bullet-only `views.py` change as `doc`, outside the source budget. The recurrence is
  named: it becomes the standing rule or the operator retires it at the next aperture.

## Standing constraints honored

- No commits/pushes/stashes by the implementing session or this close-out; the coordinator commits
  and pushes once per batch under the operator's commission, after the verdict. No git mutations of
  any kind were run (read-only `git rev-parse`/`git status`/`git show`/`git diff` only).
- Targeted pytest only by the implementer; this close-out ran NO test suite — only
  `pytest tests --collect-only -q` to re-collect 2592 for the ledger, plus read-only greps; the
  orchestrator owns the ONE complete clean-tree run (C-25).
- `.dev-flow/**` was the only writable surface; `taskboard/` and `tests/` were never edited by this
  close-out (the five law-driven fixture updates and the mutation battery were the coordinator's
  runs, before this close-out, with hash-verified restores).
- `REQUIREMENTS.md` (the living canon) was not edited — the fold-canon is the coordinator's
  mechanical step at the commit.
- Synthetic boards only; English artifacts; the reserved field names kept literal.

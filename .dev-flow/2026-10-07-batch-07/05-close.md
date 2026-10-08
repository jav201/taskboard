# Close — taskboard — Batch 2026-10-07-batch-07 (the templates batch)

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` — seed baseline (before any close-out fill): **1 block · 51 notice · exit 1** · 2026-10-07; final loop at this close: **3 block · 38 notice · exit 1** · 2026-10-07. The seed's one block was `V26` — the ledger's LED-2026-10-07-batch-07.2 pairings existed only in the ledger because the live contract's `Ledger:` fields named .1 alone; cleared INSIDE the writable set (both `Ledger:` fields now read `.1 · .2`). The 3 blocks that remain are ONE class, OUTSIDE the close-out's writable set: **3 × V22 — the canon fold-back** (`HLR-1301` · `LLR-1301.1` · `LLR-1301.2` are not yet tokens in the living canon `REQUIREMENTS.md`): discharge = `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` at the coordinator's commit step, then re-run — the same class batch-2026-10-07-batch-06 recorded and discharged at its commit; the close-out does not edit `REQUIREMENTS.md`, per the commission. **No `V2` finding fires** — the AT-1301 dash token the rule reads sits in `tests/test_templates_app.py`'s docstring (line 3, verified). The 38 notices are historical-batch lines (`V9`/`V13`/`V22`/`V23`/`V42`/`V53` over older sealed batches — none against this batch's packet) plus the runtime/station-expected ones (`V30`'s bundle-floor half-derivation · `V27`'s decisions-log currency over the rolled `state.json` · `V56` retired by naming the 21-failure transcript in the packet · `V57`'s dirty-tree notice — the `Gated tree` row below declares the dirty set by design, uncommitted until the coordinator's commit) | **Final run after the fold-canon discharge: 0 block · 38 notice · exit 0 · 2026-10-07.**
| Gated tree | `1cf2f7475f8a1981b03e88478eda7dcbe92f2fde` · dirty — `taskboard/{models,app,modals,keymap,views}.py` · `README.md` (the batch's frozen-surface edits) · `tests/test_templates.py` · `tests/test_templates_app.py` (new) · `.dev-flow/2026-10-07-batch-07/` (the batch record, incl. `evidence/`) · `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` (the batch-07 evidence `-text` line the rollover added — verified present) · `.dev-flow/2026-10-07-batch-0{5,6}/decisions-log.json` · `.dev-flow/rollover_batch{g,h}.py` — uncommitted **by design**: the coordinator commits and pushes once per batch under the operator's commission, after the verdict |
| Requirements canon | `repo:REQUIREMENTS.md` — the living-canon fold-back for this batch's ids (US-1301 · HLR-1301 · LLR-1301.1/.2) is the coordinator's `--fold-canon` step at the commit (this close-out does not edit `REQUIREMENTS.md`, per the commission) |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (RC-1: local
  `1cf2f74` == `origin/main` at the open, re-verified at this close by `git rev-parse HEAD origin/main`;
  the batch-07 rollover's own bookkeeping — `state.json`, the batch dir, `rollover_batchh.py`, the
  `.gitattributes` line — is the batch's, listed in the dirty set above)

---

## Objective outcome (BLUF)

**Press `I`, pick a template, and the project's chain of tasks exists — linked, named, undoable in
one step.** The picker lists the board's own templates first (`settings["templates"]`, portable,
edited in the board JSON at v1) and the `Simple chain` / `Bugfix` presets after, each row
`name — N tasks`; the insert lands the tasks in the selected task's project (the focused project
when set; no resolvable project → `No project to insert into.`), in the board's first phase, with
no invented dates, linked exactly as the template's forward-only `wait` declares; the toast reads
`Inserted '<name>' — <N> tasks into <project>`; one `u` removes the whole insert and a second
says `Nothing to undo.` The `?` kanban help names the key and the board-JSON edit seat.

**The batch-06 visual re-verdict stays PENDING** (the amended C-2b frames + the new chrome) —
carried in the backlog, not this batch's gate.

## Numbers

- Suite: **2575 = 2566 − 0 + 9** — base 2566 (the batch-06 trunk), 9 new nodes (4 store arms + 5
  app arms); the README row and the `?` bullet modified no test. The shipping session's complete
  green run passed 2575 (`evidence/inc001b-run.log`, 423.20s); the close-out re-collected **2575
  tests** on the final tree (`pytest tests --collect-only -q`); the orchestrator's C-25 owns the
  ONE final clean-tree run.
- Sources touched: **4** (models · app · modals · keymap) — the four seats of one gesture, max 4 ≤ 4;
  the `views.py` help bullet and the README row are `doc`, outside the count.
- Contract: 2 LED (LED-2026-10-07-batch-07.1 the contract · LED .2 the T→I correction) · 1 US · 1 HLR · 2 LLR.
- Mutation battery: 3 mutants — **M13 · M14 · M15, all KILLED**, restores sha256-verified
  (`evidence/mutations.log`).

## What changed

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1301 (process/chain templates insertable into a project) | v1 (the key corrected `T`→`I` under LED-2026-10-07-batch-07.2 before the first edit) | AT-1301's 9 arms (4 store + 5 app) · M13/M14/M15 | pass |
| LLR-1301.1 (the template store: user settings + presets, lenient read) | v1 | the 4 store arms · M15 | pass |
| LLR-1301.2 (the insert: picker, creation, links, one undo, the toast) | v1 (amended by LED .2) | the 5 app arms · M13/M14 | pass |

## New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — (candidate, not minted) — the seat-check-before-key rule: grep the shipped keymap (and its pinning tests) for a proposed key BEFORE the contract's HLR/LLR text freezes it, so a contract can never pin a key the product already ships | a contract that pins a seat already taken — `T` ships `project_pin_toggle` (keymap.py:86, pinned by test_focus.py:46/:151 + test_markup_sites.py:267); the implementing agent's stop gate caught it before code, at the cost of a stopped session and a LED | the stopped session's transcript (`evidence/inc001-run.log`) + LED-2026-10-07-batch-07.2 — the second consecutive batch whose contract text was written before the shipped surface was checked (batch-06's marker glyphs, batch-07's key) |
| — (candidate, not minted) — the LED-sweep completeness check: a correction LED re-greps EVERY site class of the corrected claim (statements, IFC blocks, briefs, plan objectives), not only the statements it set out to fix | the LED .2 sweep corrected HLR/LLR but missed the IFC node (`keymap T`, `01-requirements.md:145`) — found at the record pass as finding F1 | `02-review.md` F1 · the packet's supersession inspection |

**The four landings — record which ones actually happened:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | not landed — nothing minted this batch | — |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | not landed — nothing minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | not landed — the lessons are recorded below; the catalog lives in the flow bundle, outside this close-out's writable tree | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | not landed — nothing minted | — |

- **New controls:** `none — this batch minted no control: the seat-check-before-key rule and the LED-sweep completeness check are recorded as candidates above with their measured origins; minting them into the flow's catalog is the operator's ruling at the next aperture (the seat-check candidate is now TWO batches deep — batch-06's shipped-surface-first rule is its parent)`

---

## Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/{models,app,modals,keymap,views}.py` · `README.md` · `tests/test_templates.py` · `tests/test_templates_app.py` | 📋 left on purpose — the batch's frozen-surface edits + the 9 new nodes' files, uncommitted by design; the coordinator commits + pushes under the commission after the operator's verdict | the gate's dirty list above; the diffs read in the increment packet |
| `.dev-flow/2026-10-07-batch-07/` | 📋 left on purpose — the batch record (this close) | the artifacts themselves |
| `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-0{5,6}/decisions-log.json` · `.dev-flow/rollover_batch{g,h}.py` | 📋 left on purpose — the batch's bookkeeping (the open-items refresh, the rolled state, the evidence `-text` line verified, batch-05/06's decisions logs archived at the rollovers, the P0 rollover helpers) | `git status --short` |

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally` (the seed's one `V26` block
  was cleared inside the writable set, not discharged; the 3 remaining `V22` canon blocks are the
  coordinator's standing discharge — `--fold-canon` at the commit, as batch-06's — and the AT-1301
  dash token already sits in the test file's docstring — `tests/test_templates_app.py:3`)

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| — | — | — |

---

## Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| US-1301 — process/chain templates insertable into a project (the operator's 2026-10-07 request) | ✅ done in `2026-10-07-batch-07` (the store + the picker + the insert + one-step undo + the toast; AT-1301's 9 arms; the T→I correction under LED .2; M13/M14/M15 KILLED) | BACKLOG · `03-increments/increment-001.md` |
| the batch-06 visual re-verdict (amended C-2b frames + the new chrome) | **carried — still OPEN** (the operator's verdict remains pending; the item is kept verbatim in the new Open section, as it was kept at batch-06's close) | BACKLOG · `2026-10-07-batch-06/05-close.md` |
| carries | ONE new open item — **template authoring from the app ("save this chain as a template"), v2** — declared inside HLR-1301, surfaced by the implementing session as the natural next increment | the "Open — after `2026-10-07-batch-07`" section in `.dev-flow/BACKLOG.md` |

---

## How the work was done

Two implementing sessions (both DeepSeek V4 Pro under the coordinator's brief —
`evidence/inc001-brief.md`) executed the batch's single increment in the MAIN checkout. The FIRST
session did the reconnaissance the brief ordered — read the contract, the keymap, the pinned tests —
and STOPPED before writing any code: it found the brief's `T` key already shipped as
`project_pin_toggle`, named the two ways taking it could only redden the suite, and asked for a
decision (`evidence/inc001-run.log`). The contract was corrected to `I` under
LED-2026-10-07-batch-07.2 before the first edit. The SECOND session then shipped: the store, the
key, the action + one-step undo, the picker, the `?` bullet, the README row (which the shipped README-census test forced — its first full-suite attempt held that
one census failure plus twenty git-state/environment arms the settled tree cleared, per the packet's
V56 note), and the two test files — reporting its targeted 9-passed run and its ONE complete green
run at 2575 (`evidence/inc001b-run.log`). The coordinator then ran the close-out
mutation battery M13-M15 (byte-level runner, restores sha256-verified — `evidence/mutations.log`),
wrote the contract at P1 (`evidence/p1_fill.py`), reviewed the increment, filled the record, and
cleared the validator from the seed's 1 block to 0. No implementing agent committed, pushed, or
stashed anything; this close-out ran no test suite — only `pytest tests --collect-only -q` for the
ledger and read-only greps.

## Human perimeter

- **Human perimeter:** `the operator's 2026-10-07 request is the commissioning input — "Creo que falta algo que no vi y es el crear templates de procesos o templates de cadenas que se reflejan en tareas que se pueden insertar a proyecto." — read with the established chain: the gates run autonomously under the two exceptions; the COORDINATOR commits and pushes at each close (no PR); synthetic boards only; the implementing agents do NOT commit/push/stash; the batch-06 visual re-verdict stays pending in the backlog. The auto-mode decision record: (1) at P1 the coordinator scoped the commission to v1 — insertion only, user templates in the board's settings + two factory presets, authoring deferred as a declared v2 carry (the request named insertion; authoring is its own surface); (2) at the stop gate the coordinator chose correction over collision — re-key `project_pin_toggle` off `T` would have moved shipped seats and their pinning tests outside the increment's budget without a verdict, so the contract took `I` (Insert), the global palette-only seat, leaving every shipped key untouched; (3) the README row the brief did not list was accepted once the shipped census test showed it was the enforceable half of the keymap contract. The operator owns the commit/push, the batch-06 visual re-verdict (still pending), the first-eye verdict on the new picker, personnel, and business judgement — the flow covers the record, the gates, and the suite.`

## Human review ledger

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + the ledger | the LED .1/.2 ↔ requirements pairings both ways (V26 green at the final gate) · the P2 gate `approve` | ❌ | `none` | — |
| `02-review.md` (the lenses) | 0 blocker · 0 major · 1 minor (F1 fixed) | ❌ | `none` | — |
| `03-increments/increment-001.md` | the 16-row gate signed · M13-M15 executed per the transcript · digests verified | ❌ | `none` | — |
| `04-validation.md` | `Result: PASS` · the ledger reconciles 2566 − 0 + 9 = 2575 | ❌ | `none` | — |
| `05-close.md` | the `Gated tree` row binds `1cf2f74` · C-44/C-45 answered | ❌ | `none` | — |
| The code | the full green at 2575 · the M13-M15 battery all KILLED | ❌ | `none — not audited line by line beyond the packet's diff reads` | the untouched regions of the five product files outside the diff hunks |
| The commission (the operator's request) | recorded in `PLAN.md` + `state.json` | ✅ | — | the operator's own words |

- **Human review ledger:** `human:coordinator — every artifact self-executed under the named lenses; no other human audited these artifacts. The single ✅ row is the operator's commissioning words, accepted as the batch's authorization, not a review of the record.`

## Lessons carried

- **Check the seat before the contract names it — and honor the agent that stops.** The contract
  pinned `T` without grepping the keymap; `T` ships `project_pin_toggle`, pinned by three tests.
  The first session stopped BEFORE writing code, named the conflict, named the predicted RED, and
  asked — the stop-and-name gate working as designed. The correction (`I`, under LED .2) cost a
  stopped session and one ledger entry, against the alternative: a suite reddened by a seat moved
  without a verdict. This is the same class as batch-06's marker-glyphs defect (contract text
  written before the shipped surface was checked) — twice in two batches makes the seat-check
  candidate control two batches deep.
- **A shipped test is the enforceable half of a contract.** The README row landed outside the
  brief's file list because `test_keymap.py:404` enforces every bound key documented — the census
  reddened on the session's own keymap change, and the row followed. Declared, accepted, and the
  packet counts it as `doc`, outside the source budget.
- **Lenient by declared semantics, not by accident.** The store skips a malformed template WHOLE
  (dropping a mid-chain task would silently rewire `wait` indices) and drops only a bad link — the
  reasoning is written in the code's docstring (`models.py:2290-2296`), the session's report, and
  the mutation log's review notes, and M15 pins the never-raising law. Silent degradation is a v1
  choice documented at the `?` seat, not an oversight.
- **The two-session shape is a feature, not a failure.** A brief that orders "read the patterns
  first" plus a gate that orders "stop and name" turned a would-be collision into a record-pass
  correction. The first session's transcript (`evidence/inc001-run.log`) is the batch's hero
  evidence.

## Standing constraints honored

- No commits/pushes/stashes by the implementing sessions or this close-out; the coordinator commits
  and pushes once per batch under the operator's commission, after the verdict. No git mutations of
  any kind were run.
- Targeted pytest only by the implementer; this close-out ran NO test suite — only
  `pytest tests --collect-only -q` to re-collect 2575 for the ledger, plus read-only greps; the
  orchestrator owns the ONE complete clean-tree run (C-25).
- `.dev-flow/**` was the only writable surface; `taskboard/` and `tests/` were never edited by this
  close-out (the mutation battery was the coordinator's run, before this close-out, with
  hash-verified restores).
- `REQUIREMENTS.md` (the living canon) was not edited — the fold-canon is the coordinator's
  mechanical step at the commit.
- Synthetic boards only; English artifacts; the reserved field names kept literal.

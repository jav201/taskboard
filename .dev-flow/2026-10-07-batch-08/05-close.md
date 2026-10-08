# Batch close — taskboard — Batch 2026-10-07-batch-08 (template authoring v2)

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` — seed baseline (before any close-out fill, over the unchanged seed files): **0 block · 52 notice · exit 0** · 2026-10-07 · mid-loop (record filled, close not yet written): **0 block · 42 notice · exit 0** · 2026-10-07 · **final loop over the complete record: 2 block · 39 notice · exit 1** · 2026-10-07. The seed carried no block: the 52 notices were the unfilled-seed placeholders (V31-V44/V47-V51/V54 — cleared by this record pass) over the historical and runtime/standing lines. **The 2 remaining blocks are ONE class, OUTSIDE the close-out's writable set: 2 × V22 — the canon fold-back** (`HLR-1401` · `LLR-1401.1` are declared as headings in the active batch's `01-requirements.md` but are not yet tokens in the living canon `REQUIREMENTS.md`; the rule fires only once the close exists): discharge = `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` at the coordinator's commit step, then re-run — the same class batch-2026-10-07-batch-07 recorded and discharged at its commit; this close-out does not edit `REQUIREMENTS.md`, per the commission. **No `V2` finding fires** — the AT-1401 dash token the rule reads sits in `tests/test_template_save_app.py`'s docstring (line 3, verified). The 39 notices: the historical/standing set (V9/V13/V22/V23/V27/V30/V42/V53 over older sealed batches, the runtime floor, V56) **plus V57's dirty-tree notice** — expected, the `Gated tree` row below declares the dirty set by design, uncommitted until the coordinator's commit. The V56 notice stands by design — the packet names both transcripts (the `6 failed`/`2 failed` sit in `evidence/mutations.log`'s deliberate per-mutant REDs and `evidence/inc001-run.log:1108`'s first full-suite attempt, tabled in increment-001 §4) and the rule's under-report branch is a notice, never a refusal | **Final run after the fold-canon discharge: 0 block · 39 notice · exit 0 · 2026-10-07.**
| Gated tree | `762d18cc4de2cf9a595fa3c49c29599b9f9524da` · dirty — `taskboard/{models,app,keymap,views}.py` · `README.md` (the batch's edits) · `tests/test_template_save.py` · `tests/test_template_save_app.py` (new) · `.dev-flow/2026-10-07-batch-08/` (the batch record, incl. `evidence/`) · `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` (the batch-08 evidence `-text` line the rollover added — verified present at `.gitattributes:16`) · `.dev-flow/2026-10-07-batch-0{5,6,7}/decisions-log.json` · `.dev-flow/rollover_batch{g,h,i}.py` — uncommitted **by design**: the coordinator commits and pushes once per batch under the operator's commission, after the verdict |
| Requirements canon | `repo:REQUIREMENTS.md` — the living-canon fold-back for this batch's ids (US-1401 · HLR-1401 · LLR-1401.1) is the coordinator's `--fold-canon` step at the commit when the rule fires it (this close-out does not edit `REQUIREMENTS.md`, per the commission) |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (RC-1: local
  `9a13c12` == `origin/main` at the open, `state.json` `base_ref`; re-verified at this close by
  `git rev-parse HEAD origin/main` — both now at `762d18c`, the batch-06 verdict commit the
  coordinator landed on top of the base, docs-only). The untracked `decisions-log.json` files
  (batch-05/06/07) and `rollover_batch{g,h}.py` predate the batch — the coordinator's carried
  bookkeeping, listed in the dirty set; the batch-08 rollover's own files (the batch dir,
  `rollover_batchi.py`, the `.gitattributes` line, the rolled `state.json`) are the batch's.

---

## 1 · What changed

*(BLUF. What the user can now do that they could not before, and through which surface. Then the mechanism.)*

**On the chain map, `,` on a selected tile → type a name → press enter — the chain is a template
from then on.** The one-line name prompt opens prefilled with the chain's first task's title; the
tile's whole open component — every open task of its project reachable through `depends_on` in
both directions — is stored in the board's `settings["templates"]` under the typed name, in a
deterministic topological order (every `wait` points backward; a task with several predecessors
keeps its FIRST link, the rest dropped — the template shape cannot hold a diamond, declared); the
board is saved and the toast `Template '<name>' saved — <N> tasks` renders. The new template lists
FIRST in the `I` picker from that moment and inserts through the batch-07 insert. Esc or an empty
name cancels with nothing written — the board file's bytes are untouched. Saving is NOT an undo
step (declared, docstring-pinned): it writes settings, not tasks. The `,` key ships view-scoped on
the chain map as the key NAME `comma` — a literal `,` is Textual's alias separator — discoverable
via the docked keybar and the `?` bullet; the in-frame footer key-hints were deliberately left
byte-untouched (golden C-2b frames).

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1401 (save a chain as a template from the app) | v1 | AT-1401's 11 arms (7 unit + 4 app) · M16/M17 | pass |
| LLR-1401.1 (the component walk and the template shape) | v1 | the 7 unit arms · M17 | pass |

**How the work was done.** ONE implementing session (DeepSeek V4 Pro under the coordinator's brief —
`evidence/inc001-brief.md`) executed the batch's single increment in the MAIN checkout. The session
read the seats first (the batch-07 store/picker/insert, the TextPrompt pattern, the `x`/`m`
view-dispatch wiring), verified the `,` seat free (the brief's discipline grep → 0), and shipped:
the walk, the action + named callback, the view-scoped key, the `?` bullet, the README row (which
the shipped README-census test forced — its first full-suite attempt held that one census failure
plus the G-011 flake, per the packet's V56 note), and the two test files — reporting its targeted
11-passed run and its settled full run at `1 failed, 2585 passed` (`evidence/inc001-run.log`). The
coordinator then ran the close-out mutation battery M16-M17 (byte-level runner, restores
sha256-verified — `evidence/mutations.log`), reviewed the increment (`02-review.md` approve), and
filled this record. No implementing agent committed, pushed, or stashed anything; this close-out
ran no test suite — only `pytest tests --collect-only -q` for the ledger (2586) and read-only
greps.

**The G-011 declaration** (exactly as the backlog states it): `test_win_clipboard_roundtrip`
remains an intermittent environmental flake (G-011): it failed on its own clipboard SETUP in
every B2 gate run — and fired there again at this batch's full-suite run (the test's own message:
`SETUP failed — this is the environment, not the code under test`, the PowerShell `Set-Clipboard`
ExternalException). The coordinator verified it fails isolated too (`1 failed in 4.19s`,
`evidence/inc001-run.log:1251-1266`). The BACKLOG has carried it since batch B2; the increment
touched no clipboard seat. It is the suite's ONLY failure; the suite otherwise passed 2585 at the
settled run, 2586 collected at this close.

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — (candidate, not minted) — the key-name-before-key-literal rule: when a contract names a punctuation key, bind the Textual key NAME (probe `_character_to_key`) and ship the literal as the DISPLAY — never bind the literal (Textual's binding grammar treats `,` as the alias separator and dies at construction) | a keymap line that kills COLLECTION with `InvalidBinding` — the first `,` construction died before any test ran (`evidence/inc001-run.log:978-1000`); the batch-07 parent rule (grep the shipped seat before the contract freezes a key) catches collisions, NOT grammar traps — this is its complement | this batch's executed evidence + batch-07's T-key stop (the seat-check candidate is now THREE batches deep) |
| — (candidate, not minted) — the golden-frame documentation-seat rule: a new chainmap key that must not disturb the byte-golden footer documents at the docked-keybar + `?` seats instead, and the record declares the trade | an in-frame hint edit that would reopen the byte-exact oracle the operator re-verified at `762d18c` — this batch deliberately vetoed its own footer hint and recorded the discoverability trade | `02-review.md` observation (a) · the packet's §1/§5 · the close's lessons |

**The four landings — record which ones actually happened:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | not landed — nothing minted this batch | — |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | not landed — nothing minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | not landed — the lessons are recorded below; the catalog lives in the flow bundle, outside this close-out's writable tree | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | not landed — nothing minted | — |

- **New controls:** `none — this batch minted no control: the key-name-before-key-literal rule and the
  golden-frame documentation-seat rule are recorded as candidates above with their measured
  origins; minting them into the flow's catalog is the operator's ruling at the next aperture (the
  seat-check candidate they extend is now three batches deep)`

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/{models,app,keymap,views}.py` · `README.md` · `tests/test_template_save.py` · `tests/test_template_save_app.py` | 📋 left on purpose — the batch's edits + the 11 new nodes' files, uncommitted by design; the coordinator commits + pushes under the commission after the operator's verdict | the gate's dirty list above; the diffs read in the increment packet |
| `.dev-flow/2026-10-07-batch-08/` | 📋 left on purpose — the batch record (this close) | the artifacts themselves |
| `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-0{5,6,7}/decisions-log.json` · `.dev-flow/rollover_batch{g,h,i}.py` | 📋 left on purpose — the batch's bookkeeping (the header refresh + the only-open-item closed, the rolled state, the evidence `-text` line verified, the carried decisions logs + rollover helpers) | `git status --short` |

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally` (no V-block was discharged
  to pass; the standing V56 under-report notice persists by design with its transcripts named in
  increment-001 §4; the canon fold-back the final gate fired for `HLR-1401` · `LLR-1401.1` — 2 ×
  V22 — is the coordinator's standing discharge, `--fold-canon` at the commit, as batch-07's, and
  the AT-1401 dash token already sits in the test file's docstring —
  `tests/test_template_save_app.py:3`)

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| — | — | — |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| US-1401 — save a chain as a template from the app (the operator's 'continua junto con deepseek lo que sigue' 2026-10-07 — the batch-07 carry) | ✅ done in `2026-10-07-batch-08` (the walk + the action + the view-scoped `comma` key + the doc seats; AT-1401's 11 arms; M16/M17 KILLED) | BACKLOG · `03-increments/increment-001.md` |
| Template authoring from the app — v2 (queued at batch-07, the backlog's ONLY open feature item) | ✅ **CLOSED** — shipped by this batch; struck in place in the "Open — after `2026-10-07-batch-07`" section | BACKLOG |
| the batch-06 visual re-verdict (amended C-2b frames + the new chrome) | **CLOSED before this batch closed** — the coordinator folded the operator's verdict ("Se ve bien.", all four accepted) at `762d18c`; the backlog's re-verdict item reads done; NOT reopened here | BACKLOG · `2026-10-07-batch-06/evidence/veredicto-batch06.json` |
| carries | NOTHING new open — the "Open — after `2026-10-07-batch-08`" section reads "Nothing new from this batch"; the G-011 environmental flake line stands as the only standing item | the "Open — after `2026-10-07-batch-08`" section in `.dev-flow/BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-07-batch-08
mode: core
verdict: pass
increments: 1
source_files_max: 3          # highest source-file count in any one increment
notices_raised: 5            # ⚠ declared across the batch (views.py-as-doc · README row outside the brief · footer-hint trade · the pinned `1 tasks` degenerate literal · the mutations.log M17 parenthetical wording slip)
rework_returns: 0            # items that came back, per QA's phase checklists
triggers_fired: "none"
tests_base_to_post: "2575 -> 2586"
new_control: none
open_items_next: 0
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + the ledger | LED-2026-10-07-batch-08.1 ↔ requirements pairings both ways (no V26 finding at the gate) · the P2 gate `approve` | ❌ | `none` | — |
| `02-review.md` (the lenses) | 0 blocker · 0 major · 0 minor — two declared observations | ❌ | `none` | — |
| `03-increments/increment-001.md` | the 16-row gate signed · M16/M17 executed per the transcript · digests verified | ❌ | `none` | — |
| `04-validation.md` | `Result: PASS` · the ledger reconciles 2575 − 0 + 11 = 2586 | ❌ | `none` | — |
| `05-close.md` | the `Gated tree` row binds `762d18c` · C-44/C-45 answered | ❌ | `none` | — |
| The code | the settled full run 2585 + the declared flake · the M16-M17 battery all KILLED | ❌ | `none — not audited line by line beyond the packet's diff reads` | the untouched regions of the product files outside the diff hunks |
| The commission (the operator's request) | recorded in `PLAN.md` + `state.json` | ✅ | — | the operator's own words |
| The batch-06 visual verdict fold | `762d18c` == the coordinator's commit on top of the base, re-verified by `git rev-parse` | ✅ | — | the operator's "Se ve bien." — the human verdict itself, accepted as given |

- **Human perimeter:** `the operator's 2026-10-07 words are the commissioning input — "si no hay nada
  que decidir continua junto con deepseek lo que sigue" — read with the established chain: the
  gates run autonomously under the two exceptions; the COORDINATOR commits and pushes at each close
  (no PR); synthetic boards only; the implementing agents do NOT commit/push/stash. The batch-06
  visual verdict arrived mid-batch ("Se ve bien.", all four accepted) and was folded by the
  coordinator at 762d18c before this close — the record carries it as done, not pending. The
  auto-mode decision record: (1) at P1 the coordinator scoped the queued carry to its contract —
  one increment, one HLR, the fan-in drop and the no-undo semantics declared in the text; (2) the
  `,` key's group deviated from the brief's guess to the shipped seat (task) at the agent's seat
  census — declared, not a LED; (3) the README row the brief did not list was accepted once the
  shipped census test showed it was the enforceable half of the keymap contract — the same
  acceptance batch-07 set. The operator owns the commit/push, the first-eye verdict on the new name
  prompt, personnel, and business judgement — the flow covers the record, the gates, and the suite.`
- **Human review ledger:** `human:coordinator — every artifact self-executed under the named lenses;
  no other human audited these artifacts. The two ✅ rows are the operator's commissioning words
  and the operator's visual verdict, accepted as the batch's authorizations, not reviews of the
  record.`

## Lessons carried

- **A literal punctuation key is a grammar trap, not just a seat collision.** Batch-07's rule —
  grep the shipped keymap before the contract freezes a key — catches collisions. It cannot catch
  Textual's binding grammar: a literal `,` IS the alias separator, and the first construction died
  at COLLECTION (`InvalidBinding: Can not bind empty string`) before any test ran. The working
  move, now measured twice over: bind the canonical key NAME (`comma`, probed via
  `_character_to_key`), ship the literal as the display, and let the keybar re-derive. The candidate
  control is recorded in §2.
- **Golden frames veto in-frame hints; the keybar and `?` are the documentation seats.** The
  chainmap footer's key-hint row is byte-golden in the C-2b frames the operator re-verified at
  762d18c. Shipping `,` WITHOUT touching it costs nothing discoverable — the docked keybar
  re-derives from the keymap seat and the `?` bullet names the key — while touching it would have
  reopened the oracle. First batch where a golden frame actively vetoed an in-frame hint; the
  trade is declared, and recurrence makes it a rule.
- **The forced README row is the enforceable half of the keymap contract — twice now.** Two
  consecutive batches landed a keybinding row outside the brief's file list because
  `test_keymap.py:404` enforces every bound key documented. The record's standing treatment: `doc`,
  outside the source budget, declared. A third occurrence should just add "the README row" to the
  briefs' file lists.
- **One session, one brief, green the same evening.** Batch-07's two-session shape (stop-and-name)
  was the right shape for a conflict; this batch needed none — the seat was free, the grammar trap
  was caught by collection and probed inside the session, and the single session shipped 11 arms
  with two full-suite runs. The discipline that matters is invariant: read the seats first, verify
  the seat free, stop-and-name on anything outside your files (here: the census failure + the
  flake, both named in the report).
- **A battery's parenthetical is prose, not a verdict.** The stored `mutations.log` named M17's
  GREEN arm "the round-trip arm"; the resolved arms say it is the None-cases arm. The count
  (`6 failed, 1 passed`) is the load-bearing fact and it matched — but the record declares the slip
  rather than laundering it through a silent edit of the transcript. Stored evidence stays
  byte-verified; the reconciliation lives in the packet.

## Standing constraints honored

- No commits/pushes/stashes by the implementing session or this close-out; the coordinator commits
  and pushes once per batch under the operator's commission, after the verdict. No git mutations of
  any kind were run (read-only `git rev-parse`/`git status`/`git show`/`git diff` only).
- Targeted pytest only by the implementer; this close-out ran NO test suite — only
  `pytest tests --collect-only -q` to re-collect 2586 for the ledger, plus read-only greps; the
  orchestrator owns the ONE complete clean-tree run (C-25).
- `.dev-flow/**` was the only writable surface; `taskboard/` and `tests/` were never edited by this
  close-out (the mutation battery was the coordinator's run, before this close-out, with
  hash-verified restores).
- `REQUIREMENTS.md` (the living canon) was not edited — the fold-canon is the coordinator's
  mechanical step at the commit.
- Synthetic boards only; English artifacts; the reserved field names kept literal.

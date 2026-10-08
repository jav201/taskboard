# Close — taskboard — Batch 2026-10-07-batch-06 (the operator-feedback batch)

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" --brief .` → **5 block · 37 notice · exit 1** · 2026-10-07 — the close-out's validation loop over the filled record. The seed baseline (run before any close-out fill) read 0 block · 51 notice; the loop cleared every block reachable inside the close-out's writable set (`.dev-flow/**`): the packets' reserved fields, the RED counterfactuals, the review naming, the evidence digests, the V41 shape (evidence-home rows only). The 5 blocks that remain are ONE class, OUTSIDE `.dev-flow/**`: **5 × V22 — the canon fold-back** (`HLR-1201` · `HLR-1202` · `LLR-1201.1` · `LLR-1201.2` · `LLR-1202.1` are not yet tokens in the living canon `REQUIREMENTS.md`): discharge = `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-init.py" --fold-canon` at the coordinator's commit step, then re-run — the same class batch-2026-10-07-batch-05 recorded and discharged at its commit; the close-out does not edit `REQUIREMENTS.md`, per the commission. **No `V2` finding fires** — the AT-1201/AT-1202 dash tokens the coordinator placed in the test files' docstrings (`tests/test_chainmap_app.py:1` · `tests/test_kanban_window.py:1`) satisfy the AT-token rule. The 37 NOTICEs are historical-batch lines (`V9`/`V13`/`V22`/`V23`/`V42`/`V53` over older sealed batches) plus the runtime-expected ones (`V27`'s decisions-log currency over the rolled `state.json` · `V30`'s bundle-floor half-derivation) | **Final run after the fold-canon discharge: 0 block · 37 notice · exit 0 · 2026-10-07.**
| Gated tree | `8284d3af9a570ac773d5370c4308986f32adf2fc` · dirty — `taskboard/views.py` · `tests/{test_app,test_chainmap,test_chainmap_app,test_kanban_readable}.py` (the batch's frozen-surface edits) · `tests/test_kanban_window.py` (new) · `.dev-flow/2026-10-07-batch-06/` (the batch record, incl. `evidence/`) · `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` (the batch-06 evidence `-text` line the rollover added) · `.dev-flow/2026-10-07-batch-05/decisions-log.json` · `.dev-flow/rollover_batchg.py` — uncommitted **by design**: the coordinator commits and pushes once per batch under the operator's commission, after the verdict |
| Requirements canon | `repo:REQUIREMENTS.md` — the living-canon fold-back for this batch's ids (US-1201/1202 · HLR-1201/1202 · LLR-1201.1/.2 · LLR-1202.1) is the coordinator's `--fold-canon` step at the commit (the close-out does not edit `REQUIREMENTS.md`, per the commission) |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (RC-1: local
  `8284d3a` == `origin/main` at the open, pushed at batch-05's close; the batch-06 rollover's own
  bookkeeping — `state.json`, the batch dir, `rollover_batchg.py`, the `.gitattributes` line — is the
  batch's, listed in the dirty set above)

---

## Objective outcome (BLUF)

**The chain map is now the place where chains are born; the kanban window announces its hidden
sides.** On a board with zero links, the map draws every open task as a one-row `○` tile
(selectable, reachable by the arrows), `L` on a tile opens the shipped LinkPicker and the pick
lands as the task's first incoming link right there, `x` leaves the task a visible re-linkable
tile, the strip says `◂ waits on  nothing yet`, and the inert `no links` row survives only for a
project with no open work. The kanban's phase-head row now carries `◂` before the first visible
phase when the window is offset and ` ▸ N` (N exact) after the last when columns hide right —
nothing when everything fits — and the `?` help gained the window bullet. The C-2b oracle frames
amend under LED-2026-10-07-batch-06.1: the amended frames are this renderer's bytes on the same
frozen fixture, stored at the batch's evidence home (sha256-verified); the sealed batch-02 frames
stay history.

**The operator's visual re-verdict is PENDING — on the amended C-2b frames AND the new chrome**
(the `○` tiles, the window markers): the batch pushes under the commission; the operator's
verdict folds on arrival (batch C's exact form).

## Numbers

- Suite: **2566 = 2556 − 0 + 10** — base 2556 (the batch-05 trunk), 10 new nodes (4 window arms +
  3 tile unit arms + 3 tile app arms); the TC-810/AT-802/AT-801c amendments, the `FRAMES` move and
  the two pinned kanban updates modified, not added. The session's two complete green runs passed
  2566 (`evidence/inc001-run.log`), and the close-out re-collected **2566 tests** on the final
  tree (`pytest tests --collect-only -q`); the orchestrator's C-25 owns the ONE final clean-tree run.
- Sources touched: **1** (`taskboard/views.py`) — one file per increment, max 1 ≤ 4.
- Contract: 1 LED (LED-2026-10-07-batch-06.1) · 2 US · 2 HLR · 3 LLR.
- Mutation battery: 4 mutants — **M9 · M10 · M11 · M12, all KILLED**, restores sha256-OK
  (`evidence/mutations.log`); M9 doubles as the oracle amendment's RED counterfactual.

## What changed

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1201 (the chain map admits every open task; chains are created on the map) | v1 (amending the C-2b oracle under LED-2026-10-07-batch-06.1) | AT-1201 (L on the map · x leaves a tile · nav reaches a tile) · the amended TC-801/TC-802 · the amended TC-810 · M9/M10/M11 | pass |
| HLR-1202 (the kanban window shows its hidden sides) | v1 | AT-1202 (the 4 arms) · the pinned arms at `test_app.py:1598-1603` / `test_kanban_readable.py:557` · M12 | pass |

## New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — (candidate, not minted) — the shipped-surface-first contract rule: check the chrome the product already ships (grep it) BEFORE minting a glyph law in the contract | a contract that specifies "new" glyphs the product already ships in another chrome — the marker law was written against an imagined blank slate while `◀ N`/`N ▶` were pinned in `test_app.py` | `evidence/mutations.log`'s review note + the removed `-` lines of the pinned arms (increment-001's packet §1) |
| — (candidate, not minted) — the oracle-amendment protocol: when a renderer change moves a sealed oracle's bytes, amend under a formal LED — the amended frames are the NEW renderer's bytes on the SAME frozen fixture at the batch's evidence home, the test's frame path moves citing the LED, the sealed frames stay history, and the admission-dropping mutation doubles as the amendment's RED counterfactual | a silent oracle drift (hand-edited frames) or a stale frame path pinning the old bytes forever | the amended frames' digests (`cd955e18…`/`227a2ced…`) + M9 in `evidence/mutations.log` |

**The four landings — record which ones actually happened:**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | not landed — nothing minted this batch | — |
| 2 | its **artifact** (a template section) — a control with no output degrades to "I thought about it" | not landed — nothing minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | not landed — the lessons are recorded below; the catalog lives in the flow bundle, outside this close-out's writable tree | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | not landed — nothing minted | — |

- **New controls:** `none — this batch minted no control: the shipped-surface-first contract rule and the oracle-amendment protocol are recorded as candidates above with their measured origins; minting them into the flow's catalog is the operator's ruling at the next aperture`

---

## Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py` · `tests/{test_app,test_chainmap,test_chainmap_app,test_kanban_readable}.py` · `tests/test_kanban_window.py` | 📋 left on purpose — the batch's frozen-surface edits + the 10 new nodes' files, uncommitted by design; the coordinator commits + pushes under the commission after the operator's verdict | the gate's dirty list above; the diffs read in the increment packets |
| `.dev-flow/2026-10-07-batch-06/` | 📋 left on purpose — the batch record (this close) | the artifacts themselves |
| `.dev-flow/BACKLOG.md` · `.dev-flow/state.json` · `.gitattributes` · `.dev-flow/2026-10-07-batch-05/decisions-log.json` · `.dev-flow/rollover_batchg.py` | 📋 left on purpose — the batch's bookkeeping (the open-items refresh, the rolled state, the evidence `-text` line, batch-05's decisions log archived at the rollover, the P0 rollover helper) | `git status --short` |

### Conditional-gate discharge

- **Conditional-gate discharge:** `none — no gate closed conditionally` (if `V22`/`V2` promote to
  blocks at the coordinator's station advance, the discharge is the coordinator's, as batch-05's:
  `--fold-canon` at the commit for the canon fold-back; the AT-1201/AT-1202 dash tokens already sit
  in the test files' docstrings — `tests/test_chainmap_app.py:1` · `tests/test_kanban_window.py:1`)

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| — | — | — |

---

## Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| US-1201 — the chain map shows every open task; chains are created on the map | ✅ done in `2026-10-07-batch-06` (the `○` tiles + L/x/nav on the map + the strip truth; AT-1201; the amended oracle under LED .1; M9/M10/M11) | BACKLOG · `03-increments/increment-002.md` |
| US-1202 — the kanban shows its hidden phase columns | ✅ done in `2026-10-07-batch-06` (`◂`/`▸ N` on the head row + the `?` bullet; AT-1202; M12) | BACKLOG · `03-increments/increment-001.md` |
| carries | ONE new open item — **the operator's visual re-verdict on the amended C-2b frames + the new chrome (PENDING; the batch pushes under the commission; the operator's verdict folds on arrival — batch C's form)** — plus the queued batch-07 (process/chain templates: user templates in settings + factory presets, `T` picker, one undo step — the operator's request, scoped by the coordinator, to be contracted at batch-07's P1) | the "Open — after `2026-10-07-batch-06`" section in `.dev-flow/BACKLOG.md` |

---

## How the work was done

One implementing session (DeepSeek V4 Pro under the coordinator's brief — `evidence/inc001-brief.md`)
executed BOTH increments in the MAIN checkout, in the brief's order: task 1 (the kanban window
markers) then task 2 (the `○` tiles + the oracle amendment), with scratch confined to the batch's
`evidence/` (`gen_frames.py` + the `c2b.json` fixture — batch-05's sandbox rule held; the session's
stray scratch boards at the repo root were removed at the coordinator's review, and the dirty list
above is the settled one). The session read the sealed batch-02 frames before amending them,
regenerated the frames through the test's own render path, moved the `FRAMES` path under the LED,
extended the two chainmap test files, updated the three layout-driven pinned tests + the two pinned
kanban arms, and ran the targeted suites (399 · 19 · 30-deselected) and the full suite twice green
at 2566 (`evidence/inc001-run.log`). The coordinator then ran the close-out mutation battery
M9-M12 (byte-level runner, restores sha256-OK — `evidence/mutations.log`), wrote the contract at P1
(`evidence/p1_fill.py` · `p1b_fill.py`), reviewed both increments, and wrote this record. No
implementing agent committed, pushed, or stashed anything.

## Human perimeter

- **Human perimeter:** `the operator's two 2026-10-07 reports from real use are the commissioning input — (1) the kanban hides the later phase columns with no on-screen sign of the window ("no logro ver el resto... incluso reescalando"); (2) the chain map shows projects with no tasks and no way to create a chain ("es imposible crear cadenas") — read with the established chain: the gates run autonomously under the two exceptions; the COORDINATOR commits and pushes at each close (no PR); synthetic boards only; the implementing agents do NOT commit/push/stash. The auto-mode decision record: at P1 the coordinator weighed the discovery-only alternative (a help bullet / an announcement, no surface change) against the root fix for BOTH reports; the operator's "es imposible crear cadenas" — a report that the surface itself was a dead end, not merely undocumented — decided it: discoverability-only remedies were rejected in favor of root fixes (the tiles admit every open task; the markers announce the window on the surface). The operator owns the commit/push, the visual re-verdict on the amended frames + the new chrome at the next session, personnel, and business judgement — the flow covers the record, the gates, and the suite.`

## Human review ledger

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + the ledger | the LED .1 ↔ 5 requirements both ways (V26) · the P2 gate `approve` | ❌ | `none` | — |
| `02-review.md` (the lenses) | 0 blocker · 0 major · 0 minor | ❌ | `none` | — |
| `03-increments/increment-001..002.md` | the 16-row gates signed · M9-M12 executed per the transcript · digests verified | ❌ | `none` | — |
| `04-validation.md` | `Result: PASS` · the ledger reconciles 2556 − 0 + 10 = 2566 | ❌ | `none` | — |
| `05-close.md` | the `Gated tree` row binds `8284d3a` · C-44/C-45 answered | ❌ | `none` | — |
| The code | the two full greens at 2566 · the M9-M12 battery all KILLED | ❌ | `none — not audited line by line beyond the packets' diff reads` | the untouched regions of views.py outside the diff hunks |
| The commission (the operator's two reports) | recorded in `PLAN.md` + `state.json` | ✅ | — | the operator's own words |

- **Human review ledger:** `human:coordinator — every artifact self-executed under the named lenses; no other human audited these artifacts. The single ✅ row is the operator's commissioning words, accepted as the batch's authorization, not a review of the record.`

## Lessons carried

- **Check the shipped surface before writing the contract.** HLR-1202 specified the window markers
  as if new; the product had shipped hidden-phase marks in a prior chrome (`◀ N` / `N ▶`), pinned by
  `test_app.py`'s window test. The review caught the writing defect and folded it: the batch refines
  the form (`◂` / `▸ N`), keeps the exact count, adds the left-edge case and the `?` bullet — the
  operator's real gap was discoverability, and the help bullet is the substantive fix. A contract
  that mints a glyph law should grep the shipped chrome first.
- **The oracle-amendment protocol, executed end to end.** A renderer change that moves a sealed
  oracle's bytes amends under a formal LED: the amended frames are the new renderer's bytes on the
  same frozen fixture (generated, CRLF, sha256-verified at rest), the test's frame path moves
  citing the LED, the sealed frames stay history — and the admission-dropping mutation (M9) doubles
  as the amendment's RED counterfactual: without the renderer change the frames cannot match.
- **Layout-driven reddening is not mechanism reddening — name it honestly.** Three pinned tests
  (TC-810 · AT-802 · AT-801c) reddened because the tiles grew every band and the shipped fold law
  then folded bands at familiar sizes. Each update changed a fixture, a size, or a selection —
  never a law's threshold — and the packet names all three. The all-fits marker arm asserts the new
  glyphs' absence only; the pre-batch glyphs were different codepoints (declared in the packet so
  the next reader does not "strengthen" it into something it never was).
- **Sandbox discipline held.** One session, scratch under the batch's `evidence/` (the frames
  generator + its fixture), no `/tmp` repro, no git mutations by the implementing agent; the stray
  root-level scratch boards were caught at review and removed before the close.

## Standing constraints honored

- No commits/pushes/stashes by the implementing session or this close-out; the coordinator commits
  and pushes once per batch under the operator's commission, after the verdict. No git mutations of
  any kind were run.
- Targeted pytest only (the close-out ran `pytest tests --collect-only -q` to re-collect 2566, plus
  read-only greps); the full suite was never run here — the orchestrator owns the ONE complete
  clean-tree run (C-25).
- `.dev-flow/**` was the only writable surface; `taskboard/` and `tests/` were never edited by this
  close-out (the mutation battery was the coordinator's run, before this close-out, with
  hash-verified restores).
- `REQUIREMENTS.md` (the living canon) was not edited — the fold-canon is the coordinator's
  mechanical step at the commit.
- Synthetic boards only; English artifacts; the reserved field names kept literal.

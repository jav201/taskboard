# Batch close — taskboard — Batch 2026-10-02-batch-04

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
| Gate record | Re-close, 2026-10-04: `devflow-validate.py --brief` from the same rev99 snapshot, **0 block · 26 notice · 61 not applicable**, exit 0 (`evidence/validator-reclose.txt`, sha256 `98315fdc…`, the same notice set as the first close). First close, 2026-10-03: `devflow-validate.py --brief` from the read-only rev99 snapshot (skills `1154c8a`, flow_hash `16c4f1a047699996`, D-420), 2026-10-03: **0 block · 26 notice · 61 not applicable**, exit 0 (`evidence/validator-close.txt`, sha256 `98315fdc…`). The notices are inherited from closed batches, plus V57 for the uncommitted tree (this table's own Gated tree row). |
| Gated tree | `56a1b10cc4667bfcde3ff84c593e770eced990a8` · dirty: every change is still in the working tree, waiting for the coordinator's commit (standing authorization: the coordinator commits and pushes to `main`; this agent does not commit). Files: `taskboard/modals.py`, `taskboard/app.py`, `taskboard/views.py`, `taskboard/models.py`, `taskboard/team_sync.py`, `taskboard/taskboard.tcss`, `tests/test_app.py`, `tests/test_archive.py`, `tests/test_details_markup.py`, `tests/test_edit_window.py`, `tests/test_prism_laws.py`, `tests/test_markup_census.py` (new), `tests/test_markup_sites.py` (new), `tests/test_highlight_segments.py` (new), `tests/test_control_bytes.py` (new), `tests/test_sync_fields.py` (new), `tests/test_details_grid.py` (new), `.gitattributes`, `REQUIREMENTS.md`, `.dev-flow/state.json`, `.dev-flow/BACKLOG.md`, `.dev-flow/2026-10-02-batch-03/decisions-log.json` (new), `.dev-flow/2026-10-02-batch-04/**` (new) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`), folded with the rev99 snapshot's `devflow-init.py --fold-canon`: 13 folded (4 HLR, 9 LLR), 0 refused; a second run folds nothing (`evidence/p5-fold-canon.txt`); at the re-close the LLR-403.1 row was updated by hand to amendment A-7 (the fold never rewrites an existing row, D-423) |

---

## 1 · What changed

**Bracket, backslash and emoji text — the operator's or a teammate's — no longer kills, empties or
rewrites a dialog, picker or toast; control bytes from a board file, a teammate's file or the clipboard
never reach the terminal; a shared `team.json` can no longer run an app action, crash a view or grow
the board; and the task details view shows its five fields.** Every dialog, picker, select, button
and toast builds user, synced and OS text as Rich `Text` pieces that no markup parser reads (operator
ruling "Piezas de texto, sin formato"); a census test derives every Textual sink and parser call from
the code and fails on a new unsafe one. One control-byte rule runs at the board-load, team-sync,
Setup and clipboard doors. Synced project and roster fields pass the loading rule; an empty synced id
and a deeply nested shared file are refused. One scoped stylesheet rule paints the details grid; after the operator's visual verdict (2026-10-04)
the batch re-opened (D-422) and increment 004 moved the blank row under the details title and
narrowed its label column to 10 cells (UX-3, UX-4; PV-1 accepted).
Security S-1 (HIGH, a teammate's status firing an app action on click) is closed and verified.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-401 | v1 (amended A-1, A-2, A-4) | AT-401 · AT-402 · AT-403 · TC-401..406 · TC-412 · TC-415 · TC-417 | pass |
| LLR-401.1 | v1 | TC-401 · TC-402 · TC-403 · TC-404 | pass |
| LLR-401.2 | v1 | TC-405 · TC-412 | pass |
| LLR-401.3 | v1 (A-2, A-3) | TC-406 · TC-415 · TC-417 | pass |
| HLR-402 | v1 | AT-404 · AT-405 · TC-407..410 · TC-414 · TC-419 | pass |
| LLR-402.1 | v1 (A-5) | TC-407 · TC-414 | pass |
| LLR-402.2 | v1 | TC-408 · TC-410 | pass |
| LLR-402.3 | v1 (A-5) | TC-409 · TC-419 | pass |
| HLR-403 | v1 (threshold amended A-7) | AT-406 · TC-411 · TC-420 · TC-421 | pass |
| LLR-403.1 | v2 (A-6, amendment A-7) | TC-411 · TC-420 · TC-421 | pass |
| HLR-404 | v1 | AT-407 · TC-413 · TC-416 · TC-418 | pass |
| LLR-404.1 | v1 (A-5) | TC-413 · TC-418 | pass |
| LLR-404.2 | v1 | TC-416 | pass |

Tests: 1855 → 2218. The P4 gate run was 2214 passed, exit 0 (`evidence/p4-gate.txt`). The increment-004 gate run was 2218 passed in 398.62 s, exit 0 (`evidence/inc004-gate-r3.txt`), and the light P4 passed (qa PASS-WITH-NOTES, ux PASS; `04-validation.md` §Increment 004 re-validation).

**Security close pass (mandatory): `security-reviewer` PASS-WITH-NOTES, no HIGH open.**
- **Re-probed on the final tree:** S-1 (HIGH) and S4-1 (MEDIUM) were probed again and still hold.
  - S-1: a hostile `team.json` status loads as `on_track`; clicking every picker cell fires the action 0 times.
  - S4-1: the app boots 15 of 15 times at nesting depths 990 to 200000 in `team.json`, a teammate's file and `board.json`.
- **Every other S-finding** holds as folded or routed. The final tree matches each increment's last frozen set.
- **S6-1 (LOW), folded at close:** two evidence scripts (`make_mutants_inc002.py`, `make_mutants_inc002_r2.py`) wrote the home path. They now resolve it from `Path(__file__)`. The batteries they generated are unchanged: the sha256 of `mutants_inc002.json` (`6c66796a…`) and `mutants_inc002_r2.json` (`a0977f27…`) match the hashes recorded during increment 002.
  - Re-running the r2 script overwrote its hand-edited battery. I restored it by replaying the two recorded edits (N13, then R7/R8), and the restored file matches its recorded hash.
  - No account path remains under the batch folder.
- **S6-2 (LOW), discharged:** S4-3 and S4-4 already carry their text in `BACKLOG.md` ("Hand-edited data is normalised silently", and the census residuals item).
- **Re-close delta pass (2026-10-04): PASS-WITH-NOTES, no HIGH.** Increment 004 is presentation only: two CSS rules scoped to `#details-box`, no Python change, no new input, I/O or network path. The new evidence holds no secret, account name or personal data. S7-1 (LOW, pre-existing): `state.json` `owner` carries the full local path with the account name, already at `56a1b10` → BACKLOG.
- **Noted:** `p4-gate.txt` does not name the tree it ran on. The reviewer tied it to the final tree through the frozen hashes. Recorded here and left as-is.

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|

**The four landings — record which ones actually happened.**

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a — no control minted | — |
| 2 | its **artifact** (a template section) | n/a — no control minted | — |
| 3 | the **catalog** entry (`dev-flow-lessons`) | n/a — no control minted | — |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a — no control minted | — |

- **New controls:** none — every failure in this batch was caught by an existing control: the vacuous census rule (Q-1/S-2) and the vacuous test clauses (code review F1 of increment 003, the TC-418 masking fixture, the C2 planted arm, the `_dirty` fixture) by C-40/C-55 (falsifiability, positive controls) through the reviewers and the mutation batteries; the crash on an empty highlight `====` (D-415) by C-39 pre-execution of the tokeniser split. One stack-specific lesson — `run_test` hides toasts unless `notifications=True` — belongs to the project's `docs/engineering-rules.md` (BACKLOG), not to the flow.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| every file in §0 *Gated tree* | 📋 ready to commit — the coordinator commits and pushes to `main` without a PR, the operator's visual verdict now given and applied (standing authorization, `merge: false`); this agent does not | `git status --short` |
| `~/.claude/skills` | not touched by this batch; another session committed rev100 work there during the batch (D-420), reported as found | `git -C ~/.claude/skills log --oneline -3` |
| scratch exports, probes, the rev99 snapshot | outside the repo (session scratchpad), not part of the record | — |

- **Found before the batch:** `none — no tracked file was modified when the batch began`

### Conditional-gate discharge

- **Conditional-gate discharge:** 7 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| P2 security `BLOCK-UNTIL: S-1` (applied and verified) | ✅ | `03-increments/increment-002.md` §4b — S-1 CLOSED with `p_status4` transcripts |
| P2 security `BLOCK-UNTIL: S-2` (the census over `_rich`) | ✅ | `03-increments/increment-001.md` §4 — TC-406, TC-403; C1–C6 KILLED |
| increment 002 code review `BLOCK-UNTIL: F1` (HIGH) | ✅ | `03-increments/increment-002.md` §4b — round 2 verified (`evidence/inc002-red-r2.txt`) |
| increment 003 code review `BLOCK-UNTIL: F1` (HIGH, test-only) | ✅ | `03-increments/increment-003.md` §4b — round 2 verified (`evidence/inc003-f1-red.txt`) |
| security S4-1 (MEDIUM) folded | ✅ | `03-increments/increment-002.md` §4b — CLOSED with boot transcripts at 990/2000/50000 |
| P4 qa G-002 (base AT-407 transcript) and G-007 (UX rows) | ✅ | `04-validation.md` §Orchestrator fold; `evidence/p4-at407-base.txt` |
| increment 004 code review F1 (MEDIUM, test pin) and qa N1–N6 | ✅ | `03-increments/increment-004.md` §4b; `04-validation.md` §Increment 004 re-validation |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| Security S1, the remaining sites (MEDIUM) | done | HLR-401; `03-increments/increment-001.md` |
| Security S2 (LOW) | done | HLR-402; `03-increments/increment-002.md` |
| Titles carry terminal escape sequences (L1) | done | HLR-402 |
| `app.py` notifies ids and exceptions with markup on (S-5) | done | LLR-401.2 |
| `TaskDetails` info grid paints blank | done | HLR-403; `03-increments/increment-003.md` |
| `collapse_runs` can join escaped pieces (S-2) | kept open, reason added | D-405 (its seat is `views.py`) |
| The markup census's residual blind spots (H1, H2, round-1 residuals, S4-4) | added | code review of increment 001; security |
| Ctrl+V through the handler untested (P4 G-001) | added | `04-validation.md` |
| Roster hues may wear alert tones (S4-2) | added | security, P3 |
| Hand-edited data normalised silently (S4-3) | added | security, P3 |
| Setup over an unreadable `team.json` resets its version (S5-1) | added | security, P3 revision 2 |
| Synced phases and project extras unbounded (D-414) | added | `01-requirements.md` |
| `history.jsonl` not cleaned, deep nesting uncaught (D-409) | added | `01-requirements.md`; security note |
| A teammate's task dates untyped | added | code review of increment 002 |
| Unicode format characters pass (S-9) | added | P2 security |
| Details values in the label tone (UX-8) | added | P2 ux |
| Two test names say "escapes" (F5) | added | code review of increment 001 |
| The `team.json` toast wraps on a long path; the 80×24 scrollbar thumb (UXV-3, UXV-2) | added | P4 ux |
| `run_test` hides toasts unless `notifications=True` | added | P4 ux note |
| `.modal-title`'s `margin-bottom` never applies to a Label title inside `.modal` | added | code review of increment 004 (observation) |
| `state.json` `owner` holds the full local path (S7-1) | added | security re-close delta pass |
| Base ref + refresh date | bumped to `56a1b10` · 2026-10-03 | `BACKLOG.md` header |

### Visual decisions — the operator's verdict (2026-10-04, `evidence/operator-verdict-provisional.json`)

| Id | Decision | Captures (before → after) | ux recommendation → operator verdict |
|---|---|---|---|
| PV-1 | the details info grid draws one row per field, no blank row between, long values wrap under the value column; the edit modals' grids untouched (D-406) | `evidence/captures/` base-details-140x40 → after-details-140x40; base-details-80x24 → after-details-80x24; base-details-140x40-long → after-details-140x40-long; base-details-80x24-long → after-details-80x24-long (`.svg` + `.txt`) | accept (`evidence/p4-ux-walkthrough.txt`) → **accepted** |
| UX-3 | a gap under the details title (two blank rows above it, none below, before) | `after-details-*` → `after2-details-*` (both sizes, both name lengths) | accept as a MOVED row → **applied** in increment 004 (TC-420) |
| UX-4 | a narrower label column (10 cells instead of 20) | `after-details-*` → `after2-details-*` | accept → **applied** in increment 004 (TC-421; the long name 2 rows at 80×24) |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-02-batch-04
mode: core
verdict: pass
increments: 4
source_files_max: 3
notices_raised: 31
rework_returns: 7                # P2 iterate-to-refine x2; the P2 stop on S-1; increment 002 F1 and its revisions; increment 003 F1; the TC-418 fixture; the post-close re-open (D-422)
triggers_fired: "B1,B4,C,D,E,F2"
tests_base_to_post: "1855 -> 2218"
new_control: none
open_items_next: 16
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| P2 security HIGH S-1 and the scope / fix form / folds | `02-review.md` iteration 1 | ✅ operator rulings 1–3 at the gate, 2026-10-03 | `spot-check` | the full contract |
| Increment 002 code-review HIGH F1 | `03-increments/increment-002.md` §4b | ✅ operator ruling "Corregir todo en el 002" | `spot-check` | the diff |
| Increment 003 code-review HIGH F1 and the amendment for test-only HIGHs | `03-increments/increment-003.md` §4b | ✅ operator rulings "Sí, corregir y seguir", "Sí, solo para HIGH de pruebas" | `spot-check` | the diff |
| PV-1, UX-3, UX-4 on the captures | `04-validation.md` UX walkthrough | ✅ the operator's verdict, 2026-10-04 (`evidence/operator-verdict-provisional.json`) | `spot-check` | the code |

- **Human perimeter:** the operator (Javier) owns: the look of the `after2-details-*` result; whether the routed security LOWs (S4-2, S4-3, S5-1) and the census residuals are scheduled; the team's trust model for the shared folder (who can write to it); the commit and push.
- **Human review ledger:** human:Javier — 4 decision points reviewed (rulings at the P2 and P3 gates; the visual verdict at P5), 0 rigorous · 0 declared not-reviewed

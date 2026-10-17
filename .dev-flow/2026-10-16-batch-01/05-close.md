# Batch close — taskboard — Batch 2026-10-16-batch-01

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**,
> and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/guides/close-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

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
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 39 notice · 2026-10-17 |
| Gated tree | `82b45e54a7bf9c15fa8db6f027082548ad58a7a2` · dirty — .dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md, .dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md, .dev-flow/BACKLOG.md, .gitattributes, .dev-flow/2026-10-07-batch-05/decisions-log.json, .dev-flow/2026-10-07-batch-06/decisions-log.json, .dev-flow/2026-10-07-batch-06/evidence/gen_verdict_sheet.py, .dev-flow/2026-10-07-batch-06/evidence/kanban-demo.json, .dev-flow/2026-10-07-batch-06/evidence/veredicto-batch06.html, .dev-flow/2026-10-07-batch-06/evidence/veredicto-board.json, .dev-flow/2026-10-07-batch-07/decisions-log.json, .dev-flow/2026-10-07-batch-08/decisions-log.json, .dev-flow/rollover_batchg.py, .dev-flow/rollover_batchh.py, .dev-flow/rollover_batchi.py, .dev-flow/rollover_batchj.py (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` (`artifact_homes.requirements_canon`) — `devflow-init.py --fold-canon`: 10 folded, 0 kept, 0 refused (HLR-1601..1603, LLR-1601.1/.2, LLR-1602.1/.2/.3, LLR-1603.1/.2) |

---

## 1 · What changed

The presenter can now read WHEN each bar is from `R` (a month band with today and the project's due, a tick row naming the selected task's exact dates, a start–end chip on every field row), can leave a task out of the presentation and have it remembered (`space` hides, `a` shows all, "Show in presentation" in the task editor, saved on the task as `show_in_present`, omitted from `board.json` when shown), and `?` shows every key (a full-width column-major Keys band, the palette-only global keys docked outside the scroll). After the operator's verdict on the handoff (2026-10-17) the frame — and so the `x` export — speaks to the room: the tick row reads `selected task ▸` instead of the axis scale, and the ` — hybrid` suffix and the in-frame keys row are gone. Surfaces: `R` → `PresentScreen`; the task editor; `?` → `HelpModal`. Four increments, one lane, on the local branch `present-v2` from `origin/main` `64443be`.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| HLR-1601 · LLR-1601.1 · LLR-1601.2 | v1 + LED .7, .8, .9 | `AT-1601` · `TC-1601`, `TC-1602`, `TC-1608` · `TC-1001`/`TC-1002`/`AT-1001` (PRES-R2) | pass |
| HLR-1602 · LLR-1602.1 · LLR-1602.2 · LLR-1602.3 | v1 + LED .4–.6, .8 | `AT-1602` · `TC-1603`, `TC-1604`, `TC-1605` | pass |
| HLR-1603 · LLR-1603.1 · LLR-1603.2 | v1 + LED .4, .5 | `AT-1603` · `TC-1606`, `TC-1607` | pass |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| — | — | — |

| # | Landing | Done? | SHA / path |
|---|---|---|---|
| 1 | the **command** (`commands/…`) — the rule itself | n/a | no control minted |
| 2 | its **artifact** (a template section) | n/a | no control minted |
| 3 | the **catalog** entry (`dev-flow-lessons`) with its measured origin | n/a | no control minted |
| 4 | **committed and pushed**, manifest re-hashed and bumped | n/a | no control minted |

- **New controls:** none — the one lesson this batch met (regenerating a hashed evidence file in place breaks an earlier packet's digest) is already caught by `V41`, which blocked it at increment 004's gate; the fix was a new file name, not a new control.

---

## 3 · Working-file reconciliation (C-44)

Sweep: `git status --short` and `git log present-v2 --not --remotes` in `C:\Users\jjgh8\Github\taskboard` (the only repository the batch touched). Every commit below sits on the local branch `present-v2`; **none is landed**: the commission forbids a push (PLAN.md `Standing authorization`: «push is NOT authorized»), so landing is owed to the operator.

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py` | ✅ committed on `present-v2`, not pushed (push not authorized) | `ea002aa`, `d30aa8e`, `8cd8dbd` |
| `taskboard/models.py`, `taskboard/app.py` | ✅ committed on `present-v2`, not pushed | `d30aa8e` |
| `taskboard/modals.py` | ✅ committed on `present-v2`, not pushed | `d30aa8e`, `2292e63` |
| `taskboard/keymap.py` | ✅ committed on `present-v2`, not pushed | `2292e63` |
| `tests/test_present_rulers.py` | ✅ committed on `present-v2`, not pushed | `ea002aa` |
| `tests/test_present_hide.py` | ✅ committed on `present-v2`, not pushed | `d30aa8e`, `8cd8dbd` |
| `tests/test_help_keys.py` | ✅ committed on `present-v2`, not pushed | `2292e63` |
| `tests/test_present_room.py` | ✅ committed on `present-v2`, not pushed | `8cd8dbd` |
| `tests/test_present.py` | ✅ committed on `present-v2`, not pushed | `ea002aa`, `8cd8dbd` |
| `.dev-flow/2026-10-16-batch-01/03-increments/*`, `evidence/*` (frames, captures, transcripts, harnesses) | ✅ committed on `present-v2`, not pushed | `ea002aa`, `d30aa8e`, `2292e63`, `8cd8dbd` |
| `.dev-flow/2026-10-16-batch-01/{01-requirements*.md, 04-validation.md, PLAN.md, design/DDR-2026-10-16-batch-01.md}`, `evidence/suite-p4.txt`, `evidence/p4-clipboard-env.txt`, `.dev-flow/state.json`, `REQUIREMENTS.md` | ✅ committed on `present-v2` by the close's deliverable commit (step 6), not pushed | the deliverable commit, the parent of the close commit |
| `.dev-flow/2026-10-16-batch-01/05-close.md`, `.dev-flow/BACKLOG.md` | ✅ committed on `present-v2` by the close commit (step 8), not pushed | the close commit |
| `prototypes/present_rulers/**` | ✅ committed on `present-v2`, not pushed (the approved prototype, frozen evidence) | `ea002aa` |
| untracked `.dev-flow/2026-10-07-batch-0{5..8}/decisions-log.json`, `.dev-flow/2026-10-07-batch-06/evidence/{gen_verdict_sheet.py,kanban-demo.json,veredicto-batch06.html,veredicto-board.json}`, `.dev-flow/rollover_batch{g,h,i,j}.py` | 📋 left on purpose — found before the batch, another session's files, not this batch's to commit or delete | PLAN.md §*Gate notices* "Found before the batch" |

- **Found before the batch:** `.dev-flow/2026-10-07-batch-08/evidence/inc001-brief.md @ a751d73fdcddc239d01f02a2dfcb9ec042222110` `.dev-flow/2026-10-07-batch-09/evidence/inc001-brief.md @ 737b913e5559b8337969790137c4bda87fac2788` `.gitattributes @ 177349380b67f879fc7e21d0841983300b2dba64`

### Conditional-gate discharge

- **Conditional-gate discharge:** 11 condition(s) · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| PDR PC-1..PC-11 (`PDR-2026-10-16-batch-01`, `approved with conditions`) | ✅ each re-read at the DDR at `8cd8dbd` | `design/DDR-2026-10-16-batch-01.md` §B condition table, one row per PC with its test line |
| DDR qa-reviewer F-1 (LLR-1601.2 named the superseded PRES-R frames) | ✅ applied and re-read | `01-requirements.md` LLR-1601.2 threshold names `PRES-R2-*`; ledger LED .9 |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| US-1601, US-1602, US-1603 (present v2: ruler + chips, the hide flag, the `?` keys) | shipped on `present-v2` (`ea002aa`, `d30aa8e`, `2292e63`, `8cd8dbd`), not pushed — no merge SHA: push not authorized | §1, §3 |
| the operator's verdict on the handoff (2026-10-17): the tick label, ` — hybrid`, the in-frame keys row | shipped, increment 004 (`8cd8dbd`); the PLAN's out-of-scope carry closed | PLAN.md §Out-of-scope carries |
| the operator's visual verdict on the 80-column oracle frame | carried (path updated to `PRES-R2-80x24.txt`) | `BACKLOG.md` lane `2026-10-16-batch-01` |
| the 2 pre-existing standup failures | carried, unchanged | same lane |
| `_present_ruler` repeats the gantt ruler layout | carried, unchanged | same lane |
| `selected: no dates` — operator approval | added | same lane; 04-validation G-006 |
| the gantt view's own tick label still shows the scale with a selection | added (operator option) | same lane; increment 004 review F1 |
| `test_win_clipboard_roundtrip` environment failure at P4 | added | same lane; G-001 |
| stale "hybrid"/PRES-R comments and docstrings | added | same lane; G-005 |
| PNG content unasserted; truncated mutant lines | added (optional) | same lane; G-004, G-007 |
| header | refreshed: base `64443be`, last refresh 2026-10-17 (2026-10-16-batch-01 close), status line | `BACKLOG.md` lines 6-8 |
| push of `present-v2`, merge to `main` | owed to the operator (the commission forbids a push) | §3 |

---

## 5 · Batch metrics — the 13 keys of `core`

Extract, do not invent: a key the artifacts did not record goes `null`, and the key is never dropped.

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-16-batch-01
mode: core
verdict: pass
increments: 4
source_files_max: 4              # increment 002 (models, views, app, modals)
notices_raised: null             # PLAN.md declares several NOTICEs as ranges (V31–V34, V36–V38, V41–V51), not one id per line
rework_returns: 1                # P2 iterate-to-refine (iterations_per_station P1 = 1)
triggers_fired: "A2,A3,B1,B4,C8,D1,E1"
tests_base_to_post: "2592 -> 2634"
new_control: none
open_items_next: 8               # the 2026-10-16-batch-01 lane of BACKLOG.md
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| prototype round `prototypes/present_rulers/` (variants, chips, hide flag, legend fix) | prototype renders of the real app | ✅ the operator's verdict, 2026-10-16 | `light` | the code behind the prototype |
| the P3 handoff and the shipped present frame | gates 0 block; captures `app-00{1,2,3}-*` | ✅ the operator's verdict, 2026-10-17 (4 items) | `spot-check` | ⏸ DEFER the operator's visual verdict on the 80-column oracle frame |
| `01-requirements.md` / ledger | P2 review + DDR; `V26` green | ❌ | `none — reviewed by the architect, qa, ux and security agents, not by a human` | |
| Code (`views.py`, `models.py`, `app.py`, `modals.py`, `keymap.py`) | code-reviewer PASS / PASS with notes ×4, 0 HIGH; 31/32 mutants KILLED + 1 declared equivalent | ❌ | `none — agent review only` | not audited line by line |
| `04-validation.md` | qa-reviewer PASS-WITH-NOTES | ❌ | `none` | |
| the increment 004 captures `app-004-*.svg`, `app-004-118x31-present-open.png` | — | ❌ | `none — produced for the operator's review, not yet seen` | |

- **Human perimeter:** the operator owns whether the presentation reads well to a real meeting audience (no user evaluation was done), the approval of `selected: no dates`, the 80-column visual verdict, and the push/merge of `present-v2` (not authorized here).
- **Human review ledger:** human:operator — 2 artifact(s) reviewed, 0 rigorous · 4 declared not-reviewed

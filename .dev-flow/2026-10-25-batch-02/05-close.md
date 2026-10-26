# Batch close — taskboard — Batch 2026-10-25-batch-02

> **Artifact language.** Canonical **English scaffold**; generate in the batch's language — the **prose**, and never a label.

> **Owed in.** `core` ✓ · `full` —

> **Field guide:** `templates/guides/close-template.md` explains each field below and the rules that read it.

> **Reserved field names** (parsed literally, never translated): `Conditional-gate discharge` · `New controls` · `Human perimeter` · `Human review ledger` · `Gated tree` · `Found before the batch` · `⏸ DEFER` · and the §6 DEPTH tokens `light` · `rigorous` · `spot-check` · `none` · `✅` · `❌`.

> **Notice convention.** `⚠` yellow = declare and continue · `✗` red = block · `✓` green = satisfied **with its citation**.

---

## 0 · Gate record — which tree this close gated

| Field | Value |
|---|---|
| Gate record | `python "C:/Users/jjgh8/.claude/skills/dev-flow/scripts/devflow-validate.py" .` from the project root · exit 0 · 0 block · 159 notice · 2026-10-25 |
| Gated tree | `4b409060ad1b11c86e4ee459b9afba291933af1d` · dirty — .dev-flow/BACKLOG.md (the close record itself excluded) |
| Requirements canon | `REQUIREMENTS.md` — 11 ids folded by `--fold-canon` at close (HLR-2901..2905, LLR-2901.1/.2, LLR-2902.1, LLR-2903.1, LLR-2904.1, LLR-2905.1); every id this batch's `01-requirements.md` declares as a heading is a token in it |

---

## 1 · What changed

The operator presenting a board to a room (`R`) now sees the notes' highlights coloured on every
presentation surface: the gantt view's cursor note (view 1), the split view's note blocks (view 2),
and their `x` SVG/PNG exports paint `==…==` yellow (`soon`), `!!…!!` rose (`over`), `++…++` green —
markers dropped, unmarked text in the presentation's own bright `ink`, a mention inside any span
bold pink, a highlighted span keeping its tone across a wrapped row, and nothing else changed (no
layout, keys, hints, cut wording or other view). The mechanism: the note pipeline tokenises with the
one `highlight_segments` before wrapping (the wrap measures the marker-free text) and carries
`(lead, [(segment, tone)])` rows to a tone-aware `_paint_marks`; the export renders the same
composed frame it always did.

| Requirement | Version | Verified by | Verdict |
|---|---|---|---|
| `HLR-2901` | v1 | `AT-2901` · layer-0 arms | pass (gate chunk02; the P1 RED probe at base_ref) |
| `HLR-2902` | v1 | `AT-2902` (118x30 + 80x24) · `test_L0_marker_free_twin_wraps_identically` | pass |
| `HLR-2903` | v1 | `AT-2903` (the emitted SVG bytes) | pass |
| `HLR-2904` | v1 | `AT-2904` (mention / unclosed marker / bullets / hostile payload) | pass |
| `HLR-2905` | v1 | `AT-2905` + the P4 3-chunk gate | pass (3278 = 3258 + 20) |
| `LLR-2901.1` | v1 | layer-0 + the reverse census | pass |
| `LLR-2901.2` | v1 | the hostile arm + mutation arm d2 | pass |
| `LLR-2902.1` | v1 | the wrap fixture + the twin arm | pass |
| `LLR-2903.1` | v1 | inspection (empty diff) + `AT-2903` | pass |
| `LLR-2904.1` | v1 | the mention arm + mutation arm d1 | pass |
| `LLR-2905.1` | v1 | the diff census | pass |

---

## 2 · New controls discovered — and where they landed (C-45)

| Control | What failure it closes | Measured origin |
|---|---|---|
| none — no new control minted. The batch's one genuinely new lesson (a matcher that re-attributes wrapped rows must take its whitespace test from the WRAPPER's notion — `str.isspace()` against textwrap's drop, not an ASCII set — or legal NBSP text crashes the render) is a code-review catch inside this batch's own battery, not a reusable flow control; the F1 arm now pins it in the suite. | — | — |

**The four landings:** none — no new control.

- **New controls:** none — the reason above.

---

## 3 · Working-file reconciliation (C-44)

| File | State | Evidence |
|---|---|---|
| `taskboard/views.py` | ✅ committed — lands on the local branch `fix/present-note-highlights`; push/merge NOT granted by the commission («Do NOT push or merge»), the operator owns the landing | the deliverable commit |
| `tests/test_present_note_highlights.py` (new) + `tests/test_present_views.py` + `tests/test_people_look.py` | ✅ committed — same branch | the deliverable commit |
| `REQUIREMENTS.md` (canon fold, 11 rows) | ✅ committed — same branch | the deliverable commit |
| `.dev-flow/` batch record + evidence (incl. the 4 capture PNGs) | ✅ committed — same branch | the deliverable commit |
| `.scratch/` (the rollover/take-up scripts, the impl spec, the mutation battery) | 🗑️ deliberately deleted at close — git-excluded scratch | `git status` clean of it at the close gate |

- **Found before the batch:** `none — no tracked file was modified when the batch began` (init printed `found: none`)

### Conditional-gate discharge

- **Conditional-gate discharge:** 3 conditions · ✅ all discharged

| Condition | Discharged? | The artifact line that proves it |
|---|---|---|
| DDR COND-1 — the packet's signed-balance line | ✅ | folded at seal — `increment-001.md` §4 reads `base 200 − deleted 0 + added 20 = post 220` with the 16 named as the correction population |
| DDR COND-2 — the Q5 baseline reconciliation | ✅ | `04-validation.md` §✅ Verdict «Baseline reconciliation» + the second signed-ledger row: affected suites 200 (base_ref) = 200 (post), Δ0; the full-suite reconciliation 3258 + 20 = 3278 executed |
| DDR UX-1 — the painted contrast evidence | ✅ | `04-validation.md` §UX walkthrough: the four `n01-` captures, each READY gate asserting the three tone hexes + zero marker runs on the live composited frame, ≥ 8 colours, the no-leftover assertion |

---

## 4 · Backlog reconciliation — the carry-over contract

| Item | Move | Reference |
|---|---|---|
| BACKLOG item 4 — the presentation draws the notes' markers raw | **done** — marked in place in the people-round section | `01-requirements.md` US-2901 · this close |
| this batch's QA-P4-01..05 | folded in `04-validation.md`; nothing carries | the validation record |
| the operator's remaining ordered items (1–3, 5+ of the people round and the older carries) | stay open in their sections | `.dev-flow/BACKLOG.md` |

---

## 5 · Batch metrics — the 13 keys of `core`

```yaml
type: dev-flow-batch
project: taskboard
batch_id: 2026-10-25-batch-02
mode: core
verdict: pass
increments: 1
source_files_max: 1
notices_raised: 5            # V27, V30, V40, V53, V57 — declared in PLAN.md §Gate notices and runtime absences
rework_returns: 2            # P2 round 1 and round 2 both returned iterate-to-refine (3 majors, then 1 major + 3 minors); round 3 verified
triggers_fired: "B1,C8,D1"
tests_base_to_post: "3258 -> 3278"   # +20 new nodes; the clipboard arm TC-1902 ran and passed (0 skips), named in 04-validation
new_control: none
open_items_next: 0           # no new carries; the prior queue stands in BACKLOG.md untouched
```

---

## 6 · Human review ledger — what a human audited, at what depth

| Artifact | Machine verdict (citation) | Human review | Depth | Deliberately NOT reviewed |
|---|---|---|---|---|
| `01-requirements.md` + ledger | gate `V26` green at every gate · scan flags answered in §6.3 | ❌ | `none — the contract was reviewed by three independent lens agents at P2 (three rounds) and the architect at the PDR` | |
| Test cases / ATs | the mutation battery: 6 arms KILLED twice (the second against the shipped bytes), per-arm verdicts, restore hashes | ❌ | `none — the code-reviewer and the DDR's qa lens audited the oracles` | |
| Evidence bytes | `V41` — every cited digest re-hashes; the P4 qa lens re-derived the packet digests | ❌ | `none` | |
| Code | gates + `code-reviewer` OK-TO-ADVANCE after the F1 discharge, 0 HIGH | ❌ | `none — the diff is confined to the note pipeline beside a byte-identical frozen set` | |
| The four capture PNGs | scripted content checks (tones + no marker runs on the live frame at capture time) + colour/byte floors | ❌ | `none — a human eyeball of all four PNGs agreed with the script (recorded in the captures README)` | |

- **Human perimeter:** the operator owns what this flow does not cover: the merge/push decision (NOT granted — nothing is pushed), the disposition of the remaining backlog queue, and any evaluation with users (none exist outside the one-person team — the ux lens's declared answer).
- **Human review ledger:** `none — every review in this batch was an independent sub-agent lens carrying the flow's role files (12 reviewer agents in all: 3 at P2 round 1, 1 re-review at round 2, 1 verification at round 3, 1 at the PDR, 1 code-review + 1 re-read, 2 at the DDR, 1 at P4 — plus the spawned implementer and two amendment/revision agents); no human read the artifacts at a gate. The operator's reconstruction path is the decisions_log + this record.`

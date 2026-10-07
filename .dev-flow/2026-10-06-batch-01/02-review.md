# Review — taskboard — Batch 2026-10-06-batch-01

> Phase 2 (P2) — the four lenses over `01-requirements.md`. Reviewers spawned as generic
> sub-agents, each carrying its role file from the flow's `agents/` (the runtime has no named
> roles; SKILL.md §*What refuses an invocation here* step 5's discipline).

## ✅ Verdict (read first) — iteration 1

**FAIL — iterate-to-refine to P1.** qa-reviewer FAIL (blocker Q-1) · architect FAIL (blockers
A-1, A-2) · security-reviewer FAIL (HIGH S-1, S-2) · ux-reviewer FAIL (blocker UX-1). Two
defects account for every blocker, each proved by EXECUTING the prototype engine on the
contract's own fixture:

1. **The AT thresholds were predicted, not executed** (Q-1/A-1/S-1/UX-1): `+` on `tm2` moves
   `tm3` AND `tm4` (tm4's own pre-existing 3d overlap on tm3 grows), not "tm3 and no other
   task"; AT-608's together arm had no mode discriminator (`tm5` moves only under `together`).
2. **The "ONE measure" claim was false on disk for milestone waiters** (Q-3/A-2/S-2/UX-2): the
   shipped `link_overlap` has no milestone arm, so it disagrees with the prototype's carve-out
   by 1d exactly where the screen paints — and AT-610's flag arm could not go RED.

## Detail

### Findings and dispositions (iteration 1)

| Id | Severity | Finding (one line) | Disposition |
|---|---|---|---|
| Q-1/A-1/S-1/UX-1 | blocker ×4 | AT-607/608/609 moved-sets contradict the executed engine | **folded**: every arm's moved-set executed on the exact AT board (`evidence/p1_thresholds.py` → `p1-thresholds.txt`); thresholds rewritten to the executed numbers (tm3 AND tm4; the tm5 discriminator under together; the editor's +3/+3/+3) |
| Q-2 | major | AT-608/609 moved-sets incomplete; no discriminator | folded with Q-1 |
| Q-3/A-2/S-2/UX-2 | blocker/major ×4 | the ONE-measure claim false for milestone waiters; the flag arm vacuous | **folded as D-633**: the ONE measure IS the shipped `link_overlap` applied to planned dates; the prototype's carve-out dropped (redundant under start==due; moved sets identical — the constant cancels in the delta); §1.3 rewritten; the flag arm now asserts the toast's `flagged` clause with the ADDED days, not the glyph (lit at base) |
| A-3 | major | the undated-task base is new engine behavior | **folded**: LLR-604.1 states the today base (the bump's own rule); TC-627 pins it |
| A-4/UX-3 | major | toast grammar must NAME the moved tasks (the approved C-3 frame) | **folded**: LLR-604.2 adopts the prototype's ladder verbatim — names when they fit, count when not, mixed shifts spelled, the project clause, the narrowing key suffix |
| Q-5/UX-4 | minor | `flagged` was a phantom literal | **folded**: the flag toast clause (`flagged ‹names› +‹N›d`, added days) specified in LLR-604.2 and asserted in AT-608/AT-610 |
| UX-5 | minor | the key suffix and `m`'s Key entry unpinned | **folded**: `· u undo · m change for this move` → `m change` → `m` (the C-3 ladder); `Key("m", "m", "cascade_mode", "Chain", group="date")` pinned in §1.6 and LLR-604.4 |
| UX-6 | minor | the refusal literal unspecified | **folded**: `m re-applies the last date move — nothing to re-apply`, asserted verbatim in AT-608 |
| A-5/UX-7 | minor | the flag surface's view unpinned; read the painted frame (C-32) | **folded**: the persistent flag is the gantt gutter; §5's capture list gains the `↳` gutter frame; the AT reads the toast (the glyph is lit at base under the shipped measure) |
| S-3 | MEDIUM | §6.3's "atomic save" claim false (`save()` is a plain write_text) | **folded as D-634**: a cascade touching >1 task saves through `save_atomic()`; §6.3 states the session-only undo boundary |
| S-4 | LOW | "local-only" overstates: a NEW synced project imports `date_links` whole | **folded**: D-630 and P-6 amended to name the new-project path; read leniently, never written back by sync |
| S-5 | LOW | "nothing file-derived is parsed" a false absolute | **folded**: §6.3 reworded — the control is `markup=False` + `clip()` + lenient parsing |
| Q-6 | minor | RC-1(b) cited an evidence file that did not hold the output | **folded**: the executed `git grep` output appended to `p0-probes.txt`; the citation corrected |
| A-6 | minor | P-1's empty probe body; `· m` suffix missing from §1.6 | **folded**: command + empty output pasted in `p1-premises.txt`; §1.6 carries the toast template, the project clause and the full suffix ladder |
| UX-⚠ D-627 | notice | the setting re-sited from the approved chain map to the project editor | **declared**: D-627 now names the re-siting and flags it for the P4 visual verdict |
| UX-⚠ latency | notice | no slow-state line | **folded**: §2.4 — local JSON, no slow state |

### shall / should check

Clean — `shall` only inside HLR/LLR statements (checked both iterations).

### Two-layer acceptance review (blockers)

Iteration 1's blockers were exactly this layer: acceptance thresholds that contradicted the
executed engine. Iteration 2's thresholds are executed (`p1-thresholds.txt`), one node per AT
(C-18), every AT driving the real app with real keys (C-16).

### Supersession census (change-first)

Touched symbols with tests belonging to earlier requirements (B1): `bump_due`
(test_milestones, test_momentum), `open_predecessors`/`depends_on` readers (11 test files),
`_on_task_edited` (test_edit_window, test_app), `action_undo` (test_app), `ProjectModal` /
`ProjectPicker` (test_app), KEYMAP (11 files). `link_overlap` is READ, not edited (D-633) — the
engine calls it; its own tests (`test_links.py:171`) keep their meaning. Re-validated per
increment.

### Security review summary

Iteration 1: 2 HIGH (S-1, S-2 — both the shared contract defects), 1 MEDIUM (S-3), 2 LOW (S-4,
S-5). All folded (D-633, D-634, amended D-630, §6.3). No new external surface; the write path
is the shipped atomic save; untrusted text follows S1.

### Evidence checklists — architect · qa-reviewer · security-reviewer · ux-reviewer

Each reviewer verified every seat against disk and executed the decisive probes (the engine on
the contract's own fixture). Their checklists are summarized by the findings table above; the
orchestrator's fold is `p1_thresholds.py` / `p1-thresholds.txt` and the iteration-2 contract.

## ✅ Verdict — iteration 2 (the same four lenses re-read the delta)

**FAIL — iterate-to-refine to P1.** qa-reviewer PASS-WITH-NOTES (0 blocker; Q-7 major, Q-8
minor) · architect FAIL (A-7, A-8 blockers) · security-reviewer FAIL (S-6, S-7 HIGH) ·
ux-reviewer FAIL (UX-8 major). The iteration-1 folds all verified REAL (thresholds re-executed
byte-identical; D-634/D-630/§6.3 confirmed on disk). The new defect class: the iteration-2
toast literals were pinned without executing the toast ladder — `pushed Add push, Offline +1d
each` and `Data Warehouse +2d past ◆` match nothing the adopted C-3 ladder produces at 118
columns (executed by two lenses independently). Plus one falsified proof: D-633's "the constant
cancels in the delta" fails at a milestone waiter's slack boundary (three lenses, executed).

### Findings and dispositions (iteration 2)

| Id | Severity | Finding | Disposition |
|---|---|---|---|
| A-7/S-6 (sec) | blocker/HIGH | AT-607's toast literal not produced by the ladder at 118 | **folded**: the ladder executed (`p2_arch_probe.py`); the literal corrected to `pushed Add push, Offline sync +1d each` (`_short_title(·,12)` keeps "Offline sync"); the ladder rule defined in §1.3 and pinned in LLR-604.2 |
| A-8/S-7/UX-8 | blocker/HIGH/major | the project-clause literals match no single rule ("Mobile" vs "Data Warehouse") | **folded**: the rule is the ladder's — full name when it fits, FIRST WORD otherwise; AT-610 corrected to `Data +2d past ◆`, AT-608's `Mobile +1d past ◆` stands (first word of "Mobile App") |
| A-9/Q-7/S-8 (sec) | major | "the constant cancels in the delta" false at the slack boundary (executed) | **folded**: D-633/§1.3 re-worded — the choice stands on the screen, not the algebra; TC-628 pins the boundary (milestone waiter 1d slack, pred +1 → milestone +1; RED against the carve-out) |
| A-10 | major | the toast fitting rule existed nowhere; AT-607's 80-col arm had no expectation | **folded**: §1.3 defines the ladder (rungs, `_short_title(·,12)`, full/first-word project, narrowing suffix); the 80-col expectation pinned (`pushed 2 +1d each`) |
| A-11 | major | the flag clause is not in the C-3 ladder; its grammar unspecified; the AT-610 substring vacuous (`+2d` is already in the lead) | **folded**: the clause specified (names from the worsened overlaps, ADDED days, count fallback); the pinned substrings are the full clause (`flagged Revenue +2d`), not the bare number |
| Q-8/S-10 (sec) | minor/LOW | `new_conflicts`: contract says ADDED, the prototype carries totals | **folded**: LLR-604.1 states `ov_new − ov_old`, deliberately; §5 notes AT-610's flag total is 3 (1 pre-existing + 2 added) |
| A-12/UX-9 | minor | the refusal literal and the flag template missing from §1.6 | **folded**: both rows added |
| A-13 | minor | AT-610's "(editor or `+` twice)" — `+` moves the due only | **folded**: AT-610 pins the editor; the alternative dropped |
| A-14/S-9 | note/LOW | §5's `td0<td4` 1d cited evidence that didn't list it | **folded**: the shipped-measure listing appended to `p1-thresholds.txt` (executed) |
| A-15 | note | the project clause names only the moved task's project | **folded**: stated in LLR-604.2 |
| ux-S-6 | minor | the atomic-save rule didn't cover the undo's restore | **folded**: D-634 extended to the restore |
| ux ⚠ notices | notice | mislabeled probe arm; the §6.3 citation | **folded**: the control arm relabeled in `p1_thresholds.py` (evidence regenerated); the citation corrected to `app.py:1014` |

### Iteration-2 verdicts, recorded

- qa-reviewer: PASS-WITH-NOTES — every iteration-1 blocker fold real and executed; Q-7 (major)
  and Q-8 (minor) folded above.
- architect: FAIL — A-7, A-8 blockers (executed); A-9..A-11 majors; A-12..A-15 minors/notes.
- security-reviewer: FAIL — S-6, S-7 HIGH (executed); S-8..S-11 LOW.
- ux-reviewer: FAIL — UX-8 major; A-7, S-6, UX-9 minors; notices declared (the D-627 re-siting
  stays carried to the P4 visual verdict; no user evaluation — one-person team).

## ✅ Verdict — iteration 3 (the four lenses re-read the delta, LED .3)

**qa FAIL (Q-9 major) · architect PASS-WITH-NOTES (A-16 = Q-9; A-17, A-18) · security
PASS-WITH-NOTES (S-12, S-13) · ux PASS-WITH-NOTES (UX-10, UX-11) → iterate-to-refine to P1.**

Every iteration-2 fold verified REAL (all four lenses re-executed the probe; the corrected
literals reproduce byte-for-byte; D-633/TC-628 executed; D-634's restore extension on disk).
One fold-introduced defect: §1.3's ladder gloss fixed the name budget at 12 while the adopted
ladder narrows 12 → 8 — and AT-608's @118 toast lands on the 8-rung, so a P3 written from the
gloss flips the pinned `Mobile +1d past ◆` to RED (proved by execution, two lenses).

### Findings and dispositions (iteration 3)

| Id | Severity | Finding | Disposition |
|---|---|---|---|
| Q-9/A-16 | major | §1.3's ladder gloss fixed the name budget at 12; the adopted ladder narrows 12 → 8 (the 8-rung is load-bearing) | **folded**: §1.3 states the narrowing and why it is load-bearing |
| Q-10/A-18 | minor | the flag clause's count and mixed forms unspecified | **folded**: both forms pinned in §1.6 and LLR-604.2 (`flagged 2 +2d each`; `flagged 2 overlaps (‹A› +1d, ‹B› +3d)`) |
| Q-11/A-17/UX-10/S-12 | minor/LOW | the probe's self-check block still pinned the iteration-2 literals and printed FAIL | **folded**: checks corrected to the iteration-3 literals; transcripts captured (`p2-arch-probe.txt`, 4 PASS; `p2-arch-probe2.txt`) |
| S-13 | LOW | P-9 overclaimed ("toast strings executed") for the two NEW strings | **folded**: P-9 scoped — components executed, derivation stated |
| UX-11 | minor | (a) no probe transcripts (b) §5 didn't disambiguate AT-608's totals (c) §1.3's agreement claim sat next to probe2's `conflicts identical: False` | **folded**: (a) transcripts captured; (b) the parenthetical added; (c) the claim scoped to moved sets and added deltas |

### Iteration-3 verdicts, recorded

- qa-reviewer: FAIL — Q-9 major (executed), Q-10 minor, Q-11 note.
- architect: PASS-WITH-NOTES — A-16 major (advised folding before P3), A-17, A-18 minors.
- security-reviewer: PASS-WITH-NOTES — S-12, S-13 LOW (evidence hygiene).
- ux-reviewer: PASS-WITH-NOTES — UX-10, UX-11 minors; the D-627 re-siting stays carried to P4.

## ✅ Verdict — iteration 4 (the four lenses re-read the one-sentence delta, LED .4)

**PASS — P2 approved.** qa-reviewer PASS-WITH-NOTES (0 defect; Q-12 note) · architect
PASS-WITH-NOTES (0 finding) · security-reviewer PASS-WITH-NOTES (S-14, S-15 LOW, hygiene) ·
ux-reviewer PASS-WITH-NOTES (0 finding). The 8-rung narrowing verified by re-run (4 PASS,
byte-identical transcript); every iteration-3 finding folded REAL.

**Gate folds (the minors, discharged at the gate per the standing authorization):**
- Q-12 (note): the lead-title clip named in §1.3's ladder bullet.
- S-14 (LOW): `sys.stdout.reconfigure(encoding="utf-8")` at `p2_arch_probe.py`'s top (the probe
  crashed a stock cp1252 console); re-run still 4 PASS.
- S-15 (LOW): LLR-604.2's flag clause now notes the prototype transcript's `flagged 0
  dependents ()` is a degenerate artifact, not the grammar.

**Carried, not folded:** the D-627 re-siting (setting in the project editor, not the approved
C-2 chain map) — the P4 visual verdict's own question; the two NEW toast strings stand on
scoped P-9 (components executed, derivation stated) and P4 executes them.

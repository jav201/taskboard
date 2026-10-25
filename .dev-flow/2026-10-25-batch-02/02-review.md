# Review — taskboard — Batch 2026-10-25-batch-02

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read them. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `iterate-to-refine` → Phase 1 (rounds 1 and 2 folded by amendment; round 3 verified the R2 folds (architect lens: LED-2905.1 reciprocal, contract folds landed, V26 pairs clean, no stale contradiction) — PASS, the gate approves)
- **Out-of-scope findings:** `none` named and routed below

- **Findings:** `0` blocker · `4` major · `15` minor (rounds 1+2 cumulative)
- **shall/should check:** ✓ clean  /  ✗ misuse (blocker)
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete · ATs are genuinely black-box  /  ✗ `<none>`
- **Census (change-first):** done — best-effort + gate-confirmed  /  ⚠ incomplete   (NEVER stamp "VERIFIED COMPLETE")
- **Security:** ✓ no findings  /  ⚠ `5` findings (all minors, all folded)
- **Evidence checklists (architect / qa / security):** ✓ all complete  /  ✗ `<missing>`

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

### Review setup

- **Batch:** `2026-10-25-batch-02` · **Input:** `01-requirements.md` (P1, iteration 1 after amendment)
- **Lenses:** `architect` + `qa-reviewer` + `security-reviewer` (trigger family C fired — C8), all spawned as independent generic sub-agents carrying the bundle's `agents/<role>.md`.
- **Rounds:** round 1 on the original contract; round 2 on the amended contract (both recorded below); round 3 verified the R2 folds (architect lens: LED-2905.1 reciprocal, contract folds landed, V26 pairs clean, no stale contradiction) — PASS, the gate approves.

### Findings (round 1)

| ID | Lens | Severity | Requirement | file:line | Finding (one line) | Disposition |
|----|----------|----------|------------|-----------|--------------------|-------------|
| A1 | architect | major | IFC Part A | 01-requirements.md:319 | The IFC FLOW omits `_paint_marks`, a symbol the fix changes — a P3 reverse census keyed on Part A would miss it. | folded-in-LED-2901 |
| A2 | architect | major | LLR-2901.1, LLR-2902.1 | 01-requirements.md:250, 272 | C-26 asks each changing LLR to declare its touched symbols; the LLRs named only symbols that stay unchanged. | folded-in-LED-2901 |
| A3 | qa-reviewer | minor | §1.3 definitions | 01-requirements.md:49 | The word "rose" collides with the HEX key `rose` = `#fb7185`, a different colour — never key assertions on the word. | folded-in-LED-2901.3 |
| Q1 | qa-reviewer | major | HLR-2905 | 01-requirements.md:228 | The known-in-advance oracle casualty is not named: `tests/people_round_fixture.py` holds `++sign-off by the sponsor++` in task c5's notes and `tests/test_people_look.py:182-186` asserts the split frame's `.plain`. | folded-in-LED-2905 |
| Q2 | qa-reviewer | minor | HLR-2903 | 01-requirements.md:196 | The statement promises PNG parity the threshold never asserts — PNG rendering is Edge-dependent. | folded-in-LED-2903 |
| Q3 | qa-reviewer | minor | HLR-2901 | 01-requirements.md:168 | "Marker characters (`=`, `!`, `+` in marker positions)" is not a mechanical predicate. | folded-in-LED-2901.3 |
| Q4 | qa-reviewer | minor | HLR-2904 | 01-requirements.md:223 | Two of AT-2904's three arms hold at `base_ref` by design — the negative control must say which arm has an executed P1 red. | folded-in-LED-2901.3 |
| Q5 | qa-reviewer | minor | HLR-2905 | 01-requirements.md:232 | "3258 + new-node count" holds a P3-minted unknown and the baseline is asserted from the commission, not re-executed — the exact integer must be pinned in `04-validation.md` from an executed pre-increment 3-chunk run. | folded-in-LED-2905 |
| Q6 | qa-reviewer | minor | HLR-2902 | 01-requirements.md:191 | The evidence paraphrase said `word ==tail==`; the bytes in `evidence/red-p1.txt` probe 4 say `word word ==tail==`. | folded-in-LED-2901.3 |
| Q7 | qa-reviewer | minor | HLR-2905 | 01-requirements.md:232 | The existing byte oracles compare `text.plain` only — a style-only regression such as `ink`→`mut` on marker-free rows stays green. | folded-in-LED-2905 |
| S1 | security-reviewer | minor | LLR-2901.2 | 01-requirements.md:261 | The `k == 1` cut path of `_present_cut` composes plain text today — the seat where the escape could be dropped is unnamed. | folded-in-LED-2901.2 |
| S2 | security-reviewer | minor | LLR-2901.2 | 01-requirements.md:264 | The hostile payload set lacks the unbalanced close tag `[/]`, which raises `MarkupError` unescaped. | folded-in-LED-2901.2 |
| S3 | security-reviewer | minor | LLR-2901.2 | 01-requirements.md:265 | The ANSI payload's fate is unasserted — Textual strips `\x1b` before render, but no threshold pins it. | folded-in-LED-2901.2 |
| S4 | security-reviewer | minor | HLR-2903 / AT-2903 | 01-requirements.md:200 | The SVG sink's HTML-escaping is inherited analysis, not evidence — no assertion on the emitted bytes. | folded-in-LED-2903 |
| S5 | security-reviewer | minor | §6.3 | 01-requirements.md:368 | §6.3 claims "Residual risk: none open" while the C-17 control's hostile arms are still P3-minted, not executed. | folded-in-LED-2901.2 |

Round-1 dispositions summary: 0 blockers; majors A1, A2, Q1 folded by the P1 amendment (iterate-to-refine route, ledger entries LED-2901, LED-2901.2, LED-2901.3, LED-2903, LED-2905); all minors folded the same way. The `file:line` column cites the amended contract (post-fold) for traceability; each finding was raised against the round-1 original at the same location. Route to date: two `iterate-to-refine` rounds so far; round 3 (verification of the R2 folds) is owed next.

Round 2 — see the Findings (round 2) subsection below.

### Findings (round 2 — architect re-review of the amended contract)

Round-2 verdict: `iterate-to-refine` — 1 major (R2-1) + 3 minors, all folded (R2-1 via the new ledger entry LED-2905.1; the minors in place).

| ID | Lens | Severity | Requirement | file:line | Finding (one line) | Disposition |
|----|----------|----------|------------|-----------|--------------------|-------------|
| R2-1 | architect | major | HLR-2905 / LED-2905 | 01-requirements.md:228 | LED-2905's named oracle casualty is wrong twice: `++sign-off by the sponsor++` is task c7's note (`N_EVAL`), not c5's (`N_GOLDEN` holds `!!12 questions still have no answer key!!`), and `tests/test_people_look.py:182-186` asserts mention membership, not marker bytes — it stays green; no test asserts any marker string. | folded-in-LED-2905.1 |
| R2-2 | architect | minor | HLR-2903 | 01-requirements.md:206 | Boundary catalog used `☑` and duplicated the empty entry — the convention is `☐` for every class with the checked content inside the text. | folded in place |
| R2-3 | architect | minor | LLR-2903.1 | 01-requirements.md:287 | Numeric pass threshold paraphrases AT-2903 stale — it omits the amended numbers (0 raw `<script` bytes) and the inspection arm (empty export diff). | folded in place |
| R2-4 | architect | minor | HLR-2901 | 01-requirements.md:171 | Observable outcome still keys on the word "rose" ("yellow, rose and green") — the HEX-key collision A3 removed from §1.3 survives in the acceptance prose. | folded in place |

Round-1 fold status at round 2: A1/A2 verified in the amended contract (the IFC `_paint_marks` node is present with its owners; the C-26 symbol declarations sit on LLR-2901.1/LLR-2902.1); A3, Q2, Q4, Q6 folded; Q1's fold itself was corrected by R2-1 — the casualty it named exists on neither count, so LED-2905.1 replaces the claim with the grep-verified absence and owes the casualty list to the P3 census + suite run.

### shall / should check

✓ clean — every HLR/LLR statement reads `shall`; no modal `should`/`debería` inside any statement (the acceptance prose's normatives are out of statement scope).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2901 → AT-2901..AT-2905 → HLR-2901..HLR-2905 → LLR-2901.1..LLR-2905.1 | yes | yes | yes | yes | ✓ |

(a) ✓ every story has a black-box `AT` — US-2901 names AT-2901..AT-2905, one node per the commission.
(b) ✓ every output-producing requirement names its observable deliverable + observation method — HLR-2903 names the SVG file bytes (`reports/present-*-split-*.svg`); HLR-2905 names the P4 suite counts.
(c) ✓ both chains complete — behavioral US-2901 → AT-2901..AT-2905 → observable outcomes (§2.6, acceptance blocks); functional US-2901 → HLR-2901..2905 → LLR-2901.1..2905.1 → TC/inspection arms.
(d) ✓ each `AT` is genuinely black-box — the acceptance limbs drive the `R` screen by keys at 118x30/80x24 and assert painted styles / emitted SVG bytes, referencing no internal symbol.

### Supersession census (change-first)

B1 fired — the crossed reverse census commands for P3 are declared here as owed, keyed on the batch's edited symbols:
- `grep -rl highlight_segments tests/`
- `grep -rl present_note_lines tests/`
- `grep -rl _present_cut tests/`
- `grep -rl _paint_marks tests/`

Best-effort at P2/P3 + gate-confirmed at the increment gate; never "VERIFIED COMPLETE" from this station. Planned source set: `taskboard/views.py` alone (+ tests uncapped); the census above is the completeness guarantee's input, not its verdict.

### Security review summary

Family C fired (C8 — the increment widens what is parsed into markup over file-derived note text), so the security lens ran. The Phase-1 scan's flags are answered in §6.3 of the amended contract: `role` → §2.3 (no auth surface exists or changes); `form` → §1.5/§2.7 prose matches (a Textual screen, not a web form); `escape` → LLR-2901.2's own subject, answered BY a requirement. Five minor findings (S1–S5), all folded into the contract via LED-2901.2 and LED-2903. The C-17 control's hostile-arm execution is owed at P3 — no ship verdict before it and before its mutation-battery kills.

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer

- **Architect** — ✓ contract structure and IFC read against the field guide; ✓ trace chains walked both directions (no orphan HLR/LLR/AT); ✓ IFC Part A node/owner pairs re-checked after the A1 fold (`_paint_marks` node present, owners LLR-2901.1/LLR-2901.2); ✓ C-26 symbol declarations present on LLR-2901.1/LLR-2902.1.
- **QA-reviewer** — ✓ every Numeric pass threshold is an executable predicate (post-Q3/Q7 folds); ✓ negative controls name their RED side per arm (post-Q4 fold); ✓ evidence quotes match `evidence/red-p1.txt` bytes (post-Q6 fold); ✓ the named oracle casualty and the baseline-integer pin are in HLR-2905.
- **Security-reviewer** — ✓ scan flags (`role`, `form`, `escape`) traced and answered in §6.3; ✓ escape seats named (`_paint_marks` span-by-span, the `k == 1` cut path); ✓ hostile payloads include Rich brackets, ANSI bytes, a link tag and the unbalanced `[/]`; ✓ ANSI fate pinned (0 `\x1b` bytes, restatement path declared); ✓ SVG escape assertion added to AT-2903; ✓ §6.3 residual risk now states the owed execution.

### Verdict

`iterate-to-refine` (rounds 1 and 2) — the gate tokens' home is `templates/review-template.md`. Both amendments are folded (ledger entries LED-2901, LED-2901.2, LED-2901.3, LED-2903, LED-2905, LED-2905.1); round 3 verified the R2 folds (architect lens: LED-2905.1 reciprocal, contract folds landed, V26 pairs clean, no stale contradiction) — PASS, the gate approves.

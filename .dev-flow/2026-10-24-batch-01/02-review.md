# Review — taskboard — Batch 2026-10-24-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — four lenses over three iterations; the last pass: architect, security-reviewer and ux-reviewer `approve` clean, qa-reviewer `approve` after verifying the QA-4 fold (LED .45). The requirement-defect majors (ARCH-1 the `:2433` project-span due mark misfiled as a seat site; ARCH-2 the `find` semantics contradicting the round's prefix rule; SEC-1 the load validation omitting `colour`/types; UX-1 the unsatisfiable empty-catalog claim; QA-4 the `SHAPES`/`◆` membership contradiction) and every minor were folded into the contract as LED-2026-10-24-batch-01.26–.45 the same day → Phase 3 through the PDR
- **Out-of-scope findings:** none — every finding was folded or is record-only (QA-5: an arithmetic slip in LED .38's evidence prose, append-only ledger, no normative weight)
- **Findings:** 0 blocker · 5 major (ARCH-1, ARCH-2, SEC-1, UX-1, QA-4) · 22 minor
- **shall/should check:** ✓ clean (every normative `shall` inside an HLR/LLR Statement; zero `should` in the document)
- **Two-layer (blockers):** ✓ every story has an `AT` (AT-2601..2607 = the commission's AT-a..AT-g) · output reqs name deliverable+observation (the styled-segment export oracle of §5.1 for tone claims, the `m01-` captures as visual confirmation) · both trace chains complete (4 US → 8 HLR → 17 LLR; ledger 45 entries paired both ways) · ATs are genuinely black-box (two recorded exceptions: AT-2602's file-as-surface two-window proxy, LED .36; style assertions via the §5.1 oracle)
- **Census (change-first):** done — best-effort + gate-confirmed (PLAN.md §Triggers B1; each increment's packet repeats the reverse census)
- **Security:** ⚠ 1 major (SEC-1, folded: load-time validation of `colour ∈ COLOURS`, field types, `hidden` coercion, with TC arms) + 4 minors (SEC-2..SEC-5, folded); the security-reviewer re-checks `marks.py` at increment 001's gate (§6.3); no new external surface, so no scope-change re-route fired
- **Evidence checklists (architect / qa / security):** ✓ all complete (in the reviewers' returns; ux-reviewer too)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C6, C8 fired; C3, C4 not) — each spawned as a sub-agent with its `agents/<role>.md` role, read-only, in parallel, 2026-10-24, over the contract and ledger. **Three iterations.** Pass 1: architect and security-reviewer returned requirement-defect majors → the contract was amended (LED .26–.36) and the full P2 review re-ran (pass 2), which caught the ARCH-1 fold half-landed at three downstream consumers (the "three notices" of AT-2603's threshold, the "(21 sites)" count, the shipped surface's "slip") → second amendment (LED .37–.44) and a confirmation pass (pass 3); qa-reviewer named QA-4 (the LED .40 SHAPES fold landing in LLR-2601.1 only) → third one-line-two-cell amendment (LED .45) and the qa-reviewer re-verified: APPROVE. Every other fold of every pass was verified LANDED by the next pass. The half-landed-fold class (a fold that fixes its target but not its downstream consumers) was caught twice by the change-first census rule and is recorded in `dev-flow-lessons` terms for the increment gates: every fold names its consumers.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| ARCH-1 | architect | major | HLR-2604, LLR-2604.2 | `app.py:2433` is a project-span due mark (`{pn} +{over}d past ◆`), misfiled as a seat site; unimplementable (the seat is keyed by task) | move to the exclusion list; qualify the commission's "when they show a milestone mark" | fixed (LED .26/.27; pass 2 closed the three stale consumers, LED .37) |
| ARCH-2 | architect | major | LLR-2601.1 vs LLR-2608.2 | `find` two-stage semantics contradict the round's prefix rule the filter cites (`find_class` is startswith-only) | make `find` prefix-only | fixed (LED .29) |
| ARCH-3 | architect | minor | LLR-2604.1 | the date-style channel unspecified (style consumed by the glyph) | a non-empty `late_chip` implies the date renders `over` at every site | fixed (LED .28) |
| ARCH-4 | architect | minor | LLR-2605.1, §1.2 | the round's `+ new class…` Select option dropped without a carve-out | record the drop in §1.2 Out with its reason | fixed (LED .33) |
| ARCH-5 | architect | minor | LLR-2601.1 | `named(name)` has no consumer | drop it | fixed (LED .29) |
| QA-1 | qa-reviewer | minor | HLR-2601 | black-box arms read the internal `app.marks.path` | assert the file's bytes on disk | fixed (LED .30) |
| QA-2 | qa-reviewer | minor | HLR-2607 | the README clause not covered by its verification command | add `tests/test_readme.py` to the command | fixed (LED .31) |
| QA-3 | qa-reviewer | minor | LLR-2607.2 | details-line seat hedged while the threshold pins it | statement/threshold agree; increment-004 gate confirms `_gantt_legend` | fixed (LED .32) |
| QA-4 | qa-reviewer | major | §1.3, HLR-2606 vs LLR-2601.1 | the LED .40 fold (`◆` ∉ `SHAPES`) landed in the LLR only; the glossary and the form's statement still offered `◆` as a member — a saved class would be dropped at the next start | fix both consumers | fixed (LED .45, verified by the qa-reviewer) |
| QA-5 | qa-reviewer | minor | LED .38 evidence | the decomposition prose sums to 22, not 20 | append-only ledger; record-only | accepted (record-only) |
| SEC-1 | security-reviewer | major | LLR-2601.1 | load validation omits `colour` (and field types): a hostile `marks.json` injects an arbitrary style → Rich raises at first paint | validate `colour ∈ COLOURS` (NEW constant), types, `hidden` coerced; TC arms | fixed (LED .29/.40) |
| SEC-2 | security-reviewer | minor | §6.3, LLR-2601.1 | the `form` answer overclaims: `strip_controls` keeps `\t`/`\n` | cite the flattening step; soften §6.3; a newline-name TC arm | fixed (LED .29/.43) |
| SEC-3 | security-reviewer | minor | LLR-2601.1 | the ANSI/control-byte hostile arm untraced | name it in the threshold | fixed (LED .40; wording softened, LED .37 pass) |
| SEC-4 | security-reviewer | minor | §6.3 | the slug travels on team sync; "names never travel" nominal only | one acknowledging line | fixed (LED .44) |
| SEC-5 | security-reviewer | minor | AT-2602 | white-box against rule (d) | record the file-as-surface exception | fixed (LED .36) |
| UX-1 | ux-reviewer | major | HLR-2604 catalog | "empty: every frame draws exactly as before" unsatisfiable — the encoding itself changes unclassified draws (MM-D1's accepted cost) | reword to unclassified-draws | fixed (LED .26) |
| UX-2 | ux-reviewer | minor | HLR-2606 | the key row says `␣ hide` but space toggles both ways | `␣ hide/show` as the round paints it | fixed (LED .35) |
| UX-3 | ux-reviewer | minor | §5.1 | style claims assert plain screen text (no tone) | name the styled-segment export as the machine oracle; the `m01-` captures the visual one | fixed (LED .42) |
| UX-4 | ux-reviewer | minor | LLR-2607.2 | the `/#cls` gesture documented only in the README | `?` names the filter | fixed (LED .32) |
| UX-5 | ux-reviewer | minor | HLR-2605, LLR-2605.1 | "no directory" unsatisfiable (the app always loads one, possibly empty) | "an empty directory" | fixed (LED .33/.34/.41) |
| pass-2 minors | all four | minor | the ARCH-1 half-land: AT-2603 "the three notices"; the "(21 sites)" count; the shipped surface's "slip"; HLR-2601's narrow skip list; the "nine glyphs" miscount; §6.3 "AT arms"; the missing `env -u NO_COLOR` prefixes; §5.1/§6.3 ledger pairings | — | fixed (LED .37–.44) |

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ clean across all three iterations (the only out-of-statement `shall` is the template preamble's own rule text, `01-requirements.md:4`).

### Security review summary

Family C fired C6 (new input surface: `marks.json`, the form, `/#cls`) and C8 (new screens drawing loaded text); C1/C2/C3/C4/C5/C7 did not fire (`marks.json` holds only the operator's own class labels — no third-party personal data, unlike the people round). §6.3 answers the scanner's four flags (`session`, `payment`, `form`, `escape`). SEC-1 (the load-validation gap) was the one major; folded with TC arms. The security-reviewer verified every payload arm lands in a TC threshold with a machine oracle, and re-reviews `marks.py` at increment 001's gate per the commission's swarm rule and §6.3. No secrets, synthetic data only, the conftest home seam, the operator's name nowhere.

### Census notes

Change-first, best-effort + gate-confirmed: the pass-2/pass-3 stale-consumer sweeps (no live "21 sites" / "three notices" / `:2433`-as-seat remains anywhere in §1.2–§6; the only hits are the ledger's append-only Before-side quotes) are the worked example of why the census is keyed on consumers, not on the checklist. The increment packets repeat the reverse census (B1 fired).

# Review — taskboard — Batch 2026-10-21-batch-01

> **Artifact language:** canonical English scaffold. Generate in the batch's development language (`state.json` `language`).
> Phase 2 artifact. Reviewers (in parallel): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` by trigger family C (always in `full`).

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/review-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

## ✅ Verdict (read first)

- **Gate:** `approve` — all four lenses `approve with conditions` (architect: ARQ, P2, PDR; qa-reviewer: P2, PDR; ux-reviewer: P2, PDR; security-reviewer: P2, PDR with S-1 re-checked at increment 001); the requirement-defect majors (qa QA-1 a self-contradicting cap; ux UX-1 the key row misdescribing `enter`) and every minor were folded into the contract the same day as LED-2026-10-21-batch-01.2 and into the draft code and tests before Phase 3 → Phase 3 through the PDR
- **Out-of-scope findings:** 5 named and routed below — S-2 (the `.corrupt` copy's POSIX mode), S-3 (one copy per start of a still-unreadable file), S-5 (format characters in names), UX-11 (`Save` on the filter window), A-7 (another window's adds shown after a restart) → `BACKLOG.md` at the close (A-7 accepted in §6.3)
- **Findings:** 0 blocker · 9 major (QA-1..QA-5, UX-1..UX-3; S-1 medium) · 29 minor/low/info
- **shall/should check:** ✓ clean
- **Two-layer (blockers):** ✓ every story has an `AT` · output reqs name deliverable+observation · both trace chains complete (the map in §2.6 after A-4) · ATs drive `open_app` and keys and read the screen's text, the notices and the files (QA-9's internal reads replaced by drawn text and typed keys)
- **Census (change-first):** done — best-effort + gate-confirmed (PLAN.md §Triggers B1; each increment's packet repeats it)
- **Security:** ⚠ 6 findings (S-1 medium, fixed in the draft and to be re-checked by the security-reviewer at increment 001; S-2, S-3 low, accepted and logged; S-4 low, S-5, S-6 info, accepted)
- **Evidence checklists (architect / qa / security):** ✓ all complete (in the reviewers' returns; ux-reviewer too)

> If gate = `approve` and every line is ✓, the Detail below is reference. Any blocker/⚠ → read the matching part.

---

## Detail (reference)

Reviewers: `architect`, `qa-reviewer`, `ux-reviewer` (D1 fired), `security-reviewer` (C3, C6, C8 fired) — each spawned as a sub-agent with its `agents/<role>.md` role, read-only, in parallel, 2026-10-21, one iteration; each reviewed the ARQ amendment, the requirements (P2), the design proposal (PDR) and the drafted code and tests together. The qa-reviewer ran 9 mutants in scratch copies; the security-reviewer timed the tokeniser; the ux-reviewer drove the real app headless and read its SVG styles.

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| A-1 | architect | minor | ARQ §2/§4 | the keymap's exceptions, `key_line`'s and `peek_board`'s consumers, and three changed signatures not in the map | add the rows | fixed (ARQ) |
| A-2 | architect | minor | ARQ §1/§5 | `people.json.lock` not in the lock row; no §5 row for `PeopleDirectory` | add both | fixed (ARQ) |
| A-3 | architect | minor | LLR-2501.1, ARQ §3 | `people.py` imports the private `boards._keep_aside` | public `boards.keep_aside`, docstring generalised | fixed (LED .2; increment 001) |
| A-4 | architect | minor | HLR-2502 | no AT of its own; US/HLR numbering offset | AT-2502 (the rename arm); the chain map in §2.6 | fixed (LED .2) |
| A-5 | architect | minor | HLR-2503 | `tab` leaves the list open; `enter` elsewhere writes a mention | `tab` closes it; the list's keys act only while the notes hold the focus | fixed (LED .2; increment 003) |
| A-6 | architect | minor | HLR-2501 | an empty file warns of a copy at "nowhere" | empty → no notice; `no copy could be kept` | fixed (LED .2; increment 001) |
| A-7 | architect | minor | HLR-2501 | another window's adds invisible until restart | record as accepted | accepted (§6.3) |
| A-8 | architect | info | HLR-2501 | the no-registry location is a test seam | say so | fixed (LED .2) |
| A-9, A-10, A-12 | architect | info | PDR | `Board.people` live dict sound; `tab` binding equivalent; split the draft carefully | keep the guards; run each increment's and the touched files' suites on the split tree | noted (each packet) |
| A-11 | architect | info | AT-2504 | `@` over the presentation and from the main screen not driven | two arms | fixed |
| QA-1 | qa-reviewer | major | HLR-2505 | «at most 6 … all of them» contradicts itself; the cap untested (M2 survived) | the first 6 by name; assert Luis shown, Marta and Pablo not | fixed (LED .2; increment 005) |
| QA-2 | qa-reviewer | major | AT-2503 | only the x bound; the flip-up never runs (M3 survived) | an arm near the bottom at 80×24 | fixed (increment 003) |
| QA-3 | qa-reviewer | major | AT-2504 | `@` on the home untested (M4 survived) | press `@` on the home | fixed (increment 004) |
| QA-4 | qa-reviewer | major | AT-2505 | the gantt untested (M6 survived) | a gantt arm | fixed (increment 005) |
| QA-5 | qa-reviewer | major | HLR-2504 catalog | the vanished board and the failed write ticked, untested | two arms | fixed (increment 004) |
| QA-6 | qa-reviewer | minor | HLR-2504 | four strings unasserted | one assertion each | fixed |
| QA-7 | qa-reviewer | minor | HLR-2501 | name and note caps untested | 61/201 cut, 60/200 kept | fixed |
| QA-8 | qa-reviewer | minor | AT-2504 | seat keys checked by the stack only | the view, board, task count, selection | fixed |
| QA-9 | qa-reviewer | minor | §5.1 | ATs reading internal state | drawn text on another board; the rename typed | fixed |
| QA-10 | qa-reviewer | minor | TC-2504, TC-2506 | `or` assertions | the one string; the full order | fixed |
| QA-11 | qa-reviewer | minor | HLR-2503 | arrows with the list closed | an `up` arm | fixed |
| QA-12 | qa-reviewer | info | C-40 | RED on base and mutations still planned | record per increment | per packet |
| UX-1 | ux-reviewer | major | HLR-2504, D-7 | the key row says `↵ open on its board` on the people pane | a row per pane: `↵ their tasks` / `↵ open task` | fixed (LED .2; increment 004) |
| UX-2 | ux-reviewer | major | HLR-2504 | the tones are inspected, not exercised | a TC on the spans | fixed (increment 004) |
| UX-3 | ux-reviewer | major | AT-2503 | the notes reached by `.focus()` | reach them by `tab`; assert the y bound | fixed (increment 003) |
| UX-4 | ux-reviewer | minor | HLR-2504 | the key row ends `n   e   esc` at 80; `e edit` ambiguous | shorter words, `e edit person` | fixed |
| UX-5 | ux-reviewer | minor | HLR-2504 | no "more" marker; an orphan quote after scrolling | whole tasks; `↓ N more below` | fixed |
| UX-6 | ux-reviewer | minor | HLR-2504 | two teal cursors | the other pane's dimmed | fixed |
| UX-7 | ux-reviewer | minor | HLR-2505 | `alt+p page` reads like paging | `alt+p their page` | fixed |
| UX-8 | ux-reviewer | minor | `PersonForm` | placeholders only; `tab` unsaid | labels; `⇥ next field` | fixed |
| UX-9 | ux-reviewer | info | D-3 | the box's order vs the objection's spoken order | name it on the capture page | → close (operator item) |
| UX-10 | ux-reviewer | info | D4 | `read-only` beside `n`/`e` | `tasks read-only` | fixed |
| UX-11 | ux-reviewer | info | HLR-2505 | the filter window's button says `Save` | backlog | routed → `BACKLOG.md` |
| S-1 | security-reviewer | medium | HLR-2507, LLR-2502.1 | `MENTION_RE`'s link branch is quadratic: 100 000 chars ≈ 25 s per render | bound the name `{1,60}`; skip a text without `@`; a timing TC | fixed (LED .2; increment 001; re-check owed by security) |
| S-2 | security-reviewer | low | the `.corrupt` copy | follows the umask on POSIX (0644) | owner-only, or accept | accepted, logged → `BACKLOG.md` |
| S-3 | security-reviewer | low | the `.corrupt` copy | one more copy per start of a still-unreadable file | skip identical bytes, or accept | accepted, logged → `BACKLOG.md` (shared with the registry) |
| S-4 | security-reviewer | low | the presentation | paints by name, not by parsed mention | accept | accepted (§6.3) |
| S-5 | security-reviewer | info | names | format characters survive `strip_controls` | a later batch | accepted, logged |
| S-6 | security-reviewer | info | leakage | names reach the screen only | none | — |

### shall / should check
✓ clean — every HLR/LLR statement uses `shall`; no modal `should` in a statement.

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-2501 | yes (AT-2501, AT-2502, AT-2507) | yes (`people.json`, the screen, the team file) | yes | yes after QA-9 | ✓ |
| US-2502 | yes (AT-2503) | yes (the notes, the preview, `board.json`) | yes | yes | ✓ |
| US-2503 | yes (AT-2504) | yes (the screen, `people.json`) | yes | yes | ✓ |
| US-2504 | yes (AT-2505) | yes (the filtered view and its bar) | yes | yes | ✓ |
| US-2505 | yes (AT-2506) | yes (details, card, presentation) | yes | yes | ✓ |

### Supersession census (change-first)
The planned source files (`people.py` new, `models.py`, `app.py`, `views.py`, `modals.py`, `keymap.py`, `boards.py` — `keep_aside`, A-3) against the guard families: behavioral (the B1 census in `PLAN.md` §Triggers: the editor, details, kanban, presentation, filter, keymap and agenda suites), structural (`tests/test_markup_census.py`'s sink law, `tests/test_modal_keys.py`'s inventory law, `tests/test_keymap.py`/`tests/test_readme.py`'s README laws), frozen modules: none. Reservations: the draft run found the markup census and the README laws (fixed in the draft: Text pieces, `Directory.edit` — a method named `update` read as a Textual sink —, `@` spelled); the increment gate is the completeness guarantee.

### Security review summary
`approve with conditions` — S-1 fixed in the draft (bounded link name, the `@` pre-check, a timing TC that must fail on the unbounded pattern); the security-reviewer re-runs its timing at increment 001. Verified clean: markup injection (every new render Text pieces, the new notices `markup=False`), the atomic write and lock, symlinks, hostile `people.json`, team sync (`Board.people` outside `_to_dict`).

### Evidence checklists (full) — architect · qa-reviewer · security-reviewer
- **architect:** constraints stated ✓ · alternatives ✓ (PDR §6) · n/a constraints marked ✓ · rationale ✓ (D-1..D-11) · risks ✓ · cost/latency n/a ✓ · diagram ✓ · what would change it ✓ · two-layer ✓ (A-4) · layering checked against the code ✓ · tests executed ✓ (84 passed, people suites).
- **qa-reviewer:** Given/When/Then (EARS) ✓ · explicit expected ✓ · edge cases ✗→✓ after QA-1, QA-2, QA-5, QA-7 · regression checklist ✓ · exit criteria ✓ · no real PII ✓ · mode declared (plan) ✓ · planned results labelled ✓ · Layer B through the surface ✗→✓ after QA-3, QA-4, QA-9.
- **ux-reviewer:** context of use ✓ · observable criteria ✓ (UX-2 folded) · real mechanism ✓ (headless pilot; UX-3 folded) · painted result: SVG computed style, not the Windows Terminal paint — the real captures come at the DDR · error/empty/slow states ✓ (declared) · evaluation with users: not performed (one operator; the verdict chose renders).
- **security-reviewer:** each finding what/where/why/recommendation ✓ · severity ✓ · no secret values ✓ · explicit verdict ✓ · new tool scope n/a (no external integration).

# Review — taskboard — Batch 2026-10-02-batch-01

> Phase 2, two-lens cross-review (core) plus the security lens (family C fired). Lenses:
> `qa-reviewer`, `ux-reviewer` and `security-reviewer`, each spawned as an independent
> sub-agent of this runtime with its role file (`agents/<role>.md`), read-only, over
> `01-requirements.md` as drafted at P1 iteration 1.

## ✅ Verdict (read first)

- **Gate:** `approve` → Phase 3 after iteration 2 (all three lenses PASS-WITH-NOTES, 0 blocker, 0 HIGH, every new note folded or carried), under the standing authorization. Iteration 1 — qa-reviewer `FAIL` (2 blockers), ux-reviewer `FAIL` (1 blocker, the same defect as Q-2), security-reviewer `PASS-WITH-NOTES` (0 HIGH) → `iterate-to-refine` → P1. Every finding folded into the live contract (ledger `LED-2026-10-02-batch-01.10` through `.18`) or declared with a disposition below. Iteration 2 — the same three lenses re-read the folded contract (verdicts recorded in §Iteration 2); the gate is taken on that pass.
- **Out-of-scope findings:** 6 named and routed below (operator design questions UX-6, UX-7, UX-9, UX-11b, UX-12; accepted risk S-5).
- **Findings:** 3 blocker (Q-1, Q-2, UX-1 — two defects) · 19 major · 19 minor/low
- **shall/should check:** ✓ clean (no `should` in any HLR/LLR statement; qa-reviewer)
- **Two-layer (blockers):** ✓ after the fold — every story has an `AT` through the shipped surface (US-101: AT-101/102/103/108/109; US-102: AT-104/105; US-103: AT-106; US-104: AT-107); render-level checks are TCs (Q-12).
- **Census (change-first):** done — best-effort + gate-confirmed; the reverse census is MEASURED (P-10: 31 nodes, `01-requirements.md` §6.6), not predicted.
- **Security:** ⚠ 6 findings (3 MEDIUM folded, 1 MEDIUM evidence redaction done, 1 LOW folded, 1 LOW accepted risk → BACKLOG); 0 HIGH.
- **Evidence checklists:** each lens report is summarised in the findings table; the reports themselves are the sub-agents' final messages (this runtime keeps them out of the tree).

## Detail

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| Q-1 | qa | blocker | HLR-106 | "every tick drawn" is false whenever a task is selected: the verdict frames drop ticks under the echo | exempt the echo zone; no-selection arm | fixed — LED .15 |
| Q-2 | qa | blocker | HLR-104, scope | `_select_first` keeps a done task (`tw1`) → `down` dead once nav holds open work only | LLR on `app.py`; entry + phase-move arms | fixed — LLR-101.9, LED .13, P-9 |
| UX-1 | ux | blocker | HLR-104, D2 | same defect as Q-2, reached by `]` and by `3` | AT through the real keys | fixed — AT-108, LED .13 |
| Q-3 | qa | major | AT-102 (C-12) | `line_map` membership ≠ the consumer scrolling it | assert the viewport holds the row | fixed — LED .13 |
| Q-4 | qa | major | HLR-102 | `N open` / `✓n` contradict the 80×24 frame | narrow form | fixed — LLR-101.11, LED .11 |
| UX-2 | ux | major | HLR-102 | same as Q-4 | — | fixed — LED .11 |
| Q-5 | qa | major | LLR-101.3 | stop-vs-skip fold order ambiguous; oracle board cannot tell | state skip; synthetic board | fixed — LED .11 |
| Q-6 | qa | major | HLR-101 | past / undated project would vanish | always a span row | fixed — LED .10 |
| Q-7 | qa | major | HLR-104, D8 | span overflow strands the cursor on an undrawn group | draw the run holding the selection | fixed — LLR-101.6, LED .13 |
| Q-8 | qa | major | C-10a | `v`, `F`, `/` never driven off default | one AT arm each | fixed — AT-109, LED .10 |
| Q-9 | qa | major | AT-106 (C-31) | no URL card; presentations hand-listed; detector could be vacuous; shared tokens' other views untested | URL card, reach asserts, non-vacuity, extra arms | fixed — LED .17, LLR-103.3 |
| Q-10 | qa | major | C-26 | no LLR names the surfaces it supersedes; §6.3 sorted failures after the fact | measured census table | fixed — P-10, §6.6 |
| Q-11 | qa | major | LLR-101.3 | `height = 0` undefined | 0 = unbounded | fixed — LLR-101.3 |
| Q-12 | qa | major | ATs | four ATs drove `render_view` | ATs through the pilot, render checks as TCs | fixed — §5 AT table |
| Q-13 | qa | major | LLR-101.4 | `%-d` crashes on Windows | state the output | fixed — LED .12 |
| Q-14 | qa | major | HLR-106 | scale reach unasserted in the sweep | assert set of scales, ≥ 1 tick per arm | fixed — LED .15 |
| UX-3 | ux | major | HLR-106 | same as Q-1 | — | fixed — LED .15 |
| UX-4 | ux | major | HLR-105/107 | the day row's cadence·scale label missing; fallback unstated | state both | fixed — LED .14, .16 |
| UX-5 | ux | major | layout | legend-row rule and width breakpoints unstated | LLR | fixed — LLR-101.10 |
| UX-6 | ux | major | HLR-108, D10 | keybar keeps accent; per-view title colour | reword; **operator question** | fixed (wording, LED .17); title-per-view routed to the operator (D10) |
| UX-7 | ux | major | US-103, D4 | the selection is reverse, today is the loudest accent | reword to what ships; **operator question** | fixed (wording, LED .17); routed to the operator (D4) |
| UX-8 | ux | major | ATs | `line_map` is not the painted screen; panel ≠ terminal | painted-screen asserts; define sizes | fixed — §1.3 sizes, HLR-104 threshold |
| Q-15 | qa | minor | HLR-104 | "wrap" wrong: ends are no-ops | restate | fixed — LED .13 |
| UX-10 | ux | minor | HLR-104 | same as Q-15 | — | fixed |
| Q-16 | qa | minor | LLR-102.4 | same-month shortening only for the joined form | restrict | fixed — LED .16 |
| Q-17 | qa | minor | HLR-105 | `daily` unreachable in an HLR | move to LLR | fixed — LED .14 |
| Q-18 | qa | minor | layout | vertical split unstated | formula | fixed — LLR-101.10 |
| Q-19 | qa | minor | LLR-103.2 | `━ chain N` ≠ frame `chain 4` | quote the frame | fixed — LED .17 |
| UX-11 | ux | minor | LLR-103.2, D3 | (a) invented `━` in header; (b) `━` shared by chain and echo; (c) packet on a chain reach | (a) fix; (b) **operator question**; (c) criterion | (a) fixed; (b) routed (D13); (c) fixed — LLR-101.7 |
| Q-20 | qa | minor | HLR-101 | unparsable date marked N/A | make it a case | fixed — LED .10 |
| Q-21 | qa | minor | HLR-109 | hand-listed path strings | one pattern | fixed — LED .18 |
| Q-22 | qa | minor | LLR-101.5 | "late" undefined; no-start dependency rule | define | fixed — §1.3, LED .12 |
| Q-23 | qa | minor | AT-105 | drive undetermined; old bracket not asserted | explicit drive | fixed — LED .16 |
| Q-24 | qa | minor | P-4 | hand-listed accent sites missed two | census from rendered output | fixed — P-4 re-taken (`evidence/p0-probes.txt`) |
| UX-9 | ux | minor | D9 | tall-group window position; above/below hint | page-aligned; **operator question** on the hint | fixed (page-aligned, LLR-101.6); hint routed (D9) |
| UX-12 | ux | minor | D11, D12 | `This week` urgency hue; mixed language | `hd`; **operator question** | D11 → `hd` (fixed); D12 routed |
| UX-13 | ux | minor | HLR-107/108 | no-selection `today …` label in accent | list as a today mark | fixed — HLR-108 |
| UX-14 | ux | minor | §2.3, §6.1 | task, evaluation states, empty text | add | fixed — §2.3, §6.1, HLR-101 empty |
| S-1 | security | MEDIUM | LLR-101.8 | focused-header project name unescaped: `[/]` → `MarkupError` (reproduced on base) | add the seat, negative control | fixed — LLR-101.8 |
| S-2 | security | MEDIUM | LLR-101.8 | payload matrix narrow; fit-then-escape order unstated | extend; state order | fixed — LLR-101.8 |
| S-3 | security | MEDIUM | record | `PLAN.md` and `evidence/base-suite.txt` carried a home path | redact before commit | fixed — redacted, re-grepped 0 |
| S-4 | security | LOW | HLR-109 | literal path list misses forms, over-matches `<you>` | one pattern | fixed — LED .18 |
| S-5 | security | LOW | repo | the username path is public in older tracked files | accept; BACKLOG | routed — BACKLOG at close (accepted risk) |
| S-6 | security | MEDIUM | §6.1 | captures not tied to a synthetic board | fixture only + privacy sweep at gates | fixed — §5 |
| S-7 | security (P3, increment 003 pass) | MEDIUM | record | the pytest temp directory name carried the username into three evidence transcripts | scrub with the runtime username; redact at capture | fixed — scrubbed (0 files), runtime redaction added; verified by security-reviewer |
| S-8 | security (P3, increment 003 pass) | MEDIUM | `tools/privacy_sweep.py`, `tools/precommit_privacy.py` | the privacy tools do not decode HTML entities, and rich's SVG writes spaces as `&#160;`, so a multi-word board title in an SVG capture could pass unseen (nothing leaks today) | decode before matching; RED test with an entity-encoded two-word title | routed — BACKLOG at close (tools/ is outside this batch); the entity-decoded sweep over `evidence/` and `docs/*.svg` is a close-gate step until it lands |
| S-9 | security (P3) | LOW | `tests/test_readme.py` | the home-path pattern has no bare-username arm | never put the literal username in a committed file; use the runtime grep | accepted — runtime grep at each gate |

### shall / should check
No `should` in any HLR/LLR statement (qa-reviewer, iteration 1); the folded statements re-checked by grep at iteration 2: `grep -n "should" 01-requirements.md` → only informative text.

### Two-layer acceptance review (blockers)
| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-101 | yes (AT-101/102/103/108/109) | yes — painted board panel | yes (HLR-101..104 → LLR-101.1..11 → TC-101..111) | yes — keys through `TaskboardApp` | ✓ |
| US-102 | yes (AT-104/105) | yes — painted ruler rows | yes (HLR-105..107 → LLR-102.1..5 → TC-112..116) | yes | ✓ |
| US-103 | yes (AT-106) | yes — painted accent cells | yes (HLR-108 → LLR-103.1..3 → TC-117..119) | yes | ✓ |
| US-104 | yes (AT-107) | yes — the files | yes (HLR-109 → LLR-104.1..2 → TC-120..121) | yes | ✓ |

### Supersession census (change-first)
Planned edits: `taskboard/views.py` (gantt renderer + helpers, nav seat, legend/help; kanban accent sites; `card_cell`, `reldue_token`), `taskboard/app.py` (`_select_first`), `README.md`, `RUN.md`; new tests. The reverse census was EXECUTED (P-10) on a scratch copy with the drafted renderer: 31 nodes in 7 files, each dispositioned in `01-requirements.md` §6.6; the kanban-side census (titles, `+Nd`, `↗`, horizon colour, matrix percent) is run at its increment. Best-effort + gate-confirmed: the full suite at each increment gate is the guarantee.

### Security review summary
security-reviewer, iteration 1: PASS-WITH-NOTES, 0 HIGH. S-1 (a live `MarkupError` in the focused gantt header, reproduced on the base tree) and S-2 folded into LLR-101.8; S-3 discharged by redaction; S-4 folded into HLR-109; S-6 folded into §5; S-5 accepted and routed to BACKLOG.

### Out-of-scope / routed
| Item | Owner | Where |
|---|---|---|
| UX-6 per-view title colour until app-wide budget | operator | D10, close report |
| UX-7 today in accent vs selection in accent | operator | D4, close report |
| UX-9 above/below hint for a paged group | operator | D9, close report |
| UX-11b `━` shared by chain and echo | operator | D13, close report |
| UX-12 gantt header English beside Spanish help | operator | D12, close report |
| S-5 username path in older tracked files | backlog | BACKLOG at close |

### Iteration 2
| Lens | Verdict | Notes |
|---|---|---|
| qa-reviewer | PASS-WITH-NOTES | Q-1, Q-2 (blockers) and 20 more discharged; Q-8, Q-11 partial → closed by N-1/N-2 folds. New: N-1 major (vacuous `v` arm; F and / expected values) folded LED .20; N-2 height 1–3 folded LED .20; N-3 filtered offset folded (IFC); N-4 page-aligned overflow run folded LED .21; N-5 the `app.py` seat's census owed at increment 001's gate — carried |
| ux-reviewer | PASS-WITH-NOTES | UX-1 (blocker) and 11 more discharged; UX-7 → US-103 reworded; UX-11c visual claim judged at P4 from captures. New: UX-15 major (repair to the group's first task) folded LED .19 — neighbour rule; new operator question: a cue when a finished task leaves the gantt (no prototype covers it) |
| security-reviewer | PASS-WITH-NOTES, 0 HIGH | S-1..S-4, S-6 discharged; S-5 routed. New LOW: N-1 re-grep the batch folder at each gate (folded, §5); N-2 one pattern for RUN.md (folded, LLR-104.2); N-3 add the bare username to the pattern — declined: the test file would then carry the username itself |


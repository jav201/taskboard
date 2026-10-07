# Requirements ledger — taskboard — Batch 2026-10-07-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._

### LED-2026-10-07-batch-02.1 — the chain map derived from the D-C frames (P1)
- **Requirement:** HLR-801, HLR-802, HLR-803, LLR-801.1, LLR-801.2, LLR-802.1, LLR-803.1
- **Date:** 2026-10-07
- **What changed:** new requirements: US-801/802/803 (the chain map view, the per-chain rule switch, the high-band cap); HLR-801 (the D-C frame as the law: chains, connectors, fan-ins, the meta row, the critical chain in structure not hue, the band heads, the legend, the strip, 118x30 and 80x24); HLR-802 (the dates: switch on the shipped extra["date_links"] storage — UXV-6's deferral); HLR-803 (the R-1b cap). LLRs decompose renderer/wiring/switch/cap.
- **Why:** the approved plan's batch C ("K-B, chain map view"); the operator's 2026-10-07 commission to finish the plan's proposed changes; the frames were verdicted in rounds 3-7 and the storage/seats they need shipped in batches 2026-10-04-01/02 and B2b.
- **Evidence:** the prototype frames `out/D-C-118x30.txt`, `out/D-C-80x24.txt`, `out/C-2*.txt` (worktree kg-mejoras) · DEPS-CONTRACT.md · the round-7 polish rules (accent = focus only; critical chain = structure).

### LED-2026-10-07-batch-02.2 — P2 iteration-1 findings folded (P1, iteration 2)
- **Requirement:** HLR-801, HLR-802, HLR-803, LLR-801.1, LLR-801.2, LLR-802.1, LLR-803.1
- **Date:** 2026-10-07
- **What changed:** the oracle is C-2b (round-7 verdict), both sizes (`C-2b-80x24.txt` added to `evidence/frames/`) — the D-C frames stay as history; TWO fixtures (base for the frame rows — 15 linked; milestones for the rule arms — `td0`/`td4`/`td5`); the critical chain pins the heavy `┃`/`━━▸┃` structure with a greyscale-law arm; the switch/footer literals pinned per width from the frames (118: `dates  ○ stay  ● push  ○ together`; 80: compact; wide footer with the verbatim explainers; narrow `▌‹label›: ‹short› · m change for this chain`); the label↔stored-string map pinned (stay↔flag, push↔push_delta, together↔together — labels never paint the stored strings); `set here` pinned (the deviating band's marker at 118); the `x`/`m` view-dispatch decided and pinned (x → the shipped `unlink_tasks` seat with the new refusal literal `nothing to remove — the selection waits on no task`; m → the selected task's project rule; the shipped archive/cascade meanings inert on this view); HLR-803 re-scoped as a CHARACTERIZATION pin of the shipped cap (`views.py:4641-4650,5024-5028`) — no renderer change owed; the port-source citation corrected (`variants_polish.py`'s `_dc2`/`strip2`, deriving `variants_deps_gantt.render_dc`); §2.7 filled with the four executed premises (P-3 recording the x/m decision); an S1 hostile-title arm added (TC-807); the TC↔arm ownership enumerated (TC-801..808).
- **Why:** P2 iteration 1 — four lenses FAIL (blockers: the D-C-vs-C-2b oracle contradiction, RED-by-construction thresholds, the one-fixture error; majors: the x/m collisions, the shipped-cap re-scope, the phantom literals and the port path); every disposition in the lenses' reports, convergent across all four.
- **Evidence:** `evidence/frames/C-2b-118x30.txt`, `C-2b-80x24.txt` (the law) · the lenses' P2 iteration-1 reports.

### LED-2026-10-07-batch-02.3 — P2 iteration-2 findings folded (P1, iteration 3)
- **Requirement:** HLR-801, HLR-802, LLR-801.1, LLR-801.2, LLR-802.1
- **Date:** 2026-10-07
- **What changed:** `set here` restated at BOTH widths (the port source paints it whenever the rule is custom — the "80 has no marker" claim and its false footer clause are gone); the wide footer's lead is ` ▌‹hue›` (the `◆` was the superseded C-2 form) and the Label slot is the LONG labels, pinned verbatim (`Keep others, flag conflicts` / `Push what it collides with` / `Move the whole chain`); the strip's early-by measure pinned as the prototype's `(pred.due − start).days` — plain difference, NOT `link_overlap`'s both-days +1; the `no links` row restated as the full band head; the 80 head-drop rule restated generically; LLR-801.2 pins extending `L`'s `views=` tuple with `chainmap`; §5 gains PER-ARM fixtures (TC-801/802 on the base board with `pdwh.extra["date_links"] = "together"` set in-test; the milestones call takes the REQUIRED `date.today()`); §2.8 declared `none`.
- **Why:** P2 iteration 2 — four lenses FAIL on literal pins contradicting the C-2b law (C22-1/2/3 convergent) plus fixture/citation notes; the iteration-1 blockers verified genuinely resolved.
- **Evidence:** `evidence/frames/C-2b-118x30.txt:15,18,22,30`, `C-2b-80x24.txt:15,18` · `variants_polish.py:510,750` · `variants_cascade.py:38-40,364-366` · `variants_deps_gantt.py:75-78`.

### LED-2026-10-07-batch-02.4 — P2 iteration-3 findings folded (P1, iteration 4)
- **Requirement:** HLR-801, LLR-801.1, LLR-802.1, HLR-802
- **Date:** 2026-10-07
- **What changed:** LLR-802.1's LIVE text corrected (the fold .3 had amended HLR-802 but left LLR-802.1's stale ` ◆ ` footer template and its "(118)" residue — the exact blocker qa/architect flagged; the live text now carries ` ▌‹hue›` and both widths, matching LED .3's intent); the `○` meta gloss corrected (open chain head — no predecessors — dated or not; NOT "undated-open"); §5 gains the FROZEN-CALENDAR clause for the exact-row arms (the house `frozen` monkeypatch, today = kg_board.TODAY — without it the shifted board's dates drift off the frames' fixed bytes every day); AT-801/AT-803's fixtures named (frozen base + in-test together; the crowded in-test fixture + the recorded-mutation route); the legend row named in LLR-801.1's statement (with the 80 `─ satisfied` shed).
- **Why:** P2 iteration 3 — security PASS-WITH-NOTES, ux PASS, qa/architect FAIL on the single residual blocker (the .3 fold partially applied) plus the ○ gloss, the frozen-calendar coupling and the fixture-name notes; the qa lens's note about V26 passing a contract whose text contradicted its own ledger recorded here as the lesson (folds must touch EVERY site of a repeated literal).
- **Evidence:** `evidence/frames/C-2b-118x30.txt:30` · `variants_polish.py:750,691-711` (the ○ slot) · `tests/test_gantt_board.py:65-76` (the frozen-calendar fixture).

### LED-2026-10-07-batch-02.5 — increment 001 review folds (the code-reviewer's HIGHs)
- **Requirement:** LLR-801.1, LLR-801.2, LLR-802.1
- **Date:** 2026-10-07
- **What changed:** TC-809/TC-810/AT-801b added (the deep-chain crash, the mid-band fold, the L arm); the column cap at 4 with the depth clamp (CM-1); the whole-band fold with the line_map clear and the app-side nav filter (CM-2); the header counting drawable tasks only (CM-4); the selection inked bright per the app-wide accent budget, the strip's › marker bright (AT-201); the census docstring (CM-5). HLR-801's ledger pairing gains this entry.
- **Why:** the code-reviewer's r1 BLOCK-UNTIL (CM-1/CM-2 HIGH, executed repros beyond the oracle frames' reach), fixed RED-first under the second exception; r2 PASS-WITH-NOTES verified both on the fixed tree.
- **Evidence:** `evidence/chunkA-run.log` · the reviewer's rev-2 report (repros re-executed) · `evidence/inc001-gate.txt`.

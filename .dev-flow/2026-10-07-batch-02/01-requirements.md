# Requirements Document — taskboard — Batch 2026-10-07-batch-02

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development language (`state.json` `language`). For Spanish batches, translate the **prose** — section headers and guidance — **and never a label**, and use `deberá` as the normative keyword (≡ `shall`). The normative RULES in this preamble are **language-independent** and enforced regardless of artifact language.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/docs/req-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `Validation` · `Acceptance test(s)` · `Boundary catalog` · `Negative control` · `Premise evaluation` · `Fork preconditions` · `Ledger` · `Requirement` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

---

## 1. Introduction

### 1.1 Purpose
*(Informative text. Describes the document's objective.)*

### 1.2 Scope
*(What this batch covers and what it does NOT cover.)*

### 1.3 Definitions, acronyms, abbreviations
| Term | Definition |
|------|------------|
| | |

### 1.4 References
*(Related documents, standards, external tickets.)*

### 1.5 Document overview
*(How this document is structured.)*

---

## 2. Overall description

### 2.1 Product perspective
*(How the change fits into the larger system.)*

### 2.2 Product functions
*(High-level list of functional capabilities.)*

### 2.3 User characteristics
*(Roles, permissions, expected experience levels.)*

### 2.4 Constraints
*(Technological, regulatory, business.)*

### 2.5 Assumptions and dependencies
*(What we take for granted. If an assumption fails, the batch is invalidated.)*

### 2.6 Source user stories

| ID | User Story | Source | DoR status |
|----|------------|--------|------------|
| US-801 | As a taskboard user, I want the chain map — who waits on whom, per project, with the ready/waits/late marks and the rule per chain on screen — so that the dependency web is something I SEE, not something I remember. | round-3 verdict (D-C ships as a view; IMPLEMENTATION-PLAN.md batch C) | READY |
| US-802 | As the operator, I want the per-project dates rule visible and editable where the chains live (the C-2 switch), so that I know what a move will do before I make it (UXV-6's deferral). | round-6 verdict (per-project setting, C-2) + round 7 (C-2b: full-width band rules, aligned switch) | READY |
| US-803 | As a taskboard user reading the kanban, I want the high band capped (`+N more`) so that it never pushes a project's late milestones below the fold. | round-8 open item (R-1b's cap; BACKLOG UX2-2 family) | READY |

**Refinement (one block):** INVEST all ✓ for the three (the frames exist and were verdicted; the storage — `extra["date_links"]` — shipped in batch B2b; the link seats — L picker, x remove — shipped in batch 2026-10-04-batch-01). Out of scope: batch D (flow templates), batch E (presentation mode), editing chains by dragging (read + keys only).

### 2.6a Source frames — the ORACLE is C-2b (round-7 verdict)

Round 7 built and checked T-C2 + C-2b ("full-width per-project band rules in the project hue,
aligned `dates:` switch"); C-2b is the law. The oracle frames (copied verbatim to
`evidence/frames/`, byte-identical to the prototype's renders): `C-2b-118x30.txt` and
`C-2b-80x24.txt`. The round-3 `D-C-*.txt` frames stay as history only. The renderer re-derives
from `variants_polish.py`'s `_dc2`/`strip2` (provenance: `variants_deps_gantt.render_dc`,
`variants_flow.chain_strip`) — re-deriving, not pasting.

**Two fixtures.** The frame rows pin against the BASE board (`kg_board.shifted` — 15 linked
tasks, the C-2b header's own count). The rule arms (AT-802) pin against the MILESTONES board
(`kg_board.milestones(kg_board.shifted(...))` — adds `td0` waiting on `td4`, `td5` waiting on
`td0`), which the frames' fixture does not carry; both fixtures are declared per arm in §5.

### 2.7 Premise evaluation (C-43)

| # | Premise | Verdict | Executed evidence |
|---|---|---|---|
| P-1 | Key `6` is unbound and `VIEW_ORDER` has no chainmap | TRUE | `keymap.py:61-69` (1-5,7-9,0), `app.py:52` |
| P-2 | `extra["date_links"]` ships lenient (junk → `push_delta`) and the project editor reads/writes the same key | TRUE | `models.py:1836-1838,1896-1905`; `modals.py:597-601,728-729` |
| P-3 | The board-level `x` is archive (global) and board-level unlink exists only inside the picker/details — the chain map's `x` and `m` are NEW view-dispatched meanings, decided here | TRUE (and the decision: on `view_mode == "chainmap"`, `x` routes to the shipped `unlink_tasks` seat with a new refusal literal; `m` cycles the selected task's PROJECT rule — pinned in LLR-801.2/802.1) | `keymap.py:80,103`; `app.py:1020-1023`; the frames' keybars (`C-2b-118x30.txt:28`, `C-2b-80x24.txt:22`) |
| P-4 | The kanban high-band cap ships (LLR-306.1): `cap = max(5, 2*(height-KANBAN_HEAD_ROWS)//3)`, `+N more ↓` per open-phase column | TRUE — HLR-803 is a CHARACTERIZATION pin, no renderer change owed | `views.py:4641-4650,5024-5028,5846-5848` |

### 2.8 Fork preconditions (C-52)

`none — the batch runs one lane: the increments land in order on the previous one's tree.`

## 3. High-level requirements (HLR)

### HLR-801 — The chain map makes the dependency web visible (the C-2b law)
- **Traceability:** US-801
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2, LED-2026-10-07-batch-02.3, LED-2026-10-07-batch-02.4
- **Statement:** The system shall provide a chain map view behind key `6` drawing, per the C-2b oracle frames at 118×30 and 80×24: the header `◆ CHAIN MAP · who waits on whom   15 linked tasks · ▲2 late · ━ chain 4`; per project a full-width band head — `─▌‹project›  ‹n› linked · ‹m› open not linked ──── ○stay ●push ○together ─` (118: `dates  ○ stay  ● push  ○ together`, spaced; 80: compact, no `dates` word) with `· ━ critical chain` in the counts where true (an 80 head sheds its trailing `· N open not linked` when room is short — Mobile App drops its own `· 1 open not linked`, Website keeps `· 2 open not linked` — per the frames); the chains laid left to right by due — `──▸` light connectors (two-space indent), fan-ins joined (`┬▸` above, `╰───╯` below), the meta row under each task (`✓` done · `▷ ready` · `○` open chain head (no predecessors — dated or not) · `◂N` waits on N open · `Mon D` · `▲Nd` late); the CRITICAL chain in heavy structure — `┃` task cells, `━━▸┃` connectors, bold — hue never carries it; a project with no links draws one full-width band head `─▌‹project›  ‹k› open · no links ───…` (no switch, per the frames); the selection strip at the bottom — the early-by measure is the PROTOTYPE's `(pred.due − start).days` (plain difference, no both-days +1 — pinned so the port does not inherit `link_overlap`'s convention): (`◂ waits on  ›‹title› · ‹title› (starts ‹n›d early)` / `▸ unblocks  ‹title› (starts ‹n›d early)` / `▸ unblocks  nothing waits on it`); the keys bar `x remove the › link · L link · ↵ open · ←→↑↓ move` (80: `x remove › · L link · ↵ open`) — every painted string escaped (S1) and clipped to its cell.
- **Rationale (informative):** the operator: "no veo si realmente eso está implementado"; round 7 checked C-2b.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q`
- **Numeric pass threshold:** TC-801 (the exact C-2b-118x30 rows on the base board), TC-802 (the exact C-2b-80x24 rows), TC-803 (the critical chain's structure: a greyscale-law arm — the heavy chain must differ from the light chains with the colour taken away), TC-804 (the header counts on BOTH boards — base `15 linked · ▲2 late · ━ chain 4`; milestones `17 linked`), TC-807 (an S1 hostile title renders escaped, the frame width holds).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the user presses `6` and reads who waits on whom, per project, with the ready/waits/late marks and the heavy critical chain; the strip names what the selection waits on and unblocks.
  - **Shipped surface:** key `6`, the painted view, the strip, the keys bar.
  - **Acceptance test(s):** AT-801
  - **Boundary catalog:** ☑ empty (a no-links project; a one-task chain) ☑ boundary (the deepest chain; the last column; the 24-row fold) ☑ invalid — none new ☑ error (a stored cycle renders once, no hang)
  - **Negative control:** AT-801's arm removing a link — the chain re-renders shorter.

### HLR-802 — The rule is visible and editable per chain
- **Traceability:** US-802
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2, LED-2026-10-07-batch-02.3, LED-2026-10-07-batch-02.4
- **Statement:** The chain map shall carry the per-band `dates` switch (the shipped storage's labels: stay ↔ `flag`, push ↔ `push_delta`, together ↔ `together` — the map pinned, never the raw stored string on screen), read leniently (absent or junk shows and behaves as `●push`); `m` on the chain map shall cycle the SELECTED TASK'S PROJECT rule (stay → push → together → stay), writing `extra["date_links"]`, saving, and refreshing the footer — wide (118): ` ▌‹project hue›‹project› · ‹LONG label› (default|set here): ‹explainer› · m change` — the LONG labels pinned verbatim: `Keep others, flag conflicts` (flag) · `Push what it collides with` (push_delta) · `Move the whole chain` (together) — the explainers pinned verbatim: flag `only the moved task moves; overlaps are flagged`, push_delta `a move pushes waiting tasks by the overlap it adds`, together `a move shifts every later task by the same days`; narrow (80): `▌‹label›: ‹short explainer› · m change for this chain`; a band whose stored rule differs from the default carries `set here` in its head at BOTH widths (the port source paints it whenever the rule is custom; at 80 the head may drop its trailing `· N open not linked` to fit, but keeps the marker and all three switch labels). On the chain map, `m` and `x` are view-dispatched: `m` is the rule cycle (the shipped global `m` = cascade_mode is inert on this view — no date move can top its undo stack there), `x` unlinks the selected task's incoming link (LLR-801.2).
- **Rationale (informative):** round-6 verdict; UXV-6's deferral; round 7's C-2b.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q -k chainmap_rule`
- **Numeric pass threshold:** TC-805 (the cycle: the switch shows `●push` by default; `m` cycles `○together ○stay ●push`; the written key is the STORED string; the `set here` marker appears on the deviating band at both widths; the footer wide form holds) and AT-802 (on the milestones board: set `together` for Data Warehouse, bump `td4` — `td0`/`td5` keep their gaps; set `stay`, the same bump moves nothing; a hand-edited `5` shows `●push` and behaves as `push_delta`, never raises).
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** the user sees `●push` on Website's band and knows what a move will do; `m` on a task cycles its project's rule, the band marks `set here`, the footer explains the active rule.
  - **Shipped surface:** the band switch, `m` on the chain map, the footer, `extra["date_links"]`.
  - **Acceptance test(s):** AT-802
  - **Boundary catalog:** ☑ empty (no key) ☑ boundary (the three exact values) ☑ invalid (junk) ☑ error — none new
  - **Negative control:** the junk arm.

### HLR-803 — The shipped high-band cap is pinned
- **Traceability:** US-803
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2
- **Statement:** The kanban's shipped high-band cap (LLR-306.1) shall be pinned by test: on a board with more open highs than fit, the band names what fits and carries the rest as `+N more ↓` per open-phase column, at 118×30 and 80×24; a band whose highs all fit shows no cap. No renderer change is owed — this is a characterization pin of `views.py:4641-4650,5024-5028`.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests -q -k high_band`
- **Numeric pass threshold:** AT-803's arms (the exact `+N more ↓` with N exact, at both sizes, on a fixture with more highs than fit; the all-fits negative control).
- **Priority:** medium
- **Acceptance (black-box):** **Observable outcome:** a crowded band says `+N more ↓` and names the rest nowhere. **Shipped surface:** the kanban band rule. **Acceptance test(s):** AT-803. **Boundary catalog:** ☑ boundary (exactly-fits vs one-over). **Negative control:** the all-fits arm.

### LLR-801.1 — The chain map renderer (the C-2b oracle)
- **Traceability:** HLR-801
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2, LED-2026-10-07-batch-02.3, LED-2026-10-07-batch-02.4, LED-2026-10-07-batch-02.5
- **Statement:** `views.py` shall provide the chain map renderer drawing the C-2b oracle frames byte-faithfully at 118×30 and 80×24 — per project the full-width band head (`─▌…── ○stay ●push ○together ─`; 118: `dates  ○ stay  ● push  ○ together` with the `set here` marker on a deviating band), the chains left to right by due with `──▸`/`┬▸`/`╰───╯` connectors and the meta row, the critical chain in `┃`/`━━▸┃` heavy bold structure (greyscale-separable from the light chains), the `no links` row, the header count, the selection strip, the keys bar and the legend row (`✓ done · ▷ ready · ◂N waits on N · ━ critical chain · ─ starts before due · ─ satisfied · ▲ late`; at 80 it sheds `─ satisfied`) — composing the views' own helpers, re-deriving from `variants_polish.py`'s `_dc2`/`strip2` (themselves deriving `variants_deps_gantt.render_dc`), every untrusted string escaped and clipped (S1), the frame fitting the screen at both sizes.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests -q -k chainmap`
- **Numeric pass threshold:** TC-801 (the exact C-2b-118x30 rows, base board), TC-802 (the exact C-2b-80x24 rows), TC-803 (the greyscale law + the fan-in join), TC-804 (the header counts on both boards), TC-807 (S1: a hostile title renders escaped, the width holds), TC-808 (a stored 2-cycle renders once, no hang).
- **Negative control:** removing a link re-renders the chain shorter.
- **Boundary catalog:** ☑ empty (no-links project; one-task chain) ☑ boundary (deepest chain; last column) ☑ error (the cycle arm)

### LLR-801.2 — The view wiring and the x/m view-dispatch
- **Traceability:** HLR-801
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2, LED-2026-10-07-batch-02.3, LED-2026-10-07-batch-02.5
- **Statement:** Key `6` shall open the chain map beside the shipped views: `Key("6", "6", "view('chainmap')", "Chains", primary=True, group="views")`; `VIEW_ORDER`, the key bar and the `?` map learn it (KEYBAR_BASE re-derived, executed); the arrows walk the chains in draw order; `↵` opens the shipped details; `L`'s `views=` tuple gains `"chainmap"` (keymap.py:79) so the picker lives here too. ON THE CHAIN MAP, view-dispatched inside the existing actions (no new global bindings): `x` routes to the shipped `unlink_tasks` seat — removing the selected task's FIRST incoming link — and, when the selection has none, refuses with the toast `nothing to remove — the selection waits on no task`; `m` routes to the rule cycle (LLR-802.1); the shipped archive/cascade meanings of `x`/`m` are inert on this view. The chain map's key bar row names the view's keys (`x remove the › link · L link · ↵ open · ←→↑↓ move` at 118).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests -q -k chainmap_app`
- **Numeric pass threshold:** AT-801: `6` paints the C-2b rows; arrows walk the chains; `↵` details; `x` on a linked task unlinks and the frame re-renders shorter; `x` on an unlinked task refuses verbatim; `L` links (the shipped picker).
- **Negative control:** the refusal arm.
- **Boundary catalog:** none beyond LLR-801.1's.

### LLR-802.1 — The per-chain switch and footer
- **Traceability:** HLR-802
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2, LED-2026-10-07-batch-02.3, LED-2026-10-07-batch-02.4, LED-2026-10-07-batch-02.5
- **Statement:** The band switch shall read `extra["date_links"]` through the shipped lenient read and render the LABELS (`○stay ●push ○together`; the stored strings never paint); `m` on the chain map cycles the selected task's project stay → push → together → stay, writes the STORED string to `extra["date_links"]`, saves, marks the band `set here` (both widths), and refreshes the footer to the selected chain's rule — wide form ` ▌‹hue›‹project› · ‹LONG label› (default|set here): ‹explainer› · m change` (LONG labels + explainers pinned verbatim in HLR-802) / narrow form `▌‹label›: ‹short› · m change for this chain`; the project editor and the kanban read the same key (unchanged).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests -q -k chainmap_rule`
- **Numeric pass threshold:** TC-805 (the cycle, the stored-string write, `set here`, the wide footer) and AT-802 (the milestones-board behavioral arms + the junk arm).
- **Negative control:** the junk arm.
- **Boundary catalog:** ☑ empty ☑ boundary ☑ invalid (junk).

### LLR-803.1 — The shipped cap, pinned
- **Traceability:** HLR-803
- **Ledger:** LED-2026-10-07-batch-02.1, LED-2026-10-07-batch-02.2
- **Statement:** No renderer change; the shipped cap (`views.py:4641-4650`) and its `+N more ↓` rendering (`views.py:5024-5028`) shall be pinned by AT-803 on a fixture with more open highs than fit, at 118×30 and 80×24, with N exact and the all-fits negative control.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests -q -k high_band`
- **Numeric pass threshold:** AT-803's arms.
- **Negative control:** the all-fits arm.
- **Boundary catalog:** ☑ boundary (exactly-fits vs one-over).

### Information Flow Contract (IFC)

Part A:

```
FLOW: the dependency web, from the board file to the chain map and back
  SOURCE : the board file on disk (depends_on, start_date, due_date, milestone, archived, phases, project extra); the user's keys
  NODES  :
    - fn    : the chain map renderer (chains, connectors, meta row, critical chain, band heads, legend, strip)
      owner : LLR-801.1
    - fn    : KEYMAP 6 / VIEW_ORDER / the key bar / nav on the chain map / x and L (the shipped link seats) / ↵ details
      owner : LLR-801.2
    - fn    : the band dates: switch / m on the chain map / extra["date_links"] (the shipped storage)
      owner : LLR-802.1
    - fn    : the kanban high-band cap
      owner : LLR-803.1
  SINK   : the painted chain map, the saved board file (the rule writes), the undo-less rule switch (a setting, not a move)
```

Part B: `no — no new addressable component.` (the switch lives in the band head row, not a widget address.)

## 5. Validation strategy

Layer A (`TC-801..TC-808`, unit, `tests/test_chainmap.py`) and Layer B (`AT-801..803`,
`tests/test_chainmap_app.py`) drive `TaskboardApp` with real keys over board files in
`tmp_path`. TWO fixtures: the BASE board (`kg_board.shifted` — the C-2b frames' own, 15
linked) pins the frame rows; the MILESTONES board (`kg_board.milestones(kg_board.shifted(...))`)
pins the rule arms (it alone carries `td0`/`td4`/`td5`) — the today argument is REQUIRED (kg_board.py:236-239). PER-ARM fixtures — the exact-row arms (TC-801/802, AT-801) run UNDER THE HOUSE FROZEN CALENDAR (the `frozen` monkeypatch of test_gantt_board.py, today = kg_board.TODAY) so the shifted board reproduces the frames' fixed dates byte-exact on any day: TC-801/TC-802 (the exact rows) run on the base board with `pdwh.extra["date_links"] = "together"` set IN-TEST — the frames' Data Warehouse is the deviating band (`●together` + `set here`); TC-803/804/807/808 run on the raw base board; TC-805/806 and AT-802 run on the milestones board; AT-801 runs on the frozen base board + in-test `pdwh="together"`; AT-803 builds its crowded fixture in-test (more open highs than fit at both sizes) and is RED by the §5.2 recorded-mutation route. TC↔arms: TC-801 the exact C-2b-118x30
rows (base) · TC-802 the exact C-2b-80x24 rows (base) · TC-803 the critical-chain greyscale law
+ the fan-in join · TC-804 the header counts on both boards · TC-805 the switch cycle, the
stored-string write, `set here`, the wide footer · TC-806 the junk arm · TC-807 the S1 hostile
title · TC-808 the stored cycle renders once.

### 5.2 Batch acceptance criteria
- every HLR has a passing AT; every LLR a passing TC; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures other than the declared G-011 flake.

## 6. Appendices (optional)

### 6.1 Extended glossary
### 6.2 Relevant design decisions
### 6.3 Open risks
### 6.4 Phase-1 reconciliation log — moved to the ledger (§7)

### 6.5 Requirement amendments — moved to the ledger (§7)

---

## 7. The ledger — authored as a SEPARATE FILE

The fence below is the ledger's seed: `devflow-init.py` writes it to `01-requirements-ledger.md`. The shape of an entry is in the field guide.

```markdown
# Requirements ledger — taskboard — Batch 2026-10-07-batch-02

> Append-only. Entries are added in chronological order and never rewritten. The live
> contract is `01-requirements.md`; this file records how it came to say what it says.
> Every entry names the requirement it amends; every requirement names its entries. `V26`
> compares the two sets of pairs both ways.

_No entries yet. The first amendment to the live contract writes the first one, in the
shape the field guide's §7 shows (`req-template.md` in the guide directory init prints), and nothing
above this line is ever edited._
```

# Requirements ledger — taskboard — Inc C, multicolour notes

> Append-only. Every entry names the requirements it amends one by one (V26: no ranges).

### LED-2026-11-01-incC.1 — the commission's C-1..C-3 made strict, with the failure paths it left open
- **Requirement:** HLR-4201
- **Requirement:** HLR-4202
- **Requirement:** HLR-4203
- **Requirement:** HLR-4205
- **Date:** 2026-11-01
- **What changed:** the commission text (C-1..C-4) was split into 55 single-`shall` LLRs. Added beyond its words, each as its own requirement: the one-space rule around markers (LLR-4201.2), so `a ::b:: x :: c` renders `a x c` and not `a  x  c`; an opener inside an open span ends that span (LLR-4201.6), so the hand-typed `::b:: x ::r:: y ::` renders two colours instead of a literal `r:: y ::`; the empty-span removal on lift and on save (LLR-4203.6, LLR-4203.11); `enter` under a pen continues the pen on the next line (LLR-4203.7), because a span never crosses a line; the pen turns off when the cursor leaves its span (LLR-4203.8); the palette's three refusals (LLR-4205.10, LLR-4205.11, LLR-4205.12) and the pen lift before the palette (LLR-4205.14); the label fit at 80x24 (LLR-4203.9). Self-check against 29148 split the compound LLR-4203.6 (lift or save) into LLR-4203.6 and LLR-4203.11.
- **Why:** each addition closes a path where the commission's literal text renders the operator's own syntax wrongly (double spaces, literal markers on line 2, an empty pair saved) or leaves a key with undefined behaviour.
- **Evidence:** `prototypes/capture_round/proto.py` EditorB/EditorC (the proto's `::` pen on enter left `::` literal on line 2; its label clipped `off` at 80x24, `out/png/col-B-ed_80x24.png`).

### LED-2026-11-01-incC.2 — the workspace keeps its one-theme highlight variables
- **Requirement:** LLR-4202.7
- **Date:** 2026-11-01
- **What changed:** LLR-4202.7 no longer asks for light-theme variables in the workspace; it asks for three `:root` variables used as `.hl-soon` uses `--soon`.
- **Why:** the baseline graph (E2) shows the workspace's light block does not redefine `--soon`, `--over` or `--green`; its highlights are 22 % background tints under the ink, so one variable each is the convention (rule 11: match the codebase).
- **Evidence:** `baseline-notes.md` "Design facts"; `taskboard/report_workspace.py:18-21, 84-86`.

### LED-2026-11-01-incC.3 — the E2 prototype's findings, ruled
- **Requirement:** HLR-4206
- **Requirement:** LLR-4201.7
- **Requirement:** LLR-4203.2
- **Requirement:** LLR-4203.7
- **Requirement:** LLR-4203.12
- **Requirement:** LLR-4203.13
- **Requirement:** LLR-4203.14
- **Requirement:** LLR-4203.15
- **Requirement:** LLR-4204.1
- **Requirement:** LLR-4204.2
- **Requirement:** LLR-4205.7
- **Requirement:** LLR-4205.8
- **Requirement:** LLR-4205.11
- **Requirement:** LLR-4205.12
- **Requirement:** LLR-4205.13
- **Requirement:** LLR-4205.15
- **Requirement:** LLR-4205.16
- **Date:** 2026-11-01
- **What changed:** reworded HLR-4206, LLR-4201.7, LLR-4203.2, LLR-4203.7, LLR-4204.1, LLR-4204.2, LLR-4205.7, LLR-4205.8, LLR-4205.11, LLR-4205.12, LLR-4205.13; added LLR-4203.12, LLR-4203.13, LLR-4203.14, LLR-4203.15, LLR-4205.15, LLR-4205.16 (55 → 61 LLRs).
- **Why:** the prototype groups' findings P-V-2, P-V-3, P-M1-1..5, P-M1-8, P-M2-1..4, P-M2-6, P-M2-9 — each ruling in `03-pdr-rulings.md` round 0.
- **Evidence:** `graph-proto-V.cw.md`, `graph-proto-M1.cw.md`, `graph-proto-M2.cw.md` (`## Findings`).

### LED-2026-11-01-incC.4 — the PDR round 1, ruled
- **Requirement:** LLR-4201.10
- **Requirement:** LLR-4203.16
- **Requirement:** LLR-4203.17
- **Requirement:** LLR-4204.7
- **Requirement:** LLR-4204.8
- **Requirement:** LLR-4204.9
- **Date:** 2026-11-01
- **What changed:** added LLR-4201.10, LLR-4203.16, LLR-4203.17, LLR-4204.7, LLR-4204.8, LLR-4204.9 (61 → 67); the AT-4201 and AT-4202 key scripts corrected (ARCH-6).
- **Why:** ARCH-1 (alt+digit arrives as Option glyphs under Windows Terminal 1.24 without the kitty protocol), SEC-1 (quadratic scan), SEC-2 (a pen insert fusing with neighbours), SEC-3 (private-API fail-safe), SEC-6 (lone surrogate).
- **Evidence:** `03-pdr-architect.md`, `03-pdr-security.md`, `evidence/wt-kitty-query.log`; rulings in `03-pdr-rulings.md` round 1.

### LED-2026-11-01-incC.5 — a lone surrogate: no ink rather than one more private override
- **Requirement:** LLR-4204.9
- **Date:** 2026-11-01
- **What changed:** the threshold no longer asks for `x` in blue; the editor opens and accepts typing with no ink.
- **Why:** Textual 8.2.8 `TextArea._render_line` encodes each visible line strictly whenever any highlight exists (the correction agent ran it: UnicodeEncodeError). Painting would need an override of `_render_line`, a fourth private name; prefer removing the feature over guarding it.
- **Evidence:** correction pass round 1 report; `03-pdr-rulings.md` round 1 addendum R1-1.

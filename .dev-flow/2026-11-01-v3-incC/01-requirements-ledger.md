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

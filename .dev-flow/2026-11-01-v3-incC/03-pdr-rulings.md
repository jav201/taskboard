# Inc C — rulings (orchestrator, Opus)

> Every proposal from the prototype groups (E2) and the design review (E3) gets one ruling here.
> Bias: prefer removing a feature over guarding it. Ids: P-V-n, P-M1-n, P-M2-n (E2), then the PDR ids.

## Round 0 — E2 prototype findings and seams (2026-11-01)

| Id | Proposal | Ruling | Applied in |
|---|---|---|---|
| P-V-1 | orange sits 51 RGB from `soon` (inside the retired band); b/v are also project hues | **Keep** `HEX["orange"]`, `blue`, `violet` for note text. The palette-ration bands govern *project* hues on the board; a note tone is read with its name in the legend/pen chip, and the 256-colour numbers stay distinct (209 vs 214). No new HEX key. | rulings only |
| P-V-2 | LLR-4201.7 contradicts LLR-4201.6 | **Accept.** LLR-4201.7 reworded: markers inside a legacy span, and legacy markers inside a colour span, stay literal. | 01-requirements, LED.3 |
| P-V-3 | HLR-4206 says 0.15, LLR says 0.20 | **Accept.** HLR text: 0.15 is the cliff, 0.20 the gate. | 01-requirements, LED.3 |
| P-V-4 | `::b:: std::vector ::` closes at `std::` | **Accept as designed**; pinned by TC-4227; README sentence. | graph V, README |
| P-V-5 | TC-4213/4215 used by the interface file | **Rename** the interface's `_lift_pen` examples to TC-4258, TC-4259 (M1 range, free). | graph-interfaces |
| P-V-6 | focus legend shows syntax whenever a task is pinned | **Backlog** (base behaviour, not this increment). | BACKLOG |
| P-V-7 | focus snippet clips the raw line (markers eat width) | **Backlog.** | BACKLOG |
| P-M1-1 | ink should paint legacy spans too | **Accept.** LLR-4204.1/.2 say "span" (colour or legacy). | 01-requirements, LED.3 |
| P-M1-2 | enter gate = "picker offers no pick" | **Accept.** LLR-4203.7 reworded. | 01-requirements, LED.3 |
| P-M1-3 | `alt+n` inside an existing span or over a selection corrupts | **Remove the case:** if the pen is off and the cursor is inside a span (start < col < end) or the selection is non-empty, `alt+n` inserts nothing and notifies `Pens write new text — use alt+c to recolour.` New LLR-4203.12 (inside a span), LLR-4203.13 (selection). No "continue in span" feature. | 01-requirements, graph M1 |
| P-M1-4 | leaving an empty pen span leaves `::y::  ::` | **Accept.** New LLR-4203.14. | 01-requirements, graph M1 |
| P-M1-5 | typing `::` under a pen closes the span | **Accept as designed**; LLR-4203.2 states the exception; README sentence. | 01-requirements |
| P-M1-6 | the column is 39, not 37 | **Accept** (measured from tcss). Narrow form ≤ 38. | graph M1 |
| P-M1-7 | live ink rests on 3 Textual privates | **Accept guard tests** (one test that fails if `TextArea._build_highlight_map`/`_highlights`/`_line_cache` change shape). Pinning Textual in pyproject → **backlog** (out of scope). | tests, BACKLOG |
| P-M1-8 | same pen key while that pen is on | **Accept:** changes nothing. New LLR-4203.15. | 01-requirements |
| P-M1-9 | enter at the inner start moves the whole span down | **Reject** (special case for a cosmetic empty span; the general LLR-4203.7 path is enough). Remove the `col == s.inner_start` branch from `action_pen_enter`. | graph M1 |
| P-M1-10 | `_lift_pen` uses `_pen_span`; no span → only pen=None | **Accept.** | graph-interfaces |
| P-M2-1 | a selection holding a whole span plus other text | **Accept:** LLR-4205.11 → "overlaps a span without lying inside it" (refuse). | 01-requirements, LED.3 |
| P-M2-2 | rewrite that would change the visible text (`std::vector`, `==a::b==`) | **Accept** as a single invariant check: if the visible text (joined segments) of the line after the rewrite differs from before, change nothing and notify. New LLR-4205.15. | 01-requirements, graph M2 |
| P-M2-3 | a whitespace-only selection = nothing to colour | **Accept** (LLR-4205.12 amended). | 01-requirements |
| P-M2-4 | "unchanged" reference point | **Accept:** compared with the notes at the moment the palette opened (after the lift). LLR-4205.7/.8 amended. | 01-requirements |
| P-M2-5 | details label: drop the legacy listing | **Accept.** The label lists the six codes only; legacy notes still render. | graph M2 |
| P-M2-6 | M1 and M2 both edit `check_action` | **Accept:** `TaskModal.check_action` moves into graph-interfaces with ONE notes-focus gate for `pen`, `pen_enter`, `colour`. New LLR-4205.16 (alt+c without notes focus changes nothing). | graph-interfaces |
| P-M2-7 | example `"a:::b:: plan ::"` | **Accept.** | graph V |
| P-M2-8 | unlisted palette keys do nothing; recolour inside a span recolours the whole span | **Accept as decisions.** | rulings only |
| P-M2-9 | measure for "next to the target" | **Accept:** box top row = anchor row + 1, or box bottom row = anchor row − 1 when it would not fit below. LLR-4205.13 amended. | 01-requirements |

**Seams fixed by the orchestrator (graph-interfaces.cw.md):** `colour_spans`, `Span`, `PEN_CODES` (V → M1, M2);
`_lift_pen` and `_pen_span` (M1 → M2); `TaskModal.check_action` (shared, one gate); the Notes label carries
`alt+c` (M1 renders, M2's key).

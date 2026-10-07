# CHUNK A (product) — DeepSeek V4 Pro — increment 001, batch 2026-10-07-batch-02 — THE CHAIN MAP

You are the software-dev implementer for the PRODUCT half of increment 001 in
`C:/Users/jjgh8/Github/taskboard` (Textual TUI; 2514 pytest tests green). A second agent
writes TESTS only; you must NOT touch anything under `tests/`.

## READ FIRST (in order)
1. `.dev-flow/2026-10-07-batch-02/01-requirements.md` — HLR-801/802/803 and LLR-801.1/.2/802.1/803.1 are your contract. The pinned literals are §-exact against the oracle frames.
2. `.dev-flow/2026-10-07-batch-02/evidence/frames/C-2b-118x30.txt` and `C-2b-80x24.txt` — THE LAW: the view's exact rows at both sizes (byte-faithful reproduction is the bar).
3. The port source: `C:/Users/jjgh8/Github/taskboard/.claude/worktrees/kg-mejoras/prototypes/kg_mejoras/variants_polish.py` — `_dc2` (the C-2b chain-map renderer, ~line 538; renders exactly these frames), `_switch2` (~504), `_tile` (~691), `render_c2b` (~741) — RE-DERIVE its logic into `taskboard/views.py` using the SHIPPED helpers (the prototype's own `strip2`/`_dc2` copies and its private axis are re-derived, not pasted).
4. The shipped seats: `taskboard/keymap.py` (KEYMAP — `6` is free; `L`'s `views=` tuple at :79 gains `"chainmap"`; the view-dispatch decision in the contract), `taskboard/app.py` (`VIEW_ORDER` :52, `action_view`, the `unlink_tasks` seat :1020, `action_archive`/`action_cascade_mode` are the dispatch hosts), `taskboard/models.py` (`resolve_mode` :1896 — the lenient read; `critical_chain` :1396).

## THE WORK
1. **The renderer (LLR-801.1)**: `views.py` gains the chain map renderer composing shipped
   helpers — the header, the full-width band heads with the `dates` switch (118 spaced
   `dates  ○ stay  ● push  ○ together`; 80 compact `○stay ●push ○together`; `set here` on a
   deviating band at BOTH widths), the chains (`──▸`/`┬▸`/`╰───╯`; the critical chain in
   heavy `┃`/`━━▸┃` bold structure), the meta row (`✓`/`▷ ready`/`○` open-chain-head/`◂N`/`Mon D`/`▲Nd`),
   the `no links` full-width head, the legend, the selection strip (early-by measure =
   `(pred.due − start).days` — the prototype's plain difference, NOT link_overlap's +1), the
   keys bar — fitting the screen at 118×30 and 80×24, every untrusted string escaped+clipped.
   Also `legend_entries("chainmap", …)` and `help_usage("chainmap")` entries per the contract.
2. **The wiring (LLR-801.2)**: `Key("6", "6", "view('chainmap')", "Chains", primary=True,
   group="views")`; `VIEW_ORDER` gains the view; `L`'s views= gains `"chainmap"`; the
   view-dispatch: on `view_mode == "chainmap"`, `x` routes to `unlink_tasks` (refusing with
   the contract's verbatim literal `nothing to remove — the selection waits on no task` when
   the selection has no incoming link) and `m` routes to the rule cycle (LLR-802.1: cycle the
   SELECTED TASK'S PROJECT rule stay → push → together → stay via the labels↔stored map
   stay↔flag/push↔push_delta/together↔together, write `extra["date_links"]`, save, refresh
   the footer per the contract's wide/narrow forms with the verbatim LONG labels and
   explainers); the shipped archive/cascade meanings stay inert on this view. `↵` opens the
   shipped details; arrows walk the chains.
3. **HLR-803 needs NO renderer change** — skip it (the cap ships; the tests pin it).

## DISCIPLINE
- NO git mutations. Files: `taskboard/views.py`, `taskboard/app.py`, `taskboard/keymap.py` ONLY.
- Run the FULL suite: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests -q` — it must end 2514 passed (the new tests arrive from the other agent AFTER you; if `tests/test_chainmap*.py` appears mid-run, expect +N nodes). The KEYBAR_BASE census in tests/test_colour_budget_app.py will RED when `6` lands — that is EXPECTED and the tests agent's problem, not yours; do NOT edit tests.
- English comments in the shipped voice.

## REPORT BACK
What changed per file (file:line), the final suite count, any deviation from the contract.

# CHUNK — DeepSeek V4 Pro — increment 001 of batch 2026-10-07-batch-04 (batch E, the present-e worktree)

You implement batch E of the kg_mejoras plan in the worktree at
`C:/Users/jjgh8/Github/taskboard/.claude/worktrees/present-e` ONLY (never the main checkout).
The OPERATOR'S VERDICT on the prototype (prototypes/present_e/veredicto-present.json):
**PRES-C** — one interactive surface; **export SVG and PNG**; **`R` replaces the report**.

## READ FIRST
- The contract: `.dev-flow/2026-10-07-batch-04/01-requirements.md` (HLR-1001/LLR-1001.1/.2 —
  the prototype's PRES-C frames are the oracle: `prototypes/present_e/out/PRES-C-118x30.txt`,
  `PRES-C-80x24.txt`).
- The prototype: `prototypes/present_e/build.py` (the port source — RE-DERIVE, do not paste).

## THE WORK — `taskboard/views.py`, `taskboard/app.py`, `taskboard/keymap.py` ONLY. No tests (a parallel agent may land them; if `tests/test_present*.py` appears, keep it green). No git.

1. **LLR-1001.1 — the presentation view behind `R`**: `action_report` (app.py) currently runs
   the HTML report — REPLACE its seat with the presentation mode (the verdict: the
   presentation REPLACES the report): a new full-screen surface rendering PRES-C — the
   project's gantt field on top, the brief blocks below (title, dates, phase, the notes
   paragraph wrapped, the links line), a `⟦━⟧` cursor across the brief blocks (`←`/`→` move,
   the cursor'd task's notes expand, `↑`/`↓` move across the gantt rows), `esc` leaving. The
   project: the selected task's project (or the focused one). Byte-faithful to the PRES-C
   oracle frames at 118×30 and 80×24 (the C-2b budget: accent = the cursor only; today =
   bright; every untrusted string escaped+clipped — S1).
2. **LLR-1001.2 — the export**: the presentation exports what it shows — the shipped `R`
   report's SVG path (rich `export_svg`) AND a PNG. Textual's save_screenshot writes SVG only;
   for the PNG rasterize the SVG with the installed headless Edge:
   `msedge --headless=new --disable-gpu --screenshot=<out.png> --window-size=<W*10>,<H*20> file:///<out.svg>`
   (resolve the msedge path from the standard locations or shutil.which; run with a short
   timeout, capture the exit code). If Edge is absent, the export toasts that PNG needs Edge
   and still writes the SVG — never crash. Do NOT read site-packages to research this (the
   sandbox refuses external directories); the answer is HERE.
   The key bar or the surface names the export key (keep it simple: one key, both formats to
   the shipped report's destination convention).
3. **The README + keymap**: `R`'s README row and tooltip change to the presentation; the key
   bar census entries re-derive (a tests agent owns the test side — name any census test your
   change reddens in your report).

## DISCIPLINE
- Verify: `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest tests -q` (from the worktree) — the suite must stay green except any census RED you name. Also render the new view through the real app at 118×30 and 80×24 and diff the text against the PRES-C oracle frames (report the diff result).
- English comments, shipped voice.

## REPORT BACK
Per LLR: what changed (file:line), the oracle diff result, the suite counts, any census RED named.

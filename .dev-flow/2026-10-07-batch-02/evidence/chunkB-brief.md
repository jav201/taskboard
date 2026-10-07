# CHUNK B (tests) — DeepSeek V4.1 Flash — increment 001, batch 2026-10-07-batch-02

You are the test author for the TESTS half of increment 001 in
`C:/Users/jjgh8/Github/taskboard`. A second agent implements the PRODUCT
(`taskboard/views.py`, `app.py`, `keymap.py`) in parallel — you must NOT touch anything
outside `tests/`. Write the tests against THE CONTRACT (the exact pinned literals); they go
RED now (no chainmap code) and GREEN when the product lands.

## READ FIRST
`.dev-flow/2026-10-07-batch-02/01-requirements.md` (§5 names every arm and its fixture) and
the oracle frames `.dev-flow/2026-10-07-batch-02/evidence/frames/C-2b-118x30.txt` /
`C-2b-80x24.txt` — your expected rows come from THESE bytes. The house idioms:
`tests/test_cascade_app.py` (app driving: run_test, real keys, toasts) and
`tests/test_gantt_board.py:65-76` (the `frozen` calendar fixture — REQUIRED for the
exact-row arms so the shifted board reproduces the frames' fixed dates: freeze today to
`kg_board.TODAY`).

## YOUR FILES (new, both)
- `tests/test_chainmap.py` — the unit layer.
- `tests/test_chainmap_app.py` — the app layer.

## THE TESTS (ids in docstring + name, matching §5's ownership)

`tests/test_chainmap.py` (render against `views` directly; freeze the calendar):
- TC-801: on the BASE board (`kg_board.shifted`, frozen today) with
  `pdwh.extra["date_links"] = "together"` set in-test, the rendered frame at 118×30 equals
  the `C-2b-118x30.txt` bytes (compare the painted text line by line).
- TC-802: same board at 80×24 equals `C-2b-80x24.txt`.
- TC-803: the critical chain differs from the light chains with the colour taken away
  (greyscale-law: compare the stripped-text styles — hue must not be the only channel), and
  the fan-in join renders.
- TC-804: the header counts — base board `15 linked tasks`; the milestones board
  (`kg_board.milestones(kg_board.shifted(...), date.today())`) `17 linked tasks`.
- TC-807: an S1 hostile title (`[bold]x[/bold]` and a lone `[/]`) renders escaped, the frame
  width holds.
- TC-808: a stored 2-cycle (`kg_board.legacy`'s L7a/L7b shape, or an in-test pair) renders
  once — no hang.

`tests/test_chainmap_app.py` (drive `TaskboardApp` with real keys):
- AT-801: `6` paints the C-2b rows (frozen base + in-test pdwh together); the arrows walk
  the chains in draw order; `↵` opens the details; `x` on a linked task unlinks and the
  frame re-renders shorter; `x` on an unlinked task refuses with the verbatim toast
  `nothing to remove — the selection waits on no task`.
- AT-802: on the milestones board — the band switch shows `●push` by default; `m` cycles
  `○together ○stay ●push`; the written `extra["date_links"]` is the STORED string
  (`flag`/`push_delta`/`together`); with Data Warehouse `together`, a `+` bump on `td4`
  moves `td0` and `td5` keeping gaps; set `stay` — the same bump moves nothing; a
  hand-edited `"date_links": 5` loads showing `●push` and behaves as `push_delta`, never
  raises.
- AT-803: the shipped high-band cap — build an in-test board with more open highs than fit
  (mutate priorities on the kg base), assert the exact `+N more ↓` at 118×30 and 80×24
  with N exact, and an all-fits band shows no cap.

## DISCIPLINE
- NO git mutations. `tests/` only. Env for every run:
  `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor PYTHONIOENCODING=utf-8 python -m pytest ...`
  Expect RED until the product lands; report the RED transcripts (they are the counterfactual).
- English, matching the house style.

## REPORT BACK
The file list + test ids, the RED transcripts' failing assertions, the green counts once the
product lands (or your last state if it has not).

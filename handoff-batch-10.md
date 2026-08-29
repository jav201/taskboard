# HANDOFF — taskboard batch-10: continuar con /dev-flow (Phase 3 en adelante)

**For:** the agent implementing batch-10. **Status:** Phases 0-2 DONE and
committed (`3fb23a6`, tree clean). Next: **Phase 3, increment 1**. Resume by
reading `.dev-flow/state.json` (`current_phase: 2`, `phase_status: complete`)
and the batch plan `.dev-flow/2026-08-24-batch-10/PLAN.md` — Phase 1 has the
requirements (HLR/AT per story), Phase 2 has the folded review (7 blockers,
all mechanisms specified). **This document is the operational summary; the
PLAN is the spec of record — where they disagree, the PLAN wins.**

## Batch objective

Cuantificar el MOVIMIENTO del trabajo (hoy solo se cuantifica carga):

- **US-A** — transitions log append-only en `<board_dir>/history.jsonl`.
- **US-B** — vista de flujo (tecla `7`): ciclo mediano por fase, heatmap
  fase×semana, throughput semanal.
- **US-D** — inteligencia de dependencias: bloquear una tarea pregunta
  "What blocks it?" y el bloqueante se vuelve tarea enlazada (`depends_on`),
  token `⛓N`, sort kanban `unblock`, cadena crítica en gantt.
- **US-C (desk loop) NO está en este batch** (cross-repo, batch aparte).

## Authorization (state.json.standing_authorization)

Autonomous end-to-end within this scope · **commits authorized per increment**
· **push requires an explicit operator order** · decisions recorded in
PLAN.md decision log + state.json.decisions_log · artifacts in English,
UI strings in English (the app's register).

## Verification law of this repo (binds every increment)

- Full suite green: `python -m pytest tests/ -q` (880 passed at batch open).
  `tests/test_app.py::test_win_clipboard_roundtrip` is an intermittent
  environmental flake — if it fails, re-run it alone once and report; it is
  NOT a batch signal.
- **Mutation evidence, executed not argued:** every increment runs its ATs'
  RED arms (temporary edits to the new code, one at a time, restore exactly),
  and pastes the transcript into the increment report in PLAN.md.
- Repo conventions: docstrings carry the WHY; deterministic tests
  (tmp_path-rooted boards, injected `today`); no prints; no new deps;
  width measured in cells (`rich.cells.cell_len`), never `len()`.

---

## Increment 1 — US-A: transitions log

1. New module `taskboard/history.py` (discipline of desk's append_journal /
   read_journal — never raises; silent loss is worse than a visible error):
   - `HISTORY_ERROR: str | None` module global.
   - `history_path(board_path) -> Path` — sibling `history.jsonl`.
   - `append(board_path, record, at: datetime | None = None) -> dict | None`
     — fills `at` (ISO, timespec="seconds") when absent; does its own
     `mkdir(parents=True, exist_ok=True)`; appends one JSON line; on OSError
     sets `HISTORY_ERROR` (`f"{type}: {exc}"`) and returns None; clears on
     success. NEVER raises.
   - `read(board_path) -> tuple[list[dict], int]` — (records, skipped).
     Missing file → `([], 0)`; a line that is invalid JSON OR valid-JSON-
     wrong-shape (not a dict, or wrong/missing `task`:str / `from`:str|None /
     `to`:str / `at`:str) is skipped and counted.
2. Hooks in `taskboard/models.py` (ONE seat, do NOT hook app.py actions):
   - `Board.set_task_phase` (models.py:1089) — on the actual-move path
     (`return True`): append `{"task": task.id, "from": old, "to": phase}`.
   - `Board.add_task` (models.py:1103) — append creation record
     `{"task": task.id, "from": None, "to": task.phase}`.
3. App error surface (app.py): after the phase-move action (~app.py:500) and
   the edit-modal save (~app.py:837): if `history.HISTORY_ERROR` holds a NEW
   message (track last-notified on the app), `self.notify(...,
   severity="warning")`; leave the global in place.
4. Tests `tests/test_history.py` (tmp_path boards ONLY — the hook writes
   beside the board file, so never the relative `_UNWRITTEN` path):
   - AT-A1 app-level (pilot, pattern of tests/test_app.py:1241-1352):
     phase-move key press appends EXACTLY ONE line (task/from/to/at; `at`
     parses). Fixture task must start mid-board (the move clamps to no-op at
     the ends).
   - AT-A2 `add_task` → `from` None.
   - AT-A3 a DIRECTORY at the history path (portable unwritable on Windows)
     → move still returns True, board saves, no exception, HISTORY_ERROR
     set; notify fires (mock).
   - AT-A4 file with 2 good + 1 invalid-JSON + 1 wrong-shape (`{"task": 1}`)
     lines → 2 records, skipped == 2.
   - RED arms to execute: kill the append / raise-instead-of-swallow / drop
     the skip counter.
5. Commit: `batch-10 inc-1: transitions log (history.py) hooked into
   set_task_phase/add_task`.

## Increment 2 — US-B: flow view (key `7`)

1. `render_flow` in `taskboard/views.py`, `today` injected everywhere:
   - **Intervals:** pair each task's records ordered by `at` (a record with
     `to=P` opens an interval in P; the task's next record closes it; an
     unclosed interval closes at "now").
   - **Cycle time (HLR-B1):** median whole days (date diff of `at`) per phase
     over CLOSED intervals; even-n median renders one decimal (`2.5d`);
     phases with only open intervals render `en curso n=N`, never a number.
   - **Heatmap (HLR-B2):** rows = phases, cols = last 8 ISO weeks (current
     rightmost), cell = task-days in that phase that week, block ramp
     `░▒▓█`.
   - **Throughput (HLR-B3):** records whose `to` == the CURRENT terminal
     phase, per week, 8 weeks, mini bar strip + total (re-completions count;
     pre-phase-edit history is approximate — documented semantics).
   - **Empty (HLR-B4):** no history → the body says ONLY
     "sin historia aún — se construye desde hoy" (no metric glyphs);
     n=1 transition → renders, no division by zero.
   - Phase labels are UNTRUSTED (hand-editable file) → escape / intersect
     with `board.phases` at render.
2. Plumbing (Phase-2 fold #6 — every branch explicit, no fallbacks):
   `RENDERERS["flow"]` + explicit `render_view` branch · `nav_model` branch
   returning NO selectable rows · `VIEW_ORDER` ·
   `Key("7", "7", "view('flow')", "Flujo", group="views")` in keymap.py
   (keys 1-6 taken) · aperture handles/swallows 7 (aperture.py:51) ·
   `legend_entries("flow")` is STATE-AWARE (empty-history render paints no
   ramp — the legend may not claim swatches the view doesn't show).
3. Tests `tests/test_flow_view.py`: AT-B1 fixture history with known
   intervals → the three artifacts carry the computed values (transcript
   executed and pasted into the increment report, fixture titles only);
   AT-B2 empty-history sentence + no ramp glyphs in the body; AT-B3 pins
   "en curso n=1"; AT-B4 width sweep cell-exact (1..120) + keymap contains
   key 7 → `view('flow')`.
4. Commit: `batch-10 inc-2: flow view (key 7) — cycle time, phase×week
   heatmap, weekly throughput`.

## Increment 3 — US-D part 1: block→task + ⛓N + unblock sort

1. **Block flow** (rework `action_toggle_blocked`, app.py:515):
   - Blocking with candidates → modal "What blocks it?" (create new task /
     pick existing; inherit TextPrompt/ConfirmModal escaping; the picker
     escapes titles). At COMMIT time (inside the callback — a cancelled
     prompt leaves no snapshot): snapshot onto the undo stack with
     `depends_on` as a COPY; set `blocked=True` and reassign
     `task.depends_on = [*task.depends_on, blocker_id]`.
   - Unblocking → flips without asking (snapshot as today).
   - No candidates (single-task board) → plain flip, no prompt.
   - `_UNDO_FIELDS` (app.py:544) gains `"depends_on"` — stored as a copy;
     undo restores `blocked` + `depends_on`; the created blocker PERSISTS
     (modal adds record nothing — AMD-05).
   - DECLARED test rewrites (behavior change approved at intake):
     `tests/test_app.py:2408` (instant-flip pin) and `:3797` (undo LIFO).
2. **⛓N token** (`card_cell`, views.py:305): `unblocks_count(board, task)` —
   pure module-level helper in models.py (edges over KNOWN task ids only;
   done tasks don't count; cycle-safe). Indicator order becomes
   `[↗ ! ▤ ·Nd +Nd ⛓N ▣]` — SUPERSEDES the countdown's "only ▣ sheds later"
   comment: update card_cell's docstring (views.py:309), the countdown
   comment (views.py:347-352), and the test docstring
   (tests/test_cells.py:326) in the same increment. Bare `⛓` U+26D3 WITHOUT
   VS16 (`cell_len("⛓")==1`; with VS16 it's 2). Compute counts once per
   render pass, not per card (O(tasks²) trap).
3. **`unblock` sort** — explicit branch in BOTH `kanban_order`
   (views.py:3457 `else:"due"` trap) AND `_kanban_cell_order`
   (views.py:3637) — renderer/nav parity (F-3 law). Order: unblocks
   descending, blocked tasks SINK, ties stable. Add `"unblock"` to the cycle
   (app.py:713) + docstrings.
4. Tests: AT-D1 (block flow wires depends_on+blocked, undo restores both,
   blocker persists); AT-D2 (⛓ absent at 0, `⛓2` at 2, width sweep with the
   token); AT-D3 (fixture whose unblock order is DISTINCT from
   project/priority/due/recent — assert distinctness FIRST, the
   palindrome-fixture law).
5. Commit: `batch-10 inc-3: block-becomes-task flow + ⛓N + unblock sort`.

## Increment 4 — US-D part 2: gantt critical chain

1. Longest `depends_on` chain among open tasks: edges over known ids only,
   dangling ignored, visited-set cycle safety (hand-edited A↔B cannot hang
   the render).
2. Render (zero layout change — reviewer-verified mechanism): the existing
   3-cell `└─►` seat (views.py:2515, 2547) toned ACCENT for chain members +
   header suffix `· cadena crítica N` (views.py:2436). Bars may wear accent
   only (test_gantt.py:128-130 law). Guard `if chain:` → byte-identical
   render with no deps.
3. Tests AT-D4: a 3-long chain highlights exactly those 3 (adopt the
   assert-worn idiom of test_gantt.py:115); no-deps render byte-identical.
4. Commit: `batch-10 inc-4: gantt critical chain`.

## Phase 4-6 — close

- Phase 4 validation: full suite + per-AT verification table + the mutation
  transcripts collected per increment; update `04-validation.md`-style
  section in the batch PLAN.
- Phase 5 postmortem: working-file reconciliation (C-44 — `git status
  --short` in taskboard; every touched file lands in exactly one terminal
  state: committed / reverted / recorded in BACKLOG.md) + lessons.
- Phase 6 docs: refresh `.dev-flow/BACKLOG.md` (base ref, carries), README
  if the keymap surface changed (key 7, unblock sort).
- **Push: ONLY on explicit operator order.**

## Watch-items (declared in PLAN §Risks)

- Flow view must be useful with n=1 and honest with n=0 history.
- ⛓N tightens card_cell's budget — shed order is pinned above.
- The critical chain must not break "one color = one work": accent only,
  never project hues, never over/soon on bars.

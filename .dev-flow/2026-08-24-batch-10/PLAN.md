# PLAN — 2026-08-24-batch-10 · taskboard: cuantificar el MOVIMIENTO del trabajo

**Batch objective.** Tres historias locales a taskboard: **US-A** log append-only
de transiciones de fase (`~/.taskboard/history.jsonl`) · **US-B** vista de flujo
derivada del log (ciclo por fase, heatmap fase×semana, throughput semanal) ·
**US-D** inteligencia de dependencias (bloqueo → tarea bloqueante enlazada, token
⛓N, orden unblock-first, cadena crítica en gantt). El desk loop (US-C) queda para
su propio batch por ser cross-repo (decisión del operador).

**Mode:** `core`. Language: `en` (artefactos) / `es` (conversación).

## Verified at intake

- **Base-currency (RC-1):** `git fetch origin` → merge-base == `origin/main` tip
  == `b56d9d5` (el fix del countdown kanban, pusheado hoy). No stale tree.
- **Suite green:** 880 passed (`test_win_clipboard_roundtrip` flake ambiental
  pre-existente, reproducido en árbol limpio; se excluye por convención).
- **Already-shipped check:** `git grep velocity/throughput origin/main` → solo
  negaciones documentadas (`views.py:2054` "We store no phase-transition
  timestamps, so a velocity/ETA is not...", `report.py` "No velocity, no
  forecast"). `depends_on` solo rinde como glifo mudo `└─►` (views.py:2515,
  2547). Nada de este batch está ya shipped.
- **Backlog leído** (`.dev-flow/BACKLOG.md`): carries abiertos (chrome census,
  pulse ration UI, PULSE_PHASES) — ninguno colisiona con estas historias.
- **Integration point verificado para batch futuro (US-C):** desk journal =
  `~/.desk/pomodoros.jsonl`, append-only, `read_journal()` never-raises; el
  registro actual `{started_at, ended_at, seconds, outcome}` NO tiene task_id
  (desk necesitaría un campo opcional — por eso C es batch aparte).

## Operator decisions at intake

| pregunta | decisión |
|---|---|
| Empaque | batch-10 = US-A + US-B + US-D; US-C (desk loop) batch aparte |
| Ubicación del log | sidecar `~/.taskboard/history.jsonl`, append-only, junto a board.json |
| Autorización | autónomo + commits autorizados por incremento; **push sigue a la orden** |

## Stories — INVEST

| id | story | status | observable outcome |
|---|---|---|---|
| US-A | **Log de transiciones.** Como operador quiero que cada cambio de fase de una tarea quede registrado (tarea, origen, destino, fecha ISO) en `history.jsonl` append-only, para cuantificar el movimiento del trabajo. | READY | Mover una tarea de fase agrega una línea con los 4 campos; board sin historia funciona idéntico; una línea corrupta no tumba la lectura (never-raises, patrón `read_journal` de desk). |
| US-B | **Vista de flujo.** Como operador quiero una vista con ciclo mediano por fase, heatmap fase×semana de dónde envejece el trabajo, y throughput semanal — derivados del log — para ver dónde se atora el trabajo. | DONE | Nueva vista (tecla 7) renderiza los tres artefactos desde el log; board sin historia declara "sin historia aún — se construye desde hoy" (empty state que nombra su origen); todo número derivado de fixtures ejecutados. |
| US-D | **Dependencias inteligentes.** Como operador quiero que al bloquear una tarea me pregunte qué la bloquea y eso se vuelva una tarea enlazada (`depends_on`), ver qué desbloquea cada tarea (`⛓N`), ordenar unblock-first, y ver la cadena crítica en gantt. | READY | `b` sobre una tarea ofrece crear/enlazar el bloqueante; las tarjetas muestran `⛓N` (N = tareas que desbloquea); nuevo sort `unblock` en kanban; gantt resalta la cadena de dependencias más larga. |

Sin historias REFINE/SPIKE/OUT en este batch — las tres cierran los tres ejes
(funcionalidad, factibilidad, evaluabilidad) con las decisiones de intake.

## Increment plan (merit order: el dato primero, luego lo que lo lee)

| inc | content | source files |
|---|---|---|
| 1 | US-A: `history.py` (append + read never-raises, `Transition` record), hook en las mutaciones de fase (`app.py`), helper en `models.py`. | `taskboard/history.py` (nuevo), `taskboard/app.py`, `taskboard/models.py` |
| 2 | US-B: `render_flow` (ciclo mediano por fase, heatmap fase×semana dot-matrix, throughput semanal), keymap/tecla, empty state honesto. | `taskboard/views.py`, `taskboard/keymap.py`, `taskboard/app.py` |
| 3 | US-D parte 1: flujo bloqueo→tarea bloqueante (prompt + wiring `depends_on` + `blocked`), token `⛓N` en `card_cell`, sort `unblock` en el asiento kanban. | `taskboard/app.py`, `taskboard/views.py` |
| 4 | US-D parte 2: cadena crítica en gantt (camino más largo del DAG de `depends_on`, resaltada). | `taskboard/views.py` |

**Trigger evaluation (intake):** A1/A2/A3 FIRED (módulo nuevo `history.py`,
≥2 módulos tocados, `card_cell` leído por otras vistas) → design review en
Phase 2 + reverse census sobre `card_cell`. B1 FIRED para `card_cell`/
`reldue_token` (asserts de batch previo — los tests del countdown de hoy).
C-family: history.jsonl es escritura nueva en disco → patrón append-only
never-raises con JOURNAL_ERROR-análogo. D: vistas nuevas/cambiadas. E: 3
historias → rigor ya declarado. F: backlog refrescado hoy.

## Risks / watch-items

- El log solo empieza a acumular desde el deploy: la vista de flujo debe ser
  útil con POCA historia (n=1 transición) y honesta con NINGUNA.
- `⛓N` suma un token al presupuesto de `card_cell` (shed order: revisar).
- La cadena crítica en gantt no puede romper la ley de "un color = un trabajo":
  el resaltado usa el asiento de severidad o de acento, decidido en Phase 2.

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-24 | batch-10 abierto; scope A+B+D, US-C aparte (cross-repo desk) | operator |
| 2026-08-24 | log en sidecar `~/.taskboard/history.jsonl` append-only | operator |
| 2026-08-24 | autonomía + commits por incremento autorizados; push a la orden | operator |
| 2026-08-24 | el flujo bloqueo→tarea nace del operador: "un block se vuelve tarea" | operator |

---

# Phase 1 — Requirements (derived 2026-08-24, draft-time verified)

## US-A — transitions log (`taskboard/history.py`, new)

Writers census (C-15.1, executed): `task.phase` is written by `set_phase`
(models.py:1094-1101 — the ONLY stamper of `phase_changed`, its docstring says
so), `rename_phase` (1147 — a rename is not movement), `delete_phase` (1166 —
reassigns WITHOUT stamping; pre-existing, recorded as observation, out of
scope). **The log hooks `set_phase` + `add_task` (1102) only**; rename/delete
are admin operations, declared non-logged.

- **HLR-A1.** The system shall append one JSON record to
  `<board_dir>/history.jsonl` on every phase transition through `set_phase`,
  carrying `task` (id), `from`, `to`, `at` (ISO, seconds).
- **HLR-A2.** `add_task` shall append a creation record (`from`: null).
- **HLR-A3.** The writer shall never raise and never block the board mutation;
  a failed append sets `HISTORY_ERROR` (desk's JOURNAL_ERROR pattern) — silent
  loss presenting as clean is worse than a visible error.
- **HLR-A4.** The reader shall never raise: missing file = empty history;
  malformed lines are skipped and counted; the count is exposed.
- **HLR-A5.** `board.json` format is unchanged; reading the board never
  touches history (sidecar law — operator decision).

**Acceptance (black-box):**
- AT-A1: app phase-move on a fixture board appends exactly one line with the
  four fields; `at` parses. *(RED arm: kill the append.)*
- AT-A2: `add_task` appends `from=null`. *(RED arm: skip creation hook.)*
- AT-A3: unwritable history path → the move succeeds, `HISTORY_ERROR` set, no
  exception. *(RED arm: raise instead of swallow.)*
- AT-A4: file with 2 good + 1 corrupt line → 2 records, `skipped == 1`, no
  raise. *(RED arm: drop the skip counter.)*

## US-B — flow view (key `7` — verified free: keymap.py:67-74 occupies 1-6)

- **HLR-B1.** Cycle time per phase = median days over CLOSED intervals
  (enter→exit pairs in history); a phase with only open intervals shows
  "en curso n=N", never a number — an open interval is not a cycle.
- **HLR-B2.** Heatmap phase × week (8 weeks, current rightmost): cell
  intensity = task-days spent in that phase that week, block ramp `░▒▓█`.
- **HLR-B3.** Throughput = tasks whose `to` is the terminal phase, per week,
  8 weeks, mini bar strip + total.
- **HLR-B4.** No history → the view states "sin historia aún — se construye
  desde hoy" and nothing else (no zero-metric theater); exactly one
  transition → renders, no division by zero.
- **HLR-B5.** Width-exactness contract holds (the repo law); `7` is wired in
  the ONE keymap seat; keybar and legend show it.

**Acceptance:**
- AT-B1: fixture history with known intervals → the three artifacts carry the
  computed values; transcript executed in Phase 3 and pasted into the
  increment packet. *(RED arm: fixture with different numbers.)*
- AT-B2: empty history → the sentence, no metric glyphs.
- AT-B3: single transition → renders without error.
- AT-B4: width sweep cell-exact (1..120); keymap contains key `7` →
  `view('flow')`.

## US-D — dependency intelligence

- **HLR-D1.** `b` on an unblocked task shall ask "¿qué lo bloquea?": create a
  new task or pick an existing one; the system sets `blocked=True` on the
  blocked task and appends the blocker id to its `depends_on`. `b` on a
  blocked task unblocks without asking. Covered by the undo stack (LLR-010.1
  precedent: snapshot BEFORE the mutation).
- **HLR-D2.** A card shall show `⛓N` when N≥1 open tasks depend on it (it
  unblocks N): neutral `mut` tone, omitted at 0, rides the shared indicator
  budget with the shed law (listed after `·Nd`/`+Nd`, before `▣`).
- **HLR-D3.** Kanban sort mode `unblock`: descending unblock count, stable
  ties; **blocked tasks sink** — an ordering whose point is "what frees the
  board" may not lead with work that cannot start (decision recorded; the
  blocked-first law of `priority`/`due` is not extended here).
- **HLR-D4.** Gantt shall highlight the longest `depends_on` chain among open
  tasks (accent house; header names it: `cadena crítica · N`); a board with
  no dependencies renders byte-identical to before.

**Acceptance:**
- AT-D1: block flow wires `depends_on` + `blocked`, creates or links the
  blocker; undo restores. *(RED arm: link not written.)*
- AT-D2: `⛓` absent at N=0, `⛓2` at N=2, width-exact sweep with the token.
- AT-D3: fixture order under `unblock`; blocked task sinks.
- AT-D4: a 3-long chain highlights exactly those 3 tasks; no-deps render
  byte-identical.

## IFC (C-54) Part A

`history.jsonl` (SOURCE) → `history.read_history` → `views.flow_*`
computations → `render_flow` (SINK, key 7) · `report.py` is a declared FUTURE
consumer, untouched this batch. `depends_on` (SOURCE, models) →
`unblocks_count` → `card_cell` token + kanban `unblock` seat + gantt chain
(SINKS). No node without an owning requirement.

## Phase-1 self-check

Every named symbol verified on disk at draft time (set_phase/add_task/
action_toggle_blocked/keymap keys 1-6 taken, 7 free). Every AT names its RED
arm. No acceptance value matches a phantom constant (C-36): tones
(over/soon/accent/dim/mut) are the palette's defined keys.

---

# Phase 2 — review (two agents, parallel): findings FOLDED

Verdict: NOT clean at arrival — 7 blockers across the two reviews. All folded
below; no story changes scope. Reviewers' verified-true claims stand.

## Blockers folded

- **F-B1 (symbol).** The stamping seat is `Board.set_task_phase`
  (models.py:1089), NOT `set_phase` (does not exist). Every HLR reading
  "through `set_phase`" now reads `set_task_phase`. `add_task` =
  models.py:1103.
- **F-B2 (census).** The writers census adds the two load-path writers —
  `Task.from_dict` (models.py:806) and load-time canonicalization
  (models.py:903) — both repair paths, declared non-logged.
- **F-B3 (undo).** `_UNDO_FIELDS` (app.py:544) gains `depends_on`, snapshotted
  as a COPY (the current by-reference capture would alias the appended list).
  The snapshot moves INTO the modal callback (commit time), or a cancelled
  prompt leaves a stale snapshot. AT-D1's undo limb is scoped: undo restores
  the blocked task's `blocked` + `depends_on`; the created blocker PERSISTS
  (a modal add records nothing — AMD-05 precedent).
- **F-B4 (sort seats).** `unblock` is an EXPLICIT branch in BOTH
  `kanban_order` (views.py:3457 `else:"due"` trap) AND `_kanban_cell_order`
  (views.py:3637) — renderer/nav parity (the F-3 law); an unknown mode must
  never silently render due-order.
- **F-B5 (`b` semantics).** `b` on an unblocked task now opens the blocker
  prompt (when candidates exist) instead of flipping the flag. Two pinned
  tests are intentionally REWRITTEN to the new flow (declared):
  `test_toggle_blocked_flips_the_flag_and_the_card_prefix`
  (test_app.py:2408) and the undo-LIFO test (test_app.py:3797). When no
  candidate blocker exists (single-task board), `b` flips without prompting.
- **F-B6 (dirty DAG law).** `depends_on` is untrusted: edges only over known
  task ids (unknown id = no edge); longest-chain and `unblocks_count` carry
  visited-set cycle safety (A↔B hand-edited boards cannot hang a render).
  Folded into HLR-D2/D4.
- **F-B7 (prompt copy).** App UI strings are English; the prompt is
  "What blocks it?" (not the Spanish draft). Batch artifacts stay `en`.

## Notices folded (mechanisms now specified)

1. **Hook seat = models.py.** The append lives INSIDE `set_task_phase` /
   `add_task` — one seat, all callers (incl. the edit modal, app.py:837).
   Increment 1's file list corrected.
2. `history.append` does its own `mkdir(parents=True, exist_ok=True)`.
3. **Injectable clock:** `at=None → now` parameter; tests never read the wall
   clock. Two-clock fact declared: `phase_changed` is a date; the flow view
   buckets from `at` (datetime), never from `phase_changed`.
4. **Phase-name drift semantics (documented, not discovered):** cycle/heatmap
   key on phase NAME and fragment across renames (accepted); throughput
   counts `to` == the CURRENT terminal phase and history predating phase
   edits is approximate (accepted); a re-opened task entering the terminal
   phase again counts again (throughput = completions).
5. **⛓N slot:** indicator order becomes `[↗ ! ▤ ·Nd +Nd ⛓N ▣]` — this
   SUPERSEDES the countdown's "only ▣ sheds later" comment; the card_cell
   docstring, the countdown comment, and the test docstring
   (test_cells.py:326) are updated in the same increment. Bare `⛓` (U+26D3,
   NO VS16) — pinned by execution: `cell_len("⛓")==1`, with VS16 it's 2.
6. **View plumbing:** `flow` gets explicit branches in `render_view` (no
   swimlanes fallback), `nav_model` (no selectable rows), `VIEW_ORDER`, and
   the aperture (key 7 handled/swallowed there — aperture.py:51 binds 1-6).
7. **Flow legend is state-aware** (test_legend.py:84 iterates VIEWS): the
   empty-history render paints no ramp, so `legend_entries("flow")` only
   claims swatches the current render actually shows (ghost-mark law).
8. **AT hardening:** fixtures tmp_path-rooted (never `_UNWRITTEN` for hooked
   boards — the hook writes beside the board file). AT-A3's unwritable
   mechanism = a DIRECTORY at the history path (portable on Windows) or
   monkeypatch; `HISTORY_ERROR` surface = module global + one-shot `notify`
   on append failure (assertion targets the global AND the notify mock).
   AT-A4 gains a valid-JSON-wrong-shape line (`{"task": 1}` → skipped).
   AT-B1 pins: even-n median renders one decimal (`2.5d`); enter→exit
   granularity = whole days by date diff of `at`; transcript uses fixture
   titles only. AT-B2's glyph-absence pins the flow BODY only. AT-B3 pins
   the string "en curso n=1". AT-D3's fixture asserts its order is DISTINCT
   from project/priority/due/recent first (the palindrome-fixture law).
   AT-D4: bars may wear accent only (test_gantt.py:128-130 already lawful);
   the assert-worn idiom (test_gantt.py:115) adopted.
9. **Security (C-family):** history records carry ids + phase names +
   timestamps, NEVER titles (the 2026-08-07 leak class). Reader's
   skip-and-count IS the concurrency story (no O_APPEND atomicity on
   Windows). `render_flow` phase labels are untrusted input → escaped /
   intersected with `board.phases` at render (the repo's escape-at-render
   seat). Permissions match board.json (declared exposure, no hardening).
   The blocker prompt inherits `TextPrompt`/`ConfirmModal` escaping; the
   pick-existing list escapes titles (verify vs ProjectPicker at impl).
10. **Intake correction (honesty):** `test_win_clipboard_roundtrip` PASSED
    at the Phase-2 baseline run — the intake note "reproduced failing on
    clean tree" was true at intake time (two consecutive failures) but is
    intermittent; recorded as environmental flake, excluded by convention,
    NOT a batch signal either way.

## Reviewer-verified OK (stands)

card_cell width contract safe with ⛓N (shed-by-construction); `unblock`
contradicts no pinned law (per-mode docstrings); gantt chain via the existing
3-cell `└─►` seat toned accent + header suffix (zero-layout-change), guarded
→ byte-identical no-deps render; log record suffices for all three artifacts;
sidecar law consistent with load/save/engine watcher; seed data bypasses
`add_task` (a fresh board logs nothing — honest).

## Phase-2 gate record

Blockers found → folded here → plan amended. Authorization is autonomous
(commits authorized), so the gate proceeds on the recorded fold; the `b`
semantics change is the operator's own approved story (intake: "un block se
vuelve tarea").

---

# Phase 3 — Implementation

## Increment 1 — US-A: transitions log

**Status:** complete. **Commit:** *pending*.

### What changed
- New module `taskboard/history.py`:
  - `HISTORY_ERROR` module global (desk JOURNAL_ERROR pattern).
  - `history_path(board_path) -> Path` — sidecar `history.jsonl` beside `board.json`.
  - `append(board_path, record, at=None) -> dict | None` — fills ISO `at`, creates parent dirs, writes one JSON line; OSError sets `HISTORY_ERROR` and returns `None` (never raises).
  - `read(board_path) -> tuple[list[dict], int]` — missing file returns `([], 0)`; blank lines ignored; invalid JSON or wrong-shape lines skipped and counted.
- `taskboard/models.py`:
  - `Board.set_task_phase` appends `{"task": id, "from": old, "to": phase}` on actual moves.
  - `Board.add_task` appends creation record `{"task": id, "from": None, "to": phase}` before saving.
- `taskboard/app.py`:
  - Imports `history`; tracks `_last_history_error`.
  - `_warn_history_error()` surfaces new `HISTORY_ERROR` messages once via `notify(..., severity="warning")`.
  - Called after `action_phase_move` and `_on_task_edited` so the operator sees append failures without the board mutation aborting.

### Tests added (`tests/test_history.py`)
- `test_phase_move_appends_one_transition` — AT-A1.
- `test_add_task_appends_creation_record` — AT-A2.
- `test_history_error_is_surfaced_without_aborting_move` — AT-A3.
- `test_read_skips_malformed_lines_and_counts_them` — AT-A4.
- `test_read_missing_file_returns_empty_history` — guard.
- `test_append_sets_and_clears_history_error` — guard.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-A1 RED — append in `set_task_phase` killed:**
```
tests/test_history.py::test_phase_move_appends_one_transition FAILED
assert 0 == 1
where 0 = len([])
```
*Failure:* no history line written after the phase move.

**AT-A2 RED — creation hook in `add_task` skipped:**
```
tests/test_history.py::test_add_task_appends_creation_record FAILED
assert 0 == 1
where 0 = len([])
```
*Failure:* adding a task wrote no creation record.

**AT-A3 RED — `history.append` raised instead of swallowing:**
```
tests/test_history.py::test_history_error_is_surfaced_without_aborting_move FAILED
PermissionError: [Errno 13] Permission denied: ...\history.jsonl
```
*Failure:* the unwritable history path aborted the app action, proving the swallow is load-bearing.

**AT-A4 RED — skip counter dropped:**
```
tests/test_history.py::test_read_skips_malformed_lines_and_counts_them FAILED
assert 1 == 2
```
*Failure:* malformed lines were still skipped but no longer counted, so `skipped` under-reported corruption.

### Suite status after increment
`python -m pytest tests/ -q` → **886 passed** (880 baseline + 6 new). `test_win_clipboard_roundtrip` not flagged; environmental flake convention stands.

### Suggested commit message
`batch-10 inc-1: transitions log (history.py) hooked into set_task_phase/add_task`

## Increment 2 — US-B: flow view (key `7`)

**Status:** complete. **Commit:** *pending*.

### What changed
- `taskboard/views.py`:
  - `_FLOW_WEEKS`, `_FLOW_RAMP`, `_flow_parse_at`, `_flow_week_key`, `_flow_last_weeks`, `_flow_intervals`, `_flow_cycle_times`, `_flow_heatmap`, `_flow_throughput`, `_flow_ramp_char`, `_flow_format_median`.
  - `render_flow`: read-only dashboard of cycle time (median whole days per closed interval; "en curso n=N" for open-only phases), phase×week heatmap (block ramp `░▒▓█`), weekly throughput (counts + bar + total). Empty history shows only the pinned sentence; width-exact down to `MIN_WIDTH`.
  - Explicit branches in `render_view`, `nav_model`, `legend_entries` for `mode == "flow"`.
- `taskboard/app.py`: `VIEW_ORDER` ends with `"flow"`; `VIEW_KEYS` adds `"7": "flow"`.
- `taskboard/keymap.py`: `Key("7", "7", "view('flow')", "Flow", primary=True, group="views")`.
- `taskboard/aperture.py`: `Binding("7", "jump('flow')", "Flow", group=VIEWS)`.
- `README.md`: keybinding table documents `7` → Flow.

### Tests added (`tests/test_flow_view.py`)
- `test_flow_renders_cycle_heatmap_and_throughput` — AT-B1.
- `test_flow_empty_history_shows_sentence_and_no_ramp` — AT-B2.
- `test_flow_single_transition_renders_and_shows_open` — AT-B3.
- `test_flow_width_sweep_is_cell_exact` — AT-B4.
- `test_key_7_switches_to_flow_view` — key wiring.
- `test_flow_nav_model_has_no_selectable_rows` — nav parity.

### Fixes applied during increment
- Padded `THROUGHPUT` section header to viewport width.
- Widened cycle value column so `"en curso n=N"` fits without truncation.
- Updated width-sweep assertion to honor `MIN_WIDTH` clamping.
- Corrected AT-B1 expectation: `Doing` shows `3d` (two closed intervals), not `"en curso n=1"`.
- Updated `test_two_now_opens_agenda` and README keybinding table for the new view.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-B1 RED — fixture dates changed to 1-day Backlog / 4-day Doing:**
```
tests/test_flow_view.py::test_flow_renders_cycle_heatmap_and_throughput FAILED
E       AssertionError: assert '2d' in 'FLOW ...'
```
*Failure:* the computed medians shifted, so the pinned expectations no longer matched.

**AT-B2 RED — empty-state body rendered a ramp glyph:**
```
tests/test_flow_view.py::test_flow_empty_history_shows_sentence_and_no_ramp FAILED
E       assert not True
```
*Failure:* the body contained `░`, violating the "no metric glyphs" empty-state contract.

**AT-B3 RED — open-interval label changed from "en curso" to "abierto":**
```
tests/test_flow_view.py::test_flow_single_transition_renders_and_shows_open FAILED
E       AssertionError: assert 'en curso n=1' in 'FLOW ...'
```
*Failure:* the only-open-phase path no longer emitted the required string.

**AT-B4 RED — CYCLE header no longer padded to viewport width:**
```
tests/test_flow_view.py::test_flow_width_sweep_is_cell_exact[1] FAILED
E           assert 5 == 24
```
*Failure:* the section header was shorter than the clamped viewport width.

### Suite status after increment
`python -m pytest tests/ -q` → **1011 passed** (886 after inc-1 + 125 new flow tests; 2 previously-failing assertions updated for the new view). `test_win_clipboard_roundtrip` not flagged.

### Suggested commit message
`batch-10 inc-2: flow view (key 7) — cycle time, phase×week heatmap, weekly throughput`

## Increment 3 — US-D part 1: block-becomes-task flow + ⛓N + unblock sort

**Status:** complete. **Commit:** *pending*.

### What changed
- `taskboard/app.py`:
  - Reworked `action_toggle_blocked`: unblocking flips directly; blocking asks
    "What blocks it?" when candidate tasks exist, otherwise flips directly.
  - Added `_on_blocker_picked` and `_on_new_blocker` callbacks: snapshot at
    commit time, set `blocked=True`, append blocker id to `depends_on`; the
    created blocker persists (modal add is not undoable).
  - `_UNDO_FIELDS` gained `"depends_on"`; `_snapshot` copies the list so the
    undo stack is not aliased by later mutations.
- `taskboard/modals.py`: new `BlockerPicker` modal listing "(create new blocker)"
  plus open candidate tasks; escaped titles; dismisses with blocker id,
  `"__new__"`, or `None`.
- `taskboard/models.py`: `unblocks_count(board, task)` — direct open dependents
  only, ignores dangling ids and done/archived tasks.
- `taskboard/views.py`:
  - `card_cell` indicator order is now `[↗ ! ▤ ·Nd +Nd ⛓N ▣]`; the bare `⛓`
    (U+26D3, no VS16) is a one-cell `mut`-tone token.  Counts are computed once
    per render pass and passed via the new `unblocks` parameter.
  - `kanban_order` and `_kanban_cell_order` gained explicit `"unblock"` branches:
    unblocked tasks with the most dependents first, blocked tasks sink, stable
    ties.
- `tests/test_dependencies.py`: AT-D1 (existing/new blocker + undo), AT-D2
  (⛓N presence/absence + width contract), AT-D3 (unblock sort order + parity).
- `tests/test_app.py`: updated the kanban sort-cycle oracle and parity test for
  the new `unblock` mode; updated the undo snapshot field assertion to include
  `depends_on`.
- `tests/test_cells.py`: updated the countdown-token docstring to reflect the
  new shed order.

### Tests added (`tests/test_dependencies.py`)
- `test_block_flow_links_existing_task_and_undo_restores` — AT-D1 existing.
- `test_block_flow_creates_new_blocker_and_undo_restores` — AT-D1 new.
- `test_unblock_on_blocked_task_flips_without_prompt` — single-task guard.
- `test_unblocks_count_direct_open_dependents_only` — model helper.
- `test_unblocks_token_absent_at_zero_and_present_at_two` — AT-D2 presence.
- `test_unblocks_token_keeps_the_width_contract` — AT-D2 width sweep.
- `test_unblock_sort_puts_blocked_last_and_orders_by_count` — AT-D3 seat.
- `test_unblock_cell_order_is_distinct_from_other_sorts` — AT-D3 nav parity.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-D1 RED — blocker id not appended to `depends_on`:**
```
tests/test_dependencies.py::test_block_flow_links_existing_task_and_undo_restores FAILED
E           AssertionError: assert '<blocker-id>' in []
```
*Failure:* the blocked task flipped to `blocked=True` but its `depends_on` list
stayed empty, so the link was not recorded.

**AT-D2 RED — ⛓N token threshold raised:**
```
tests/test_dependencies.py::test_unblocks_token_absent_at_zero_and_present_at_two FAILED
E       AssertionError: assert '⛓2' in 'Hub                                today'
```
*Failure:* the token required more than 10 dependents before rendering, so a
hub with two dependents showed no chain glyph.

**AT-D3 RED — blocked tasks floated instead of sinking:**
```
tests/test_dependencies.py::test_unblock_sort_puts_blocked_last_and_orders_by_count FAILED
E       assert '<blocked-id>' == '<last-id>'
```
*Failure:* reversing the blocked tie-breaker put the blocked task at the top of
the unblock sort instead of the bottom.

### Suite status after increment
`python -m pytest tests/ -q` → **1019 passed** (1011 after inc-2 + 8 new
dependency tests; 3 existing assertions updated for the new `unblock` sort and
`depends_on` snapshot). `test_win_clipboard_roundtrip` not flagged.

### Suggested commit message
`batch-10 inc-3: block-becomes-task flow + ⛓N + unblock sort`


## Increment 4 — US-D part 2: gantt critical chain

**Status:** complete. **Commit:** *pending*.

### What changed
- `taskboard/models.py`: `critical_chain(board: Board) -> list[str]` — longest
  dependency chain among open tasks (not done, not archived). Edges only over
  known task ids; dangling ids ignored; hand-edited cycles cannot hang the
  renderer because every DFS path carries a visited set. Returns `[]` when no
  chain of length ≥2 exists.
- `taskboard/views.py`:
  - `render_gantt` computes `chain = critical_chain(board)` and a `chain_ids`
    lookup once per render.
    - Header gains ` · cadena crítica N` in `accent` when a chain exists.
    - The existing 3-cell `└─►` dependency seat at the project-task row and the
      inbox row is toned `accent` for chain members, `mut` otherwise.
  - The `if chain:` guard keeps the no-dependency render byte-identical to
    before.

### Tests added (`tests/test_dependencies.py`)
- `test_critical_chain_finds_longest_open_chain` — pins the longest chain and
  the deterministic tie-breaker.
- `test_critical_chain_ignores_done_archived_and_dangling` — only open, known
  edges count.
- `test_critical_chain_cycle_safe` — a hand-edited A↔B cycle terminates without
  repeating nodes.
- `test_gantt_critical_chain_highlights_exactly_three_linked_tasks` — AT-D4:
  header names length 3 and exactly the three chain members wear the accent
  arrow; a non-chain dependent keeps `mut`.
- `test_gantt_no_dependencies_has_no_chain_header_or_accent_arrow` — AT-D4:
  dangling `depends_on` keeps the arrow glyph but does not form a chain, so no
  header suffix and the arrow remains `mut`.

### Mutation evidence (RED arms)
Each AT was temporarily broken in the expected way, run, and restored exactly.

**AT-D4 RED — longest-chain tie-breaker reversed:**
```
tests/test_dependencies.py::test_critical_chain_finds_longest_open_chain FAILED
E   AssertionError: assert ['a', 'd', 'e'] == ['a', 'b', 'c']

tests/test_dependencies.py::test_gantt_critical_chain_highlights_exactly_three_linked_tasks FAILED
E   AssertionError: 'AChain' arrow is not accent
```
*Failure:* with the tie-breaker flipped, the alternative length-3 branch
(`a → d → e`) was selected instead of the expected critical chain, so the
wrong tasks were highlighted.

**AT-D4 RED — chain-member accent tone disabled:**
```
tests/test_dependencies.py::test_gantt_critical_chain_highlights_exactly_three_linked_tasks FAILED
E   AssertionError: 'AChain' arrow is not accent
```
*Failure:* the dependency arrow stayed `mut` for chain members, so the gantt
no longer visually distinguished the critical chain.

**AT-D4 RED — cycle guard removed:**
```
timeout 5 python -m pytest tests/test_dependencies.py::test_critical_chain_cycle_safe -q
exit=124
```
*Failure:* without the `if nxt in seen: continue` guard, the hand-edited
A↔B cycle caused infinite recursion and the test runner was killed by the
5-second timeout.

### Suite status after increment
`python -m pytest tests/ -q` → **1024 passed** (1019 after inc-3 + 5 new
critical-chain tests). `test_win_clipboard_roundtrip` not flagged;
environmental flake convention stands.

### Suggested commit message
`batch-10 inc-4: gantt critical chain`


---

# Phase 4 — Validation

**Status:** complete.

## Full-suite run

```
python -m pytest tests/ -q
1024 passed in 82.40s (0:01:22)
```

`tests/test_app.py::test_win_clipboard_roundtrip` did not flag in this run;
it is treated as an intermittent environmental flake per repo convention.

## Per-AT verification table

| AT | Requirement | Test location | Result | RED arm evidence (PLAN.md) |
|---|---|---|---|---|
| AT-A1 | Phase move appends one transition | `tests/test_history.py::test_phase_move_appends_one_transition` | pass | Increment 1 — "append in set_task_phase killed" |
| AT-A2 | `add_task` appends creation record | `tests/test_history.py::test_add_task_appends_creation_record` | pass | Increment 1 — "creation hook in add_task skipped" |
| AT-A3 | Unwritable history path does not abort move | `tests/test_history.py::test_history_error_is_surfaced_without_aborting_move` | pass | Increment 1 — "history.append raised instead of swallowing" |
| AT-A4 | Malformed history lines skipped and counted | `tests/test_history.py::test_read_skips_malformed_lines_and_counts_them` | pass | Increment 1 — "skip counter dropped" |
| AT-B1 | Flow view renders cycle/heatmap/throughput | `tests/test_flow_view.py::test_flow_renders_cycle_heatmap_and_throughput` | pass | Increment 2 — "fixture dates changed" |
| AT-B2 | Empty history shows sentence and no ramp | `tests/test_flow_view.py::test_flow_empty_history_shows_sentence_and_no_ramp` | pass | Increment 2 — "empty-state body rendered a ramp glyph" |
| AT-B3 | Single transition renders without error | `tests/test_flow_view.py::test_flow_single_transition_renders_and_shows_open` | pass | Increment 2 — "open-interval label changed" |
| AT-B4 | Width sweep cell-exact and key 7 wired | `tests/test_flow_view.py::test_flow_width_sweep_is_cell_exact` / `test_key_7_switches_to_flow_view` | pass | Increment 2 — "CYCLE header no longer padded" |
| AT-D1 | Block flow wires depends_on + blocked, undo restores | `tests/test_dependencies.py::test_block_flow_links_existing_task_and_undo_restores` / `test_block_flow_creates_new_blocker_and_undo_restores` | pass | Increment 3 — "blocker id not appended to depends_on" |
| AT-D2 | ⛓N token presence/absence and width contract | `tests/test_dependencies.py::test_unblocks_token_absent_at_zero_and_present_at_two` / `test_unblocks_token_keeps_width_contract` | pass | Increment 3 — "⛓N token threshold raised" |
| AT-D3 | Unblock sort: blocked sinks, count desc | `tests/test_dependencies.py::test_unblock_sort_puts_blocked_last_and_orders_by_count` / `test_unblock_cell_order_is_distinct_from_other_sorts` | pass | Increment 3 — "blocked tasks floated" |
| AT-D4 | Gantt critical chain highlights exactly longest chain | `tests/test_dependencies.py::test_gantt_critical_chain_highlights_exactly_three_linked_tasks` / `test_gantt_no_dependencies_has_no_chain_header_or_accent_arrow` | pass | Increment 4 — "longest-chain tie-breaker reversed", "accent tone disabled", "cycle guard removed" |

## Cross-cutting checks

- **Byte-identical no-deps guard:** `render_gantt` only emits the header suffix
  and accent arrow when `critical_chain(board)` returns a non-empty chain;
  the dangling-id test in AT-D4 verifies the fallback arrow stays `mut`.
- **Cycle safety:** `critical_chain` uses a per-path visited set; the RED arm
  shows the renderer hangs without it on a hand-edited A↔B cycle.
- **Palette law:** the only new hue on the gantt is `accent` on the existing
  `└─►` seat; bars retain their identity/project hues (verified by
  `tests/test_gantt.py::test_a_bar_never_wears_an_urgency_hue`).


---

# Phase 5 — Postmortem

**Status:** complete.

## Working-file reconciliation

```
$ git status --short
?? prototypes/city/
?? prototypes/lanes_load/
?? prototypes/mapper/
?? prototypes/team_sync/
?? prototypes/vista/
```

All batch-10 touched files are committed in `0cf0e72`. The untracked
`prototypes/*` directories belong to a parallel batch-11 exploration and are
NOT part of this batch. No uncommitted batch-10 changes remain; no reverts
were needed.

## Lessons

1. **Deterministic fixtures need deterministic ids.** The critical-chain
   tie-breaker test initially passed/failed depending on random UUID ordering;
   pinning task ids made the RED arm reliable.
2. **Cycle safety is not hypothetical.** Removing the visited-set guard caused
   an immediate hang on a 2-node hand-edited cycle; the guard pays for itself.
3. **Guarded render paths preserve byte-identical contracts.** The `if chain:`
   check keeps no-dependency gantt output identical to pre-batch-10, which a
   dedicated AT can verify through the dangling-id fallback.

---

# Phase 6 — Docs

**Status:** complete.

- `.dev-flow/BACKLOG.md` refreshed with new base ref `0cf0e72`, test count
  (1024 green), and a "Shipped — batch-10" section summarizing scope and
  deferring US-C.
- `README.md` was already updated in increment 2 for the new `7` Flow view
  keybinding and the `unblock` sort key; no further README changes were needed
  for the gantt critical chain.
- No new public API or operator-facing keybindings in increment 4, so no
  additional user docs required.

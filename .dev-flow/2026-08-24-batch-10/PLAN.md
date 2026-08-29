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

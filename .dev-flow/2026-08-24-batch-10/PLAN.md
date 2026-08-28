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
| US-B | **Vista de flujo.** Como operador quiero una vista con ciclo mediano por fase, heatmap fase×semana de dónde envejece el trabajo, y throughput semanal — derivados del log — para ver dónde se atora el trabajo. | READY (depende de US-A) | Nueva vista (tecla) renderiza los tres artefactos desde el log; board sin historia declara "sin historia aún — se construye desde hoy" (empty state que nombra su origen); todo número derivado de fixtures ejecutados. |
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

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

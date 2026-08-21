# PLAN — 2026-08-19-batch-09 · taskboard Lanes retícula G2

**Batch objective.** Implementar la vista **Lanes (tecla `1`) como retícula de paneles 2×3** variante **G2** del prototipo `prototypes/lanes_gauge`: espina de mercurio con la ventana del proyecto, barra de sedimento con ventana fija −7d…+21d, filas de tarea con texto completo y tally `n/N done`. El renderer clásico (`waves`) sigue disponible vía `Tab`. Sin cambios en `models.py`.

**Mode:** `core` (nueva presentación + navegación). Language: `en`.

## Verified at intake

- Base: `main` @ `7d0e12d` (batch-08 merged).
- Suite green: `python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"` → 860 passed.
- Prototype approved: `prototypes/lanes_gauge/out/lanes-gauge.html?variant=g2`.

## Stories — INVEST

| id | story | status | observable outcome |
|---|---|---|---|
| R-01 | **Lanes grid 2×3.** Como usuario quiero ver los proyectos como paneles apilados con mercurio, sedimento y tareas completas. | DONE | `render_swimlanes(..., presentation="grid")` produce la retícula; filas exactas al ancho pedido; tareas reversibles; capas extra cuando hay muchos proyectos. |
| R-02 | **Navegación 2D en grid.** Como usuario quiero moverme por columnas y filas como en kanban lanes. | DONE | `nav_model("swimlanes", ..., presentation="grid")` devuelve columnas por posición-x del panel, en el orden exacto que dibuja el renderer. |
| R-03 | **Ciclo de presentación.** Como usuario quiero alternar grid/waves con `Tab`. | DONE | `Tab` en swimlanes cicla `grid → waves`; el header nombra el modo (`grid n×m`); la keybar muestra `Layout`. |

## Increment plan

| inc | content | source files |
|---|---|---|
| 1 | Datos y helpers del grid: `start_in` en `LaneFacts`; helpers `_noise`, `_shade_hex`, `_grid_chip`, `_grid_list_order`, `_grid_c_hub`, `_grid_sediment_rows`, `_grid_task_row`, `_grid_panel_rows`, `_grid_mercury_cell`, `_grid_render`. | `taskboard/views.py` |
| 2 | Renderer con presentaciones: `render_swimlanes` acepta `presentation="waves"` (default) y `"grid"`; llena `line_map`. | `taskboard/views.py` |
| 3 | Navegación 2D: `grid_nav`; `nav_model` rama `swimlanes` bifurcada por presentación. | `taskboard/views.py` |
| 4 | Wiring de app y keymap: `lanes_presentation`, `action_toggle_presentation`, `render_view` kwarg, `keymap.py` tab scope. | `taskboard/app.py`, `taskboard/keymap.py` |
| 5 | Tests y validación: `tests/test_lanes_grid.py`; ajustes a tests de keymap/legend; README. | `tests/test_lanes_grid.py`, `tests/test_keymap.py`, `tests/test_legend.py`, `README.md` |

## Validation

- Full suite: `python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"` → **877 passed**.
- New tests cubren: geometría, sedimento, mercurio, nav 2D, ciclo Tab, regresión de waves.

## Risks / watch-items

- El grid no implementa animación de entrada en este batch; queda especificada en el handoff como sweep out-cubic y se puede agregar posteriormente.
- `panel_h` puede volverse pequeño con muchos proyectos; el renderer sigue dibujando y confía en `_scroll_selected_into_view`.

## Decision log

| date | decision | by |
|---|---|---|
| 2026-08-19 | Batch-09 abierto; variante G2 elegida desde `handoff-lanes-grid.md` | operator + handoff |
| 2026-08-19 | `lanes_presentation` es session-level, default `"grid"`, no se persiste | implementation |
| 2026-08-19 | `start_in` vive en `LaneFacts`; `lane_facts` recibe `start_date` keyword-only | implementation |
| 2026-08-19 | Animación de entrada diferida; grid se entrega estático con `sweep=1.0` | implementation |
| 2026-08-19 | Header de panel conserva el case original del proyecto para no romper contratos de board text | implementation |

# Handoff: implementar la vista Lanes como retícula G2 (mercurio + sedimento)

## Qué se decidió

La vista principal (Lanes, tecla `1`) se rehace como **retícula de paneles 2×3**:
menos columnas, capas apiladas, cada panel con TRES cosas — la espina de mercurio
(tiempo del proyecto), la barra de sedimento (cuenta regresiva al próximo
aterrizaje) y las filas de tareas con su texto completo. Es la variante **G2** del
prototipo, elegida por el usuario tras cinco rondas (`prototypes/lanes_gauge/NOTES.md`
tiene la historia completa y por qué se descartaron ola acumulada, tiras, diales
planos, polígonos, toro 3D y reloj de arena).

- **Referencia visual (la fuente de verdad):**
  `prototypes/lanes_gauge/out/lanes-gauge.html?variant=g2` — abrir en browser,
  flipbook de entrada + fixture en calma + render a 68 cols.
- **Implementación de referencia (casi literal):**
  `prototypes/lanes_gauge/proto.py` → `render_grid_board()` y sus helpers. El
  prototipo compone los asientos reales (`lanes_of`, `header`, `to_text`, etc.),
  así que el port es mayormente mecánico. Regenerar:
  `python prototypes/lanes_gauge/capture.py && python prototypes/lanes_gauge/build_html.py`.

## Forma de la integración (recomendada)

`tab` hoy cicla presentations en kanban (grouped/matrix/lanes) y focus
(tiles/inspector/images/review/stale) — mismo patrón para swimlanes:

- `render_swimlanes` gana `presentation="waves"` (default = el clásico intacto)
  y `"grid"` enruta al renderer nuevo. **El clásico no se toca**: sus tests
  (`test_row_cost.py`, `test_swimlanes.py`) siguen verdes por construcción.
- `app.py`: `self.lanes_presentation = "grid"` (session-level, junto a
  `kanban_presentation`, app.py:181) — G2 es el default que el usuario pidió;
  `tab` en swimlanes cicla `grid → waves`. El header nombra el modo
  (`◆ TASKBOARD · grid 2×3`, ley LLR-003.2: un modo no-default se nombra).
- `keymap.py`: la Key `tab` (keymap.py:114) amplía `views` a
  `("kanban", "focus", "swimlanes")`.
- `app.py` `action_toggle_presentation` (app.py:639): rama `swimlanes`.
- `render_view`: nuevo kwarg `lanes_presentation` enhebrado desde los dos call
  sites de app.py (refresh + resize, app.py:316-325 y 598-607).

## Semántica (fijadas por el prototipo — no reinventar)

**Espina de mercurio** (2 celdas a la izquierda de cada panel, corre por TODAS
las filas del panel menos el header; proto `_mercury_cell`):

- La tira mapea la ventana DEL PROYECTO: `start_date` abajo, `due_date` arriba.
- El mercurio sube desde abajo = fracción de tiempo consumida
  (`(today - start) / span`), con textura de grano (sombra por `_noise` fila a
  fila). Tono: el hue del proyecto.
- **Atrasado** (today > due): toda la columna en `over` y un `▲` rojo como cap
  en la fila superior del riel.
- **Sin fechas** (Inbox): riel `│` dim desnudo.
- Muescas `▪` en el riel a la altura de cada tarea fechada (over / accent si es
  hoy / hue del proyecto).
- **Requiere `start_date` en `LaneFacts`**: agregar `start_in: int | None` a
  `LaneFacts` (views.py:707) computado en `lane_facts` igual que `due_in`
  (additive; revisar construcciones literales en tests). Nada cambia en
  `models.py` — `Project.start_date` ya existe.

**Barra de sedimento** (ancho del panel; proto `_sediment_rows`):

- Ventana fija `−7d … +21d` mapeada al ancho del panel; relleno desde la
  izquierda hasta el próximo aterrizaje (min due de las tareas abiertas),
  rampa de grano `▓▒░` con ruido determinista (`_noise`), tintes de zona:
  `over` en lo vencido, `soon` 0–7d, `dim` más allá.
- `╎` accent en hoy; un stud `▄` por tarea fechada (over/accent/hue).
- Fuera de ventana: `◂`/`▸` en las etiquetas de extremo (`−7d` / `+21d`), la
  convención de clip-and-flag de la app. Tareas sin fecha: no marcan (cubiertas
  por el conteo del hub).
- Hub bajo la barra: chip absoluto del próximo aterrizaje + `·N` abiertas
  (proto `_c_hub`): `Aug 1 ▲16d ·3`. Etiquetas de extremo en la fila siguiente.

**Filas de tarea** (proto `_task_row_full`): prefijo `▲` over si bloqueada /
`▊` hue; título; grupo derecho `! ▤ ↗` + chip absoluto (`Aug 1`, tono por
severidad: over/accent/soon/mut). Seleccionada → reverse. Overflow del panel:
`+N more` dim. Tally `n/N done` fijado a la ÚLTIMA fila del panel.

**Geometría**: `cols=2` (G2). `n_cols = max(1, min(cols, inner // 19))`;
`col_w = (inner - (n_cols-1)) // n_cols`; `layers_n = ceil(len(lanes)/n_cols)`;
`panel_h = (body - (layers_n-1)) // layers_n` (body = h-1; una regla `─` frame
entre capas). Más proyectos que capacidad → nota `+N lanes` en el header.
**Decisión pendiente menor**: si `panel_h` cae bajo un mínimo útil (~7),
dibujar más alto que el viewport y dejar scrollear (el app ya tiene
`_scroll_selected_into_view`) — verificar contra la ley de vertical-fill en
`tests/test_vertical_fill.py`.

**Estrecho**: 68 cols → 2 columnas aguantan; el mecanismo ya lo demuestra el
SVG `grid-g2-68.svg`.

**Animación de entrada** (spec): barrido `sweep ∈ {0, .45, .8, 1}` (~600 ms,
out-cubic) — el mercurio sube y el relleno del sedimento crece. Frames
precomputados por cambio de datos, NUNCA re-derivar por tick (M21 §3 y
BUDGET.md). Sin motion ambiental adicional en esta variante.

## Navegación y selección (la trampa nombrada del repo)

- `nav_model` (views.py:3594+) rama `swimlanes` hoy devuelve
  `[swimlane_nav(...)]` (1 columna). Para `grid` debe volverse 2D siguiendo el
  patrón EXACTO de kanban lanes (views.py:3629-3649): una columna de nav por
  posición-x de panel; cada una contiene las tareas de sus paneles en orden de
  capa, en el orden en que el renderer las dibuja. Renderer y navegador leen
  del MISMO asiento — un cursor que puede estacionar en una tarea no dibujada
  es la trampa F-3, ya pagada tres veces en batch-04.
- El renderer debe llenar `line_map` por fila de tarea (patrón en
  `_kanban_grouped`, views.py:2989) o el scroll-into-view queda ciego.
- Selección: reverse sobre el título (el prototipo ya lo hace).

## Leyes del repo que aplican

- **`/dev-flow` primero.** No commit / no push sin orden explícita.
- Suite verde de entrada: `python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"`.
- Un solo asiento de orden; renderer y navegador lo comparten.
- Keymap contract: toda tecla que funciona se muestra (tab en swimlanes debe
  aparecer en la barra).
- `rich.markup.escape` en todo texto de usuario; glyphs width-1; spans por
  `collapse_runs` (span economy — el grid compone MUCHAS celdas, pasar por
  `to_text` como todo lo demás).
- Estado de vista: session-level, nunca en el JSON del board.
- Fixtures sintéticos para artifacts commiteables (ver docstring de
  `prototypes/capture.py`).

## Tests a escribir (nuevo `tests/test_lanes_grid.py` + ciclo en `test_app.py`)

- Geometría: ancho exacto por fila a 118/86/68; `panel_h` y reglas entre
  capas; `+N lanes` cuando no caben.
- Sedimento: relleno hasta el próximo aterrizaje; tintes de zona; posición
  del `╎`; studs; flags `◂/▸`; tarea sin fecha no marca.
- Mercurio: fracción llenada == `(today-start)/span`; atrasado → rojo + cap
  `▲`; sin fechas → riel desnudo; muescas a la altura correcta.
- Nav: `nav_model` devuelve exactamente lo dibujado (ambas presentations).
- Ciclo `tab` en swimlanes + el header nombrando el modo.
- Verdes de regresión: `test_row_cost.py`, `test_swimlanes.py`,
  `test_prism_laws.py`, `test_palette_ration.py` (los tonos del grid salen de
  la paleta existente — `_mul` sombrea hues de proyecto: verificar que la
  ración de paleta no se rompe; si el test mide hexes literales, el shader
  del prototipo puede necesitar un asiento de "tiers" declarado en views.py).

## Qué NO tocar

- `models.py` — sin campos nuevos (`start_in` vive en `LaneFacts`, en views).
- El renderer clásico (`waves`) y su allocator (`allocate`) — quedan como
  presentation alternativa.
- El keymap: ninguna tecla nueva; `tab` existente amplía su scope.

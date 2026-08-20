# Handoff: implementación de los prototipos "next level"

## Contexto

El handoff anterior (`handoff-three-prototypes.md`) proponía tres ideas. Al revisar el
repo resultó que **dos ya estaban implementadas en `main`**:

- **Kanban ordenable/agrupable** — batch-04 (`c92f896`): `s` sort
  (project/priority/due/recent), `g` group (project/priority/horizon), `z` collapse,
  `F` foco por proyecto, `tab` layout grouped/matrix.
- **Focus board con tiles** — batch-07 (`f9b72a9`/`9e86925`): vista `5` Focus con
  presentations tiles/inspector/images, `t` pin, highlights y thumbnails en notas.
- **Búsqueda global** — **no existe**; es la única idea virgin del handoff original.

Con eso se prototipó **el nivel siguiente de las tres ideas**, a color y con renders
reales del motor Rich sobre el fixture sintético. El usuario revisó la página
comparativa y aprobó el set ("me gustó todo").

- Página comparativa: `prototypes/next_level/out/next-level.html` (navegar con ←/→,
  teclas 1/2/3 por idea).
- Renderers de las variantes: `prototypes/next_level/proto.py` (componen los views
  REALES — `render_kanban`/`render_gantt`/`_focus_tiles`/`card_cell` — vía un
  compositor de celdas; nada es mockup redibujado).
- Notas de generación y enriquecimiento en memoria del fixture:
  `prototypes/next_level/NOTES.md`.
- Regenerar: `python prototypes/next_level/capture.py && python prototypes/next_level/build_html.py`.

## Decisión pendiente (bloquea /dev-flow)

Elegir qué se implementa de cada idea antes de abrir el batch:

| Idea | Variantes prototipadas | Recomendación del prototipista |
|---|---|---|
| 1 · Kanban lanes | 1A carriles×prioridad · 1B carriles×proyecto | **Ambas con una sola implementación**: el carril toma el `kanban_group` activo (ver abajo) |
| 2 · Focus follow-up | 2A review queue · 2B tiles stale-first | 2A como nueva presentation; 2B es casi gratis si entra 2A (mismo `stale_order`) |
| 3 · Búsqueda `/` | 3A filtro vivo · 3B jump palette · 3C context dim | **3A** primero (kanban+gantt); 3B como complemento después; 3C es la más débil |

Una vez elegidas las variantes, arrancar con **`/dev-flow`** (preferencia explícita
del usuario) y no tocar `models.py`: **ninguna variante requiere cambios al modelo**.

---

## Idea 1 — Kanban lanes (segunda dimensión del kanban)

**Qué es:** una tercera presentation del kanban — carriles horizontales × columnas de
fase con tarjetas reales en cada celda (la matrix shipped muestra conteos, no
tarjetas). Validado en `kanban-lanes-priority.svg` y `kanban-lanes-project.svg`.

**Diseño recomendado (una implementación, ambas variantes):**
el carril lo define el `kanban_group` activo (`project`/`priority`/`horizon`) y el
orden intra-celda el `kanban_sort` activo. Así `lanes` no introduce estado nuevo ni
una segunda fuente de orden — respeta la ley del repo de UN solo asiento de orden
(`kanban_order`, views.py:2830). 1A = lanes + group:priority; 1B = lanes +
group:project.

**Asientos a tocar:**

- `views.py:3055` `render_kanban` — agregar la rama `presentation == "lanes"` que
  llame a un `_kanban_lanes()` nuevo. Portar `kanban_lanes()` de
  `prototypes/next_level/proto.py` casi literal: geometría (`label_w=18`, `distribute`,
  junctions con `rule_row`), header nombrando el modo (ley LLR-003.2: un modo
  no-default se NOMBRA), celdas con `card_cell` (prefix `▊ ` en `project_color`),
  overflow `+N more` por celda, lanes vacíos omitidos (misma ley que
  `kanban_order`: "an empty group header is a ghost mark").
- Reusar `_windowed_header` (views.py:2766) para los encabezados de fase con WIP
  tags — el prototipo ya lo hace y salen los `◀ N ▶` gratis.
- `views.py:3175` `nav_model` — el grid carril×fase necesita su mapa de navegación
  2D: `h/l` entre columnas, `j/k` dentro de celda. El prototipo NO llena
  `line_map`; la implementación SÍ debe (patrón en `_kanban_grouped`,
  views.py:2989-2992), si no, `scroll_selected_into_view` queda ciego.
- `app.py:639` `action_toggle_presentation` — extender el ciclo de `tab` en kanban:
  `grouped → matrix → lanes`. **Cero bindings nuevos.**
- Estado: `kanban_presentation` ya existe y es session-level (app.py:181) — nada se
  persiste (LLR-003.2).

**Tests:** ciclo de `tab` en `tests/test_app.py`; nuevo test de lanes: ancho exacto
por fila a 118/86/60, overflow `+N`, omisión de lanes vacíos, coherencia con
`kanban_order` (mismo orden que grouped para el mismo group/sort). Verdes de
entrada: `tests/test_prism_laws.py`, `tests/test_palette_ration.py`.

---

## Idea 2 — Focus follow-up

**2A · Review queue** (`focus-review-queue.svg`): una tarea a tamaño completo
(notas con highlights, checklist, adjuntos) y el resto de la cola en un rail
stale-first. El follow-up como PASO DE REVISIÓN, no vitrina.

- Nueva presentation `"review"` en `render_focus` (views.py:2710); el ciclo `tab`
  en focus ya recorre presentations vía `focus_presentation` (app.py:187,
  session-level). Portar `focus_review()` y `stale_order()` del proto como
  `_focus_review()`.
- **Cero bindings nuevos**: `j/k` ya mueven la selección — el "índice de cola" es
  la posición de `selected_task_id` dentro de `stale_order`, no estado nuevo. El
  rail marca el seleccionado con `▸` accent (hoy el prototipo lo fija por índice;
  en la app se deriva de la selección).
- `stale_order`: grupos por proyecto ordenados por su tarea MÁS vieja, dentro del
  grupo por `days_in_phase` desc, Inbox al final. **`None` (sin stamp) hunde, nunca
  se lee como 0** — misma ley que `_recent_first` (views.py:2823).

**2B · Tiles stale-first** (`focus-stale-tiles.svg`): el grid shipped reordenado
con `stale_order` + tira de presión (`▲ N overdue · ■ N sitting ≥7d`) bajo el
header. Si entra 2A, 2B es una presentation más (`"stale"`) que llama a
`_focus_tiles` con el orden nuevo — el costo es la tira, ~10 líneas.

- **Artifact cosmético conocido** (visible en el prototipo): `_focus_tiles` abre
  header de proyecto mirando solo la PRIMERA tarjeta de cada fila del grid, así con
  órdenes no-proyecto una fila mixta puede etiquetar el grupo con el proyecto
  vecino. Si 2B se shippea, corregir el agrupado para que siga a los grupos, no a
  la fila.
- Tests en `tests/test_focus.py`: orden stale (None hunde), tira de presión, estado
  vacío de la cola sin pins.

---

## Idea 3 — Búsqueda / filtro global `/`

La única idea totalmente nueva. Tres mecánicas prototipadas sobre kanban y gantt
reales (query de demo `api`, 3/15 matches: uno por título, tres por proyecto).

**Binding:** `/` en `keymap.py` (KEYMAP es el único asiento — toda tecla que
funciona se muestra). Decidir alcance: kanban+gantt mínimo (el pedido original), o
universal. **Coordinar `escape`**: hoy `escape` = `focus_exit` guarded en
kanban/gantt (keymap.py:111); con búsqueda activa, `esc` limpia la query PRIMERO
y solo sale del foco si no hay query.

**3A · Filtro vivo (recomendada):** barra bajo el header (`/ query▌` + tally
`3/15 tasks · esc clears`), el board re-renderiza filtrado al tipear, matches en
reverse.

- Seat de matching: portar `matches()` del proto a views.py
  (título > proyecto > notas, case-insensitive). Las notas cubren `#etiquetas`
  orgánicamente; no hay campo tags ni hace falta.
- Filtro: NO copiar el `copy.copy(board)` del prototipo tal cual — mejor un
  parámetro `query` en `render_kanban`/`render_gantt` (o un helper
  `filter_tasks()`) para que el tally y los carriles vacíos sean coherentes por
  construcción. En gantt, **ocultar carriles de proyecto sin matches** (el
  prototipo lo valida filtrando también `projects`).
- Highlight: el prototipo post-procesa el `Text` renderizado (grid de celdas +
  `Style(reverse=True)` por match) sin tocar los renderers — mecanismo válido
  también para la app, y deja `card_cell` intacto.
- Input: `TextPrompt` (modals.py:734) da el modal de texto; la variante "barra
  inline viva" es más trabajosa (input siempre montado). Decidir en el batch; el
  prototipo dibuja la barra, no el mecanismo de tecleo.
- Estado: `self.search_query: str | None` session-level en app.py; nunca persistir.

**3B · Jump palette (complemento posterior):** overlay rankeado
(título>proyecto>notas), `↵` mueve `selected_task_id` y scrollea. El patrón exacto
ya existe: `CommandPalette` (modals.py:1113). No filtra el board — es la opción de
menor fricción si 3A resulta intrusiva.

**3C · Context dim:** nada se oculta, no-matches al 30% vía `line_map`. Es la más
débil de las tres (conserva el ruido visual); queda documentada por si se quiere un
modo "spotlight" después.

**Tests:** matching por las tres vías + case; precedencia de `esc`; gantt sin
carriles vacíos tras filtrar; la barra nombra el estado (LLR-003.2).

---

## Transversal (leyes del repo que aplican a las tres)

- **`/dev-flow` primero** — preferencia explícita del usuario para implementar.
- **No commit / no push sin orden explícita.** Todo commiteado queda en manos del
  usuario.
- Suite verde de entrada: `python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"`
  (849 passed en `a93b17e`).
- Un solo asiento de orden/filtro por feature; renderer y navegador leen del mismo
  seat (la trampa nombrada del batch-04).
- Keymap contract: toda tecla que funciona se muestra; toda tecla mostrada
  funciona (`keymap.py`).
- `rich.markup.escape` en TODO texto de usuario; glyphs width-1; spans pasan por
  `collapse_runs` (span economy, views.py:557).
- Los modos no-default se NOMBRAN en el header de la vista (LLR-003.2).
- Estado de vista: session-level, nunca en el JSON del board.

## Hallazgos incidentales (scripts de prototipado, no de la app)

Descubiertos al capturar; **no se corrigieron** por estar fuera de scope:

1. **rich 15.0.0 exige width Y height en `Console(...)`**: `Console.size` solo
   honra `_width` si `_height` también viene; si no, cae al fallback 80×25 y todo
   renglón >80 cols se envuelve en el SVG exportado. Los captures viejos
   (`capture.py`, `capture_gantt.py`, etc.) pasan solo width — **regenerar sus SVGs
   con la rich actual produce layouts rotos**. `prototypes/next_level/capture.py:77`
   ya lo documenta y lo hace bien.
2. **`prototypes/capture.py` produce SVGs vacíos**: envuelve el `print` en
   `with con.capture():` y eso mata el buffer de grabación. Por eso
   `prototypes/out/kanban-baseline.svg` (committed) está vacío. El patrón correcto
   es `record=True` + `print` directo (como `capture_gantt.py`).

Si alguna variante requiere repoblar fixtures: el fixture sintético es
`prototypes/out/_fixture_late.json` y los artifacts de prototipo NUNCA deben
contener datos del board real del usuario (ver el docstring de `prototypes/capture.py`).

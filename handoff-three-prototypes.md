# Handoff: taskboard — próximos prototipos

## Contexto
Proyecto **taskboard** (aplicación TUI de gestión de tareas con kanban, gantt, agenda y focus).

- Repo local: `C:\Users\jjgh8\Github\taskboard`
- Repo remoto: `https://github.com/jav201/taskboard`
- Último commit implementado: `a93b17e` *"gantt: date chips (variant G) with absolute start/due dates"*
- Suite de tests verde:
  ```bash
  python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"
  # 849 passed, 1 deselected
  ```

## Estado actual reciente
Se acaba de cerrar el batch de mejoras al Gantt:

- Las filas de proyecto y tarea en el Gantt muestran ahora chips de fecha absoluta (`Jul 14 → Aug 17`) en lugar del metro relativo (`+16d` / `done`).
- `taskboard/views.py` fue ajustado para reservar `META_FULL_W = 20` celdas al chip de fechas en terminales anchos.
- Se actualizaron `tests/test_gantt.py` y `tests/test_app.py` a las nuevas semánticas.
- Se generaron prototipos en `prototypes/out/` (HTML y TXT), manejados por los scripts en `prototypes/`.

Ver los archivos modificados y prototipos existentes para no repetir trabajo:
- `taskboard/views.py` (cambios recientes en geometría del Gantt y `_gantt_date_pair`)
- `prototypes/capture_gantt_shipped.py`
- `prototypes/out/gantt-shipped.html`
- `prototypes/out/gantt-shipped.txt`

## Próximo objetivo
El usuario quiere explorar **tres ideas** para decidir el siguiente incremento. Deben prototiparse a color (render real de terminal, preferiblemente HTML/SVG) usando las skills `/tui-design` y `/prototype`.

### 1. Kanban ordenable / agrupable
- **Problema:** el usuario usa mucho el kanban y le falta poder ordenar o agrupar de otras maneras.
- **Propuesta:** permitir ordenar cada columna del kanban por prioridad, due date o proyecto; opcionalmente mostrar swimlanes por proyecto o prioridad.
- **Pistas técnicas:** la lógica de ordenamiento ya existe en el Gantt (`sort_by_due`). Revisar `render_kanban` y el modelo `Task`/`Board`.

### 2. Vista Focus / Follow-up con tiles
- **Problema:** necesita un board de seguimiento donde marcar tareas para revisión y ver sus detalles (notas, emojis, imágenes, highlights de color) sin entrar al editor.
- **Propuesta:** agregar un flag `focus` (o similar) a las tareas, un binding rápido para marcar/desmarcar, y una nueva vista que muestre solo esas tareas en tiles grandes.
- **Pistas técnicas:** ya se discutió esta vista en sesiones previas; los emojis y el highlight de color en notas ya están implementados en `views.py`. Revisar si existe un campo `pinned` o similar que se pueda reutilizar.

### 3. Búsqueda / filtro rápido global
- **Problema:** a medida que crece el board, encontrar tareas se vuelve lento.
- **Propuesta:** un atajo (ej. `/` o `Ctrl+F`) que filtre tareas por título, notas, proyecto o etiqueta, y que funcione en kanban y gantt.
- **Pistas técnicas:** puede implementarse como un modo de "focus" sobre las tareas visibles sin tocar el modelo persistente.

## Restricciones y preferencias del usuario
- Quiere **prototipos primero**, a color, con renders reales de terminal.
- Valora la **novedad y facilidad de uso**.
- Prefiere decisiones basadas en comparación visual (A/B/C).
- No le gusta descartar lenguajes de diseño; los prototipos deben partir de la estética actual de taskboard.
- Antes de implementar código, usa `/dev-flow` para mantener orden.

## Skills recomendadas para la siguiente sesión
- `/tui-design` — para diseñar la jerarquía, tokens y layout de cada opción.
- `/prototype` — para generar variaciones comparables a color.
- `/html-visualizer` — si se quiere una página comparativa interactiva.
- `/dev-flow` — solo después de que el usuario elija una opción y apruebe implementarla.

## Comandos útiles
```bash
# Ejecutar suite
python -m pytest tests/ -q -k "not test_win_clipboard_roundtrip"

# Regenerar prototipo del Gantt (actual)
python prototypes/capture_gantt_shipped.py

# Ver estado del repo
git status
```

## Notas
- No se perdió trabajo en esta sesión; todo está commiteado y pusheado a `main`.
- Si alguna de las tres ideas requiere cambios en el modelo (`Task`/`Board`), proponerlos primero en el prototipo y luego discutirlos con el usuario antes de tocar `models.py`.

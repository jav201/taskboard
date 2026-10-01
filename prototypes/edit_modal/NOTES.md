# Prototipo — ventana de edición (ronda edición + prioridad)

**Pregunta.** «Cuando se editan tareas toda la interfaz de edición está muy
amontonada y sobre todo la parte de texto es muy pequeña como para ver con
claridad todo el contenido que ya está más el que se está escribiendo.»
¿Qué ESTRUCTURA de ventana deja ver las notas mientras se escriben?

**Dónde verlo.** `prototypes/edit_modal/out/ronda-edicion-prioridad.html`
(galería única con los dos problemas, conmutador 120×36 / 80×24, PNG real de
Windows Terminal + SVG de Textual por variante, cajas de decisión).

**Forma.** Sub-shape A: la `TaskboardApp` real en la vista kanban, con
subclases de `TaskModal` que re-componen los widgets enviados en sus ids reales
(`f-title … f-images`, `paste-img`, `save`, `cancel`, `cal-f-start`,
`cal-f-due`), así `_save`, el calendario, pegar imagen y ctrl+v / ctrl+e
siguen vivos. Fixture: tarea con 23 líneas de notas reales (es/en, ==…==,
!!…!!, ++…++, lista, URL), 2 URLs, 1 imagen; foco en notas con el cursor al
final. Fecha fijada 2026-09-30 (`fixture.pin_today`).

## Variantes

- **0 · Baseline** — `TaskModal` tal cual.
- **A · Editor dividido** — 92 %×92 %; columna izquierda de 34 col con campos de
  una fila; notas a 1fr a la derecha.
- **B · Pestañas** — título fijo, `TabbedContent` Notes / Details / Links;
  Save/Cancel siempre visibles. Capturado también con Details activa.
- **C · Pantalla completa + vista previa** — título, fila de chips de
  propiedades, editor | vista previa en vivo con `_highlight_markup` de la app,
  URLs/imágenes/botones al pie.
- **D · Compacto** — modal vertical de 100 col, rejilla 4 col de campos de una
  fila, banderas en una fila, notas 1fr (mín. 8), URLs/imágenes lado a lado.

## Hechos medidos (del render, `out/facts_edit.json`)

Filas de texto de notas visibles (región de contenido del TextArea recortada
por el compositor) / filas envueltas totales · ancho en columnas:

| variante | 120×36 | 80×24 |
|---|---|---|
| 0 | **3** / 43 · 50 col · título y Save fuera de vista | **3** / 43 · 50 col · ídem |
| A | **20** / 30 · 67 col | **9** / 59 · 30 col |
| B | **18** / 26 · 102 col | **7** / 30 · 65 col |
| C | **23** / 38 · 55 col (+ vista previa) | **11** / 50 · 35 col |
| D | **9** / 26 · 92 col | **6** / 30 · 66 col · Save bajo el pliegue |

## Límites encontrados

- **Baseline:** al enfocar las notas el `VerticalScroll` desplaza el modal; el
  título y Save quedan fuera de vista. Es parte de la queja, no un artefacto.
- **A a 80 col:** la columna de metadatos fija (34) deja las notas en 30 col
  (59 filas envueltas). Necesitaría colapsar la columna bajo ~100 col.
- **C a 80 col:** la fila de chips se recorta (se ve hasta la fecha de vence;
  banderas fuera). A 120 cabe justo, tras quitar márgenes. La vista previa
  aplica la regex de la app por línea (igual que la app: un resaltado no
  cruza líneas). El título de sección es una heurística del prototipo.
- **D a 80×24:** con mínimo 8 en notas, Save queda bajo el pliegue (el modal
  hace scroll). Es la variante que menos gana.
- Campos «slim» (una fila): Select/Input/Checkbox sin borde `tall`; el foco se
  marca con un fondo teñido (#10343a) en vez del borde — más débil que hoy.
- El CSS va en `App.CSS` (mismo nivel que `taskboard.tcss`): un `DEFAULT_CSS`
  en la pantalla PIERDE contra `.modal Label` sin importar la especificidad.
- El reloj del ribbon es la hora real de la captura (no se fijó).
- `cursor_blink=False` solo en captura, para que el cursor salga en el frame.

## Cómo correrlo

    python prototypes/edit_modal/proto.py            # vivo: 0-4 abren variante, ←/→ ciclan, esc cierra
    python prototypes/edit_modal/proto.py live C 12  # abre C directo y sale a los 12 s
    python prototypes/edit_modal/proto.py shot       # SVGs + facts_edit.json en out/
    powershell -File prototypes/edit_modal/shoot.ps1 -Proto edit_modal -Variant C [-Cols 80 -Rows 24]
    python prototypes/edit_modal/build_html.py       # la galería
    python prototypes/edit_modal/look.py out/x.svg   # SVG -> PNG para mirarlo (Chrome headless)

Dentro del modal las teclas escriben (no cambian de variante): `esc` y luego
el número. Los guardados van a una copia temporal del fixture.

**Estado.** Desechable. Nada en `taskboard/` cambió. Pin: textual 8.2.8.

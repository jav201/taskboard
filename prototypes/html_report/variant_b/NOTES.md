# Variante B — Interactive Workspace (propuesta de exportación)

Reporte HTML autocontenido y **interactivo**: un gantt de todas las tareas
(zoom fit/day/week/month, tooltip al pasar el cursor, clic abre la ficha de la
tarea), filtros (board, proyecto, persona, clase de milestone, estado, búsqueda
de texto), tabla ordenable por columnas, notas con ==!!++ y @menciones, y los
datos embebidos como JSON con botones *Download CSV* / *Download JSON*. Todo
con JS vanilla inline, cero peticiones externas, temas claro/oscuro y hoja de
impresión (imprime la tabla y las cifras; el gantt se simplifica).

## a. La tecla

Verificado en `taskboard/keymap.py`: en el KEYMAP global están tomadas las
minúsculas `a b c d e f g h i j k l m o p q s t u v x z , ; ? [ ] ! + -` y las
mayúsculas `A B F I M P R S T X`; libres quedan `n r w y` y `C D E G H J K N O Q
U V W Y Z`. Dentro de `R` (PresentScreen, `PRESENT_KEYS`: 1-3, tab, shift+flechas,
pgup/pgdn, space, a, u, K, J, enter, x, esc, q, ?) también están libres `H` y `W`.

**Elegida: `H` (mayúscula), GLOBAL** en la app principal, declarada como las
otras globales fuera de la barra (`bar=False`, como `R`, `S`, `A`): alcanzable
desde cualquier vista, nombrada en el `?` y en la paleta. No se pone dentro de
`R` porque el reporte no describe "lo que la presentación muestra u oculta":
describe el tablero entero, igual que `A` (agenda de todos los boards) ya lo
hace para otra lectura.

**Qué exporta: todos los boards cargados** (el workspace completo: cada
proyecto, cada tarea incluidos archivados, la gente, las clases de milestone).
Es la misma filosofía de `A` — una lectura transversal — llevada al formato
explorable. Si el operador quiere un solo board, la convención de
`report.report_path` (un HTML por board en `reports/`) ya existe y convive.

## b. Dónde cae el archivo y qué dice la app

Ruta: **`<carpeta del board actual>/reports/workspace-<YYYY-MM-DD>.html`** —
la misma convención que `report.py` (`reports/` junto al board), así el archivo
vive donde el operador ya busca los reportes y funciona igual con boards de
prueba. Toast, siguiendo el estilo de `app.py` ("Exported … to …"):

> `Report written: workspace-2026-10-29.html — o opens it`

y tras ese export, **`o` abre el último reporte generado en el navegador**
(mientras no haya reporte reciente, `o` sigue siendo `open_url`, como hoy).

## c. ¿Reemplaza o convive con el SVG (x dentro de R)?

**Convive.** El SVG/PNG de `x` es una imagen para pegar en slides o mandar por
chat: un retrato de una vista curada. El HTML es una herramienta de trabajo:
filtra, ordena y descarga los datos. Son salidas de distinta naturaleza (pixels
vs. datos), así que cada una merece su tecla y su momento; lo que sí reemplaza
este HTML es el reporte CLI estático de `report.py`, que queda obsoleto frente
a una versión interactiva de lo mismo.

## Límites conocidos / qué necesitaría la versión real

- **Rango del gantt dominado por lo archivado**: una tarea archivada de hace
  un año (Old: 2024 filing) estira el eje y comprime el trabajo actual; el
  prototipo lo resuelve con zoom "fit", pero la versión real querría un
  ajuste automático del rango (p. ej. excluir archivados del eje por defecto)
  sin perder honestidad en las etiquetas.
- **Sin lazy rendering**: con boards grandes (cientos de tareas) el SVG entero
  se reconstruye a cada filtro; haría falta virtualización de filas o un límite
  con aviso, nunca recorte silencioso.
- **Las descargas usan Blob + URL.createObjectURL**: perfecto en desktop, pero
  en algunos navegadores móviles el gesto de descarga de un `file://` es
  inconsistente; la versión real podría ofrecer copiar al portapapeles como
  alternativa.
- **Estado del filtro no viaja**: al recargar, todo vuelve al valor por
  defecto; una versión real podría guardar preferencias en el propio archivo
  (localStorage no aplica bien a `file://`) o aceptar parámetros.
- **El modal es de solo lectura**: la ficha muestra campos y notas pero no
  edita; que el reporte escribiera de vuelta rompería la ley de que el board
  solo se toca desde la app, así que la versión real seguiría siendo de lectura.

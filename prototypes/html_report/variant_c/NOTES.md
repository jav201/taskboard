# Variante C — Deck de presentación / handout en HTML

La propuesta del operador fue: «prototipes un reporte con funcionalidad
expandida en html que se exporte de la app». Esta variante toma la
presentación (R) y la reconstruye como un **deck HTML vectorial**: la misma
información que hoy sale como SVG (una imagen de celdas de texto), pero con
texto real y seleccionable, temas claro/oscuro, impresión limpia y lectura en
el teléfono.

## Qué es el prototipo

`build.py` genera un único `.html` autocontenido (cero peticiones externas)
con 8 diapositivas:

1. **Portada** — totales por tablero y la leyenda.
2. **Overview** — la vista «all» de la presentación: todos los proyectos de
   todos los tableros en una sola línea de tiempo.
3. **Una diapositiva por proyecto** (6) — cada una un gantt SVG con:
   - texto real `<text>` (seleccionable, buscable, copiable);
   - regla de «today»;
   - barras coloreadas por fase, con etiqueta directa (título + fase +
     prioridad + vencimiento + días en fase) — el color nunca significa solo;
   - hitos como rombos con la forma y el color de su clase (Delivery ▲,
     Billing ■, Launch ★), en ceniza si ya pasaron;
   - flechas de dependencia entre barras (la cadena photos → content →
     homepage → launch se ve completa);
   - trabajo bloqueado (borde rojo punteado + ⛔), hecho (✓, último), sin
     fechas (banda punteada «no dates»), archivado (línea al pie, fuera de la
     escala para no estirarla);
   - las notas de las tareas visibles con los resaltados ==!!++ y las
     @menciones resueltas a nombre y rol.

Navegación: ← → (también PageUp/PageDown, Home/End) solo cuando el foco no
está en un campo de texto, y botones en pantalla con contador «n / 8» para el
teléfono. A 390 px cada gantt cambia a un segundo layout SVG (etiqueta arriba,
barra abajo) en vez de encoger el de escritorio. `@media print` apila una
diapositiva por página con la paleta clara.

## a. La tecla

Verificado en `taskboard/keymap.py`: el KEYMAP global toma las minúsculas
`a b c d e f g h i j k l m o p q s t u v x z`, `, ; ? [ ] ! + -`, espacio,
enter, esc, tab, `@ #`, las flechas y las mayúsculas `A B F I M P R S T X`.
Libres en minúscula: `n r w y`; en mayúscula: `C D E G H J K N O Q U V W Y Z`.
Dentro de R (`PRESENT_KEYS`), el set propio liga `1 2 3`, tab/shift+tab,
`↑↓ k j`, `←→ h l`, pgup/pgdn, espacio, `a u K J` enter, `x`, esc, `q`, `?` —
así que en la presentación también están libres, p. ej., `H` y `W`.

**Elegida: `H` (mayúscula), dentro de R.** El `h` global ya es «izquierda»
(y dentro de R «rail ↔ timeline»), pero `H` mayúscula está libre en ambos
mundos y sigue la convención de la app: mayúscula = gesto grande y poco
frecuente (R presentar, S standup, X purgar). **Qué exporta:** el tablero
actual tal como la presentación lo muestra — portada + vista «all» + una
diapositiva por proyecto **respetando el estado de curaduría** (lo oculto con
`␣` no sale; `a` lo revela antes de exportar si se quiere completo), con el
nombre del tablero como slug de la portada. No exporta todos los tableros: R
es por tablero y el deck hereda ese alcance.

## b. Dónde cae y qué dice la app

Mismo convenio que `present_paths` y `report_path`: **al lado del tablero, en
`reports/`** — `reports/<slug>-<fecha>-deck.html`, donde `<slug>` es el
proyecto enfocado (tecla `F`) o `board` cuando no hay foco. Toast en el
estilo notify de la app (`Exported … to …`, `title="Present"`,
`severity="information"`, `timeout=10`, `markup=False`):

> Exported storefront-relaunch-2026-10-29-deck.html to C:\…\reports · o opens it

Seguimiento con **`o`**: hoy `o` abre la URL de la tarea seleccionada. Se
propone que, cuando la selección no tiene URL, `o` abra el último export
escrito (la app recuerda la ruta; se reutiliza el mismo `webbrowser.open` de
`action_open_url`). Así no se roba la tecla a nadie y el flujo «exportar →
mirar» queda en un solo golpe de tecla.

## c. ¿Reemplaza o convive con el SVG (x en R)?

**Reemplaza.** El SVG actual es una foto de celdas de texto: no se puede
seleccionar, buscar ni reordenar, y manipularlo en otro programa fue justo el
dolor del operador. El deck HTML lleva la misma vista como vectores vivos que
cualquier navegador imprime a PDF mejor que el PNG. Mantener ambos exportes
obliga a sostener dos renderizadores de la misma pantalla; que `x` pase a
escribir el deck (y muera el PNG, que hoy además exige Edge) concentra el
esfuerzo en una sola salida.

## Límites conocidos / qué necesitaría la versión real

- Los datos son sintéticos (fixture de la ronda). La versión real debe leer el
  tablero vivo, el estado oculto/plegado de PresentScreen y el orden de
  proyectos reordenado con K/J, que hoy el prototipo no respeta.
- La paginación es JS: con JavaScript desactivado la impresión muestra todo
  apilado (cubierto por `@media print`), pero no hay navegación alternativa.
- El gantt de teléfono es un segundo layout SVG generado en paralelo; un
  proyecto con decenas de tareas haría la diapositiva interminable — haría
  falta paginar filas o comprimir hitos.
- El archivo no interacciona más allá de pasar diapositivas: no se puede
  plegar/curar como dentro de R.
- Las URLs de las tareas quedan como enlaces externos (solo se abren con
  conexión); el archivo en sí sigue siendo 100 % offline.

## Verificación

`python prototypes/html_report/shot.py prototypes/html_report/out/c-report.html prototypes/html_report/out/c`
→ `_ok: true` en las cuatro combinaciones (1366×900 y 390×844, claro y
oscuro): 0 errores de consola, 0 peticiones externas, sin desbordamiento
horizontal. Se revisaron además las 8 diapositivas a mano en escritorio y
teléfono (capturas en `%TEMP%\cshots*`).

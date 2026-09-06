# PROTOTYPE — los seis heredados (+ blueprint) × seis pantallas canónicas

**Ronda de prototipo, no de implementación.** 42 frames reales, ya renderizados por la ruta del kit en
`inc37` (`taskboard.language` → `Static` headless → `capture_languages.svg_from_grid`). Esta ronda **no
tocó ningún kit, ningún test y ningún frame**: sólo los leyó. La ronda que faltaba desde que la matriz
pasó de 5×6 a 11×6 y nadie miró las seis filas nuevas.

`.txt` es la obra, `.svg` es una foto de ella en color. Cada frame tiene su `.candidates.md` al lado y
los 42 dicen lo mismo: *«Nothing was drawn by hand»*. Eso es lo que pone la celda en `implementa`, y es
justamente por lo que esta ronda existe: **`implementa` dice que un kit lo dibujó, no que se lea.**

Vocabulario cerrado de veredicto: **`keep` / `keep with a note` / `rework`**. Propuestos, no decididos.

---

## 0. Dos cosas que hay que decir antes de la primera tabla

### 0a. El conjunto pedido no es el conjunto de herederos (conflicto, no promediado)

El encargo nombra **instrument, swiss, industrial, darkside, solari, blueprint**. El repo nombra otros
seis: `inc35`/`inc36`/`inc37` llaman **INHERITORS** a *instrument, swiss, industrial, **nord**, darkside,
solari*. **Blueprint no es un heredero** — es uno de los cinco prototipados y sus seis frames ya fueron
juzgados en `PROTOTYPE.md`. **Nord sí lo es, y sus seis frames siguen sin juicio.**

**Corregido a mitad de ronda, por el coordinador.** La ronda cubre ahora **los seis herederos
— instrument, swiss, industrial, nord, darkside, solari — más blueprint**: siete lenguajes, 42 frames.
Blueprint se queda porque su hallazgo de `S4` es real y no se cae (§0b), y **nord entra con la misma
forma de bloque y la misma lectura adversarial** (§2.4), así que ya no queda ningún frame del repo del
que se pueda decir que nunca lo miró nadie. La deuda que abrió este § queda **saldada dentro de este
mismo documento**, no aplazada.

Blueprint se juzga aquí por segunda vez, y esa segunda mirada encontró un defecto que la primera no
podía ver (§0b). Nord se juzga por primera vez, y encontró el hallazgo estructural de la ronda: **el
defecto de `INVALID` no es de los cinco lenguajes que lo tienen, es del kit base** (§2.4, `nord_S2`).

### 0b. Una pregunta abierta de `PROTOTYPE.md` fue cerrada por código, sin veredicto

`PROTOTYPE.md` §4, pregunta 10:

> ¿El knockout de blueprint puede **moverse** del title block a la respuesta por defecto en un confirm,
> manteniendo «exactamente uno por vista»?

**Ya se movió.** `blueprint_S4.svg` contiene exactamente dos `<rect>`: el fondo de la hoja y

```
<rect x="236.8" y="282.0" width="67.2" height="17.0" fill="#eef4f8"/>
<text x="236.8" y="295.3" fill="#123a5c"> DELETE </text>
```

— tinta oscura sobre fondo pálido, sobre el botón destructivo del modal. Y en los seis frames el
title block se dibuja `<text ... fill="#7fa8c4">├ CLEAR ┤</text>`, tinta normal: **el knockout del title
block no se renderiza en ninguno de los seis.** La respuesta a la pregunta 10 fue «sí» y la dio el
render, no el operador. Está en §2.7 como `rework` de `blueprint_S4` y como evidencia en los otros cinco.

---

## 1. La matriz 7×6 de veredictos propuestos

|  | S1 list+detail | S2 form+validation | S3 settings | S4 modal | S5 monitor/log | S6 command palette |
|---|---|---|---|---|---|---|
| **instrument** | note | **rework** | **rework** | **rework** | keep | note |
| **swiss** | note | **rework** | **rework** | **rework** | note | note |
| **industrial** | note | **rework** | **rework** | keep | note | note |
| **nord** | **rework** | **rework** | note | keep | note | note |
| **darkside** | **rework** | note | **rework** | keep | keep | **rework** |
| **solari** | note | **rework** | keep | **rework** | note | note |
| **blueprint** | **rework** | **rework** | **rework** | **rework** | note | note |

**`keep` 6 · `keep with a note` 17 · `rework` 19.**

Los 19 `rework` no son 19 defectos independientes. Son **cinco hallazgos** con muchas caras, y nord
— el lenguaje que no tiene mecanismos propios — es el que prueba dónde viven cuatro de los cinco:

1. **La celda de severidad hace de cursor, de perilla y de pared** (instrument, swiss, industrial,
   darkside). El alfabeto de cada lenguaje es de tres a cinco celdas y cada celda tiene entre dos y
   nueve significados en la misma pantalla.
2. **El control destructivo pierde su marca justo donde importa** — `blueprint_S4` lo deja como palabra
   desnuda, `instrument_S4` le quita el peldaño de error y se lo pone a `Cancel`.
3. **Un caption se lee como un control** (industrial S3, darkside S3) y **un control se lee como un
   caption** (swiss S2, blueprint S4). Es el mismo error con los signos cambiados.
4. **El estado `invalid` se señala por orientación de pared**, no por forma (instrument S2, industrial
   S2, blueprint S2) — **y también `nord_S2`, que no overrideó nada. Eso lo convierte en un defecto del
   kit base heredado cuatro veces, no en cuatro decisiones de diseño** (§2.7).
5. **`Kit.match` no es observable en ningún frame de los 42** — §4.

---

## 2. Los 42 bloques

Cada bloque: **compromiso** que esa pantalla pone a prueba (con cita) · **qué muestra el frame**
(glifos copiados del `.txt`, nunca parafraseados) · **objeción** (contexto de uso · criterio observable ·
tier que hace falta) · **veredicto propuesto**.

Contexto de uso común, salvo que un bloque lo cambie: **operador único** (`jav201`), en un terminal de
100×32, monoespaciado, en una sesión de trabajo diurna con el terminal en su tema por defecto; la tarea
es la que la pantalla nombra (mirar el tablero, llenar el formulario, cambiar un ajuste, confirmar un
borrado, vigilar el log, ejecutar un comando).

---

### 2.1 instrument

Doctrina: `Instrument.__doc__` y LANGUAGES.md §1 — *«mono + one accent · dense · WHITESPACE STRUCTURE ·
drawn dot-matrix type · clinical. Numerals and icons drawn on a coarse dot grid; BORDERS ALMOST ABSENT;
one saturated hue for state»*. Alfabeto declarado: `LEVELS = {"info": "⠂⠂", "warn": "⠆⠆", "error": "⠇⠇"}`,
`PANE_RULE = "⠸"`, `REQUIRED = "⠁"`, `DISCLOSE = "⠿"`, `LATT = "⠒"`.

#### `instrument_S1` — list + detail
* **Compromiso puesto a prueba:** *«borders almost absent»* frente a la necesidad de partir la pantalla
  en dos. `inc36` lo resolvió con un argumento fino: *«a graticule is not a border — it was on the glass
  before either pane arrived»*.
* **Qué muestra:** la columna de graticule sostenida 27 filas, `5 ⠸ ⣿ DETAIL  Fix login redirect`, y el
  retículo de días por fase, `    ─├────7d┴───14d┴───21d┴`. El panel derecho llena sus filas con
  `project ⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒Web`.
* **Objeción:** el operador que barre esta pantalla para *localizar el corte entre panel y tablero* ve
  `⠸` una vez por fila y `⠒` entre seis y cuarenta veces por fila. **Criterio observable:** con el frame
  a 100 celdas, señalar la columna donde termina el tablero — hoy compite con seis filas de leaders que
  usan la misma familia de puntos. El `.txt` basta para verlo; no hace falta el SVG.
* **Veredicto propuesto: `keep with a note`** — el gutter funciona; los leaders del panel derecho gastan
  la misma retícula y le quitan al gutter la única cosa que lo hacía leerse, que era ser lo único vertical.

#### `instrument_S2` — form with validation
* **Compromiso puesto a prueba:** que la severidad sea **cuenta de puntos** (`⠂⠂ / ⠆⠆ / ⠇⠇`) y no matiz —
  el compromiso que `inc36` protegió explícitamente al elegir `⠸` para el gutter *«porque `⠇` es el
  peldaño de error y un divisor neutro con la celda de la escalera diría "rechazado" a un lector en
  escala de grises»*.
* **Qué muestra:** exactamente eso, dentro de los controles. Fila 17:

  ```
                  ⠄    Save    ⠄   ⠇   Cancel   ⠸
  ```

  El botón neutro `Cancel` abre con `⠇`. Y el campo inválido, fila 6, invierte el par del textarea:

  ```
    due⠁          ⠸12/09/26⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠇
                  ⠇⠇ expected YYYY-MM-DD
    notes         ⠇Redirect drops the ?next= param w⠿⠸
  ```

  `⠸…⠇` es inválido, `⠇…⠸` es normal. La diferencia entre «este campo está mal» y «este campo está bien»
  es **el orden de dos paredes**.
* **Objeción:** el operador llena el formulario y busca qué campo lo está bloqueando (`Save is held until
  due parses`). **Criterio observable:** tapar la fila 7 (el mensaje) y pedir que señale el campo
  inválido leyendo sólo las paredes. Falla: hay que comparar dos celdas braille en extremos opuestos de
  una fila de 34. El `.txt` lo muestra entero; el SVG no añade nada porque el canal es la forma.
* **Veredicto propuesto: `rework`** — el hallazgo (2) del encargo, confirmado y agravado: el peldaño de
  error abre el botón *seguro*, y el estado `invalid` se señala por orientación.

#### `instrument_S3` — settings
* **Compromiso puesto a prueba:** `REQUIRED = "⠁"` — *«one dot, at the top of the cell … la obligación es
  el piso de la cuenta»* (`inc35` §2).
* **Qué muestra:** el switch deshabilitado lleva esa misma celda, dos veces:

  ```
    sound                     ⡇⠒⠒
    sync to remote            ⠄⠁⠁   (no remote configured)
  ```

  Y el botón destructivo abre otra vez con el peldaño de error: `  ⠇ ⠛Delete all⠛ ⠸`.
* **Objeción:** el operador que viene de `S2` acaba de aprender que `⠁` significa «obligatorio». En `S3`
  la misma celda significa «apagado y no lo puedes tocar». **Criterio observable:** mostrar `S2` y `S3`
  seguidas y preguntar qué significa `⠁` — hay dos respuestas correctas y ninguna pista en pantalla.
  El `.txt` basta.
* **Veredicto propuesto: `rework`** — colisión directa entre la marca de obligación y el estado
  `DISABLED`, el hermano del hallazgo (2) que el encargo pedía buscar.

#### `instrument_S4` — modal dialog
* **Compromiso puesto a prueba:** el rechazo declarado de tapa de modal (`MODAL_BORDER_REFUSED`), *«a lid
  ENCLOSES; a graticule MEASURES»*.
* **Qué muestra:** dos reglas de graticule a ancho completo (filas 13 y 20) **idénticas byte a byte a la
  regla de cabecera de la fila 3**, y los dos botones:

  ```
  ⠧  ⠛Delete⠛  ⠼   ⠇   Cancel   ⠸
  ```

  El destructivo enfocado abre con `⠧`; el seguro, con `⠇⠇`-a-medias.
* **Objeción:** contexto de uso agudo — el operador está a una tecla de borrar tres tareas. **Criterio
  observable:** señalar, sin leer las palabras, cuál de los dos botones es el peligroso. La única celda
  de severidad de la pantalla está sobre `Cancel`. Segundo criterio: distinguir «hay un modal abierto» de
  «aquí termina la cabecera» — las tres reglas son la misma cadena. `.txt` suficiente.
* **Veredicto propuesto: `rework`** — severidad invertida en un confirm destructivo. Es el peor caso del
  hallazgo (2), porque aquí sí hay una acción irreversible detrás.

#### `instrument_S5` — live monitor / log
* **Compromiso puesto a prueba:** severidad como **cuenta**, que es el compromiso central del lenguaje.
* **Qué muestra:** la escalera limpia, en columna alineada:

  ```
    09:41:07 ⠂⠂ sync started  remote=origin
    09:41:09 ⠆⠆ 3 tasks overdue in BACKLOG
    09:41:18 ⠇⠇ rate limit hit  retry in 30 s
  ```
* **Objeción:** la que queda es leve. **Criterio observable:** con el color quitado, ordenar las tres
  filas por gravedad — se puede, porque 2 < 3 < 4 puntos es monótono y no depende del matiz. Es el único
  sitio de los seis frames donde `⠇⠇` significa lo que dice el registro.
* **Veredicto propuesto: `keep`** — el mecanismo hace exactamente lo que su cita promete.

#### `instrument_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "underline {accent}"` — *«a scope marks a span with a
  cursor»*.
* **Qué muestra:** nada. Fila 6, `  ⣿ redirect to task                            enter`, y ninguna de
  las seis filas de resultado lleva marca sobre el `re` que las hizo aparecer. El `.svg` tampoco:
  `instrument_S6.svg` tiene `font-weight: 0`, `text-decoration: 0` y un solo `<rect>` (el fondo).
* **Objeción:** el operador escribió `re` y quiere ver *por qué* casó cada fila. **Criterio observable:**
  circular los caracteres que casaron. **No es respondible en ninguno de los dos tiers**, porque
  `svg_from_grid` emite corridas de fondo y colores de relleno y nada más (§4). El subrayado existe en
  el kit y no existe en el artefacto.
* **Veredicto propuesto: `keep with a note`** — el frame no está mal; **la ronda no puede juzgarlo**, y
  esa es la nota. El criterio queda *inspeccionado, no ejercitado*.

---

### 2.2 swiss

Doctrina: `Swiss.__doc__` y LANGUAGES.md §2 — *«near-mono + one accent (classically red) · AIRY · single
hairline rules · plain cells. Strict grid, generous emptiness, FLUSH-LEFT EVERYTHING, NO BOXES —
ALIGNMENT DOES THE DIVIDING»*. Alfabeto declarado, entero: `LEVELS = {"info": "·", "warn": "─",
"error": "━"}`, `REQUIRED = "•"`, `DISCLOSE = "─"`, `DANGER_FORM = ("╲", "╱")`.

**El hallazgo de swiss es aritmético.** Su alfabeto tiene **cuatro celdas** y sus seis pantallas
necesitan distinguir por lo menos once cosas. No hay reparto posible sin colisión, y las colisiones que
salieron no son las que menos duelen.

#### `swiss_S1` — list + detail
* **Compromiso puesto a prueba:** *«ONE hairline rule»* y *«no boxes — alignment does the dividing»*.
* **Qué muestra:** el gutter es aire, correcto (`PANE_SPLIT_REFUSED`), y las cabeceras van
  letterspaced (`  B A C K L O G                 5`). Pero hay **tres** hairlines en la pantalla: la fila
  3 a ancho completo, y dos más en la fila 6 (`  ────…────    ────…────`). Y el cursor de selección es la
  celda de error:

  ```
  ━ D O I N G                     4
  ━   Fix login redirect           3d
  ```
* **Objeción:** el operador barre el tablero buscando problemas. **Criterio observable:** con el color
  quitado, decir si `DOING` está *seleccionado* o *en error* — `━` es lo uno en `S1` y lo otro en `S5`
  fila 14. No hay acción destructiva detrás, así que el riesgo es de lectura, no de acto. `.txt`
  suficiente.
* **Veredicto propuesto: `keep with a note`** — la retícula funciona; la nota es que la regla «una sola
  hairline» ya se gastó tres veces en esta pantalla y que `━` está sobrecargado.

#### `swiss_S2` — form with validation
* **Compromiso puesto a prueba:** *«NO BOXES — ALIGNMENT DOES THE DIVIDING»*, sin excepción de ancho.
* **Qué muestra:** el hallazgo (1) y el hallazgo (3) del encargo, en la misma pantalla, a nueve filas de
  distancia:

  ```
    title•        ┃Fix login▏ redirect···············┃
    tags          │ │ api  │▪│ ui  │▪│ urgent
    notes         │Redirect drops the ?next= param w─│
                       Save        ·   Cancel
  ```

  `inc38` le quitó las paredes **al botón**. El textfield, el checkbox, el textarea y el select
  (`│mon    ─│`, `S3`) las conservan. El resultado neto: el único control de la pantalla sin ninguna
  marca de control es el que el usuario tiene que pulsar.
* **Objeción:** contexto de uso — el operador acaba de escribir un formulario y busca el botón de
  guardar. **Criterio observable:** con el frame delante, señalar los controles pulsables. `Save`, que
  está `DISABLED`, no se distingue tipográficamente de la leyenda `Save is held until due parses` de la
  fila siguiente; ambos son palabras en el mismo tono sobre el mismo aire. `.txt` suficiente y decisivo.
* **Veredicto propuesto: `rework`** — un control deshabilitado que se lee como caption es riesgo de
  interacción, y la corrección de `inc38` dejó la pantalla **menos** consistente de lo que estaba: un
  componente sin paredes junto a cuatro con paredes.

#### `swiss_S3` — settings
* **Compromiso puesto a prueba:** que el acento rojo esté *racionado* y que la jerarquía sea peso.
* **Qué muestra:** el peldaño **más bajo** de la escalera abre el control **más peligroso**:

  ```
    ───────────────────────────────────────────────────────────────────────────────────────────────
    danger zone    delete every completed task
    · ╲Delete all╱     7 tasks, not recoverable
  ```

  `·` es `LEVELS["info"]`. Y ahí está la segunda y tercera hairline de la pantalla (filas 3 y 19).
  El switch es pared más peso: `━━│` encendido, `│──` apagado, `┆┈┈` deshabilitado.
* **Objeción:** el operador entra a ajustes y baja hasta el final. **Criterio observable:** sin leer las
  palabras, ordenar por peligro los controles de la pantalla — el borrado irreversible sale último,
  detrás de cinco switches. `.txt` suficiente.
* **Veredicto propuesto: `rework`** — el `·` delante de un `Delete all` es el peldaño informativo
  haciendo de prefijo de un destructivo.

#### `swiss_S4` — modal dialog
* **Compromiso puesto a prueba:** modal sin caja, con la única hairline como separación.
* **Qué muestra:** una regla de apertura (fila 13, 100 celdas — una más que la de la fila 3, que son 99)
  y **ninguna de cierre**; y la marca de foco del botón destructivo:

  ```
  •  ╲Delete╱      ·   Cancel
  ```

  `•` es `REQUIRED`. Debajo del modal, el tablero desapareció y sólo queda el pager de la fila 31.
* **Objeción:** confirm destructivo. **Criterio observable:** decir dónde termina el modal — no hay
  marca; y decir qué significa `•` — significa «campo obligatorio» dos pantallas antes. `.txt`
  suficiente.
* **Veredicto propuesto: `rework`** — la marca de obligación haciendo de anillo de foco sobre el botón
  irreversible, en una superposición que se abre y no se cierra.

#### `swiss_S5` — live monitor / log
* **Compromiso puesto a prueba:** la escalera de peso como severidad.
* **Qué muestra:**

  ```
    09:41:09 ─ 3 tasks overdue in BACKLOG
    09:41:18 ━ rate limit hit  retry in 30 s
  ```

  `─` (warn) es exactamente `DISCLOSE` y exactamente la celda con que se dibujan las tres hairlines de la
  pantalla.
* **Objeción:** el operador vigila el log. **Criterio observable:** con el color quitado, distinguir una
  fila `warn` de una fila `info` — un guion contra un punto, a una celda, en la misma columna. Se puede,
  pero es el margen más estrecho de los seis lenguajes. El alineamiento de columna es lo que lo salva.
* **Veredicto propuesto: `keep with a note`**.

#### `swiss_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "bold {alert}"` — *«the classic red, and never alone»*.
* **Qué muestra:** `  ━ redirect to task                            enter` — el cursor otra vez en la
  celda de error, y ninguna marca sobre `re`. `swiss_S6.svg`: 1 `<rect>`, 0 `font-weight`.
* **Objeción:** *«never alone»* es exactamente el compromiso que el artefacto no puede verificar: el
  «never alone» era el `bold`, y el `bold` no llega ni al `.txt` ni al `.svg`. **Criterio observable:**
  circular el `re` que casó. No respondible en ningún tier.
* **Veredicto propuesto: `keep with a note`** — inspeccionado, no ejercitado.

---

### 2.3 industrial

Doctrina: `Industrial.__doc__` y LANGUAGES.md §3 — *«~5 flat colours on grey · dense · BOXED GROUPS ·
plain cells. Everything is NUMBERED AND LABELLED; colour codes FUNCTION, not decoration … **FAILS: WHEN
COLOUR MUST CARRY SEVERITY**»*. Por esa última cláusula la severidad es forma: `LEVELS = {"info": "▫▫",
"warn": "▪▪", "error": "■■"}`, `REQUIRED = "▐"`, `DISCLOSE = "▼"`, plato `▐ nn ▌`.

#### `industrial_S1` — list + detail
* **Compromiso puesto a prueba:** *«boxed groups»* — el único de los once cuyo compromiso **pide** caja,
  y por eso el único que dibuja su gutter (`▌ ▐`, dos platos enfrentados, `inc36`).
* **Qué muestra:** el par `▐ … ▌` significa tres cosas distintas en la misma pantalla:

  ```
    ▐ 05 ▌ Audit the theme tokens                      [21d]▌ ▐──────────────────────────────────
                                                            ▌ ▐PROJECT                       ▐ Web ▌
  ```

  plato de código de tarjeta, gutter de paneles, y plato de valor en el panel de detalle. El cursor de
  selección es `▪`, que es la mitad del peldaño `warn` (`▪▪`).
* **Objeción:** **criterio observable:** contar los paneles de la pantalla leyendo sólo los platos —
  salen entre dos y quince según qué `▐` se cuente. La convención es coherente («la tinta mira al
  contenido») pero no es *discriminante*. `.txt` suficiente; el SVG añade que 17 de esos platos tienen
  fondo propio (17 `<rect>`), lo que sí los separa en color.
* **Veredicto propuesto: `keep with a note`** — la nota es que el SVG salva una ambigüedad que el `.txt`
  no salva, y en esta casa el `.txt` es la obra.

#### `industrial_S2` — form with validation
* **Compromiso puesto a prueba:** `REQUIRED = "▐"`, *«the plate, opened»*.
* **Qué muestra:** la marca de obligación y la pared del campo son la misma celda, en la misma fila, a
  ocho espacios:

  ```
    title▐        ▐Fix login| redirect---------------▌
    due▐          ▌12/09/26//////////////////////////▐
                  ■■ expected YYYY-MM-DD
  ```

  Y el estado `INVALID` es el mismo par de platos **girado**: `▌…▐` en vez de `▐…▌`.
* **Objeción:** el operador busca los campos obligatorios. **Criterio observable:** en la fila 4, decir
  cuál de los dos `▐` es la obligación — la respuesta depende de saber que el otro pertenece al control.
  Segundo criterio: decir cuál campo es inválido por la orientación del plato, con el mensaje `■■` tapado.
  `.txt` suficiente para ambos.
* **Veredicto propuesto: `rework`** — hermano exacto del hallazgo (2): la marca de propiedad y la marca
  de estructura comparten celda, y el estado de error se cifra en una orientación.

#### `industrial_S3` — settings
* **Compromiso puesto a prueba:** *«everything is numbered and labelled»* y el plato como notación única.
* **Qué muestra:**

  ```
    DANGER ZONE                                                      ▐ delete every completed task ▌
    ▐ ╱╱Delete all╱╱ ▌   7 tasks, not recoverable
  ```

  El **caption** de la zona de peligro va emplatado exactamente igual que el botón `Cancel` de `S2`
  (`▐   Cancel   ▌`) y que el botón `Delete all` de la fila siguiente.
* **Objeción:** contexto de uso — pantalla de ajustes, hay algo irreversible al fondo. **Criterio
  observable:** señalar los elementos pulsables de las dos últimas filas. Hay dos platos y sólo uno es un
  control; el otro es una frase que describe la consecuencia. `.txt` suficiente y decisivo.
* **Veredicto propuesto: `rework`** — un caption que se lee como control, adyacente a un destructivo. Es
  el hermano invertido del hallazgo (1) que el encargo pedía buscar.

#### `industrial_S4` — modal dialog
* **Compromiso puesto a prueba:** que la tapa del modal sea plato de media celda y no la hairline del
  terminal (`MODAL_BOX = DISPLAY_BOX`, `inc32`).
* **Qué muestra:** la mejor superposición de los seis:

  ```
                               ▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
                               ▌ Delete 3 tasks?                       ▐
                               ▌ ▐_╱╱Delete╱╱_▌   ▐   Cancel   ▌       ▐
                               ▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟
  ```

  La barra de modos sigue en la fila 1, el tablero sigue detrás, la caja cierra por los cuatro lados, y
  el destructivo lleva **hachura** (`╱╱`) que sobrevive a la escala de grises.
* **Objeción:** la que queda es de contraste, no de estructura: `▐_╱╱Delete╱╱_▌` mete cinco notaciones
  en un botón de trece celdas. **Criterio observable:** leer la palabra `Delete` a través de la hachura —
  se lee, porque la hachura va a los lados y no encima.
* **Veredicto propuesto: `keep`** — es el único de los seis modales que conserva el chrome, cierra la
  caja y marca el destructivo por forma.

#### `industrial_S5` — live monitor / log
* **Compromiso puesto a prueba:** la severidad en forma, porque *«el color ya se gastó en identidad»*.
* **Qué muestra:** `▫▫` / `▪▪` / `■■` — el mismo cuadrado en tres tamaños.
* **Objeción:** **criterio observable:** a 12 px de altura de celda, distinguir `▪` de `■` sin verlos
  adyacentes. La diferencia es de unos dos píxeles y **depende de la fuente**, no del lenguaje. Aquí las
  tres aparecen en la misma columna y en la misma pantalla, que es el caso favorable; el caso real es un
  log donde pasan minutos entre un `▪▪` y un `■■`. Además `▪` es el cursor de selección en `S1`/`S3`/`S6`.
  Esto **necesita el tier del SVG o de un terminal real** para juzgarse: el `.txt` los muestra como dos
  code points distintos, que es precisamente lo que un lector no tiene.
* **Veredicto propuesto: `keep with a note`**.

#### `industrial_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "reverse {accent}"` — *«a plate struck over the run»*.
* **Qué muestra:** `  ▪ redirect to task` y `  > ▐re|--------▌`. `industrial_S6.svg` tiene **1 solo
  `<rect>`** (el fondo): el `reverse` no produjo ninguna corrida de fondo. En `S1` el mismo lenguaje
  produce 17.
* **Objeción:** **criterio observable:** circular el `re` que casó. No respondible en ningún tier, y aquí
  el fallo es más duro que en los que usan `bold`, porque `reverse` **sí** es un canal que este
  exportador sabe pintar — lo pinta 17 veces en `S1` — y aun así no aparece.
* **Veredicto propuesto: `keep with a note`** — con la nota de que este caso es *diagnosticable* (§4) y
  los otros no.

---

### 2.4 nord

Doctrina: `Nord.__doc__` y LANGUAGES.md §6 - *«the only language here that INHERITS THE USER'S
ENVIRONMENT instead of overriding it, the app looks like the rest of their terminal … **Fails: when you
need a distinctive identity, BY CONSTRUCTION IT HAS NONE OF ITS OWN**»*. Siete mecanismos
(`field_row`, `DISCLOSE`, `DANGER_FORM`, `LEVELS`, `MATCH_STYLE`, `keyhint`, `overlay`) **vienen de
`Kit`**, y eso está aseverado, no prometido:
`test_nord_declares_the_environment_and_the_declaration_is_checked` camina el MRO y exige que el dueño
sea `Kit`. Su único compromiso propio es el `layout="split"`.

**Por eso nord es el reactivo de esta ronda.** En los otros seis, un defecto puede ser una decisión de
diseño discutible. Aquí no hay decisión: lo que se ve es lo que el kit base hace solo. Un defecto que
aparezca en nord **y** en otros es del kit base, no del lenguaje; y un defecto que sólo aparezca aquí es
la prueba de que «ser el entorno» no basta para una pantalla real.

#### `nord_S1` — list + detail
* **Compromiso puesto a prueba:** el único que este lenguaje se reserva, y viene con su propia medición
  en el docstring: *«colour-stripped at 118×30 nord had NO first fixation … the only isolated element,
  the hero numeral, came FIFTH behind the load plot standing beside it in the same panel»*. El split
  existe para arreglar eso: *«the split gives the eye one subject»*.
* **Qué muestra:** el split, correctamente. Gutter `│` sostenido 27 filas, reglas bajo cada cabecera,
  cursor `▸` consistente entre pestaña, columna y tarjeta. Y en el panel de detalle, la fila 13:

  ```
  ▸   Fix login redirect                                   3d  │ ▇▇▇▇▇▇▇▇▇▇▇▇░░░░░░░░░░░░░░░  44%
  ```

  Veintisiete celdas de bloque sólido, aisladas, en el panel que existe para tener **un** sujeto. El
  sujeto declarado, `DETAIL  Fix login redirect` (fila 4), es texto normal.
* **Objeción:** **criterio observable, y es el del propio lenguaje:** con el color quitado, ordenar los
  elementos del panel de detalle por celdas de tinta y por aislamiento. Gana la barra de carga, no el
  título. **Es exactamente el fallo que el docstring midió y que el split venía a corregir**, reproducido
  un layout más tarde: el load plot volvió a pasar por delante del sujeto. Segunda objeción, menor:
  `BACKLOG 5▂` y `DOING 4▂` pegan un muñón de sparkline al conteo sin espacio, y se lee como artefacto
  de render y no como dato. El `.txt` basta para las dos.
* **Veredicto propuesto: `rework`** - el único compromiso propio del lenguaje no cumple su propia
  métrica en su propia pantalla.

#### `nord_S2` — form with validation
* **Compromiso puesto a prueba:** que las convenciones del terminal basten para un formulario. `REQUIRED`
  es `*` y **eso es una respuesta declarada**, no un hueco: `inc35` §2a asertó `starred == ["nord"]`
  precisamente para que un sexto lenguaje que derive al `*` del base salga rojo.
* **Qué muestra:** el `*` aguanta. Lo que no aguanta son las paredes, que son **tres vocabularios
  distintos en una pantalla**:

  ```
    title*        ▐Fix login▏ redirect▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▌
    due*          ]12/09/26                          [
                  !! expected YYYY-MM-DD
    tags          [ ] api  [x] ui  [x] urgent
    notes         [Redirect drops the ?next= param w▾]
                  ╌    Save    ╌   [   Cancel   ]
  ```

  `▐ … ▌` para el campo editado, `[ … ]` para textarea, checkbox y botón, y `] … [` **hacia afuera**
  para el campo inválido.
* **Objeción:** dos, y la segunda es el hallazgo estructural de la ronda.

  **(a)** **Criterio observable:** tapar la fila 7 y señalar el campo inválido leyendo sólo las paredes.
  Es la misma cifra por orientación que instrument, industrial y blueprint, pero aquí es **peor**, porque
  `] … [` hacia afuera no es una convención de terminal de ninguna clase: no se lee como un estado, se
  lee como un render roto. El lenguaje que se define por ser convencional tiene el chrome de campo más
  inconsistente de los siete.

  **(b)** **Nord no override nada de esto.** Las paredes, `LEVELS` y `DANGER_FORM` son de `Kit`, y hay un
  test que lo obliga. Así que el defecto de `INVALID`-por-orientación aparece en cuatro lenguajes y **el
  cuarto es el que no tomó ninguna decisión**. Eso lo mueve de sitio: no son cuatro diseños discutibles,
  es **un defecto del kit base heredado cuatro veces**. Se arregla una vez, en `Kit`, o se arregla cuatro
  veces mal.
* **Veredicto propuesto: `rework`** - y de los diecinueve, es el que más barato sale de arreglar, porque
  es uno solo.

#### `nord_S3` — settings
* **Compromiso puesto a prueba:** que el idioma del terminal sepa decir «esto es un control» y «esto es
  una frase» sin inventarse nada.
* **Qué muestra:** **lo sabe, y es el único de los siete que lo sabe.** El caption va desnudo y
  flush-right; el botón va entre corchetes:

  ```
    danger zone                                                          delete every completed task
    [ !Delete all! ]   7 tasks, not recoverable
  ```

  Compárese con `industrial_S3` (`▐ delete every completed task ▌`) y `darkside_S3`
  (`▬ delete every completed task`), que emplatan el caption igual que el botón. Y el switch distingue
  tres estados con holgura: `██▌` encendido, `▌──` apagado, `╳╌╌` deshabilitado.
* **Objeción:** `!` bracketeando `Delete all` es `LEVELS["warn"]`, no una marca de destrucción.
  **Criterio observable:** decir si `!Delete all!` es «peligroso» o «hay una advertencia sobre esto». En
  `S5` fila 11, el mismo `!` significa lo segundo.
* **Veredicto propuesto: `keep with a note`** - la nota es el `!`; la separación caption/control es un
  acierto que los otros seis deberían copiar, y es un acierto **del kit base**.

#### `nord_S4` — modal dialog
* **Compromiso puesto a prueba:** el modal del terminal, `┌─┐`, listado en el docstring entre las
  convenciones que este lenguaje hereda a propósito.
* **Qué muestra:** el mejor modal de los siete:

  ```
                               ┌───────────────────────────────────────┐
                               │ Delete 3 tasks?                       │
                               │ ▐  !Delete!  ▌   [   Cancel   ]       │
                               └───────────────────────────────────────┘
  ```

  Barra de modos intacta en la fila 1, tablero detrás, caja cerrada por los cuatro lados, y el
  destructivo separado del seguro **por vocabulario de pared** (`▐ ▌` contra `[ ]`), no sólo por el `!`.
* **Objeción:** que el canal que separa los dos botones es el mismo `▐ ▌` que en `S2` significaba «campo
  en edición». **Criterio observable:** señalar el botón peligroso. Se puede, y por dos canales
  independientes a la vez. Es la objeción más débil de las cuarenta y dos.
* **Veredicto propuesto: `keep`** - y una observación que vale para toda la ronda: la caja redondeada de
  darkside y la caja de plato de industrial son **variaciones sobre esta respuesta**. El original está
  aquí y funciona mejor que las dos.

#### `nord_S5` — live monitor / log
* **Compromiso puesto a prueba:** la escalera `· / ! / !!` del terminal.
* **Qué muestra:** una escalera legible y monótona por cuenta:

  ```
    09:41:09 !  3 tasks overdue in BACKLOG
    09:41:18 !! rate limit hit  retry in 30 s
  ```
* **Objeción, y es la que el coordinador mandó buscar:** `DANGER_FORM` es `!` y `LEVELS["warn"]` es `!`.
  **La misma celda marca una fila de advertencia en el log y un botón de borrado irreversible en `S3` y
  `S4`.** Eso es idéntico a lo que le costó un `rework` a instrument (cuyo `⠇` abre botones y marca
  errores) y a swiss (cuyo `━` es cursor y error), **pero aquí nadie lo señala, porque `!` para las dos
  cosas es la convención del terminal. El entorno no arregla el defecto: lo blanquea.** Esa es la
  respuesta a «dónde esconde el entorno un defecto que los otros revelan».
  **Criterio observable:** enseñar `!` fuera de contexto y preguntar qué significa. Hay dos respuestas y
  ningún canal que las separe salvo la posición.
* **Veredicto propuesto: `keep with a note`** - la escalera funciona; la nota es que este lenguaje
  **hereda la colisión sin poder decidir nada**, y por eso su `!` es evidencia contra `Kit` y no contra
  nord.

#### `nord_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "bold {accent}"`, heredado de `Kit`, el mismo del que
  cuelgan swiss, darkside y blueprint.
* **Qué muestra:** `  ▸ redirect to task                            enter` y cero marca sobre `re`.
  `nord_S6.svg`: 1 `<rect>`, 0 `font-weight`. El cursor `▸` sí es consistente con las pestañas y con
  `S1`/`S3`, que es lo mejor que tiene la pantalla.
* **Objeción:** **criterio observable:** circular el `re`. No respondible en ningún tier. Y aquí la
  atribución vuelve a importar: **este `MATCH_STYLE` es el de `Kit`**, así que el agujero de §4 no es de
  seis lenguajes que eligieron mal, es de uno que eligió y de cinco que heredaron. Nota menor: el campo
  de consulta usa `▐re▏…▌` mientras el textarea de `S2` usa `[ … ]`; la inconsistencia de paredes de
  `S2` también llega aquí.
* **Veredicto propuesto: `keep with a note`** - inspeccionado, no ejercitado.

---

### 2.5 darkside

Doctrina: `Darkside.__doc__` y LANGUAGES.md §8 — *«achromatic + ONE RESERVED ACCENT · airy · **DEPTH BY
±1 GREY STEP, NEVER BORDERS** · plain cells · clinical-warm … the accent marks interactivity, NOTHING
ELSE … hierarchy by WEIGHT AND DIMMING, not size … **BORDERS ARE RESERVED FOR MODALS**»*.
`LEVELS = {"info": "·", "warn": "o", "error": "O"}`, `REQUIRED = "▪"`, `RAIL = "▏"`.

#### `darkside_S1` — list + detail
* **Compromiso puesto a prueba:** *«never borders»*, y el rechazo del gutter que `inc36` derivó de él:
  *«two panes are two regions, and this language has exactly one answer»* — `depth_ground()`.
* **Qué muestra:** el gutter no está en el `.txt` (*«a background is not a cell»*, dice el propio
  método). Lo que sí está, catorce veces, es un trazo vertical:

  ```
    ▏  backlog 5                                                 detail  fix login redirect
      ▏  audit the theme tokens                           21d
  O ▏  doing 4                                                   status                         ▬ open
  ```
* **Objeción:** el lenguaje se prohibió el trazo vertical **en el único sitio donde hacía falta** y lo
  imprime catorce veces donde no. **Criterio observable:** con el `.txt` delante, señalar la separación
  entre el tablero y el panel de detalle — no existe; el operador tiene que inferirla del salto de
  columna. En el `.svg` **sí** existe (28 `<rect>` de escalón gris), y ahí está el problema: los dos
  tiers cuentan estructuras distintas de la misma pantalla, y la convención de la casa es que el `.txt`
  es la obra.
* **Veredicto propuesto: `rework`** — no por el escalón gris, que es doctrina limpia, sino porque el
  `.txt` es un artefacto **estructuralmente incompleto** de esta pantalla y esta ronda lo publica como si
  no lo fuera. O el rail cede, o el `.txt` deja de ser la obra para este lenguaje, y eso es un veredicto
  del operador.

#### `darkside_S2` — form with validation
* **Compromiso puesto a prueba:** que el acento marque interactividad **y nada más**, lo que obliga a que
  obligación y severidad vivan en la escalera de peso.
* **Qué muestra:** `▬` con seis significados en 18 filas — leader de `field_row` (`S1`), pared de botón,
  pared de select, segmento de switch encendido, relleno de slider, prefijo de caption (`S3`):

  ```
    title▪        ▮Fix login◆ redirect···············▮
    due▪          Ø12/09/26                          Ø
                  O  expected YYYY-MM-DD
                  ╌    Save    ╌   ▬   Cancel   ▬
  ```

  A favor: `▪` (obligación), `╌` (deshabilitado) y `▬` (normal) **sí** son tres formas distintas, y `Ø`
  para inválido es una forma, no una orientación. Este es el mejor `S2` de los seis en ese eje.
* **Objeción:** **criterio observable:** decir qué significa `▬` señalando una ocurrencia cualquiera —
  hay seis respuestas. Pero ninguna de las seis lleva a una acción equivocada en esta pantalla.
* **Veredicto propuesto: `keep with a note`** — sobrecarga sin consecuencia de acto, aquí.

#### `darkside_S3` — settings
* **Compromiso puesto a prueba:** el acento reservado a lo interactivo.
* **Qué muestra:** el caption y el botón destructivo abren con la misma celda, en filas consecutivas:

  ```
    danger zone                                                        ▬ delete every completed task
    ▬ ØDelete allØ ▬   7 tasks, not recoverable
  ```
* **Objeción:** idéntica a `industrial_S3`, y con el agravante de que aquí `▬` es además la pared de
  botón de `S2`. **Criterio observable:** señalar los pulsables de las dos últimas filas. `.txt`
  suficiente.
* **Veredicto propuesto: `rework`** — caption que se lee como control, junto a un irreversible.

#### `darkside_S4` — modal dialog
* **Compromiso puesto a prueba:** la excepción escrita en la propia doctrina — *«borders are RESERVED for
  modals»* — y que un sistema clinical-warm **redondea** su única caja.
* **Qué muestra:** el gasto exacto de esa reserva, una vez:

  ```
                               ╭───────────────────────────────────────╮
                               │ Delete 3 tasks?                       │
                               │ ▮  ØDeleteØ  ▮   ▬   Cancel   ▬       │
                               ╰───────────────────────────────────────╯
  ```

  Chrome intacto en la fila 1, tablero detrás, destructivo en `Ø…Ø` (forma, no color), foco en `▮`.
* **Objeción:** dos trazos verticales en la pantalla, `▏` (rail) y `│` (modal). **Criterio observable:**
  distinguirlos — se distinguen, `▏` está pegado al borde izquierdo de su celda y `│` centrado; y además
  no comparten columna. Es la objeción más débil de la ronda.
* **Veredicto propuesto: `keep`** — la única caja del lenguaje, gastada donde su doctrina la reservó.

#### `darkside_S5` — live monitor / log
* **Compromiso puesto a prueba:** severidad acromática por forma, porque el acento está prohibido y el
  matiz también.
* **Qué muestra:** `·` / `o` / `O` — un punto, un anillo, un anillo grande.
* **Objeción:** **criterio observable:** con todo el color quitado, ordenar por gravedad. Se puede: la
  progresión es de área y es monótona. Nota: `O` es además el cursor de selección (`S1`, `S6`), la
  perilla del switch (`S3`) y el radio marcado (`S2`) — pero en esta pantalla, sola, la escalera hace lo
  que promete.
* **Veredicto propuesto: `keep`**.

#### `darkside_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "bold {ink}"` en un lenguaje **acromático por
  compromiso**.
* **Qué muestra:** `  O redirect to task` — el cursor es la celda de error — y cero marca sobre `re`.
  `darkside_S6.svg`: 1 `<rect>`, 0 `font-weight`.
* **Objeción:** este es el peor `S6` de los seis y por una razón estructural, no de exportador: en un
  lenguaje que ha renunciado al matiz, `bold {ink}` **es peso y nada más**. Un terminal que renderiza
  `bold` como «más brillante» (el comportamiento por defecto de buena parte de ellos) le deja a este
  lenguaje **cero canales** para el match. **Criterio observable:** circular el `re`. No respondible en
  ningún tier, y aquí tampoco sería respondible en el terminal real bajo una configuración común.
* **Veredicto propuesto: `rework`** — el único `S6` donde el mecanismo no sólo es inobservable en el
  artefacto sino probablemente inobservable en el destino.

---

### 2.6 solari

Doctrina: `Solari.__doc__` y LANGUAGES.md §10 — *«amber on near-black, rationed · dense · **THE SEAM IS
THE WHOLE DIVIDER VOCABULARY** · flap-cell digits · public-signage. A STATE IS A WORD IN A STATUS
COLUMN … headers are BANDS IN REVERSE VIDEO … tabular fields PADDED TO THEIR WIDEST CONTENT»*.
`SEAM = "▁"`, `REQUIRED = "▁"`, `LEVELS = {"info": "OK ", "warn": "DLY", "error": "CNX"}`,
`DANGER_FORM = ("▀", "▄")`.

#### `solari_S1` — list + detail
* **Compromiso puesto a prueba:** *«a state is a WORD in a status column»* y *«tabular fields padded to
  their widest content»*.
* **Qué muestra:** el mejor uso de palabra-como-estado de los once:

  ```
      03  FIX LOGIN REDIRECT                    BOARDING  HIGH   OWNER ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ jav201
      02  RATE-LIMIT THE API                    LATE      HIGH   DONE 007 OF 016  044%
  ```

  `ON TIME` / `BOARDING` / `LATE` sobreviven a la escala de grises perfectamente, porque son texto.
* **Objeción:** cada fila de tarea gasta **dos** filas (la fila y su costura, `    ▁▁▁▁▁…`), así que en
  32 filas caben seis tareas de dieciséis, y `GATE DONE 07` (fila 23) aparece con su cabecera y nada
  debajo. **Criterio observable:** contar cuántas de las 16 tareas están en pantalla — seis. La costura
  es doctrina; el coste es la mitad del tablero. `.txt` suficiente.
* **Veredicto propuesto: `keep with a note`** — la nota es de densidad, no de mecanismo: el compromiso se
  paga con la mitad de la superficie útil.

#### `solari_S2` — form with validation
* **Compromiso puesto a prueba:** *«this language HAS one divider and spends it everywhere»* — el
  argumento con que `inc35` justificó `REQUIRED = "▁"`, la misma celda que `SEAM`.
* **Qué muestra:** `▁` haciendo **nueve** trabajos en una pantalla:

  ```
    title▁        ▔Fix login▮ redirect▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▔
    due▁          ═12/09/26··························═
                  CNX expected YYYY-MM-DD
    priority      ▁▁▁ low  ▁▁▁ norm  ▁●▁ high
    tags          ▁ ▁ OFF api  ▁▼▁ ON  ui  ▁▼▁ ON  urgent
    notes         ▁Redirect drops the ?next= param w═▁
                  ╌    Save    ╌   ▁   Cancel   ▁
  ```

  marca de obligación · relleno de campo · corchete de radio · corchete de checkbox · pared de textarea ·
  pared de select · pared de botón · regla de cabecera (fila 3, 100 celdas) · costura de fila.
* **Objeción:** **criterio observable, y es el más nítido de la ronda:** «señala los campos obligatorios».
  `▁` aparece más de sesenta veces en esta pantalla y dos de ellas son la respuesta. No hay lectura
  posible que no sea posicional (pegado al final del caption). `.txt` suficiente y devastador.
* **Veredicto propuesto: `rework`** — el argumento doctrinal («una costura, gastada en todas partes») es
  sólido y aun así produce una pantalla donde la obligación es indistinguible de la decoración. Es
  exactamente el caso que el encargo pedía buscar, en su forma extrema.

#### `solari_S3` — settings
* **Compromiso puesto a prueba:** *«a state is a WORD»*, aplicado a un switch.
* **Qué muestra:** el único switch de los seis legible con **todos** los glifos borrados:

  ```
    notify on overdue         ▁▁▼ ON
    sound                     ▼·· OFF
    sync to remote            ▽╌╌ OFF   (no remote configured)
  ```

  Encendido, apagado y deshabilitado difieren en la aleta (`▼` llena / `▽` hueca), en el relleno
  (`▁▁` / `··` / `╌╌`) **y** en la palabra.
* **Objeción:** `▁` sigue sobrecargado (la costura de la `DANGER ZONE`, fila 19, y las paredes del botón
  `▁ ▀Delete all▄ ▁`). **Criterio observable:** decir el estado de los cinco switches sin ver glifos —
  respondible, y en ningún otro lenguaje de los seis lo es.
* **Veredicto propuesto: `keep`** — redundancia de tres canales para un estado binario; es lo que la
  doctrina promete y lo cumple.

#### `solari_S4` — modal dialog
* **Compromiso puesto a prueba:** modal sin regla, con la costura como toda separación.
* **Qué muestra:** el modal **se comió las ocho primeras filas de la pantalla**. Compárese con
  `solari_S1`, cuyas filas 1-8 son la tira de modos, el masthead, la regla y el `GATE BACKLOG`:

  ```
  fila 1  (vacía)
  fila 2  Delete 3 tasks?
  fila 7  ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
  fila 8  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁… (100 celdas)
  fila 9  PRIORITY ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ high
  ```

  La fila 9 de `S4` es la fila 9 de `S1`, byte a byte. El modal no se superpuso: **desplazó y descartó**.
  El operador pierde la tira de modos, el masthead y el `GATE BACKLOG` — el gate del que se van a borrar
  las tres tareas — y lo que queda arranca a mitad del panel de detalle.
* **Objeción:** contexto de uso — confirmación destructiva. **Criterio observable:** con el frame
  delante, decir en qué modo está la aplicación y de qué gate se borra. Ninguna de las dos es
  respondible. Los otros cinco lenguajes conservan la fila 1 en `S4`; este es el único que la pierde.
  `.txt` suficiente y decisivo.
* **Veredicto propuesto: `rework`** — es el defecto más grave de los 42 y no es de doctrina: es de
  composición.

#### `solari_S5` — live monitor / log
* **Compromiso puesto a prueba:** *«quantity is DIGITS in flap cells, never a bar»* (DATAVIZ law 1) y la
  columna de estado como palabra.
* **Qué muestra:** las dos mitades del compromiso, y salen con signo opuesto:

  ```
    rate    1212123211222122  ceiling 10
    09:41:09 DLY 3 tasks overdue in BACKLOG
    09:41:18 CNX rate limit hit  retry in 30 s
  ```

  El log es el mejor de los once: `OK` / `DLY` / `CNX` no dependen de ningún canal gráfico. La
  sparkline es dieciséis dígitos.
* **Objeción:** **criterio observable:** «¿en qué momento subió la tasa?». Sobre `▂▄▂▄▂▄█▄` la respuesta
  es una fijación; sobre `1212123211222122` es una lectura dígito a dígito de dieciséis caracteres, y la
  forma —que es la razón de existir de una sparkline— no está. La ley DATAVIZ 1 se cumple y la tarea se
  pierde. Segunda objeción, menor: `CNX` («cancelado») como peldaño de error junto a un campo de fecha
  (`S2`, fila 7) se lee como «el vuelo se canceló», no como «el valor es inválido».
* **Veredicto propuesto: `keep with a note`** — dos mecanismos de calidad opuesta en una pantalla; la
  nota nombra la sparkline.

#### `solari_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "reverse {ink}"` — *«a band, which is this board's
  mark»* — y la ley de contenido byte a byte (ruling 9 de `PROTOTYPE.md` §4).
* **Qué muestra:** `solari_S6.svg` tiene 3 `<rect>`: el fondo, la banda de la pestaña (`x=10 y=10
  w=58.8`) y la banda del masthead (`x=10 y=27 w=840`). **Ninguna sobre una fila de resultado.** Y la
  cabecera recasea la consulta mientras el campo no:

  ```
  fila 2   COMMAND  QUERY 'RE'  ·  6 RESULTS
  fila 4   > ▔re▮▁▁▁▁▁…▔
  fila 16      NO DEPARTURES
  ```
* **Objeción:** tres. La banda del match no existe; la misma cadena aparece en dos casings en la misma
  pantalla; y el estado vacío dice `NO DEPARTURES` para «ningún comando casó con `zzq`», donde la
  metáfora deja de ayudar y empieza a mentir. **Criterio observable** para la tercera: leer la fila 16 y
  decir qué pasó — la respuesta correcta es «la búsqueda no encontró nada», no «no hay salidas».
* **Veredicto propuesto: `keep with a note`**.

---

### 2.7 blueprint

Doctrina: `Blueprint.__doc__` — *«NOTHING IS BOXED, at any width … los únicos glifos de dibujo que este
lenguaje traza son `─ ━ ├ ┤ ╌`, `┌ ┐ └ ┘` y la hachura — DIEZ, y ninguno es un trazo vertical»*;
*«emphasis is KNOCKOUT: **exactly ONE element per view** reverses to a pale ground with dark ink, and it
is the title block's STATE cell. That is the first-fixation law here»*. `REQUIRED = "├"`.

#### `blueprint_S1` — list + detail
* **Compromiso puesto a prueba:** la ley de primera fijación — *«exactamente un elemento por vista se
  invierte, y es la celda STATE del title block»*.
* **Qué muestra:** **no se invierte ninguno.** `blueprint_S1.svg` contiene un solo `<rect>` (el fondo de
  la hoja) y el title block se dibuja en tinta normal:

  ```
  <text x="287.2" y="533.3" fill="#7fa8c4">├ CLEAR ┤</text>
  ```

  Lo mismo en `S2`, `S3`, `S5` y `S6`. Y el cursor de selección es una marca de registro, la misma
  familia que las cuatro esquinas del title block de las filas 30 y 32:

  ```
  ┌ DOING                                     ├ 04 ─┤
  ┌   FIX LOGIN REDIRECT                      ├───┤ 03D
  ```
* **Objeción:** **criterio observable:** «¿dónde cae la primera fijación en esta hoja?». La ley del
  lenguaje da una respuesta (`CLEAR`) y el frame no la implementa, así que la respuesta real es «donde
  caiga». Y esto **sólo se ve en el tier del SVG**: en el `.txt` el knockout nunca fue visible, así que
  su ausencia tampoco. Ese es el punto — `PROTOTYPE.md` §3 ya lo dijo (*«el knockout de blueprint es
  invertir el fondo, y el `.txt` no lo lleva … la convención de la casa es que el `.txt` es la obra —
  aquí no basta»*) y esta ronda encuentra que en el tier donde sí bastaría, tampoco está.
* **Veredicto propuesto: `rework`** — el mecanismo firma del lenguaje no se renderiza en cinco de sus
  seis frames.

#### `blueprint_S2` — form with validation
* **Compromiso puesto a prueba:** `REQUIRED = "├"` sobre un alfabeto de diez glifos donde `├` ya es el
  terminador de apertura de toda cota.
* **Qué muestra:** la marca de obligación es el terminador de cota, y dos controles adyacentes usan el
  mismo par en orientaciones opuestas para decir lo mismo:

  ```
    title├        ╞Fix login╪ redirect╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╡
    due├          ┤12/09/26··························├
                  ━━ expected YYYY-MM-DD ╌╌╌╌╌╌╌╌╌╌╌…
    priority      ┤ ├ low  ┤ ├ norm  ┤○├ high
    tags          ├ ┤ api  ├╪┤ ui  ├╪┤ urgent
                  ╎    Save    ╎   ├   Cancel   ┤
  ```

  Radio vacío `┤ ├`, checkbox vacío `├ ┤`. Y el campo inválido (`due`) abre con `┤` y cierra con `├` —
  el par de la cota, girado.
* **Objeción:** **criterio observable:** en la fila 3, decir si `title├` es una obligación o el comienzo
  de una cota cuya cifra no llegó. En la hoja de `S1` `├` abre siete cotas (`├── 09D ──┤`), así que el
  lector ya tiene la otra respuesta aprendida. Segundo criterio: distinguir radio de checkbox por su
  forma vacía — la única diferencia es hacia dónde apuntan los terminadores. `.txt` suficiente.
* **Veredicto propuesto: `rework`** — hermano del hallazgo (2): la marca de obligación es la celda que
  el lenguaje gasta en medir, y el estado vacío de dos componentes se cifra en una orientación.

#### `blueprint_S3` — settings
* **Compromiso puesto a prueba:** que la cota sirva para todo, incluido un estado binario.
* **Qué muestra:** la señal de estado más estrecha de la ronda:

  ```
    notify on overdue         ├─┤
    sound                     ├┤·
    sync to remote            ├╎╌   (no remote configured)
    row density               ├────────┤···· 70
    ├ ━Delete all━ ┤   7 tasks, not recoverable
  ```

  Encendido y apagado difieren en **una celda de hairline**. Y el botón destructivo usa `━`, que es
  `LEVELS["error"]` (`S5`, fila 12: `09:41:18 ━━ rate limit hit`).
* **Objeción:** **criterio observable:** decir cuáles de los cinco switches están encendidos, a un metro
  de la pantalla. `├─┤` contra `├┤·` es una diferencia de un carácter en tres. `.txt` suficiente; el SVG
  no ayuda porque el canal es la forma y no hay fondo.
* **Veredicto propuesto: `rework`** — el estado binario más frecuente de la aplicación cifrado en una
  celda, en el lenguaje más claro de los seis en todo lo demás.

#### `blueprint_S4` — modal dialog
* **Compromiso puesto a prueba:** *«las cuatro esquinas de registro no se tocan»* (rechazo declarado de
  tapa de modal) **y** la ley de un solo knockout por vista.
* **Qué muestra:** el `.txt` y el `.svg` **no coinciden en qué controles hay**:

  ```
  .txt   fila 17:                             DELETE    ├  CANCEL  ┤
  .svg   <rect x="236.8" y="282.0" width="67.2" height="17.0" fill="#eef4f8"/>
         <text x="236.8" y="295.3" fill="#123a5c"> DELETE </text>
  ```

  En el `.txt`, `DELETE` es una palabra desnuda y `CANCEL` es lo único que parece un botón. En el `.svg`,
  `DELETE` es el knockout de la vista —tinta oscura sobre fondo pálido— y por tanto el punto de primera
  fijación. Los dos artefactos dicen lo contrario el uno del otro sobre el control irreversible.
* **Objeción:** **criterio observable:** leyendo sólo el `.txt`, señalar los botones del confirm. Sale
  uno, y es el seguro. Es el mismo error que `swiss_S2` (`Save` desnudo) pero sobre la acción destructiva
  y con foco. **Este bloque necesita el tier del SVG obligatoriamente** — y el hecho de que lo necesite
  es la objeción, no un detalle de método.
* **Veredicto propuesto: `rework`** — y con él, la pregunta 10 de `PROTOTYPE.md` §4 vuelve a la mesa del
  operador: el knockout **ya se movió** del title block al confirm (§0b), la ley de «exactamente uno por
  vista» se respeta, y nadie lo aprobó.

#### `blueprint_S5` — live monitor / log
* **Compromiso puesto a prueba:** que la escalera de severidad sea peso de trazo dentro del vocabulario
  de cota.
* **Qué muestra:** `··` / `╌╌` / `━━`, y una sparkline en las mismas celdas:

  ```
    rate    ╌─╌─╌─━─╌╌───╌──  ceiling 10
    09:41:18 ━━ rate limit hit  retry in 30 s
  ```

  El pico de la traza es la celda de error del log de dos filas más abajo.
* **Objeción:** **criterio observable:** decir si `━` en la fila 5 significa «pico» o «error». En esta
  pantalla significa las dos cosas a seis filas de distancia. Es un lugar donde la coincidencia es casi
  afortunada (un pico de tasa **es** lo que causa el error de la fila 12), pero es coincidencia del
  fixture, no mecanismo. Nota adicional: sin knockout en la hoja (§`blueprint_S1`), esta pantalla no
  tiene punto de primera fijación.
* **Veredicto propuesto: `keep with a note`**.

#### `blueprint_S6` — command palette
* **Compromiso puesto a prueba:** `MATCH_STYLE = "bold {ink}"` — *«the heavy weight, in type»* — sobre un
  lenguaje cuya croma es casi cero por diseño (*«`ink`, `mut` y `dim` son una sola familia cian»*).
* **Qué muestra:** `  ┌ redirect to task` y cero marca sobre `re`. `blueprint_S6.svg`: 1 `<rect>`, 0
  `font-weight`. El vocabulario de cota sí aguanta: `  > ╞re╪╌╌╌…╌╡`.
* **Objeción:** **criterio observable:** circular el `re`. No respondible en ningún tier. Con la croma
  casi a cero por compromiso, `bold {ink}` está en la misma situación que darkside — con la diferencia de
  que aquí el lenguaje **sí** tiene un canal estructural disponible y sin gastar en esta vista: el
  knockout, que no se usa en ninguna parte (§`blueprint_S1`).
* **Veredicto propuesto: `keep with a note`** — con la observación de que la respuesta propia de este
  lenguaje al match está escrita en su propia doctrina y sin usar.

---

## 3. La tabla de tinta

### 3a. `verify_ink.py`, ejecutado — y lo que mide no son estos frames

`python -X utf8 prototypes/verify_ink.py` mide **el widget del tablero en vivo**, 11 lenguajes × 3
clases de tamaño = 33 medidas, contra `prototypes/out/_fixture_late.json`. **No mide los 42 frames de
esta ronda ni los 66 del repo.** El «darkside S6 a 8,3 %» que el encargo esperaba **no puede salir de
esta herramienta**: sale del barrido de frames de `inc37`. Se registran las dos cosas.

Se corrió **dos veces**, y las dos corridas son la evidencia de la limitación que el propio docstring
declara (*«run-to-run variance of several points … the cause is NOT established»*):

```
                 glance            widget             board
language     run1   run2       run1   run2       run1   run2
corgi        24.6   24.6       45.4   45.4       47.0   47.0
naught       37.4   37.4       48.8   48.8       37.6   37.7
instrument   23.1   23.1       26.5   26.5       34.6   34.7
swiss        17.3   17.3       25.7   25.8       21.2   21.2
industrial   14.8   14.8       37.2   37.4       50.8   50.8
nord         20.5   20.2       29.7   29.6       29.4   29.3
darkside     14.8   14.8       23.3   23.5       13.4   13.4
prism        39.2   39.2       46.5   46.5       32.4   32.5
ledger       10.8   10.6       27.4   27.4       35.6   35.7
solari       12.1   11.5       20.0   19.7       30.3   30.1
blueprint    10.8   10.4       21.6   21.3       21.1   20.7
```

`DENSITY.md` floor: 35 % en superficie *glance*. **Por debajo del piso: 9 de 11**, en las dos corridas.
La deriva máxima observada es **0,6 puntos** (`solari` glance, 12,1 → 11,5) sin cambiar nada entre
corridas. **La tabla no puede usarse como umbral de aceptación** hasta que la varianza esté fijada; eso
es la nota del propio script y esta ronda la confirma con dos muestras en vez de una.

### 3b. Los 66 frames, con la fórmula del propio `verify_ink.ink_fraction`

`(celdas no-espacio / celdas totales)` sobre los 66 `.txt`, 100×32. Determinista (son archivos), así que
no tiene varianza. Las seis filas de `inc37` se reproducen exactamente.

```
lang              S1      S2      S3      S4      S5      S6    media
naught         29.2%   15.1%   13.6%   35.0%   14.5%   12.5%    20.0%
corgi          27.0%   14.4%   15.7%    2.7%   17.8%   15.4%    15.5%
instrument     36.0%   13.2%   13.6%   34.1%   14.6%   14.9%    21.1%
swiss          16.4%   11.4%   14.6%   18.6%   17.1%   14.0%    15.4%
industrial     24.0%   13.9%   15.4%   23.0%   17.8%   15.1%    18.2%
nord           19.3%    8.5%   11.7%   19.9%   14.2%   12.7%    14.4%
darkside       13.1%    8.7%    8.9%   14.4%   11.3%    8.3%    10.8%
prism          16.7%   10.6%    8.9%   18.2%   11.4%   11.8%    12.9%
ledger         47.5%   18.1%   19.2%   48.8%   19.5%   16.6%    28.3%
solari         33.5%   13.7%   13.8%   23.6%   14.5%   11.2%    18.4%
blueprint      22.4%   13.1%   11.3%   19.4%   12.3%   10.4%    14.8%
```

* **Piso de los 66: `corgi_S4` a 2,7 %** — no `darkside_S6`. Corgi rehúsa el overlay por doctrina («el
  modo se apodera de la pantalla»), así que su modal es una pantalla casi vacía. `darkside_S6` a **8,3 %**
  es el piso **de los seis de esta ronda**, como decía el encargo, y el segundo de los 66.
* **Techo: `ledger_S4` a 48,8 %.**
* 62 de 66 quedan bajo el 35 %, **y eso no es un fallo**: el piso de `DENSITY.md` está escrito para una
  superficie *glance*, y estos son frames de 100×32 con una sola pantalla de aplicación. Publicar «62
  fallos» sería la lectura falsa. Lo que sí dice la tabla es la **firma** de cada lenguaje: ledger e
  instrument densos por compromiso, darkside y prism aireados por compromiso, y la columna `S4` como la
  más bimodal de las seis (2,7 % a 48,8 %) porque es donde cada lenguaje decide qué hace con lo que hay
  detrás.

---

## 4. Un hallazgo que no cabe en ninguna celda: `Kit.match` no es observable en los 42

`S6` existe para probar `Kit.match` (`inc19`, con su ley de contenido byte a byte). En los siete
lenguajes, el mecanismo es de **estilo**, no de glifo, y **`nord` prueba de quién es la decisión**: su
`MATCH_STYLE` es el de `Kit` sin tocar, así que la fila de abajo no es un lenguaje que eligió mal, es la
línea base contra la que los otros seis eligieron:

| lenguaje | `MATCH_STYLE` | ¿en el `.txt`? | ¿en el `.svg`? |
|---|---|---|---|
| instrument | `underline {accent}` | no | **no** — 0 `text-decoration` |
| swiss | `bold {alert}` | no | **no** — 0 `font-weight` |
| industrial | `reverse {accent}` | no | **no** — 1 `<rect>` en `S6`, y 17 en `S1` |
| nord | `bold {accent}` **(de `Kit`)** | no | **no** |
| darkside | `bold {ink}` | no | **no** |
| solari | `reverse {ink}` | no | **no** — 3 `<rect>` en `S6`, ninguno sobre un resultado |
| blueprint | `bold {ink}` | no | **no** |

La causa está en el exportador y está documentada en él: `capture_languages.svg_from_grid` emite
**corridas de fondo y colores de relleno**, y nada más — ni `font-weight` ni `text-decoration`. Los siete
`.svg` de `S6` juntos tienen 9 `<rect>`, de los cuales 7 son el fondo de la hoja.

**Consecuencia para esta ronda, dicha como límite y no como veredicto:** ningún criterio sobre peso,
subrayado o inversión de una corrida corta puede juzgarse desde estos artefactos. Los siete `S6` quedan
*inspeccionados, no ejercitados*, y los dos casos donde el canal es `reverse` (industrial, solari) son
además **diagnosticables**: el exportador sabe pintarlo y no lo pintó, así que ahí hay un defecto que
un test puede atrapar.

---

## 5. Lo que esta ronda no puede ver

Esta ronda leyó **archivos estáticos**: 36 `.txt`, 36 `.svg` y 36 `.candidates.md`. **No se ejecutó la
aplicación, no se pulsó ninguna tecla, no se movió ningún foco y no se cambió ningún estado.** Todo lo de
arriba es un recorrido cognitivo sobre imágenes fijas, con criterios declarados. Lo siguiente queda
fuera, por construcción:

1. **Los tiers de color.** El `.svg` lleva rellenos y fondos; el `.txt` no lleva ninguno. Ninguno de los
   dos lleva peso ni subrayado (§4). Un criterio de contraste (`alert` contra `ink` a 1,8:1, el número
   que el propio docstring de solari cita) **no es medible aquí**.
2. **El movimiento del foco.** `FOCUSED` aparece en los frames como una decoración fija. Qué pasa al
   pulsar `tab`, si el anillo salta donde el lector espera, y si el orden de tabulación coincide con el
   orden visual — ninguna de las tres es respondible desde un frame. Todo lo dicho sobre «el botón
   destructivo está enfocado» se leyó de una marca, no de un foco.
3. **El asentamiento a 8 lecturas** (`capture_languages.settle`). Los frames son la lectura estable;
   qué se ve en las siete anteriores, y si algún lenguaje parpadea en una de ellas, es invisible aquí.
4. **El comportamiento en otros anchos.** Los 36 están a 100×32. Los compromisos que hablan «at any
   width» (blueprint: *«nothing is boxed, AT ANY WIDTH»*; swiss: `MEASURE_MIN = 24`) se juzgaron a un
   solo ancho. `inc36` encontró un defecto real de blueprint a `w=1` que ningún test al ancho de diseño
   veía; el mismo agujero sigue abierto para los frames.
5. **La animación y la latencia.** Los frames se capturaron con `animations off`. El estado `held` del
   log (`held -- space resumes`), lo que se ve mientras el log corre, y el coste de repintado por frame
   no están aquí.
6. **La densidad como se experimenta.** §3b es aritmética de celdas. Que una pantalla al 47,5 % se sienta
   llena y una al 8,3 % se sienta vacía es una hipótesis razonable y **no una medición**.
7. **Usuarios reales.** ISO 9241-210 pide evaluación con usuarios; este equipo es una persona. Lo que hay
   aquí es **inspección con criterios declarados**, no un estudio. **No se hizo ninguna evaluación con
   usuarios reales, y ninguna afirmación de este documento debe leerse como si se hubiera hecho.**
8. **La atribución, cuando el defecto es de `Kit`.** Nord muestra qué hace el kit base solo, pero
   **no muestra qué haría otro lenguaje si `Kit` cambiara**: los seis restantes overridean cantidades
   distintas de la superficie, y esta ronda no reejecutó nada. Que arreglar `INVALID` en `Kit` arregle
   los cuatro frames es una **inferencia**, no una medición, y hay que rendirla antes de creerla.

---

## 6. Los 42 frames

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| instrument | [txt](instrument_S1.txt) · [svg](instrument_S1.svg) · [cand](instrument_S1.candidates.md) | [txt](instrument_S2.txt) · [svg](instrument_S2.svg) · [cand](instrument_S2.candidates.md) | [txt](instrument_S3.txt) · [svg](instrument_S3.svg) · [cand](instrument_S3.candidates.md) | [txt](instrument_S4.txt) · [svg](instrument_S4.svg) · [cand](instrument_S4.candidates.md) | [txt](instrument_S5.txt) · [svg](instrument_S5.svg) · [cand](instrument_S5.candidates.md) | [txt](instrument_S6.txt) · [svg](instrument_S6.svg) · [cand](instrument_S6.candidates.md) |
| swiss | [txt](swiss_S1.txt) · [svg](swiss_S1.svg) · [cand](swiss_S1.candidates.md) | [txt](swiss_S2.txt) · [svg](swiss_S2.svg) · [cand](swiss_S2.candidates.md) | [txt](swiss_S3.txt) · [svg](swiss_S3.svg) · [cand](swiss_S3.candidates.md) | [txt](swiss_S4.txt) · [svg](swiss_S4.svg) · [cand](swiss_S4.candidates.md) | [txt](swiss_S5.txt) · [svg](swiss_S5.svg) · [cand](swiss_S5.candidates.md) | [txt](swiss_S6.txt) · [svg](swiss_S6.svg) · [cand](swiss_S6.candidates.md) |
| industrial | [txt](industrial_S1.txt) · [svg](industrial_S1.svg) · [cand](industrial_S1.candidates.md) | [txt](industrial_S2.txt) · [svg](industrial_S2.svg) · [cand](industrial_S2.candidates.md) | [txt](industrial_S3.txt) · [svg](industrial_S3.svg) · [cand](industrial_S3.candidates.md) | [txt](industrial_S4.txt) · [svg](industrial_S4.svg) · [cand](industrial_S4.candidates.md) | [txt](industrial_S5.txt) · [svg](industrial_S5.svg) · [cand](industrial_S5.candidates.md) | [txt](industrial_S6.txt) · [svg](industrial_S6.svg) · [cand](industrial_S6.candidates.md) |
| nord | [txt](nord_S1.txt) · [svg](nord_S1.svg) · [cand](nord_S1.candidates.md) | [txt](nord_S2.txt) · [svg](nord_S2.svg) · [cand](nord_S2.candidates.md) | [txt](nord_S3.txt) · [svg](nord_S3.svg) · [cand](nord_S3.candidates.md) | [txt](nord_S4.txt) · [svg](nord_S4.svg) · [cand](nord_S4.candidates.md) | [txt](nord_S5.txt) · [svg](nord_S5.svg) · [cand](nord_S5.candidates.md) | [txt](nord_S6.txt) · [svg](nord_S6.svg) · [cand](nord_S6.candidates.md) |
| darkside | [txt](darkside_S1.txt) · [svg](darkside_S1.svg) · [cand](darkside_S1.candidates.md) | [txt](darkside_S2.txt) · [svg](darkside_S2.svg) · [cand](darkside_S2.candidates.md) | [txt](darkside_S3.txt) · [svg](darkside_S3.svg) · [cand](darkside_S3.candidates.md) | [txt](darkside_S4.txt) · [svg](darkside_S4.svg) · [cand](darkside_S4.candidates.md) | [txt](darkside_S5.txt) · [svg](darkside_S5.svg) · [cand](darkside_S5.candidates.md) | [txt](darkside_S6.txt) · [svg](darkside_S6.svg) · [cand](darkside_S6.candidates.md) |
| solari | [txt](solari_S1.txt) · [svg](solari_S1.svg) · [cand](solari_S1.candidates.md) | [txt](solari_S2.txt) · [svg](solari_S2.svg) · [cand](solari_S2.candidates.md) | [txt](solari_S3.txt) · [svg](solari_S3.svg) · [cand](solari_S3.candidates.md) | [txt](solari_S4.txt) · [svg](solari_S4.svg) · [cand](solari_S4.candidates.md) | [txt](solari_S5.txt) · [svg](solari_S5.svg) · [cand](solari_S5.candidates.md) | [txt](solari_S6.txt) · [svg](solari_S6.svg) · [cand](solari_S6.candidates.md) |
| blueprint | [txt](blueprint_S1.txt) · [svg](blueprint_S1.svg) · [cand](blueprint_S1.candidates.md) | [txt](blueprint_S2.txt) · [svg](blueprint_S2.svg) · [cand](blueprint_S2.candidates.md) | [txt](blueprint_S3.txt) · [svg](blueprint_S3.svg) · [cand](blueprint_S3.candidates.md) | [txt](blueprint_S4.txt) · [svg](blueprint_S4.svg) · [cand](blueprint_S4.candidates.md) | [txt](blueprint_S5.txt) · [svg](blueprint_S5.svg) · [cand](blueprint_S5.candidates.md) | [txt](blueprint_S6.txt) · [svg](blueprint_S6.svg) · [cand](blueprint_S6.candidates.md) |

### Cómo reproducir esta ronda

```
python -X utf8 prototypes/components/render.py    # 66 .txt + 66 .svg + 66 .candidates.md
python -X utf8 prototypes/components/matrix.py    # la matriz 11x6
python -X utf8 prototypes/verify_ink.py           # 3a (widget en vivo, 11x3)
python -X utf8 -m pytest -q
```

La tabla de §3b y los conteos de `<rect>` / `font-weight` / `text-decoration` de §4 se derivan de los
archivos con la fórmula de `verify_ink.ink_fraction` y con `re.findall` sobre los `.svg`; están escritos
en el cuerpo de cada sección para que cualquiera los rehaga sin este documento.

---

## 7. Preguntas para el veredicto (cerradas)

1. **`Kit` antes que los lenguajes.** Nord demuestra que `INVALID`-por-orientación y el `match`
   invisible son del **kit base**, no de los seis que los heredan (§2.4). ¿Se abre un incremento contra
   `Kit` **antes** de tocar un solo lenguaje, o cada lenguaje responde por su cuenta y se acepta que la
   respuesta base siga rota debajo?
2. **Blueprint, pregunta 10 reabierta**: el knockout ya se movió del title block al `DELETE` del confirm.
   ¿Se ratifica, o vuelve al title block y el confirm marca su destructivo de otra forma? (§0b, §2.6)
3. **Blueprint, ley de primera fijación**: el knockout no se renderiza en `S1/S2/S3/S5/S6`. ¿Es un bug de
   render o el título block deja de ser el ancla y la ley se reescribe?
4. **`solari_S4`**: ¿el modal debe conservar la tira de modos y el masthead como en los otros cinco, o
   «una salida se apodera del tablero» es doctrina de este lenguaje y hay que escribirla?
5. **Sobrecarga de celda**: ¿se acepta como principio que la celda de severidad de un lenguaje **no**
   puede ser también su cursor de selección, su perilla y su pared de botón? Si sí, afecta a cuatro de
   los seis y es un registro nuevo, no un parche.
6. **Marca de obligación**: `⠁` (instrument) colisiona con `DISABLED`, `▐` (industrial) con la pared del
   campo, `▁` (solari) con nueve cosas, `├` (blueprint) con el terminador de cota, `•` (swiss) con el
   foco del botón. De las seis marcas de `inc35`, **cinco colisionan en frame**. ¿Se rehacen las cinco,
   o `required` deja de ser una celda y pasa a ser una posición?
7. **`INVALID` por orientación**: instrument, industrial y blueprint cifran «inválido» girando el par de
   paredes. ¿Se prohíbe la orientación como único canal de estado?
8. **Caption contra control**: `industrial_S3` y `darkside_S3` emplatan el caption igual que el botón.
   ¿El caption pierde su marca, o el botón gana una segunda?
9. **`Kit.match`**: ¿el mecanismo pasa a incluir un glifo (y entonces choca con la ley de contenido byte
   a byte), o `svg_from_grid` aprende `bold`/`underline` y la ronda se rehace sobre artefactos que
   pueden mostrarlo? (§4)
10. **El `.txt` como obra**: darkside `S1` y blueprint `S4` sólo son juzgables en el `.svg`. ¿Se mantiene
    «el `.txt` es la obra» y esos dos mecanismos ceden, o la convención admite una excepción escrita?

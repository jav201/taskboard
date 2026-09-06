# PROTOTYPE-inheritors-2 — los 42 frames, rejuzgados después de `rework-1/2/3`

**Segunda ronda adversarial sobre los mismos 42 frames.** La primera
(`PROTOTYPE-inheritors.md`, 2026-09-05) propuso **keep 6 · nota 17 · rehacer 19**. Después corrieron
tres lotes — `rework-1` (inc39–41, nivel `Kit`), `rework-2` (inc42–44, instrumental y censo) y
`rework-3` (inc45–48, nivel lenguaje) — y los kits volvieron a renderizar los 42.

Esta ronda **no tocó ningún kit, ningún test y ningún frame**: sólo los leyó, y los diffeó contra
`8604607` (el commit anterior a `rework-1`). Vocabulario de veredicto cerrado, el mismo:
**`keep` / `keep with a note` / `rework`**. Propuestos, no decididos.

**Resultado: keep 14 · nota 21 · rework 7.** Ninguna etiqueta empeoró. Cuatro objeciones sí
empeoraron sin que la etiqueta se moviera, y están nombradas en §4.

---

## 0. Tres cosas que hay que decir antes de la primera tabla

### 0a. El tier de estilo se ve por primera vez, y cambia siete veredictos

`inc43` enseñó a `svg_from_grid` a emitir `font-weight`, `text-decoration` y el `reverse` como
fondo. El hallazgo §4 de la primera ronda — *«`Kit.match` no es observable en ninguno de los 42»* —
**está cerrado**. Contado sobre los siete `S6`:

| lenguaje | `MATCH_STYLE` | qué pinta ahora el `.svg` | tinta del match | tinta del cuerpo | contraste match↔cuerpo |
|---|---|---|---|---|---|
| instrument | `underline {accent}` | 6 × `text-decoration="underline"` | `#2dd4bf` | `#6b7785` | 2,45:1 |
| swiss | `bold {alert}` | 6 × `font-weight="bold"` | `#e2231a` | `#8a8a8a` | **1,36:1** |
| industrial | `reverse {accent}` | 6 `<rect>` `#ff4b1f`, tinta `#121212` | — | — | 5,60:1 (tinta sobre plato) |
| nord | `bold {accent}` (de `Kit`) | 6 × `font-weight="bold"` | `#88c0d0` | `#7b88a1` | 1,79:1 |
| darkside | `reverse {mut}` | 6 `<rect>` `#737373`, tinta `#121212` | — | — | 3,95:1 |
| solari | `reverse {ink}` | 6 `<rect>` `#f0ede4`, tinta `#121212` | — | — | 16,00:1 |
| blueprint | `bold {ink}` | 6 × `font-weight="bold"` | `#eef4f8` | `#7fa8c4` | 2,28:1 |

Dos lecturas que la primera ronda no podía tener:

* **`reverse` gana.** Los tres kits que lo declaran producen el único canal que sobrevive entero a la
  escala de grises (3,95 · 5,60 · 16,00 tinta-sobre-plato). Los cuatro `bold`/`underline` producen
  un salto de luminancia de 1,36 a 2,45 y dependen del peso para el resto.
* **La predicción de la primera ronda sobre `blueprint_S6` era falsa.** Decía que con la croma casi a
  cero `bold {ink}` es «peso y nada más». No: en blueprint `ink` es `#eef4f8` y el cuerpo es `mut`
  `#7fa8c4`, así que el match es un salto de **valor** grande (16,89:1 contra la hoja). Se corrige
  aquí, contra el artefacto.

### 0b. El hallazgo nuevo de esta ronda: las tres leyes comparan code points, y el lector lee formas

Las tres leyes de `rework-3` (`test_a_languages_meaning_marks_do_not_share_a_cell`,
`test_a_meaning_never_stands_at_a_disabled_or_indicator_seat`,
`test_no_control_opens_with_a_mark_that_means_something`) construyen su conjunto de significados con
`set("".join(k.LEVELS.values())) | {k.REQUIRED} | set("".join(k.DANGER_FORM))` y comparan por
igualdad de carácter. **Casi todos los movimientos del lote cayeron dentro de la misma familia
visual del cell que abandonaban:**

| lenguaje | movió | a | y el vecino que queda |
|---|---|---|---|
| swiss | `radio.knob` `•` | `●` | `•` sigue siendo `REQUIRED` (`title•` y `╵●  high` en la misma pantalla) |
| swiss | ladder de botón `· • ●` | `▫ ▪ ■` | `▮` es `CUR`: cuatro rectángulos macizos a cuatro tamaños |
| darkside | leader de `field_row` `▬` | `◦` | `o ` es `LEVELS["warn"]`; `◦` y `o` a 12 px son el mismo anillo |
| darkside | `CUR` `O` | `▊` | `▮` es la pared/foco: dos bloques verticales macizos de anchos distintos |
| industrial | `CUR` `▪` | `▶` | `DISCLOSE` es `▼`: el mismo triángulo girado |
| nord | — | — | `CUR` `▸` contra `stepper.step` `▶`/`►` |
| solari | `REQUIRED` `▁` | `▮` | `▮` es el propio caret del campo, en la misma fila, a 14 celdas (admitido en §11.5) |
| blueprint | — | — | `━` (error+danger) contra `─`/`┄` de los indicadores |

Las leyes pasan. El criterio observable — *enseñar la marca fuera de contexto y preguntar qué
significa* — no. **La regla del lote dice «distintas en un canal que ese lenguaje declara (cuenta,
peso, tier, posición)»; el diámetro y la rotación no están en esa lista y son lo que se usó.** Es la
decisión (D) de §6.

### 0c. Una ley no llega al asiento que el frame enseña

`meaning_marks_at_named_seats` mira `comp == "switch" and part == "indicator"`. En estos kits el
`indicator` es **la pista** y el `knob` es **la perilla** — la celda que el lector lee como «el
switch». `MEANING_AT_A_NAMED_SEAT["darkside"] = 0`, y sin embargo:

```
darkside switch.knob  default / checked   'O'      == LEVELS["error"]
darkside_S3 filas 4-8:   ▬▬O   ▬▬O   O──   x╌╌   ▬▬O
```

El censo **sí** lo ve — `O [3 families] LEVELS[error] · checkbox.knob mid · switch.knob mark` — y la
ley no. Lo mismo en `naught` (`◉` = `REQUIRED` en el knob) y en `corgi` (`██`/`▀▀` = `LEVELS[error]`
y `REQUIRED` en el knob). Tres lenguajes, un asiento que la cláusula nombró mal.

---

## 1. La matriz 7×6, antes → después

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| **instrument** | nota → **nota** | rework → **rework** | rework → **nota** | rework → **nota** | keep → **keep** | nota → **keep** |
| **swiss** | nota → **nota** | rework → **rework** | rework → **keep** | rework → **rework** | nota → **nota** | nota → **nota** |
| **industrial** | nota → **nota** | rework → **nota** | rework → **keep** | keep → **keep** | nota → **nota** | nota → **keep** |
| **nord** | rework → **nota** | rework → **nota** | nota → **keep** | keep → **keep** | nota → **keep** | nota → **nota** |
| **darkside** | rework → **rework** | nota → **nota** | rework → **nota** | keep → **keep** | keep → **keep** | rework → **keep** |
| **solari** | nota → **nota** | rework → **nota** | keep → **keep** | rework → **nota** | nota → **nota** | nota → **nota** |
| **blueprint** | rework → **nota** | rework → **rework** | rework → **rework** | rework → **rework** | nota → **nota** | nota → **keep** |

|  | keep | keep with a note | rework |
|---|---|---|---|
| **antes** (2026-09-05) | 6 | 17 | 19 |
| **después** (`4b453cc`) | **14** | **21** | **7** |

Los siete `rework` que quedan son **cuatro cosas**:

1. **Dos campos inválidos que perdieron el canal en vez de ganarlo** (`instrument_S2`) o que nunca lo
   tuvieron (`swiss_S2`, donde el control muerto sigue siendo aire).
2. **Dos composiciones que ningún lote tocó** (`swiss_S4`, el modal que abre y no cierra;
   `darkside_S1`, el `.txt` sin separación de paneles con la doctrina citada y el fallo sin dar).
3. **Blueprint entero, que no tuvo incremento** (`S2`, `S3`, `S4`).
4. Nada más. Los otros doce `rework` de la primera ronda se cerraron o bajaron a nota.

**Densidad: el lote no la movió.** Con la fórmula de `verify_ink.ink_fraction` sobre los 42, el
cambio máximo es **−0,8 puntos** (`industrial_S1` 24,0 → 23,6; `solari_S4` 23,6 → 22,8); 34 de los 42
no se mueven ni una décima. El `36,0 → 34,3` de `instrument_S1` que §10.6 marcó **no es un cambio de
frame**: es `inc44` descartando `U+2800` de la fórmula. El frame es idéntico byte a byte.

---

## 2. Los 42 bloques

Formato de cada uno: **veredicto previo · objeción que llevaba · qué cambió en el frame (celdas
viejas y nuevas, citadas de los dos `.txt`) · estado de la objeción · veredicto nuevo**.

Contexto de uso, sin cambios respecto de la primera ronda: **operador único** (`jav201`), terminal de
100×32 monoespaciado, sesión diurna, tema por defecto; la tarea es la que la pantalla nombra.

---

### 2.1 instrument

Alfabeto en HEAD: `LEVELS = {info: ⠂⠂, warn: ⠆⠆, error: ⠇⠇}`, `REQUIRED = ⠁`,
`DANGER_FORM = (⠛, ⠛)`, `CUR = ⣿`, `PANE_RULE = ⠸`, `LATT = ⠒`.

#### `instrument_S1` — nota → **`keep with a note`**
* **Objeción previa:** el gutter `⠸` (una vez por fila) compite con los leaders `⠒` del panel derecho
  (hasta cuarenta por fila); el gutter deja de ser «lo único vertical».
* **Qué cambió:** **nada.** El `.txt` es byte a byte el de `8604607`.
* **Estado:** **sigue en pie**, intacta. Ningún incremento del lote tocó `LATT` ni `PANE_RULE`.
* **Veredicto: `keep with a note`.**

#### `instrument_S2` — rework → **`rework`**
* **Objeción previa:** *«la diferencia entre este campo está mal y este campo está bien es el orden
  de dos paredes»*, y `⠇` (peldaño de error) abre el botón seguro.
* **Qué cambió — y ésta es la parte que hay que leer con los dos ficheros al lado:**

  ```
  8604607  fila 04  title⠁   ⠧Fix login⡇ redirect⠤⠤…⠼      (default)
  8604607  fila 06  due⠁     ⠸12/09/26⠶⠶…⠇                  (INVALID)
  8604607  fila 13  notes    ⠇Redirect drops the ?next= …⠸  (textarea)
  8604607  fila 17           ⠄ Save ⠄   ⠇   Cancel   ⠸

  HEAD     fila 04  title⠁   ⠼Fix login⡇ redirect⠤⠤…⠧      (default)
  HEAD     fila 06  due⠁     ⠸12/09/26⠶⠶…⠇                  (INVALID) ← SIN CAMBIO
  HEAD     fila 13  notes    ⠸Redirect drops the ?next= …⠇  (textarea)
  HEAD     fila 17           ⠄ Save ⠄   ⠸   Cancel   ⠇
  ```

  **La fila 6 es idéntica byte a byte a la de `8604607`.** `inc39` la desgiró (`⠇⠶⠸`) y luego `inc46`
  espejó todos los rieles del lenguaje (`⠇` deja de abrir y pasa a cerrar), lo que la devolvió
  exactamente a donde estaba. Y las paredes que se movieron **se movieron encima de las suyas**.
* **Estado: la objeción no está respondida — está sustituida por otra más dura.** Antes, inválido
  (`⠸…⠇`) y textarea (`⠇…⠸`) eran dos pares distintos, mal distinguibles pero distintos. Ahora el
  campo inválido, el textarea y el botón por defecto llevan **la misma pareja de paredes**. El censo
  lo firma en dos filas: `⠇ [4 families] LEVELS[error] · INVALID textfield.main close · button.main
  close (default) · textfield.main close (default)` y `⠸ [3 families]` en los tres abridores.
  **Criterio observable:** tapar la fila 7 (`⠇⠇ expected YYYY-MM-DD`) y señalar el campo inválido
  leyendo sólo las paredes. Antes había una respuesta débil; ahora no hay ninguna.
  *En descargo del lote:* el canal que sí funciona ya estaba y sigue estando — el relleno `⠶` del
  campo inválido contra el `⠤` del normal, 26 celdas en vez de dos. Pero eso era verdad en
  `8604607` y no lo movió este lote.
* **Veredicto: `rework`.** Con la nota de que el arreglo correcto es de una línea y de `Kit`: darle
  al `INVALID` una **forma** (como hicieron nord con `?` y darkside con `Ø`), no un par de paredes.

#### `instrument_S3` — rework → **`keep with a note`**
* **Objeción previa:** `⠁` significa «obligatorio» en `S2` y «apagado y no lo puedes tocar» aquí.
* **Qué cambió:** `sync to remote  ⠄⠁⠁` → `sync to remote  ⠄⠈⠈`. Los cinco asientos muertos pasaron a
  `⠄` / `⠈`, peldaños que este lenguaje ya gasta en cosas muertas (`⠄ Save ⠄` en `S2`). El botón
  destructivo pasó de `⠇ ⠛Delete all⠛ ⠸` a `⠸ ⠛Delete all⠛ ⠇`.
* **Estado: respondida.** `⠁` significa obligación y nada más; su fila del censo desapareció.
* **Objeción nueva:** `⣿` es `CUR` **y** el relleno de la pista encendida de los cinco switches
  (`⣿⣿⡇`) **y** el relleno del slider (`⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠒⠒⠒⠒`) **y** la marca de opción elegida (`⣿ dark`)
  **y** la pestaña activa. **Criterio:** enseñar `⣿` fuera de contexto — «aquí estás» o «esto está
  encendido». `MEANING_AT_A_NAMED_SEAT` no lo ve porque `CUR` está deliberadamente fuera del conjunto
  de significados (documentado en el propio docstring de la ley), y el asiento es `switch.indicator`,
  que aquí es la pista.
* **Veredicto: `keep with a note`.**

#### `instrument_S4` — rework → **`keep with a note`**
* **Objeción previa:** *«severidad invertida en un confirm destructivo: la única celda de severidad
  de la pantalla está sobre `Cancel`»*, más el segundo criterio de que las tres reglas de graticule
  (filas 3, 13, 20) son la misma cadena.
* **Qué cambió:** una fila. `⠧  ⠛Delete⠛  ⠼   ⠇   Cancel   ⠸` → `⠼  ⠛Delete⠛  ⠧   ⠸   Cancel   ⠇`.
* **Estado: media respondida, y la mitad respondida lo fue por evidencia contra la primera ronda.**
  §11.3 de `spec.md` lo dice y tiene razón: contado en puntos, el destructivo enfocado siempre fue
  más pesado — `⠼`(4) + `⠧`(4) = 8 contra `⠸`(3) + `⠇`(3) = 6, más la hachura `⠛…⠛`(4+4) alrededor de
  la palabra. **Eso ya era verdad en `8604607`**, así que «severidad invertida» era una lectura
  equivocada de la primera ronda y queda retirada. **Criterio observable:** sin leer las palabras,
  señalar el peligroso — respondible, y lo era antes.
  **Lo que queda en pie:** `⠇` sigue estando sobre `Cancel`; sólo cambió de extremo. La ley que se
  cumplió es «un significado no abre un control», no «la severidad no está en el botón seguro».
  Y el segundo criterio — distinguir «hay un modal» de «aquí acaba la cabecera» — **no se tocó**: las
  filas 3, 13 y 20 siguen siendo la misma cadena de 100 `⠒`.
* **Veredicto: `keep with a note`.**

#### `instrument_S5` — keep → **`keep`**
* Frame idéntico. La escalera `⠂⠂ / ⠆⠆ / ⠇⠇` sigue siendo monótona por cuenta. Sin cambios.

#### `instrument_S6` — nota → **`keep`**
* **Objeción previa:** *«circular los caracteres que casaron. No respondible en ningún tier.»*
  Inspeccionado, no ejercitado.
* **Qué cambió:** el `.txt` sólo espejó las paredes del campo de consulta (`> ⠧re⡇…⠼` → `> ⠼re⡇…⠧`).
  **El `.svg` es lo que cambió:** 6 × `<text ... fill="#2dd4bf" text-decoration="underline">re</text>`,
  contra un cuerpo de fila en `#6b7785`.
* **Estado: respondida, y ejercitada por primera vez.** El criterio ahora tiene respuesta en el tier
  del `.svg`: dos canales independientes (subrayado + salto de tono 2,45:1).
* **Nota menor:** el acento `#2dd4bf` es también el `⣿` del cursor de la misma fila, y la doctrina de
  instrument reserva *«one saturated hue for state»*. El match no es un estado.
* **Veredicto: `keep`.**

---

### 2.2 swiss

`LEVELS = {info: ·, warn: ─, error: ━}`, `REQUIRED = •`, `DANGER_FORM = (╲, ╱)`, `CUR = ▮`,
`DISCLOSE = ─`.

#### `swiss_S1` — nota → **`keep with a note`**
* **Objeción previa:** el cursor de selección es la celda de error (`━ D O I N G`), y hay tres
  hairlines en una pantalla cuyo compromiso dice «una».
* **Qué cambió:** `━ D O I N G` → `▮ D O I N G`; `━   Fix login redirect` → `▮   Fix login redirect`.
* **Estado: la primera mitad, respondida.** `━` ya no es cursor; el criterio «decir si `DOING` está
  seleccionado o en error» tiene una respuesta. **La segunda mitad sigue en pie**: las tres hairlines
  (filas 3 y 6×2) no se tocaron.
* **Objeción nueva (§0b):** `▮` (`CUR`) entra en una pantalla donde `▪` y `■` son los dos peldaños
  altos de la escalera de botón que `inc46` creó. Cuatro rectángulos macizos a cuatro tamaños
  (`▫ ▪ ■ ▮`) es exactamente la queja que la primera ronda le hizo a `industrial_S5` (`▪` contra `■`,
  «dos píxeles y depende de la fuente»), ahora en swiss.
* **Veredicto: `keep with a note`.**

#### `swiss_S2` — rework → **`rework`**
* **Objeción previa:** *«un control deshabilitado que se lee como caption»* — `Save` (DISABLED) es
  tipográficamente idéntico a la leyenda de la fila siguiente; y la corrección de `inc38` dejó un
  componente sin paredes junto a cuatro con paredes.
* **Qué cambió:**

  ```
  8604607  title•   ┃Fix login▏ redirect···············┃
  HEAD     title•   ┃Fix login▏ redirect···············      (sin cierre)

  8604607  due•     ╲12/09/26                          ╱
  HEAD     due•     ╲12/09/26                                (sin cierre)

  8604607  priority ╵ ╵ low  ╵ ╵ norm  ╵•╵ high
  HEAD     priority ╵   low  ╵   norm  ╵●  high

  8604607  tags     │ │ api  │▪│ ui  │▪│ urgent
  HEAD     tags     │   api  │▪  ui  │▪  urgent

  8604607           Save        ·   Cancel
  HEAD              Save        ▫   Cancel
  ```
* **Estado: dos objeciones en pie y una tercera nueva.**
  **(a)** `Save` sigue siendo aire. Lo admite `spec.md` §11.3 palabra por palabra: *«the dead button
  is still air … Still open»*. El criterio «señalar los controles pulsables» sigue sin respuesta para
  el botón que el usuario tiene que pulsar.
  **(b)** El packet dice *«the four controls beside it lost their walls so the screen is
  consistent»*. **El frame no dice eso: perdieron el cierre, no las paredes.** Cinco controles abren
  con una pared y ninguno cierra. Bajo `NO BOXES` de swiss una marca de un solo lado es defendible
  (principio de `inc38`), pero la afirmación del packet no es lo que se ve, y la consistencia que
  reclama es «cinco medias cajas contra un botón sin nada».
  **(c) Objeción nueva:** el campo inválido abre con `╲`, que es `DANGER_FORM[0]`. En `S3` y `S4` esa
  misma celda abre `╲Delete all╱` y `╲Delete╱`, los dos irreversibles del lenguaje. **Criterio:**
  enseñar `╲` fuera de contexto — «este valor no parsea» o «esto borra datos». La ley del abridor
  **exime este caso por nombre** (docstring de `meaning_marks_at_an_opener`: *«a field whose INVALID
  walls are that language's own DANGER_FORM … there the opening cell IS the rejection»*), de modo que
  `MEANING_AT_AN_OPENER["swiss"] = 0` y ningún test lo va a ver nunca. El censo sí:
  `╲ [2 families] DANGER_FORM open · INVALID textfield.main open`.
* **Veredicto: `rework`.**

#### `swiss_S3` — rework → **`keep`**
* **Objeción previa:** *«el `·` delante de un `Delete all` es el peldaño informativo haciendo de
  prefijo de un destructivo»*.
* **Qué cambió:** `·  ╲Delete all╱` → `▫  ╲Delete all╱`. Los switches pasaron de `━━│` a `▀▀│`, el
  slider de `━━━━━━━━━│────` a `▀▀▀▀▀▀▀▀▀│────`, el select perdió el cierre y la opción elegida pasó
  de `━ dark` a `▮ dark`.
* **Estado: respondida.** La escalera del botón es ahora `▫ ▪ ■`, una forma a tres pesos, y ninguno
  de los tres es una declaración. `━` desapareció de la pantalla entera.
* **Nota:** `─` (`LEVELS["warn"]`) sigue siendo la pista apagada del switch (`│──`) y la pista vacía
  del slider (`────`) — censo `─ [2 families] LEVELS[warn] · switch.main mark`. La ley del asiento
  nombrado mira `switch.indicator`, no `switch.main`, así que tampoco lo ve (§0c). La posición
  salva la lectura; se registra.
* **Veredicto: `keep`.**

#### `swiss_S4` — rework → **`rework`**
* **Objeción previa:** dos. `•` (`REQUIRED`) haciendo de anillo de foco sobre el botón irreversible,
  y *«el modal se abre y no se cierra»*.
* **Qué cambió:** `•  ╲Delete╱      ·   Cancel` → `▪  ╲Delete╱      ▫   Cancel`.
* **Estado:** la primera, **respondida** — la obligación se queda con `•` y el foco toma `▪`. La
  segunda, **en pie y admitida**: `spec.md` §11.3 la llama *«a composition finding in
  `overlay_instead` and is still open»*. La fila 13 sigue siendo una regla de 100 celdas de apertura
  y **no hay ninguna de cierre**; debajo del confirm sólo queda el pager de la fila 31.
  **Criterio observable:** decir dónde termina el modal. Sigue sin respuesta, en un confirm
  destructivo.
* **Objeción nueva:** `▪` es el checkbox marcado de `S2` (`│▪  ui`). El anillo de foco del botón
  irreversible es la celda que dos pantallas antes significaba «esta casilla está marcada».
* **Veredicto: `rework`.**

#### `swiss_S5` — nota → **`keep with a note`**
* **Objeción previa:** `─` (warn) es exactamente `DISCLOSE` y exactamente la celda de las tres
  hairlines; el margen más estrecho de los seis lenguajes.
* **Qué cambió:** una fila, el medidor: `EVENTS/S ━━━━━━━───────  5` → `EVENTS/S ▀▀▀▀▀▀▀───────  5`.
* **Estado: sin cambio real.** La objeción sigue entera.
* **Objeción nueva, que la primera ronda le hizo a `blueprint_S5` y no a éste:** la sparkline de la
  fila 7 es `─━─━─━━━──━━━─━━` — **los dos peldaños altos de `LEVELS`**, seis filas encima de
  `09:41:09 ─ 3 tasks overdue` y `09:41:18 ━ rate limit hit`, que usan esas mismas celdas como
  severidad. **Criterio:** decir si un `━` de la fila 7 significa «pico» o «error». Es el mismo
  defecto que blueprint, en la misma pantalla canónica, y ningún lote lo tocó.
* **Veredicto: `keep with a note`.**

#### `swiss_S6` — nota → **`keep with a note`**
* **Objeción previa:** *«"never alone" es exactamente el compromiso que el artefacto no puede
  verificar»*. Inspeccionado, no ejercitado.
* **Qué cambió:** `.txt`, el cierre del campo de consulta y el cursor (`━ redirect to task` →
  `▮ redirect to task`). `.svg`: 6 × `<text fill="#e2231a" font-weight="bold">re</text>`.
* **Estado: el «never alone» queda verificado** — el rojo llega acompañado del `bold`, que es lo que
  la doctrina prometía. El criterio «circular el `re`» tiene respuesta.
* **Objeción nueva, y sólo se puede hacer ahora:** `#e2231a` contra el cuerpo de la fila `#8a8a8a` es
  **1,36:1**. En la convención de la casa — *«con el color quitado»*, el criterio que esta ronda
  aplicó a las seis escaleras de severidad — el match de swiss **desaparece** y queda sólo el peso.
  Contra la hoja `#121212` da 4,00:1, por debajo del 4,5:1 de texto normal. Es el más débil de los
  siete en el tier que acaba de hacerse visible.
* **Veredicto: `keep with a note`.**

---

### 2.3 industrial

`LEVELS = {info: ▫▫, warn: ▪▪, error: ■■}`, `REQUIRED = !`, `DANGER_FORM = (╱╱, ╱╱)`, `CUR = ▶`,
`DISCLOSE = ▼`.

#### `industrial_S1` — nota → **`keep with a note`**
* **Objeción previa:** *«contar los paneles leyendo sólo los platos — salen entre dos y quince según
  qué `▐` se cuente»*; y el cursor `▪` es la mitad del peldaño `warn`.
* **Qué cambió:** el `field_row` del panel de detalle perdió el plato del **valor**, y el cursor pasó
  a `▶`:

  ```
  8604607  ▌ ▐PROJECT                       ▐ Web ▌        ▪ ▐▌ [2]DOING
  HEAD     ▌ ▐PROJECT                           Web        ▶ ▐▌ [2]DOING
  ```
* **Estado: las dos, respondidas en parte.** El plato pasó de cinco sentidos a cuatro (gutter
  `▌ ▐`, cabecera de columna `▐▌`, código de tarjeta `▐ 05 ▌`, pared izquierda del panel derecho); el
  valor ya no compite. Y `▪` deja de ser cursor. El criterio sigue teniendo ambigüedad, más
  estrecha.
* **Objeción nueva:** `CUR = ▶` y `DISCLOSE = ▼` son **el mismo triángulo girado**, y en `S3` viven a
  tres filas: `▐dark   ▼▌` (filas 10-11) contra `▶ dark` (fila 14). `inc39` escribió una ley entera
  sobre que la orientación no es un canal que un lector pueda usar, y la escribió sólo para los
  campos. Aquí vuelve, en el cursor.
* **Veredicto: `keep with a note`.**

#### `industrial_S2` — rework → **`keep with a note`**
* **Objeción previa:** `▐` es a la vez `REQUIRED` y la pared del campo, en la misma fila a ocho
  espacios; y `INVALID` es el mismo par de platos girado.
* **Qué cambió:**

  ```
  8604607  title▐   ▐Fix login| redirect---------------▌
  8604607  due▐     ▌12/09/26//////////////////////////▐
  HEAD     title!   ▐Fix login| redirect---------------▌
  HEAD     due!     ▐12/09/26//////////////////////////▌
  ```
* **Estado: las dos, respondidas.** La obligación toma `!`, el estarcido del registro; el plato se
  queda con la celda porque es la notación entera del lenguaje. El giro desapareció.
* **Objeción nueva, más pequeña que la que sustituye:** las paredes del campo inválido ahora son
  **byte a byte** las del campo normal y las del botón — censo `▐ [3 families]` y `▌ [3 families]`.
  El canal que queda es el relleno: `//////` (30 celdas) contra `------`, más el `■■` de la fila 7.
  Eso es un canal real y ancho, y por eso baja a nota y no se queda en rework. Segunda nota: `!` es
  también el marcador de vencido en `S1` (`▐ 02 ▌ Rate-limit the API   [2d!]`).
* **Veredicto: `keep with a note`.**

#### `industrial_S3` — rework → **`keep`**
* **Objeción previa:** *«un caption que se lee como control, adyacente a un destructivo»* —
  `▐ delete every completed task ▌` emplatado igual que `▐   Cancel   ▌`.
* **Qué cambió:**

  ```
  8604607  DANGER ZONE                    ▐ delete every completed task ▌
  HEAD     DANGER ZONE                        delete every completed task
  ```
* **Estado: respondida, y con la respuesta correcta al nivel correcto.** §11.3 lo documenta: la hoja
  no llamaba a `button` para un caption; era `field_row` emplatando el valor, y el plato de
  industrial era byte a byte su botón por defecto. El caption va desnudo, como `nord_S3`, que la
  primera ronda puso como referencia. El botón conserva `▐ ╱╱Delete all╱╱ ▌`.
* **Veredicto: `keep`.**

#### `industrial_S4` — keep → **`keep`**
* La caja de plato, el chrome intacto y la hachura `╱╱` sobre `Delete` siguen exactamente igual. Lo
  único que se movió es el tablero de detrás (los platos de valor y el cursor, §`industrial_S1`), lo
  que hace el fondo algo menos ruidoso. Sigue siendo la mejor superposición de las siete.

#### `industrial_S5` — nota → **`keep with a note`**
* **Objeción previa:** distinguir `▪` de `■` a 12 px sin verlos adyacentes; y `▪` es además el cursor
  en `S1`/`S3`/`S6`.
* **Qué cambió:** el frame, nada. Pero **`▪` dejó de ser el cursor** (`inc45`), así que la segunda
  mitad de la objeción está cerrada por un cambio hecho en otras pantallas.
* **Estado:** la primera mitad **sigue en pie y sigue sin poder juzgarse**: el `.svg` no lleva
  métrica de fuente y el `.txt` los muestra como dos code points distintos, que es justo lo que un
  lector no tiene. *Inspeccionado, no ejercitado*, por segunda ronda seguida.
* **Veredicto: `keep with a note`.**

#### `industrial_S6` — nota → **`keep`**
* **Objeción previa:** *«el `reverse` sí es un canal que este exportador sabe pintar — lo pinta 17
  veces en `S1` — y aun así no aparece»*. Diagnosticable.
* **Qué cambió:** el `.svg` pasó de 1 `<rect>` a **7**: el fondo y seis platos `#ff4b1f` con la tinta
  puesta en el fondo de la celda (`#121212`). `inc43` asertó además que el séptimo `re` — el del
  campo de búsqueda — queda excluido, que es lo que separa esta medición de contar texto.
* **Estado: respondida.** *«A plate struck over the run»*, literal, 5,60:1 de tinta sobre plato.
* **Veredicto: `keep`.**

---

### 2.4 nord

`LEVELS = {info: "· ", warn: "! ", error: "!!"}`, `REQUIRED = *`, `DANGER_FORM = (#, #)`, `CUR = ▸`.

#### `nord_S1` — rework → **`keep with a note`**
* **Objeción previa:** *«el load plot volvió a pasar por delante del sujeto»*, 27 celdas de bloque
  sólido aisladas en el panel que existe para tener **un** sujeto; y, menor, `BACKLOG 5▂` pega un
  muñón de sparkline al conteo.
* **Qué cambió:**

  ```
  8604607  ▸   Fix login redirect      3d  │ ▇▇▇▇▇▇▇▇▇▇▇▇░░░░░░░░░░░░░░░  44%
  HEAD     ▸   Fix login redirect      3d  │  44% ━━━━━━━━━━━━───────────────
  ```

  La cifra encabeza y la barra pasa a trazo fino. Celdas de bloque en el frame entero: **77 → 50**
  (el «27 → 0» del packet está acotado al medidor y es correcto para el medidor).
* **Estado: la objeción principal, respondida** — y respondida contra la métrica del propio
  docstring, que es lo que pedía. **La segunda sigue intacta:** `BACKLOG 5▂` (fila 4) y `DOING 4▂`
  (fila 11) están sin tocar.
* **Objeción nueva:** la pista vacía del medidor, `───────────────`, es la misma celda con la que se
  dibujan las tres reglas de sección (filas 5, 12, 23, 57 celdas cada una). En la fila 13, leída
  sola, el tramo vacío se lee como una regla que chocó con la cifra.
* **Veredicto: `keep with a note`.**

#### `nord_S2` — rework → **`keep with a note`**
* **Objeción previa:** dos. **(a)** `] … [` hacia afuera *«no se lee como un estado, se lee como un
  render roto»*; **(b)** el defecto es del kit base, heredado cuatro veces.
* **Qué cambió:** `due*   ]12/09/26                          [` → `due*   ?12/09/26                          ?`.
* **Estado: (a) respondida.** `? … ?` es **simétrico y es una forma**: dice «esto está en duda» sin
  pedirle al lector que compare la orientación de dos celdas en extremos opuestos de una fila de 34.
  **(b) respondida en la atribución y corregida en la aritmética por el propio lote**: `spec.md` §9.3
  q1 mide que diez de los once declaran un `PART_GLYPHS` completo de 14 claves, así que parchear
  `Kit` movía `nord_S2` y nada más; se arregló en los cuatro asientos de declaración. La inferencia
  que §5.8 de la primera ronda marcó como no renderizada, **está renderizada**.
* **Objeción que sigue en pie:** la pantalla mantiene **tres vocabularios de pared** — `▐ … ▌` para el
  campo en edición, `[ … ]` para textarea, checkbox y botón, y ahora `? … ?` para el inválido. El
  lenguaje que se define por ser convencional sigue teniendo el chrome de campo más heterogéneo de
  los siete. Censo: `[ [4 families]` y `] [4 families]`.
* **Veredicto: `keep with a note`.**

#### `nord_S3` — nota → **`keep`**
* **Objeción previa:** `!` bracketeando `Delete all` es `LEVELS["warn"]`, no una marca de destrucción.
* **Qué cambió:** `[ !Delete all! ]` → `[ #Delete all# ]`.
* **Estado: respondida en la declaración.** `DANGER_FORM` es `#` y `!` significa `warn` y nada más.
  Y el acierto que la primera ronda le reconoció — caption desnudo, control entre corchetes — sigue
  intacto.
* **Nota:** `#` no lleva semántica de peligro propia; en convención de terminal es «comentario» o
  «número». Es defendible como hachura (`###`) y es mejor que un peldaño de severidad, pero se
  registra: **criterio:** decir si `#Delete all#` es peligroso, sin leer el contexto.
* **Veredicto: `keep`.**

#### `nord_S4` — keep → **`keep`**
* `▐  !Delete!  ▌` → `▐  #Delete#  ▌`. La separación por vocabulario de pared (`▐ ▌` contra `[ ]`)
  sigue entera y ahora la marca interior también es propia. Sigue siendo el mejor modal de los siete.

#### `nord_S5` — nota → **`keep`**
* **Objeción previa, y era la que el coordinador mandó buscar:** *«`DANGER_FORM` es `!` y
  `LEVELS["warn"]` es `!`. La misma celda marca una fila de advertencia en el log y un botón de
  borrado irreversible en `S3` y `S4` … el entorno no arregla el defecto: lo blanquea.»*
* **Qué cambió:** el frame, **nada**. La declaración, todo: `DANGER_FORM` pasó de `!` a `#` en
  `inc45`.
* **Estado: cerrada en el asiento.** El criterio *«enseñar `!` fuera de contexto y preguntar qué
  significa»* tiene ahora una sola respuesta. Es el caso más limpio del lote: el hallazgo estructural
  de la primera ronda se cerró sin tocar el frame que lo enseñaba.
* **Veredicto: `keep`.**

#### `nord_S6` — nota → **`keep with a note`**
* **Objeción previa:** circular el `re`, no respondible en ningún tier; más la inconsistencia de
  paredes del campo de consulta.
* **Qué cambió:** `.txt` idéntico. `.svg`: 6 × `<text fill="#88c0d0" font-weight="bold">re</text>`.
* **Estado: la principal, respondida**, pero con **el margen de tono más estrecho de los cuatro kits
  de `bold`**: `#88c0d0` contra el cuerpo `#7b88a1` es **1,79:1**. Casi todo el trabajo lo hace el
  peso. Como `MATCH_STYLE` aquí es el de `Kit` sin tocar, esa cifra es la línea base contra la que
  eligieron los otros seis.
  **La menor sigue en pie:** el campo de consulta usa `▐re▏…▌` mientras el textarea de `S2` usa
  `[ … ]`.
* **Veredicto: `keep with a note`.**

---

### 2.5 darkside

`LEVELS = {info: "· ", warn: "o ", error: "O "}`, `REQUIRED = ▪`, `DANGER_FORM = (Ø, Ø)`, `CUR = ▊`,
`RAIL = ▏`.

#### `darkside_S1` — rework → **`rework`**
* **Objeción previa:** el `.txt` **no tiene ninguna separación de paneles** (el escalón gris vive
  sólo en el `.svg`, 28 `<rect>`), mientras el rail `▏` se imprime catorce veces donde no hacía
  falta. *«O el rail cede, o el `.txt` deja de ser la obra para este lenguaje, y eso es un veredicto
  del operador.»*
* **Qué cambió:** el leader del `field_row` del panel de detalle, `▬ Web` → `◦ Web` (seis filas), y el
  cursor `O` → `▊`.
* **Estado: no está respondida — está esperando el veredicto que la propia objeción pedía.**
  `spec.md` §11.3 cita la doctrina (`pane_split_instead`, *«a background is not a cell»*) y dice
  explícitamente *«the ruling is the operator's, which is the round's own last sentence»*, y añade
  que lo que `inc48` hizo fue asegurarse de que no empeorara: `▏` 16 → 16, `▬` 6 → 0.
  **El criterio observable sigue sin respuesta en el tier que la casa llama la obra:** con el `.txt`
  delante, señalar la separación entre el tablero y el panel de detalle.
* **Objeción nueva (§0b):** el leader nuevo es `◦` (U+25E6). `LEVELS["warn"]` es `o `. A la altura de
  celda de estos frames `◦` y `o` son el mismo anillo, y `◦` aparece seis veces en el panel de
  detalle de `S1`/`S4` y una en el caption de `S3`. El censo no lo puede ver — `◦` no lleva familia
  A, cosa que §10.4 predijo por escrito — y las tres leyes tampoco, porque comparan code points.
* **Veredicto: `rework`.** Es un `rework` **de decisión**, no de implementación: sigue abierto porque
  nadie lo ha fallado.

#### `darkside_S2` — nota → **`keep with a note`**
* Frame idéntico. `▬` perdió el rol de prefijo de caption (`inc48`), así que baja de seis
  significados a cinco. `Ø` para inválido sigue siendo una forma y no una orientación — sigue siendo
  el mejor `S2` de los siete en ese eje. La sobrecarga de `▬` sigue sin consecuencia de acto en esta
  pantalla.
* **Veredicto: `keep with a note`.**

#### `darkside_S3` — rework → **`keep with a note`**
* **Objeción previa:** *«el caption y el botón destructivo abren con la misma celda, en filas
  consecutivas»* — `▬ delete every completed task` sobre `▬ ØDelete allØ ▬`.
* **Qué cambió:**

  ```
  8604607  danger zone                    ▬ delete every completed task
  HEAD     danger zone                    ◦ delete every completed task
  ```

  (el botón se queda en `▬ ØDelete allØ ▬`). §11.3 razona la elección: `◦` es la celda más ligera del
  alfabeto, y no `▏` porque `▏` habría llevado `darkside_S1` de 16 trazos a 22.
* **Estado: respondida.** El criterio «señalar los pulsables de las dos últimas filas» tiene ahora
  dos abridores distintos.
* **Objeción nueva, y es de las duras (§0c):** los cinco switches de esta pantalla llevan la perilla
  en `O`, que es `LEVELS["error"]`:

  ```
  notify on overdue  ▬▬O      sound  O──      sync to remote  x╌╌
  ```

  El censo lo firma (`O [3 families] LEVELS[error] · checkbox.knob mid · switch.knob mark`) y
  `MEANING_AT_A_NAMED_SEAT["darkside"] = 0`, porque la ley mira `switch.indicator` — que aquí es la
  pista, `▬` — y nunca `switch.knob`. **Criterio observable:** en la fila 6, decir si `O──` significa
  «apagado» o «error en este ajuste». Y `◦` (el caption nuevo) contra `o ` (warn) es el par
  homoglifo de arriba.
* **Veredicto: `keep with a note`.** La objeción de la primera ronda está cerrada; la que la
  sustituye es de otro tipo y de menor riesgo de acto (no hay destructivo detrás de un switch).

#### `darkside_S4` — keep → **`keep`**
* La caja redondeada, el gasto único de la reserva de bordes y `Ø…Ø` sobre `Delete` siguen igual.
  El tablero de detrás cambió el cursor `O` → `▊` y los leaders `▬` → `◦`.
* **Nota nueva:** `▊` (`CUR`, filas 10-11, detrás del modal) y `▮` (el foco del destructivo, fila 19)
  son dos bloques verticales macizos que se diferencian por el ancho. En un lenguaje cuya jerarquía
  declarada es *«weight and dimming»*, eso es un canal declarado — pero es el mismo canal para dos
  cosas distintas, a nueve filas.
* **Veredicto: `keep`.**

#### `darkside_S5` — keep → **`keep`**
* Frame idéntico. `· / o / O` sigue siendo monótona por área. `O` perdió el rol de cursor
  (`inc45`); conserva el de perilla de switch y de checkbox (§`darkside_S3`), que es una objeción de
  `S3` y no de esta pantalla.

#### `darkside_S6` — rework → **`keep`**
* **Objeción previa, y era estructural, no de exportador:** *«en un lenguaje que ha renunciado al
  matiz, `bold {ink}` es peso y nada más. Un terminal que renderiza `bold` como "más brillante" le
  deja a este lenguaje cero canales para el match … tampoco sería respondible en el terminal real
  bajo una configuración común.»*
* **Qué cambió:** `MATCH_STYLE` pasó de `bold {ink}` a **`reverse {mut}`** (`inc48`). El `.svg` pinta
  seis platos `#737373` con la tinta en `#121212`, y `GROUNDED_FRAMES` subió 14 → 15.
* **Estado: respondida en el mecanismo, no en el exportador** — que es lo correcto, porque la
  objeción era del mecanismo. Un `reverse` es un atributo SGR que cualquier terminal pinta como
  inversión de celda; no depende de cómo el emulador interprete `bold`. Y `±1 grey step` es
  literalmente el canal que la doctrina de este lenguaje declara. El plato `#737373` es además
  **exactamente la tinta del cuerpo de la fila**: el match es un agujero abierto en el color del
  texto, que es la respuesta más limpia de los siete a *«el acento marca interactividad y nada
  más»*.
* **Veredicto: `keep`.** Es el cambio de veredicto más grande de la ronda, y el único `rework` de la
  primera lista que se cierra cambiando la declaración en vez del dibujo.

---

### 2.6 solari

`LEVELS = {info: "OK ", warn: DLY, error: CNX}`, `REQUIRED = ▮`, `DANGER_FORM = (▀, ▄)`, `CUR = ▼`,
`SEAM = ▁`.

#### `solari_S1` — nota → **`keep with a note`**
* Frame idéntico. La nota de densidad sigue exacta: cada tarea gasta dos filas (la fila y su
  costura), así que en 32 filas caben seis de dieciséis y `GATE DONE 07` aparece con cabecera y nada
  debajo. La costura es doctrina; el coste es la mitad de la superficie.

#### `solari_S2` — rework → **`keep with a note`**
* **Objeción previa, la más nítida de la primera ronda:** *«"señala los campos obligatorios". `▁`
  aparece más de sesenta veces en esta pantalla y dos de ellas son la respuesta.»*
* **Qué cambió:**

  ```
  8604607  title▁    ▔Fix login▮ redirect▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▔
  8604607  due▁      ═12/09/26··························═
  HEAD     title▮    ▔Fix login▮ redirect▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▔
  HEAD     due▮      ═12/09/26··························═
  ```

  §11.3 lo re-mide: `▁` 139 → 137, de las cuales las que significaban `REQUIRED` pasaron de 2 a 0.
  (La primera ronda contó «más de sesenta» y se quedó corta; las dos lecturas llegan al mismo
  veredicto.)
* **Estado: respondida, con una reserva que el propio lote declara.** `▮` aparece **tres** veces en la
  pantalla — `title▮`, el caret de `title`, `due▮` — y dos son la respuesta. Contra sesenta-y-tantas
  con dos respuestas, es otro orden de magnitud. La reserva: `▮` es el caret, censo
  `▮ [2 families] REQUIRED · textfield.caret mark`, y §11.5 lo admite (*«naught and solari have no
  unspent cell left … the argument is available exactly twice and it has been spent twice»*).
  **Criterio observable:** «señala los campos obligatorios» — respondible por forma en dos de tres
  ocurrencias, y la tercera se descarta por posición (el caret está dentro del campo, la obligación
  pegada al final del caption).
* **Veredicto: `keep with a note`.**

#### `solari_S3` — keep → **`keep`**
* Frame idéntico. Sigue siendo el único switch de los siete legible con todos los glifos borrados
  (aleta + relleno + palabra).

#### `solari_S4` — rework → **`keep with a note`**
* **Objeción previa, y era *«el defecto más grave de los 42»*:** el modal se comió las ocho primeras
  filas; el operador pierde la tira de modos, el masthead y el `GATE BACKLOG`. *«Con el frame
  delante, decir en qué modo está la aplicación y de qué gate se borra. Ninguna de las dos es
  respondible.»*
* **Qué cambió:**

  ```
  8604607  fila 1  (vacía)              HEAD  fila 1   BOARD  form  cfg  log
  8604607  fila 2  Delete 3 tasks?      HEAD  fila 2   BOARD  16 TASKS  ·  4 PROJECTS
  8604607  fila 3  (vacía)              HEAD  fila 3  ▁▁▁▁▁… (100 celdas)
                                        HEAD  fila 5  Delete 3 tasks?
                                        HEAD  fila 10 ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
  ```

  `inc40` movió la banda al primer *full-measure seam* (`Solari.schedule_head`), no a `Kit.overlay` ni
  a `screens.py`.
* **Estado: el primer criterio, respondido.** «En qué modo está la aplicación» tiene respuesta en la
  fila 1, y el masthead y la costura de cabecera están de vuelta. Los siete lenguajes conservan ya la
  fila 1 en `S4`.
* **El segundo criterio sigue sin respuesta, y ahora con una arista nueva.** Comparadas fila a fila,
  `solari_S4` y `solari_S1` sólo difieren en las filas **4-11**, y esas filas de `S1` son:

  ```
  fila 04   GATE BACKLOG 05   STATUS  PROJ  PRI
  fila 05     21  AUDIT THE THEME TOKENS      ON TIME  LOW
  fila 06     ▁▁▁▁▁… (costura)
  fila 07     30  DROP THE LEGACY SHIM        ON TIME  NORM
  fila 08     ▁▁▁▁▁… (costura)
  fila 10   GATE DOING 04     STATUS  PROJ  PRI
  fila 11     03  FIX LOGIN REDIRECT          BOARDING HIGH
  ```

  **La banda se sigue comiendo exactamente el gate que el modal nombra** (*«3 tasks will be removed
  from BACKLOG»*), sus dos tareas visibles, y la cabecera `GATE DOING 04`. Y deja una arista que
  antes no estaba: la fila 12 del frame nuevo es la **costura de `FIX LOGIN REDIRECT`**, una tarea
  que la banda se llevó — el tablero superviviente arranca con una costura huérfana y cinco filas de
  tarea bajo ninguna cabecera de gate. Las dos únicas cabeceras visibles son `GATE BLOCKED 00` y
  `GATE DONE 07`, ambas vacías.
  **El intercambio es exacto y se ve en la imagen:** la banda no encogio, se deslizo tres filas. Antes
  ocupaba las filas 1-8 y se comia el chrome; ahora ocupa las 4-11 y se come **dos filas mas de
  tablero** (`GATE DOING 04` y `FIX LOGIN REDIRECT`) a cambio de devolver la tira de modos, el masthead
  y la costura de cabecera. La ley de `inc40` (*«una banda contigua, y nunca la primera fila»*) se
  cumple; el sujeto del confirm sigue siendo lo que desaparece.
* **Veredicto: `keep with a note`,** y la nota es la más gruesa de la ronda. Es la decisión (F) de
  §6: o «una salida se apodera de la cabecera del tablero» es doctrina escrita de este lenguaje, o
  el confirm tiene que dejar en pantalla el gate que nombra.

#### `solari_S5` — nota → **`keep with a note`**
* Frame idéntico. La sparkline de dieciséis dígitos (`1212123211222122`) sigue cumpliendo DATAVIZ 1 y
  perdiendo la tarea; el log `OK / DLY / CNX` sigue siendo el mejor de los once. `CNX` junto a un
  campo de fecha se sigue leyendo como «el vuelo se canceló».

#### `solari_S6` — nota → **`keep with a note`**
* **Objeción previa:** tres. **(1)** la banda del match no existe; **(2)** la misma cadena aparece en
  dos casings (`QUERY 'RE'` contra `re`); **(3)** `NO DEPARTURES` para «ningún comando casó con
  `zzq`».
* **Qué cambió:** el `.txt`, **nada**. El `.svg` pasó de 3 `<rect>` a **9**: el fondo, la banda de
  pestaña, la banda del masthead y **seis platos de match** `#f0ede4` con tinta `#121212` — 16,00:1,
  el contraste más alto de los siete.
* **Estado: (1) respondida** — *«a band, which is this board's mark»*, literal. Los seis platos caen
  en las filas 6-11, que no llevan costura, así que el `reverse` no se come ningún `▁`.
  **(2) y (3) siguen en pie, sin tocar.** La fila 2 sigue diciendo `QUERY 'RE'` mientras la 4 dice
  `re`, y la fila 16 sigue diciendo `NO DEPARTURES` donde lo que pasó es que la búsqueda no encontró
  nada. **Criterio:** leer la fila 16 y decir qué ocurrió.
* **Veredicto: `keep with a note`.**

---

### 2.7 blueprint

`LEVELS = {info: ··, warn: ╌╌, error: ━━}`, `REQUIRED = ├`, `DANGER_FORM = (━, ━)`, `CUR = ┌`.
**Blueprint no tuvo ningún incremento en `rework-3`.** Su único cambio en todo el lote es una fila de
`S2`, de `inc39`.

#### `blueprint_S1` — rework → **`keep with a note`**
* **Objeción previa:** *«el mecanismo firma del lenguaje no se renderiza en cinco de sus seis
  frames»* — la ley de primera fijación da una respuesta (`CLEAR`) y el frame no la implementa.
* **Qué cambió:** nada.
* **Estado: respondida por doctrina, con cita.** `spec.md` §9.3 q3: `_state_cell` dispara el reverse
  **sólo sobre el mood `alert`**, y el tablero sembrado está en calma, así que el knockout del title
  block está **sin gastar, no ausente** — que es justamente lo que hace legal el traslado de la
  ruling 10 sin romper «exactamente uno por vista». `inc41` lo ejercita en los dos moods.
* **Nota que queda:** ningún frame del corpus renderiza el mood `alert`, así que **el mecanismo firma
  de uno de los once lenguajes está asertado en un test y no está en ninguna imagen que el operador
  pueda mirar**. En esta hoja, en consecuencia, no hay punto de primera fijación.
* **Veredicto: `keep with a note`.**

#### `blueprint_S2` — rework → **`rework`**
* **Objeción previa:** dos. `├` es a la vez `REQUIRED` y el terminador de apertura de toda cota; y
  radio y checkbox se distinguen sólo por hacia dónde apuntan sus terminadores (`┤ ├` contra `├ ┤`).
* **Qué cambió:** una fila.

  ```
  8604607  due├   ┤12/09/26··························├
  HEAD     due├   ━12/09/26··························━
  ```
* **Estado: tercios.**
  **(a) El giro del campo inválido: respondido.** `━ … ━` es simétrico. Objeción nueva, la misma que
  swiss: `━` es `DANGER_FORM` **y** `LEVELS["error"]` (censo `━ [3 families]`), así que ahora el
  campo de fecha que no parsea y `━Delete all━` de `S3` llevan las mismas dos celdas. Es la ruling de
  `inc39` §9.2 aplicada a propósito, eximida por nombre en la ley del abridor, y es la decisión (C).
  **(b) Radio contra checkbox: doctrina, con cita.** §9.3 q7 — `blueprint`'s `radio.main` gira sus
  terminadores a propósito (*«a callout selecting one item from a schedule»*), citado en el kit, y la
  ley de `inc39` se acota a `textfield` y lo exime por nombre. La lectura de la primera ronda queda
  retirada.
  **(c) `├` = `REQUIRED` = terminador de cota: intacta.** Censo `├ [7 families]`, roster del abridor
  `MEANING_AT_AN_OPENER["blueprint"] = 6`. **Criterio observable:** en la fila 3, decir si `title├`
  es una obligación o el comienzo de una cota cuya cifra no llegó — en la hoja de `S1` `├` abre siete
  cotas. Sigue sin respuesta.
* **Veredicto: `rework`.**

#### `blueprint_S3` — rework → **`rework`**
* **Objeción previa:** encendido y apagado difieren en **una celda de hairline** (`├─┤` contra `├┤·`);
  y el botón destructivo usa `━`, que es `LEVELS["error"]`.
* **Qué cambió:** nada.
* **Estado: en pie, entera, y con la causa nombrada.** §11.3: *«still open — a contrast finding
  between two states of one part, which no law in this batch reaches»*. Ninguna de las tres leyes
  compara dos estados del mismo `part`; comparan un `part` contra las declaraciones de significado.
  Y `╌` (`LEVELS["warn"]`) es todo el vocabulario `DISABLED` de este lenguaje, cinco `parts` — censo
  `╌ [6 families]`, roster de asiento nombrado `MEANING_AT_A_NAMED_SEAT["blueprint"] = 8`.
* **Veredicto: `rework`.**

#### `blueprint_S4` — rework → **`rework`**
* **Objeción previa:** el `.txt` y el `.svg` no coinciden en qué controles hay; leyendo sólo el
  `.txt`, del confirm sale **un** botón y es el seguro. Más la reapertura de la pregunta 10.
* **Qué cambió:** **nada.** El `.txt` sigue diciendo `DELETE    ├  CANCEL  ┤` y el `.svg` sigue
  teniendo dos `<rect>`, el segundo el knockout de ` DELETE `.
* **Estado: la mitad de la premisa, refutada en el expediente.** §9.3 q2 lo documenta: `PROTOTYPE.md`
  §4 era la lista de preguntas **puestas** al operador, las diez se respondieron el 2026-09-04 y
  `spec-20260905-kits-learn-3-closed.md` §6.1 las recoge; la 10 se respondió **sí**. §0b de la
  primera ronda (*«la respuesta la dio el render, no el operador»*) es incorrecta y queda retirada.
  **La otra mitad sigue exactamente igual, y ahora tiene el asiento nombrado:** `screens.s4_blueprint`
  construye el control destructivo con `knockout_cell(" DELETE ")` en vez de
  `button(..., FOCUSED, danger=True)`, así que pierde sus paredes, su `DANGER_FORM` y su foco, y gana
  el reverse. Registrado en `inc41` §8, repetido en §9.5 y en §10.6, **no tocado por ningún
  incremento**. **Criterio observable:** leyendo sólo el `.txt`, señalar los botones del confirm.
  Sale uno y es el seguro.
* **Veredicto: `rework`.** El arreglo pedido está nombrado y no inventado: que `knockout_cell` y
  `button` compongan, lo que es un asiento nuevo del kit.

#### `blueprint_S5` — nota → **`keep with a note`**
* **Objeción previa:** `━` en la fila 5 (pico de la traza) significa a la vez «pico» y «error», a seis
  filas de distancia.
* **Qué cambió:** nada en el frame. **La nota engordó por lo que pasó en `S2`:** `━` ahora carga
  cuatro papeles en el corpus — `LEVELS["error"]`, `DANGER_FORM`, las **dos** paredes del campo
  inválido (`inc39`) y el pico de la sparkline.
* **Veredicto: `keep with a note`.** Es una de las cuatro objeciones que empeoraron sin que la
  etiqueta se moviera (§4).

#### `blueprint_S6` — nota → **`keep`**
* **Objeción previa:** *«con la croma casi a cero por compromiso, `bold {ink}` está en la misma
  situación que darkside»*; no respondible en ningún tier.
* **Qué cambió:** el `.txt`, nada. El `.svg`: 6 × `<text fill="#eef4f8" font-weight="bold">re</text>`
  contra un cuerpo de fila en `#7fa8c4`.
* **Estado: respondida, y la predicción de la primera ronda queda refutada por el artefacto.** `ink`
  en blueprint no es «la misma familia cian» que el cuerpo: es `#eef4f8`, casi blanco, contra `mut`
  `#7fa8c4`. El match es un salto de **valor** grande — 16,89:1 contra la hoja, 2,28:1 contra el
  cuerpo — más el peso. Dos canales.
* **Nota menor:** `CUR = ┌` se dibuja también en `#eef4f8`, así que en la primera fila de resultado
  el cursor y el match llevan la misma tinta en los dos extremos.
* **Veredicto: `keep`.**

---

## 3. Qué se movió, en números

| | antes | después |
|---|---|---|
| `keep` | 6 | **14** |
| `keep with a note` | 17 | **21** |
| `rework` | 19 | **7** |
| frames con `.txt` movido | — | 26 de 42 |
| frames byte a byte idénticos | — | 16 de 42 |
| `S6` con su `MATCH_STYLE` pintado | 0 de 7 | **7 de 7** |
| celdas colisionantes (censo, 11 lenguajes) | 54 | 48 |
| filas vivas de significado × significado | 15 | 8 (las ocho llevan `INVALID`) |
| deriva máxima de tinta por frame | — | −0,8 puntos |

**Doce de los diecinueve `rework` se cerraron o bajaron.** De los siete que quedan, tres son de
blueprint, que no tuvo incremento; dos son composiciones que ningún lote tocó (`swiss_S4`,
`darkside_S1`); y dos son campos de formulario (`instrument_S2`, `swiss_S2`).

---

## 4. Dónde empeoró la objeción, aunque la etiqueta no

**Ninguna etiqueta retrocedió** — no hay `keep → nota` ni `nota → rework` en los 42. Decirlo como
«nada empeoró» sería falso, porque cuatro objeciones sí se pusieron peores debajo de una etiqueta que
no se movió:

1. **`instrument_S2`** (`rework` → `rework`). En `8604607` el campo inválido (`⠸…⠇`) y el textarea
   (`⠇…⠸`) eran dos pares distintos; a HEAD son **la misma pareja**, y el botón por defecto también.
   `inc39` desgiró la fila y `inc46` espejó los rieles del lenguaje, así que la fila 6 volvió a ser
   byte a byte la de antes del lote mientras todo lo demás se mudaba encima de ella. El criterio de
   la primera ronda pasó de «respuesta débil» a **«ninguna respuesta»**.

2. **`swiss_S2`** (`rework` → `rework`). El campo inválido ahora **abre con `╲`**, la mitad abierta
   del `DANGER_FORM` con la que se dibujan los dos irreversibles del lenguaje. Y la ley del abridor
   lo exime por nombre, de modo que ningún test puede volver a señalarlo. Además, `Cancel` ganó `▫` y
   `Save` no ganó nada: en la misma fila, el botón que hay que pulsar es ahora el único de los dos
   sin marca.

3. **`darkside_S1`** (`rework` → `rework`). El leader del `field_row` se movió de `▬` (sin familia de
   significado) a `◦`, que a la altura de celda de estos frames es indistinguible de `o `,
   `LEVELS["warn"]`. Se cambió una celda muda por una homoglifa de una que habla, en el frame cuya
   objeción principal sigue esperando fallo del operador.

4. **`blueprint_S5`** (`nota` → `nota`). `━` ganó un cuarto papel — las dos paredes del campo
   inválido de `S2` — sin que nadie mirara `S5`. La nota que la primera ronda escribió («pico o
   error») ahora tiene cuatro respuestas en vez de dos.

Y el patrón que las cruza es el de §0b: **cinco de los seis lenguajes que sí tuvieron incremento
resolvieron una colisión mudándose a un homoglifo** — `• → ●` (swiss), `▬ → ◦` (darkside),
`▪ → ▶` contra `▼` (industrial), `▁ → ▮` sobre su propio caret (solari), `O → ▊` junto a `▮`
(darkside). Las tres leyes lo dan por resuelto porque comparan code points.

---

## 5. Las objeciones en pie, agrupadas por quién las arregla

### `Kit` y los tests

| # | objeción | evidencia |
|---|---|---|
| K1 | **La ley del asiento nombrado mira `switch.indicator` y nunca `switch.knob`.** darkside dibuja la perilla de cinco switches con `O` = `LEVELS["error"]` y el roster dice 0. Lo mismo en `naught` (`◉` = `REQUIRED`) y `corgi` (`██`/`▀▀`). | `darkside_S3` filas 4-8; censo `O [3 families]`; `MEANING_AT_A_NAMED_SEAT["darkside"] = 0` |
| K2 | **Las tres leyes comparan code points; el canal del lector es la forma.** Seis de los arreglos del lote cayeron en el mismo grupo visual del que salían. | §0b, §4 |
| K3 | **`Kit.PART_GLYPHS["stepper.step"][INVALID] = "]["` sigue sin arreglar y el stepper sigue sin ley.** Excluido por nombre en `inc39`, en `OPENING_CONTROLS` y en `RULED_CONTROLS`. Cuesta cinco asientos de swiss y cinco de nord en la ley del abridor. | `spec.md` §9.5, §11.5; docstring de `OPENING_CONTROLS` |
| K4 | **Ninguna ley compara dos estados del mismo `part`,** que es la forma exacta de `blueprint_S3` (`├─┤` contra `├┤·`) y de `industrial_S5` (`▪` contra `■`). | §11.3, `blueprint_S3` |

### Nivel lenguaje (una declaración de un kit)

| # | objeción | frame |
|---|---|---|
| L1 | El campo inválido lleva **las mismas dos paredes** que el campo normal y que el botón por defecto. | `instrument_S2` |
| L2 | El botón deshabilitado sigue siendo aire, sin ninguna marca, junto a un `Cancel` que sí tiene abridor. | `swiss_S2` |
| L3 | `├` es `REQUIRED` y el terminador de apertura de toda cota (7 familias); `╌` es `warn` y todo el vocabulario `DISABLED` (6 familias); on y off difieren en una celda. **blueprint no tuvo incremento.** | `blueprint_S2`, `S3` |
| L4 | Tres vocabularios de pared en una pantalla (`▐▌`, `[ ]`, `? ?`) en el lenguaje que se define por ser convencional. | `nord_S2` |
| L5 | El cursor y el `DISCLOSE` son el mismo triángulo girado. | `industrial_S1`, `S3` |
| L6 | La sparkline se dibuja con los dos peldaños altos de `LEVELS`, seis filas encima del log que los usa como severidad. | `swiss_S5`, `blueprint_S5` |

### Hoja y composición (`screens.py`, `overlay_instead`)

| # | objeción | frame |
|---|---|---|
| C1 | El control destructivo se construye con `knockout_cell(" DELETE ")` en vez de `button(..., FOCUSED, danger=True)`: sin marca de peligro y sin marca de foco **en los dos tiers**. Nombrado en `inc41` §8, sin tocar. | `blueprint_S4` |
| C2 | El modal abre con una regla de 100 celdas y **no cierra**. Nombrado en §11.3 como *still open*. | `swiss_S4` |
| C3 | La banda se sigue comiendo el gate que el propio modal nombra, y deja una costura huérfana y cinco filas de tarea bajo ninguna cabecera. | `solari_S4` |
| C4 | El `.txt` sigue sin ninguna separación de paneles; la doctrina está citada y el fallo sin dar. | `darkside_S1` |
| C5 | `BACKLOG 5▂` / `DOING 4▂`: el muñón de sparkline pegado al conteo, nombrado por la primera ronda, sin tocar. | `nord_S1` |
| C6 | La cabecera recasea la consulta (`QUERY 'RE'` contra `re`) y el estado vacío dice `NO DEPARTURES` para «la búsqueda no encontró nada». | `solari_S6` |
| C7 | Las filas 3, 13 y 20 son la misma cadena de 100 `⠒`: no hay forma de distinguir «hay un modal» de «aquí acaba la cabecera». | `instrument_S4` |

### Exportador

| # | objeción | estado |
|---|---|---|
| E1 | **Cerrada.** Los siete `S6` pintan su tier declarado (`inc43`), con el séptimo `re` excluido por aserción. | §0a |
| E2 | **Abierta y nueva:** el `.svg` no lleva métrica de fuente, así que ninguna objeción de homoglifo (§0b) ni la de `▪`/`■` de `industrial_S5` se puede **resolver** desde el artefacto. Haría falta un tier más: un raster a la altura de celda de diseño. | `industrial_S5`, K2 |
| E3 | `gallery_darkside` es dependiente del calendario (`PHASES[date.today().day % 6]`); ningún re-horneado lo cierra. | `spec.md` §10.3 |

---

## 6. Lo que le toca decidir al operador

**A. `corgi`, `prism` y `blueprint` nunca han tenido un incremento, y son los peores del corpus en
todos los rosters que este lote construyó.** corgi: 31 asientos de abridor, 8 de asiento nombrado, 2
filas vivas de significado × significado. prism: 19 / 8 / 1. blueprint: 6 / 8 / 3. Doce de los 66
frames del repo (corgi y prism) **no los ha juzgado ninguna ronda**. ¿Se abre un lote, o se escribe
que la matriz de once lenguajes tiene tres sin juzgar?

**B. La ley del stepper.** Dos leyes lo excluyen por nombre, `Kit` tiene el giro `][` sin arreglar y
ningún frame del barrido renderiza un stepper inválido. Se escribe la ley, o se escribe que el
stepper queda fuera de la regla.

**C. La ruling de `inc39`: `INVALID` toma el `DANGER_FORM`.** Es por lo que `swiss ╲12/09/26`,
`blueprint ━12/09/26━`, `darkside Ø…Ø`, corgi y ledger deletrean «este valor no parsea» con la misma
celda con la que deletrean «esto destruye datos». El censo lo marca y dice que **no puede distinguir
una alineación deliberada de un accidente**; la ley del abridor lo exime por nombre. Se ratifica o se
revierte; hoy está aplicado sin que nadie lo haya aprobado como tal.

**D. ¿El diámetro y la rotación son «un canal que el lenguaje declara»?** La regla del lote lista
*cuenta, peso, tier, posición*. Seis arreglos usaron diámetro (`• ●`, `o ◦`), rotación (`▶ ▼`,
`▸ ▶`) o ancho (`▊ ▮`). Si la respuesta es sí, esos seis quedan como están y hay que añadirlos a la
lista de canales. Si es no, esos seis están a medias y las tres leyes necesitan una cláusula de
familia de forma.

**E. `darkside_S1` y «el `.txt` es la obra».** La pregunta 10 de la primera ronda sigue sin fallo:
o el rail cede, o la convención admite una excepción escrita para este lenguaje. `spec.md` §11.3 dice
literalmente que la decisión es del operador.

**F. `solari_S4`.** ¿«Una salida se apodera de la cabecera del tablero» es doctrina escrita de este
lenguaje, o un confirm destructivo tiene que dejar en pantalla el gate que nombra? Hoy la banda se
come `GATE BACKLOG` y sus dos tareas, y el tablero superviviente arranca en una costura huérfana.

**G. La ley de primera fijación de blueprint está ejercitada en un test y no está en ninguna
imagen.** El knockout del title block sólo se enciende en el mood `alert` y el fixture está en
calma. ¿Se añade un frame en mood `alert` al barrido, o se acepta que el mecanismo firma de uno de
los once lenguajes nunca aparece en la galería?

---

## 7. Lo que esta ronda sigue sin poder ver

Se dice llano, y se dice segunda vez porque sigue siendo verdad.

1. **No se ejecutó nada.** Se leyeron 42 `.txt` y 42 `.svg` a HEAD y los mismos 42 `.txt` a
   `8604607`. **No se ejecutó la aplicación, no se pulsó ninguna tecla, no se movió ningún foco y no
   se cambió ningún estado.** Todo lo de arriba es un recorrido cognitivo sobre imágenes fijas con
   criterios declarados. Tampoco se corrió la suite ni ninguno de los scripts: los números de gates
   citados (1040 passed, censo 48, rosters) están **leídos de los packets y del
   `collision_census.txt` en disco**, no reproducidos aquí.
2. **Un solo ancho.** Los 42 están a 100×32. Los compromisos que dicen «at any width» siguen juzgados
   a un ancho. `inc36` encontró un defecto real de blueprint a `w=1`; el agujero sigue abierto.
3. **El foco es una decoración fija.** `FOCUSED` se lee de una marca, no de un foco. Qué pasa al
   pulsar `tab`, si el anillo salta donde el lector espera y si el orden de tabulación coincide con
   el visual: ninguna es respondible desde un frame. Todo lo dicho sobre «el destructivo está
   enfocado» sigue siendo lectura de una marca.
4. **La métrica de fuente.** El tier de estilo ya se ve, pero el `.svg` no dice a qué tamaño de celda
   ni con qué fuente se va a renderizar. Por eso **ninguna** de las objeciones de homoglifo de §0b
   está *resuelta* aquí: están *planteadas* con la evidencia de la declaración, y hace falta un
   raster a la altura de celda real para cerrarlas.
5. **Animación, latencia y asentamiento.** Capturados con `animations off`; los frames son la lectura
   estable de ocho. El estado `held` del log y el coste de repintado no están aquí.
6. **La densidad como se experimenta.** §1 es aritmética de celdas.
7. **Usuarios reales.** ISO 9241-210 pide evaluación con usuarios; este equipo es una persona. Lo que
   hay aquí es **inspección con criterios declarados**, un recorrido cognitivo sobre las tareas que
   el contexto de uso nombra. **No se hizo ninguna evaluación con usuarios reales, y ninguna
   afirmación de este documento debe leerse como si se hubiera hecho.**

---

## 8. Cómo reproducir esta ronda

```
git -C <worktree> diff --stat 8604607 HEAD -- prototypes/components/
git -C <worktree> show 8604607:prototypes/components/<frame>.txt
python -X utf8 prototypes/components/render.py       # 66 .txt + 66 .svg + 66 .candidates.md
python -X utf8 prototypes/collision_census.py        # prototypes/out/collision_census.txt
python -X utf8 prototypes/verify_ink.py --frames     # tinta determinista sobre los 66
python -X utf8 -m pytest -q                          # las tres leyes y sus tests de dientes
```

Los contrastes de §0a se derivan de los `fill=` de los siete `*_S6.svg` con la fórmula WCAG de
luminancia relativa; los conteos de `<rect>`, `font-weight` y `text-decoration` con `re.findall`
sobre los mismos ficheros. Los diffs de celdas están citados con las dos versiones al lado para que
nadie tenga que creerse este documento.

**Página del operador:** `ronda-36-despues.html`, con los 42 frames nuevos, el `.svg` viejo al lado
para los 26 que se movieron, y un voto por frame.

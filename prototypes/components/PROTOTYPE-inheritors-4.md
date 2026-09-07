# PROTOTYPE-inheritors-4 — los 66 frames tras `rework-6a/6b/6c`, y la primera ronda que mide la pintura

**Cuarta ronda adversarial sobre el corpus completo.** La tercera (`PROTOTYPE-inheritors-3.md`,
2026-09-07, en `abd5193`/`f1508ad`) juzgo los 66 por primera vez y devolvio **keep 15 · nota 40 ·
rehacer 11**, con ocho objeciones nuevas (K5, L7–L10, C8–C10, E4) y seis desacuerdos con rulings
firmes. Desde entonces corrieron tres lotes y nueve incrementos: `rework-6a` (inc63–66), `rework-6b`
(inc67–70) y `rework-6c` (inc71).

Esta ronda **no toco ningun kit, ningun test y ningun frame**: leyo los 66 `.txt` y los 66 `.svg` a
`4089eda`, los `.txt` y `.svg` de `f1508ad` para comparar, `spec.md` §16–§18, los nueve packets,
`prototypes/out/collision_census.txt` y `taskboard/themes.py`. Vocabulario de veredicto cerrado, el
mismo: **`keep` / `keep with a note` / `rework`**. Propuestos, no decididos.

Las rulings de inc63–inc71 son del orquestador sobre la delegacion del operador y **son firmes**: aqui
se juzga si el frame las honra. Donde no estoy de acuerdo con una ruling va una linea en §7.

**Resultado: keep 11 · nota 51 · rehacer 4.** Siete `rework` se cerraron y **cuatro `keep`
retrocedieron a nota, los cuatro por la misma medicion**, que es la primera vez en cuatro rondas que
una etiqueta baja.

---

## 0. Tres cosas que hay que decir antes de la primera tabla

### 0a. E4 esta respondida, y al cerrarla el exportador dejo de mentir sobre algo mas grande

inc63 hizo lo que la ronda tres pidio en una linea: `cell_grid()` lee `THEMES[lang]["ground"]` y el
`.svg` pinta el ground declarado. **Verificado sobre los 66**: el `<rect>` de lienzo de cada frame es
byte a byte el `ground` de su kit, en los once. El criterio ejecutable de §0a de la ronda tres
—*abrir `ledger_S1.svg` y decir que tarea esta en `DOING`*— **responde**: `#1c1a15` sobre `#e9e1cf`
es **13,36:1**.

Y ahora que el fondo es real, los demas numeros se pueden calcular por primera vez. **Esta ronda los
calculo, celda a celda, atribuyendo cada caracter al rect que hay realmente debajo de el.** El
resultado es la tabla que ninguna ronda tuvo:

| lenguaje | ground | `ink` | `mut` | `dim`/`seam`/`rail` | celdas `dim` en las 6 hojas | % de la hoja bajo 3:1 |
|---|---|---|---|---|---|---|
| instrument | `#0a0d12` | 16,52 | 4,50 | **1,74** | 2488 | **68 %** |
| swiss | `#101010` | 17,30 | 5,51 | **1,75** | 1829 | **60 %** |
| industrial | `#1a1a1a` | 15,55 | 5,38 | **1,96** | 1828 | **58 %** |
| nord | `#2e3440` | 10,84 | 4,51 | **1,69** | 1351 | **54 %** |
| darkside | `#000000` | 19,26 | 4,56 | **1,39** | 899 | 45 % |
| solari | `#0b0b0c` | 16,81 | 3,65 (exenta) | **1,20** | 2355 | **79 %** |
| blueprint | `#123a5c` | 10,60 | 4,65 | **1,24** | 1155 | 41 % |
| naught | `#000000` | 19,26 | 6,08 | **1,35** | 2391 | **62 %** |
| corgi | `#0d0d0d` | 17,36 | 6,91 | **1,71** | 519 | 19 % |
| prism | `#0d1117` | 16,02 | 6,43 | **3,25** | 559 | 27 % |
| ledger | `#e9e1cf` | 13,36 | 4,51 | **1,50** | 622 + 1619 (`rule` 2,92) | 48 % |

**`dim` esta por debajo de 3:1 en los once y por debajo de 1,6:1 en cinco. En seis de los once, mas
de la mitad de las celdas pintadas de la hoja estan bajo 3:1.** inc70 midio `dim` y lo dejo en un
roster por decision escrita; el roster son once numeros y estos frames son la consecuencia.

**Y la inversion de ledger no se cerro: se dio la vuelta.** La ronda tres midio `ink` 1,08:1 y `dim`
9,62:1 y escribio *«lo unico legible son los puntos guia»*. Hoy `ink` es 13,36:1 y `dim` es
**1,50:1** — que es lo correcto para un guia de puntos, salvo que `#c4b99f` tambien pinta
`· form`, `· cfg` y `· log`, **las tres etiquetas de modo inactivas de la fila 1**, y el `low` de la
tabla de detalle. **Criterio observable:** abrir `ledger_S1.svg` y nombrar los cuatro modos.
Responde uno.

### 0b. El peldanio `info` no se ve en nueve de los once, y solo dos lo declaran

L7 quedo **RULED como doctrina** en §16.1 para blueprint y ledger: *«una escalera de tipo de linea
donde la AUSENCIA es el estado calmo»*. Esta ronda midio el color con que se pinta cada peldanio en
la hoja `S5` de los once:

| lenguaje | `info` | ratio | `warn` | ratio | `error` | ratio |
|---|---|---|---|---|---|---|
| instrument | `⠂⠂` | **1,74** | `⠆⠆` | 4,50 | `⠇⠇` | 16,52 |
| swiss | `·` | **1,75** | `─` | 5,51 | `━` | 17,30 |
| industrial | `▫▫` | **1,96** | `▪▪` | 5,38 | `■■` | 15,55 |
| nord | `·` | **1,69** | `!` | 4,51 | `!!` | 10,84 |
| darkside | `·` | **1,39** | `o` | — | `O` | — |
| naught | `◦◦` | **1,35** | `∙◦` | 6,08 | `∙∙` | 19,26 |
| corgi | `▁▁` | **1,71** | `▄▄` | 6,91 | `██` | 17,36 |
| prism | `⣀⣀` | 3,25 | `⣤⣤` | 6,43 | `⣿⣿` | 16,02 |
| blueprint | (aire) | — | `╌╌` | 4,65 | `━━` | 10,60 |
| ledger | (aire) | — | `* ` | 4,51 | `**` | 13,36 |
| solari | `OK ` | palabras | `DLY` | — | `CNX` | — |

**Siete lenguajes dibujan su peldanio `info` y lo pintan entre 1,35:1 y 1,96:1.** Dos lo declaran
aire por doctrina. Uno usa palabras. Uno (prism, 3,25:1) lo pinta por encima del piso de 3:1 que WCAG
1.4.11 pide a un componente no textual.

**Criterio observable, ejecutable sobre cualquiera de las siete hojas:** en `<lang>_S5.svg`, senialar
las filas del log que llevan una severidad. Responden dos de las ocho; las seis de `info` estan
pintadas al mismo nivel que el fondo. **Es la misma frase que la ronda tres le escribio a
`blueprint_S5` y a `ledger_S5`, y ahora vale para nueve de once por dos caminos distintos.**
Ninguna ley lo mira: inc70 asertar `ink` y `mut`, y `LEVELS["info"]` no es ninguno de los dos.

**Esto no es una regresion de inc63.** Contra el falso `#121212`, `#333c47` marcaba 1,62:1 y hoy
marca 1,74:1: los numeros apenas se movieron. Lo que cambio es que **ahora significan algo**, porque
se miden contra un ground declarado en vez de contra un fondo inventado. Es la clase buena de
empeorar, y es la razon por la que cuatro `keep` bajan a nota en §1.

### 0c. El piso de `mut` compro legibilidad contra el fondo y la pago en el tier de match

inc70 subio cuatro `mut` *«por el paso mas pequenio que preserva el matiz»* y lo hizo bien: los
cuatro cruzan 4,5:1. Nadie midio el otro numero que ese token sostiene — el salto entre la tinta del
match y el cuerpo, que es el unico canal que tiene la pantalla `S6` con el color quitado.

| lenguaje | `mut` antes → despues | match ↔ cuerpo, antes | despues | |
|---|---|---|---|---|
| **nord** | `#7b88a1` → `#919cb0` | 1,79:1 | **1,38:1** | **PEOR** |
| instrument | `#6b7785` → `#6e7b89` | 2,45:1 | 2,32:1 | PEOR |
| ledger | `#6b6558` → `#6a6458` | 3,00:1 | 2,96:1 | PEOR |
| darkside | `#737373` → `#757575` | 4,35:1 (placa↔cuerpo) | 4,23:1 | PEOR |
| darkside | idem | 4,43:1 (knockout) | **4,56:1** | mejor |

**nord_S6 pasa de 1,79:1 a 1,38:1 y se convierte en el segundo peor del corpus**, por debajo del 1,58
de prism y a dos centesimas del 1,36 de swiss. La ronda tres lo cito como *«la linea base contra la
que eligieron los otros diez»*. Ya no lo es, y el lote que lo movio no lo midio: **subir `mut` hacia
`ink` es, por construccion, bajar todo canal que separaba `mut` de `ink`.**

Los cuatro kits que inc70 movio quedan ademas **pegados al piso**: instrument 4,50 · nord 4,51 ·
ledger 4,51 · darkside 4,56. Tres de los cuatro estan a una centesima.

---

## 1. La matriz 11×6

Antes (`f1508ad`, ronda tres) → despues (`4089eda`, esta ronda).

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| **instrument** | nota → **nota** | nota → **nota** | nota → **nota** | nota → **nota** | keep → **nota** | keep → **keep** |
| **swiss** | nota → **nota** | rework → **nota** | keep → **keep** | rework → **nota** | nota → **nota** | nota → **nota** |
| **industrial** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | keep → **nota** | keep → **keep** |
| **nord** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | keep → **nota** | nota → **nota** |
| **darkside** | nota → **nota** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **nota** | keep → **keep** |
| **solari** | nota → **nota** | nota → **nota** | keep → **keep** | nota → **nota** | nota → **nota** | nota → **nota** |
| **blueprint** | nota → **nota** | nota → **nota** | rework → **rework** | nota → **nota** | nota → **nota** | keep → **keep** |
| **naught** | nota → **nota** | rework → **rework** | nota → **nota** | rework → **rework** | nota → **nota** | nota → **nota** |
| **corgi** | rework → **nota** | nota → **nota** | nota → **nota** | rework → **nota** | nota → **nota** | nota → **nota** |
| **prism** | rework → **nota** | rework → **nota** | nota → **nota** | nota → **nota** | nota → **nota** | nota → **nota** |
| **ledger** | nota → **nota** | nota → **nota** | nota → **nota** | rework → **rework** | nota → **nota** | rework → **nota** |

|  | keep | keep with a note | rework |
|---|---|---|---|
| **ronda tres** (`f1508ad`) | 15 | 40 | 11 |
| **ronda cuatro** (`4089eda`) | **11** | **51** | **4** |

**Siete `rework` cerrados:** `swiss_S2` (L2), `swiss_S4` (C2), `corgi_S1` (K5), `corgi_S4` (C8, por
ruling), `prism_S1` (L9), `prism_S2` (L8), `ledger_S6` (E4).

**Cuatro `keep` retrocedidos, todos por §0b:** `instrument_S5`, `industrial_S5`, `nord_S5`,
`darkside_S5`. Es la primera bajada de etiqueta en cuatro rondas y **no la causo ningun incremento**:
la causo un instrumento nuevo aplicado a frames que no se movieron.

**Cuatro `rework` en pie:** `blueprint_S3` (K4 en el frame), `naught_S2` (L10), `naught_S4` (el marco
del modal es el `DANGER_FORM`), `ledger_S4` (C2). **Los cuatro estaban nombrados en la ronda tres y
los cuatro son un incremento de un fichero.**

**Trece `.txt` se movieron** (`corgi_S1` `S4` `S6`, `ledger_S4`, `naught_S1` `S4`, `prism_S1` `S2`
`S3` `S4`, `solari_S4`, `swiss_S2` `S4`) y **los 66 `.svg`**, una vez, en inc63.

---

## 2. Los 66 bloques

Contexto de uso, sin cambios: **operador unico** (`jav201`), terminal 100×32 monoespaciada, sesion
diurna, tema por defecto; la tarea es la que la pantalla nombra. Formato: *objecion previa · que
cambio · estado · veredicto*.

---

### 2.1 instrument

`LEVELS ⠂⠂/⠆⠆/⠇⠇` · `REQUIRED ⠁` · `DANGER ⠛⠛` · `CUR ⣿` · `FIELD_LEAD ⠒`. **Ningun `.txt` se movio
en los tres lotes.** `mut` subio `#6b7785` → `#6e7b89` (inc70) y el ground pasa a `#0a0d12` (inc63).

#### `instrument_S1` — nota → **`keep with a note`**
* **Objecion previa:** el gutter `⠸` compite con los leaders `⠒` del panel derecho.
* **Que cambio:** nada en el frame. El `.svg` pinta ahora el ground declarado.
* **Estado: en pie, y con una lectura nueva a favor del frame.** Medido: los leaders `⠒` van en `dim` a **1,74:1** y el gutter en `mut` a **4,50:1**. Hay un canal de contraste de 2,6× entre los dos, y ninguna ronda lo habia podido ver porque el fondo era falso. **Criterio:** en `instrument_S1.svg`, distinguir el gutter del leader. Responde el contraste; no responde la celda.
* **Lo que no cierra:** con el color quitado —que es como se juzga el resto del corpus— siguen siendo la misma celda.
* **Veredicto: `keep with a note`.**

#### `instrument_S2` — nota → **`keep with a note`**
* **Objecion previa:** `⠶` es el campo invalido (27 celdas) **y** el radio elegido tres filas mas abajo.
* **Que cambio:** nada. inc71 movio la RUNA del campo a cromo, pero el invalido de instrument es una tirada uniforme sin abridor/runa/cierre, asi que `split_field_glyph` no lo alcanza. Censo: `⠶ [6 families]`, sin cambio de rol.
* **Estado: en pie, entera, cuarta ronda.**
* **Veredicto: `keep with a note`.**

#### `instrument_S3` — nota → **`keep with a note`**
* **Objecion previa:** `⣿` es `CUR` y el relleno de cinco switches y del slider y la pestania activa.
* **Que cambio:** nada en el frame, y **mucho en el censo**. inc67 metio el conjunto B: `⣿ [3 families]` → **`⣿ [7 families]`** — CUR, `bar.indicator`, `mascot.pixel`, `meter.fill`, `spark.peak`, `scrollbar.indicator`, `slider.indicator`, `switch.indicator`.
* **Estado: en pie, y peor medida.** Es la clase buena de empeorar: el instrumento aprendio a verla. `CUR` sigue fuera del conjunto de significados por decision documentada.
* **Veredicto: `keep with a note`.**

#### `instrument_S4` — nota → **`keep with a note`**
* **Objecion previa (C7):** las filas 3, 13 y 20 son la misma cadena de 100 `⠒`.
* **Que cambio:** nada, cuarto lote.
* **Estado: en pie.** Y el `.svg` la agrava por un lado nuevo: las tres cadenas van en `dim` a 1,74:1, asi que en el artefacto no hay ni siquiera la diferencia de peso que un `.txt` sugiere.
* **Veredicto: `keep with a note`.**

#### `instrument_S5` — keep → **`keep with a note`**
* **Objecion previa:** ninguna. La ronda tres la llamo *«de las dos mejores escaleras del corpus con el color quitado»*.
* **Que cambio:** nada en el frame. El `.svg` pinta el ground declarado por primera vez.
* **Objecion nueva, y es la que baja la etiqueta (§0b):** el peldanio `info` `⠂⠂` va en `dim` a **1,74:1**. **Criterio observable:** en `instrument_S5.svg`, senialar las filas del log que llevan una severidad. Responden dos (`⠆⠆` a 4,50 y `⠇⠇` a 16,52); las seis de `info` estan al nivel del fondo. La escalera sigue siendo monotona por cuenta de puntos **en el `.txt`** y deja de serlo en el unico tier que lleva color.
* **A favor:** la escalera tambien es monotona en contraste (1,74 / 4,50 / 16,52), lo cual es un tercer canal bien puesto. El problema no es el orden, es el suelo.
* **Veredicto: `keep with a note`.** El eje: el peldanio bajo esta por debajo del piso de 3:1 de WCAG 1.4.11 en el artefacto de registro.

#### `instrument_S6` — keep → **`keep`**
* Frame identico. El subrayado sigue. **El salto de color bajo 2,45:1 → 2,32:1** por el `mut` de inc70 (§0c): es un 5 % y el subrayado no se movio, asi que la etiqueta aguanta.
* **Nota que engorda por tercera ronda:** `#2dd4bf` es el acento de match de instrument **y** de prism, y en los dos es la tinta del cursor de la misma fila.
* **Veredicto: `keep`.**

---

### 2.2 swiss

`LEVELS ·/─/━` · `REQUIRED •` · `DANGER ╲╱` · `CUR ▮` · `FIELD_LEAD ""`. **Dos frames movidos**
(inc66, inc69). `mut` sin cambio.

#### `swiss_S1` — nota → **`keep with a note`**
* **Objecion previa:** tres hairlines en una pantalla cuyo compromiso dice «una»; `▮ ▪ ■ ▫` son cuatro rectangulos macizos.
* **Que cambio:** nada.
* **Estado: en pie.** Y el `.svg` anade: las hairlines van en `dim` a **1,75:1**, 1829 celdas en las seis hojas. **Criterio:** en `swiss_S1.svg`, decir cuantas reglas hay. La respuesta de la ronda tres era «tres, y ese es el problema»; en el artefacto la respuesta es «no se ven».
* **Veredicto: `keep with a note`.**

#### `swiss_S2` — rework → **`keep with a note`**
* **Objecion previa:** **(a)** `Save` (DISABLED) es aire; **(b)** cinco controles abren con pared y ninguno cierra; **(c)** el invalido abre con `DANGER_FORM[0]` (ya cerrada en ronda tres por ruling C).
* **Que cambio** (inc66 ruling C follow-through, inc69 ruling L2):

  ```
  f1508ad  due•          ║12/09/26
  4089eda  due•          ║12/09/26┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆┆║

  f1508ad                     Save        ▫   Cancel
  4089eda                ╎    Save        ▫   Cancel
  ```
* **Estado: (a) RESPONDIDA.** `╎` es una marca, derivada de la celda muerta de `stepper.main`, y la ley de inc69 la asegura sobre los 110 asientos que el registro deriva por kit, a tres anchos. **Cinco lotes y tres rondas de L2, cerrada.** **(b) RESPONDIDA a medias y solo en un asiento:** `║12/09/26┆…┆║` abre, empapela y cierra, y el criterio *«decir hasta donde llega el campo de fecha»* responde por primera vez. Los otros cinco controles siguen sin cerrar.
* **Objecion nueva, y es de las que empeoraron:** la pantalla tiene ahora **seis verticales distintas** — `┃` (titulo), `║` (invalido), `│` (checkbox, notas), `╵` (radio), `╎` (Save muerto), `▏` (caret) — y la de inc69 es la sexta. **Criterio observable:** en `swiss_S2`, tapar las palabras y decir cual de las verticales marca un control muerto y cual uno vivo. `╎` contra `│` es un trazo entero contra un trazo roto a 12 px. Es L4 (nord: *«tres vocabularios de pared en una pantalla»*) en el lenguaje que la ronda tres declaraba el mas limpio de paredes.
* **Y lo que no se movio:** `▪` sigue siendo el radio elegido (f10) y el checkbox marcado (f12), dos filas seguidas, y el anillo de foco de `╲Delete╱` en `S4`.
* **Veredicto: `keep with a note`.** L2 cerrada; el eje que queda es la familia de verticales, y es de declaracion.

#### `swiss_S3` — keep → **`keep`**
* Frame identico. `▫ ▪ ■` sigue avalada por la ruling D-addendum. `─` (`warn`) sigue siendo la pista apagada del switch y la vacia del slider — y ahora **rostrado**: `FILL_IS_NOT_A_MEANING["swiss"] = 3`. La objecion existe, esta contada y tiene duenio.
* **Veredicto: `keep`.**

#### `swiss_S4` — rework → **`keep with a note`**
* **Objecion previa (C2):** el modal abre con una regla de 100 celdas y **no cierra**. Sin mover un byte desde `8604607`.
* **Que cambio** (inc66): `Swiss.overlay_instead` cierra su banda con una segunda regla en la fila 21.
* **Estado: RESPONDIDA.** **Criterio observable:** decir donde termina el modal. Responde: fila 21, con la misma regla que lo abre. Tres rondas y seis lotes, cerrada.
* **El coste, declarado aqui porque el packet no lo cuenta:** la banda crecio una fila y **`Rate-limit the API 2d!` desaparecio del tablero de detras**. `▮ D O I N G  4` dice cuatro y ensenia una. Es el precio correcto por un cierre, y hay que escribirlo.
* **Objecion nueva, menor:** las dos reglas del modal miden 100 celdas y la del masthead 99. Un canal de una celda no es un canal. Es C7 con otra forma, un lenguaje mas.
* **Veredicto: `keep with a note`.**

#### `swiss_S5` — nota → **`keep with a note`**
* **Objecion previa (L6):** la sparkline usa los dos peldanios altos de `LEVELS`.
* **Que cambio:** nada en el frame; L6 **contada por primera vez** (inc67, cinco de las dieciseis filas de `FILL_IS_NOT_A_MEANING`).
* **Objecion nueva (§0b):** `·` (`info`) va a **1,75:1**.
* **Veredicto: `keep with a note`.**

#### `swiss_S6` — nota → **`keep with a note`**
* **Objecion previa:** `#e2231a` contra el cuerpo `#8a8a8a` es **1,36:1**, el peor del corpus.
* **Que cambio:** nada; `mut` de swiss no se movio, asi que 1,36 sigue exacto. **Sigue siendo el peor de los once**, ahora por dos centesimas sobre nord (§0c).
* **Veredicto: `keep with a note`.**

---

### 2.3 industrial

`LEVELS ▫▫/▪▪/■■` · `REQUIRED !` · `DANGER ╱╱` · `CUR ▶` · `DISCLOSE ▼`. Ningun `.txt` movido; `mut`
sin cambio.

#### `industrial_S1` — nota → **`keep with a note`**
* **Objecion previa (L5):** retirada por ruling en la ronda tres. Queda el plato `▐▌` con cuatro sentidos.
* **Que cambio:** nada. Censo: `▐ [3 families]` y `▌ [3 families]`, sin mover.
* **Veredicto: `keep with a note`.**

#### `industrial_S2` — nota → **`keep with a note`**, y la nota se reescribe por inc71
* **Objecion previa:** las paredes del campo invalido son las del normal y las del boton; el canal que queda es el relleno `//////` contra `------`.
* **Que cambio:** nada en el frame. **inc71 partio el rol de la celda:** el papel del campo pasa a cromo y el censo revela una fila que estaba escondida — `/ [2 families]`: `INVALID slider.knob` + `INVALID stepper.step` contra `textfield.main mark (invalid)`.
* **La pregunta que el brief pone, respondida sobre el frame:** en `industrial_S2`, **un lector no puede distinguir papel de rechazo, y no por la razon que inc71 nombra.** Medido sobre los seis frames de industrial: `/` aparece **28 veces en `S2`, una en `S5` y cero en las otras cuatro**. El slider de `industrial_S3` es `[████████|···]` y no dibuja `/`; ningun artefacto del repo dibuja un stepper (§12.5). **El segundo rol de `/` no se renderiza en ninguno de los 66 frames**, asi que la colision que inc71 midio es real en la declaracion e **incomprobable en el corpus**.
* **La colision que si se ve, y que nadie ha nombrado:** de las 28 `/` de `S2`, **26 son el papel y dos son los separadores del propio valor** — `▐12/09/26//////////////////////////▌`. **Criterio observable:** en la fila 6, decir donde acaba el valor introducido y donde empieza el papel. Sin respuesta salvo por conocimiento previo de que una fecha lleva dos barras. El canal de relleno que la ronda tres llamo *«real y ancho»* es ancho contra el campo normal y nulo contra su propio contenido.
* **Veredicto: `keep with a note`.**

#### `industrial_S3` — keep → **`keep`**
* Frame identico. Sigue siendo la referencia del corpus para la separacion caption/control. `FILL_IS_NOT_A_MEANING["industrial"] = 0`: el slider `[████████|···]` no gasta ningun peldanio, y es uno de los cinco kits limpios en el roster nuevo.
* **Veredicto: `keep`.**

#### `industrial_S4` — keep → **`keep`**
* Frame identico. Sigue siendo la mejor superposicion de los once con nord: tablero entero detras, modal cerrado por sus cuatro lados, respuesta destructiva mas pesada.
* **Veredicto: `keep`.**

#### `industrial_S5` — keep → **`keep with a note`**
* **Que cambio:** nada en el frame; el ground declarado en el `.svg`.
* **Objecion nueva (§0b):** `▫▫` (`info`) va en `dim` a **1,96:1**. La escalera `▫▫ ▪▪ ■■` que la ruling D-addendum avalo por ir *«de hueco a lleno y creciendo en el mismo sentido»* es correcta en forma y tiene el peldanio bajo por debajo del piso de 3:1 en el artefacto.
* **Criterio observable:** en `industrial_S5.svg`, senialar las filas con severidad. Responden dos de ocho.
* **Veredicto: `keep with a note`.**

#### `industrial_S6` — keep → **`keep`**
* Frame identico. Los seis platos `#ff4b1f` con tinta `#1a1a1a` dan **5,20:1** medidos contra el ground real (la ronda tres cito 5,60 contra el falso `#121212`): la ruling se sostiene con el numero correcto.
* **Nota nueva, medida:** el corchete de foco `▐` del campo de consulta va en `focus #2e2e2e` sobre el ground `#1a1a1a`, **1,28:1**, ocho celdas. Y el cuerpo `mut` sobre el plato de detalle `#2e2e2e` cae a **4,20:1**, por debajo del piso que inc70 acaba de asertar contra el ground (§7.2).
* **Veredicto: `keep`.**

---

### 2.4 nord

`LEVELS "· "/"! "/"!!"` · `REQUIRED *` · `DANGER ##` · `CUR ▸`. Ningun `.txt` movido. **`mut`
`#7b88a1` → `#919cb0`** (inc70).

#### `nord_S1` — nota → **`keep with a note`**
* **Objecion previa (C5):** el munion de sparkline pegado al conteo; la pista vacia del medidor es la misma celda que las reglas de seccion.
* **Que cambio:** nada, quinto lote. `FILL_IS_NOT_A_MEANING["nord"] = 0` — el medidor de nord no gasta ningun peldanio, y eso es a su favor.
* **Nuevo:** `│` y las reglas van en `dim` a **1,69:1**, 1351 celdas.
* **Veredicto: `keep with a note`.**

#### `nord_S2` — nota → **`keep with a note`**
* **Objecion previa (L4):** tres vocabularios de pared, mas un cuarto declarado y no renderizado (`░░` del stepper).
* **Que cambio:** nada. El stepper sigue sin dibujarse en ningun artefacto del repo.
* **Estado: en pie**, y con compania: swiss llego a seis verticales en `S2` (§2.2).
* **Veredicto: `keep with a note`.**

#### `nord_S3` — keep → **`keep`**
* Frame identico. `[ #Delete all# ]` con caption desnudo.
* **Veredicto: `keep`.**

#### `nord_S4` — keep → **`keep`**
* Frame identico. `▐  #Delete#  ▌` contra `[ ]`. Sigue siendo el mejor modal del corpus con industrial: caja cerrada, tablero detras, dos respuestas distinguibles.
* **Veredicto: `keep`.**

#### `nord_S5` — keep → **`keep with a note`**
* **Que cambio:** nada en el frame.
* **Objecion nueva (§0b):** `·` (`info`) va a **1,69:1** — el segundo mas bajo de los siete. La ronda uno llamo a esta pantalla *«el caso mas limpio de todo el programa»* y lo sigue siendo en el `.txt`.
* **Veredicto: `keep with a note`.**

#### `nord_S6` — nota → **`keep with a note`**, y es la que mas empeoro de las 66
* **Objecion previa:** `#88c0d0` contra el cuerpo `#7b88a1` es **1,79:1**, y la ronda tres lo cito como *«la linea base contra la que eligieron los otros diez»*.
* **Que cambio:** el frame nada. **inc70 subio `mut` a `#919cb0` para cruzar 4,5:1 contra el ground, y el salto del match cayo a `1,38:1`.**
* **Estado: EMPEORO, bajo etiqueta fija, por obra de un incremento cuyo proposito era la legibilidad.** nord pasa de ser la referencia del tier a ser el segundo peor del corpus, a dos centesimas de swiss. **Criterio observable:** en `nord_S6.svg`, con el color quitado, senialar las seis coincidencias. Responde el peso y nada mas.
* **Y ninguna ley lo vio:** inc70 asertar `contrast(mut, ground)`; el numero que se rompio es `contrast(accent, mut)`, y no existe.
* **Veredicto: `keep with a note`.** Se mantiene la etiqueta por consistencia con `swiss_S6` (1,36, nota desde la ronda dos); el eje se registra en §4 y en §7.1.

---

### 2.5 darkside

`LEVELS "· "/"o "/"O "` · `REQUIRED ▪` · `DANGER ▚▞` · `CUR ▊` · `FIELD_LEAD ▔`. Ningun `.txt`
movido. **`mut` `#737373` → `#757575`** (inc70).

#### `darkside_S1` — nota → **`keep with a note`**
* **Objecion previa:** la ruling E asciende el `.svg` a artefacto de registro **y estaba sin auditar** (§7.3 de la ronda tres): el exportador no llevaba el ground declarado.
* **Que cambio** (inc63): el lienzo pinta `#000000`, el ground declarado de darkside. La ronda tres dijo que *«que darkside no salga danado es suerte»*; **medido, era suerte, y ahora es una medicion**: `#121212` no lo declara ningun kit.
* **Estado: la objecion a la ruling esta RESPONDIDA. La ruling E se sostiene sobre un exportador auditado.**
* **Objecion nueva, y sale de la misma auditoria:** en el artefacto de registro, `rail #262626` sobre `#000000` es **1,39:1**, y son **899 celdas** — la tirada mas grande de darkside, que incluye los `( )` de pestanias y checkboxes. **Criterio observable:** en `darkside_S1.svg`, senialar el escalon gris que separa los paneles. Es lo unico que la ruling E defendia, y esta a 1,39:1.
* **Lo que la ruling no cierra:** los dieciseis trazos del rail y **E2**.
* **Veredicto: `keep with a note`.**

#### `darkside_S2` — nota → **`keep with a note`**
* **Objecion previa:** `▬` con cinco significados; y `( )` de pestania es byte a byte `checkbox.main[default]`.
* **Que cambio:** nada. **inc68 midio la segunda por primera vez:** `state_channel()` deja a darkside con **1 fila** de estados indistinguibles y el censo con **8 filas de homoglifo** (`· ●`, `o ◦`, `O ◦`, `o ◎`, `o ◉`, `O ◎`, `O ◉`, `▪ ▫`).
* **Estado: en pie, y contada.** El instrumento existe y el frame no se movio. Y en el `.svg`, los `( )` van a 1,39:1: la pregunta *«cuales de los siete pares de parentesis son pestanias y cuales casillas»* es hoy inatendible en el artefacto por una razon distinta a la que la ronda tres nombro.
* **Veredicto: `keep with a note`.**

#### `darkside_S3` — nota → **`keep with a note`**
* **Objecion previa:** `▔` es el `FIELD_LEAD` de seis filas de detalle **y** el abridor del caption destructivo.
* **Que cambio:** nada. Es C9, y C9 sigue sin tocar en tres lenguajes.
* **Veredicto: `keep with a note`.**

#### `darkside_S4` — keep → **`keep`**
* Frame identico. La nota de la ronda dos sigue resuelta por ruling D (peso es canal).
* **Nota nueva:** `#000000` es el ground declarado, asi que las 12 celdas de knockout de `S6` suben de 4,43 a **4,56:1** por el `mut` de inc70. Es la unica de las cuatro mediciones de §0c que mejoro.
* **Veredicto: `keep`.**

#### `darkside_S5` — keep → **`keep with a note`**
* **Que cambio:** nada en el frame.
* **Objecion nueva (§0b), y es la mas dura de las cuatro bajadas:** `·` (`info`) va en `rail #262626` sobre `#000000` a **1,39:1**, el peor de los siete. La escalera `· / o / O` es monotona por area en el `.txt` y en el `.svg` el peldanio bajo no esta.
* **Y lo que la ronda tres dejo abierto y sigue abierto:** `Darkside.SPIN = (".", "o", "O", "o")` es la misma coleccion una familia mas alla, y ningun `SPIN` de ningun lenguaje esta censado — ni siquiera despues de que inc67 metiera el conjunto B entero.
* **Veredicto: `keep with a note`.**

#### `darkside_S6` — keep → **`keep`**
* Frame identico. El knockout mejora a 4,56:1 (§0c) y la separacion placa↔cuerpo baja a 4,23:1. Los dos numeros se mueven en direcciones opuestas por el mismo cambio de token, y el que importa para *«el match es un agujero en el color del propio texto»* es el que mejoro.
* **Veredicto: `keep`.**

---

### 2.6 solari

`LEVELS "OK "/DLY/CNX` · `REQUIRED ▮` · `DANGER ▀▄` · `CUR ▼` · `SEAM/FIELD_LEAD ▁`. **Un `.txt`
movido** (inc65). `mut` **exento por nombre** con la aritmetica (`THE_BAND_IS_A_SECOND_GROUND`).

#### `solari_S1` — nota → **`keep with a note`**
* **Objecion previa:** cada tarea gasta dos filas; la costura es doctrina y el coste es la mitad de la superficie.
* **Que cambio:** nada.
* **Objecion nueva, medida:** la costura `▁` va en `seam #1f1f22` sobre `#0b0b0c` a **1,20:1**, y son **2355 celdas: el 79 % de las celdas pintadas de las seis hojas de solari, la proporcion mas alta del corpus.** **Criterio observable:** en `solari_S1.svg`, senialar las costuras. La doctrina dice que la costura es el lenguaje; en el artefacto de registro el lenguaje ocupa cuatro quintas partes de la pagina y no se ve.
* **Veredicto: `keep with a note`.**

#### `solari_S2` — nota → **`keep with a note`**
* **Objecion previa:** `▮` aparece tres veces y dos son la respuesta a *«senala los campos obligatorios»*.
* **Que cambio:** nada. La reserva sigue admitida (§11.5).
* **Nota nueva:** `mut` de solari es **3,65:1** y esta **exento por nombre con la aritmetica** (inc70/inc71: `L ≥ 0,19021` contra el ground, `L ≤ 0,14960` contra la banda; los dos pisos no se solapan). Es la unica exencion de contraste del corpus, esta razonada y esta escrita en `themes.py` y en `spec.md`. La objecion no es a la exencion: es que el cuerpo de esta hoja va a 3,65:1 y eso es un hecho del frame, exento o no.
* **Veredicto: `keep with a note`.**

#### `solari_S3` — keep → **`keep`**
* Frame identico. Sigue siendo el unico switch del corpus legible con todos los glifos borrados.
* **Veredicto: `keep`.**

#### `solari_S4` — nota → **`keep with a note`**, y la nota se reescribe entera por segunda ronda seguida
* **Objecion previa (C3'):** la banda se comia la cabecera `GATE DOING 04` entera y `14 REWRITE THE ONBOARDING` quedaba archivada bajo `GATE BACKLOG 05`. *«Un frame que afirma algo falso es peor que uno que calla.»*
* **Que cambio** (inc65, ruling F amended):

  ```
  f1508ad  f10   (vacia)
  f1508ad  f16   ▁▁▁▁… (costura huerfana)
  f1508ad  f17       14  REWRITE THE ONBOARDING     <- bajo GATE BACKLOG 05

  4089eda  f10  ▼  GATE DOING 04   STATUS  PROJ  PRI
  4089eda  f16  ▁▁▁▁▁▁▁▁▁… (100 celdas, cierre de banda)
  4089eda  f17       14  REWRITE THE ONBOARDING     <- bajo GATE DOING 04
  ```
* **Estado: RESPONDIDA, y la ley lo asegura con la pertenencia leida de `fixture.py` por ruta.** **Criterio observable:** en `solari_S4`, decir a que gate pertenece `REWRITE THE ONBOARDING`. La cabecera mas cercana por encima es `GATE DOING 04`. **Responde bien por primera vez en cuatro rondas**, y la costura huerfana de la fila 16 se convirtio en el cierre de la banda, que es un uso mejor de la misma celda.
* **Objecion nueva 1:** la banda **cierra y no abre**. La fila 16 es una regla de 100 celdas; las filas 11-15 arrancan sin nada por encima salvo la cabecera del gate. **Criterio:** decir donde empieza el modal. Sin respuesta. Es C2 al reves, y es el unico caso del corpus.
* **Objecion nueva 2:** `GATE DOING 04` dice cuatro y ensenia una. Es el coste correcto de una banda y hay que escribirlo; no es una afirmacion falsa, es una truncacion.
* **Objecion nueva 3:** la cabecera de la fila 10 abre con `▼`, que es `CUR`. En `solari_S1` la cabecera de gate no lleva cursor. **Criterio:** decir si el cursor esta sobre el gate o sobre la banda.
* **Veredicto: `keep with a note`.** Duenio: `Solari.band_head`, y lo que queda es la regla de apertura.

#### `solari_S5` — nota → **`keep with a note`**
* Frame identico. El log `OK / DLY / CNX` sigue siendo el mejor de los once por un margen amplio, y **es el unico que sobrevive a §0b**: tres palabras, cero glifos, cero dependencia del contraste de un token de cromo.
* **Objecion previa (la sparkline de dieciseis digitos pierde la tarea):** en pie.
* **Veredicto: `keep with a note`.**

#### `solari_S6` — nota → **`keep with a note`**
* **Objecion previa (C6):** la cabecera recasea la consulta y el estado vacio dice `NO DEPARTURES` para «la busqueda no encontro nada».
* **Que cambio:** nada. C6 sigue en dos lenguajes.
* **Veredicto: `keep with a note`.**

---

### 2.7 blueprint

`LEVELS "  "/╌╌/━━` · `REQUIRED ═` · `DANGER ━━` · `CUR ┌` · `FIELD_LEAD ·─`. Ningun `.txt` movido.
`mut` sin cambio.

#### `blueprint_S1` — nota → **`keep with a note`**
* **Objecion previa (C10):** `blueprint_S1` dice `├ CLEAR ┤` y `S2` dice `├ OVERDUE ┤` sobre el mismo tablero sembrado.
* **Que cambio:** **RULED** (`G vs ruling 10`, §16.1): *«en S4 el mood del fixture es calmo; G vale solo para S2»*. Recordado, sin codigo, y `screens.s4` medido para confirmarlo.
* **Estado: RESUELTA POR RULING.** El frame la honra. Queda la lectura de fondo — un fixture que rinde dos hechos — y es una decision escrita, no un defecto.
* **Nuevo:** `dim #24486b` va a **1,24:1**, 1155 celdas, y la muestra es `┤`: los terminadores de cota, que son la firma del lenguaje.
* **Veredicto: `keep with a note`.**

#### `blueprint_S2` — nota → **`keep with a note`**
* **Objecion previa 1:** `═`, `╞` y `╡` en la misma fila 3, las tres con horizontal doble. **Objecion previa 2:** `Blueprint.ERROR_FILL` pone 50 `╌` (`warn`) extendiendo una fila que abre con `━━` (`error`).
* **Que cambio:** nada en el frame. El `ERROR_FILL` sigue fuera de `PART_GLYPHS` y **sigue fuera del conjunto B**: inc67 metio slider, barra, scrollbar, medidor, spark, pager y mascot; el relleno de un mensaje de error no es ninguno de los siete.
* **Estado: la 1 en pie; la 2 en pie y ahora es la unica superficie grande que ningun instrumento alcanza.**
* **Veredicto: `keep with a note`.**

#### `blueprint_S3` — rework → **`rework`**
* **Objecion previa (K4):** tres horizontales distinguidas por CUENTA DE GUIONES — `╌` (2), `┄` (3), `┈` (4) — a 12 px.
* **Que cambio** (inc68): **K4 esta CERRADA como instrumento.** `state_channel()` compara dos estados de un `part` sobre todas las tablas de los once, con `None` como REFUSAL, y anadio la clausula de orden sobre las dos escaleras aritmeticas del corpus, una de las cuales es exactamente esta. El censo lee ahora `blueprint 2 filas de homoglifo`: `╌ ┄` y `╌ ┈`.
* **Estado: el instrumento existe, lo mide, y el FRAME NO SE MOVIO.** La ley asegura que la escalera **sube**; no asegura que se pueda contar. **Criterio observable, sin cambios:** en `blueprint_S3`, tapar las etiquetas y decir cuales de los cinco switches estan encendidos y cual esta muerto. `├─┤` contra `├┤·` contra `├╎┈` sigue siendo un trazo, un trazo mas corto y un trazo punteado.
* **Y el `.svg` lo agrava:** los tres van en `dim` a **1,24:1**, el segundo peor del corpus. Contar guiones que no se ven no es un canal.
* **Objecion en pie (C9):** la fila 18 dibuja el caption destructivo exactamente como una fila de campo.
* **Veredicto: `rework`.** El eje: **K4 en el frame**. Es el unico `rework` del corpus cuyo instrumento se construyo y cuyo frame no se toco.

#### `blueprint_S4` — nota → **`keep with a note`**
* **Objecion previa:** el asiento destructivo paso de 8 a 12 celdas y nada renderiza `S4` por debajo de 100; el modal se delimita con cuatro esquinas sueltas.
* **Que cambio:** nada. Sigue *«untested rather than safe»* por escrito.
* **Estado: en pie, y es la unica de las 66 que sigue siendo un limite de metodo y no de disenio.**
* **Veredicto: `keep with a note`.**

#### `blueprint_S5` — nota → **`keep with a note`**
* **Objecion previa (L7):** inc60 mando `LEVELS["info"]` al aire; seis de ocho filas del log sin marca.
* **Que cambio:** **RULED como doctrina** (§16.1): *«una escalera de tipo de linea donde la ausencia es el estado calmo»*.
* **Estado: RESUELTA POR RULING, y §0b la reabre por el otro lado.** Medido, siete lenguajes mas dibujan su `info` y lo pintan entre 1,35 y 1,96:1. **La doctrina describe nueve de los once y solo dos la declaran.** Ver §7.7.
* **A favor del frame:** los dos peldanios que blueprint SI dibuja van a 4,65 y 10,60:1. De los nueve que no clasifican por `info`, blueprint es el unico honesto: no dibuja lo que no se va a ver.
* **Veredicto: `keep with a note`.**

#### `blueprint_S6` — keep → **`keep`**
* Frame identico. 2,28:1 mas el peso; `mut` de blueprint no se movio, asi que el numero es exacto.
* **Veredicto: `keep`.**

---

### 2.8 naught

`LEVELS ◦◦/∙◦/∙∙` · `REQUIRED ⊛` · `DANGER ∙∙` · `CUR ●` · `FIELD_LEAD ◦`. **Dos `.txt` movidos**
(inc67, inc68). Exenciones vivas: `DANGER_IS_THE_TOP_RUNG` y `THE_GROUND_IS_NOT_A_MARK` (tasada en
`(7, 2)`).

#### `naught_S1` — nota → **`keep with a note`**
* **Objecion previa (K5):** la barra de 44 % es trece `∙`, `LEVELS[error]` y el `DANGER_FORM` byte a byte; `∙` aparece 70 veces y dos significan severidad. **Segunda:** el pager mezcla `·` (U+00B7), `∙` (U+2219) y `◦`.
* **Que cambio** (inc67, inc68):

  ```
  f1508ad  f13  ◦ ∙∙∙∙∙∙∙∙∙∙∙∙∙ ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦  44%
  4089eda  f13  ◦ ◉◉◉◉◉◉◉◉◉◉◉◉◉ ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦  44%

  f1508ad  f31  view ·●●●●······· 3-10 of 23
  4089eda  f31  view ◦●●●●◦◦◦◦◦◦◦ 3-10 of 23
  ```
* **Estado: las dos RESPONDIDAS en el asiento.** `∙` **70 → 57**; la barra deja de gastar el `DANGER_FORM`; `·` sale del frame (9 → 1) y con el la unica pareja de homoglifo que el censo ya sabia leer.
* **Objecion nueva, y es un traslado:** `◉` es el **checkbox marcado** de `naught_S2` f11 y la perilla del switch de `S3`, y `⊙`/`◉` es uno de los dos pares que L10 nombra como el defecto mas apretado de este kit. La barra dejo el `DANGER_FORM` y aterrizo en la pareja de homoglifo que la ronda tres declaro irresoluble sin raster (E2). **Criterio observable:** en `naught_S1`, decir si las trece celdas de la fila 13 son un porcentaje o trece casillas marcadas.
* **Y lo que no se movio:** quedan **57 `∙`** y dos de ellas (fila 23) son la severidad. Los latigos de tarjeta siguen siendo `∙`. La objecion baja un 19 %, no se cierra.
* **Veredicto: `keep with a note`.**

#### `naught_S2` — rework → **`rework`**
* **Objecion previa (L10):** el radio y el checkbox se distinguen solo por diametro y relleno de un circulo, a dos filas — `⊙` contra `◉`, `○` contra `◦` — y ninguno de los dos pares estaba en la lista fija de cinco de `HOMOGLYPHS`.
* **Que cambio** (inc68): **K2 esta CERRADA como instrumento.** `HOMOGLYPH_FAMILIES` deriva 48 pares en vez de enumerar cinco, y `homoglyph_rows` lee MEANING × MEANING. **El censo lee ahora `naught 12 filas de homoglifo`, de cero.**
* **Estado: MEDIDA POR PRIMERA VEZ, Y EL FRAME NO SE MOVIO.** `naught_S2.txt` es byte a byte el de `f1508ad`. **Criterio observable, sin cambios:** en `naught_S2`, tapar la columna de etiquetas y decir cual de las dos filas de opciones es una eleccion unica y cual son casillas independientes. Sin respuesta.
* **Lo que cambio en el argumento, y hay que decirlo:** la ronda tres tuvo que plantear esta objecion contra un instrumento que no podia verla. Hoy el instrumento la ve, la cuenta y la firma con nombre. **El `rework` deja de ser una opinion y pasa a ser una fila de un roster.**
* **Segunda objecion (el boton muerto abre con `⋅`, el papel del campo invalido):** **RESPONDIDA por inc71.** La runa del campo es cromo por definicion compartida; `⋅` deja de llevar la familia `invalid` y el censo de naught baja de 4 a 3 celdas colisionantes. La discrepancia de tres lotes esta cerrada en una funcion que los dos ficheros importan.
* **Veredicto: `rework`.** El eje: **L10**, y ahora con su medicion.

#### `naught_S3` — nota → **`keep with a note`**
* **Objecion previa (K5):** la parte viva del slider son nueve `∙`, el `DANGER_FORM` byte a byte, cuatro filas encima de `◦ ∙Delete all∙ ◦`.
* **Que cambio:** **nada en el frame.** `naught_S3.txt` no se movio. Lo que cambio es el alcance: la ruling **A amended** metio el slider en el conjunto B, y el censo confirma que `∙ [5 families]` incluye `slider.indicator mark (active,default,edited,focused)`. La fila esta en `FILL_IS_NOT_A_MEANING["naught"] = 3`.
* **Estado: cambio de clase, no de frame.** De *«fuera de todo instrumento por peticion del operador»* a *«dentro de un instrumento, en un roster de dieciseis filas, con duenio, sin arreglar»*. **El criterio observable no se movio una celda:** tapar las palabras y decir cual de las dos tiradas de `∙` es un valor y cual un boton irreversible.
* **Segunda (C9, el caption pegado a su etiqueta):** en pie.
* **Veredicto: `keep with a note`.** Se mantiene la etiqueta porque el frame honra la ruling A tal como la ruling A quedo redactada, y porque el eje ahora tiene duenio escrito.

#### `naught_S4` — rework → **`rework`**
* **Objecion previa:** `∙` aparece **237 veces** y dos significan «esto destruye datos». Las otras 235 son las dos reglas de 100 celdas con las que la banda se delimita, y el tablero de detras.
* **Que cambio:** **el pager, y nada mas.** `∙` **237 → 237**, medido. Las filas 13 y 20 siguen siendo `∙∙∙∙∙…` a 100 celdas.
* **Estado: EN PIE, INTACTA, y es la unica objecion de `rework` de la ronda tres que ningun incremento de los nueve toco ni nombro.** No aparece en §16.6, ni en §17.6, ni en §18.5.
* **Criterio observable, sin cambios:** en `naught_S4`, senialar las celdas que significan «irreversible». 237 candidatas, dos correctas, y las 200 mas grandes y contiguas de la pantalla son el marco del modal.
* **Lo unico que se movio, y es a favor:** el pager pasa de `·●●●●·······` a `◦●●●●◦◦◦◦◦◦◦`, con lo que `·` sale del frame. A cambio, el pager queda dibujado en las dos celdas mas cargadas del lenguaje: `◦ [13 families]` y `● [9 families]`.
* **Veredicto: `rework`.** El eje: el `DANGER_FORM` del lenguaje es su propio marco de modal, en la unica pantalla donde hay que reconocerlo.

#### `naught_S5` — nota → **`keep with a note`**
* **Objecion previa:** el peldanio `info` es `◦◦`, la celda del suelo, dibujada 99 veces en la fila 3 de esta misma pantalla.
* **Que cambio:** nada. **Y §0b la confirma por el otro camino:** `◦◦` va en `dim #242424` sobre `#000000` a **1,35:1**, el segundo peor de los once. La objecion de la ronda tres (*«la evidencia es que estan en la columna de severidad, no la marca»*) se refuerza con un numero.
* **Segunda (la sparkline en braille en un lenguaje de circulos):** en pie, y sigue siendo el gemelo invertido de `prism_S5`.
* **Veredicto: `keep with a note`.**

#### `naught_S6` — nota → **`keep with a note`**
* **Objecion previa:** el separador de la barra de teclas es `∙`, el `DANGER_FORM`, cuatro veces.
* **Que cambio:** nada.
* **Estado: en pie.** El tier de match (`bold {ink}`, 3,17:1) tampoco se movio: `mut` de naught no era de los cuatro que inc70 subio, asi que es el unico kit `bold` cuyo numero de la ronda tres sigue exacto.
* **Veredicto: `keep with a note`.**

---

### 2.9 corgi

`LEVELS ▁▁/▄▄/██` · `REQUIRED ▀` · `DANGER ██` · `CUR ▐` · `FIELD_LEAD ""`. **Tres `.txt` movidos**
(inc67). `mut` sin cambio.

#### `corgi_S1` — rework → **`keep with a note`**
* **Objecion previa (K5):** **`█` aparece 47 veces y ninguna significa peligro ni error.** 25 son el tabique `Corgi.PANE_RULE`, 18 el mascot, una la pagina del pager. *«El eje incumplido es una constante, y gasta la marca mas fuerte del lenguaje 25 veces en la pantalla que el usuario mira mas tiempo.»*
* **Que cambio** (inc67):

  ```
  f1508ad  f04-f30   █ [D] D E T A I L          (tabique, 25 celdas)
  4089eda  f04-f30   ▓ [D] D E T A I L
  f1508ad  f18-f23   ██  ██ / █ █ / ██████      (mascot, 18 celdas)
  4089eda  f18-f23   ▓▓  ▓▓ / ▓ ▓ / ▓▓▓▓▓▓
  ```
* **Estado: RESPONDIDA.** `█` **47 → 2**. **Criterio observable:** en `corgi_S1`, senialar las celdas que significan «irreversible». **Dos candidatas**, cero correctas, contra cuarenta y siete. El tabique y el mascot son metal fresado y no el peldanio de error.
* **Objecion nueva 1, y es un traslado:** `▓` **0 → 45**, y `▓▓` es el **checkbox marcado** de `corgi_S2` f11 (`▓▓ ON ui`) y la pista encendida del switch de `S3`. El tabique de 25 celdas esta hoy dibujado con la marca de «esta casilla esta marcada». Es mas benigno que el `DANGER_FORM` y es la misma clase de movimiento que naught hizo con `◉`.
* **Objecion nueva 2, y es la que el packet no cuenta:** **las dos `█` que quedan son la pagina actual del pager**, fila 31, `view ██ ░░ ░░ ░░`. §17.7 escribe que *«el pager nunca fue un widget aparte … toda K5 para ese widget era una tupla en un fichero»* y arreglo el de prism. **El de corgi no se movio.** La marca mas fuerte del lenguaje sigue diciendo «estas en la pagina uno».
* **Tercera, en pie:** el medidor de la fila 13 sigue lleno con `▄▄` (`warn`) y vacio con `░░` (la pared del campo invalido). `FILL_IS_NOT_A_MEANING["corgi"] = 6`, el mas alto del roster.
* **Veredicto: `keep with a note`.** El eje del `rework` esta cerrado; lo que queda esta rostrado y tiene duenio.

#### `corgi_S2` — nota → **`keep with a note`**
* **Objecion previa:** la fila 9 (`▒◦ low  ▒◦ norm  ▒● high`) esta en un **tercer registro que nadie declaro** — corgi no tiene circulos.
* **Que cambio:** **nada.** inc67 declaro el registro de las cantidades y no toco el radio.
* **Estado: en pie, entera, y ahora con una razon medida para molestar mas:** `● ◦` es el alfabeto entero de naught, y el censo de naught lee `● [9 families]`.
* **Segunda:** RESPONDIDA por inc71 — las paredes del `Save` muerto son `·`, la runa del campo invalido, y la runa es cromo por definicion compartida. corgi baja de 5 a 4 celdas colisionantes y de 1 a 0 filas de homoglifo.
* **Veredicto: `keep with a note`.**

#### `corgi_S3` — nota → **`keep with a note`**
* **Objecion previa (K5):** el eje del slider es `▄▄` y `▁▁`, los peldanios `warn` e `info`, cuatro filas encima de `█Delete all█`.
* **Que cambio:** **nada.** `corgi_S3.txt` no se movio; la fila 16 sigue siendo `row density  ▄▄ ▄▄ ▄▄ ▙▟ ▁▁[70]`.
* **Estado: cambio de clase.** La ruling **A amended** metio el slider en el conjunto B y el censo lo firma: `▄ [4 families]` y `▁ [3 families]`, las dos con `slider.indicator` y `slider.main` listadas por nombre. Seis de las dieciseis filas de `FILL_IS_NOT_A_MEANING` son de corgi. **El criterio observable no se movio:** tapar el `[70]` y decir si la fila 16 es un valor o cinco calificaciones de severidad.
* **Veredicto: `keep with a note`.**

#### `corgi_S4` — rework → **`keep with a note`**
* **Objecion previa (C8):** **es el unico de los once cuyo `S4` pierde la fila 1.** Borra el masthead, la regla, el tablero, el panel de detalle, el pager y el propio marco del modal. `corgi_S4.svg` tenia **siete** runs de texto. *«Con `corgi_S4` delante, decir en que modo esta la aplicacion y de que gate se borra.»*
* **Que cambio** (inc65): la exencion `MODAL_KEEPS_NOTHING` paso a `MODAL_KEEPS_ONLY_THE_HEAD` y `Corgi.overlay_instead` conserva `under[0]`.

  ```
  f1508ad  f01  (vacia)
  4089eda  f01  [1]B O A R D [2]FORM [3]CFG [4]LOG
  ```
  `corgi_S4.svg`: **7 → 14** runs de texto.
* **Estado: los dos criterios que la ronda tres escribio RESPONDEN.** *«En que modo esta la aplicacion»* → la tira de modos, fila 1. *«De que gate se borra»* → `3 tasks will be removed from BACKLOG`, fila 16.
* **Lo que queda, y es una objecion a la ruling y no al frame (§7.4):** **treinta de las treinta y dos filas siguen en blanco**, y la banda no tiene ni abridor ni cierre ni caja. **Criterio observable:** decir donde empieza y donde acaba el modal. Sin respuesta, en el unico lenguaje del corpus que no dibuja ningun limite. Es C2 en su forma mas pura, y a `swiss_S4` y a `ledger_S4` se les cuenta como `rework`.
* **Segunda, en pie:** `▛▛ █Delete█ ▜▜` — el anillo de foco del boton irreversible es el par de paredes del campo de texto normal de `S2`.
* **Veredicto: `keep with a note`.** La etiqueta baja porque los dos criterios escritos responden y porque el alcance esta ruled por escrito; el desacuerdo va a §7.

#### `corgi_S5` — nota → **`keep with a note`**
* **Objecion previa (L6):** la sparkline usa `▄` y `█`, seis filas encima del log que los usa como severidad.
* **Que cambio:** nada en el frame; **L6 contada por primera vez** (inc67).
* **Objecion nueva (§0b):** `▁▁` (`info`) va a **1,71:1**. La escalera `▁▁ / ▄▄ / ██` que la ronda tres llamo *«la mejor del corpus con el color quitado»* lo sigue siendo en el `.txt` y pierde su peldanio bajo en el `.svg`.
* **Veredicto: `keep with a note`.**

#### `corgi_S6` — nota → **`keep with a note`**
* **Objecion previa:** el mascot del estado vacio esta dibujado con **18 `█`**, la marca de destruccion, debajo de un campo de busqueda que no encontro nada.
* **Que cambio** (inc67): `█` **18 → 0**; el mascot es `▓`.
* **Estado: RESPONDIDA.** **Criterio observable:** senialar las celdas que significan «irreversible» en `corgi_S6`. **Cero candidatas**, contra dieciocho.
* **Objecion nueva:** el mascot esta ahora en `▓`, el checkbox marcado y la pista encendida del switch. En esta pantalla no hay ninguno de los dos, asi que es el caso mas benigno del traslado.
* **Veredicto: `keep with a note`.**

---

### 2.10 prism

`LEVELS ⣀⣀/⣤⣤/⣿⣿` · `REQUIRED ⡀` · `DANGER ⣿⣿` · `CUR ▸` · `FIELD_LEAD ⡀⡤⣶`. **Cuatro `.txt`
movidos** (inc64, inc67). `mut` sin cambio.

#### `prism_S1` — rework → **`keep with a note`**
* **Objecion previa (L9):** **la barra de progreso va al reves.** Doce `⣀` (la celda mas ligera) seguidos de quince `⣿` (la mas pesada), etiquetados `44%`: la lectura que da el frame es 56 %. Y prism se contradice: `S3` y `S5` llenan por lo pesado.
* **Que cambio** (inc64, inc67):

  ```
  f1508ad  f13  ⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  44%
  4089eda  f13  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀  44%

  f1508ad  f31  view ⠒⣿⣿⣿⣿⠒⠒⠒⠒⠒⠒⠒ 3-10 of 23
  4089eda  f31  view ⠒⠿⠿⠿⠿⠒⠒⠒⠒⠒⠒⠒ 3-10 of 23
  ```
* **Estado: RESPONDIDA, y con ley.** *«La direccion de llenado de un lenguaje es una declaracion»* (L9, inc64) se rinde al piso y al techo de medidor, slider y readbar de los once, con dos saltos escritos (`RAMPLESS_METERS`: solari y blueprint) y la ley **asertando que siguen sin ser pesables** para que un tercero salga en rojo. **Criterio observable:** en la fila 13, tapar `44%` y decir que fraccion esta hecha. Doce de veintisiete. Correcto.
* **Y el pager sale de la brasa:** `⣿` **31 → 24**.
* **Objecion nueva:** las doce celdas de relleno son `⣿`, que sigue siendo `DANGER_FORM` y `LEVELS[error]` byte a byte. inc67 le concedio al medidor una **exencion por nombre** (*«el medidor ES el device de severidad»*, dos lenguajes) y se la **nego al slider y al pager** de prism porque `prism_S3` la refutaba. **Criterio:** en `prism_S1`, senialar las celdas que significan «esto destruye datos». 24 candidatas, cero correctas. Era 31 y cero.
* **Segunda, sin tocar:** el guia de campo `⡀⡤⣶` **abre con `⡀`, que es `REQUIRED`**, en seis filas de detalle de solo lectura. La exencion existe por nombre desde inc59 y el propio packet escribio que *«the frame does not bear it out»*. Cuarta ronda.
* **Veredicto: `keep with a note`.**

#### `prism_S2` — rework → **`keep with a note`**
* **Objecion previa (L8):** **el checkbox esta invertido.** El fixture marca `ui` y `urgent`; el frame las dibujaba con el pozo vacio (`⠿⠀⠿`) y `api`, sin marcar, con una marca dentro (`⠿⠉⠿`).
* **Que cambio** (inc64):

  ```
  f1508ad  f11  tags  ⠿⠉⠿ api  ⠿⠀⠿ ui  ⠿⠀⠿ urgent
  4089eda  f11  tags  ⠿⠀⠿ api  ⠿⠉⠿ ui  ⠿⠉⠿ urgent
  ```
* **Estado: RESPONDIDA, y con ley.** *«Una casilla marcada nunca es mas ligera que una vacia»* (L8, inc64), medida sobre la CAJA y no sobre el control, con `>=` porque naught marca por forma a igual peso. **Criterio observable:** en la fila 11, senialar los tags marcados. Todo lector senialara `ui` y `urgent`. Correcto.
* **Objecion nueva, y la crea el arreglo:** `⠉` es ahora **la marca del checkbox marcado** (f11) **y** el relleno del radio SIN elegir (f9: `⠉⠉⠉ low  ⠉⠉⠉ norm`) **y** el papel del campo normal (f4). Tres roles, dos filas de distancia. **Criterio observable:** en `prism_S2`, tapar las palabras y decir si `⠉` significa «elegido» o «no elegido». Depende de si esta dentro de `⠿…⠿` o repetido tres veces.
* **Segunda, sin tocar:** el papel del campo invalido sigue siendo `⠀`, el blanco braille — el campo de fecha no tiene fondo visible y sus dos paredes, `⣹` y `⣏`, son imagenes espejo. Es la forma `] … [` que la ronda uno le hizo rehacer a nord.
* **Y K4 esta cerrada como instrumento:** `state_channel()` deja a prism **fuera** de las dos lenguas con filas (naught 8, darkside 1). La inversion que ninguna ley podia ver hoy tiene ley.
* **Veredicto: `keep with a note`.**

#### `prism_S3` — nota → **`keep with a note`**
* **Objecion previa (K5):** nueve `⣿` en el slider, `DANGER_FORM` y `LEVELS[error]`, cuatro filas encima de `⣿Delete all⣿`.
* **Que cambio** (inc67):

  ```
  f1508ad  f16  row density  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70
  4089eda  f16  row density  ⠿⠿⠿⠿⠿⠿⠿⠿⠿⢸⠉⠉⠉⠉ 70
  ```
* **Estado: RESPONDIDA, y es el mejor arreglo de los nueve incrementos.** `⣿` **11 → 2**, y las dos son `⣿Delete all⣿`. **Criterio observable:** tapar las palabras y decir cual de las dos tiradas de `⣿` es un valor y cual un boton irreversible. **Solo hay una, y es el boton.**
* **Objecion nueva:** el slider toma sus dos celdas del toggle, y el destructivo de la fila 20 es `⠿⠉⣿Delete all⣿⠉⠿`: **las dos celdas del slider son las dos paredes del boton irreversible, cuatro filas mas abajo.** Sigue habiendo respuesta (la brasa de dentro), asi que el criterio pasa; se registra porque es el tercer traslado de la ronda.
* **Segunda, sin tocar (C9):** el caption del destructivo abre con `⡀⡤⣶`, el guia que empieza en `REQUIRED`.
* **Veredicto: `keep with a note`.**

#### `prism_S4` — nota → **`keep with a note`**
* **Objecion previa:** `⣿` aparece 18 veces; dos son la respuesta destructiva y ocho el mascot del estado vacio, tres filas por debajo del modal.
* **Que cambio** (inc67): el pager, `⣿⣿⣿⣿` → `⠿⠿⠿⠿`. `⣿` **18 → 14**.
* **Estado: mejora del 22 %, objecion en pie.** El mascot no se movio y sigue estando en pantalla al mismo tiempo que el confirm.
* **A favor, sin cambios:** el tablero de detras esta entero, el modal esta cerrado por sus cuatro lados y las dos respuestas se distinguen por la brasa y por las paredes. Sigue siendo la mejor superposicion de los cuatro lenguajes tardios.
* **Veredicto: `keep with a note`.**

#### `prism_S5` — nota → **`keep with a note`**
* **Objecion previa:** la sparkline esta dibujada con elementos de bloque en un lenguaje cuyo alfabeto entero es braille.
* **Que cambio:** nada.
* **A favor, y §0b lo confirma:** **prism es el unico de los once que pinta su peldanio `info` por encima de 3:1** (`⣀⣀`, 3,25:1). La escalera es monotona por cuenta de puntos braille (2, 4, 8), por area y por contraste, y es la unica que sobrevive entera a la medicion de esta ronda.
* **Veredicto: `keep with a note`.**

#### `prism_S6` — nota → **`keep with a note`**
* **Objecion previa:** **1,58:1**, el segundo peor del corpus; y `#2dd4bf` es la tinta del cursor `▸` de la misma fila y el acento de match de instrument.
* **Que cambio:** nada; `mut` de prism no se movio, asi que 1,58 sigue exacto. **Deja de ser el segundo peor** porque nord cayo a 1,38 (§0c): prism es hoy el tercero.
* **Veredicto: `keep with a note`.**

---

### 2.11 ledger

`LEVELS "  "/"* "/"**"` · `REQUIRED †` · `DANGER ( )` · `CUR ▶` · `FIELD_LEAD ·`. **Un `.txt`
movido** (inc66). **`mut` `#6b6558` → `#6a6458`** (inc70). El unico kit de papel claro.

#### `ledger_S1` — nota → **`keep with a note`**
* **Objecion previa:** los dos paneles se tocan con tres `═` en la fila 4, y `═` es en todas partes la regla bajo una cabecera de gate. **Tercera (E4):** *«nada de lo anterior es visible en el artefacto»*.
* **Que cambio** (inc63): el lienzo pinta `#e9e1cf`.
* **Estado: E4 RESPONDIDA.** **Criterio observable de §0a de la ronda tres:** abrir `ledger_S1.svg` y decir que tarea esta en `DOING`. **Responde**, `#1c1a15` a 13,36:1. La objecion del `═` vuelve a ser mirable y **sigue en pie**: nada se movio en el `.txt`.
* **Objecion nueva, y es el reverso exacto de E4:** `dim #c4b99f` es hoy **1,50:1** (era 9,62 contra el fondo falso) y pinta, ademas de los guias, **`· form`, `· cfg` y `· log` — las tres etiquetas de modo inactivas de la fila 1** — y el `low` de la tabla de detalle. **Criterio observable:** abrir `ledger_S1.svg` y nombrar los cuatro modos. Responde uno.
* **Tercera, medida:** `rule #8a8272` es **2,92:1** y son **1619 celdas**: la reticula de columnas entera de la pagina de libro mayor esta por debajo del piso de 3:1. Sobre las filas cebra (`#e0d7c2`) baja a 2,66.
* **Veredicto: `keep with a note`.**

#### `ledger_S2` — nota → **`keep with a note`**
* **Objecion previa:** **`†` y `‡` estan en la fila 6, a tres celdas, y son el mismo dibujo con un travesanio mas.** El roster de homoglifos leia **cero** para ledger.
* **Que cambio** (inc68): **K2 cerrada como instrumento.** `HOMOGLYPH_FAMILIES` deriva la pareja y `homoglyph_rows` lee meaning × meaning. El censo dice hoy: `LEDGER 1 row(s) — † is required and its homoglyph ‡ is invalid MEANING`. §17.4 lo llama *«la mas apretada del corpus, invisible hasta inc68»*.
* **Estado: MEDIDA. El frame no se movio.** **Criterio observable, sin cambios:** tapar las palabras y decir cual de las tres marcas de referencia dice «obligatorio», cual «rechazado» y cual «error». Y **E2 sigue diciendo que no se puede resolver desde el artefacto**, porque el `.svg` no lleva metrica de fuente.
* **Segunda, en pie:** el campo enfocado abre con `▶` (`CUR`) y cierra con `│`, la regla de columna.
* **Veredicto: `keep with a note`.**

#### `ledger_S3` — nota → **`keep with a note`**
* **Objecion previa (C9):** la fila 19 dibuja el caption destructivo byte a byte como una fila de campo.
* **Que cambio:** nada. C9 sigue sin tocar en tres lenguajes.
* **Segunda, en pie:** el switch deshabilitado y el apagado dicen la misma palabra (`open`).
* **Veredicto: `keep with a note`.**

#### `ledger_S4` — rework → **`rework`**
* **Objecion previa (C2):** **el modal abre con una regla de 100 celdas y no cierra, y la respuesta destructiva esta en la ultima fila de la pantalla.** *«Debajo de `(Delete)` no hay nada, ni un pager ni una costura, asi que el limite inferior del modal es el borde de la terminal.»* **Segunda:** las paredes de `(Delete)` no son un par — abre con el cursor y cierra con la regla de columna.
* **Que cambio** (inc66): **la segunda, y solo la segunda.**

  ```
  f1508ad  f32  ▶  (Delete)  │   │   Cancel   │
  4089eda  f32  ▶  (Delete)  ◀   │   Cancel   │
  ```
  Y `button.main` ACTIVE pasa de `▶  ◀` a `▶──◀`, con `─` elegido por medicion (no lleva ninguna familia) sobre `·`, que habria subido una fila de seis a siete familias.
* **Estado: la segunda RESPONDIDA** — `▶ … ◀` es un par declarado (`WALL_MIRRORS`, derivado de los once) y la ley lo asegura a tres anchos. `◀` aparece **una sola vez en los 66 frames** y no colisiona con nada. **La primera SIGUE EN PIE, entera, cuarta ronda.** La fila 26 abre con 100 `─` y la 32 es la ultima fila del terminal.
* **Y es lo mas duro de la ronda:** **`swiss_S4` tenia exactamente la misma objecion y se cerro en el MISMO incremento.** inc66 le anadio a `Swiss.overlay_instead` una segunda regla; `Ledger.overlay_instead` no se toco. La ronda tres habia escrito que la de ledger era **la peor de las dos** (*«con un agravante que swiss no tiene»*). Se arreglo la benigna. Ver §7.5.
* **Tercera, en pie:** las filas 27-32 arrancan en la columna 1 y las 1-25 en la 3.
* **Criterio observable, sin cambios:** decir donde termina el modal. Sin respuesta, y el control irreversible esta pegado al borde.
* **Veredicto: `rework`.** El eje: **C2**, y hoy es el unico del corpus.

#### `ledger_S5` — nota → **`keep with a note`**
* **Objecion previa (L7):** el peldanio `info` es aire.
* **Que cambio:** **RULED como doctrina** (§16.1), y esta es la declaracion que inc60 uso como precedente para blueprint. La ronda tres objeto que *«un precedente tomado de un frame sin juzgar no es un precedente»* (§7.5).
* **Estado: la ruling la cierra como decision, y §0b cambia el argumento a favor de la ruling.** Medido, siete lenguajes mas ya tienen el `info` invisible sin declararlo; ledger y blueprint son los dos unicos que lo dicen. **El precedente era debil por su procedencia y resulta correcto por su contenido.** Se registra la reversion de la objecion.
* **Segunda, en pie:** la sparkline tiene el suelo en `▫` (la pista del switch deshabilitado de `S3`) y el pico en `▪` (la pestania activa, la perilla del slider y el relleno del medidor).
* **Veredicto: `keep with a note`.**

#### `ledger_S6` — rework → **`keep with a note`**
* **Objecion previa (E4):** **el compromiso declarado de esta pantalla no es verificable en el unico tier que puede llevarlo.** `#1c1a15` sobre `#121212` es **1,08:1**.
* **Que cambio** (inc63): `<rect ... fill="#121212"/>` → `<rect ... fill="#e9e1cf"/>`, en los 66.
* **Estado: RESPONDIDA, y la correccion fue exactamente la linea que la ronda tres describio.** **Criterio observable, el mismo:** abrir `ledger_S6.svg` y circular las seis coincidencias de `re`. Seis runs `#1c1a15` subrayados a **13,36:1**. Responde.
* **Y la auditoria fue mas ancha que la objecion:** §16.7 mide que el exportador estaba mal **en los once** y que la galeria estaba bien, porque `set_theme` corre antes del primer pintado. La ronda tres reporto ledger porque ledger es el unico kit cuyo ground esta lo bastante lejos de `#121212` para que el ojo lo cace.
* **Lo que queda:** el tier de match cae de 3,00 a **2,96:1** por el `mut` de inc70 (§0c), y `dim` a 1,50 (§2.11 `S1`). Y **C6 sin tocar**: la fila 16 dice `nil balance` para «la busqueda no encontro nada», el mismo texto que `S1` usa para «este gate no tiene tareas».
* **Veredicto: `keep with a note`.**

---

## 3. Que se movio, en numeros

| | ronda 1 | ronda 2 | ronda 3 | ronda 4 |
|---|---|---|---|---|
| frames juzgados | 42 | 42 | 66 | **66** |
| `keep` | 6 | 14 | 15 | **11** |
| `keep with a note` | 17 | 21 | 40 | **51** |
| `rework` | 19 | 7 | 11 | **4** |
| frames con `.txt` movido desde la ronda anterior | — | 26 de 42 | 27 de 66 | **13 de 66** |
| frames con `.svg` movido | — | — | 27 | **66** |
| celdas colisionantes (censo) | 54 | 48 | 25 | **30** |
| filas de homoglifo | — | 4 | 1 | **26** |
| pares de homoglifo leidos | — | 5 | 5 | **48** |
| `MEANING_AT_AN_OPENER` / `MEANING_AT_A_NAMED_SEAT` | — | 78 / 56 | 0 / 0 | **0 / 0** |
| `FILL_IS_NOT_A_MEANING` (roster nuevo) | — | — | — | **16 filas, 6 lenguajes** |
| `state_channel` (roster nuevo) | — | — | — | **9 filas, 2 lenguajes** |
| lenguajes cuyo `.svg` pinta el ground declarado | — | 0 de 7 | 0 de 11 | **11 de 11** |
| lenguajes cuyo `ink` y `mut` cruzan 4,5:1 | — | — | — | **10 de 11** (solari exenta) |
| lenguajes cuyo `dim` cruza 3:1 | — | — | — | **1 de 11** (prism) |
| lenguajes cuyo peldanio `info` cruza 3:1 o es doctrina | — | — | — | **4 de 11** |

**El censo sube de 25 a 30 y las filas de homoglifo de 1 a 26, y ni un kit empeoro.** Los dos saltos
son el instrumento aprendiendo a mirar: +9 por el conjunto B (inc67), +25 filas por la tabla derivada
(inc68), −5 y −4 por la runa (inc71). §17.4 y §18.3 lo desglosan celda a celda y esta ronda lo
confirma contra `collision_census.txt` en disco.

**Los cuatro `rework` que quedan son cuatro cosas, y las cuatro son un incremento de un fichero:**

1. **Una composicion que abre y no cierra** — `ledger_S4`, y el arreglo es el que inc66 le hizo a swiss.
2. **Un marco de modal dibujado con el `DANGER_FORM`** — `naught_S4`, 200 celdas, sin tocar en nueve incrementos.
3. **Un par sin canal** — `naught_S2`, hoy con doce filas de censo que lo firman.
4. **Una escalera de tres cuentas de guion a 1,24:1** — `blueprint_S3`, con instrumento y sin frame.

---

## 4. Donde empeoro la objecion, aunque la etiqueta no

Cuatro etiquetas retrocedieron (§1) y son las cuatro de §0b. Aparte de esas, **ocho objeciones se
pusieron peores bajo una etiqueta que no se movio**, y hay que separarlas en dos clases porque no son
lo mismo.

**Empeoro el frame — dos, y las dos las causo un incremento de estos lotes:**

1. **`nord_S6`** (nota → nota). inc70 subio `mut` para cruzar 4,5:1 contra el ground y **el salto del match cayo de 1,79:1 a 1,38:1**. nord pasa de ser la linea base del tier de estilo al segundo peor del corpus. Es la peor regresion de la ronda y ninguna ley la vio, porque inc70 asertar `contrast(mut, ground)` y el numero que se rompio es `contrast(accent, mut)`.

2. **`swiss_S2`** (rework → nota). L2 se cerro anadiendo `╎` al `Save` muerto, que es correcto y estaba pedido desde la ronda uno. **A cambio, la pantalla tiene ahora seis verticales** — `┃ ║ │ ╵ ╎ ▏` — y la nueva es la que hay que distinguir de `│` a 12 px. La etiqueta subio y el vocabulario de paredes empeoro.

**Empeoro la medicion y no el frame — seis, y es la clase buena:**

3. **`instrument_S3`** (nota → nota). `⣿` paso de 3 familias a **7** en el censo, porque inc67 metio el conjunto B. El frame no se movio; el instrumento aprendio a verlo.

4. **`naught_S2`** (rework → rework). El censo pasa de cero a **doce filas de homoglifo** para naught. La objecion que la ronda tres tuvo que plantear contra un instrumento ciego hoy es una fila con nombre.

5. **`ledger_S2`** (nota → nota). `† / ‡` pasa de invisible a **una fila del censo**, y §17.4 la llama la mas apretada del corpus.

6. **`blueprint_S3`** (rework → rework). `╌ ┄ ┈` pasa de cero a **dos filas**, con la clausula de orden que asegura que la escalera sube.

7. **`darkside_S1`** (nota → nota). La objecion de la ronda tres a la **ruling E** —*«ascender el `.svg` presupone un exportador fiel y no lo es»*— esta respondida por inc63, y la auditoria que la responde mide que en el artefacto de registro `rail` esta a **1,39:1** sobre 899 celdas.

8. **`industrial_S2`** (nota → nota). inc71 revelo que `/` lleva dos roles, y esta ronda mide que **el segundo no se dibuja en ninguno de los 66** y que la colision que si se ve es otra: los separadores del propio valor contra el papel que los sigue.

**Y hay tres traslados, que no son ni una cosa ni la otra.** Tres arreglos de K5 sacaron un
`DANGER_FORM` de un widget de cantidad y lo pusieron sobre una marca de control:

| frame | de | a | lo que `a` significa en el mismo lenguaje |
|---|---|---|---|
| `naught_S1` f13 | `∙` (13 celdas) | `◉` | checkbox marcado, perilla del switch, mitad del par L10 |
| `corgi_S1` f4-30, f18-23 | `█` (43 celdas) | `▓` | checkbox marcado, pista encendida del switch |
| `corgi_S6` f16-21 | `█` (18 celdas) | `▓` | idem |

Los tres son mejoras netas: `checkbox marcado` es una familia mas baja que `DANGER_FORM` y las
pantallas donde aterriza no dibujan casillas. Se registran porque **la ley que los guio dice que una
celda de relleno no puede ser una marca de `LEVELS`/`DANGER_FORM`/`REQUIRED`, y no dice nada de que
no pueda ser la marca de un control.** Un cuarto traslado del mismo tipo empezaria a ser un patron.

---

## 5. Las objeciones en pie, por quien las arregla

### `Kit` y los tests

| # | objecion | estado | evidencia |
|---|---|---|---|
| K1 | La ley del asiento nombrado nunca miraba `switch.knob`. | **CERRADA** (inc49) | `darkside_S3` |
| K2 | Las leyes comparan code points; `HOMOGLYPHS` es una lista fija de cinco pares. | **CERRADA COMO INSTRUMENTO** (inc68): 48 pares derivados, meaning × meaning. **26 filas en pie**, y ningun frame se movio por ellas | `naught_S2` (12), `darkside_S2` (8), `blueprint_S3` (2), `ledger_S2` (1) |
| K3 | El stepper no tenia ley. | **CERRADA** (inc51) — y **ningun artefacto del repo dibuja un stepper**, cuarta ronda | `spec.md` §12.5 |
| K4 | Ninguna ley compara dos estados de un mismo `part`. | **CERRADA COMO INSTRUMENTO** (inc68, `state_channel()` + clausula de orden). **9 filas en pie**, dos lenguajes | `naught` 8, `darkside` 1 |
| K5 | Ninguna ley ni instrumento lee un widget de CANTIDAD. | **CERRADA COMO INSTRUMENTO** (inc67, ruling A amended). **16 filas en pie** en `FILL_IS_NOT_A_MEANING`; **cuatro de las ocho filas de §0b de la ronda tres siguen exactas** | `naught_S3`, `corgi_S1` (pager), `corgi_S3`, `corgi_S1` (medidor) |
| **K6** | **NUEVA. Ninguna ley lee el fondo que hay REALMENTE debajo de un run.** inc70 asertar `ink` y `mut` contra `THEMES[lang]["ground"]`. Cinco kits pintan un segundo ground y contra el los numeros caen por debajo del piso que la ley acaba de asertar. | **NUEVA Y ABIERTA** | ledger `mut` 4,51 → **4,10** sobre `#e0d7c2`; industrial `mut` 5,38 → **4,20** sobre `#2e2e2e`; industrial `focus` **1,28**; ledger `rule` 2,92 → 2,66 |
| **K7** | **NUEVA. Ninguna ley lee `dim` ni `alert`.** `dim`/`seam`/`rail` esta bajo 3:1 en los once y bajo 1,6:1 en cinco, y es mas de la mitad de las celdas pintadas en seis hojas. `alert` esta bajo 4,5:1 en cinco. | **NUEVA Y ABIERTA.** inc70 midio `dim` en un roster y declino accionar | §0a; nord `alert` 3,05 · corgi 3,99 · naught 4,05 · swiss 4,07 |

### Nivel lenguaje (una declaracion de un kit)

| # | objecion | estado | frame |
|---|---|---|---|
| L1 | Las paredes del invalido son las del normal. | **CERRADA** (inc52) | `instrument_S2` |
| L2 | El boton deshabilitado es aire. | **CERRADA** (inc69, ruling L2, sobre 110 asientos a tres anchos) | `swiss_S2` |
| L3 | `├` era `REQUIRED` y todo terminador. | **CERRADA** (inc60) | `blueprint_S2` |
| L4 | Tres vocabularios de pared en una pantalla. | **ABIERTA, y ahora en dos lenguajes**: swiss llego a seis verticales al cerrar L2 | `nord_S2`, **`swiss_S2`** |
| L5 | El cursor y el `DISCLOSE` son el mismo triangulo girado. | **RESPONDIDA POR RULING** (D-addendum) | `industrial_S1` |
| L6 | La sparkline se dibuja con los peldanios altos de `LEVELS`. | **ABIERTA, y CONTADA por primera vez** (5 de las 16 filas de `FILL_IS_NOT_A_MEANING`, tres lenguajes) | `swiss_S5`, `blueprint_S5`, `corgi_S5` |
| L7 | `LEVELS["info"]` es aire en dos lenguajes. | **RULED como doctrina** — y **reabierta por medicion**: en siete lenguajes mas se dibuja y se pinta a 1,35–1,96:1 (§0b) | los once |
| L8 | El checkbox de prism esta invertido. | **CERRADA** (inc64, ley sobre la CAJA) | `prism_S2` |
| L9 | La barra de prism se llena por lo ligero. | **CERRADA** (inc64, ley de direccion con dos saltos escritos) | `prism_S1` |
| L10 | El radio y el checkbox de naught se distinguen solo por diametro. | **ABIERTA, y MEDIDA**: 12 filas de homoglifo, 8 de `state_channel` | `naught_S2` |
| **L11** | **NUEVA. El match tier de tres kits se estrecho al subir `mut`.** nord 1,79 → 1,38; instrument 2,45 → 2,32; ledger 3,00 → 2,96. | **NUEVA Y ABIERTA** | `nord_S6`, `instrument_S6`, `ledger_S6` |

### Hoja y composicion (`screens.py`, `overlay_instead`)

| # | objecion | estado | frame |
|---|---|---|---|
| C1 | El destructivo con `knockout_cell`. | **CERRADA** (inc54) | `blueprint_S4` |
| C2 | El modal abre con una regla y no cierra. | **CERRADA EN SWISS** (inc66) · **ABIERTA EN LEDGER**, cuarta ronda, con el destructivo en la ultima fila | **`ledger_S4`** |
| C3 | La banda se come el gate que el confirm nombra. | **CERRADA** (inc55) | `solari_S4` |
| C3' | La banda archiva una tarea bajo el gate equivocado. | **CERRADA** (inc65, ruling F amended, pertenencia leida del fixture) | `solari_S4` |
| **C3''** | **NUEVA. La banda de solari CIERRA y no ABRE.** | **NUEVA Y ABIERTA** | `solari_S4` f11 |
| C4 | El `.txt` de darkside no separa paneles. | **RULED** (E) — y la ruling esta **AUDITADA** desde inc63 y se sostiene | `darkside_S1` |
| C5 | El munion de sparkline pegado al conteo. | **ABIERTA, cuarta ronda, sin tocar** | `nord_S1` |
| C6 | El estado vacio de la busqueda es el del tablero. | **ABIERTA**, dos lenguajes, sin tocar | `solari_S6`, `ledger_S6` |
| C7 | Tres reglas identicas en una pantalla. | **ABIERTA, sin tocar**, y con un caso nuevo (swiss: 99 contra 100 celdas) | `instrument_S4`, `swiss_S4` |
| C8 | El confirm borra la aplicacion entera. | **CERRADA A MEDIAS por ruling** (`MODAL_KEEPS_ONLY_THE_HEAD`): vuelve la fila 1, siguen en blanco 30 de 32, y la banda no tiene ni abridor ni cierre | `corgi_S4` |
| C9 | El caption destructivo dibujado como fila de campo. | **ABIERTA, sin tocar**, tres lenguajes | `blueprint_S3`, `ledger_S3`, `naught_S3` |
| C10 | El fixture rinde dos hechos sobre el mismo tablero. | **RULED** (`G vs ruling 10`), sin codigo | `blueprint_S1`, `S2` |
| **C11** | **NUEVA. El cierre de la banda de swiss se cobro una fila del tablero de detras:** `DOING 4` ensenia una tarea. | **NUEVA, menor, declarada aqui porque el packet no la cuenta** | `swiss_S4` |

### Exportador

| # | objecion | estado |
|---|---|---|
| E1 | El tier de estilo no se pintaba. | **CERRADA** (inc43) |
| E2 | **El `.svg` no lleva metrica de fuente.** | **ABIERTA, cuarta ronda**, y ahora sostiene **siete** objeciones: los cuatro pares de homoglifo, `blueprint_S3`, `ledger_S2`, y toda la §0a — un ratio de contraste no es una prueba de legibilidad sin un raster a la altura de celda real |
| E3 | `gallery_darkside` es dependiente del calendario. | **ABIERTA**; no disparo en estos tres lotes |
| E4 | `cell_grid()` no leia el `ground` declarado. | **CERRADA** (inc63), verificada aqui sobre los 66 lienzos, con tres clausulas y dientes sobre bytes reales |
| **E5** | **NUEVA. El exportador pinta segundos grounds que ninguna ley lee** (`#2e2e2e`, `#1f2630`, `#e0d7c2`, `#1f1f1f`, `#17171a`). Es K6 desde el lado del artefacto. | **NUEVA Y ABIERTA** |

### Galeria y skill

| # | objecion | estado |
|---|---|---|
| G1 | La galeria instalada se queda rancia. | **CERRADA en `rework-6a` y RE-ABIERTA en `rework-6b`**: cinco de las 22 entradas estan rancias (32, 35, 37, 42, 43), misma causa, `export_to_skill.py` sigue sin tocar `assets/gallery/` |
| G2 | El repo del skill esta sucio y sin commitear. | **ABIERTA, sexto lote** |

---

## 6. La disciplina, medida

Cuatro cosas de estos tres lotes estan medidas, no afirmadas, y son mejores que la media:

1. **Cada ruling esta citada palabra por palabra en el packet y reproducida en `spec.md`**, con la razon escrita de por que dos de las cinco de `rework-6a` son *recorded and not implemented*. Una ruling que solo vive en un chat es una ruling con la que nadie puede discutir despues; estas se pueden citar en contra, y §7 lo hace.
2. **Toda ley se vio fallar sobre la declaracion o los bytes REALES antes de pasar** — inc63 sobre `ledger_S6.svg` y cuatro frames restaurados de `abd5193`, inc64 sobre las dos tablas de inc59, inc65 sobre el cuerpo de `band_head` de inc55, inc66 sobre el `▶  │` que ledger enviaba, inc69 sobre los cuatro espacios de inc38 byte a byte, inc70 sobre los cuatro `mut` con sus ratios de envio. **Un test que solo se ve pasar no es un test.**
3. **inc63 tuvo un brazo de control y lo dijo:** las 22 capturas de galeria volvieron **byte-identicas** tras el arreglo del exportador, porque `set_theme` corre antes del primer pintado. Un arreglo que no mueve la tuberia que ya estaba bien es la mejor evidencia de que se arreglo la que estaba mal.
4. **inc71 midio una prediccion publicada cuatro lotes antes y la encontro corta.** El pronostico de seis filas asumia que la pareja de cada runa era cromo desnudo; dos de seis (las de naught) eran significados reales, y solo correr el arreglo lo encontro. **Una prediccion publicada que nadie corrio es una conjetura con cifras.**

Y una al reves, por cuarta ronda: **`test_win_clipboard_roundtrip` estuvo en rojo en todas las
corridas de los nueve incrementos, incluidas las lineas base**, y esta nombrado en cada packet como
acoplado al entorno, no contado y no tocado. Es la forma correcta de llevar un test enfermo, y es la
cuarta ronda seguida que lo dice.

---

## 7. Objeciones a las rulings

Las rulings son firmes y los frames se juzgaron contra ellas. Estas siete lineas son desacuerdos.

1. **La ruling del `mut` tiene una clausula y rompio un numero que nadie medía.** *«`mut` es texto de cuerpo y debe alcanzar 4,5:1 contra el ground declarado»* es correcta. Subir `mut` hacia `ink` es, por construccion, estrechar todo canal que separaba `mut` de `ink`, y el tier de match es exactamente eso: nord 1,79 → **1,38**, instrument 2,45 → 2,32, ledger 3,00 → 2,96. **Una ley con una sola clausula optimizo un numero y degrado otro que tres rondas venian siguiendo.**

2. **La misma ruling lee un solo fondo.** Cinco kits pintan un segundo ground y contra el los numeros caen por debajo del piso recien asertado: ledger `mut` 4,51 → **4,10**, industrial `mut` 5,38 → **4,20**. Y los cuatro kits que inc70 movio quedaron **a una centesima del piso** (4,50 · 4,51 · 4,51 · 4,56), por la propia definicion de *«el paso mas pequenio que preserva el matiz»*. **Un piso alcanzado por el minimo paso posible se rompe con el primer rect que alguien pinte debajo.**

3. **La ruling nombra `ink` y `mut`; los frames gastan `dim` y `alert`.** `dim`/`seam`/`rail` esta bajo 3:1 en los once, bajo 1,6:1 en cinco, y es **mas de la mitad de las celdas pintadas en seis de las once hojas** — el 79 % en solari. `alert`, el token que dice «esto esta mal», esta bajo 4,5:1 en cinco kits. inc70 midio `dim` y lo dejo en un roster: el roster son once numeros y §0a es la consecuencia.

4. **`MODAL_KEEPS_ONLY_THE_HEAD` tomo la mitad barata de C8.** Volvio una fila a `corgi_S4` y siguen en blanco treinta. La objecion de la ronda tres tenia dos criterios y los dos responden, asi que la etiqueta baja — pero el frame **sigue sin abridor, sin cierre y sin caja**, que es palabra por palabra el eje por el que `swiss_S4` y `ledger_S4` son `rework`. **La exencion se renombro en vez de retirarse.**

5. **inc66 cerro C2 en el lenguaje que NO tenia el agravante.** La ronda tres nombro C2 en dos lenguajes y escribio que la de ledger era peor (*«debajo de `(Delete)` no hay nada … el limite inferior del modal es el borde de la terminal»*). En el mismo incremento, `Swiss.overlay_instead` gano su segunda regla y `Ledger.overlay_instead` no se toco. El arreglo existe, esta escrito y esta a cuatro lineas del que se hizo.

6. **inc71 partio `/` correctamente en el censo y de forma incomprobable en el corpus.** El segundo rol de `/` vive en `slider.knob[INVALID]` y `stepper.step[INVALID]`, y **ninguno de los 66 frames dibuja ninguno de los dos**. La fila de censo es real y ningun artefacto puede confirmarla ni refutarla. Y la colision que un lector SI puede ver en `industrial_S2` es otra: `▐12/09/26//////…▌`, donde los separadores del valor y el papel que los sigue son la misma celda sin frontera. **La ruling arreglo la contabilidad y la pregunta observable sigue sin duenio.**

7. **L7 se ruled como doctrina para dos lenguajes sobre una medicion que nadie habia tomado para los otros nueve.** *«Una escalera de tipo de linea donde la ausencia es el estado calmo»* se escribio para blueprint y ledger. Medido en el artefacto (§0b), **siete lenguajes mas dibujan su `info` y lo pintan entre 1,35:1 y 1,96:1**. La doctrina describe nueve de once y solo dos la declaran. **La ruling resulta mas correcta de lo que su propio argumento sabia**, y eso significa que se tomo por la razon equivocada: se cito un precedente en vez de medir el corpus.

---

## 8. Lo que esta ronda no puede ver

Se dice llano, y se dice por cuarta vez porque sigue siendo verdad.

1. **No se ejecuto nada.** Se leyeron 66 `.txt` y 66 `.svg` a `4089eda`, los mismos a `f1508ad`, los nueve packets, `spec.md` §16–§18, `collision_census.txt` y `themes.py`. **No se ejecuto la aplicacion, no se pulso ninguna tecla, no se movio ningun foco y no se corrio la suite.** Los numeros de gates citados (1249 passed, censo 30, 26 filas de homoglifo, rosters 16 y 9) estan **leidos de los packets y del disco**, no reproducidos aqui. Lo unico que esta ronda calculo son los contrastes de §0a–§0c, las cuentas de glifo y las atribuciones de fondo, los tres derivados de los ficheros.

2. **Un ratio de contraste no es una prueba de legibilidad, y esta ronda no tiene mas que ratios.** Cada numero de §0a–§0c sale de los `fill=` del `.svg` con la formula WCAG de luminancia relativa, atribuyendo cada caracter al rect que lo cubre por coordenada. **E2 sigue abierta**: el `.svg` no dice a que tamanio de celda ni con que fuente se va a renderizar, asi que `⠂` a 1,74:1 a una altura desconocida es un numero y no una fotografia. Antialiasing, subpixel y la gamma del monitor del lector estan fuera de este documento. **Todo §0b esta *planteado* con evidencia de la declaracion; ninguna de sus siete filas esta *resuelta*.**

3. **Y el instrumento puede fallar en la otra direccion.** La primera pasada de esta ronda atribuyo runs enteros a placas de dos celdas y devolvio dos contrastes de **1,00:1 y 1,03:1** en `darkside_S6` e `industrial_S6`. Los dos eran artefactos del medidor: la placa de match cubre dos celdas y el run empieza dentro de ella. **Se rehizo caracter a caracter y los dos hallazgos desaparecieron.** Se deja escrito porque una medicion adversarial que no publica su propio falso positivo no es una medicion.

4. **Aplicar 4,5:1 a un guia de puntos es probablemente el instrumento equivocado.** WCAG 1.4.3 es un piso para TEXTO y 1.4.11 para componentes no textuales. Un leader decorativo a 1,50:1 puede ser disenio correcto; un peldanio de severidad que clasifica una fila a 1,35:1 no lo es. **Esta ronda no resuelve cuales de las once tiradas de `dim` son decoracion y cuales son senial**: nombra las que son senial (los peldanios `info`, las tres etiquetas de modo de ledger, los terminadores de cota de blueprint) y deja el resto planteado.

5. **Un solo ancho.** Los 66 estan a 100×32. Los compromisos que dicen «at any width» siguen juzgados a un ancho, e inc54 declaro por escrito que el asiento destructivo de blueprint paso de 8 a 12 celdas y que nada en este repo renderiza `S4` por debajo de 100.

6. **El foco es una decoracion fija.** `FOCUSED` se lee de una marca, no de un foco. Que pasa al pulsar `tab`, si el modal atrapa el foco, si el anillo salta donde el lector espera: ninguna es respondible desde un frame.

7. **El componente que nadie ha visto.** El stepper tiene ley desde inc51 y **ningun artefacto de este repo lo dibuja**, cuarta ronda — y en `industrial` es una de las dos mitades de la colision que inc71 acaba de registrar (§7.6).

8. **Densidad, animacion y latencia.** La densidad no se re-midio (`verify_ink.py` no se corrio). Los `SPIN` de darkside y prism siguen sin censar, incluso despues de que inc67 metiera el conjunto B entero.

9. **Usuarios reales.** ISO 9241-210 pide evaluacion con usuarios; este equipo es una persona. Lo que hay aqui es **inspeccion con criterios declarados**, un recorrido cognitivo sobre las tareas que el contexto de uso nombra. **No se hizo ninguna evaluacion con usuarios reales, y ninguna afirmacion de este documento debe leerse como si se hubiera hecho.**

---

## 9. Convergencia — y si vale la pena una quinta ronda

### 9a. Lo que dice que si converge

- **Los `rework` van 19 → 7 → 11 → 4**, y el 11 de la ronda tres incluia ocho primeras lecturas. Sobre los 42 originales la serie es 19 → 7 → 3 → **1** (`blueprint_S3`).
- **Los cinco objetivos de instrumento estan cerrados.** K1, K2, K3, K4 y K5. El censo lee el conjunto B, la tabla de homoglifos es derivada, dos estados de un `part` se comparan, el rune tiene una definicion que los dos ficheros importan. Once lotes, y esta hecho.
- **Los cuatro `rework` que quedan son un incremento de un fichero cada uno**, los cuatro nombrados desde la ronda tres, y **uno de ellos (`ledger_S4`) tiene el arreglo ya escrito y probado en otro lenguaje**.
- **Ninguna etiqueta bajo por un defecto nuevo del corpus.** Las cuatro bajadas son un instrumento nuevo aplicado a frames que no se movieron.

### 9b. Lo que dice que no

- **El instrumento nuevo de esta ronda encontro una clase nueva en su primera pasada.** Leer la pintura contra un ground que no es mentira produjo, de una vez: siete lenguajes con el peldanio `info` invisible, tres tiers de match estrechados por el lote que buscaba legibilidad, cinco segundos grounds fuera de toda ley, `alert` bajo 4,5:1 en cinco kits, y **cuatro etiquetas retrocedidas**. Eso es K6, K7, L11, C3'', C11 y E5: **seis objeciones nuevas en la ronda que tenia menos `rework` de la serie.**
- **El patron que los propios packets nombran no se ha detenido.** §17.7: *«la escritura de una ley encontro la siguiente, dos veces en dos lotes»* — inc63 escribio `contrast(ink, ground)` y midio `mut`; inc70 escribio `contrast(mut, ground)` y midio `dim`. Esta ronda escribio `contrast(cualquier cosa, lo que hay realmente debajo)` y encontro los segundos grounds y `alert`. **Cuatro iteraciones, exactamente una pregunta nueva por iteracion.** Una serie que produce una incognita por vuelta no ha convergido; esta iterando.
- **La tasa de hallazgo no cayo, cayo la tasa de `rework`.** Son cosas distintas. Las objeciones nuevas por ronda van 8 (ronda tres) → 6 (ronda cuatro), y las de esta son estructuralmente mas grandes: K5 era un widget, K7 es la mitad de las celdas pintadas del corpus.

### 9c. Que encontraria una quinta ronda que esta no pudo

Tres cosas, y **ninguna de las tres se consigue leyendo los mismos 66 `.svg` otra vez**:

1. **Un raster a la altura de celda real (E2).** Es lo unico que convierte en decidibles las siete objeciones que hoy estan solo *planteadas*: los cuatro pares de homoglifo, los tres guiones de `blueprint_S3`, `† / ‡`, y toda la §0a — porque un ratio no dice si `⠂` a 1,74:1 y 12 px se ve. **Lleva tres rondas pedido y no se ha construido.** Es un script y un PNG por frame.
2. **Un segundo y un tercer ancho.** Todo compromiso que dice «at any width» esta juzgado a 100. inc54 dejo escrito que el asiento destructivo de blueprint es *«untested rather than safe»*. Renderizar a 80 y a 120 es una linea de `render.py` y la respuesta es hoy desconocida.
3. **Una tecla.** El foco es decoracion en los 66. Tab order, atrapado de foco en el modal y viaje del anillo son la parte de *«el disenio atiende la experiencia completa»* de ISO 9241-210 que este corpus no ha tocado nunca, y `App.run_test()` + `Pilot` es el mecanismo real que existe y no se ha usado.

### 9d. El veredicto

**La serie de rondas ha convergido; el programa no.** Y son dos afirmaciones distintas.

Una quinta lectura adversarial de las mismas 66 imagenes fijas encontraria la version de cuarto orden
de lo mismo, y la evidencia esta en esta ronda: **sus cuatro regresiones salen todas de una sola
medicion nueva, y sus cuatro `rework` supervivientes estaban los cuatro nombrados en la ronda tres.**
Lo que produjo hallazgos aqui no fue mirar otra vez, fue **mirar con una regla que antes no existia**.
Otra pasada con la misma regla anade prosa.

**Recomendacion, y es parar la ronda y cambiar el instrumento:**

- **Enviar los cuatro `rework`** como un lote. Son cuatro ediciones en cuatro ficheros y cada una tiene un criterio observable escrito. `ledger_S4` es literalmente el diff que inc66 le hizo a swiss.
- **Decidir K6/K7 en una ruling, no en una ronda.** ¿Se floorea `dim`? ¿Se floorea `alert`? ¿La ley lee el rect que hay debajo o solo el ground declarado? Son tres preguntas de una linea cada una y esta ronda las deja medidas. **Ninguna necesita otra lectura de 66 frames.**
- **Construir el raster (E2) y solo entonces correr la ronda cinco**, contra el raster y a dos anchos. Esa ronda puede fallar de una forma distinta, que es la unica razon honesta para correr una.

Y el limite que ninguna de las tres cosas levanta: **once lenguajes de disenio se han argumentado
hasta esta forma leyendo imagenes, y lo que mas moveria el corpus no es una quinta ronda ni un raster.
Es una sesion con una persona que no haya visto el kit, a la que se le pida senialar la celda que
significa «esto destruye datos».** Cuatro rondas de este documento han escrito ese criterio
veintitantas veces y ninguna lo ha ejecutado sobre un ser humano.

---

## 10. Como reproducir esta ronda

```
git -C <worktree> diff --stat f1508ad 4089eda -- prototypes/components/
git -C <worktree> show f1508ad:prototypes/components/<frame>.txt
git -C <worktree> show f1508ad:prototypes/components/<frame>.svg
python -X utf8 prototypes/components/render.py       # 66 .txt + 66 .svg (NO corrido)
python -X utf8 prototypes/collision_census.py        # (NO corrido; leido de out/)
python -X utf8 -m pytest -q                          # (NO corrido)
```

Los contrastes de §0a–§0c salen de los `fill=` de los `.svg` con la formula WCAG de luminancia
relativa (`L = 0,2126R + 0,7152G + 0,0722B` sobre canales linealizados; `(L1+0,05)/(L2+0,05)`),
**atribuyendo cada caracter al `<rect>` que lo cubre por coordenada**, con ancho de celda 8,4 px y
alto 17 px leidos del propio `.svg`. Las cuentas de glifo son `str.count` sobre los `.txt` en disco.

**Pagina del operador:** `ronda-66-despues.html`, con los 66 frames, el `.svg` de `f1508ad` al lado
del nuevo para los 66 (el ground cambio en todos), y un voto por frame.

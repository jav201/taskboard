# PROTOTYPE-inheritors-3 — los 66 frames: 42 rejuzgados, 24 leidos por primera vez

**Tercera ronda adversarial, y la primera sobre el corpus completo.** La primera
(`PROTOTYPE-inheritors.md`, 2026-09-05) juzgo 42 frames y propuso **keep 6 · nota 17 · rehacer 19**.
La segunda (`PROTOTYPE-inheritors-2.md`, 2026-09-06, en `b559e92`) rejuzgo los mismos 42 tras
`rework-1/2/3` y propuso **keep 14 · nota 21 · rehacer 7**, con las objeciones en pie agrupadas por
duenio (K1–K4, L1–L6, C1–C7, E2, E3) y siete decisiones (A–G) puestas al operador.

Desde entonces corrieron cuatro lotes — `rework-4` (inc49–51), `rework-5a` (inc52–54),
`rework-5b` (inc55–57) y `rework-5c` (inc58–62) — **las siete decisiones estan RULED**, los dos
rosters de asiento estan en cero para los once lenguajes por primera vez en el corpus, el censo bajo
de 48 a 25 y las filas de homoglifo de 4 a 1.

Esta ronda **no toco ningun kit, ningun test y ningun frame**: leyo los 66 `.txt` y los 66 `.svg` a
`f1508ad`, los `.txt` y `.svg` de `b559e92` para los 27 que se movieron, los packets `inc49`–`inc62`,
`spec.md` §12–§15 y `prototypes/out/collision_census.txt`. Vocabulario de veredicto cerrado, el mismo:
**`keep` / `keep with a note` / `rework`**. Propuestos, no decididos.

Las rulings de inc52–inc61 son del orquestador sobre la delegacion del operador y **son firmes**: aqui
se juzga si el frame las honra, no si la ruling era correcta. Donde no estoy de acuerdo con una ruling
va una linea en §7 y nada mas.

**Resultado: de los 42, keep 15 · nota 24 · rehacer 3. De los 24 nunca juzgados, keep 0 · nota 16 ·
rehacer 8. Total sobre 66: keep 15 · nota 40 · rehacer 11.**

---

## 0. Cuatro cosas que hay que decir antes de la primera tabla

### 0a. El defecto mas grande de la ronda esta en el exportador y no en ningun kit

`ledger` es **el unico de los once lenguajes con papel claro**: `themes.py` linea 361 declara
`ground="#e9e1cf", ink="#1c1a15"`. `cell_grid()` no lee esa declaracion: mide el fondo como *"the most
common background in the frame"* y devuelve `#121212`. Resultado, medido sobre los seis `.svg` de
ledger con la formula WCAG:

| tinta | rol | contra el `fill="#121212"` que el `.svg` pinta | contra el ground declarado `#e9e1cf` |
|---|---|---|---|
| `#1c1a15` | `ink` — nombres de tarea, gates, cabeceras | **1,08:1** | 13,36:1 |
| `#2b3a67` | `accent` — el cursor `▶` | **1,70:1** | — |
| `#6b6558` | `mut` — el cuerpo de las filas | 3,24:1 | — |
| `#c4b99f` | `dim` — los puntos guia `·` | **9,62:1** | — |

**Los seis `.svg` de ledger estan en negro sobre negro y con la jerarquia invertida: lo unico legible
son los puntos guia.** `ledger_S6.svg` contiene 14 runs a `#1c1a15` y 13 a `#c4b99f`.
**Criterio observable, ejecutable hoy:** abrir `ledger_S1.svg` y decir que tarea esta en `DOING`. El
`.txt` responde; el `.svg` a 1,08:1 no. Es **E4**, es una linea del exportador, y no es de ledger.

Importa mas de lo que parece porque la ruling **E** (inc55) asciende el `.svg` a *artefacto de
registro* para darkside. Esa ruling es correcta y esta **sin auditar**: el exportador no lleva el
ground declarado del kit, y que darkside no salga danado es suerte (su ground ya es oscuro), no una
medicion.

### 0b. Ninguna ley, ningun censo y ninguna ruling llega a un widget de CANTIDAD, y ahi viven tres de los ocho rehacer nuevos

El slider, la barra y el scrollbar estan **fuera del conjunto B del censo por peticion del propio
operador** (`spec.md` §15.4 lo imprime), y el medidor de progreso, la sparkline, el pager y el mascot
del estado vacio se dibujan fuera de `PART_GLYPHS` en los once. Los cuatro lenguajes nuevos ponen un
peldano de significado dentro de uno:

| frame | el widget | la celda | lo que esa celda significa en el mismo lenguaje |
|---|---|---|---|
| `naught_S1` f13 | barra 44 % | `∙` × 13 | `LEVELS[error]` (`∙∙`) y `DANGER_FORM` byte a byte |
| `naught_S3` f16 | slider 70 | `∙` × 9 | idem, **cuatro filas encima de `∙Delete all∙`** |
| `corgi_S1` f4-30 | el rail entre tablero y detalle | `█` × 25 | `LEVELS[error]` (`██`) y `DANGER_FORM` |
| `corgi_S1` f13 | medidor 44 % | `▄▄` × 4 | `LEVELS[warn]` |
| `corgi_S3` f16 | slider 70 | `▄▄` × 3, `▁▁` | `LEVELS[warn]` y `LEVELS[info]` |
| `corgi_S1` f31 | pager, pagina actual | `██` | `LEVELS[error]` y `DANGER_FORM` |
| `prism_S1` f31 | pager, ventana actual | `⣿⣿⣿⣿` | `LEVELS[error]` y `DANGER_FORM` |
| `prism_S3` f16 | slider 70 | `⣿` × 9 | idem, **cuatro filas encima de `⣿Delete all⣿`** |

`MEANING_AT_AN_OPENER` y `MEANING_AT_A_NAMED_SEAT` leen **cero** para los cuatro. Los frames no.
Es **K5**, nueva, y es la superficie sin cubrir mas grande del corpus.

### 0c. El tier de estilo de los cuatro lenguajes nuevos, medido por primera vez

| lenguaje | `MATCH_STYLE` | lo que pinta el `.svg` | tinta match | tinta cuerpo | match↔cuerpo |
|---|---|---|---|---|---|
| naught | `bold {ink}` | 6 × `font-weight="bold"` | `#f5f5f5` | `#8a8a8a` | 3,17:1 |
| corgi | `bold {ink}` | 6 × `font-weight="bold"` | `#f2f2f2` | `#9a9a9a` | 2,51:1 |
| prism | `bold {accent}` | 6 × `font-weight="bold"` | `#2dd4bf` | `#8b98a5` | **1,58:1** |
| ledger | `underline {ink}` | 6 × `text-decoration="underline"` | `#1c1a15` | `#6b6558` | 3,00:1 **e ilegible por E4** |

Dos lecturas: **prism es ahora el peor de los once en este tier** (1,58:1, por debajo del 1,79 de nord
y por encima solo del 1,36 de swiss), y **`#2dd4bf` es byte a byte el acento de match de instrument y
tambien el cursor `▸` de prism en la misma fila** — la nota que la segunda ronda le escribio a
`instrument_S6` y a `blueprint_S6`, ahora por tercera vez y en dos lenguajes a la vez.

### 0d. Lo que las tres leyes siguen sin poder ver, ampliado por los 24

K2 (*«las leyes comparan code points y el lector lee formas»*) sigue abierta y los cuatro lenguajes
nuevos la agravan. `HOMOGLYPHS` del censo es una **lista fija de cinco pares** (`• ●`, `· ∙`, `○ O`,
`o ◦`, `▪ ■`). Los cuatro pares mas apretados del corpus no estan en ella:

| lenguaje | el par | los dos significados | donde |
|---|---|---|---|
| naught | `⊙` contra `◉` | radio elegido contra checkbox marcado | `naught_S2` f9 y f11, **dos filas** |
| naught | `○` contra `◦` | radio sin elegir contra tag sin marcar | mismas dos filas |
| ledger | `†` contra `‡` | `REQUIRED` contra `INVALID` | `ledger_S2` f4 y f6, **tres celdas** |
| blueprint | `╌` `┄` `┈` | warn contra extension muerta contra leader muerto | `blueprint_S3` f6, cuenta de guiones 2/3/4 |

Y **E2 sigue abierta**: el `.svg` no lleva metrica de fuente, asi que ninguna de las cuatro se puede
*resolver* aqui. Se plantean con la evidencia de la declaracion y del frame, y hace falta un raster a
la altura de celda real para cerrarlas.

---

## 1. La matriz 11×6

Para los 42: **antes (`b559e92`) → despues**. Para los 24: primera lectura.

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| **instrument** | nota → **nota** | rework → **nota** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** |
| **swiss** | nota → **nota** | rework → **rework** | keep → **keep** | rework → **rework** | nota → **nota** | nota → **nota** |
| **industrial** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | nota → **keep** | keep → **keep** |
| **nord** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | keep → **keep** | nota → **nota** |
| **darkside** | rework → **nota** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | keep → **keep** |
| **solari** | nota → **nota** | nota → **nota** | keep → **keep** | nota → **nota** | nota → **nota** | nota → **nota** |
| **blueprint** | nota → **nota** | rework → **nota** | rework → **rework** | rework → **nota** | nota → **nota** | keep → **keep** |
| **naught** | **nota** | **rework** | **nota** | **rework** | **nota** | **nota** |
| **corgi** | **rework** | **nota** | **nota** | **rework** | **nota** | **nota** |
| **prism** | **rework** | **rework** | **nota** | **nota** | **nota** | **nota** |
| **ledger** | **nota** | **nota** | **nota** | **rework** | **nota** | **rework** |

|  | keep | keep with a note | rework |
|---|---|---|---|
| **los 42, antes** (`b559e92`) | 14 | 21 | 7 |
| **los 42, despues** (`f1508ad`) | **15** | **24** | **3** |
| **los 24, primera lectura** | **0** | **16** | **8** |
| **los 66** | **15** | **40** | **11** |

**Ninguna etiqueta de los 42 retrocedio.** Cuatro `rework` se cerraron (`instrument_S2`,
`darkside_S1`, `blueprint_S2`, `blueprint_S4`) y uno subio a keep (`industrial_S5`). Los tres que
quedan son **dos composiciones que ningun lote ha tocado** (`swiss_S4`, `blueprint_S3`, la primera
nombrada como *still open* desde §11.3) y **una declaracion que lleva tres rondas nombrada**
(`swiss_S2`, L2).

**Cero `keep` en los 24.** La primera ronda dio 6 keep de 42 en primera lectura (14 %); esta da 0 de
24, y no es dureza: los cuatro lenguajes tuvieron **un** incremento cada uno, guiado por tres leyes
que miran declaraciones de control, y ninguna de las tres mira una composicion, una cantidad ni una
hoja. El resultado es exactamente el que ese alcance predice.

---

## 2. Los 66 bloques

Contexto de uso, sin cambios respecto de las dos rondas anteriores: **operador unico** (`jav201`),
terminal de 100×32 monoespaciado, sesion diurna, tema por defecto; la tarea es la que la pantalla
nombra. Para los 42 el formato es *objecion previa · que cambio · estado · veredicto*; para los 24 es
*compromiso puesto a prueba · lo que ensenia el frame · objecion mas fuerte con criterio observable ·
veredicto*.

---

### 2.1 instrument

`LEVELS ⠂⠂/⠆⠆/⠇⠇` · `REQUIRED ⠁` · `DANGER ⠛⠛` · `CUR ⣿` · `FIELD_LEAD ⠒` (declarado en inc57) ·
`MATCH underline {accent}`. Sin incremento en `rework-4/5a/5b/5c` salvo inc52 (una declaracion) e
inc57 (`FIELD_LEAD` declarado, sin mover).

#### `instrument_S1` — nota → **`keep with a note`**
* **Objecion previa:** el gutter `⠸` (una vez por fila) compite con los leaders `⠒` del panel derecho (hasta cuarenta por fila).
* **Que cambio:** nada en el frame. **Pero inc57 declaro `FIELD_LEAD = "⠒" (= LATT)`**, asi que la celda que compite con el gutter tiene ahora una familia mas en el censo (B×B de instrument 12 → 14).
* **Estado: sigue en pie, y con una familia mas.** Es una de las objeciones que empeoraron bajo etiqueta fija.
* **Veredicto: `keep with a note`.**

#### `instrument_S2` — rework → **`keep with a note`**
* **Objecion previa (L1):** el campo invalido, el textarea y el boton por defecto llevaban **la misma pareja de paredes** (`⠸ … ⠇`). *«Tapar la fila 7 y senialar el campo invalido leyendo solo las paredes: no hay ninguna respuesta.»*
* **Que cambio** (inc52, ruling C):

  ```
  b559e92  due⠁   ⠸12/09/26⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠇
  f1508ad  due⠁   ⠶12/09/26⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶
  ```
* **Estado: RESPONDIDA, y por el camino correcto.** El campo invalido es ahora **una tirada uniforme de 27 `⠶`** contra `⠼Fix login⡇ redirect⠤⠤…⠧` del campo normal. Es una respuesta de forma, no de orden de paredes, que es literalmente lo que el veredicto de la segunda ronda pidio (*«darle al INVALID una forma, no un par de paredes»*).
* **Objecion nueva:** `⠶` es tambien **el radio elegido**, tres filas mas abajo — `priority  ⠐ low  ⠐ norm  ⠶ high`. Censo: `⠶ [3 families] INVALID stepper.step + INVALID textfield.main × 3 · radio.knob mark (checked,default) · switch.indicator mark (disabled)`. **Criterio observable:** en `instrument_S2`, tapar las palabras y decir cual de las dos apariciones de `⠶` dice «elegido» y cual dice «no parsea». La posicion y la cuenta (1 celda contra 27) responden; la celda no.
* **Y lo que no se movio:** `⠇` sigue cerrando `Cancel` en la fila 17 y sigue siendo el leader del mensaje de error de la fila 7. Censo `⠇ [3 families]`.
* **Veredicto: `keep with a note`.**

#### `instrument_S3` — nota → **`keep with a note`**
* **Objecion previa:** `⣿` es `CUR` **y** el relleno de la pista encendida de los cinco switches **y** el relleno del slider **y** la marca de opcion elegida **y** la pestania activa.
* **Que cambio:** nada. Ningun incremento de los cuatro lotes toco `CUR` en instrument.
* **Estado: sigue en pie, intacta.** `CUR` esta fuera del conjunto de significados por decision documentada, asi que ninguna de las tres leyes lo vera nunca; el censo lo firma (`⣿ [3 families]`).
* **Veredicto: `keep with a note`.**

#### `instrument_S4` — nota → **`keep with a note`**
* **Objecion previa (C7):** las filas 3, 13 y 20 son la misma cadena de 100 `⠒`; no hay forma de distinguir «hay un modal» de «aqui acaba la cabecera».
* **Que cambio:** nada.
* **Estado: en pie, entera.** `inc57` ademas declaro `⠒` como `FIELD_LEAD`, con lo que la cadena que dibuja el modal es tambien la que dibuja el guia de campo.
* **Veredicto: `keep with a note`.**

#### `instrument_S5` — keep → **`keep`**
* Frame identico. La escalera `⠂⠂ / ⠆⠆ / ⠇⠇` sigue siendo monotona por cuenta de puntos y sigue siendo de las dos mejores del corpus con el color quitado. Sin cambios.

#### `instrument_S6` — keep → **`keep`**
* Frame identico. El subrayado + el salto 2,45:1 siguen. **Nota que engorda:** `#2dd4bf` es ahora el acento de match de **dos** lenguajes (instrument y prism) y en los dos es tambien la tinta del cursor de la misma fila.
* **Veredicto: `keep`.**

---

### 2.2 swiss

`LEVELS ·/─/━` · `REQUIRED •` · `DANGER ╲╱` · `CUR ▮` · `FIELD_LEAD ""` (aire, por compromiso).

#### `swiss_S1` — nota → **`keep with a note`**
* **Objecion previa:** tres hairlines en una pantalla cuyo compromiso dice «una»; y `▮ ▪ ■ ▫` son cuatro rectangulos macizos a cuatro tamanios.
* **Que cambio:** nada en el frame. **Pero inc53 movio el radio elegido a `▪`**, de modo que la celda que en `S1` es el peldanio alto del boton es ahora tambien «esta opcion esta elegida» y «esta casilla esta marcada».
* **Estado: en pie, y el grupo de cuatro rectangulos gano dos roles.**
* **Veredicto: `keep with a note`.**

#### `swiss_S2` — rework → **`rework`**
* **Objecion previa:** **(a)** `Save` (DISABLED) es aire, tipograficamente identico a la leyenda de la fila siguiente; **(b)** cinco controles abren con una pared y ninguno cierra; **(c)** el campo invalido abre con `╲`, `DANGER_FORM[0]`.
* **Que cambio** (inc52 ruling C, inc53 ruling D):

  ```
  b559e92  due•      ╲12/09/26            HEAD  due•      ║12/09/26
  b559e92  priority  ╵   low  ╵   norm  ╵●  high
  f1508ad  priority  ╵   low  ╵   norm  ╵▪  high
  ```
* **Estado: (c) RESPONDIDA por ruling C** — `║` no es el `DANGER_FORM` ni ningun peldanio, y la exencion por nombre que la protegia fue **borrada** en inc52 despues de medirla en cero disparos. **(a) SIGUE EN PIE, tercera ronda.** La fila 18 es `     Save        ▫   Cancel`: el boton que el usuario tiene que pulsar es el unico control de la pantalla sin ninguna marca, y esta justo encima de `Save is held until due parses`, que es una leyenda. `spec.md` §11.3 lo admite palabra por palabra desde `rework-3`. **(b) sigue en pie.**
* **Objecion nueva, y es de las que empeoraron:** `▪` es ahora **el radio elegido (f10) y el checkbox marcado (f12), dos filas seguidas**, y en `swiss_S4` es el anillo de foco de `╲Delete╱`. **Criterio observable:** en `swiss_S2`, tapar las palabras `low/norm/high` y `api/ui/urgent` y decir cual de las dos filas es una eleccion unica y cual son casillas. La unica diferencia es el pozo, `╵` contra `│`, una celda.
* **Y el campo invalido perdio la ultima referencia de extension:** `║12/09/26` es una pared y ocho caracteres; sin papel y sin cierre. **Criterio:** decir hasta donde llega el campo de fecha. Sin respuesta.
* **Veredicto: `rework`.** El eje incumplido: **L2**, un control deshabilitado sin marca junto a uno con marca, nombrado en la primera ronda, en la segunda y en `spec.md` §11.3, y sin tocar en cinco lotes.

#### `swiss_S3` — keep → **`keep`**
* Frame identico. La escalera `▫ ▪ ■` sigue siendo una forma a tres pesos (avalada por la ruling D-addendum de inc55) y `━` sigue fuera de la pantalla entera.
* **Nota:** `─` (`LEVELS[warn]`) sigue siendo la pista apagada del switch y la vacia del slider. La posicion salva la lectura; se registra por segunda vez.

#### `swiss_S4` — rework → **`rework`**
* **Objecion previa (C2):** el modal abre con una regla de 100 celdas y **no cierra**.
* **Que cambio:** **nada.** `swiss_S4` no se movio ni un byte desde `8604607`: ni `rework-1/2/3` ni los cuatro lotes posteriores lo tocaron.
* **Estado: en pie, entera, y nombrada como *still open* desde `spec.md` §11.3.** **Criterio observable:** decir donde termina el modal. Sin respuesta, en un confirm destructivo, tercera ronda seguida.
* **Nota:** inc53 puso el anillo de foco del boton irreversible (`▪`) sobre la misma celda que el checkbox marcado de `S2`.
* **Veredicto: `rework`.** El eje incumplido: **C2**, composicion en `overlay_instead`.

#### `swiss_S5` — nota → **`keep with a note`**
* **Objecion previa (L6):** la sparkline de la fila 7 se dibuja con los dos peldanios altos de `LEVELS`, seis filas encima del log que los usa como severidad.
* **Que cambio:** nada.
* **Estado: en pie, y ahora con un tercer caso** — `corgi_S5` hace exactamente lo mismo (§2.9). L6 pasa de dos lenguajes a tres.
* **Veredicto: `keep with a note`.**

#### `swiss_S6` — nota → **`keep with a note`**
* **Objecion previa:** `#e2231a` contra el cuerpo `#8a8a8a` es **1,36:1**; con el color quitado el match desaparece y queda solo el peso.
* **Que cambio:** nada.
* **Estado: en pie. Sigue siendo el peor de los once en el tier de estilo**, ahora medido contra los cuatro nuevos (naught 3,17 · corgi 2,51 · prism 1,58 · ledger 3,00).
* **Veredicto: `keep with a note`.**

---

### 2.3 industrial

`LEVELS ▫▫/▪▪/■■` · `REQUIRED !` · `DANGER ╱╱` · `CUR ▶` · `DISCLOSE ▼` · `MATCH reverse {accent}`.

#### `industrial_S1` — nota → **`keep with a note`**
* **Objecion previa (L5):** `CUR = ▶` y `DISCLOSE = ▼` son el mismo triangulo girado; y el plato `▐▌` carga cuatro sentidos.
* **Que cambio:** nada.
* **Estado: L5 RESPONDIDA POR RULING.** El addendum a D (inc55, citado en `spec.md` §14.1) dice: *«Rotation counts as a channel when it is direction the language already spends (opener/closer, up/down), not otherwise.»* industrial gasta direccion en su propio alfabeto (`▶` derecha, `▼` abajo), asi que la rotacion es un canal declarado aqui. **La objecion queda retirada.**
* **Lo que queda:** el plato con cuatro sentidos, sin cambio.
* **Veredicto: `keep with a note`.**

#### `industrial_S2` — nota → **`keep with a note`**
* **Objecion previa:** las paredes del campo invalido son byte a byte las del campo normal y las del boton; el canal que queda es el relleno `//////` (30 celdas) contra `------`.
* **Que cambio:** nada. inc52 no toco industrial (su `textfield[INVALID]` nunca fue el `DANGER_FORM`).
* **Estado: en pie, y sigue siendo aceptable por la misma razon**: el canal del relleno es real y ancho. Segunda nota sin cambio: `!` es tambien el marcador de vencido en `S1`.
* **Veredicto: `keep with a note`.**

#### `industrial_S3` — keep → **`keep`**
* Frame identico. El caption va desnudo y el boton conserva `▐ ╱╱Delete all╱╱ ▌`. Sigue siendo la referencia del corpus para la separacion caption/control, y §2.10 y §2.11 muestran los dos lenguajes que no la tienen.

#### `industrial_S4` — keep → **`keep`**
* Frame identico. La caja de plato, el chrome intacto y la hachura `╱╱` sobre `Delete`. Sigue siendo la mejor superposicion de los once: el tablero de detras entero, el modal cerrado por sus cuatro lados, la respuesta destructiva mas pesada que la segura.

#### `industrial_S5` — nota → **`keep`**
* **Objecion previa:** distinguir `▪` de `■` a 12 px sin verlos adyacentes.
* **Que cambio:** nada en el frame.
* **Estado: RESPONDIDA POR RULING.** El addendum a D (inc55): *«A ladder is one meaning at monotone intensities and is one declaration: industrial's severity `▫▫ ▪▪ ■■` passes from hollow to filled (weight) and grows (size) in the same direction, so it stands.»* La escalera va en el mismo sentido en dos canales a la vez, peso y tamanio, y la ruling la avala por nombre. La lectura de la primera y la segunda ronda **queda retirada**.
* **Lo que no cierra, y no es de este frame:** K4 (ninguna ley compara dos estados de un mismo `part`) y E2 (sin metrica de fuente no hay como *resolverlo* desde el artefacto). Los dos son de instrumento.
* **Veredicto: `keep`.** Es la unica subida de etiqueta de los 42 en esta ronda.

#### `industrial_S6` — keep → **`keep`**
* Frame identico. Los seis platos `#ff4b1f` con tinta `#121212`, 5,60:1. Sigue siendo la respuesta mas robusta a la escala de grises junto con solari.

---

### 2.4 nord

`LEVELS "· "/"! "/"!!"` · `REQUIRED *` · `DANGER ##` · `CUR ▸` · `FIELD_LEAD ""`.
**El lenguaje mas limpio del censo: 1 celda colisionante de 25.**

#### `nord_S1` — nota → **`keep with a note`**
* **Objecion previa (C5):** `BACKLOG 5▂` / `DOING 4▂`, el munion de sparkline pegado al conteo; y la pista vacia del medidor `───────` es la misma celda que las tres reglas de seccion.
* **Que cambio:** nada.
* **Estado: en pie, entera.** Nombrada en la primera ronda, en la segunda y sin tocar en cuatro lotes.
* **Veredicto: `keep with a note`.**

#### `nord_S2` — nota → **`keep with a note`**
* **Objecion previa (L4):** tres vocabularios de pared en una pantalla — `▐ … ▌` para el campo en edicion, `[ … ]` para textarea/checkbox/boton, `? … ?` para el invalido.
* **Que cambio:** nada en el frame. inc51 le dio a `stepper.main[DEFAULT]` el `░░` de nord (el peldanio mas claro de su rampa de sombra) — **un cuarto vocabulario, que ningun frame del corpus dibuja**, porque `spec.md` §12.5 mide que *«no artefact in this repo draws a stepper at all»*.
* **Estado: en pie, y con un cuarto vocabulario declarado y no renderizado.**
* **Nota que se mantiene:** `?` sigue siendo simetrico y una forma, que es lo que resolvio la objecion original, y inc52 lo midio limpio y lo dejo por instruccion expresa de la ruling C.
* **Veredicto: `keep with a note`.**

#### `nord_S3` — keep → **`keep`**
* Frame identico. `[ #Delete all# ]` con caption desnudo. La nota de la segunda ronda (`#` no lleva semantica de peligro propia) se mantiene sin engordar.

#### `nord_S4` — keep → **`keep`**
* Frame identico. `▐  #Delete#  ▌` contra `[ ]`. Sigue siendo el mejor modal del corpus junto a industrial.

#### `nord_S5` — keep → **`keep`**
* Frame identico. El caso mas limpio de todo el programa: el hallazgo estructural de la primera ronda se cerro sin tocar el frame que lo ensenaba.

#### `nord_S6` — nota → **`keep with a note`**
* **Objecion previa:** `#88c0d0` contra el cuerpo `#7b88a1` es **1,79:1**, el margen mas estrecho de los kits de `bold`; y el campo de consulta usa `▐re▏…▌` mientras el textarea de `S2` usa `[ … ]`.
* **Que cambio:** nada.
* **Estado: en pie. Ya no es el margen mas estrecho**: prism marca 1,58:1 (§0c). Como `MATCH_STYLE` aqui es el de `Kit` sin tocar, 1,79 sigue siendo la linea base contra la que eligieron los otros diez.
* **Veredicto: `keep with a note`.**

---

### 2.5 darkside

`LEVELS "· "/"o "/"O "` · `REQUIRED ▪` · `DANGER ▚▞` (inc52) · `CUR ▊` · `FIELD_LEAD ▔` (inc53/57) ·
`IDENT_GLYPHS` declarado (inc57) · `MATCH reverse {mut}`.

#### `darkside_S1` — rework → **`keep with a note`**
* **Objecion previa (C4):** el `.txt` no tiene ninguna separacion de paneles (el escalon gris vive solo en el `.svg`, 28 `<rect>`), mientras el rail `▏` se imprime dieciseis veces. *«O el rail cede, o el `.txt` deja de ser la obra para este lenguaje, y eso es un veredicto del operador.»*
* **Que cambio:**

  ```
  b559e92  (O)board  ( )form  ( )cfg  ( )log     ...   project   ◦ Web
  f1508ad  (●)board  ( )form  ( )cfg  ( )log     ...   project   ▔ Web
  ```
* **Estado: RESPONDIDA POR RULING E** (inc55, `spec.md` §14.1): *«For darkside the SVG is the artefact of record, not the txt; a darkside frame's grey step is a real signal. `darkside_S1` is not reworked on the txt's evidence.»* Escrita en `Darkside.pane_split_instead` para que quien lea un `.txt` pelado encuentre la resolucion antes que la objecion. **El frame honra la ruling y la etiqueta baja.**
* **Lo que la ruling no cierra, y lo dice ella misma:** los dieciseis trazos del rail, y **E2**.
* **Objecion nueva, y va contra la ruling y no contra el frame:** ascender el `.svg` a artefacto de registro presupone que el exportador es fiel al kit. **No lo es** — §0a mide que `cell_grid()` ignora el `ground` declarado y que ledger sale a 1,08:1. Que darkside no salga danado es que su ground ya era oscuro.
* **Veredicto: `keep with a note`.**

#### `darkside_S2` — nota → **`keep with a note`**
* **Objecion previa:** la sobrecarga de `▬` (cinco significados) sin consecuencia de acto en esta pantalla.
* **Que cambio** (inc49, inc57): `( )board (O)form` → `( )board (●)form`; `(O) ui  (O) urgent` → `(◎) ui  (◎) urgent`.
* **Estado: la sobrecarga de `▬` sigue** (paredes de textarea, paredes de select, pista de switch, relleno de slider). `O` salio de los controles, que es K1.
* **Objecion nueva, y la admite el propio inc57:** *«`(●)` is one cell away from `{●}` … and `( )` IS `checkbox.main[default]`»*. En esta pantalla la fila 1 dice `( )board  (●)form  ( )cfg  ( )log` y la fila 11 dice `( ) api  (◎) ui  (◎) urgent`: **cuatro pares de parentesis en la fila 1 son byte a byte un checkbox sin marcar.** **Criterio observable:** en `darkside_S2`, tapar las palabras y decir cuales de los siete pares de parentesis son pestanias y cuales casillas. Responde la posicion; no responde la marca.
* **Veredicto: `keep with a note`.**

#### `darkside_S3` — nota → **`keep with a note`**
* **Objecion previa (K1):** los cinco switches llevan la perilla en `O`, que es `LEVELS[error]`, y la ley del asiento nombrado no lo veia porque miraba `switch.indicator`.
* **Que cambio** (inc49 + inc52 + inc53):

  ```
  b559e92  notify on overdue  ▬▬O     sound  O──     danger zone  ◦ delete every completed task
  b559e92  ▬ ØDelete allØ ▬
  f1508ad  notify on overdue  ▬▬◎     sound  ◎──     danger zone  ▔ delete every completed task
  f1508ad  ▬ ▚Delete all▞ ▬
  ```
* **Estado: RESPONDIDA en el asiento y en la ley.** `O` (`LEVELS[error]`) ya no aparece en ningun control de darkside; `MEANING_AT_A_NAMED_SEAT` cubre ahora `switch.knob`, `checkbox.knob` y `radio.knob`; el `DANGER_FORM` dejo de ser `Ø` (que era la pared invalida) y es la hachura `▚▞`, que es una forma propia. **Criterio observable:** en la fila 6, decir si `◎──` significa «apagado» o «error en este ajuste» — ahora responde, porque `◎` no significa nada mas que «la perilla esta aqui».
* **Objecion nueva:** `▔` es el `FIELD_LEAD` de las seis filas del panel de detalle de `S1`/`S4` **y** el abridor del caption del boton destructivo de esta pantalla (f19). **Criterio:** decir si la fila 19 es un caption o una fila de campo. La fila 20 tiene `▬ … ▬`, distinta; la 19 abre como un valor de detalle.
* **Veredicto: `keep with a note`.**

#### `darkside_S4` — keep → **`keep`**
* **Que cambio:** `ØDeleteØ` → `▚Delete▞`, los leaders `◦` → `▔`, la pestania `(O)` → `(●)`.
* **La nota de la segunda ronda queda RESUELTA POR RULING:** `▊` (`CUR`) contra `▮` (foco) es un salto de **peso**, y peso es uno de los cuatro canales que la ruling D nombra; inc53 lo escribio como aceptado con su razon.
* **Veredicto: `keep`.**

#### `darkside_S5` — keep → **`keep`**
* Solo cambio la pestania (`(O)` → `(●)`). `· / o / O` sigue siendo monotona por area.
* **Nota que la ronda deja abierta y que inc57 nombro sin arreglar:** `Darkside.SPIN = (".", "o", "O", "o")` es la misma coleccion una familia mas alla, ningun `SPIN` de ningun lenguaje esta censado, y el spinner de esta pantalla respira una vez por frame.

#### `darkside_S6` — keep → **`keep`**
* Solo cambio la pestania. Los seis platos `#737373` con tinta `#121212` siguen siendo la respuesta mas limpia del corpus a *«el acento marca interactividad y nada mas»*: el match es un agujero abierto en el color del propio texto.

---

### 2.6 solari

`LEVELS "OK "/DLY/CNX` · `REQUIRED ▮` · `DANGER ▀▄` · `CUR ▼` · `SEAM/FIELD_LEAD ▁` · `MATCH reverse {ink}`.

#### `solari_S1` — nota → **`keep with a note`**
* Frame identico. Cada tarea gasta dos filas (la fila y su costura): en 32 filas caben seis de dieciseis y `GATE DONE 07` aparece con cabecera y nada debajo. La costura es doctrina; el coste es la mitad de la superficie.

#### `solari_S2` — nota → **`keep with a note`**
* Frame identico. `▮` aparece tres veces y dos son la respuesta a «senala los campos obligatorios»; la tercera es el caret, descartable por posicion. La reserva sigue admitida en `spec.md` §11.5 (*«naught and solari have no unspent cell left»*), y `rework-5c` no toco solari.
* **Veredicto: `keep with a note`.**

#### `solari_S3` — keep → **`keep`**
* Frame identico. Sigue siendo el unico switch del corpus legible con todos los glifos borrados (aleta + relleno + palabra).

#### `solari_S4` — nota → **`keep with a note`**, y la nota se reescribe entera
* **Objecion previa (C3):** *«la banda se sigue comiendo exactamente el gate que el modal nombra»* (`3 tasks will be removed from BACKLOG`), sus dos tareas y la cabecera `GATE DOING 04`, y deja una costura huerfana.
* **Que cambio** (inc55, ruling F):

  ```
  b559e92 f04  (vacia; la banda arrancaba aqui)
  f1508ad f04     GATE BACKLOG 05   STATUS  PROJ  PRI     DETAIL  FIX LOGIN REDIRECT
  f1508ad f05      21  AUDIT THE THEME TOKENS      ON TIME  LOW
  f1508ad f07      30  DROP THE LEGACY SHIM        ON TIME  NORM
  f1508ad f11  Delete 3 tasks?
  f1508ad f14  ▔  ▀Delete▄  ▔   ▁   Cancel   ▁
  ```
* **Estado: RESPONDIDA. El frame honra la ruling F al pie de la letra:** `GATE BACKLOG 05` y sus dos salidas estan en pantalla y su bloque es byte a byte el de `solari_S1`. El criterio *«de que gate se borra»* tiene respuesta por primera vez en tres rondas.
* **Objecion nueva, y es la que empeoro:** la banda ahora se come **la cabecera `GATE DOING 04` entera y tres de sus cuatro tareas**, y la cuarta, `14  REWRITE THE ONBOARDING` (fila 17), queda bajo la unica cabecera que hay encima de ella, que es `GATE BACKLOG 05`. **El frame afirma algo falso**: presenta una tarea de `DOING` archivada en `BACKLOG`. La costura huerfana de la fila 16 es el coste que inc55 declaro por escrito; **la tarea mal archivada no lo es**. **Criterio observable:** en `solari_S4`, decir a que gate pertenece `REWRITE THE ONBOARDING`. La respuesta que da el frame es la equivocada, no ninguna — que es peor que no responder.
* **Segunda objecion nueva, tambien declarada por inc50:** las filas 11-14 perdieron el aire; `Delete 3 tasks?`, el cuerpo y los botones van seguidos, separados solo por tier.
* **Veredicto: `keep with a note`.** El duenio es **C3'**, `Solari.band_head` / `schedule_foot`: la banda cabe entre dos gates, y hoy elige el hueco por indice y no por frontera.

#### `solari_S5` — nota → **`keep with a note`**
* Frame identico. La sparkline de dieciseis digitos sigue cumpliendo DATAVIZ 1 y perdiendo la tarea; el log `OK / DLY / CNX` sigue siendo el mejor de los once por un margen amplio (tres palabras, cero glifos, legible con el color quitado y sin fuente monoespaciada).

#### `solari_S6` — nota → **`keep with a note`**
* **Objecion previa (C6):** la cabecera recasea la consulta (`QUERY 'RE'` contra `re`) y el estado vacio dice `NO DEPARTURES` para «la busqueda no encontro nada».
* **Que cambio:** nada.
* **Estado: en pie, y ahora con un gemelo** — `ledger_S6` dice `nil balance` para lo mismo (§2.11). C6 pasa de un lenguaje a dos, y en los dos el estado vacio de la busqueda es el estado vacio del **tablero**, reutilizado.
* **Veredicto: `keep with a note`.**

---

### 2.7 blueprint

`LEVELS "  "/╌╌/━━` · `REQUIRED ═` (inc60) · `DANGER ━━` · `CUR ┌` · `FIELD_LEAD ·─` · `MATCH bold {ink}`.
**inc60 le dio su primer incremento: doce marcas donde el docstring decia diez.**

#### `blueprint_S1` — nota → **`keep with a note`**
* **Objecion previa:** ningun frame del corpus renderiza el mood `alert`, asi que el mecanismo firma del lenguaje esta asertado en un test y no en ninguna imagen.
* **Que cambio:** nada en `S1`.
* **Estado: RESPONDIDA POR RULING G, y no aqui.** inc56 puso el mood `alert` en la hoja `S2` y solo ahi. Asi que el knockout esta en una imagen — **en el formulario, no en el tablero**, que es la pantalla donde la ley de primera fijacion tiene sentido.
* **Objecion nueva (C10):** `blueprint_S1` dice `├ CLEAR ┤` y `blueprint_S2` dice `├ OVERDUE ┤` **sobre el mismo tablero sembrado**. inc56 lo declara: *«the same seeded board is now `alert` on S2 and `clear` on the other five … a real cost, not a rounding error»*. **Criterio observable:** leer el bloque de estado de `S1` y el de `S2` y decir si el tablero tiene una tarea vencida. Dos respuestas opuestas.
* **Veredicto: `keep with a note`.**

#### `blueprint_S2` — rework → **`keep with a note`**
* **Objecion previa:** **(a)** el campo invalido lleva `━`, que es `DANGER_FORM` y `LEVELS[error]`; **(c)** `├` es a la vez `REQUIRED` y el terminador de apertura de toda cota (censo `├ [7 families]`, roster del abridor 6).
* **Que cambio** (inc52, inc56, inc60), y son cuatro filas:

  ```
  b559e92  title├   ╞Fix login╪ redirect╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╡      due├   ━12/09/26·…·━
  f1508ad  title═   ╞Fix login╪ redirect───────────────╡      due═   ╲12/09/26·…·╲
  b559e92  ├ CLEAR ┤          f1508ad  ├ OVERDUE ┤   (invertido, el knockout del corpus)
  ```
* **Estado: (a) RESPONDIDA por ruling C** (`╲` es la textura REFUSED, no el `DANGER_FORM`). **(c) RESPONDIDA por inc60:** la obligacion se muda a `═`, un run doblado, y *«los terminadores son cromo y nada mas»*. `MEANING_AT_AN_OPENER["blueprint"]` 12 → 0. **Y la ruling G esta entregada aqui:** `├ OVERDUE ┤` invertido es el unico knockout del corpus y por primera vez esta en una imagen.
* **Objecion nueva 1:** `═`, `╞` y `╡` **estan en la misma fila 3** y las tres llevan el horizontal doble. **Criterio observable:** en la fila 3, tapar las palabras y decir cual de las tres marcas dice «esto es obligatorio». El vertical de los tees lo responde; el trazo doble no.
* **Objecion nueva 2, y es la mas dura de blueprint:** la fila 6 es `━━ expected YYYY-MM-DD ╌╌╌╌…╌` — **50 `╌`, que son `LEVELS[warn]`, extendiendo hasta el margen la fila que abre con `━━`, que es `LEVELS[error]`.** Es `Blueprint.ERROR_FILL`, y `inc60.md` lo llama *«the sharpest thing inc60 leaves open»*: dos severidades en una fila, y ninguna ley y ningun censo lo alcanza porque esta fuera de `PART_GLYPHS`. Recuento del frame: `╌` × 61 contra `━` × 2.
* **Veredicto: `keep with a note`.**

#### `blueprint_S3` — rework → **`rework`**
* **Objecion previa (K4/L3-b):** encendido y apagado difieren en una celda de hairline (`├─┤` contra `├┤·`), y ninguna ley compara dos estados de un mismo `part`.
* **Que cambio** (inc60): `sync to remote  ├╎╌` → `├╎┈`, una celda.
* **Estado: en pie, y con un caso mas.** Hoy la pantalla distingue **tres** cosas por cuenta de guiones: `╌` (warn / select apagado), `┄` (extension muerta), `┈` (leader muerto). `inc60.md` lo dice: *«tres horizontales de guiones distinguidas por CUENTA DE GUIONES (2, 3, 4) … a un cell de 12 px se le esta pidiendo al lector que cuente guiones»*. **Criterio observable:** en `blueprint_S3`, tapar las etiquetas y decir cuales de los cinco switches estan encendidos y cual esta muerto. `├─┤` contra `├┤·` contra `├╎┈` a 12 px es un trazo, un trazo mas corto y un trazo punteado.
* **Objecion nueva (C9):** la fila 18 es `DANGER ZONE ·──────…─── delete every completed task` — el caption del control destructivo esta dibujado **exactamente como una fila de campo** (`FIELD_LEAD = "·─"`), byte a byte como `OWNER ·──────… jav201` en `blueprint_S4` f10. **Criterio:** decir si `delete every completed task` es un caption, el valor del campo `DANGER ZONE`, o un control. Es la objecion que la primera ronda le cerro a `industrial_S3` y a `darkside_S3`, viva en un lenguaje que nadie habia juzgado hasta la ronda dos.
* **Veredicto: `rework`.** El eje incumplido: **K4** — dos estados de un `part` sin ninguna ley que los compare, y ahora tres.

#### `blueprint_S4` — rework → **`keep with a note`**
* **Objecion previa (C1):** `screens.s4_blueprint` construia el destructivo con `knockout_cell(" DELETE ")` en vez de `button(..., FOCUSED, danger=True)`, asi que perdia sus paredes, su `DANGER_FORM` y su foco. *«Leyendo solo el `.txt`, del confirm sale un boton y es el seguro.»*
* **Que cambio** (inc54, ruling C1):

  ```
  b559e92                              DELETE    ├  CANCEL  ┤
  f1508ad                             ╞ ━DELETE━ ╡   ├  CANCEL  ┤
  ```
* **Estado: RESPONDIDA.** `╞ ╡` son las paredes enfocadas del lenguaje (las mismas de `╞Fix login╪…╡` en `S2`, que es lo correcto: foco es foco), `━` es el `DANGER_FORM`, y el knockout sigue en el `.svg`. **Criterio observable:** leyendo solo el `.txt`, senialar los botones del confirm. Salen dos, y el peligroso es el mas pesado. Respondido.
* **Lo que queda, y esta declarado:** el asiento destructivo paso de 8 a 12 celdas; a 100 columnas dentro de un overlay de 60 eso es aire, **a una medida mas estrecha las dos respuestas serian lo primero en chocar, y nada en este repo renderiza `S4` por debajo de 100** (`inc54.md` §7: *«untested rather than safe»*). Y el modal se sigue delimitando con **cuatro esquinas sueltas** (`┌ … ┐` en la fila 11, `└ … ┘` en la 19) y ningun lado, que es doctrina escrita de blueprint (*«a containing box here is unconstructable»*) y sigue costando el criterio «decir donde acaba el modal».
* **Veredicto: `keep with a note`.**

#### `blueprint_S5` — nota → **`keep with a note`**
* **Objecion previa (L6):** `━` en la fila 5 (pico de la traza) significa a la vez «pico» y «error», y en la segunda ronda habia acumulado cuatro papeles.
* **Que cambio** (inc52, inc60), y es en dos direcciones:

  ```
  b559e92  09:41:02 ·· board loaded  16 tasks  4 projects
  f1508ad  09:41:02    board loaded  16 tasks  4 projects
  ```
* **Estado: la objecion MEJORO en un eje.** `━` perdio las dos paredes del campo invalido (inc52 las mando a `╲`), asi que baja de cuatro papeles a tres: error, danger (exento por `DANGER_IS_THE_TOP_RUNG`, con cita) y pico de sparkline.
* **Objecion nueva, y es la que empeoro (L7):** inc60 mando `LEVELS["info"]` **al aire**. Seis de las ocho filas del log no llevan ninguna marca de severidad. **Criterio observable:** en `blueprint_S5`, senialar las filas del log que llevan una severidad. Dos responden (`╌╌`, `━━`); las otras seis son indistinguibles de una fila sin clasificar. La escalera dejo de ser monotona por cuenta y paso a ser «nada, algo, mucho», donde «nada» es tambien lo que dibuja una fila que nadie clasifico.
* **Y la cita del precedente es el problema:** `inc60.md` asienta el cambio *contra `Ledger.LEVELS`* — una declaracion que **ninguna ronda habia juzgado nunca**. Ver §7.
* **Veredicto: `keep with a note`.**

#### `blueprint_S6` — keep → **`keep`**
* **Que cambio:** el guia del campo de consulta, `╌` → `─` (inc60, el papel EDITED del campo).
* `#eef4f8` contra `mut #7fa8c4` sigue siendo 2,28:1 mas el peso: dos canales. La nota menor de la segunda ronda (`CUR = ┌` se dibuja tambien en `#eef4f8`) se mantiene sin engordar.
* **Veredicto: `keep`.**

---

### 2.8 naught — primera lectura

`LEVELS ◦◦/∙◦/∙∙` · `REQUIRED ⊛` (inc61) · `DANGER ∙∙` · `CUR ●` · `FIELD_LEAD ◦` (= `NA.OFF`) ·
`MATCH bold {ink}`. Rampa de carga de cinco peldanios `⋅ ◦ ∙ ◉ ●`.
**Exenciones vivas:** `DANGER_IS_THE_TOP_RUNG` (`∙∙`, desde inc45) y `THE_GROUND_IS_NOT_A_MARK`
(`◦`, concedida en inc61, **tasada en `GROUND_EXEMPTION_IS_WORTH = (7, 2)`**).

#### `naught_S1` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** *«la reticula CUENTA; el pixel se CARGA»* (inc61) — que cuantos hay encendidos sea la senial y que la carga sea el canal.
* **Lo que ensenia el frame:** el compromiso se cumple en el tablero. Cada tarjeta lleva un latigo de ocho celdas (`∙∙◦◦◦◦◦◦` = 2, `∙∙∙∙∙∙◦◦` = 6) y la lectura es una cuenta, no un color ni un tamanio. Es de las cosas mas limpias del corpus.
* **Objecion mas fuerte (K5):** la fila 13 es la barra de progreso `◦ ∙∙∙∙∙∙∙∙∙∙∙∙∙ ◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦  44%` — **trece `∙` seguidos, que son `LEVELS[error]` y el `DANGER_FORM` byte a byte.** `∙` aparece 70 veces en este frame; ninguna significa peligro y ninguna significa error. La fila 23 usa `∙` otra vez como leader de la tarea vencida (`∙ Rate-limit the API … 2d!`), que si es severidad.
* **Criterio observable:** en `naught_S1`, senialar las celdas que significan «error». Hay 70 candidatas, dos de ellas (fila 23) son la respuesta, y trece seguidas de la fila 13 son un porcentaje.
* **Segunda:** la fila 31 es `view ·●●●●······· 3-10 of 23` — `·` (U+00B7) contra `∙` (U+2219, la celda de peligro) contra `◦` (el suelo) en el mismo frame. `· ∙` **si** esta en la tabla `HOMOGLYPHS` del censo, y el censo lee naught con **cero** filas de homoglifo, porque el pager se dibuja fuera de `PART_GLYPHS`.
* **Veredicto: `keep with a note`.**

#### `naught_S2` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** que la carga sea el canal y que ruling D (*«count, weight, position, direction; diameter alone is not a channel»*) valga para el alfabeto entero de este lenguaje y no solo para los pares que alguien escribio en una lista.
* **Lo que ensenia el frame:** nueve marcas circulares en 18 filas.

  ```
  f04   title⊛        ○Fix login◉ redirect◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦○
  f06   due⊛          ◑12/09/26⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅◑
  f09   priority      ○ low  ○ norm  ⊙ high
  f11   tags          ◦ api  ◉ ui  ◉ urgent
  f17                 ⋅    Save    ⋅   ◦   Cancel   ◦
  ```
* **Objecion mas fuerte:** **el radio y el checkbox de este formulario se distinguen solo por el diametro y el relleno de un circulo, y estan a dos filas.** Elegido `⊙` contra marcado `◉`; sin elegir `○` contra sin marcar `◦`. Ninguno de los dos pares esta en la lista de cinco de `HOMOGLYPHS`; los cuatro marcan **cero** en el roster de homoglifos, y la ruling D dice literalmente que el diametro solo no es un canal.
* **Criterio observable:** en `naught_S2`, tapar la columna de etiquetas y decir cual de las dos filas de opciones es una eleccion unica y cual son casillas independientes. Sin respuesta: los dos controles son un anillo con o sin punto dentro, sin pozo, sin palabra y sin posicion que los separe.
* **Segunda:** el boton deshabilitado abre con `⋅`, que es **el papel del campo invalido de la fila 6**, veintiseis celdas. Censo `⋅ [7 families]`. Es la exclusion de la RUNA que `_invalid_marks` hace por nombre desde inc52 y que el censo no hace: la discrepancia que `spec.md` §15.5 nombra como *«la unica fila que le queda a cinco lenguajes»*.
* **A favor, y hay que decirlo:** `⊛` es la mejor marca de obligacion del corpus junto a `†` de ledger — un asterisco dentro de un anillo no se parece a nada mas en la pantalla; y `⋅` contra `◦` separa correctamente el boton muerto del boton vivo, que es exactamente lo que swiss lleva tres rondas sin hacer.
* **Veredicto: `rework`.** El eje incumplido: **ruling D aplicada al alfabeto propio de naught** — el lenguaje no tiene canal entre su radio y su checkbox, y su instrumento no puede verlo porque `HOMOGLYPHS` es una lista de cinco pares fijos (K2).

#### `naught_S3` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el mismo, y ademas *«ningun asiento de control dibuja `NA.ON`»* (inc61).
* **Lo que ensenia el frame:** los switches son **lo mejor de esta pantalla** — `⊖⊖◉` encendido, `◉◦◦` apagado, `◌⋅⋅` muerto. La perilla se mueve de extremo (posicion) y la pista cambia (`⊖⊖` contra `◦◦` contra `⋅⋅`): dos canales, sin palabras.
* **Objecion mas fuerte (K5):** la fila 16 es `row density  ∙∙∙∙∙∙∙∙∙◉◦◦◦◦ 70` — **la parte viva del slider son nueve `∙`, el `DANGER_FORM` byte a byte, cuatro filas encima de `◦ ∙Delete all∙ ◦`.** Es la situacion que el brief de la ruling A mando medir antes de decidir (*«an exemption must leave the opener of a control distinct from an error rung in the frame»*), inc61 la midio para los controles y **el slider quedo fuera del conjunto B del censo por peticion del operador**.
* **Criterio observable:** en `naught_S3`, tapar las palabras y decir cual de las dos tiradas de `∙` es un valor y cual es un boton irreversible. Nueve celdas contra dos, cuatro filas de distancia, misma celda.
* **Segunda:** la fila 19 es `danger zone delete every completed task ◦◦◦◦…` — **el caption y su etiqueta van pegados en una sola frase sin separador**, y despues el relleno del guia hasta el margen. Es C9 con otra forma.
* **Veredicto: `keep with a note`.**

#### `naught_S4` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** que el `DANGER_FORM` sea reconocible como tal en la unica pantalla del barrido donde hay un acto irreversible detras.
* **Lo que ensenia el frame:**

  ```
  f13   ∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙  (100 celdas)
  f14   Delete 3 tasks?
  f19   ○  ∙Delete∙  ○   ◦   Cancel   ◦
  f20   ∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙  (100 celdas)
  ```
* **Objecion mas fuerte:** **`∙` aparece 237 veces en este frame y dos de ellas significan «esto destruye datos».** Las otras 235 son las dos reglas de 100 celdas con las que la banda se delimita y el tablero de detras. Es exactamente la objecion que la primera ronda le hizo a `solari_S2` (*«`▁` aparece mas de sesenta veces y dos de ellas son la respuesta»*) a cuatro veces la magnitud, en un confirm destructivo en vez de en un formulario.
* **Criterio observable:** en `naught_S4`, senialar las celdas que significan «irreversible». 237 candidatas, dos correctas, y las 200 mas grandes y mas contiguas de la pantalla son cromo.
* **Segunda:** `○  ∙Delete∙  ○` — el anillo de foco del boton irreversible es `○`, que en `S2` es **la pared del campo normal y el radio sin elegir**. Y `◦   Cancel   ◦` pone las paredes del boton seguro sobre `NA.OFF`, el suelo, que se dibuja miles de veces: `Cancel` esta efectivamente sin paredes.
* **Veredicto: `rework`.** El eje incumplido: el `DANGER_FORM` del lenguaje es su propio marco de modal, y es el unico caso del corpus donde la marca de peligro se gasta 200 veces en la misma pantalla en la que hay que reconocerla.

#### `naught_S5` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** *«cuantos hay encendidos es la senial»*, en la pantalla donde la severidad es el trabajo.
* **Lo que ensenia el frame:** `◦◦ / ∙◦ / ∙∙` es **monotona por cuenta y por nada mas**: cero, uno y dos puntos cargados. Con el color quitado sigue funcionando. Es la escalera bien hecha, y es la razon por la que este frame no es un rehacer.
* **Objecion mas fuerte:** el peldanio `info` es `◦◦`, que es **la celda del suelo de este lenguaje**, dibujada 99 veces en la fila 3 de esta misma pantalla y miles de veces en `S1`. **Criterio observable:** en `naught_S5`, decir si la fila `09:41:02 ◦◦ board loaded` lleva una severidad o si esas dos celdas son fondo. La respuesta correcta es «lleva `info`», y la evidencia es que estan en la columna de severidad, no la marca.
* **Segunda:** la fila 6 es `rate ⡀⡄⡀⡄⡀⡄⡇⡄⡀⡀⡄⡄⡄⡀⡄⡄` — **la sparkline esta dibujada en braille**, que es el alfabeto entero de instrument y de prism, en un lenguaje cuya identidad es una reticula de circulos. Ver el gemelo invertido en `prism_S5`.
* **Veredicto: `keep with a note`.**

#### `naught_S6` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el tier de estilo del match (`bold {ink}`) y la coherencia del estado vacio.
* **Lo que ensenia el frame:** el `.svg` pinta 6 × `<text fill="#f5f5f5" font-weight="bold">re</text>` contra un cuerpo `#8a8a8a`: **3,17:1 mas el peso**, el mejor de los cuatro kits de `bold` medidos aqui. Y el estado vacio de las filas 16-20 es una carita triste dibujada en la reticula (`◦◦∙◦◦◦∙◦◦` / `◦∙◦◦◦◦◦∙◦` / `◦◦∙∙∙∙∙◦◦`), que es el compromiso del lenguaje aplicado a un dibujo. Bien.
* **Objecion mas fuerte:** la fila 23 es `enter∙run   esc∙close   ^p∙prev   ^n∙next` — **el separador de la barra de teclas es `∙`, el `DANGER_FORM`, cuatro veces.** Es la unica pantalla del corpus donde una marca de significado se usa como puntuacion de cromo.
* **Criterio observable:** enseniar `∙` fuera de contexto y preguntar que significa. En este lenguaje: error, peligro, el relleno del slider, la mitad de la barra de progreso, el marcador de vencido, la cara del estado vacio y el punto medio entre `esc` y `close`.
* **Veredicto: `keep with a note`.**

---

### 2.9 corgi — primera lectura

`LEVELS ▁▁/▄▄/██` · `REQUIRED ▀` · `DANGER ██` · `CUR ▐` · `FIELD_LEAD ""` (aire) · `MATCH bold {ink}`.
inc58: *«el banco de segmentos es la lectura, el metal fresado es el panel»*.
**Exencion viva:** `DANGER_IS_THE_TOP_RUNG` (`██`).

#### `corgi_S1` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** la frontera que inc58 declaro — dos registros, el banco conducido (`▁ ▄ ▀ █`) para los significados y la rampa de sombra mas los cuadrantes para los controles.
* **Lo que ensenia el frame:** el compromiso **no llega a esta pantalla**. `corgi_S1` no dibuja ningun control: dibuja cromo, y el cromo esta hecho con el banco.

  ```
  f04-f30   ...  █ [D] D E T A I L  FIX LOGIN REDIRECT      (el rail, 25 celdas de alto)
  f13       ▄▄ ▄▄ ▄▄ ▄▄ ░░ ░░ ░░ ░░ [ 44%]                  (el medidor)
  f18-f23   ██    ██  /  █        █  /   ██████             (el mascot)
  f31       view ██ ░░ ░░ ░░ 3-10 of 23                     (el pager)
  ```
* **Objecion mas fuerte (K5):** **`█` aparece 47 veces en este frame y ninguna significa peligro ni error.** Veinticinco de ellas son la pared entre el tablero y el panel de detalle, dieciocho el mascot y una la pagina actual del pager. En `corgi_S3` `█` aparece **dos** veces y son `█Delete all█`, y en `corgi_S5` tres, dos de ellas `██ rate limit hit`. El lector aprende `█` en `S1` como «aqui acaba el panel» y se lo encuentra en `S3` como «esto no se puede deshacer». `spec.md` §15.7 lo nombra por escrito (*«`Corgi.PANE_RULE = "█"` … it is unmeasured, which is a different complaint»*) y no lo arregla.
* **Criterio observable:** en `corgi_S1`, senialar las celdas que significan «irreversible». Cuarenta y siete candidatas, cero correctas, y la mas alta y contigua de las cuatro es un tabique.
* **Segunda:** el medidor de la fila 13 esta lleno con `▄▄`, `LEVELS[warn]`, y vacio con `░░`, que es **la pared del campo invalido de `corgi_S2`**. Un porcentaje de avance dibujado con el peldanio de advertencia y la marca de rechazo.
* **Veredicto: `rework`.** El eje incumplido: es **una constante**, `Corgi.PANE_RULE`, y gasta la marca mas fuerte del lenguaje 25 veces en la pantalla que el usuario mira mas tiempo.

#### `corgi_S2` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** los dos registros de inc58, en la pantalla donde el incremento trabajo.
* **Lo que ensenia el frame:** el incremento hizo su trabajo y se ve.

  ```
  f04   title▀        ▛▛Fix login▌ redirect▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▜▜
  f06   due▀          ░░12/09/26··························░░
  f11   tags          ▒▒ -- api  ▓▓ ON ui  ▓▓ ON urgent
  f17                 ··   Save   ··   ▒▒  Cancel  ▒▒
  ```
  El campo invalido tiene **paredes mas claras y papel mas claro** que el normal (`░░`+`·` contra `▛▛`/`▜▜`+`▒▒`): un canal de peso ancho y correcto. Las casillas llevan **palabra ademas de marca** (`-- api`, `ON ui`), que junto con ledger es el mejor checkbox del corpus. El boton muerto (`··`) y el vivo (`▒▒`) se separan.
* **Objecion mas fuerte:** la fila 9 es `priority  ▒◦ low  ▒◦ norm  ▒● high` — **las perillas del radio son `◦` y `●`, dos circulos, y corgi no tiene circulos.** El lenguaje declaro dos registros (banco conducido y metal fresado) y esta fila esta en un **tercero** que nadie declaro. Los circulos son el alfabeto entero de naught, y `● ◦` no aparece en ninguna otra fila de ninguna pantalla de corgi salvo aqui y en el `radio.knob`.
* **Criterio observable:** en `corgi_S2`, decir a que registro pertenece la fila 9. No pertenece a ninguno de los dos que el kit nombra.
* **Segunda:** las paredes del `Save` deshabilitado son `·`, que es **el papel del campo invalido de la fila 6**, veintiseis celdas. Censo `corgi · [7 families]`: es la exclusion de la runa, quinta lengua.
* **Veredicto: `keep with a note`.**

#### `corgi_S3` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el mismo, en la pantalla que la propia ruling A mando medir antes de decidir la exencion en bloque.
* **Lo que ensenia el frame:** los switches son excelentes — `▓▓ ▙▟ ON`, `▙▟ ▒▒ --`, `╳╳ ·· --`: pista, perilla que se mueve de lado y **palabra**. Tres canales. El boton destructivo (`▒▒█Delete all█▒▒`) tiene el caption desnudo encima (`DANGER ZONE delete every completed task`), que es lo correcto.
* **Objecion mas fuerte (K5):** la fila 16 es `row density  ▄▄ ▄▄ ▄▄ ▙▟ ▁▁[70]` — **el eje del slider esta dibujado con `▄▄` y `▁▁`, que son los peldanios `warn` e `info`, y en `corgi_S5` esas dos celdas son los leaders de severidad del log.** Cuatro filas mas abajo, `█Delete all█`. `spec.md` §15.4 lo declara por escrito (*«`▁` y `▄` siguen siendo los peldanios info y warn de corgi y siguen siendo el eje y el relleno de su slider»*) y lo deja fuera del conjunto B **por peticion del operador**.
* **Criterio observable:** en `corgi_S3`, tapar el `[70]` y decir si la fila 16 es un valor o cinco calificaciones de severidad.
* **Veredicto: `keep with a note`,** porque el frame **honra la ruling A** (los asientos de control se movieron, el slider quedo explicitamente fuera del alcance). La objecion es contra el alcance, no contra el frame: §7.

#### `corgi_S4` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** que un confirm destructivo deje al operador saber donde esta y sobre que actua. Es el criterio que la primera ronda declaro *«el defecto mas grave de los 42»* para `solari_S4` y que cuatro lotes han estado corrigiendo.
* **Lo que ensenia el frame:** el frame entero.

  ```
  f01-f13   (trece filas vacias)
  f14       Delete 3 tasks?
  f16       3 tasks will be removed from BACKLOG.
  f17       This cannot be undone.
  f19       ▛▛ █Delete█ ▜▜   ▒▒  Cancel  ▒▒
  f20-f32   (trece filas vacias)
  ```
  `corgi_S4.svg` contiene **siete** runs de texto en total.
* **Objecion mas fuerte:** **es el unico de los once cuyo `S4` pierde la fila 1.** Medido sobre los once: naught, instrument, swiss, industrial, nord, darkside, prism, ledger, solari y blueprint conservan la tira de modos; corgi la borra, y con ella el masthead, la regla, el tablero, el panel de detalle, el pager y el propio marco del modal. La segunda ronda escribio *«los siete lenguajes conservan ya la fila 1 en `S4`»*; con los once en la mesa, la frase es falsa.
* **Criterio observable:** con `corgi_S4` delante, decir **en que modo esta la aplicacion** y **de que gate se borra**. Ninguna de las dos es respondible, que es palabra por palabra el criterio que hizo `rework` a `solari_S4` en la primera ronda. Y este es peor: solari perdia ocho filas, corgi pierde treinta.
* **Segunda:** `▛▛ █Delete█ ▜▜` — el anillo de foco del boton irreversible es el par de paredes del **campo de texto normal** de `S2` y del campo de consulta de `S6`.
* **Veredicto: `rework`.** El eje incumplido: **C8**, composicion. El confirm no es una banda ni una caja: es un borrado de pantalla.

#### `corgi_S5` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el banco conducido como device de severidad.
* **Lo que ensenia el frame:** `▁▁ / ▄▄ / ██` es **la mejor escalera de severidad del corpus con el color quitado**: un segmento a tres alturas, monotona, sin depender de la forma, del tamanio ni del matiz. Junto con `naught` (cuenta) y `solari` (palabras) es una de las tres que sobreviven enteras a la escala de grises.
* **Objecion mas fuerte (L6, tercer lenguaje):** la fila 6 es `rate ▄▆▄▆▄▆█▆▄▄▆▆▆▄▆▆` — **la sparkline usa `▄` y `█`, el peldanio de advertencia y el de error, seis filas encima del log que los usa como severidad.** Es el mismo defecto que la primera ronda le encontro a `blueprint_S5` y la segunda a `swiss_S5`.
* **Criterio observable:** decir si un `█` de la fila 6 significa «pico» o «error». Y la fila 4 (`EVENTS/S ▄▄ ▄▄ ▄▄ ▁▁ ▁▁[ 5]`) lo repite con `warn` e `info`.
* **Veredicto: `keep with a note`.**

#### `corgi_S6` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el tier de match y la notacion de teclas.
* **Lo que ensenia el frame:** el `.svg` pinta 6 × `bold` en `#f2f2f2` contra un cuerpo `#9a9a9a`, **2,51:1**. Y la fila 24, `[enter] RUN   [esc] CLOSE   [^p] PREV   [^n] NEXT`, usa la misma notacion de corchetes que las pestanias (`[1]BOARD`) y los codigos de tarjeta: **una convencion, aplicada en tres sitios**. Es lo mejor que hace este lenguaje.
* **Objecion mas fuerte:** el mascot del estado vacio (filas 16-21) esta dibujado con **18 `█`**, la marca de destruccion, debajo de un campo de busqueda que no encontro nada. `corgi_S1` hace lo mismo. Es K5 otra vez y es el caso mas benigno de los cuatro.
* **Criterio observable:** el mismo de `S1`: senialar las celdas que significan «irreversible» en `corgi_S6`. Dieciocho candidatas, cero correctas.
* **Veredicto: `keep with a note`.**

---

### 2.10 prism — primera lectura

`LEVELS ⣀⣀/⣤⣤/⣿⣿` · `REQUIRED ⡀` · `DANGER ⣿⣿` · `CUR ▸` · `FIELD_LEAD ⡀⡤⣶` · `MATCH bold {accent}`.
inc59: *«la brasa se lee desde ABAJO; un control se lee desde ARRIBA»*.
**Exenciones vivas:** `DANGER_IS_THE_TOP_RUNG` (`⣿⣿`) y `⡀` (`REQUIRED` × `field.leader`), **esta ultima
concedida por inc59 con la cita marcada como discutible por el propio incremento**.

#### `prism_S1` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** *«la brasa se lee desde abajo»* — que la rampa `⣀ ⣤ ⣿` sea monotona y que su direccion signifique lo mismo en toda la pantalla.
* **Lo que ensenia el frame:**

  ```
  f06-f11   project                       ⡀⡤⣶ Web      (seis filas de detalle)
  f13       ⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  44%
  f31       view ⠒⣿⣿⣿⣿⠒⠒⠒⠒⠒⠒⠒ 3-10 of 23
  ```
* **Objecion mas fuerte:** **la barra de progreso va al reves.** Doce `⣀` (la celda mas ligera) seguidos de quince `⣿` (la mas pesada), etiquetados `44%`: 12 de 27 es 44 %, asi que **lo hecho es la parte ligera y lo que falta es la pesada**. Los otros diez lenguajes hacen lo contrario en la misma fila del mismo frame (`darkside_S1`: `████████████▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ 44%`; `naught_S1`: trece cargados, dieciseis apagados). **Y prism se contradice a si mismo:** `prism_S5` fila 4 es `EVENTS/S ⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀ 5` — pesado primero — y `prism_S3` fila 16 es `⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70`, tambien pesado primero.
* **Criterio observable:** en `prism_S1` fila 13, tapar `44%` y decir que fraccion esta hecha. La lectura que da el frame es 56 %. En `prism_S3` y `prism_S5` la misma pregunta con las mismas celdas se responde al reves.
* **Segunda:** el guia de campo es `⡀⡤⣶` y **abre con `⡀`, que es `REQUIRED`**, en seis filas de detalle de solo lectura, ninguna de las cuales es obligatoria y todas las cuales tienen valor. La exencion existe por nombre (inc59) y el propio packet escribe que *«the frame does not bear it out»*. **Criterio:** en `prism_S1`, senialar los campos obligatorios. Seis filas abren con la marca de obligacion y ninguna de las seis es un campo.
* **Tercera:** el pager de la fila 31 dibuja la ventana actual con `⣿⣿⣿⣿`, `DANGER_FORM` y `LEVELS[error]` byte a byte. `⣿` aparece 31 veces en el frame y ninguna es peligro.
* **Veredicto: `rework`.** El eje incumplido: la direccion de la rampa **no es la misma en dos frames del mismo lenguaje**, y una de las dos es un porcentaje que el frame lee al reves.

#### `prism_S2` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** *«un control se lee desde ARRIBA»* (inc59), en la pantalla donde el incremento reescribio diez tablas.
* **Lo que ensenia el frame:**

  ```
  f04   title⡀        ⠿Fix login⡆ redirect⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠿
  f06   due⡀          ⣹12/09/26⠀⠀⠀⠀⠀…⠀⠀⣏
  f09   priority      ⠉⠉⠉ low  ⠉⠉⠉ norm  ⠉⢸⠉ high
  f11   tags          ⠿⠉⠿ api  ⠿⠀⠿ ui  ⠿⠀⠿ urgent
  ```
* **Objecion mas fuerte: el checkbox esta invertido.** El fixture marca `ui` y `urgent` y deja `api` sin marcar — se comprueba en los otros diez (`darkside`: `( ) api  (◎) ui  (◎) urgent`; `corgi`: `▒▒ -- api  ▓▓ ON ui`; `naught`: `◦ api  ◉ ui`). En prism, **las dos marcadas son `⠿⠀⠿`, el pozo VACIO, y la no marcada es `⠿⠉⠿`, con una marca dentro.** Se confirma en la declaracion: inc59 movio `checkbox.main` a `⠿⠉⠿` (el cuerpo, sin marcar) y `checkbox.knob` a `⠿⠀⠿` (la marca, marcado), y **no lo noto**.
* **Criterio observable:** en `prism_S2` fila 11, senialar los tags marcados. Todo lector que no haya leido el kit senialara `api`.
* **Segunda:** el papel del campo invalido es `⠀`, el **blanco braille**: el campo de fecha no tiene fondo visible y sus dos paredes, `⣹` y `⣏`, son imagenes espejo. Es la forma exacta de `] … [` que la primera ronda le hizo rehacer a nord (*«no se lee como un estado, se lee como un render roto»*), con la diferencia de que aqui el papel tambien desaparecio.
* **Tercera:** el radio sin elegir (`⠉⠉⠉`) es byte a byte el papel del campo normal de la fila 4, quince celdas.
* **Veredicto: `rework`.** El eje incumplido: **K4** — dos estados de un mismo `part` en el orden equivocado, y ninguna ley del corpus compara dos estados de un `part`.

#### `prism_S3` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el registro de inc59, en la pantalla que decidio que no habia exencion en bloque que dar.
* **Lo que ensenia el frame:** los controles se movieron y se ve — switch `⠿⠿⢸` / `⢸⠉⠉` / `⠈⠄⠄`, select `⠿mon ⣶⠿`, y el destructivo `⠿⠉⣿Delete all⣿⠉⠿` con la brasa dentro y el cromo fuera. La perilla se mueve de extremo. Bien.
* **Objecion mas fuerte (K5):** la fila 16 es `row density  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣀⣀⣀⣀ 70` — **nueve `⣿`, `DANGER_FORM` y `LEVELS[error]`, cuatro filas encima de `⣿Delete all⣿`.** `inc59.md` dice *«no exemption was drafted for prism»* y la razon que da es la fila del `S4`; el slider no entro en la cuenta porque el conjunto B lo excluye.
* **Criterio observable:** en `prism_S3`, tapar las palabras y decir cual de las dos tiradas de `⣿` es un valor y cual es un boton irreversible.
* **Segunda:** el caption del destructivo (f19) abre con `⡀⡤⣶`, el guia que empieza en `REQUIRED`. C9 con una tercera forma.
* **Veredicto: `keep with a note`,** porque el frame honra la ruling A en el alcance que la ruling tiene. La objecion es al alcance: §7.

#### `prism_S4` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** los bordes reservados para modales (doctrina §8 de prism) y la respuesta destructiva.
* **Lo que ensenia el frame:** **el tablero de detras esta entero** (filas 1-12 y 21-31), el modal esta cerrado por sus cuatro lados, y `⠿⠛ ⣿Delete⣿ ⠛⠿   ⠿⠉  Cancel  ⠉⠿` distingue las dos respuestas por la brasa dentro y por las paredes. Es la superposicion mejor construida de los cuatro lenguajes nuevos por un margen amplio, y la unica que compite con industrial y nord.
* **Objecion mas fuerte:** `⣿` aparece 18 veces en el frame; **dos son la respuesta destructiva y ocho son el mascot del estado vacio, tres filas por debajo del modal.** La marca de peligro y el dibujo del gato de la pantalla vacia son la misma celda, y estan a la vez en pantalla.
* **Criterio observable:** en `prism_S4`, senialar las celdas que significan «esto destruye datos». Dieciocho candidatas, dos correctas, y el grupo mas grande esta debajo del confirm.
* **Veredicto: `keep with a note`.**

#### `prism_S5` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** la rampa de brasa como device de severidad.
* **Lo que ensenia el frame:** `⣀⣀ / ⣤⣤ / ⣿⣿` es monotona por cuenta de puntos braille (2, 4, 8) **y** por area. Sobrevive a la escala de grises. Es de las tres o cuatro mejores del corpus.
* **Objecion mas fuerte:** la fila 6 es `rate ▂▅▂▅▂▅█▅▂▂▅▅▅▂▅▅` — **la sparkline esta dibujada con elementos de bloque en un lenguaje cuyo alfabeto entero es braille.** Es el gemelo invertido de `naught_S5`, que dibuja la suya en braille en un lenguaje de circulos: el compositor de sparkline reparte alfabetos sin preguntarle al kit, y se ve en los dos lenguajes que mas lejos estan de su alfabeto por defecto.
* **Criterio observable:** en `prism_S5`, decir a que lenguaje pertenece la fila 6. `█` no es una celda que prism declare en ninguna tabla.
* **Segunda, y a favor del frame:** aqui la rampa **se llena por lo pesado** (`⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀`), que es lo correcto y lo contrario de `prism_S1`.
* **Veredicto: `keep with a note`.**

#### `prism_S6` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el tier de match (`bold {accent}`) y la reserva del acento.
* **Lo que ensenia el frame:** el `.svg` pinta 6 × `<text fill="#2dd4bf" font-weight="bold">re</text>` contra un cuerpo `#8b98a5`.
* **Objecion mas fuerte:** **1,58:1 — el segundo peor del corpus, solo por encima del 1,36 de swiss.** Con el color quitado, el match de prism es peso y nada mas. Y `#2dd4bf` es exactamente la tinta del cursor `▸` **de la misma fila** (`y="108.3"`: `▸` en `#2dd4bf`, `re` en `#2dd4bf`) y exactamente el acento de match de instrument. **Criterio observable:** en la primera fila de resultado de `prism_S6`, decir cual de los dos runs en `#2dd4bf` es el cursor y cual es la coincidencia. Responde la posicion (columna 1 contra columna 3); no responde la tinta.
* **Segunda:** la fila 26 usa `⣶` como separador de la barra de teclas (`enter⣶run`), que es el tercer peldanio del guia de campo y el `DISCLOSE` del select. Es la misma clase de defecto que `naught_S6` y es mas benigna: `⣶` no es un peldanio de `LEVELS`.
* **Veredicto: `keep with a note`.**

---

### 2.11 ledger — primera lectura

`LEVELS "  "/"* "/"**"` · `REQUIRED †` · `DANGER ( )` · `CUR ▶` · `FIELD_LEAD ·` (= `LEAD`) ·
`MATCH underline {ink}`. inc61: *«ledger deja de escalonar su papel POR TAMANIO»*.
**El unico lenguaje del corpus con papel claro** (`ground #e9e1cf`), y por eso el unico al que E4 le
rompe los seis `.svg` (§0a).

#### `ledger_S1` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el libro mayor — que el guia de puntos, las reglas dobles y la columna de importe compongan una pagina que se lea como un asiento contable.
* **Lo que ensenia el frame:** lo compone, y bien. `1 BACKLOG ····· 5 entries`, `══════` bajo cada cabecera de gate, `nil balance` para el gate vacio, `│ doing │ 3d│` en columnas: es la pantalla mas legible de los cuatro lenguajes nuevos con las palabras tapadas.
* **Objecion mas fuerte:** la fila 4 es `1 BACKLOG ····································· 5 entries═══DETAIL ··········· Fix login redirect`. **Los dos paneles se tocan con tres `═` en la fila 4 y con `│` en las filas 5 a 30.** Ninguna otra fila de la pantalla usa `═` en esa columna, y `═` es en todas partes la regla bajo una cabecera de gate.
* **Criterio observable:** en la fila 4 de `ledger_S1`, decir donde acaba el panel izquierdo. La respuesta que da el frame es «en `═══`», que en cualquier otra fila significa «aqui empieza un gate».
* **Segunda:** el medidor de la fila 13 (`▪▪▪▪▪ ▪▪▪▪· ····· ·····  44%`) esta hecho con `▪`, que es **la marca de la pestania activa de la fila 1**, y con `·`, que es el guia de puntos que aparece cientos de veces en la pantalla.
* **Tercera (E4):** el `.svg` de este frame pinta `#1c1a15` sobre `#121212`. **Nada de lo anterior es visible en el artefacto.**
* **Veredicto: `keep with a note`.**

#### `ledger_S2` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** *«el orden de las llamadas es toda la notacion: `†` marca el asiento que hay que hacer, `‡` el que fue rechazado»* (la cita con la que inc61 exime el par).
* **Lo que ensenia el frame:**

  ```
  f04   title†        ▶Fix login▏ redirect───────────────│
  f06   due†          ‡12/09/26··························‡
  f07                 ** expected YYYY-MM-DD ·····························
  f11   tags          │ │ open   api  │×│ posted ui  │×│ posted urgent
  f17                 ╌    Save    ╌   │   Cancel   │
  ```
  El checkbox de la fila 11 lleva **marca y palabra** (`│×│ posted`): es, con corgi, el mejor del corpus. `†` es una marca de obligacion excelente y exclusiva.
* **Objecion mas fuerte:** **`†` y `‡` estan en la fila 6, a tres celdas, y son el mismo dibujo con un travesanio mas.** Es el par mas apretado de los once, y no esta en la lista de cinco de `HOMOGLYPHS`, asi que el roster de homoglifos lee **cero** para ledger. Formalmente la ruling D lo permite — la cuenta de travesanios es COUNT, y count es uno de los cuatro canales — pero **es un canal de dos pixeles y E2 dice que no se puede resolver desde el artefacto**, porque el `.svg` no lleva metrica de fuente. Y en este lenguaje ni siquiera se puede mirar (E4).
* **Criterio observable:** en `ledger_S2`, tapar las palabras y decir cual de las tres marcas de referencia dice «obligatorio», cual «rechazado» y cual «error». Son `†`, `‡` y `**`: tres marcas de la misma familia tipografica (llamada al pie) para tres cosas distintas, en cinco filas.
* **Segunda:** el campo enfocado abre con `▶`, que es `CUR` y el cursor del margen de `S1`, y **cierra con `│`, la regla de columna que en `S1` aparece unas cuarenta veces.** Censo `▶ [7 families]`. El boton `Cancel` de la fila 17 tiene las mismas paredes `│`.
* **Veredicto: `keep with a note`.**

#### `ledger_S3` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** el `DANGER_FORM` del lenguaje, que es el parentesis contable — un importe negativo se escribe entre parentesis.
* **Lo que ensenia el frame:** el argumento es bueno y el gasto es exclusivo: `( )` no se usa en ninguna otra parte de ledger. Los switches llevan pista, posicion **y palabra** (`──▪ posted`, `▪·· open`, `▫╌╌ open`).
* **Objecion mas fuerte (C9):** la fila 19 es `DANGER ZONE ························································ delete every completed task`. **El caption del control destructivo esta dibujado byte a byte como una fila de campo**: en `ledger_S1` la fila 6 es `PROJECT ························· Web`. La unica diferencia es la longitud del guia. **Criterio observable:** en `ledger_S3`, decir si `delete every completed task` es un caption, el valor del campo `DANGER ZONE`, o un control. Es la objecion cerrada para industrial y darkside en la primera ronda, viva aqui y en `blueprint_S3`.
* **Segunda:** el switch deshabilitado y el apagado dicen **la misma palabra** (`open`), asi que el unico canal entre «apagado» y «no lo puedes tocar» es `▪··` contra `▫╌╌`.
* **Tercera:** `( )` fuera de contexto dice «aparte», no «peligro», a cualquier lector que no sea contable. Se registra; el gasto exclusivo lo salva.
* **Veredicto: `keep with a note`.**

#### `ledger_S4` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** el mismo que `corgi_S4` y `solari_S4` — que un confirm destructivo diga donde esta y sobre que actua, y que se sepa donde termina.
* **Lo que ensenia el frame:**

  ```
  f01-f25   (el tablero, intacto: tira de modos, masthead, gates, panel de detalle)
  f26       ──────────────────────────────────────────────────  (100 celdas)
  f27       Delete 3 tasks?
  f29       3 tasks will be removed from BACKLOG.
  f30       This cannot be undone.
  f32       ▶  (Delete)  │   │   Cancel   │        <- ULTIMA FILA DEL TERMINAL
  ```
* **Objecion mas fuerte:** **el modal abre con una regla de 100 celdas y no cierra, y la respuesta destructiva esta en la ultima fila de la pantalla.** Es C2 — el defecto de `swiss_S4`, nombrado como *still open* desde `rework-3` — con un agravante que swiss no tiene: debajo de `(Delete)` no hay nada, ni un pager ni una costura, asi que el limite inferior del modal es el borde de la terminal. **Criterio observable:** decir donde termina el modal. Sin respuesta, y el control irreversible esta pegado al borde.
* **Segunda:** la fila 32 lleva `▶  (Delete)  │   │   Cancel   │` — **un `▶` y tres `│`**. Las paredes de `(Delete)` no son un par: abre con el cursor y cierra con la regla de columna. **Criterio:** en la fila 32, senialar los dos botones y sus limites. `(Delete)` esta delimitado por sus propios parentesis, que es el `DANGER_FORM`, asi que la unica marca que dice donde acaba el boton peligroso es la que dice que es peligroso.
* **Tercera:** el tablero superviviente pierde la sangria de dos que tiene todo el lenguaje; las filas 27-32 arrancan en la columna 1 mientras las 1-25 arrancan en la 3.
* **Veredicto: `rework`.** El eje incumplido: **C2**, composicion en `overlay_instead`, segundo lenguaje.

#### `ledger_S5` — primera lectura → **`keep with a note`**
* **Compromiso puesto a prueba:** la escalera `"  " / "* " / "**"` como cuenta de asteriscos, que es una eleccion tipografica coherente con `†` y `‡`.
* **Lo que ensenia el frame:** el argumento de la cuenta es correcto — cero, uno y dos asteriscos es monotono y sobrevive al color quitado.
* **Objecion mas fuerte (L7):** **el peldanio `info` es aire.** Seis de las ocho filas del log no llevan ninguna marca. **Criterio observable:** en `ledger_S5`, senialar las filas que llevan una severidad. Responden dos; las otras seis son indistinguibles de una fila que nadie clasifico. Y **`inc60.md` uso esta declaracion como PRECEDENTE** para mandar el `info` de blueprint al aire, con lo que el corpus tiene ahora dos lenguajes con severidad `info` invisible y el precedente sale de un frame que ninguna ronda habia mirado. Ver §7.
* **Segunda:** la sparkline de la fila 6 (`:▫:▫:▫▪▫::▫▫▫:▫▫`) tiene el suelo en `▫`, que es **la pista del switch deshabilitado de `S3`**, y el pico en `▪`, que es la pestania activa, la perilla del slider y el relleno del medidor.
* **Veredicto: `keep with a note`.**

#### `ledger_S6` — primera lectura → **`rework`**
* **Compromiso puesto a prueba:** `MATCH_STYLE = "underline {ink}"` — el unico compromiso de esta pantalla, y el unico que solo se puede juzgar en el `.svg`.
* **Lo que ensenia el frame:** el `.txt` esta bien: `> ▶re▏─────…─│`, seis resultados, el cursor `▶`, la barra de teclas en la notacion del lenguaje (`enter··RUN`, con el guia de puntos como separador, que es coherente). El `.svg` pinta 6 × `<text fill="#1c1a15" text-decoration="underline">re</text>` **sobre un `<rect fill="#121212">`**.
* **Objecion mas fuerte (E4):** **el compromiso declarado de esta pantalla no es verificable en el unico tier que puede llevarlo.** `#1c1a15` sobre `#121212` es **1,08:1**; el subrayado y el texto que subraya estan en negro sobre negro. Y la jerarquia esta invertida: lo unico que se lee en el frame son los puntos guia (`#c4b99f`, 9,62:1), que es el elemento menos importante de la pagina.
* **Criterio observable, y es ejecutable ahora mismo:** abrir `ledger_S6.svg` y circular las seis coincidencias de `re`. Sin respuesta. Abrir `ledger_S1.svg` y decir que tarea esta en `DOING`. Sin respuesta.
* **Segunda:** la fila 16 dice `nil balance` para «la busqueda no encontro nada», que es el mismo texto que `ledger_S1` usa para «este gate no tiene tareas». Es C6, el gemelo del `NO DEPARTURES` de solari. **Criterio:** leer la fila 16 y decir que ocurrio.
* **Veredicto: `rework`.** El eje incumplido: **E4**, el exportador. **La correccion no es de ledger y es de una linea**: `cell_grid()` tiene que devolver el `ground` declarado del kit y no el fondo mas frecuente del compositor.

---

## 3. Que se movio, en numeros

| | ronda 1 | ronda 2 | ronda 3 |
|---|---|---|---|
| frames juzgados | 42 | 42 | **66** |
| `keep` (de los 42) | 6 | 14 | **15** |
| `keep with a note` (de los 42) | 17 | 21 | **24** |
| `rework` (de los 42) | 19 | 7 | **3** |
| `keep` / nota / rework (los 24, primera lectura) | — | — | **0 / 16 / 8** |
| frames con `.txt` movido desde la ronda anterior | — | 26 de 42 | **27 de 66** (14 de los 42, 13 de los 24) |
| celdas colisionantes (censo, 11 lenguajes) | 54 | 48 | **25** |
| filas vivas de significado × significado (exenciones aparte) | 15 | 8 | **0** |
| filas de homoglifo | — | 4 (desde inc53) | **1** |
| `MEANING_AT_AN_OPENER`, total | — | 78 | **0** |
| `MEANING_AT_A_NAMED_SEAT`, total | — | 56 | **0** |
| exenciones vivas, por nombre | — | 1 | **2** |
| lenguajes cuyo `S6` pinta su `MATCH_STYLE` | 0 de 7 | 7 de 7 | **11 de 11** |
| lenguajes cuyo `.svg` es legible | — | 7 de 7 | **10 de 11** |

**Dieciseis de los diecinueve `rework` de la primera ronda estan cerrados.** Los tres que quedan de
aquella lista son `swiss_S2` (L2, una declaracion), `swiss_S4` (C2, una composicion) y `blueprint_S3`
(K4, una ley que no existe). Ninguno de los tres necesita una decision del operador: los tres estan
nombrados en `spec.md` como abiertos y los tres son trabajo.

**Los ocho `rework` nuevos son cuatro cosas y ninguna es un alfabeto:**

1. **Dos composiciones que borran o no cierran la pantalla** — `corgi_S4` (borra el tablero entero),
   `ledger_S4` (abre y no cierra, con el destructivo en la ultima fila).
2. **Tres cantidades mal dibujadas** — `naught_S1`/`S4` y `corgi_S1` gastan la marca de peligro en
   cromo; `prism_S1` lee su propia rampa al reves.
3. **Dos estados de un `part` en el orden equivocado** — `prism_S2`, el checkbox invertido.
4. **Un tier de estilo que no se puede mirar** — `ledger_S6`, y es del exportador.

---

## 4. Donde empeoro la objecion, aunque la etiqueta no

Ninguna etiqueta de los 42 retrocedio. Cuatro objeciones si se pusieron peores bajo una etiqueta que
no se movio, y una de ellas es la mas grave de la ronda.

1. **`solari_S4`** (nota → nota). La ruling F se cumplio y el gate que el confirm nombra esta en
   pantalla. **A cambio, la banda se come la cabecera `GATE DOING 04` y tres de sus cuatro tareas, y
   la cuarta queda archivada bajo `GATE BACKLOG 05`.** Antes el frame **no respondia** a «de que gate
   se borra»; ahora responde bien a eso y **responde mal** a «a que gate pertenece esta tarea». Un
   frame que afirma algo falso es peor que un frame que calla. El coste que inc55 declaro por escrito
   es la costura huerfana, no esto.

2. **`blueprint_S5`** (nota → nota). `━` bajo de cuatro papeles a tres, lo cual es una mejora real.
   Pero inc60 mando `LEVELS["info"]` al aire y **seis de las ocho filas del log perdieron su marca de
   severidad**. La escalera dejo de ser monotona por cuenta.

3. **`swiss_S2`** (rework → rework). La ruling C saco el `DANGER_FORM` de la pared del campo
   invalido, que era la objecion (c). Pero inc53 movio el radio elegido a `▪`, que es **el checkbox
   marcado de dos filas mas abajo y el anillo de foco del destructivo de `S4`**. Y `Save` sigue sin
   nada: en cinco lotes, la unica cosa que ha cambiado en esa fila es que `Cancel` gano una marca.

4. **`instrument_S1`** (nota → nota). El frame no se movio, pero inc57 declaro `FIELD_LEAD = "⠒"`, de
   modo que la celda que compite con el gutter tiene ahora una familia mas en el censo. La objecion
   se puso peor porque el instrumento aprendio a verla, que es la clase buena de empeorar.

**Y el patron que las cruza ya no es el de la segunda ronda.** La ronda dos encontro que cinco de seis
lenguajes resolvian una colision mudandose a un homoglifo. Los cuatro lotes desde entonces han
resuelto casi todo lo que **una declaracion de control** puede resolver: los dos rosters estan en cero
y las filas vivas de significado × significado tambien. **Lo que queda esta todo fuera de
`PART_GLYPHS`** — el rail, el pager, el slider, la sparkline, el medidor, el mascot, el `ERROR_FILL`,
el `SPIN`, el marco del modal y el caption del destructivo. El programa arreglo el alfabeto de los
controles y no ha empezado el de la pagina.

---

## 5. Las objeciones en pie, por quien las arregla

### `Kit` y los tests

| # | objecion | estado | evidencia |
|---|---|---|---|
| K1 | La ley del asiento nombrado mira `switch.indicator` y nunca `switch.knob`. | **CERRADA** (inc49, `KNOB_SEATS`) | `darkside_S3` |
| K2 | **Las tres leyes comparan code points; el canal del lector es la forma.** `HOMOGLYPHS` es una lista fija de cinco pares. | **ABIERTA, tercera ronda, y peor** | naught `⊙`/`◉` y `○`/`◦`; ledger `†`/`‡`; blueprint `╌`/`┄`/`┈` |
| K3 | El stepper no tenia ley y `stepper.step[INVALID]` era `][`. | **CERRADA** (inc51) — y ningun frame del corpus dibuja un stepper, asi que la ley esta sobre un test de propiedad y sobre nada que se pueda mirar | `spec.md` §12.5 |
| K4 | **Ninguna ley compara dos estados del mismo `part`.** | **ABIERTA, tercera ronda** | `blueprint_S3` (`├─┤` / `├┤·` / `├╎┈`), **`prism_S2` (el checkbox invertido)** |
| K5 | **NUEVA. Ninguna ley y ningun instrumento lee un widget de CANTIDAD.** slider, barra, scrollbar, medidor, sparkline, pager y mascot estan fuera de `PART_GLYPHS`, y los tres primeros fuera del conjunto B por peticion del operador. Los cuatro lenguajes nuevos ponen un peldanio de significado dentro de uno. | **NUEVA Y ABIERTA** | §0b, y tres de los ocho rehacer nuevos |

### Nivel lenguaje (una declaracion de un kit)

| # | objecion | estado | frame |
|---|---|---|---|
| L1 | El campo invalido lleva las mismas dos paredes que el normal y que el boton. | **CERRADA** (inc52) — sustituida por `⠶` = radio elegido | `instrument_S2` |
| L2 | **El boton deshabilitado sigue siendo aire**, junto a un `Cancel` que si tiene abridor y encima de una leyenda. | **ABIERTA, tercera ronda, cinco lotes** | `swiss_S2` |
| L3 | `├` era `REQUIRED` y el terminador de toda cota. | **CERRADA** (inc60, `═`) — sustituida por `═`/`╞`/`╡` en una fila | `blueprint_S2` |
| L4 | Tres vocabularios de pared en una pantalla. | **ABIERTA**, y hay un cuarto declarado sin renderizar (`░░`) | `nord_S2` |
| L5 | El cursor y el `DISCLOSE` son el mismo triangulo girado. | **RESPONDIDA POR RULING** (D-addendum, inc55: la rotacion es un canal cuando es direccion que el lenguaje ya gasta) | `industrial_S1` |
| L6 | La sparkline se dibuja con los peldanios altos de `LEVELS`. | **ABIERTA, y ahora en tres lenguajes** | `swiss_S5`, `blueprint_S5`, **`corgi_S5`** |
| L7 | **NUEVA. `LEVELS["info"]` es AIRE en dos lenguajes.** Seis de ocho filas del log sin marca de severidad. | **NUEVA Y ABIERTA** | `blueprint_S5`, `ledger_S5` |
| L8 | **NUEVA. El checkbox de prism esta invertido**: marcado dibuja el pozo vacio y sin marcar dibuja una marca dentro. | **NUEVA Y ABIERTA** | `prism_S2` |
| L9 | **NUEVA. La barra de progreso de prism se llena por lo ligero y sus otros dos medidores por lo pesado.** | **NUEVA Y ABIERTA** | `prism_S1` contra `prism_S3`, `prism_S5` |
| L10 | **NUEVA. El radio y el checkbox de naught se distinguen solo por diametro y relleno de un circulo, a dos filas.** | **NUEVA Y ABIERTA** | `naught_S2` |

### Hoja y composicion (`screens.py`, `overlay_instead`)

| # | objecion | estado | frame |
|---|---|---|---|
| C1 | El destructivo se construye con `knockout_cell` en vez de `button`. | **CERRADA** (inc54) | `blueprint_S4` |
| C2 | **El modal abre con una regla de 100 celdas y no cierra.** | **ABIERTA, tercera ronda, y ahora en dos lenguajes** | `swiss_S4`, **`ledger_S4`** (con el destructivo en la ultima fila) |
| C3 | La banda se come el gate que el confirm nombra. | **CERRADA** (inc55, ruling F) | `solari_S4` |
| C3' | **NUEVA. La banda se come la cabecera de OTRO gate y deja una tarea archivada bajo el gate equivocado.** | **NUEVA Y ABIERTA** | `solari_S4` |
| C4 | El `.txt` de darkside no tiene separacion de paneles. | **RULED** (E, inc55: el `.svg` es el artefacto de registro) | `darkside_S1` |
| C5 | `BACKLOG 5▂` / `DOING 4▂`, el munion de sparkline pegado al conteo. | **ABIERTA, tercera ronda, sin tocar** | `nord_S1` |
| C6 | El estado vacio de la busqueda es el estado vacio del tablero. | **ABIERTA, y ahora en dos lenguajes** | `solari_S6` (`NO DEPARTURES`), **`ledger_S6`** (`nil balance`) |
| C7 | Las filas 3, 13 y 20 son la misma cadena de 100 `⠒`. | **ABIERTA, sin tocar** | `instrument_S4` |
| C8 | **NUEVA. El confirm borra la aplicacion entera**: `corgi_S4` es el unico de los once cuyo `S4` pierde la fila 1, y su `.svg` tiene siete runs de texto. | **NUEVA Y ABIERTA** | `corgi_S4` |
| C9 | **NUEVA. El caption del control destructivo esta dibujado como una fila de campo**, byte a byte igual que un valor de detalle de la misma hoja. | **NUEVA Y ABIERTA** | `blueprint_S3`, `ledger_S3`, `naught_S3` |
| C10 | **NUEVA. El fixture se contradice entre frames:** `blueprint_S2` dice `OVERDUE` y `S1`/`S3`/`S4` dicen `CLEAR` sobre el mismo tablero sembrado. | **NUEVA Y ABIERTA**, declarada por inc56 | `blueprint_S1`, `S2` |

### Exportador

| # | objecion | estado |
|---|---|---|
| E1 | El tier de estilo no se pintaba. | **CERRADA** (inc43); los once `S6` pintan su `MATCH_STYLE` |
| E2 | **El `.svg` no lleva metrica de fuente**, asi que ninguna objecion de homoglifo se puede *resolver* desde el artefacto. Hace falta un raster a la altura de celda de disenio. | **ABIERTA, tercera ronda, y ahora sostiene cuatro objeciones** (naught, ledger, blueprint, industrial) |
| E3 | `gallery_darkside` es dependiente del calendario. | **ABIERTA**, y **disparo por primera vez en inc58** (el dia rodo 6 → 7) tras dos mediciones que la predijeron |
| E4 | **NUEVA. `cell_grid()` mide el ground como el fondo mas frecuente del compositor en vez de leer el `ground` declarado del kit.** ledger es el unico lenguaje de papel claro y sus seis `.svg` pintan `#1c1a15` sobre `#121212` a **1,08:1**, con la jerarquia invertida. | **NUEVA Y ABIERTA. Es una linea.** |

### Galeria y skill (fuera del alcance de los frames, arrastrado cuatro lotes)

| # | objecion | estado |
|---|---|---|
| G1 | `49_darkside-modal-rounded-lid` esta rancio en tres sitios (danger form, guias de campo, pestania activa). `export_to_skill.py` copia `prototypes/gallery/*` y no toca `assets/gallery/`. | **ABIERTA, cuarto lote seguido.** O alguien lo reinstala a mano o se le ensenia al exportador ese directorio |
| G2 | El repo del skill esta sucio y sin commitear desde `rework-5a`. | **ABIERTA, tres lotes** |

---

## 6. La disciplina, medida — lo que este programa hace bien y hay que decir

Un documento adversarial que solo lista defectos miente por omision. Cuatro cosas de estos cuatro
lotes son mejores que la media de la industria y estan medidas, no afirmadas:

1. **Toda exencion esta por nombre, con cita, y una esta TASADA.** `GROUND_EXEMPTION_IS_WORTH = (7, 2)`
   es una constante del suite con su propia ley: vaciar `THE_GROUND_IS_NOT_A_MARK` sobre el kit
   publicado marca 7 abridores y 2 asientos. Nadie puede apoyar mas peso en esa exencion en silencio.
   **Y el packet dice lo incomodo:** cinco de esos siete son obra de inc61, asi que sin la exencion
   naught leeria 7, peor que el 3 con el que empezo.
2. **Dos exenciones en bloque se redactaron y el FRAME las rechazo** (corgi y naught, inc58 y inc61),
   con la medicion citada. Y **una exencion se borro despues de medirla en cero disparos** (inc52).
3. **`verify_language.py` cogio tres veces lo que la suite de pytest no podia, y no se edito nunca.**
   Dos de esas tres veces escribio el arreglo (la division de los runs muertos de blueprint en `┈` y
   `┄` es la respuesta de la ley, no una preferencia).
4. **Los packets registran sus propios errores.** `inc60.md` deja escrito que su prediccion
   `BLUEPRINT_TABLES_WORTH = (0, 0)` era falsa y que el numero real es `(1, 8)`; `inc61.md` registra
   que la primera respuesta para el papel EDITED de naught y de ledger fue la misma equivocacion dos
   veces, cogida mirando la fila renderizada y no la tabla.

Y una que hay que decir al reves: **`test_win_clipboard_roundtrip` estuvo en rojo en todas las
corridas de `rework-5c`, incluida la linea base**, y esta nombrado en cada packet como acoplado al
entorno, no contado y no tocado. Es la forma correcta de llevar un test enfermo.

---

## 7. Objeciones a las rulings

Las rulings son firmes y los frames se juzgaron contra ellas. Estas seis lineas son desacuerdos, y
nada mas que eso.

1. **Ruling A (los cinco lenguajes sin incremento).** Su cero descansa en que el slider, la barra y el
   scrollbar estan fuera del conjunto B «por peticion del operador». Tres de mis ocho rehacer nuevos
   viven exactamente ahi. Un roster en cero que excluye el widget donde el defecto vive no es un cero.
2. **Ruling D (los cuatro canales).** El instrumento que la hace cumplir es una lista fija de cinco
   pares de homoglifos. Una ruling que solo obliga contra los pares que alguien escribio no es una
   ruling sobre la forma, es una lista de excepciones al reves. Los cuatro pares mas apretados del
   corpus estan fuera de ella.
3. **Ruling E (el `.svg` es el artefacto de registro para darkside).** Es correcta y esta sin
   auditar. El exportador no lleva el `ground` declarado del kit (§0a), y que darkside no salga danado
   es que su ground ya era oscuro. Ascender un tier presupone haberlo medido.
4. **Ruling G (el mood `alert` en `S2`).** Se cumplio y el knockout esta por fin en una imagen. Pero
   ponerlo en una hoja y no en las otras hace que **un fixture rinda dos hechos distintos**, y el
   propio inc56 midio que ponerlo globalmente rompe la ruling 10. Eso significa que **la ruling 10 y
   la ruling G no pueden valer las dos en `S4`**, y nadie ha decidido cual cede.
5. **`inc60` mando `LEVELS["info"]` de blueprint al aire citando `Ledger.LEVELS` como precedente.**
   Ledger era uno de los doce frames que ninguna ronda habia juzgado. **Un precedente tomado de un
   frame sin juzgar no es un precedente**, y el resultado es que el corpus tiene ahora dos lenguajes
   con la severidad `info` invisible en vez de uno.
6. **Ruling C (INVALID nunca toma el `DANGER_FORM`)** es correcta y los siete reverts se hicieron.
   Pero en swiss nada ocupo el canal que se libero: `║12/09/26` es una pared y ocho caracteres, sin
   papel y sin cierre. El frame perdio una respuesta equivocada y no gano ninguna.

---

## 8. Lo que esta ronda no puede ver

Se dice llano, y se dice por tercera vez porque sigue siendo verdad.

1. **No se ejecuto nada.** Se leyeron 66 `.txt` y 66 `.svg` a `f1508ad`, mas los `.txt` y `.svg` de
   `b559e92` para los 27 que se movieron. **No se ejecuto la aplicacion, no se pulso ninguna tecla, no
   se movio ningun foco y no se cambio ningun estado.** Todo lo de arriba es un recorrido cognitivo
   sobre imagenes fijas con criterios declarados. Tampoco se corrio la suite ni ninguno de los
   scripts: los numeros de gates citados (1111 passed, censo 25, rosters en cero, filas de homoglifo
   1) estan **leidos de los packets y del `collision_census.txt` en disco**, no reproducidos aqui. Los
   unicos numeros que esta ronda calculo son los contrastes WCAG de §0a y §0c y los conteos de glifos,
   los dos derivados de los ficheros con la formula escrita en §9.
2. **Un solo ancho.** Los 66 estan a 100×32. Los compromisos que dicen «at any width» siguen juzgados
   a un ancho, e inc54 declaro por escrito que el asiento destructivo de blueprint paso de 8 a 12
   celdas y que **nada en este repo renderiza `S4` por debajo de 100**.
3. **El foco es una decoracion fija.** `FOCUSED` se lee de una marca, no de un foco. Que pasa al
   pulsar `tab`, si el anillo salta donde el lector espera y si el orden de tabulacion coincide con el
   visual: ninguna es respondible desde un frame.
4. **La metrica de fuente (E2).** El `.svg` no dice a que tamanio de celda ni con que fuente se va a
   renderizar. **Ninguna** de las cuatro objeciones de homoglifo de §0d esta *resuelta* aqui: estan
   *planteadas* con la evidencia de la declaracion y del frame. Hace falta un raster a la altura de
   celda real.
5. **El componente que nadie ha visto.** El stepper tiene ley desde inc51 y **ningun artefacto de este
   repo lo dibuja**; la hoja de componentes se corta antes de su fila a 118×34. La ley esta sobre un
   test de propiedad y sobre nada mirable.
6. **La densidad no se re-midio.** La segunda ronda la calculo sobre los 42 con
   `verify_ink.ink_fraction` y encontro una deriva maxima de −0,8 puntos. Esta ronda **no corrio ese
   script** y no tiene cifra para los 24. Que una pantalla al 47,5 % se sienta llena y una al 8,3 %
   vacia sigue siendo una hipotesis razonable y no una medicion.
7. **Animacion, latencia y asentamiento.** Capturados con `animations off`. El `SPIN` de darkside y el
   de prism respiran una vez por frame y ningun `SPIN` esta censado; el estado `held` del log y el
   coste de repintado no estan aqui.
8. **Usuarios reales.** ISO 9241-210 pide evaluacion con usuarios; este equipo es una persona. Lo que
   hay aqui es **inspeccion con criterios declarados**, un recorrido cognitivo sobre las tareas que el
   contexto de uso nombra. **No se hizo ninguna evaluacion con usuarios reales, y ninguna afirmacion
   de este documento debe leerse como si se hubiera hecho.**

---

## 9. Como reproducir esta ronda

```
git -C <worktree> diff --stat b559e92 f1508ad -- prototypes/components/
git -C <worktree> show b559e92:prototypes/components/<frame>.txt
git -C <worktree> show b559e92:prototypes/components/<frame>.svg
python -X utf8 prototypes/components/render.py       # 66 .txt + 66 .svg + 66 .candidates.md
python -X utf8 prototypes/collision_census.py        # prototypes/out/collision_census.txt
python -X utf8 prototypes/verify_ink.py --frames     # tinta determinista sobre los 66 (NO corrido)
python -X utf8 -m pytest -q                          # las tres leyes y sus tests de dientes
```

Los contrastes de §0a y §0c se derivan de los `fill=` de los `.svg` con la formula WCAG de luminancia
relativa (`L = 0.2126R + 0.7152G + 0.0722B` sobre canales linealizados; `(L1+0.05)/(L2+0.05)`). Los
conteos de glifos son `str.count` sobre los `.txt` en disco. Los diffs de celdas estan citados con las
dos versiones al lado para que nadie tenga que creerse este documento.

**Pagina del operador:** `ronda-66.html`, con los 66 frames nuevos, el `.svg` viejo al lado para los 27
que se movieron, y un voto por frame.

# PROTOTYPE-inheritors-5, los 66 frames contra el raster, a dos anchos, y la primera ronda que le lleva la contraria a la anterior

`PROTOTYPE-inheritors-4.md` (2026-09-07, en `4089eda`) juzgo los 66 por cuarta vez y devolvio
**keep 11 · nota 51 · rehacer 4**. Su §9d cerro con una recomendacion y no con una lista: *«parar la
ronda y cambiar el instrumento … construir el raster (E2) y solo entonces correr la ronda cinco,
contra el raster y a dos anchos.»* Corrieron `rework-7a` (inc72–75: los cuatro rehacer, K6/K7, el tier
de match por canal, un rol por token, `DIM_CLASSIFIES`, las paredes del confirm de corgi, el papel de
industrial) y `rework-7b` (inc76–78: `raster.py`, `legibility.py`, `second_width.py`).

**Esta ronda es la primera que MIRA.** Los 66 PNG a Cascadia Mono 16 px, celda 9×19, y los 66 a 80×24.
No se leyo un `fill=`; se leyo un pixel. Y el instrumento hizo lo que se le pidio: **fallo de una
manera distinta.** Cuatro objeciones que tres rondas dieron por buenas resultan falsas sobre la
pintura, dos frames que nadie habia mirado con desconfianza resultan rotos, y la mejor fila del
programa la escribio una fila de cien celdas en blanco.

**Resultado: keep 14 · nota 46 · rehacer 6.** Siete frames mejoraron, seis empeoraron. Es la primera
ronda en la que suben `keep` **y** `rehacer` a la vez, y eso es exactamente lo que un instrumento
nuevo tiene que hacer si sirve de algo.

Contexto de uso, sin cambios: **operador unico** (`jav201`), terminal monoespaciada, sesion diurna,
tema por defecto; la tarea es la que la pantalla nombra. Lo nuevo del contexto es el **tamanio**:
100×32 y 80×24 celdas, a 9×19 px por celda, en la fuente por defecto de Windows Terminal.

---

## 0. Cuatro cosas que hay que decir antes de la primera tabla

### 0a. Una fila de cien celdas en blanco es lo mas ruidoso de `solari_S4`, y ningun instrumento del programa la ve

`solari_S4` fila 10 es esto, leido del sidecar que inc76 escribio:

```
[0, "                    (100 espacios)                    ", ink #0b0b0c, ground #f5a300]
```

Cien celdas en blanco pintadas sobre el ambar del kit. En el PNG es **una barra ambar de 900×19 px, la
cosa mas brillante de la pantalla.** Y es el ABRIDOR de la banda: el confirm de solari abre con esa
barra y cierra con cien `▁` de `seam` a **1,20:1**, la tirada mas apagada del corpus.

**La ronda cuatro escribio exactamente lo contrario** (§2.6, objecion nueva 1): *«la banda cierra y no
abre … criterio: decir donde empieza el modal. Sin respuesta.»* Sobre el `.txt` la fila 10 esta vacia,
sobre el `.svg` no tiene ni un `<text>`, y **una tirada de espacios no lleva tinta, asi que no la mide
el censo, ni `HOMOGLYPH_FAMILIES`, ni `painted_runs()` de inc73, ni la cobertura de inc77.** Todos los
instrumentos de once lotes leen glifos.

Barrido sobre los 132 sidecars: **18 tiradas de ocho celdas o mas, en blanco, sobre un ground que no
es el lienzo, en tres kits.**

| kit | frames | tiradas | ground | que es |
|---|---|---|---|---|
| industrial | `S1` | 16 | `#2e2e2e` | el plato del panel de detalle |
| prism | `S4` | 1 (63 celdas) | `#1f2630` | el plato del confirm |
| solari | `S4` | 1 (100 celdas) | `#f5a300` | **el abridor de la banda** |

Las tres se ven a simple vista en el PNG y ninguna existe para el resto del aparato. La ley que si las
alcanza es una sola y por accidente: `test_a_confirm_opens_and_closes_on_marks_of_its_own` mide el
ANCHO de los `<rect>` del svg para solari, que es la unica clausula del suite que lee un ground sin
glifo. **E6 (nueva): el exportador pinta superficie que ninguna ley puede nombrar.**

### 0b. La continuidad vence a la cobertura, y eso decide §0b de la ronda cuatro

La ronda cuatro bajo cuatro etiquetas porque el peldanio `info` de nueve kits esta bajo 3:1, y §8.4
dejo escrito que *«esta ronda no resuelve cuales de las once tiradas de `dim` son decoracion y cuales
son senial»*. **El raster lo resuelve, y lo resuelve con una regla mecanica.**

Medido sobre los `.txt` en disco, la tirada horizontal ininterrumpida mas larga de cada marca:

| marca | contraste | tirada mas larga | se ve en el PNG |
|---|---|---|---|
| solari `▁` costura | **1,20:1**, el peor del corpus | **100 celdas = 900 px** | **si, limpiamente** |
| swiss `─` regla | 1,75:1 | 100 celdas = 900 px | si |
| ledger `·` guia | 1,50:1 | 74 celdas = 666 px | si |
| blueprint `─` cota | 1,24:1 | 55 celdas = 495 px | si |
| darkside `·` severidad | 1,39:1 | **1 celda = 9 px** | **no** |
| swiss `·` severidad | 1,75:1 | 1 celda | no |
| instrument `⠂` severidad | 1,74:1 | 2 celdas | apenas |
| prism `⡀` obligatorio | 3,25:1 | **1 celda**, y es el mejor ratio de los cuatro | **no** |

**La misma celda, al mismo contraste, es legible a 55 celdas de largo e invisible a una.** El ojo
integra a lo largo de un trazo continuo y no tiene nada que integrar en un punto de cuatro pixeles.
Ningun ratio puede decir esto porque un ratio no sabe cuantas veces se dibuja la celda seguida.

**Consecuencia directa:** las once tiradas de `dim` se parten por LARGO DE TIRADA, no por gusto. Las
costuras, reglas, guias y cotas (tiradas de 8 celdas o mas) son estructura y se ven; los peldanios de
severidad, los obligatorios y los cursores (tiradas de 1 a 4 celdas) son significado y cinco kits los
dibujan invisibles. §7 lo convierte en la recomendacion de piso.

### 0c. La polaridad no esta en la formula, y ledger lo demuestra

La ronda cuatro (§2.11): *«`dim #c4b99f` es hoy 1,50:1 … criterio: abrir `ledger_S1.svg` y nombrar los
cuatro modos. Responde uno.»*

**En el PNG responden los cuatro.** `· form`, `· cfg` y `· log` se leen letra por letra, palidos y
completos. El mismo 1,50:1 en swiss o en darkside (tinta clara sobre negro) desaparece; en ledger
(tinta oscura sobre papel `#e9e1cf`) aguanta. WCAG 1.4.3 es simetrico por construccion
`(L1+0,05)/(L2+0,05)` no sabe cual de los dos es el fondo, y **el unico kit de papel claro del corpus
es el mas legible de los once a 16 px por un margen que ningun numero de estas cinco rondas registra.**

Se escribe como limite del instrumento, no como merito de ledger: el corpus no tiene un segundo kit
claro con el que contrastarlo, asi que esto es UNA observacion sobre ONCE kits y no una ley.

### 0d. El match tier era un problema de luminancia y el canal es el matiz

L11 de la ronda cuatro: *«el match tier de tres kits se estrecho al subir `mut`: nord 1,79 → 1,38;
instrument 2,45 → 2,32; ledger 3,00 → 2,96»*, y `nord_S6` fue **«la que mas empeoro de las 66»**.

En el PNG, `nord_S6` ensenia seis `re` en verde azulado sobre cuerpo pizarra y **no hay forma de no
verlos.** Igual `swiss_S6`, rojo sobre gris, con la peor cifra del corpus (1,52 contra `mut`). La
clausula que los juzga es la rama acromatica de la ruling de inc73 (*«para kits acromaticos, el acento
difiere de `mut` en ≥ 1,5:1 de luminancia»*), y cae en esa rama **porque `mut` es gris y la distancia
de matiz contra un gris no esta definida**. Medir luminancia entre un rojo saturado y un gris es medir
la dimension en la que menos se diferencian.

`nord_S6` y `swiss_S6` suben a **`keep`**. Lo que queda, y es de corpus y no de frame: **el canal es el
matiz solo**, y eso es una objecion nueva (**L12**) que se registra en §5 y que ninguna de estas cinco
rondas puede resolver, porque no hay lector daltonico en este equipo ni captura en escala de grises en
este repo.

---

## 1. La matriz 11×6

Etiqueta de la ronda cuatro → etiqueta de esta.

|  | S1 lista | S2 formulario | S3 ajustes | S4 modal | S5 monitor | S6 paleta |
|---|---|---|---|---|---|---|
| **instrument** | nota → **nota** | nota → **rehacer** | nota → **nota** | nota → **nota** | nota → **nota** | keep → **nota** |
| **swiss** | nota → **nota** | nota → **nota** | keep → **keep** | nota → **nota** | nota → **nota** | nota → **keep** |
| **industrial** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | nota → **keep** | keep → **keep** |
| **nord** | nota → **nota** | nota → **nota** | keep → **keep** | keep → **keep** | nota → **keep** | nota → **keep** |
| **darkside** | nota → **nota** | nota → **nota** | nota → **nota** | keep → **keep** | nota → **nota** | keep → **keep** |
| **solari** | nota → **nota** | nota → **keep** | keep → **keep** | nota → **rehacer** | nota → **nota** | nota → **nota** |
| **blueprint** | nota → **nota** | nota → **nota** | rehacer → **nota** | nota → **rehacer** | nota → **nota** | keep → **nota** |
| **naught** | nota → **nota** | rehacer → **rehacer** | nota → **nota** | rehacer → **rehacer** | nota → **nota** | nota → **nota** |
| **corgi** | nota → **nota** | nota → **nota** | nota → **nota** | nota → **nota** | nota → **nota** | nota → **nota** |
| **prism** | nota → **nota** | nota → **rehacer** | nota → **nota** | nota → **nota** | nota → **nota** | nota → **nota** |
| **ledger** | nota → **nota** | nota → **nota** | nota → **nota** | rehacer → **nota** | nota → **nota** | nota → **nota** |

|  | keep | keep with a note | rework |
|---|---|---|---|
| ronda 4 | 11 | 51 | 4 |
| **ronda 5** | **14** | **46** | **6** |

**Siete frames mejoraron:** `swiss_S6` y `nord_S6` (§0d), `industrial_S5` y `nord_S5` (el peldanio bajo
tiene area y se ve), `solari_S2` (la mejor gramatica de formulario del corpus), `blueprint_S3` (K4
respondida en el frame por LARGO DE PISTA, no por cuenta de guiones) y `ledger_S4` (inc72 cerro C2 y el
raster lo confirma).

**Seis empeoraron:** `instrument_S2` y `prism_S2` (la marca de obligatorio no se puede senialar),
`solari_S4` (§0a mas el rojo de la ruling F), `blueprint_S4` (cuatro esquinas a 44 celdas no son una
caja), `instrument_S6` y `blueprint_S6` (a 24 filas se cae la barra de teclas).

**Los tres rehacer de la ronda cuatro que siguen:** `naught_S2` y `naught_S4`, los dos confirmados
celda a celda sobre la pintura. **`blueprint_S3` cierra**, y con el se cierra el ultimo de los 42
originales.

---

## 2. Los 66 bloques

Formato: *que ensenia el raster que el svg no podia · la objecion mas fuerte con criterio observable ·
80×24 · veredicto*.

---

### 2.1 instrument

`LEVELS ⠂⠂/⠆⠆/⠇⠇` · `REQUIRED ⠁` · `DANGER ⠛⠛` · `CUR ⣿` · `FIELD_LEAD ⠒`.

#### `instrument_S1` — nota → **`keep with a note`**
* **El raster:** el canal de 2,6× que la ronda cuatro midio entre gutter (`⠸`, 4,50:1) y guia (`⠒`, 1,74:1) **se ve**: el gutter es una columna de marcas claras y las guias una trama tenue. Lo que el svg no podia ensenar: `⣿` no es un bloque, es una **trama de puntos al 41 %**, asi que la celda mas pesada del kit y la mas ligera son la misma textura vista de lejos.
* **Criterio (que tarea esta en DOING):** responde. Cabecera `DOING 4`, cuatro titulos debajo.
* **80×24:** el titulo del detalle se corta a `DETAIL Fix` sin elipsis. La barra de progreso pasa de 12 celdas a 4.
* **Veredicto: `keep with a note`.**

#### `instrument_S2` — nota → **`rework`**
* **El raster, y es el eje nuevo:** `⠁` (`REQUIRED`) en su asiento DECLARADO (fila 3, la etiqueta `title`) mide **cobertura 5,8 % · efectivo 3,79 · declarado 16,52:1 · producto 0,221**. Es el segundo peor obligatorio del corpus **con el mejor ratio de contraste de los once**. En el PNG es un pico de tres pixeles a la derecha de la palabra.
* **Criterio observable (que campos son obligatorios):** en `instrument_S2.png`, senialar los campos obligatorios. **Sin respuesta.** Dos de los once frames de formulario fallan este criterio y este es uno.
* **En pie:** `⠶` sigue siendo el campo invalido y el radio elegido tres filas mas abajo; en el raster las dos tiradas son la misma trama.
* **80×24:** identico.
* **Veredicto: `rework`.** El eje: **la marca de obligatorio no tiene area.** Es una tupla.

#### `instrument_S3` — nota → **`keep with a note`**
* **El raster:** `⣿ [7 families]` se ve como una sola trama gris en los cinco switches, el slider y la pestania activa. El censo lo cuenta; ahora hay una foto.
* **Criterio (que pestania esta activa):** responde, por color y por la trama llena.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `instrument_S4` — nota → **`keep with a note`**
* **El raster:** C7 confirmada de la peor manera. Las filas 3, 13 y 20 son cien `⠒` cada una y en el PNG son **tres tramas identicas**; no hay ni diferencia de peso. Y el confirm flota: texto blanco sobre el tablero, sin abridor, con un cierre punteado abajo.
* **Criterio (que celda significa que esto destruye datos):** **ninguna.** Lo dice la palabra `"Delete"` entre comillas; el `DANGER_FORM` `⠛⠛` no esta.
* **80×24:** mejora. A 24 filas el confirm queda a media pagina con tablero arriba y abajo.
* **Veredicto: `keep with a note`.**

#### `instrument_S5` — nota → **`keep with a note`**
* **El raster:** §0b de la ronda cuatro se matiza. El peldanio `⠂⠂` **si esta dibujado y se intuye**; lo que no se puede es contar la escalera. `⠂⠂` (2 puntos), `⠆⠆` (4) y `⠇⠇` (6) se separan por unos cuatro pixeles. Lo que responde el criterio es que el TEXTO de las dos filas graves va en `ink` y el resto en `mut`.
* **Criterio (que filas del log llevan severidad):** responde **por el peso del mensaje, no por la marca**. La escalera es un tercer canal correcto y el suelo sigue bajo.
* **80×24:** identico, el log es estrecho.
* **Veredicto: `keep with a note`.**

#### `instrument_S6` — keep → **`keep with a note`**
* **El raster a favor:** el subrayado del match es una regla real de un pixel bajo `re`; el salto de color de 2,32:1 no tiene que trabajar solo. Sigue siendo un `keep` a 100×32.
* **Lo que baja la etiqueta, y es de ancho:** **a 80×24 la barra de teclas desaparece.** `enter run · esc close · ^p prev · ^n next` es la fila que ensenia como se sale de la paleta, y es la que se cae. Cuatro de los once pierden esta fila (instrument, nord, blueprint, prism); siete la conservan.
* **Objecion en pie:** dos prompts en pantalla con caret en los dos; decir cual tiene el foco no tiene respuesta.
* **Veredicto: `keep with a note`.**

---

### 2.2 swiss

`LEVELS ·/─/━` · `REQUIRED •` · `DANGER ╲╱` · `CUR ▮` · `FIELD_LEAD ""`.

#### `swiss_S1` — nota → **`keep with a note`**
* **El raster refuta la lectura de la ronda cuatro:** *«criterio: decir cuantas reglas hay … en el artefacto la respuesta es "no se ven"»*. **Se ven todas.** Las hairlines a 1,75:1 son reglas grises limpias porque miden 100 celdas (§0b).
* **Objecion en pie, y con la foto es mas facil de contar:** hay **cinco reglas de tres pesos** en una pantalla cuyo compromiso dice «una».
* **80×24:** identico arriba, y el panel de detalle se parte por la mitad; ver `swiss_S1` en §2.2 nota de ancho abajo.
* **Veredicto: `keep with a note`.**

#### `swiss_S2` — nota → **`keep with a note`**
* **El raster afloja la objecion de la ronda cuatro:** `╎` contra `│` a 16 px son un trazo roto en tres contra un trazo entero. **Se distinguen.** La familia de seis verticales sigue siendo mucha, pero la pareja que la ronda cuatro llamo indistinguible no lo es.
* **Objecion nueva, y es la L10 de naught en swiss:** `▪` es el **radio elegido** (fila 10) y el **checkbox marcado** (fila 12), dos filas seguidas, y en el PNG son el mismo cuadrado macizo. **Criterio observable:** tapar las palabras y decir cual de las dos filas es una eleccion unica y cual son casillas independientes. **Sin respuesta.**
* **A favor:** `•` obligatorio mide 0,060 en su peor asiento y **1,288 en el declarado**; se ve.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `swiss_S3` — keep → **`keep`**
* **El raster:** el mejor conjunto de controles del corpus junto con nord y darkside. Switch encendido = barra gris maciza, apagado = trazo, muerto = punteado; slider con perilla.
* **Nota, medida:** la barra del switch encendido y el relleno del slider son **el mismo rectangulo gris** a doce filas de distancia. `FILL_IS_NOT_A_MEANING["swiss"] = 3`, con foto.
* **80×24:** identico.
* **Veredicto: `keep`.**

#### `swiss_S4` — nota → **`keep with a note`**
* **El raster:** las dos reglas de la banda se ven y son iguales entre si. **Criterio (donde termina el modal):** responde. C2 cerrada, confirmada en pixeles.
* **C11 confirmada:** `DOING 4` con una tarea a la vista, y a 80×24 con ninguna.
* **80×24:** la banda abre y cierra igual; el tablero de detras queda en una tarea de BACKLOG y un `DONE 7` huerfano.
* **Veredicto: `keep with a note`.**

#### `swiss_S5` — nota → **`keep with a note`**
* **El raster:** la escalera `· / ─ / ━` es punto → trazo fino → trazo grueso, y los dos peldanios altos se leen sin esfuerzo. El bajo es el **numero 2 de los diez peores del corpus** (0,060) y en el PNG es una mota de 2×2 px.
* **Criterio:** las filas graves responden; las calmas dicen que estan calmas por no tener nada visible, que es doctrina en dos kits y accidente en este.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `swiss_S6` — nota → **`keep`**
* **El raster da la vuelta a la peor cifra del corpus.** 1,52:1 entre el rojo del match y el gris del cuerpo, y en el PNG los seis `re` saltan a la cara. La clausula que los juzga mide luminancia porque `mut` es acromatico (§0d): esta midiendo la dimension equivocada.
* **Criterio (donde aterrizo la consulta):** responde. Caret visible, seis coincidencias en rojo, teclas en rojo.
* **Lo que no cierra, y va a corpus (L12):** **el canal es el matiz solo.** En escala de grises no queda nada.
* **80×24:** identico, barra de teclas conservada.
* **Veredicto: `keep`.**

---

### 2.3 industrial

`LEVELS ▫▫/▪▪/■■` · `REQUIRED !` · `DANGER ╱╱` · `CUR ▶` · `DISCLOSE ▼`.

#### `industrial_S1` — nota → **`keep with a note`**
* **El raster:** el plato `▐▌` es una banda gris solida y el panel se lee como panel. `▐ [3 families]` sigue.
* **Objecion nueva, y solo un raster la puede plantear:** el mascot del estado vacio de `BLOCKED` esta dibujado en **`alert` `#ff6039`, veinte y pico celdas**, y es **lo mas ruidoso de la pantalla**. En la misma hoja, «esta tarea lleva dos dias de retraso» son dos celdas del mismo color. **Criterio observable:** en `industrial_S1.png`, senialar lo mas urgente. Un lector senialara la cara. Es un reparto de peso visual, y ninguna ley del suite lo mide.
* **80×24:** el detalle se corta el titulo, los valores sobreviven porque van alineados a la derecha.
* **Veredicto: `keep with a note`.**

#### `industrial_S2` — nota → **`keep with a note`**, y la objecion de la ronda cuatro CIERRA
* **El raster:** inc75 funciona. El papel `░` es una **banda gris uniforme** y el valor `12/09/26` es texto blanco: la frontera es un borde neto. La ronda cuatro (*«en la fila 6, decir donde acaba el valor introducido y donde empieza el papel. Sin respuesta»*) **tiene respuesta en el pixel**.
* **Lo mejor del corpus:** `!` obligatorio, naranja, producto **0,848** en el asiento declarado; `■■` rojo para el error. Los dos criterios de formulario responden a la primera.
* **Lo que queda:** las paredes del invalido siguen siendo las del campo normal; hoy solo las separa el papel.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `industrial_S3` — keep → **`keep`**
* **El raster:** sigue siendo la referencia del corpus para caption/control. Slider y switches se leen a un metro.
* **80×24:** identico.
* **Veredicto: `keep`.**

#### `industrial_S4` — keep → **`keep`**
* **El raster:** **el mejor modal de los once.** Caja blanca cerrada por cuatro lados, tablero entero atenuado detras, respuesta destructiva naranja.
* **Nota nueva, medida:** `▌//Delete//▐` y `▌Cancel▐` llevan **las mismas paredes blancas**; lo unico que separa las dos respuestas es el naranja. Es L12 otra vez.
* **80×24:** **la caja aguanta entera**, con tablero arriba y abajo. Es el mejor resultado del segundo ancho.
* **Veredicto: `keep`.**

#### `industrial_S5` — nota → **`keep`**
* **El raster revierte la bajada de la ronda cuatro.** `▫▫` (cobertura 17,0 %, hueco), `▪▪` (17,5 %, macizo pequenio) y `■■` (47,4 %, macizo grande) son **tres dibujos distintos y los tres se ven**. La bajada de §0b se apoyaba en 1,96:1; el area es 2,7× entre el peldanio bajo y el alto y eso es un canal.
* **Criterio (que filas llevan severidad):** responde, tres niveles.
* **80×24:** identico.
* **Veredicto: `keep`.**

#### `industrial_S6` — keep → **`keep`**
* **El raster:** el match es **video inverso**, un rectangulo naranja bajo `re`. Es el match mas legible del corpus y el unico inmune a §0d. El corchete de foco de inc73 (`#777777`) se ve.
* **Nota:** el mascot naranja otra vez, debajo de una busqueda sin resultados.
* **80×24:** la barra de teclas **se conserva**, en la ultima fila.
* **Veredicto: `keep`.**

---

### 2.4 nord

`LEVELS "· "/"! "/"!!"` · `REQUIRED *` · `DANGER ##` · `CUR ▸`.

#### `nord_S1` — nota → **`keep with a note`**
* **El raster:** las reglas y el `│` a 1,69:1 se ven bien (§0b). C5 en pie: el munion de la sparkline sigue pegado al conteo.
* **Objecion nueva:** el mascot de `BLOCKED` en verde azulado, grande, es lo mas llamativo de la hoja. Mas benigno que el de industrial porque no gasta `alert`.
* **80×24:** detalle recortado, valores a la derecha sobreviven.
* **Veredicto: `keep with a note`.**

#### `nord_S2` — nota → **`keep with a note`**
* **A favor, y hay que escribirlo:** `( ) low ( ) norm (o) high` contra `[ ] api [x] ui [x] urgent` es **la gramatica de control mas clara de los once**: parentesis contra corchetes, `o` contra `x`. Cero ambiguedad en el pixel.
* **L4 en pie:** tres vocabularios de pared, y el invalido se cierra con `?` a los dos lados, que en el PNG se lee como un signo de interrogacion y no como una pared.
* **Criterio (que fila esta en error):** responde, `!!` en rojo.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `nord_S3` — keep → **`keep`**
* Frame identico, se lee entero. **80×24:** identico. **Veredicto: `keep`.**

#### `nord_S4` — keep → **`keep`**
* **El raster:** caja cerrada, tablero detras, `▌#Delete#▌` con paredes de acento contra `[ Cancel ]` con corchetes desnudos. Dos respuestas distinguibles por FORMA y no solo por color, que es mas de lo que hace industrial.
* **80×24:** la caja aguanta entera.
* **Veredicto: `keep`.**

#### `nord_S5` — nota → **`keep`**
* **El raster revierte la bajada.** `· / ! / !!`: **dos de los tres peldanios son letras de altura completa**. La escalera es inequivoca aunque el peldanio calmo sea invisible, y un peldanio calmo invisible es lo que blueprint y ledger declaran como doctrina.
* **Criterio (que filas llevan severidad):** responde, y el orden tambien.
* **Lo que queda, y va a §5:** nord dibuja su `·` sin declararlo aire. L7 describe nueve de once y solo dos lo dicen; nord es de los nueve.
* **80×24:** identico.
* **Veredicto: `keep`.**

#### `nord_S6` — nota → **`keep`**
* **El raster da la vuelta a «la que mas empeoro de las 66».** 1,38:1 de luminancia, 40,0° de matiz, y en el PNG los seis `re` en verde azulado sobre pizarra son lo primero que ve el ojo.
* **Criterio (senialar las seis coincidencias):** responde a la primera.
* **Lo que no cierra (L12):** el canal es el matiz.
* **80×24:** **se cae la barra de teclas.**
* **Veredicto: `keep`.** La etiqueta sube por el criterio de esta pantalla; la perdida de la barra a 24 filas se registra en §5 y en §8 como asunto de composicion, porque afecta a cuatro kits por el mismo motivo.

---

### 2.5 darkside

`LEVELS "· "/"o "/"O "` · `REQUIRED ▪` · `DANGER ▚▞` · `CUR ▊` · `FIELD_LEAD ▔`.

#### `darkside_S1` — nota → **`keep with a note`**
* **El raster refuta la objecion de la ronda cuatro:** *«senialar el escalon gris que separa los paneles. Esta a 1,39:1»*. En el PNG es **una columna gris maciza de dos celdas de ancho y treinta de alto**, imposible de no ver. La ruling E se sostiene y su unico argumento tambien.
* **Objecion nueva, del raster:** los `▔` de `FIELD_LEAD` del panel de detalle son **rayitas altas sueltas** que a 16 px se leen como suciedad, no como guias.
* **80×24:** identico arriba, detalle recortado.
* **Veredicto: `keep with a note`.**

#### `darkside_S2` — nota → **`keep with a note`**
* **El raster confirma la objecion mas antigua del kit:** la tira de modos usa `( )` / `(●)` y los tags usan `( )` / `(◎)`. **Son la misma familia de dibujo en dos filas que significan cosas distintas.** Criterio: decir cuales de los pares de parentesis son pestanias y cuales casillas. Solo por posicion.
* **A favor:** el radio usa `‹ ›` y el checkbox `( )`, que si es un canal; y `▪` obligatorio mide **1,777** en el asiento declarado, el tercero mejor.
* **Medido aqui:** la fila mas apretada del censo, `▪ ▫` a **3,20 %**, **no se dibuja junta en ningun frame de darkside**: `▫` aparece cero veces en las seis hojas de darkside (swiss 3, industrial 12, ledger 10). Ver §6.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `darkside_S3` — nota → **`keep with a note`**
* **El raster:** el switch (pista gris + perilla azul) y el slider son **los controles mas convencionales y mas legibles de los once**. Vale la pena escribirlo: la ronda tres se lo concedio a solari por el `.txt` y en pixeles lo gana darkside.
* **C9 en pie:** `▔` es el `FIELD_LEAD` de seis filas de detalle y el abridor del caption destructivo; en el PNG las dos son la misma rayita alta.
* **Nota:** la perilla del switch, la del slider y el radio elegido son la misma familia de circulo; ocho filas de homoglifo con foto.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `darkside_S4` — keep → **`keep`**
* **El raster:** caja blanca, tablero detras, dos respuestas.
* **Nota:** las paredes de `Delete` y las marcas que flanquean `Cancel` son las dos azules; la forma las separa, el color no.
* **80×24:** la caja aguanta.
* **Veredicto: `keep`.**

#### `darkside_S5` — nota → **`keep with a note`**
* **El raster:** la escalera `· / o / O` es una rampa de tamanio dentro de una familia, que es la idea correcta. Y el peldanio bajo es **el numero 1 de los diez peores del corpus (0,053)**: en el PNG no esta.
* **La asimetria que decide la etiqueta:** blueprint y ledger no dibujan el peldanio calmo y lo declaran; darkside dibuja uno invisible. **Dibujar una marca que no se ve es peor que no dibujar ninguna, porque reclama un canal que no tiene.**
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `darkside_S6` — keep → **`keep`**
* **El raster:** el match es un rectangulo gris bajo `re`, video inverso. Inmune a §0d. El knockout a 4,56:1 se ve.
* **80×24:** barra de teclas conservada.
* **Veredicto: `keep`.**

---

### 2.6 solari

`LEVELS "OK "/DLY/CNX` · `REQUIRED ▮` · `DANGER ▀▄` · `CUR ▼` · `SEAM ▁`.

#### `solari_S1` — nota → **`keep with a note`**
* **El raster refuta la objecion mas dura que la ronda cuatro le puso a este kit:** *«la costura va a 1,20:1 y son 2355 celdas, el 79 % de la superficie … el lenguaje ocupa cuatro quintas partes de la pagina y no se ve»*. **Se ve perfectamente.** Cada fila de tarea lleva su subrayado y el tablero de horarios se lee como un tablero de horarios (§0b: 100 celdas seguidas).
* **Objecion en pie, y ahora es la unica:** dos filas por tarea. `BACKLOG 5` gasta cinco filas para ensenar dos, y `GATE DONE 07` ensenia una cabecera y nada.
* **80×24:** aguanta; el detalle recorta el titulo.
* **Veredicto: `keep with a note`.**

#### `solari_S2` — nota → **`keep`**
* **El raster:** `▮` obligatorio en ambar, producto **1,794**, el segundo mejor del corpus. El error se llama `CNX`, una palabra. Los tags dicen `OFF` y `ON` con letras. **Es el unico formulario de los once cuyo estado se puede leer con todos los glifos borrados.**
* **Los tres criterios del brief responden:** que campos son obligatorios (dos, en ambar), que fila esta en error (`CNX`, en rojo), que tags estan puestos (`ON`, en palabras).
* **La exencion de `mut` (3,65:1) sobrevive la inspeccion:** las etiquetas se leen a 16 px.
* **80×24:** identico.
* **Veredicto: `keep`.**

#### `solari_S3` — keep → **`keep`**
* **El raster:** `▼ ON` / `▼ OFF`. Nada que interpretar.
* **Nota en pie:** `▼` es `CUR`, la perilla del switch, la flecha del select, el radio elegido y la perilla del slider, cinco oficios en una hoja y todos en ambar.
* **80×24:** identico.
* **Veredicto: `keep`.**

#### `solari_S4` — nota → **`rework`**
* **El raster invierte la objecion de la ronda cuatro y encuentra una peor.** La banda **ABRE** con una barra ambar de cien celdas (fila 10, cien espacios sobre `#f5a300`) y **CIERRA** con cien `▁` de `seam` a **1,20:1**. La ronda cuatro escribio *«cierra y no abre»* leyendo el `.txt`, donde la fila 10 esta vacia. **Los dos extremos de la banda estan en los dos extremos del peso visual del kit, y ningun instrumento del programa puede ver el abridor porque esta hecho de espacios** (§0a).
* **Criterio observable:** en `solari_S4.png`, senialar el principio y el final del modal. El principio salta a la vista; el final hay que buscarlo. La respuesta no es «sin respuesta»: es **«las dos respuestas son correctas y estan a 14× de distancia en contraste»**.
* **Segundo eje, y sale de inc78:** **la ruling F va en rojo a 24 filas.** *Un confirm nunca tapa la puerta que nombra*: a 100×32 un confirm sobre `DOING` deja su banda en 24-28, por debajo del bloque; a 80×24 no hay debajo, la banda cae en 17-22 y se come las filas 17 y 18, que son las salidas de `DOING`. Es un hallazgo de ALTURA con ropa de ancho. §8.
* **En pie:** la cabecera de la fila 10 abre con `▼`, que es `CUR`.
* **Veredicto: `rework`.** Duenio: `Solari.band_head`. Dos ejes, los dos con criterio escrito.

#### `solari_S5` — nota → **`keep with a note`**
* **El raster:** `OK / DLY / CNX` sigue siendo el mejor log de los once por un margen amplio, y es el unico que no depende de ningun token de cromo.
* **Objecion en pie, y el raster la agrava:** la sparkline es **`1212123211222122`**, dieciseis digitos. En el PNG parece un numero de serie. **Criterio:** decir si el ritmo sube o baja. Sin respuesta sin leer dieciseis cifras.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `solari_S6` — nota → **`keep with a note`**
* **El raster:** el match en video inverso ambar es excelente.
* **C6 en pie y mas visible que nunca:** el estado vacio de una busqueda fallida dice **`NO DEPARTURES`**. Con la pantalla delante se lee como un tablero de aeropuerto sin vuelos, que es la doctrina, y sigue siendo la respuesta equivocada a «tu busqueda no encontro nada».
* **80×24:** barra de teclas conservada.
* **Veredicto: `keep with a note`.**

---

### 2.7 blueprint

`LEVELS "  "/╌╌/━━` · `REQUIRED ═` · `DANGER ━━` · `CUR ┌` · `FIELD_LEAD ·─`.

#### `blueprint_S1` — nota → **`keep with a note`**
* **El raster refuta la nota de la ronda cuatro:** `dim #24486b` a 1,24:1 son los terminadores de cota, la firma del lenguaje, y **a 16 px la hoja de delineacion entera se lee** (§0b: 55 celdas seguidas).
* **Objecion nueva:** el mascot del estado vacio esta dibujado en **`ink`**, el token reservado para los titulos de tarea, y es lo mas brillante de la pantalla. Es la version blueprint de la objecion de `industrial_S1`, y la peor de las tres porque gasta el token mas alto.
* **80×24:** el medidor `WORK` pierde el `44%` sin decirlo.
* **Veredicto: `keep with a note`.**

#### `blueprint_S2` — nota → **`keep with a note`**
* **El raster:** `═`, `╞` y `╡` en la fila 3 son tres horizontales dobles y se distinguen por los extremos. El `ERROR_FILL` de 50 `╌` sigue fuera de todo instrumento.
* **A favor:** `═` obligatorio mide **1,484** en el asiento declarado.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `blueprint_S3` — rehacer → **`keep with a note`**
* **K4 en el frame, RESPONDIDA, y no por donde se esperaba.** El eje era *«tres horizontales distinguidas por cuenta de guiones, `╌` (2), `┄` (3), `┈` (4), a 12 px»*. inc72 retiro `┄` y `┈` del kit y movio el peldanio `warn`, asi que **la escalera de cuenta de guiones ya no esta en el frame**. Lo que queda en el PNG son cinco switches que se separan por **LARGO DE PISTA**: linea larga con terminador (encendido), munion corto (apagado), punteado palido (muerto).
* **Criterio observable, el mismo de tres rondas:** tapar las etiquetas y decir cuales de los cinco switches estan encendidos y cual esta muerto. **Responde.** Cierra el ultimo `rework` de los 42 originales.
* **C9 en pie:** la fila 18 dibuja el caption destructivo como una fila de campo.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `blueprint_S4` — nota → **`rework`**
* **El raster convierte un limite de metodo en un defecto de disenio.** El modal se delimita con **cuatro esquinas sueltas** `┌ ┐ └ ┘` separadas **44 celdas en horizontal (396 px)**. A 16 px el ojo **no cierra ese hueco**: son cuatro marcas, no un rectangulo. La ronda cuatro escribio que era *«la unica de las 66 que sigue siendo un limite de metodo y no de disenio»*; con la foto delante deja de serlo.
* **Criterio observable:** en `blueprint_S4.png`, senialar el borde del modal. Sin respuesta: se senialan cuatro puntos.
* **Y la prueba de que el vocabulario no esta roto, solo mal escalado:** en la MISMA pantalla, la tira de modos usa `┌ ┐` / `└ ┘` a **dos celdas** de separacion y ahi **si** se lee como una caja. **La ley que falta es de distancia, no de glifo.**
* **80×24:** identico defecto, mismas 44 celdas.
* **Veredicto: `rework`.** El eje: **un par de esquinas deja de ser una caja pasada cierta separacion, y esa separacion no esta escrita en ninguna parte.**

#### `blueprint_S5` — nota → **`keep with a note`**
* **El raster confirma la doctrina por su contenido:** blueprint no dibuja el peldanio calmo, y sus dos peldanios dibujados (`╌╌` 4,65:1 y `━━` 10,60:1) son **la pareja mas legible de los once**. De los nueve kits que no clasifican por `info`, es el unico honesto.
* **L6 en pie:** la sparkline gasta los peldanios altos.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `blueprint_S6` — keep → **`keep with a note`**
* **El raster a favor:** el match a 2,28:1 mas el peso se lee; el vocabulario de esquinas funciona a corta distancia.
* **Lo que baja la etiqueta:** **a 80×24 la barra de teclas desaparece.** Mismo motivo que `instrument_S6`.
* **Veredicto: `keep with a note`.**

---

### 2.8 naught

`LEVELS ◦◦/∙◦/∙∙` · `REQUIRED ⊛` · `DANGER ∙∙` · `CUR ●` · `FIELD_LEAD ◦`.

#### `naught_S1` — nota → **`keep with a note`**
* **El raster confirma el traslado de inc67 y lo empeora:** las trece `◉` de la barra de 44 % son, a 16 px, **trece anillos con punto**, y el checkbox marcado de `S2` es el mismo anillo con punto. **Criterio observable:** decir si las trece celdas de la fila 13 son un porcentaje o trece casillas marcadas. Con la foto delante, un lector dice casillas.
* **En pie:** quedan 57 `∙` y dos son la severidad.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `naught_S2` — rehacer → **`rework`**
* **L10 confirmada en pixeles, sin margen.** La fila de radios (`○ ○ ◉`) y la de tags (`◦ ◉ ◉`) son, en el PNG, **dos filas de circulitos, uno hueco y uno lleno en las dos**. **Criterio, sin cambios en tres rondas:** tapar la columna de etiquetas y decir cual fila es una eleccion unica y cual son casillas independientes. **Sin respuesta.**
* **Eje nuevo que L10 no nombra:** `⊛` (`REQUIRED`) tiene radios de un pixel a 16 px y se lee como **un anillo**, es decir, como `○`, el radio sin elegir. La marca de obligatorio y el estado «no elegido» son el mismo dibujo en la misma pantalla.
* **80×24:** identico.
* **Veredicto: `rework`.** Doce filas de censo, dos ejes, una foto.

#### `naught_S3` — nota → **`keep with a note`**
* **El raster:** la parte viva del slider son nueve `∙` y el boton irreversible es `∙Delete all∙`. Lo que separa a los dos en la foto es el PESO del texto, no la celda. **Criterio:** tapar las palabras y decir cual tirada es un valor y cual un boton. Sin respuesta.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `naught_S4` — rehacer → **`rework`**
* **El raster confirma la objecion y anade una.** Las filas 13 y 20 son cien `∙` cada una y en el PNG son **dos reglas punteadas**, lo mas destacado de la pantalla; y `∙` es el `DANGER_FORM`. **Criterio, sin cambios:** senialar las celdas que significan «irreversible». 237 candidatas, dos correctas, y las 200 mas grandes y contiguas son el marco del modal.
* **Objecion nueva, del raster:** el tablero de detras va en `dim #242424` sobre `#000000`, **1,35:1, y en el PNG practicamente no esta**. La afirmacion «el confirm conserva el tablero» es cierta en el `.txt` y falsa en la pintura.
* **80×24:** las dos reglas siguen; el tablero de detras sigue igual de ausente.
* **Veredicto: `rework`.**

#### `naught_S5` — nota → **`keep with a note`**
* **El raster:** `◦◦ / ∙◦ / ∙∙` es la escalera de pasos mas cortos del corpus que todavia tiene tres peldanios visibles. `◦` es el numero 8 de los diez peores (0,154) y **en la foto se ve mejor que varios que estan por encima**, porque un anillo tiene contorno: §7 lo usa para recomendar un piso y no una tabla de posiciones.
* **En pie:** la sparkline en braille en un lenguaje de circulos.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `naught_S6` — nota → **`keep with a note`**
* **El raster:** el separador de la barra de teclas sigue siendo `∙`, el `DANGER_FORM`, cuatro veces, y en la foto son cuatro puntos entre palabras: benignos por contexto, identicos por dibujo.
* **80×24:** barra de teclas conservada.
* **Veredicto: `keep with a note`.**

---

### 2.9 corgi

`LEVELS ▁▁/▄▄/██` · `REQUIRED ▀` · `DANGER ██` · `CUR ▐` · `FIELD_LEAD ""`.

#### `corgi_S1` — nota → **`keep with a note`**
* **El raster afloja la objecion nueva de la ronda cuatro:** las dos `█` que quedan (la pagina actual del pager) van en **verde de acento**, no en el rojo del error, y en la foto se leen como «estas aqui». **Criterio:** senialar lo irreversible. Dos candidatas, cero correctas, y ninguna de las dos se parece al `██` del error.
* **En pie:** `▓` (45 celdas) es el checkbox marcado y la pista encendida del switch; el tabique de 25 celdas esta dibujado con esa marca.
* **80×24:** `D E T A I L` pierde el titulo de la tarea entero y el medidor se corta en `[ 44%`.
* **Veredicto: `keep with a note`.**

#### `corgi_S2` — nota → **`keep with a note`**
* **El raster afila la objecion del tercer registro:** `▒◦ low ▒◦ norm ▒● high` en un lenguaje cuyo alfabeto es bloques al 100 %. En la foto **el circulo es la marca mas pequenia de la pantalla (10 % de tinta) y el bloque la mas grande (100 %)**: es el mayor salto de peso dentro de un mismo kit del corpus, y esta en la fila que elige la prioridad.
* **A favor:** `▀` obligatorio mide **9,786**, el mejor de los once por un factor de cinco; y los tags dicen `ON`.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `corgi_S3` — nota → **`keep with a note`**
* **El raster:** el eje del slider, la pista del switch y el relleno del medidor son **el mismo bloque verde**. Seis de las dieciseis filas de `FILL_IS_NOT_A_MEANING` son de corgi y en la foto son una sola textura repetida.
* **Criterio:** tapar el `[70]` y decir si la fila 16 es un valor o cinco calificaciones. Sin respuesta.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `corgi_S4` — nota → **`keep with a note`**
* **inc75 funciona en pixeles.** Las dos barras `▓` de `PANE_RULE` **se ven** como abridor y cierre. **Criterio (donde empieza y donde acaba el modal):** responde por primera vez en cuatro rondas. Los tres criterios escritos sobre este frame responden hoy: el modo (fila 1), la puerta (`from BACKLOG`) y los bordes.
* **Lo que queda, y esta ruled:** treinta de treinta y dos filas en negro. En la foto la aplicacion parece haberse ido. Es una decision escrita, con precio escrito.
* **80×24:** mismas dos barras, veinte filas en negro.
* **Veredicto: `keep with a note`.**

#### `corgi_S5` — nota → **`keep with a note`**
* **El raster revierte la mitad de la objecion.** `▁▁ / ▄▄ / ██` es **la mejor escalera del corpus en pixeles**: tres alturas de bloque, monotona en area y en contraste, y el peldanio bajo **se ve** porque es una barra de 18 px de ancho pegada a la linea base (§0b). La bajada de §0b se apoyaba en 1,71:1.
* **L6 en pie:** la sparkline usa `▄` y `█`, seis filas encima del log que los usa como severidad, y en la foto son el mismo verde.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `corgi_S6` — nota → **`keep with a note`**
* **El raster:** cero `█`; el mascot es `▓` en naranja apagado. **Criterio:** senialar lo irreversible. Cero candidatas.
* **En pie, benigno:** el mascot lleva la marca del checkbox marcado, y en esta pantalla no hay casillas.
* **80×24:** barra de teclas conservada.
* **Veredicto: `keep with a note`.**

---

### 2.10 prism

`LEVELS ⣀⣀/⣤⣤/⣿⣿` · `REQUIRED ⡀` · `DANGER ⣿⣿` · `CUR ▸` · `FIELD_LEAD ⡀⡤⣶`.

#### `prism_S1` — nota → **`keep with a note`**
* **El raster:** L9 respondida y visible. Doce celdas densas y quince ligeras, en ese orden. Y lo que el svg no podia ensenar: **`⣿` es una trama de 2×4 puntos con huecos, al 44 % de cobertura**, no un bloque; el techo de densidad de prism es una pantalla de semitono.
* **En pie:** el guia de campo `⡀⡤⣶` abre con `REQUIRED` en seis filas de solo lectura, y en la foto `⡀` es un punto de dos pixeles: la exencion sigue sin verse ni a favor ni en contra.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `prism_S2` — nota → **`rework`**
* **El eje nuevo, medido en el asiento declarado:** `⡀` (`REQUIRED`) en la fila 3 mide **cobertura 5,3 % · efectivo 4,42 · declarado 16,02:1 · producto 0,233**. Es **el peor obligatorio del corpus** y tiene el segundo mejor ratio de contraste de los once. En el PNG es un punto abajo a la izquierda de la celda.
* **Criterio observable:** en `prism_S2.png`, senialar los campos obligatorios. **Sin respuesta.**
* **En pie, y confirmado en la foto:** `⠉` es la marca del checkbox marcado (fila 11), el relleno del radio sin elegir (fila 9) y el papel del campo normal (fila 4). Tres roles, dos filas, un dibujo.
* **En pie:** el campo invalido no tiene fondo (`⠀`) y sus dos paredes `⣹`/`⣏` son imagenes espejo.
* **80×24:** identico.
* **Veredicto: `rework`.** Mismo eje que `instrument_S2` y misma forma de arreglo: una tupla.

#### `prism_S3` — nota → **`keep with a note`**
* **El raster:** el mejor arreglo de los nueve incrementos aguanta. `⣿` solo en `⣿Delete all⣿`, y la brasa se ve.
* **En pie:** las dos celdas del slider son las dos paredes del boton irreversible cuatro filas mas abajo.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `prism_S4` — nota → **`keep with a note`**
* **El raster:** modal cerrado por cuatro lados **mas un plato** (`#1f2630`), que es la tercera de las 18 tiradas en blanco sobre segundo ground de §0a. El plato se ve y ningun instrumento lo cuenta.
* **En pie:** el mascot en la misma pantalla que el confirm.
* **80×24:** la caja aguanta entera.
* **Veredicto: `keep with a note`.**

#### `prism_S5` — nota → **`keep with a note`**
* **El raster:** prism sigue siendo el unico de los once que pinta su peldanio `info` por encima de 3:1, y **se ve**: `⣀⣀` es un par de puntos bajos legible. La escalera es monotona por cuenta de puntos, por area y por contraste.
* **En pie:** la sparkline en elementos de bloque en un lenguaje de braille, y en la foto el contraste de vocabulario es evidente.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `prism_S6` — nota → **`keep with a note`**
* **El raster:** el match en verde azulado con peso se ve; 1,58:1 de luminancia con 40° y pico de matiz (§0d). La objecion de la ronda cuatro por la CIFRA queda retirada.
* **Lo que queda, y es lo unico:** `#2dd4bf` es el acento de match de prism **y** de instrument, y en los dos es la tinta del cursor de la misma fila.
* **80×24:** **se cae la barra de teclas.**
* **Veredicto: `keep with a note`.**

---

### 2.11 ledger

`LEVELS "  "/"* "/"**"` · `REQUIRED †` · `DANGER ( )` · `CUR ▶` · `FIELD_LEAD ·`. El unico kit de papel claro.

#### `ledger_S1` — nota → **`keep with a note`**
* **El raster refuta la objecion de la ronda cuatro.** *«Nombrar los cuatro modos. Responde uno.»* **Responden los cuatro:** `· form`, `· cfg` y `· log` se leen enteros a 1,50:1 porque son tinta oscura sobre papel claro (§0c). Y la reticula de columnas a 2,92:1, 1619 celdas, tambien.
* **Objecion en pie:** los dos paneles se tocan con tres `═` en la fila 4, y `═` es en todas partes la regla bajo una cabecera de puerta.
* **80×24:** la reticula aguanta; el detalle recorta el titulo y conserva los valores.
* **Veredicto: `keep with a note`.**

#### `ledger_S2` — nota → **`keep with a note`**
* **El raster confirma la objecion en su forma mas fuerte.** `†` (obligatorio, en `title` y `due`) y `‡` (invalido, en las paredes de la fecha) estan en la misma zona de la pantalla, a tres filas, y a 16 px **la unica diferencia son dos pixeles de travesanio**. `† ‡` mide 4,87 %.
* **Y una correccion al hallazgo 2 de inc77, medida aqui (§6):** el par mas apretado del censo, darkside `▪ ▫` a 3,20 %, **no se dibuja junto en ningun frame**. De las 24 filas del censo, **15 se dibujan juntas y 9 no**. **La pareja mas apretada que un lector puede llegar a ver de verdad es `† ‡` en `ledger_S2`**, que es donde la pusieron las rondas dos y tres.
* **En pie:** el campo enfocado abre con `▶` (`CUR`) y cierra con `│`, la regla de columna.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `ledger_S3` — nota → **`keep with a note`**
* **El raster confirma la segunda objecion sin discusion:** el switch apagado dice `open` y el deshabilitado dice `open`. Dos filas, la misma palabra, y lo unico que las separa es el gris. **Criterio:** decir cual switch esta deshabilitado. Responde el contraste, no la palabra.
* **Nota nueva, del raster:** `( Delete all )` es el `DANGER_FORM` de ledger, y en papel contable un parentesis es un negativo. Es la marca destructiva mas elegante del corpus **y la menos alarmante**: quien no lea contabilidad lee un inciso.
* **C9 en pie.**
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `ledger_S4` — rehacer → **`keep with a note`**
* **C2 CERRADA, y el raster lo confirma.** inc72 hizo que `Ledger.overlay_instead` construya `[regla] + filas + [regla]` y recorte la pagina. En el PNG la banda abre con una regla, cierra con otra, y **`(Delete)` ya no esta en la ultima fila del terminal**. **Criterio (decir donde termina el modal):** responde. Cuatro rondas, cerrada.
* **Lo que hay que escribir, y lo encuentra el segundo ancho:** el arreglo compro exactamente una fila, **y a 80×24 se la gasta**. La fila de respuestas queda en la 22 y el cierre en la 23, que es la ultima. El agravante que la ronda tres nombro vuelve a un pelo de distancia.
* **En pie:** las filas 27-32 arrancan en la columna 1 y las 1-25 en la 3.
* **Veredicto: `keep with a note`.**

#### `ledger_S5` — nota → **`keep with a note`**
* **El raster:** doctrina L7 confirmada por contenido, igual que blueprint. Los dos peldanios dibujados (`*`, `**`) se ven; el calmo no existe y eso esta declarado.
* **En pie:** la sparkline es una fila de cuadraditos y dos puntos; no se lee como tendencia.
* **80×24:** identico.
* **Veredicto: `keep with a note`.**

#### `ledger_S6` — nota → **`keep with a note`**
* **El raster:** el match es negrita mas subrayado sobre papel claro, **el mas legible de los once** junto con los tres de video inverso, y el unico que no depende del matiz.
* **C6 en pie:** el estado vacio de la busqueda dice `nil balance`.
* **80×24:** barra de teclas conservada.
* **Veredicto: `keep with a note`.**

---

## 3. Totales

|  | ronda 1 | ronda 2 | ronda 3 | ronda 4 | ronda 5 |
|---|---|---|---|---|---|
| frames juzgados | 42 | 42 | 66 | 66 | **66** |
| `keep` | 6 | 14 | 15 | 11 | **14** |
| `keep with a note` | 17 | 21 | 40 | 51 | **46** |
| `rework` | 19 | 7 | 11 | 4 | **6** |
| frames con `.txt` movido | - | 26 de 42 | 27 de 66 | 13 de 66 | **7 de 66** (inc72, inc75) |
| anchos juzgados | 1 | 1 | 1 | 1 | **2** |
| instrumento | lectura | lectura | lectura | `fill=` del svg | **pixeles** |
| celdas colisionantes (censo) | 54 | 48 | 25 | 30 | **28** |
| filas de homoglifo | - | 4 | 1 | 26 | **24** |
| filas de homoglifo **co-dibujadas en un frame** | - | - | - | - | **15 de 24** |
| tiradas en blanco sobre segundo ground | - | - | - | - | **18, en 3 kits, sin instrumento** |
| kits cuyo `info` se ve o es doctrina | - | - | - | 4 de 11 | **6 de 11** (+industrial, +corgi) |
| kits cuyo obligatorio se puede senialar | - | - | - | - | **9 de 11** |
| frames que pierden la barra de teclas a 24 filas | - | - | - | - | **4 de 11** |

**Los seis `rework`, y cada uno es un incremento de un fichero:**

* **1.** **Una marca de obligatorio sin area**, `instrument_S2` y `prism_S2`, la misma causa y la misma forma de arreglo (una tupla, `REQUIRED`).
* **2.** **Un abridor invisible para el aparato y ensordecedor para el ojo, mas una ruling en rojo a 24 filas**, `solari_S4`.
* **3.** **Cuatro esquinas que no son una caja**, `blueprint_S4`.
* **4.** **Un par sin canal**, `naught_S2`, con foto.
* **5.** **Un marco de modal dibujado con el `DANGER_FORM`**, `naught_S4`, sin tocar en catorce incrementos.

---

## 4. Donde cambio la objecion aunque el frame no

**Refutadas por el raster (cinco, y las cinco eran de la ronda cuatro):**

| # | frame | lo que decia la ronda cuatro | lo que ensenia el pixel |
|---|---|---|---|
| 1 | `solari_S1` | la costura a 1,20:1 es el 79 % de la pagina y no se ve | se ve limpiamente; 100 celdas seguidas |
| 2 | `ledger_S1` | nombrar los cuatro modos; responde uno | responden los cuatro (polaridad, §0c) |
| 3 | `darkside_S1` | senialar el escalon gris que separa los paneles, esta a 1,39:1 | es una columna maciza de dos celdas de ancho |
| 4 | `swiss_S1` | decir cuantas reglas hay; no se ven | se ven las cinco |
| 5 | `nord_S6` | la que mas empeoro de las 66, el match cayo a 1,38:1 | el match salta a la vista; el numero mide el eje equivocado |

**Invertida (una, y es la mas util):** `solari_S4`. La ronda cuatro escribio *«la banda cierra y no abre»*; la banda abre con la fila mas brillante del kit y cierra con la mas apagada. La lectura era correcta sobre el `.txt` y falsa sobre la pantalla, **porque el abridor esta hecho de espacios**.

**Confirmadas y agravadas por el raster (cuatro):** `naught_S2` (L10, dos filas de circulitos), `naught_S4` (dos reglas punteadas que son el `DANGER_FORM`, y un tablero de detras que no esta), `ledger_S2` (`† ‡` a dos pixeles de travesanio), `instrument_S4` (tres tramas identicas de cien celdas).

**Objeciones nuevas que solo un raster puede plantear (cuatro):**

* **1.** **El reparto de peso visual.** Los mascots de estado vacio de industrial (`alert`), blueprint (`ink`) y nord son lo mas llamativo de sus pantallas y significan «aqui no hay nada». Ninguna ley del suite mide cuanta atencion pide una celda.
* **2.** **La distancia a la que un par de esquinas deja de ser una caja** (`blueprint_S4`, 44 celdas si; 2 celdas no).
* **3.** **La trama contra el bloque.** `⣿` de instrument y de prism no es un bloque lleno: es una pantalla de semitono al 41 y al 44 %. Todo argumento de densidad de cuatro rondas sobre esos dos kits describe una textura y no un solido.
* **4.** **El salto de peso dentro de un kit.** corgi pone un circulo del 10 % de tinta en la fila de prioridad de un lenguaje de bloques del 100 %.

---

## 5. Las objeciones en pie, por quien las arregla

Solo las que cambian. El resto sigue como en la ronda cuatro §5.

### `Kit` y los tests

| # | objecion | estado |
|---|---|---|
| K4 | Ninguna ley compara dos estados de un mismo `part`. | **CERRADA como instrumento** (inc68) y **RESPONDIDA en el frame** (`blueprint_S3`, por largo de pista) |
| K6 | Ninguna ley lee el fondo que hay realmente debajo de un run. | **CERRADA** (inc73, `painted_runs()`) |
| K7 | Ninguna ley lee `dim` ni `alert`. | **CERRADA a medias** (inc73/inc74) y **REDEFINIDA**: §0b dice que la particion correcta es por largo de tirada, no por token |
| **K8** | **NUEVA. Ninguna ley ni instrumento lee una tirada SIN TINTA.** 18 tiradas de espacios sobre un segundo ground, en 3 kits, y una de ellas es el abridor de un modal. | **NUEVA Y ABIERTA** |
| **K9** | **NUEVA. Ninguna ley mide el AREA de una marca**, y las dos peores del corpus tienen los dos mejores ratios de contraste (`instrument ⠁` 16,52:1, `prism ⡀` 16,02:1). | **NUEVA Y ABIERTA.** §7 propone el piso |
| **K10** | **NUEVA. Ninguna ley mide la SEPARACION de un par de marcas que dice ser una caja.** | **NUEVA Y ABIERTA** (`blueprint_S4`) |

### Nivel lenguaje

| # | objecion | estado |
|---|---|---|
| L4 | Tres vocabularios de pared en una pantalla. | **ABIERTA en nord; ALIVIADA en swiss** (`╎` contra `│` se distinguen a 16 px) |
| L7 | `LEVELS["info"]` es aire en dos lenguajes. | **RULED como doctrina** y **medida**: se ve en industrial (17 % de area), corgi (16 %) y prism (3,25:1); es aire declarada en blueprint y ledger; y es **una marca invisible dibujada** en darkside, swiss, nord, instrument y naught. Cinco kits reclaman un canal que no tienen |
| L10 | El radio y el checkbox de naught se distinguen solo por diametro. | **ABIERTA, MEDIDA y FOTOGRAFIADA**, y con un eje mas: `⊛` obligatorio se lee como `○` |
| L11 | El match tier de tres kits se estrecho al subir `mut`. | **RETIRADA como objecion de legibilidad** (§0d). Los tres matches se ven |
| **L12** | **NUEVA. En tres kits el unico canal del match es el MATIZ** (nord, swiss, prism). En escala de grises no queda nada, y la clausula que los aprueba mide luminancia contra un `mut` acromatico, que es la dimension en la que menos se diferencian. | **NUEVA Y ABIERTA** |
| **L13** | **NUEVA. Dos kits gastan una celda sin area en `REQUIRED`** (instrument `⠁`, prism `⡀`). | **NUEVA Y ABIERTA** - es el eje de dos de los seis `rework` |

### Hoja y composicion

| # | objecion | estado |
|---|---|---|
| C2 | El modal abre con una regla y no cierra. | **CERRADA EN LOS ONCE.** inc66 swiss, inc72 ledger, inc75 corgi; confirmadas las tres en pixeles |
| C3'' | La banda de solari cierra y no abre. | **RETIRADA Y SUSTITUIDA** por C3''' |
| **C3'''** | **NUEVA. La banda de solari abre en el token mas brillante del kit y cierra en el mas apagado**, y el abridor no existe para ningun instrumento porque son espacios. | **NUEVA Y ABIERTA** (`solari_S4`) |
| C7 | Tres reglas identicas en una pantalla. | **ABIERTA, confirmada en pixeles** (`instrument_S4`: tres tramas de cien celdas indistinguibles) |
| C8 | El confirm borra la aplicacion entera. | **CERRADA A MEDIAS por ruling y RESPONDIDA en los bordes** (inc75, confirmado en pixeles) |
| **C12** | **NUEVA. A 24 filas, cuatro de los once pierden la barra de teclas de `S6`** (instrument, nord, blueprint, prism). Es la fila que ensenia como se sale. | **NUEVA Y ABIERTA** |
| **C13** | **NUEVA. A 80 columnas, el titulo del panel de detalle se trunca sin decirlo en los once**, y en swiss se truncan tambien los valores (`phase: do`). | **NUEVA Y ABIERTA** |
| **C14** | **NUEVA. El mascot del estado vacio es el elemento de mas peso visual de su pantalla en industrial (`alert`), blueprint (`ink`) y nord.** | **NUEVA Y ABIERTA** |

### Exportador

| # | objecion | estado |
|---|---|---|
| E2 | El `.svg` no lleva metrica de fuente. | **CERRADA** (inc76). Esta ronda es la primera que la gasta |
| **E6** | **NUEVA. El exportador pinta superficie sin glifo** (18 tiradas, 3 kits) **y ninguna ley puede nombrarla.** Es K8 desde el lado del artefacto. | **NUEVA Y ABIERTA** |

---

## 6. Los diez pares mas cercanos, mirados

Cada par se dibujo con `raster.cell_tile()` a **la medida del corpus** (Cascadia Mono 16 px en una caja
de 9×19) y se amplio con vecino mas proximo. **Volver a renderizar el glifo a 4× el cuerpo seria otra
rasterizacion, otra rejilla de hinting y otro conjunto de pixeles**; lo que se ensenia son los 171
pixeles exactos de los que estan hechos los 66 PNG, aumentados.

La distancia se volvio a derivar de forma independiente (diferencia de luminancia sobre el mosaico
compuesto, en vez de XOR de cobertura alfa). **El orden reproduce el del informe exactamente y el unico
cero reproduce exactamente**, a un factor de escala constante de 0,885. Es una comprobacion cruzada de
inc77 y sale limpia.

| par | inc77 | aqui | ¿lo confirma la foto? |
|---|---|---|---|
| `• ∙` | 0,00 % | **0,00 %** | **SI, y es la prueba.** El XOR es negro entero. Un disco y el mismo disco |
| `⋅ ⠀` | 1,38 % | 1,22 % | SI. `⋅` esta a **cuatro pixeles de una celda vacia** |
| `⊚ ⊛` | 1,46 % | 1,30 % | SI. Dos anillos que solo difieren en el centro; el centro mide 2 px a 1:1 |
| `⊖ ⊚` | 1,85 % | 1,64 % | SI, misma familia, misma razon |
| `─ ┈` | 2,00 % | 1,78 % | **NO.** El XOR son cuatro barras limpias: es una regla continua contra una punteada, y eso es una de las distinciones mas fiables que hay. **El area es un mal proxy cuando la diferencia es periodica** |
| `⊖ ⊛` | 2,27 % | 2,02 % | SI |
| `. :` | 2,39 % | 2,12 % | **NO.** Un punto contra dos: es una diferencia de CUENTA, y a 1:1 se lee sin esfuerzo en prosa |
| `. ⠀` | 2,39 % | 2,12 % | SI, trivialmente: un punto contra nada |
| `· ⠀` | 2,39 % | 2,12 % | SI, y es el numero que importa: **la marca mas dibujada del corpus (2496 celdas) esta al 2,39 % de una celda vacia** |
| `⠀ ⠄` | 2,52 % | 2,23 % | SI, nada contra un punto bajo |

**La lectura, y va a la recomendacion de §7:** de los diez, **seis tienen una celda vacia o una
diferencia de centro en uno de los lados**. Las distancias mas pequenias del instrumento estan
dominadas por «una marca chica contra nada», que es una afirmacion sobre AREA y no sobre confusion.
Los unicos pares que un lector puede confundir de verdad son `• ∙` (identicos) y los tres operadores
circulados. **El XOR es una cota inferior de la diferencia, no una medida de confundibilidad: la
periodicidad y la cuenta son canales que no ve.**

**Y el par que de verdad importa no esta en los diez.** De las 24 filas de homoglifo del censo,
**quince se dibujan juntas en algun frame y nueve no**, incluida la mas apretada:

| distancia | kit | par | ¿co-dibujado? |
|---|---|---|---|
| **3,20 %** | darkside | `▪ ▫` | **NO.** darkside dibuja `▫` **cero veces** en sus seis hojas |
| **4,87 %** | ledger | `† ‡` | **SI, `ledger_S2`**, a tres filas |
| 7,68 % | swiss | `· •` | SI, `swiss_S2` |
| 8,69 % | naught | `∙ ⋅` | SI, `S2` y `S3` |
| 17,61 % | naught | `◦ ◎` | NO |
| 21,56 % | darkside / solari | `O ◉` | NO en ninguno de los dos |
| 22,25 % | naught | `⊛ ◎` | NO |
| 25,75 % | naught | `⊛ ⊙` | NO |
| 29,32 % | nord | `· ●` | NO |
| 33,32 % | naught | `◦ ⊙` | NO |

**inc77 corrigio a tres documentos diciendo que el par mas apretado del censo es darkside `▪ ▫` y no
ledger `† ‡`. Sobre la DECLARACION tenia razon; sobre el CORPUS RENDERIZADO la tenian los tres
documentos**, porque `▪ ▫` no coincide en ninguna pantalla. La ronda corrige la correccion, que es
exactamente para lo que sirve una quinta vuelta con un instrumento nuevo.

**Y un aviso de medida:** el barrido de pares trata `o` y `O` como un par de homoglifo, y esas dos
letras coinciden en **56 de los 66 frames** por la simple razon de que el corpus escribe en ingles. El
censo cuenta prosa. No cambia ninguna fila de significado y hay que decirlo.

---

## 7. Las diez peores marcas de significado, miradas, y el piso que se recomienda

Las diez de `legibility.txt` D1, dibujadas a la medida del corpus y ampliadas, y ademas repetidas ocho
veces a 1:1, que es como las ve el operador.

| # | kit | marca | familia | cob | efect | producto | ¿se encuentra a ojo a 16 px? |
|---|---|---|---|---|---|---|---|
| 1 | darkside | `·` | severidad | 4,7 % | 1,13 | 0,053 | **No.** Una mota de 2×2 al borde del ruido |
| 2 | swiss | `·` | severidad | 4,7 % | 1,28 | 0,060 | **No** |
| 3 | nord | `·` | severidad | 4,7 % | 1,30 | 0,061 | **No** |
| 4 | instrument | `⠂` | severidad | 5,3 % | 1,24 | 0,065 | **Apenas.** Un punto bajo; se intuye la fila, no la marca |
| 5 | instrument | `⠁` | obligatorio | 5,3 % | 1,24 | 0,065 | **No.** Y solo se distingue de `⠂` por la ALTURA dentro de la celda |
| 6 | prism | `⡀` | obligatorio | 4,7 % | 1,77 | 0,083 | **No.** El peor obligatorio del corpus |
| 7 | prism | `⣀` | severidad | 9,9 % | 1,46 | 0,145 | **Si, a duras penas.** Dos puntos bajos hacen una linea base |
| 8 | naught | `◦` | severidad | 13,5 % | 1,14 | 0,154 | **Si.** Un anillo tiene contorno y el ojo lo engancha |
| 9 | naught | `∙` | peligro+severidad | 14,0 % | 1,20 | 0,169 | **Si, la mas facil de las diez.** Un disco macizo |
| 10 | instrument | `⠇` | severidad | 15,8 % | 1,24 | 0,196 | **Si, pero peor que la 8 y la 9** pese al producto mas alto |

**El producto ordena las diez en un orden que la foto no reproduce.** Coinciden en el fondo (las tres
`·`) y en la cabeza (`∙`, `◦`) y discrepan en el medio, porque un contorno cerrado se encuentra mejor
que la misma area repartida en puntos sueltos. **El producto es un buen colador y una mala tabla de
posiciones**, y eso es justo lo que un piso tiene que ser.

### Las tres preguntas de inc77, con recomendacion

> **(1) ¿Es cobertura × efectivo la medida, o cobertura Y efectivo como dos clausulas con dos pisos?**

**DOS CLAUSULAS, con dos pisos: cobertura ≥ 15 % de la celda Y contraste efectivo ≥ 3:1**, las dos en
el asiento declarado. **Razon, medida en esta ronda:** el producto mezcla dos fallos con dos arreglos
distintos y la foto los separa. `prism ⡀` esta a **16,02:1** y no se ve: subirle el contraste no compra
nada porque el problema son tres pixeles, y el arreglo es dibujar otra celda. `solari ▁` esta a
**1,20:1** y se ve: el arreglo ahi no es ninguno. Un solo numero esconde esa diferencia; dos clausulas
la nombran y cada una apunta a su arreglo. Bajo estas dos clausulas, **los once obligatorios pasan el
contraste y dos fallan la cobertura** (instrument 5,8 %, prism 5,3 %), que es exactamente el resultado
que la pantalla da.

> **(2) ¿Vincula a toda marca de significado, o solo a las que una lista tipo `DIM_CLASSIFIES` diga que clasifican?**

**A las que clasifican, y la lista deja de escribirse a mano: el criterio es el LARGO DE TIRADA.**
§0b es la evidencia. Propuesta mecanica:

* **tirada de 1 a 4 celdas** de un glifo que lleva una familia de `A_FAMILIES` en ese asiento: **es
  significado y esta vinculada** por las dos clausulas de (1);
* **tirada de 8 celdas o mas** de un mismo glifo: **es estructura** (costura, regla, guia, cota,
  papel) y esta vinculada solo a *«no ser igual al fondo»*, porque la continuidad sustituye al area;
* **5 a 7 celdas:** se nombra, asiento por asiento, exactamente como hace `DIM_CLASSIFIES` hoy.

Esto convierte §8.4 de la ronda cuatro (*«esta ronda no resuelve cuales son decoracion»*) en
aritmetica, y la evidencia es que **todas las marcas que esta ronda encontro legibles por debajo del
piso son largas y todas las que encontro invisibles son cortas**, sin una sola excepcion en los 66.

> **(3) ¿Se juzga una marca en su peor asiento o en el declarado?**

**En el DECLARADO, con el peor reportado como aviso y nunca como rojo.** Dos razones medidas aqui:
el peor asiento del corpus es casi siempre el DECORATIVO (`instrument ·` en un masthead, `ledger ·` en
una guia), asi que juzgar por el peor suspende a un kit por su decoracion; e inc74 ya juzga asientos de
uno en uno y un mismo glifo puede ser legitimamente dos cosas. La tabla del asiento declarado (§2.2 de
`instrument_S2` y §2.10 de `prism_S2`) es la que produce el veredicto correcto en los dos casos donde
esta ronda cambia una etiqueta.

**Y el piso NO se enuncia como ranking.** §7 arriba es la razon: el orden que produce no es el orden
que ve un lector. Un umbral que separa «se encuentra» de «no se encuentra» es defendible; una tabla de
posiciones no lo es.

---

## 8. Los dos rojos de solari a 80×24, y que hacer con cada uno

inc78 corrio 79 brazos de ley con `FRAMES` apuntando a `w80/`, con un brazo de control a 100×32
primero. **77 verdes, 2 rojos, los dos de solari.**

### Rojo 1, la ruling F falla a 24 filas, y es un hallazgo de ALTURA

`test_a_solari_confirm_never_covers_the_gate_it_names`. El primer brazo (el frame enviado, sobre
`BACKLOG`) es verde a los dos tamanios. El que se pone rojo es el que inc55 anadio: **preguntarle al
MECANISMO lo mismo una vez por cada puerta de la pagina.** A 100×32 un confirm sobre `DOING` deja su
banda en 24-28, limpiamente por debajo del bloque de `DOING` (9-18); a 80×24 no hay debajo, la banda
cae en 17-22 y se come las filas 17 y 18, que son las salidas de `DOING`. **La regla de colocacion se
escribio, y se probo, en una pagina que siempre tenia adonde ir.**

**Recomendacion, y son tres opciones ordenadas:**

* **1.** **La que se recomienda: el ancla deja de ser «debajo del bloque» y pasa a ser «la posicion a medida
   completa mas cercana que no corta ningun bloque de puerta», probando debajo primero y encima
   despues.** Es un cambio en `Solari.band_head`, conserva la ruling F palabra por palabra y la hace
   cierta a cualquier altura. La ley no se toca.
* **2.** Si no cabe en ninguna de las dos posiciones a la altura dada, **la banda toma la pagina entera** y
   el confirm deja de ser una banda: es un confirm de pantalla completa, que es lo honesto a 24 filas y
   lo que hace corgi por doctrina.
* **3.** **Ultimo recurso, y hay que escribirlo si se toma:** declarar una altura minima para solari
   (`H ≥ 28`) y que el kit se niegue a renderizar por debajo. Es aceptable y hay que decirlo en
   `LANGUAGES.md`, porque contradice *«at any width»*.

**Lo que NO se recomienda: relajar la ruling F al brazo del frame enviado.** El brazo que se pone rojo
es el que inc55 anadio precisamente para que una colocacion afortunada no pasara por buena.

### Rojo 2, una ley atada a un ancho, y el frame tiene razon

El brazo de solari de `test_a_confirm_opens_and_closes_on_marks_of_its_own` comprueba que el plato de
la banda esta a medida completa con `any(w > 800)` sobre los `<rect>` del svg. **800 es 100 celdas ×
8,4 unidades.** A 80 columnas el plato mide 672 unidades y **si esta a medida completa**. El frame es
correcto y la ley esta mal.

**Recomendacion:** la clausula se deriva del propio frame, no de una constante.
`max(w) >= cols * CELL_W * 0,95`, con `cols` leido del `.txt` que la ley ya abre. Es una linea, cierra
el rojo sin mover un pixel, y **no debe tomarse en el incremento que lo encontro** (inc78 hizo bien en
dejarlo escrito).

**Y hay una tercera cosa que decir aqui**, porque este rojo la destapa: **esa clausula del ancho es la
UNICA del suite entero que lee una superficie sin glifo.** Es lo que hace que el plato ambar de §0a
tenga alguna ley encima, y lo tiene por accidente. K8 propone que deje de ser un accidente.

### Y lo que el segundo ancho encontro sin que ninguna ley lo pidiera

* **C12: cuatro de los once pierden la barra de teclas de `S6` a 24 filas** (instrument, nord,
  blueprint, prism). Siete la conservan. Es la fila que dice como se cierra la paleta.
* **C13: los once truncan el titulo del panel de detalle a 80 columnas sin decirlo.** Diez alinean los
  valores a la derecha y los salvan; **swiss los alinea a la izquierda y los corta**: `phase: do`,
  `priority: hi`, `owner: ja`. Un frame que afirma algo falso.
* **`ledger_S4` gasta a 24 filas la fila que inc72 le compro:** la respuesta destructiva queda en la
  22 y el cierre en la 23, la ultima.
* **Las cinco cajas de modal reales (industrial, nord, darkside, prism, y la banda de corgi) aguantan
  enteras a 80×24.** Ninguna se rompe, ninguna pierde un lado. Es el mejor resultado del segundo ancho
  y hay que escribirlo tan claro como los rojos.

---

## 9. Lo que esta ronda no puede ver

* **1.** **No se ejecuto nada.** Se miraron 132 PNG, se leyeron los 132 sidecars `.json`, los 66 `.txt` a los dos anchos, `legibility.txt`, `spec.md` §19–§20 y los cinco packets. **No se ejecuto la aplicacion, no se pulso ninguna tecla, no se movio ningun foco y no se corrio la suite.** Los numeros de puertas citados (1370 passed, censo 28, 24 filas, 79 brazos, 2 rojos) estan **leidos de `spec.md` y del disco**, no reproducidos aqui. Lo que esta ronda calculo por su cuenta: las 18 tiradas en blanco, las 15 de 24 filas co-dibujadas, los productos en el asiento declarado de los once obligatorios, los largos de tirada, y la re-derivacion independiente de los diez pares.

* **2.** **Una fuente, un cuerpo, un tamanio de celda.** Cascadia Mono 16 px, 9×19. Windows Terminal dibuja **sus propios** glifos de caja y de bloque, asi que toda fila de este documento cuyo glifo sea box drawing o block element es un hecho sobre la version de Cascadia y no necesariamente sobre lo que vera el operador. La escalera de corgi, las esquinas de blueprint y las paredes de industrial estan en esa clase.

* **3.** **Un solo ojo, y es el mismo que escribe.** «¿Se encuentra a ojo?» de §7 es un juicio de quien redacta, hecho sobre imagenes ampliadas y sobre tiras a 1:1, no un experimento. Esta declarado par por par para que se pueda discutir cada uno; no esta medido.

* **4.** **Nada sobre movimiento.** Antialiasing y gamma del monitor del lector siguen fuera. Un raster estatico tampoco dice nada de parpadeo, de refresco ni de como se lee una pantalla que cambia.

* **5.** **El foco sigue siendo decoracion.** `FOCUSED` se lee de una marca. Tab order, atrapado de foco en el modal y viaje del anillo siguen sin tocarse, y `App.run_test()` + `Pilot` sigue siendo el mecanismo real que existe y no se ha usado. Es la ultima de las tres cosas que la ronda cuatro pidio y la unica que sigue sin construirse.

* **6.** **El stepper.** Ley desde inc51, cero artefactos, quinta ronda.

* **7.** **Usuarios reales.** ISO 9241-210 pide evaluacion con usuarios; este equipo es una persona. Lo que hay aqui es **inspeccion con criterios declarados**, un recorrido cognitivo sobre las tareas que el contexto de uso nombra, ahora sobre la pintura real y a dos tamanios. **No se hizo ninguna evaluacion con usuarios reales, y ninguna afirmacion de este documento debe leerse como si se hubiera hecho.** En particular, §7 llama «se encuentra a ojo» a algo que un experimento con personas podria contradecir en cualquiera de las diez filas.

---

## 10. Convergencia

### 10a. Que encontro el raster que cuatro rondas de svg no pudieron

Cinco cosas, y ninguna es de grado: son de clase.

* **1.** **Superficie sin tinta.** 18 tiradas de espacios sobre un segundo ground, invisibles para el censo, para los homoglifos, para `painted_runs()` y para la cobertura, y **una de ellas es el abridor mas ruidoso del corpus**. Cuatro rondas de instrumentos leen glifos y esto no es un glifo.
* **2.** **La continuidad.** La misma celda al mismo contraste se ve a 55 celdas de largo y no se ve a una. Eso parte las once tiradas de `dim` por una regla mecanica y cierra §8.4 de la ronda cuatro, que estaba escrita como irresoluble.
* **3.** **El area contra el ratio.** Los dos obligatorios que nadie puede senialar tienen los dos mejores ratios de contraste de los once. Ninguna clausula de contraste de este programa puede producir ese hallazgo, por construccion.
* **4.** **La polaridad y el matiz.** WCAG es simetrico y aqui hay un kit claro que gana; la distancia de matiz contra un `mut` acromatico cae a una clausula de luminancia que mide la dimension equivocada, y por eso la peor regresion de la ronda cuatro no era una regresion.
* **5.** **La distancia.** Un par de esquinas es una caja a dos celdas y son cuatro marcas a cuarenta y cuatro. Es una ley que falta y que nadie podia escribir sin mirar.

### 10b. Que dice que si converge

* **`blueprint_S3` cierra**, y con el el ultimo `rework` de los 42 originales. Sobre los 42 la serie es **19 → 7 → 3 → 1 → 0**.
* **C2 esta cerrada en los once**, confirmada en pixeles en swiss, ledger y corgi.
* **Los seis `rework` son seis ediciones de un fichero cada una**, y dos de ellos (`instrument_S2`, `prism_S2`) son literalmente la misma tupla en dos kits.
* **Cinco objeciones de la ronda anterior se retiran por medicion, no por cansancio.** Es la primera vez en el programa que una ronda retira objeciones de la anterior con evidencia y no con una ruling.

### 10c. Que dice que no

* **El instrumento nuevo encontro una clase nueva en su primera pasada, otra vez.** K8, K9, K10, L12, L13, C3''', C12, C13, C14, E6: **diez objeciones nuevas**, contra seis de la ronda cuatro y ocho de la tres. **La tasa de hallazgo subio.**
* **Y el patron que los packets vienen nombrando desde §17.7 no se ha roto, solo cambio de eje.** inc63 escribio `contrast(ink, ground)` y encontro `mut`; inc70 escribio `contrast(mut, ground)` y encontro `dim`; la ronda cuatro escribio «contra lo que hay realmente debajo» y encontro los segundos grounds; **esta ronda miro los pixeles y encontro la superficie que no tiene pixeles de tinta.** Cinco iteraciones, exactamente una incognita nueva por vuelta.
* **Tres de las cinco cosas de §10a son sobre el INSTRUMENTO y no sobre los kits.** Un programa cuya quinta vuelta dedica la mayor parte de sus hallazgos a corregir sus propias mediciones no ha terminado de medir.

### 10d. El veredicto, y que necesitaria una sexta ronda

**El instrumento convergio; la pregunta no.** La ronda cuatro dijo *«la serie de rondas ha convergido;
el programa no»* y recomendo cambiar el instrumento. Se cambio, y el cambio produjo diez objeciones
nuevas y siete cambios de etiqueta en las dos direcciones. **Eso es exactamente lo que se pidio, y es
la razon por la que no se puede decir que esto haya terminado.**

Pero hay que ser preciso sobre que tipo de ronda seria util ahora, porque **una sexta lectura del mismo
raster no lo seria.** Las tres cosas que anadirian informacion, en orden de lo que compra cada una:

* **1.** **Una persona.** Es la unica de las tres que compra una clase de hallazgo entera y es la que lleva pedida desde la ronda uno. **Los criterios ya estan escritos: hay veintitantas frases de la forma «senialar la celda que significa que esto destruye datos» repartidas por cinco documentos, y ninguna se ha ejecutado nunca sobre un ser humano.** No hace falta un estudio: hacen falta seis pantallas, seis preguntas y una persona que no haya visto el kit. §7 de esta ronda es la que mas lo necesita, porque «se encuentra a ojo» lo decidio quien escribe.
* **2.** **Una tecla.** `App.run_test()` + `Pilot` existe, es el mecanismo real de esta pila, y sigue sin usarse en cinco rondas. Tab order, atrapado de foco en el modal y viaje del anillo son la parte de *«el disenio atiende la experiencia completa»* que este corpus no ha tocado nunca. **Un frame no puede fallar en foco porque un frame no tiene foco**, y por eso las cinco rondas dan `keep` a modales cuyo comportamiento de foco nadie ha visto.
* **3.** **Una segunda fuente, y NO un tercer ancho.** El segundo ancho ya se corrio y devolvio dos rojos y tres objeciones de composicion; un tercero daria mas de lo mismo. Una segunda cara **no**: cuatro de las cinco cosas de §10a son independientes de la fuente. **La que si compraria algo es una captura en ESCALA DE GRISES**, porque L12 dice que en tres kits el unico canal del match es el matiz y esta ronda no puede decidirlo. Es una linea de `raster.py`.

**Y el limite, escrito por quinta vez porque sigue siendo verdad:** once lenguajes de disenio se han
argumentado hasta esta forma mirando imagenes. Esta ronda por fin miro las imagenes correctas, y aun
asi lo que mas moveria el corpus no es una sexta ronda ni una sexta medicion. Es media hora con alguien
que no lo haya visto nunca.

---

## 11. Como reproducir esta ronda

```
python -X utf8 prototypes/components/raster.py          # 66 png + 66 json  (NO corrido; leidos de disco)
python -X utf8 prototypes/components/legibility.py      # out/legibility.txt (NO corrido)
python -X utf8 prototypes/components/second_width.py    # w80/ 264 ficheros  (NO corrido)
python -X utf8 -m pytest -q                             # (NO corrido)
```

Las 18 tiradas en blanco salen de los 132 `*.json` de `png/` y `w80/`: una tirada cuyo texto es todo
espacios, de ocho celdas o mas, cuyo `ground` no es el `ground` del frame. Las 15 de 24 filas
co-dibujadas salen de `str.__contains__` sobre los `.txt` de cada kit. Los productos del asiento
declarado se calculan dibujando la celda con `raster.cell_tile()` con la tinta y el fondo que el
sidecar declara para ese run, midiendo la fraccion de pixeles distintos del fondo y el contraste WCAG
del color medio de esos pixeles contra el fondo; es el metodo de la seccion C de `legibility.txt`
aplicado a un asiento elegido en vez de al peor. Los largos de tirada son `re.finditer` sobre los
`.txt`.

**Pagina del operador:** `ronda-66-raster.html`, con los 66 a 100×32 y a 80×24 uno al lado del otro,
los diez pares dibujados, las diez peores marcas a 1:1 y un voto por frame.

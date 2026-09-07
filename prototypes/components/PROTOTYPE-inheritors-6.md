# PROTOTYPE-inheritors-6, la primera ronda que aprieta una tecla

`PROTOTYPE-inheritors-5.md` (2026-09-07) juzgo los 66 por quinta vez y cerro con una sola frase como
recomendacion: **«una tecla: `App.run_test()` + `Pilot`, cinco rondas sin usar; un frame no puede
fallar en foco porque un frame no tiene foco.»** `SESION-PERSONA.md` §7.3 dice lo mismo desde el otro
lado, en la lista de lo que una sesion humana **no** va a poder ver: *«Ninguna tecla. El foco es
decoracion en los 66 frames y lo sigue siendo aqui.»*

Corrieron `rework-10` inc91 (el instrumento: `prototypes/components/keys.py`, once lenguajes por seis
pasos de guion, 264 artefactos identicos entre dos procesos), inc92 (L12 corregida) e inc93 (los dos
defectos que inc91 grabo).

**Esta ronda no mira una hoja. Mira la aplicacion, despues de una tecla.** Los 66 frames de esta ronda
no son las seis pantallas canonicas dibujadas a mano en `screens.py`: son las pantallas que la app
**tiene**, fotografiadas despues de cada paso de un guion fijo. Y el instrumento hizo lo que se le
pidio: **fallo de una manera que ninguna ronda anterior podia fallar.**

**Resultado: keep 33 · nota 12 · rehacer 21.** Es la proporcion de rehacer mas alta del programa, y no
porque los lenguajes hayan empeorado: **casi todos los rehacer son de la APP y no de los kits**. Tres
de los seis pasos se juzgan sobre superficies que ningun kit dibuja.

Contexto de uso, sin cambios: **operador unico** (`jav201`), terminal monoespaciada, sesion diurna,
tema por defecto. Ancho unico: **100x32**, que es el de la ronda cinco y el de la sesion humana.

---

## 0. Tres cosas que hay que decir antes de la primera tabla

### 0a. El foco de esta aplicacion es UNA regla de CSS y UN token, y el token falla de dos maneras opuestas a la vez

`themes.tcss()` tiene una sola regla para el anillo:

```
.tile:focus  { background: {panel}; border-left: {sel} {accent}; }
#hero:focus  { border: {sel} {accent}; }
```

y once valores de `panel` y de `sel`. **Ningun kit declara una marca de foco.** No hay `Kit.FOCUS`
como hay `Kit.CUR`; el foco no pasa por el contrato en ningun punto.

Medido celda a celda entre `K1` y `K2`, sobre el asiento que toma el foco:

```
kit          glifos que se mueven   fondos que cambian   sel
naught                1                  16 / 16         outer
corgi                 1                  16 / 16         solid
instrument            1                  15 / 15         outer
swiss                 1                  13 / 13         solid
industrial            1                  16 / 16         solid
nord                  1                  16 / 16         round
darkside              1                   8 /  8         solid
prism                 1                  16 / 16         solid
ledger                0                  16 / 16         none
solari                0                  15 / 16         none
blueprint             0                  16 / 16         none
```

**Ocho kits mueven exactamente un glifo** -- la celda del `border-left`, que es `▌` o `│` en el
`accent` del kit -- **y tres no mueven ninguno**. En ledger, solari y blueprint el foco es **color y
nada mas**, y eso contradice la regla que este corpus se escribio a si mismo: *«this contract's states
may never ride colour alone»* (`Kit.textfield`) y la ruling **L2** (`rework-6b`, inc69): *«a disabled
control always carries a mark; air is not a state»*. El foco es un estado.

**Y el mismo token falla al reves en los otros ocho.** El anillo del `#hero` es un BORDE completo, y un
borde cuesta una fila y dos columnas. Medido sobre la region del hero entre `K1` (con el anillo) y
`K2` (sin el):

```
kit          glifos que se mueven en el hero    mismo texto?
naught                  226                        no
corgi                   232                        no
instrument              254                        no
swiss                   342                        no
industrial              304                        no
nord                    269                        no
darkside                154                        no
prism                   312                        no
ledger                    0                        si
solari                    0                        si
blueprint                 0                        si
```

**En ocho de los once, quitar el foco del hero REDIBUJA su contenido**: hasta 342 celdas, y el texto
que queda no es el mismo texto. El hero es un numeral dibujado a la anchura que le den, el borde le
quita dos columnas, y el numeral se recompone. Los tres que no se mueven son los mismos tres que no
tienen anillo, por la misma causa: `sel: none`.

**Un token, dos fallos opuestos.** Donde dibuja, el foco cambia el CONTENIDO del widget que toma;
donde no dibuja, el foco no es nada. Ninguna de las dos cosas es una decision de lenguaje: las dos
salen de una hoja de estilo que ningun kit escribio.

### 0b. El unico modal que la app tiene rompe la ley que el barrido de las hojas impone

`render.py` la enuncia sin margen: *«for each screen, no two languages may render byte-identically.
Two languages agreeing on a whole screen is the exact defect LANGUAGES.md records.»* Las 66 hojas la
cumplen, a los dos anchos, desde que existe el barrido.

Los once `K3` -- el modal de ayuda, la unica banda modal que la app tiene -- son **cuatro textos**:

```
grupo 1   naught, instrument
grupo 2   corgi, swiss, industrial, darkside, prism      <- CINCO
grupo 3   nord
grupo 4   ledger, solari, blueprint
```

Cinco lenguajes dibujan las mismas 32 filas caracter por caracter. Difieren en color y en nada mas.

La causa es estructural y no descuidada: `HelpScreen` compone los `BINDINGS` de la App a traves de
`LG.mark()` y de `hint_row()`, asi que **un kit llega al modal solo donde TRANSFORMA TEXTO**. Un kit
que no transforma texto no tiene ninguna via de entrada a esta pantalla. Los grupos de arriba son
exactamente los grupos de transformacion de texto del corpus.

Lo que lo arreglaria es un modal dibujado a traves del kit como `screens.s4` dibuja el confirm de las
hojas -- paredes, cerrador, forma de peligro -- y eso es una pantalla reescrita, no una regla anadida.

### 0c. Lo que esta ronda MIRA, dicho antes de la primera nota

Los 66 frames de esta ronda son **cuatro paginas** vistas seis veces:

- `K1`, `K2`, `K4` son la misma pagina (el `Aperture`) en tres estados de foco;
- `K3` es el modal;
- `K5` es la pantalla de configuracion;
- `K6` es la paleta de comandos.

`K4` es, por ley, **identico a `K2` celda por celda** en los once. Es el unico frame del programa cuyo
valor esta en ser identico a otro, y ninguna imagen puede ensenar eso: hay que medirlo. Se juzga
igual, y su bloque dice lo que muestra y por que su veredicto no puede ser otro.

---

## 1. La matriz 11x6

| lenguaje | K1 inicial | K2 foco | K3 modal | K4 escape | K5 invalido | K6 match |
|---|---|---|---|---|---|---|
| naught | nota | keep | rehacer | keep | rehacer | keep |
| corgi | nota | keep | rehacer | keep | keep | keep |
| instrument | nota | keep | rehacer | keep | nota | keep |
| swiss | nota | keep | rehacer | keep | keep | keep |
| industrial | nota | keep | rehacer | keep | keep | nota |
| nord | nota | keep | keep | keep | rehacer | keep |
| darkside | nota | keep | rehacer | keep | keep | rehacer |
| prism | nota | keep | rehacer | keep | keep | keep |
| ledger | rehacer | rehacer | rehacer | keep | nota | keep |
| solari | rehacer | rehacer | rehacer | keep | rehacer | rehacer |
| blueprint | rehacer | rehacer | rehacer | keep | nota | keep |

**keep 33 · nota 12 · rehacer 21.**

Por paso: `K1` 0/8/3 · `K2` 8/0/3 · `K3` 1/0/10 · `K4` 11/0/0 · `K5` 5/3/3 · `K6` 8/1/2.

**Las columnas son mas informativas que las filas, y eso es el hallazgo.** `K3` es rehacer en diez de
once por una sola causa, `K1` es nota en ocho por una sola causa, y `K4` es keep en once por una sola
causa. Solo `K5` y `K6` se reparten por lenguaje, y son precisamente los dos pasos que un kit dibuja.

---

## 2. Los 66 bloques

### 2.1 naught

Alfabeto de circulos y una retícula; el rojo racionado a la alarma. Es el kit cuyo alfabeto
`spec.md` §24.3.10 declaro agotado.

#### `naught_K1` — la pagina que se abre, el anillo en el hero → **`nota`**

Lo que muestra: 36,9 % de tinta, el hero en `[2,1,62,9]` con el borde `outer` en `#e51b24` alrededor.
La objecion: el anillo es un borde y el borde le quita dos columnas al hero, asi que al soltarlo
**226 celdas del hero se redibujan** y el texto que queda no es el mismo. El foco cambia el contenido
del widget que toca. El veredicto es nota y no rehacer porque el anillo **se ve**: es lo unico rojo de
la pagina y este kit raciona el rojo.

#### `naught_K2` — el foco tras tres tabuladores → **`keep`**

Lo que muestra: el tile `t-wip` en `[34,15,16,1]`, dieciseis fondos de `#000000` a `#0a0a0a` y una
celda de glifo: `▌` en `#e51b24`. La objecion: un solo cell de marca es poco, y el fondo `#0a0a0a`
sobre `#000000` es el escalon mas fino del corpus. El veredicto es keep porque **son dos canales** --
area y marca -- y porque el rojo del borde es el unico rojo que este kit gasta.

#### `naught_K3` — el modal de ayuda → **`rehacer`**

Lo que muestra: la banda en `[19,4,62,22]`, fondo `#0a0a0a`, 11,5 % de tinta, y la pagina de detras
**no esta**: el modal la tapa entera. La objecion: naught comparte su texto con instrument, caracter
por caracter. Dos lenguajes de acuerdo sobre una pantalla completa es el defecto que `render.py`
prohibe en las hojas. El veredicto: rehacer, y el arreglo es una pantalla, no once.

#### `naught_K4` — la pagina devuelta → **`keep`**

Lo que muestra: `K2` otra vez, celda por celda, y 574 celdas de distancia a `K1` -- que es exactamente
el paseo del foco que el guion hizo. La objecion: ninguna que una imagen pueda sostener. El veredicto
es keep y es el unico veredicto disponible: el modal devuelve la pagina que tapo, que es todo lo que
un modal debe.

#### `naught_K5` — el campo rechazado → **`rehacer`**

Lo que muestra: `◑12/99/26◑` en `#f5f5f5`, en la fila 10. La objecion: `◑` es **un decimo circulo**
en el alfabeto que L10 declaro agotado con nueve. inc90 enumero veinte filas sobre nueve dibujos y
`spec.md` §11.5 escribio el limite: *«naught y solari no tienen celda libre.»* La pared del campo
invalido gasta una mas, y las dos mitades no se espejan (el mismo `◑` a los dos lados). El veredicto:
rehacer, y no por el asiento -- que es correcto -- sino por la celda.

#### `naught_K6` — la paleta con un resultado → **`keep`**

Lo que muestra: la fila del resultado en `#f5f5f5`, diez celdas de tinta y **cinco en negrita**, que
son las cinco de la consulta. La objecion: la tinta del match es la misma tinta de la fila, asi que el
canal es solo el peso. El veredicto es keep porque **eso es exactamente lo que `bold {ink}` declara**:
la paleta ahora dice lo que el kit dice.

### 2.2 corgi

LCD y bloques; el naranja es el unico color y la pantalla es un aparato.

#### `corgi_K1` — la pagina que se abre → **`nota`**

Lo que muestra: 49,4 % de tinta, la mas cargada de los once junto con industrial; el hero ocupa
`[2,1,96,9]`. La objecion: 232 celdas del hero se recomponen al soltar el foco. El veredicto: nota,
por lo mismo que naught.

#### `corgi_K2` — el foco → **`keep`**

Dieciseis fondos de `#0d0d0d` a `#1c1c1c` y un `│` en `#ff6600`. El escalon de fondo es el mas ancho
de los once oscuros, asi que aqui el anillo se lee de lejos. keep.

#### `corgi_K3` — el modal → **`rehacer`**

Es miembro del grupo de CINCO: corgi, swiss, industrial, darkside y prism dibujan las mismas 32 filas
caracter por caracter. La objecion no es de este kit sino de la pantalla, y el veredicto es el mismo
para los cinco. rehacer.

#### `corgi_K4` — la pagina devuelta → **`keep`**

811 celdas de distancia a `K1`, la mayor de los once, porque este kit es el que mas tinta gasta y el
paseo del foco toca mas celdas. Identico a `K2`. keep.

#### `corgi_K5` — el campo rechazado → **`keep`**

`▚▚12/99/26▞▞`. **Las unicas paredes de dos celdas del corpus, y las unicas que se espejan**: `▚`
inclina a un lado y `▞` al otro, asi que el par se lee como una ranura y no como dos marcas iguales.
Es la mejor de las once. keep.

#### `corgi_K6` — la paleta → **`keep`**

`bold {ink}`: diez celdas de tinta, cinco en negrita. keep.

### 2.3 instrument

Braille de seis puntos, capitales dibujadas, retícula de banco de medida.

#### `instrument_K1` — la pagina que se abre → **`nota`**

El hero en `[13,1,74,9]`, indentado trece columnas -- la composicion mas centrada de los once. 254
celdas se recomponen al soltar el foco. nota.

#### `instrument_K2` — el foco → **`keep`**

Quince fondos y un `▌` en `#39d7c3`. El `outer` de este kit dibuja el borde FUERA del widget, asi que
la marca no le come una columna al contenido del tile. keep.

#### `instrument_K3` — el modal → **`rehacer`**

Comparte texto con naught. rehacer, misma causa.

#### `instrument_K4` — la pagina devuelta → **`keep`**

666 celdas de `K1`, identico a `K2`. keep.

#### `instrument_K5` — el campo rechazado → **`nota`**

`⠶12/99/26⠶`. Este es el kit del que `spec.md` §23.3.6 dice que su pared y su papel son **el mismo
glifo**, y que por eso el corte de asiento de inc85 se ve dentro de un solo campo. **Con el campo
lleno no se ve nada de eso**: no hay papel, hay valor, asi que lo que queda es `⠶` dos veces. La
demostracion mas limpia del corpus es invisible en el unico frame vivo que la contiene. nota.

#### `instrument_K6` — la paleta → **`keep`**

`underline {accent}`: cinco celdas en `#39d7c3` con la regla debajo, sobre un cuerpo en `#e8edf2`.
Dos canales, matiz y subrayado, y el subrayado es el que inc92 demostro que este kit siempre tuvo.
keep.

### 2.4 swiss

Sin cajas, sin marcadores, sin tipografia dibujada: aire y una escala. Un solo rojo.

#### `swiss_K1` — la pagina que se abre → **`nota`**

21,4 % de tinta, la segunda mas vacia. La objecion pesa mas aqui que en ningun otro kit: **342 celdas
del hero se recomponen**, la cifra mas alta de los once, en el lenguaje que menos tinta gasta. Un
kit cuya doctrina es el aire no puede permitirse que el foco le mueva el dibujo. nota, y esta a un
paso de rehacer.

#### `swiss_K2` — el foco → **`keep`**

Trece fondos -- el asiento mas estrecho despues de darkside -- y un `│` en `#eb574f`. keep.

#### `swiss_K3` — el modal → **`rehacer`**

Grupo de cinco. rehacer.

#### `swiss_K4` — la pagina devuelta → **`keep`**

688 celdas de `K1`, identico a `K2`. keep.

#### `swiss_K5` — el campo rechazado → **`keep`**

`║12/99/26║`. Una regla doble vertical. Este kit no dibuja cajas por doctrina, asi que **una pared
doble es lo mas alto que puede gastar sin contradecirse**, y no es una caja: son dos reglas. keep.

#### `swiss_K6` — la paleta → **`keep`**

`bold {alert}`: cinco celdas en `#e7372e` con peso, sobre un cuerpo en `#f4f4f4`. El unico rojo del
kit, en el unico sitio de la app donde hay algo que encontrar. keep.

### 2.5 industrial

Naranja de senal, bloques macizos, la pantalla como panel de maquina.

#### `industrial_K1` — la pagina que se abre → **`nota`**

El hero ocupa `[1,0,98,7]` -- **empieza en la fila 0**, el unico de los once que llega al borde de
arriba. 304 celdas se recomponen. nota.

#### `industrial_K2` — el foco → **`keep`**

Dieciseis fondos de `#1a1a1a` a `#232323` y un `│` en `#ff623b`. keep.

#### `industrial_K3` — el modal → **`rehacer`**

Grupo de cinco. rehacer.

#### `industrial_K4` — la pagina devuelta → **`keep`**

696 celdas de `K1`, identico a `K2`. keep.

#### `industrial_K5` — el campo rechazado → **`keep`**

`▐12/99/26▌`. Dos medios bloques mirando hacia dentro: se espejan, y a 9x19 son dos barras solidas de
cuatro pixeles de ancho. Es la pared mas maciza de las once y la segunda mejor. keep.

#### `industrial_K6` — la paleta → **`nota`**

`reverse {accent}`: la paleta pinta **la tinta y no la placa**. `Widget.get_visual_style(...,
partial=True)` construye su estilo con cinco banderas -- bold, dim, italic, underline, strike -- y
`reverse` no esta entre ellas; un fondo opaco en un estilo parcial se resuelve a transparente por la
mezcla de esa misma funcion. Asi que el match sale `#ff623b` sobre el fondo de la fila en vez de ser
una placa naranja. **Se ve** -- es el unico naranja de la fila -- pero no es el canal que el kit
declara. nota, y la causa esta en el framework, no en el kit.

### 2.6 nord

base16: hereda la paleta del entorno y por construccion no tiene identidad propia.

#### `nord_K1` — la pagina que se abre → **`nota`**

269 celdas del hero se recomponen. nota.

#### `nord_K2` — el foco → **`keep`**

Dieciseis fondos de `#2e3440` a `#3b4252` y un `│` en `#8fbcbb`, con `sel: round` -- el unico kit que
redondea. keep.

#### `nord_K3` — el modal → **`keep`**

**Es el unico de los once que no comparte su texto con nadie**, y hay que decir por que: nord es el
kit base y su `LG.mark()` no transforma nada, asi que su modal es el texto crudo y los otros diez son
transformaciones de el. Estar solo aqui no es un merito de diseno: es el efecto de ser el origen. Aun
asi, la ley se cumple en esta fila y el veredicto es keep.

#### `nord_K4` — la pagina devuelta → **`keep`**

523 celdas de `K1`, la segunda distancia mas corta. Identico a `K2`. keep.

#### `nord_K5` — el campo rechazado → **`rehacer`**

`?12/99/26?`. **La pared de este campo es un signo de interrogacion literal, y su papel es un
espacio.** Dos objeciones, y las dos son de lectura y no de medida:

1. `?` no dice *esto esta mal*, dice *no se*. Es la unica marca de rechazo del corpus que hace una
   pregunta.
2. **`?` es la tecla de ayuda de esta misma aplicacion**, impresa en el pie de la pantalla dos filas
   mas abajo (`? Keys`). El mismo caracter es un atajo y un rechazo en la misma pantalla.

rehacer.

#### `nord_K6` — la paleta → **`keep`**

`bold {accent}`: cinco celdas en `#8fbcbb` con peso. inc92 midio que este peso siempre estuvo ahi y
que la clasificacion no lo leia. keep.

### 2.7 darkside

Negro puro, un azul, y la densidad como material.

#### `darkside_K1` — la pagina que se abre → **`nota`**

14,8 % de tinta: **la pagina mas vacia de los once**. El hero ocupa `[2,1,46,9]`, la mitad de ancho
que en los demas. 154 celdas se recomponen al soltar el foco -- la cifra mas baja, y sigue siendo
ciento cincuenta y cuatro. nota.

#### `darkside_K2` — el foco → **`keep`**

**Ocho fondos**, el asiento mas estrecho de los once, y un `│` en `#1783ff`. Un anillo de ocho celdas
en una pagina de 3 200 es la marca de foco mas pequena del corpus, y es la que mas se ve, porque el
fondo `#121212` sobre `#000000` es el unico escalon de esta pagina. keep.

#### `darkside_K3` — el modal → **`rehacer`**

Grupo de cinco. rehacer.

#### `darkside_K4` — la pagina devuelta → **`keep`**

326 celdas de `K1`, la distancia mas corta de los once, porque es la pagina con menos tinta. Identico
a `K2`. keep.

#### `darkside_K5` — el campo rechazado → **`keep`**

`Ø12/99/26Ø`. El cero barrado es la marca internacional de *no*, y a 9x19 es un anillo con una
diagonal que ninguna otra celda del corpus dibuja. Las dos mitades no se espejan -- es el mismo glifo
a los dos lados -- pero la marca es inequivoca. keep.

#### `darkside_K6` — la paleta → **`rehacer`**

`reverse {mut}`: sin la placa, el match sale en `#757575` sobre una fila cuyo cuerpo esta en
`#f5f5f5`. **El match queda MAS APAGADO que el texto en el que esta.** Un realce invertido es peor
que ningun realce: dice *esto importa menos*. La causa es la misma limitacion del framework que en
industrial, pero aqui el resultado no es un canal perdido sino un canal al reves. rehacer.

### 2.8 prism

Braille de ocho puntos y el campo consumido como cantidad.

#### `prism_K1` — la pagina que se abre → **`nota`**

312 celdas del hero se recomponen. nota.

#### `prism_K2` — el foco → **`keep`**

Dieciseis fondos y un `│` en `#2dd4bf`. keep.

#### `prism_K3` — el modal → **`rehacer`**

Grupo de cinco. rehacer.

#### `prism_K4` — la pagina devuelta → **`keep`**

604 celdas de `K1`, identico a `K2`. keep.

#### `prism_K5` — el campo rechazado → **`keep`**

`⣹12/99/26⣏`. Dos celdas braille que **se espejan**: `⣹` carga la izquierda y `⣏` la derecha. Es la
unica pared del corpus que dice *dentro* con la direccion de sus propios puntos. keep.

#### `prism_K6` — la paleta → **`keep`**

`bold {accent}`: cinco celdas en `#2dd4bf` con peso. keep.

### 2.9 ledger

El unico papel claro del corpus. Ordenes de imprenta: `* † ‡ § ‖ ¶`.

#### `ledger_K1` — la pagina que se abre → **`rehacer`**

Lo que muestra: 43,3 % de tinta sobre `#e9e1cf`, el hero en `[2,1,96,7]` -- **y ninguna senal de que
el hero tenga el foco.** `sel: none`, asi que `border: none {accent}` no dibuja nada. La objecion: la
pagina se abre con el anillo puesto y no hay forma de saber donde esta. El veredicto es rehacer y es
el mas facil de la ronda: no hay nada que juzgar porque no hay nada dibujado.

#### `ledger_K2` — el foco tras tres tabuladores → **`rehacer`**

Dieciseis fondos de `#e9e1cf` a `#f2ecdd` y **cero glifos**. El foco de este kit es color y nada mas,
contra su propia regla (`Kit.textfield`: *«this contract's states may never ride colour alone»*) y
contra la ruling L2. Y el escalon es el de un papel sobre otro papel: `#e9e1cf` a `#f2ecdd` es el
salto mas fino que este kit hace en cualquier sitio. rehacer.

#### `ledger_K3` — el modal → **`rehacer`**

Comparte texto con solari y blueprint. Su banda es de veinte filas y no de veintidos -- es uno de los
tres kits cuya linea de pistas ocupa menos -- y su tinta en el modal es 6,3 %, la mitad que en los
otros ocho. rehacer.

#### `ledger_K4` — la pagina devuelta → **`keep`**

660 celdas de `K1`, identico a `K2`. keep.

#### `ledger_K5` — el campo rechazado → **`nota`**

`‡12/99/26‡`. La daga doble, del orden de imprenta propio del kit. La objecion es de **serie**: inc89
movio `§` -- la marca siguiente del mismo orden -- al peldano de aviso de la escalera de severidad. Asi
que `‡` es un RECHAZO y `§` es un AVISO, y las dos salen del mismo alfabeto de seis marcas en un orden
que un lector no tiene por que conocer. Nada las distingue salvo saberse la serie. nota.

#### `ledger_K6` — la paleta → **`keep`**

`underline {ink}`: diez celdas de tinta y **cinco subrayadas**, sobre el unico papel claro del corpus.
Este es el frame donde el arreglo de inc93 mas se nota: antes de el, la paleta ponia una losa
`#141f27` de modo nocturno atravesada sobre esta pagina de color crema. keep.

### 2.10 solari

Tablilla de aeropuerto: placas, ambar, la fila como objeto.

#### `solari_K1` — la pagina que se abre → **`rehacer`**

`sel: none`: el hero tiene el foco y no lo dice. rehacer, misma causa que ledger.

#### `solari_K2` — el foco → **`rehacer`**

**Quince fondos de dieciseis y cero glifos** -- la unica fila de la tabla que no cambia el fondo
entero, porque una de las celdas del asiento ya estaba en `#17171a`. El foco de este kit es un color
sobre un color parecido, y su `focus` es `#f5a300`, que es su propio `accent`: el kit tiene el ambar
mas fuerte del corpus y no lo gasta en el anillo. rehacer.

#### `solari_K3` — el modal → **`rehacer`**

Comparte texto con ledger y blueprint. rehacer.

#### `solari_K4` — la pagina devuelta → **`keep`**

721 celdas de `K1`, identico a `K2`. keep.

#### `solari_K5` — el campo rechazado → **`rehacer`**

`═12/99/26═`. **Una regla doble HORIZONTAL usada como pared VERTICAL.** A 9x19 el glifo son dos trazos
horizontales cortos: el campo no queda encerrado, queda con un guion doble a cada lado y el valor
flotando entre ellos. Es la unica pared del corpus que apunta al eje contrario. rehacer.

#### `solari_K6` — la paleta → **`rehacer`**

`reverse {ink}`, y es el peor resultado de los seis pasos. Sin la placa, la tinta del match es
`#f0ede4`, que es **exactamente la tinta de la fila en la que esta**: la fila del resultado sale como
una sola tirada de un solo color y el match **no se distingue en absoluto**. Medido: quince celdas en
la tinta del match y cero celdas de cuerpo en otra tinta. Este kit pone toda su distincion en la
placa, y la placa es lo unico que el framework no puede gastar. rehacer.

### 2.11 blueprint

Cianotipo: papel azul, tinta blanca, el plano tecnico.

#### `blueprint_K1` — la pagina que se abre → **`rehacer`**

`sel: none`: el anillo no existe. rehacer.

#### `blueprint_K2` — el foco → **`rehacer`**

Dieciseis fondos de `#123a5c` a `#0e2f4a` -- **y este es el unico kit de los once cuyo foco OSCURECE
el asiento en vez de aclararlo**, porque su `panel` es mas oscuro que su ground. Cero glifos. Color
solo, y ademas al reves que en los otros diez. rehacer.

#### `blueprint_K3` — el modal → **`rehacer`**

Comparte texto con ledger y solari. Y una nota que no es del modal sino del kit: es el unico de los
once cuyo `K3` gasta **cuatro tintas** y no cinco. rehacer.

#### `blueprint_K4` — la pagina devuelta → **`keep`**

721 celdas de `K1`, identico a `K2`. keep.

#### `blueprint_K5` — el campo rechazado → **`nota`**

`╲12/99/26╲`. Las dos paredes **inclinan hacia el mismo lado**, asi que el par no se lee como un
corchete sino como dos barras en cursiva alrededor del valor. Compara con corgi (`▚▚` / `▞▞`),
industrial (`▐` / `▌`) y prism (`⣹` / `⣏`), que se espejan. nota.

#### `blueprint_K6` — la paleta → **`keep`**

`bold {ink}`: diez celdas de tinta, cinco en negrita, sobre el papel azul. keep.

---

## 3. Totales

| | keep | keep with a note | rework | total |
|---|---|---|---|---|
| ronda seis, contra las teclas | **33** | **12** | **21** | 66 |

Por paso:

| paso | keep | nota | rehacer | la causa dominante |
|---|---|---|---|---|
| `K1` inicial | 0 | 8 | 3 | el anillo del hero es un borde: recompone el contenido, o no existe |
| `K2` foco | 8 | 0 | 3 | tres kits tienen `sel: none` y el foco es color solo |
| `K3` modal | 1 | 0 | 10 | cuatro textos para once lenguajes; el grupo mayor tiene cinco |
| `K4` escape | 11 | 0 | 0 | la restauracion es exacta en los once |
| `K5` invalido | 5 | 3 | 3 | reparto por kit: la celda de la pared |
| `K6` match | 8 | 1 | 2 | reparto por kit: los tres de `reverse` |

**Solo `K5` y `K6` se reparten por lenguaje.** Los otros cuatro pasos tienen un veredicto por causa y
no por kit, y las cuatro causas viven en `themes.tcss()`, en `HelpScreen` y en Textual. Esta ronda
juzga once lenguajes y encuentra que **cuatro de sus seis columnas no son sobre los lenguajes**.

---

## 4. Las objeciones en pie, por quien las arregla

### 4a. El programa de lenguajes (once kits, un contrato)

- **El foco no pasa por el contrato en ningun punto.** No hay `Kit.FOCUS` como hay `Kit.CUR`. Mientras
  no lo haya, el anillo es una regla de CSS y un token `sel`, y tres kits pueden declarar `none` sin
  que nada lo note. `FOCUS_RIDES_COLOUR_ALONE` es el registro con dientes; lo que falta es la
  decision de si el foco es un asiento del contrato.
- **`naught ◑` es un decimo circulo** en un alfabeto que `spec.md` §24.3.10 declaro agotado con nueve.
  L10 sigue abierta y esta pared la ensancha.
- **`nord ?`** es la unica marca de rechazo del corpus que hace una pregunta, y es la tecla de ayuda
  de la misma aplicacion impresa dos filas mas abajo.
- **`solari ═`** apunta al eje contrario: una regla horizontal usada como pared vertical.
- **`ledger ‡` contra `§`**: rechazo y aviso, dos marcas del mismo orden de imprenta, distinguibles
  solo por saberse la serie.
- **`blueprint ╲ ╲`** no se espeja.

### 4b. La aplicacion (`prototypes/widget_slice/app.py`, `themes.tcss`)

- **El anillo del `#hero` es un borde y recompone el contenido**: hasta 342 celdas, en ocho de once.
  Un anillo debe rodear, no reescribir.
- **`HelpScreen` no pasa por el kit.** Cuatro textos para once lenguajes, con un grupo de cinco. El
  arreglo es la pantalla dibujada como `screens.s4` dibuja el confirm.
- **Ningun kit dibuja el modal, la configuracion ni la paleta.** Tres de las cuatro paginas que esta
  ronda mira son chrome del framework o de la app.

### 4c. El framework (Textual 8.2.8)

- **`reverse` no llega a la paleta.** `Widget.get_visual_style(..., partial=True)` construye su
  `VisualStyle` con cinco banderas y `reverse` no esta; un fondo opaco en un estilo parcial se
  resuelve a transparente. Tres kits pierden el canal que declaran, y en solari eso cuesta la
  distincion entera. `PALETTE_CANNOT_REVERSE` es el registro con dientes.
- **El glifo del prompt de la paleta es `U+1F50E`**, dos columnas de ancho, ausente de la cara medida,
  y **la unica celda de los 66 frames que no eligio ni un kit ni una pantalla**. Darle un lenguaje es
  un asiento nuevo del contrato (`Kit.SEARCH`) en los once.
- **Las celdas en blanco de la paleta llevan `#00ff00`**, el color por defecto del `Input` de Textual,
  en los once. No pinta nada solo porque esas celdas son espacios.

### 4d. El instrumento (`keys.py`)

- **`settle_reads` no es reproducible** y es el unico campo de los 264 artefactos que no lo es. Esta
  enmascarado por `UNPINNED` en la comprobacion entre procesos y **no** esta quitado del registro, asi
  que unas pocas `.json` cambian en disco en cada corrida sin que ninguna imagen cambie.
- **El guion es uno.** Seis pasos, un orden, un ancho.

---

## 5. Lo que esta ronda NO puede ver

Se dice aqui, como en las cinco anteriores, antes de que nadie tenga que descubrirlo.

1. **Ningun humano.** Sigue siendo `n = 0`. Esta ronda mide que el asiento con el foco se dibuja
   distinto; **no puede decir que alguien lo note**. Ocho de los once mueven un solo glifo, y si un
   glifo basta es exactamente la pregunta que `SESION-PERSONA.md` existe para hacer.
2. **Un solo guion.** Seis pasos en un orden. No hay `shift+tab`, no hay una segunda pulsacion de la
   misma tecla, no hay dos teclas a la vez, no hay una tecla mantenida. El anillo viaja hacia adelante
   y nunca hacia atras.
3. **Un solo ancho.** 100x32. Las cuatro barras de teclas que se caen a 24 filas (C12) siguen sin ojo
   humano y ahora tambien sin tecla.
4. **Ninguna latencia.** `settle` espera a que la pantalla se quede quieta y fotografia el reposo. Lo
   que pasa **entre** la tecla y el reposo -- que es donde vive la sensacion de una interfaz -- no esta
   en ningun frame de esta ronda.
5. **El foco solo llega a tres asientos.** Tres tabuladores desde el hero llegan a un `Tile`. Las
   `TaskCard` del tablero, que son los widgets que mas foco reciben en uso real, no las toca este
   guion.
6. **El modal es el de ayuda y no hay confirmacion.** La app **no vincula ningun borrado**, asi que la
   banda que esta ronda juzga es un keymap y no un confirm. Lo que las hojas dibujan en `S4` -- la
   pregunta irreversible, la forma de peligro, el brazo de confirmacion -- no tiene ninguna tecla que
   lo abra.
7. **El campo vivo es uno y es un numero.** El brief pedia un campo de FECHA; la app no tiene ninguno
   y el unico valor que el motor ya tenia es un umbral. Las once paredes de invalido se juzgan aqui
   alrededor de `12/99/26`, que es lo que se tecleo, y **no alrededor de una fecha**.
8. **Solo dos de las seis senales tienen umbral.** El guion tuvo que aprender a bajar dos filas para
   encontrar el asiento. Un campo que existe en un tercio de las filas es un campo que la mayoria de
   las filas no tiene.
9. **La paleta se dibuja sobre la pantalla de configuracion**, porque el guion es una secuencia y el
   paso 6 se aprieta donde el paso 5 dejo al usuario. Es igual en los once, que es lo que la
   comparacion necesita, pero no es la pagina sobre la que un usuario la abriria.
10. **Los 66 frames de las hojas siguen donde estaban.** Esta ronda no los vuelve a juzgar y no los
    contradice: son dos corpus distintos y `PROTOTYPE-inheritors-5.md` sigue siendo el juicio vigente
    sobre el suyo.

---

## 6. Como reproducir esta ronda

```
python -X utf8 prototypes/components/keys.py
python -X utf8 -m pytest tests/test_components.py -q -k "key or invalid_state or palette or focus_ring or one_modal"
```

`keys.py` escribe los 66 `.txt`, `.svg`, `.png` y `.json` en `prototypes/components/keys/`, imprime la
tabla de veredictos de los seis pasos y de los once lenguajes, imprime la tabla de canales de la que
salen §0a y §0b, y vuelve a correr el guion entero **en un proceso nuevo** para comprobar que los 264
artefactos son identicos byte a byte.

Los numeros de este documento salen de esas `.json` y de nada mas: las regiones de foco, la banda del
modal, las tintas y las banderas de peso y subrayado los escribe el sidecar, y las leyes de
`tests/test_components.py` los vuelven a medir sin importar el instrumento.

# SESION-PERSONA, el protocolo de la primera sesion con alguien que no ha visto los kits

Once lenguajes de diseno, seis pantallas cada uno, cinco rondas de lectura adversarial, cuarenta y
tres *rulings*, mil cuatrocientos sesenta y seis tests, y **cero personas ajenas al programa**. Este
documento es el guion de la primera. Dura 45 minutos, la corre el operador en esta maquina, y el
participante no necesita saber nada del programa.

El cierre de la ronda cuatro lo dejo escrito y la ronda cinco lo repitio: *"lo que mas moveria el
corpus no es una quinta ronda ni un raster. Es una sesion con una persona que no haya visto el kit, a
la que se le pida senalar la celda que significa «esto destruye datos»"*. La ronda cinco lo pone en
su §10d como la primera de tres cosas que faltan, y anade la razon: *"hay veintitantas frases de la
forma «senalar la celda que significa que esto destruye datos» repartidas por cinco documentos, y
ninguna se ha ejecutado nunca sobre un ser humano"*.

**Artefacto de la sesion:** `C:\Users\jjgh8\.claude\jobs\85046efb\tmp\gal\sesion-persona.html`, la
pagina imprimible con los 24 frames a 1:1, la hoja de registro y la clave de respuestas plegada.

---

## 1. Proposito, y lo que esta sesion NO es

**Proposito.** Ejecutar, una vez y sobre un ser humano, los seis criterios observables que el corpus
lleva cinco rondas escribiendo y ninguna ejecutando.

| criterio | la pregunta, tal como la hace el corpus |
|---|---|
| **S1** lista | que tarea esta en `DOING` |
| **S2** formulario | que campo es obligatorio |
| **S3** ajustes | que pestana esta activa |
| **S4** modal | que celda significa que esto destruye datos |
| **S5** monitor | que fila esta en error |
| **S6** paleta | donde aterrizo la consulta |

**Lo que NO es, y se dice al principio para que no haya que desdecirlo al final:**

1. **No es lo que el programa ya tiene.** Lo que hay hasta hoy es **inspeccion con criterios
   declarados**: un recorrido cognitivo hecho por quien escribe el corpus. La ISO 9241-210 pide
   evaluacion con usuarios y eso es otra cosa. Las cinco rondas lo declaran cada una en su seccion
   *"lo que esta ronda no puede ver"*, y la quinta lo agrava: la tabla §7 *"¿se encuentra a ojo a
   16 px?"* la decidio quien redacta, sobre imagenes ampliadas, sin experimento.
2. **Esta es la primera.** No hay linea base, no hay sesion anterior con la que comparar, y por lo
   tanto no hay ninguna afirmacion de la forma *"empeoro"* o *"mejoro"* que esta sesion pueda
   sostener.
3. **n = 1 no generaliza, y esta hoja no va a pretender que si.** Lo que compra n = 1 es
   **refutacion**, no confirmacion: si la unica persona de fuera que ha mirado el corpus no encuentra
   una marca que un documento declara encontrable, esa declaracion deja de estar en pie sin mas
   evidencia. Al reves no funciona: que la encuentre no prueba que se encuentre.
4. **No es un test de usabilidad del producto.** No hay aplicacion, no hay tecla, no hay foco, no hay
   latencia. Son fotografias fijas. El foco sigue siendo decoracion en los 66 frames y esta sesion no
   lo toca; eso lo compra `App.run_test()` + `Pilot`, que es otro trabajo.
5. **No mide preferencia.** No se pregunta cual gusta mas. Ninguna pregunta de esta hoja se responde
   con una opinion.
6. **Un solo ancho y una sola altura.** Los 24 frames son 100x32. Los dos rojos de solari a 80x24
   quedan fuera y siguen sin ojo humano.

---

## 2. Preparacion (10 minutos antes)

**La celda del corpus mide 9x19 px**, Cascadia Mono 16 px, fallback Segoe UI Symbol para `⊖⊚⊛⋅`. Los
PNG son de 900x608 px = 100 x 32 celdas. Todo lo de abajo existe para que el participante vea
exactamente esos pixeles y no una version escalada de ellos.

**Tres caminos equivalentes para ensenar cada frame a tamano real:**

1. **`sesion-persona.html` en el navegador al 100 % de zoom** (recomendado). Las 24 imagenes llevan
   `width` y `height` iguales a su tamano en pixeles y no hay ni una regla de CSS que las escale. En
   Chrome y Edge, `Ctrl` + `0` deja el zoom en 100 %. **Comprueba el zoom delante del participante**,
   no antes: una pestana heredada al 110 % invalida la sesion entera y no avisa.
2. **Los PNG de `prototypes/components/png/` en el visor de imagenes de Windows con el zoom en 1:1**,
   no en "ajustar a la ventana", que es el modo por defecto y escala.
3. **Windows Terminal con Cascadia Mono a 16 px**, que da la misma caja de 9x19 px de la que estan
   hechos los PNG. Es el unico camino que ensena el original en vez de una foto del original, y es el
   mas caro de montar porque hay que renderizar los frames.

Los tres ensenan los mismos pixeles. El (1) es el recomendado porque lleva la pregunta al lado.

**Lo demas:**

- **Prohibido el zoom durante la sesion**: del navegador, del visor y de la lupa de Windows. Si el
  participante acerca la cara a la pantalla, eso no se impide, **se anota**.
- **Luz.** Una sola condicion de luz para toda la sesion, y se anota en la cabecera de la hoja:
  *sala iluminada* o *sala en penumbra*. **Diez de los once kits son de fondo oscuro** (medido en los
  sidecars de `png/`: el unico claro es ledger, `#e9e1cf`), asi que la luz de la sala no es una
  variable neutra: una sala iluminada castiga a diez de los once y favorece al unico claro. No la
  cambies a media sesion. Con un solo participante no se puede contrabalancear, y por eso la
  condicion es un dato de la sesion y no un detalle.
- **Pantalla.** Anota modelo y resolucion. Escalado de Windows al 100 %, no al 125 %.
- **Lentes.** Si el participante los usa, que los use. Se anota que los usa.
- **20 segundos por frame, maximo.** Cronometra. Pasado el limite se retira la imagen y se anota `D`.
  Una marca que necesita mas de 20 segundos ya fallo el criterio, que dice *senalar*, no *deducir*.
- **Material:** la hoja de registro impresa, un cronometro, y la clave de respuestas **cerrada**.

---

## 3. Muestreo

**24 imagenes: 22 pantallas completas y 2 celdas aisladas.** Cubren **los once kits** y **los seis
criterios**, y estan escogidas para tocar las *rulings* que cinco rondas de lectura no pudieron
cerrar.

| frame | fichero | criterio | kit | ruling que pone a prueba |
|---|---|---|---|---|
| `F01` | `darkside_S1.png` | S1 | darkside | `E`, `L7` |
| `F02` | `ledger_S1.png` | S1 | ledger | `Q2` |
| `F03` | `swiss_S2.png` | S2 | swiss | **`swiss •` / `SEEN_BY_EYE`**, `Q1 (COV)` |
| `F04` | `instrument_S2.png` | S2 | instrument | `Q1`, `L13` |
| `F05` | `prism_S2.png` | S2 | prism | `Q1`, `L13` |
| `F06` | `naught_S2.png` | S2 | naught | `L10`, `D, amended (K2)` |
| `F07` | `swiss_S3.png` | S3 | swiss | **calibracion**, `Q3` |
| `F08` | `corgi_S3.png` | S3 | corgi | **calibracion**, `Q3` |
| `F09` | `naught_S4.png` | S4 | naught | `Q2`, `L10` |
| `F10` | `solari_S4.png` | S4 | solari | `K8 / E6`, `C3'''`, `F at 24 rows` |
| `F11` | `blueprint_S4.png` | S4 | blueprint | `K10` |
| `F12` | `ledger_S4.png` | S4 | ledger | `C2` (brazo de confirmacion) |
| `F13` | `darkside_S5.png` | S5 | darkside | `L7`, `Q1`, `K7 (dim)` |
| `F14` | `industrial_S5.png` | S5 | industrial | `L7`, `Q1` |
| `F15` | `nord_S6.grey.png` | S6 | nord, **gris** | `L12`, `match tier by channel` |
| `F16` | `swiss_S6.grey.png` | S6 | swiss, **gris** | `L12`, `match tier by channel` |
| `F17` | `prism_S6.grey.png` | S6 | prism, **gris** | `L12`, `match tier by channel` |
| `F18` | `instrument_S6.grey.png` | S6 | instrument, **gris** | `L12`, `match tier by channel` |
| `F19` | `prism_S6.png` | S6 | prism, color | `L12`, `match tier by channel` |
| `F20` | `instrument_S6.png` | S6 | instrument, color | `L12`, `match tier by channel` |
| `F21` | `nord_S6.png` | S6 | nord, color | `L12`, `match tier by channel` |
| `F22` | `swiss_S6.png` | S6 | swiss, color | `L12`, `match tier by channel` |
| `F23` | recorte 1:1 de `naught_S2.png` | pares | naught | `D, amended (K2)`, `L10` |
| `F24` | recorte 1:1 de `naught_S2.png` | pares | naught | `D, amended (K2)`, `Q1 (COV)` |

**Por que estos y no otros, punto por punto del encargo:**

- **Un frame por kit y por criterio, sobre el conjunto `keep with a note` por legibilidad.** Los 46
  `keep with a note` de la ronda cinco no caben en 45 minutos. La cobertura que si cabe y que si es
  decidible es: **los once kits presentes** y **los seis criterios presentes**, tomando de cada kit
  el frame cuya nota es de legibilidad y no de gramatica. S1 y S3 quedan a dos frames cada uno;
  S2 y S4 a cuatro; S6 a ocho porque es donde vive la ruling mas nueva. **Esta es la asimetria
  deliberada del muestreo y se declara en §6.**
- **El frame del `•` de swiss (`F03`).** Es el unico renglon de `SEEN_BY_EYE`, la primera exencion
  del programa concedida por **una lectura** y no por una medicion: cobertura 14,0 % contra un piso
  de 15 %, con contraste efectivo 9,13 y declarado 17,30:1, es decir con la mitad de contraste de Q1
  fuera de discusion. Su propio campo `review` dice, literalmente, *"la sesion humana. La revision
  del operador es lo unico que puede revocar esta fila"*. **Este frame no pone a prueba la ruling: es
  la ruling.**
- **`darkside_S1` (`F01`), el escalon gris.** La ronda cuatro objeto *"senalar el escalon gris que
  separa los paneles. Esta a 1,39:1"*; la ronda cinco lo refuto con el raster y con un argumento de
  lectura: *"es una columna gris maciza de dos celdas de ancho y treinta de alto, imposible de no
  ver. La ruling E se sostiene y su unico argumento tambien"*. Medido en el sidecar
  `png/darkside_S1.json`, el escalon son **tres columnas (c60 a c62) por 27 filas**, `#1f1f1f` sobre
  `#000000`. **La refutacion de ruling E descansa hoy sobre un ojo, y es el mismo ojo que la
  escribio.**
- **Los cuatro S6 de matiz, en color Y en gris (`F15` a `F22`).** `MATCH_IN_GREY` mide instrument
  2,34:1, swiss 1,52:1, nord 1,34:1 y prism 1,59:1. L12 dice que un *match* de matiz por debajo de
  3:1 en gris es un **limite del lenguaje**, *recorded and not fixed*. Un limite es una decision
  sobre una persona que no se ha consultado. El par gris/color del **mismo kit** es la unica forma de
  separar *"el match no se ve"* de *"esta persona no entendio la pregunta"*.

  > **Aviso medido al preparar esta hoja, y va contra la premisa de L12.** El *match* de estos cuatro
  > kits **no viaja solo en el matiz**. En el sidecar del raster, el run del match lleva `bold=True`
  > en nord, swiss y prism, y `underline=True` en instrument. Medido sobre el PNG **en gris**, el run
  > del match tiene **1,36x** (nord), **1,42x** (prism) y **1,86x** (instrument) la tinta de su
  > vecino inmediato; en swiss va al reves (0,83x) porque su rojo cae **mas oscuro** que el cuerpo
  > gris, que tambien es un canal acromatico. `match_branch()` clasifica por la relacion entre
  > tokens de color y **no lee `bold` ni `underline`**, asi que la frase *"el unico canal es el
  > matiz"* describe la clasificacion y no el pixel. **Esto no invalida `F15` a `F22`: los mejora.**
  > Lo que miden no es *"¿basta el matiz?"* sino *"¿basta el peso, o el subrayado, sin el matiz?"*,
  > y esa es la pregunta que el corpus deberia estar haciendo. **Se reporta y no se arregla aqui**:
  > tocar `MATCH_IN_GREY`, `match_branch()` o los docstrings de los cuatro kits es un incremento y
  > este documento no es uno.
- **La banda de `naught_S4` (`F09`).** `∙` es el `DANGER_FORM` de naught y mide **una celda**; las dos
  reglas que dominan la pantalla (filas 12 y 19) son **cien celdas de `◦`** cada una, la misma familia
  de circulo. Q2 dice que una tirada de 1 a 4 es significado y una de 8 o mas es estructura. **Esa
  particion es aritmetica; la pregunta es si el ojo la hace.**
- **Dos pares de homoglifo a menos del 3 %, como celdas aisladas (`F23`, `F24`).** `⊚` contra `⊛`
  (1,30 %), que son *"prioridad alta elegida"* contra *"campo obligatorio"*, y **se dibujan en la
  misma pantalla**; y `⋅` contra una celda vacia (1,22 %). Se recortan a 1:1 del propio
  `naught_S2.png`, ocho repeticiones de cada uno, que es como la ronda cinco los miro.
  **Los dos pares son del mismo kit, del mismo fondo y de la misma fila cuando se puede**, para que
  la comparacion sea de dibujo y no de tema.
  **El par de 0,00 % (`• ∙`) NO esta**, y se dice: `•` es de swiss (fondo claro) y `∙` es de naught
  (fondo negro); no hay pantalla que los dibuje juntos, asi que ensenarlos lado a lado no mediria una
  confusion sino un contraste de fondos. §6 de la ronda cinco ya dice lo mismo con otras palabras.
- **Dos frames de calibracion (`F07`, `F08`).** Son `keep` de la ronda cinco, es decir frames que el
  corpus declara que responden. **Si el participante falla uno de los dos, la sesion se anula**: un
  criterio que falla donde el corpus dice que no puede fallar esta midiendo el instrumento, no el
  diseno. Sin este par, cualquier fallo de esta sesion seria inatribuible.
- **Un brazo de confirmacion (`F12`).** `ledger_S4` subio a `keep` en la ronda cinco despues de que
  inc72 cerrara C2. Una sesion que solo mira lo que se sospecha roto no puede decir si sus fallos son
  del corpus o de la sesion.

### Orden, y como se aleatoriza

Barajado **determinista por participante**, con dos restricciones que no son de gusto sino de
contaminacion:

1. **Los cuatro frames en gris (`F15` a `F18`) van antes que su gemelo en color**, y con al menos
   seis frames de por medio. Ver el color primero ensena la respuesta y el gris deja de medir nada.
2. **Las dos celdas aisladas (`F23`, `F24`) van al final.** Ensenar una marca suelta le pone nombre y
   contamina las pantallas que la contienen: `⊛` y `⊚` estan los dos en `F06`.

Receta para el participante `N`:

```python
import random
rest = ["F%02d" % i for i in list(range(1, 15)) + list(range(19, 23))]
for seed in (N, N + 100, N + 200):
    random.seed(seed); random.shuffle(rest)
    order = list(rest)
    for pos, f in zip((1, 3, 5, 7), ("F15", "F16", "F17", "F18")):
        order.insert(pos, f)
    ok = all(abs(order.index(g) - order.index(c)) >= 6 for g, c in
             (("F15", "F21"), ("F16", "F22"), ("F17", "F19"), ("F18", "F20")))
    if ok:
        print(seed, order + ["F23", "F24"]); break
```

**Anota la semilla que usaste** en la cabecera de la hoja. Sin la semilla el orden no es reproducible
y una segunda sesion no se puede comparar con esta.

---

## 4. Tareas y registro

Una pregunta por frame; dos o tres en los que lo dicen. El participante **senala con el dedo sobre la
pantalla** y el operador anota fila y columna. Las coordenadas de la clave son **base 0**, como en los
`.txt`.

### Criterios de anotacion

| marca | cuando |
|---|---|
| **H** acierto | senala la celda correcta (o una contigua de la misma marca) **en menos de 5 s** y sin preguntar |
| **D** duda | llega a la celda correcta pero **tarda mas de 5 s**, o se corrige, o pregunta antes de decidir |
| **F** fallo | senala otra celda, dice que no la encuentra, o se agotan los 20 s |

**La duda no es un acierto.** El criterio del corpus dice *senalar*, no *deducir*, y una marca que se
deduce a los doce segundos ya perdio la propiedad que la nota de la ronda cinco le atribuye.

### Las preguntas, por criterio

| criterio | pregunta literal |
|---|---|
| S1 | "Esto es un tablero de tareas con varias listas. Senala la primera tarea de la lista DOING." |
| S2 | "Esto es un formulario. Senala los campos que son obligatorios." **y luego** "Senala otra vez la marca que usaste para decidirlo. ¿Que significa?" |
| S3 | "¿En que pestana estas ahora mismo? Senalala." **y luego** "Senala lo que en esta pantalla sea irreversible." |
| S4 | "Esta pantalla te esta preguntando algo. Senala la celda o celdas que significan que esto destruye datos." |
| S5 | "Esto es un registro de eventos. Senala la fila que es un error." **y luego** "¿Cuantos niveles distintos de gravedad ves en esa lista?" |
| S6 | "Arriba se escribio algo en una barra de busqueda. Senala, dentro de los resultados, en que parte cayo lo que se escribio." |
| pares | "Aqui hay dos marcas, la de la izquierda y la de la derecha. ¿Son la misma marca o marcas distintas?" **y luego** "¿Que crees que significa cada una?" |

**"¿Que significa esta marca?" se hace en seis frames y solo en seis:** los cuatro de obligatorio
(`F03`, `F04`, `F05`, `F06`) y los dos pares (`F23`, `F24`). Y se hace **despues** de que el
participante haya senalado, sobre la marca que **el** senalo. Preguntar por una marca que el operador
elige es ensenarsela.

`F06` lleva una tercera: *"sin leer las etiquetas de la izquierda: de estas dos filas de circulitos,
¿cual es una eleccion unica y cual son casillas independientes?"*. Es L10, literal, con tres rondas
de antiguedad.

### Hoja de registro

Cabecera: participante ____ · semilla ____ · fecha ____ · luz (iluminada / penumbra) ____ ·
pantalla ____ · lentes si/no ____ · operador ____

| # | frame | pregunta (criterio) | celda esperada | celda senalada | seg | H/F/D | notas |
|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |
| 11 |  |  |  |  |  |  |  |
| 12 |  |  |  |  |  |  |  |
| 13 |  |  |  |  |  |  |  |
| 14 |  |  |  |  |  |  |  |
| 15 |  |  |  |  |  |  |  |
| 16 |  |  |  |  |  |  |  |
| 17 |  |  |  |  |  |  |  |
| 18 |  |  |  |  |  |  |  |
| 19 |  |  |  |  |  |  |  |
| 20 |  |  |  |  |  |  |  |
| 21 |  |  |  |  |  |  |  |
| 22 |  |  |  |  |  |  |  |
| 23 |  |  |  |  |  |  |  |
| 24 |  |  |  |  |  |  |  |

Al pie: **respuesta a la pregunta abierta de cierre**, literal, sin interpretar.

### Clave de respuestas

**Derivada del `.txt` enviado y verificada contra el al construir la pagina**: si un `.txt` cambia, la
construccion falla en vez de mentir. Fila y columna base 0.

| frame | celda(s) correcta(s) |
|---|---|
| `F01` | `f10 c7-24` = `fix login redirect`; cabecera `f9 c5-11` = `doing 4`. Escalon: **c60-62, 27 filas**, `#1f1f1f` sobre `#000000` = 1,39:1 |
| `F02` | `f12 c9-26` = `Fix login redirect`; cabecera `f10 c3-9` = `2 DOING` |
| `F03` | `f4 c7` = `•` y `f6 c5` = `•` |
| `F04` | `f3 c7` = `⣉` y `f5 c5` = `⣉` |
| `F05` | `f3 c7` = `⣆` y `f5 c5` = `⣆` |
| `F06` | `f3 c7` = `⊛` y `f5 c5` = `⊛`. Eleccion unica: fila 8, `f8 c31` = `⊚`. Casillas: fila 10, `f10 c23` = `◉` |
| `F07` | `f0 c15-19` = `C F G`. Irreversible: `f20 c4-15` = `╲Delete all╱` |
| `F08` | `f0 c17-24` = `[3]C F G`. Irreversible: `f19 c4-15` = `█Delete all█` |
| `F09` | `f18 c3` = `∙` y `f18 c10` = `∙`. Senuelos: filas 12 y 19, cien celdas de `◦` cada una |
| `F10` | `f14 c3-10` = `▀Delete▄`. Abridor de la banda `f14 c0` = `▔`; cierre `f15 c0` = `▁` |
| `F11` | `f16 c27-38` = `╞ ━DELETE━ ╡`. Esquinas: `f10 c27` = `┼` y `f17 c27` = `┼` |
| `F12` | `f30 c3-10` = `(Delete)`. Extremos: `f30 c0` = `▶` y `f30 c13` = `◀` |
| `F13` | `f12 c11` = `O`. Aviso `f10 c11` = `o`. Calmo `f8 c11` = `·` (la ronda cinco dice que **no esta**) |
| `F14` | `f12 c11-12` = `■■`. Aviso `f10 c11-12` = `▪▪`. Calmo `f8 c11-12` = `▫▫` |
| `F15`, `F21` | nord: `f5 c4-5` = `re`, y las otras cinco coincidencias, filas 5 a 10 |
| `F16`, `F22` | swiss: `f6 c4-5` = `re`, y las otras cinco coincidencias, filas 6 a 11 |
| `F17`, `F19` | prism: `f5 c4-5` = `re`, y las otras cinco coincidencias, filas 5 a 10 |
| `F18`, `F20` | instrument: `f5 c4-5` = `re`, y las otras cinco coincidencias, filas 5 a 10 |
| `F23` | **distintas.** Izquierda `⊚` (`naught_S2 f8 c31`), derecha `⊛` (`naught_S2 f3 c7`); 1,30 % |
| `F24` | **distintas.** Izquierda `⋅` (`naught_S2 f14 c17`), derecha celda vacia (`naught_S2 f14 c60`); 1,22 % |

---

## 5. Analisis

### El umbral, propuesto ANTES de correr la sesion

Se escribe aqui para que no se pueda mover despues de ver el resultado. Es la mitad del valor del
documento.

| participantes | que revoca |
|---|---|
| **1 (esta sesion)** | **un fallo NO revoca ninguna ruling.** La marca como **discutida** y entra en la lista de la siguiente sesion |
| **1, excepcion unica** | **`SEEN_BY_EYE` si se revoca con un fallo**, porque su propio campo `review` dice que la revision del operador es lo unico que puede hacerlo. La asimetria esta escrita en la ley, no aqui |
| **2** | **dos fallos del mismo frame revocan.** Un fallo de dos no revoca: se anota como discutida |
| **calibracion** | **si `F07` o `F08` fallan, la sesion entera se anula** y no se lee ningun otro resultado |

### Que revoca cada fallo, ruling por ruling

| si falla | la ruling que queda tocada | y que se escribe |
|---|---|---|
| `F03` | **`swiss •` / `SEEN_BY_EYE`** | se **retira la fila** de `SEEN_BY_EYE` en `tests/test_components.py`. La marca vuelve a estar bajo el piso de cobertura de Q1 y swiss necesita el incremento que inc82 le hizo a instrument y a prism. `test_the_eye_exemption_is_named_measured_and_still_needed` exige que todo obligatorio bajo el piso este exento, asi que retirar la fila deja el test **en rojo hasta que la marca se arregle**. Eso es correcto y es el punto |
| `F03` acierta | idem | se **anade la sesion al campo `evidence`** de esa fila, con fecha, condicion de luz y `n = 1`. La exencion deja de ser la lectura de quien escribe |
| `F15`-`F18` fallan y `F19`-`F22` aciertan | **`L12`** | L12 pasa de *NUEVA Y ABIERTA* a **confirmada por observacion**, y ademas **agravada**: el match no se encuentra ni siquiera con el segundo canal (peso o subrayado) que el aviso de §3 documenta. El docstring de los cuatro kits deja de decir solo `RECORDED AND NOT FIXED` |
| `F15`-`F18` **aciertan** | **`L12`** y su premisa | el limite deja de serlo, y la causa mas probable es el `bold`/`underline` que `match_branch()` no lee. **Esa es una correccion del instrumento, no del diseno**, y va a `MATCH_IN_GREY` |
| `F19`-`F22` tambien fallan | **`match tier by channel`** | no es L12: es la ruling de arriba la que cae, porque el match tampoco se encuentra **con** su canal declarado |
| `F01` | **`E`** | la ronda cinco refuto a la cuatro con un argumento de lectura (*"imposible de no ver"*) y la refutacion se cae. La objecion de la ronda cuatro se reabre |
| `F13` acierta los tres peldanos | **`L7`, `Q1`** | la afirmacion de la ronda cinco de que el peldano calmo *"en el PNG no esta"* se cae, y con ella el argumento de asimetria que le dio la etiqueta al frame |
| `F13` falla y `F14` acierta | **`L7`, `Q1`** confirmadas | la ronda cinco tenia razon en las dos, y por primera vez no es su propio ojo quien lo dice |
| `F09` senala las reglas de cien celdas | **`Q2`** | la particion por largo de tirada sigue siendo aritmeticamente cierta y **deja de describir lo que hace el ojo**. Es la clase de fallo que no se arregla subiendo un contraste |
| `F02` | **`Q2`** (clausula de estructura) | los lideres largos de ledger dejan de estar exentos por continuidad |
| `F10` | **`K8 / E6`, `C3'''`** | el abridor de la banda de solari son espacios sobre un segundo ground; si nadie lo ve, K8 acerto al declararlos tinta y C3''' es un defecto y no una nota |
| `F11` | **`K10`** | cuatro esquinas no prometen dos paredes; el rework de `blueprint_S4` deja de ser opcional |
| `F12` falla | **`C2`** | una ruling que el programa cree cerrada en los once no lo esta, y `ledger_S4` vuelve de `keep` |
| `F23` dice "la misma marca" | **`D, amended (K2)`, `L10`** | esa fila del censo deja de ser aritmetica y pasa a ser **confusion observada**; L10 gana su primer dato que no es una medicion de diametro |
| `F24` dice "dos marcas distintas" | **`D, amended (K2)`, `Q1 (COV)`** | se confirma que las distancias mas pequenas del instrumento son una afirmacion sobre **area** y no sobre confusion, que es justo lo que §6 argumento sin poder probarlo |
| `F04`, `F05` | **`Q1`, `L13`** | el arreglo de inc82 no compro lo que decia comprar y las dos celdas sin area siguen sin ser una marca |
| `F06` (tercera pregunta) | **`L10`** | el radio y el checkbox de naught no se distinguen, con un ojo y no con un calibre |
| `F07`, `F08` | **la sesion** | ver el umbral de calibracion arriba |

### Que se escribe de vuelta, y donde

1. **`SEEN_BY_EYE`**, en `tests/test_components.py`: los campos `evidence` (se anade la sesion, la
   fecha, la luz y el `n`) o la fila entera (se retira). Es el unico sitio del programa donde una
   sesion humana tiene poder de escritura declarado por la propia ley.
2. **Los docstrings de los cuatro kits de `MATCH_IN_GREY`**, si L12 queda confirmada u odiada.
3. **La seccion "lo que esta ronda no puede ver" del siguiente `PROTOTYPE-inheritors`**: **todo**
   resultado, acierte o falle, con el numero de participantes al lado. Un resultado de `n = 1` citado
   sin el `n = 1` es exactamente la clase de afirmacion vacia que esta sesion existe para corregir.
4. **§7 de la ronda cinco**, la tabla *"¿se encuentra a ojo a 16 px?"*: cada fila que esta sesion
   toque deja de ser un juicio de quien redacta y pasa a llevar una fuente.

---

## 6. Guion literal del operador

Se lee tal cual. **Lo que no esta escrito aqui, no se dice.**

### Al empezar

> "Gracias por el rato. Te voy a ensenar veinticuatro imagenes de pantallas de computadora, una por
> una. No son tuyas, no las hiciste tu, y aqui no se te esta evaluando a ti: se esta evaluando el
> diseno de esas pantallas. Si algo no se entiende, el error es del diseno."
>
> "Con cada imagen te voy a hacer una pregunta corta. Quiero que **me senales con el dedo** en la
> pantalla donde esta la respuesta. Si no la encuentras, dime *no la encuentro*: esa es una respuesta
> valida y es util."
>
> "No te acerques ni hagas zoom, por favor. Tengo veinte segundos por imagen; si se acaban, pasamos a
> la siguiente y no pasa nada."
>
> "¿Alguna duda antes de empezar?"

### Entre frames

> "Siguiente."

Y la pregunta que toque, **leida tal como esta escrita** en la tabla de §4. No se parafrasea.

- **Si pregunta que es la pantalla:** *"es una aplicacion de tareas, como una lista de pendientes."*
  Nada mas.
- **Si pregunta si va bien:** *"no hay respuesta buena o mala para mi aqui; senala lo que te
  parezca."*
- **Si senala y se queda callado:** *"¿ya?"* Nada mas. **No repitas la pregunta con otras palabras**:
  la segunda formulacion siempre es mas facil que la primera y contamina el dato.
- **Si dice "no la encuentro":** *"perfecto, lo anoto. Siguiente."* **No le ensenes la respuesta.**
  Tampoco al final del bloque.
- **Si se rie o se disculpa:** *"no, va bien; esto es lo que estamos midiendo."*

### Lo que el operador NO puede decir, ni una vez

- **No nombrar la marca.** Nunca "el puntito", "el circulo", "el simbolo", "el recuadro", "la
  rayita". La mitad de los frames existen para saber si la marca se encuentra sin que se la nombre.
- **No nombrar el color.** Nunca "lo que esta en rojo", "lo azul". Ocho de los 24 frames existen
  precisamente para saber si el color hace falta, y cuatro de ellos no lo tienen.
- **No dar la zona.** Nunca "mira arriba", "en esa columna", "mas a la derecha".
- **No confirmar ni negar.** Nunca "exacto", "casi", "mmm". **Un "mmm" es una pista.**
- **No explicar el kit, ni el programa, ni por que hay once versiones.** Eso se cuenta al terminar, y
  se cuenta entero.

### Al cerrar

> "Ya esta. Te cuento que era esto: son once versiones del mismo programa, dibujadas cada una con un
> vocabulario distinto de simbolos. Llevamos cinco revisiones mirandolas nosotros y tu eres la
> primera persona de fuera que las ve. Lo que no encontraste es exactamente lo que necesitabamos
> saber."

Y **una sola** pregunta abierta, al final y no antes:

> "¿Hubo alguna imagen que te haya parecido especialmente confusa?"

Se anota literal, sin interpretarla y sin repreguntar.

---

## 7. Lo que esta sesion NO va a poder ver

Se dice aqui, antes de correrla, para que no haya que descubrirlo despues.

1. **Usuarios reales, en plural.** Es **una** persona. La ISO 9241-210 pide evaluacion con usuarios y
   una sesion de `n = 1` es la primera pulgada de eso, no el trayecto. Ninguna frase del informe que
   salga de aqui puede omitir el `n`.
2. **Un solo ancho, una sola altura.** 100x32. Los dos rojos de solari a 80x24 y las cuatro barras de
   teclas que se caen a 24 filas (C12) siguen sin ojo humano.
3. **Ninguna tecla.** El foco es decoracion en los 66 frames y lo sigue siendo aqui. Tab order,
   atrapado de foco en el modal y viaje del anillo son la parte de *"el diseno atiende la experiencia
   completa"* que este corpus no ha tocado nunca, y el mecanismo real que existe y no se ha usado es
   `App.run_test()` + `Pilot`.
4. **Ninguna latencia, ningun estado vacio en movimiento, ningun error de red.** Las pantallas de
   estado vacio (`S6` sin resultados) se ven, pero como fotografia: nadie espera a que aparezcan.
5. **Una sola condicion de luz.** Con un participante no se puede contrabalancear iluminada contra
   penumbra, y **diez de los once kits son de fondo oscuro**; el unico claro es ledger, que aparece
   en `F02` y `F12`. La condicion de la sesion es un dato, no un detalle, y un fallo de un kit oscuro
   en sala iluminada es tambien una hipotesis sobre la luz. Al reves: **si ledger acierta y los
   oscuros fallan, la primera hipotesis es la sala y no el kit**, porque ledger es la unica
   observacion del otro lado.
6. **Un solo idioma de pantalla.** El corpus escribe en ingles y el participante es hispanohablante.
   Las preguntas van en espanol y las pantallas no. **`F02` es el frame donde mas pesa**, porque su
   respuesta es leer un titulo. Si `F02` falla, la primera hipotesis es el idioma y no `Q2`, y hay
   que decirlo asi.
7. **La densidad, la animacion y los `SPIN`** de darkside y prism, que siguen sin censar.
8. **El muestreo es desigual a proposito.** S1 y S3 llevan dos frames y S6 lleva ocho. Un fallo
   aislado en S1 no se puede atribuir al criterio ni al kit, porque solo hay dos observaciones. En S6
   si, porque hay cuatro kits en dos versiones cada uno.
9. **La sesion no puede arreglar un instrumento.** El aviso de §3 sobre `match_branch()` salio de
   leer el sidecar y de medir tinta, no de una persona, y ninguna respuesta de `F15` a `F22` lo
   confirma ni lo refuta por si sola: si el match se encuentra en gris, la explicacion mas probable
   es el `bold` que la clasificacion no lee, pero **probable no es medido**.
10. **Los 42 frames que no estan.** 24 de 66. Cuarenta y dos combinaciones de kit y pantalla no las
   mira nadie de fuera en esta sesion, y once de las 46 notas de legibilidad de la ronda cinco quedan
   exactamente donde estaban.

---

## 8. Como se construyo la pagina

```
python -X utf8 C:\Users\jjgh8\.claude\jobs\85046efb\tmp\gal\build_sesion_page.py
```

- Los 22 PNG salen de `prototypes/components/png/` **tal cual**, incrustados como `data:` URI, con
  `width` y `height` iguales a su tamano en pixeles. **No hay una sola regla de CSS que los escale.**
- Los 2 recortes de celda se cortan de `png/naught_S2.png` en `(col*9, fila*19)`, con la misma caja
  de 9x19 px del corpus, y se repiten ocho veces a 1:1.
- **Cada celda de la clave de respuestas se afirma contra el `.txt` enviado antes de escribirse.** Si
  un `.txt` cambia una columna, el build muere con `ORACULO ROTO <frame> fila N col M` y no publica
  una respuesta equivocada. Durante la construccion de esta hoja el oraculo mordio **cinco veces**
  (dos columnas mal contadas y tres puntos de codigo braille equivocados), que es la unica prueba de
  que puede morder.
- Verificado al cerrar, **en el navegador y no en el fichero**
  (`skills/browser-automation/browser.mjs`, patchright headless, `file://`):
  **24 `<img>`, las 24 pintadas a su tamano natural** (`naturalWidth` = atributo `width` =
  `getBoundingClientRect().width` en las 24; 22 de 900x608 y 2 de 171x19), **24 `<details>` cerrados
  por defecto**, **36 preguntas**, 24 filas de hoja, **cero errores de consola** (linea de captura
  limpia, sin `capture DEGRADED`), **cero peticiones fallidas**, **cero recursos externos**, cero
  guiones largos en el texto pintado, sin scroll horizontal del documento, fondo de `body`
  explicito en claro (`rgb(251,251,249)`), en oscuro (`rgb(20,20,20)`) y en `@media print`
  (`rgb(255,255,255)`). **1.137.519 bytes = 1,08 MB**, muy por debajo del limite de 8 MB.

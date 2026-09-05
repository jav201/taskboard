# PROTOTYPE — seis pantallas canónicas × cinco lenguajes

> **AMENDMENT 2026-09-04, after the operator's verdict.** The matrix in §1 and the per-language sections
> below are the record of the PROTOTYPE ROUND and are kept verbatim. The batch that executed the verdict
> is `kits-learn-3` (`.fast-dev-flow/spec.md`, packets `inc14.md`..`inc19.md`), and it moved the matrix
> from **0** cells at `implementa` to **14 of 30**. The `.candidates.md` sidecars beside these frames have
> been RE-RENDERED and now describe the current frames, so where §1 and a sidecar disagree, **the sidecar
> is right and §1 is history**. Re-run `python -X utf8 prototypes/components/matrix.py` for the live table.


**Ronda de prototipo, no de implementación.** 30 frames reales renderizados por la ruta del kit
(`taskboard.language` → `Static` headless → `capture_languages.svg_from_grid`). **`taskboard/language.py`
y los once kits están intactos.** Suite del worktree: `341 passed, 2 skipped`. Falta tu veredicto antes
de tocar un kit.

---

## 1. La matriz 6 × 5

Derivada de los propios `Sheet` por `matrix.py`, no escrita a mano — la tabla y los frames no pueden
discrepar. `R` = rehúsa, `E` = evoca. *Implementa* significa que **ninguna** parte de esa celda se
dibujó a mano.

| | S1 lista+detalle | S2 formulario | S3 ajustes | S4 modal | S5 monitor | S6 paleta |
|---|---|---|---|---|---|---|
| **corgi** | evoca 2E | evoca 3E | evoca 3E | **rehúsa** 1R/1E | **rehúsa** 1R/2E | evoca 2E |
| **blueprint** | **rehúsa** 1R/1E | evoca 3E | evoca 3E | **rehúsa** 2R/2E | evoca 2E | evoca 2E |
| **prism** | evoca 2E | evoca 3E | evoca 3E | evoca 3E | evoca 2E | evoca 2E |
| **naught** | evoca 2E | evoca 3E | evoca 3E | **rehúsa** 1R/3E | evoca 2E | evoca 2E |
| **ledger** | evoca 2E | evoca 3E | **rehúsa** 1R/2E | **rehúsa** 1R/0E | **rehúsa** 1R/2E | evoca 2E |

**El elemento que decide cada celda** está en el `.candidates.md` de cada frame, con el número de fila
exacto donde se dibujó. No hay ninguna celda `implementa` y ninguna `falta`: los cinco lenguajes
pudieron renderizar las seis pantallas, y ninguno pudo hacerlo sólo con primitivas del kit.

**Ese es el hallazgo de la ronda.** No es que un lenguaje sea débil — es que **doce primitivas faltan en
los cinco a la vez**, y cada pantalla tropieza con al menos dos. Un kit con nueve componentes
(`bar, button, checkbox, radio, scrollbar, slider, stepper, switch, textfield`) y seis estados
(`default, focused, edited, active, checked, disabled`) no alcanza para las pantallas que toda app de
terminal tiene. **`STATES` no tiene `invalid`**: la premisa entera de S2 no tiene asiento en el contrato.

---

## 2. Por lenguaje

**corgi** — *ya tenía y bastó:* la tira de modos numerada, las ranuras grabadas de la tarjeta
(`DUE/PR/ST`), el LCD de segmento en meter/spark/gauge, los estados de botón (`▔▔` foco, `··`
deshabilitado). *Rehúsa dos veces, y ambas son diseño:* el overlay del modal — «el modo se apodera de
la pantalla», así que un confirm **es un modo**, numerado, y el tablero desaparece (`corgi_S4`); y la
etiqueta del readout — **L-33**, los números *son* el keymap, así que un readout se **rotula**, nunca se
numera (`corgi_S5`). *Propone:* `keyhint` (ya tiene la notación, le falta el asiento).

**blueprint** — *ya tenía y bastó:* `dimension()`, `series()`, `stamp()` acoplado a la esquina inferior,
el hatch, la marca de registro como cursor. *Rehúsa la regla vertical* en S1 y S4: sus diez marcas no
contienen ningún trazo vertical, así que un divisor de paneles es **inconstruible** — la división es
aire en un segundo datum. *Rehúsa la caja del modal* por lo mismo; las cuatro esquinas de registro
**no se tocan** (se corrigió a mitad de ronda: la primera pasada corrió un `─` entre ellas, que es una
tapa de caja por mucho que se deletree distinto). *Propone:* `knockout_cell` — y con ella la pregunta 10.

**prism** — **el único que no rehúsa nada.** Sus compromisos autorizan las seis pantallas, y es el único
lenguaje al que su propia doctrina le **permite** el borde del modal («los bordes están reservados para
modales»); el tablero detrás retrocede un paso de gris con `depth_ground()`, que el kit ya calcula. Es
también el que menos tinta gasta (8.6 %–17.8 %). *Propone:* `overlay` — el mecanismo existe, falta la
primitiva.

**naught** — *ya tenía y bastó:* el lattice visible, los sprites dibujados (`wordmark`), el dotgrid.
*Rehúsa el marco del modal* — «no frames at all» es uno de sus cuatro compromisos; la separación es la
**carga** del lattice: una banda encendida entre dos reglas encendidas, con el tablero apagado detrás
(`naught_S4`). *Propone:* `recede` — su scrim es el lattice que ya dibujaba.

**ledger** — *ya tenía y bastó:* las columnas regladas (`cols()`), los puntos guía, el tally, la banda
cada 5 líneas, el folio. **Rehúsa tres veces, y una es al nivel del contenido:** «nada se borra, todo se
cuadra» descarta el borrado silencioso *como diseño*, así que «¿borrar 3 tareas?» no es un diálogo que
este lenguaje pueda renderizar con honestidad — lo que renderiza es el **asiento de reversión**
(`ledger_S4`), y por la misma razón rehúsa el botón destructivo en S3 (`ledger_S3`). También rehúsa
numerar el readout, como corgi. Es el más denso con diferencia (47.5 % en S1).

---

## 3. Por pantalla — qué componente costó más, en más lenguajes

| pantalla | primitivas que faltan (× lenguajes) | la más difícil |
|---|---|---|
| S1 | `field_row`×5, `pane_split`×5 | **`field_row`** |
| S2 | `INVALID`×5, `required`×5, `textarea`×5 | **`INVALID`** |
| S3 | `select`×5, `menu`×5, `danger`×5 | **`menu`** |
| S4 | `overlay`×5, + 5 más | **`overlay`** |
| S5 | `log_row`×5, `tail`×5 | **`log_row`** |
| S6 | `match`×5, `keyhint`×5 | **`match`** |

**Las dos que van primero al `COMPONENTS.md` del skill:**

1. **`STATES += INVALID`.** Es la única que no es una primitiva sino un **eje**: sin sexto estado, los
   nueve componentes no tienen respuesta para un formulario, y hoy los cinco lenguajes marcan el error
   con un `!` rojo idéntico — el fallo de palette-swap exacto contra el que el skill escribe, en un
   glifo. Debe derivarse en `component_states` como los otros cinco y leerse en **glifo + estructura**,
   nunca sólo en el matiz de alerta.
2. **`Kit.field_row`.** La fila `rótulo → valor` es la forma **más reutilizada** de las seis pantallas
   (panel de detalle, KPI, resumen de ajustes) y la única sin asiento. Hoy los cinco frames dibujan el
   mecanismo de **ledger** (puntos guía): la respuesta propia de un lenguaje generalizada a cuatro que
   nunca la eligieron.

Un hallazgo colateral, dicho porque afecta a cómo se juzgan estos frames: **el knockout de blueprint es
invertir el fondo, y el `.txt` no lo lleva.** En el grid de celdas `DELETE` se lee igual que cualquier
palabra; sólo el `.svg` lo muestra. La convención de la casa es que el `.txt` es la obra — aquí no basta.

---

## 4. Preguntas para el veredicto (cerradas)

1. ¿`invalid` entra al registro `STATES` como sexto estado derivado, **o** la validación es notación del
   llamador y el kit sólo presta `Kit.error(msg, w)`?
2. ¿`Kit.field_row` es primitiva nueva, **o** el panel de detalle debe componerse con `card_rows` y esa
   fila simplemente no existe?
3. ¿Corgi **numera** los botones de un formulario o los **rotula**? (los números son el keymap: ¿un botón
   es un control numerable, o gasta una tecla que no le toca?)
4. ¿Naught dibuja un overlay, **o** su respuesta definitiva es cambiar la carga del lattice (lo que
   propone `naught_S4`)?
5. ¿Prism es el **único** autorizado a dibujar borde de modal, y los otros cuatro rehúsan por compromiso?
6. ¿Ledger rehúsa el botón destructivo por género («nada se borra»), **o** se acepta `danger=True` con
   mecanismo de **forma** (no de color, que ya está gastado en la deuda)?
7. ¿`Kit.select` es primitiva propia, **o** `stepper` cubre el estado cerrado y sólo falta `Kit.menu`?
8. ¿El nivel de log es una entrada nueva en `ICONS` (`info/warn/error`), **o** una `Kit.log_row` completa?
9. ¿`Kit.match` obliga a la ley de contenido byte por byte — es decir, **prohíbe** el recasing en esa fila
   a los tres lenguajes que mayusculizan títulos?
10. ¿El knockout de blueprint puede **moverse** del title block a la respuesta por defecto en un confirm,
    manteniendo «exactamente uno por vista»?

---

## 5. Plan de implementación propuesto (no ejecutado)

Batch `kits-learn-3`, **sólo las celdas que apruebes**. Cada incremento: ≤ 4 archivos, un **property
test** (no sólo mutación: «¿se lee el token?» vs «¿se lee correctamente?»), y una **captura antes del
commit**.

| # | incremento | archivos | property test |
|---|---|---|---|
| 1 | `INVALID` en `STATES` + `component_states` | `language.py`, `test_components.py`, 2 frames | que `component_states("textfield")` lo derive y que el estado sobreviva en escala de grises |
| 2 | `Kit.field_row` + los 5 mecanismos | `language.py`, test, frame | que dos lenguajes no devuelvan la misma fila con el mismo `(caption, value, w)` |
| 3 | `Kit.select` / `Kit.menu` | `language.py`, test, frame | que `menu` respete el rehúse de overlay de quien lo declare |
| 4 | `Kit.overlay` + registro de rehúses | `language.py`, test, frame | que los 4 rehúses estén **declarados** y sean falsables (patrón `LABEL_REFUSED`) |
| 5 | `Kit.log_row` + `Kit.tail` | `language.py`, test, frame | que el nivel se lea en glifo, con el color quitado |
| 6 | `Kit.match` + `Kit.keyhint` | `language.py`, test, frame | que el texto vuelva byte por byte (ley de contenido, L-33/inc12) |

Después: `export_to_skill.py`, frames a `prototypes/gallery/` con su línea `L-NN`, y las secciones que
`COMPONENTS.md` no tiene. Los seis lenguajes restantes heredan al final.

---

## 6. Los 30 frames

`.txt` es la obra, `.svg` es una foto de ella en color. Cada frame tiene su `.candidates.md` al lado.

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| corgi | [txt](corgi_S1.txt) · [svg](corgi_S1.svg) · [cand](corgi_S1.candidates.md) | [txt](corgi_S2.txt) · [svg](corgi_S2.svg) · [cand](corgi_S2.candidates.md) | [txt](corgi_S3.txt) · [svg](corgi_S3.svg) · [cand](corgi_S3.candidates.md) | [txt](corgi_S4.txt) · [svg](corgi_S4.svg) · [cand](corgi_S4.candidates.md) | [txt](corgi_S5.txt) · [svg](corgi_S5.svg) · [cand](corgi_S5.candidates.md) | [txt](corgi_S6.txt) · [svg](corgi_S6.svg) · [cand](corgi_S6.candidates.md) |
| blueprint | [txt](blueprint_S1.txt) · [svg](blueprint_S1.svg) · [cand](blueprint_S1.candidates.md) | [txt](blueprint_S2.txt) · [svg](blueprint_S2.svg) · [cand](blueprint_S2.candidates.md) | [txt](blueprint_S3.txt) · [svg](blueprint_S3.svg) · [cand](blueprint_S3.candidates.md) | [txt](blueprint_S4.txt) · [svg](blueprint_S4.svg) · [cand](blueprint_S4.candidates.md) | [txt](blueprint_S5.txt) · [svg](blueprint_S5.svg) · [cand](blueprint_S5.candidates.md) | [txt](blueprint_S6.txt) · [svg](blueprint_S6.svg) · [cand](blueprint_S6.candidates.md) |
| prism | [txt](prism_S1.txt) · [svg](prism_S1.svg) · [cand](prism_S1.candidates.md) | [txt](prism_S2.txt) · [svg](prism_S2.svg) · [cand](prism_S2.candidates.md) | [txt](prism_S3.txt) · [svg](prism_S3.svg) · [cand](prism_S3.candidates.md) | [txt](prism_S4.txt) · [svg](prism_S4.svg) · [cand](prism_S4.candidates.md) | [txt](prism_S5.txt) · [svg](prism_S5.svg) · [cand](prism_S5.candidates.md) | [txt](prism_S6.txt) · [svg](prism_S6.svg) · [cand](prism_S6.candidates.md) |
| naught | [txt](naught_S1.txt) · [svg](naught_S1.svg) · [cand](naught_S1.candidates.md) | [txt](naught_S2.txt) · [svg](naught_S2.svg) · [cand](naught_S2.candidates.md) | [txt](naught_S3.txt) · [svg](naught_S3.svg) · [cand](naught_S3.candidates.md) | [txt](naught_S4.txt) · [svg](naught_S4.svg) · [cand](naught_S4.candidates.md) | [txt](naught_S5.txt) · [svg](naught_S5.svg) · [cand](naught_S5.candidates.md) | [txt](naught_S6.txt) · [svg](naught_S6.svg) · [cand](naught_S6.candidates.md) |
| ledger | [txt](ledger_S1.txt) · [svg](ledger_S1.svg) · [cand](ledger_S1.candidates.md) | [txt](ledger_S2.txt) · [svg](ledger_S2.svg) · [cand](ledger_S2.candidates.md) | [txt](ledger_S3.txt) · [svg](ledger_S3.svg) · [cand](ledger_S3.candidates.md) | [txt](ledger_S4.txt) · [svg](ledger_S4.svg) · [cand](ledger_S4.candidates.md) | [txt](ledger_S5.txt) · [svg](ledger_S5.svg) · [cand](ledger_S5.candidates.md) | [txt](ledger_S6.txt) · [svg](ledger_S6.svg) · [cand](ledger_S6.candidates.md) |

### Cómo reproducir

```
python -X utf8 prototypes/components/render.py    # 30 .txt + 30 .svg + 30 .candidates.md
python -X utf8 prototypes/components/matrix.py    # la matriz de §1
python -X utf8 -m pytest -q                       # 341 passed, 2 skipped
```

`fixture.py` es el contenido único que leen los cinco lenguajes — una sola tarea, un solo formulario, un
solo log. Si un lenguaje leyera un número distinto estaría siendo halagado, no probado.

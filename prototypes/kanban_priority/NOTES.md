# Prototipo — señal de prioridad alta en kanban

**Pregunta.** «KANBAN necesita algunos cues de color o tamaño (o algo) para
diferenciar tareas con alta prioridad.» Hoy la prioridad alta es un único `!`
en tono `ink` a la derecha de la tarjeta (`card_cell`, THE GLYPH HOUSE: ámbar =
vence hoy, hues de proyecto = identidad). ¿Qué señal se ve sin romper esa casa?

**Dónde verlo.** `prototypes/edit_modal/out/ronda-edicion-prioridad.html`,
sección 2.

**Forma.** Sub-shape A: la app real en kanban (grouped), con
`views.card_cell`, `views.kanban_order` y `views._kanban_column_rows`
parcheados por variante dentro del prototipo. Fixture
(`fixture.py`, compartido con edit_modal): 4 proyectos (sky, lime, violet,
**pink** a propósito), 21 tareas en Backlog/Doing/Review/Done, 6 altas: 5
abiertas + 1 terminada («Release 3.4», que no grita: toda variante aplica la
señal solo a altas no terminadas y no archivadas). Selección en una tarjeta
normal.

## Variantes

- **0 · Baseline** — `!` ink.
- **K1 · Franja** — `▊` de proyecto + `▌` ink negrita en el espacio siguiente,
  título negrita brillante; el `!` se quita (la franja ya lo dice).
  *Si se quiere color:* no hay hue libre limpio. El menos malo sería
  `orange #fb923c` (ya no es hue de proyecto ofrecido — se remapea a fuchsia —
  y no es severidad), pero es vecino de `amber` (= hoy). Recomiendo quedarse en
  ink + negrita.
- **K2 · Tamaño** — la tarjeta alta ocupa 2 filas: la normal + primera línea de
  notas (o el chip de fecha si no hay notas), con la franja continuando.
  `line_map` apunta a la primera fila (la segunda es `(markup, None)`).
- **K3 · Insignia inversa** — `!!` en video inverso `rose` (`_priority_hue`
  del gantt) tras la franja.
- **K4 · Banda** — en cada columna las altas abiertas suben a una banda
  `── high ──` cerrada por una regla; el resto sigue en sus grupos. Va por
  `kanban_order` (el único asiento de orden), así la navegación sigue la vista.

## Hechos medidos (render real, `out/facts_kanban.json`)

| variante | filas tablero 120×36 | filas 80×24 | Δ caracteres de título por tarjeta alta (120 / 80) |
|---|---|---|---|
| 0 | 16 | 16 | — (12–17 visibles a 120; 2–7 a 80) |
| K1 | 16 (+0) | 16 (+0) | **+2 / +2** (se libera la celda del `!`) |
| K2 | 18 (+2) | 18 (+2) | 0 / 0 — cuesta 1 fila por tarjeta alta abierta |
| K3 | 16 (+0) | 16 (+0) | **−1 / −1** (insignia 3 celdas vs `!` 2) |
| K4 | 17 (+1) | 17 (+1) | 0 / 0 — cuesta 2 filas por columna con altas (divisor + regla), menos los encabezados de grupo que se vacían |

Las 21 tareas siguen en `line_map` en todas las variantes.

## Conflicto de color de K3 (verificado contra la paleta)

`rose #fb7185` ya no es hue de proyecto ofrecido (`PROJECT_COLORS` lo retiró y
`DROPPED_PROJECT_COLORS` lo remapea a `pink #f472b6`, distancia 49.5), pero
**pink sí lo es** — en el fixture «Marketing site» es pink y la insignia queda
pegada a una franja casi del mismo tono. Además rose está junto a
`over #f43f5e` (vencido/bloqueado): en «Login con biometría» la insignia y el
`-1d` rojo se leen como la misma alarma. `▲` se descartó porque ya es el glifo
de bloqueado (`status_glyph` y el prefijo `▲ `).

## Límites encontrados

- A 80 col los títulos ya son de 2–7 caracteres en la base; K3 los deja en 1–6.
- K2: la nota de la segunda fila usa `_focus_note_snippet`, que recorta ANTES
  de resaltar: un `!!…!!` cortado muestra los marcadores crudos (`==A…`).
- K4: el parche cambia `kanban_order` para TODAS las presentaciones (lanes y
  el navegador incluidos); en lanes la banda aparecería como un carril
  llamado `\x00high` — no se probó lanes ni matrix.
- K1/K3 parchean `card_cell`, que también usa la presentación lanes; no se
  capturó.
- El cambio de variante en vivo usa `shift+←/→` (← y → ya navegan el tablero).
- El reloj del ribbon es la hora real de la captura.

## Cómo correrlo

    python prototypes/kanban_priority/proto.py            # vivo: 0-4, shift+←/→
    python prototypes/kanban_priority/proto.py live K3 12 # abre K3, sale a los 12 s
    python prototypes/kanban_priority/proto.py shot       # SVGs + facts_kanban.json
    powershell -File prototypes/edit_modal/shoot.ps1 -Proto kanban_priority -Variant K3

**Estado.** Desechable. Nada en `taskboard/` cambió. Pin: textual 8.2.8.

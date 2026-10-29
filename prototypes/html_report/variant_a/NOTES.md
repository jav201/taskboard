# Variante A — Status report / one-pager para reunión

Documento de estado que lee **a través de los tres boards** (Personal, Client A,
Course): fichas de resumen, qué se movió en los últimos 7 días
(`phase_changed`), trabajo atrasado y próximos 7 días en dos paneles, hitos
agrupados por su clase (Delivery ▲ / Billing ■ / Launch ★), cadenas de
dependencia y progreso por proyecto (done vs open vs archived, due del
proyecto, momentum). Al final, una tabla de @menciones resueltas a nombres. Es
un documento para leer e imprimir: cero JavaScript, cero peticiones externas,
tema claro/oscuro con `prefers-color-scheme`, reflow a 390px sin desbordes y
una hoja de impresión compacta (A4, 2 páginas, snippets de notas recortados en
papel, todo lo demás con etiqueta directa). Respeta las leyes de honestidad de
`taskboard/report.py`: solo conteos y fechas, nada pronosticado; todo texto del
usuario escapado; la cifra nunca viaja sola en el color.

## La propuesta de exportación

**a. La tecla.** Revisado `taskboard/keymap.py`: en el mapa global están
tomadas a–m, o–x, z, `,`, `;`, `?`, `[`, `]`, `!`, `+`, `-`, espacio, enter,
esc, tab, `@`, `#`, flechas y A B F I L M P R S T X (L=Link, R=Present, x=archive).
Libres en minúscula: **n r w y**; libres en mayúscula: **C D E G H J K N O Q U V W Y Z**.
`PRESENT_KEYS` (R, PresentScreen) ata su propio juego — 1-3, tab, shift+flechas,
pgup/pgdn, espacio, a, u, K, J, enter, x, esc, q, ? — así que dentro de R también
sobran H y W. **Elegida: `H`, GLOBAL** (fuera de R, desde cualquier vista). Qué
exporta: **todos los boards cargados** en el formato de esta variante — el
status de reunión se lee cruzando boards, no desde uno solo. Dentro de R queda
reservada para una exportación futura de "lo que la presentación muestra u
oculta" (proyecto actual + curaduría), que es otra pregunta y merece otra
tecla cuando exista.

**b. Dónde cae y qué dice la app.** Misma convención que `report.py`
(`report_path`): junto al board, en `reports/`, con fecha fija en el nombre:
`reports/status-<YYYY-MM-DD>.html` (al ser multi-board se escribe en el
directorio del board activo y el aviso lo dice entero). Toast, estilo notify de
la app: **"Report written: reports/status-2026-10-29.html · o opens it"**.
Seguimiento con **`o`**: tras exportar, la app recuerda el último report y `o`
(lo hoy `open_url`) lo abre en el navegador; si no hay report reciente, `o`
sigue abriendo la URL de la tarea como siempre.

**c. ¿Sustituye o convive con el SVG (x dentro de R)?** **Convive.** El SVG de
la presentación es una *imagen* de la vista curada: sirve para proyectar o
embeber el diseño exacto de la timeline. Este HTML es un *documento de datos*:
se lee, se imprime y se puede procesar. Son dos asientos distintos — el que
presenta y el que informa — y pegar uno encima del otro dejaría sin hogar a la
curaduría de R.

## Límites conocidos / qué necesitaría la versión real

- `phase_changed` solo registra el último movimiento: el bloque "what changed"
  muestra la fase destino, no de dónde vino ni quién lo movió. El dato no
  existe; el reporte no lo inventa.
- Las cadenas se dibujan como camino lineal; si una tarea tuviera varios hijos
  (grafo con bifurcación) solo se recorre el primero. La versión real necesita
  recorrer el árbol completo o declarar el límite.
- El reporte exporta todo lo visible; no conoce la curaduría de R (filas
  ocultas con espacio, `hidden_picker`). Una opción "lo que muestra la
  presentación" necesitaría recibir ese filtro como parámetro.
- Un hito sin clase (mark vacío o clase borrada) no tiene grupo en "Milestones
  by class"; el fixture no lo ejercita, pero el HTML real necesitaría una
  sección "uncategorized" para no perderlo.
- En papel se recortan los snippets de notas (para caber en 2 páginas): las
  evidencias `==/!!/++` y las @menciones viven en pantalla; si la reunión las
  necesita en papel, habría que elegir qué otra sección cede el espacio.

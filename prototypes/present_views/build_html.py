"""Build the verdict page from the app captures (PNGs embedded as base64).

    python prototypes/present_views/app_capture.py
    python prototypes/present_views/build_html.py
"""
from __future__ import annotations

import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "present-views-prototype.html"


def img(name: str, cap: str, narrow: bool = False) -> str:
    data = base64.b64encode((OUT / f"{name}.png").read_bytes()).decode()
    cls = ' class="narrow"' if narrow else ""
    return (f'<figure{cls}><figcaption>{cap}</figcaption>'
            f'<img alt="{cap}" src="data:image/png;base64,{data}"></figure>')


VARIANTS = [
    ("A", "gantt", "1", "La vista actual, sin cambios",
     "<p>La presentación que ya existe: regla de fechas, campo Gantt con chips de inicio–fin, "
     "una línea por tarea y las notas de la tarea del cursor recortadas a 3 líneas. Lo único "
     "nuevo es la palabra <code>gantt</code> en gris junto al nombre del proyecto, que dice "
     "en qué vista está la sala.</p>",
     ["Sigue siendo la única vista que muestra el <em>calendario</em> del proyecto completo.",
      "No cambia nada de lo aprobado (oráculo PRES-R)."],
     ["Las notas se leen solo para una tarea y a 3 líneas.",
      "El renderer actual <strong>aplana los saltos de línea</strong>: una nota con lista "
      "numerada se lee «Sep 22. 1. Feature-flag…» (ver la captura con <code>⇥</code>). "
      "Es un defecto del helper actual, no de esta ronda."],
     [("118-A-gantt", "118 × 31 · cursor en «Fix checkout 500 error»", False),
      ("118-tab-cycle", "118 × 31 · ⇥ desde split vuelve a gantt; el cursor (Launch) viaja entre vistas y su nota pierde los saltos de línea", False),
      ("80-A-gantt", "80 × 25", True)]),
    ("B", "cards", "2", "Tarjetas: todo el proyecto legible de un vistazo",
     "<p>Cada tarea abierta es una tarjeta en una cuadrícula (3 columnas desde 100 de ancho, 2 "
     "debajo). Sin cajas: una barra vertical del color del proyecto marca la altura de la "
     "tarjeta; la tarjeta del cursor lleva barra y título en acento. Cada tarjeta trae título, "
     "fase · prioridad, inicio–fin con días relativos, la nota con párrafos y viñetas, "
     "«waits on» y el conteo de links e imágenes. Cuando el alto no alcanza, se encoge primero "
     "la fila más alta y la del cursor cede al final; lo cortado se declara (<code>… +4 lines</code>).</p>",
     ["La sala ve todo el contenido a la vez; sirve para «repasemos todo».",
      "No necesita navegación: el cursor solo resalta.",
      "La nota vacía se ve como estado (<code>no notes</code>), no como hueco."],
     ["Una nota larga se corta: la tarjeta no es lugar para un plan de 30 líneas.",
      "A 80 × 25 caben 3 filas de tarjetas con 2–7 líneas de nota cada una; con más de "
      "6 tareas haría falta paginar (no prototipado).",
      "Pierde el calendario: las fechas son texto, no barras."],
     [("118-B-cards", "118 × 31 · 5 tarjetas, cursor en «Fix checkout 500 error»", False),
      ("118-B-cards-moved", "118 × 31 · → → cursor en «Launch new homepage»: su fila crece", False),
      ("118-B-cards-hidden", "118 × 31 · ← ␣ «Optimize image assets» oculta: sale de la cuadrícula; «1 hidden» solo en la fila de ayuda", False),
      ("80-B-cards", "80 × 25", True),
      ("80-B-cards-moved", "80 × 25 · cursor movido", True)]),
    ("C", "slide", "3", "Diapositiva por tarea",
     "<p>Una tarea llena el marco como una lámina. Título en mayúsculas espaciadas (tipo "
     "display sin fuente), subrayado en acento (es el cursor). A la derecha, la <strong>figura "
     "dibujada</strong>: los días de atraso o restantes en dígitos de bloque (la fuente 4×7 de "
     "<code>wave.py</code>), rojo si va tarde. Debajo: inicio–fin, prioridad, la escalera de fases "
     "(<code>● Backlog ── ◉ DOING ── ○ Review</code>), de qué depende y qué desbloquea, links "
     "e imágenes, y la nota completa a un ancho de lectura de 88 columnas. Abajo, una tira de "
     "posición estilo deck: anterior · puntos · <code>2 / 5</code> · siguiente. "
     "<code>←→</code> pasa de lámina.</p>",
     ["Es lo más legible a distancia y lo más «presentable»: una idea por pantalla.",
      "La nota larga cabe entera a 118 × 31; a 80 × 25 se desplaza con <code>pgdn</code> y "
      "el marco dice <code>↓ 7 more lines</code> / <code>↑ 4 lines above</code>.",
      "La figura (días) se lee desde el fondo de la sala sin leer texto."],
     ["Se pierde el contexto: no se ve el resto del proyecto ni el calendario.",
      "Los dígitos de bloque son un elemento nuevo en el app (código nuevo, aunque pequeño).",
      "El título espaciado solo cabe con títulos cortos; con títulos largos cae a mayúsculas normales."],
     [("118-C-slide", "118 × 31 · «Fix checkout 500 error», 2 días tarde", False),
      ("118-C-slide-moved", "118 × 31 · → → «Launch new homepage»: la nota larga completa", False),
      ("118-C-slide-empty", "118 × 31 · «SEO redirects map»: nota vacía", False),
      ("80-C-slide", "80 × 25 · la escalera de fases cabe; links completos", True),
      ("80-C-slide-long", "80 × 25 · nota larga: desborde declarado", True),
      ("80-C-slide-long-pgdn", "80 × 25 · pgdn: el resto de la nota", True)]),
    ("D", "split", "4", "Gantt arriba + panel de lectura",
     "<p>Las filas del Gantt actual tal cual (regla, proyecto, tareas, chips) y, debajo, en "
     "lugar de las líneas breves, un panel de lectura: a la izquierda los datos de la tarea del "
     "cursor (fechas, fase, prioridad, depende de, desbloquea, links, imágenes) y a la derecha "
     "su nota <strong>sin el tope de 3 líneas</strong>, con párrafos y listas. "
     "<code>pgdn</code> desplaza la nota cuando no cabe.</p>",
     ["Conserva el calendario y añade el contenido: es el paso más corto desde lo actual.",
      "Reutiliza los helpers ya probados del Gantt (<code>_present_ruler</code>, "
      "<code>_present_task_row</code>); el riesgo de implementación es el más bajo.",
      "A 118 × 31 la nota larga entra completa."],
     ["Solo una tarea a la vez se lee completa.",
      "El alto del panel depende de cuántas tareas tenga el proyecto: con 12 tareas, a 80 × 25 "
      "quedan ~5 filas para la nota.",
      "A 80 columnas los títulos del Gantt se cortan (<code>Build component…</code>), igual que hoy."],
     [("118-D-split", "118 × 31 · cursor en «Fix checkout 500 error»", False),
      ("118-D-split-long", "118 × 31 · «Launch new homepage»: la nota larga cabe completa", False),
      ("80-D-split", "80 × 25", True),
      ("80-D-split-long", "80 × 25 · nota larga: ↓ 6 more lines", True),
      ("80-D-split-long-pgdn", "80 × 25 · pgdn", True)]),
]


R2 = [
    ("D2", "stacked", "2", "Bloques apilados",
     "<p>Bajo las filas del Gantt, un bloque por tarea: encabezado (título · inicio–fin · días) y "
     "su nota con saltos de línea y listas. A partir de 100 columnas va en dos columnas (la primera "
     "mitad de las tareas a la izquierda); debajo, en una. El reparto es justo: si todo cabe, todo se "
     "ve; si no, la nota del cursor recibe hasta la mitad del espacio y las demás al menos 1–2 líneas, "
     "con <code>… +N lines</code>. La tarea sin nota ocupa una sola fila (<code>no notes</code> en su "
     "encabezado).</p>",
     ["Se lee como un documento: encabezado y texto, en el orden del Gantt.",
      "A 118 × 31 entran todas las notas casi completas (solo la larga pierde 2 líneas).",
      "La tarea sin nota cuesta 1 fila."],
     ["A 80 × 25 las notas que no son del cursor quedan en 1–2 líneas.",
      "En dos columnas el orden de lectura baja por la izquierda y luego sigue a la derecha."],
     [("r2-118-D2-stacked", "118 × 31 · cursor en «Fix checkout 500 error»: todas las notas visibles", False),
      ("r2-118-D2-stacked-long", "118 × 31 · cursor en «Launch new homepage» (nota larga)", False),
      ("r2-118-D2-stacked-hidden", "118 × 31 · «Optimize image assets» oculta: sale del Gantt y de los bloques", False),
      ("r2-80-D2-stacked", "80 × 25 · una columna; cursor en «Fix checkout 500 error»", True),
      ("r2-80-D2-stacked-long", "80 × 25 · cursor en la nota larga: recibe más líneas", True)]),
    ("D3", "columns", "3", "Una columna por tarea",
     "<p>Bajo el Gantt, una columna por tarea con nota (hasta 4 a 118 y 2 a 80; mínimo 28 celdas "
     "cada una), con título, fechas y la nota envuelta. Las tareas sin nota no gastan una columna: van "
     "juntas en una línea gris abajo (<code>no notes  SEO redirects map</code>). Si hay más tareas que "
     "columnas, se ve la ventana que contiene al cursor y la esquina dice <code>◂ 2 more</code> / "
     "<code>2 more ▸</code>.</p>",
     ["Cada nota tiene todo el alto del panel: a 118 se leen 4 notas completas a la vez.",
      "La comparación lado a lado es natural («qué dice cada tarea»)."],
     ["Columnas angostas (~26 caracteres): la nota larga se vuelve muy alta y se corta.",
      "A 80 solo caben 2 columnas: deja de ser «todas a la vez» con más de 2 tareas con nota.",
      "Con muchas tareas la ventana se mueve con el cursor, y el resto no se ve."],
     [("r2-118-D3-columns", "118 × 31 · 4 columnas; la tarea sin nota en la línea de abajo", False),
      ("r2-118-D3-columns-long", "118 × 31 · cursor en la nota larga", False),
      ("r2-118-D3-columns-hidden", "118 × 31 · una tarea oculta: quedan 3 columnas más anchas", False),
      ("r2-80-D3-columns", "80 × 25 · 2 columnas", True),
      ("r2-80-D3-columns-long", "80 × 25 · cursor en la nota larga: ◂ 2 more", True)]),
    ("D4", "inline", "4", "Nota bajo su barra",
     "<p>Cada nota va <strong>debajo de su propia fila del Gantt</strong>, con sangría bajo el título: "
     "la barra y su texto se leen juntos, y la regla de fechas sigue arriba, alineada con todas las "
     "barras. La nota del cursor lleva una guía en acento y recibe el espacio sobrante; las demás "
     "comparten el resto. La tarea sin nota es solo su fila del Gantt (0 filas extra).</p>",
     ["Sin vocabulario nuevo: es el Gantt, con el texto junto a su tarea.",
      "Usa todo el ancho para el texto (líneas largas, pocas filas por nota).",
      "La tarea sin nota no cuesta nada; ocultar una tarea libera su espacio para las demás."],
     ["El Gantt se «estira»: las barras quedan separadas por texto y la vista de conjunto del "
      "cronograma se pierde un poco (la regla queda lejos de las últimas filas).",
      "A 80 × 25 las notas que no son del cursor quedan en 1 línea + <code>… +N lines</code>."],
     [("r2-118-D4-inline", "118 × 31 · cursor en «Fix checkout 500 error»", False),
      ("r2-118-D4-inline-long", "118 × 31 · cursor en la nota larga", False),
      ("r2-118-D4-inline-hidden", "118 × 31 · una tarea oculta", False),
      ("r2-80-D4-inline", "80 × 25", True),
      ("r2-80-D4-inline-long", "80 × 25 · cursor en la nota larga", True),
      ("r2-80-D4-inline-hidden", "80 × 25 · una tarea oculta: la nota larga gana sus filas", True)]),
]


def round2() -> str:
    out = []
    for key, name, k, title, prose, pros, cons, shots in R2:
        pl = "".join(f"<li>{x}</li>" for x in pros)
        cl = "".join(f"<li>{x}</li>" for x in cons)
        figs = "".join(img(n, cap, nar) for n, cap, nar in shots)
        out.append(f'<section id="r2-{key}"><h3 class="v"><span class="tag">{key}</span> {name} · '
                   f'tecla <kbd>{k}</kbd> en este prototipo — {title}</h3>{prose}'
                   f'<div class="pc"><div><h3>A favor</h3><ul>{pl}</ul></div>'
                   f'<div><h3>En contra</h3><ul>{cl}</ul></div></div>{figs}</section>')
    first = img("r2-118-A-gantt", "118 × 31 · 1 gantt con el arreglo: la nota del cursor "
                "respeta párrafos (máx. 3 líneas)")
    return f"""<h2 id="r2">Ronda 2 · D con todas las notas</h2>
<p class="box"><strong>Conclusión:</strong> las tres variantes muestran las notas de <em>todas</em> las
tareas abiertas a la vez, con el Gantt arriba sin cambios y la tarea del cursor en acento. Recomiendo
<strong>D2 · stacked</strong>: a 118 × 31 se leen las cinco notas casi completas, a 80 × 25 sigue
mostrándolas todas (la del cursor con más líneas) y es la que mejor degrada. <strong>D4 · inline</strong>
es la alternativa si prefieres que cada texto quede pegado a su barra.</p>
<p>Mismo método que la ronda 1: app real en headless, teclas por el piloto, <code>export_screenshot()</code>
y PNG con Edge (<code>app_capture2.py</code>; renderers en <code>views_d.py</code>). En este prototipo las
teclas <kbd>2</kbd>–<kbd>4</kbd> eligen la variante para compararlas; en el producto la elegida sería la
única vista «split». Ya están aplicadas las decisiones aceptadas: abre siempre en gantt, solo tareas
abiertas, imágenes como conteo y nombre, y la nota de la vista gantt <strong>conserva sus saltos de
línea</strong> (primera captura).</p>
{first}
{"".join(out)}
<h3 class="v">Comparación · ronda 2</h3>
<table>
<tr><th></th><th>Notas visibles a 118 × 31</th><th>A 80 × 25</th><th>Tarea sin nota</th><th>Nota larga</th><th>Gantt</th><th>Riesgo</th></tr>
<tr><td>D2 stacked</td><td>todas, casi completas</td><td>todas, 1–4 líneas (cursor más)</td><td>1 fila</td><td>cursor: hasta la mitad del panel; <code>pgdn</code></td><td>intacto</td><td>bajo</td></tr>
<tr><td>D3 columns</td><td>4 completas</td><td>solo 2 (ventana + «more»)</td><td>línea común abajo</td><td>columna alta, se corta</td><td>intacto</td><td>medio (ventana)</td></tr>
<tr><td>D4 inline</td><td>todas, casi completas</td><td>todas, 1–2 líneas (cursor más)</td><td>0 filas</td><td>cursor gana el sobrante; <code>pgdn</code></td><td>estirado por el texto</td><td>bajo</td></tr>
</table>
<h3 class="v">Recomendación y preguntas · ronda 2</h3>
<ul>
<li><strong>Recomiendo D2 · stacked.</strong> Cumple «todas a la vez» en ambos tamaños, deja el Gantt compacto
y entero arriba, y el reparto (todo si cabe; si no, el cursor primero) es simple de probar.</li>
<li>¿Dos columnas desde 100 de ancho (como en las capturas) o una sola columna siempre, para leer de arriba abajo?</li>
<li>¿Cuánto se lleva el cursor cuando no cabe todo? Hoy: hasta la mitad del panel. Alternativa: reparto parejo.</li>
<li>¿Las vistas B (cards) y C (slide) de la ronda 1 se descartan, o C se queda como vista aparte?</li>
</ul>
<h2 id="r1">Ronda 1 · tres vistas de contenido</h2>
"""


def main() -> None:
    sections = []
    for key, name, k, title, prose, pros, cons, shots in VARIANTS:
        pl = "".join(f"<li>{x}</li>" for x in pros)
        cl = "".join(f"<li>{x}</li>" for x in cons)
        figs = "".join(img(n, cap, nar) for n, cap, nar in shots)
        sections.append(
            f'<section id="v-{key}"><h2><span class="tag">{key}</span> {name} · '
            f'tecla <kbd>{k}</kbd> — {title}</h2>{prose}'
            f'<div class="pc"><div><h3>A favor</h3><ul>{pl}</ul></div>'
            f'<div><h3>En contra</h3><ul>{cl}</ul></div></div>{figs}</section>')
    nav = "".join(f'<a href="#v-{v[0]}">{v[0]} · {v[1]}</a>' for v in VARIANTS)
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Present · content views</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.6rem 16px; display:flex; gap:1rem; flex-wrap:wrap; font-size:.9rem; }}
nav a {{ color:var(--acc); text-decoration:none; }}
main {{ max-width:1400px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .3rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
h3 {{ font-size:1rem; color:var(--mut); margin:.4rem 0; }}
h3.v {{ font-size:1.25rem; color:var(--fg); margin-top:2rem; }}
.tag {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px;
  padding:0 .5rem; font-family:ui-monospace,Consolas,monospace; }}
p, li {{ max-width:80ch; }}
code, kbd {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em;
  border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
.pc {{ display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; }}
figure {{ margin:1.2rem 0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; }}
figure.narrow img {{ max-width:68%; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
table {{ border-collapse:collapse; margin:1rem 0; font-size:.92rem; display:block; overflow-x:auto; }}
th, td {{ border:1px solid var(--line); padding:.35rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--mut); font-weight:600; }}
.box {{ border-left:3px solid var(--acc); padding:.4rem 1rem; background:#101722; }}
@media (max-width:700px) {{ .pc {{ grid-template-columns:1fr; }} figure.narrow img {{ max-width:100%; }} }}
</style></head><body>
<nav><strong>Present · content views</strong><a href="#r2">Ronda 2 · D con todas las notas</a><a href="#r1">Ronda 1</a>{nav}<a href="#teclas">Teclas</a><a href="#limites">Límites</a><a href="#veredicto">Veredicto</a></nav>
<main>
<h1>Present (<code>R</code>): varias vistas para que se lea el contenido</h1>
{round2()}
<p class="box"><strong>Conclusión:</strong> el Gantt se queda como vista 1 y se añaden tres
vistas de contenido, cada una con su tecla. Recomiendo enviar primero <strong>D · split</strong>
(Gantt + nota completa: el paso más corto y el más seguro) y <strong>C · slide</strong> (la más
legible en una sala); <strong>B · cards</strong> es la mejor para «repasemos todo», pero a 80 columnas
corta casi todas las notas.</p>

<p>Todas las capturas salen del <strong>app real</strong>: <code>TaskboardApp</code> en headless con
<code>run_test</code>, teclas pulsadas con el piloto (<code>R</code>, <code>1</code>–<code>4</code>,
<code>⇥</code>, flechas, <code>␣</code>, <code>pgdn</code>) y cada marco es
<code>export_screenshot()</code> pasado a PNG con Edge headless. Solo se sustituye
<code>PresentScreen</code> por una subclase
(<code>prototypes/present_views/app_capture.py</code>); los renderers de prueba están en
<code>views_proto.py</code>. Tablero sintético propio (<code>fixture.py</code>): el tablero del
oráculo PRES-C con notas de 2 a 13 líneas, una muy larga («Launch new homepage») y una vacía
(«SEO redirects map»). Hoy = 30 sep 2026. La fila de abajo de cada captura es la fila de ayuda: no
forma parte del marco que ve la sala ni de lo que exporta <code>x</code>.</p>

<h2 id="teclas">Teclas y cambio de vista</h2>
<ul>
<li><kbd>1</kbd> gantt · <kbd>2</kbd> cards · <kbd>3</kbd> slide · <kbd>4</kbd> split — salto directo.
Es el mismo idioma del tablero, donde los dígitos ya eligen vista.</li>
<li><kbd>⇥</kbd> / <kbd>⇧⇥</kbd> recorre las vistas en círculo. En el tablero <kbd>⇥</kbd> ya es
«Layout»; dentro del modal el app suelta su <kbd>⇥</kbd> (<code>check_action</code>), así que no hay choque.</li>
<li>No uso <kbd>v</kbd>: en el tablero es «Archived», y repetir una letra con otro significado confunde.</li>
<li><kbd>pgdn</kbd> / <kbd>pgup</kbd> desplazan la nota en slide y split. Mover el cursor vuelve al inicio de la nota.</li>
<li>El cursor es <strong>uno solo</strong> para las cuatro vistas: cambiar de vista mantiene la tarea señalada.</li>
<li>Indicador: la vista actual aparece en la fila de ayuda (<code>1 gantt  <b>2 cards</b>  3 slide…</code>)
y, en el marco, solo una palabra gris junto al proyecto. Nada de menú en lo que ve la sala.</li>
<li><kbd>␣</kbd> oculta en <em>todas</em> las vistas (las cuatro leen <code>present_tasks</code>, que ya filtra
<code>show_in_present</code>); el conteo «1 hidden» sigue solo en la fila de ayuda.</li>
</ul>

{"".join(sections)}

<h2 id="limites">Límites de terminal encontrados</h2>
<ul>
<li><strong>Alto, no ancho, es el recurso escaso.</strong> A 80 × 25 hay 24 filas de marco: cards
reparte ~6 filas por tarjeta; slide y split necesitan <code>pgdn</code> para una nota de 13 líneas.</li>
<li><strong>No hay tipografía grande.</strong> El título de la lámina usa mayúsculas espaciadas; solo los
dígitos se dibujan grandes (fuente 4×7 en medios bloques, 4 filas). Un título dibujado en bloques no cabe:
22 letras × 5 celdas = 110 columnas.</li>
<li><strong>La escalera de fases mide 67 columnas</strong>: a 80 cabe junto a la figura solo porque la
figura mide 14; con 3 dígitos o fases con nombres largos cae a la forma compacta
<code>● ● ◉ ○ ○ DOING</code> (implementada).</li>
<li><strong>Los títulos del Gantt se cortan a 80</strong> (<code>Build component…</code>), igual que hoy; en
split la columna de datos repite el título completo de la tarea del cursor.</li>
<li><strong>Medios bloques en la exportación:</strong> los dígitos se ven como matriz de puntos en el PNG de Edge
(pequeñas costuras entre celdas). En una terminal real se ven sólidos o casi.</li>
<li><strong>El app reveló</strong> que <code>Widget._render</code> es un nombre reservado de Textual (la subclase
lo pisaba y el app caía); y que la nota actual de la vista gantt pierde los saltos de línea.</li>
</ul>

<h2>Comparación</h2>
<table>
<tr><th></th><th>Tecla</th><th>Para qué</th><th>Notas visibles</th><th>Calendario</th><th>Nota larga</th><th>80 × 25</th><th>Código nuevo</th></tr>
<tr><td>A gantt</td><td>1</td><td>cronograma</td><td>1 tarea, 3 líneas, sin saltos</td><td>sí</td><td>cortada</td><td>bien</td><td>ninguno</td></tr>
<tr><td>B cards</td><td>2</td><td>repasar todo</td><td>todas, recortadas</td><td>no (texto)</td><td>cortada, declarada</td><td>apretado</td><td>medio (cuadrícula + reparto de alto)</td></tr>
<tr><td>C slide</td><td>3</td><td>presentar tarea por tarea</td><td>1 tarea, completa</td><td>no (días dibujados)</td><td>completa a 118; <code>pgdn</code> a 80</td><td>bien</td><td>medio (figura, tira, scroll)</td></tr>
<tr><td>D split</td><td>4</td><td>cronograma + leer</td><td>1 tarea, completa</td><td>sí</td><td>completa a 118; <code>pgdn</code> a 80</td><td>bien</td><td>bajo (reusa filas del Gantt)</td></tr>
</table>

<h2 id="veredicto">Recomendación y veredicto que necesito</h2>
<ul>
<li><strong>Recomiendo D primero</strong>: resuelve el pedido («que se vea el contenido») sin perder el
Gantt, con el menor código nuevo. <strong>C después</strong>, como la vista de exposición.
<strong>B</strong> la dejaría para un tercer incremento, o la descartaría si las juntas casi siempre
recorren tarea por tarea.</li>
<li><strong>Teclas:</strong> <kbd>1</kbd>–<kbd>4</kbd> + <kbd>⇥</kbd>. ¿Te sirven, o prefieres solo <kbd>⇥</kbd>?</li>
<li><strong>¿La vista elegida persiste?</strong> Hoy el prototipo abre siempre en gantt. Opción: recordar
la última vista en los <code>settings</code> del tablero (sería una segunda escritura de Present).</li>
<li><strong>Arreglar la nota en A:</strong> ¿respeto los saltos de línea en la vista gantt actual (cambia
el oráculo PRES-R) o la dejo como está?</li>
<li><strong>¿Tareas terminadas?</strong> Todas las vistas muestran solo tareas abiertas, como el Gantt. ¿Quieres
que cards o slide incluyan las terminadas al final?</li>
<li><strong>Imágenes:</strong> se muestran como conteo y nombre de archivo; dibujarlas en la terminal no
entra en esta ronda.</li>
</ul>
</main></body></html>
"""
    PAGE.write_text(html, encoding="utf-8")
    print(PAGE, f"{PAGE.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

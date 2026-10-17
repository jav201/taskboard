"""Build the verdict page from the captured SVGs.

    python prototypes/present_rulers/build_html.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "present-rulers-prototype.html"

VARIANTS = [
    ("S", "Shipped — the defect",
     "Lo que hay hoy en <code>R</code>. El campo tiene la línea de hoy <code>╎</code> y las guías "
     "semanales <code>┆</code>, pero ninguna fila dice qué fecha es cada columna. Quien ve la "
     "presentación solo puede leer las fechas en los chips de la derecha, nunca en las barras."),
    ("A", "Two-row ruler (the gantt's own)",
     "Se traslada tal cual la regla de dos filas de la vista Gantt (<code>3</code>): la banda de "
     "meses con <code>┃</code> en el día 1 y el <code>◆</code> de entrega del proyecto, y debajo la fila de "
     "ticks (lunes a esta escala) que cae exactamente sobre cada guía <code>┆</code>. Columna de "
     "etiqueta: hoy y la escala. Cuesta 2 filas arriba. Única diferencia con el Gantt: hoy va en "
     "<em>bright</em>, no en acento, porque en Present el acento es solo del cursor."),
    ("B", "Cursor ruler (A + echo)",
     "Igual que A, pero la fila de ticks repite las fechas exactas de la tarea bajo el cursor "
     "(<code>Sep 24 ⟦━━━⟧ Sep 28</code>) en el color del cursor. Al mover el cursor con "
     "<code>←→</code>, la regla lo sigue: el presentador señala una tarea y la audiencia lee sus fechas "
     "sobre el calendario. La segunda captura muestra el cursor movido a otra tarea."),
    ("C", "X-axis below (chart style)",
     "Una sola fila, <em>debajo</em> de las barras, como el eje X de una gráfica proyectada. Cada guía "
     "lleva su fecha completa (<code>╵Sep 21</code>), legible a distancia sin combinar fila de mes + "
     "número. Hoy se marca <code>╎today</code> y gana cualquier choque (por eso <code>Sep 28</code> "
     "pierde su texto). Cuesta 1 fila; sin banda de meses ni <code>◆</code> en la regla."),
]


def svg(name: str) -> str:
    s = (OUT / name).read_text(encoding="utf-8")
    return s[s.index("<svg"):]


def main() -> None:
    sections = []
    for key, title, prose in VARIANTS:
        figs = [f'<figure><figcaption>118 × 30</figcaption>{svg(f"present-{key}-118x30.svg")}</figure>']
        if key == "B":
            figs.append('<figure><figcaption>118 × 30 · cursor moved to “Launch new homepage”'
                        f'</figcaption>{svg("present-B2-118x30.svg")}</figure>')
        figs.append(f'<figure class="narrow"><figcaption>80 × 24</figcaption>'
                    f'{svg(f"present-{key}-80x24.svg")}</figure>')
        sections.append(f'<section id="v-{key}"><h2><span class="tag">{key}</span> {title}</h2>'
                        f'<p>{prose}</p>{"".join(figs)}</section>')
    nav = "".join(f'<a href="#v-{k}">{k} · {t.split(" (")[0].split(" —")[0]}</a>'
                  for k, t, _ in VARIANTS)
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Present · date rulers</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#7aa2f7; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.6rem 1rem; display:flex; gap:1rem; flex-wrap:wrap; font-size:.9rem; }}
nav a {{ color:var(--acc); text-decoration:none; }}
main {{ max-width:1400px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .3rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
.tag {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px;
  padding:0 .5rem; font-family:ui-monospace,Consolas,monospace; }}
p, li {{ max-width:75ch; }}
code {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em;
  border-radius:3px; }}
figure {{ margin:1rem 0; }}
figure svg {{ width:100%; height:auto; display:block; }}
figure.narrow svg {{ max-width:70%; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
table {{ border-collapse:collapse; margin:1rem 0; font-size:.92rem; }}
th, td {{ border:1px solid var(--line); padding:.35rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--mut); font-weight:600; }}
.box {{ border-left:3px solid var(--acc); padding:.4rem 1rem; background:#101722; }}
@media (max-width:700px) {{ figure.narrow svg {{ max-width:100%; }} }}
</style></head><body>
<nav><strong>Present · date rulers</strong><a href="#r2">R2 · from the app</a>{nav}<a href="#leyenda">? legend</a><a href="#veredicto">Veredicto</a></nav>
<main>
<h1>Present (<code>R</code>): el Gantt perdió sus reglas de fechas</h1>
<p class="box"><strong>Conclusión:</strong> el campo Gantt del modo presentación no tiene ninguna
fila con fechas; el oráculo PRES-C se aprobó así y los tests lo fijan byte a byte. Abajo están 3
variantes que la devuelven, renderizadas con el renderer real (<code>render_present</code> y los
helpers del Gantt) sobre el tablero del oráculo PRES-C, hoy = 30 sep 2026. Mi recomendación es
<strong>B</strong>.</p>

<h2 id="r2"><span class="tag">R2</span> Round 2 — B + start–end + hide flag, captured from the app</h2>
<p><strong>Capturas directas del app:</strong> <code>TaskboardApp</code> corriendo headless; se oprime
<code>R</code>, <code>→</code>, <code>space</code> y <code>a</code> con el piloto de Textual, y cada imagen es el
<code>export_screenshot()</code> del propio app (compositor real, fila de ayuda real). Solo se
parchean <code>render_present</code> y <code>PresentScreen</code>
(<code>prototypes/present_rulers/app_capture.py</code>).</p>
<ul>
<li><strong>Ambas fechas en cada fila:</strong> el chip dice <code>Sep 24–28</code> /
<code>Aug 21–Oct 10</code>; si la tarea no tiene inicio, <code>due Oct 14</code> (su barra arranca
en una fecha inferida, y el chip no la inventa). Los días relativos (<code>▲2d</code>,
<code>in 10d</code>) se quedan en el brief de abajo.</li>
<li><strong>Bandera de presentación:</strong> <code>space</code> oculta la tarea del cursor del
diagrama y del brief; <code>a</code> las vuelve a mostrar todas. Por default todas se muestran. El eje de
fechas se reajusta a lo visible. El conteo «1 hidden» va en la fila de ayuda, <em>no</em> en el
marco: el marco es lo que ve la sala y lo que exporta <code>x</code>.</li>
<li><strong>Lo que el app reveló y los mocks no:</strong> el chip del proyecto se cortaba a 80
columnas (<code>Aug 21–Oct …</code>), la ayuda perdía <code>esc leave</code>, y el «hidden» en
el encabezado se habría exportado. Los tres ya están corregidos en estas capturas.</li>
</ul>
<figure><figcaption>118 × 31 · 1 · R opened, cursor on “Fix checkout 500 error”</figcaption>{svg("app-118-1-open.svg")}</figure>
<figure><figcaption>118 × 31 · 2 · → → cursor on “Launch new homepage”: the ruler follows</figcaption>{svg("app-118-2-cursor-moved.svg")}</figure>
<figure><figcaption>118 × 31 · 3 · ← space: “Optimize image assets” left out (hint says 1 hidden)</figcaption>{svg("app-118-3-hidden.svg")}</figure>
<figure><figcaption>118 × 31 · 4 · a: all shown again</figcaption>{svg("app-118-4-show-all.svg")}</figure>
<figure class="narrow"><figcaption>80 × 25 · open</figcaption>{svg("app-80-1-open.svg")}</figure>
<figure class="narrow"><figcaption>80 × 25 · one task hidden</figcaption>{svg("app-80-3-hidden.svg")}</figure>
<h2>Round 1 — the three ruler variants (renderer-level)</h2>
<table>
<tr><th></th><th>Filas</th><th>Meses</th><th>Ticks</th><th>◆ entrega</th><th>Sigue al cursor</th><th>Reusa código</th></tr>
<tr><td>A</td><td>+2 arriba</td><td>sí</td><td>número de día</td><td>sí</td><td>no</td><td>100 % (<code>gantt_month_row</code>, <code>gantt_day_row</code>)</td></tr>
<tr><td>B</td><td>+2 arriba</td><td>sí</td><td>número de día + fechas exactas del cursor</td><td>sí</td><td>sí</td><td>100 % + <code>gantt_echo</code></td></tr>
<tr><td>C</td><td>+1 abajo</td><td>dentro de cada fecha</td><td>fecha completa por guía</td><td>no</td><td>no</td><td>fila nueva</td></tr>
</table>

{"".join(sections)}

<h2 id="leyenda"><span class="tag">?</span> Legend: the keys the bar never draws</h2>
<p>El modal <code>?</code> arma su lista Keys con <code>bar_keys()</code>, que descarta toda tecla
<code>bar=False</code>; por eso <code>R</code> Present y <code>S</code> Standup no aparecen. Hallazgo
del prototipo: esa lista ya es más alta que la caja y se corta en <code>6 Chains</code>, así que agregar
las teclas <em>al final</em> las volvería a esconder. La propuesta pone un bloque <strong>Global</strong>
en la columna izquierda, bajo Usage, donde sobra espacio. Capturado del app real (vista gantt, 118×40).</p>
<figure><figcaption>shipped</figcaption>{svg("legend-shipped.svg")}</figure>
<figure><figcaption>proposed · Global block under Usage</figcaption>{svg("legend-proposed.svg")}</figure>

<h2 id="veredicto">Veredicto que necesito</h2>
<ul>
<li><strong>R2 · ¿la bandera persiste?</strong> Hoy Present es de solo lectura (nunca escribe el
tablero). Opción 1 (recomendada): se guarda en la tarea (<code>board.json</code>) y también se puede editar desde el
editor de tareas, para preparar la junta antes. Opción 2: solo dura la sesión de presentación y se pierde al salir.</li>
<li><strong>R2 · ¿una sola bandera o por junta?</strong> Una bandera por tarea es lo simple. Si alternas
juntas con públicos distintos, harían falta «perfiles», que es más grande y no está prototipado.</li>
<li><strong>Recomiendo B.</strong> Es la regla que ya conoces de la vista Gantt (cero vocabulario
nuevo) y, en presentación, añade lo que importa: la tarea que señalas muestra sus fechas en el
calendario. Se arma con helpers ya probados; el riesgo es bajo.</li>
<li>C es más legible a distancia (fecha completa), pero inventa una segunda regla distinta de la
del Gantt y pierde la banda de meses y el <code>◆</code>.</li>
<li><strong>Leyenda <code>?</code>:</strong> ¿bloque Global en la columna izquierda (propuesto),
o prefieres otra ubicación? Aparte: la lista Keys de la derecha ya se corta; ¿lo atiendo en el mismo
batch o lo dejo en backlog?</li>
<li>Cualquier opción cambia los marcos del oráculo PRES-C (<code>TC-1001/1002</code>): se
re-capturan como oráculo nuevo con tu veredicto, en el mismo batch de dev-flow.</li>
<li>Presupuesto de color: hoy pasa de acento a <em>bright</em> en la regla, para que el acento siga
siendo solo del cursor (regla C-2b del PRES-C). Si prefieres hoy en acento como en el Gantt, dilo.</li>
</ul>
<p style="color:var(--mut)">Fuente: <code>prototypes/present_rulers/proto.py</code> ·
capturas SVG headless (rich <code>export_svg</code>), sin edición manual.</p>
</main></body></html>
"""
    PAGE.write_text(html, encoding="utf-8")
    print("wrote", PAGE, len(html) // 1024, "KB")


if __name__ == "__main__":
    main()

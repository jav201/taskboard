"""Build the verdict page from the app captures (SVGs embedded as base64, so
the page works opened alone).

    python prototypes/present_portfolio/app_capture.py
    python prototypes/present_portfolio/build_html.py
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "present-portfolio-prototype.html"
USED: set[str] = set()


def img(name: str, cap: str) -> str:
    USED.add(name)
    data = base64.b64encode((OUT / f"{name}.svg").read_bytes()).decode()
    return (f'<figure><figcaption>{cap}</figcaption>'
            f'<img alt="{cap}" loading="lazy" src="data:image/svg+xml;base64,{data}"></figure>')


VARIANTS = {
    "A": ("Apilada", "Cada proyecto visible: una fila de cabecera (color, nombre, barra del "
          "proyecto, abiertas, ▲ atrasadas, cuenta regresiva) y debajo sus tareas visibles. Una "
          "sola regla de fechas. Si no caben las filas, los proyectos más lejos del cursor se "
          "pliegan a su cabecera.",
          "Ganas: todos los timelines y todas las tareas relevantes en un solo marco; a 160 × 45 "
          "cabe el portafolio entero sin plegar.",
          "Cedes: a 80 × 24 dos proyectos quedan plegados; para traer de vuelta UN proyecto oculto "
          "hay que usar <kbd>a</kbd> (muestra todo)."),
    "B": ("Resumen + foco", "Cada proyecto visible es UNA fila: su barra con los vencimientos de "
          "sus tareas como marcas (<code>▪</code> tarea, <code>◆</code> hito, rojo si va tarde), "
          "progreso <code>●</code> y fechas. Solo los proyectos que despliegas con "
          "<kbd>enter</kbd> muestran sus tareas.",
          "Ganas: la vista de portafolio más limpia; se lee igual a 80 que a 160 y deja aire para "
          "desplegar lo que vas a contar.",
          "Cedes: las marcas no dicen qué tarea es cuál; a 160 × 45 dos tercios del marco quedan "
          "vacíos hasta que despliegas."),
    "C": ("Carril de curaduría", "Un carril a la izquierda lista todos los proyectos en orden "
          "(<code>●</code> visible, <code>○</code> oculto, número de posición); a la derecha el "
          "timeline de A. Ocultar y reordenar se hacen en el carril; <kbd>x</kbd> exporta solo el "
          "timeline.",
          "Ganas: ves y recuperas cada proyecto oculto por separado (<kbd>␣</kbd> alterna "
          "● / ○); el orden se ve como lista numerada.",
          "Cedes: 19–25 columnas del ancho; a 80 los nombres del carril y el campo de fechas "
          "quedan muy cortos; dos focos (carril / timeline) con <kbd>←→</kbd>."),
}

SIZES = [("160", "160 × 45 · tamaño principal"), ("118", "118 × 30"), ("80", "80 × 24")]

SEQ = [("1-cursor-header", "1 · cursor en la cabecera de «Brand Refresh»"),
       ("2-hidden", "2 · <kbd>␣</kbd>: el proyecto sale del marco; la fila de ayuda cuenta «2 projects + 2 tasks hidden»"),
       ("3-moved-top", "3 · cursor en «Mobile Release 3.2», <kbd>shift ↑</kbd> ×2: sube al primer lugar"),
       ("4-show-all", "4 · <kbd>a</kbd>: vuelven los proyectos y tareas ocultos; el orden nuevo se queda")]
EXTRA = {"A": ("5-folded", "5 · <kbd>enter</kbd> en «Customer Portal»: se pliega a su cabecera"),
         "B": ("5-unfolded", "5 · <kbd>enter</kbd> en «Billing Migration»: se despliega con sus tareas"),
         "C": None}


def main() -> None:
    ev = json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))
    grid = []
    for size, cap in SIZES:
        cells = "".join(
            f'<div class="cell"><h4><span class="tag">{v}</span> {VARIANTS[v][0]}</h4>'
            + img(f"{v}-{size}-initial", f"{v} · {cap}") + "</div>" for v in "ABC")
        grid.append(f'<h3 class="v">{cap}</h3><div class="tri">{cells}</div>')
    cards = "".join(
        f'<div class="card"><h3><span class="tag">{v}</span> {n}</h3><p>{d}</p>'
        f'<p class="gain">{g}</p><p class="give">{x}</p></div>'
        for v, (n, d, g, x) in VARIANTS.items())
    seqs = []
    for v in "ABC":
        shots = [img(f"{v}-160-seq-{k}", f"{v} · {c}") for k, c in SEQ]
        if EXTRA[v]:
            shots.append(img(f"{v}-160-seq-{EXTRA[v][0]}", f"{v} · {EXTRA[v][1]}"))
        if v == "C":
            shots.append(img("C-160-timeline", "C · <kbd>→</kbd> pasa el foco al timeline, "
                             "<kbd>↓</kbd> recorre tareas como en A"))
        seqs.append(f'<h3 class="v"><span class="tag">{v}</span> {VARIANTS[v][0]}</h3>'
                    f'<div class="two">{"".join(shots)}</div>')
    ev_rows = "".join(
        f"<tr><td>{name}</td><td>{d.get('present_rank', '—')}</td>"
        f"<td>{d.get('show_in_present', '(sin clave = visible)')}</td></tr>"
        for name, d in ev["A"].items())

    objections = "".join(
        f'<div class="obj"><label><input type="checkbox" data-k="obj-{v}"> Objeto a '
        f'<strong>{v} · {VARIANTS[v][0]}</strong></label>'
        f'<textarea data-k="txt-{v}" placeholder="Qué no te convence de {v} (opcional)"></textarea></div>'
        for v in "ABC")

    body = f"""
<h1>Present (<code>R</code>) · vista 3: todos los proyectos en un solo timeline</h1>

<div class="box"><strong>Conclusión.</strong> Recomiendo <strong>A · Apilada</strong> como vista 3,
con dos préstamos baratos: la cabecera <em>plegada</em> dibuja las marcas de B (así un proyecto
plegado sigue diciendo cuándo vencen sus tareas), y el orden y lo oculto se guardan
<strong>solo para la presentación</strong> (<code>Project.present_rank</code> y
<code>Project.show_in_present</code>): el tablero, el Gantt, los carriles y el kanban no se mueven.
C es la mejor para <em>curar</em> antes de la junta, pero cuesta ancho; si la quieres, propongo que el
carril sea un modo que se abre y se cierra, no una columna fija.</div>

<h2 id="pedido">Lo que pediste</h2>
<blockquote>«la parte de presentación es muy útil, pero también el gantt con todos los proyectos.
Necesito que en el modo presentación pueda tener la vista del gantt con todos los proyectos. Y tener
la opción de esconder tareas o proyectos. De modo que pueda ver los proyectos de interés enfocándome
en las tareas más relevantes y ver todos los timelines juntos, así también reordenar los proyectos en
el orden que mejor me convenga.»</blockquote>
<p>Traducido a pantalla: una vista 3 dentro de <code>R</code> (después de <kbd>1</kbd> gantt y
<kbd>2</kbd> split) con todos los proyectos sobre <strong>una sola regla de fechas</strong>; ocultar
tareas <em>o proyectos enteros</em>; reordenar proyectos; y que lo que ve la sala siga siendo solo el
marco (las teclas viven en la fila de ayuda, abajo).</p>

<h2 id="variantes">Las tres variantes</h2>
<div class="cards">{cards}</div>
<p class="note">Común a las tres: la ventana de fechas se ajusta al trabajo abierto de los proyectos
<em>visibles</em> (ocultar uno puede acortar la ventana); hoy en la etiqueta del mes; la fila de días
repite las fechas exactas de lo que tiene el cursor — de una tarea con la regla actual
(<code>selected task ▸</code>) y, en una cabecera, el lapso del proyecto (<code>project span ▸</code>,
texto nuevo); chips inicio–fin a la derecha; ▲ atrasadas en rojo. Tablero sintético: 6 proyectos, uno
ya oculto (Security Audit), uno sin fechas (Brand Refresh), dos tareas ocultas; hoy = lun 19 oct 2026.
Haz clic en cualquier captura para verla en grande.</p>
{"".join(grid)}

<h2 id="secuencia">Ocultar y reordenar (160 × 45)</h2>
<p>Teclas reales pulsadas con el piloto, en el mismo orden en las tres variantes. <kbd>␣</kbd> en una
tarea la oculta (la marca de tarea que ya existe); en una cabecera oculta el proyecto entero.
<kbd>shift ↑/↓</kbd> mueve el proyecto del cursor entre los visibles (en C, en el carril, entre todos).
<kbd>a</kbd> muestra todo otra vez. <kbd>⇥</kbd> recorre 1 → 2 → 3; el cursor es uno solo: al volver a
la vista 1 se presenta el proyecto de la tarea del cursor.</p>
{"".join(seqs)}
<h3 class="v">El cursor compartido entre vistas</h3>
<div class="two">{img("A-160-tab-to-view1", "Desde la vista 3 con el cursor en «Tax rules for new regions», <kbd>⇥</kbd> vuelve a la vista 1 de «Billing Migration» con la misma tarea señalada")}</div>

<h2 id="persistencia">Persistencia: qué se guarda y qué cambia en el resto del app</h2>
<div class="box"><strong>Propuesta por defecto.</strong> Ocultar un proyecto se guarda como
<code>Project.show_in_present = false</code> (igual que la marca de tarea: la clave solo se escribe
cuando es <code>false</code>). Reordenar se guarda como <code>Project.present_rank</code>, un orden
<strong>solo de la presentación</strong>.<br><strong>Alternativa.</strong> Reordenar mueve el proyecto en
el orden único del tablero: cambian también los carriles, el Gantt y el kanban.</div>
<p>Lo que el tablero guardó al final de la secuencia de A (leído del JSON salvado; en el prototipo las
claves viven en <code>Project.extra</code>, que el cargador ya conserva y <code>save()</code> ya escribe):</p>
<table><tr><th>Proyecto</th><th>present_rank</th><th>show_in_present</th></tr>{ev_rows}</table>
<p>La consecuencia, en el Gantt del tablero (vista <kbd>3</kbd> del app, 160 × 45), después de subir
«Mobile Release 3.2» al primer lugar en la presentación:</p>
<div class="two">
{img("board-gantt-before", "Por defecto propuesto (<code>present_rank</code>): el Gantt del tablero queda EXACTAMENTE como antes — Customer Portal primero")}
{img("board-gantt-board-order", "Alternativa (orden del tablero): el Gantt del tablero también pone «Mobile Release 3.2» arriba, y lo mismo carriles y kanban")}
</div>
<p>Nota: el Gantt del tablero ignora lo oculto en la presentación (ahí siguen Security Audit,
«Help-center links» y «Cost dashboards»): ocultar es solo para la sala, con cualquiera de las dos opciones.</p>

<h2 id="bordes">Bordes</h2>
<div class="two">
{img("A-30-narrow", "Menos de 36 columnas: el mismo aviso de hoy («widen to 36+ columns»), cualquiera que sea la vista")}
{img("C-160-export", "C · lo que escribe <kbd>x</kbd>: el timeline sin el carril (el SVG que produce <code>save_present_svg</code>, el exportador real)")}
</div>

<h2 id="limites">Lo que esta ronda no representa fielmente</h2>
<ul>
<li><strong>Las claves nuevas no existen en el modelo.</strong> <code>show_in_present</code> y
<code>present_rank</code> de proyecto viven en <code>Project.extra</code>; el round-trip por
<code>save()</code> es real, pero no hay validación al cargar ni migración.</li>
<li><strong>Sin PNG.</strong> Solo SVG; el exportador real escribe también PNG con Edge y avisa con un
toast que <code>run_test</code> no pinta.</li>
<li><strong>Hitos.</strong> En la vista 3 un hito se dibuja como en el Gantt del tablero (<code>◆ Nov 6</code>).
La vista 1 actual lo dibuja como barra desde hoy hasta su fecha (ver «Cut-over weekend» en la captura del
cursor compartido): una incoherencia que ya existe y que esta ronda deja a la vista.</li>
<li><strong>Plegado automático de B</strong> (cuando despliegas más de lo que cabe) está programado pero
ninguna captura lo ejercita.</li>
</ul>

<h2 id="preguntas">Preguntas abiertas</h2>
<ol>
<li><strong>¿A, B o C?</strong> Recomiendo <strong>A</strong> con las marcas de B en las cabeceras
plegadas.</li>
<li><strong>¿Reordenar solo en la presentación o en todo el tablero?</strong> Recomiendo
<strong>solo en la presentación</strong> (<code>present_rank</code>): el orden de una junta no tiene por
qué ser el orden de trabajo, y el tablero no cambia a tus espaldas.</li>
<li><strong>En A/B, ¿cómo traes de vuelta UN proyecto oculto?</strong> Hoy solo con <kbd>a</kbd> (todo).
Recomiendo una tecla nueva, <kbd>u</kbd> (libre en Present), que abre
una lista corta de lo oculto para elegir qué vuelve; el conteo sigue en la fila de ayuda — sin carril fijo.</li>
</ol>

<h2 id="objeciones">Tus objeciones</h2>
<p>Marca solo lo que objetas; lo que no marques lo tomo como aceptado.</p>
{objections}
<div class="obj"><label><input type="checkbox" data-k="obj-persist"> Objeto a la persistencia propuesta
(<code>present_rank</code> solo de presentación)</label>
<textarea data-k="txt-persist" placeholder="¿Prefieres que reordenar cambie el tablero?"></textarea></div>
<div class="obj"><label>Respuesta a la pregunta 3 u otras notas</label>
<textarea data-k="txt-notes" placeholder="Notas libres"></textarea></div>
<button id="export">Exportar respuestas</button> <span id="done"></span>
"""
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Present · all projects</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.6rem 16px; display:flex; gap:1rem; flex-wrap:wrap; font-size:.9rem; }}
nav a {{ color:var(--acc); text-decoration:none; }}
main {{ max-width:1500px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .6rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
h3 {{ font-size:1.05rem; margin:.4rem 0; }}
h3.v {{ font-size:1.2rem; margin-top:1.8rem; }}
h4 {{ margin:.2rem 0; font-size:.95rem; }}
.tag {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px;
  padding:0 .45rem; font-family:ui-monospace,Consolas,monospace; }}
p, li, blockquote {{ max-width:85ch; }}
blockquote {{ border-left:3px solid var(--line); margin:0; padding:.2rem 1rem; color:var(--mut); font-style:italic; }}
code, kbd {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:95ch; }}
.note {{ color:var(--mut); font-size:.92rem; }}
.cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.6rem 1rem; }}
.card p {{ margin:.4rem 0; font-size:.94rem; }}
.gain::before {{ content:"+ "; color:var(--acc); font-weight:700; }}
.give::before {{ content:"− "; color:#f43f5e; font-weight:700; }}
.tri {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; align-items:start; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; align-items:start; }}
figure {{ margin:.6rem 0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; cursor:zoom-in; background:#0d1117; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
table {{ border-collapse:collapse; margin:1rem 0; font-size:.92rem; }}
th, td {{ border:1px solid var(--line); padding:.3rem .6rem; text-align:left; }}
th {{ color:var(--mut); }}
.obj {{ margin:.8rem 0; max-width:85ch; }}
.obj textarea {{ display:block; width:100%; min-height:3.5rem; margin-top:.3rem; background:var(--panel);
  color:var(--fg); border:1px solid var(--line); border-radius:6px; font:inherit; padding:.4rem; box-sizing:border-box; }}
button {{ background:var(--acc); color:#0b0f14; border:0; border-radius:6px; padding:.5rem 1rem; font:inherit; font-weight:600; cursor:pointer; }}
#zoom {{ position:fixed; inset:0; background:#000d; display:none; z-index:9; overflow:auto; cursor:zoom-out; }}
#zoom img {{ display:block; margin:1rem auto; max-width:none; width:min(1900px,180vw); }}
@media (max-width:900px) {{ .tri, .two, .cards {{ grid-template-columns:1fr; }} }}
</style></head><body>
<nav><strong>Present · all projects</strong><a href="#pedido">Pedido</a><a href="#variantes">Variantes</a>
<a href="#secuencia">Ocultar / reordenar</a><a href="#persistencia">Persistencia</a><a href="#bordes">Bordes</a>
<a href="#limites">Límites</a><a href="#preguntas">Preguntas</a><a href="#objeciones">Objeciones</a></nav>
<main>{body}</main>
<div id="zoom"><img alt=""></div>
<script>
const z = document.getElementById('zoom'), zi = z.querySelector('img');
document.querySelectorAll('figure img').forEach(i => i.onclick = () => {{ zi.src = i.src; z.style.display = 'block'; }});
z.onclick = () => {{ z.style.display = 'none'; }};
document.getElementById('export').onclick = async () => {{
  const out = ['Present · all projects — respuestas'];
  document.querySelectorAll('[data-k]').forEach(el => {{
    if (el.type === 'checkbox') {{ if (el.checked) out.push('OBJETO: ' + el.dataset.k.replace('obj-', '')); }}
    else if (el.value.trim()) out.push(el.dataset.k.replace('txt-', '') + ': ' + el.value.trim());
  }});
  if (out.length === 1) out.push('Sin objeciones: acepto la recomendación.');
  const txt = out.join('\\n');
  try {{ await navigator.clipboard.writeText(txt); document.getElementById('done').textContent = 'Copiado.'; }}
  catch (e) {{ window.prompt('Copia el texto:', txt); }}
}};
</script>
</body></html>
"""
    PAGE.write_text(html, encoding="utf-8")
    produced = {p.stem for p in OUT.glob("*.svg")}
    print(PAGE, f"{PAGE.stat().st_size // 1024} KB", "embedded", len(USED), "of", len(produced),
          "missing:", sorted(produced - USED))


if __name__ == "__main__":
    main()

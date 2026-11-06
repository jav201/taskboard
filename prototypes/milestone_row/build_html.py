"""THROWAWAY — build the verdict page of the milestone-row round from its captures.

    powershell -File prototypes/milestone_row/shoot.ps1      (real Windows Terminal PNGs)
    python prototypes/milestone_row/build_html.py

Every image is embedded (base64), so the page works opened alone. A missing
capture is printed on the page as missing — never replaced by an SVG. The CSS
and the export script follow `prototypes/milestone_marks/build_html.py`.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "milestone-row.html"
SIZES = ("118x30", "80x24")
MISSING: list[str] = []
FIGN = [0]


def shot(scene: str) -> str:
    out = []
    for s in SIZES:
        p = OUT / "png" / f"{scene}_{s}.png"
        if not p.exists():
            MISSING.append(p.name)
            out.append(f'<div class="miss sz sz-{s}">captura faltante: {scene} · {s}</div>')
        else:
            data = base64.b64encode(p.read_bytes()).decode()
            out.append(f'<img class="sz sz-{s}" alt="{scene} {s}" loading="lazy" '
                       f'src="data:image/png;base64,{data}">')
    return "".join(out)


def fig(scene: str, cap: str) -> str:
    FIGN[0] += 1
    return (f'<figure id="fig{FIGN[0]}"><figcaption><b>Fig. {FIGN[0]}</b> · {cap}</figcaption>'
            f'{shot(scene)}</figure>')


# rows under the ruler on the synthetic board (prototypes/milestone_row/proto.py check)
ROWS = {"hoy": 23, "A": 18, "B": 14, "C": 15}

VARIANTS = [
    ("A", "A · Una fila de hitos por proyecto, bajo su barra", "A", [
        ("A-rest", "Cursor en una tarea: cada fila muestra sus marcas y la fecha donde cabe; tarde = <code>▲1d</code>, alcanzado = hueco + <code>✓</code>"),
        ("A-sel", "<kbd>↑</kbd> desde la primera tarea: el cursor entra en la fila sobre el próximo hito (<em>Steering go/no-go</em>, choque <code>■2</code>, <code>1/2</code>)"),
        ("A-late", "<kbd>←</kbd>: el hito tarde (<em>Rubric sign-off</em>), chip <code>▲1d</code>"),
        ("A-enter", "<kbd>→</kbd> recorre el choque (<code>2/2</code>, <em>Store list frozen</em>) y <kbd>↵</kbd> abre sus detalles"),
     ],
     "Cada proyecto conserva su barra intacta y gana una sola fila debajo con todos sus hitos. "
     "El seleccionado muestra el título completo en la columna de etiqueta y, si cabe, junto a su marca; "
     "los demás su fecha, o <code>▲Nd</code> si van tarde, solo donde cabe entera. Un choque del mismo día "
     "se dibuja <code>■2</code> y <kbd>←→</kbd> entra en él (<code>1/2</code>, <code>2/2</code>). "
     "<kbd>↑↓</kbd> se detiene una vez por proyecto. Ahorra 5 filas aquí (23 → 18), y a 80×24 ya no se pliega "
     "ningún proyecto (hoy se pliegan dos)."),
    ("B", "B · Los hitos sobre la barra del proyecto", "", [
        ("B-rest", "Cero filas extra: las marcas pisan la barra <code>─</code>; sin fechas para no romperla"),
        ("B-sel", "<kbd>↑</kbd>: la barra misma es la fila; la etiqueta cambia el nombre del proyecto por el hito"),
        ("B-late", "<kbd>←</kbd>: el hito tarde; el <code>▲1d</code> solo está en el chip"),
        ("B-enter", "<kbd>→</kbd> <kbd>↵</kbd>: detalles del segundo hito del choque"),
     ],
     "Es la que más ahorra (23 → 14), pero la barra del proyecto deja de leerse sola: las marcas la cortan, "
     "no queda sitio para fechas ni para el título en el campo, y cuando un hito cae en la fecha comprometida "
     "del proyecto su marca tapa el <code>◆</code> del proyecto (Docs &amp; handover, Nov 4: el rombo verde pasa "
     "a gris). Con un hito seleccionado la etiqueta pierde el nombre del proyecto (queda en la regla). "
     "El cursor se detiene en la barra, que hoy no es seleccionable."),
    ("C", "C · Un solo carril de hitos para todo el gantt", "", [
        ("C-rest", "Un carril bajo la regla con los 9 hitos del tablero, en el color de su clase"),
        ("C-sel", "<kbd>↑</kbd> desde la primera tarea de Pilot rollout sube al carril: el próximo hito del tablero (<em>Golden set frozen</em>, de otro proyecto)"),
        ("C-late", "<kbd>←</kbd>: el hito tarde"),
        ("C-enter", "<kbd>→</kbd> <kbd>↵</kbd>: detalles"),
     ],
     "Una vista panorámica: ahorra 8 filas (23 → 15) y deja ver todas las fechas del tablero de un vistazo. "
     "Pero la marca ya no dice de qué proyecto es (el color es de la clase), las marcas de proyectos distintos "
     "se amontonan y chocan (a 80×24 casi no caben fechas), y para llegar a un hito de un proyecto de abajo "
     "hay que subir hasta arriba. <kbd>←→</kbd> recorre hitos de todos los proyectos mezclados."),
]

DECISIONS = [
    ("d1", "D1 · ¿La presentación (<kbd>R</kbd>) sigue al gantt del tablero?", "no", [
        ("no", "No: la presentación queda como hoy",
         ["Es lo que hace el prototipo: el cambio solo toca el gantt del tablero (el mismo corte que ya usa <code>done_rows</code>).",
          "La presentación sigue nombrando cada hito en su fila, que es lo que lee un cliente; su exportación no cambia.",
          "Dos formas de ver hitos: en el tablero compactos, en <kbd>R</kbd> uno por fila."]),
        ("si", "Sí: también una fila por proyecto",
         ["Una sola forma de leer hitos en todo el app.",
          "La presentación pierde los títulos de los hitos no seleccionados (allí no hay cursor que los revele), y su exportación también.",
          "Más trabajo: la presentación tiene su propio ciclo de cursor y su propia regla."]),
    ], "No. La presentación se enseña a otros: ahí un título por hito vale más que la fila ahorrada."),
    ("d2", "D2 · ¿A dónde va un hito sin proyecto (Inbox)?", "fila", [
        ("fila", "A la fila de hitos del grupo Inbox",
         ["El Inbox ya es un grupo del gantt; recibe su fila igual que un proyecto (Fig. 3, <em>Insurance renewal</em>).",
          "Una sola regla, nada nuevo que aprender.",
          "Con un solo hito no ahorra nada, pero tampoco cuesta."]),
        ("carril", "A un carril propio arriba del gantt (como C)",
         ["Lo separa de las tareas del Inbox.",
          "Mezcla dos modelos: A para proyectos, C para el Inbox."]),
        ("filas", "Se queda con una fila por hito",
         ["Nada cambia en el Inbox.",
          "Dos reglas: el mismo hito se dibuja distinto según tenga proyecto o no."]),
    ], "A la fila del grupo Inbox: misma regla que un proyecto."),
    ("d3", "D3 · ¿La búsqueda <kbd>/</kbd> y ocultar una clase siguen alcanzando hitos sueltos?", "si", [
        ("si", "Sí: la fila se arma con lo que el filtro deja",
         ["Es lo que hace el prototipo sin código extra: la fila se arma desde el tablero ya filtrado.",
          "<code>/store</code> deja en la fila solo <em>Store list frozen</em> y el cursor cae en él (Fig. 15).",
          "Una clase oculta saca sus marcas de la fila; si un proyecto se queda sin hitos visibles, su fila desaparece."]),
        ("entera", "La fila se queda entera y atenúa lo que no coincide",
         ["Se ve el contexto de fechas del proyecto.",
          "El cursor puede caer en un hito que no coincide, y ocultar una clase deja de ocultar.",
          "Requiere un estado atenuado nuevo en la fila."]),
    ], "Sí: el filtro decide qué marcas quedan, igual que hoy decide qué filas quedan."),
]

FINDINGS = [
    "<strong><kbd>←→</kbd> no hace nada en el gantt de hoy.</strong> Es <code>hmove(±1)</code>, que salta a la columna vecina "
    "del modelo de navegación; el gantt tiene <em>una sola</em> columna (<code>nav_model</code> devuelve sus filas en orden), así que "
    "<kbd>←→</kbd> no se mueve (Fig. 2: el cursor sigue en el mismo hito tras dos <kbd>→</kbd>). No mueve la ventana de tiempo. "
    "El prototipo le da <kbd>←→</kbd> a la fila de hitos: recorre sus hitos por fecha; fuera de la fila no cambia nada.",
    "<strong>Cómo se selecciona un hito:</strong> en el plan del gantt (el único sitio que leen el dibujo y la navegación) los hitos "
    "dejan de ser filas y uno solo los representa: el seleccionado, si no el próximo abierto. <kbd>↑↓</kbd> se detiene una vez en la "
    "fila; <kbd>↵</kbd> abre los detalles del hito en el cursor, como hoy.",
    "<strong>Filas bajo la regla en el tablero sintético</strong> (3 proyectos + Inbox, 9 hitos, 10 tareas): hoy 23 · A 18 · B 14 · C 15. "
    "A 80×24 caben 20: hoy se pliegan <em>Docs &amp; handover</em> e <em>Inbox</em>; con A, B o C se ve todo.",
    "<strong>Ancho:</strong> medí cada línea que el gantt entrega a la pantalla en las 30 capturas: ninguna pasa de 118 ni de 80 celdas, "
    "ninguna se parte. Solo se recorta (con <code>…</code>) el título del hito seleccionado dentro del campo; la etiqueta lo muestra completo hasta donde cabe.",
]

LIMITS = [
    "El prototipo envuelve <code>gantt_plan</code> y <code>_gantt_frame</code> desde <code>prototypes/milestone_row/proto.py</code>; nada de <code>taskboard/</code> cambia.",
    "Un hito alcanzado de un proyecto sin trabajo abierto no se dibuja hoy, y tampoco en la fila: no lo cambié.",
    "En B y C no probé el modo de enlace (<kbd>L</kbd>) ni el plegado paginado de un proyecto más alto que la pantalla.",
    "El marcador seleccionado usa vídeo inverso del color de la clase; con <code>◆</code> sin clase (gris) se ve menos.",
]


def opt_cards(name, opts, rec):
    out = []
    for val, title, cons in opts:
        li = "".join(f"<li>{x}</li>" for x in cons)
        r = val == rec
        out.append(f"<div class='opt{' rec' if r else ''}'><label><input type='radio' name='{name}' "
                   f"value='{val}'> <strong>{title}</strong>{' · recomendada' if r else ''}</label>"
                   f"<ul>{li}</ul></div>")
    return "".join(out)


def main() -> None:
    body = [f"""
<h1>Hitos en una sola fila del gantt</h1>
<div class="box bluf"><p><strong>En corto:</strong> recomiendo la <strong>variante A</strong>: una fila de hitos por proyecto, justo
bajo su barra. Ahorra 5 filas en el tablero de prueba (23 → 18) y a 80×24 deja de plegar proyectos; la barra del proyecto se sigue
leyendo sola y caben fechas. <kbd>↑↓</kbd> entra una vez en la fila y <kbd>←→</kbd> recorre sus hitos (hoy <kbd>←→</kbd> no hace nada
en el gantt). B ahorra más (→ 14) pero tapa la barra y el <code>◆</code> del proyecto; C (→ 15) mezcla proyectos en un carril.
Para las decisiones: <strong>D1 no</strong> (la presentación queda igual), <strong>D2 a la fila del Inbox</strong>,
<strong>D3 sí</strong> (el filtro decide qué marcas quedan).</p>
<p>Todo con la app real, capturado en Windows Terminal a 118×30 y 80×24 (cambia el tamaño arriba). Marca <em>Elijo esta</em>,
objeta solo lo que no te convenza y pulsa <strong>Exportar respuestas</strong> al final.</p></div>
<blockquote class="ask">«Necesito un cambio más, los milestones ocupan cada uno una línea en el gantt... esto gasta mucho espacio.
Necesito que queden en una sola línea en el gantt.»</blockquote>
<section id="hallazgos"><h2>Lo que encontré</h2><ul>{"".join(f"<li>{x}</li>" for x in FINDINGS)}</ul>
<table><tr><th></th><th>Hoy</th><th>A</th><th>B</th><th>C</th></tr>
<tr><td>Filas bajo la regla</td><td>{ROWS["hoy"]}</td><td class="rec">{ROWS["A"]} (−5)</td><td>{ROWS["B"]} (−9)</td><td>{ROWS["C"]} (−8)</td></tr>
<tr><td>Proyectos plegados a 80×24</td><td>2</td><td class="rec">0</td><td>0</td><td>0</td></tr></table></section>
<section id="hoy"><h2>Hoy</h2><p>Cada hito ocupa su fila: 9 de las 23 filas son hitos.</p>
<div class="grid g2">{fig("now", "La app de hoy, cursor en <em>Steering go/no-go</em>")}{fig("now-lr", "Hoy, tras <kbd>→</kbd> <kbd>→</kbd>: nada se mueve")}</div></section>"""]
    for key, title, rec, scenes, cons in VARIANTS:
        media = "".join(fig(s, c) for s, c in scenes)
        r = " rec" if rec else ""
        ahorro = ROWS["hoy"] - ROWS[key]
        body.append(f"""
<section id="v{key}" class="item{r}"><h2>{title}{" · recomendada" if rec else ""}</h2>
<p>{cons}</p><p class="saved">Filas: {ROWS["hoy"]} → {ROWS[key]} (ahorra {ahorro}).</p>
<div class="grid g2">{media}</div>
<label class="pick"><input type="radio" name="variant" value="{key}"> Elijo esta</label>
<div class="obj"><label>Objeción sobre {key} (opcional)</label>
<textarea data-note="v{key}" placeholder="Solo si objetas algo"></textarea></div></section>""")
    body.append(f"""
<section id="find"><h2>Búsqueda sobre la fila (D3)</h2>
<div class="grid g2">{fig("A-find", "Variante A, <kbd>/</kbd> <code>store</code> <kbd>↵</kbd>: la fila guarda solo el hito que coincide y el cursor cae en él")}</div></section>
<section id="decisiones"><h2>Decisiones (D1–D3)</h2><p>Vacío = la recomendada.</p>""")
    for name, title, rec, opts, rtext in DECISIONS:
        body.append(f"""<div class="dec" id="{name}"><h3>{title}</h3><div class="opts">{opt_cards(name, opts, rec)}</div>
<div class="box"><strong>Recomendación:</strong> {rtext}</div>
<div class="obj"><label><input type="checkbox" data-obj="{name}"> Objeto</label>
<textarea data-note="{name}" placeholder="Qué cambiarías"></textarea></div></div>""")
    body.append(f"""</section>
<section id="limites"><h2>Lo que esta ronda no representa</h2><ul>{"".join(f"<li>{x}</li>" for x in LIMITS)}</ul></section>
<section id="respuestas"><h2>Notas generales y exportar</h2>
<div class="obj"><label>Notas generales o peticiones nuevas</label>
<textarea data-note="general" placeholder="Cualquier cosa que no encaje arriba"></textarea></div>
<button id="export">Exportar respuestas</button> <span id="done"></span>
<pre id="preview" data-lang="text" hidden></pre></section>""")
    decs = json.dumps([(n, r) for n, _t, r, _o, _x in DECISIONS])
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Milestone row</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722; --red:#f43f5e; --pink:#f472b6; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.5rem 16px; display:flex; gap:.8rem; flex-wrap:wrap; align-items:center; font-size:.9rem; }}
nav a {{ color:var(--acc); text-decoration:none; }}
nav .sw {{ margin-left:auto; display:flex; gap:.3rem; align-items:center; }}
nav .sw button {{ background:var(--panel); color:var(--fg); border:1px solid var(--line); padding:.2rem .6rem; }}
nav .sw button.on {{ background:var(--acc); color:#0b0f14; }}
main {{ max-width:1600px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .6rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
.item.rec h2 {{ color:var(--acc); }}
h3 {{ margin:.2rem 0 .4rem; font-size:1.05rem; color:var(--acc); }}
p, li {{ max-width:100ch; }}
.saved {{ font-weight:600; }}
code, kbd {{ font-family:ui-monospace,"Cascadia Mono",Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:115ch; margin:1rem 0; }}
.ask {{ border-left:3px solid var(--pink); margin:1rem 0; padding:.4rem 1rem; color:var(--mut); max-width:110ch; font-style:italic; }}
.dec {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.7rem 1rem; margin:1rem 0; }}
.opts {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; }}
.opt {{ border:1px solid var(--line); border-radius:6px; padding:.5rem .7rem; background:#0d1219; }}
.opt.rec {{ border-color:var(--acc); }}
.opt ul {{ margin:.3rem 0 0; padding-left:1.1rem; font-size:.93rem; }}
.grid {{ display:grid; gap:1rem; align-items:start; }}
.g2 {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
figure {{ margin:0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; cursor:zoom-in; background:#0d1117; }}
figcaption {{ color:var(--mut); font-size:.88rem; margin-bottom:.3rem; }}
.miss {{ border:2px dashed var(--red); color:var(--red); padding:1rem; border-radius:6px; }}
body.s80 .sz-118x30, body.s118 .sz-80x24 {{ display:none; }}
table {{ border-collapse:collapse; margin:.8rem 0; font-size:.95rem; }}
th, td {{ border:1px solid var(--line); padding:.35rem .7rem; text-align:left; }}
th {{ color:var(--mut); }} td.rec {{ background:#0f1f22; color:var(--acc); font-weight:600; }}
.pick {{ display:inline-block; margin-top:.8rem; background:#0d1219; border:1px solid var(--acc); border-radius:6px; padding:.3rem .8rem; cursor:pointer; }}
.obj {{ margin:.8rem 0; max-width:95ch; }}
.obj textarea {{ display:block; width:100%; min-height:3rem; margin-top:.3rem; background:#0d1219; color:var(--fg);
  border:1px solid var(--line); border-radius:6px; font:inherit; padding:.4rem; box-sizing:border-box; }}
button {{ background:var(--acc); color:#0b0f14; border:0; border-radius:6px; padding:.5rem 1rem; font:inherit; font-weight:600; cursor:pointer; }}
pre {{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:.6rem .8rem; overflow-x:auto;
  white-space:pre-wrap; font:13px/1.45 ui-monospace,"Cascadia Mono",Consolas,monospace; max-width:115ch; }}
pre .k {{ color:#22d3ee; }} pre .s {{ color:#fbbf24; }}
#zoom {{ position:fixed; inset:0; background:#000d; display:none; z-index:9; overflow:auto; cursor:zoom-out; }}
#zoom img {{ display:block; margin:1rem auto; max-width:96vw; }}
@media (max-width:1000px) {{ .g2, .opts {{ grid-template-columns:1fr; }} }}
</style></head><body class="s118">
<nav><strong>Milestone row</strong><a href="#hallazgos">Hallazgos</a><a href="#hoy">Hoy</a><a href="#vA">A</a><a href="#vB">B</a><a href="#vC">C</a>
<a href="#d1">D1</a><a href="#d2">D2</a><a href="#d3">D3</a><a href="#respuestas">Exportar</a>
<span class="sw">Tamaño: <button data-s="118" class="on">118×30</button><button data-s="80">80×24</button></span></nav>
<main>{"".join(body)}</main>
<div id="zoom"><img alt=""></div>
<script>
const DECS = {decs};
document.querySelectorAll('nav .sw button').forEach(b => b.onclick = () => {{
  document.body.className = 's' + b.dataset.s;
  document.querySelectorAll('nav .sw button').forEach(x => x.classList.toggle('on', x === b));
}});
const z = document.getElementById('zoom'), zi = z.querySelector('img');
document.querySelectorAll('figure img').forEach(i => i.onclick = () => {{ zi.src = i.src; z.style.display = 'block'; }});
z.onclick = () => {{ z.style.display = 'none'; }};
const note = k => document.querySelector('[data-note="' + k + '"]').value.trim();
const radio = n => {{ const c = document.querySelector('input[name="' + n + '"]:checked'); return c ? c.value : null; }};
// the preview's tiny highlighter: JSON keys and strings on the JSON line
const paint = txt => txt.split('\\n').map(l => {{
  const e = l.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  return l.startsWith('JSON: ') ? e.replace(/("(?:[^"\\\\]|\\\\.)*")(\\s*:)?/g,
    (m, s, c) => c ? '<span class="k">' + s + '</span>' + c : '<span class="s">' + s + '</span>') : e;
}}).join('\\n');
document.getElementById('export').onclick = async () => {{
  const pick = radio('variant');
  const data = {{ round: 'milestone_row', branch: 'proto/milestone-row',
    variant: {{ choice: pick || 'A', chosen_explicitly: !!pick, objections: {{}} }}, decisions: {{}}, notes: note('general') }};
  const lines = ['Milestone row round — respuestas',
                 'Variante: ' + (pick || 'A') + (pick ? '' : ' (recomendada, sin marcar)')];
  for (const v of ['A', 'B', 'C']) {{
    const o = note('v' + v); data.variant.objections[v] = o;
    if (o) lines.push('Objeción ' + v + ': ' + o);
  }}
  for (const [k, rec] of DECS) {{
    const p = radio(k), obj = document.querySelector('[data-obj="' + k + '"]').checked, t = note(k);
    data.decisions[k] = {{ choice: p || rec, chosen_explicitly: !!p, objects: obj || !!t, note: t }};
    lines.push(k.toUpperCase() + ': ' + (p || rec) + (p ? '' : ' (recomendada, sin marcar)')
               + ((obj || t) ? ' · OBJETO' + (t ? ': ' + t : '') : ''));
  }}
  if (data.notes) lines.push('NOTAS: ' + data.notes);
  lines.push('JSON: ' + JSON.stringify(data));
  const txt = lines.join('\\n');
  const pre = document.getElementById('preview'); pre.innerHTML = paint(txt); pre.hidden = false;
  try {{ await navigator.clipboard.writeText(txt); document.getElementById('done').textContent = 'Copiado al portapapeles.'; }}
  catch (e) {{ document.getElementById('done').textContent = 'No pude copiar: selecciona el texto de abajo.'; }}
}};
</script>
</body></html>
"""
    PAGE.write_text(page, encoding="utf-8")
    print(PAGE, f"{PAGE.stat().st_size // 1024} KB · figures", FIGN[0], "· missing:", MISSING)


if __name__ == "__main__":
    main()

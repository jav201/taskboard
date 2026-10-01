"""THROWAWAY: build the decision gallery for the edit-modal + kanban-priority round.

    python prototypes/edit_modal/proto.py shot
    python prototypes/kanban_priority/proto.py shot
    powershell -File prototypes/edit_modal/shoot.ps1 -Proto ... -Variant ...   (PNGs)
    python prototypes/edit_modal/build_html.py

-> prototypes/edit_modal/out/ronda-edicion-prioridad.html (self-contained:
   SVGs inline with the cdnjs @font-face stripped, PNGs as data URIs).
"""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EOUT = HERE / "out"
KOUT = HERE.parent / "kanban_priority" / "out"
HTML_OUT = EOUT / "ronda-edicion-prioridad.html"
SIZES = (("120", "120x36"), ("80", "80x24"))

ef = json.loads((EOUT / "facts_edit.json").read_text(encoding="utf-8"))
kf = json.loads((KOUT / "facts_kanban.json").read_text(encoding="utf-8"))


def svg(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    if t.startswith("<?xml"):
        t = t.split("?>", 1)[1]
    t = re.sub(r"@font-face\s*\{[^}]*\}", "", t)
    return t.strip()


def png(path: Path) -> str:
    if not path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def e_fact(v: str, w: str) -> str:
    f = ef[f"{v}-{w}"]
    s = (f"notas: <b>{f['notes_rows_visible']}</b> filas visibles de "
         f"{f['notes_wrapped_rows_total']} · {f['notes_cols']} columnas de ancho")
    if not f["title_visible"]:
        s += " · <span class=warn>título fuera de vista</span>"
    if not f["save_visible"]:
        s += " · <span class=warn>Save fuera de vista (hay que hacer scroll)</span>"
    return s


def k_fact(v: str, w: str) -> str:
    f, b = kf[f"{v}-{w}"], kf[f"0-{w}"]
    rows = f["board_rows"] - b["board_rows"]
    tc = f["high_title_chars"]
    delta = sum(tc[k] - b["high_title_chars"][k] for k in tc) / len(tc)
    return (f"tablero: <b>{f['board_rows']}</b> filas ({rows:+d} vs base) · "
            f"título de cada tarjeta alta: <b>{delta:+.0f}</b> caracteres vs base · "
            f"{f['high_open']} tarjetas altas abiertas, 1 alta terminada (no grita)")


EDIT = [
    ("0", "0 · Baseline — el TaskModal actual",
     "Un VerticalScroll de 62 columnas: ocho campos de 3 filas cada uno, Notes fijo en "
     "height: 5 (3 filas de texto tras el borde), URLs e Images de 4. Al enfocar las notas "
     "el modal hace scroll y el título desaparece arriba. Es la queja tal cual: 3 filas para "
     "un texto que envuelve a 43."),
    ("A", "A · Editor dividido",
     "Modal al 92 % × 92 %. Columna izquierda de 34 columnas con campos de UNA fila (Select e "
     "Input sin el borde tall, sobre un pozo teñido), checkboxes apiladas, URLs e imágenes "
     "chicas abajo. La derecha es solo notas a 1fr: el texto se lleva toda la altura."),
    ("B", "B · Pestañas",
     "Título fijo arriba, luego un TabbedContent: Notes (el TextArea llena la pestaña), Details "
     "(los ocho campos en rejilla 2 × par etiqueta/valor, tamaño normal) y Links (URLs + imágenes "
     "+ pegar). Save/Cancel siempre visibles. Es el que da más ANCHO al texto: menos envoltura."),
    ("C", "C · Pantalla completa + vista previa",
     "Pantalla entera: una línea de título, una fila densa de 'chips' de propiedades "
     "(proyecto · fase · prioridad · inicio→vence · banderas), y debajo editor | vista previa. "
     "La vista previa usa _highlight_markup de la app: ==…== amarillo, !!…!! rojo, ++…++ verde, "
     "en vivo mientras escribes. URLs/imágenes y botones en una franja al pie."),
    ("D", "D · Compacto (conservador)",
     "El mismo modal vertical, pero de 100 columnas, campos de una fila en rejilla de 4 columnas "
     "(etiqueta/valor × 2), las tres banderas en una sola fila, notas a 1fr con mínimo 8, URLs e "
     "imágenes lado a lado. El cambio más chico respecto a hoy."),
]

KANBAN = [
    ("0", "0 · Baseline — el `!` neutro",
     "La prioridad alta es un único `!` en tono ink entre los indicadores de la derecha "
     "(card_cell, 'THE GLYPH HOUSE'): ni ámbar (= vence hoy) ni tono de proyecto (= identidad). "
     "Correcto en semántica, pero un glifo de 1 celda entre ·4d +2d se pierde."),
    ("K1", "K1 · Franja",
     "La franja de proyecto ▊ se queda con su hue; el espacio que la sigue se vuelve un medio "
     "bloque ▌ en ink, y el título va en negrita brillante. Cero celdas gastadas (el `!` sobra y "
     "se quita, así el título GANA 2 caracteres). Todo en la casa neutra."),
    ("K2", "K2 · Tamaño",
     "La tarjeta alta ocupa dos filas: la normal y una segunda con la primera línea de notas "
     "(o el chip de fecha si no hay notas), con la franja de proyecto continuando. Lo que "
     "diferencia es la MASA, no un color. line_map sigue apuntando a la primera fila."),
    ("K3", "K3 · Insignia inversa",
     "Una insignia `!!` en video inverso, color rose (el hue de prioridad alta del gantt, "
     "_priority_hue), justo después de la franja. Es la señal más fuerte a la vista — y la que "
     "rompe la casa de color (ver conflicto abajo)."),
    ("K4", "K4 · Banda de prioridad",
     "Dentro de cada columna, las tarjetas altas abiertas suben a una banda arriba, bajo un "
     "divisor `── high ──` y cerrada con una regla; el resto sigue en sus grupos de proyecto. "
     "La posición es la señal. Pasa por el ÚNICO asiento de orden (kanban_order), así que la "
     "navegación con flechas sigue lo que se ve."),
]


def figure(prefix: str, out: Path, v: str, stem: str, extra: str = "") -> str:
    parts = []
    for w, size in SIZES:
        p = png(out / f"wt_{v}_{size}.png")
        s = svg(out / f"{stem}_{v}_{size}.svg")
        pimg = (f'<img alt="Windows Terminal real · {prefix} {v} · {size}" src="{p}">'
                if p else '<p class="warn">sin PNG de Windows Terminal</p>')
        parts.append(f'''<div class="size" data-w="{w}">
  <div class="shot wt"><span class="tag">Windows Terminal real · {size}</span>{pimg}</div>
  <div class="shot svgf"><span class="tag">SVG Textual (run_test) · {size}</span><div class="term">{s}</div></div>
</div>''')
    return "\n".join(parts) + extra


def section(title: str, intro: str, items, stem: str, out: Path, fact, prefix: str,
            decide: str) -> str:
    cards = []
    for v, name, why in items:
        extra = ""
        if stem == "edit" and v == "B":
            extra = "".join(
                f'<div class="size" data-w="{w}"><div class="shot svgf"><span class="tag">'
                f'SVG · pestaña Details activa · {size}</span><div class="term">'
                f'{svg(out / f"edit_B_{size}_details.svg")}</div></div></div>'
                for w, size in SIZES)
        facts = "".join(f'<p class="fact" data-w="{w}">mide · {size}: {fact(v, w)}</p>'
                        for w, size in SIZES)
        cards.append(f'''<article class="variant" id="{prefix}-{v}">
<h3>{html.escape(name)}</h3>
<p class="why">{html.escape(why)}</p>
{facts}
{figure(prefix, out, v, stem, extra)}
</article>''')
    opts = "".join(
        f'<label><input type="radio" name="{prefix}-pick" value="{v}"> {html.escape(n)}</label>'
        for v, n, _ in items)
    steal = "".join(
        f'<label><input type="checkbox" name="{prefix}-steal" value="{v}"> {v}</label>'
        for v, _n, _ in items if v != "0")
    return f'''<section class="problem" id="{prefix}">
<h2>{title}</h2>
<p class="intro">{intro}</p>
{''.join(cards)}
<div class="decide" data-p="{prefix}">
<h3>Decisión · {title.split("·")[-1].strip()}</h3>
{decide}
<div class="opts">{opts}</div>
<p class="sub">¿Robar algo de otra variante?</p><div class="opts">{steal}</div>
<textarea placeholder="por qué / qué combinar…"></textarea>
</div>
</section>'''


EDIT_DECIDE = """<ul class="sum">
<li><b>0</b> — sin cambio: 3 filas de notas, título y Save fuera de vista al escribir.</li>
<li><b>A</b> — más filas en 120×36 (20), pero a 80 columnas las notas quedan en 30 de ancho.</li>
<li><b>B</b> — el texto más ANCHO (102 col) y buen alto (18); los metadatos quedan a un clic de pestaña.</li>
<li><b>C</b> — el más alto (23 filas) + vista previa con color; la fila de chips no cabe a 80 columnas.</li>
<li><b>D</b> — el cambio mínimo: 9 filas a 120×36; a 80×24 Save queda bajo el pliegue (scroll).</li>
</ul>"""

KANBAN_DECIDE = """<ul class="sum">
<li><b>0</b> — `!` ink de 1 celda: correcto y fácil de no ver.</li>
<li><b>K1</b> — franja ink + negrita: 0 filas, +2 caracteres de título, sin conflicto de color.</li>
<li><b>K2</b> — dos filas por tarjeta alta: +1 fila por cada una; diferencia por masa.</li>
<li><b>K3</b> — insignia rose: la señal más fuerte, choca con pink (proyecto) y over (vencido).</li>
<li><b>K4</b> — banda arriba de cada columna: +2 filas por columna con altas; la posición es la señal.</li>
</ul>
<p class="note">Conflicto de color de K3, verificado contra la paleta: <code>rose #fb7185</code> ya NO es un hue
de proyecto ofrecido (PROJECT_COLORS lo retiró y lo remapea a <code>pink #f472b6</code>, distancia rgb 49.5), pero
pink SÍ lo es — el fixture lo usa en «Marketing site» y la insignia queda junto a una franja casi del mismo tono.
Además rose vive a un paso de <code>over #f43f5e</code> (vencido/bloqueado): en «Login con biometría» la insignia y
el <code>-1d</code> rojo se leen como la misma alarma. Y <code>▲</code> se descartó porque ya es el glifo de bloqueado.</p>"""


page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>taskboard — ronda: ventana de edición y prioridad en kanban</title>
<style>
:root{{--bg:#0b0f14;--fg:#c9d1d9;--mut:#7d8790;--acc:#2dd4bf;--amb:#fbbf24;--line:#1f2733;--warn:#fb7185}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.wrap{{max-width:1280px;margin:0 auto;padding:28px 18px 120px}}
h1{{font-size:22px;color:var(--acc);margin:0 0 .4em}}
h2{{font-size:19px;color:var(--amb);margin:2.2em 0 .4em;border-bottom:1px solid var(--line);padding-bottom:.3em}}
h3{{font-size:15px;color:#e6edf3;margin:0 0 .4em}}
p{{line-height:1.55}} .intro,.lead{{color:var(--mut);max-width:96ch}}
nav.top{{position:sticky;top:0;background:#0b0f14ee;border-bottom:1px solid var(--line);padding:8px 0;z-index:10;display:flex;gap:16px;flex-wrap:wrap;align-items:center}}
nav.top a{{color:var(--fg);text-decoration:none;font-size:13px}} nav.top a:hover{{color:var(--acc)}}
.toggle button{{background:#111821;border:1px solid #334154;color:var(--fg);border-radius:6px;padding:4px 12px;cursor:pointer;font:inherit}}
.toggle button.on{{border-color:var(--acc);color:var(--acc)}}
.variant{{border:1px solid var(--line);border-radius:10px;padding:16px;margin:18px 0;background:#0d1219}}
.why{{max-width:100ch}} .fact{{font-size:13px;color:var(--amb);margin:.2em 0}}
.warn{{color:var(--warn)}}
.size{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}}
.size[hidden],.fact[hidden]{{display:none}}
.shot{{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#000;position:relative}}
.shot .tag{{display:block;font-size:11px;color:var(--mut);padding:4px 8px;background:#0b111a;border-bottom:1px solid var(--line)}}
.shot img{{display:block;width:100%;height:auto;cursor:zoom-in}}
.term svg{{display:block;width:100%;height:auto}}
.shot.big{{grid-column:1/-1}}
.decide{{border:1px solid var(--acc);border-radius:10px;padding:16px;margin:24px 0;background:#0b1a1a}}
.decide .opts{{display:flex;flex-wrap:wrap;gap:10px 22px;margin:8px 0}}
.decide textarea{{width:100%;min-height:70px;background:#0b111a;color:var(--fg);border:1px solid #334154;border-radius:6px;font:inherit;padding:8px;box-sizing:border-box}}
.sum li{{margin:.25em 0}} .note{{color:var(--mut);font-size:13px}} code{{color:var(--amb)}}
.sub{{margin:.6em 0 0;color:var(--mut);font-size:13px}}
#verdict{{white-space:pre-wrap;background:#0b111a;border:1px solid var(--line);border-radius:8px;padding:10px;font-size:13px}}
.hint{{font-size:12px;color:var(--mut)}}
@media (max-width:900px){{.size{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">
<h1>Ronda de prototipos: ventana de edición y prioridad en kanban</h1>
<p class="lead">Dos problemas, cinco variantes cada uno (la 0 es lo que hay hoy). Todas corren DENTRO de la app
real (vista kanban, tema y tcss reales, widgets reales en sus ids). Cada variante trae el PNG de una ventana real de
Windows Terminal y el SVG que exporta Textual con <code>run_test</code> + <code>save_screenshot</code>. Fecha fijada:
miércoles 30-sep-2026 (el reloj del ribbon sí es la hora real de la captura). Los números «mide» salen del render,
no de una estimación. Nada de esto se envía: es para elegir.</p>
<nav class="top">
<a href="#edit">1 · Ventana de edición</a><a href="#kan">2 · Prioridad en kanban</a><a href="#out">Veredicto</a>
<span class="toggle">ancho: <button data-w="120" class="on">120×36</button> <button data-w="80">80×24</button></span>
<span class="hint">clic en un PNG = tamaño completo</span>
</nav>

{section("1 · Ventana de edición de tareas",
         "«Cuando se editan tareas toda la interfaz de edición está muy amontonada y sobre todo la parte de "
         "texto es muy pequeña como para ver con claridad todo el contenido que ya está más el que se está "
         "escribiendo.» Fixture: una tarea con 23 líneas de notas reales (es/en, con ==…==, !!…!!, ++…++, "
         "lista y URL), 2 URLs y 1 imagen. El foco está en las notas con el cursor al final: es el estado "
         "«escribiendo».", EDIT, "edit", EOUT, e_fact, "edit", EDIT_DECIDE)}

{section("2 · Prioridad alta en kanban",
         "«KANBAN necesita algunos cues de color o tamaño (o algo) para diferenciar tareas con alta "
         "prioridad.» Fixture: 4 proyectos (sky, lime, violet, pink), 21 tareas en 4 fases, 6 de prioridad "
         "alta — 5 abiertas y 1 terminada («Release 3.4», que NO debe gritar). La selección está en una "
         "tarjeta normal para que el video inverso de selección no se confunda con la señal.",
         KANBAN, "kanban", KOUT, k_fact, "kan", KANBAN_DECIDE)}

<section id="out">
<h2>Veredicto para copiar</h2>
<p class="intro">Se arma solo con lo que marques arriba. Cópialo y pégalo en el chat.</p>
<div id="verdict">(marca una variante en cada problema)</div>
<p><button id="copy" class="toggle">copiar</button></p>
</section>
</div>
<script>
(function(){{
  function setW(w){{
    document.querySelectorAll('.size,.fact').forEach(function(el){{ el.hidden = el.dataset.w !== w; }});
    document.querySelectorAll('nav .toggle button').forEach(function(b){{ b.classList.toggle('on', b.dataset.w === w); }});
    try {{ localStorage.setItem('ronda-w', w); }} catch(e) {{}}
  }}
  document.querySelectorAll('nav .toggle button').forEach(function(b){{
    b.addEventListener('click', function(){{ setW(b.dataset.w); }});
  }});
  var w0 = '120'; try {{ w0 = localStorage.getItem('ronda-w') || '120'; }} catch(e) {{}}
  setW(w0);
  document.querySelectorAll('.shot.wt img').forEach(function(img){{
    img.addEventListener('click', function(){{ img.parentNode.classList.toggle('big'); }});
  }});
  function verdict(){{
    var out = [];
    document.querySelectorAll('.decide').forEach(function(d){{
      var p = d.dataset.p, name = p === 'edit' ? 'Edición' : 'Kanban';
      var pick = d.querySelector('input[type=radio]:checked');
      var steal = Array.prototype.map.call(d.querySelectorAll('input[type=checkbox]:checked'), function(c){{ return c.value; }});
      var why = d.querySelector('textarea').value.trim();
      out.push(name + ': ' + (pick ? pick.value : '—') + (steal.length ? ' + robar de ' + steal.join(', ') : '') + (why ? '\\n  ' + why : ''));
    }});
    document.getElementById('verdict').textContent = out.join('\\n');
  }}
  document.querySelectorAll('.decide input, .decide textarea').forEach(function(el){{
    el.addEventListener('input', verdict); el.addEventListener('change', verdict);
  }});
  document.getElementById('copy').addEventListener('click', function(){{
    var t = document.getElementById('verdict').textContent;
    if (navigator.clipboard) navigator.clipboard.writeText(t);
  }});
  verdict();
}})();
</script>
</body>
</html>
"""

HTML_OUT.write_text(page, encoding="utf-8")
print(f"wrote {HTML_OUT} ({HTML_OUT.stat().st_size // 1024} KB)")

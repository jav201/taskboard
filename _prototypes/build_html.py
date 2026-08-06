import sys, html, pathlib
sys.path.insert(0, r"C:\Users\jjgh8\Github\taskboard\_prototypes")
import proto

SCREENS = [("gantt", proto.ledger, "ledger"), ("gantt", proto.darkside, "darkside"),
           ("gantt", proto.naught, "naught")]

def grid_html(cells, ground):
    rows = []
    for row in cells:
        out, run, fg, bg = [], "", None, None
        for ch, f, b in row:
            f = f or "#888"; b = b or ground
            if (f, b) != (fg, bg):
                if run: out.append(f'<span style="color:{fg};background:{bg}">{html.escape(run)}</span>')
                run, fg, bg = "", f, b
            run += ch
        if run: out.append(f'<span style="color:{fg};background:{bg}">{html.escape(run)}</span>')
        rows.append("".join(out))
    return "\n".join(rows)

panes = []
for lang in ("taskboard", "ledger", "darkside", "naught"):
    if lang == "taskboard":
        gg, t = proto.hybrid(screen="gantt"); lg, _ = proto.hybrid(screen="lanes")
    else:
        gg, t = {"ledger": proto.ledger, "darkside": proto.darkside, "naught": proto.naught}[lang]()
        lg, _ = proto.lanes(lang)
    panes.append((lang, t, grid_html(gg, t["ground"]), grid_html(lg, t["ground"]), t["note"]))

DOC = {"taskboard": "<strong>El híbrido que pediste.</strong> Estructura de <em>Ledger</em>: guía vertical de semana, mes rotulado, guías de puntos del título a la cifra, banda cada 5ª fila. Discreción de <em>Darkside</em>: la tarea pasiva es un trazo fino y apagado, y el acento <code>#2dd4bf</code> se gasta <strong>solo en lo interactivo</strong> — la espina de la fila enfocada y sus acciones. Colores: los tuyos, sin inventar ninguno. El hue del proyecto sigue siendo IDENTIDAD (la ley que ya tiene la app) y <code>over</code> sigue siendo la única severidad.",
 "ledger": "Estructura = COLUMNAS REGLADAS, nunca cajas. La regla de semana <em>es</em> el gauge que pediste: cada barra se mide contra ella. Guías de puntos cierran el hueco entre el nombre y su cifra. Cada 5ª línea lleva la banda de papel rayado — la ayuda que deja al ojo cruzar 80 celdas sin perder su fila. Rojo = deuda, y solo en vencidos.",
 "darkside": "Acromático. Los datos pasivos son <strong>escalones de gris cuyo nivel va en la FORMA</strong>, no en el color — por eso las barras dejan de gritar. El único acento azul se gasta <strong>exclusivamente en lo interactivo</strong>: la fila seleccionada y sus acciones. La profundidad es un escalón de fondo, nunca un borde.",
 "naught": "La cantidad son <strong>puntos discretos encendidos, nunca una barra llena</strong>: un punto por semana, así que la duración se <em>cuenta</em> en vez de estimarse. Sin marcos. El rojo existe solo para la alarma."}

body = []
for lang, t, gh, lh, note in panes:
    body.append(f'''<section class="v" id="v-{lang}">
  <h2>{t["label"]} <span class="note">{html.escape(note)}</span></h2>
  <p class="doc">{DOC[lang]}</p>
  <h3>Gantt</h3><pre class="term" style="background:{t['ground']}">{gh}</pre>
  <h3>Lanes — un proyecto por fila, y la selección se despliega</h3>
  <pre class="term" style="background:{t['ground']}">{lh}</pre>
</section>''')

page = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prototipos — gantt y lanes</title></head><body>
<h1>Prototipos — gantt y lanes</h1>
<p class="lede">Tres lenguajes del catálogo de <code>tui-design</code>, renderizados <strong>con tu board real</strong>
(104×26). Cada uno responde a una lectura distinta de tu queja; no son recoloreos.</p>

<div class="brief">
<h2>El brief, medido antes de dibujar</h2>
<table>
<tr><th>pantalla</th><th>suelo (retícula + vacío)</th><th>texto</th><th>marcas de datos</th></tr>
<tr><td>gantt hoy</td><td class="bad">68.2 %</td><td>22.5 %</td><td class="bad">9.3 %</td></tr>
<tr><td>lanes hoy</td><td class="bad">53.3 %</td><td>38.5 %</td><td class="bad">8.2 %</td></tr>
</table>
<p><strong>Postura: se OPERAN</strong> — navegas y editas. De ahí salen tres decisiones que comparten
las tres variantes: la fila seleccionada manda, el campo cede ancho al texto de las tareas, y
<strong>la selección despliega más información</strong> (lo que pediste) en una fila extra que solo
existe mientras esa tarea está enfocada.</p>
<p>Tu diagnóstico —<em>"atraen la vista a barras sin sentido, no hay gauges de semana y mes"</em>— es la
raíz: hoy la barra no se mide contra nada. <strong>Las tres variantes traen rejilla temporal</strong>
(mes rotulado + semana marcada) y <strong>matan la segunda fila vacía por proyecto</strong>.</p>
</div>

<div class="switch">
  <button data-t="taskboard" class="on">Taskboard (híbrido)</button>
  <button data-t="ledger">Ledger</button>
  <button data-t="darkside">Darkside</button>
  <button data-t="naught">Naught</button>
</div>

{"".join(body)}

<style>
:root{{--fg:#1e2230;--mut:#5b6478;--line:#e3e7f0;--card:#fff;--bg:#f6f7fb}}
@media (prefers-color-scheme:dark){{:root{{--fg:#e6e9f2;--mut:#9aa4bd;--line:#26304a;--card:#141a2a;--bg:#0b0f1a}}}}
:root[data-theme="dark"]{{--fg:#e6e9f2;--mut:#9aa4bd;--line:#26304a;--card:#141a2a;--bg:#0b0f1a}}
:root[data-theme="light"]{{--fg:#1e2230;--mut:#5b6478;--line:#e3e7f0;--card:#fff;--bg:#f6f7fb}}
body{{background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;
     max-width:1180px;margin:0 auto;padding:28px}}
h1{{font-size:28px;margin:0 0 6px}} .lede{{color:var(--mut);margin:0 0 22px}}
h2{{font-size:20px;margin:26px 0 4px}} h3{{font-size:14px;color:var(--mut);margin:18px 0 6px;
   text-transform:uppercase;letter-spacing:.06em}}
.note{{font-size:13px;color:var(--mut);font-weight:400}}
.doc{{color:var(--mut);margin:2px 0 12px;max-width:80ch}}
.brief{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 0 22px}}
.brief table{{border-collapse:collapse;margin:8px 0 14px;font-size:14px}}
.brief th,.brief td{{border:1px solid var(--line);padding:5px 12px;text-align:left}}
.bad{{color:#e05252;font-weight:600}}
.switch{{display:flex;gap:8px;margin:0 0 18px;position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:5}}
.switch button{{font:inherit;padding:7px 16px;border:1px solid var(--line);background:var(--card);
  color:var(--fg);border-radius:999px;cursor:pointer}}
.switch button.on{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
pre.term{{font:12px/1.18 "Cascadia Mono",Consolas,"DejaVu Sans Mono",monospace;padding:14px;
  border-radius:10px;overflow-x:auto;border:1px solid var(--line);white-space:pre;tab-size:1}}
.v{{display:none}} .v.on{{display:block}}
</style>
<script>
const show=t=>{{document.querySelectorAll('.v').forEach(s=>s.classList.toggle('on',s.id==='v-'+t));
 document.querySelectorAll('.switch button').forEach(b=>b.classList.toggle('on',b.dataset.t===t));}};
document.querySelectorAll('.switch button').forEach(b=>b.onclick=()=>show(b.dataset.t));
show('taskboard');
</script>
</body></html>'''

out = pathlib.Path(r"C:\Users\jjgh8\Github\taskboard\_prototypes\prototipos.html")
out.write_text(page, encoding="utf-8")
print("escrito:", out, f"({len(page)} bytes)")

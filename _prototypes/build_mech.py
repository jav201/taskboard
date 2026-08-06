import sys, html, pathlib
sys.path.insert(0, r"C:\Users\jjgh8\Github\taskboard\_prototypes")
import proto

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

DOC = {
 "A": ("Contesta <strong>«cuánto del trabajo ya está comprometido para tal fecha»</strong>. Es la semántica "
       "real de <code>wave.load_curve</code>: acumulada, normalizada al conjunto TOTAL del proyecto, y "
       "<strong>cortada en la fecha del proyecto</strong> — donde ves <code>╵</code> el banco se detiene, "
       "así una meseta no puede irse al borde diciendo nada. Pendiente = presión; meseta = holgura."),
 "C": ("Contesta <strong>«qué tan avanzado va»</strong>, y nada más. Sin eje, sin tiempo: proporción hecha "
       "contra total, con la cifra al lado para que la barra no tenga que ser leída con precisión. "
       "Es la más barata de entender y la que menos dice."),
 "D": ("Contesta <strong>«qué me exige ahora»</strong>. Cero ambigüedad y cero aprendizaje: no hay marca "
       "que descifrar. <code>▲n late</code> sólo aparece cuando hay deuda; si no, dice <em>on time</em>. "
       "Es la que encaja con la postura que declaraste — se OPERA, no se contempla."),
}
blocks = []
for m in "ACD":
    g, t = proto.mech_rows(m)
    blocks.append(f'''<div class="mech">
  <p class="doc">{DOC[m]}</p>
  <pre class="term" style="background:{t['ground']}">{grid_html(g, t['ground'])}</pre>
</div>''')

page = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mecanismos A · C · D — la fila de proyecto</title></head><body>
<h1>La fila de proyecto, tres mecanismos</h1>
<p class="lede">Las mismas cinco filas, tus datos reales, la paleta de la app. Sólo cambia
<strong>qué pregunta contesta la marca</strong>.</p>
{"".join(blocks)}
<div class="verdict">
<h2>Lo que veo al compararlas</h2>
<p><strong>A</strong> es la única que usa el eje del tiempo, y su corte <code>╵</code> es información
real: te dice dónde termina el compromiso del proyecto. Pero sigue exigiendo que aprendas a leer una
pendiente, y en una fila de 1 celda de alto la pendiente es difícil de juzgar.</p>
<p><strong>C</strong> se entiende sin explicación, pero contesta la pregunta menos útil de las tres:
saber que vas 12/20 no te dice si algo arde hoy.</p>
<p><strong>D</strong> no tiene nada que descifrar y es la única que nombra la urgencia
(<code>▲n late</code>) y el próximo golpe (<code>next Nd</code>). En una pantalla que se OPERA, eso es
lo que necesitas a la altura de la fila.</p>
<p class="rec"><strong>Sigo recomendando D en la fila, y A en la vista de detalle</strong> — donde hay
sitio para que la curva se lea de verdad y estás leyendo, no navegando.</p>
</div>
<style>
:root{{--fg:#1e2230;--mut:#5b6478;--line:#e3e7f0;--card:#fff;--bg:#f6f7fb}}
@media (prefers-color-scheme:dark){{:root{{--fg:#e6e9f2;--mut:#9aa4bd;--line:#26304a;--card:#141a2a;--bg:#0b0f1a}}}}
:root[data-theme="dark"]{{--fg:#e6e9f2;--mut:#9aa4bd;--line:#26304a;--card:#141a2a;--bg:#0b0f1a}}
:root[data-theme="light"]{{--fg:#1e2230;--mut:#5b6478;--line:#e3e7f0;--card:#fff;--bg:#f6f7fb}}
body{{background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;
     max-width:1100px;margin:0 auto;padding:28px}}
h1{{font-size:26px;margin:0 0 6px}} .lede{{color:var(--mut);margin:0 0 22px}}
.mech{{margin:0 0 22px}} .doc{{color:var(--mut);margin:0 0 8px;max-width:88ch}}
pre.term{{font:12.5px/1.25 "Cascadia Mono",Consolas,"DejaVu Sans Mono",monospace;padding:14px;
  border-radius:10px;overflow-x:auto;border:1px solid var(--line);white-space:pre}}
.verdict{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin-top:26px}}
.verdict h2{{font-size:18px;margin:0 0 8px}} .verdict p{{margin:8px 0}}
.rec{{border-left:3px solid #2dd4bf;padding-left:12px}}
code{{font-family:Consolas,monospace;font-size:.92em}}
</style></body></html>'''
out = pathlib.Path(r"C:\Users\jjgh8\Github\taskboard\_prototypes\mecanismos.html")
out.write_text(page, encoding="utf-8"); print("escrito:", out)

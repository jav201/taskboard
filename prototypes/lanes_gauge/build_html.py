"""Build the comparison HTML for the gauge-board prototypes (with flipbook).

    python prototypes/lanes_gauge/build_html.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HTML = OUT / "lanes-gauge.html"

SECTIONS = ["g1", "g2"]

COPY = {
    "g1": (
        "G1 · Retícula 3×2 — mercurio + sedimento",
        "Menos columnas, capas apiladas: cada panel respira. La espina de mercurio "
        "(la ventana del proyecto: start abajo, due arriba; roja con ▲ si pasó) "
        "corre a la izquierda; la barra de sedimento mide el countdown al próximo "
        "aterrizaje a lo ancho del panel (36 celdas para 28 días — los studs por "
        "tarea ya no están apretados); y las filas de tareas recuperan su texto "
        "completo: título, indicadores (! ▤ ↗) y chip de fecha absoluta. El tally "
        "de done ancla el pie del panel."),
    "g2": (
        "G2 · Retícula 2×3 — paneles anchos",
        "Dos columnas de 57 celdas, tres capas: el máximo de texto por fila "
        "(títulos casi completos a 118) y la barra de sedimento a ~2 celdas por "
        "día. Menos proyectos a la vista por capa; la regla horizontal separa "
        "capas. Para boards con muchos proyectos, la retícula paginaría con "
        "`+N lanes` en el header."),
}

NAMES = {k: COPY[k][0] for k in SECTIONS}


def read_svg(name: str) -> str:
    text = (OUT / name).read_text(encoding="utf-8")
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[1]
    return text.strip()


def section(key: str, hidden: bool) -> str:
    frames = "\n".join(
        f'<div class="term-fig frame" data-frame="{i}"{" hidden" if i else ""}>'
        f'{read_svg(f"grid-{key}-f{i}-118.svg")}</div>'
        for i in range(4))
    return f'''<section class="variant" data-variant="{key}"{" hidden" if hidden else ""}>
<h2>{COPY[key][0]}</h2>
<p class="note">{COPY[key][1]}</p>
<div class="flipbook" data-variant="{key}">
{frames}
</div>
<p class="note cap">▲ fixture cargado (barrido de entrada, 4 frames reales · ~600 ms).
▶ mismo board en calma:</p>
<div class="term-fig">{read_svg(f"grid-{key}-calm-118.svg")}</div>
<p class="note cap">▶ el mismo mecanismo a 68×24:</p>
<div class="term-fig narrow">{read_svg(f"grid-{key}-68.svg")}</div>
</section>'''


sections_html = "\n".join(section(k, i > 0) for i, k in enumerate(SECTIONS))

HTML.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>taskboard — Lanes como columnas con diales</title>
<style>
body{{margin:0;background:#0b0f14;color:#c9d1d9;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.wrap{{max-width:1240px;margin:0 auto;padding:30px 20px 120px}}
h1{{font-size:22px;color:#2dd4bf}}
h2{{font-size:16px;color:#fbbf24;margin:0 0 .5em}}
p.note{{color:#7d8790;max-width:92ch;margin:.3em 0 1.2em;line-height:1.5}}
p.cap{{font-size:12px;margin:1.2em 0 .4em}}
.term-fig{{margin:16px 0;border:1px solid #1f2733;border-radius:8px;overflow:hidden;background:#000;box-shadow:0 10px 30px rgba(0,0,0,.45)}}
.term-fig svg{{display:block;width:100%;height:auto}}
.term-fig.narrow{{max-width:640px}}
.switcher{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:#1f2733;border:1px solid #334154;border-radius:999px;padding:8px 18px;display:flex;gap:14px;align-items:center;box-shadow:0 8px 24px rgba(0,0,0,.55);z-index:100}}
.switcher button{{background:#0b0f14;border:1px solid #334154;color:#c9d1d9;border-radius:6px;padding:5px 12px;cursor:pointer;font:inherit}}
.switcher button:hover{{border-color:#2dd4bf;color:#2dd4bf}}
.switcher .label{{font-weight:bold;color:#2dd4bf;min-width:230px;text-align:center}}
</style>
</head>
<body>
<div class="wrap">
<h1>Instrumentos de tiempo que juegan a favor del medio</h1>
<p class="note">Ronda 4: mecanismos que miden el tiempo usando lo que la terminal hace
BIEN — aristas rectas, textura de grano, resolución vertical — en vez de pelear la
cuantización del círculo. Mismo layout de columnas y mismas fechas; cambia el
instrumento. La animación de entrada se muestra como flipbook de renders reales
(4 frames · ~600 ms). Navega con ←/→.</p>
{sections_html}
</div>

<div class="switcher">
  <button id="prev">←</button>
  <span class="label" id="label"></span>
  <button id="next">→</button>
</div>

<script>
const variants = {SECTIONS!r};
const names = {NAMES!r};
function read(){{ const v = new URLSearchParams(location.search).get('variant'); return variants.includes(v) ? v : variants[0]; }}
function show(v){{
  document.querySelectorAll('.variant').forEach(el => el.hidden = el.dataset.variant !== v);
  document.getElementById('label').textContent = names[v];
  const url = new URL(location.href); url.searchParams.set('variant', v); history.replaceState(null, '', url);
}}
let idx = variants.indexOf(read());
show(variants[idx]);
function go(i){{ idx = (i + variants.length) % variants.length; show(variants[idx]); resetFlip(); }}
document.getElementById('prev').addEventListener('click', () => go(idx - 1));
document.getElementById('next').addEventListener('click', () => go(idx + 1));
document.addEventListener('keydown', e => {{
  if (['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) return;
  if (e.key === 'ArrowLeft') go(idx - 1);
  if (e.key === 'ArrowRight') go(idx + 1);
}});

// flipbook: play f0..f3 at ~150 ms, hold the last frame, restart
let timer = null;
function resetFlip() {{
  if (timer) clearInterval(timer);
  const book = document.querySelector('.variant:not([hidden]) .flipbook');
  if (!book) return;
  const frames = book.querySelectorAll('.frame');
  let f = 0, hold = 0;
  frames.forEach((el, i) => el.hidden = i !== 0);
  timer = setInterval(() => {{
    if (f < frames.length - 1) {{ f++; frames.forEach((el, i) => el.hidden = i !== f); }}
    else if (hold < 8) {{ hold++; }}               // ~1.2 s en el frame final
    else {{ f = 0; hold = 0; frames.forEach((el, i) => el.hidden = i !== 0); }}
  }}, 150);
}}
resetFlip();
</script>
</body>
</html>
""", encoding="utf-8")

print(f"wrote {HTML}")

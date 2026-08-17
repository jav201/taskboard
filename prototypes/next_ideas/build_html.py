"""Build a self-contained prototype HTML from the generated SVGs."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HTML = OUT / "next-ideas.html"

SVGS = {
    "baseline": OUT / "gantt-current.svg",
    "b": OUT / "gantt-variant-b.svg",
    "c": OUT / "gantt-variant-c.svg",
}


def read_svg(key: str) -> str:
    text = SVGS[key].read_text(encoding="utf-8")
    # strip XML declaration so it embeds cleanly
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[1]
    return text.strip()


HTML.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>taskboard — próximos incrementos y mejoras al gantt</title>
<style>
body{{margin:0;background:#0b0f14;color:#c9d1d9;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.wrap{{max-width:1180px;margin:0 auto;padding:30px 20px 120px}}
h1{{font-size:22px;color:#2dd4bf}}
h2{{font-size:16px;color:#fbbf24;margin:0 0 .5em}}
p.note{{color:#7d8790;max-width:85ch;margin:.3em 0 1.2em;line-height:1.5}}
.term-fig{{margin:16px 0;border:1px solid #1f2733;border-radius:8px;overflow:hidden;background:#000;box-shadow:0 10px 30px rgba(0,0,0,.45)}}
.term-fig svg{{display:block;width:100%;height:auto}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media(max-width:900px){{.pair{{grid-template-columns:1fr}}}}

.palette pre{{margin:0;padding:12px 14px;font-size:13px;line-height:1.5;color:#c9d1d9}}
.fg-accent{{color:#2dd4bf}} .fg-amber{{color:#fbbf24}} .fg-rose{{color:#fb7185}}
.fg-sky{{color:#38bdf8}} .fg-mut{{color:#7d8790}} .fg-white{{color:#e6edf3;font-weight:bold}}
.bg-match{{background:rgba(45,212,191,.18)}}

.switcher{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:#1f2733;border:1px solid #334154;border-radius:999px;padding:8px 18px;display:flex;gap:14px;align-items:center;box-shadow:0 8px 24px rgba(0,0,0,.55);z-index:100}}
.switcher button{{background:#0b0f14;border:1px solid #334154;color:#c9d1d9;border-radius:6px;padding:5px 12px;cursor:pointer;font:inherit}}
.switcher button:hover{{border-color:#2dd4bf;color:#2dd4bf}}
.switcher .label{{font-weight:bold;color:#2dd4bf;min-width:160px;text-align:center}}
</style>
</head>
<body>
<div class="wrap">
<h1>Próximos incrementos y mejoras al gantt</h1>
<p class="note">Página throwaway. Usa la barra flotante o las flechas del teclado para cambiar de variante. Los renders de gantt son capturas reales del motor de Rich/Textual.</p>

<section class="variant" data-variant="A">
<h2>A · Cierres inmediatos del batch-05</h2>
<p class="note">Tres mejoras pequeñas que completan lo entregado: un comando "Open legend" en el palette, resaltado fuzzy al tipear, y la barra "more" en terminales angostos.</p>
<div class="pair">
<div class="term-fig palette">
  <pre><span class="fg-mut">type a command...</span> <span class="fg-white">kan</span>

 <span class="fg-accent">3</span>  Switch to <span class="bg-match">kan</span>ban
 <span class="fg-amber">?</span>  Open legend
 <span class="fg-accent">1</span>  Switch to swimlanes
 <span class="fg-sky">a</span>  Add task
 <span class="fg-sky">b</span>  Toggle blocked

<span class="fg-mut">1 match · esc/?/q close · ↓↑ select · ↵ run</span></pre>
</div>
<div class="term-fig palette">
  <pre><span class="fg-mut">system</span> <span class="fg-amber">?</span> Map <span class="fg-amber">;</span> More <span class="fg-amber">q</span> Quit  <span class="fg-mut">views</span> <span class="fg-accent">1</span> Lanes <span class="fg-accent">2</span> Agenda <span class="fg-accent">3</span> Gantt  <span class="fg-mut">task</span> <span class="fg-sky">↵</span> Details <span class="fg-sky">a</span> Add  <span class="fg-rose">+3</span></pre>
</div>
</div>
</section>

<section class="variant" data-variant="baseline" hidden>
<h2>Baseline · gantt actual</h2>
<p class="note">Densidad de referencia: mismo modelo de datos, sin controles de zoom ni semántica de prioridad.</p>
<div class="term-fig">{read_svg("baseline")}</div>
</section>

<section class="variant" data-variant="B" hidden>
<h2>B · Gantt: control del tiempo (refinado)</h2>
<p class="note">Menos carga visual: se quita el % de progreso de cada proyecto, se reemplaza el meter de cada tarea por un punto de estado, y se agregan controles de zoom/paneo. La marca de "hoy" es la misma regla vertical del motor actual, más visible.</p>
<div class="term-fig">{read_svg("b")}</div>
</section>

<section class="variant" data-variant="C" hidden>
<h2>C · Gantt: semántica de tareas (refinado)</h2>
<p class="note">Las barras usan el tono de prioridad (high=rose, normal=sky, low=mut). Los hitos son un rombo. Se añade un indicador de dependencia ligero al costado de la tarea que bloquea.</p>
<div class="term-fig">{read_svg("c")}</div>
</section>

</div>

<div class="switcher">
  <button id="prev">←</button>
  <span class="label" id="label">A</span>
  <button id="next">→</button>
</div>

<script>
const variants = ['A','baseline','B','C'];
const names = {{
  A: 'A · Cierres batch-05',
  baseline: 'Baseline · actual',
  B: 'B · Gantt tiempo',
  C: 'C · Gantt semántica'
}};
function read(){{ const v = new URLSearchParams(location.search).get('variant'); return variants.includes(v) ? v : 'A'; }}
function show(v){{
  document.querySelectorAll('.variant').forEach(el => el.hidden = el.dataset.variant !== v);
  document.getElementById('label').textContent = names[v];
  const url = new URL(location.href); url.searchParams.set('variant', v); history.replaceState(null, '', url);
}}
let idx = variants.indexOf(read());
show(variants[idx]);
document.getElementById('prev').addEventListener('click', () => {{ idx = (idx - 1 + variants.length) % variants.length; show(variants[idx]); }});
document.getElementById('next').addEventListener('click', () => {{ idx = (idx + 1) % variants.length; show(variants[idx]); }});
document.addEventListener('keydown', e => {{
  if (['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) return;
  if (e.key === 'ArrowLeft') {{ idx = (idx - 1 + variants.length) % variants.length; show(variants[idx]); }}
  if (e.key === 'ArrowRight') {{ idx = (idx + 1) % variants.length; show(variants[idx]); }}
}});
</script>
</body>
</html>
""", encoding="utf-8")

print(f"wrote {HTML}")

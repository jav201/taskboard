"""Build the self-contained comparison HTML for the next-level prototypes.

    python prototypes/next_level/build_html.py

Inlines the captured SVGs into one switchable page — same pattern as
prototypes/next_ideas/build_html.py.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HTML = OUT / "next-level.html"

# (variant key, [svg slugs]) — section order is switcher order
SECTIONS = [
    ("baseline", ["kanban-baseline"]),
    ("1A", ["kanban-lanes-priority"]),
    ("1B", ["kanban-lanes-project"]),
    ("2A", ["focus-review-queue"]),
    ("2B", ["focus-stale-tiles"]),
    ("3A", ["search-filter-kanban", "search-filter-gantt"]),
    ("3B", ["search-jump-palette"]),
    ("3C", ["search-context-dim"]),
]

COPY = {
    "baseline": (
        "Referencia · kanban actual",
        "Lo que ya está en main (batch-04): orden por proyecto/prioridad/due/recientes, "
        "grupos por proyecto/prioridad/horizonte, colapso de la última columna, foco por "
        "proyecto. Es la base contra la que se comparan 1A y 1B."),
    "1A": (
        "1A · Kanban lanes: prioridad",
        "El segundo eje que le falta al kanban: carriles horizontales × columnas de fase, "
        "con tarjetas reales en cada celda. Responde «¿qué es urgente y dónde está "
        "atorado?» de un vistazo. Misma geometría y mismos tonos que el group=priority "
        "ya shipped; la navegación sería j/k dentro de celda, h/l entre columnas."),
    "1B": (
        "1B · Kanban lanes: proyecto",
        "Los mismos carriles pero por proyecto: es la vista matrix ya shipped, pero con "
        "tarjetas en vez de conteos. Responde «¿cómo fluye cada proyecto?». Celda que "
        "desborda cierra con «+N», nunca corta una tarjeta."),
    "2A": (
        "2A · Focus: review queue",
        "El follow-up como PASO DE REVISIÓN, no como vitrina: una tarea a la vez a "
        "tamaño completo (notas con highlights, checklist, adjuntos), el resto de la "
        "cola en un rail ordenado por días-quieto. Todas las teclas del hint ya "
        "existen; no requiere cambios de modelo ni bindings nuevos."),
    "2B": (
        "2B · Focus: tiles stale-first",
        "El grid de tiles ya shipped, re-ordenado por días en fase (grupos por proyecto "
        "según su tarea más vieja) con una tira de presión arriba: «▲ 6 overdue · "
        "■ 4 sitting ≥7d». El board responde «¿qué se está pudriendo?» antes que "
        "«¿qué pineé?». Cero widgets nuevos: mismo tile, otro orden."),
    "3A": (
        "3A · Búsqueda: filtro vivo",
        "«/» abre una barra bajo el header; el board se re-renderiza filtrado al tipear "
        "(título, proyecto y notas), con los matches en reverse y el conteo a la "
        "derecha. Funciona igual en kanban y en gantt — el gantt además oculta los "
        "carriles de proyecto que quedan vacíos. «esc» limpia."),
    "3B": (
        "3B · Búsqueda: jump palette",
        "El board no se filtra: un overlay sólido (sin bordes, como manda el lenguaje) "
        "lista los resultados rankeados — match por título primero, luego proyecto, "
        "luego notas — y «↵» salta la selección a esa tarjeta en la vista actual. "
        "El board atrás se atenúa para dar contexto sin competir."),
    "3C": (
        "3C · Búsqueda: context dim",
        "Nada se oculta: las tarjetas que NO matchean se atenúan al 30 % y los matches "
        "conservan color completo con el texto en reverse. Mantiene la memoria "
        "espacial del board («sé dónde está esa tarjeta») a costa de conservar el "
        "ruido visual."),
}

NAMES = {k: COPY[k][0] for k, _ in SECTIONS}


def read_svg(slug: str) -> str:
    text = (OUT / f"{slug}.svg").read_text(encoding="utf-8")
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[1]
    return text.strip()


def figures(slugs: list[str]) -> str:
    return "\n".join(f'<div class="term-fig">{read_svg(s)}</div>' for s in slugs)


sections_html = "\n".join(
    f'''<section class="variant" data-variant="{key}"{" hidden" if i else ""}>
<h2>{COPY[key][0]}</h2>
<p class="note">{COPY[key][1]}</p>
{figures(slugs)}
</section>'''
    for i, (key, slugs) in enumerate(SECTIONS))

keys = [k for k, _ in SECTIONS]

HTML.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>taskboard — tres ideas, nivel siguiente</title>
<style>
body{{margin:0;background:#0b0f14;color:#c9d1d9;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.wrap{{max-width:1240px;margin:0 auto;padding:30px 20px 120px}}
h1{{font-size:22px;color:#2dd4bf}}
h2{{font-size:16px;color:#fbbf24;margin:0 0 .5em}}
p.note{{color:#7d8790;max-width:92ch;margin:.3em 0 1.2em;line-height:1.5}}
.term-fig{{margin:16px 0;border:1px solid #1f2733;border-radius:8px;overflow:hidden;background:#000;box-shadow:0 10px 30px rgba(0,0,0,.45)}}
.term-fig svg{{display:block;width:100%;height:auto}}
.switcher{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:#1f2733;border:1px solid #334154;border-radius:999px;padding:8px 18px;display:flex;gap:14px;align-items:center;box-shadow:0 8px 24px rgba(0,0,0,.55);z-index:100}}
.switcher button{{background:#0b0f14;border:1px solid #334154;color:#c9d1d9;border-radius:6px;padding:5px 12px;cursor:pointer;font:inherit}}
.switcher button:hover{{border-color:#2dd4bf;color:#2dd4bf}}
.switcher .label{{font-weight:bold;color:#2dd4bf;min-width:220px;text-align:center}}
.switcher .idea{{color:#5b6675;font-size:12px}}
</style>
</head>
<body>
<div class="wrap">
<h1>Tres ideas, nivel siguiente</h1>
<p class="note">Las ideas 1 (kanban ordenable) y 2 (focus tiles) del handoff ya están en main
(batch-04 y batch-07); esto es el nivel siguiente de las tres. Renders reales del motor de
Rich sobre el fixture sintético de siempre — 118×30, query de demo «api». Navega con ←/→;
las teclas 1/2/3 saltan a la primera variante de cada idea. Ninguna variante requiere
cambios al modelo.</p>
{sections_html}
</div>

<div class="switcher">
  <button id="prev">←</button>
  <span class="label" id="label"></span>
  <button id="next">→</button>
  <span class="idea">1 kanban · 2 focus · 3 búsqueda</span>
</div>

<script>
const variants = {keys!r};
const names = {NAMES!r};
function read(){{ const v = new URLSearchParams(location.search).get('variant'); return variants.includes(v) ? v : variants[0]; }}
function show(v){{
  document.querySelectorAll('.variant').forEach(el => el.hidden = el.dataset.variant !== v);
  document.getElementById('label').textContent = names[v];
  const url = new URL(location.href); url.searchParams.set('variant', v); history.replaceState(null, '', url);
}}
let idx = variants.indexOf(read());
show(variants[idx]);
function go(i){{ idx = (i + variants.length) % variants.length; show(variants[idx]); }}
document.getElementById('prev').addEventListener('click', () => go(idx - 1));
document.getElementById('next').addEventListener('click', () => go(idx + 1));
document.addEventListener('keydown', e => {{
  if (['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) return;
  if (e.key === 'ArrowLeft') go(idx - 1);
  if (e.key === 'ArrowRight') go(idx + 1);
  if (e.key === '1') show(variants[variants.indexOf('1A')]), idx = variants.indexOf('1A');
  if (e.key === '2') show(variants[variants.indexOf('2A')]), idx = variants.indexOf('2A');
  if (e.key === '3') show(variants[variants.indexOf('3A')]), idx = variants.indexOf('3A');
}});
</script>
</body>
</html>
""", encoding="utf-8")

print(f"wrote {HTML}")

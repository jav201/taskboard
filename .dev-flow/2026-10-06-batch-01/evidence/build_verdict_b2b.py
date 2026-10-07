"""Build the operator's visual-verdict sheet for batch 2026-10-06-batch-01 (B2b).

Inlines the close captures and renders one question block per visual decision;
answers download as taskboard-veredicto-b2b.json (the operator relays the file).

    PYTHONIOENCODING=utf-8 python .dev-flow/2026-10-06-batch-01/evidence/build_verdict_b2b.py
"""
import base64
import re
from pathlib import Path

EV = Path(r"C:\Users\jjgh8\Github\taskboard\.dev-flow\2026-10-06-batch-01\evidence")
CAP = EV / "captures"
OUT = EV / "veredicto-b2b.html"


def svg(name):
    t = (CAP / f"{name}.svg").read_text(encoding="utf-8")
    t = re.sub(r'\s*url\("https://[^"]+"\) format\("woff2?"\),?', "", t)
    t = re.sub(r",(\s*;)", r"\1", t)
    t = re.sub(r"src:\s*,", "src:", t)
    return "data:image/svg+xml;base64," + base64.b64encode(t.encode("utf-8")).decode()


FRAMES = "".join(
    f'<figure><figcaption>{cap}</figcaption><img src="{svg(cap)}"></figure>'
    for cap in ("close-toast-118", "close-toast-80", "close-toast-m-together",
                "close-toast-m-flag", "close-project-editor", "close-kanban-before"))

QS = [
    ("PV-612", "El toast del movimiento (118 columnas)",
     "«Audit dependencies due Oct 9 (+1d) · pushed Add push, Offline sync +1d each · "
     "u undo · m change for this move». Nombra lo que se movió, dice cuánto, ofrece u y m.",
     [("accept", "Aceptar"), ("names", "Prefiero solo el conteo («pushed 2 +1d each» siempre)")]),
    ("PV-613", "El ciclo de `m` (together → flag)",
     "Tras «+», `m` re-aplica el movimiento bajo together (el hito tm5 se mueve: «moved … "
     "Mobile +1d past ◆»); otro `m` lo re-aplica bajo flag (nada más se mueve: «flagged …»).",
     [("accept", "Aceptar"), ("arm", "Preferiría que `m` arme el MODO de la próxima jugada, no re-aplicar")]),
    ("PV-614", "El toast a 80 columnas",
     "«pushed 2 +1d each · u undo · m change» — sin nombres, solo el conteo.",
     [("accept", "Aceptar"), ("always-names", "Quiero nombres aunque no quepan")]),
    ("PV-615", "El select «Linked dates» en el editor de proyectos",
     "stay/push/together vive FUERA de la grilla pinneada del modal (la grilla tiene su censo "
     "propio) y es la reubicación de la regla por cadena que aprobaste en el mapa de cadenas (C-2).",
     [("accept", "Aceptar la ubicación"), ("inside", "Moverlo dentro de la grilla (costaría renegociar el censo TC-411)")]),
    ("UXV-6", "La regla se ve antes de mover",
     "Hoy la regla del proyecto solo se ve en el editor de proyectos; el mapa de cadenas (donde "
     "la viste en el prototipo) sigue siendo batch C.",
     [("accept", "Aceptar (batch C lo mostrará)"), ("soon", "Quiero ver la regla activa antes de la próxima versión")]),
]

blocks = "".join(
    f'''<section><h3>{qid} — {title}</h3><p>{desc}</p>
    {''.join(f'<label><input type="radio" name="{qid}" value="{val}"> {label}</label><br>' for val, label in opts)}
    </section>'''
    for qid, title, desc, opts in QS)

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Veredicto visual — taskboard — B2b (moving linked dates)</title>
<style>
body{{font-family:system-ui;margin:2rem auto;max-width:960px;color:#e6edf3;background:#0d1117}}
figure{{margin:1rem 0}}figcaption{{color:#8b98a5;font-size:.85rem;margin-bottom:.3rem}}
img{{max-width:100%;border:1px solid #30363d;border-radius:6px;background:#000}}
section{{border-top:1px solid #30363d;padding:1rem 0}}h3{{margin:.2rem 0}}
button{{font-size:1rem;padding:.6rem 1.2rem;border-radius:6px;border:0;background:#2dd4bf;color:#0d1117;font-weight:600;cursor:pointer}}
</style></head><body>
<h1>Veredicto visual — batch B2b: «mover fechas mueve lo que espera»</h1>
<p>Las capturas son del árbol de cierre (2509 tests + 13 pines). Responde y pulsa
<strong>Descargar veredicto</strong>; pasa el JSON a la sesión del coordinador.</p>
{FRAMES}
{blocks}
<button onclick="download()">Descargar veredicto</button>
<script>
function download() {{
  const answers = {{}};
  document.querySelectorAll('section').forEach(s => {{
    const id = s.querySelector('h3').textContent.split(' ')[0];
    const pick = s.querySelector('input:checked');
    answers[id] = {{choice: pick ? pick.value : "", label: pick ? pick.nextSibling.textContent.trim() : "", note: ""}};
  }});
  const blob = new Blob([JSON.stringify({{batch: "2026-10-06-batch-01", exported: new Date().toISOString(), answers}}, null, 2)],
    {{type: "application/json"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "taskboard-veredicto-b2b.json";
  a.click();
}}
</script></body></html>"""

OUT.write_text(HTML, encoding="utf-8")
print("sheet:", OUT)

"""Build the verdict page (html-report-round.html) for the HTML-report round.

Embeds the 12 variant screenshots from out/ as base64 data URIs so the page
is fully self-contained (zero external requests). Prose is Spanish; the page
is what the operator reads to give his verdict.

Usage:  python prototypes/html_report/verdict/build.py
"""
from __future__ import annotations

import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"
DEST = ROOT / "html-report-round.html"

VARIANTS = ("a", "b", "c")


def data_uri(png: Path) -> str:
    b64 = base64.b64encode(png.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def shots(variant: str) -> dict[str, str]:
    return {
        f"{variant}-{name}": data_uri(OUT / f"{variant}-{name}.png")
        for name in ("desktop-light", "desktop-dark",
                     "phone-light", "phone-dark")
    }


# --- Spanish content -------------------------------------------------------

BLUF = (
    "Recomendación: la variante B (espacio de trabajo interactivo) es la que "
    "mejor responde al dolor original: el export SVG era una foto de celdas de "
    "texto que no se podía usar ni manipular, y B entrega los mismos datos "
    "como datos — filtra, ordena, busca y descarga CSV/JSON para reutilizarlos. "
    "Las tres variantes funcionan y se sostienen solas, pero A informa sin "
    "manipular y C sólo rehace la presentación que ya existe."
)

BLUF_LINE = (
    "En una línea: elegir B, con la tecla H global (fuera de R), exportando "
    "todos los boards cargados, y el HTML conviviendo con el SVG de la "
    "presentación, que sigue siendo útil para proyectar."
)

VARIANT_HTML = {
    "a": """
<h2>Variante A — Status de reunión (one-pager cruzando boards)</h2>
<div class="cols">
  <div class="card">
    <h3>Qué es</h3>
    <p>Documento de estado que lee a través de los tres boards (Personal,
    Client A, Course): fichas de resumen, qué se movió en los últimos 7 días,
    atrasados y próximos 7 días, hitos por clase (Delivery ▲ / Billing ■ /
    Launch ★), cadenas de dependencia y progreso por proyecto. Cero
    JavaScript: se lee y se imprime en 2 páginas A4.</p>
    <h3>Propuesta de exportación</h3>
    <ul>
      <li><b>Tecla:</b> <code>H</code>, <b>global</b> (fuera de R, desde
      cualquier vista).</li>
      <li><b>Alcance:</b> <b>todos los boards cargados</b> — el status de
      reunión se lee cruzando boards.</li>
      <li><b>Dónde cae:</b> <code>reports/status-YYYY-MM-DD.html</code> junto
      al board activo. Toast: «Report written: reports/status-…html ·
      <code>o</code> opens it», y <code>o</code> abre el último reporte.</li>
      <li><b>¿Sustituye al SVG?</b> <b>Convive</b>: el SVG es una imagen de la
      vista curada para proyectar; este HTML es un documento de datos para
      leer e imprimir.</li>
    </ul>
    <h3>Si eliges esta, pasa esto…</h3>
    <p>Tu queja era que el SVG no se podía usar ni manipular. A se lee muy
    bien en la reunión e imprime limpio, pero sigue siendo un documento
    estático: no puedes filtrarlo, buscar en profundidad ni llevarte los
    datos a otra herramienta — el «manipular» queda igual de cerrado que con
    el SVG, sólo que más bonito y legible.</p>
    <h3>Recomendación</h3>
    <p>Buena pieza de reuniones, pero no resuelve el dolor de fondo. Úsala
    como complemento de impresión si el equipo la pide, no como respuesta a
    la queja del SVG.</p>
  </div>
  <div class="card shots">
    <h3>Capturas</h3>
    <figure><img src="{{a-desktop-light}}" alt="Variante A, escritorio, tema claro">
      <figcaption>Escritorio · claro</figcaption></figure>
    <figure><img src="{{a-desktop-dark}}" alt="Variante A, escritorio, tema oscuro">
      <figcaption>Escritorio · oscuro</figcaption></figure>
    <figure class="phone"><img src="{{a-phone-light}}" alt="Variante A, teléfono, tema claro">
      <figcaption>Teléfono · claro</figcaption></figure>
    <figure class="phone"><img src="{{a-phone-dark}}" alt="Variante A, teléfono, tema oscuro">
      <figcaption>Teléfono · oscuro</figcaption></figure>
    <p class="open"><a href="out/a-report.html">Abrir el reporte real
    (out/a-report.html) ↗</a></p>
  </div>
</div>
<div class="control">
  <label><input type="checkbox" id="choose-a"> <b>Elijo esta</b></label>
  <textarea id="obj-a" rows="2" placeholder="Objeción / pero…"></textarea>
</div>
""",
    "b": """
<h2>Variante B — Espacio de trabajo interactivo</h2>
<div class="cols">
  <div class="card">
    <h3>Qué es</h3>
    <p>Reporte autocontenido e interactivo: gantt de todas las tareas (zoom
    fit/día/semana/mes, tooltip, clic abre la ficha de la tarea), filtros por
    board, proyecto, persona, clase de milestone y estado, buscador, tabla
    ordenable, notas con ==!!++ y @menciones, y los datos embebidos como JSON
    con botones <i>Download CSV / JSON</i>. Todo con JS vanilla inline.</p>
    <h3>Propuesta de exportación</h3>
    <ul>
      <li><b>Tecla:</b> <code>H</code> (mayúscula), <b>global</b>
      (<code>bar=False</code>, como R, S, A), nombrada en <code>?</code> y en
      la paleta.</li>
      <li><b>Alcance:</b> <b>todos los boards cargados</b> — cada proyecto,
      cada tarea (incluidos archivados), la gente y las clases.</li>
      <li><b>Dónde cae:</b> <code>reports/workspace-YYYY-MM-DD.html</code> en
      la carpeta del board, misma convención que <code>report.py</code>.
      Toast: «Report written: workspace-…html — o opens it».</li>
      <li><b>¿Sustituye al SVG?</b> <b>Convive</b> con el SVG de R (pixels
      vs. datos); lo que sí deja obsoleto es el reporte CLI estático de
      <code>report.py</code>.</li>
    </ul>
    <h3>Si eliges esta, pasa esto…</h3>
    <p>Es la respuesta directa a tu queja: el «manipular» que el SVG no
    permitía aquí es real — filtras por persona o clase, ordenas la tabla,
    buscas texto y te llevas todo a Excel o a otra herramienta con un clic.
    El coste: el archivo pesa más, depende de JavaScript, y en boards muy
    grandes hará falta virtualización para no ir lento.</p>
    <h3>Recomendación</h3>
    <p>Es la recomendada. Es la única de las tres que convierte el export en
    una herramienta de trabajo y deja los datos reutilizables, que era el
    fondo de la queja.</p>
  </div>
  <div class="card shots">
    <h3>Capturas</h3>
    <figure><img src="{{b-desktop-light}}" alt="Variante B, escritorio, tema claro">
      <figcaption>Escritorio · claro</figcaption></figure>
    <figure><img src="{{b-desktop-dark}}" alt="Variante B, escritorio, tema oscuro">
      <figcaption>Escritorio · oscuro</figcaption></figure>
    <figure class="phone"><img src="{{b-phone-light}}" alt="Variante B, teléfono, tema claro">
      <figcaption>Teléfono · claro</figcaption></figure>
    <figure class="phone"><img src="{{b-phone-dark}}" alt="Variante B, teléfono, tema oscuro">
      <figcaption>Teléfono · oscuro</figcaption></figure>
    <p class="open"><a href="out/b-report.html">Abrir el reporte real
    (out/b-report.html) ↗</a></p>
  </div>
</div>
<div class="control">
  <label><input type="checkbox" id="choose-b"> <b>Elijo esta</b></label>
  <textarea id="obj-b" rows="2" placeholder="Objeción / pero…"></textarea>
</div>
""",
    "c": """
<h2>Variante C — Deck de presentación en HTML vectorial</h2>
<div class="cols">
  <div class="card">
    <h3>Qué es</h3>
    <p>La presentación (R) reconstruida como deck HTML: portada, vista
    «all» y una diapositiva por proyecto, con gantt SVG de texto real y
    seleccionable, hitos con su clase, flechas de dependencia, regla de
    «today» y notas con ==!!++ y @menciones. Se navega con ← → (y botones
    con contador para el teléfono) e imprime una diapositiva por página.</p>
    <h3>Propuesta de exportación</h3>
    <ul>
      <li><b>Tecla:</b> <code>H</code> (mayúscula), <b>dentro de R</b> — el
      <code>h</code> global ya es «izquierda», pero <code>H</code> mayúscula
      está libre en ambos mundos.</li>
      <li><b>Alcance:</b> el <b>tablero actual tal como la presentación lo
      muestra</b> — respeta la curaduría (lo oculto con ␣ no sale).</li>
      <li><b>Dónde cae:</b> <code>reports/&lt;slug&gt;-&lt;fecha&gt;-deck.html</code>
      junto al tablero, como <code>present_paths</code>. Toast: «Exported
      …-deck.html to …\reports · o opens it».</li>
      <li><b>¿Sustituye al SVG?</b> <b>Reemplaza</b>: propone que
      <code>x</code> pase a escribir el deck y muera el PNG, que hoy además
      exige Edge.</li>
    </ul>
    <h3>Si eliges esta, pasa esto…</h3>
    <p>Resuelve el «manipular» sólo para la presentación: el texto ya se
    puede seleccionar, buscar y copiar, e imprime mejor que el PNG. Pero fuera
    de esa vista curada no filtra, no ordena, no descarga datos — si tu dolor
    era trabajar con la información del tablero, esta variante te deja igual
    de mano atada que antes, con mejor tipografía.</p>
    <h3>Recomendación</h3>
    <p>La idea de reemplazar el PNG de <code>x</code> por un deck vectorial es
    sólida y probablemente merezca implementarse, pero es una mejora de la
    presentación, no la respuesta al pedido de un reporte manipulable.</p>
  </div>
  <div class="card shots">
    <h3>Capturas</h3>
    <figure><img src="{{c-desktop-light}}" alt="Variante C, escritorio, tema claro">
      <figcaption>Escritorio · claro</figcaption></figure>
    <figure><img src="{{c-desktop-dark}}" alt="Variante C, escritorio, tema oscuro">
      <figcaption>Escritorio · oscuro</figcaption></figure>
    <figure class="phone"><img src="{{c-phone-light}}" alt="Variante C, teléfono, tema claro">
      <figcaption>Teléfono · claro</figcaption></figure>
    <figure class="phone"><img src="{{c-phone-dark}}" alt="Variante C, teléfono, tema oscuro">
      <figcaption>Teléfono · oscuro</figcaption></figure>
    <p class="open"><a href="out/c-report.html">Abrir el reporte real
    (out/c-report.html) ↗</a></p>
  </div>
</div>
<div class="control">
  <label><input type="checkbox" id="choose-c"> <b>Elijo esta</b></label>
  <textarea id="obj-c" rows="2" placeholder="Objeción / pero…"></textarea>
</div>
""",
}

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ronda de prototipos — reporte HTML · veredicto</title>
<style>
:root {{
  --bg: #f6f7f9; --fg: #1c2430; --muted: #5b6675; --card: #ffffff;
  --line: #d9dee5; --accent: #1f6feb; --accent-fg: #ffffff;
  --bluf-bg: #eaf2ff; --bluf-line: #b6d3ff; --mark: #fff4d6;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #11151b; --fg: #e3e8ef; --muted: #9aa6b4; --card: #1a212b;
    --line: #2c3542; --accent: #4d8dff; --accent-fg: #0d1117;
    --bluf-bg: #16283f; --bluf-line: #2c4a75; --mark: #3a2f14;
  }}
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  background: var(--bg); color: var(--fg);
  font: 16px/1.55 system-ui, "Segoe UI", sans-serif;
}}
main {{ max-width: 1080px; margin: 0 auto; padding: 24px 16px 64px; }}
h1 {{ font-size: 1.6rem; margin: 8px 0 4px; }}
.sub {{ color: var(--muted); margin: 0 0 20px; }}
.bluf {{
  background: var(--bluf-bg); border: 1px solid var(--bluf-line);
  border-radius: 10px; padding: 14px 18px; margin-bottom: 28px;
}}
.bluf p {{ margin: 6px 0; }}
.oneline {{ font-weight: 600; }}
h2 {{
  font-size: 1.3rem; margin: 34px 0 10px;
  padding-top: 18px; border-top: 2px solid var(--line);
}}
h3 {{
  font-size: 0.95rem; text-transform: uppercase; letter-spacing: .04em;
  color: var(--muted); margin: 16px 0 6px;
}}
.cols {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
  align-items: start;
}}
.card {{
  background: var(--card); border: 1px solid var(--line);
  border-radius: 10px; padding: 6px 16px 14px;
}}
.card p, .card ul {{ margin: 6px 0; }}
.card ul {{ padding-left: 20px; }}
code {{
  background: var(--mark); border-radius: 4px; padding: 0 4px;
  font-size: 0.9em;
}}
.shots figure {{ margin: 10px 0; }}
.shots img {{
  width: 100%; height: auto; display: block;
  border: 1px solid var(--line); border-radius: 8px;
}}
.shots figcaption {{ color: var(--muted); font-size: 0.85rem; margin-top: 2px; }}
.open a {{ color: var(--accent); font-weight: 600; }}
.control {{
  background: var(--card); border: 1px solid var(--line);
  border-radius: 10px; padding: 12px 16px; margin-top: 12px;
}}
.control label {{ display: block; margin-bottom: 8px; cursor: pointer; }}
textarea {{
  width: 100%; resize: vertical; font: inherit; color: inherit;
  background: var(--bg); border: 1px solid var(--line);
  border-radius: 8px; padding: 8px 10px;
}}
.general {{ margin-top: 34px; border-top: 2px solid var(--line); padding-top: 18px; }}
.export-row {{ margin-top: 18px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }}
button {{
  font: inherit; font-weight: 600; cursor: pointer;
  background: var(--accent); color: var(--accent-fg);
  border: 0; border-radius: 8px; padding: 10px 18px;
}}
.hint {{ color: var(--muted); font-size: 0.9rem; }}
@media (max-width: 760px) {{
  .cols {{ grid-template-columns: 1fr; }}
  h1 {{ font-size: 1.3rem; }}
}}
</style>
</head>
<body>
<main>
  <h1>Reporte HTML exportado de la app — ronda de prototipos</h1>
  <p class="sub">Tres variantes (A, B, C) generadas desde un tablero sintético
  (boards «Personal», «Client A», «Course»). Marca tu elección por variante,
  deja objeciones y pulsa «Exportar respuestas» para copiar tu veredicto.</p>

  <div class="bluf">
    <p><b>BLUF.</b> {bluf}</p>
    <p class="oneline">{oneline}</p>
  </div>

{variants}

  <section class="general">
    <h2>Bloque general — la recomendación de la ronda</h2>
    <p>Resumen de lo propuesto: elegir la <b>variante B</b> como reporte HTML
    principal, con la tecla <code>H</code> <b>global</b> (fuera de R),
    exportando <b>todos los boards cargados</b>, dejando el HTML
    <b>conviviendo</b> con el SVG de la presentación (que sigue sirviendo
    para proyectar). La idea de la variante C de reemplazar el PNG de
    <code>x</code> por un deck vectorial puede avanzar después como mejora
    independiente de R.</p>
    <div class="control">
      <label><input type="checkbox" id="choose-general"> <b>Elijo esta</b>
      (confirmo la recomendación general)</label>
      <textarea id="obj-general" rows="2" placeholder="Objeción / pero…"></textarea>
    </div>
    <h3>Notas generales</h3>
    <textarea id="notes" rows="5"
      placeholder="Notas generales — lo que quieras agregar fuera de las objeciones"></textarea>
    <div class="export-row">
      <button id="export" type="button">Exportar respuestas</button>
      <span class="hint">Copia al portapapeles el veredicto en texto plano y
      en JSON.</span>
    </div>
  </section>
</main>
<script>
(function () {{
  var VARIANTS = ["a", "b", "c"];

  function collect() {{
    var answers = VARIANTS.map(function (v) {{
      return {{
        variant: v,
        chosen: document.getElementById("choose-" + v).checked,
        objection: document.getElementById("obj-" + v).value.trim()
      }};
    }});
    return {{
      round: "html-report",
      date: new Date().toISOString().slice(0, 10),
      general: {{
        chosen: document.getElementById("choose-general").checked,
        objection: document.getElementById("obj-general").value.trim()
      }},
      notes: document.getElementById("notes").value.trim(),
      variants: answers
    }};
  }}

  function toText(d) {{
    var lines = [
      "Veredicto — ronda de prototipos del reporte HTML",
      "Fecha: " + d.date, ""
    ];
    d.variants.forEach(function (v) {{
      lines.push("Variante " + v.variant.toUpperCase() + ": " +
        (v.chosen ? "ELEGIDA" : "no elegida"));
      if (v.objection) lines.push("  Objeción: " + v.objection);
    }});
    lines.push("");
    lines.push("Recomendación general (B, H global, todos los boards, " +
      "convive con SVG): " + (d.general.chosen ? "CONFIRMADA" : "no confirmada"));
    if (d.general.objection) lines.push("  Objeción: " + d.general.objection);
    if (d.notes) lines.push("", "Notas generales: " + d.notes);
    return lines.join("\\n");
  }}

  function toJson(d) {{ return JSON.stringify(d, null, 2); }}

  function copy(text) {{
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      return navigator.clipboard.writeText(text);
    }}
    return new Promise(function (resolve, reject) {{
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {{
        if (document.execCommand("copy")) resolve();
        else reject(new Error("execCommand copy failed"));
      }} catch (e) {{ reject(e); }}
      document.body.removeChild(ta);
    }});
  }}

  document.getElementById("export").addEventListener("click", function () {{
    var btn = this;
    var d = collect();
    var text = toText(d) + "\\n\\n--- JSON ---\\n" + toJson(d);
    copy(text).then(function () {{
      btn.textContent = "Copiado ✓";
      setTimeout(function () {{ btn.textContent = "Exportar respuestas"; }}, 2000);
    }}).catch(function () {{
      btn.textContent = "No se pudo copiar";
      setTimeout(function () {{ btn.textContent = "Exportar respuestas"; }}, 2000);
    }});
  }});
}})();
</script>
</body>
</html>
"""


def main() -> None:
    uris: dict[str, str] = {}
    for v in VARIANTS:
        uris.update(shots(v))
    body_parts = []
    for v in VARIANTS:
        chunk = VARIANT_HTML[v]
        for key, uri in uris.items():
            chunk = chunk.replace("{{%s}}" % key, uri)
        body_parts.append(chunk)
    html = PAGE.format(bluf=BLUF, oneline=BLUF_LINE, variants="\n".join(body_parts))
    DEST.write_text(html, encoding="utf-8")
    print(f"wrote {DEST} ({DEST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

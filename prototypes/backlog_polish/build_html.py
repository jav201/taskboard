"""Build the verdict page from the app captures (PNGs embedded as base64).

    python prototypes/backlog_polish/capture.py
    python prototypes/backlog_polish/build_html.py

Prose in Spanish (the operator's), UI in English (the app's). One section per
polish item: the current look and its variants side by side at 118×31 and
80×25, the contrast ratios measured from the app's own tones, and one
recommendation marked `data-recommend="<capture id>"`; a last section shows
the narrow frame and hint that increment 002 shipped, for review.
"""
from __future__ import annotations

import base64
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
OUT = HERE / "out"
PAGE = HERE / "backlog-polish-prototype.html"

from taskboard.views import HEX  # noqa: E402

BG = "#0d1117"


def _lum(hex_: str) -> float:
    def ch(v: int) -> float:
        c = v / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(fg: str, bg: str = BG) -> float:
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


LOOK_NAMES = {
    "contrast": {"current": f"actual · dim {HEX['dim']} · {ratio(HEX['dim']):.1f}:1",
                 "A": f"A · reached {HEX['reached']} · {ratio(HEX['reached']):.1f}:1",
                 "B": f"B · mut {HEX['mut']} · {ratio(HEX['mut']):.1f}:1"},
    "hint80": {"current": "actual · la corta de hoy", "A": "A · intermedia con «next» y «show all»",
               "B": "B · sin separadores «·»"},
    "notecap": {"current": "actual · 3 filas", "A": "A · llena las filas libres", "B": "B · 6 filas"},
    "narrow": {"current": "lo que ya se implementó (incremento 002)"},
}
SCENE_NAMES = {"gantt-long": "gantt · nota larga bajo el cursor",
               "split-long": "split · nota larga bajo el cursor",
               "gantt": "gantt · ninguna tarea oculta", "split": "split · ninguna tarea oculta",
               "gantt-hidden": "gantt · 1 tarea oculta",
               "gantt-short": "gantt · nota de 3 párrafos",
               "narrow-30x12": "30 × 12 · el marco angosto",
               "narrow-20x12": "20 × 12 · el escalón siguiente",
               "narrow-50x20-hidden": "50 × 20 · la pista compacta, 1 oculta"}

ITEMS = [
    ("contrast", "1 · La palabra de la vista y las marcas de corte",
     "<p>En la cabecera, la palabra <code>gantt</code> / <code>split</code> y las marcas que declaran "
     "un corte (<code>… +N lines</code>, <code>↓ N more lines</code>, <code>↑ N lines above</code>) van "
     "en <code>dim</code>: cerca de 3:1 sobre el fondo. En una pantalla compartida o un proyector "
     "pueden perderse (UX4-2 del walkthrough de P4). Las variantes solo repintan esas marcas; el resto "
     "del <code>dim</code> (la retícula, <code>no notes</code>) queda igual.</p>",
     "contrast-A-gantt-long-118x31",
     "<p><strong>Recomiendo A (<code>reached</code>).</strong> Supera 4.5:1, el mínimo de lectura de "
     "texto, y sigue siendo más callado que <code>mut</code>, así que la palabra de la vista y los "
     "cortes no compiten con los títulos ni con las fechas. B se lee mejor aún, pero empareja las "
     "marcas con el texto secundario y se pierde la jerarquía.</p>"),
    ("hint80", "2 · La pista a 80 columnas",
     "<p>A 80 columnas la fila de teclas cae a la versión corta (<code>⇥ · ←→ · ␣ hide · a all</code>) "
     "aunque sobran ~20 celdas (UX4-3). Las variantes agregan una redacción intermedia que se prueba "
     "después de la larga; a 118 columnas no cambia nada (la larga cabe). Con una sola tarea oculta el conteo "
     "<code>· 1 hidden</code> ya no deja sitio y las tres vuelven a la corta (tercera escena).</p>",
     "hint80-A-gantt-80x25",
     "<p><strong>Recomiendo A.</strong> Recupera <code>next</code> y <code>show all</code>, que son las "
     "dos teclas que alguien que presenta por primera vez no adivina, sin cambiar el vocabulario ni el "
     "orden de la larga. B cabe en más casos pero, sin los <code>·</code>, los grupos de teclas se "
     "funden y se leen peor de un vistazo.</p>"),
    ("notecap", "3 · El tope de 3 filas de la nota en la vista gantt",
     "<p>La vista gantt muestra la nota de la tarea del cursor en 3 filas aunque abajo queden de 6 "
     "(80×25) a 11 (118×31) filas vacías (UX4-4). La vista <code>2</code> ya muestra la nota "
     "completa. A llena las filas libres (el corte se sigue declarando); B sube el tope a 6.</p>",
     "notecap-A-gantt-long-118x31",
     "<p><strong>Recomiendo A.</strong> Usa el espacio que hoy se pierde y se adapta solo al tamaño "
     "de la terminal; si la nota no cabe, la marca <code>… +N lines</code> lo sigue diciendo. B es un "
     "número fijo que a 118×31 todavía deja filas vacías.</p>"),
]


def _same_as_current(entry: dict) -> bool:
    """A variant capture byte-equal (ids aside) to the current look's at the
    same scene and size — it is labelled, never passed off as a difference."""
    if entry["look"] == "current" or entry["item"] == "narrow":
        return False
    cur = OUT / f"{entry['item']}-current-{entry['scene']}-{entry['size']}.svg"
    norm = lambda p: re.sub(r"terminal-\d+", "terminal-N", p.read_text(encoding="utf-8"))  # noqa: E731
    return norm(cur) == norm(OUT / entry["svg"])


def _img(entry: dict) -> str:
    data = base64.b64encode((OUT / entry["png"]).read_bytes()).decode()
    same = _same_as_current(entry)
    cap = html.escape(f"{LOOK_NAMES[entry['item']][entry['look']]} · {entry['size']}"
                      + (" · = actual (aquí no cambia nada)" if same else ""))
    mark = ' data-same="current"' if same else ""
    return (f'<figure id="{entry["id"]}" data-capture="{entry["id"]}" data-svg="{entry["svg"]}"{mark}>'
            f'<figcaption>{cap}</figcaption>'
            f'<img alt="{cap}" src="data:image/png;base64,{data}"></figure>')


def main() -> None:
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    by_item: dict[str, list[dict]] = {}
    for e in manifest:
        by_item.setdefault(e["item"], []).append(e)
    sections = []
    for item, title, intro, rec_id, rec in ITEMS:
        entries = by_item[item]
        rows = []
        for scene in dict.fromkeys(e["scene"] for e in entries):
            for size in ("118x31", "80x25"):
                cells = [e for e in entries if e["scene"] == scene and e["size"] == size]
                rows.append(f'<h4>{html.escape(SCENE_NAMES[scene])} · {size.replace("x", " × ")}</h4>'
                            f'<div class="row">{"".join(_img(e) for e in cells)}</div>')
        sections.append(f'<section id="{item}" data-item="{item}" data-recommend="{rec_id}">'
                        f'<h2>{title}</h2>{intro}{"".join(rows)}'
                        f'<div class="rec">{rec}<p class="small">Captura recomendada: '
                        f'<a href="#{rec_id}"><code>{rec_id}</code></a></p></div></section>')
    narrow = "".join(f'<h4>{html.escape(SCENE_NAMES[e["scene"]])}</h4><div class="row">{_img(e)}</div>'
                     for e in by_item["narrow"])
    sections.append(
        '<section id="narrow" data-item="narrow"><h2>4 · Para revisar: la presentación angosta</h2>'
        "<p>Esto ya se implementó en el incremento 002 (el encargo lo clasificó como arreglo, no como "
        "diseño): por debajo de 36 columnas el marco dice cuánto debe medir — el escalón más largo que "
        "cabe, de <code>widen to 36+ columns · esc leave</code> a <code>36+</code> —, ninguna tecla "
        "salvo <code>esc</code>/<code>q</code> hace nada y <code>x</code> avisa en vez de exportar; la "
        "pista se acorta en pasos y, si aun así no cabe, se corta con <code>…</code>. Se muestra para "
        "su visto bueno. Un detalle abierto (UX2-2): entre 32 y 35 columnas <code>esc leave</code> "
        "aparece dos veces, en el marco y en la pista. El aviso de <code>x</code> (<code>Widen the terminal to 36+ "
        "columns to export</code>) no sale en estas capturas: <code>export_screenshot</code> no pinta avisos sobre "
        "la presentación (tampoco el de exportar a 118 columnas); su texto lo verifica la prueba AT-1903.</p>" + narrow + "</section>")
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Backlog polish round</title>
<style>
:root {{ --bg:#f6f7f9; --fg:#1b1f24; --muted:#5b6675; --card:#ffffff; --line:#d5dae1; --accent:#0f8f80; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --fg:#e6edf3; --muted:#8b98a5; --card:#161b22; --line:#30363d; --accent:#2dd4bf; }} }}
body {{ margin:0; padding:24px 16px 64px; background:var(--bg); color:var(--fg); font:16px/1.55 system-ui, sans-serif; }}
main {{ max-width:1500px; margin:0 auto; }}
h1 {{ font-size:1.6rem; margin:0 0 .3rem; }} h2 {{ margin-top:2.6rem; border-top:1px solid var(--line); padding-top:1.4rem; }}
h4 {{ margin:1.4rem 0 .4rem; color:var(--muted); font-weight:600; }}
code {{ font-family: ui-monospace, Consolas, monospace; font-size:.92em; }}
.row {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:12px; }}
figure {{ margin:0; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:8px; }}
figure:target {{ outline:3px solid var(--accent); }}
figcaption {{ font-size:.85rem; color:var(--muted); margin-bottom:6px; }}
img {{ width:100%; height:auto; display:block; cursor:zoom-in; image-rendering:auto; }}
.rec {{ margin-top:1.2rem; padding:12px 16px; border-left:4px solid var(--accent); background:var(--card); border-radius:4px; }}
.small {{ font-size:.85rem; color:var(--muted); }}
#zoom {{ position:fixed; inset:0; background:rgba(0,0,0,.85); display:none; overflow:auto; cursor:zoom-out; z-index:9; }}
#zoom img {{ width:auto; max-width:none; margin:24px auto; cursor:zoom-out; }}
</style></head><body><main>
<h1>Ronda de prototipo · pulido del backlog</h1>
<p class="small">taskboard · batch 2026-10-18-batch-02 · capturas del app real (headless, <code>export_screenshot</code> → SVG → PNG con Edge) sobre el tablero sintético de notas, a 118 × 31 y 80 × 25. Nada de producción cambió por estas variantes: se aplican solo dentro del proceso de captura.</p>
<p>Tres puntos de pulido quedaron abiertos en el walkthrough de la presentación (P4 del batch anterior). Para cada uno: cómo se ve hoy, una o dos variantes y mi recomendación. Ninguno se implementa hasta su veredicto. Al final, la presentación angosta que sí se implementó, para su revisión. Clic en una captura para verla a tamaño completo.</p>
{''.join(sections)}
</main><div id="zoom"></div>
<script>
const z = document.getElementById('zoom');
document.querySelectorAll('figure img').forEach(i => i.addEventListener('click', () => {{
  z.innerHTML = ''; const c = i.cloneNode(); z.appendChild(c); z.style.display = 'block'; }}));
z.addEventListener('click', () => {{ z.style.display = 'none'; }});
</script></body></html>
"""
    PAGE.write_text(page, encoding="utf-8")
    print(PAGE.relative_to(ROOT).as_posix(), f"{len(page) // 1024} KB")


if __name__ == "__main__":
    main()

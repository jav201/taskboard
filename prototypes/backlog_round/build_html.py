"""THROWAWAY — build the verdict page of the backlog round from its captures.

    powershell -File prototypes/backlog_round/shoot.ps1      (real Windows Terminal PNGs)
    python prototypes/backlog_round/proto.py exports         (the export files, item 4)
    python prototypes/backlog_round/build_html.py

Every image is embedded (base64), so the page works opened alone. A missing
capture is printed on the page as missing — never replaced by an SVG.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "backlog-round.html"
SIZES = ("118x30", "80x24")
MISSING: list[str] = []
USED: set[str] = set()


def b64(path: Path) -> str | None:
    if not path.exists():
        MISSING.append(str(path.relative_to(HERE)))
        return None
    return base64.b64encode(path.read_bytes()).decode()


def shot(scene: str, folder: str = "png") -> str:
    """The real Windows Terminal PNG at both sizes (the size switch picks one)."""
    out = []
    for s in SIZES:
        USED.add(f"{scene}_{s}")
        data = b64(OUT / folder / f"{scene}_{s}.png")
        if data is None:
            out.append(f'<div class="miss sz sz-{s}">captura faltante: {scene} · {s}</div>')
        else:
            out.append(f'<img class="sz sz-{s}" alt="{scene} {s}" loading="lazy" '
                       f'src="data:image/png;base64,{data}">')
    return "".join(out)


def export_png(name: str) -> str:
    out = []
    for s in SIZES:
        data = b64(OUT / "export" / f"{name}_{s}.png")
        out.append(f'<div class="miss sz sz-{s}">export faltante: {name} · {s}</div>' if data is None
                   else f'<img class="sz sz-{s}" alt="{name} {s}" src="data:image/png;base64,{data}">')
    return "".join(out)


# (number, key, title, problem, [(value, label, scene|None, consequence)], recommendation, rec text)
ITEMS = [
    (1, "agenda", "Opción D · una agenda de todos los tableros",
     "Hoy no hay ninguna vista que junte tableros. La ronda multi-board la dejó como opción D, "
     "detrás de su propia tecla. <kbd>A</kbd> está libre en <code>taskboard/keymap.py</code> "
     "(se comprobó: ninguna <code>Key(\"A\"…)</code> en <code>KEYMAP</code>).",
     [("hoy", "Hoy · solo el inicio (B)", "ag-now",
       "Lo más cercano es el inicio: una tarjeta por tablero con sus próximas 1–3 fechas. Para saber "
       "qué vence hoy <em>en todos</em> los tableros, abres cada uno o lees cada tarjeta."),
      ("A", "A · Una lista en tres bandas", "ag-A",
       "Una sola lista de lo más urgente a lo menos: <strong>LATE</strong>, <strong>TODAY</strong>, "
       "<strong>REST OF THE WEEK</strong> (hasta el domingo). Cada fila: barra y nombre del tablero "
       "en su color, proyecto, tarea, fecha. <kbd>↑↓</kbd> y <kbd>↵</kbd> abre la tarea en su "
       "tablero. Consecuencia: en una pasada sabes qué hacer hoy, venga de donde venga; con muchas "
       "tareas la lista se desplaza; bajo 100 columnas se cae la columna del proyecto."),
      ("B", "B · La semana en columnas", "ag-B",
       "Una columna por día (LATE, TODAY, Wed … Sun), cada tarea una tarjeta de dos líneas en el "
       "color de su tablero; <kbd>←→</kbd> día, <kbd>↑↓</kbd> tarea. Consecuencia: ves qué día "
       "está cargado; pero a 118 columnas cada columna tiene ~16 celdas y los títulos se cortan "
       "(«Golden questi…»), a 80 se reduce a tres columnas y pierde el día exacto, y con pocas "
       "tareas casi toda la pantalla queda vacía."),
      ("C", "C · Un carril por tablero + el día elegido", "ag-C",
       "Arriba, un carril por tablero con un punto por vencimiento en cada día; abajo, las tareas "
       "del día elegido de todos los tableros. Consecuencia: ves de un vistazo qué tablero carga qué "
       "día (gana con 5+ tableros); pero para leer los títulos vas día por día: un paso más que A "
       "para la pregunta «¿qué hago hoy?»."),
      ],
     "A",
     "A responde la pregunta en una pasada y se ve igual a 80 columnas. Ojo con el hallazgo de "
     "abajo: saltar a otro tablero dejó la ventana real en negro, también sin el prototipo. La "
     "franja de puntos de C podría ser más adelante la cabecera de A. Al implementarlo, "
     "<kbd>A</kbd> entra en <code>KEYMAP</code> (sin barra, como <kbd>R</kbd>), así lo listan "
     "<kbd>?</kbd> y la paleta; en este prototipo es un binding aparte y la barra no lo muestra.",
     ["ag-A-open"]),
    (2, "chip", "El nombre del tablero en la presentación R",
     "Desde la batch de varios tableros, cada vista abre su fila de cabecera con el chip del "
     "tablero — menos <kbd>R</kbd>, que es lo que ve la sala.",
     [("hoy", "Hoy · sin chip", "pc-now",
       "La presentación no dice de qué tablero es. Ni el público ni la exportación lo ven; tú "
       "tampoco, si dudas en qué tablero abriste <kbd>R</kbd>."),
      ("B", "B · Chip discreto en la fila de teclas", "pc-B",
       "El chip va al inicio de la fila de teclas de abajo, la que solo mira quien presenta y que "
       "<kbd>x</kbd> nunca exporta. Consecuencia: sabes en qué tablero estás antes de proyectar; el "
       "marco, los PNG/SVG exportados y los oráculos de bytes de <kbd>R</kbd> quedan idénticos. "
       "A 80 columnas la pista pierde palabras (pasa a la redacción corta)."),
      ("C", "C · Chip en el marco (y en la exportación)", "pc-C",
       "El chip abre la cabecera del marco, como en las demás vistas. Consecuencia: lo ve la sala y "
       "entra en cada exportación — útil si presentas a ese cliente, una fuga si el nombre es "
       "interno («Personal», «Main»). Cambian los marcos de oráculo de <kbd>R</kbd>."),
      ],
     "B",
     "B te da la información a ti sin cambiar lo que ve la sala ni lo que se exporta. Si algún día "
     "quieres el nombre en la diapositiva, C es un cambio aparte y explícito.", []),
    (3, "help", "<kbd>?</kbd> dentro de la presentación",
     "Las teclas de <kbd>R</kbd> (vista 3 y <kbd>u</kbd> incluidas) solo viven en su fila de pistas; "
     "a 80 columnas son solo glifos. <kbd>?</kbd> no llega dentro de <kbd>R</kbd>.",
     [("hoy", "Hoy · ? no hace nada", "ph-now",
       "Captura: vista 3, se pulsó <kbd>?</kbd> y no cambió nada. Lo único es la pista de abajo, "
       "recortada a «⇥ · ↑↓ · ←→ rail · ␣ hide · ⇧↑↓ order …»."),
      ("A", "A · Ventana de teclas", "ph-A",
       "<kbd>?</kbd> abre una ventana con todas las teclas de la presentación en cuatro grupos "
       "(VIEWS · MOVE · CURATE · OUT); las que valen en la vista actual en claro, las de otra vista "
       "atenuadas con su vista entre paréntesis. La pista gana «? keys». Consecuencia: igual que "
       "<kbd>?</kbd> en el resto de la app; tapa el marco mientras está abierta (nunca se exporta)."),
      ("B", "B · Hoja de teclas bajo el marco", "ph-B",
       "<kbd>?</kbd> cambia la fila de pistas por una hoja de 5–6 filas con las teclas en palabras. "
       "Consecuencia: ves teclas y marco a la vez; el marco pierde esas filas mientras está abierta "
       "(a 80×24 la vista 3 se queda con ~18 filas y empuja proyectos a «+N more rows»)."),
      ],
     "A",
     "A es el mismo gesto que en toda la app y no le quita filas al marco. Necesita un asiento de "
     "teclas para la presentación (hoy sus teclas viven fuera de <code>KEYMAP</code>); la ventana "
     "se puede generar de ese asiento, como la barra.", []),
    (4, "export", "La exportación <code>-all</code> sin el cursor, cortada a su contenido",
     "<kbd>x</kbd> en la vista 3 escribe SVG + PNG del timeline. Abajo, los archivos reales que "
     "escribe la app (su propio rasterizador con Edge), no capturas de pantalla.",
     [("hoy", "Hoy · con el cursor y filas vacías", None,
       "La exportación lleva la marca <code>⟦</code> delante del proyecto del cursor, la fila "
       "«project span ▸» que repite su tramo, y filas vacías hasta el alto de la terminal: 29 filas "
       "a 118×30 para 21 de contenido. Se nota que es una captura de tu pantalla."),
      ("limpia", "Limpia · sin cursor, cortada", None,
       "El mismo timeline sin cursor (la regla muestra las semanas en vez del eco del proyecto) y "
       "cortado a su contenido: 21 filas. Consecuencia: el PNG se lee como una diapositiva; lo "
       "exportado deja de ser idéntico a lo que ves (la pantalla sigue con cursor)."),
      ],
     "limpia",
     "La exportación es para otra gente; el cursor solo le sirve a quien presenta. La regla del "
     "corte: quitar las filas en blanco del final, nunca filas con contenido.", ["ex-now"]),
    (5, "reorder", "Una segunda tecla para reordenar proyectos",
     "En la vista 3, <kbd>shift+↑/↓</kbd> es la única forma de mover un proyecto; algunos "
     "terminales y multiplexores no pasan shift+flecha.",
     [("hoy", "Hoy · solo ⇧↑↓", "ro-now",
       "Si tu terminal no pasa <kbd>shift+↑</kbd>, reordenar no existe para ti y nada lo dice."),
      ("A", "A · K / J además de ⇧↑↓", "ro-A",
       "<kbd>K</kbd> / <kbd>J</kbd> (shift+k, shift+j) hacen lo mismo. Son letras — todo terminal las "
       "pasa — y siguen la pareja <kbd>k</kbd>/<kbd>j</kbd> = <kbd>↑</kbd>/<kbd>↓</kbd> que la "
       "presentación ya acepta; están libres en la app y en <kbd>R</kbd>. La pista dice «⇧↑↓/K J "
       "reorder» (larga) o «K J order» (media, la de 118). Abajo: tras <kbd>↓</kbd> y <kbd>K</kbd>, "
       "Eval harness sube al primer lugar."),
      ],
     "A",
     "Descarté <kbd>[</kbd>/<kbd>]</kbd>: en la pantalla principal son Phase−/Phase+ (mover de "
     "fase), y la misma tecla con dos sentidos confunde.", ["ro-A-moved"]),
    (6, "confirm", "ConfirmModal: confirmar con el teclado",
     "La confirmación (borrar un proyecto, archivar un tablero) abre con el foco en la caja: "
     "confirmar es <kbd>tab</kbd>, <kbd>enter</kbd>, y nada lo dice.",
     [("hoy", "Hoy · foco en la caja, sin pista", "cf-now",
       "<kbd>enter</kbd> no hace nada; hay que adivinar <kbd>tab</kbd>. <kbd>esc</kbd> cancela. "
       "<strong>Hallazgo de la captura:</strong> el mensaje se corta en una línea («…its folder is "
       "not») — la mitad que dice cómo recuperar el tablero no se ve."),
      ("A", "A · Foco en el botón de confirmar", "cf-A",
       "<kbd>enter</kbd> confirma en el acto. Consecuencia: más rápido, pero un <kbd>enter</kbd> "
       "de más borra un proyecto sin pensar — esta misma caja confirma borrados."),
      ("B", "B · y / n y una línea que lo dice", "cf-B",
       "<kbd>y</kbd> confirma, <kbd>n</kbd>/<kbd>esc</kbd> cancelan, y una línea lo dice: "
       "«y archive  n / esc cancel  ⇥ the buttons». El foco sigue en la caja: un <kbd>enter</kbd> "
       "suelto sigue sin hacer nada. Consecuencia: una tecla, escrita en pantalla."),
      ],
     "B",
     "B es explícito y no abre la puerta al <kbd>enter</kbd> accidental. El mensaje cortado es un "
     "defecto aparte (que la caja ajuste el texto en varias líneas): lo propongo como entrada nueva "
     "del backlog.", []),
    (7, "startup", "Los modales de arranque no dicen a qué tablero responden",
     "Con más de un tablero, el arranque abre el inicio y encima los modales del tablero que se "
     "abrió (la oferta de hitos, el selector de identidad del modo equipo).",
     [("hoy", "Hoy · sin nombre", "su-now-offer",
       "La oferta de hitos no dice de qué tablero son esas tareas. <strong>Hallazgo de la captura "
       "real:</strong> el inicio no llega a dibujarse detrás (fondo vacío), así que no hay ninguna "
       "pista. El selector de identidad (abajo) igual."),
      ("A", "A · Chip del tablero en el título", "su-A-offer",
       "El mismo chip de la cabecera abre el título del modal. Consecuencia: sabes a qué tablero "
       "respondes antes de convertir nada; el modal no crece."),
      ("B", "B · El borde en el color del tablero", "su-B-offer",
       "Borde grueso en el color del tablero, «for board Client A» en el borde y «answers for this "
       "board only» abajo. Consecuencia: imposible no verlo; pero el borde de color es un lenguaje "
       "nuevo (en el inicio, el borde de color significa «cursor aquí»)."),
      ],
     "A",
     "A usa el chip que ya conoces. Vale para los dos modales.", ["su-now-id", "su-A-id", "su-B-id"]),
    (8, "twice", "Dos instancias en el mismo tablero",
     "Dos ventanas pueden tener abierto el mismo tablero; ambas escriben el mismo archivo y la "
     "última escritura gana. Otro agente añade el bloqueo; aquí solo el mensaje.",
     [("hoy", "Hoy · nada", "in-now", "Abres Client A dos veces y nada avisa."),
      ("A", "A · Un aviso al abrir", "in-A",
       "Al abrir el tablero (al arrancar o desde el inicio), un aviso amarillo: «Client A is already "
       "open in another taskboard window (since 09:12). Both save the same file: the last save "
       "wins. Close one of them.» Consecuencia: lo ves al entrar, se va solo, no bloquea nada."),
      ("B", "B · Aviso + chip que lo recuerda", "in-B",
       "Además el chip queda «Client A ⚠ open twice» mientras sigas ahí. Consecuencia: no se "
       "olvida; pero si cierras la otra ventana el chip miente hasta que algo vuelva a mirar el "
       "bloqueo (habría que sondearlo), y ocupa el chip, cortado a 24 celdas."),
      ],
     "A",
     "A dice lo necesario en el momento en que importa, sin un estado que pueda quedarse viejo.", []),
    (9, "register", "<code>--board PATH</code> registra la ruta para siempre",
     "Este punto es sobre todo de comportamiento; las dos capturas muestran la consecuencia.",
     [("hoy", "Hoy · registra", "rg-now",
       "<code>taskboard --board elsewhere/board-copy.json</code> añade esa ruta a "
       "<code>boards.json</code>: una tarjeta «board-copy» aparece en el inicio en cada arranque "
       "hasta que la archivas con <kbd>x</kbd> (y la entrada archivada se queda en el registro). Es "
       "también como vuelve un tablero archivado — el mensaje de archivar lo indica."),
      ("A", "A · Además, abrir sin registrar (--open)", "rg-A",
       "Una opción nueva (<code>--open PATH</code>) abre el archivo sin tocar "
       "<code>boards.json</code>: el chip dice «board-copy · not listed», <kbd>B</kbd> muestra tus 3 "
       "tableros y el próximo arranque normal vuelve a tu último tablero. Consecuencia: mirar una "
       "copia o un respaldo no ensucia tu inicio; ese archivo no sale en el inicio ni en la agenda de "
       "todos, y no recibe proyectos movidos."),
      ],
     "A",
     "Mantener <code>--board</code> como está (es la puerta de vuelta de un archivado) y añadir "
     "<code>--open</code> para lo puntual.", []),
]

LIMITS = [
    "Las PNG son ventanas reales de Windows Terminal de esta máquina (su fuente y su tema), "
    "seleccionadas por título; el log está en <code>out/png/capture-log.txt</code>.",
    "La fecha está fijada (mar 20 oct 2026); los datos son sintéticos (Personal, Client A, Course).",
    "El selector de identidad (punto 7) lo abre el guion encima del inicio, como lo haría "
    "<code>_init_team_mode</code>; no hay una carpeta de equipo real detrás.",
    "<kbd>A</kbd> (punto 1) es un binding del prototipo, fuera de <code>KEYMAP</code>: la barra de "
    "teclas no lo muestra.",
    "El chip «⚠ open twice» (punto 8 B) y «not listed» (punto 9 A) reutilizan la etiqueta del chip; "
    "una implementación tendría su propia marca.",
    "Los SVG de Textual (<code>out/svg/</code>) no muestran los avisos (toasts); por eso la página "
    "solo usa las PNG reales.",
]


def item_html(n, key, title, problem, variants, rec, rec_text, extras) -> str:
    cards = []
    for val, label, scene, cons in variants:
        if key == "export":
            media = export_png("now" if val == "hoy" else "clean")
        else:
            media = shot(scene)
        is_rec = " rec" if val == rec else ""
        cards.append(
            f'<div class="card{is_rec}"><h4>{label}{" · recomendada" if val == rec else ""}</h4>'
            f'<figure>{media}</figure><p>{cons}</p>'
            f'<label class="pick"><input type="radio" name="c-{key}" value="{val}"> Elijo esta</label>'
            f'</div>')
    extra = ""
    if extras:
        caps = {"ag-A-open": "<strong>Hallazgo, no variante:</strong> A tras ↵ sobre «Week 3 plan» "
                             "(Personal). El estado es correcto (pantalla principal, tablero "
                             "Personal, tarea seleccionada: lo escribe el propio guion), pero en "
                             "Windows Terminal la ventana queda en negro. Lo mismo pasa con el "
                             "código sin cambios: inicio → ↵ sobre Personal o Course, o arrancar "
                             "en Personal; Client A se dibuja bien. En el render sin terminal "
                             "(headless) sí se dibuja. No lo diagnostiqué.",
                "ex-now": "La pantalla al pulsar x (el aviso de la app con el archivo escrito)",
                "ro-A-moved": "A tras ↓ y K: Eval harness sube al primer lugar",
                "su-now-id": "Hoy · el selector de identidad, sin nombre",
                "su-A-id": "A · el selector con el chip",
                "su-B-id": "B · el selector con el borde"}
        extra = '<div class="extras">' + "".join(
            f'<figure><figcaption>{caps.get(s, s)}</figcaption>'
            f'{shot(s, "png/black" if s == "ag-A-open" else "png")}</figure>' for s in extras) \
            + "</div>"
    facts = ""
    if key == "export":
        f = json.loads((OUT / "export" / "facts.json").read_text(encoding="utf-8"))
        rows = "".join(f"<tr><td>{s}</td><td>{v['now_width']} × {v['now_rows']}</td>"
                       f"<td>{v['now_width']} × {v['clean_rows']}</td></tr>" for s, v in f.items())
        facts = (f'<table><tr><th>terminal</th><th>hoy (celdas × filas)</th><th>limpia</th></tr>'
                 f'{rows}</table>')
    return f"""
<section id="i{n}" class="item">
<h2><span class="num">{n}</span> {title}</h2>
<p>{problem}</p>
<div class="grid g{len(variants)}">{"".join(cards)}</div>
{facts}{extra}
<div class="box"><strong>Recomendación: {rec if rec != "limpia" else "Limpia"}.</strong> {rec_text}</div>
<div class="obj"><label>Objeción u otra idea para el punto {n} (opcional)</label>
<textarea data-note="{key}" placeholder="Solo si objetas algo"></textarea></div>
</section>"""


def main() -> None:
    body = []
    recs = "".join(f"<li><a href='#i{n}'>{n} · {t}</a> → <strong>"
                   f"{'Limpia' if r == 'limpia' else r}</strong></li>"
                   for n, _k, t, _p, _v, r, _rt, _e in ITEMS)
    body.append(f"""
<h1>Ronda de backlog · nueve pendientes de la batch de varios tableros</h1>
<div class="box bluf"><p><strong>En corto:</strong> nueve pendientes pequeños, cada uno con la app
real hoy y 1–3 variantes, capturados en Windows Terminal a 118×30 y 80×24 (cambia el tamaño
arriba). Mi recomendación por punto:</p><ol class="recs">{recs}</ol>
<p>Marca <em>Elijo esta</em> en cada punto (vacío = acepto la recomendada), escribe solo lo que
objetas, y pulsa <strong>Exportar respuestas</strong> al final.</p></div>
<p class="note">Todo es la <code>TaskboardApp</code> real (subclases en
<code>prototypes/backlog_round/proto.py</code>) sobre un registro sintético en una carpeta temporal;
nada en <code>taskboard/</code> cambió. Teclas reales pulsadas por el guion.</p>""")
    for it in ITEMS:
        body.append(item_html(*it))
    lim = "".join(f"<li>{x}</li>" for x in LIMITS)
    body.append(f"""
<section id="limites"><h2>Lo que esta ronda no representa fielmente</h2><ul>{lim}</ul></section>
<section id="respuestas"><h2>Notas generales y exportar</h2>
<div class="obj"><label>Notas generales o peticiones nuevas</label>
<textarea data-note="general" placeholder="Cualquier cosa que no encaje en un punto"></textarea></div>
<button id="export">Exportar respuestas</button> <span id="done"></span>
<pre id="preview" hidden></pre></section>""")
    keys = json.dumps([(n, k, r) for n, k, _t, _p, _v, r, _rt, _e in ITEMS])
    nav = "".join(f'<a href="#i{n}">{n}</a>' for n, *_ in ITEMS)
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Backlog round</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.5rem 16px; display:flex; gap:.8rem; flex-wrap:wrap; align-items:center; font-size:.9rem; }}
nav a, main a {{ color:var(--acc); text-decoration:none; }}
nav .sw {{ margin-left:auto; display:flex; gap:.3rem; }}
nav .sw button {{ background:var(--panel); color:var(--fg); border:1px solid var(--line); padding:.2rem .6rem; }}
nav .sw button.on {{ background:var(--acc); color:#0b0f14; }}
main {{ max-width:1600px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .6rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
h4 {{ margin:.2rem 0 .4rem; font-size:1rem; }}
.num {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px; padding:0 .5rem; }}
p, li {{ max-width:90ch; }}
code, kbd {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:110ch; margin:1rem 0; }}
.bluf ol {{ columns:2; margin:.4rem 0; }}
.note {{ color:var(--mut); font-size:.92rem; }}
.grid {{ display:grid; gap:1rem; align-items:start; }}
.g2 {{ grid-template-columns:repeat(2,1fr); }} .g3 {{ grid-template-columns:repeat(3,1fr); }}
.g4 {{ grid-template-columns:repeat(2,1fr); }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.6rem .8rem; }}
.card.rec {{ border-color:var(--acc); }}
.card p {{ font-size:.93rem; margin:.4rem 0; }}
.extras {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1rem; }}
figure {{ margin:0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; cursor:zoom-in; background:#0d1117; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
.miss {{ border:2px dashed #f43f5e; color:#f43f5e; padding:1rem; border-radius:6px; }}
body.s80 .sz-118x30, body.s118 .sz-80x24 {{ display:none; }}
table {{ border-collapse:collapse; margin:1rem 0; font-size:.92rem; }}
th, td {{ border:1px solid var(--line); padding:.3rem .6rem; text-align:left; }}
th {{ color:var(--mut); }}
.pick {{ display:inline-block; margin-top:.3rem; background:#0d1219; border:1px solid var(--line);
  border-radius:6px; padding:.25rem .7rem; cursor:pointer; }}
.obj {{ margin:.8rem 0; max-width:90ch; }}
.obj textarea {{ display:block; width:100%; min-height:3rem; margin-top:.3rem; background:var(--panel);
  color:var(--fg); border:1px solid var(--line); border-radius:6px; font:inherit; padding:.4rem; box-sizing:border-box; }}
button {{ background:var(--acc); color:#0b0f14; border:0; border-radius:6px; padding:.5rem 1rem;
  font:inherit; font-weight:600; cursor:pointer; }}
pre {{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:.6rem .8rem;
  white-space:pre-wrap; font:13px/1.45 ui-monospace,Consolas,monospace; }}
#zoom {{ position:fixed; inset:0; background:#000d; display:none; z-index:9; overflow:auto; cursor:zoom-out; }}
#zoom img {{ display:block; margin:1rem auto; max-width:96vw; }}
@media (max-width:1000px) {{ .g2, .g3, .g4, .extras {{ grid-template-columns:1fr; }} .bluf ol {{ columns:1; }} }}
</style></head><body class="s118">
<nav><strong>Backlog round</strong>{nav}<a href="#limites">Límites</a><a href="#respuestas">Exportar</a>
<span class="sw">Tamaño: <button data-s="118" class="on">118×30</button><button data-s="80">80×24</button></span></nav>
<main>{"".join(body)}</main>
<div id="zoom"><img alt=""></div>
<script>
const ITEMS = {keys};
document.querySelectorAll('nav .sw button').forEach(b => b.onclick = () => {{
  document.body.className = 's' + b.dataset.s;
  document.querySelectorAll('nav .sw button').forEach(x => x.classList.toggle('on', x === b));
}});
const z = document.getElementById('zoom'), zi = z.querySelector('img');
document.querySelectorAll('figure img').forEach(i => i.onclick = () => {{ zi.src = i.src; z.style.display = 'block'; }});
z.onclick = () => {{ z.style.display = 'none'; }};
document.getElementById('export').onclick = async () => {{
  const data = {{ round: 'backlog_round', branch: 'proto/backlog-round', items: {{}}, notes: '' }};
  const lines = ['Backlog round — respuestas'];
  for (const [n, key, rec] of ITEMS) {{
    const c = document.querySelector('input[name="c-' + key + '"]:checked');
    const choice = c ? c.value : rec;
    const obj = document.querySelector('[data-note="' + key + '"]').value.trim();
    data.items[n] = {{ key, choice, chosen_explicitly: !!c, objection: obj }};
    lines.push(n + ' ' + key + ': ' + choice + (c ? '' : ' (recomendada, sin marcar)')
               + (obj ? ' · OBJECIÓN: ' + obj : ''));
  }}
  data.notes = document.querySelector('[data-note="general"]').value.trim();
  if (data.notes) lines.push('NOTAS: ' + data.notes);
  lines.push('JSON: ' + JSON.stringify(data));
  const txt = lines.join('\\n');
  const pre = document.getElementById('preview'); pre.textContent = txt; pre.hidden = false;
  try {{ await navigator.clipboard.writeText(txt); document.getElementById('done').textContent = 'Copiado al portapapeles.'; }}
  catch (e) {{ document.getElementById('done').textContent = 'No pude copiar: selecciona el texto de abajo.'; }}
}};
</script>
</body></html>
"""
    PAGE.write_text(page, encoding="utf-8")
    print(PAGE, f"{PAGE.stat().st_size // 1024} KB · images", len(USED), "· missing:", MISSING)


if __name__ == "__main__":
    main()

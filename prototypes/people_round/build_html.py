"""THROWAWAY — build the verdict page of the people round from its captures.

    powershell -File prototypes/people_round/shoot.ps1      (real Windows Terminal PNGs)
    python prototypes/people_round/build_html.py

Every image is embedded (base64), so the page works opened alone. A missing
capture is printed on the page as missing — never replaced by an SVG.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "people-round.html"
SIZES = ("118x30", "80x24")
MISSING: list[str] = []
USED: set[str] = set()


def b64(path: Path) -> str | None:
    if not path.exists():
        MISSING.append(str(path.relative_to(HERE)))
        return None
    return base64.b64encode(path.read_bytes()).decode()


def shot(scene: str) -> str:
    """The real Windows Terminal PNG at both sizes (the size switch picks one)."""
    out = []
    for s in SIZES:
        USED.add(f"{scene}_{s}")
        data = b64(OUT / "png" / f"{scene}_{s}.png")
        if data is None:
            out.append(f'<div class="miss sz sz-{s}">captura faltante: {scene} · {s}</div>')
        else:
            out.append(f'<img class="sz sz-{s}" alt="{scene} {s}" loading="lazy" '
                       f'src="data:image/png;base64,{data}">')
    return "".join(out)


def fig(scene: str, cap: str = "") -> str:
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f"<figure>{c}{shot(scene)}</figure>"


# ---------------------------------------------------------------------------
# the decisions (the orchestrator's), each with its consequences
# ---------------------------------------------------------------------------
DECISIONS = [
    ("d1", "D1 · Un solo directorio para todos los tableros",
     "El directorio vive en <code>~/.taskboard/people.json</code>, junto a <code>boards.json</code>, "
     "no dentro de cada tablero. La vista de una persona lista sus tareas abiertas de <em>todos</em> "
     "los tableros (como la agenda <kbd>A</kbd>), cada fila con el chip de su tablero.",
     ["Ana aparece una vez aunque tenga tareas en Client A y en Course (se ve en las capturas del punto 1).",
      "Copiar un <code>board.json</code> a otra máquina no lleva el directorio: las menciones se leen "
      "como el texto guardado (con el formato recomendado abajo, <code>@ana.ruiz</code>, sigue siendo legible).",
      "La vista lee cada tablero una vez al abrirse, igual que <kbd>A</kbd>: lo que cambie en otra "
      "ventana mientras está abierta no se ve hasta reabrirla."]),
    ("d2", "D2 · Una persona = nombre + rol (+ nota libre opcional)",
     "Nada más: sin correo, teléfono ni empresa. La nota es una línea (\"Prefers a written agenda the day before\").",
     ["La lista cabe en dos filas por persona (nombre / rol) y el buscador filtra por nombre o rol.",
      "Si un día hace falta el correo, es un campo más en <code>people.json</code>; no se diseña ahora.",
      "Dos personas con el mismo nombre se distinguen por el rol en el selector y por su id."]),
    ("d3", "D3 · La mención se escribe con @ y guarda una referencia estable",
     "<kbd>@</kbd> en las notas abre un mini buscador que filtra el directorio mientras escribes; "
     "<kbd>↵</kbd> elige, y la última fila <code>+ add 'Nombre'</code> crea a la persona pidiendo su rol en el sitio. "
     "La nota guarda una referencia estable, así renombrar a alguien no rompe sus menciones; se dibuja <code>@Nombre</code>. "
     "El formato de guardado se decide en la sección siguiente.",
     ["Las notas dejan de ser texto 100&nbsp;% libre: hay un patrón (<code>@handle</code>) que la app lee. "
      "Se lee con un tokenizador como el del resaltado (<code>highlight_segments</code>), nunca como markup.",
      "Escribir un correo (<code>ana@x.com</code>) no abre el buscador: solo una <kbd>@</kbd> al inicio de palabra.",
      "<kbd>esc</kbd> con el buscador abierto deja la <code>@texto</code> como texto normal."]),
    ("d4", "D4 · El roster del modo equipo queda aparte en esta ronda",
     "El roster de <code>team_sync.py</code> (el standup, la vista <kbd>9</kbd> <em>People</em>) no se "
     "mezcla con este directorio. Son dos cosas: compañeros que sincronizan tableros vs. personas con "
     "las que tengo pendientes.",
     ["<strong>Choque de nombre:</strong> ya existe la vista <kbd>9</kbd> llamada <em>People</em> (carriles por "
      "miembro del equipo, captura «hoy» del punto 1). Con esta ronda habría dos cosas llamadas People. "
      "Propongo que la nueva se titule <em>PEOPLE · directory</em> en pantalla, o renombrar una de las dos; dímelo en la objeción.",
      "Un compañero del equipo que también es contacto aparece dos veces (roster y directorio) hasta que se unan en otra ronda.",
      "Las menciones viajan por la sincronización de equipo como texto; el compañero sin mi directorio ve <code>@ana.ruiz</code>."]),
    ("d5", "D5 · Cada botón de una ventana tiene su tecla, mostrada",
     "<kbd>y</kbd>/<kbd>n</kbd> en confirmaciones; <kbd>alt+letra</kbd> en ventanas con campos de texto. "
     "Se aplicó a todo lo nuevo de esta ronda.",
     ["Selector B (ventana): <kbd>↵ / alt+s</kbd> mencionar, <kbd>alt+a</kbd> añadir, <kbd>esc</kbd> cancelar/volver — escrito en su línea de teclas.",
      "Selector A (desplegable): no tiene botones; sus teclas (<kbd>↑↓</kbd> <kbd>↵</kbd> <kbd>esc</kbd> <kbd>⇥</kbd>) van en su propia línea.",
      "<strong>Hallazgo:</strong> dentro del editor, <kbd>alt+s</kbd> ya es <em>Save</em> de la tarea. En el alta en línea (A) "
      "el rol se confirma con <kbd>↵</kbd>, no con <kbd>alt+s</kbd>, para no guardar la tarea por accidente."]),
]

STORAGE = [
    ("handle", "S3 · handle: <code>@ana.ruiz</code>",
     "Ask @ana.ruiz about the stores",
     "El id <em>es</em> el handle, derivado del nombre al crear a la persona (<code>Ana Ruiz → ana.ruiz</code>, "
     "<code>ana.ruiz2</code> si ya existe) y nunca cambia. Renombrar a Ana cambia solo cómo se dibuja. "
     "En el editor se lee bien y se puede escribir a mano sin el buscador. Sin el directorio "
     "(otra máquina, un compañero) sigue siendo legible. Coste: tras un renombre fuerte el texto "
     "crudo muestra el handle viejo (<code>@luis.mora</code> para «Luis Moreno»)."),
    ("link", "S1 · enlace: <code>@[Ana Ruiz](p:ab12)</code>",
     "Ask @[Ana Ruiz](p:ab12) about the stores",
     "Guarda nombre visible + id. Sin el directorio se ve el nombre (el mejor respaldo). Pero el "
     "editor muestra el token entero: 22 caracteres por mención en un TextArea, fácil de romper al "
     "editar a mitad, y el nombre guardado queda viejo tras un renombre (se dibuja el actual, pero el texto crudo miente)."),
    ("list", "S2 · texto + lista: <code>@Ana Ruiz</code> y <code>people: [\"ab12\"]</code> en la tarea",
     "Ask @Ana Ruiz about the stores   (+ task.people = [\"ab12\"])",
     "El texto queda limpio, pero hay dos fuentes de verdad: borrar la mención del texto no la "
     "quita de la lista (o hay que reconciliar en cada guardado), y renombrar a Ana deja el texto viejo. "
     "Cambia el formato del tablero (campo nuevo en cada tarea)."),
]

# (number, key, title, problem, [(value, label, [(scene, caption)], consequence)], rec, rec_text)
ITEMS = [
    (1, "view", "La vista por persona",
     "Hoy no hay forma de responder «¿qué tengo pendiente con Ana?» sin buscar tarea por tarea. "
     "Postura: se usa operando y de reojo en una junta. Flujo: en la junta → abro a la persona → veo "
     "sus tareas abiertas en todos los tableros (atrasadas, hoy, el resto) → salto a una. "
     "Tecla propuesta: <kbd>@</kbd> (global, fuera de la barra como <kbd>A</kbd> y <kbd>R</kbd>; "
     "comprobado libre en <code>taskboard/keymap.py</code>). Las personas van ordenadas por urgencia: "
     "atrasadas, luego hoy, luego abiertas.",
     [("hoy", "Hoy · la vista 9 «People» es otra cosa", [("pv-now", "")],
       "La única vista de personas es la del modo equipo (carriles por miembro); sin modo equipo dice "
       "«team mode off». No hay nada para contactos."),
      ("A", "A · Dos paneles: lista | tareas", [("pv-A", ""), ("pv-A-open", "↵ sobre «Golden question set»: el tablero, con la tarea seleccionada")],
       "Todo a la vista de una vez: quién me necesita (contadores ▲ atrasadas, ● hoy, abiertas) y lo de la "
       "persona elegida, por bandas. <kbd>⇥</kbd> cambia de panel, <kbd>↵</kbd> abre la tarea en su tablero. "
       "A 80 columnas el panel de tareas pierde la columna de proyecto."),
      ("B", "B · Una tarjeta por persona", [("pv-B", "")],
       "Se lee de reojo: la barra dibuja atrasadas/hoy/abiertas y «next» dice lo próximo. Pero para ver "
       "las tareas hay que entrar (<kbd>↵</kbd> abre la página C): un paso más en la junta. Con más de "
       "~9 personas hay que desplazarse."),
      ("C", "C · Una página por persona", [("pv-C", "")],
       "Una persona a la vez, a ancho completo, y bajo cada tarea la línea de la nota que la menciona "
       "(lo que escribí sobre ella): el mejor apoyo en la junta. <kbd>←→</kbd> pasa a la siguiente persona. "
       "No da el panorama de quién me necesita más."),
      ],
     "A", "A da el panorama y el detalle sin cambiar de pantalla, que es lo que pide la junta. "
          "Sugiero robar de C la línea de contexto (la frase de la nota) bajo la tarea con el cursor."),
    (2, "picker", "El selector @ dentro de las notas del editor",
     "Escribiendo en las notas de una tarea, <kbd>@</kbd> al inicio de palabra abre el selector. "
     "Filtra por nombre (primero los que empiezan así) y luego por rol; la última fila crea a la persona. "
     "La captura muestra el editor real (<kbd>e</kbd> sobre «Steering committee»), con la vista previa "
     "dibujando las menciones.",
     [("hoy", "Hoy · @ es texto", [("mt-now", "")],
       "Nada pasa: <code>@an</code> queda como texto y nadie lo enlaza a una persona."),
      ("A", "A · Desplegable bajo el cursor", [("mt-A", "Escribiendo <code>@an</code>"),
                                               ("mt-A-add", "<code>@Sofia</code> no existe → ↵ en «+ add»: nombre y rol en el sitio"),
                                               ("mt-A-done", "Elegida Ana: el texto guarda <code>@ana.ruiz</code>, la vista previa dibuja <code>@Ana Ruiz</code>")],
       "No sales de la nota: sigues escribiendo y la lista se estrecha. El alta pide nombre completo "
       "(prellenado con lo escrito, porque un espacio cierra la mención) y rol, y confirma con <kbd>↵</kbd>. "
       "A 80 columnas el desplegable tapa parte de la vista previa."),
      ("B", "B · Ventana centrada", [("mt-B", "Escribiendo <code>@</code> y luego <code>an</code> en su campo"),
                                     ("mt-B-add", "<kbd>alt+a</kbd>: añadir a «Sofia» con su rol")],
       "Más espacio y botones con tecla (D5), y el filtro admite espacios. Pero tapa la nota que estás "
       "escribiendo y es una ventana más sobre el editor (que ya es pantalla completa)."),
      ],
     "A", "A respeta el flujo de escritura: la mención es una palabra más, no un diálogo."),
    (3, "search", "Buscar por persona",
     "Hoy <kbd>/</kbd> (solo en kanban y gantt) filtra por texto en título, proyecto o notas. "
     "Buscar «ana» encuentra las notas con <code>@ana.ruiz</code>, pero también «Can<strong>a</strong>ry release plan» (falso positivo). "
     "Se pide buscar por persona y poder usar el buscador solo para nombres.",
     [("hoy", "Hoy · texto plano", [("sr-now", "<kbd>/</kbd> ana"), ("sr-now-res", "Resultado: 4 tareas, una es «Canary» por el título")],
       "Funciona a medias: encuentra el texto crudo de la mención y cualquier palabra que contenga «ana»."),
      ("A", "A · @ dentro del mismo campo", [("sr-A", "<kbd>/</kbd> @an: la lista muestra solo nombres"),
                                              ("sr-A-res", "↵ sobre Ana: el kanban filtrado a sus tareas, la barra dice quién")],
       "Mismo idioma que las notas: <kbd>@</kbd> empieza una persona y <kbd>@</kbd> sola lista a todos (modo «solo nombres»). "
       "<kbd>↵</kbd> filtra sus tareas, <kbd>alt+p</kbd> abre su página. Exacto: sin falsos positivos. No hay modo que recordar."),
      ("B", "B · Interruptor tareas | personas", [("sr-B", "<kbd>/</kbd> <kbd>alt+n</kbd> → personas, «ma»"),
                                                   ("sr-B-res", "↵: la vista de personas sobre Marta")],
       "Explícito, pero es un modo: hay que mirar en qué lado está el interruptor. En «personas» el "
       "buscador solo lleva a la página de la persona, no filtra el tablero."),
      ("C", "C · El texto también busca en nombres y roles", [("sr-C-res", "<kbd>/</kbd> pm: las tareas que mencionan a la PM de Client A")],
       "Cero sintaxis nueva, pero más ruido: «ana» sigue trayendo «Canary», y un rol corto («pm») "
       "coincide con muchas cosas. «Solo nombres» queda para el <kbd>/</kbd> de la vista de personas."),
      ],
     "A", "A da búsqueda exacta por persona y el modo solo-nombres sin añadir un modo. Nota: <kbd>/</kbd> "
          "hoy vive solo en kanban y gantt; ampliarlo a otras vistas es otra decisión."),
    (4, "look", "Cómo se ve una mención: detalle, tarjeta kanban y presentación",
     "La misma tarea («Golden question set», con Ana y Andrés en sus notas) en tres sitios: "
     "el detalle (<kbd>↵</kbd>), su tarjeta en el kanban (<kbd>4</kbd>) y la presentación "
     "(<kbd>R</kbd> → <kbd>2</kbd> split, que muestra las notas a la sala).",
     [("hoy", "Hoy · el texto crudo", [("m-now-det", "Detalle"), ("m-now-kb", "Kanban"), ("m-now-pr", "Presentación")],
       "Se ve el handle guardado (<code>@ana.ruiz</code>): legible, pero no es el nombre y no destaca."),
      ("A", "A · @Nombre resaltado", [("m-A-det", "Detalle"), ("m-A-kb", "Kanban: <code>@Ana+1</code> en la fila de datos"), ("m-A-pr", "Presentación")],
       "Un tono propio (rosa, que hoy solo usa el chip de un tablero sin registrar) y el nombre actual. "
       "No cambia anchos. En la tarjeta, <code>@Ana+1</code> se pierde antes que la fecha cuando falta sitio."),
      ("B", "B · Chip", [("m-B-det", "Detalle"), ("m-B-kb", "Kanban"), ("m-B-pr", "Presentación")],
       "Salta más a la vista, pero cuesta dos celdas por mención, pesa en un párrafo con varias, y en "
       "la presentación el bloque de color compite con el resaltado <code>==…==</code>."),
      ("C", "C · Discreto + fila «with»", [("m-C-det", "Detalle: fila «with» con nombre y rol"), ("m-C-kb", "Kanban: nada"), ("m-C-pr", "Presentación: solo el nombre")],
       "La presentación queda limpia (la sala lee nombres, sin @ ni color) y el detalle dice con quién "
       "y su rol. Pero la tarjeta del kanban no muestra a nadie."),
      ],
     "A", "A: un solo tono, sin cambiar anchos, visible en los tres sitios. En la presentación también se "
          "muestra (las notas ya se enseñan ahí y la sala ve nombres, no handles)."),
]

LIMITS = [
    "Es la <code>TaskboardApp</code> real con pantallas nuevas y subclases parcheadas por escena "
    "(<code>prototypes/people_round/proto.py</code>); nada en <code>taskboard/</code> cambió.",
    "<kbd>@</kbd> no está en <code>KEYMAP</code> ni en el mapa <kbd>?</kbd>: el prototipo la liga aparte. "
    "En la implementación iría como <kbd>A</kbd> (global, <code>bar=False</code>).",
    "Las teclas <kbd>/</kbd> (buscar nombre), <kbd>n</kbd> (nueva persona) y <kbd>e</kbd> (editar) de la vista "
    "de personas se muestran pero no hacen nada en el prototipo; tampoco hay pantalla para editar el directorio.",
    "El alta de una persona («+ add») la añade solo en memoria; el prototipo no escribe <code>people.json</code>.",
    "No se modela la sincronización de equipo ni qué ve un compañero sin mi directorio (se describe en D4).",
    "Los formatos S1 y S2 se muestran como texto, no capturados: las capturas usan S3 (handle).",
    "<strong>Hallazgo ajeno a la ronda:</strong> la vista split de la presentación muestra los marcadores "
    "<code>!!…!!</code> y <code>++…++</code> en crudo (se ve en «hoy» del punto 4); el resto de la app los colorea.",
]


def item_html(n, key, title, problem, variants, rec, rec_text) -> str:
    cards = []
    for val, label, scenes, cons in variants:
        media = "".join(fig(s, cap) for s, cap in scenes)
        is_rec = " rec" if val == rec else ""
        cards.append(
            f'<div class="card{is_rec}"><h4>{label}{" · recomendada" if val == rec else ""}</h4>'
            f'<div class="media">{media}</div><p>{cons}</p>'
            f'<label class="pick"><input type="radio" name="c-{key}" value="{val}"> Elijo esta</label>'
            f'</div>')
    return f"""
<section id="i{n}" class="item">
<h2><span class="num">{n}</span> {title}</h2>
<p>{problem}</p>
<div class="grid g{len(variants)}">{"".join(cards)}</div>
<div class="box"><strong>Recomendación: {rec}.</strong> {rec_text}</div>
<div class="obj"><label>Objeción u otra idea para el punto {n} (opcional)</label>
<textarea data-note="{key}" placeholder="Solo si objetas algo"></textarea></div>
</section>"""


def decisions_html() -> str:
    out = []
    for key, title, what, cons in DECISIONS:
        li = "".join(f"<li>{c}</li>" for c in cons)
        out.append(f"""<div class="dec"><h3>{title}</h3><p>{what}</p>
<p class="lab">Consecuencias</p><ul>{li}</ul>
<div class="obj"><label><input type="checkbox" data-obj="{key}"> Objeto</label>
<textarea data-note="{key}" placeholder="Qué cambiarías (vacío = de acuerdo)"></textarea></div></div>""")
    rows = "".join(
        f'<tr class="{"rec" if k == "handle" else ""}"><td><label><input type="radio" name="c-storage" value="{k}"> '
        f'{t}{" · recomendada" if k == "handle" else ""}</label></td><td><code>{ex}</code></td><td>{c}</td></tr>'
        for k, t, ex, c in STORAGE)
    out.append(f"""<div class="dec" id="storage"><h3>D3 · Formato de guardado de la mención</h3>
<p>Cómo queda la línea en <code>board.json</code> cuando eliges a Ana en el selector:</p>
<div class="tw"><table><tr><th>forma</th><th>texto guardado</th><th>consecuencias</th></tr>{rows}</table></div>
<div class="box"><strong>Recomendación: S3 (handle).</strong> Las notas se escriben y se leen en un
TextArea: el handle es corto, se teclea a mano, es legible sin el directorio y estable ante renombres.
La lista de personas de una tarea se <em>deriva</em> del texto (una sola fuente de verdad). El
tokenizador acepta también S1 por si algún día se importa ese formato.</div>
<div class="obj"><label>Objeción sobre el formato (opcional)</label>
<textarea data-note="storage" placeholder="Solo si objetas"></textarea></div></div>""")
    return "".join(out)


def main() -> None:
    body = []
    recs = "".join(f"<li><a href='#i{n}'>{n} · {t}</a> → <strong>{r}</strong></li>"
                   for n, _k, t, _p, _v, r, _rt in ITEMS)
    body.append(f"""
<h1>Ronda de personas · directorio, menciones @ y vista por persona</h1>
<div class="box bluf"><p><strong>En corto:</strong> un directorio único de personas (nombre + rol) para
todos los tableros; <kbd>@</kbd> en las notas abre un selector que menciona o da de alta; una vista por
persona con sus tareas abiertas de todos los tableros, abierta con <kbd>@</kbd>; y búsqueda por persona con
<code>/@nombre</code>. Cuatro puntos con la app real hoy y 2–3 variantes cada uno, capturados en Windows
Terminal a 118×30 y 80×24 (cambia el tamaño arriba). Mi recomendación:</p><ol class="recs">{recs}</ol>
<p>Formato de la mención: <strong>handle <code>@ana.ruiz</code></strong> (S3). Decisiones D1–D5 abajo: marca
solo lo que objetas.</p>
<p>Marca <em>Elijo esta</em> en cada punto (vacío = acepto la recomendada), escribe solo lo que
objetas, y pulsa <strong>Exportar respuestas</strong> al final.</p></div>
<blockquote class="ask">«Esta parte va a requerir un directorio de personas y rol. Porque en algunas tareas hay que dar
seguimiento con personas, y a veces buscar por tarea no es lo más adecuado, si no por persona. Así cuando hay
una junta podría revisar si tengo alguna tarea pendiente con esa persona. Me imagino que en las notas podría usar
@ para referirme a las personas de este directorio (desplegar un mini buscador para seleccionarla o agregarla al
directorio en ese momento si es necesario), tener una vista también en función de las personas y poder usar el
buscador para buscar sus nombres o usarlo para nombres únicamente.»</blockquote>
<p class="note">Datos sintéticos: tres tableros (Personal, Client A, Course) y ocho personas (Ana Ruiz · Client A PM,
Luis Mora · Course TA, Marta Gil · Accountant…). Hoy fijado en martes 20 de octubre. Teclas reales pulsadas por el guion.</p>
<section id="decisiones"><h2>Decisiones de diseño (D1–D5)</h2>
<p>Las tomé para poder prototipar; cada una con lo que implica. Marca <em>Objeto</em> y escribe solo si no estás de acuerdo.</p>
{decisions_html()}</section>""")
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
    keys = json.dumps([(n, k, r) for n, k, _t, _p, _v, r, _rt in ITEMS])
    dkeys = json.dumps([k for k, *_ in DECISIONS])
    nav = "".join(f'<a href="#i{n}">{n}</a>' for n, *_ in ITEMS)
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>People round</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722; --pink:#f472b6; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.5rem 16px; display:flex; gap:.8rem; flex-wrap:wrap; align-items:center; font-size:.9rem; }}
nav a, main a {{ color:var(--acc); text-decoration:none; }}
nav .sw {{ margin-left:auto; display:flex; gap:.3rem; align-items:center; }}
nav .sw button {{ background:var(--panel); color:var(--fg); border:1px solid var(--line); padding:.2rem .6rem; }}
nav .sw button.on {{ background:var(--acc); color:#0b0f14; }}
main {{ max-width:1600px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .6rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
h3 {{ margin:.2rem 0 .4rem; font-size:1.05rem; color:var(--pink); }}
h4 {{ margin:.2rem 0 .4rem; font-size:1rem; }}
.num {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px; padding:0 .5rem; }}
p, li {{ max-width:90ch; }}
code, kbd {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:110ch; margin:1rem 0; }}
.bluf ol {{ columns:2; margin:.4rem 0; }}
.ask {{ border-left:3px solid var(--pink); margin:1rem 0; padding:.4rem 1rem; color:var(--mut); max-width:110ch; font-style:italic; }}
.note {{ color:var(--mut); font-size:.92rem; }}
.dec {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.7rem 1rem; margin:1rem 0; max-width:120ch; }}
.dec .lab {{ color:var(--mut); font-size:.85rem; margin:.4rem 0 0; text-transform:uppercase; letter-spacing:.04em; }}
.dec ul {{ margin:.2rem 0 .4rem; }}
.grid {{ display:grid; gap:1rem; align-items:start; }}
.g2 {{ grid-template-columns:repeat(2,1fr); }} .g3 {{ grid-template-columns:repeat(3,1fr); }}
.g4 {{ grid-template-columns:repeat(2,1fr); }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.6rem .8rem; min-width:0; }}
.card.rec {{ border-color:var(--acc); }}
.card p {{ font-size:.93rem; margin:.4rem 0; }}
.media {{ display:grid; gap:.6rem; }}
figure {{ margin:0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; cursor:zoom-in; background:#0d1117; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
.miss {{ border:2px dashed #f43f5e; color:#f43f5e; padding:1rem; border-radius:6px; }}
body.s80 .sz-118x30, body.s118 .sz-80x24 {{ display:none; }}
.tw {{ overflow-x:auto; }}
table {{ border-collapse:collapse; margin:.6rem 0; font-size:.92rem; }}
th, td {{ border:1px solid var(--line); padding:.35rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--mut); }}
tr.rec td:first-child {{ border-left:3px solid var(--acc); }}
.pick {{ display:inline-block; margin-top:.3rem; background:#0d1219; border:1px solid var(--line);
  border-radius:6px; padding:.25rem .7rem; cursor:pointer; }}
.obj {{ margin:.8rem 0; max-width:90ch; }}
.obj textarea {{ display:block; width:100%; min-height:3rem; margin-top:.3rem; background:#0d1219;
  color:var(--fg); border:1px solid var(--line); border-radius:6px; font:inherit; padding:.4rem; box-sizing:border-box; }}
button {{ background:var(--acc); color:#0b0f14; border:0; border-radius:6px; padding:.5rem 1rem;
  font:inherit; font-weight:600; cursor:pointer; }}
pre {{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:.6rem .8rem;
  white-space:pre-wrap; font:13px/1.45 ui-monospace,Consolas,monospace; }}
#zoom {{ position:fixed; inset:0; background:#000d; display:none; z-index:9; overflow:auto; cursor:zoom-out; }}
#zoom img {{ display:block; margin:1rem auto; max-width:96vw; }}
@media (max-width:1000px) {{ .g2, .g3, .g4 {{ grid-template-columns:1fr; }} .bluf ol {{ columns:1; }} }}
</style></head><body class="s118">
<nav><strong>People round</strong><a href="#decisiones">D1–D5</a><a href="#storage">Formato</a>{nav}<a href="#limites">Límites</a><a href="#respuestas">Exportar</a>
<span class="sw">Tamaño: <button data-s="118" class="on">118×30</button><button data-s="80">80×24</button></span></nav>
<main>{"".join(body)}</main>
<div id="zoom"><img alt=""></div>
<script>
const ITEMS = {keys};
const DECS = {dkeys};
document.querySelectorAll('nav .sw button').forEach(b => b.onclick = () => {{
  document.body.className = 's' + b.dataset.s;
  document.querySelectorAll('nav .sw button').forEach(x => x.classList.toggle('on', x === b));
}});
const z = document.getElementById('zoom'), zi = z.querySelector('img');
document.querySelectorAll('figure img').forEach(i => i.onclick = () => {{ zi.src = i.src; z.style.display = 'block'; }});
z.onclick = () => {{ z.style.display = 'none'; }};
const note = k => document.querySelector('[data-note="' + k + '"]').value.trim();
document.getElementById('export').onclick = async () => {{
  const data = {{ round: 'people_round', branch: 'proto/people', decisions: {{}}, storage: {{}}, items: {{}}, notes: '' }};
  const lines = ['People round — respuestas'];
  for (const k of DECS) {{
    const obj = document.querySelector('[data-obj="' + k + '"]').checked, txt = note(k);
    data.decisions[k] = {{ objects: obj || !!txt, note: txt }};
    lines.push(k.toUpperCase() + ': ' + ((obj || txt) ? 'OBJETO' + (txt ? ' · ' + txt : '') : 'de acuerdo'));
  }}
  const s = document.querySelector('input[name="c-storage"]:checked');
  data.storage = {{ choice: s ? s.value : 'handle', chosen_explicitly: !!s, objection: note('storage') }};
  lines.push('formato: ' + data.storage.choice + (s ? '' : ' (recomendado, sin marcar)')
             + (data.storage.objection ? ' · OBJECIÓN: ' + data.storage.objection : ''));
  for (const [n, key, rec] of ITEMS) {{
    const c = document.querySelector('input[name="c-' + key + '"]:checked');
    const choice = c ? c.value : rec, obj = note(key);
    data.items[n] = {{ key, choice, chosen_explicitly: !!c, objection: obj }};
    lines.push(n + ' ' + key + ': ' + choice + (c ? '' : ' (recomendada, sin marcar)')
               + (obj ? ' · OBJECIÓN: ' + obj : ''));
  }}
  data.notes = note('general');
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

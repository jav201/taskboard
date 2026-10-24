"""THROWAWAY — build the verdict page of the milestone-marks round from its captures.

    powershell -File prototypes/milestone_marks/shoot.ps1      (real Windows Terminal PNGs)
    python prototypes/milestone_marks/build_html.py

Every image is embedded (base64), so the page works opened alone. A missing
capture is printed on the page as missing — never replaced by an SVG.
"""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "milestone-marks.html"
SIZES = ("118x30", "80x24")
MISSING: list[str] = []
USED: set[str] = set()


def b64(path: Path) -> str | None:
    if not path.exists():
        MISSING.append(str(path.relative_to(HERE)))
        return None
    return base64.b64encode(path.read_bytes()).decode()


def shot(scene: str) -> str:
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


FIGN = [0]


def fig(scene: str, cap: str = "") -> str:
    FIGN[0] += 1
    c = f"<figcaption><b>Fig. {FIGN[0]}</b> · {cap or scene}</figcaption>"
    return f'<figure id="fig{FIGN[0]}">{c}{shot(scene)}</figure>'


# ---------------------------------------------------------------------------
# the decisions
# ---------------------------------------------------------------------------
D1_OPTS = [
    ("A", "A · Forma = clase; color = estado (como hoy)",
     ["Nada cambia en lo que significa el color: rojo tarde, gris alcanzado, matiz del proyecto mientras está abierto.",
      "La clase se distingue <em>solo por la forma</em>, en el mismo matiz: ■ ⬢ ▲ de un mismo proyecto a una celda cuestan (Fig. 3).",
      "La leyenda no puede usar color: es una lista de formas grises."]),
    ("B", "B · Forma + color = clase; el estado se va al texto",
     ["Clasificar de un vistazo: el color es la señal más rápida que tiene la terminal.",
      "El estado no se pierde porque ya estaba repetido en texto en todas las vistas: gantt = fecha en rojo junto a la marca + chip <code>▲2d</code>; "
      "kanban = <code>· 2d late</code> en rojo; lanes/focus = fecha roja; agenda <kbd>A</kbd> = <code>▲2d</code>; presentación = chip.",
      "Alcanzado = la forma <em>hueca</em> (⬢→⬡, ▲→△) + ✓ + título gris: se sigue viendo que «era un pago».",
      "Coste: un hito tarde ya no es una marca roja; hay que leer la fecha. En la regla de meses del gantt (marcas sin fecha al lado) el estado no se ve.",
      "Coste: los hitos <em>sin clase</em> pierden el rojo de «tarde» (siguen en el matiz del proyecto; su fecha sí se pone roja).",
      "Riesgo: los 8 colores de clase son los mismos matices que usan los proyectos (Client A tiene sky/blue/indigo/green): una clase cian junto a un proyecto cian se parecen."]),
    ("C", "C · Forma + color = clase; estado = fondo de la celda",
     ["Las dos cosas en la marca: frente = clase, fondo = estado (dos colores en la celda, dentro de la ley de 2 colores).",
      "En la captura real el fondo oscuro de <em>una</em> celda casi no se ve (Fig. 7): rojo y ámbar se leen como una sombra.",
      "Choca con el fondo de fin de semana del gantt y con la selección; en lanes y agenda un fondo detrás del glifo parece un resaltado.",
      "Alcanzado vuelve a ser gris: la clase se pierde en lo terminado."]),
]

D2_OPTS = [
    ("global", "Global · <code>~/.taskboard/marks.json</code> (como <code>people.json</code>)",
     ["«Payment» significa lo mismo en todos los tableros; la agenda <kbd>A</kbd> y el conteo de la ventana <kbd>#</kbd> («4 in all») cruzan tableros.",
      "Se define una vez. Mismo modelo que el directorio de personas (batch 2026-10-21-batch-01).",
      "Copiar un <code>board.json</code> a otra máquina no lleva las clases: el hito se dibuja ◆ y el editor muestra <code>payment (unknown)</code>. "
      "En modo equipo, el compañero sin mis clases ve ◆."]),
    ("board", "Por tablero · en <code>settings</code> del <code>board.json</code>",
     ["Viaja con el tablero, también por la sincronización de equipo.",
      "Hay que crear «Payment» en cada tablero; dos tableros pueden tener «Payment» con forma distinta y la agenda <kbd>A</kbd> mezcla significados.",
      "La ventana <kbd>#</kbd> solo podría contar el tablero abierto."]),
    ("hybrid", "Global + copia en el tablero de las clases que usa",
     ["Se ve bien en otra máquina o en el tablero de un compañero.",
      "Dos fuentes de verdad: cambiar la forma en el global deja copias viejas; hay que reconciliar al abrir cada tablero."]),
]

# (number, key, title, problem, [(value, label, [(scene, caption)], consequence)], rec, rec_text)
ITEMS = [
    (1, "model", "El modelo de marcador: qué canal lleva la clase y cuál el estado (D1)",
     "Hoy un hito es siempre <code>◆</code> y su color <em>ya está gastado</em> en el estado: matiz del proyecto mientras "
     "está abierto, rojo (<code>over</code>) cuando va tarde, gris (<code>reached</code>) con <code>◆✓</code> cuando se alcanzó. "
     "Un color de clase choca con ese color de estado. Las capturas muestran el mismo tablero (Client A, 10 hitos: 4 clases + uno sin clase; "
     "uno tarde, uno hoy, dos alcanzados) en el gantt y en el kanban (donde un hito nunca es tarjeta: vive en la regla de banda del proyecto).",
     [("hoy", "Hoy · todo ◆, el color es estado", [("e-now-g", "Gantt"), ("e-now-k", "Kanban (reglas de banda)")],
       "No hay forma de saber cuál es un pago y cuál una entrega sin leer el título."),
      ("A", "A · Forma = clase, color = estado", [("e-A-g", "Gantt: ■ rojo = Review tarde, ■ azul = Review abierto"), ("e-A-k", "Kanban")],
       "Quien no clasifica no nota nada. Pero las clases del mismo proyecto comparten matiz: hay que distinguir ■ de ⬢ de ▲ a una celda."),
      ("B", "B · Forma + color = clase; estado en el texto", [("e-B-g", "Gantt: Rubric sign-off ■ violeta, su fecha <code>Oct 18</code> y el chip <code>▲2d</code> en rojo; alcanzados huecos △ ⬡"), ("e-B-k", "Kanban: la regla dice <code>2d late</code> en rojo")],
       "Las clases saltan a la vista (cian, ámbar, violeta, rosa). El estado sigue en la fecha y el chip; lo alcanzado queda hueco y gris en el título."),
      ("C", "C · Forma + color = clase; estado de fondo", [("e-C-g", "Gantt: el fondo rojo/ámbar bajo ■ apenas se ve"), ("e-C-k", "Kanban")],
       "Honesto en papel, débil en pantalla: una sola celda de fondo oscuro no se distingue a simple vista. Lo alcanzado pierde el color de clase."),
      ],
     "B", "B libera el color para la clase sin perder el estado, que ya estaba escrito en texto en todas las vistas. "
          "Una regla nueva y simple: <em>el rojo vive en el texto, la marca dice qué es</em>."),
    (2, "editor", "Elegir la clase en el editor",
     "El editor es la pantalla completa de hoy (<kbd>e</kbd> sobre «Index v1 delivered», una Delivery). "
     "Cada variante añade la clase con su tecla directa <kbd>alt+m</kbd>, escrita en la línea de teclas del pie "
     "(estándar: todo botón con tecla; <kbd>alt+letra</kbd> junto a campos de texto). Comprobado: <kbd>alt+m</kbd> está libre en el editor.",
     [("hoy", "Hoy · solo la casilla milestone", [("ed-now", "")],
       "El hito es un sí/no; no hay dónde decir de qué tipo es."),
      ("A", "A · Un select «Mark» en la fila de chips", [("ed-A", "<kbd>alt+m</kbd> abre la lista; la última fila crea una clase")],
       "Igual que proyecto/fase/prioridad (mismo widget, misma fila). A 80 columnas cabe justo (la mitad «what» mide 72). "
       "<code>+ new class…</code> abriría el mismo formulario que la ventana <kbd>#</kbd>."),
      ("B", "B · Una fila con todas las clases", [("ed-B", "<kbd>alt+m</kbd> enfoca la fila, <kbd>←→</kbd> elige")],
       "Todo visible y un gesto; pero cuesta una fila de notas y con más de 5–6 clases ya no cabe a 80 columnas."),
      ("C", "C · Botón en la fila del título + ventana", [("ed-C", "<kbd>alt+m</kbd>: filtro, clases con conteos, <kbd>alt+n</kbd> nueva"), ("ed-C-new", "<kbd>alt+n</kbd> con «Legal» escrito: el formulario de clase")],
       "Muestra cuántos hitos tiene cada clase y crea en el sitio; pero es una ventana más sobre el editor."),
      ],
     "A", "A: un campo más con el mismo patrón que ya conoces, sin ventanas ni filas extra."),
    (3, "legend", "La leyenda: dónde se explica qué es cada forma",
     "Con clases, el <code>◆ milestone</code> de la leyenda ya no basta. Dónde va (y si la sala la ve en la presentación). "
     "Abajo, primero cómo se leen las clases en el resto de vistas con D1-B (fijo, no se elige), luego las 3 leyendas.",
     [("A", "A · En la fila de leyenda del gantt y en el mapa <kbd>?</kbd>", [("lg-A", "<kbd>?</kbd> en el gantt: una línea por clase y cómo se dibujan tarde/alcanzado"), ("e-B-g", "La fila de leyenda de abajo (solo cuando sobra una fila)")],
       "Sin filas nuevas. Pero la fila de abajo desaparece cuando el tablero llena la altura (a 80×24 y con la banda del punto 4 no aparece), "
       "y la presentación no tiene leyenda para la sala."),
      ("B", "B · Una franja bajo la regla (gantt y presentación)", [("lg-B", "Gantt: <code>▲ Delivery 1 · ⬢ Payment 2 …</code> con abiertos"), ("lg-B-pr", "Presentación: solo las clases de ese proyecto")],
       "Siempre visible, también en la exportación de la presentación (<kbd>x</kbd> exporta el mismo cuadro). Cuesta una fila del cuerpo."),
      ("C", "C · Sin leyenda: el nombre va junto a la fecha", [("lg-C", "<code>■ Oct 18 · review</code>"), ("lg-C-pr", "Presentación")],
       "Se explica solo y la sala lo lee sin leyenda; pero ocupa el campo del gantt y en fechas cercanas los nombres chocan o se cortan."),
      ],
     "B", "B: una fila fija que la sala también ve. Lista solo las clases presentes, así que en un proyecto con 2 clases es corta."),
    (4, "filter", "Filtrar o agrupar por clase (opcional)",
     "Ver solo los pagos en el gantt o en la presentación. Tres formas, de la más barata a la más nueva.",
     [("A", "A · <code>/#pay</code> en el buscador", [("f-A-res", "<kbd>/</kbd> <code>#pay</code> ↵: solo los hitos Payment")],
       "Casi gratis: reutiliza el filtro de <kbd>/</kbd> (mismo idioma que <code>/@ana</code> de la ronda de personas). "
       "Pero oculta también el trabajo (solo quedan los hitos) y la presentación no tiene <kbd>/</kbd>."),
      ("B", "B · La ventana <kbd>#</kbd>: <kbd>␣</kbd> oculta/muestra, <kbd>↵</kbd> solo esta", [("f-B-win", "Review oculto con <kbd>␣</kbd>"), ("f-B-res", "El gantt: el trabajo sigue, Review no; la franja dice qué falta"), ("f-B-pr", "La presentación también lo respeta (sin «Steering go/no-go»)")],
       "Un solo sitio para las clases (gestionar y filtrar). Funciona en gantt y presentación, y deja las barras de trabajo."),
      ("C", "C · Agrupar: una banda «MILESTONES BY CLASS»", [("f-C", "<kbd>g</kbd> en el gantt: una fila por clase con todos sus hitos")],
       "Responde «¿qué pagos vienen?» en una fila; pero son 2+N filas nuevas y a 80×24 pliega proyectos."),
      ("ninguno", "Ninguno por ahora", [], "La clase solo se ve; filtrar queda para otra ronda."),
      ],
     "B", "B: la misma ventana que gestiona las clases filtra gantt y presentación. A (<code>/#pay</code>) se puede añadir de regalo porque el asiento del filtro ya existe."),
]

READ_COMMON = [
    ("rd-lanes", "Lanes <kbd>1</kbd>: la marca junto al título"),
    ("rd-focus", "Focus <kbd>5</kbd>"),
    ("rd-now-agenda", "Agenda <kbd>A</kbd> hoy: los hitos <em>no</em> se marcan"),
    ("rd-agenda", "Agenda <kbd>A</kbd> con la marca antes del título"),
    ("rd-now-pr1", "Presentación hoy (<kbd>R</kbd>)"),
    ("rd-pr1", "Presentación con clases"),
    ("rd-pr2", "Presentación split <kbd>2</kbd>"),
]

GLYPHS = [  # glyph, hollow, verdict, why
    ("◆", "◇", "se queda", "el hito sin clase; ojo: también es la fecha comprometida del proyecto en la fila del span, y una tarea de un día en el gantt"),
    ("▲", "△", "acepto", "Cascadia Mono; ▲ también es la marca «tarde» del texto (▲2d), pero vive en otra columna y en rojo"),
    ("■", "□", "acepto", "Cascadia Mono"),
    ("⬢", "⬡", "acepto", "Cascadia Mono — reemplaza a ● para Payment. Honesto: Cascadia la dibuja pequeña; de cerca es un hexágono, "
     "en las capturas reducidas (kanban, a 80 columnas) se parece a ●. Si molesta, ⬟ o ■ separan más"),
    ("⬟", "⬠", "acepto", "Cascadia Mono"),
    ("▼", "▽", "acepto", "Cascadia Mono"),
    ("★", "☆", "acepto*", "no está en Cascadia Mono; Windows Terminal la dibuja con su fuente de respaldo en una celda (capturado). Otra terminal podría no"),
    ("✦", "✧", "acepto*", "igual que ★"),
    ("⚑", "⚐", "acepto*", "igual que ★"),
    ("●", "○", "evito", "es el punto de progreso del gantt; ○ ◔ ◑ ◕ son sus puntas de fase. Por eso Payment pasó de ● (tu ejemplo) a ⬢"),
    ("◉", "◎", "rechazo", "es el pulso del gantt"),
    ("♦", "◈", "rechazo", "se lee como ◆"),
    ("⬤", "◯", "rechazo", "en Cascadia se dibuja igual que ●"),
    ("⬛", "⬜", "rechazo", "ancho de Asia oriental: 2 celdas, las barras se corren (Fig. 9)"),
    ("⭐", "", "rechazo", "emoji ancho: 2 celdas"),
]

FINDINGS = [
    "<strong>El color ya está gastado.</strong> El estado del hito (tarde / alcanzado) vive en su color; por eso D1 existe.",
    "<strong><code>◆</code> significa tres cosas hoy:</strong> hito, fecha comprometida del proyecto (en la fila del span) y, en el gantt, "
    "una tarea normal de un solo día (inicio = fin). Las clases alivian esto: el ◆ queda para «hito sin clase».",
    "<strong>El círculo está tomado en el gantt:</strong> <code>●</code> progreso, <code>◉ ◎</code> pulso, <code>○ ◔ ◑ ◕</code> punta de fase. "
    "Tu ejemplo «Payment ●» se cambió por <code>⬢</code> en todas las capturas.",
    "<strong>La agenda <kbd>A</kbd> hoy no marca los hitos</strong> (ni con ◆). Con clases, gana la marca.",
    "<strong>El kanban no tiene tarjetas de hito:</strong> un hito vive en la regla de banda de su proyecto; ahí aparece su clase.",
    "<strong>Sin migración:</strong> la clase se guarda como <code>\"mark\": \"payment\"</code> en la tarea. <code>Task.extra</code> ya conserva claves "
    "desconocidas, así que una versión vieja de taskboard lo preserva al guardar.",
    "<strong>Teclas libres comprobadas en <code>keymap.py</code>:</strong> <kbd>#</kbd> (global) y <kbd>alt+m</kbd> (editor). "
    "<kbd>g</kbd> solo existe en el kanban, así que en el gantt está libre para la variante 4C.",
]

LIMITS = [
    "Es la <code>TaskboardApp</code> real con funciones de <code>views</code> parcheadas por escena "
    "(<code>prototypes/milestone_marks/proto.py</code>); nada en <code>taskboard/</code> cambió. Teclas reales pulsadas por el guion.",
    "<kbd>#</kbd>, <kbd>alt+m</kbd> y <kbd>g</kbd> (gantt) no están en <code>KEYMAP</code> ni en el mapa <kbd>?</kbd>; el prototipo las liga aparte.",
    "El formulario de clase, <kbd>n</kbd>/<kbd>e</kbd>/<kbd>d</kbd> de la ventana <kbd>#</kbd> y <code>+ new class…</code> del select no guardan nada; "
    "<kbd>d</kbd> solo muestra la tecla (pediría confirmación y/n). Elegir una clase en el editor no se guarda en la tarea.",
    "El texto de uso del mapa <kbd>?</kbd> («◆ title = a milestone») y la línea del detalle <kbd>↵</kbd> («· ◆ milestone») no se actualizaron.",
    "La vista de personas no marca hitos (hoy tampoco). La exportación de la presentación (<kbd>x</kbd>) usa el mismo render que se capturó, pero no se exportó en la ronda.",
    "No se resolvió el choque de color clase/proyecto (riesgo anotado en D1-B); el formulario podría avisar si el color ya lo usa un proyecto del tablero.",
    "En la variante C las marcas de la regla de meses no llevan fondo.",
    "El fixture usa <code>⬢</code> para Payment en lugar de tu <code>●</code> (ver hallazgos). Datos sintéticos: tableros Personal, Client A y Course; hoy fijado en martes 20 de octubre de 2026.",
]

JSON_EX = """// ~/.taskboard/marks.json   (D2 · global, beside boards.json and people.json)
{"version": 1, "marks": [
  {"id": "delivery", "name": "Delivery", "shape": "▲", "colour": "cyan"},
  {"id": "payment",  "name": "Payment",  "shape": "⬢", "colour": "amber"},
  {"id": "review",   "name": "Review",   "shape": "■", "colour": "violet"},
  {"id": "launch",   "name": "Launch",   "shape": "★", "colour": "pink"}]}

// a task in board.json: one new key, kept by Task.extra (no migration)
{"title": "Milestone 2 invoice", "milestone": true, "due_date": "2026-11-10", "mark": "payment"}"""


def code(src: str, lang: str) -> str:
    return f'<pre data-lang="{lang}"><code>{html.escape(src)}</code></pre>'


def channel_table() -> str:
    """The difference map: which channel carries what, today and in each option."""
    rows = [("forma", "siempre ◆", "clase", "clase", "clase"),
            ("color de la marca", "estado", "estado", "clase", "clase"),
            ("fondo de la celda", "—", "—", "—", "estado (rojo tarde, ámbar hoy)"),
            ("relleno", "—", "—", "hueco = alcanzado", "—"),
            ("fecha / chip en texto", "estado", "estado", "estado (único canal)", "estado"),
            ("✓", "alcanzado", "alcanzado", "alcanzado", "alcanzado")]
    head = "<tr><th>canal</th><th>hoy</th><th>A</th><th class='rec'>B · recomendada</th><th>C</th></tr>"
    body = "".join("<tr>" + "".join(
        f"<td class='{'chg' if i and r[i] != r[1] and i > 1 else ''}{' rec' if i == 3 else ''}'>{x}</td>"
        for i, x in enumerate(r)) + "</tr>" for r in rows)
    return (f"<div class='tw'><table class='chan'>{head}{body}</table></div>"
            "<p class='note'>«estado» en el color = matiz del proyecto abierto, rojo tarde, gris alcanzado; "
            "en el texto = la fecha en rojo y el chip <code>▲2d</code> / <code>today</code> / <code>✓ done</code>.</p>")


def glyph_table() -> str:
    cls = {"se queda": "keep", "acepto": "ok", "acepto*": "ok2", "evito": "warn", "rechazo": "bad"}
    rows = "".join(f"<tr class='{cls[v]}'><td class='g'>{g}</td><td class='g'>{h}</td><td>U+{ord(g):04X}</td>"
                   f"<td><b>{v}</b></td><td>{w}</td></tr>" for g, h, v, w in GLYPHS)
    return (f"<div class='tw'><table class='gl'><tr><th>forma</th><th>hueca</th><th>código</th><th>veredicto</th>"
            f"<th>por qué (de la captura real)</th></tr>{rows}</table></div>")


def opt_cards(name: str, opts, rec: str) -> str:
    out = []
    for val, title, cons in opts:
        li = "".join(f"<li>{c}</li>" for c in cons)
        r = val == rec
        out.append(f"<div class='opt{' rec' if r else ''}'><label><input type='radio' name='{name}' value='{val}'> "
                   f"<strong>{title}</strong>{' · recomendada' if r else ''}</label><ul>{li}</ul></div>")
    return "".join(out)


def decisions_html() -> str:
    return f"""
<div class="dec" id="d1"><h3>D1 · Estado vs. clase: quién se queda con el color</h3>
<p>El mapa de canales (qué lleva cada cosa, hoy y en cada opción; en verde lo que cambia respecto a hoy):</p>
{channel_table()}
<p>Las capturas de cada opción están en el <a href="#i1">punto 1</a> (elegir aquí o allí marca lo mismo). Consecuencias:</p>
<div class="opts">{opt_cards("d1", D1_OPTS, "B")}</div>
<div class="box"><strong>Recomendación: B.</strong> El estado ya está escrito en texto en cada vista que dibuja un hito, así que el color puede pasar a la clase con poca pérdida. La pérdida real (la regla de meses del gantt y los hitos sin clase) está nombrada arriba.</div>
<div class="obj"><label><input type="checkbox" data-obj="d1"> Objeto</label>
<textarea data-note="d1" placeholder="Qué cambiarías (vacío = de acuerdo con lo que marques)"></textarea></div></div>

<div class="dec" id="d2"><h3>D2 · Alcance de las clases: global o por tablero</h3>
<div class="opts">{opt_cards("d2", D2_OPTS, "global")}</div>
<div class="box"><strong>Recomendación: global</strong>, igual que el directorio de personas. El hito guarda solo el id (<code>"mark": "payment"</code>); sin el archivo de clases se dibuja ◆, que es exactamente el comportamiento de hoy.</div>
{code(JSON_EX, "json")}
<div class="obj"><label><input type="checkbox" data-obj="d2"> Objeto</label>
<textarea data-note="d2" placeholder="Qué cambiarías"></textarea></div></div>"""


def item_html(n, key, title, problem, variants, rec, rec_text) -> str:
    cards = []
    for val, label, scenes, cons in variants:
        media = "".join(fig(s, cap) for s, cap in scenes)
        is_rec = " rec" if val == rec else ""
        pick = (f'<label class="pick"><input type="radio" name="c-{key}" value="{val}"> Elijo esta</label>'
                if val != "hoy" else '<span class="today">referencia: la app de hoy</span>')
        cards.append(f'<div class="card{is_rec}"><h4>{label}{" · recomendada" if val == rec else ""}</h4>'
                     f'<div class="media">{media}</div><p>{cons}</p>{pick}</div>')
    extra = ""
    if key == "model":
        extra = f"""
<h3 class="sub">Las clases del prototipo y el marcador por defecto</h3>
<p>Una clase = nombre + forma + color, creada por ti (pocas: 3–8). Un hito sin clase sigue siendo <code>◆</code>, como hoy. Las cuatro de las capturas:
<code class="cl c-cyan">▲ Delivery</code> <code class="cl c-amber">⬢ Payment</code> <code class="cl c-violet">■ Review</code> <code class="cl c-pink">★ Launch</code>.</p>
<h3 class="sub">Qué formas sirven: cobertura real en Cascadia Mono / Windows Terminal</h3>
<p>Cada forma 6 veces entre barras (una por celda), seguidas, sobre los fondos de la variante C y con su gemela hueca. Una forma ancha corre las barras.</p>
<div class="grid g1">{fig("glyphs", "La hoja de formas, capturada")}</div>
{glyph_table()}"""
    if key == "editor":
        extra = f"""
<h3 class="sub">Común a las tres: la ventana de clases <kbd>#</kbd> y el formulario</h3>
<p><kbd>#</kbd> (global, libre) abre la lista de clases con sus hitos abiertos / totales en todos los tableros. Teclas: <kbd>n</kbd> nueva,
<kbd>e</kbd> editar, <kbd>d</kbd> borrar (pide y/n), <kbd>␣</kbd> ocultar/mostrar y <kbd>↵</kbd> solo esta (punto 4). El formulario tiene
<kbd>alt+n</kbd> nombre, <kbd>alt+c</kbd> color, <kbd>alt+h</kbd> forma (<kbd>←→</kbd> elige), <kbd>alt+s</kbd> guardar, <kbd>esc</kbd>, y una
vista previa de cómo se dibuja abierta / tarde / alcanzada con D1-B.</p>
<div class="grid g2">{fig("mg-list", "<kbd>#</kbd> en el gantt")}{fig("mg-edit", "<kbd>e</kbd> sobre Payment, <kbd>alt+h</kbd> <kbd>→</kbd>: la forma cambia y la vista previa también")}</div>
<div class="obj"><label>Objeción sobre la ventana <kbd>#</kbd> o el formulario (opcional)</label>
<textarea data-note="manager" placeholder="Solo si objetas"></textarea></div>"""
    if key == "legend":
        common = "".join(fig(s, c) for s, c in READ_COMMON)
        extra_top = f"""
<h3 class="sub">Así se lee la clase en el resto de vistas (con D1-B)</h3>
<div class="grid g2">{common}</div>
<h3 class="sub">Las leyendas</h3>"""
        problem = problem + extra_top
    grid = f'<div class="grid g{min(len(variants), 4)}">{"".join(cards)}</div>'
    return f"""
<section id="i{n}" class="item">
<h2><span class="num">{n}</span> {title}</h2>
<p>{problem}</p>
{grid}
{extra}
<div class="box"><strong>Recomendación: {rec}.</strong> {rec_text}</div>
<div class="obj"><label>Objeción u otra idea para el punto {n} (opcional)</label>
<textarea data-note="{key}" placeholder="Solo si objetas algo"></textarea></div>
</section>"""


def main() -> None:
    body = []
    recs = "".join(f"<li><a href='#i{n}'>{n} · {t.split(':')[0]}</a> → <strong>{r}</strong></li>"
                   for n, _k, t, _p, _v, r, _rt in ITEMS)
    finds = "".join(f"<li>{x}</li>" for x in FINDINGS)
    body.append(f"""
<h1>Marcadores de hito · forma y color por clase</h1>
<div class="box bluf"><p><strong>En corto:</strong> cada hito puede tener una <em>clase</em> que tú nombras (forma + color:
<code class="cl c-cyan">▲ Delivery</code> <code class="cl c-amber">⬢ Payment</code> <code class="cl c-violet">■ Review</code>
<code class="cl c-pink">★ Launch</code>); sin clase sigue siendo <code>◆</code>. El problema de fondo es que el color del hito ya
dice su estado (rojo tarde, gris alcanzado). Recomiendo <strong>D1-B</strong>: la marca dice <em>qué es</em> (forma + color) y el
estado se queda en el texto, donde ya estaba (fecha roja, chip <code>▲2d</code>; alcanzado = forma hueca ✓). Clases <strong>globales</strong>
(D2), como el directorio de personas. Cuatro puntos con la app real hoy y 2–3 variantes cada uno, capturados en Windows Terminal a
118×30 y 80×24 (cambia el tamaño arriba). Mi recomendación:</p><ol class="recs">{recs}</ol>
<p>Marca <em>Elijo esta</em> en cada punto (vacío = acepto la recomendada), objeta solo lo que no te convenza, y pulsa
<strong>Exportar respuestas</strong> al final.</p></div>
<blockquote class="ask">«Necesitamos tener marcadores de figura y color para los milestones... me doy cuenta que hay veces que necesito
clasificarlos y esto me ayudaría. Por favor prototipemos primero»</blockquote>
<section id="hallazgos"><h2>Lo que encontré al leer el código y capturar</h2><ul>{finds}</ul></section>
<section id="decisiones"><h2>Decisiones (D1–D2)</h2>
<p>Marca la opción que quieres (vacío = la recomendada) y escribe solo si objetas.</p>
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
    nav = "".join(f'<a href="#i{n}">{n}</a>' for n, *_ in ITEMS)
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Milestone marks</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722;
  --cyan:#22d3ee; --amber:#fbbf24; --violet:#a78bfa; --pink:#f472b6; --red:#f43f5e; --green:#4ade80; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.5rem 16px; display:flex; gap:.8rem; flex-wrap:wrap; align-items:center; font-size:.9rem; }}
nav a, main a {{ color:var(--acc); text-decoration:none; }}
nav .sw {{ margin-left:auto; display:flex; gap:.3rem; align-items:center; }}
nav .sw button {{ background:var(--panel); color:var(--fg); border:1px solid var(--line); padding:.2rem .6rem; }}
nav .sw button.on {{ background:var(--acc); color:#0b0f14; }}
main {{ max-width:1600px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .6rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
h3 {{ margin:.2rem 0 .4rem; font-size:1.05rem; color:var(--acc); }}
h3.sub {{ margin-top:1.4rem; color:var(--fg); }}
h4 {{ margin:.2rem 0 .4rem; font-size:1rem; }}
.num {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px; padding:0 .5rem; }}
p, li {{ max-width:95ch; }}
code, kbd {{ font-family:ui-monospace,"Cascadia Mono",Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
code.cl {{ font-weight:600; }} .c-cyan {{ color:var(--cyan); }} .c-amber {{ color:var(--amber); }}
.c-violet {{ color:var(--violet); }} .c-pink {{ color:var(--pink); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:115ch; margin:1rem 0; }}
.bluf ol {{ columns:2; margin:.4rem 0; }}
.ask {{ border-left:3px solid var(--pink); margin:1rem 0; padding:.4rem 1rem; color:var(--mut); max-width:110ch; font-style:italic; }}
.dec {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.7rem 1rem; margin:1rem 0; }}
.opts {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; }}
.opt {{ border:1px solid var(--line); border-radius:6px; padding:.5rem .7rem; background:#0d1219; }}
.opt.rec {{ border-color:var(--acc); }}
.opt ul {{ margin:.3rem 0 0; padding-left:1.1rem; font-size:.93rem; }}
.grid {{ display:grid; gap:1rem; align-items:start; }}
.g1 {{ grid-template-columns:minmax(0,900px); }}
.g2 {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .g3 {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
.g4 {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.6rem .8rem; min-width:0; }}
.card.rec {{ border-color:var(--acc); }}
.card p {{ font-size:.93rem; margin:.4rem 0; }}
.media {{ display:grid; gap:.6rem; }}
figure {{ margin:0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; cursor:zoom-in; background:#0d1117; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
.miss {{ border:2px dashed var(--red); color:var(--red); padding:1rem; border-radius:6px; }}
body.s80 .sz-118x30, body.s118 .sz-80x24 {{ display:none; }}
.tw {{ overflow-x:auto; }}
table {{ border-collapse:collapse; margin:.6rem 0; font-size:.92rem; }}
th, td {{ border:1px solid var(--line); padding:.35rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--mut); }}
th.rec, td.rec {{ background:#0f1f22; }}
td.chg {{ color:var(--green); }}
table.gl td.g {{ font-family:"Cascadia Mono",ui-monospace,monospace; font-size:1.15rem; text-align:center; }}
table.gl tr.ok td:nth-child(4) {{ color:var(--green); }} table.gl tr.ok2 td:nth-child(4) {{ color:#a3e635; }}
table.gl tr.warn td:nth-child(4) {{ color:var(--amber); }} table.gl tr.bad td:nth-child(4) {{ color:var(--red); }}
.pick {{ display:inline-block; margin-top:.3rem; background:#0d1219; border:1px solid var(--line); border-radius:6px; padding:.25rem .7rem; cursor:pointer; }}
.today, .note {{ color:var(--mut); font-size:.85rem; }}
.obj {{ margin:.8rem 0; max-width:95ch; }}
.obj textarea {{ display:block; width:100%; min-height:3rem; margin-top:.3rem; background:#0d1219; color:var(--fg);
  border:1px solid var(--line); border-radius:6px; font:inherit; padding:.4rem; box-sizing:border-box; }}
button {{ background:var(--acc); color:#0b0f14; border:0; border-radius:6px; padding:.5rem 1rem; font:inherit; font-weight:600; cursor:pointer; }}
pre {{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:.6rem .8rem; overflow-x:auto;
  white-space:pre-wrap; font:13px/1.45 ui-monospace,"Cascadia Mono",Consolas,monospace; max-width:115ch; }}
pre .k {{ color:var(--cyan); }} pre .s {{ color:var(--amber); }} pre .c {{ color:var(--mut); font-style:italic; }} pre .b {{ color:var(--violet); }}
#zoom {{ position:fixed; inset:0; background:#000d; display:none; z-index:9; overflow:auto; cursor:zoom-out; }}
#zoom img {{ display:block; margin:1rem auto; max-width:96vw; }}
@media (max-width:1000px) {{ .g2, .g3, .g4, .opts {{ grid-template-columns:1fr; }} .bluf ol {{ columns:1; }} }}
</style></head><body class="s118">
<nav><strong>Milestone marks</strong><a href="#hallazgos">Hallazgos</a><a href="#d1">D1</a><a href="#d2">D2</a>{nav}<a href="#limites">Límites</a><a href="#respuestas">Exportar</a>
<span class="sw">Tamaño: <button data-s="118" class="on">118×30</button><button data-s="80">80×24</button></span></nav>
<main>{"".join(body)}</main>
<div id="zoom"><img alt=""></div>
<script>
const ITEMS = {keys};
// a tiny JSON highlighter for <pre data-lang="json"> (comments, keys, strings, booleans)
document.querySelectorAll('pre[data-lang="json"] code').forEach(el => {{
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  el.innerHTML = el.textContent.split('\\n').map(line => {{
    if (line.trim().startsWith('//')) return '<span class="c">' + esc(line) + '</span>';
    return esc(line).replace(/("(?:[^"\\\\]|\\\\.)*")(\\s*:)?|\\b(true|false|null)\\b/g,
      (m, str, colon, kw) => kw ? '<span class="b">' + kw + '</span>'
        : colon ? '<span class="k">' + str + '</span>' + colon : '<span class="s">' + str + '</span>');
  }}).join('\\n');
}});
document.querySelectorAll('nav .sw button').forEach(b => b.onclick = () => {{
  document.body.className = 's' + b.dataset.s;
  document.querySelectorAll('nav .sw button').forEach(x => x.classList.toggle('on', x === b));
}});
const z = document.getElementById('zoom'), zi = z.querySelector('img');
document.querySelectorAll('figure img').forEach(i => i.onclick = () => {{ zi.src = i.src; z.style.display = 'block'; }});
z.onclick = () => {{ z.style.display = 'none'; }};
// D1 and point 1 are the same question: picking one marks the other
const sync = (a, b) => document.querySelectorAll('input[name="' + a + '"]').forEach(r => r.addEventListener('change', () => {{
  const t = document.querySelector('input[name="' + b + '"][value="' + r.value + '"]'); if (t) t.checked = true; }}));
sync('d1', 'c-model'); sync('c-model', 'd1');
const note = k => document.querySelector('[data-note="' + k + '"]').value.trim();
const radio = n => {{ const c = document.querySelector('input[name="' + n + '"]:checked'); return c ? c.value : null; }};
document.getElementById('export').onclick = async () => {{
  const data = {{ round: 'milestone_marks', branch: 'proto/milestone-marks', decisions: {{}}, items: {{}}, manager: '', notes: '' }};
  const lines = ['Milestone marks round — respuestas'];
  for (const [k, rec] of [['d1', 'B'], ['d2', 'global']]) {{
    const pick = radio(k), obj = document.querySelector('[data-obj="' + k + '"]').checked, txt = note(k);
    data.decisions[k] = {{ choice: pick || rec, chosen_explicitly: !!pick, objects: obj || !!txt, note: txt }};
    lines.push(k.toUpperCase() + ': ' + (pick || rec) + (pick ? '' : ' (recomendada, sin marcar)')
               + ((obj || txt) ? ' · OBJETO' + (txt ? ': ' + txt : '') : ''));
  }}
  for (const [n, key, rec] of ITEMS) {{
    const pick = radio('c-' + key), obj = note(key);
    data.items[n] = {{ key, choice: pick || rec, chosen_explicitly: !!pick, objection: obj }};
    lines.push(n + ' ' + key + ': ' + (pick || rec) + (pick ? '' : ' (recomendada, sin marcar)')
               + (obj ? ' · OBJECIÓN: ' + obj : ''));
  }}
  data.manager = note('manager');
  if (data.manager) lines.push('ventana #: ' + data.manager);
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

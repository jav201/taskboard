"""THROWAWAY — build the verdict page of the capture round from its captures.

    powershell -File prototypes/capture_round/shoot.ps1      (real Windows Terminal PNGs)
    python prototypes/capture_round/build_html.py

Every image is embedded (base64), so the page works opened alone. A missing capture is
printed on the page as missing — never replaced by an SVG. The D2 comparison table and
the HTML-report rendering of item 3 are COMPUTED here from the fixture, not typed.
"""
from __future__ import annotations

import base64
import html
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE))

import fixture as fx  # noqa: E402
import suggest as sg  # noqa: E402
import proto  # noqa: E402
from taskboard.boards import peek_board  # noqa: E402
from taskboard.people import Person  # noqa: E402
from taskboard.views import HEX  # noqa: E402

OUT = HERE / "out"
PAGE = HERE / "capture-round.html"
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


def fig(scene: str, cap: str = "") -> str:
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f"<figure>{c}{shot(scene)}</figure>"


# ---------------------------------------------------------------------------
# computed evidence: the suggester on the fixture, and the report rendering
# ---------------------------------------------------------------------------
def fixture_docs():
    root = Path(tempfile.mkdtemp(prefix="cp-html-"))
    try:
        fx.build(root)
        marks = {i: type("M", (), {"name": n})() for i, n, _s, _c in fx.MARKS}
        boards = []
        for bid, name, col, _rel, _h in fx.BOARDS:
            b = peek_board(fx.board_path(root, bid))
            b.marks = marks
            boards.append((bid, name, col, b))
        return sg.corpus(boards)
    finally:
        shutil.rmtree(root, ignore_errors=True)


DOCS = fixture_docs()
SAMPLES = [t for _i, _a, t in fx.INBOX] + [fx.INBOX_LIVE, "Buy running shoes before the 10k",
                                            "chunk size for the index", "Pay physio invoice"]


def first(t: str) -> str:
    return html.escape(t.split("\n")[0])


def tfidf_cell(note: str) -> str:
    hits = sg.suggest(note, DOCS)
    opts = proto.options(hits)
    top = opts[0]
    if top is None:
        alt = f"<br><span class='mut'>o {html.escape(hits[0].doc.name)} {sg.bars(hits[0].score)}</span>" if hits else ""
        return f"<b class='amb'>+ new project</b>{alt}"
    return (f"<b>{html.escape(top.doc.name)}</b> <span class='mut'>· {top.doc.board}</span> "
            f"<span class='acc'>{sg.bars(top.score)}</span><br>"
            f"<span class='mut'>why: {html.escape(' · '.join(top.why[:3]))}</span>")


def base_cell(rank) -> str:
    d, s = rank[0]
    if not s:
        return "<span class='mut'>nada (0)</span>"
    return f"{html.escape(d.name)} <span class='mut'>({s:.2f})</span>" if isinstance(s, float) \
        else f"{html.escape(d.name)} <span class='mut'>({s} palabra{'s' if s != 1 else ''})</span>"


def timing() -> tuple[float, float, int]:
    t0 = time.perf_counter()
    for _ in range(50):
        for n in SAMPLES:
            sg.suggest(n, DOCS)
    small = (time.perf_counter() - t0) / (50 * len(SAMPLES)) * 1000
    big = [d._replace(order=d.order + 10000 * k, name=f"{d.name} {k}") for k in range(45) for d in DOCS]
    t0 = time.perf_counter()
    for n in SAMPLES:
        sg.suggest(n, big)
    large = (time.perf_counter() - t0) / len(SAMPLES) * 1000
    return small, large, len(big)


def d2_table() -> str:
    rows = []
    for n in SAMPLES:
        rows.append(f"<tr><td>{first(n)}</td><td>{tfidf_cell(n)}</td>"
                    f"<td>{base_cell(sg.suggest_trigram(n, DOCS))}</td>"
                    f"<td>{base_cell(sg.suggest_overlap(n, DOCS))}</td></tr>")
    small, large, nbig = timing()
    stable = all(sg.suggest(n, DOCS) == sg.suggest(n, DOCS) for n in SAMPLES)
    return (f"<div class='tw'><table><tr><th>nota (primera línea)</th><th>M1 · TF-IDF de palabras "
            f"(recomendado)</th><th>M2 · trigramas de letras</th><th>M3 · palabras en común</th></tr>"
            f"{''.join(rows)}</table></div>"
            f"<p class='note'>Calculado al construir esta página sobre los {len(DOCS)} proyectos del "
            f"fixture: {small:.2f}&nbsp;ms por nota; {large:.1f}&nbsp;ms por nota con {nbig} proyectos "
            f"(copias sintéticas). Misma entrada → misma salida: {'sí' if stable else 'NO'} en las "
            f"{len(SAMPLES)} notas.</p>")


PEOPLE = {h: Person(h, n, r) for h, n, r, _note in fx.PEOPLE}
REPORT_CSS_DECK = " ".join(f".deck .hl-{t}{{color:{HEX[t]}}}" for _m, t, _n in proto.PENS)
REPORT_CSS_WS = " ".join(
    f".ws .hl-{t}{{background:color-mix(in srgb,{HEX[t]} 22%,transparent);border-radius:3px;"
    f"padding:0 .15em}}" for _m, t, _n in proto.PENS)


def report_demo() -> str:
    body = proto.report_html_snippet(fx.N_COLOUR, PEOPLE)
    return (f"<div class='grid g2'><div class='card'><h4>Reporte «deck» (texto en color)</h4>"
            f"<div class='rep deck'>{body}</div></div>"
            f"<div class='card'><h4>Reporte «workspace» (fondo teñido)</h4>"
            f"<div class='rep ws'>{body}</div></div></div>"
            f"<p class='note'>HTML real: la función <code>report_html.notes_html</code> del app con el "
            f"tokenizador de seis plumas. Las clases <code>hl-blue</code>, <code>hl-violet</code> y "
            f"<code>hl-orange</code> no existen hoy en el CSS de los reportes; aquí se añaden con los "
            f"mismos tonos de <code>views.HEX</code>.</p>")


# ---------------------------------------------------------------------------
# the decisions, each with its consequences
# ---------------------------------------------------------------------------
DECISIONS = [
    ("d1", "D1 · Una sola bandeja para todos los tableros",
     "La bandeja vive en <code>~/.taskboard/inbox.json</code>, junto a <code>boards.json</code>, "
     "<code>people.json</code> y <code>marks.json</code>, no dentro de cada tablero. Las imágenes "
     "pegadas van a <code>~/.taskboard/inbox/images/&lt;nota&gt;/</code> y se copian a "
     "<code>&lt;tablero&gt;/images/&lt;tarea&gt;/</code> al volcar.",
     ["Capturas antes de saber a qué tablero va: es justo lo que pides (la sugerencia lo decide después).",
      "Las sugerencias ya leen todos los tableros; con una bandeja por tablero, una nota de Client A "
      "capturada con Personal abierto quedaría en el sitio equivocado.",
      "Copiar un <code>board.json</code> a otra máquina no lleva la bandeja; lo no volcado se queda en la máquina "
      "donde lo escribiste.",
      "La sincronización de equipo no ve la bandeja (es personal, como <code>people.json</code>)."]),
    ("d2", "D2 · Sugerencia por TF-IDF de palabras, explicable y estable",
     "Cada proyecto de cada tablero activo es un «documento» con lo que ya tiene: su nombre (peso 3), los "
     "títulos de sus tareas (2), las <code>@personas</code> de sus notas (2), el nombre de la clase de sus hitos "
     "(1) y el texto de sus notas (1). Nota y proyecto se vuelven bolsas de palabras normalizadas (minúsculas, "
     "sin acentos, sin plural, raíz de 6 letras, sin palabras vacías ni números sueltos). Cada palabra pesa más si "
     "pocos proyectos la tienen (TF-IDF) y la puntuación es el coseno. Con una sola palabra en común la puntuación "
     "se divide entre dos. Debajo de ▰▰▱ la sugerencia principal es «+ new project» y los aciertos débiles quedan "
     "como alternativas. Desempate fijo: orden de tableros, luego nombre.",
     ["El «por qué» son las palabras de tu nota que más pesan: <code>why questions · @ana.ruiz · key</code>.",
      "Aprende sin IA: cada nota volcada pasa a ser una tarea del proyecto, así que la siguiente nota parecida "
      "puntúa más alto ahí.",
      "No entiende sinónimos (<em>deck</em> ≠ <em>presentación</em>) ni mezcla de idiomas: si escribes en español "
      "y tus tareas están en inglés, puntúa bajo y ofrece «new project». Es el precio de ser determinista.",
      "Solo lee tableros activos, y en ellos ignora las tareas archivadas.",
      "Comparación medida con dos alternativas en la tabla de abajo."]),
    ("d3", "D3 · Campo nuevo <code>created</code> y orden inferido para lo viejo",
     "<code>Task.created</code>: fecha y hora ISO local con segundos (<code>2026-11-04T08:10:00</code>), escrita "
     "solo si existe (como <code>mark</code>), puesta en un solo sitio: <code>Board.add_task</code>. Las tareas "
     "viejas no se reescriben: al mostrarlas se infiere su orden.",
     ["Con registro <code>from: null</code> en <code>history.jsonl</code> → su hora real, marcada "
      "<code>≈Oct 28 10:30</code> (≈ = viene del historial).",
      "Sin registro → <code>? before Oct 31</code> y su lugar en el archivo del tablero, que es orden de alta "
      "(se añaden al final). Van juntas al final de la lista (o al principio en «oldest first»), agrupadas por "
      "tablero: entre tableros distintos no hay forma honesta de intercalarlas.",
      "Un <code>board.json</code> abierto por una versión vieja del app conserva <code>created</code> (hoy ya se "
      "guarda en <code>Task.extra</code>); el prototipo lo usa así, sin tocar <code>taskboard/</code>.",
      "Riesgo a revisar en la implementación: toda vía que crea tareas sin pasar por <code>add_task</code> "
      "(plantillas, cadenas, sync de equipo) quedaría sin <code>created</code> y se vería como «?»."]),
    ("d4", "D4 · El color se guarda como pares de marcas en el texto",
     "Las tres de hoy siguen igual y se añaden tres: <code>==amarillo==</code> <code>!!rojo!!</code> "
     "<code>++verde++</code> <code>::azul::</code> <code>^^violeta^^</code> <code>%%naranja%%</code>. "
     "<code>highlight_segments</code> sigue siendo el único tokenizador; todas las superficies lo leen. "
     "El rosa queda para las <code>@menciones</code>; seis tonos con saturación alta (sobreviven a la paleta de 256).",
     ["La nota sigue legible fuera del app (un correo, un .txt): las marcas son dos caracteres a cada lado.",
      "Nadie tiene que memorizar las marcas: la pluma, la tecla o el selector las escribe por ti.",
      "<code>::</code> choca con texto técnico (<code>std::vector</code>, IPv6 <code>::1</code>): dos <code>::</code> "
      "en una línea colorean lo de en medio. Igual que hoy pasa con <code>!!</code>.",
      "Los reportes HTML necesitan tres clases CSS nuevas (se ven abajo, ya renderizadas)."]),
]

STORAGE = [
    ("pairs", "S1 · un par por color: <code>::azul::</code>",
     "- ::ask @ana.ruiz for the store list::",
     "Extiende lo que ya existe; el tokenizador crece una alternativa por color. Corto y legible. Coste: "
     "seis símbolos distintos (la interfaz los escribe) y el choque con <code>::</code> técnico."),
    ("named", "S2 · etiqueta con nombre: <code>{blue}…{/}</code>",
     "- {blue}ask @ana.ruiz for the store list{/}",
     "Se explica sola y admite colores ilimitados. Pero es 3–4 veces más larga, parece código en una nota, "
     "y conviviría con las tres marcas de hoy (dos sintaxis para lo mismo)."),
    ("side", "S3 · rangos aparte: texto limpio + <code>colors: [[3,40,\"blue\"]]</code> en la tarea",
     "- ask @ana.ruiz for the store list   (+ task.colors)",
     "El texto queda intacto, pero hay dos fuentes de verdad: editar la nota fuera del app (o por sync) "
     "desplaza los rangos y pinta lo que no era. Cambia el formato del tablero."),
]

ITEMS = [
    (1, "capture", "Captura rápida: una libreta que se vuelve tareas",
     "Postura: en una junta o pensando; escribir tiene que empezar con UNA tecla y cero preparación. "
     "Tecla propuesta: <kbd>n</kbd> (<em>note</em>), libre en <code>taskboard/keymap.py</code> en la pantalla "
     "principal (<kbd>i</kbd> ya es <em>Images</em>). Las tres variantes leen y escriben la misma bandeja "
     "(D1) y usan el mismo sugeridor (D2). Volcar = una tecla: primera línea → título, el resto → notas, "
     "<code>img:</code> → imágenes; menciones y resaltados pasan tal cual. Una nota volcada se pliega en "
     "«dumped» (7 días, con <kbd>alt+u</kbd> deshacer) en vez de borrarse: queda el rastro de a dónde fue cada nota.",
     [("hoy", "Hoy · hay que llenar el editor", [("cap-now", "<kbd>a</kbd>: el editor completo, con proyecto, fase, prioridad y fechas por decidir")],
       "Para apuntar una idea hay que decidir antes proyecto, fase y fechas. Por eso acabas en un bloc aparte y la nota no vuelve."),
      ("A", "A · Libreta + carril de sugerencias", [("cap-A", "<kbd>n</kbd> y escribes; cada bloque separado por una línea en blanco es una nota"),
                                                    ("cap-A-dump", "<kbd>alt+d</kbd>: la nota 4 se vuelve tarea en Pilot rollout; queda plegada en «dumped»"),
                                                    ("cap-A-new", "Nota sin proyecto: <kbd>alt+n</kbd> nombra uno nuevo; <kbd>alt+b</kbd> cambia el tablero")],
       "Escribes libre, como en un bloc: varias notas, varias líneas, imágenes. A la derecha, cada nota con su "
       "proyecto sugerido, el porqué y la confianza; la nota del cursor muestra alternativas. <kbd>alt+o</kbd> "
       "pasa a la siguiente, <kbd>alt+a</kbd> abre el repaso por lotes. A 80 columnas el carril baja y muestra "
       "solo la nota del cursor."),
      ("B", "B · Cajón sobre el tablero con autocompletado", [("cap-B", "<kbd>n</kbd> sobre el kanban: el cajón ocupa la mitad de abajo"),
                                                              ("cap-B-tab", "<kbd>⇥</kbd>: la siguiente sugerencia (2/3)")],
       "El tablero sigue a la vista y la sugerencia aparece bajo lo que escribes, como un autocompletador "
       "(<kbd>⇥</kbd> alterna). <kbd>↵↵</kbd> archiva la nota en la bandeja, <kbd>alt+d</kbd> la vuelca ya. Pero se escribe "
       "una nota a la vez y las anteriores quedan en una línea cada una."),
      ("C", "C · Una línea, una nota", [("cap-C", "<kbd>↵</kbd> añade la nota; una línea que empieza con «-» se suma a la de arriba"),
                                        ("cap-C-rev", "<kbd>alt+r</kbd>: repaso por lotes, cada nota con su destino, <kbd>␣</kbd> incluye, <kbd>d</kbd> vuelca")],
       "Lo más rápido para apuntes de una línea (chat): cada <kbd>↵</kbd> es una nota y la sugerencia sale a la derecha. "
       "Varias líneas solo con el prefijo «-». El repaso por lotes es el mismo que abre A."),
      ],
     "A", "A es la libreta que describes: escribir sin estructura y que la estructura (proyecto) aparezca al lado. "
          "Sugiero que <kbd>n</kbd> abra A y que el repaso por lotes (capturado en C) sea su <kbd>alt+a</kbd>."),
    (2, "list", "Vista de lista: las tareas en el orden en que se agregaron",
     "Todas las tareas de todos los tableros en orden de alta, no por fechas planeadas, con toda su "
     "información. Tecla propuesta: <kbd>N</kbd> (<em>newest</em>: <kbd>n</kbd> escribe, <kbd>N</kbd> lee lo nuevo). Del <kbd>1</kbd> "
     "al <kbd>0</kbd> no queda ninguna y no hay tecla de ciclo de vistas; la lista es global como "
     "<kbd>A</kbd>, <kbd>@</kbd> y <kbd>#</kbd>: pantalla aparte, <kbd>esc</kbd> vuelve a la vista donde estabas, "
     "y aparece en el mapa <kbd>?</kbd>. <kbd>o</kbd> alterna «newest first» / «oldest first». Las horas: "
     "sin marca = campo <code>created</code>; <code>≈</code> = del historial; <code>?</code> = desconocida (D3).",
     [("hoy", "Hoy · solo hay orden por fechas", [("ls-now", "<kbd>2</kbd> Agenda: ordena por fecha planeada")],
       "Ninguna vista responde «¿qué agregué hoy / esta semana?»; una tarea sin fechas no aparece en orden alguno."),
      ("A", "A · Libro de registro, se despliega en el sitio", [("ls-A", "Dos líneas por tarea, agrupadas por día de alta"),
                                                                ("ls-A-open", "<kbd>␣</kbd> despliega la nota completa, enlaces, imágenes y de dónde sale la hora"),
                                                                ("ls-A-old", "<kbd>o</kbd> oldest first: arriba las de alta desconocida, dichas con honestidad")],
       "Se recorre rápido (dos líneas: título + proyecto · tablero; fase, prioridad, fechas, hito, personas, "
       "enlaces, imágenes y el inicio de la nota) y <kbd>␣</kbd> muestra todo sin perder el sitio. "
       "A 80 columnas la hora se acorta y el chip de proyecto se estrecha."),
      ("B", "B · Lista estrecha + panel de detalle", [("ls-B", "La tarea del cursor, completa, a la derecha")],
       "El panel siempre muestra todo de una tarea (nota entera con colores, enlaces, imágenes, dependencias), "
       "sin teclas extra. Pero la lista solo dice hora y título: para comparar dos tareas hay que moverse."),
      ("C", "C · Bitácora con línea de tiempo", [("ls-C", "Cada entrada con su meta y hasta 3 líneas de nota, siempre")],
       "Se lee como un cuaderno: todo visible, sin desplegar. Cuesta 3–5 filas por tarea: en 30 filas caben ~6 tareas."),
      ],
     "A", "A cumple «ver toda la información» sin sacrificar el recorrido: dos líneas bastan para ubicar y "
          "<kbd>␣</kbd> da el resto. La honestidad de las horas (≈ y ?) se ve igual en las tres."),
    (3, "colour", "Notas multicolor",
     "Cambiar de color mientras escribes debe ser tan fácil como cambiar de pluma. Las tres variantes guardan "
     "igual (D4: pares de marcas) y se ven igual en detalle, presentación y reportes; cambia cómo se elige el color. "
     "La misma tarea «Sync notes · Oct 30» lleva una línea por color.",
     [("hoy", "Hoy · tres marcas", [("col-now-ed", "Editor: las marcas en crudo, vista previa en 3 colores; ::, ^^ y %% no se reconocen"),
                                     ("col-now-det", "Detalle: igual")],
       "Hay que saber las marcas de memoria y escribirlas a mano; solo amarillo, rojo y verde."),
      ("A", "A · Seis pares + alt+c recolorea la palabra", [("col-A-ed", "«venue» tras cuatro <kbd>alt+c</kbd>: amarillo → rojo → verde → azul")],
       "<kbd>alt+c</kbd> envuelve la palabra del cursor (o la selección) y cada pulsación pasa al siguiente color, "
       "luego a ninguno. Ideal para colorear después; para escribir una frase entera en color hay que seleccionarla."),
      ("B", "B · Plumas: alt+1…6 y escribes en ese color", [("col-B-ed", "<kbd>alt+4</kbd> azul «call the venue», <kbd>alt+0</kbd>, <kbd>alt+2</kbd> rojo «pay the deposit»")],
       "Es la metáfora del cuaderno: tomas la pluma azul y lo que escribes sale azul, en el propio campo de notas "
       "(las marcas se atenúan). La etiqueta muestra la pluma activa. Cuesta seis combinaciones <kbd>alt+número</kbd> que hay que aprender (están escritas en la etiqueta)."),
      ("C", "C · Selector sobre la selección", [("col-C-ed", "Seleccionas «by friday» y <kbd>alt+c</kbd>: una tecla por color"),
                                                ("col-C-done", "<kbd>r</kbd>: rojo")],
       "Lo más descubrible: no hay nada que recordar salvo <kbd>alt+c</kbd>. Pero son tres pasos (seleccionar, abrir, "
       "elegir) y no sirve para escribir ya en color."),
      ("todas", "Las seis plumas en las demás superficies (igual para A, B y C)",
       [("col-all-det", "Detalle (<kbd>↵</kbd>)"), ("col-all-pr", "Presentación (<kbd>R</kbd> → <kbd>2</kbd>)")],
       "Un solo tokenizador: lo que colorea el editor colorea el detalle, la presentación y los reportes HTML (abajo)."),
      ],
     "B", "B es literalmente «cambiar de pluma» y se ve el color mientras escribes. Sugiero sumarle el "
          "<kbd>alt+c</kbd> de A para recolorear una palabra ya escrita (se complementan; no chocan)."),
]

LIMITS = [
    "Es la <code>TaskboardApp</code> real con pantallas nuevas y el editor subclasificado por escena "
    "(<code>prototypes/capture_round/proto.py</code>); nada en <code>taskboard/</code> cambió.",
    "<kbd>n</kbd> y <kbd>N</kbd> no están en <code>KEYMAP</code> ni en el mapa <kbd>?</kbd>: el prototipo las liga aparte.",
    "<kbd>alt+i</kbd> en la libreta no lee el portapapeles: crea una imagen sintética e inserta su línea "
    "<code>img:</code>. La implementación reutilizaría <code>grab_clipboard_image</code> del editor.",
    "En el cajón (B) <kbd>alt+n</kbd> solo avisa; el campo de proyecto nuevo se capturó en A. El repaso por lotes "
    "no escribe (avisa cuántas volcaría).",
    "La carpeta «dumped» de 7 días y su limpieza no están modeladas; solo el plegado y <kbd>alt+u</kbd>.",
    "Windows Terminal reserva <kbd>alt+enter</kbd> (pantalla completa); por eso ninguna variante lo usa. Las "
    "combinaciones <kbd>alt+número</kbd> de B están libres en la configuración por defecto de WT.",
    "S2 y S3 del formato se muestran como texto, no capturados.",
]


def item_html(n, key, title, problem, variants, rec, rec_text) -> str:
    cards = []
    for val, label, scenes, cons in variants:
        media = "".join(fig(s, cap) for s, cap in scenes)
        is_rec = " rec" if val == rec else ""
        pick = "" if val == "todas" else \
            f'<label class="pick"><input type="radio" name="c-{key}" value="{val}"> Elijo esta</label>'
        cards.append(f'<div class="card{is_rec}"><h4>{label}{" · recomendada" if val == rec else ""}</h4>'
                     f'<div class="media">{media}</div><p>{cons}</p>{pick}</div>')
    return f"""
<section id="i{n}" class="item">
<h2><span class="num">{n}</span> {title}</h2>
<p>{problem}</p>
<div class="grid g2">{"".join(cards)}</div>
<div class="box"><strong>Recomendación: {rec}.</strong> {rec_text}</div>
{report_demo() if key == "colour" else ""}
<div class="obj"><label>Objeción u otra idea para el punto {n} (opcional)</label>
<textarea data-note="{key}" placeholder="Solo si objetas algo"></textarea></div>
</section>"""


def decisions_html() -> str:
    out = []
    for key, title, what, cons in DECISIONS:
        li = "".join(f"<li>{c}</li>" for c in cons)
        extra = ""
        if key == "d2":
            extra = "<p class='lab'>Los tres métodos sobre las notas del fixture</p>" + d2_table()
        if key == "d4":
            rows = "".join(
                f'<tr class="{"rec" if k == "pairs" else ""}"><td><label><input type="radio" name="c-storage" value="{k}"> '
                f'{t}{" · recomendada" if k == "pairs" else ""}</label></td><td><code>{html.escape(ex)}</code></td><td>{c}</td></tr>'
                for k, t, ex, c in STORAGE)
            extra = (f"<p class='lab'>Formas de guardar el color</p><div class='tw'><table><tr><th>forma</th>"
                     f"<th>texto guardado</th><th>consecuencias</th></tr>{rows}</table></div>")
        out.append(f"""<div class="dec" id="{key}"><h3>{title}</h3><p>{what}</p>
<p class="lab">Consecuencias</p><ul>{li}</ul>{extra}
<div class="obj"><label><input type="checkbox" data-obj="{key}"> Objeto</label>
<textarea data-note="{key}" placeholder="Qué cambiarías (vacío = de acuerdo)"></textarea></div></div>""")
    return "".join(out)


def main() -> None:
    ex = sg.suggest(fx.INBOX[0][2], DOCS)[0]
    example = (f"→ {ex.doc.name} · {ex.doc.board} {sg.bars(ex.score)} · why "
               f"{' · '.join(ex.why[:3])}")
    recs = "".join(f"<li><a href='#i{n}'>{n} · {t}</a> → <strong>{r}</strong></li>"
                   for n, _k, t, _p, _v, r, _rt in ITEMS)
    body = [f"""
<h1>Ronda de captura · libreta rápida, lista por orden de alta y notas multicolor</h1>
<div class="box bluf"><p><strong>En corto:</strong> <kbd>n</kbd> abre una libreta global donde escribes sin
preparar nada; cada bloque separado por una línea en blanco es una nota, y al lado aparece el proyecto al que
probablemente pertenece, con el porqué (<code>{html.escape(example)}</code>). Una tecla la vuelca como tarea; si no hay proyecto,
lo creas ahí mismo. <kbd>N</kbd> abre la lista de todas las tareas en el orden en que se agregaron, diciendo
con honestidad cuáles tienen hora real, cuáles inferida (≈) y cuáles desconocida (?). Y las notas pasan de
3 a 6 colores, elegidos como plumas. Capturas reales en Windows Terminal a 118×30 y 80×24 (cambia el tamaño
arriba). Mi recomendación:</p><ol class="recs">{recs}</ol>
<p>Decisiones: <strong>D1</strong> bandeja global · <strong>D2</strong> TF-IDF de palabras, sin IA ·
<strong>D3</strong> campo <code>created</code> + orden inferido sin reescribir lo viejo ·
<strong>D4</strong> pares de marcas (<code>::azul::</code>, <code>^^violeta^^</code>, <code>%%naranja%%</code>).
Marca <em>Elijo esta</em> por punto (vacío = acepto la recomendada), escribe solo lo que objetas y pulsa
<strong>Exportar respuestas</strong> al final.</p></div>
<blockquote class="ask">«Me di cuenta de algo... para hacer una tarea el tiempo que se toma hacer el setup es ya
considerable..., hay veces que estoy tomando notas y sólo puedo hacer como en un scratchpad y después ya no vuelvo
la información al taskboard... será que haya una manera más sencilla de simplemente escribir, volcar imágenes y tener
una especie de parser (o usar un ngram o por similitud de palabras, algo determinista) para que según las notas me
sugiera volcar la información a un task de un proyecto? (es decir que el autocompletador ya me sugiera el proyecto donde
pertenece, si no, crear uno nuevo ahí mismo) ya me lo imagino como una lista de notas random, divididas por línea (para
separar tópicos) y tener la opción de volcar... y veo que me hace falta también una vista de lista precisamente, donde
vea las tareas pero como se fueron agregando, no por las fechas dispuestas de planeación, donde vea toda la
información... y me gustaría que las notas acepten color... que sea fácil de hacer ese cambio, para tener el texto
multicolor, eso es algo que uso en mis cuadernos.»</blockquote>
<p class="note">Datos sintéticos: tres tableros (Personal, Client A, Course), seis personas, tres notas en la bandeja
y una cuarta escrita en vivo por el guion. Hoy fijado en miércoles 4 de noviembre; <code>created</code> existiría
desde el 31 de octubre. Teclas reales pulsadas por el guion.</p>
<section id="decisiones"><h2>Decisiones de diseño (D1–D4)</h2>
<p>Las tomé para poder prototipar; cada una con lo que implica. Marca <em>Objeto</em> y escribe solo si no estás de acuerdo.</p>
{decisions_html()}</section>"""]
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
<title>Capture round</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722; --amb:#fbbf24; }}
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
h3 {{ margin:.2rem 0 .4rem; font-size:1.05rem; color:var(--acc); }}
h4 {{ margin:.2rem 0 .4rem; font-size:1rem; }}
.num {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px; padding:0 .5rem; }}
p, li {{ max-width:90ch; }}
code, kbd {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
.mut {{ color:var(--mut); }} .acc {{ color:var(--acc); }} .amb {{ color:var(--amb); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:110ch; margin:1rem 0; }}
.bluf ol {{ margin:.4rem 0; }}
.ask {{ border-left:3px solid var(--amb); margin:1rem 0; padding:.4rem 1rem; color:var(--mut); max-width:110ch; font-style:italic; }}
.note {{ color:var(--mut); font-size:.92rem; }}
.dec {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.7rem 1rem; margin:1rem 0; max-width:130ch; }}
.dec .lab, .lab {{ color:var(--mut); font-size:.85rem; margin:.6rem 0 0; text-transform:uppercase; letter-spacing:.04em; }}
.dec ul {{ margin:.2rem 0 .4rem; }}
.grid {{ display:grid; gap:1rem; align-items:start; }}
.g2 {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
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
table {{ border-collapse:collapse; margin:.6rem 0; font-size:.9rem; }}
th, td {{ border:1px solid var(--line); padding:.35rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--mut); }}
tr.rec td:first-child {{ border-left:3px solid var(--acc); }}
.rep {{ font:14px/1.6 ui-monospace,Consolas,monospace; background:#0d1117; padding:.6rem .8rem; border-radius:6px; }}
.rep .hl-mut {{ color:#c9d4e0; }} .rep .mention {{ color:var(--acc); font-weight:600; }}
{REPORT_CSS_DECK}
{REPORT_CSS_WS}
.ws .hl-mut {{ background:none; }}
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
@media (max-width:1000px) {{ .g2 {{ grid-template-columns:1fr; }} }}
</style></head><body class="s118">
<nav><strong>Capture round</strong><a href="#decisiones">D1–D4</a>{nav}<a href="#limites">Límites</a><a href="#respuestas">Exportar</a>
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
  const data = {{ round: 'capture_round', branch: 'proto/capture-list-colour', decisions: {{}}, storage: {{}}, items: {{}}, notes: '' }};
  const lines = ['Capture round — respuestas'];
  for (const k of DECS) {{
    const obj = document.querySelector('[data-obj="' + k + '"]').checked, txt = note(k);
    data.decisions[k] = {{ objects: obj || !!txt, note: txt }};
    lines.push(k.toUpperCase() + ': ' + ((obj || txt) ? 'OBJETO' + (txt ? ' · ' + txt : '') : 'de acuerdo'));
  }}
  const s = document.querySelector('input[name="c-storage"]:checked');
  data.storage = {{ choice: s ? s.value : 'pairs', chosen_explicitly: !!s }};
  lines.push('formato del color: ' + data.storage.choice + (s ? '' : ' (recomendado, sin marcar)'));
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
    PAGE.write_text(page, encoding="utf-8", newline="\n")
    print(PAGE, f"{PAGE.stat().st_size // 1024} KB · images", len(USED), "· missing:", MISSING)


if __name__ == "__main__":
    main()

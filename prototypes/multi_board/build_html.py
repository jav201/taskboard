"""THROWAWAY — build the verdict page from the app captures (SVGs embedded as
base64, so the page works opened alone).

    python prototypes/multi_board/app_capture.py
    python prototypes/multi_board/build_html.py
"""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PAGE = HERE / "multi-board-prototype.html"
USED: set[str] = set()


def img(name: str, cap: str) -> str:
    USED.add(name)
    data = base64.b64encode((OUT / f"{name}.svg").read_bytes()).decode()
    return (f'<figure><figcaption>{cap}</figcaption>'
            f'<img alt="" loading="lazy" src="data:image/svg+xml;base64,{data}"></figure>')


VARIANTS = {
    "A": ("Selector modal",
          "<kbd>B</kbd> abre una lista de tableros encima del tablero actual: color, nombre, abiertas, "
          "▲ atrasadas, la próxima fecha con su tarea y cuándo lo abriste. Escribes para filtrar, "
          "<kbd>↑↓</kbd> y <kbd>↵</kbd> cambias. Crear, renombrar/recolorear y archivar viven aquí "
          "(<kbd>^n</kbd> <kbd>^e</kbd> <kbd>^x</kbd>).",
          "Ganas: cero filas permanentes; escala a 20 tableros (filtras); idéntico a 80 y a 160.",
          "Cedes: no ves cómo van los otros tableros hasta que lo abres; cambiar son 2–3 teclas."),
    "B": ("Pestañas",
          "Una tira arriba con todos los tableros: el activo en su color, los demás con su marca de "
          "color y ▲ atrasadas. <kbd>&lt;</kbd> / <kbd>&gt;</kbd> recorren; los dígitos siguen siendo "
          "las vistas. <kbd>B</kbd> abre el selector de A para crear/editar.",
          "Ganas: siempre sabes qué hay y dónde hay atraso, sin abrir nada; cambiar al vecino es 1 tecla.",
          "Cedes: una fila fija en cada vista; ir del 1.º al 4.º son 3 teclas; con más de ~6 tableros "
          "los nombres se recortan."),
    "C": ("Inicio con tarjetas",
          "Una pantalla de tarjetas, una por tablero: abiertas, ▲ atrasadas, cuántas vencen esta "
          "semana, una <strong>tira de vencimientos de 4 semanas dibujada</strong> (alto = cuántas "
          "vencen ese día), las próximas fechas y, si cabe, sus proyectos. Sale al arrancar si hay "
          "más de un tablero (cursor en el último usado) y con <kbd>B</kbd>.",
          "Ganas: comparas la presión de cada contexto de un vistazo sin mezclarlos; es la mejor "
          "respuesta a «¿qué sombrero me pongo hoy?».",
          "Cedes: una pantalla más al arrancar (un <kbd>↵</kbd>); a 80 × 24 cada tarjeta solo muestra "
          "la próxima fecha; con más de 6 tableros hay que desplazarse."),
}

SIZES = [("160", "160 × 45 · tu tamaño"), ("118", "118 × 30"), ("80", "80 × 24")]

PROPOSALS = [
    ("P1", "Un archivo por tablero, cada uno en su carpeta, y un registro pequeño",
     """<p>Hallazgo al leer el código: <code>history.jsonl</code> (lo que lee la vista Flow),
<code>images/</code> y <code>reports/</code> viven <strong>junto al archivo del tablero</strong>
(<code>history.py:21</code>, <code>models.py:948</code>, <code>report.py:272</code>). Dos tableros en la
misma carpeta mezclarían su historial y sus reportes. Por eso P1 es <strong>una carpeta por
tablero</strong>, no solo un archivo.</p>
<div class="two"><div><h4>Hoy</h4><pre>~/.taskboard/
  board.json          todo mezclado
  history.jsonl
  images/  reports/</pre></div>
<div><h4>Propuesto (nada se mueve solo)</h4><pre>~/.taskboard/
  boards.json         <b>nuevo</b>: nombre, ruta, color, último uso
  board.json          «Main» = tu tablero de hoy, en su sitio
  history.jsonl  images/  reports/   (de Main, igual que hoy)
  boards/
    personal/board.json            + su history, images, reports
    client-retail-rag/board.json
    course-docker/board.json</pre></div></div>
<p class="gain">Un archivo dañado afecta un solo tablero; el modo equipo (su carpeta compartida va en los
<code>settings</code> de cada tablero), los reportes, el historial y los respaldos siguen siendo por
tablero sin cambiar una línea de esa lógica.</p>
<p class="give">Una tarea no puede esperar a otra de otro tablero (ver P3). El registro es un archivo
más que mantener; si falta, el app abre <code>board.json</code> como hoy.</p>"""),
    ("P2", "Abre en el último tablero usado; su nombre y color siempre a la vista",
     """<p>El nombre va como una <strong>etiqueta de color al inicio de la fila de encabezado</strong> que
ya tiene cada vista (la de <code>◆ TASKBOARD</code>, <code>◆ GANTT</code>…): cero filas nuevas, visible
en todas las vistas. En B la tira de pestañas cumple ese papel. Abajo: hoy vs. propuesto, mismo tablero.</p>
<div class="two">{before}{after}</div>
<p class="give">Con C, «abre en el último» se vuelve «abre el inicio con el cursor en el último»: un
<kbd>↵</kbd> más (pregunta 1).</p>"""),
    ("P3", "«Mover proyecto a tablero…» para partir el tablero mezclado",
     """<p>En <kbd>P</kbd> (Projects) una tecla nueva, <kbd>m</kbd>: eliges proyecto → tablero destino →
confirmación que <strong>lista cada link que cruza</strong> y dice que se quitará. Se mueve el proyecto con
todas sus tareas (también las hechas), los links internos se conservan, sus líneas de
<code>history.jsonl</code> y sus imágenes viajan con él, y antes de escribir se respaldan los dos
archivos. Secuencia completa en <a href="#mover">Mover un proyecto</a>.</p>
<p class="give">Mover no entra en <kbd>u</kbd> deshacer (toca dos archivos): el respaldo
<code>board.json.pre-move-FECHA</code> es la vuelta atrás.</p>"""),
    ("P4", "Crear, renombrar/recolorear y archivar desde el selector; <code>--board</code> sigue igual",
     """<p>Crear pide nombre y uno de los 8 colores de proyecto, y enseña la ruta que se va a crear
(<code>~/.taskboard/boards/&lt;nombre&gt;/board.json</code>). Archivar oculta el tablero del selector y no
toca su carpeta. <code>taskboard --board RUTA</code> abre ese archivo y lo agrega al registro si no estaba.</p>
<div class="two">{create1}{create2}</div>
<p class="give">El tablero nuevo abre vacío con la rejilla vacía que el app ya dibuja hoy: no hay una
indicación de «agrega tu primer proyecto con <kbd>p</kbd>» (hallazgo, ver límites).</p>"""),
]

KEYS = [
    ("<kbd>B</kbd>", "Abre el selector (A, B) o el inicio (C).",
     "En <code>keymap.py</code> solo existe <kbd>b</kbd> minúscula (Blocked); <kbd>B</kbd> no está en "
     "el asiento. Mnemónico: Boards. Se declara <code>universal</code>: en la barra nunca es la tecla "
     "que se cae."),
    ("<kbd>&lt;</kbd> <kbd>&gt;</kbd>", "Solo B: tablero anterior / siguiente.",
     "Ninguna entrada usa <code>less_than_sign</code>/<code>greater_than_sign</code>; <kbd>,</kbd> "
     "(guardar plantilla en Chains) es otra tecla. En teclado latinoamericano <kbd>&lt;</kbd> está junto "
     "al shift izquierdo."),
    ("<kbd>A</kbd>", "Solo la opción D: agenda de todos los tableros.",
     "<kbd>a</kbd> minúscula es Add; <kbd>A</kbd> está libre. Solo paleta y <kbd>?</kbd>, no barra."),
    ("<kbd>m</kbd> en <kbd>P</kbd>", "Mover el proyecto del cursor a otro tablero.",
     "El modal Projects usa <kbd>e</kbd> <kbd>x</kbd> <kbd>d</kbd> <kbd>j</kbd> <kbd>k</kbd>; "
     "<kbd>m</kbd> está libre ahí (en la pantalla principal <kbd>m</kbd> es Chain, no se toca)."),
    ("<kbd>^n</kbd> <kbd>^e</kbd> <kbd>^x</kbd>", "Dentro del selector A: nuevo, nombre/color, archivar.",
     "Con Ctrl porque las letras van al filtro. En el inicio C no hay campo de texto, así que son "
     "<kbd>n</kbd> <kbd>e</kbd> <kbd>x</kbd> sin Ctrl."),
]

LIMITS = [
    "<strong>Los avisos (toasts) no salen en las capturas.</strong> El de «Moved … · 7 tasks · 3 links "
    "kept · 2 dropped» se emite pero <code>run_test</code> no lo pinta.",
    "<strong>El registro y el movimiento son código de prototipo</strong> (<code>mb_proto.py</code>): sin "
    "validación de <code>boards.json</code>, sin choque de ids entre tableros (los ids del app son "
    "aleatorios), sin bloqueo si otro proceso tiene abierto el tablero destino.",
    "<strong>Modo equipo no se ejercitó.</strong> Mover un proyecto compartido deja su id en "
    "<code>team.json</code> del tablero viejo; la implementación tiene que negarlo o avisar.",
    "<strong><kbd>B</kbd> bajo un modal.</strong> En el app real hay que agregar <code>boards</code> a las "
    "acciones que se liberan cuando hay un modal (<code>check_action</code>), o abriría el selector "
    "encima de Present.",
    "<strong>Hora fija.</strong> «opened 2h ago» se calcula contra las 09:30 del 20-oct-2026; los datos son "
    "sintéticos.",
    "<strong>Bordes gruesos.</strong> La tarjeta elegida de C usa borde <code>heavy</code>; el SVG lo dibuja "
    "punteado con la fuente del navegador, en la terminal es línea gruesa.",
    "<strong>B con muchos tableros.</strong> La tira recorta nombres a 12 / 7 / 4 / 1 letras según quepan; "
    "con 4 tableros nunca se activa, así que ninguna captura lo muestra.",
]

QUESTIONS = [
    ("Con C, ¿al arrancar ves el inicio o entras directo al último tablero?",
     "El inicio, solo si hay más de un tablero, con el cursor en el último usado: entrar es un "
     "<kbd>↵</kbd> y ganas la vista de presión de todos los contextos antes de elegir."),
    ("Los links que cruzan tableros al mover un proyecto: ¿se quitan o se guardan como referencia?",
     "Se quitan, con confirmación y con la lista escrita en <code>move-FECHA.json</code> junto a cada "
     "tablero. Un link entre archivos rompe el aislamiento de P1 y ni el modo equipo ni los reportes "
     "sabrían resolverlo."),
    ("¿La opción D (agenda de todos) entra?",
     "No en el núcleo. Si la quieres después: solo lectura, detrás de <kbd>A</kbd>, nunca como vista "
     "de arranque, y <kbd>↵</kbd> te lleva a la tarea <em>en su tablero</em>."),
]


def main() -> None:
    ev = json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))
    cards = "".join(
        f'<div class="card"><h3><span class="tag">{v}</span> {n}</h3><p>{d}</p>'
        f'<p class="gain">{g}</p><p class="give">{x}</p></div>'
        for v, (n, d, g, x) in VARIANTS.items())
    grid = []
    for size, cap in SIZES:
        cells = "".join(
            f'<div class="cell"><h4><span class="tag">{v}</span> {VARIANTS[v][0]}</h4>'
            + img(f"{v}-{size}-open", f"{v} · {cap}") + "</div>" for v in "ABC")
        grid.append(f'<h3 class="v">{cap}</h3><div class="tri">{cells}</div>')
    switched = "".join([
        img("A-160-filter", "A · escribir «do» deja solo «Course · Docker», con la coincidencia subrayada"),
        img("A-160-switched", "A · <kbd>B</kbd> <kbd>↓</kbd> <kbd>↵</kbd>: ahora en «Client · Retail RAG»; "
            "la etiqueta de color abre la fila de encabezado"),
        img("B-160-switched", "B · <kbd>&gt;</kbd>: la pestaña activa pasa a «Client · Retail RAG»"),
        img("C-160-switched", "C · <kbd>→</kbd> <kbd>↵</kbd> en el inicio: entra a «Client · Retail RAG»"),
        img("C-160-switched-gantt", "Misma etiqueta en cualquier vista (aquí <kbd>3</kbd> Gantt)"),
    ])
    props = []
    for pid, title, body in PROPOSALS:
        body = body.format(
            before=img("before-160-today", "Hoy: el encabezado no dice qué archivo estás viendo"),
            after=img("move-160-0-main-before", "Propuesto: la etiqueta «Main» en su color abre la fila"),
            create1=img("create-160-1-form", "<kbd>B</kbd> <kbd>^n</kbd>: nombre, color con <kbd>⇥</kbd>, "
                        "y la ruta que se creará"),
            create2=img("create-160-2-created", "<kbd>↵</kbd>: se crea la carpeta y el tablero abre vacío"))
        props.append(f'<div class="prop" id="{pid}"><h3><span class="tag">{pid}</span> {title}</h3>'
                     f'{body}</div>')
    move = "".join([
        img("move-160-1-projects", "1 · <kbd>P</kbd> en «Main», cursor en «Retail RAG · pilot»; la fila "
            "de título anuncia <kbd>m</kbd>"),
        img("move-160-2-target", "2 · <kbd>m</kbd>: ¿a qué tablero? (los otros tres, con su tamaño); "
            "<kbd>↓</kbd> a «Client · Retail RAG»"),
        img("move-160-3-confirm", "3 · <kbd>↵</kbd>: confirmación. 7 tareas, 3 links internos se quedan, "
            "<strong>2 links cruzan</strong> y se nombran uno por uno"),
        img("move-160-4-moved", "4 · <kbd>↵</kbd>: hecho; la lista de Projects ya no lo tiene"),
        img("move-160-5-main-after", "5 · «Main» después: 4 proyectos, 12 abiertas (antes 17)"),
        img("move-160-6-client-after", "6 · «Client · Retail RAG» después: el proyecto llegó con sus 7 "
            "tareas y su color"),
    ])
    tree_b = html.escape(ev["tree_before"])
    tree_a = html.escape(ev["tree_after"])
    keys = "".join(f"<tr><td>{k}</td><td>{w}</td><td>{why}</td></tr>" for k, w, why in KEYS)
    limits = "".join(f"<li>{x}</li>" for x in LIMITS)
    qs = "".join(f"<li><strong>{q}</strong><br>Recomiendo: {a}</li>" for q, a in QUESTIONS)

    def obj(key: str, label: str, ph: str) -> str:
        return (f'<div class="obj"><label><input type="checkbox" data-obj="{key}"> Objeto a '
                f'<strong>{label}</strong></label>'
                f'<textarea data-note="{key}" placeholder="{ph}"></textarea></div>')

    choose = "".join(
        f'<label class="pick"><input type="radio" name="variant" value="{v}"> Elijo '
        f'<strong>{v} · {VARIANTS[v][0]}</strong></label>' for v in "ABC") + (
        '<label class="pick"><input type="radio" name="variant" value="mix"> Elijo una '
        '<strong>combinación</strong> (dime cuál en notas)</label>')
    objs = "".join([
        obj("P1", "P1 · una carpeta por tablero + boards.json", "¿Qué cambiarías del disco?"),
        obj("P2", "P2 · último tablero + etiqueta en el encabezado", "¿Dónde quieres ver el tablero activo?"),
        obj("P3", "P3 · mover proyecto, links que cruzan se quitan", "¿Qué no te convence del flujo?"),
        obj("P4", "P4 · crear / editar / archivar desde el selector", ""),
        obj("A", "A · Selector modal (aunque no la elijas)", ""),
        obj("B", "B · Pestañas (aunque no la elijas)", ""),
        obj("C", "C · Inicio con tarjetas (aunque no la elijas)", ""),
        obj("D", "D · agenda de todos los tableros (opción)", "¿La quieres? ¿así?"),
        obj("keys", "las teclas (B, &lt; &gt;, A, m, ^n ^e ^x)", ""),
    ])

    body = f"""
<h1>Varios tableros en taskboard</h1>
<div class="box"><strong>Conclusión.</strong> Recomiendo <strong>C · Inicio con tarjetas</strong> como
el selector: al arrancar (si hay más de un tablero, cursor en el último usado) y con <kbd>B</kbd>. Es la
única variante que <em>dibuja</em> la presión de cada contexto — atrasadas y una tira de vencimientos de
4 semanas por tablero — sin mezclarlos, y a 160 × 45 las cuatro tarjetas caben con sus próximas cinco
fechas. Con P1–P4 como están: una carpeta por tablero (el historial, imágenes y reportes ya viven junto
al archivo), tu <code>board.json</code> se queda como «Main» sin mover nada, y lo partes con
<kbd>P</kbd> → <kbd>m</kbd>. Si no quieres una pantalla al arrancar, la segunda opción es
<strong>A</strong>: la más barata y la que mejor escala.</div>

<h2 id="pedido">Lo que pediste</h2>
<blockquote>«La aplicación funciona como un excelente visor de tareas para project management. Me ha
servido muchísimo… me di cuenta que necesito tener configurados varios boards. Hago boards para varios
proyectos de distintas disciplinas además de mis tareas personales. Entonces todo está mezclado y no
necesariamente debería serlo. Así que requiero prototipar este aumento.»</blockquote>
<p>Hoy: un solo archivo (<code>~/.taskboard/board.json</code>); otro archivo solo con
<code>taskboard --board RUTA</code> y sin cambiar dentro del app. Esta ronda: cuatro tableros sintéticos
— «Personal», «Client · Retail RAG», «Course · Docker» y «Main», el tablero mezclado a partir. Cada
captura es el <code>TaskboardApp</code> real con teclas reales (<code>run_test</code>); nada en
<code>taskboard/</code> cambió. Haz clic en una captura para verla en grande.</p>

<h2 id="decisiones">Decisiones propuestas (por consecuencia)</h2>
<p>Ya están tomadas como punto de partida; marca abajo solo lo que objetas.</p>
{"".join(props)}

<h2 id="variantes">El selector: tres variantes</h2>
<div class="cards">{cards}</div>
<p class="note">Las tres abren sobre «Personal» (el último usado). A y C ponen la etiqueta del tablero en
el encabezado de cada vista; B la reemplaza por la tira.</p>
{"".join(grid)}
<h3 class="v">Después de cambiar (160 × 45)</h3>
<div class="two">{switched}</div>

<h2 id="mover">Mover un proyecto: partir «Main» (160 × 45)</h2>
<p>«Retail RAG · pilot» vive en «Main» pero es trabajo del cliente. Dos links lo cruzan: «Case study:
retail RAG» (Agency website, se queda) espera a «Pilot results deck» (se va), y «Demo env on Docker» (se
va) espera a «Compose template» (Docker labs, se queda).</p>
<div class="two">{move}</div>
<div class="two"><div><h4>Carpeta antes (leída del disco de la captura)</h4><pre>{tree_b}</pre></div>
<div><h4>Carpeta después</h4><pre>{tree_a}</pre></div></div>
<p class="note">Los tableros sintéticos no tienen <code>history.jsonl</code> ni imágenes, por eso no
aparecen; el código del prototipo sí los mueve cuando existen.</p>

<h2 id="d">Opción D: agenda de todos los tableros (no es parte del núcleo)</h2>
<p>Una sola lista de solo lectura — atrasadas, hoy, resto de la semana — cada fila con el color y nombre
de su tablero; <kbd>↵</kbd> abre la tarea en su tablero. Va contra el espíritu de «separar», por eso es
opción: sirve el lunes por la mañana, no para trabajar.</p>
<div class="two">{img("D-160-open", "D · 160 × 45 (<kbd>A</kbd>)")}{img("D-80-open", "D · 80 × 24: sin columna de proyecto; lo que no cabe se corta")}</div>

<h2 id="teclas">Teclas y por qué están libres</h2>
<table><tr><th>Tecla</th><th>Hace</th><th>Por qué está libre</th></tr>{keys}</table>

<h2 id="observaciones">Lo que vi en cada tamaño</h2>
<ul>
<li><strong>A</strong> se lee igual en los tres tamaños; a 80 corta el título de la próxima tarea. Tapa la
parte de arriba del tablero mientras está abierto, que es lo esperado en un modal.</li>
<li><strong>B</strong> cabe completa aun a 80 × 24 con 4 tableros (nombres enteros y ▲). Su costo es la
fila fija: a 80 × 24 es 1 de 22 filas útiles. En la barra de teclas a 80, <kbd>&lt;</kbd>
<kbd>&gt;</kbd> pierden su palabra.</li>
<li><strong>C</strong> a 160 × 45 llena la mitad superior (4 tarjetas, 5 fechas y proyectos); la mitad de abajo
queda libre — hay sitio para 2 tableros más sin desplazarse. A 118 × 30 pasa a 3 fechas; a 80 × 24 a 1
fecha y «this week» en vez de «due this week».</li>
<li>La etiqueta de color en el encabezado (P2) se ve en todas las vistas sin costar una fila; con un color
de tablero igual al de un proyecto (Client = sky = su proyecto) se distingue porque es un bloque de fondo,
no una barra.</li>
</ul>

<h2 id="limites">Lo que esta ronda no representa fielmente</h2>
<ul>{limits}</ul>

<h2 id="preguntas">Preguntas abiertas</h2>
<ol>{qs}</ol>

<h2 id="respuestas">Tus respuestas</h2>
<p><strong>1. ¿Cuál variante eliges?</strong> (esto es una elección, no una objeción)</p>
<div class="picks">{choose}</div>
<p><strong>2. Objeciones.</strong> Marca solo lo que objetas; lo que no marques lo tomo como aceptado.</p>
{objs}
<div class="obj"><label>Respuestas a las preguntas abiertas u otras notas</label>
<textarea data-note="notas" placeholder="Notas libres"></textarea></div>
<button id="export">Exportar respuestas</button> <span id="done"></span>
"""
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Multi-board prototype</title>
<style>
:root {{ --bg:#0b0f14; --fg:#d7dee7; --mut:#8b98a5; --line:#233041; --acc:#2dd4bf; --panel:#101722; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:#0d1219ee; border-bottom:1px solid var(--line);
  padding:.6rem 16px; display:flex; gap:1rem; flex-wrap:wrap; font-size:.9rem; }}
nav a, main a {{ color:var(--acc); text-decoration:none; }}
main {{ max-width:1500px; margin:0 auto; padding:1rem 16px 4rem; }}
h1 {{ font-size:1.6rem; margin:1rem 0 .6rem; }}
h2 {{ margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1.2rem; }}
h3 {{ font-size:1.05rem; margin:.4rem 0; }}
h3.v {{ font-size:1.2rem; margin-top:1.8rem; }}
h4 {{ margin:.2rem 0; font-size:.95rem; }}
.tag {{ display:inline-block; background:var(--acc); color:#0b0f14; border-radius:4px;
  padding:0 .45rem; font-family:ui-monospace,Consolas,monospace; }}
p, li, blockquote {{ max-width:85ch; }}
blockquote {{ border-left:3px solid var(--line); margin:0; padding:.2rem 1rem; color:var(--mut); font-style:italic; }}
code, kbd {{ font-family:ui-monospace,Consolas,monospace; background:#151c26; padding:0 .25em; border-radius:3px; }}
kbd {{ border:1px solid var(--line); }}
pre {{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:.6rem .8rem;
  overflow-x:auto; font:13px/1.45 ui-monospace,Consolas,monospace; }}
pre b {{ color:var(--acc); }}
.box {{ border-left:3px solid var(--acc); padding:.6rem 1rem; background:var(--panel); max-width:95ch; }}
.prop {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.6rem 1rem; margin:1rem 0; }}
.note {{ color:var(--mut); font-size:.92rem; }}
.cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:.6rem 1rem; }}
.card p {{ margin:.4rem 0; font-size:.94rem; }}
.gain::before {{ content:"+ "; color:var(--acc); font-weight:700; }}
.give::before {{ content:"− "; color:#f43f5e; font-weight:700; }}
.tri {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; align-items:start; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; align-items:start; }}
figure {{ margin:.6rem 0; }}
figure img {{ width:100%; height:auto; display:block; border-radius:6px; cursor:zoom-in; background:#0d1117; }}
figcaption {{ color:var(--mut); font-size:.85rem; margin-bottom:.3rem; }}
table {{ border-collapse:collapse; margin:1rem 0; font-size:.92rem; max-width:110ch; }}
th, td {{ border:1px solid var(--line); padding:.3rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--mut); }}
.picks {{ display:flex; flex-direction:column; gap:.4rem; margin:.4rem 0 1rem; }}
.pick {{ background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:.4rem .8rem; max-width:60ch; }}
.obj {{ margin:.8rem 0; max-width:85ch; }}
.obj textarea {{ display:block; width:100%; min-height:3rem; margin-top:.3rem; background:var(--panel);
  color:var(--fg); border:1px solid var(--line); border-radius:6px; font:inherit; padding:.4rem; box-sizing:border-box; }}
button {{ background:var(--acc); color:#0b0f14; border:0; border-radius:6px; padding:.5rem 1rem; font:inherit; font-weight:600; cursor:pointer; }}
#zoom {{ position:fixed; inset:0; background:#000d; display:none; z-index:9; overflow:auto; cursor:zoom-out; }}
#zoom img {{ display:block; margin:1rem auto; max-width:none; width:min(1900px,180vw); }}
@media (max-width:900px) {{ .tri, .two, .cards {{ grid-template-columns:1fr; }} }}
</style></head><body>
<nav><strong>Varios tableros</strong><a href="#pedido">Pedido</a><a href="#decisiones">P1–P4</a>
<a href="#variantes">Variantes</a><a href="#mover">Mover proyecto</a><a href="#d">Opción D</a>
<a href="#teclas">Teclas</a><a href="#limites">Límites</a><a href="#preguntas">Preguntas</a>
<a href="#respuestas">Respuestas</a></nav>
<main>{body}</main>
<div id="zoom"><img alt=""></div>
<script>
const z = document.getElementById('zoom'), zi = z.querySelector('img');
document.querySelectorAll('figure img').forEach(i => i.onclick = () => {{ zi.src = i.src; z.style.display = 'block'; }});
z.onclick = () => {{ z.style.display = 'none'; }};
document.getElementById('export').onclick = async () => {{
  const out = ['Varios tableros — respuestas'];
  const v = document.querySelector('input[name=variant]:checked');
  out.push('VARIANTE ELEGIDA: ' + (v ? v.value : '(sin elegir)'));
  const objs = [];
  document.querySelectorAll('[data-obj]').forEach(el => {{
    const note = document.querySelector('[data-note="' + el.dataset.obj + '"]');
    const txt = note && note.value.trim() ? ' — ' + note.value.trim() : '';
    if (el.checked) objs.push('OBJECIÓN ' + el.dataset.obj + txt);
    else if (txt) objs.push('nota ' + el.dataset.obj + txt);
  }});
  out.push(...(objs.length ? objs : ['Sin objeciones: acepto P1–P4 como están.']));
  const n = document.querySelector('[data-note="notas"]').value.trim();
  if (n) out.push('NOTAS: ' + n);
  const txt = out.join('\\n');
  try {{ await navigator.clipboard.writeText(txt); document.getElementById('done').textContent = 'Copiado.'; }}
  catch (e) {{ window.prompt('Copia el texto:', txt); }}
}};
</script>
</body></html>
"""
    PAGE.write_text(page, encoding="utf-8")
    produced = {p.stem for p in OUT.glob("*.svg")}
    print(PAGE, f"{PAGE.stat().st_size // 1024} KB", "embedded", len(USED), "of", len(produced),
          "missing:", sorted(produced - USED))


if __name__ == "__main__":
    main()

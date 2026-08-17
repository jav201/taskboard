"""PROTOTYPE — keybar layout variants.

    python prototypes/keybar_ideas/proto.py

Throwaway: renders proposed keybars as SVG terminal captures + a single-file
HTML comparison. No shipping code touched.
"""
from __future__ import annotations

import html as H
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rich.console import Console                                               # noqa: E402
from rich.text import Text                                                     # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
W = 118

# palette matches taskboard/views.py HEX
HEX = {
    "frame": "#334154",
    "mut": "#8b98a5",
    "dim": "#5b6675",
    "ink": "#e6edf3",
    "hd": "#c9d4e0",
    "accent": "#2dd4bf",
    "violet": "#a78bfa",
    "sky": "#38bdf8",
    "amber": "#fbbf24",
    "rose": "#fb7185",
    "green": "#4ade80",
    "orange": "#fb923c",
    "lime": "#a3e635",
    "cyan": "#22d3ee",
    "blue": "#60a5fa",
    "indigo": "#818cf8",
    "fuchsia": "#e879f9",
    "pink": "#f472b6",
    "over": "#f43f5e",
    "ash": "#6b4a3f",
    "bright": "#e6edf7",
    "soon": "#fbbf24",
    "later": "#64748b",
    "done": "#3f9c6d",
}


def markup_key(key: str, color: str = "accent") -> str:
    return f"[{HEX[color]}]{key}[/]"


def markup_label(label: str, color: str = "mut") -> str:
    return f"[{HEX[color]}]{label}[/]"


def entry(key: str, label: str, key_color: str = "accent", label_color: str = "mut") -> str:
    return f"{markup_key(key, key_color)} {markup_label(label, label_color)}"


def sep() -> str:
    return f"[{HEX['frame']}]│[/]"


# ---------------------------------------------------------------------------
# current single-row bar as rendered by keymap.py
# ---------------------------------------------------------------------------
def current_bar() -> str:
    from taskboard.keymap import render_key_bar
    return render_key_bar(W, "kanban")


# ---------------------------------------------------------------------------
# Option A — two-row grouped bar
# ---------------------------------------------------------------------------
def two_row_bar() -> str:
    # Row 1: navigation, views, primary task ops
    row1_parts = [
        entry("?", "Keys", "amber"), entry("q", "Quit", "rose"),
        sep(),
        entry("1", "Lanes"), entry("2", "Agenda"), entry("3", "Gantt"), entry("4", "Kanban"), entry("6", "Widget", "violet"),
        sep(),
        entry("↵", "Open"), entry("a", "Add"), entry("e", "Edit"), entry("d", "Del", "rose"),
        sep(),
        entry("↓↑←→", "Nav"),
    ]
    # Row 2: kanban + advanced ops (abbreviated to fit 118 cols)
    row2_parts = [
        entry("[", "Ph-"), entry("]", "Ph+"),
        sep(),
        entry("!", "Prio"), entry("b", "Blk"), entry("+", "Due+"), entry("-", "Due-"),
        sep(),
        entry("s", "Sort"), entry("g", "Group"), entry("z", "Coll"), entry("F", "Focus"), entry("esc", "Off", "sky"),
        sep(),
        entry("x", "Arch"), entry("X", "Purge"), entry("v", "Archvd"), entry("u", "Und", "amber"),
        sep(),
        entry("o", "URL"), entry("i", "Img"), entry("p", "Proj+"), entry("P", "Ps"), entry("f", "Phs"), entry("c", "Clk"), entry("R", "Rep"), entry("S", "Std"),
    ]
    return "\n".join(["  ".join(row1_parts), "  ".join(row2_parts)])


# ---------------------------------------------------------------------------
# Option B — compact one-row with category badges and overflow hint
# ---------------------------------------------------------------------------
def compact_bar() -> str:
    parts = [
        f"[{HEX['frame']}]▐[/]{markup_key('?', 'amber')} {markup_label('keys', 'amber')}[{HEX['frame']}]▌[/]",
        entry("q", "quit", "rose", "rose"),
        sep(),
        f"[{HEX['violet']}]1-4[/] {markup_label('views', 'violet')}",
        entry("6", "widget", "violet", "violet"),
        sep(),
        entry("↵", "open"), entry("a", "add"), entry("e", "edit"), entry("d", "del", "rose"),
        sep(),
        entry("[", "ph-"), entry("]", "ph+"), entry("!", "prio"), entry("b", "blk"),
        sep(),
        f"[{HEX['sky']}]s/g/z[/] {markup_label('kanban', 'sky')}",
        entry("F", "focus", "sky", "sky"), entry("esc", "off", "sky", "sky"),
        sep(),
        entry("+", "due+"), entry("-", "due-"), entry("u", "undo", "amber"),
        sep(),
        entry("↓↑←→", "nav"),
        sep(),
        f"[{HEX['mut']}]x/X/v/o/i/p/P/f/c/R/S ?[/] {markup_label('more', 'mut')}",
    ]
    return "  ".join(parts)


# ---------------------------------------------------------------------------
# Option C — dedicated cheat-sheet panel (rendered as a modal body)
# ---------------------------------------------------------------------------
def cheat_sheet() -> str:
    sections = [
        ("NAVIGATION", [
            ("↓/j", "down"), ("↑/k", "up"), ("←/h", "left"), ("→/l", "right"), ("⇥", "layout"),
        ], "mut"),
        ("VIEWS", [
            ("1", "lanes"), ("2", "agenda"), ("3", "gantt"), ("4", "kanban"), ("6", "widget"),
        ], "violet"),
        ("TASK", [
            ("↵", "details"), ("a", "add"), ("e", "edit"), ("d", "delete"), ("x", "archive"),
            ("X", "purge done"), ("v", "archived"), ("u", "undo"),
        ], "accent"),
        ("PHASE / PRIORITY", [
            ("[", "phase back"), ("]", "phase forward"), ("!", "cycle priority"), ("b", "toggle blocked"),
        ], "sky"),
        ("KANBAN", [
            ("s", "sort"), ("g", "group"), ("z", "collapse"), ("F", "focus project"), ("esc", "focus off"),
        ], "cyan"),
        ("DATE", [
            ("+", "due +1d"), ("-", "due -1d"),
        ], "amber"),
        ("MISC", [
            ("o", "URL"), ("i", "images"), ("p", "new project"), ("P", "projects"), ("f", "phases"),
            ("c", "clocks"), ("R", "report"), ("S", "standup"),
        ], "green"),
        ("SYSTEM", [
            ("?", "this help"), ("q", "quit"),
        ], "rose"),
    ]
    lines = []
    for title, pairs, color in sections:
        lines.append(f"[{HEX[color]}]{title}[/]")
        for key, label in pairs:
            lines.append(f"  {markup_key(key, color)} {markup_label(label)}")
        lines.append("")
    return "\n".join(lines).rstrip()


# ---------------------------------------------------------------------------
# Option D — mini keyboard map in the footer (novel / visual)
# ---------------------------------------------------------------------------
def mini_keyboard() -> str:
    """A 60% keyboard layout where used keys are coloured by category.

    The user sees WHERE the keys live on the keyboard, not just a list.
    Below the board, a one-line legend maps colours to categories."""

    def k(ch: str, color: str | None = None) -> str:
        base = f"[{HEX['frame']}]▢[/]" if color is None else f"[{HEX[color]}]{ch}[/]"
        return base

    # Row by row of a compact keyboard; empty slots are grey squares.
    rows = [
        "      " + "  ".join([
            k("1", "violet"), k("2", "violet"), k("3", "violet"), k("4", "violet"),
            k("6", "violet"), k("", None), k("", None), k("", None), k("", None), k("", None),
            k("-", "amber"), k("=", "amber"),
        ]) + "     " + k("", None),
        "  " + "  ".join([
            k("", None), k("q", "rose"), k("", None), k("e", "accent"), k("r", "green"),
            k("", None), k("", None), k("i", "green"), k("o", "green"), k("p", "green"),
            k("[", "sky"), k("]", "sky"),
        ]) + "   " + k("", None) + " " + k("", None),
        " " + "  ".join([
            k("", None), k("a", "accent"), k("b", "sky"), k("c", "green"), k("d", "accent"),
            k("", None), k("g", "cyan"), k("", None), k("", None),
            k("", None), k("", None), k("s", "cyan"),
        ]) + "   " + k("↵", "accent") + "  " + k("", None),
        "   " + "  ".join([
            k("x", "green"), k("", None), k("v", "green"), k("", None),
            k("", None), k("", None), k("", None), k("", None),
            k(",", None), k(".", None), k("/", None),
        ]) + "      " + k("↑", "mut"),
        "     " + k("", None) + "       " + k("F", "cyan") + "            " + k("", None) + "  " +
        k("←", "mut") + " " + k("↓", "mut") + " " + k("→", "mut"),
    ]
    legend = (
        f"  {markup_key('q', 'rose')} quit   "
        f"{markup_key('1-4', 'violet')} views   "
        f"{markup_key('ae', 'accent')} task   "
        f"{markup_key('[]!b', 'sky')} phase/prio   "
        f"{markup_key('sgzF', 'cyan')} kanban   "
        f"{markup_key('+-', 'amber')} date   "
        f"{markup_key('oriOpcRS', 'green')} misc   "
        f"{markup_key('arrows', 'mut')} nav   "
        f"{markup_key('?', 'amber')} full map"
    )
    return "\n".join(rows + ["", legend])


# ---------------------------------------------------------------------------
# Option E — command palette (novel / fast)
# ---------------------------------------------------------------------------
def command_palette() -> str:
    """A fuzzy command palette summoned by ? (or ctrl+p).

    Type to filter; arrow keys move; enter runs. No need to memorise keys."""
    lines = [
        f"[{HEX['frame']}]╭────────────────────────────────────────────────────────────────────────────────────────╮[/]",
        f"[{HEX['frame']}]│[/] [{HEX['accent']}]›[/] [{HEX['ink']}]due[/] [{HEX['mut']}]· 7 matches[/]                                                                         [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]├────────────────────────────────────────────────────────────────────────────────────────┤[/]",
        f"[{HEX['frame']}]│[/] [{HEX['accent']}]▸ +  Due +1 day[/]                                                                       [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]│[/]   -  Due -1 day                                                                       [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]│[/]   [  Phase back                                                                       [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]│[/]   ]  Phase forward                                                                     [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]│[/]   F  Focus project                                                                    [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]│[/]   s  Sort kanban                                                                      [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]│[/]   g  Group kanban                                                                     [{HEX['frame']}]│[/]",
        f"[{HEX['frame']}]╰────────────────────────────────────────────────────────────────────────────────────────╯[/]",
        "",
        f"[{HEX['mut']}]esc/ctrl+c close   ↓↑ select   ↵ run   type to filter[/]",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Option F — layered keybar: press ; to see related commands
# ---------------------------------------------------------------------------
def layered_normal() -> str:
    return "  ".join([
        entry("?", "map", "amber"), entry(";", "more", "violet"),
        sep(),
        entry("1", "Lanes"), entry("2", "Agenda"), entry("3", "Gantt"), entry("4", "Kanban"),
        sep(),
        entry("a", "Add"), entry("e", "Edit"), entry("d", "Del"),
        sep(),
        entry("↓↑←→", "Nav"),
        sep(),
        entry("↵", "Open"),
    ])


def layered_more() -> str:
    return "  ".join([
        f"[{HEX['violet']}]modo ; activo[/]",
        sep(),
        entry("[", "Ph-"), entry("]", "Ph+"), entry("!", "Prio"), entry("b", "Blk"),
        sep(),
        entry("s", "Sort"), entry("g", "Group"), entry("z", "Coll"), entry("F", "Focus"),
        sep(),
        entry("+", "Due+"), entry("-", "Due-"), entry("u", "Undo"),
        sep(),
        entry("x", "Arch"), entry("X", "Purge"), entry("v", "Archvd"),
        sep(),
        entry("o", "URL"), entry("i", "Img"), entry("p", "Proj+"), entry("P", "Ps"), entry("f", "Phs"), entry("c", "Clk"), entry("R", "Rep"), entry("S", "Std"),
        sep(),
        entry("esc", "cancel"),
    ])


# ---------------------------------------------------------------------------
# Final proposal — E + F: command palette + layered bar
# ---------------------------------------------------------------------------
def final_ef_normal() -> str:
    return layered_normal()


def final_ef_more() -> str:
    return layered_more()


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def svg(text: str, slug: str, title: str) -> str:
    con = Console(record=True, width=W + 2, legacy_windows=False,
                  color_system="truecolor")
    con.print(text, soft_wrap=True)
    s = con.export_svg(title=title)
    s = re.sub(r'\s*url\("https://[^"]+"\) format\("woff2?"\),?', "", s)
    s = re.sub(r",(\s*;)", r"\1", s)
    (OUT / f"{slug}.svg").write_text(s, encoding="utf-8")
    return s


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    variants = [
        ("current", "ACTUAL · una fila, saturada", current_bar()),
        ("tworow", "A · dos filas agrupadas por categoría", two_row_bar()),
        ("compact", "B · una fila compacta con badges de categoría", compact_bar()),
    ]
    svgs = {slug: svg(text, slug, title) for slug, title, text in variants}

    # taller panels get their own render
    sheet_svg = svg(cheat_sheet(), "cheatsheet", "C · panel dedicado de ayuda")
    mini_svg = svg(mini_keyboard(), "mini", "D · mini mapa de teclado")
    palette_svg = svg(command_palette(), "palette", "E · command palette")
    layered_normal_svg = svg(layered_normal(), "layered_normal", "F · barra por capas · normal")
    layered_more_svg = svg(layered_more(), "layered_more", "F · barra por capas · modo ;")

    final_ef_normal_svg = svg(final_ef_normal(), "final_ef_normal", "PROPUESTA FINAL · E+F · barra normal")
    final_ef_more_svg = svg(final_ef_more(), "final_ef_more", "PROPUESTA FINAL · E+F · modo ;")
    final_ef_palette_svg = svg(command_palette(), "final_ef_palette", "PROPUESTA FINAL · E+F · command palette (?)")

    html_parts = [
        '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">',
        '<title>taskboard — propuestas de keybar</title>',
        '<style>',
        'body{margin:0;background:#0b0f14;color:#c9d1d9;font:14px/1.6 ui-monospace,Consolas,monospace}',
        '.wrap{max-width:1240px;margin:0 auto;padding:30px 20px 80px}',
        'h1{font-size:22px} h2{font-size:16px;color:#2dd4bf;margin:2em 0 .3em}',
        'p{color:#7d8790;max-width:90ch;margin:.2em 0 10px}',
        'figure{margin:0;border:1px solid #1f2733;border-radius:6px;overflow:hidden;background:#000}',
        'figure svg{display:block;width:100%;height:auto}',
        '.note{color:#565f68;font-size:12px}',
        '.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}',
        '</style></head><body><div class="wrap">',
        '<h1>Keybar — propuestas de layout</h1>',
        '<p>El keybar actual muestra ~38 bindings en una sola fila; a 118 columnas pierde las etiquetas y termina siendo una sopa de caracteres. Primero las opciones clásicas y luego tres propuestas más novedosas.</p>',
    ]
    for slug, title, _ in variants:
        html_parts.append(f'<section><h2>{H.escape(title)}</h2><figure>')
        html_parts.append(svgs[slug])
        html_parts.append('</figure></section>')

    html_parts.append('<section><h2>C · panel dedicado de ayuda (se abre con ?)</h2>')
    html_parts.append('<p>Reemplaza la pantalla modal actual por un panel flotante agrupado por categorías. La barra inferior puede quedar en cualquiera de las opciones anteriores.</p>')
    html_parts.append('<figure>')
    html_parts.append(sheet_svg)
    html_parts.append('</figure></section>')

    html_parts.append('<section><h2>D · mini mapa de teclado en la barra inferior</h2>')
    html_parts.append('<p>En lugar de una lista, dibujamos un teclado 60% donde cada tecla usada brilla con el color de su categoría. Abajo, una leyenda de una línea. Muy visual y ayuda a memorizar la ubicación física.</p>')
    html_parts.append('<figure>')
    html_parts.append(mini_svg)
    html_parts.append('</figure></section>')

    html_parts.append('<section><h2>E · command palette con búsqueda difusa</h2>')
    html_parts.append('<p>Presionas <code>?</code> (o <code>ctrl+p</code>) y escribes lo que quieres hacer. No hace falta saber la tecla de antemano. Ideal para usuarios nuevos y para comandos poco frecuentes.</p>')
    html_parts.append('<figure>')
    html_parts.append(palette_svg)
    html_parts.append('</figure></section>')

    html_parts.append('<section><h2>F · barra por capas (modo <code>;</code>)</h2>')
    html_parts.append('<p>La barra muestra solo lo esencial. Al mantener/presionar <code>;</code> cambia a una segunda capa con el resto de comandos. Mantiene la interfaz limpia sin sacrificar descubrimiento.</p>')
    html_parts.append('<div class="pair"><figure>')
    html_parts.append(layered_normal_svg)
    html_parts.append('</figure><figure>')
    html_parts.append(layered_more_svg)
    html_parts.append('</figure></div></section>')

    html_parts.append('<section><h2>PROPUESTA FINAL · E + F</h2>')
    html_parts.append('<p>La barra base muestra lo esencial: <code>?</code> abre el command palette, <code>;</code> activa la segunda capa. El palette permite buscar cualquier comando sin memorizar teclas; la segunda capa da acceso rápido a todo cuando ya sabes qué hacer.</p>')
    html_parts.append('<div class="pair"><figure>')
    html_parts.append(final_ef_normal_svg)
    html_parts.append('</figure><figure>')
    html_parts.append(final_ef_more_svg)
    html_parts.append('</figure></div>')
    html_parts.append('<figure>')
    html_parts.append(final_ef_palette_svg)
    html_parts.append('</figure></section>')

    html_parts.append('</div></body></html>')
    (OUT / "keybar-ideas.html").write_text("\n".join(html_parts), encoding="utf-8")
    print(f"wrote {OUT / 'keybar-ideas.html'}")


if __name__ == "__main__":
    main()

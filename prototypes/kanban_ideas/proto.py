"""PROTOTYPE — visual variants for the kanban improvement proposals (K1-K4).

    python prototypes/kanban_ideas/proto.py

Throwaway: renders the REAL kanban view (taskboard/views.py) against the
SYNTHETIC fixture (never the live board), monkeypatching ONLY the grouping
function per variant, and writes one SVG per variant + a single-file HTML
to compare them. No persistence, no edits to shipping code.
"""
from __future__ import annotations

import html as H
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rich.console import Console                                   # noqa: E402

from taskboard import views as V                                   # noqa: E402
from taskboard.models import Board, parse_iso                     # noqa: E402

FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"
OUT = Path(__file__).resolve().parent / "out"
W, HGT = 118, 30

PRIO = {"high": 0, "normal": 1, "low": 2}
TODAY = date(2026, 8, 14)          # frozen: the fixture's "today" (render determinism)


def load() -> Board:
    return Board.load(str(FIXTURE))


def render(board: Board) -> Text:  # noqa: F821
    return V.render_view("kanban", board, False, None, today=TODAY,
                         width=W, height=HGT, line_map={}, presentation="grouped")


def svg(markup, slug: str, title: str) -> str:
    # NO force_terminal: with it, this rich (15.0.0) re-detects the terminal
    # and IGNORES width=120 — every capture came out 81 cells wide and the
    # third phase column was silently clipped off the figures (measured:
    # con.size -> 80 with the param set). color_system alone keeps the hues.
    con = Console(record=True, width=W + 2, legacy_windows=False,
                  color_system="truecolor")
    con.print(markup, soft_wrap=True)  # soft_wrap: rich re-wraps at 80 even
    s = con.export_svg(title=title)    # with width=118, mangling column edges
    # offline: drop the cdnjs Fira Code url()s, keep local()+monospace
    s = re.sub(r'\s*url\("https://[^"]+"\) format\("woff2?"\),?', "", s)
    s = re.sub(r",(\s*;)", r"\1", s)
    (OUT / f"{slug}.svg").write_text(s, encoding="utf-8")
    return s


# ---- grouping overrides (the ONLY thing monkeypatched) ----------------------

def flat(sort_key):
    def grouper(board, tasks, show_archived):
        return [("", "dim", sorted(tasks, key=sort_key))]
    return grouper


def by_priority(board, tasks, show_archived):
    out = []
    for p, label, col in (("high", "ALTA", "over"), ("normal", "NORMAL", "mut"),
                          ("low", "BAJA", "dim")):
        items = sorted((t for t in tasks if t.priority == p),
                       key=lambda t: (parse_iso(t.due_date) is None,
                                      parse_iso(t.due_date) or TODAY))
        if items:
            out.append((label, col, items))
    return out


def by_horizon(board, tasks, show_archived):
    def bucket(t):
        d = parse_iso(t.due_date)
        if d is None:
            return 3
        dd = (d - TODAY).days
        return 0 if dd < 0 else (1 if dd <= 7 else 2)
    out = []
    for b, label, col in ((0, "VENCIDA", "over"), (1, "ESTA SEMANA", "accent"),
                          (2, "DESPUÉS", "mut"), (3, "SIN FECHA", "dim")):
        items = sorted((t for t in tasks if bucket(t) == b),
                       key=lambda t: (parse_iso(t.due_date) is None,
                                      parse_iso(t.due_date) or TODAY))
        if items:
            out.append((label, col, items))
    return out


def sort_prio(t):
    return (not t.blocked, PRIO[t.priority],
            parse_iso(t.due_date) is None, parse_iso(t.due_date) or TODAY)


def sort_due(t):
    return (not t.blocked, parse_iso(t.due_date) is None,
            parse_iso(t.due_date) or date(2999, 1, 1), PRIO[t.priority])


# ---- second batch: WIP limits, aging, collapse, focus, standup --------------

WIP_LIMIT = {"Doing": 3}


def wip_header(board, start, widths):
    """K5: the phase header COUNTS, and burns when the column is over its
    WIP limit — the one rule kanban has and this board does not draw."""
    buckets = phase_buckets(board, board.visible_tasks(False))
    cells = []
    for i, wc in enumerate(widths):
        ph = board.phases[start + i]
        n = len(buckets[start + i])
        lim = WIP_LIMIT.get(ph)
        tag = f" {n}/{lim}" if lim else f" {n}"
        over = lim is not None and n > lim
        cells.append(V.c(V.escape(V.fit(ph.upper(), wc - len(tag))), "hd", bold=True)
                     + V.c(tag, "over" if over else "mut"))
    return cells


def aged(board: Board) -> Board:
    """Inject phase_changed dates into the fixture (it predates the field) so
    K6 has something to say; then render titles as `title ·Nd`."""
    spread = {"Fix checkout 500 error": 2, "Renew TLS certificate": 12,
              "Write API reference": 5, "Compress database backups": 1,
              "Deprecate v1 endpoints": 21, "Plan Q3 roadmap": 30,
              "Design homepage mockups": 3, "Audit dependencies": 9}
    from datetime import timedelta
    for t in board.visible_tasks(False):
        if t.title in spread:
            t.phase_changed = str(TODAY - timedelta(days=spread[t.title]))
    return board


def aging_card(original):
    def wrapper(task, board, wc, selected, **kw):
        d = parse_iso(getattr(task, "phase_changed", None))
        if d is not None and not board.is_done(task):
            days = (TODAY - d).days
            import dataclasses
            task = dataclasses.replace(task, title=f"{task.title} ·{days}d")
        return original(task, board, wc, selected, **kw)
    return wrapper


def collapse_done(board, tasks, wc, selected_id, show_archived):
    """K7: a phase you never operate collapses to ONE summary row."""
    if tasks and all(board.is_done(t) for t in tasks):
        return [(V.c(f"✓ {len(tasks)} completadas · colapsada (`u` expande)",
                     "dim"), None)]
    return _REAL_COL_ROWS(board, tasks, wc, selected_id, show_archived)


def focus_project(name):
    def grouper(board, tasks, show_archived):
        items = [t for t in tasks
                 if (p := board.project_by_id(t.project_id)) and p.name == name]
        return [(name, "accent", items)] if items else []
    return grouper


def standup_markup(board: Board):
    """K11: the week, derived from phase_changed — what moved, per project."""
    from datetime import timedelta
    week_ago = TODAY - timedelta(days=7)
    lines = [V.c("STANDUP · semana al ", "accent", bold=True) + V.c(str(TODAY), "mut"),
             ""]
    moved = [t for t in board.visible_tasks(False)
             if (d := parse_iso(t.phase_changed)) and d >= week_ago]
    by_proj: dict[str, list] = {}
    for t in moved:
        p = board.project_by_id(t.project_id)
        by_proj.setdefault(p.name if p else "Inbox", []).append(t)
    for name, items in by_proj.items():
        done = [t for t in items if board.is_done(t)]
        lines.append(V.c(f"▐ {name}", "accent", bold=True))
        for t in items:
            mark = "✓" if board.is_done(t) else "→"
            lines.append(f"  {mark} {V.escape(t.title)}"
                         + V.c(f"   {t.phase}", "mut"))
        lines.append(V.c(f"  {len(done)}/{len(items)} cerradas esta semana", "dim"))
        lines.append("")
    if not moved:
        lines.append(V.c("  nada se movió esta semana", "dim"))
    return "\n".join(lines)


VARIANTS = []        # (slug, title, note, [svg,...])
_REAL_GROUPS = V._kanban_groups
_REAL_COL_ROWS = V._kanban_column_rows
_REAL_HEADER = V._windowed_header
_REAL_CARD = V.card_cell
phase_buckets = V.phase_buckets


def capture(slug: str, title: str, note: str, renders: list) -> None:
    svgs = [svg(m, f"{slug}{'' if len(renders) == 1 else '_' + 'abc'[i]}",
                title) for i, m in enumerate(renders)]
    VARIANTS.append((slug, title, note, svgs))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # V0 — the board as it ships today
    capture("v0", "V0 · kanban actual (referencia)",
            "Agrupado por proyecto dentro de cada fase, orden de alta. "
            "Así se ve hoy — las variantes siguientes cambian UNA cosa.",
            [render(load())])

    # K2 — flat sorts (single group: an honest sort admits no sub-groups)
    V._kanban_groups = flat(sort_prio)
    capture("k2p", "K2a · ordenar por prioridad (tecla s)",
            "Bloqueadas primero (▲), luego alta→normal→baja (`!` = alta), "
            "vencimiento como desempate. El `▐` de color sigue diciendo el "
            "proyecto, así no se pierde esa lectura.",
            [render(load())])
    V._kanban_groups = flat(sort_due)
    capture("k2d", "K2b · ordenar por vencimiento (tecla s)",
            "Lo más urgente arriba en cada columna; sin fecha al final. "
            "Misma tecla, segundo estado del ciclo.",
            [render(load())])

    # K3 — alternative groupings
    V._kanban_groups = by_priority
    capture("k3p", "K3a · agrupar por prioridad (tecla g)",
            "Sub-grupos ALTA / NORMAL / BAJA dentro de cada fase. Agrupar "
            "en vez de ordenar: cada bloque queda compacto y con etiqueta.",
            [render(load())])
    V._kanban_groups = by_horizon
    capture("k3h", "K3b · agrupar por horizonte (tecla g)",
            "VENCIDA / ESTA SEMANA / DESPUÉS / SIN FECHA. La lectura "
            "'qué me urge' sin salir del kanban.",
            [render(load())])
    V._kanban_groups = _REAL_GROUPS  # restore the real one for the interactions

    # K1 — move between phases with [ / ]  (before -> after)
    b1, b2 = load(), load()
    t = next(t for t in b2.visible_tasks(False)
             if t.title == "Renew TLS certificate")
    b2.set_task_phase(t, "Doing")
    capture("k1", "K1 · mover entre fases con [ ] (antes → después)",
            "La seleccionada salta de columna SIN abrir el modal, y el movimiento "
            "queda fechado (set_task_phase). Aquí: 'Renew TLS certificate' "
            "Backlog → Doing.",
            [render(b1), render(b2)])

    # K4 — quick priority / blocked on the selected task (before -> after)
    b3, b4 = load(), load()
    t2 = next(t for t in b4.visible_tasks(False)
              if t.title == "Write API reference")
    t2.priority, t2.blocked = "high", True
    capture("k4", "K4 · `!` prioridad y `b` bloqueo al instante (antes → después)",
            "'Write API reference' pasa a alta+bloqueada sin modal: gana el "
            "marcador `!` y el prefijo ▲. Con K2/K3 estos dos gestos reordenan "
            "el tablero en dos teclas.",
            [render(b3), render(b4)])

    # ---- SECOND BATCH -------------------------------------------------------
    # K5 — WIP limits burn in the phase header
    V._windowed_header = wip_header
    capture("k5", "K5 · WIP limits en el header de fase",
            "Doing tiene límite 3 y hay 4: el contador `4/3` se enciende. La "
            "única regla que el kanban tiene y este tablero no dibuja. "
            "(K5 no toca tarjetas, sólo el header.)",
            [render(load())])
    V._windowed_header = _REAL_HEADER

    # K6 — aging: how long each card has sat in its phase
    V.card_cell = aging_card(_REAL_CARD)
    capture("k6", "K6 · aging — cuánto lleva cada tarjeta sentada",
            "El `·Nd` sale de `phase_changed`, que ya se fecha solo al mover. "
            "'Deprecate v1 endpoints ·21d' y 'Plan Q3 roadmap ·30d' se delatan "
            "solas. (Fechas inyectadas en el fixture, que es anterior al campo.)",
            [render(aged(load()))])
    V.card_cell = _REAL_CARD

    # K7 — collapse the phase you never operate
    V._kanban_column_rows = collapse_done
    capture("k7", "K7 · Done colapsada a una fila",
            "La columna que nunca operas deja de pagar ancho: `✓ N completadas` "
            "en una fila, `u` la expande. Mira la columna Done contra V0.",
            [render(load())])
    V._kanban_column_rows = _REAL_COL_ROWS

    # K8 — focus mode: one project only
    V._kanban_groups = focus_project("API Platform")
    capture("k8", "K8 · focus mode — un solo proyecto",
            "Una tecla cicla el foco por proyecto: el tablero entero filtra a "
            "'API Platform'. Para trabajar en una cosa con cinco proyectos "
            "abiertos. (`Esc` o ciclar hasta salir lo quita.)",
            [render(load())])
    V._kanban_groups = _REAL_GROUPS

    # K11 — weekly standup, derived from phase_changed
    capture("k11", "K11 · standup semanal (modal in-app)",
            "Qué se movió y qué se cerró esta semana, por proyecto — todo "
            "derivado de `phase_changed`, sin guardar nada nuevo. El reporte "
            "`R` ya existe en HTML; esto es la versión de una tecla, in-app.",
            [standup_markup(aged(load()))])

    # ---- FOUR PHASES, like the real board ------------------------------------
    def four_phases() -> Board:
        b = load()
        b.add_phase("Review")           # inserted before Done? no — appended;
        # move two tasks there so the column has something to say
        for title, ph in (("Audit dependencies", "Review"),
                          ("Design homepage mockups", "Review")):
            t = next(t for t in b.visible_tasks(False) if t.title == title)
            b.set_task_phase(t, ph)
        return b

    capture("x4", "V0 · kanban actual con 4 fases (como tu board)",
            "El fixture con una fase extra ('Review', tareas de Doing movidas "
            "ahí). Las 4 columnas caben a 118 celdas; a menos ancho la ventana "
            "de fases pagina con ◀ N / N ▶, como ya hace la app.",
            [render(four_phases())])

    V._kanban_groups = flat(sort_prio)
    capture("k2px4", "K2a con 4 fases · ordenar por prioridad",
            "El orden es POR COLUMNA: da igual que haya 3, 4 o 7 fases — cada "
            "una ordena su contenido. Lo mismo aplica a K3 (agrupar), K5 (WIP "
            "por fase), K6 (aging) y K7 (colapsar la fase que elijas).",
            [render(four_phases())])
    V._kanban_groups = _REAL_GROUPS

    # ---- the single-file comparison page ------------------------------------
    secs = []
    for slug, title, note, svgs in VARIANTS:
        figs = "".join(f'<figure>{s}</figure>' for s in svgs)
        cls = "pair" if len(svgs) > 1 else ""
        secs.append(f'<section><h2>{H.escape(title)}</h2><p>{H.escape(note)}</p>'
                    f'<div class="{cls}">{figs}</div></section>')
    page = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>taskboard kanban — prototipos K1-K4</title>
<style>
body{{margin:0;background:#0b0f14;color:#c9d1d9;font:14px/1.6 ui-monospace,Consolas,monospace}}
.wrap{{max-width:1240px;margin:0 auto;padding:30px 20px 80px}}
h1{{font-size:22px}} h2{{font-size:16px;color:#2dd4bf;margin:2em 0 .3em}}
p{{color:#7d8790;max-width:90ch;margin:.2em 0 10px}}
figure{{margin:0;border:1px solid #1f2733;border-radius:6px;overflow:hidden;background:#000}}
figure svg{{display:block;width:100%;height:auto}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.note{{color:#565f68;font-size:12px}}
</style></head><body><div class="wrap">
<h1>Kanban — prototipos de las propuestas K1–K11</h1>
<p>Renders del kanban REAL (taskboard/views.py) sobre el fixture sintético de
15 tareas — no tu board. Cada variante cambia una sola cosa respecto a V0.
Nada de esto está implementado: es el prototipo para decidir. K1–K4 ya están
aprobadas; K5–K11 son la tanda nueva.</p>
{''.join(secs)}
<p class="note">Generado por prototypes/kanban_ideas/proto.py (descartable) ·
{len(VARIANTS)} propuestas · fixture _fixture_late.json · colores del tema real de la app.</p>
</div></body></html>"""
    dest = OUT / "kanban-ideas.html"
    dest.write_text(page, encoding="utf-8")
    # VERIFY: balanced svg tags, no external resource, all sections present
    assert page.count("<svg") == page.count("</svg>") == len(
        [s for _, _, _, sv in VARIANTS for s in sv])
    assert not re.search(r'(src|href)="(https?:)?//', page)
    assert not re.search(r'url\("?(https?:)?//', page)
    assert page.rstrip().endswith("</html>")
    print(f"OK  {dest}  ({dest.stat().st_size // 1024} KB, "
          f"{sum(len(sv) for *_, sv in VARIANTS)} figs)")


if __name__ == "__main__":
    main()

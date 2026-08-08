"""Prototype: the shaded progress block becomes a line and a circle.

    python _prototypes/gantt_line_circle.py

WHAT THE OPERATOR ASKED FOR (2026-08-07), three complaints in one message:
  1. "está truncado... no puedo ver el resto de tareas"
  2. "las barras de tiempo mejoraron pero siguen siendo muy grandes"
  3. "en vez del cuadro sombreado, opta por lo que se prototipó, una línea y el
     círculo como elemento animado"

(3) turns out to answer (1). Today a project costs TWO rows: the reach line
`━━━◆` and, under it, the shaded progress block `▓▓▓▓▌`. If the progress mark
rides ON the reach line instead of under it, every project gives a row back to
the tasks -- which is exactly the space that was missing.

HOW THIS IS RENDERED, AND WHY IT IS NOT A MOCKUP. `taskboard/views.py` is read,
patched TEXTUALLY in memory, and exec'd as a throwaway module. Every variant
therefore runs the real `render_gantt` with the real `gantt_geometry`, the real
clipping and the real width law. A hand-drawn mockup would let me show column
widths the app cannot actually produce -- which is how a prototype earns an
approval the implementation then cannot honour.

THE BOARD IS SYNTHETIC. `_demo_board()`, never `~/.taskboard/board.json`.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console                      # noqa: E402

from proto import _demo_board                         # noqa: E402

SRC = (ROOT / "taskboard" / "views.py").read_text(encoding="utf-8")

W, H = 104, 26
TODAY = dt.date(2026, 8, 6)


def build(patches, name):
    """Exec a patched copy of views.py as an independent module."""
    src = SRC
    for old, new in patches:
        if old not in src:
            raise SystemExit(f"[{name}] patch anchor not found: {old[:60]!r}")
        src = src.replace(old, new, 1)
    import taskboard                              # the real package must exist
    mod = types.ModuleType(f"taskboard.views_{name}")
    # `__package__` is what makes `from .models import ...` resolve: the patched
    # copy has to believe it lives inside the real package, or every relative
    # import in views.py fails and the "prototype" would silently become a
    # different program from the one being previewed.
    mod.__dict__["__package__"] = "taskboard"
    mod.__dict__["__name__"] = f"taskboard.views_{name}"
    mod.__dict__["__file__"] = str(ROOT / "taskboard" / "views.py")
    sys.modules[mod.__name__] = mod
    exec(compile(src, str(ROOT / "taskboard" / "views.py"), "exec"), mod.__dict__)
    return mod


# --------------------------------------------------------------------------
# the patch pieces
# --------------------------------------------------------------------------

# (a) the progress mark rides on the SPAN instead of filling a second row.
#     `PROGRESS_DOT` is the animated element: it is the only glyph in the field
#     that changes with the app's shared tick, so motion means "this is where
#     the work actually is" and nothing else moves.
RIDE_ON_SPAN = ('''    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    for x in range(c0, min(reached, geo.field_w)):
        band[x] = (FIELD_PROGRESS, hue)
    if reached > c0:
        band[min(reached, geo.field_w - 1)] = (FIELD_HALF, hue)
    return span, band''',
'''    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    dot = min(max(reached, c0), min(c1, geo.field_w - 1))
    if 0 <= dot < geo.field_w:
        span[dot] = ("●", hue)
    return span, band''')

# (b) drop the second project row entirely -- this is the row the operator gets
#     back for tasks.
DROP_BAND_ROW = ('''        rows.append((band_row(" " * geo.label_w, band, " " * geo.figs_w), None))
''', '')

# (c) the task reach stops being a texture and becomes a rule with an end mark.
LIGHT_TASK = [('FIELD_TASK = "▒"', 'FIELD_TASK = "─"'),
              ('FIELD_HALF = "▌"', 'FIELD_HALF = "╴"'),
              ('FIELD_PHASE_TIP = ("▃", "▅", "▆", "▇")',
               'FIELD_PHASE_TIP = ("○", "◔", "◑", "◕")')]

# (d) variant B keeps a second row but draws it as a rule, not a slab.
RULE_BAND = ('''    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    for x in range(c0, min(reached, geo.field_w)):
        band[x] = (FIELD_PROGRESS, hue)
    if reached > c0:
        band[min(reached, geo.field_w - 1)] = (FIELD_HALF, hue)
    return span, band''',
'''    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    for x in range(c0, min(c1 + 1, geo.field_w)):
        band[x] = ("┈", "ash")
    dot = min(max(reached, c0), min(c1, geo.field_w - 1))
    if 0 <= dot < geo.field_w:
        band[dot] = ("●", hue)
    return span, band''')

# (e) variant C: the literal prototype -- one countable dot per week.
WEEK_DOTS = ('''    today_cell = geo.today_dc // 2
    for x in range(c0, c1 + 1):
        span[x] = (FIELD_REACH, "ash" if x < today_cell else hue)''',
'''    today_cell = geo.today_dc // 2
    for x in range(c0, c1 + 1):
        if (x - c0) % 4 == 0:
            span[x] = ("●", "ash" if x < today_cell else hue)''')


# (f) the operator's second complaint: the span itself still reads heavy. `━`
#     is a HEAVY horizontal; `─` is the light one at the same width, so the
#     mechanism is untouched and only the weight moves.
THIN_SPAN = ('FIELD_REACH = "━"', 'FIELD_REACH = "─"')


VARIANTS = [
    ("ACTUAL", "two rows per project: the reach line, then the shaded block",
     []),
    ("A · una fila", "the circle rides ON the reach line; the shaded row is gone",
     [RIDE_ON_SPAN, DROP_BAND_ROW, *LIGHT_TASK]),
    ("A' · una fila, trazo fino", "same as A with a light span instead of a heavy one",
     [RIDE_ON_SPAN, DROP_BAND_ROW, THIN_SPAN, *LIGHT_TASK]),
    ("B · dos filas", "the second row stays, but as a rule with the circle on it",
     [RULE_BAND, *LIGHT_TASK]),
    ("C · puntos por semana", "the original prototype: one countable dot per week",
     [WEEK_DOTS, RIDE_ON_SPAN, DROP_BAND_ROW, *LIGHT_TASK]),
]


def render(name, patches):
    mod = build(patches, re.sub(r"\W", "", name))
    board = _demo_board()
    text = mod.render_gantt(board, False, None, today=TODAY,
                            width=W, height=H, line_map={}, tick=0)
    return text


def measure(plain: str) -> dict:
    """The operator's first complaint, measured rather than described.

    Counting "visible task rows" was the WRONG measure and it undersold the
    change as 15-vs-14. What he asked about is whether anything is CUT, and the
    view answers that itself with its `+N not shown` figure. A variant that
    fits everything and still has blank rows to spare is a different outcome
    from one that shows a single task more.
    """
    lines = plain.split("\n")
    tasks = sum(1 for l in lines
                if l.startswith("▎  ") or l.startswith("▏  ") or l.startswith("▏▤"))
    m = re.search(r"\+(\d+) not shown", plain)
    return {"tasks": tasks,
            "hidden": int(m.group(1)) if m else 0,
            "blank": sum(1 for l in lines if not l.strip())}


def main() -> None:
    # `python gantt_line_circle.py corta` writes a second, SHORTER file with
    # only the variants that actually compete. The full one is ~980 text
    # elements and browsers stall zooming it, which makes the artifact hard to
    # USE even though it is correct -- and a prototype nobody can look at
    # closely has not done its job.
    short = len(sys.argv) > 1 and sys.argv[1] == "corta"
    wanted = {"ACTUAL", "A · una fila", "A' · una fila, trazo fino"}
    out = ROOT / "_prototypes" / (
        "gantt-line-circle-corta.svg" if short else "gantt-line-circle.svg")
    con = Console(record=True, width=W + 2, force_terminal=True,
                  legacy_windows=False, color_system="truecolor")
    counts = []
    for name, why, patches in VARIANTS:
        if short and name not in wanted:
            continue
        text = render(name, patches)
        m = measure(text.plain)
        counts.append((name, m))
        cut = (f"[red]{m['hidden']} tarea(s) OCULTAS[/red]" if m["hidden"]
               else "[green]nada oculto[/green]")
        con.print()
        con.print(f"[bold]{name}[/bold]  [dim]— {why}[/dim]")
        con.print(f"[dim]{W}x{H} · {m['tasks']} tareas dibujadas · [/dim]{cut}"
                  f"[dim] · {m['blank']} filas libres[/dim]")
        con.print(text)
    con.print()
    con.print("[bold]a la misma altura (%dx%d)[/bold]" % (W, H))
    con.print("[dim]  variante                  dibujadas   ocultas   libres[/dim]")
    for name, m in counts:
        con.print(f"  {name:<26}{m['tasks']:>9}{m['hidden']:>10}{m['blank']:>9}")
    con.save_svg(str(out), title="taskboard · gantt: línea y círculo")
    print(f"wrote {out}")
    for name, m in counts:
        print(f"  {name:<24} dibujadas={m['tasks']:<3} ocultas={m['hidden']:<3} "
              f"libres={m['blank']}")


if __name__ == "__main__":
    main()

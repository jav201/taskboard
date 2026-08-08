"""Prototype: the progress circle as the ANIMATED element (variant A', thin span).

    python _prototypes/gantt_circle_pulse.py      -> gantt-circle-pulse.html

WHAT THIS HAS TO ANSWER FIRST. The gantt is NOT still today: `tests/test_motion.py`
documents a flow packet `▬` that advances exactly ONE cell per tick along a
task's reach, riding the app's single clock. So animating the circle is not
"adding motion to a still view" -- it is adding a SECOND kind of motion to a
view that already has one, and the house laws are explicit:

  * `TICK_SECONDS` is the one clock; nothing may keep a private constant.
  * a perceptual cycle must clear 2 s or it reads as a fault flashing
    (`test_the_cycle_is_slow_enough_to_read_as_breathing`).
  * the ambient lives in the GLYPH; no colour may change with time
    (`test_no_colour_changes_between_phases`).

Both variants below obey all three: 4 phases x 1 s = 4 s, glyph-only, no hue
moves. What they differ on is WHETHER MOTION MEANS ANYTHING.

  P — every project's circle breathes. Decoration: motion carries no
      information, and five breathing circles compete with the flow packets
      already crossing the task rows underneath.
  L — only a project that is BEHIND breathes. Motion becomes a channel:
      "the work is left of where the calendar says it should be." Rationed the
      way this codebase already rations red.

WIDTH: `●◉◎` are East-Asian AMBIGUOUS, so a CJK locale could render them two
cells wide and the gantt is width-exact. That is NOT a new exposure -- the view
already ships `◆ ━ ▓ ▒ ▌ ┆ ▲`, all ambiguous. Same accepted policy, said out
loud rather than discovered later.

THE BOARD IS SYNTHETIC.
"""
from __future__ import annotations

import datetime as dt
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import io                                             # noqa: E402
from rich.console import Console                      # noqa: E402

from proto import _demo_board                         # noqa: E402
from taskboard.app import TICK_SECONDS                # the ONE clock, read     # noqa: E402

SRC = (ROOT / "taskboard" / "views.py").read_text(encoding="utf-8")
W, H = 104, 22
TODAY = dt.date(2026, 8, 6)

#: a breath, not a blink: filled -> fisheye -> bullseye -> fisheye closes the
#: cycle, so weight rises and falls instead of jumping.
PULSE = ("●", "◉", "◎", "◉")
CYCLE_MS = len(PULSE) * TICK_SECONDS * 1000
assert CYCLE_MS >= 2000, f"{CYCLE_MS} ms sits inside the illegal 400-2000 band"

# ---- the shared patches (variant A' from the previous prototype) ----------
THIN_SPAN = ('FIELD_REACH = "━"', 'FIELD_REACH = "─"')
LIGHT_TASK = [('FIELD_TASK = "▒"', 'FIELD_TASK = "─"'),
              ('FIELD_HALF = "▌"', 'FIELD_HALF = "╴"'),
              ('FIELD_PHASE_TIP = ("▃", "▅", "▆", "▇")',
               'FIELD_PHASE_TIP = ("○", "◔", "◑", "◕")')]
DROP_BAND_ROW = ('''        rows.append((band_row(" " * geo.label_w, band, " " * geo.figs_w), None))
''', '')

# `_span_bands` has no tick today; the prototype threads one through.
THREAD_TICK = ('''def _span_bands(project, geo: FieldGeo, today: date, hue: str,
                progress: float)''',
               '''def _span_bands(project, geo: FieldGeo, today: date, hue: str,
                progress: float, tick: int = 0, rationed: bool = False)''')
PASS_TICK = ('span, band = _span_bands(p, geo, today, p.color, prog)',
             'span, band = _span_bands(p, geo, today, p.color, prog, tick, RATIONED)')


def ride(rationed: bool) -> tuple[str, str]:
    """The circle replaces the shaded band and takes the pulse."""
    return ('''    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    for x in range(c0, min(reached, geo.field_w)):
        band[x] = (FIELD_PROGRESS, hue)
    if reached > c0:
        band[min(reached, geo.field_w - 1)] = (FIELD_HALF, hue)
    return span, band''',
            '''    reached = c0 + int(round((c1 - c0) * max(0.0, min(1.0, progress))))
    dot = min(max(reached, c0), min(c1, geo.field_w - 1))
    # elapsed fraction of the span: where the calendar says the work should be
    _tc = geo.today_dc // 2
    elapsed = 0.0 if c1 == c0 else max(0.0, min(1.0, (_tc - c0) / (c1 - c0)))
    behind = progress < elapsed - 0.02
    glyph = "●"
    if (not rationed) or behind:
        glyph = PULSE_PHASES[tick % len(PULSE_PHASES)]
    if 0 <= dot < geo.field_w:
        span[dot] = (glyph, hue)
    return span, band''')


def build(patches, rationed, name):
    src = SRC
    for old, new in patches:
        if old not in src:
            raise SystemExit(f"[{name}] anchor not found: {old[:60]!r}")
        src = src.replace(old, new, 1)
    src = src.replace("LATTICE = \"·\"",
                      f"LATTICE = \"·\"\nPULSE_PHASES = {PULSE!r}\n"
                      f"RATIONED = {rationed!r}", 1)
    import taskboard                                                  # noqa: F401
    mod = types.ModuleType(f"taskboard.views_{name}")
    mod.__dict__.update(__package__="taskboard", __name__=f"taskboard.views_{name}",
                        __file__=str(ROOT / "taskboard" / "views.py"))
    sys.modules[mod.__name__] = mod
    exec(compile(src, str(ROOT / "taskboard" / "views.py"), "exec"), mod.__dict__)
    return mod


VARIANTS = [
    ("P · pulso en todos", "every circle breathes — motion carries no information",
     False),
    ("L · pulso racionado", "only a project BEHIND its calendar breathes", True),
]


def frames(rationed, name):
    mod = build([THREAD_TICK, PASS_TICK, ride(rationed), DROP_BAND_ROW,
                 THIN_SPAN, *LIGHT_TASK], rationed, name)
    board = _demo_board()
    out = []
    for tick in range(len(PULSE)):
        con = Console(record=True, width=W + 2, force_terminal=True,
                      legacy_windows=False, color_system="truecolor",
                      file=io.StringIO())   # record only; do not spray stdout
        con.print(mod.render_gantt(board, False, None, today=TODAY, width=W,
                                   height=H, line_map={}, tick=tick))
        out.append(con.export_html(inline_styles=True, code_format="{code}"))
    return out


PAGE = """<!doctype html><meta charset="utf-8">
<title>taskboard · el círculo animado</title>
<style>
 body{{background:#0f1115;color:#c9d1d9;font:14px/1.4 system-ui,sans-serif;
      margin:0;padding:24px 28px}}
 h1{{font-size:16px;margin:0 0 4px}} h2{{font-size:14px;margin:26px 0 2px}}
 p{{margin:0 0 10px;color:#8b949e;max-width:80ch}}
 .stage{{position:relative;height:{h}px}}
 .stage pre{{position:absolute;inset:0;margin:0;opacity:0;
             animation:cycle {cycle}s steps(1,end) infinite}}
 {delays}
 @keyframes cycle{{0%,{on}%{{opacity:1}} {off}%,100%{{opacity:0}}}}
 code{{color:#c9d1d9}}
</style>
<h1>taskboard · gantt A′ — el círculo como elemento animado</h1>
<p>Ciclo real de la app: {n} fases × {tick}s = <b>{cycle}s</b>, fuera de la banda
ilegal de 400–2000 ms. Sólo cambia el <b>glifo</b> (<code>{glyphs}</code>); ningún
color se mueve. El <code>▬</code> que cruza las filas de tarea es el
<i>flow packet</i> que la vista <b>ya</b> tenía.</p>
{body}
"""


def main() -> None:
    n = len(PULSE)
    step = 100.0 / n
    body, css = [], []
    for i, (name, why, rationed) in enumerate(VARIANTS):
        fs = frames(rationed, f"v{i}")
        body.append(f"<h2>{name}</h2><p>{why}</p><div class='stage' id='s{i}'>")
        for k, html in enumerate(fs):
            body.append(f"<pre class='f{k}'>{html}</pre>")
            css.append(f"#s{i} .f{k}{{animation-delay:{k * TICK_SECONDS}s}}")
        body.append("</div>")
    page = PAGE.format(h=(H + 3) * 19, cycle=n * TICK_SECONDS,
                       on=round(step - 0.01, 2), off=round(step, 2),
                       delays="\n ".join(css), n=n, tick=TICK_SECONDS,
                       glyphs=" ".join(PULSE), body="\n".join(body))
    out = ROOT / "_prototypes" / "gantt-circle-pulse.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")
    print(f"  {n} fases x {TICK_SECONDS}s = {CYCLE_MS/1000}s por ciclo")


if __name__ == "__main__":
    main()

"""Headless capture of the gantt axis variants -> SVG + HTML.

    python prototypes/capture_axis_variants.py
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console

from taskboard.models import Board
import gantt_axis_variants as GAV

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

W, H = 86, 28
TODAY = date(2026, 8, 17)
OUT = ROOT / "prototypes" / "out"
FIXTURE = OUT / "_fixture_late.json"

VARIANTS = [
    ("A · top ruler (months + week numbers)", GAV.render_axis_a),
    ("B · week ticks on every row", GAV.render_axis_b),
    ("C · weekend-aware lattice + ruler", GAV.render_axis_c),
    ("D · month bands", GAV.render_axis_d),
]


def capture_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not FIXTURE.exists():
        raise SystemExit(f"FIXTURE MISSING: {FIXTURE}")
    board = Board.load(FIXTURE)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None

    sections: list[str] = []
    for label, fn in VARIANTS:
        text = fn(board, sel, TODAY, W, H)
        con = Console(record=True, width=W + 2, force_terminal=True,
                      legacy_windows=False, color_system="truecolor")
        con.print(text)
        slug = label.split(" · ")[0].lower()
        svg_path = OUT / f"gantt-axis-{slug}.svg"
        con.save_svg(str(svg_path), title=f"taskboard gantt — {label}")

        svg_text = svg_path.read_text(encoding="utf-8")
        if svg_text.startswith("<?xml"):
            svg_text = svg_text.split("?>", 1)[1].strip()
        desc = label.split(" · ", 1)[1]
        sections.append(f"""
<section class="variant" data-variant="{slug.upper()}" {'hidden' if slug != 'a' else ''}>
<h2>{label}</h2>
<p class="note">{desc}</p>
<div class="term-fig">{svg_text}</div>
</section>
""")
        print(f"wrote {svg_path}")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>taskboard — Gantt axis prototypes</title>
<style>
:root {{ --bg: #0b0f14; --panel: #0d1117; --text: #c9d1d9; --muted: #7d8790;
        --accent: #2dd4bf; --amber: #fbbf24; --rose: #fb7185; --frame: #1f2733; }}
body {{ margin: 0; background: var(--bg); color: var(--text);
       font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
.wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 120px; }}
h1 {{ font-size: 24px; color: var(--accent); margin: 0 0 8px; }}
h2 {{ font-size: 18px; color: var(--amber); margin: 0 0 10px; }}
p.note {{ color: var(--muted); max-width: 85ch; line-height: 1.55; margin: 0 0 18px; }}
.term-fig {{ margin: 16px 0; border: 1px solid var(--frame); border-radius: 8px;
             overflow: hidden; background: #000;
             box-shadow: 0 10px 30px rgba(0,0,0,.45); }}
.term-fig svg {{ display: block; width: 100%; height: auto; }}
.prompt {{ background: var(--panel); border: 1px solid var(--frame); border-radius: 8px;
           padding: 16px 18px; margin: 24px 0; }}
.prompt p {{ margin: 0; color: var(--muted); line-height: 1.6; }}
.prompt strong {{ color: var(--accent); }}
.switcher {{ position: fixed; bottom: 22px; left: 50%; transform: translateX(-50%);
             background: var(--panel); border: 1px solid var(--frame); border-radius: 999px;
             padding: 8px 18px; display: flex; gap: 10px; align-items: center;
             box-shadow: 0 8px 24px rgba(0,0,0,.55); z-index: 100; }}
.switcher button {{ background: var(--bg); border: 1px solid var(--frame);
                    color: var(--text); border-radius: 6px; padding: 5px 12px;
                    cursor: pointer; font: inherit; }}
.switcher button:hover {{ border-color: var(--accent); color: var(--accent); }}
.switcher button.active {{ border-color: var(--accent); background: rgba(45,212,191,.12); }}
.switcher .label {{ font-weight: bold; color: var(--accent); min-width: 240px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
<h1>Gantt axis / scale prototypes</h1>
<p class="note">
  Four ways to make the background lattice read as a real date scale instead of
  anonymous dots. Use the floating switcher or the arrow keys to move between
  variants, then tell us which one to ship.
</p>
<div class="prompt">
  <p><strong>Pick one:</strong> A (top ruler), B (week ticks), C (day grid), or D (month bands).</p>
  <p>What matters most — readable dates, subtle structure, or exact day scale?</p>
</div>
{''.join(sections)}
</div>
<div class="switcher">
  <button id="prev">←</button>
  <span class="label" id="label">A · top ruler</span>
  <button id="next">→</button>
</div>
<script>
const variants = ['A','B','C','D'];
const names = {{
  A: 'A · top ruler (months + week numbers)',
  B: 'B · week ticks on every row',
  C: 'C · weekend-aware lattice + ruler',
  D: 'D · month bands'
}};
function read() {{ const v = new URLSearchParams(location.search).get('variant'); return variants.includes(v) ? v : 'A'; }}
function show(v) {{
  document.querySelectorAll('.variant').forEach(el => el.hidden = el.dataset.variant !== v);
  document.getElementById('label').textContent = names[v];
  const url = new URL(location.href); url.searchParams.set('variant', v); history.replaceState(null, '', url);
}}
let idx = variants.indexOf(read());
show(variants[idx]);
document.getElementById('prev').addEventListener('click', () => {{ idx = (idx - 1 + variants.length) % variants.length; show(variants[idx]); }});
document.getElementById('next').addEventListener('click', () => {{ idx = (idx + 1) % variants.length; show(variants[idx]); }});
document.addEventListener('keydown', e => {{
  if (['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) return;
  if (e.key === 'ArrowLeft') {{ idx = (idx - 1 + variants.length) % variants.length; show(variants[idx]); }}
  if (e.key === 'ArrowRight') {{ idx = (idx + 1) % variants.length; show(variants[idx]); }}
}});
</script>
</body>
</html>
"""
    html_path = ROOT / "prototypes" / "gantt-axis-prototype.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"wrote {html_path}")


if __name__ == "__main__":
    capture_all()

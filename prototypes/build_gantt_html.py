"""Build a dark, self-contained HTML prototype page from the captured SVGs.

    python prototypes/build_gantt_html.py

Reads prototypes/out/gantt-{a,b,c,d}.svg and writes
prototypes/gantt-prototype.html.
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HTML = HERE / "gantt-prototype.html"

SVGS = {
    "A": OUT / "gantt-a.svg",
    "B": OUT / "gantt-b.svg",
    "C": OUT / "gantt-c.svg",
    "D": OUT / "gantt-d.svg",
}

DESCRIPTIONS = {
    "A": ("Minimal timeline",
          "Project rows only. Thin single-line bars, no task rows, no meters, no progress band — just the project span and a small due delta."),
    "B": ("Card-style Gantt",
          "Each project and task is a card strip with date chips and a status dot. More readable dates, priority hue on task bars, selected task highlighted."),
    "C": ("Compact horizon",
          "Hides distant past/future and focuses on today ± 3 weeks. Tasks fully outside the horizon are omitted, giving a tight, centred view of the active window."),
    "D": ("Swimlane Gantt",
          "Projects as clean swimlanes with bold separators. Tasks sit inside their lane as compact bars; the layout emphasises grouping over density."),
}


def read_svg(key: str) -> str:
    text = SVGS[key].read_text(encoding="utf-8")
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[1]
    return text.strip()


sections = []
for key in ("A", "B", "C", "D"):
    title, desc = DESCRIPTIONS[key]
    sections.append(f"""
<section class="variant" data-variant="{key}" {'hidden' if key != 'A' else ''}>
<h2>{key} · {title}</h2>
<p class="note">{desc}</p>
<div class="term-fig">{read_svg(key)}</div>
</section>
""")

HTML.write_text(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>taskboard — Gantt view prototypes</title>
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
.switcher .label {{ font-weight: bold; color: var(--accent); min-width: 180px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
<h1>Gantt view prototypes</h1>
<p class="note">
  Four cleaner alternatives to the current Gantt. Each tries to reduce visual load
  while keeping the schedule readable. Use the floating switcher or the arrow keys
  to move between variants, then tell us which one to refine.
</p>

<div class="prompt">
  <p><strong>Pick one:</strong> A (minimal), B (cards), C (horizon), or D (swimlanes).</p>
  <p>What matters most — density, date legibility, focus on the near-term, or clear project grouping?</p>
</div>

{''.join(sections)}
</div>

<div class="switcher">
  <button id="prev">←</button>
  <span class="label" id="label">A · Minimal timeline</span>
  <button id="next">→</button>
</div>

<script>
const variants = ['A','B','C','D'];
const names = {{
  A: 'A · Minimal timeline',
  B: 'B · Card-style',
  C: 'C · Compact horizon',
  D: 'D · Swimlane'
}};
function read() {{ const v = new URLSearchParams(location.search).get('variant'); return variants.includes(v) ? v : 'A'; }}
function show(v) {{
  document.querySelectorAll('.variant').forEach(el => el.hidden = el.dataset.variant !== v);
  document.getElementById('label').textContent = names[v];
  document.querySelectorAll('.switcher button').forEach(b => b.classList.remove('active'));
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
""", encoding="utf-8")

print(f"wrote {HTML}")

"""Headless capture of the SHIPPED gantt view -> SVG.

    python prototypes/capture_gantt_shipped.py

Uses the same synthetic fixture as the variant prototypes so the artifact is
safe to commit/share.
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rich.console import Console

from taskboard.models import Board
from taskboard.views import render_gantt

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

W, H = 86, 30
TODAY = date(2026, 8, 17)
OUT = ROOT / "prototypes" / "out"
FIXTURE = OUT / "_fixture_late.json"


def capture() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not FIXTURE.exists():
        raise SystemExit(f"FIXTURE MISSING: {FIXTURE}")
    board = Board.load(FIXTURE)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None

    text = render_gantt(board, False, sel, TODAY, width=W, height=H)

    html_path = OUT / "gantt-shipped.html"
    html_path.write_text(_render_html(text, "taskboard gantt — date chips"), encoding="utf-8")

    txt_path = OUT / "gantt-shipped.txt"
    txt_path.write_text(str(text), encoding="utf-8")

    print(f"wrote {html_path}")
    print(f"wrote {txt_path}")
    print(f"viewport {W}x{H} | board: {len(tasks)} tasks | selected: {sel}")


def _render_html(text, title: str) -> str:
    """Render the Text to a standalone HTML page so the date chips are visible
    without rich's terminal-width wrapping."""
    import html as _html
    plain = text.plain
    char_styles = [None] * len(plain)
    for s in text.spans:
        st = str(s.style)
        for i in range(s.start, s.end):
            char_styles[i] = st

    def style_seg(seg: str, st: str | None) -> str:
        if st is None:
            return _html.escape(seg)
        if st.startswith("link "):
            url = st.split(" ", 1)[1]
            return f'<a href="{_html.escape(url)}">{_html.escape(seg)}</a>'
        color = None
        bold = rev = False
        for tok in st.split():
            if tok == "bold":
                bold = True
            elif tok == "reverse":
                rev = True
            elif tok.startswith("#"):
                color = tok
        css = f"color:{color};" if color else ""
        if bold:
            css += "font-weight:bold;"
        cls = "reverse" if rev else ""
        if css or cls:
            return f'<span class="{cls}" style="{css}">{_html.escape(seg)}</span>'
        return _html.escape(seg)

    parts: list[str] = []
    i = 0
    while i < len(plain):
        ch = plain[i]
        if ch == "\n":
            parts.append("\n")
            i += 1
            continue
        st = char_styles[i]
        j = i
        while j < len(plain) and plain[j] != "\n" and char_styles[j] == st:
            j += 1
        parts.append(style_seg(plain[i:j], st))
        i = j

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{_html.escape(title)}</title>
<style>
body {{
    background: #1e1e1e;
    margin: 24px;
    font-family: 'Fira Code', Consolas, 'Courier New', monospace;
}}
pre {{
    font-family: inherit;
    font-size: 15px;
    line-height: 1.35;
    color: #e6edf3;
    margin: 0;
}}
a {{ color: inherit; text-decoration: underline; }}
.reverse {{ background: #e6edf3; color: #1e1e1e !important; }}
</style>
</head>
<body>
<pre><code>{''.join(parts)}</code></pre>
</body>
</html>'''


if __name__ == "__main__":
    capture()

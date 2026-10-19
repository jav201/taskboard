"""What differs between two capture folders, run by run (batch 2026-10-18-batch-03).

    python explain_diff.py <dir A> <dir B>

For every SVG pair that differs after `terminal-<N>` normalisation, prints the text runs
(the `<text>` elements: their class, which carries the colour, and their characters) that
only one side has. A difference that is not a text run (a background rect alone) is
printed as such, so nothing is hidden behind the summary.
"""
import difflib
import html
import re
import sys
from pathlib import Path


def runs(p: Path) -> list[str]:
    svg = re.sub(r"terminal-\d+", "terminal-N", p.read_text(encoding="utf-8"))
    return svg.split("><")


a, b = Path(sys.argv[1]), Path(sys.argv[2])
for pa in sorted(a.glob("*.svg")):
    ra, rb = runs(pa), runs(b / pa.name)
    if ra == rb:
        continue
    lines = [ln for ln in difflib.unified_diff(ra, rb, lineterm="", n=0)
             if ln[:1] in "+-" and ln[:3] not in ("---", "+++")]
    texts = [(ln[0], re.search(r'class="([^"]+)"', ln).group(1),
              html.unescape(ln.split(">", 1)[1].rsplit("</", 1)[0]).replace("\xa0", " "))
             for ln in lines if ln[1:].startswith("text ")]
    other = [ln for ln in lines if not ln[1:].startswith(("text ", "rect "))]
    print(pa.name, "·", " | ".join(f"{s}{c} {t!r}" for s, c, t in texts),
          ("· OTHER: %d non-text, non-rect line(s)" % len(other)) if other else "")

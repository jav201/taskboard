"""The board report: one self-contained HTML file, generated on demand.

READ-ONLY. Nothing in this module writes to the board — it takes a loaded `Board`
and returns a string. `write_report` puts that string beside the board it came
from. A law in `tests/test_report.py` holds `board.json` byte-identical across a
generation, and a mutant that saves the board turns it red.

WHAT IT MAY SAY. Only what the data holds: counts, dates, distances, and the load
curve the app already draws. No velocity, no forecast, no invented completion
dates — a project whose work carries no `phase_changed` reads `unaged`, exactly as
the lanes view says it. The momentum ruling travels to the document.

REGISTER. It describes the board. It never addresses the reader and never grades
the work: "overdue" is a fact about a date.

COLOUR. The project hues name projects here as they do in the app, but this
document may NOT lean on them: measured with the dataviz validator, two of the
eight are hard to tell apart with full colour vision (violet/indigo, dE 5.4) and
two are identical to a red-blind reader (fuchsia/violet, dE 0.4). So every figure
carries direct labels and a table of the same numbers, and the hue is decoration
over an already-legible row.
"""

from __future__ import annotations

import html
from datetime import date, timedelta
from pathlib import Path

from .models import Board, Task, days_in_phase, parse_iso
from .views import HEX, lanes_of, sitting

REPORT_CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { margin: 0; padding: 2rem 1.25rem 4rem;
       font: 15px/1.55 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
       background: #0d1117; color: #e6edf3; }
main { max-width: 60rem; margin: 0 auto; }
h1 { font-size: 1.5rem; margin: 0 0 .25rem; letter-spacing: .01em; }
h2 { font-size: 1.05rem; margin: 2.5rem 0 .75rem; padding-bottom: .35rem;
     border-bottom: 1px solid #334154; font-weight: 600; }
.sub { color: #8b98a5; margin: 0 0 2rem; font-size: .9rem; }
.tiles { display: flex; flex-wrap: wrap; gap: .75rem; margin: 0 0 .5rem; }
.tile { flex: 1 1 8rem; background: #161b22; border: 1px solid #21262d;
        border-radius: 8px; padding: .7rem .85rem; }
.tile .n { font-size: 1.6rem; font-weight: 650; letter-spacing: -.01em; }
.tile .k { color: #8b98a5; font-size: .78rem; text-transform: uppercase;
           letter-spacing: .06em; }
table { border-collapse: collapse; width: 100%; margin: .5rem 0 0; font-size: .9rem; }
th, td { text-align: left; padding: .45rem .6rem; border-bottom: 1px solid #21262d;
         vertical-align: top; }
th { color: #8b98a5; font-weight: 600; font-size: .78rem; text-transform: uppercase;
     letter-spacing: .06em; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
.chip { display: inline-block; width: .6rem; height: .6rem; border-radius: 2px;
        margin-right: .45rem; vertical-align: baseline; }
.over { color: #f43f5e; }
.spent { color: #6b4a3f; }
.mut { color: #8b98a5; }
figure { margin: 1rem 0 0; }
figcaption { color: #8b98a5; font-size: .82rem; margin: .4rem 0 0; }
.curve { display: block; width: 100%; height: auto; background: #0f141b;
         border: 1px solid #21262d; border-radius: 8px; }
footer { color: #8b98a5; font-size: .82rem; margin-top: 3rem;
         border-top: 1px solid #21262d; padding-top: .75rem; }
@media (prefers-color-scheme: light) {
  body { background: #ffffff; color: #1f2328; }
  .tile, .curve { background: #f6f8fa; border-color: #d0d7de; }
  h2 { border-color: #d0d7de; }
  th, td { border-color: #d0d7de; }
  .sub, .k, .mut, figcaption, footer { color: #59636e; }
}
@media print { body { background: #fff; color: #000; } .curve { background: #fff; } }
"""


def _e(text: object) -> str:
    """Everything user-authored goes through here. Titles and project names are
    untrusted input the moment they reach markup — the same lesson the views
    learned for rich's markup, in a new surface."""
    return html.escape(str(text), quote=True)


def _due_word(days: int | None, closed: bool = False) -> str:
    """A distance in days. NOTHING IS EXPECTED OF A CLOSED PROJECT, so nothing
    about it can be late — a cancelled or completed project gets the plain
    distance, never the overdue framing. Same ruling the due meter obeys."""
    if days is None:
        return "no date"
    if closed:
        return f"{days:+d}d"
    if days < 0:
        return f"{-days}d overdue"
    if days == 0:
        return "due today"
    return f"in {days}d"


def _bucket(task: Task, board: Board, today: date) -> str:
    """The horizon buckets. Categorical, like the meter: a linear scale would
    spend its resolution on a future where nothing is decided."""
    if board.is_done(task):
        return "done"
    d = parse_iso(task.due_date)
    if d is None:
        return "no date"
    n = (d - today).days
    return ("overdue" if n < 0 else "today" if n == 0 else
            "this week" if n <= 7 else "this month" if n <= 31 else "later")


# Reading order is the urgency order, with spent work last — the same ranking the
# board itself uses. `done` is a bucket because finished work is part of the
# horizon's total; leaving it out would make the shares lie.
BUCKETS = ("overdue", "today", "this week", "this month", "later", "no date", "done")


def _curve_svg(lane, today: date, width: int = 640, height: int = 72) -> str:
    """The project's cumulative load, drawn from the SAME curve the app draws.

    `wave.load_curve` fills a dot bitmap bottom-up; here its per-column heights
    become an SVG area. One engine, two rasterisers — so the document cannot
    describe a shape the app stopped drawing."""
    from .wave import Bitmap, load_curve

    cols = []
    for t in lane.open:
        d = parse_iso(t.due_date)
        if d is not None:
            cols.append((d - today).days)
    horizon_lo = min([-14] + cols)
    horizon_hi = max([21] + cols)
    span = max(1, horizon_hi - horizon_lo)
    steps = [sum(1 for c in cols if c <= horizon_lo + x) for x in range(span)]
    bm = Bitmap(span, 32)
    load_curve(bm, steps, max(1, lane.total), span - 1)
    heights = [bm.ink_at(x) / 32 for x in range(span)]

    dx = width / max(1, span - 1)
    pts = " ".join(f"{i * dx:.1f},{height - h * (height - 8):.1f}"
                   for i, h in enumerate(heights))
    zero = (0 - horizon_lo) / span * width
    hue = HEX.get(lane.hue, HEX["mut"])
    return (
        f'<svg class="curve" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="cumulative load for {_e(lane.name)}">'
        f'<polyline points="0,{height} {pts} {width},{height}" fill="{hue}" '
        f'fill-opacity="0.20" stroke="none"/>'
        f'<polyline points="{pts}" fill="none" stroke="{hue}" stroke-width="2" '
        f'stroke-linejoin="round"/>'
        f'<line x1="{zero:.1f}" y1="0" x2="{zero:.1f}" y2="{height}" '
        f'stroke="{HEX["accent"]}" stroke-width="1.5"/>'
        f'<text x="{zero + 4:.1f}" y="12" fill="{HEX["accent"]}" '
        f'font-size="10">today</text>'
        f"</svg>")


def _tiles(pairs) -> str:
    cells = "".join(f'<div class="tile"><div class="n">{_e(v)}</div>'
                    f'<div class="k">{_e(k)}</div></div>' for k, v in pairs)
    return f'<div class="tiles">{cells}</div>'


def _horizon_table(tasks, board: Board, today: date) -> str:
    """The horizon as a table AND a bar — never as colour alone. The palette
    measurement is the reason: two identity hues are indistinguishable to some
    readers, so no figure here may carry meaning in hue by itself."""
    counts = {b: 0 for b in BUCKETS}
    for t in tasks:
        counts[_bucket(t, board, today)] += 1
    top = max(1, max(counts.values()))
    rows = []
    for b in BUCKETS:
        n = counts[b]
        pct = 100 * n / top
        tone = HEX["over"] if b == "overdue" else (
            HEX["accent"] if b == "today" else (
                HEX["ash"] if b == "done" else HEX["mut"]))
        bar = (f'<svg width="100%" height="10" viewBox="0 0 100 10" '
               f'preserveAspectRatio="none" role="presentation">'
               f'<rect x="0" y="1" width="{pct:.1f}" height="8" rx="2" '
               f'fill="{tone}"/></svg>')
        cls = ' class="over"' if b == "overdue" and n else ""
        rows.append(f"<tr><td{cls}>{_e(b)}</td><td class=\"n\">{n}</td>"
                    f"<td style=\"width:55%\">{bar}</td></tr>")
    return ("<table><thead><tr><th>when</th><th class=\"n\">tasks</th>"
            "<th>share</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def _project_section(lane, board: Board, today: date) -> str:
    hue = HEX.get(lane.hue, HEX["mut"])
    status = "" if lane.status == "on_track" else f" · {_e(lane.status)}"
    momentum = sitting(lane, today) or "nothing open"
    late = f'<span class="over">{len(lane.late)} overdue</span>' if lane.late else "0 overdue"
    worst = f" (worst {lane.worst}d)" if lane.late else ""
    named = sorted([t for t in lane.open if parse_iso(t.due_date)],
                   key=lambda t: parse_iso(t.due_date))[:8]
    rows = "".join(
        "<tr><td>{title}</td><td>{phase}</td><td class=\"n\">{due}</td>"
        "<td class=\"n mut\">{age}</td></tr>".format(
            title=_e(t.title), phase=_e(t.phase),
            due=_e(_due_word((parse_iso(t.due_date) - today).days)),
            age=_e(f"{days_in_phase(t, today)}d in phase"
                   if days_in_phase(t, today) is not None else "unaged"))
        for t in named)
    task_table = (
        "<table><thead><tr><th>next due</th><th>phase</th>"
        "<th class=\"n\">due</th><th class=\"n\">in phase</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>" if rows else
        '<p class="mut">Nothing open with a date.</p>')
    return f"""
<h2><span class="chip" style="background:{hue}"></span>{_e(lane.name)}{status}</h2>
{_tiles([("open", len(lane.open)), ("done", lane.done_n),
         ("total", lane.total), ("high priority", lane.high),
         ("own due date", _due_word(lane.due_in, lane.closed))])}
<p class="mut">{late}{_e(worst)} · momentum: {_e(momentum)}</p>
<figure>{_curve_svg(lane, today)}
<figcaption>Cumulative open work by its due day — the same curve the board draws.
The rule marks today.</figcaption></figure>
{task_table}
"""


def build_report(board: Board, today: date | None = None,
                 project: str | None = None) -> str:
    """The document, as a string. Reads the board; never writes it."""
    today = today or date.today()
    lanes = lanes_of(board, False, today)
    if project is not None:
        lanes = [ln for ln in lanes if ln.name == project]
    scope = _e(project) if project else "the whole board"
    tasks = [t for ln in lanes for t in ln.tasks]
    open_n = sum(len(ln.open) for ln in lanes)
    done_n = sum(ln.done_n for ln in lanes)
    late_n = sum(len(ln.late) for ln in lanes)
    archived = sum(1 for t in board.visible_tasks(True)
                   if t.archived and (project is None or any(
                       t in ln.tasks for ln in lanes)))
    sections = "".join(_project_section(ln, board, today) for ln in lanes)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>taskboard — {scope}</title>
<style>{REPORT_CSS}</style></head>
<body><main>
<h1>taskboard · {scope}</h1>
<p class="sub">Generated {_e(today.isoformat())} from the board's own data.
Counts and dates only — nothing here is a forecast.</p>

<h2>Where the board stands</h2>
{_tiles([("projects", len(lanes)), ("open", open_n), ("done", done_n),
         ("overdue", late_n), ("archived", archived)])}

<h2>The horizon</h2>
{_horizon_table(tasks, board, today)}
{sections}
<footer>taskboard · a local file, generated on demand. Work with no recorded
completion date reads <em>unaged</em> rather than a guess.</footer>
</main></body></html>
"""


def report_path(board: Board, today: date | None = None,
                project: str | None = None) -> Path:
    """Beside the board it came from — so a fixture's report lands by the fixture
    and the real app's lands in its own directory."""
    today = today or date.today()
    slug = "board" if project is None else "".join(
        ch.lower() if ch.isalnum() else "-" for ch in project).strip("-")[:40]
    return Path(board.path).parent / "reports" / f"{slug}-{today.isoformat()}.html"


def write_report(board: Board, today: date | None = None,
                 project: str | None = None) -> Path:
    """Write the document and return where it went. The board is not touched."""
    out = report_path(board, today, project)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report(board, today, project), encoding="utf-8")
    return out

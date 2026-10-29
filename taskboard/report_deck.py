"""The deck report (variant C): one self-contained HTML file of vector slides.

It renders from the extraction dict ALONE (`report_html.extract`): a cover, an
overview (every project in scope on one timeline) and one slide for every
non-archived project in scope — the Inbox included — that holds a task of any
status. Each project slide is an SVG gantt with real `<text>`, today's rule,
phase-coloured bars, milestones labelled with their class, dependency arrows
by task key, and the project's notes.

Every board string is escaped here (`esc` = `report._e`) before it reaches
HTML or SVG text; notes are the dict's server-built `notes_html`; task links
are re-checked to http(s). Status, due words and counts are read from the
dict, never re-derived. Offline: inline CSS and JS, no external resource.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

from .report_html import esc

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
TICK_STEPS = (1, 2, 3, 5, 7, 10, 14, 21, 30, 60)
MUTED = "#8b98a5"

WIDE = {"cls": "g-wide", "W": 1000, "X0": 208, "X1": 986, "TOP": 30, "RH": 38, "BH": 18,
        "chars": 30, "ty": 14, "my": 27, "yc": 17, "fs": 12.5, "mfs": 9.5, "md": 9,
        "lfs": 11, "ufs": 10, "HH": 20, "ORH": 30, "ochars": 28, "oty": 13, "omy": 25,
        "oyc": 15, "obh": 10, "ofs": 12, "omfs": 9.5, "bfs": 11}
NARROW = {"cls": "g-narrow", "W": 420, "X0": 8, "X1": 412, "TOP": 26, "RH": 46, "BH": 13,
          "chars": 64, "ty": 12, "my": 24, "yc": 34, "fs": 11.5, "mfs": 8.8, "md": 8,
          "lfs": 10, "ufs": 9, "HH": 18, "ORH": 40, "ochars": 56, "oty": 12, "omy": 23,
          "oyc": 32, "obh": 9, "ofs": 11, "omfs": 8.8, "bfs": 10.5}


def _day(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


def _hue(c: str | None) -> str:
    return c if re.fullmatch(r"#[0-9a-fA-F]{6}", c or "") else MUTED


def safe_href(u: str | None) -> str | None:
    return u if re.match(r"https?://", u or "", re.I) else None


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _trunc(text: str, n: int) -> str:
    return text if len(text) <= n else text[:max(1, n - 1)] + "…"


# ---- timeline geometry -----------------------------------------------------

def _x(d: date, lo: date, hi: date, x0: float, x1: float) -> float:
    return x0 + (d - lo).days / max(1, (hi - lo).days) * (x1 - x0)


def _scale(tasks: list, today: date) -> tuple[date, date]:
    pts = [d for t in tasks for d in (_day(t["start"]), _day(t["due"])) if d]
    if not pts:
        return today - timedelta(days=7), today + timedelta(days=7)
    lo, hi = min(pts), max(pts)
    pad = max(2, (hi - lo).days // 12)
    lo, hi = lo - timedelta(days=pad), hi + timedelta(days=pad)
    if lo <= today <= hi:
        return lo, hi
    return (today - timedelta(days=10), hi) if today < lo else (lo, today + timedelta(days=10))


def _ticks(lo: date, hi: date) -> list[date]:
    step = next((s for s in TICK_STEPS if (hi - lo).days // s <= 8), 90)
    d = lo + timedelta(days=(step - lo.toordinal() % step) % step)
    out = []
    while d <= hi:
        out.append(d)
        d += timedelta(days=step)
    return out


def _frame(lo, hi, today, L, top, bottom) -> str:
    x0, x1, w = L["X0"], L["X1"], L["W"]
    p = []
    dw = (x1 - x0) / max(1, (hi - lo).days)
    d = lo
    while d <= hi:
        if d.weekday() >= 5:
            p.append(f'<rect x="{_x(d, lo, hi, x0, x1):.1f}" y="{top}" width="{dw:.1f}" '
                     f'height="{bottom - top}" class="wk"/>')
        d += timedelta(days=1)
    for t in _ticks(lo, hi):
        x = _x(t, lo, hi, x0, x1)
        p.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" class="gl"/>')
        if x + 3 <= w - 46:
            p.append(f'<text x="{x + 3:.1f}" y="{top - 8}" class="m" font-size="10">'
                     f"{MONTHS[t.month - 1]} {t.day}</text>")
    if lo <= today <= hi:
        x = _x(today, lo, hi, x0, x1)
        p.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" class="today"/>')
        p.append(f'<text x="{x + 3:.1f}" y="{bottom - 5}" class="td" font-size="10">today</text>')
    return "".join(p)


def _diamond(cx: float, yc: float, r: float, t: dict, marks: dict) -> str:
    if t["status"] == "done":
        paint = 'class="msr"'
    elif t["status"] == "late":
        paint = 'class="mso"'
    else:
        m = marks.get(t["mark"])
        paint = f'style="fill:{_hue(m["colour"] if m else None)}"'
    return (f'<path d="M{cx:.1f},{yc - r} L{cx + r:.1f},{yc} {cx:.1f},{yc + r} '
            f'L{cx - r:.1f},{yc} Z" {paint}/>')


def _is_point(t: dict) -> bool:
    return t["milestone"] and t["due"] is not None and t["start"] == t["due"]


def _bar_cls(t: dict, phases: list) -> str:
    if t["done"]:
        return "done"
    return f"ph{min(4, phases.index(t['phase']))}" if t["phase"] in phases else "ph0"


def _mark_label(t: dict, marks: dict) -> str | None:
    m = marks.get(t["mark"])
    return f"{m['shape']} {m['name']}" if m else None


def _meta(t: dict, marks: dict) -> list[tuple[str, str]]:
    parts = [(t["phase"], "m")]
    if t["priority"] == "high":
        parts.append(("high", "m"))
    parts.append((t["due_word"], "mo" if t["status"] == "late" else "m"))
    if t["blocked"]:
        parts.append(("blocked", "mo"))
    if t["age"] is not None:
        parts.append((f"{t['age']}d in phase", "m"))
    label = _mark_label(t, marks)
    if label:
        parts.append((label, "mk"))
    return parts


def _rows(tasks: list) -> list:
    """Open dated by due, then open undated, then done (latest first)."""
    def key(t):
        d = t["due"] or t["start"]
        return (d, t["start"] or d)
    live = [t for t in tasks if not t["done"]]
    dated = sorted((t for t in live if t["start"] or t["due"]), key=key)
    undated = [t for t in live if not (t["start"] or t["due"])]
    done = sorted((t for t in tasks if t["done"]), key=lambda t: t["due"] or "", reverse=True)
    return dated + undated + done


def _gantt(rows: list, phases: list, marks: dict, today: date, L: dict, sid: str) -> str:
    lo, hi = _scale(rows, today)
    W, X0, X1, TOP, RH, BH = L["W"], L["X0"], L["X1"], L["TOP"], L["RH"], L["BH"]
    H = TOP + len(rows) * RH + 12
    p = [f'<svg class="g {L["cls"]}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="gantt of the project’s tasks">'
         f'<defs><marker id="ah{sid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
         f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" class="ahd"/>'
         f"</marker></defs>",
         _frame(lo, hi, today, L, TOP, H - 4)]
    anchors = {}
    for i, t in enumerate(rows):
        y = TOP + i * RH
        yc = y + L["yc"]
        p.append(f'<line x1="4" y1="{y + RH - 1}" x2="{W - 4}" y2="{y + RH - 1}" class="rl"/>')
        title = _trunc(t["title"], L["chars"])
        if t["done"]:
            title = "✓ " + title
        if t["blocked"]:
            title = "⛔ " + title
        p.append(f'<text x="8" y="{y + L["ty"]}" class="t" font-size="{L["fs"]}">{esc(title)}</text>')
        meta = "".join((f'<tspan class="m"> · </tspan>' if j else "")
                       + f'<tspan class="{cls}">{esc(text)}</tspan>'
                       for j, (text, cls) in enumerate(_meta(t, marks)))
        p.append(f'<text x="8" y="{y + L["my"]}" font-size="{L["mfs"]}">{meta}</text>')
        s, d = _day(t["start"]), _day(t["due"])
        if _is_point(t):
            cx = _x(d, lo, hi, X0, X1)
            p.append(_diamond(cx, yc, L["md"], t, marks))
            label = _mark_label(t, marks) or "milestone"
            fs = L["lfs"]
            if cx + 12 + len(label) * fs * 0.58 + 4 > W - 6:
                p.append(f'<text x="{cx - 12:.1f}" y="{yc + 4}" class="mk" font-size="{fs}" '
                         f'text-anchor="end">{esc(label)}</text>')
            else:
                p.append(f'<text x="{cx + 12:.1f}" y="{yc + 4}" class="mk" font-size="{fs}">'
                         f"{esc(label)}</text>")
            anchors[t["key"]] = (cx, yc)
        elif s is None and d is None:
            p.append(f'<rect x="{X0}" y="{yc - BH // 2}" width="{X1 - X0}" height="{BH - 4}" '
                     f'class="undated"/>')
            p.append(f'<text x="{X0 + 6}" y="{yc + 3}" class="m" font-size="{L["ufs"]}">'
                     f"no dates</text>")
            anchors[t["key"]] = (None, yc)
        else:
            s, d = s or d, d or s
            xs, xe = _x(s, lo, hi, X0, X1), _x(d, lo, hi, X0, X1)
            xe = max(xe, xs + 4)
            blk = " blk" if t["blocked"] else ""
            p.append(f'<rect x="{xs:.1f}" y="{yc - BH // 2}" width="{xe - xs:.1f}" height="{BH}" '
                     f'rx="3" class="bar {_bar_cls(t, phases)}{blk}"/>')
            anchors[t["key"]] = (xe, yc)
    for t in rows:
        x2, y2 = anchors[t["key"]]
        for dep in t["deps"]:
            if dep not in anchors or anchors[dep][0] is None or x2 is None:
                continue
            x1, y1 = anchors[dep]
            xt = _x(_day(t["start"]) or _day(t["due"]) or today, lo, hi, X0, X1)
            c = 16 if xt >= x1 else -16
            p.append(f'<path d="M{x1:.1f},{y1:.1f} C{x1 + c:.1f},{y1:.1f} {xt - c:.1f},{y2:.1f} '
                     f'{xt - 2:.1f},{y2:.1f}" class="arrow" marker-end="url(#ah{sid})"/>')
    p.append("</svg>")
    return "".join(p)


def _overview(entries: list, boards: dict, marks: dict, today: date, L: dict) -> str:
    tasks = [t for _, ts in entries for t in ts]
    lo, hi = _scale(tasks, today)
    W, X0, X1, TOP, HH, RH = L["W"], L["X0"], L["X1"], L["TOP"], L["HH"], L["ORH"]
    heads = len({p["board"] for p, _ in entries})
    H = TOP + heads * HH + len(entries) * RH + 12
    p = [f'<svg class="g {L["cls"]}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="all projects on one timeline">', _frame(lo, hi, today, L, TOP, H - 4)]
    y, last = TOP, None
    for proj, ts in entries:
        if proj["board"] != last:
            p.append(f'<text x="8" y="{y + 13}" class="bd" font-size="{L["bfs"]}">'
                     f"{esc(boards.get(proj['board'], ''))}</text>")
            y += HH
            last = proj["board"]
        p.append(f'<line x1="4" y1="{y + RH - 1}" x2="{W - 4}" y2="{y + RH - 1}" class="rl"/>')
        p.append(f'<text x="8" y="{y + L["oty"]}" class="t" font-size="{L["ofs"]}">'
                 f"{esc(_trunc(proj['name'], L['ochars']))}</text>")
        st = "" if proj["status"] == "on_track" else f" · {proj['status']}"
        line = f"open {proj['open']}{st} · {proj['due_word']}"
        p.append(f'<text x="8" y="{y + L["omy"]}" class="m" font-size="{L["omfs"]}">'
                 f"{esc(line)}</text>")
        yc, bh = y + L["oyc"], L["obh"]
        for t in ts:
            s, d = _day(t["start"]), _day(t["due"])
            if _is_point(t):
                p.append(_diamond(_x(d, lo, hi, X0, X1), yc, 7, t, marks))
            elif s or d:
                s, d = s or d, d or s
                xs, xe = _x(s, lo, hi, X0, X1), _x(d, lo, hi, X0, X1)
                xe = max(xe, xs + 3)
                p.append(f'<rect x="{xs:.1f}" y="{yc - bh // 2}" width="{xe - xs:.1f}" '
                         f'height="{bh}" rx="2" class="bar {_bar_cls(t, proj["phases"])}"/>')
        y += RH
    p.append("</svg>")
    return "".join(p)


# ---- slides ----------------------------------------------------------------

def slide_projects(d: dict) -> list[tuple[dict, list]]:
    """(project, its tasks) for every slide: a non-archived project holding a task."""
    out = []
    for p in d["projects"]:
        ts = [t for t in d["tasks"] if t["project"] == p["key"]]
        if not p["archived"] and ts:
            out.append((p, ts))
    return out


def _legend(phases: list, marks: list) -> str:
    ph = "".join(f'<span class="lg"><span class="sw ph{min(4, i)}"></span>{esc(n)}</span>'
                 for i, n in enumerate(phases))
    mk = "".join(f'<span class="lg"><span class="sw" style="background:{_hue(m["colour"])}">'
                 f'</span>{esc(m["shape"])} {esc(m["name"])}</span>' for m in marks)
    return (f'<p class="legend">{ph}{mk}<span class="lg"><span class="sw msr"></span>'
            f"reached (done)</span></p>")


def _scope_line(d: dict, boards: dict) -> str:
    sc = d["meta"]["scope"]
    if sc["kind"] == "project":
        p = next((p for p in d["projects"] if p["key"] == sc["project"]), None)
        if p is not None:
            return f"Project {p['name']} on {boards.get(p['board'], '')}"
    return f"All loaded boards ({len(sc['boards'])}): " + ", ".join(sc["boards"])


def _cover(d: dict, boards: dict) -> str:
    rows, tot = [], {"boards": 0, "projects": 0, "open": 0, "done": 0, "overdue": 0, "archived": 0}
    for b in d["boards"]:
        ps = [p for p in d["projects"] if p["board"] == b["key"] and not p["archived"]]
        n = {"projects": len(ps), "open": sum(p["open"] for p in ps),
             "done": sum(p["done"] for p in ps), "overdue": sum(p["late"] for p in ps),
             "archived": sum(1 for t in d["tasks"]
                             if t["board"] == b["key"] and t["status"] == "archived")}
        tot["boards"] += 1
        for k, v in n.items():
            tot[k] += v
        cells = "".join(f'<td class="n">{n[k]}</td>'
                        for k in ("projects", "open", "done", "overdue", "archived"))
        rows.append(f"<tr><td>{esc(b['name'])}</td>{cells}</tr>")
    tiles = "".join(f'<div class="tile"><div class="n">{v}</div><div class="k">{k}</div></div>'
                    for k, v in tot.items())
    phases = d["projects"][0]["phases"] if d["projects"] else []
    return (f'<section class="slide cover"><h1>taskboard · project deck</h1>'
            f'<p class="scope">{esc(_scope_line(d, boards))}</p>'
            f'<p class="sub">Generated {esc(d["meta"]["generated"])} · statuses as of '
            f'{esc(d["meta"]["today"])} · counts and dates only, nothing here is a forecast.</p>'
            f'<div class="tiles">{tiles}</div>'
            f'<table><thead><tr><th>board</th><th class="n">projects</th>'
            f'<th class="n">open</th><th class="n">done</th><th class="n">overdue</th>'
            f'<th class="n">archived</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
            f'{_legend(phases, d["marks"])}'
            f'<p class="hint">Page with ← → (PageUp / PageDown, Home / End) or the '
            f"buttons below · prints as one slide per page · every figure is labelled "
            f"directly — colour never carries meaning alone.</p></section>")


def _overview_slide(entries: list, boards: dict, marks: dict, today: date) -> str:
    live = [(p, [t for t in ts if t["status"] != "archived"]) for p, ts in entries]
    if live:
        body = "".join(_overview(live, boards, marks, today, L) for L in (WIDE, NARROW))
    else:
        body = '<p class="sub">No project in this scope holds a task.</p>'
    return ('<section class="slide"><h2>All projects — the overview</h2>'
            '<p class="sub">Every project in scope on one timeline. Bars wear their phase; '
            f"diamonds are milestones.</p>{body}</section>")


def _notes(tasks: list) -> str:
    cards = []
    for t in tasks:
        links = [h for h in map(safe_href, t["urls"]) if h]
        if not (t["notes_html"] or links):
            continue
        body = f'<p class="nl">{t["notes_html"]}</p>' if t["notes_html"] else ""
        for h in links:
            label = re.sub(r"^https?://", "", h, flags=re.I)
            body += (f'<p class="nl"><a class="url" href="{esc(h)}" target="_blank" '
                     f'rel="noopener noreferrer">{esc(label)}</a></p>')
        cards.append(f'<div class="note"><p class="nt">{esc(t["title"])}</p>{body}</div>')
    if not cards:
        return ""
    return f'<h3>Notes</h3><div class="notes">{"".join(cards)}</div>'


def _project_slide(p: dict, tasks: list, boards: dict, marks: dict, today: date, n: int) -> str:
    live = [t for t in tasks if t["status"] != "archived"]
    k = len(tasks) - len(live)
    status = "" if p["status"] == "on_track" else f" · {esc(p['status'])}"
    late = (f'<span class="over">{p["late"]} overdue</span> (worst {p["worst"]}d)'
            if p["late"] else "0 overdue")
    head = (f'<h2><span class="chip" style="background:{_hue(p["colour"])}"></span>'
            f'<span class="pname">{esc(p["name"])}</span>{status}</h2>'
            f'<p class="sub">{esc(boards.get(p["board"], ""))} · open {p["open"]} · '
            f'done {p["done"]} · high {p["high"]} · {late} · due '
            f'{esc(p["due_word"])} · momentum: {esc(p["momentum"])}</p>')
    if live:
        rows = _rows(live)
        chart = "".join(_gantt(rows, p["phases"], marks, today, L, f"{n}{L['cls'][2]}")
                        for L in (WIDE, NARROW))
        used = [m for key, m in marks.items() if any(t["mark"] == key for t in live)]
        chart += _legend(p["phases"], used)
    else:
        chart = '<p class="sub">Nothing to chart: every task of this project is archived.</p>'
    count = _plural(len(live), "task") + (f" · {k} archived" if k else "")
    return (f'<section class="slide" data-project="{esc(p["key"])}">{head}{chart}'
            f'{_notes(live)}<p class="foot">{count}</p></section>')


LIGHT = """--bg:#ffffff;--panel:#f6f8fa;--ink:#1f2328;--mut:#59636e;--line:#d8dee4;
  --frame:#c8d0da;--weekend:#edf1f5;--done:#2f8f5b;--accent:#0f766e;--over:#c81e4f;
  --ph0:#94a3b8;--ph1:#1f6feb;--ph2:#8250df;--ph3:#bf6106;--ph4:#2f8f5b;--msr:#8a919b;
  --soon:#8a5a00;--green:#1a7f37;"""

CSS = """
:root{color-scheme:light dark;
  --bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--mut:#8b98a5;--line:#21262d;--frame:#334154;
  --accent:#2dd4bf;--over:#f43f5e;--weekend:#151a22;--done:#3f9c6d;
  --ph0:#64748b;--ph1:#60a5fa;--ph2:#a78bfa;--ph3:#fb923c;--ph4:#3f9c6d;--msr:#7a828c;
  --soon:#fbbf24;--green:#4ade80;}
@media (prefers-color-scheme:light){ :root{%(light)s} }
*{box-sizing:border-box}
body{margin:0;padding:1.2rem .9rem 6rem;background:var(--bg);color:var(--ink);
  font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;overflow-wrap:anywhere}
.slide{display:none;max-width:1100px;margin:0 auto}
.slide.on{display:block}
h1{font-size:2rem;margin:1rem 0 .3rem;letter-spacing:-.01em}
h2{font-size:1.2rem;margin:.6rem 0 .2rem;font-weight:650;display:flex;align-items:center;
  gap:.5rem;flex-wrap:wrap}
h3{font-size:.95rem;margin:1.6rem 0 .4rem;color:var(--mut);text-transform:uppercase;
  letter-spacing:.06em;font-weight:600}
.scope{font-weight:600;margin:0 0 .3rem}
.sub{color:var(--mut);margin:0 0 1rem;font-size:.9rem}
.chip{display:inline-block;width:.75rem;height:.75rem;border-radius:3px;flex:none}
.tiles{display:flex;flex-wrap:wrap;gap:.7rem;margin:.4rem 0 1.2rem}
.tile{flex:1 1 6rem;background:var(--panel);border:1px solid var(--line);border-radius:8px;
  padding:.65rem .8rem}
.tile .n{font-size:1.5rem;font-weight:650}
.tile .k{color:var(--mut);font-size:.75rem;text-transform:uppercase;letter-spacing:.06em}
table{border-collapse:collapse;width:100%%;margin:.4rem 0 1rem;font-size:.9rem}
th,td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.over{color:var(--over);font-weight:600}
.g{display:block;width:100%%;height:auto;background:var(--panel);border:1px solid var(--line);
  border-radius:10px;margin:.6rem 0}
.g-narrow{display:none}
svg text{font-family:inherit}
.t{fill:var(--ink)} .m{fill:var(--mut)} .mo{fill:var(--over)} .mk{fill:var(--accent)}
.td{fill:var(--accent)} .bd{fill:var(--mut)}
.wk{fill:var(--weekend)} .gl{stroke:var(--line);stroke-width:1}
.rl{stroke:var(--line);stroke-width:1;opacity:.55}
.today{stroke:var(--accent);stroke-width:1.5}
.ahd{fill:var(--mut)} .arrow{stroke:var(--mut);stroke-width:1.3;fill:none;opacity:.9}
.bar{opacity:.92} .bar.blk{stroke:var(--over);stroke-width:1.6;stroke-dasharray:4 2}
.bar.ph0{fill:var(--ph0)} .bar.ph1{fill:var(--ph1)} .bar.ph2{fill:var(--ph2)}
.bar.ph3{fill:var(--ph3)} .bar.ph4,.bar.done{fill:var(--done)}
.undated{fill:none;stroke:var(--frame);stroke-width:1.2;stroke-dasharray:5 3}
.msr{fill:var(--msr)} .mso{fill:var(--over)}
.legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;color:var(--mut);font-size:.82rem;margin:.8rem 0 0}
.lg{display:inline-flex;align-items:center;gap:.35rem}
.sw{display:inline-block;width:.7rem;height:.7rem;border-radius:2px}
.sw.ph0{background:var(--ph0)} .sw.ph1{background:var(--ph1)} .sw.ph2{background:var(--ph2)}
.sw.ph3{background:var(--ph3)} .sw.ph4{background:var(--ph4)} .sw.msr{background:var(--msr)}
.notes{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(17rem,100%%),1fr));gap:.6rem}
.note{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:.55rem .75rem}
.nt{margin:0 0 .25rem;font-weight:600;font-size:.88rem}
.nl{margin:.12rem 0;font-size:.86rem}
.mention{color:var(--accent);font-weight:600}
.hl-soon{color:var(--soon)} .hl-over{color:var(--over)} .hl-green{color:var(--green)}
.url{color:var(--accent);font-size:.82rem;word-break:break-all}
.foot{color:var(--mut);font-size:.85rem;margin:1.2rem 0 0;padding-top:.4rem;
  border-top:1px solid var(--line)}
.hint{color:var(--mut);font-size:.85rem;margin-top:1.4rem}
.bar-nav{position:fixed;left:0;right:0;bottom:0;z-index:9;display:flex;align-items:center;
  justify-content:center;gap:1rem;padding:.55rem;background:var(--panel);
  border-top:1px solid var(--line)}
.bar-nav button{font:inherit;font-size:1.05rem;min-width:3rem;min-height:2.6rem;border-radius:8px;
  cursor:pointer;background:var(--bg);color:var(--ink);border:1px solid var(--frame)}
.bar-nav button:disabled{opacity:.35;cursor:default}
#cnt{font-variant-numeric:tabular-nums;color:var(--mut);min-width:4rem;text-align:center}
@media (max-width:700px){
  .g-wide{display:none} .g-narrow{display:block}
  body{padding:.7rem .5rem 6rem}
  h1{font-size:1.5rem}
  th,td{padding:.3rem .35rem}
  th{letter-spacing:0;font-size:.62rem;overflow-wrap:normal}
  table{font-size:.82rem}
}
@media print{
  :root{color-scheme:light;%(light)s}
  body{background:#fff;color:#000;padding:0}
  .bar-nav{display:none}
  .slide{display:block!important;break-after:page;max-width:none}
  .g-narrow{display:none!important} .g-wide{display:block!important}
}
""" % {"light": LIGHT}

JS = """
(function () {
  var slides = [].slice.call(document.querySelectorAll('.slide'));
  var cur = 0;
  var cnt = document.getElementById('cnt');
  var prev = document.getElementById('prev');
  var next = document.getElementById('next');
  function show(n) {
    cur = Math.min(slides.length - 1, Math.max(0, n));
    slides.forEach(function (s, i) { s.classList.toggle('on', i === cur); });
    cnt.textContent = (cur + 1) + ' / ' + slides.length;
    prev.disabled = cur === 0;
    next.disabled = cur === slides.length - 1;
    window.scrollTo(0, 0);
  }
  prev.addEventListener('click', function () { show(cur - 1); });
  next.addEventListener('click', function () { show(cur + 1); });
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' ||
              t.tagName === 'SELECT' || t.isContentEditable)) { return; }
    if (e.ctrlKey || e.altKey || e.metaKey) { return; }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { show(cur - 1); e.preventDefault(); }
    else if (e.key === 'ArrowRight' || e.key === 'PageDown') { show(cur + 1); e.preventDefault(); }
    else if (e.key === 'Home') { show(0); e.preventDefault(); }
    else if (e.key === 'End') { show(slides.length - 1); e.preventDefault(); }
  });
  show(0);
})();
"""

NAV = ('<div class="bar-nav"><button id="prev" type="button" aria-label="Previous slide">'
       '&#9664;</button><span id="cnt" aria-live="polite"></span><button id="next" '
       'type="button" aria-label="Next slide">&#9654;</button></div>')


def render(d: dict) -> str:
    """The deck page: cover, overview, one slide per project in scope that holds a task."""
    today = date.fromisoformat(d["meta"]["today"])
    boards = {b["key"]: b["name"] for b in d["boards"]}
    marks = {m["key"]: m for m in d["marks"]}
    entries = slide_projects(d)
    slides = [_cover(d, boards), _overview_slide(entries, boards, marks, today)]
    slides += [_project_slide(p, ts, boards, marks, today, i) for i, (p, ts) in enumerate(entries)]
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f"<title>taskboard · project deck</title>\n<style>{CSS}</style></head>\n"
            f"<body>\n{''.join(slides)}\n{NAV}\n<script>{JS}</script>\n</body></html>\n")

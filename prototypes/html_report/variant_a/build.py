"""Variant A — the meeting one-pager.

A status report that reads ACROSS all three boards: summary tiles, what moved
in the last 7 days (phase_changed), late work, the next 7 days, milestones
grouped by their class mark, dependency chains, and per-project progress.
Honesty laws from taskboard/report.py apply: counts and dates only, no
forecasts; every figure carries a direct label; all user-authored text is
escaped; project hue is decoration over an already-legible row.
"""
from __future__ import annotations

import html
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fixture import MARKS, PEOPLE, TODAY, all_boards

from taskboard.models import days_in_phase, parse_iso
from taskboard.people import mention_ids, split_mentions
from taskboard.views import HEX, highlight_segments, lanes_of, sitting

OUT = Path(__file__).resolve().parents[1] / "out" / "a-report.html"
WINDOW = 7  # "the last 7 days" / "the next 7 days"

CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { margin: 0; padding: 1.75rem 1.25rem 3rem;
       font: 15px/1.5 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
       background: #0d1117; color: #e6edf3;
       --line: #21262d; --panel: #161b22; --mut: #8b98a5;
       --chip-bg: #1c2129; --mark: #c9d4e0; }
main { max-width: 62rem; margin: 0 auto; }
h1 { font-size: 1.45rem; margin: 0 0 .2rem; letter-spacing: .01em; }
h2 { font-size: 1rem; margin: 2rem 0 .6rem; padding-bottom: .3rem;
     border-bottom: 1px solid var(--line); font-weight: 650; }
h2 .tag { float: right; font-size: .72rem; color: var(--mut); font-weight: 500;
          text-transform: uppercase; letter-spacing: .07em; padding-top: .25rem; }
.sub { color: var(--mut); margin: 0 0 1.5rem; font-size: .88rem; }
.sub b { color: var(--mark); font-weight: 600; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(7.2rem, 1fr));
         gap: .6rem; margin: 0 0 .25rem; }
.tile { background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
        padding: .6rem .75rem; }
.tile .n { font-size: 1.55rem; font-weight: 650; letter-spacing: -.01em; }
.tile .n small { font-size: .8rem; color: var(--mut); font-weight: 500; }
.tile .k { color: var(--mut); font-size: .72rem; text-transform: uppercase;
           letter-spacing: .06em; margin-top: .1rem; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; align-items: start; }
@media (max-width: 780px) { .cols { grid-template-columns: 1fr; } }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
         padding: .35rem .8rem .6rem; }
.panel h3 { font-size: .78rem; text-transform: uppercase; letter-spacing: .07em;
            color: var(--mut); margin: .5rem 0 .35rem; font-weight: 650; }
table { border-collapse: collapse; width: 100%; margin: .4rem 0 0; font-size: .87rem; }
th, td { text-align: left; padding: .4rem .55rem; border-bottom: 1px solid var(--line);
         vertical-align: top; overflow-wrap: anywhere; }
th { color: var(--mut); font-weight: 600; font-size: .72rem; text-transform: uppercase;
     letter-spacing: .06em; overflow-wrap: anywhere; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
th.n { white-space: normal; }
@media (max-width: 560px) { .col-open, .col-mom { display: none; } }
tr:last-child td { border-bottom: none; }
.chip { display: inline-block; width: .58rem; height: .58rem; border-radius: 2px;
        margin-right: .4rem; vertical-align: baseline; }
.board-chip { display: inline-block; font-size: .68rem; font-weight: 650; padding: 0 .4rem;
              border-radius: 99px; border: 1px solid var(--line); background: var(--chip-bg);
              color: var(--mut); letter-spacing: .04em; white-space: nowrap; }
.mark { font-weight: 650; }
.mut { color: var(--mut); }
.over { color: #f43f5e; font-weight: 600; }
.blocked { color: #fb923c; font-weight: 650; }
.done { color: #4ade80; }
.hl-soon { color: #fbbf24; }
.hl-over { color: #f43f5e; font-weight: 600; }
.hl-green { color: #4ade80; }
.mention { color: #f472b6; font-weight: 650; }
.note, .meta { color: var(--mut); font-size: .82rem; }
.list { list-style: none; margin: .3rem 0 0; padding: 0; }
.list li { padding: .45rem 0; border-bottom: 1px solid var(--line); }
.list li:last-child { border-bottom: none; }
.list .when { font-variant-numeric: tabular-nums; white-space: nowrap; }
.chain { margin: .4rem 0 0; padding: 0; list-style: none; }
.chain li { display: flex; gap: .5rem; align-items: baseline; padding: .28rem 0;
            border-bottom: none; }
.chain .arrow { color: var(--mut); flex: 0 0 auto; }
.chain .dot { flex: 0 0 auto; width: .5rem; height: .5rem; border-radius: 50%;
              background: var(--mut); align-self: center; }
.chain .dot.done { background: #4ade80; }
.chain .dot.late { background: #f43f5e; }
.chain .dot.open { background: #38bdf8; }
.prog { width: 100%; min-width: 5.5rem; }
.prog .bar { height: .5rem; border-radius: 3px; background: var(--chip-bg);
             overflow: hidden; margin-top: .2rem; }
.prog .bar i { display: block; height: 100%; border-radius: 3px; }
.prog .lbl { font-size: .74rem; color: var(--mut); font-variant-numeric: tabular-nums; }
footer { color: var(--mut); font-size: .8rem; margin-top: 2.5rem;
         border-top: 1px solid var(--line); padding-top: .7rem; }
h2, h3 { page-break-after: avoid; }
.panel, .chain { page-break-inside: avoid; }
tr { page-break-inside: avoid; }
@media (prefers-color-scheme: light) {
  body { background: #ffffff; color: #1f2328;
         --line: #d0d7de; --panel: #f6f8fa; --mut: #59636e;
         --chip-bg: #eaeef2; --mark: #1f2328; }
}
@media print {
  body { background: #fff; color: #000; padding: 0;
         font-size: 8.6px; line-height: 1.25;
         --line: #bbb; --panel: #fff; --mut: #444; --chip-bg: #eee; --mark: #000; }
  main { max-width: none; }
  h1 { font-size: 1.05rem; }
  h2 { font-size: .78rem; margin: .55rem 0 .2rem; }
  h2 .tag { display: none; }
  h3 { font-size: .68rem; }
  section .sub { display: none; }
  .sub { font-size: .72rem; margin-bottom: .45rem; }
  .tiles { grid-template-columns: repeat(auto-fit, minmax(4.5rem, 1fr)); gap: .3rem; }
  .tile { border-color: #999; padding: .2rem .35rem; }
  .tile .n { font-size: .9rem; }
  .tile .k { font-size: .54rem; }
  th, td { padding: .1rem .25rem; }
  th { font-size: .56rem; }
  .note, .meta { font-size: .68rem; }
  .cols { gap: .8rem; }
  .panel { padding: .05rem .4rem .15rem; border-color: #999; margin-bottom: .3rem; }
  .note { display: none; }  /* print is the compact one-pager; note snippets stay on screen */
  div.meta { display: inline; font-size: .95em; }
  div.meta::before { content: " · "; color: #999; }
  .list li, .chain li { padding: .06rem 0; }
  .board-chip { font-size: .56rem; }
  footer { margin-top: .5rem; font-size: .6rem; color: #444; }
  .sub, footer { color: #444; }
  .over, .hl-over { color: #b00020; }
  .done, .hl-green { color: #1a7f37; }
  .hl-soon { color: #8a6100; }
  .mention { color: #a0247a; }
  .blocked { color: #b35000; }
  section { page-break-inside: auto; }
}
"""

TONE_CLASS = {"soon": "hl-soon", "over": "hl-over", "green": "hl-green"}


def e(text: object) -> str:
    return html.escape(str(text), quote=True)


def due_word(days: int | None, closed: bool = False) -> str:
    if days is None:
        return "no date"
    if closed:
        return f"{days:+d}d"
    if days < 0:
        return f"{-days}d overdue"
    if days == 0:
        return "due today"
    return f"in {days}d"


def note_html(text: str, max_lines: int = 2) -> str:
    """Notes with the app's own highlighter and mention resolution, escaped."""
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    out = []
    for ln in lines[:max_lines]:
        pieces = []
        for seg, tone in highlight_segments(ln):
            for piece, handle in split_mentions(seg):
                if handle and handle in PEOPLE:
                    pieces.append(f'<span class="mention">@{e(PEOPLE[handle].name)}</span>')
                elif piece:
                    pieces.append(f'<span class="{TONE_CLASS.get(tone, "mut")}">{e(piece)}</span>')
        out.append("".join(pieces))
    return f'<div class="note">{"<br>".join(out)}</div>' if out else ""


def task_due_days(task, today) -> int | None:
    d = parse_iso(task.due_date)
    return (d - today).days if d else None


def gather():
    boards = all_boards()
    per_board = {}
    open_all, done_all, late_all, next_all, changed_all, milestones = (
        [], [], [], [], [], [])
    archived_n = 0
    for bname, board in boards.items():
        lanes = lanes_of(board, False, TODAY)
        visible = board.visible_tasks(False)
        archived_n += sum(1 for t in board.tasks if t.archived)
        open_ = [t for t in visible if not board.is_done(t)]
        open_all.extend(open_)
        done_all.extend(t for t in visible if board.is_done(t))
        per_board[bname] = (board, lanes, open_)
        for t in visible:
            changed = parse_iso(t.phase_changed)
            if changed is not None and 0 <= (TODAY - changed).days <= WINDOW:
                changed_all.append((t, board, bname, TODAY - changed))
            if t.milestone and t.mark:
                milestones.append((t, board, bname))
        for t in open_:
            proj = board.project_by_id(t.project_id)
            pname = proj.name if proj else "Inbox"
            dd = task_due_days(t, TODAY)
            if dd is not None and dd < 0:
                late_all.append((t, board, bname, pname, dd))
            if dd is not None and 0 <= dd <= WINDOW:
                next_all.append((t, board, bname, pname, dd))
    return (boards, per_board, open_all, done_all, late_all, next_all,
            changed_all, milestones, archived_n)


def tiles(boards, per_board, open_all, done_all, late_all, next_all,
          archived_n) -> str:
    proj_n = sum(len(lanes) for _, lanes, _ in per_board.values())
    high_n = 0
    for board, _, open_ in per_board.values():
        high_n += sum(1 for t in open_ if t.priority == "high")
    late_n = len(late_all)
    pairs = [
        (str(len(boards)), "boards"), (str(proj_n), "projects"),
        (str(len(open_all)), "open"), (str(len(done_all)), "done"),
        (f'{late_n}' if late_n else "0", "overdue"),
        (str(len(next_all)), "due ≤ 7d"),
        (str(high_n), "high prio"),
        (str(archived_n), "archived"),
    ]
    cells = "".join(
        f'<div class="tile"><div class="n">{e(v)}</div>'
        f'<div class="k">{e(k)}</div></div>' for v, k in pairs)
    return f'<div class="tiles">{cells}</div>'


def changed_section(changed_all) -> str:
    rows = []
    for t, board, bname, ago in sorted(changed_all, key=lambda x: x[3]):
        proj = board.project_by_id(t.project_id)
        pname = proj.name if proj else "Inbox"
        done = board.is_done(t)
        rows.append(
            f'<tr><td class="n mut">{ago.days}d ago</td>'
            f"<td>{e(t.title)}"
            f'<div class="meta">{e(pname)} · <span class="board-chip">{e(bname)}</span></div></td>'
            f"<td>{'done' if done else e(t.phase)}"
            f'{" · " + str(days_in_phase(t, TODAY)) + "d in phase" if days_in_phase(t, TODAY) is not None else ""}</td>'
            f"</tr>")
    return ("<table><thead><tr><th class='n'>moved</th><th>task</th>"
            "<th>now in</th></tr></thead><tbody>" + "".join(rows) +
            "</tbody></table>")


def horizon_panel(title, items, board_lookup, *, late: bool) -> str:
    rows = []
    for t, board, bname, pname, dd in sorted(items, key=lambda x: x[4]):
        word = due_word(dd)
        cls = "over" if late else ""
        blocked = '<span class="blocked">blocked</span> · ' if t.blocked else ""
        rows.append(
            f'<tr><td class="n {cls}">{e(word)}</td>'
            f"<td>{blocked}{e(t.title)}"
            f'<div class="meta">{e(pname)} · <span class="board-chip">{e(bname)}</span></div>'
            f"{note_html(t.notes)}</td>"
            f"<td class='mut'>{e(t.phase)}"
            f'{" · " + str(days_in_phase(t, TODAY)) + "d" if days_in_phase(t, TODAY) is not None else ""}</td>'
            f"</tr>")
    body = "".join(rows) or '<tr><td class="mut">nothing here</td><td></td><td></td></tr>'
    return (f'<div class="panel"><h3>{e(title)}</h3>'
            f"<table><thead><tr><th class='n'>due</th><th>task</th>"
            "<th>phase</th></tr></thead><tbody>" + body +
            "</tbody></table></div>")


def milestones_section(milestones) -> str:
    groups: dict[str, list] = {mid: [] for mid in MARKS}
    other = []
    for t, board, bname in milestones:
        groups.get(t.mark, other).append((t, board, bname))
    out = []
    for mid, mark in MARKS.items():
        items = groups[mid]
        if not items:
            continue
        rows = []
        for t, board, bname in sorted(items, key=lambda x: task_due_days(x[0], TODAY) or 9999):
            dd = task_due_days(t, TODAY)
            proj = board.project_by_id(t.project_id)
            pname = proj.name if proj else "Inbox"
            deps = [board.task_by_id(d) for d in t.depends_on]
            dep_txt = ""
            if deps:
                pending = sum(1 for d in deps if d and not board.is_done(d))
                dep_txt = (f'<div class="meta">after: '
                           + " · ".join(e(d.title) for d in deps if d)
                           + f" ({pending} still open)</div>")
            rows.append(
                f"<tr><td>{e(t.title)}"
                f'<div class="meta">{e(pname)} · <span class="board-chip">{e(bname)}</span></div>'
                f"{note_html(t.notes, 1)}{dep_txt}</td>"
                f'<td style="white-space:nowrap">{e(t.phase)}</td>'
                f'<td class="n {"over" if dd is not None and dd < 0 else ""}">{e(due_word(dd))}</td>'
                f"</tr>")
        hue = HEX.get(mark.colour, HEX["mut"])
        out.append(
            f'<h3 style="margin-top:1rem"><span class="chip" style="background:{hue}"></span>'
            f'{e(mark.name)} <span class="mark">{e(mark.shape)}</span></h3>'
            f"<table><thead><tr><th>milestone</th><th>phase</th>"
            "<th class='n'>due</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")
    return "".join(out)


def chains_section(boards) -> str:
    out = []
    for bname, board in boards.items():
        tasks = {t.id: t for t in board.visible_tasks(False)}
        depended = {d for t in tasks.values() for d in t.depends_on if d in tasks}

        def children(tid):
            return sorted((x for x in tasks.values() if tid in x.depends_on),
                          key=lambda x: x.title)

        heads = [t for t in tasks.values()
                 if not t.depends_on and t.id in depended]
        if not heads:
            continue
        blocks = []
        for head in sorted(heads, key=lambda t: t.title):
            path = [head]
            seen = {head.id}
            while True:
                kids = [k for k in children(path[-1].id) if k.id not in seen]
                if not kids:
                    break
                path.append(kids[0])
                seen.add(kids[0].id)
            steps = []
            for i, t in enumerate(path):
                dd = task_due_days(t, TODAY)
                if board.is_done(t):
                    dot, state = "done", '<span class="done">done</span>'
                elif t.blocked:
                    dot, state = "late", '<span class="blocked">blocked</span>'
                elif dd is not None and dd < 0:
                    dot, state = "late", f'<span class="over">{e(due_word(dd))}</span>'
                else:
                    dot, state = "open", e(t.phase)
                age = days_in_phase(t, TODAY)
                age_txt = f" · {age}d in phase" if age is not None else ""
                cell = (f'<span class="dot {dot}"></span><span>{e(t.title)}'
                        f'<span class="meta"> — {state}{age_txt}</span></span>')
                arrow = '<span class="arrow">→</span>' if i else '<span class="arrow"></span>'
                steps.append(f"<li>{arrow}{cell}</li>")
            proj = board.project_by_id(path[0].project_id)
            pname = proj.name if proj else "Inbox"
            blocks.append(
                f'<div class="panel" style="margin-bottom:.7rem"><h3>{e(pname)} · '
                f'<span class="board-chip">{e(bname)}</span></h3>'
                f'<ul class="chain">{"".join(steps)}</ul></div>')
        out.append("".join(blocks))
    return "".join(out)


def progress_section(per_board) -> str:
    rows = []
    for bname, (board, lanes, _) in per_board.items():
        for lane in lanes:
            hue = HEX.get(lane.hue, HEX["mut"])
            pct = round(100 * lane.done_n / lane.total) if lane.total else 0
            status = "" if lane.status == "on_track" else f' · {e(lane.status)}'
            late = (f'<span class="over">{len(lane.late)} overdue</span>'
                    if lane.late else "0 overdue")
            momentum = sitting(lane, TODAY) or "nothing open"
            bar = (f'<div class="prog"><div class="lbl">{lane.done_n}/{lane.total} '
                   f'done ({pct}%)</div>'
                   f'<div class="bar"><i style="width:{pct}%;background:{hue}"></i></div></div>')
            rows.append(
                f"<tr><td><span class='chip' style='background:{hue}'></span>{e(lane.name)}"
                f'<div class="meta"><span class="board-chip">{e(bname)}</span>{status}</div></td>'
                f"<td>{bar}</td>"
                f"<td class='n'>{len(lane.open)}</td>"
                f"<td class='n'>{late}</td>"
                f"<td class='n {'over' if lane.due_in is not None and lane.due_in < 0 and not lane.closed else 'mut'}'>"
                f"{e(due_word(lane.due_in, lane.closed))}</td>"
                f"<td class='mut col-mom'>{e(momentum)}</td></tr>")
    return ("<table><thead><tr><th>project</th><th>progress</th>"
            "<th class='n col-open'>open</th><th class='n'>late</th>"
            "<th class='n'>project due</th><th class='col-mom'>momentum</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def people_section(per_board) -> str:
    """Who the notes point at — mentions resolved to names, one line each."""
    rows = []
    for handle, person in PEOPLE.items():
        hits = []
        for bname, (board, _, open_) in per_board.items():
            for t in open_:
                if handle in mention_ids(t.notes):
                    proj = board.project_by_id(t.project_id)
                    hits.append(f"{e(t.title)} ({e(proj.name if proj else 'Inbox')} · "
                                f'<span class="board-chip">{e(bname)}</span>)')
        if hits:
            rows.append(f"<tr><td>@{e(person.name)}"
                        f'<div class="meta">{e(person.role)}</div></td>'
                        f"<td>{'; '.join(hits)}</td></tr>")
    if not rows:
        return ""
    return ("<table><thead><tr><th>person</th><th>mentioned on open work</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def build() -> str:
    (boards, per_board, open_all, done_all, late_all, next_all, changed_all,
     milestones, archived_n) = gather()
    changed_n = len(changed_all)
    header = f"""
<h1>Status report · all boards</h1>
<p class="sub">Generated <b>{e(TODAY.isoformat())}</b> · covers Personal, Client A and
Course · counts and dates only — nothing here is a forecast. Work with no recorded
phase-change date reads <em>unaged</em>, exactly as the board says.</p>
"""
    late_panel = horizon_panel(
        f"Late work · {len(late_all)} task{'s' if len(late_all) != 1 else ''}",
        late_all, None, late=True)
    next_panel = horizon_panel(
        f"Next 7 days · {len(next_all)} task{'s' if len(next_all) != 1 else ''}",
        next_all, None, late=False)
    people = people_section(per_board)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Status report · taskboard · {e(TODAY.isoformat())}</title>
<style>{CSS}</style></head>
<body><main>
{header}
<section><h2>Where everything stands <span class="tag">3 boards</span></h2>
{tiles(boards, per_board, open_all, done_all, late_all, next_all, archived_n)}
</section>
<section><h2>What changed in the last 7 days <span class="tag">{changed_n} task{'s' if changed_n != 1 else ''}</span></h2>
<p class="sub" style="margin-bottom:.4rem">Every task whose phase moved since
{e((TODAY - timedelta(days=WINDOW)).isoformat())}, oldest move first.</p>
{changed_section(changed_all)}
</section>
<section><h2>The two horizons <span class="tag">late · next 7 days</span></h2>
<div class="cols">{late_panel}{next_panel}</div>
</section>
<section><h2>Milestones by class <span class="tag">{len(milestones)} upcoming</span></h2>
{milestones_section(milestones)}
</section>
<section><h2>Dependency chains <span class="tag">what waits on what</span></h2>
{chains_section(boards)}
</section>
<section><h2>Per-project progress <span class="tag">done vs open</span></h2>
{progress_section(per_board)}
</section>
{('<section><h2>Who the notes point at <span class="tag">@mentions</span></h2>' + people + '</section>') if people else ''}
<footer>taskboard · a local file, generated on demand. Every figure above carries
its own label; project colour is decoration, never the message. Archived work is
counted but never "late" — nothing is expected of it.</footer>
</main></body></html>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

"""The one extraction behind the HTML reports (the workspace and the deck).

READ-ONLY, like `report.py`: `extract` takes loaded boards and returns plain,
JSON-able facts; nothing here saves a board. Both renderers read ONLY that
dict, so they cannot disagree on a project, a task, a status or a due word.

ONE STATUS RULE, here and nowhere else: archived > done > late (not done, due
before today) > open. The page and the deck read `status` and `due_word`; they
never re-derive them. Due words are the CLI report's own (`report._due_word`).

UNTRUSTED TEXT. Board strings reach HTML only escaped (`esc` = `report._e`), or
through the page's `textContent`; `notes_html` is built here from escaped
pieces in constant tags; `embed_json` makes the data unable to close its
`<script>` element. Task URLs keep only what `views.valid_url` accepts.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .models import days_in_phase, parse_iso
from .people import mention_ids, split_mentions
from .report import _due_word, _e
from .views import HEX, highlight_segments, lane_facts, sitting, valid_url

esc = _e

SHAPE_VERSION = 1


def _hex(name: str | None) -> str:
    return HEX.get(name or "", HEX["mut"])


def _iso(value: str | None) -> str | None:
    d = parse_iso(value)
    return d.isoformat() if d else None


def notes_html(text: str, people: dict) -> str:
    """Notes as inert HTML: ==soon== / !!over!! / ++green++ tones and @mentions
    of directory people as `@Name`; every piece escaped, only constant tags."""
    if not text:
        return ""
    lines = []
    for line in text.split("\n"):
        parts = []
        for seg, tone in highlight_segments(line):
            for piece, handle in split_mentions(seg):
                if handle is not None and handle in people:
                    parts.append(f'<span class="hl-{tone} mention">@{esc(people[handle].name)}</span>')
                else:
                    parts.append(f'<span class="hl-{tone}">{esc(piece)}</span>')
        lines.append("".join(parts))
    return "<br>".join(lines)


def _notes_text(text: str) -> str:
    return "\n".join("".join(seg for seg, _ in highlight_segments(line))
                     for line in (text or "").split("\n"))


def embed_json(d: dict) -> str:
    """JSON safe inside `<script type="application/json">`: no `<`, `>` or `&`."""
    raw = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    return raw.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def _status(board, t, today: date) -> str:
    if t.archived:
        return "archived"
    if board.is_done(t):
        return "done"
    due = parse_iso(t.due_date)
    if due is not None and due < today:
        return "late"
    return "open"


def _chains(tasks: list[dict]) -> None:
    kids: dict[str, list[str]] = {}
    for t in tasks:
        for d in t["deps"]:
            kids.setdefault(d, []).append(t["key"])
    for t in tasks:
        chain, seen, stack = [], {t["key"]}, [t["key"]]
        while stack:
            for kid in kids.get(stack.pop(), []):
                if kid not in seen:
                    seen.add(kid)
                    chain.append(kid)
                    stack.append(kid)
        t["chain"] = chain


def extract(boards: list, people: dict, marks: dict, today: date,
            project: str | None = None) -> dict:
    """`boards`: `(registry id | None, name, colour, Board)` per loaded board.
    `project`: None for every project, or one project KEY (`<board key>:<id>`)."""
    out_boards, out_projects, out_tasks = [], [], []
    for pos, (bid, bname, bcolour, board) in enumerate(boards):
        bkey = bid if bid is not None else f"#{pos}"
        rows = []
        for p in board.projects:
            rows.append((f"{bkey}:{p.id}", p, [t for t in board.tasks if t.project_id == p.id]))
        inbox = [t for t in board.tasks if board.project_by_id(t.project_id) is None]
        if inbox:
            rows.append((f"{bkey}:inbox", None, inbox))
        rows = [r for r in rows if project is None or r[0] == project]
        if not rows and project is not None:
            continue
        out_boards.append({"key": bkey, "name": bname, "colour": _hex(bcolour)})
        in_scope = {t.id for _, _, ts in rows for t in ts}
        for pkey, p, ts in rows:
            if p is None:
                lane = lane_facts(board, today, "Inbox", "dim", "on_track", None, ts)
            else:
                lane = lane_facts(board, today, p.name, p.color, p.status, p.due_date, ts,
                                  start_date=p.start_date)
            out_projects.append({
                "key": pkey, "board": bkey, "id": p.id if p else None,
                "name": lane.name, "colour": _hex(lane.hue),
                "archived": bool(p and p.archived), "status": lane.status,
                "momentum": sitting(lane, today) or "nothing open",
                "open": len(lane.open), "late": len(lane.late),
                "done": sum(1 for t in ts if not t.archived and board.is_done(t)),
                "worst": lane.worst or None, "high": lane.high,
                "due": _iso(p.due_date) if p else None,
                "due_word": _due_word(lane.due_in, lane.closed),
                "phases": list(board.phases),
            })
            for t in ts:
                due = parse_iso(t.due_date)
                due_in = (due - today).days if due else None
                mark = t.mark if t.milestone and t.mark in marks else None
                out_tasks.append({
                    "key": f"{bkey}:{t.id}", "project": pkey, "board": bkey,
                    "title": t.title, "phase": t.phase, "priority": t.priority,
                    "start": _iso(t.start_date), "due": due.isoformat() if due else None,
                    "due_in": due_in, "age": days_in_phase(t, today),
                    "done": board.is_done(t), "archived": t.archived,
                    "status": _status(board, t, today), "blocked": t.blocked,
                    "milestone": t.milestone, "mark": mark,
                    "mentions": [h for h in mention_ids(t.notes) if h in people],
                    "deps": [f"{bkey}:{d}" for d in t.depends_on if d in in_scope],
                    "chain": [],
                    "due_word": _due_word(due_in),
                    "notes_html": notes_html(t.notes, people),
                    "notes_text": _notes_text(t.notes),
                    "urls": [u for u in map(valid_url, t.urls) if u],
                })
    if project is not None and not out_projects:
        raise ValueError(f"no project with the key {project!r} on the given boards")
    _chains(out_tasks)
    mentioned = {h for t in out_tasks for h in t["mentions"]}
    used = {t["mark"] for t in out_tasks if t["mark"]}
    return {
        "v": SHAPE_VERSION,
        "meta": {"generated": today.isoformat(), "today": today.isoformat(),
                 "scope": {"kind": "all" if project is None else "project",
                           "project": project,
                           "boards": [b["name"] for b in out_boards]},
                 "view": None},
        "boards": out_boards,
        "projects": out_projects,
        "tasks": out_tasks,
        "people": [{"id": h, "name": p.name, "role": p.role}
                   for h, p in people.items() if h in mentioned],
        "marks": [{"key": k, "name": m.name, "shape": m.shape, "colour": _hex(m.colour)}
                  for k, m in marks.items() if k in used],
    }


def slug(name: str) -> str:
    """The CLI report's slug rule (`report.report_path`), pinned by TC-3123."""
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")[:40]


def report_name(kind: str, today: date, board_slug: str | None = None,
                project_slug: str | None = None) -> str:
    if kind not in ("workspace", "deck"):
        raise ValueError(f"unknown report kind: {kind}")
    if project_slug is None:
        return f"{kind}-{today.isoformat()}.html"
    return f"{kind}-{board_slug}-{project_slug}-{today.isoformat()}.html"


def _scope_slugs(d: dict) -> tuple[str | None, str | None]:
    key = d["meta"]["scope"]["project"]
    if key is None:
        return None, None
    proj = next((p for p in d["projects"] if p["key"] == key), None)
    if proj is None:
        raise ValueError(f"no project with the key {key!r} in the dict")
    board = next(b for b in d["boards"] if b["key"] == proj["board"])
    return slug(board["name"]), slug(proj["name"])


def write_reports(d: dict, kinds: tuple[str, ...], folder: Path, today: date) -> list[Path]:
    """Render each kind from the dict and write it into `folder` (a same-day
    file is overwritten). Every kind is checked before the folder or any file
    is touched, so a bad kind writes nothing. The renderers are imported here, not at module
    level: they import this module."""
    bad = [k for k in kinds if k not in ("workspace", "deck")]
    if bad:
        raise ValueError(f"unknown report kind: {bad[0]}")
    board_slug, project_slug = _scope_slugs(d)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    for kind in kinds:
        if kind == "workspace":
            from . import report_workspace as renderer
        else:
            from . import report_deck as renderer
        path = folder / report_name(kind, today, board_slug, project_slug)
        path.write_text(renderer.render(d), encoding="utf-8")
        out.append(path)
    return out

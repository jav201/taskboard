"""Headless capture of the next-level prototypes -> SVG + one TXT.

    python prototypes/next_level/capture.py

Same synthetic fixture as the other capture scripts — these artifacts are
committable. Pins, notes and phase_changed are enriched IN MEMORY ONLY (the
fixture file is never written): the fixture pins nothing and stamps nothing,
and without that minimum the two focus variants would render empty.
"""
from __future__ import annotations

import io
import os
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rich.console import Console

from taskboard.models import Board
from taskboard.views import focus_tasks, render_gantt, render_kanban

import proto

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

W, H = 118, 30
TODAY = date(2026, 8, 17)
OUT = Path(__file__).resolve().parent / "out"
FIXTURE = ROOT / "prototypes" / "out" / "_fixture_late.json"
QUERY = "api"

PIN = ["a6530d", "2ea15c", "ed6306", "f26153", "8229aa", "26964b"]
NOTES = {
    "a6530d": ("==Hero needs final copy== before Friday\n"
               "reference shots live in the !!brand folder!!\n"
               "- [x] wireframes\n- [ ] mobile layout\n- [ ] assets handoff"),
    "2ea15c": ("repro: pay with an expired card -> 500, never 402\n"
               "!!rollbacks are fine: fix forward!!\n"
               "- [ ] regression test for the gateway mapping"),
    "ed6306": ("notify partners ==two weeks ahead==\n"
               "- [x] usage report\n- [ ] sunset headers on v1 responses"),
    "8229aa": "three PRs waiting on me\n++review latency is down this week++",
    "26964b": "expires !!Aug 20!! — auto-renew is disabled",
}
AGE_DAYS = {"a6530d": 2, "2ea15c": 14, "ed6306": 5, "f26153": 21,
            "8229aa": 7, "26964b": 9, "c604ff": 3, "df1d6d": 18}


def _enrich(board: Board) -> None:
    """In-memory demo state: pins for the focus board, notes with highlight
    syntax for the review card, phase_changed so 'stale first' has a signal."""
    for t in board.tasks:
        pre = t.id[:6]
        if pre in PIN:
            t.pinned = True
        if pre in NOTES:
            t.notes = NOTES[pre]
        if pre in AGE_DAYS:
            t.phase_changed = (TODAY - timedelta(days=AGE_DAYS[pre])).isoformat()


def capture() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not FIXTURE.exists():
        raise SystemExit(f"FIXTURE MISSING: {FIXTURE}")
    board = Board.load(FIXTURE)
    _enrich(board)
    tasks = board.visible_tasks(False)
    sel = tasks[len(tasks) // 3].id if tasks else None
    pinned = focus_tasks(board, False)

    # rich 15 needs BOTH width and height: Console.size honours _width only
    # when _height is also set, otherwise every line wraps at the 80-col
    # fallback (this silently broke the older capture scripts' SVGs).
    con = Console(width=W + 2, height=H + 10, force_terminal=True,
                  legacy_windows=False, color_system="truecolor")

    figures = [
        ("kanban-baseline", "kanban actual (baseline)",
         render_kanban(board, False, sel, today=TODAY, width=W, height=H)),
        ("kanban-lanes-priority", "1A · kanban lanes: prioridad",
         proto.kanban_lanes(board, proto.priority_lanes(board), sel,
                            TODAY, W, H, "priority")),
        ("kanban-lanes-project", "1B · kanban lanes: proyecto",
         proto.kanban_lanes(board, proto.project_lanes(board), sel,
                            TODAY, W, H, "project")),
        ("focus-review-queue", "2A · focus: review queue",
         proto.focus_review(board, pinned, 1, TODAY, W, H)),
        ("focus-stale-tiles", "2B · focus: tiles stale-first",
         proto.focus_stale(board, pinned, sel, TODAY, W, H)),
        ("search-filter-kanban", f"3A · filtro vivo /{QUERY} en kanban",
         proto.search_view(render_kanban, board, QUERY, TODAY, W, H, con,
                           selected_id=sel)),
        ("search-filter-gantt", f"3A · filtro vivo /{QUERY} en gantt",
         proto.search_view(render_gantt, board, QUERY, TODAY, W, H,
                           con, selected_id=sel)),
        ("search-jump-palette", f"3B · jump palette /{QUERY}",
         proto.jump_palette(board, QUERY, TODAY, W, H, con, selected_id=sel)),
        ("search-context-dim", f"3C · context dim /{QUERY}",
         proto.context_dim(board, QUERY, TODAY, W, H, con, selected_id=sel)),
    ]

    plain_all: list[str] = []
    for slug, title, text in figures:
        # record=True + print: save_svg needs the RECORDED buffer, and wrapping
        # the print in capture() starves it (the old kanban-baseline.svg trap)
        rec = Console(record=True, width=W + 2, height=H + 10,
                      force_terminal=True, legacy_windows=False,
                      color_system="truecolor", file=io.StringIO())
        rec.print(text)
        rec.save_svg(str(OUT / f"{slug}.svg"), title=f"taskboard — {title}")

        plain = Console(width=W + 2, height=H + 10, force_terminal=False,
                        legacy_windows=False)
        with plain.capture() as cap:
            plain.print(text)
        plain_all.append(f"{'=' * W}\n=== {title.upper()}\n{'=' * W}\n"
                         + cap.get())
        print(f"wrote {slug}.svg")

    (OUT / "next-level.txt").write_text("\n".join(plain_all),
                                        encoding="utf-8")
    print(f"wrote next-level.txt | viewport {W}x{H} | query '{QUERY}'")


if __name__ == "__main__":
    capture()

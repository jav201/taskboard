"""Links mean "waits on" (batch 2026-10-04-batch-01, HLR-501, HLR-504).

Field report: the shipped `b` did two jobs — it set the Blocked flag AND appended a
task id to `depends_on` — so links piled up unseen behind the flag, and unblocking
left them behind (DEPS-CONTRACT.md, P-1). The operator could not tell whether
dependencies existed.

Law: `b` is the external block only (`▲`, a block with no task to point at); a link
is made with `L`. Every board here is synthetic (`tests/kg_board.py`).
"""
from __future__ import annotations

import json

import kg_board
from taskboard.app import TaskboardApp
from taskboard.keymap import KEYMAP


def _key_for(action: str) -> str:
    return next(k for k in KEYMAP if k.action == action).keys.split(",")[0]


async def test_TC_506_b_is_the_external_block_only(tmp_path):
    """TC-506, the `b` arm (LLR-501.4, D-504): `b` twice on a task that waits on
    another flips `blocked` True then False, pushes no screen, leaves
    `depends_on` exactly as it was (board and file), and is one undo step each.
    RED on base: `b` opens BlockerPicker (P-1) and, picked, appends an id."""
    path = tmp_path / "board.json"
    kg_board.shifted(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "tm3"                 # waits on tm2
        stored = list(app.board.task_by_id("tm3").depends_on)
        for want in (True, False):
            await pilot.press(_key_for("toggle_blocked"))
            await pilot.pause()
            assert len(app.screen_stack) == 1
            t = app.board.task_by_id("tm3")
            assert (t.blocked, t.depends_on) == (want, stored)
            saved = {x["id"]: x for x in json.loads(path.read_text(encoding="utf-8"))["tasks"]}
            assert (saved["tm3"]["blocked"], saved["tm3"]["depends_on"]) == (want, stored)
        await pilot.press(_key_for("undo"))
        await pilot.pause()
        assert app.board.task_by_id("tm3").blocked is True


# =========================================================================== #
# Increment 002 — the waits-on model, the marks, the guard
# =========================================================================== #
import ast  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
from collections import Counter  # noqa: E402
from datetime import date, timedelta  # noqa: E402
from pathlib import Path  # noqa: E402

import pytest  # noqa: E402
from rich.text import Text  # noqa: E402

from taskboard import views  # noqa: E402
from taskboard.models import (Board, Task, archive_refusal, dependents_chain,  # noqa: E402
                              is_open, link_marks, link_overlap, loop_path,
                              open_dependents, open_predecessors, ready_messages,
                              waiting_ids)
from taskboard.views import HEX, card_cell, gantt_dep_mark, kanban_card  # noqa: E402

TODAY = kg_board.TODAY


def _plain(markup: str) -> str:
    return Text.from_markup(markup).plain


def _session_states() -> list[Board]:
    """The 11 states `deps_logic.py`'s session steps through (Q-17), re-derived:
    each a fresh kg board with the steps so far applied (a refused step leaves
    the board as it was). Guarded: exactly 11."""
    steps = [
        lambda b: None,                                                   # 0 initial
        lambda b: b.task_by_id("tw6").depends_on.append("tw5"),            # 1 L w6→w5
        lambda b: None,                                                   # 2 loop refused
        lambda b: b.task_by_id("tw5").depends_on.remove("tw4"),            # 3 remove w5→w4
        lambda b: b.task_by_id("tw5").depends_on.append("tw4"),            # 4 its undo
        lambda b: setattr(b.task_by_id("tm2"), "phase", "Done"),           # 5 m2 done
        lambda b: setattr(b.task_by_id("tw2"), "phase", "Done"),           # 6 w2 done
        lambda b: setattr(b.task_by_id("tm4"), "blocked", True),           # 7 b on m4
        lambda b: None,                                                   # 8 archive refused
        lambda b: setattr(b.task_by_id("tw1"), "archived", True),          # 9 archive done w1
        lambda b: b.task_by_id("ta2").depends_on.remove("ta3"),            # 10 remove a2→a3
    ]
    out = []
    for n in range(len(steps)):
        b = kg_board.build()
        for step in steps[:n + 1]:
            step(b)
        out.append(b)
    assert len(out) == 11
    return out


def test_TC_501_waiting_is_derived_from_live_links_in_every_session_state():
    """TC-501 (LLR-501.1): in each of the 11 session states, the reverse-index
    marks agree with the per-task derivation (`waiting ⇔ ◂ > 0`), Σ◂ == Σ▸, a
    closed task carries (0, 0), and no stored link sits on a loop. RED: a
    closed task counted, a duplicate id counted twice, a dangling id counted."""
    for i, b in enumerate(_session_states()):
        marks = link_marks(b)
        waiting = waiting_ids(b)
        for t in b.tasks:
            w, u = marks[t.id]
            assert w == len(open_predecessors(b, t)), (i, t.id)
            assert u == len(open_dependents(b, t)), (i, t.id)
            assert (t.id in waiting) == (w > 0), (i, t.id)
            if not is_open(b, t):
                assert (w, u) == (0, 0), (i, t.id)
            for x in t.depends_on:
                p = b.task_by_id(x)
                assert p is None or loop_path(b, t, p) is None, (i, t.id, x)
        assert sum(w for w, _ in marks.values()) == sum(u for _, u in marks.values())


def test_TC_501_dangling_self_duplicate_and_teammate_ids_do_not_count(tmp_path):
    """TC-501 (§1.3 live link, A-11/S-8): a dangling id, the task's own id and a
    repeated id count once or not at all; a teammate's task (not a board task)
    that names a local id adds no `▸` and paints no mark. RED: any counted."""
    a = Task("A", phase="Doing", id="A")
    w = Task("W", phase="Backlog", depends_on=["A", "A", "W", "ghost"], id="W")
    b = Board([], [a, w], tmp_path / "b.json", phases=["Backlog", "Doing", "Done"])
    assert link_marks(b) == {"A": (0, 1), "W": (1, 0)}
    # a teammate's task carrying a LOCAL id (code review F3, battery N5): it is
    # not the board's task, so it paints none of that task's marks
    foreign = Task("Theirs", phase="Backlog", depends_on=["A"], id="W")
    assert link_marks(b)["A"] == (0, 1)
    plain = _plain(card_cell(foreign, b, 40, False, today=TODAY))
    assert "◂" not in plain and "▸" not in plain
    # a CLOSED waiter linking to an open task counts nowhere (battery N16)
    b.tasks.append(Task("Done waiter", phase="Done", depends_on=["A"], id="D"))
    assert link_marks(b) == {"A": (0, 1), "W": (1, 0), "D": (0, 0)}


def test_TC_502_the_loop_path_runs_through_closed_tasks():
    """TC-502 (LLR-501.1, D-512): `loop_path(tm2, tm5)` names the loop in order;
    a loop through a CLOSED task is still found, so reopening it cannot surface
    a live loop. RED: a search over open tasks only."""
    b = kg_board.build()
    path = loop_path(b, b.task_by_id("tm2"), b.task_by_id("tm5"))
    assert [t.title for t in path] == ["Audit dependencies", "Beta release to testers",
                                       "Offline sync", "Add push notifications",
                                       "Audit dependencies"]
    b.task_by_id("tm3").phase = "Done"               # the middle of the chain closed
    assert loop_path(b, b.task_by_id("tm2"), b.task_by_id("tm5")) is not None
    assert loop_path(b, b.task_by_id("tm5"), b.task_by_id("to4")) is None


@pytest.mark.parametrize("ws,wd,pd,want", [
    ("2026-10-08", "2026-10-20", "2026-10-10", 3),   # start before the due day
    ("2026-10-10", "2026-10-20", "2026-10-10", 1),   # start ON the due day
    ("2026-10-11", "2026-10-20", "2026-10-10", 0),   # the day after
    (None, "2026-10-07", "2026-10-10", 3),           # no start, due before
    (None, "2026-10-10", "2026-10-10", 0),           # no start, due on
    (None, "2026-10-12", "2026-10-10", 0),           # no start, due after
    ("2026-10-01", None, None, 0),                   # predecessor has no due
    (None, None, "2026-10-10", 0),                   # waiter has no dates
])
def test_TC_503_the_one_overlap_measure(ws, wd, pd, want):
    """TC-503 (LLR-501.1, D-503): the table of §5, row by row
    (`evidence/p1-tables.txt`). RED: `<` for `≤` at the due day (row 2 → 0)."""
    assert link_overlap(Task("w", start_date=ws, due_date=wd), Task("p", due_date=pd)) == want


def test_TC_504_cards_paint_the_marks_never_the_chain():
    """TC-504 (LLR-501.2): for every kg task, `kanban_card` and `card_cell` at
    widths 9, 12, 24 and 40 paint `◂N`/`▸M` equal to `link_marks` whenever they
    paint them, never `⛓`, nothing on a closed card; under pressure `▸` goes
    before `◂` and the due is kept last. RED: a renderer still on the unblock
    count; `▸` on a done card; a mark after the due."""
    b = kg_board.build()
    marks = link_marks(b)
    for t in b.tasks:
        w, u = marks[t.id]
        for wc in (9, 12, 24, 40):
            for row in (*kanban_card(t, b, wc, False, today=TODAY, marks=marks),
                        card_cell(t, b, wc, False, today=TODAY, marks=marks)):
                plain = _plain(row)
                assert "⛓" not in plain
                assert all(int(n) == w for n in re.findall(r"◂(\d+)", plain)), (t.id, wc)
                assert all(int(n) == u for n in re.findall(r"▸(\d+)", plain)), (t.id, wc)
        if not is_open(b, t):
            plain = _plain(card_cell(t, b, 40, False, today=TODAY, marks=marks))
            assert "◂" not in plain and "▸" not in plain
    both = b.task_by_id("tw4")                        # waits on tw2, tw5 waits on it
    assert marks["tw4"] == (1, 1)
    full = _plain(kanban_card(both, b, 40, False, today=TODAY, marks=marks)[1])
    assert "▸1" in full and "◂1" in full
    for wc in range(9, 41):                           # ▸ is shed before ◂, due kept
        row = _plain(kanban_card(both, b, wc, False, today=TODAY, marks=marks)[1])
        assert not ("▸1" in row and "◂1" not in row), row
        assert row.rstrip().endswith("+6d"), row


def test_TC_504_every_card_caller_passes_one_map():
    """TC-504 (LLR-501.2, qa Q-5): the callers are DERIVED from `views.py`'s AST
    (every call of `card_cell` / `kanban_card`, guard ≥ 4) and each passes
    `marks=`. RED: a caller left on the old `unblocks=` or on the fallback."""
    tree = ast.parse(Path(views.__file__).read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and getattr(n.func, "id", None) in ("card_cell", "kanban_card")]
    assert len(calls) >= 4
    for n in calls:
        assert "marks" in {k.arg for k in n.keywords}, ast.unparse(n)[:80]


def test_TC_504_the_help_names_the_marks_and_L():
    """TC-504 (LLR-501.2, ux UX-17): the kanban help says what `◂N` and `▸N` are
    and names `L`; the example line carries both marks before the due."""
    usage = " ".join(x for _h, lines in views.help_usage("kanban") for x in lines)
    assert "◂N" in usage and "▸N" in usage and "L links" in usage and "⛓" not in usage
    line, _meaning = views.help_example("kanban")
    assert line.index("▸") < line.index("◂") < line.index("+4d") and "⛓" not in line


def test_TC_505_the_gutter_and_the_packet_read_the_same_rule():
    """TC-505 (LLR-501.3): an ARCHIVED predecessor is closed (no mark); a start
    ON the predecessor's due day is `over`, the day after is not (D-503); the
    flow packet stops for a waiting task and moves once its predecessor is done
    (D-519). RED on base: the archived arm (P-2) and the due-day arm."""
    b = kg_board.build()
    b.task_by_id("ta3").archived = True
    assert gantt_dep_mark(b.task_by_id("ta2"), b, set()) == " "
    b = kg_board.build()
    w5, w4 = b.task_by_id("tw5"), b.task_by_id("tw4")
    w4.due_date = w5.start_date
    assert gantt_dep_mark(w5, b, set()) == views.c("↳", "over")
    w4.due_date = (date.fromisoformat(w5.start_date) - timedelta(days=1)).isoformat()
    assert gantt_dep_mark(w5, b, set()) == views.c("↳", "mut")
    m3 = b.task_by_id("tm3")
    assert not views._flowing(b, m3)
    b.task_by_id("tm2").phase = "Done"
    assert views._flowing(b, m3)


def test_TC_506_ready_lines_are_capped_and_say_a_block_remains(tmp_path):
    """TC-506 (LLR-501.4, D-508): five waiters released at once → three lines and
    "+2 more ready"; a released waiter that is still blocked says so; a link
    removed by hand releases silently. RED: an uncapped flood; no suffix."""
    hub = Task("Hub", phase="Doing", id="H")
    ws = [Task(f"W{i}", phase="Backlog", depends_on=["H"], id=f"W{i}", blocked=(i == 0))
          for i in range(5)]
    b = Board([], [hub, *ws], tmp_path / "b.json", phases=["Backlog", "Doing", "Done"])
    before = waiting_ids(b)
    hub.phase = "Done"
    assert ready_messages(b, before, {"H"}) == [
        "W0 is ready — Hub done (still ▲ blocked)", "W1 is ready — Hub done",
        "W2 is ready — Hub done", "+2 more ready"]
    for w in ws[3:]:                                  # exactly three: no "+K" (F6)
        w.depends_on = []
    hub.phase = "Doing"
    before = waiting_ids(b)
    hub.phase = "Done"
    assert len(ready_messages(b, before, {"H"})) == 3
    hub.phase = "Doing"
    before = waiting_ids(b)
    ws[1].depends_on = []
    assert ready_messages(b, before, set()) == []


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


def _ready(app) -> list[str]:
    return [t.split("\n")[-1] for t in _toasts(app) if "is ready" in t]


async def test_TC_506_done_says_once_what_became_ready(tmp_path):
    """TC-506 (LLR-501.4): `]` on `Audit dependencies` (Doing → Review) says
    nothing; `]` again (→ Done) says once "Add push notifications is ready —
    Audit dependencies done"; `u` says nothing new; finishing `Build component
    library` names only `Optimize image assets`; the editor moving `Rate
    limiting` to Done says `SDK regeneration` is ready. RED: a toast on every
    `]`, or none."""
    path = tmp_path / "board.json"
    kg_board.shifted(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        app.clear_notifications()
        app.selected_task_id = "tm2"
        await pilot.press("]")
        await pilot.pause()
        assert _ready(app) == []
        await pilot.press("]")
        await pilot.pause()
        assert _ready(app) == ["Add push notifications is ready — Audit dependencies done"]
        # an undo that puts the predecessor BACK into Done releases the waiter
        # again, silently (D-508; code review F5: undoing a `]` cannot fail)
        await pilot.press("[")
        await pilot.pause()
        app.clear_notifications()
        await pilot.press("u")
        await pilot.pause()
        assert app.board.is_done(app.board.task_by_id("tm2"))
        assert _ready(app) == []
        app.selected_task_id = "tw2"
        await pilot.press("]")
        await pilot.pause()
        assert _ready(app) == ["Optimize image assets is ready — Build component library done"]
        app.clear_notifications()
        app._on_task_edited(app.board.task_by_id("ta4"), {"phase": "Done", "archived": False})
        await pilot.pause()
        assert _ready(app) == ["SDK regeneration is ready — Rate limiting done"]


def test_TC_517_the_refusal_names_who_waits(tmp_path):
    """TC-517 (LLR-504.1): the refusal for one, two and five waiters (three names,
    "and 2 more"), real plurals; None for a done predecessor, for a task whose
    waiters are all archived, for waiters inside what is being archived. RED on
    base: no guard (P-3)."""
    hub = Task("Hub", phase="Doing", id="H")
    ws = [Task(f"W{i}", phase="Backlog", depends_on=["H"], id=f"W{i}") for i in range(5)]
    b = Board([], [hub, ws[0]], tmp_path / "b.json", phases=["Backlog", "Doing", "Done"])
    assert archive_refusal(b, hub, "archive") == (
        "can't archive Hub — 1 open task waits on it (W0). "
        "Finish it, or remove the link in its details (↵, then x).")
    b.tasks.append(ws[1])
    assert archive_refusal(b, hub, "delete").startswith(
        "can't delete Hub — 2 open tasks wait on it (W0, W1).")
    b.tasks += ws[2:]
    assert "5 open tasks wait on it (W0, W1, W2 and 2 more)" in archive_refusal(b, hub, "archive")
    assert archive_refusal(b, hub, "archive", leaving={"H", *(w.id for w in ws)}) is None
    for w in ws:
        w.archived = True
    assert archive_refusal(b, hub, "archive") is None
    ws[0].archived = False
    hub.phase = "Done"
    assert archive_refusal(b, hub, "archive") is None


def test_TC_518_the_derivations_are_bounded_on_hostile_boards(tmp_path):
    """TC-518 (LLR-501.1, S-5): a chain of 5000 open tasks, one task holding
    100 000 ids, a dense 800-task board and a stored 2-cycle: `link_marks`,
    `waiting_ids`, `dependents_chain` and `loop_path` each return in < 1 s and
    none recurses. RED: `task_by_id` per link, or a recursive search."""
    chain = [Task(f"c{i}", phase="Doing", depends_on=[f"c{i - 1}"] if i else [], id=f"c{i}")
             for i in range(5000)]
    many = [Task("hub", phase="Doing", depends_on=[f"c{i % 5000}" for i in range(100_000)],
                 id="hub")]
    dense = [Task(f"d{i}", phase="Doing", id=f"d{i}",
                  depends_on=[f"d{j}" for j in range(800) if j != i][:400]) for i in range(800)]
    cyc = [Task("X", phase="Doing", depends_on=["Y"], id="X"),
           Task("Y", phase="Doing", depends_on=["X"], id="Y")]
    for tasks in (chain + many, dense, cyc):
        b = Board([], tasks, tmp_path / "h.json", phases=["Doing", "Done"])
        for fn in (lambda: link_marks(b), lambda: waiting_ids(b),
                   lambda: dependents_chain(b, tasks[0]),
                   lambda: loop_path(b, tasks[-1], tasks[0])):
            t0 = time.perf_counter()
            fn()
            assert time.perf_counter() - t0 < 1.0


def _painted(app) -> list[str]:
    return [s.text for s in app.screen._compositor.render_strips(app.screen.size)]


def _mark_tones(app) -> set[str]:
    """The painted foreground of every segment that starts with a mark glyph."""
    tones = set()
    for strip in app.screen._compositor.render_strips(app.screen.size):
        for seg in strip:
            if seg.text.strip()[:1] in ("◂", "▸") and seg.style is not None and seg.style.color:
                tones.add(seg.style.color.triplet.hex)
    return tones


async def test_AT_501_the_board_says_who_waits_and_b_is_an_outside_block(tmp_path):
    """AT-501 (US-501): on the kg board shifted to today, kanban at 118×40 (every
    band drawn, `p2-kanban-height.txt`), grouped: every open card is drawn (badges
    counted = open tasks); the painted values are the board's — `◂` 7 of 8 (the
    high-band `Deprecate v1 endpoints` keeps its project tag, A-3), `▸` 8 of 8;
    lanes (`tab tab`): all 8 `◂` — the age and `▸` shed before them under the
    title floor (D-529, D-533); never `⛓`; every mark painted in the muted tone.
    `b` opens nothing and keeps the links; `]` twice on `Audit dependencies` → one
    ready toast and `Add push notifications` loses its `◂`. RED on base: `⛓1` on
    the predecessor, nothing on the waiter (P-2); `b` opens the picker (P-1)."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    want = link_marks(b)
    n_open = sum(1 for t in b.tasks if is_open(b, t))
    assert Counter(w for w, _ in want.values() if w) == Counter({1: 7, 2: 1})
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        text = "\n".join(_painted(app)[:-2])
        assert sum(text.count(x) for x in ("!! ", "== ", "++ ")) == n_open
        assert Counter(int(x) for x in re.findall(r"◂(\d+)", text)) == Counter({1: 6, 2: 1})
        assert Counter(int(x) for x in re.findall(r"▸(\d+)", text)) == Counter({1: 7, 2: 1})
        assert "Deprecate v1" in text and "⛓" not in text
        # the one unpainted `◂` is the high-band card's (it keeps its tag, A-3)
        rows = text.splitlines()
        deprecate = [r for i, r in enumerate(rows)
                     if i and "Deprecate v1" in rows[i - 1] and "endpoints" in r]
        assert deprecate and "◂" not in deprecate[0] and "API" in deprecate[0]
        assert _mark_tones(app) == {HEX["mut"]}
        await pilot.press("tab", "tab")             # grouped → matrix → lanes
        await pilot.pause()
        assert app.kanban_presentation == "lanes"
        text = "\n".join(_painted(app)[:-2])
        # operator D-529 + D-533 "Dejar ◂ solo, quitar la edad antes": the title
        # keeps 6 cells, the age and `▸` shed first — every `◂` is painted
        assert Counter(int(x) for x in re.findall(r"◂(\d+)", text)) == Counter({1: 7, 2: 1})
        assert "⛓" not in text
        await pilot.press("tab")                    # back to grouped
        await pilot.pause()
        app.selected_task_id = "tm2"
        stored = list(app.board.task_by_id("tm2").depends_on)
        await pilot.press("b")
        await pilot.pause()
        assert len(app.screen_stack) == 1
        assert app.board.task_by_id("tm2").depends_on == stored
        assert app.board.task_by_id("tm2").blocked
        await pilot.press("b")
        app.clear_notifications()
        await pilot.press("]")
        await pilot.press("]")
        await pilot.pause()
        assert _ready(app) == ["Add push notifications is ready — Audit dependencies done"]
        rows = _painted(app)
        assert not any("Add push" in r and "◂" in r for r in rows)
        app.selected_task_id = "to3"                  # a further `]`: nothing ready
        app.clear_notifications()
        await pilot.press("]")
        await pilot.pause()
        assert _ready(app) == []


async def test_AT_505_work_others_wait_on_is_not_put_away(tmp_path):
    """AT-505 (US-504): `x`, `d` and the editor's archived box on `Partner notice
    emails` (open; `Deprecate v1 endpoints` waits on it) are refused naming the
    waiter — the task stays, no confirm opens, the file is unchanged but for the
    editor's other field, which is saved; a done predecessor archives; `X`
    archives done work even when a task links to it. RED on base: `x` archives,
    `d` deletes (P-3)."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.task_by_id("tm1").phase_changed = None             # unstamped done: X's work
    b.task_by_id("td5").depends_on.append("tm1")
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        raw = path.read_bytes()                   # after the start's own saves
        app.selected_task_id = "ta3"
        for key in ("x", "d"):
            app.clear_notifications()
            await pilot.press(key)
            await pilot.pause()
            assert len(app.screen_stack) == 1, key
            assert app.board.task_by_id("ta3") is not None
            assert not app.board.task_by_id("ta3").archived
            notes = [t for t in _toasts(app) if "can't" in t]
            assert len(notes) == 1 and "Deprecate v1 endpoints" in notes[0], key
        assert path.read_bytes() == raw
        app.clear_notifications()
        await pilot.press("e")
        await pilot.pause()
        app.screen.query_one("#f-title").value = "Partner notice emails v2"
        app.screen.query_one("#f-archived").value = True
        await pilot.click("#save")
        await pilot.pause()
        t = app.board.task_by_id("ta3")
        assert t.title == "Partner notice emails v2" and not t.archived
        assert any("other changes saved" in x for x in _toasts(app))
        app.selected_task_id = "tw1"                      # done; tw2 links to it
        await pilot.press("x")
        await pilot.pause()
        assert app.board.task_by_id("tw1").archived
        await pilot.press("X")
        await pilot.pause()
        await pilot.click("#yes")
        await pilot.pause()
        assert app.board.task_by_id("tm1").archived
        # the project archive (D-523, increment 003): `Deprecate v1 endpoints`
        # (API Platform) is made to wait on `Audit dependencies` (Mobile App);
        # archiving Mobile App is refused naming it, nothing is archived
        app.board.task_by_id("ta2").depends_on.append("tm2")
        app.board.save()
        app.clear_notifications()
        await pilot.press("P")
        await pilot.pause()
        await pilot.press("j", "x")
        await pilot.pause()
        assert len(app.screen_stack) == 2               # no confirm opened
        assert not app.board.project_by_id("pmob").archived
        assert not app.board.task_by_id("tm2").archived
        notes = [t for t in _toasts(app) if "can't archive this project" in t]
        assert len(notes) == 1 and "Deprecate v1 endpoints" in notes[0]
        await pilot.press("escape")
        await pilot.pause()


async def test_TC_517_delete_is_judged_again_after_its_confirm(tmp_path):
    """TC-517 (LLR-504.1, code review F4, security S-7): a waiter added while the
    delete confirm is open (a sync tick) refuses the delete at `yes`. RED: the
    guard checked only before the confirm."""
    path = tmp_path / "board.json"
    kg_board.shifted(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "to4"                  # nobody waits on it
        await pilot.press("d")
        await pilot.pause()
        assert len(app.screen_stack) == 2
        app.board.task_by_id("to5").depends_on.append("to4")   # arrives meanwhile
        await pilot.click("#yes")
        await pilot.pause()
        assert app.board.task_by_id("to4") is not None
        assert any("can't delete" in t for t in _toasts(app))


async def test_TC_517_x_in_setup_never_touches_a_task(tmp_path):
    """TC-517 (HLR-504, code review F2, security S-7; operator: "Corregir en el
    002"): `x` in the Setup view removes a setup row and nothing else — the task
    still selected on the board behind it (open, a task waits on it) is not
    archived, no task snapshot is pushed, no archive toast. RED on the frozen r1
    tree: the selected task was archived and saved before the setup removal."""
    path = tmp_path / "board.json"
    kg_board.shifted(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "ta3"                  # ta2 waits on it
        await pilot.press("0")
        await pilot.pause()
        assert app.view_mode == "setup"
        stack = len(app._undo_stack)
        app.clear_notifications()
        await pilot.press("x")
        await pilot.pause()
        assert not app.board.task_by_id("ta3").archived
        assert len(app._undo_stack) == stack
        assert not any("archived" in t or "can't" in t for t in _toasts(app))
    saved = {t["id"]: t for t in __import__("json").loads(path.read_text(encoding="utf-8"))["tasks"]}
    assert saved["ta3"]["archived"] is False


async def test_TC_517_the_refusal_paints_a_markup_title_literally(tmp_path):
    """TC-517 (LLR-504.1, S1; increment 002 code review R2-1): the refusal toast is
    built with markup OFF — a waiter titled `[b]x[/b]` and a predecessor titled
    `[@click=app.quit]q[/]` are painted as typed. RED: the toast's markup on (the
    tags vanish, or the click becomes an action)."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    b.task_by_id("ta2").title = "[b]x[/b]"
    b.task_by_id("ta3").title = "[@click=app.quit]q[/]"
    b.save()
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        app.selected_task_id = "ta3"
        app.clear_notifications()
        await pilot.press("x")
        await pilot.pause()
        notes = [t for t in _toasts(app) if "can't" in t]
        assert notes and "can't archive [@click=app.quit]q[/] — 1 open task waits on it ([b]x[/b])" in notes[0]


def test_TC_502_a_predecessor_off_the_board_closes_no_loop(tmp_path):
    """TC-502 (increment 002 code review F10 / R2-2): `loop_path` with a task that
    is not a board task returns None rather than raising."""
    b = kg_board.build()
    assert loop_path(b, b.task_by_id("tm2"), Task("stray", id="stray")) is None


async def test_TC_517_a_project_whose_waiters_are_inside_archives(tmp_path):
    """TC-517 (HLR-504 boundary, D-523; code review T4/F7, battery P8): a project
    whose open tasks are waited on only by its OWN tasks archives as before; a
    waiter that appears outside it while the confirm is open refuses the archive
    at `yes`. RED: inside waiters counted; the guard checked only before confirm."""
    path = tmp_path / "board.json"
    kg_board.shifted(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(118, 40), notifications=True) as pilot:
        await pilot.press("4")
        await pilot.pause()
        await pilot.press("P")
        await pilot.pause()
        await pilot.press("j", "j", "j", "x")        # Data Warehouse: d5 waits on d4, inside
        await pilot.pause()
        assert type(app.screen).__name__ == "ConfirmModal"
        await pilot.click("#yes")
        await pilot.pause()
        assert app.board.project_by_id("pdwh").archived
        assert app.board.task_by_id("td4").archived
        await pilot.press("j", "x")                  # Ops & Security: no waiter yet
        await pilot.pause()
        assert type(app.screen).__name__ == "ConfirmModal"
        app.board.task_by_id("tw5").depends_on.append("to2")   # arrives meanwhile
        await pilot.click("#yes")
        await pilot.pause()
        assert not app.board.project_by_id("pops").archived
        assert any("can't archive this project" in t and "Launch new homepage" in t
                   for t in _toasts(app))


@pytest.mark.parametrize("size", [(118, 30), (80, 24), (118, 40)])
async def test_TC_504_a_lanes_card_keeps_a_readable_title(tmp_path, size):
    """TC-504, operator D-529 "Corregirlo antes del push" (ux U-2): in lanes a
    card's title is never cut to nothing — `▸M ◂N` are shed first, then the other
    meta, before the title drops below 6 cells (5 characters and `…`: the
    readability measure counts a title only once its first word shows, and the
    kg board's median first word is 5 characters). Every card cell painted in
    lanes shows at least 5 characters of its title (or the whole title).
    RED: `▊ ==  ·7d ▸1 ◂1 +8d` — a card with no title (2 at 118×30 and 80×24).
    Operator D-533 (A-12): every painted waiting card keeps `◂N`; RED: the D-529
    order, which shed every mark at 118 and 80."""
    path = tmp_path / "board.json"
    b = kg_board.shifted(path)
    titles = [t.title for t in b.tasks]
    marks = link_marks(b)
    waiting_seen = 0
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=size) as pilot:
        await pilot.press("4")
        await pilot.press("tab", "tab")
        await pilot.pause()
        assert app.kanban_presentation == "lanes"
        cards = [cell for row in _painted(app)[:-2] for cell in row.split("│")
                 if cell.startswith("▊ ")]
        assert cards
        for cell in cards:
            body = re.sub(r"^▊ (!!|==|\+\+)? ?", "", cell)
            stub = body.split("…")[0] if "…" in body.split("  ")[0] else body.split("  ")[0]
            stub = re.split(r" [·▸◂↗▤!+\-]\S*", stub)[0].strip()
            assert (len(stub) >= 5 or stub in titles             # 5 characters, the whole
                    or stub in {t.split()[0] for t in titles}), (cell, stub)   # title or word
            # operator D-533 "Dejar ◂ solo, quitar la edad antes": a waiting card keeps
            # its `◂N` while its title keeps the floor — the age and `▸` go first
            owner = [t for t in b.tasks if t.title.startswith(stub)]
            if len(owner) == 1:
                waits = marks.get(owner[0].id, (0, 0))[0]
                if waits:
                    assert f"◂{waits}" in cell, (cell, waits)
                    waiting_seen += 1
                else:
                    assert "◂" not in cell, cell
        assert waiting_seen


def test_TC_504_the_lanes_floor_sheds_age_then_unblocks_and_keeps_waits():
    """TC-504, operator D-533 "Dejar ◂ solo, quitar la edad antes" (A-12): under the
    lanes' title floor the age `·Nd` goes FIRST, then `▸`, then the other meta;
    `◂` (waits on N open) stays as long as the title keeps its 6 cells. At no
    width does a lanes card keep its age after shedding a mark, keep `▸` without
    `◂`, or keep any token at all without `◂`; the title never shows fewer than 5
    characters (or a whole first word). Other callers keep the shipped law.
    RED: the D-529 order (marks shed before the age)."""
    b = kg_board.build()
    t = b.task_by_id("tm3")                              # ▸1 ◂1, aged, dated
    from rich.text import Text as _T
    seen = set()
    for wc in range(8, 40):
        plain = _T.from_markup(views.card_cell(t, b, wc, False, prefix="▊ ", badge=True,
                                                today=kg_board.TODAY,
                                                title_floor=views.CARD_TITLE_FLOOR)).plain
        assert len(plain) == wc
        title = plain[5:].split(" ·")[0].split(" ▸")[0].split(" ◂")[0].split(" +")[0]
        stub = title.rstrip("…").strip()
        assert stub == "Add" or len(stub) >= min(5, wc - 6), (wc, plain)   # a whole word or 5
        age, up, wait = "·" in plain, "▸" in plain, "◂" in plain
        other = bool(re.search(r" [+\-]\d+d", plain))
        assert not (age and not (up and wait)), (wc, plain)    # the age goes first
        assert not (up and not wait), (wc, plain)              # then `▸`, `◂` kept
        assert not (other and not wait), (wc, plain)           # `◂` outlives other meta
        seen.add((age, up, wait, other))
    assert (False, False, True, False) in seen and (True, True, True, True) in seen
    shipped = _T.from_markup(views.card_cell(t, b, 16, False, prefix="▊ ", badge=True,
                                             today=kg_board.TODAY)).plain
    assert "◂1" in shipped, shipped                       # no floor: the shipped law keeps it

async def test_TC_504_wide_lanes_still_paint_every_mark(tmp_path):
    """TC-504, code review 006 M2, operator D-533: under the title floor the lanes
    shed the age, then `▸`, keeping `◂` (at 118 every waiting card keeps `◂`, no
    `▸`); at 160×40 there is room for all, and lanes paint the board's exact
    values — `◂` 7×1 + 1×2, `▸` 7×1 + 1×2. RED: a floor that sheds the marks
    everywhere."""
    path = tmp_path / "board.json"
    kg_board.shifted(path)
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(160, 40)) as pilot:
        await pilot.press("4")
        await pilot.press("tab", "tab")
        await pilot.pause()
        assert app.kanban_presentation == "lanes"
        text = "\n".join(_painted(app)[:-2])
        assert Counter(int(x) for x in re.findall(r"◂(\d+)", text)) == Counter({1: 7, 2: 1})
        assert Counter(int(x) for x in re.findall(r"▸(\d+)", text)) == Counter({1: 7, 2: 1})

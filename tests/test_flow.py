"""Gantt flow current: an in-progress task's bar carries a bright packet that
drifts toward the due date, one cell per tick. Backlog/done/blocked bars stay
static, so on-bar motion always means 'this is being worked on right now'."""
import io
import tempfile
from datetime import date, timedelta
from pathlib import Path

from rich.console import Console

from taskboard.models import Board, Project, Task
from taskboard import views

TODAY = date(2026, 7, 24)


def _styled(text) -> str:
    """Render a Text to ANSI so colour changes (the packet) are visible — plain
    str() would hide them, since the packet is a recolour, not a glyph swap."""
    con = Console(file=io.StringIO(), color_system="truecolor", width=100)
    con.print(text)
    return con.file.getvalue()


def _board(tasks) -> Board:
    p = Project(name="GRNDIA", color="amber", id="p1",
                start_date=(TODAY - timedelta(days=3)).isoformat(),
                due_date=(TODAY + timedelta(days=21)).isoformat())
    return Board([p], tasks, Path(tempfile.mkdtemp()) / "b.json",
                 phases=["Backlog", "Doing", "Done"])


def _doing() -> Task:
    return Task(title="shipping", project_id="p1", phase="Doing", id="t1",
                start_date=(TODAY - timedelta(days=2)).isoformat(),
                due_date=(TODAY + timedelta(days=16)).isoformat())


def _backlog() -> Task:
    return Task(title="later", project_id="p1", phase="Backlog", id="t2",
                start_date=TODAY.isoformat(),
                due_date=(TODAY + timedelta(days=14)).isoformat())


def test_flowing_is_in_progress_only():
    """The packet is gated on being genuinely in progress — not backlog, done,
    or blocked. If this predicate drifts, backlog bars would twitch and the
    motion would stop meaning anything."""
    b = _board([])
    assert views._flowing(b, _doing()) is True
    assert views._flowing(b, _backlog()) is False
    blocked = _doing(); blocked.blocked = True
    assert views._flowing(b, blocked) is False
    done = _doing(); done.phase = "Done"
    assert views._flowing(b, done) is False


def test_packet_moves_as_the_tick_advances():
    """Flow only means something if it MOVES — the render must change across
    ticks for an in-progress task."""
    b = _board([_doing()])
    frames = {_styled(views.render_gantt(b, False, "t1", today=TODAY, width=80, tick=k))
              for k in range(6)}
    assert len(frames) > 1                       # the packet drifts, not frozen


def test_backlog_bar_is_static_across_ticks():
    """A not-started task must not animate, or on-bar motion would stop being a
    reliable 'in progress' signal."""
    b = _board([_backlog()])
    a = _styled(views.render_gantt(b, False, "t2", today=TODAY, width=80, tick=0))
    z = _styled(views.render_gantt(b, False, "t2", today=TODAY, width=80, tick=7))
    assert a == z


def test_flow_preserves_gantt_row_width():
    """The packet is overlaid in place, so every gantt row keeps one exact width
    (an off-by-one here would ripple the whole chart)."""
    b = _board([_doing()])
    for tick in (0, 3, 5):
        text = views.render_gantt(b, False, "t1", today=TODAY, width=80, tick=tick)
        rows = [ln for ln in str(text).split("\n") if ln.strip()]
        assert len({len(ln) for ln in rows}) == 1


def test_render_view_threads_tick_to_gantt():
    """The public entry point must carry the tick through, or the app's per-second
    repaint would render a frozen packet."""
    b = _board([_doing()])
    a = _styled(views.render_view("gantt", b, False, "t1", today=TODAY, width=80, tick=0))
    z = _styled(views.render_view("gantt", b, False, "t1", today=TODAY, width=80, tick=1))
    assert a != z

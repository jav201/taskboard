"""The ambient — a surface kept open all day needs a sign of life.

AUDIT.md §7 found the lanes view "not merely still, it is inert": no interval
touched it, so nothing on screen ever moved. Now the today rule breathes.

The laws are about RESTRAINT, and they are the reason this is three glyphs and
not an animation: the cycle must be slow enough to read as breathing rather
than as a fault, nothing but the rule may move, and no colour may change at all.
"""

from datetime import date, timedelta

from taskboard.app import TICK_SECONDS      # the app's ONE shared clock, READ not assumed
from taskboard.models import Board, Project, Task
from taskboard.views import RULE_PHASES, lane_geometry, render_view

TODAY = date(2026, 7, 30)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def busy(tmp_path):
    b = Board.load(str(tmp_path / "motion.json"))
    b.projects.clear()
    b.tasks.clear()
    for i, (name, hue) in enumerate((("Atlas", "lime"), ("Beacon", "sky"),
                                     ("Cinder", "violet"))):
        p = Project(name, hue, "on_track", due_date=iso(10 + i * 9))
        b.projects.append(p)
        b.tasks += [Task(f"{name} work {k}", p.id, ["Backlog", "Doing"][k % 2],
                         "normal", due_date=iso(k * 5 - 8 + i))
                    for k in range(3)]
    return b


def frame(b, tick, w=96, h=30):
    return str(render_view("swimlanes", b, False, None, TODAY,
                           width=w, height=h, tick=tick)).split("\n")


def styles(b, tick, w=96, h=30):
    text = render_view("swimlanes", b, False, None, TODAY, width=w, height=h, tick=tick)
    return sorted(str(s.style) for s in text.spans)


# --------------------------------------------------------------------------- #
# the regime
# --------------------------------------------------------------------------- #
def test_the_cycle_is_slow_enough_to_read_as_breathing():
    """Two regimes exist and the band between them is illegal: an ambient cycle
    must clear 2 s, or it reads as a fault flashing at the reader rather than as
    a surface that is alive."""
    cycle_ms = len(RULE_PHASES) * TICK_SECONDS * 1000
    assert cycle_ms >= 2000, f"{cycle_ms} ms is inside the 400-2000 ms band"


def test_the_cycle_closes(tmp_path):
    b = busy(tmp_path)
    assert frame(b, 0) == frame(b, len(RULE_PHASES))
    assert frame(b, 1) == frame(b, len(RULE_PHASES) + 1)


def test_every_phase_glyph_is_one_cell(tmp_path):
    """A phase that changed the glyph's WIDTH would move every cell after it."""
    assert all(len(g) == 1 for g in RULE_PHASES)
    b = busy(tmp_path)
    for tick in range(len(RULE_PHASES)):
        assert all(len(line) == 96 for line in frame(b, tick))


# --------------------------------------------------------------------------- #
# restraint
# --------------------------------------------------------------------------- #
def test_nothing_but_the_rule_moves_between_phases(tmp_path):
    """The whole law of this increment. If any other cell changed, the reader's
    eye would be pulled to the wrong thing every second."""
    b = busy(tmp_path)
    geo = lane_geometry(94, 30)
    rule_col = geo.label_w + geo.today_dc // 2
    base = frame(b, 0)
    moved_at_least_once = False
    for tick in range(1, len(RULE_PHASES) * 2):
        other = frame(b, tick)
        assert len(base) == len(other)
        for r, (a, bl) in enumerate(zip(base, other)):
            for col, (ca, cb) in enumerate(zip(a, bl)):
                if ca != cb:
                    assert col == rule_col, \
                        f"tick {tick}: cell ({r},{col}) changed — only the rule may"
                    assert ca in RULE_PHASES and cb in RULE_PHASES
                    moved_at_least_once = True
    assert moved_at_least_once, "vacuous: nothing moved at all"


def test_no_colour_changes_between_phases(tmp_path):
    """The ambient lives in the GLYPH. A hue that pulsed would be a second
    variable riding on time, and time already has the rule."""
    b = busy(tmp_path)
    base = styles(b, 0)
    for tick in range(1, len(RULE_PHASES) * 2):
        assert styles(b, tick) == base, f"tick {tick} repainted something"


def test_the_other_views_do_not_breathe(tmp_path):
    """Only the lanes view gained an ambient. Kanban/columns/agenda are still,
    and the gantt keeps the flow packet it already had."""
    b = busy(tmp_path)
    for mode in ("agenda", "kanban"):
        a = str(render_view(mode, b, False, None, TODAY, width=96, height=30, tick=0))
        z = str(render_view(mode, b, False, None, TODAY, width=96, height=30, tick=3))
        assert a == z, f"{mode} changed with the tick"


def test_the_rule_still_breathes_at_the_narrow_step(tmp_path):
    b = busy(tmp_path)
    seen = {line[c] for tick in range(len(RULE_PHASES))
            for line in frame(b, tick, 40, 20)
            for c in range(len(line))} & set(RULE_PHASES)
    assert len(seen) >= 2

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
from taskboard import views as V
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


# --------------------------------------------------------------------------- #
# the gantt's flow packet — the OTHER thing that moves, and it shares the clock
# --------------------------------------------------------------------------- #
def gframe(b, tick, w=96, h=30):
    return str(render_view("gantt", b, False, None, TODAY,
                           width=w, height=h, tick=tick)).split("\n")


def packets(lines):
    """(row, column) of every flow packet on screen."""
    return [(r, c) for r, line in enumerate(lines)
            for c, ch in enumerate(line) if ch == "▬"]


def long_reach(tmp_path):
    """ONE task with a LONG span, in progress. The reach has to be long for the
    speed to be observable at all: over a two-cell reach, a packet stepping 3
    cells per tick and one stepping 1 land on the same cells every time (3t mod 2
    == t mod 2), so a short fixture cannot tell a detached clock from the shared
    one — it reports green while the animation runs at any speed it likes."""
    b = Board.load(str(tmp_path / "reach.json"))
    b.projects.clear()
    b.tasks.clear()
    p = Project("Atlas", "lime", "on_track", start_date=iso(-30), due_date=iso(30))
    b.projects.append(p)
    b.tasks.append(Task("A long haul", p.id, "Doing", "normal",
                        start_date=iso(-28), due_date=iso(28)))
    return b


def test_the_gantt_flow_rides_the_ONE_shared_clock(tmp_path):
    """The lanes view breathes and the gantt flows, and BOTH are driven by the
    app's single interval — the packet advances exactly ONE cell per tick. That
    is what makes `TICK_SECONDS` the one number governing every moving thing on
    screen: change it and both regimes change together. A packet that advanced
    by two, or by a private constant, would have detached from the clock while
    still looking animated, and nothing would have caught it."""
    b = long_reach(tmp_path)
    a, nxt = packets(gframe(b, 0)), packets(gframe(b, 1))
    assert a, "fixture must actually draw a flow packet to be a test"
    assert len(a) == len(nxt), (a, nxt)
    for (r0, c0), (r1, c1) in zip(a, nxt):
        assert r0 == r1, f"a packet changed ROW between ticks: {r0} -> {r1}"
        assert c1 - c0 in (1, 0) or c1 < c0, f"packet jumped {c0} -> {c1}"
    moved = [c1 - c0 for (_r, c0), (_r1, c1) in zip(a, nxt) if c1 > c0]
    assert moved, "no packet moved at all between two ticks"
    assert set(moved) == {1}, f"a packet advanced by {set(moved)} cells per tick"
    # and over a long run, so a multiplier cannot hide inside a short wrap
    cols = [packets(gframe(b, t))[0][1] for t in range(10)]
    steps = {cols[i + 1] - cols[i] for i in range(len(cols) - 1)}
    assert steps == {1}, f"across ten ticks the packet stepped {steps}, not one cell"


def test_the_flow_packet_is_never_faster_than_the_illegal_band(tmp_path):
    """The same restraint law the today rule answers to, applied to the packet:
    its perceptual cycle is the time to cross its own reach and wrap, so a SHORT
    reach is what would make it strobe. A one-cell reach is static (nothing to
    cross); every longer one must clear 2 s at the shared clock, or it flashes at
    the reader instead of reading as work in motion."""
    b = long_reach(tmp_path)
    seen = set()
    for tick in range(12):
        for _row, col in packets(gframe(b, tick)):
            seen.add(col)
    # the packet visits >1 column, so it is genuinely moving and its wrap period
    # is at least that many ticks
    assert len(seen) > 1, "the packet never moved; this law would be vacuous"
    cycle_ms = len(seen) * TICK_SECONDS * 1000
    assert cycle_ms >= 2000, (
        f"the flow packet wraps every {cycle_ms} ms, inside the 400-2000 ms band")


# --------------------------------------------------------------------------- #
# the project pulse — a SECOND motion in the gantt, and the reason it is allowed
# --------------------------------------------------------------------------- #
# The laws above were written when the flow packet was the only thing moving
# here, and `test_the_other_views_do_not_breathe` still names only agenda and
# kanban precisely because the gantt was already excluded. On 2026-08-07 the
# project's progress mark became a circle on the span and the operator asked for
# it to be the animated element.
#
# Admitting a second motion is a real widening of the restraint law, so it is
# paid for rather than waved through: the pulse rides the SAME clock, obeys the
# SAME 2 s floor, changes NO colour, and — the part that is new — is RATIONED.
# It runs only where the work is behind its calendar, so a board with nothing
# behind it is exactly as still as it was before this change. That last property
# is what makes this a channel rather than an ambient, and it is the one a lazy
# implementation would drop, so it is tested from both sides.
def behind_and_on_time(tmp_path):
    """One project clearly BEHIND (a long span, almost nothing done) and one
    clearly ahead of its calendar (span nearly over, everything done)."""
    b = Board.load(str(tmp_path / "pulse.json"))
    b.projects.clear()
    b.tasks.clear()
    late = Project("Late", "rose", "on_track", start_date=iso(-30), due_date=iso(30))
    ok = Project("Onsched", "lime", "on_track", start_date=iso(-30), due_date=iso(30))
    b.projects += [late, ok]
    # `project_progress` is done-tasks / all-tasks, so the two are built to sit
    # on opposite sides of the elapsed line rather than asserted to be there.
    b.tasks += [Task(f"late {k}", late.id, "Backlog", due_date=iso(5))
                for k in range(4)]
    b.tasks += [Task(f"ok {k}", ok.id, "Done", due_date=iso(5)) for k in range(4)]
    return b


def pulse_counts(b, tick, w=96, h=30):
    """How many of each pulse phase are on screen at `tick`.

    Reads `V.PULSE_PHASES` through the module rather than importing the tuple,
    so a test may substitute a distinguishable alphabet and still be counting
    what the renderer actually drew."""
    plain = str(render_view("gantt", b, False, None, TODAY, width=w, height=h,
                            tick=tick))
    return {g: plain.count(g) for g in dict.fromkeys(V.PULSE_PHASES)}


def test_the_pulse_runs_only_where_the_work_is_behind(tmp_path):
    """THE RATION, first half. Two projects, one behind: exactly one circle may
    leave the resting glyph on any tick."""
    from taskboard.views import PROGRESS_DOT, PULSE_PHASES
    b = behind_and_on_time(tmp_path)
    moved = set()
    for tick in range(len(PULSE_PHASES)):
        counts = pulse_counts(b, tick)
        breathing = sum(n for g, n in counts.items() if g != PROGRESS_DOT)
        assert breathing <= 1, (tick, counts)
        moved |= {g for g, n in counts.items() if n and g != PROGRESS_DOT}
    assert moved, "nothing ever breathed; the ration swallowed the pulse itself"


def test_a_board_with_nothing_behind_is_completely_still(tmp_path):
    """THE RATION, second half, and the one a lazy implementation drops. Without
    it the pulse is an ambient wearing a condition, and 'rationed' would be a
    claim no test could refute."""
    b = behind_and_on_time(tmp_path)
    b.projects = [p for p in b.projects if p.name == "Onsched"]
    b.tasks = [t for t in b.tasks if t.project_id == b.projects[0].id]
    base = str(render_view("gantt", b, False, None, TODAY, width=96, height=30,
                           tick=0))
    assert "●" in base, "fixture draws no progress dot; this law would be vacuous"
    for tick in range(1, 8):
        assert str(render_view("gantt", b, False, None, TODAY, width=96,
                               height=30, tick=tick)) == base, (
            f"tick {tick} moved something on a board with nothing behind")


def test_the_pulse_rides_the_ONE_shared_clock_and_clears_the_floor(tmp_path, monkeypatch):
    """Same two properties the rule and the packet answer to. A private
    constant, or a cycle inside the 400-2000 ms band, would look animated and
    be wrong in the same invisible way."""
    from taskboard.views import PULSE_PHASES
    cycle_ms = len(PULSE_PHASES) * TICK_SECONDS * 1000
    assert cycle_ms >= 2000, f"{cycle_ms} ms is inside the illegal band"
    # ONLY the behind project, because `PULSE_PHASES[0]` IS the resting glyph:
    # with an on-time project on screen its permanent `●` is indistinguishable
    # from the pulsing one at phase 0, and "which phase is showing" stops being
    # a question the screen can answer.
    b = behind_and_on_time(tmp_path)
    b.projects = [p for p in b.projects if p.name == "Late"]
    b.tasks = [t for t in b.tasks if t.project_id == b.projects[0].id]

    def phase_at(tick):
        """Which phase of the cycle is on screen at `tick`."""
        counts = pulse_counts(b, tick)
        on = [g for g, n in counts.items() if n]
        assert len(on) == 1, (tick, counts)
        return on[0]

    # ONE PHASE PER TICK, and it must be tested through an alphabet where every
    # phase is DISTINGUISHABLE.
    #
    # Asserting the walk against the shipped glyphs does not work, and finding
    # out why is the point of this comment. `PULSE_PHASES` is a palindrome —
    # `●◉◎◉`, phases 1 and 3 are the same glyph — because that is what makes it
    # read as a breath rising and falling rather than a sawtooth. `tick * 3`
    # against four phases permutes {0,1,2,3} to {0,3,2,1}, and through a
    # palindrome that produces the IDENTICAL sequence on screen. A detached
    # multiplier therefore looked animated, walked "correctly", and survived the
    # mutation harness. The very symmetry that makes the motion good is what
    # blinds the observable to it.
    #
    # So the arithmetic is exercised with four distinct marks. The law is about
    # the mapping from tick to phase, not about which glyphs occupy it.
    # NOT digits, which was the first attempt and was wrong: the view is full of
    # numerals (`50%`, `25d`, `-46d`), so counting `"1"` counted the axis. Four
    # width-1 marks that appear nowhere else in a rendered gantt.
    distinct = ("⬒", "⬓", "⬔", "⬕")
    monkeypatch.setattr(V, "PULSE_PHASES", distinct)
    walk = [phase_at(t) for t in range(len(distinct) * 2 + 1)]
    expected = [distinct[t % len(distinct)] for t in range(len(walk))]
    assert walk == expected, f"the pulse walked {walk}, not one phase per tick"


def test_the_pulse_changes_no_colour(tmp_path):
    """The ambient lives in the GLYPH here too. A hue riding time would be a
    second variable on the same axis, and this view already spends time on the
    rule and the packet."""
    b = behind_and_on_time(tmp_path)
    def styles(tick):
        text = render_view("gantt", b, False, None, TODAY, width=96, height=30,
                           tick=tick)
        return sorted(str(s.style) for s in text.spans)
    base = styles(0)
    for tick in range(1, 8):
        assert styles(tick) == base, f"tick {tick} repainted something"

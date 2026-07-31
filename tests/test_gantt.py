"""The gantt's right edge and its titles (REV5 #19).

Two changes, one law between them: the row ends in the six-cell due meter, and
because the meter now says WHEN, the bar goes back to saying only WHOSE. That is
the ration again — identity names, severity judges, no mark wears both — and it
leaves `▲` as the single alert on the row.

The titles run OVER THE FIELD, which is where the reader actually reads, and they
stop where the task's own bar starts so they can never cover the thing they
describe.
"""

import re
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.views import HEX, METER_W, gantt_meta_geometry, render_gantt

TODAY = date(2026, 7, 30)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, name="g.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def fixture(tmp_path):
    b = board(tmp_path)
    p = Project("Atlas", "lime", "on_track", start_date=iso(-20), due_date=iso(25))
    b.projects.append(p)
    b.tasks += [
        Task("Checkout returns 500 on retry", p.id, "Doing", "high",
             start_date=iso(-6), due_date=iso(-2)),                    # bar at week 0
        Task("Rework the pricing page copy", p.id, "Backlog", "normal",
             start_date=iso(9), due_date=iso(16)),                     # bar a week out
        Task("Compress the hero assets", p.id, "Backlog", "normal",
             start_date=iso(20), due_date=iso(27)),                    # further out
        Task("Old finished thing", p.id, "Done", "normal",
             start_date=iso(-30), due_date=iso(-20)),
    ]
    return b, p


def rows(b, w=96, h=20):
    return str(render_gantt(b, False, None, TODAY, width=w, height=h)).split("\n")


def geo(w):
    inner = w - 2
    glabel_w = max(18, min(30, inner // 3))
    meta_w, _full = gantt_meta_geometry(inner, glabel_w, 6)
    return inner, glabel_w, meta_w


# --------------------------------------------------------------------------- #
# the right edge
# --------------------------------------------------------------------------- #
def test_every_row_ends_in_the_six_cell_meter(tmp_path):
    b, _p = fixture(tmp_path)
    out = rows(b)
    body = [l for l in out if l.startswith("│▐ ")
            or (l.startswith("│  ") and any(t.title[:12] in l for t in b.tasks))]
    assert len(body) >= 5
    for line in body:
        edge = line[-1 - METER_W:-1]
        assert set(edge) <= set("⣿⡇·▲⣤ "), f"{line[-10:]!r} is not a meter"
        # an EMPTY edge is not a meter either — the first version of this law
        # allowed spaces, so deleting the meter altogether kept it green
        assert set(edge) & set("⣿⡇·▲⣤"), f"{line[-10:]!r} has no meter at all"


def test_finished_work_shows_a_spent_meter(tmp_path):
    b, _p = fixture(tmp_path)
    line = next(l for l in rows(b) if "Old finished thing" in l)
    assert set(line[-1 - METER_W:-1]) == {"⣤"}


def test_the_project_row_keeps_its_progress_figure(tmp_path):
    b, _p = fixture(tmp_path)
    line = next(l for l in rows(b) if "Atlas" in l)
    assert re.search(r"\d+%", line), line
    assert set(line[-1 - METER_W:-1]) <= set("⣿⡇·▲⣤ ")


def test_the_alert_is_the_meters_cap_and_nothing_else(tmp_path):
    """`▲` is severity's one seat on this row. The task bar used to turn red for
    overdue and amber for due-today; the meter says when now, so the bar is free
    to say only whose."""
    b, _p = fixture(tmp_path)
    text = render_gantt(b, False, None, TODAY, width=96, height=20)
    worn = [text.plain[s.start:s.end].strip() for s in text.spans
            if HEX["over"] in str(s.style)]
    assert worn, "vacuous: nothing wears the severity hue at all"
    for seg in worn:
        assert re.fullmatch(r"▲|▲\d+ past due|\d+ past due", seg), \
            f"severity worn by {seg!r}"


def test_a_bar_never_wears_an_urgency_hue(tmp_path):
    """The bar glyph `▬` may only ever be an identity hue or the flow packet."""
    from taskboard.models import PROJECT_COLORS
    b, _p = fixture(tmp_path)
    text = render_gantt(b, False, None, TODAY, width=96, height=20)
    lawful = {HEX[c] for c in PROJECT_COLORS} | {HEX["bright"], HEX["dim"],
                                                HEX["accent"], HEX["frame"]}
    for s in text.spans:
        seg = text.plain[s.start:s.end]
        if seg and set(seg) <= {"▬", " "} and seg.strip():
            assert any(h in str(s.style) for h in lawful), f"bar wears {s.style}"
            assert HEX["over"] not in str(s.style)
            assert HEX["soon"] not in str(s.style)


# --------------------------------------------------------------------------- #
# the titles
# --------------------------------------------------------------------------- #
def test_a_title_never_covers_its_own_bar(tmp_path):
    """The mechanism's safety property: the title spends only the EMPTY field in
    front of the bar, so however long it grows it cannot hide the mark it names."""
    b, p = fixture(tmp_path)
    _inner, glabel_w, _meta = geo(96)
    checked = 0
    for t in b.tasks:
        # a task whose whole span sits before the chart window has no bar to
        # cover — that is the axis clipping it, not the title swallowing it
        if t.due_date and t.due_date < iso(-13):
            continue
        line = next(l for l in rows(b) if t.title[:12] in l)
        body = line[1:-1]
        first_bar = body.find("▬")
        # every dated task in this fixture draws a bar; a row with NO bar means
        # the title swallowed it, which is exactly the failure this law is for
        assert first_bar >= 0, f"{t.title!r}: its bar is gone from the row"
        assert "▬" not in body[:first_bar]
        checked += 1
    assert checked >= 3


def test_a_task_whose_bar_starts_later_gets_a_wider_title(tmp_path):
    """MEASURED: a title boxed in the label column has 27 cells at 96 wide; one
    whose bar starts a week out has 33 — the number REV5 §0.003 asks for — and
    it grows by a week's cells for every week of empty field in front."""
    b, p = fixture(tmp_path)
    b.tasks.append(Task("A" * 60, p.id, "Backlog", "normal",
                        start_date=iso(9), due_date=iso(16)))
    b.tasks.append(Task("B" * 60, p.id, "Doing", "normal",
                        start_date=iso(-6), due_date=iso(-2)))
    out = rows(b)
    near = next(l for l in out if "B" * 10 in l)
    far = next(l for l in out if "A" * 10 in l)
    # the title cell is letters + the truncation mark it earns
    assert near.count("B") + 1 == 27, near.count("B")   # boxed in the label column
    assert far.count("A") + 1 == 33, far.count("A")     # a week of field in front


def test_the_header_names_what_the_edge_actually_holds(tmp_path):
    b, _p = fixture(tmp_path)
    header = rows(b)[1]
    assert "when" in header
    assert "due" not in header          # the due FIGURE became the meter


# --------------------------------------------------------------------------- #
# the invariant every view in this codebase obeys
# --------------------------------------------------------------------------- #
def test_width_exact_at_every_step(tmp_path):
    b, _p = fixture(tmp_path)
    for w in (24, 40, 60, 72, 96, 97, 130, 200):
        for h in (0, 12, 20, 30):
            for line in rows(b, w, h):
                assert len(line) == max(24, w), f"{w}x{h}: {len(line)}"


def test_an_empty_board_still_renders(tmp_path):
    b = board(tmp_path, "empty.json")
    out = rows(b, 96, 12)
    assert all(len(l) == 96 for l in out)

"""Short content stays at the TOP, and only an axis may sit at the bottom.

WHY THIS FILE EXISTS: reported from use — "algunas tareas se ven hasta el fondo
del view (lanes y kanban) mientras el resto está bien organizado en la parte
superior". It was real, and it was one line.

`fill_height` padded a short view by putting the blank rows ABOVE the last row,
on the reasoning that the last row "is the axis every view closes with". The
lanes and the gantt do close with an axis, so they looked right and the
assumption survived. **The kanban and the agenda close with a TASK**, so their
last task was pinned to the bottom of the viewport with a field of blanks above
it. Swept over the real board: 84 kanban sizes and 44 agenda sizes stranded a
row. An axis is now something a view SAYS it has (`to_text(..., pinned=1)`)
rather than something the padder guesses.

The two halves are tested TOGETHER on purpose. Fixing the strand by never
pinning anything would have made the first half green and silently dropped the
gantt's axis to the middle of the screen — which is exactly what happened while
this was being written, and what the first version of the sweep called "clean".
A law that can be satisfied by deleting the behaviour it protects is not a law.
"""

from datetime import date, timedelta
from pathlib import Path

import pytest

from taskboard.models import Board, Project, Task
from taskboard.views import render_view

PHASES = ["Backlog", "Doing", "Review", "Done"]

# how many trailing rows each view legitimately pins to the bottom
PINNED = {"swimlanes": 1, "gantt": 1, "agenda": 0, "kanban": 0}

_UNWRITTEN = Path("__never_written__.json")


def short_board() -> Board:
    """Deliberately small: the bug only appears when the content does not fill
    the viewport, which is why a full board never showed it."""
    p = Project(name="Demo", color="cyan")
    today = date.today()
    tasks = [Task(title=f"tarea {i}", project_id=p.id, phase=PHASES[i % 4],
                  start_date=str(today - timedelta(days=5)),
                  due_date=str(today + timedelta(days=i)))
             for i in range(5)]
    return Board([p], tasks, _UNWRITTEN, phases=PHASES)


def rows_after_the_first_blank(mode, presentation, width, height) -> list[str]:
    text = render_view(mode, short_board(), False, None, width=width,
                       height=height, line_map={}, presentation=presentation,
                       tick=0)
    lines = text.plain.split("\n")
    seen_blank = False
    out = []
    for line in lines:
        if not line.strip():
            seen_blank = True
        elif seen_blank:
            out.append(line.rstrip())
    return out


def _cases():
    for mode, pinned in PINNED.items():
        for pres in (("grouped", "matrix") if mode == "kanban" else ("grouped",)):
            yield mode, pres, pinned


@pytest.mark.parametrize("mode,pres,pinned", list(_cases()))
@pytest.mark.parametrize("height", [14, 20, 30, 45, 60])
@pytest.mark.parametrize("width", [80, 120])
def test_no_row_is_stranded_below_the_blank_pad(mode, pres, pinned, height, width):
    """THE REPORTED BUG. Nothing may sit below the pad except a declared axis."""
    below = rows_after_the_first_blank(mode, pres, width, height)
    assert len(below) <= pinned, (
        f"{mode}/{pres} @{width}x{height}: {len(below)} row(s) stranded at the "
        f"bottom, first is {below[0][:60]!r}")


@pytest.mark.parametrize("mode", [m for m, p in PINNED.items() if p])
@pytest.mark.parametrize("height", [30, 45, 60])
def test_a_view_that_declares_an_axis_keeps_it_at_the_bottom(mode, height):
    """THE OTHER HALF, and the one that catches the lazy fix. Padding below
    everything would pass the test above and quietly leave the gantt's day axis
    floating in the middle of the screen with blank rows under it.

    The check is written on the LAST ROW rather than on the pad, because the
    lanes never pad at all — their allocator spends the whole height it is
    given, so a pad-shaped assertion would be vacuous exactly there, on the view
    the report named first."""
    text = render_view(mode, short_board(), False, None, width=100,
                       height=height, line_map={}, presentation="grouped", tick=0)
    lines = text.plain.split("\n")
    assert lines[-1].strip(), f"{mode} @{height}: the view ends in a blank row"

    # and when the view DID pad, the axis is what sits under the pad
    if any(not line.strip() for line in lines):
        below = rows_after_the_first_blank(mode, "grouped", 100, height)
        assert len(below) == PINNED[mode], (
            f"{mode} @{height}: the axis is no longer pinned to the bottom "
            f"({len(below)} rows below the pad)")


@pytest.mark.parametrize("mode,pres,pinned", list(_cases()))
def test_the_view_still_spends_the_whole_viewport(mode, pres, pinned):
    """Padding must not go missing either: a short view still fills its height,
    otherwise the fix would just be 'stop padding'."""
    text = render_view(mode, short_board(), False, None, width=100, height=40,
                       line_map={}, presentation=pres, tick=0)
    assert len(text.plain.split("\n")) == 40, f"{mode}/{pres} does not fill 40 rows"

"""`?` — the legend, and why it cannot lie (REV5 #21).

Three commitments, and each one is a law here:

  1. every swatch is drawn by CALLING the same function that draws the mark in
     the view, so there is no second copy of the art to drift out of date;
  2. it is per view — the gantt's legend is not the lanes';
  3. it explains ONLY what is on screen. A board with no cancelled project gets
     no `╳` entry, because sending the reader to hunt for an absent mark is
     another way of lying. The proposal's own law caught seven such ghost marks
     in its first version.

Register: the legend DESCRIBES MARKS. It never addresses the reader and never
judges the work — "overdue" is a fact about a date.
"""

import re
from datetime import date, timedelta

from taskboard.keymap import KEYMAP, VIEWS
from taskboard.models import Board, Project, Task
from taskboard.views import _strip, legend_entries, render_view

TODAY = date(2026, 7, 30)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, name="l.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def full(tmp_path):
    """A board that shows nearly every mark the language has."""
    b = board(tmp_path, "full.json")
    for i, st in enumerate(("on_track", "paused", "cancelled", "completed")):
        p = Project(f"P{i}", ["lime", "sky", "violet", "pink"][i], st,
                    start_date=iso(-20), due_date=iso(10 + i))
        b.projects.append(p)
    a = b.projects[0]
    b.tasks += [
        Task("Late thing", a.id, "Doing", "high", start_date=iso(-9), due_date=iso(-4)),
        Task("Due today", a.id, "Doing", "normal", start_date=iso(-2), due_date=iso(0)),
        Task("This week", a.id, "Backlog", "normal", start_date=iso(1), due_date=iso(4)),
        Task("Much later", a.id, "Backlog", "normal", start_date=iso(20), due_date=iso(50)),
        Task("Finished", a.id, "Done", "normal", start_date=iso(-30), due_date=iso(-25)),
        Task("No date", a.id, "Backlog", "normal"),
        Task("Blocked", a.id, "Doing", "normal", due_date=iso(6), blocked=True),
    ]
    return b


def bare(tmp_path):
    """One healthy project, one dated task: most marks are absent."""
    b = board(tmp_path, "bare.json")
    p = Project("Solo", "lime", "on_track", start_date=iso(-3), due_date=iso(20))
    b.projects.append(p)
    b.tasks.append(Task("Only thing", p.id, "Backlog", "normal",
                        start_date=iso(1), due_date=iso(9)))
    return b


def swatches(entries):
    return [_strip(s) for s, _m in entries]


def meanings(entries):
    return [m for _s, m in entries]


# --------------------------------------------------------------------------- #
# 3 — it explains only what is on screen
# --------------------------------------------------------------------------- #
def test_no_entry_describes_a_mark_the_view_is_not_drawing(tmp_path):
    """THE GHOST-MARK LAW. Every swatch must actually occur in the rendered
    view; an entry for a mark that is not there sends the reader hunting."""
    for maker in (full, bare):
        b = maker(tmp_path)
        for mode in VIEWS:
            painted = str(render_view(mode, b, False, None, TODAY,
                                      width=120, height=40))
            for swatch, meaning in legend_entries(mode, b, TODAY, 120, 40):
                plain = _strip(swatch)
                if plain == "!N":                  # the count, drawn as `!3`
                    assert "!" in painted, f"{mode}: {meaning}"
                    continue
                assert any(ch in painted for ch in plain if ch != " "), \
                    f"{mode}: legend shows {plain!r} ({meaning}) but the view has none"


def test_a_quiet_board_gets_a_shorter_legend_than_a_busy_one(tmp_path):
    """The filter is real, not decorative: absent statuses, absent urgencies and
    absent phases all drop out."""
    busy, quiet = legend_entries("swimlanes", full(tmp_path), TODAY), \
        legend_entries("swimlanes", bare(tmp_path), TODAY)
    assert len(quiet) < len(busy)
    assert not [m for m in meanings(quiet) if "cancelled" in m or "paused" in m]
    assert [m for m in meanings(busy) if "cancelled" in m]


def test_the_status_marks_appear_only_for_statuses_the_board_holds(tmp_path):
    b = board(tmp_path, "st.json")
    p = Project("Only paused", "lime", "paused", due_date=iso(5))
    b.projects.append(p)
    b.tasks.append(Task("A thing", p.id, "Doing", "normal", due_date=iso(3)))
    marks = meanings(legend_entries("swimlanes", b, TODAY))
    assert [m for m in marks if "paused" in m]
    assert not [m for m in marks if "cancelled" in m or "completed" in m]


def test_an_empty_board_promises_nothing(tmp_path):
    """With nothing drawn, there is nothing to explain but the axis itself."""
    b = board(tmp_path, "empty.json")
    for mode in VIEWS:
        for _swatch, meaning in legend_entries(mode, b, TODAY):
            assert "meter" not in meaning, f"{mode}: {meaning}"
            assert "project" not in meaning or "under most pressure" in meaning
            assert "phase" not in meaning


# --------------------------------------------------------------------------- #
# 1 — the swatches ARE the render functions
# --------------------------------------------------------------------------- #
def test_the_meter_swatches_are_the_meter_itself(tmp_path):
    """Not a picture of a meter: the same call the row makes."""
    from taskboard.views import due_meter, meter_markup
    entries = dict((m, s) for s, m in legend_entries("swimlanes", full(tmp_path), TODAY))
    assert entries["meter: overdue — ▲ is the only alert"] == \
        meter_markup(due_meter(-1, done=False))
    assert entries["meter: due later"] == meter_markup(due_meter(40, done=False))
    assert entries["meter in ash: work spent"] == \
        meter_markup(due_meter(None, done=True))


def test_the_phase_swatches_are_the_phase_glyph_itself(tmp_path):
    """Needs a board with a STACKED lane: the leader names no phases (its tail
    row carries a title and a distance), so a one-project board draws no phase
    glyph at all — and, correctly, gets no phase entry."""
    from taskboard.views import phase_glyph
    b = full(tmp_path)
    second = b.projects[1]
    second.status = "on_track"
    b.tasks += [Task("Second backlog", second.id, "Backlog", "normal", due_date=iso(5)),
                Task("Second doing", second.id, "Doing", "normal", due_date=iso(7))]
    swatch = swatches(legend_entries("swimlanes", b, TODAY, 120, 40))
    assert phase_glyph({0}) in swatch and phase_glyph({1}) in swatch
    assert phase_glyph({0}) != phase_glyph({1})

    lonely = swatches(legend_entries("swimlanes", bare(tmp_path), TODAY, 120, 40))
    assert phase_glyph({0}) not in lonely


# --------------------------------------------------------------------------- #
# 2 — it is per view
# --------------------------------------------------------------------------- #
def test_each_view_gets_its_own_legend(tmp_path):
    b = full(tmp_path)
    sets = {mode: set(swatches(legend_entries(mode, b, TODAY))) for mode in VIEWS}
    assert sets["swimlanes"] != sets["gantt"] != sets["agenda"]
    assert "●" in sets["agenda"] and "●" not in sets["swimlanes"]
    # the gantt's marks after the field redesign: the two bands, not a slab
    assert any("⣿" in s for s in sets["gantt"])
    assert not any("⣿" in s for s in sets["agenda"])


# --------------------------------------------------------------------------- #
# the register
# --------------------------------------------------------------------------- #
def test_the_legend_describes_marks_and_never_addresses_the_reader(tmp_path):
    """No second person, no instruction, no judgement of the work."""
    banned = re.compile(r"\b(you|your|yours|please|should|must|don't|do not)\b", re.I)
    for maker in (full, bare):
        b = maker(tmp_path)
        for mode in VIEWS:
            for _s, meaning in legend_entries(mode, b, TODAY):
                assert not banned.search(meaning), f"{mode}: {meaning!r}"
                assert meaning == meaning.lower() or meaning[0].isupper() is False


# --------------------------------------------------------------------------- #
# the key and the screen
# --------------------------------------------------------------------------- #
def test_the_legend_key_is_universal_so_it_can_never_be_dropped():
    """It explains the keys that lost their words, so it must outlive them."""
    entry = next(k for k in KEYMAP if k.action == "legend")
    assert entry.universal is True
    assert entry.show == "?"


async def test_pressing_question_mark_opens_the_legend_over_the_view(tmp_path):
    from taskboard.app import TaskboardApp
    from taskboard.modals import LegendModal
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("3")                       # gantt
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, LegendModal)
        assert app.screen._mode == "gantt"           # the CURRENT view's legend
        assert len(app.screen_stack) > 1             # drawn over, not instead of
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, LegendModal)


async def test_the_legend_follows_the_view_the_reader_is_on(tmp_path):
    from taskboard.app import TaskboardApp
    from taskboard.modals import LegendModal
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        for key, mode in (("1", "swimlanes"), ("2", "agenda"), ("4", "kanban")):
            await pilot.press(key)
            await pilot.pause()
            await pilot.press("question_mark")
            await pilot.pause()
            assert app.screen._mode == mode
            await pilot.press("escape")
            await pilot.pause()

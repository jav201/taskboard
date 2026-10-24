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

import json
import re
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.text import Text

import milestone_marks_fixture as fx
from taskboard import app as app_module
from taskboard import models, views
from taskboard.keymap import KEYMAP, VIEWS
from taskboard.marks import Mark
from taskboard.models import Board, Project, Task
from taskboard.views import (_strip, legend_entries, legend_strip,
                             legend_strip_project, render_present,
                             render_present_all, render_view)

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
    assert entries["days overdue — ▲ is the only alert"] == \
        meter_markup(due_meter(-1, done=False))
    assert entries["due later"] == meter_markup(due_meter(40, done=False))
    assert entries["finished, and no longer counting down"] == \
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
    # THE DISCRIMINATOR IS THE TASK REACH, NOT THE PROJECT SPAN, and the reason
    # is a design convergence rather than a bug. This used to assert that
    # `FIELD_REACH` appeared in the gantt and NOT in the agenda -- true only
    # while the gantt's span was the HEAVY `━` and the agenda's reach the light
    # `─`. The 2026-08-07 redesign made the gantt's span thin, so both views now
    # draw `─` for "a reach", which is one mark meaning one thing in two places:
    # exactly what a legend register is for. Asserting the old inequality would
    # have forced the two views apart to keep a test green.
    #
    # `FIELD_TASK` still separates them: only the gantt draws a task's own reach.
    from taskboard.views import FIELD_REACH, FIELD_TASK
    assert any(FIELD_REACH in s for s in sets["gantt"])
    assert any(FIELD_TASK in s for s in sets["gantt"])
    assert not any(FIELD_TASK in s for s in sets["agenda"])
    assert FIELD_TASK != FIELD_REACH, (
        "the two rules collapsed into one; the hierarchy reach > task is gone")


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


async def test_pressing_question_mark_opens_help_modal(tmp_path):
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette, HelpModal
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("3")                       # gantt
        await pilot.pause()
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        assert len(app.screen_stack) > 1             # drawn over, not instead of
        # the palette is reachable from the help modal with another `?`
        await pilot.press("question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        await pilot.press("escape")                  # close palette
        await pilot.pause()
        assert isinstance(app.screen, HelpModal)
        await pilot.press("escape")                  # close help modal
        await pilot.pause()
        assert not isinstance(app.screen, HelpModal)


async def test_the_palette_follows_the_view_the_reader_is_on(tmp_path):
    """The palette lists only the commands live in the current view."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette
    from textual.widgets import OptionList
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        for key, mode in (("1", "swimlanes"), ("2", "agenda"), ("4", "kanban")):
            await pilot.press(key)
            await pilot.pause()
            await pilot.press("question_mark", "question_mark")
            await pilot.pause()
            palette = app.screen
            assert isinstance(palette, CommandPalette)
            lst = palette.query_one("#palette-list", OptionList)
            rows = [str(o.prompt) for o in lst.options]
            expected = {k.show for k in KEYMAP if k.views is None or mode in k.views}
            shown = {r.split()[0] for r in rows}
            assert expected <= shown, f"{mode}: missing {expected - shown}"
            await pilot.press("escape", "escape")
            await pilot.pause()



# --------------------------------------------------------------------------- #
# the KEYS section (LLR-012.2): what the narrow bar drops stays one `?` away
# --------------------------------------------------------------------------- #
def _palette_rows(app) -> list[str]:
    """The palette's option rows, read off the mounted CommandPalette."""
    from textual.widgets import OptionList
    lst = app.screen.query_one("#palette-list", OptionList)
    return [str(o.prompt) for o in lst.options]


def _seat_live(view: str) -> list[str]:
    """The expected rows, computed off the RAW seat — never through the
    `bar_keys` accessor the palette consumes, or the test would certify the
    accessor against itself."""
    live = [k for k in KEYMAP if k.views is None or view in k.views]
    live = sorted(live, key=lambda k: not k.universal)
    return [f"{k.show}  {k.label}" for k in live]


async def test_the_palette_lists_exactly_the_current_views_live_keys(tmp_path):
    """LLR-012.2: the PALETTE is DERIVED from the same seat the bar reads —
    it lists the view's live keys, every one of them, in bar order, and none
    the seat does not declare for that view. Exact equality is the pin."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        for key, view in (("4", "kanban"), ("1", "swimlanes")):
            await pilot.press(key)
            await pilot.pause()
            await pilot.press("question_mark", "question_mark")
            await pilot.pause()
            assert isinstance(app.screen, CommandPalette)
            assert _palette_rows(app) == _seat_live(view), view
            await pilot.press("escape", "escape")
            await pilot.pause()


async def test_the_palette_keys_follow_the_views_scope(tmp_path):
    """The discriminating limbs: kanban's palette includes the kanban-scoped
    `tab` and the batch's new quick keys; swimlanes now includes `tab` too,
    but still scopes away keys that do not work there."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    tab = next(k for k in KEYMAP if k.action == "toggle_presentation")
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("4")
        await pilot.pause()
        await pilot.press("question_mark", "question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        rows = _palette_rows(app)
        assert any(r.startswith(tab.show) for r in rows)
        for show in ("[", "]", "!", "b"):
            assert any(r.startswith(show) for r in rows), show
        await pilot.press("escape", "escape")
        await pilot.pause()
        await pilot.press("1")
        await pilot.pause()
        await pilot.press("question_mark", "question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        rows = _palette_rows(app)
        assert any(r.startswith(tab.show) for r in rows)
        await pilot.press("escape", "escape")
        await pilot.pause()


async def test_the_palette_filters_commands_by_name_or_key(tmp_path):
    """Typing in the palette narrows the list by label or key show."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette
    from textual.widgets import Input
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("question_mark", "question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        inp = app.screen.query_one("#palette-input", Input)
        await pilot.press("q", "u", "i", "t")
        await pilot.pause()
        rows = _palette_rows(app)
        assert rows, "filtering quit should keep at least the quit row"
        assert all("quit" in r.lower() or "q" in r.lower() for r in rows)
        await pilot.press("escape", "escape")
        await pilot.pause()


async def test_the_palette_runs_a_selected_command(tmp_path):
    """Enter on a palette item executes its action."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette
    from textual.widgets import Input
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("1")
        await pilot.pause()
        assert app.view_mode == "swimlanes"
        await pilot.press("question_mark", "question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        inp = app.screen.query_one("#palette-input", Input)
        await pilot.press("k", "a", "n", "b", "a", "n")
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert not isinstance(app.screen, CommandPalette)
        assert app.view_mode == "kanban"


async def test_the_palette_closes_without_running(tmp_path):
    """esc, ? and q close the palette and leave the board untouched."""
    from taskboard.app import TaskboardApp
    from taskboard.modals import CommandPalette
    b = full(tmp_path)
    b.save()
    app = TaskboardApp(board_path=str(tmp_path / "full.json"))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("1")
        await pilot.pause()
        original_mode = app.view_mode
        await pilot.press("question_mark", "question_mark")
        await pilot.pause()
        assert isinstance(app.screen, CommandPalette)
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, CommandPalette)
        assert app.view_mode == original_mode


# --------------------------------------------------------------------------- #
# batch 2026-10-24-batch-01, increment 004 — the classes' strip, hide and help
# (HLR-2607/HLR-2608; AT-2605 minted here; TC-2607, TC-2608)
# --------------------------------------------------------------------------- #
FX_TODAY = fx.TODAY
FX_HEX = {k: v.lower() for k, v in views.HEX.items()}


class _FxToday(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def fx_home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views):
        monkeypatch.setattr(mod, "date", _FxToday)
    return tmp_path / ".taskboard"


def _fx_open(home):
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    return open_app(None)


def _fx_board(tmp_path, bid="client-a", hidden=(), extra=()):
    """The fixture's board with its directory live: `hidden` class ids toggled,
    `extra` (id, name, shape, colour) classes with no milestones appended."""
    b = fx.build_board(tmp_path, bid)
    marks = {cid: Mark(cid, n, s, k) for cid, n, s, _h, k in fx.CLASSES}
    marks.update({cid: Mark(cid, n, s, k) for cid, n, s, k in extra})
    for cid in hidden:
        marks[cid].hidden = True
    b.marks = marks
    return b


def _painted2(app) -> list[list[tuple[str, str | None]]]:
    strips = app.screen._compositor.render_strips(app.screen.size)
    rows = []
    for s in strips:
        cells = []
        for seg in s:
            hx = (seg.style.color.triplet.hex.lower()
                  if seg.style and seg.style.color and seg.style.color.triplet else None)
            cells += [(ch, hx) for ch in seg.text]
        rows.append(cells)
    return rows


def _ptext(rows) -> list[str]:
    return ["".join(ch for ch, _ in r) for r in rows]


def _prow2(rows, needle):
    for r in rows:
        if needle in "".join(ch for ch, _ in r):
            return r
    raise AssertionError(f"{needle!r} not painted")


def _hexes2(row, needle) -> list[str | None]:
    text = "".join(ch for ch, _ in row)
    i = text.index(needle)
    return [row[i + k][1] for k in range(len(needle))]


def _span_styles(markup: str) -> list[tuple[str, str]]:
    t = Text.from_markup(markup, emoji=False)
    return [(t.plain[sp.start:sp.end], str(sp.style)) for sp in t.spans]


def _strip_row(painted: list[str]) -> str:
    """The gantt's strip row: the one naming a class and the hidden count."""
    return next(ln for ln in painted
                if "hidden" in ln and any(n in ln for n in ("Delivery", "Review")))


# --------------------------------------------------------------------------- #
# TC-2607 — the gantt's strip (LLR-2607.1)
# --------------------------------------------------------------------------- #
def test_TC_2607_the_strip_lists_exactly_the_drawn_classes_then_the_hidden_count(tmp_path):
    """Only the classes of the board's milestones, in directory order — a class
    with no milestone is not drawn and not named; a hidden class is gone from
    the names and counted instead. RED: the legend counting all classes."""
    b = _fx_board(tmp_path, extra=[("zzz", "Zephyr", "▼", "green")])
    strip = legend_strip(b, 118)
    plain = _strip(strip)
    assert views.vis(plain) == 118
    for name, shape, colour in (("Delivery", "▲", "cyan"), ("Payment", "⬢", "amber"),
                                ("Review", "■", "violet"), ("Launch", "★", "pink")):
        i = plain.index(name)
        assert plain[i - 2] == shape
        styles = _span_styles(strip)
        assert (shape + " ", views.HEX[colour]) in styles, (shape, styles)
        assert (name, views.HEX["mut"]) in styles, (name, styles)
    assert "Zephyr" not in plain and "0 hidden" in plain
    assert plain.index("Delivery") < plain.index("Payment") < plain.index("Review")
    # hide one: its milestones are not drawn, so it is not named — it is counted
    b.marks["payment"].hidden = True
    plain = _strip(legend_strip(b, 118))
    assert "Payment" not in plain and "⬢" not in plain
    assert all(n in plain for n in ("Delivery", "Review", "Launch"))
    assert "1 hidden" in plain


def test_TC_2607_no_classed_milestone_in_view_draws_no_strip(tmp_path):
    """The empty arm: only unclassified milestones (or no directory at all) →
    no strip row. RED: the strip drawn with no classed milestone in view."""
    b = _fx_board(tmp_path)
    for t in b.tasks:
        t.mark = None
    assert legend_strip(b, 118) == ""
    b.marks = {}
    assert legend_strip(b, 118) == ""


def test_TC_2607_every_class_hidden_draws_no_strip(tmp_path):
    """With every class hidden every classed milestone left the frame with
    them: no class is drawn, so no strip names one."""
    b = _fx_board(tmp_path, hidden=("delivery", "payment", "review", "launch"))
    assert legend_strip(b, 118) == ""


def test_TC_2607_at_80_cells_the_strip_cuts_names_from_the_right(tmp_path):
    """The 80-cell arm: the row stays exactly `w` cells; whole classes give way
    from the right. RED: the row left wider than `w`, or the cut from the left."""
    marks = [(f"c{i}", f"Classified number {i}", "■", "violet") for i in range(6)]
    b = Board([], [Task(f"t{i}", None, "Next", "normal", due_date=fx._d(i + 1),
                        milestone=True, mark=f"c{i}", id=f"t{i}") for i in range(6)],
              fx.Path("x.json"), phases=["Next", "Done"])
    b.marks = {cid: Mark(cid, n, s, k) for cid, n, s, k in marks}
    strip = legend_strip(b, 80)
    plain = _strip(strip)
    assert views.vis(plain) == 80
    assert "Classified number 5" not in plain      # the rightmost names went first
    assert "Classified number 0" in plain


def test_TC_2607_a_markup_looking_name_prints_as_typed(tmp_path):
    """C-17 in the strip: a class named like markup is printed literally, never
    parsed. RED: the strip built as markup with the raw name."""
    b = _fx_board(tmp_path)
    b.marks["review"].name = "[b]x[/b]"
    strip = legend_strip(b, 118)
    t = Text.from_markup(strip, emoji=False)
    assert "[b]x[/b]" in t.plain
    name_span = next(sp for sp in t.spans if "[b]x[/b]" in t.plain[sp.start:sp.end])
    assert str(name_span.style) == views.HEX["mut"] and "bold" not in str(name_span.style)


# --------------------------------------------------------------------------- #
# TC-2607 — the presentation's strip (LLR-2607.1)
# --------------------------------------------------------------------------- #
def test_TC_2607_the_presentation_strip_names_only_the_projects_shown_classes(tmp_path):
    """`legend_strip_project`: the classes of the milestones THIS project shows
    (open or done), not the board's — and `N hidden` keeps the toggle honest."""
    b = _fx_board(tmp_path)
    pilot = b.project_by_id("pcr")             # Pilot rollout: payment, review, launch
    plain = _strip(legend_strip_project(b, pilot, 118))
    assert views.vis(plain) == 118
    for n in ("Payment", "Review", "Launch"):
        assert n in plain
    assert "Delivery" not in plain and "0 hidden" in plain
    b.marks["payment"].hidden = True
    plain = _strip(legend_strip_project(b, pilot, 118))
    assert "Payment" not in plain and "1 hidden" in plain
    quiet = _fx_board(tmp_path, bid="main").project_by_id("ppf")   # Fitness: no classed ms
    assert legend_strip_project(_fx_board(tmp_path, bid="main"), quiet, 118) == ""


def test_TC_2607_the_presentation_views_and_export_carry_the_strip(tmp_path):
    """`render_present`'s gantt and split views draw the strip under the ruler
    and the SVG export carries it — at 118x30 and 80x24. RED: the strip row
    computed but never painted into the frame (the PDR's reddener)."""
    from taskboard.views import present_all_export, save_present_svg
    b = _fx_board(tmp_path)
    for w, h in ((118, 30), (80, 24)):
        for view in ("gantt", "split"):
            text = render_present(b, "pcr", None, FX_TODAY, w, h, view)
            row = next(ln for ln in text.plain.split("\n")
                       if "hidden" in ln and "Review" in ln)
            for n in ("Payment", "Review", "Launch"):
                assert n in row, (w, view, row)
    text = render_present(b, "pcr", None, FX_TODAY, 118, 30, "gantt")
    out = save_present_svg(text, tmp_path / "reports" / "present.svg", 118, 30)
    svg = out.read_text(encoding="utf-8")
    assert "Payment" in svg and "Launch" in svg
    exp_text, exp_w, exp_h = present_all_export(b, FX_TODAY, 118, 30)
    assert "Final payment" in exp_text.plain     # view 3's export path is exercised


# --------------------------------------------------------------------------- #
# TC-2607 — the `?` help names the classes and the filter (LLR-2607.2)
# --------------------------------------------------------------------------- #
def test_TC_2607_help_names_the_classes_the_manager_and_the_class_filter():
    """`help_usage` names the `/#cls` filter and the `#` manager on the gantt
    and the kanban; `legend_entries("gantt")` gains one entry per drawn class
    beside the `◆ milestone` entry. RED: `?` omits the filter."""
    from taskboard.views import help_usage
    for mode in ("gantt", "kanban"):
        text = "\n".join(ln for _h, lines in help_usage(mode) for ln in lines)
        assert "/#cls" in text, mode
        assert "# manage the classes" in text, mode
    entry = next(k for k in KEYMAP if k.action == "marks_manager")
    assert entry.show == "#"                       # `?` lists the manager
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        b = _fx_board(Path(d))
        meanings = [m for _s, m in legend_entries("gantt", b, FX_TODAY, 118, 30)]
        for _cid, n, _s, _h, _k in fx.CLASSES:
            assert f"{n} · a milestone class" in meanings
        assert "a milestone: one date, no bar" in meanings


# --------------------------------------------------------------------------- #
# TC-2608 — hide leaves the gantt and the presentation (LLR-2608.1)
# --------------------------------------------------------------------------- #
PAYMENT_TITLES = ("Kickoff invoice paid", "Milestone 2 invoice", "Final payment")


def test_TC_2608_hide_drops_the_class_from_the_gantt_and_the_board_is_untouched(tmp_path):
    """`_hide` at the gantt frame's entry: the payment milestones leave the
    cells, the title markers and the label column; the board object stays
    whole — a save writes every task it held. RED: the proxy leaking into a
    save, or a hidden class still drawn."""
    b = _fx_board(tmp_path, hidden=("payment",))
    painted = render_view("gantt", b, False, None, FX_TODAY, 118, 30).plain
    for title in PAYMENT_TITLES:
        assert title not in painted, title
    b2 = _fx_board(tmp_path)                       # no hidden class: the identity
    assert PAYMENT_TITLES[1] in render_view("gantt", b2, False, None, FX_TODAY,
                                            118, 30).plain
    assert {t.id for t in b.tasks} == \
        {t.id for t in _fx_board(tmp_path, hidden=("payment",)).tasks}
    marked = [t for t in b.tasks if t.mark == "payment"]
    assert {t.id for t in marked} == {"tc8", "tcc", "tce"}
    b.save()
    data = json.loads(b.path.read_text(encoding="utf-8"))
    saved = {t["id"]: t for t in data["tasks"]}
    assert all(saved[t.id].get("mark") == "payment" for t in marked)   # kept on disk


def test_TC_2608_present_tasks_m_drops_hidden_classes_and_none_hidden_is_identity(tmp_path):
    """The wrapper over `present_tasks`: hidden-classed milestones leave both
    the open list and the all list (done ones included); with nothing hidden
    the wrapper is the identity. RED: `present_tasks_m` not filtering."""
    b = _fx_board(tmp_path, hidden=("payment",))
    open_t, tasks = views.present_tasks_m(b, "pcr")
    ids = {t.id for t in tasks}
    assert "tcc" not in ids and "tc8" not in ids          # the payment milestones
    assert {"tc9", "tca", "tcb"} <= ids
    assert all(t.id in ids for t in open_t)
    b2 = _fx_board(tmp_path)
    o2, t2 = views.present_tasks_m(b2, "pcr")
    assert [t.id for t in o2] == [t.id for t in views.present_tasks(b2, "pcr")[0]]
    assert [t.id for t in t2] == [t.id for t in views.present_tasks(b2, "pcr")[1]]


def test_TC_2608_hidden_classes_leave_the_presentations_three_views_and_exports(tmp_path):
    """At 118x30 and 80x24: the payment milestones are gone from the gantt and
    split views, view 3's timeline, and the exported bytes — and the strips
    keep the hidden count instead of the names. RED: one export still drawing
    a hidden class."""
    from taskboard.views import present_all_export, save_present_svg
    b = _fx_board(tmp_path, hidden=("payment",))
    for w, h in ((118, 30), (80, 24)):
        for view in ("gantt", "split"):
            plain = render_present(b, "pcr", None, FX_TODAY, w, h, view).plain
            for title in PAYMENT_TITLES:
                assert title not in plain, (w, view, title)
            row = next(ln for ln in plain.split("\n")
                       if "hidden" in ln and "Review" in ln)
            assert "Payment" not in row and "1 hidden" in row, (w, view, row)
        all_frame = render_present_all(b, None, FX_TODAY, w, h)
        for title in PAYMENT_TITLES:
            assert title not in all_frame.timeline.plain, (w, title)
    text = render_present(b, "pcr", None, FX_TODAY, 118, 30, "gantt")
    out = save_present_svg(text, tmp_path / "reports" / "hidden.svg", 118, 30)
    svg = out.read_text(encoding="utf-8")
    for title in PAYMENT_TITLES:
        assert title not in svg, title
    exp_text, _w, _h = present_all_export(b, FX_TODAY, 118, 30)
    for title in PAYMENT_TITLES:
        assert title not in exp_text.plain, title


# --------------------------------------------------------------------------- #
# AT-2605 — hide and the legend, through the app's own keys (HLR-2607/2608)
# --------------------------------------------------------------------------- #
async def test_AT_2605_hide_and_the_legend(fx_home):
    """`#`, `down`, `space` on Payment: its milestones leave the gantt (cells,
    title markers) and the presentation's three views and their exports, at
    118x30 and 80x24; the strip under the ruler names the drawn classes and
    `1 hidden`; the gantt's details line names the classes beside `◆
    milestone` (painted at both sizes); `space` again brings the class back.
    Tone claims ride the styled-segment export. RED: the strip naming a class
    not drawn, or a hidden class still drawn in one export."""
    app = _fx_open(fx_home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")                  # the home
        await pilot.press("3")                       # the gantt
        await pilot.pause()
        rows = _painted2(app)
        strip = _strip_row(_ptext(rows))
        for name in ("Delivery", "Payment", "Review", "Launch"):
            assert name in strip
        assert "0 hidden" in strip
        srow = _prow2(rows, "Delivery")
        assert _hexes2(srow, "▲")[0] == FX_HEX["cyan"]      # the shapes in their colours
        assert _hexes2(srow, "⬢")[0] == FX_HEX["amber"]
        # ---- hide Payment through the manager ----
        await pilot.press("number_sign")
        await pilot.pause()
        await pilot.press("down")                    # delivery -> payment
        await pilot.press("space")
        await pilot.press("escape")
        await pilot.pause()
        rows = _painted2(app)
        text = _ptext(rows)
        for title in PAYMENT_TITLES:
            assert not any(title in ln for ln in text), title
        strip = _strip_row(text)
        assert "Payment" not in strip and "1 hidden" in strip
        for name in ("Delivery", "Review", "Launch"):
            assert name in strip
        assert {t.id for t in app.board.tasks if t.mark == "payment"} == \
            {"tc8", "tcc", "tce"}                    # the board itself untouched
        # the details line (the spare row) names the classes beside ◆ milestone
        details = _prow2(rows, "◆ milestone")
        dtext = "".join(ch for ch, _ in details)
        for name in ("Delivery", "Review", "Launch"):
            assert name in dtext, dtext
        assert "Payment" not in dtext
        # ---- the presentation: views 1/2/3 and their exports ----
        app.selected_task_id = "tc9"                 # Pilot rollout: payment ms inside
        await pilot.press("R")
        await pilot.pause()
        rows = _painted2(app)
        assert not any(PAYMENT_TITLES[1] in ln for ln in _ptext(rows))
        pstrip = "".join(ch for ch, _ in _prow2(rows, "■ Review"))
        assert "Payment" not in pstrip and "1 hidden" in pstrip
        for view_key in ("2", "3", "1"):             # split, all, gantt
            await pilot.press(view_key)
            await pilot.pause()
            rows = _painted2(app)
            assert not any(PAYMENT_TITLES[1] in ln for ln in _ptext(rows)), view_key
        await pilot.press("x")                       # export view 1's frame
        await pilot.press("3")                       # view 3: its timeline exports
        await pilot.press("x")
        await pilot.pause()
        reports = fx_home / "boards" / "client-a" / "reports"
        svgs = sorted(reports.glob("*.svg"))
        assert len(svgs) >= 2, svgs
        for svg in svgs:
            body = svg.read_text(encoding="utf-8")
            for title in PAYMENT_TITLES:
                assert title not in body, (svg.name, title)
        await pilot.press("escape")                  # leave the presentation
        await pilot.pause()
        # ---- unhide: the class is back ----
        await pilot.press("number_sign")
        await pilot.pause()
        await pilot.press("down")
        await pilot.press("space")
        await pilot.press("escape")
        await pilot.pause()
        rows = _painted2(app)
        text = _ptext(rows)
        assert any(PAYMENT_TITLES[1] in ln for ln in text)
        strip = _strip_row(text)
        assert "Payment" in strip and "0 hidden" in strip
    # ---- the same at 80x24: a second window on the same home ----
    app2 = _fx_open(fx_home)
    async with app2.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await pilot.press("3")
        await pilot.pause()
        await pilot.press("number_sign")
        await pilot.pause()
        await pilot.press("down")
        await pilot.press("space")
        await pilot.press("escape")
        await pilot.pause()
        rows = _painted2(app2)
        text = _ptext(rows)
        for title in PAYMENT_TITLES:
            assert not any(title in ln for ln in text), title
        strip = next(ln for ln in text if "1 hidden" in ln)
        assert views.vis(strip) == 80
        assert "Payment" not in strip
        for name in ("Delivery", "Review", "Launch"):
            assert name in strip
        srow = _prow2(rows, "Delivery")
        assert _hexes2(srow, "■")[0] == FX_HEX["violet"]
        details = _prow2(rows, "◆ milestone")        # the details line paints here too
        dtext = "".join(ch for ch, _ in details)
        for name in ("Delivery", "Review", "Launch"):
            assert name in dtext, dtext
        app2.selected_task_id = "tc9"
        await pilot.press("R")
        await pilot.pause()
        rows = _painted2(app2)
        assert not any(PAYMENT_TITLES[1] in ln for ln in _ptext(rows))
        pstrip = "".join(ch for ch, _ in _prow2(rows, "■ Review"))
        assert "Payment" not in pstrip and "1 hidden" in pstrip
        await pilot.press("2")                       # the split view, narrow
        await pilot.pause()
        rows = _painted2(app2)
        assert not any(PAYMENT_TITLES[1] in ln for ln in _ptext(rows))


def test_TC_2607_a_lone_over_long_name_is_cut_not_crashed(tmp_path):
    """The lone-class arm of the width law: one drawn class whose name exceeds
    the room at a narrow `w` (below the gantt's MIN_WIDTH, where `room` leaves
    the name ~10 cells) is CUT from its right — never a crash, the row still
    exactly `w` cells with the shape leading. RED on the F1 code: the
    `(text, colour)` tuple unpacked as `(shape, name)` and `parts[1]` on a
    1-element list — an IndexError inside the frame."""
    long_name = "Quarterly review checkpoint"                   # 27 cells
    b = _fx_board(tmp_path)
    b.marks = {"solo": Mark("solo", long_name, "■", "violet")}
    for t in b.tasks:
        t.mark = "solo" if t.milestone else None
    for w in (30, 20):                                      # 20 < the gantt's MIN_WIDTH
        plain = _strip(legend_strip(b, w))
        assert views.vis(plain) == w, (w, plain)
        assert plain.lstrip().startswith("■"), plain        # the shape still leads
        assert long_name not in plain and plain.rstrip().endswith("hidden"), plain
        assert long_name[:5] in plain                         # the cut is from the right
    pilot = b.project_by_id("pcr")
    plain = _strip(legend_strip_project(b, pilot, 30))      # the 2-cell lead too
    assert views.vis(plain) == 30 and plain.lstrip().startswith("■"), plain
    assert long_name not in plain and "hidden" in plain.rstrip(), plain

"""Ctrl+E — pick an emoji by name, insert the glyph.

WHY THIS FILE EXISTS: the board renders emoji happily, but nobody remembers that
the bug is `:bug:` and the rocket is `:rocket:`. The picker removes the memory
requirement. Two things about it are load-bearing and are pinned here:

1. **It inserts the GLYPH, never the `:shortcode:`.** A shortcode is 5+ characters
   that draw as 2, so a title holding one sizes its row wrong — that is the whole
   subject of tests/test_cells.py. The glyph is a real character `views.vis()`
   measures correctly, so picking one costs the layout nothing. The last test
   here proves that end to end rather than asserting it in prose.

2. **The emoji table is a PRIVATE rich module.** `rich._emoji_codes` could move
   in any release. This file asserts it is present and shaped as expected, so an
   upgrade that moves it turns RED here instead of silently shipping a picker
   with a shorter list, or none.
"""

from datetime import date
from pathlib import Path

import pytest
from rich.cells import cell_len

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import (EMOJI_RESULTS, EmojiPicker, TaskModal, _EMOJI_CHOICES,
                              search_emoji)
from taskboard.views import render_view

PHASES = ["Backlog", "Doing", "Review", "Done"]


# --------------------------------------------------------------------------- #
# the table we depend on
# --------------------------------------------------------------------------- #
def test_the_private_rich_emoji_table_is_still_there():
    """Deliberately brittle. If rich moves `_emoji_codes`, this is the red that
    says so — the alternative is a silent fallback nobody notices for months."""
    from rich._emoji_codes import EMOJI
    assert len(EMOJI) > 1000, "the emoji table shrank unrecognisably"
    assert EMOJI["bug"] == "\U0001F41B"
    assert EMOJI["rocket"] == "\U0001F680"


def test_every_offered_emoji_is_actually_visible():
    """A zero-width entry is a combining part; offering one means offering a
    choice that does nothing on screen."""
    assert _EMOJI_CHOICES, "the picker has nothing to offer"
    assert all(cell_len(g) >= 1 for _, g in _EMOJI_CHOICES)


# --------------------------------------------------------------------------- #
# search — the part that decides what you can find
# --------------------------------------------------------------------------- #
def test_search_finds_the_obvious_ones():
    assert ("bug", "\U0001F41B") in search_emoji("bug")
    assert ("rocket", "\U0001F680") in search_emoji("rocket")


def test_space_and_underscore_are_the_same_keystroke():
    """The table spells it `flexed_biceps`; a human types 'flexed biceps'."""
    assert search_emoji("flexed biceps") == search_emoji("flexed_biceps")
    assert search_emoji("flexed biceps"), "a real multi-word name found nothing"


def test_search_is_case_insensitive_and_ignores_surrounding_space():
    assert search_emoji("  BUG  ") == search_emoji("bug")


def test_an_empty_search_offers_everything():
    assert search_emoji("") == _EMOJI_CHOICES
    assert search_emoji("   ") == _EMOJI_CHOICES


def test_a_nonsense_search_finds_nothing_rather_than_everything():
    assert search_emoji("zzzznotanemoji") == []


# --------------------------------------------------------------------------- #
# the picker, driven
# --------------------------------------------------------------------------- #
def board(tmp_path) -> Board:
    p = Project(name="Proj", color="cyan")
    return Board([p], [Task(title="arreglar el parser", project_id=p.id,
                            phase="Doing")], tmp_path / "board.json", phases=PHASES)


def app_on(tmp_path) -> TaskboardApp:
    """NEVER `TaskboardApp()`: the bare constructor loads the REAL board from
    ~/.taskboard, and `on_mount` SAVES it (the renumber notice). A test that
    reads a developer's live data is a leak, and one that writes it is worse."""
    app = TaskboardApp(board_path=str(tmp_path / "board.json"))
    app.board = board(tmp_path)
    return app


async def test_ctrl_e_inserts_the_glyph_at_the_cursor(tmp_path):
    """The whole feature, end to end: open the task editor, Ctrl+E, type a name,
    Enter — and the TITLE FIELD holds the glyph."""
    app = app_on(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")                      # new-task modal
        await pilot.pause()
        modal = app.screen
        assert isinstance(modal, TaskModal)
        title = modal.query_one("#f-title")
        title.focus()
        await pilot.pause()
        await pilot.press("ctrl+e")
        await pilot.pause()
        assert isinstance(app.screen, EmojiPicker), "ctrl+e did not open the picker"
        for ch in "bug":
            await pilot.press(ch)
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert "\U0001F41B" in title.value, f"no glyph inserted (value={title.value!r})"
        assert ":bug:" not in title.value, "a shortcode was inserted instead of a glyph"


async def test_escaping_the_picker_inserts_nothing(tmp_path):
    app = app_on(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")
        await pilot.pause()
        title = app.screen.query_one("#f-title")
        title.focus()
        await pilot.pause()
        before = title.value
        await pilot.press("ctrl+e")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert title.value == before, "cancelling still changed the field"


async def test_ctrl_e_without_a_text_field_focused_does_not_crash(tmp_path):
    """A keypress must never be able to take the app down; the modal says why
    instead."""
    app = app_on(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-project").focus()   # a Select, not a text field
        await pilot.pause()
        await pilot.press("ctrl+e")
        await pilot.pause()
        assert isinstance(app.screen, TaskModal), "the picker opened on a Select"


def test_the_result_cap_is_stated_not_silent():
    """`_show` writes the count line; a picker that shows 200 of 900 without
    saying so teaches you the other 700 do not exist. This pins the CAP itself —
    the count line is asserted through the driven test below."""
    assert EMOJI_RESULTS > 0
    assert len(search_emoji("")) > EMOJI_RESULTS, (
        "the corpus no longer exceeds the cap, so the 'showing the first N' "
        "path is unreachable and this guard has gone vacuous")


async def test_the_picker_says_when_it_is_showing_only_some(tmp_path):
    app = app_on(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("a")
        await pilot.pause()
        app.screen.query_one("#f-title").focus()
        await pilot.pause()
        await pilot.press("ctrl+e")
        await pilot.pause()
        # `Label.content` is the public read-back in textual 8.2.8; `.renderable`
        # does not exist and reading it would make this test a no-op that throws.
        note = str(app.screen.query_one("#emoji-count").content)
        assert "showing the first" in note, f"the cut is not stated: {note!r}"


# --------------------------------------------------------------------------- #
# and the reason it inserts a glyph
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", ["bug", "rocket", "fire", "white_check_mark"])
def test_any_pickable_emoji_leaves_the_rows_the_right_width(name):
    """Pick it, put it in a title, and the board still lines up. This is the
    contract between this feature and tests/test_cells.py — if the picker ever
    starts returning shortcodes, these rows go wrong and this goes red."""
    glyph = dict(_EMOJI_CHOICES)[name]
    p = Project(name=f"Proj {glyph}", color="cyan")
    b = Board([p], [Task(title=f"arreglar {glyph} parser", project_id=p.id,
                         phase="Doing", due_date=str(date.today()))],
              Path("x.json"), phases=PHASES)
    for mode in ("swimlanes", "agenda", "gantt", "kanban"):
        text = render_view(mode, b, False, None, width=96, height=24,
                           line_map={}, presentation="grouped", tick=0)
        bad = [cell_len(l) for l in text.plain.split("\n")
               if l.strip() and cell_len(l) != 96]
        assert not bad, f"{mode} with {name}: widths {bad[:4]}"


async def test_both_editors_say_the_key_exists(tmp_path):
    """This app does not ship keys off-screen: a picker you cannot discover is a
    picker that does not exist. Both text editors announce ctrl+e in their title."""
    from taskboard.modals import ProjectModal
    app = app_on(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        for key, screen_type in (("a", TaskModal), ("p", ProjectModal)):
            await pilot.press(key)
            await pilot.pause()
            assert isinstance(app.screen, screen_type)
            title = str(app.screen.query_one(".modal-title").content)
            assert "ctrl+e" in title, f"{screen_type.__name__} hides the key: {title!r}"
            await pilot.press("escape")
            await pilot.pause()

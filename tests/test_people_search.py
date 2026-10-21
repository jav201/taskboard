"""Search by person: `@` inside the `/` filter (batch 2026-10-21-batch-01, the round's
item 3, variant A).

HLR-2505 / LLR-2505.1, LLR-2505.2 · TC-2505 · AT-2505 (US-2504). Why it matters: the
text filter `ana` also finds «Canary release plan»; a person's filter must find exactly
the tasks whose notes mention them, and `@` alone must be a names-only list — the same
language as the notes, with no mode to remember. Synthetic people only.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from rich.text import Text

import people_round_fixture as fx
from taskboard import app as app_module, models, modals, views
from taskboard.app import PeopleDirectory
from taskboard.models import Board
from taskboard.people import Directory
from test_people_look import screen_text


class _Today(date):
    @classmethod
    def today(cls):
        return fx.TODAY


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    return tmp_path / ".taskboard"


@pytest.fixture
def client_a(tmp_path):
    fx.build(tmp_path)
    b = Board.load(fx.board_path(tmp_path, "client-a"))
    b.people = Directory.load(tmp_path / "people.json").people
    return b


# --------------------------------------------------------------------------- #
# TC-2505 — the filter and its bar (LLR-2505.1)
# --------------------------------------------------------------------------- #
def test_TC_2505_a_person_query_matches_exactly_their_mentions(client_a):
    hits = sorted(t.title for t in client_a.tasks if views.matches(t, client_a, "@ana.ruiz"))
    assert hits == ["Chunking experiments", "Eval report v1", "Golden question set",
                    "Steering committee"]
    assert all(views.matches(t, client_a, "@ana.ruiz") in (None, "person") for t in client_a.tasks)
    assert not any(views.matches(t, client_a, "@ana") for t in client_a.tasks)   # exact handle
    text = sorted(t.title for t in client_a.tasks if views.matches(t, client_a, "ana"))
    assert "Canary release plan" in text                                        # text: unchanged
    fb = views.filtered_board(client_a, "@ana.ruiz", False)
    assert "Canary release plan" not in [t.title for t in fb.tasks]


def test_TC_2505_the_bar_names_the_person_and_their_role(client_a):
    bar = Text.from_markup(views.filter_bar("@ana.ruiz", 3, 11, 118, client_a.people)[0]).plain
    assert bar.startswith("/ @Ana Ruiz  Client A PM · tasks that mention them")
    assert bar.rstrip().endswith("3/11 tasks · esc clears")
    typed = Text.from_markup(views.filter_bar("@Ana.Ruiz", 3, 11, 118, client_a.people)[0]).plain
    assert typed.startswith("/ @Ana Ruiz  Client A PM")                 # CR-3 of 005
    raw = Text.from_markup(views.filter_bar("@zz", 0, 11, 118, client_a.people)[0]).plain
    assert raw.startswith("/ @zz▌")
    assert Text.from_markup(views.filter_bar("ana", 5, 11, 118)[0]).plain.startswith("/ ana▌")


# --------------------------------------------------------------------------- #
# AT-2505 — `/` in the real app
# --------------------------------------------------------------------------- #
def _open(home):
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    return open_app(None)


async def _search(pilot, *keys):
    await pilot.pause()
    await pilot.press("escape", "4", "slash")
    await pilot.pause()
    for k in keys:
        await pilot.press(k)
    await pilot.pause(0.2)


@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2505_at_lists_names_only_and_enter_filters_to_their_tasks(home, size):
    app = _open(home)
    async with app.run_test(size=size) as pilot:
        await _search(pilot, "at", "a", "n")
        assert isinstance(app.screen, modals.SearchPrompt)
        text = await screen_text(pilot, *size)
        assert "PEOPLE · names only" in text and "▶ Ana Ruiz" in text
        assert "+ add" not in text and "esc cancel" in text and "alt+p their page" in text
        await pilot.press("enter")
        text = await screen_text(pilot, *size)
        assert app.search_query == "@ana.ruiz"
        assert "/ @Ana Ruiz" in text
        for title in ("Steering", "Golden", "Chunking"):
            assert title in text
        assert "Canary" not in text and "Invoice" not in text
        await pilot.press("slash")                       # reopened on the person's filter
        text = await screen_text(pilot, *size)
        assert "▶ Ana Ruiz" in text and "no one by that name" not in text   # CR-1 of 005
        await pilot.press("escape")


async def test_AT_2505_at_alone_lists_everyone_and_arrows_choose(home):
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await _search(pilot, "at")
        text = await screen_text(pilot, 118, 30)
        assert "▶ Ana Ruiz" in text and "Diego Paz" in text and "Luis Mora" in text
        assert "Marta Gil" not in text and "Pablo Ortiz" not in text     # QA-1: the first 6
        await pilot.press("down", "enter")
        await pilot.pause()
        assert app.search_query == "@andres.lima"


async def test_AT_2505_alt_p_opens_their_page(home):
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await _search(pilot, "at", "m", "a", "r")
        await pilot.press("alt+p")
        await pilot.pause()
        scr = app.screen
        assert isinstance(scr, PeopleDirectory) and scr.people[scr.sel].id == "marta.gil"
        assert app.search_query is None


async def test_AT_2505_no_one_by_that_name_and_text_still_filters(home):
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await _search(pilot, "at", "z", "z")
        assert "no one by that name" in await screen_text(pilot, 118, 30)
        await pilot.press("alt+p")                 # nothing to open
        assert isinstance(app.screen, modals.SearchPrompt)
        await pilot.press("enter")
        await pilot.pause()
        assert app.search_query == "@zz"
        await pilot.press("escape", "slash", "ctrl+a")
        for k in "ana":
            await pilot.press(k)
        text = await screen_text(pilot, 118, 30)
        assert "text filters tasks · @ starts a person" in text and "↵ / alt+s filter" in text
        await pilot.press("enter")
        await pilot.pause()
        assert app.search_query == "ana"
        assert "Canary" in await screen_text(pilot, 118, 30)


async def test_AT_2505_the_gantt_filters_by_person_too(home):
    """qa QA-4: `/` in the gantt, `@an`, `enter`: the bar names the person."""
    app = _open(home)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "3", "slash", "at", "a", "n", "enter")
        text = await screen_text(pilot, 118, 30)
        assert app.view_mode == "gantt" and app.search_query == "@ana.ruiz"
        assert "/ @Ana Ruiz  Client A PM · tasks that mention them" in text
        assert "Canary" not in text

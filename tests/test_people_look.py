"""How a mention looks: `@Name` in pink in the details, the kanban card and the
presentation (batch 2026-10-21-batch-01, the round's item 4, variant A).

HLR-2506 / LLR-2506.1, LLR-2506.2 · TC-2506 · AT-2506 (US-2505); HLR-2507 / TC-2507 —
a teammate's task carrying mentions draws in the team view and breaks nothing. Why it
matters: the notes store `@ana.ruiz` (the handle), but the operator reads names — in the
details, on the card at a glance, and in front of a room. A mention of a handle the
directory does not hold is shown as typed, never as someone else. Synthetic people only.
"""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

import pytest
from rich.text import Text

import people_round_fixture as fx
from taskboard import app as app_module, models, modals, views
from taskboard.models import Board, Task
from taskboard.people import Directory, Person

_SVG = re.compile(r'<text class="[^"]*" x="([\d.]+)" y="[\d.]+" textLength="[\d.]+" '
                  r'clip-path="url\(#[^)]*-line-(\d+)\)">([^<]*)</text>')
PINK = views.HEX["pink"]
NB = " "


def svg_rows(svg: str, width: int, height: int) -> list[str]:
    rows = [[" "] * width for _ in range(height)]
    for x, line, body in _SVG.findall(svg):
        y, col = int(line), round(float(x) / 12.2)
        if y >= height:
            continue
        for i, ch in enumerate(html.unescape(body).replace("\xa0", " ")):
            if col + i < width:
                rows[y][col + i] = ch
    return ["".join(r).rstrip() for r in rows]


async def screen_text(pilot, w, h) -> str:
    await pilot.pause(0.4)
    return "\n".join(svg_rows(pilot.app.export_screenshot(), w, h))


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


PEOPLE = {h: Person(h, n, r, note) for h, n, r, note in fx.PEOPLE}


def _spans(t: Text) -> dict[str, str]:
    return {t.plain[s.start:s.end]: str(s.style) for s in t.spans}


# --------------------------------------------------------------------------- #
# TC-2506 — the details / editor preview (LLR-2506.1)
# --------------------------------------------------------------------------- #
def test_TC_2506_the_preview_draws_a_known_mention_as_its_name_in_pink():
    t = modals.notes_preview("Review with @ana.ruiz\n- ==send to @diego.paz== now", PEOPLE)
    assert t.plain == "Review with @Ana Ruiz\n- send to @Diego Paz now"
    st = _spans(t)
    assert st["@Ana Ruiz"] == f"b {PINK}" and st["@Diego Paz"] == f"b {PINK}"
    assert st["send to "] == views.HEX["soon"]          # the highlight around it survives


def test_TC_2506_an_unknown_handle_stays_as_typed_and_dimmed():
    t = modals.notes_preview("Ask @an and @sofia.vega, mail ana@x.com", PEOPLE)
    assert t.plain == "Ask @an and @sofia.vega, mail ana@x.com"
    st = _spans(t)
    assert st["@an"] == views.HEX["dim"] and st["@sofia.vega"] == views.HEX["dim"]
    assert st[", mail ana@x.com"] == views.HEX["mut"]


@pytest.mark.parametrize("people", [None, {}], ids=["none", "empty"])
def test_TC_2506_without_a_directory_the_preview_is_unchanged(people):
    """code review CR-1: an app with no people (the board's `{}`) draws as before."""
    t = modals.notes_preview("Ask @ana.ruiz", people)
    assert t.plain == "Ask @ana.ruiz" and _spans(t) == {"Ask @ana.ruiz": views.HEX["mut"]}


def test_TC_2506_a_name_that_looks_like_markup_is_printed_as_typed():
    """code review CR-2: the preview (Text pieces), and the two markup paths — the card's
    token and the presentation's painted row — print a markup-looking name as typed."""
    evil = {"x.y": Person("x.y", "[b]Bold[/b] [/]")}
    t = modals.notes_preview("see @x.y", evil)
    assert t.plain == "see @[b]Bold[/b] [/]"
    b = Board([], [Task(title="T", phase="Doing", due_date="2026-10-20", notes="@x.y", id="t1")],
              Path("unused.json"))
    b.people = evil
    row2 = Text.from_markup(views.kanban_card(b.tasks[0], b, 40, False, today=fx.TODAY)[1]).plain
    assert "@[b]Bold[/b]" in row2
    marks = views.mention_marks(evil)
    row = Text.from_markup(views._present_note_markup(("", views.present_mentions("hi @x.y", evil)),
                                                      40, marks)).plain
    assert row.rstrip() == f"hi @[b]Bold[/b]{NB}[/]"


# --------------------------------------------------------------------------- #
# TC-2506 — the kanban card (LLR-2506.1)
# --------------------------------------------------------------------------- #
def _board(notes: str, due: str | None = "2026-10-20") -> Board:
    b = Board([], [Task(title="Golden question set", phase="Doing", due_date=due, notes=notes,
                        id="t1")], Path("unused.json"))
    b.people = PEOPLE
    return b


def test_TC_2506_the_card_names_the_first_person_and_counts_the_rest_before_the_due():
    b = _board("with @ana.ruiz and @andres.lima, @ana.ruiz again, @nobody")
    toks = views._card_meta(b.tasks[0], b, fx.TODAY, {}, None)
    assert toks[-2:] == [("@Ana+1", "pink"), ("today", toks[-1][1])]
    b.people = {}
    assert all("@" not in tok for tok, _ in views._card_meta(b.tasks[0], b, fx.TODAY, {}, None))


def test_TC_2506_one_person_has_no_count_and_a_tight_card_keeps_the_due():
    b = _board("@marta.gil needs it")
    assert ("@Marta", "pink") in views._card_meta(b.tasks[0], b, fx.TODAY, {}, None)
    wide = views.kanban_card(b.tasks[0], b, 30, False, today=fx.TODAY)
    tight = views.kanban_card(b.tasks[0], b, 12, False, today=fx.TODAY)
    plain = lambda m: Text.from_markup(m).plain
    assert "@Marta" in plain(wide[1]) and "today" in plain(wide[1])
    assert "@Marta" not in plain(tight[1]) and "today" in plain(tight[1])


# --------------------------------------------------------------------------- #
# TC-2506 — the presentation's notes (LLR-2506.2)
# --------------------------------------------------------------------------- #
def test_TC_2506_present_lines_write_the_name_and_never_split_it():
    rows = views.present_note_lines("Review the 40 questions with @ana.ruiz in Tuesday's sync",
                                    24, PEOPLE)
    flat = [r for _lead, r in rows]
    assert any(f"@Ana{NB}Ruiz" in r for r in flat)
    assert all(not r.endswith("@Ana") for r in flat)
    assert views.present_note_lines("with @ana.ruiz", 40) == [("", "with @ana.ruiz")]


def test_TC_2506_a_present_row_paints_each_mention_pink_bold():
    marks = views.mention_marks(PEOPLE)
    assert [len(m) for m in marks] == sorted((len(m) for m in marks), reverse=True)   # QA-10
    assert set(marks) == {"@" + p.name.replace(" ", NB) for p in PEOPLE.values()}
    row = views._present_note_markup(("• ", f"@Andrés{NB}Lima adds @Ana{NB}Ruiz"), 40, marks)
    t = Text.from_markup(row)
    st = _spans(t)
    assert st[f"@Andrés{NB}Lima"] == f"bold {PINK}" and st[f"@Ana{NB}Ruiz"] == f"bold {PINK}"
    assert views._present_note_markup(("", "plain"), 10) == views._present_note_markup(("", "plain"), 10, ())
    # code review CR-3: typed text that only starts like a name is not painted
    ana = views.mention_marks({"ana": Person("ana", "Ana")})
    t2 = Text.from_markup(views._present_note_markup(("", "mail @Anabel, ask @Ana"), 40, ana))
    pink = [(s.start, t2.plain[s.start:s.end]) for s in t2.spans if str(s.style) == f"bold {PINK}"]
    assert pink == [(t2.plain.index("ask @Ana") + 4, "@Ana")]          # only the whole word


def test_TC_2506_a_note_cut_to_one_row_still_paints_its_mention():
    """code review CR-4: the one-row cut paints the mention like every other row."""
    marks = views.mention_marks(PEOPLE)
    rows = views.present_note_lines("with @ana.ruiz\n- two\n- three", 40, PEOPLE)
    row = Text.from_markup(views._present_cut(rows, 1, 40, marks)[0])
    assert row.plain.startswith(f"with @Ana{NB}Ruiz") and "+2 lines" in row.plain
    assert _spans(row)[f"@Ana{NB}Ruiz"] == f"bold {PINK}"


def test_TC_2506_the_split_view_shows_names(tmp_path):
    fx.build(tmp_path)
    b = Board.load(fx.board_path(tmp_path, "client-a"))
    b.people = Directory.load(tmp_path / "people.json").people
    proj = next(p for p in b.projects if p.name == "Eval harness")
    frame = views.render_present(b, proj.id, "tc5", fx.TODAY, 118, 30, view="split").plain
    assert f"@Ana{NB}Ruiz" in frame and f"@Andrés{NB}Lima" in frame and "@ana.ruiz" not in frame
    b.people = {}
    assert "@ana.ruiz" in views.render_present(b, proj.id, "tc5", fx.TODAY, 118, 30,
                                               view="split").plain


# --------------------------------------------------------------------------- #
# AT-2506 — the three places in the real app
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [(118, 30), (80, 24)])
async def test_AT_2506_details_card_and_presentation_name_the_people(home, size):
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        await pilot.press("escape")                     # the home
        app.selected_task_id = "tc5"
        app.refresh_view()
        await pilot.press("enter")                      # the details
        text = await screen_text(pilot, *size)
        assert "@Ana Ruiz" in text and "@Andrés Lima" in text and "@ana.ruiz" not in text
        await pilot.press("escape")
        await pilot.press("4")                          # kanban
        text = await screen_text(pilot, *size)
        # at 80 columns the card is too narrow: the mention goes first, the due stays
        # (the round's own 80x24 capture)
        assert ("@Ana+1" in text) is (size[0] == 118) and "today" in text
        await pilot.press("R", "2")                     # the presentation, split
        text = await screen_text(pilot, *size)
        assert "@Ana Ruiz" in text and "@ana.ruiz" not in text


# --------------------------------------------------------------------------- #
# TC-2507 — a teammate's mentions in the team view
# --------------------------------------------------------------------------- #
def test_TC_2507_foreign_tasks_with_mentions_draw_in_the_team_view(tmp_path):
    from taskboard.team_sync import TeamState
    team = tmp_path / "team"
    team.mkdir()
    b = Board.load(tmp_path / "board.json")
    b.people = PEOPLE
    pid = b.projects[0].id
    import json
    (team / "team.json").write_text(json.dumps({
        "version": 1, "phases": b.phases, "projects": [{"id": pid, "name": "P"}],
        "roster": [{"id": "u1", "name": "username_subject"}, {"id": "u2", "name": "Teammate B"}]}),
        encoding="utf-8")
    weird = ["with @ana.ruiz", "@[x](p:", "@@@ @", "@[Ana](p:ana.ruiz)", "@" + "a" * 500]
    (team / "board.u2.json").write_text(json.dumps({"user": "u2", "tasks": [
        {"id": f"f{i}", "title": f"Foreign {i}", "project_id": pid, "phase": b.phases[0],
         "notes": n} for i, n in enumerate(weird)]}), encoding="utf-8")
    state = TeamState(team, user_id="u1")
    assert state.pull()
    out = views.render_people(b, False, None, today=fx.TODAY, width=118, height=60,
                              team_state=state, team_filter="todo").plain
    assert "Foreign 0" in out and "Foreign 4" in out
    foreign = [t for t, _uid in state.foreign_tasks()]
    assert len(foreign) == len(weird)
    metas = [views._card_meta(t, b, fx.TODAY, {}, None) for t in foreign]
    assert ("@Ana", "pink") in metas[0] and ("@Ana", "pink") in metas[3]
    assert all(("@Ana", "pink") not in m for m in (metas[1], metas[2], metas[4]))
    assert [modals.notes_preview(t.notes, PEOPLE).plain for t in foreign][:4] == [
        "with @Ana Ruiz", "@[x](p:", "@@@ @", "@Ana Ruiz"]


# --------------------------------------------------------------------------- #
# AT-2502 — a rename changes what is drawn, never what is stored (architect A-4)
# --------------------------------------------------------------------------- #
async def test_AT_2502_a_renamed_person_draws_the_new_name_and_the_note_keeps_the_handle(home):
    from taskboard.__main__ import open_app
    fx.build(home, last="client-a")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape", "at")             # renamed the operator's way (QA-DDR-2)
        await pilot.pause()
        scr = app.screen
        assert scr.people[scr.sel].id == "ana.ruiz"
        await pilot.press("e")
        await pilot.pause()
        await pilot.press("end", "space", "P", "r", "i", "e", "t", "o", "enter")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert app.people.people["ana.ruiz"].name == "Ana Ruiz Prieto"
        app.selected_task_id = "tc5"
        app.refresh_view()
        await pilot.press("enter")
        text = await screen_text(pilot, 118, 30)
        assert "@Ana Ruiz Prieto" in text
        assert app.board.task_by_id("tc5").notes.startswith("Review the 40 questions with @ana.ruiz")


async def test_TC_2501_another_board_draws_the_same_people(home):
    """AT-2501, qa QA-9: the directory reaches a board opened on its own — Course's details draw
    `@Ana Ruiz` from `~/.taskboard/people.json`."""
    from taskboard.__main__ import open_app
    fx.build(home, last="course")
    app = open_app(None)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("escape")
        assert app.board_id == "course"
        app.selected_task_id = "tk5"
        app.refresh_view()
        await pilot.press("enter")
        text = await screen_text(pilot, 118, 30)
        assert "Guest talk by @Ana Ruiz" in text and "@Juana Soto" in text


@pytest.mark.parametrize("text", ["@[" * 50000, "@[" + "x" * 99000, "a@" * 50000],
                         ids=["at-bracket-x50000", "one-open-link", "a-at-x50000"])
def test_TC_2507_a_crafted_note_draws_in_linear_time(text):
    """security S-1: the preview's pieces and the card's token over 100 000 crafted
    characters take well under 2 s of CPU (unbounded tokeniser: ~25 s per render; CPU
    time, so a loaded host does not make it flaky — code review CR-2)."""
    import time
    board = Board([], [Task(title="t", notes=text, id="t1")], Path("unused.json"))
    board.people = PEOPLE
    t0 = time.process_time()
    views.notes_text(text, board.people)
    views._card_meta(board.tasks[0], board, fx.TODAY, {}, None)
    rows = views.present_note_lines(text, 40, board.people)        # the full note (security)
    marks = views.mention_marks(board.people)
    for r in rows[:2000]:
        views._present_note_markup(r, 40, marks)                    # and its colouring
    assert time.process_time() - t0 < 2.0

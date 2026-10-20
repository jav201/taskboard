"""Several boards: the chip, the home and `B`.

Batch 2026-10-20-batch-01 (variant C of the multi-board round, P2):
HLR-2202 (its AT), HLR-2203, HLR-2204 / LLR-2203.1, LLR-2204.1 · TC-2203, TC-2204 ·
AT-2202, AT-2203, AT-2204 (US-2201, US-2202). Synthetic data only: the round's
boards (`tests/multi_board_fixture.py`) under this test's own temporary home.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
from rich.text import Text

import multi_board_fixture as mb
from taskboard import keymap, models, views
from taskboard.models import Board, Project, Task
from taskboard.views import _strip, vis

ROUND = Path(__file__).resolve().parents[1] / "prototypes" / "multi_board" / "out"
EVIDENCE = Path(__file__).resolve().parents[1] / ".dev-flow" / "2026-10-20-batch-01" / "evidence"
PAYLOADS = ["[@click=app.quit]x[/]", "tail\\", "[bold", "x[/]"]
NOW = datetime(2026, 10, 20, 9, 30)
KEY_ROW = "←→↑↓ move  ↵ open  n new  e name/colour  x archive  esc back  q quit"


class _Today(date):
    @classmethod
    def today(cls):
        return mb.TODAY


class _Now(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW


@pytest.fixture
def home(tmp_path, monkeypatch):
    """`Path.home()` → this test's folder; the calendar and the clock frozen at
    every module that reads them (qa-reviewer QA-2)."""
    from taskboard import app as app_module, modals
    import taskboard.__main__ as entry
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    for mod in (app_module, models, views, modals):
        monkeypatch.setattr(mod, "date", _Today)
    monkeypatch.setattr(app_module, "datetime", _Now)
    monkeypatch.setattr(entry, "datetime", _Now)
    return tmp_path / ".taskboard"


def _open(board=None):
    from taskboard.__main__ import open_app
    return open_app(board)


async def _press(pilot, *keys):
    for k in keys:
        await pilot.press(k)
        await pilot.pause()


def _row0(app) -> str:
    return app.query_one("#board").content.plain.split("\n")[0]


def _scr(app) -> str:
    return type(app.screen).__name__


_SVG = re.compile(r'<text class="[^"]*" x="([\d.]+)" y="[\d.]+" textLength="[\d.]+" '
                  r'clip-path="url\(#[^)]*-line-(\d+)\)">([^<]*)</text>')


def _svg_rows(svg: str, width: int, height: int) -> list[str]:
    """The text rows of a Textual `export_screenshot` SVG: every `<text>` of a
    terminal line placed at its column (`x / 12.2`, the export's cell width)."""
    rows = [[" "] * width for _ in range(height)]
    for x, line, body in _SVG.findall(svg):
        y, col = int(line), round(float(x) / 12.2)
        if y >= height:
            continue
        for i, ch in enumerate(html.unescape(body).replace("\xa0", " ")):
            if col + i < width:
                rows[y][col + i] = ch
    return ["".join(r).rstrip() for r in rows]


# --------------------------------------------------------------------------- #
# TC-2203 — the chip (LLR-2203.1)
# --------------------------------------------------------------------------- #
def test_TC_2203_board_chip():
    """TC-2203: nothing without a label; the name bold in board-background ink on
    its colour, a space each side and one after; cut to 24 cells; escaped."""
    assert views.board_chip(None) == ""
    t = Text.from_markup(views.board_chip(("Client · Retail RAG", "sky")))
    assert t.plain == " Client · Retail RAG  "
    span = next(s for s in t.spans if "Client" in t.plain[s.start:s.end])
    st = str(span.style)
    assert "bold" in st and "#0d1117" in st and f"on {views.HEX['sky']}" in st
    long = Text.from_markup(views.board_chip(("x" * 25, "plaid"))).plain
    assert long == " " + "x" * 23 + "… " + " "
    assert views.HEX["violet"] in views.board_chip(("A", "plaid"))
    for p in PAYLOADS:
        t = Text.from_markup(views.board_chip((p, "sky")))
        assert p in t.plain and not any(getattr(s.style, "meta", None) for s in t.spans), p


def _labelled_main(tmp_path, name="Main"):
    b = mb.build_board(tmp_path, "main")
    b.label = (name, "fuchsia")
    return b


@pytest.mark.parametrize("width", (30, 40, 80, 118, 160))
def test_TC_2203_every_view_opens_with_the_chip_at_its_width(tmp_path, width):
    """TC-2203 (architect A-19, qa QA-6): every main view's head row is exactly the
    width — a chip counted twice would leave it short — and opens with the chip
    unless the row is too narrow for its title (the literal fallback)."""
    from taskboard.app import VIEW_ORDER
    b = _labelled_main(tmp_path)
    for mode in VIEW_ORDER:
        text = views.render_view(mode, b, False, None, today=mb.TODAY, width=width, height=40)
        row0 = text.split("\n")[0]
        if mode == "setup":
            assert row0.cell_len <= width, (mode, row0.plain)
            assert row0.plain.startswith(" Main "), (mode, row0.plain)
            continue
        assert row0.cell_len == width, (mode, width, row0.cell_len, row0.plain)
        styled = any("on " + views.HEX["fuchsia"] in str(s.style) for s in row0.spans)
        if styled:
            assert row0.plain.startswith(" Main  "), (mode, row0.plain)
        else:
            assert width <= 40 and row0.plain.startswith(" Main"), (mode, width, row0.plain)


@pytest.mark.parametrize("width", (30, 40, 80, 160))
def test_TC_2203_markup_in_a_board_name_paints_literally(tmp_path, width):
    """TC-2203 (security S-3, qa QA-3): a board name holding markup — or an emoji
    shortcode (code review F2) — is literal in every view at every width, the
    narrow fallback included, and no span carries an action."""
    from taskboard.app import VIEW_ORDER
    for payload in PAYLOADS + [":bug: x"]:
        b = _labelled_main(tmp_path, payload)
        for mode in VIEW_ORDER:
            text = views.render_view(mode, b, False, None, today=mb.TODAY, width=width,
                                     height=30)
            row0 = text.split("\n")[0]
            assert not any(getattr(s.style, "meta", None) and "@click" in s.style.meta
                           for s in row0.spans), (mode, payload)
            want = (" " + views.fit(payload, 24).rstrip())[:width - 1]
            assert row0.plain.startswith(want), (mode, width, payload, row0.plain)


def test_TC_2203_no_label_is_the_base_frame(tmp_path):
    """TC-2203 (qa QA-6): with no label every view's frame equals the one
    `render_view` gave at `base_ref` (`evidence/frames-base.json`, rendered in a
    worktree at 783397e by `evidence/frames_base.py`)."""
    from taskboard.app import VIEW_ORDER
    want = json.loads((EVIDENCE / "frames-base.json").read_text(encoding="utf-8"))
    b = mb.build_board(tmp_path, "main")
    assert b.label is None
    for mode in VIEW_ORDER:
        for w in (40, 80, 118, 160):
            text = views.render_view(mode, b, False, None, today=date(2026, 10, 20), width=w,
                                     height=40)
            assert text.plain == want[f"{mode}@{w}"]["plain"], (mode, w)
            first = text.split("\n")[0]
            assert [[first.plain[s.start:s.end], str(s.style)] for s in first.spans] \
                == want[f"{mode}@{w}"]["row0_spans"], (mode, w)


def test_TC_2203_the_presentation_takes_no_chip(tmp_path):
    b = _labelled_main(tmp_path, "Chip Name")
    t = views.render_present(b, "pmr", None, mb.TODAY, 160, 40)
    assert "Chip Name" not in t.plain


# --------------------------------------------------------------------------- #
# TC-2204 — the home's renders and its screen (LLR-2204.1)
# --------------------------------------------------------------------------- #
def test_TC_2204_board_summary_counts_what_the_cards_show(tmp_path):
    """TC-2204: the counts the round's captures show, and Personal's next dues
    in date order (a late task is never next — qa QA-8)."""
    want = {"personal": (6, 1, 3, 2), "client-retail-rag": (7, 1, 2, 2),
            "course-docker": (5, 0, 2, 2), "main": (17, 3, 6, 5)}
    for bid, counts in want.items():
        s = views.board_summary(mb.build_board(tmp_path, bid), mb.TODAY)
        assert (s["open"], s["late"], s["week"], len(s["projects"])) == counts, bid
    s = views.board_summary(mb.build_board(tmp_path, "personal"), mb.TODAY)
    assert [t.id for _d, t in s["next"]] == ["tp6", "tp1", "tp4", "tp2", "tp5"]
    assert all(d >= mb.TODAY for d, _t in s["next"])


@pytest.mark.parametrize("mins, want", [(1, "just now"), (2, "2m ago"), (59, "59m ago"),
                                        (60, "1h ago"), (23 * 60 + 59, "23h ago"),
                                        (24 * 60, "1d ago")])
def test_TC_2204_ago(mins, want):
    assert views.ago((NOW - timedelta(minutes=mins)).isoformat(), NOW) == want


def test_TC_2204_ago_never():
    assert views.ago(None, NOW) == "never opened"
    assert views.ago("yesterday", NOW) == "never opened"
    # a hand-edited time with an offset is read, never a crash at start (code review F1)
    assert views.ago("2026-10-20T07:30+00:00", NOW) == "2h ago"


@pytest.mark.parametrize("inner, days, cw", [(74, 28, 2), (53, 21, 2), (34, 14, 2),
                                             (27, 21, 1), (12, 7, 1)])
def test_TC_2204_the_strip_takes_the_first_window_that_fits(inner, days, cw):
    s = {"late": 1, "by_day": {0: 1, 1: 2, 2: 3, 3: 4}}
    bars, axis = views.due_strip(s, inner, "sky", mb.TODAY)
    assert bars.cell_len == 3 + days * cw
    assert bars.plain[3:3 + 4 * cw] == "".join(g * cw for g in "▃▅▇█")
    assert axis.plain.startswith("   20")


def test_TC_2204_the_counts_row_joins_and_shortens(tmp_path):
    s = views.board_summary(mb.build_board(tmp_path, "main"), mb.TODAY)
    wide = views.home_card(s, "fuchsia", 74, 5, True, mb.TODAY).plain.split("\n")[0]
    assert wide == "17 open  ·  ▲3 late  ·  6 due this week  ·  5 projects"
    narrow = views.home_card(s, "fuchsia", 34, 1, False, mb.TODAY).plain.split("\n")[0]
    assert narrow == "17 open · ▲3 late · 6 this week"
    # inner 53 (118 columns): Personal's four parts joined are exactly 53 cells, yet
    # the round's rule (each part + 5, summed) drops the projects count — as the
    # approved `C-118-open` row 3 shows (qa QA-21)
    p = views.board_summary(mb.build_board(tmp_path, "personal"), mb.TODAY)
    row = views.home_card(p, "green", 53, 3, False, mb.TODAY).plain.split("\n")[0]
    assert row == "6 open  ·  ▲1 late  ·  3 this week"


def test_TC_2204_names_paint_literally_in_a_card(tmp_path):
    for p in PAYLOADS:
        b = Board([Project(p, id="pa")], [Task(p, project_id="pa", due_date="2026-10-21",
                                               id="ta")], tmp_path / "b.json")
        t = views.home_card(views.board_summary(b, mb.TODAY), "sky", 74, 5, True, mb.TODAY)
        assert t.plain.count(p) == 2, p
        assert not any(getattr(s.style, "meta", None) for s in t.spans)


def test_TC_2204_B_is_in_the_seat_for_every_view():
    from taskboard.app import VIEW_ORDER
    keys = [k.keys for k in keymap.KEYMAP]
    assert len(keys) == len(set(keys))
    b = next(k for k in keymap.KEYMAP if k.keys == "B")
    assert (b.action, b.label, b.universal, b.primary) == ("boards", "Boards", True, True)
    for v in VIEW_ORDER:
        assert b in keymap.bar_keys(v)
        assert keymap.key_bar_plain(160, v, "primary").startswith("? Map  ; More  q Quit  B Boards")


async def test_TC_2204_check_action_and_the_cursor(home):
    """TC-2204 (architect A-9): `boards` is released under any pushed screen; with
    the home anywhere on the stack (a modal over it too) no main action acts but
    `quit`; the cursor clamps."""
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert _scr(app) == "BoardsHome"
        assert app.check_action("add_task", ()) is False
        assert app.check_action("quit", ()) is True
        app.push_screen(models_confirm())
        await pilot.pause()
        assert app.check_action("add_task", ()) is False
        assert app.check_action("view", ("kanban",)) is False
        await _press(pilot, "escape")
        home_scr = app.screen
        await _press(pilot, "left", "left")
        assert home_scr.cursor == 0
        await _press(pilot, "down")
        assert home_scr.cursor == 2            # down: a row of two cards (code review F3)
        await _press(pilot, "left")
        assert home_scr.cursor == 1
        await _press(pilot, "up")
        assert home_scr.cursor == 0
        await _press(pilot, "down", "down", "right", "right", "right")
        assert home_scr.cursor == 3
        await _press(pilot, "escape")
        assert _scr(app) == "Screen"
        assert app.check_action("boards", ()) is True
        await _press(pilot, "P")
        assert app.check_action("boards", ()) is False


def models_confirm():
    from taskboard.modals import ConfirmModal
    return ConfirmModal("A question", confirm="Yes")


async def test_TC_2204_seven_boards_scroll_and_a_missing_file(home):
    """TC-2204: seven boards — the cursor's card stays in view; a board whose file
    is missing reads `file missing`, `enter` warns, keeps the home and writes
    nothing; the home writes no board file."""
    reg_path = mb.build(home, "personal")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    for i in range(3):
        p = home / "boards" / f"extra-{i}" / "board.json"
        if i < 2:
            mb.build_board(home, "personal").__class__([], [], p).save()
        reg["boards"].append({"id": f"extra-{i}", "name": f"Extra {i}", "color": "blue",
                              "path": str(p), "last_opened": None, "archived": False})
    reg_path.write_text(json.dumps(reg), encoding="utf-8")
    before = {p: p.read_bytes() for p in home.rglob("*") if p.is_file()}
    app = _open()
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        scr = app.screen
        assert [e.id for e in scr.entries][-1] == "extra-2"
        await _press(pilot, "down", "down", "down")
        assert scr.cursor == 6
        card = scr.query_one(f"#card-{scr.cursor}")
        assert card.region.y >= 0 and card.region.bottom <= 30, card.region
        scr.cursor = 6
        scr._paint()
        await pilot.pause()
        assert "file missing" in scr.query_one("#card-6").content.plain
        await _press(pilot, "enter")
        assert _scr(app) == "BoardsHome"
        assert any("its file is missing" in n.message for n in app._notifications)
    assert not (home / "boards" / "extra-2").exists()
    after = {p: p.read_bytes() for p in home.rglob("*") if p.is_file() and p.name != "boards.json"}
    assert {p: b for p, b in before.items() if p.name != "boards.json"} == after


async def test_TC_2204_enter_closes_the_home_before_the_board_starts(home):
    """TC-2204 (architect A-9): a team board with no identity opens its identity
    picker on `enter` — the picker is the active screen and no home is left."""
    mb.build(home, "personal")
    shared = home.parent / "team"
    shared.mkdir()
    (shared / "team.json").write_text(json.dumps({
        "version": 1, "phases": ["Backlog", "Next", "Doing", "Review", "Done"],
        "roster": [{"id": "u1", "name": "Member One", "hue": "sky"}], "projects": []}),
        encoding="utf-8")
    p = home / "boards" / "client-retail-rag" / "board.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["settings"]["team_shared_dir"] = str(shared)
    p.write_text(json.dumps(data), encoding="utf-8")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "right", "enter")
        assert _scr(app) == "TeamIdentityPicker"
        assert not any(type(s).__name__ == "BoardsHome" for s in app.screen_stack)


async def test_TC_2204_the_home_reads_an_unreadable_board_without_copying_it(home):
    mb.build(home, "personal")
    bad = home / "boards" / "course-docker" / "board.json"
    bad.write_text("{oops", encoding="utf-8")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert _scr(app) == "BoardsHome"
        idx = [e.id for e in app.screen.entries].index("course-docker")
        assert "file unreadable" in app.screen.query_one(f"#card-{idx}").content.plain
    assert not (bad.parent / "board.json.corrupt").exists()


# --------------------------------------------------------------------------- #
# AT-2202 — switching boards (HLR-2202)
# --------------------------------------------------------------------------- #
async def test_AT_2202_switching_boards_in_place(home):
    """AT-2202 (US-2201): the home → Personal; `B` → Client: its work on screen, its
    history in its own folder; the next start returns to it; `--board` adds one."""
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert _scr(app) == "BoardsHome"
        await _press(pilot, "escape")
        plain = app.query_one("#board").content.plain
        assert "Renew passport" in plain
        await _press(pilot, "B", "right", "enter")
        plain = app.query_one("#board").content.plain
        assert "Hybrid search index" in plain and "Renew passport" not in plain
        app.selected_task_id = "tc1"
        await _press(pilot, "left_square_bracket")
    hist = home / "boards" / "client-retail-rag" / "history.jsonl"
    lines = [json.loads(x) for x in hist.read_text(encoding="utf-8").splitlines()]
    assert [(r["task"], r["from"], r["to"]) for r in lines] == [("tc1", "Done", "Review")]
    assert not (home / "boards" / "personal" / "history.jsonl").exists()
    reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
    assert reg["last"] == "client-retail-rag"
    assert next(e for e in reg["boards"]
                if e["id"] == "client-retail-rag")["last_opened"] == "2026-10-20T09:30"
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        cards = list(app.screen.query("BoardCard"))
        on = [c for c in cards if str(c.border_title).startswith("▶ ")]
        assert len(on) == 1 and "Client · Retail RAG" in str(on[0].border_title)
    side = home.parent / "side" / "notes.json"
    side.parent.mkdir()
    Board([], [], side, {"seen_view_renumber_2026_07": True}).save()
    app = _open(str(side))
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert _scr(app) == "BoardsHome"
        await _press(pilot, "escape")
        assert _row0(app).startswith(" notes  ◆ TASKBOARD"), _row0(app)
    reg = json.loads((home / "boards.json").read_text(encoding="utf-8"))
    e = next(e for e in reg["boards"] if e["id"] == "notes")
    assert Path(e["path"]).resolve() == side.resolve()


# --------------------------------------------------------------------------- #
# AT-2203 — the chip in every view (HLR-2203)
# --------------------------------------------------------------------------- #
async def test_AT_2203_the_chip_in_every_view(home, tmp_path):
    """AT-2203 (US-2202): ` Personal ` opens every view's head row; Client's head
    row is the round's `C-160-switched` row 0; none in the presentation; none
    with one board."""
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "escape")
        assert _row0(app).startswith(" Personal  ◆ TASKBOARD"), _row0(app)
        for key in "1234567890":
            await _press(pilot, key)
            assert _row0(app).startswith(" Personal "), (key, _row0(app))
        await _press(pilot, "escape", "1", "B", "right", "enter")
        want = _svg_rows((ROUND / "C-160-switched.svg").read_text(encoding="utf-8"), 160, 45)
        assert _row0(app).rstrip() == want[0], (_row0(app), want[0])
        app.selected_task_id = "tc3"
        await _press(pilot, "R")
        frame = app.screen.query_one("#present-frame").content.plain
        assert "Client · Retail RAG" not in frame
    solo = tmp_path / "solo"
    Board([Project("Solo", id="ps")], [], solo / ".taskboard" / "board.json").save()
    from taskboard.app import TaskboardApp
    app = TaskboardApp(board_path=str(solo / ".taskboard" / "board.json"))
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        assert _row0(app).startswith("◆ TASKBOARD")


# --------------------------------------------------------------------------- #
# AT-2204 — the home (HLR-2204)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size, svg", [((160, 45), "C-160-open.svg"),
                                       ((118, 30), "C-118-open.svg"),
                                       ((80, 24), "C-80-open.svg")])
async def test_AT_2204_the_home_is_the_approved_capture(home, size, svg):
    """AT-2204 (US-2202): at start over the round's four boards the home's rows
    equal the round's approved C capture but its key row, which loses option D's
    `A all boards` and reads the shipped keys."""
    w, h = size
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=size) as pilot:
        for _ in range(4):
            await pilot.pause()
        assert _scr(app) == "BoardsHome"
        got = _svg_rows(app.export_screenshot(), w, h)
    want = _svg_rows((ROUND / svg).read_text(encoding="utf-8"), w, h)
    diff = [(y, g, x) for y, (g, x) in enumerate(zip(got[:-1], want[:-1])) if g != x]
    assert not diff, diff
    assert got[-1] == " " + KEY_ROW


async def test_AT_2204_B_and_the_keys_the_home_holds(home):
    """AT-2204: `3` and `a` do nothing on the home; `B` opens it from a view but not
    over the presentation or the projects modal; the bar and `?` list `B`."""
    mb.build(home, "personal")
    app = _open()
    async with app.run_test(size=(160, 45)) as pilot:
        await pilot.pause()
        await _press(pilot, "3", "a", "escape")
        assert _scr(app) == "Screen"
        assert _row0(app).startswith(" Personal  ◆ TASKBOARD · grid"), _row0(app)
        await _press(pilot, "B")
        assert _scr(app) == "BoardsHome"
        await _press(pilot, "escape")
        app.selected_task_id = "tp1"
        await _press(pilot, "R")
        assert _scr(app) == "PresentScreen"
        await _press(pilot, "B")
        assert _scr(app) == "PresentScreen"
        await _press(pilot, "escape", "P")
        assert _scr(app) == "ProjectPicker"
        await _press(pilot, "B")
        assert _scr(app) == "ProjectPicker"
        await _press(pilot, "escape")
        bar = keymap_plain(app)
        assert bar.startswith("? Map  ; More  q Quit  B Boards"), bar
        await _press(pilot, "question_mark")
        assert "Boards" in _all_text(app.screen)


def keymap_plain(app) -> str:
    c = app.query_one("#keybar").content
    return c.plain if hasattr(c, "plain") else Text.from_markup(str(c)).plain


def _all_text(screen) -> str:
    out = []
    for w in screen.query("*"):
        c = getattr(w, "content", None)
        if c is not None:
            out.append(c.plain if hasattr(c, "plain") else str(c))
    return "\n".join(out)

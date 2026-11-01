"""`n` — the capture view: a focused notes pad whose notes become tasks (Inc K, dev-flow-v3-beta;
HLR-4401, HLR-4402 (drawing and keys), HLR-4403 (the rail), HLR-4404, HLR-4405 (the view's side),
HLR-4406, HLR-4408 (the view's side), HLR-4409 · AT-4401..AT-4408).

WHY. US-4401: the owner (`username_subject`) types notes during a meeting, separates them with a
`____` line, and turns each into a task in the project the pad suggests — on any board, or in a new
project made right there — without a setup dialog. A capture tool used in a hurry must never lose a
note (a failed write keeps the text and says so; a dump either lands whole or leaves the note in
the pad), must never put a note on the wrong board silently (the option shown is the option used,
even after the suggestions are rebuilt), must never type a key's letter into the pad when a key was
meant (every pad key is a priority binding, P-V-2), and must never write a board, a history, the
people or the marks directory just by being opened. Every pad key that is shown must work in a real
terminal (R1-1: `alt+l`, not `alt+enter`; P-V-1: `tab`, not `alt+b`).

Layer 0 drives `taskboard.inbox.dump_note` on fixture S (graph-proto-S); the pilots drive the
shipped app on fixture F (graph-proto-T §Fixture F, two registry boards, `Path.home` redirected) at
118x30 and 80x24 through its keys and dialogs. Exact strings, cell counts and colours are the
examples of graph-proto-V / graph-interfaces; where an example disagreed with a requirement the
test follows the requirement (noted in the test's docstring).

RED on the base revision (545c18a): `taskboard.inbox` and `taskboard.suggest` do not exist, the
keymap has no `n` entry, `n` opens nothing and the README has no `n | Capture` row. Every new name is
reached through `capture_fixture` (`fx.inbox()`, `fx.need`, `fx.app_class`), and every pilot asserts
the capture view opened right after `n` (`fx.open_capture`), so each test fails on an assertion
with a message, never at collection. Guards that PASS on base by design: TC-4415 (the `n` keys of
the boards home, the people directory and the marks manager act as they act at 545c18a — the
mutant it catches, an app-level priority `n`, is the increment's own).

Synthetic data only; the real clock (the store's 7-day keep and the app's stamps read one clock).
"""
from __future__ import annotations
import json, os, re
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path
import pytest
from textual import events
import capture_fixture as fx
from capture_fixture import home  # noqa: F401
from taskboard import app as app_module, boards, history, keymap, models
from taskboard.models import Board, Project, Task

W118, W80 = fx.W118, fx.W80
N1, N2, N3, N4, N5 = fx.N1, fx.N2, fx.N3, fx.N4, fx.N5
N2T = "Volume lab fails on WSL\nthe oracle script expects /mnt/c"     # N2 without its image line
EVAL_NOTE = "eval rubric for the oracle pilot"     # Eval harness 0.4379, Pilot rollout 0.1578
WEAK3 = "store rubric"                             # [+ new project, Pilot rollout, Eval harness]
GHOST = ["first line → the task's title", "next lines → its notes", "─" * 24,
         "____ ↵ starts the next note"]
HINT = "____ ↵ new note · alt+l divider"
CAPTURE_KEYS = [("alt+d", "dump"), ("alt+o", "other"), ("alt+n", "new project"),
                ("alt+a", "review"), ("alt+i", "image"), ("alt+u", "undo"), ("esc", "close")]
DIVIDER_NOTICE = ("That ____ line divides notes: the text above and below it dump as two tasks. "
                  "alt+l inserts one.")
DUMP_COURSE = "Dumped → Module 4 · Volumes · Course   ·   alt+u undo"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
@asynccontextmanager
async def capture(home, pad: str | None = None, size=W118, cursor=None, dumped=None,
                  build: dict | None = None, before: tuple = (), divider_notice=None):
    """Fixture F written under `home`, the store's pad (when given) written before the app
    starts, the app started as `taskboard` starts it, the home left (`escape`), `before`
    keys, `n`; yields (app, pilot, paths) with the capture view on top."""
    p = fx.build_f(home, **(build or {}))
    if pad is not None or dumped is not None or divider_notice is not None:
        fx.write_store(home, pad=pad or "", dumped=dumped, divider_notice=divider_notice)
    app = fx.open_f_app()
    async with app.run_test(size=size) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app, *before)
        if cursor is not None:
            await fx.cursor_to(pilot, app, *cursor)
        yield app, pilot, p


def pad_text(app) -> str:
    return fx.pad_of(app).text


def title_rows(lines: list[str]) -> list[str]:
    return [x for x in lines if re.match(r"^[ ▌]\d+ ", x)]


def arrow_rows(lines: list[str]) -> list[str]:
    return [x for x in lines if re.match(r"^[ ▌]  → ", x)]


def trimmed(lines: list[str]) -> list[str]:
    out = list(lines)
    while out and not out[-1].strip():
        out.pop()
    return out


def one(app, text: str):
    """Exactly one notification `text`, shown as literal text under the title `Capture`."""
    got = fx.notified(app, text)
    assert len(got) == 1, f"expected one notice {text!r}, got {fx.messages(app)}"
    n = got[0]
    assert n.title == "Capture" and n.markup is False, (n.title, n.markup)
    return n


def starting(app, prefix: str):
    return [m for m in fx.messages(app) if m.startswith(prefix)]


def holding(app, part: str):
    return [m for m in fx.messages(app) if part in m]


def field(app):
    return fx.by_id(app, "cap-new")


def field_open(app) -> bool:
    return field(app).has_class("on")


def border_title(widget) -> str:
    t = widget.border_title
    return getattr(t, "plain", None) or str(t or "")


def s_dump(tmp_path, monkeypatch):
    """Fixture S (graph-proto-S head) with task ids t0000001, t0000002, …"""
    p = fx.build_s(tmp_path)
    ids = fx.seq_ids(monkeypatch)
    return p, ids


def target(p, which: str = "C", live=None):
    DumpTarget = fx.need("inbox", "DumpTarget")
    if which == "C":
        return DumpTarget(p["C"], "Course", None)
    return DumpTarget(p["A"], "Client A", live)


def dump(tgt, note: str, folder, project_id=None, new_name=None, project_name=""):
    return fx.need("inbox", "dump_note")(tgt, project_id, new_name, note, folder, project_name)


def file_bytes(path: Path) -> bytes:
    return Path(path).read_bytes()


def write_lock(path: Path) -> Path:
    """A fresh foreign lock beside `path` (another taskboard holds it)."""
    lock = Path(path).resolve()
    lock = lock.with_name(lock.name + ".lock")
    lock.write_bytes(b"foreign-holder-token")
    return lock


def task_rec(path: Path, title: str) -> dict | None:
    return next((t for t in fx.tasks_of(path) if t["title"] == title), None)


def project_recs(path: Path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["projects"]


def png(path: Path, data: bytes = b"\x89PNG\r\n\x1a\nsynthetic") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def spy_suggest(monkeypatch) -> list[str]:
    """Every scored text the view hands `taskboard.app.suggest` (G-V calls it through the
    module attribute, graph-proto-V options_for)."""
    calls: list[str] = []
    real = getattr(app_module, "suggest", None)

    def wrapper(note, corpus):
        calls.append(note)
        if real is None:
            pytest.fail("taskboard.app.suggest missing (not built yet)")
        return real(note, corpus)
    monkeypatch.setattr(app_module, "suggest", wrapper, raising=False)
    return calls


async def dump_at(pilot, app, row: int, col: int = 0, key: str = "alt+d"):
    await fx.cursor_to(pilot, app, row, col)
    await fx.press(pilot, key)
    await pilot.pause(0.1)


def row_of(text: str, needle: str) -> int:
    """The pad row index of the first line starting with `needle`."""
    for i, line in enumerate(text.split("\n")):
        if line.startswith(needle):
            return i
    raise AssertionError(f"{needle!r} not in the pad {text!r}")


# --------------------------------------------------------------------------- #
# HLR-4401 — the view and its keys
# --------------------------------------------------------------------------- #
def test_TC_4401_n_is_one_global_key_declared_after_N_off_the_bar():
    """TC-4401 (LLR-4401.1): exactly one KEYMAP entry `n` → `capture`, label `Capture`, off the
    bar, no view scope, not priority, directly after `N` — one seat for keys (R0-1). The key-law
    tests of tests/test_keymap.py stay GREEN with it (5 run here). NC: entry missing."""
    found = [k for k in keymap.KEYMAP if k.keys == "n"]
    assert len(found) == 1, f"KEYMAP entries with keys 'n': {found}"
    k = found[0]
    assert (k.action, k.label, k.bar, k.views, k.priority) == ("capture", "Capture", False,
                                                               None, False)
    keys = [x.keys for x in keymap.KEYMAP]
    assert keys.index("n") == keys.index("N") + 1
    import test_keymap as laws
    for law in ("test_every_binding_the_app_has_comes_from_the_seat",
                "test_every_shown_key_has_a_real_action_on_the_app",
                "test_the_seat_has_no_duplicate_keys_or_labels",
                "test_every_key_alias_is_bound_not_just_the_shown_one",
                "test_no_two_shown_keys_share_an_action"):
        getattr(laws, law)()


async def test_TC_4402_n_on_the_main_screen_opens_the_capture_view(home):
    """TC-4402 (LLR-4401.2): fixture F, `escape` (leave the home), `n` → app.screen is a
    CaptureView. NC: `n` unbound."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await fx.leave_home(pilot)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert isinstance(app.screen, fx.app_class("CaptureView"))


async def test_TC_4403_every_printable_key_types_into_the_pad(home):
    """TC-4403 (LLR-4401.3): `nNAqjkhlBuv@#?;` — each a global key elsewhere — typed into an
    empty pad gives exactly that text; the view stays on top; no board file is written (3/3).
    NC: the pad not focused at open (then `q` quits). ARCH-5: a holding-tuple mutant cannot fire
    above a focused TextArea, so focus is the control."""
    async with capture(home) as (app, pilot, p):
        before = fx.shas(p)
        await fx.type_text(pilot, "nNAqjkhlBuv@#?;")
        assert pad_text(app) == "nNAqjkhlBuv@#?;"
        assert fx.on_capture(app), fx.screen_names(app)
        assert fx.shas(p)[:4] == before[:4], "a key typed in the pad wrote a board or a history"


async def test_TC_4404_esc_closes_the_view(home):
    """TC-4404 (LLR-4401.4): the name field closed and nothing unsaved, `escape` → the main
    screen is on top. NC: `esc` unbound."""
    async with capture(home) as (app, pilot, p):
        await fx.press(pilot, "escape")
        await pilot.pause(0.1)
        assert fx.captures_on_stack(app) == 0
        assert len(app.screen_stack) == 1, fx.screen_names(app)


async def test_TC_4405_the_pad_has_focus_with_the_cursor_at_the_end(home):
    """TC-4405 (LLR-4401.5): store pad "a\\nb" → app.focused is the pad and the cursor is at
    document.end (1, 1) — the owner types at once, after what is there (2/2). NC: (0, 0)."""
    async with capture(home, pad="a\nb") as (app, pilot, p):
        pad = fx.pad_of(app)
        assert app.focused is pad
        assert pad.cursor_location == pad.document.end == (1, 1)


async def test_TC_4406_the_pad_opens_with_the_stored_text(home):
    """TC-4406 (LLR-4401.6): store pad "a\\n____\\nb" → the pad holds exactly that. NC: empty."""
    async with capture(home, pad="a\n____\nb") as (app, pilot, p):
        assert pad_text(app) == "a\n____\nb"


async def test_TC_4407_wide_the_rail_is_a_50_cell_column_right_of_the_pad(home):
    """TC-4407 (LLR-4401.7): at 118x30 the rail's region x 68, width 50; the pad's x 0 (2/2,
    P-V-5). NC: the rail below the pad."""
    async with capture(home, pad=N1) as (app, pilot, p):
        rail = fx.by_id(app, "cap-rail-box").region
        assert (rail.x, rail.width) == (68, 50), rail
        assert fx.pad_of(app).region.x == 0


async def test_TC_4408_narrow_the_rail_sits_below_the_pad_with_the_cursors_note_only(home):
    """TC-4408 (LLR-4401.8): at 80x24, pad N1|N2|N3 with the cursor in N2 → the rail's region
    starts below the pad's last row, is 7 rows high, and holds exactly 1 note title of the 3 —
    N2's (3/3). NC: every note in the narrow rail."""
    pad = f"{N1}\n____\n{N2}\n____\n{N3}"
    async with capture(home, pad=pad, size=W80, cursor=(3, 2)) as (app, pilot, p):
        rail = fx.by_id(app, "cap-rail-box").region
        prow = fx.pad_of(app).region
        assert rail.y > prow.y + prow.height - 1, (rail, prow)
        assert rail.height == 7
        titles = title_rows(fx.rail_lines(app))
        assert titles == ["▌2 Volume lab fails on WSL  ▣ 1"], fx.rail_lines(app)
        assert trimmed(fx.rail_lines(app))[:3] == [
            "▌2 Volume lab fails on WSL  ▣ 1", "▌  → Module 4 · Volumes · Course ▰▰▰",
            "▌    why volume · oracle · script"]


@pytest.mark.parametrize("pad, expected", [
    (f"{N1}\n____\n{N2}\n____\n{N3}", "CAPTURE  3 notes · suggestions read every board"),
    (N1, "CAPTURE  1 note · suggestions read every board"),
])
async def test_TC_4409_the_head_row_counts_the_notes(home, pad, expected):
    """TC-4409 (LLR-4401.9): 3 notes → `CAPTURE  3 notes · …`; 1 note → `1 note` (2/2).
    NC: a fixed `notes`."""
    async with capture(home, pad=pad) as (app, pilot, p):
        assert fx.head(app) == expected


@pytest.mark.parametrize("size", [W80, W118])
async def test_TC_4410_the_key_row_names_every_pad_key(home, size):
    """TC-4410 (LLR-4401.10): the key row is `keymap.key_line(CAPTURE_KEYS, w − 2)` (words go
    first, keys never): at 80x24 all 7 key glyphs, at 118x30 all 7 words (2/2, P-V-6). NC: no
    `alt+u`."""
    async with capture(home, size=size) as (app, pilot, p):
        row = fx.keys_row(app)
        assert row == keymap.key_line(CAPTURE_KEYS, size[0] - 2).plain
        for key, word in CAPTURE_KEYS:
            assert key in row
            if size == W118:
                assert f"{key} {word}" in row
        if size == W80:
            assert row == ("alt+d dump   alt+o other   alt+n new project   alt+a   alt+i   "
                           "alt+u   esc")


async def test_TC_4411_capture_is_refused_while_a_modal_is_open(home):
    """TC-4411 (LLR-4401.11): `check_action("capture", ())` False with a ModalScreen (the task
    editor) on the stack and True with none; `n` typed in the editor's title is typed, and no
    capture view opens (3/3). NC: `capture` not gated: arm 1."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await fx.leave_home(pilot)
        assert app.check_action("capture", ()) is True
        await fx.press(pilot, "a")
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "TaskModal", fx.screen_names(app)
        assert app.check_action("capture", ()) is False
        await fx.press(pilot, "n")
        assert fx.captures_on_stack(app) == 0
        from textual.widgets import Input
        title = app.screen.query(Input).first()
        assert "n" in title.value


async def test_TC_4412_the_view_holds_the_seat(home):
    """TC-4412 (LLR-4401.12): with the capture view open, `add_task`, `delete`, `archive` are
    refused, `quit` is not; the arrows move the PAD cursor and leave app.selected_task_id as it
    was (4/4; ARCH-9: `cursor` is refused by the pushed-screen clause anyway). NC: CaptureView
    missing from the holding tuple: the `archive` arm."""
    async with capture(home, pad="abc\ndef", cursor=(0, 1)) as (app, pilot, p):
        for action in ("add_task", "delete", "archive"):
            assert app.check_action(action, ()) is False, action
        assert app.check_action("quit", ()) is True
        sel = app.selected_task_id
        pad = fx.pad_of(app)
        await fx.press(pilot, "down")
        assert pad.cursor_location == (1, 1)
        await fx.press(pilot, "right")
        assert pad.cursor_location == (1, 2)
        await fx.press(pilot, "left", "up")
        assert pad.cursor_location == (0, 1)
        assert app.selected_task_id == sel


def test_TC_4413_the_readme_key_table_carries_the_capture_row():
    """TC-4413 (LLR-4401.13): the seat's README test stays GREEN, and the main key table holds
    a line starting ``| `n` | Capture |`` (2/2). P-V-4: the home table's `n` (New board) already
    satisfies the seat test, so the row itself is the control."""
    import test_keymap as laws
    laws.test_the_readme_keybinding_table_matches_the_seat()
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    assert any(line.startswith("| `n` | Capture |") for line in readme.splitlines())


async def test_TC_4414_n_brings_one_capture_view_to_the_top(home):
    """TC-4414 (LLR-4401.14): off the home, `N` then `n` → the capture view on top and exactly
    one on the stack; `capture` run again with it on top changes nothing; `escape`, `n` → still
    exactly one; `A`, `n` from the main screen → the view over the agenda (3/3). NC: `capture`
    not in check_action's always-allowed tuple."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await fx.leave_home(pilot)
        await fx.press(pilot, "N")
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "AddedList", fx.screen_names(app)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert fx.on_capture(app) and fx.captures_on_stack(app) == 1, fx.screen_names(app)
        assert fx.screen_names(app) == ["Screen", "AddedList", "CaptureView"]
        await app.run_action("capture")
        await pilot.pause()
        assert fx.screen_names(app) == ["Screen", "AddedList", "CaptureView"]
        await fx.press(pilot, "escape")
        await pilot.pause(0.1)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert fx.on_capture(app) and fx.captures_on_stack(app) == 1, fx.screen_names(app)
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await fx.leave_home(pilot)
        await fx.press(pilot, "A")
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "AllBoardsAgenda", fx.screen_names(app)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert fx.screen_names(app) == ["Screen", "AllBoardsAgenda", "CaptureView"]


async def test_TC_4415_the_other_n_keys_keep_their_meaning(home):
    """TC-4415 (LLR-4401.15) — a GUARD, GREEN on base by design: `n` on the boards home opens its
    new-board form, on the people directory its add-person form, on the marks manager its
    add-class form, and none opens a capture view (3/3). NC: the app's `n` made a priority
    binding (it would beat the screens' own `n`)."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "BoardsHome", fx.screen_names(app)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "BoardForm", fx.screen_names(app)
        assert fx.captures_on_stack(app) == 0
        await fx.press(pilot, "escape")
        await fx.press(pilot, "escape")
        await pilot.pause(0.1)
        for opener, form in (("@", "PersonForm"), ("#", "MarkForm")):
            await fx.press(pilot, opener)
            await pilot.pause(0.2)
            await fx.press(pilot, "n")
            await pilot.pause(0.2)
            assert type(app.screen).__name__ == form, (opener, fx.screen_names(app))
            assert fx.captures_on_stack(app) == 0
            await fx.press(pilot, "escape")
            await pilot.pause(0.1)
            await fx.press(pilot, "escape")
            await pilot.pause(0.1)


async def test_TC_4416_an_empty_pad_shows_no_notes_yet(home):
    """TC-4416 (LLR-4401.16): empty pad → the rail reads `no notes yet`. NC: a blank rail."""
    async with capture(home) as (app, pilot, p):
        assert trimmed(fx.rail_lines(app)) == ["no notes yet"]


async def test_TC_4417_narrow_with_the_cursor_in_no_note(home):
    """TC-4417 (LLR-4401.17, P-V-7): at 80x24, pad "a\\n____\\n" with the cursor on row 2 (the
    empty part being started) → the rail reads `no note under the cursor`. NC: the first note."""
    async with capture(home, pad="a\n____\n", size=W80, cursor=(2, 0)) as (app, pilot, p):
        assert trimmed(fx.rail_lines(app)) == ["no note under the cursor"]


async def test_TC_4418_the_terminal_form_of_an_alt_key_types_nothing(home):
    """TC-4418 (LLR-4401.18, P-V-2): a real terminal sends `ESC o` as Key("alt+o", "o") — a
    printable key a non-priority binding would let the pad type. Posted through the driver:
    `alt+o` → pad "abc"; `alt+u` on an empty `dumped` → pad "abc" and `Nothing to undo.`; every
    CaptureView binding has priority=True (3/3). NC: `alt+o` non-priority → "abco"."""
    async with capture(home, pad="abc", cursor=(0, 1)) as (app, pilot, p):
        await fx.post_key(pilot, "alt+o", "o")
        assert pad_text(app) == "abc"
        await fx.post_key(pilot, "alt+u", "u")
        assert pad_text(app) == "abc"
        one(app, "Nothing to undo.")
        view = fx.app_class("CaptureView")
        bindings = list(view.BINDINGS)
        assert bindings and all(getattr(b, "priority", False) is True for b in bindings), bindings


async def test_TC_4419_capture_is_refused_under_the_boards_home(home):
    """TC-4419 (LLR-4401.19, ARCH-3): a registry of 2 boards starts with the home on top →
    `check_action("capture", ())` False; `N` from the home, then `n` → no capture view and the
    board files' bytes unchanged (the open board has not started: a dump would write it before
    its start-up backup); `escape` (the board starts), `N`, `n` → a capture view (3/3)."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await pilot.pause()
        assert type(app.screen).__name__ == "BoardsHome", fx.screen_names(app)
        assert app.check_action("capture", ()) is False
        before = [fx.sha(p["A"]), fx.sha(p["C"])]
        await fx.press(pilot, "N")
        await pilot.pause(0.2)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert fx.captures_on_stack(app) == 0, fx.screen_names(app)
        assert [fx.sha(p["A"]), fx.sha(p["C"])] == before
        await fx.press(pilot, "escape")
        await pilot.pause(0.1)
        if type(app.screen).__name__ == "BoardsHome":
            await fx.press(pilot, "escape")
            await pilot.pause(0.1)
        await fx.press(pilot, "N")
        await pilot.pause(0.2)
        await fx.press(pilot, "n")
        await pilot.pause(0.2)
        assert fx.on_capture(app), fx.screen_names(app)


# --------------------------------------------------------------------------- #
# HLR-4402 — the divider, its rule and its hints (the view's side)
# --------------------------------------------------------------------------- #
def _divider_screen_row(app, doc_row: int) -> list[tuple[str, str | None]]:
    pad = fx.pad_of(app)
    r = pad.content_region
    return fx.painted(app)[r.y + doc_row][r.x:r.x + r.width]


@pytest.mark.parametrize("size, width", [(W118, 64), (W80, 76)])
async def test_TC_4436_a_divider_off_the_cursor_is_a_full_width_rule(home, size, width):
    """TC-4436 (LLR-4402.6): "a\\n____\\nb", cursor (2, 1) → the screen row of line 1 holds `─`
    in every content cell of the pad (64 at 118x30, 76 at 80x24, P-V-1) and no `_` (2/2). NC: the
    raw underscores drawn."""
    async with capture(home, pad="a\n____\nb", size=size, cursor=(2, 1)) as (app, pilot, p):
        cells = _divider_screen_row(app, 1)
        assert fx.pad_of(app).content_region.width == width
        text = "".join(c for c, _ in cells)
        assert text == "─" * width, repr(text)
        assert "_" not in text


async def test_TC_4437_the_cursors_divider_shows_its_raw_text(home):
    """TC-4437 (LLR-4402.7): the cursor on the divider line → its row holds `____` and no `─`, so
    it stays editable. NC: always the rule."""
    async with capture(home, pad="a\n____\nb", cursor=(1, 0)) as (app, pilot, p):
        text = "".join(c for c, _ in _divider_screen_row(app, 1))
        assert "____" in text and "─" not in text, repr(text)


async def test_TC_4439_alt_l_inserts_a_divider_after_the_cursors_line(home):
    """TC-4439 (LLR-4402.9): "abc", cursor (0, 1), `alt+l` → "abc\\n____\\n", cursor (2, 0); with a
    following line "abc\\nd" → "abc\\n____\\n\\nd", cursor (2, 0) (2/2). NC: inserted at the cursor,
    splitting the line."""
    async with capture(home, pad="abc", cursor=(0, 1)) as (app, pilot, p):
        await fx.press(pilot, "alt+l")
        pad = fx.pad_of(app)
        assert (pad.text, pad.cursor_location) == ("abc\n____\n", (2, 0))
        await fx.set_pad(pilot, app, "abc\nd", cursor=(0, 1))
        await fx.press(pilot, "alt+l")
        assert (pad.text, pad.cursor_location) == ("abc\n____\n\nd", (2, 0))


async def test_TC_4440_alt_l_on_a_blank_line_writes_the_divider_there(home):
    """TC-4440 (LLR-4402.10): "a\\n", cursor (1, 0) → "a\\n____\\n", cursor (2, 0). NC: a blank line
    kept above the divider."""
    async with capture(home, pad="a\n", cursor=(1, 0)) as (app, pilot, p):
        await fx.press(pilot, "alt+l")
        pad = fx.pad_of(app)
        assert (pad.text, pad.cursor_location) == ("a\n____\n", (2, 0))


@pytest.mark.parametrize("size", [W118, W80])
async def test_TC_4441_the_hint_row_shows_in_every_state(home, size):
    """TC-4441 (LLR-4402.11, R1-1): the hint row reads `____ ↵ new note · alt+l divider` with an
    empty pad, with 3 notes and with the name field open, at 118x30 and 80x24 (4/4). NC: hidden
    once a divider exists."""
    async with capture(home, size=size) as (app, pilot, p):
        hint = fx.by_id(app, "cap-hint")
        assert fx.hint(app) == HINT
        assert fx.region_rows(app, hint)[0].strip() == HINT
        await fx.set_pad(pilot, app, f"{N1}\n____\n{N2}\n____\n{N3}")
        await pilot.pause(0.2)
        assert fx.hint(app) == HINT and fx.region_rows(app, hint)[0].strip() == HINT
        await fx.press(pilot, "alt+n")
        await pilot.pause(0.1)
        assert field_open(app)
        assert fx.hint(app) == HINT and fx.region_rows(app, hint)[0].strip() == HINT


@pytest.mark.parametrize("size", [W118, W80])
async def test_TC_4442_an_empty_pad_shows_the_ghost_example(home, size):
    """TC-4442 (LLR-4402.12): an empty pad shows four placeholder lines in order — `first line →
    the task's title`, `next lines → its notes`, 24 × `─`, `____ ↵ starts the next note`; after one
    typed character none of them (2/2). NC: no rule line."""
    async with capture(home, size=size) as (app, pilot, p):
        pad = fx.pad_of(app)
        rows = [r.strip() for r in fx.region_rows(app, pad)]
        assert rows[:4] == GHOST, rows[:5]
        await fx.type_text(pilot, "x")
        rows = [r.strip() for r in fx.region_rows(app, pad)]
        assert rows[0] == "x"
        assert not any(g in r for g in GHOST for r in rows), rows[:5]


async def test_TC_4443_the_divider_notice_shows_once_per_session(home):
    """TC-4443 (LLR-4402.13): the first `____` drawn as a rule shows exactly one notice `That ____
    line divides notes: …`, title `Capture`, markup False; a second divider in the same session
    shows none (2/2). NC: a notice on every divider."""
    async with capture(home) as (app, pilot, p):
        await fx.type_text(pilot, "a\n____\n")
        await pilot.pause(0.2)
        one(app, DIVIDER_NOTICE)
        await fx.type_text(pilot, "b\n____\n")
        await pilot.pause(0.2)
        one(app, DIVIDER_NOTICE)


async def test_TC_4444b_showing_the_divider_notice_sets_the_stored_flag(home):
    """TC-4444b (LLR-4402.14, pilot): after the notice, inbox.json read back holds
    `"divider_notice": true` — a one-time notice that came back every session would not be one
    (R0-6). NC: a session flag only."""
    async with capture(home) as (app, pilot, p):
        await fx.type_text(pilot, "a\n____\n")
        await pilot.pause(0.3)
        one(app, DIVIDER_NOTICE)
        assert fx.read_store(home).get("divider_notice") is True


async def test_TC_4445_a_stored_flag_keeps_the_notice_away(home):
    """TC-4445 (LLR-4402.15): a new app on a store holding `"divider_notice": true`, a divider
    made → 0 such notices. NC: the stored flag ignored."""
    async with capture(home, pad="", divider_notice=True) as (app, pilot, p):
        await fx.type_text(pilot, "a\n____\n")
        await pilot.pause(0.3)
        assert fx.notified(app, DIVIDER_NOTICE) == []


async def test_TC_4446c_a_long_divider_is_kept_as_typed(home):
    """TC-4446c (LLR-4402.16, pilot): `______` typed → the pad text and the stored `pad` both hold
    `______` (the rule is a rendering; the text is what the owner typed). NC: normalised to
    `____`."""
    async with capture(home) as (app, pilot, p):
        await fx.type_text(pilot, "a\n______\nb")
        await pilot.pause(1.3)
        assert pad_text(app) == "a\n______\nb"
        assert fx.read_store(home)["pad"] == "a\n______\nb"


async def test_TC_4447_no_alt_enter_binding(home):
    """TC-4447 (LLR-4402.17, R1-1): no binding of CaptureView, PadArea (inherited ones included)
    or ReviewList names `alt+enter` — Windows Terminal cannot deliver it to Textual 8.2.8, so a
    bound `alt+enter` would be a key that never works; `alt+enter` pressed in the pad inserts no
    divider line (2/2). NC: `alt+enter` bound as an alias."""
    for name in ("CaptureView", "PadArea", "ReviewList"):
        cls = fx.app_class(name)
        for klass in cls.__mro__:
            for b in klass.__dict__.get("BINDINGS", []):
                keys = b.key if hasattr(b, "key") else b[0]
                assert "alt+enter" not in [k.strip() for k in keys.split(",")], (name, klass, b)
    async with capture(home, pad="abc", cursor=(0, 3)) as (app, pilot, p):
        await fx.press(pilot, "alt+enter")
        await pilot.pause(0.1)
        assert not any(line.strip().startswith("____") for line in pad_text(app).split("\n"))


async def test_TC_4448_the_rule_is_drawn_by_the_line_render_not_the_highlight_map(home):
    """TC-4448 (LLR-4402.18, R1-5): "a\\n____\\nb" → the pad's highlight map holds no entry for the
    divider row, and the rule's cells are `─` glyphs in the dim hue #5b6675 — not styled `_`
    (2/2). NC: a highlight style on the underscores (the row would still read `____`)."""
    async with capture(home, pad="a\n____\nb", cursor=(2, 1)) as (app, pilot, p):
        pad = fx.pad_of(app)
        assert not pad._highlights.get(1), pad._highlights.get(1)
        cells = _divider_screen_row(app, 1)
        assert {c for c, _ in cells} == {"─"}
        assert {fg for _, fg in cells} == {"#5b6675"}, {fg for _, fg in cells}


# --------------------------------------------------------------------------- #
# HLR-4403 — the rail (the view's side of the suggestions)
# --------------------------------------------------------------------------- #
RAIL_123 = [" 1 Golden set: 12 questions still have no answe…",
            "   → Eval harness · Client A ▰▰▰",
            "     why questions · @username_subject · key",
            "",
            " 2 Volume lab fails on WSL  ▣ 1",
            "   → Module 4 · Volumes · Course ▰▰▰",
            "     why volume · oracle · script",
            "",
            "▌3 Quote for the new client: contracts Q&A",
            "▌  → + new project",
            "▌    no project shares a word"]
PAD_123 = f"{N1}\n____\n{N2}\n____\n{N3}"


async def test_TC_4475_the_rail_shows_each_note_its_option_and_why(home):
    """TC-4475 (LLR-4403.15): pad N1|N2|N3 with the cursor in N3, 118x30 → the rail's plain lines
    equal graph-proto-V's rail_rows example (9 lines + spacers; scores = G-T's executed values).
    NC: reason words joined by `, `."""
    async with capture(home, pad=PAD_123) as (app, pilot, p):
        assert trimmed(fx.rail_lines(app)) == RAIL_123, fx.rail_lines(app)


def _styles(text) -> list:
    from rich.style import Style

    def as_style(s):
        return s if isinstance(s, Style) else (Style.parse(s) if s else Style.null())
    out = [as_style(text.style)] * len(text.plain)
    for span in text.spans:
        st = as_style(span.style)
        for k in range(span.start, min(span.end, len(out))):
            out[k] = out[k] + st
    return out


def _hex(style) -> str | None:
    return style.color.get_truecolor().hex.lower() if style and style.color else None


def need_corpus(sg, tmp_path):
    return fx.need(sg, "corpus")(fx.f_lanes(tmp_path), fx.f_marks())


def test_TC_4476b_an_option_names_project_board_and_cue_in_their_hues(tmp_path):
    """TC-4476b (LLR-4403.16, hit_text): a hit on Eval harness · Client A drawn at 0.41, 0.20,
    0.09 → `Eval harness · Client A ▰▰▰` / `▰▰▱` / `▰▱▱` (3/3); the name cells bold in the project
    hue #60a5fa, the board cells in the board hue #38bdf8 (sky) (4/4); None → `+ new project`
    bold amber #fbbf24. NC: no board name."""
    sg = fx.suggest()
    hit_text = fx.app_class("hit_text")
    corpus = need_corpus(sg, tmp_path)
    doc = next(d for d in corpus.docs if d.project_name == "Eval harness")
    Hit = fx.need(sg, "Hit")
    for score, cue in ((0.41, "▰▰▰"), (0.20, "▰▰▱"), (0.09, "▰▱▱")):
        t = hit_text(Hit(doc, score, ["eval"]))
        assert t.plain == f"Eval harness · Client A {cue}"
    t = hit_text(Hit(doc, 0.41, ["eval"]))
    st = _styles(t)
    assert all(_hex(s) == "#60a5fa" and s.bold for s in st[0:12]), [str(s) for s in st[0:12]]
    i = t.plain.index("Client A")
    assert all(_hex(s) == "#38bdf8" for s in st[i:i + 8])
    t = hit_text(None)
    assert t.plain == "+ new project"
    assert all(_hex(s) == "#fbbf24" and s.bold for s in _styles(t))


async def test_TC_4476c_the_rail_paints_the_hues(home):
    """TC-4476c (LLR-4403.16, pilot): the rail's `→ Eval harness · Client A ▰▰▰` row paints
    `Eval harness` in #60a5fa and `Client A` in #38bdf8."""
    async with capture(home, pad=N1) as (app, pilot, p):
        box = fx.by_id(app, "cap-rail")
        r = box.content_region
        rows = fx.painted(app)
        for y in range(r.y, r.y + r.height):
            cells = rows[y][r.x:r.x + r.width]
            text = "".join(c for c, _ in cells)
            if "→ Eval harness" in text:
                i, j = text.index("Eval harness"), text.index("Client A")
                assert {fg for _, fg in cells[i:i + 12]} == {"#60a5fa"}
                assert {fg for _, fg in cells[j:j + 8]} == {"#38bdf8"}
                break
        else:
            pytest.fail(f"no `→ Eval harness` row painted: {fx.rail_lines(app)}")


async def test_TC_4477_only_the_cursors_note_shows_its_other_options(home):
    """TC-4477 (LLR-4403.17): cursor in N1 → under its reason line `▌    or Pilot rollout ·
    Client A ▰▰▱`; notes 2 and 3 show no `or` line (2/2). NC: an `or` line on every note."""
    async with capture(home, pad=PAD_123, cursor=(0, 0)) as (app, pilot, p):
        lines = trimmed(fx.rail_lines(app))
        assert lines[:4] == ["▌1 Golden set: 12 questions still have no answe…",
                             "▌  → Eval harness · Client A ▰▰▰",
                             "▌    why questions · @username_subject · key",
                             "▌    or Pilot rollout · Client A ▰▰▱"], lines
        assert sum(x.lstrip("▌ ").startswith("or ") for x in lines) == 1, lines


async def test_TC_4478_a_note_no_project_shares_a_word_with(home):
    """TC-4478 (LLR-4403.18): N3 (no hit) with the cursor elsewhere → its reason row reads exactly
    `     no project shares a word`. NC: a blank reason."""
    async with capture(home, pad=PAD_123, cursor=(0, 0)) as (app, pilot, p):
        lines = fx.rail_lines(app)
        i = lines.index(" 3 Quote for the new client: contracts Q&A")
        assert lines[i + 1:i + 3] == ["   → + new project", "     no project shares a word"]


async def test_TC_4479_a_weak_note_names_its_weak_words(home):
    """TC-4479 (LLR-4403.19): N5 `Answer the region chair` (Pilot rollout 0.1488 < MID) → `▌  → +
    new project`, `▌    weak: chair · region (Pilot rollout)`, `▌    or Pilot rollout · Client A
    ▰▱▱`. NC: `no project shares a word` for a note with hits."""
    async with capture(home, pad=N5) as (app, pilot, p):
        assert trimmed(fx.rail_lines(app)) == ["▌1 Answer the region chair",
                                               "▌  → + new project",
                                               "▌    weak: chair · region (Pilot rollout)",
                                               "▌    or Pilot rollout · Client A ▰▱▱"]


@pytest.mark.parametrize("extra, tail", [([], " · 1 board not read"),
                                         ([("gone", "Gone", "pink", None)],
                                          " · 2 boards not read")])
async def test_TC_4480_boards_not_read_are_named_in_the_head(home, extra, tail):
    """TC-4480 (LLR-4403.20): Course's file missing → the head ends ` · 1 board not read` and no
    suggestion names Course; with a second registry board missing too → ` · 2 boards not read`
    (3/3). NC: a silent skip."""
    p = fx.build_f(home, extra_boards=extra)
    fx.write_store(home, pad=N2)
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await fx.leave_home(pilot)
        p["C"].unlink()
        await fx.open_capture(pilot, app)
        assert fx.head(app).endswith(tail), fx.head(app)
        assert "Course" not in fx.rail_text(app), fx.rail_lines(app)


async def test_TC_4481_a_notes_hits_are_computed_once_per_distinct_text(home, monkeypatch):
    """TC-4481 (LLR-4403.21): pad N1|N2|N3 painted, then 5 characters typed at the end of N2's
    first line and 1.3 s waited → N1's and N3's texts are not scored again, no scored text is
    scored twice, and N2's final text exactly once (a spy on taskboard.app.suggest). The
    threshold's "exactly 1 for note 2" assumed the withdrawn 1 s scoring pause (A-1: the rail
    scores on every change), so the test holds the LLR's own words: at most once per distinct
    note text. NC: no cache."""
    calls = spy_suggest(monkeypatch)
    async with capture(home, pad=PAD_123) as (app, pilot, p):
        await pilot.pause(0.2)
        nt = fx.need("inbox", "note_task")

        def scored(t):
            x = nt(t)
            return x.title + "\n" + x.notes
        assert scored(N1) in calls and scored(N3) in calls, calls
        seen_before = len(calls)
        await fx.cursor_to(pilot, app, 3, len("Volume lab fails on WSL"))
        await fx.type_text(pilot, "xyzzy")
        await pilot.pause(1.3)
        later = calls[seen_before:]
        assert scored(N1) not in later and scored(N3) not in later, later
        assert len(calls) == len(set(calls)), [c for c in calls if calls.count(c) > 1]
        final = scored("Volume lab fails on WSLxyzzy\nthe oracle script expects /mnt/c\n"
                       "img: board-0938.png")
        assert calls.count(final) == 1, later


async def test_TC_4483b_the_view_reads_every_board(home):
    """TC-4483b (LLR-4403.23, pilot): 2 readable boards → the view suggests from both: N1 →
    Eval harness · Client A, N2 → Module 4 · Volumes · Course. NC: `app.board` only."""
    async with capture(home, pad=f"{N1}\n____\n{N2}") as (app, pilot, p):
        arrows = arrow_rows(fx.rail_lines(app))
        assert any("Eval harness · Client A" in a for a in arrows), arrows
        assert any("Module 4 · Volumes · Course" in a for a in arrows), arrows


async def test_TC_4484b_a_dump_rebuilds_the_suggestions(home):
    """TC-4484b (LLR-4403.24, pilot arm 1): a note `rotation` has no hit; a note titled `Rotation
    plan` (its notes `eval harness` make Eval harness its top choice) dumped there → the note
    `rotation` now names Eval harness (a weak hit, its `or` line). NC: no rebuild."""
    pad = "rotation\n____\nRotation plan\neval harness"
    async with capture(home, pad=pad, cursor=(0, 0)) as (app, pilot, p):
        first = fx.rail_text(app).split("\n 2 ")[0]
        assert "no project shares a word" in first and "Eval harness" not in first, first
        await dump_at(pilot, app, 2, 0)
        assert task_rec(p["A"], "Rotation plan") is not None, fx.messages(app)
        await fx.cursor_to(pilot, app, 0, 0)
        await pilot.pause(0.2)
        block = fx.rail_text(app)
        assert "Eval harness" in block and "weak: rotation" in block, block


async def test_TC_4485b_no_project_anywhere_offers_a_new_project(home):
    """TC-4485b (LLR-4403.25, rail): one readable board with 0 projects, note `rotation plan` →
    `▌1 rotation plan`, `▌  → + new project`, `▌    no project shares a word`; 0 exceptions
    (2/2). NC: index the empty document list."""
    p = fx.build_f(home, course=False)
    Board([], [], p["A"], fx.settings(), ["Backlog", "Doing", "Done"]).save()
    fx.write_store(home, pad="rotation plan")
    app = fx.open_f_app()
    async with app.run_test(size=W118) as pilot:
        await pilot.pause()
        if type(app.screen).__name__ == "BoardsHome":
            await fx.press(pilot, "escape")
        await fx.open_capture(pilot, app)
        assert trimmed(fx.rail_lines(app)) == ["▌1 rotation plan", "▌  → + new project",
                                               "▌    no project shares a word"]
        assert app.is_running


async def test_TC_4488b_the_view_scores_a_note_without_its_image_lines(home, monkeypatch):
    """TC-4488b (LLR-4403.28, pilot): pad N2 → the spy sees suggest called with "Volume lab fails
    on WSL\\nthe oracle script expects /mnt/c" — an image line is no word source (P-T-4). NC: the
    raw part text scored."""
    calls = spy_suggest(monkeypatch)
    async with capture(home, pad=N2) as (app, pilot, p):
        await pilot.pause(0.2)
        assert N2T in calls, calls
        assert not any("img:" in c for c in calls), calls


# --------------------------------------------------------------------------- #
# HLR-4404 — dump, alternatives, the inline new project
# --------------------------------------------------------------------------- #
VOLUME_NOTE = N2T


def test_TC_4501_a_dump_adds_one_task_to_the_chosen_project_on_its_board(tmp_path, monkeypatch):
    """TC-4501 (LLR-4404.1, layer 0): target Course (not the open board), project pm, the AT-4402
    note → ok; Course's task ids ["tc1", "t0000001"]; the new task's project_id "pm" (2/2).
    NC: dump to the open board always."""
    p, ids = s_dump(tmp_path, monkeypatch)
    out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm",
               project_name="Module 4 · Volumes")
    assert out.ok is True, out.notice
    assert fx.task_ids(p["C"]) == ["tc1", "t0000001"]
    assert fx.tasks_of(p["C"])[-1]["project_id"] == "pm"
    assert fx.tasks_of(p["A"]) == []


async def test_TC_4501b_alt_d_files_the_note_on_the_suggested_board(home):
    """TC-4501b (LLR-4404.1, pilot): cursor in the volume note → Course's task count +1, the new
    task in Module 4 · Volumes (pv) — the suggested project on ANOTHER board."""
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        before = len(fx.tasks_of(p["C"]))
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        recs = fx.tasks_of(p["C"])
        assert len(recs) == before + 1, fx.messages(app)
        assert recs[-1]["project_id"] == "pv" and recs[-1]["title"] == "Volume lab fails on WSL"


def test_TC_4502_the_title_is_the_visible_text_of_the_title_line(tmp_path, monkeypatch):
    """TC-4502 (LLR-4404.2): "::b:: Golden set ::\\nmore" → `Golden set` (titles draw no colour,
    so a marker would show literally); "img: a.png\\nTitle\\nx" → `Title` (2/2). NC: the raw first
    line."""
    nt = fx.need("inbox", "note_task")
    assert nt("::b:: Golden set ::\nmore").title == "Golden set"
    assert nt("img: a.png\nTitle\nx").title == "Title"
    p, ids = s_dump(tmp_path, monkeypatch)
    out = dump(target(p), "::b:: Golden set ::\nmore", p["F"], project_id="pm")
    assert out.ok and out.task.title == "Golden set"
    assert fx.tasks_of(p["C"])[-1]["title"] == "Golden set"


def test_TC_4503_the_notes_are_the_other_lines_verbatim(tmp_path, monkeypatch):
    """TC-4503 (LLR-4404.3): "T\\n\\nask @username_subject ::r:: now ::\\n\\nsecond\\nimg: a.png\\n" →
    notes "ask @username_subject ::r:: now ::\\n\\nsecond" (inner blank line kept, image line and
    outer blanks gone). NC: inner blank lines dropped."""
    nt = fx.need("inbox", "note_task")
    text = "T\n\nask @username_subject ::r:: now ::\n\nsecond\nimg: a.png\n"
    assert nt(text).notes == "ask @username_subject ::r:: now ::\n\nsecond"


def test_TC_4504_a_dumped_task_is_stamped_on_both_paths(tmp_path, monkeypatch):
    """TC-4504 (LLR-4404.4): an open-board dump (through `add_task`) and an other-board dump (its
    own `models.stamp`) each give `created` matching YYYY-MM-DDTHH:MM:SS within [t0, t1] (2/2).
    The owner finds a captured task again by when it was added (Inc L). NC: no stamp on the
    other-board path."""
    p, ids = s_dump(tmp_path, monkeypatch)
    live = Board.load(p["A"])
    t0 = datetime.now().replace(microsecond=0)
    a = dump(target(p, "A", live), "Golden set answer key", p["F"], project_id="pe")
    c = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    t1 = datetime.now()
    assert a.ok and c.ok, (a.notice, c.notice)
    for path, tid in ((p["A"], a.task.id), (p["C"], c.task.id)):
        rec = next(r for r in fx.tasks_of(path) if r["id"] == tid)
        assert re.match(fx.STAMP_RE, rec.get("created") or ""), rec
        assert t0 <= datetime.fromisoformat(rec["created"]) <= t1


def test_TC_4505_a_dumped_task_takes_the_boards_first_phase(tmp_path, monkeypatch):
    """TC-4505 (LLR-4404.5): Course's phases ["Todo", "Doing", "Done"] → phase `Todo` (the Task
    default `Backlog` is not a phase there); Client A → `Backlog`. NC: the dataclass default."""
    p, ids = s_dump(tmp_path, monkeypatch)
    c = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    assert c.ok and fx.tasks_of(p["C"])[-1]["phase"] == "Todo"
    live = Board.load(p["A"])
    a = dump(target(p, "A", live), "Golden set", p["F"], project_id="pe")
    assert a.ok and fx.tasks_of(p["A"])[-1]["phase"] == "Backlog"


@pytest.mark.parametrize("which", ["b", "c"])
async def test_TC_4506_a_dump_removes_the_note_and_one_adjacent_divider(home, which):
    """TC-4506 (LLR-4404.6): pad a|b|c with b and c dumpable: dump b → "a\\n____\\nc"; dump c →
    "a\\n____\\nb" (the divider after, else the one before); every other line byte-identical (3/3).
    NC: the divider left behind (`a\\n____\\n____\\nc`)."""
    b, c = N4, EVAL_NOTE
    pad = f"a\n____\n{b}\n____\n{c}"
    async with capture(home, pad=pad) as (app, pilot, p):
        await dump_at(pilot, app, 2 if which == "b" else 4)
        want = {"b": f"a\n____\n{c}", "c": f"a\n____\n{b}"}[which]
        assert pad_text(app) == want, fx.messages(app)


async def test_TC_4507_a_dump_says_where_the_task_went(home):
    """TC-4507 (LLR-4404.7): exactly one notice `Dumped → Module 4 · Volumes · Course   ·   alt+u
    undo`, title `Capture`, markup False. NC: no `alt+u` hint."""
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        one(app, DUMP_COURSE)


async def test_TC_4508_an_open_board_dump_goes_through_the_live_board(home):
    """TC-4508 (LLR-4404.8): N1 into Eval harness (Client A, the open board) → `app.board` holds
    the task, the board file holds it, and after `escape` the board view draws its title (3/3).
    NC: added to a fresh copy (`app.board` lacks it, a later save of the app would drop it)."""
    async with capture(home, pad=N1) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        assert any(t.title == fx.N1_TITLE for t in app.board.tasks), fx.messages(app)
        assert task_rec(p["A"], fx.N1_TITLE) is not None
        await fx.press(pilot, "escape")
        await pilot.pause(0.3)
        assert not fx.on_capture(app)
        assert "Golden set" in "\n".join(fx.screen_rows(app))


def test_TC_4509_another_board_is_written_fresh_under_its_lock(tmp_path, monkeypatch):
    """TC-4509 (LLR-4404.9, layer 0): at the save the board's lock file exists; `save_atomic` is
    called once and `Board.save` never on that board; a task another writer appended to the file
    before the dump is still there after it (3/3; `move_project`'s pattern, R1-3)."""
    p, ids = s_dump(tmp_path, monkeypatch)
    data = json.loads(p["C"].read_text(encoding="utf-8"))
    data["tasks"].append({"id": "tw1", "title": "Other writer", "project_id": "pm",
                          "phase": "Todo"})
    p["C"].write_text(json.dumps(data, indent=2), encoding="utf-8")
    lock = p["C"].resolve().with_name("board.json.lock")
    atomic, plain = [], []
    real_atomic, real_save = Board.save_atomic, Board.save

    def spy_atomic(self):
        atomic.append((Path(self.path).resolve(), lock.exists()))
        return real_atomic(self)

    def spy_save(self):
        plain.append(Path(self.path).resolve())
        return real_save(self)
    monkeypatch.setattr(Board, "save_atomic", spy_atomic)
    monkeypatch.setattr(Board, "save", spy_save)
    out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    assert out.ok, out.notice
    assert atomic == [(p["C"].resolve(), True)], atomic
    assert p["C"].resolve() not in plain
    assert fx.task_ids(p["C"]) == ["tc1", "tw1", "t0000001"]


async def test_TC_4509b_a_task_written_after_the_view_opened_survives_the_dump(home):
    """TC-4509b (LLR-4404.9, pilot): the view opened (Course read for the suggestions), another
    writer appends `tw1` to Course's file, then the volume note is dumped there → `tw1` is still
    in the file beside the new task. NC: the board saved from the read made at open."""
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        data = json.loads(p["C"].read_text(encoding="utf-8"))
        data["tasks"].append({"id": "tw1", "title": "Other writer", "project_id": "pv",
                              "phase": "Todo"})
        p["C"].write_text(json.dumps(data, indent=2), encoding="utf-8")
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        ids = fx.task_ids(p["C"])
        assert "tw1" in ids and len(ids) == 5, (ids, fx.messages(app))


def test_TC_4510_a_missing_board_file_dumps_nothing_and_creates_nothing(tmp_path, monkeypatch):
    """TC-4510 (LLR-4404.10, layer 0): target S/gone/board.json → ok False, `Course's file is
    missing — nothing dumped.`; neither the file nor its lock created (3/3). NC: `Board.load`
    seeds and saves sample data there."""
    p, ids = s_dump(tmp_path, monkeypatch)
    gone = tmp_path / "gone" / "board.json"
    out = dump(fx.need("inbox", "DumpTarget")(gone, "Course", None), VOLUME_NOTE, p["F"],
               project_id="pm")
    assert out.ok is False and out.notice == "Course's file is missing — nothing dumped."
    assert not gone.exists() and not gone.with_name("board.json.lock").exists()


async def test_TC_4510b_the_note_stays_when_the_board_file_went_missing(home):
    """TC-4510b (LLR-4404.10, pilot): Course's file deleted after `n` → the notice, the pad
    unchanged, no file at that path."""
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        p["C"].unlink()
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        one(app, "Course's file is missing — nothing dumped.")
        assert pad_text(app) == VOLUME_NOTE
        assert not p["C"].exists()


def test_TC_4511_an_unreadable_board_file_is_left_as_it_is(tmp_path, monkeypatch):
    """TC-4511 (LLR-4404.11): Course's file "{not json" → ok False, `Course's file cannot be read
    — nothing dumped.`, the bytes unchanged (2/2). NC: an empty board written over it."""
    p, ids = s_dump(tmp_path, monkeypatch)
    p["C"].write_text("{not json", encoding="utf-8")
    out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    assert out.ok is False and out.notice == "Course's file cannot be read — nothing dumped."
    assert p["C"].read_text(encoding="utf-8") == "{not json"


def test_TC_4512_a_project_gone_from_the_fresh_board_dumps_nothing(tmp_path, monkeypatch):
    """TC-4512 (LLR-4404.12): pm removed from Course's file after the suggestion → `Module 4 ·
    Volumes is no longer on Course — nothing dumped.`; the bytes unchanged (2/2). NC: a task with
    a dangling project_id."""
    p, ids = s_dump(tmp_path, monkeypatch)
    data = json.loads(p["C"].read_text(encoding="utf-8"))
    data["projects"] = []
    p["C"].write_text(json.dumps(data, indent=2), encoding="utf-8")
    before = file_bytes(p["C"])
    out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm",
               project_name="Module 4 · Volumes")
    assert out.ok is False
    assert out.notice == "Module 4 · Volumes is no longer on Course — nothing dumped."
    assert file_bytes(p["C"]) == before


async def test_TC_4512b_the_view_words_a_vanished_project_by_name(home):
    """TC-4512b (LLR-4404.12, pilot): Module 4 · Volumes removed from Course's file after `n` →
    the notice names the project; the pad keeps the note."""
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        data = json.loads(p["C"].read_text(encoding="utf-8"))
        data["projects"] = []
        p["C"].write_text(json.dumps(data, indent=2), encoding="utf-8")
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        one(app, "Module 4 · Volumes is no longer on Course — nothing dumped.")
        assert pad_text(app) == VOLUME_NOTE


def test_TC_4513_a_busy_board_dumps_nothing(tmp_path, monkeypatch):
    """TC-4513 (LLR-4404.13, layer 0): a fresh foreign Course lock → ok False, the notice holds
    `Course is busy`; the board's bytes and the pad images folder unchanged. NC: write without
    the lock."""
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2)
    p, ids = s_dump(tmp_path, monkeypatch)
    write_lock(p["C"])
    before = file_bytes(p["C"])
    out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    assert out.ok is False and "Course is busy" in (out.notice or ""), out.notice
    assert file_bytes(p["C"]) == before


async def test_TC_4513b_the_note_stays_when_the_board_is_busy(home, monkeypatch):
    """TC-4513b (LLR-4404.13, pilot): a held Course lock → the notice holds `is busy`; pad and
    board bytes unchanged (3/3)."""
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2)
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        write_lock(p["C"])
        before = file_bytes(p["C"])
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.5)
        assert holding(app, "is busy"), fx.messages(app)
        assert pad_text(app) == VOLUME_NOTE and file_bytes(p["C"]) == before


def test_TC_4514_a_failed_save_dumps_nothing(tmp_path, monkeypatch):
    """TC-4514 (LLR-4404.14, layer 0): Course's file read-only → ok False, the notice starts
    `Course could not be saved: ` and ends ` — nothing dumped.` (2/2). NC: an unguarded save."""
    import stat
    p, ids = s_dump(tmp_path, monkeypatch)
    os.chmod(p["C"], stat.S_IREAD)
    try:
        out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    finally:
        os.chmod(p["C"], stat.S_IREAD | stat.S_IWRITE)
    assert out.ok is False
    assert out.notice.startswith("Course could not be saved: ") and \
        out.notice.endswith(" — nothing dumped."), out.notice


async def test_TC_4514b_the_note_stays_when_the_save_fails(home):
    """TC-4514b (LLR-4404.14, pilot): Course read-only → the notice's prefix and suffix, the pad
    unchanged."""
    import stat
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        os.chmod(p["C"], stat.S_IREAD)
        try:
            await fx.press(pilot, "alt+d")
            await pilot.pause(0.2)
        finally:
            os.chmod(p["C"], stat.S_IREAD | stat.S_IWRITE)
        got = starting(app, "Course could not be saved: ")
        assert got and got[0].endswith(" — nothing dumped."), fx.messages(app)
        assert pad_text(app) == VOLUME_NOTE


def test_TC_4515_a_failed_open_board_save_rolls_the_live_board_back(tmp_path, monkeypatch):
    """TC-4515 (LLR-4404.15): `Board.save` raising OSError("disk full") during an open-board dump
    into a new project → ok False, `Client A could not be saved: disk full — nothing dumped.`;
    the live board holds neither the task nor the project (its task and project counts as before),
    and no `images/t0000001` folder is left (2/2). NC: no roll-back (the app's next save would
    write them)."""
    p, ids = s_dump(tmp_path, monkeypatch)
    live = Board.load(p["A"])
    n_tasks, n_projects = len(live.tasks), len(live.projects)

    def boom(self):
        raise OSError("disk full")
    monkeypatch.setattr(Board, "save", boom)
    out = dump(target(p, "A", live), "Contracts kickoff", p["F"], new_name="Contracts pilot")
    assert out.ok is False
    assert out.notice == "Client A could not be saved: disk full — nothing dumped."
    assert (len(live.tasks), len(live.projects)) == (n_tasks, n_projects)
    assert not (p["A"].parent / "images" / "t0000001").exists()


async def test_TC_4516_alt_o_cycles_the_options_and_wraps(home):
    """TC-4516 (LLR-4404.16): `store rubric` has 3 options (+ new project, Pilot rollout, Eval
    harness); `alt+o` steps the rail's `→` line through them and the third press is back at the
    top choice (2/2). NC: no wrap."""
    async with capture(home, pad=WEAK3) as (app, pilot, p):
        seen = [arrow_rows(fx.rail_lines(app))[0]]
        for _ in range(3):
            await fx.press(pilot, "alt+o")
            seen.append(arrow_rows(fx.rail_lines(app))[0])
        assert seen == ["▌  → + new project", "▌  → Pilot rollout · Client A ▰▱▱",
                        "▌  → Eval harness · Client A ▰▱▱", "▌  → + new project"], seen


def _arrow_of(app, k: int) -> str:
    """The `→` row of note k (1-based) in the wide rail."""
    lines = fx.rail_lines(app)
    for i, line in enumerate(lines):
        if re.match(rf"^[ ▌]{k} ", line):
            return lines[i + 1]
    raise AssertionError(f"note {k} not in the rail: {lines}")


async def test_TC_4517_the_choice_is_the_options_identity_shared_with_the_review(home):
    """TC-4517 (LLR-4404.17, ARCH-2), 3 arms. (1) `alt+o` on note 2 (N1), then `alt+a` → its
    review row shows the same option, Pilot rollout. (2) `Rubric for the pilot` (Pilot rollout
    0.2232, Eval harness 0.0885) set to Eval harness with `alt+o`; three rubric notes dumped into
    Eval harness (its options become [Eval harness 0.6028, Pilot rollout 0.1593]) → the choice is
    still Eval harness (an index 1 would now be Pilot rollout). (3) a chosen option that is no
    longer among the options (its project archived, the suggestions rebuilt by a dump) → the top
    choice. NC: keyed by note index / kept as a list index."""
    async with capture(home, pad=f"{N2T}\n____\n{N1}", cursor=(3, 0)) as (app, pilot, p):
        await fx.press(pilot, "alt+o")
        assert _arrow_of(app, 2) == "▌  → Pilot rollout · Client A ▰▰▱", fx.rail_lines(app)
        await fx.press(pilot, "alt+a")
        await pilot.pause(0.2)
        body = fx.plain(fx.by_id(app, "rv-body", screen=app.screen)).split("\n")
        row = next(x for x in body if "Golden set" in x)
        assert "Pilot rollout · Client A ▰▰▱" in row, body
    pad = ("Rubric for the pilot\n____\nRubric review\n____\nRubric scoring\n____\n"
           "Pilot judge rubric")
    async with capture(home, pad=pad, cursor=(0, 0)) as (app, pilot, p):
        await fx.press(pilot, "alt+o")
        assert _arrow_of(app, 1) == "▌  → Eval harness · Client A ▰▱▱", fx.rail_lines(app)
        for title, other in (("Rubric review", True), ("Rubric scoring", True),
                             ("Pilot judge rubric", False)):
            r = row_of(pad_text(app), title)
            await fx.cursor_to(pilot, app, r, 0)
            if other:
                await fx.press(pilot, "alt+o")
            assert "Eval harness" in fx.rail_text(app), fx.rail_lines(app)
            await fx.press(pilot, "alt+d")
            await pilot.pause(0.2)
            assert task_rec(p["A"], title) is not None, (title, fx.messages(app))
        assert all(task_rec(p["A"], t)["project_id"] == "pe"
                   for t in ("Rubric review", "Rubric scoring", "Pilot judge rubric"))
        await fx.cursor_to(pilot, app, 0, 0)
        assert _arrow_of(app, 1).startswith("▌  → Eval harness · Client A"), fx.rail_lines(app)


async def test_TC_4517b_a_choice_that_left_the_options_falls_back_to_the_top(home):
    """TC-4517b (LLR-4404.17 arm 3): EVAL_NOTE set to Pilot rollout with `alt+o`; Pilot rollout
    archived on the live board; the volume note dumped (the suggestions rebuilt without Pilot
    rollout) → EVAL_NOTE's `→` line is its top choice, Eval harness."""
    async with capture(home, pad=f"{EVAL_NOTE}\n____\n{N2T}", cursor=(0, 0)) as (app, pilot, p):
        await fx.press(pilot, "alt+o")
        assert _arrow_of(app, 1).startswith("▌  → Pilot rollout"), fx.rail_lines(app)
        app.board.project_by_id("pr").archived = True
        await dump_at(pilot, app, 2, 0)
        assert task_rec(p["C"], "Volume lab fails on WSL") is not None, fx.messages(app)
        await fx.cursor_to(pilot, app, 0, 0)
        assert _arrow_of(app, 1).startswith("▌  → Eval harness · Client A"), fx.rail_lines(app)


async def test_TC_4518_alt_d_on_a_new_project_note_opens_the_name_field(home):
    """TC-4518 (LLR-4404.18): cursor in N3 (top choice + new project), `alt+d` → the name field
    shown and focused, titled `New project for note 1`; no board changed (2/2). NC: dump to the
    best weak hit."""
    async with capture(home, pad=N3) as (app, pilot, p):
        before = fx.shas(p)
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.1)
        assert field_open(app) and app.focused is field(app)
        assert border_title(field(app)) == "New project for note 1"
        assert fx.shas(p) == before


async def test_TC_4519_alt_n_names_the_note_it_is_for(home):
    """TC-4519 (LLR-4404.19): pad N1|N2|N3, cursor in N3, `alt+n` → the field titled `New project
    for note 3`. NC: unbound."""
    async with capture(home, pad=PAD_123) as (app, pilot, p):
        await fx.press(pilot, "alt+n")
        await pilot.pause(0.1)
        assert field_open(app)
        assert border_title(field(app)) == "New project for note 3"


async def test_TC_4520_the_name_fields_board_starts_as_the_open_board(home):
    """TC-4520 (LLR-4404.20): the open board is Course (lane 1) → the key row reads `↵ create on
    Course + dump …`. NC: the first registry board (Client A)."""
    async with capture(home, pad=N3, build={"last": "course"}) as (app, pilot, p):
        assert Path(app.board.path).resolve() == p["C"].resolve()
        await fx.press(pilot, "alt+n")
        await pilot.pause(0.1)
        assert fx.keys_row(app) == "↵ create on Course + dump   ⇥ board   esc back"


async def test_TC_4521_tab_cycles_the_readable_boards(home):
    """TC-4521 (LLR-4404.21, P-V-1): 4 registry boards, the third one's file missing; `tab`
    posted as Key("tab", "\\t") through the driver steps Client A → Course → Third → Client A,
    skipping the unreadable board, and the field keeps its value and focus (3/3). NC: unreadable
    boards included; `tab` non-priority (focus leaves the field)."""
    third = Board([Project("Ops", "pink", id="po")], [], Path("x"), {}, ["Todo", "Done"])
    build = {"extra_boards": [("gone", "Gone", "pink", None), ("third", "Third", "lime", third)]}
    async with capture(home, pad=N3, build=build) as (app, pilot, p):
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "xy")
        seen = []
        for _ in range(3):
            await fx.post_key(pilot, "tab", "\t")
            seen.append(fx.keys_row(app).split(" + dump")[0])
            assert field(app).value == "xy" and app.focused is field(app)
        assert seen == ["↵ create on Course", "↵ create on Third", "↵ create on Client A"], seen


async def test_TC_4522_the_name_fields_key_row(home):
    """TC-4522 (LLR-4404.22): field open at 118x30 → the key row is exactly `↵ create on Client A
    + dump   ⇥ board   esc back`. NC: the pad's key row kept."""
    async with capture(home, pad=N3) as (app, pilot, p):
        await fx.press(pilot, "alt+n")
        await pilot.pause(0.1)
        assert fx.keys_row(app) == "↵ create on Client A + dump   ⇥ board   esc back"


async def test_TC_4523_enter_creates_the_project_and_dumps_in_one_write(home, monkeypatch):
    """TC-4523 (LLR-4404.23, pilot): cursor in N3, `alt+n`, `Contracts pilot`, `enter` → Client
    A's file holds the project and a task whose project_id is its id; `Board.save` called once
    (3/3). NC: `add_project` then `add_task` (2 saves)."""
    async with capture(home, pad=N3) as (app, pilot, p):
        saves = []
        real = Board.save

        def spy(self):
            saves.append(Path(self.path).resolve())
            return real(self)
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "Contracts pilot")
        monkeypatch.setattr(Board, "save", spy)
        await fx.press(pilot, "enter")
        await pilot.pause(0.2)
        proj = next((x for x in project_recs(p["A"]) if x["name"] == "Contracts pilot"), None)
        assert proj is not None, fx.messages(app)
        task = task_rec(p["A"], "Quote for the new client: contracts Q&A")
        assert task and task["project_id"] == proj["id"]
        assert saves.count(p["A"].resolve()) == 1, saves


def test_TC_4523b_a_new_project_dump_is_one_save_on_either_path(tmp_path, monkeypatch):
    """TC-4523b (LLR-4404.23, layer 0): open board → `Board.save` once, `add_project` never;
    another board → `save_atomic` once; on both the task's project_id is the new project's."""
    p, ids = s_dump(tmp_path, monkeypatch)
    calls = {"save": 0, "atomic": 0, "add_project": 0}
    real_save, real_atomic, real_add = Board.save, Board.save_atomic, Board.add_project

    def count(name, real):
        def f(self, *a):
            calls[name] += 1
            return real(self, *a)
        return f
    monkeypatch.setattr(Board, "save", count("save", real_save))
    monkeypatch.setattr(Board, "save_atomic", count("atomic", real_atomic))
    monkeypatch.setattr(Board, "add_project", count("add_project", real_add))
    live = Board.load(p["A"])
    out = dump(target(p, "A", live), "Kickoff call", p["F"], new_name="Contracts pilot")
    assert out.ok, out.notice
    assert (calls["save"], calls["add_project"]) == (1, 0), calls
    assert live.projects[-1].name == "Contracts pilot"
    assert out.task.project_id == live.projects[-1].id
    calls.update(save=0, atomic=0)
    out = dump(target(p), "Kickoff call", p["F"], new_name="Contracts pilot")
    assert out.ok and calls["atomic"] == 1 and calls["save"] == 0, (out.notice, calls)
    recs = project_recs(p["C"])
    assert recs[-1]["name"] == "Contracts pilot"
    assert fx.tasks_of(p["C"])[-1]["project_id"] == recs[-1]["id"]


def test_TC_4524_a_new_project_takes_the_first_free_hue(tmp_path, monkeypatch):
    """TC-4524 (LLR-4404.24): Client A uses lime and green → `sky`; Course uses sky → `lime`; a
    board of 9 projects using all 8 hues → `PROJECT_COLORS[9 % 8]` (2/2 + the Course arm). NC:
    always violet."""
    p, ids = s_dump(tmp_path, monkeypatch)
    live = Board.load(p["A"])
    assert dump(target(p, "A", live), "Kick", p["F"], new_name="New one").ok
    assert live.projects[-1].color == "sky"
    assert dump(target(p), "Kick", p["F"], new_name="New one").ok
    assert project_recs(p["C"])[-1]["color"] == "lime"
    nine = [Project(f"P{i}", models.PROJECT_COLORS[i % 8], id=f"p{i}") for i in range(9)]
    Board(nine, [], p["C"], fx.settings(), ["Todo", "Doing", "Done"]).save()
    assert dump(target(p), "Kick", p["F"], new_name="Tenth").ok
    assert project_recs(p["C"])[-1]["color"] == models.PROJECT_COLORS[9 % 8] == "green"


@pytest.mark.parametrize("name", ["   ", "\x07\t"])
def test_TC_4525_a_blank_project_name_creates_nothing(tmp_path, monkeypatch, name):
    """TC-4525 (LLR-4404.25, layer 0): a name empty once control characters and surrounding
    whitespace are removed → `A project needs a name.`; 0 projects added. NC: an `Untitled`
    project."""
    p, ids = s_dump(tmp_path, monkeypatch)
    out = dump(target(p), "Kick", p["F"], new_name=name)
    assert out.ok is False and out.notice == "A project needs a name."
    assert len(project_recs(p["C"])) == 1


async def test_TC_4525b_the_field_stays_open_on_a_blank_name(home):
    """TC-4525b (LLR-4404.25, pilot): `   `, `enter` → the notice, 0 projects added, the field
    still open (3/3)."""
    async with capture(home, pad=N3) as (app, pilot, p):
        n = len(project_recs(p["A"]))
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "   ")
        await fx.press(pilot, "enter")
        await pilot.pause(0.1)
        one(app, "A project needs a name.")
        assert len(project_recs(p["A"])) == n and field_open(app)


def test_TC_4526_a_taken_project_name_creates_nothing(tmp_path, monkeypatch):
    """TC-4526 (LLR-4404.26, layer 0): `eval HARNESS ` against `Eval harness` (case and
    surrounding whitespace ignored) → `Client A already has a project named eval HARNESS.`; 0
    projects added (2/2). NC: a second same-named project."""
    p, ids = s_dump(tmp_path, monkeypatch)
    live = Board.load(p["A"])
    out = dump(target(p, "A", live), "Kick", p["F"], new_name="eval HARNESS ")
    assert out.ok is False
    assert out.notice == "Client A already has a project named eval HARNESS."
    assert len(live.projects) == 2 and len(project_recs(p["A"])) == 2


async def test_TC_4526b_the_view_refuses_a_taken_name(home):
    """TC-4526b (LLR-4404.26, pilot): `eval HARNESS `, `enter` → a notice holding `Client A
    already has a project named`; no project added."""
    async with capture(home, pad=N3) as (app, pilot, p):
        n = len(project_recs(p["A"]))
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "eval HARNESS ")
        await fx.press(pilot, "enter")
        await pilot.pause(0.1)
        assert holding(app, "Client A already has a project named"), fx.messages(app)
        assert len(project_recs(p["A"])) == n


async def test_TC_4527_esc_in_the_name_field_goes_back_to_the_pad(home):
    """TC-4527 (LLR-4404.27): field open, `escape` → the field hidden, the pad focused, and the
    view still open; boards and store unchanged (3/3). NC: `esc` closes the view."""
    async with capture(home, pad=N3) as (app, pilot, p):
        before, store = fx.shas(p), fx.sha(p["store"])
        await fx.press(pilot, "alt+n")
        await fx.press(pilot, "escape")
        await pilot.pause(0.1)
        assert not field_open(app) and app.focused is fx.pad_of(app) and fx.on_capture(app)
        assert fx.shas(p) == before and fx.sha(p["store"]) == store


async def test_TC_4528_a_key_with_no_note_under_the_cursor_says_so(home):
    """TC-4528 (LLR-4404.28): an empty pad, `alt+d`, `alt+o`, `alt+n` → each `No note under the
    cursor.`; nothing changes (3/3). NC: act on the last note."""
    async with capture(home) as (app, pilot, p):
        before = fx.shas(p)
        for key in ("alt+d", "alt+o", "alt+n"):
            await fx.press(pilot, key)
        assert len(fx.notified(app, "No note under the cursor.")) == 3, fx.messages(app)
        assert fx.shas(p) == before and not field_open(app)


@pytest.mark.parametrize("note", ["img: a.png", "::b:: ::"])
def test_TC_4529_a_note_with_no_title_line_dumps_nothing(tmp_path, monkeypatch, note):
    """TC-4529 (LLR-4404.29, layer 0): `img: a.png` and `::b:: ::` have no line with visible text
    → `This note has no text line for a title.`; 0 tasks, 0 files written. NC: a task titled
    `img: a.png`."""
    p, ids = s_dump(tmp_path, monkeypatch)
    before = file_bytes(p["C"])
    out = dump(target(p), note, p["F"], project_id="pm")
    assert out.ok is False and out.notice == "This note has no text line for a title."
    assert file_bytes(p["C"]) == before and not p["F"].exists()


async def test_TC_4529b_the_view_refuses_a_titleless_note(home):
    """TC-4529b (LLR-4404.29, pilot): note `img: a.png`, `alt+d` → the notice; no task."""
    async with capture(home, pad="img: a.png") as (app, pilot, p):
        before = fx.shas(p)
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.1)
        assert fx.notified(app, "This note has no text line for a title."), fx.messages(app)
        assert fx.shas(p) == before


async def test_TC_4530_the_cursors_note_on_a_divider_is_the_one_above(home):
    """TC-4530 (LLR-4404.30): "a\\n____\\nb": the cursor on row 1 (the divider) → the note is `a`
    (`alt+n` titles its field `note 1`); on row 2 → `b` (`note 2`) (2/2). NC: the note below."""
    nat = fx.need("inbox", "note_at")
    assert nat("a\n____\nb", 1).text == "a" and nat("a\n____\nb", 2).text == "b"
    async with capture(home, pad="a\n____\nb", cursor=(1, 0)) as (app, pilot, p):
        await fx.press(pilot, "alt+n")
        assert border_title(field(app)) == "New project for note 1"
        await fx.press(pilot, "escape")
        await fx.cursor_to(pilot, app, 2, 0)
        await fx.press(pilot, "alt+n")
        assert border_title(field(app)) == "New project for note 2"


def test_TC_4531_the_other_fields_stay_at_the_task_defaults(tmp_path, monkeypatch):
    """TC-4531 (LLR-4404.31): a note holding a URL → priority normal, no dates, not archived, no
    URLs, no links (5/5; milestone off, no mark). NC: the note's first URL copied into `urls`."""
    p, ids = s_dump(tmp_path, monkeypatch)
    out = dump(target(p), "Vendor portal\nsee https://example.com/spec", p["F"], project_id="pm")
    assert out.ok
    t = out.task
    assert (t.priority, t.start_date, t.due_date, t.archived) == ("normal", None, None, False)
    assert (t.urls, t.depends_on, t.milestone, t.mark) == ([], [], False, None)
    rec = fx.tasks_of(p["C"])[-1]
    assert rec.get("urls") == [] and rec.get("depends_on") == []


def test_TC_4532_a_dump_writes_one_birth_record(tmp_path, monkeypatch):
    """TC-4532 (LLR-4404.32): open-board and other-board dumps each append exactly 1 birth record
    {"task": id, "from": null, "to": phase} whose `at` equals the task's `created`; on the other
    board it is appended after `save_atomic` returned (3/3). NC: no record on the other-board
    path (no `add_task` there)."""
    p, ids = s_dump(tmp_path, monkeypatch)
    live = Board.load(p["A"])
    a = dump(target(p, "A", live), "Golden set", p["F"], project_id="pe")
    real = Board.save_atomic
    seen_at_save = []

    def spy(self):
        seen_at_save.append(len(fx.history_lines(self.path)))
        return real(self)
    monkeypatch.setattr(Board, "save_atomic", spy)
    before_c = len(fx.history_lines(p["C"]))
    c = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    assert a.ok and c.ok
    for path, out, phase in ((p["A"], a, "Backlog"), (p["C"], c, "Todo")):
        births = [r for r in fx.history_lines(path) if r.get("task") == out.task.id]
        rec = next(r for r in fx.tasks_of(path) if r["id"] == out.task.id)
        assert len(births) == 1, births
        assert births[0]["from"] is None and births[0]["to"] == phase
        assert births[0]["at"] == rec["created"]
    assert seen_at_save == [before_c], "the birth line was written before save_atomic returned"


def test_TC_4533_a_board_changed_between_read_and_save_dumps_nothing(tmp_path, monkeypatch):
    """TC-4533 (LLR-4404.33): a lock-ignoring writer appends `tx1` to Course right after the dump's
    fresh read → ok False, `Course changed while dumping — nothing dumped.`; the board's bytes are
    that writer's (3/3 with the view's arm). NC: no stamp check (the writer's task lost)."""
    p, ids = s_dump(tmp_path, monkeypatch)
    inbox = fx.inbox()
    real = boards.peek_board
    state = {"done": False}
    written = {}

    def racing(path):
        b = real(path)
        if not state["done"] and Path(path).resolve() == p["C"].resolve():
            state["done"] = True
            data = json.loads(p["C"].read_text(encoding="utf-8"))
            data["tasks"].append({"id": "tx1", "title": "Racer", "phase": "Todo"})
            p["C"].write_text(json.dumps(data, indent=2), encoding="utf-8")
            written["bytes"] = p["C"].read_bytes()
        return b
    monkeypatch.setattr(boards, "peek_board", racing)
    monkeypatch.setattr(inbox, "peek_board", racing, raising=False)
    out = dump(target(p), VOLUME_NOTE, p["F"], project_id="pm")
    assert state["done"], "the dump read no fresh copy of Course"
    assert out.ok is False and out.notice == "Course changed while dumping — nothing dumped."
    assert p["C"].read_bytes() == written["bytes"]


async def test_TC_4533b_the_note_stays_when_the_board_changed_mid_dump(home, monkeypatch):
    """TC-4533b (LLR-4404.33, pilot): the same racing writer under the view → the notice, the note
    still in the pad."""
    async with capture(home, pad=VOLUME_NOTE) as (app, pilot, p):
        inbox = fx.inbox()
        real = boards.peek_board
        state = {"done": False}

        def racing(path):
            b = real(path)
            if not state["done"] and Path(path).resolve() == p["C"].resolve():
                state["done"] = True
                data = json.loads(p["C"].read_text(encoding="utf-8"))
                data["tasks"].append({"id": "tx1", "title": "Racer", "phase": "Todo"})
                p["C"].write_text(json.dumps(data, indent=2), encoding="utf-8")
            return b
        monkeypatch.setattr(boards, "peek_board", racing)
        monkeypatch.setattr(inbox, "peek_board", racing, raising=False)
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        one(app, "Course changed while dumping — nothing dumped.")
        assert pad_text(app) == VOLUME_NOTE
        assert "tx1" in fx.task_ids(p["C"])


def test_TC_4534_a_note_that_will_not_encode_dumps_nothing(tmp_path, monkeypatch):
    """TC-4534 (LLR-4404.34, SEC-2): `T\\ud800x` into the open board and into Course → ok False,
    `This note holds a character that cannot be saved — nothing dumped.`; the open board's file
    bytes and its live task count unchanged, Course's bytes unchanged (3/3). `Board.save`
    truncates the file before it fails to encode, so the refusal must come first. NC: no encode
    check (the open board's file left at 0 bytes)."""
    p, ids = s_dump(tmp_path, monkeypatch)
    live = Board.load(p["A"])
    a0, c0, n = file_bytes(p["A"]), file_bytes(p["C"]), len(live.tasks)
    msg = "This note holds a character that cannot be saved — nothing dumped."
    a = dump(target(p, "A", live), "T\ud800x", p["F"], project_id="pe")
    c = dump(target(p), "T\ud800x", p["F"], project_id="pm")
    assert (a.ok, a.notice) == (False, msg) and (c.ok, c.notice) == (False, msg)
    assert file_bytes(p["A"]) == a0 and len(live.tasks) == n and file_bytes(p["C"]) == c0


# --------------------------------------------------------------------------- #
# HLR-4405 — undo and the 7-day keep (the view's side)
# --------------------------------------------------------------------------- #
def _drop_task(path: Path, title: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    data["tasks"] = [t for t in data["tasks"] if t["title"] != title]
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def _edit_task(path: Path, title: str, **fields) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for t in data["tasks"]:
        if t["title"] == title:
            for k, v in fields.items():
                if callable(v):
                    t[k] = v(t.get(k))
                else:
                    t[k] = v
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


async def test_TC_4541_alt_u_undoes_the_newest_dump_first(home):
    """TC-4541 (LLR-4405.1): N1 dumped (Client A), then the volume note (Course); `alt+u` → the
    Course task gone, the Client A task kept; `alt+u` → the Client A task gone too (2/2). NC:
    undo the oldest."""
    async with capture(home, pad=f"{N1}\n____\n{N2T}") as (app, pilot, p):
        await dump_at(pilot, app, 0)
        await dump_at(pilot, app, 0)
        assert task_rec(p["A"], fx.N1_TITLE) and task_rec(p["C"], "Volume lab fails on WSL"), \
            fx.messages(app)
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        assert task_rec(p["C"], "Volume lab fails on WSL") is None
        assert task_rec(p["A"], fx.N1_TITLE) is not None
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        assert task_rec(p["A"], fx.N1_TITLE) is None


@pytest.mark.parametrize("pad, row, after", [
    (N2T, 0, N2T),
    (f"a\n____\n{N2T}", 2, f"a\n____\n{N2T}"),
])
async def test_TC_4543_the_undone_note_returns_at_the_pads_end(home, pad, row, after):
    """TC-4543 (LLR-4405.3, pilot): the note comes back at the pad's end — after a new divider
    when the pad holds text ("a" → "a\\n____\\n<note>"), alone in an empty pad (2/2). NC: no
    divider (the note would merge into `a`)."""
    async with capture(home, pad=pad) as (app, pilot, p):
        await dump_at(pilot, app, row)
        assert "Volume lab" not in pad_text(app), fx.messages(app)
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        assert pad_text(app) == after


@pytest.mark.parametrize("old", [False, True])
async def test_TC_4547_nothing_to_undo(home, old):
    """TC-4547 (LLR-4405.7): an empty `dumped`, and one entry 8 days old → `alt+u` shows `Nothing
    to undo.` and changes nothing (2/2). NC: IndexError."""
    pp = fx.f_paths(home)
    dumped = [fx.entry("old note", "t0ld", "Old note", pp["C"], "pv", at=fx.ago(days=8))] \
        if old else []
    async with capture(home, pad="x", dumped=dumped) as (app, pilot, p):
        before = fx.shas(p)
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.1)
        one(app, "Nothing to undo.")
        assert fx.shas(p) == before and pad_text(app) == "x"


async def test_TC_4549_a_task_deleted_since_gives_the_note_back(home):
    """TC-4549 (LLR-4405.9, with LLR-4405.8's pad arm): the volume note dumped, its task deleted
    from Course → `Volume lab fails on WSL is no longer on Course: the note is back in the pad.`;
    the pad ends with the note. NC: silent."""
    async with capture(home, pad=N2T) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        _drop_task(p["C"], "Volume lab fails on WSL")
        before = file_bytes(p["C"])
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        one(app, "Volume lab fails on WSL is no longer on Course: the note is back in the pad.")
        assert pad_text(app).endswith(N2T)
        assert file_bytes(p["C"]) == before


@pytest.mark.parametrize("edit", [
    {"title": "Volume lab fixed"}, {"phase": "Doing"}, {"due_date": "2026-11-05"},
    {"urls": ["https://example.com/x"]}, {"images": lambda v: (v or []) + ["C:/x/shot.png"]},
])
async def test_TC_4550b_an_edited_task_is_never_undone(home, edit):
    """TC-4550b (LLR-4405.10, pilot): after the dump, each of: the title edited, the phase moved,
    a due date set, a URL added, an image added → `alt+u` shows `Volume lab fails on WSL changed
    since the dump — undo left it.`, and the board, the pad and inbox.json keep their bytes (the
    owner's later work on the task is never thrown away). NC: compare title and notes only (the
    phase arm)."""
    async with capture(home, pad=N2T) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        _edit_task(p["C"], "Volume lab fails on WSL", **edit)
        before = (file_bytes(p["C"]), pad_text(app), file_bytes(p["store"]))
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        one(app, "Volume lab fails on WSL changed since the dump — undo left it.")
        assert (file_bytes(p["C"]), pad_text(app), file_bytes(p["store"])) == before


async def test_TC_4551b_a_busy_board_undoes_nothing(home, monkeypatch):
    """TC-4551b (LLR-4405.11, pilot): a held Course lock at the undo → a notice starting `Course
    could not be changed: ` and ending ` — nothing undone.`; pad and inbox.json unchanged (2/2).
    NC: the entry removed first."""
    monkeypatch.setattr(boards, "LOCK_WAIT", 0.2)
    async with capture(home, pad=N2T) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        write_lock(p["C"])
        before = (pad_text(app), file_bytes(p["store"]))
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.5)
        got = starting(app, "Course could not be changed: ")
        assert got and got[0].endswith(" — nothing undone."), fx.messages(app)
        assert (pad_text(app), file_bytes(p["store"])) == before


@pytest.mark.parametrize("n", [2, 0])
async def test_TC_4553_the_wide_rail_counts_the_kept_dumps(home, n):
    """TC-4553 (LLR-4405.13): 2 kept entries → the wide rail ends `✓ dumped 2  ·  alt+u undo  ·
    kept 7 days`; 0 → no such line (2/2). NC: the line missing."""
    pp = fx.f_paths(home)
    dumped = [fx.entry(f"kept {i}", f"tk{i}", f"Kept {i}", pp["C"], "pv", at=fx.ago(days=1))
              for i in range(n)]
    async with capture(home, pad=N3, dumped=dumped) as (app, pilot, p):
        lines = trimmed(fx.rail_lines(app))
        if n:
            assert lines[-1] == "✓ dumped 2  ·  alt+u undo  ·  kept 7 days", lines
        else:
            assert not any(x.startswith("✓ dumped") for x in lines), lines


async def test_TC_4554_a_dump_and_its_undo_leave_the_boards_undo_stack_alone(home):
    """TC-4554 (LLR-4405.14, R1-4): `len(app._undo_stack)` is the same before a dump, after it and
    after `alt+u`; after an open-board dump, `u` on the board leaves the dumped task (3/3). NC: a
    snapshot pushed on dump (the board's `u` would then delete the task behind the store's
    back)."""
    async with capture(home, pad=N1) as (app, pilot, p):
        n0 = len(app._undo_stack)
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        assert len(app._undo_stack) == n0
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        assert len(app._undo_stack) == n0 and pad_text(app) == N1
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        await fx.press(pilot, "escape")
        await pilot.pause(0.2)
        assert not fx.on_capture(app)
        await fx.press(pilot, "u")
        await pilot.pause(0.2)
        assert any(t.title == fx.N1_TITLE for t in app.board.tasks)
        assert task_rec(p["A"], fx.N1_TITLE) is not None


async def test_TC_4555_a_successful_undo_says_so(home):
    """TC-4555 (LLR-4405.15, P-V-12): the volume note dumped into Course, then `alt+u` → exactly 1
    notice `Undone: Volume lab fails on WSL left Course; the note is back in the pad.`, title
    `Capture`, markup False. NC: a silent success (the task left a board the owner cannot see)."""
    async with capture(home, pad=N2T) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        one(app, "Undone: Volume lab fails on WSL left Course; the note is back in the pad.")


@pytest.mark.parametrize("unc", [False, True])
async def test_TC_4556_an_entry_naming_an_unknown_board_undoes_nothing(home, monkeypatch, unc):
    """TC-4556 (LLR-4405.16, P-S-4, SEC-8): the newest entry's `board` is a board-shaped file in no
    lane → `<board> is not a known board — nothing undone.`; the entry kept; that file and both
    lane boards byte-unchanged; with `\\\\host\\share\\board.json` the same refusal and 0 `os.stat`
    / `os.path.samefile` calls on that string — the store's value reaches no file system call
    (4/4). NC: undo any `board` path (the outside file rewritten)."""
    pp = fx.f_paths(home)
    loose = home / "loose" / "board.json"
    if unc:
        board = "\\\\host\\share\\board.json"
    else:
        Board([Project("Loose", "pink", id="pl")],
              [Task("Loose task", project_id="pl", phase="Backlog", id="tl1")], loose,
              fx.settings(), ["Backlog", "Done"]).save()
        board = str(loose)
    dumped = [fx.entry("Loose task", "tl1", "Loose task", board, "pl", at=fx.ago(seconds=60))]
    async with capture(home, pad="x", dumped=dumped) as (app, pilot, p):
        before = [fx.sha(p["A"]), fx.sha(p["C"]), fx.sha(loose)]
        touched = []
        real_stat, real_same = os.stat, os.path.samefile

        def stat_spy(path, *a, **k):
            if "host" in str(path) and "share" in str(path):
                touched.append(("stat", str(path)))
            return real_stat(path, *a, **k)

        def same_spy(a, b):
            if any("host" in str(x) and "share" in str(x) for x in (a, b)):
                touched.append(("samefile", str(a), str(b)))
            return real_same(a, b)
        monkeypatch.setattr(os, "stat", stat_spy)
        monkeypatch.setattr(os.path, "samefile", same_spy)
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        monkeypatch.setattr(os, "stat", real_stat)
        monkeypatch.setattr(os.path, "samefile", real_same)
        one(app, f"{board} is not a known board — nothing undone.")
        assert [e["task"] for e in fx.read_store(home)["dumped"]] == ["tl1"]
        assert [fx.sha(p["A"]), fx.sha(p["C"]), fx.sha(loose)] == before
        if unc:
            assert touched == [], touched


async def test_TC_4557b_an_entry_undone_in_another_window_is_not_undone_twice(home):
    """TC-4557b (LLR-4405.17, pilot): N1 then the volume note dumped here; a second Inbox (another
    window) undoes the newest entry (its note restored in that window's pad); `alt+u` here →
    N1's task leaves Client A, and the volume note is in the pad once only (2/2). NC: read memory
    only (its note restored a second time)."""
    async with capture(home, pad=f"{N1}\n____\n{N2T}") as (app, pilot, p):
        await dump_at(pilot, app, 0)
        await dump_at(pilot, app, 0)
        Inbox = fx.need("inbox", "Inbox")
        other = Inbox.load(p["store"])
        e2 = other.dumped[-1]
        assert e2["title"] == "Volume lab fails on WSL", other.dumped
        other.write_pad(other.pad, drop=dict(e2))
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.3)
        assert task_rec(p["A"], fx.N1_TITLE) is None, fx.messages(app)
        assert pad_text(app).count("Volume lab fails on WSL") <= 1, pad_text(app)
        assert fx.read_store(home)["pad"].count("Volume lab fails on WSL") <= 1


async def test_TC_4559b_a_task_another_depends_on_is_not_undone(home):
    """TC-4559b (LLR-4405.19, SEC-3, pilot): after the volume note's dump, Course's `Volume oracle
    script` given `depends_on` [the new id] → `Another task depends on Volume lab fails on WSL —
    undo left it.`; board, pad and inbox.json bytes unchanged (2/2). NC: no dependency check (a
    dangling id left behind)."""
    async with capture(home, pad=N2T) as (app, pilot, p):
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        new = task_rec(p["C"], "Volume lab fails on WSL")
        assert new, fx.messages(app)
        _edit_task(p["C"], "Volume oracle script", depends_on=[new["id"]])
        before = (file_bytes(p["C"]), pad_text(app), file_bytes(p["store"]))
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        one(app, "Another task depends on Volume lab fails on WSL — undo left it.")
        assert (file_bytes(p["C"]), pad_text(app), file_bytes(p["store"])) == before


# --------------------------------------------------------------------------- #
# HLR-4408 — images on a note (the view's side)
# --------------------------------------------------------------------------- #
def _grab(monkeypatch, value):
    monkeypatch.setattr(app_module, "grab_clipboard_image", lambda: value, raising=False)


def _pil(size=(2, 2)):
    from PIL import Image
    return Image.new("RGB", size, (45, 212, 191))


@pytest.mark.parametrize("pad, after", [
    ("T\nx", "T\nx\nimg: paste-001.png\nimg: shot.png"),
    ("T\nx\n____\nb", "T\nx\nimg: paste-001.png\nimg: shot.png\n____\nb"),
])
async def test_TC_4614_alt_i_adds_one_image_line_per_image_after_the_note(home, monkeypatch,
                                                                          tmp_path, pad, after):
    """TC-4614 (LLR-4408.4): note "T\\nx", the cursor on `T`, a clipboard of 2 image files → the
    note becomes "T\\nx\\nimg: paste-001.png\\nimg: shot.png" — the lines after the note's last
    line, never mid-line at the cursor; before a divider they stay inside the note (1/1 + the
    divider arm). NC: inserted at the cursor."""
    u = tmp_path / "U"
    files = [png(u / "paste-001.png"), png(u / "shot.png", b"\x89PNG\r\n\x1a\nshot")]
    _grab(monkeypatch, [str(f) for f in files])
    async with capture(home, pad=pad, cursor=(0, 0)) as (app, pilot, p):
        await fx.press(pilot, "alt+i")
        await pilot.pause(0.2)
        assert pad_text(app) == after, fx.messages(app)
        assert (p["images"] / "shot.png").exists() and (u / "shot.png").exists()


async def test_TC_4615b_an_empty_clipboard_says_so(home, monkeypatch):
    """TC-4615b (LLR-4408.5, pilot): the clipboard holds nothing → `No image found in the
    clipboard.`; the pad unchanged. NC: silent."""
    _grab(monkeypatch, None)
    async with capture(home, pad="T") as (app, pilot, p):
        await fx.press(pilot, "alt+i")
        await pilot.pause(0.1)
        assert fx.notified(app, "No image found in the clipboard."), fx.messages(app)
        assert pad_text(app) == "T"


async def test_TC_4616b_a_clipboard_of_non_images_copies_nothing(home, monkeypatch, tmp_path):
    """TC-4616b (LLR-4408.6, pilot): a `.txt` and a `.svg` on the clipboard → `Clipboard holds no
    image files.`; 0 copies (2/2). NC: the `.svg` copied."""
    u = tmp_path / "U"
    u.mkdir()
    (u / "a.txt").write_text("x", encoding="utf-8")
    (u / "b.svg").write_text("<svg/>", encoding="utf-8")
    _grab(monkeypatch, [str(u / "a.txt"), str(u / "b.svg")])
    async with capture(home, pad="T") as (app, pilot, p):
        await fx.press(pilot, "alt+i")
        await pilot.pause(0.1)
        assert fx.notified(app, "Clipboard holds no image files."), fx.messages(app)
        assert not p["images"].exists() or list(p["images"].iterdir()) == []
        assert pad_text(app) == "T"


async def test_TC_4617b_a_failed_save_adds_no_image_line(home, monkeypatch):
    """TC-4617b (LLR-4408.7, pilot): saving the pasted bitmap fails → a notice starting `The image
    could not be saved: `; the pad unchanged (2/2). The read-only folder of the threshold cannot be
    made on Windows (a directory's read-only bit does not stop file creation), so the save is
    made to fail. NC: a line added for a missing file."""
    def boom(directory, image):
        raise OSError("read-only")
    monkeypatch.setattr(models, "save_pil_image", boom)
    monkeypatch.setattr(fx.inbox(), "save_pil_image", boom, raising=False)
    _grab(monkeypatch, _pil())
    async with capture(home, pad="T") as (app, pilot, p):
        await fx.press(pilot, "alt+i")
        await pilot.pause(0.1)
        assert starting(app, "The image could not be saved: "), fx.messages(app)
        assert pad_text(app) == "T"


async def test_TC_4618_alt_i_with_no_note_writes_no_file(home, monkeypatch):
    """TC-4618 (LLR-4408.8): an empty pad, `alt+i` with a bitmap on the clipboard → `No note under
    the cursor.`; 0 files in the pad images folder (2/2). NC: a note holding only the image line."""
    _grab(monkeypatch, _pil())
    async with capture(home) as (app, pilot, p):
        await fx.press(pilot, "alt+i")
        await pilot.pause(0.1)
        assert fx.notified(app, "No note under the cursor."), fx.messages(app)
        assert not p["images"].exists() or list(p["images"].iterdir()) == []
        assert pad_text(app) == ""


async def test_TC_4619_the_rail_counts_a_notes_images(home):
    """TC-4619 (LLR-4408.9): N2 (1 image line) → its title row ends `  ▣ 1`; N3 → no `▣` (2/2).
    NC: no count."""
    async with capture(home, pad=f"{N2}\n____\n{N3}", cursor=(0, 0)) as (app, pilot, p):
        titles = title_rows(fx.rail_lines(app))
        assert titles[0].endswith("  ▣ 1"), titles
        assert "▣" not in titles[1], titles


# --------------------------------------------------------------------------- #
# HLR-4409 — colour, mentions and untrusted text
# --------------------------------------------------------------------------- #
async def test_TC_4631_the_pad_colours_spans_live(home):
    """TC-4631 (LLR-4409.1): pad "::b:: x ::" → the cell of `x` in HEX["blue"] #60a5fa, the marker
    cells in HEX["dim"] #5b6675 — Inc C's live ink, as in the task editor's notes (2/2). NC: a
    plain TextArea."""
    async with capture(home, pad="::b:: x ::", cursor=(0, 10)) as (app, pilot, p):
        pad = fx.pad_of(app)
        r = pad.content_region
        cells = fx.painted(app)[r.y][r.x:r.x + r.width]
        text = "".join(c for c, _ in cells)
        assert text.startswith("::b:: x ::"), repr(text)
        assert cells[6][1] == "#60a5fa", cells[:10]
        assert {cells[i][1] for i in range(0, 5)} == {"#5b6675"}, cells[:10]


async def test_TC_4634_markup_in_notes_projects_and_boards_draws_literally(home):
    """TC-4634 (LLR-4409.4): a note titled `[red]x[/red] [@click=app.quit]q` is drawn literally in
    the rail row and the review row; a project named `[b]P[/b]`, made with `alt+n`, is literal in
    the dump notice and in its rail option; the app still runs (4/4). NC: `Text.from_markup` of the
    title (the tags vanish, the click becomes an action)."""
    title = "[red]x[/red] [@click=app.quit]q"
    async with capture(home, pad=f"{title}\n____\nVendor desk") as (app, pilot, p):
        await fx.cursor_to(pilot, app, 0, 0)
        assert any(title in x for x in title_rows(fx.rail_lines(app))), fx.rail_lines(app)
        await fx.press(pilot, "alt+a")
        await pilot.pause(0.2)
        body = fx.plain(fx.by_id(app, "rv-body", screen=app.screen))
        assert title in body, body
        await fx.press(pilot, "escape")
        await pilot.pause(0.1)
        await fx.cursor_to(pilot, app, 2, 0)
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "[b]P[/b]")
        await fx.press(pilot, "enter")
        await pilot.pause(0.2)
        one(app, "Dumped → [b]P[/b] · Client A   ·   alt+u undo")
        await fx.set_pad(pilot, app, f"{title}\n____\nvendor desk call")
        await pilot.pause(0.3)
        text = fx.rail_text(app)
        assert "[b]P[/b] · Client A" in text, fx.rail_lines(app)
        assert app.is_running and fx.on_capture(app)


# --------------------------------------------------------------------------- #
# Acceptance — black box, through keys and dialogs
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", [W118, W80])
async def test_AT_4401_type_divide_and_close_a_pad(home, size):
    """AT-4401 (K-1, K-2): `n` → the capture view with an empty pad: the ghost example, the hint
    row, head `CAPTURE  0 notes …`, rail `no notes yet`. Type `Golden set answer key`, `enter`,
    `____`, `enter` → the divider row draws as a rule, the one-time notice shows, head `2 notes`;
    `Pilot stores`, `alt+l` (a divider and a new line); `esc` → the store holds the pad verbatim and
    `divider_notice: true`; the boards, their histories, people.json and marks.json keep their
    bytes. At 80x24 the rail sits below the pad."""
    p = fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=size) as pilot:
        await fx.leave_home(pilot)
        before = fx.shas(p)
        await fx.open_capture(pilot, app)
        pad = fx.pad_of(app)
        assert [r.strip() for r in fx.region_rows(app, pad)][:4] == GHOST
        hint = fx.by_id(app, "cap-hint")
        assert fx.hint(app) == HINT
        assert hint.region.y == pad.region.y + pad.region.height, (hint.region, pad.region)
        assert fx.head(app) == "CAPTURE  0 notes · suggestions read every board"
        assert trimmed(fx.rail_lines(app)) == ["no notes yet"]
        await fx.type_text(pilot, "Golden set answer key\n____\n")
        await pilot.pause(0.3)
        rule = "".join(c for c, _ in _divider_screen_row(app, 1))
        assert rule == "─" * pad.content_region.width, repr(rule)
        one(app, DIVIDER_NOTICE)
        assert fx.read_store(home).get("divider_notice") is True
        assert fx.head(app) == "CAPTURE  2 notes · suggestions read every board"
        await fx.type_text(pilot, "Pilot stores")
        await fx.press(pilot, "alt+l")
        assert pad.text == "Golden set answer key\n____\nPilot stores\n____\n"
        assert pad.cursor_location == (4, 0)
        if size == W80:
            rail, prow = fx.by_id(app, "cap-rail-box").region, pad.region
            assert rail.y > prow.y + prow.height - 1 and rail.x == 0, (rail, prow)
        await fx.press(pilot, "escape")
        await pilot.pause(0.2)
        assert not fx.on_capture(app), fx.screen_names(app)
        store = fx.read_store(home)
        assert store["pad"] == "Golden set answer key\n____\nPilot stores\n____\n"
        assert store.get("divider_notice") is True
        assert fx.shas(p) == before


async def test_AT_4402_a_note_with_an_image_becomes_a_task_on_another_board(home):
    """AT-4402 (K-3, K-4, K-6): Client A (Eval harness, Pilot rollout) and Course (Module 4 ·
    Volumes); pad N2 with its image waiting in `inbox-images/`: the rail names `Module 4 · Volumes
    · Course` with `why volume · oracle · script`; `alt+d` → Course's file holds the task titled
    `Volume lab fails on WSL`, notes `the oracle script expects /mnt/c`, phase Todo, `created`
    stamped, the image moved into `images/<id>/`; the note gone from the pad; the dump notice."""
    pp = fx.f_paths(home)
    src = png(pp["images"] / "board-0938.png", b"\x89PNG\r\n\x1a\nboard-0938")
    data = src.read_bytes()
    async with capture(home, pad=N2) as (app, pilot, p):
        assert trimmed(fx.rail_lines(app)) == ["▌1 Volume lab fails on WSL  ▣ 1",
                                               "▌  → Module 4 · Volumes · Course ▰▰▰",
                                               "▌    why volume · oracle · script"]
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.3)
        rec = task_rec(p["C"], "Volume lab fails on WSL")
        assert rec is not None, fx.messages(app)
        assert rec["notes"] == "the oracle script expects /mnt/c" and rec["phase"] == "Todo"
        assert re.match(fx.STAMP_RE, rec.get("created") or "")
        dest = (p["C"].parent / "images" / rec["id"] / "board-0938.png").resolve()
        assert rec["images"] == [str(dest)] and dest.read_bytes() == data
        assert not src.exists()
        assert pad_text(app) == ""
        one(app, DUMP_COURSE)
        dumped = fx.read_store(home)["dumped"]
        assert len(dumped) == 1 and dumped[0]["images"] == ["board-0938.png"]


async def test_AT_4403_a_weak_note_goes_to_a_new_project_on_another_board(home, monkeypatch):
    """AT-4403 (K-4): a note whose best hit is weak → `+ new project`; `alt+o` cycles to the weak
    hit and back; `alt+n`, `tab` → Course (P-V-1), `Contracts pilot`, `enter` → Course holds the
    project (the first free hue, lime) and the task in one write; a duplicate name is refused with
    its notice."""
    async with capture(home, pad=N5) as (app, pilot, p):
        lines = trimmed(fx.rail_lines(app))
        assert lines[1:3] == ["▌  → + new project", "▌    weak: chair · region (Pilot rollout)"]
        await fx.press(pilot, "alt+o")
        assert arrow_rows(fx.rail_lines(app))[0] == "▌  → Pilot rollout · Client A ▰▱▱"
        await fx.press(pilot, "alt+o")
        assert arrow_rows(fx.rail_lines(app))[0] == "▌  → + new project"
        await fx.press(pilot, "alt+n")
        assert border_title(field(app)) == "New project for note 1"
        assert fx.keys_row(app) == "↵ create on Client A + dump   ⇥ board   esc back"
        await fx.post_key(pilot, "tab", "\t")
        assert fx.keys_row(app) == "↵ create on Course + dump   ⇥ board   esc back"
        await fx.type_text(pilot, "Contracts pilot")
        writes = []
        real = Board.save_atomic

        def spy(self):
            writes.append(Path(self.path).resolve())
            return real(self)
        monkeypatch.setattr(Board, "save_atomic", spy)
        await fx.press(pilot, "enter")
        await pilot.pause(0.3)
        proj = next((x for x in project_recs(p["C"]) if x["name"] == "Contracts pilot"), None)
        assert proj is not None and proj["color"] == "lime", (project_recs(p["C"]),
                                                              fx.messages(app))
        task = task_rec(p["C"], "Answer the region chair")
        assert task and task["project_id"] == proj["id"]
        assert writes.count(p["C"].resolve()) == 1, writes
        assert "Answer the region chair" not in pad_text(app)
        await fx.type_text(pilot, "Client call")
        await fx.press(pilot, "alt+n")
        await fx.post_key(pilot, "tab", "\t")
        await fx.type_text(pilot, "contracts PILOT")
        await fx.press(pilot, "enter")
        await pilot.pause(0.2)
        assert holding(app, "Course already has a project named"), fx.messages(app)
        assert sum(x["name"].casefold() == "contracts pilot" for x in project_recs(p["C"])) == 1


async def test_AT_4404_undo_the_dumps_newest_first(home):
    """AT-4404 (K-4): two dumps; `alt+u` → the second task leaves its board and its note returns
    at the pad's end after a divider; `alt+a`, `u` → the first undone too; a third `alt+u` →
    `Nothing to undo.`; an entry dated 8 days ago is dropped from `dumped` at the next write."""
    pad = f"{N1}\n____\n{N2T}\n____\nkeep me"
    async with capture(home, pad=pad) as (app, pilot, p):
        await dump_at(pilot, app, row_of(pad_text(app), "Volume lab"))
        await dump_at(pilot, app, 0)
        assert pad_text(app) == "keep me", (pad_text(app), fx.messages(app))
        assert task_rec(p["A"], fx.N1_TITLE) and task_rec(p["C"], "Volume lab fails on WSL")
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.2)
        assert task_rec(p["A"], fx.N1_TITLE) is None
        assert pad_text(app) == f"keep me\n____\n{N1}"
        await fx.press(pilot, "alt+a")
        await pilot.pause(0.2)
        assert type(app.screen).__name__ == "ReviewList", fx.screen_names(app)
        await fx.press(pilot, "u")
        await pilot.pause(0.3)
        assert task_rec(p["C"], "Volume lab fails on WSL") is None
        body = fx.plain(fx.by_id(app, "rv-body", screen=app.screen)).split("\n")
        assert sum(("[x]" in x or "[ ]" in x) for x in body) == 3, body
        await fx.press(pilot, "escape")
        await pilot.pause(0.2)
        assert fx.on_capture(app)
        assert pad_text(app) == f"keep me\n____\n{N1}\n____\n{N2T}"
        await fx.press(pilot, "alt+u")
        await pilot.pause(0.1)
        one(app, "Nothing to undo.")
        data = fx.read_store(home)
        data["dumped"].append(fx.entry("stale note", "tst1", "Stale note", p["C"], "pv",
                                       at=fx.ago(days=8)))
        p["store"].write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        await fx.cursor_to(pilot, app, 0, len("keep me"))
        await fx.type_text(pilot, "!")
        await pilot.pause(1.3)
        assert all(e["task"] != "tst1" for e in fx.read_store(home)["dumped"])


async def test_AT_4407_colour_mentions_and_an_image_carry_over_and_markup_stays_text(
        home, monkeypatch):
    """AT-4407 (HLR-4409, K-6): note `Vendor call\\n::b:: ask the vendor :: @username_subject` with a
    clipboard image via `alt+i`: the pad shows `ask the vendor` in blue; the dump (into a new
    project) keeps the span and the mention verbatim in the task's notes and the image in its
    folder; a note titled `[red]x[/red]` shows literally in the rail, and a project named
    `[b]P[/b]` (made with `alt+n`) literally in the dump notice (P-V-9, P-V-11)."""
    _grab(monkeypatch, _pil())
    note = "Vendor call\n::b:: ask the vendor :: @username_subject"
    async with capture(home, pad=note) as (app, pilot, p):
        await fx.press(pilot, "alt+i")
        await pilot.pause(0.2)
        assert pad_text(app) == note + "\nimg: paste-001.png", fx.messages(app)
        assert (p["images"] / "paste-001.png").exists()
        pad = fx.pad_of(app)
        r = pad.content_region
        cells = fx.painted(app)[r.y + 1][r.x:r.x + r.width]
        line = "".join(c for c, _ in cells)
        i = line.index("ask the vendor")
        assert {fg for _, fg in cells[i:i + len("ask the vendor")]} == {"#60a5fa"}, cells[i:i + 14]
        await fx.cursor_to(pilot, app, 0, 0)
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "Vendor desk")
        await fx.press(pilot, "enter")
        await pilot.pause(0.3)
        rec = task_rec(p["A"], "Vendor call")
        assert rec is not None, fx.messages(app)
        assert rec["notes"] == "::b:: ask the vendor :: @username_subject"
        dest = (p["A"].parent / "images" / rec["id"] / "paste-001.png").resolve()
        assert rec["images"] == [str(dest)] and dest.exists()
        await fx.set_pad(pilot, app, "[red]x[/red]")
        await pilot.pause(0.3)
        assert "▌1 [red]x[/red]" in fx.rail_lines(app), fx.rail_lines(app)
        await fx.press(pilot, "alt+n")
        await fx.type_text(pilot, "[b]P[/b]")
        await fx.press(pilot, "enter")
        await pilot.pause(0.3)
        one(app, "Dumped → [b]P[/b] · Client A   ·   alt+u undo")


# --------------------------------------------------------------------------- #
# HLR-4406 — the review list (alt+a), and AT-4405
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# HLR-4406 — the batch review list (`alt+a`, variant C) · TC-4561..TC-4577 · AT-4405
# (+ TC-4484c, the batch's one corpus rebuild). Staged by fork A; relies on this module's header.
# --------------------------------------------------------------------------- #
RV_PAD4 = "\n____\n".join([fx.N1, fx.N2, fx.N3, fx.N4])
RV_N4_TITLE = "Steering deck: demo the hybrid search on pilot stores"
RV_N3_TITLE = "Quote for the new client: contracts Q&A"
RV_KEYS3 = "↑↓ move   ␣ include   o other   d dump 3 checked   u undo   esc back"
RUBRIC_PAD = "Rubric review\n____\nRubric scoring\n____\nPilot judge rubric\n____\nRubric for the pilot"


def _rv_image(home):
    """N2's `img: board-0938.png` names a real pad image (a byte file; the dump copies bytes)."""
    folder = home / "inbox-images"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "board-0938.png").write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-board-0938")


def _rv_setup(home, pad: str = RV_PAD4, image: bool = True) -> dict:
    p = fx.build_f(home)
    if image:
        _rv_image(home)
    fx.write_store(home, pad=pad)
    return p


def _rv_on(app) -> bool:
    return type(app.screen).__name__ == "ReviewList"


async def _rv_open(pilot, app):
    """`alt+a` from the pad; fails here, with a message, when no review list opens."""
    await fx.press(pilot, "alt+a")
    await pilot.pause(0.2)
    assert _rv_on(app), f"`alt+a` opened no review list: screen stack {fx.screen_names(app)}"
    return app.screen


async def _rv_start(pilot, app, cursor=(0, 0)):
    await fx.leave_home(pilot)
    await fx.open_capture(pilot, app)
    await fx.cursor_to(pilot, app, *cursor)


def _rv_body(app) -> list[str]:
    return [x.rstrip() for x in fx.plain(fx.by_id(app, "rv-body", screen=app.screen)).split("\n")]


def _rv_rows(app) -> list[dict]:
    """The review rows as drawn: cursor mark, check box, the rest of the first line."""
    rows = []
    for line in _rv_body(app):
        if line[:2] in ("▶ ", "  ") and line[2:6] in ("[x] ", "[ ] "):
            rows.append({"cursor": line[:2] == "▶ ", "checked": line[2:6] == "[x] ",
                         "rest": line[6:], "line": line})
    return rows


def _rv_checks(app) -> list[bool]:
    return [r["checked"] for r in _rv_rows(app)]


def _rv_sel(app) -> int:
    marks = [i for i, r in enumerate(_rv_rows(app)) if r["cursor"]]
    assert len(marks) == 1, f"expected one cursor row, got {marks}"
    return marks[0]


def _rv_key_row(app) -> str:
    lines = [x for x in _rv_body(app) if x.strip()]
    return lines[-1]


def _rv_titles(path) -> list[tuple[str, str]]:
    return [(t["title"], t.get("project_id")) for t in fx.tasks_of(path)]


def _rv_pad(app) -> str:
    return fx.pad_of(app).text


async def test_TC_4561_alt_a_opens_one_row_per_note_of_the_pad_as_it_is_now(home):
    """TC-4561 (LLR-4406.1): N1..N3 in the store, N4 typed 0.2 s before `alt+a` → 4 rows in
    pad order, over the capture view, a ModalScreen (NC rows from the store's last write: N4
    missing)."""
    from textual.screen import ModalScreen
    _rv_setup(home, pad="\n____\n".join([fx.N1, fx.N2, fx.N3]))
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        pad = fx.pad_of(app)
        pad.move_cursor(pad.document.end)
        await pilot.pause()
        await fx.press(pilot, "enter")
        await fx.type_text(pilot, "____\n" + RV_N4_TITLE)
        await pilot.pause(0.2)
        await _rv_open(pilot, app)
        assert isinstance(app.screen, ModalScreen)
        assert fx.captures_on_stack(app) == 1
        rows = _rv_rows(app)
        assert len(rows) == 4
        assert [r["rest"].startswith(t) for r, t in zip(rows, [
            fx.N1_TITLE, fx.N2_TITLE, RV_N3_TITLE, RV_N4_TITLE])] == [True] * 4


async def test_TC_4562_each_row_draws_cursor_box_title_option_and_a_why_line(home):
    """TC-4562 (LLR-4406.2): the 4-row fixture at 118x30 (body width 108) → the graph's plain
    lines exactly (title padded to 66, the option at column 74, a second `why` line or
    `needs a name: alt+n in the pad`, then the key row) (NC no second line)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        want = [
            "▶ [x] " + fx.N1_TITLE.ljust(66) + "  Eval harness · Client A ▰▰▰",
            "      why questions · @username_subject · key",
            "  [x] " + fx.N2_TITLE.ljust(66) + "  Module 4 · Volumes · Course ▰▰▰",
            "      why volume · oracle · script",
            "  [ ] " + RV_N3_TITLE.ljust(66) + "  + new project",
            "      needs a name: alt+n in the pad",
            "  [x] " + RV_N4_TITLE.ljust(66) + "  Pilot rollout · Client A ▰▰▰",
            "      why pilot · stores · steering",
            "",
            RV_KEYS3,
        ]
        body = _rv_body(app)
        while body and not body[-1]:
            body.pop()
        assert body == want


async def test_TC_4563_rows_open_checked_for_a_project_and_unchecked_for_new_project(home):
    """TC-4563 (LLR-4406.3): N1, N2, N4 (a project each) open `[x]`, N3 (`+ new project`)
    `[ ]` (NC all checked)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert _rv_checks(app) == [True, True, False, True]


async def test_TC_4564_up_and_down_move_the_cursor_clamped_to_the_rows(home):
    """TC-4564 (LLR-4406.4): `↑` at row 0 stays 0; `↓` ×9 on 4 rows ends at 3 (NC no
    clamp)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert _rv_sel(app) == 0
        await fx.press(pilot, "up")
        assert _rv_sel(app) == 0
        await fx.press(pilot, *(["down"] * 9))
        assert _rv_sel(app) == 3
        assert _rv_on(app)


async def test_TC_4565_space_toggles_a_project_rows_check(home):
    """TC-4565 (LLR-4406.5): row 1 `[x]` → `space` `[ ]` → `space` `[x]` (NC one-way)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert _rv_checks(app)[0] is True
        await fx.press(pilot, "space")
        assert _rv_checks(app)[0] is False
        await fx.press(pilot, "space")
        assert _rv_checks(app)[0] is True


async def test_TC_4566_space_on_a_new_project_row_is_refused_with_a_notice(home):
    """TC-4566 (LLR-4406.6): `space` on N3's row → it stays `[ ]`; notice `Needs a name:
    alt+n in the pad.` (NC checkable)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        await fx.press(pilot, "down", "down", "space")
        assert _rv_sel(app) == 2
        assert _rv_checks(app) == [True, True, False, True]
        got = fx.notified(app, "Needs a name: alt+n in the pad.")
        assert len(got) == 1 and got[0].markup is False


async def test_TC_4567_o_picks_the_next_option_shared_with_the_rail(home):
    """TC-4567 (LLR-4406.7, ARCH-2): `o` on row 1 (N1) → row 1 shows `Pilot rollout · Client A
    ▰▰▱`; after `esc` the rail's N1 `→` line shows the same option (NC a review-local choice:
    the rail still shows Eval harness)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        await fx.press(pilot, "o")
        row = _rv_rows(app)[0]
        assert row["rest"].rstrip().endswith("Pilot rollout · Client A ▰▰▱"), row["line"]
        await fx.press(pilot, "escape")
        assert fx.on_capture(app)
        arrows = [x.strip("▌ ") for x in fx.rail_lines(app) if x.strip("▌ ").startswith("→")]
        assert arrows, fx.rail_text(app)
        assert arrows[0] == "→ Pilot rollout · Client A ▰▰▱", fx.rail_text(app)


async def test_TC_4568_d_dumps_every_checked_row_and_only_those(home):
    """TC-4568 (LLR-4406.8): 3 of 4 checked (N1, N2, N4) → `d` → N1 in Eval harness and N4 in
    Pilot rollout on Client A, N2 in Module 4 · Volumes on Course; the pad holds N3 only (NC
    unchecked rows dumped too: a 4th task)."""
    p = _rv_setup(home)
    a0, c0 = len(fx.tasks_of(p["A"])), len(fx.tasks_of(p["C"]))
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        assert _rv_pad(app) == fx.N3
    a, c = _rv_titles(p["A"]), _rv_titles(p["C"])
    assert len(a) == a0 + 2 and len(c) == c0 + 1
    assert a[-2:] == [(fx.N1_TITLE, "pe"), (RV_N4_TITLE, "pr")]
    assert c[-1] == (fx.N2_TITLE, "pv")
    assert not any(t == RV_N3_TITLE for t, _ in a + c)


async def test_TC_4569_the_review_list_closes_when_the_batch_ends(home):
    """TC-4569 (LLR-4406.9): after `d` the capture view is on top (NC the list stays open)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        assert fx.on_capture(app), fx.screen_names(app)
        assert not any(n == "ReviewList" for n in fx.screen_names(app))


async def test_TC_4570_a_failed_row_stays_in_the_pad_and_the_batch_goes_on(home):
    """TC-4570 (LLR-4406.10): 3 checked, the 2nd row's board (Course) deleted before `d` →
    rows 1 and 3 dumped, N2 still in the pad, notices `Course's file is missing — nothing
    dumped.` and `Dumped 2 of 3 checked` (NC stop at the first failure: N4 not dumped)."""
    p = _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        p["C"].unlink()
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        text = _rv_pad(app)
        assert fx.N2 in text and fx.N3 in text
        assert fx.N1 not in text and RV_N4_TITLE not in text
        assert len(fx.notified(app, "Course's file is missing — nothing dumped.")) == 1
        assert len(fx.notified(app, "Dumped 2 of 3 checked")) == 1
    assert not p["C"].exists()
    a = _rv_titles(p["A"])
    assert (fx.N1_TITLE, "pe") in a and (RV_N4_TITLE, "pr") in a


async def test_TC_4571_u_undoes_the_newest_dump_and_rebuilds_the_rows(home):
    """TC-4571 (LLR-4406.11): N2 dumped earlier with `alt+d`, the review open on N1 alone,
    `u` → N2's task leaves Course and its note appears as row 2 `[x]` (NC `u` unbound)."""
    p = _rv_setup(home, pad=fx.N1 + "\n____\n" + fx.N2)
    c0 = fx.task_ids(p["C"])
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app, cursor=(3, 0))
        await fx.press(pilot, "alt+d")
        await pilot.pause(0.2)
        assert len(fx.task_ids(p["C"])) == len(c0) + 1, "alt+d dumped nothing"
        await fx.cursor_to(pilot, app, 0, 0)
        await _rv_open(pilot, app)
        assert len(_rv_rows(app)) == 1
        await fx.press(pilot, "u")
        await pilot.pause(0.2)
        assert _rv_on(app)
        rows = _rv_rows(app)
        assert len(rows) == 2
        assert rows[1]["rest"].startswith(fx.N2_TITLE) and rows[1]["checked"] is True
    assert fx.task_ids(p["C"]) == c0


async def test_TC_4572_esc_closes_the_review_list_and_changes_nothing(home):
    """TC-4572 (LLR-4406.12): `esc` → the capture view on top; boards, histories and
    inbox.json bytes unchanged (NC `esc` closes the capture view too)."""
    p = _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        before = fx.shas(p) + [fx.sha(p["store"])]
        await _rv_open(pilot, app)
        await fx.press(pilot, "escape")
        await pilot.pause(0.2)
        assert fx.on_capture(app), fx.screen_names(app)
        assert fx.shas(p) + [fx.sha(p["store"])] == before


async def test_TC_4573_the_key_row_counts_the_checked_rows(home):
    """TC-4573 (LLR-4406.13): the key row reads `d dump 3 checked`, then `d dump 2 checked`
    after one `space` (NC fixed `dump checked`); at 80x24 all 6 key glyphs are present."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert _rv_key_row(app) == RV_KEYS3
        await fx.press(pilot, "space")
        assert "d dump 2 checked" in _rv_key_row(app)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W80) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        row = _rv_key_row(app)
        for glyph in ("↑↓", "␣", "o", "d", "u", "esc"):
            assert glyph in row, (glyph, row)
        assert "d dump 3 checked" in row


async def test_TC_4574_alt_a_on_a_pad_with_no_note_opens_nothing(home):
    """TC-4574 (LLR-4406.14): empty pad, `alt+a` → notice `No notes to review.`, the capture
    view stays on top (NC an empty modal)."""
    fx.build_f(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        await fx.press(pilot, "alt+a")
        await pilot.pause(0.2)
        assert fx.on_capture(app), fx.screen_names(app)
        got = fx.notified(app, "No notes to review.")
        assert len(got) == 1 and got[0].markup is False


async def test_TC_4575_typed_keys_in_the_review_list_never_reach_the_pad(home):
    """TC-4575 (LLR-4406.15): `x` and `a` typed in the review list → the pad text unchanged
    and Client A's task count unchanged (`a` is add-task on the board) (NC not modal)."""
    p = _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        before, n = _rv_pad(app), len(app.board.tasks)
        await _rv_open(pilot, app)
        await fx.press(pilot, "x", "a")
        assert _rv_on(app), fx.screen_names(app)
        assert len(app.board.tasks) == n
        await fx.press(pilot, "escape")
        assert _rv_pad(app) == before
    assert len(fx.tasks_of(p["A"])) == n


async def test_TC_4576_the_batch_ends_with_dumped_k_of_n_checked(home):
    """TC-4576 (LLR-4406.16): all 3 checked rows succeed → exactly one notice `Dumped 3 of 3
    checked`, markup False (NC no notice)."""
    _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        got = fx.notified(app, "Dumped 3 of 3 checked")
        assert len(got) == 1 and got[0].markup is False


async def test_TC_4577_every_checked_rows_target_is_fixed_before_the_first_dump(home):
    """TC-4577 (LLR-4406.17, ARCH-2): rows `Rubric review`, `Rubric scoring` (`o` once each →
    Eval harness, then `space`), `Pilot judge rubric` (top Eval harness 0.2889) and `Rubric for
    the pilot` (top Pilot rollout 0.2232), all checked, `d` → the first 3 in Eval harness and
    `Rubric for the pilot` in Pilot rollout, the option its row showed (NC each target
    re-resolved after the earlier dumps: Eval harness 0.6028)."""
    p = _rv_setup(home, pad=RUBRIC_PAD, image=False)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert _rv_checks(app) == [False, False, True, True]
        rows = _rv_rows(app)
        assert rows[2]["rest"].rstrip().endswith("Eval harness · Client A ▰▰▱"), rows[2]["line"]
        assert rows[3]["rest"].rstrip().endswith("Pilot rollout · Client A ▰▰▱"), rows[3]["line"]
        await fx.press(pilot, "o", "space", "down", "o", "space")
        rows = _rv_rows(app)
        assert [r["checked"] for r in rows] == [True, True, True, True]
        for r in rows[:2]:
            assert "Eval harness · Client A" in r["rest"], r["line"]
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        assert len(fx.notified(app, "Dumped 4 of 4 checked")) == 1
    new = {t: pid for t, pid in _rv_titles(p["A"])}
    assert {k: new.get(k) for k in ("Rubric review", "Rubric scoring", "Pilot judge rubric",
                                    "Rubric for the pilot")} == {
        "Rubric review": "pe", "Rubric scoring": "pe", "Pilot judge rubric": "pe",
        "Rubric for the pilot": "pr"}


async def test_TC_4484c_a_review_batch_rebuilds_the_documents_once_after_its_dumps(
        home, monkeypatch):
    """TC-4484c (LLR-4403.24, ARCH-2/ARCH-6): a batch of 3 checked rows → exactly 1 `corpus`
    call, after the batch's last dump and 0 between its dumps (spies on taskboard.app.corpus
    and taskboard.app.dump_note) (NC a rebuild per dump: 3 calls)."""
    real_corpus = fx.need(app_module, "corpus")
    real_dump = fx.need(app_module, "dump_note")
    events_seen: list[str] = []

    def corpus_spy(*a, **k):
        events_seen.append("corpus")
        return real_corpus(*a, **k)

    def dump_spy(*a, **k):
        events_seen.append("dump")
        return real_dump(*a, **k)
    monkeypatch.setattr(app_module, "corpus", corpus_spy, raising=False)
    monkeypatch.setattr(app_module, "dump_note", dump_spy, raising=False)
    _rv_setup(home, pad="\n____\n".join([fx.N1, fx.N2, fx.N4]))
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert _rv_checks(app) == [True, True, True]
        events_seen.clear()
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        assert events_seen.count("dump") == 3, events_seen
        assert events_seen.count("corpus") == 1, events_seen
        assert events_seen[-1] == "corpus", events_seen


async def test_AT_4405_review_four_notes_refuse_one_switch_one_dump_three(home):
    """AT-4405 (K-1 variant C, HLR-4406): fixture F, pad N1..N4: `n`, `alt+a` → 4 rows, rows 1,
    2, 4 `[x]`; `↓ ↓ space` → row 3 stays `[ ]` with `Needs a name: alt+n in the pad.`; `↑ ↑ o`
    → row 1 `Pilot rollout · Client A ▰▰▱`; `d` → Client A holds N1's task (Pilot rollout) and
    N4's (Pilot rollout), Course holds N2's with its image moved; `Dumped 3 of 3 checked`; the
    capture view on top; the pad is N3."""
    p = _rv_setup(home)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await _rv_start(pilot, app)
        await _rv_open(pilot, app)
        assert len(_rv_rows(app)) == 4
        assert _rv_checks(app) == [True, True, False, True]
        await fx.press(pilot, "down", "down", "space")
        assert _rv_checks(app)[2] is False
        assert len(fx.notified(app, "Needs a name: alt+n in the pad.")) == 1
        await fx.press(pilot, "up", "up", "o")
        assert _rv_rows(app)[0]["rest"].rstrip().endswith("Pilot rollout · Client A ▰▰▱")
        await fx.press(pilot, "d")
        await pilot.pause(0.2)
        assert len(fx.notified(app, "Dumped 3 of 3 checked")) == 1
        assert fx.on_capture(app), fx.screen_names(app)
        assert _rv_pad(app) == fx.N3
    a = _rv_titles(p["A"])
    assert (fx.N1_TITLE, "pr") in a and (RV_N4_TITLE, "pr") in a
    c = fx.tasks_of(p["C"])
    n2 = [t for t in c if t["title"] == fx.N2_TITLE]
    assert len(n2) == 1 and n2[0]["project_id"] == "pv"
    assert n2[0]["notes"] == "the oracle script expects /mnt/c"
    moved = p["C"].parent / "images" / n2[0]["id"] / "board-0938.png"
    assert moved.exists()
    assert not (home / "inbox-images" / "board-0938.png").exists()


# --------------------------------------------------------------------------- #
# AT-4406, AT-4408 — the store, black box
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# AT-4406 and AT-4408 (staged by the store tester; pasted after the other ATs)
# --------------------------------------------------------------------------- #
_ST_NOTE_B = "Volume lab fails on WSL\nthe oracle script expects /mnt/c"


def _st_inbox():
    return fx.need("inbox", "Inbox")


def _st_hold_lock(path, monkeypatch, wait: float = 0.3) -> Path:
    monkeypatch.setattr(boards, "LOCK_WAIT", wait)
    lock = Path(path).resolve()
    lock = lock.with_name(lock.name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_bytes(b"0123456789abcdef0123456789abcdef")
    return lock


def _st_fail_store_once(monkeypatch) -> dict:
    real = models.write_atomic
    box = {"left": 1}

    def w(path, text):
        if Path(path).name == "inbox.json" and box["left"] > 0:
            box["left"] -= 1
            raise OSError("disk full")
        return real(path, text)
    monkeypatch.setattr(models, "write_atomic", w)
    monkeypatch.setattr(fx.inbox(), "write_atomic", w, raising=False)
    return box


def _st_pad(app) -> str:
    return fx.pad_of(app).text


def _st_titled(path, title) -> int:
    return sum(t["title"] == title for t in fx.tasks_of(path))


async def test_AT_4406_the_store_survives_corruption_a_busy_lock_and_a_failed_write(
        home, monkeypatch):
    """AT-4406 (K-5; HLR-4407): an unreadable `inbox.json` (`{"pad": 5}`) → `n` shows the
    empty pad and the set-aside notice, `inbox.json.corrupt` equals the bad bytes; a held
    `inbox.json.lock` → typing then waiting gives the save notice and the pad keeps the
    text; `esc` warns once, `esc` again closes. A store write failing right after a dump →
    the task is on its board, the note leaves the pad, the notice says the save is retried;
    the next successful write stores the dumped entry and `alt+u` undoes that dump (ARCH-4:
    no flagged note)."""
    p = fx.build_f(home)
    fx.write_store(home, raw='{"pad": 5}')
    course_ids = fx.task_ids(p["C"])
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        assert _st_pad(app) == ""
        aside = ("inbox.json could not be read; it was copied to inbox.json.corrupt and the "
                 "pad starts empty.")
        assert len(fx.notified(app, aside)) == 1, fx.messages(app)
        assert (home / "inbox.json.corrupt").read_bytes() == b'{"pad": 5}'

        lock = _st_hold_lock(p["store"], monkeypatch)
        await fx.type_text(pilot, "x")
        await pilot.pause(2.0)
        saved = [m for m in fx.messages(app) if m.startswith("inbox.json could not be saved: ")]
        assert saved and "is busy" in saved[0], fx.messages(app)
        assert _st_pad(app) == "x"
        warn = "inbox.json could not be saved — esc again closes without saving."
        await fx.press(pilot, "escape")
        assert fx.on_capture(app) and len(fx.notified(app, warn)) == 1
        await fx.press(pilot, "escape")
        await pilot.pause(0.5)
        assert not fx.on_capture(app)
        lock.unlink()

        await fx.open_capture(pilot, app)
        await fx.set_pad(pilot, app, _ST_NOTE_B, cursor=(0, 0))
        _st_fail_store_once(monkeypatch)
        await fx.press(pilot, "alt+d")
        new = [t for t in fx.task_ids(p["C"]) if t not in course_ids]
        assert len(new) == 1, "the dump put no task on Course"
        assert "Volume lab fails on WSL" not in _st_pad(app)
        retried = [m for m in fx.messages(app)
                   if m.startswith("Module 4 · Volumes · Course got the task, but inbox.json "
                                   "could not be saved: ")
                   and m.endswith(" — it is retried at the next save.")]
        assert len(retried) == 1, fx.messages(app)

        await fx.type_text(pilot, "y")
        await pilot.pause(1.3)
        data = fx.read_store(home)
        assert [d["task"] for d in data["dumped"]] == new
        assert data["pad"] == _st_pad(app) == "y"

        await fx.press(pilot, "alt+u")
        assert fx.task_ids(p["C"]) == course_ids
        assert _st_pad(app) == "y\n____\n" + _ST_NOTE_B
        assert fx.read_store(home)["dumped"] == []


async def test_AT_4408_two_windows_on_one_store_lose_no_note_and_dump_none_twice(home):
    """AT-4408 (K-5, D1; HLR-4407 · LLR-4407.19, .48, .49): a second window (a second
    `Inbox`) dumps note `b` and adds note `c` while this pad (`a`, `b`) adds `d`: the next
    write writes the union `a`, `c`, `d` (`b` is an unseen entry), shows the merge notice,
    and no task is created twice. ARCH-1 arms, each with the file changed by the second
    window first: (D) this pad `a|b` dumps `b` while the second window's pad is `a|b|c` →
    the stored pad `a|c`, `b` never back; (U) this window undoes its dump of `b` over a
    fresh pad `a|c|d` → the stored pad `a|c|d|b`, `b` once; (R) a note `follow up` re-typed
    here, whose earlier dump this window already knew → kept in the stored pad."""
    p = fx.build_f(home)
    Inbox = _st_inbox()
    merged = "inbox.json changed in another window: its notes were merged into the pad."

    # the union: the other window dumps `b` and writes `a|c`; this one types `d`
    fx.write_store(home, pad="a\n____\nb", divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        y = Inbox.load(p["store"])
        out = fx.need("inbox", "dump_note")(
            fx.need("inbox", "DumpTarget")(p["C"], "Course", None), "pv", None, "b",
            y.images_dir, "Module 4 · Volumes")
        assert out.ok, out.notice
        y.write_pad("a\n____\nc", record=fx.need("inbox", "entry_for")(
            out, "b", p["C"], datetime.now()))
        pad = fx.pad_of(app)
        pad.move_cursor(pad.document.end)
        await pilot.pause()
        await fx.type_text(pilot, "\n____\nd")
        await pilot.pause(1.3)
        assert fx.read_store(home)["pad"] == "a\n____\nc\n____\nd"
        assert _st_pad(app) == "a\n____\nc\n____\nd"
        assert len(fx.notified(app, merged)) == 1, fx.messages(app)
        assert _st_titled(p["C"], "b") == 1 and _st_titled(p["A"], "b") == 0

    # (D) the dump of `b` here over the other window's `a|b|c`
    fx.write_store(home, pad="a\n____\n" + _ST_NOTE_B, divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        y = Inbox.load(p["store"])
        y.write_pad("a\n____\n" + _ST_NOTE_B + "\n____\nc")
        await fx.cursor_to(pilot, app, 2, 0)
        await fx.press(pilot, "alt+d")
        data = fx.read_store(home)
        assert data["pad"] == "a\n____\nc"
        assert [d["text"] for d in data["dumped"]][-1] == _ST_NOTE_B
        assert _st_pad(app) == "a\n____\nc"
        y.write_pad("a\n____\n" + _ST_NOTE_B + "\n____\nc\n____\ne")
        assert "Volume lab fails on WSL" not in fx.read_store(home)["pad"]
        assert _st_titled(p["C"], "Volume lab fails on WSL") == 1

    # (U) the undo of `b` here over the other window's `a|c|d`
    for t in [t["id"] for t in fx.tasks_of(p["C"]) if t["title"] == "Volume lab fails on WSL"]:
        b = Board.load(p["C"])
        b.tasks = [x for x in b.tasks if x.id != t]
        b.save_atomic()
    fx.write_store(home, pad="a\n____\n" + _ST_NOTE_B, divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        await fx.cursor_to(pilot, app, 2, 0)
        await fx.press(pilot, "alt+d")
        assert fx.read_store(home)["pad"] == "a"
        Inbox.load(p["store"]).write_pad("a\n____\nc\n____\nd")
        await fx.press(pilot, "alt+u")
        data = fx.read_store(home)
        assert data["pad"] == "a\n____\nc\n____\nd\n____\n" + _ST_NOTE_B
        assert data["pad"].count("Volume lab fails on WSL") == 1 and data["dumped"] == []
        assert _st_pad(app) == data["pad"]
        assert _st_titled(p["C"], "Volume lab fails on WSL") == 0

    # (R) a re-typed note whose earlier dump this window held
    e0 = fx.entry("follow up", "e0", "follow up", p["C"], "pv", at=fx.ago(days=3))
    fx.write_store(home, pad="", dumped=[e0], divider_notice=True)
    app = fx.open_f_app()
    async with app.run_test(size=fx.W118) as pilot:
        await fx.leave_home(pilot)
        await fx.open_capture(pilot, app)
        Inbox.load(p["store"]).write_pad("x")
        await fx.set_pad(pilot, app, "x\n____\nfollow up")
        await pilot.pause(1.3)
        assert fx.read_store(home)["pad"] == "x\n____\nfollow up"

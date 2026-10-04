"""Control bytes are stripped where text enters the app (S2, L1).

Field report (BACKLOG S2, L1; batch 2026-10-02-batch-04): ESC, BEL and C1 bytes in a
board file survived `Board.load` and reached the terminal — a title could carry an
escape sequence, and in team mode a teammate's `board.<user>.json` could inject one
into every member's screen. Only the clipboard was cleaned, by a rule that kept CR.

Law (HLR-402): every string read from the board file, the shared team directory or
the clipboard loses its control bytes — C0 except tab and newline, DEL, C1 — with
CR-LF turned into one newline; nothing else changes, so a file the app saved
round-trips byte for byte. One rule (`models.strip_controls`) at four doors:
`Board.load`, `team_sync._read_json`, the Setup view's `team.json` read, the clipboard.
RED on the pre-fix tree: the rule does not exist and every door keeps the bytes.
"""
from __future__ import annotations

import json

import pytest

from taskboard import models
from taskboard.models import Board, Project, Task

CONTROL = {c for c in map(chr, range(0x100))
           if (ord(c) < 0x20 and c not in "\t\n") or 0x7F <= ord(c) <= 0x9F}
DIRTY = "a\x1b[31mb\x07c\x7fd\x9be\x00f\r\ng"          # ESC, BEL, DEL, C1, NUL, CR-LF
CLEAN = "a[31mbcdef\ng"


def _strings(obj):
    """Every string inside a JSON-like value, keys included."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(k)
            yield from _strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _strings(v)


def _dirty(obj, keys=False):
    """The same JSON value with DIRTY appended to every string VALUE, and to the
    keys of the free-form `settings` map — not to schema keys (`tasks`, `title`),
    which would make the loader see an empty board and the check vacuous."""
    if isinstance(obj, str):
        return obj + DIRTY
    if isinstance(obj, dict):
        return {(k + DIRTY if keys else k): _dirty(v, keys=(k == "settings"))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [_dirty(v) for v in obj]
    return obj


def _no_control(strings) -> list[str]:
    return [s for s in strings if set(s) & CONTROL]


# ---------------------------------------------------------------- the one rule
@pytest.mark.parametrize("code", range(0x100))
def test_TC_407_strip_controls_keeps_exactly_the_printable(code):
    """TC-407 (LLR-402.1), layer 0. Over every code point U+0000..U+00FF (the set
    DERIVED from the range, 256 arms): kept exactly when tab, newline, 0x20..0x7E
    or ≥ 0xA0. RED on a rule that keeps CR or DEL or drops U+00A0."""
    c = chr(code)
    kept = c in "\t\n" or 0x20 <= code <= 0x7E or code >= 0xA0
    assert models.strip_controls(f"x{c}y") == (f"x{c}y" if kept else "xy")


def test_TC_407_strip_controls_shapes():
    """TC-407 (LLR-402.1). CR-LF becomes LF, a lone CR is removed (D-404); emoji
    and NBSP kept; non-strings unchanged; `clean_strings` reaches nested strings
    and keys, a key equal to another after cleaning keeping the later value (D-408)."""
    assert models.strip_controls("a\r\nb\rc\n") == "a\nbc\n"
    assert models.strip_controls("café 🎉 — ñ\t") == "café 🎉 — ñ\t"
    assert models.strip_controls("") == ""
    for v in (1, 2.5, True, None, [1], {"a": 1}):
        assert models.strip_controls(v) == v
    assert models.clean_strings({"k\x1b": ["x\x9b", {"y": "z\x07"}], "n": 3, "b": None}) == \
        {"k": ["x", {"y": "z"}], "n": 3, "b": None}
    assert models.clean_strings({"id": "1", "id\x1b": "2"}) == {"id": "2"}


def test_TC_414_the_clipboard_shares_the_rule():
    """TC-414 (LLR-402.1). The clipboard cleaner is the same rule plus its cap: it
    no longer keeps CR (P2 A-2: the old rule kept it, so a pasted CR-LF reached a
    title). RED on the pre-fix tree: `"a\\r\\nb\\rc"` came back unchanged."""
    from taskboard.models import _MAX_PASTE_CHARS, _clean_clipboard_text
    assert _clean_clipboard_text("a\r\nb\rc") == "a\nbc"
    every = "".join(map(chr, range(0x100)))
    assert _clean_clipboard_text(every) == models.strip_controls(every)
    assert _clean_clipboard_text("x\x1b[<0;5;5M\x00\x7f\x9by") == "x[<0;5;5My"
    assert len(_clean_clipboard_text("z" * (_MAX_PASTE_CHARS + 50))) == _MAX_PASTE_CHARS
    assert _clean_clipboard_text("\x1b\x07") is None


# ------------------------------------------------------------------ the load door
def _board_json() -> dict:
    return {
        "phases": ["Backlog", "Doing", "Done"],
        "projects": [{"id": "p1", "name": "Alpha", "color": "sky", "status": "on_track",
                      "start_date": "2026-10-01", "due_date": "2026-10-09"}],
        "tasks": [{"id": "t1", "title": "Write", "project_id": "p1", "phase": "Doing",
                   "notes": "line one\nline two", "urls": ["https://e.example/a"],
                   "images": ["img/a.png"], "start_date": "2026-10-01",
                   "due_date": "2026-10-03"}],
        "settings": {"clock1": "Tokyo", "note": "kept"},
    }


def test_TC_408_the_load_door_cleans_every_string(tmp_path):
    """TC-408 (LLR-402.2). A board file with control bytes planted in EVERY string
    value and key (the set derived by walking the JSON, its size asserted): the
    loaded board holds 0 control bytes in any project, task, phase or setting.
    RED on the pre-fix tree (P-3)."""
    raw = _dirty(_board_json())
    raw["phases"] = ["Backlog", "Doing", "Done"]              # kept valid: tested apart
    raw["tasks"][0]["phase"] = "Doing"                        # a phase the board holds
    for t in raw["tasks"]:
        t["id"], t["project_id"] = "t1", "p1"                 # ids stay joinable
    raw["projects"][0]["id"] = "p1"
    planted = [s for s in _strings(raw) if DIRTY in s]
    assert len(planted) >= 15, len(planted)
    path = tmp_path / "board.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    b = Board.load(path)
    assert len(b.projects) == 1 and len(b.tasks) == 1 and len(b.settings) == 2
    found = list(_strings([vars(p) for p in b.projects] + [vars(t) for t in b.tasks]
                          + [b.phases, b.settings]))
    assert not _no_control(found), _no_control(found)[:5]
    assert b.tasks[0].notes.startswith("line one\nline two")


def test_TC_408_loading_judges_names_dates_and_phases(tmp_path):
    """TC-408 (LLR-402.2, D-408, D-410). A phase made only of control bytes is
    empty once cleaned, so the phase list is refused and the defaults load (as for
    any empty phase); a hand-edited `""` or non-text project name loads as
    `Untitled`, a non-text date as `None`, a non-boolean flag as `False`."""
    raw = _board_json()
    raw["phases"] = ["Backlog", "\x1b\x07", "Done"]
    raw["projects"] = [{"id": "p1", "name": "", "due_date": 7, "start_date": "2026-10-01",
                        "archived": "no", "pinned": 1},
                       {"id": "p2", "name": 123, "start_date": [1]}]
    path = tmp_path / "board.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    b = Board.load(path)
    assert b.phases == list(models.DEFAULT_PHASES)
    p1, p2 = b.projects
    assert (p1.name, p1.due_date, p1.start_date, p1.archived, p1.pinned) == \
        ("Untitled", None, "2026-10-01", False, False)
    assert (p2.name, p2.start_date) == ("Untitled", None)


def test_TC_410_a_saved_board_round_trips(tmp_path):
    """TC-410 (LLR-402.2, HLR-402). A file the app saved, holding no control byte,
    loads and saves byte-identical; a dirty file's first save is a fixed point."""
    path = tmp_path / "board.json"
    path.write_text(json.dumps(_board_json()), encoding="utf-8")
    Board.load(path).save()
    first = path.read_bytes()
    Board.load(path).save()
    assert path.read_bytes() == first
    dirty = _dirty(_board_json()) | {"phases": ["Backlog", "Doing", "Done"]}
    dirty["tasks"][0].update(id="t1", project_id="p1", phase="Doing")
    dirty["projects"][0]["id"] = "p1"
    path.write_text(json.dumps(dirty), encoding="utf-8")
    Board.load(path).save()
    once = path.read_bytes()
    assert len(json.loads(once)["tasks"]) == 1          # the dirty board loaded whole
    Board.load(path).save()
    assert path.read_bytes() == once
    assert not _no_control(_strings(json.loads(once)))


# ------------------------------------------------------------------ the sync doors
def _team_dir(tmp_path, roster_name="Ana", phases=("Backlog", "Doing", "Done")):
    sd = tmp_path / "shared"
    sd.mkdir()
    (sd / "team.json").write_text(json.dumps({
        "version": 3, "phases": list(phases),
        "roster": [{"id": "ana", "name": roster_name, "hue": "mut"},
                   {"id": "me", "name": "Me", "hue": "mut"}],
        "projects": [{"id": "p1", "name": "Alpha\x1b]0;pwn\x07", "color": "sky"}],
        "template": {"fields": ["title\x9b"]}}), encoding="utf-8")
    (sd / "board.ana.json").write_text(json.dumps({
        "user": "ana", "pushed_at": "2026-10-03T00:00:00Z",
        "tasks": [{"id": "f1", "title": "x\x1b[2Jy", "project_id": "p1",
                   "phase": "Doing\x9b", "notes": "n\x07o"}]}), encoding="utf-8")
    return sd


def test_TC_409_the_sync_doors_clean_what_teammates_wrote(tmp_path):
    """TC-409 (LLR-402.3). A teammate's file and `team.json` holding control bytes
    in titles, notes, project names, phases and roster names (a consumer-contract
    guard: the files are written directly): `foreign_tasks()`, `member_names()` and
    the board after `apply_config_to_board` hold 0 control bytes. RED on the
    pre-fix tree (P-4)."""
    from taskboard.team_sync import TeamState
    sd = _team_dir(tmp_path, roster_name="A\x1bna",
                   phases=("Backlog", "Doing\x07", "Done"))
    ts = TeamState(sd, user_id="me")
    ts.pull()
    b = Board([Project("Alpha", id="p1")], [], tmp_path / "b.json")
    ts.apply_config_to_board(b)
    found = list(_strings([vars(t) for t, _ in ts.foreign_tasks()]
                          + [ts.member_names(), b.phases, [vars(p) for p in b.projects]]))
    assert not _no_control(found), _no_control(found)[:5]


async def test_TC_409_the_setup_view_republishes_a_clean_config(tmp_path):
    """TC-409 (LLR-402.3, P2 A-3). The Setup view read `team.json` with a bare
    `json.loads` and wrote its phases and template back to the shared folder
    uncleaned; it now reads through `_read_json`. Saving Setup republishes a
    `team.json` whose strings hold 0 control bytes. RED on the pre-fix tree."""
    from taskboard.app import TaskboardApp
    sd = _team_dir(tmp_path, phases=("Backlog", "Doing\x07", "Done"))
    b = Board.load(tmp_path / "board.json")
    b.settings["team_shared_dir"] = str(sd)
    b.settings["team_user_id"] = "me"
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.press("0")
        await pilot.pause()
        app.action_setup_save()
        await pilot.pause()
    written = json.loads((sd / "team.json").read_text(encoding="utf-8"))
    assert written["version"] == 4
    assert not _no_control(_strings(written)), _no_control(_strings(written))


# ------------------------------------------------------------------ black box
def _painted(app, box="#details-box") -> str:
    strips = app.screen._compositor.render_strips(app.screen.size)
    r = app.screen.query_one(box).region
    return "\n".join(s.text[r.x:r.x + r.width] for s in strips[r.y:r.y + r.height])


async def test_AT_404_a_dirty_board_opens_clean_and_saves_clean(tmp_path):
    """AT-404 (US-402, HLR-402). A board file whose title, notes, project and phase
    hold ESC and C1 sequences, opened by the app: the details view paints no ESC
    or C1 (Rich drops BEL itself, so BEL is checked at the file — P2 Q-5) and the
    title's printable text; `]` moves the task and saves; the saved file's PARSED
    strings hold 0 control bytes (json writes ESC as `\\u001b`, so a raw-byte check
    would be vacuous). RED on the pre-fix tree: ESC and C1 painted, and saved."""
    from taskboard.app import TaskboardApp
    raw = _board_json()
    raw["phases"] = ["Backlog", "Doing", "Review", "Done"]
    raw["projects"][0]["name"] = "Al\x1b[1mpha\x9b"
    raw["tasks"][0].update(title="Wri\x1b[31mte\x07 the\x9bspec", phase="Doing",
                           notes="be\x1b]0;x\x07fore")
    path = tmp_path / "board.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        app.selected_task_id = "t1"
        await pilot.press("enter")
        for _ in range(3):
            await pilot.pause()
        painted = _painted(app)
        assert not ({"\x1b", "\x9b"} & set(painted)), "a control byte reached the paint"
        assert "Wri[31mte thespec" in painted, painted
        await pilot.press("escape")
        await pilot.pause()
        app.selected_task_id = "t1"
        await pilot.press("]")
        await pilot.pause()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["tasks"][0]["phase"] == "Review", "the key did not save"
    assert not _no_control(_strings(saved)), _no_control(_strings(saved))


async def test_AT_405_what_the_app_pushes_reaches_a_teammate_clean(tmp_path):
    """AT-405 (US-402, HLR-402, C-12). The chain through the shipped handlers: app A
    opens a dirty board in team mode and its startup sync PUSHES `board.me.json`;
    the file A wrote is re-read — its parsed strings hold 0 control bytes (RED
    under a reverted load door alone, P2 Q2-4) — and fed UNCHANGED to a second
    `TeamState` and to a second app (user `ana`), whose painted board holds no
    control byte and shows the title. RED on the pre-fix tree."""
    from taskboard.app import TaskboardApp
    from taskboard.team_sync import TeamState
    sd = _team_dir(tmp_path)
    (sd / "board.ana.json").unlink()
    raw = _board_json()
    raw["tasks"][0].update(title="Ship\x1b[5m it\x9b now", notes="n\x07")
    raw["settings"] = {"team_shared_dir": str(sd), "team_user_id": "me"}
    a_dir = tmp_path / "a"
    a_dir.mkdir()
    (a_dir / "board.json").write_text(json.dumps(raw), encoding="utf-8")
    app_a = TaskboardApp(board_path=str(a_dir / "board.json"), team_sync_interval=1e9)
    async with app_a.run_test(size=(120, 36)) as pilot:
        await pilot.pause()
    pushed = sd / "board.me.json"
    assert pushed.exists(), "app A's startup sync pushed nothing"
    written = json.loads(pushed.read_text(encoding="utf-8"))
    assert written["tasks"], "app A pushed no team task"
    assert not _no_control(_strings(written)), _no_control(_strings(written))
    ts = TeamState(sd, user_id="ana")
    ts.pull()
    titles = [t.title for t, _ in ts.foreign_tasks()]
    assert titles == ["Ship[5m it now"], titles
    b_dir = tmp_path / "b"
    b_dir.mkdir()
    b = Board.load(b_dir / "board.json")
    b.settings["team_shared_dir"] = str(sd)
    b.settings["team_user_id"] = "ana"
    b.save()
    app_b = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app_b.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        await pilot.press("9")                      # the people lanes: teammates' work
        for _ in range(3):
            await pilot.pause()
        strips = app_b.screen._compositor.render_strips(app_b.screen.size)
        screen = "\n".join(s.text for s in strips)
    assert not ({"\x1b", "\x9b", "\x07"} & set(screen))
    assert "Ship[5m" in screen, "the teammate's title is not on the people view"


def _nested(depth: int):
    deep = "end"
    for _ in range(depth):
        deep = [deep]
    return deep


async def test_TC_419_a_deeply_nested_team_file_is_refused_visibly(tmp_path):
    """TC-419 (LLR-402.3, P3 security S4-1). The cleaning at the sync door
    recursed once per nesting level outside the read's error handling, so a
    `team.json` ~1000 levels deep (about 2 KB anyone with the shared folder can
    write) raised `RecursionError` at startup and every teammate's app failed to
    boot. The door now refuses such a file like any unreadable one: the app boots,
    team sync stays off, and a toast says `team.json` could not be read; a deep
    teammate file is skipped; a deep board file is quarantined. RED on the frozen
    tree: the boot raises."""
    from taskboard.app import TaskboardApp
    from taskboard.team_sync import TeamState, _read_json
    sd = tmp_path / "shared"
    sd.mkdir()
    (sd / "team.json").write_text(json.dumps({
        "version": 2, "phases": ["Todo", "Done"], "roster": [{"id": "a", "name": "A"}],
        "projects": [], "deep": _nested(1000)}), encoding="utf-8")
    (sd / "board.ana.json").write_text(json.dumps({"user": "ana", "tasks": [],
                                                   "deep": _nested(1000)}), encoding="utf-8")
    assert _read_json(sd / "team.json") is None
    ts = TeamState(sd, user_id="a")
    assert ts.pull() and "ana" not in ts.others
    path = tmp_path / "board.json"
    path.write_text(json.dumps({"phases": ["Todo", "Done"], "projects": [], "tasks": [],
                                "settings": {"team_shared_dir": str(sd),
                                             "team_user_id": "a"}}), encoding="utf-8")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(120, 36), notifications=True) as pilot:
        for _ in range(3):
            await pilot.pause()
        toasts = [str(t.render()) for t in app.screen.query("Toast")]
        assert app.is_running
    assert any("team.json" in t and "could not be read" in t for t in toasts), toasts
    incomplete = tmp_path / "incomplete"
    incomplete.mkdir()
    (incomplete / "team.json").write_text(json.dumps({"version": 1, "phases": ["Todo"],
                                                      "roster": [], "projects": []}),
                                          encoding="utf-8")
    path2 = tmp_path / "board2.json"
    path2.write_text(json.dumps({"phases": ["Todo", "Done"], "projects": [], "tasks": [],
                                 "settings": {"team_shared_dir": str(incomplete),
                                              "team_user_id": "a"}}), encoding="utf-8")
    app2 = TaskboardApp(board_path=str(path2), team_sync_interval=1e9)
    async with app2.run_test(size=(120, 36), notifications=True) as pilot:
        for _ in range(3):
            await pilot.pause()
        toasts2 = [str(t.render()) for t in app2.screen.query("Toast")]
    assert not any("could not be read" in t for t in toasts2), toasts2   # G1: read, not unreadable
    deep_board = tmp_path / "deep.json"
    deep_board.write_text(json.dumps({"phases": ["A"], "projects": [], "tasks": [],
                                      "settings": {"x": _nested(1000)}}), encoding="utf-8")
    b = Board.load(deep_board)
    assert b.load_report.get("file_unreadable") is True


def test_TC_410_the_rule_strips_nothing_else(tmp_path):
    """TC-410 (LLR-402.2, P3 code review F2). The round trip cannot see a rule
    that strips TOO MUCH — the first save already ran the rule — so a board built
    in the app holding every class the rule must keep (tab, newline, ASCII
    punctuation and brackets, a backslash run, accents, NBSP, emoji, CJK) is saved,
    loaded and its text compared with what was put in, field by field. RED under a
    rule that also drops newline, tab or every character ≥ U+00A0."""
    keep = "a\tb\nc [b]x[/b] \\\\\\ ñé — 🎉 漢字 ~!@#$%^&*()_+{}|:\"<>?"
    path = tmp_path / "board.json"
    b = Board([Project(keep, "sky", id="p1")],
              [Task(keep, "p1", "Doing", notes=keep, urls=[keep], id="t1")],
              path, settings={"note": keep}, phases=["Backlog", "Doing", "Done"])
    b.save()
    first = path.read_bytes()
    back = Board.load(path)
    assert (back.projects[0].name, back.tasks[0].title, back.tasks[0].notes,
            back.tasks[0].urls, back.settings["note"]) == (keep, keep, keep, [keep], keep)
    back.save()
    assert path.read_bytes() == first

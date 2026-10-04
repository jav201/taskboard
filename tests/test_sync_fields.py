"""A shared config cannot act or crash (S-1, S-3; batch 2026-10-02-batch-04).

Field report (P2 security S-1, HIGH; S-3, S2-1, S2-2): `apply_config_to_board` copied a
teammate's `team.json` project fields onto local projects with a bare `setattr`,
skipping every check loading a board file makes — a status `[@click=app.pwn]X`
reached the project picker as markup and a click RAN the action; an unknown or
unhashable colour, an int name, a duplicate id or a roster name `123` crashed views.

Law (HLR-404, LLR-404.1, LLR-404.2): a synced project field is applied only when
present, only through `Project.from_dict`'s value for it, and left unchanged where
the INPUT is refused (a name that is not non-empty text, a date that is neither
text nor null); a synced `null` date clears; `archived` only as a boolean; the first
entry of each id wins; the roster gets the same treatment in `clean_roster`.
RED on the pre-fix tree: the hostile arms are applied raw.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from taskboard.models import (PROJECT_COLORS, PROJECT_STATUSES, Board, Project,
                              project_color_on_load)
from taskboard.team_sync import TeamState


def _sync(tmp_path, entries, *, roster=None) -> Board:
    sd = tmp_path / "shared"
    sd.mkdir(exist_ok=True)
    (sd / "team.json").write_text(json.dumps({
        "version": 2, "phases": ["Todo", "Doing", "Done"],
        "roster": roster or [{"id": "a", "name": "A"}], "projects": entries}),
        encoding="utf-8")
    b = Board([], [], tmp_path / "b.json")
    b.projects.append(Project("Alpha", "sky", "paused", start_date="2026-10-01",
                              due_date="2026-10-09", id="p1"))
    ts = TeamState.from_settings(str(sd), "a")
    ts.load_config()
    ts.apply_config_to_board(b)
    return b


HOSTILE = object()                     # a marker: the key's value is refused input

# (key, synced value, expected) — the matrix is DERIVED from the model's constant
# tuples plus the hostile values the reviews named; expected HOSTILE = unchanged.
ARMS = (
    [("status", s, s) for s in PROJECT_STATUSES]
    + [("status", "[@click=app.pwn]X", "on_track"), ("status", "at_risk", "on_track"),
       ("status", 3, "on_track")]
    + [("color", c, c) for c in PROJECT_COLORS]
    + [("color", "evil", "violet"), ("color", [], "violet"), ("color", {}, "violet"),
       ("color", "#123456", "violet")]
    + [("name", "Ops", "Ops"), ("name", "Untitled", "Untitled"), ("name", 123, HOSTILE),
       ("name", None, HOSTILE), ("name", "", HOSTILE)]
    + [("start_date", "2026-09-01", "2026-09-01"), ("start_date", None, None),
       ("start_date", 7, HOSTILE)]
    + [("due_date", "2026-12-24", "2026-12-24"), ("due_date", None, None),
       ("due_date", 7, HOSTILE)]
    + [("archived", True, True), ("archived", False, False), ("archived", 1, HOSTILE),
       ("archived", "true", HOSTILE), ("archived", "false", HOSTILE), ("archived", None, HOSTILE)]
)
BEFORE = {"name": "Alpha", "color": "sky", "status": "paused", "start_date": "2026-10-01",
          "due_date": "2026-10-09", "archived": False}


@pytest.mark.parametrize("key, value, expected", ARMS,
                         ids=[f"{k}={v!r}" for k, v, _ in ARMS])
def test_TC_413_a_synced_field_passes_the_loading_rule(tmp_path, key, value, expected):
    """TC-413 (LLR-404.1). An existing project's field is set from the synced entry
    only through the loading rule; refused input leaves it as it was. RED on the
    pre-fix tree for every hostile arm (P-12) except the `archived` ones, which the
    pre-fix tree already guarded (a boolean only) — those four are preservation
    pins (code review F5), as are the valid-value arms."""
    b = _sync(tmp_path, [{"id": "p1", key: value}])
    got = getattr(b.projects[0], key)
    assert got == (BEFORE[key] if expected is HOSTILE else expected), (key, value, got)
    assert all(getattr(b.projects[0], k) == v for k, v in BEFORE.items() if k != key)


def test_TC_413_absent_keys_are_not_applied(tmp_path):
    """TC-413 (LLR-404.1, A2-1, S2-6). An entry holding only `id` changes nothing:
    the pre-fix gate on present keys is kept — the loading rule would otherwise
    reset the colour to `violet` and the status to `on_track`."""
    b = _sync(tmp_path, [{"id": "p1"}])
    assert {k: getattr(b.projects[0], k) for k in BEFORE} == BEFORE


def test_TC_413_new_projects_and_duplicate_ids(tmp_path):
    """TC-413 (LLR-404.1, S3-1, A3-2). A new synced project is `Project.from_dict`
    of its entry; of two entries with one id — new or existing — only the first is
    applied or appended. RED on the pre-fix tree: both duplicates applied."""
    entry = {"id": "n1", "name": 123, "color": [], "status": "[@click=app.pwn]X",
             "due_date": 7, "archived": "yes", "pinned": 1}
    b = _sync(tmp_path, [entry, {"id": "n1", "name": "Second"},
                         {"id": "p1", "name": "First"}, {"id": "p1", "name": "Later"}])
    news = [p for p in b.projects if p.id == "n1"]
    assert len(news) == 1
    want = Project.from_dict(entry)
    assert [(news[0].name, news[0].color, news[0].status, news[0].due_date,
             news[0].archived, news[0].pinned)] == \
        [(want.name, want.color, want.status, want.due_date, want.archived, want.pinned)] == \
        [("Untitled", "violet", "on_track", None, False, False)]
    assert b.projects[0].name == "First"


@pytest.mark.parametrize("color", [[], {}, ("x",), 3, None, "evil"])
def test_TC_413_any_colour_value_loads(color):
    """TC-413 (LLR-404.1, S2-2). `project_color_on_load` takes a value of ANY type:
    the fix routes synced colours through it, and on the pre-fix tree an
    unhashable one raised `TypeError` — the fix's own new crash otherwise."""
    assert project_color_on_load(color) == "violet"


def test_TC_416_the_roster_passes_a_loading_rule(tmp_path):
    """TC-416 (LLR-404.2). A roster with a duplicate id, a non-text name, an empty
    name, an unhashable and an unknown hue, and every palette key: one entry per
    id (the first), names text or the id, hues palette keys or `mut`; the people,
    standup and setup views render. RED on the pre-fix tree (P-15)."""
    from taskboard.team_sync import clean_roster
    from taskboard.views import HEX, render_view
    keys = sorted(HEX)
    roster = ([{"id": "a", "name": 123, "hue": []}, {"id": "a", "name": "Dup", "hue": "sky"},
               {"id": "b", "name": "", "hue": "evil"}, {"id": "c", "name": "Bo", "hue": "mut"}]
              + [{"id": f"k{i}", "name": f"K{i}", "hue": k} for i, k in enumerate(keys)])
    cleaned = clean_roster(roster)
    assert [r["id"] for r in cleaned][:3] == ["a", "b", "c"]
    assert [r["name"] for r in cleaned][:3] == ["a", "b", "Bo"]
    assert [r["hue"] for r in cleaned][:3] == ["mut", "mut", "mut"]
    assert [r["hue"] for r in cleaned][3:] == keys
    sd = tmp_path / "shared"
    sd.mkdir()
    (sd / "team.json").write_text(json.dumps({"version": 2, "phases": ["Todo", "Done"],
                                              "roster": roster, "projects": []}),
                                  encoding="utf-8")
    ts = TeamState.from_settings(str(sd), "a")
    ts.load_config()
    assert [r["id"] for r in ts.roster()] == [r["id"] for r in cleaned]
    assert ts.member_names()["a"] == "a" and ts.member_hues()["a"] == "mut"
    b = Board([], [], tmp_path / "b.json")
    for mode in ("people", "standup", "setup"):
        render_view(mode, b, False, None, width=100, height=30, team_state=ts,
                    setup_state={"roster": ts.roster(), "projects": [], "phases": ["Todo"]})


@pytest.mark.parametrize("pid", ["\x07", "", "\x1b\x9b"])
def test_TC_413_an_empty_synced_id_never_grows_the_board(tmp_path, pid):
    """TC-413 (LLR-404.1, P3 code review F1). A synced project id that is empty —
    literally, or once its control bytes are stripped at the sync door — is
    refused: `Project.from_dict` would give it a fresh random id, so no later pass
    could match it and every sync tick appended a new project to every teammate's
    board. Three passes keep the board at its one project. RED on the frozen
    tree: 3 projects after 3 passes (the reviewer's probe)."""
    sd = tmp_path / "shared"
    sd.mkdir()
    (sd / "team.json").write_text(json.dumps({
        "version": 2, "phases": ["Todo", "Done"], "roster": [{"id": "a", "name": "A"}],
        "projects": [{"id": pid, "name": "Ghost"}]}), encoding="utf-8")
    b = Board([Project("Alpha", "sky", id="p1")], [], tmp_path / "b.json")
    ts = TeamState.from_settings(str(sd), "a")
    for _ in range(3):
        ts.load_config()
        ts.apply_config_to_board(b)
    assert [p.id for p in b.projects] == ["p1"], [(p.id, p.name) for p in b.projects]


async def test_TC_413_sync_ticks_and_the_startup_save_keep_the_board_size(tmp_path):
    """TC-413 (LLR-404.1, F1) through the app: in team mode with a `team.json`
    holding a control-byte-only project id, the startup sync, its save and three
    sync ticks leave the board — in memory and in the saved file — at its size."""
    from taskboard.app import TaskboardApp
    sd = tmp_path / "shared"
    sd.mkdir()
    (sd / "team.json").write_text(json.dumps({
        "version": 2, "phases": ["Todo", "Doing", "Done"],
        "roster": [{"id": "a", "name": "A"}],
        "projects": [{"id": "\x07", "name": "Ghost"}, {"id": "p1", "name": "Alpha"}]}),
        encoding="utf-8")
    path = tmp_path / "board.json"
    path.write_text(json.dumps({
        "phases": ["Todo", "Doing", "Done"],
        "projects": [{"id": "p1", "name": "Alpha", "color": "sky"}], "tasks": [],
        "settings": {"team_shared_dir": str(sd), "team_user_id": "a"}}), encoding="utf-8")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.pause()
        app.board.save()
        sizes = [len(app.board.projects)]
        for _ in range(3):
            app._team_sync_tick()
            await pilot.pause()
            sizes.append(len(app.board.projects))
        app.board.save()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert sizes == [1, 1, 1, 1], sizes
    assert [p["id"] for p in saved["projects"]] == ["p1"]


async def test_TC_418_setup_republishes_the_first_entry_validated(tmp_path):
    """TC-418 (LLR-404.1, P3 code review F3). The Setup view staged a team
    project from the LAST entry of its id and copied its raw name, colour and
    status, so saving Setup republished `[]` and a click-action status to every
    teammate. It stages the board's validated values of the FIRST entry — the
    rule `apply_config_to_board` follows — and the `team.json` it writes holds
    them. RED on the frozen tree: `Later`, `[]`, the action tag republished; RED
    under either guard alone removed (the first-entry rule, the validated values)."""
    from taskboard.app import TaskboardApp
    sd = tmp_path / "shared"
    sd.mkdir()
    (sd / "team.json").write_text(json.dumps({
        "version": 2, "phases": ["Todo", "Doing", "Done"],
        "roster": [{"id": "a", "name": "A"}],
        "projects": [{"id": "p1", "name": "First", "color": "evil", "status": "paused",
                      "template": "t-first"},
                     {"id": "p1", "name": "Later", "color": [],
                      "status": "[@click=app.quit]X", "template": "t-later"}]}),
        encoding="utf-8")
    path = tmp_path / "board.json"
    path.write_text(json.dumps({
        "phases": ["Todo", "Doing", "Done"],
        "projects": [{"id": "p1", "name": "Alpha", "color": "lime"}], "tasks": [],
        "settings": {"team_shared_dir": str(sd), "team_user_id": "a"}}), encoding="utf-8")
    app = TaskboardApp(board_path=str(path), team_sync_interval=1e9)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.pause()
        await pilot.press("0")
        await pilot.pause()
        app.action_setup_save()
        await pilot.pause()
    written = json.loads((sd / "team.json").read_text(encoding="utf-8"))
    p1 = [p for p in written["projects"] if p["id"] == "p1"]
    assert len(p1) == 1, written["projects"]
    # each guard observable on its own (the battery found the two masking each other):
    # the raw first entry's colour `evil` vs the board's validated `violet`; the
    # last entry's template `t-later` vs the first's `t-first`
    assert (p1[0]["name"], p1[0]["color"], p1[0]["status"], p1[0]["template"]) == \
        ("First", "violet", "paused", "t-first"), p1

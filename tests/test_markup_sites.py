"""Every dialog, picker and toast paints user and synced text exactly (Batch S).

Field report (BACKLOG "Security S1, the remaining sites", S-5; P2 S-4, batch
2026-10-02-batch-04): text the app did not write — a task title, notes, a URL,
an image reference, a project or phase name, a teammate's roster name, an id
typed in Setup, a file path, an exception message — is handed to a markup
parser on its way to the screen. Textual's parser reads `[LINK=…]` (which
Rich's `escape` leaves alone, P-1) and kills the screen with `MarkupError`;
Rich's parser behind `modals._rich` turns `:smile:` into an emoji and eats the
backslashes of `x\\\\\\` (P-11); a toast with markup on does both. A team
mode user gets the same from a teammate's `team.json`.

Law (HLR-401, LLR-401.2, LLR-401.3): for each reachable site of the contract's
§5.1 and each payload of §1.3, the screen stays up and the text is painted
exactly — read off the painted screen (box-cropped, so the board behind a
modal cannot answer for it) or off the painted `Toast` (`str(toast.render())`,
P-7) — and the app-styled sites keep the style they paint today (TC-415).

Method (§5): one node per AT; inside a node every site x payload runs in its
OWN `App.run_test(notifications=True)`, failures are collected and asserted
together, so the base run lists every RED site at once.
"""
from __future__ import annotations

import contextlib
import io
import json
from datetime import date
from pathlib import Path
from unittest.mock import patch

from taskboard import history
from taskboard.app import RENUMBER_NOTICE_KEY, TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.team_sync import TeamState

SIZE = (140, 40)

P_LINK = "[LINK=http://e]x"          # a Textual tag Rich's escape leaves alone (P-1)
P_BACK = "x\\\\\\"                   # x then three backslashes (S-4)
P_EMOJI = ":smile: [b]y[/b]"         # a Rich emoji code and a Rich tag (S-4)
PAYLOADS = (P_LINK, P_BACK, P_EMOJI)
DIRS = ("a[B]x", "[B]x")             # the path payloads (§1.3)


# ---------------------------------------------------------------- fixtures --
def _board(d: Path, projects=(), tasks=(), phases=None, settings=None) -> Path:
    """A board file on disk under `d` (created), the renumber notice already
    seen so its toast does not crowd the ones under test."""
    d.mkdir(parents=True, exist_ok=True)
    s = {RENUMBER_NOTICE_KEY: True}
    s.update(settings or {})
    b = Board(list(projects), list(tasks), d / "board.json", s, phases)
    b.save()
    return b.path


def _one(d: Path, *, title="Plain title", project="Plain", phase="Doing",
         phases=None, others=(), **fields) -> Path:
    """One project, one task (selected by the arms), optional extra tasks."""
    p = Project(project, "sky")
    phases = phases or ["Backlog", "Doing", "Done"]
    tasks = [Task(title, p.id, phase, **fields)]
    tasks += [Task(t, p.id, ph, **kw) for t, ph, kw in others]
    return _board(d, [p], tasks, phases)


def _team(d: Path, roster, projects=(), phases=("Todo", "Done")) -> Path:
    shared = d / "shared"
    shared.mkdir(parents=True, exist_ok=True)
    (shared / "team.json").write_text(json.dumps(
        {"version": 3, "phases": list(phases), "roster": list(roster),
         "projects": list(projects)}), encoding="utf-8")
    return shared


def _app(path: Path) -> TaskboardApp:
    return TaskboardApp(board_path=str(path), team_sync_interval=1e9)


def _png(path: Path) -> Path:
    from PIL import Image
    Image.new("RGB", (4, 4), (200, 30, 30)).save(path, "PNG")
    return path


# ----------------------------------------------------------------- reading --
def _strip_rows(app, sel=None, content=True):
    """Painted strips, cropped by CELLS to a widget's (content) region."""
    strips = app.screen._compositor.render_strips(app.screen.size)
    if sel is None:
        return list(strips)
    w = app.screen.query_one(sel) if isinstance(sel, str) else sel
    r = w.content_region if content else w.region
    return [s.crop(r.x, r.x + r.width) for s in strips[r.y:r.y + r.height]]


def _rows(app, sel=None, content=True) -> list[str]:
    return [s.text for s in _strip_rows(app, sel, content)]


def _option_row(rows: list[str], expected: str) -> bool:
    """One option-list row (its border cells dropped) equal to `expected`."""
    return any(r.strip(" ▊▎│") == expected for r in rows)


def _norm(s: str) -> str:
    return " ".join(s.split())


def _shows(rows: list[str], expected: str) -> bool:
    """`expected` painted in one row, or wrapped at a space over several."""
    return (any(expected in r for r in rows)
            or _norm(expected) in _norm(" ".join(rows)))


def _toasts(app) -> list[str]:
    return [str(t.render()) for t in app.screen.query("Toast")]


async def _settle(pilot, n=3):
    for _ in range(n):
        await pilot.pause()


async def _press_select(app, pilot, *keys):
    await pilot.pause()
    app.selected_task_id = app.board.tasks[0].id
    await pilot.press(*keys)
    await _settle(pilot)


def _miss(where: str, expected: str, rows: list[str]) -> str:
    shown = [r.strip() for r in rows if r.strip()][:12]
    return f"{expected!r} not painted in {where}; painted {shown!r}"


async def _collect(failures: list[str], name: str, fn) -> None:
    """Run one site x payload arm; record why it failed. Textual prints a
    crash traceback (with local paths) on exit: it goes to a sink, the
    exception type and message are what the arm records."""
    sink = io.StringIO()
    try:
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            why = await fn()
    except Exception as exc:          # MarkupError and friends: the screen died
        why = f"{type(exc).__name__}: {str(exc).splitlines()[0][:110] if str(exc) else ''}"
    if why:
        failures.append(f"{name}: {why}")


def _verdict(failures: list[str], total: int) -> None:
    assert not failures, (f"{len(failures)} of {total} site x payload arms failed:\n  "
                          + "\n  ".join(failures))


# ---- shared arm bodies --------------------------------------------------------
async def _box_arm(path: Path, keys, box: str, expected: str, screen=None, end=False,
                   row=False):
    app = _app(path)
    async with app.run_test(size=SIZE, notifications=True) as pilot:
        await _press_select(app, pilot, *keys)
        if screen is not None and type(app.screen).__name__ != screen:
            return f"{screen} did not open (screen {type(app.screen).__name__})"
        if end:                      # an inline image is tall: read the box's end
            app.screen.query_one(box).scroll_end(animate=False)
            await _settle(pilot)
        rows = _rows(app, box)
        ok = _option_row(rows, expected) if row else _shows(rows, expected)
        return None if ok else _miss(box, expected, rows)


async def _toast_arm(path: Path, keys, title: str | None, message: str, exact=False):
    app = _app(path)
    async with app.run_test(size=SIZE, notifications=True) as pilot:
        await _press_select(app, pilot, *keys)
        return _toast_check(app, title, message, exact)


def _toast_check(app, title, message, exact) -> str | None:
    toasts = _toasts(app)
    for t in toasts:
        head, _, body = t.partition("\n")
        if title is None:
            head, body = None, t
        if head != title:
            continue
        if (body == message) if exact else (message in body):
            return None
    return f"no {title!r} toast {'equal to' if exact else 'holding'} {message!r}; toasts {toasts!r}"


async def _select_checks(app, pilot, sel_id: str, expected: str) -> str | None:
    """A task-editor Select: its current value (20 / 12 cells wide, so the
    painted cells are a prefix of the value; the label's rendered content is
    the whole value), then the opened overlay list (it wraps, so whitespace is
    dropped on both sides before comparing)."""
    from textual.widgets import Select
    from textual.widgets._select import SelectCurrent, SelectOverlay
    s = app.screen.query_one(sel_id, Select)
    label = s.query_one(SelectCurrent).query_one("#label")
    rendered = str(label.render())
    r = label.region.intersection(s.content_region)     # the cells the Select shows
    strips = app.screen._compositor.render_strips(app.screen.size)
    painted = " ".join(st.crop(r.x, r.x + r.width).text.strip()
                       for st in strips[r.y:r.y + r.height]).strip()
    if rendered != expected:
        return f"{sel_id} current value renders {rendered!r}, not {expected!r}"
    if not painted or not expected.startswith(painted.rstrip("…").rstrip()):
        return f"{sel_id} current value painted {painted!r}, not a prefix of {expected!r}"
    s.focus()
    await pilot.pause()
    await pilot.press("enter")
    await _settle(pilot)
    ov = s.query_one(SelectOverlay)
    flat = "".join("".join(r.split()) for r in _rows(app, ov))
    if "".join(expected.split()) not in flat:
        return f"{sel_id} opened list paints {flat!r}, without {expected!r}"
    return None


# ================================================================== AT-401 ==
async def test_AT_401_board_text_is_painted_exactly(tmp_path, monkeypatch):
    """AT-401 (HLR-401, US-401) — board-file text in every dialog and picker.

    Field report: a title, project or phase name, note, URL or image reference
    from the board file is handed to Textual's markup parser (a str prompt or
    label, `escape` first — which leaves `[LINK=…]` alone) or to Rich's
    (`modals._rich`, `notes_preview`, which read `:smile:` and eat
    backslashes). Law: every §5.1 site marked AT-401 x every payload, each in
    its own run: the screen stays up and paints the payload exactly — box-
    cropped (confirm, picker, blocker, phase editor, prompt, standup, details,
    viewer boxes), the task editor's Select read as its current value and its
    opened list, the archive / pin toasts read off the painted `Toast`, the
    editor preview fed by KEYS typed into the notes. The file-backed image
    branches run with the bracket name only (`a[B]x.png`, `bad[B].png`: the
    other payloads are not legal Windows file names); the image-URL branch
    runs with the URL-legal payloads `x\\\\\\` and `:smile:` (`valid_url`
    refuses `[`, `]` and space, so `[LINK=…` and `[b]y[/b]` land in
    `missing:`, which is armed for every payload). The details URL list shows
    every stored URL string, so its arm stores the payload itself as the URL
    (a board file or a synced task can hold any string there).
    RED on base: `MarkupError` at the Textual-parsed sites, the payload
    altered at the `_rich` sites (P-1, P-7, P-11). Not every arm is RED on
    base — Textual's parser reads no emoji code and keeps a backslash that
    precedes no `[`, and Rich's ignores an uppercase tag — those arms are
    pins that the conversion keeps the text; the base transcript lists the
    RED ones. Four `[LINK=…` arms are RED on base UPSTREAM of the site they
    name: the project archive / delete confirms, the delete-phase confirm and
    the rename prompt never open, because the picker or phase list they open
    from dies first."""
    failures: list[str] = []
    arms = []
    n = iter(range(10_000))

    def d():
        return tmp_path / f"a{next(n)}"

    today = date.today().isoformat()
    for p in PAYLOADS:
        arms += [
            (f"delete-task confirm d [{p!r}]", lambda p=p: _box_arm(
                _one(d(), title=p), ["d"], "#confirm-box", f"Delete '{p}'?", "ConfirmModal")),
            (f"archive toast x [{p!r}]", lambda p=p: _toast_arm(
                _one(d(), title=p), ["x"], "Archive", f'"{p}" archived')),
            (f"pin toast T [{p!r}]", lambda p=p: _toast_arm(
                _one(d(), project=p), ["T"], "Pin project", f'"{p}" pinned')),
            (f"project picker line P [{p!r}]", lambda p=p: _box_arm(
                _one(d(), project=p), ["P"], "#picker-box", f"{p}  ·  on_track",
                "ProjectPicker")),
            (f"project archive confirm P j x [{p!r}]", lambda p=p: _box_arm(
                _one(d(), project=p), ["P", "j", "x"], "#confirm-box", f"Archive '{p}'?",
                "ConfirmModal")),
            (f"project delete confirm P j d [{p!r}]", lambda p=p: _box_arm(
                _one(d(), project=p), ["P", "j", "d"], "#confirm-box", f"Delete '{p}'?",
                "ConfirmModal")),
            (f"link picker L [{p!r}]", lambda p=p: _box_arm(
                _one(d(), others=[(p, "Doing", {})]), ["L"], "#link-box", p,
                "LinkPicker")),
            (f"task editor project select e [{p!r}]", lambda p=p: _editor_select_arm(
                _one(d(), project=p), "#f-project", p)),
            (f"task editor phase select e [{p!r}]", lambda p=p: _editor_select_arm(
                _one(d(), phase=p, phases=["Backlog", p, "Done"]), "#f-phase", p)),
            (f"phase editor list f [{p!r}]", lambda p=p: _box_arm(
                _one(d(), phase=p, phases=[p, "Doing", "Done"]), ["f"], "#picker-box",
                f"{p}  ·  1 task", "PhaseEditor")),
            (f"delete-phase confirm f d [{p!r}]", lambda p=p: _box_arm(
                _one(d(), phase=p, phases=[p, "Doing", "Done"]), ["f", "d"], "#confirm-box",
                f"Delete '{p}'?", "ConfirmModal")),
            (f"rename-phase prompt f e [{p!r}]", lambda p=p: _box_arm(
                _one(d(), phase=p, phases=[p, "Doing", "Done"]), ["f", "e"], "#modal-box",
                p, "TextPrompt")),
            (f"standup project S [{p!r}]", lambda p=p: _box_arm(
                _one(d(), project=p, phase_changed=today), ["S"], "#modal-box", f"▐ {p}",
                "StandupModal")),
            (f"standup title S [{p!r}]", lambda p=p: _box_arm(
                _one(d(), title=p, phase_changed=today), ["S"], "#modal-box",
                f"→ {p} Doing", "StandupModal")),
            (f"standup phase S [{p!r}]", lambda p=p: _box_arm(
                _one(d(), phase=p, phases=["Backlog", p, "Done"], phase_changed=today),
                ["S"], "#modal-box", f"→ Plain title {p}", "StandupModal")),
            (f"details title enter [{p!r}]", lambda p=p: _box_arm(
                _one(d(), title=p), ["enter"], "#details-box", f"{p}  —  o open raw",
                "TaskDetails")),
            (f"details notes enter [{p!r}]", lambda p=p: _box_arm(
                _one(d(), notes=p), ["enter"], "#details-box", p, "TaskDetails")),
            (f"details URL enter [{p!r}]", lambda p=p: _box_arm(
                _one(d(), urls=[p]), ["enter"], "#details-box", f"link · {p}",
                "TaskDetails")),
            (f"image viewer title i [{p!r}]", lambda p=p: _box_arm(
                _one(d(), title=p), ["i"], "#viewer-box", f"{p}  —  o open raw",
                "ImageViewer")),
            (f"image block missing: enter [{p!r}]", lambda p=p: _box_arm(
                _one(d(), images=[p]), ["enter"], "#details-box", f"missing: {p}",
                "TaskDetails")),
            (f"editor preview e + typed notes [{p!r}]", lambda p=p: _preview_arm(_one(d()), p)),
        ]
    for q in (P_BACK, ":smile:"):         # the URL-legal payloads (see docstring)
        arms.append((f"image block link · enter [{q!r}]", lambda q=q: _box_arm(
            _one(d(), images=[f"https://e.example/{q}"]), ["enter"], "#details-box",
            f"link · https://e.example/{q}", "TaskDetails")))

    async def file_arm(name: str, corrupt: bool):
        here = d()
        here.mkdir(parents=True)
        if corrupt:
            (here / name).write_bytes(b"not a png at all")
        else:
            _png(here / name)
        monkeypatch.chdir(here)               # the reference is the bare name
        expected = f"could not render: {name}" if corrupt else name
        return await _box_arm(_one(here, images=[name]), ["enter"], "#details-box",
                              expected, "TaskDetails", end=True)

    arms.append(("image block existing image a[B]x.png enter",
                 lambda: file_arm("a[B]x.png", False)))
    arms.append(("image block could not render: bad[B].png enter",
                 lambda: file_arm("bad[B].png", True)))

    for name, fn in arms:
        await _collect(failures, name, fn)
    _verdict(failures, len(arms))


async def _editor_select_arm(path: Path, sel_id: str, expected: str):
    app = _app(path)
    async with app.run_test(size=SIZE, notifications=True) as pilot:
        await _press_select(app, pilot, "e")
        if type(app.screen).__name__ != "TaskModal":
            return f"the task editor did not open (screen {type(app.screen).__name__})"
        return await _select_checks(app, pilot, sel_id, expected)


async def _preview_arm(path: Path, typed: str):
    from textual.widgets import TextArea
    app = _app(path)
    async with app.run_test(size=SIZE, notifications=True) as pilot:
        await _press_select(app, pilot, "e")
        notes = app.screen.query_one("#f-notes", TextArea)
        notes.focus()
        await pilot.pause()
        await pilot.press(*typed)
        await _settle(pilot)
        if notes.text != typed:     # the fixture typed what it meant to
            return f"fixture: the notes hold {notes.text!r}, not the typed {typed!r}"
        rows = _rows(app, "#task-preview")
        return None if _shows(rows, typed) else _miss("#task-preview", typed, rows)


# ================================================================== AT-402 ==
async def test_AT_402_synced_text_is_painted_exactly(tmp_path):
    """AT-402 (HLR-401, US-401) — a teammate's text from `team.json`.

    Field report: in team mode a roster name reaches the identity picker that
    opens at mount (`_init_team_mode` → `TeamIdentityPicker`), and a
    synced project name or phase reaches the board through the startup sync
    (`apply_config_to_board`) and from there the task editor's Selects and the
    project picker — another person's file, handed to Textual's parser with
    `escape` first. Law: for each payload, each in its own run: the identity
    picker paints the roster name exactly (one row equal to it); after the
    startup sync (asserted: the board holds the synced name / phase) the
    editor's project and phase Selects paint it (current value and opened
    list) and the project picker line paints it. RED on base: `MarkupError`
    for `[LINK=…]`; the other payloads may paint unchanged through Textual's
    parser (recorded per arm)."""
    failures: list[str] = []
    arms = []
    n = iter(range(10_000))

    def d():
        return tmp_path / f"a{next(n)}"

    def synced(here: Path, *, name=None, phases=("Todo", "Done")) -> Path:
        tp = {"id": "tp", "name": name or "Local", "color": "sky", "status": "on_track"}
        shared = _team(here, [{"id": "a", "name": "Ann"}], [tp], phases)
        proj = Project("Local", "sky", id="tp")
        return _board(here, [proj], [Task("Plain title", "tp", "Todo")], ["Todo", "Done"],
                      {"team_shared_dir": str(shared), "team_user_id": "a"})

    async def identity_arm(p):
        here = d()
        shared = _team(here, [{"id": "a", "name": p}, {"id": "b", "name": "Bo"}])
        path = _board(here, [Project("Local", "sky")], [Task("Plain title")], None,
                      {"team_shared_dir": str(shared)})
        app = _app(path)
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _settle(pilot)
            if type(app.screen).__name__ != "TeamIdentityPicker":
                return f"the identity picker did not open (screen {type(app.screen).__name__})"
            rows = _rows(app, "#identity-box")
            return None if _option_row(rows, p) else _miss("#identity-box", p, rows)

    async def editor_arm(p, sel_id, **kw):
        app = _app(synced(d(), **kw))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await pilot.pause()
            got = app.board.projects[0].name if sel_id == "#f-project" else app.board.phases[0]
            if got != p:
                return f"fixture: the startup sync did not apply the payload (board holds {got!r})"
            await _press_select(app, pilot, "e")
            if type(app.screen).__name__ != "TaskModal":
                return f"the task editor did not open (screen {type(app.screen).__name__})"
            return await _select_checks(app, pilot, sel_id, p)

    async def picker_arm(p):
        app = _app(synced(d(), name=p))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await pilot.pause()
            if app.board.projects[0].name != p:
                return "fixture: the startup sync did not apply the synced name"
            await _press_select(app, pilot, "P")
            rows = _rows(app, "#picker-box")
            want = f"{p}  ·  on_track"
            return None if _shows(rows, want) else _miss("#picker-box", want, rows)

    for p in PAYLOADS:
        arms += [
            (f"team identity picker roster name [{p!r}]", lambda p=p: identity_arm(p)),
            (f"synced project name in editor select [{p!r}]",
             lambda p=p: editor_arm(p, "#f-project", name=p)),
            (f"synced phase in editor select [{p!r}]",
             lambda p=p: editor_arm(p, "#f-phase", phases=(p, "Done"))),
            (f"synced project name in project picker [{p!r}]", lambda p=p: picker_arm(p)),
        ]
    for name, fn in arms:
        await _collect(failures, name, fn)
    _verdict(failures, len(arms))


# ================================================================== AT-403 ==
async def test_AT_403_typed_and_os_text_is_painted_exactly(tmp_path, monkeypatch):
    """AT-403 (HLR-401, US-401) — typed ids and names, file paths, OS errors.

    Field report (S-5): `app.py` and the phase editor notify a typed id or
    name, a file path and an OS error message with markup ON — the Setup id
    is lowercased (`[LINK=…` becomes Textual's `[link=…` tag), the duplicate
    phase name is `escape`d, the report and recovery paths and the
    transition-log error are not escaped at all, and a board directory named
    `a[B]x` or `[B]x` is a markup tag inside them. Law: each in its own run,
    the toast read off the painted `Toast` equals the text exactly: Setup
    `0` → roster / projects section → `a`, an id typed twice → `Member|Project
    '<id lowercased>' already exists.`; phase editor `a` and `e` with an
    existing name → `'<name>' already exists.`; `R` → `Report written to
    <the written file>` (the one `.html` found on disk, compared whole with
    `str(path)`); an unreadable board at mount → the recovery message naming
    the `.corrupt` copy found on disk; a DIRECTORY named `history.jsonl` beside
    the board in `a[B]x`, then `]` → the toast equals `history.HISTORY_ERROR`
    of that same failing write (it holds `repr(path)`, P-16). RED on base:
    `MarkupError` or the text altered (`a[B]x` paints `ax`; the separator
    before `[B]x` is eaten). The `[LINK=…` phase-editor duplicate arms are
    RED UPSTREAM: the phase list they are typed from dies first. The
    three-backslash payload is inert at the Setup and phase-name toasts on
    base (no tag follows it)."""
    failures: list[str] = []
    arms = []
    n = iter(range(10_000))

    def d():
        return tmp_path / f"a{next(n)}"

    async def setup_arm(p, tabs, title_word):
        app = _app(_one(d()))
        uid = p.strip().lower()
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _press_select(app, pilot, "0", *(["tab"] * tabs))
            if app.view_mode != "setup" or app._setup_state.get("cursor_section") != tabs:
                return "fixture: not in the Setup section"
            for _ in range(2):
                await pilot.press("a")
                await _settle(pilot)
                if type(app.screen).__name__ != "TextPrompt":
                    return f"the id prompt did not open (screen {type(app.screen).__name__})"
                await pilot.press(*p, "enter")
                await _settle(pilot)
            return _toast_check(app, "Setup", f"{title_word} '{uid}' already exists.", True)

    async def phase_dup_arm(p, rename):
        phases = ["A", p, "Done"]
        app = _app(_one(d(), phase="A", phases=phases))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _press_select(app, pilot, "f", "e" if rename else "a")
            if type(app.screen).__name__ != "TextPrompt":
                return f"the phase prompt did not open (screen {type(app.screen).__name__})"
            if rename:
                await pilot.press("end", "backspace")
            await pilot.press(*p)
            await pilot.pause()
            typed = app.screen.query_one("#f-text").value
            if typed != p:
                return f"fixture: the prompt holds {typed!r}"
            await pilot.press("enter")
            await _settle(pilot)
            if app.board.phases != phases:
                return f"the phases changed to {app.board.phases!r}"
            return _toast_check(app, None, f"'{p}' already exists.", True)

    async def report_arm(dirname):
        here = d() / dirname
        app = _app(_one(here))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _press_select(app, pilot, "R")
            written = list((here / "reports").glob("*.html"))
            if len(written) != 1:
                return f"fixture: {len(written)} reports on disk"
            return _toast_check(app, "Report", f"Report written to {written[0]}", True)

    async def recovered_arm(dirname):
        here = d() / dirname
        here.mkdir(parents=True)
        (here / "board.json").write_text("{not json", encoding="utf-8")
        app = _app(here / "board.json")
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _settle(pilot)
            backup = here / "board.json.corrupt"
            if not backup.is_file():
                return "fixture: no .corrupt copy on disk"
            return _toast_check(app, "Board recovered",
                                f"board.json was unreadable; a copy was kept at {backup}. "
                                "Started empty — the original file was not overwritten.",
                                True)

    async def history_arm():
        here = d() / "a[B]x"
        path = _one(here, phase="Backlog")
        (here / "history.jsonl").mkdir()
        monkeypatch.setattr(history, "HISTORY_ERROR", None)
        app = _app(path)
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _press_select(app, pilot, "]")
            err = history.HISTORY_ERROR
            if app.board.tasks[0].phase != "Doing":
                return "fixture: ] did not move the task"
            if not err or repr(str(here / "history.jsonl")) not in err:
                return f"fixture: the failing write left {err!r}"
            return _toast_check(app, "Transition log", err, True)

    for p in PAYLOADS:
        arms += [
            (f"Setup duplicate member id [{p!r}]", lambda p=p: setup_arm(p, 2, "Member")),
            (f"Setup duplicate project id [{p!r}]", lambda p=p: setup_arm(p, 1, "Project")),
            (f"phase editor add duplicate [{p!r}]", lambda p=p: phase_dup_arm(p, False)),
            (f"phase editor rename duplicate [{p!r}]", lambda p=p: phase_dup_arm(p, True)),
        ]
    for dirname in DIRS:
        arms += [
            (f"report-written toast R [{dirname}]", lambda x=dirname: report_arm(x)),
            (f"board-recovered toast [{dirname}]", lambda x=dirname: recovered_arm(x)),
        ]
    arms.append(("transition-log toast ] [a[B]x/history.jsonl a directory]", history_arm))
    for name, fn in arms:
        await _collect(failures, name, fn)
    _verdict(failures, len(arms))


# ================================================================== TC-412 ==
async def test_TC_412_the_sync_failure_toast_shows_the_exception_text(tmp_path):
    """TC-412 (LLR-401.2, D-407) — declared fault injection.

    Field report: `_team_sync_tick` notifies `f"Team sync failed: {exc}"` with
    markup ON and no escape, so an exception message holding a tag kills the
    screen or vanishes. The sync path swallows its own errors (Q-3), so no
    black-box input reaches the toast: `TeamState.sync` is patched, AFTER the
    app has mounted and run its startup sync, to raise an exception carrying
    each payload, and the app's own tick callback is driven. Law: the painted
    `Team sync` toast's message equals `Team sync failed: <payload>` exactly.
    RED on base: `MarkupError` for `[LINK=…]`, `[b]y[/b]` styled away
    (`:smile: y`); `x\\\\\\` paints unchanged on base — no tag follows it in
    this message, an inert arm kept as a pin."""
    failures: list[str] = []
    arms = []
    n = iter(range(10_000))

    async def arm(p):
        here = tmp_path / f"a{next(n)}"
        shared = _team(here, [{"id": "a", "name": "Ann"}])
        path = _board(here, [Project("Local", "sky")], [Task("Plain title")], ["Todo", "Done"],
                      {"team_shared_dir": str(shared), "team_user_id": "a"})
        app = _app(path)
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _settle(pilot)
            if app.team_state is None:
                return "fixture: team mode is off"

            def boom(self, board):
                raise RuntimeError(p)

            with patch.object(TeamState, "sync", boom):
                app._team_sync_tick()
                await _settle(pilot)
            return _toast_check(app, "Team sync", f"Team sync failed: {p}", True)

    for p in PAYLOADS:
        arms.append((f"team-sync failure toast [{p!r}]", lambda p=p: arm(p)))
    for name, fn in arms:
        await _collect(failures, name, fn)
    _verdict(failures, len(arms))


# ================================================================== TC-415 ==
FLAGS = ("bold", "dim", "reverse", "underline")
HIGHLIGHT_NOTE = "a ==soon== b !!over!! c ++green++ d"


def _cells(app, sel) -> list[list[tuple[str, object]]]:
    """Each painted row of a widget's content region as (character, style)."""
    return [[(ch, seg.style) for seg in st for ch in seg.text]
            for st in _strip_rows(app, sel)]


def _line(cells) -> str:
    return "".join(ch for ch, _ in cells)


def _hex(st) -> str | None:
    if st is None or st.color is None or st.color.triplet is None:
        return None
    return st.color.triplet.hex.lower()


def _one_of(values: set):
    return values.pop() if len(values) == 1 else "mixed"


def _flags(rows, text: str, anchor: str | None = None):
    """The painted text-style flags over the non-blank cells of `text` in the
    first row holding it (and `anchor`): each True / False, or "mixed", and the
    foreground colour — Textual paints `dim` as a blended colour, not as the
    attribute (the `dim` flag reads False at every dim site on base), so the
    colour is what carries it; None when `text` is not painted."""
    for cells in rows:
        line = _line(cells)
        if anchor is not None and anchor not in line:
            continue
        i = line.find(text)
        if i < 0:
            continue
        styles = [st for ch, st in cells[i:i + len(text)] if not ch.isspace()]
        out = {f: _one_of({bool(getattr(st, f, None)) if st is not None else False
                           for st in styles}) for f in FLAGS}
        out["color"] = _one_of({_hex(st) for st in styles})
        return out
    return None


def _tones(app, sel) -> dict:
    """The note's own row (`a soon b over c green d`, not the `highlight:`
    legend above it): each highlighted word's colour, the plain text's
    colour, and which markers that row still paints."""
    rows = [r for r in _cells(app, sel)
            if "soon" in _line(r) and "over" in _line(r) and "highlight" not in _line(r)]
    if not rows:
        return {"note row": None}
    row, line = rows[0], _line(rows[0])
    out = {}
    for word in ("soon", "over", "green", " b "):
        i = line.find(word)
        out[word.strip()] = _one_of({_hex(st) for ch, st in row[i:i + len(word)]
                                     if not ch.isspace()})
    out["markers painted"] = [m for m in ("==", "!!", "++") if m in line]
    return out


async def _css_bold_off(app, pilot):
    """The lens the stylesheet cannot answer for (review F2): `.modal-title`
    is `text-style: bold` in `taskboard.tcss`, so a title's PAINTED bold says
    nothing about the bold piece the code builds — drop that piece and the
    title still paints bold. An inline `text-style: none` on every
    `.modal-title` of the screen (inline styles beat the stylesheet) leaves the
    content's own spans as the only source of bold. A test-side control lens,
    not a product state: the "(CSS bold off)" arms read through it."""
    for w in app.screen.query(".modal-title"):
        w.styles.text_style = "none"
    await _settle(pilot)


async def _style_readings(tmp: Path, chdir) -> dict:
    """Every TC-415 reading, each site in its own run. The SAME function
    recorded the base literals (`evidence/inc001-style-base.txt`, written by
    `evidence/inc001_style_base.py`)."""
    from taskboard.views import help_example, help_usage
    today = date.today().isoformat()
    got: dict = {}
    n = iter(range(10_000))

    def d():
        return tmp / f"s{next(n)}"

    async def run(path, keys, fn, end_box=None):
        app = _app(path)
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _press_select(app, pilot, *keys)
            if end_box:
                app.screen.query_one(end_box).scroll_end(animate=False)
                await _settle(pilot)
            await fn(app, pilot)

    async def details(app, pilot):
        rows = _cells(app, "#details-box")
        got["details title"] = _flags(rows, "Plain title")
        got["details title tail"] = _flags(rows, "o open raw · esc close")
        got["details — placeholders"] = [_flags([r], "—") for r in rows
                                         if _line(r).strip() == "—"]
        await _css_bold_off(app, pilot)
        rows = _cells(app, "#details-box")
        got["details title (CSS bold off)"] = _flags(rows, "Plain title")
        got["details title tail (CSS bold off)"] = _flags(rows, "o open raw · esc close")
    await run(_one(d()), ["enter"], details)

    async def viewer(app, pilot):
        rows = _cells(app, "#viewer-box")
        got["viewer title"] = _flags(rows, "Plain title")
        got["viewer title tail"] = _flags(rows, "o open raw · esc close")
        await _css_bold_off(app, pilot)
        rows = _cells(app, "#viewer-box")
        got["viewer title (CSS bold off)"] = _flags(rows, "Plain title")
        got["viewer title tail (CSS bold off)"] = _flags(rows, "o open raw · esc close")
    await run(_one(d()), ["i"], viewer)

    async def missing(app, pilot):
        rows = _cells(app, "#details-box")
        got["missing: prefix"] = _flags(rows, "missing:")
        got["missing: reference"] = _flags(rows, "nope.png", anchor="missing:")
    await run(_one(d(), images=["nope.png"]), ["enter"], missing)

    here = d()
    here.mkdir(parents=True)
    (here / "bad.png").write_bytes(b"not a png at all")
    chdir(here)

    async def corrupt(app, pilot):
        rows = _cells(app, "#details-box")
        got["could not render: prefix"] = _flags(rows, "could not render:")
        got["could not render: reference"] = _flags(rows, "bad.png",
                                                    anchor="could not render:")
    await run(_one(here, images=["bad.png"]), ["enter"], corrupt, end_box="#details-box")

    async def picker(app, pilot):
        got["picker: Beta row is off the cursor"] = (
            app.screen.query_one("#proj-list").highlighted != 1)
        rows = _cells(app, "#picker-box")
        got["picker off-cursor name"] = _flags(rows, "Beta", anchor="archived")
        got["picker off-cursor archived"] = _flags(rows, "archived", anchor="Beta")
        got["picker off-cursor status (plain)"] = _flags(rows, "on_track", anchor="Beta")
    alpha, beta = Project("Alpha", "sky"), Project("Beta", "rose", archived=True)
    await run(_board(d(), [alpha, beta], [Task("Plain title", alpha.id, "Doing")]),
              ["P"], picker)

    async def phases(app, pilot):
        got["phase editor: row 2 is off the cursor"] = (
            app.screen.query_one("#phase-list").highlighted != 1)
        rows = _cells(app, "#picker-box")
        got["phase editor off-cursor N."] = _flags(rows, "2.", anchor="Doing")
        got["phase editor off-cursor name"] = _flags(rows, "Doing", anchor="2.")
        got["phase editor off-cursor count (plain)"] = _flags(rows, "1 task", anchor="2.")
        got["phase editor title"] = next((_line(r).strip() for r in rows
                                          if "Phases" in _line(r)), None)
    await run(_one(d()), ["f"], phases)

    async def prompt(app, pilot):
        got["text prompt title"] = _flags(_cells(app, "#modal-box"), "New phase")
        await _css_bold_off(app, pilot)
        got["text prompt title (CSS bold off)"] = _flags(_cells(app, "#modal-box"),
                                                         "New phase")
    await run(_one(d()), ["f", "a"], prompt)

    async def standup(app, pilot):
        rows = _cells(app, "#modal-box")
        got["standup title"] = _flags(rows, "Standup · week ending")
        got["standup ▐ project"] = _flags(rows, "▐ Plain")
        got["standup phase"] = _flags(rows, "Doing", anchor="Plain title")
        got["standup task title (plain)"] = _flags(rows, "Plain title")
        got["standup k/n closed"] = _flags(rows, "0/1 closed this week")
        await _css_bold_off(app, pilot)
        rows = _cells(app, "#modal-box")
        got["standup title (CSS bold off)"] = _flags(rows, "Standup · week ending")
        got["standup ▐ project (CSS bold off)"] = _flags(rows, "▐ Plain")
    await run(_one(d(), phase_changed=today), ["S"], standup)

    async def calendar(app, pilot):
        app.screen.query_one("#cal-f-due").focus()
        await pilot.press("enter")
        await _settle(pilot)
        got["calendar opened"] = type(app.screen).__name__
        title = _cells(app, "#cal-title")
        grid = _cells(app, "#cal-grid")
        got["calendar month"] = _flags(title, "October 2026")
        got["calendar title"] = next((_line(r).strip() for r in title
                                      if "October" in _line(r)), None)
        got["calendar week header"] = _flags(grid, "Mo Tu We Th Fr Sa Su")
        got["calendar selected day"] = _flags(grid, "15")
        got["calendar day in month"] = _flags(grid, "16")
        got["calendar days outside the month"] = _flags(grid, "28 29 30")
        await _css_bold_off(app, pilot)
        got["calendar month (CSS bold off)"] = _flags(_cells(app, "#cal-title"),
                                                      "October 2026")
    await run(_one(d(), due_date="2026-10-15"), ["e"], calendar)

    async def help_modal(app, pilot):
        rows = _cells(app, "#help-modal-box")
        got["help title"] = _flags(rows, "Help · swimlanes")
        got["help Usage heading"] = _flags(rows, "Usage")
        got["help Keys heading"] = _flags(rows, "Keys")
        got["help usage section heading"] = _flags(rows, help_usage("swimlanes")[0][0])
        got["help example meaning"] = _flags(rows, help_example("swimlanes")[1][:12])
        got["help usage bullet (plain)"] = _flags(rows, help_usage("swimlanes")[0][1][0][:12])
        await _css_bold_off(app, pilot)
        rows = _cells(app, "#help-modal-box")
        got["help title (CSS bold off)"] = _flags(rows, "Help · swimlanes")
        got["help Usage heading (CSS bold off)"] = _flags(rows, "Usage")
        got["help Keys heading (CSS bold off)"] = _flags(rows, "Keys")
    await run(_one(d()), ["question_mark"], help_modal)

    async def tones_details(app, pilot):
        got["details highlight"] = _tones(app, "#details-box")
    await run(_one(d(), notes=HIGHLIGHT_NOTE), ["enter"], tones_details)

    async def tones_preview(app, pilot):
        from textual.widgets import TextArea
        notes = app.screen.query_one("#f-notes", TextArea)
        notes.focus()
        await pilot.pause()
        await pilot.press(*HIGHLIGHT_NOTE)
        await _settle(pilot)
        got["preview typed"] = notes.text == HIGHLIGHT_NOTE
        got["preview highlight"] = _tones(app, "#task-preview")
    await run(_one(d()), ["e"], tones_preview)
    return got


def _f(color: str, bold=False, reverse=False, underline=False) -> dict:
    """A base reading: the flags, `dim` False everywhere (Textual paints dim
    as a colour — the colour literal is the dim pin)."""
    return {"bold": bold, "dim": False, "reverse": reverse, "underline": underline,
            "color": color}


# Recorded on the base tree (HEAD 56a1b10, taskboard/ unmodified) by
# `evidence/inc001_style_base.py` -> `evidence/inc001-style-base.txt`, BEFORE the
# conversion; the "(CSS bold off)" rows (round 2, review F2) by the same script
# over a `git archive 56a1b10` export -> `evidence/inc001-style-base-r2.txt`.
# "(plain)" rows are the unstyled neighbour each dim pin is read against: a
# dropped `[dim]` piece paints the neighbour's colour.
#
# The `.modal-title` rows: the stylesheet bolds every `.modal-title`, so their
# PAINTED bold pins the painted result only — dropping the code's bold piece
# leaves it bold (review F2, measured in `evidence/inc001-style-mutations.txt`).
# The code's own bold is pinned by the "(CSS bold off)" sibling, read through
# `_css_bold_off`.
STYLE_BASE = {
    "details title": _f("#8b98a5", bold=True),
    # base: the WHOLE title row is bold — `.modal-title` is bold in the
    # stylesheet — so the tail is bold too (LLR-401.3's "tail not bold" is not
    # what base paints; pinned as painted)
    "details title tail": _f("#8b98a5", bold=True),
    "details title (CSS bold off)": _f("#8b98a5", bold=True),
    # the tail's own spans are NOT bold — LLR-401.3's "tail not bold", which
    # the painted row cannot show (the stylesheet bolds the whole row)
    "details title tail (CSS bold off)": _f("#8b98a5"),
    "details — placeholders": [_f("#9ca2a8"), _f("#606a75"), _f("#606a75")],
    "viewer title": _f("#8b98a5", bold=True),
    "viewer title tail": _f("#8b98a5", bold=True),
    "viewer title (CSS bold off)": _f("#8b98a5", bold=True),
    "viewer title tail (CSS bold off)": _f("#8b98a5"),
    "missing: prefix": _f("#606a75"),
    "missing: reference": _f("#8b98a5"),
    "could not render: prefix": _f("#606a75"),
    "could not render: reference": _f("#8b98a5"),
    "picker: Beta row is off the cursor": True,
    "picker off-cursor name": _f("#e0e0e0", bold=True),
    "picker off-cursor archived": _f("#9a9d9f"),
    "picker off-cursor status (plain)": _f("#e0e0e0"),
    "phase editor: row 2 is off the cursor": True,
    "phase editor off-cursor N.": _f("#a1a1a1"),
    "phase editor off-cursor name": _f("#e0e0e0", bold=True),
    "phase editor off-cursor count (plain)": _f("#e0e0e0"),
    "text prompt title": _f("#8b98a5", bold=True),
    "text prompt title (CSS bold off)": _f("#8b98a5", bold=True),
    "standup title": _f("#8b98a5", bold=True),
    "standup ▐ project": _f("#8b98a5", bold=True),
    "standup title (CSS bold off)": _f("#8b98a5", bold=True),
    "standup ▐ project (CSS bold off)": _f("#8b98a5", bold=True),
    "standup phase": _f("#606a75"),
    "standup task title (plain)": _f("#8b98a5"),
    "standup k/n closed": _f("#606a75"),
    "calendar opened": "CalendarModal",
    "calendar month": _f("#8b98a5", bold=True),
    "calendar month (CSS bold off)": _f("#8b98a5", bold=True),
    "calendar week header": _f("#89919b"),
    "calendar selected day": _f("#c9d3df", bold=True, reverse=True),
    "calendar day in month": _f("#c9d3df"),
    "calendar days outside the month": _f("#89919b"),
    "help title": _f("#e6edf7", bold=True),
    "help Usage heading": _f("#e6edf7", bold=True),
    "help Keys heading": _f("#e6edf7", bold=True),
    "help title (CSS bold off)": _f("#e6edf7", bold=True),
    "help Usage heading (CSS bold off)": _f("#e6edf7", bold=True),
    "help Keys heading (CSS bold off)": _f("#e6edf7", bold=True),
    "help usage section heading": _f("#e6edf3", underline=True),
    "help example meaning": _f("#9ca2a8"),
    "help usage bullet (plain)": _f("#e6edf3"),
    "details highlight": {"soon": "#fbbf24", "over": "#f43f5e", "green": "#4ade80",
                          "b": "#8b98a5", "markers painted": []},
    "preview typed": True,
    "preview highlight": {"soon": "#fbbf24", "over": "#f43f5e", "green": "#4ade80",
                          "b": "#8b98a5", "markers painted": []},
}


async def test_TC_415_converted_sites_keep_their_painted_style(tmp_path, monkeypatch):
    """TC-415 (LLR-401.3) — the conversion to Text pieces keeps every painted style.

    Field report: the sites LLR-401.3 converts carry app styling written as
    markup around user text (`[b]{name}[/b]`, `[dim]archived[/dim]`, `[u]…`,
    `[b reverse]15[/]`, the notes' `==`/`!!`/`++` tones); rebuilding them as
    pieces can silently drop a piece's style, and nothing else would notice.
    Law: each reading below — the painted flags (bold, dim, reverse, underline)
    and foreground colour over the named text, read from the painted segments
    of the site's own box — equals the literal the base tree painted
    (`STYLE_BASE`, recorded first by `evidence/inc001_style_base.py`); and the
    app's bracket key hints paint without a backslash: the phase editor's
    `[ / ] reorder` and the calendar's `[ ] month`.

    A PRESERVATION PIN: GREEN on base for every `STYLE_BASE` arm. The mutation
    that reddens each arm: drop the bold piece of the picker or phase-editor
    name → bold False; drop the bold piece of a `.modal-title` (details /
    viewer / prompt / standup / help / calendar month titles, `▐ project`, the
    help headings) → its "(CSS bold off)" arm turns bold False, while its
    PAINTED arm stays bold — the stylesheet's `.modal-title` rule bolds it
    anyway, so the painted arm pins the painted result and cannot go RED by
    any single code-side mutation (review F2); drop `text-style: bold` from
    `.modal-title` → the painted title tails turn bold False; bold a title
    tail's piece → its "(CSS bold off)" tail arm turns bold True; drop a dim
    piece (`archived`, `N.`, standup
    phase and `k/n closed`, calendar header and outside days, help meaning,
    `—`, `missing:` / `could not render:`) → that text paints its "(plain)"
    neighbour's colour; drop `[u]` → underline False; drop `reverse` from the
    selected day → reverse False; let a style piece cover user text → the
    "(plain)" / reference pins change; build the notes without the shared
    tokeniser → the tones turn plain and the markers paint. Per-arm verdicts:
    `evidence/inc001-style-mutations.txt`. Known base RED:
    the calendar title paints `[ \\] month` (the `\\]` escape is not undone
    by Textual) — the law arm, not a base pin; on base this node fails on that
    arm alone."""
    got = await _style_readings(tmp_path, monkeypatch.chdir)
    failures = [f"{k}: base painted {v!r}, now {got.get(k, '<not read>')!r}"
                for k, v in STYLE_BASE.items() if got.get(k, "<not read>") != v]
    phase_title = got.get("phase editor title") or ""
    if "[ / ] reorder" not in phase_title or "\\" in phase_title:
        failures.append(f"phase editor title: {phase_title!r} does not paint '[ / ] reorder' "
                        "without a backslash")
    cal_title = got.get("calendar title") or ""
    if "[ ] month" not in cal_title or "\\" in cal_title:
        failures.append(f"calendar title: {cal_title!r} does not paint '[ ] month' "
                        "without a backslash")
    assert not failures, (f"{len(failures)} of {len(STYLE_BASE) + 2} style arms failed:\n  "
                          + "\n  ".join(failures))


# ================================================================== AT-407 ==
HOSTILE = {"status": "[@click=app.view('gantt')]X", "color": [], "name": 123, "due_date": 7}
ROSTER_OK = [{"id": "a", "name": "Ann"}]
ROSTER_HOSTILE = [{"id": "b", "name": 123, "hue": []}, {"id": "a"}, {"id": "a", "name": "Dup"}]
VIEW_KEYS = (("1", "swimlanes"), ("2", "agenda"), ("3", "gantt"), ("4", "kanban"),
             ("5", "focus"), ("7", "flow"), ("8", "standup"), ("9", "people"),
             ("0", "setup"))                  # the eight views and Setup (keymap.py)


async def test_AT_407_a_shared_config_cannot_act_or_crash(tmp_path):
    """AT-407 (HLR-404, LLR-404.1, LLR-404.2, US-404) — a hostile `team.json`.

    Field report (P2 security S-1 HIGH, S-3; P-12, P-15): the shared directory
    is another person's to write. On base `apply_config_to_board` `setattr`s a
    synced project's raw fields onto the board: a status `[@click=app.pwn]X`
    reached the project picker line as markup and a click on it FIRED the
    action; a colour that is not a palette key (`evil`, `[]`) raises in the
    board views, a name `123` raises in render; two synced projects (or roster
    entries) with one id are both kept; a roster name `123` raises in people
    and standup, a roster hue `[]` in Setup.

    Law (HLR-404 threshold), each case in its own `App.run_test`, failures
    collected: (a) the board holds `p1` (`Alpha`, due `2026-10-09`); the
    synced p1 entry carries the hostile status / colour / name / due; after
    the startup sync (as `a`) and `P`, p1's picker line paints `Alpha` and
    `on_track` and neither `[@click` nor `gantt`; then one run per painted
    cell of that status run: a click on it leaves the view `swimlanes`, and
    the board keeps p1's name `Alpha` and due `2026-10-09`. (b) a new synced
    `n1` with the same hostile fields and a duplicate `n1` named `Second`: the
    board and the picker hold exactly one `n1`, painted
    `Untitled  ·  on_track` (the first entry), and `Second` is painted
    nowhere. (c) a roster with a duplicate id and a hostile entry: with no
    identity the identity picker opens and lists `b` (for the name `123`) and
    `a`, each once, and not `Dup`; as `a` with the whole hostile `team.json`,
    each of the eight views (keys `1`..`5`, `7`..`9`) and Setup (`0`) is
    entered, one run each, across one clock tick, and the app stays up.
    (d) boundary: a valid synced `paused` / `sky` IS applied (picker paints
    `paused`, board colour `sky`) and a synced `null` due clears p1's due.

    RED on the pre-fix tree (the increment-001 tree, no HLR-404 validation):
    every case but (d) — the per-case reasons are in
    `evidence/inc002-at407-red-prefix.txt`. Since increment 001 the picker
    line is Text pieces, so the status no longer parses as an action there;
    on this tree the hostile entry is caught by what it paints and what it
    crashes, not by a fired action. Case (d) is a boundary pin that passes on
    both trees by design (the raw `setattr` applies valid values too)."""
    failures: list[str] = []
    n = iter(range(10_000))

    def d():
        return tmp_path / f"a{next(n)}"

    def fixture(projects, roster=ROSTER_OK, user="a", color="lime") -> Path:
        here = d()
        shared = _team(here, roster, projects)
        settings = {"team_shared_dir": str(shared)}
        if user:
            settings["team_user_id"] = user
        p1 = Project("Alpha", color, id="p1", due_date="2026-10-09")
        task = Task("Plain title", "p1", "Todo", start_date="2026-10-01",
                    due_date="2026-10-09")
        return _board(here, [p1], [task], ["Todo", "Done"], settings)

    def p1_of(app):
        return next((p for p in app.board.projects if p.id == "p1"), None)

    def p1_kept(app) -> str | None:
        p = p1_of(app)
        if p is not None and p.name == "Alpha" and p.due_date == "2026-10-09":
            return None
        return (f"board p1 name / due became {getattr(p, 'name', None)!r} / "
                f"{getattr(p, 'due_date', None)!r}")

    async def open_picker(app, pilot):
        await _settle(pilot)
        if app.team_state is None or app.team_state.user_id != "a":
            return "fixture: team mode as `a` is off"
        await _press_select(app, pilot, "P")
        if type(app.screen).__name__ != "ProjectPicker":
            return f"the project picker did not open (screen {type(app.screen).__name__})"
        return None

    def option_rows(app) -> list[str]:
        return [r.strip(" ▊▎│") for r in _rows(app, "#proj-list") if "  ·  " in r]

    # -- (a) the existing project ------------------------------------------
    hostile_p1 = [{"id": "p1", **HOSTILE}]
    found: dict = {}

    async def a_paint(entries=hostile_p1, key="cells"):
        """Paint checks; records the painted status run's cells for the clicks."""
        app = _app(fixture(entries))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            why = await open_picker(app, pilot)
            if why:
                return why
            rows = _rows(app, "#proj-list")
            hit = [(i, r) for i, r in enumerate(rows) if "  ·  " in r]
            if len(hit) != 1:
                return f"expected one project line, painted {[r for _, r in hit]!r}"
            i, row = hit[0]
            start = row.index("  ·  ") + len("  ·  ")
            end = row.find("  ·  ", start)
            found[key] = (i, start, len(row.rstrip()) if end < 0 else end)
            line = row.strip(" ▊▎│")
            bad = []
            if not line.startswith("Alpha  ·  "):
                bad.append("the name is not painted `Alpha`")
            if "on_track" not in line:
                bad.append("the status is not painted `on_track`")
            if "[@click" in line or "gantt" in line:
                bad.append("the synced action tag is painted")
            if p1_kept(app):
                bad.append(p1_kept(app))
            return (f"line {line!r}: " + "; ".join(bad)) if bad else None

    async def a_click(row: int, col: int, entries=hostile_p1):
        app = _app(fixture(entries))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            why = await open_picker(app, pilot)
            if why:
                return why
            if app.view_mode != "swimlanes":
                return f"fixture: the view is {app.view_mode!r} before the click"
            ol = app.screen.query_one("#proj-list")
            cr = ol.content_region
            await pilot.click(ol, offset=(cr.x - ol.region.x + col, cr.y - ol.region.y + row))
            await _settle(pilot)
            bad = []
            if app.view_mode != "swimlanes":
                bad.append(f"the click changed the view to {app.view_mode!r}")
            if type(app.screen).__name__ == "ProjectModal":   # a click opens the editor
                await pilot.press("escape")
                await _settle(pilot)
                if app.view_mode != "swimlanes":
                    bad.append(f"the view is {app.view_mode!r} after esc")
            if p1_kept(app):
                bad.append(p1_kept(app))
            return "; ".join(bad) or None

    # -- (b) the new project and its duplicate -----------------------------
    async def b_new():
        app = _app(fixture([{"id": "n1", **HOSTILE}, {"id": "n1", "name": "Second"}]))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            why = await open_picker(app, pilot)
            if why:
                return why
            rows = option_rows(app)
            bad = []
            n1 = sum(p.id == "n1" for p in app.board.projects)
            if n1 != 1:
                bad.append(f"the board holds {n1} `n1` projects")
            if len(rows) != 2:
                bad.append(f"{len(rows)} project lines painted for 2 ids")
            if sum(r.startswith("Untitled  ·  on_track  ·  ") for r in rows) != 1:
                bad.append("not exactly one `Untitled  ·  on_track` line")
            if any("Second" in r for r in _rows(app)):
                bad.append("the duplicate entry `Second` is painted")
            return (f"lines {rows!r}: " + "; ".join(bad)) if bad else None

    # -- (c) the roster and every view -------------------------------------
    async def c_identity():
        app = _app(fixture([], roster=ROSTER_HOSTILE, user=None))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _settle(pilot)
            if type(app.screen).__name__ != "TeamIdentityPicker":
                return f"the identity picker did not open (screen {type(app.screen).__name__})"
            listed = [r.strip(" ▊▎│") for r in _rows(app, "#identity-list")]
            listed = [r for r in listed if r]
            return None if listed == ["b", "a"] else (
                f"the picker lists {listed!r}, expected ['b', 'a'] (each roster id once, "
                "`b` for the name 123, the first `a`)")

    everything = [{"id": "p1", **HOSTILE}, {"id": "n1", **HOSTILE},
                  {"id": "n1", "name": "Second"}]

    async def c_view(key: str, mode: str, projects=everything):
        app = _app(fixture(projects, roster=ROSTER_HOSTILE))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            await _settle(pilot)
            if app.team_state is None or app.team_state.user_id != "a":
                return "fixture: team mode as `a` is off"
            await pilot.press(key)
            await _settle(pilot)
            await pilot.pause(1.2)        # one clock tick: lanes / gantt repaint
            await _settle(pilot)
            if app.view_mode != mode:
                return f"key {key!r} left the view at {app.view_mode!r}"
            return None

    # -- (d) the boundary --------------------------------------------------
    async def d_valid():
        app = _app(fixture([{"id": "p1", "status": "paused", "color": "sky",
                             "due_date": None}]))
        async with app.run_test(size=SIZE, notifications=True) as pilot:
            why = await open_picker(app, pilot)
            if why:
                return why
            rows = option_rows(app)
            p = p1_of(app)
            bad = []
            if len(rows) != 1 or not rows[0].startswith("Alpha  ·  paused  ·  "):
                bad.append(f"the line is not painted `Alpha  ·  paused`: {rows!r}")
            if p is None or p.color != "sky":
                bad.append(f"the synced colour `sky` was not applied "
                           f"({getattr(p, 'color', None)!r})")
            if p is None or p.due_date is not None:
                bad.append(f"the synced null due did not clear it "
                           f"({getattr(p, 'due_date', None)!r})")
            return "; ".join(bad) or None

    async def clicks(label: str, entries, key: str) -> int:
        """One run per painted cell of the status run `a_paint` recorded."""
        if key not in found:
            failures.append(f"{label}: not executed — no painted p1 line to click "
                            "(see its paint run)")
            return 1
        row, start, end = found[key]
        for col in range(start, end):
            await _collect(failures, f"{label} cell {col - start}",
                           lambda c=col: a_click(row, c, entries))
        return end - start

    # (a) first: its paint run finds the painted status cells to click.
    await _collect(failures, "(a) p1 picker line after the hostile sync", a_paint)
    total = 1 + await clicks("(a) click on p1's status", hostile_p1, "cells")
    # Isolation (not a separate threshold): each hostile field alone, so one
    # field's crash cannot hide another's — the same law, one field per run;
    # the status alone is clicked cell by cell like the whole entry.
    alone = {f: [{"id": "p1", f: v}] for f, v in HOSTILE.items()}
    for f, entries in alone.items():
        await _collect(failures, f"(a) p1 picker line, synced {f} alone",
                       lambda e=entries, f=f: a_paint(e, f"alone-{f}"))
        total += 1
    total += await clicks("(a) click on p1's status, synced status alone",
                          alone["status"], "alone-status")
    arms = [("(b) new n1 and its duplicate in the picker", b_new),
            ("(c) identity picker over the hostile roster", c_identity)]
    arms += [(f"(c) view {mode} (key {key!r}) as `a`", lambda k=key, m=mode: c_view(k, m))
             for key, mode in VIEW_KEYS]
    arms += [(f"(c) view {mode} (key {key!r}) as `a`, hostile roster alone",
              lambda k=key, m=mode: c_view(k, m, projects=[]))
             for key, mode in VIEW_KEYS if mode in ("standup", "people", "setup")]
    arms.append(("(d) valid paused / sky / null due applied", d_valid))
    for name, fn in arms:
        await _collect(failures, name, fn)
    _verdict(failures, total + len(arms))

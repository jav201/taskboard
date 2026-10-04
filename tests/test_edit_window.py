"""The task edit window — variant C of the 2026-09-30 round (owner verdict).

Field report (Javier, 2026-09-30): "Cuando se editan tareas toda la interfaz de
edición está muy amontonada y sobre todo la parte de texto es muy pequeña como
para ver con claridad todo el contenido que ya está más el que se está
escribiendo." Measured on the shipped editor with the round's 23-line task: 3
note rows visible at 120x36 AND at 80x24, and with the cursor in the notes the
title and Save had scrolled off the top and bottom of the modal.

The verdict: full screen, one title line, a chip row of properties, the notes
beside a live preview, URLs / images / Save in a footer strip. These tests pin
what that verdict BOUGHT, so a later "tidy-up" cannot quietly give it back.
Batch 2026-09-30-batch-01 · HLR-001 / HLR-002.
"""
from __future__ import annotations

import pytest
from rich.cells import cell_len
from textual.widgets import Checkbox, Input, Select, TextArea

from taskboard.app import TaskboardApp
from taskboard.models import Board, Project, Task
from taskboard.modals import TaskModal
from taskboard.views import HEX

ACCENT = HEX["accent"]

# The round's fixture notes: 23 logical lines, es/en, all three highlights, a
# list and a URL — the shape of a real working note, not lorem ipsum.
LONG_NOTES = """Contexto: el cliente quiere migrar el ==portal de proveedores== antes del cierre de Q4; la fase 1 (catálogo) ya está en producción.
Owner: Javier · reviewer: Lucía (backend) · QA: Marco

Decisiones tomadas
- Auth via SSO (Azure AD) — ++aprobado por TI el 24/09++
- Mantener el endpoint legacy /v1/invoices hasta enero
- !!No tocar el esquema de pagos sin sign-off de finanzas!!
- Rate limit: 100 req/min por proveedor, burst de 20

Open questions
- ¿El export CSV necesita columnas en inglés o en español?
- Who owns the S3 bucket after go-live? ==preguntar a Diego==
- Staging data: anonimizar RFC y CLABE antes de compartir con el proveedor externo

Plan de esta semana
1. Terminar el mapping de campos (60% hecho, faltan impuestos y retenciones)
2. Demo interna el jueves 10:00 — ++sala reservada++
3. !!Bloqueante: credenciales de staging vencen el 02/10!!
4. Draft del runbook de rollback (owner: Lucía)

Ref: https://wiki.example.com/portal/migracion-fase-2
Llamada 29/09: el CFO pidió un reporte semanal con avance, riesgos y fechas comprometidas; quiere verlo en el mismo formato que el de fase 1.
Próximo paso: confirmar con Lucía si el webhook de pagos puede quedar detrás del feature flag hasta """

# Every widget id the rest of the app and the existing tests talk to. The
# editor's layout may move them; it may not drop or hide one.
CONTRACT_IDS = ("f-title", "f-project", "f-phase", "f-priority", "f-start",
                "cal-f-start", "f-due", "cal-f-due", "f-blocked", "f-archived",
                "f-pinned", "f-notes", "f-urls", "f-images", "paste-img",
                "save", "cancel")
SIZES = [(120, 36), (80, 24)]
MIN_NOTE_ROWS = {(120, 36): 20, (80, 24): 10}


def _board(tmp_path) -> Board:
    b = Board.load(tmp_path / "board.json")
    b.projects.clear()
    b.tasks.clear()
    p = Project("Portal Proveedores", "sky")
    b.projects.append(p)
    b.tasks.append(Task("Migrar portal de proveedores (fase 2)", p.id, "Doing",
                        "high", due_date="2026-10-02", notes=LONG_NOTES,
                        urls=["https://wiki.example.com/portal/migracion-fase-2",
                              "https://github.com/example/portal/pull/412"],
                        images=["images/x/pasted.png"]))
    b.save()
    return b


def _app(tmp_path) -> TaskboardApp:
    b = _board(tmp_path)
    return TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


async def _open_editor(app, pilot):
    """Through the shipped surface: select the task and press `e`."""
    await pilot.pause()
    app.selected_task_id = app.board.tasks[0].id
    await pilot.press("e")
    for _ in range(3):
        await pilot.pause()
    assert isinstance(app.screen, TaskModal), "`e` did not open the editor"
    return app.screen


async def _open_editor_writing(app, pilot):
    """...and put the cursor at the END of the notes — the 'I am writing'
    state the complaint is about."""
    scr = await _open_editor(app, pilot)
    ta = scr.query_one("#f-notes", TextArea)
    ta.focus()
    ta.move_cursor(ta.document.end)
    for _ in range(3):
        await pilot.pause()
    return scr


# The clip and the painted cells have no public API in textual 8.2.8; these
# helpers read the compositor (private) on purpose, in one place, so a
# rename in a later Textual errors HERE rather than silently passing.
def _fully_visible(screen, widget) -> bool:
    vis = screen._compositor.visible_widgets
    if widget not in vis:
        return False
    region, clip = vis[widget]
    return region.area > 0 and region.intersection(clip) == region


def _note_rows(screen) -> int:
    ta = screen.query_one("#f-notes", TextArea)
    vis = screen._compositor.visible_widgets
    if ta not in vis:
        return 0
    region, clip = vis[ta]
    return region.shrink(ta.styles.gutter).intersection(clip).height


def _painted(app):
    return app.screen._compositor.render_strips(app.screen.size)


def _hex(seg) -> str | None:
    col = seg.style.color if seg.style else None
    return col.triplet.hex.lower() if col is not None and col.triplet else None


# --------------------------------------------------------------------------- #
# AT-001 — the notes own the screen, and nothing else falls off it
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("size", SIZES, ids=lambda s: f"{s[0]}x{s[1]}")
async def test_the_notes_own_the_screen_while_writing(tmp_path, size):
    """AT-001 (HLR-001). With the 23-line note open and the cursor at its end,
    the editor shows >= 20 note rows at 120x36 and >= 10 at 80x24, a preview
    at least 20 columns wide holding about as many rows, and the title, Save
    and every other control wholly on screen.

    Why each limb: the rows are the complaint; the title and Save are what the
    old modal scrolled away the moment you typed (you could not see WHICH task
    you were writing in, nor reach Save without scrolling back); the full id
    list is the contract the rest of the app talks to. RED on the base tree:
    3 rows at both sizes, title and Save off-screen."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        scr = await _open_editor_writing(app, pilot)
        rows = _note_rows(scr)
        assert rows >= MIN_NOTE_ROWS[size], f"{size}: only {rows} note rows visible"
        hidden = [wid for wid in CONTRACT_IDS
                  if not _fully_visible(scr, scr.query_one(f"#{wid}"))]
        assert not hidden, f"{size}: off-screen or clipped while writing: {hidden}"
        prev = scr.query_one("#task-preview-scroll")
        assert prev.region.width >= 20, f"{size}: preview {prev.region.width} cols"
        assert prev.region.height >= rows - 2, \
            f"{size}: preview {prev.region.height} rows vs notes {rows}"


async def test_a_new_task_gets_the_same_room(tmp_path):
    """The empty boundary: `a` opens the same editor with no notes at all; the
    layout must not depend on content to hold its controls on screen."""
    app = _app(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("a")
        for _ in range(3):
            await pilot.pause()
        scr = app.screen
        assert isinstance(scr, TaskModal)
        assert _note_rows(scr) >= MIN_NOTE_ROWS[(80, 24)]
        hidden = [wid for wid in CONTRACT_IDS
                  if not _fully_visible(scr, scr.query_one(f"#{wid}"))]
        assert not hidden, f"new-task editor hides {hidden}"


# --------------------------------------------------------------------------- #
# LLR-001.1 — the chip row wraps instead of clipping
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("width", list(range(80, 141, 4)) + ["threshold-1", "threshold"])
async def test_every_chip_stays_reachable_at_every_width(tmp_path, width):
    """The limit the round measured: at 80 columns variant C's one-row chip
    row was clipped and the flags fell off the right edge — a control you
    cannot see is a control you cannot tab to with confidence. The row wraps
    to two rows below the width where it fits. The swept set of chips is READ
    FROM THE CHIP ROW ITSELF (every focusable widget in it) and guarded, so a
    chip added later is swept too (C-31); the threshold and the column below
    it are always in the sweep. RED: force the one-row layout at 80 ->
    `f-pinned` (and its neighbours) clipped."""
    from taskboard.modals import TASK_CHIPS_ONE_ROW
    if width == "threshold":
        width = TASK_CHIPS_ONE_ROW
    elif width == "threshold-1":
        width = TASK_CHIPS_ONE_ROW - 1
    app = _app(tmp_path)
    async with app.run_test(size=(width, 36)) as pilot:
        scr = await _open_editor_writing(app, pilot)
        chips = [w for w in scr.query_one("#task-chips").query("*")
                 if w.can_focus and w.id]
        assert len(chips) >= 10, f"chip set looks wrong: {[w.id for w in chips]}"
        clipped = [w.id for w in chips if not _fully_visible(scr, w)]
        assert not clipped, f"{width} cols: chips clipped {clipped}"


# --------------------------------------------------------------------------- #
# LLR-001.2 — focus is the navigation model, so it must be visible
# --------------------------------------------------------------------------- #
FOCUS_MARKED = ("f-title", "f-project", "f-phase", "f-priority", "f-start",
                "cal-f-start", "f-due", "cal-f-due", "f-blocked", "f-archived",
                "f-pinned", "paste-img", "save", "cancel")


def _wears_bar(w) -> bool:
    kind, color = w.styles.border_left
    return kind not in ("", "none", "hidden") and color.hex.lower() == ACCENT


async def test_focus_mark_shows_on_every_one_row_control(tmp_path):
    """LLR-001.2 (UX-6). The one-row fields gave up the tall focus border that
    used to say where the cursor was; on a keyboard-first editor that border
    IS the navigation model. Its replacement is an accent bar on the left edge
    of whatever holds focus, on nothing else — read back from the style AND
    found painted on the focused control's row. (The notes / URLs / images
    TextAreas are multi-row and keep their tall focus border.) RED: drop the
    `:focus` rule -> no accent bar on the focused control."""
    app = _app(tmp_path)
    async with app.run_test(size=(120, 36)) as pilot:
        scr = await _open_editor_writing(app, pilot)
        for wid in FOCUS_MARKED:
            w = scr.query_one(f"#{wid}")
            w.focus()
            await pilot.pause()
            assert app.focused is w, f"{wid} did not take focus"
            assert _wears_bar(w), f"{wid}: focused but no accent bar"
            row = _painted(app)[w.region.y]
            x, bar = 0, False
            for seg in row:
                if x == w.region.x and seg.text.strip() and _hex(seg) == ACCENT:
                    bar = True
                x += cell_len(seg.text)   # cells, not codepoints: the 📅 is 2
            assert bar, f"{wid}: no accent mark painted at its left edge"
            others = [o for o in FOCUS_MARKED
                      if o != wid and _wears_bar(scr.query_one(f"#{o}"))]
            assert not others, f"{others} wear the focus bar while {wid} has focus"


# --------------------------------------------------------------------------- #
# AT-002 — the preview shows the note as the board paints it, and follows you
# --------------------------------------------------------------------------- #
def _preview_segments(app):
    """(text, hex colour) for every painted segment INSIDE the preview's
    on-screen region — what the reader actually sees there, not a markup
    string the widget was handed."""
    r = app.screen.query_one("#task-preview-scroll").content_region
    out = []
    for y, strip in enumerate(_painted(app)):
        if not (r.y <= y < r.y + r.height):
            continue
        x = 0
        for seg in strip:
            if seg.text.strip() and r.x <= x < r.x + r.width:
                out.append((seg.text, _hex(seg)))
            x += cell_len(seg.text)   # cells, not codepoints: the 📅 is 2
    return out


async def test_the_preview_paints_the_note_on_open(tmp_path):
    """AT-002, first limb (HLR-002, Q-3). US-001 says SEE what is already
    written: the preview must carry the note, highlighted, the moment the
    editor opens — not only after the first keystroke. The fixture's first
    `==portal de proveedores==` must be painted in the yellow (`soon`) the
    board uses, with the markers gone. RED: no initial render -> the preview
    is empty on open."""
    app = _app(tmp_path)
    async with app.run_test(size=(120, 36)) as pilot:
        await _open_editor(app, pilot)
        segs = _preview_segments(app)
        assert any("portal" in t and c == HEX["soon"] for t, c in segs), \
            f"the ==…== span is not painted yellow on open: {segs[:6]}"
        assert not any("==" in t for t, _c in segs), "markers shown raw"


async def test_the_preview_follows_the_typing_to_the_last_line(tmp_path):
    """AT-002, second limb (HLR-002, UX-4). Typing on the LAST line of a note
    longer than the preview: the new `!!…!!` span must appear in the preview,
    in the app's red (`over`), INSIDE the preview's visible rows — a preview
    parked at the top would show nothing of what you are writing at 80x24.
    RED: no change handler -> the typed text never reaches it; no scroll
    follow -> it is below the fold."""
    app = _app(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await _open_editor_writing(app, pilot)
        await pilot.press("enter")
        for ch in "!!ship it now!!":
            await pilot.press(ch)
        for _ in range(3):
            await pilot.pause()
        hit = [(t, c) for t, c in _preview_segments(app) if "ship it now" in t]
        assert hit, "typed text is not in the preview's visible rows"
        assert any(c == HEX["over"] for _t, c in hit), f"not red: {hit}"


async def test_the_preview_paints_markup_typed_in_a_note_as_text(tmp_path):
    """Security (family C, C-17: markup rendering over file-derived text). A note
    is user/file text, so a `[link=…]` or `[reverse]` typed into it must come out
    LITERALLY, never as a style or a hyperlink. Since batch 2026-10-02-batch-04
    (S1, LLR-401.3) the preview is built from `highlight_segments` as Text
    pieces and no parser reads the notes; this pins that. RED: render the raw
    notes as markup -> the brackets vanish into a style."""
    app = _app(tmp_path)
    async with app.run_test(size=(120, 36)) as pilot:
        scr = await _open_editor(app, pilot)
        scr.query_one("#f-notes", TextArea).text = \
            "[reverse]boom[/reverse] [link=https://evil.example]x[/link] ==[b]y[/b]=="
        for _ in range(3):
            await pilot.pause()
        text = "".join(t for t, _c in _preview_segments(app))
        assert "[reverse]boom[/reverse]" in text, text
        assert "[link=https://evil.example]x[/link]" in text, text
        assert "[b]y[/b]" in text, text


@pytest.mark.parametrize("note", ["[LINK=http://e]x", "[B]bold?", "[ red]x", "a[b"])
async def test_a_bracket_textual_would_parse_neither_crashes_nor_vanishes(tmp_path, note):
    """Security review S1 (2026-09-30): `rich.markup.escape` only escapes a `[`
    that RICH would read as a tag; Textual's own markup parser also reads
    uppercase and space-led brackets. Fed through `Static.update(str)`, a note
    holding `[LINK=…` raised MarkupError (the app died, unsaved edits lost —
    and notes also arrive by team sync), and `[B]x` silently vanished. The
    preview is built as a Rich `Text`, so Textual never parses the note. RED:
    hand the markup string to the Static -> MarkupError / text missing."""
    app = _app(tmp_path)
    async with app.run_test(size=(120, 36)) as pilot:
        scr = await _open_editor(app, pilot)
        scr.query_one("#f-notes", TextArea).text = note
        for _ in range(3):
            await pilot.pause()
        assert isinstance(app.screen, TaskModal), "the editor died"
        text = "".join(t for t, _c in _preview_segments(app))
        assert note in text, f"{note!r} not shown literally: {text!r}"


async def test_an_empty_note_previews_as_nothing(tmp_path):
    """Empty boundary: no notes -> an empty preview, not a placeholder that
    looks like content."""
    app = _app(tmp_path)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.pause()
        await pilot.press("a")
        for _ in range(3):
            await pilot.pause()
        assert _preview_segments(app) == []


# --------------------------------------------------------------------------- #
# AT-005 — keyboard: tab walks the editor, Save works from the keys, esc drops
# --------------------------------------------------------------------------- #
TAB_ORDER = ["f-title", "f-project", "f-phase", "f-priority", "f-start",
             "cal-f-start", "f-due", "cal-f-due", "f-blocked", "f-archived",
             "f-pinned", "f-notes", "f-urls", "f-images", "paste-img", "save",
             "cancel"]


@pytest.mark.parametrize("size", SIZES, ids=lambda s: f"{s[0]}x{s[1]}")
async def test_tab_walks_the_editor_and_save_works_from_the_keys(tmp_path, size):
    """AT-005 (HLR-001, UX-1/UX-2). Focus is this app's navigation model, so
    the order tab visits things is part of the design: title, the chips left
    to right (row by row when wrapped), the notes, the footer, Save, Cancel —
    and never the preview, which is read-only. Visible is not operable: the
    walk then lands on Save and ENTER saves. RED: a focusable preview (a
    VerticalScroll focuses by default) inserts a stop after the notes."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        scr = await _open_editor_writing(app, pilot)
        scr.query_one("#f-title").focus()
        await pilot.pause()
        seen = [app.focused.id]
        for _ in range(len(TAB_ORDER) - 1):
            await pilot.press("tab")
            await pilot.pause()
            seen.append(app.focused.id)
        assert seen == TAB_ORDER
        await pilot.press("shift+tab")
        await pilot.pause()
        assert app.focused.id == "save"
        scr.query_one("#f-title", Input).value = "Saved from the keys"
        await pilot.press("enter")
        await pilot.pause()
        assert not isinstance(app.screen, TaskModal), "enter on Save did not save"
        assert app.board.tasks[0].title == "Saved from the keys"


async def test_escape_discards_an_edited_task(tmp_path):
    """The other half of AT-005: esc closes WITHOUT saving, even when dirty."""
    app = _app(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        scr = await _open_editor_writing(app, pilot)
        scr.query_one("#f-title", Input).value = "should not stick"
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
        assert app.board.tasks[0].title == "Migrar portal de proveedores (fase 2)"


@pytest.mark.parametrize("size", SIZES, ids=lambda s: f"{s[0]}x{s[1]}")
async def test_the_editor_paints_its_keys_in_full(tmp_path, size):
    """UX-3: this app does not ship keys off-screen. ctrl+e (emoji), ctrl+v
    (paste) and esc must be PAINTED, whole, at both sizes — and the
    `.modal-title` still names ctrl+e (the emoji tests read it there)."""
    app = _app(tmp_path)
    async with app.run_test(size=size) as pilot:
        scr = await _open_editor_writing(app, pilot)
        assert "ctrl+e" in str(scr.query_one(".modal-title").content)
        painted = "\n".join(s.text for s in _painted(app))
        for key in ("ctrl+e emoji", "ctrl+v paste", "esc cancel"):
            assert key in painted, f"{size}: {key!r} is not painted"


# --------------------------------------------------------------------------- #
# LLR-001.3 — the save contract did not move with the widgets
# --------------------------------------------------------------------------- #
async def test_save_payload_round_trips_every_field(tmp_path):
    """The editor was rebuilt widget by widget; the dict `_save` hands the app
    is a contract with `_on_task_edited`. Change EVERY field away from its
    current value (C-10: a default that merely survives proves nothing), save
    through the button, and read the task back. Preservation test: GREEN on
    the base tree by design; RED under the mutation "drop a key from the
    payload" -> that field keeps its old value."""
    app = _app(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        scr = await _open_editor_writing(app, pilot)
        task = app.board.tasks[0]
        scr.query_one("#f-title", Input).value = "Renamed"
        scr.query_one("#f-project", Select).value = "__none__"
        scr.query_one("#f-phase", Select).value = "Backlog"
        scr.query_one("#f-priority", Select).value = "low"
        scr.query_one("#f-start", Input).value = "2026-09-01"
        scr.query_one("#f-due", Input).value = "2026-12-24"
        for flag in ("f-blocked", "f-archived", "f-pinned"):
            cb = scr.query_one(f"#{flag}", Checkbox)
            cb.value = not cb.value
        scr.query_one("#f-notes", TextArea).text = "short note"
        scr.query_one("#f-urls", TextArea).text = "https://a.example\nnot a url"
        scr.query_one("#f-images", TextArea).text = "img/one.png"
        await pilot.pause()
        scr.query_one("#save").press()
        await pilot.pause()
        assert not isinstance(app.screen, TaskModal)
        assert (task.title, task.project_id, task.phase, task.priority) == \
            ("Renamed", None, "Backlog", "low")
        assert (task.start_date, task.due_date) == ("2026-09-01", "2026-12-24")
        assert (task.blocked, task.archived, task.pinned) == (True, True, True)
        assert task.notes == "short note"
        assert task.urls == ["https://a.example"]
        assert task.images == ["img/one.png"]


# --------------------------------------------------------------------------- #
# LLR-001.4 — the project editor is not in scope and must not move
# --------------------------------------------------------------------------- #
async def test_project_modal_keeps_its_box(tmp_path):
    """The task editor's full-screen rules are scoped to the task editor. The
    project editor shares `#modal-box` / `.modal`; if the new rules leaked
    onto those it would silently become full screen too. Preservation test:
    GREEN on base; RED under the mutation "write the rules against
    `#modal-box`" -> this box is no longer 62 wide."""
    app = _app(tmp_path)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.pause()
        await pilot.press("p")
        await pilot.pause()
        box = app.screen.query_one("#modal-box")
        assert box.outer_size.width == 62, f"ProjectModal box is {box.outer_size.width} wide"

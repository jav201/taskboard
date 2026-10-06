"""The colour budget, app-wide (round 7, `variants_polish.BUDGET`).

Batch 2026-10-02-batch-02 · HLR-201, HLR-202, HLR-203 · AT-201, AT-202, AT-203 ·
TC-201, TC-202, TC-203, TC-204, TC-205, TC-213.

Field report (the operator, answers D10 / SOON / PKT, 2026-10-02): batch-01 took
the accent off the kanban and the gantt only, so the other seven views still
branded their titles, chips and spines teal — "hacer el pase global". The law:
the accent paints a FOCUS ROLE only — today's marks, the field being edited, a
list's cursor — and every view title is bold bright. Soon-due tokens go back to
amber; the moving gantt packet goes quiet so it is not read as the critical chain.

Every census is over RENDERED spans, over a set DERIVED from the code (the
views, and the presentation tuples parsed out of `app.py`), and first proves it
can see the accent at all.
"""
from __future__ import annotations

import ast
from datetime import date, timedelta
from pathlib import Path

import pytest
from rich.text import Text

import kg_board
from kg_board import TODAY
from taskboard import app as app_mod
from taskboard import models, views
from taskboard.app import VIEW_KEYS, VIEW_ORDER, TaskboardApp
from taskboard.views import HEX, RULE_PHASES, render_view, reldue_token

ACCENT = HEX["accent"].lower()
ACCENT_RGB = "rgb({},{},{})".format(*(int(ACCENT[i:i + 2], 16) for i in (1, 3, 5)))
RULES = set(RULE_PHASES) | {"┃"}
SIZES = ((118, 30), (80, 24), (40, 14))


def presentations() -> dict[str, tuple[str, ...]]:
    """The presentation tuples `action_toggle_presentation` cycles, read out of
    `app.py` itself so a new presentation joins the census without a test edit
    (C-31: the input set is derived, never hand-listed)."""
    tree = ast.parse(Path(app_mod.__file__).read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "action_toggle_presentation")
    out = {}
    for branch in ast.walk(fn):
        if (isinstance(branch, ast.If) and isinstance(branch.test, ast.Compare)
                and isinstance(branch.test.comparators[0], ast.Constant)):
            view = branch.test.comparators[0].value
            for st in branch.body:
                if (isinstance(st, ast.Assign) and isinstance(st.value, ast.Tuple)
                        and getattr(st.targets[0], "id", "") == "modes"):
                    out[view] = tuple(e.value for e in st.value.elts)
    return out


KW = {"swimlanes": "lanes_presentation", "kanban": "presentation",
      "focus": "focus_presentation"}


def pairs() -> list[tuple[str, dict]]:
    pres = presentations()
    out = []
    for view in VIEW_ORDER:
        if view in pres:
            out += [(view, {KW[view]: p}) for p in pres[view]]
        else:
            out.append((view, {}))
    return out


def test_TC_202_the_census_set_is_complete():
    """Guard for the census input set (qa P2 Q-7): 9 views, 2 + 3 + 5 of them
    presentations — 16 pairs. Losing one (a parse that misses a branch, a view
    dropped from VIEW_ORDER) turns this RED before the census can go quiet."""
    ps = pairs()
    assert len(VIEW_ORDER) == 9 and len(ps) == 16, ps
    assert {v for v, _ in ps} == set(VIEW_ORDER)


def render(mode, kw, b, st, setup, w, h, **extra):
    more = {"team_state": st} if mode in ("standup", "people") else {}
    if mode == "setup":
        more = {"setup_state": setup, "team_state": st}
    return render_view(mode, b, False, "tw3", TODAY, w, h, {}, **kw, **more, **extra)


def accent_cells(text: Text) -> list[tuple[int, int, str]]:
    """(row, column, painted text) of every run whose style carries the accent."""
    plain = text.plain
    starts = [0]
    for line in plain.split("\n"):
        starts.append(starts[-1] + len(line) + 1)
    out = []
    for s in text.spans:
        st = str(s.style).lower().replace(" ", "")
        if ACCENT in st or ACCENT_RGB in st:
            row = max(i for i, x in enumerate(starts) if x <= s.start)
            out.append((row, s.start - starts[row], plain[s.start:s.end]))
    return out


def off_role(mode: str, kw: dict, text: Text, due_today: int) -> list:
    """The accent runs that are NOT a focus role (§1.3). By POSITION where a
    role has one (qa P2 Q-9): every rule glyph of a view stands in ONE column —
    the today column — except the lanes grid, whose panels each carry a bar and
    a rail column (two per panel column, at most four); a today stud or rail
    (`▄`, `▪`) at most once per task due today; ONE cursor mark (the list's
    `▸`/`>`). The filter field is checked by the gantt/kanban census of batch-01.
    LIMIT (code review F5): every census render carries a selection; the
    gantt's no-selection `today …` label is a run this whitelist would not
    accept, so selection-less renders are left to batch-01's gantt census."""
    bad, rule_cols, studs, cursors = [], set(), {"▄": 0, "▪": 0}, 0
    for row, col, seg in accent_cells(text):
        s = seg.strip()
        if s and set(s) <= RULES:
            rule_cols.add(col)
        elif s in ("today", f"{TODAY:%b} {TODAY.day}") or (mode == "gantt" and s == str(TODAY.day)):
            pass
        elif s in studs:
            studs[s] += 1
        elif s in ("▸", ">"):
            cursors += 1
        else:
            bad.append((row, col, seg))
    if cursors > 1:
        bad.append(("cursor marks", cursors))
    limit = 4 if kw.get("lanes_presentation") == "grid" else 1
    if len(rule_cols) > limit:
        bad.append(("rule columns", sorted(rule_cols)))
    for g, n in studs.items():
        if n > due_today:
            bad.append((g, n))
    return bad


def due_today(b) -> int:
    return sum(1 for t in b.tasks if t.due_date == TODAY.isoformat() and not b.is_done(t))


# =========================================================================== #
# TC-201 — every title bold bright
# =========================================================================== #
TITLES = {"swimlanes": "TASKBOARD", "agenda": "AGENDA", "gantt": "GANTT", "kanban": "KANBAN",
          "focus": "FOCUS", "flow": "FLOW", "standup": "STANDUP", "people": "PEOPLE",
          "setup": "SETUP"}


@pytest.mark.parametrize("w,h", [(118, 30), (24, 10)])
def test_TC_201_every_view_title_is_bold_bright(tmp_path, w, h):
    """TC-201 (LLR-201.1). Every view × presentation draws its title bold
    `bright`, the clipped title of a 24-cell panel included. RED on the base
    tree: lanes, agenda, focus, flow, standup and people titles are accent."""
    b, st, setup = kg_board.census(tmp_path)
    for mode, kw in pairs():
        text = render(mode, kw, b, st, setup, w, h)
        word = TITLES[mode]
        line0 = text.plain.split("\n")[0]
        probe = word if word in line0 else word[:max(1, w - 4)].split()[0][:3]
        at = text.plain.index(probe)
        styles = " ".join(str(s.style).lower() for s in text.spans if s.start <= at < s.end)
        assert HEX["bright"].lower() in styles and "bold" in styles, (mode, kw, w, styles)
        assert ACCENT not in styles, (mode, kw, w)


# =========================================================================== #
# TC-202 — the census over every view × presentation × size
# =========================================================================== #
def test_TC_202_every_accent_run_is_a_focus_role(tmp_path):
    """TC-202 (LLR-201.2, HLR-201). 16 pairs × 3 sizes on the census board:
    every accent run is a focus role. RED on the base tree: the agenda's `◐`,
    the lanes grid's `↗`, the flow throughput bar, the operator spine, the team
    filter's active segment, Setup's section names and hint keys."""
    b, st, setup = kg_board.census(tmp_path)
    reached = set()
    for w, h in SIZES:
        for mode, kw in pairs():
            text = render(mode, kw, b, st, setup, w, h)
            reached.add((mode, tuple(kw.items()), w))
            assert not off_role(mode, kw, text, due_today(b)), (mode, kw, w, off_role(
                mode, kw, text, due_today(b))[:5])
    assert len(reached) == 16 * len(SIZES)


def test_TC_202_the_census_can_see_the_accent(tmp_path):
    """Non-vacuity, and the positional rule can fail: the detector finds today's
    rule on the lanes, the filter field on a filtered kanban, and Setup's `>`
    cursor; an accent `╎` painted OFF the today column is reported."""
    b, st, setup = kg_board.census(tmp_path)
    lanes = render("swimlanes", {"lanes_presentation": "waves"}, b, st, setup, 118, 30)
    assert any(set(s.strip()) <= RULES and s.strip() for _r, _c, s in accent_cells(lanes))
    filt = render("kanban", {}, b, st, setup, 118, 30, search_query="API")
    assert any(r in (1, 2) for r, _c, _s in accent_cells(filt))
    setup_t = render("setup", {}, b, st, setup, 118, 30)
    assert any(s.strip() == ">" for _r, _c, s in accent_cells(setup_t)), "Setup's cursor"
    # the mutation arm: a second accent rule column must be caught
    forged = lanes.copy()
    forged.append(Text("\n" + "╎", style=HEX["accent"]))
    assert off_role("swimlanes", {"lanes_presentation": "waves"}, forged, due_today(b))


def test_TC_202_the_legend_swatches_follow_their_marks(tmp_path):
    """Each legend swatch wears its mark's tone: the operator row/lane spine
    `bright`, the throughput bar `hd`; only today's swatches keep the accent."""
    b, st, _setup = kg_board.census(tmp_path)
    for mode in VIEW_ORDER:
        for swatch, meaning in views.legend_entries(mode, b, TODAY, 118, 30, team_state=st,
                                                    selected_id="tw3"):
            if ACCENT in swatch.lower():
                assert "today" in meaning, (mode, meaning)
    ents = dict((m, s) for s, m in views.legend_entries("standup", b, TODAY, 118, 30,
                                                        team_state=st))
    assert HEX["bright"] in ents["operator row"]
    flow = dict((m, s) for s, m in views.legend_entries("flow", b, TODAY, 118, 30))
    assert HEX["hd"] in flow["throughput: tasks reaching the terminal phase"]


# =========================================================================== #
# TC-213 — Setup's rows keep their styles
# =========================================================================== #
# The plain rows, frozen (P-13: the columns must not move; only the styles return).
# Read off the base tree's columns with increment 003's English words (HLR-204).
SETUP_ROWS_BASE = [
    "  team mode               on   off                      !    team.json missing or invalid",
    "> shared folder          ▌D:/team-never-there           !    does not exist",
    "    reach                                               !    no folder",
    "  sync every              - 30 + min                    !    no sync yet",
]


def setup_rows(text: Text) -> list[Text]:
    return text.split("\n")[5:9]


def styled_columns(row: Text) -> bool:
    """A span on the label, control or check column (cells 0..58), not only
    the dim note after them — the base rows carried that one (code review F2)."""
    return any(s.start < 59 for s in row.spans)


@pytest.mark.parametrize("enabled", [True, False])
def test_TC_213_setup_rows_keep_their_styles(tmp_path, enabled):
    """TC-213 (LLR-201.3). Every Setup body row carries its styles: the cursor
    `>` in accent, the chosen chip bold `bright` against `mut`, the check marks
    in their tones — with the plain text exactly the base's. RED on the base
    tree: the rows were built from `str()` of styled Text, so the label,
    control and check columns carried no span (P-13)."""
    b, st, setup = kg_board.census(tmp_path)
    setup["enabled"] = enabled
    text = render("setup", {}, b, st, setup, 118, 30)
    rows = setup_rows(text)
    assert [r.plain.rstrip() for r in rows] == SETUP_ROWS_BASE
    for r in rows:
        assert styled_columns(r), r.plain
    mode_row = rows[0]

    def style_at(word):
        at = mode_row.plain.index(word)
        return " ".join(str(s.style).lower() for s in mode_row.spans if s.start <= at < s.end)
    chosen, other = (" on", "off") if enabled else ("off", " on")
    assert "bold" in style_at(chosen.strip()) and HEX["bright"] in style_at(chosen.strip())
    assert HEX["mut"] in style_at(other.strip()) and "bold" not in style_at(other.strip())
    cursor = rows[1]
    assert any(cursor.plain[s.start:s.end].startswith(">") and ACCENT in str(s.style).lower()
               for s in cursor.spans)


@pytest.mark.parametrize("section,row", [(0, 1), (0, 4), (1, 0), (2, 0)])
def test_TC_213_the_cursor_is_painted_on_every_section(tmp_path, section, row):
    """The `>` cursor is the list's focus: wherever it stands — the team
    rows, a project row, a roster row — it is painted in accent, and every
    body row keeps a styled column (code review F3)."""
    b, st, setup = kg_board.census(tmp_path)
    setup.update(cursor_section=section, cursor_row=row)
    text = render("setup", {}, b, st, setup, 118, 30)
    lines = text.split("\n")
    marked = [ln for ln in lines if ln.plain.startswith("> ")]
    assert len(marked) == 1
    assert ACCENT in " ".join(str(s.style).lower() for s in marked[0].spans if s.start == 0)
    body = [ln for ln in lines[4:] if ln.plain.startswith(("  ", "> ")) and len(ln.plain) > 30]
    assert len(body) >= 7
    for ln in body:
        assert styled_columns(ln), ln.plain


def test_TC_213_a_long_value_is_cut_to_its_column_with_its_style(tmp_path):
    """A shared folder longer than the 30-cell control column is cut with `…`
    in its last cell, the check column stays at cell 56, and the cut text
    keeps its style (the truncation branch of `_fit_text`, code review F1)."""
    b, st, setup = kg_board.census(tmp_path)
    setup["shared_dir"] = "D:/" + "x" * 40
    setup["projects"][0]["name"] = "P" * 30
    text = render("setup", {}, b, st, setup, 118, 30)
    row = next(ln for ln in text.split("\n") if "D:/x" in ln.plain)
    assert row.plain[25:55].endswith("…") and len(row.plain[25:55]) == 30, row.plain
    assert row.plain[55] == " " and row.plain[56] in "!✓", row.plain
    spine = [s for s in row.spans if row.plain[s.start:s.end] == "▌"]
    assert spine and HEX["mut"] in str(spine[0].style)
    proj = next(ln for ln in text.split("\n") if "PPPP" in ln.plain)
    assert proj.plain[:24].endswith("…") and styled_columns(proj)


def test_TC_213_a_passing_check_is_done_not_accent(tmp_path):
    """The passing check `✓` wears `done` (a verdict, not a focus)."""
    b, st, setup = kg_board.census(tmp_path)
    setup["shared_dir"] = str(tmp_path / "team")
    text = render("setup", {}, b, st, setup, 118, 30)
    ticks = [s for s in text.spans if text.plain[s.start:s.end].strip() == "✓"]
    assert ticks and all(HEX["done"] in str(s.style) for s in ticks)


@pytest.mark.parametrize("bad", ["not a colour", ["not", "a string"]])
async def test_TC_213_a_bad_project_colour_does_not_crash_setup(tmp_path, bad):
    """A colour `team.json` spells wrong is drawn `mut` instead of reaching
    Textual as a style (code review F9): Textual raises on an unknown colour
    when it PAINTS, so the Setup render is painted in a Static here, as the
    board panel paints it. RED before the fix: `MissingStyle`."""
    from textual.app import App
    from textual.widgets import Static

    b, st, setup = kg_board.census(tmp_path)
    setup["projects"][0]["color"] = bad    # a bad string, or not a str (security L2)
    text = render("setup", {}, b, st, setup, 118, 30)

    class _Paint(App):
        def compose(self):
            yield Static(text, id="s")

    app = _Paint()
    async with app.run_test(size=(120, 32)) as pilot:
        await pilot.pause()
        assert "Website Redesign" in app.query_one("#s").render().plain


# =========================================================================== #
# TC-205 — soon in amber; the packet quiet
# =========================================================================== #
def test_TC_205_the_relative_due_token_is_amber_within_a_week():
    """TC-205 (LLR-203.1). +1..+7 days → `soon`; +8 → `dim`; today `soon`
    (unchanged); late `over`. RED on the base tree: +4d was `mut` (P-8)."""
    b = kg_board.build()
    t = b.task_by_id("tw6")
    expect = {1: "soon", 4: "soon", 7: "soon", 8: "dim", 0: "soon", -1: "over"}
    for d, tone in expect.items():
        t.due_date = (TODAY + timedelta(days=d)).isoformat()
        assert reldue_token(t, TODAY, b)[1] == tone, (d, reldue_token(t, TODAY, b))


def test_TC_205_the_packet_is_quiet(tmp_path):
    """The flow packet `▬` is `mut`, never the chain's `bright`, at every tick
    0..7 (≥ 12 packets seen in all — the guard that the arm is not empty).
    RED on the base tree: `#e6edf7` (P-8)."""
    b = kg_board.build()
    seen = 0
    for tick in range(8):
        text = render_view("gantt", b, False, "tw3", TODAY, 118, 30, {}, tick=tick)
        for s in text.spans:
            if text.plain[s.start:s.end] == "▬":
                seen += 1
                assert HEX["mut"] in str(s.style) and HEX["bright"] not in str(s.style)
    assert seen >= 12


# =========================================================================== #
# AT-201 / AT-203 — through the running app (US-201)
# =========================================================================== #
class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    for mod in (views, app_mod, models):
        monkeypatch.setattr(mod, "date", _Today)


def _team_app(tmp_path):
    b, _st, _setup = kg_board.census(tmp_path)
    b.settings["team_shared_dir"] = str(tmp_path / "team")
    b.settings["team_user_id"] = "jav"
    b.save()
    return b, TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)


def painted(app) -> Text:
    return app.query_one("#board").render()


async def test_AT_201_every_view_paints_the_accent_only_for_focus(tmp_path, frozen):
    """AT-201 (HLR-201). The running app in team mode at 118×30: every view key,
    and `tab` through every presentation of lanes, kanban and focus — each
    painted board carries accent only on focus roles, and Setup's chosen chip
    reads bold bright. RED on the base tree: lanes `◆ TASKBOARD`, the agenda's
    `◐`, the standup spine and Setup's hint keys are accent."""
    b, app = _team_app(tmp_path)
    pres = presentations()
    keys = {v: k for k, v in VIEW_KEYS.items()}
    seen = set()
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        assert app.team_state is not None, "team mode is on"
        for view in VIEW_ORDER:
            await pilot.press(keys[view])
            await pilot.pause()
            for _ in range(len(pres.get(view, ("one",)))):
                kw = {KW[view]: {"swimlanes": app.lanes_presentation, "kanban":
                                 app.kanban_presentation, "focus": app.focus_presentation}[view]
                      } if view in KW else {}
                seen.add((view, tuple(kw.items())))
                text = painted(app)
                assert not off_role(view, kw, text, due_today(app.board)), (view, kw)
                if view in pres:
                    await pilot.press("tab")
                    await pilot.pause()
        assert len(seen) == 16, seen
        await pilot.press("0")
        await pilot.pause()
        setup_line = next(ln for ln in painted(app).split("\n") if " on " in ln.plain)
        at = setup_line.plain.index(" on ") + 1
        st = " ".join(str(s.style).lower() for s in setup_line.spans if s.start <= at < s.end)
        assert "bold" in st and (HEX["bright"] in st or "rgb(230,237,247)" in st), st


async def test_AT_203_soon_is_amber_and_the_packet_quiet(tmp_path, frozen):
    """AT-203 (HLR-203). Key `4`: every `+1d`..`+7d` the kanban paints is amber
    (at least one); key `3`: every painted `▬` is `mut`. RED on the base tree:
    the tokens are `mut` and the packet `bright`."""
    b = kg_board.build(tmp_path / "board.json")
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("4")
        await pilot.pause()
        text = painted(app)
        toks = [s for s in text.spans
                if text.plain[s.start:s.end].strip() in {f"+{n}d" for n in range(1, 8)}]
        assert toks
        for s in toks:
            assert HEX["soon"] in str(s.style).lower() or "rgb(251,191,36)" in str(s.style).lower()
        await pilot.press("3")
        await pilot.pause()
        text = painted(app)
        packets = [s for s in text.spans if text.plain[s.start:s.end] == "▬"]
        assert packets
        for s in packets:
            st = str(s.style).lower()
            assert HEX["bright"] not in st and "rgb(230,237,247)" not in st, st


# =========================================================================== #
# TC-203 / TC-204 / AT-202 — the chrome (HLR-202, increment 002)
# =========================================================================== #
import re  # noqa: E402

from rich.markup import render as render_markup  # noqa: E402

from taskboard.keymap import fit_bar, key_bar_plain, render_key_bar  # noqa: E402

HEXES = re.compile(r"#[0-9a-fA-F]{6}")
KEY_HEXES = {HEX["bright"], HEX["mut"], HEX["dim"]}

# The base strings, frozen (qa P2 Q-12): the words must not move, only the tones.
KEYBAR_BASE = {   # read off the base tree a0e7d9a (`key_bar_plain`), not typed
    ("gantt", 80, "primary"):
        # batch 2026-10-04-batch-01 added `L` (Link) to the primary layer: the
        # bar sheds one more word ("Agenda") and keeps every key
        "? Map  ; More  q Quit  1 Lanes  2  3  4  5  7  8  9  0  ↵  a  e  d  L  ↓  ↑",
    ("gantt", 118, "more"):
        # batch 2026-10-04-batch-02 added `M` (Milestone) to the more layer: the
        # bar sheds one more word ("More") and keeps every key
        "? Map  ;  q  1  2  3  4  5  7  8  9  0  ↵  a  e  d  L  x  X  v  u  t  T  M  [  ]  !  b"
        "  +  -  F  esc  /  ↓  ↑  ←  →",
}


def test_TC_203_the_key_bar_wears_bright_keys_and_muted_words():
    """TC-203 (LLR-202.1). Every view × both layers × widths 24..160: the bar's
    hexes are only bright (keys, bold), mut (words) and dim (the overflow note);
    every key shown is bold bright; the markup paints exactly the plain bar.
    RED on the base tree: accent keys (primary), eight group hues (more)."""
    from taskboard.app import VIEW_ORDER as views_
    checked = 0
    for view in views_:
        for layer in ("primary", "more"):
            for width in (24, 60, 80, 118, 160):
                markup = render_key_bar(width, view, layer)
                assert set(h.lower() for h in HEXES.findall(markup)) <= KEY_HEXES, (view, layer, width)
                text = render_markup(markup)
                assert text.plain == key_bar_plain(width, view, layer)
                at = 0
                for show, label in fit_bar(width, view, layer)[0]:   # each key's own cell
                    st = " ".join(str(sp.style) for sp in text.spans if sp.start <= at < sp.end)
                    assert "bold" in st and HEX["bright"] in st, (view, layer, width, show, st)
                    at += len(f"{show} {label}".strip()) + 2
                checked += 1
    assert checked == 9 * 2 * 5
    for (view, width, layer), plain in KEYBAR_BASE.items():
        assert key_bar_plain(width, view, layer) == plain


def test_TC_204_the_ribbon_has_no_accent():
    """TC-204 (LLR-202.2). The local time is bold bright, each city's name mut
    and its time hd; no accent. RED on the base tree: three accent clocks."""
    from datetime import datetime

    from taskboard.ribbon import Ribbon

    class _Probe(Ribbon):
        def update(self, renderable="", **kw):
            return None

    markup = _Probe().update_clock(datetime(2026, 9, 30, 9, 5, 7))
    assert ACCENT not in markup.lower()
    assert f"[b {HEX['bright']}]09:05:07[/]" in markup
    assert len(re.findall(rf"\[{HEX['hd']}\]\d\d:\d\d\[/\]", markup)) == 2
    assert markup.count(f"[{HEX['mut']}]") >= 3          # the week and two city names


def test_TC_204_modal_titles_and_the_key_map_are_bright():
    """TC-204 (LLR-202.2). `.modal-title` is bright (bold) in the stylesheet;
    the focused input borders keep the accent (the field being edited); the
    help key map writes no accent. RED on the base tree: `.modal-title` and
    the key map's keys are `#2dd4bf`."""
    from taskboard import app as app_module
    css = Path(app_module.__file__).with_name("taskboard.tcss").read_text(encoding="utf-8")
    block = css[css.index(".modal-title {"):].split("}")[0]
    assert "color: #e6edf7" in block and "bold" in block
    for focus_rule in (".modal Input:focus", "#proj-list:focus"):
        rule = css[css.index(focus_rule):].split("}")[0]
        assert ACCENT in rule.lower(), focus_rule
    from taskboard.modals import CommandPalette           # the palette's own field (F4)
    palette = CommandPalette.DEFAULT_CSS
    assert ACCENT in palette[palette.index("#palette-input:focus"):].split("}")[0].lower()
    src = Path(app_module.__file__).read_text(encoding="utf-8")
    help_src = src[src.index("class HelpScreen"):src.index("class TaskboardApp")]
    assert ACCENT not in help_src.lower()


async def test_AT_202_the_chrome_spends_no_accent(tmp_path, frozen):
    """AT-202 (HLR-202). The running app at 118×30: the key bar and the ribbon
    paint no accent, in both bar layers; `?` paints its title and headings
    bright; `m` paints the key map without accent; the `/` prompt's focused
    input keeps the accent border. RED on the base tree: accent keys, accent
    clocks, accent titles."""
    b = kg_board.build(tmp_path / "board.json")
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)

    def accents(widget) -> int:
        content = widget.render()
        return sum(1 for sp in content.spans
                   if ACCENT in str(sp.style).lower() or ACCENT_RGB in str(sp.style).lower())

    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        await pilot.press("3")
        await pilot.pause()
        seen = []
        for layer in ("primary", "more"):
            bar = app.query_one("#keybar")
            assert bar.bar_layer == layer        # the layer really is the one checked (F1)
            seen.append(bar.render().plain)
            assert seen[-1].strip()
            assert accents(bar) == 0
            assert accents(app.query_one("#ribbon")) == 0
            await pilot.press("semicolon")
            await pilot.pause()
        assert seen[0] != seen[1]
        await pilot.press("question_mark")
        await pilot.pause()
        titles = list(app.screen.query(".modal-title"))
        assert len(titles) >= 3
        for t in titles:
            assert t.styles.color.hex.lower() == HEX["bright"], (str(t.render()), t.styles.color)
            assert t.styles.text_style.bold                        # F5
        await pilot.press("m")
        await pilot.pause()
        keymap_text = "".join(str(w.render()) for w in app.screen.query("Static"))
        assert "KEYS" in keymap_text
        for w in app.screen.query("Static"):
            assert accents(w) == 0
        # the key map paints its heading and every key bold bright (F2)
        kmap = next(w for w in app.screen.query("Static") if "KEYS" in w.render().plain)
        content = kmap.render()
        styles = [str(sp.style).lower().replace(" ", "") for sp in content.spans]
        bright_b = f"b{HEX['bright']}"
        assert set(styles) <= {bright_b, HEX["mut"], "#c8d3de"}, set(styles)
        keys_at = content.plain.index("KEYS")
        assert [st for sp, st in zip(content.spans, styles)
                if sp.start <= keys_at < sp.end] == [bright_b]
        assert styles.count(bright_b) >= 10                       # the heading + the keys
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        await pilot.press("slash")
        await pilot.pause()
        field = app.screen.query_one("Input")
        assert field.has_focus
        assert field.styles.border_top[1].hex.lower() == ACCENT

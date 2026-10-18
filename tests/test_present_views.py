"""Present v3, renderer level (batch 2026-10-18-batch-01, increment 001).

HLR-1801 / LLR-1801.1, LLR-1801.2, LLR-1801.3 · HLR-1802 / LLR-1802.1 ·
TC-1801 .. TC-1807.

Why these tests exist: in a meeting the operator wants the room to read what
each task SAYS, not only when it falls — «si las demás tareas tienen texto, me
gustaría que todas se vieran al mismo tiempo». So the split view must show text
from EVERY shown open task that has notes at once (TC-1804), say so whenever it
had to cut one (a hidden cut would let the presenter think the room read the
whole note), and keep a note's own structure — line breaks, bullets, numbered
steps — because a go-live plan read as one run-on line ("Sep 22. 1. Feature-flag
…") is the defect the operator named in the gantt view (TC-1801, TC-1807).

The oracle frames are `.dev-flow/2026-10-18-batch-01/evidence/frames/PRES-V3-*`,
written by that folder's `gen_frames.py` and cross-checked there row for row
against the approved prototype's own renderer (`prototypes/present_views/
views_d.py`, D2 · stacked). Synthetic boards only (`present_board.py`,
`present_notes_board.py`).

RED on the base tree: `render_present` takes no `view`, `present_note_lines` /
`present_alloc` do not exist, and the gantt view flattens a note's line breaks.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

import present_board as pb
import present_notes_board as nb
from taskboard import views

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / ".dev-flow" / "2026-10-18-batch-01" / "evidence" / "frames"


def _frame(name: str) -> list[str]:
    return (FRAMES / name).read_text(encoding="utf-8").splitlines()


def _rows(b, cursor, w, h, view="split", scroll=0) -> list[str]:
    return views.render_present(b, pb.PROJECT_ID, cursor, pb.TODAY, w, h, view,
                                scroll).plain.split("\n")


def _shown_open_with_notes(b) -> list:
    """From the RULE, not from the renderer: the project's visible tasks that are
    open, shown in the presentation and carry note text."""
    return [t for t in b.visible_tasks(False)
            if t.project_id == pb.PROJECT_ID and not b.is_done(t) and t.show_in_present
            and (t.notes or "").strip()]


def _first_words(notes: str) -> str:
    """The first words of a note's first non-blank line, item marker dropped —
    what any visible row of that note must begin with."""
    line = next(ln.strip() for ln in notes.splitlines() if ln.strip())
    line = re.sub(r"^(- |\* |• |\d+\. )", "", line)
    return line[:14]


# --------------------------------------------------------------------------- #
# TC-1801 — a note keeps its structure (LLR-1801.1)
# --------------------------------------------------------------------------- #
def test_TC_1801_line_breaks_bullets_and_numbers_are_kept():
    """TC-1801 (LLR-1801.1): every line break starts a new row; `- ` / `* ` /
    `• ` become `• `; `1. ` and `12. ` keep their number; an item's wrapped
    rows hang under its text; a run of blank lines is one blank row; leading
    and trailing blank lines and an empty note give nothing."""
    notes = ("First line.\n- a dash item\n* a star item\n• a dot item\n\n\n"
             "1. step one\n12. step twelve that is long enough to wrap twice here\nLast.")
    got = views.present_note_lines(notes, 24)
    assert got == [
        ("", "First line."),
        ("• ", "a dash item"),
        ("• ", "a star item"),
        ("• ", "a dot item"),
        ("", ""),
        ("1. ", "step one"),
        ("12. ", "step twelve that is"),
        ("    ", "long enough to wrap"),
        ("    ", "twice here"),
        ("", "Last."),
    ], got
    assert views.present_note_lines("\n\n  \n", 40) == []
    assert views.present_note_lines("", 40) == []
    assert views.present_note_lines(None, 40) == []
    for lead, txt in views.present_note_lines(nb.NOTES[nb.LONG], 30):
        assert views.vis(lead + txt) <= 30, (lead, txt)
    # wide glyphs (code-review F1): rows fit the CELLS, and no glyph is lost
    wide = "発表の前に全部のメモを確認する 🚀🚀 ok\n- 項目ひとつめ、とても長い説明がここに続きます"
    rows = views.present_note_lines(wide, 20)
    for lead, txt in rows:
        assert views.vis(lead + txt) <= 20, (lead, txt, views.vis(lead + txt))
    flat = "".join(txt for _, txt in rows).replace(" ", "")
    assert flat == wide.replace("\n- ", "").replace(" ", ""), flat
    i = [lead for lead, _ in rows].index("• ")
    assert i > 0 and all(lead == "  " for lead, _ in rows[i + 1:]), rows


# --------------------------------------------------------------------------- #
# TC-1802 — the fair share (LLR-1801.2)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("ns, cur, room, want", [
    ([5, 6, 3, 13, 0], 1, 40, [5, 6, 3, 13, 0]),   # everything fits -> everything
    ([5, 6, 3, 13, 0], 3, 14, [2, 2, 2, 8, 0]),    # cursor first: half, then surplus
    ([5, 6, 3, 13, 0], 1, 9, [1, 4, 2, 2, 0]),     # the largest other gives way first
    ([5, 6, 3, 13, 0], -1, 9, [3, 2, 2, 2, 0]),    # no cursor here: round-robin
    ([0, 0, 0], 0, 1, [0, 0, 0]),                  # no notes -> no rows
    ([4, 4, 4], 0, 3, [1, 1, 1]),                  # one row each when that is all
    ([5, 6, 3, 13, 0], 4, 9, [3, 2, 2, 2, 0]),     # the cursor on the task with no notes
    ([5, 6, 3, 13, 0], 0, 3, [1, 1, 1, 1, 0]),     # below a row per note: the cursor keeps 1
    ([5, 6, 3, 13, 0], 0, 6, [3, 1, 1, 1, 0]),     # no surplus: the half-room promise binds
])
def test_TC_1802_present_alloc_truth_table(ns, cur, room, want):
    """TC-1802 (LLR-1801.2): all notes whole when they fit; otherwise the
    cursor is promised up to half the room, every other note at least 2 rows,
    1 when even that does not fit, a note with no rows gets 0, and the rows
    handed out never exceed the room whenever the room holds a row per note."""
    got = views.present_alloc(ns, cur, room)
    assert got == want, got
    assert all(0 <= k <= n for k, n in zip(got, ns)), got
    if room >= sum(1 for n in ns if n):
        assert sum(got) <= room, got
        assert all(k >= 1 for k, n in zip(got, ns) if n), got
    if 0 <= cur < len(ns) and ns[cur]:
        assert got[cur] >= 1, got


# --------------------------------------------------------------------------- #
# TC-1803 — the exact split frames (LLR-1801.2)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name, cursor, w, h", [
    ("PRES-V3-split-118x30.txt", nb.CURSOR, 118, 30),
    ("PRES-V3-split-80x24.txt", nb.CURSOR, 80, 24),
    ("PRES-V3-split-long-118x30.txt", nb.LONG, 118, 30),
    ("PRES-V3-split-long-80x24.txt", nb.LONG, 80, 24),
])
def test_TC_1803_the_exact_split_frames(tmp_path, name, cursor, w, h):
    """TC-1803 (LLR-1801.2): the split view equals the PRES-V3 split frames —
    the shipped gantt rows unchanged on top, then a block per task, two columns
    at 118 and one at 80, the cursor's block accented."""
    b = nb.build(tmp_path / "board.json")
    assert _rows(b, cursor, w, h) == _frame(name)


def test_TC_1803_the_gantt_rows_on_top_are_the_gantt_views(tmp_path):
    """TC-1803 (LLR-1801.2): the split view's top — header aside, which names the
    view — is the gantt view's top, row for row, down to the separator."""
    b = nb.build(tmp_path / "board.json")
    for w, h in ((118, 30), (80, 24)):
        g, s = _rows(b, nb.CURSOR, w, h, "gantt"), _rows(b, nb.CURSOR, w, h, "split")
        top = 1 + 2 + 1 + 5 + 1
        assert g[1:top] == s[1:top], (w, h)
        assert s[top - 1].startswith("─" * 20)


# --------------------------------------------------------------------------- #
# TC-1804 — every note at once (LLR-1801.2): the operator's requirement
# --------------------------------------------------------------------------- #
SIZES = [(118, 30), (80, 24), (100, 30), (99, 30), (140, 40), (118, 24), (80, 30), (120, 36),
         (80, 19)]          # 80x19: exactly a heading per task and a row per note


@pytest.mark.parametrize("w, h", SIZES)
def test_TC_1804_every_shown_open_task_with_notes_shows_its_text(tmp_path, w, h):
    """TC-1804 (LLR-1801.2): for every cursor, every shown open task WITH notes
    has its own note text on screen at the same time; a task with no notes says
    `no notes` on its heading; every cut note says `… +` (a silent cut is a lie
    to the room); two columns from 100 wide, one below."""
    b = nb.build(tmp_path / "board.json")
    noted = _shown_open_with_notes(b)
    assert len(noted) == 4, [t.id for t in noted]           # the rule's population
    for t in [x for x in b.visible_tasks(False) if x.project_id == pb.PROJECT_ID
              and not b.is_done(x)]:
        rows = _rows(b, t.id, w, h)
        body = rows[10:]
        joined = "\n".join(body)
        for n in noted:
            assert _first_words(n.notes) in joined, (w, h, t.id, n.id, joined)
        assert "no notes" in joined, (w, h, t.id)
        cw = (w - 5) // 2 if w >= 100 else w - 2
        for n in noted:                                  # each cut note says so, in its block
            block = _block(body, n.title, w)
            whole = [x for _, x in views.present_note_lines(n.notes, cw - 2) if x]
            if any(x not in block for x in whole):
                assert "… +" in block, (w, h, t.id, n.id, block)
        bar = [r for r in body if r.strip()]
        if w >= 100:
            assert all("│" in r for r in body), (w, h, t.id)
        else:
            assert not any(" │ " in r for r in bar), (w, h, t.id)
        for r in rows:
            assert views.vis(r) == w, (w, h, views.vis(r), r)


def _block(body: list[str], title: str, w: int) -> str:
    """A task's block: its heading row and the rows under it, in its column."""
    cols = [(0, (w - 5) // 2 + 1), ((w - 5) // 2 + 4, w)] if w >= 100 else [(0, w)]
    for a, z in cols:
        rows = [r[a:z] for r in body]
        start = next((i for i, r in enumerate(rows) if title in r), None)
        if start is not None:
            end = next((i for i in range(start + 1, len(rows))
                        if rows[i].lstrip().startswith(("▎ ", "▌ ")) and
                        re.search(r"(in \d+d|▲\d+d|today|no due)\s*$", rows[i])), len(rows))
            return "\n".join(rows[start:end])
    raise AssertionError(title)


@pytest.mark.parametrize("w, h", [(80, 18), (118, 15), (80, 11)])
def test_TC_1804_below_a_row_per_note_every_missing_note_is_declared(tmp_path, w, h):
    """TC-1804 (LLR-1801.2; qa-reviewer QA-1, QA-4): when the room no longer
    holds a heading per task and a row per note, the cursor's note keeps a row
    and stays in view, and what does not fit is declared — a `… +N` on a cut
    note, `↑ N lines above` / `↓ N more lines` at a column's edge — never a
    silent cut."""
    b = nb.build(tmp_path / "board.json")
    for t in _shown_open_with_notes(b):
        rows = _rows(b, t.id, w, h)
        body = rows[10:]
        joined = "\n".join(body)
        assert "more lines" in joined or "lines above" in joined, (w, h, t.id, joined)
        if h - 10 >= 3:                                    # a room that holds a window
            block = _block(body, t.title, w)
            assert _first_words(t.notes)[:8] in block, (w, h, t.id, block)
        for r in rows:
            assert views.vis(r) == w, (w, h, r)


def test_TC_1806_the_first_page_down_never_moves_the_text_back(tmp_path):
    """TC-1806 (LLR-1801.3; ux-reviewer PDR PC-1): when page 0 was windowed onto
    the cursor's block (80x18, cursor `tw5`), the first page down starts the
    whole text at or below the first block page 0 showed — the room never
    watches the text jump back to the top — and keeps paging down from there."""
    b = nb.build(tmp_path / "board.json")
    pages = [_rows(b, nb.LONG, 80, 18, scroll=p)[10:] for p in range(4)]
    assert pages[0][0].lstrip().startswith("↑"), pages[0]
    first0 = next(r for r in pages[0] if r.lstrip().startswith(("▎", "▌")))
    assert "Fix checkout 500 error" in first0, first0
    assert not any("Build component library" in r for r in pages[1]), pages[1]
    assert pages[1][0].lstrip().startswith("↑"), pages[1]
    above = [int(re.search(r"↑ (\d+)", pg[0]).group(1)) for pg in pages[1:]]
    assert above == sorted(above) and len(set(above)) == len(above), above


def test_TC_1804_every_task_hidden_leaves_the_notes_area_blank(tmp_path):
    """TC-1804 (LLR-1801.2; ux-reviewer UX-5, architect A-6): with every task
    hidden the split view keeps the header, the ruler, the span row and the
    rule, and paints nothing under the rule."""
    b = nb.build(tmp_path / "board.json")
    for t in b.tasks:
        if t.project_id == pb.PROJECT_ID:
            t.show_in_present = False
    for w, h in ((118, 30), (80, 24)):
        rows = _rows(b, None, w, h)
        assert "WEBSITE REDESIGN" in rows[3] and rows[4].startswith("────"), rows[:5]
        assert all(r.strip() == "" for r in rows[5:]), rows[5:]


def test_TC_1804_hidden_and_done_tasks_are_in_neither_part(tmp_path):
    """TC-1804 (LLR-1801.2): a task hidden with `space` (`show_in_present`) and a
    done task are out of the split view entirely — no gantt row, no block."""
    b = nb.build(tmp_path / "board.json")
    b.task_by_id("tw4").show_in_present = False
    rows = _rows(b, nb.CURSOR, 118, 30)
    joined = "\n".join(rows)
    assert "Optimize image assets" not in joined
    assert _first_words(nb.NOTES["tw4"]) not in joined
    assert "Design homepage mockups" not in joined                 # tw1 is done
    assert _first_words(nb.NOTES[nb.LONG]) in joined


def test_TC_1804_the_cursor_note_gets_more_when_it_does_not_fit(tmp_path):
    """TC-1804 (LLR-1801.2): at 80x24 the long note shows more of itself when it
    is the cursor's than when it is not — the presenter reads the task under
    discussion further, the others keep their first line."""
    b = nb.build(tmp_path / "board.json")
    first = _first_words(nb.NOTES[nb.LONG])

    def long_rows(cursor):
        rows = _rows(b, cursor, 80, 24)[10:]
        start = next(i for i, r in enumerate(rows) if "Launch new homepage" in r)
        end = next(i for i, r in enumerate(rows) if "SEO redirects map" in r)
        return rows[start + 1:end]

    other, own = long_rows(nb.CURSOR), long_rows(nb.LONG)
    assert first in other[0] and first in own[0]
    assert len(own) > len(other), (own, other)


# --------------------------------------------------------------------------- #
# TC-1805 — S1 over the notes (LLR-1801.2)
# --------------------------------------------------------------------------- #
def test_TC_1805_hostile_notes_and_titles_render_literally(tmp_path):
    """TC-1805 (LLR-1801.2, S1/C8): note text and titles from the board file are
    painted literally in both views — `[bold]`, a lone `[/]`, a `[link=…]` — and
    every row keeps its exact width."""
    b = nb.build(tmp_path / "board.json")
    b.task_by_id("tw2").notes = "[/] boom\n- [bold]x[/bold] item\n1. [link=https://e.x]y[/link]"
    b.task_by_id("tw4").title = "[red]Optimize[/red]"
    for view in ("split", "gantt"):
        for w, h in ((118, 30), (80, 24)):
            rows = _rows(b, "tw2", w, h, view)
            joined = "\n".join(rows)
            assert "[/] boom" in joined, (view, w)
            assert "[bold]x[/bold] item" in joined, (view, w)
            assert "[link=https://e.x]y[/link]" in joined, (view, w)
            assert "[red]Optimize" in joined, (view, w)
            for r in rows:
                assert views.vis(r) == w, (view, w, r)


# --------------------------------------------------------------------------- #
# TC-1806 — scrolling the notes (LLR-1801.3)
# --------------------------------------------------------------------------- #
def test_TC_1806_pgdn_scrolls_the_cursor_note_and_says_what_is_above(tmp_path):
    """TC-1806 (LLR-1801.3): with the long note under the cursor and cut to 4
    rows at 80x24, page 1 shows its next rows under `↑ 3 lines above`, page 999
    ends on the note's last line; the gantt rows and the other blocks do not
    move."""
    b = nb.build(tmp_path / "board.json")
    top = _rows(b, nb.LONG, 80, 24)
    one = _rows(b, nb.LONG, 80, 24, scroll=1)
    end = _rows(b, nb.LONG, 80, 24, scroll=999)
    assert "↑ 3 lines above" in "\n".join(one), one
    assert "↓" in "\n".join(one)
    assert "username_subject" not in "\n".join(top)
    assert "username_subject" in "\n".join(end), end
    assert top[10:18] == one[10:18]                     # tw2, tw3, tw4 blocks unchanged
    assert top[:10] == one[:10]                         # the gantt rows unchanged


@pytest.mark.parametrize("w, h, cursor, whole", [(80, 24, nb.LONG, False),
                                                 (118, 30, nb.LONG, False),
                                                 (80, 30, nb.LONG, False),
                                                 (60, 20, nb.CURSOR, True)])
def test_TC_1806_paging_down_shows_every_row_of_the_note(tmp_path, w, h, cursor, whole):
    """TC-1806 (LLR-1801.3; ux-reviewer UX-1): paging down from page 0 to the
    last page puts EVERY wrapped row of the scrolled text on screen at least
    once — the cursor's note, or every note when the whole area scrolls — so a
    page never jumps over rows the presenter could not then reach; the pages
    stop changing at the last one."""
    b = nb.build(tmp_path / "board.json")
    seen, prev = set(), None
    for page in range(60):
        rows = _rows(b, cursor, w, h, scroll=page)[10:]
        seen.update(r.strip() for r in rows)
        if rows == prev:
            break
        prev = rows
    else:
        raise AssertionError("the pages never stopped changing")
    text = "\n".join(seen)
    tasks = _shown_open_with_notes(b) if whole else [b.task_by_id(cursor)]
    cw = (w - 5) // 2 if w >= 100 else w - 2
    for t in tasks:
        for lead, txt in views.present_note_lines(t.notes, cw - 2):
            if txt:
                assert txt in text, (w, h, t.id, txt)


def test_TC_1806_when_no_cursor_note_can_scroll_the_whole_area_does(tmp_path):
    """TC-1806 (LLR-1801.3): at 60x20 every note is cut to one or two rows, so
    the cursor's note cannot scroll; one step down shows the column's whole
    text from its top — every note whole, the cut declared `↓ N more lines` —
    and scrolling further reaches the last note's last line."""
    b = nb.build(tmp_path / "board.json")
    top = "\n".join(_rows(b, nb.CURSOR, 60, 20))
    one = "\n".join(_rows(b, nb.CURSOR, 60, 20, scroll=1))
    end = "\n".join(_rows(b, nb.CURSOR, 60, 20, scroll=999))
    assert "• Buttons, inputs and cards: done" not in top
    assert "• Buttons, inputs and cards: done" in one, one
    assert "more lines" in one
    assert "username_subject" in end, end
    assert "↑" in end


def test_TC_1806_scroll_moves_nothing_in_the_gantt_view(tmp_path):
    """TC-1806 (LLR-1801.3): the gantt view ignores `scroll`."""
    b = nb.build(tmp_path / "board.json")
    assert _rows(b, nb.LONG, 118, 30, "gantt", 10) == _rows(b, nb.LONG, 118, 30, "gantt")


@pytest.mark.parametrize("w, h", [(118, 30), (80, 24), (60, 20), (118, 12), (80, 11)])
def test_TC_1806_every_scroll_keeps_the_frame_exact(tmp_path, w, h):
    """TC-1806 (LLR-1801.3): any scroll, any cursor, a small frame — every row
    is exactly `w` cells and the frame exactly `h` rows."""
    b = nb.build(tmp_path / "board.json")
    for cur in ("tw2", "tw3", "tw5", "tw6"):
        for sc in (0, 5, 10, 15, 400):
            rows = _rows(b, cur, w, h, scroll=sc)
            assert len(rows) == h
            for r in rows:
                assert views.vis(r) == w, (w, h, cur, sc, r)


# --------------------------------------------------------------------------- #
# TC-1807 — the gantt view keeps a note's line breaks (LLR-1802.1)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name, w, h", [
    ("PRES-V3-gantt-notes-118x30.txt", 118, 30),
    ("PRES-V3-gantt-notes-80x24.txt", 80, 24),
])
def test_TC_1807_the_cursor_note_keeps_its_line_breaks(tmp_path, name, w, h):
    """TC-1807 (LLR-1802.1): the gantt view's cursor note is at most 3 rows —
    its line breaks kept (`1. Feature-flag` starts its own row, never
    `Sep 22. 1. Feature-flag`), the cut said `… +N lines` — and equals the
    PRES-V3 frame."""
    b = nb.build(tmp_path / "board.json")
    rows = _rows(b, nb.LONG, w, h, "gantt")
    assert rows == _frame(name)
    notes = [r for r in rows if r.startswith("  · ")]
    assert len(notes) == 3, notes
    assert notes[0].strip().endswith("Sep 22."), notes
    assert notes[1].startswith("  · 1. Feature-flag"), notes
    assert re.match(r"  · … \+\d+ lines", notes[2]), notes
    assert "Sep 22. 1." not in "\n".join(rows)


def test_TC_1807_the_header_names_the_view(tmp_path):
    """TC-1807 (LLR-1802.1): the header carries the view's name in one quiet
    word after the project — `gantt` or `split` — and nothing else of the
    keys."""
    b = nb.build(tmp_path / "board.json")
    for w, h in ((118, 30), (80, 24)):
        for view in ("gantt", "split"):
            head = _rows(b, nb.CURSOR, w, h, view)[0]
            assert head.startswith(f"◆ PRESENT · Website Redesign  {view} "), head
            text = "\n".join(_rows(b, nb.CURSOR, w, h, view))
            for key in ("pgdn", "⇥", "1 gantt", "2 split", "esc"):
                assert key not in text, (view, w, key)


def test_TC_1805_hostile_text_on_every_new_escape_site(tmp_path):
    """TC-1805 (LLR-1801.2, S1/C8; security-reviewer S-2): the escape holds at
    the sites the 118/80 frames do not reach — the one-row cut (`… +N` beside
    a first line, 60x20), the scrolled cursor note, a split heading for a
    hostile cursor title — and for notes ending in a backslash or holding
    a backslash and a bracket; every row keeps its width."""
    b = nb.build(tmp_path / "board.json")
    b.task_by_id("tw2").notes = "[/] cut row\n" + "\n".join(f"- line {i}" for i in range(9))
    b.task_by_id("tw4").notes = "ends in a backslash x\\"
    b.task_by_id("tw6").notes = "a\\[b] literal"
    b.task_by_id("tw5").title = "[bold]Launch[/bold]"
    b.task_by_id("tw5").notes = "\n".join(f"[i]step {i}[/i]" for i in range(30))
    for w, h, cur, sc in ((60, 20, "tw3", 0), (80, 24, "tw5", 1),
                          (118, 30, "tw5", 0)):
        rows = _rows(b, cur, w, h, scroll=sc)
        joined = "\n".join(rows)
        assert "[/] cut row" in joined, (w, h)
        assert "x\\" in joined and "a\\[b] literal" in joined, (w, h)
        assert "[bold]Launch[/bold]" in joined or "[bold]Launch" in joined, (w, h)
        assert "[i]step" in joined, (w, h)
        for r in rows:
            assert views.vis(r) == w, (w, h, r)

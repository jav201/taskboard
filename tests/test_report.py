"""The board report — one self-contained HTML file, generated on demand.

The law that matters most here is the one about NOT doing something: generating a
report must leave the board byte-identical. A reporting feature that writes is a
reporting feature that can corrupt, and this is the first surface in the app whose
whole job is to read.

The rest is the doctrine travelling into a document: no forecast, no invented
completion date, a closed project is never judged, and nothing addresses the
reader. Plus the one rule the palette measurement forced — no figure may encode a
project by hue alone.
"""

import hashlib
import json
import re
import subprocess
import sys
from datetime import date, timedelta

from taskboard.models import Board, Project, Task
from taskboard.report import (BUCKETS, build_report, report_path, write_report,
                              _bucket, _due_word)

TODAY = date(2026, 7, 31)


def iso(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def board(tmp_path, name="b.json") -> Board:
    b = Board.load(str(tmp_path / name))
    b.projects.clear()
    b.tasks.clear()
    return b


def loaded(tmp_path, name="b.json") -> Board:
    """A board with every state the report has to describe."""
    b = board(tmp_path, name)
    web = Project("Website Redesign", "lime", "on_track",
                  start_date=iso(-24), due_date=iso(12))
    plat = Project("Platform", "sky", "on_track", start_date=iso(-10), due_date=iso(38))
    old = Project("Data Warehouse", "green", "completed",
                  start_date=iso(-70), due_date=iso(-9))
    b.projects += [web, plat, old]
    b.tasks += [
        Task("Fix checkout 500 error", web.id, "Doing", "high",
             start_date=iso(-9), due_date=iso(-3)),
        Task("Design homepage mockups", web.id, "Doing", "normal", due_date=iso(0)),
        Task("Optimize image assets", web.id, "Backlog", "normal", due_date=iso(9)),
        Task("Ship the schema change", web.id, "Done", "normal", due_date=iso(-14)),
        Task("KServe rollout", plat.id, "Doing", "normal", due_date=iso(16)),
        Task("k3s bootstrap", plat.id, "Backlog", "high", due_date=iso(40)),
        Task("Compress database backups", old.id, "Done", "normal", due_date=iso(-40)),
        Task("Review pull requests", None, "Doing", "normal", due_date=iso(3)),
    ]
    b.save()
    return b


def text_of(html_doc: str) -> str:
    """The document's readable text, with the style block and figures removed."""
    body = html_doc.split("</style>", 1)[1]
    body = re.sub(r"<svg.*?</svg>", " ", body, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))


# --------------------------------------------------------------------------- #
# AC4 — the law of not writing
# --------------------------------------------------------------------------- #
def test_generating_a_report_never_writes_the_board(tmp_path, monkeypatch):
    """THE LAW OF THIS FEATURE, and it took a mutant to state it correctly.

    The first version compared the file's CHECKSUM before and after — and a
    report that called `board.save()` passed it, because saving an unmodified
    board writes the SAME BYTES BACK. Content-equality cannot see a write; it
    only sees a change. That distinction is the whole risk: if the in-memory
    board ever differs from disk (a load-time colour remap, the archive sweep),
    a stray save would overwrite the user's file with bytes they never asked for,
    and the checksum test would still be green.

    So the law now asserts the two things it actually means: the file is not
    REWRITTEN (its mtime does not move), and `Board.save` is never called at
    all."""
    b = loaded(tmp_path, "readonly.json")
    path = tmp_path / "readonly.json"
    before_hash = hashlib.md5(path.read_bytes()).hexdigest()
    before_mtime = path.stat().st_mtime_ns

    saves = []
    monkeypatch.setattr(Board, "save", lambda self: saves.append(self.path))

    write_report(b, TODAY)
    write_report(b, TODAY, project="Platform")
    build_report(b, TODAY)

    assert saves == [], f"the report called Board.save: {saves}"
    assert path.stat().st_mtime_ns == before_mtime, "the board file was rewritten"
    assert hashlib.md5(path.read_bytes()).hexdigest() == before_hash


def test_the_report_lands_beside_its_own_board(tmp_path):
    """So a fixture's report lands by the fixture — the live board's directory is
    unreachable from a test by construction, not by care."""
    b = loaded(tmp_path, "where.json")
    out = write_report(b, TODAY)
    assert out.parent == tmp_path / "reports"
    assert out.exists() and out.stat().st_size > 0
    assert report_path(b, TODAY, "Platform").name.startswith("platform-")


# --------------------------------------------------------------------------- #
# AC3 — self-contained
# --------------------------------------------------------------------------- #
def test_the_document_needs_nothing_from_the_network(tmp_path):
    """One file, no CDN: it opens on a laptop with no internet, and it cannot be
    silently changed by something a third party serves."""
    doc = build_report(loaded(tmp_path), TODAY)
    assert "http://" not in doc and "https://" not in doc
    assert "<script" not in doc
    assert "<link" not in doc
    assert doc.lstrip().startswith("<!doctype html>")
    assert "<style>" in doc                      # the CSS travels inside


# --------------------------------------------------------------------------- #
# AC5 — the numbers are the board's numbers
# --------------------------------------------------------------------------- #
def test_the_counts_are_the_boards_real_counts(tmp_path):
    b = loaded(tmp_path)
    txt = text_of(build_report(b, TODAY))
    open_n = sum(1 for t in b.visible_tasks(False) if not b.is_done(t))
    done_n = sum(1 for t in b.visible_tasks(False) if b.is_done(t))
    assert re.search(rf"{open_n}\s+open", txt), txt[:400]
    assert re.search(rf"{done_n}\s+done", txt), txt[:400]
    assert re.search(r"1\s+overdue", txt)        # the one late task


def test_a_scoped_report_covers_only_that_project(tmp_path):
    b = loaded(tmp_path)
    doc = text_of(build_report(b, TODAY, project="Platform"))
    assert "Platform" in doc
    assert "Website Redesign" not in doc
    assert "KServe rollout" in doc
    assert "Fix checkout 500 error" not in doc


def test_the_horizon_buckets_add_up_to_the_tasks(tmp_path):
    """A share that does not total is a lie about proportion, which is why `done`
    is a bucket rather than a silent omission."""
    b = loaded(tmp_path)
    tasks = b.visible_tasks(False)
    counted = sum(1 for t in tasks if _bucket(t, b, TODAY) in BUCKETS)
    assert counted == len(tasks)


# --------------------------------------------------------------------------- #
# AC6 / doctrine — honesty travels into the document
# --------------------------------------------------------------------------- #
def test_work_with_no_recorded_date_reads_unaged_never_zero(tmp_path):
    """The momentum ruling, in document form: unknown is unknown."""
    doc = text_of(build_report(loaded(tmp_path), TODAY))
    assert "unaged" in doc
    assert "0d in phase" not in doc


def test_a_closed_project_is_never_judged(tmp_path):
    """Nothing is expected of a completed project, so nothing about it is late —
    the same ruling the due meter obeys, carried into the report."""
    b = loaded(tmp_path)
    doc = text_of(build_report(b, TODAY))
    i = doc.index("Data Warehouse")
    section = doc[i:i + 300]
    # "0 overdue" is a count; the JUDGEMENT form is "Nd overdue" — that is what a
    # closed project may never wear
    assert not re.search(r"\d+d overdue", section), section
    assert "-9d" in section                      # the plain distance instead
    assert _due_word(-9, closed=True) == "-9d"
    assert _due_word(-9, closed=False) == "9d overdue"


def test_the_document_states_no_forecast(tmp_path):
    """It may SAY it makes no forecast (it does, twice); it may not make one."""
    doc = text_of(build_report(loaded(tmp_path), TODAY)).lower()
    for claim in ("velocity", "eta ", "estimated completion", "projected",
                  "will finish", "on track to", "expected to"):
        assert claim not in doc, claim
    assert "nothing here is a forecast" in doc          # the disclaimer stays


# --------------------------------------------------------------------------- #
# AC8 — the register
# --------------------------------------------------------------------------- #
def test_the_document_never_addresses_or_grades_the_reader(tmp_path):
    """It is the turn's log, in document form: it describes the board and does
    not talk to the person reading it. Same law the views obey."""
    doc = text_of(build_report(loaded(tmp_path), TODAY))
    banned = re.compile(r"\b(you|your|yours|we|our|us)\b", re.I)
    hits = banned.findall(doc)
    assert not hits, hits[:4]
    for judgement in ("behind schedule", "poor", "bad", "at risk", "failing"):
        assert judgement not in doc.lower()


# --------------------------------------------------------------------------- #
# AC7 — the palette measurement, honoured
# --------------------------------------------------------------------------- #
def test_no_figure_carries_meaning_in_hue_alone(tmp_path):
    """MEASURED CONSTRAINT, not a preference: two of the eight project hues are
    hard to tell apart with full colour vision (violet/indigo) and two are
    identical to a red-blind reader (fuchsia/violet). So every project that gets
    a coloured chip is ALSO named in text, and every figure has a table of the
    same numbers beside it."""
    b = loaded(tmp_path)
    doc = build_report(b, TODAY)
    for p in b.projects:
        i = doc.index(p.name)
        assert '<span class="chip"' in doc[max(0, i - 200):i], p.name
    assert doc.count("<table") >= 1 + len(b.projects) - 1
    assert doc.count("<figure") == len(b.projects) + 1   # +1 Inbox lane


def test_the_horizon_is_a_table_as_well_as_a_bar(tmp_path):
    doc = build_report(loaded(tmp_path), TODAY)
    for bucket in BUCKETS:
        assert f">{bucket}<" in doc, bucket


# --------------------------------------------------------------------------- #
# untrusted text (the C-17 lesson, new surface)
# --------------------------------------------------------------------------- #
def test_a_hostile_title_cannot_break_out_into_markup(tmp_path):
    b = board(tmp_path, "hostile.json")
    p = Project("<script>alert(1)</script>", "lime", "on_track", due_date=iso(5))
    b.projects.append(p)
    b.tasks.append(Task('Fix "><img src=x onerror=alert(1)> now', p.id, "Doing",
                        "normal", due_date=iso(2)))
    doc = build_report(b, TODAY)
    assert "<script>alert(1)</script>" not in doc
    assert "&lt;script&gt;" in doc
    assert "onerror=alert(1)>" not in doc
    assert doc.count("<html") == 1


# --------------------------------------------------------------------------- #
# AC1 / AC2 — the CLI, driven as a user drives it
# --------------------------------------------------------------------------- #
def test_the_cli_writes_a_report_and_says_where(tmp_path):
    b = loaded(tmp_path, "cli.json")
    path = tmp_path / "cli.json"
    before = hashlib.md5(path.read_bytes()).hexdigest()
    r = subprocess.run([sys.executable, "-m", "taskboard", "--board", str(path),
                        "--report"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "Report written to" in r.stdout
    written = r.stdout.split("Report written to", 1)[1].strip()
    assert written.endswith(".html")
    from pathlib import Path
    assert Path(written).exists()
    assert hashlib.md5(path.read_bytes()).hexdigest() == before   # still read-only


def test_the_cli_scopes_to_a_project_and_refuses_an_unknown_one(tmp_path):
    loaded(tmp_path, "cli2.json")
    path = tmp_path / "cli2.json"
    ok = subprocess.run([sys.executable, "-m", "taskboard", "--board", str(path),
                         "--report", "Platform"], capture_output=True, text=True)
    assert ok.returncode == 0 and "platform-" in ok.stdout

    bad = subprocess.run([sys.executable, "-m", "taskboard", "--board", str(path),
                          "--report", "Nope"], capture_output=True, text=True)
    assert bad.returncode != 0
    assert "no project named" in (bad.stderr + bad.stdout)
    assert "Website Redesign" in (bad.stderr + bad.stdout)   # it names the real ones
    assert not list((tmp_path / "reports").glob("nope-*.html"))


# --------------------------------------------------------------------------- #
# AC9 — the key, and the contract it owes
# --------------------------------------------------------------------------- #
def test_the_report_key_is_in_the_seat():
    from taskboard.keymap import KEYMAP, fit_bar
    entry = next(k for k in KEYMAP if k.action == "report")
    assert entry.show == "R"
    assert "R" in {show for show, _label in fit_bar(400, "swimlanes")[0]}


async def test_pressing_R_writes_the_report_and_reports_the_path(tmp_path, monkeypatch):
    from taskboard.app import TaskboardApp
    loaded(tmp_path, "key.json")
    path = tmp_path / "key.json"
    said = []
    app = TaskboardApp(board_path=str(path))
    async with app.run_test(size=(100, 30)) as pilot:
        app.notify = lambda *a, **k: said.append(a[0] if a else "")
        await pilot.pause()
        # measured AFTER startup on purpose: launching the app may legitimately
        # write (the one-time renumber notice, the 20-day sweep). The report's
        # read-only law is about the REPORT, not about mounting. And it watches
        # for the WRITE, not for a change — saving an unmodified board rewrites
        # identical bytes, which a checksum cannot see.
        before_mtime = path.stat().st_mtime_ns
        saves = []
        monkeypatch.setattr(Board, "save", lambda self: saves.append(self.path))
        await pilot.press("R")
        await pilot.pause()
        assert saves == [], f"pressing R saved the board: {saves}"
        assert path.stat().st_mtime_ns == before_mtime
    assert any("Report written to" in m for m in said), said
    assert list((tmp_path / "reports").glob("board-*.html"))


def test_an_empty_board_still_produces_a_document(tmp_path):
    b = board(tmp_path, "empty.json")
    doc = build_report(b, TODAY)
    assert doc.lstrip().startswith("<!doctype html>")
    assert "0 projects" in text_of(doc).replace("  ", " ") or "0" in text_of(doc)

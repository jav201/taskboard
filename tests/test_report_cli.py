"""`taskboard --report` exports the new HTML reports and asks for the board (batch
2026-10-29-batch-02, increment 001: HLR-4101..HLR-4105, LLR-4101.1..LLR-4105.4;
AT-4101..AT-4107, TC-4101..TC-4112).

Every CLI run is a SUBPROCESS of `python -m taskboard` with the repo root as its working
directory (the editable install points at the MAIN checkout, so the cwd decides which
`taskboard` imports) and a temporary HOME and USERPROFILE: the real `~/.taskboard` is never
touched. Boards are the report fixture's synthetic ones. Expected names, files and counts
are typed here, never read back from the code under test.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import report_fixture as F
from report_browser import new_context, open_page, require_browser, shown_ids

import taskboard
from taskboard import __main__ as entry
from taskboard import report_html
from taskboard.boards import peek_board
from taskboard.people import Person

REPO = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
ALPHA = ("alpha", "Alpha", F.personal)
BETA = ("beta", "Beta", F.course)
ALPHA_PROJECTS = {"Move apartment", "Taxes 2026", "Docs"}
BETA_PROJECTS = {"Video module 3", "Community forum", "Someday ideas", F.HOSTILE_NAME}
ROOT_FILE_OK = Path(taskboard.__file__).resolve().parent.parent == REPO


def test_the_probe_these_tests_run_against_the_worktree():
    """The import probe, in the suite: this file's `taskboard` is the checkout it sits in."""
    assert ROOT_FILE_OK, taskboard.__file__


def make_home(tmp_path: Path, boards=(ALPHA, BETA), last: str = "alpha", missing=(), where=None):
    """A temp HOME with a registry of `boards` (each saved in `~/.taskboard/boards/<id>/`);
    ids in `missing` are registered but have no file. Returns (home, {id: board file})."""
    home = tmp_path / "home"
    root = home / ".taskboard"
    entries, files = [], {}
    for bid, name, make in boards:
        path = (where or {}).get(bid) or root / "boards" / bid / "board.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        if bid not in missing:
            make(path).save()
        files[bid] = path
        entries.append({"id": bid, "name": name, "color": "sky", "path": str(path),
                        "last_opened": "2026-10-29T09:00", "archived": False})
    (root / "boards.json").write_text(
        json.dumps({"version": 1, "last": last, "boards": entries}), encoding="utf-8")
    return home, files


def cli(home: Path, *args: str, stdin: str = "", io: str = "utf-8"):
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home), PYTHONIOENCODING=io)
    return subprocess.run([sys.executable, "-m", "taskboard", *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", env=env, cwd=REPO,
                          input=stdin, timeout=120)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(home: Path) -> list[str]:
    return sorted(str(p.relative_to(home)) for p in home.rglob("*")) if home.exists() else []


def embedded(path: Path) -> dict:
    page = path.read_text(encoding="utf-8")
    raw = re.search(r'<script id="board-data" type="application/json">(.*?)</script>',
                    page, re.S).group(1)
    return json.loads(raw)


def reports_in(files: dict, bid: str) -> list[str]:
    folder = files[bid].parent / "reports"
    return sorted(p.name for p in folder.iterdir()) if folder.exists() else []


def lines(r) -> list[str]:
    return [ln for ln in r.stdout.splitlines() if ln.strip()]


# --------------------------------------------------------------------------- #
# AT-4101..AT-4107 — the commission's AT-a..AT-f and the old report's retirement
# --------------------------------------------------------------------------- #
def test_AT_4101_two_boards_pick_two_writes_b_and_c_for_board_two(tmp_path):
    """AT-4101 (US-4101, HLR-4102, HLR-4104): with two registered boards and stdin `2`,
    the command prints two paths under board 2's `reports/`, writes B and C there,
    and leaves board 1, board 2's own file and the registry byte-identical. RED at the
    base: `--report` never reads stdin and writes one old-report file for the default."""
    home, files = make_home(tmp_path)
    before = {k: sha(v) for k, v in files.items()} | {"reg": sha(home / ".taskboard" / "boards.json")}
    r = cli(home, "--report", stdin="2\n")
    assert r.returncode == 0, r.stderr
    folder = files["beta"].parent / "reports"
    assert lines(r) == [str(folder / f"workspace-{TODAY}.html"), str(folder / f"deck-{TODAY}.html")]
    assert all(Path(p).stat().st_size > 0 for p in lines(r))
    assert reports_in(files, "alpha") == []
    names = {p["name"] for p in embedded(folder / f"workspace-{TODAY}.html")["projects"]}
    assert names == BETA_PROJECTS
    assert "Alpha" in r.stderr and "Beta" in r.stderr and "(default)" in r.stderr
    after = {k: sha(v) for k, v in files.items()} | {"reg": sha(home / ".taskboard" / "boards.json")}
    assert after == before


def test_AT_4102_a_writes_reports_covering_all_boards(tmp_path):
    """AT-4102 (HLR-4102): stdin `a` writes B and C that cover both boards, into the
    default board's folder, and says so on stderr before the paths."""
    home, files = make_home(tmp_path)
    r = cli(home, "--report", stdin="a\n")
    assert r.returncode == 0, r.stderr
    folder = files["alpha"].parent / "reports"
    assert lines(r) == [str(folder / f"workspace-{TODAY}.html"), str(folder / f"deck-{TODAY}.html")]
    data = embedded(folder / f"workspace-{TODAY}.html")
    assert [b["name"] for b in data["boards"]] == ["Alpha", "Beta"]
    assert {p["name"] for p in data["projects"]} == ALPHA_PROJECTS | BETA_PROJECTS | {"Inbox"}
    assert "2 boards" in r.stderr and str(folder) in r.stderr
    assert reports_in(files, "beta") == []


def test_AT_4103_empty_piped_stdin_exits_2_with_the_list(tmp_path):
    """AT-4103 (HLR-4102): stdin that is not a terminal and ends before any line exits 2,
    lists the boards, says to pass `--board PATH`, and writes nothing."""
    home, files = make_home(tmp_path)
    before = tree(home)
    r = cli(home, "--report", stdin="")
    assert r.returncode == 2
    assert "Alpha" in r.stderr and "Beta" in r.stderr and "--board PATH" in r.stderr
    assert r.stdout == "" and tree(home) == before


@pytest.mark.parametrize("answer", ["q\n", "Q\n", "x\n", "9\n", "0\n", "-1\n"])
def test_AT_4103_q_and_an_end_of_input_after_a_bad_answer_exit_1(tmp_path, answer):
    """AT-4103 (HLR-4102): `q`, and end of input after an invalid answer, exit 1 and
    write nothing; an invalid answer is said, not guessed."""
    home, files = make_home(tmp_path)
    before = tree(home)
    r = cli(home, "--report", stdin=answer)
    assert r.returncode == 1
    assert r.stdout == "" and tree(home) == before
    if answer[0] not in "qQ":
        assert "Not a choice" in r.stderr


def test_AT_4104_board_flag_does_not_prompt_and_project_scopes(tmp_path):
    """AT-4104 (HLR-4101, HLR-4103): `--board PATH` never prompts (empty piped stdin is
    fine) and writes both reports beside that file; `PROJECT` scopes the files to that
    project; an unknown project exits 2, lists the board's projects and writes nothing."""
    home, files = make_home(tmp_path)
    alpha = files["alpha"]
    registry_before = sha(home / ".taskboard" / "boards.json")
    plain = cli(home, "--board", str(alpha), "--report", stdin="")
    assert plain.returncode == 0, plain.stderr
    folder = alpha.parent / "reports"
    assert lines(plain) == [str(folder / f"workspace-{TODAY}.html"), str(folder / f"deck-{TODAY}.html")]
    assert "Board [" not in plain.stderr
    scoped = cli(home, "--board", str(alpha), "--report", "Move apartment", stdin="")
    assert scoped.returncode == 0, scoped.stderr
    name = f"workspace-alpha-move-apartment-{TODAY}.html"
    assert lines(scoped)[0] == str(folder / name)
    assert {p["name"] for p in embedded(folder / name)["projects"]} == {"Move apartment"}
    reports_before = reports_in(files, "alpha")
    bad = cli(home, "--board", str(alpha), "--report", "Nope", stdin="")
    assert bad.returncode == 2 and bad.stdout == ""
    assert "no project named 'Nope'" in bad.stderr
    for n in ALPHA_PROJECTS:
        assert n in bad.stderr
    assert reports_in(files, "alpha") == reports_before
    assert sha(home / ".taskboard" / "boards.json") == registry_before   # nothing registered


def test_AT_4105_missing_board_path_is_refused_and_creates_nothing(tmp_path):
    """AT-4105 (HLR-4104): `--board <path>` that is no board file is refused with exit 2
    before anything is built, and nothing is created at it or under HOME. RED at the base:
    `Board.load` seeds and saves sample data at the missing path (security S-3)."""
    home, files = make_home(tmp_path)
    folder = tmp_path / "elsewhere"
    folder.mkdir()
    (tmp_path / "notes.txt").write_text("not a board", encoding="utf-8")
    cases = {"missing": folder / "nope" / "b.json", "folder": folder,
             "text": tmp_path / "notes.txt", "escape": folder / "a\x1b[2Jb.json", "empty": ""}
    for label, target in cases.items():
        before = (tree(home), tree(tmp_path))
        r = cli(home, "--board", str(target), "--report", stdin="")
        assert r.returncode == 2, (label, r.stderr)
        assert r.stderr.startswith("taskboard: no board file at "), (label, r.stderr)
        assert "\x1b" not in r.stderr and r.stdout == ""
        assert (tree(home), tree(tmp_path)) == before, label
    assert not (folder / "nope").exists()


def test_AT_4106_the_written_files_load_headless_with_no_console_errors(tmp_path):
    """AT-4106 (HLR-4101, trigger B4): the two files the command wrote, loaded in
    headless Chromium, log 0 console errors and 0 page errors and request nothing but
    themselves; the workspace shows the board's tasks and the deck its slides."""
    require_browser()
    home, files = make_home(tmp_path)
    r = cli(home, "--board", str(files["alpha"]), "--report", stdin="")
    assert r.returncode == 0, r.stderr
    workspace, deck = (Path(p) for p in lines(r))
    api = require_browser()
    with api.sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            w = open_page(new_context(browser), workspace, ready="#tbody")
            assert w.problems() == []
            assert len(shown_ids(w.page)) > 0
            d = open_page(new_context(browser), deck, ready="#cnt")
            assert d.problems() == []
            assert d.page.locator("section.slide").count() >= 3
        finally:
            browser.close()


def test_AT_4107_the_old_report_is_not_reachable_and_the_readme_says_so(tmp_path):
    """AT-4107 (HLR-4105): the command's stdout holds the two new paths and not the old
    `Report written to` line, and no `board-<date>.html` old-report file appears."""
    home, files = make_home(tmp_path)
    r = cli(home, "--board", str(files["alpha"]), "--report", stdin="")
    assert r.returncode == 0, r.stderr
    assert "Report written to" not in r.stdout + r.stderr
    assert len(lines(r)) == 2
    names = reports_in(files, "alpha")
    assert names == sorted([f"deck-{TODAY}.html", f"workspace-{TODAY}.html"])


# --------------------------------------------------------------------------- #
# TC-4101.. — the mechanism
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("kind, expected", [("workspace", ["workspace"]), ("deck", ["deck"]),
                                            ("both", ["deck", "workspace"])])
def test_TC_4101_report_kind_selects_the_files(tmp_path, kind, expected):
    """TC-4101 (LLR-4101.1, LLR-4101.2): `--report-kind` picks the files; the default is both."""
    home, files = make_home(tmp_path)
    r = cli(home, "--board", str(files["alpha"]), "--report", "--report-kind", kind)
    assert r.returncode == 0, r.stderr
    assert reports_in(files, "alpha") == [f"{k}-{TODAY}.html" for k in expected]
    assert len(lines(r)) == len(expected)


def test_TC_4102_report_kind_is_validated(tmp_path):
    """TC-4102 (LLR-4101.1): an unknown kind, and a kind without `--report`, exit 2."""
    home, files = make_home(tmp_path)
    assert cli(home, "--board", str(files["alpha"]), "--report", "--report-kind", "other").returncode == 2
    lone = cli(home, "--report-kind", "deck")
    assert lone.returncode == 2 and "--report-kind needs --report" in lone.stderr
    assert reports_in(files, "alpha") == []


class Stream:
    """A stdin stand-in: the answers it gives, whether it is a terminal."""

    def __init__(self, answers, tty):
        self.answers, self.tty = list(answers), tty

    def readline(self, limit=-1):
        return self.answers.pop(0) if self.answers else ""

    def isatty(self):
        return self.tty


class Entry:
    def __init__(self, bid, name, path):
        self.id, self.name, self.path = bid, name, path


def _entries(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    for p in (a, b):
        p.write_text("{}", encoding="utf-8")
    return [Entry("alpha", "Alpha", str(a)), Entry("beta", "Beta", str(b))]


class Err(list):
    def write(self, text):
        self.append(text)

    def flush(self):
        pass


def test_TC_4103_the_prompt_answers(tmp_path):
    """TC-4103 (LLR-4102.2, LLR-4102.3): a blank line takes the default, a number picks,
    an invalid answer asks again, `a` is every board, and a terminal at end of input
    exits 1 where a pipe at end of input exits 2."""
    es = _entries(tmp_path)
    ask = lambda answers, tty=False, err=None: entry.ask_board(es, es[0], Stream(answers, tty), err if err is not None else Err())
    assert ask(["\n"]) is es[0]
    assert ask(["2\n"]) is es[1]
    err = Err()
    assert ask(["9\n", "x\n", "2\n"], err=err) is es[1]
    assert "".join(err).count("Not a choice") == 2
    assert ask(["A\n"]) is None
    err2 = Err()
    assert ask(["\u0662\n", "\u00b2\n", "1\n"], err=err2) is es[0]     # Arabic-Indic two, superscript two
    assert "".join(err2).count("Not a choice") == 2
    with pytest.raises(SystemExit) as e1:
        ask([], tty=True)
    assert e1.value.code == 1
    with pytest.raises(SystemExit) as e2:
        ask([], tty=False)
    assert e2.value.code == 2
    with pytest.raises(SystemExit) as e3:
        ask(["x\n"], tty=False)             # an end of input AFTER an answer is exit 1
    assert e3.value.code == 1
    listing = entry._board_lines(es, es[1])
    assert "2. Beta  (default)" in listing and "1. Alpha  (default)" not in listing


def test_TC_4103_a_picked_board_whose_file_is_gone_asks_again(tmp_path):
    es = _entries(tmp_path)
    Path(es[1].path).unlink()
    err = Err()
    assert entry.ask_board(es, es[0], Stream(["2\n", "1\n"], False), err) is es[0]
    assert "missing or unreadable" in "".join(err)


def test_TC_4104_a_skips_and_counts_a_missing_board(tmp_path):
    """TC-4104 (LLR-4102.4): `a` skips a registered board whose file is gone, says how many."""
    home, files = make_home(tmp_path, boards=(ALPHA, BETA, ("gone", "Gone", F.side)), missing=("gone",))
    r = cli(home, "--report", stdin="a\n")
    assert r.returncode == 0, r.stderr
    assert "1 board skipped" in r.stderr and len(lines(r)) == 2
    assert [b["name"] for b in embedded(Path(lines(r)[0]))["boards"]] == ["Alpha", "Beta"]


def test_TC_4105_project_with_a_is_refused(tmp_path):
    """TC-4105 (LLR-4103.1): `--report PROJECT` with the answer `a` exits 2, nothing written."""
    home, files = make_home(tmp_path)
    before = tree(home)
    r = cli(home, "--report", "Docs", stdin="a\n")
    assert r.returncode == 2 and "names one project on one board" in r.stderr
    assert tree(home) == before


def test_TC_4106_names_and_paths_are_printed_without_control_bytes(tmp_path):
    """TC-4106 (LLR-4104.3): a board named with a newline, an ESC byte and a bidi override,
    and a project named with a newline, each print on one line with nothing a terminal obeys."""
    evil = "Evil\x1b[2J\nFAKE 9. injected\t‮txet"
    home, files = make_home(tmp_path, boards=(ALPHA, ("evil", evil, F.course)))
    # the registry loader strips ESC itself; the print function must hold on its own
    r = cli(home, "--report", stdin="x\n")
    assert r.returncode == 1
    for bad in ("\x1b", "‮", " "):
        assert bad not in r.stderr
    assert not any(ln.lstrip().startswith("FAKE") for ln in r.stderr.splitlines())
    assert "Evil" in r.stderr and "\\n" in r.stderr
    assert entry._safe("a\x1b[2Jb\nc\td e‮f") == "a[2Jb\\nc\\td" "ef"
    p = cli(home, "--board", str(files["alpha"]), "--report", "Nope\nFAKE: x", stdin="")
    assert p.returncode == 2 and not any(ln.startswith("FAKE") for ln in p.stderr.splitlines())


def test_TC_4106_a_path_with_two_spaces_is_printed_unchanged(tmp_path):
    home, files = make_home(tmp_path)
    spaced = tmp_path / "two  spaces"
    spaced.mkdir()
    board = spaced / "b.json"
    F.personal(board).save()
    r = cli(home, "--board", str(board), "--report", stdin="")
    assert r.returncode == 0, r.stderr
    assert lines(r)[0] == str(spaced / "reports" / f"workspace-{TODAY}.html")
    assert Path(lines(r)[0]).exists()


def test_TC_4107_the_cli_bytes_equal_the_h_path_bytes(tmp_path):
    """TC-4107 (LLR-4101.2): the files the command writes are byte-equal to the ones
    `report_html.extract` + `write_reports` write in-process for the same boards. The CLI
    and the app cannot drift."""
    home, files = make_home(tmp_path)
    (home / ".taskboard" / "people.json").write_text(json.dumps({"people": [
        {"id": "luis.prado", "name": "Luis Prado", "role": "Developer"}]}), encoding="utf-8")
    r = cli(home, "--report", stdin="a\n")
    assert r.returncode == 0, r.stderr
    assert [p["id"] for p in embedded(Path(lines(r)[0]))["people"]] == ["luis.prado"]
    boards = []
    for bid, name, _ in (ALPHA, BETA):
        board = peek_board(files[bid])
        board.marks = {}
        boards.append((bid, name, "sky", board))
    people = {"luis.prado": Person("luis.prado", "Luis Prado", "Developer")}
    data = report_html.extract(boards, people, {}, date.today())
    out = report_html.write_reports(data, ("workspace", "deck"), tmp_path / "inproc", date.today())
    for cli_path, mine in zip(lines(r), out):
        assert Path(cli_path).read_bytes() == mine.read_bytes()


def test_TC_4108_one_board_does_not_prompt_and_a_missing_default_is_refused(tmp_path):
    """TC-4108 (LLR-4102.1): one active board never prompts; with no registry and no
    default board file the command is refused and creates nothing (no `~/.taskboard`)."""
    home, files = make_home(tmp_path, boards=(ALPHA,))
    ok = cli(home, "--report", stdin="")
    assert ok.returncode == 0 and "Board [" not in ok.stderr and len(lines(ok)) == 2
    bare = tmp_path / "bare"
    bare.mkdir()
    r = cli(bare, "--report", stdin="")
    assert r.returncode == 2 and r.stderr.startswith("taskboard: no board file at ")
    assert tree(bare) == []


def test_TC_4109_the_source_and_the_readme_pin_the_new_behaviour():
    """TC-4109 (LLR-4105.1, LLR-4105.2): the entry point no longer calls the old report;
    the README tells the new story."""
    src = (REPO / "taskboard" / "__main__.py").read_text(encoding="utf-8")
    assert not re.search(r"\bwrite_report\b|\bbuild_report\b", src)
    text = (REPO / "README.md").read_text(encoding="utf-8")
    for needle in ("`taskboard --report-kind", "reports", "exit code 2", "exit code 1",
                   "no longer written"):
        assert needle in text.replace("Exit code", "exit code"), needle
    assert "Report written to" not in text


def test_TC_4110_stdin_that_misbehaves_never_tracebacks(tmp_path):
    """TC-4110 (LLR-4102.5): invalid UTF-8, a 10000-character line and a closed stdin are
    an invalid answer or end of input — never a traceback — and write nothing."""
    home, files = make_home(tmp_path)
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
    before = tree(home)
    raw = subprocess.run([sys.executable, "-m", "taskboard", "--report"], capture_output=True,
                         env=env, cwd=REPO, input=b"\xff\xfe\x80\n", timeout=120)
    assert raw.returncode in (1, 2) and b"Traceback" not in raw.stderr
    long = cli(home, "--report", stdin="7" * 10000 + "\n2\n")
    assert long.returncode == 0 and "Not a choice" in long.stderr and "Traceback" not in long.stderr
    assert reports_in(files, "beta") == [f"deck-{TODAY}.html", f"workspace-{TODAY}.html"]
    assert tree(home) != before                      # the long line did not stop the later `2`
    with pytest.raises(SystemExit) as e:
        entry.ask_board(_entries(tmp_path), _entries(tmp_path)[0], None, Err())
    assert e.value.code == 2
    exact = entry._read_answer(Stream(["1" * 4096 + "\n"], True))
    assert exact == "1" * 4096 + "\n"                  # the newline is not counted
    assert entry._read_answer(Stream(["1" * 4097 + "\n"], True)) == "?\n"
    padded = cli(home, "--report", stdin=" " * 5000 + "2\n1\n")
    assert padded.returncode == 0 and "Not a choice" in padded.stderr      # the cap, observable
    assert reports_in(files, "alpha") != [] and "Traceback" not in padded.stderr


def test_TC_4110_a_corrupt_registry_people_and_marks_are_not_copied_aside(tmp_path):
    """TC-4110 (LLR-4104.2): with a corrupt `boards.json`, `people.json` and `marks.json` the
    run still writes only the reports folder — no `.corrupt` copy under HOME."""
    home, files = make_home(tmp_path)
    root = home / ".taskboard"
    (root / "boards.json").write_text("{not json", encoding="utf-8")
    (root / "people.json").write_text("{not json", encoding="utf-8")
    (root / "marks.json").write_text("{not json", encoding="utf-8")
    before = tree(home)
    r = cli(home, "--board", str(files["alpha"]), "--report", stdin="")
    assert r.returncode == 0, r.stderr
    added = sorted(set(tree(home)) - set(before))
    assert all("reports" in a for a in added), added
    assert not any("corrupt" in a for a in tree(home))


def test_TC_4111_a_reports_path_that_cannot_be_a_folder_exits_1(tmp_path):
    """TC-4111 (LLR-4101.2): a plain file named `reports` beside the board makes the write
    fail: exit 1, one message, no traceback."""
    home, files = make_home(tmp_path)
    (files["alpha"].parent / "reports").write_text("in the way", encoding="utf-8")
    r = cli(home, "--board", str(files["alpha"]), "--report", stdin="")
    assert r.returncode == 1 and "report not written" in r.stderr and "Traceback" not in r.stderr


def test_TC_4112_a_falls_back_when_the_default_board_is_unreadable(tmp_path):
    """TC-4112 (LLR-4102.4): the default board is the one the registry opens, and the
    registry never skips the main board (`~/.taskboard/board.json`) even when its file is
    gone; with it missing, `a` writes into the first readable board's folder."""
    main = tmp_path / "home" / ".taskboard" / "board.json"
    home, files = make_home(tmp_path, boards=(ALPHA, BETA, ("gamma", "Gamma", F.side)),
                            missing=("alpha",), where={"alpha": main})
    r = cli(home, "--report", stdin="a\n")
    assert r.returncode == 0, r.stderr
    assert reports_in(files, "beta") == [f"deck-{TODAY}.html", f"workspace-{TODAY}.html"]
    assert reports_in(files, "gamma") == [] and "1 board skipped" in r.stderr
    assert not main.exists()


def test_TC_4113_a_board_flag_registers_nothing(tmp_path):
    """TC-4113 (LLR-4104.2): `--board` of a file the registry does not list leaves
    `boards.json` byte-identical, and with no registry at all creates no `~/.taskboard`."""
    home, files = make_home(tmp_path)
    other = tmp_path / "other" / "b.json"
    other.parent.mkdir()
    F.personal(other).save()
    before = sha(home / ".taskboard" / "boards.json")
    r = cli(home, "--board", str(other), "--report", stdin="")
    assert r.returncode == 0, r.stderr
    assert sha(home / ".taskboard" / "boards.json") == before
    bare = tmp_path / "bare"
    bare.mkdir()
    r2 = cli(bare, "--board", str(other), "--report", stdin="")
    assert r2.returncode == 0, r2.stderr
    assert tree(bare) == []


def test_TC_4114_a_stdout_that_cannot_spell_the_path_still_prints_it(tmp_path):
    """TC-4114 (LLR-4101.2): a board folder whose name the console codepage cannot spell
    still gets its paths printed (escaped), after the files are written, exit 0."""
    home, files = make_home(tmp_path)
    odd = tmp_path / "ma\u00f1ana"
    odd.mkdir()
    board = odd / "b.json"
    F.personal(board).save()
    r = cli(home, "--board", str(board), "--report", stdin="", io="ascii")
    assert r.returncode == 0, r.stderr
    assert len(lines(r)) == 2 and "\\xf1" in lines(r)[0]
    assert sorted(p.name for p in (odd / "reports").iterdir()) == [f"deck-{TODAY}.html", f"workspace-{TODAY}.html"]

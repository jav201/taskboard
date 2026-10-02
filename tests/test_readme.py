"""The README and RUN.md describe the app as shipped, and leak nothing.

Batch 2026-10-02-batch-01 · HLR-109 · AT-107 · TC-120, TC-121.

Field report (the operator, 2026-09-30): "actualiza el README del repo, está muy
desactualizado y tiene errores y problemas estéticos". The audit
(`README-AUDIT.md`) found the README describing four views of nine, `?` as the
command palette (it is the per-view help), and the operator's personal
absolute path three times; RUN.md documented a retired prototype flow under the
same path. The laws below read the two files and check them against the code —
the views from `VIEW_KEYS`, the help key from `KEYMAP` — so they move when the
app does. (`tests/test_keymap.py` already holds the README's key-table, image
and retired-view laws; this file adds what the audit found missing.)
"""
from __future__ import annotations

import re
from pathlib import Path

from taskboard.app import VIEW_KEYS
from taskboard.keymap import KEYMAP

ROOT = Path(__file__).resolve().parents[1]

#: ONE pattern for a path into somebody's home or personal drive, in every form
#: the security review listed (S-4): `X:\Users\name`, `X:/Users/name`, doubled
#: JSON backslashes, Git-Bash / WSL `/c/Users/name` and `/mnt/c/Users/name`,
#: `/home/name`, `/Users/name`, and the two sync-folder names. Placeholders
#: (`<you>`, `%USERPROFILE%`, `~`) are allowed by construction: the name
#: segment may not start with `<`, `%` or `~`.
HOME_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]+users[\\/]+[^\\/<%~\s`\"']+)"
    r"|(?:(?<!:)\\+users\\+[^\\/<%~\s`\"']+)"
    r"|(?:/(?:mnt/)?c/users/[^/<%~\s`\"']+)"
    r"|(?:(?<![\w.])/home/[^/<%~\s`\"']+)"
    r"|(?:(?<![\w.:])/users/[^/<%~\s`\"']+)"
    r"|onedrive|my drive")


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_the_home_path_pattern_sees_every_form_and_spares_placeholders():
    """Instrument RED-proof for HOME_PATH: each listed form is caught, each
    placeholder is not. Without this a pattern that matched nothing would let
    both laws below pass on a leaking page."""
    for leak in (r"C:\Users\someone\taskboard", "C:/Users/someone/x",
                 r"C:\\Users\\someone\\x", "/c/Users/someone/x",
                 "/mnt/c/Users/someone/x", "/home/someone/x", "/Users/someone/x",
                 r"\Users\someone\x", r"\\host\Users\someone\x",
                 r"D:\OneDrive\x", r"G:\My Drive\x"):
        assert HOME_PATH.search(leak), leak
    for fine in (r"C:\Users\<you>\.taskboard", r"%USERPROFILE%\.taskboard",
                 "~/.taskboard/board.json", "https://github.com/jav201/taskboard.git",
                 "docs/taskboard-gantt.svg"):
        assert not HOME_PATH.search(fine), fine


def test_AT_107_the_readme_carries_no_home_path():
    """AT-107 (HLR-109, LLR-104.1). RED on the base README: the personal path
    three times."""
    hits = [m.group(0) for m in HOME_PATH.finditer(_read("README.md"))]
    assert not hits, f"{len(hits)} home path(s) in README.md"


def test_TC_121_run_md_carries_no_home_path_and_no_retired_flow():
    """TC-121 (LLR-104.2). RUN.md: no home path, no `6` view key, no retired
    prototype worktree flow. RED on the base RUN.md: all three."""
    text = _read("RUN.md")
    hits = [m.group(0) for m in HOME_PATH.finditer(text)]
    assert not hits, f"{len(hits)} home path(s) in RUN.md"
    assert not re.search(r"`6`\s*key|\b6\b[^\n]*(aperture|view)", text, re.I)
    assert "widget_slice" not in text and "worktrees" not in text


def test_TC_120_the_readme_names_every_view_with_its_key():
    """TC-120 (LLR-104.1). Every view in `VIEW_KEYS` has a row in the Views
    table, with its key — derived from the app, never a hand list. A
    PRESERVATION pin: the base README already had the nine rows (qa D-6); the
    base-RED arm for the view count is the next test."""
    rows = {m.group(1): m.group(2) for m in
            re.finditer(r"^\| `(\d)` \| \*\*(\w+)\*\* \|", _read("README.md"), re.M)}
    names = {"swimlanes": "Lanes", "agenda": "Agenda", "gantt": "Gantt",
             "kanban": "Kanban", "focus": "Focus", "flow": "Flow",
             "standup": "Standup", "people": "People", "setup": "Setup"}
    assert len(VIEW_KEYS) == 9
    for key, view in VIEW_KEYS.items():
        assert rows.get(key) == names[view], (key, view, rows)
    assert set(rows) == set(VIEW_KEYS), set(rows) ^ set(VIEW_KEYS)


def test_TC_120_question_mark_is_documented_as_help():
    """TC-120 (audit #5). `?` opens the per-view help — the README says so and
    no longer calls it the command palette."""
    key = next(k for k in KEYMAP if k.keys == "?")
    assert key.action == "legend"
    row = next(l for l in _read("README.md").splitlines() if l.startswith("| `?` |"))
    assert "help" in row.lower() and "palette" not in row.lower(), row


def test_TC_120_the_readme_installs_from_a_clone_and_counts_no_tests():
    """TC-120 (audit #1, #11). Install starts from `git clone` of the public
    repository; the README states no test count (it went stale twice)."""
    text = _read("README.md")
    assert "git clone https://github.com/jav201/taskboard.git" in text
    assert not re.search(r"\b\d{2,5} (Pilot|tests?\b|passed)", text)
    assert "Four switchable views" not in text


def test_TC_120_the_readme_states_the_view_count_from_the_app():
    """TC-120 (qa D-6). The README says how many views there are, in words,
    derived from `VIEW_ORDER`. RED on the base README: "Four switchable views"."""
    from taskboard.app import VIEW_ORDER
    words = {9: "Nine", 10: "Ten", 8: "Eight"}
    assert words[len(VIEW_ORDER)].lower() + " views" in _read("README.md").lower()


def _keys_section() -> list[str]:
    text = _read("README.md")
    assert "\n## Keys\n" in text, "the README has no `## Keys` section"
    body = text.split("\n## Keys\n", 1)[1].split("\n## ", 1)[0]
    return [ln for ln in body.splitlines() if ln.startswith("| `")]


def test_TC_120_every_key_the_readme_documents_is_bound():
    """TC-120 (qa D-5, HLR-109). The other direction of the key-table law in
    `test_keymap.py`: every key the Keys table names is bound — in `KEYMAP` or
    in a modal's `BINDINGS`, derived from the classes, never a hand list. RED:
    a documented key nobody binds (a phantom row). The base README has no
    `## Keys` section, so this node fails there on the missing section."""
    import inspect
    from textual.binding import Binding
    import taskboard.modals as modals
    bound = set()
    for k in KEYMAP:
        bound.update(k.keys.split(","))
    for _n, cls in inspect.getmembers(modals, inspect.isclass):
        for b in getattr(cls, "BINDINGS", None) or []:
            bound.update((b.key if isinstance(b, Binding) else b[0]).split(","))
    spelled = {"↑": "up", "↓": "down", "←": "left", "→": "right", "Enter": "enter",
               "Delete": "delete", "Tab": "tab", "esc": "escape"}
    rows = _keys_section()
    assert len(rows) >= 20, len(rows)
    for row in rows:
        for key in re.findall(r"`([^`]+)`", row.split("|")[1]):
            assert spelled.get(key, key) in bound, f"the README documents {key!r}, which nothing binds"


def test_TC_120_the_facts_the_readme_states_match_the_code():
    """TC-120 (qa D-7). The numbers and names that go stale are compared with
    their source, each derived at run time: the city count, the sweep days,
    the WIP default, the Python floor, the version pins, the CLI flags, the
    default clocks, the default phases and the project colours."""
    import argparse
    import tomllib
    from unittest import mock
    from taskboard import models
    import taskboard.__main__ as entry
    text = _read("README.md")
    assert f"{len(models.CITY_ZONES)} cities" in text
    assert f"{models.AUTO_ARCHIVE_DAYS} days" in text
    assert f"the default is {models.DEFAULT_WIP_LIMITS['Doing']} for `Doing`" in text
    floor = tomllib.loads(_read("pyproject.toml"))["project"]["requires-python"]
    assert floor.lstrip(">=") + " or newer" in text
    pins = dict(re.findall(r"^(textual|rich)==([\d.]+)", _read("requirements.txt"), re.M))
    assert f"Textual {pins['textual']} / rich {pins['rich']}" in text
    flags = []
    real = argparse.ArgumentParser.add_argument

    def spy(self, *names, **kw):
        flags.extend(n for n in names if n.startswith("--") and n != "--help")
        return real(self, *names, **kw)
    with mock.patch.object(argparse.ArgumentParser, "add_argument", spy), \
            mock.patch("sys.argv", ["taskboard", "--help"]), \
            mock.patch("sys.stdout"):
        try:
            entry.main()
        except SystemExit:
            pass
    assert flags and all(f"`taskboard {f}" in text for f in flags), flags
    assert f"default {models.DEFAULT_CLOCK1} and" in text and models.DEFAULT_CLOCK2 in text
    assert "`" + "`, `".join(models.DEFAULT_PHASES) + "`" in text
    assert "(" + ", ".join(models.PROJECT_COLORS) + ")" in text

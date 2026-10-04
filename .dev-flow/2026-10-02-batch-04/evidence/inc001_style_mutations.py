"""Increment 001 (batch 2026-10-02-batch-04), round 2 (review F2): the oracle
control for TC-415 — ONE source mutation per TC-415 arm, each run against the
real node `tests/test_markup_sites.py::test_TC_415_converted_sites_keep_their_painted_style`
in a SCRATCH tree (a `git archive` export with the working tree's `taskboard/`
and `tests/` overlaid — never the live checkout).

    PYTHONIOENCODING=utf-8 python -B <this file> SCRATCH_TREE

Each mutation is located BY POSITION (the one source line whose stripped text
equals an anchor; for the stylesheet, the first matching line after the
`.modal-title {` rule opens) and applied as one in-line substitution that must
occur exactly once on that line. The transcript names the file:line and the
OPERATION in words — never the mangled text (C-56). For each mutation: the
file's sha256 is recorded, the node run once with -rA, the failing arms read
off the node's own assertion message, the file restored and its sha256
re-checked. Verdict per TARGET arm: KILLED when that arm is among the node's
failing arms, SURVIVED otherwise; every SURVIVED arm carries the reason it
cannot go RED. Prints no absolute path.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

NODE = "tests/test_markup_sites.py::test_TC_415_converted_sites_keep_their_painted_style"
LAW = ("phase editor title", "calendar title")
M, CSS = "taskboard/modals.py", "taskboard/taskboard.tcss"
CSS_RULE = ".modal-title {"

# The painted bold of a `.modal-title` row is carried by the stylesheet too.
CSS_BOLD = ("cannot go RED by any single code-side mutation: the stylesheet's "
            "`.modal-title { text-style: bold }` bolds the row anyway; the code's bold "
            "piece is pinned by the '(CSS bold off)' sibling arm")

# (target arm, file, anchor = the stripped source line, old, new, operation in words,
#  reason if it is EXPECTED to survive or None)
DROP_TITLE_BOLD = {
    "details": ('yield Label(Text.assemble((t.title, "bold"), "  —  o open raw · esc close"),',
                '(t.title, "bold")', '(t.title, "")',
                "TaskDetails.compose title row: drop the 'bold' style of the title piece"),
    "viewer": ('Text.assemble((self._view_task.title, "bold"), "  —  o open raw · esc close"),',
               '(self._view_task.title, "bold")', '(self._view_task.title, "")',
               "ImageViewer.compose title row: drop the 'bold' style of the title piece"),
    "prompt": ('yield Label(Text(self._title, style="bold"), classes="modal-title")',
               ', style="bold"', '',
               "TextPrompt.compose title: drop the style='bold' argument"),
    "standup title": ('yield Label(Text(f"Standup · week ending {self._today.isoformat()}", '
                      'style="bold"),', ', style="bold"', '',
                      "StandupModal.compose title: drop the style='bold' argument"),
    "standup project": ('yield Label(Text(f"▐ {name}", style="bold"), classes="modal-title")',
                        ', style="bold"', '',
                        "StandupModal.compose project heading: drop the style='bold' argument"),
    "calendar month": ('return Text.assemble((f"{self._sel:%B %Y}", "bold"),',
                       '"bold"', '""',
                       "CalendarModal._title_text: drop the 'bold' style of the month piece"),
    "help title": ('yield Label(Text(f"Help · {self._mode}", style="bold"), classes="modal-title")',
                   ', style="bold"', '',
                   "HelpModal.compose title: drop the style='bold' argument"),
    "help usage": ('yield Label("[b]Usage[/b]", classes="modal-title")',
                   '"[b]Usage[/b]"', '"Usage"',
                   "HelpModal.compose 'Usage' heading: strip its b tag pair"),
    "help keys": ('yield Label("[b]Keys[/b]", classes="modal-title")',
                  '"[b]Keys[/b]"', '"Keys"',
                  "HelpModal.compose 'Keys' heading: strip its b tag pair"),
}
CSS_OFF = (CSS, "text-style: bold;", "text-style: bold;", "text-style: none;",
           "taskboard.tcss `.modal-title` rule: text-style bold -> none")
TAIL = {
    "details": ('yield Label(Text.assemble((t.title, "bold"), "  —  o open raw · esc close"),',
                '"  —  o open raw · esc close")', '("  —  o open raw · esc close", "bold"))',
                "TaskDetails.compose title row: give the tail piece a 'bold' style"),
    "viewer": ('Text.assemble((self._view_task.title, "bold"), "  —  o open raw · esc close"),',
               '"  —  o open raw · esc close")', '("  —  o open raw · esc close", "bold"))',
               "ImageViewer.compose title row: give the tail piece a 'bold' style"),
}


def _t(arm, spec, why=None, file=M):
    anchor, old, new, op = spec
    return (arm, file, anchor, old, new, op, why)


MUTANTS = [
    _t("details title", DROP_TITLE_BOLD["details"], CSS_BOLD),
    (("details title tail",) + CSS_OFF + (None,)),
    _t("details title (CSS bold off)", DROP_TITLE_BOLD["details"]),
    _t("details title tail (CSS bold off)", TAIL["details"]),
    _t("details — placeholders", ('yield Static("[dim]—[/dim]")', '"[dim]—[/dim]"', '"—"',
                                  "TaskDetails.compose empty-notes placeholder: strip its dim "
                                  "tag pair")),
    _t("viewer title", DROP_TITLE_BOLD["viewer"], CSS_BOLD),
    (("viewer title tail",) + CSS_OFF + (None,)),
    _t("viewer title (CSS bold off)", DROP_TITLE_BOLD["viewer"]),
    _t("viewer title tail (CSS bold off)", TAIL["viewer"]),
    _t("missing: prefix", ('yield Label(Text.assemble(("missing:", "dim"), f" {ref}"))',
                           '("missing:", "dim")', '("missing:", "")',
                           "image_block missing row: drop the 'dim' style of the prefix piece")),
    _t("missing: reference", ('yield Label(Text.assemble(("missing:", "dim"), f" {ref}"))',
                              'f" {ref}"))', '(f" {ref}", "dim")))',
                              "image_block missing row: let a 'dim' style cover the reference")),
    _t("could not render: prefix",
       ('yield Label(Text.assemble(("could not render:", "dim"), f" {ref}"))',
        '("could not render:", "dim")', '("could not render:", "")',
        "image_block could-not-render row: drop the 'dim' style of the prefix piece")),
    _t("could not render: reference",
       ('yield Label(Text.assemble(("could not render:", "dim"), f" {ref}"))',
        'f" {ref}"))', '(f" {ref}", "dim")))',
        "image_block could-not-render row: let a 'dim' style cover the reference")),
    _t("picker: Beta row is off the cursor",
       ("if keep is not None:", "keep is not None", "(keep := keep or projects[1].id) is not None",
        "ProjectPicker._reload: when no row is kept, highlight the second project")),
    _t("picker off-cursor name", ('line = Text.assemble((p.name, "bold"), "  ·  ", p.status)',
                                  '(p.name, "bold")', '(p.name, "")',
                                  "ProjectPicker._project_line: drop the 'bold' style of the "
                                  "name piece")),
    _t("picker off-cursor archived", ('line.append("archived", "dim")', '"dim"', '""',
                                      "ProjectPicker._project_line: drop the 'dim' style of the "
                                      "archived piece")),
    _t("picker off-cursor status (plain)",
       ('line = Text.assemble((p.name, "bold"), "  ·  ", p.status)',
        'p.status)', '(p.status, "dim"))',
        "ProjectPicker._project_line: let a 'dim' style cover the status")),
    _t("phase editor: row 2 is off the cursor",
       ("ol.highlighted = max(0, min(len(phases) - 1, keep or 0))", "keep or 0", "keep or 1",
        "PhaseEditor._reload: default cursor row 0 -> 1")),
    _t("phase editor off-cursor N.",
       ('return Text.assemble((f"{index + 1}.", "dim"), "  ", (name, "bold"),',
        '"dim"', '""', "PhaseEditor._phase_line: drop the 'dim' style of the N. piece")),
    _t("phase editor off-cursor name",
       ('return Text.assemble((f"{index + 1}.", "dim"), "  ", (name, "bold"),',
        '(name, "bold")', '(name, "")',
        "PhaseEditor._phase_line: drop the 'bold' style of the name piece")),
    _t("phase editor off-cursor count (plain)",
       ("f\"  ·  {n} task{'s' if n != 1 else ''}\")",
        "f\"  ·  {n} task{'s' if n != 1 else ''}\")",
        "(f\"  ·  {n} task{'s' if n != 1 else ''}\", \"dim\"))",
        "PhaseEditor._phase_line: let a 'dim' style cover the count")),
    _t("text prompt title", DROP_TITLE_BOLD["prompt"], CSS_BOLD),
    _t("text prompt title (CSS bold off)", DROP_TITLE_BOLD["prompt"]),
    _t("standup title", DROP_TITLE_BOLD["standup title"], CSS_BOLD),
    _t("standup ▐ project", DROP_TITLE_BOLD["standup project"], CSS_BOLD),
    _t("standup title (CSS bold off)", DROP_TITLE_BOLD["standup title"]),
    _t("standup ▐ project (CSS bold off)", DROP_TITLE_BOLD["standup project"]),
    _t("standup phase", ('(task.phase, "dim")))', '"dim"', '""',
                         "StandupModal.compose task row: drop the 'dim' style of the phase "
                         "piece")),
    _t("standup task title (plain)",
       ('yield Label(Text.assemble(f"  {mark} {task.title} ",',
        'f"  {mark} {task.title} ",', '(f"  {mark} {task.title} ", "dim"),',
        "StandupModal.compose task row: let a 'dim' style cover the task title")),
    _t("standup k/n closed", ('"dim")))', '"dim"', '""',
                              "StandupModal.compose k/n closed row: drop its 'dim' style")),
    _t("calendar opened", ("self.app.push_screen(CalendarModal(current or None),",
                           "self.app.push_screen(", "(lambda *a: None)(",
                           "TaskModal._open_calendar: replace the push_screen call with a "
                           "no-op")),
    _t("calendar month", DROP_TITLE_BOLD["calendar month"], CSS_BOLD),
    _t("calendar month (CSS bold off)", DROP_TITLE_BOLD["calendar month"]),
    _t("calendar week header",
       ('grid.append(_WEEK_HEADER, "dim")       # a piece: Text(style=) would dim every day',
        '_WEEK_HEADER, "dim"', '_WEEK_HEADER, ""',
        "CalendarModal._grid_text: drop the 'dim' style of the week header")),
    _t("calendar selected day", ('style = ("bold reverse" if day == d', '"bold reverse"', '"bold"',
                                 "CalendarModal._grid_text: drop 'reverse' from the selected "
                                 "day's style")),
    _t("calendar day in month", ('else "dim" if day.month != d.month else "")',
                                 'else "")', 'else "bold")',
                                 "CalendarModal._grid_text: give in-month days a 'bold' style")),
    _t("calendar days outside the month",
       ('else "dim" if day.month != d.month else "")', 'else "dim" if', 'else "" if',
        "CalendarModal._grid_text: drop the 'dim' style of out-of-month days")),
    _t("help title", DROP_TITLE_BOLD["help title"], CSS_BOLD),
    _t("help Usage heading", DROP_TITLE_BOLD["help usage"], CSS_BOLD),
    _t("help Keys heading", DROP_TITLE_BOLD["help keys"], CSS_BOLD),
    _t("help usage section heading", ('yield Label(Text(heading, style="underline"))',
                                      ', style="underline"', '',
                                      "HelpModal.compose usage heading: drop the "
                                      "style='underline' argument")),
    _t("help example meaning", ('yield Label(Text(example_meaning, style="dim"))',
                                ', style="dim"', '',
                                "HelpModal.compose example meaning: drop the style='dim' "
                                "argument")),
    _t("help usage bullet (plain)", ('yield Label(Text(f"  • {bullet}"))',
                                     'Text(f"  • {bullet}")', 'Text(f"  • {bullet}", style="dim")',
                                     "HelpModal.compose usage bullet: give it a 'dim' style")),
    _t("help title (CSS bold off)", DROP_TITLE_BOLD["help title"]),
    _t("help Usage heading (CSS bold off)", DROP_TITLE_BOLD["help usage"]),
    _t("help Keys heading (CSS bold off)", DROP_TITLE_BOLD["help keys"]),
    _t("details highlight", ("yield Static(notes_preview(t.notes))", "notes_preview(t.notes)",
                             "Text(t.notes)",
                             "TaskDetails.compose notes: build them as plain Text instead of "
                             "through the shared tokeniser")),
    _t("preview typed", ('yield TextArea(t.notes if t else "", id="f-notes")',
                         'id="f-notes")', 'id="f-notes", read_only=True)',
                         "TaskModal.compose notes editor: make the TextArea read-only")),
    _t("preview highlight", ("notes_preview(event.text_area.text))", "notes_preview(", "Text(",
                             "TaskModal.on_text_area_changed: rebuild the preview as plain Text "
                             "instead of through the shared tokeniser")),
    _t("phase editor title",
       ('"\\\\[ / ] reorder · esc close", classes="modal-title")', '"\\\\[', '"\\\\\\\\[',
        "PhaseEditor.compose title: double the backslash that escapes the reorder key "
        "hint's opening bracket (an escape applied twice). Deleting it instead is NOT a "
        "fault: Textual 8.2.8 reads `[ / ]` as text, not a tag — measured in round 2, "
        "that deletion leaves the node GREEN and the row painted the same")),
    _t("calendar title",
       ('"  —  ←→ day · ↑↓ week · [ ] month · t today · enter pick")', "[ ] month",
        "\\\\[ ] month",
        "CalendarModal._title_text: insert an escaping backslash before the month key hint")),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def locate(lines: list[str], file: str, anchor: str, old: str) -> int:
    if file == CSS:                      # the first `old` line inside the .modal-title rule
        start = [i for i, ln in enumerate(lines) if ln.strip() == CSS_RULE]
        assert len(start) == 1, "stylesheet rule not unique / absent"
        hits = [i for i in range(start[0] + 1, start[0] + 5) if lines[i].strip() == anchor]
        assert hits, "rule property absent"
        return hits[0]
    hits = [i for i, ln in enumerate(lines) if ln.strip() == anchor]
    assert len(hits) == 1, f"anchor not unique / absent ({len(hits)})"
    return hits[0]


def main() -> None:
    tree = Path(sys.argv[1]).resolve()
    assert not (tree / ".git").exists(), "refusing: this is a git checkout, not a scratch export"
    sys.path.insert(0, str(tree / "tests"))
    sys.path.insert(0, str(tree))
    from test_markup_sites import STYLE_BASE      # the node's own arm list
    arms = list(STYLE_BASE) + list(LAW)
    targets = [m[0] for m in MUTANTS]
    assert sorted(targets) == sorted(arms), (
        "one mutation per arm: missing " + repr(sorted(set(arms) - set(targets)))
        + " extra " + repr(sorted(set(targets) - set(arms))))
    print(f"node: {NODE}")
    print(f"arms: {len(arms)} ({len(STYLE_BASE)} STYLE_BASE + {len(LAW)} law); "
          f"mutants: {len(MUTANTS)}, one per arm")
    verdicts = []
    for k, (arm, file, anchor, old, new, op, why) in enumerate(MUTANTS, 1):
        f = tree / file
        raw = f.read_bytes()
        before = sha(f)
        lines = raw.decode("utf-8").splitlines(keepends=True)
        i = locate(lines, file, anchor, old)
        assert lines[i].count(old) == 1, (arm, "operation site not unique on its line")
        lines[i] = lines[i].replace(old, new)
        f.write_bytes("".join(lines).encode("utf-8"))
        assert sha(f) != before, (arm, "mutation did not apply")
        out = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p",
                              "no:cacheprovider", "-rA", NODE], cwd=tree, capture_output=True,
                             env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
                             encoding="utf-8", errors="replace").stdout
        f.write_bytes(raw)
        restored = sha(f) == before
        outcome = next((ln.split()[0] for ln in out.splitlines()
                        if ln.startswith(("PASSED ", "FAILED ", "ERROR "))), "NO-RESULT")
        msg = [re.sub(r"^E\s+", "", ln) for ln in out.splitlines() if ln.startswith("E ")]
        red = [a for a in arms if any(m.startswith(f"{a}: ") for m in msg)]
        crashed = outcome != "PASSED" and not red
        status = "KILLED" if (arm in red or crashed) else "SURVIVED"
        verdicts.append((arm, status, why))
        print(f"\n[{k:02d}] arm: {arm}")
        print(f"     mutation: {file}:{i + 1} — {op}")
        print(f"     node {outcome}; red arms ({len(red)}): {red if red else '-'}"
              + ("; node failed without an arm message (crash)" if crashed else ""))
        print(f"     verdict: {status}"
              + (f" — expected: {why}" if status == "SURVIVED" and why else "")
              + (" — UNEXPECTED (no reason recorded)" if status == "SURVIVED" and not why
                 else ""))
        print(f"     restore sha256 {before[:16]}… {'OK' if restored else 'MISMATCH'}")
        assert restored
    killed = [a for a, s, _ in verdicts if s == "KILLED"]
    survived = [(a, w) for a, s, w in verdicts if s == "SURVIVED"]
    print(f"\nSUMMARY: {len(killed)} of {len(verdicts)} arms KILLED, {len(survived)} SURVIVED")
    for a, w in survived:
        print(f"  SURVIVED {a}: {w or 'UNEXPECTED'}")


if __name__ == "__main__":
    main()

"""Mutation harness of batch 2026-10-19-batch-01.

    python .dev-flow/2026-10-19-batch-01/evidence/mutate.py <increment>   (from the repo root, NO_COLOR unset)

Each mutant replaces one exact source snippet (it must occur exactly once), runs
the named test selection, and restores the file byte for byte (the restore digest
is checked against the digest taken before). KILLED = the selection fails on the
mutant; SURVIVED = it passes. A pre-check refuses to run on a red tree."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

MUTANTS = {
    "001": [
        ("M1 the milestone branch removed (the bar returns)", "taskboard/views.py",
         "    if task.milestone:\n        tone = milestone_tone(task, board, p.today)",
         "    if False:\n        tone = milestone_tone(task, board, p.today)",
         ["tests/test_present_milestone.py"]),
        ("M2 the chip keeps the start date", "taskboard/views.py",
         "chip = \" \" + _present_chip(None, task.due_date, p.today, p.chip_w)",
         "chip = \" \" + _present_chip(task.start_date, task.due_date, p.today, p.chip_w)",
         ["tests/test_present_milestone.py"]),
        ("M3 the cursor's ◆ not accented", "taskboard/views.py",
         "        if cursor:\n            cells = [(\"◆\", \"accent\")",
         "        if False:\n            cells = [(\"◆\", \"accent\")",
         ["tests/test_present_milestone.py"]),
        ("M4 the label's ◆ dropped", "taskboard/views.py",
         "c(\"▎\", p.hue) + \" \" + c(\"◆\", tone) + \" \"",
         "c(\"▎\", p.hue) + \" \" + c(\" \", tone) + \" \"",
         ["tests/test_present_milestone.py"]),
        ("M5 the cursor's ⟦ lead never drawn (code review F1)", "taskboard/views.py",
         "lead = c(\"⟦\", \"accent\", bold=True) if cursor else \" \"",
         "lead = \" \"",
         ["tests/test_present_milestone.py"]),
    ],
    "002": [
        ("N1 a boolean accepted as a rank", "taskboard/models.py",
         "and not isinstance(rank, bool) else None", "else None",
         ["tests/test_present_all.py"]),
        ("N2 a None rank written", "taskboard/models.py",
         "if \"present_rank\" in d and d[\"present_rank\"] is None:",
         "if False:",
         ["tests/test_present_all.py"]),
        ("N3 the shown flag read truthy (0 hides)", "taskboard/models.py",
         "show_in_present=d.get(\"show_in_present\") is not False,\n            present_rank=",
         "show_in_present=bool(d.get(\"show_in_present\", True)),\n            present_rank=",
         ["tests/test_present_all.py"]),
        ("N4 the unranked sorted first", "taskboard/models.py",
         "key=lambda p: (p.present_rank is None,", "key=lambda p: (p.present_rank is not None,",
         ["tests/test_present_all.py"]),
        ("N5 the team pull keeps the keys", "taskboard/team_sync.py",
         "if k not in (\"show_in_present\",", "if k not in (\"x\",",
         ["tests/test_present_all.py"]),
        ("N6 the ranks not from 0", "taskboard/models.py",
         "board.project_by_id(pid).present_rank = i", "board.project_by_id(pid).present_rank = i + 1",
         ["tests/test_present_all.py"]),
    ],
    "003": [
        ("P1 the rail drawn below 100 columns", "taskboard/views.py",
         "    if width < PRESENT_RAIL_MIN:\n        lines, stops, drawn", "    if width < 60:\n        lines, stops, drawn",
         ["tests/test_present_all.py"]),
        ("P2 hidden projects reach the timeline", "taskboard/views.py",
         "for p in present_order(board) if p.show_in_present]", "for p in present_order(board)]",
         ["tests/test_present_all.py"]),
        ("P3 the auto-fold may fold the cursor's project", "taskboard/views.py",
         "if p.id != cur_pid and open_[p.id] and ts:", "if open_[p.id] and ts:",
         ["tests/test_present_all.py"]),
        ("P4 the order ignores present_rank", "taskboard/views.py",
         "return [(p, present_tasks(board, p.id)[0]) for p in present_order(board) if p.show_in_present]",
         "return [(p, present_tasks(board, p.id)[0]) for p in board.visible_projects(False) if p.show_in_present]",
         ["tests/test_present_all.py"]),
        ("P5 the rail's name loses its escape (PC-2)", "taskboard/views.py",
         "name = c(escape(fit(p.name, rw - 8)), tone, bold=on)", "name = c(fit(p.name, rw - 8), tone, bold=on)",
         ["tests/test_present_all.py"]),
        ("P6 the header's name loses its escape (PC-2)", "taskboard/views.py",
         "body = c(escape(fit(p.name, max(0, name_w))),", "body = c(fit(p.name, max(0, name_w)),",
         ["tests/test_present_all.py"]),
        ("P7 a hidden project's own hidden tasks dropped from u", "taskboard/views.py",
         "rows += [(\"task\", t.id, 1) for t in tasks]", "rows += [(\"task\", t.id, 1) for t in tasks if p.show_in_present]",
         ["tests/test_present_all.py"]),
        ("P8 u lists shown tasks too", "taskboard/views.py",
         "return [(\"task\", t.id, 0) for t in present_hidden(board, project_id)]",
         "return [(\"task\", t.id, 0) for t in present_tasks(board, project_id)[1]]",
         ["tests/test_present_all.py"]),
    ],
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(tests: list[str]) -> int:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                           "--color=no", *tests], cwd=ROOT, capture_output=True).returncode


def main(inc: str) -> int:
    muts = MUTANTS[inc]
    selection = sorted({t for *_, ts in muts for t in ts})
    pre = _run(selection)
    print(f"pre-check: {' '.join(selection)} -> exit {pre}")
    if pre != 0:
        print("REFUSED: the selection is red before any mutation")
        return 2
    killed = 0
    for name, rel, old, new, tests in muts:
        path = ROOT / rel
        before = _digest(path)
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"
        o, n = old.replace("\n", nl), new.replace("\n", nl)
        assert text.count(o) == 1, (name, text.count(o))
        try:
            path.write_bytes(text.replace(o, n).encode("utf-8"))
            code = _run(tests)
        finally:
            path.write_bytes(raw)
        assert _digest(path) == before, name
        verdict = "KILLED" if code != 0 else "SURVIVED"
        killed += code != 0
        print(f"{name} · {rel} · {' '.join(tests)} -> exit {code} · {verdict} · restore digest {before}")
    print(f"{killed}/{len(muts)} KILLED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

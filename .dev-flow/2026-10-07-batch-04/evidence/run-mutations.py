"""Mutation battery + RED counterfactual for batch-2026-10-07-batch-04 increment 001.

Each mutation: hash before -> apply -> run the targeted node -> verdict ->
restore -> hash after (must equal before). Transcript goes to stdout.
Run from the worktree root with the suite env; PYTHONDONTWRITEBYTECODE=1.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("C:/Users/jjgh8/Github/taskboard/.claude/worktrees/present-e")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(node: str) -> tuple[int, str]:
    cmd = ["python", "-m", "pytest", node, "-q", "-x", "--no-header",
           "-p", "no:cacheprovider"]
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    env.update({"TERM": "xterm-256color", "COLORTERM": "truecolor",
                "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    tail = "\n".join((r.stdout + r.stderr).splitlines()[-6:])
    return r.returncode, tail


VIEWS = ROOT / "taskboard" / "views.py"
APP = ROOT / "taskboard" / "app.py"

MUTS = [
    ("M1", VIEWS,
     '    return c(title_markup(task, max(0, width), False), "bright", bold=True)',
     '    return c(task.title, "bright", bold=True)  # MUTATION M1: no escape/clip',
     ["tests/test_present.py::test_TC_1003_a_hostile_title_and_notes_render_escaped"]),
    ("M2", VIEWS,
     "            for x in range(lo, hi + 1):          # the echo `⟦━⟧`: heavy fill in focus",
     "            for x in range(0):          # MUTATION M2: no cursor echo",
     ["tests/test_present.py::test_TC_1001_the_exact_presc_frame_at_118x30"]),
    ("M3", APP,
     "        if project_id is None:",
     "        if project_id is not None:  # MUTATION M3: the screen never opens",
     ["tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle",
      "tests/test_report.py::test_pressing_R_opens_the_presentation_read_only"]),
    ("M4", APP,
     "        self._cursor_id = ids[max(0, min(len(ids) - 1, i + delta))]",
     "        self._cursor_id = ids[max(0, min(len(ids) - 1, i - delta))]  # MUTATION M4: reversed",
     ["tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle"]),
    ("M5", APP,
     "        save_present_svg(text, svg_path, w, h)",
     "        svg_path = svg_path  # MUTATION M5: the SVG write skipped",
     ["tests/test_present.py::test_AT_1001_R_presents_the_project_and_the_frame_is_the_oracle"]),
    ("M6", VIEWS,
     "        return Text.from_markup(markup, emoji=False).plain",
     '        return re.sub(r"\\[/?[^\\]]*\\]", "", markup)  # MUTATION M6: the regex measure back',
     ["tests/test_present.py::test_TC_1003_a_hostile_title_and_notes_render_escaped"]),
]

for name, path, old, new, nodes in MUTS:
    src = path.read_text(encoding="utf-8")
    before = sha(path)
    print(f"\n===== {name} on {path.name} =====")
    print(f"sha256 before: {before}")
    if src.count(old) != 1:
        print(f"BAD: anchor not unique/found ({src.count(old)}) — mutation skipped")
        continue
    path.write_text(src.replace(old, new), encoding="utf-8")
    for node in nodes:
        try:
            code, tail = run(node)
        except subprocess.TimeoutExpired:
            print(f"{node}: CRASH (timeout)")
            continue
        status = "KILLED" if code else "SURVIVED"
        print(f"{node}: {status} (exit {code})")
        if code:
            print("  " + tail.replace("\n", "\n  "))
    after = sha(path)
    path.write_text(src, encoding="utf-8")  # restore
    restored = sha(path)
    print(f"sha256 restored: {restored}  {'OK' if restored == before else 'MISMATCH!'}")
print("\n===== battery done =====")

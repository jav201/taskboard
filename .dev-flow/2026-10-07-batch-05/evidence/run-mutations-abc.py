"""Mutation battery for batch-05 increments 001/002/004.

Each mutation: hash before -> apply -> run the targeted node (or probe) ->
verdict -> restore -> hash after (must equal before). Transcript to stdout.
Run from the repo root with the suite env; PYTHONDONTWRITEBYTECODE=1.
"""
import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path("C:/Users/jjgh8/Github/taskboard")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(args) -> tuple[int, str]:
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    env.update({"TERM": "xterm-256color", "COLORTERM": "truecolor",
                "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    r = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    tail = "\n".join((r.stdout + r.stderr).splitlines()[-6:])
    return r.returncode, tail


MODELS = ROOT / "taskboard" / "models.py"
APP = ROOT / "taskboard" / "app.py"
MODALS = ROOT / "taskboard" / "modals.py"
TM = ROOT / "tests" / "test_milestones.py"

MUTS = [
    ("M1", MODELS,
     "                    try:\n                        p.unlink(missing_ok=True)\n                    except OSError:\n                        pass\n",
     "                    # MUTATION M1: no unlink\n",
     ["python", "-m", "pytest",
      "tests/test_backup_write.py::test_failed_write_leaves_no_partial_file",
      "-q", "-x", "--no-header", "-p", "no:cacheprovider"]),
    ("M2", MODELS,
     "                    try:\n                        p.unlink(missing_ok=True)\n                    except OSError:\n                        pass\n",
     "                    p.unlink(missing_ok=True)  # MUTATION M2: the guard removed\n",
     ["python", "-m", "pytest",
      "tests/test_backup_write.py::test_refusing_unlink_never_masks_the_write_error",
      "-q", "-x", "--no-header", "-p", "no:cacheprovider"]),
    ("M3", APP,
     '            self.notify(f"Undone — {task.title} is back as it was.", title="Undo", severity="information", markup=False)\n',
     "            # MUTATION M3: no undo toast\n",
     ["python", "-m", "pytest", "tests/test_undo_toast.py",
      "-q", "-x", "--no-header", "-p", "no:cacheprovider"]),
    ("M4", MODALS,
     "    if cell_len(s) <= width:\n        return s\n",
     "    if True:  # MUTATION M4: never clip\n        return s\n",
     ["python", "-m", "pytest", "tests/test_help_clip.py",
      "-q", "-x", "--no-header", "-p", "no:cacheprovider"]),
]

for name, path, old, new, cmd in MUTS:
    src = path.read_text(encoding="utf-8")
    before = sha(path)
    print(f"\n===== {name} on {path.name} =====")
    print(f"sha256 before: {before}")
    if src.count(old) != 1:
        print(f"BAD: anchor not unique/found ({src.count(old)}) — mutation skipped")
        continue
    path.write_text(src.replace(old, new), encoding="utf-8")
    try:
        code, tail = run(cmd)
    except subprocess.TimeoutExpired:
        print(f"{cmd[-4]}: CRASH (timeout)")
        continue
    status = "KILLED" if code else "SURVIVED"
    print(f"{' '.join(cmd[2:])}: {status} (exit {code})")
    if code:
        print("  " + tail.replace("\n", "\n  "))
    after = sha(path)
    path.write_text(src, encoding="utf-8")
    restored = sha(path)
    print(f"sha256 restored: {restored}  {'OK' if restored == before else 'MISMATCH!'}")

# M5 — the planted-assignment probe for increment 004 (grep pin as a probe)
print(f"\n===== M5 on {TM.name} (planted assignment; grep probe) =====")
src = TM.read_text(encoding="utf-8")
before = sha(TM)
anchor = "def test_AT_601_a_task_becomes_a_milestone_saved_undoable_said_and_pushed"
if anchor not in src:
    print("BAD: AT-601 anchor missing")
else:
    planted = src.replace(anchor, anchor, 1).replace(
        "        # MUTATION-M5-RESTORE-MARKER", "", 1)  # no-op guard
    first = src.index(anchor)
    line_end = src.index("\n", first) + 1
    mutated = src[:line_end] + "    app.selected_task_id = 'ta1'  # MUTATION M5\n" + src[line_end:]
    TM.write_text(mutated, encoding="utf-8")
    code, tail = run(["grep", "-n", "selected_task_id =", str(TM.relative_to(ROOT))])
    print(f"grep probe exit {code} (non-zero => a direct assignment is visible => pin fires):")
    print("  " + tail.replace("\n", "\n  "))
    TM.write_text(src, encoding="utf-8")
    restored = sha(TM)
    print(f"sha256 restored: {restored}  {'OK' if restored == before else 'MISMATCH!'}")
print("\n===== battery done =====")

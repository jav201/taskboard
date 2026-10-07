"""M4 per-node re-run — increment 002's clip mutation, both arms resolved.

The stored battery ran M4 with -x (`1 failed, 1 passed` — mutations-abc.log):
the first-failing node reddens and the sibling is never reported. This re-run
plants the same mutation (`if True: return s` at the head of _clip_words) and
runs BOTH test_help_clip nodes without -x, so the verdict table can name the
per-arm RED truthfully. Binary mode: the restore digest matches exactly.
"""
import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path("C:/Users/jjgh8/Github/taskboard")
MODALS = ROOT / "taskboard" / "modals.py"

OLD_LF = b"    if cell_len(s) <= width:\n        return s\n"
NEW_LF = b"    if True:  # MUTATION M4 (re-run): never clip\n        return s\n"
# the text-mode restores left CRLF in the shipped region (mixed endings, cosmetic)
OLD = OLD_LF.replace(b"\n", b"\r\n")
NEW = NEW_LF.replace(b"\n", b"\r\n")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


before = sha(MODALS)
src = MODALS.read_bytes()
print(f"sha256 before: {before}")
if src.count(OLD) != 1:
    OLD, NEW = OLD_LF, NEW_LF
n = src.count(OLD)
print(f"anchor count: {n}")
assert n == 1, "anchor must apply exactly once"
MODALS.write_bytes(src.replace(OLD, NEW))
env = dict(os.environ)
env.pop("NO_COLOR", None)
env.update({"TERM": "xterm-256color", "COLORTERM": "truecolor",
            "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
try:
    r = subprocess.run(["python", "-m", "pytest", "tests/test_help_clip.py",
                        "-q", "--no-header", "-p", "no:cacheprovider", "-rf"],
                       cwd=ROOT, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    lines = [l for l in (r.stdout + r.stderr).splitlines()
             if any(k in l for k in ("FAILED", "failed", "passed", "assert", "Error"))]
    print("pytest tests/test_help_clip.py -q (both arms, no -x, -rf):")
    print("  " + "\n  ".join(lines[-8:]))
    print(f"exit {r.returncode} -> {'KILLED' if r.returncode else 'SURVIVED'}")
finally:
    MODALS.write_bytes(src)
    restored = sha(MODALS)
    print(f"sha256 restored: {restored}  {'OK' if restored == before else 'MISMATCH!'}")

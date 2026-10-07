"""M3 clean re-run — increment 002's undo-toast mutation with the corrected anchor.

The stored battery (run-mutations-abc.py / mutations-abc.log) planted M3 with a
ONE-LINE anchor:
    self.notify(f"Undone — {task.title} is back as it was.", title="Undo", severity="information", markup=False)
but the shipped call is TWO lines (app.py:1468-1469), so the anchor matched 0
times: BAD — mutation skipped (mutations-abc.log §M3). This re-run plants the
same mutation against the true two-line anchor, runs BOTH test_undo_toast nodes
(no -x, per-node granularity), and restores byte-exact (binary mode, so the
restore digest matches the pre-mutation hash — the text-mode LF normalization
that left M1/M4/M5's restores cosmetically MISMATCHed cannot happen here).
"""
import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path("C:/Users/jjgh8/Github/taskboard")
APP = ROOT / "taskboard" / "app.py"

OLD_LF = (b'            self.notify(f"Undone \xe2\x80\x94 {task.title} is back as it was.",\n'
          b'                        title="Undo", severity="information", markup=False)\n')
NEW_LF = b'            # MUTATION M3 (re-run): no undo toast\n'
# the text-mode restores left CRLF in the shipped region (mixed endings, cosmetic)
OLD = OLD_LF.replace(b"\n", b"\r\n") if OLD_LF.replace(b"\n", b"\r\n") else OLD_LF
NEW = NEW_LF.replace(b"\n", b"\r\n")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


before = sha(APP)
src = APP.read_bytes()
print(f"sha256 before: {before}")
if src.count(OLD) != 1:
    OLD, NEW = OLD_LF, NEW_LF
n = src.count(OLD)
print(f"two-line anchor count: {n} (the stored run's one-line anchor counted 0 — mutations-abc.log)")
assert n == 1, "anchor must apply exactly once"
APP.write_bytes(src.replace(OLD, NEW))
env = dict(os.environ)
env.pop("NO_COLOR", None)
env.update({"TERM": "xterm-256color", "COLORTERM": "truecolor",
            "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
try:
    r = subprocess.run(["python", "-m", "pytest", "tests/test_undo_toast.py",
                        "-q", "--no-header", "-p", "no:cacheprovider", "-rf"],
                       cwd=ROOT, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    lines = [l for l in (r.stdout + r.stderr).splitlines()
             if any(k in l for k in ("FAILED", "failed", "passed", "assert", "Error"))]
    print("pytest tests/test_undo_toast.py -q (both arms, no -x, -rf):")
    print("  " + "\n  ".join(lines[-8:]))
    print(f"exit {r.returncode} -> {'KILLED' if r.returncode else 'SURVIVED'}")
finally:
    APP.write_bytes(src)
    restored = sha(APP)
    print(f"sha256 restored: {restored}  {'OK' if restored == before else 'MISMATCH!'}")

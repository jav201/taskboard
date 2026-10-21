"""Mutation battery of increment 002 (batch 2026-10-20-batch-02), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_present_all.py::"
H = "tests/test_hygiene.py::"
M = "taskboard/modals.py"
ARMS = [
    ("N1 the rank kept on a tie", M, "            if proj.present_rank in ranks:", "            if False:",
     T + "test_TC_2304_the_unarchive_rank_rule"),
    ("N1b the rank kept on a tie (AT)", M, "            if proj.present_rank in ranks:", "            if False:",
     T + "test_AT_2304_an_unarchived_project_never_ties_a_rank"),
    ("N2 always re-ranked (ux UX-1)", M, "            if proj.present_rank in ranks:", "            if True:",
     T + "test_TC_2304_the_unarchive_rank_rule"),
    ("N3 archived projects' ranks counted", M,
     "            ranks = [p.present_rank for p in self.board.visible_projects(False)",
     "            ranks = [p.present_rank for p in self.board.projects",
     T + "test_TC_2304_the_unarchive_rank_rule"),
    ("N4 its own rank counted", M,
     "                     if p is not proj and p.present_rank is not None]",
     "                     if p.present_rank is not None]",
     T + "test_TC_2304_the_unarchive_rank_rule"),
    ("N5 the unused parameter back", M,
     "    def _move_target(self, proj: Project, bid: str | None) -> None:",
     "    def _move_target(self, proj: Project, bid: str | None, _boards: dict | None = None) -> None:",
     H + "test_TC_2306_move_target_takes_the_project_and_the_board"),
]
print("arms:", len(ARMS), flush=True)
bad = 0
env = dict(os.environ, PY_COLORS="0", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
env.pop("NO_COLOR", None)
for label, path, old, new, node in ARMS:
    f = pathlib.Path(path)
    src = f.read_bytes()
    text = src.decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    o, n = old.replace("\n", nl), new.replace("\n", nl)
    h0 = hashlib.sha256(src).hexdigest()
    if text.count(o) != 1:
        print(f"{label}: BAD (anchor found {text.count(o)} times)", flush=True)
        bad += 1
        continue
    try:
        f.write_bytes(text.replace(o, n, 1).encode("utf-8"))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--color=no", node], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=300)
    finally:
        f.write_bytes(src)
    h1 = hashlib.sha256(f.read_bytes()).hexdigest()
    assert h1 == h0, "the restore is not proven"
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    bad += verdict != "RED (KILLED)"
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"{label} · {path} · {node.split('::')[1]}: {verdict or 'CRASH/BAD (exit %d)' % r.returncode}"
          f" · sha256 {h0[:12]} restored · {tail}", flush=True)
print("not killed:", bad)
sys.exit(1 if bad else 0)

"""Mutation battery of increment 003 (tests only: each hardened node against a shipped-code or test-file edit it must catch) (batch 2026-10-20-batch-02), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_present_all.py::"
H = "tests/test_boards_home.py::"
L = "tests/test_hygiene.py::test_AT_2306_the_hygiene_law"
ARMS = [
    ("H1 B left out of the help's keys (the word kept)", "taskboard/modals.py",
     "band = keys_grid([f\"{k.show:<3} {k.label}\" for k in bar_keys(self._mode)], width)",
     "band = keys_grid([f\"{'' if k.action == 'boards' else k.show:<3} {k.label}\" for k in bar_keys(self._mode)], width)",
     H + "test_AT_2204_the_home"),
    ("H2 the cursor's echo on every other row", "taskboard/views.py",
     "    if not on:\n        return cells\n    xs = [x for x, (gl, _) in enumerate(cells) if gl != \" \"]",
     "    if on:\n        return cells\n    xs = [x for x, (gl, _) in enumerate(cells) if gl != \" \"]",
     T + "test_AT_2104_three_views_one_cursor_and_the_export"),
    ("H3 u inert in view 2", "taskboard/app.py",
     "        if self._narrow():\n            return\n        rows = present_hidden_rows(",
     "        if self._narrow() or self._view == 1:\n            return\n        rows = present_hidden_rows(",
     T + "test_AT_2106_u_lists_the_hidden_and_brings_one_back"),
    ("H4 the rail's cursor on the next row", "taskboard/views.py",
     "        on = p.id == cur_pid\n        mark = c(",
     "        on = i > 0 and ps[i - 1].id == cur_pid\n        mark = c(",
     T + "test_AT_2102_the_order_and_hidden_projects_survive_a_restart"),
    ("H5 PAYLOADS back in test_boards_forms", "tests/test_boards_forms.py",
     "SETTINGS = {", "PAYLOADS = [\"x\"]\nSETTINGS = {", L),
    ("H6 the private border title read again", "tests/test_boards_forms.py",
     "        assert Text.from_markup(card.border_title).plain == \"▶ \" + payload   # the public title",
     "        assert card._border_title.plain == \"▶ \" + payload   # the public title", L),
    ("H7 _move_target's unused parameter back", "taskboard/modals.py",
     "    def _move_target(self, proj: Project, bid: str | None) -> None:",
     "    def _move_target(self, proj: Project, bid: str | None, _boards: dict | None = None) -> None:", L),
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

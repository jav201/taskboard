"""Mutation battery — increment 002 (2026-10-24-batch-02).

One node per run; exit 1 = RED (KILLED), 0 = GREEN (SURVIVED), else CRASH/BAD.
Every arm restores the mutated file and proves the restore by hash. Run from
the project root:
    env -u NO_COLOR python .dev-flow/2026-10-24-batch-02/evidence/mutation-002.py
"""
import hashlib
import itertools
import os
import pathlib
import subprocess
import sys

CASES = [
    # (file, anchor, replacement) — the PDR §5 / C4 named mutations
    ("taskboard/people.py", b"        if stamp == self._stamp:\r\n            return None",
     b"        if False:\r\n            return None"),                       # E1: no gate, re-parse always
    ("taskboard/people.py", b"            stamp = (stat.st_mtime_ns, stat.st_size)",
     b"            stamp = (stat.st_mtime_ns, 0)"),                   # E2: the size arm dropped
    ("taskboard/people.py", b"        if people is None:\r\n            return False",
     b"        if people is None:\r\n            self.people.clear()\r\n            return False"),  # E3: failure empties
    ("taskboard/people.py", b"        self._stamp = stamp                 # a bad file is not re-parsed and re-reported on every open\r\n        if people is None:",
     b"        if people is not None:\r\n            self._stamp = stamp\r\n        if people is None:"),  # E4: no stamp advance on failure
    ("taskboard/app.py", b"            if directory.refresh() is False:",
     b"            if False:"),                                       # E5: the seats never refresh
    ("taskboard/modals.py", b"        self._directory_queried = True\r\n        if self._on_directory_query is not None:",
     b"        if self._on_directory_query is not None:"),            # E6: the callback fires on every keystroke
]
NODES = [
    "tests/test_directory_refresh.py::test_TC_2701_refresh_gates_on_mtime_or_size",
    "tests/test_directory_refresh.py::test_TC_2702_a_failed_refresh_keeps_and_flags_once",
    "tests/test_directory_refresh.py::test_AT_2706_the_directories_stay_fresh",
    "tests/test_directory_refresh.py::test_AT_2707_a_failed_re_read_keeps_the_directory",
    "tests/test_directory_refresh.py::test_D3_the_search_query_refreshes_the_directories_once",
]
arms = len(CASES) * len(NODES)
print("arms:", arms)
bad = 0
for (fname, old, new), node in itertools.product(CASES, NODES):
    f = pathlib.Path(fname)
    src = f.read_bytes()
    h0 = hashlib.sha256(src).hexdigest()
    print("before:", fname, h0, flush=True)
    arm = "%s @ %s [%s]" % (node, fname, old.decode().strip().replace("\n", "\\n")[:44])
    try:
        if old not in src:
            print(arm + ": BAD (anchor not found)")
            sys.exit(1)
        f.write_bytes(src.replace(old, new, 1))
        if hashlib.sha256(f.read_bytes()).hexdigest() == h0:
            print(arm + ": BAD (the edit did not apply)")
            sys.exit(1)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--color=no", node], env=dict(os.environ, PY_COLORS="0"))
    finally:
        f.write_bytes(src)
    h1 = hashlib.sha256(f.read_bytes()).hexdigest()
    print("after: ", h1)
    assert h1 == h0, "the restore is not proven"
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    bad += verdict is None
    print(arm + ":", verdict or "CRASH/BAD (exit %d)" % r.returncode, flush=True)
sys.exit(1 if bad else 0)

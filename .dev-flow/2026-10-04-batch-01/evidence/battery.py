"""Mutation battery for batch 2026-10-04-batch-01 — runs in a scratch EXPORT, never
in the working tree (C-40: no other session reads it).

    python -B battery.py SPEC.json OUT.txt

SPEC: {"export": <dir>, "mutants": [{"id", "file", "old", "new", "tests": [pytest args]}]}.
The export is `git archive HEAD` overlaid with the working tree's `taskboard/` and
`tests/` (made by the caller). Per mutant: hash the file, apply the replacement
byte-exactly (anchors follow the file's own line endings; refused when `old` is not
found exactly once — a BAD anchor), run the named tests with `-rA`, record the
verdict PER NODE, restore the original bytes and check the hash returns.

Revision history: r1 read and wrote text with newline translation, so a restore
could change a file's line endings (increment 003's P1 `MISMATCH`); since then
bytes in, bytes out."""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

CRLF, LF = "\r\n", "\n"
spec = __import__("json").loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out_lines: list[str] = []
root = Path(spec["export"])


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(tests: list[str]) -> tuple[dict[str, str], str]:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "-rA", *tests], cwd=root, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    nodes = {}
    for m in re.finditer(r"^(PASSED|FAILED|ERROR) (\S+)", r.stdout, re.M):
        nodes[m.group(2)] = m.group(1)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]
    return nodes, tail


for m in spec["mutants"]:
    f = root / m["file"]
    h0 = sha(f)
    raw = f.read_bytes()
    src = raw.decode("utf-8")
    old, new = m["old"], m["new"]
    if CRLF in src:
        old, new = old.replace(LF, CRLF), new.replace(LF, CRLF)
    if src.count(old) != 1:
        out_lines.append(f"{m['id']}: BAD (anchor found {src.count(old)} times) in {m['file']}")
        continue
    f.write_bytes(src.replace(old, new).encode("utf-8"))
    try:
        nodes, tail = run(m["tests"])
    finally:
        f.write_bytes(raw)
    restored = sha(f) == h0
    red = sorted(n for n, v in nodes.items() if v != "PASSED")
    green = sorted(n for n, v in nodes.items() if v == "PASSED")
    verdict = "KILLED" if red else ("BAD (0 nodes resolved)" if not nodes else "SURVIVED")
    out_lines.append(f"{m['id']}: {verdict} — {m.get('what', '')}")
    out_lines.append(f"   file {m['file']} restore sha256 {h0[:16]} {'OK' if restored else 'MISMATCH'}")
    out_lines.append(f"   nodes resolved {len(nodes)} · RED {len(red)} · GREEN {len(green)} · {tail}")
    for n in red:
        out_lines.append(f"   RED   {n}")
    for n in green:
        out_lines.append(f"   GREEN {n}")
Path(sys.argv[2]).write_text(LF.join(out_lines) + LF, encoding="utf-8")
print(LF.join(line for line in out_lines if not line.startswith("   GREEN")))

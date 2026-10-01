"""RED counterfactuals for increment 003 (security S1 in TaskDetails / image_block):
one mutation at a time on taskboard/modals.py, run the nodes, restore and prove
the restore by SHA-256. Run from the project root:
    python .dev-flow/2026-09-30-batch-01/evidence/mutate_inc003.py
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.getcwd()
MODALS = os.path.join(ROOT, "taskboard", "modals.py")
T = "tests/test_details_markup.py"

MUTATIONS = [
    ("N1 notes handed to Textual as a markup str",
     "                yield Static(notes_preview(t.notes))",
     "                yield Static(_highlight_markup(t.notes))",
     "notes"),
    ("N2 title label as a markup str",
     "            yield Label(_rich(f\"[b]{escape(t.title)}[/b]  —  o open raw · esc close\"),",
     "            yield Label((f\"[b]{escape(t.title)}[/b]  —  o open raw · esc close\"),",
     "title"),
    ("N3 project label as a markup str",
     "                yield Label(_rich(proj_name))",
     "                yield Label(proj_name)",
     "project"),
    ("N4 url label as a markup str",
     "                    yield Label(_rich(f\"link · {escape(u)}\"))",
     "                    yield Label(f\"link · {escape(u)}\")",
     "url"),
    ("N5 image fallback label as a markup str",
     "        yield Label(_rich(f\"[dim]missing:[/dim] {escape(ref)}\"))",
     "        yield Label(f\"[dim]missing:[/dim] {escape(ref)}\")",
     "image"),
    ("N6 notes flattened to plain text (highlight lost)",
     "                yield Static(notes_preview(t.notes))",
     "                yield Static(Text(t.notes))",
     "still_highlight"),
    ("N7 image viewer title as a markup str (review F1)",
     "                _rich(f\"[b]{escape(self._view_task.title)}[/b]  —  o open raw · esc close\"),",
     "                (f\"[b]{escape(self._view_task.title)}[/b]  —  o open raw · esc close\"),",
     "viewer"),
    ("N8 phase label as a markup str (review F2)",
     "                yield Label(_rich(escape(t.phase) + (\" · blocked\" if t.blocked else \"\")))",
     "                yield Label(escape(t.phase) + (\" · blocked\" if t.blocked else \"\"))",
     "phase"),
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    for name, old, new, node in MUTATIONS:
        before = open(MODALS, "rb").read()
        digest = sha(MODALS)
        text = before.decode("utf-8")
        if text.count(old) != 1:
            print(f"{name}: BAD (anchor matched {text.count(old)} times)")
            continue
        open(MODALS, "wb").write(text.replace(old, new).encode("utf-8"))
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", T, "-k", node],
                               capture_output=True, text=True, env=env, cwd=ROOT)
            tail = [ln for ln in r.stdout.splitlines() if " passed" in ln or " failed" in ln]
        finally:
            open(MODALS, "wb").write(before)
        ok = sha(MODALS) == digest
        verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
        print(f"{name}: {verdict} · -k {node!r} · restore sha256 {digest[:16]} ok={ok}")
        for ln in tail[-2:]:
            print("    " + ln)


if __name__ == "__main__":
    main()

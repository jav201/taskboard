"""Mutant spec for increment 003 (the kanban), written into <export>/spec.json and, with the
export redacted, into evidence/mutants_inc003.json. Run from the repo root:
    python mk_mutants_inc003.py <export dir>"""
import json
import sys

exp = sys.argv[1]
V, A = "taskboard/views.py", "taskboard/app.py"
T = ["tests/test_kanban_milestones.py"]
m = [
    ("K1", V, "    return [t for t in tasks if not t.milestone]\n\n\ndef _kanban_groups",
     "    return list(tasks)\n\n\ndef _kanban_groups", "kanban_work filters nothing"),
    ("K2", V, "    tasks = kanban_work(board.visible_tasks(show_archived))\n    if focus is not None and board.project_by_id(focus) is not None:",
     "    tasks = board.visible_tasks(show_archived)\n    if focus is not None and board.project_by_id(focus) is not None:",
     "the grouped plan lays out milestones"),
    ("K3", V, "    inner = w\n    tasks = kanban_work(board.visible_tasks(show_archived))\n    label_w = max(6",
     "    inner = w\n    tasks = board.visible_tasks(show_archived)\n    label_w = max(6", "the matrix counts milestones"),
    ("K4", V, "    inner = w\n    tasks = kanban_work(board.visible_tasks(show_archived))\n    focused =",
     "    inner = w\n    tasks = board.visible_tasks(show_archived)\n    focused =", "the lanes draw milestones"),
    ("K5", V, "        tasks = kanban_work(tasks)       # a milestone is never a card (LLR-603.1)\n", "",
     "the nav walks milestones"),
    ("K6", V, "            total = len(kanban_work(board.visible_tasks(show_archived)))   # LLR-603.1\n            hits = len(kanban_work(fb.visible_tasks(show_archived)))",
     "            total = len(board.visible_tasks(show_archived))\n            hits = len(fb.visible_tasks(show_archived))",
     "the filter counts milestones"),
    ("K7", V, "    return late + ahead + [(\"reached\", t) for t in reached]",
     "    return ahead + late + [(\"reached\", t) for t in reached]", "late after upcoming"),
    ("K8", V, "    reached = sort_by_due([t for t in ms if board.is_done(t)])[-1:]",
     "    reached = sort_by_due([t for t in ms if board.is_done(t)])", "every reached milestone listed"),
    ("K9", V, "        more = sum(1 for kind, _t in items[n:] if kind != \"reached\")\n        return out",
     "        more = len(items[n:])\n        return out", "reached counted in +N"),
    ("K10", V, "    return [(f\"+{more} ◆\", \"mut\")] if more and len(f\"+{more} ◆\") <= room else []",
     "    return []", "no +N fallback (D-619)"),
    ("K11", V, "            if more:\n                facts = facts + [(\" ── \", \"frame\")] + more\n",
     "            if False:\n                facts = facts + [(\" ── \", \"frame\")] + more\n", "the band rule carries nothing"),
    ("K12", A, "            if sel is not None and sel.milestone:\n", "            if False:\n",
     "a milestone selection jumps to the first task, not the nearest column"),
    ("K13", A, "                        if best is None or cp > best[0]:\n",
     "                        if best is None or cp < best[0]:\n", "the farthest column, not the nearest"),
    ("K14", V, "            tone, dk, tk, rk = color, \"ink\", \"hd\", \"soon\" if n == 0 else \"mut\"\n",
     "            tone, dk, tk, rk = color, \"ink\", \"hd\", \"mut\"\n", "today not in soon"),
    ("K15", V, "            tone, dk, tk, rk = color, \"ink\", \"hd\", \"soon\" if n == 0 else \"mut\"\n",
     "            tone, dk, tk, rk = \"over\", \"ink\", \"hd\", \"soon\" if n == 0 else \"mut\"\n",
     "an upcoming milestone in over"),
    ("K16", V, "            if tw < 8:\n                break\n", "            if tw < 1:\n                break\n",
     "titles cut below 8 cells"),
]
spec = {"export": exp, "mutants": [dict(id=i, file=f, old=o, new=n, what=w, tests=T)
                                   for i, f, o, n, w in m]}
json.dump(spec, open(exp + "/spec.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
spec["export"] = "<scratch>/bat003"
json.dump(spec, open(".dev-flow/2026-10-04-batch-02/evidence/mutants_inc003.json", "w",
                     encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(m))

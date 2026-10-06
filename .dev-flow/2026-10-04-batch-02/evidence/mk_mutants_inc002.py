import json, re, sys
exp = sys.argv[1]
V = "taskboard/views.py"
A = "taskboard/app.py"
T = ["tests/test_gantt_milestones.py"]
src = open(V, encoding="utf-8").read()
i = src.index('    items = [("⟦━⟧", "bright", "selected, exact dates", "selected"),')
j = src.index('             ("◂▸", "mut", "beyond window", "beyond")]', i) + len('             ("◂▸", "mut", "beyond window", "beyond")]')
block = src[i:j]
moved = block.replace('''             # right after the selection, as the M-1 frames place them (D-624)
             ("◆", "mut", "milestone", "milestone"),
             ("◆✓", "ash", "reached", "reached"),
''', "").replace('("◂▸", "mut", "beyond window", "beyond")]', '("◂▸", "mut", "beyond window", "beyond"),\n             ("◆", "mut", "milestone", "milestone"),\n             ("◆✓", "ash", "reached", "reached")]')
m = [
 ("G1", V, "    rows = [tuple(sort_by_due(o + [t for t in r if t.milestone and board.is_done(t)\n                                   and not t.archived])) if o else ()\n",
  "    rows = [tuple(o) if o else ()\n", "reached milestones never rows"),
 ("G2", V, "    rows = [tuple(sort_by_due(o + [t for t in r if t.milestone", "    rows = [tuple((o + [t for t in r if t.milestone", "reached rows appended, not merged by due"),
 ("G3", V, "                                   and not t.archived])) if o else ()\n", "                                   and not t.archived])) if True else ()\n", "reached rows without open work"),
 ("G4", V, "        return [[t.id for g in groups for t in g.rows]]", "        return [[t.id for g in groups for t in g.open]]", "nav walks open, not rows"),
 ("G5", V, "    if board.is_done(task):\n        return \"ash\"\n", "    if board.is_done(task):\n        return project_color(board, task)\n", "a reached milestone in its project hue"),
 ("G6", V, "    elif d < today:\n        lab, tone = f\"▲{(today - d).days}d\", \"over\"\n    elif d == today:\n        lab, tone = \"today\", \"soon\"\n    else:\n        lab, tone = f\"in {(d - today).days}d\", \"mut\"\n",
  "    elif d <= today:\n        lab, tone = f\"▲{(today - d).days}d\", \"over\"\n    else:\n        lab, tone = f\"in {(d - today).days}d\", \"mut\"\n", "today chipped as late"),
 ("G7", V, "        if t.milestone:            # one date, no bar (M-1, LLR-602.2)\n", "        if False:                  # one date, no bar (M-1, LLR-602.2)\n", "a milestone drawn as a bar"),
 ("G8", V, block, moved, "legend items appended last"),
 ("G9", V, "            if (t.project_id == sel_p.id and t.milestone and not t.archived\n", "            if (t.milestone and not t.archived\n", "ruler marks from every project"),
 ("G10", V, "                title = c(title, \"ash\")\n", "                title = title\n", "a reached title not ash"),
 ("G11", A, "        if task.milestone and g is not None and any(t is task for t in g.rows):\n", "        if False:\n", "] says folded for a drawn milestone"),
 ("G12", V, "            title = title_markup(t, label_w - 4, t.id == selected_id)\n", "            title = t.title\n", "an unescaped title"),
 ("G13", V, "    if x < 0:\n        cells[0] = (OFF_LEFT, \"mut\")\n        x = 1\n", "    if x < 0:\n        cells[0] = (OFF_LEFT, \"mut\")\n        x = 0\n", "the off-window diamond covers the edge glyph"),
 ("G14", V, "        cells[at - 1 if at == after else at + len(lab)] = (\" \", \"gap\")   # `◆ Oct 10`\n", "", "no space between the diamond and its date"),
]
spec = {"export": exp, "mutants": [dict(id=a, file=f, old=o, new=n, what=w, tests=T) for a, f, o, n, w in m]}
json.dump(spec, open(exp + "/spec.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
spec["export"] = "<scratch>/bat002"
json.dump(spec, open(".dev-flow/2026-10-04-batch-02/evidence/mutants_inc002.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(m))

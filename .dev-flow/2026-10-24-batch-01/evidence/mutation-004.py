"""Mutation battery, increment 004 (C-40/C-19/C-60). One arm per new node;
run by the orchestrator in the worktree; restore proven by hash.
Run:  env -u NO_COLOR python .dev-flow/2026-10-24-batch-01/evidence/mutation-004.py
"""
import hashlib, os, pathlib, subprocess, sys

VW = "taskboard/views.py"
RD = "README.md"
TL = "tests/test_legend.py"
TM = "tests/test_milestone_marks.py"
TR = "tests/test_readme.py"

ARMS = [
    ('test_TC_2607_a_lone_over_long_name_is_cut_not_crashed', TL, VW,
     b'    if width(parts) > room:\n        text, colour = parts[0]\n        shape, _, name = text.partition(" ")\n        parts[0] = (f"{shape} {fit(name, max(1, room - 2))}", colour)',
     b'    if width(parts) > room:\n        shape, name = parts[0]\n        parts[0] = (shape + " " + fit(name, max(1, room - 2)), parts[1])'),
    ('test_TC_2607_the_strip_lists_exactly_the_drawn_classes_then_the_hidden_count', TL, VW,
     b'    return [m for cid, m in (getattr(board, "marks", None) or {}).items()\n            if not m.hidden and cid in used]',
     b'    return [m for cid, m in (getattr(board, "marks", None) or {}).items()\n            if not m.hidden]'),
    ('test_TC_2607_no_classed_milestone_in_view_draws_no_strip', TL, VW,
     b'    drawn = _drawn_class_marks(board)\n    if not drawn:\n        return ""',
     b'    drawn = _drawn_class_marks(board)\n    if False:\n        return ""'),
    ('test_TC_2607_every_class_hidden_draws_no_strip', TL, VW,
     b'    drawn = _drawn_class_marks(board)\n    if not drawn:\n        return ""',
     b'    drawn = _drawn_class_marks(board)\n    if False:\n        return ""'),
    ('test_TC_2607_at_80_cells_the_strip_cuts_names_from_the_right', TL, VW,
     b'    while len(parts) > 1 and width(parts) > room:\n        parts.pop()',
     b'    if False:\n        parts.pop()'),
    ('test_TC_2607_a_markup_looking_name_prints_as_typed', TL, VW,
     b'        cells.append((escape(text[2:]), "mut"))',
     b'        cells.append((text[2:], "mut"))'),
    ('test_TC_2607_the_presentation_strip_names_only_the_projects_shown_classes', TL, VW,
     b'    drawn = [m for cid, m in (getattr(board, "marks", None) or {}).items()\n             if not m.hidden and cid in used]',
     b'    drawn = [m for cid, m in (getattr(board, "marks", None) or {}).items()\n             if cid in used]'),
    ('test_TC_2607_the_presentation_views_and_export_carry_the_strip', TL, VW,
     b"    if strip:\n        rows.append(strip)          # under the ruler, with the frame's export",
     b"    if False:\n        rows.append(strip)          # under the ruler, with the frame's export"),
    ('test_TC_2607_help_names_the_classes_the_manager_and_the_class_filter', TL, VW,
     b'                           "\xe2\x97\x86 = no class \xc2\xb7 # manage the classes,",\n',
     b''),
    ('test_TC_2608_hide_drops_the_class_from_the_gantt_and_the_board_is_untouched', TL, VW,
     b'    if _hidden_class_ids(board):\n        board = _hide(board)          # hidden classes leave the frame (LLR-2608.1)',
     b'    if False:\n        board = _hide(board)          # hidden classes leave the frame (LLR-2608.1)'),
    ('test_TC_2608_present_tasks_m_drops_hidden_classes_and_none_hidden_is_identity', TL, VW,
     b'    keep = [t for t in tasks if not (t.milestone and t.mark and t.mark in hidden)]',
     b'    keep = list(tasks)'),
    ('test_TC_2608_hidden_classes_leave_the_presentations_three_views_and_exports', TL, VW,
     b'    keep = [t for t in tasks if not (t.milestone and t.mark and t.mark in hidden)]',
     b'    keep = list(tasks)'),
    ('test_AT_2605_hide_and_the_legend', TL, VW,
     b'    if _hidden_class_ids(board):\n        board = _hide(board)          # hidden classes leave the frame (LLR-2608.1)',
     b'    if False:\n        board = _hide(board)          # hidden classes leave the frame (LLR-2608.1)'),
    ('test_AT_2606_hash_pay_filters_to_that_class', TM, VW,
     b'    if q.startswith("#"):\n        return matches_m(task, board, q)\n',
     b''),
    ('test_TC_2608_the_class_query_keeps_exactly_that_class_milestones', TM, VW,
     b'    if q.startswith("#"):\n        return matches_m(task, board, q)\n',
     b''),
    ('test_TC_2608_the_bar_names_the_class_and_nothing_when_no_class_holds', TM, VW,
     b'    elif query.startswith("#"):\n        return filter_bar_m(query, hits, total, w, marks)\n',
     b''),
    ('test_TC_2608_the_class_query_lights_no_text_in_the_overlay', TM, VW,
     b'    if not query.startswith(("@", "#")):\n        _highlight_grid(grid, query)',
     b'    lit = query[1:] if query.startswith("#") else query\n    _highlight_grid(grid, lit)'),
    ('test_TC_2607_readme_documents_the_classes_end_to_end', TR, RD,
     b"A hidden class's milestones leave the gantt and the presentation",
     b"A hidden class's milestones leave nothing"),
    ('test_TC_2607_readme_data_files_table_lists_the_directory', TR, RD,
     b'| `marks.json` | The milestone classes, for every board: id, name, shape, colour, hidden; written only when you add, edit or hide a class (never sent to a team folder) |\n',
     b''),
]

def norm_map(raw):
    norm = bytearray(); mapping = []
    i = 0
    while i < len(raw):
        if raw[i:i + 2] == bytes((13, 10)):
            norm.append(10); mapping.append(i); i += 2
        else:
            norm.append(raw[i]); mapping.append(i); i += 1
    return bytes(norm), mapping

def raw_span(raw, mapping, pos, length):
    start = mapping[pos]
    j = mapping[pos + length - 1]
    end = j + 2 if raw[j:j + 2] == bytes((13, 10)) else j + 1
    return start, end

bad = 0
hashes = {}
for f in sorted({f for _, _, f, _, _ in ARMS}):
    hashes[f] = hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
print("arms:", len(ARMS), flush=True)
for f, h in hashes.items():
    print("before %s: %s" % (f, h), flush=True)
for node, tfile, f, old, new in ARMS:
    arm = "%s::%s" % (tfile, node)
    p = pathlib.Path(f)
    src = p.read_bytes()
    h0 = hashes[f]
    try:
        norm, mapping = norm_map(src)
        pos = norm.find(old)
        if pos < 0:
            print(arm + ": BAD (anchor not found in %s)" % f, flush=True)
            bad += 1
            continue
        rs, re_ = raw_span(src, mapping, pos, len(old))
        p.write_bytes(src[:rs] + new + src[re_:])
        if hashlib.sha256(p.read_bytes()).hexdigest() == h0:
            print(arm + ": BAD (the edit did not apply)", flush=True)
            bad += 1
            continue
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
             "--color=no", "%s::%s" % (tfile, node)],
            env=dict(os.environ, PY_COLORS="0", NO_COLOR=""))
    finally:
        p.write_bytes(src)
    h1 = hashlib.sha256(p.read_bytes()).hexdigest()
    print("after: ", h1, flush=True)
    assert h1 == h0, "the restore of %s is not proven" % f
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    if verdict != "RED (KILLED)":
        bad += 1
    print(arm + ":", verdict or "CRASH/BAD (exit %d)" % r.returncode, flush=True)
print("BAD arms:", bad, flush=True)
sys.exit(1 if bad else 0)

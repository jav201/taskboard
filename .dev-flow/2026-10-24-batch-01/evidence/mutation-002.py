"""Mutation battery, increment 002 (C-40/C-19/C-60). One arm per reddener the
PDR section 5 declares for the new nodes; run by the orchestrator in the
worktree, no other session reading; restore proven by hash.
Run:  env -u NO_COLOR python .dev-flow/2026-10-24-batch-01/evidence/mutation-002.py
"""
import hashlib, os, pathlib, subprocess, sys

V = "taskboard/views.py"
MO = "taskboard/models.py"
T = "tests/test_milestone_marks.py"

ARMS = [
    ('test_TC_2604_the_seats_truth_table', V,
     b'    glyph = cls.shape if cls is not None else "\xe2\x97\x86"\n    style = cls.colour if cls is not None else "mut"',
     b'    glyph, style = "\xe2\x97\x86", "mut"'),
    ('test_TC_2604_the_seats_truth_table', V,
     b'        return HOLLOW.get(glyph, glyph), style, "\xe2\x9c\x93"',
     b'        return glyph, style, "\xe2\x9c\x93"'),
    ('test_TC_2604_a_nonempty_chip_implies_over_at_the_gantt_cells', V,
     b'        return glyph, style, f"\xe2\x96\xb2{(today - d).days}d"',
     b'        return glyph, style, ""'),
    ('test_TC_2604_a_nonempty_chip_implies_over_at_the_gantt_cells', V,
     b'    key = ("reached" if chip == "\xe2\x9c\x93" else\n           "over" if chip else "soon" if d == today else "mut")',
     b'    key = ("reached" if board.is_done(task) else\n           "over" if d and d < today else "soon" if d == today else "over")'),
    ('test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat', V,
     b'    for i, m in enumerate(marks):',
     b'    cells[0] = Text("\xe2\x97\x86", style="mut")  # a raw draw outside the seat\n    for i, m in enumerate(marks):'),
    ('test_TC_2604_the_sites_enumeration_every_milestone_mark_routes_through_the_seat', V,
     b'    if not task.milestone:\n        return title_markup(task, width, selected, arrow=arrow)\n    glyph, style, _chip = milestone_mark(task, board, today)',
     b'    if not task.milestone:\n        return title_markup(task, width, selected, arrow=arrow)\n    _raw = Text("\xe2\x97\x86", style="mut")  # a raw draw outside the seat\n    glyph, style, _chip = milestone_mark(task, board, today)'),
    ('test_AT_2603_the_state_shows_in_text', V,
     b'    style = cls.colour if cls is not None else "mut"',
     b'    style = ("reached" if board.is_done(task) else "over" if (d0 := parse_iso(task.due_date)) is not None and d0 < today else "mut")'),
    ('test_AT_2607_an_unknown_id_is_safe', MO,
     b'        if "mark" in d and d["mark"] is None:',
     b'        if "mark" in d:'),
    ('test_TC_2606_render_marks_every_row_is_exactly_w_cells', V,
     b'        r.truncate(w, overflow="ellipsis", pad=True)',
     b'        pass'),
    ('test_TC_2606_render_marks_the_frame_names_every_class_and_the_plain_row', V,
     b'            (m.shape, dim if off else HEX[m.colour]),\n            (f" {m.name}", dim if off else HEX["ink"]),',
     b'            (m.shape, dim if off else HEX[m.colour]),'),
    ('test_TC_2606_render_marks_a_hidden_class_is_dimmed_with_what_hiding_means', V,
     b'            (m.shape, dim if off else HEX[m.colour]),',
     b'            (m.shape, HEX[m.colour]),'),
    ('test_TC_2606_render_marks_narrow_counts_drop_before_the_names', V,
     b'        if counts is not None and cells_len(cells + tail) > w:',
     b'        if False and counts is not None and cells_len(cells + tail) > w:'),
    ('test_TC_2606_render_marks_an_empty_directory_says_so_and_a_markup_name_is_literal', V,
     b'        for text, style in cells:',
     b'        for text, style in cells:\n            if "[" in text: text = str(Text.from_markup(text))'),
    ('test_TC_2602_a_mark_set_on_a_non_milestone_is_kept_and_drawn_nowhere', V,
     b'    cls = (getattr(board, "marks", None) or {}).get(task.mark or "")',
     b'    cls = ((getattr(board, "marks", None) or {}).get(task.mark or "") if task.milestone else None)'),
]

bad = 0
hashes = {}
for f in sorted({f for _, f, _, _ in ARMS}):
    hashes[f] = hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
print("arms:", len(ARMS), flush=True)
for f, h in hashes.items():
    print("before %s: %s" % (f, h), flush=True)
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

for node, f, old, new in ARMS:
    arm = "%s::%s" % (T, node)
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
             "--color=no", "%s::%s" % (T, node)],
            env=dict(os.environ, PY_COLORS="0", NO_COLOR=""))
    finally:
        p.write_bytes(src)
    h1 = hashlib.sha256(p.read_bytes()).hexdigest()
    print("after: ", h1, flush=True)
    assert h1 == h0, "the restore of %s is not proven" % f
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    if verdict is None:
        bad += 1
    print(arm + ":", verdict or "CRASH/BAD (exit %d)" % r.returncode, flush=True)
print("BAD arms:", bad, flush=True)
sys.exit(1 if bad else 0)

"""Mutation battery, increment 003 (C-40/C-19/C-60). One arm per new node;
run by the orchestrator in the worktree; restore proven by hash.
Run:  env -u NO_COLOR python .dev-flow/2026-10-24-batch-01/evidence/mutation-003.py
"""
import hashlib, os, pathlib, subprocess, sys

MD = "taskboard/modals.py"
AP = "taskboard/app.py"
KM = "taskboard/keymap.py"
VW = "taskboard/views.py"
T = "tests/test_marks_manager.py"
TM = "tests/test_modal_keys.py"

ARMS = [
    ('test_TC_2605_the_editor_mounts_the_class_select_after_milestone', T, MD,
     b'                Binding("alt+m", "mark", "Class", priority=True),\n',
     b''),
    ('test_TC_2605_down_enter_carries_the_next_class', T, MD,
     b'            data["mark"] = str(mark_sel.value) or None',
     b'            pass'),
    ('test_TC_2605_none_saves_with_no_mark_key', T, MD,
     b'            data["mark"] = str(mark_sel.value) or None',
     b'            data["mark"] = str(mark_sel.value) or "none"'),
    ('test_TC_2605_a_markup_looking_class_name_shows_as_typed', T, MD,
     b'    return Text.assemble((mark.shape + " ", HEX[mark.colour]), (mark.name, HEX["ink"]))',
     b'    return f"{mark.shape} {mark.name}"'),
    ('test_TC_2605_an_empty_directory_composes_no_select', T, MD,
     b'                    if self._marks is not None and self._marks.marks:',
     b'                    if self._marks is not None:'),
    ('test_TC_2606_keymap_hash_is_global_off_the_bar_and_listed', T, KM,
     b'    Key("number_sign", "#", "marks_manager", "Milestone classes", group="misc", bar=False),\n',
     b''),
    ('test_TC_2606_the_manager_lists_every_class_with_counts_and_the_key_row', T, AP,
     b'            render_marks(self.app.marks, self.sel, w - 2, h, self.counts))',
     b'            render_marks(self.app.marks, self.sel, w - 2, h))'),
    ('test_TC_2606_space_hides_a_class_persisted_and_the_frame_redraws', T, AP,
     b'            self.app.marks.set_hidden(cid, not self.app.marks.marks[cid].hidden)',
     b'            self.app.marks.marks[cid].hidden = not self.app.marks.marks[cid].hidden'),
    ('test_TC_2606_e_edits_the_class_and_keeps_its_id', T, AP,
     b'            self.app.push_screen(MarkForm(cid), self._saved)',
     b'            self.app.push_screen(MarkForm(), self._saved)'),
    ('test_TC_2606_a_refused_write_says_so_and_keeps_the_form', T, MD,
     b'        shape, colour = SHAPES[self.si], COLOURS[self.ci]\n        try:',
     b'        shape, colour = SHAPES[self.si], COLOURS[self.ci]\n        self.dismiss(None)\n        try:'),
    ('test_TC_2606_a_blank_name_is_refused_and_the_form_is_kept', T, MD,
     b'        name = str(self.query_one("#mf-name", Input).value).strip()\n        if not name:',
     b'        name = str(self.query_one("#mf-name", Input).value).strip()\n        if False:'),
    ('test_TC_2606_hash_opens_from_the_main_screen_and_the_home_and_hash_esc_close', T, AP,
     b'    BINDINGS = [Binding("escape,number_sign", "back", "", priority=True),',
     b'    BINDINGS = [Binding("escape", "back", "", priority=True),'),
    ('test_TC_2606_hash_over_a_modal_does_nothing', T, MD,
     b'    def on_mount(self) -> None:\n        self._fit_width(self.app.size.width)',
     b'    def on_mount(self) -> None:\n        self._fit_width(self.app.size.width)\n        self.query_one("#f-save", Button).focus()'),
    ('test_TC_2606_the_seat_keys_are_refused_behind_the_manager', T, AP,
     b'PeopleDirectory, MarksManager))',
     b'PeopleDirectory))'),
    ('test_TC_2606_an_empty_directory_says_so_and_n_still_works', T, AP,
     b'    def action_new(self) -> None:\n        self.app.push_screen(MarkForm(), self._saved)',
     b'    def action_new(self) -> None:\n        if self._cur() is None:\n            return\n        self.app.push_screen(MarkForm(), self._saved)'),
    ('test_AT_2601_a_class_is_created_and_survives', T, VW,
     b'    glyph = cls.shape if cls is not None else "\xe2\x97\x86"\n    style = cls.colour if cls is not None else "mut"',
     b'    glyph, style = "\xe2\x97\x86", "mut"'),
    ('test_AT_2604_the_marks_manager_and_its_form_obey_the_modal_key_law', TM, TM,
     b'    "MarkForm": {"save": "alt+s", "cancel": "escape"},    # the marks manager\'s form (batch 2026-10-24-batch-01)\n',
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

"""Mutation battery, increment 001 (C-40/C-19/C-60). One arm per new node:
one edit, one node, one verdict per resolved arm; run by the orchestrator in
the worktree, no other session reading; restore proven by hash.
Run:  env -u NO_COLOR python .dev-flow/2026-10-24-batch-01/evidence/mutation-001.py
"""
import hashlib, itertools, os, pathlib, subprocess, sys

M = "taskboard/marks.py"
MO = "taskboard/models.py"
A = "taskboard/app.py"
T = "tests/test_marks_directory.py"

ARMS = [
    # node, file, old, new
    ("test_TC_2601_a_missing_file_is_an_empty_directory_and_nothing_is_written", M,
     b"                return cls(path)            # nothing written yet, or nothing to keep",
     b"                return cls(path, [], {\"unreadable\": True, \"backup\": None})"),
    ("test_TC_2601_an_empty_or_blank_file_is_an_empty_directory_and_nothing_is_said", M,
     b"                return cls(path)            # nothing written yet, or nothing to keep",
     b"                return cls(path, [], {\"unreadable\": True, \"backup\": None})"),
    ("test_TC_2601_the_file_is_read_and_bad_entries_are_skipped", M,
     b"if not (isinstance(colour, str) and colour in COLOURS):",
     b"if not isinstance(colour, str):"),
    ("test_TC_2601_an_unreadable_file_is_kept_aside_and_the_directory_starts_empty", M,
     b"            backup = keep_aside(path)",
     b"            backup = None"),
    ("test_TC_2601_find_resolves_a_prefix_only_and_lower_case", M,
     b"if m.name.lower().startswith(q)), None)",
     b"if q in m.name.lower()), None)"),
    ("test_TC_2601_add_derives_the_id_and_writes_the_file", M,
     b"write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))",
     b"write_atomic(self.path.with_suffix('.wrong'), json.dumps(data, indent=2, ensure_ascii=False))"),
    ("test_TC_2601_a_name_with_nothing_left_is_refused", M,
     b'raise ValueError("a class needs a name")',
     b"pass"),
    ("test_TC_2601_a_shape_or_colour_outside_the_sets_is_refused", M,
     b"        if colour not in COLOURS:\n            raise ValueError",
     b"        if False:\n            raise ValueError"),
    ("test_TC_2601_two_directories_on_one_file_both_survive_an_add", M,
     b"fresh = {m.id: m for m in (marks if marks is not None\n"
     b"                                       else list(self.marks.values()))}",
     b"fresh = {m.id: m for m in list(self.marks.values())}"),
    ("test_TC_2601_edit_keeps_the_id_and_writes_back_a_class_the_file_lost", M,
     b"write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))",
     b"write_atomic(self.path.with_suffix('.wrong'), json.dumps(data, indent=2, ensure_ascii=False))"),
    ("test_TC_2601_edit_and_set_hidden_keep_the_rest_of_the_class", M,
     b"m = Mark(cls_id, held.name, held.shape, held.colour, bool(hidden))",
     b"m = Mark(cls_id, held.name, held.shape, held.colour, not bool(hidden))"),
    ("test_TC_2601_an_unparseable_file_is_kept_aside_before_it_is_replaced", M,
     b"if marks is None and not self._set_aside():",
     b"if marks is None and self._set_aside():"),
    ("test_TC_2601_an_unparseable_file_that_cannot_be_kept_is_never_written_over", M,
     b"if marks is None and not self._set_aside():",
     b"if False:"),
    ("test_TC_2601_a_held_lock_makes_the_write_wait_then_fail_and_change_nothing", M,
     b"with file_lock(self.path):",
     b"with file_lock(self.path.with_name(self.path.name + '.other')):"),
    ("test_TC_2601_a_failed_write_changes_nothing_in_memory", M,
     b"            result = change(fresh)",
     b"            result = change(fresh); self._hold(list(fresh.values()))"),
    ("test_TC_2602_a_mark_round_trips_through_the_model", MO,
     b"mark=d.get(\"mark\") if isinstance(d.get(\"mark\"), str) else None,",
     b"mark=None,"),
    ("test_TC_2602_a_task_without_a_mark_saves_with_no_mark_key", MO,
     b'if "mark" in d and d["mark"] is None:',
     b"if False:"),
    ("test_TC_2602_a_board_without_marks_keeps_its_bytes_through_a_load_and_a_save", MO,
     b'if "mark" in d and d["mark"] is None:',
     b"if False:"),
    ("test_TC_2602_an_unknown_id_is_kept_byte_for_byte_through_a_save", MO,
     b"mark=d.get(\"mark\") if isinstance(d.get(\"mark\"), str) else None,",
     b"mark=None,"),
    ("test_TC_2602_unticking_milestone_keeps_the_mark", MO,
     b"mark=d.get(\"mark\") if isinstance(d.get(\"mark\"), str) else None,",
     b"mark=None,"),
    ("test_TC_2602_only_marked_tasks_gain_the_key", MO,
     b'            del d["mark"]       # written only when set, like show_in_present',
     b'            d["mark"] = d["mark"] or "unclassified"   # every task gains a key'),
    ("test_TC_2603_ten_interleaved_adds_lose_nothing", M,
     b"fresh = {m.id: m for m in (marks if marks is not None\n"
     b"                                       else list(self.marks.values()))}",
     b"fresh = {m.id: m for m in list(self.marks.values())}"),
    ("test_TC_2603_the_corrupt_copy_is_never_replaced", M,
     b"            backup = keep_aside(path)",
     b"            path.with_name(path.name + '.corrupt').unlink(missing_ok=True); backup = keep_aside(path)"),
    ("test_AT_2602_the_store_is_safe", M,
     b"fresh = {m.id: m for m in (marks if marks is not None\n"
     b"                                       else list(self.marks.values()))}",
     b"fresh = {m.id: m for m in list(self.marks.values())}"),
    ("test_TC_2607_a_push_carries_the_id_and_nothing_of_the_directory", MO,
     b"mark=d.get(\"mark\") if isinstance(d.get(\"mark\"), str) else None,",
     b"mark=None,"),
    ("test_TC_2601_the_app_holds_the_directory_and_hands_it_to_every_board", A,
     b"self.board.marks = self.marks.marks",
     b"self.board.marks = {}"),
    ("test_TC_2601_after_move_carries_the_directory", A,
     b"new_src.marks = self.board.marks",
     b"new_src.marks = {}"),
    ("test_TC_2601_an_unreadable_directory_is_said_and_kept", A,
     b"if self.marks.load_report.get(\"unreadable\"):",
     b"if False and self.marks.load_report.get(\"unreadable\"):"),
    ("test_TC_2601_an_app_without_a_registry_never_writes_a_directory", M,
     b"                return cls(path)            # nothing written yet, or nothing to keep",
     b"                path.write_text('{}'); return cls(path)"),
    ("test_TC_2601_a_class_written_through_the_store_survives_a_restart", M,
     b"            write_atomic(self.path, json.dumps(data, indent=2, ensure_ascii=False))",
     b"            pass  # the write is gone"),
    ("test_TC_2603_a_fresh_home_has_no_marks_json_after_open_app_alone", M,
     b"                return cls(path)            # nothing written yet, or nothing to keep",
     b"                path.write_text('{}'); return cls(path)"),
]

bad = 0
hashes = {}
for f in sorted({f for _, f, _, _ in ARMS}):
    hashes[f] = hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
print("arms:", len(ARMS), flush=True)
for f, h in hashes.items():
    print("before %s: %s" % (f, h), flush=True)
for node, f, old, new in ARMS:
    arm = "%s::%s" % (T, node)
    p = pathlib.Path(f)
    src = p.read_bytes()
    h0 = hashes[f]
    try:
        if old not in src:
            print(arm + ": BAD (anchor not found in %s)" % f, flush=True)
            bad += 1
            continue
        p.write_bytes(src.replace(old, new, 1))
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

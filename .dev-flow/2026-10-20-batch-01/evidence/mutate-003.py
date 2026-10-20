"""Increments 003 and 004's mutation batteries (C-40): one edit per arm, its node(s)
run, the file restored and its hash compared. Run from the project root, NO_COLOR unset:

    python .dev-flow/2026-10-20-batch-01/evidence/mutate-00N.py > .dev-flow/2026-10-20-batch-01/evidence/mutation-00N.txt
"""
import hashlib
import os
import pathlib
import subprocess
import sys

F = "tests/test_boards_forms.py::"
V = "tests/test_boards_move.py::"
ARMS_003 = [
    ("taskboard/boards.py", "        folder.mkdir(parents=True, exist_ok=False)",
     "        folder.mkdir(parents=True, exist_ok=True)",
     [F + "test_TC_2205_a_folder_on_disk_is_never_written_into"]),
    ("taskboard/boards.py", "        taken = {p.name.lower() for p in root.iterdir()} if root.is_dir() else set()",
     "        taken = set()", [F + "test_TC_2205_a_folder_on_disk_is_never_written_into"]),
    ("taskboard/boards.py", '        if not name:\n            raise ValueError("a board needs a name")',
     '        if False:\n            raise ValueError("a board needs a name")',
     [F + "test_TC_2205_an_empty_name_is_refused"]),
    ("taskboard/boards.py", "    return strip_controls(str(name)).strip()[:NAME_MAX].strip()",
     "    return strip_controls(str(name)).strip()",
     [F + "test_TC_2205_names_are_cut_and_reserved_slugs_suffixed"]),
    ("taskboard/boards.py", '    return out + "-board" if out in _RESERVED else out', "    return out",
     [F + "test_TC_2205_names_are_cut_and_reserved_slugs_suffixed"]),
    ("taskboard/boards.py", '        return next((c for c in PROJECT_COLORS if c not in used), "violet")',
     '        return "violet"', [F + "test_TC_2205_edit_archive_and_free_color",
                               F + "test_AT_2205_manage_boards_from_the_home"]),
    ("taskboard/boards.py", "        try:\n            self.save()\n        except OSError:\n            entry.name, entry.color = before",
     "        try:\n            pass\n        except OSError:\n            entry.name, entry.color = before",
     [F + "test_TC_2205_edit_archive_and_free_color"]),
    ("taskboard/app.py", "        if entry.id == self.app.board_id:\n            self.app.notify(\"The open board cannot be archived",
     "        if False:\n            self.app.notify(\"The open board cannot be archived",
     [F + "test_TC_2205_the_open_board_is_never_archived"]),
    ("taskboard/app.py", "                    RENUMBER_NOTICE_KEY: True}", "                    }",
     [F + "test_AT_2205_manage_boards_from_the_home"]),
    ("taskboard/app.py", 'ConfirmModal(msg, confirm="Archive", variant="warning")', "ConfirmModal(msg)",
     [F + "test_AT_2205_manage_boards_from_the_home",
      F + "test_TC_2205_the_chip_follows_a_rename_and_leaves_at_one_board"]),
    ("taskboard/app.py", "            return\n        self.app._label_board()\n        self.app.refresh_view()\n        self._paint()",
     "            return\n        self.app.refresh_view()\n        self._paint()",
     [F + "test_TC_2205_the_chip_follows_a_rename_and_leaves_at_one_board"]),
    ("taskboard/modals.py", "        self.hue = (self.hue + delta) % len(PROJECT_COLORS)",
     "        self.hue = min(len(PROJECT_COLORS) - 1, max(0, self.hue + delta))",
     [F + "test_TC_2205_the_form"]),
    ("taskboard/boards.py", "    return value if when.tzinfo is None else None", "    return value",
     [F + "test_TC_2205_an_offset_time_in_the_registry_is_none"]),
    ("taskboard/app.py", "    def _notify_save_error(self, failed: str | None) -> None:\n        if failed:",
     "    def _notify_save_error(self, failed: str | None) -> None:\n        if False:",
     [F + "test_TC_2205_a_registry_that_cannot_be_written"]),
    # the code review's F1 and F3
    ("taskboard/boards.py", "                self.entries.remove(entry)          # nothing registered",
     "                pass          # nothing registered",
     [F + "test_TC_2205_a_failed_registry_save_changes_nothing"]),
    ("taskboard/boards.py", "            shutil.rmtree(folder, ignore_errors=True)   # the folder",
     "            pass   # the folder", [F + "test_TC_2205_a_failed_registry_save_changes_nothing"]),
    ("taskboard/boards.py", "            entry.name, entry.color = before        # as on disk",
     "            pass        # as on disk",
     [F + "test_TC_2205_a_failed_registry_save_changes_nothing",
      F + "test_TC_2205_a_registry_that_cannot_be_written"]),
    ("taskboard/boards.py", "                entry.archived = False              # as on disk",
     "                pass              # as on disk",
     [F + "test_TC_2205_a_failed_registry_save_changes_nothing"]),
    ("taskboard/modals.py", '"boards" / self.next_id(name)', '"boards" / slug(name)',
     [F + "test_TC_2205_the_form"]),
    ("taskboard/app.py", "        try:\n            self.app.registry.edit(self.entries[self.cursor].id, *result)\n        except OSError as exc:",
     "        try:\n            self.app.registry.edit(self.entries[self.cursor].id, *result)\n        except ZeroDivisionError as exc:",
     [F + "test_TC_2205_a_registry_that_cannot_be_written"]),
]
ARMS_004 = [
    ("taskboard/boards.py", "        for t in new_src.tasks:\n            t.depends_on = [d for d in t.depends_on if d not in ids]",
     "        for t in new_src.tasks:\n            pass", [V + "test_TC_2206_the_move"]),
    ("taskboard/boards.py", "            t.depends_on = [d for d in t.depends_on if d in ids]",
     "            t.depends_on = list(t.depends_on)", [V + "test_TC_2206_the_move"]),
    ("taskboard/boards.py", "            t.depends_on = [d for d in t.depends_on if d in ids]",
     "            t.depends_on = []", [V + "test_TC_2206_the_move", V + "test_AT_2206_move_a_project_to_another_board"]),
    ("taskboard/boards.py", 'pre-move-{day}" + (f"-{n}" if n > 1 else ""))\n        try:\n            with open(dest, "xb") as fh:',
     'pre-move-{day}" + (f"-{n}" if n > 1 else ""))\n        try:\n            with open(dest, "wb") as fh:',
     [V + "test_TC_2206_a_second_move_the_same_day"]),
    ("taskboard/boards.py", '        new_dst.save_atomic()\n        steps.append("saved the target")\n        new_src.save_atomic()\n        saved = new_src\n        steps.append("saved the source")',
     '        new_src.save_atomic()\n        saved = new_src\n        steps.append("saved the source")\n        new_dst.save_atomic()\n        steps.append("saved the target")',
     [V + "test_TC_2206_the_target_save_failing_leaves_the_source"]),
    ("taskboard/boards.py", "        new_src, new_dst = copy.deepcopy(src), copy.deepcopy(dst)",
     "        new_src, new_dst = src, dst",
     [V + "test_TC_2206_the_move", V + "test_TC_2206_the_target_save_failing_leaves_the_source"]),
    ("taskboard/boards.py", "        if plan.refusal:\n            raise OSError(plan.refusal)",
     "        if False:\n            raise OSError(plan.refusal)", [V + "test_TC_2206_the_target_lacks_a_phase"]),
    ("taskboard/boards.py", "                    refs.append(str(new_dir / r.resolve().relative_to(old_dir.resolve())))",
     "                    refs.append(ref)",
     [V + "test_TC_2206_the_move", V + "test_AT_2206_move_a_project_to_another_board"]),
    ("taskboard/boards.py", "        if not (isinstance(x, str) and _ID.fullmatch(x)):",
     "        if False:", [V + "test_TC_2206_an_id_that_cannot_name_a_folder"]),
    ("taskboard/boards.py", "    if pid in src_team or pid in dst_team:", "    if pid in src_team:",
     [V + "test_TC_2206_shared_in_team_mode_either_side"]),
    ("taskboard/boards.py", "    if _key(src.path) == _key(dst.path) or _samefile(src.path, dst.path):",
     "    if False:", [V + "test_TC_2206_a_missing_or_unreadable_target_or_the_same_file"]),
    ("taskboard/boards.py", "        if _stamp(dst.path) != plan.dst_stamp:", "        if False:",
     [V + "test_TC_2206_a_target_changed_after_the_plan"]),
    ("taskboard/boards.py", "    if missing:\n        return f\"the target has no phase", "    if False:\n        return f\"the target has no phase",
     [V + "test_TC_2206_the_target_lacks_a_phase", V + "test_TC_2206_refusal_notices_and_no_other_board"]),
    ("taskboard/boards.py", "        saved = new_src\n", "", [V + "test_TC_2206_a_failure_after_the_source_save"]),
    ("taskboard/boards.py", '                (moved if isinstance(rec, dict) and rec.get("task") in ids else keep).append(line)',
     "                keep.append(line)",
     [V + "test_TC_2206_the_move", V + "test_AT_2206_move_a_project_to_another_board"]),
    ("taskboard/boards.py", "    write_atomic(p, json.dumps(items + [entry], indent=2, ensure_ascii=False))",
     "    write_atomic(p, json.dumps([entry], indent=2, ensure_ascii=False))",
     [V + "test_TC_2206_a_second_move_the_same_day"]),
    ("taskboard/modals.py", '        ("m", "move_board", "Move to board"),\n', "",
     [V + "test_AT_2206_move_a_project_to_another_board"]),
    ("taskboard/app.py", "        self.board = new_src\n        self._undo_stack = []", "        self.board = new_src",
     [V + "test_AT_2206_move_a_project_to_another_board"]),
    ("taskboard/modals.py", "        links.rstrip()\n", "",
     [V + "test_TC_2206_the_confirmation_is_the_rounds_box_and_the_undo_line"]),
]
ARMS = {"003": ARMS_003, "004": ARMS_004}[sys.argv[1]]

print("arms:", sum(len(n) for *_x, n in ARMS))
bad = 0
for path, old, new, nodes in ARMS:
    f = pathlib.Path(path)
    src = f.read_bytes()
    h0 = hashlib.sha256(src).hexdigest()
    text = src.decode("utf-8")
    assert text.count(old) == 1, ("anchor", path, old, text.count(old))
    for node in nodes:
        try:
            f.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            assert hashlib.sha256(f.read_bytes()).hexdigest() != h0, "the edit did not apply"
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", node], env=dict(os.environ, PY_COLORS="0",
                                                              PYTHONDONTWRITEBYTECODE="1"),
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        finally:
            f.write_bytes(src)
        h1 = hashlib.sha256(f.read_bytes()).hexdigest()
        assert h1 == h0, "the restore is not proven"
        verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
        bad += verdict != "RED (KILLED)"
        print(f"{path} [{old.strip()[:50]!r} -> {new.strip()[:40]!r}] {node.split('::')[1]}: "
              f"{verdict or 'CRASH/BAD (exit %d)' % r.returncode} · restore {h1[:16]}", flush=True)
print("not killed:", bad)
sys.exit(1 if bad else 0)

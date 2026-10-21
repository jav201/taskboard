"""Mutation battery of increment 002 (batch 2026-10-20-batch-03), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_present_backlog_round.py::"
A, V, M, K = "taskboard/app.py", "taskboard/views.py", "taskboard/modals.py", "taskboard/keymap.py"
CHIP = "            return Text.assemble(chip, self._keys_hint(w, hidden, room - chip.cell_len))"
ARMS = [
    ("M1 the chip dropped from the hint", A, CHIP,
     "            return self._keys_hint(w, hidden, room)", T + "test_TC_2402_the_hint_opens_with_the_chip"),
    ("M1b the chip dropped (AT)", A, CHIP, "            return self._keys_hint(w, hidden, room)",
     T + "test_AT_2402_the_presenter_reads_the_board_the_slide_never_does"),
    ("M2 the chip in the frame too", A,
     '        self.query_one("#present-frame", Static).update(self._frame_text())',
     '        self.query_one("#present-frame", Static).update(Text.assemble(board_chip_text(self._board.label), self._frame_text()))',
     T + "test_AT_2402_the_presenter_reads_the_board_the_slide_never_does"),
    ("M2b narrow and the rail read off the chip's room (code review CR-1)", A, CHIP,
     "            return Text.assemble(chip, self._keys_hint(w - chip.cell_len, hidden, room - chip.cell_len))",
     T + "test_TC_2402_the_chip_never_costs_the_keys"),
    ("M3 a binding outside the seat", A, "    BINDINGS = present_bindings()\n",
     "    BINDINGS = present_bindings() + [Binding(\"z\", \"close\", \"\", priority=True)]\n",
     T + "test_TC_2403_the_bindings_are_the_seat"),
    ("M4 `?` unbound", K, '    PresentKey((("question_mark", "keys"),), "?", "these keys", "OUT"),\n', "",
     T + "test_AT_2403_question_mark_shows_every_key"),
    ("M5 the live rule inverted", M, "            live = row.view is None or row.view == self.view",
     "            live = row.view is None or row.view != self.view",
     T + "test_TC_2403_the_window_is_the_seat_live_by_view"),
    ("M5b the live rule inverted (AT)", M, "            live = row.view is None or row.view == self.view",
     "            live = row.view is None or row.view != self.view",
     T + "test_AT_2403_question_mark_shows_every_key"),
    ("M6 `? keys` dropped from the hint", A, '        hint.append("?", style="bold #e6edf7")\n', "",
     T + "test_AT_2403_question_mark_shows_every_key"),
    ("M7 the export keeps the cursor", V,
     "    lines, _stops, _cur = _all_timeline(board, tw, height, today, None, folded, True, anchor)",
     "    lines, _stops, _cur = _all_timeline(board, tw, height, today, (\"proj\", anchor) if anchor else None, folded, False, anchor)",
     T + "test_AT_2404_the_export_reads_as_a_slide[size0-93]"),
    ("M8 the cut drops a content row", V,
     "    while lines and not _strip(lines[-1]).strip():\n        lines.pop()",
     "    while lines and not _strip(lines[-1]).strip():\n        lines.pop()\n    lines = lines[:-1]",
     T + "test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content"),
    ("M9 no cut at all", V,
     "    while lines and not _strip(lines[-1]).strip():\n        lines.pop()", "    pass",
     T + "test_AT_2404_the_export_reads_as_a_slide[size1-80]"),
    ("M10 the export anchored on no project", V,
     "    around = anchor if anchor is not None else (cur_proj.id if cur_proj else None)",
     "    around = cur_proj.id if cur_proj else None",
     T + "test_TC_2404_the_export_has_no_cursor_and_ends_at_its_content"),
    ("M11 the export back on the screen's timeline", A,
     "            text, w, h = present_all_export(self._board, self._today, w, h,\n"
     "                                            frozenset(self._folded), proj.id if proj else None)",
     "            r = self._render_all()\n            text, w = r.timeline, r.timeline_w",
     T + "test_AT_2404_the_export_reads_as_a_slide[size0-93]"),
    ("M12 K/J unbound", K, '    PresentKey((("shift+up,K", "reorder(-1)"), ("shift+down,J", "reorder(1)")),',
     '    PresentKey((("shift+up", "reorder(-1)"), ("shift+down", "reorder(1)")),',
     T + "test_AT_2405_K_and_J_reorder"),
    ("M13 a wording without K J", A,
     '                ("  ", "⇥ · ↑↓ · ←→ rail · ␣ hide · K J order · enter fold · a all · x · esc"),',
     '                ("  ", "⇥ · ↑↓ · ←→ rail · ␣ hide · ⇧↑↓ order · enter fold · a all · x · esc"),',
     T + "test_TC_2405_the_hint_names_K_J[None]"),
]
print("arms:", len(ARMS), flush=True)
bad = 0
env = dict(os.environ, PY_COLORS="0", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
env.pop("NO_COLOR", None)
for label, path, old, new, node in ARMS:
    f = pathlib.Path(path)
    src = f.read_bytes()
    text = src.decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    o, n = old.replace("\n", nl), new.replace("\n", nl)
    h0 = hashlib.sha256(src).hexdigest()
    if text.count(o) != 1:
        print(f"{label}: BAD (anchor found {text.count(o)} times)", flush=True)
        bad += 1
        continue
    try:
        f.write_bytes(text.replace(o, n, 1).encode("utf-8"))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--color=no", node], env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
    finally:
        f.write_bytes(src)
    h1 = hashlib.sha256(f.read_bytes()).hexdigest()
    assert h1 == h0, "the restore is not proven"
    verdict = {1: "RED (KILLED)", 0: "GREEN (SURVIVED)"}.get(r.returncode)
    bad += verdict != "RED (KILLED)"
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"{label} · {path} · {node.split('::')[1]}: {verdict or 'CRASH/BAD (exit %d)' % r.returncode}"
          f" · sha256 {h0[:12]} restored · {tail}", flush=True)
print("not killed:", bad)
sys.exit(1 if bad else 0)

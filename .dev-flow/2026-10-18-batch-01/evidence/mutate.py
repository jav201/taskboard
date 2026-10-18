"""Mutation battery for batch 2026-10-18-batch-01 (restore-verified).

    python .dev-flow/2026-10-18-batch-01/evidence/mutate.py <tree root> 001|002

Run against a tree no other session is reading (a scratch copy holding the
increment's exact bytes). Each mutant replaces ONE exact byte string (it must
occur exactly once) in its file, runs each named node on its own, records one
verdict per node — KILLED (exit 1), SURVIVED (exit 0), BAD (any other code) —
restores the original bytes and verifies their SHA-256. The arm count is
asserted before any verdict is trusted. Redirect into `mutation-<inc>.txt`.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

V = "taskboard/views.py"
A = "taskboard/app.py"
PV = "tests/test_present_views.py::"
PA = "tests/test_present_views_app.py::"
PR = "tests/test_present.py::"

MUTANTS = {
    "001": [
        ("M1", "the note is one paragraph again (line breaks dropped)", V,
         b'(notes or "").strip().split("\\n"):',
         b'(notes or "").strip().replace("\\n", " ").split("\\n"):',
         [PV + "test_TC_1801_line_breaks_bullets_and_numbers_are_kept",
          PV + "test_TC_1807_the_cursor_note_keeps_its_line_breaks[PRES-V3-gantt-notes-118x30.txt-118-30]",
          PV + "test_TC_1803_the_exact_split_frames[PRES-V3-split-118x30.txt-tw3-118-30]"]),
        ("M2", "a dash item keeps its dash, no bullet", V,
         b'lead, body = "\xe2\x80\xa2 ", body[2:]',
         b'lead, body = "", body',
         [PV + "test_TC_1801_line_breaks_bullets_and_numbers_are_kept",
          PV + "test_TC_1803_the_exact_split_frames[PRES-V3-split-118x30.txt-tw3-118-30]"]),
        ("M3", "a numbered item takes one digit only", V,
         b'_PRESENT_ITEM = re.compile(r"\\d{1,3}\\. ")',
         b'_PRESENT_ITEM = re.compile(r"\\d\\. ")',
         [PV + "test_TC_1801_line_breaks_bullets_and_numbers_are_kept"]),
        ("M4", "two columns only above 100 columns", V,
         b'    wide = width >= 100\n    label_w, chip_w, field_w = _present_cols(width, wide)\n    ax = _present_axis(board, proj, open_t, field_w, today)\n    chain',
         b'    wide = width > 100\n    label_w, chip_w, field_w = _present_cols(width, wide)\n    ax = _present_axis(board, proj, open_t, field_w, today)\n    chain',
         [PV + "test_TC_1804_every_shown_open_task_with_notes_shows_its_text[100-30]"]),
        ("M5", "the cursor is not promised half the room", V,
         b'max(floor_n, room // 2)',
         b'max(floor_n, 0)',
         [PV + "test_TC_1802_present_alloc_truth_table[ns8-0-6-want8]",
          PV + "test_TC_1803_the_exact_split_frames[PRES-V3-split-long-80x24.txt-tw5-80-24]"]),
        ("M6", "a cut note says nothing about the cut", V,
         b'more = c(escape(clip(f"\xe2\x80\xa6 +{len(rows) - k + 1} lines", w)), "dim")',
         b'more = ""',
         [PV + "test_TC_1803_the_exact_split_frames[PRES-V3-split-80x24.txt-tw3-80-24]",
          PV + "test_TC_1807_the_cursor_note_keeps_its_line_breaks[PRES-V3-gantt-notes-80x24.txt-80-24]",
          PV + "test_TC_1804_every_shown_open_task_with_notes_shows_its_text[80-24]"]),
        ("M7", "a task with no notes does not say so", V,
         b'right = c("no notes", "dim") + c("  \xc2\xb7  ", "dim") + right',
         b'right = right',
         [PV + "test_TC_1804_every_shown_open_task_with_notes_shows_its_text[118-30]",
          PV + "test_TC_1803_the_exact_split_frames[PRES-V3-split-118x30.txt-tw3-118-30]"]),
        ("M8", "a note row's text is not escaped", V,
         b'c(escape(clip(txt, w - vis(lead))), "ink")',
         b'c(clip(txt, w - vis(lead)), "ink")',
         [PV + "test_TC_1805_hostile_notes_and_titles_render_literally"]),
        ("M9", "the cursor's note ignores scroll", V,
         b'if i == cur and note_scroll and sizes[i] < len(notes[i]):',
         b'if False:',
         [PV + "test_TC_1806_pgdn_scrolls_the_cursor_note_and_says_what_is_above"]),
        ("M10", "no area scroll when no cursor note can scroll", V,
         b'if whole and scroll:',
         b'if False:',
         [PV + "test_TC_1806_when_no_cursor_note_can_scroll_the_whole_area_does"]),
        ("M11", "the first page down skips the column's top", V,
         b'room, scroll - 1, w)',
         b'room, scroll, w)',
         [PV + "test_TC_1806_when_no_cursor_note_can_scroll_the_whole_area_does"]),
        ("M14", "a page jumps over rows (the step outgrows the window)", V,
         b'(page - 1) * (room - 2)',
         b'(page - 1) * (room + 3)',
         [PV + "test_TC_1806_paging_down_shows_every_row_of_the_note[80-24-tw5-False]",
          PV + "test_TC_1806_paging_down_shows_every_row_of_the_note[60-20-tw3-True]"]),
        ("M15", "below a row per note the cursor's note gets no row", V,
         b'ks[cur] = max(min(1, ns[cur]), min(want_c, room - sum(ks)))',
         b'ks[cur] = max(0, min(want_c, room - sum(ks)))',
         [PV + "test_TC_1802_present_alloc_truth_table[ns7-0-3-want7]"]),
        ("M16", "the one-row cut mark loses its unit", V,
         b'tag = f" \xe2\x80\xa6 +{len(rows) - 1} lines"',
         b'tag = f" \xe2\x80\xa6 +{len(rows) - 1}"',
         [PV + "test_TC_1803_the_exact_split_frames[PRES-V3-split-80x24.txt-tw3-80-24]"]),
        ("M18", "an overflowing column at page 0 starts at its top even when that hides the cursor", V,
         b'top = end - (room - 2) if len(summary) > room >= 3 and end > room - 1 else 0',
         b'top = 0',
         [PV + "test_TC_1804_below_a_row_per_note_every_missing_note_is_declared[80-18]",
          PV + "test_TC_1804_below_a_row_per_note_every_missing_note_is_declared[118-15]"]),
        ("M19", "the first page down jumps the whole text back to its top", V,
         b'        out = (_present_scrolled(full, room, scroll - 1, w) if base == 0 else\n',
         b'        out = (_present_scrolled(full, room, scroll - 1, w) if True else\n',
         [PV + "test_TC_1806_the_first_page_down_never_moves_the_text_back"]),
        ("M20", "wide glyphs wrapped by code points again", V,
         b'if vis(body) == len(body) else _wrap_cells(body, tw)',
         b'if True else _wrap_cells(body, tw)',
         [PV + "test_TC_1801_line_breaks_bullets_and_numbers_are_kept"]),
        ("M17", "every task hidden still paints the empty columns", V,
         b'if view == "split" and open_t:',
         b'if view == "split":',
         [PV + "test_TC_1804_every_task_hidden_leaves_the_notes_area_blank"]),
        ("M12", "the gantt note keeps 4 rows, not 3", V,
         b'_present_cut(rows, 3, width - 6)',
         b'_present_cut(rows, 4, width - 6)',
         [PV + "test_TC_1807_the_cursor_note_keeps_its_line_breaks[PRES-V3-gantt-notes-118x30.txt-118-30]"]),
        ("M13", "the header loses its view word", V,
         b' + c(f"  {escape(view)}", "dim"))',
         b')',
         [PV + "test_TC_1807_the_header_names_the_view",
          PR + "test_TC_1001_the_exact_presc_frame_at_118x30"]),
    ],
    "002": [
        ("N1", "the screen's `2` loses priority", A,
         b'Binding("2", "view(1)", "", priority=True),',
         b'Binding("2", "view(1)", ""),',
         [PA + "test_TC_1810_the_bindings_and_the_scroll_state"]),
        ("N2", "a page down past the end is taken", A,
         b'        if delta > 0 and self._frame_text(new).plain == self._frame_text().plain:\n            return\n',
         b'',
         [PA + "test_TC_1810_the_bindings_and_the_scroll_state",
          PA + "test_AT_1803_the_view_keys_and_what_the_views_share"]),
        ("N3", "a cursor move keeps the scroll", A,
         b'        self._scroll = 0\n        self._paint()\n\n    def action_view(',
         b'        self._paint()\n\n    def action_view(',
         [PA + "test_TC_1810_the_bindings_and_the_scroll_state"]),
        ("N4", "the gantt hint offers pgdn", A,
         b'split = PRESENT_VIEWS[self._view] == "split"',
         b'split = True',
         [PA + "test_TC_1808_the_hint_row_per_view[118]"]),
        ("N5", "the bold marks the other view", A,
         b'style="bold #e6edf7" if i == self._view else "#5b6675"',
         b'style="bold #e6edf7" if i != self._view else "#5b6675"',
         [PA + "test_TC_1808_the_hint_row_per_view[80]"]),
        ("N6", "both views export to one file", V,
         b'tail = "" if view == "gantt" else f"-{view}"',
         b'tail = ""',
         [PA + "test_TC_1809_each_view_exports_to_its_own_file",
          PA + "test_AT_1803_the_view_keys_and_what_the_views_share"]),
        ("N7", "the gantt export changes its shipped name", V,
         b'tail = "" if view == "gantt" else f"-{view}"',
         b'tail = f"-{view}"',
         [PA + "test_TC_1809_each_view_exports_to_its_own_file"]),
        ("N8", "R opens on the split view", A,
         b'self._view = 0           # R always opens on the gantt view',
         b'self._view = 1           # R always opens on the gantt view',
         [PA + "test_AT_1803_the_view_keys_and_what_the_views_share",
          PA + "test_TC_1810_the_bindings_and_the_scroll_state",
          PA + "test_AT_1802_the_gantt_note_keeps_its_line_breaks[size0-PRES-V3-gantt-notes-118x30.txt]"]),
        ("N9", "x exports the gantt file whatever the view", A,
         b'                                           PRESENT_VIEWS[self._view])',
         b'                                           "gantt")',
         [PA + "test_AT_1803_the_view_keys_and_what_the_views_share"]),
        ("N11", "the long hint wording whatever the width", A,
         b'wide = names + vis(long_keys + tail) <= w - 2',
         b'wide = w >= 100',
         [PA + "test_TC_1808_the_hint_row_per_view[100]"]),
        ("N12", "a resize keeps the page cut for the old size", A,
         b'        self._scroll = 0                 # the pages are cut for the old size\n',
         b'',
         [PA + "test_TC_1810_the_bindings_and_the_scroll_state"]),
        ("N10", "tab stops at the last view instead of wrapping", A,
         b'self.action_view((self._view + delta) % len(PRESENT_VIEWS))',
         b'self.action_view(max(0, min(len(PRESENT_VIEWS) - 1, self._view + delta)))',
         [PA + "test_AT_1803_the_view_keys_and_what_the_views_share"]),
    ],
}


def main(root: Path, inc: str) -> int:
    mutants = MUTANTS[inc]
    files = sorted({m[2] for m in mutants})
    srcs = {f: (root / f).read_bytes() for f in files}
    h0 = {f: hashlib.sha256(b).hexdigest() for f, b in srcs.items()}
    arms = sum(len(m[5]) for m in mutants)
    print("tree:", root)
    print("increment:", inc, "· arms:", arms, "over", len(mutants), "mutants")
    for f in files:
        print("before:", f, h0[f], flush=True)
    bad = 0
    for mid, what, f, old, new, nodes in mutants:
        src, path = srcs[f], root / f
        eol = b"\r\n" if b"\r\n" in src else b"\n"
        old, new = old.replace(b"\n", eol), new.replace(b"\n", eol)
        assert src.count(old) == 1, (mid, src.count(old))
        print(f"\n== {mid} ({f}): {what}", flush=True)
        for node in nodes:
            node = node.encode().decode("unicode_escape").encode("latin-1").decode("utf-8") \
                if "\\u" in node else node
            try:
                path.write_bytes(src.replace(old, new, 1))
                if hashlib.sha256(path.read_bytes()).hexdigest() == h0[f]:
                    print(f"{mid} {node}: BAD (the edit did not apply)")
                    return 1
                r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                    "--color=no", node], cwd=root, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace",
                                   env=dict(os.environ, PY_COLORS="0",
                                            PYTHONDONTWRITEBYTECODE="1"))
            finally:
                path.write_bytes(src)
            h1 = hashlib.sha256(path.read_bytes()).hexdigest()
            assert h1 == h0[f], "the restore is not proven"
            tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
            verdict = {1: "KILLED", 0: "SURVIVED"}.get(r.returncode)
            bad += verdict != "KILLED"
            print(f"{mid} {node}: {verdict or 'BAD (exit %d)' % r.returncode} -- {tail}",
                  flush=True)
            print("  after:", h1)
    for f in files:
        print("\nafter all:", f, hashlib.sha256((root / f).read_bytes()).hexdigest())
    print("not killed:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]).resolve(), sys.argv[2]))

"""RED counterfactuals for increment 001: apply one mutation at a time to the
product source, run the named nodes, restore the bytes and prove the restore by
SHA-256. Run from the project root:  python .dev-flow/2026-09-30-batch-01/evidence/mutate_inc001.py
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.getcwd()
MODALS = os.path.join(ROOT, "taskboard", "modals.py")
TCSS = os.path.join(ROOT, "taskboard", "taskboard.tcss")

MUTATIONS = [
    ("M1 no change handler", MODALS,
     "    def on_text_area_changed(self, event: TextArea.Changed) -> None:\n        if event.text_area.id == \"f-notes\":",
     "    def on_text_area_changed(self, event: TextArea.Changed) -> None:\n        if False:",
     "test_the_preview_follows_the_typing_to_the_last_line"),
    ("M2 no initial render", MODALS,
     "yield Static(notes_preview(t.notes if t else \"\"),",
     "yield Static(notes_preview(\"\"),",
     "test_the_preview_paints_the_note_on_open"),
    ("M3 preview focusable", MODALS,
     "preview.can_focus = False",
     "preview.can_focus = True",
     "test_tab_walks_the_editor_and_save_works_from_the_keys"),
    ("M4 no focus bar", TCSS,
     "#task-box Button:focus {\n    border-left: tall #2dd4bf;",
     "#task-box Button:focus {\n    border-left: tall #0d1219;",
     "test_focus_mark_shows_on_every_one_row_control"),
    ("M5 threshold one too low", MODALS,
     "TASK_CHIPS_ONE_ROW = 122",
     "TASK_CHIPS_ONE_ROW = 121",
     "test_every_chip_stays_reachable_at_every_width"),
    ("M6 payload drops pinned", MODALS,
     "            \"pinned\": bool(self.query_one(\"#f-pinned\", Checkbox).value),\n"
     "            \"priority\": self._val(\"f-priority\"),",
     "            \"priority\": self._val(\"f-priority\"),",
     "test_save_payload_round_trips_every_field"),
    ("M7 rules leak to #modal-box", TCSS,
     "#task-box {\n    width: 100%;",
     "#task-box, #modal-box {\n    width: 100%;",
     "test_project_modal_keeps_its_box"),
    ("M8 preview does not follow the cursor", MODALS,
     "        scroll.scroll_to(y=scroll.max_scroll_y * notes.cursor_location[0] / last,",
     "        scroll.scroll_to(y=0 * notes.cursor_location[0] / last,",
     "test_the_preview_follows_the_typing_to_the_last_line"),
    ("M9 ctrl+v hint gone", MODALS,
     "Preview  [dim]ctrl+v paste · esc cancel[/dim]",
     "Preview  [dim]esc cancel[/dim]",
     "test_the_editor_paints_its_keys_in_full"),
    ("M10 notes back to 5 rows", TCSS,
     "#f-notes {\n    height: 1fr;",
     "#f-notes {\n    height: 5;",
     "test_the_notes_own_the_screen_while_writing"),
    ("M11 preview renders raw notes as markup", MODALS,
     "Text.from_markup(\"\\n\".join(_highlight_markup(ln) if ln.strip() else \"\"",
     "Text.from_markup(\"\\n\".join(ln if ln.strip() else \"\"",
     "test_the_preview_paints_markup_typed_in_a_note_as_text"),
    ("M12 Static parses the markup string (security S1)", MODALS,
     "    return Text.from_markup(\"\\n\".join(",
     "    return (\"\\n\".join(",
     "test_a_bracket_textual_would_parse_neither_crashes_nor_vanishes"),
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    for name, path, old, new, node in MUTATIONS:
        before = open(path, "rb").read()
        digest = sha(path)
        text = before.decode("utf-8")
        if text.count(old) != 1:
            print(f"{name}: BAD (anchor matched {text.count(old)} times)")
            continue
        open(path, "wb").write(text.replace(old, new).encode("utf-8"))
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "--color=no", "tests/test_edit_window.py", "-k", node],
                               capture_output=True, text=True, env=env, cwd=ROOT)
            tail = [ln for ln in r.stdout.splitlines()
                    if ln.startswith(("FAILED", "PASSED")) or " passed" in ln or " failed" in ln]
        finally:
            open(path, "wb").write(before)
        restored = sha(path) == digest
        verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
        print(f"{name}: {verdict} · node {node} · restore sha256 {digest[:16]} ok={restored}")
        for ln in tail[-4:]:
            print("    " + ln)


if __name__ == "__main__":
    main()

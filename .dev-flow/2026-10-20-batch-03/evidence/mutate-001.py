"""Mutation battery of increment 001 (batch 2026-10-20-batch-03), run from the project root
with NO_COLOR unset. One edit per arm, one node per run: exit 1 = RED (KILLED), 0 = GREEN
(SURVIVED), anything else = CRASH/BAD. Each file's hash is checked before and after."""
import hashlib, os, pathlib, subprocess, sys

T = "tests/test_modal_keys.py::"
M, K, C = "taskboard/modals.py", "taskboard/keymap.py", "taskboard/taskboard.tcss"
ARMS = [
    ("M1 y unbound in ConfirmModal", M,
     '                Binding("y", "press_button(\'yes\')", "Confirm", priority=True),\n', "",
     T + "test_TC_2406_a_confirmation_answers_y_and_n_and_not_enter[y-answer0]"),
    ("M1b y unbound (AT)", M,
     '                Binding("y", "press_button(\'yes\')", "Confirm", priority=True),\n', "",
     T + "test_AT_2406_a_confirmation_is_one_written_key[size0]"),
    ("M2 the wrap rule dropped", C, "#confirm-box .modal-title {\n    width: 100%;",
     "#confirm-box .modal-title {\n    width: auto;",
     T + "test_TC_2406_the_message_wraps_and_is_whole"),
    ("M2b the wrap rule dropped (AT)", C, "#confirm-box .modal-title {\n    width: 100%;",
     "#confirm-box .modal-title {\n    width: auto;",
     T + "test_AT_2406_a_confirmation_is_one_written_key[size1]"),
    ("M3 a key dropped before the words", K,
     "        if n_words:\n            n_words -= 1\n        else:\n            n_keys -= 1",
     "        if n_keys:\n            n_keys -= 1\n        else:\n            n_words -= 1",
     T + "test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys"),
    ("M4 the slash styled as a key", K, '                    out.append(" / ", style=HEX["dim"])',
     '                    out.append(" / ", style=KEY_STYLE)',
     T + "test_TC_2406_key_line_is_the_key_bar_style_and_keeps_its_keys"),
    ("M5 alt+s presses cancel", M, "FORM_KEYS = [Binding(\"alt+s\", \"press_button('save')\"",
     "FORM_KEYS = [Binding(\"alt+s\", \"press_button('cancel')\"",
     T + "test_TC_2407_alt_s_does_what_save_does[TaskModal]"),
    ("M5b alt+s presses cancel (AT)", M, "FORM_KEYS = [Binding(\"alt+s\", \"press_button('save')\"",
     "FORM_KEYS = [Binding(\"alt+s\", \"press_button('cancel')\"",
     T + "test_AT_2407_alt_s_saves_and_letters_type[size0]"),
    ("M6 alt+t opens the due calendar", M, "Binding(\"alt+t\", \"press_button('cal-f-start')\"",
     "Binding(\"alt+t\", \"press_button('cal-f-due')\"",
     T + "test_TC_2407_alt_t_and_alt_d_open_the_calendars[TaskModal-alt+t-f-start]"),
    ("M7 alt+i unbound", M,
     "                Binding(\"alt+i\", \"press_button('paste-img')\", \"Paste image\", priority=True)]",
     "                ]", T + "test_TC_2407_alt_i_pastes_an_image"),
    ("M8 ProjectModal without its date keys", M, "                *FORM_KEYS, *DATE_KEYS]\n",
     "                *FORM_KEYS]\n",
     T + "test_TC_2407_alt_t_and_alt_d_open_the_calendars[ProjectModal-alt+d-f-due]"),
    ("M9 ConfirmModal's key line dropped", M,
     '                                  ("⇥", "the buttons")]), id="confirm-keys")',
     '                                  ("⇥", "the buttons")][:0]), id="confirm-keys")',
     T + "test_TC_2407_every_button_has_its_key[ConfirmModal]"),
    ("M10 the editor's key line left empty", M,
     '        self.query_one("#task-keys", Static).update(key_line(TASK_KEYS, width - 2))',
     '        self.query_one("#task-keys", Static).update("")',
     T + "test_AT_2407_alt_s_saves_and_letters_type[size1]"),
    ("M11 MoveConfirm confirms on enter again", M,
     '                Binding("y", "yes", "", priority=True, show=False),',
     '                Binding("y,enter", "yes", "", priority=True, show=False),',
     T + "test_TC_2406_the_move_confirms_on_y_never_on_enter"),
    ("M11b MoveConfirm confirms on enter again (AT)", M,
     '                Binding("y", "yes", "", priority=True, show=False),',
     '                Binding("y,enter", "yes", "", priority=True, show=False),',
     T + "test_AT_2406_a_confirmation_is_one_written_key[size0]"),
    ("M12 TextPrompt's key line without alt+s", M,
     '            yield Label(key_line([("↵ / alt+s", "save"), ("esc", "cancel")], MODAL_KEYS_W),',
     '            yield Label(key_line([("↵", "save"), ("esc", "cancel")], MODAL_KEYS_W),',
     T + "test_TC_2407_every_button_has_its_key[TextPrompt]"),
    ("M13 a button key not bound (the law)", M,
     "                *FORM_KEYS, *DATE_KEYS]\n", "                *DATE_KEYS]\n",
     T + "test_TC_2407_every_modal_is_in_the_inventory"),
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

# HF-3 diagnosis — copy & paste in the notes and the capture pad

Date: 2026-11-05. Branch: `fix/hotfix-chain-move-paste`. Verdict first: **paste in the
capture pad is impossible, and copy-out of both surfaces is impossible**, because the
two surfaces are wired to two different clipboards and only one of them reaches the OS.

## The two clipboards in play

1. **The OS clipboard** — read by `taskboard.models.grab_clipboard_text()`
   (models.py:606): Win32 `OpenClipboard`/`GetClipboardData` via ctypes, control-stripped
   and length-capped, never raises. This is the one the operator means.
2. **Textual's app-local clipboard** — `App.clipboard` (textual 8.2.8), whose own doc
   says: *"only contains text copied in the app, and not text copied from elsewhere in
   the OS"*. It starts EMPTY every run and `App.copy_to_clipboard()` writes through an
   OSC 52 escape sequence, which **Windows Terminal does not honour** (write is dropped
   silently). So on the operator's terminal this clipboard is a black hole in both
   directions.

## PASTE

### Task editor notes (modals.py)
- `TaskModal.BINDINGS` (modals.py:764) binds `ctrl+v → paste_text` **priority=True**,
  so the screen wins over the TextArea's own native `ctrl+v`. The mixin
  (`ClipboardPasteMixin.action_paste_text`, modals.py:336) reads the OS clipboard via
  `grab_clipboard_text()` and inserts into `app.focused`. **This path works** — the
  2026-10 note in the mixin says exactly why it exists: *"Textual's native paste is
  unreliable on Windows, so we read the clipboard ourselves."*
- The pen does NOT swallow it: `TaskModal.action_paste_text` (modals.py:981) lifts the
  pen first (E5 CR-2), then delegates.
- The colour palette DOES swallow it while open: `ColourPalette` is a pushed screen that
  binds no `ctrl+v`, and the app seat binds none either, so the key dies inside the
  palette. Documented limitation — recolouring and pasting are different moments.
- `ProjectModal` (modals.py:1366) and `ClockModal` (modals.py:2374) have the same
  working binding.

### Capture pad (app.py)
- `CaptureView.BINDINGS` (app.py:1558-1566) has **no `ctrl+v` at all**. The pad is a
  `PadArea(InkArea(TextArea))`, and Textual's `TextArea.action_paste` (8.2.8) pastes
  from `self.app.clipboard` — the app-local one, which starts empty. **Result: pressing
  ctrl+v in the pad pastes nothing, always.** Root cause #1.
- Bracketed paste: Textual's `TextArea._on_paste` handles the terminal's bracketed-paste
  event and DOES insert — so a mid-size paste can work by luck while the same operator
  pressing ctrl+v gets nothing. Inconsistent behaviour, one root cause.

## COPY

- Nothing in the app ever writes the OS clipboard. `grep -r "ctrl+c"` in taskboard/: no
  hits. The app does not bind `ctrl+c` to quit (quit is `q`), so the key falls through
  to the focused widget.
- Textual's `TextArea` (and `Input`) bind `ctrl+c → copy` natively, but that calls
  `App.copy_to_clipboard()` = OSC 52, dropped by Windows Terminal. **Result: selecting
  text in the notes or the pad and pressing ctrl+c copies nothing the operator can paste
  anywhere else — the selection may as well not exist.** Root cause #2.
- The `?`/key bar never mentions copy or paste; the operator had no way to discover what
  WAS possible.

## The fix (root causes, both surfaces, one way)

- `models.py`: add `stash_clipboard_text(text)` — the write-side twin of
  `grab_clipboard_text()` (Win32 `SetClipboardData` via ctypes; `pbcopy`/`xclip -i` fixed
  argv elsewhere; never raises).
- `ClipboardPasteMixin` gains `action_copy_text`: reads the focused widget's selection
  (`TextArea.selected_text` / `Input.selected_text`), stashes it to the OS clipboard,
  and toasts when there is nothing selected. Renamed in spirit but kept as the same
  mixin so every modal that wires paste can wire copy identically.
- `TaskModal`/`ProjectModal`/`ClockModal`: add `Binding("ctrl+c", "copy_text", …,
  priority=True)` beside the existing ctrl+v.
- `CaptureView`: add BOTH `ctrl+v → paste_text` and `ctrl+c → copy_text` priority
  bindings, with the same two actions on the pad — the pad now behaves exactly like the
  notes.

## Tests that would have failed before

- Capture pad: `ctrl+v` pastes OS-clipboard text at the cursor (binding absent before);
  `ctrl+c` stashes the pad's selection to the OS clipboard (no such binding before).
- Notes: `ctrl+c` stashes the selection to the OS clipboard via the same
  `stash_clipboard_text` (before: OSC 52 black hole; asserted by monkeypatching the
  stash and checking the modal action calls it).
- `stash_clipboard_text` round-trips through `grab_clipboard_text` on win32.

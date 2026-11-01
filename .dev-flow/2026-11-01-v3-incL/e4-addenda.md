# E4 addenda — minor PDR notes carried into the build (orchestrator)

- **A-1 (ARCH-5):** `AddedList.on_screen_resume` calls `_paint()`, so names renamed under `@`/`#` show when the list is back on top (TC-4331b).
- **A-2 (ARCH-9):** the key row is `key_line(ADDED_KEYS + [("·", "read-only: nothing here edits a task")])`; when that is wider than `w − 2`, it is `key_line(ADDED_KEYS, w − 2)` (AllBoardsAgenda._paint's rule). LLR-4303.19 examples: at 118 the tail is shown; at 80 it is dropped and all 5 keys stay.
- **A-3 (SEC-4):** the pane wraps at most `room × (rw + 1)` characters of the cursor's note (`room` = pane lines left for the notes); when the note was cut, the last line reads `… more lines` in `HEX["dim"]` (no count); when not cut, P-V-7's `… k more lines` stands.
- **A-4 (ARCH-R2-1):** graph-proto-V.cw.md:208 example renamed TC-4364 → TC-4365b (it checks LLR-4304.5). Applied by the orchestrator.
- **A-5 (ARCH-R2-2):** `Board._to_dict`'s docstring states that `with_created` defaults to False for the team push and that every save path must pass True (`_serialized` does).
- **A-6 (SEC-R2-1):** `mention_names` on a huge mention-heavy note costs ~0.2 s a repaint; not fixed here — BACKLOG L-BL-4.

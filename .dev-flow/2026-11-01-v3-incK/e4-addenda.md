# E4 addenda — minor PDR notes carried into the build (orchestrator)

- **A-1 (ARCH-12):** LLR-4403.30 and LLR-4403.31 are WITHDRAWN. The rail recomputes the hits of a changed note on every pad change (cached corpus + per-text hit cache, LLR-4403.29); no 1 s scoring pause, no stale rail lines. Any graph node/example that encodes the pause is void (the store-write debounce of F-7 stays).
- **A-2 (ARCH-13):** an `alt+o` pick is keyed by the note's exact text, so editing the note resets the pick. As designed; no change.
- **A-3 (SEC R2-1):** `action_quit`, from any screen, first retries a held pending store write once (Inbox pending record); on failure it exits anyway (recorded risk: the note stays in `dumped`, recoverable with `alt+u` for 7 days).
- **A-4 (SEC R2 INFO):** a load that fails with `OSError` (the file exists but cannot be read now) is not unreadable CONTENT: no `keep_aside` copy, the stamp is not taken (SEC-4), and the notice reads `inbox.json could not be read right now; its notes merge back on the next save.` Unparseable content keeps its LLR-4407.8 path and notice.

# E4 addenda — minor PDR notes carried into the build (orchestrator)

- **A-1 (SEC-R2-1):** `_unshadow_alt_digits` pops each of `"\x1b0"`..`"\x1b6"` only if its current value equals the Textual 8.2.8 glyph (`º ¡ ™ £ ¢ ∞ §`), inside `try/except Exception`; it never raises at import.
- **A-2 (C-2 / ARCH-5):** the TaskDetails Notes label is `Notes  ::c:: … ::  r o y g b v`, each code letter in its tone.
- **A-3 (ARCH-14):** TC-4249 names only the parser test; the stale "TC-4249 dropped" line in graph-proto-M1 is obsolete.
- **A-4 (SEC-5):** the palette callback re-validates the target line; if it changed, nothing changes and notice N5 shows.
- **A-5 (SEC-9):** TC-4209 asserts every emitted tone ∈ {mut, soon, over, green, orange, blue, violet}.

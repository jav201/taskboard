# Inc L — PDR round 2 (blocking-only re-review) — architect

**Verdict: PASS-WITH-NOTES** — ARCH-1 (HIGH) is closed, and ARCH-2 and ARCH-3 are applied consistently. The corrections introduce no new MAJOR or HIGH finding. There are 2 notes (1 MINOR, 1 INFO), and neither blocks E4.

The scope is the one round 2 asks for: ARCH-1..3 and the side effects of the round-1 corrections, SEC-1's `with_created` default first. Ruled MINOR items are not reopened. I compared commit `aa40b62` against `966020f`.

## ARCH-1 — closed (`executed`)

I wrote a pure-Python probe, `C:\Users\jjgh8\AppData\Local\Temp\incL-r2\probe.py` (scratch, outside the repo). It implements the interface sort, unknown rows by (lane, pos) and then dated rows by (at, lane, pos), and 7 mutants of it. I ran both on every shuffled-input example now in the design: interfaces `added_order` TC-4364 and TC-4366b, and V `added_order` TC-4365 and the three TC-4364 arms.

**The reference sort is correct.** On all 6 examples it gives exactly the expected order the design states. That includes `A B E C D`, `D C E B A`, `w1 h1 w3 w2 h2 w4` and `w1 w5 h1 w3 w2 h2 w4`.

**Every mutant turns RED on at least one example:**

| Mutant | Examples RED | Notes |
|---|---|---|
| M1 dated rows by moment only | 4 of 6 | iface TC-4364 gives `A B E D C`; both V tie arms keep input order |
| M2 unknown rows in input order | 4 of 6 | iface TC-4364 gives `B A E C D`; V TC-4365 gives `h1 w1 …` |
| M3 unknown rows last | 4 of 6 | V TC-4365 gives `w3 w2 h2 w4 w1 h1` |
| M4 the round-1 mutant (M1 + M2) | 6 of 6 | |
| M5 dated tie broken by (pos, lane) | 1 | only V TC-4364 tie arm 1 |
| M6 unknown rows by (pos, lane) | 1 | only the V F-V archived arm, which gives `w1 h1 w5 …` |
| M7 file position only (HLR-4303 NC) | 4 of 6 | |

The RED orders V names in its NC text for TC-4365 match what the probe printed. The NCs of LLR-4304.4 and LLR-4304.5 now point at inputs on which they fire, and HLR-4303's NC ("order by file position only: TC-4364 RED") holds.

## ARCH-2 — applied consistently (`executed`, by reading)

The three places agree:

- **HLR-4302's NC** names TC-4316 (01-requirements.md:65).
- **LLR-4302.5's threshold** names the birth record (01-requirements.md:141).
- **D's fixture note** gives the exact line (graph-proto-D.cw.md:15): `{"task":"ta","from":null,"to":"Doing","at":"2026-10-20T09:00:00"}`. TC-4316 arm 2 asserts that "ta" gains no `created` and states the back-fill NC (graph-proto-D.cw.md:117).

The record is valid input to `history.read`: `task`, `to` and `at` are str and `from` is None (history.py:52–80). A back-fill mutant therefore has a birth to copy, and TC-4316 kills it. History is a separate file (`history_path`, history.py:19), so the byte oracle of LLR-4302.4/.5 is unaffected.

## ARCH-3 — applied consistently (`executed`)

- **LLR-4304.13** is rewritten (aware means not valid; 3 arms, `c`/`h`/`?`). **LLR-4304.16** is withdrawn in three places: the requirements (:229), the ledger and the trace (e2-trace.txt:70).
- **`added_moment`** has the same rule in the interface (graph-interfaces.cw.md:46) and in V (graph-proto-V.cw.md:193): one `except ValueError`, and an aware value gives None. No `astimezone` call remains in any func; the word appears only in NC text and in P-V-2's superseded history.
- **The NC is machine-independent.** "Convert or strip" yields source `c` on any zone. The project requires Python >= 3.12 (pyproject.toml:12), and on it `fromisoformat` parses both `…Z` and `…+00:00` to aware UTC (probe). So TC-4373 and TC-4373b give None on every runner. The UTC-runner hole from round 1 is gone.

## Side effects of the corrections — no new MAJOR or HIGH (`executed`)

**Census of `_to_dict` callers** (`grep -rn _to_dict taskboard tests`):

- **Production code** has exactly two callers. `_serialized` (models.py:1071–1072) passes `with_created=True` in the design (graph-proto-D.cw.md:73), and it is the only path to `save` and `save_atomic` (models.py:1078, :1083). `TeamState.push` (team_sync.py:157) takes the default, as intended. No other `asdict(task)` serialization exists (models.py:1059 is the only one). Every caller that must persist `created` therefore passes True.
- **The team round trip cannot lose `created`.** `pull` skips the user's own file (team_sync.py:190), and `foreign_tasks` builds display-only Tasks. A local `created` is never overwritten by its own pushed record.
- **Tests that call `_to_dict` directly** need no `created`:
  - test_cascade.py:42 `_dump` is compared before and after with the same call on both sides (:150, :158).
  - test_marks_directory.py:254, :263 read `mark`.
  - test_boards_move.py:188 dumps a Project.
- **Tests over pushed records** assert only `title`, `owner`, `pushed_at`, `milestone`, `mark` and `@` substrings (test_team_sync.py:90–112, test_marks_directory.py:404–408, test_people_directory.py:323–327, test_milestones.py:399–401). None expects every field and none expects `created`.

## Findings

### ARCH-R2-1 — MINOR — the F-V archived-arm example is filed under TC-4364 but tests LLR-4304.5
- **Anchor:** graph-proto-V.cw.md:208
- **Seen:**
  - The "reversed F-V input, show_archived True" example checks how unknown rows are ordered among themselves. That is LLR-4304.5's subject (TC-4365), not the tie-break of LLR-4304.4.
  - It is the only example that kills M6 (unknown rows by (pos, lane)).
  - e2-trace.txt:47 traces LLR-4304.5 to the single TC-4365 example.
- **Proposal:** relabel the example TC-4365b, or have the E4 tester place it in the TC-4365 test. It costs nothing either way, because both tests run. Not blocking.

### ARCH-R2-2 — INFO — the default `with_created=False` fails toward losing data, not toward exposing it
- **Anchor:** `Board._to_dict` (graph-proto-D.cw.md:57)
- **Seen:** a future persistence path that calls `_to_dict` without `with_created=True` would silently drop `created` from the board file. D3 cannot recover a dropped stamp, because the history inference gives only `≈`. Two facts bound the risk today:
  - **Its only guard is a test.** TC-4318 asserts that `_serialized` keeps `created`.
  - **The default is forced.** Putting the default the other way round would mean editing team_sync.py, a 5th source file.
- **Proposal:** none for this increment; the risk is accepted. Add one line to the `_to_dict` docstring at E4 ("persistence must pass with_created=True"), state `planned`, so the next caller sees it.

## Evidence checklist
- [x] Constraints: unchanged from round 1. No new dependency, and team_sync.py is still untouched (graph-proto-D.cw.md:290).
- [x] Alternatives: `n/a — ruled at round 1` (ARCH-3 remove-vs-guard, SEC-1 default direction).
- [x] Risks: ARCH-R2-2. Round 1 §Risks stand.
- [x] Each claim above names its evidence state. The probe run and the greps are `executed`; the E4 guard run is `planned`.

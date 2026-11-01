# Inc L — PDR security review, round 2 (blocking-only re-review)

**Verdict: PASS-WITH-NOTES.** SEC-1, SEC-2, SEC-3 and SEC-4 are closed in the design. Each fix sits on a named node with an example and a negative control (NC). The corrections add no HIGH and no MEDIUM. They leave one LOW (SEC-R2-1), a part of SEC-4 the A-3 cut does not cover. All the mitigations are `planned`: the design specifies them and nothing has run them. I re-verify them at the increment gate on the E4 RED/GREEN runs.

## Scope reviewed

- What changed: `git diff 966020f aa40b62 -- .dev-flow/2026-11-01-v3-incL/` (requirements, ledger LED.4, interfaces, graph-proto-D/V/S, e4-addenda, the E4 briefs), checked against `03-pdr-rulings.md` round 1.
- Code census at `aa40b62` (product code unchanged since base): `taskboard/` writer paths (`_to_dict`, `asdict(`, `json.dump`, `write_text`, `save_atomic`). Also `team_sync.py`, `report_html.py`, `report.py`, `boards.py` (`_log`, `move_project`) and `views.py` (`mention_names`).
- One read-only probe: `C:/Users/jjgh8/anaconda3/python.exe -I`, scratch script in `%TEMP%/incL-sec2/`. It printed `taskboard.__file__` = `…\capture-proto\taskboard\__init__.py`. Data was synthetic. State: `executed`.

## Round-1 findings: closure check

### SEC-1 — `created` in the team push: CLOSED (design)
- **Nodes:** `Board._to_dict` (graph-proto-D.cw.md:56–66), with `in: … bool with_created = False`. Its func has two drops:
  - It drops the field when it is None or `not with_created`.
  - It also runs `if not with_created: extra.pop("created", None)`, so **`extra["created"]` is dropped too**. A raw non-str value cannot reach the push.
  - `asdict` deep-copies, so `item.extra` is never changed.
- **`Board._serialized`** (:70–76) now passes `with_created=True` for projects and tasks, so `created` still reaches the board file. **`TeamState.push`** (:78–85) has no code change and calls `_to_dict(t)` with the default.
- **Entity and edge:** the entity `[I/O: board.<user>.json]` (:175) says the file never holds `created`. The edge at :201–202 has the same condition.
- **Examples:** TC-4318 has 4 arms:
  - the default call on a stamped task;
  - the default call on a raw `5` in `extra`, which stays in `extra` afterwards;
  - `_serialized` holds both;
  - an end-to-end push writes 0 of 2 records with the key.
- **NC:** a default of `True` makes the test fail (RED).
- **Requirements:** LLR-4302.7 is added. LLR-4302.1's threshold is moved to the saved record (01-requirements.md:133); the D graph had flagged this mismatch. The README team note is withdrawn (:182, :290).
- **Other outbound writers:** none carries `created`. Census at `aa40b62`:
  - `_to_dict` is called only by `_serialized` (models.py:1071–1072, the only path to `save` and `save_atomic`) and by `team_sync.py:157`.
  - `team_sync` never reads or copies `history.jsonl` (grep: no hits).
  - `report_html.extract` and `report.py` build their output from named fields. No base code names `created`, and neither iterates `extra`.
  - `boards._log` (move logs) writes counts and names only. `move_project` saves through `save_atomic` (with_created=True), which is the local destination board and is correct.
  - The marks, people and registry writers use their own dataclasses.
  - The `x` export renders frames.
  - Only one indirect route remains. `_rescue_task` puts the raw JSON of a task entry that could not be parsed into `notes`, and `notes` are pushed. That entry's `created` travels with it. This was already true at base for every key of a corrupt entry, it needs corrupt input, and it is not a `created` key. No finding.
- **State:** finding closed in design. Mitigation `planned` (TC-4318 is not yet run; first run is the tester's RED-on-base run).

### SEC-2 — RecursionError from `history.read`: CLOSED (design)
- **Interface:** `added_rows` func (graph-interfaces.cw.md:32) catches `OSError, ValueError … or RecursionError` and treats that board as having no births. The group V node says the same (graph-proto-V.cw.md:177), and so does `AddedList.compose` (graph-proto-S.cw.md:41).
- **Requirement:** LLR-4304.12 (01-requirements.md:223–224) names all three exceptions. Its third arm is a line nested 10 000 deep.
- **Example:** TC-4372c (interfaces :39, V :185). Its NC is "guard without RecursionError: RED".
- **Depth:** 10 000 is enough. The interpreter's default recursion limit is 1 000, and my round-1 probe raised at that order.
- **Backlog:** L-BL-2 is the fix at the source.
- **State:** mitigation `planned`.

### SEC-3 — non-str task id: CLOSED (design)
- **`added_rows`:** births are keyed only by a str `rec["task"]`, and the lookup runs only when `isinstance(task.id, str)` (interfaces :32; V :177).
- **`_added_pane`:** `titles = {t.id: t.title for t in row.board.tasks if isinstance(t.id, str)}` (V :136).
- **Requirement:** LLR-4304.17 (01-requirements.md:232–233).
- **Examples:** TC-4377 covers the rows (V :187, interfaces :40) and the pane, both with the cursor on the odd-id task and with an `after:` that points at it (V :144). The NC is the unguarded lookup, which raises TypeError.
- **No other site hashes a task id:**
  - `added_order` sorts by `(lane, pos)` / `(at, lane, pos)`.
  - `first_created` takes a min over `at`.
  - The S cursor keys on `(lane, pos)` (S :122).
  - `enter` passes the id to `open_on_board` → `jump_to`, which compares with `==`. That is the base behaviour of `A` (S :445).
  - `state_boxes` uses `list.index`, which compares with `==`.
- **State:** mitigation `planned`.

### SEC-4 — wrapping a huge note: CLOSED for the wrap (design)
- **Where:** addendum A-3 (e4-addenda.md:5) and `_added_pane` (V :136).
- **The cut:** before `notes_text`, the note is sliced to `nroom × (rw + 1)`, with `cut` returned. When cut, `render_added_list` ends the pane with `… more lines` (V :59).
- **Examples:** TC-4335b, plus TC-4332b (5 MB in under 50 ms, NC no cut). TC-4335 keeps the count under the cap.
- **Probe:** `strip("\n")` plus the slice of 5 MB takes 0.0 ms.
- **What is not covered:** see SEC-R2-1.

## New findings (round 2)

### SEC-R2-1 — `mention_names` still scans the whole note on every paint  [LOW]
- **What:** the A-3 cut bounds `notes_text` and the wrap only. The meta line still calls `mention_names(task, people)` (V :150), which runs `mention_ids(task.notes)` over the **uncut** note (views.py:3619–3623) every time the pane paints.
- **Where:** `_added_meta` (graph-proto-V.cw.md:150) and the performance note (:51), which counts `mention_names` as built for the cursor's task only but does not bound it by note length.
- **Seen:** probe `%TEMP%/incL-sec2/p.py`, run on synthetic notes of about 5 MB:

  | Note content | `mention_names` per call |
  |---|---|
  | `"lorem "` repeated | 0.2 ms |
  | `"@ana lorem "` repeated | 198 ms |
  | `"@"` repeated | 69 ms |

  TC-4332b uses `"lorem "` repeated, so it passes while a note full of mentions still costs about 0.2 s on every key and resize.
- **Why it matters:** this is the same low-impact class as SEC-4: a crafted board in any registered folder makes the list sluggish. There is no crash and no effect on data.
- **Recommendation (non-blocking, choose one):**
  - (a) Give TC-4332b a second arm with a mention-dense 5 MB note, and compute the meta line's mentions once per cursor change, cached by `(lane, pos)`, not once per paint.
  - (b) Accept it as is and record a BACKLOG line.
  - Do not bound the scan by A-3's cap: that would silently drop people mentioned late in the note.
- **Evidence state:** finding `executed` (probe). Mitigation `n/a — operator's choice`.

## Checked, no new HIGH or MEDIUM

- **ARCH-3 (offset-aware value → None):** this lowers risk. It removes the `astimezone()` path. It also guarantees that every `at` is naive, so the `(at, lane, pos)` sort cannot raise TypeError by comparing a naive datetime with an aware one.
- **ARCH-5 (`on_screen_resume` repaints):** it repaints only, from rows already read. No new read and no write.
- **ARCH-9 (the read-only tail on the key row):** a constant string. No board text.
- **The `_to_dict` default flip:** it has no security effect on the local board file, because `_serialized` passes `True`. The test callers listed in D :59 are a correctness concern, which the E4 guard run covers.
- **Secrets / PII in the corrected design files:** none. Fixtures are synthetic. No new dependency, no network access, no new external tool.

## Evidence checklist

- ✓ Each finding has what, where, why and recommendation: SEC-R2-1 has all four.
- ✓ Each finding has a severity: SEC-R2-1 is LOW.
- ✓ No secret values appear in this output: none exist in scope.
- ✓ The verdict is explicit: PASS-WITH-NOTES. There is no HIGH. SEC-1..4 are closed in the design, and their mitigations are `planned` until the E4 runs.
- ✓ The new data flow was checked for scope and blast radius. The team push carries no `created`, neither as a field nor from `extra`. The census found no other path to an outbound file. No new tool or integration is added.

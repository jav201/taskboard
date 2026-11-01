# Inc K — E5 security review (increment gate)

**Verdict: PASS-WITH-NOTES.** HIGH 0 · MAJOR 0 · MEDIUM 0 · LOW 5 · INFO 3.

The code applies every PDR mitigation (SEC-1..SEC-8, R2-1, R-E4-1) as the rulings designed it. I confirmed each one with probes on synthetic temp homes and with the targeted tests. The on-disk cap holds exactly on Windows (`\r\n`). No store value reaches a path outside the store folder, the pad images folder or `images/<id>/`. Store text is never read as markup. A failed store write keeps the dump or undo as a pending record. The five LOW findings are robustness and notice gaps, and none of them loses data silently. No secret, dependency, network path or outbound data is added.

## Scope reviewed

- Change: `git diff 545c18a f931070 -- taskboard/ README.md tests/`. I read all of `taskboard/inbox.py`, and from `taskboard/app.py` the capture section (`PadArea`, `CaptureView`, `ReviewList`, painters :1336-2211, `check_action` :2306, `_retry_pending_once`/`action_quit` :2476-2503). I skimmed `taskboard/suggest.py` (regexes, caps) and read the `keymap.py` and `README.md` hunks.
- Base helpers I read: `models.write_atomic`, `models.clean_strings`, `models.grab_clipboard_image`, `boards.keep_aside`, `boards.file_lock`, `boards.peek_board`, `history.append` and `app.board_lanes`. I also read PIL 12.2.0 `ImageGrab.grabclipboard` (the win32 CF_HDROP decode).
- Design: `03-pdr-security.md`, `03-pdr-security-r2.md`, `03-pdr-rulings.md`, `e4-addenda.md`, `e4-integration.md`, `01-requirements.md` §Recorded risks.
- Probes: `%TEMP%/incK-e5sec/p1.py`, `p2.py`, run with `C:/Users/jjgh8/anaconda3/python.exe -I` under `env -u NO_COLOR`. Each printed `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`. They used fresh `tempfile.mkdtemp` homes and synthetic data only, and never touched `~/.taskboard`.
- Targeted tests: `pytest tests/test_inbox_store.py tests/test_capture_view.py -k "4556 or 4686 or 4687 or 4650 or 4677c or 4683 or 4685 or 4599 or 4550 or 4559 or 4534 or 4628 or 4634"` gave **48 passed**. State: `executed`.
- I edited no product code, test or record except this file. `../incK-mut`, `../incK-base` and `../incK-marks` were not touched.

## PDR mitigations: verified in code

| Id | Where | Verified by | State |
|---|---|---|---|
| SEC-1 multiset of unseen entries only | `inbox.py:313-327` (`Counter` budget), `:640-643` (`unseen` = fresh entries whose (task, board) this Inbox did not hold) | p1: a seen entry `follow up` re-typed after another window wrote → kept, union reported. An unseen foreign dump against two typed copies → one copy kept. TC-4599 passes. | executed, approved |
| SEC-2 lone surrogates refused | door `_parse` `:462-464` (encode probe inside the `ValueError` try). `dump_note` `:841-847` (note and new name). `_commit` `:596-600` (`UnicodeError` → `OSError` before `write_atomic`). `on_unmount` catches `(OSError, ValueError)` `app.py:1770`. | p1: `{"pad":"a\ud800b"}` → unreadable, `.corrupt` byte-equal, pad `""`. A surrogate note into another board and into the open board → refused, board bytes unchanged. A `_commit` with a surrogate → worded OSError, no `.tmp` left. TC-4534 and TC-4683 pass. | executed, approved |
| SEC-3 whole record + depends-on | `_unchanged` `:981-993` (`asdict` vs the rebuilt record), `_needed` `:996-998`, both undo paths `:1029-1032`, `:1076-1079` | p1/p2 on another board: phase, priority, due_date, urls, pinned and `extra` each give `changed` with board bytes unchanged. A dependent task gives `needed`. Unedited → `undone`. Open-board undo after a reload → `undone`. TC-4550 and TC-4559 pass. | executed, approved |
| SEC-4 failed read keeps the old stamp | `load` `:497-514` (`read_failed` → no stamp, no `keep_aside`), `refresh` `:529-532` | p1: `open` raising a sharing violation at load → `_stamp is None`. The next write gives the stored pad `p\n____\nq`: both kept. TC-4685 passes. | executed, approved |
| SEC-5 quit with an unsaved pad writes first | `app.py:2486-2501`. A key or cursor move disarms (`:1728`, `:1736`). | Read, plus TC-4686/TC-4687 pass (held lock → warn; a second quit exits; a key between re-arms). | executed, approved |
| R2-1 / A-3 retry pending before quit | `app.py:2476-2484`, `:2502` | Read only. No test covers it (see K-SEC-3). | read |
| SEC-6 link/junction check | `_links_ok` `:745-757`, used by `_drop_pad_copies` (`:908`, `:974`) and `_images_back` (`:1014-1015`) | p2: the pad images folder as a junction to an outside folder → the dump succeeds and the outside `a.png` is kept. The task image folder as a junction → undo refuses earlier (SEC-3: the image path resolves elsewhere, `changed`), and the outside file is kept. TC-4650 passes. | executed, approved |
| SEC-7 reserved names | `RESERVED_STEMS` `:47-53`, stem rule `:140` | p1: `con .png`, `conin$.png`, `COM¹.png`, `com0.png`, `nul.tar.png` → refused; `ok.png` → accepted. TC-4628 passes. | executed, approved |
| SEC-8 lane test by string first | `app.py:2046-2052` (`normcase(abspath)` against lane paths before `undo_dump`). `_where` `:1918-1929` is a string compare + `name_for` (pure). | Read, plus TC-4556 passes (UNC `\\host\share\board.json` → refusal, 0 `stat`/`samefile` calls on it). | executed, approved |
| R-E4-1 cap counts bytes on disk | `_commit` `:603-606`. `write_atomic` opens text mode with utf-8 (`models.py:738`), so each structural `\n` becomes `\r\n`; string newlines are JSON-escaped. | p1, real filesystem on Windows: a write sized to the cap → `getsize == 8 388 608`. One byte more → OSError, file unchanged at 8 388 608. A pad of `\n`s (escaped) → 8 388 607, below the cap. The reload is readable. TC-4677c passes. | executed, approved |
| Traversal via the store | `_entry` `:416-444`: `task` matches `ID_RE`, images pass `_image_ok`, exact types, non-blank text/board | p1: `task` `../x` and `a/b`, image `..\a.png` and `a:b.png`, reserved image names, `new_project: 1` and blank text → each entry dropped. `undo_dump` re-validates (`:1005`). | executed, approved |
| Markup / control text | Every capture `notify` passes `markup=False`. The painters (`hit_text`, `capture_head`, `capture_hint`, `rail_rows`, `review_rows`) build `Text` by `append`. `border_title` is `Text` or a constant. No `from_markup` in app/inbox/suggest. Store strings pass `clean_strings`. | grep census plus TC-4634 pass (`[red]x[/red]` and `[@click=app.quit]q` literal) | executed |
| No loss on failed writes | `write_pad` `:649-656` keeps the record/drop as pending on any OSError. Pending survives `refresh` and is applied first on the next write (`:620-639`). `pad_now` `:663-678`. `_dump`/`action_undo` keep the pad consistent (`app.py:1886-1896`, `:2071-2078`). | Read and traced. RISK-ARCH-4 (exit before a retry) is a recorded risk. | read |
| Other board write | `_dump_other` `:913-976`: existence check before the lock, `peek_board`, s0/s1 and pre-save stamp checks, `save_atomic`, birth record after the save (`history.append` swallows OSError) | Read. The PDR §Checked-and-sound items still hold. | read |
| `suggest.py` | `WORD_RE` `:32` cannot backtrack catastrophically (a separator is required between groups). `NOTE_CHARS` 10 000, `DOC_CHARS` 100 000. It reads and writes no file. | Read | read |

## Findings

### K-SEC-1 — undo can raise after the board save and crash the app  [LOW · impl]
- **What:** `undo_dump` saves the board without the task, then calls `_images_back`. That function's `folder.mkdir(parents=True, exist_ok=True)` (`inbox.py:1101`) and `_free_name` (`:1111`, raises at 10 000) sit outside its `try`. `CaptureView.action_undo` (`app.py:2054`) does not catch, so the exception leaves a key handler and Textual ends the app.
- **Seen (p2, executed):** `inbox-images` is a regular file, a note with no image is dumped, then undone → `FileExistsError` from `undo_dump`. The task is already gone from the board. The note is not back in the pad, and the store still holds the entry.
- **Impact:** the app exits on a destructive path. Any held pending record is lost (RISK-ARCH-4). The note text comes back only through a later `alt+u` (the "gone" path). The precondition is an odd folder state (the folder name taken by a file, an unwritable home), so the blast radius is low.
- **Fix:** move `folder.mkdir` and `_free_name` inside `_images_back`'s `try`, so an OSError stops the loop and the files stay in the board (P-S-12). Return the renames so far. Add a TC: `inbox-images` is a file, then undo → state `undone`, the note is back in the pad, the app still runs. *NC:* mkdir outside the try → RED.

### K-SEC-2 — addendum A-4's notice did not land: an OSError at load says "the pad starts empty"  [LOW · impl]
- **What:** `Inbox.load` records a failed read as `{"unreadable": True, "backup": None}` (`inbox.py:510`). `CaptureView.on_mount` then shows `inbox.json could not be read and no copy could be kept; the pad starts empty.` (`app.py:1599-1601`). A-4 (e4-addenda) fixes the wording `inbox.json could not be read right now; its notes merge back on the next save.`. grep finds that string in no source file and no test.
- **Impact:** nothing is lost, because the stamp stays None and the next write unions (SEC-4, verified). But the notice tells the user the notes are gone. A user may then re-type them, which gives duplicates after the merge, or delete `inbox.json` to "repair" it, which is real loss.
- **Fix:** mark the transient case in `load_report` (for example `"read_failed": True`) and show A-4's string for it. Add a TC on the shown notice. *NC:* the old wording → RED.

### K-SEC-3 — the R2-1 / A-3 retry before quit has no test  [LOW · impl (test)]
- **What:** `_retry_pending_once` (`app.py:2476-2484`) is correct when I read it, but no test sets a pending record and quits from the main screen. TC-4686/4687 cover only the view-on-stack branch.
- **Fix:** add a TC: a store write fails at dump (pending held), the store is unlocked, the view is closed with esc, then `ctrl+q` → `inbox.json` holds the entry and the pad lacks the note. *NC:* skip the retry → RED.

### K-SEC-4 — undo deletes a dump-created project together with the user's edits to it  [LOW · design-gap]
- **What:** `_undo_open` and `_undo_other` remove the project when `entry.new_project` is set and no task uses it (`inbox.py:1037-1044`, `:1081-1083`). SEC-3 compares the task record but not the project record.
- **Seen (p2, executed):** a dump made a new project, the user renamed and recoloured it, then undo → `undone`, and the project and its edits are gone.
- **Impact:** a small loss of project metadata (name, colour and any later settings) on an empty project, with no notice. This is the same class of silent edit loss as SEC-3, at a smaller scale.
- **Fix (prefer removing behaviour):** the entry does not hold the project's name or colour as the dump created them, so the undo cannot tell an edited project from an unedited one. The simplest fix is to never delete the project: leave it empty and say so in the undo notice. If deleting it must stay, compare `asdict(project)` against the created record, which needs the name and colour stored in the entry (a store-shape change). Add a TC arm for a renamed project.

### K-SEC-5 — `_free_name` can produce a name that the image-name rule rejects  [LOW · impl]
- **What:** `_free_name` appends `-<k>` to the stem with no length check (`inbox.py:722-732`). A 128-character name that is taken becomes 130 characters, so `image_name("img: " + name)` returns None. The same happens in `_images_back` renames through `_renamed` (`:1111`, `:1122-1132`).
- **Seen (p2, executed):** attach of a second 128-character file → name length 130, not an image line.
- **Impact:** the copied file is orphaned in `inbox-images/` and is never moved or cleaned up. The `img:` line dumps as note text (or as the title, if it is the first line). This is not exploitable, but it leaves user screenshots in a folder nothing manages.
- **Fix:** cut the stem so that `len(stem-k+suffix) ≤ 128`, and assert `_image_ok(candidate)` in `_free_name`. Add a TC with a 128-character name taken twice.

### INFO
- **I-1 Retention (ARCH-11, still for the operator).** A dumped note's text stays in `inbox.json` for 7 days even after its task is deleted, and an `at` stamped in the future is never pruned (`prune_dumped` `:333-344`). Pad images of notes deleted by hand stay in `inbox-images/` forever. `Inbox.load` adds one `.corrupt-N` copy (up to 8 MiB) per launch while a corrupt store is never written; people and marks follow the same pattern. The README row says where the pad lives and "kept 7 days" for undo, but not that the text outlives its task. Suggest one README sentence.
- **I-2 Surrogate image names (defence in depth).** `_image_ok` accepts a lone surrogate (p1: `a\ud800.png` → True). This cannot be reached today: PIL 12.2.0 decodes CF_HDROP with strict `utf-16le`, so such a file list makes `grab_clipboard_image` return None. If it ever became reachable, each store write would fail until the line is removed. A one-line `name.encode("utf-8")` check in `_image_ok` closes it for good.
- **I-3 Backlog hand-off.** RISK-ARCH-4, RISK-SEC-2, RISK-SEC-9/10/11 and RISK-P-S-11/12/17 are listed in `01-requirements.md` §Recorded risks, which says the orchestrator moves them to `.dev-flow/BACKLOG.md` at E5. Do that, with K-SEC-1..5, before the batch closes, so the deferred mitigations are not lost (the same lesson as Inc L SR-5).

## Evidence states

| Id | Finding | Mitigation |
|---|---|---|
| K-SEC-1 | `executed` (p2) | `planned` |
| K-SEC-2 | `read` (grep + code) | `planned` |
| K-SEC-3 | `read` (test census) | `planned` |
| K-SEC-4 | `executed` (p2) | `planned` |
| K-SEC-5 | `executed` (p2) | `planned` |
| SEC-1..SEC-8, R-E4-1 | — | `executed`, `approved` (table above) |
| R2-1 / A-3 | — | `read` (code correct, untested) |

## Evidence checklist
- ✓ Each finding has what, where, why and a fix: K-SEC-1..K-SEC-5 above.
- ✓ Each finding has a severity and a tag: all five are LOW; four are impl (K-SEC-1, 2, 3, 5) and one is a design-gap (K-SEC-4).
- ✓ No secret values appear in this output. A diff scan for keys, tokens, emails and the profile name found none, and every fixture mention is `@username_subject`.
- ✓ The verdict is explicit: PASS-WITH-NOTES. There is no HIGH or MAJOR. Every PDR mitigation is applied and I verified it (`executed`), except A-3, which is `read` (K-SEC-3). This clearance is not the operator's authorization.
- ✓ New tool or integration: none. No network, no new dependency, and no data leaves the machine. The new local surfaces (the store, `inbox-images/`, lane boards) are scoped as the table above shows.

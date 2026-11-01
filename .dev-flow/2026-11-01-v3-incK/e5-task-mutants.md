# E5 mutants — Inc K new arms (mechanical task)

Run each mutant below in the COPY `C:/Users/jjgh8/Github/taskboard-wt/incK-mut`, a detached worktree of
the head commit `<HEAD>` (the orchestrator fills `<HEAD>`; the copy is made with
`git -C C:/Users/jjgh8/Github/taskboard-wt/capture-proto worktree add --detach ../incK-mut <HEAD>`).
NEVER edit the main worktree `capture-proto` except to write the two output files named at the end.
Interpreter: `C:/Users/jjgh8/anaconda3/python.exe` — never the shell's `python`. Run every pytest with
`env -u NO_COLOR`, cwd = `C:/Users/jjgh8/Github/taskboard-wt/incK-mut`, and first print
`taskboard.__file__` once (`env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -c "import taskboard; print(taskboard.__file__)"`)
to prove the copy is imported; if it does not point inside `incK-mut`, stop and report — run nothing.
Remove nothing: no file, folder or worktree is deleted by this task.

**Baseline (once, before M01).** On the unmutated copy run
`env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -p no:cacheprovider tests/test_inbox_store.py tests/test_suggest.py tests/test_capture_view.py`
(no `-x`). Record every failing test node id as BASELINE-RED in the transcript and in the result file.
Add `--deselect <node id>` for each BASELINE-RED test to every mutant run below. A mutant whose row's
tests are all BASELINE-RED is recorded `NOT JUDGED (baseline red)`, not SURVIVED. (Known risk: TC-4685,
the only test of M46, may be red at baseline — `Inbox.load` no longer calls `Inbox._read`, which the
test wraps.)

**For each mutant:** apply the ONE edit to the copy's source, then run
`env -u NO_COLOR C:/Users/jjgh8/anaconda3/python.exe -m pytest -q -x -p no:cacheprovider <files> [-k "<filter>"]`
with `<files>` and the `-k` filter exactly as the row's last column gives them. Record KILLED (≥ 1 failure
or error; give the first failing test id) or SURVIVED. If a run with a `-k` filter passes, re-run the
same file(s) WITHOUT `-k` (still `-x`) before recording SURVIVED, and say "full-file rerun" in Notes.
Then restore the file with `git -C C:/Users/jjgh8/Github/taskboard-wt/incK-mut checkout -- <file>` and
confirm `git -C C:/Users/jjgh8/Github/taskboard-wt/incK-mut status --short` is empty before the next mutant.

**How to apply an edit.** A single-line row quotes the exact text to replace (without its leading
indentation); it occurs exactly once in the file — replace that text only and keep the line's
indentation. "delete the whole line" removes that line and its newline. "multi-line: see block Mxx"
replaces the exact lines of that block (indentation as shown) with the block's new lines. Each edit was
checked to occur exactly once in its file and to leave the file compiling. If an edit cannot be
applied as written (the code differs), apply the closest equivalent and say what you did in Notes.

Spread: HLR-4401 view/keys 6 · HLR-4402 divider 5 · HLR-4403 suggest 8 · HLR-4404 dump 9 · HLR-4405 undo 6 ·
HLR-4406 review 5 · HLR-4407 store 12 · HLR-4408 images 6 · HLR-4409 colour/controls 3 = 60. Security and
data-loss arms covered: SEC-1 (M40, M41), SEC-2 (M25, M44, M45), SEC-3 (M29, M33), SEC-4 (M46), SEC-5 (M47),
SEC-6 (M52), SEC-7 (M53), SEC-8 (M34), the cap LLR-4407.35/.37 incl. the on-disk count (M48, M49),
ARCH-1 (M42, M43), ARCH-2 (M28, M39), ARCH-3 (M02), ARCH-4 (M32, M50, M51).

| M | File:function (line ~N) | Edit | Req (LLR id) | Test file(s) to run |
|---|---|---|---|---|
| M01 | keymap.py:KEYMAP (line ~149) | delete the whole line `    Key("n", "n", "capture", "Capture", group="misc", bar=False),` | LLR-4401.1 | `tests/test_capture_view.py -k "TC_4401 or TC_4402"` |
| M02 | app.py:TaskboardApp.check_action (line ~2316) | `if action == "capture" and any(isinstance(sc, BoardsHome) for sc in self.screen_stack):` → `if False:` (keep the line's indentation) | LLR-4401.19 (ARCH-3) | `tests/test_capture_view.py -k "TC_4419"` |
| M03 | app.py:TaskboardApp.check_action (line ~2322) | `"capture"):` → `"capture_off"):` (keep the line's indentation) | LLR-4401.14 | `tests/test_capture_view.py -k "TC_4414 or TC_4411"` |
| M04 | app.py:TaskboardApp.check_action (line ~2329) | `AddedList, CaptureView))` → `AddedList))` (keep the line's indentation) | LLR-4401.12 | `tests/test_capture_view.py -k "TC_4412"` |
| M05 | app.py:CaptureView.BINDINGS (line ~1538) | `Binding("alt+o", "other", "", priority=True),` → `Binding("alt+o", "other", ""),` (keep the line's indentation) | LLR-4401.18 | `tests/test_capture_view.py -k "TC_4418"` |
| M06 | app.py:CaptureView.on_mount (line ~1588) | `pad.move_cursor(pad.document.end)` → `pad.move_cursor((0, 0))` (keep the line's indentation) | LLR-4401.5 | `tests/test_capture_view.py -k "TC_4405"` |
| M07 | inbox.py:DIVIDER_RE (module) (line ~55) | `DIVIDER_RE = re.compile("_{4,}")` → `DIVIDER_RE = re.compile("_{3,}")` (keep the line's indentation) | LLR-4402.1 | `tests/test_inbox_store.py -k "TC_4431"` |
| M08 | inbox.py:note_count (line ~198) | `if len(parts) > 1 and last.end >= last.start and not last.is_note:` → `if False:` (keep the line's indentation) | LLR-4402.8 | `tests/test_inbox_store.py -k "TC_4438"` |
| M09 | app.py:PadArea.get_line (line ~1522) | `if line_index != self.selection.end[0] and is_divider(line.plain):` → `if is_divider(line.plain):` (keep the line's indentation) | LLR-4402.7 | `tests/test_capture_view.py -k "TC_4437"` |
| M10 | app.py:CaptureView.action_divider (line ~1829) | `if line.strip() == "":` → `if False:` (keep the line's indentation) | LLR-4402.10 | `tests/test_capture_view.py -k "TC_4440"` |
| M11 | app.py:CaptureView._notice_divider (line ~1702) | `if self.app.inbox.divider_notice or self.app._divider_said:` → `if self.app._divider_said:` (keep the line's indentation) | LLR-4402.15 | `tests/test_capture_view.py -k "TC_4445"` |
| M12 | suggest.py:stem (line ~75) | `return w[:6]` → `return w[:5]` (keep the line's indentation) | LLR-4403.2 | `tests/test_suggest.py -k "TC_4462"` |
| M13 | suggest.py:words (line ~88) | `if w.startswith("@") or (len(w) >= 3 and w not in STOP and not w.isdigit()):` → `if w.startswith("@") or (len(w) >= 3 and w not in STOP):` (keep the line's indentation) | LLR-4403.1 | `tests/test_suggest.py -k "TC_4461"` |
| M14 | suggest.py:W_NAME.. (module) (line ~35) | `W_NAME, W_TITLE, W_PEOPLE, W_MARK, W_NOTES = 3, 2, 2, 1, 1` → `W_NAME, W_TITLE, W_PEOPLE, W_MARK, W_NOTES = 2, 2, 2, 1, 1` (keep the line's indentation) | LLR-4403.4 | `tests/test_suggest.py -k "TC_4464"` |
| M15 | suggest.py:_idf (line ~184) | `return {s: math.log((n + 1) / (c + 1)) + 1.0 for s, c in df.items()}` → `return {s: math.log(n / c) for s, c in df.items()}` (keep the line's indentation) | LLR-4403.6 | `tests/test_suggest.py -k "TC_4466"` |
| M16 | suggest.py:suggest (line ~217) | `score *= 0.5` → `score *= 1.0` (keep the line's indentation) | LLR-4403.8 | `tests/test_suggest.py -k "TC_4468"` |
| M17 | suggest.py:options (line ~254) | `if hits and hits[0].score >= MID:` → `if hits and hits[0].score >= HIGH:` (keep the line's indentation) | LLR-4403.11 | `tests/test_suggest.py -k "TC_4471 or TC_4472"` |
| M18 | suggest.py:suggest (sort key) (line ~225) | `h.doc.project_name.casefold(),` → `h.doc.project_name,` (keep the line's indentation) | LLR-4403.9 | `tests/test_suggest.py -k "TC_4469"` |
| M19 | app.py:CaptureView.options_for (line ~1641) | `hits = suggest(nt.title + "\n" + nt.notes, self.docs)` → `hits = suggest(text, self.docs)` (keep the line's indentation) | LLR-4403.28 | `tests/test_capture_view.py -k "TC_4488b"` |
| M20 | inbox.py:_dump_other (line ~921) | `with file_lock(path, name):` → `with open(os.devnull):` (keep the line's indentation) | LLR-4404.9 / .13 | `tests/test_capture_view.py -k "TC_4509 or TC_4513"` |
| M21 | inbox.py:_dump_other (line ~966) | multi-line: see block M21 below | LLR-4404.9 | `tests/test_capture_view.py -k "TC_4509"` |
| M22 | inbox.py:_dump_other (line ~959) | `images=paths, created=models.stamp(now), id=tid)` → `images=paths, id=tid)` (keep the line's indentation) | LLR-4404.4 | `tests/test_capture_view.py -k "TC_4504"` |
| M23 | inbox.py:_dump_other (line ~958) | `task = Task(title, project_id=pid, phase=fresh.phases[0], notes=notes,` → `task = Task(title, project_id=pid, notes=notes,` (keep the line's indentation) | LLR-4404.5 | `tests/test_capture_view.py -k "TC_4505"` |
| M24 | inbox.py:_dump_other (line ~971) | delete the whole line `            history.append(path, {"task": tid, "from": None, "to": task.phase}, at=now)` | LLR-4404.32 | `tests/test_capture_view.py -k "TC_4532"` |
| M25 | inbox.py:dump_note (line ~842) | delete the whole line `        note.encode("utf-8")` | LLR-4404.34 (SEC-2) | `tests/test_capture_view.py -k "TC_4534"` |
| M26 | inbox.py:_dump_open (line ~904) | `live.projects.remove(project_obj)` → `pass` (keep the line's indentation) | LLR-4404.15 | `tests/test_capture_view.py -k "TC_4515"` |
| M27 | app.py:CaptureView._dump (line ~1871) | `live=(app.board if Path(path).resolve() == Path(app.board.path).resolve()` → `live=(app.board if False` (keep the line's indentation) | LLR-4404.8 | `tests/test_capture_view.py -k "TC_4508"` |
| M28 | app.py:CaptureView._key (line ~1632) | `return (str(opt.doc.board_path), opt.doc.project_id)` → `return str(opt.doc.board_path)` (keep the line's indentation) | LLR-4404.17 (ARCH-2) | `tests/test_capture_view.py -k "TC_4516 or TC_4517"` |
| M29 | inbox.py:_unchanged (line ~993) | `return asdict(task) == asdict(expected)` → `return (task.title, task.notes) == (expected.title, expected.notes)` (keep the line's indentation) | LLR-4405.10 (SEC-3) | `tests/test_inbox_store.py -k "TC_4550"` |
| M30 | inbox.py:Inbox.last_dump (line ~698) | `return result[-1] if result else None` → `return result[0] if result else None` (keep the line's indentation) | LLR-4405.1 | `tests/test_inbox_store.py -k "TC_4541b"` |
| M31 | inbox.py:Inbox.last_dump (line ~690) | `entries = state["dumped"] if state is not None else self.dumped` → `entries = self.dumped` (keep the line's indentation) | LLR-4405.17 | `tests/test_inbox_store.py -k "TC_4557"` |
| M32 | inbox.py:Inbox.last_dump (line ~695) | `result.append(dict(e))` → `pass` (keep the line's indentation) | LLR-4405.18 (ARCH-4) | `tests/test_inbox_store.py -k "TC_4558"` |
| M33 | inbox.py:_needed (line ~998) | `return any(task_id in t.depends_on for t in board.tasks if t.id != task_id)` → `return False` (keep the line's indentation) | LLR-4405.19 (SEC-3) | `tests/test_inbox_store.py -k "TC_4559"` |
| M34 | app.py:CaptureView.action_undo (line ~2048) | `== norm), None)` → `== norm), (entry["board"], "", None, ""))` (keep the line's indentation) | LLR-4405.16 (SEC-8) | `tests/test_capture_view.py -k "TC_4556"` |
| M35 | app.py:ReviewList.on_mount (line ~2137) | `self.on = [self.view.chosen(t) is not None for t in self.texts]` → `self.on = [True for t in self.texts]` (keep the line's indentation) | LLR-4406.3 | `tests/test_capture_view.py -k "TC_4563"` |
| M36 | app.py:ReviewList.action_move (line ~2148) | `self.sel = max(0, min(len(self.texts) - 1, self.sel + delta))` → `self.sel = max(0, self.sel + delta)` (keep the line's indentation) | LLR-4406.4 | `tests/test_capture_view.py -k "TC_4564"` |
| M37 | app.py:ReviewList.action_toggle (line ~2157) | `self.on[self.sel] = not self.on[self.sel]` → `self.on[self.sel] = True` (keep the line's indentation) | LLR-4406.5 | `tests/test_capture_view.py -k "TC_4565"` |
| M38 | app.py:ReviewList.action_toggle (line ~2153) | multi-line: see block M38 below | LLR-4406.6 | `tests/test_capture_view.py -k "TC_4566"` |
| M39 | app.py:ReviewList.action_dump (line ~2184) | `if self.view.dump_part(part, quiet=True, target=targets[t], rebuild=False):` → `if self.view.dump_part(part, quiet=True):` (keep the line's indentation) | LLR-4406.17 (ARCH-2) | `tests/test_capture_view.py -k "TC_4577"` |
| M40 | inbox.py:union_pads (line ~318) | delete the whole line `    budget.update(unseen)` | LLR-4407.19 (SEC-1) | `tests/test_inbox_store.py -k "TC_4599"` |
| M41 | inbox.py:union_pads (line ~324) | `budget[p.text] -= 1` → `pass` (keep the line's indentation) | LLR-4407.19 (SEC-1) | `tests/test_inbox_store.py -k "TC_4599"` |
| M42 | inbox.py:Inbox.write_pad (inner change) (line ~631) | multi-line: see block M42 below | LLR-4407.48 (ARCH-1) | `tests/test_inbox_store.py -k "TC_4688"` |
| M43 | inbox.py:Inbox._commit (line ~589) | `base = dict(fresh) if fresh is not None else {` → `base = dict(fresh) if False else {` (keep the line's indentation) | LLR-4407.4 (ARCH-1) | `tests/test_inbox_store.py -k "TC_4584"` |
| M44 | inbox.py:Inbox._parse (line ~463) | delete the whole line `            json.dumps(raw, ensure_ascii=False).encode("utf-8")` | LLR-4407.43 (SEC-2) | `tests/test_inbox_store.py -k "TC_4683"` |
| M45 | inbox.py:Inbox._commit (line ~598) | `except UnicodeError as exc:` → `except LookupError as exc:` (keep the line's indentation) | LLR-4407.44 (SEC-2) | `tests/test_inbox_store.py -k "TC_4684"` |
| M46 | inbox.py:Inbox.refresh (line ~529) | multi-line: see block M46 below | LLR-4407.45 (SEC-4) | `tests/test_inbox_store.py -k "TC_4685"` |
| M47 | app.py:TaskboardApp.action_quit (line ~2495) | `if view._flush():` → `if view._flush() or True:` (keep the line's indentation) | LLR-4407.46 (SEC-5) | `tests/test_inbox_store.py -k "TC_4686"` |
| M48 | inbox.py:Inbox.load (line ~498) | `head = fh.read(STORE_MAX_BYTES + 1)` → `head = fh.read()` (keep the line's indentation) | LLR-4407.35 | `tests/test_inbox_store.py -k "TC_4675"` |
| M49 | inbox.py:Inbox._commit (line ~603) | `size = len(data) + text.count("\n") * (len(os.linesep) - 1)` → `size = len(data)` (keep the line's indentation) | LLR-4407.37 | `tests/test_inbox_store.py -k "TC_4677"` |
| M50 | inbox.py:Inbox.write_pad (except) (line ~653) | `self.pending.append(("record", record))` → `pass` (keep the line's indentation) | LLR-4407.39 (ARCH-4) | `tests/test_inbox_store.py -k "TC_4679 or TC_4681 or TC_4558"` |
| M51 | inbox.py:Inbox.write_pad (line ~620) | `ops = list(self.pending)` → `ops = []` (keep the line's indentation) | LLR-4407.41 (ARCH-4) | `tests/test_inbox_store.py -k "TC_4681 or TC_4598b"` |
| M52 | inbox.py:_links_ok (line ~751) | `if os.path.islink(folder) or folder.is_junction():` → `if False:` (keep the line's indentation) | LLR-4408.20 (SEC-6) | `tests/test_inbox_store.py -k "TC_4650"` |
| M53 | inbox.py:_image_ok (line ~140) | `if name.split(".")[0].rstrip(" ").lower() in RESERVED_STEMS:` → `if name.split(".")[0].lower() in RESERVED_STEMS:` (keep the line's indentation) | LLR-4408.18 (SEC-7) | `tests/test_inbox_store.py -k "TC_4628"` |
| M54 | inbox.py:_copy_images (line ~802) | `shutil.copy2(src, dest_dir / name)` → `shutil.move(src, dest_dir / name)` (keep the line's indentation) | LLR-4408.11 | `tests/test_inbox_store.py -k "TC_4621"` |
| M55 | inbox.py:_copy_images (line ~800) | `dest_dir.mkdir()          # exclusive: a taken folder is refused (ARCH-7)` → `dest_dir.mkdir(exist_ok=True)` (keep the line's indentation) | LLR-4408.13 | `tests/test_inbox_store.py -k "TC_4623"` |
| M56 | inbox.py:attach_images (line ~1160) | `shutil.copy2(p, folder / name)` → `shutil.move(p, folder / name)` (keep the line's indentation) | LLR-4408.3 | `tests/test_inbox_store.py -k "TC_4613"` |
| M57 | inbox.py:_images_back (line ~1111) | `free = _free_name(folder, name)` → `free = name` (keep the line's indentation) | LLR-4408.16 | `tests/test_inbox_store.py -k "TC_4626"` |
| M58 | inbox.py:_task_fields (line ~272) | `return title, strip_controls(notes)` → `return title, notes` (keep the line's indentation) | LLR-4409.3 | `tests/test_inbox_store.py -k "TC_4633"` |
| M59 | app.py:rail_rows.emit (line ~1403) | `r.append(note.title, f"b {HEX['ink']}" if is_cur else HEX["hd"])` → `r.append_text(Text.from_markup(note.title))` (keep the line's indentation) | LLR-4409.4 | `tests/test_capture_view.py -k "TC_4634"` |
| M60 | inbox.py:Inbox.write_pad (line ~617) | delete the whole line `        pad = strip_controls(pad)` | LLR-4409.5 | `tests/test_inbox_store.py -k "TC_4635"` |

## Multi-line edits

### Block M21 — taskboard/inbox.py (line ~966)

Replace exactly these lines:

```python
                fresh.save_atomic()
            except OSError as exc:
                shutil.rmtree(fresh.image_dir(tid), ignore_errors=True)
```

with:

```python
                fresh.save()
            except OSError as exc:
                shutil.rmtree(fresh.image_dir(tid), ignore_errors=True)
```

### Block M38 — taskboard/app.py (line ~2153)

Replace exactly these lines:

```python
        if self.view.chosen(t) is None:
            self.notify("Needs a name: alt+n in the pad.", title="Capture",
```

with:

```python
        if False:
            self.notify("Needs a name: alt+n in the pad.", title="Capture",
```

### Block M42 — taskboard/inbox.py (line ~631)

Replace exactly these lines:

```python
                    if _has_entry(d, e):
                        continue
                    p = _remove_first_note(p, e["text"])
```

with:

```python
                    if _has_entry(d, e):
                        continue
```

### Block M46 — taskboard/inbox.py (line ~529)

Replace exactly these lines:

```python
        try:
            state = self._read(self.path)
        except OSError:
            return False
        self._stamp = stamp
```

with:

```python
        self._stamp = stamp
        try:
            state = self._read(self.path)
        except OSError:
            return False
```

## Output

Write the table to `C:/Users/jjgh8/Github/taskboard-wt/capture-proto/.dev-flow/2026-11-01-v3-incK/05-mutants.md`
as `| M | Where | Edit applied | Req | Result | First failing test / Notes |` (Where and Req as in the rows
above), with the BASELINE-RED list above the table, then a totals line `killed K / N` (N = mutants judged;
list any NOT JUDGED ids beside it), and save the full transcript of the baseline and of all runs to
`C:/Users/jjgh8/Github/taskboard-wt/capture-proto/.dev-flow/2026-11-01-v3-incK/evidence/mutants-run.txt`.
At the end the copy must be clean (`git status --short` empty). Return ≤ 6 lines: totals, every SURVIVED id,
every NOT JUDGED id.

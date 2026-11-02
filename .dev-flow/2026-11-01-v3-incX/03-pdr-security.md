# Inc X — E3 PDR, security review (code-free)

Reviewer: `security-reviewer` (Opus). Worktree `taskboard-wt/x-html` at `82d8d4c`. Read-only: no product
file, requirement or graph was changed.

## Scope reviewed

- `.dev-flow/COMMISSION-present-x-html.md`; in `.dev-flow/2026-11-01-v3-incX/`: `01-requirements.md`,
  `00-e1-rulings.md` (rulings 1–11), `graph-interfaces.cw.md`, `graph-proto-A.cw.md`, `graph-proto-B.cw.md`,
  `graph-baseline.cw.md` (by reference), `e2-seams.md`, `baseline-notes.md`.
- The source behind the seams, at 509d444-equivalent lines in this tree: `report_html.py` (`extract` 98–174,
  `slug` 177–179, `write_reports` 202–222), `report_deck.py` (escaping 1–58, `_notes` 338–352, `render`
  505–516), `report.py:_e` 78–82, `views.py` (`lane_facts` 941–970, `_hidden_class_ids`/`_hide` 3144–3160,
  `present_tasks`/`present_tasks_m` 6642–6660, `_present_pool` 6686, `present_paths` … `save_present_png`
  7340–7400), `models.py` (`project_by_id`/`task_by_id`/`is_done` 1185–1217, clipboard subprocess 606–627),
  `app.py` (`action_export` 623–649, `action_report_export`/`_on_report_chosen`/`_open_report` 2993–3052,
  `action_open_url` 4667–4680), `__main__.py:open_app` 23–34.

## Focus answers (short)

| # | Question | Answer |
|---|---|---|
| 1 | Hidden data out of the bytes | Holds by design. Filtering `proxy.projects` and `proxy.tasks` is enough: every reader in `extract` reads only those two lists (S-0). One residual: the deck carries task links the screen never draws (S-1, MEDIUM). |
| 2 | File name from a project name | Safe. `report_html.slug` keeps only `str.isalnum()` characters and `-`. No separator, dot, colon, control or NUL character can pass. The fixed `present-` prefix keeps the name off the reserved device names. The name is 64 characters or fewer (S-4). |
| 3 | Writing to `reports/`, overwrite, symlinks | The same posture as `H`: a same-day file is overwritten (ruling 9), and `write_text` follows a planted symlink or junction. This is acceptable for a single-user local tool (S-4, S-5). |
| 4 | `o` opens only the file just written | Holds. The offer holds only the path `write()` returned, its `.html` suffix is fixed, the offer is single-use and lives 10 s, and it dies with the screen. Residuals: a pre-existing `as_uri()` `ValueError` off Windows, and a stale toast after `esc` (S-6). |
| 5 | Escaping reuses the deck's | Holds. `render(d)` is byte-unchanged (ruling 8); `x` adds no HTML sink; the toast is `markup=False` (S-7). |
| 6 | Edge subprocess removal | It removes a real surface: a binary found on PATH plus a headless browser. No product caller remains once app.py drops its 4 imports (S-8). |

## Findings

### S-0 — Confirmation: the two-list proxy is a complete hide filter  [Severity: INFO]
- **What:** proto-B finding P-B-1 asks whether filtering only `proxy.projects` and `proxy.tasks` keeps every hidden project, task and milestone class out of the bytes.
- **Where:** `report_html.extract` 98–174, over `present_deck_boards`' proxy.
- **Why it matters:** if any reader in `extract` walks the board by another route, hidden data reaches the file. Ruling 2 and HLR-4502 forbid that.
- **Evidence (code read):**
  - `project_by_id` and `task_by_id` iterate the live `self.projects` and `self.tasks` (models.py:1185–1193), so they see the proxy's lists. There is no index or cache that the shallow copy could share.
  - `lane_facts` reads only its `rows` argument (views.py:941–970).
  - `deps` are filtered by `in_scope` (report_html.py:148), so a hidden blocker's key never appears. `_chains` walks only `out_tasks`.
  - `people` is emitted only for mentioned handles (report_html.py:170). `marks` is emitted only for used classes (report_html.py:172–173). Together these satisfy LLR-4502.5.
  - The cover counts come from `d["projects"]` and `d["tasks"]` (report_deck.py:296–308), so hidden tasks do not appear in the counts.
  - `inbox` is empty by construction, because every proxy task belongs to a proxy project. That satisfies LLR-4502.3.
  - Hidden classes use `present_tasks_m`, the same function the frames use, through `board.marks` (shared by `copy.copy`). The deck therefore hides exactly what the screen hides.
- **Residual (accepted, no action):** a shown task blocked by a hidden one still carries `blocked: true`. That reveals that some blocker exists, not which one. The presentation draws the same flag.
- **Recommendation:** none to the design. In E4, keep TC-4721..4725 as byte searches over the written file, not over `d`.
- **Evidence state:** `executed` (code read); design `approved`.

### S-1 — The deck carries task links (and per-task meta) the presentation never draws  [Severity: MEDIUM]
- **What:** The base `x` wrote the terminal frame, so the file held only what the screen showed. The `x` deck is `H`'s deck (ruling 8). On each project slide it prints every shown task's `urls` as clickable links (`report_deck._notes`, 338–352). It also prints the priority and `<n>d in phase` meta (`_meta`, 135–148). The presentation's renderers draw notes but no URL: views.py 6590–7700 has no `.urls` read.
- **Where:** `report_deck._notes` / `_meta`, reached by `PresentScreen.action_export` → `render(d)`.
- **Why it matters:** the presentation export is the file most likely to be sent to a client. A task link can hold a capability, such as a signed share link, a meeting passcode or a private doc URL. The user's story says "exactly what I am presenting". Ruling 2 says "The deck draws exactly what the presentation draws". No hide flag is broken, so this is not a HLR-4502 failure. It does widen what leaves the screen.
- **Recommendation:** the orchestrator rules one of two options, and the choice goes in `03-pdr-rulings.md`:
  - **(a) Preferred: accept and say it.** The `x` deck is `H`'s deck and includes task links. Add one README sentence where the `x` export is described (LLR-4506.5's lines). No code change, and LLR-4501.3/.4 byte identity stands.
  - **(b) Drop the links from the `x` deck.** This needs a render option, which is a new feature and breaks ruling 8's byte identity. Not recommended under "remove, don't guard".
- **Blocks:** no (MEDIUM). It is owed a ruling before E4.
- **Evidence state:** `planned` (awaiting ruling).

### S-2 — The proxy shares the board's `path` (P-B-1): no guard, under two conditions  [Severity: LOW]
- **What:** `copy.copy(board)` keeps `path`, `settings`, `phases` and `marks`. A `save()` on the proxy would overwrite `board.json` with the filtered lists, destroying the hidden tasks.
- **Where:** `present_deck_boards` (graph-interfaces.cw.md node 1; proto-B).
- **Why it matters:** the failure is irreversible data loss, but the design reaches no writer. `extract` is read-only (TC-3101), and the proxy lives only in `action_export`'s locals.
- **Recommendation:** agree with P-B-1: no guard. Add as an **E4 addendum**:
  - the proxy (or the `boards` list) is never stored on `PresentScreen` or the app; no caching. This also keeps S-8 of the seams (the flags are read at each press) true;
  - TC-4710 (sha256 of `board.json` and `history.jsonl` before and after `x`, 6/6) is the control, and its NC (`board.save()` in the export) must be run in the mutant table.
- **Evidence state:** `planned` (E4 addendum).

### S-3 — `present_name`'s home differs between ruling 11 and the frozen interfaces  [Severity: LOW]
- **What:** ruling 11 puts `present_name` in `views.py`, beside `present_deck_boards`, with `report_deck.py` unchanged. Five texts still place it in `report_deck.py`:
  - graph-interfaces.cw.md, header (lines 7–8) and node `present_name` (`module: taskboard/report_deck.py`);
  - e2-seams.md S-3 (`report_deck.present_name`);
  - graph-proto-B.cw.md, header and node `present_name`;
  - graph-proto-A.cw.md, `action_export` step (5): `report_deck.present_name(d)`.
- **Where:** the files above.
- **Why it matters (security angle):** the file-name safety in S-4 rests on calling `report_html.slug` and no second slug rule. `views.present_paths` holds a private copy of that rule, and it is being removed. If E4 meets two homes for the function, an implementer may copy the slug loop again.
- **Recommendation:** align the five texts to ruling 11 with targeted edits. The node must say "calls `report_html.slug`; no local slug rule". This is mainly an architect item. The security condition is the single slug rule.
- **Evidence state:** `planned`.

### S-4 — File name from the project name: safe; same-day overwrite accepted  [Severity: LOW]
- **What:**
  - `slug` maps every character that is not `isalnum()` to `-`, strips the `-` at both ends and keeps at most 40 characters (report_html.py:177–179).
  - Path separators (`/ \`), `.`, `:`, the Windows-forbidden characters `<>"|?*`, control characters (U+0000–U+001F, U+007F) and the bidi controls are all non-alphanumeric, so traversal cannot reach the name. For example, `..\..\evil` becomes `evil`.
  - The `present-` prefix keeps the stem off the reserved device names (`CON`, `NUL`, `COM1` …). Windows matches those on the stem before the first dot.
  - The longest name is 8 + 40 + 1 + 10 + 5 = 64 characters, far under 255. It never ends in a dot or a space.
  - An empty slug becomes `project` (TC-4701c).
- **Residual:** two projects whose names slug alike (`Q1 Plan` / `Q1-Plan`, or a project named `All` against view 3, finding P-B-2) overwrite each other the same day. The toast says "written", not "overwritten". The file is regenerable, so this is accepted by ruling 9.
- **Recommendation:** an **E4 addendum** test: a project named `..\..\evil` and a project named `CON`. The written path's `parent` must equal `F` (resolved), and the names must be `present-evil-<date>.html` and `present-con-<date>.html`. This pins the traversal property, which today has only a name example.
- **Evidence state:** `executed` (code read); test `planned`.

### S-5 — `reports/` symlink or junction is followed  [Severity: LOW]
- **What:** `folder.mkdir(exist_ok=True)` accepts a `reports` that is a junction or symlink, and `path.write_text` follows a planted `present-*.html` link. The deck's bytes therefore land wherever the link points. This is the same as `H`'s `write_reports` today.
- **Where:** `PresentScreen.action_export` step (6) (proto-A).
- **Why it matters:** exploiting this needs write access to the board's folder. Anyone with that access can already edit `board.json`. Synced drives do not sync links as links. No privilege boundary is crossed.
- **Recommendation:** no guard: keep parity with `H`. Record the acceptance in the rulings.
- **Evidence state:** `n/a — accepted residual, matches the shipped H writer`.

### S-6 — `o` opens only the file just written; two pre-existing residuals  [Severity: LOW]
- **What:**
  - `_export_offer` holds only the `Path` that `write()` returned: `folder / present_name(d)`, suffix `.html`. It is single-use, live 10 s on a monotonic clock, withdrawn on a failed write (LLR-4503.5), and dies with the screen. It is separate from `H`'s `_report_offer`.
  - `os.startfile` receives that fixed `.html` path, so the shell resolves it to the `.html` handler and never to an executable association. No other path can reach the opener.
- **Residuals:**
  1. **Relative path off Windows.** `_open_report` catches only `OSError` (app.py:3041–3047). With `--open` given a relative path, `Path(board.path).parent` is relative, and off Windows `path.as_uri()` raises `ValueError`, which escapes into the screen. This is pre-existing for `H`; `x` now reaches it too. The graph says `action_open_export` "never raises".
  2. **Stale toast after `esc`.** Toasts are app-level, so after `x` and then `esc`, the toast still reads "o opens it (10 s)" for up to 10 s. On the main screen, `o` is `action_open_url`: it uses `H`'s offer if one is live, else it opens every link of the selected task in the browser. A browser opening an unintended outbound link is a minor surprise, not a breach: it is the user's own link and a deliberate keypress.
- **Recommendation:**
  - (1) **E4 addendum, one token in app.py (in budget):** catch `(OSError, ValueError)` in `_open_report`, or pass `path.resolve()` to it. Either one also fixes `H`.
  - (2) No code change. One line in the packet's Risks; the architect may weigh it as a UX item.
- **Evidence state:** `planned`.

### S-7 — Escaping: the deck's existing escaping is reused unchanged  [Severity: INFO]
- **What:**
  - `render(d)` is byte-unchanged (ruling 8; graph-interfaces node `render`).
  - Every board string reaches the HTML through `esc` = `html.escape(quote=True)` (report.py:78–82). Notes come from `notes_html`, built from escaped pieces in constant tags. Links are re-checked to `https?://` and escaped in `href`, with `rel="noopener noreferrer"`.
  - The deck embeds no JSON (`render` does not call `embed_json`). `x` adds no new HTML sink.
  - The toast is `markup=False`, and LLR-4503.7 tests a `[red]rx[/red]` folder.
- **Recommendation:** none. In E4, the implementer must not render with anything but `report_deck.render`, which proto-A already states.
- **Evidence state:** `executed` (code read).

### S-8 — Removing the Edge rasteriser removes a real attack surface; nothing else calls it  [Severity: INFO]
- **What the removal takes away** (`_find_msedge` / `save_present_png`, views.py:7367–7400):
  - The executable comes from the environment variables `ProgramFiles(x86)` and `ProgramFiles`, then from `shutil.which("msedge" | "microsoft-edge")`. On Windows, `shutil.which` also searches the current directory, which is a binary-planting vector.
  - That binary runs headless on a `file://` URI, with arguments built from the path.
  - It runs on every `x`, including during the test suite: `test_AT_1001` launched the real Edge (baseline-notes).
- **Remaining callers:**
  - After app.py drops `present_all_export`, `present_paths`, `save_present_png` and `save_present_svg` (app.py:55–61, 634–642), no product caller remains.
  - views.py's `os`, `shutil` and `subprocess` imports become unused (baseline-notes, seam S-7).
  - The only other `subprocess` in the package is `models.grab_clipboard_text`: off Windows only, a fixed argv and no shell, not on the `x` path. It does not disturb LLR-4504.2's patched-`subprocess` test.
  - The three prototype scripts that still call the functions are frozen evidence (ruling 5). They fail at import or attribute lookup and execute nothing.
- **Recommendation:** none beyond LLR-4504.2/.3 as written. In E4, run LLR-4504.3's grep over `taskboard/*.py` after integration, as TC-4743 states.
- **Evidence state:** `executed` (code read); TC-4742/4743 `planned`.

## Verdict

- [ ] OK to ship
- [ ] BLOCK-UNTIL
- [ ] Block
- **E3 security round: PASS-WITH-NOTES.**
  - **Counts:** HIGH 0, MEDIUM 1, LOW 5, INFO 3.
  - **S-1 (MEDIUM):** needs an orchestrator ruling (preferred: accept and document) before E4. It does not block.
  - **To E4 as addenda:** S-2, S-4 and S-6(1).
  - **To targeted design edits:** S-3.
  - **Recorded as accepted residuals:** S-5 and S-6(2).
- This review clears a design risk. It authorises no merge, push or deploy.

## Evidence checklist

- [x] Each finding has what · where · why · recommendation: S-0..S-8 above.
- [x] Each finding has a severity rating: S-0..S-8 headers.
- [x] No secret values appear in this output. None were read; the board fixtures are synthetic.
- [x] The verdict is explicit (PASS-WITH-NOTES), and no HIGH is open: none was found.
- [x] New tool or integration: none added. One external process is removed (S-8). The OS handler for `o` already existed in `H`'s flow, and its scope is limited to the one written path (S-6).

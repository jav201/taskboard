# Review — taskboard — Batch 2026-10-02-batch-04

> Phase 2 artifact. Reviewers (in parallel, spawned as named sub-agents following the installed
> bundle's `agents/<role>.md`): `architect` ∥ `qa-reviewer` ∥ `security-reviewer` (trigger family C,
> and commissioned) ∥ `ux-reviewer` (trigger family D). Iteration 1, 2026-10-02.

## ✅ Verdict (read first)

- **Gate:** `iterate-to-refine` → Phase 1 (blockers present) — **and STOPPED for the operator: security HIGH S-1 is open** (standing authorization: "a HIGH finding blocks regardless — stop and report").
- **Out-of-scope findings:** 2 named and routed below (UX-8, S-9)

- **Findings:** 3 blocker (Q-1 ≡ A-1 ≡ S-2, the same census defect; S-1 HIGH) · 12 major · 20 minor/LOW/info
- **shall/should check:** ✓ clean (architect: grep 0 hits)
- **Two-layer (blockers):** ✗ AT-402's sync-failure arm has no black-box trigger (Q-3); AT-405 is a consumer-contract guard, not the C-12 chain (Q-6)
- **Census (change-first):** done — best-effort + gate-confirmed (architect §Supersession census)
- **Security:** ✗ 1 HIGH (S-1), 3 MEDIUM (S-2, S-3, S-4), 5 LOW (S-5..S-9) — verdict FAIL, `BLOCK-UNTIL: S-1, S-2`
- **Evidence checklists (architect / qa / security / ux):** ✓ all complete (below)

---

## Detail (reference)

### Findings
| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| S-1 | security | **HIGH** (blocker) | US-401 / new | A teammate's `team.json` sets a project `status` that `apply_config_to_board` copies with no validation (`team_sync.py:251-253`, bypassing `PROJECT_STATUSES`, `models.py:750`); `ProjectPicker._project_line` puts `p.status` into markup unescaped (`modals.py:649`). Probe on base: status `[@click=app.pwn]X` — a click **ran the action**. | validate synced project fields as `Project.from_dict` does (status, colour, name str, dates); escape or `Text`-wrap `status`; an AT arm: a synced status payload clicked fires no action | open — operator |
| Q-1 / A-1 / S-2 | qa (blocker), architect (major), security (MEDIUM, blocker) | blocker | LLR-401.1, TC-401, TC-403 | The census marks any `_rich(...)` call safe whatever its argument holds; the planted module even certifies `_rich(f"[b]{task.title}[/b]")`. `[LINK=…]` paints literally under Rich without escape, so the main payload cannot catch a missing `escape`. | a `_rich`/`from_markup` argument is safe only when every non-literal part is `escape(...)` (or a name bound to one); plant the unescaped form as unsafe; run every AT site with the three catalog payloads | open |
| S-3 | security | MEDIUM (major) | US-401/402 | unvalidated synced `color` → `KeyError` in gantt render (`views.py:71`); non-str `name` → `AttributeError` | same fix as S-1; an AT loading a hostile `team.json` and rendering every view | open |
| S-4 | security | MEDIUM (major) | LLR-401.1 fix form | `_rich` + `escape` cannot meet HLR-401's own catalog: a trailing backslash paints doubled, `\\` before a closing tag loses one, `\\\` leaks the app's style; `:smile:` is substituted (emoji on). No link/action. | build user pieces with `Text.assemble((user, style), …)` / `Text.append`; or `from_markup(..., emoji=False)` + a backslash-run-safe escape | open — design question |
| A-2 | architect | major | HLR-402, D-404 | D-404 is false: `_clean_clipboard_text` keeps `\r`; Ctrl+V into an `Input` keeps `\r\n`, so an app-written file is not byte-stable | make `_clean_clipboard_text` use `strip_controls` + its cap, or narrow HLR-402 to "a file holding no control byte" | open |
| Q-2 | qa | major | AT-403 path sites | `[LINK=http://e]x` cannot be a path component; a path-safe payload vanishes rather than raising; `\` before `[B]` escapes it on Windows | per-site payload; for paths a `a[B]x` directory and full-path equality | open |
| Q-3 | qa | major | AT-402 sync-failure toast | no black-box trigger: the sync path never raises | declared fault injection with a reason, or a white-box TC | open |
| Q-4 | qa | major | AT-401..403 | one node per AT: the first `MarkupError` hides the other sites' RED | each site its own `run_test` inside the node, failures collected; a base run listing all 19 RED | open |
| Q-5 | qa | major | HLR-402 / AT-404 | the saved file writes ESC as `\u001b` (raw-byte check vacuous); Rich strips BEL before paint | assert parsed JSON strings; screen check with ESC and C1 | open |
| Q-6 | qa | major | AT-405, B4 | AT-405 writes the teammate file directly — a consumer-contract guard, not C-12 | add the handler → re-read → fresh consumer chain | open |
| UX-1 | ux | major | HLR-403, LLR-403.1, PV-1 | `height: 1` cuts a long value with no marker | `height: auto` (wraps); thresholds "≥ 1 row, never cut"; a long-value AT arm | open |
| A-3 | architect | minor | LLR-402.3 | `app.py:1005-1009` reads `team.json` with bare `json.loads` and republishes it | use `team_sync._read_json` (increment 002 → 3 SOURCE) | open |
| A-4 | architect | minor | LLR-402.1/.2 | cleaning keys can merge two keys; a phase of only control bytes empties the phases list (defaults load); path values with DEL/C1 redirected | boundary arms + a decision | open |
| A-5 | architect | minor | US-402 vs §1.2 | in-session typed/pasted text reaches the screen before the next load | one §1.2 Out line | open |
| A-6 / S-6 / S-7 / Q-8 | architect, security, qa | minor/LOW | TC-402, TC-404 | method sinks matched by name; `notify(title=)`, `tooltip=`, `replace_option_prompt*`, `Select(prompt=)` outside the list; exemptions keyed by function, not by value source | key exemptions on the value's source text; assert the package imports only censused widgets | open |
| Q-7 | qa | minor | US-402 | round-trip only white-box; "written by the app" overclaims | reword; a through-app round trip in AT-404 | open |
| Q-9 | qa | minor | §5 | reachable-site table not declared; project archive/delete confirms and both duplicate-phase sites unnamed | add the 19 reachable / 26 app-constant table | open |
| Q-10 | qa | minor | AT-403 | Setup ids are lowercased before the toast | state the lowercased expected value | open |
| Q-11 | qa | minor | LLR-403.1 | thresholds predicted from a 2-row stand-in | mark predicted until run; non-default priority in AT-406 | open |
| Q-12 | qa | minor | LLR-402.3 | the teammate id from the file name bypasses `_read_json` | narrow the wording | open |
| S-5 | security | LOW | `_rich` templates | two escaped user pieces with only plain text between them can join into a tag (the BACKLOG S-2 class) | the S-4 form removes the class | open |
| S-8 | security | LOW | S2 doors | `history.jsonl` rendered uncleaned; typed text and OS paths not stripped; `app.py:1007` (A-3) | name as non-doors or strip at `history.read` | open |
| UX-2..UX-7 | ux | minor | PV-1, AT-406, D-404 | keep compact (UX-2); a gap under the title (UX-3); label column 20 → 10 (UX-4); 80×24 scroll arm (UX-5); read painted toasts (UX-6); a lone CR joins old-Mac lines (UX-7) | operator's call / AT arms / declare | open |
| A-7 | architect | info | increment 001 | three existing nodes assert the current escaping: `test_archive.py:557-577`, `test_app.py:300-313`, `test_app.py:2052-2059` | supersede in increment 001's reverse census | carried to P3 |
| UX-8 | ux | out of scope | details view | values painted in the label tone `#8b98a5` | BACKLOG | routed |
| S-9 | security | out of scope | bidi / zero-width | visual spoofing only | BACKLOG | routed |

### shall / should check
✓ No modal `should`/`may`/`could` inside any statement (architect, grep 0 hits).

### Two-layer acceptance review (blockers)

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-401 | yes (AT-401..403) | yes | yes | no — the sync-failure arm (Q-3) | blocker (with Q-1) |
| US-402 | yes (AT-404, 405) | yes, but Q-5 makes the file check vacuous | yes | AT-405 is a contract guard (Q-6) | major |
| US-403 | yes (AT-406) | yes | yes | yes | ✓ (UX-1 major) |

### Supersession census (change-first)
Architect, best-effort + gate-confirmed: will go RED and be superseded in increment 001 —
`tests/test_archive.py:557-577`, `tests/test_app.py:300-313`, `tests/test_app.py:2052-2059`;
watch — `test_legend.py:250,266,294`, `test_emoji_picker.py:174`, `test_history.py:98`,
`test_report.py:299`, `test_archive.py:408,429,536`, `test_rescue.py:126`, `test_app.py:1891`;
`test_app.py:1135-1145` (`_clean_clipboard_text`) only if A-2 unifies the rule; no observers for
file moves, imports, git-diff, goldens.

### Security review summary
FAIL — `BLOCK-UNTIL: S-1, S-2`. S-1 HIGH (pre-existing, reachable from a teammate's `team.json`:
an action fired on click, `executed` on base by the reviewer's probe `p_status.py`); S-2 the census
defect (same as Q-1/A-1); S-3, S-4 MEDIUM; S-5..S-9 LOW. The `_rich` seat holds against link and
action injection when every user piece is escaped (31 payloads × 4 templates, 0 link/meta spans).

### Evidence checklists — architect · qa-reviewer · security-reviewer · ux-reviewer
- **architect:** ✓ constraints stated (§2.4, P-1..P-10) · ✓ alternatives where a decision exists (shipped `_rich` seat; grid variants) · ✓ non-applicable marked · ✓ rationale tied (D-404 false, A-2) · ✓ risks listed (incomplete: A-1, A-4, A-6) · ✓ cost n/a · ✓ IFC suffices · ✓ change conditions (A2, §6.3) · ✓ both chains complete, 0 `should`.
- **qa-reviewer:** ✗ Given/When/Then (req-template form instead; not a finding) · ✓ explicit expected · ✓ edge cases (use gaps Q-1, Q-5) · ✓ regression checklist · ✓ exit criteria §5.2 · ✓ no PII · ✓ mode: plan, P2 · ✓ results `planned` · ✗ Layer B through the surface (Q-3, Q-6) · ✗ bidirectional reachability (Q-2, Q-5) · ✓ no unfilled template.
- **security-reviewer:** ✓ each finding what/where/why/fix · ✓ severity on each (1 HIGH, 3 MEDIUM, 5 LOW) · ✓ no secrets in output · ✓ verdict explicit (FAIL, `BLOCK-UNTIL: S-1, S-2`) · ✓ new tool scope n/a.
- **ux-reviewer:** ✓ context of use (thin: environment only in thresholds) · ✓ criteria observable (with UX-1/5/6) · ✓ real mechanism (`enter`, `down`, `pagedown`, `esc` in `run_test`) · ✓ painted result read · ✓ error/empty states (long value missing: UX-1) · automated walkthrough performed · expert inspection performed · evaluation with users not performed — a one-person team.

---

## Iteration-1 fold (2026-10-03, under the operator's rulings asked at the gate)

Rulings, verbatim: (1) scope "Sí, dentro de S" — S-1 and S-3 brought into the batch; (2) fix form
"Piezas de texto, sin formato" — user/synced/OS text as Rich `Text` pieces, never through a parser;
(3) review folds "Sí, todas". Disposition of every finding:

| Finding | Disposition |
|---|---|
| S-1 (HIGH) | folded: US-404, HLR-404, LLR-404.1, AT-407, TC-413 (validation via `Project.from_dict`); the picker status as a piece (LLR-401.3) — discharged only when the increment's fix is applied and verified (P3) |
| Q-1 / A-1 / S-2 | folded: parsers censused, safe only over a literal (TC-406), the planted module flags `_rich(f"[b]{escape(t)}[/b]")` (TC-403) — RED-proven on the planted set |
| S-3 | folded with S-1 (HLR-404: every view renders) |
| S-4 | folded: the Text-piece form (LLR-401.3, P-13); payload set carries `x\\` and `:smile:` |
| S-5 | folded: the class cannot occur — no user text meets a parser in the Textual seat; in `views.py` it stays BACKLOG `collapse_runs` S-2 (D-405) |
| S-6 | folded: `tooltip=` and `replace_option_prompt*` censused; every imported widget censused or declared plain (TC-404); `notify(title=)` is painted plain by Toast (architect, verified) — no sink |
| S-7 / Q-8 / A-6 (exemption half) | folded: exemptions keyed by the value's source text and matched exactly once (TC-402) |
| A-6 (name matching) | declared in §6.3 (fails loud) |
| S-8 | folded: the Setup view's `team.json` read via `_read_json` (A-3, LLR-402.3); typed text and OS paths declared non-doors (§1.2); legacy `history.jsonl` routed to BACKLOG (D-409) |
| S-9, UX-8 | routed to BACKLOG at close |
| A-2 | folded: the clipboard cleaner shares `strip_controls` (LLR-402.1, TC-414); D-404 rewritten |
| A-3 | folded: LLR-402.3 (increment 002 takes `app.py` as its third SOURCE file) |
| A-4 | folded: D-408 (keys cleaned, later wins; control-only phase → default phases; path settings accepted) with boundary arms in TC-407 / TC-408 |
| A-5 | folded: §1.2 Out line |
| A-7 | carried to increment 001's reverse census |
| Q-2 | folded: per-site payloads; path sites use a directory `a[B]x` and whole-path equality (§5, AT-403) |
| Q-3 | folded: declared fault injection, white-box TC-412 (D-407) |
| Q-4 | folded: one run per site inside each AT node, failures collected, base run recording every site RED (§5) |
| Q-5 | folded: parsed saved-file strings; ESC and C1 on screen, BEL at model/file level (HLR-402) |
| Q-6 | folded: AT-405 is the C-12 chain through the app's own save and push; the direct-written teammate file is TC-409's consumer-contract guard |
| Q-7 | folded: "a board file holding no control byte"; a through-app round trip in AT-404 |
| Q-9 | folded: §5.1 reachable-site table, both duplicate-phase sites and the project confirms named |
| Q-10 | folded: Setup ids expected lowercased (§5) |
| Q-11 | folded: threshold marked predicted until P3; priority `high` in AT-406 |
| Q-12 | folded: LLR-402.3 worded over the files' contents; the file-name id is matched, never painted |
| UX-1 | folded: `height: auto`, wrap (LLR-403.1, D-406) |
| UX-2 | folded: compact kept (PV-1) |
| UX-3, UX-4 | left to the operator's verdict on the captures (PV-1 notes) |
| UX-5 | folded: the 80×24 visibility arm (HLR-403) |
| UX-6 | folded: toasts read from the painted `Toast` (§5) |
| UX-7 | folded: declared in D-404 (accepted) |

---

## Iteration 2 (2026-10-03) — the same four lenses over the iteration-2 contract

- **Gate:** `iterate-to-refine` → Phase 1 (qa blocker Q2-1); no HIGH — the batch continues under the standing authorization.
- **Verdicts:** qa FAIL (1 blocker, 5 major, 5 minor); architect PASS-WITH-NOTES (1 major, 4 minor); security PASS-WITH-NOTES (0 new HIGH, 3 MEDIUM, 3 LOW; S-1 and S-2 requirement-closed, S-1 stays `BLOCK-UNTIL` until the P3 fix is applied and verified); ux PASS-WITH-NOTES (1 major, 4 minor).
- **Iteration-1 discharge (re-read by each lens):** Q-1, Q-3, Q-4, Q-5, Q-8, Q-10, Q-11, Q-12 discharged, Q-2, Q-6, Q-7, Q-9 partial (closed by Q2-1, Q2-3, Q2-4, Q2-5, Q2-8 below); A-1..A-6 discharged, A-7 carried to P3; S-1, S-2 requirement-closed, S-3 partial (S2-1, S2-2), S-4..S-9 closed or routed; UX-1, UX-2, UX-5, UX-6, UX-7 closed, UX-3/UX-4 with the operator.

| ID | Reviewer | Severity | What | Disposition (iteration 3) |
|----|----------|----------|------|---------------------------|
| Q2-1 | qa | blocker | the transition-log toast compared with `str(path)`; the Windows OS error carries `repr(path)` (P-16) | folded: expected = the error text of the same failing write; trigger named (HLR-401, AT-403) |
| Q2-2 | qa | major | five exemptions in code, three in the contract; the help-modal shape undeclared; TC-402's negative control misstated | folded: LLR-401.1 names five; a sink over an exempt parser site counts inert; negative control corrected |
| Q2-3 | qa | major | `image_block` branches and the editor preview rest on AT-007 with too few payloads and one branch | folded: §5.1 rows per branch into AT-401; install branch n/a declared |
| Q2-4 | qa | major | AT-405 green under a single reverted door | folded: the pushed file's parsed strings asserted; the startup sync named |
| Q2-5 | qa | major | AT-404's through-app round trip names no save | folded: dropped from AT-404; TC-410 owns the round trip |
| Q2-6 | qa | major | AT-407's "0 actions" needs instrumentation; sync trigger and project state unnamed | folded: `[@click=app.view('gantt')]X` (view unchanged), existing + new project, startup sync |
| Q2-7 | qa | minor | sites by function, not key; toast read method | folded: keys column, toast read in §5 |
| Q2-8 | qa | minor | a bracket after a separator promised, not defined | folded: `[B]x` directory arm |
| Q2-9 | qa | minor | planted module lacks `.tooltip =`, `border_subtitle`, `set_options`, `replace_option_prompt`, `render` | folded: planted (LLR-401.1) |
| Q2-10 | qa | minor | any call named like a `-> Text` function trusted | folded: bare name or `self.<method>` only (§1.3) |
| Q2-11 | qa | minor | HLR-403 thresholds predicted | folded: executed (P-14) |
| A2-1 | architect | major | "refused" judged on the output; absent keys; `null` dates; HLR/LLR disagree on `""` | folded: refusal on the input, present keys only, `null` clears (D-410, LLR-404.1, HLR-404) |
| A2-2 | architect | minor | board-file load path normalises hand-edited fields; HLR-402 overclaims | folded: HLR-402 "a board file the app saved"; D-410; TC-408 arms |
| A2-3 | architect | minor | a second highlight dispatch | folded: one tokeniser `views.highlight_segments` (D-411; increment 001 takes `views.py`) |
| A2-4 | architect | minor | HLR-404's picker clause has no LLR under it | folded: moved to LLR-401.3 (HLR-401) |
| A2-5 | architect | minor | A-7 supersessions not in PLAN | folded: PLAN increment 001 names them |
| S2-1 | security | MEDIUM | roster names/hues and duplicate ids crash views and pickers | folded: HLR-404 roster clause, LLR-404.2, TC-416, AT-407 arms (P-15) |
| S2-2 | security | MEDIUM | `project_color_on_load([])` raises — the fix's own new crash | folded: any-type colour (LLR-404.1), arms `[]`, `{}` |
| S2-3 | security | MEDIUM | census misses `render`, keyword method sinks, tuple rebinding, `from_values`, `prompt=`, aliased parser, `setattr` | folded: owed at P3 in TC-403's planted set (LLR-401.1) |
| S2-4 | security | LOW | a piece style from data can carry an OSC-8 link | folded: D-413, LLR-401.3 statement; checked in code review |
| S2-5 | security | LOW | a bare-name exemption keyed by name only | folded: keyed with its binding (LLR-401.1) |
| S2-6 | security | LOW | absent keys, `null` dates, non-bool `archived` / `pinned` | folded: LLR-404.1 |
| UX2-1 | ux | major | no check catches a lost style in ~60 conversions | folded: TC-415 painted-style pins vs base (LLR-401.3) |
| UX2-2 | ux | minor | `\[ \] month`, `\[ / ] reorder` could show a backslash | folded: pinned in LLR-401.3 |
| UX2-3 | ux | minor | wrap geometry under-specified | folded: value column, next label, whitespace-normalised, 80×24 with the long name (HLR-403) |
| UX2-4 | ux | minor | where `on_track` is read; a live sentinel | folded: painted picker line; visible-effect action (HLR-404) |
| UX2-5 | ux | minor | only `!!` pinned; preview via `.text` | folded: three tones, keys typed (LLR-401.3) |

---

## Iteration 3 (2026-10-03) — discharge re-read by the same four lenses

- **Gate:** `approve` → Phase 3 (0 blocker, 0 HIGH) under the standing authorization, with the notes folded at the gate (ledger LED .9). **S-1 (HIGH) stays `BLOCK-UNTIL: S-1`** — requirement-closed, open until increments 001/002 apply its fix and `security-reviewer` verifies it.
- **Verdicts:** qa PASS-WITH-NOTES (Q2-1..Q2-11 all discharged; Q3-1 major, Q3-2..Q3-6 minor); architect PASS-WITH-NOTES (A2-1..A2-5 discharged; A3-1 major, A3-2 minor); security PASS-WITH-NOTES (S2-1..S2-6 discharged, S2-3's planted forms owed at P3; S3-1, S3-2 LOW); ux PASS-WITH-NOTES (UX2-1..UX2-5 discharged; UX3-1, UX3-2 minor).

| ID | Reviewer | Severity | What | Disposition |
|----|----------|----------|------|-------------|
| A3-1 | architect | major | the Setup view builds its roster from the raw config (`app.py:409`, `:1032`), so LLR-404.2's rule misses it; the identity picker reads raw `roster()` | folded: `clean_roster` read by `roster()` and the Setup read/republish (LLR-404.2, D-412) |
| A3-2 / S3-1 | architect, security | minor / LOW | an existing project's duplicate synced entries: the last wins | folded: first entry per id, existing or new (LLR-404.1), TC-413 arm |
| S3-2 | security | LOW | `archived` on an existing project unpinned; phases and extras unvalidated | folded: boolean guard in LLR-404.1 with arms; D-414; bounds → BACKLOG |
| Q3-1 | qa | major | `archived` / `pinned` / start clauses have no arm | folded: TC-413 and TC-408 arms |
| Q3-2 | qa | minor | duplicate ids fed to AT-407 with no assertion | folded: one line / one roster entry per id, the first |
| Q3-3 | qa | minor | TC-415's base flags unsourced | folded: recorded before the conversion with a base transcript |
| Q3-4 | qa | minor | long name unpinned; continuation x unmeasured | folded: `LONG` pinned; asserted at P3; probe comment 89 chars |
| Q3-5 | qa | minor | file-backed image branches vs payloads | folded: bracket payload only there, declared |
| Q3-6 | qa | minor | AT-407 click location and identity state | folded: each status cell, one run per cell; no-identity and `a` runs |
| UX3-1 | ux | minor | §5.1 promised style pins TC-415 does not list | folded: sentence narrowed |
| UX3-2 | ux | minor | the gantt-view payload's base RED unrecorded | folded: recorded at P3 |

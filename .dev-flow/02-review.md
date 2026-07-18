# Review — taskboard — Batch 2026-07-18-batch-01

> **Artifact language:** English. Phase 2 artifact.
> Reviewers (independent, single-agent multi-lens): `architect` ∥ `qa-reviewer` ∥ `security-reviewer`.

## ✅ Verdict (read first)

- **Gate:** **PROCEED to Phase 3** — **0 blockers**. 4 majors + 5 minors to fold into Phase 3 (a light Phase-1 patch is recommended for M1 + M3/M4; neither forces a requirements redesign).
- **Findings:** `0` blocker · `4` major · `5` minor
- **shall/should check:** ✓ clean — every `should` sits in preamble/rationale/context; **zero** modal `should` inside any HLR/LLR **Statement** (grep-confirmed, 31 statement lines all use `shall`/`may`).
- **Two-layer (blockers):** ✓ every story has an `AT` (US-001→AT-001, US-002→AT-002, US-003→AT-003) · every output req names deliverable+observation · both trace chains complete (§5.2) · ATs are black-box (drive `Board.load` / Pilot keypresses / boundary-mock seams). No two-layer blocker.
- **Census (change-first):** done — best-effort + gate-confirmed. **One missed observer** (test at `test_app.py:361` constructs `Task(url=…)`) → M1. NOT stamped "VERIFIED COMPLETE".
- **Security:** ⚠ 2 major hardening findings (M3 no existence/regular-file check on `os.startfile`; M4 `.svg` in the startfile allowlist) + 1 minor (no open-all cap). Core allowlist IS present and blocks the primary `.exe`-by-association execution vector — hence hardening, not blocking, under the single-user trust boundary (A-1).
- **Evidence checklists (architect / qa / security):** ✓ all complete below.

> Gate = PROCEED. The 4 majors are correctness/robustness improvements that the software-dev + security-reviewer loop must land during Phase 3; M1 and M4 are also cheap to patch in Phase 1 and I recommend doing so to avoid a surprising red suite / a mis-scoped acceptance criterion.

---

## Detail (reference)

### Findings

| ID | Reviewer | Severity | Area / Req | What | Recommendation | Status |
|----|----------|----------|------------|------|----------------|--------|
| F1 | qa / architect | **major** | §2.5 A-3 · §6.3 R-2 · §5.3 (supersession / C-26) | **Missed test observer.** The reverse-census names only `test_url_task_open_action` (`test_app.py:382-391`) and `test_url_renders_link_and_arrow` (`394-398`). A **third** site breaks when `url` is removed/replaced (LLR-002.1): `test_columns_card_indicators_never_overlap_title` builds `Task(..., url="https://example.com/x")` at **`test_app.py:361`** — a constructor kwarg, so it raises `TypeError` at construction, not `AttributeError`. §5.3's claim "the two URL tests updated" and "28 tests green after the migration touch" is therefore incomplete (3 breakage sites across 2 test functions; the `url=` kwarg escapes a naive `\.url\b` grep). | Add `test_app.py:361` to the migration-touch list (A-3, R-2); correct §5.3 to "the URL-dependent tests (`:361`, `:382-391`, `:394-398`) updated." Update line 361 to `urls=["https://example.com/x"]`. If LLR-002.1 keeps a read-only `url` mirror property, note that; if it removes the field outright (current DD-2 recommendation), the constructor call MUST change. | open |
| F2 | qa | **major** | HLR-007 / LLR-007.2 · AT-003 (C-10-adjacent) | **NEW binding wiring unverified.** LLR-004.2/007.2 executed-verification calls `app.action_open_url()` / `action_open_images()` **directly** (mirrors existing `test_app.py:390`). The open-image binding (proposed `i`) is brand new — calling the action method never proves the `i` key is actually bound in `BINDINGS`. A green AT would pass even if `i` is unwired. | AT-003 must press the real key through Pilot (`await pilot.press("i")`) at least once and assert the open occurred, in addition to any direct-method leg. Same for confirming `o` still fires post-migration in AT-002. | open |
| F3 | security | **major** | LLR-007.3 (C-6, R-1) | **Extension-only gate; no existence / regular-file / path check.** The allowlist checks `Path(ref).suffix.lower()` only. It does not require the path to be an existing **regular file**, and does not guard UNC (`\\host\share\x.png`), `file://`, or non-existent paths. `os.startfile` on a missing path raises `OSError` (a crash on keypress); a UNC path triggers network access. C-4's no-raise convention covers model load, not this action. | LLR-007.3 shall additionally require `os.path.isfile(ref)` (existing regular file) before `os.startfile`, wrap the call in `try/except OSError` (log-and-ignore, never crash), and reject paths beginning with `\\` / `//` (UNC) unless explicitly in scope. Add a negative TC leg: non-existent path → 0 `startfile` calls, no exception. | open |
| F4 | security | **major** | LLR-007.3 allowlist member `.svg` (R-1) | **`.svg` partially defeats the allowlist's stated purpose.** The allowlist exists (C-6) to prevent code execution via OS association. `.svg` is a scriptable format; on Windows `os.startfile("x.svg")` typically opens in a browser that executes embedded script. R-1 acknowledges this as "residual, acceptable" but it is the one member that undermines the control. | Remove `.svg` from the **`os.startfile`** local-path allowlist (keep it, if desired, only for `http(s)` refs routed through `webbrowser`). Final allowlist for the startfile branch: `{.png,.jpg,.jpeg,.gif,.webp,.bmp}`. Requires `security-reviewer` sign-off either way (already gated in §5.3/§6.3 R-1). | open |
| F5 | security | minor | HLR-004 / HLR-007 (open-all) | **No cap on open-all.** A task with 100 URLs/images opens 100 tabs/viewer windows. Low risk (single-user own data, A-1) but unbounded. | Add a sane cap (e.g. open ≤ N, or a `ConfirmModal` above a threshold). Or explicitly record "no cap — own-data trust boundary" as a DD so the choice is deliberate. | open |
| F6 | architect | minor | LLR-004.1 / `title_markup` (`views.py:108-121`) | **OSC-8 link target ambiguous for multi-URL.** `title_markup` wraps the title in `[link={url}]`. With `task.urls` a list, the spec says render `↗` when `any(valid_url)` but never states **which** URL becomes the single OSC-8 link target. | Specify "the FIRST valid URL becomes the `[link=…]` target" in LLR-004.1 so the render is deterministic. | open |
| F7 | qa | minor | HLR-006 boundary catalog | **Vacuous safety-boundary.** HLR-006's boundary lists "markup in a ref escaped on render — C-3", but image refs are **not** rendered into any markup sink on the card (only a width-1 glyph is drawn; the modal `TextArea` is a plain-text widget). The boundary implies a rendering path that does not exist. | Reword to reflect that image refs are not a markup sink in the core (glyph-only); drop or re-scope the C-3 note for images. Keep the C-3 net for **URLs** (where it genuinely applies via `valid_url`). | open |
| F8 | architect | minor | §1.3 glossary citation | **Imprecise `file:line`.** Glossary cites `models.py:325` for "Standalone task — `project_id is None` … Inbox". `models.py:325` is `tasks = [` inside `seed_data()`. The field default is `models.py:185` (`project_id: str \| None = None`); the Inbox rule is `views.py:325` (correct). | Change the models cite to `models.py:185` (field default). `views.py:325` is correct. | open |
| F9 | qa/security | minor | AT-002 (markup-safety visibility, C-17) | Hostile-URL coverage is folded into AT-002's boundary catalog ("markup/injection line dropped by `valid_url`") and the existing `test_markup_injection_is_escaped` — the net EXISTS and is not bypassed. But no AT step explicitly drives a `[link]`-injection **URL** line and asserts literal render / no `MarkupError`. | Add an explicit AT-002 step: enter a URL line containing `]`/`[`, save, assert it is dropped by `valid_url` and the board renders without `MarkupError`. Makes the C-17 guarantee observable, not implied. | open |

**Blocker count: 0.** Major: 4 (F1–F4). Minor: 5 (F5–F9).

### shall / should check
> Any modal `should` / `debería` inside an HLR/LLR statement is a writing error → blocker.

✓ **Clean.** Grep over `01-requirements.md`: every `should` occurrence is in the template preamble (lines 8, 34) or in prose/rationale — **none inside an HLR/LLR Statement line**. All 7 HLR + 23 LLR statements use `shall` for binding clauses and `may` for the one optional (LLR-007.4 inline-preview). LLR-007.4 correctly pairs `may` (optional preview) with `shall` (the mandatory fallback). No misuse.

### Two-layer acceptance review (blockers)
> (a) every story has a black-box `AT`; (b) every output-producing req names deliverable + observation; (c) BOTH chains complete; (d) each `AT` genuinely black-box.

| Story / Req | (a) AT present | (b) deliverable+method named | (c) both chains | (d) black-box pure | Status |
|-------------|----------------|------------------------------|-----------------|--------------------|--------|
| US-001 | AT-001 | yes — on-disk `board.json` + in-memory `Board`, denylist-regex + dimension-set observation | yes (US→AT-001; US→HLR-001→LLR-001.1..6→TC-001x) | yes — drives `Board.load(tmp_path)` (shipped surface); asserts serialized artifact | ✓ |
| US-002 | AT-002 | yes — `Task.urls` (reloaded), `↗` in `board_text`, collected `webbrowser.open` calls | yes (US→AT-002; US→HLR-002/003/004→LLRs→TC-002x/003x/004x) | mostly — Pilot keypress + boundary-mock of `webbrowser.open` (standard seam, matches existing `test_app.py:382-391`). See F2 re: press the binding | ✓ (F2 sharpens) |
| US-003 | AT-003 | yes — image glyph in `board_text`, collected `os.startfile`/`webbrowser.open` calls | yes (US→AT-003; US→HLR-005/006/007→LLRs→TC-005x/006x/007x) | mostly — same seam pattern. F2: must press the NEW `i` binding, not only the action method | ✓ (F2 sharpens) |

No two-layer blocker. AT default-reliance (C-10): all three ATs drive **non-default** values (AT-001 a full seed, AT-002 three URLs incl. one invalid, AT-003 an image path + image URL + a non-image path) — none confirms only a default. ✓

### Supersession census (change-first)
> Planned edited files: `models.py`, `modals.py`, `views.py`, `app.py`, `tests/test_app.py`. Guard families checked against each.

- **behavioral-placeholder guards:** none in this repo (no deferral/"not-yet" assertions). N/A.
- **structural / placement / allowlist / AST / engine-frozen guards:** none — this repo has no path/module-shape/import-graph/git-freeze test guards (verified: `tests/` is a single `test_app.py` of behavioral+render tests). N/A.
- **behavioral observers of the changed contract (`Task.url`):** reverse-grep `\.url\b` + `url=` over `tests/` → **3 sites in 2 functions**: `test_app.py:361` (`Task(url=…)` constructor — **MISSED by the spec**, F1), `:388` (`t.url` read — acknowledged A-3), `:391` (`url_task.url` read — acknowledged A-3). `test_url_renders_link_and_arrow` (`:394-398`) depends on the seed producing a `↗` (indirect; acknowledged).
- **Reservation / what the I-gate must confirm:** the completeness guarantee is the increment gate (run the real suite). This census is a cost-reduction heuristic and it surfaced one missed observer (F1). Not stamped "VERIFIED COMPLETE" — the (N+1)th observer that F1 found is exactly why.

### Security review summary
**Attack surface this batch is real** (the batch's key surface): `os.startfile` (US-3, execute-by-association) + multi-URL/image "open-all" (US-2/US-3).

- **`os.startfile` allowlist (LLR-007.3):** PRESENT and blocks the primary vector — `.exe`/`.bat` never reach `startfile` (negative TC: `["C:/evil.exe","C:/ok.png"]` → 1 call for ok.png only). This is why there is **no blocker**. Two hardening gaps: **F3** (no existing-regular-file check, no UNC/`file://`/non-existent guard, no exception wrap) and **F4** (`.svg` is scriptable and partially defeats the control's purpose).
- **URL scheme allowlist (US-2):** `valid_url` enforces `http(s)` and rejects `[`/`]`/whitespace/newline (`views.py:97-105`) — scheme allowlist satisfied; `file://`/`javascript:` refs fail `valid_url` → not opened. ✓
- **Open-all abuse (F5):** unbounded count, low severity under single-user trust; recommend a cap or a deliberate DD.
- **Migration reversibility (DD-2):** one-way door **explicitly acknowledged and flagged loudly**; corrupt/partial load handled (LLR-002.2: non-list `urls`→`[]`, `url:None`→`[]`, no raise; corrupt file→empty board, existing `test_app.py:434-439`). ✓ No finding.
- **Markup-safety (C-17):** URLs pass through the preserved `valid_url` guard before `[link=…]` (LLR-003.2, LLR-004.1); images are not a markup sink (glyph-only). Net not bypassed → **no mandatory-LLR blocker**. F9 makes the URL guarantee explicitly observable in AT-002.

**Security verdict:** proceed with F3+F4 folded in; `security-reviewer` sign-off on the final `os.startfile` branch remains a §5.3/§6.3 R-1 merge gate.

### Evidence checklists (full)

**Architect gate**
- [✓] Completeness — all 3 US decompose to HLR→LLR with no orphan requirement. Trace tables §5.2 complete both directions.
- [✓] Ambiguity — one residual (F6: OSC-8 target for multi-URL) + one imprecise cite (F8). Minor.
- [✓] Contradiction — none. DD-2 (one-way migration) is internally consistent with LLR-002.2/§5.3.
- [✓] Derivation soundness — LLR-001.4 correctly declares its cross-HLR composition dependency (needs LLR-002.1/005.1 first; dependency order recorded).
- [✓] Draft-time symbol verification — spot-checked 20+ cites against source: `Task.url` `models.py:190` ✓, `seed_data` `:311` ✓, `PROJECT_STATUSES/TASK_STATUSES/TASK_PRIORITIES` `:19/20/21` ✓, `from_dict` legacy `url` `:204` ✓, `card_cell` `views.py:142-161` ✓, `valid_url` `:97-105` ✓, `↗`/`◉` tokens `:154/156` ✓, `action_open_url` `app.py:252-255` ✓, `o` binding `:48` ✓, `os` NOT imported `app.py:1-17` ✓, `TaskModal`/`#f-url` `modals.py:28/66-68` ✓, `_on_task_*` setattr/`Task(**data)` `app.py:206/221-222` ✓. One imprecise (F8, `models.py:325`).
- [✓] Probe self-test — denylist probe recorded 16 pre-state hits (LLR-001.5); dimension probe recorded missing `cancelled` + missing archived items. Both re-derivable from `models.py:318-346` (seed has `Textual/GRNDIA/Job Hunt`, no `cancelled` status, `archived=False` throughout). ✓

**qa-reviewer gate**
- [✓] Acceptance criteria use Given/When/Then equivalents — HLR Acceptance blocks state Observable outcome / Shipped surface / Deliverable+observation; boundary catalogs present.
- [✓] Test cases have explicit Expected — numeric pass thresholds on every `test`/`analysis` LLR (e.g. `startfile calls == 1`, `urls length == 2`, `denylist == 0`).
- [✓] Edge cases include empty/boundary/invalid/error — every HLR boundary catalog (QC-3) covers all four.
- [✓] Regression checklist exists — §5.3 (28 pre-existing green) + R-2. **Incomplete** re: the 3rd observer → F1 (major).
- [✓] Exit criteria stated — §5.3 batch acceptance criteria.
- [✓] No real PII / secrets — denylist scrubs author identity; seeds are neutral.
- [✓] Test results left blank — spec is pre-implementation; no fabricated pass claims.
- [✓] Layer B (black-box) — each output story observed through shipped surface with boundary+negative evidence (AT-001/002/003). F2 sharpens the NEW-binding leg.
- [✓] Bidirectional surface-reachability — inputs (multi-URL, image path, image URL, non-image path) AND deliverables (seeded `board.json`, `urls`/`images` lists, `↗`/image glyph, opened refs) all exercised through the handler/UI, not only the service API (LLR-001.4 explicitly composes the two new fields into the seed per rule A-5).
- [✓] No unfilled template — the scaffold placeholders are fully replaced; the phase actually ran (denylist + dimension probes executed with recorded pre-state).

**security-reviewer gate**
- [✓] Attack surface enumerated — `os.startfile` (exec-by-association), open-all, migration data-loss, markup injection. §2.4 C-3/C-6, §6.3 R-1.
- [✓] Sensitive data — single-user local trust (A-1); no secrets; author identity scrubbed by denylist.
- [✓] Unsafe calls gated — `os.startfile` behind extension allowlist (LLR-007.3). **Hardening gaps** F3 (existence/regular-file/UNC/exception) + F4 (`.svg`).
- [✓] URL scheme allowlist — `valid_url` http(s)-only, injection chars rejected (`views.py:97-105`). ✓
- [✓] Unbounded action — F5 (no open-all cap), low severity.
- [✓] Reversibility / data-loss — DD-2 one-way door flagged; lenient load handles corrupt/partial. ✓
- [✓] Merge gate — `security-reviewer` sign-off on the final `os.startfile` branch required before merge (§5.3, §6.3 R-1); F3+F4 are its inputs.

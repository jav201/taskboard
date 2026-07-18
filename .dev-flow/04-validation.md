# Validation — taskboard — Batch 2026-07-18-batch-01

> **Artifact language:** English. Phase 4 artifact. Owner: `qa-reviewer`.
> Executes the Phase-1 validation strategy (§5). No code changed in this phase.
> Suite run 2026-07-18: `.venv\Scripts\python.exe -m pytest -q` → **`36 passed in 12.08s`**; `--collect-only -q` → **36 collected**.

## ✅ Verdict (read first)

- **Result:** **PASS → proceed to Phase 5.** No Phase-4 blocker.
- **Requirements:** 7/7 HLR pass · 22/22 CI-gated LLR pass · 1 LLR (`LLR-007.4`, `demo`-only inline preview) intentionally out of CI — **0 blocker fails**.
- **Black-box acceptance (Layer B):** ✓ every story's `AT` observes its outcome through the **shipped surface** (Pilot keypress / on-disk `board.json`) with representative + boundary + **negative** evidence. AT-001/002/003 each reconcile to **exactly one distinct collected node** (C-18).
- **Surface-reachability (bidirectional):** ✓ all 4 named input dimensions AND all 4 named deliverables reached/observed **through the handler**, not only the service API.
- **Supersession inspection:** ✓ the superseded singular `Task.url` has **zero live source references**; its only surviving reference is a **negative** assertion (`not hasattr(...)`). Author-denylist over the shipped seed = **0**.
- **Test ledger:** ✓ reconciles — `base 28 − D 0 + A 8 = 36`; actual collected = 36; passed = 36.
- **Evidence checklist (qa-reviewer):** ✓ complete (below).
- **Honestly-open items (both ACCEPTED, not failures):** (1) `▤` **true terminal cell-width** is unverifiable headlessly — attributed to C-2/C-5, proven single-cell only by Python line-width invariance; (2) **inline image preview intentionally not built** — degrades to open-in-viewer per the stretch `LLR-007.4` (`may`).

---

## AT → node reconciliation (the 3 required rows, C-18)

| US | Acceptance test (single driving node) | Observable outcome | Shipped surface | repr · boundary · negative | Result |
|----|---------------------------------------|--------------------|-----------------|----------------------------|--------|
| US-001 | `tests/test_app.py::test_at_001_seed_generic_and_complete` | Freshly seeded board has **0** author tokens + ≥1 item in every feature dimension | `Board.load(fresh_path)`→`seed_data()`; **on-disk `board.json`** read back (`:535`) | repr: full seed · boundary: exactly-one-item per `≥1` dim (archived proj/task, ≥2-URL task, ≥1-image task) · **negative:** `SEED_DENYLIST.findall(on_disk) == []` (`:536`) | **pass** |
| US-002 | `tests/test_app.py::test_at_002_multiple_urls_black_box` | 3+ URLs entered in modal → card shows `↗`; pressing **real `o`** opens every valid URL | `TaskModal` `#f-urls` TextArea → save handler → `card_cell`/`title_markup` → `action_open_url` bound to `o` (`app.py:54`) | repr: 2 valid URLs kept in order (`:462`) · boundary: `↗` present in `board_text` (`:466`) · **negative:** markup `[boom]` line + `not a url` line dropped by `valid_url`, no MarkupError; `o` opens exactly the 2 valid (`:470-471`) | **pass** |
| US-003 | `tests/test_app.py::test_at_003_images_black_box` | Image refs entered → card shows `▤`; pressing **real `i`** opens the image URL (browser) + existing image-ext file (`startfile`) | `TaskModal` `#f-images` TextArea → save handler → `card_cell` `▤` glyph → `action_open_images` bound to `i` (`app.py:55`) | repr: `startfile==[real_png]`, `browser==[http url]` (`:594-595`) · boundary: `▤` present + all lines width-exact ⇒ single-cell (`:586-588`) · **negative:** `.svg`, `.exe`, missing file NONE `startfile`'d (`:596-597`) | **pass** |

**Proxy-vs-real check (F2 discharged):** AT-002 drives `await pilot.press("o")` (`:470`) and AT-003 drives `await pilot.press("i")` (`:593`) — the **real key bindings**, not a direct `action_*()` method call. Bindings verified live: `("o","open_url",…)` `app.py:54`, `("i","open_images",…)` `app.py:55`. A green suite could not pass with `i`/`o` unwired.

**Author-token negative:** `SEED_DENYLIST` (16-token author regex, `test_app.py:515-518`) over the **actual persisted** `board.json` returns `[]` (`:536`). Mutation-checked in Increment 3 (renaming a project to "Textual Redesign" → AT-001 RED).

---

## Layer A — functional (white-box): per-requirement results

> `TC-NNN` ↔ LLR/HLR. Evidence = collected node id + assertion line. All nodes GREEN in the 36-pass run.

| Req | Method | Driving node (`test_app.py::`) + line | Numeric threshold | Result |
|-----|--------|----------------------------------------|-------------------|--------|
| HLR-001 | test | `test_at_001_seed_generic_and_complete` | denylist==0; dims complete | **pass** |
| LLR-001.1 | test (unit) | `test_at_001…` `:539,:544` | proj-status 4/4; archived proj ≥1 | **pass** |
| LLR-001.2 | test (unit) | `test_at_001…` `:541-542,:545` | task-status 4/4; prio 3/3; archived task ≥1 | **pass** |
| LLR-001.3 | test (unit) | `test_at_001…` `:547-553` | buckets ⊇{overdue,today,none,done}∧{week\|later}; standalone≥1∧project≥1 | **pass** |
| LLR-001.4 | test (unit) | `test_at_001…` `:555-556` | ≥1 task len(urls)≥2; ≥1 task len(images)≥1 | **pass** |
| LLR-001.5 | test+inspection | `test_at_001…` `:536` | denylist matches == 0 (pre-state 16) | **pass** |
| LLR-001.6 | test (integration) | `test_boots_and_seeds`; `test_corrupt_file_starts_empty` | seeds & saves; corrupt→empty | **pass** |
| LLR-002.1 | test (unit) | `test_task_urls_model_migration` `:406-407` | default==[]; per-instance identity | **pass** |
| LLR-002.2 | test (unit) | `test_task_urls_model_migration` `:409-415` | legacy→[url], modern, 3× malformed→[], 0 raises | **pass** |
| LLR-002.3 | test (integration) | `test_task_urls_roundtrip`; `test_legacy_url_board_migrates_on_load` | 3-URL save→load exact; legacy file→[url] | **pass** |
| LLR-003.1 | test (e2e) + inspection | widget present & wired — `test_at_002…` `#f-urls` TextArea `:454`, `test_at_003…` `#f-images` `:578` | multi-line widget exists, pre-fills task refs | **pass** (see G-001, prefill-on-edit note) |
| LLR-003.2 | test (e2e) | `test_at_002_multiple_urls_black_box` `:462` | 4 lines (2 invalid) → urls==2 valid, order kept | **pass** |
| LLR-004.1 | test (unit/e2e) | `test_at_002…` `:466`; `test_url_renders_link_and_arrow`; `test_columns_card_indicators_never_overlap_title` `:360-377` | ↗ iff ≥1 valid URL; width-1, no overlap | **pass** |
| LLR-004.2 | test (e2e) | `test_at_002…` `:471`; `test_url_task_open_action` `:391` | 2 valid → 2 opens, set-exact; 0→0 | **pass** |
| LLR-005.1 | test (unit) | `test_task_images_model` `:478-479` | default==[]; per-instance identity | **pass** |
| LLR-005.2 | test (unit/integration) | `test_task_images_model` `:480-488` | list read; non-list→[]; round-trip exact | **pass** |
| LLR-006.1 | test (e2e) + inspection | `#f-images` TextArea present & wired `test_at_003…` `:578` | multi-line widget exists, pre-fills images | **pass** (see G-001) |
| LLR-006.2 | test (e2e) | `test_at_003…` `:581` | non-blank lines kept, order preserved | **pass** |
| LLR-007.1 | test (unit/e2e) | `test_at_003…` `:586-588`; overlap test `:360-377` | ▤ iff ≥1 image; every line width-exact | **pass** (cell-width caveat, ACCEPTED) |
| LLR-007.2 | test (e2e) | `test_at_003…` `:594-595`; `test_open_images_allowlist_and_isfile` `:512` | 1 startfile (img file) + 1 browser (http) | **pass** |
| LLR-007.3 | test (unit)+analysis | `test_open_images_allowlist_and_isfile` `:501-512`; `test_at_003…` `:596-597` | startfile ONLY existing image-ext file; .exe/.svg/UNC/file:///missing → 0 | **pass** |
| LLR-007.4 | demo (NOT CI) | — (manual WezTerm) | inline preview OR viewer fallback, no crash | **ACCEPTED open** — not built; degrades to LLR-007.2 |

**Analysis leg (LLR-007.3):** allowlist `{.png,.jpg,.jpeg,.gif,.webp,.bmp}` — `.svg` **excluded** (F4 folded, scriptable). No member executes by Windows association. Guards enforced in `_open_local_image`: UNC/`file://` refused, `Path(...).suffix.lower()` allowlist, `os.path.isfile`, `try/except OSError` (F3 folded). Negative proven live: `["C:/evil.exe", ..., "\\\\host\\share\\a.png", "file:///c:/a.png", missing.png]` → `startfile` called for `ok.png` only (`:512`).

---

## Bidirectional surface-reachability matrix (extends A-5, batch-11)

| Direction | US dimension / deliverable | Producer / param | Reached/observed through the HANDLER? | Node | Status |
|-----------|---------------------------|------------------|----------------------------------------|------|--------|
| input | multi-URL entry (`≥2` lines) | `TaskModal #f-urls` → `data["urls"]` → save handler | yes — `.text=` set on real TextArea, `#save` pressed | `test_at_002…` `:454-459` | ✓ |
| input | image entry (local + http, blanks) | `TaskModal #f-images` → `data["images"]` → save handler | yes — `.text=` set, `#save` pressed | `test_at_003…` `:578-579` | ✓ |
| input | open-url (`o`) | `action_open_url` via `o` binding | yes — `await pilot.press("o")` | `test_at_002…` `:470` | ✓ |
| input | open-image (`i`) | `action_open_images` via `i` binding | yes — `await pilot.press("i")` | `test_at_003…` `:593` | ✓ |
| output | `↗` URL indicator | `card_cell`/`title_markup` | yes — observed in `board_text` | `test_at_002…` `:466` | ✓ |
| output | `▤` image indicator | `card_cell` | yes — observed in `board_text` + width invariance | `test_at_003…` `:586-588` | ✓ |
| output | opened URLs / images | `webbrowser.open` / `os.startfile` | yes — collected via monkeypatch after real keypress | `test_at_002…` `:471`; `test_at_003…` `:594-595` | ✓ |
| output | clean (author-neutral) seed | `seed_data()` → on-disk `board.json` | yes — read back from disk, denylist scanned | `test_at_001…` `:535-536` | ✓ |

No gap: every input is driven through the modal/binding (not direct service kwargs), and every deliverable is observed at the shipped surface (rendered text / opened-call collector / on-disk file).

---

## Supersession-completeness inspection (batch-09 V-3)

| Superseded marker | grep result (2026-07-18) | All surviving refs negative? | Evidence |
|-------------------|--------------------------|------------------------------|----------|
| singular `Task.url` field (read) | `grep -rnE '\.url\b' taskboard/ \| grep -vE '\.urls\b'` → **0 hits** | yes (no live dependency) | source uses `.urls` only |
| singular `url=` constructor kwarg | `grep -rnE 'url=' taskboard/ tests/ \| grep -vE 'urls='` → **0 hits** | yes | all migrated (incl. former `test_app.py:361` → `urls=[…]` `:362`, F1 fixed) |
| legacy `url` field existence on model | `test_legacy_url_board_migrates_on_load :442` | yes — **negative** assertion `not hasattr(Task("t"), "url")` | one-way migration confirmed |
| author-denylist tokens over shipped seed | `test_at_001… :536` (16-token regex over on-disk json) | yes — **negative** assertion `findall == []` | 0 live author references |

All surviving references to superseded artifacts are absence/negative assertions — no live dependency. F1's missed third observer (`test_app.py:361` constructor kwarg) is resolved; the reverse-grep is clean.

---

## Signed-balance test ledger (batch-07 / 09)

| base | − D | + A | = post | actual collected | passed | reconciles? |
|------|-----|-----|--------|------------------|--------|-------------|
| 28 | 0 | 8 | 36 | 36 | 36 | **yes** |

- **D = 0:** no test deleted. Three sites were **edited in place** (migration touch, not deletion): `test_url_task_open_action` (`:388-391`), `test_url_renders_link_and_arrow` (`:397-398`), and `test_columns_card_indicators_never_overlap_title` (`:360-362`, the F1 constructor kwarg).
- **A = 8:** `test_task_urls_model_migration`, `test_task_urls_roundtrip`, `test_legacy_url_board_migrates_on_load`, `test_at_002_multiple_urls_black_box` (Inc-1); `test_task_images_model`, `test_open_images_allowlist_and_isfile`, `test_at_003_images_black_box` (Inc-2); `test_at_001_seed_generic_and_complete` (Inc-3).

---

## Gaps detected

| ID | Requirement | Gap | Severity | Proposed action |
|----|-------------|-----|----------|-----------------|
| G-001 | LLR-003.1 / LLR-006.1 (modal **prefill on edit**) | No test asserts that opening the modal via **`e`** on a task with existing `urls`/`images` renders those refs pre-filled, one per line. The widgets' **presence and wiring** are proven (AT-002/003 set `#f-urls`/`#f-images` `.text` and save successfully); the **read-back prefill** leg is covered by inspection, not a dedicated assertion. | **minor** | Optional: add an edit-path TC that presses `e` on a 2-URL task and asserts the TextArea initial text has both lines. Not a blocker — the write path and the black-box deliverable are both observed; prefill is a read convenience. |

No blocker, major, or Layer-B (deliverable-observation) gap.

## Accepted open items (not failures)

- **`▤` true terminal cell-width (C-2/C-5).** Headless CI proves single-cell only via Python line-width invariance (`test_at_003… :587-588`, overlap test `:367`). True WezTerm rendered cell width is a manual/Phase-3 render check — **attributed, accepted**.
- **Inline image preview (LLR-007.4, stretch).** Intentionally **not implemented**; the `may` clause degrades to open-in-viewer (LLR-007.2), which is fully validated. No overpromise — **accepted per spec**.

---

## Escaped-bug regression

None. No defect escaped the suite in Phase 4; no regression fixture required. (Mutation-sanity was exercised per-increment: open-all→first-only turned AT-002 RED; re-adding `.svg` turned AT-003 RED; "Textual Redesign" rename turned AT-001 RED — all restored green. These are Phase-3 mutation checks, recorded in `03-increments/*`, not Phase-4 escaped bugs.)

---

## Gate verdict

**Validation PASS — proceed to Phase 5.**

- **Every story has a black-box deliverable observation** through the shipped surface, each reconciled to exactly one distinct on-disk collected node (US-001→`test_at_001…`, US-002→`test_at_002…`, US-003→`test_at_003…`), with representative + boundary + negative evidence. **No Phase-4 blocker.**
- **Exit axes:**
  - **Coverage — MET.** 100% of CI-gated LLRs (22/22) have ≥1 passing TC/AT; all 4 input dimensions and 4 deliverables reach/observe the shipped surface. The lone non-CI LLR (007.4) is a spec-sanctioned `demo` stretch. G-001 (prefill assertion) is a minor read-path nuance, not a coverage hole in the deliverable.
  - **Certainty — MET.** 36/36 green; the three ATs are mutation-discriminating (each has a recorded RED under a counterfactual mutation), so the black-box assertions discriminate value, not merely wiring.
  - **Evidence — MET.** Every gate item carries a re-runnable citation (collected node id + assertion line, or `grep` command output).
- **Confirming the framing:** 36 green + 3 mutation-checked ATs **is** sufficient to pass — but the pass rests on the ATs being (a) driven through the **real bindings** (`o`/`i` pressed, F2), (b) observing the **actual on-disk deliverable** for US-001, and (c) carrying **negative** legs (dropped-invalid-URL, refused-`.exe`/`.svg`/missing, zero author tokens). All three hold. Challenge resolved: **confirmed PASS**, no iterate-to-fix (P3) or iterate-to-refine (P1) triggered.

---

## Evidence checklist — qa-reviewer (full)

- [✓] Acceptance criteria use Given/When/Then equivalents — HLR Acceptance blocks (Observable outcome / Shipped surface / Deliverable+observation) drive the ATs; the AT→node table above states each outcome.
- [✓] Test cases have explicit Expected — every Layer-A row carries a numeric threshold and a passing node id/line (e.g. `urls==2 valid @:462`, `startfile==[real_png] @:512`).
- [✓] Edge cases include empty, boundary, invalid, error — empty (0-URL/0-image no-open), boundary (exactly-one-item seed dims; single-cell glyph), invalid (`not a url`, non-list refs), error (corrupt file→empty `:637-638`; missing/UNC/`file://` refused; markup line no MarkupError).
- [✓] Regression checklist exists — supersession inspection (singular `url` gone, 0 live refs) + ledger (`28−0+8=36`) + pre-existing suite green.
- [✓] Exit criteria stated — the three axes above; §5.3 batch acceptance re-verified.
- [✓] No real PII / secrets — seed scrubbed to 0 author-denylist tokens over the on-disk deliverable (`:536`); no credentials in tests or artifact.
- [✓] Test results NOT fabricated — every result cites the actual `36 passed` run and a collected node id; nothing marked pass without a node.
- [✓] Layer B (black-box) — each output-producing story observed through the SHIPPED surface (Pilot `o`/`i` keypress; on-disk `board.json`) with boundary + negative evidence — not only white-box TCs on the mechanism.
- [✓] Bidirectional surface-reachability — all 4 inputs (multi-url, image, open-url, open-image) AND all 4 deliverables (↗, ▤, opened refs, clean seed) exercised/observed through the handler (matrix above).
- [✓] No unfilled template — no `<...>` placeholder, no `TC-NNN` stub, no empty required row remains; the phase actually ran (36-pass suite + greps executed).

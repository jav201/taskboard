# Increment 002 — HLR-202 · the chrome: key bar, ribbon, modal titles, help key map

> Review packet (flow `templates/increment-template.md`; reserved field names kept literal).
> Lives in the repo next to the diff it describes. Mode `core`, language `en`. Flow pinned to rev98.

| Field | Value |
|---|---|
| Batch | `2026-10-02-batch-02` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | HLR-202 (LLR-202.1 amended by LED .16, LLR-202.2) |
| Acceptance | AT-202 · white-box TC-203, TC-204 ×2 |
| Agent | `software-dev` (this runtime's implementing agent) |
| Date | `2026-10-02` |

---

## 1 · What changed

**The chrome spends no accent outside the field being edited.** Every key in the key bar is bold
bright with its word muted, in both layers (the eight per-group hues are gone); the ribbon's local
time is bold bright, the city names `mut` and their times `hd`; every modal title and help heading
is bold bright (`.modal-title`); the help key map draws its heading and keys bold bright. Focused
input borders keep the accent (the edited-field focus role). **Code review found a pre-existing
bug, fixed here (D-218):** `;` never showed the key bar's `more` layer — the toggle read
Textual's CSS `layer` (always `"default"`) instead of `bar_layer` — so half of "both layers" had
been invisible since commit 8b73920.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/keymap.py` | source | LLR-202.1 | `GROUP_HUE` removed; one `KEY_STYLE` (bold bright) for both layers |
| `taskboard/ribbon.py` | source | LLR-202.2 | local time bold bright; city time `hd` |
| `taskboard/app.py` | source | LLR-202.1, LLR-202.2 | `HelpScreen` heading and keys bold bright; `action_layer_toggle` reads `bar_layer` (D-218) |
| `taskboard/taskboard.tcss` | source | LLR-202.2 | `.modal-title` color `#e6edf7` |
| `tests/test_colour_budget_app.py` | test | HLR-202, LLR-202.1, LLR-202.2 | appended: TC-203, TC-204 ×2, AT-202 (4 nodes) |
| `tests/test_keymap.py` | test | HLR-202, LLR-202.1 | reverse census: keys bold bright, no accent (rewritten in place); the layer test asserts `bar_layer == "more"` and a different bar |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ at the cap — the chrome lives in four files (the bar, the ribbon, the key map's screen, the stylesheet); cutting smaller would leave HLR-202 half-applied, one surface teal and the next white |
| Test files | 2 (uncapped) |
| Doc files | 0 |

## 3 · How to test

```bash
python -m pytest -q tests/test_colour_budget_app.py -k "203 or 204 or AT_202" tests/test_keymap.py
python -m pytest -q
```

## 4 · Test results

| Layer | Owed in | Nodes | Result |
|---|---|---|---|
| **0 · unit** | `core` · `full` | n/a — no unit with 2+ paths added (the bar's two branches were collapsed into one) | — |
| **A · white-box** `TC-NNN` ↔ LLR | `core` · `full` | TC-203 (9 views × 2 layers × 5 widths, frozen base strings), TC-204 ribbon, TC-204 stylesheet + palette + key map source | 3 passed |
| **B · black-box** `AT-NNN` ↔ story, through the shipped surface | `core` · `full` | AT-202 (both bar layers, ribbon, `?` titles, `m` key map spans, `/` focused border) | 1 passed |

Gate run on the frozen round-1 tree: `python -m pytest -q -p no:cacheprovider` → **1634 passed in
201.05s, exit 0** (`evidence/inc002-green.txt`).

### RED counterfactual — executed, not predicted

| Field | Value |
|---|---|
| Mutation applied | the increment-001 tree (HEAD + increment 001's `views.py`) with the new tests; then 16 mutants on the increment tree |
| Where it ran | scratch exports |
| Transcript | `evidence/inc002-red.txt` (the 4 new nodes FAILED; `-k` also matched 5 TC-202/AT-203 nodes, green there by design); `evidence/inc002-mutations.txt` |
| Restore proven by | per-mutant sha256 (`keymap.py` `6f52b1d72c9dabc4…`, `app.py` `8e34f69a8f0e3655…`) |
| Bytecode cache | `-B`, `-p no:cacheprovider` |
| Arms resolved at baseline | 9 |
| Verdict granularity | per node (`-rA`) |
| Arms that stayed GREEN | the 5 increment-001 nodes the `-k 202` filter also matched (not owned by this increment) |

| Field | Value |
|---|---|
| **RED counterfactual** | TC-203, TC-204 ×2 and AT-202 RED on the increment-001 tree (4 failed) (accent keys and group hues, `[b #2dd4bf]09:05:07`, `.modal-title color: #2dd4bf`, 18 key-bar accents) · `evidence/inc002-red.txt` · the review-round nodes RED by MG, F3, MA, MB, MC, C3, P1 · restore digests in `evidence/inc002-mutations.txt` |

| Field | Value |
|---|---|
| **Mutation verdicts** | 16 of 16 KILLED (`evidence/inc002-mutations.txt`, specs `mutants_inc002.json` 9/9 + `mutants_inc002_r1.json` 7/7, round-1 tree): K1 keys accent, K2 keys unbolded, K3 hue on the words, R1/R2 clocks accent, A1/A2 key map accent, C1 titles accent, C2 the edited field loses its accent (a focus role removed), MG accent on the `more` layer only (AT-202 alone), F3 the toggle reverted, MA/MB/MC the key map unbolded/violet/pink, C3 titles unbolded (AT-202 alone), P1 the palette's focus border |

### Instrument RED-proof — every instrument shown able to report FAILURE first

| Instrument | Known-bad input fed to it | The FAILURE it reported |
|---|---|---|
| AT-202's `accents()` over painted widgets | the increment-001 key bar | `18 == 0` (`inc002-red.txt`) |
| the layer check | the pre-fix toggle (mutant F3) | `'primary' == 'more'` |
| the key-map span check | mutants MA, MB, MC | styles outside the allowed set |

| Field | Value |
|---|---|
| **Instrument RED-proof** | 3 instruments, each shown failing before its PASS was believed |

### Emitted-form assertion — assert the bytes the producer EMITS (C-42)

| Artifact emitted | The assertion, run against the EMITTED form | What it returned |
|---|---|---|
| the key-bar markup | parsed with `rich.markup.render`; plain == `key_bar_plain`; each key's own span | TC-203 passed |
| the painted key bar, ribbon, modals | Textual `render()` spans and computed `styles` in `run_test` | AT-202 passed |
| the stylesheet | the `.modal-title` block and the `:focus` rules as written | TC-204 passed |

| Field | Value |
|---|---|
| **Emitted-form assertion** | 3 artifacts, each asserted in the form the producer emitted |

### Evidence files — bytes at a declared home, verbatim, hash-verified (C-59)

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| RED on the increment-001 tree | `.dev-flow/2026-10-02-batch-02/evidence/inc002-red.txt` | `0b0381baadfa9ad6ff17717c6db6fde03e5d684b038663f2982c2da09a3c17f5` |
| mutation battery | `.dev-flow/2026-10-02-batch-02/evidence/inc002-mutations.txt` | `e655857b61c73113c9de9666969601614be278412382d99be572673c86f67605` |
| mutant specs | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc002.json` | `fb76d8a528f875b88534345892276ede872c630fb6d220fe18c0d1b1536266d0` |
| mutant specs, review round | `.dev-flow/2026-10-02-batch-02/evidence/mutants_inc002_r1.json` | `21f472c921dff2ce1bc8b6d1c4a0c8f104eb40fd9ac82ae258c0c389168d75f7` |
| reverse census run | `.dev-flow/2026-10-02-batch-02/evidence/inc002-reverse-census.txt` | `8dfc20e0176179334bcf5762a75f790313e6d207211bc85348c813bb65de80df` |
| gate run | `.dev-flow/2026-10-02-batch-02/evidence/inc002-green.txt` | `23c019805963eb8237d21edf6be370d2965eb749a162e2329e4e0545f6d30643` |
| app + chrome, 118×30 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc002-app-gantt-118x30.svg` | `4d9645a20b569153792bf339c281bf56117dc568456941ab9fba8ae933a3dfc3` |
| help modal, 80×24 | `.dev-flow/2026-10-02-batch-02/evidence/captures/inc002-app-help-80x24.svg` | `91dc2aaef4b5888f2b5d42c37d8eb771812db9428b5042265da1b37c4c5172ea` |

| Field | Value |
|---|---|
| **Evidence files** | 8 artifacts under the declared home, each cited with its digest (`captures/inc002-app-*` at both terminal sizes; base in `captures/base-app-*`) |

### Load-bearing emptiness — what is this resting on that is only true today? (C-55)

| Field | Value |
|---|---|
| Does any claim here rest on the tree holding NO instance of some case? | yes: "no accent in the chrome outside a focus border" |
| If the result is an ABSENCE, what made the search wide enough | every view × both layers × 5 widths of the bar; the painted bar in both layers (the layer asserted); every `.modal-title` of the help modal; every Static of the key map |
| Guard labelled as protecting a CONCLUSION, not a behaviour | the `bar_layer` assertion in AT-202 (code review F1) |
| Conjunctive criteria: one mutation per conjunct | K1–K3, R1–R2, A1–A2, C1–C3, MG, P1 |
| Synthetic instance of the absent case | each mutant |
| **Positive control for every probe that returned an ABSENCE** | C2 and P1: the detectors see the accent where it must stay (the focused borders) |

### Reverse census — trigger family B

| Probe | Command | Result |
|---|---|---|
| B1 symbols asserted by **other** tests | full suite after the edit (`evidence/inc002-reverse-census.txt`: 1 failed / 1633 passed); `grep -rn "GROUP_HUE\|modal-title\|update_clock" tests/` | `tests/test_keymap.py::test_keys_and_words_wear_different_tones_and_neither_judges` pinned accent keys → rewritten in place, its law (keys and words differ; nothing judges) kept; `test_palette_ration.py` (ribbon judges nothing), `test_edit_window.py` / `test_emoji_picker.py` (`.modal-title` content) green |
| B2 file moved on disk | none | did not fire |
| B3 byte-identical golden captures this source | none | did not fire |
| B4 artifact produced here is consumed elsewhere | `.modal-title` is shared by every modal (ConfirmModal's message, the calendar's hint line, the help footer) | all read bold bright now — HLR-202 asks for every modal title (code review F6, informational) |
| A3 | interface consumed by another module changed | `GROUP_HUE` removed | no reader in `taskboard/` or `tests/` |

| Field | Value |
|---|---|
| **Reverse census** | 5 probes: B1 fired (1 node rewritten), B4 fired (shared class, declared), B2/B3/A3 did not fire |

### Correction population — enumerated BEFORE the first site was edited

| Correction | Population — the assertion category | Enumeration method (the command) | Count | Sites edited | Sites left, and why |
|---|---|---|---|---|---|
| accent in the chrome | `accent` / `#2dd4bf` in `keymap.py`, `ribbon.py`, `app.py`, `taskboard.tcss` | `grep -n "2dd4bf\|accent" taskboard/keymap.py taskboard/ribbon.py taskboard/app.py taskboard/taskboard.tcss` | 9 | 6 | 3 `:focus` borders/bars in the stylesheet (the edited-field focus role); `modals.py`'s palette focus border likewise kept |

| Field | Value |
|---|---|
| **Correction population** | 1 correction, enumerated before its first site was edited |

### Signed-balance test ledger

`post = base − deleted + added` → `1634 = 1630 − 0 + 4` ✓ (the `test_keymap.py` rewrites are in place, net 0).

## 4b · Independent review — the lens the author cannot be

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a named sub-agent with `agents/code-reviewer.md` (rev98 snapshot) · round 1: `BLOCK-UNTIL: F1` — F1 HIGH (AT-202 never reached the `more` layer; mutant MG survived), F3 HIGH pre-existing (`;` never left primary — scope decision taken: fixed here, D-218), F2 MEDIUM (key map asserted only "no accent"), F4/F5 LOW, F6 informational; golden double-proof: 3438 bars plain-identical base vs work · all folded, RED proof per finding (MG, F3, MA, MB, MC, C3, P1 killed) · round 2: OK to advance, F1 discharged by re-reading and re-running MG (killed by AT-202, `35 == 0`), nothing open |

## 5 · Risks

- Without group hues the `more` layer is one tone; the P4 walkthrough checks it still reads (ux item 8).
- `.modal-title` styles hint lines too (calendar, help footer) — bold bright at title weight (F6).

## 6 · Pending items / spec deviations

- `;` showing the `more` layer is a visible behaviour change the operator has not seen since 8b73920 (D-218) — named in the close.

## 7 · Suggested next task

Increment 003 — English (HLR-204).

## Increment gate checklist

| # | Item | Owed in | ✓/⚠/✗ | Evidence (node id · command output · file:line) |
|---|---|---|---|---|
| 1 | ≤4 source files, or reason declared | all | ⚠ | 4 / 4, reason in §2 |
| 2 | Tests written in this same increment | all | ✓ | 4 new nodes |
| 3 | Layer 0 written where the criterion applies | `core` · `full` | ✓ | n/a — no 2+-path unit added |
| 4 | **RED counterfactual** declared | `core` · `full` | ✓ | §4 |
| 5 | **Reverse census** declared | `core` · `full` | ✓ | §4 |
| 6 | `code-reviewer` passed | `core` · `full` | ✓ | §4b (round 2) |
| 7 | No file from another lane touched | all | ✓ | one lane |
| 8 | Frozen interfaces untouched (or returned to the trunk) | all | ✓ | `GROUP_HUE` had no reader |
| 9 | Coverage claims verified **on disk**, not from intent | all | ✓ | ids in docstrings |
| 10 | Load-bearing emptiness declared, with its synthetic instance (C-55) | all | ✓ | §4 |
| 11 | **Mutation verdicts** declared | all | ✓ | §4 |
| 12 | **Instrument RED-proof** declared | all | ✓ | §4 |
| 13 | **Correction population** declared | all | ✓ | §4 |
| 14 | **Emitted-form assertion** declared | all | ✓ | §4 |
| 15 | **Independent review** names somebody | all | ✓ | §4b |
| 16 | **Evidence files** declared | all | ✓ | §4 |

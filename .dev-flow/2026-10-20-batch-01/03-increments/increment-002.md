# Increment 002 — LLR-2203.1, LLR-2204.1 · `the chip, the home and B`

> **Artifact language**
> This template is the canonical **English scaffold**. Generate the artifact in the batch's development
> language — the **prose**, and never a label. **Where that language is declared:**
> `state.json`'s `language` key in `core` and `full`. The normative RULES below are
> language-independent.

> **Owed in.** `core` ✓ · `full` ✓

> **Field guide:** `templates/guides/increment-template.md` explains each field below and the rules that read it. It ships with the flow and is not copied into this batch.

> **Reserved field names.** The **field names and block keywords below are language-independent** — the
> validator parses them literally and they are never translated:
> `SOURCE files` · `Instrument RED-proof` · `Correction population` · `Mutation verdicts` · `Emitted-form assertion` · `Reverse census` · `RED counterfactual` · `Independent review` · `Evidence files` · `Traces to` · `File` · `Kind` · `source` · `test` · `doc` · `config` · `generated` · `fixture` · `⏸ DEFER`
> Everything else on this page — headings, guidance, the prose in every cell — is translated with the batch.
> **One strategy, not two:** the flow ships no alias table, so a translated label is read as an ABSENT one and the rule keyed on it reports a true-sounding silence.
> **And one FLOW-WIDE reserved token, read out of this artifact by `V42` no matter which template minted it:** `⏸ DEFER`. It is a MARKER rather than a field name, which is why it is stated here *and* in `/dev-flow` §Language of artifacts rather than in a per-template list — a deferral can be written in any batch artifact, including the ones that carry no block at all.

> **Where this lives:** the **repo**, next to the diff it describes —
> `.dev-flow/2026-10-20-batch-01/03-increments/increment-002.md`. It is not synced to the vault.

> **Notice convention.** `⚠` yellow = notice: does not block, obliges you to DECLARE the reason here.
> `✗` red = block. `✓` green = satisfied **with its evidence cited**. A notice repeated for three
> consecutive batches becomes a rule or is retired.

> **A table you may delete.** A table whose `| **Field** |` row reads `none — <reason>`, or whose question one line of the gate checklist answers, may be deleted, its field row kept: `stations/core-runbook.md` §*A minimal increment packet* is a one-function change written that way.

| Field | Value |
|---|---|
| Batch | `2026-10-20-batch-01` |
| Increment | `002` |
| Lane (if the batch forked) | none — one lane |
| Requirement(s) | `HLR-2202` (its AT), `HLR-2203`, `HLR-2204` / `LLR-2203.1`, `LLR-2204.1` |
| Acceptance | `AT-2202`, `AT-2203`, `AT-2204` · white-box `TC-2203`, `TC-2204` · unit: the strip's window choice, `ago`, the counts row's drop rule (Layer 0, `TC-2204`) |
| Agent | `software-dev` (the orchestrator, self-implemented; drafted in a scratch worktree, ported here) |
| Date | `2026-10-20` |

---

## 1 · What changed

The open board is named and the boards are one key away. `Board.label` (runtime only) carries the open board's name and colour when more than one board is active; `views.header(..., chip=)` opens the head row with it (`board_chip`: the name cut to 24 cells, escaped, bold `#0d1117` on its colour) through `_head(board, …)` at the fifteen main-screen head rows, and `render_setup` prefixes it to its first row, cut to the width; the narrow fallback of `header` now escapes its plain text (security S-3). The presentation's head rows and the `/` bar take no chip. `app.BoardsHome` is the round's variant C home — a title row, a two-column grid of board cards in a scroll, the key row — its card bodies pure renders in `views` (`board_summary`, `ago`, `due_strip`, `home_card`, `home_missing`, `home_title`, `home_keys`), each board read once with `peek_board`; a missing file reads `file missing` and does not open. It shows at start with more than one active board (before the opened board's own modals) and on `B`, now a universal key of the seat (`B Boards` in every key bar, the `?` help, the palette, the README's Keys table). `check_action` releases `boards` under any pushed screen and blocks every action of the seat but `quit` while the home is anywhere on the stack; `enter` closes the home and then switches.

## 2 · Files modified

| File | Kind | Traces to | Change |
|---|---|---|---|
| `taskboard/models.py` | source | LLR-2203.1 | `Board.label` |
| `taskboard/views.py` | source | LLR-2203.1, LLR-2204.1 | `board_chip`, `header(..., chip=)` (and its escaped fallback), `_head` at 15 head rows, the setup row; the home's renders; `board_hex`; `ago` reads an aware time; `home_missing(..., why)` |
| `taskboard/app.py` | source | LLR-2203.1, LLR-2204.1 | `BoardsHome`, `BoardCard`, `SEAT_ACTIONS`, `check_action`, the launch push, `_label_board`, `action_boards`; the label at a switch |
| `taskboard/keymap.py` | source | LLR-2204.1 | `B` → `boards`, universal, primary, after `q` |
| `tests/test_boards_home.py` | test | HLR-2202, HLR-2203, HLR-2204, LLR-2203.1, LLR-2204.1 | new: TC-2203, TC-2204, AT-2202, AT-2203, AT-2204 |
| `tests/test_colour_budget_app.py` | test | LLR-2204.1 | `KEYBAR_BASE`'s two literal bars updated law-driven (census below) |
| `README.md` | doc | HLR-2204 | the Keys table's `B` row (the seat's README law) |
| `.dev-flow/2026-10-20-batch-01/evidence/frames-base.json` | fixture | LLR-2203.1 | TC-2203's oracle: every view's frame at `base_ref` (`frames_base.py`) |

| Count | Value |
|---|---|
| **SOURCE files** | **4 / 4** ⚠ — the chip's attribute, its renders, the screen and the key cannot ship apart: a key with no screen, or a home with no key, breaks the seat's law (planned so at the PDR) |
| Test files | 2 (uncapped) |

## 3 · How to test

`python -m pytest -q -p no:cacheprovider tests/test_boards_home.py tests/test_colour_budget_app.py tests/test_keymap.py tests/test_readme.py`; the battery: `python .dev-flow/2026-10-20-batch-01/evidence/mutate-002.py`.

## 4 · Test results

| Layer | Nodes | Result |
|---|---|---|
| 0, A and B | `tests/test_boards_home.py` — TC-2203 (12 nodes), TC-2204 (20), AT-2202, AT-2203, AT-2204 (4) — 38 nodes | in the full suite (`suite-002.txt`) |
| full suite | `python -m pytest -q -p no:cacheprovider -rs --color=no` on the working tree (`e522eac` + this increment) | 0 failed, 2893 passed (`suite-002.txt`; the ledger 2855 + 38 = 2893) |

| Field | Value |
|---|---|
| **RED counterfactual** | the test files and the base-frame oracle copied into a clean worktree at `base_ref` `783397e`, the main checkout's `taskboard/boards.py` moved aside for the run and restored by digest: `tests/test_boards_home.py` 28 failed, 10 errors (no `open_app`, no `board_chip`, no home), 1 passed — `test_TC_2203_no_label_is_the_base_frame`, a regression pin true on base by construction; `test_TC_203_…` (the law-driven bars) RED · `.dev-flow/2026-10-20-batch-01/evidence/red-002.txt` |
| **Mutation verdicts** | 21 mutants over 27 arms, one node per arm, each restore proven by digest: a chip without a label · KILLED ×2; the name unescaped · KILLED ×2; the narrow fallback unescaped · KILLED; the 24-cell cut dropped · KILLED; the chip counted twice · KILLED; a head row without the chip · KILLED ×2; `week` past Sunday · KILLED; a late task as next · KILLED; the round's drop rule replaced by "fits" · KILLED ×2 (TC's inner-53 arm and the 118×30 capture); `boards` not released under a modal · KILLED (TC-2204's `check_action` arm — AT-2204's `B`-over-the-presentation arm does NOT see it: Textual itself does not run a non-priority app binding under a `ModalScreen`, so that AT arm is a regression pin, and it was taken out of the battery); a main key acting behind the home · KILLED; the home seeding a missing board · KILLED; `enter` switching before closing the home · KILLED; the launch push with one board · KILLED (AT-2201); the chip with one board · KILLED; `B` out of the seat · KILLED ×2; a missing card opened · KILLED; the code review's folds: an aware time crashing `ago` · KILLED; the setup chip parsing emoji · KILLED; `↓` moving by one card · KILLED; an unreadable board drawn as empty · KILLED · arms that stayed GREEN: none · `.dev-flow/2026-10-20-batch-01/evidence/mutation-002.txt` (harness `evidence/mutate-002.py`) |
| **Instrument RED-proof** | 2 instruments: `evidence/mutate-002.py` (anchors asserted once, each edit asserted applied; increment 001's run of its twin saw a survivor); `evidence/frames_base.py` — run on `base_ref` (`783397e`) its 40 frames equal the branch's with no label (the qa-reviewer re-ran it independently: 40/40) |
| **Emitted-form assertion** | 3 artifacts: the home's screen as Textual exports it (`export_screenshot()` SVG rows compared with the round's capture rows), the board view's first row as `#board` holds it, the views' frames as `render_view` returns them (`Text.plain` and row 0's spans) |
| **Reverse census** | 5 probes: B1 `grep -rln "header(\|key_bar_plain\|render_key_bar\|fit_bar\|bar_keys\|KEYMAP\|check_action\|global_keys\|palette_commands" tests/` → the files the PLAN's B1 row lists — every one green in `suite-002.txt` but `test_colour_budget_app.py`, whose `KEYBAR_BASE` holds two literal bars: law-driven, old → new `? Map  ; More  q Quit  1 Lanes  2  3 …` → `? Map  ; More  q Quit  B  1  2  3 …` (gantt, 80, primary: `B`'s word and `Lanes` go, every key kept) and `…  ↓  ↑  ←  →` → `…  ↓  ↑ +2` (gantt, 118, more: every word was already gone, so the last two keys go and are counted) — the new values fitted BY HAND from the seat's literal strings (`evidence/keybar-law.py` → `keybar-law.txt`), never read from the code; `test_keymap.py`'s README and dead-action laws satisfied by the README row and `action_boards` · B2 no file moved · B3 the shipped frame oracles render no chip without a label (`frames-base.json` equality, TC-2203) · B4 the home reads every board's file (`peek_board`, never writing) · A3 the interface rows amended at ARQ — 0 foreign hits. **What `B Boards` costs (PDR PC-1, ux N1):** per view, layer and width the words (and keys) the bar no longer shows — `evidence/keybar-words.txt` (`bar_words.py` over `783397e` and this tree): at 160 primary `e Edit` and `d Del` (or `a Add`), at 118 primary `6 Chains` and/or `7 Flow`, at 80 primary `1 Lanes`; the more layer loses one key at 80 (`[`, `]` or `!`, counted `+N`) and at 118 gantt `←` `→`, kanban `/` |
| **Correction population** | 2 shipped literals, both in `KEYBAR_BASE` (above) — the only assertions the seat's change reaches |

### Evidence files

| Evidence artifact | Path — under `artifact_homes.evidence` | SHA-256 |
|---|---|---|
| suite-002.txt | .dev-flow/2026-10-20-batch-01/evidence/suite-002.txt | fff50abad7a3885ca4e4b46fe85f5fa38b756f474604a457142dbdca9ac3ca9f |
| red-002.txt | .dev-flow/2026-10-20-batch-01/evidence/red-002.txt | fbe4c292282a51056cbc8601651bcd660ce2846a4ef3c1388e36dad97342469c |
| mutation-002.txt | .dev-flow/2026-10-20-batch-01/evidence/mutation-002.txt | 37a50794be580546cabae8306a352524e4611e5c74f9148a4084730f7b834abe |
| mutate-002.py | .dev-flow/2026-10-20-batch-01/evidence/mutate-002.py | c5ba52c2373a85cb25739fe065ca228f14d264ddeca6ebcbb4c5c5804ac9e2f1 |
| keybar-law.py | .dev-flow/2026-10-20-batch-01/evidence/keybar-law.py | 6ff9285a17f49b6bc3e3022b26b0738e2659fbff4467b73c6407bdda1869550b |
| keybar-law.txt | .dev-flow/2026-10-20-batch-01/evidence/keybar-law.txt | ea41e5ac17bfc697858c4dc4994107d71f8a044b1de300cf1b493f359782c4e1 |
| keybar-words.txt | .dev-flow/2026-10-20-batch-01/evidence/keybar-words.txt | 2937aef6fadf6e512f36532aa8268a45b19af2fd0bfa82874949eb5b7e812f72 |
| bar_words.py | .dev-flow/2026-10-20-batch-01/evidence/bar_words.py | 487e97b27079814690bdeb315e9f83af899b9ca23cf12504239c300bcdc11d34 |
| frames-base.json | .dev-flow/2026-10-20-batch-01/evidence/frames-base.json | e0fd8e96d277d404f228d5bf3d3d6dc8e9d373a0cf288b18763afc84f25bd752 |
| frames_base.py | .dev-flow/2026-10-20-batch-01/evidence/frames_base.py | 19d90ccb20fed6db3211479e4abb5e1795f83adbb4557e64896ec95a317b867a |
| inc002.diff | .dev-flow/2026-10-20-batch-01/evidence/inc002.diff | b1efdab2126cbed66cbb5881929651c875255019341fb99d79ba971fb7295eaa |

| Field | Value |
|---|---|
| **Evidence files** | 11 artifacts, each at the declared home with the digest of its stored bytes |

## 4b · Independent review

| Field | Value |
|---|---|
| **Independent review** | `code-reviewer` — spawned as a generic agent with agents/code-reviewer.md · PASS-WITH-NOTES, 0 HIGH open: round 1 (`inc002.diff`) BLOCK-UNTIL F1 — HIGH, `ago` raised `TypeError` on a hand-edited `last_opened` with an offset and the home crashed the start; F2 MEDIUM (the setup chip parsed emoji shortcodes), F3 MEDIUM (`↑↓` ±2 untested), F4–F6 LOW — all folded; round 2 (`inc002b.diff`): F1 fixed and re-read, its arm killed, 62 targeted tests pass; notes: the registry's own time validator hardened in increment 003 (owed), the strip below 40 columns accepted, `enter` on an unreadable card opens it through the board loader's quarantine (as at start — recorded) |

## 5 · Risks

The home's equality with the round's captures depends on Textual's grid and border rendering at the pinned version (AT-2204 fails loudly if it drifts). `B` costs words in every key bar (`keybar-words.txt`).

## 6 · Pending items / spec deviations

The registry's time validator rejects an offset from increment 003 on (code review F1, owed). The census wrap: the home's four `update(...)` calls pass `Text.assemble(<views render>)` so the markup census (`tests/test_markup_census.py`) reads them as `Text` — the renders build plain-piece `Text` (TC-2204's payload arms).

## 7 · Suggested next task

Increment 003 — the board forms.

## Increment gate checklist

| # | Item | ✓/⚠/✗ | Evidence |
|---|---|---|---|
| 1 | SOURCE budget | ⚠ | §2: 4 source files, the reason declared |
| 2 | Tests in this increment | ✓ | `tests/test_boards_home.py` |
| 3 | Layer 0 where it applies | ✓ | the strip, `ago`, the drop rule |
| 4 | RED counterfactual | ✓ | §4, `red-002.txt` |
| 5 | Reverse census | ✓ | §4: 5 probes, 2 law-driven literals |
| 6 | `code-reviewer` passed | ✓ | §4b |
| 7 | No file from another lane | ✓ | one lane |
| 8 | Frozen interfaces untouched | ✓ | none frozen |
| 9 | Coverage verified on disk | ✓ | `suite-002.txt` |
| 10 | Load-bearing emptiness | ✓ | the census's greps quoted |
| 11 | Mutation verdicts | ✓ | §4: 27/27 KILLED |
| 12 | Instrument RED-proof | ✓ | §4 |
| 13 | Correction population | ✓ | §4: 2 literals |
| 14 | Emitted-form assertion | ✓ | §4 |
| 15 | Independent review | ✓ | §4b |
| 16 | Evidence files | ✓ | §4: the digests |

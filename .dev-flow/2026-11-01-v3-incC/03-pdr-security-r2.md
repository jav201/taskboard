VERDICT: PASS-WITH-NOTES

# Security Review, round 2 — Inc C, multicolour notes (PDR re-check)

> security-reviewer, 2026-11-01. Read-only. This round re-checks SEC-1, SEC-2, SEC-3, SEC-4, SEC-5, SEC-6 and
> SEC-9 against the Round 1 rulings and their addendum, and reviews one new element: ARCH-1's
> `_unshadow_alt_digits`.
> Inputs: graph-interfaces, graph-proto-V, graph-proto-M1 and graph-proto-M2 (all at 01:2x), 01-requirements.md,
> 03-pdr-rulings.md, and the Textual 8.2.8 source.
> This file lists only new or still-open findings: 0 HIGH, 1 MEDIUM, 1 LOW. Every mitigation is `planned`.

## Round 1 items: re-check

| Id | Designed fix | Re-check | State |
|---|---|---|---|
| SEC-1 | V scan step 1 keeps the next match of each kind and searches again only when that match starts before `pos`. A kind whose search returned `None` is never searched again. Step 3 uses `str.find` bounded by the next `::`. `ink_highlights` uses identity offsets on ASCII lines and one prefix table otherwise. New LLR-4201.10 and LLR-4204.7. | **Closed.** I ran the revised algorithm on the round-1 worst cases. At 100k chars: `"!!" + "::b::x::"*n` took 11 ms (918 ms before), `"==a=="*n` 5 ms, `"::b:: == ::"*n` 9 ms, `"::b:: !! ::"*n` 9 ms. Going from 10k to 100k chars multiplies the time by 6.7–10.7, so the scan is linear. Thresholds: ≤ 250 ms, and t(100k)/t(10k) ≤ 20 against a quadratic ≈ 100. Optional: add `"!!" + "::b::x::"*n` to TC-4213. It was the measured worst case before the fix (566 ms at 80k chars). | design `approved`, build `planned` |
| SEC-2 | `action_pen` step (4) compares the visible text before and after the insert and shows N4 when they differ. LLR-4203.17; TC-4252 covers `b:: x`, `C::b` and `note y::`. | **Closed.** I also checked these cases: a lone `:` before or after the cursor, a cursor at a span's start or end (including a span ended by the next opener), and legacy markers around the cursor. The cursor-inside refusal (step 2) together with the visible check leaves no input where the pair changes another span's tone while the visible text stays the same. `action_pen_enter` and the ARCH-10 ` ::` insert in `_lift_pen` do not need the check: the text after the cursor is the pen span's own rest, or the line end, a `\n`, or an opener (TC-4258 pins the opener case). | design `approved` |
| SEC-3 | The `_build_highlight_map` override catches any exception and falls back to `super()`. LLR-4204.8; TC-4251 covers a raising `colour_spans` and a deleted `_line_cache`. The pyproject pin goes to the backlog. | **Closed** for build-time failures. **Residual** at paint time: a change to the `_render_line` tuple shape is not covered, and the design says so (see SEC-R2-2). | design `approved`, residual open (LOW) |
| SEC-4 | `_pen_at` is written by `action_pen` and `action_pen_enter`, refreshed by `_pen_follow`, and set to `None` on every lift or pen-off. The delete runs only while `_pen_at` still points at an empty span of the pen's code. TC-4257 shows an older empty span is not touched. | **Closed.** Because of SEC-2, an empty pen span always parses as the pair that was inserted. Deleting it gives back the pre-insert line byte-for-byte, so I drop my round-1 request for a visible-text check on the delete. | design `approved` |
| SEC-5 | `_apply_colour` checks again at pick time: the row must exist and equal `line_at_open`, else it shows N5 and does nothing. `recolour` is never called on a changed line. TC-4288 covers a changed row and a deleted row. | **Closed.** `recolour` can still raise, but only if `colour_target` and `recolour` disagree, and the ARCH-4 target rules keep every target inside one span or one gap. I accept this. | design `approved` |
| SEC-6 | Offsets use `encode("utf-8", "surrogatepass")`. The override leaves the map empty when the document holds a lone surrogate. LLR-4204.9 is amended to "opens and accepts typing without ink" (R1-1). | **Closed.** At base, `_render_line` encodes a line only when `_highlights` is non-empty, and an empty map is falsy, so Textual's strict encode never runs. One check of my own: `alt+s` with a lone surrogate saves safely, because `_serialized` uses `json.dumps` with its default `ensure_ascii=True`. | design `approved` |
| SEC-9 | TC-4209 asserts that every emitted tone ∈ {mut, soon, over, green, orange, blue, violet}. | **Closed.** The tone set is what `hl-<tone>` is built from. | design `approved` |
| SEC-7, SEC-8 | Ruled as covered by ARCH-1/2 (SEC-7) and sent to the backlog (SEC-8). | Not re-opened. | — |

## New and still-open findings

### SEC-R2-1 [MEDIUM] — `_unshadow_alt_digits` changes a private Textual global at import time with no guard

- **What:** at import, `taskboard/modals.py` runs `textual._ansi_sequences.ANSI_SEQUENCES_KEYS.pop(k, None)`
  for `"\x1b0"`..`"\x1b6"`.
  - **Scope.** The change is process-wide, lives only in memory, and is never written to disk. It
    widens no input path: `ESC <digit>` already turned into a key, and now it is `Key("alt+n", "n")`
    instead of `∞`/`º`.
  - **Outside `TaskModal`.** No binding is named `alt+0`..`alt+6`. The one handler that reads
    `event.character` is the picker filter at `modals.py:1789`; it now appends `5` where it used to
    append `∞`. That is harmless.
  - **Failure mode.** The table's declared type is `Mapping[...]` (`_ansi_sequences.py:19`), and in
    8.2.8 the object happens to be a plain `dict`. If a Textual release makes it immutable (for example
    a `MappingProxyType`, or a frozen table built at parse time), `.pop` raises `AttributeError` or
    `TypeError` during `import taskboard.modals`. The app then cannot start, which is worse than
    SEC-3, where only the editor failed. `pyproject.toml` still declares `textual` without a version
    (pin backlogged), so a fresh install can pull such a release.
  - **Silent removal.** The blind `pop` would also remove a meaning a later Textual version might give
    those keys.
- **Where:** graph-proto-M1, node `_unshadow_alt_digits` and the entity `[Outside: textual ANSI_SEQUENCES_KEYS]`.
- **Evidence:**
  - `_ansi_sequences.py:19` annotates the table as `Mapping`, and `_xterm_parser.py:431` reads it only
    with `.get`. Nothing in Textual's contract promises that `.pop` exists.
  - Concrete input for the test: `monkeypatch.setattr(textual._ansi_sequences, "ANSI_SEQUENCES_KEYS",
    types.MappingProxyType(dict(...)))`, then call `_unshadow_alt_digits()`. As designed, this raises
    `AttributeError`.
- **Smallest fix:** keep the node, and guard it the way SEC-3 guards the override.
  1. Pop a key only while it still holds its 8.2.8 glyph: `if TABLE.get(k) == GLYPH[k]`, where
     `GLYPH = {"\x1b0": "º", "\x1b1": "¡", "\x1b2": "™", "\x1b3": "£", "\x1b4": "¢", "\x1b5": "∞", "\x1b6": "§"}`.
  2. Wrap the loop in `try/except Exception: pass`. The fallback is base behaviour: the pens do not
     fire under the legacy encoding, and the app still starts.
  3. Add a TC-4249 arm: with an immutable table, importing and calling raise nothing and change nothing.
     NC: the unguarded pop raises, RED.
- **State:** `planned`.

### SEC-R2-2 [LOW] — a paint-time failure after a Textual upgrade is still not fail-safe (residual of SEC-3)

- **What:** the SEC-3 guard covers `_build_highlight_map`, but not `_render_line`. Textual's
  `_render_line` unpacks our 3-tuples, so if a later version expects another shape, every paint of the
  notes field raises and the app crashes with the unsaved edit. The design states this gap
  (graph-proto-M1, `InkArea._build_highlight_map` func). Its cover is a dev-only guard test plus a
  backlogged pin, so nothing protects a user's fresh install.
- **Where:** `InkArea` (graph-proto-M1). The same version exposure as SEC-R2-1.
- **Smallest fix:** one runtime version gate that covers both private-API dependents and leaves
  `pyproject.toml` as ruled.
  - Compute `INK_OK = importlib.metadata.version("textual").startswith("8.2.")` once in modals.py.
  - When it is False, `InkArea._build_highlight_map` defers to `super()` (no ink), and
    `_unshadow_alt_digits` returns at once.
  - Either way the app runs as at base on any unverified Textual version. Following "prefer removing
    over guarding", this turns the two features off where they are unverified instead of guarding each
    private name.
  - Test: monkeypatch the version to `"9.0.0"`. The editor opens with no ink, and `"\x1b5"` parses as base.
- **State:** `planned`.

## Verdict (role tokens)

- [x] **OK to ship (design stage)** with notes. No HIGH. All 7 round-1 items re-checked here are closed
  in the design: SEC-1, SEC-2, SEC-3 (build-time part), SEC-4, SEC-5, SEC-6 and SEC-9.
  SEC-R2-1 should be folded into `_unshadow_alt_digits` before E4. It is small, and it is the only way
  this increment can stop the app from starting at all. I re-verify both findings at the increment
  gate, where they must be `executed`.
- [ ] `BLOCK-UNTIL:` none. [ ] Block: none.

This clearance is not the operator's authorisation for anything.

## Evidence checklist

- ✓ Each finding has what · where · evidence (a concrete input) · fix: SEC-R2-1 and SEC-R2-2.
- ✓ Each finding has a severity: 0 HIGH, 1 MEDIUM, 1 LOW.
- ✓ No secret values appear here.
- ✓ The verdict is explicit. There are no HIGH findings.
- ✓ New tool or integration: `n/a`. No dependency is added. The private Textual global is covered in SEC-R2-1.

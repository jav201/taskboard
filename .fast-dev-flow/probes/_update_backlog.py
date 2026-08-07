"""Reconcile .dev-flow/BACKLOG.md for 2026-08-06-fastflow-03, preserving CRLF."""
from pathlib import Path

BL = Path(__file__).resolve().parents[2] / ".dev-flow" / "BACKLOG.md"

OLD_HEADER = ("**Base ref:** `bd935ff` (origin/main) · **Last refresh:** 2026-08-03")
NEW_HEADER = ("**Base ref:** `3b0f011` (local HEAD; `origin/main` = `6b7c4c3`) · "
              "**Last refresh:** 2026-08-06")

OLD_STATUS = "**Status:** 707 tests green."
NEW_STATUS = "**Status:** 725 tests green."

OLD_ITEM = "- **FIX AND VERIFY THE ROW COST MODEL, ALONE, WITH NO VISUAL CHANGE.**"
NEW_ITEM = ("- **DONE** (2026-08-06, `/fast-dev-flow`) · **FIX AND VERIFY THE ROW COST MODEL,"
            " ALONE, WITH NO VISUAL CHANGE.**")

NEW_SECTION = '''
## From 2026-08-06-fastflow-03 — the row cost model (SHIPPED, no visual change)

`/fast-dev-flow`, one increment, three files. **No behaviour change**: the `taskboard/views.py`
diff is two docstrings, proven prose-only by comparing the AST with every docstring stripped.
707 → 725 tests. Spec + probes: `.fast-dev-flow/spec.md`, `.fast-dev-flow/probes/`.

### What it settled

- **THE COST MODEL HAD NO DEFECT.** `swimlane_plan`'s `h - 2 - (2 if active else 0)` and
  `lead_band`'s `prof + 2` are the two halves of ONE correct identity, verified **124/124**
  in regime over 160 renders (5 boards × 4 widths × 8 heights, frozen clock, synthetic boards):

      room = h - 2 - 2*[active]      need = prof + Σ(wrows + min(titles,o)) + n_rest
      BODY == need + 2*[active]      2 + BODY + ABSENCE == h

  **The two `2`s are different**: `h - 2` is the panel's own chrome (header + axis, the close
  being frameless); `- 2*[active]` is the lead band's head and tail. Batch-03's headline claim
  ("the cost model undercharges `prof`") is **FALSE by execution**, and so is its inverse.
- **Pinned** by `tests/test_row_cost.py` (18 tests, laws L1–L9), and the model is now written
  down in the docstrings of `allocate` and `swimlane_plan` **with its regime**.
- **Every law is answerable to a mutation that reddens it** — 5 source mutations applied to
  `taskboard/views.py` for real (not monkeypatched), each killed, `views.py` restored
  byte-identical: `room = h-2` (6 failed) · `room = h-6` (2) · `lead_band ±1 row` (7 / 5) ·
  rung four dropping its `- 1` (1). Runner kept at `.fast-dev-flow/probes/_mutate_check.py`.

### Findings

- **A claim this repo shipped was FALSE, and is corrected.** `tests/test_vertical_fill.py:91`
  said *"the lanes never pad at all — their allocator spends the whole height it is given"*.
  It holds **only while a project is active**. On an all-resting board nothing draws the bench,
  `prof` is billed for it anyway, and the view pads **exactly `h - 3 - n_rest`** rows (verified
  across 5 lane counts × 4 widths × 8 heights). The operator reproduced this independently and
  ruled: **document the regime, do not change the behaviour.** Done.
- **`prof` is billed and never drawn when no lane is active.** Dead budget, harmless in effect
  (nothing else could spend it) but it makes the model's A=0 branch vacuous. **Deliberately left
  alone** — fixing it is a behaviour change, out of a "no visual change" batch. Carried below.
- **A vacuity trap that hid 2 of 5 mutations, and it was live in the first draft of this batch's
  own test.** Selecting the sample on `feasible = charge <= room` — a quantity computed from the
  code under test — makes M1 (call site never pays for the lead band) and M4 (no absence row
  reserved) pass **vacuously**; M1 leaves the sample EMPTY. The off-regime exclusion must be
  **static** (named fixture + height), and feasibility must be **asserted**, never selected on.
  Measured both ways. **Candidate control** for `dev-flow-lessons`: *an exclusion predicate
  computed from the code under test is a vacuous check wearing a filter's clothes.*
- **The bench share was already shipped behaviour, not change-induced.** On HEAD today, a calm
  board's bench is 86.7 % at h=30, **93.3 % at h=60, 95.0 % at h=80**; by board shape the max is
  `calm` 95.0 % · `typical` 73.8 % · `huge` 44.4 % · `busy` 41.2 %. The driver is **how many
  active lanes exist**, not `wrows`. Fed into the O-3 re-presentation above; the operator kept
  the ruling. The **post-change** share remains `NOT MEASURED` — it belongs to the redesign batch.
- **`fa821ae` was unpushed** when this batch opened, though the handoff asserted
  `HEAD == origin/main == fa821ae`. Resolved by the operator mid-batch: amended and pushed as
  `6b7c4c3` (which also made `_prototypes/` render a **synthetic** board on a frozen clock
  instead of carrying real project names and task titles into committed files), then `3b0f011`.
  **Standing practice, now explicit: no artifact may carry the operator's board data.** This
  batch's probes and fixtures are synthetic and in-memory throughout.

### Carried forward from this batch

- **`prof` is billed for a bench nothing draws when no lane is active.** A behaviour change, so
  out of scope here. Whoever opens it must keep `tests/test_row_cost.py::test_L8...` honest —
  it currently pins the pad as `h - 3 - n_rest`, which is what would change.
- **`lead_band`, `stack_block`, `project_wave` still have no direct test guards** beyond the
  arity/accounting ones this batch added. `project_wave` remains entirely unguarded.
- **The redesign batch is unblocked**: with the model fixed and pinned, "the project row states
  its demand; the curve moves to a disclosure row" becomes row substitution against a known
  budget. O-1, O-2, O-3, O-4 are all ruled; nothing in this batch reopened them.
'''


def main():
    raw = BL.read_bytes()
    src = raw.decode("utf-8")
    eol = "\r\n" if b"\r\n" in raw else "\n"
    out = src
    for old, new in ((OLD_HEADER, NEW_HEADER), (OLD_STATUS, NEW_STATUS),
                     (OLD_ITEM, NEW_ITEM)):
        assert out.count(old) == 1, f"anchor count {out.count(old)}: {old[:60]!r}"
        out = out.replace(old, new)
    if not out.endswith(eol):
        out += eol
    out += NEW_SECTION.replace("\n", eol)
    BL.write_bytes(out.encode("utf-8"))
    d = BL.read_bytes()
    print(f"bare-LF introduced: {d.count(chr(10).encode()) - d.count(b'@@'.replace(b'@@', b'\r\n'))}")
    print(f"CRLF: {d.count(b'\r\n')}  bare-LF: {d.count(b'\n') - d.count(b'\r\n')}")


main()

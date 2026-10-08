"""One-shot P1 fill for batch-06's 01-requirements.md."""
from pathlib import Path

p = Path(".dev-flow/2026-10-07-batch-06/01-requirements.md")
s = p.read_text(encoding="utf-8")

NEW_HLR = '''### HLR-1201 — The chain map draws every open task; chains are created on the map
- **Traceability:** US-1201
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** The chain map shall draw every OPEN task of a visible project: linked tasks as today (chains, the meta rows, the critical chain, the per-band `dates` switch) and UNLINKED open tasks as one-row `○` tiles at depth 0 inside their project's band — the legend's existing "open chain head" mark — each selectable and reachable by the arrows; `L` on ANY tile opens the shipped LinkPicker so a chain is created where it is seen (the picked task gains its incoming link and its tile joins that chain); `x` unlinks the selected task's first incoming link as today, leaving it an `○` tile — visible and re-linkable, never vanished; the band heads keep their counts (`‹n› linked · ‹m› open not linked` — the `○` tiles ARE those m tasks); the inert `no links` row survives only for a project with no open work at all; the C-2b oracle frames at 118×30 and 80×24 AMEND under LED-2026-10-07-batch-06.1 (the amended frames are the new renderer's bytes on the same frozen fixture, stored at this batch's evidence home; the sealed batch-02 frames stay history).
- **Rationale (informative):** the operator's report 2026-07.. no — 2026-10-07: a board with zero links shows projects with no tasks and no way to create a chain ("es imposible crear cadenas"); the picker flow existed only off-view (kanban/gantt `L`), invisible from the map.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_chainmap.py tests/test_chainmap_app.py -q`
- **Numeric pass threshold:** `0 failures`; TC-801/TC-802 byte-exact against the AMENDED frames at both sizes; the new arms: an unlinked task paints as an `○` tile, is selectable, `L` links it ON the map (the picker opens, the link lands, the tile joins the chain); `x` leaves an `○` tile; the `no links` row only for projects with no open work.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** on a board with no links, the chain map shows every open task as an `○` tile; selecting one and pressing `L` creates the first link right there; the web grows where it is looked at.
  - **Shipped surface:** the chain map (tiles, the `L`/`x` seats, the band heads), the amended oracle frames.
  - **Acceptance test(s):** AT-1201.
  - **Boundary catalog (QC-3):** ☑ empty (a project with no open work — the inert row stands) ☑ boundary (the first link of a board; a task that becomes unlinked) ☑ error — none new.
  - **Negative control:** `x` on a never-linked task refuses as today (nothing to remove).

### HLR-1202 — The kanban window shows its hidden sides
- **Traceability:** US-1202
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** When the kanban's phase window hides open-phase columns (the shipped `fits`/`start` law), the phase-head row shall mark the hidden sides — `◂` at the left edge when any phase is hidden left, `▸ N` (N exact) at the right edge when any are hidden right; when nothing is hidden the head row carries no markers; the `?` kanban help gains the window bullet: more phases than fit — the window follows the selection (`j`/`k` into a later column), `◂`/`▸` mark the hidden sides.
- **Rationale (informative):** the operator's report 2026-10-07: "prioriza las primeras columnas... incluso reescalando" — the window follows the selection and nothing on screen says the rest exists.
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_kanban_window.py tests/test_kanban_readable.py -q` (the increment's file + the readable census)
- **Numeric pass threshold:** `0 failures`; at a width fitting 2 of 4 phases the head row carries `◂` and `▸ 2` exact; at a width fitting all, none; the help bullet present.
- **Priority:** medium
- **Acceptance (black-box):**
  - **Observable outcome:** the user always sees that more phases exist and which side they are on, before moving the selection.
  - **Shipped surface:** the kanban's phase-head row, the `?` help.
  - **Acceptance test(s):** AT-1202.
  - **Boundary catalog (QC-3):** ☑ boundary (exactly-fits vs one-hidden; the left-edge marker when the selection sits late).
  - **Negative control:** an all-fits width renders zero markers.'''

OLD_HLR_HEAD = "### HLR-001"
i = s.index(OLD_HLR_HEAD)
j = s.index("---\n\n## 4. Low-level requirements (LLR)")
s = s[:i] + NEW_HLR + "\n\n" + s[j:]

NEW_LLR = '''### LLR-1201.1 — the renderer draws the `○` tiles and the amended oracle
- **Traceability:** HLR-1201
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** `views.render_chainmap`'s plan shall admit every open unlinked task as a depth-0 one-row `○` tile in its project's band (fold-aware: the tiles take part in the fold and the `+N more ↓` cap like any row, and only painted tiles reach the `line_map`); the band heads' counts stay as shipped; the `no links` row renders only when the project has no open work; the amended C-2b frames are this renderer's bytes on the frozen kg fixture (Data Warehouse `together`, the TC-801 board) at 118×30 and 80×24, stored at `.dev-flow/2026-10-07-batch-06/evidence/frames/`, and `tests/test_chainmap.py`'s frame path moves there citing the LED.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_chainmap.py -q`
- **Numeric pass threshold:** `0 failures`; TC-801/TC-802 byte-exact vs the AMENDED frames; the fold arms (TC-810, the cap) stay green with the tiles present.
- **Negative control:** a width where a band's `○` tiles do not fit still drops/caps the band whole (the dangling-head law).
- **Boundary catalog:** ☑ empty (no-open-work project) ☑ boundary (exactly-fits vs one-over rows).

### LLR-1201.2 — the app seats: L creates a link on the map, x leaves an `○` tile
- **Traceability:** HLR-1201
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** on the chain map, `L` with a tile selected (linked or `○`) shall open the shipped LinkPicker and apply the pick as the task's incoming link (the tile joins that chain on re-render); `x` removes the first incoming link as shipped and the task REMAINS as an `○` tile; the arrows/`j`/`k` reach the `○` tiles in nav order (band order, then the chain columns — the `○` tiles at their depth-0 column); the selection strip names an `○` selection's waits-on/unblocks truthfully (waits on nothing yet · unblocks nothing).
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_chainmap_app.py -q`
- **Numeric pass threshold:** `0 failures`; the create-on-map arm (pick a predecessor → `depends_on` lands → the tile renders inside the chain); the unlink-leaves-tile arm; the nav arm reaches an `○` tile.
- **Negative control:** `x` on a never-linked task — the shipped refusal toast, unchanged.
- **Boundary catalog:** none beyond LLR-1201.1's.

### LLR-1202.1 — the window markers and the help bullet
- **Traceability:** HLR-1202
- **Ledger:** LED-2026-10-07-batch-06.1
- **Statement:** `views`' kanban head row shall render `◂` before the first visible phase title when `start > 0`, and `▸ N` (N = `n_open − (start + fits)`, exact) after the last visible one when positive; no markers when the window shows everything; `views.help_usage("kanban")` carries the window bullet verbatim: "more phases than fit — the window follows the selection (j/k into a later column) · ◂ ▸ mark the hidden sides".
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_kanban_window.py -q`
- **Numeric pass threshold:** `0 failures`; the 4-phase/2-fit fixture shows `◂` and `▸ 2` at 80 cells and no markers at a full width; the help bullet string present.
- **Negative control:** the all-fits width renders zero markers.
- **Boundary catalog:** ☑ boundary (exactly-fits; selection late so `start > 0`).'''

OLD_LLR_HEAD = "### LLR-001.1"
k = s.index(OLD_LLR_HEAD)
m = s.index("### Information Flow Contract (IFC) — C-54")
s = s[:k] + NEW_LLR + "\n\n" + s[m:]

OLD_IFC = """- **Part A — flows:** `<one fenced FLOW block per information flow: SOURCE, NODES (each node with exactly one owner, an LLR above — split a node two LLRs own), SINK>`
- **Part B — boundary decomposition:** `<yes — one fenced COMPONENT block per component | no — and why no component of the boundary is addressable on its own>`"""
NEW_IFC = """- **Part A — flows:**

```
FLOW: the dependency web and the kanban window, from the board to the eye
  SOURCE : the board file (tasks, phases, depends_on); the keys (L, x, the arrows); the terminal size
  NODES  :
    - fn    : views.render_chainmap + the _chainmap_* plan (the `○` tiles, the amended C-2b oracle)
      owner : LLR-1201.1
    - fn    : the chain map seats (L links on the map, x leaves the tile, nav reaches the tiles)
      owner : LLR-1201.2
    - fn    : the kanban plan's window markers + help_usage("kanban")
      owner : LLR-1202.1
  SINK   : the chain map canvas (every open task a tile), the kanban's phase-head row, the ? help
```

- **Part B — boundary decomposition:** `no — no new addressable component.`"""
assert OLD_IFC in s
s = s.replace(OLD_IFC, NEW_IFC)

p.write_text(s, encoding="utf-8")
print("batch-06 requirements done")

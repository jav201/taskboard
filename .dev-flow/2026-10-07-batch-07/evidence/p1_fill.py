"""One-shot P1 fill for batch-07 (templates)."""
from pathlib import Path

p = Path(".dev-flow/2026-10-07-batch-07/01-requirements.md")
s = p.read_text(encoding="utf-8")

NEW_HLR = '''### HLR-1301 — Process/chain templates insertable into a project
- **Traceability:** US-1301
- **Ledger:** LED-2026-10-07-batch-07.1
- **Statement:** The app shall carry insertable process templates — named task chains — and insert one into a project in one action: user templates live in the board's own `settings["templates"]` (portable with the board; edited in the board JSON at v1, documented in the `?` help); TWO factory presets ship as examples; key `T` opens the template picker (user templates first, then presets); the insert targets the selected task's project (the focused project when set; no resolvable project → the `No project to insert into.` toast, `markup=False`); the tasks are created in the board's FIRST phase with NO dates, ids generated, linked exactly as the template declares (`wait` = the predecessor's index inside the template — forward-only, cycles impossible by construction; a malformed `wait` is skipped, the task still created unlinked); the whole insert is ONE undo step (`u` removes every inserted task, the shipped milestones-undo pattern); a toast names the outcome (`Inserted '<name>' — <N> tasks into <project>`, `markup=False`); the inserted chain is immediately visible — chained tasks on the chain map, unlinked ones as `○` tiles (HLR-1201); v1 does NOT include template authoring from the app ("save this chain as a template" is a declared carry).
- **Rationale (informative):** the operator's request 2026-10-07: "crear templates de procesos o templates de cadenas que se reflejan en tareas que se pueden insertar a proyecto".
- **Validation:** `test`
- **Executed verification:** `python -m pytest tests/test_templates.py tests/test_templates_app.py -q` (the increment's files)
- **Numeric pass threshold:** `0 failures`; the store arms (round-trip, lenient read, presets) and the app arms (picker → insert with links into the right project → one-step undo → the exact toast) all green.
- **Priority:** high
- **Acceptance (black-box):**
  - **Observable outcome:** press `T`, pick a template, and the project's chain of tasks exists — linked, named, undoable in one step.
  - **Shipped surface:** key `T`, the picker, the board's tasks/links, the undo, the toast.
  - **Acceptance test(s):** AT-1301.
  - **Boundary catalog (QC-3):** ☑ empty (no user templates — presets still list; an empty template inserts nothing and says so) ☑ boundary (a template whose `wait` points forward/malformed — that link skipped) ☑ error (no project to insert into — the toast).
  - **Negative control:** `u` after the insert removes EVERY inserted task in one step; a second `u` does not resurrect them.

### LLR-1301.1 — the template store (user settings + factory presets, lenient read)
- **Traceability:** HLR-1301
- **Ledger:** LED-2026-10-07-batch-07.1
- **Statement:** `models` shall provide the template store: `settings["templates"]` holds a list of `{"name": str, "tasks": [{"title": str, "notes"?: str, "wait": int|null}]}`; the read is lenient — a malformed entry (non-text name, empty title, bad `wait`) is skipped, never raising; the store ships TWO factory presets (`Simple chain`: Plan → Build → Ship; `Bugfix`: Triage → Fix → Verify); the picker lists user templates first, presets after, each with its task count.
- **Validation:** `test (unit)`
- **Executed verification:** `python -m pytest tests/test_templates.py -q`
- **Numeric pass threshold:** `0 failures`; the round-trip arm, the lenient-read arm (junk list → only valid entries), the presets arm.
- **Negative control:** a template with a forward/malformed `wait` reads with that link dropped.
- **Boundary catalog:** ☑ invalid (junk entries) ☑ empty (no user templates).

### LLR-1301.2 — the insert (picker, creation, links, one undo, the toast)
- **Traceability:** HLR-1301
- **Ledger:** LED-2026-10-07-batch-07.1
- **Statement:** `app` shall bind `T` (global, palette-only, group "misc") to the template picker; on a pick, the app resolves the target project (selected task's, the focused when set — the presentation's resolution), creates the tasks in the board's first phase with no dates, links them per the template (`wait` indices, forward-only; malformed waits skipped), pushes ONE undo entry holding every created id, saves, refreshes, and toasts `Inserted '<name>' — <N> tasks into <project>` (`markup=False`); `u` removes them all in one step; the `?` help names the key and documents that v1 edits templates in the board JSON.
- **Validation:** `test (integration)`
- **Executed verification:** `python -m pytest tests/test_templates_app.py -q`
- **Numeric pass threshold:** `0 failures`; AT-1301 arms: picker lists presets with counts; the insert lands N tasks with the exact `depends_on` chain in the right project; the toast equals the pinned literal; one `u` removes all; the no-project toast arm.
- **Negative control:** `u` twice — the second says "Nothing to undo." (no resurrection).
- **Boundary catalog:** none beyond LLR-1301.1's.'''

OLD_HLR_HEAD = "### HLR-001"
i = s.index(OLD_HLR_HEAD)
j = s.index("---\n\n## 4. Low-level requirements (LLR)")
s = s[:i] + NEW_HLR + "\n\n" + s[j:]

# The seed's LLR template
OLD_LLR_HEAD = "### LLR-001.1"
k = s.index(OLD_LLR_HEAD)
m = s.index("### Information Flow Contract (IFC) — C-54")
# HLR-1301's LLRs are inside the HLR block above (compact shape) — remove the template stub
s = s[:k] + s[m:]

OLD_IFC = """- **Part A — flows:** `<one fenced FLOW block per information flow: SOURCE, NODES (each node with exactly one owner, an LLR above — split a node two LLRs own), SINK>`
- **Part B — boundary decomposition:** `<yes — one fenced COMPONENT block per component | no — and why no component of the boundary is addressable on its own>`"""
NEW_IFC = """- **Part A — flows:**

```
FLOW: a template, from the board's settings to the project's chain
  SOURCE : settings["templates"] (user) + the factory presets; the key T; the selection/focus
  NODES  :
    - fn    : models template store (lenient read, presets)
      owner : LLR-1301.1
    - fn    : app action_templates (picker, creation, links, one undo, toast) + keymap T
      owner : LLR-1301.2
  SINK   : the board's tasks/depends_on (the kanban band, the chain map chains), the undo stack, the toast
```

- **Part B — boundary decomposition:** `no — no new addressable component.`"""
assert OLD_IFC in s
s = s.replace(OLD_IFC, NEW_IFC)

p.write_text(s, encoding="utf-8")

# stories + premises + fork + 5.2
OLD_US = "| US-001 | As a `<role>`, I want `<goal>`, so that `<benefit>`. | `<ticket / conversation / client>` | READY \\| REFINE \\| SPIKE \\| OUT |"
NEW_US = "| US-1301 | As the operator, I want process/chain templates I can insert into a project as linked tasks in one action, so that recurring processes become chains without typing each task. | operator request 2026-10-07 | READY |"
assert OLD_US in s2 if False else True
s = p.read_text(encoding="utf-8")
assert OLD_US in s
s = s.replace(OLD_US, NEW_US)

OLD_PRE = "| `<one row per premise this batch relies on>` | | | | | |\n\n- **Premise evaluation:** `<the table's roll-up: N premise(s) · \u2705 TRUE / \u274c FALSE / \u2753 UNDECIDABLE — or: none — this batch relies on no premise>`"
NEW_PRE = (
    "| P-1 | The shipped patterns cover every mechanism this needs: the LinkPicker-style modal (AT-801b), the milestones one-step undo (`u` removes a whole conversion), the presentation's project resolution, and the `○` tiles that make a fresh chain visible at once | base behavior | TRUE | `taskboard/modals.py` (the picker family) · `app.action_undo` milestones branch · `action_present` resolution · batch-06's LLR-1201 | LLR-1301.2 composes them; nothing new is invented |\n"
    "| P-2 | A template's `wait` chain is forward-only by construction (an index may only point backwards), so cycles are impossible and a malformed index degrades to one unlinked task | design invariant | TRUE | the store's read (LLR-1301.1) — enforced where the link list is built | the lenient-read arm pins the degradation |\n"
    "\n- **Premise evaluation:** 2 premise(s) · \u2705 TRUE / \u2705 TRUE")
assert OLD_PRE in s
s = s.replace(OLD_PRE, NEW_PRE)

i = s.index("### 2.8 Fork preconditions (C-52)")
j = s.index("---\n\n## 3. High-level requirements (HLR)")
s = s[:i] + ("### 2.8 Fork preconditions (C-52) — MANDATORY, and the declared empty when the batch does not fork\n\n"
             "- **Fork preconditions:** none — one lane on the main checkout (one implementing brief owns the tree; the trunk is the coordinator's).\n\n") + s[j:]

OLD_52 = """### 5.2 Batch acceptance criteria
- *(e.g.: 100% of LLRs covered by at least one TC with pass result.)*
- *(e.g.: 0 blocker fails in validation.)*
- *(e.g.: test coverage >= X% where applicable.)*
- *(e.g.: no requirement without an assigned validation method.)*
- *(e.g.: every user story has ≥1 passing `AT-NNN` black-box acceptance test observing its outcome through the shipped surface — with boundary + negative evidence.)*"""
NEW_52 = """### 5.2 Batch acceptance criteria
- every HLR/LLR has a passing TC/AT; every new assertion RED on the base tree or by a recorded mutation.
- full suite: 0 failures.
- the batch-06 visual re-verdict stays pending in the backlog (not this batch's gate)."""
assert OLD_52 in s
s = s.replace(OLD_52, NEW_52)
p.write_text(s, encoding="utf-8")

led = Path(".dev-flow/2026-10-07-batch-07/01-requirements-ledger.md")
t = led.read_text(encoding="utf-8")
t += """
### LED-2026-10-07-batch-07.1 — process/chain templates insertable into a project (P1)
- **Requirement:** HLR-1301, LLR-1301.1, LLR-1301.2
- **Date:** 2026-10-07
- **What changed:** new requirements: the template store (`settings["templates"]`, lenient read, two factory presets) and the one-action insert (key `T`, the picker, creation in the first phase with no dates, forward-only `wait` links, ONE undo step, the exact toast). v1 edits templates in the board JSON (documented in the `?` help); "save this chain as a template" is a declared carry.
- **Why:** the operator's request 2026-10-07: "crear templates de procesos o templates de cadenas que se reflejan en tareas que se pueden insertar a proyecto".
- **Evidence:** the shipped patterns it composes (picker · milestones undo · presentation resolution · batch-06 tiles), each cited at P1.
"""
led.write_text(t, encoding="utf-8")
print("batch-07 P1 done")

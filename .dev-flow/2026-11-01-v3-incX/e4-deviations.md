# Inc X — E4 deviations (implementer record, 2026-11-01)

Both groups (A: app.py + keymap.py; B: views.py) implemented the frozen graphs
(`graph-proto-A.cw.md`, `graph-proto-B.cw.md`) and the seams of `e2-seams.md` with
no deviation from the frozen interfaces.

Notes for the reviewer (implementation equivalences, not deviations):

- `PresentScreen.action_export` branches on `self._view < 2` where the graph says
  "in views 1/2" (`pid = None if self._all() else self._project_id` is kept
  verbatim for the scope read); `_all()` is exactly `self._view == 2`, so the two
  forms are the same predicate.
- S-R2-2 is honoured as written: URLs are rebound (`t2.urls = []`) on per-task
  shallow copies inside `present_deck_boards`; no `.clear()`, no mutation of the
  board's own Task objects or lists.
- Seam S-7 landed in one commit: group A dropped the four removed names from
  `app.py`'s views import in the same changeset in which group B removed them
  from `views.py`; `env -u NO_COLOR python -c "import taskboard.app"` passes.

No test file was created, edited or deleted. No existing test file imports a
removed function at module level (all such imports are function-level), so
collection does not break; the tests that reference the removed functions or the
SVG export fail at run time by design and are the independent tester's rewrite
list (see baseline-notes.md §"Tests that call a target by name").

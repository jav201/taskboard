# Increment 22 — F-16: the card composes at the seat it is drawn at

**Batch:** `wedge` · **AC-1, AC-2, AC-3, AC-4** · the finding `capture-settle` filed and named as its
next task (`inc20.md` §5/§8, `inc21.md` §7)
**Files:** `prototypes/widget_slice/kanban.py`, `tests/test_card_seat.py` (new) — **2 source files**;
plus `.fast-dev-flow/spec.md` (new batch spec) and
`.fast-dev-flow/archive/spec-20260905-capture-settle-closed.md` (predecessor, archived verbatim).

**The sweep now finishes every time: 27/30 → 30/30, with 0/22 frames drifting and 0.0 % pairwise
disagreement unchanged. The fix is 20 lines and it moves no committed frame.**

---

## 1. What changed

`TaskCard` repaired its paint from EVENTS. There were three chances and the wedge spends all three:

| | | what it does when the seat is 0 |
| --- | --- | --- |
| `on_mount` → `render_card()` | synchronous | composes at the 20-cell fallback (`w = 18`) |
| `on_mount` → `call_after_refresh(render_card)` | deferred | fires **before the layout ran**: composes at 18 again |
| `on_resize` → `render_card()` | on the event | **the event is never posted** |

The card now composes in `render()` — the one hook the framework guarantees on a seat change:

```python
    def render(self):
        if self._painted_w != self.size.width:
            self._painted_w = self.size.width
            self.render_card()
        return super().render()
```

**`_painted_w` is written in `render()` and nowhere else, and that is deliberate.** The settle's
condition C (`capture_languages._stale_paint`) diagnoses a card by calling `render_card()` with
`update` intercepted; if `render_card` stamped the counter, the diagnostic would mark a stale card
fresh and quietly defeat the repair it exists to catch. `render_card`, `on_mount` and `on_resize` are
untouched.

---

## 2. AC-1 — the state dump, and why the repair could not be an event

### 2a. The instrument

`prototypes/out/_f16_probe.py` (gitignored scratch) runs the shipped sweep with five recorders and
dumps at the wedge. It records and never repairs: every patch calls the original.

- `TaskCard.render_card` — every call and the seat it saw, with `_stale_paint`'s shadow calls excluded
  (they are detectable: the oracle shims `update` as an instance attribute).
- `TaskCard.on_mount` / `on_resize` — every call.
- `Widget._size_updated` — every size change, with `layout` and the return.
- `MessagePump.post_message` — every `events.Resize` posted **to a `TaskCard`**.
- `Compositor.reflow` (`shown` / `resized` membership) and the `Compositor.full_map` **property**, which
  rebuilds the map lazily; both snapshot each card's region so a geometry change can be attributed to
  the reflow or to the lazy rebuild.

**15 sweeps in ONE interpreter produced no wedge**, which agrees with inc20 §6 and with race-probe's own
§4a: every in-process arm is 0/30. Run one sweep per fresh process, it landed on **attempt 15**.

### 2b. The dump

```
WEDGE on board industrial at 6020.56 ms
  board industrial: never settled after 40 frames; not settled:
    kb-card@60,21 STALE PAINT (composed at a seat it no longer has; seat is now 31), (x4)

  compositor: reflow=141 lazy_full_map=52 reflow_visible=0 size=Size(118, 34) dirty_regions=0
  app.message_queue_size=0 screen.mq=0 screen._dirty_widgets=0 screen._next_callbacks=0
  board: mq=0 next_cbs=0 _built_w=116 size=Size(116, 14) layout=columns

  --- STALE CARD 'Design homepage mockups' col=1 row=0
      size=Size(31, 2) region=Region(60, 21, 33, 2) outer=Size(33, 2) container=Size(31, 2)
      display=True visible=True mounted=True running=True styles.width=1fr
      _repaint_required=False _layout_required=False _recompose_required=False
      _dirty_regions=0 render_cache.size=Size(31, 2)
      message_queue_size=0 next_callbacks=0 in screen._dirty_widgets=False
      parent=PhaseColumn size=Size(33, 14) vscroll=False scroll_y=0.0
      compositor region=Region(60, 21, 33, 2) clip=Region(60, 19, 33, 14)
      COMPOSITED FRAME in area:
        | ▐01 Design h… [0d]              |
        |     [PH:DOIN]                   |
      CONTENT (widget's own) |…[#f2f2f2]Design h…[/] [#ffd400]\[0d][/]…|
      SHADOW  (render now)   |…[#f2f2f2]Design homepage …[/] [#ffd400]\[0d][/]…|
      _render_cache.lines[0] |▐01 Design h… [0d]|
```

**Every question the diagnosis had to answer, answered by that block:**

- *What is not re-rendering?* Four `kb-card`s in the DOING column, at seats 60,21 / 60,23 / 60,25 /
  60,27 — one column, four consecutive rows.
- *Is anything pending?* **No.** `_repaint_required`, `_layout_required`, `_recompose_required` all
  `False`; `_dirty_regions` empty; the card's own message queue and `_next_callbacks` empty; the board's,
  the screen's and the app's queues all zero; the card is not in `screen._dirty_widgets`. Nothing is
  waiting to run. **This is not a settle being impatient. The app is at rest and wrong.**
- *Is it drawn?* `display=True visible=True`, and the compositor lists it with a region that intersects
  its clip.
- *Is the truncated title a stale Strip in the compositor's cache, or the card's own render?*
  **The card's own.** `_render_cache.size` is `Size(31, 2)` — the cache was rebuilt AT THE NEW WIDTH —
  and it contains the narrow text. The compositor is faithfully drawing what the widget gave it; the
  widget gave it a bake composed for a seat 13 cells narrower.

### 2c. The timeline — the mechanism, one card, verbatim

```
    4647.36 ms  on_mount           seat=0 title='Design homepage mockup'
    4647.54 ms  render             seat=0 -> w=18
    4660.99 ms  render             seat=0 -> w=18
    4667.90 ms  GEO[LAZY-full_map] None -> (33, 2)
    4674.98 ms  _size_updated      0x0 -> 33x2 ret=True layout=True
    (nothing, ever again)
```

All four cards produce the same five lines within 0.6 ms of each other. **No `POST-Resize`. No
`ON_RESIZE`. No `reflow.shown`, no `reflow.RESIZED`.** And it never comes right: the probe kept the loop
alive **200 more pauses (5.9 s)**, re-dumped, and the timeline had not gained a line —
`frame changed after 200 pauses: False`.

**Read against Textual 8.2.8's source, the mechanism is exact:**

1. `Screen._refresh_layout` (`screen.py:1360-1377`) walks the compositor's layers and calls
   `widget._size_updated(...)` on **every** widget — which sets `_size` and, on a change, calls
   `_set_dirty()` — but posts `Resize` only for `send_resize = shown | resized`.
2. `shown` and `resized` come from `Compositor.reflow` (`_compositor.py:400-427`) as a **diff of the new
   map against `old_map = self._full_map`**: `shown = new − old`, and `resized` = widgets in both whose
   `old_map[w].region.size` differs.
3. `Compositor.full_map` (`_compositor.py:485-497`) is a **lazy property**. When
   `update_widgets` has set `_full_map_invalidated` — which it does whenever a dirty widget is not yet in
   `visible_widgets`, i.e. exactly what a freshly mounted card is (`_compositor.py:1256-1259`) — the next
   read of the property re-arranges the whole tree and **writes the new geometry into `_full_map`,
   posting nothing.** The probe counted **52** such rebuilds in this run.

So when the lazy rebuild wins the race, the reflow that follows compares the new map against a map that
already holds the new geometry. The diff is empty, `send_resize` does not contain the card, and
`_size_updated` moves `_size` from 0 to 33 in silence. `on_resize` — the card's only remaining
repair — never fires.

**The falsifiable prediction, and it held:** if that is the mechanism, then a repair hung on the
RE-RENDER rather than on the EVENT must take the rate to zero, because `_size_updated` calls
`_set_dirty()` on the very size change it fails to announce — and the dump proves the re-render happened
(`render_cache.size == Size(31, 2)`). It did: 30/30, §4a.

---

## 3. Files modified

- `prototypes/widget_slice/kanban.py` — `TaskCard.__init__` gains `_painted_w`; new `TaskCard.render`.
  **20 insertions, 0 deletions** (`git diff --stat`).
- `tests/test_card_seat.py` — **new**, 2 tests.
- `.fast-dev-flow/spec.md` — the new batch spec (Phase A), predecessor archived verbatim to
  `.fast-dev-flow/archive/spec-20260905-capture-settle-closed.md`.
- Evidence in the gitignored scratch yard: `_race_wedge_before.txt`, `_race_wedge_after.txt`,
  `_f16_dump.txt`, `_f16_suite.txt`, and the three throwaway probes `_f16_probe.py`, `_f16_cmp.py`,
  `_f16_dbg.py`, plus `_kanban_fixed.py.bak` (the copy the red arm restored from).

---

## 4. How to test, and the results

```powershell
cd "C:\Users\jjgh8\Github\taskboard\.claude\worktrees\kanban-variants"
$env:PYTHONIOENCODING = "utf-8"

python -X utf8 -m pytest -q tests\test_card_seat.py
python -X utf8 -m pytest -q

# THE GATE (~6.5 min): 30 whole sweeps in 30 fresh interpreters, all 22 frames diffed
python -X utf8 prototypes\race_probe.py --cross 30 --engine shipped --tag wedge_after `
    > prototypes\out\_race_wedge_after.txt 2>&1
```

Every headless run went to a **file**, never `DEVNULL` (L-42). No terminal process was killed. No
`--surface` was issued (F-8 untouched). `prototypes/verify_language.py` was **not** run (F-17 would
rewrite the fixture the frames are measured against). `prototypes/gallery/` was never opened for write.

### 4a. AC-2 — the gate, before and after, from the one tool

| arm | sweeps that finished | frames drifting | sweeps non-modal | pairwise |
| --- | --- | --- | --- | --- |
| **before** (HEAD `2817550`) | **27 / 30** | 0 / 22 | 0 / 27 | 0.0 % (0/351) |
| **after** | **30 / 30** | 0 / 22 | 0 / 30 | 0.0 % (0/435) |

Before, the three that stopped — the columns branch, four DOING cards, every time:

```
sweep  0  RuntimeError: board instrument:  never settled after 40 frames; not settled:
            kb-card@59,20 STALE PAINT (... seat is now 28), ... (x4)
sweep 17  RuntimeError: board industrial: ... kb-card@60,21 ... (seat is now 31) (x4)
sweep 29  RuntimeError: board industrial: ... kb-card@60,21 ... (seat is now 31) (x4)
```

After:

```
  CROSS-PROCESS DRIFT: 0/22 frames over 30 sweeps -> []
  sweeps that are non-modal on >=1 frame: 0/30 []
  PAIRWISE DISAGREEMENT (what the shipped determinism check asks): 0/435 pairs = 0.0 %
```

`grep -c 'FAILED rc=1'` on the after log: **0**. inc20's 0/22 and 0.0 % are held, not traded away —
which was the other half of AC-2, because a "fix" that made the settle stop asking would also show 30/30.

**Sweep time is unchanged:** 11.6-13.5 s per sweep after, 11.6-12.9 s before. The repair is one extra
string build per seat change, and there is at most one per card per layout.

### 4b. AC-3 — the test, red then green, run against both files

`tests/test_card_seat.py`, two tests. Against **HEAD `2817550`'s** `kanban.py` (installed with
`git show HEAD:… > …`, restored from a copy in the same command, verified by `git diff --stat`):

```
FAILED tests/test_card_seat.py::test_the_next_paint_composes_at_the_new_seat
  AssertionError: the card is drawing a paint composed at a seat it no longer has:
  content '[on #2e2e2e][#4a4a4a]▐[/][#8f8f8f]01[/] [#f2f2f2]Design h…[/] [#4a4a4a]\[--][/]['
1 failed, 1 passed in 0.38s
```

Against the new file:

```
2 passed in 0.26s
```

**The one that passes in both is the point**, and it is the same device inc20 §4c used.
`test_a_card_repaired_only_from_events_keeps_the_narrow_bake` drives `PreFixCard` — `TaskCard` with
`render = Static.render`, the paint path as it stood at `2817550`, quoted in the test rather than
reached for through git — and asserts it DOES go stale. Without it, "the shipped card is not stale"
could be satisfied by a fixture that never widened anything.

**How the wedge is reached without the race, and what that costs in fidelity.** The missing POST needs a
fresh interpreter and lands about one sweep in ten; a test that drove it would fail for the wrong reason
nine times out of ten. What the race LEAVES BEHIND is not a race — it is a card whose seat moved with no
repair on the other end of the event — and `deafen()` reaches that state in three lines: it replaces
`TaskCard.on_resize` with a recorder, so the event arrives and repairs nothing, which from the card's
side is the same hole as an event that was never sent. Both tests assert the recorder is **non-empty**,
so a fixture that stopped delivering the resize would fail rather than pass quietly.

**One thing that had to be measured before it could be written.** The first fixture made the card deaf
by SUBCLASSING `TaskCard.on_resize`. It does not work: Textual dispatches the handler of **every class
in the MRO**, so the base's repair still ran and the pre-fix card came out clean. The patch had to go on
`TaskCard` itself, and the reason is in the helper's docstring rather than left as a trap.

The other thing measured and worth stating: **`Widget.size` is not `_size`.** It is
`content_region.size`, and `region` is read from the **compositor's map** — so the seat a card composes
against is the compositor's, not the widget's cached size. An earlier version of this test moved
`_size_updated` directly and changed nothing observable, which is how that got established.

### 4c. AC-4 — which frames moved: none, and that is a measurement

The 22 frames the 30-sweep arm produced were hashed against the committed `prototypes/gallery/*.txt`:

```
after  : 22 frames compared against prototypes/gallery/ -> 0 differ
before : 22 frames compared against prototypes/gallery/ -> 0 differ
```

All 22 hashes are identical between the before and after arms as well
(`board_industrial.txt 0182fbd7cdb1` ×27 before, ×30 after, and so on for the other 21).

**Why nothing moved, said plainly:** the wedged frame was never written. inc20's settle refuses it — that
is what the 3 loud failures WERE — so the committed art has always been the good frame. This fix does not
change what a settled board draws; it removes the state in which the board never settles. A re-bake would
have rewritten 44 files with identical bytes, so `prototypes/gallery/` was not opened, and
`export_to_skill.py` was not run: **no frame the skill carries moved.**

### 4d. Suite

```
python -X utf8 -m pytest -q
688 passed, 2 skipped, 4 warnings in 34.88s
```

**686 + 2 = 688**, the 686 baseline plus this increment's two tests. The baseline's one failure —
`tests/test_app.py::test_win_clipboard_roundtrip`, environment-dependent (PENDING #22, `RUN.md`) — is
**green on this run**, which is the same coin it has always been: it passes or fails with the state of
the Windows clipboard and this increment touches neither. Recorded rather than claimed as an
improvement.

---

## 5. Risks

- **The repair runs inside `render()`.** `render_card()` calls `Static.update()`, which calls
  `refresh(layout=True)` — so a paint can schedule a layout. It is bounded: `_painted_w` is set BEFORE
  the recompose, so at most one extra layout pass per seat change, and the second pass finds nothing to
  do. It is still a refresh from a render path, which is a pattern worth knowing about before the next
  person adds a second one. Measured: sweep time unmoved (§4a).
- **A hazard that was loud is now silent.** The wedge announced itself by stopping the sweep. It cannot
  occur now, but the same class of defect in any OTHER widget — the hero, the column heads, the tiles —
  still depends on `on_resize` and would go unnoticed in exactly the same way. Only `TaskCard` is fixed
  here, because only `TaskCard` had the measurement.
- **`_painted_w` is a second source of truth about the seat**, and it is correct only because it is
  written in one place. The packet says why (§1); a future `render_card` that stamps it would silently
  re-open F-16 AND blind condition C at the same time.
- **The test reaches the wedged state by neutralising `on_resize`, not by racing the compositor**
  (§4b). It pins the invariant — a seat change is repaired at paint time, with no help from the event —
  and it does NOT pin the framework behaviour that makes the event go missing. If Textual changes how
  `send_resize` is computed, the tests stay green and the wedge stops existing without anyone noticing.
  The 30-sweep arm is what would notice.
- **30/30 is a measurement, not a proof.** The before rate was 3 in 30; a run of 30 clean sweeps rules
  out that rate with decent confidence and does not rule out a rarer one.

---

## 6. Pending

- **F-16 is closed.** F-1's app half goes with it; F-1's capture half closed at inc20.
- **F-8, F-14, F-15 untouched** — no `--surface` sweep, no `verify_language.py` run in this increment.
- **F-17 open** (`verify_language.py:11592` overwrites `prototypes/out/_fixture_late.json` relative to
  `date.today()`). It is the reason the language harness was not run here, so this increment did not
  re-check F-14's two pre-existing reds either.
- **Every other widget still repairs from `on_resize`** (§5). `Hero`, `Tile`, the column heads and the
  empty seats all compose from an event, and nothing measures whether they ever miss one. That is the
  next thing this batch's finding points at, and it is not this increment's.
- **No check asserts a published component sheet carries every derived state** — inc21 §5's hole, still
  open.

---

## 7. Suggested next task

**Ask the other push-painted widgets the question F-16 answered for `TaskCard`.** The instrument already
exists: `_f16_probe.py`'s `_size_updated` / `POST-Resize` recorders are widget-agnostic, so pointing them
at `Hero`, `Tile` and the `col-head`/`kb-empty` `Static`s costs one edit and says, with counts, whether
any of them takes a silent seat change. If none does, that is a one-line finding and the class of bug is
closed; if one does, it is the same 20 lines.

---

## Evidence checklist

- [x] **Tests/type checks/lint pass** — `688 passed, 2 skipped, 4 warnings in 34.88s` (§4d); 686
      baseline + 2 new. The baseline's environment-dependent clipboard test is green on this run and is
      recorded as such rather than claimed.
- [x] **No secrets in code or output** — the change is one widget's paint path: no path is read, no file
      written, no network. `freeze_clock()`'s repointing of `default_board_path` at the synthetic
      fixture is untouched, so no capture can print the operator's real board.
      `tests/test_no_live_board.py` and `tests/test_privacy_sweep.py` are green in the suite.
- [x] **No destructive commands run without approval** — no `rm`, no terminal process killed, no force,
      no `git` command that discards work. The one file swapped in place (HEAD's `kanban.py`, for §4b's
      red run) was restored from a copy in the same command and verified with `git diff --stat`
      (`20 insertions`, the fix and nothing else). Every sweep wrote to a `TemporaryDirectory` or to the
      gitignored scratch yard; `prototypes/gallery/` was never opened for write.
- [x] **File count within cap** — 2 source files (`prototypes/widget_slice/kanban.py`,
      `tests/test_card_seat.py`) plus the batch spec and the archived predecessor: 4, under the 5 the
      spec sets.
- [x] **Review packet attached** — this document.

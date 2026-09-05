# Quick Spec — taskboard · batch "kits-learn-4" (the last sixteen cells, and the six that inherit)

**Batch:** `2026-09-05-fastflow-15` · **Base:** worktree `kanban-variants`, HEAD `e2169c7`
(harness-hygiene phase C), pushed. Predecessor `harness-hygiene` closed 2026-09-05, §8 filled, archived
verbatim to `archive/spec-20260905-harness-hygiene-closed.md`. Language: English.
Increments continue the worktree's single sequence: **… inc24 · inc25 · inc26 … inc27 … inc32**.

**Operator approval 2026-09-05.** Two things, stated as one: bring the **16 component cells that did not
reach `implementa` in `kits-learn-3`** to `implementa`, and have the **six languages that inherit base
mechanisms choose their own**.

**Input:** the matrix `kits-learn-3` left at **14 of 30**, derived by `prototypes/components/matrix.py`
from the sheets rather than typed:

```
                        S1              S2              S3              S4              S5              S6
corgi             evoca 1E        evoca 3E    implementa -    implementa -    rehusa 1R/0E    implementa -
blueprint     rehusa 1R/0E        evoca 3E    implementa -    rehusa 1R/0E    implementa -    implementa -
prism             evoca 1E        evoca 3E    implementa -        evoca 1E    implementa -    implementa -
naught            evoca 1E        evoca 3E    implementa -        evoca 1E    implementa -    implementa -
ledger            evoca 1E        evoca 3E    implementa -        evoca 1E    rehusa 1R/0E    implementa -

S1: pane_split x5      S2: Kit.error x5, Kit.required() x5, Kit.textarea x5
S4: pane_split x4      S5: Kit.readout_label x2
```

Five primitives, named **before** the batch by `prototypes/components/PROTOTYPE.md` §5/§6.3 and by
`inc19.md` §8, plus one inheritance debt `inc19.md` §7 records in one line: *"Five languages inherit the
base hint row and the base match style."*

---

## 1. Objective (1 line)

Seat the five remaining primitives with a per-language mechanism each, take the matrix to **30 of 30
`implementa` with every refusal DECLARED in a registry rather than drawn by hand**, and close the
inheritance debt on the seven older mechanisms for the six languages that never chose them.

---

## 2. User stories

- As **the operator judging these thirty frames**, I want no element in any frame to be hand-drawn in
  `prototypes/components/screens.py`, so that what I am looking at is eleven kits and not a prototype's
  taste.
- As **a language that says no**, I want my refusal to be *read* by the mechanism rather than *noted* by
  the frame, so that deleting my entry makes me draw the thing I committed against and a test goes red.
- As **one of the six languages that never got asked**, I want my own answer to `field_row`, `DISCLOSE`,
  `DANGER_FORM`, `LEVELS`, `MATCH_STYLE`, `keyhint` and `overlay`, because a seat with five
  implementations and six holes is the palette-swap failure with a longer fuse.
- As **anyone running the toolbox**, I want `RUN.md` and the exporter's docstring to describe the harness
  that exists, because `harness-hygiene` closed F-17 and three lines still describe it in the present
  tense.

---

## 3. Acceptance criteria (observable)

- [ ] **AC-0 · inc27 · the three stale lines.** `RUN.md`'s "2178 checks" and "flake-free since the
  forty-sixth pass", and `export_to_skill.py:copy_captures`'s docstring describing F-17's symptom in the
  present tense. Three lines, no behaviour.
- [ ] **AC-1 · inc28 · `Kit.pane_split`.** The S1 divider and the S4 backdrop's split come out of the kit
  in all five. Blueprint's refusal of the vertical rule is **declared in a registry the mechanism reads**
  (the `MODAL_BORDER_REFUSED` pattern), not noted by the frame. Property test: **five pairwise-distinct
  splits for one width**, compared on the plain text; and `render.py`'s closure law holds on every S1 and
  S4 frame.
- [ ] **AC-2 · inc29 · `Kit.error` + `Kit.required`.** The validation message row and the required marker
  for S2, both deriving from what the language already declares where such a table exists. Property test:
  the message **survives greyscale** and comes back **byte for byte**; the five marks are distinct; the
  required mark is not a bare `*` in any of the five.
- [ ] **AC-3 · inc30 · `Kit.textarea`.** The multi-line field with its own caret row and wrap mark.
  Property test: **a 3-line text renders three rows in all five, with a visible caret row**, and the text
  comes back byte for byte.
- [ ] **AC-4 · inc31 · `Kit.readout_label`.** The labelled — never numbered — readout for S5 in the two
  languages that still hand-draw it. L-33's test extended: a numbered language's readout label carries no
  digit, and the refusal is in a registry.
- [ ] **AC-5 · inc32 · the six inheriting languages choose.** Instrument, Swiss, Industrial, Nord,
  Darkside and Solari each answer for `field_row`, `DISCLOSE`, `DANGER_FORM`, `LEVELS`, `MATCH_STYLE`,
  `keyhint` and `overlay`, **each with its commitment cited from `LANGUAGES.md`**, and a refusal declared
  in the registries where the language says no. Property test: **no two languages return the same plain
  row for the same input** on the mechanisms where a plain difference is lawful.
- [ ] **AC-6 · the matrix reaches 30.** `matrix.py` prints `implementa` in all thirty cells, refusals
  declared where a language says no, and the 30 `.candidates.md` sidecars are regenerated and empty.
- [ ] **AC-7 · nothing else moves.** Suite green after every increment (693 baseline).
  `verify_language.py` **ALL PASSED** (10857 baseline) — it is run freely now, F-17 is closed. The
  `--surface` sweep run **plain and alone** leaves its 11 frames unchanged unless a frame legitimately
  moves, and the packet says which and why.
- [ ] **AC-8 · export.** `python prototypes/export_to_skill.py "C:/Users/jjgh8/.claude/skills/tui-design"`
  at the close, its output reported, the skill **never hand-edited**; plus a list of frames that should
  join the skill's gallery (compositor provenance, zero hand-drawn) with a draft `Limit` line each.

---

## 4. Validation strategy

`python -X utf8 -m pytest -q` is the gate. Baseline at Phase A, measured: **692 passed, 1 failed, 2
skipped** — the failure is the documented env-dependent `test_win_clipboard_roundtrip` (PENDING #22),
which is what "693 baseline" counts.

`python -X utf8 prototypes/verify_language.py` is a gate here and it is **run freely**: F-17 closed in
inc24, so the harness no longer rewrites `prototypes/out/_fixture_late.json`. Baseline at Phase A,
measured: **10857 PASS, ALL PASSED**, working tree clean afterwards.

`python -X utf8 prototypes/components/render.py` re-renders the 30 frames and their sidecars, and
`python -X utf8 prototypes/components/matrix.py` derives the matrix from the same sheets. Both run after
every increment that touches a mechanism a frame consumes.

Headless stdout goes **to a file, never to `DEVNULL`** (L-42). `--surface` is run **plain and alone**
(F-8). No terminal process is ever killed. Git: committed per increment in this worktree, pushed at the
close.

---

## 5. Non-goals (what is OUT)

- **`required` and `pane_split` for the six inheriting languages.** AC-5 names seven mechanisms and these
  are not among them. Both are recorded as the batch's own inheritance debt in §8 rather than smuggled in.
- **`prototypes/gallery/`'s 22 frames.** Re-swept only to prove they are unmoved.
- **The skill's prose.** `export_to_skill.py` writes it; nothing is hand-edited. Gallery candidates are
  *proposed*, not installed.
- **pulso, GBL, the course.** Untouched.
- **A `TAIL` mark of its own** (`inc19.md` §8). Still nobody's ruling.

---

## 6. Detected security flags

None fires. Every change is a pure-render method on a kit, a test, or a prototype frame builder. No
network, no new dependency, no destructive command, no secret, no path outside the worktree except the
skill directory the exporter already writes and which the operator named.

---

## 7. Batch status

| | |
| --- | --- |
| Phase A (spec) | **done** — this file; predecessor archived verbatim |
| Phase B (implement) | inc27 · inc28 · inc29 · inc30 · inc31 · inc32 |
| Phase C (close) | §8 |

---

## 8. Close (filled in phase C)

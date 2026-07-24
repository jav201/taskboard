# Quick Spec — gantt: wider task/project label column

## 1. Objective (1 line)
Widen the gantt view's left label column so project and task names are readable, not truncated to ~14 chars.

## 2. User stories
- As a user reading the gantt, I want to see each task's text and the full project name, so that the timeline is actually usable.

## 3. Acceptance criteria (observable)
- [ ] AC1: at a normal widget width (inner >= ~100), the label column shows at least ~26 visible characters of a name (today it caps at ~14), so names like "Unity Trainings" and "Training_Playground_Navigation" are read in full or near-full.
- [ ] AC2: the label width scales with terminal width (wider terminal -> wider labels) with a sensible floor and ceiling, and never leaves the timeline with zero week columns.
- [ ] AC3: every gantt row stays width-exact at 40/68/100/140, and the existing gantt tests (dual-density bar, dividers, adaptive meta, due figure) stay green.

## 4. Validation strategy
Adjust `glabel_w` in `render_gantt` to a wider scaling formula (one line). Add a test asserting the label width at a wide render is >= the old ceiling+something (e.g. a long name that used to truncate now appears with more of its text), plus the width-exact sweep already exists. Manual smoke: render the real board and read the project/task names.

## 5. Non-goals
- No change to the timeline scale, bar textures, meta column, or any other view.
- Not making EVERY possible name fit (a 30+ char name may still ellipsize at narrow widths) — just making the column generous instead of stingy.

## 6. Detected security flags
- [ ] Auth / identity
- [ ] Secrets / config
- [ ] External integrations
- [ ] Sensitive data
- [ ] Destructive DB
- [ ] Input / attack surface
- [ ] Network / exposure

**security_required:** false

## 7. Batch status
| Field | Value |
|-------|-------|
| Current phase | closed |
| Started | 2026-07-23 |
| Closed | 2026-07-23 |
| Notes | 1 increment, 1-2 files (views.py + test). Old batch spec archived. |


## 8. Close (2026-07-23)
`5ae4d42` — `glabel_w` in render_gantt: `max(10, min(16, inner//4))` -> `max(18, min(30, inner//3))`. Visible name width doubles (14 -> 28 chars at inner 108); timeline gives up ~2 week columns. 104 tests green (one existing test's local glabel_w proxy updated to mirror the new formula — truth-preserving). Verified on a COPY of the real board: "Unity Trainings" and "GPU Homelab (MLOps)" now render in full; only a 30-char title still ellipsizes; all rows width-exact; real board untouched.

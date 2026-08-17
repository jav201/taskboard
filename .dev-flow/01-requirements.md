:batch: 2026-08-17-batch-07
:project: taskboard
:language: en

# Requirements — Focus Board

## 1. Scope

A new view, **Focus Board**, for tasks (and whole projects) the user has marked for
tracking and detail work. It is a reading-and-annotation surface, not an editor:
all mutations route through the existing task/project modals and quick keys.

## 2. User stories and acceptance criteria

### US-01 Pin/unpin a task
**As a** taskboard user  
**I want** to mark or unmark the selected task as pinned  
**So that** it appears in (or leaves) the Focus Board.

**AC1.** Pressing `t` toggles `task.pinned` for the selected task.  
**AC2.** The pinned flag persists to `board.json` and survives reload.  
**AC3.** The task editor shows a checkbox for `pinned`.  
**AC4.** A pinned task renders with a ⭐ indicator in views that show it.

### US-02 Pin/unpin a project
**As a** taskboard user  
**I want** to mark or unmark a whole project as pinned  
**So that** all its tasks appear in the Focus Board at once.

**AC1.** Pressing `T` toggles `project.pinned` for the selected task's project.  
**AC2.** All tasks of a pinned project are included in the Focus Board.  
**AC3.** A task pinned individually AND belonging to a pinned project appears once.  
**AC4.** Unpinning a project does not unpin individually pinned tasks from other projects.

### US-03 Card stream presentation
**As a** Focus Board user  
**I want** pinned tasks rendered as vertical cards  
**So that** I can read notes, dates and image counts at a glance.

**AC1.** The default Focus Board (`5`) shows the card stream.  
**AC2.** Each card shows: project spine, title, due readout, note snippet, image count, URL count, emoji row.  
**AC3.** Emoji row supports: ❗ alert, ❓ question, ⭐ important, ⏰ due soon, 📋 has notes, ☐/☑ checklist items.  
**AC4.** Cards are ordered by project then due date; Inbox last.

### US-04 Inspector split presentation
**As a** Focus Board user  
**I want** a two-pane layout  
**So that** I can read full notes and preview images of the selected pinned task.

**AC1.** `Tab` inside Focus Board cycles card stream → inspector split → image-first.  
**AC2.** The left pane lists pinned tasks; the right pane shows the selected task's details.  
**AC3.** The detail pane shows: full notes, image thumbnails/names, URLs, checklist, due readout.  
**AC4.** `i` opens the existing ImageViewer for the selected task.

### US-05 Image-first presentation
**As a** Focus Board user  
**I want** pinned tasks with images to surface first  
**So that** visual material is scannable.

**AC1.** The image-first presentation groups pinned tasks into "with images" and "without images".  
**AC2.** Each image task shows a thumbnail placeholder and image count.  
**AC3.** Tasks without images are listed compactly below.

## 3. Functional requirements

- FR-01 `Task` shall have a `pinned: bool` field, default `False`.
- FR-02 `Project` shall have a `pinned: bool` field, default `False`.
- FR-03 Both flags shall round-trip through JSON load/save.
- FR-04 `render_focus` shall accept `presentation` (`"cards"`, `"inspector"`, `"images"`).
- FR-05 Focus Board content shall be the union of: individually pinned tasks + tasks whose project is pinned.
- FR-06 The view shall respect `show_archived`: archived pinned tasks are hidden unless `v` is active.

## 4. Interface requirements

- IR-01 Key `5` enters Focus Board.
- IR-02 `t` toggles pin on the selected task.
- IR-03 `T` toggles pin on the selected task's project.
- IR-04 `Tab` cycles the three presentations.
- IR-05 `i` opens the ImageViewer for the selected task.
- IR-06 `esc` exits Focus Board to the previous view.

## 5. Out of scope

- Persisting colour highlights inside task text.
- Inline image pixel rendering (terminal-dependent); preview is a placeholder strip.
- Pinning from the project manager modal.

# Inc K — orchestrator rulings (E2/E3)

## Round 0a — interface seams (before the group prototypes)

| Seam | Ruling | Why |
|---|---|---|
| S-a: an open-board dump saves through `live.add_task` + the app's plain `save()` (no lock, no stamp check) | ACCEPT. Recorded risk: same as every other edit of the open board today (`Board.save` is plain `write_text` app-wide). | Consistent with the app's existing writes of the open board; changing the open-board save path is out of scope. |
| S-b: the in-memory rollback of `live` on a failed dump (LLR-4404.15) | ACCEPT in G-S. `dump_note` already mutates `live` through `add_task`; one owner for the dump's all-or-nothing. | Keep the undo of a mutation beside the mutation. |
| S-c: the review list's choice dict lives in CaptureView (G-V) | ACCEPT. | No group boundary crossed. |

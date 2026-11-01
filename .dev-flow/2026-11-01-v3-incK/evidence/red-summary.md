# Inc K — RED on base (E4, independent tester)

Evidence state: `executed` (RED capture). The GREEN run is the orchestrator's (C-25); `approved` is not the tester's to write.

**Base:** `C:/Users/jjgh8/Github/taskboard-wt/incK-base` at `545c18a`; `taskboard.__file__` = `C:\Users\jjgh8\Github\taskboard-wt\incK-base\taskboard\__init__.py` (first line of the run in `red-base.txt`).
**Command (one complete run, transcript `evidence/red-base.txt`):**
`cd incK-base && env -u NO_COLOR python -m pytest -q -p no:cacheprovider tests/test_inbox_store.py tests/test_suggest.py tests/test_capture_view.py -rA` (with `PYTHONIOENCODING=utf-8` so the cp1252 console can print the box-drawing characters).
Base tree restored afterwards: copies deleted, `tests/test_modal_keys.py` checked out, `git -C incK-base status --short` empty.

## Counts

| File | Test functions | Collected | Failed on base | Passed on base | Errors |
|---|---|---|---|---|---|
| tests/test_inbox_store.py | 103 | 142 | 142 | 0 | 0 |
| tests/test_suggest.py | 28 | 28 | 28 | 0 | 0 |
| tests/test_capture_view.py | 135 | 154 | 153 | 1 | 0 |
| **total** | **266** | **324** | **323** | **1** | **0** |

`323 failed, 1 passed in 103.73s`. Every failure is a message assertion, never a collection error.
- 143 × `Failed: taskboard.inbox missing (not built yet)`
- 143 × ``AssertionError: `n` opened no capture view``
- 28 × `Failed: taskboard.suggest missing`
- 2 × `taskboard.app.CaptureView missing`
- 1 × `taskboard.app.corpus missing`
- 1 × ``TaskboardApp holds no `inbox` ``
- 1 × `KEYMAP entries with keys 'n': []` (TC-4401)
- 1 × the stack `['Screen', 'AddedList']` (TC-4414)
- 2 × `assert True is False` (TC-4411 and TC-4419: `check_action("capture")` is True at base)
- 1 × the README row missing (TC-4413)

**Edited existing test:** `tests/test_modal_keys.py` INVENTORY gains `"ReviewList": {}` (P-V-5). On the same base it gives `1 failed, 34 passed`. The failure is `test_TC_2407_every_modal_is_in_the_inventory` (`{'ReviewList'} == set()`), which is expected until ReviewList exists.

## Tests that pass on base (guards by design)

| Test | Why it is a guard |
|---|---|
| `tests/test_capture_view.py::test_TC_4415_the_other_n_keys_keep_their_meaning` | LLR-4401.15 says the `n` keys of the boards home, the people directory and the marks manager act as they do at 545c18a. The mutant it catches is the increment's own: an app-level priority `n` that beats those screens' bindings. |

## Disagreements with the graph (the tests follow the requirement or the ruling)

1. **TC-4481 (LLR-4403.21).** The threshold's "exactly 1 computation for note 2" assumed the withdrawn 1 s scoring pause; A-1 says the rail scores on every change. The test asserts the LLR's own words instead: no note text is scored twice, N1/N3 are never rescored, and N2's final text is scored once.
2. **TC-4577 (LLR-4406.17).** The graph example presses `alt+o` in the pad, then `space` in the review. By LLR-4406.3 those rows would open already checked, and `space` would uncheck them. The test uses `o` then `space` inside the review list.
3. **TC-4468.** The graph's halving example (0.0379) is below LOW, so it can never be observed as a hit. The test uses `Café questions clés` (0.1877, one shared stem) instead.
4. **TC-4486.** `%TEMP%/incK-e3fix/suggest_fix.py` is absent. The 7 probe notes and the digest formula were taken from the probe driver `%TEMP%/incK-T-probe/run.py` (the reference implementation was not read). The digest `d694943ce6d21f09` holds only if `Hit.why` is a list.
5. **TC-4489b.** The 300-document generator was never published, so the test uses its own (seed 7) and checks only the < 20 ms bound.
6. **TC-4551.** The graph example says "Course is busy", but `_undo_other` labels the lock with the folder name ("c" in fixture S). The test asserts `is busy` only.
7. **TC-4650 arm 2.** `resolve()` follows the junction, so the test sets the task's image path to its resolved form before the undo. Otherwise SEC-3's whole-record check answers "changed".
8. **TC-4617b and TC-4617.** A read-only folder does not block file creation on Windows, so the save or copy is made to fail by patching instead.

## Limits (not covered, or environment)

- **TC-4598, arm 3 of LLR-4407.18** (a pending record with an unchanged pad: `esc` writes once) is tested at layer 0 only (TC-4598b), not in the pilot.
- **TC-4622c** (symlink) and **TC-4650** (junction) skip, with the reason given, if Windows refuses the link privilege. Neither skipped here: they failed on the missing module first.
- **Spies** (`suggest`, `corpus`, `write_atomic`, `peek_board`, `save_pil_image`) patch both the defining module and the `taskboard.inbox` / `taskboard.app` attribute (`raising=False`), so they work whichever import style the build uses.
- **No GREEN run.** The tests were never run against the Inc K code, so their mechanics against the shipped widgets (ids `#cap-*`, `#rv-body`; `PadArea._highlights`) are `not-run` until the orchestrator's gate run.

## Coverage: TC → LLR

All 203 active LLRs have at least one test, the 9 withdrawn LLRs have none, and all 8 ATs are covered. The table below was generated from the test docstrings by `tcmap.py`, a scratch script under %TEMP%.

| LLR | TC (file) |
|---|---|
| LLR-4401.1 | TC-4401 (capture_view) |
| LLR-4401.2 | TC-4402 (capture_view) |
| LLR-4401.3 | TC-4403 (capture_view) |
| LLR-4401.4 | TC-4404 (capture_view) |
| LLR-4401.5 | TC-4405 (capture_view) |
| LLR-4401.6 | TC-4406 (capture_view) |
| LLR-4401.7 | TC-4407 (capture_view) |
| LLR-4401.8 | TC-4408 (capture_view) |
| LLR-4401.9 | TC-4409 (capture_view) |
| LLR-4401.10 | TC-4410 (capture_view) |
| LLR-4401.11 | TC-4411 (capture_view) |
| LLR-4401.12 | TC-4412 (capture_view) |
| LLR-4401.13 | TC-4413 (capture_view) |
| LLR-4401.14 | TC-4414 (capture_view) |
| LLR-4401.15 | TC-4415 (capture_view) |
| LLR-4401.16 | TC-4416 (capture_view) |
| LLR-4401.17 | TC-4417 (capture_view) |
| LLR-4401.18 | TC-4418 (capture_view) |
| LLR-4401.19 | TC-4419 (capture_view) |
| LLR-4402.1 | TC-4431 (inbox_store) |
| LLR-4402.2 | TC-4432 (inbox_store) |
| LLR-4402.3 | TC-4433 (inbox_store) |
| LLR-4402.4 | TC-4434 (inbox_store) |
| LLR-4402.5 | TC-4435 (inbox_store) |
| LLR-4402.6 | TC-4436 (capture_view) |
| LLR-4402.7 | TC-4437 (capture_view) |
| LLR-4402.8 | TC-4438 (inbox_store) |
| LLR-4402.9 | TC-4439 (capture_view) |
| LLR-4402.10 | TC-4440 (capture_view) |
| LLR-4402.11 | TC-4441 (capture_view) |
| LLR-4402.12 | TC-4442 (capture_view) |
| LLR-4402.13 | TC-4443 (capture_view) |
| LLR-4402.14 | TC-4444 (inbox_store), TC-4444b (capture_view) |
| LLR-4402.15 | TC-4445 (capture_view) |
| LLR-4402.16 | TC-4446b (inbox_store), TC-4446c (capture_view) |
| LLR-4402.17 | TC-4447 (capture_view) |
| LLR-4402.18 | TC-4448 (capture_view) |
| LLR-4403.1 | TC-4461 (suggest) |
| LLR-4403.2 | TC-4462 (suggest) |
| LLR-4403.3 | TC-4463 (suggest) |
| LLR-4403.4 | TC-4464 (suggest), TC-4464b (suggest) |
| LLR-4403.5 | TC-4465 (suggest) |
| LLR-4403.6 | TC-4466 (suggest), TC-4466b (suggest) |
| LLR-4403.7 | TC-4467 (suggest) |
| LLR-4403.8 | TC-4468 (suggest) |
| LLR-4403.9 | TC-4469 (suggest) |
| LLR-4403.10 | TC-4470 (suggest) |
| LLR-4403.11 | TC-4471 (suggest) |
| LLR-4403.12 | TC-4472 (suggest) |
| LLR-4403.13 | TC-4473 (suggest) |
| LLR-4403.14 | TC-4474 (suggest), TC-4474b (suggest) |
| LLR-4403.15 | TC-4475 (capture_view), TC-4475b (suggest) |
| LLR-4403.16 | TC-4476 (suggest), TC-4476b (capture_view), TC-4476c (capture_view) |
| LLR-4403.17 | TC-4477 (capture_view) |
| LLR-4403.18 | TC-4478 (capture_view) |
| LLR-4403.19 | TC-4479 (capture_view) |
| LLR-4403.20 | TC-4480 (capture_view) |
| LLR-4403.21 | TC-4481 (capture_view) |
| LLR-4403.22 | TC-4482 (suggest) |
| LLR-4403.23 | TC-4483 (suggest), TC-4483b (capture_view) |
| LLR-4403.24 | TC-4484 (suggest), TC-4484b (capture_view), TC-4484c (capture_view) |
| LLR-4403.25 | TC-4485 (suggest), TC-4485b (capture_view) |
| LLR-4403.26 | TC-4486 (suggest) |
| LLR-4403.27 | TC-4464b (suggest), TC-4487 (suggest) |
| LLR-4403.28 | TC-4488 (suggest), TC-4488b (capture_view) |
| LLR-4403.29 | TC-4489 (suggest), TC-4489b (suggest) |
| LLR-4404.1 | TC-4501 (capture_view), TC-4501b (capture_view) |
| LLR-4404.2 | TC-4502 (capture_view) |
| LLR-4404.3 | TC-4503 (capture_view) |
| LLR-4404.4 | TC-4504 (capture_view) |
| LLR-4404.5 | TC-4505 (capture_view) |
| LLR-4404.6 | TC-4506 (capture_view), TC-4506b (inbox_store) |
| LLR-4404.7 | TC-4507 (capture_view) |
| LLR-4404.8 | TC-4508 (capture_view) |
| LLR-4404.9 | TC-4509 (capture_view), TC-4509b (capture_view) |
| LLR-4404.10 | TC-4510 (capture_view), TC-4510b (capture_view) |
| LLR-4404.11 | TC-4511 (capture_view) |
| LLR-4404.12 | TC-4512 (capture_view), TC-4512b (capture_view) |
| LLR-4404.13 | TC-4513 (capture_view), TC-4513b (capture_view) |
| LLR-4404.14 | TC-4514 (capture_view), TC-4514b (capture_view) |
| LLR-4404.15 | TC-4515 (capture_view) |
| LLR-4404.16 | TC-4516 (capture_view) |
| LLR-4404.17 | TC-4517 (capture_view), TC-4517b (capture_view) |
| LLR-4404.18 | TC-4518 (capture_view) |
| LLR-4404.19 | TC-4519 (capture_view) |
| LLR-4404.20 | TC-4520 (capture_view) |
| LLR-4404.21 | TC-4521 (capture_view) |
| LLR-4404.22 | TC-4522 (capture_view) |
| LLR-4404.23 | TC-4523 (capture_view), TC-4523b (capture_view) |
| LLR-4404.24 | TC-4524 (capture_view) |
| LLR-4404.25 | TC-4525 (capture_view), TC-4525b (capture_view) |
| LLR-4404.26 | TC-4526 (capture_view), TC-4526b (capture_view) |
| LLR-4404.27 | TC-4527 (capture_view) |
| LLR-4404.28 | TC-4528 (capture_view), TC-4528b (inbox_store) |
| LLR-4404.29 | TC-4529 (capture_view), TC-4529b (capture_view) |
| LLR-4404.30 | TC-4530 (capture_view), TC-4530b (inbox_store) |
| LLR-4404.31 | TC-4531 (capture_view) |
| LLR-4404.32 | TC-4532 (capture_view) |
| LLR-4404.33 | TC-4533 (capture_view), TC-4533b (capture_view) |
| LLR-4404.34 | TC-4534 (capture_view) |
| LLR-4405.1 | TC-4541 (capture_view), TC-4541b (inbox_store) |
| LLR-4405.2 | TC-4542 (inbox_store) |
| LLR-4405.3 | TC-4543 (capture_view), TC-4543b (inbox_store) |
| LLR-4405.4 | TC-4544 (inbox_store) |
| LLR-4405.5 | TC-4545 (inbox_store) |
| LLR-4405.6 | TC-4546 (inbox_store) |
| LLR-4405.7 | TC-4547 (capture_view), TC-4547b (inbox_store) |
| LLR-4405.8 | TC-4548 (inbox_store), TC-4549 (capture_view) |
| LLR-4405.9 | TC-4549 (capture_view) |
| LLR-4405.10 | TC-4550 (inbox_store), TC-4550b (capture_view) |
| LLR-4405.11 | TC-4551 (inbox_store), TC-4551b (capture_view) |
| LLR-4405.12 | TC-4552 (inbox_store) |
| LLR-4405.13 | TC-4553 (capture_view) |
| LLR-4405.14 | TC-4554 (capture_view) |
| LLR-4405.15 | TC-4555 (capture_view) |
| LLR-4405.16 | TC-4556 (capture_view) |
| LLR-4405.17 | TC-4557 (inbox_store), TC-4557b (capture_view) |
| LLR-4405.18 | TC-4558 (inbox_store) |
| LLR-4405.19 | TC-4559 (inbox_store), TC-4559b (capture_view) |
| LLR-4406.1 | TC-4561 (capture_view) |
| LLR-4406.2 | TC-4562 (capture_view) |
| LLR-4406.3 | TC-4563 (capture_view) |
| LLR-4406.4 | TC-4564 (capture_view) |
| LLR-4406.5 | TC-4565 (capture_view) |
| LLR-4406.6 | TC-4566 (capture_view) |
| LLR-4406.7 | TC-4567 (capture_view) |
| LLR-4406.8 | TC-4568 (capture_view) |
| LLR-4406.9 | TC-4569 (capture_view) |
| LLR-4406.10 | TC-4570 (capture_view) |
| LLR-4406.11 | TC-4571 (capture_view) |
| LLR-4406.12 | TC-4572 (capture_view) |
| LLR-4406.13 | TC-4573 (capture_view) |
| LLR-4406.14 | TC-4574 (capture_view) |
| LLR-4406.15 | TC-4575 (capture_view) |
| LLR-4406.16 | TC-4576 (capture_view) |
| LLR-4406.17 | TC-4577 (capture_view) |
| LLR-4407.1 | TC-4581 (inbox_store), TC-4581b (inbox_store) |
| LLR-4407.2 | TC-4582 (inbox_store) |
| LLR-4407.3 | TC-4583 (inbox_store) |
| LLR-4407.4 | TC-4584 (inbox_store), TC-4584b (inbox_store) |
| LLR-4407.5 | TC-4585 (inbox_store) |
| LLR-4407.6 | TC-4586 (inbox_store) |
| LLR-4407.7 | TC-4587 (inbox_store) |
| LLR-4407.8 | TC-4588 (inbox_store), TC-4678b (inbox_store) |
| LLR-4407.9 | TC-4589 (inbox_store), TC-4589b (inbox_store) |
| LLR-4407.10 | TC-4590 (inbox_store) |
| LLR-4407.11 | TC-4591 (inbox_store) |
| LLR-4407.12 | TC-4592 (inbox_store), TC-4592b (inbox_store) |
| LLR-4407.13 | TC-4593 (inbox_store), TC-4593b (inbox_store) |
| LLR-4407.14 | TC-4594 (inbox_store), TC-4594b (inbox_store) |
| LLR-4407.15 | TC-4595 (inbox_store) |
| LLR-4407.16 | TC-4596 (inbox_store) |
| LLR-4407.17 | TC-4597 (inbox_store) |
| LLR-4407.18 | TC-4598 (inbox_store), TC-4598b (inbox_store) |
| LLR-4407.19 | AT-4408 (capture_view), TC-4599 (inbox_store) |
| LLR-4407.20 | TC-4600 (inbox_store), TC-4600b (inbox_store) |
| LLR-4407.21 | TC-4601 (inbox_store) |
| LLR-4407.22 | TC-4602 (inbox_store) |
| LLR-4407.23 | TC-4603 (inbox_store), TC-4603b (inbox_store) |
| LLR-4407.24 | TC-4604 (inbox_store) |
| LLR-4407.25 | TC-4605 (inbox_store) |
| LLR-4407.27 | TC-4607 (inbox_store) |
| LLR-4407.28 | TC-4608 (inbox_store) |
| LLR-4407.29 | TC-4609 (inbox_store) |
| LLR-4407.35 | TC-4675 (inbox_store) |
| LLR-4407.36 | TC-4676 (inbox_store) |
| LLR-4407.37 | TC-4677 (inbox_store), TC-4677b (inbox_store) |
| LLR-4407.38 | TC-4678 (inbox_store), TC-4678b (inbox_store) |
| LLR-4407.39 | TC-4679 (inbox_store) |
| LLR-4407.40 | TC-4680 (inbox_store) |
| LLR-4407.41 | TC-4681 (inbox_store), TC-4681b (inbox_store) |
| LLR-4407.42 | TC-4682 (inbox_store), TC-4682b (inbox_store) |
| LLR-4407.43 | TC-4683 (inbox_store), TC-4683b (inbox_store) |
| LLR-4407.44 | TC-4684 (inbox_store) |
| LLR-4407.45 | TC-4685 (inbox_store) |
| LLR-4407.46 | TC-4686 (inbox_store) |
| LLR-4407.47 | TC-4687 (inbox_store) |
| LLR-4407.48 | TC-4688 (inbox_store) |
| LLR-4407.49 | TC-4689 (inbox_store) |
| LLR-4408.1 | TC-4611 (inbox_store) |
| LLR-4408.2 | TC-4612 (inbox_store) |
| LLR-4408.3 | TC-4613 (inbox_store) |
| LLR-4408.4 | TC-4614 (capture_view) |
| LLR-4408.5 | TC-4615 (inbox_store), TC-4615b (capture_view) |
| LLR-4408.6 | TC-4616 (inbox_store), TC-4616b (capture_view) |
| LLR-4408.7 | TC-4617 (inbox_store), TC-4617b (capture_view) |
| LLR-4408.8 | TC-4618 (capture_view) |
| LLR-4408.9 | TC-4619 (capture_view) |
| LLR-4408.10 | TC-4620 (inbox_store) |
| LLR-4408.11 | TC-4621 (inbox_store) |
| LLR-4408.12 | TC-4622 (inbox_store), TC-4622c (inbox_store) |
| LLR-4408.13 | TC-4623 (inbox_store) |
| LLR-4408.15 | TC-4625 (inbox_store) |
| LLR-4408.16 | TC-4626 (inbox_store) |
| LLR-4408.17 | TC-4627 (inbox_store) |
| LLR-4408.18 | TC-4628 (inbox_store), TC-4628b (inbox_store) |
| LLR-4408.19 | TC-4629 (inbox_store) |
| LLR-4408.20 | TC-4650 (inbox_store) |
| LLR-4409.1 | TC-4631 (capture_view) |
| LLR-4409.2 | TC-4632 (inbox_store) |
| LLR-4409.3 | TC-4633 (inbox_store) |
| LLR-4409.4 | TC-4634 (capture_view) |
| LLR-4409.5 | TC-4635 (inbox_store) |
| AT-4401 | AT-4401 (capture_view) |
| AT-4402 | AT-4402 (capture_view) |
| AT-4403 | AT-4403 (capture_view) |
| AT-4404 | AT-4404 (capture_view) |
| AT-4405 | AT-4405 (capture_view) |
| AT-4406 | AT-4406 (capture_view) |
| AT-4407 | AT-4407 (capture_view) |
| AT-4408 | AT-4408 (capture_view) |


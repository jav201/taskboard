# inc93 — the two states no key could reach, reached; and the round that pressed the keys

Batch `rework-10`, increment 3 of 3, and the batch close.

## §0 — the rulings, verbatim

Rulings (orchestrator, 2026-09-07, on the operator's delegation):

- **A frame has no focus; the round presses keys.** The instrument is `App.run_test()` + `Pilot` on
  the widget slice, per language, driving a fixed script and capturing the screen after each key
  through the same `cell_grid` the raster uses.
- **L12 corrected:** the match channel in grey is weight or decoration where the kit declares it, and
  the grey test reads the sidecar's `bold`/`underline` flags, not colour tokens; a kit is hue-only in
  grey only if its match run carries neither.

And the increment's own brief: *fix the failures inc91 recorded that are defects (focus not visible in
some language; a modal that does not restore the page byte-identically; an invalid state that does not
draw live what the sheet draws; a match that the palette does not show), each with a law over the
eleven and teeth; doctrine gets a citation. Then write `PROTOTYPE-inheritors-6.md`.*

## §1 — cause

inc91 ran the six-step script in all eleven languages and recorded **44 of 66 laws holding**. The
twenty-two that failed were K5 and K6, in every language, and neither failure was language-shaped:

1. **The widget had no live TYPED seat.** `textfield_block`'s own docstring had said so since pass 53
   and refused to invent one: *"nothing in the engine is TYPED."* Measured, that refusal cost the
   corpus a state **all eleven kits draw** at `S2` and whose two walls inc85 moved into `ink` in every
   one of them because a refusal is a MEANING MARK. Eleven languages drew a refusal nobody could
   provoke.
2. **The command palette was byte-identical in all eleven.** Its eight rows, run-encoded, collapsed to
   ONE distinct block: Textual's `#141f27` slab, its `#0e395a` cursor row, and a `bold underline`
   highlight on a colour no kit declares. On ledger — the corpus's one light-paper kit — that was a
   night-mode slab laid across the middle of the page.

Two of the brief's four named defects **did not occur**: focus is visible in all eleven (K2 held), and
`escape` restores the page cell for cell in all eleven (K4 held). They are not fixed because there was
nothing to fix, and §5 says what the round found in their place instead.

## §2 — mechanism

### The palette speaks the language, and the rule is DERIVED from `MATCH_STYLE`

`Kit.palette()` is new and `Kit.tcss()` appends it, so the rules travel with the kit rather than with
the theme. The match highlight's channel and ink come out of **the same string `Kit.match` reads**, so
a kit that changes its match channel changes the palette with it and the sheet and the app cannot
disagree about what a match looks like.

`CommandList` ships `text-style: bold` on every option. That is now `none`: weight was the palette's
baseline, and **seven of the eleven kits carry their match on weight** and would have been shouting
into a shout.

### The live typed seat is a value the model already had

The threshold is the one number in the engine a user changes and it has had keys since `ConfigScreen`
existed (`[` and `]`). inc93 gave it a keyboard: a digit opens a field, the field takes what is typed,
and `tab` validates. `12/99/26` is not an integer, so the field draws `KIT.textfield(..., LG.INVALID)`
— each kit's own walls in the tier `field_wall_tone` names — **and the refusal outlives the blur**,
because a field that only looked wrong while the caret was in it is a field nobody sees refuse.

Three decisions in it are worth naming:

- **Typing starts on a DIGIT and on nothing else**, and that was learned the hard way — see §5.1.
- **The layout question is asked on the STEADY row.** `_wide()` masks the typed buffer, because a
  field is wider than the slider it replaces and the radio set would otherwise collapse to a stepper
  under the caret.
- **Leaving the row abandons the edit, refusal included**, so the invalid state is a property of the
  SEAT and not of the screen.

### The script learned to walk to the seat, and that is a finding

`K5`'s keys gain two `down` presses. **Only two of the six signals have a threshold at all**, and the
cursor opens on one that does not; a script that typed at the first row would have measured a row with
no seat and called the app broken.

### The K5 law was wrong twice, in opposite directions, and both were measured

| version | what it asked | what it did |
| --- | --- | --- |
| character scan | *is any cell anywhere drawing the wall glyph in the wall tone* | **passed on instrument (5 cells) and industrial (2)** on a screen with no field — `⠶` and `▐`/`▌` are those kits' chrome. `spec.md` §23.3.1 one instrument out |
| wall + PAPER + wall | `field_wall_tone`'s own doctrine: the paper stays in `dim` | **found nothing at all.** A field showing an eight-character value in an eight-cell window draws NO PAPER: the shipped frame is one run, walls and value alike in `ink`. The clause describes an EMPTY field and the seat under test is a FULL one |
| wall + THE VALUE + wall | the glyphs the language declares, the tier the method names, and the bytes the user said | binds three things at once and cannot be satisfied by chrome, **because no kit's chrome spells `12/99/26`** |

## §3 — the limit inc93 found and did not fix

`reverse` does not reach the command palette, and it is **Textual's limit and not any language's**.
`Widget.get_visual_style(..., partial=True)` builds its `VisualStyle` from five flags — `bold`, `dim`,
`italic`, `underline`, `strike` — and `reverse` is not among them; an opaque `background` in a partial
style resolves to **transparent** by that same function's own blend
(`background.blend(tint, 1 - tint.a)` with `a == 1`). Both were measured, not read:
`prototypes/out/_probe_rev.py` set `text-style: reverse` and `background: <ink>` on
`command-palette--highlight` and neither changed anything but the foreground.

So industrial, darkside and solari get their match **ink** and not their **plate**:

```
industrial  reverse {accent}  #ff623b on the row's ground   a distinct hue, no plate
darkside    reverse {mut}     #757575 in a body of #f5f5f5  QUIETER than the text it stands in
solari      reverse {ink}     #f0ede4 in a body of #f0ede4  INDISTINGUISHABLE
```

**Recorded and not faked.** Giving them a second channel here would be the app choosing a channel the
kit did not declare, which is what the *match tier by channel* ruling (`rework-7a`, inc73) forbids in
as many words. `PALETTE_CANNOT_REVERSE` is the roster and it has four clauses of teeth, including the
one that asserts solari's match ink equals the ink of the row it stands in.

## §4 — law and teeth

| law | ×11? | what it binds |
| --- | --- | --- |
| `test_the_invalid_state_is_reachable_by_a_key_in_every_language` | ×11 | the kit's own walls around the value the script typed, in the tier `field_wall_tone` names, drawn EXACTLY ONCE, on the screen the script says |
| `test_the_palette_paints_the_match_in_the_kits_own_ink` | ×11 | the match ink on the row the query found, and for the eight text-attribute kits the declared channel, at exactly the query's length |
| `test_the_palettes_one_missing_channel_is_the_frameworks_and_is_named` | roster | the roster is exactly the `reverse` kits; none gets a plate; all three keep the ink; and **exactly one — solari — is indistinguishable** |
| `test_the_focus_ring_is_a_ground_in_eleven_and_a_glyph_in_only_eight` | roster | every kit changes the ground of the seat that takes focus; the kits that change NO GLYPH are exactly `FOCUS_RIDES_COLOUR_ALONE`; the other eight change exactly ONE |
| `test_the_one_modal_the_app_has_breaks_the_law_the_sheets_obey` | roster | the `K3` grouping is `MODAL_TEXT_GROUPS`; there are FEWER groups than languages; inside a group the COLOURS still differ; and the eleven `S4` sheets do NOT collapse |

**Teeth** — `test_the_two_seats_inc93_fixed_are_measured_and_not_assumed`. Both measurements are run
over `K1`, the page as it opens: no invalid field, no result row. **And the second arm is why the
match law is row-bound.** Written frame-wide it went RED on swiss: its match ink is `alert`, and the
aperture spends `alert` bold on an overdue chip, so a page where nothing had been searched carried a
"match run". A match ink is not a private colour and the SEAT is what makes it a match.

The focus law carries its own vacuity arm (the measurement over `K1` against itself must find
nothing), and the modal law's fourth clause is the sheets' own non-collapse.

## §5 — what was found by looking

1. **The first version of the typed seat ATE THIS SCREEN'S OWN `r`, and the key round could not see
   it.** Taking any printable character the moment the cursor sat on a row with a threshold swallowed
   the refresh key: the button stopped pressing and `verify_language.py`'s drive-check went red in
   **four clauses at once**. No step of the key script presses `r`, so the instrument this batch built
   was blind to the defect the increment introduced, and the older instrument caught it. Typing now
   starts on a digit and on nothing else.
2. **A live text seat made a doctrine sentence false in three files at once.** `textfield_block`'s
   docstring, `verify_language.py`'s blink clause and the clause's own assertion (`"textfield" not in
   inspect.getsource(ConfigScreen)`) all encoded *"this app has no live text seat"*. The clause is
   rewritten to bind what is still true — the BLINK is gallery-only, because the live seat calls
   `textfield` with no `tick` and no `caret_on` — and the assertion now requires the field to be there.
3. **And the rewritten clause read English instead of code, once.** Its first form looked for `"tick"`
   in `ConfigScreen`'s source and found it in the motion player's prose (*"a recompute per tick"*). It
   asks for `tick=` now.
4. **Focus in this app is ONE CSS rule and ONE token, and the token fails in two opposite ways.**
   `themes.tcss()` has `.tile:focus { background: {panel}; border-left: {sel} {accent}; }` and eleven
   values. Measured between `K1` and `K2` on the seat that takes focus: eight kits move **one glyph**
   (the border cell) and a row of grounds; **ledger, solari and blueprint move none** — `sel: none`,
   so focus is colour alone, against this corpus's own *"states may never ride colour alone"* and
   against ruling L2. And the same token fails the other way on the hero, whose ring is a full border:
   **letting go of focus redraws the hero's content in eight of eleven, up to 342 cells.** No kit
   declares a focus mark; there is no `Kit.FOCUS` as there is a `Kit.CUR`.
5. **The one modal the app has breaks the law the sheet sweep enforces.** `render.py`: *"for each
   screen, no two languages may render byte-identically."* The eleven `K3` frames are **four texts**,
   and the largest group has **five members** — corgi, swiss, industrial, darkside and prism draw the
   same 32 rows character for character. The cause is structural: `HelpScreen` composes the App's own
   `BINDINGS` through `LG.mark()`, so a kit reaches the modal only where it TRANSFORMS TEXT.
6. **The palette's prompt is the only cell in 66 key frames that neither a kit nor a screen chose.**
   `U+1F50E`, two columns wide, absent from the measured face. It is coloured by `Kit.palette()` and
   its GLYPH is not touched: giving it a language is a new contract seat (`Kit.SEARCH`) in all eleven.
7. **`nord`'s invalid wall is a question mark, and `?` is this app's help key.** `field_form(INVALID)`
   returns `('?', ' ', '?')`: the only refusal mark in the corpus that asks a question, and the same
   character the footer prints two rows below as `? Keys`. In the round it is one of three `rehacer`
   on `K5`.
8. **`solari`'s invalid wall points at the wrong axis.** `═` is a horizontal double rule used as a
   vertical wall; at 9×19 the value floats between two short dashes.

## §6 — the round: `PROTOTYPE-inheritors-6.md`

**keep 33 · nota 12 · rehacer 21**, over 66 frames.

| paso | keep | nota | rehacer | the dominant cause |
| --- | --- | --- | --- | --- |
| `K1` initial | 0 | 8 | 3 | the hero's ring is a border: it recomposes the content, or it does not exist |
| `K2` focus | 8 | 0 | 3 | three kits declare `sel: none` and focus is colour alone |
| `K3` modal | 1 | 0 | 10 | four texts for eleven languages; the largest group has five |
| `K4` escape | 11 | 0 | 0 | the restoration is exact in all eleven |
| `K5` invalid | 5 | 3 | 3 | shared out by kit: the cell of the wall |
| `K6` match | 8 | 1 | 2 | shared out by kit: the three `reverse` |

**Only `K5` and `K6` are shared out by language.** The other four steps have one verdict per CAUSE,
and the four causes live in `themes.tcss()`, in `HelpScreen` and in Textual. A round that judged
eleven languages found that **four of its six columns are not about the languages**.

The page: `C:\Users\jjgh8\.claude\jobs\85046efb\tmp\gal\ronda-teclas.html`, built by
`build_ronda_teclas.py` from the round document and the 66 PNGs. **4 167 157 bytes = 3.97 MB**, under
the 10 MB budget. Verified in the browser and not in the file (patchright headless, `file://`): **66
`<img>`, all 900×608 natural and painted at 900** (1:1, no CSS scaling), 264 radios in 66 independent
groups, 66 note fields, **zero console errors, zero failed requests, zero external URLs, zero
em-dashes**, no horizontal document scroll at 1280 or 700, the wide frames scrolling inside their own
container, the explicit theme override winning in both directions, and the matrix chip jumping to the
frame it names.

## §7 — files and frames

| file | change |
| --- | --- |
| `taskboard/language.py` | `Kit.palette()`, appended by `Kit.tcss()` |
| `prototypes/widget_slice/app.py` | `ConfigScreen._typed` / `_refused`, `_threshold_cell`, `on_key`, `_commit`, `_wide` masking, `action_move` clearing; `textfield_block`'s docstring corrected |
| `prototypes/components/keys.py` | `REFUSED`, `PALETTE_CANNOT_REVERSE`, `field_seats` taking the value, `K5`'s two `down`s, the channels report |
| `tests/test_components.py` | `KEY_REFUSED`, `PALETTE_CANNOT_REVERSE`, `FOCUS_RIDES_COLOUR_ALONE`, `MODAL_TEXT_GROUPS`, `_focus_channels`; five laws and two teeth, two record laws removed |
| `prototypes/verify_language.py` | the blink clause rewritten: the field exists now, the LOOP is what stays gallery-only |
| `prototypes/components/PROTOTYPE-inheritors-6.md` | **new, 66 blocks** |
| `.fast-dev-flow/spec.md` | **§25** — the batch record |

**Five source files, which is the cap.**

**Frames changed: `K5` and `K6` in all eleven — 22 frames, 88 artefacts** (22 `.txt` + 22 `.svg` +
22 `.png` + 22 `.json`). `K1` through `K4` are byte-identical to inc91's in every picture; **four more
`.json` differ in `settle_reads` alone**, which is the field `UNPINNED` names and the one thing in
this corpus that changes on disk without anything having moved. **Zero component sheets, zero board grids, zero rasters:**
`render.py`, `raster.py`, `second_width.py`, `matrix.py`, `collision_census.py` and
`capture_languages.py` were all re-run and `git status --porcelain` shows nothing under
`prototypes/components/*_S?.*` or `prototypes/gallery/`.

**Gallery 30–51: none changed byte-wise** in any of the three increments, read off
`prototypes/components/` (the `.txt`): no sheet moved in `rework-10` at all.

## §8 — deviations, named

- **Two of the brief's four named defects did not occur.** Focus IS visible in all eleven and `escape`
  DOES restore the page cell for cell. Nothing was fixed for either; what the round found in their
  place — the ring's two opposite failures and the modal's four texts — is recorded with teeth
  (§5.4, §5.5) and handed to the round rather than fixed inside an increment that was not briefed for
  it.
- **The live seat is a THRESHOLD and the brief says a date field.** The app has no date anywhere in
  its model. The one value the engine already had is a signal's threshold, and it already had keys.
  Inventing a date setting for a widget that has none would be the demo `textfield_block` refused; the
  keystrokes are the brief's own (`12/99/26`) and they are refused by this seat for the same reason
  they would be refused by a date field.
- **`K5`'s script gained two `down` presses**, which changes the frame inc91 shipped for that step.
  Declared in `keys.py`, restated in the suite's `KEY_SCRIPT`, and the reason is a finding (§2).
- **The `reverse` kits are a recorded limit and not a fix**, §3.
- **`settle_reads` remains outside the reproducibility bargain**, so a handful of `.json` sidecars
  differ on disk between runs while none of the 198 pictures does. Named by `UNPINNED`, masked by the
  cross-process check, and left in the record because it is the honest answer to *"how settled was
  this frame"*.

## §9 — gates

```
pytest -q                1560 passed, 1 failed, 2 skipped in 49.14s
                         (inc92 1537 total -> 1561, +24: 11 invalid + 11
                          palette + 1 limit + 1 teeth + 1 focus + 1 modal,
                          less the 2 record laws inc91 shipped.  The one failure is
                          test_win_clipboard_roundtrip, environment-coupled,
                          reported and not counted, not touched)
keys.py                  66 of 66 laws HOLD (was 44 of 66)
                         264 artefacts identical across two PROCESSES
                         (66 .txt + 66 .svg + 66 .png + 66 .json)        exit 0
verify_language.py       ALL PASSED                                      exit 0
                         -- and one FLAKE, named: the clause "nord's BOARD
                         is identical either way" (two board captures
                         compared) failed in one run of four with the same
                         tree and passed in the three around it.  It is the
                         ~10 % loud failure `settle`'s own docstring predicts
                         for the columns branch.  Reported, not smoothed over.
render.py                66 .txt + 66 .svg / 330 pairs / 0 hand-drawn     exit 0
                         -- and nothing changed on disk
raster.py                132 PNGs identical across two PROCESSES
                         (66 colour + 66 grey)                           exit 0
legibility.py            1202 lines · byte-identical across two PROCESSES exit 0
second_width.py          0 rows cut in 0 frames · 330 pairs distinct     exit 0
matrix.py                refusals [] for all eleven                       exit 0
collision_census.py      TOTAL 23 · homoglyph rows 22 · both self-checks
                         green · zero collisions: darkside                exit 0
capture_languages.py     22 grids identical across two processes ·
                         no two boards identical                          exit 0
export_to_skill.py       11 languages round-trip; every token, doc and family
                         verified; captures **0 written / 66 already
                         identical**; SURFACES.md 11 postures.  `languages.py`
                         itself is rewritten (inc92's four docstrings and
                         inc93's `Kit.palette`).  **The skill repo is NOT
                         committed from here.**             exit 0
gallery 30-51            **none changed**, checked two ways: no `.txt` under
                         `prototypes/components/` moved in the whole batch,
                         and `git status` in the skill repo shows nothing
                         under `assets/gallery/`.
```

`BELOW_THE_FLOOR`, old → new: **4 → 4, unchanged.** No seat moved; a stylesheet and a screen did.

## §10 — pending / next

Batch `rework-10` is closed; `spec.md` §25 is the record. What goes back to the round, all of it in
`PROTOTYPE-inheritors-6.md` §4:

- **The focus ring**, which is one CSS rule and a `sel` token with two opposite failure modes, and
  which passes through no kit contract at any point. `FOCUS_RIDES_COLOUR_ALONE` holds the three.
- **`HelpScreen`**, whose eleven renderings are four texts. The fix is the screen drawn through the
  kit the way `screens.s4` draws the sheets' confirm.
- **`Kit.SEARCH`**, the contract seat the palette's prompt would need.
- **`reverse` in the palette**, a framework limit with three kits behind it and one (solari) whose
  match is invisible because of it.
- **Four kit cells** the round objected to by name: `naught ◑` (a tenth circle in an alphabet declared
  exhausted at nine), `nord ?` (a refusal that asks a question, and the app's own help key),
  `solari ═` (a horizontal rule used as a vertical wall), `blueprint ╲ ╲` (walls that do not mirror).
- **The confirm nobody can open.** The app binds no delete, so the band this round judged is a keymap.
  What the sheets draw at `S4` — the irreversible question, the danger form, the confirming arm — has
  no key at all.

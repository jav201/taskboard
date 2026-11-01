# Code-Wire prototype — group T (taskboard/suggest.py) — Inc K

Differences from `graph-baseline.cw.md` (545c18a) only. `taskboard/suggest.py` is a NEW file, so every node here is new; no baseline node changes. Group T owns the deterministic TF-IDF suggester of K-3 (R0-7): the word reducer, the documents (one per live project of every readable board), the scorer with its "why" words and board chip data, the confidence cue, and the option list with the `+ new project` sentinel. The module is pure: it imports only the standard library (`math`, `re`, `unicodedata`, `collections.Counter`, `typing.NamedTuple`, `pathlib.Path`), never `app`, `inbox`, a file or the network. It reads the `Board`, `Project`, `Task` and `Mark` objects it is handed by attribute only (`board.projects`, `board.tasks`, `board.path`, `p.id`, `p.name`, `p.color`, `p.archived`, `t.project_id`, `t.title`, `t.notes`, `t.archived`, `t.milestone`, `t.mark`, `mark.name`), so it needs no `models` import either.

Design source: `prototypes/capture_round/suggest.py` (tfidf method). Kept from it: STOP, WORD_RE, fold/stem/words, the idf formula, cosine, the one-word halving, the "why" order, the cuts. Changed from it, by the commission (R0-7) and the R2 rulings: the weights are integers name 3, title 2, `@handle` in notes 2, mark name 1, other note words 1 (the proto's floats had the same values; integers keep the tf Counter exact); the documents come from `board_lanes` lanes and the app's marks dict (not `board.marks`); Doc carries the board path and lane/position instead of the proto's `order = bi * 1000 + pi` and `text`; the tie order is (−score, lane, project name, position) (the proto had no position term); the note is cut to its first 10 000 characters BEFORE folding (LLR-4403.22); `options` is new (at most 3 entries, `+ new project` only as a weak top, R2 F-11); the trigram and overlap baselines, `split_topics` and `as_task` are NOT carried (scope R0-11: the pad parse is G-S's `note_parts`/`note_task`).

E2 correction pass (round 0b, `03-pdr-rulings.md`): P-T-1 (`NOTE_CHARS` lives here), P-T-2 (a df-0 stem weighs 0), P-T-3 (name ties by `casefold`, then the stored name), P-T-4 (G-V passes the note's scored text: `note_task` title + "\n" + notes, image lines left out) and P-T-5 (`DOC_CHARS` = 100 000 per document) applied below. The ruled order and cap were re-executed (`%TEMP%\incK-E2-probe\run_ruled.py` = `run.py` over `ref_suggest.py` with the P-T-3 sort key; `e2c.py`, `cap.py`): every earlier example below is unchanged, and the TC-4486 digest is still `d694943ce6d21f09` under PYTHONHASHSEED 0, 1, 2.

E3 round 1 (`03-pdr-rulings.md` §Round 1, LED-2026-11-01-incK.4, `03-e3-corrections.md`): ARCH-6 — `corpus` returns a `Corpus(docs, idf)`; idf, each document's tf·idf vector and its norm are computed ONCE per build and `suggest(note, corpus)` only reads them (new LLR-4403.29; G-V scores on the debounce, LLR-4403.30/31); ARCH-5 — TC-4482's control is the deterministic `"x" × 9 995 + " eval harness"` arm and TC-4486 compares two subprocesses (`PYTHONHASHSEED` 0 and 1). Re-executed against the corrected design (`%TEMP%\incK-e3fix\suggest_fix.py`, `nc4482.py` over the ruled reference): the 7 probe notes give the same hits as the per-call computation, digest `d694943ce6d21f09` under seeds 0 and 1; `_idf` is called once per build; at 300 documents (p4_cost's worst shape) a call takes 2.7 ms instead of 139.6 ms.

### Fixture F (synthetic; every example below was EXECUTED)

> All numbers and "why" lists below were produced by running a scratch reference of exactly this design (`%TEMP%\incK-T-probe\ref_suggest.py`, driven by `run.py`, `more2.py`, `hand.py`; cwd = the worktree, `taskboard.__file__` printed = `C:\Users\jjgh8\Github\taskboard-wt\capture-proto\taskboard\__init__.py`; real `taskboard.models.Board/Project/Task` and `taskboard.marks.Mark` objects, never saved; nothing written in the repo). Run on 2026-11-01 under `PYTHONHASHSEED` 0, 1 and 2: identical digest `d694943ce6d21f09`.
> Marks dict M = `{"payment": Mark("payment", "Payment", "▲", "amber"), "release": Mark("release", "Release", "★", "cyan")}` (the shape of `app.marks.marks`).
> Lane 0 `("Client A", "sky", A, "")`, A.path `S/boards/client-a/board.json` (the open board). Projects in order: `Eval harness` (id `pe`, colour "blue", position 0), `Pilot rollout` (id `pr`, "indigo", position 1). Tasks in order:
> - `Question bank` (pe), notes `40 questions; each needs a key from @username_subject`
> - `Judge rubric` (pe), no notes
> - `Eval report v1` (pe), milestone, mark `release`
> - `Pilot store list` (pr), notes `six stores, two per region`
> - `Steering committee` (pr), notes `@username_subject chairs; demo hybrid search on pilot stores`
> - `Invoice October` (pr), milestone, mark `payment`
> - `Loose idea zebra` (no project)
> - `Old golden set` (pe), archived
> Lane 1 `("Course", "violet", C, "")`, C.path `S/boards/course/board.json`. Project `Module 4 · Volumes` (id `pv`, "violet", position 0). Tasks: `Volume oracle script` (pv) notes `check on Windows`; `Bind vs named volumes page` (pv) notes `the oracle prints the inode`; `Module 4 publish` (pv), milestone, mark `release`.
> Documents of F (N = 3), tf exactly:
> - `Eval harness`: eval 5, harnes 3, questi 3, bank 2, each 1, key 1, @username_subject 2, judge 2, rubric 2, report 2, releas 1
> - `Pilot rollout`: pilot 6, rollou 3, store 4, list 2, six 1, region 1, steeri 2, commit 2, @username_subject 2, chair 1, demo 1, hybrid 1, search 1, invoic 2, octobe 2, paymen 1
> - `Module 4 · Volumes`: module 5, volume 7, oracle 3, script 2, check 1, window 1, bind 2, named 2, page 2, print 1, inode 1, publis 2, releas 1
> idf: df 1 → ln(4/2) + 1 = 1.6931471805599454; df 2 (`@username_subject`, `releas`) → ln(4/3) + 1 = 1.2876820724517808.
> Hand values of N1 = `Golden set: 12 questions still have no answer key ask @username_subject` against `Eval harness`: note stems golden, set, questi, answer, key, @username_subject (12 a number; still, have, no, ask stop words); query weights questi 1.693147, key 1.693147, @username_subject 1.287682, golden/set/answer 0 (held by no document); |q| 2.718753, |d| 13.533744, dot 14.783240 (shares questi 8.600242, @username_subject 3.316250, key 2.866747), cosine 0.401774 → score 0.4018.

### Scoring algorithm of suggest (precise)

> 0. Once per build, in `corpus` (ARCH-6): idf = `_idf(docs)`; for each doc, `vec` = {s: tf[s] × idf[s]} (tf order) and `norm` = sqrt(Σ vec²) or 1.0; returned as `Corpus(docs, idf)`.
> 1. corpus.docs empty → `[]`. `note` is the scored text G-V passes (`nt.title + "\n" + nt.notes` of `inbox.note_task`, P-T-4). text = note[:NOTE_CHARS] (a str slice, before any fold; NOTE_CHARS = 10 000).
> 2. idf = `corpus.idf` (not recomputed). nw = words(text). q = Counter of the stems of nw in note order; surface[stem] = the first surface word of that stem in note order.
> 3. qv[s] = q[s] × idf.get(s, 0.0) — a stem no document holds weighs 0 (P-T-2). |q| = sqrt(Σ qv²) or 1.0.
> 4. For each doc in docs order: dv = doc.vec, |d| = doc.norm (set at the build; an empty document scores 0); share = {s: qv[s] × dv[s] for s in qv if s in dv} (dict in qv's order); cosine = Σ share / (|q| × |d|); × 0.5 when len(share) == 1; score = round(…, 4). score ≤ 0 → no hit. why = [surface[s] for s, v in sorted(share.items(), key=(−v, s))].
> 5. hits sorted by (−score, doc.lane, doc.project_name.casefold(), doc.project_name, doc.position) (ruled P-T-3: case-folded name first, then the stored name, then position); keep score ≥ LOW; first MAX_HITS (3).
> No `set` is iterated for any order or any sum (the sums run over insertion-ordered dicts), so the result is independent of `PYTHONHASHSEED` (TC-4486). Cost: O(len(text[:10 000]) + Σ over docs of the note's stems) per call — the O(Σ |tf|) idf and vector work is paid once per build (ARCH-6); G-V's hit cache (LLR-4403.21) calls it once per distinct note text, and only on the debounce (LLR-4403.30).

## Nodes

fold
req: LLR-4403.1
in: str s
out: str folded
func: `unicodedata.normalize("NFKD", s or "")` with every combining character dropped, then `.lower()`. Never raises; `None` or "" → "".
module: taskboard/suggest.py
examples: (TC-4461) s "Golden SET: Café" → folded "golden set: cafe"
examples: (TC-4461) s "clés" → folded "cles"

stem
req: LLR-4403.2
in: str w
out: str stemmed
func: a word starting with `@` is returned unchanged; else a final `ies` becomes `y` when len(w) > 4, else a final `s` not preceded by `s` is dropped when len(w) > 3; the result is cut to its first 6 characters.
module: taskboard/suggest.py
examples: (TC-4462) w "questions" → stemmed "questi"
examples: (TC-4462) w "stories" → stemmed "story"
examples: (TC-4462) w "class" → stemmed "class"
examples: (TC-4462) w "@username_subject" → stemmed "@username_subject"
examples: (TC-4462) w "harness" → stemmed "harnes"; w "volumes" → stemmed "volume"; w "pies" → stemmed "pie"

words
req: LLR-4403.1, LLR-4403.2
in: str text
out: list[tuple[str, str]] pairs
func: implements the interface contract: for each match of WORD_RE (`@[a-z0-9]+(?:[._\-][a-z0-9]+)*|[a-z0-9]+`) in fold(text), in text order, keep a handle (starts with `@`) always, any other word only when len ≥ 3, not in STOP and not `isdigit()`; each kept word as (stem(word), word). Colour markers need no stripping: their codes are one letter (`::b::` → "b", dropped by length), and `==`/`!!`/`++` are not word characters. Never raises.
module: taskboard/suggest.py
examples: (TC-4461) text "Golden SET: 12 Questions @username_subject de la Café" → pairs ("golden", "golden"), ("set", "set"), ("questi", "questions"), ("@username_subject", "@username_subject"), ("cafe", "cafe") — `5` pairs, no "12", no "de", no "la"
examples: (TC-4461) text "::b:: Golden set :: ==late== img: board-0938.png" → pairs ("golden", "golden"), ("set", "set"), ("late", "late"), ("img", "img"), ("board", "board"), ("png", "png")

corpus
req: LLR-4403.3, LLR-4403.4, LLR-4403.5, LLR-4403.23, LLR-4403.24, LLR-4403.25, LLR-4403.27, LLR-4403.29, HLR-4403
in: list[tuple[str, str, Board?, str]] lanes; dict marks
out: Corpus corpus
func: for lane index li, lane (board_name, board_colour, board, state) in lanes order: board None → skipped (G-V counts those for LLR-4403.20); for position pi, project p in board.projects order (archived ones keep their position): p.archived → skipped; else tf = Counter(): each stem of words(p.name) += 3; for each task t in board.tasks order with `t.project_id == p.id` and not t.archived: each stem of words(t.title) += 2; each stem of words(t.notes) += 2 when it starts with `@`, else += 1; when `t.milestone is True` and t.mark and `t.mark in marks`: each stem of words(marks[t.mark].name) += 1 (a hidden mark counts too). Document cap (P-T-5, LLR-4403.27): each project starts a budget `left = DOC_CHARS` (100 000); every field is fed in the order above (p.name; then per task t.title, t.notes, the mark name) as `piece = field[:left]`, `left -= len(piece)`, and only `piece` is tokenised (a word cut at the budget edge counts as the shorter word it became); once `left` is 0 nothing more is read. Doc(lane=li, board_name, board_colour, board_path=board.path, project_id=p.id, project_name=p.name, project_colour=p.color, position=pi, tf, vec, norm), vec and norm filled after all docs are built: idf = `_idf(docs)` once, then step 0 of the algorithm; returns `Corpus(docs, idf)` (ARCH-6, LLR-4403.29). A task with no project, an unknown project id or an archived project joins no document. A project whose words are all dropped is still a Doc (empty tf; it counts in N and never scores). Pure: reads no file, writes nothing; G-V calls it on open (LLR-4403.23) and again after each dump or undo that changed a board (LLR-4403.24).
module: taskboard/suggest.py
examples: (TC-4464) one lane, project "Eval harness" with one task "Answer key", notes "ask @username_subject key", milestone, mark "payment", marks M → tf "eval": `3`, "harnes": `3`, "answer": `2`, "key": `3`, "@username_subject": `2`, "paymen": `1` and nothing else (`6` stems; "ask" a stop word)
examples: (TC-4463) fixture F with an archived project "Module 3 · Images" added to Course → docs `3` (not 4)
examples: (TC-4465) fixture F (task "Loose idea zebra" has no project) → no doc holds "zebra"; the archived task "Old golden set" → no doc holds "golden"
examples: (TC-4483) fixture F → docs "Eval harness" (lane `0`, position `0`), "Pilot rollout" (lane `0`, position `1`), "Module 4 · Volumes" (lane `1`, position `0`, board_path "S/boards/course/board.json", board_name "Course", board_colour "violet")
examples: (TC-4483) lanes Client A (A) and ("Gone", "pink", None, "file missing") → docs `2` (only Client A's)
examples: (TC-4484) fixture F plus a task "Rotation plan" in Eval harness (the board as read after the dump) → Eval harness tf holds "rotati": `2` and "plan": `2`
examples: (TC-4485) one lane whose board has 0 projects → corpus docs `[]`, idf `{}`
examples: (TC-4489) fixture F → `_idf` called `1` time for the build; then 7 suggest calls → still `1` (executed, suggest_fix.py); Eval harness's norm 13.533744 (as the hand value of |d|)
examples: (TC-4485) a project "Q&A" with no task, placed before F's lanes → a Doc with tf `{}`, N = `4`, and N1 still scores only "Eval harness" (0.4044)
examples: (TC-4487) one lane, project "Ledger alpha" with one task "Audit log", notes "audit " × 20 000 + "zebra" (120 005 characters) → tf {"ledger": `3`, "alpha": `3`, "audit": `16665`, "log": `2`} exactly, no "zebra"; corpus in 0.0175 s (< 1.0 s); executed (cap.py)
examples: (TC-4487) fixture F → the same tf for all 3 documents as without the cap

_idf
req: LLR-4403.6
in: list[Doc] docs
out: dict[str, float] idf
func: df = for each doc, +1 for each distinct stem of its tf; idf[s] = `math.log((N + 1) / (df[s] + 1)) + 1.0`, N = len(docs). Only stems some document holds are keys. Called by `corpus` only, once per build (ARCH-6).
module: taskboard/suggest.py
examples: (TC-4466) fixture F → idf "questi" 1.6931471805599454 (df 1), "@username_subject" 1.2876820724517808 (df 2), "releas" 1.2876820724517808 (df 2); `3` docs
examples: (TC-4466) five projects "Ledger alpha" … "Ledger echo", each one task "Audit trail" → idf "ledger" `1.0` (df 5 = N), "alpha" 2.098612

suggest
req: HLR-4403, LLR-4403.6, LLR-4403.7, LLR-4403.8, LLR-4403.9, LLR-4403.10, LLR-4403.14, LLR-4403.15, LLR-4403.19, LLR-4403.22, LLR-4403.25, LLR-4403.26, LLR-4403.28, LLR-4403.29
in: str note; Corpus corpus
out: list[Hit] hits
func: the scoring algorithm in the note above (implements the interface contract): idf, vectors and norms read from the corpus, never recomputed (ARCH-6); first NOTE_CHARS (10 000) characters, sliced before fold; tf·idf cosine (a stem no document holds weighs 0, P-T-2); halved on exactly one shared stem; rounded to 4 decimals; score ≥ LOW (0.08); ordered (−score, lane, project name casefolded, project name, position) (P-T-3); `note` is the scored text (P-T-4: G-V strips the image lines through `note_task`; suggest.py imports no inbox); at most 3; why = the note's first surface word of each shared stem, largest contribution qv·dv first, ties by stem; `why` holds every shared word (G-V shows at most 3). Pure and deterministic; never raises; [] for no docs.
module: taskboard/suggest.py
examples: (TC-4474) note N1 "Golden set: 12 questions still have no answer key ask @username_subject" over F → hits `1`: "Eval harness" · "Client A", score `0.4018`, why "questions", "@username_subject", "key" (in that order)
examples: (TC-4467) note N1 against "Eval harness" → cosine 0.401774 (dot 14.783240 / (2.718753 × 13.533744)), score `0.4018`
examples: (TC-4468) note N1 against "Pilot rollout" (one shared stem "@username_subject") → cosine 0.075806, score `0.0379` (= 0.5 × cosine, rounded; not a hit); against "Eval harness" (3 shared stems) → score `0.4018`, not halved
examples: (AT-4402) note "Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png" over F → hits `1`: "Module 4 · Volumes" · "Course", score `0.668`, why "volume", "oracle", "script" (the image line's words img, board, png weigh 0: the same score without that line)
examples: (TC-4471) note "eval rubric for the oracle pilot" over F → hits "Eval harness" `0.4379` why "eval", "rubric"; "Pilot rollout" `0.1578` why "pilot"; ("Module 4 · Volumes" scored `0.0723` < LOW, absent)
examples: (TC-4472) note "store rubric" over F → hits "Pilot rollout" `0.1488` why "store"; "Eval harness" `0.0885` why "rubric"
examples: (TC-4472) note "Quote for the new client: contracts Q&A\ntwo weeks, fixed price" over F → hits `[]`
examples: (TC-4470) note "committee rubric" over F → hits `1`: "Eval harness" `0.0885`; "Pilot rollout" scored `0.0744` (below LOW) is absent
examples: (TC-4470) five projects "Ledger alpha" … "Ledger echo" on one board, each with task "Audit trail", note "ledger audit" → all five score `0.4698`; hits `3`: "Ledger alpha", "Ledger bravo", "Ledger charlie"
examples: (TC-4469) lane 0 "Zulu" holding project "Beta", lane 1 "Able" holding project "Alpha", each with one task "Ledger audit", note "ledger audit" → both `0.5571`; order "Beta" then "Alpha" (board order wins over name)
examples: (TC-4469) one board, "Beta" at position 0 and "Alpha" at position 1, same tasks → order "Alpha" then "Beta"; two projects both named "Beta" (ids "p0", "p1") → both `0.686`, "p0" (position `0`) first
examples: (TC-4469) one board, "alpha" at position 0 and "Beta" at position 1 → both `0.5571`, order "alpha" then "Beta" (plain str order would put "Beta" first); "beta" at position 0 and "Beta" at position 1 → both `0.686`, order "Beta" then "beta" (equal casefold, then the stored name); "beta" at 0 and "Alpha" at 1 → "Alpha" then "beta" (executed, e2c.py)
examples: (TC-4466) note N1 over F → "Eval harness" `0.4018` with the df-0 stems golden, set, answer weighing 0 (P-T-2; weighted ln(N + 1) + 1 they would give 0.2208)
examples: (TC-4488) F plus a lane ("Shots", "pink") holding a project "Png board" with no task: scored text "Shot\n" of the note "Shot\nimg: board-1.png" → hits `[]`; the raw part text would give "Png board" `1.0` why "board", "png" (the NC); the AT-4402 note's scored text "Volume lab fails on WSL\nthe oracle script expects /mnt/c" → "Module 4 · Volumes" `0.668` (as with the line)
examples: (TC-4475) the rail notes of graph-proto-V over F (executed, e2c.py, scored text): N1 "Golden set: 12 questions still have no answer key\nask @username_subject which stores count" → "Eval harness" · "Client A" `0.341` why "questions", "@username_subject", "key"; "Pilot rollout" · "Client A" `0.2869` why "stores", "@username_subject" → opts both (0.341 ≥ MID); N3 "Quote for the new client: contracts Q&A\ntwo weeks, fixed price" → hits `[]`
examples: (TC-4475) note "Steering deck: demo the hybrid search on pilot stores" over F → hits `1`: "Pilot rollout" `0.6444` why "pilot", "stores", "steering", "demo", "hybrid", "search"
examples: (TC-4479) note "Answer the region chair" over F → hits `1`: "Pilot rollout" `0.1488` why "chair", "region" → opts `None`, "Pilot rollout" (weak top)
examples: (AT-4407) note "Vendor call\n::b:: ask the vendor :: @username_subject" over F → "Eval harness" `0.0951` why "@username_subject"; "Pilot rollout" `0.08` why "@username_subject" → opts `None`, "Eval harness", "Pilot rollout"
examples: (TC-4482) note "eval harness " + "z " × 2 000 000 (4 000 013 chars) over F → the same hits as its first 10 000 characters: "Eval harness" `0.7077` why "eval", "harness"; executed in 0.0013 s (< 1.0 s) — not the control: uncapped it still scores in 0.51 s (ARCH-5, p5_nc)
examples: (TC-4482) note "x" × 9 995 + " eval harness" → only "eval" survives the cut: "Eval harness" `0.3128` why "eval" — THE control: uncapped → "Eval harness" `0.7077` why "eval", "harness" (executed, nc4482.py)
examples: (TC-4484) note "rotation" over F → hits `[]`; over F plus task "Rotation plan" in Eval harness → "Eval harness" `0.1179` (one shared stem, halved) why "rotation"
examples: (TC-4485) a corpus with docs `[]`, note "eval" → hits `[]`
examples: (TC-4486) the 7 probe notes over F, scored in 2 subprocesses under PYTHONHASHSEED 0 and 1 (`env -u NO_COLOR`) → identical (project id, score, why) lists, digest "d694943ce6d21f09" in both (executed, suggest_fix.py over the cached corpus; ARCH-5: in-process runs share one seed)
examples: (TC-4489) the 7 probe notes over F's corpus → the same hits as idf and vectors computed per call; over p4_cost's worst shape (20 boards × 15 projects × 40 tasks × 80 note words, 5 000-word vocabulary, seed 7: 300 docs, 734 619 stems) → corpus build 1 227 ms, suggest 2.69 ms per call (per-call idf: 139.6 ms), same hits (executed, suggest_fix.py)

level
req: LLR-4403.16
in: float score
out: int n
func: `3` when score ≥ HIGH (0.30), `2` when ≥ MID (0.16), `1` when ≥ LOW (0.08), else `0`; compares the rounded score as given.
module: taskboard/suggest.py
examples: (TC-4476) score 0.41 → n `3`; 0.30 → `3`; 0.2999 → `2`; 0.16 → `2`; 0.1599 → `1`; 0.08 → `1`; 0.0799 → `0`

bars
req: LLR-4403.16
in: float score
out: str cue
func: "▰" × level(score) + "▱" × (3 − level(score)); plain text, no style (G-V styles it). Always 3 characters.
module: taskboard/suggest.py
examples: (TC-4476) score 0.41 → cue "▰▰▰"; 0.20 → "▰▰▱"; 0.09 → "▰▱▱"; 0.05 → "▱▱▱"
examples: (TC-4476) fixture scores 0.4018 → "▰▰▰"; 0.1877 (note "Café questions clés", one stem, halved) → "▰▰▱"; 0.0885 → "▰▱▱"

options
req: LLR-4403.11, LLR-4403.12, LLR-4403.13, LLR-4403.25
in: list[Hit] hits
out: list[Hit?] opts
func: hits non-empty and hits[0].score ≥ MID (0.16) → `list(hits[:3])`; else `[NEW_PROJECT] + list(hits[:2])` (NEW_PROJECT is None, drawn by G-V as `+ new project`). At most 3 entries; the first is the top choice; never appends NEW_PROJECT after a strong top (R2 F-11).
module: taskboard/suggest.py
examples: (TC-4471) hits of "eval rubric for the oracle pilot" → opts "Eval harness" (0.4379), "Pilot rollout" (0.1578): `2` entries, no `None`
examples: (TC-4471) hits of "Café questions clés" → opts "Eval harness" (0.1877) only (0.1877 ≥ MID)
examples: (TC-4472) hits of "committee rubric" (best 0.0885) → opts `None`, "Eval harness"
examples: (TC-4472) hits `[]` (note "Quote for the new client: contracts Q&A\ntwo weeks, fixed price") → opts `None` only
examples: (TC-4473) hit scores 0.40, 0.20, 0.10 → opts the three hits; hit scores 0.12, 0.09 → opts `None`, then the two hits
examples: (TC-4473) hits of "store rubric" → opts `None`, "Pilot rollout" (0.1488), "Eval harness" (0.0885): `3` entries
examples: (TC-4485) corpus `[]` → suggest `[]` → opts `None` only

## Entities

[Data: suggest constants]
in: STOP set[str]; WORD_RE re.Pattern; W_NAME 3; W_TITLE 2; W_PEOPLE 2; W_MARK 1; W_NOTES 1; HIGH 0.30; MID 0.16; LOW 0.08; NOTE_CHARS 10 000; DOC_CHARS 100 000; MAX_HITS 3; NEW_PROJECT None
desc: module-level in suggest.py; STOP is the prototype's list verbatim (LLR-4403.1); the weights are ints (R0-7); `NOTE_CHARS` lives here, not in inbox.py (P-T-1 ruled); `DOC_CHARS` caps each document (P-T-5 ruled); never written at run time.

[Data: Doc]
in: NamedTuple(int lane, str board_name, str board_colour, Path board_path, str project_id, str project_name, str project_colour, int position, Counter tf, dict vec, float norm)
desc: as in graph-interfaces; lane = index in `board_lanes` lanes, position = index in `board.projects` (archived counted); board_name / board_colour are the lane's registry name and colour (the chip); board_path is `board.path` (G-V turns it into a DumpTarget); vec / norm set once per build (ARCH-6).

[Data: Corpus]
in: NamedTuple(list[Doc] docs, dict[str, float] idf)
desc: as in graph-interfaces; what corpus returns and suggest reads (ARCH-6).

[Data: Hit]
in: NamedTuple(Doc doc, float score, list[str] why)
desc: as in graph-interfaces; score already halved and rounded to 4 decimals; why holds every shared surface word, largest share first; the option None is NEW_PROJECT.

[Data: Board.projects]
desc: read by corpus: `id`, `name`, `color`, `archived`, list order.

[Data: Board.tasks]
desc: read by corpus: `project_id`, `title`, `notes`, `archived`, `milestone`, `mark`, list order.

[Data: marks.Directory.marks]
in: dict[str, Mark]
desc: `app.marks.marks` (id → Mark), passed to corpus by G-V; only `Mark.name` is read.

## Edges

[Data: suggest constants] ──▶ words
[Data: suggest constants] ──▶ corpus
[Data: suggest constants] ──▶ suggest
[Data: suggest constants] ──▶ level
[Data: suggest constants] ──▶ options
fold ──▶ words
stem ──▶ words
words ──▶ corpus
words ──▶ suggest
[Data: Board.projects] ──▶ corpus
[Data: Board.tasks] ──▶ corpus
[Data: marks.Directory.marks].name ──▶ corpus
corpus ──▶ [Data: Doc]
[Data: Doc] ──▶ _idf
_idf ──▶ corpus
corpus ──▶ [Data: Corpus]
[Data: Doc] ──▶ [Data: Corpus]
[Data: Corpus] ──▶ suggest
suggest ──▶ [Data: Hit]
[Data: Hit] ──▶ options
level ──▶ bars

### Seams

> Calls G-T makes into other groups: none. suggest.py imports no taskboard module; it reads the Board/Project/Task/Mark attributes listed in the head note on the objects G-V hands it.
> Calls other groups make into G-T (all from G-V, `taskboard/app.py`):
> - `corpus(lanes, app.marks.marks)` with `lanes = board_lanes(app)[0]` — in CaptureView on open (LLR-4403.23) and once after every dump, undo or review batch whose outcome changed a board (LLR-4403.24, ARCH-2/ARCH-6), each time from a fresh `board_lanes` (the other boards re-peeked). G-V clears its hit cache whenever it rebuilds the corpus.
> - `suggest(scored_text, corpus)` once per distinct note text while the corpus is unchanged, and from the rail only once the pad has been still for 1.0 s (LLR-4403.30) (G-V's cache, keyed by the Part text, LLR-4403.21); scored_text = `nt.title + "\n" + nt.notes` of `inbox.note_task(part.text)` — image lines left out (P-T-4 ruled; G-T stays free of inbox imports).
> - `options(hits)` → the note's option cycle (`alt+o` / `o` steps through it; `+ new project` = None). LLR-4403.18 ("no project shares a word") is `hits == []`; LLR-4403.19 uses `hits[0].doc.project_name` and `hits[0].why[:2]`.
> - `bars(hit.score)` for the cue; G-V styles the project name with `HEX[doc.project_colour]` and the board name with `HEX[doc.board_colour]` (LLR-4403.16).
> - `Doc.board_path`, `Doc.board_name`, `Doc.project_id` → G-V's DumpTarget and dump_note's project_id (G-S).
> G-S never calls G-T.
> Sample rail lines for the fixture (G-V draws them): N1 → `→ Eval harness · Client A ▰▰▰` / `why questions · @username_subject · key`; AT-4402's note → `why volume · oracle · script`.
> E2c cross-check (round 0b): every hit score and why list in graph-proto-V's examples equals an executed example of this file (G-V's N1, N2, N3, N4, N5 and AT-4407 notes; `rotation` after the TC-4484 dump = `0.1179`); G-V adopted fixture F.

## Findings

finding P-T-1 the 10 000-character cap constant is placed in inbox.py but used by suggest.py
anchor: suggest
seen: 01-requirements.md §6 unit 1 lists `SUGGEST_CHARS` among inbox.py's constants, while unit 14 puts the cap inside `suggest(note, docs)`; graph-interfaces forbids G-T to import inbox.
decision: ruled — ACCEPT (round 0b): the note cap lives in suggest.py as `NOTE_CHARS` (10 000); inbox.py defines no SUGGEST_CHARS. Applied: [Data: suggest constants]; LLR-4403.22 and requirements §6 reworded (LED-2026-11-01-incK.3).

finding P-T-2 the weight of a note word that no document holds is not stated
anchor: suggest
seen: LLR-4403.6 defines idf from df over the documents; a note stem with df 0 has no stated weight. With the formula it would weigh ln(N+1)+1 and lower every score against the fixed cuts (executed over F: N1 → Eval harness 0.2208 instead of 0.4018, ▰▰▱ instead of ▰▰▰; AT-4402's note → 0.2662 instead of 0.668); the prototype gives it 0 (`idf.get(s, 0.0)`), and the cuts HIGH/MID/LOW were tuned on that.
decision: ruled — ACCEPT the prototype (round 0b): a note word no board holds weighs 0. Applied: suggest func and TC-4466 example; LLR-4403.6's threshold gains the arm (LED-2026-11-01-incK.3).

finding P-T-3 the project-name tie order is code-point order
anchor: suggest
seen: LLR-4403.9 says "then by project name" without a collation; executed: one board holding "beta" (position 0) and "Alpha" (position 1) with equal scores → "Alpha" first, but "alpha" vs "Beta" would put "Beta" first (upper case sorts before lower case).
decision: ruled — AMEND (round 0b): ties on project name sort by `name.casefold()`, then `name`. Applied: algorithm step 5, suggest func, TC-4469 arms ("alpha"/"Beta", "beta"/"Beta"); LLR-4403.9 reworded (LED-2026-11-01-incK.3).

finding P-T-4 image lines of a note are scored as words
anchor: suggest
seen: the note text G-V passes holds `img: <name>` lines; words gives "img", the name's stem words and the suffix ("png"). Executed: they weigh 0 over F (no document holds them), so AT-4402 scores 0.668 with or without the line; a board whose documents hold "img"/"png"/"board" would match them.
decision: ruled — AMEND (round 0b): G-V passes `suggest` the note's title + "\n" + notes from `inbox.note_task` (image lines already removed); suggest.py stays free of inbox imports. Applied: algorithm step 1, suggest func, Seams, TC-4488 example; new LLR-4403.28 (LED-2026-11-01-incK.3).

finding P-T-5 documents have no size cap
anchor: corpus
seen: LLR-4403.22 caps the note at 10 000 characters but a board task's notes are scored whole; a board with very long notes makes corpus linear in its total text, once per open and per dump/undo.
decision: ruled — ACCEPT a cap (round 0b): each project document is cut at 100 000 characters before tokenising (deterministic). Applied: `DOC_CHARS` constant, corpus func, TC-4487 examples; new LLR-4403.27 (LED-2026-11-01-incK.3).

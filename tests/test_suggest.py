"""Deterministic, explained project suggestions for a captured note (Inc K, dev-flow-v3-beta;
HLR-4403 layer 0 · LLR-4403.1..4403.14, .16, .22..4403.29 — the suggest.py arms;
.30/.31 withdrawn by ARCH-12, the rail arms live in tests/test_capture_view.py).

WHY. The owner (`username_subject`) types notes in a hurry during a meeting and turns each one
into a task in the project the pad suggests (US-4401, K-3, D2). A suggestion is only useful when
it is RIGHT and EXPLAINED: a wrong weight (name ×2 instead of ×3), a lost tie rule or an uncapped
note files a note under the wrong project — silently, because the owner trusts the top choice.
So every number below is an exact executed value of graph-proto-T's fixture F (TF-IDF cosine,
halved on one shared stem, rounded to 4 decimals, cuts HIGH 0.30 / MID 0.16 / LOW 0.08), and the
reason words, their order, the tie order and the caps are pinned. The same note over the same
boards must give the same hits in every process (`PYTHONHASHSEED`), or the rail flickers between
sessions and the owner cannot learn it.

RED on the base revision (545c18a): `taskboard/suggest.py` does not exist. Every name is reached
through `capture_fixture.suggest()` / `need`, so each test fails on `pytest.fail("taskboard.suggest
missing (not built yet)")` — an assertion, never a collection error. No test here is a guard: every
one is RED on base.

Synthetic boards only (fixture F, `capture_fixture.f_lanes`); nothing is written to disk.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import pytest

import capture_fixture as fx
from taskboard.models import Board, Project, Task

ROOT = Path(__file__).resolve().parents[1]

# the 7 probe notes of the TC-4486 / TC-4489 digest (graph-proto-T, the executed run.py)
PROBES = [
    "Golden set: 12 questions still have no answer key ask @username_subject",
    "Volume lab fails on WSL\nthe oracle script expects /mnt/c\nimg: board-0938.png",
    "Volume lab fails on WSL\nthe oracle script expects /mnt/c",
    "Quote for the new client: contracts Q&A\ntwo weeks, fixed price",
    "Contracts pilot for the new client",
    "Steering deck: demo the hybrid search on pilot stores",
    "eval rubric for the oracle",
]
DIGEST = "d694943ce6d21f09"
N1_SHORT = PROBES[0]

IDF1 = 1.6931471805599454          # df 1 of N = 3: ln(4/2) + 1
IDF2 = 1.2876820724517808          # df 2 of N = 3: ln(4/3) + 1

# the documents of fixture F, tf exactly (graph-proto-T §Fixture F)
F_TF = {
    "Eval harness": {"eval": 5, "harnes": 3, "questi": 3, "bank": 2, "each": 1, "key": 1,
                     "@username_subject": 2, "judge": 2, "rubric": 2, "report": 2, "releas": 1},
    "Pilot rollout": {"pilot": 6, "rollou": 3, "store": 4, "list": 2, "six": 1, "region": 1,
                      "steeri": 2, "commit": 2, "@username_subject": 2, "chair": 1, "demo": 1,
                      "hybrid": 1, "search": 1, "invoic": 2, "octobe": 2, "paymen": 1},
    "Module 4 · Volumes": {"module": 5, "volume": 7, "oracle": 3, "script": 2, "check": 1,
                           "window": 1, "bind": 2, "named": 2, "page": 2, "print": 1,
                           "inode": 1, "publis": 2, "releas": 1},
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _s(name: str):
    return fx.need(fx.suggest(), name)


def _corpus(lanes, marks=None):
    return _s("corpus")(lanes, fx.f_marks() if marks is None else marks)


def _f(tmp_path):
    return _corpus(fx.f_lanes(tmp_path))


def _hits(note: str, corpus):
    return _s("suggest")(note, corpus)


def _view(hits) -> list[tuple[str, float, list[str]]]:
    return [(h.doc.project_name, h.score, list(h.why)) for h in hits]


def _doc(corpus, name: str):
    found = [d for d in corpus.docs if d.project_name == name]
    assert len(found) == 1, f"one document named {name!r}, got {len(found)}"
    return found[0]


def _lane(name: str, colour: str, board) -> tuple:
    return (name, colour, board, "")


def _board(tmp_path, folder: str, projects, tasks, phases=("Todo", "Doing", "Done")) -> Board:
    return Board(list(projects), list(tasks), tmp_path / folder / "board.json", {}, list(phases))


def _ledger_board(tmp_path, folder: str, names, ids=None) -> Board:
    """One board whose projects `names` each hold one task "Ledger audit"."""
    ids = ids or [f"p{i}" for i in range(len(names))]
    projects = [Project(n, "blue", id=i) for n, i in zip(names, ids)]
    tasks = [Task("Ledger audit", project_id=i, id=f"t{k}") for k, i in enumerate(ids)]
    return _board(tmp_path, folder, projects, tasks)


def _digest(corpus) -> str:
    rows = [[(h.doc.project_id, h.score, h.why) for h in _hits(n, corpus)] for n in PROBES]
    return hashlib.sha256(repr(rows).encode()).hexdigest()[:16]


# --------------------------------------------------------------------------- #
# LLR-4403.1 / 4403.2 — words and stems
# --------------------------------------------------------------------------- #
def test_TC_4461_words_fold_accents_drop_short_words_numbers_and_stop_words():
    """TC-4461 (LLR-4403.1): the reducer keeps `golden set questions @username_subject cafe`
    of the commission's sample, in text order — `12` (a bare number), `de`, `la` (stop words)
    gone; accents folded (NC keep numbers: `12` present)."""
    words, fold = _s("words"), _s("fold")
    assert fold("Golden SET: Café") == "golden set: cafe"
    assert fold("clés") == "cles"
    pairs = list(words("Golden SET: 12 Questions @username_subject de la Café"))
    assert pairs == [("golden", "golden"), ("set", "set"), ("questi", "questions"),
                     ("@username_subject", "@username_subject"), ("cafe", "cafe")]
    assert all(s != "12" and w != "12" for s, w in pairs)
    # colour markers are not words: one-letter codes drop by length; `0938` is a number
    assert list(words("::b:: Golden set :: ==late== img: board-0938.png")) == [
        ("golden", "golden"), ("set", "set"), ("late", "late"), ("img", "img"),
        ("board", "board"), ("png", "png")]


def test_TC_4462_stems_ies_to_y_drop_final_s_cut_to_six_handles_unstemmed():
    """TC-4462 (LLR-4403.2): `questions`→`questi`, `stories`→`story`, `class`→`class`,
    a handle unchanged (NC cut to 5: `quest`)."""
    stem = _s("stem")
    assert stem("questions") == "questi"
    assert stem("stories") == "story"
    assert stem("class") == "class"
    assert stem("@username_subject") == "@username_subject"
    assert stem("harness") == "harnes"
    assert stem("volumes") == "volume"
    assert stem("pies") == "pie"


# --------------------------------------------------------------------------- #
# LLR-4403.3 .. 4403.5 — documents and weights
# --------------------------------------------------------------------------- #
def test_TC_4463_one_document_per_live_project_of_every_readable_board(tmp_path):
    """TC-4463 (LLR-4403.3): 2 boards holding 3 live projects and 1 archived → 3 documents
    (NC archived included: 4)."""
    lanes = fx.f_lanes(tmp_path)
    lanes[1][2].projects.append(Project("Module 3 · Images", "sky", archived=True, id="pi"))
    lanes[1][2].tasks.append(Task("Image layers", project_id="pi", id="c9"))
    corpus = _corpus(lanes)
    assert [d.project_name for d in corpus.docs] == [
        "Eval harness", "Pilot rollout", "Module 4 · Volumes"]
    assert all(d.project_id != "pi" for d in corpus.docs)


def test_TC_4464_weights_name_x3_titles_x2_handles_x2_mark_name_x1_notes_x1(tmp_path):
    """TC-4464 (LLR-4403.4): project `Eval harness`, task `Answer key`, notes `ask
    @username_subject key`, milestone mark `payment` named `Payment` → tf exactly
    {eval 3, harnes 3, answer 2, key 3, @username_subject 2, paymen 1} (NC name ×2: eval 2)."""
    b = _board(tmp_path, "one", [Project("Eval harness", "blue", id="pe")],
               [Task("Answer key", project_id="pe", notes="ask @username_subject key",
                     due_date="2026-11-20", milestone=True, mark="payment", id="t1")])
    corpus = _corpus([_lane("Client A", "sky", b)])
    assert dict(_doc(corpus, "Eval harness").tf) == {
        "eval": 3, "harnes": 3, "answer": 2, "key": 3, "@username_subject": 2, "paymen": 1}


def test_TC_4464b_fixture_F_documents_hold_the_executed_term_counts(tmp_path):
    """TC-4464b (LLR-4403.4, LLR-4403.27): the three documents of F, tf exactly as executed
    (milestone mark names ×1, an archived task and a project-less task left out)."""
    corpus = _f(tmp_path)
    for name, tf in F_TF.items():
        assert dict(_doc(corpus, name).tf) == tf, name


def test_TC_4465_tasks_with_no_project_and_archived_tasks_join_no_document(tmp_path):
    """TC-4465 (LLR-4403.5): the project-less `Loose idea zebra` → no document holds `zebra`;
    the archived `Old golden set` → none holds `golden` (NC a `None`-project document)."""
    corpus = _f(tmp_path)
    assert len(corpus.docs) == 3
    assert all(d.project_id in ("pe", "pr", "pv") for d in corpus.docs)
    assert not any("zebra" in d.tf for d in corpus.docs)
    assert not any("golden" in d.tf for d in corpus.docs)


# --------------------------------------------------------------------------- #
# LLR-4403.6 .. 4403.8 — idf, cosine, halving
# --------------------------------------------------------------------------- #
def test_TC_4466_idf_is_ln_n_plus_1_over_df_plus_1_plus_1(tmp_path):
    """TC-4466 (LLR-4403.6): every idf of the 3-document fixture equals the hand value
    ln((N + 1)/(df + 1)) + 1 within 1e-9, keys only for stems some document holds (NC
    `ln(N / df)`: questi 1.0986)."""
    corpus = _f(tmp_path)
    df = Counter(s for tf in F_TF.values() for s in tf)
    hand = {s: math.log(4 / (n + 1)) + 1.0 for s, n in df.items()}
    assert set(corpus.idf) == set(hand)
    for s, v in hand.items():
        assert abs(corpus.idf[s] - v) < 1e-9, s
    assert abs(corpus.idf["questi"] - IDF1) < 1e-12
    assert abs(corpus.idf["@username_subject"] - IDF2) < 1e-12
    assert abs(corpus.idf["releas"] - IDF2) < 1e-12
    five = _board(tmp_path, "led", [Project(f"Ledger {w}", "blue", id=f"l{i}") for i, w in
                                    enumerate(["alpha", "bravo", "charlie", "delta", "echo"])],
                  [Task("Audit trail", project_id=f"l{i}", id=f"t{i}") for i in range(5)])
    c5 = _corpus([_lane("Ledgers", "sky", five)])
    assert abs(c5.idf["ledger"] - 1.0) < 1e-9            # df 5 = N
    assert abs(c5.idf["alpha"] - 2.098612) < 1e-6


def test_TC_4466b_a_note_stem_no_document_holds_weighs_zero(tmp_path):
    """TC-4466 arm 2 (LLR-4403.6, P-T-2): N1's golden/set/answer are held by no document and
    weigh 0 → `Eval harness` 0.4018 (NC a df-0 stem weighted ln(N + 1) + 1: 0.2208)."""
    assert _view(_hits(N1_SHORT, _f(tmp_path))) == [
        ("Eval harness", 0.4018, ["questions", "@username_subject", "key"])]


def test_TC_4467_the_score_is_the_cosine_of_the_tfidf_vectors(tmp_path):
    """TC-4467 (LLR-4403.7): N1 against `Eval harness` → the hand cosine 14.783240 /
    (2.718753 × 13.533744) = 0.401774 → 0.4018 within 1e-4 (NC dot without norms: 14.78)."""
    corpus = _f(tmp_path)
    eh = _doc(corpus, "Eval harness")
    assert abs(eh.norm - 13.533744) < 1e-5
    hand = 14.783240 / (2.718753 * 13.533744)
    hit = [h for h in _hits(N1_SHORT, corpus) if h.doc.project_name == "Eval harness"][0]
    assert abs(hit.score - hand) < 1e-4
    assert hit.score == round(hit.score, 4)


def test_TC_4468_one_shared_stem_halves_the_score_two_do_not(tmp_path):
    """TC-4468 (LLR-4403.8): `Café questions clés` shares only `questi` with `Eval harness`:
    score = 0.5 × cosine = 0.5 × 3·idf/|d| → 0.1877 (NC no halving: 0.3753); N1 shares 3 stems
    → 0.4018, not halved."""
    corpus = _f(tmp_path)
    cosine = 3 * IDF1 / 13.533744
    hits = _hits("Café questions clés", corpus)
    assert [(h.doc.project_name, h.score) for h in hits] == [("Eval harness", 0.1877)]
    assert abs(hits[0].score - 0.5 * cosine) < 1e-4
    assert [h.score for h in _hits(N1_SHORT, corpus)] == [0.4018]


# --------------------------------------------------------------------------- #
# LLR-4403.9 — tie order
# --------------------------------------------------------------------------- #
def test_TC_4469_equal_scores_order_by_board_then_casefolded_name_then_name_then_position(
        tmp_path):
    """TC-4469 (LLR-4403.9, P-T-3), 4 arms: board order wins over name; on one board the
    name wins over position; `alpha` before `Beta` (case-folded: NC plain `str` puts `Beta`
    first); `Beta` before `beta` (equal fold, then the stored name; NC position first puts
    `beta` first); two projects both named `Beta` → position."""
    note = "ledger audit"
    # arm 1 — lane 0 "Zulu" holds Beta, lane 1 "Able" holds Alpha
    zulu = _ledger_board(tmp_path, "zulu", ["Beta"], ["pz"])
    able = _ledger_board(tmp_path, "able", ["Alpha"], ["pa"])
    hits = _hits(note, _corpus([_lane("Zulu", "sky", zulu), _lane("Able", "lime", able)]))
    assert [(h.doc.project_name, h.score) for h in hits] == [("Beta", 0.5571), ("Alpha", 0.5571)]
    # arm 2 — one board, Beta at position 0, Alpha at position 1
    b = _ledger_board(tmp_path, "b2", ["Beta", "Alpha"])
    assert [h.doc.project_name for h in _hits(note, _corpus([_lane("B", "sky", b)]))] == [
        "Alpha", "Beta"]
    # arm 3 — alpha at 0, Beta at 1
    b = _ledger_board(tmp_path, "b3", ["alpha", "Beta"])
    hits = _hits(note, _corpus([_lane("B", "sky", b)]))
    assert [(h.doc.project_name, h.score) for h in hits] == [("alpha", 0.5571), ("Beta", 0.5571)]
    # arm 4 — beta at 0, Beta at 1
    b = _ledger_board(tmp_path, "b4", ["beta", "Beta"])
    hits = _hits(note, _corpus([_lane("B", "sky", b)]))
    assert [(h.doc.project_name, h.score) for h in hits] == [("Beta", 0.686), ("beta", 0.686)]
    # beta at 0, Alpha at 1 → Alpha then beta; two "Beta" (p0, p1) → p0 first
    b = _ledger_board(tmp_path, "b5", ["beta", "Alpha"])
    assert [h.doc.project_name for h in _hits(note, _corpus([_lane("B", "sky", b)]))] == [
        "Alpha", "beta"]
    b = _ledger_board(tmp_path, "b6", ["Beta", "Beta"], ["p0", "p1"])
    hits = _hits(note, _corpus([_lane("B", "sky", b)]))
    assert [(h.doc.project_id, h.score) for h in hits] == [("p0", 0.686), ("p1", 0.686)]


# --------------------------------------------------------------------------- #
# LLR-4403.10 .. 4403.13 — cut, top choice, options
# --------------------------------------------------------------------------- #
def test_TC_4470_at_most_three_hits_each_at_least_LOW(tmp_path):
    """TC-4470 (LLR-4403.10): five documents scoring 0.4698 → 3 hits (NC k = 4); a 0.0744
    document below LOW is absent; a score of exactly LOW 0.08 is kept."""
    led = _board(tmp_path, "led", [Project(f"Ledger {w}", "blue", id=f"l{i}") for i, w in
                                   enumerate(["alpha", "bravo", "charlie", "delta", "echo"])],
                 [Task("Audit trail", project_id=f"l{i}", id=f"t{i}") for i in range(5)])
    hits = _hits("ledger audit", _corpus([_lane("Ledgers", "sky", led)]))
    assert [(h.doc.project_name, h.score) for h in hits] == [
        ("Ledger alpha", 0.4698), ("Ledger bravo", 0.4698), ("Ledger charlie", 0.4698)]
    corpus = _f(tmp_path)
    assert [(h.doc.project_name, h.score) for h in _hits("committee rubric", corpus)] == [
        ("Eval harness", 0.0885)]
    at = _hits("Vendor call\n::b:: ask the vendor :: @username_subject", corpus)
    assert _view(at) == [("Eval harness", 0.0951, ["@username_subject"]),
                         ("Pilot rollout", 0.08, ["@username_subject"])]


def test_TC_4471_a_best_hit_at_or_above_MID_is_the_top_choice(tmp_path):
    """TC-4471 (LLR-4403.11): best 0.4379 → top is `Eval harness`, no `+ new project` in the
    options; best 0.1877 (≥ MID, < HIGH) is still the top (NC cut at HIGH: None first)."""
    options, corpus = _s("options"), _f(tmp_path)
    hits = _hits("eval rubric for the oracle pilot", corpus)
    assert _view(hits) == [("Eval harness", 0.4379, ["eval", "rubric"]),
                           ("Pilot rollout", 0.1578, ["pilot"])]
    opts = options(hits)
    assert [o.doc.project_name for o in opts] == ["Eval harness", "Pilot rollout"]
    opts = options(_hits("Café questions clés", corpus))
    assert [None if o is None else o.doc.project_name for o in opts] == ["Eval harness"]


def test_TC_4472_no_hit_at_or_above_MID_makes_new_project_the_top(tmp_path):
    """TC-4472 (LLR-4403.12): best 0.1488 → top None (NC the weak hit as top); no hit at
    all → top None, the only option."""
    options, corpus = _s("options"), _f(tmp_path)
    assert fx.need(fx.suggest(), "NEW_PROJECT") is None
    hits = _hits("store rubric", corpus)
    assert _view(hits) == [("Pilot rollout", 0.1488, ["store"]),
                           ("Eval harness", 0.0885, ["rubric"])]
    assert options(hits)[0] is None
    none = _hits(PROBES[3], corpus)
    assert none == []
    assert options(none) == [None]
    hits = _hits("Answer the region chair", corpus)
    assert _view(hits) == [("Pilot rollout", 0.1488, ["chair", "region"])]
    assert [None if o is None else o.doc.project_name for o in options(hits)] == [
        None, "Pilot rollout"]


def test_TC_4473_alternatives_are_the_next_two_hits_or_the_first_two_after_new_project(
        tmp_path):
    """TC-4473 (LLR-4403.13, R2 F-11): hits [0.40, 0.20, 0.10] → those 3 options; hits
    [0.12, 0.09] → [None, 0.12, 0.09]; never a 4th `+ new project` (the proto's NC)."""
    S, corpus = fx.suggest(), _f(tmp_path)
    Hit, options = fx.need(S, "Hit"), fx.need(S, "options")
    d = corpus.docs
    strong = [Hit(d[0], 0.40, ["a"]), Hit(d[1], 0.20, ["b"]), Hit(d[2], 0.10, ["c"])]
    assert options(strong) == strong
    weak = [Hit(d[0], 0.12, ["a"]), Hit(d[1], 0.09, ["b"])]
    assert options(weak) == [None] + weak
    three_weak = [Hit(d[0], 0.12, ["a"]), Hit(d[1], 0.09, ["b"]), Hit(d[2], 0.085, ["c"])]
    assert options(three_weak) == [None] + three_weak[:2]
    opts = options(_hits("store rubric", corpus))
    assert [None if o is None else (o.doc.project_name, o.score) for o in opts] == [
        None, ("Pilot rollout", 0.1488), ("Eval harness", 0.0885)]


# --------------------------------------------------------------------------- #
# LLR-4403.14 — the reason words
# --------------------------------------------------------------------------- #
def test_TC_4474_why_lists_the_notes_surface_words_largest_contribution_first(tmp_path):
    """TC-4474 (LLR-4403.14): N1 → why `questions`, `@username_subject`, `key` (shares 8.60,
    3.32, 2.87; NC alphabetical: @username_subject first); the note's own spelling
    (`questions`, not the stem `questi`)."""
    hits = _hits(N1_SHORT, _f(tmp_path))
    assert hits[0].doc.project_name == "Eval harness"
    assert list(hits[0].why) == ["questions", "@username_subject", "key"]


def test_TC_4474b_equal_contributions_tie_by_stem_and_every_shared_word_is_kept(tmp_path):
    """TC-4474b (LLR-4403.14): `chair` and `region` contribute equally → stem order; a
    6-word share keeps all 6 (the rail shows 3); the AT-4402 note → volume, oracle, script."""
    corpus = _f(tmp_path)
    assert list(_hits("Answer the region chair", corpus)[0].why) == ["chair", "region"]
    hits = _hits("Steering deck: demo the hybrid search on pilot stores", corpus)
    assert _view(hits) == [("Pilot rollout", 0.6444,
                            ["pilot", "stores", "steering", "demo", "hybrid", "search"])]
    hits = _hits(PROBES[1], corpus)
    assert _view(hits) == [("Module 4 · Volumes", 0.668, ["volume", "oracle", "script"])]
    assert hits[0].doc.board_name == "Course"


def test_TC_4475b_the_rail_notes_hit_values_G_V_draws(tmp_path):
    """TC-4475b (LLR-4403.15's data, E2c cross-check): the rail's N1 (two lines) → Eval
    harness 0.341 and Pilot rollout 0.2869, both ≥ MID so both are options; N3 → []."""
    corpus = _f(tmp_path)
    hits = _hits(fx.N1, corpus)
    assert _view(hits) == [("Eval harness", 0.341, ["questions", "@username_subject", "key"]),
                           ("Pilot rollout", 0.2869, ["stores", "@username_subject"])]
    assert len(_s("options")(hits)) == 2
    assert _hits(fx.N3, corpus) == []


# --------------------------------------------------------------------------- #
# LLR-4403.16 — the confidence cue
# --------------------------------------------------------------------------- #
def test_TC_4476_the_cue_is_three_two_or_one_filled_bars_by_cut(tmp_path):
    """TC-4476 (LLR-4403.16, layer 0): level and bars at and either side of each cut —
    0.30 → ▰▰▰, 0.2999 → ▰▰▱, 0.16 → ▰▰▱, 0.1599 → ▰▱▱, 0.08 → ▰▱▱, 0.0799 → ▱▱▱."""
    level, bars = _s("level"), _s("bars")
    for score, n in [(0.41, 3), (0.30, 3), (0.2999, 2), (0.16, 2), (0.1599, 1), (0.08, 1),
                     (0.0799, 0)]:
        assert level(score) == n, score
    assert [bars(x) for x in (0.41, 0.20, 0.09, 0.05)] == ["▰▰▰", "▰▰▱", "▰▱▱", "▱▱▱"]
    assert [bars(x) for x in (0.4018, 0.1877, 0.0885)] == ["▰▰▰", "▰▰▱", "▰▱▱"]
    assert all(len(bars(x)) == 3 for x in (0.0, 0.5, 1.0))


# --------------------------------------------------------------------------- #
# LLR-4403.22 — the note cap
# --------------------------------------------------------------------------- #
def test_TC_4482_a_note_is_scored_on_its_first_10000_characters(tmp_path):
    """TC-4482 (LLR-4403.22, P-T-1, ARCH-5): `"x" × 9 995 + " eval harness"` → only `eval`
    survives the cut: `Eval harness` 0.3128 why `eval` (THE control: uncapped 0.7077 why eval,
    harness); a 4 MB note → the same hits as its first 10 000 characters in < 1.0 s."""
    S = fx.suggest()
    assert fx.need(S, "NOTE_CHARS") == 10_000
    corpus = _f(tmp_path)
    assert _view(_hits("x" * 9_995 + " eval harness", corpus)) == [
        ("Eval harness", 0.3128, ["eval"])]
    big = "eval harness " + "z " * 2_000_000
    t0 = time.perf_counter()
    hits = _hits(big, corpus)
    took = time.perf_counter() - t0
    assert _view(hits) == _view(_hits(big[:10_000], corpus)) == [
        ("Eval harness", 0.7077, ["eval", "harness"])]
    assert took < 1.0, f"{took:.3f} s"


# --------------------------------------------------------------------------- #
# LLR-4403.23 / 4403.24 / 4403.25 — documents from every lane, rebuilt, empty
# --------------------------------------------------------------------------- #
def test_TC_4483_documents_come_from_every_lane_in_lane_then_project_order(tmp_path):
    """TC-4483 (LLR-4403.23, layer 0): F's two lanes → Eval harness (lane 0, pos 0), Pilot
    rollout (lane 0, pos 1), Module 4 · Volumes (lane 1, pos 0, Course's path, name, colour)
    (NC `app.board` only: 2 documents); a lane whose board is None adds none."""
    lanes = fx.f_lanes(tmp_path)
    docs = _corpus(lanes).docs
    assert [(d.project_name, d.lane, d.position) for d in docs] == [
        ("Eval harness", 0, 0), ("Pilot rollout", 0, 1), ("Module 4 · Volumes", 1, 0)]
    mv = docs[2]
    assert (mv.board_name, mv.board_colour, Path(mv.board_path)) == (
        "Course", "violet", lanes[1][2].path)
    assert (mv.project_id, mv.project_colour) == ("pv", "violet")
    assert (docs[0].board_name, docs[0].board_colour, docs[0].project_colour) == (
        "Client A", "sky", "blue")
    gone = [lanes[0], ("Gone", "pink", None, "file missing")]
    assert [d.project_name for d in _corpus(gone).docs] == ["Eval harness", "Pilot rollout"]


def test_TC_4484_a_corpus_built_after_a_dump_holds_the_new_task(tmp_path):
    """TC-4484 (LLR-4403.24, layer 0): note `rotation` → no hit over F; over F plus a task
    `Rotation plan` in Eval harness (the board as read after the dump) → its tf holds rotati 2,
    plan 2 and `rotation` hits Eval harness 0.1179 (one shared stem, halved)."""
    assert _hits("rotation", _f(tmp_path)) == []
    lanes = fx.f_lanes(tmp_path)
    lanes[0][2].tasks.append(Task("Rotation plan", project_id="pe", id="a9"))
    corpus = _corpus(lanes)
    tf = _doc(corpus, "Eval harness").tf
    assert (tf["rotati"], tf["plan"]) == (2, 2)
    assert _view(_hits("rotation", corpus)) == [("Eval harness", 0.1179, ["rotation"])]


def test_TC_4485_no_live_project_anywhere_gives_new_project_only(tmp_path):
    """TC-4485 (LLR-4403.25, layer 0): one board with 0 projects → `Corpus([], {})`, every
    note → hits [] and options [None], 0 exceptions (NC index the empty list); a project
    `Q&A` with no task → an empty document that counts in N (N1 then scores 0.4044)."""
    S = fx.suggest()
    empty = _board(tmp_path, "empty", [], [Task("No project here", id="t1")])
    corpus = _corpus([_lane("Empty", "sky", empty)])
    assert list(corpus.docs) == [] and dict(corpus.idf) == {}
    for note in ("eval", "rotation plan", ""):
        assert _hits(note, corpus) == []
    assert fx.need(S, "options")([]) == [None]
    qa = _board(tmp_path, "qa", [Project("Q&A", "lime", id="qa")], [])
    corpus = _corpus([_lane("QA", "lime", qa)] + fx.f_lanes(tmp_path))
    assert len(corpus.docs) == 4
    assert dict(_doc(corpus, "Q&A").tf) == {}
    assert [(h.doc.project_name, h.score) for h in _hits(N1_SHORT, corpus)] == [
        ("Eval harness", 0.4044)]


# --------------------------------------------------------------------------- #
# LLR-4403.26 — determinism across processes
# --------------------------------------------------------------------------- #
_CHILD = r"""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path("tests").resolve()))
import capture_fixture as fx
from taskboard import suggest as S
corpus = S.corpus(fx.f_lanes(Path("S")), fx.f_marks())
notes = json.loads(sys.argv[1])
rows = [[(h.doc.project_id, h.score, h.why) for h in S.suggest(n, corpus)] for n in notes]
print(json.dumps({"rows": rows, "digest": hashlib.sha256(repr(rows).encode()).hexdigest()[:16]}))
"""


def _child(seed: str) -> dict:
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    env["PYTHONHASHSEED"] = seed
    env["PYTHONIOENCODING"] = "utf-8"
    out = subprocess.run([sys.executable, "-c", _CHILD, json.dumps(PROBES)], cwd=ROOT, env=env,
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_TC_4486_the_same_note_gives_the_same_hits_under_any_hash_seed():
    """TC-4486 (LLR-4403.26, ARCH-5): the 7 probe notes scored in 2 subprocesses with
    PYTHONHASHSEED 0 and 1 (NO_COLOR removed) → equal (project id, score, why) lists, digest
    `d694943ce6d21f09` in both (NC iterate a `set` for the tie order: the seeds differ — one
    process shares one seed, so only two processes can see it)."""
    fx.need(fx.suggest(), "corpus")
    a, b = _child("0"), _child("1")
    assert a["rows"] == b["rows"]
    assert a["digest"] == b["digest"] == DIGEST


# --------------------------------------------------------------------------- #
# LLR-4403.27 / 4403.28 — the document cap, the scored text
# --------------------------------------------------------------------------- #
def test_TC_4487_a_document_is_tokenised_on_its_first_100000_characters(tmp_path):
    """TC-4487 (LLR-4403.27, P-T-5): `Ledger alpha` / `Audit log` / notes `"audit " × 20 000 +
    "zebra"` (120 005 characters) → tf {ledger 3, alpha 3, audit 16 665, log 2}, no `zebra`
    (NC no cap: zebra present), built in < 1.0 s; F (under the cap) keeps its full tf."""
    S = fx.suggest()
    assert fx.need(S, "DOC_CHARS") == 100_000
    b = _board(tmp_path, "led", [Project("Ledger alpha", "blue", id="la")],
               [Task("Audit log", project_id="la", notes="audit " * 20_000 + "zebra", id="t1")])
    t0 = time.perf_counter()
    corpus = _corpus([_lane("Ledgers", "sky", b)])
    took = time.perf_counter() - t0
    assert dict(_doc(corpus, "Ledger alpha").tf) == {
        "ledger": 3, "alpha": 3, "audit": 16_665, "log": 2}
    assert took < 1.0, f"{took:.3f} s"
    f = _f(tmp_path)
    for name, tf in F_TF.items():
        assert dict(_doc(f, name).tf) == tf, name


def test_TC_4488_a_note_is_scored_on_its_title_and_notes_without_image_lines(tmp_path):
    """TC-4488 (LLR-4403.28, P-T-4): F plus a lane `Shots` holding `Png board` (no task) —
    the scored text of `Shot\\nimg: board-1.png` (`inbox.note_task` title + "\\n" + notes)
    → hits [] (the raw part text would hit `Png board` 1.0: the control is live); the AT-4402
    note → `Module 4 · Volumes` 0.668 with or without its image line."""
    note_task = fx.need(fx.inbox(), "note_task")
    lanes = fx.f_lanes(tmp_path)
    shots = _board(tmp_path, "shots", [Project("Png board", "pink", id="pb")], [])
    corpus = _corpus(lanes + [_lane("Shots", "pink", shots)])
    raw = "Shot\nimg: board-1.png"
    nt = note_task(raw)
    scored = nt.title + "\n" + nt.notes
    assert scored == "Shot\n"
    assert _hits(scored, corpus) == []
    assert [(h.doc.project_name, h.score) for h in _hits(raw, corpus)] == [("Png board", 1.0)]
    nt2 = note_task(PROBES[1])
    assert nt2.title + "\n" + nt2.notes == PROBES[2]
    for text in (PROBES[1], PROBES[2]):
        assert [(h.doc.project_name, h.score) for h in _hits(text, corpus)] == [
            ("Module 4 · Volumes", 0.668)]


# --------------------------------------------------------------------------- #
# LLR-4403.29 — idf, vectors and norms once per build
# --------------------------------------------------------------------------- #
def test_TC_4489_idf_vectors_and_norms_are_built_once_per_corpus(tmp_path, monkeypatch):
    """TC-4489 (LLR-4403.29, ARCH-6): a spy on `suggest._idf` → 1 call for 1 build and still 1
    after the 7 probe suggest calls (NC idf inside suggest: 8); each Doc's `vec` = tf × idf and
    `norm` = its length; the 7 notes' digest `d694943ce6d21f09` (the per-call computation's)."""
    S = fx.suggest()
    real = fx.need(S, "_idf")
    calls = []

    def spy(docs):
        calls.append(len(docs))
        return real(docs)
    monkeypatch.setattr(S, "_idf", spy)
    corpus = _f(tmp_path)
    assert calls == [3]
    for n in PROBES:
        _hits(n, corpus)
    assert len(calls) == 1, f"_idf called {len(calls)} times for 1 build"
    for d in corpus.docs:
        want = {s: c * corpus.idf[s] for s, c in d.tf.items()}
        assert set(d.vec) == set(want)
        for s, v in want.items():
            assert abs(d.vec[s] - v) < 1e-9, (d.project_name, s)
        assert abs(d.norm - math.sqrt(sum(v * v for v in want.values()))) < 1e-9
    assert _digest(corpus) == DIGEST
    assert len(calls) == 1


def _large_lanes(tmp_path) -> list:
    """20 boards × 15 projects × 40 tasks × 80 note words of a 5 000-word synthetic vocabulary,
    seed 7 (LLR-4403.29's stated large fixture; 300 documents)."""
    rnd = random.Random(7)
    letters = "abcdefghijklmnopqrstuvwxyz"
    vocab, seen = [], set()
    while len(vocab) < 5_000:
        w = "".join(rnd.choice(letters) for _ in range(rnd.randint(4, 9)))
        if w not in seen:
            seen.add(w)
            vocab.append(w)
    lanes = []
    for b in range(20):
        projects, tasks = [], []
        for p in range(15):
            pid = f"b{b}p{p}"
            projects.append(Project(" ".join(rnd.sample(vocab, 2)), "blue", id=pid))
            for t in range(40):
                tasks.append(Task(" ".join(rnd.sample(vocab, 3)), project_id=pid,
                                  notes=" ".join(rnd.choice(vocab) for _ in range(80)),
                                  id=f"{pid}t{t}"))
        lanes.append(_lane(f"Board {b}", "sky",
                           _board(tmp_path, f"big{b}", projects, tasks)))
    return lanes, vocab


def test_TC_4489b_one_suggest_call_over_300_documents_takes_under_20_ms(tmp_path):
    """TC-4489 arm 3 (LLR-4403.29): over the stated large fixture one `suggest` call takes
    < 20 ms (executed 2.7 ms; idf recomputed per call: 139.6 ms — the NC)."""
    lanes, vocab = _large_lanes(tmp_path)
    corpus = _corpus(lanes, {})
    assert len(corpus.docs) == 300
    rnd = random.Random(11)
    note = " ".join(rnd.choice(vocab) for _ in range(30))
    _hits(note, corpus)                          # warm
    best = min(_timed(note, corpus) for _ in range(5))
    assert best < 0.020, f"{best * 1000:.1f} ms per suggest call"


def _timed(note, corpus) -> float:
    t0 = time.perf_counter()
    _hits(note, corpus)
    return time.perf_counter() - t0

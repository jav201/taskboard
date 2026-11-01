"""Deterministic TF-IDF project suggester (Inc K, HLR-4403).

One document per non-archived project of every readable board; a note is scored
as the cosine of its tf-idf bag against each document's bag, halved when it
rests on a single shared stem. The module is pure: it imports only the standard
library, reads the `Board` / `Project` / `Task` / `Mark` attributes it is handed
by attribute only, and never reads a file, writes anything, or imports another
taskboard module.
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import NamedTuple

# ---- suggestion constants (never written at run time) -----------------------

#: Stop words of LLR-4403.1 — the capture-round prototype's list verbatim.
STOP = set("""
a an and are as at be been but by can de del do el en es for from has have how i if in
into is it its la las los me my no not of on or our para por que se so the their them then
there these this to too un una was we were what when where which who will with y you your
ask get got let make new still need needs want via also just only more most very about
after before over under per two one all any some
day days week weeks month today tomorrow monday tuesday wednesday thursday friday saturday sunday
""".split())

#: A word is an `@handle` (with `.`, `_`, `-` segments) or a run of `[a-z0-9]`.
WORD_RE = re.compile(r"@[a-z0-9]+(?:[._\-][a-z0-9]+)*|[a-z0-9]+")

#: Document weights (R0-7): integers keep the `tf` Counter exact.
W_NAME, W_TITLE, W_PEOPLE, W_MARK, W_NOTES = 3, 2, 2, 1, 1

#: Confidence cuts (LLR-4403.16): ▰▰▰ / ▰▰▱ / ▰▱▱ / ▱▱▱.
HIGH, MID, LOW = 0.30, 0.16, 0.08

#: A note's scored text is cut to its first NOTE_CHARS characters before folding
#: (LLR-4403.22; P-T-1: the cap lives here, not in inbox.py).
NOTE_CHARS = 10_000

#: Each document's text is cut at DOC_CHARS characters before tokenising
#: (LLR-4403.27, P-T-5).
DOC_CHARS = 100_000

#: At most this many hits (and options) are returned (LLR-4403.10).
MAX_HITS = 3

#: The `+ new project` option (LLR-4403.12), drawn by G-V.
NEW_PROJECT = None


def fold(s: str) -> str:
    """Fold `s` to comparable form: NFKD, combining marks dropped, lower case.

    Never raises; ``None`` or ``""`` fold to ``""`` (LLR-4403.1).
    """
    return "".join(ch for ch in unicodedata.normalize("NFKD", s or "")
                   if not unicodedata.combining(ch)).lower()


def stem(w: str) -> str:
    """Stem one word (LLR-4403.2): handles stay whole; a final ``ies`` becomes
    ``y`` when the word is longer than 4; a final ``s`` that is not ``ss`` is
    dropped when longer than 3; the result is cut to its first 6 characters.
    """
    if w.startswith("@"):
        return w
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    return w[:6]


def words(text: str) -> list[tuple[str, str]]:
    """(stem, surface word) for each word that counts (LLR-4403.1/4403.2).

    Each `@handle` is kept whole; any other word only when it is 3 or more
    characters, not a stop word and not all digits. Colour markers and the
    `==`/`!!`/`++` spans need no stripping: their one-letter codes drop by
    length and the span glyphs are not word characters. Never raises.
    """
    out: list[tuple[str, str]] = []
    for w in WORD_RE.findall(fold(text)):
        if w.startswith("@") or (len(w) >= 3 and w not in STOP and not w.isdigit()):
            out.append((stem(w), w))
    return out


class Doc(NamedTuple):
    """One project's weighted bag of stems, with its board chip and tf-idf data."""
    lane: int                 # index in `board_lanes` lanes
    board_name: str           # the lane's registry name (the chip)
    board_colour: str         # the lane's registry colour
    board_path: Path          # `board.path` — G-V turns it into a DumpTarget
    project_id: str
    project_name: str
    project_colour: str
    position: int             # index in `board.projects` (archived counted)
    tf: Counter               # stem -> weighted count
    vec: dict                 # stem -> tf·idf, set once by corpus (ARCH-6)
    norm: float               # |vec| or 1.0, set once by corpus (ARCH-6)


class Corpus(NamedTuple):
    """What `corpus` returns and `suggest` reads (ARCH-6)."""
    docs: list[Doc]
    idf: dict[str, float]


class Hit(NamedTuple):
    """One suggestion: the document, its rounded score and its reason words."""
    doc: Doc
    score: float              # cosine, halved on one shared stem, rounded to 4 decimals
    why: list[str]            # every shared surface word, largest share first


def corpus(lanes: list[tuple[str, str, object | None, str]],
           marks: dict) -> Corpus:
    """Build one document per non-archived project of every readable board.

    `lanes` is ``board_lanes(app)[0]``: ``(board_name, board_colour, board,
    state)`` in board order (LLR-4403.23). `marks` is ``app.marks.marks``
    (id → `Mark`); only ``Mark.name`` is read. The idf, each document's tf·idf
    vector and its norm are computed exactly once per build (ARCH-6, LLR-4403.29).
    """
    rows: list[tuple] = []
    for li, lane in enumerate(lanes):
        board_name, board_colour, board, _state = lane
        if board is None:                      # a missing/unreadable board: skip
            continue
        for pi, p in enumerate(board.projects):
            if p.archived:                     # archived keeps its position but joins no doc
                continue
            tf: Counter = Counter()
            left = DOC_CHARS                   # the per-document text budget (P-T-5)
            piece = p.name[:left]
            left -= len(piece)
            for s, _w in words(piece):
                tf[s] += W_NAME
            for t in board.tasks:
                if t.project_id != p.id or t.archived:
                    continue
                piece = t.title[:left]
                left -= len(piece)
                for s, _w in words(piece):
                    tf[s] += W_TITLE
                piece = t.notes[:left]
                left -= len(piece)
                for s, _w in words(piece):
                    tf[s] += W_PEOPLE if s.startswith("@") else W_NOTES
                if t.milestone is True and t.mark and t.mark in marks:
                    piece = marks[t.mark].name[:left]
                    left -= len(piece)
                    for s, _w in words(piece):
                        tf[s] += W_MARK
            rows.append((li, board_name, board_colour, board.path,
                         p.id, p.name, p.color, pi, tf))
    docs = [Doc(*row, {}, 0.0) for row in rows]
    idf = _idf(docs)
    filled: list[Doc] = []
    for d in docs:
        vec = {s: c * idf[s] for s, c in d.tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        filled.append(Doc(d.lane, d.board_name, d.board_colour, d.board_path,
                          d.project_id, d.project_name, d.project_colour,
                          d.position, d.tf, vec, norm))
    return Corpus(filled, idf)


def _idf(docs: list[Doc]) -> dict[str, float]:
    """`idf = ln((N + 1) / (df + 1)) + 1` over the documents (LLR-4403.6).

    ``df`` counts a stem once per document that holds it. Only stems some
    document holds are keys. Called by `corpus` only, once per build (ARCH-6).
    """
    df: Counter = Counter()
    for d in docs:
        df.update(set(d.tf))
    n = len(docs)
    return {s: math.log((n + 1) / (c + 1)) + 1.0 for s, c in df.items()}


def suggest(note: str, corpus: Corpus) -> list[Hit]:
    """The top suggestions for `note`, best first, or ``[]`` for no docs.

    `note` is the scored text G-V passes (``note_task`` title + "\\n" + notes,
    image lines left out, P-T-4). Its first `NOTE_CHARS` characters are scored.
    idf, vectors and norms are read from the corpus, never recomputed (ARCH-6).
    A note stem no document holds weighs 0 (P-T-2). The score is the tf·idf
    cosine, halved on exactly one shared stem, rounded to 4 decimals; only
    scores ≥ LOW are hits, at most MAX_HITS, ordered by (−score, lane, project
    name case-folded, project name, position) (LLR-4403.9, P-T-3). Pure and
    deterministic; never raises.
    """
    docs = corpus.docs
    if not docs:
        return []
    text = (note or "")[:NOTE_CHARS]
    idf = corpus.idf
    nw = words(text)
    q: Counter = Counter(s for s, _w in nw)
    surface: dict[str, str] = {}
    for s, w in nw:
        surface.setdefault(s, w)
    qv = {s: c * idf.get(s, 0.0) for s, c in q.items()}
    qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
    hits: list[Hit] = []
    for d in docs:
        dv = d.vec
        share = {s: qv[s] * dv[s] for s in qv if s in dv}
        score = sum(share.values()) / (qn * d.norm)
        if len(share) == 1:                    # one shared word is a guess: halve
            score *= 0.5
        score = round(score, 4)
        if score <= 0:
            continue
        why = [surface[s] for s, _v in sorted(share.items(),
                                              key=lambda kv: (-kv[1], kv[0]))]
        hits.append(Hit(d, score, why))
    hits.sort(key=lambda h: (-h.score, h.doc.lane,
                             h.doc.project_name.casefold(),
                             h.doc.project_name, h.doc.position))
    return [h for h in hits if h.score >= LOW][:MAX_HITS]


def level(score: float) -> int:
    """The cue level of a rounded score (LLR-4403.16): 3/2/1/0 at HIGH/MID/LOW."""
    if score >= HIGH:
        return 3
    if score >= MID:
        return 2
    if score >= LOW:
        return 1
    return 0


def bars(score: float) -> str:
    """The 3-glyph confidence cue (LLR-4403.16); plain text, G-V styles it."""
    n = level(score)
    return "▰" * n + "▱" * (3 - n)


def options(hits: list[Hit]) -> list[Hit | None]:
    """A note's option list (LLR-4403.11/4403.12/4403.13).

    A strong top (≥ MID) is the hits (≤ 3); otherwise `+ new project` (None)
    leads and up to 2 weak hits follow. Never appends NEW_PROJECT after a
    strong top (R2 F-11).
    """
    if hits and hits[0].score >= MID:
        return list(hits[:MAX_HITS])
    return [NEW_PROJECT] + list(hits[:2])

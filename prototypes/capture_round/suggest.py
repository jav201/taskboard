"""THROWAWAY — the capture round's deterministic project suggester (D2). No AI, no network.

Method (recommended, `tfidf`): every project of every board is one document built
from what the boards already hold — its NAME (weight 3), its tasks' TITLES (2),
the `@people` its notes mention (2), its milestones' MARK names (1) and its
tasks' NOTES (1). A note and each document become bags of normalised words
(lower case, accents dropped, a plural `s` dropped, cut to 6 letters, stop words
and bare numbers out; an `@handle` is one word). Each word is weighted by
TF-IDF across the projects (a word every project has says nothing), and the
score is the cosine of the two bags, halved when it rests on ONE shared word
(one word is a guess). Below MID the top suggestion is "new project" and the
weak hits are only offered as alternatives. The "why" is the note's words that carry
the score, largest share first. Ties break on board order, then project name:
the same boards and the same note give the same answer, every time.

Two baselines are kept only for the page's comparison: `trigram` (Jaccard of
character 3-grams) and `overlap` (count of shared words, unweighted).
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, defaultdict
from typing import NamedTuple

STOP = set("""
a an and are as at be been but by can de del do el en es for from has have how i if in
into is it its la las los me my no not of on or our para por que se so the their them then
there these this to too un una was we were what when where which who will with y you your
ask get got let make new still need needs want via also just only more most very about
after before over under per two one all any some
day days week weeks month today tomorrow monday tuesday wednesday thursday friday saturday sunday
""".split())
WORD_RE = re.compile(r"@[a-z0-9]+(?:[._\-][a-z0-9]+)*|[a-z0-9]+")
W_NAME, W_TITLE, W_PEOPLE, W_MARK, W_NOTES = 3.0, 2.0, 2.0, 1.0, 1.0
HIGH, MID, LOW = 0.30, 0.16, 0.08       # cosine cut-offs: ▰▰▰ / ▰▰▱ / ▰▱▱ ; below LOW: "new project"


def fold(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", s or "")
                   if not unicodedata.combining(ch)).lower()


def stem(w: str) -> str:
    if w.startswith("@"):
        return w
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    return w[:6]


def words(text: str) -> list[tuple[str, str]]:
    """(stem, surface word) for every word that counts."""
    out = []
    for w in WORD_RE.findall(fold(text)):
        if w.startswith("@") or (len(w) >= 3 and w not in STOP and not w.isdigit()):
            out.append((stem(w), w))
    return out


class Doc(NamedTuple):
    board_id: str
    board: str
    board_colour: str
    project_id: str
    name: str
    colour: str
    order: int
    tf: Counter          # stem -> weighted count
    text: str            # everything, for the trigram baseline


class Hit(NamedTuple):
    doc: Doc
    score: float
    why: list[str]       # the note's words that carry the score


def corpus(boards) -> list[Doc]:
    """`boards`: [(board_id, name, colour, Board)] in registry order."""
    docs = []
    for bi, (bid, bname, bcol, board) in enumerate(boards):
        marks = getattr(board, "marks", None) or {}
        for pi, p in enumerate(board.projects):
            if p.archived:
                continue
            tf: Counter = Counter()
            parts = [p.name]
            for s, _w in words(p.name):
                tf[s] += W_NAME
            for t in board.tasks:
                if t.project_id != p.id or t.archived:
                    continue
                parts += [t.title, t.notes]
                for s, _w in words(t.title):
                    tf[s] += W_TITLE
                for s, _w in words(t.notes):
                    tf[s] += W_PEOPLE if s.startswith("@") else W_NOTES
                if t.milestone and t.mark and t.mark in marks:
                    for s, _w in words(marks[t.mark].name):
                        tf[s] += W_MARK
            docs.append(Doc(bid, bname, bcol, p.id, p.name, p.color, bi * 1000 + pi, tf,
                            " ".join(parts)))
    return docs


def _idf(docs: list[Doc]) -> dict[str, float]:
    df: Counter = Counter()
    for d in docs:
        df.update(set(d.tf))
    n = len(docs)
    return {s: math.log((n + 1) / (c + 1)) + 1.0 for s, c in df.items()}


def suggest(note: str, docs: list[Doc], k: int = 3) -> list[Hit]:
    """The top `k` projects for `note`, best first; [] when nothing scores LOW."""
    if not docs:
        return []
    idf = _idf(docs)
    nw = words(note)
    q: Counter = Counter(s for s, _w in nw)
    surface: dict[str, str] = {}
    for s, w in nw:
        surface.setdefault(s, w)
    qv = {s: c * idf.get(s, 0.0) for s, c in q.items()}
    qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
    hits = []
    for d in docs:
        dv = {s: c * idf[s] for s, c in d.tf.items()}
        dn = math.sqrt(sum(v * v for v in dv.values())) or 1.0
        share = {s: qv[s] * dv[s] for s in qv if s in dv}
        score = sum(share.values()) / (qn * dn)
        if len(share) == 1:          # one shared word is a guess: half the score
            score *= 0.5
        if score <= 0:
            continue
        why = [surface[s] for s, _v in sorted(share.items(), key=lambda kv: (-kv[1], kv[0]))]
        hits.append(Hit(d, round(score, 4), why))
    hits.sort(key=lambda h: (-h.score, h.doc.order, h.doc.name))
    return [h for h in hits if h.score >= LOW][:k]


def level(score: float) -> int:
    return 3 if score >= HIGH else 2 if score >= MID else 1 if score >= LOW else 0


def bars(score: float) -> str:
    n = level(score)
    return "▰" * n + "▱" * (3 - n)


# --- the two baselines (the page's D2 comparison only) -----------------------------------
def _grams(s: str) -> set[str]:
    s = " " + re.sub(r"\s+", " ", fold(s)) + " "
    return {s[i:i + 3] for i in range(len(s) - 2)}


def suggest_trigram(note: str, docs: list[Doc]) -> list[tuple[Doc, float]]:
    g = _grams(note)
    out = []
    for d in docs:
        h = _grams(d.text)
        out.append((d, len(g & h) / (len(g | h) or 1)))
    out.sort(key=lambda x: (-x[1], x[0].order))
    return out


def suggest_overlap(note: str, docs: list[Doc]) -> list[tuple[Doc, int]]:
    q = {s for s, _w in words(note)}
    out = [(d, len(q & set(d.tf))) for d in docs]
    out.sort(key=lambda x: (-x[1], x[0].order))
    return out


def split_topics(text: str) -> list[tuple[int, int, str]]:
    """The pad's text as topics: (first line, last line, text) for each run of
    non-blank lines — a blank line separates topics."""
    out, start, buf = [], None, []
    lines = text.split("\n")
    for i, ln in enumerate(lines + [""]):
        if ln.strip():
            if start is None:
                start = i
            buf.append(ln)
        elif start is not None:
            out.append((start, i - 1, "\n".join(buf)))
            start, buf = None, []
    return out


def as_task(text: str) -> tuple[str, str, list[str]]:
    """A topic as (title, notes, images): the first line is the title, `img:` lines
    are the images, the rest are the notes (mentions and highlights carried as typed)."""
    lines = [ln for ln in text.split("\n")]
    title = lines[0].strip()
    imgs = [ln.split(":", 1)[1].strip() for ln in lines[1:] if ln.strip().startswith("img:")]
    rest = [ln for ln in lines[1:] if not ln.strip().startswith("img:")]
    return title, "\n".join(rest).strip(), imgs


__all__ = ["corpus", "suggest", "bars", "level", "split_topics", "as_task", "Doc", "Hit",
           "suggest_trigram", "suggest_overlap", "defaultdict"]

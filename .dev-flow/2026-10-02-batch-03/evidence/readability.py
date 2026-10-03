"""Title readability, re-derived from the prototype metric
(`prototypes/kg_mejoras/capture_kanban.py` `visible_chars` / `readability`) as
measurement tooling for batch 2026-10-02-batch-03 — never product code.

For each of the oracle board's 28 task titles: the longest title prefix found in a
row of the drawn region, plus a word-wrapped continuation read on the next row at
the same column. Reports (avg visible chars over all 28 titles, titles shown in
full, titles drawn at all). The region is the panel's BODY as seen at scroll 0:
rows 3..h-1 of the first `h` (the head, the phase row and the rule dropped), and the
last row too when it is a fold row (`▲`/`▼`). A match counts only when it covers
the title's whole first word (P2 qa Q-3: a 1-2 char hit inside a header or another
card is not a drawn title).
"""
from __future__ import annotations


def visible_chars(rows: list[str], title: str) -> int:
    best = 0
    for r, row in enumerate(rows):
        k = len(title)
        while k > 0 and title[:k] not in row:
            k -= 1
        if k <= best or k < len(title.split(" ")[0]):
            continue
        tot = k
        if k < len(title) and title[k] == " " and r + 1 < len(rows):
            x = row.index(title[:k])
            rest, nxt = title[k + 1:], rows[r + 1]
            j = 0
            while j < len(rest) and x + j < len(nxt) and nxt[x + j] == rest[j]:
                j += 1
            if j:
                tot = k + 1 + j
        best = max(best, tot)
    return best


def readability(rows: list[str], titles: list[str]) -> tuple[float, int, int]:
    seen = [visible_chars(rows, t) for t in titles]
    full = sum(1 for s, t in zip(seen, titles) if s == len(t))
    return sum(seen) / len(titles), full, sum(1 for s in seen if s)


def body(rows: list[str], h: int) -> list[str]:
    region = rows[3:h]
    if region and region[-1].lstrip().startswith(("▲", "▼")):
        region = region[:-1]
    return region

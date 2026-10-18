"""The backlog polish prototype round reaches the operator (batch
2026-10-18-batch-02, increment 003). HLR-1905 / LLR-1905.1 · AT-1905.

Why: the operator's standing rule — a TUI design change ships only after a
prototype round of REAL-APP renders and a verdict. A page that silently lacks
a capture, shows a "variant" identical to today's look, pulls a resource from
the network, embeds a picture that is not the app's own screenshot, or names
no recommendation would put a verdict on something nobody saw. The checker
below is run on the committed round and on corrupted copies of it, each of
which it must reject.

Retirement: this test and `prototypes/backlog_polish/` leave together, in the
batch that implements the operator's verdict.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import shutil
from pathlib import Path

ROUND = Path(__file__).resolve().parents[1] / "prototypes" / "backlog_polish"
PAGE = "backlog-polish-prototype.html"
POLISH = ("contrast", "hint80", "notecap")
SIZES = ("118x31", "80x25")


def _norm(svg: str) -> str:
    return re.sub(r"terminal-\d+", "terminal-N", svg)


def check_round(folder: Path) -> list[str]:
    """Every problem with the round in `folder`; empty when it is fit for a verdict."""
    problems = []
    page_path = folder / PAGE
    if not page_path.is_file():
        return [f"no page {PAGE}"]
    page = page_path.read_text(encoding="utf-8")
    if '<html lang="es"' not in page:
        problems.append("the page is not lang=es")
    if re.search(r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//|url\(\s*["']?(?:https?:)?//|@import""",
                 page):
        problems.append("the page loads an external resource")
    figures = dict(re.findall(r'<figure id="([^"]+)"[^>]*>.*?src="data:image/png;base64,([^"]+)"',
                              page, re.S))
    manifest = json.loads((folder / "out" / "manifest.json").read_text(encoding="utf-8"))
    ids = {e["id"] for e in manifest}
    svgs = {}
    for e in manifest:
        svg, png = folder / "out" / e["svg"], folder / "out" / (e["png"] or "")
        if not svg.is_file() or not e["png"] or not png.is_file():
            problems.append(f"{e['id']}: a capture is missing")
            continue
        if hashlib.sha256(svg.read_bytes()).hexdigest() != e["svg_sha256"]:
            problems.append(f"{e['id']}: the SVG's digest disagrees with the manifest")
        if hashlib.sha256(png.read_bytes()).hexdigest() != e["png_sha256"]:
            problems.append(f"{e['id']}: the PNG's digest disagrees with the manifest")
        if figures.get(e["id"]) != base64.b64encode(png.read_bytes()).decode():
            problems.append(f"{e['id']}: the page does not embed this capture's PNG")
        text = svg.read_text(encoding="utf-8").replace("&#160;", " ")
        if "terminal-" not in text or not ("PRESENT" in text or "36+" in text):
            problems.append(f"{e['id']}: not an app export of the presentation")
        if f'data-capture="{e["id"]}"' not in page:
            problems.append(f"{e['id']}: not on the page")
        svgs[e["id"]] = _norm(text)
    if page.count("data:image/png;base64,") != len(manifest):
        problems.append("the page does not embed one PNG per capture")
    for item in POLISH:
        mine = [e for e in manifest if e["item"] == item]
        looks = {e["look"] for e in mine}
        if "current" not in looks or len(looks) < 2:
            problems.append(f"{item}: no current look and variant")
        for e in mine:
            if e["size"] not in SIZES:
                problems.append(f"{e['id']}: an unexpected size")
        for look in looks - {"current"}:
            pairs = [(e["id"], f"{item}-current-{e['scene']}-{e['size']}")
                     for e in mine if e["look"] == look]
            if not any(svgs.get(a) is not None and svgs.get(a) != svgs.get(b) for a, b in pairs):
                problems.append(f"{item}: variant {look} shows nothing the current look does not")
            for a, b in pairs:                    # an equal capture is labelled as such
                same = svgs.get(a) is not None and svgs.get(a) == svgs.get(b)
                if same != bool(re.search(rf'<figure id="{a}"[^>]*data-same="current"', page)):
                    problems.append(f"{a}: equal to the current look but not labelled so"
                                    if same else f"{a}: labelled equal to the current look but differs")
            for size in SIZES:
                if not any(e["look"] == look and e["size"] == size for e in mine):
                    problems.append(f"{item}: variant {look} has no capture at {size}")
        m = re.search(rf'data-item="{item}" data-recommend="([^"]+)"', page)
        if not m or m.group(1) not in ids or not m.group(1).startswith(f"{item}-"):
            problems.append(f"{item}: no recommendation naming one of its captures")
    if not any(e["item"] == "narrow" for e in manifest):
        problems.append("the narrow frame is not shown for review")
    return problems


def _copy(tmp_path) -> Path:
    dst = tmp_path / "round"
    shutil.copytree(ROUND, dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def _manifest(folder: Path) -> list[dict]:
    return json.loads((folder / "out" / "manifest.json").read_text(encoding="utf-8"))


def test_AT_1905_the_round_is_fit_for_a_verdict(tmp_path):
    """AT-1905 (US-1903, HLR-1905): the committed round passes the checker;
    every corruption the checker exists for is rejected (the RED arms)."""
    assert check_round(ROUND) == []

    moved = _copy(tmp_path / "a")
    first = _manifest(moved)[0]
    (moved / "out" / first["svg"]).rename(moved / "out" / (first["svg"] + ".aside"))
    assert any("missing" in p for p in check_round(moved))

    same = _copy(tmp_path / "b")
    entries = _manifest(same)
    for e in entries:
        if e["item"] == "notecap" and e["look"] == "A":
            cur = same / "out" / f"notecap-current-{e['scene']}-{e['size']}.svg"
            shutil.copyfile(cur, same / "out" / e["svg"])
            e["svg_sha256"] = hashlib.sha256(cur.read_bytes()).hexdigest()
    (same / "out" / "manifest.json").write_text(json.dumps(entries), encoding="utf-8")
    assert "notecap: variant A shows nothing the current look does not" in check_round(same)

    ext = _copy(tmp_path / "c")
    page = ext / PAGE
    page.write_text(page.read_text(encoding="utf-8").replace(
        "</head>", '<link rel="stylesheet" href="https://cdn.example.com/x.css"></head>'), encoding="utf-8")
    assert "the page loads an external resource" in check_round(ext)

    fake = _copy(tmp_path / "d")
    entries = _manifest(fake)
    target = fake / "out" / entries[0]["svg"]
    target.write_text("<svg><text>PRESENT</text></svg>", encoding="utf-8")
    entries[0]["svg_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    (fake / "out" / "manifest.json").write_text(json.dumps(entries), encoding="utf-8")
    assert any("not an app export" in p for p in check_round(fake))

    drift = _copy(tmp_path / "e")
    target = drift / "out" / _manifest(drift)[0]["svg"]
    target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert any("digest disagrees" in p for p in check_round(drift))

    norec = _copy(tmp_path / "f")
    page = norec / PAGE
    text = page.read_text(encoding="utf-8")
    m = re.search(r'data-item="hint80" data-recommend="([^"]+)"', text)
    page.write_text(text.replace(m.group(0), 'data-item="hint80" data-recommend="contrast-A-gantt-long-118x31"'),
                    encoding="utf-8")
    assert "hint80: no recommendation naming one of its captures" in check_round(norec)

    unlabelled = _copy(tmp_path / "g")
    page = unlabelled / PAGE
    text = page.read_text(encoding="utf-8")
    assert ' data-same="current"' in text
    page.write_text(text.replace(' data-same="current"', "", 1), encoding="utf-8")
    assert any("equal to the current look but not labelled so" in p for p in check_round(unlabelled))

    swapped = _copy(tmp_path / "h")
    entries = _manifest(swapped)
    a, b = (swapped / "out" / entries[i]["png"] for i in (0, 1))
    pa, pb_ = a.read_bytes(), b.read_bytes()
    a.write_bytes(pb_)
    b.write_bytes(pa)
    assert any("the PNG's digest disagrees" in p for p in check_round(swapped))

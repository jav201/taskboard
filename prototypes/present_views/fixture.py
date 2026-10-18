"""The prototype's OWN copy of the present board: tests/present_board.py's
`build()` plus realistic multi-line notes, links and images on the Website
Redesign tasks. Synthetic data only. tests/ is never written.

Notes cover the states the content views must survive: a 5-line bulleted
note, a 3-paragraph note, a short one, one very long note (overflow), and one
empty note (empty state)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import present_board as pb  # noqa: E402

TODAY, PROJECT_ID, CURSOR = pb.TODAY, pb.PROJECT_ID, pb.CURSOR

NOTES = {
    "tw2": ("Design tokens are frozen at v2.3.\n"
            "- Buttons, inputs and cards: done\n"
            "- Modal and toast: in review with the design team\n"
            "- Data table: not started, needs the sorting spec\n"
            "Publish the storybook before Friday's review."),
    "tw3": ("The 500 comes from a missing tax-rate row for the three new regions "
            "(CL, PE, UY); checkout calls the rate service and gets nothing back.\n"
            "Hotfix PR #412 adds the rows and a guard that falls back to the "
            "default rate, with an alert when it does.\n"
            "If the fix is not green by end of day, roll back deploy 2026.09.27."),
    "tw4": ("Convert the hero images to AVIF and keep a JPEG fallback.\n"
            "Lazy-load everything below the fold.\n"
            "Target: homepage under 1.5 MB on a 4G profile."),
    "tw5": ("Go-live plan, agreed with marketing and support on Sep 22.\n"
            "1. Feature-flag the new homepage for internal users first, then 10 % "
            "of traffic for one full business day while we watch conversion, "
            "error rate and the p95 of the checkout page against last week.\n"
            "2. Lower the DNS TTL to 300 seconds two days before the cut-over so "
            "a rollback propagates in minutes, not hours.\n"
            "3. Support gets the FAQ and the macro set one week before; the "
            "status page draft is written in advance and kept unpublished.\n"
            "4. Rollback: flip the flag, restore the old sitemap, purge the CDN. "
            "The runbook lives in the ops wiki and was rehearsed on staging.\n"
            "Risks: the component library slipped three days; if the asset pass "
            "slips too, launch moves to the following Tuesday, never a Friday.\n"
            "Owner on call during launch: username_subject."),
    "tw6": "",
}
URLS = {
    "tw2": ["https://design-system.example.com/tokens"],
    "tw3": ["https://status.example.com/incident/4821",
            "https://git.example.com/web/pull/412"],
    "tw5": ["https://wiki.example.com/ops/launch-runbook",
            "https://flags.example.com/homepage-v2"],
}
IMAGES = {
    "tw2": ["mockups/library.png", "mockups/tokens.png"],
    "tw5": ["launch/timeline.png"],
}


def build(path: Path):
    b = pb.build(path)
    for t in b.tasks:
        if t.id in NOTES:
            t.notes = NOTES[t.id]
            t.urls = list(URLS.get(t.id, []))
            t.images = list(IMAGES.get(t.id, []))
    return b

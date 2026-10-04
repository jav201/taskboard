"""Minimise the TaskDetails blank grid: one Grid of Labels inside a VerticalScroll,
CSS variants toggled one at a time; print each Label's painted height."""
import asyncio
from textual.app import App
from textual.containers import Grid, VerticalScroll
from textual.widgets import Label, Input

BASE = """
.modal-grid { grid-size: 2; grid-columns: 20 1fr; grid-gutter: 0 1; height: auto; }
.modal Label { margin-top: 1; }
.modal-grid Label { margin-top: 1; content-align: left middle; height: 3; }
"""
VARIANTS = {
    "shipped": BASE,
    "no-margin": BASE + ".modal-grid Label { margin-top: 0; }",
    "no-height3": BASE + ".modal-grid Label { height: auto; }",
    "rows-auto": BASE + ".modal-grid { grid-rows: auto; }",
    "rows-3": BASE + ".modal-grid { grid-rows: 3; }",
    "rows-4": BASE + ".modal-grid { grid-rows: 4; }",
    "fix-scoped": BASE + "#details-box .modal-grid Label { margin-top: 0; height: 1; }",
}

def make(css, with_input=False):
    class A(App):
        CSS = css
        def compose(self):
            with VerticalScroll(classes="modal", id="details-box"):
                with Grid(classes="modal-grid"):
                    for k, v in [("Project", "Alpha"), ("Phase", "Doing")]:
                        yield Label(k)
                        yield (Input(v) if with_input else Label(v))
    return A()

async def run(name, css, with_input=False):
    app = make(css, with_input)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        g = app.query_one(Grid)
        hs = [(type(w).__name__, w.region.height, w.region.y) for w in g.children]
        print(f"{name:12} input={with_input!s:5} grid h={g.region.height} cells={hs}")

async def main():
    for n, c in VARIANTS.items():
        await run(n, c)
    await run("shipped", BASE, with_input=True)
asyncio.run(main())

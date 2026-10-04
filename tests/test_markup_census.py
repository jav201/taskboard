"""No user-authored or synced text reaches a Textual widget, or a markup parser (S1).

Security review S1 (batch 2026-09-30-batch-01), S-5 (batch 2026-10-02-batch-02) and
the P2 review of batch 2026-10-02-batch-04 (Q-1, S-2, S-4): Textual parses a `str`
handed to a `Label`, `Static`, `Option`, `Select` prompt, `Button` label or `notify`
as ITS markup, and `rich.markup.escape` only escapes what RICH would read as a tag —
so `Label(escape("[LINK=http://e]x"))` raises `MarkupError` and the screen dies.
Escaping and re-parsing with Rich (`_rich`) does not repair it either: a trailing
backslash doubles, `:smile:` becomes an emoji, and an unescaped piece becomes a tag —
a clickable `[@click=…]` action from a teammate's `team.json` (S-1, HIGH).

The rule (operator ruling 2, "Piezas de texto, sin formato"): user and synced text
is a Rich `Text` PIECE; it never meets a parser. The census below is DERIVED, never
hand-listed (C-31): it walks every module in `taskboard/` that imports Textual,
finds every call that hands a value to a Textual markup sink and every call to a
markup parser, and requires each value to be markup-inert — an app literal, a
`Text` built without a parser, a parser over an app literal, a call to a function
annotated `-> Text` that is defined in a censused module and whose every `return`
is itself markup-inert (every same-named definition, code review F1/G1), or, for
`notify`, `markup=False`. A new site fed anything else
turns this RED, by file, line and source. HLR-401, LLR-401.1, LLR-401.2, LLR-401.3.

Out of its reach, declared: the board renderers in `views.py` (they import no
Textual; their seat is Rich markup built with `escape`, BACKLOG `collapse_runs` S-2),
reached from here only by the two board repaints, which EXEMPT names (D-405).
"""
from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

import textual.widgets
import textual.widgets.option_list
from textual.app import App
from textual.widgets import OptionList, Select, Static

PKG = Path(__file__).resolve().parents[1] / "taskboard"

# The first constructor parameter names Textual renders as markup when given a str
# (textual 8.2.8: Label/Static `content`, Button/Checkbox `label`, Option `prompt`,
# Select `options` = (prompt, value) pairs, OptionList `*content`).
MARKUP_PARAMS = {"content", "label", "prompt", "options"}
# Widgets the package imports whose first parameter is plain text, never markup.
PLAIN_WIDGETS = {"Input": "value is plain text", "TextArea": "text is plain text"}
# Method sinks: each takes its markup-bearing value as the first argument.
METHOD_SINKS = {"notify", "update", "add_option", "add_options", "set_options",
                "replace_option_prompt", "replace_option_prompt_at_index"}
# Attribute and keyword sinks: assigning or passing a str parses it as markup.
ATTR_SINKS = {"border_title", "border_subtitle", "tooltip"}
# Builders of a Text that read no markup; and the parsers, safe only over a literal.
TEXT_BUILDERS = {"Text", "assemble"}
PARSERS = {"_rich", "from_markup", "from_ansi"}

# Sites whose markup is built ONLY from app constants, so no user or synced text can
# reach them — and the two board repaints, whose seat is views.py's own (D-405). Keyed by (module, enclosing function, sink, the value's source text):
# a new value fed into one of these functions is a new key, and RED (S-7, Q-8).
EXEMPT = {
    ("keymap.py", "KeyBar.refresh_bar", "update",
     "markup <- render_key_bar(max(0, width), self.view_mode, self.bar_layer)"):
        "the key bar: render_key_bar over the keymap contract (app constants)",
    ("ribbon.py", "Ribbon.update_clock", "update", "markup <- ' ' + sep.join(parts) + ' '"):
        "the clocks: city names validated against CITY_TO_ZONE (Board._resolve_clock)",
    ("app.py", "HelpScreen.compose", "Static", "'\\n'.join(rows)"):
        "the full keymap: binding keys and descriptions (app constants)",
    ('app.py', 'TaskboardApp._repaint_flow', 'update',
     'render_view(self.view_mode, self.board, self.show_archived, self.selected_task_id, width=bw.size.width or 0, height=h, line_map=self._line_map, presentation=self.kanban_presentation, tick=self._tick_n, kanban_sort=self.kanban_sort, kanban_group=self.kanban_group, kanban_collapsed=self.kanban_collapsed, kanban_focus=self.focused_project_id, gantt_focus=self.focused_project_id, gantt_previous=self._gantt_previous, lanes_presentation=self.lanes_presentation, focus_presentation=self.focus_presentation, search_query=self.search_query, team_state=self.team_state, team_filter=self.team_filter)'):
        "the board seat: views.render_view builds Rich markup with escape (D-405, out of this census)",
    ('app.py', 'TaskboardApp.refresh_view', 'update',
     'content <- render_view(self.view_mode, self.board, self.show_archived, self.selected_task_id, width=w, height=h, line_map=self._line_map, presentation=self.kanban_presentation, tick=self._tick_n, kanban_sort=self.kanban_sort, kanban_group=self.kanban_group, kanban_collapsed=self.kanban_collapsed, kanban_focus=self.focused_project_id, gantt_focus=self.focused_project_id, gantt_previous=self._gantt_previous, lanes_presentation=self.lanes_presentation, focus_presentation=self.focus_presentation, search_query=self.search_query, team_state=self.team_state, team_filter=self.team_filter, setup_state=self._setup_state)'):
        "the board seat: views.render_view builds Rich markup with escape (D-405, out of this census)",
    ("modals.py", "HelpModal.compose", "from_markup", "example"):
        "help_example(mode): a constant example per view",
    ("modals.py", "HelpModal.compose", "from_markup", "swatch"):
        "legend_entries: swatches built from the palette (app constants)",
}


def _imports_textual(tree: ast.AST) -> bool:
    return any(isinstance(n, ast.ImportFrom) and (n.module or "").startswith("textual")
               for n in ast.walk(tree))


def _imported_widgets(tree: ast.AST) -> dict[str, type]:
    out = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.ImportFrom)
                and node.module in ("textual.widgets", "textual.widgets.option_list")):
            mod = sys.modules[node.module]
            for alias in node.names:
                cls = getattr(mod, alias.name, None)
                if inspect.isclass(cls):
                    out[alias.asname or alias.name] = cls
    return out


def _widget_sinks(tree: ast.AST) -> dict[str, str]:
    """{local name: markup parameter} for every Textual widget class the module
    imports whose FIRST constructor parameter is rendered as markup — derived from
    Textual's own signatures, not listed by hand."""
    out = {}
    for name, cls in _imported_widgets(tree).items():
        params = list(inspect.signature(cls.__init__).parameters.values())[1:]
        if params and params[0].name in MARKUP_PARAMS:
            out[name] = params[0].name
    return out


def _text_functions(trees) -> dict[str, list[ast.FunctionDef]]:
    """Functions annotated to return a Rich `Text` (or a list of them), defined
    in a CENSUSED module only. An annotation is a claim, not a proof: the judge
    trusts a call to one of these only when every `return` of its definition is
    itself markup-inert (code review F1: a lying `-> Text`, or a `-> Text` that
    parses its argument, would otherwise pass)."""
    defs = {}
    for tree in trees:
        if not _imports_textual(tree):
            continue
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.returns is not None:
                if ast.unparse(n.returns) in ("Text", "list[Text]"):
                    defs.setdefault(n.name, []).append(n)   # a name can repeat (G1)
    return defs


def _call_name(call: ast.Call) -> str | None:
    f = call.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None


def _parser_names(tree: ast.AST) -> set[str]:
    """The names a module can call a markup parser by: the parsers themselves,
    `render` imported from `rich.markup`, and any name bound to a parser
    attribute (`fm = Text.from_markup`) — an alias is a parser (S2-3)."""
    names = set(PARSERS)
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom) and n.module == "rich.markup":
            names |= {a.asname or a.name for a in n.names if a.name == "render"}
        if (isinstance(n, ast.Assign) and isinstance(n.value, ast.Attribute)
                and n.value.attr in PARSERS | {"render"}):
            names |= {t.id for t in n.targets if isinstance(t, ast.Name)}
    return names


def _is_parser(call: ast.Call, parsers: set[str]) -> bool:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id in parsers
    if isinstance(f, ast.Attribute):
        return f.attr in PARSERS or (f.attr == "render"
                                     and ast.unparse(f.value).endswith("markup"))
    return False


class _Census(ast.NodeVisitor):
    """Collect (qualname, sink, value node, notify-markup-off, kind) per site; a
    site of kind "parser" is a parser call, wherever it sits."""

    def __init__(self, sinks: dict[str, str], parsers: set[str]):
        self.sinks, self.parsers = sinks, parsers
        self.stack, self.funcs, self.sites = [], [], []

    def _scope(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_ClassDef(self, node):
        self._scope(node)

    def visit_FunctionDef(self, node):
        self.funcs.append(node)
        self._scope(node)
        self.funcs.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def _add(self, node, sink, value, markup_off=False, kind="sink", pair=False):
        self.sites.append({"qual": ".".join(self.stack), "sink": sink, "line": node.lineno,
                           "value": value, "markup_off": markup_off, "kind": kind,
                           "pair": pair, "func": self.funcs[-1] if self.funcs else None})

    def visit_Call(self, node):
        name = _call_name(node)
        kw = {k.arg: k.value for k in node.keywords}
        f = node.func
        if _is_parser(node, self.parsers):
            value = node.args[0] if node.args else next(iter(kw.values()), None)
            if value is not None:
                self._add(node, name, value, kind="parser")
        elif isinstance(f, ast.Name) and name in self.sinks:
            value = node.args[0] if node.args else kw.get(self.sinks[name])
            if name == "OptionList":
                for a in node.args:
                    self._add(node, name, a)
            elif value is not None:
                self._add(node, name, value, pair=name == "Select")
            if name == "Select" and "prompt" in kw:
                self._add(node, "Select(prompt=)", kw["prompt"])
        elif (isinstance(f, ast.Attribute) and name == "from_values"
              and isinstance(f.value, ast.Name) and f.value.id in self.sinks):
            value = node.args[0] if node.args else kw.get("values")
            if value is not None:
                self._add(node, "Select.from_values", value)
        elif isinstance(f, ast.Attribute) and name in METHOD_SINKS:
            if name.startswith("replace_option") and node.args:
                value = node.args[-1]
            else:
                value = node.args[0] if node.args else next(
                    (kw[k] for k in ("message", "content", "option", "options", "prompt")
                     if k in kw), None)
            if value is not None:
                off = (name == "notify" and isinstance(kw.get("markup"), ast.Constant)
                       and kw["markup"].value is False)
                self._add(node, name, value, off, pair=name == "set_options")
        elif (isinstance(f, ast.Name) and name == "setattr" and len(node.args) == 3
              and isinstance(node.args[1], ast.Constant) and node.args[1].value in ATTR_SINKS):
            self._add(node, node.args[1].value, node.args[2])
        if "tooltip" in kw:
            self._add(node, "tooltip=", kw["tooltip"])
        self.generic_visit(node)

    def visit_Assign(self, node):
        for t in node.targets:
            if isinstance(t, ast.Attribute) and t.attr in ATTR_SINKS:
                self._add(node, t.attr, node.value)
        self.generic_visit(node)


def _assignments(func, name: str):
    """Every value bound to `name` in `func`; None when `name` is a parameter,
    a loop/with/comprehension target, a tuple-unpack target, or bound by anything
    but a plain `=` (S2-3: an unpacking rebinding is not trusted)."""
    if func is None:
        return None
    args = func.args
    if name in {a.arg for a in args.args + args.kwonlyargs + args.posonlyargs}:
        return None
    values = []
    for n in ast.walk(func):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    values.append(n.value)
                elif isinstance(t, (ast.Tuple, ast.List)) and name in {
                        x.id for x in ast.walk(t) if isinstance(x, ast.Name)}:
                    return None
        elif isinstance(n, (ast.For, ast.comprehension, ast.With, ast.AugAssign,
                            ast.AnnAssign, ast.NamedExpr)):
            targets = ([n.target] if hasattr(n, "target") else
                       [i.optional_vars for i in n.items if i.optional_vars])
            if any(isinstance(t, ast.AST) and name in {x.id for x in ast.walk(t)
                                                       if isinstance(x, ast.Name)}
                   for t in targets):
                return None
    return values or None


def _literal(node) -> bool:
    """An app literal: a str constant, or literals joined by `+` / chosen by `if`."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, str)
    if isinstance(node, ast.IfExp):
        return _literal(node.body) and _literal(node.orelse)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _literal(node.left) and _literal(node.right)
    if isinstance(node, ast.JoinedStr):
        return all(isinstance(v, ast.Constant) for v in node.values)
    return False


def _source(value, func) -> str:
    """A site's value as source text; a bare name carries its bindings, so an
    exemption keyed on it breaks when the binding changes (S2-5)."""
    text = ast.unparse(value)
    if isinstance(value, ast.Name):
        bound = _assignments(func, value.id)
        if bound:
            text += " <- " + " | ".join(ast.unparse(b) for b in bound)
    return text


class _Judge:
    """The safety rule over one module: what counts as markup-inert."""

    def __init__(self, text_fns, sinks, parsers, exempt_parsers):
        self.text_fns, self.sinks = text_fns, sinks
        self.parsers, self.exempt_parsers = parsers, exempt_parsers
        self._judging: set[str] = set()

    def trusted_text_call(self, call) -> bool:
        """A censused `-> Text` function called by its bare name or as a method
        of `self` (not any call that merely shares the name, Q2-10), whose every
        `return` is itself markup-inert (F1). A recursive call is not trusted."""
        f = call.func
        if isinstance(f, ast.Name):
            name = f.id
        elif (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)
              and f.value.id == "self"):
            name = f.attr
        else:
            return False
        fns = self.text_fns.get(name)
        if not fns or name in self._judging:
            return False
        self._judging.add(name)
        try:
            return all(self._returns_inert(fn) for fn in fns)   # every namesake (G1)
        finally:
            self._judging.discard(name)

    def _returns_inert(self, fn) -> bool:
        returns = [r.value for r in ast.walk(fn)
                   if isinstance(r, ast.Return) and r.value is not None]
        return bool(returns) and all(self.safe(r, fn) for r in returns)

    def text_builder(self, call) -> bool:
        f = call.func
        if isinstance(f, ast.Name):
            return f.id in TEXT_BUILDERS or f.id in self.sinks
        return (isinstance(f, ast.Attribute) and f.attr in TEXT_BUILDERS
                and ast.unparse(f.value) == "Text")

    def safe(self, node, func, pair=False) -> bool:
        s = lambda n, p=pair: self.safe(n, func, p)       # noqa: E731
        if _literal(node):
            return True
        if isinstance(node, ast.IfExp):
            return s(node.body) and s(node.orelse)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return s(node.left) and s(node.right)        # list + list of options
        if isinstance(node, ast.Call):
            if _is_parser(node, self.parsers):
                arg = node.args[0] if node.args else None
                return arg is not None and (
                    _literal(arg) or _source(arg, func) in self.exempt_parsers)
            return self.text_builder(node) or self.trusted_text_call(node)
        if isinstance(node, ast.Starred):
            return s(node.value)
        if isinstance(node, ast.Tuple) and pair:
            return bool(node.elts) and s(node.elts[0], False)
        if isinstance(node, (ast.List, ast.Tuple)):
            return all(s(e) for e in node.elts)
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            return s(node.elt)
        if isinstance(node, ast.Name):
            values = _assignments(func, node.id)
            return values is not None and all(s(v) for v in values)
        return False


def census(sources: dict[str, str]) -> list[dict]:
    """Every Textual markup-sink site and every parser call in `sources` ({module
    file name: source}), each with `safe` set. Pure: the planted-module tests feed
    it a fake module."""
    trees = {name: ast.parse(src) for name, src in sources.items()}
    text_fns = _text_functions(trees.values())
    out = []
    for name, tree in trees.items():
        if not _imports_textual(tree):
            continue
        sinks, parsers = _widget_sinks(tree), _parser_names(tree)
        v = _Census(sinks, parsers)
        v.visit(tree)
        exempt_parsers = {k[3] for k in EXEMPT if k[0] == name and k[2] in parsers | {"render"}}
        judge = _Judge(text_fns, sinks, parsers, exempt_parsers)
        for site in v.sites:
            site["module"] = name
            site["source"] = _source(site["value"], site["func"])
            if site["kind"] == "parser":
                site["safe"] = _literal(site["value"])
            else:
                site["safe"] = site["markup_off"] or judge.safe(
                    site["value"], site["func"], pair=site["pair"])
            out.append(site)
    return out


def _key(s: dict) -> tuple:
    return (s["module"], s["qual"], s["sink"], s["source"])


def _sources() -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(PKG.glob("*.py"))}


def _package_census() -> list[dict]:
    return census(_sources())


def _report(sites) -> str:
    return "\n".join(f"  {s['module']}:{s['line']} {s['qual']} {s['sink']}({s['source'][:80]})"
                     for s in sites)


def test_TC_401_no_textual_sink_takes_a_markup_str():
    """TC-401 (LLR-401.1). Every site in the package that hands a value to a
    Textual markup sink hands it markup-inert. RED on base: the census lists the
    str sites (ConfirmModal / TextPrompt titles, Option and Select labels, the
    notifies carrying ids, names and exceptions, the standup and help labels) and
    every `_rich` over user text; GREEN once each is a Text piece or `markup=False`."""
    unsafe = [s for s in _package_census()
              if s["kind"] == "sink" and not s["safe"] and _key(s) not in EXEMPT]
    assert not unsafe, "Textual sinks fed a markup str:\n" + _report(unsafe)


def test_TC_402_every_exemption_names_one_live_site():
    """TC-402 (LLR-401.1). The exemptions are a declared set, guarded both ways: an
    exemption whose site is gone turns this RED, and each names exactly one live
    site by its value's source text — a new value fed into an exempt function is a
    new key, flagged by TC-401 or TC-406, never excused (S-7, Q-8)."""
    keys = [_key(s) for s in _package_census()]
    stale = sorted(k for k in EXEMPT if keys.count(k) != 1)
    assert not stale, f"exemptions not matching exactly one live site: {stale}"


def test_TC_406_no_user_value_reaches_a_markup_parser():
    """TC-406 (LLR-401.3). Every markup parser call in a module that talks to
    Textual takes an app literal: user and synced text is a `Text` piece, never
    parsed (operator ruling 2; P2 Q-1/S-2/S-4). RED on base: the `_rich(...)`
    calls over escaped titles, URLs and image refs and `notes_preview`'s
    `Text.from_markup` over the highlighted notes."""
    unsafe = [s for s in _package_census()
              if s["kind"] == "parser" and not s["safe"] and _key(s) not in EXEMPT]
    assert not unsafe, "markup parsers fed a non-literal:\n" + _report(unsafe)


PLANTED = """
from rich.markup import escape, render
from textual.widgets import Label, Select, Static, Button, OptionList
from textual.widgets.option_list import Option
from rich.text import Text

def _rich(m) -> Text:
    return Text.from_markup(m)

def title_text(t) -> Text:
    return Text(t)

def _lie(x) -> Text:
    return x

def _parsed(x) -> Text:
    return Text.from_markup(x)

def piece(x) -> Text:
    return x

class Honest:
    def piece(self, x) -> Text:
        return Text(x)

fm = Text.from_markup

class Box:
    def compose(self, task, names, err, w, o):
        yield Label(task.title)                            # sink: attribute
        yield Label(f"[b]{task.title}[/b]")                 # sink: f-string
        yield Option(name)                                 # sink: free name
        yield Select([(n, n) for n in names])              # sink: prompt is str
        yield Button(self.confirm)                         # sink: attribute
        self.notify(f"failed: {err}")                      # sink: markup on
        self.border_title = task.title                     # sink: attribute sink
        label = "Saved " + task.title
        yield Static(label)                                # sink: bound to a str
        yield Label(_rich(f"[b]{escape(task.title)}[/b]"))  # sink + parser over user text
        yield Label("x", tooltip=task.title)               # sink: tooltip keyword
        w.tooltip = task.title                             # sink: .tooltip =
        w.border_subtitle = task.notes                     # sink: border_subtitle
        w.set_options([(n, n) for n in names])             # sink: set_options pairs
        o.replace_option_prompt("id", task.title)          # sink: replace_option_prompt
        w.update(content=task.title)                       # sink: keyword method sink
        yield Static(render(task.notes))                   # sink + parser: rich.markup.render
        yield Static(fm(task.notes))                       # sink + parser: an alias
        pair = Text(task.title)
        pair, _ = task.title, 1                            # the rebinding a census must not trust
        yield Label(pair)                                  # sink: tuple-unpack rebinding
        yield Select.from_values(names)                    # sink: Select.from_values
        yield Select([], prompt=task.title)                # sink: Select(prompt=)
        setattr(w, "border_title", task.title)             # sink: setattr
        yield Label(o.title_text(task.title))              # sink: a method named like a -> Text fn
        yield Label(_lie(task.title))                      # sink: a -> Text that returns its str
        yield Label(_parsed(task.title))                   # sink: a -> Text that parses its argument
        yield Label(piece(task.title))                     # sink: a lying namesake of an honest method
        yield Select([(Text("none"), 0)] + [(n, n) for n in names])   # sink: + with a str prompt
        yield Select([(Text("none"), 0)] + [(Text(n), n) for n in names])  # safe: + of Text prompts
        yield Label("[b]Literal[/b]")                      # safe: app literal
        yield Label(_rich("[b]Literal[/b]"))               # safe: a parser over a literal
        yield Label(Text.assemble((task.title, "bold"), " — x"))   # safe: pieces
        yield Select([(Text(n), n) for n in names])        # safe: Text prompts
        self.notify(f"failed: {err}", markup=False)        # safe: markup off
        shown = Text(task.title)
        yield Static(shown)                                # safe: bound to Text
        yield Label(title_text(task.title))                # safe: a bare-name -> Text call
        Text.from_markup(task.notes)                       # parser: unsafe
        Text.from_markup("[dim]—[/dim]")                   # parser: safe
"""


def test_TC_403_the_census_finds_planted_sites():
    """TC-403 (LLR-401.1, LLR-401.3). The census can produce a NON-absence (C-55
    rider): over a planted module it flags every unsafe sink form the P2 reviews
    found (Q2-9, Q2-10, S2-3) and every parser over user text, and passes each safe
    form. RED if the scanner is narrowed (a sink kind dropped, a name trusted
    without its binding, an alias or `render` missed, a parser over user text
    trusted) — a scanner that finds nothing would make TC-401 and TC-406
    vacuously green."""
    sites = census({"planted.py": PLANTED})
    flagged = sorted((s["kind"], s["sink"], s["source"]) for s in sites if not s["safe"])
    passed = sorted((s["kind"], s["sink"], s["source"]) for s in sites if s["safe"])
    assert flagged == sorted([
        ("sink", "Label", "task.title"), ("sink", "Label", "f'[b]{task.title}[/b]'"),
        ("sink", "Option", "name"), ("sink", "Select", "[(n, n) for n in names]"),
        ("sink", "Button", "self.confirm"), ("sink", "notify", "f'failed: {err}'"),
        ("sink", "border_title", "task.title"),
        ("sink", "Static", "label <- 'Saved ' + task.title"),
        ("sink", "Label", "_rich(f'[b]{escape(task.title)}[/b]')"),
        ("parser", "_rich", "f'[b]{escape(task.title)}[/b]'"),
        ("sink", "tooltip=", "task.title"), ("sink", "tooltip", "task.title"),
        ("sink", "border_subtitle", "task.notes"),
        ("sink", "set_options", "[(n, n) for n in names]"),
        ("sink", "replace_option_prompt", "task.title"),
        ("sink", "update", "task.title"),
        ("sink", "Static", "render(task.notes)"), ("parser", "render", "task.notes"),
        ("sink", "Static", "fm(task.notes)"), ("parser", "fm", "task.notes"),
        ("sink", "Label", "pair"), ("sink", "Select.from_values", "names"),
        ("sink", "Select(prompt=)", "task.title"), ("sink", "border_title", "task.title"),
        ("sink", "Label", "o.title_text(task.title)"),
        ("sink", "Label", "_lie(task.title)"), ("sink", "Label", "_parsed(task.title)"),
        ("sink", "Label", "piece(task.title)"),
        ("parser", "from_markup", "x"),
        ("sink", "Select", "[(Text('none'), 0)] + [(n, n) for n in names]"),
        ("parser", "from_markup", "task.notes"), ("parser", "from_markup", "m"),
    ]), flagged
    assert passed == sorted([
        ("sink", "Label", "'x'"), ("sink", "Label", "'[b]Literal[/b]'"),
        ("sink", "Label", "_rich('[b]Literal[/b]')"),
        ("parser", "_rich", "'[b]Literal[/b]'"),
        ("sink", "Label", "Text.assemble((task.title, 'bold'), ' — x')"),
        ("sink", "Select", "[(Text(n), n) for n in names]"),
        ("sink", "notify", "f'failed: {err}'"),
        ("sink", "Select", "[]"),
        ("sink", "Select", "[(Text('none'), 0)] + [(Text(n), n) for n in names]"),
        ("sink", "Static", "shown <- Text(task.title)"),
        ("sink", "Label", "title_text(task.title)"),
        ("parser", "from_markup", "'[dim]—[/dim]'"),
    ]), passed


def test_TC_404_the_census_population_is_not_empty():
    """TC-404 (LLR-401.1). A guard on the derived set (C-31): the package census
    reaches every sink kind the app uses and a population no smaller than the one
    measured at P1 minus slack; every method sink is a real Textual API; and every
    widget class the package imports from Textual is a censused sink or a declared
    plain-text widget — so a scanner that silently stops matching, or a new widget
    whose markup parameter is not in the list, cannot pass (S-6)."""
    sources = _sources()
    sites = census(sources)
    kinds = {s["sink"] for s in sites if s["kind"] == "sink"}
    assert {"Label", "Static", "Option", "Select", "Button", "Checkbox", "OptionList",
            "notify", "update", "add_option", "add_options"} <= kinds, kinds
    assert len([s for s in sites if s["kind"] == "sink"]) >= 140
    for m in METHOD_SINKS:
        assert any(hasattr(c, m) for c in (App, OptionList, Static, Select)), m
    for name, src in sources.items():
        tree = ast.parse(src)
        unknown = set(_imported_widgets(tree)) - set(_widget_sinks(tree)) - set(PLAIN_WIDGETS)
        assert not unknown, f"{name}: Textual widgets neither censused nor declared plain: {unknown}"


def _escaped_notifies(sources: dict[str, str]) -> list[str]:
    """`notify(..., markup=False)` calls whose message holds an `escape(...)`
    call, directly or through a name bound in the same function."""
    out = []
    for name, src in sources.items():
        tree = ast.parse(src)
        funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        for fn in funcs:
            for call in ast.walk(fn):
                if not (isinstance(call, ast.Call) and _call_name(call) == "notify"):
                    continue
                kw = {k.arg: k.value for k in call.keywords}
                off = isinstance(kw.get("markup"), ast.Constant) and kw["markup"].value is False
                if not off or not call.args:
                    continue
                parts = [call.args[0]]
                names = {n.id for n in ast.walk(call.args[0]) if isinstance(n, ast.Name)}
                parts += [a.value for a in ast.walk(fn) if isinstance(a, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id in names for t in a.targets)]
                if any(isinstance(n, ast.Call) and _call_name(n) == "escape"
                       for part in parts for n in ast.walk(part)):
                    out.append(f"{name}:{call.lineno}")
    return out


def test_TC_405_a_markup_off_notify_shows_the_raw_text():
    """TC-405 (LLR-401.2). With markup off Textual paints the message as is, so an
    `escape()` inside it would paint its backslash before the bracket. No
    markup-off notify in the package builds its message with `escape`; a planted
    one is flagged, so the check can go RED."""
    assert _escaped_notifies({"planted.py": PLANTED_NOTIFY}) == ["planted.py:6", "planted.py:7"]
    found = _escaped_notifies(_sources())
    assert not found, found


PLANTED_NOTIFY = """from textual.app import App
from rich.markup import escape
class A(App):
    def f(self, name):
        shown = escape(name)
        self.notify(f'{shown} pinned', markup=False)
        self.notify(f'{escape(name)} done', markup=False)
        self.notify(f'{name} done', markup=False)
"""

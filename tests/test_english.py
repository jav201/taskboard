"""The app speaks English (answer D12, "Todo en inglés").

Batch 2026-10-02-batch-02 · HLR-204 · AT-204 · TC-206.

Field report (batch-01 D12): the views had followed the English verdict frames
(`chain 4`, `past due`) while the help modal's prose, Setup, the flow view and the
team filter stayed Spanish — two languages on one screen. The operator chose
English throughout. Stored values are data and stay as they are (the filter's
`todo`/`equipo`/`personal`); only what is PAINTED changes.

The lexicon is whole Spanish words that do not occur in English plus accented
letters; it is GUARDED by a control corpus copied verbatim from the base tree's
painted strings, so a lexicon that has gone blind turns RED here first.
"""
from __future__ import annotations

import re
from datetime import date

import pytest
from rich.cells import cell_len

import kg_board
from kg_board import TODAY
from taskboard import app as app_mod
from taskboard import models, views
from taskboard.app import VIEW_KEYS, VIEW_ORDER, TaskboardApp
from taskboard.views import help_example, help_usage, render_view

# The Spanish vocabulary increment 003 REMOVED, derived from the base tree's literals
# (`evidence/spanish_vocab.py`: the words of a0e7d9a's views/team_sync/modals literals
# minus the words still in them, minus words that are also English) and frozen here —
# never a hand-picked sample (code review F1, C-31). The 8 words dropped as also
# English: actual, del, dice, nada, persona, solo, tope, visible.
WORDS = (
    'abiertas', 'abierto', 'abiertos', 'abre', 'abrir', 'agrega', 'agrupar', 'ahí', 'aire',
    'ajustado', 'alcanzable', 'alta', 'altas', 'alterna', 'anotar', 'antes', 'antigüedad',
    'arriba', 'asesorios', 'atención', 'atora', 'atoró', 'aún', 'baja', 'banda', 'bloquean',
    'cabe', 'cada', 'cadena', 'cambia', 'campo', 'cancela', 'carga', 'cargada', 'cargó',
    'celda', 'ceniza', 'cerrados', 'cicla', 'ciclo', 'cierra', 'columna', 'compartida',
    'compartido', 'compartidos', 'compañero', 'completa', 'completadas', 'completo',
    'computan', 'con', 'configurar', 'conjunta', 'construye', 'crítica', 'cuantificar',
    'curso', 'curva', 'cuánto', 'dato', 'demasiado', 'demás', 'dentro', 'dependen', 'derecha',
    'desbloquea', 'desde', 'dibujado', 'directorio', 'distancia', 'donde', 'día', 'días',
    'dónde', 'edad', 'edición', 'edita', 'eje', 'ejemplo', 'ella', 'entre', 'entrega',
    'envejece', 'envejecimiento', 'esa', 'escanear', 'esconde', 'escribe', 'escribible',
    'escribir', 'espacio', 'espera', 'está', 'exactas', 'existe', 'falta', 'fase', 'fases',
    'fechada', 'fechas', 'fila', 'frente', 'frescura', 'funciona', 'grupo', 'guarda', 'hace',
    'haces', 'hasta', 'hechas', 'historia', 'horas', 'horizonte', 'hoy', 'igual', 'imágenes',
    'intervalo', 'intervalos', 'inválido', 'juzga', 'las', 'lee', 'leer', 'lento', 'leyenda',
    'lleva', 'los', 'luego', 'léelo', 'líder', 'mapa', 'marca', 'marcas', 'mediana', 'medidor',
    'mente', 'meses', 'miembro', 'mira', 'mirar', 'misma', 'mover', 'movimiento', 'muestra',
    'más', 'navega', 'necesita', 'nombrando', 'nunca', 'número', 'números', 'operar', 'orden',
    'otra', 'paleta', 'para', 'pasó', 'pinea', 'pineada', 'pineaste', 'plegado', 'pliega',
    'por', 'presentaciones', 'presentación', 'presión', 'primero', 'prioridad', 'progreso',
    'propósito', 'proyecto', 'proyectos', 'que', 'queda', 'quieto', 'quita', 'quién', 'qué',
    'regla', 'reposo', 'respira', 'resto', 'rojo', 'ruido', 'rótulo', 'sección',
    'seleccionado', 'semana', 'siempre', 'sin', 'sobre', 'sube', 'tablero', 'tarda', 'tarea',
    'tareas', 'tarjeta', 'tarjetas', 'teclas', 'termina', 'tiene', 'tocar', 'tolerancia',
    'trabajo', 'tras', 'una', 'urgencia', 'uso', 'veces', 'vence', 'verificado', 'viaja',
    'visibilidad', 'vista', 'vistazo', 'válido', 'ésta', 'último',
)
# The STORED values are data and stay Spanish in the code (D-212) — but they must
# never be PAINTED again, so the painted-text lexicon carries them too.
STORED = {"todo", "equipo", "personal", "modo", "carpeta", "alcance", "identidad",
          "proyectos", "roster", "sync"}
PAINT_TOO = ("equipo", "modo", "carpeta", "alcance", "identidad")   # not English words
# Frequent Spanish function and UI words a NEW Spanish string would likely carry
# (code review X1: "ninguna ruta" shares no word with the base copy). Declared
# limit, as the privacy sweep declares its floor: Spanish built only of words in
# neither list passes unseen — the lists catch the old copy and the common case,
# not every Spanish sentence.
FREQUENT = ("ninguna", "ninguno", "ruta", "archivo", "usuario", "configuración", "guardar",
            "guardado", "cancelar", "aceptar", "borrar", "eliminar", "nuevo", "nueva",
            "buscar", "cerrar", "ayuda", "salir", "listo", "pendiente", "vacío", "vacía",
            "también", "pero", "porque", "cuando", "muy", "aquí", "ahora", "todos",
            "todas", "esto", "este", "estos", "estas", "eso", "fue", "ser", "puede",
            "debe", "así", "mismo", "error de", "sí")
# accented letters too: the scanned surfaces carry no proper noun (no city, no
# fixture name) — a ribbon or zone-picker scan would need its own allowance (F4)
SPANISH = re.compile(r"(?i)\b(" + "|".join(WORDS + PAINT_TOO + FREQUENT) + r")\b|[áéíóúñ¿¡]")
WORD_ONLY = re.compile(r"(?i)\b(" + "|".join(WORDS) + r")\b")

# Painted by the base tree (a0e7d9a), copied from its source verbatim — the
# lexicon's positive control (qa P2 Q-10). One per surface this batch translates.
BASE_SPANISH = [
    "para qué es", "lo primero que haces", "los números de la tarjeta",   # help_usage
    "la distancia al ╎ ES la urgencia; nada más hace falta",             # help_example
    "sin historia aún — se construye desde hoy", "en curso n=1",          # flow
    " · equipo · proyectos · roster", "modo equipo", "carpeta compartida",  # Setup
    " sección   ", " compartido ", "proyectos del equipo",
    "team.json falta o es inválido", "existe y es escribible", "sin sync aún",  # checks
    "Uso", "Leyenda", "Ejemplo", "Teclas", "m mapa completo · ? paleta · esc/q cierra",  # modal
    "todo · equipo · personal",                                           # filter labels
]


# Words of the control strings that are ALSO English (never flagged, by design):
# the 8 dropped from the vocabulary, and the English the strings carry
ENGLISH_OK = {"actual", "del", "dice", "nada", "persona", "solo", "tope", "visible",
              "team", "json", "roster", "es", "sync", "esc", "personal", "todo"}


def test_TC_206_the_lexicon_sees_every_base_surface():
    """Guard: EVERY Spanish word of every control string — one per translated
    surface of the base tree — is flagged, not merely one per string (code
    review F1). A lexicon that misses a word of the base copy cannot certify
    its absence on the new tree."""
    assert len(BASE_SPANISH) >= 21 and len(WORDS) >= 200
    blind = {s: sorted(w for w in {w.lower() for w in re.findall(r"[^\W\d_]{3,}", s)}
                       if w not in ENGLISH_OK and not SPANISH.search(w))
             for s in BASE_SPANISH}
    assert not any(blind.values()), blind


def test_TC_206_no_literal_in_the_source_carries_the_old_copy():
    """At the source, not one render: no string literal of the package holds a
    word of the removed vocabulary — so a rarely-painted branch (a failing
    Setup check, an empty flow) cannot keep Spanish. Docstrings and comments
    are prose about the code and are skipped, like the second-person law."""
    import ast
    from pathlib import Path

    from taskboard import views as pkg
    from taskboard.models import CITY_TO_ZONE        # place names are data
    offenders = []
    for path in sorted(Path(pkg.__file__).parent.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        docs = {id(n.body[0].value) for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module))
                and n.body and isinstance(n.body[0], ast.Expr)
                and isinstance(n.body[0].value, ast.Constant)}
        for n in ast.walk(tree):
            if (isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs
                    and n.value not in STORED and n.value not in CITY_TO_ZONE
                    and WORD_ONLY.search(n.value)):
                offenders.append((path.name, n.lineno, n.value[:50]))
    assert not offenders, offenders[:5]


def spanish(text: str) -> list[str]:
    return sorted({m.group(0) for m in SPANISH.finditer(text)})


def test_TC_206_help_copy_is_english_and_fits():
    """TC-206 (LLR-204.1). Every view's help usage and example carry no Spanish,
    keep their section count, and every bullet fits the 44-cell help column
    (the fit law of TC-116 widened to every view, qa P2 Q-11). RED on the base
    tree: Spanish everywhere, 27 bullets wider than 44 cells."""
    sections = {"kanban": 4, "swimlanes": 3, "agenda": 3, "gantt": 3, "focus": 3,
                "chainmap": 3,
                "flow": 3, "standup": 3, "people": 3, "setup": 3}
    assert set(sections) == set(VIEW_ORDER)
    for mode in VIEW_ORDER:
        usage = help_usage(mode)
        assert len(usage) == sections[mode], mode
        for heading, bullets in usage:
            assert not spanish(heading), (mode, heading)
            for b in bullets:
                assert not spanish(b), (mode, b, spanish(b))
                assert cell_len(b) <= 44, (mode, cell_len(b), b)
        line, meaning = help_example(mode)
        assert not spanish(line + " " + meaning), (mode, spanish(line + " " + meaning))


def test_TC_206_the_help_names_only_shipped_keys():
    """The copy names the keys the app binds (D-219): `t` pins (not `p`), and
    the people view's filter is named without a key (none is bound)."""
    focus = " ".join(" ".join(b) for _h, b in help_usage("focus"))
    assert "t pins" in focus and "p pin" not in focus
    people = " ".join(" ".join(b) for _h, b in help_usage("people"))
    assert "all · team · personal" in people and not re.search(r"\bf\b", people)


@pytest.mark.parametrize("mode", ["flow", "setup", "standup", "people"])
def test_TC_206_the_views_paint_english(tmp_path, mode):
    """The flow view (with and without history), Setup with its checks failing
    and passing, standup and people under all three filter values: no Spanish
    in the painted text; the stored filter values still work."""
    b, st, setup = kg_board.census(tmp_path)
    renders = []
    if mode == "flow":
        renders.append(render_view("flow", b, False, "tw3", TODAY, 118, 30, {}))
        renders.append(render_view("flow", kg_board.build(tmp_path / "empty" / "b.json"),
                                   False, None, TODAY, 118, 30, {}))
    elif mode == "setup":
        renders.append(render_view("setup", b, False, None, TODAY, 118, 30, {},
                                   setup_state=setup, team_state=st))
        passing = dict(setup, shared_dir=str(tmp_path / "team"))
        renders.append(render_view("setup", b, False, None, TODAY, 118, 30, {},
                                   setup_state=passing, team_state=st))
    else:
        for value in views.TEAM_FILTER_MODES:
            renders.append(render_view(mode, b, False, "tw3", TODAY, 118, 30, {},
                                       team_state=st, team_filter=value))
    for text in renders:
        plain = text.plain.replace(str(tmp_path), "")
        assert not spanish(plain), (mode, spanish(plain))
    if mode in ("standup", "people"):
        assert "all · team · personal" in renders[0].plain


# =========================================================================== #
# AT-204 — through the running app (US-202)
# =========================================================================== #
class _Today(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def frozen(monkeypatch):
    for mod in (views, app_mod, models):
        monkeypatch.setattr(mod, "date", _Today)


def _labels(screen) -> str:
    return "\n".join(w.render().plain for w in screen.query("Label"))


async def test_AT_204_no_spanish_is_painted(tmp_path, frozen):
    """AT-204 (HLR-204). Team mode on, terminal 118×30: `?` in every view paints
    an English help modal; the flow, standup, people and Setup panels paint no
    Spanish; standup and people stay English under all three filter values
    (cycled through the app's own action — no key is bound to it, D-219). RED
    on the base tree: `Uso`, `para qué es`, `modo equipo`, `todo · equipo`."""
    b, _st, _setup = kg_board.census(tmp_path)
    b.settings["team_shared_dir"] = str(tmp_path / "team")
    b.settings["team_user_id"] = "jav"
    b.save()
    app = TaskboardApp(board_path=str(b.path), team_sync_interval=1e9)
    keys = {v: k for k, v in VIEW_KEYS.items()}
    async with app.run_test(size=(118, 30)) as pilot:
        await pilot.pause()
        for view in VIEW_ORDER:
            await pilot.press(keys[view])
            await pilot.pause()
            board = app.query_one("#board").render().plain.replace(str(tmp_path), "")
            assert not spanish(board), (view, spanish(board))
            await pilot.press("question_mark")
            await pilot.pause()
            text = _labels(app.screen)
            assert "Usage" in text and "Keys" in text, view
            assert not spanish(text), (view, spanish(text))
            await pilot.press("escape")
            await pilot.pause()
        for view in ("standup", "people"):
            await pilot.press(keys[view])
            await pilot.pause()
            for _ in range(3):
                await app.run_action("team_filter_cycle")
                await pilot.pause()
                painted = app.query_one("#board").render().plain
                assert "all · team · personal" in painted
                assert not spanish(painted), (view, app.team_filter, spanish(painted))

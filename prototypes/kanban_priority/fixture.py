"""THROWAWAY prototype fixture — shared by prototypes/kanban_priority and
prototypes/edit_modal. Builds a realistic board (4 projects, 21 tasks, 6 high
priority of which 1 is done) RELATIVE TO A PINNED TODAY, writes it to a temp
JSON (never the user's board), and pins `date.today()` inside the taskboard
modules so every render and every capture agree on the day.
"""
from __future__ import annotations

import json
import tempfile
from datetime import date, timedelta
from pathlib import Path

TODAY = date(2026, 9, 30)

LONG_TASK_ID = "f0e1d2c3"

LONG_NOTES = """Contexto: el cliente quiere migrar el ==portal de proveedores== antes del cierre de Q4; la fase 1 (catálogo) ya está en producción.
Owner: Javier · reviewer: Lucía (backend) · QA: Marco

Decisiones tomadas
- Auth via SSO (Azure AD) — ++aprobado por TI el 24/09++
- Mantener el endpoint legacy /v1/invoices hasta enero
- !!No tocar el esquema de pagos sin sign-off de finanzas!!
- Rate limit: 100 req/min por proveedor, burst de 20

Open questions
- ¿El export CSV necesita columnas en inglés o en español?
- Who owns the S3 bucket after go-live? ==preguntar a Diego==
- Staging data: anonimizar RFC y CLABE antes de compartir con el proveedor externo

Plan de esta semana
1. Terminar el mapping de campos (60% hecho, faltan impuestos y retenciones)
2. Demo interna el jueves 10:00 — ++sala reservada++
3. !!Bloqueante: credenciales de staging vencen el 02/10!!
4. Draft del runbook de rollback (owner: Lucía)

Ref: https://wiki.example.com/portal/migracion-fase-2
Llamada 29/09: el CFO pidió un reporte semanal con avance, riesgos y fechas comprometidas; quiere verlo en el mismo formato que el de fase 1.
Próximo paso: confirmar con Lucía si el webhook de pagos puede quedar detrás del feature flag hasta """

PROJECTS = [
    ("p-portal", "Portal Proveedores", "sky"),
    ("p-mobile", "Mobile app", "lime"),
    ("p-data", "Data pipeline", "violet"),
    ("p-web", "Marketing site", "pink"),     # pink on purpose: K3's rose-vs-pink check
]

# (id, title, project, phase, priority, due offset | None, blocked, days in phase)
TASKS = [
    (LONG_TASK_ID, "Migrar portal de proveedores (fase 2)", "p-portal", "Doing", "high", 2, False, 4),
    ("t02", "SSO integration Azure AD", "p-portal", "Doing", "normal", 5, False, 2),
    ("t03", "Export CSV de facturas", "p-portal", "Backlog", "low", 14, False, 9),
    ("t04", "Anonimizar datos de staging", "p-portal", "Review", "high", 0, False, 1),
    ("t05", "Webhook de pagos", "p-portal", "Backlog", "normal", None, True, 6),
    ("t06", "Login con biometría", "p-mobile", "Doing", "high", -1, False, 7),
    ("t07", "Push notifications v2", "p-mobile", "Backlog", "normal", 10, False, 12),
    ("t08", "Fix crash en Android 12", "p-mobile", "Review", "normal", 1, False, 2),
    ("t09", "Release 3.4 store listing", "p-mobile", "Done", "high", -3, False, 3),
    ("t10", "Offline mode spike", "p-mobile", "Backlog", "low", None, False, 15),
    ("t11", "Ingesta de CSV nocturna", "p-data", "Doing", "normal", 3, False, 5),
    ("t12", "Migrar DAG a Airflow 2", "p-data", "Backlog", "high", 7, False, 3),
    ("t13", "Alertas de calidad de datos", "p-data", "Review", "normal", 4, False, 1),
    ("t14", "Dashboard de costos", "p-data", "Done", "normal", -5, False, 6),
    ("t15", "Backfill histórico 2024", "p-data", "Backlog", "normal", 20, False, 8),
    ("t16", "Landing GRNDIA LATAM", "p-web", "Doing", "normal", 6, False, 3),
    ("t17", "Caso de éxito: portal", "p-web", "Backlog", "high", 9, False, 4),
    ("t18", "SEO técnico", "p-web", "Review", "low", 12, False, 2),
    ("t19", "Newsletter octubre", "p-web", "Done", "normal", -2, False, 2),
    ("t20", "Formulario de contacto", "p-web", "Done", "normal", -8, False, 8),
    ("t21", "Revisar contrato hosting", None, "Backlog", "normal", 15, False, 5),
]

SHORT_NOTES = {
    "t04": "!!RFC y CLABE!! fuera antes de compartir\nscript en /tools/anon.py",
    "t06": "Face ID ok; ==Android pendiente==",
    "t12": "Probar en staging primero; ++DAGs simples ya migrados++",
    "t17": "Entrevista con el cliente agendada",
}


def _iso(off: int | None) -> str | None:
    return None if off is None else (TODAY + timedelta(days=off)).isoformat()


def board_dict() -> dict:
    tasks = []
    for tid, title, pid, phase, prio, due, blocked, age in TASKS:
        t = {
            "id": tid, "title": title, "project_id": pid, "phase": phase,
            "priority": prio, "start_date": _iso(-age - 3) if due is not None else None,
            "due_date": _iso(due), "notes": SHORT_NOTES.get(tid, ""),
            "urls": [], "images": [], "archived": False, "pinned": False,
            "blocked": blocked, "depends_on": [],
            "phase_changed": (TODAY - timedelta(days=age)).isoformat(),
        }
        if tid == LONG_TASK_ID:
            t["notes"] = LONG_NOTES
            t["urls"] = ["https://wiki.example.com/portal/migracion-fase-2",
                         "https://github.com/example/portal/pull/412"]
            t["images"] = [f"images/{LONG_TASK_ID}/pasted-2026-09-29-1012.png"]
        tasks.append(t)
    return {
        "phases": ["Backlog", "Doing", "Review", "Done"],
        "projects": [{"id": pid, "name": name, "color": col, "status": "on_track",
                      "archived": False, "start_date": None, "due_date": None}
                     for pid, name, col in PROJECTS],
        "tasks": tasks,
        # the one-time "keys moved" toast would cover the capture
        "settings": {"seen_view_renumber_2026_07": True},
    }


def write_board() -> Path:
    """A throwaway copy in a temp dir: the app may save to it, nothing else."""
    d = Path(tempfile.mkdtemp(prefix="tb_proto_"))
    p = d / "board.json"
    p.write_text(json.dumps(board_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return p


class _PinnedDate(date):
    @classmethod
    def today(cls):            # noqa: D401 - the whole point of the class
        return TODAY


def pin_today() -> None:
    """Every `date.today()` the app's render path reads goes through these
    three module globals; swapping them pins the captures to TODAY."""
    import taskboard.app as app_mod
    import taskboard.models as models_mod
    import taskboard.views as views_mod
    for mod in (app_mod, models_mod, views_mod):
        if getattr(mod, "date", None) is date:
            mod.date = _PinnedDate

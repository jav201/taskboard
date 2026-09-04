"""fixture.py -- ONE body of mock content, shared by all five languages.

The rule this file exists to keep is `capture_languages.py`'s: "the same
screen in five languages" is only an honest comparison when it really is the
same screen.  Every string, every count and every state below is read by all
five kits; a language that reads a DIFFERENT number here would be being
flattered rather than tested.

Nothing here is a render.  There is not one glyph of design in this file --
it is content, and the six screen builders in `screens.py` are the only place
that decides what a language DOES with it.  That split is the same one
`language.py` keeps between a caller's content and a kit's notation (L-33).
"""
from __future__ import annotations

# -- S1: the board -----------------------------------------------------------
#: (title, project, phase, due-in-days or None, priority, status)
TASKS = [
    ("Fix login redirect",      "Web",  "doing",   3,  "high",   "open"),
    ("Rate-limit the API",      "API",  "doing",  -2,  "high",   "blocked"),
    ("Port the CSV importer",   "API",  "doing",   9,  "normal", "open"),
    ("Rewrite the onboarding",  "Web",  "doing",  14,  "low",    "open"),
    ("Audit the theme tokens",  "Docs", "backlog", 21, "low",    "open"),
    ("Drop the legacy shim",    "API",  "backlog", 30, "normal", "open"),
]

#: the columns the board shows, in order: (name, count).  BLOCKED is EMPTY on
#: purpose -- S1 owes an empty-column state and a column that is merely short
#: does not exercise it.
COLUMNS = [("BACKLOG", 5), ("DOING", 4), ("BLOCKED", 0), ("DONE", 7)]

SELECTED = 0                      # index into TASKS -- the card with the cursor
FOCUS_COL = 1                     # DOING holds the focus ring

#: the detail pane's fields for TASKS[SELECTED], as (caption, value) rows.
DETAIL = [
    ("project",  "Web"),
    ("phase",    "doing"),
    ("due",      "3d"),
    ("priority", "high"),
    ("status",   "open"),
    ("owner",    "jav201"),
]

#: the list's viewport, for the scroll indication: (start, size, total)
SCROLL = (2, 8, 23)

# -- S2: the form ------------------------------------------------------------
FORM_TITLE = "Fix login redirect"
FORM_TITLE_CARET = 9              # the caret sits after "Fix login"
FORM_DUE_RAW = "12/09/26"         # what the user typed
FORM_DUE_ERROR = "expected YYYY-MM-DD"
PRIORITIES = ["low", "norm", "high"]
PRIORITY_SEL = 2
TAGS = [("api", False), ("ui", True), ("urgent", True)]
NOTES = ["Redirect drops the ?next= param when the", "session cookie is renewed mid-flight."]
#: Save is DISABLED because `due` is invalid.  Cancel is the secondary action.
SAVE_ENABLED = False

# -- S3: settings ------------------------------------------------------------
#: (label, on, disabled)
SWITCHES = [
    ("notify on overdue",   True,  False),
    ("daily digest",        True,  False),
    ("sound",               False, False),
    ("sync to remote",      False, True),    # the disabled one
    ("compact rows",        True,  False),
]
#: (label, options, selected, open)
SELECTS = [
    ("start of week", ["sun", "mon"], 1, False),
    ("theme",         ["auto", "light", "dark"], 2, True),   # the OPEN one
]
SLIDER_LABEL = "row density"
SLIDER_VAL = 70                   # the 70 % the spec asks for
DANGER_LABEL = "delete every completed task"
DANGER_ACTION = "Delete all"

# -- S4: the modal -----------------------------------------------------------
MODAL_TITLE = "Delete 3 tasks?"
MODAL_BODY = ["3 tasks will be removed from BACKLOG.",
              "This cannot be undone."]
MODAL_BUTTONS = [("Delete", True), ("Cancel", False)]     # (label, is_default)
MODAL_COUNT = 3

# -- S5: the live monitor ----------------------------------------------------
#: (timestamp, level, message)
LOG = [
    ("09:41:02", "info",  "board loaded  16 tasks  4 projects"),
    ("09:41:07", "info",  "sync started  remote=origin"),
    ("09:41:09", "warn",  "3 tasks overdue in BACKLOG"),
    ("09:41:12", "info",  "sync ok  216 ms  0 conflicts"),
    ("09:41:18", "error", "rate limit hit  retry in 30 s"),
    ("09:41:20", "info",  "retry scheduled  attempt 2 of 5"),
    ("09:41:33", "info",  "sync ok  198 ms  0 conflicts"),
    ("09:41:41", "info",  "signal engine idle"),
]
#: the sparkline's series and the ceiling every language must share.
RATE_SERIES = [2, 5, 3, 8, 4, 6, 9, 7, 4, 2, 5, 8, 6, 3, 7, 5]
RATE_CEILING = 10
RATE_VALUE = 5                    # events/s right now
RATE_LABEL = "events/s"
PAUSED = True                     # the tail is HELD -- S5 owes a paused state

# -- S6: the command palette -------------------------------------------------
QUERY = "re"                      # the 2-char query the spec asks for
#: (label, the [start, end) span of the match, the key hint)
RESULTS = [
    ("redirect to task",     (0, 2),  "enter"),
    ("rename project",       (0, 2),  ""),
    ("refresh board",        (0, 2),  "r"),
    ("archive released",     (12, 14), ""),
    ("restore from backup",  (0, 2),  ""),
    ("set reminder",         (6, 8),  ""),
]
RESULT_SEL = 0
QUERY_EMPTY = "zzq"               # the no-match query
HINTS = [("enter", "run"), ("esc", "close"), ("^p", "prev"), ("^n", "next")]

# -- shared chrome -----------------------------------------------------------
MODES = ["board", "form", "cfg", "log"]
APP = "TASKBOARD"
REV = "2026-09-04"
WORK = (7, 16)                    # done / total, for any meter a screen shows
COUNTS = [5, 4, 7]                # per-column load, for any meter's sub-row

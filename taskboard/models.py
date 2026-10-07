"""Data model + JSON persistence for the taskboard widget.

Two entities (Project, Task) and a Board that owns them and reads/writes a
single JSON file. Tasks may be standalone (project_id is None) -> shown in the
"Inbox" group. A missing file is seeded with demo data; a corrupt file starts
empty (we never overwrite it, so the user can recover it by hand).
"""

from __future__ import annotations

import errno
import json
import os
import shutil
import stat
import tempfile
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

from . import history

# --- enumerations (kept as plain strings; validated leniently at the edges) ---
# THE COLOUR RATION. A project hue NAMES (which project); the app's reserved hues
# JUDGE (over #f43f5e = overdue, soon #fbbf24 = due today) or CALL ATTENTION
# (accent #2dd4bf = today/focus). No mark may wear both jobs, so an identity hue
# that is confusable with a reserved one is not offered. Four were dropped on
# measured euclidean rgb distance (nearest reserved hue in brackets):
#   amber  #fbbf24 -> soon      0.0   IDENTICAL to "due today"
#   cyan   #22d3ee -> accent   48.3   reads as the today rule
#   orange #fb923c -> soon     51.0
#   rose   #fb7185 -> over     63.8
# Bands: >=70 from a judging hue (over/soon), >=55 from accent. The closest
# survivors are lime 97.7 (soon), pink 101.7 (over) and sky 62.4 (accent).
# The oracle is in tests/test_palette_ration.py — it measures, it does not
# consult this list, so re-adding a hue near a reserved one turns it red.
PROJECT_COLORS = ("lime", "green", "sky", "blue",
                  "indigo", "violet", "fuchsia", "pink")

# Boards saved before the ration keep loading: a dropped hue is remapped to a
# surviving one. The assignment is the injective map with the smallest total rgb
# distance (unique optimum over all 1680 injective maps; runner-up +3.04).
# INJECTIVE ON PURPOSE: plain nearest-hue would send amber AND orange to lime,
# making two previously-distinct projects indistinguishable — which breaks the
# very job the identity hue has. Distances in brackets.
DROPPED_PROJECT_COLORS = {
    "cyan": "sky",        # 32.7
    "rose": "pink",       # 49.5
    "amber": "lime",      # 97.7
    "orange": "fuchsia",  # 191.6
}
PROJECT_STATUSES = ("on_track", "paused", "cancelled", "completed")
TASK_PRIORITIES = ("low", "normal", "high")


def next_priority(p: str) -> str:
    """One step through TASK_PRIORITIES, wrapping at the end. An unknown value
    counts as the default (`normal`) — coerced at load, but a caller holding a
    pre-coercion string still gets a member of the declared order back."""
    if p not in TASK_PRIORITIES:
        return "normal"
    return TASK_PRIORITIES[(TASK_PRIORITIES.index(p) + 1) % len(TASK_PRIORITIES)]

# Finished work stops being news. A task that has been in its done phase this
# long is archived automatically — but ONLY when the board knows when it was
# finished (see Board.auto_archive_done).
AUTO_ARCHIVE_DAYS = 20

# Tasks move through an ORDERED list of phases owned by the board; progress is
# positional (phase index / last index), so a board can define its own workflow.
DEFAULT_PHASES = ("Backlog", "Doing", "Done")

# The operator-approved WIP-limit policy (HLR-005, §6.5 AMD-08): when a board's
# settings carry no `wip_limits` entry for a phase, the limit reads from THIS
# map — the default is never written into settings by a READ, so a board file
# is never rewritten just by being looked at.
DEFAULT_WIP_LIMITS = {"Doing": 3}
# legacy task.status -> (phase, blocked) ; kept forever so old boards keep loading
LEGACY_STATUS = {"backlog": ("Backlog", False), "doing": ("Doing", False),
                 "active": ("Doing", False), "blocked": ("Doing", True),
                 "done": ("Done", False)}

# --- ribbon clocks: CITY -> IANA timezone (real, DST-aware via zoneinfo) ------
# Curated across the regions the user works in. Display name is the city; the
# value stored in board.json is the city name (unique -> recovers its zone).
CITY_ZONES: tuple[tuple[str, str], ...] = (
    # --- LATAM -----------------------------------------------------
    ("Mexico City", "America/Mexico_City"),
    ("Monterrey", "America/Monterrey"),
    ("Guadalajara", "America/Mexico_City"),
    ("Tijuana", "America/Tijuana"),
    ("Cancún", "America/Cancun"),
    ("Chihuahua", "America/Chihuahua"),
    ("Mérida", "America/Merida"),
    ("Hermosillo", "America/Hermosillo"),
    ("Guatemala City", "America/Guatemala"),
    ("San Salvador", "America/El_Salvador"),
    ("Tegucigalpa", "America/Tegucigalpa"),
    ("Managua", "America/Managua"),
    ("San José", "America/Costa_Rica"),
    ("Panama", "America/Panama"),
    ("Havana", "America/Havana"),
    ("Santo Domingo", "America/Santo_Domingo"),
    ("San Juan", "America/Puerto_Rico"),
    ("Kingston", "America/Jamaica"),
    ("Port-au-Prince", "America/Port-au-Prince"),
    ("Nassau", "America/Nassau"),
    ("Bogotá", "America/Bogota"),
    ("Medellín", "America/Bogota"),
    ("Quito", "America/Guayaquil"),
    ("Guayaquil", "America/Guayaquil"),
    ("Lima", "America/Lima"),
    ("La Paz", "America/La_Paz"),
    ("Caracas", "America/Caracas"),
    ("Asunción", "America/Asuncion"),
    ("Santiago", "America/Santiago"),
    ("Buenos Aires", "America/Argentina/Buenos_Aires"),
    ("Córdoba", "America/Argentina/Cordoba"),
    ("Mendoza", "America/Argentina/Mendoza"),
    ("Montevideo", "America/Montevideo"),
    ("São Paulo", "America/Sao_Paulo"),
    ("Rio de Janeiro", "America/Sao_Paulo"),
    ("Brasília", "America/Sao_Paulo"),
    ("Manaus", "America/Manaus"),
    ("Recife", "America/Recife"),
    ("Fortaleza", "America/Fortaleza"),
    ("Belém", "America/Belem"),
    ("Porto Alegre", "America/Sao_Paulo"),
    ("Salvador", "America/Bahia"),
    ("Curitiba", "America/Sao_Paulo"),
    ("Fernando de Noronha", "America/Noronha"),
    ("Galápagos", "Pacific/Galapagos"),
    ("Easter Island", "Pacific/Easter"),
    ("Punta Arenas", "America/Punta_Arenas"),
    ("Ushuaia", "America/Argentina/Ushuaia"),
    ("Paramaribo", "America/Paramaribo"),
    ("Georgetown", "America/Guyana"),
    ("Cayenne", "America/Cayenne"),
    ("Belize City", "America/Belize"),
    ("Willemstad", "America/Curacao"),
    ("Bridgetown", "America/Barbados"),
    ("Port of Spain", "America/Port_of_Spain"),
    # --- US / Canada -----------------------------------------------
    ("New York", "America/New_York"),
    ("Boston", "America/New_York"),
    ("Miami", "America/New_York"),
    ("Atlanta", "America/New_York"),
    ("Washington DC", "America/New_York"),
    ("Philadelphia", "America/New_York"),
    ("Detroit", "America/Detroit"),
    ("Pittsburgh", "America/New_York"),
    ("Charlotte", "America/New_York"),
    ("Orlando", "America/New_York"),
    ("Toronto", "America/Toronto"),
    ("Montreal", "America/Toronto"),
    ("Ottawa", "America/Toronto"),
    ("Quebec City", "America/Toronto"),
    ("Halifax", "America/Halifax"),
    ("St. John's", "America/St_Johns"),
    ("Chicago", "America/Chicago"),
    ("Houston", "America/Chicago"),
    ("Dallas", "America/Chicago"),
    ("Austin", "America/Chicago"),
    ("San Antonio", "America/Chicago"),
    ("Minneapolis", "America/Chicago"),
    ("Kansas City", "America/Chicago"),
    ("New Orleans", "America/Chicago"),
    ("Nashville", "America/Chicago"),
    ("Winnipeg", "America/Winnipeg"),
    ("Denver", "America/Denver"),
    ("Salt Lake City", "America/Denver"),
    ("Albuquerque", "America/Denver"),
    ("Calgary", "America/Edmonton"),
    ("Edmonton", "America/Edmonton"),
    ("Phoenix", "America/Phoenix"),
    ("Las Vegas", "America/Los_Angeles"),
    ("Los Angeles", "America/Los_Angeles"),
    ("San Diego", "America/Los_Angeles"),
    ("San Francisco", "America/Los_Angeles"),
    ("San Jose (CA)", "America/Los_Angeles"),
    ("Portland", "America/Los_Angeles"),
    ("Seattle", "America/Los_Angeles"),
    ("Vancouver", "America/Vancouver"),
    ("Anchorage", "America/Anchorage"),
    ("Juneau", "America/Juneau"),
    ("Honolulu", "Pacific/Honolulu"),
    ("Adak", "America/Adak"),
    ("Indianapolis", "America/Indiana/Indianapolis"),
    ("Louisville", "America/Kentucky/Louisville"),
    ("Whitehorse", "America/Whitehorse"),
    ("Yellowknife", "America/Edmonton"),
    ("Iqaluit", "America/Iqaluit"),
    ("Regina", "America/Regina"),
    ("Nuuk", "America/Nuuk"),
    ("Hamilton", "Atlantic/Bermuda"),
    # --- Europe ----------------------------------------------------
    ("London", "Europe/London"),
    ("Manchester", "Europe/London"),
    ("Edinburgh", "Europe/London"),
    ("Dublin", "Europe/Dublin"),
    ("Lisbon", "Europe/Lisbon"),
    ("Porto", "Europe/Lisbon"),
    ("Madrid", "Europe/Madrid"),
    ("Barcelona", "Europe/Madrid"),
    ("Valencia", "Europe/Madrid"),
    ("Seville", "Europe/Madrid"),
    ("Bilbao", "Europe/Madrid"),
    ("Las Palmas", "Atlantic/Canary"),
    ("Paris", "Europe/Paris"),
    ("Lyon", "Europe/Paris"),
    ("Marseille", "Europe/Paris"),
    ("Brussels", "Europe/Brussels"),
    ("Amsterdam", "Europe/Amsterdam"),
    ("Rotterdam", "Europe/Amsterdam"),
    ("Luxembourg", "Europe/Luxembourg"),
    ("Berlin", "Europe/Berlin"),
    ("Munich", "Europe/Berlin"),
    ("Frankfurt", "Europe/Berlin"),
    ("Hamburg", "Europe/Berlin"),
    ("Cologne", "Europe/Berlin"),
    ("Stuttgart", "Europe/Berlin"),
    ("Düsseldorf", "Europe/Berlin"),
    ("Zurich", "Europe/Zurich"),
    ("Geneva", "Europe/Zurich"),
    ("Bern", "Europe/Zurich"),
    ("Vienna", "Europe/Vienna"),
    ("Rome", "Europe/Rome"),
    ("Milan", "Europe/Rome"),
    ("Naples", "Europe/Rome"),
    ("Turin", "Europe/Rome"),
    ("Venice", "Europe/Rome"),
    ("Florence", "Europe/Rome"),
    ("Prague", "Europe/Prague"),
    ("Bratislava", "Europe/Bratislava"),
    ("Budapest", "Europe/Budapest"),
    ("Warsaw", "Europe/Warsaw"),
    ("Kraków", "Europe/Warsaw"),
    ("Copenhagen", "Europe/Copenhagen"),
    ("Oslo", "Europe/Oslo"),
    ("Stockholm", "Europe/Stockholm"),
    ("Gothenburg", "Europe/Stockholm"),
    ("Helsinki", "Europe/Helsinki"),
    ("Tallinn", "Europe/Tallinn"),
    ("Riga", "Europe/Riga"),
    ("Vilnius", "Europe/Vilnius"),
    ("Reykjavík", "Atlantic/Reykjavik"),
    ("Athens", "Europe/Athens"),
    ("Thessaloniki", "Europe/Athens"),
    ("Sofia", "Europe/Sofia"),
    ("Bucharest", "Europe/Bucharest"),
    ("Belgrade", "Europe/Belgrade"),
    ("Zagreb", "Europe/Zagreb"),
    ("Ljubljana", "Europe/Ljubljana"),
    ("Sarajevo", "Europe/Sarajevo"),
    ("Skopje", "Europe/Skopje"),
    ("Tirana", "Europe/Tirane"),
    ("Chișinău", "Europe/Chisinau"),
    ("Kyiv", "Europe/Kiev"),
    ("Minsk", "Europe/Minsk"),
    ("Moscow", "Europe/Moscow"),
    ("Saint Petersburg", "Europe/Moscow"),
    ("Kaliningrad", "Europe/Kaliningrad"),
    ("Samara", "Europe/Samara"),
    ("Yekaterinburg", "Asia/Yekaterinburg"),
    ("Novosibirsk", "Asia/Novosibirsk"),
    ("Krasnoyarsk", "Asia/Krasnoyarsk"),
    ("Irkutsk", "Asia/Irkutsk"),
    ("Yakutsk", "Asia/Yakutsk"),
    ("Vladivostok", "Asia/Vladivostok"),
    ("Magadan", "Asia/Magadan"),
    ("Kamchatka", "Asia/Kamchatka"),
    ("Anadyr", "Asia/Anadyr"),
    ("Malta", "Europe/Malta"),
    ("Monaco", "Europe/Monaco"),
    ("Andorra", "Europe/Andorra"),
    ("Gibraltar", "Europe/Gibraltar"),
    ("Nicosia", "Asia/Nicosia"),
    ("Azores", "Atlantic/Azores"),
    ("Faroe Islands", "Atlantic/Faroe"),
    ("Torshavn", "Atlantic/Faroe"),
    # --- Middle East -----------------------------------------------
    ("Istanbul", "Europe/Istanbul"),
    ("Ankara", "Europe/Istanbul"),
    ("Tel Aviv", "Asia/Jerusalem"),
    ("Jerusalem", "Asia/Jerusalem"),
    ("Beirut", "Asia/Beirut"),
    ("Damascus", "Asia/Damascus"),
    ("Amman", "Asia/Amman"),
    ("Baghdad", "Asia/Baghdad"),
    ("Kuwait City", "Asia/Kuwait"),
    ("Riyadh", "Asia/Riyadh"),
    ("Jeddah", "Asia/Riyadh"),
    ("Doha", "Asia/Qatar"),
    ("Manama", "Asia/Bahrain"),
    ("Dubai", "Asia/Dubai"),
    ("Abu Dhabi", "Asia/Dubai"),
    ("Muscat", "Asia/Muscat"),
    ("Tehran", "Asia/Tehran"),
    ("Yerevan", "Asia/Yerevan"),
    ("Tbilisi", "Asia/Tbilisi"),
    ("Baku", "Asia/Baku"),
    # --- Africa ----------------------------------------------------
    ("Cairo", "Africa/Cairo"),
    ("Alexandria", "Africa/Cairo"),
    ("Casablanca", "Africa/Casablanca"),
    ("Rabat", "Africa/Casablanca"),
    ("Marrakesh", "Africa/Casablanca"),
    ("Algiers", "Africa/Algiers"),
    ("Tunis", "Africa/Tunis"),
    ("Tripoli", "Africa/Tripoli"),
    ("Khartoum", "Africa/Khartoum"),
    ("Addis Ababa", "Africa/Addis_Ababa"),
    ("Nairobi", "Africa/Nairobi"),
    ("Kampala", "Africa/Kampala"),
    ("Dar es Salaam", "Africa/Dar_es_Salaam"),
    ("Kigali", "Africa/Kigali"),
    ("Lagos", "Africa/Lagos"),
    ("Abuja", "Africa/Lagos"),
    ("Accra", "Africa/Accra"),
    ("Abidjan", "Africa/Abidjan"),
    ("Dakar", "Africa/Dakar"),
    ("Bamako", "Africa/Bamako"),
    ("Douala", "Africa/Douala"),
    ("Kinshasa", "Africa/Kinshasa"),
    ("Luanda", "Africa/Luanda"),
    ("Lusaka", "Africa/Lusaka"),
    ("Harare", "Africa/Harare"),
    ("Maputo", "Africa/Maputo"),
    ("Windhoek", "Africa/Windhoek"),
    ("Gaborone", "Africa/Gaborone"),
    ("Johannesburg", "Africa/Johannesburg"),
    ("Cape Town", "Africa/Johannesburg"),
    ("Durban", "Africa/Johannesburg"),
    ("Antananarivo", "Indian/Antananarivo"),
    ("Port Louis", "Indian/Mauritius"),
    ("Victoria", "Indian/Mahe"),
    ("Praia", "Atlantic/Cape_Verde"),
    ("Mogadishu", "Africa/Mogadishu"),
    # --- South / Central Asia --------------------------------------
    ("Karachi", "Asia/Karachi"),
    ("Lahore", "Asia/Karachi"),
    ("Islamabad", "Asia/Karachi"),
    ("Kabul", "Asia/Kabul"),
    ("Mumbai", "Asia/Kolkata"),
    ("Delhi", "Asia/Kolkata"),
    ("Bengaluru", "Asia/Kolkata"),
    ("Hyderabad", "Asia/Kolkata"),
    ("Chennai", "Asia/Kolkata"),
    ("Kolkata", "Asia/Kolkata"),
    ("Pune", "Asia/Kolkata"),
    ("Ahmedabad", "Asia/Kolkata"),
    ("Colombo", "Asia/Colombo"),
    ("Kathmandu", "Asia/Kathmandu"),
    ("Dhaka", "Asia/Dhaka"),
    ("Thimphu", "Asia/Thimphu"),
    ("Malé", "Indian/Maldives"),
    ("Tashkent", "Asia/Tashkent"),
    ("Almaty", "Asia/Almaty"),
    ("Astana", "Asia/Almaty"),
    ("Bishkek", "Asia/Bishkek"),
    ("Dushanbe", "Asia/Dushanbe"),
    ("Ashgabat", "Asia/Ashgabat"),
    # --- East / Southeast Asia -------------------------------------
    ("Bangkok", "Asia/Bangkok"),
    ("Hanoi", "Asia/Ho_Chi_Minh"),
    ("Ho Chi Minh City", "Asia/Ho_Chi_Minh"),
    ("Phnom Penh", "Asia/Phnom_Penh"),
    ("Vientiane", "Asia/Vientiane"),
    ("Yangon", "Asia/Yangon"),
    ("Jakarta", "Asia/Jakarta"),
    ("Bali", "Asia/Makassar"),
    ("Makassar", "Asia/Makassar"),
    ("Jayapura", "Asia/Jayapura"),
    ("Kuala Lumpur", "Asia/Kuala_Lumpur"),
    ("Singapore", "Asia/Singapore"),
    ("Bandar Seri Begawan", "Asia/Brunei"),
    ("Manila", "Asia/Manila"),
    ("Hong Kong", "Asia/Hong_Kong"),
    ("Macau", "Asia/Macau"),
    ("Shanghai", "Asia/Shanghai"),
    ("Beijing", "Asia/Shanghai"),
    ("Shenzhen", "Asia/Shanghai"),
    ("Guangzhou", "Asia/Shanghai"),
    ("Chengdu", "Asia/Shanghai"),
    ("Ürümqi", "Asia/Urumqi"),
    ("Taipei", "Asia/Taipei"),
    ("Seoul", "Asia/Seoul"),
    ("Busan", "Asia/Seoul"),
    ("Pyongyang", "Asia/Pyongyang"),
    ("Tokyo", "Asia/Tokyo"),
    ("Osaka", "Asia/Tokyo"),
    ("Kyoto", "Asia/Tokyo"),
    ("Sapporo", "Asia/Tokyo"),
    ("Ulaanbaatar", "Asia/Ulaanbaatar"),
    ("Dili", "Asia/Dili"),
    # --- Oceania ---------------------------------------------------
    ("Perth", "Australia/Perth"),
    ("Eucla", "Australia/Eucla"),
    ("Darwin", "Australia/Darwin"),
    ("Adelaide", "Australia/Adelaide"),
    ("Brisbane", "Australia/Brisbane"),
    ("Sydney", "Australia/Sydney"),
    ("Melbourne", "Australia/Melbourne"),
    ("Canberra", "Australia/Sydney"),
    ("Hobart", "Australia/Hobart"),
    ("Lord Howe Island", "Australia/Lord_Howe"),
    ("Auckland", "Pacific/Auckland"),
    ("Wellington", "Pacific/Auckland"),
    ("Christchurch", "Pacific/Auckland"),
    ("Chatham Islands", "Pacific/Chatham"),
    ("Suva", "Pacific/Fiji"),
    ("Port Moresby", "Pacific/Port_Moresby"),
    ("Nouméa", "Pacific/Noumea"),
    ("Honiara", "Pacific/Guadalcanal"),
    ("Port Vila", "Pacific/Efate"),
    ("Apia", "Pacific/Apia"),
    ("Nukuʻalofa", "Pacific/Tongatapu"),
    ("Papeete", "Pacific/Tahiti"),
    ("Marquesas Islands", "Pacific/Marquesas"),
    ("Guam", "Pacific/Guam"),
    ("Pago Pago", "Pacific/Pago_Pago"),
    ("Midway", "Pacific/Midway"),
    ("Kiritimati", "Pacific/Kiritimati"),
    ("Tarawa", "Pacific/Tarawa"),
    ("Majuro", "Pacific/Majuro"),
    ("Palau", "Pacific/Palau"),
    ("Norfolk Island", "Pacific/Norfolk"),
    ("Rarotonga", "Pacific/Rarotonga"),
    ("Niue", "Pacific/Niue"),
    ("Baker Island", "Etc/GMT+12"),
    ("Fakaofo", "Pacific/Fakaofo"),
    # --- polar / research ------------------------------------------
    ("McMurdo Station", "Antarctica/McMurdo"),
    ("Casey Station", "Antarctica/Casey"),
    ("Longyearbyen", "Arctic/Longyearbyen"),
)
CITY_TO_ZONE: dict[str, str] = dict(CITY_ZONES)
_CITY_LOWER: dict[str, str] = {name.lower(): name for name, _ in CITY_ZONES}


def _fold(text: str) -> str:
    """Lowercase and strip accents, so a plain-ASCII keyboard finds the city.

    Typing "Sao Paulo" must find "São Paulo" and "Bogota" must find "Bogotá" —
    the accent is how the city is SPELLED, not how it is searched for."""
    return "".join(ch for ch in unicodedata.normalize("NFKD", text.strip().lower())
                   if not unicodedata.combining(ch))


# The folded index only ever RESOLVES an ambiguity that does not exist: a law in
# tests/test_cities.py asserts no two display names fold to the same key, so the
# accent-blind lookup can never silently pick the wrong city.
_CITY_FOLDED: dict[str, str] = {_fold(name): name for name, _ in CITY_ZONES}

DEFAULT_CLOCK1 = "Mexico City"
DEFAULT_CLOCK2 = "New York"

# migrate old fixed-offset abbreviations (pre-city boards) to a representative city
_LEGACY_ABBREV_TO_CITY = {
    "UTC": "London", "GMT": "London", "HST": "Honolulu", "AKST": "Anchorage",
    "PST": "Los Angeles", "MST": "Denver", "CST": "Mexico City", "EST": "New York",
    "AST": "Santiago", "BRT": "São Paulo", "CET": "Madrid", "EET": "Athens",
    "MSK": "Moscow", "GST": "Dubai", "IST": "Mumbai", "ICT": "Bangkok",
    "HKT": "Hong Kong", "JST": "Tokyo", "AEST": "Sydney", "NZST": "Auckland",
}


def city_names() -> list[str]:
    """All selectable city display names (for the searchable picker)."""
    return [name for name, _ in CITY_ZONES]


def resolve_city(text: str | None) -> str | None:
    """Match typed text to a canonical city name, else None.

    Case-insensitive first — that is the behaviour boards were saved with, and
    it stays exact. Only when nothing matches does the ACCENT-BLIND index get a
    turn, so "Sao Paulo" resolves without changing what "São Paulo" already did."""
    if not text:
        return None
    return (_CITY_LOWER.get(text.strip().lower())
            or _CITY_FOLDED.get(_fold(text)))


def default_board_path() -> Path:
    """User-data location for the JSON store.

    The package dir is read-only once pip/pipx-installed, so the board lives
    under the user's home instead: ~/.taskboard/board.json
    """
    return Path.home() / ".taskboard" / "board.json"


# Local image paths are opened with their OS-associated handler, so a non-image
# file would EXECUTE — .svg is excluded because it is scriptable. Canonical home
# for the allowlist (app.py and modals.py both import it).
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}


def grab_clipboard_image():
    """Return a PIL.Image from the clipboard, a list of file-path strings when
    files were copied instead, or None when the clipboard holds neither / Pillow
    is unavailable. Never raises."""
    try:
        from PIL import ImageGrab
        from PIL import Image as _PILImage
    except Exception:
        return None
    try:
        data = ImageGrab.grabclipboard()
    except Exception:
        return None
    if isinstance(data, _PILImage.Image):
        return data
    if isinstance(data, list):
        return [str(p) for p in data]
    return None


_MAX_PASTE_CHARS = 100_000


def strip_controls(value):
    """The one control-byte rule (S2, L1): a str loses every C0 byte but tab and
    newline, DEL and every C1 byte — all of which some terminals read as control
    introducers, so a title or a note carrying one could drive the terminal. CR
    is one of them, so a CR-LF pair keeps its newline and a lone CR is removed.
    Every other character is kept (accents, emoji, NBSP); any other value is
    returned unchanged."""
    if not isinstance(value, str):
        return value
    return "".join(c for c in value
                   if c in "\t\n" or 0x20 <= ord(c) < 0x7f or ord(c) >= 0xa0)


def clean_strings(value):
    """`strip_controls` over every string inside nested dicts and lists, keys
    included (two keys equal once cleaned keep the later value) — applied where
    text enters the app: the board file and the shared team directory."""
    if isinstance(value, dict):
        return {strip_controls(k): clean_strings(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_strings(v) for v in value]
    return strip_controls(value)


def _clean_clipboard_text(text: str | None) -> str | None:
    """Make clipboard text safe to insert into a field: the one control-byte rule
    (`strip_controls`), then a length cap so a huge/binary clipboard can't freeze
    rendering. None if nothing usable remains."""
    if not text:
        return None
    return strip_controls(text)[:_MAX_PASTE_CHARS] or None


def _win_clipboard_text() -> str | None:
    """Windows clipboard TEXT via the Win32 API (ctypes). None on empty/error.

    ctypes return/arg types are set EXPLICITLY: on 64-bit Windows the HANDLE and
    pointer values are 64-bit, and ctypes' default ``c_int`` return TRUNCATES
    them to 32 bits -> a bogus handle -> GlobalLock hands back a pointer into
    arbitrary memory, which a scan-to-NUL read then dumps as a huge garbage
    string (froze the UI + corrupted the terminal). The read is bounded by
    GlobalSize so it can never run past the real buffer."""
    import ctypes
    from ctypes import wintypes
    CF_UNICODETEXT = 13
    try:
        u, k = ctypes.windll.user32, ctypes.windll.kernel32
        u.OpenClipboard.argtypes = [wintypes.HWND]
        u.OpenClipboard.restype = wintypes.BOOL
        u.GetClipboardData.argtypes = [wintypes.UINT]
        u.GetClipboardData.restype = wintypes.HANDLE          # 64-bit (was c_int)
        u.CloseClipboard.restype = wintypes.BOOL
        k.GlobalLock.argtypes = [wintypes.HGLOBAL]
        k.GlobalLock.restype = wintypes.LPVOID
        k.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
        k.GlobalSize.argtypes = [wintypes.HGLOBAL]
        k.GlobalSize.restype = ctypes.c_size_t
        if not u.OpenClipboard(None):
            return None
        try:
            handle = u.GetClipboardData(CF_UNICODETEXT)
            if not handle:
                return None
            ptr = k.GlobalLock(handle)
            if not ptr:
                return None
            try:
                size = k.GlobalSize(handle)                   # bytes of the buffer
                if not size:
                    return None
                raw = ctypes.string_at(ptr, size)            # bounded read
            finally:
                k.GlobalUnlock(handle)
            # CF_UNICODETEXT is NUL-terminated UTF-16LE; stop at the terminator.
            return raw.decode("utf-16-le", "replace").split("\x00", 1)[0] or None
        finally:
            u.CloseClipboard()
    except Exception:
        return None


def grab_clipboard_text() -> str | None:
    """Return the OS clipboard's TEXT as a str, or None when it holds no text or
    on any error. Windows reads the Win32 clipboard directly (ctypes); macOS uses
    ``pbpaste``; Linux uses ``xclip``/``xsel``. Fixed argv (never a shell), so
    clipboard contents can't inject a command. The result is control-stripped and
    length-capped (``_clean_clipboard_text``). Never raises."""
    import sys
    try:
        if sys.platform == "win32":
            return _clean_clipboard_text(_win_clipboard_text())
        import subprocess
        for argv in (["pbpaste"],
                     ["xclip", "-selection", "clipboard", "-o"],
                     ["xsel", "-b", "-o"]):
            try:
                res = subprocess.run(argv, capture_output=True, timeout=2)
            except (OSError, subprocess.SubprocessError):
                continue
            if res.returncode == 0:
                return _clean_clipboard_text(res.stdout.decode("utf-8", "replace"))
        return None
    except Exception:
        return None


def save_pil_image(directory: Path, image) -> Path:
    """Save a PIL image as the next free ``paste-NNN.png`` in ``directory``
    (created if missing) and return its resolved absolute path."""
    directory.mkdir(parents=True, exist_ok=True)
    n = 1
    while (directory / f"paste-{n:03d}.png").exists():
        n += 1
    dest = directory / f"paste-{n:03d}.png"
    to_save = image if image.mode in ("RGB", "RGBA", "L") else image.convert("RGB")
    to_save.save(dest, "PNG")
    return dest.resolve()


def _new_id() -> str:
    return uuid4().hex[:8]


def parse_iso(value: str | None) -> date | None:
    """Lenient ISO date parse. Blank / bad input -> None (never raises)."""
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None


def date_base(stored: str | None, today: date) -> date:
    """The one "undated means today" base (ARCH4-4/SEC4-6): a readable stored
    date is itself; an undated or unreadable one is `today` — never an invented
    epoch. `bump_due` and `plan_move` both build on this rule."""
    return parse_iso(stored) or today


def bump_due(task: "Task", delta: int, today: date) -> None:
    """Move `task.due_date` `delta` days and write it back as ISO text.

    The base is the task's OWN date, or `today` when there is no readable
    one: an undated task and a corrupt stored string both parse to None
    (`parse_iso` leniency), and None means the bump starts from today —
    never from an invented epoch. Pure bar the one field write; the caller
    saves (the `set_task_phase` convention)."""
    base = date_base(task.due_date, today)
    task.due_date = (base + timedelta(days=delta)).isoformat()
    if task.milestone:                  # a milestone moves whole: one date (D-605)
        task.start_date = task.due_date


MILESTONE_NEEDS_DATE = "a milestone needs a date — give it a due date first"


def set_milestone(task: "Task", on: bool) -> str | None:
    """Make `task` a milestone (`on`) or a task again (LLR-601.1). A milestone has
    ONE date, its due: the start becomes the due, or — with only a start — the
    due becomes the start. With no readable date nothing changes and the reason
    is returned; no date is ever invented. Clearing touches the flag only."""
    if not on:
        task.milestone = False
        return None
    due, start = parse_iso(task.due_date), parse_iso(task.start_date)
    if due is None and start is None:
        return MILESTONE_NEEDS_DATE
    day = (due or start).isoformat()
    task.milestone, task.start_date, task.due_date = True, day, day
    return None


def _extra_keys(d: dict, known: set[str]) -> dict:
    """Every key we don't model, kept verbatim so a load->save round-trip never
    drops data another (older/newer) version of the app wrote."""
    return {k: v for k, v in d.items() if k not in known}


_PROJECT_KEYS = {"id", "name", "color", "status", "archived", "pinned", "start_date",
                 "due_date", "extra"}
_TASK_KEYS = {"id", "title", "project_id", "phase", "blocked", "priority", "start_date",
              "due_date", "notes", "urls", "images", "archived", "pinned", "extra",
              "phase_changed", "depends_on", "milestone",
              "status", "url"}          # last two: legacy, consumed by the migration


def _quarantine_corrupt_file(path: Path):
    """Copy a corrupt/unreadable board file to a `.corrupt` sidecar (never
    clobbering an existing quarantine) so the user's bytes survive even if the
    app later writes a fresh empty board. Returns the backup path, or None."""
    try:
        if not path.exists() or path.stat().st_size == 0:
            return None
        backup = path.with_name(path.name + ".corrupt")
        if not backup.exists():
            shutil.copy2(path, backup)
        return backup
    except OSError:
        return None


def _rescue_task(entry, reason: str) -> "Task":
    """Preserve an unreadable task entry instead of dropping it: the original
    content is kept in `notes` (shown in the task modal) and flagged in `extra`,
    so a format change can never make a task silently vanish."""
    try:
        raw = entry if isinstance(entry, str) else json.dumps(entry, ensure_ascii=False, default=str)
    except Exception:
        raw = repr(entry)
    title = "(recovered task)"
    if isinstance(entry, dict) and isinstance(entry.get("title"), str) and entry["title"].strip():
        title = entry["title"].strip()
    elif isinstance(entry, str) and entry.strip():
        title = "(recovered) " + entry.strip()[:48]
    note = (f"[rescued] this task could not be read normally ({reason}). Its "
            f"original content was preserved below so nothing is lost:\n{raw}")
    return Task(title=title, notes=note,
                extra={"_rescued": True, "_rescue_reason": reason})


def _rescue_project(entry) -> "Project":
    """Preserve an unreadable project entry as a flagged placeholder rather than
    letting one bad row drop every project (which would orphan its tasks)."""
    name = "(recovered project)"
    if isinstance(entry, dict) and isinstance(entry.get("name"), str) and entry["name"].strip():
        name = entry["name"].strip()
    elif isinstance(entry, str) and entry.strip():
        name = "(recovered) " + entry.strip()[:48]
    return Project(name=name, extra={"_rescued": True})


def days_in_phase(task: "Task", today: date) -> int | None:
    """How long this task has sat where it is, or None when the board never
    recorded the move. UNKNOWN IS NOT ZERO: a board written before the stamp
    existed knows nothing about its own history, and inventing a start date for
    it would turn every old task into a fresh one at a glance."""
    moved = parse_iso(task.phase_changed)
    if moved is None:
        return None
    return max(0, (today - moved).days)


def project_color_on_load(color) -> str:
    """The lawful hue for a stored colour: itself if still offered, its ration
    remap if it was dropped, else the `violet` fallback for anything unknown.

    A FIXED POINT — every output is in PROJECT_COLORS and no output is a remap
    key, so loading and saving repeatedly never keeps changing a project's
    colour. A board that used no dropped hue is not touched at all."""
    if not isinstance(color, str):         # a synced or hand-edited value of
        return "violet"                    # any type (S2-2): [] is unhashable
    if color in PROJECT_COLORS:
        return color
    return DROPPED_PROJECT_COLORS.get(color, "violet")


def _coerce_title(value) -> str:
    """A present-but-wrong-typed title (S-9): SCALAR values keep the user's text
    (`str(value)` -- a hand-edited `5` reads "5"); CONTAINERS (list/dict) and
    None become `Untitled` -- a repr of a pathological structure is not a title
    and can blow the cell widths. Never raises."""
    if value is None or isinstance(value, (list, dict)):
        return "Untitled"
    try:
        return str(value)
    except Exception:
        return "Untitled"


@dataclass
class Project:
    name: str
    color: str = "violet"
    status: str = "on_track"
    archived: bool = False
    pinned: bool = False
    start_date: str | None = None
    due_date: str | None = None
    extra: dict = field(default_factory=dict)
    id: str = field(default_factory=_new_id)

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        """The loading rule for a project, from a board file or a teammate's
        `team.json` alike (HLR-404): a name that is not non-empty text is
        `Untitled`, a date that is not text is None, an unknown status or colour
        of any type is the default, a flag is True only as the boolean True."""
        name, start, due = d.get("name"), d.get("start_date"), d.get("due_date")
        return cls(
            id=d.get("id") or _new_id(),
            name=name if isinstance(name, str) and name else "Untitled",
            color=project_color_on_load(d.get("color")),
            status=d.get("status") if d.get("status") in PROJECT_STATUSES else "on_track",
            archived=d.get("archived") is True,
            pinned=d.get("pinned") is True,
            start_date=start if isinstance(start, str) else None,
            due_date=due if isinstance(due, str) else None,
            extra=_extra_keys(d, _PROJECT_KEYS),
        )


@dataclass
class Task:
    title: str
    project_id: str | None = None
    phase: str = "Backlog"
    priority: str = "normal"
    start_date: str | None = None
    due_date: str | None = None
    notes: str = ""
    urls: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    archived: bool = False
    pinned: bool = False
    blocked: bool = False
    depends_on: list[str] = field(default_factory=list)
    # ISO date this task last CHANGED PHASE. None on every task that existed
    # before the field did, and on every task that has never moved — the board
    # has no history, so this can only ever start counting from now. `None`
    # means UNKNOWN and must never be read as zero.
    phase_changed: str | None = None
    # one date, its due, no duration (batch 2026-10-04-batch-02, D-603). Only the
    # boolean true counts: a hand-edited or synced "yes" is not a milestone.
    milestone: bool = False
    extra: dict = field(default_factory=dict)
    id: str = field(default_factory=_new_id)

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        """Total: never raises. A non-object entry, or a dict that trips the
        parser, is rescued into a placeholder Task that PRESERVES the original
        content, so a schema change can never make a task silently disappear."""
        if not isinstance(d, dict):
            return _rescue_task(d, "not a JSON object")
        try:
            # urls: prefer the modern list; migrate a legacy single "url" string
            # into a one-element list (one-way, DD-2); else empty. Never raises.
            if isinstance(d.get("urls"), list):
                urls = [str(u) for u in d["urls"]]
            elif isinstance(d.get("url"), str) and d.get("url"):
                urls = [d["url"]]
            else:
                urls = []
            images = [str(i) for i in d["images"]] if isinstance(d.get("images"), list) else []
            # phase/blocked when present; otherwise migrate the legacy status field.
            legacy_phase, legacy_blocked = LEGACY_STATUS.get(d.get("status"),
                                                             ("Backlog", False))
            phase = d["phase"] if isinstance(d.get("phase"), str) and d["phase"] else legacy_phase
            blocked = bool(d["blocked"]) if "blocked" in d else legacy_blocked
            raw_title = d.get("title", "Untitled")
            title = raw_title if isinstance(raw_title, str) else _coerce_title(raw_title)
            return cls(
                id=d.get("id") or _new_id(),
                title=title,
                project_id=d.get("project_id"),
                phase=phase,
                blocked=blocked,
                extra=_extra_keys(d, _TASK_KEYS),
                priority=d.get("priority") if d.get("priority") in TASK_PRIORITIES else "normal",
                start_date=d.get("start_date"),
                due_date=d.get("due_date"),
                notes=str(d.get("notes") or ""),   # additive; absent on pre-notes boards
                urls=urls,
                images=images,
                archived=bool(d.get("archived", False)),
                pinned=bool(d.get("pinned", False)),
                depends_on=[str(x) for x in d.get("depends_on")]
                if isinstance(d.get("depends_on"), list) else [],
                # additive; absent -> unknown, never back-filled with a guess
                phase_changed=(d.get("phase_changed")
                               if isinstance(d.get("phase_changed"), str) else None),
                milestone=d.get("milestone") is True,
            )
        except Exception as exc:                    # never let one bad task raise
            return _rescue_task(d, type(exc).__name__)


class Board:
    """Owns projects + tasks and the JSON file behind them."""

    def __init__(self, projects: list[Project], tasks: list[Task], path: Path,
                 settings: dict | None = None, phases: list[str] | None = None):
        self.projects = projects
        self.tasks = tasks
        self.path = path
        self.settings = settings or {}
        self._load_report: dict = {}
        # ordered workflow; never empty (progress + every view index into it)
        self.phases = list(phases) if phases else list(DEFAULT_PHASES)

    @property
    def load_report(self) -> dict:
        """Health of the most recent load: how many entries were rescued and
        whether the file was quarantined. Empty dict for a clean load."""
        return self._load_report

    def canonical_phase(self, name: str) -> str:
        """Resolve a stored phase name to this board's spelling. Matching is
        case- and whitespace-insensitive, so a legacy 'backlog' or ' Done '
        snaps to 'Backlog'/'Done' instead of silently falling back to the first
        phase (which would demote finished work)."""
        if not self.phases:
            return name
        table = {p.strip().lower(): p for p in self.phases}
        return table.get(str(name).strip().lower(), self.phases[0])

    def image_dir(self, task_id: str) -> Path:
        """Per-task folder for pasted images, kept beside the board file so the
        raw files are openable by any app: <board-dir>/images/<task_id>/."""
        return self.path.parent / "images" / task_id

    # ---- persistence -------------------------------------------------------
    @classmethod
    def load(cls, path: str | Path) -> "Board":
        path = Path(path)
        if not path.exists():
            # a board this version seeds is new-model data: neither migration has
            # anything to read on it (D-617; B1's links, this batch's milestones)
            board = cls(*seed_data(), path=path,
                        settings={"migrations": {"links": LINKS_MIGRATION,
                                                 "milestones": MILESTONES_MIGRATION}})
            board.save()
            return board
        try:
            # the load door: no control byte gets in. A file nested deeper than
            # the cleaning can follow is unreadable like any other (S4-1).
            raw = clean_strings(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError, TypeError, ValueError, RecursionError):
            raw = None
        if not isinstance(raw, dict):
            # Whole file unreadable: quarantine a copy so a later save can never
            # destroy the user's bytes, then start empty (the file is untouched).
            backup = _quarantine_corrupt_file(path)
            board = cls([], [], path)
            board._load_report = {"file_unreadable": True,
                                  "backup": str(backup) if backup else None,
                                  "projects_rescued": 0, "tasks_rescued": 0}
            return board
        # per-item rescue: one malformed entry can NEVER empty the whole board.
        projects, p_rescued = [], 0
        for p in raw.get("projects", []) or []:
            try:
                projects.append(Project.from_dict(p))
            except Exception:
                projects.append(_rescue_project(p))
                p_rescued += 1
        tasks, t_rescued = [], 0
        for t in raw.get("tasks", []) or []:
            task = Task.from_dict(t)                 # total: rescues internally
            tasks.append(task)
            if task.extra.get("_rescued"):
                t_rescued += 1
        settings = raw.get("settings") if isinstance(raw.get("settings"), dict) else {}
        phases = raw.get("phases")
        if not (isinstance(phases, list) and phases
                and all(isinstance(p, str) and p for p in phases)):
            phases = None
        board = cls(projects, tasks, path, settings, phases)
        for t in board.tasks:                # snap to the board's spelling;
            t.phase = board.canonical_phase(t.phase)   # unknown -> first
        board._load_report = {"file_unreadable": False, "backup": None,
                              "projects_rescued": p_rescued, "tasks_rescued": t_rescued}
        return board

    @staticmethod
    def _to_dict(item) -> dict:
        """Serialize a Project/Task, merging its preserved unknown keys back in
        (known fields win, so our model is always the source of truth)."""
        d = asdict(item)
        return {**d.pop("extra", {}), **d}

    def _serialized(self) -> str:
        return json.dumps({
            "phases": self.phases,
            "projects": [self._to_dict(p) for p in self.projects],
            "tasks": [self._to_dict(t) for t in self.tasks],
            "settings": self.settings,
        }, indent=2)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self._serialized(), encoding="utf-8")

    def save_atomic(self) -> None:
        """Save so the file on disk holds either the old bytes or the new ones,
        never a truncated half: write a fresh temporary file beside the RESOLVED
        file (a symlinked board keeps its link; its target is replaced), then
        swap it in. The temporary name is random and created exclusively
        (`.<board file name>.<random>.tmp`): nothing at it is written through,
        a file a crash left there never blocks a later save, and team pull's
        `board.*.json` never matches it. It goes on failure."""
        target = self.path.resolve()
        if target.exists() and not os.access(target, os.W_OK):
            # a read-only board is refused before anything is written: on
            # Windows its bit, copied to the temp file, made the swap AND the
            # cleanup fail — a temp file per launch, named in the error (D-530)
            raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(target))
        fd, name = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.",
                                    suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(self._serialized())
            # the swapped-in file keeps the board's permissions, not mkstemp's
            # owner-only 0600 (code review N1)
            if target.exists():
                os.chmod(name, stat.S_IMODE(target.stat().st_mode))
            os.replace(name, target)
        except OSError:
            try:                                # the temp file goes on every failure:
                os.chmod(name, stat.S_IREAD | stat.S_IWRITE)    # a copied read-only
                Path(name).unlink(missing_ok=True)              # bit blocks its unlink
            except OSError:
                pass                            # never mask the save's own error
            raise

    # ---- ribbon clock settings --------------------------------------------
    def get_clocks(self) -> tuple[str, str]:
        """The two selected clock CITIES, validated + migrated from old boards."""
        return (self._resolve_clock(self.settings.get("clock1"), DEFAULT_CLOCK1),
                self._resolve_clock(self.settings.get("clock2"), DEFAULT_CLOCK2))

    @staticmethod
    def _resolve_clock(value: str | None, default: str) -> str:
        if value in CITY_TO_ZONE:
            return value
        if value in _LEGACY_ABBREV_TO_CITY:      # pre-city board -> migrate
            return _LEGACY_ABBREV_TO_CITY[value]
        return default

    def set_clocks(self, clock1: str, clock2: str) -> None:
        self.settings["clock1"] = clock1
        self.settings["clock2"] = clock2
        self.save()

    # ---- WIP limits (kanban phase headers, HLR-005 / LLR-005.1) -------------
    def wip_limit(self, phase: str) -> int | None:
        """The WIP limit for `phase`, or None when the phase is unlimited.

        PURE (§6.5 AMD-08): no write side-effects and no read-time
        materialization — this getter NEVER touches `self.settings` and never
        saves, so reading a limit can never dirty a hand-edited board file.
        An operator-set value in `settings["wip_limits"]` wins when it coerces
        to a positive int; anything else (absent, non-numeric, non-positive, or
        keyed to a phase the board does not have) is ignored and falls through
        to the operator-approved default map {"Doing": 3}, then to None.
        `set_wip_limit` is the ONLY write path."""
        if phase not in self.phases:
            return None
        limits = self.settings.get("wip_limits")
        if isinstance(limits, dict) and phase in limits:
            try:
                value = int(limits[phase])
            except (TypeError, ValueError):
                value = 0
            if value > 0:
                return value
        return DEFAULT_WIP_LIMITS.get(phase)

    def set_wip_limit(self, phase: str, limit) -> None:
        """THE ONLY write path for WIP limits — validation and coercion live
        here, never in the getter. A value that coerces to a positive int sets
        the phase's limit; anything else CLEARS it, so there is no way to
        persist a value the getter would have to guess at. The caller saves
        (the add_phase/rename_phase precedent)."""
        limits = dict(self.settings.get("wip_limits") or {})
        try:
            value = int(limit)
        except (TypeError, ValueError):
            value = 0
        if value > 0:
            limits[phase] = value
        else:
            limits.pop(phase, None)
        if limits:
            self.settings["wip_limits"] = limits
        else:
            self.settings.pop("wip_limits", None)

    # ---- lookups -----------------------------------------------------------
    def project_by_id(self, pid: str | None) -> Project | None:
        if pid is None:
            return None
        return next((p for p in self.projects if p.id == pid), None)

    def task_by_id(self, tid: str | None) -> Task | None:
        if tid is None:
            return None
        return next((t for t in self.tasks if t.id == tid), None)

    def visible_projects(self, show_archived: bool) -> list[Project]:
        return [p for p in self.projects if show_archived or not p.archived]

    def visible_tasks(self, show_archived: bool) -> list[Task]:
        return [t for t in self.tasks if show_archived or not t.archived]

    # ---- progress (positional: how far along the phase list a task sits) ----
    def phase_index(self, task: Task) -> int:
        try:
            return self.phases.index(task.phase)
        except ValueError:
            return 0

    def task_progress(self, task: Task) -> float:
        n = len(self.phases)
        return self.phase_index(task) / (n - 1) if n > 1 else 0.0

    def project_progress(self, project_id: str, show_archived: bool = False) -> float:
        rows = [t for t in self.visible_tasks(show_archived) if t.project_id == project_id]
        return sum(self.task_progress(t) for t in rows) / len(rows) if rows else 0.0

    def is_done(self, task: Task) -> bool:
        return bool(self.phases) and task.phase == self.phases[-1]

    # ---- mutations ---------------------------------------------------------
    def auto_archive_done(self, today: date | None = None) -> list[Task]:
        """Archive finished work that has been finished a long time.

        Uses the board's ONE archive: `task.archived`, the same flag `x` toggles,
        so nothing is deleted, nothing moves to a second store, and the existing
        unarchive path reverses it exactly. Returns what it archived.

        THE AGE MUST BE KNOWN. `phase_changed` only exists from the moment that
        field shipped, so a done task that has not moved since has no completion
        date — and a task with no date is not old, it is UNDATED. Archiving it
        would be inventing the history increment 6 refused to invent. In practice
        this means the sweep does nothing on an existing board and starts biting
        only as work is completed from now on.

        'Completed' means the LAST time the task entered its done phase: bouncing
        out of done and back restarts the clock, which is the honest reading of
        'finished 20 days ago'."""
        today = today or date.today()
        moved = []
        for t in self.tasks:
            if t.archived or not self.is_done(t):
                continue
            age = days_in_phase(t, today)
            if age is not None and age >= AUTO_ARCHIVE_DAYS:
                t.archived = True
                moved.append(t)
        return moved

    def unstamped_done(self) -> list[Task]:
        """Finished work the board has NO completion date for — every task that
        was already done when `phase_changed` shipped.

        The standing 20-day sweep cannot touch these and never will: an undated
        task is not old, it is undated, and inventing a date would be the
        fabrication the momentum increment refused. So they need a DELIBERATE
        one-time decision instead, which is what `archive_unstamped_done` is."""
        return [t for t in self.tasks
                if not t.archived and self.is_done(t) and t.phase_changed is None]

    def archive_unstamped_done(self) -> list[Task]:
        """Archive that work, once, because the user asked — never on a timer.

        STAMPS NOTHING. A task archived this way keeps its empty
        `phase_changed`, because the board still does not know when it was
        finished and writing a date now would make that unknowable forever.
        It lands in the ordinary archive, so `v` shows it and `x` brings it
        back like anything else."""
        moved = self.unstamped_done()
        for t in moved:
            t.archived = True
        return moved

    def archivable_report(self, today: date | None = None) -> dict:
        """What the sweep would do, and what it CANNOT know — so the rollout can
        be explained instead of just happening."""
        today = today or date.today()
        done = [t for t in self.tasks if not t.archived and self.is_done(t)]
        aged = [t for t in done if days_in_phase(t, today) is not None]
        return {"done_on_board": len(done),
                "archivable": sum(1 for t in aged
                                  if days_in_phase(t, today) >= AUTO_ARCHIVE_DAYS),
                "too_recent": sum(1 for t in aged
                                  if days_in_phase(t, today) < AUTO_ARCHIVE_DAYS),
                "unknown_age": len(done) - len(aged)}

    def set_task_phase(self, task: Task, phase: str, today: date | None = None) -> bool:
        """Move a task to `phase`, stamping WHEN it moved. Returns whether it
        actually moved — re-saving a task without touching its phase must not
        reset the clock, or every edit would make stale work look fresh.

        The caller saves. This is the ONLY place the stamp is written, so a
        phase that changes by any other route stays honestly unknown."""
        phase = self.canonical_phase(phase)
        if phase == task.phase:
            return False
        old_phase = task.phase
        task.phase = phase
        task.phase_changed = (today or date.today()).isoformat()
        history.append(self.path, {"task": task.id, "from": old_phase, "to": phase})
        return True

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        history.append(self.path, {"task": task.id, "from": None, "to": task.phase})
        self.save()

    def add_project(self, project: Project) -> None:
        self.projects.append(project)
        self.save()

    def delete_task(self, tid: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != tid]
        self.save()

    def delete_project(self, pid: str) -> None:
        """Delete a project; its tasks become standalone (Inbox)."""
        self.projects = [p for p in self.projects if p.id != pid]
        for t in self.tasks:
            if t.project_id == pid:
                t.project_id = None
        self.save()

    # ---- phase mutations (in memory; the caller saves) ----------------------
    def add_phase(self, name: str) -> bool:
        """Append a phase. Rejects blank, or a name already present
        (case-insensitively)."""
        name = str(name).strip()
        if not name or any(p.strip().lower() == name.lower() for p in self.phases):
            return False
        self.phases.append(name)
        return True

    def rename_phase(self, old: str, new: str) -> bool:
        """Rename a phase AND move every task that referenced it. Without the
        second half the tasks would be orphaned and silently demoted to the
        first phase on the next load. A WIP limit set on the phase migrates
        with it (§6.5 AMD-08), so a rename can never orphan an operator-set
        limit either."""
        new = str(new).strip()
        if not new or old not in self.phases:
            return False
        if any(p.strip().lower() == new.lower() and p != old for p in self.phases):
            return False
        self.phases[self.phases.index(old)] = new
        for t in self.tasks:
            if t.phase == old:
                t.phase = new
        limits = self.settings.get("wip_limits")
        if isinstance(limits, dict) and old in limits:
            limits[new] = limits.pop(old)
        return True

    def delete_phase(self, name: str, reassign_to: str | None = None) -> bool:
        """Remove a phase; its tasks move to `reassign_to`, defaulting to the
        previous phase (or the next one when deleting the first). Refuses to
        delete the last remaining phase — a board always needs one."""
        if name not in self.phases or len(self.phases) <= 1:
            return False
        i = self.phases.index(name)
        target = reassign_to if (reassign_to in self.phases and reassign_to != name) else None
        if target is None:
            target = self.phases[i - 1] if i > 0 else self.phases[1]
        self.phases.remove(name)
        for t in self.tasks:
            if t.phase == name:
                t.phase = target
        return True

    def move_phase(self, name: str, delta: int) -> bool:
        """Reorder a phase (-1 earlier, +1 later). Task phase NAMES are
        untouched; only the order changes — which is exactly what progress and
        the estimate read."""
        if name not in self.phases:
            return False
        i = self.phases.index(name)
        j = i + delta
        if not (0 <= j < len(self.phases)):
            return False
        self.phases.insert(j, self.phases.pop(i))
        return True


def standup_query(board: "Board", today: date,
                  show_archived: bool) -> list[tuple[str, list[tuple["Task", bool]]]]:
    """The weekly standup, derived ONLY from `phase_changed` (LLR-011.1) —
    nothing new is stored, so a board that never recorded a move honestly has
    no week to report.

    Returns `(project name, [(task, done), ...])` groups for the visible tasks
    stamped inside the window `today-7 <= phase_changed <= today` — the
    boundary day is IN, eight days ago is OUT, and a None or corrupt stamp is
    OUT (`parse_iso` already reads both as unknown). Groups follow
    `visible_projects` order, anything not under a visible project lands in
    the Inbox LAST, and empty groups simply do not appear (no ghost headers —
    the legend's law applied to the week). `done` is read off
    `board.is_done`, the same seat the board itself uses."""
    week_ago = today - timedelta(days=7)
    moved = [t for t in board.visible_tasks(show_archived)
             if (d := parse_iso(t.phase_changed)) is not None
             and week_ago <= d <= today]
    groups: list[tuple[str, list[tuple[Task, bool]]]] = []
    for p in board.visible_projects(show_archived):
        items = [(t, board.is_done(t)) for t in moved if t.project_id == p.id]
        if items:
            groups.append((p.name, items))
    grouped = {t.id for _name, items in groups for t, _d in items}
    inbox = [(t, board.is_done(t)) for t in moved if t.id not in grouped]
    if inbox:
        groups.append(("Inbox", inbox))
    return groups


def seed_data() -> tuple[list[Project], list[Task]]:
    """Neutral, author-agnostic demo content that exercises every board feature.

    A generic software-product org: it reveals nothing about who built the tool
    while covering all project statuses, every default phase (plus a blocked
    task), priorities, urgency buckets,
    archived items, standalone + project tasks, multiple URLs and images. Anchored
    to today so the urgency buckets stay populated on any run.
    """
    today = date.today()

    def iso(offset_days: int) -> str:
        return (today + timedelta(days=offset_days)).isoformat()

    web = Project("Website Redesign", "sky", "on_track", start_date=iso(-20), due_date=iso(14))
    mobile = Project("Mobile App", "violet", "on_track", start_date=iso(-10), due_date=iso(30))
    api = Project("API Platform", "lime", "paused", start_date=iso(-5), due_date=iso(45))
    legacy = Project("Legacy Sunset", "pink", "cancelled", start_date=iso(-40), due_date=iso(-5))
    warehouse = Project("Data Warehouse", "green", "completed",
                        start_date=iso(-60), due_date=iso(-3))
    wiki = Project("Internal Wiki", "green", "completed", archived=True,
                   start_date=iso(-120), due_date=iso(-80))
    projects = [web, mobile, api, legacy, warehouse, wiki]

    tasks = [
        # Website Redesign — note: image tasks stay normal/low priority + no URL
        # so their card carries only the image glyph (never with the !/↗ markers).
        Task("Design homepage mockups", web.id, "Doing", "normal", due_date=iso(0),
             images=["./mockups/home.png", "./mockups/home-dark.png"]),
        Task("Fix checkout 500 error", web.id, "Doing", "high", due_date=iso(-2),
             blocked=True,
             urls=["https://status.example.com/incident/4821",
                   "https://logs.example.com/checkout"]),
        Task("Optimize image assets", web.id, "Doing", "low", due_date=iso(6),
             images=["https://picsum.photos/seed/hero/640"]),
        # API Platform (paused)
        Task("Write API reference", api.id, "Backlog", "normal", due_date=iso(5),
             urls=["https://docs.example.com/api/v2"]),
        Task("Plan Q3 roadmap", api.id, "Backlog", "normal"),
        Task("Deprecate v1 endpoints", api.id, "Backlog", "high", due_date=iso(9)),
        # Mobile App
        Task("Audit dependencies", mobile.id, "Doing", "normal", due_date=iso(12)),
        Task("Set up CI pipeline", mobile.id, "Done", "normal"),
        Task("Add push notifications", mobile.id, "Backlog", "normal", due_date=iso(18)),
        # Data Warehouse (completed)
        Task("Migrate user table", warehouse.id, "Done", "low"),
        Task("Compress database backups", warehouse.id, "Doing", "normal",
             due_date=iso(-1), blocked=True),
        Task("Archive old logs", warehouse.id, "Backlog", "low", due_date=iso(25),
             archived=True),
        # Legacy Sunset (cancelled)
        Task("Shut down legacy servers", legacy.id, "Backlog", "normal", due_date=iso(8)),
        # standalone tasks -> Inbox
        Task("Renew TLS certificate", None, "Backlog", "high", due_date=iso(3)),
        Task("Update onboarding copy", None, "Backlog", "normal"),
        Task("Review pull requests", None, "Doing", "normal", due_date=iso(1)),
    ]
    return projects, tasks


def unblocks_count(board: Board, task: Task) -> int:
    """How many OPEN tasks directly depend on ``task``.

    Dangling ids in ``depends_on`` are ignored, and done/archived dependents do
    not count — they no longer need unblocking.  Direct edges only: a task that
    depends on a dependent of ``task`` is not counted here (that is the critical
    chain's job in increment 4)."""
    tid = task.id
    count = 0
    for t in board.tasks:
        if t is task:
            continue
        if board.is_done(t) or t.archived:
            continue
        if tid in t.depends_on:
            count += 1
    return count


def critical_chain(board: Board) -> list[str]:
    """The longest open-task dependency chain, or ``[]`` when there are none.

    A chain is a sequence of open tasks where each task unblocks the next
    (``next.depends_on`` contains the previous task's id).  Dangling ids are
    ignored, and a hand-edited cycle cannot hang the renderer because every
    search path keeps a visited set.
    """
    open_tasks = [t for t in board.visible_tasks(False) if not board.is_done(t)]
    open_ids = {t.id for t in open_tasks}
    if len(open_ids) < 2:
        return []

    dependents: dict[str, list[str]] = {tid: [] for tid in open_ids}
    for t in open_tasks:
        for dep_id in t.depends_on:
            if dep_id in open_ids and dep_id != t.id:
                dependents[dep_id].append(t.id)
    for dep_list in dependents.values():
        dep_list.sort()

    def longest_from(start: str) -> list[str]:
        best = [start]

        def extend(current: str, path: list[str], seen: set[str]):
            nonlocal best
            for nxt in dependents.get(current, []):
                if nxt in seen:
                    continue
                new_path = path + [nxt]
                if len(new_path) > len(best) or (
                    len(new_path) == len(best) and new_path < best
                ):
                    best = new_path
                extend(nxt, new_path, seen | {nxt})

        extend(start, [start], {start})
        return best

    best_chain: list[str] = []
    for tid in sorted(open_ids):
        chain = longest_from(tid)
        if len(chain) > len(best_chain) or (
            len(chain) == len(best_chain) and chain < best_chain
        ):
            best_chain = chain
    return best_chain if len(best_chain) >= 2 else []


# ---- links: "waits on" (batch 2026-10-04-batch-01) ---------------------------
def is_open(board: Board, task: Task) -> bool:
    """Neither in the board's last phase nor archived (LLR-501.1)."""
    return not board.is_done(task) and not task.archived


# ---- the one-time link migration (HLR-505) -----------------------------------
# Until this batch the ONLY writer of `depends_on` was `b`: blocking appended the
# picked id and set the flag; unblocking cleared the flag and KEPT the id. Read
# with the new meaning (a link = "waits on"), every kept id would re-block work
# the user had already unblocked. `migrate_links` reads the legacy shapes back by
# the rule the operator ruled on (`deps_logic.migrate`) plus D-515 and D-516;
# `run_link_migration` applies it ONCE, a backup first.
LINKS_MIGRATION = 1
MIGRATION_BACKUP = ".pre-links-migration"
MIGRATION_LOG = ".links-migration-log"


@dataclass
class LinkChange:
    task_id: str
    title: str
    before: tuple[bool, list[str]]
    after: tuple[bool, list[str]]
    note: str


@dataclass
class LinkMigration:
    changes: list[LinkChange]
    backup: str | None = None
    log: str | None = None
    error: str | None = None


def links_marked(settings: dict) -> bool:
    """Marked ⇔ `settings["migrations"]` is a dict whose `links` is exactly the
    int 1. Read totally: a hand-edited value of any type never raises (S-4)."""
    m = settings.get("migrations")
    return (isinstance(m, dict) and type(m.get("links")) is int
            and m.get("links") == LINKS_MIGRATION)


def migrate_links(board: Board) -> list[LinkChange]:
    """What the legacy rule changes, per task in board order; the board is NOT
    touched (LLR-505.1).

    Dangling, self and repeated ids go. A blocked task whose last stored id is
    live and OPEN now waits on it and loses the flag — the flag `b` set meant
    exactly that link. Its last stored id live but CLOSED: the flag stays (D-515:
    it may have been set again after that link was done). No live last id: the
    flag stays (an outside block, or a deleted blocker nobody can vouch for).
    Every other id pointing at an open task was released by an unblock and goes;
    ids pointing at a closed task are satisfied and stay. Any link that would
    close a loop over the links already kept goes too, and a blocker dropped so
    leaves its flag on (D-516) — so the migrated board holds no cycle."""
    by_id: dict[str, Task] = {}
    for t in board.tasks:
        by_id.setdefault(t.id, t)       # the first of a repeated id, as task_by_id
    into: dict[str, list[str]] = {}     # x -> the tasks whose kept links point at x
    done_ids: set[str] = set()          # tasks already processed (they own kept links)
    changes: list[LinkChange] = []
    for t in board.tasks:
        if by_id[t.id] is not t:
            continue                    # a repeated id: left as it is (F4)
        stored = list(t.depends_on)
        live = list(dict.fromkeys(x for x in stored if x != t.id and x in by_id))
        last = stored[-1] if stored else None
        blocker = last if t.blocked and last in by_id and last != t.id else None
        wanted = [x for x in live if not is_open(board, by_id[x]) or x == blocker]
        if t.id in into and any(x in done_ids for x in wanted):
            # one walk back over the kept links: every task that can already
            # reach this one; a link to any of them would close a loop. Only a
            # processed task owns kept links, so only a link to one can close it
            reach, todo = {t.id}, [t.id]
            while todo:
                for a in into.get(todo.pop(), ()):
                    if a not in reach:
                        reach.add(a)
                        todo.append(a)
            keep = [x for x in wanted if x not in reach]
        else:
            keep = wanted
        for x in keep:
            into.setdefault(x, []).append(t.id)
        done_ids.add(t.id)
        blocked, note = t.blocked, "released links dropped"
        if blocker is not None and is_open(board, by_id[blocker]):
            if blocker in keep:
                blocked = False
                note = "flag cleared, waits on its blocker — press b if this was an outside block"
            else:
                note = "blocked kept — its link would close a loop"
        elif t.blocked:
            note = ("blocked kept — its last link is done" if blocker is not None
                    else "blocked kept — no task to wait on")
        if (blocked, keep) != (t.blocked, stored):
            changes.append(LinkChange(t.id, t.title, (t.blocked, stored),
                                      (blocked, keep), note))
    return changes


def _create_beside(target: Path, suffix: str, data: bytes) -> Path:
    """Write `data` to `<file name><suffix>` beside `target`, or to the first
    free `.1`, `.2`, … — by EXCLUSIVE create, so no existing file is ever
    overwritten and no symlink (dangling or not) is written through."""
    for n in range(1000):
        p = target.with_name(target.name + suffix + (f".{n}" if n else ""))
        if p.is_symlink():
            continue
        try:
            with open(p, "xb") as fh:
                fh.write(data)
            return p
        except FileExistsError:
            continue
    raise FileExistsError(errno.EEXIST, "no free name", target.name + suffix)


def _set_links(board: Board, changes: list[LinkChange], side: str) -> None:
    for ch in changes:
        t = board.task_by_id(ch.task_id)
        if t is not None:
            blocked, deps = getattr(ch, side)
            t.blocked, t.depends_on = blocked, list(deps)


def run_link_migration(board: Board, today: date | None = None) -> LinkMigration | None:
    """Migrate the board's links ONCE (LLR-505.2). None when there is nothing to
    run: the load was unreadable, or the board carries the mark.

    Order: the backup (the board file's own bytes), then the log, then the
    changes, the mark and ONE atomic save. Any failure restores the board and
    the mark in memory FIRST, then removes this run's backup/log best-effort
    (never raising), leaves the file untouched and unmarked, and returns the
    reason — a file name and the OS's words, never a directory path. A malformed
    mark is replaced, and replacing it forces the backup and the log (S2-2)."""
    if board.load_report.get("file_unreadable") or links_marked(board.settings):
        return None
    had_mark = "migrations" in board.settings
    old_mark = board.settings.get("migrations")
    changes = migrate_links(board)
    result = LinkMigration(changes)
    target = board.path.resolve()
    try:
        if changes or had_mark:
            result.backup = _create_beside(target, MIGRATION_BACKUP,
                                           target.read_bytes()).name
            log = {"date": (today or date.today()).isoformat(),
                   "backup": result.backup,
                   "replaced_mark": old_mark if had_mark else None,
                   "changes": [asdict(ch) for ch in changes]}
            result.log = _create_beside(target, MIGRATION_LOG,
                                        json.dumps(log, indent=2).encode("utf-8")).name
        _set_links(board, changes, "after")
        # a dict keeps its other keys (S3-3); anything else is replaced whole
        mark = dict(old_mark) if isinstance(old_mark, dict) else {}
        mark["links"] = LINKS_MIGRATION
        board.settings["migrations"] = mark
        board.save_atomic()
    except OSError as exc:
        _set_links(board, changes, "before")        # restore the board first …
        if had_mark:                                 # … then the migration mark
            board.settings["migrations"] = old_mark
        else:
            board.settings.pop("migrations", None)
        for made in (result.log, result.backup):     # then this run's files,
            if made:                                 # best-effort, never raising
                try:
                    (target.parent / made).unlink(missing_ok=True)
                except OSError:
                    pass
        result.backup = result.log = None
        name = Path(exc.filename).name if exc.filename else target.name
        result.error = f"{name}: {exc.strerror or type(exc).__name__}"
    return result


# ---- the one-time milestone offer (HLR-605, M-3 as a migration) ---------------
# An existing board holds the operator's habit: milestones typed as one-day tasks
# (start == due) and dated tasks with no start. The offer shows them ONCE; it
# converts exactly what the user checks, a backup and a log first, and records the
# mark whatever the answer, so it never shows again (operator: "Sí: respaldo +
# registro + deshacer").
MILESTONES_MIGRATION = 1
MILESTONE_BACKUP = ".pre-milestones"
MILESTONE_LOG = ".milestones-log"
MILESTONE_LOG_NOTE = ("restoring the backup brings back a board without the offer's mark; "
                      "the offer is shown again at the next start")


def milestones_marked(settings: dict) -> bool:
    """Marked ⇔ `settings["migrations"]` is a dict whose `milestones` is exactly
    the int 1 — read totally, as `links_marked` reads its own key (LLR-605.1)."""
    m = settings.get("migrations")
    return (isinstance(m, dict) and type(m.get("milestones")) is int
            and m.get("milestones") == MILESTONES_MIGRATION)


def milestone_candidates(board: Board) -> list[tuple[Task, bool]]:
    """`(task, preset)` for every open board task (the first of a repeated id) that
    is not a milestone, has a text title and a readable due: preset when its
    readable start equals its due (one-day), not preset when it has no start
    (due-only); any other start is a duration and not a candidate. Group 1 first,
    then by due, then board order (LLR-605.1)."""
    by_id = _ids(board)
    rows = []
    for i, t in enumerate(board.tasks):
        if by_id.get(t.id) is not t:
            continue                    # a repeated id: the first one only (B1 F4)
        if (not is_open(board, t) or t.milestone or not isinstance(t.title, str)):
            continue
        due = parse_iso(t.due_date)
        if due is None:
            continue
        if t.start_date is None or t.start_date == "":
            rows.append((False, due, i, t))
        elif parse_iso(t.start_date) == due:
            rows.append((True, due, i, t))
    rows.sort(key=lambda r: (not r[0], r[1], r[2]))
    return [(t, preset) for preset, _d, _i, t in rows]


@dataclass
class MilestoneConversion:
    changes: list[dict]
    ineligible: int = 0
    backup: str | None = None
    log: str | None = None
    error: str | None = None


def run_milestone_offer(board: Board, chosen, today: date | None = None
                        ) -> MilestoneConversion | None:
    """Answer the offer ONCE (LLR-605.2). None on an unreadable load or a marked
    board. Converts each CANDIDATE (re-read now) whose id was chosen, at most once;
    chosen ids no longer candidates are counted, never converted. With anything to
    convert — or a malformed mark to replace — the board file's bytes are read once,
    here, and backed up, then logged, by exclusive create; then the flags, the mark
    and ONE atomic save. Any failure restores the board in memory FIRST, then removes
    this run's files best-effort, and returns the reason (basename and strerror)."""
    if board.load_report.get("file_unreadable") or milestones_marked(board.settings):
        return None
    chosen = list(chosen)
    had_mark = "migrations" in board.settings
    old_mark = board.settings.get("migrations")
    replaced = (had_mark and not isinstance(old_mark, dict)) or (
        isinstance(old_mark, dict) and "milestones" in old_mark)
    cands = [t for t, _preset in milestone_candidates(board)]
    picked = set(chosen)
    convert = [t for t in cands if t.id in picked]          # each at most once
    result = MilestoneConversion([], len(picked - {t.id for t in convert}))
    # each converted task's stored dates, byte-exact: converting writes the due in
    # canonical form, so both come back on a failure and with `u` (security S4-1)
    before = [(t, t.milestone, t.start_date, t.due_date) for t in convert]
    target = board.path.resolve()
    made: list[str] = []
    try:
        if convert or replaced:
            raw = target.read_bytes()
            result.backup = _create_beside(target, MILESTONE_BACKUP, raw).name
            made.append(result.backup)
            log = {"date": (today or date.today()).isoformat(), "backup": result.backup,
                   "replaced_mark": old_mark if replaced else None,
                   "note": MILESTONE_LOG_NOTE,
                   "changes": [{"task_id": t.id, "title": t.title, "start_before": t.start_date,
                                "due_before": t.due_date,
                                "start_after": parse_iso(t.due_date).isoformat()}
                               for t in convert]}
            result.log = _create_beside(target, MILESTONE_LOG,
                                        json.dumps(log, indent=2).encode("utf-8")).name
            made.append(result.log)
        for t in convert:
            set_milestone(t, True)
        mark = dict(old_mark) if isinstance(old_mark, dict) else {}
        mark["milestones"] = MILESTONES_MIGRATION
        board.settings["migrations"] = mark
        board.save_atomic()
        result.changes = [{"task_id": t.id, "title": t.title, "start_before": s0,
                           "due_before": d0, "start_after": t.start_date}
                          for t, _m0, s0, d0 in before]
    except OSError as exc:
        for t, m0, s0, d0 in before:             # the board first …
            t.milestone, t.start_date, t.due_date = m0, s0, d0
        if had_mark:
            board.settings["migrations"] = old_mark
        else:
            board.settings.pop("migrations", None)
        for name in made:                        # … then this run's files, best-effort
            try:
                (target.parent / name).unlink(missing_ok=True)
            except OSError:
                pass
        result.backup = result.log = None
        name = Path(exc.filename).name if exc.filename else target.name
        result.error = f"{name}: {exc.strerror or type(exc).__name__}"
    return result


# ---- the waits-on model (LLR-501.1) ------------------------------------------
# A link is an id in `depends_on`: the task (the waiter) waits on the task with
# that id (the predecessor). It is independent of `blocked`, the external block.
# Waiting is DERIVED, never stored. Only board tasks count (a teammate's task is
# never one), only LIVE links (an id naming another board task), once per id.
# Every derivation looks tasks up through one id map and recurses nowhere, so a
# hand-edited or hostile board (a stored cycle, a task with 100 000 ids) costs
# a bounded walk, never a hang (S-5, D-522).


def _ids(board: Board) -> dict[str, Task]:
    out: dict[str, Task] = {}
    for t in board.tasks:
        out.setdefault(t.id, t)
    return out


def _live(task: Task, by_id: dict[str, Task]) -> list[Task]:
    return [by_id[x] for x in dict.fromkeys(task.depends_on)
            if x != task.id and x in by_id]


def open_predecessors(board: Board, task: Task, by_id: dict | None = None) -> list[Task]:
    """The open tasks `task` waits on — none when `task` itself is closed."""
    if not is_open(board, task):
        return []
    by_id = by_id if by_id is not None else _ids(board)
    return [p for p in _live(task, by_id) if is_open(board, p)]


def open_dependents(board: Board, task: Task) -> list[Task]:
    """The open tasks that wait on `task` — none when `task` itself is closed
    (a finished predecessor's links are satisfied)."""
    if not is_open(board, task):
        return []
    return [t for t in _ids(board).values()
            if t is not task and task.id in t.depends_on and is_open(board, t)]


def link_marks(board: Board) -> dict[str, tuple[int, int]]:
    """(◂ open predecessors, ▸ open dependents) per board task, built from ONE
    pass over the links (a reverse index), so a render pays O(links) once."""
    by_id = _ids(board)
    marks = {tid: [0, 0] for tid in by_id}
    for t in by_id.values():
        if not is_open(board, t):
            continue
        for p in _live(t, by_id):
            if is_open(board, p):
                marks[t.id][0] += 1
                marks[p.id][1] += 1
    return {k: (w, u) for k, (w, u) in marks.items()}


def dependents_chain(board: Board, task: Task) -> list[tuple[Task, int]]:
    """Every open task that waits on `task` — directly (depth 1) or down the
    chain (depth ≥ 2) — breadth first, each once."""
    waiters: dict[str, list[Task]] = {}
    for t in board.tasks:
        if is_open(board, t):
            for x in dict.fromkeys(t.depends_on):
                if x != t.id:
                    waiters.setdefault(x, []).append(t)
    out, seen, level, depth = [], {task.id}, [task], 0
    if not is_open(board, task):
        return out
    while level:
        depth += 1
        nxt = []
        for cur in level:
            for w in waiters.get(cur.id, ()):
                if w.id not in seen:
                    seen.add(w.id)
                    out.append((w, depth))
                    nxt.append(w)
        level = nxt
    return out


def link_overlap(waiter: Task, pred: Task) -> int:
    """THE overlap measure (`cascade.overlap`, one everywhere — D-503, D-633), in days,
    both days counting: a waiter with a start overlaps by `pred.due − start + 1`;
    one with no start compares dues, `pred.due − waiter.due`; 0 when a date it
    needs is absent. A start ON the predecessor's due day is 1 day. The single
    rule lives in `_cascade_overlap` (D-633) — this reads the STORED dates."""
    return _cascade_overlap(parse_iso(waiter.start_date), parse_iso(waiter.due_date),
                            parse_iso(pred.due_date))


def link_conflicts(board: Board, task: Task) -> list[tuple[Task, int]]:
    """The open predecessors whose overlap with `task` is ≥ 1 day (rule 9′)."""
    return [(p, n) for p in open_predecessors(board, task)
            if (n := link_overlap(task, p)) >= 1]


# --- moving linked dates (batch 2026-10-06-batch-01, LLR-604.1) ----------------
CASCADE_MODES = ("flag", "push_delta", "together")
CASCADE_ALL_MODES = CASCADE_MODES + ("push",)
CASCADE_DEFAULT_MODE = "push_delta"


@dataclass
class Plan:
    """What one date move does to a chain, computed before anything is written."""
    mode: str
    moved: dict = field(default_factory=dict)          # id -> (start|None, due|None)
    shift: dict = field(default_factory=dict)          # id -> days
    conflicts: list = field(default_factory=list)      # (waiter, pred, TOTAL days) after —
                                                       # the tested intermediate (TC-629);
                                                       # production reads new_conflicts
    new_conflicts: list = field(default_factory=list)  # (waiter, pred, ADDED days)
    project_over: dict = field(default_factory=dict)   # project id -> days past due, after
    project_over_before: dict = field(default_factory=dict)


def _cascade_dates(t: Task) -> tuple[date | None, date | None]:
    """A task's dates for the cascade: a milestone's start IS its due (the shipped
    invariant), so the milestone always takes the start arm of the measure."""
    s, d = parse_iso(t.start_date), parse_iso(t.due_date)
    if t.milestone and d:
        s = d
    return s, d


def _cascade_open(board: Board, t: Task) -> bool:
    return not board.is_done(t) and not t.archived


def _cascade_dependents(board: Board, tid: str) -> list[Task]:
    return [t for t in board.tasks if tid in t.depends_on and _cascade_open(board, t)]


def _cascade_downstream(board: Board, tid: str) -> set[str]:
    """Open tasks that transitively wait on tid, through open tasks only."""
    t = board.task_by_id(tid)
    if t is None or not _cascade_open(board, t):
        return set()
    seen, todo = set(), [tid]
    while todo:
        for w in _cascade_dependents(board, todo.pop()):
            if w.id not in seen:
                seen.add(w.id)
                todo.append(w.id)
    return seen


def _cascade_overlap(ws: date | None, wd: date | None, pdue: date | None) -> int:
    """`link_overlap`'s rule on PLANNED dates (D-633 — ONE measure, the same one
    the screen paints): both days count on the start arm."""
    if pdue is None:
        return 0
    if ws is not None:
        return max(0, (pdue - ws).days + 1)
    return max(0, (pdue - wd).days) if wd is not None else 0


def resolve_mode(board: Board, task_id: str, override: str | None = None) -> str:
    """The mode a move runs under: the per-move override, else the moved task's
    project's `date_links`, else the default. A stored value outside the three
    modes reads as the default (the lenient model — it arrives from a file)."""
    if override in CASCADE_ALL_MODES:
        return override
    t = board.task_by_id(task_id)
    pr = board.project_by_id(t.project_id) if t is not None else None
    v = pr.extra.get("date_links") if pr is not None else None
    return v if v in CASCADE_MODES else CASCADE_DEFAULT_MODE


def plan_move(board: Board, task_id: str, start_delta: int, due_delta: int, mode: str,
              today: date) -> Plan:
    """Plan the cascade of one date move — pure, writes nothing.

    Modes (LLR-604.1): `flag` moves nothing else (the shipped ↳ conflict mark is
    the flag); `push_delta` (DEFAULT) pushes a dependent later by only the overlap
    the move ADDED — slack absorbs, a pre-existing overlap is tolerated, a zero or
    earlier move pulls nothing; `together` shifts the whole open downstream by the
    due delta, both directions (all gaps kept); `push` (strict finish-to-start) is
    accepted under its name and offered nowhere. Done/archived never move and stop
    the chain. A milestone ignores `start_delta` and moves whole. An undated moved
    task bases its dates on `today` (the bump's own rule) before the cascade is
    computed."""
    assert mode in CASCADE_ALL_MODES, mode
    t = board.task_by_id(task_id)
    if t.milestone:
        start_delta = due_delta
    s, d = _cascade_dates(t)
    if s is None and start_delta:
        s = date_base(t.start_date, today)
    if d is None and due_delta:
        d = date_base(t.due_date, today)
    plan = Plan(mode)
    plan.moved[task_id] = (s + timedelta(days=start_delta) if s else None,
                           d + timedelta(days=due_delta) if d else None)
    plan.shift[task_id] = due_delta
    down = _cascade_downstream(board, task_id)

    def new(x: Task):
        return plan.moved.get(x.id, _cascade_dates(x))

    def put(w: Task, k: int):
        ws, wd = _cascade_dates(w)
        kk = timedelta(days=k)
        plan.moved[w.id] = (ws + kk if ws else None, wd + kk if wd else None)
        plan.shift[w.id] = k

    if mode == "together" and due_delta:
        for wid in down:
            put(board.task_by_id(wid), due_delta)
    elif mode in ("push", "push_delta"):
        todo = [task_id]
        while todo:
            for w in _cascade_dependents(board, todo.pop(0)):
                k = 0
                for p in w.depends_on:
                    pt = board.task_by_id(p)
                    if pt is None or not _cascade_open(board, pt):
                        continue
                    ov_new = _cascade_overlap(*_cascade_dates(w), new(pt)[1])
                    ov_old = (_cascade_overlap(*_cascade_dates(w), _cascade_dates(pt)[1])
                              if mode == "push_delta" else 0)
                    k = max(k, ov_new - ov_old)
                if k > plan.shift.get(w.id, 0):
                    put(w, k)
                    todo.append(w.id)

    def old(x: Task):
        return _cascade_dates(x)

    def conflicts(dates) -> list[tuple[str, str, int]]:
        out = []
        for w in board.tasks:
            if not _cascade_open(board, w):
                continue
            for p in w.depends_on:
                pt = board.task_by_id(p)
                if pt and _cascade_open(board, pt):
                    ov = _cascade_overlap(*dates(w), dates(pt)[1])
                    if ov:
                        out.append((w.id, p, ov))
        return out

    before = {(a, b_): n for a, b_, n in conflicts(old)}
    plan.conflicts = conflicts(new)
    plan.new_conflicts = [(a, b_, n - before.get((a, b_), 0))   # the ADDED days; a
                          for a, b_, n in plan.conflicts         # pair that never existed
                          if n > before.get((a, b_), 0)]         # before is still added

    def over(ids, dates) -> dict[str, int]:
        out: dict[str, int] = {}
        for i in ids:
            x = board.task_by_id(i)
            pr = board.project_by_id(x.project_id)
            pdue = parse_iso(pr.due_date) if pr else None
            nd = dates(x)[1]
            if pdue and nd and nd > pdue:
                out[pr.id] = max(out.get(pr.id, 0), (nd - pdue).days)
        return out

    plan.project_over = over(plan.moved, new)
    plan.project_over_before = over([x.id for x in board.tasks], old)
    return plan


def apply_plan(board: Board, plan: Plan) -> None:
    """Write a plan's dates. A milestone's stored start follows its due (the plan
    holds them equal); a task that vanished since the plan is skipped (C-2)."""
    for tid, (s, d) in plan.moved.items():
        t = board.task_by_id(tid)
        if t is None:
            continue
        if t.start_date is not None and s:
            t.start_date = s.isoformat()
        if d:
            t.due_date = d.isoformat()


def snapshot(board: Board, plan: Plan) -> dict[str, tuple[str | None, str | None]]:
    """One undo step: the stored dates of every task the plan will touch (a task
    that vanished since the plan is skipped — its bytes are already gone)."""
    out = {}
    for i in plan.moved:
        t = board.task_by_id(i)
        if t is not None:
            out[i] = (t.start_date, t.due_date)
    return out


def restore(board: Board, snap: dict) -> None:
    for i, (s, d) in snap.items():
        t = board.task_by_id(i)
        if t is None:
            continue
        t.start_date, t.due_date = s, d


def loop_path(board: Board, waiter: Task, pred: Task) -> list[Task] | None:
    """Would `waiter` waiting on `pred` close a loop? Searches every stored live
    link, closed tasks included (D-512), iteratively with parent pointers, and
    returns `waiter → pred → … → waiter`, or None."""
    by_id = _ids(board)
    if pred.id == waiter.id:
        return [waiter, waiter]
    if pred.id not in by_id:            # not a board task: no stored link reaches it
        return None
    parent: dict[str, str | None] = {pred.id: None}
    todo = [pred.id]
    while todo:
        cur = todo.pop()
        for p in _live(by_id[cur], by_id):
            if p.id in parent:
                continue
            parent[p.id] = cur
            if p.id == waiter.id:
                path, node = [], p.id
                while node is not None:
                    path.append(by_id[node])
                    node = parent[node]
                return [waiter] + path[::-1]
            todo.append(p.id)
    return None


def waiting_ids(board: Board) -> set[str]:
    """The ids of the open tasks with at least one open predecessor."""
    return {tid for tid, (w, _u) in link_marks(board).items() if w}


def ready_messages(board: Board, waiting_before: set[str], finished: set[str]) -> list[str]:
    """One line per task that stopped waiting in a mutation that moved the tasks
    `finished` into the last phase: "‹title› is ready — ‹pred› done" (+ " (still
    ▲ blocked)"). At most 3 lines, then one "+K more ready" (D-508). A task let
    go only because a link was removed is not listed — that was the user's act."""
    by_id = _ids(board)
    now = waiting_ids(board)
    lines = []
    for t in board.tasks:
        if t.id not in waiting_before or t.id in now or not is_open(board, t):
            continue
        preds = [p for p in _live(t, by_id) if p.id in finished]
        if not preds:
            continue
        line = (f"{_clip_title(t.title)} is ready — "
                + ", ".join(_clip_title(p.title) for p in preds) + " done")
        lines.append(line + (" (still ▲ blocked)" if t.blocked else ""))
    if len(lines) > 3:
        lines = lines[:3] + [f"+{len(lines) - 3} more ready"]
    return lines


def _clip_title(title: str, n: int = 40) -> str:
    return title if len(title) <= n else title[:n - 1] + "…"


def _names(tasks: list[Task]) -> str:
    shown = ", ".join(_clip_title(t.title) for t in tasks[:3])
    return shown + (f" and {len(tasks) - 3} more" if len(tasks) > 3 else "")


def archive_refusal(board: Board, task: Task, verb: str,
                    leaving: set[str] | None = None) -> str | None:
    """Why `task` cannot be archived or deleted (`verb`), or None (HLR-504): an
    OPEN task that open tasks outside `leaving` (what is being archived with it)
    wait on is refused, naming them. A finished task archives as before."""
    leaving = leaving or {task.id}
    waiters = [w for w in open_dependents(board, task) if w.id not in leaving]
    if not waiters:
        return None
    n = len(waiters)
    return (f"can't {verb} {_clip_title(task.title)} — {n} open task"
            f"{'s wait' if n != 1 else ' waits'} on it ({_names(waiters)}). "
            "Finish it, or remove the link in its details (↵, then x).")


# ---- choosing a link (LLR-502.1, LLR-502.2) ----------------------------------
def _md(d: date) -> str:
    return f"{d:%b} {d.day}"


def link_refusal(board: Board, waiter: Task, pred: Task) -> str | None:
    """Why `waiter` may not wait on `pred`, or None: the task itself, a closed
    task, or a loop — named by its path (a long one shortened in the middle)."""
    if pred.id == waiter.id:
        return "a task cannot wait on itself"
    if not is_open(board, pred):
        return f"{_clip_title(pred.title)} is closed"
    path = loop_path(board, waiter, pred)
    if path:
        names = [_clip_title(t.title) for t in path]
        if len(names) > 6:
            names = names[:3] + ["…"] + names[-2:]
        return "would create a loop: " + " → ".join(names)
    return None


def link_hint(waiter: Task, pred: Task) -> str:
    """What waiting on `pred` would mean for `waiter`'s dates (the one measure,
    D-503), in the words of LLR-502.2."""
    s, d = parse_iso(waiter.start_date), parse_iso(waiter.due_date)
    pd = parse_iso(pred.due_date)
    if s is None and d is None:
        return "this has no dates — timing can't be checked"
    if pd is None:
        return "no due date — timing can't be checked"
    n = link_overlap(waiter, pred)
    if s is not None:
        return (f"◂ overlaps {n}d: due {_md(pd)}, this starts {_md(s)}" if n
                else f"ok — due {(s - pd).days}d before this starts")
    return (f"◂ overlaps {n}d: due {_md(pd)}, this is due {_md(d)}" if n
            else "ok — due on or before the day this is due")


@dataclass
class LinkCandidate:
    task: Task
    same_project: bool
    linked: bool
    loop: list[Task] | None
    hint: str


def loopers_of(board: Board, waiter: Task) -> set[str]:
    """Every board task that already (transitively) waits on `waiter`, over
    every stored live link, closed tasks included: making `waiter` wait on any
    of them closes a loop. ONE reverse walk per picker open (D-522)."""
    waits_on_me: dict[str, list[str]] = {}
    by_id = _ids(board)
    for t in by_id.values():
        for p in _live(t, by_id):
            waits_on_me.setdefault(p.id, []).append(t.id)
    seen, todo = {waiter.id}, [waiter.id]
    while todo:
        for x in waits_on_me.get(todo.pop(), ()):
            if x not in seen:
                seen.add(x)
                todo.append(x)
    seen.discard(waiter.id)
    return seen


def link_candidates(board: Board, waiter: Task, query: str = "",
                    loopers: set[str] | None = None) -> list[LinkCandidate]:
    """The tasks `waiter` could wait on (LLR-502.2): every open board task but
    the waiter, its own project first, then by due (undated last), then title;
    `query` keeps titles containing it, case-insensitively. A candidate already
    linked says so; one that would close a loop carries its path."""
    q = query.strip().lower()
    loopers = loopers if loopers is not None else loopers_of(board, waiter)
    linked = set(waiter.depends_on)
    out = []
    for t in _ids(board).values():
        if t is waiter or not is_open(board, t) or (q and q not in t.title.lower()):
            continue
        loop = loop_path(board, waiter, t) if t.id in loopers else None
        hint = link_hint(waiter, t)
        out.append(LinkCandidate(t, t.project_id == waiter.project_id, t.id in linked,
                                 loop, hint))
    out.sort(key=lambda c: (not c.same_project, parse_iso(c.task.due_date) is None,
                            parse_iso(c.task.due_date) or date.max, c.task.title.lower()))
    return out


def project_archive_refusal(board: Board, project_id: str) -> str | None:
    """The project archive's guard (D-523): archiving a project archives its
    tasks, so it is refused when an open task OUTSIDE the project waits on one
    of them — named, as `archive_refusal` names them."""
    inside = {t.id for t in board.tasks if t.project_id == project_id}
    waiters: list[Task] = []
    for t in board.tasks:
        if t.id in inside:
            for w in open_dependents(board, t):
                if w.id not in inside and all(w is not x for x in waiters):
                    waiters.append(w)
    if not waiters:
        return None
    n = len(waiters)
    return (f"can't archive this project — {n} open task"
            f"{'s' if n != 1 else ''} outside it wait{'' if n != 1 else 's'} on its "
            f"tasks ({_names(waiters)}). Finish them, or remove the links first.")

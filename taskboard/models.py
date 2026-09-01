"""Data model + JSON persistence for the taskboard widget.

Two entities (Project, Task) and a Board that owns them and reads/writes a
single JSON file. Tasks may be standalone (project_id is None) -> shown in the
"Inbox" group. A missing file is seeded with demo data; a corrupt file starts
empty (we never overwrite it, so the user can recover it by hand).
"""

from __future__ import annotations

import json
import shutil
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


def _clean_clipboard_text(text: str | None) -> str | None:
    """Make clipboard text safe to insert into a field: drop C0/C1 control
    characters (except tab/newline/carriage-return) so stray control bytes can't
    corrupt the terminal, and cap the length so a huge/binary clipboard can't
    freeze rendering. None if nothing usable remains."""
    if not text:
        return None
    # keep tab/newline/CR + printable ASCII (0x20-0x7E) + everything from 0xA0 up
    # (accents, emoji, NBSP…); drop C0 (incl. ESC), DEL (0x7F), and C1 (0x80-0x9F)
    # — all of which some terminals treat as control introducers.
    cleaned = "".join(
        c for c in text
        if c in "\t\n\r" or (0x20 <= ord(c) < 0x7f) or ord(c) >= 0xa0
    )
    return cleaned[:_MAX_PASTE_CHARS] or None


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


def bump_due(task: "Task", delta: int, today: date) -> None:
    """Move `task.due_date` `delta` days and write it back as ISO text.

    The base is the task's OWN date, or `today` when there is no readable
    one: an undated task and a corrupt stored string both parse to None
    (`parse_iso` leniency), and None means the bump starts from today —
    never from an invented epoch. Pure bar the one field write; the caller
    saves (the `set_task_phase` convention)."""
    base = parse_iso(task.due_date) or today
    task.due_date = (base + timedelta(days=delta)).isoformat()


def _extra_keys(d: dict, known: set[str]) -> dict:
    """Every key we don't model, kept verbatim so a load->save round-trip never
    drops data another (older/newer) version of the app wrote."""
    return {k: v for k, v in d.items() if k not in known}


_PROJECT_KEYS = {"id", "name", "color", "status", "archived", "pinned", "start_date",
                 "due_date", "extra"}
_TASK_KEYS = {"id", "title", "project_id", "phase", "blocked", "priority", "start_date",
              "due_date", "notes", "urls", "images", "archived", "pinned", "extra",
              "phase_changed", "depends_on",
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
    if color in PROJECT_COLORS:
        return color
    return DROPPED_PROJECT_COLORS.get(color, "violet")


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
        return cls(
            id=d.get("id") or _new_id(),
            name=d.get("name", "Untitled"),
            color=project_color_on_load(d.get("color")),
            status=d.get("status") if d.get("status") in PROJECT_STATUSES else "on_track",
            archived=bool(d.get("archived", False)),
            pinned=bool(d.get("pinned", False)),
            start_date=d.get("start_date"),
            due_date=d.get("due_date"),
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
            return cls(
                id=d.get("id") or _new_id(),
                title=d.get("title", "Untitled"),
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
            board = cls(*seed_data(), path=path)
            board.save()
            return board
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
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

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "phases": self.phases,
            "projects": [self._to_dict(p) for p in self.projects],
            "tasks": [self._to_dict(t) for t in self.tasks],
            "settings": self.settings,
        }
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

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

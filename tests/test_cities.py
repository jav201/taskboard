"""The world-city catalog for the ribbon clocks.

The catalog is DATA, and data that was typed from memory is data that is wrong
somewhere. These laws are the verification gate: every zone is resolved through
`zoneinfo` on the machine running the suite, every offset in current use has a
city, and nothing that a saved board might already name has been dropped.

The search laws exist because the catalog is bilingual by nature — the city is
spelled "São Paulo" and typed "Sao Paulo".
"""

import collections
import datetime
import unicodedata
import zoneinfo

from taskboard.models import (CITY_TO_ZONE, CITY_ZONES, DEFAULT_CLOCK1,
                              DEFAULT_CLOCK2, _LEGACY_ABBREV_TO_CITY, city_names,
                              resolve_city)

# Every display name the catalog shipped with before it was widened. A name that
# vanishes is not cosmetic: `get_clocks` validates against the catalog, so a user
# whose clock is set to a dropped city is silently reset to the default.
SHIPPED = (
    "Mexico City", "Monterrey", "Guadalajara", "Guatemala City", "San José",
    "Panama", "Bogotá", "Quito", "Lima", "Caracas", "Santiago", "Buenos Aires",
    "Montevideo", "São Paulo", "New York", "Boston", "Miami", "Atlanta",
    "Toronto", "Chicago", "Denver", "Phoenix", "Los Angeles", "San Francisco",
    "Seattle", "Vancouver", "Anchorage", "Honolulu", "London", "Dublin",
    "Lisbon", "Madrid", "Paris", "Brussels", "Amsterdam", "Berlin", "Zurich",
    "Rome", "Vienna", "Prague", "Warsaw", "Copenhagen", "Oslo", "Stockholm",
    "Helsinki", "Athens", "Moscow", "Istanbul", "Tel Aviv", "Dubai", "Riyadh",
    "Tehran", "Cairo", "Casablanca", "Lagos", "Accra", "Nairobi", "Johannesburg",
    "Karachi", "Mumbai", "Delhi", "Bangkok", "Jakarta", "Singapore", "Hong Kong",
    "Shanghai", "Taipei", "Manila", "Seoul", "Tokyo", "Perth", "Brisbane",
    "Sydney", "Melbourne", "Auckland",
)

WINTER = datetime.datetime(2026, 1, 15, 12)
SUMMER = datetime.datetime(2026, 7, 15, 12)


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s.strip().lower())
                   if not unicodedata.combining(c))


def offsets_of(zone: str) -> set[float]:
    """The UTC offsets a zone actually uses across the year (so a DST zone
    contributes both of its offsets)."""
    return {probe.replace(tzinfo=zoneinfo.ZoneInfo(zone)).utcoffset().total_seconds() / 3600
            for probe in (WINTER, SUMMER)}


# --------------------------------------------------------------------------- #
# the catalog is real
# --------------------------------------------------------------------------- #
def test_every_zone_in_the_catalog_resolves():
    """THE gate. A zone string that does not exist raises the moment a user
    picks that city, and it would ship green without this."""
    available = zoneinfo.available_timezones()
    for name, zone in CITY_ZONES:
        assert zone in available, f"{name}: {zone!r} is not an IANA zone here"
        zoneinfo.ZoneInfo(zone)          # constructs, or raises


def test_every_city_can_actually_tell_the_time():
    """End to end: the thing the ribbon does with a city, done for all of them."""
    for name, zone in CITY_ZONES:
        stamp = SUMMER.replace(tzinfo=zoneinfo.ZoneInfo(zone))
        assert stamp.utcoffset() is not None, name
        assert stamp.strftime("%H:%M")


def test_display_names_are_unique():
    dupes = [n for n, k in collections.Counter(city_names()).items() if k > 1]
    assert dupes == [], f"duplicate city names: {dupes}"


def test_no_two_cities_collide_once_accents_are_stripped():
    """This is what makes the accent-blind search SAFE. "San José" (Costa Rica)
    and "San Jose" (California) fold to the same key, so the Californian is
    listed as "San Jose (CA)" — without this law a future addition could make
    the search silently resolve to the wrong continent."""
    folded = collections.Counter(fold(n) for n in city_names())
    collisions = [k for k, v in folded.items() if v > 1]
    assert collisions == [], f"names that fold together: {collisions}"


def test_the_catalog_is_big_enough_to_be_worth_searching():
    assert len(CITY_ZONES) >= 300
    assert len(set(CITY_TO_ZONE.values())) >= 200


# --------------------------------------------------------------------------- #
# coverage: the reason the catalog was widened
# --------------------------------------------------------------------------- #
def test_every_utc_offset_in_use_anywhere_has_a_city():
    """The complaint this increment answers: "a veces busco una ciudad y no está
    y debo buscar por otro lado qué ciudades se alinean". Whatever offset a
    counterpart is on — including the half- and quarter-hour ones (India +5:30,
    Nepal +5:45, Newfoundland -3:30, Chatham +12:45, Eucla +8:45) — some city in
    this catalog is on it. Computed from the installed tzdata, not assumed."""
    world = set()
    for zone in zoneinfo.available_timezones():
        try:
            world |= offsets_of(zone)
        except Exception:                # a zone this platform cannot build
            continue
    covered = set()
    for _name, zone in CITY_ZONES:
        covered |= offsets_of(zone)
    assert not (world - covered), f"no city on offset(s): {sorted(world - covered)}"


def test_the_awkward_offsets_are_named_explicitly():
    """The ones a user cannot find by guessing a big city."""
    by_offset = collections.defaultdict(set)
    for name, zone in CITY_ZONES:
        for off in offsets_of(zone):
            by_offset[off].add(name)
    for off in (5.5, 5.75, -3.5, 12.75, 8.75, 4.5, 6.5, 9.5, -9.5):
        assert by_offset[off], f"nothing on UTC{off:+}"


# --------------------------------------------------------------------------- #
# nothing that already worked stopped working
# --------------------------------------------------------------------------- #
def test_no_shipped_city_was_dropped():
    have = set(city_names())
    missing = [n for n in SHIPPED if n not in have]
    assert missing == [], f"boards may already name these: {missing}"


def test_the_legacy_abbreviation_migration_still_points_at_real_cities():
    for abbrev, city in _LEGACY_ABBREV_TO_CITY.items():
        assert city in CITY_TO_ZONE, f"{abbrev} migrates to a city that is gone: {city}"


def test_the_defaults_are_still_in_the_catalog():
    assert DEFAULT_CLOCK1 in CITY_TO_ZONE
    assert DEFAULT_CLOCK2 in CITY_TO_ZONE


# --------------------------------------------------------------------------- #
# the search
# --------------------------------------------------------------------------- #
def test_exact_and_case_insensitive_matching_is_unchanged():
    assert resolve_city("Mexico City") == "Mexico City"
    assert resolve_city("mexico city") == "Mexico City"
    assert resolve_city("  TOKYO  ") == "Tokyo"
    assert resolve_city("São Paulo") == "São Paulo"
    assert resolve_city("são paulo") == "São Paulo"
    assert resolve_city("Atlantis") is None
    assert resolve_city("") is None
    assert resolve_city(None) is None


def test_an_ascii_keyboard_finds_an_accented_city():
    """The actual pain: he types what his keyboard gives him."""
    assert resolve_city("Sao Paulo") == "São Paulo"
    assert resolve_city("sao paulo") == "São Paulo"
    assert resolve_city("Bogota") == "Bogotá"
    assert resolve_city("Asuncion") == "Asunción"
    assert resolve_city("Reykjavik") == "Reykjavík"
    assert resolve_city("Zurich") == "Zurich"          # already ASCII, unchanged
    assert resolve_city("Dusseldorf") == "Düsseldorf"
    assert resolve_city("Malmo") is None               # still not a city we list


def test_an_exact_match_always_beats_the_accent_blind_one():
    """"San Jose" is a real, distinct entry, so it must resolve to itself and
    NOT be folded into "San José". Exactness first is what keeps the fallback
    from ever taking something away."""
    assert resolve_city("San José") == "San José"
    assert resolve_city("San Jose (CA)") == "San Jose (CA)"
    assert resolve_city("san jose (ca)") == "San Jose (CA)"


def test_every_catalog_name_resolves_to_itself():
    """No entry is unreachable by typing its own name."""
    for name in city_names():
        assert resolve_city(name) == name
        assert resolve_city(name.lower()) == name
        assert resolve_city(fold(name)) is not None

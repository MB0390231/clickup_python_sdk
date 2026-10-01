"""
Date helpers for ClickUp task dates (due_date / start_date).

ClickUp stores task dates as Unix timestamps in milliseconds, paired with a
``*_date_time`` boolean that says whether the time part is meaningful. A date-only
value is still a timestamp: the ClickUp UI stores it at 4:00 AM in the user's
timezone (e.g. a date-only due date of 2026-10-07 for an America/Chicago user is
2026-10-07T09:00:00Z with ``due_date_time`` false). These helpers follow the same
convention, so a date set through the API looks the same as one set in the UI.

Example:
    from clickup_python_sdk.dates import date_fields
    task.update(**date_fields("due", "2026-10-07", tz="America/Chicago"))
    # -> due_date=1791363600000, due_date_time=False
"""

import datetime as _dt
import re

# The hour ClickUp's UI uses for date-only values, in the user's timezone.
DATE_ONLY_HOUR = 4

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATETIME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[T ](\d{1,2}):(\d{2})$")


def _zone(tz):
    """Resolve ``tz`` (IANA name, tzinfo, or None for UTC) to a tzinfo."""
    if tz is None:
        return _dt.timezone.utc
    if isinstance(tz, _dt.tzinfo):
        return tz
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
    except ImportError as e:  # pragma: no cover
        raise ValueError("timezone names need Python 3.9+ (zoneinfo); pass a tzinfo") from e
    try:
        return ZoneInfo(str(tz))
    except Exception as e:
        raise ValueError(f"unknown timezone {tz!r}") from e


def to_timestamp(value, tz=None):
    """
    Convert a date or date-time to a ClickUp timestamp.

    Args:
        value: One of
            - ``"YYYY-MM-DD"`` or a ``datetime.date``: date only (stored at 4:00 AM local);
            - ``"YYYY-MM-DDTHH:MM"`` / ``"YYYY-MM-DD HH:MM"`` or a naive ``datetime``:
              wall-clock time in ``tz``;
            - an aware ``datetime``: used as is (``tz`` ignored).
        tz: IANA timezone name (e.g. ``"America/Chicago"``) or tzinfo. Defaults to UTC.

    Returns:
        tuple: ``(milliseconds, has_time)``.

    Raises:
        ValueError: If the value or timezone can't be parsed.
    """
    zone = _zone(tz)
    has_time = True

    if isinstance(value, _dt.datetime):
        moment = value if value.tzinfo is not None else value.replace(tzinfo=zone)
    elif isinstance(value, _dt.date):
        moment = _dt.datetime(value.year, value.month, value.day, DATE_ONLY_HOUR, tzinfo=zone)
        has_time = False
    elif isinstance(value, str):
        text = value.strip()
        m = _DATETIME_RE.match(text)
        try:
            if _DATE_RE.match(text):
                day = _dt.date.fromisoformat(text)
                moment = _dt.datetime(day.year, day.month, day.day, DATE_ONLY_HOUR, tzinfo=zone)
                has_time = False
            elif m:
                day = _dt.date.fromisoformat(m.group(1))
                moment = _dt.datetime(day.year, day.month, day.day, int(m.group(2)),
                                      int(m.group(3)), tzinfo=zone)
            else:
                raise ValueError
        except ValueError:
            raise ValueError(
                f"not a date: {value!r} (use YYYY-MM-DD or YYYY-MM-DDTHH:MM)"
            ) from None
    else:
        raise ValueError(f"not a date: {value!r}")

    return int(moment.timestamp() * 1000), has_time


def from_timestamp(ms, tz=None):
    """
    Convert a ClickUp timestamp (int or numeric string, milliseconds) to an aware datetime.

    Returns None for a missing value (None or "").
    """
    if ms is None or ms == "":
        return None
    return _dt.datetime.fromtimestamp(int(ms) / 1000, _zone(tz))


def format_timestamp(ms, tz=None, has_time=None):
    """
    Human-readable form of a ClickUp timestamp, e.g. ``"Wed 2026-10-07"`` or
    ``"Wed 2026-10-07 17:00 CDT"``.

    Args:
        ms: Timestamp in milliseconds (int or string), or None.
        tz: Timezone to display in (IANA name or tzinfo). Defaults to UTC.
        has_time: The task's ``*_date_time`` flag. When None (ClickUp often returns
            null for date-only values), a value at exactly 4:00 AM local is shown as
            date only.

    Returns:
        str or None.
    """
    moment = from_timestamp(ms, tz)
    if moment is None:
        return None
    if has_time is None:
        has_time = (moment.hour, moment.minute, moment.second) != (DATE_ONLY_HOUR, 0, 0)
    if not has_time:
        return moment.strftime("%a %Y-%m-%d")
    return moment.strftime("%a %Y-%m-%d %H:%M %Z").strip()


def date_fields(kind, value, tz=None):
    """
    Request-body fields for one task date.

    Args:
        kind: ``"due"`` or ``"start"``.
        value: Anything ``to_timestamp`` accepts, or None to clear the date.
        tz: Timezone for naive values.

    Returns:
        dict: e.g. ``{"due_date": 1791363600000, "due_date_time": False}``, or
        ``{"due_date": None}`` to clear (sent as JSON null, which removes the date).
    """
    if kind not in ("due", "start"):
        raise ValueError(f"kind must be 'due' or 'start' (got {kind!r})")
    if value is None:
        return {f"{kind}_date": None}
    ms, has_time = to_timestamp(value, tz)
    return {f"{kind}_date": ms, f"{kind}_date_time": has_time}

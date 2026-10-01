"""Unit tests for clickup_python_sdk.dates (no network). Run: python3 -m unittest discover tests"""

import datetime as dt
import unittest
from unittest import mock

from clickup_python_sdk.api import ClickupClient
from clickup_python_sdk.clickupobjects.task import Task
from clickup_python_sdk.dates import date_fields, format_timestamp, from_timestamp, to_timestamp

# 2026-10-07 04:00 America/Chicago (CDT, UTC-5) = 09:00Z — what the ClickUp UI stores for a
# date-only due date set by a Central user.
OCT7_DATE_ONLY_CHICAGO = 1791363600000


class ToTimestamp(unittest.TestCase):
    def test_date_only_string_is_4am_local(self):
        self.assertEqual(to_timestamp("2026-10-07", "America/Chicago"),
                         (OCT7_DATE_ONLY_CHICAGO, False))

    def test_date_object_matches_string(self):
        self.assertEqual(to_timestamp(dt.date(2026, 10, 7), "America/Chicago"),
                         (OCT7_DATE_ONLY_CHICAGO, False))

    def test_date_time_string_is_wall_clock_in_tz(self):
        ms, has_time = to_timestamp("2026-10-07T17:00", "America/Chicago")
        self.assertTrue(has_time)
        self.assertEqual(dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc),
                         dt.datetime(2026, 10, 7, 22, 0, tzinfo=dt.timezone.utc))

    def test_space_separator_accepted(self):
        self.assertEqual(to_timestamp("2026-10-07 17:00", "America/Chicago"),
                         to_timestamp("2026-10-07T17:00", "America/Chicago"))

    def test_winter_offset(self):
        # CST (UTC-6) after the DST change: 04:00 local = 10:00Z.
        ms, _ = to_timestamp("2026-12-01", "America/Chicago")
        self.assertEqual(dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).hour, 10)

    def test_default_tz_is_utc(self):
        ms, _ = to_timestamp("2026-10-07")
        self.assertEqual(dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc),
                         dt.datetime(2026, 10, 7, 4, 0, tzinfo=dt.timezone.utc))

    def test_aware_datetime_ignores_tz(self):
        moment = dt.datetime(2026, 10, 7, 9, 0, tzinfo=dt.timezone.utc)
        self.assertEqual(to_timestamp(moment, "Asia/Tokyo"), (OCT7_DATE_ONLY_CHICAGO, True))

    def test_bad_values(self):
        for bad in ["10/07/2026", "2026-13-01", "2026-10-07T25:00", "tomorrow", "", 5]:
            with self.assertRaises(ValueError, msg=repr(bad)):
                to_timestamp(bad, "America/Chicago")

    def test_bad_timezone(self):
        with self.assertRaises(ValueError):
            to_timestamp("2026-10-07", "Mars/Olympus")


class Formatting(unittest.TestCase):
    def test_round_trip_date_only(self):
        self.assertEqual(format_timestamp(OCT7_DATE_ONLY_CHICAGO, "America/Chicago"),
                         "Wed 2026-10-07")

    def test_string_ms_and_explicit_flag(self):
        self.assertEqual(format_timestamp(str(OCT7_DATE_ONLY_CHICAGO), "America/Chicago",
                                          has_time=True), "Wed 2026-10-07 04:00 CDT")

    def test_time_detected(self):
        ms, _ = to_timestamp("2026-10-07T17:00", "America/Chicago")
        self.assertEqual(format_timestamp(ms, "America/Chicago"), "Wed 2026-10-07 17:00 CDT")

    def test_missing(self):
        self.assertIsNone(format_timestamp(None))
        self.assertIsNone(from_timestamp(""))


class DateFields(unittest.TestCase):
    def test_due(self):
        self.assertEqual(date_fields("due", "2026-10-07", "America/Chicago"),
                         {"due_date": OCT7_DATE_ONLY_CHICAGO, "due_date_time": False})

    def test_start_with_time(self):
        fields = date_fields("start", "2026-10-07T17:00", "America/Chicago")
        self.assertEqual(set(fields), {"start_date", "start_date_time"})
        self.assertTrue(fields["start_date_time"])

    def test_clear(self):
        self.assertEqual(date_fields("due", None), {"due_date": None})

    def test_bad_kind(self):
        with self.assertRaises(ValueError):
            date_fields("end", "2026-10-07")


class TaskUpdateClear(unittest.TestCase):
    def _sent(self, **kwargs):
        api = mock.Mock()
        api.make_request.return_value = {"id": "abc"}
        with mock.patch.object(ClickupClient, "get_default_api", return_value=api):
            Task(id="abc").update(**kwargs)
        return api.make_request.call_args.kwargs["values"]

    def test_clear_due_sends_null(self):
        self.assertEqual(self._sent(clear_due_date=True), {"due_date": None})

    def test_clear_start_sends_null(self):
        self.assertEqual(self._sent(clear_start_date=True), {"start_date": None})

    def test_set_due_unchanged(self):
        self.assertEqual(self._sent(**date_fields("due", "2026-10-07", "America/Chicago")),
                         {"due_date": OCT7_DATE_ONLY_CHICAGO, "due_date_time": False})

    def test_set_and_clear_conflict(self):
        with self.assertRaises(ValueError):
            self._sent(due_date=OCT7_DATE_ONLY_CHICAGO, clear_due_date=True)


if __name__ == "__main__":
    unittest.main()

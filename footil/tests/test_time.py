from footil.time import minutes_to_hours, hours_to_days

from . import common


class TestDatetimeManipulation(common.TestFootilCommon):
    """Class to test datetime manipulation functions."""

    def test_01_minutes_to_hours(self):
        """Convert greater or equal one hour of minutes."""
        self.assertEqual(minutes_to_hours(90), (1, 30))
        self.assertEqual(minutes_to_hours(219), (3, 39))
        self.assertEqual(minutes_to_hours(60), (1, 0))

    def test_02_minutes_to_hours(self):
        """Convert over under one hour of minutes."""
        self.assertEqual(minutes_to_hours(30), (0, 30))
        self.assertEqual(minutes_to_hours(1), (0, 1))
        self.assertEqual(minutes_to_hours(0), (0, 0))

    def test_03_hours_to_days(self):
        """Convert greater or equal one days of hours."""
        self.assertEqual(hours_to_days(30), (1, 6))
        self.assertEqual(hours_to_days(48), (2, 0))
        self.assertEqual(hours_to_days(24), (1, 0))

    def test_04_hours_to_days(self):
        """Convert over under one day of hours."""
        self.assertEqual(hours_to_days(15), (0, 15))
        self.assertEqual(hours_to_days(1), (0, 1))
        self.assertEqual(hours_to_days(0), (0, 0))

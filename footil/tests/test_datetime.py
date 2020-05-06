from footil.datetime import to_datetime

import datetime

from . import common


class TestDatetimeManipulation(common.TestFootilCommon):
    """Class to test datetime manipulation functions."""

    def test_01_to_datetime(self):
        """Check with default format."""
        # valid
        try:
            dt = to_datetime('2020-01-01 01:05:20')
        except ValueError:
            self.fail(
                "Should not fail. '2020-01-01 01:05:20' fits default format.")
        self.assertEqual(type(dt), datetime.datetime)
        # invalid
        self.assertRaises(ValueError, to_datetime, '2020/01/01 01:05:20')

    def test_02_to_datetime(self):
        """Check with custom format."""
        # valid
        try:
            dt = to_datetime('2020-01 01:20', '%Y-%d %M:%H')
        except ValueError:
            self.fail("Should not fail. '2020-01 01:20' fits custom format.")
        self.assertEqual(type(dt), datetime.datetime)
        # invalid
        self.assertRaises(ValueError, to_datetime, '2020 01:20', '%Y-%d %M:%H')

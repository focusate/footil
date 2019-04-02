from footil.date import get_first_day_date, get_last_day_date

from . import common


class TestDateManipulation(common.TestFootilCommon):
    """Class to test date manipulation functions."""

    def test_get_first_day_date(self):
        """Get first day date for provided date."""
        res = get_first_day_date('1989-02-19')
        self.assertEqual(res, '1989-02-01')
        res = get_first_day_date('1989.02.19', fmt='%Y.%m.%d')
        self.assertEqual(res, '1989.02.01')
        # First day of the next month
        res = get_first_day_date('1989-02-19', months=1)
        self.assertEqual(res, '1989-03-01')
        res = get_first_day_date('1989-02-19', months=2)
        self.assertEqual(res, '1989-04-01')
        # First day of the last month
        res = get_first_day_date('1989-02-19', months=-1)
        self.assertEqual(res, '1989-01-01')
        res = get_first_day_date('1989-02-19', months=-2)
        self.assertEqual(res, '1988-12-01')

    def test_get_last_day_date(self):
        """Get last day date for provided date."""
        res = get_last_day_date('1989-02-19')
        self.assertEqual(res, '1989-02-28')
        res = get_last_day_date(
            '1989.02.19', fmt='%Y.%m.%d', new_fmt='%Y-%m-%d')
        self.assertEqual(res, '1989-02-28')
        # Last day of the next month
        res = get_last_day_date('1989-02-19', months=1)
        self.assertEqual(res, '1989-03-31')
        res = get_last_day_date('1989-02-19', months=2)
        self.assertEqual(res, '1989-04-30')
        # Last day of the last month
        res = get_last_day_date('1989-02-19', months=-1)
        self.assertEqual(res, '1989-01-31')
        res = get_last_day_date('1989-02-19', months=-2)
        self.assertEqual(res, '1988-12-31')

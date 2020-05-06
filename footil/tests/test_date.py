from footil.date import (
    get_first_day_date_str, get_last_day_date_str,
    get_first_day_date, get_last_day_date, DATE_FMT,
    to_date
)
import datetime

from . import common

DTTM = datetime.datetime


class TestDateManipulation(common.TestFootilCommon):
    """Class to test date manipulation functions."""

    def test_01_get_first_day_date(self):
        """Get first day date for provided date string."""
        res = get_first_day_date_str('1989-02-19')
        self.assertEqual(res, '1989-02-01')
        res = get_first_day_date_str('1989.02.19', fmt='%Y.%m.%d')
        self.assertEqual(res, '1989.02.01')
        # First day of the next month
        res = get_first_day_date_str('1989-02-19', months=1)
        self.assertEqual(res, '1989-03-01')
        res = get_first_day_date_str('1989-02-19', months=2)
        self.assertEqual(res, '1989-04-01')
        # First day of the last month
        res = get_first_day_date_str('1989-02-19', months=-1)
        self.assertEqual(res, '1989-01-01')
        res = get_first_day_date_str('1989-02-19', months=-2)
        self.assertEqual(res, '1988-12-01')
        # Test with datetime.date object, date object to return
        dt = DTTM.strptime('1989-02-19', DATE_FMT).date()
        res_dt = DTTM.strptime('1988-12-01', DATE_FMT).date()
        self.assertEqual(get_first_day_date(dt, months=-2), res_dt)
        # Test with datetime.date object, but other date format
        dt = DTTM.strptime('1989.02.19', '%Y.%m.%d').date()
        res_dt = DTTM.strptime('1989.02.01', '%Y.%m.%d').date()
        self.assertEqual(get_first_day_date(dt), res_dt)

    def test_02_get_last_day_date(self):
        """Get last day date for provided date."""
        res = get_last_day_date_str('1989-02-19')
        self.assertEqual(res, '1989-02-28')
        res = get_last_day_date_str(
            '1989.02.19', fmt='%Y.%m.%d', new_fmt='%Y-%m-%d')
        self.assertEqual(res, '1989-02-28')
        # Last day of the next month
        res = get_last_day_date_str('1989-02-19', months=1)
        self.assertEqual(res, '1989-03-31')
        res = get_last_day_date_str('1989-02-19', months=2)
        self.assertEqual(res, '1989-04-30')
        # Last day of the last month
        res = get_last_day_date_str('1989-02-19', months=-1)
        self.assertEqual(res, '1989-01-31')
        res = get_last_day_date_str('1989-02-19', months=-2)
        self.assertEqual(res, '1988-12-31')
        # Test with datetime.date object, date object to return
        dt = DTTM.strptime('1989-02-19', DATE_FMT).date()
        res_dt = DTTM.strptime('1988-12-31', DATE_FMT).date()
        self.assertEqual(get_last_day_date(dt, months=-2), res_dt)
        # Test with datetime.date object, but other date format
        dt = DTTM.strptime('1989.02.19', '%Y.%m.%d').date()
        res_dt = DTTM.strptime('1989.02.28', '%Y.%m.%d').date()
        self.assertEqual(get_last_day_date(dt), res_dt)

    def test_03_to_date(self):
        """Check when date string satisfies date format."""
        # default format
        try:
            to_date('2020-01-01')
        except ValueError:
            self.fail("Should not fail. '2020-01-01' fits default format.")
        # custom formats
        try:
            to_date('2020', '%Y')
        except ValueError:
            self.fail("Should not fail. '2020' fits given format.")
        try:
            to_date('2020/12', '%Y/%m')
        except ValueError:
            self.fail("Should not fail. '2020/12' fits given format.")
        # datetime
        try:
            dt = to_date('2020/12 15:20', '%Y/%m %M:%S')
        except ValueError:
            self.fail("Should not fail. '2020/12 15:20' fits given format.")
        self.assertEqual(type(dt), datetime.date)

    def test_04_to_date(self):
        """Check when date string does not satisfy date format."""
        # default format
        self.assertRaises(ValueError, to_date, '2020/01/01')
        # custom formats
        self.assertRaises(ValueError, to_date, '2020/01/01', '%Y')
        self.assertRaises(ValueError, to_date, '2020', '%Y/%m')
        # datetime
        self.assertRaises(ValueError, to_date, '2020 15:20', '%Y %m')

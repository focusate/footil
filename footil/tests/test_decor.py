import unittest

from footil import decor
from footil import log


def _dummy(): pass


def _dummy2(a, b, c='ctest'): pass


class _Dummy:

    def __init__(self, x):
        self.x = x

    dummy_attr = 'cls_attr'

    @classmethod
    def _dummy(cls, a, b, c='ctest'): pass

    def _dummy2(self, a, b, c='ctest'): pass


class TestDecor(unittest.TestCase):
    """Test class for decorators."""

    def test_time_it_msg_1(self):
        """Time it message in milliseconds."""
        t = decor.time_it(uom='ms')
        msg = t._get_message(_dummy, 1)
        self.assertEqual(msg, "'_dummy' took 1000.00 millisecond(s)")

    def test_time_it_msg_2(self):
        """Time it message in seconds."""
        t = decor.time_it()
        msg = t._get_message(_dummy, 1)
        self.assertEqual(msg, "'_dummy' took 1.00 second(s)")

    def test_time_it_msg_3(self):
        """Time it message in minutes."""
        t = decor.time_it(uom='m')
        msg = t._get_message(_dummy, 60)
        self.assertEqual(msg, "'_dummy' took 1.00 minute(s)")

    def test_time_it_msg_4(self):
        """Time it message in hours."""
        t = decor.time_it(uom='h')
        msg = t._get_message(_dummy, 1800)
        self.assertEqual(msg, "'_dummy' took 0.50 hour(s)")

    def test_time_it_msg_5(self):
        """Time it message with different message format."""
        t = decor.time_it(
            msg_fmt='{arg1} test1 {c} {_uom_name}')
        msg = t._get_message(
            _dummy, 1, args=('t1', 't2'), kwargs={'c': 'kwtest'})
        self.assertEqual(msg, "t2 test1 kwtest second(s)")
        t = decor.time_it(
            msg_fmt='{arg0} test2 {_uom_name}')
        msg = t._get_message(_dummy, 1, args=('t1', 't2'))
        self.assertEqual(msg, "t1 test2 second(s)")
        # Test with class method.
        t = decor.time_it(
            msg_fmt='{_f_name} {arg0.dummy_attr} {arg1} test2 {_uom_name}')
        msg = t._get_message(_Dummy._dummy, 1, args=('t1', 't2'))
        self.assertEqual(msg, "_dummy cls_attr t1 test2 second(s)")
        # Test with bound method.
        t = decor.time_it(
            msg_fmt='{arg0.x} {arg1} {_dur:.3f} {_uom_name}')
        msg = t._get_message(_Dummy(x='X')._dummy2, 1, args=('t1', 't2'))
        self.assertEqual(msg, "X t1 1.000 second(s)")
        t = decor.time_it(
            msg_fmt='test3 {_uom_name}')
        msg = t._get_message(_dummy, 1, args=('t1', 't2'))
        self.assertEqual(msg, "test3 second(s)")

    def test_time_it_1(self):
        """Run decorator and capture its print output."""
        d = decor.time_it(uom='h')(_dummy)
        res = log.capture_output(d)
        self.assertEqual(res, "'_dummy' took 0.00 hour(s)\n")
        d = decor.time_it(
            uom='h',
            msg_fmt="'{_f_name}' took {_dur:.2f} {_uom_name} {arg1} {c}")(
            _dummy2)
        res = log.capture_output(d, args=(0, 1), kwargs={'c': 2})
        self.assertEqual(res, "'_dummy2' took 0.00 hour(s) 1 2\n")

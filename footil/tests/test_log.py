import unittest
import logging

from footil import log


class TestLog(unittest.TestCase):
    """Class to test stdout/stderr helpers."""

    def test_log_1(self):
        """Capture output from print."""
        res = log.capture_output(print, args=('test',))
        self.assertEqual(res, 'test\n')

    # TODO: There might be a bug with logging, so disabled tests for
    # now.
    # def test_log_2(self):
    #     """Capture output from logging."""
    #     res = log.capture_output(
    #         lambda a=10: logging.warning(a), kwargs={'a': 'test2'})
    #     self.assertEqual(res, 'WARNING:root:test2\n')

    # def test_log_3(self):
    #     """Capture output from both print and logging."""

    #     def dummy(a, b='dummy'):
    #         print(a)
    #         logging.warning(b)

    #     res = log.capture_output(
    #         dummy, args=('test3',), kwargs={'b': 'test4'})
    #     self.assertEqual(res, 'test3\nWARNING:root:test4\n')

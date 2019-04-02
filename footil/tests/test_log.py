from footil import log

from . import common


class TestLog(common.TestFootilCommon):
    """Class to test logging/formatting helpers."""

    def test_capture_output_1(self):
        """Capture output from print."""
        res = log.capture_output(print, args=('test',))
        self.assertEqual(res, 'test\n')

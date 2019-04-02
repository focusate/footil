from footil import xtyping

from . import common


class TestXtyping(common.TestFootilCommon):
    """Class to test xtyping module."""

    def test_is_iterable_1(self):
        """Check int."""
        self.assertFalse(xtyping.is_iterable(1))

    def test_is_iterable_2(self):
        """Check float."""
        self.assertFalse(xtyping.is_iterable(1.0))

    def test_is_iterable_3(self):
        """Check str."""
        self.assertFalse(xtyping.is_iterable('abc'))

    def test_is_iterable_4(self):
        """Check list."""
        self.assertTrue(xtyping.is_iterable([1, 2]))

    def test_is_iterable_5(self):
        """Check tuple."""
        self.assertTrue(xtyping.is_iterable((1, 2)))

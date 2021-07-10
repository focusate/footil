from footil import xtyping

from . import common


class TestXtyping(common.TestFootilCommon):
    """Class to test xtyping module."""

    def test_01_is_iterable(self):
        """Check int."""
        self.assertFalse(xtyping.is_iterable(1))

    def test_02_is_iterable(self):
        """Check float."""
        self.assertFalse(xtyping.is_iterable(1.0))

    def test_03_is_iterable(self):
        """Check str."""
        self.assertFalse(xtyping.is_iterable('abc'))

    def test_04_is_iterable(self):
        """Check list."""
        self.assertTrue(xtyping.is_iterable([1, 2]))

    def test_05_is_iterable(self):
        """Check tuple."""
        self.assertTrue(xtyping.is_iterable((1, 2)))

    def test_06_bytes_to_str(self):
        """Convert bytes to string."""
        self.assertEqual(xtyping.bytes_to_str(b'123'), '123')

    def test_07_bytes_to_str(self):
        """Convert string to string."""
        self.assertEqual(xtyping.bytes_to_str('123', errors='replace'), '123')

    def test_08_str_to_bytes(self):
        """Convert string to bytes."""
        self.assertEqual(xtyping.str_to_bytes('123'), b'123')

    def test_09_str_to_bytes(self):
        """Convert bytes to bytes."""
        self.assertEqual(xtyping.str_to_bytes(
            b'123', encoding='utf-8'), b'123')

    def test_10_dict_to_namedtuple(self):
        """Convert dictionary to namedtuple."""
        obj = xtyping.dict_to_namedtuple("X1", {'a': 10, 'b': 20})
        self.assertEqual(obj.a, 10)
        self.assertEqual(obj.b, 20)

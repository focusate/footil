from footil import xdata

from .common import TestFootilCommon


class TestFormatting(TestFootilCommon):
    """Test cases for xdata module."""

    def test_01_pickle_copy(self):
        """Copy list."""
        lst = [[1, 2]]
        lst2 = xdata.pickle_copy(lst)
        self.assertEqual(lst, lst2)
        self.assertIsNot(lst, lst2)
        lst[0].append(3)
        self.assertEqual(lst2, [[1, 2]])

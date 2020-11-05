from footil.sorting import ReverseComparator

from . import common


def _unpack_objects(rc_list):
    return [rc.obj for rc in rc_list]


class TestSorting(common.TestFootilCommon):
    """Test cases for module sorting."""

    @classmethod
    def setUpClass(cls):
        """Set up data for sorting tests."""
        super().setUpClass()
        cls.RC = ReverseComparator
        cls.rc_list = [cls.RC(2), cls.RC(5), cls.RC(3)]

    def test_01_reverse_comparator(self):
        """Sort list with ReverseComparator objects. reverse=False."""
        rc_list_sorted = sorted(self.rc_list)
        self.assertEqual(_unpack_objects(rc_list_sorted), [5, 3, 2])

    def test_02_reverse_comparator(self):
        """Sort list with ReverseComparator objects. reverse=True."""
        rc_list_sorted = sorted(self.rc_list, reverse=True)
        self.assertEqual(_unpack_objects(rc_list_sorted), [2, 3, 5])

from footil.xiter import iterate_limit

from . import common


def _iter_to_list(iterable):
    return [i for i in iterable]


class TestXiter(common.TestFootilCommon):
    """Test class for xiter module."""

    @property
    def _list_1(self):
        return [1, 10, 5, 20]

    @property
    def _iter_list_1(self):
        return iter(self._list_1)

    def test_01_iterate_limit(self):
        """Iterate all items."""
        self.assertEqual(
            _iter_to_list(iterate_limit(self._iter_list_1)), self._list_1
        )

    def test_02_iterate_limit(self):
        """Iterate less items than list has."""
        self.assertEqual(
            _iter_to_list(iterate_limit(self._iter_list_1, limit=2)),
            [1, 10]
        )

    def test_03_iterate_limit(self):
        """Iterate more items than list has."""
        self.assertEqual(
            _iter_to_list(iterate_limit(self._iter_list_1, limit=10)),
            self._list_1
        )

    def test_04_iterate_limit(self):
        """Iterate 0 items."""
        with self.assertRaises(StopIteration):
            # Force to iterate one more, when 0 iterations was
            # requested.
            next(iterate_limit(self._iter_list_1, limit=0))

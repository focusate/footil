from footil.xcollections import batch, to_intervals

from . import common

SEQUENCE_1 = [1, 2, 3, 4, 5]


class TestCollections(common.TestFootilCommon):
    """Common class for collections module tests."""

    def test_01_batch(self):
        """Check batches: sequence length < batch size."""
        self.assertEqual(list(batch(SEQUENCE_1, 6)), [SEQUENCE_1])

    def test_02_batch(self):
        """Check batches: sequence length > batch size (2 batches)."""
        self.assertEqual(list(batch(SEQUENCE_1, 3)), [[1, 2, 3], [4, 5]])

    def test_03_batch(self):
        """Check batches: sequence length > batch size (5 batches)."""
        self.assertEqual(list(batch(SEQUENCE_1, 1)), [[1], [2], [3], [4], [5]])

    def test_04_to_intervals(self):
        """Interval unsorted, with dupes [2, 1, 2, 4]."""
        self.assertEqual(
            to_intervals([2, 1, 2, 4], no_dupes=False, sort=False),
            [(2, 1), (1, 2), (2, 4)],
        )

    def test_05_to_intervals(self):
        """Interval unsorted, without dupes [2, 1, 2, 4]."""
        self.assertEqual(
            to_intervals([2, 1, 2, 4], no_dupes=True, sort=False),
            [(2, 1), (1, 4)],
        )

    def test_06_to_intervals(self):
        """Interval sorted, with dupes [2, 1, 2, 4]."""
        self.assertEqual(
            to_intervals([2, 1, 2, 4], no_dupes=False, sort=True),
            [(1, 2), (2, 2), (2, 4)],
        )

    def test_07_to_intervals(self):
        """Interval sorted, without dupes [2, 1, 2, 4]."""
        self.assertEqual(
            to_intervals([2, 1, 2, 4], no_dupes=True, sort=True),
            [(1, 2), (2, 4)],
        )

    def test_08_to_intervals(self):
        """Interval incorrect sequence.

        Case 1: no items in sequence.
        Case 2: one item in sequence only.
        """
        # Case 1.
        self.assertEqual(to_intervals([]), [])
        # Case 2.
        self.assertEqual(to_intervals([2]), [])

    def test_09_to_intervals(self):
        """Interval sorted with key ['1B', '2A', '1C', '1C'].

        Case 1: reverse=False
        Case 2: reverse=True
        """
        # Case 1.
        self.assertEqual(
            to_intervals(
                ['1B', '2A', '1C'],
                no_dupes=True,
                sort=True,
                reverse=False,
                # Sort by letters.
                key=lambda i: i[1]
            ),
            [('2A', '1B'), ('1B', '1C')],
        )
        # Case 2.
        self.assertEqual(
            to_intervals(
                ['1B', '2A', '1C'],
                no_dupes=True,
                sort=True,
                reverse=True,
                # Sort by letters.
                key=lambda i: i[1]
            ),
            [('1C', '1B'), ('1B', '2A')],
        )

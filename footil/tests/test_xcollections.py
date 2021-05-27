from footil import xcollections

from . import common

SEQUENCE_1 = [1, 2, 3, 4, 5]


class TestCollections(common.TestFootilCommon):
    """Common class for collections module tests."""

    def test_01_batch(self):
        """Check batches: sequence length < batch size."""
        self.assertEqual(list(xcollections.batch(SEQUENCE_1, 6)), [SEQUENCE_1])

    def test_02_batch(self):
        """Check batches: sequence length > batch size (2 batches)."""
        self.assertEqual(
            list(xcollections.batch(SEQUENCE_1, 3)), [[1, 2, 3], [4, 5]]
        )

    def test_03_batch(self):
        """Check batches: sequence length > batch size (5 batches)."""
        self.assertEqual(
            list(xcollections.batch(SEQUENCE_1, 1)), [[1], [2], [3], [4], [5]]
        )

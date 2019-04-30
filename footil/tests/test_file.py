from . import common
from footil import file


class TestFile(common.TestFootilCommon):
    """Test cases for module xos."""

    @classmethod
    def setUpClass(cls):
        """Set up data for file module tests."""
        super(TestFile, cls).setUpClass()
        cls.data = 'test1234'

    def test_written_named_temporary_file_1(self):
        """Create temp file with data written on it.

        File is kept open and without changing stream position.
        """
        f = file.WrittenNamedTemporaryFile(self.data, mode='w+t', delete=False)
        self.assertFalse(f.closed)
        self.assertEqual(f.read(), '')

    def test_written_named_temporary_file_2(self):
        """Create temp file with data written on it.

        File steam position is set to start.
        """
        f = file.WrittenNamedTemporaryFile(
            self.data, mode='w+t', delete=False, seek=0)
        self.assertFalse(f.closed)
        self.assertEqual(f.read(), self.data)

    def test_written_named_temporary_file_3(self):
        """Create temp file with data written on it.

        File is closed.
        """
        f = file.WrittenNamedTemporaryFile(
            self.data, mode='w+t', delete=False, close=True)
        self.assertTrue(f.closed)
        f = open(f.name)
        self.assertEqual(f.read(), self.data)

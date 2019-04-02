from . import common
from footil import path
import os


class TestXos(common.TestFootilCommon):
    """Test cases for module xos."""

    @classmethod
    def setUpClass(cls):
        """Set up data for xos module tests."""
        super(TestXos, cls).setUpClass()
        cls.cfd = path.get_cfp(fdir=True)

    def test_get_cfp(self):
        """Check current file directory."""
        self.assertTrue(self.cfd.endswith('/footil/footil/tests'))

    def test_chdir_tmp(self):
        """Change current working directory and then change it back."""
        with path.chdir_tmp(self.cfd):
            self.assertTrue(os.getcwd().endswith('/footil/footil/tests'))
        self.assertTrue(os.getcwd().endswith('/footil'))

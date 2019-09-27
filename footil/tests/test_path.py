import unittest
import doctest
import os
from footil import path

from . import common


class TestPath(common.TestFootilCommon):
    """Test cases for module xos."""

    @classmethod
    def setUpClass(cls):
        """Set up data for path module tests."""
        super(TestPath, cls).setUpClass()
        cls.cfd = path.get_cfp(fdir=True)

    def test_01_get_cfp(self):
        """Check current file directory."""
        self.assertTrue(self.cfd.endswith('/footil/footil/tests'))

    def test_02_chdir_tmp(self):
        """Change current working directory and then change it back."""
        with path.chdir_tmp(self.cfd):
            self.assertTrue(os.getcwd().endswith('/footil/footil/tests'))
        self.assertTrue(os.getcwd().endswith('/footil'))


# Add to run doctest alongside unittests.
testSuite = unittest.TestSuite()
testSuite.addTests(unittest.makeSuite(TestPath))
testSuite.addTest(doctest.DocTestSuite(path))
unittest.TextTestRunner(verbosity=2).run(testSuite)

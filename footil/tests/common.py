import unittest


class Dummy(object):
    """Dummy class to create object with various attributes."""

    def __init__(self, **kwargs):
        """Set up attributes."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestFootilCommon(unittest.TestCase):
    """Common class for all test classes.."""

    @classmethod
    def setUpClass(cls):
        """Set up data for all test classes."""
        super(TestFootilCommon, cls).setUpClass()
        cls.dummy_lst = [
            'traceback:\n', 'something_went_wrong\n', 'some_error\n']

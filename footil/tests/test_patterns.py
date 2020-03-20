from . import common
from footil import patterns, log


def _dummy_func(s):
    print(s, end='')


class TestPatterns(common.TestFootilCommon):
    """Test cases for module xos."""

    @classmethod
    def setUpClass(cls):
        """Set up data for design pattern tests."""
        super().setUpClass()
        cls.DequeInvoker = patterns.DequeInvoker
        MethodCommand = patterns.MethodCommand
        cls.mc1 = MethodCommand(_dummy_func, args=('a',))
        cls.mc2 = MethodCommand(_dummy_func, args=('b',))
        cls.mc3 = MethodCommand(_dummy_func, args=('c',))

    def test_01_command(self):
        """Execute commands in fifo order."""
        invoker = self.DequeInvoker()
        invoker.add_command(self.mc1)
        invoker.add_command(self.mc2)
        invoker.add_command(self.mc3)
        res = log.capture_output(invoker.run)
        self.assertEqual(res, 'abc')

    def test_02_command(self):
        """Execute commands in lifo order."""
        invoker = self.DequeInvoker()
        invoker.add_command(self.mc1)
        invoker.add_command(self.mc2)
        invoker.add_command(self.mc3)
        res = log.capture_output(invoker.run, kwargs={'priority': 'lifo'})
        self.assertEqual(res, 'cba')

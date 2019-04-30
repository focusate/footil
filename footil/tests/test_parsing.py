from footil import parsing

from .common import TestFootilCommon


class TestParsing(TestFootilCommon):
    """Test cases for parsing module."""

    def test_eval_limited_1(self):
        """Eval with no context."""
        res = parsing.eval_limited('1')
        self.assertEqual(res, 1)

    def test_eval_limited_2(self):
        """Eval with some builtins only."""
        res = parsing.eval_limited(
            'len([1, 2])', {'included_builtins': ['len']})
        self.assertEqual(res, 2)
        # excluded_builtins takes priority over excluded_builtins.
        res = parsing.eval_limited(
            'len([1, 2])',
            {
                'excluded_builtins': ['zip'],
                'included_builtins': ['abs']
            }
        )
        self.assertEqual(res, 2)
        res = parsing.eval_limited(
            'len([1, 2])', {'excluded_builtins': ['zip']}
        )
        self.assertEqual(res, 2)
        with self.assertRaises(NameError):
            parsing.eval_limited(
                'len([1, 2])', {'included_builtins': ['abs']})
        with self.assertRaises(NameError):
            parsing.eval_limited(
                'len([1, 2])',
                {
                    'excluded_builtins': ['len'],
                    'included_builtins': ['abs']
                }
            )

    def test_eval_limited_3(self):
        """Eval with builtins, independent globals and locals."""
        global_x = 'x1'
        local_x = 'x2'
        not_included_x = 'x3'  # noqa
        res = parsing.eval_limited(
            'len([x1, x2])',
            {
                'included_builtins': ['len'],
                'globals': {'x1': global_x},
                'locals': {'x2': local_x}
            }
        )
        self.assertEqual(res, 2)
        with self.assertRaises(NameError):
            parsing.eval_limited(
                'len([x1, x2, not_included_x])',
                {
                    'included_builtins': ['len'],
                    'globals': {'x1': global_x},
                    'locals': {'x2': local_x}
                }
            )
        # Use all_builtins flag to have all builtins, so
        # excluded_builtins would be ignored.
        res = parsing.eval_limited(
            'len([1, 2, 3])',
            {
                'all_builtins': True,
                'excluded_builtins': ['len'],
            }
        )
        self.assertEqual(res, 3)

    def test_exec_limited_1(self):
        """Execute source with included variable in locals."""
        x = 10
        _locals = {'x': x}
        parsing.exec_limited(
            'x += 5', {'locals': _locals, 'all_builtins': True})
        self.assertEqual(_locals['x'], 15)

    def test_exec_limited_2(self):
        """Execute source with included variable in globals.

        Case 1: locals use globals.
        Case 2: use explicit locals, so modifications would not
        persist.
        """
        x = 10
        _globals = {'x': x}
        parsing.exec_limited(
            'x += 5', {'globals': _globals, 'all_builtins': True})
        self.assertEqual(_globals['x'], 15)
        parsing.exec_limited(
            'x += 5',
            {'globals': _globals, 'locals': {}, 'all_builtins': True})
        # Value should not change, because locals is not None, meaning
        # x from globals won't persist.
        self.assertEqual(_globals['x'], 15)

    def test_exec_limited_3(self):
        """Execute source with not included variable."""
        with self.assertRaises(NameError):
            parsing.exec_limited('x += 5')

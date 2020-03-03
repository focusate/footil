from footil import decor, log
from . import common


def _func1(a, b, c):
    pass


def _func2(a=5, b=10):
    pass


def _func3(a, b, c=5, d=10):
    pass


def _func4(a, b, *args):
    pass


def _func5(a, b, *args, c=5):
    pass


def _func6(a, b, c=5, **kwargs):
    pass


def _func7(a, b, *args, c=5, **kwargs):
    pass


def _func8(*args):
    pass


def _func9(**kwargs):
    pass


def _func10(*args, **kwargs):
    pass


def _func11(*args, **kwargs):
    return '123'


def _func_exception():
    raise TypeError("Some Type Error")


def _dummy(): pass


def _dummy2(a, b, c='ctest'): pass


class _Dummy:

    def __init__(self, x):
        self.x = x

    dummy_attr = 'cls_attr'

    @classmethod
    def _dummy(cls, a, b, c='ctest'): pass

    def _dummy2(self, a, b, c='ctest'): pass


class TestDecor(common.TestFootilCommon):
    """Test class for decorators."""

    def test_01_time_it_msg(self):
        """Time it message in milliseconds."""
        t = decor.time_it(uom='ms')
        msg = t._get_message(_dummy, 1)
        self.assertEqual(msg, "'_dummy' took 1000.00 millisecond(s)")

    def test_02_time_it_msg(self):
        """Time it message in seconds."""
        t = decor.time_it()
        msg = t._get_message(_dummy, 1)
        self.assertEqual(msg, "'_dummy' took 1.00 second(s)")

    def test_03_time_it_msg(self):
        """Time it message in minutes."""
        t = decor.time_it(uom='m')
        msg = t._get_message(_dummy, 60)
        self.assertEqual(msg, "'_dummy' took 1.00 minute(s)")

    def test_04_time_it_msg(self):
        """Time it message in hours."""
        t = decor.time_it(uom='h')
        msg = t._get_message(_dummy, 1800)
        self.assertEqual(msg, "'_dummy' took 0.50 hour(s)")

    def test_05_time_it_msg(self):
        """Time it message with different message format."""
        t = decor.time_it(
            msg_fmt='{arg1} test1 {c} {_uom_name}')
        msg = t._get_message(
            _dummy, 1, args=('t1', 't2'), kwargs={'c': 'kwtest'})
        self.assertEqual(msg, "t2 test1 kwtest second(s)")
        t = decor.time_it(
            msg_fmt='{arg0} test2 {_uom_name}')
        msg = t._get_message(_dummy, 1, args=('t1', 't2'))
        self.assertEqual(msg, "t1 test2 second(s)")
        # Test with class method.
        t = decor.time_it(
            msg_fmt='{_f_name} {arg0.dummy_attr} {arg1} test2 {_uom_name}')
        msg = t._get_message(_Dummy._dummy, 1, args=('t1', 't2'))
        self.assertEqual(msg, "_dummy cls_attr t1 test2 second(s)")
        # Test with bound method.
        t = decor.time_it(
            msg_fmt='{arg0.x} {arg1} {_dur:.3f} {_uom_name}')
        msg = t._get_message(_Dummy(x='X')._dummy2, 1, args=('t1', 't2'))
        self.assertEqual(msg, "X t1 1.000 second(s)")
        t = decor.time_it(
            msg_fmt='test3 {_uom_name}')
        msg = t._get_message(_dummy, 1, args=('t1', 't2'))
        self.assertEqual(msg, "test3 second(s)")

    def test_06_time_it(self):
        """Run decorator and capture its print output."""
        d = decor.time_it(uom='h')(_dummy)
        res = log.capture_output(d)
        self.assertEqual(res, "'_dummy' took 0.00 hour(s)\n")
        d = decor.time_it(
            uom='h',
            msg_fmt="'{_f_name}' took {_dur:.2f} {_uom_name} {arg1} {c}")(
            _dummy2)
        res = log.capture_output(d, args=(0, 1), kwargs={'c': 2})
        self.assertEqual(res, "'_dummy2' took 0.00 hour(s) 1 2\n")

    def _func11(self, a, b=5):
        pass

    def test_07_args_kwargs_map_func1(self):
        """Map func1 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func1, 1, 2, 3)
        self.assertEqual(res, {'args': (1, 2, 3), 'kwargs': {}})

    def test_08_args_kwargs_map_func2(self):
        """Map func2 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func2, a=5, b=10)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 5, 'b': 10}})
        res = decor.catch_exceptions._map_args_kwargs(_func2, a=6, b=7)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 6, 'b': 7}})
        res = decor.catch_exceptions._map_args_kwargs(_func2, 6, b=7)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 6, 'b': 7}})
        res = decor.catch_exceptions._map_args_kwargs(_func2, 6, 7)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 6, 'b': 7}})
        res = decor.catch_exceptions._map_args_kwargs(_func2, b=9, a=10)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 10, 'b': 9}})
        res = decor.catch_exceptions._map_args_kwargs(_func2, a=5, b=9)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 5, 'b': 9}})

    def test_09_args_kwargs_map_func3(self):
        """Map func3 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func3, 1, 2, c=5, d=10)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 5, 'd': 10}})
        res = decor.catch_exceptions._map_args_kwargs(_func3, 1, 2, c=6, d=10)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 6, 'd': 10}})
        res = decor.catch_exceptions._map_args_kwargs(_func3, 1, 2, c=6, d=9)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 6, 'd': 9}})
        res = decor.catch_exceptions._map_args_kwargs(_func3, 1, 2, 3, d=9)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 3, 'd': 9}})
        res = decor.catch_exceptions._map_args_kwargs(_func3, 1, 2, 3, 4)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 3, 'd': 4}})

    def test_10_args_kwargs_map_func4(self):
        """Map func4 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func4, 1, 2)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {}})
        res = decor.catch_exceptions._map_args_kwargs(_func4, 1, 2, 3)
        self.assertEqual(res, {'args': (1, 2, 3), 'kwargs': {}})
        res = decor.catch_exceptions._map_args_kwargs(_func4, 1, 2, 3, 4)
        self.assertEqual(res, {'args': (1, 2, 3, 4), 'kwargs': {}})

    def test_11_args_kwargs_map_func5(self):
        """Map func5 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func5, 1, 2, c=5)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func5, 1, 2, 3, c=5)
        self.assertEqual(res, {'args': (1, 2, 3), 'kwargs': {'c': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func5, 1, 2, 3, 4, c=5)
        self.assertEqual(res, {'args': (1, 2, 3, 4), 'kwargs': {'c': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func5, 1, 2, 3, c=6)
        self.assertEqual(res, {'args': (1, 2, 3), 'kwargs': {'c': 6}})

    def test_12_args_kwargs_map_func6(self):
        """Map func6 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func6, 1, 2, c=5)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func6, 1, 2, 3)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 3}})
        res = decor.catch_exceptions._map_args_kwargs(_func6, 1, 2, 3, d=5)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 3, 'd': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func6, 1, 2, c=5, d=10)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 5, 'd': 10}})

    def test_13_args_kwargs_map_func7(self):
        """Map func7 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func7, 1, 2, c=5)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'c': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func7, 1, 2, 3, c=5)
        self.assertEqual(res, {'args': (1, 2, 3), 'kwargs': {'c': 5}})
        res = decor.catch_exceptions._map_args_kwargs(
            _func7, 1, 2, 3, c=5, d=6)
        self.assertEqual(
            res, {'args': (1, 2, 3), 'kwargs': {'c': 5, 'd': 6}})

    def test_14_args_kwargs_map_func8(self):
        """Map func8 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func8, 1, 2)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {}})
        res = decor.catch_exceptions._map_args_kwargs(_func8, 1)
        self.assertEqual(res, {'args': (1,), 'kwargs': {}})
        res = decor.catch_exceptions._map_args_kwargs(_func8)
        self.assertEqual(res, {'args': (), 'kwargs': {}})

    def test_15_args_kwargs_map_func9(self):
        """Map func9 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func9, a=5, b=10)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 5, 'b': 10}})
        res = decor.catch_exceptions._map_args_kwargs(_func9, a=5)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func9)
        self.assertEqual(res, {'args': (), 'kwargs': {}})

    def test_16_args_kwargs_map_func10(self):
        """Map func10 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(_func10)
        self.assertEqual(res, {'args': (), 'kwargs': {}})
        res = decor.catch_exceptions._map_args_kwargs(_func10, 1)
        self.assertEqual(res, {'args': (1,), 'kwargs': {}})
        res = decor.catch_exceptions._map_args_kwargs(_func10, a=5)
        self.assertEqual(res, {'args': (), 'kwargs': {'a': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func10, 1, a=5)
        self.assertEqual(res, {'args': (1,), 'kwargs': {'a': 5}})
        res = decor.catch_exceptions._map_args_kwargs(_func10, 1, 2, a=5, b=10)
        self.assertEqual(res, {'args': (1, 2), 'kwargs': {'a': 5, 'b': 10}})

    def test_17_args_kwargs_map_func11(self):
        """Map func11 args/kwargs."""
        res = decor.catch_exceptions._map_args_kwargs(self._func11, 1, b=5)
        self.assertEqual(res, {'args': (self, 1,), 'kwargs': {'b': 5}})
        res = decor.catch_exceptions._map_args_kwargs(self._func11, 1, 2)
        self.assertEqual(res, {'args': (self, 1,), 'kwargs': {'b': 2}})

    def test_18_catch_exception(self):
        """Catch TypeError and raise ValueError."""
        wrapped_f = decor.catch_exceptions([
            {
                'exception': TypeError,
                'raise_exception': ValueError,
                'msg': "%s",
            },
        ])(_func_exception)
        with self.assertRaises(ValueError):
            wrapped_f()

    def test_19_catch_exception(self):
        """Catch TypeError and raise same error."""
        wrapped_f = decor.catch_exceptions([
            {
                'exception': TypeError,
                'msg': "%s",
            },
        ])(_func_exception)
        with self.assertRaises(TypeError):
            wrapped_f()

    def test_20_stdout_input(self):
        """Use stdout input decorator with default options."""
        wrapper_f = decor.stdout_input()(_func10)
        stdout = log.capture_output(wrapper_f)
        # \n is added by print statement.
        self.assertEqual(stdout, '_func10()\n')
        stdout = log.capture_output(
            wrapper_f, args=(10, '20'), kwargs={'a': 30})
        # \n is added by print statement.
        self.assertEqual(stdout, "_func10(10, '20', a=30)\n")

    def test_21_stdout_input(self):
        """Use stdout input decorator with custom options."""
        wrapper_f = decor.stdout_input(options={
            'stdout_writer': print,
            'no_first_arg': True,
            'prefix': 'custom ',
        })(_func10)
        stdout = log.capture_output(wrapper_f)
        self.assertEqual(stdout, 'custom _func10()\n')
        wrapper_f = decor.stdout_input(options={
            'stdout_getter': lambda *args, **kwargs: print,
            'command': True
        })(_func10)
        stdout = log.capture_output(
            wrapper_f, args=(10, '20'), kwargs={'a': 30})
        self.assertEqual(stdout, "_func10 10 20 a=30\n")

    def test_22_stdout_output(self):
        """Use stdout output decorator with default options."""
        wrapper_f = decor.stdout_output()(_func11)
        stdout = log.capture_output(wrapper_f)
        self.assertEqual(stdout, '123\n')
        stdout = log.capture_output(
            wrapper_f, args=(10, '20'), kwargs={'a': 30})
        self.assertEqual(stdout, '123\n')

    def test_23_stdout_output(self):
        """Use stdout output decorator with custom options."""
        wrapper_f = decor.stdout_output(options={
            'stdout_writer': print,
            'prefix': 'custom ',
        })(_func11)
        stdout = log.capture_output(wrapper_f)
        self.assertEqual(stdout, 'custom 123\n')
        wrapper_f = decor.stdout_output(options={
            'stdout_getter': lambda *args, **kwargs: print,
        })(_func11)
        stdout = log.capture_output(
            wrapper_f, args=(10, '20'), kwargs={'a': 30})
        self.assertEqual(stdout, "123\n")

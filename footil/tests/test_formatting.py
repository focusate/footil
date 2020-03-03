import xml.etree.ElementTree as ET
from footil import formatting
from footil.lib import pattern_methods

from .common import TestFootilCommon, Dummy


class TestFormatting(TestFootilCommon):
    """Test cases for formatting module."""

    def test_01_formatted_exception_1(self):
        """Use default formatting for exception list (no formatter)."""
        res = formatting._get_formatted_exception(self.dummy_lst)
        self.assertEqual(res, 'traceback:\nsomething_went_wrong\nsome_error\n')

    def test_02_formatted_exception_2(self):
        """Use html formatter for exception list.

        Case: full message is showed.
        """
        res = formatting._get_formatted_exception(
            self.dummy_lst, formatter=formatting.format_list_to_html())
        dest = (
            '<div style="line-height: 1"><p>traceback:</p>'
            '<p>something_went_wrong</p>'
            '<p>some_error</p>'
            '</div>')
        self.assertEqual(res, dest)
        # Format it with line_height specified.
        res = formatting._get_formatted_exception(
            self.dummy_lst, formatter=formatting.format_list_to_html(
                line_height=0))
        dest = (
            '<div style="line-height: 0"><p>traceback:</p>'
            '<p>something_went_wrong</p>'
            '<p>some_error</p>'
            '</div>')
        self.assertEqual(res, dest)

    def test_03_formatted_exception_3(self):
        """Use html formatter for exception list.

        Case: part of message is showed. Default bootstrap collapse is
        used to toggle hidden part of message.
        """
        # Format it with collapse configuration.
        res = formatting._get_formatted_exception(
            self.dummy_lst, formatter=formatting.format_list_to_html(
                collapse_cfg={'max_lines': 1, 'collapse_id': 'test_1'}))
        tree = ET.ElementTree(ET.fromstring(res))
        # Check tree if it matches expected structure.
        root = tree.getroot()
        self.assertEqual(root.items(), [('style', 'line-height: 1')])
        # Check root children.
        root_childs = root.getchildren()
        self.assertEqual(len(root_childs), 3)
        p = root_childs[0]
        self.assertEqual(p.text, 'traceback:')
        div = root_childs[1]
        self.assertEqual(
            sorted(div.items()), [('class', 'collapse'), ('id', 'test_1'), ])
        div_childs = div.getchildren()
        self.assertEqual(len(div_childs), 2)
        self.assertEqual(div_childs[0].text, 'something_went_wrong')
        self.assertEqual(div_childs[1].text, 'some_error')
        a = root_childs[2]
        self.assertEqual(
            sorted(a.items()),
            [
                ('class', 'btn btn-link'),
                ('data-target', '#test_1'),
                ('data-toggle', 'collapse')
            ]
        )
        self.assertEqual(a.text, 'Toggle More')
        # Check if uuid4 is used when collapse_id is not specified.
        res = formatting._get_formatted_exception(
            self.dummy_lst, formatter=formatting.format_list_to_html(
                collapse_cfg={'max_lines': 1}))
        tree = ET.ElementTree(ET.fromstring(res))
        root_childs = tree.getroot().getchildren()
        div = root_childs[1]
        div_id = dict(div.items())['id']
        a = root_childs[2]
        a_data_target = dict(a.items())['data-target']
        # Slice to remove '#'.
        self.assertEqual(div_id, a_data_target[1:])

    def test_04_formatted_exception_4(self):
        """Use html formatter for exception list.

        Case: part of message is showed. Custom attribute is
        included to specify part that needs to be hidden.
        """
        res = formatting._get_formatted_exception(
            self.dummy_lst,
            formatter=formatting.format_list_to_html(
                collapse_cfg={
                    'max_lines': 1,
                    'attr_toggle': ('data-o-mail-quote', 1)
                }
            )
        )
        tree = ET.ElementTree(ET.fromstring(res))
        # Check tree if it matches expected structure.
        root = tree.getroot()
        self.assertEqual(root.items(), [('style', 'line-height: 1')])
        # Check root children.
        root_childs = root.getchildren()
        self.assertEqual(len(root_childs), 2)
        p = root_childs[0]
        self.assertEqual(p.text, 'traceback:')
        div = root_childs[1]
        self.assertEqual(div.items(), [('data-o-mail-quote', '1')])
        div_childs = div.getchildren()
        self.assertEqual(len(div_childs), 2)
        self.assertEqual(div_childs[0].text, 'something_went_wrong')
        self.assertEqual(div_childs[1].text, 'some_error')

    def test_05_generate_name_0(self):
        """Get name without using any attributes."""
        # Modify dummy object by adding two attributes.
        dummy = Dummy(a=10, b='test')
        res = formatting.generate_name('a / b', dummy)
        self.assertEqual(res, 'a / b')

    def test_06_generate_name_1(self):
        """Get name using two attributes."""
        # Modify dummy object by adding two attributes.
        dummy = Dummy(a=10, b='test')
        res = formatting.generate_name('{a} / {b}', dummy)
        self.assertEqual(res, '10 / test')

    def test_07_generate_name_2(self):
        """Specify non existing attribute on pattern to raise error."""
        dummy = Dummy(c=5)
        self.assertRaises(
            AttributeError,
            formatting.generate_name,
            '{b} / {c}',
            dummy)

    def test_08_generate_name_3(self):
        """Strip falsy attributes."""
        dummy = Dummy(a=False, b='test')
        dummy.a = False
        res = formatting.generate_name(
            '{a} / {b}', dummy, strip_falsy=True)
        self.assertEqual('test', res)

    def test_09_generate_name_4(self):
        """Do Not strip falsy attributes."""
        dummy = Dummy(a=False, b='test')
        res = formatting.generate_name(
            '{a} / {b}', dummy, strip_falsy=False)
        self.assertEqual('False / test', res)

    def test_10_generate_name_5(self):
        """Get name with attributes of attribute (n-depth access)."""
        dummy = Dummy(c=10)
        dummy2 = Dummy(b=dummy)
        dummy3 = Dummy(a=dummy2, b='something')
        res = formatting.generate_name(
            '{a.b.c} | {b}', dummy3, strip_falsy=True)
        self.assertEqual('10 | something', res)
        # Now by make c attr falsy to be stripped away.
        dummy.c = 0
        res = formatting.generate_name(
            '{a.b.c} | {b}', dummy3, strip_falsy=True)
        self.assertEqual('something', res)
        # Now do not strip falsy attribute.
        res = formatting.generate_name(
            '{a.b.c} | {b}', dummy3, strip_falsy=False)
        self.assertEqual('0 | something', res)

    def test_11_generate_name_6(self):
        """Get name with recursive attributes pattern access."""
        dummy = Dummy(parent=False, name='d1', z='test0')
        dummy2 = Dummy(parent=dummy, name='d2')
        dummy3 = Dummy(parent=dummy2, name='d3', z='test')
        res = formatting.generate_name(
            '$join_parent_attrs("parent", "name", ".", "False") - {z}',
            dummy3,
            strip_falsy=False)
        self.assertEqual(res, "d3.d2.d1 - test")
        res = formatting.generate_name(
            '$join_parent_attrs("parent", "name") - {z}',
            dummy3,
            strip_falsy=False)
        self.assertEqual(res, "d1 / d2 / d3 - test")
        res = formatting.generate_name(
            '$join_parent_attrs("parent", "name") - {z}',
            dummy,
            strip_falsy=False)
        self.assertEqual(res, "d1 - test0")

    def test_12_join_parent_attrs(self):
        """Join all truthy parents attributes."""
        dummy = Dummy(parent=False, name='d1')
        dummy2 = Dummy(parent=dummy, name='d2')
        dummy3 = Dummy(parent=dummy2, name='d3', z='test')
        res = pattern_methods._join_parent_attrs(
            dummy3, 'parent', 'name', '.', _reversed=False)
        self.assertEqual(res, 'd3.d2.d1')
        res = pattern_methods._join_parent_attrs(
            dummy3, 'parent', 'name', '.', _reversed=True)
        self.assertEqual(res, 'd1.d2.d3')
        # Make it skip one parent.
        dummy4 = Dummy(parent=dummy3, name='d4')
        res = pattern_methods._join_parent_attrs(
            dummy4, 'parent.parent', 'name', _reversed=False)
        self.assertEqual(res, 'd4 / d2')
        res = pattern_methods._join_parent_attrs(
            dummy4, 'parent.parent', 'name', _reversed=True)
        self.assertEqual(res, 'd2 / d4')
        # Modify some values to be non string.
        dummy.name = 1
        dummy2.name = False
        res = pattern_methods._join_parent_attrs(
            dummy3, 'parent', 'name', '.',)
        self.assertEqual(res, '1.False.d3')

    def test_13_generate_names_1(self):
        """Generate names using iterator object. Default key."""
        dummy_1 = Dummy(c=10)
        dummy_1_2 = Dummy(b=dummy_1)
        dummy_1_3 = Dummy(a=dummy_1_2, b='something', id=1)
        dummy_2 = Dummy(c=50)
        dummy_2_2 = Dummy(b=dummy_2)
        dummy_2_3 = Dummy(a=dummy_2_2, b='something2', id=2)
        objects_lst = [dummy_1_3, dummy_2_3]
        res = formatting.generate_names(
            {'pattern': '{a.b.c} | {b}', 'objects': objects_lst})
        self.assertEqual(res, [(1, '10 | something'), (2, '50 | something2')])
        # Generate names with empty list as objects value.
        res = formatting.generate_names(
            {'pattern': '{a.b.c} | {b}', 'objects': []})
        self.assertEqual(res, [])
        # Generate names with empty pattern.
        res = formatting.generate_names(
            {'pattern': '', 'objects': objects_lst})
        self.assertEqual(res, [(1, ''), (2, '')])

    def test_14_generate_names_2(self):
        """Generate names using iterator object. Specified key."""
        dummy_1 = Dummy(c=10)
        dummy_1_2 = Dummy(b=dummy_1)
        dummy_1_3 = Dummy(a=dummy_1_2, b='something', key=1)
        dummy_2 = Dummy(c=50)
        dummy_2_2 = Dummy(b=dummy_2)
        dummy_2_3 = Dummy(a=dummy_2_2, b='something2', key=2)
        objects_lst = [dummy_1_3, dummy_2_3]
        res = formatting.generate_names(
            {'pattern': '{a.b.c} | {b}', 'objects': objects_lst, 'key': 'key'})
        self.assertEqual(res, [(1, '10 | something'), (2, '50 | something2')])

    def test_15_generate_names_3(self):
        """Try to call generate_names without required keys."""
        self.assertRaises(
            ValueError, formatting.generate_names, {'pattern': ''})
        self.assertRaises(
            ValueError, formatting.generate_names, {'objects': []})

    def test_16_replace_email_name_1(self):
        """Replace name for email 'A <a@b.com>'."""
        email = formatting.replace_email_name('B', 'A <a@b.com>')
        self.assertEqual(email, 'B <a@b.com>')

    def test_17_replace_email_name_2(self):
        """Replace name for email '<a@b.com>'."""
        email = formatting.replace_email_name('B', '<a@b.com>')
        self.assertEqual(email, 'B <a@b.com>')

    def test_18_replace_email_name_3(self):
        """Replace name for email 'a@b.com'."""
        email = formatting.replace_email_name('B', 'a@b.com')
        self.assertEqual(email, 'B <a@b.com>')

    def test_19_replace_email_name_4(self):
        """Replace name for email 'A a@b.com'."""
        email = formatting.replace_email_name('B', 'A a@b.com')
        self.assertEqual(email, 'B <A a@b.com>')

    def test_20_replace_email_name_5(self):
        """Replace name for email ''."""
        email = formatting.replace_email_name('B', '')
        self.assertEqual(email, 'B <>')

    def test_21_replace_email_name_6(self):
        """Replace name for email '' when name is ''."""
        email = formatting.replace_email_name('', '')
        self.assertEqual(email, '')

    def test_22_replace_email_1(self):
        """Replace email for email 'A <a@b.com>'."""
        email = formatting.replace_email('c@d.com', 'A <a@b.com>')
        self.assertEqual(email, 'A <c@d.com>')

    def test_23_replace_email_2(self):
        """Replace email for email '<a@b.com>'."""
        email = formatting.replace_email('<c@d.com>', '<a@b.com>')
        self.assertEqual(email, '<c@d.com>')

    def test_24_replace_email_3(self):
        """Replace email for email 'a@b.com'."""
        email = formatting.replace_email('c@d.com', 'a@b.com')
        self.assertEqual(email, 'c@d.com')

    def test_25_replace_email_4(self):
        """Replace email for email ''."""
        email = formatting.replace_email('c@d.com', '')
        self.assertEqual(email, 'c@d.com')

    def test_26_replace_email_5(self):
        """Replace email for email '' when name is ''."""
        email = formatting.replace_email('', '')
        self.assertEqual(email, '')

    def test_27_replace_ic_1(self):
        """Replace 'HelLo' with default replace_with ('')."""
        new_term = formatting.replace_ic('Hello and heLLo And hello', 'HelLo')
        self.assertEqual(new_term, ' and  And ')

    def test_28_replace_ic_2(self):
        """Replace 'HelLo' with 'byE' (existing fragment)."""
        new_term = formatting.replace_ic(
            'Hello and heLLo And hello', 'HelLo', 'byE')
        self.assertEqual(new_term, 'byE and byE And byE')

    def test_29_replace_ic_3(self):
        """Replace 'byE' with 'HelLo' (non existing fragment)."""
        new_term = formatting.replace_ic(
            'Hello and heLLo And hello', 'byE', 'HelLo')
        # Term should left unchanged.
        self.assertEqual(new_term, 'Hello and heLLo And hello')

    def test_30_strip_space(self):
        """Strip string without spaces."""
        s = formatting.strip_space('abc')
        self.assertEqual(s, 'abc')

    def test_31_strip_space(self):
        """Strip string with white space only."""
        s = formatting.strip_space('\tabc ')
        self.assertEqual(s, 'abc')

    def test_32_strip_space(self):
        """Strip string with white space and space around chars."""
        s = formatting.strip_space('\tab c \nd\r')
        self.assertEqual(s, 'abcd')

    def test_33_format_func_input(self):
        """Format input as normal function.

        Case: args, kwargs passed.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            args=('a', 'b'),
            kwargs={'x': 10})
        self.assertEqual(
            pattern % pattern_args, "my_func('a', 'b', x=10)")

    def test_34_format_func_input(self):
        """Format input as normal function.

        Case: args, kwargs passed. First arg ignored.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            no_first_arg=True,
            args=('a', 'b'),
            kwargs={'x2': '20'}
        )
        self.assertEqual(
            pattern % pattern_args, "my_func('b', x2='20')")

    def test_35_format_func_input(self):
        """Format input as normal function.

        Case: args only
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            args=('a', 'b'),
        )
        self.assertEqual(
            pattern % pattern_args, "my_func('a', 'b')")

    def test_36_format_func_input(self):
        """Format input as normal function.

        Case: kwargs only
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            kwargs={'x': 10}
        )
        self.assertEqual(
            pattern % pattern_args, "my_func(x=10)")

    def test_37_format_func_input(self):
        """Format input as normal function.

        Case 1: no args, kwargs
        Case 2: no args, kwargs and no first arg.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
        )
        self.assertEqual(
            pattern % pattern_args, "my_func()")
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            no_first_arg=True,
        )
        self.assertEqual(
            pattern % pattern_args, "my_func()")

    def test_38_format_func_input(self):
        """Format input as shell command.

        Case: args, kwargs passed.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            command=True,
            args=('a', 'b'),
            kwargs={'x': 10})
        self.assertEqual(
            pattern % pattern_args, "my_func a b x=10")

    def test_39_format_func_input(self):
        """Format input as shell command.

        Case: args, kwargs passed. First arg ignored.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            command=True,
            no_first_arg=True,
            args=('a', 'b'),
            kwargs={'x2': '20'}
        )
        self.assertEqual(
            pattern % pattern_args, "my_func b x2=20")

    def test_40_format_func_input(self):
        """Format input as shell command.

        Case: args only
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            command=True,
            args=('a', 'b'),
        )
        self.assertEqual(
            pattern % pattern_args, "my_func a b")

    def test_41_format_func_input(self):
        """Format input as shell command.

        Case: kwargs only
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            command=True,
            kwargs={'x2': "'20'"}
        )
        self.assertEqual(
            pattern % pattern_args, "my_func x2='20'")

    def test_42_format_func_input(self):
        """Format input as shell command.

        Case 1: no args, kwargs
        Case 2: no args, kwargs and no first arg.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            command=True
        )
        self.assertEqual(
            pattern % pattern_args, "my_func")
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            command=True,
            no_first_arg=True,
        )
        self.assertEqual(
            pattern % pattern_args, "my_func")

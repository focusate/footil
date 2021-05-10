import xml.etree.ElementTree as ET
from footil import formatting
from footil.tools import string_pattern_methods

from .common import TestFootilCommon, Dummy


class TestFormatting(TestFootilCommon):
    """Test cases for formatting module."""

    def test_01_formatted_exception(self):
        """Use default formatting for exception list (no formatter)."""
        res = formatting._get_formatted_exception(self.dummy_lst)
        self.assertEqual(res, 'traceback:\nsomething_went_wrong\nsome_error\n')

    def test_02_formatted_exception(self):
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

    def test_03_formatted_exception(self):
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
        root_childs = list(root)
        self.assertEqual(len(root_childs), 3)
        p = root_childs[0]
        self.assertEqual(p.text, 'traceback:')
        div = root_childs[1]
        self.assertEqual(
            sorted(div.items()), [('class', 'collapse'), ('id', 'test_1'), ])
        div_childs = list(div)
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
        root_childs = list(tree.getroot())
        div = root_childs[1]
        div_id = dict(div.items())['id']
        a = root_childs[2]
        a_data_target = dict(a.items())['data-target']
        # Slice to remove '#'.
        self.assertEqual(div_id, a_data_target[1:])

    def test_04_formatted_exception(self):
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
        root_childs = list(root)
        self.assertEqual(len(root_childs), 2)
        p = root_childs[0]
        self.assertEqual(p.text, 'traceback:')
        div = root_childs[1]
        self.assertEqual(div.items(), [('data-o-mail-quote', '1')])
        div_childs = list(div)
        self.assertEqual(len(div_childs), 2)
        self.assertEqual(div_childs[0].text, 'something_went_wrong')
        self.assertEqual(div_childs[1].text, 'some_error')

    def test_05_generate_name(self):
        """Get name without using any attributes."""
        # Modify dummy object by adding two attributes.
        dummy = Dummy(a=10, b='test')
        res = formatting.generate_name('a / b', dummy)
        self.assertEqual(res, 'a / b')

    def test_06_generate_name(self):
        """Get name using three attributes (one falsy)."""
        # Modify dummy object by adding three attributes. Third is False
        # to not be included.
        dummy = Dummy(a=10, b='test', c=False)
        # Adding parenthesis, to make sure parts without attributes are
        # handled properly.
        res = formatting.generate_name('{a} / ({b}) ({c})', dummy)
        self.assertEqual(res, '10 / (test)')

    def test_07_generate_name(self):
        """Specify non existing attribute on pattern to raise error."""
        dummy = Dummy(c=5)
        self.assertRaises(
            AttributeError,
            formatting.generate_name,
            '{b} / {c}',
            dummy)

    def test_08_generate_name(self):
        """Strip falsy attributes."""
        dummy = Dummy(a=False, b='test')
        res = formatting.generate_name(
            '{a} / {b}', dummy, strip_falsy=True)
        self.assertEqual(res, 'test')
        dummy = Dummy(a=False, b='test', c=False, d='test2')
        res = formatting.generate_name(
            '{a} / {b} / {c} / {d}', dummy, strip_falsy=True)
        self.assertEqual(res, 'test / test2')

    def test_09_generate_name(self):
        """Do Not strip falsy attributes."""
        dummy = Dummy(a=False, b='test')
        res = formatting.generate_name(
            '{a} / {b}', dummy, strip_falsy=False)
        self.assertEqual(res, 'False / test')

    def test_10_generate_name(self):
        """Get name with attributes of attribute (n-depth access)."""
        dummy = Dummy(c=10)
        dummy2 = Dummy(b=dummy)
        dummy3 = Dummy(a=dummy2, b='something')
        res = formatting.generate_name(
            '{a.b.c} | {b}', dummy3, strip_falsy=True)
        self.assertEqual(res, '10 | something')
        # Now by make c attr falsy to be stripped away.
        dummy.c = 0
        res = formatting.generate_name(
            '{a.b.c} | {b}', dummy3, strip_falsy=True)
        self.assertEqual(res, 'something')
        # Now do not strip falsy attribute.
        res = formatting.generate_name(
            '{a.b.c} | {b}', dummy3, strip_falsy=False)
        self.assertEqual(res, '0 | something')

    def test_11_generate_name(self):
        """Convert old style formatting and then generate name."""
        fmt = '%(x)s\n%(y)s\n%(j)s'
        new_fmt = formatting.to_new_named_format(fmt)
        self.assertEqual(new_fmt, '{x}\n{y}\n{j}')
        dummy = Dummy(x=33, y=False, j=11)
        res = formatting.generate_name(new_fmt, dummy, strip_falsy=True)
        self.assertEqual(res, '33\n11')

    def test_12_generate_name(self):
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

    def test_13_join_parent_attrs(self):
        """Join all truthy parents attributes."""
        dummy = Dummy(parent=False, name='d1')
        dummy2 = Dummy(parent=dummy, name='d2')
        dummy3 = Dummy(parent=dummy2, name='d3', z='test')
        res = string_pattern_methods._join_parent_attrs(
            dummy3, 'parent', 'name', '.', _reversed=False)
        self.assertEqual(res, 'd3.d2.d1')
        res = string_pattern_methods._join_parent_attrs(
            dummy3, 'parent', 'name', '.', _reversed=True)
        self.assertEqual(res, 'd1.d2.d3')
        # Make it skip one parent.
        dummy4 = Dummy(parent=dummy3, name='d4')
        res = string_pattern_methods._join_parent_attrs(
            dummy4, 'parent.parent', 'name', _reversed=False)
        self.assertEqual(res, 'd4 / d2')
        res = string_pattern_methods._join_parent_attrs(
            dummy4, 'parent.parent', 'name', _reversed=True)
        self.assertEqual(res, 'd2 / d4')
        # Modify some values to be non string.
        dummy.name = 1
        dummy2.name = False
        res = string_pattern_methods._join_parent_attrs(
            dummy3, 'parent', 'name', '.',)
        self.assertEqual(res, '1.False.d3')

    def test_14_generate_names(self):
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

    def test_15_generate_names(self):
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

    def test_16_generate_names(self):
        """Try to call generate_names without required keys."""
        self.assertRaises(
            ValueError, formatting.generate_names, {'pattern': ''})
        self.assertRaises(
            ValueError, formatting.generate_names, {'objects': []})

    def test_17_replace_email_name(self):
        """Replace name for email 'A <a@b.com>'."""
        email = formatting.replace_email_name('B', 'A <a@b.com>')
        self.assertEqual(email, 'B <a@b.com>')

    def test_18_replace_email_name(self):
        """Replace name for email '<a@b.com>'."""
        email = formatting.replace_email_name('B', '<a@b.com>')
        self.assertEqual(email, 'B <a@b.com>')

    def test_19_replace_email_name(self):
        """Replace name for email 'a@b.com'."""
        email = formatting.replace_email_name('B', 'a@b.com')
        self.assertEqual(email, 'B <a@b.com>')

    def test_20_replace_email_name(self):
        """Replace name for email 'A a@b.com'."""
        email = formatting.replace_email_name('B', 'A a@b.com')
        self.assertEqual(email, 'B <A a@b.com>')

    def test_21_replace_email_name(self):
        """Replace name for email ''."""
        email = formatting.replace_email_name('B', '')
        self.assertEqual(email, 'B <>')

    def test_22_replace_email_name(self):
        """Replace name for email '' when name is ''."""
        email = formatting.replace_email_name('', '')
        self.assertEqual(email, '')

    def test_23_replace_email(self):
        """Replace email for email 'A <a@b.com>'."""
        email = formatting.replace_email('c@d.com', 'A <a@b.com>')
        self.assertEqual(email, 'A <c@d.com>')

    def test_24_replace_email(self):
        """Replace email for email '<a@b.com>'."""
        email = formatting.replace_email('<c@d.com>', '<a@b.com>')
        self.assertEqual(email, '<c@d.com>')

    def test_25_replace_email(self):
        """Replace email for email 'a@b.com'."""
        email = formatting.replace_email('c@d.com', 'a@b.com')
        self.assertEqual(email, 'c@d.com')

    def test_26_replace_email(self):
        """Replace email for email ''."""
        email = formatting.replace_email('c@d.com', '')
        self.assertEqual(email, 'c@d.com')

    def test_27_replace_email(self):
        """Replace email for email '' when name is ''."""
        email = formatting.replace_email('', '')
        self.assertEqual(email, '')

    def test_28_email_to_domain(self):
        """Extract domain from 'John Doe <a@b.com>' ."""
        self.assertEqual(
            formatting.email_to_domain('John Doe <a@b.com>'),
            'b.com'
        )

    def test_29_email_to_domain(self):
        r"""Extract domain from '\"John Doe\"a@b.com'."""
        self.assertEqual(
            formatting.email_to_domain('"John Doe" a@b.com'),
            'b.com'
        )

    def test_30_email_to_domain(self):
        """Extract domain from 'a@b.com'."""
        self.assertEqual(
            formatting.email_to_domain('a@b.com'),
            'b.com'
        )

    def test_31_email_to_domain(self):
        """Try to extract domain from ''."""
        self.assertEqual(
            formatting.email_to_domain(''),
            ''
        )

    def test_32_email_to_domain(self):
        """Try to extract domain from 'a-eta-b.com'."""
        self.assertEqual(
            formatting.email_to_domain('a-eta-b.com'),
            ''
        )

    def test_33_email_to_alias(self):
        """Extract alias from 'John Doe <a@b.com>' ."""
        self.assertEqual(
            formatting.email_to_alias('John Doe <a@b.com>'),
            'a'
        )

    def test_34_email_to_alias(self):
        r"""Extract alias from '\"John Doe\"a@b.com'."""
        self.assertEqual(
            formatting.email_to_alias('"John Doe" <a@b.com>'),
            'a'
        )

    def test_35_email_to_alias(self):
        """Extract alias from 'a@b.com'."""
        self.assertEqual(
            formatting.email_to_alias('a@b.com'),
            'a'
        )

    def test_36_email_to_alias(self):
        """Try to extract alias from ''."""
        self.assertEqual(
            formatting.email_to_alias(''),
            ''
        )

    def test_37_email_to_alias(self):
        """Try to extract alias from 'a-eta-b.com'."""
        self.assertEqual(
            formatting.email_to_alias('a-eta-b.com'),
            ''
        )

    def test_38_to_new_named_format(self):
        """Convert 'abcd' to new named args format."""
        new_fmt = formatting.to_new_named_format('abcd')
        self.assertEqual(new_fmt, 'abcd')

    def test_39_to_new_named_format(self):
        """Convert '%(x)s - %(y)s' to new named args format."""
        new_fmt = formatting.to_new_named_format('%(x)s - %(y)s')
        self.assertEqual(new_fmt, '{x} - {y}')

    def test_40_to_new_named_format(self):
        """Convert '%(x)s %% %%%(y)s' to new named args format."""
        new_fmt = formatting.to_new_named_format('%(x)s %% %%%(y)s')
        self.assertEqual(new_fmt, '{x} % %{y}')

    def test_41_to_new_named_format(self):
        """Convert '{ %(x)s } - {%%%(y)s}' to new named args format."""
        new_fmt = formatting.to_new_named_format('{ %(x)s } - {%%%(y)s}')
        self.assertEqual(new_fmt, '{{ {x} }} - {{%{y}}}')

    def test_42_to_new_named_format(self):
        """Convert '%%(x)s %(y)s' to new named args format."""
        new_fmt = formatting.to_new_named_format('%%(x)s %(y)s')
        self.assertEqual(new_fmt, '%(x)s {y}')

    def test_43_to_new_named_format(self):
        """Try to convert '%(x)s % %%%(y)s' to new named args format.

        extra % is not escaped.
        """
        with self.assertRaises(ValueError):
            formatting.to_new_named_format('%(x)s % %%%(y)s')

    def test_44_to_new_pos_format(self):
        """Convert 'abcd' to new named args format."""
        new_fmt = formatting.to_new_pos_format('abcd')
        self.assertEqual(new_fmt, 'abcd')

    def test_45_to_new_pos_format(self):
        """Convert '%(x)s - %(y)s' to new named args format."""
        new_fmt = formatting.to_new_pos_format('%s - %s')
        self.assertEqual(new_fmt, '{} - {}')

    def test_46_to_new_pos_format(self):
        """Convert '%s %% %%%s' to new named args format."""
        new_fmt = formatting.to_new_pos_format('%s %% %%%s')
        self.assertEqual(new_fmt, '{} % %{}')

    def test_47_to_new_pos_format(self):
        """Convert '{ %s } - {%%%s}' to new named args format."""
        new_fmt = formatting.to_new_pos_format('{ %s } - {%%%s}')
        self.assertEqual(new_fmt, '{{ {} }} - {{%{}}}')

    def test_48_to_new_pos_format(self):
        """Try to convert '%s % %%%s' to new named args format.

        extra % is not escaped.
        """
        with self.assertRaises(ValueError):
            formatting.to_new_pos_format('%s % %%%s')

    def test_49_to_new_pos_format(self):
        """Try to convert '%s %%s' to new named args format.

        even % on placeholder s, means not enough arguments error.
        """
        with self.assertRaises(TypeError):
            formatting.to_new_pos_format('%s %%s')

    def test_50_replace_ic(self):
        """Replace 'HelLo' with default replace_with ('')."""
        new_term = formatting.replace_ic('Hello and heLLo And hello', 'HelLo')
        self.assertEqual(new_term, ' and  And ')

    def test_51_replace_ic(self):
        """Replace 'HelLo' with 'byE' (existing fragment)."""
        new_term = formatting.replace_ic(
            'Hello and heLLo And hello', 'HelLo', 'byE')
        self.assertEqual(new_term, 'byE and byE And byE')

    def test_52_replace_ic(self):
        """Replace 'byE' with 'HelLo' (non existing fragment)."""
        new_term = formatting.replace_ic(
            'Hello and heLLo And hello', 'byE', 'HelLo')
        # Term should left unchanged.
        self.assertEqual(new_term, 'Hello and heLLo And hello')

    def test_53_strip_space(self):
        """Strip string without spaces."""
        s = formatting.strip_space('abc')
        self.assertEqual(s, 'abc')

    def test_54_strip_space(self):
        """Strip string with white space only."""
        s = formatting.strip_space('\tabc ')
        self.assertEqual(s, 'abc')

    def test_55_strip_space(self):
        """Strip string with white space and space around chars."""
        s = formatting.strip_space('\tab c \nd\r')
        self.assertEqual(s, 'abcd')

    def test_56_format_func_input(self):
        """Format input as normal function.

        Case: args, kwargs passed.
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            args=('a', 'b'),
            kwargs={'x': 10})
        self.assertEqual(
            pattern % pattern_args, "my_func('a', 'b', x=10)")

    def test_57_format_func_input(self):
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

    def test_58_format_func_input(self):
        """Format input as normal function.

        Case: args only
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            args=('a', 'b'),
        )
        self.assertEqual(
            pattern % pattern_args, "my_func('a', 'b')")

    def test_59_format_func_input(self):
        """Format input as normal function.

        Case: kwargs only
        """
        pattern, pattern_args = formatting.format_func_input(
            'my_func',
            kwargs={'x': 10}
        )
        self.assertEqual(
            pattern % pattern_args, "my_func(x=10)")

    def test_60_format_func_input(self):
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

    def test_61_format_func_input(self):
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

    def test_62_format_func_input(self):
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

    def test_63_format_func_input(self):
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

    def test_64_format_func_input(self):
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

    def test_65_format_func_input(self):
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

    def test_66_split_force(self):
        """Split 'a b c' into 3 parts.

        Case: sep=None, maxsplit=-1, defaults not used.
        """
        self.assertEqual(
            formatting.split_force('a b c'),
            ['a', 'b', 'c']
        )

    def test_67_split_force(self):
        """Split 'a b c' into 2 parts.

        Case: sep=None, maxsplit=1, default=None.
        """
        self.assertEqual(
            formatting.split_force('a b c', maxsplit=1),
            ['a', 'b c']
        )

    def test_68_split_force(self):
        """Split 'a b c' into 4 parts.

        Case: sep=None, maxsplit=3, default=None.
        """
        self.assertEqual(
            formatting.split_force('a b c', maxsplit=3),
            ['a', 'b', 'c', None]
        )

    def test_69_split_force(self):
        """Split 'abc' into 4 parts.

        Case: sep=' ', maxsplit=3, default=''.
        """
        self.assertEqual(
            formatting.split_force(
                'abc', sep=' ', maxsplit=3, default=''),
            ['abc', '', '', '']
        )

    def test_70_split_force(self):
        """Split 'a b c d' into 1 part.

        Case: sep=' ', maxsplit=0, default=''.
        """
        self.assertEqual(
            formatting.split_force(
                'a b c d', sep=' ', maxsplit=0, default=''
            ),
            ['a b c d']
        )

    def test_71_format_digits(self):
        """Format string with digits/other chars."""
        self.assertEqual(formatting.format_digits('123 abc'), '123')

    def test_72_format_digits(self):
        """Format string with digits only."""
        self.assertEqual(formatting.format_digits('123'), '123')

    def test_73_format_digits(self):
        """Format string with non digits only."""
        self.assertEqual(formatting.format_digits('abc '), '')

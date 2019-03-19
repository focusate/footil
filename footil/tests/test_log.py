import unittest

from footil import log
import xml.etree.ElementTree as ET


class TestLog(unittest.TestCase):
    """Class to test logging/formatting helpers."""

    @classmethod
    def setUpClass(cls):
        """Set up data for log tests."""
        super(TestLog, cls).setUpClass()
        cls.dummy_lst = [
            'traceback:\n', 'something_went_wrong\n', 'some_error\n']

    def test_capture_output_1(self):
        """Capture output from print."""
        res = log.capture_output(print, args=('test',))
        self.assertEqual(res, 'test\n')

    def test_formatted_exception_1(self):
        """Use default formatting for exception list (no formatter)."""
        res = log._get_formatted_exception(self.dummy_lst)
        self.assertEqual(res, 'traceback:\nsomething_went_wrong\nsome_error\n')

    def test_formatted_exception_2(self):
        """Use html formatter for exception list.

        Case: full message is showed.
        """
        res = log._get_formatted_exception(
            self.dummy_lst, formatter=log.format_list_to_html())
        dest = (
            '<div style="line-height: 1"><p>traceback:</p>'
            '<p>something_went_wrong</p>'
            '<p>some_error</p>'
            '</div>')
        self.assertEqual(res, dest)
        # Format it with line_height specified.
        res = log._get_formatted_exception(
            self.dummy_lst, formatter=log.format_list_to_html(
                line_height=0))
        dest = (
            '<div style="line-height: 0"><p>traceback:</p>'
            '<p>something_went_wrong</p>'
            '<p>some_error</p>'
            '</div>')
        self.assertEqual(res, dest)

    def test_formatted_exception_3(self):
        """Use html formatter for exception list.

        Case: part of message is showed. Default bootstrap collapse is
        used to toggle hidden part of message.
        """
        # Format it with collapse configuration.
        res = log._get_formatted_exception(
            self.dummy_lst, formatter=log.format_list_to_html(
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
        res = log._get_formatted_exception(
            self.dummy_lst, formatter=log.format_list_to_html(
                collapse_cfg={'max_lines': 1}))
        tree = ET.ElementTree(ET.fromstring(res))
        root_childs = tree.getroot().getchildren()
        div = root_childs[1]
        div_id = dict(div.items())['id']
        a = root_childs[2]
        a_data_target = dict(a.items())['data-target']
        # Slice to remove '#'.
        self.assertEqual(div_id, a_data_target[1:])

    def test_formatted_exception_4(self):
        """Use html formatter for exception list.

        Case: part of message is showed. Custom attribute is
        included to specify part that needs to be hidden.
        """
        res = log._get_formatted_exception(
            self.dummy_lst,
            formatter=log.format_list_to_html(
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

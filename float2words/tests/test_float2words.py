# -*- coding: utf-8 -*-

import unittest

from float2words import float2words


class TestFloat2Words(unittest.TestCase):
    """Test float to words conversion cases."""

    def setUp(self):
        """Set up data for testing cases."""
        self.Float2Words = float2words

    def test_floatw2words_1(self):
        """Test only with required arguments."""
        self.assertEqual(
            self.Float2Words(13.23, 'en_US'),
            'thirteen, twenty-three',
            "Incorrect float conversion to words!"
        )

    def test_floatw2words_2(self):
        """Test default precision rounding."""
        self.assertEqual(
            self.Float2Words(13.235, 'en_US'),
            'thirteen, twenty-four',
            "Incorrect float conversion to words!"
        )

    def test_floatw2words_3(self):
        """Test custom precision rounding."""
        self.assertEqual(
            self.Float2Words(13.235, 'en_US', precision=1),
            'thirteen, two',
            "Incorrect float conversion to words!"
        )

    def test_floatw2words_4(self):
        """Test with currency suffixes."""
        self.assertEqual(
            self.Float2Words(13.23, 'en_US', sfx1='EUR', sfx2='ct.'),
            'thirteen EUR, twenty-three ct.',
            "Incorrect float conversion to words!"
        )

    def test_floatw2words_5(self):
        """Test with weight suffixes."""
        self.assertEqual(
            self.Float2Words(13.234, 'en_US', sfx1='kg', sfx2='g',
                             precision=3),
            'thirteen kg, two hundred and thirty-four g',
            "Incorrect float conversion to words!"
        )

    def test_floatw2words_6(self):
        """Test with ' and ' connector."""
        self.assertEqual(
            self.Float2Words(13.23, 'en_US', sfx1='kg', sfx2='g',
                             precision=3, connector=' and '),
            'thirteen kg and two hundred and thirty g',
            "Incorrect float conversion to words!"
        )

    def test_floatw2words_7(self):
        """Test with Lithuanian language and ' ir ' connector."""
        self.assertEqual(
            self.Float2Words(13.23, 'lt_LT', sfx1='kg', sfx2='g',
                             precision=3, connector=' ir '),
            'trylika kg ir du šimtai trisdešimt g',
            "Incorrect float conversion to words!"
        )

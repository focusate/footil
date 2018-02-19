# -*- coding: utf-8 -*-

import unittest

from monetary2words import monetary2words


class TestMonetary2Words(unittest.TestCase):
    """Test monetary to words conversion cases."""

    def setUp(self):
        """Set up data for testing cases."""
        self.Monetary2Words = monetary2words

    def test_monetary2words_1(self):
        """Test with not implemented currency (Czech koruna)."""
        with self.assertRaises(NotImplementedError):
            self.Monetary2Words(13.23, 'en_US', 'CHF'),

    def test_monetary2words_2(self):
        """Test with not implemented language/localization (Spanish)."""
        with self.assertRaises(NotImplementedError):
            self.Monetary2Words(13.23, 'es_ES', 'USD'),

    def test_monetary2words_3(self):
        """Test with English language (shorten code) and USD currency."""
        self.assertEqual(
            self.Monetary2Words(13.23, 'en', 'USD'),
            'thirteen USD, twenty-three ct.',
            "Monetary value was not correctly converted to words!"
        )

    def test_monetary2words_4(self):
        """Test with English language (full code) and USD currency."""
        self.assertEqual(
            self.Monetary2Words(13.23, 'en_US', 'USD'),
            'thirteen USD, twenty-three ct.',
            "Monetary value was not correctly converted to words!"
        )

    def test_monetary2words_5(self):
        """Test with Russian language (full code) and RUB currency."""
        self.assertEqual(
            self.Monetary2Words(13.23, 'ru_RU', 'RUB'),
            'тринадцать RUB, двадцать три коп.',
            "Monetary value was not correctly converted to words!"
        )

    def test_monetary2words_6(self):
        """Test with Lithuanian language (full code) and EUR currency."""
        self.assertEqual(
            self.Monetary2Words(13.23, 'lt_LT', 'EUR'),
            'trylika EUR, dvidešimt trys ct.',
            "Monetary value was not correctly converted to words!"
        )

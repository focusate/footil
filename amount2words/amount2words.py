# -*- coding: utf-8 -*-

from num2words import num2words


class Amoun2Words(object):
    """Class for amount conversion to string using num2words."""

    def get_amount_in_words(lang, amount, currency='',
                            currency_decimal='', connector=', '):
        """Convert amount to words by given optional parameters.

        Args:
            lang (str): language code (e.g. 'en_US', 'ru_RU', etc.).
            amount (float or int): amount as float or integer.
            currency (str): currency symbol (e.g. 'USD', 'EUR', etc.).
            currency_decimal (str): currency symbol of amount decimal
                part.
            connector (str): it will be put between whole and decimal
                parts in words.

        Returns:
            amount_in_words (str): amount in words.

        """
        amount_split = ('%.2f' % amount).split('.')
        main = int(amount_split[0])
        decimal_part = int(amount_split[1])
        amount_in_words = '{} {}{}{} {}'.format(
            num2words(main, lang=lang),
            currency,
            connector,
            num2words(decimal_part, lang=lang),
            currency_decimal,
        )
        return amount_in_words

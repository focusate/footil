# -*- coding: utf-8 -*-

from num2words import num2words
from decimal import Decimal, ROUND_HALF_UP


def float2words(number, lang, sfx1='', sfx2='', connector=', ',
                precision=2):
    """Convert float to words by given optional parameters.

    Args:
        number (float): float number.
        lang (str): language code (e.g. 'en_US', 'ru_RU', etc.).
        sfx1 (str): suffix for whole part of float number
            (e.g. 'USD', '$', 'kg', etc.).
        sfx2 (str): suffix for decimal part of float number.
            (e.g. 'ct.', 'g', etc.)
        connector (str): connector will be used between whole and
            decimal parts expressed in words.
        precision (int): number of digits after decimal point.

    Returns:
        number_in_words (str): float number in words.

    """
    whole_number = int(number // 1)
    # we round float number half up by given precision
    rounded_number = Decimal('%s' % number).quantize(
        Decimal('.%s' % ('0' * precision)),
        rounding=ROUND_HALF_UP
    )
    decimal_part = int((
        '%.{}f'.format(precision) % rounded_number
    ).split('.')[-1])
    # add whitespace before suffix for better readability.
    sfx1 = ' ' + sfx1 if sfx1 else sfx1
    sfx2 = ' ' + sfx2 if sfx2 else sfx2
    whole_in_words = num2words(whole_number, lang=lang) + sfx1
    decimal_in_words = num2words(decimal_part, lang=lang) + sfx2
    number_in_words = '%s' % (
        whole_in_words + connector + decimal_in_words
    )
    return number_in_words

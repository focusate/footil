# -*- coding: utf-8 -*-

from float2words import float2words

subunit_mapping = {
    'EUR': {
        # Cents
        'en': 'ct.',
        'et': 'st.',
        'lt': 'ct.',
        'lv': 'ct.',
        'pl': 'ct.',
        'ru': 'цт.',
    },
    'GBP': {
        # Pence
        'en': 'p.',
        'et': 'p.',
        'lt': 'p.',
        'lv': 'p.',
        'pl': 'p.',
        'ru': 'п.',
    },
    'PLN': {
        # Groszy
        'en': 'gr.',
        'et': 'gr.',
        'lt': 'gr.',
        'lv': 'gr.',
        'pl': 'gr.',
        'ru': 'гр.',
    },
    'RUB': {
        # Kopeks
        'en': 'kop.',
        'et': 'kop.',
        'lt': 'kap.',
        'lv': 'kap.',
        'pl': 'kop.',
        'ru': 'коп.',
    },
    'USD': {
        # Cents
        'en': 'ct.',
        'et': 'st.',
        'lt': 'ct.',
        'lv': 'ct.',
        'pl': 'ct.',
        'ru': 'цт.',
    },
}


def monetary2words(
        number, language, currency_code, connector=', ', precision=2):
    """Convert monetary to words by given optional parameters.

    Arguments:
        number (float): float number.
        language (string): the code of language
            (e.g. 'en_US', 'ru_RU', 'en', 'ru', etc.).
        currency_code (string): the code of currency (e.g. 'USD', 'EUR', etc.).
        connector (string): connector will be used between whole and
            decimal parts expressed in words.
        precision (int): number of digits after decimal point.

    Returns:
        number_in_words (string): monetary number in words.

    """
    if currency_code not in subunit_mapping:
        raise NotImplementedError(
            "Currency code '%s' is not implemented!" % currency_code)
    currency = subunit_mapping[currency_code]
    # We check if full language code is implemented and then check with first
    # two letters if it's not.
    if language not in currency:
        language = language[:2]
    if language not in currency:
        raise NotImplementedError(
            "Language '%s' is not implemented for currency '%s'!" % (
                language, currency_code))
    return float2words(number, language, currency_code, currency[language],
                       connector, precision)

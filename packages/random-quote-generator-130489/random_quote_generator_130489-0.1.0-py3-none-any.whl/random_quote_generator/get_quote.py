import random

from .quotes import quotes


def get_quote():
    """
    Get random quote

    Get randomly quote from our quotes database

    :return: selected quote
    :rtype: dict
    """

    return quotes[random.randint(0, len(quotes) - 1)]

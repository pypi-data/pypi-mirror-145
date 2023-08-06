import pytest

from patricesorter.lib.pricing import sort_prices

__author__ = "PatriceJada"
__copyright__ = "PatriceJada"
__license__ = "MIT"


def test_sort_prices():
    """API Tests"""
    t = sort_prices(['10', '1234', '2345', '3456', '4567'])
    assert t[0] == ['10', '1234', '2345', '3456', '4567']
    assert t[1].first == '10'
    assert t[1].last == '4567'

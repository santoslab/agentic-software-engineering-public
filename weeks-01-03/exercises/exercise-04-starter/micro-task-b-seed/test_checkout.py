from cart import total
from discount import apply_discount


def test_discount_applied_over_threshold():
    assert apply_discount(total([60, 50]), 100, 0.1) == 99.0


def test_no_discount_under_threshold():
    assert apply_discount(total([20, 30]), 100, 0.1) == 50

"""Tests for calculator module."""

# this import works for tox run
from dreamtim.calculator import Calculator

import pytest


def test_calculator():
    """Check are the calculations and reset() method correct"""

    calc_obj = Calculator('3.5')

    assert calc_obj.divide(7) == 0.5
    assert calc_obj.add(1.0) == 1.5
    assert calc_obj.multiply('2') == 3
    assert calc_obj.substract(5) == -2
    assert calc_obj.multiply(4) == -8

    # Root should be tested especially carefully
    assert calc_obj.root(3) ** 3 == -8
    # Because of base conversion we do not expect 2.0
    assert calc_obj.root(-3) ** (-3) == -1.9999999999999996
    assert calc_obj.root(-1/3) == -1.9999999999999996
    assert calc_obj.multiply(-4) == 7.999999999999998
    # We expect, that reset() method doesn't return anything
    assert calc_obj.reset() is None
    assert calc_obj.add(8) == 8
    assert calc_obj.root(3) == 2
    assert calc_obj.root(-3) ** (-3) == 1.9999999999999996
    assert calc_obj.reset() is None
    assert calc_obj.add(9) == 9
    assert calc_obj.root(-2) ** -2 == 9.000000000000002


def test_calculator_inmput():
    """Check wrong imput cases"""

    with pytest.raises(ValueError):
        calc_obj = Calculator('abc')

    with pytest.raises(TypeError):
        calc_obj = Calculator(1, 1, 1, 1, 1)


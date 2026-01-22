import pytest
from calculator import add, subtract, multiply, divide, calculate_velocity

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    assert subtract(-2, -2) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5
    assert multiply(0, 100) == 0

def test_divide():
    assert divide(6, 3) == 2
    assert divide(-10, 2) == -5
    assert divide(5, 2) == 2.5
    with pytest.raises(ValueError):
        divide(10, 0)

def test_calculate_velocity():
    assert calculate_velocity(100, 10) == 10
    assert calculate_velocity(0, 5) == 0
    assert calculate_velocity(50, 2) == 25
    with pytest.raises(ValueError):
        calculate_velocity(10, 0)
    with pytest.raises(ValueError):
        calculate_velocity(10, -5)

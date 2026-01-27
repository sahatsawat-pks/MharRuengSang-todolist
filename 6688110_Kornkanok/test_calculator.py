import pytest
from calculator import add, subtract, multiply, divide, velocity

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    assert divide(-6, 2) == -3

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)

def test_velocity():
    assert velocity(100, 10) == 10
    assert velocity(50, 2) == 25
    assert velocity(0, 5) == 0

def test_velocity_zero_time():
    with pytest.raises(ValueError, match="Time cannot be zero"):
        velocity(10, 0)
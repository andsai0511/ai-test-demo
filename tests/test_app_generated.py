import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from app import add, subtract, multiply, divide

def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-2, -2) == -4
    assert add(-2, 2) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(-1, 1) == -2
    assert subtract(0, 0) == 0
    assert subtract(-2, -2) == 0
    assert subtract(-2, 2) == -4

def test_multiply():
    assert multiply(3, 5) == 15
    assert multiply(-1, 1) == -1
    assert multiply(0, 0) == 0
    assert multiply(-2, -2) == 4
    assert multiply(-2, 2) == -4

def test_divide():
    assert divide(10, 2) == 5
    assert divide(-10, 2) == -5
    assert divide(0, 2) == 0
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
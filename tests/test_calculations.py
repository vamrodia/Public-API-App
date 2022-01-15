import pytest
from app.calculations import add


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 5, 12),
    (12, 12, 24)
])
def test_add(num1, num2, expected):
    print("Testing Add Function")
    assert add(num1, num2) == expected

"""Tests for the example module."""

from drop_table_regrets.example import add_numbers, greet


def test_greet_default() -> None:
    """Test greet with default name."""
    assert greet() == "Hello, World!"


def test_greet_custom_name() -> None:
    """Test greet with custom name."""
    assert greet("Alice") == "Hello, Alice!"


def test_add_numbers() -> None:
    """Test adding two numbers."""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0

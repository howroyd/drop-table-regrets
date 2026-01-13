"""Tests for the package initialization."""

import drop_table_regrets


def test_version() -> None:
    """Test that version is defined."""
    assert hasattr(drop_table_regrets, "__version__")
    assert drop_table_regrets.__version__ == "0.1.0"


def test_greet_export() -> None:
    """Test that greet is exported from main package."""
    assert hasattr(drop_table_regrets, "greet")
    assert drop_table_regrets.greet() == "Hello, World!"
